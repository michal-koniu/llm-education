# 06 · Server engines: vLLM, SGLang and friends

**Why this chapter.** So far you have been living in the world of a single user and a single token stream: llama.cpp, llama-swap, one model on four cards. This chapter shows the other world — engines built so that **one machine can serve hundreds of concurrent requests** and do it as cheaply as possible per token. After reading it, you will be able to: explain why the KV cache is the server's main problem and how paging (*PagedAttention*) solves it; trace a request's path through vLLM from the HTTP server to the GPU kernel; tell how vLLM's hashed block chain differs from SGLang's radix tree; assess what of this stack can run on your four Radeon R9700 (gfx1201) cards and what cannot; and decide when it is worth leaving llama.cpp at all.

> ⚠️ **Nothing here was run or measured by me.** The whole chapter is desk research and code reading: vLLM at commit `b7701fc` (2026-10-19), SGLang `aaa9388`, TensorRT-LLM `7695494`, plus the GitHub API and project pages. As of **19 October 2026**. Everything about running on gfx1201 is an inference from code and documentation, not a test result. Performance numbers come from projects and companies (marked *(project's own claim)* / *(company's own claim)*) — they are not independent and must not be mixed across different hardware.

**Table of contents**

1. [Why a server engine is a different beast than a desktop one](#1-why-a-server-engine-is-a-different-beast-than-a-desktop-one)
2. [vLLM from the inside](#2-vllm-from-the-inside)
3. [vLLM on the R9700 (gfx1201)](#3-vllm-on-the-r9700-gfx1201)
4. [SGLang from the inside](#4-sglang-from-the-inside)
5. [TensorRT-LLM, TGI (archive and lesson), LMDeploy](#5-tensorrt-llm-tgi-archive-and-lesson-lmdeploy)
6. [Cluster layers: Dynamo, llm-d, LMCache, FlashInfer, FlashAttention, Modular MAX](#6-cluster-layers-dynamo-llm-d-lmcache-flashinfer-flashattention-modular-max)
7. [Comparison table: vLLM, SGLang, TensorRT-LLM, llama.cpp](#7-comparison-table-vllm-sglang-tensorrt-llm-llamacpp)
8. [What this means for the reference setup](#8-what-this-means-for-the-reference-setup)

Tag convention in the text: no tag = verified in code or in a primary source; *(project's own claim)* / *(company's own claim)* = the project's own claim; *(press report)* / *(third-party source)* = third-party account; *(unverified)* and *(my calculation)* = inferences. If you want to see what the stack layers are, go back to [`01-MAP-AND-LAYERS.md`](01-MAP-AND-LAYERS.md); about why decoding is limited by memory bandwidth, see [`02-HOW-INFERENCE-WORKS.md`](02-HOW-INFERENCE-WORKS.md); llama.cpp is described in [`04-LLAMA-CPP-AND-THE-GGML-FAMILY.md`](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md).

---

## 1. Why a server engine is a different beast than a desktop one

### 1.1 A different goal: an aggregate instead of a single stream

A desktop engine (llama.cpp, Ollama, LM Studio) optimizes **time to first token** and the **generation speed (tok/s) of a single stream**, and on top of that it must politely share the machine with other programs. A server engine optimizes something else: the **total number of tokens per second under a given latency limit**, spread across dozens or hundreds of concurrent requests.

This is not a cosmetic difference. It changes what the bottleneck is, and therefore the whole design of the program.

Reminder from chapter 02: decoding a single token requires reading all active weights from the card's memory, and the arithmetic work per token is small, so the card waits for memory. **But if in a single step you serve 64 sequences at once, you read the same weights once and get 64 tokens.** Using the example from the vLLM article (13B model, 26 GB of weights): at batch 1, one token "costs" reading 26 GB; at batch 64 — 64 tokens for the same read *(my calculation*, ignoring KV reads and overhead). Hence the whole server economy: **the more sequences you pack into one step, the cheaper the token**. At batch 1 there is nothing to amortize.

But to pack many sequences into one step, each of them must have its own KV cache in the card's memory. And here begins the problem that paging solves.
### 1.2 The KV cache problem: the arithmetic from the PagedAttention paper

Source: Kwon et al., *Efficient Memory Management for Large Language Model Serving with PagedAttention*, arXiv 2309.06180, SOSP 2023 (Koblenz, October 23–26, 2023). Authors in order: Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, Ion Stoica (UC Berkeley, Stanford, UC San Diego, independent researcher). I read pages 1–2 and 8–9 of the PDF myself; the numbers below are the numbers I saw there.

**Step 1 — what takes up GPU memory.** Fig. 1 of the paper: a 13B model on an A100 40 GB. Parameters take 26 GB, i.e. 65% of memory (26/40 = 0.65). The KV cache takes **over 30%**, i.e. over 12 GB. The rest (activations, etc.) is less than ~5% *(my calculation)* from the remainder to 100%.

**Step 2 — how many tokens that is.** Table 1: for OPT-13B on 1×A100-40GB the KV pool held **15.7 thousand tokens**. From 12 GB and 15.7 thousand tokens, the order of magnitude is **~0.8 MB of KV per token** *(my calculation*, from two numbers in the paper; this is an order of magnitude, not an exact value). For the larger models in the table: OPT-66B on 4×A100 → 9.7 thousand tokens; OPT-175B on 8×A100-80GB → 60.1 thousand tokens.

**Step 3 — how much of that pool goes to waste.** Fig. 2 of the paper measures what fraction of the reserved KV memory stores *actual token states*. In the three variants of the Orca system used in the paper (Orca-Max, Orca-Pow2, Orca-Oracle) it was **20.4% / 26.8% / 38.2%**, respectively, and in vLLM — **96.3%**. A sentence from the text: "only 20.4% – 38.2% of the KV cache memory is used to store the actual token states in the existing systems". The "near-zero waste" that the project claims in its description is precisely that 96.3%.

Let's apply these percentages to the 15.7-thousand-token pool *(illustration, my calculation* — the paper gives experiment averages, not a distribution over this specific pool):

| System | Share of KV memory with real tokens | Real tokens from the 15.7k pool |
|---|---|---|
| Orca (worst variant) | 20.4% | ≈ 3.2 thousand |
| Orca (best variant) | 38.2% | ≈ 6.0 thousand |
| vLLM | 96.3% | ≈ 15.1 thousand |

The ratio 96.3/38.2 ≈ 2.5, and 96.3/20.4 ≈ 4.7. This matches the order of magnitude of the headline result from the abstract: "vLLM improves the throughput of popular LLMs by 2-4x with the same level of latency compared to the state-of-the-art systems, such as FasterTransformer and Orca". A note on citing: **this is 2–4× relative to FasterTransformer and Orca, on 2023-era setups (ShareGPT/Alpaca traces)**. Never cite this as "vLLM is 4× faster than …" without that caveat.

**Where the waste comes from — picture it this way.** The old way is like a hotel where every guest pre-books an entire contiguous row of rooms "in case they stay a year", even though most stay two nights. The row sits empty and no one else can get it. Paging is a hotel where the guest gets rooms one at a time, **in arbitrary locations in the building**, and the front desk keeps a table: "your room 1 is physical room 7, room 2 is physical room 1".

Now strictly. When the engine does not know how many tokens a request will generate, and the KV must lie in one contiguous chunk, it must reserve space for the worst case. An illustration with **hypothetical numbers** (not from the paper): if you reserve 2048 tokens per request, the 15.7k pool fits about 7 parallel requests (15,700 / 2048 ≈ 7.7), even if all of them have only 300 tokens. When you allocate memory on demand, the same request takes ~300 tokens and the pool fits about 52 of them (15,700 / 300). **Seven sequences in a batch versus fifty** — and from point 1.1 you know that batch size is directly the cost per token.

**The paging mechanism** (paper §4, general description):

- The KV cache is divided into **fixed-size blocks**.
- A **block table** maps a request's logical blocks to physical blocks in GPU memory.
- Physical blocks can be in any order; at most a piece of the **last** block of each sequence is wasted.
- **Copy-on-write** allows blocks to be shared between sequences (parallel sampling, *beam search*).
- When blocks run out, the system **preempts** — it evicts blocks to the CPU or drops them and recomputes; FCFS queue; "all-or-nothing" eviction for a group of sequences.

An illustration with a **4-token** block (size chosen for readability; the default block size on ROCm could not be established — `block_size` is `None`/platform-dependent in `vllm/config/cache.py:74`):

```
Request A: 7 prompt tokens              Physical memory (blocks in any order)
 logical block 0: [t0 t1 t2 t3]  ──────►  physical block 7
 logical block 1: [t4 t5 t6 __]  ──────►  physical block 1   (1 free slot = the only waste)
 (the next token goes into the free slot of block 1; only the eighth gets a new block)

Request B: 5 tokens
 logical block 0: [u0 u1 u2 u3]  ──────►  physical block 3
 logical block 1: [u4 __ __ __]  ──────►  physical block 4
```

A curiosity of scale: the original implementation from the paper is "8.5K lines of Python and 2K lines of C++/CUDA code". In today's `vllm/` tree it has about 1.1 million lines of Python. Where that growth comes from — in a moment.
### 1.3 The rest of the trade-offs — table

| Issue | Desktop engine (llama.cpp) | Server engine (vLLM, SGLang) |
|---|---|---|
| Goal | time to first token and tok/s of a single stream | aggregate throughput under a latency limit |
| KV cache | contiguous chunk per slot; fragmentation shows up as "slot too small" | blocks + block table (vLLM), radix tree (SGLang) |
| GPU memory | shared with other programs; model swapping possible | **pre-allocation**: vLLM takes `gpu_memory_utilization = 0.92` by default (`vllm/config/cache.py:102`) and sizes the KV pool up front |
| Startup | no model compilation (time not measured by me) | `torch.compile` compilation + graph capture — startup cost for steady speed |
| CPU | one thread, no hiding it | Python scheduler on the critical path → async scheduling, process splitting, Rust front-end |
| Quantizations | GGUF zoo (k-quants, i-quants) | a few formats calibrated for a specific GPU (AWQ/GPTQ, FP8, FP4, compressed-tensors) |
| Multiple GPUs | secondary; tensor parallel *experimental* | first-class; assumes fast interconnects |
| Telemetry | "one file, works offline" | Prometheus/OTel metrics, health probes, usage reporting (enabled by default in vLLM and TRT-LLM) |
| Maintenance | small core, one format | 2-week releases, ~1.1M lines of Python in vLLM, 286 model files |

A few rows of this table need a comment.

**Pre-allocation vs. machine sharing.** vLLM starts, profiles memory, reserves ~92% of each GPU, and only then creates the KV pool from the remainder (`core.py::_initialize_kv_caches`). That is sound when the machine exists to serve one model; it is disastrous when llama-swap is supposed to load and release different models on the same GPUs. vLLM has `/sleep`, `/pause`, `/resume` endpoints (`EngineCore.sleep/wake_up`), which ease the problem, but they are not designed as a mechanism for frequent model swapping.

**Graphs and compilation.** In a moment you will see that vLLM captures graphs by default for many batch sizes; the docs themselves say this mode is "the most efficient, but requires the most memory and takes the longest to capture". For a single user, kernel launch overhead is a minor component, and you pay the startup and memory reservation cost on every model load (the "tens of seconds to minutes" time is *unverified* — not measured by me).

**Quantization as a maintenance cost.** A data center operator quantizes once, with calibration, for the GPU they bought. A local user downloads a file that fits. The "format × GPU architecture" matrix is a maintenance cost that servers avoid by supporting fewer formats. That is why GGUF left the vLLM core (see §3).

**What the code itself says: "small-batch" kernels on RDNA.** Even vLLM, a batch-oriented engine by design, has dedicated "skinny GEMM" kernels in the RDNA path for batch ≤ 5 (`MAX_SKINNY_BATCH_SIZE = 5` in `rdna_hybrid_w4a16.py`; FP8 `wvSplitKQ` when `A.shape[0] <= 4`, `scaled_mm/rocm.py`), because the general GEMM tuned for large batches is wasted on a few rows. Local runtimes live in this regime all the time.
### 1.4 When paging helps less

*(Unverified — reasoning, not measurement.)* A single user with one or two long conversations does not have much fragmentation to reclaim. What matters to them is **how many context tokens fit in VRAM after subtracting the weights**, and whether the prefix survives between turns. Higher levels (prefix reuse: vLLM's block chain, SGLang's radix tree) pay off when many queries share a system prompt; on a desktop, keeping a single slot "warm" plays a similar role.

---

## 2. vLLM from the inside

**One line:** the de facto standard open-source server engine: a scheduler in Python/PyTorch + a paged KV manager + CUDA/ROCm/Triton kernels behind an OpenAI-compatible (and Anthropic) HTTP server.

### 2.1 Identity and scale

| | |
|---|---|
| License | Apache-2.0 (GitHub API, `LICENSE` file) |
| Repository | github.com/vllm-project/vllm; created 2023-02-09; first release v0.1.0 2023-06-20 |
| Current version | **v0.32.0, 2026-10-18**; releases roughly every 2 weeks (v0.29.0 09-09, v0.30.0 09-22, v0.31.0 10-05) |
| Stars / forks | 94,152 / 23,600 (API, 2026-10-19) |
| Languages (bytes) | Python 69.0 MB, Rust 5.2 MB, CUDA 3.2 MB, C++ 2.4 MB |
| Lines in snapshot | `vllm/` Python 1,095,116; `csrc/` CUDA 76,562 + C++ 40,310 (plus ~46k CPU kernels); `rust/` 145,149 lines of Rust |
| Origin | UC Berkeley, Sky Computing Lab (README); "v" was originally meant to stand for "virtual" — an analogy to virtual memory *(third-party source: Wikipedia)* |
| Documentation | docs.vllm.ai; blog vllm.ai/blog |

The contributor count from the API (454) is understated because the API limits pagination; the README mentions over 2,000 developers *(project's own claim)*.

**Who this is for.** A platform team with data-center GPUs (or ROCm Instinct, TPU, Gaudi…) that maintains a shared endpoint for applications, agents, and RL rollouts. vLLM assumes **the machine is yours**: it reserves a KV pool, compiles and captures graphs at startup, and expects checkpoints in Hugging Face format. The project's own values (`docs/governance/process.md`): performance, ease of use, broad coverage, production readiness, extensibility.

### 2.2 Process model (engine V1) and the request path

Source: `docs/design/arch_overview.md` (section *V1 Process Architecture*) and code in `vllm/v1/`.

```
                       HTTP / gRPC (client: application, agent)
                                   │
        ┌──────────────────────────▼──────────────────────────┐
        │ API server  (1 process by default; --api-server-count) │
        │  vllm/entrypoints/openai/api_server.py                │
        │  tokenization, multimodal loading, SSE, detokenization│
        │  (async_llm.py, output_processor.py, detokenizer.py)  │
        └──────────────────────────┬──────────────────────────┘
                                   │  ZMQ + MessagePack
        ┌──────────────────────────▼──────────────────────────┐
        │ EngineCore  (1 process per DP rank; busy loop)         │
        │  vllm/v1/engine/core.py                               │
        │  ┌───────────────┐   ┌──────────────────────────────┐ │
        │  │  Scheduler    │◄─►│ KVCacheManager               │ │
        │  │ (v1/core/sched│   │  └─ BlockPool (blocks, hashes,│ │
        │  │  /scheduler.py)│  │     free queue, LRU)          │ │
        │  └───────┬───────┘   └──────────────────────────────┘ │
        │          │ SchedulerOutput                            │
        │  ┌───────▼───────┐                                    │
        │  │ Executor      │  uniproc / multiproc / Ray         │
        │  └───────┬───────┘                                    │
        └──────────┼────────────────────────────────────────────┘
                   │  RPC to workers
     ┌─────────────┼─────────────┬─────────────┬────────────┐
     ▼             ▼             ▼             ▼
 Worker GPU0   Worker GPU1   Worker GPU2   Worker GPU3     (one per GPU:
 ┌─────────┐                                                 TP × PP per DP rank)
 │ModelRunner│  persistent batch state, input preparation,
 │ (V1/V2)  │  CUDA/HIP graphs, sampling
 └────┬────┘
      ▼
 Attention backend + kernels: FlashAttention-fork / FlashInfer / Triton /
 rocm_attn / AITER … + csrc/ (Marlin, paged attention, MoE, skinny GEMM …)
```

An example from the documentation that matches the reference machine's exact shape: `vllm serve -tp=4` is **1 API server + 1 EngineCore + 4 GPU workers = 6 processes** (plus a DP coordinator process if DP > 1). Separating the API server from the core has one purpose: tokenization, detokenization, and HTTP must not compete for the GIL with the scheduler (V1 announcement). You pay for this with IPC and a larger number of processes, for which you need CPU cores.

Files to remember: `vllm/v1/engine/core.py` (2806 lines: `EngineCore`, `EngineCoreProc`, `DPEngineCoreProc`), `core_client.py` (2162), `async_llm.py` (1445), `output_processor.py` (1047); executors in `vllm/v1/executor/` (`uniproc_executor.py`, `multiproc_executor.py` 1134 lines, `ray_executor_v2.py`).

**One engine step** (`EngineCoreProc.run_busy_loop`, `core.py:1589`; `EngineCore.step()`, `core.py:640`):

```
while not shutdown:
    _process_input_queue()          # new requests from ZMQ
    step():
        scheduler.schedule()                      # who gets how many tokens in this step
        model_executor.execute_model(..., non_block=True)   # GPU starts forward pass
        (CPU meanwhile computes grammar mask for structured output)
        sample_tokens(grammar_output)             # sampling
        scheduler.update_from_output(...)         # write results, frees, completions
```
Construction tip: the grammar mask is computed on the CPU **during** the GPU forward pass — a standard trick to hide the cost of grammar enforcement.

V1 was announced on 2025-01-27 (blog post "vLLM V1 alpha"): unified scheduler, persistent batch, isolated EngineCore loop in a separate process, prefix caching enabled by default ("<1% throughput drop at 0% cache hits"), "up to 1.7× higher throughput than V0" *(project's own claim)*.

### 2.3 Scheduler: continuous batching as a token budget allocation

`vllm/v1/core/sched/scheduler.py` (3527 lines), plus `async_scheduler.py` and `request_queue.py` (FCFS and priority queues).

The most important thing in the whole file is the comment at `scheduler.py:623–632`:

> "There's no 'decoding phase' nor 'prefill phase' in the scheduler. Each request just has the num_computed_tokens and num_tokens_with_spec … At each step, the scheduler tries to assign tokens to the requests so that each request's num_computed_tokens can catch up its num_tokens_with_spec. This is general enough to cover chunked prefills, prefix caching, speculative decoding, and the 'jump decoding' optimization."

In Polish: **the scheduler does not know "prefill" and "decoding" phases**. Each request has a `num_computed_tokens` counter (how many tokens it has already computed) and a `num_tokens_with_spec` target. At each step, the scheduler allocates the **token budget** `max_num_batched_tokens` so that the counters "catch up" to the targets, and then admits waiting requests. This single mechanism covers:

- **continuous batching**: requests enter and leave the batch at every step, rather than waiting for the whole batch to finish;
- **chunked prefill**: a long prompt is cut into chunks and computed over several steps together with decoding of others;
- **prefix caching**: tokens hit in the cache are simply "already computed" (`num_computed_tokens` starts higher);
- **speculative decoding**: a request has more tokens to verify in a single step.

Default values in `vllm/config/scheduler.py`:

| Parameter | Default | Meaning |
|---|---|---|
| `max_num_batched_tokens` | 2048 (256 for batched-DP) | token budget per step |
| `max_num_seqs` | 128 (`DEFAULT_MAX_NUM_SEQS=128`, line 43) | max. requests in flight |
| `enable_chunked_prefill` | `True` | chunking long prompts |
| `long_prefill_token_threshold` | configurable (adaptive variant exists) | prevents a long prompt from starving others |
| "prefill cadence" | configurable | delays prefill so decoding gets longer uninterrupted runs |
| `stream_interval` | configurable | how many tokens to buffer before sending SSE |

⚠️ **Discrepancy in sources:** the Model Runner V2 design doc mentions "`max_num_reqs` (1024 by default on most platforms)", while the config class has 128. I verified both values in the files; I could not establish which one wins on a given platform (there are context-dependent overrides).

**Chunked prefill example with a budget of 2048** *(illustration, my calculation)*: 10 decoding sequences are in flight, a 6000-token prompt arrives. Step 1: 10 decoding tokens + 2038 prompt tokens (2048 − 10). Step 2: again 10 + 2038. Step 3: 10 + 1924 (the remainder). Across these 3 steps, the ten sequences **never stopped generating** — had the prompt gone as a single chunk, each of them would have waited for the entire prefill. The price is a longer time-to-first-token for the long prompt itself.

**Preemption.** When KV blocks run out, the scheduler preempts requests from the run and recomputes them later. V1 chose **recomputation instead of swap** (the 2023 article had both variants; in `schedule()` there is `preempted_reqs`, and the MRV2 doc says "Treat preemption as completion. On resume, re-add request data as fresh state").

**Async scheduling** (`AsyncScheduler`, `async_scheduler.py:14–80`): the scheduler plans step N+1 while the GPU executes step N. Since the sampled tokens of step N are not yet known, the scheduler records `num_output_placeholders` and placeholder tokens `-1`, and corrects them when the result arrives. Requests with structured output are marked `pending_structured_output_tokens`, because the grammar needs the real token. `SchedulerConfig.async_scheduling` defaults to `None` (automatic mode). This is the counterpart of "zero-overhead scheduler" in SGLang (§4).
### 2.4 KV Manager and Prefix Caching

Files in `vllm/v1/core/`: `kv_cache_manager.py` (922), `block_pool.py` (905), `kv_cache_utils.py` (1217), `kv_cache_coordinator.py` (1038), `single_type_kv_cache_manager.py` (2719), `kv_cache_planning.py` (1704).

**`BlockPool`** owns all GPU blocks as `KVCacheBlock` objects (reference counter, optional hash). Free blocks live in the `FreeKVCacheBlockQueue` — an **intrusive doubly linked list**, written so that removing an element from the middle is O(1) (touching a cached block removes it from the free list) without allocating Python objects. Eviction order is LRU, with ties broken so that the **tail of the block chain is evicted first** (`kv_cache_utils.py:258–285`).

`BlockPool.free_blocks` (`block_pool.py:776`): blocks with `ref_cnt==0` **without a hash** go to the **front** of the queue (LIFO reuse "for better GPU locality"); blocks with a hash (eligible for prefix caching) go to the **end** (FIFO = LRU eviction).

**How prefix hashing works.** The cache is a hash table `BlockHashToBlockMap`: `{(block_hash, group_id) → block}`. Rules:

1. **Only full blocks** are cached.
2. A block's hash depends on the hash of the **previous** block (chaining): `hash_block_tokens(hash_fn, parent_block_hash, curr_block_token_ids, extra_keys)` = `hash((parent_hash, tuple(token_ids), extra_keys))`; the first block gets the initial value `NONE_HASH` (`kv_cache_utils.py:707–737`).
3. `extra_keys` carry the LoRA identifier, hashes of multimodal inputs, the prompt embedding hash and — important in multi-tenancy — a per-request **`cache_salt`**.

```
tokens:  [ A A A A | B B B B | C C C C | D D ]      (block = 4 tokens, illustration)
          └─block 0─┘ └─block 1─┘ └─block 2─┘ └ incomplete: not cached
h0 = H( NONE_HASH, (A A A A), extra )
h1 = H( h0,        (B B B B), extra )
h2 = H( h1,        (C C C C), extra )
```

**Why a chain, not just the hash of the block's tokens?** Because the KV state of a token depends on *all* tokens before it. The same block `(B B B B)` after a different prefix is different KV, so it must have a different hash. The chain provides this for free: a new request computes hashes block by block from the start and looks up each in the table; the first miss ends the match.

Hash function: as of v0.11 the default is **sha256** (via pickle; the result may differ between Python/vLLM versions), `sha256_cbor` for reproducible hashes across processes and languages, `xxhash`/`xxhash_cbor` faster but non-cryptographic, with a documented caveat about collisions and privacy in multi-tenant environments (option `--prefix-caching-hash-algo`; `docs/design/prefix_caching.md`).

A design note from the code (`block_pool.py:44–49`): "we don't de-duplicate the blocks in the cache … block tables are append-only".

Consequences: O(1) lookup, trivial distribution (KV events, offload, P2P), but matching **only at whole-block granularity**. Short shared prefixes (less than one block) are not shared. Compare with the SGLang tree in §4.

**Hybrid models.** `kv_cache_coordinator.py` and `single_type_kv_cache_manager.py` manage several "KV groups" with different layer types (full attention, sliding window, Mamba/linear attention state) — `docs/design/hybrid_kv_cache_manager.md`. I reviewed the file names, not the internals.

**KV events** (`vllm/distributed/kv_events.py`: `BlockStored`/`BlockRemoved`/`AllBlocksCleared`) are published so external routers (llm-d, Dynamo) can see the cache contents. **KV offload** — `vllm/v1/kv_offload/` (15,195 lines; CPU/layers/file), `vllm/v1/simple_kv_offload/` (2,940) and offload via connectors.
### 2.5 Worker and Model Runner: V1 and V2

The `vllm/v1/worker/` directory has 45,135 lines.

**Model Runner V1:** `gpu_model_runner.py` — 7,221 lines, the largest file in `v1`. Persistent batch: request state is kept in persistent tensors (`gpu_input_batch.py`) and updated differentially at each step, so that block tables are not rebuilt in Python.

**Model Runner V2 (MRV2):** `vllm/v1/worker/gpu/` (`model_runner.py` 2,473 lines, `input_batch.py`, `cudagraph_utils.py` 1,098, `spec_decode/`, `sample/`, `pcp_manager.py`). The design document (`docs/design/model_runner_v2.md`) says, in the authors' words, that in V1 "we discovered several fundamental design mistakes and accumulated significant technical debt", so the runner was rewritten from scratch: persistent state is separated from per-step input tensors (assembled on GPU via Triton/UVA), the approach is "async-first" — "the core model execution loop is a CUDA stream with no CPU synchronization points", and Gumbel-max sampling is done GPU-side.

Status in this snapshot: `VllmConfig.use_v2_model_runner` (`vllm/config/vllm.py:707–740`) returns **`True` by default**, unless you set `VLLM_USE_V2_MODEL_RUNNER=0`, Triton is missing, or you request an unsupported feature (then a warning and fallback to V1). ⚠️ The documentation lags behind the code: `worker/gpu/README.md` still says "[Experimental]", and the design document says "not yet feature-complete". Whether the same default applies on ROCm — **I could not establish**.

`gpu_worker.py` (1,708 lines): profiles memory, sizes the KV pool, loads weights, captures graphs. KV planning: `core.py::_initialize_kv_caches` (`core.py:244`) and `kv_cache_planning.py`.

### 2.6 `torch.compile` and CUDA/HIP graphs

`vllm/compilation/` (15,974 lines), `docs/design/torch_compile.md`, `cuda_graphs.md`, `vllm/v1/cudagraph_dispatcher.py`.

- vLLM compiles the model with `torch.compile` **piecewise**: the graph is cut around attention (which cannot be captured into a CUDA graph on all backends), the pieces are compiled by Inductor, and graphs are captured for rounded batch sizes.
- A custom-op layer (`docs/design/custom_op.md`) lets you swap kernels (RMSNorm, fused ops, quantization) and run fusion passes (`vllm/compilation/passes/fusion/`, including `rocm_aiter_fusion.py`).
- `CUDAGraphMode` modes: `NONE`, `PIECEWISE`, `FULL`, `FULL_DECODE_ONLY`, **`FULL_AND_PIECEWISE` (default)** — a full graph for uniform decode batches, piecewise for prefill and mixed batches. Documentation: "generally the most performant … but also requires the most memory and takes the longest to capture". `CudagraphDispatcher` picks a graph from `BatchDescriptor`.
- On ROCm, HIP graphs do the same through the same code; "CUDA graphs" is the API name (`cuda_alike`).

Effect for a single machine: startup means compilation and capture, and graphs reserve memory. Payoff: lower CPU overhead per step at medium and large batch sizes.

### 2.7 Attention backends and kernels

`vllm/v1/attention/` (68,079 lines including ops). In `backends/`: `flash_attn.py` (a custom FlashAttention fork `vllm_flash_attn` for CUDA), `flashinfer.py`, `triton_attn.py`, `flex_attention.py`, MLA (`mla/`), Mamba/GDN/linear variants, `cpu_attn.py`; for ROCm: `rocm_attn.py`, `rocm_aiter_fa.py`, `rocm_aiter_unified_attn.py`, `rocm_segmented_attn.py`, `triton_flash_attn.py`; further `hpc_attn.py`, `turboquant_attn.py`, `ultraquant_attn.py`. Selection follows a priority list per platform (`vllm/v1/attention/selector.py`, `platforms/*.py::_get_backend_priorities`). FlashInfer is a pinned dependency (`requirements/cuda.txt: flashinfer-python==0.7.2`).

Kernels (`csrc/`, ~118 thousand lines excluding CPU): `attention/` (4,315: paged attention v1/v2, MLA), `quantization/` (27,232: Marlin, AWQ, GPTQ/Exllama, CUTLASS scaled-mm, FP8/FP4, machete), `moe/` (9,704), `rocm/` (13,701), `mamba/`, `kimi_k3/`, a custom all-reduce (`custom_all_reduce.cu*`), cache kernels (`cache_kernels.cu`), sampling kernels. Recurring kernels named "fused_*_qknorm_rope_kv_insert" per model family show how much per-model work the project takes on — which explains how 2K lines of C++/CUDA grew to ~118 thousand.
### 2.8 Features: speculative decoding, structured output, tools, LoRA, multimodal

- **Speculative decoding** (`vllm/v1/spec_decode/`, 6,373 lines): n-gram (CPU and GPU), EAGLE, draft model, MTP, suffix decoding, "dflash", "fly", hidden-state extraction, model-specific heads; rejection sampler `vllm/v1/sample/rejection_sampler.py` (1,197 lines). The general principle of "check several tokens at once for the price of one" is described in the acceleration directory: [`../speeding-up-generation/README.md`](../speeding-up-generation/README.md).
- **Structured output** (`vllm/v1/structured_output/`): xgrammar, guidance, outlines, lm-format-enforcer backends; by default `backend="auto"` selects based on the query content (`vllm/config/structured_outputs.py:20`).
- **Tool calling:** `vllm/tool_parsers/` has about 60 files (≈55 parsers: hermes, llama, mistral, pythonic, qwen3, deepseek v3/v3.1/v3.2/v4, kimi k2/k3, glm, gpt-oss/harmony, granite, …). **Reasoning parsers:** `vllm/reasoning/` ~42 files (deepseek r1/v3, qwen3, gpt-oss, kimi, glm, …). These are file counts, not parser counts. The point: each new family of open models requires its own parser, and vLLM delivers them quickly ("Day-0" is *unverified* in the sense of "within days").
- **LoRA:** multiple adapters at once (`vllm/lora/`, 14,653 lines; `/v1/load_lora_adapter`). **Multimodal:** `vllm/multimodal/` (13,441 lines; images/video/audio; encoder cache `v1/core/encoder_cache_manager.py`). **Embeddings/rerank/pooling.** **Sleep mode** (`EngineCore.sleep/wake_up`).
- **Prefill/decode disaggregation** — "experimental": NixlConnector, MooncakeConnector, MoRIIOConnector (ROCm only), LMCacheConnectorV1/LMCacheMPConnector, OffloadingConnector (offloads KV to CPU), MultiConnector, ExampleConnector connectors (`docs/features/disagg_prefill.md`). The doc is honest: "Disaggregated prefill DOES NOT improve throughput" — it serves to tune TTFT and inter-token latency separately and to control the ITL tail.

### 2.9 Parallelism

Tensor parallel, pipeline parallel, data parallel, expert parallel, context parallel (DCP/PCP), flexible EP, "dual-batch overlap" (`design/dbo.md`); `vllm/distributed` has 85,642 lines. In the course glossary: *tensor split (tensor parallel)* cuts each layer across cards (cards must frequently exchange results — hence the importance of the interconnect), while *pipeline* assigns consecutive layer groups to cards. Where this hurts on the reference hardware, you will see in §3.

### 2.10 "Platform" design and hardware plugins

vLLM is not merely a "CUDA engine". In `vllm/platforms/` the platforms live in a tree: `cuda.py`, `rocm.py` (1,408 lines), `xpu.py`, `cpu.py`, `zen_cpu.py`, `tpu.py`. Other hardware joins **out-of-tree** through Python entry points (`vllm.platform_plugins`, `docs/design/plugin_system.md`):

| Plugin | Hardware | Stars (API) |
|---|---|---|
| vllm-ascend | Huawei Ascend | 3,000 |
| vllm-gaudi | Intel Gaudi | 63 |
| tpu-inference | Google TPU (JAX + PyTorch) | 464 |
| vllm-metal | Apple Silicon (link in the installation docs) | — |

A PyTorch Foundation blog post (2025-05-06) also lists AWS Neuron and IBM Spyre as plugin or official targets. The design idea: **PyTorch + custom ops as the portability layer** — the hardware vendor supplies the plugin and op implementations, while the core (scheduler, KV) stays shared. The cost: Python overhead, mitigated by compilation and graphs.

The front-end itself is also changing: **Rust front-end** (`rust/`, "vllm-frontend-rs", HTTP+gRPC server on axum, talks to the Python core over ZMQ+MessagePack; enabled with `VLLM_USE_RUST_FRONTEND=1`; README: "experimental, not feature-complete"). It first appeared in `github.com/Inferact/vllm-frontend-rs` (archived), then was moved into the main repo.
### 2.11 API and models

The server (`vllm/entrypoints/openai/api_server.py`, the `vllm serve` command) exposes, among others, `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/responses`, `/v1/audio/transcriptions`, `/v1/realtime`, `/v1/score`, `/v1/rerank`, `/tokenize`, `/detokenize`, `/v1/load_lora_adapter`, `/sleep`, `/pause`, `/resume`, `/metrics`, `/health`, `/v1/models`. **Anthropic-compatible API**: `/v1/messages` and `/v1/messages/count_tokens` (`vllm/entrypoints/anthropic/`). There is also a `cohere` router, a gRPC server (`grpc_server.py`), the `LLM` class for offline work, and `vllm bench`. **There is no Ollama-compatible API** (SGLang has one).

Models: the README lists 200+ architectures *(project's own claim)*; the `vllm/model_executor/models/` tree contains 286 files, and the registry itself has 1607 lines.

### 2.12 Strengths and weaknesses, offline, who is behind it

**Strengths:** the broadest model coverage and the largest ecosystem (llm-compressor, production-stack, aibrix, semantic-router, guidellm, vllm-omni — all `vllm-project/*`, Apache-2.0); real hardware breadth through plugins; OpenAI + Anthropic + gRPC APIs; good tensor split on identical cards. "Fastest day-zero support" — *(unverified)*.

**Weaknesses for you:** (a) no GGUF in the core (§3); (b) first-class ROCm applies to Instinct (MI300/MI350), RDNA4 is a secondary target; (c) 0.92 of card memory — does not coexist with llama.cpp processes managed by llama-swap on the same cards; (d) one model per server process, no built-in model swapping (I could not find one in the tree; sleep mode helps partially — *(unverified)*).

**Offline.** Works offline after locally loading the weights (point to a local path; `HF_HUB_OFFLINE=1` is standard Hugging Face behavior — *(unverified)* here). **Telemetry is enabled by default**: the usage statistics reporter sends to `https://stats.vllm.ai`; the `is_usage_stats_enabled()` docstring reads: "By default, it should be enabled". You disable it with the `VLLM_DO_NOT_TRACK=1`, `DO_NOT_TRACK=1`, `VLLM_NO_USAGE_STATS=1` variables or the `$HOME/.config/vllm/do_not_track` file (`vllm/usage/usage_lib.py:50–68`, `vllm/envs.py:36–38, 828–835`). The collector also looks at cloud provider files in `/sys/class/dmi` (`_detect_cloud_provider`). What exactly is sent — I did not read it all.

**Who is behind it.** The project came out of UC Berkeley (Sky Computing Lab); since 2025-05-06 it is hosted by the PyTorch Foundation, and earlier (July 2024) it moved under the Linux Foundation umbrella *(third-party source)*. License Apache-2.0; the governance document states plainly: "No one buys their way into governance. Committer status belongs to individuals, not companies." The core "Project Leads" (the equivalent of a Technical Steering Committee) include Woosuk Kwon, Zhuohan Li, Simon Mo, Kaichao You, Robert Shaw, Tyler Michael Smith, Michael Goin, Nick Hill; lead maintainers are Woosuk Kwon and Zhuohan Li. Many of them now work at the startup **Inferact** (GitHub organization created 2025-10-20; in January 2026 the company announced raising 150 mln USD — *(company's own claim)*, repeated by Wikipedia citing TechCrunch *(press report)*; investors and valuation I could not establish) or at Red Hat. Full money and people: [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

> **Check it yourself (1) — scheduler without phases and the prefix hash chain.** In a vLLM clone (commit `b7701fc`):
> ```bash
> sed -n '620,635p' vllm/v1/core/sched/scheduler.py
> grep -n "max_num_batched_tokens\|DEFAULT_MAX_NUM_SEQS" vllm/config/scheduler.py | head
> sed -n '700,740p' vllm/v1/core/kv_cache_utils.py     # hash_block_tokens, NONE_HASH
> sed -n '770,800p' vllm/v1/core/block_pool.py          # free_blocks: blocks without hash first, with hash last
> ```
> You should see the sentence "There's no 'decoding phase' nor 'prefill phase' in the scheduler", the defaults 2048 / 128, and the pattern `hash((parent_hash, tuple(token_ids), extra_keys))`. *(Not run by me; paths and line ranges come from my notes.)*

---
## 3. vLLM on the R9700 (gfx1201)

Everything below comes from the code and documentation of snapshot `b7701fc`. **Nothing was run by me on this machine** — the cards are in production.

### 3.1 What I verified in the code and documents

1. **Official declaration.** `docs/getting_started/installation/gpu.rocm.inc.md` lists: MI200 (gfx90a), MI300 (gfx942), MI350 (gfx950), Radeon RX 7900 (gfx1100/1101), **Radeon RX 9000 (gfx1200/1201)**, Ryzen AI MAX / AI 300 (gfx1151/1150); ROCm 6.3 or newer. The name "R9700" does not appear in the documentation.
2. **The card is recognized by name.** `vllm/platforms/rocm.py:92` maps the PCI identifier **`0x7551` to `"AMD_Radeon_R9700"  # gfx1201`**, and `0x7550` to RX 9070 XT (gfx1201).
3. **Default architecture list.** `CMakeLists.txt:52` — `HIP_SUPPORTED_ARCHS` contains `gfx1200;gfx1201`; the base ROCm Docker image builds `gfx90a;gfx942;gfx950;gfx1100;gfx1101;gfx1200;gfx1201;gfx1150;gfx1151` (comment: "gfx1200 (9070XT), gfx1201 (9070)").
4. **Architecture predicates.** `rocm.py` defines `_ON_RDNA4 = gfx1200 or gfx1201`, `_ON_GFX12X`, `_ON_GFX1X` (all of RDNA3/4).
5. **Installation.** Prebuilt wheels require **Python 3.12**; on other versions pip "will silently fall back to the CUDA wheel from PyPI, which will fail" (warning from the documentation). Variants: `rocm100` (ROCm 10.0 via pip through TheRock, "includes the GPU kernels for every supported architecture"; default nightly), `rocm721`, `rocm72`, `rocm700` (0.14.0–0.18.0). Command: `uv pip install vllm --extra-index-url https://wheels.vllm.ai/rocm/ --upgrade` *(not run by me)*.

⚠️ **gfx1250 is not RDNA4.** Both vLLM and SGLang have `gfx1250` in their build lists; vLLM code treats it as a CDNA class (MI4xx type), and a comment in the SGLang Dockerfile calls it "mi45x". The docstring of the SGLang helper that calls gfx1250 "RDNA4" is wrong or imprecise. The R9700 is **gfx1201**.

### 3.2 Attention backends that will work

Priority list for models without MLA (`_get_backend_priorities`, `rocm.py` around 505–530): `ROCM_ATTN` (unless there is a KV connector), `ROCM_AITER_FA` (if AITER MHA is enabled), `ROCM_AITER_UNIFIED_ATTN` (if AITER is found; inserted **at the beginning** when `is_rdna_aiter_enabled()` = RDNA4 + `aiter` installed + enabled by the user), then `TRITON_ATTN`, `TURBOQUANT`, `ULTRAQUANT`. `VLLM_ROCM_USE_AITER` defaults to **False** (`envs.py:136, 1250`).

The custom HIP paged attention kernel (`csrc/rocm/attention.cu`) is allowed on gfx1x only for: fp16/bf16 q, **head_size == 128, block_size == 16, GQA ratio 3..16, max_seq_len ≤ 128K, no sliding window, no ALiBi, no "sinks", `kv_cache_dtype` "auto"** (`rocm.py` around 896–908). Everything else falls back to Triton. On the R9700, expect `ROCM_ATTN` (for "ordinary" shapes) or `TRITON_ATTN`.

AITER on gfx12 provides **only Triton kernels**: "Only aiter's Triton kernels exist on gfx12 (no CK build)" (`_aiter_ops.py:2276–2290`). For vision encoders, the platform prefers "Flash Attention (Triton backend)" only with `FLASH_ATTENTION_TRITON_AMD_ENABLE=TRUE` and the module present; otherwise Torch SDPA.
### 3.3 Quantization on RDNA4: Code vs. Documentation

**Code.** `ROCmPlatform.supported_quantization` (`rocm.py:625–649`) contains: awq, auto_awq, awq_marlin (→awq), gptq, auto_gptq, fp8, compressed-tensors, fbgemm_fp8, inc, quark, mxfp4, mxfp8, torchao, modelopt*, fp8 per-tensor/block/channel variants, online, gpt_oss_mxfp4, deepseek_v4_fp8. **No `gguf`, no `bitsandbytes`, no `gptq_marlin`.**

**INT4 kernels (W4A16).** Priority order in `vllm/model_executor/kernels/linear/__init__.py:541–547`:

1. `RDNA3W4A16LinearKernel` — requires **only gfx1100**;
2. **`RDNAHybridW4A16LinearKernel`** — any gfx11/gfx12: fused GEMM with dequantization in Triton for prefill + "skinny" GEMM in HIP `wvSplitK_int4_g` for decoding (rows M ≤ 5); groups 32/64/128; fp16/bf16 activations; K%16==0; weights stored once as int8 in ExLlama layout (`mixed_precision/rdna_hybrid_w4a16.py`, 651 lines);
3. `TritonW4A16LinearKernel`, 4. `ConchLinearKernel`, 5. `ExllamaLinearKernel`.

Conclusion from the code: **INT4 GPTQ/AWQ on gfx1201 is handled by the hybrid kernel**.

**FP8.** `supports_fp8()` is `on_cdna() or on_rdna()`; `ROCmFP8ScaledMMLinearKernel` has a comment "Restore RDNA4 (gfx12x) dropped by the get_cdna_version()>2 refactor" and reports "requires CDNA3+ (gfx942/gfx950) or RDNA4 (gfx12x)" (`scaled_mm/rocm.py:88–90`); the small-batch path uses `wvSplitKQ`, otherwise `torch._scaled_mm`. The fp8 type outside gfx94 is `float8_e4m3fn`. Whether FP8 performance on gfx1201 is good — **not measured**.

⚠️ **Documentation–code discrepancy (AWQ/GPTQ).** The table in `docs/features/quantization/README.md` shows for "AMD GPU": AWQ: no, GPTQ: no, FP8 (llm-compressor W8A8): yes, GGUF: yes. This contradicts the code described above (RDNA kernels, awq/gptq on the allowed list). I suspect the table is coarse and outdated, but **I cannot prove it**. Practical rule: *the documentation says "no", the code has kernels for RDNA — test before you base a plan on it.* Interestingly, the same table considers GGUF supported for AMD, while another document (below) says GGUF is outside the core — so the table is internally inconsistent with the rest of the documentation.

### 3.4 GGUF in vLLM

From `docs/features/quantization/gguf.md`:

- support "has migrated to OOT vllm-gguf-plugin" (repo `vllm-project/vllm-gguf-plugin`, 54 stars, last push 2026-09-24) — you need `pip install vllm-gguf-plugin`;
- banner: "GGUF support in vLLM is highly experimental and under-optimized … might be incompatible with other features. Currently, you can use GGUF as a way to reduce memory footprint";
- syntax: `vllm serve unsloth/Qwen3-0.6B-GGUF:Q4_K_M --tokenizer Qwen/Qwen3-0.6B`; the tokenizer should come from the base model ("conversion from GGUF is time-consuming and unstable"); the config must be convertible by HF (`--hf-config-path`); TP works (example `--tensor-parallel-size 2`);
- the `gguf.py`/`gguf_loader.py` files are no longer in the snapshot core.

What I **do not** know: which quant types the plugin supports and whether any ROCm kernels run them. Treat this as "load the weights to save VRAM, don't expect llama.cpp-class speed". For you this is key: your collection of quants (UD-IQ3_XXS etc.) is not fuel for vLLM.
### 3.5 Multiple GPUs

The custom all-reduce is only enabled on `gfx94`/`gfx95` (`rocm.py:1216–1218`). On four R9700s over PCIe, all-reduce in tensor parallel therefore goes through **RCCL** (`CudaCommunicator`). These GPUs have no NVLink-class interconnect, so TP scaling will be limited by bandwidth *(unverified — inference from the hardware, not a measurement)*. This matches what chapter 04 says about `-sm tensor` in llama.cpp.

### 3.6 An honest summary for gfx1201

**On paper supported** (in the documentation, in the default architectures, recognized by name, dedicated RDNA kernels exist). In practice, RDNA4 is the **consumer tail of a stack designed for MI300/MI350**: the fast AITER paths based on CK do not exist on gfx12 (Triton only), the custom all-reduce is only for MI300, and the quantization table is oriented toward Instinct. I could not establish CI job names for gfx1201 beyond the Buildkite configuration for ROCm (I did not inspect its internals). Expect it to work for BF16/FP16 models as well as FP8 and INT4-GPTQ in HF-format weights — **and that you will have to tune and debug**. I found no independent benchmark on RDNA4.

### 3.7 Untested — what I would try first

⚠️ **The list below is pure hypothesis. None of it has been run.** I assume you have released the GPUs from llama-swap for the duration of the test.

1. **Python 3.12** in a fresh venv (otherwise a silent fallback to the CUDA wheel from PyPI, which will not work), then the install command from §3.1. Make sure the ROCm build was installed.
2. **Start with a single GPU and a small HF model in BF16.** Only then `-tp=4` (`vllm serve <model> --tensor-parallel-size 4`). Do not start with a model that barely fits in 4×32 GB.
3. **Lower `gpu_memory_utilization`** (default 0.92; CLI flag name: check in `vllm serve --help`) and disable other processes on the GPUs — vLLM will reserve the rest.
4. **Read the startup log:** which attention backend was selected (`ROCM_ATTN` or `TRITON_ATTN`), which W4A16 kernel was used, whether MRV2 is enabled on ROCm (I do not know), which graph modes were captured and how long that took.
5. **Checkpoint GPTQ/AWQ INT4** to verify that `RDNAHybridW4A16LinearKernel` is selected — this will settle the “documentation vs. code” dispute. Then checkpoint **FP8** (`compressed-tensors`).
6. **Set `VLLM_NO_USAGE_STATS=1` (or `DO_NOT_TRACK=1`)** at the start.
7. **Do not enable AITER at the start** (`VLLM_ROCM_USE_AITER` defaults to False; on gfx12 there are only Triton kernels anyway). Only after you have a stable baseline result, check whether it changes anything.
8. **A fair measurement:** `vllm bench` (it is in `entrypoints/cli/benchmark`) with the **same** number of concurrent requests you expect in agent applications; compare with llama.cpp on the same model only if the quantizations are comparable. Remember that a batch-1 result is *not* what vLLM was designed for.
9. **At the end, if at all:** `vllm-gguf-plugin` with the example syntax from §3.4 on a small model — purely out of curiosity, with no hope of speed.

> **Check it yourself (2) — is your GPU known and what does it have in quantization.**
> ```bash
> grep -n "0x7551\|0x7550" vllm/platforms/rocm.py
> sed -n '541,547p' vllm/model_executor/kernels/linear/__init__.py
> grep -n "AWQ\|GPTQ\|GGUF" docs/features/quantization/README.md | head
> ```
> Compare the last two outputs: this is the documentation–code discrepancy from §3.3. *(Not run by me; paths from my notes.)*

---
## 4. SGLang from the Inside

**One-liner:** a high-throughput LLM/VLM engine (Python + PyTorch + Triton/CUDA/HIP kernels, Rust gateway), built around prefix reuse (RadixAttention) and a front-end language for "LLM programs"; today an engine in the vLLM class with the strongest focus on agents, RL, and DeepSeek-style MoE models.

> ⚠️ **R9700 (gfx1201) is not a supported target for SGLang.** The kernel build script for ROCm only accepts `gfx942`, `gfx950`, and `gfx1250` (`python/sglang/kernels/aot/setup_rocm.py:66–79`: "Unsupported GPU architecture … Expected gfx942, gfx950, or gfx1250"). There is no Dockerfile for gfx1200/1201 in the repo. Details in §4.5.

### 4.1 Identity

| | |
|---|---|
| License | Apache-2.0 |
| Repository | github.com/sgl-project/sglang; created 2024-01-08 (article from 2023-12); `sgl-project` organization since 2023-10-13 |
| Current version | **v0.5.22, 2026-10-19**; v0.5.21 2026-10-02; v0.5.20 2026-09-18 (~2-week cadence) |
| Stars / forks | 37,445 / 9,697 (API, 2026-10-19) |
| Languages (bytes) | Python 95.8 MB, Rust 11.0 MB, CUDA 4.8 MB, C++ 1.9 MB, Go 0.1 MB, HIP 65 KB, Metal 11 KB |
| Lines in snapshot | `srt/` (runtime) 905,669; `srt/layers` 206,385; `srt/models` 191,806; `srt/mem_cache` 91,816; `srt/managers` 44,415; `srt/disaggregation` 35,154; `srt/speculative` 31,492; kernels `python/sglang/kernels/` 450,109; gateway `sgl-model-gateway/` 112,513 |
| Documentation | docs.sglang.io, cookbook.sglang.io |

**Article:** "SGLang: Efficient Execution of Structured Language Model Programs", arXiv 2312.07104 (2023-12-12, rev. 2024-06-06). Authors: Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao, Christos Kozyrakis, Ion Stoica, Joseph E. Gonzalez, Clark Barrett, Ying Sheng. Abstract: "RadixAttention for KV cache reuse and compressed finite state machines for faster structured output decoding"; "up to 6.4x higher throughput compared to state-of-the-art inference systems" — that is the **authors' own benchmark, with 2023 baselines** *(project's own claim)*. According to Wikipedia *(third-party source)* the project was presented publicly in January 2024 (researchers from Stanford, UC Berkeley, Texas A&M, and SJTU), and the article appeared at NeurIPS 2024.

**Who it is for.** For LLM programs, not individual prompts: agent loops with many calls, branching, structured output, multi-turn conversations, and RL rollouts where requests share long common prefixes. The README today describes the project as "optimized for agentic workloads, large-scale serving, and RL rollouts" and adds an image/video generation engine ("SGLang Diffusion"). This is not a desktop application.

**Two halves:** the "Fast Backend Runtime" (`srt` — SGLang Runtime) and the "Flexible Frontend Language" (`python/sglang/lang`: `api.py`, `interpreter.py`, `ir.py`, `tracer.py`…; a DSL embedded in Python with gen/select/fork/join operations). In practice, most users today call the OpenAI API runtime and ignore the DSL — *unverified*, I have no adoption data.

### 4.2 Process and scheduler

**Three stages** (docstring `srt/entrypoints/engine.py:247–253`):

```
 HTTP / Engine  ┌──────────────────┐  ZMQ  ┌─────────────────────┐  ZMQ  ┌───────────────────────┐
 ─────────────► │ TokenizerManager │ ────► │ Scheduler           │ ────► │ DetokenizerManager    │
                │ (main process)   │       │ (subprocess)        │       │ (subprocess)           │
                │ tokenization     │       │ plans and runs      │       │ detokenization, text  │
                └──────────────────┘       │ GPU (TpModelWorker/ │       │ returns to client     │
                                           │ ModelRunner)        │       └───────────────────────┘
                                           └─────────────────────┘
```

Difference from vLLM: the scheduler and the GPU worker live **in the same process** per card (no separate IPC hop EngineCore→worker): `managers/scheduler.py` calls `run_batch` → `tp_worker`. I could not trace the process counts under DP (a `data_parallel_controller.py` exists).

**Main loop** (`srt/managers/scheduler.py`, 6278 lines — the file is a node of mixins from `scheduler_components/`, `scheduler_pp_mixin.py`, `schedule_batch.py` 4059 lines with `Req` and `ScheduleBatch`, `schedule_policy.py` 1713 lines, and `tp_worker.py`):

- `event_loop_normal` (`scheduler.py:1976`): `ingest_requests()` → `get_next_batch_to_run()` → `run_batch()` → `process_batch_result()` → repeat.
- `event_loop_overlap` (`scheduler.py:2011`): same, but keeps a `result_queue` with the result of the **previous** batch and processes it only after the next one has started. CPU work for batch N−1 (detokenization bookkeeping, insertion into the radix cache, checking completions, building batch N+1) overlaps with the GPU computing batch N. `is_disable_overlap_for_batch` falls back to synchronous mode where needed (e.g., dependent prefill after prefill).

```
 without overlap:  CPU: [prepare N]            [process N]  [prepare N+1]  ...
                   GPU:             [compute N]                                  [compute N+1]
                                   (GPU waits for CPU on both sides)

 with overlap:     CPU: [prepare N][prepare N+1 + process N-1 ][prepare N+2 + process N]
                   GPU:             [compute N        ][compute N+1        ][compute N+2 ]
```
This is a **“zero-overhead batch scheduler”** from release v0.4: “The scheduler runs one batch ahead and prepares all the metadata required for the next batch”; it claims a “1.1x speedup against its previous version and 1.3x against other state-of-the-art baselines”, largest for small models with large TP *(project's own claim, lmsys.org blog 2024-12-04)*.

**`get_next_batch_to_run`** (line 3829): handles interruption of a pending chunked prefill, HiCache events, merges the last prefill batch with the running decoding batch, selects a new prefill batch via `SchedulePolicy` + `PrefillAdder` (token budget, `chunked_prefill_size`, radix cache awareness), and otherwise a decoding step.

**Policies** (`schedule_policy.py:169–185`): cache-aware `lpm` (*longest prefix match*), `dfs-weight`, `hrrn` (*highest response ratio next*), `shortest-prefill-first`; cache-independent `fcfs`, `lof` (*longest output first*), `random`, `routing-key`. I did not read the default value, so I will not write about it. The idea: **arrange the pending queue so that queries sharing a common prefix go together, before eviction destroys it** — that is the half of RadixAttention responsible for scheduling. There are also `prefill_delayer.py`, `min_free_slots_delayer.py` (admission throttles).

### 4.3 RadixAttention: a radix tree over tokens

`srt/mem_cache/radix_cache.py` (832 lines), `base_prefix_cache.py`, new `unified_radix_cache.py` (3911 lines) and `unified_cache/` — convergence of Full/SWA/Mamba variants into one (`mem_cache/README.md`, issue #20415).

**Structure.** A radix tree over token IDs. Key: `RadixKey(token_ids, extra_key)`; `extra_key` creates a tree namespace (different LoRA adapters or cache salts never share nodes); keys are aligned to the page size (`page_size`) before matching.

**Analogy:** it is like a file system in which the “path” is a token sequence, and a directory splits exactly where two paths stop being common. **Strictly:** `match_prefix` returns the longest prefix from the cache and **splits the node in place** when the match ends in the middle of a segment (“the node is split once to expose a precise boundary”); `insert` stores the KV slot indices for the query tokens after it has run.

Example: two agent queries sharing a system prompt (letters are tokens, illustration):

```
Query 1:  S S S S S S | a b c            (S = system prompt + tool schemas)
Query 2:  S S S S S S | x y z w

After query 1 the tree has one leaf node:

   root ──► [ S S S S S S a b c ]                       (one segment)

Query 2 arrives. match_prefix matches 6 S tokens and ends
in the MIDDLE of a segment → the node is split:

   root ──► [ S S S S S S ] ──┬──► [ a b c ]            (query 1)
              (common)        └──► [ x y z w ]          (query 2: only this is counted anew)

Prefill of query 2 covers 4 tokens (x y z w), not 10.
```

**Pinning:** `inc_lock_ref(node)` / `dec_lock_ref` — nodes used by in-flight queries have `lock_ref > 0` and cannot be evicted.

**Eviction** (`radix_cache.py:552–580`): `evictable_leaves` are collected, a heap is built over `eviction_strategy.get_priority(node)`, the lowest are popped until `num_tokens` are freed; freeing a leaf can make its parent a leaf and push it onto the heap — eviction therefore walks a branch from tip to root. Policies (`radix_eviction_policy.mdx`): `lru` (default), `lfu`, `slru`, `priority`, `tlru` (TTFT-aware, for agent tails).

**Memory under the tree** (`mem_cache/README.md`): `allocation.py` → `hybrid_cache/` (layer→pool router) → `allocator/` (“give me N slots”) → `pool/` (KV on device, L1) → `pool_host/` (L2) → `storage/` (L3). In the original project slots are **token-based** (page = 1, “token attention”), not 16-token blocks as in vLLM; paging is enabled with `page_size>1` (required by some kernels) — I did not verify the default value.

**HiCache:** hierarchical KV cache L1 GPU → L2 host memory → L3 storage (file, NIXL, HF3FS, Mooncake…).

**Contrast with vLLM:**

| | vLLM | SGLang |
|---|---|---|
| Structure | hash chain of full blocks | explicit radix tree with node splitting |
| Match granularity | whole block | token (at page_size=1) |
| Scheduling | FCFS/priority; prefix helps “by the way” | prefix-aware policies (`lpm`, `dfs-weight`) |
| Routing | KV events for external routers | built-in `cache_aware` gateway |
### 4.4 Model execution, kernels, gateway

**Executor** (`srt/model_executor/`, 24,057 lines): `model_runner.py` (2,593), `forward_batch_info.py` (2,338; `ForwardBatch`), CUDA graph runners split into `runner/decode_cuda_graph_runner.py` (1,747) and `runner/prefill_cuda_graph_runner.py` (2,353) — **SGLang also captures prefill graphs**; `cpu_graph_runner.py`, `pool_configurator.py`.

**Backend notes.** `srt/layers/attention/` contains FlashInfer, FlashAttention (FA3/FA4), Triton, TRT-LLM MHA/MLA, FlashMLA, CuTe-DSL MLA, Torch-native/Flex, and for AMD `aiter_backend.py`, `wave_backend.py`, `hip_flash_mla.py`. Selection documentation: for Blackwell SM120 (RTX PRO 6000) `triton` or `flashinfer`; for ROCm "`triton` recommended" (line 403).

**Kernels** (`python/sglang/kernels/`, 450k lines): `aot/` (formerly `sgl-kernel`, ahead-of-time compiled CUDA/HIP/CPU/MUSA kernels — history *unverified*), `jit/` (templates compiled on the fly), `ops/`. SGLang relies on **FlashInfer** (pinned `flashinfer_python==0.7.2`, `python/pyproject.toml`) and DeepGEMM/DeepEP/FlashMLA from DeepSeek for MoE.

**Gateway** (`sgl-model-gateway/`, Rust): control plane (worker registry, health, K8s discovery) and data plane (HTTP and gRPC routers, PD routing, OpenAI proxy router to remote providers) with `random`, `round_robin`, `cache_aware`, `power_of_two`, `bucket` policies, retries, circuit breakers, limits, OTel/Prometheus. Claim from the v0.4 blog: cache-aware router raises throughput from 82,665 to 158,596 tok/s (1.9x), and cache hits from 20% to 75%, on 8x A100-80GB, Llama-3.1-8B-Instruct, workload with multiple prefix groups *(project's own claim; setup as given)*.

### 4.5 Disaggregation, experts, speculation, API

- **Disaggregation** (`srt/disaggregation/`, 35,154 lines): prefill/decode with transfer backends Mooncake, NIXL, MoRI (ROCm), Ascend; plus encoder/prefill/decode ("EPD") for multimodality.
- **Parallelism:** TP, PP (`scheduler_pp_mixin.py`), DP and "DP attention" (for MLA/MoE), **expert parallel** with DeepEP and EPLB load balancing (`srt/eplb`, `srt/elastic_ep`), context parallel for long prefill.
- **Speculative decoding** (`srt/speculative/`, 31,492 lines): EAGLE/EAGLE3 (v2 workers with graph runners for the draft), multi-layer EAGLE, MTP ("frozen_kv_mtp"), n-gram (`cpp_ngram`), DFlash/dspark variants, adaptive parameters. General principle — in the directory [`../speeding-up-generation/README.md`](../speeding-up-generation/README.md).
- **Structured output** (`srt/constrained/`): xgrammar, llguidance, outlines (with *jump-forward decoding*), reasoning-aware backend; from the v0.4 blog: xgrammar "up to 10x faster" for JSON than other open-source solutions *(project's own claim)*.
- **API** (`srt/entrypoints/`): OpenAI (chat, completions, embeddings, rerank, score, classify, tokenize, responses, audio), **Anthropic**, **Ollama**, gRPC, offline `Engine`. Unlike vLLM, SGLang ships an Ollama-compatible facade in the tree.
- **Tool and reasoning parsers:** `srt/function_call/` (15,162 lines), `srt/parser/` (7,640).
- **Other:** LoRA, multimodal, deterministic inference (`batch_invariant_ops`), weight sync for RL (`weight_sync`, `checkpoint_engine`), beam search, "dLLM" scheduler for diffusion models.
### 4.6 SGLang on ROCm: List of Supported Targets

To put it simply: **the R9700 is not a supported target.** Evidence from the code and docs:

1. The AMD document (`docs/docs/hardware-platforms/amd_gpu.mdx`) is entirely about the MI300X (GRUB `iommu=pt`, NUMA balancing) and installs `sgl-kernel` via `setup_rocm.py`.
2. `setup_rocm.py` accepts targets **`["gfx942", "gfx950", "gfx1250"]`**; for anything else it warns "Unsupported GPU architecture".
3. Docker images: `docker/rocm.Dockerfile` with `GPU_ARCH=gfx942|gfx950|gfx1250` and a **separate** `docker/rocm-gfx1151.Dockerfile` for Strix Halo (comment: "This is NOT a variant of docker/rocm.Dockerfile … includes components which do not support gfx1151", run with `--attention-backend triton`). There is no Dockerfile for gfx1200/1201.
4. Attention docs: "AMD (ROCm): triton recommended"; the `aiter` and `wave` backends exist.
5. A tree search for `gfx1201`/`gfx1200` yielded nothing relevant.
6. The README declares AMD Instinct MI300X/MI325X/MI350X/MI355X *(project's own claim)*.

Possible but **unverified**: SGLang may run on gfx1201 on plain PyTorch and Triton attention, without `sgl-kernel`. Nobody declares this and the docs don't mention it, so I wouldn't build a plan on it. GGUF in SGLang (`quantization.mdx`): "CUDA kernels in sgl-kernel; Ascend uses CPU pre-dequantization at load time" — **no ROCm kernels**. Plain `gptq` is "Removed on NVIDIA and AMD GPUs — use gptq_marlin instead".

### 4.7 Strengths and Weaknesses, Offline, Who Is Behind It

**Strengths:** best-in-class prefix reuse and cache-aware routing for agent loops; strong work on DeepSeek/MoE (EP, EPLB, PD); OpenAI + Anthropic + Ollama APIs in one server. **Weaknesses for you:** RDNA4 is not a target; tighter coupling with NVIDIA/FlashInfer than in vLLM; rapid internal changes (the snapshot has major refactors in progress: unified cache, `arg_groups` — flags and APIs change between 0.5.x releases, that's *my inference from the file layout*); AMD docs written for the MI300X.

**Offline.** Works with local weights. A grep of `python/sglang` for `telemetry|usage_stats|posthog|DO_NOT_TRACK` found only OpenTelemetry *tracing* (disabled by default: `enable_trace`, `arg_groups/fields/observability.py:164`) and test tooling — **I found no usage reporter** (evidence from the absence of grep results).

**Who is behind it.** The project is hosted by **LMSYS** (Large Model Systems Organization), per lmsys.org/about a 501(c)(3) non-profit established in September 2024, out of the original Berkeley/Stanford/UCSD/CMU/MBZUAI collaboration *(organization's own claim)*; supported by NVIDIA, Google Cloud, a16z, AMD, Hugging Face, Together, and others in cash, GPUs, and credits. SGLang joined the **PyTorch ecosystem** (not hosted by the foundation). The paper's authors now work at various places (GitHub profiles: Lianmin Zheng — "Meta"; Liangsheng Yin and Ying Sheng — "RadixArk"). **RadixArk** is a company formed around SGLang; Wikipedia, citing TechCrunch from 2026-01-21, gives a $400M valuation *(press report, single source)*; round amounts, investors, and founders I could not establish. For details — [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

> **Check it yourself (3) — which ROCm architectures does SGLang know.**
> ```bash
> sed -n '60,80p' python/sglang/kernels/aot/setup_rocm.py
> ls docker/ | grep -i rocm
> grep -rn "gfx1201\|gfx1200" python/sglang docker | head
> ```
> The first command will show `["gfx942", "gfx950", "gfx1250"]`; the third, per my notes, finds nothing relevant. *(Not run by me; paths from my notes.)*
## 5. TensorRT-LLM, TGI (archive and lesson), LMDeploy

### 5.1 TensorRT-LLM (NVIDIA)

**One-liner:** NVIDIA's own stack for NVIDIA cards — a PyTorch executor around hand-tuned CUDA/CUTLASS kernels and a C++ batch/KV manager, which exists to squeeze the last factor out of NVIDIA silicon (FP8/NVFP4, NVLink, Blackwell).

- **License:** GitHub shows `NOASSERTION` ("Other"). Reason from the `LICENSE` file: "This project is licensed under the Apache 2.0 license … contains portions of code that are based on or derived from other open source projects, which may have different licenses", followed by a list of attributions (Bitcoin Core MIT, causal-conv1d BSD-3, CUTLASS BSD-3 …). So: **NVIDIA code under Apache-2.0 plus notices about third-party code; GitHub's detector cannot pick a single SPDX identifier.**
- Repo `NVIDIA/TensorRT-LLM`, created 2023-08-16, 14,859 stars, 2,838 forks; version in README **1.4.0rc1**, weekly releases (v1.4.0rc0 2026-10-14, v1.3.0rc29 2026-09-29). Languages: Python 78.3 MB, C++ 29.3 MB, CUDA 6.9 MB.
- **Hardware:** NVIDIA only: Blackwell B200/GB200/B300/GB300/DGX Spark; Hopper H100/H200/GH200; Ada L20/L40/L40S; Ampere A100 (`docs/source/supported-hardware.md`). No AMD, no Apple, no CPU.
- **Architecture change (verified):** `docs/source/legacy/tensorrt-backend-removal.md`: "**Breaking change. The TensorRT engine backend has been removed. PyTorch is now the sole execution backend**". `trtllm-build`, `trtllm-refit`, `trtllm-prune`, per-model `convert_checkpoint.py` and the `tensorrt` dependency are gone; "no engine-build step — HuggingFace checkpoints load directly". What remains: `trtllm-serve <hf_model>`, `trtllm-bench`, `trtllm-eval`. The old project (compiling an engine dependent on model, GPU and shapes in advance) is why TRT-LLM is remembered as painful — and why **all articles about `trtllm-build` are outdated**.
- **Today:** `tensorrt_llm/_torch/pyexecutor/py_executor.py` (9,532 lines) is the execution loop in Python; the C++ part (`cpp/tensorrt_llm/batch_manager/`: `capacityScheduler.cpp`, `microBatchScheduler.cpp`, `kvCacheManager.cpp`, `evictionPolicy.cpp`, `cacheTransceiver.cpp`) is exposed to Python via nanobind, and roughly 531k lines of kernels (attention, MoE, GEMM, all-reduce, quantization) are hooked in as torch ops via `thop/`. Documentation: "In-flight batching (also known as continuous batching or iteration-level batching)"; default `max_num_tokens` 8,192; there is an *overlap scheduler* and piecewise CUDA graph + `torch.compile`.
- **Features:** `trtllm-serve` OpenAI-compatible with an **Anthropic adapter**, Responses API, Harmony adapter (gpt-oss), disaggregated server; paged KV with block reuse; chunked prefill; speculation (EAGLE, MTP, n-gram); LoRA; guided decoding; multimodal.
- **Performance:** headline numbers are NVIDIA's *(company's own claim)* (e.g. DeepSeek-R1 "world-record" on Blackwell; Llama 4 Maverick "breaks the 1,000 TPS/user barrier on B200") — I did not open the source posts.
- **Telemetry — enabled by default:** `tensorrt_llm/usage/__init__.py`: anonymous statistics go to NVIDIA's telemetry service (NvTelemetry/GXT), by default `https://events.gfe.nvidia.com/v1.1/events/json` (`usage_lib.py:79`); disabling: `TRTLLM_NO_USAGE_STATS=1`, `TELEMETRY_DISABLED=true|1`, `DO_NOT_TRACK=1`, file `~/.config/trtllm/do_not_track`, `TelemetryConfig(disabled=True)` or `--no-telemetry`.
- **Who is behind it:** NVIDIA employees (in the committer ranking the bots `tensorrt-cicd`, `trtllm-agent`, then staff); a strategic product that sells GPUs. Corporate governance. License risk low, third-party code notices must be respected.
- **For you:** educational only — it shows where NVIDIA-specific performance comes from.
### 5.2 TGI (Hugging Face) — archive and lesson

**One-liner:** Hugging Face's LLM server with a Rust router and Python shards over gRPC, the engine behind Inference Endpoints/HuggingChat; today in maintenance mode, and the repository is archived.

- Repo `huggingface/text-generation-inference`, created 2022-10-08; 10,879 stars; **`archived = true`**; last push 2026-03-21 (documentation commit); last release **v3.3.7, 2025-12-19**.
- **README notice** (commit "Maintenance mode (#3344)", **2025-12-11**): "text-generation-inference is now in maintenance mode. Going forward, we will accept pull requests for minor bug fixes, documentation improvements and lightweight maintenance tasks. TGI has initiated the movement for optimized inference engines to rely on a `transformers` model architectures. This approach is now adopted by downstream inference engines, which we contribute to and recommend using going forward: **vllm, SGLang, as well as local engines with inter-compatibility such as llama.cpp or MLX.**" I could not establish a dated "archived" announcement; the maintenance-mode decision is 2025-12-11, while the archive flag and last push point to March 2026.
- **License history** (from commits touching `LICENSE`): Apache-2.0 (2022) → **2023-07-28 changed to HFOIL** (restrictive HF license; "chore: update license to HFOIL (#725)") → **2024-04-08 reverted to Apache-2.0** ("Revert license to Apache 2.0 (#1714)"). I could not establish the reasons for either change in the repo — I do not give them.
- **Features:** router with continuous batching, SSE streaming, tensor parallelism, OpenAI-compatible Messages API, Flash/Paged attention (the README explicitly points to PagedAttention from vLLM), bitsandbytes/GPTQ/EETQ/AWQ/Marlin/fp8 quantizations, grammar-guided tools. Backends: custom CUDA (`v2`, `v3`), TRTLLM, Llamacpp, Neuron (AWS), Gaudi; ROCm images cover "AMD Instinct MI210, MI250 and MI300" — **no Radeons**.
- **Telemetry:** usage statistics only "when TGI is running in a Docker container" (start/stop plus a heartbeat every 15 minutes; `router/src/usage_stats.rs`).
- **Who is behind it:** Hugging Face as a company (products: Inference Endpoints, HuggingChat); authors: Olivier Dehaene (original author), Nicolas Patry, Daniël de Kok.

**Lesson (grounded):**

1. HF stopped maintaining its own zoo of model implementations. TGI had hand-written, optimized per-architecture code; the new direction is "engines rely on model definitions from `transformers`". Maintaining per-architecture kernels did not scale against the vLLM/SGLang community (this is *my inference*; the notice itself is verified).
2. The licensing turbulence (Apache → HFOIL → Apache) cost trust and may have helped vLLM/SGLang adoption — *unverified*.
3. A Rust router + Python shards over gRPC is a good split; the new Rust front-end in vLLM and the Rust gateway in SGLang recreate it.
4. **For you:** choose engines with a foundation or multiple sponsors. A single owner is a single point of decision to abandon the project.
### 5.3 LMDeploy (TurboMind)

**One-liner:** a toolkit for compressing, deploying, and serving LLM/VLMs with two engines — TurboMind (C++/CUDA; the README thanks NVIDIA FasterTransformer) and a pure-Python PyTorch engine — built by the MMRazor/MMDeploy teams around the InternLM models.

- Apache-2.0; repo `InternLM/lmdeploy`, created 2023-06-15; 8,108 stars; **v0.18.0, 2026-09-28**; Python 10.2 MB, C++ 2.9 MB, CUDA 1.4 MB.
- **Features** *(project's own claim, README)*: 4-bit weight quantization (AWQ-like W4A16) and int4/int8 KV with TurboMind kernels, persistent batch (continuous batching), block-wise KV, dynamic split&fuse, TP, prefix caching, proxy server for multiple machines and models, PD disaggregation via DLSlime/Mooncake (2025/06), MXFP4 on NVIDIA from V100 up.
- **Performance:** its own claims: "up to 1.8× higher query throughput than vLLM" (InternLM2-20B, 2024); paper "LMDeploy Accelerates Mixed-Precision LLM Inference with TurboMind", arXiv 2508.15601: "up to 61% lower serving latency (30% on average) and up to 156% higher throughput (58% on average)" versus competing mixed-precision frameworks, 16 LLMs and 4 GPU architectures — **authors' benchmark**.
- **Hardware:** NVIDIA Volta..Ada; the PyTorch engine adds Ascend, Cambricon, MetaX. **ROCm:** installable via `LMDEPLOY_TARGET_DEVICE=rocm pip install git+...` in the `rocm/pytorch` container, with no list of supported GPUs; the fast TurboMind engine is CUDA-only. **No evidence for RDNA4.**
- **Architecture** (only the tree with the API; I did not clone the code): `lmdeploy/turbomind/` + `src/turbomind/` (C++/CUDA), `lmdeploy/pytorch/` (engine in Python, easier to extend to new hardware), `lmdeploy/serve/`, `lmdeploy/vl/`, `lmdeploy/lite/` (quantization). Design assumption: an efficient engine in C++ plus a hookable engine in Python.
- **Who is behind it:** a lab-and-industry project (MMRazor/MMDeploy teams, InternLM family — the link to Shanghai AI Laboratory is *my inference*, not an established fact); no company or funding found; Chinese-speaking community. Operational curiosity: the README from April 2026 mentions extending the PyPI limit, which suggests that the large CUDA wheels were exceeding the limits.

---

## 6. Cluster layers: Dynamo, llm-d, LMCache, FlashInfer, FlashAttention, Modular MAX

These components sit **above** the engine, **next to** it, or **below** it. They exist because when you have many GPUs, many nodes, and thousands of users, the unit of optimization stops being "one engine" and becomes "a fleet". For each card, the answer to the question: **does a four-GPU box need this?**

### NVIDIA Dynamo

- **Layer:** orchestration *above* the engines. README: "the orchestration layer above inference engines — it doesn't replace SGLang, TensorRT-LLM, or vLLM, it turns them into a coordinated multi-node inference system". Core in Rust, Python for extensions.
- **Identity:** `ai-dynamo/dynamo`, created 2025-03-03, 8,332 stars. GitHub shows `NOASSERTION` because `LICENSE` starts with a note about test data under MIT; "The rest of this codebase is licensed under the Apache License 2.0".
- **What it does:** prefill/decode disaggregation with independent GPU pools; **KV-aware routing** (to the worker with the largest cache overlap and the lowest load); **KVBM** (moving blocks GPU→CPU→SSD→remote storage); **ModelExpress** (streaming weights GPU→GPU via NIXL/NVLink); **Planner** (autoscaling by SLA); **Grove** (K8s operator with topology-aware gang scheduling, NVL72). Supports SGLang, TensorRT-LLM, and vLLM; in what I read, validated on NVIDIA hardware, and I found no mention of ROCm in the README.
- **Numbers** *(company's own claim, partners; different hardware — do not compare)*: "7x higher throughput per GPU, DeepSeek R1 on GB200 NVL72 vs B200 without it", "750x … on GB300 NVL72", "80% fewer SLA violations at 5% lower TCO (Alibaba)".
- **Do you need it?** **No.** The README itself says: "If you're running a single model on a single GPU, your inference engine alone is probably sufficient". Educational value: the clearest picture of what happens *after* a single box.
### llm-d

- **Layer:** a Kubernetes-native distributed serving layer *on top of* model servers (vLLM, SGLang): prefix- and load-aware routing, multi-tier KV offload with a global index, PD disaggregation, wide expert parallelism, flow control, SLO-aware autoscaling, batch API.
- **Identity:** `llm-d/llm-d`, Apache-2.0, created 2025-04-29, 4,866 stars; v0.10.0 (2026-09-29). "a Cloud Native Computing Foundation (CNCF) sandbox project, founded by Red Hat, Google Cloud, IBM Research, CoreWeave, and NVIDIA"; joined CNCF in 2026-03.
- **People:** top committers from Red Hat/@llm-d, Google (Abdullah Gharaibeh), and Robert Shaw (Red Hat, also vLLM core) — the vLLM–Red Hat axis is central to it.
- **Numbers** *(partners' own claim)*: "3× higher output throughput and 2× faster TTFT with prefix-aware routing vs round-robin, Llama 3.1 70B on 4× AMD MI300X (Red Hat)"; "13.9× throughput with hierarchical KV offload at 250 users, 4× H100". Some results are on **AMD MI300X**, so llm-d is not locked to NVIDIA — but that's Instinct, not RDNA.
- **Do you need it?** **No** — it requires Kubernetes. From the whole tool, what's useful to you is the *idea*: route queries with the same prefix to the same backend.

### LMCache

- **Layer:** a KV cache management layer outside GPU memory: stores KV in CPU RAM, on SSD, in Redis/Valkey, Mooncake, S3, NIXL, GDS; reuses it across queries, sessions, and engine instances; moves it between prefill and decode workers. Supports **non-prefix reuse** (CacheBlend: chunks from any position with selective recomputation); the multi-process `lmcache server` mode survives an engine crash.
- **Identity:** `LMCache/LMCache`, Apache-2.0, created 2024-05-28, 12,116 stars; nightly builds for **ROCm and XPU**; vLLM has first-class connectors (`lmcache_connector.py`, `lmcache_mp_connector.py`), but its ROCm Dockerfile builds LMCache only for gfx942/gfx950; also integrates with Dynamo.
- **Who:** in the LMCache blog, joining the PyTorch Foundation as an ecosystem project (2025-10-31), plus the company **Tensormesh** (the LMCache and vLLM production stack team). I could not confirm the funding amounts declared on Tensormesh's site — I don't list them. University lineage — *unverified*.
- **Do you need it?** **Probably not.** vLLM has its own CPU KV offload (`kv_offload/`), so you get about 80% of the idea without LMCache (*unverified*, inference). Desktop analogy: save/restore slot in llama.cpp.

### FlashInfer

- **Layer:** a serving kernel library: attention (paged/ragged KV, decode/prefill/append, MLA, cascade, sparse), GEMM (FP8, NVFP4/MXFP4 on Blackwell), fused MoE, top-k/top-p sampling, communication. **NVIDIA only, SM75 and newer.**
- **Identity:** `flashinfer-ai/flashinfer`, Apache-2.0, created 2023-07-22, 6,708 stars, v0.7.2 (2026-10-15). arXiv paper 2501.01005, MLSys 2025, authors include Zihao Ye, Tianqi Chen, Luis Ceze; claimed 29–69% inter-token latency reduction vs compiler backends *(authors' own claim)*. Under SGLang (hard dependency) and vLLM; optional in TRT-LLM.
- **Do you need it?** **No, you have no path to it.** Just know that every vLLM/SGLang benchmark on NVIDIA is partly a FlashInfer benchmark.
### FlashAttention (Tri Dao)

- **Layer:** precise, IO-aware fused attention kernels that do not materialize the N×N result matrix — the root of the entire family (FlashInfer, the `vllm_flash_attn` fork in vLLM, FA3/FA4 backends in SGLang). Repo `Dao-AILab/flash-attention`, **BSD-3-Clause**, 25,161 stars. Versions: FlashAttention (arXiv 2205.14135, NeurIPS 2022), FlashAttention-2, FlashAttention-3 (Hopper, FP8), **FlashAttention-4** in CuTeDSL for Hopper and Blackwell.
- **People:** Tri Dao — professor at Princeton, co-founder and chief scientist at Together AI (tridao.me).
- **AMD thread, directly relevant for the R9700** (README, "AMD ROCm Support"): two backends. (1) **Composable Kernel (CK)** — FlashAttention-2, "MI200x, MI250x, MI300x, MI355x, and RDNA 3/4 GPUs"; (2) **Triton backend** (`FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"`) for CDNA and RDNA in fp16/bf16/fp32, with causal masks, variable lengths, MQA/GQA, ALiBi, paged attention, and FP8 via the FA3 interface; kernels from the ROCm `aiter` package included as a submodule. vLLM uses this only for vision encoders on RDNA when the environment variable is set (§3.2).
- **Do you need it?** You already have the algorithm — via llama.cpp's own flash attention kernels. The "FA2-CK for RDNA 3/4" claim is worth testing if you ever run PyTorch-based stacks.

### Modular MAX / Mojo

- **Layer:** a vertically integrated stack: the Mojo language (Python syntax on MLIR), the MAX framework and kernels, an OpenAI-compatible server; the slogan "one code base for any accelerator".
- **Identity:** `modular/modular`, 29,977 stars; version `max/v26.6.0` (2026-09-17). **Two licenses**: the repository under "Apache License v2.0 with LLVM Exceptions", and MAX usage under the "Modular Community License" (I did not read the terms). The Mojo compiler was open-sourced in August 2026.
- **Company:** founded by Chris Lattner (LLVM, Clang, Swift) and Tim Davis *(company's own claim)*. **Qualcomm announced the acquisition on 2026-06-24 and closed it on 2026-07-29** (undisclosed price) *(company's own claim; I did not open Qualcomm's press release)*. I did not verify earlier funding rounds — I will not list them.
- **Hardware** *(company's own claim, package page)*: NVIDIA B200 "tested for serving"; AMD MI355X tested for serving; **"Radeon RX 7900/7800/7600 (RDNA3) and newer RDNA4 variants are compatible"** (AMD driver 6.3.3+); Apple M1–M5 "actively developing". "Compatible" is weaker than "tested"; I found no numbers for gfx1201. This is the **only engine besides vLLM in this chapter with a declared RDNA4 compatibility claim**.
- **Do you need it?** Not as a production replacement for vLLM/SGLang — model coverage is smaller *(unverified)*, and the owner is new. Worth a weekend test if you care about Mac + AMD portability.

> **Check it yourself (4) — TGI status and release cadence.**
> ```bash
> gh api repos/huggingface/text-generation-inference --jq '.archived, .pushed_at'
> gh api "repos/vllm-project/vllm/releases?per_page=5" --jq '.[].tag_name, .[].published_at'
> ```
> The first should return `true` and a March 2026 date; the second will show vLLM's release rhythm. *(Not run by me; per the `gh` configuration, it must be run outside the sandbox.)*
## 7. Comparison table: vLLM, SGLang, TensorRT-LLM, llama.cpp

Exclusively from notes; as of 2026-10-19; stars from the GitHub API.

| | **vLLM** | **SGLang** | **TensorRT-LLM** | **llama.cpp** |
|---|---|---|---|---|
| License | Apache-2.0 | Apache-2.0 | Apache-2.0 + third-party code notices (GitHub: NOASSERTION) | MIT |
| Stars | 94,152 | 37,445 | 14,859 | 131,716 |
| Version | v0.32.0 (2026-10-18) | v0.5.22 (2026-10-19) | 1.4.0rc1 (weekly RC) | b11741 (build numbers, no semver) |
| Main languages | Python (+Rust, CUDA, C++) | Python (+Rust gateway, CUDA) | Python + C++ + CUDA | C/C++ |
| Goal | throughput for many users | agents, RL, prefixes, MoE | maximum on NVIDIA | single user, local |
| KV cache management | blocks + block table, prefix hash chain | radix tree, token slots, HiCache | paged KV with block reuse (C++) | contiguous KV per slot; LCP matching, RAM cache `--cache-ram` 8192 MiB, context checkpoints; **no** PagedAttention |
| Continuous batching | yes, token-budget scheduler | yes, prefix-aware policies | yes (*in-flight batching*) | yes, but simpler scheduler; `-np` = number of slots, default 1 |
| Tensor split / tensor parallelism | TP/PP/DP/EP/CP; "strong multi-GPU TP on identical cards" (rating from notes) | TP/PP/DP/EP (+ DP attention, context parallel) | supported; oriented toward NVLink/NVL72 | `-sm tensor` **experimental**, requires flash attention and unquantized KV |
| Formats | HF/safetensors; AWQ, GPTQ, FP8, FP4, compressed-tensors…; GGUF outside the core (plugin, "experimental") | HF; FP8, FP4, AWQ, gptq_marlin…; GGUF only CUDA/Ascend | HF; FP8, NVFP4; INT4/INT8 | **GGUF** (HF via conversion) |
| API | OpenAI + Anthropic + Cohere + gRPC; **no Ollama** | OpenAI + Anthropic + **Ollama** + gRPC | OpenAI + Anthropic adapter + Responses | OpenAI + Anthropic `/v1/messages` + Responses |
| Hardware | NVIDIA, ROCm, Intel XPU, CPU, TPU; plugins (Ascend, Gaudi, Metal…) | NVIDIA, AMD Instinct, TPU, Intel, Apple (README), Ascend | **NVIDIA only** | CPU + approx. 15 backends (CUDA, HIP, Metal, Vulkan…) |
| **gfx1201 (R9700)** | **claimed**: documentation, default arch, PCI id, RDNA kernels; unverified by test | **unsupported** (targets: gfx942/950/1250) | not applicable | **works** (HIP build for exact `gfx1201`) |
| Model swapping | one model per process; `/sleep` | I could not establish | I could not establish | router mode, `--models-max` default 4; llama-swap |
| Graphs / compilation | `torch.compile` piecewise + graphs (default `FULL_AND_PIECEWISE`) | decode **and** prefill graphs | piecewise CUDA graph + `torch.compile` | no equivalent in these notes |
| GPU memory pre-allocation | `gpu_memory_utilization` 0.92 | I could not establish | I could not establish | based on `-c` and `-ngl` |
| Telemetry | **enabled by default**, opt-out | not found | **enabled by default**, opt-out | not checked in these notes |
| Foundation | PyTorch Foundation (2025-05) | LMSYS (501(c)(3)) + PyTorch ecosystem | NVIDIA | company/maintainers; see [ch. 04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |

Note on the "gfx1201 / llama.cpp" row: this is the state of *your* production configuration (llama.cpp + llama-swap on R9700), not a result from the server notes. Detailed data on HIP and `-sm tensor` in llama.cpp: [ch. 04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md).

⚠️ Do not compare "performance" rows — they are intentionally absent. The notes contain no measurement on a single piece of hardware for all four engines, and the projects' numbers come from different cards, models, and workloads.
## 8. What this means for the reference setup

### 8.1 When to switch from llama.cpp to vLLM/SGLang

Rule of thumb from the notes (*opinion, unverified*): **server engines when the load is many concurrent requests with shared prefixes and the models are in HF format (BF16/FP8/GPTQ-INT4); llama.cpp + llama-swap for interactive single-stream work, a variety of quants, and frequent model swaps.**

Broken down by your reasons:

| Situation | Why a server engine | Note for the reference machine |
|---|---|---|
| **Many parallel agents** (fan-out, many parallel tool calls) | batching amortizes weight reads (§1.1), continuous batching keeps the GPU busy | llama.cpp also has slots (`-np`), but a simpler scheduler and no paged KV |
| **Long shared prefixes** (system prompt + tool schemas) | global prefix cache (vLLM) or radix tree (SGLang) works across requests; in llama.cpp reuse is per slot | `--cache-ram`, `--cache-idle-slots`, `--ctx-checkpoints` in llama.cpp cover part of the need — check that first |
| **FP8 hardware** | FP8 and FP4 kernels are at the center of attention for these engines | vLLM allows FP8 on RDNA4 in code; performance was not measured |
| **Non-GGUF checkpoints** (HF, safetensors, calibrated quants) | that is the native format; new models appear here fastest *(unverified)* | this is the only scenario where GGUF quantizations stop being fuel for you |
| Embeddings/rerank as services alongside chat | endpoints in one server (vLLM) | |

Also see ready-made ideas to copy into your own orchestrator: route requests with the same prefix to the same backend (pattern from the `cache_aware` policy in the SGLang gateway); `cache_salt` in vLLM as a way to isolate between tenants/agents; the "scheduler one batch ahead" pattern; a registry of tool/reasoning parsers per model family separated from the engine; `sleep`/`pause`/`resume` endpoints and LoRA hot-swap as GPU-sharing primitives.

### 8.2 Why the experiment is not worth the effort today on gfx1201 — unless …

Reasons that follow directly from the notes:

1. **The reference model.** The reference setup runs a 284B MoE in UD-IQ3_XXS. To run it in vLLM, you would need a checkpoint in HF format. The weight arithmetic alone: 284B parameters at 0.5 B in INT4 is ≈142 GB, and in FP8 ≈284 GB (*my calculation*, without KV and overheads); four cards give 4 × 32 = 128 GB. **This model in HF-INT4 would not fit in VRAM** even without KV. (vLLM does have the `deepseek_v4_fp8` quantization in the registry and DeepSeek V4 parsers, but the weight size settles the matter.) Its IQ3 quantization is exactly what server engines do poorly (§3.4).
2. **GGUF in vLLM** is a plugin, "highly experimental and under-optimized"; it is not on the ROCm quantization list.
3. **SGLang** does not have gfx1201 among its targets (§4.6). Come back when `setup_rocm.py` lists gfx12xx.
4. **vLLM pre-allocation** (0.92) conflicts with llama-swap on the same cards.
5. **TP over PCIe:** no own all-reduce outside MI300/MI350, RCCL over PCIe; scaling limited by bandwidth *(unverified)*.
6. **No independent measurements** of vLLM on RDNA4 — the notes contain not a single one.

**When it is worth it (X):** when **all three** conditions are met **simultaneously**:

- the load is **many parallel agents or requests with long shared prefixes**, not a single interactive conversation;
- the target **model exists in HF format (FP8 or INT4 GPTQ/AWQ) and fits in 128 GB with headroom for the KV pool** — that is, it is much smaller than your 284B;
- a **one-day test on isolated cards** (list from §3.7) confirms that the attention backend, the W4A16/FP8 kernel, and `-tp=4` start stably on gfx1201 and that the result measured by `vllm bench` at *your* request count beats the llama.cpp configuration.

If any of the three conditions is not met, llama.cpp + llama-swap remains the right choice for this machine. The last sentence of the notes reads: *"On R9700s, vLLM is the only engine here with documented RDNA4 support; test it before betting on it."*
### 8.3 What to take away, even without running vLLM

- **Understanding the cost** — why agentic applications with many parallel calls behave differently from a conversation: it all comes down to how many sequences fit in a single step and whether the prefix survives.
- **llama.cpp settings that implement the same ideas** (ch. 04): `--parallel` and a stable `id_slot`, `--cache-ram`, `--ctx-checkpoints`.
- **Caution with telemetry**: with every server-side tool, set opt-out at entry (vLLM and TRT-LLM send it by default).
- **Market reconnaissance:** three open-source teams (vLLM, SGLang, LMCache) spun off companies within roughly a year (Inferact, RadixArk, Tensormesh), and Modular was acquired by Qualcomm — this does not affect your technical decision, but it changes who sets the direction of these projects. The funding figures in the notes are single-source (Inferact: $150M from the company's own headline and Wikipedia; RadixArk: $400M valuation from press reports only), so the details and tags are in [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

Further chapters: comparison of all runtimes and the choice — [`09-COMPARISON-AND-CHOICE.md`](09-COMPARISON-AND-CHOICE.md); Apple and MLX — [`07-APPLE-MLX-OMLX-AND-DS4.md`](07-APPLE-MLX-OMLX-AND-DS4.md); specialists (incl. KTransformers, hybrid CPU+GPU paths for large MoEs) — [`08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS.md`](08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS.md).
