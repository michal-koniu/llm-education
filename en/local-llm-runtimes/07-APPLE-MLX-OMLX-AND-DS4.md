# 07 · Apple Silicon and single-model engines: MLX, mlx-lm, oMLX, ds4, exo

## Why this chapter

So far (chapters 04–06) we have talked about engines that try to serve **every** model on **every** piece of hardware: llama.cpp, Ollama, vLLM, SGLang. This chapter is about the opposite pole: engines that deliberately give up universality — either in favor of **one platform** (Apple Silicon), or even **one model family** (ds4/DwarfStar).

After reading it you will be able to:

- explain why on a Mac generation speed is decided by **memory bandwidth**, not by "GPU power", and calculate the tok/s ceiling for any M-series chip;
- tell apart four layers: **MLX** (array framework), **mlx-lm** (LLM library on top of MLX), **oMLX** (server on top of mlx-lm) and **exo** (cluster layer on top of MLX);
- say what "oQ4e" means, how the two-tier (RAM + SSD) KV cache in oMLX works, and why coding agents need it;
- understand the **engineering argument for a single-model engine** (ds4) and judge what of it can be carried over to llama.cpp;
- honestly assess what of all this works on the reference 4× R9700 (gfx1201) rig — **spoiler: almost nothing, apart from ideas**.

> ⚠️ **I did not run anything here.** The whole chapter is *desk research* plus reading source code (repository clones from 2026-10-19) and the GitHub API. I neither tested nor measured any of the described engines. All performance figures come from the projects or from third parties and are labeled as such; figures marked "my calculation" are arithmetic on verified inputs, not a measurement. As of **19 October 2026** — ds4 and oMLX change daily.

> ⚠️ **The reference rig (4× Radeon AI PRO R9700, gfx1201, ROCm):** MLX has no HIP/ROCm backend, oMLX runs only on Apple Silicon, exo on Linux runs only on CPU, and ds4 has ROCm only for gfx1151 (Strix Halo). **You cannot run anything from this chapter on the rig.** The chapter is for Macs and for ideas you carry over to llama.cpp.

## Table of contents

1. [Why Apple Silicon is different](#1-why-apple-silicon-is-different) — shared memory, bandwidth, the ceiling table
2. [MLX — the array framework](#2-mlx--the-array-framework)
3. [mlx-lm — the LLM layer](#3-mlx-lm--the-llm-layer)
4. [oMLX in depth](#4-omlx-in-depth) — continuous batching, a paged cache with an SSD tier, oQ, MTP
5. [ds4 / DwarfStar in depth](#5-ds4--dwarfstar-in-depth) — a single-model engine
6. [Apple's own stack](#6-apples-own-stack-foundation-models-core-ml-core-ai-ane)
7. [exo — a cluster of Macs](#7-exo--a-cluster-of-macs)
8. [What this means for the reference setup](#8-what-this-means-for-the-reference-setup)

Glossary for this chapter (see also `02-HOW-INFERENCE-WORKS.md`): *generation speed (tok/s)*, *prefill* (reading the prompt), *decoding*, *KV cache*, *quantization*, *experts (MoE)*, *continuous batching*, *tensor parallelism*, *pipeline parallelism*.

---

## 1. Why Apple Silicon is different

### 1.1 One memory for CPU and GPU

The reference rig has two memory worlds: system RAM (DDR5, wide but slow) and the cards' VRAM (GDDR6, 32 GB per card, fast). Weights that do not fit in VRAM have to be "spilled" into RAM and shipped over PCIe — and that is usually exactly where speed ends.

In Apple Silicon chips (M1…M5) the CPU, GPU and Neural Engine share **a single pool of unified memory**. There is no "host to card" copying: both processors see the same buffer. From the LLM's point of view this means that **all of the machine's memory is "VRAM"** (subject to the "wired" memory limit for the GPU — at 128 GB ds4 recommends `sudo sysctl iogpu.wired_limit_mb=120000`, see §5.9).

An analogy: the rig is two warehouses connected by a narrow bridge; a Mac is one warehouse with wide doors. More precisely: a Mac is not faster at arithmetic than the R9700, it simply **has no bridge**, and its memory is large (64–512 GB in the configurations that people swap notes about).

### 1.2 Bandwidth = generation speed

You remember from chapter 02: decoding means reading all the *active* weights once per token. So

```
tok/s (ceiling) ≈ memory bandwidth / (active parameters × bits per weight / 8)
```

This is an **upper bound**. Real engines usually reach 60–80% of it *(unverified — an engineering rule of thumb, not a measurement from this survey)*. That is why **the chip's GB/s figure is the real spec of a Mac for LLMs**, not the number of GPU cores.

### 1.3 Chip bandwidth — what is verified

| Chip | GB/s | Source |
|---|---:|---|
| M4 Pro | 273 | Wikipedia *(third-party source)* |
| M4 Max (32-core GPU version / full 40-core) | 410 / **546** | Wikipedia *(third-party source)* |
| M3 Max (14 / 16 cores) | 300 / 400 | Wikipedia *(third-party source)* |
| M3 Ultra | **819.3** | Wikipedia *(third-party source)*; Apple ML post "819 GB/s" *(company's own claim)* |
| M5 (base) | 153 (153.6) | apple.com, MacBook Pro specification *(company's own claim)*; Wikipedia *(third-party source)* |
| M5 Pro | 307 | apple.com *(company's own claim)* |
| M5 Max (32 / 40-core GPU) | 460 / **614** | apple.com, MacBook Pro and Mac Studio *(company's own claim)* |
| **M5 Ultra** (Mac Studio, August 2026; 256/512 GB) | **~1.2 TB/s** (1,228.8) | apple.com, Mac Studio *(company's own claim)*; Wikipedia *(third-party source)* |

I give the M5 Ultra value as the sources record it: it is the figure from Apple's specification page, confirmed by Wikipedia; I have no measurement that would check it.

### 1.4 The ceiling table (my calculation)

Assumptions *(my calculation)*: 4-bit weights counted as **4.5 bits per weight including group scales** (affine group quantization with group size 64, or something like Q4_K); a dense 30B model ⇒ 16.9 GB per token; an MoE with 13B active ⇒ 7.3 GB per token (the remaining experts sit idle, short context, batch 1). The "@70%" column is the ceiling × 0.7 — the typical efficiency of well-tuned code *(unverified)*.

| Chip | GB/s | Dense 30B 4-bit: ceiling / @70% | MoE 13B active 4-bit: ceiling / @70% |
|---|---:|---:|---:|
| M5 | 153.6 | 9.1 / 6.4 | 21.0 / 14.7 |
| M4 Pro | 273 | 16.2 / 11.3 | 37.3 / 26.1 |
| M5 Pro | 307 | 18.2 / 12.7 | 42.0 / 29.4 |
| M4 Max (32 cores) | 410 | 24.3 / 17.0 | 56.1 / 39.2 |
| M5 Max (32-core GPU) | 460 | 27.3 / 19.1 | 62.9 / 44.0 |
| M4 Max (full) | 546 | 32.4 / 22.6 | 74.7 / 52.3 |
| M5 Max (40-core GPU) | 614 | 36.4 / 25.5 | 84.0 / 58.8 |
| M3 Ultra | 819.3 | 48.6 / 34.0 | 112 / 78.4 |
| M5 Ultra | 1,228.8 | 72.8 / 51.0 | 168 / 117.6 |

**A sanity check against a measurement** *(project's own claim + my calculation)*: ds4 on an M5 Max 128 GB with DeepSeek V4 Flash in Q2 quantization (13B active) measures **39.35 tok/s** at 2K context. At an *average* of 2.45 bits per weight (see §5.4) the formula gives ~154 tok/s at 614 GB/s — the measurement is about 26% of the ceiling. The explanation (mine, unverified): the attention tensors, shared experts and output tensors are in Q8/F16, not in 2 bits, so per token you actually read the equivalent of about 15.6 GB (614 / 39.35), not ~4 GB. The notes also do not say whether the CSV file comes from an M5 Max with 40 or 32 GPU cores; at 460 GB/s the proportion would come out at ~34%.

**Takeaway:** the formula is an *upper bound*; non-uniform quantization and memory traffic that the formula ignores push MoE models much lower, while dense models sit closer to the ceiling. A second test: the same Spark/M5 Max proportion. The DGX Spark has 273 GB/s *(unverified — from the notes author's memory)*, and ds4 measures 18.05 tok/s there versus 39.35 on the M5 Max; the ratio is 0.46 versus a bandwidth ratio of 0.44 *(my calculation)*. Decoding really does scale with GB/s.

For comparison with the reference rig: one R9700 has about 640 GB/s *(unverified — from memory, check the AMD specification)*. That is M5 Max-class bandwidth, only multiplied by four cards — and with the difference that the cards have separate memory pools.

### 1.5 Prefill is different from decoding

Decoding is memory-bound; **prefill** (reading the prompt) is compute-bound. On the M5 Apple added a "Neural Accelerator" in every GPU core (according to Apple about 4× higher peak AI compute than the M4) *(company's own claim / third-party source)* — this helps prefill and time to first token, **not** decoding, because bandwidth grows separately. MLX has a dedicated path for this (§2.4).

---

## 2. MLX — the array framework

**Layer:** a numerical computing library (like NumPy + PyTorch in one), not an LLM engine. mlx-lm, oMLX, exo, vllm-metal, the MLX engine in LM Studio and the MLX runner in Ollama all stand on top of it.

> ⚠️ **MLX has no HIP/ROCm backend.** I checked the list of directories in `mlx/backend/`: there are `metal`, `cuda`, `cpu`, `common` — no `hip`. MLX **will not run on the R9700 cards**. On Linux you can have MLX on CPU or on CUDA (`pip install mlx[cuda]`), but that is not your platform.

### 2.1 Identity

- Repository `ml-explore/mlx`, **MIT** license, C++ with Python, Swift and C bindings; created 2023-11-28; **28,845 stars**, 2,353 forks; latest release **v0.32.4 (2026-10-14)**. Related repositories: `mlx-swift`, `mlx-swift-lm`, `mlx-c`, `mlx-lm`.
- Maintainer: "Apple machine learning research". The citation in the README lists four authors: Awni Hannun, Jagrit Digani, Angelos Katharopoulos, Ronan Collobert.

### 2.2 Ideas

- **Lazy arrays (*lazy evaluation*).** An operation on an array does not compute the result — it builds a graph node. The computation happens only at `mx.eval` (or when you need something, e.g. a printout). Thanks to this the framework sees a larger piece of the graph and can optimize it.
- **Unified memory.** Arrays live in shared memory, so the same array can be an argument of an operation on the CPU and on the GPU **without copying**.
- **Dynamic graph construction.** Changing shapes does not trigger slow recompilation (README).
- **Function transformations:** `grad`, `vmap`, `compile` (file `compile.cpp` — graph fusion, a "shapeless compile" option), exporting a function graph to a file for a C++ consumer (`export.cpp`).
- **Streams** (`scheduler.cpp`) and fast operations `mx.fast`: `rms_norm`, `layer_norm`, `rope`, `scaled_dot_product_attention`, plus **custom user kernels**: `metal_kernel`, `cuda_kernel`, `precompiled_cuda_kernel`. The model code in mlx-lm calls exactly these operations.

### 2.3 Code size and layout (clone from 2026-10-19)

| Directory | Lines | What is there |
|---|---:|---|
| `mlx/` in total | 155,825 (633 files) | core |
| `mlx/backend/metal` | 61,486 | `.metal` kernels ("steel" attention, "steel" GEMM, quantized, `gather_mm`, Hadamard, `gated_delta_update` for Qwen3.5-style linear attention, FFT) |
| `mlx/backend/cuda` | 30,830 | cuBLAS/cuDNN/CUTLASS, `.cu` kernels; `MLX_CUDA_ARCHITECTURES` defaults to native |
| `mlx/backend/cpu` | 13,410 | |
| `mlx/distributed` | 8,091 | `jaccl` 4,958, `ring` 879, `mpi` 579, `nccl` 506 |
| `python/src` | 17,432 | bindings |

Quantization in the core: affine group quantization (2–8 bits, groups of 32/64/128) and the MXFP4 / NVFP4 / MXFP8 modes (`mx.quantize(..., mode=...)`).

### 2.4 The "NAX" path (M5)

`is_nax_available()` in `mlx/backend/metal/device.cpp:978` requires macOS ≥ 26.2 and a sufficiently new GPU generation. There are separate kernels for it: `steel_gemm_fused_nax`, `fp_quantized_nax`, `gated_delta_update_nax`. This is the part of MLX that uses the Neural Accelerator from §1.5.

### 2.5 Distributed backends

From `docs/src/usage/distributed.rst`:

| Backend | Description from the documentation | Notes |
|---|---|---|
| `mpi` | "full featured and mature" | |
| `ring` | all-reduce and all-gather over TCP; "usually faster than MPI" | |
| **`jaccl`** | "Low latency communication with RDMA over thunderbolt. Necessary for things like tensor parallelism" | name = "Jack and Angelos' Collective Communication Library"; **fully-connected mesh topology only**; RDMA is enabled from Recovery mode with the command `rdma_ctl enable`; requires macOS ≥ 26.2 and Thunderbolt 5 |
| `nccl` | for the CUDA backend | |

API: `mx.distributed.init()`, `all_sum`, `all_gather`, `send`/`recv`; with a group of size 1 the operations are no-op calls; helper `mlx.launch`. The JACCL documentation thanks Jack Beasley, who "led the development of RDMA over Thunderbolt at Apple".

**Practical consequence:** a full mesh means that 4 machines require **6 cables** (n(n−1)/2), and every additional machine adds a cable to each previous one. This is a real constraint on designing a Mac cluster (come back to it in §7).

### 2.6 Numbers from Apple (with a caveat)

The Apple ML Research post of 2026-10-15 "Local and Distributed Large LLM Inference with MLX and RDMA on Mac Studio" gives, according to my source, among other things: 4× M5 Ultra over Thunderbolt 5/JACCL, tensor parallelism, the model "Muse Spark Open" (816B total / 42B active, NVFP4) — **36.73 tok/s** at 65,536 context, TTFT 4.8 s; two cables per link reduce TTFT from about 50.5 s to 40.6 s; peak power draw of about 300 W (M5 Ultra) versus about 200 W (M3 Ultra); dense models scale across machines better than MoE *(company's own claim)*.

⚠️ **Caveat:** the notes contain only a summary of that page made by a smaller model; I did not read the raw text of the post. The model names and parameters are credible, but **verify them at the source before you cite them**.

### 2.7 Who is behind it

MLX is a first-party Apple project: employed engineers are paid to work on it, the license is MIT, there is no foundation. Awni Hannun (most commits: 718), according to their own GitHub profile, now works at Anthropic and "co-created MLX at Apple"; their last commits to mlx and mlx-lm date from February 2026. The project survived the founder's departure: engineers with "Apple" in their profile are active (zcbenz — 304 commits, angeloskath — 235, jagrit06 — 58). As far as I verified, Apple has not shipped its own *product* built on MLX *(unverified)*. The full picture: [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

> **Check it yourself #1 — does MLX have an AMD backend?**
> ```bash
> gh api repos/ml-explore/mlx/contents/mlx/backend --jq '.[].name'
> ```
> You should see `common`, `cpu`, `cuda`, `metal` (and possibly helper directories) — **without** `hip`/`rocm`. *(I did not run the exact form of this command; I read the list of directories from the clone.)*

---

## 3. mlx-lm — the LLM layer

**Layer:** a library and command-line tools for language models on MLX: a model zoo, a converter and quantizers, generation, LoRA, a simple HTTP server.

### 3.1 Identity

Repository `ml-explore/mlx-lm`, MIT, Python; created 2025-03-11 (split out of `mlx-examples`); **7,405 stars**, 1,136 forks; latest **v0.32.2 (2026-10-16)** — three releases in two days. Largest contributions: awni 291 commits, angeloskath 63, Goekdeniz-Guelmez 56, mzbac 38, kernelpool 33, ivanfioravanti 26… The repository has `CLAUDE.md` and `AGENTS.md` files.

Size (clone): `mlx_lm/` is about 59.6K lines of Python; `models/` — 43.2K lines in **137 files**. Largest files: `generate.py` 2,184, `server.py` 2,094, `models/cache.py` 1,741.

### 3.2 The model zoo

137 architecture files: the llama, qwen3 / 3.5 / 3.8 families (including `qwen3_next`, `gated_delta`), deepseek v2 / v3 / v3.2 / **v4.1**, glm4 and `glm_moe_dsa`, kimi (k25, k3, linear), gpt_oss, gemma 3 / 3n / 4, mistral3/4, minimax, nemotron_h, mamba / mamba2 / rwkv7 / jamba (SSMs and hybrids), bitnet and many others. This gives mlx-lm the **widest "day zero" model coverage on a Mac**.

### 3.3 KV cache classes (`models/cache.py`)

| Class | What for |
|---|---|
| `KVCache`, `ConcatenateKVCache` | plain cache |
| `RotatingKVCache` | sliding window |
| `QuantizedKVCache` | `--kv-bits`, `--kv-group-size`, `--quantized-kv-start` (default 5000) |
| `ArraysCache` | SSM / linear-attention state |
| `ChunkedKVCache`, `CacheList` | chunking, lists of caches |
| `BatchKVCache`, `BatchRotatingKVCache` | batching |
| `PromptTrie`, **`LRUPromptCache`** | reuse of the prompt prefix in the server |

The prompt cache can be saved to disk and loaded back (`save_prompt_cache` / `load_prompt_cache`, safetensors; `mlx_lm.cache_prompt` uses this). **The server, however, has only an LRU in RAM** — there is no SSD tier; oMLX is what adds it (§4).

### 3.4 Generation

`generate.py`: `generate_step`, `speculative_generate_step` (speculative decoding with a helper model — server flags `--draft-model`, `--num-draft-tokens`, default 3), `stream_generate`, **`BatchGenerator`** with `PromptProcessingBatch` / `GenerationBatch` (continuous batching, stop automata), `batch_generate`. There is **no** MTP in `generate.py`; MTP heads appear only inside some model files (e.g. `deepseek_v41`, `kimi_k3`, `mimo`).

### 3.5 The `mlx_lm.server` server

- Endpoints: `/v1/completions`, `/v1/chat/completions`, `/v1/models`, `/health`. **No Anthropic endpoint, no embeddings.**
- Flags: `--decode-concurrency`, `--prompt-concurrency`, `--prefill-step-size`, `--prompt-cache-size`, `--prompt-cache-bytes`, `--kv-bits`, `--draft-model`, `--pipeline` (pipeline across machines), `--chat-template-args`.
- Documentation (`SERVER.md`): "not recommended for production as it only implements basic security checks"; **a quantized KV cache disables batching** (requests are handled one at a time when you set `--kv-bits`).
- Tool-call parsers in `tool_parsers/` (qwen3_coder, glm47, kimi_k2/k3, mistral, minimax_m2, gemma4, pythonic…).

### 3.6 Quantization

`mlx_lm.convert -q`: affine quantization (default 4 bits, group 64), `--q-mode {affine, mxfp4, nvfp4, mxfp8}`; learned methods in `quant/`: **DWQ** (distillation — tunes scales and biases against an unquantized teacher), **AWQ**, **GPTQ**, **dynamic quantization** (per-layer sensitivity → mixed bits). They are documented in `LEARNED_QUANTS.md`. On top of that: `mlx_lm.lora`/`fuse`, `gguf.py` export, `evaluate`, `perplexity`, `benchmark`.

Compare with chapter 03: DWQ/AWQ/GPTQ are "quantization with learning", imatrix in llama.cpp is "quantization with error weighting" — related ideas, incompatible formats.

### 3.7 mlx-community

The de facto hub of converted models on Hugging Face: according to the API on 2026-10-19 **5,753 models, 5,963 members, 17,847 followers**, `isVerified: false`. It is an open community organization, **not** an Apple organization. Who administers it, I could not establish *(unverified)*.

### 3.8 Assessment

Pros: the widest model coverage, the reference for quantization formats on the Mac. Cons: a basic server (no Anthropic endpoint, authentication, or multi-model manager); a quantized KV does not play well with batching; no KV paging and no SSD tier.

---

## 4. oMLX in depth

**Layer:** an inference server in Python/FastAPI on top of mlx-lm and mlx-vlm, Apple Silicon only: continuous batching, a **paged KV cache with a hot (RAM) and a cold (SSD) tier**, multi-model management, an admin panel, a native SwiftUI menu-bar app, its own quantizer (oQ), speculative decoding.

### 4.1 Identity

- `jundot/omlx`, **Apache-2.0**; Python 3.11–3.13 plus a Swift app, a JS panel and Metal/C++ kernels. Created **2026-02-13**; latest **v0.7.1rc1 (2026-10-15)**, weekly releases (more than 100 releases in 8 months); **3,353 commits**; **22,936 stars**, 2,171 forks; about 594 open issues and PRs.
- macOS ≥ 15 (Sequoia), Apple Silicon only. Distribution: `.dmg` (builds for macOS 15 and for 26/27), Homebrew tap `jundot/omlx`, pip wheels (universal2), source.
- Origin: "oMLX started from vllm-mlx v0.1.0 and evolved significantly" (README; vllm-mlx = `waybarrios/vllm-mlx`, 1,626 stars).

### 4.2 Why it was created

A quote from the README: the author did not want to choose between convenience and control — they wanted to permanently pin everyday models in memory, automatically swap in heavier ones on demand, set context limits, all from the menu bar, and keep the KV cache "in a hot tier in memory and a cold tier on SSD", so that local LLMs are practical for work with tools such as Claude Code. In other words: **the Mac of a power user who runs coding agents**. Not: Linux, CUDA, AMD.

### 4.3 Features

- **Models:** LLMs (whatever mlx-lm will load), VLMs (mlx-vlm: Qwen3.5/3.6/3.8, GLM-4V, Pixtral…), OCR (DeepSeek-OCR, DOTS-OCR, GLM-OCR), embeddings (BERT, BGE-M3, ModernBERT, EmbeddingGemma), rerankers, "decision" models, STT/TTS/STS engines.
- **API:** `/v1/chat/completions`, `/v1/completions`, **`/v1/messages` (Anthropic)**, `/v1/embeddings`, `/v1/rerank`, `/v1/systemone`, `/v1/models`, vLLM-style `/tokenize`, `/detokenize`; llama.cpp-style prefill progress (`return_progress`); tool calls recognized automatically (Qwen/Llama JSON, Qwen3.5 XML, Gemma, GLM, MiniMax, Mistral, Kimi, Longcat); an MCP client (`mcp.json`); grammar-constrained output (`omlx[grammar]`); built-in web search (optional). Tuning for Claude Code: the server reports the real context window (so that auto-compact works) and sends SSE keep-alives during a long prefill.
- **Management:** LRU eviction of models, manual loading/unloading, **pinning**, **per-model TTL**, `ProcessMemoryEnforcer` (default limit = system RAM − 8 GB), per-model settings and "profiles" exposed as `model:profile` identifiers, downloads from HF, one-click integrations (OpenClaw, OpenCode, Codex, Hermes Agent, Copilot, Pi, Mistral Vibe), a benchmark tool. **An API key is required for every binding other than loopback.**
- **External engine:** it serves some Qwen checkpoints through **Splash** (`incoai/splash`, a separate Metal engine under Apache-2.0, 1,557 stars) in a separate process.

### 4.4 Architecture (verified in the code)

```
 HTTP request (OpenAI / Anthropic / embeddings / rerank)
        │
        ▼
  FastAPI server ──► EnginePool
                       ├─ BatchedEngine   (LLM)
                       ├─ VLMEngine
                       ├─ EmbeddingEngine / RerankerEngine / DecisionEngine
                       ▼
              ProcessMemoryEnforcer  (RAM limit; LRU / TTL / pin)
                       ▼
                  Scheduler  (FCFS, configurable concurrency)
                       ▼
        mlx-lm BatchGenerator  ◄──── tokens: continuous batching
                       ▼
        ┌─────────────── cache stack ──────────────┐
        │ PagedCacheManager  (blocks, copy-on-write,│
        │                     prefix sharing)
        │ hot cache  (RAM, write-back)             │
        │ PagedSSDCacheManager (SSD, safetensors blocks)
        └───────────────────────────────────────────┘
```

**Scheduler** (`omlx/scheduler.py`, 16,621 lines; class `Scheduler` from line 2105; `add_request` ~10667, `_schedule_waiting` ~12592, `_process_batch_responses` ~13439, `step()` ~15061): it copies the "waiting/running" design from vLLM, but **leaves the delegation of token-level batching to mlx-lm's `BatchGenerator`** ("the key insight is that mlx-lm's BatchGenerator already implements…"). It adds: request admission estimates, chunked prefill plans, interrupt handling, reasoning-aware stop-sequence matching, boundary snapshots for hybrid caches (SSM/GDN), and MTP decoding for VLMs, which **bypasses** `BatchGenerator` for eligible requests.

**Cache** (`omlx/cache/` ≈ 20K lines): `prefix_cache.py` 5,783; `paged_ssd_cache.py` 5,639 (asynchronous writes with a queue of pending writes in RAM bounded to 10%/30% of host RAM; subdirectories sharded by hash; LRU size management; **a scan at startup that reuses existing files — the cache survives a restart**); `boundary_snapshot_store.py`, `type_handlers.py`, `vision_feature_cache.py`. The default SSD cache limit `auto` = 50% (free space + existing cache files).

### 4.5 Diagram: three cache tiers

The "paging" idea is borrowed from vLLM: the KV does not sit in one contiguous buffer per sequence but in **blocks** that can be shared between requests with a common prefix and copied only on write (*copy-on-write*). oMLX adds a **hierarchy of storage media** on top of this:

```
  new request (prompt = [system][agent history][new message])
        │  hash of prefix blocks
        ▼
 ┌──────────────────────────────────────────────────────────────┐
 │ Tier 1: blocks in GPU/unified memory (PagedCacheManager)
 │   - fastest access, prefix sharing, COW                      │
 └──────────────┬───────────────────────────────▲───────────────┘
          hit   │                       eviction│ (LRU, RAM pressure)
        ▼        │                               │ write-back
 ┌──────────────────────────────────────────────────────────────┐
 │ Tier 2: "hot" cache in RAM (write-back)                      │
 │   - queue of pending writes: ≤ 10% / 30% of host RAM        │
 └──────────────┬───────────────────────────────▲───────────────┘
          hit   │                       asynchronous write
        ▼        │                               │
 ┌──────────────────────────────────────────────────────────────┐
 │ Tier 3: "cold" cache on SSD (PagedSSDCacheManager)           │
 │   - blocks in safetensors format, compatible with mlx-lm    │
 │   - hash-sharded subdirectories, LRU eviction               │
 │   - default limit "auto" = 50% (free disk + old cache)       │
 │   - scan at startup ⇒ prefixes SURVIVE a server restart      │
 └──────────────────────────────────────────────────────────────┘
        │  miss on every tier
        ▼
   prefill only for the missing suffix → new blocks go down the hierarchy
```

*The diagram is my synthesis of the README description and the code in `omlx/cache/`; the class names and numbers (10%/30%, 50%) come from the notes, and the arrangement of arrows simplifies the code.*

**Why does this matter for an agent?** A coding agent sends the whole growing history at every step. Without prefix reuse, every step means prefill from scratch — and prefill of a long history costs a fair amount of time on a Mac (at 65K tokens of context Apple gives a TTFT on the order of several seconds on a 4× M5 Ultra cluster, §2.6). With the SSD cache, prefill covers only the new tail, even after the server is shut down or after the model has been evicted from memory.

### 4.6 KV compression, kernels and patches

- **Optional KV compression:** Affine4 / Affine8 (`docs/affine4.md`) with attention decoding on Metal TensorOps; the repository also has `turboquant_kv.py`.
- **Custom native kernels** (`omlx/custom_kernels/{attention, quant_matmul(+ane), lowbit, sparse_index, moe_staging}`, built with the Metal toolchain from Xcode; the DMG ships them precompiled). README: GLM-5.2, MiniMax M3 and Qwen3.5 *require* these kernels; "fused DSA prefill is roughly 30x faster with the kernels (measured 845 vs ~29 tok/s on an M3 Ultra)" *(project's own claim)*.
- **About 90 patches** in `omlx/patches/` — monkey-patches of layers over mlx-lm/mlx-vlm (Qwen3.5 GDN/MoE, DeepSeek V4/V4.1, GLM-DSA, MiniMax M3, Muse Spark, MiMo V2, "ragged decode", verification kernels…). This is a "day zero" support strategy through vendoring and patching — **similar in spirit to ds4, but on top of a universal library**.
- **MoE expert offloading** (`docs/experimental/MoE_Expert_Offload.md`): you keep a fraction (5–95%) of each layer's experts in a cache slot and stream the rest from the original safetensors through `pread` (12 threads, ≤ 48 reads in flight). Results are "bit-identical"; for gemma-4-26b-a4b 4-bit the peak memory at load drops from 14.28 GB to 4.69 GB with 25% resident *(project's own claim)*. It is the same idea as SSD streaming in ds4 (§5.6), but on the mlx-lm path.

### 4.7 Speculative decoding (MTP, DFlash)

- **"Lightning MTP"** — native MTP (*multi-token prediction*) heads, with verification kernels borrowed from MTPLX.
- **DFlash** — *block-diffusion*-style block drafting (arXiv:2602.06036): a draft model proposes a whole **block** of tokens based on hidden states collected from several layers of the target model; adaptive verification depth; mutually exclusive with MTP and with expert offloading; for most families one row, for Qwen3.5–3.8 and GLM-5.3 — many rows in parallel.
- **SpecPrefill** (`omlx/specprefill`).

This is the same direction you know from `../speeding-up-generation/README.md`: check several tokens at once, because the cost of a step is reading the weights.

### 4.8 Experiments

- **Prefill on two ANEs + GPU** for Qwen3.5/3.6/3.8 on the M3 Ultra through the **private AppleNeuralEngine API**: two ANE instances compute INT8 chunks of the MLP gates, the GPU does the rest; the recurrent state stays on the GPU for precision; disabled by default (`docs/experimental/qwen35_ane_prefill.md`).
- **A cluster of multiple Macs** — a pipeline by ranks over Ring or JACCL/RDMA with a panel (`omlx/cluster`).

### 4.9 oQ — its own quantizer and what "oQ4e" means

`omlx/oq.py` (11,295 lines), `docs/oQ_Quantization.md`. The author's description: "mixed-precision quantization combining GGUF K-quant layer-position strategy, unsloth Dynamic 2.0 selective non-quantization, and BnB MSE-optimal clipping". Levels: **oQ2, 2.5, 2.7, 3, 3.5, 4, 5, 6, 8**; approximate bits per weight including scales (group 64): oQ4 ≈ 4.6–4.7; oQ3 ≈ 3.5–3.7; oQ2 ≈ 2.8–3.0; oQ8 ≈ 8.5.

Procedure:

1. Stream the tensors from disk.
2. **Measure the sensitivity of each layer** on built-in calibration (600 multilingual / code / tool-call samples; 128 × 256 tokens).
3. Plan extra bits for the sensitive tensors within a size budget.
4. **The "e" variant (*enhanced*, e.g. "oQ4e")**: additionally collect an **imatrix** (about 2,700 samples; 128 × 512 tokens; for MoE sample up to 1,024 sequences, until every expert gets enough tokens) and round each group by searching for the scale/offset that give the minimum *importance-weighted* error, plus a weighted least-squares fit.
5. Save **standard MLX safetensors** — the result is loaded by plain mlx-lm/mlx-vlm.

**So "oQ4e" = oQ level 4 (4-bit base) with improved imatrix-driven rounding**, e.g. `Qwen3.5-122B-A10B-oQ4e`. The suffix `-mtp` = MTP heads preserved; `-fp16` = scales in float16. Protection: embeddings and the output head in 8 bits, MoE routers in full precision, shared-expert gates in 8 bits, vision/audio encoders, norms and SSM parameters left unquantized. Models already quantized in MLX **cannot** be a source. DeepSeek V4.1 is supported at the oQ3/oQ4(e) levels, including with a 4-bit Engram.

Quality (the project's own measurements, *project's own claim*): Qwen3.5-9B (1,900 questions from MMLU/Winogrande/MBPP/GSM8K) — original 76.53, oQ4e 77.05 (5.6 GB), oQ3e 73.79 (4.6 GB); Qwen3.6-35B-A3B — original 82.68, oQ4e 83.05 (20 GB), oQ3e 82.68 (16 GB). An earlier table (1,600 questions): uniform 4-bit from mlx-lm 70.12 vs oQ4e 72.38 on Qwen3.5-9B. These are the author's measurements, without independent replication; remember that with 1.9K questions, differences on the order of 0.5 points fall within noise.

Kinship with llama.cpp: "measure sensitivity, then distribute the bit budget" is the same idea as imatrix + `--tensor-type` in llama.cpp — you can reproduce it on the rig (chapter 03).

### 4.10 Comparison with neighbors

| | oMLX | `mlx_lm.server` | MLX engine in LM Studio | Ollama (Mac) | llama.cpp (Metal) | vllm-metal |
|---|---|---|---|---|---|---|
| Foundation | mlx-lm BatchGenerator + own paged/SSD cache | own | `lmstudio-ai/mlx-engine` (MIT, 1,189 stars) wrapping mlx-lm/mlx-vlm | Go `mlxrunner/` (about 55K lines) on mlx-c | ggml Metal | vLLM scheduler + block manager; mlx_lm layers |
| Continuous batching | yes | yes (basic) | depends on the app | via `batch/` in mlxrunner *(unverified depth)* | yes (slots) | yes |
| SSD tier for KV | **yes** | no (LRU in RAM) | no | no *(unverified)* | slot save to disk (`/slots`) | no *(unverified)* |
| Anthropic API | yes | no | no *(unverified)* | yes (`anthropic/` directory) | yes | no *(unverified)* |
| UI | web panel + menu bar | none | full app | tray icon | web UI | none |

Others building on MLX: `vllm-project/vllm-metal` (Apache-2.0, 1,890 stars, created 2025-12-12), `waybarrios/vllm-mlx` (the ancestor of oMLX), `ddalcu/mlx-serve` (1,990; Zig + a Swift app), `youssofal/mtplx` (2,605; native MTP on the Mac — "125 tok/s in OpenCode on an M5 Max" *(project's own claim)*), `bstnxbt/dflash-mlx`, `Blaizzy/mlx-vlm` (5,639), `incoai/splash`.

### 4.11 Offline

The admin panel has all CDN dependencies vendored ("fully offline"). Downloads from HF and updates are optional (`--hf-endpoint` lets you use a mirror); the DMG has an in-app auto-update, which — I assume — can be turned off *(unverified)*.

### 4.12 Who is behind it

**Jun Kim (jundot)**, Seoul. According to the GitHub profile: "Open-Source ML Engineer at Hugging Face | Creator of oMLX"; they are also a public member of the `huggingface` organization. Of the 3,353 commits, 2,110 are theirs (about 63%). On the omlx.ai site and in the repository there is **no information about sponsors, pricing or donations** (no `FUNDING.yml`); the license is Apache-2.0, with no paid version. **Whether Hugging Face funds or sponsors oMLX, I could not establish** *(unverified)*; the fact that the author is employed at HF is the only thing that is verified. Details: [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

### 4.13 Assessment

+ The only verified Mac server combining: a persistent KV cache on SSD, pinning and TTL for multiple models, OpenAI and Anthropic APIs, a quantizer and a GUI. It moves fast.
− A single maintainer (63% of commits), a large surface of patches over two upstreams, `scheduler.py` at 16.6K lines; reliance on private and experimental paths (the private ANE API; custom kernels requiring a full Xcode); macOS only; no declared funding model.

> **Check it yourself #2 — the oMLX scheduler.** In the `omlx` clone:
> ```bash
> wc -l omlx/scheduler.py omlx/oq.py omlx/cache/paged_ssd_cache.py
> grep -n "BatchGenerator" omlx/scheduler.py | head
> grep -n "def step" omlx/scheduler.py
> ```
> You should see 16,621 / 11,295 / 5,639 lines and that the scheduler calls mlx-lm's `BatchGenerator` instead of assembling a token batch itself. *(Commands reconstructed from the names in the notes.)*

---

## 5. ds4 / DwarfStar in depth

**Layer:** a small, native inference engine in C (Metal as the main backend, plus CUDA and ROCm) that runs a **handful** of very large MoE models from **its own** GGUF files, with its own HTTP server (OpenAI, Responses, Anthropic), its own coding agent, a persistent KV cache on disk, expert streaming from SSD, speculative decoding and tensor-parallel splitting across two machines.

### 5.0 A correction to the name

The name "ds4" is now historical. The README says today: "**DwarfStar** aims to be the best way to run a few excellent large language models on consumer hardware", while the binaries are still called `ds4`, `ds4-server`, `ds4-agent`, `ds4-bench`, `ds4-eval`. Supported models: DeepSeek V4 Flash (including "experimental vision"), DeepSeek V4.1 Flash, DeepSeek V4 PRO, **GLM 5.2 / 5.3 / 5.3 Flash**, **Qwen3.8 Flash Next**. So the engine is still "deliberately narrow, not a general GGUF loader", but it is already "a few models", not one.

⚠️ **A contradiction in the repository:** the `AGENT.md` file still claims that "ds4.c is a DeepSeek V4 Flash specific inference engine", which is out of date relative to the README and `docs/MODELS.md`. In case of a discrepancy, trust the README.

### 5.1 Identity

- `antirez/ds4`, **MIT** license. The `LICENSE` file has three copyright lines: "The ds4.c authors", "The ggml authors" (2023–2026) and "DeepSeek" (2023). Part of the GGUF quantization tables, the CPU logic and the kernels are adapted from llama.cpp/GGML (MIT) — README, the "Acknowledgements" section. The repo also has `licenses/Apache-2.0.txt` (an external fragment; I could not establish which).
- Created **2026-05-06**; last commit **2026-10-19**; **827 commits** in about 5.4 months. **No releases or tags** (README: "very fast changing… beta quality").
- **23,955 stars**, 2,314 forks, 793 open issues and PRs. Byte breakdown: C 9.07 MB, CUDA 4.89 MB, Objective-C 2.34 MB, Metal 1.37 MB, Python 1.0 MB, C++ 0.5 MB.
- Commits: antirez 523, kyuz0 33, ivanfioravanti 28, polymorf 23, Entrpi 15, jyatesdotdev 11, mitsuhiko 7. So about 63% is the author; the rest is a real, but small, tail.
- Documentation in the repo: `README.md` and `docs/*.md` (MODELS, SERVER, CLIENTS, SSD_STREAMING, DISTRIBUTED, SPECULATIVE_DECODING, PERFORMANCE, TESTING, METAL, DGX_SPARK, STRIX_HALO, CUDA_MULTI_GPU, QWEN38_FLASH_NEXT) and the 147-kilobyte `QA_BEFORE_RELEASES.md` — a QA runbook with measurements.
- An unusual declaration from the README: the project is built "with **strong assistance from AI coding agents** and with humans leading the ideas, testing, and debugging", and the philosophy says that software should be delivered as a "working template" that the user adapts with their own coding agents.

### 5.2 The engineering argument: why an engine for just one model

llama.cpp is universal: it loads many architectures from one format, builds a compute graph from an architecture description in `src/llama-model.cpp`, plans it through `ggml_backend_sched` and sends it to generic kernels. For this universality you pay in layers of abstraction: a generic graph, a generic allocator, kernels written "for every shape", chat templates assembled from Jinja, and so on.

ds4 goes the other way. **The graph is hard-coded for an architecture family** (`DS4_N_LAYER`, `DS4_N_HC`, the indexer's top-k, KDA linear attention for GLM 5.3, n-gram/PLE tables for Qwen…), and validation "accepts the known Flash and Pro layouts and fails early with an error for anything else" (the header comment in `ds4.c`). Consequences follow from this:

1. **A whole-model plan on Metal.** Instead of sending individual operations from a generic intermediate representation, the engine plans the entire model pass at the command-buffer level.
2. **Fusions for DeepSeek's exotic elements** (compressed KV with an indexer, hyper-connections with constraints, etc.) — the kernels can assume fixed shapes.
3. **An exact tokenizer, chat and tool templates** — "DSML blocks" for DeepSeek, custom templates for GLM — instead of a generic template engine.
4. **Tests against DeepSeek's official logprob vectors** (`ds4_test --logprob-vectors`, `CONTRIBUTING.md`): quality measured against the model vendor's reference, not against other engines.

The price: **every new architecture is a port of thousands of lines** (e.g. `metal/qwen4.metal` has 4,733 lines), and a model "may be removed when a better replacement appears" (README: support is "intentionally opportunistic"). This is not a long-lived platform; it is a fast-changing lab of a single author who tracks the currently best large MoE.

An analogy: llama.cpp is a universal workshop with a full set of wrenches; ds4 is the tooling for one engine in a factory — faster for that one engine, useless for another. To be precise: **the project does not document that it is faster than general-purpose engines** (see §5.12) — this is a design argument, not a measurement result.

### 5.3 File layout and sizes (clone from 2026-10-19)

| File / directory | Lines | Role |
|---|---:|---|
| `ds4.c` | 87,535 | the "vertical" file: GGUF loading, fixed tensor layouts, tokenizer, reference CPU kernels, **whole-model graph drivers**, sessions, disk-cache payloads |
| `ds4_metal.m` + `metal/*.metal` | 50,537 + 32,833 | Metal backend; largest: `moe.metal` 9,591, `dsv4_misc.metal` 7,110, `qwen4.metal` 4,733, `dense.metal` 2,933, `flash_attn.metal` 1,692 |
| `ds4_cuda.cu` + `cuda/mmq/*` | 36,309 + 37,498 | CUDA backend; MMQ/MMVQ kernels adapted from ggml-cuda |
| `rocm/*.cuh` + `ds4_rocm*.cu` | 32,248 | ROCm backend |
| `ds4_server.c` | 23,115 | HTTP server |
| `ds4_agent.c` | 13,635 | coding agent |
| `ds4_distributed.c`, `ds4_tp.c` | 8,437, 3,944 | splitting across machines |
| `ds4_kvstore.c` | 1,352 | on-disk KV store |
| `ds4_engram.c` | 473 | Engram tables (V4.1) |
| `tests/`, `gguf-tools/` | 76,802, about 20K | tests; converters/quantizers (`deepseek4-quantize.c`, `deepseek41_quantize.py`, `glm53_quantize.py`) |

In total the top-level C/H/M/CU/CUH files add up to about **249,625 lines**. This is an **enormous "small" engine**: the "one simple C file" aesthetic did not survive growth to many models and backends, although `AGENT.md` still demands "small, readable… Do not introduce C++" (C++ appears only in the CUDA/ROCm kernel files).

**Loading:** `mmap`-based; the loader parses only the GGUF header, metadata and tensor catalog; on Metal, slices of the mapping are wrapped as `MTLBuffer` buffers without copying. A process-level lock makes it impossible to start two huge models at once.

### 5.4 Quantization layout

Ds4 **does not invent a new format** — it uses llama.cpp/GGML types, but in an **asymmetric** layout: the compression target is the **routed experts**, and the rest stays in high precision.

- Routed experts: `IQ2_XXS` for gate/up + `Q2_K` for down (calibrated with imatrix).
- "Q8 projections, shared experts and output, plus F16/F32 tensors" stay in high precision.
- Other variants: `Q4_K` and **native MXFP4** for DeepSeek's experts (it keeps DeepSeek's original FP4 experts without requantization; Blackwell uses native FP4 matrix instructions).
- DeepSeek V4 Flash in Q2 is a file of about **81 GiB** at 284 billion parameters ⇒ on average about 2.45 bits per weight *(my calculation: 81 GiB × 8 / 284·10⁹)*.
- The DeepSeek V4 models support a 1M-token context (Flash 284B total / 13B active; PRO 1.6T / 49B active) — `MODEL_CARD.md`. The practical context is limited by the KV allocation (`--ctx`).
- Files are published on Hugging Face under `antirez/*` (`deepseek-v4-gguf`, `deepseek-v4.1-flash-gguf`, `glm-5.3-flash-gguf`, `glm-5.3-gguf`, `GLM-5.2-GGUF`, `qwen3.8-flash-next-gguf`) and `unsloth/GLM-5.2-GGUF` and `ggml-org/Qwen3.8-Flash-Next-GGUF` (mmproj) — `download_model.sh`, lines 4–11.

**An exercise for you:** the recipe "2-bit routed experts, Q8 for the rest, imatrix only on the experts" is reproducible in llama.cpp through tensor type overrides (`--tensor-type` / a custom GGUF) for any large MoE (chapter 03). Your UD-IQ3_XXS file from Unsloth is the same philosophy (dynamic, non-uniform quantization), just with different levels.

### 5.5 Why the KV in DeepSeek V4 is so small

Facts that the engine encodes (`MODEL_CARD.md`; consistent with the sizes from kvstore): 43 layers; in every layer a raw sliding window of 128 tokens; layers 0–1 raw only; even layers ≥ 2 use **compressed KV at ratio 4** plus an **indexer** (64 heads × 128 dimensions, **top-k 512** compressed rows); odd layers ≥ 3 use ratio 128; on top of that manifold-constrained hyper-connections (mHC) and MoE with shared + routed experts.

The effect: the measurement file `speed-bench/m5_max.csv` (column `kvcache_bytes`) records a **KV snapshot of 52.2 MB at 2,048 tokens and 475 MB at 32,768 tokens, i.e. about 14.5 KB per token**. This is the reason a 1M context is even imaginable and why **saving the KV to disk** (§5.7) pays off: the snapshot is small.

DeepSeek V4.1 adds **Engram** tables (row embeddings hashed by n-grams; 189 GiB of FP8 rows with scales in the Q2 file), which are **never loaded into RAM** — they are read through `pread` on demand with a separate, non-cached descriptor and bounded temporary buffers (384 KiB) (`ds4_engram.h`, `docs/MODELS.md`).

### 5.6 Streaming experts from SSD

When the model is larger than RAM (`ds4_ssd.c`, `docs/SSD_STREAMING.md`):

```
 RAM / GPU memory                       SSD (GGUF file)
 ┌──────────────────────────┐            ┌─────────────────────────┐
 │ non-routed tensors       │            │ all routed              │
 │ (attention, shared,      │            │ experts                 │
 │  output) — resident      │            └────────────▲────────────┘
 │                          │                         │ pread on a miss
 │ bounded cache of         │◄────────────────────────┘
 │ routed experts           │   (read hidden behind the compute of
 │  - start: "hotlist"      │    shared experts /
 │    from the binary       │    the previous layer)
 └──────────────────────────┘
```

- Non-routed weights stay resident (Metal tries to "pin" them in memory).
- **Routed experts live in a bounded cache; misses are read from the GGUF**, and the latency hides behind the compute of the shared experts / the previous layer. `AGENT.md`: "always try to hide loading of missing routed experts by loading them while performing the inference of the shared expert".
- The cache budget is automatic by default (`ds4_ssd_auto_cache_plan`); manually `--ssd-streaming-cache-experts 32GB` (bytes) or just a number (expert slots).
- **A precomputed hotlist**: `ds4_streaming_hotlist.inc` (192 KB; `…_glm52.inc`) is compiled into the binary (generated from profiling), so the cache starts with the experts that are probably "hot"; there is also a profiler (`ds4_expert_profile_*`).
- Measurements (M5 Max 128 GB, 2026-09-06, automatic cache; *project's own claim*): GLM 5.3 Flash Q4_K (177.77 GiB) — initial prefill 121 tok/s, decoding 11.9 → 14.9 tok/s; DeepSeek Flash Vision Exp MXFP4 (145 GiB) — prefill 300 tok/s, decoding 11.9 → 19.3 tok/s (single run; `docs/SSD_STREAMING.md`).

The intuition: an MoE activates only a handful of experts at each step, and the usage distribution is uneven, so **a small cache of hot experts is hit often**. The SSD supplies the rest. That is how a 178 GiB model runs on a machine with 128 GB of RAM at an "interactive" speed, though slower than a resident model.

### 5.7 The on-disk KV store (`ds4_kvstore.c/.h`)

This is the most "agentic" part of ds4.

- **Key = SHA-1 of the rendered text prefix** (file name = hash of the byte prefix). The payload contains the exact tokens and the graph state; a 48-byte header with `model_id`, `quant_bits`, `ctx_size` and a code for the reason of the write (COLD / CONTINUED / EVICT / SHUTDOWN / AGENT_SYSTEM / AGENT_SESSION). Eviction uses a hit counter with a **half-life of 6 hours**.
- Server flags: `--kv-disk-dir`, `--kv-disk-space-mb` (default 4096 MB), `--kv-cache-min-tokens`, `--kv-cache-cold-max-tokens`, `--kv-cache-continued-interval-tokens`, trimming and boundary alignment, `--kv-cache-reject-different-quant`.
- **Lookup order:** a live slot with a token prefix → matching text prefixes on disk → prefill of the suffix only.
- **The tool-call ID replay map (*tool-call ID replay*)**: the server remembers the exact DSML block of a tool call that was generated and reuses it, instead of re-tokenizing the JSON reformatted by the client (`--tool-memory-max-ids`). This matters because agent clients send the history back in a slightly different form — and if the tokens differed, the prefix would stop matching and the cache would miss.
- With tensor parallelism (TP), restoring a prefix must rebuild it on both ranks — there is no instant restore.

**Why a text key and not a token key?** Because the client sees text; a hash of the rendered prefix gives independence from small tokenization differences at message boundaries. I do not know whether the author justified it that way — this is my interpretation of the pattern in the code *(unverified)*.

### 5.8 Speculative decoding: DSpark and MTP

(`docs/SPECULATIVE_DECODING.md`, `ds4_deepseek41_dspark.h`, `metal_graph_dspark_*` in `ds4.c`)

- **DSpark** (DeepSeek only): a separate **"support" GGUF** (5.6 GiB for V4 Flash 0731; 8.04 GiB for V4.1) with a small drafter that consumes hidden states **collected from 3 layers of the target model** (`target[3]`, `window[3]`, a draft window of 128 positions, `DS41_DRAFT_ROWS 5`, `DS41_VERIFY_ROWS 6`) and proposes up to 5 tokens plus a **confidence head** (`--dspark-confidence`; default pruning 0.4 on a single Spark, 0.8 for exact sampling). The target model verifies in one batched pass and keeps the longest accepted prefix. For V4 it requires resident weights (it does not work with SSD streaming); for V4.1, DSpark works with streaming (the drafter stays in memory, +8 GiB). Not for PRO. Two TP hosts can split the drafter over RDMA.
- **MTP** (GLM 5.3, Qwen3.8): built into the main GGUF; GLM commits up to 2 tokens per cycle; Qwen drafts 1 ahead with an adaptive chained second one. The `--mtp` flag.
- **The sampling semantics are explicit:** the default "opportunistic" mode accepts a greedy draft only when it agrees with the greedy target token (more deterministic than true sampling); `--mtp-exact-sampling` implements the full accept/correct rule that preserves the target model's distribution.
- The documentation warns: "V4.1 DSpark can still be slower than ordinary decoding"; session batching disables MTP/DSpark (except Qwen on Metal).

Measurements (*project's own claim*, `docs/DGX_SPARK.md`; medians of 2 runs; temp 0, 64K context): two DGX Sparks over RoCE, V4 Flash 0731 Q2: **44.0 tok/s** (English prose) and **83.3 tok/s** (C code — a hash table) with DSpark, versus **26.0 tok/s** without; one Spark with DSpark: 23.4 and 44.0 tok/s.

**The lesson:** the gain from speculation depends on the **content**. Code (predictable) speeds up more than threefold, prose by about 1.7×. When you measure your own installation, measure on the prompts you actually give your agents.

### 5.9 Parallelism

From `docs/DISTRIBUTED.md` and `CUDA_MULTI_GPU.md`:

- **Tensor split across two machines** (50/50 of the routed experts, exactly one worker): coordinator/worker over **Thunderbolt RDMA on Macs** (`rdma_ctl` needed; on 128 GB machines `sudo sysctl iogpu.wired_limit_mb=120000`) or RoCEv2 on two DGX Sparks, with a TCP fallback. "No authentication or encryption"; all nodes must have the same commit.
- **Pipeline split**: whole ranges of layers on several machines (not implemented for V4.1).
- **Multiple CUDA GPUs on one host**: whole layers on a GPU (`--gpu-devices`, `--gpu-vram auto`) or `--cuda-tensor-parallel`, which pairs GPUs and splits experts within a pair; tested: 4×48 GB Q2 and 8×L40S Q4. **126 tok/s aggregate at 16 sessions on 8×L40S** (Flash Q4; *project's own claim*; the QA file also records on this hardware a prefill of 1,524.84 tok/s and 46.93 tok/s for a single stream).

For comparison with the reference rig — this is **exactly this class of configuration** (several cards, a layer layout), only in the CUDA backend, not ROCm.

### 5.10 Directional steering (*steering*)

The `dir-steering/` directory: a flat f32 matrix with one normalized direction of hidden width per layer. At run time, after the attention and/or FFN output:

```
y = y - scale * direction[layer] * dot(direction[layer], y)
```

(a negative scale amplifies the direction). File shapes: DeepSeek V4 Flash `43 × 4096`, GLM 5.3 Flash `45 × 4096`, Qwen3.8 Flash Next `48 × 2560`. `build_direction.py` builds the vector from lists of "good/bad" prompt pairs (example in the repo: concise vs verbose, 100 pairs); `/steer F` changes the scale live **without rebuilding the KV cache**. It works with MTP, the server, session batching and TP on 2 Macs for GLM 5.3; not for GLM 5.2. It is a cheap demonstration of activation editing in the interpretability style — a good educational exercise.

A separate knob: `--power N` (DeepSeek V4 only) trades throughput for a lower sustained GPU load.

### 5.11 API, tools and clients

- **Binaries:** `ds4` (CLI/REPL with linenoise), `ds4-server`, `ds4-agent` (a native coding agent without the HTTP hop, `/save`, `/switch`, sessions in `~/.ds4/kvcache`, the `view_image` tool, `/hints`), `ds4-bench` (a context-length sweep), `ds4-eval` (embedded regression suites `core`/`hard`).
- **HTTP** (`docs/SERVER.md`): `GET /v1/models`, `POST /v1/chat/completions`, `POST /v1/responses`, `POST /v1/completions`, `POST /v1/messages` (Anthropic). Tools and SSE in chat/Responses/Anthropic; reasoning is returned separately in each API's native form; `reasoning_effort=max` enables Think Max only with a sufficiently large context. Names like `deepseek-v4-flash` are "compatibility aliases, not separate loaded models" — **one model per server process**. Images (PNG/JPEG as data URIs; ≤ 16 images, 64 MiB) with the matching `--vision` encoder.
- **Recipes for clients** (`docs/CLIENTS.md`): Pi, OpenCode, Codex CLI (Responses API) and **Claude Code** (the Anthropic endpoint via `ANTHROPIC_BASE_URL`; the recipe sets `ANTHROPIC_DEFAULT_*_MODEL` and `CLAUDE_CODE_SUBAGENT_MODEL` to the local model).
- **Thinking:** on by default; `--nothink`; for V4.1 `--think-level 1..100` (0 = off); default sampling temp 1, top-p 1, min-p 0.05.
- **Multiple sessions:** `--batched-session N` preallocates N KV states; native batched decoding where supported (resident Metal V4.1: 2–8 sessions; the CUDA TP layout); **a single CUDA GPU, including the Spark = an orderly fallback, i.e. concurrency without a speedup**.
- **Security:** the server binds by default to 127.0.0.1:8000; no authentication ("put authentication and TLS in front"). The only external network call is made by `download_model.sh` (an optional HF token). I did not find telemetry or an update check in the file list, but **I did not search every source for sockets** *(unverified for the claim "exhaustively")*.

### 5.12 Performance (all figures: *project's own claim*)

Configuration: DeepSeek V4 Flash Q2 (`IQ2_XXS` gate/up + `Q2_K` down), greedy, 128 tokens per front, `ds4-bench`, text `speed-bench/promessi_sposi.txt`. Values: prefill / generation, tok/s.

| Machine | Context 2,048 | Context 32,768 | File |
|---|---|---|---|
| M5 Max 128 GB | 790.2 / 39.35 | 557.0 / 34.36 | `speed-bench/m5_max.csv` |
| M4 Max (RAM not given in the CSV name) | 343.8 / 26.76 | 247.9 / 24.52 | `m4_max.csv` |
| M2 Ultra | 410.6 / 23.22 | 325.8 / 21.92 | `m2_ultra.csv` |
| DGX Spark 128 GB (GB10) | 825.8 / 18.05 | 855.9 / 14.43 | `gb10.csv` |
| Strix Halo gfx1151 128 GB (ROCm 7.14) | prefill 231.9 at 2K ("tuned"), 292.9 at 4K (warm) | – | `speed-bench/gfx1151-prefill-results.md` |
| M3 Ultra, **PRO** Q2 (1.6T) | 183.1 / 12.42 | 138.8 / 9.56 | `pro_model_m3_ultra.csv` |

Additionally in `QA_BEFORE_RELEASES.md` (line 1491; my interpretation of the cell labels, verify it) for Strix Halo, code in 128 tokens, temp 1: plain decoding 16.26 tok/s, "opportunistic" 12.28, "exact" 13.52 — so on this prompt speculation was **slower** than plain decoding.

**What is missing:** the repository has no comparison with llama.cpp or MLX (a grep over the documentation finds "llama.cpp" only in the acknowledgements). I also did not find an external comparison *(unverified)*. So "faster than general-purpose engines" is **not documented by the project**. What is verified: quality is compared against DeepSeek's official logprob vectors, not against other engines.

**What ds4 optimizes:** single-stream latency for agentic coding on one large box, plus reuse of prefixes from disk. You get batched throughput only in the multi-GPU CUDA TP layout and on the resident Metal paths.

### 5.13 Your llama.cpp result vs the ds4 data — and why this is not an "apples to apples" comparison

Your measured result (from `../speeding-up-generation/README.md`): **23.5 → about 50 tok/s** for a single agent, llama.cpp, DeepSeek-V4-Flash in UD-IQ3_XXS, 4× R9700, tensor split + DSpark. The only ds4 data point for the R9700 (PR #558, §5.14): **one** R9700 32 GB card, V4 Flash Q2 (~81 GB) **with SSD streaming**, generation **2.30 → 4.70 tok/s**, prefill 3.67 → 6.33 tok/s.

> ⚠️ **This is not a like-for-like comparison.** The differences, each of which alone is enough to invalidate the conclusion "engine X is N times faster":

| Dimension | Your result | Data point from PR #558 |
|---|---|---|
| Engine | llama.cpp (build 0ce8cd1) | ds4 + an unmerged patch |
| Quantization | UD-IQ3_XXS (Unsloth, non-uniform) | ds4 Q2 (`IQ2_XXS` + `Q2_K`, about 2.45 bpw) |
| Cards | 4 × R9700, 128 GB VRAM in total | 1 × R9700 32 GB |
| Where the weights are | **entirely in VRAM** | mostly on SSD, streamed through the cache |
| Speculative decoding | DSpark enabled | no information in the PR |
| Rest of the platform | your host | Ryzen 9 9950X3D, 128 GB DDR5, ROCm 7.2.2, Ubuntu 26.04 |
| Source | the reference measurement | the PR author's numbers *(PR author's own data)* |

**What may be concluded from this** *(my inference)*: the roughly 10× difference between 4.7 and ~50 tok/s is most likely explained above all by **where the weights sit** — resident in 4 × 32 GB versus streamed from SSD through one card — and not by the superiority of one code base over the other. This is exactly how the claim from §1 works: when the weights have to pass through a slower medium, that medium becomes the ceiling. If ds4 had a layer layout on ROCm like the one in CUDA, it could in principle keep 81 GiB in your 128 GB of VRAM (this is a hypothesis *(unverified)*) — and only then would the comparison make sense.

The gain from speculation looks similar in both worlds: for the reference rig about 2.1× (23.5 → ~50), for the ds4 project on two Sparks 1.7× for prose and 3.2× for code (26.0 → 44.0 / 83.3). These are **not** comparable measurements (different hardware, a different model in a different quantization, different prompts), but they show the same effect: the gain depends on the content and falls within "about double".

**Practical conclusion:** for the reference rig llama.cpp is today the only real choice, because ds4 does not build on gfx1201 without patches.

### 5.14 ROCm and gfx1201 — as of 2026-10-19

- The main branch has `ROCM_ARCH ?= gfx1151` (Strix Halo). **The tuned paths are gated by `ds4_rocm_is_gfx1151()`** (e.g. `rocm/ds4_rocm_common.cuh:6-22`, `ds4_rocm_hipblaslt.cuh`, many environment switches `*_gfx1151_flag(...)`). The reference dev machine is Strix Halo (an APU with unified memory) — `QA_BEFORE_RELEASES.md`, §9.
- The ROCm backend is **single-device** in the code: `ds4_rocm_compat.cu` picks one HIP device (`hipSetDevice(g_gpu[0].device_id)`), whereas the CUDA backend has a mechanism for placing layers on multiple GPUs (`ds4_gpu_mgpu.h`, `DS4_MAX_GPUS 16`, 62 `SetDevice` call sites in `ds4_cuda.cu`). *The conclusion about single-device is my interpretation of a grep, moderate confidence.*
- **Open external work — everything unmerged as of 2026-10-19** (GitHub API):
  - issue **#521** (2026-07-08, cm999club): "gfx1201 (RDNA4, R9700) build fails: `__builtin_amdgcn_wmma_f32_16x16x16_f16_w32` not supported" — the hand-written Q8 GEMM kernel uses a gfx11-style WMMA builtin, and RDNA4 changed the signatures;
  - PR **#558** (2026-07-13): "run on discrete RDNA4 (gfx1201) — opt-in WMMA fallback + configurable VRAM reserve". The author's test on **one R9700 32 GB**, V4 Flash Q2 (~81 GB) **with SSD streaming**: prefill 3.67 → 6.33 tok/s, generation 2.30 → 4.70 tok/s after overriding the hard-coded 16 GiB reserve of free VRAM (`DS4_ROCM_FREE_RESERVE_MB=2048`, cache 26 GB) *(PR author's own data)*; the server endpoints worked;
  - PR **#599** (2026-07-24) "gate the WMMA v1 kernel" and PR **#744** (2026-08-08, bestbug456) "rdna4 gfx1201 rocwmma v2";
  - PR **#602** (ewindisch, 2026-07-24): "AMD Instinct (CDNA/gfx90a) support with multi-GPU device placement"; PR #1233 "CUDA: resident V4.1 multi-GPU layer placement, validated on Turing";
  - the umbrella issue **#16** "AMD GPU (ROCm/HIP) and especially Strix Halo".

**State:** (a) without patches it will not build on gfx1201, (b) with a patch it works on one card through SSD streaming at 2–5 tok/s, (c) a multi-card resident layer layout exists only in CUDA. It is worth watching PRs #558, #744 and #602.

### 5.15 Forks and community momentum

From the GitHub API, 2026-10-19:

| Project | Stars | What it is |
|---|---:|---|
| `notatestuser/ds4-control` | 915 | a menu-bar app in Swift (MIT) "for fast local DeepSeek V4.1, with 1M context"; a single Swift binary; ds4 as a git submodule with patches; "no embedded inference" |
| `ivanfioravanti/ds4-metal` | 87 | a Metal fork (pushed today); Ivan Fioravanti, founder of CoreView, mlx-lm contributor |
| `Entrpi/ds4` | 77 | CUDA Blackwell: "~4x prefill, ~1.5x decode, continuous batching, weight server, DSpark" *(the fork's own claim)* |
| `hebrus-labs/hebrus` | 66 | Metal-first MoE with expert streaming from SSD |
| `giannisanni/neutronstar` | 40 | CUDA, io_uring, host LFU cache, "first MTP for GLM-5.2" |
| `audreyt/ds4` | 36 | a variant with an "abliterated" checkpoint |
| `paperniuk/ds4` | 24 | M1/M2 tuning; Qwen3.8 Flash Next 262K on 64 GB, "35 tok/s on an M1 Max" |
| `kernelpool/ds4` | 15 | also an mlx-lm contributor |
| `kyuz0/strix-halo-ds4-toolbox` | 94 | toolbox containers for Strix Halo |

Independent, non-fork projects that refer to ds4 in their description: `mw00/project-maya` (1,080 stars, C++, "run GLM-5.3-Flash and DeepSeek-V4.1-Flash privately on your own GPU(s), from one card to 16, NVIDIA or AMD") and `gufo-org/gufo` (816, "Open Source Strix Halo AI engine"); the connection to ds4 is not verified *(unverified)*. The idea of "an engine built around specific models" is also copied by others (hebrus, mlx-serve, Splash, gufo).

**Reading the momentum** *(my inference from the numbers)*: about 24K stars in 5.4 months, 827 commits, daily pushes and a visible ecosystem (a menu-bar app, forks for Blackwell, Strix and M1). The architecture's bus factor ≈ 1, but the MIT license and 2,314 forks mitigate the risk.

### 5.16 Strengths and weaknesses, gotchas

+ It runs the **newest gigantic MoEs** (284B–1.6T) on 96–128 GB machines at an interactive speed thanks to 2-bit experts + an architecture with a compressed KV + SSD streaming. The mlx-lm quantization presets do not offer this asymmetric recipe by default; the closest is oQ2.
+ The on-disk KV + tool ID replay are built for coding agents.
+ Dependencies: C + Metal/CUDA/HIP, no Python at run time.
− One model per process, no model manager, authentication or hot reload; models are sometimes "opportunistically" removed.
− Fast changes, no releases/tags, "instabilities and regressions are definitely possible"; about 793 open items per single maintainer.
− **Numerical non-identity** of the scalar, batched, TP and speculative paths (documented).
− A single CUDA/ROCm GPU serves sessions one by one (no speedup); ROCm only gfx1151.
− The code is largely written with AI assistance (the project's declaration) — the review surface is about 250K lines.

### 5.17 Who is behind it

**Salvatore Sanfilippo (antirez)** — BDFL. Verified: GitHub profile ("Computer programmer based in Sicily, Italy… Born 1977", company field "Redis Labs" — out of date, 32.3K followers); Wikipedia: the author of Redis (2009), stepped down as maintainer on 2020-06-30, **returned to the Redis company in December 2024 as an "evangelist"**, then built Vector Sets. His blog, according to the summary, says that he "recently returned to Redis" and is working on DwarfStar *(wording approximate — the page was fetched by the summarizer)*. For ds4 there is no company, funding or paid version, MIT. Whether Redis pays for the time spent on ds4, I could not establish *(unverified)*. In more detail: [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

> **Check it yourself #3 — does ds4 have ROCm for gfx1201?**
> ```bash
> grep -n "ROCM_ARCH" Makefile
> grep -rn "ds4_rocm_is_gfx1151" rocm/ | head
> gh api repos/antirez/ds4/pulls/558 --jq '.state, .merged'
> ```
> You will see the default `gfx1151`, the `ds4_rocm_is_gfx1151()` gates and the state of PR #558 (as of 2026-10-19: open, unmerged). *(Reconstructed from the names in the notes; not run by me in this form. The `gh` command returns the state at the time of the call — it may be newer than in this chapter.)*

> **Check it yourself #4 — the size of the "small" engine.**
> ```bash
> wc -l ds4.c ds4_metal.m ds4_cuda.cu ds4_server.c ds4_kvstore.c
> ls docs/ && ls ~/.ds4/kvcache 2>/dev/null
> ```
> It should come out as 87,535 / 50,537 / 36,309 / 23,115 / 1,352 lines (the state of the clone from 2026-10-19; the numbers change quickly).

---

## 6. Apple's own stack: Foundation Models, Core ML, Core AI, ANE

Briefly, because this is not a path for running large open models.

- **Foundation Models** (a Swift framework): `LanguageModelSession`, type-guaranteed generation with `@Generable`, tool calls (`Tool`), transcripts, streaming, images. Requires a device with Apple Intelligence. The default on-device model has a window of **4,096 tokens per session** (the "managing the context window" documentation and TN3193). A 2025 post spoke of 65K tokens — **the numbers diverge**; what the API enforces is the value from the developer documentation (4,096), and the discrepancy remains unexplained.
- **Third-generation models** (announced 2026-06-08, *company's own claim*, via a summarizer): **AFM 3 Core** (3B dense) and **AFM 3 Core Advanced** (20B sparse, 1–4B active; full weights in flash, shared experts always active, routed ones swapped into DRAM; "Instruction-Following Pruning" = routing per prompt, not per token). The 2025 model: about 3B, 2-bit QAT weights, KV sharing in a 5:3 block split (−37.5% cache), 15 languages *(company's own claim)*.
- **Private Cloud Compute from the same API** (iOS/macOS 27): `PrivateCloudComputeLanguageModel` — 32K context, "multiple levels" of reasoning, a daily request limit, requires network and entitlement; `SystemLanguageModel` — offline, no limit, 4K, no reasoning.
- **External models:** the framework "provides a consistent API experience for using any language model, including those you bring from other model providers"; an open model exported through **Core AI** (`apple/coreai-models`, BSD-3-Clause, 2,198 stars, created 2026-06-08; "start with a model of about 0.6B parameters") you load into `LanguageModelSession` through `CoreAILanguageModel` (macOS/iOS 27, Xcode 27).
- **Core AI** (macOS/iOS 27): in-app models on the CPU, GPU and Neural Engine; the `.aimodel` format, the AOT compiler `coreai-build`, `AIModelCache`. It sits next to Core ML; whether Core ML is being deprecated, I could not establish *(unverified)*.
- **A data point from the Core ML era** (Apple post, 2024): Llama-3.1-8B-Instruct, M1 Max, macOS 15.2 beta, Int4 block-wise (block 32) → **about 33 tok/s**, 16 GB → 4.2 GB, TTFT 51.9 ms; Apple targeted the **GPU**, because LLMs "are usually constrained by memory bandwidth" *(company's own claim)*.

**What you cannot do through this channel:** no OpenAI-style server, no arbitrary GGUF/safetensors without a Core AI export, a small on-device context, a requirement for an Apple Intelligence device; 30B+ models are not the framework's target.

### The Neural Engine vs the GPU

Apple itself runs LLM decoding on the **GPU**; so do MLX, llama.cpp, ds4 and oMLX. The ANE is a block of fixed shapes and low power draw, good for matrix multiplications with high compute density. The experimental dual-ANE + GPU in oMLX helps only **prefill** (compute-bound), requires *private* APIs, fixed shapes and INT8, and leaves the recurrent and precision-sensitive parts on the GPU. Rule of thumb: **ANE = dense compute and small "always-on" models; GPU = bandwidth-bound decoding of large models**. The Neural Accelerator from the M5 in the GPU cores targets prefill and TTFT, not decoding bandwidth *(company's own claim / third-party source)*.

---

## 7. exo — a cluster of Macs

**Layer:** a cluster layer that discovers machines on the network, decides how to split the model (pipeline or tensor parallelism), runs MLX on each node with MLX distributed collectives and exposes APIs compatible with OpenAI, Claude, Responses and Ollama, plus a panel.

### 7.1 Identity

Repository `exo-explore/exo`, Apache-2.0; Python (2.87 MB) + a Svelte panel + a macOS app in Swift + networking in Rust (`rust/networking`, `rust/exo_rs`). Created 2024-06-24; **47,965 stars**, 3,567 forks, 378 open items; latest release **v1.0.71 (2026-04-23)**, but with commits up to 2026-10-13 (the project ships from `main` and through the DMG). Most commits: AlexCheema 1,424, Evanev7 147, rltakashige 141, JakeHillion 74, cadenmackenzie 64. Maintainer: **exo labs** ("Run frontier AI locally"). The company's site: the mission "building the future of democratized, sovereign machine intelligence"; a mention of revenue: "open-source software and enterprise consulting"; **funding, investors and founders are not disclosed on the site** — I did not find a funding round. More: [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

Platform tiers (`PLATFORMS.md`): Tier 1 = Apple Silicon macOS (Mac Studio M3 Ultra, Mac mini M4 Pro, MacBook Pro M5/M4 Max); planned: Linux CUDA (DGX Spark), Linux CPU; Tier 2 planned: Vulkan/CUDA on Framework Desktop; Windows later.

> ⚠️ **Linux = CPU only.** README: "Currently, exo runs on CPU on Linux. GPU support for Linux platforms is under development." There is `uv sync --extra mlx-cuda12|mlx-cuda13|mlx-cpu` (the MLX CUDA backend), but **exo is not a way to use your AMD rig** — there is no AMD path.

### 7.2 How it works

**Discovery and networking:** the Rust crate `rust/networking` (`discovery.rs`, `swarm.rs`) with pub/sub based on **Zenoh** (`EXO_ZENOH_NAMESPACE` isolates clusters; `routing/router.py`, `event_router.py`, `topics.py`). Nodes find each other on the LAN automatically, with no configuration.

**Master election and event sourcing:** `shared/election.py` — elections (3 s limit, master heartbeat every 5 s, 30 s of master silence, retries 15–300 s); the comments note that a node that went down in a cluster of ≥ 3 may remain "visible" through Zenoh liveliness. `shared/apply.py` applies events to the shared state; `master/main.py` (35 KB) places and manages instances; workers run runners (`worker/runner/llm_inference`, `image_models`).

**Topology-aware placement** (`master/placement.py::place_instance`):

1. it enumerates **cycles** of connected nodes (`topology.get_cycles()`);
2. it filters by the required memory (model size vs node memory after accounting for instances being loaded), by backend support and by divisibility for tensor parallelism (`hidden_size % n == 0` and divisible KV heads; exception: DeepSeek V4);
3. it prefers the **smallest sufficient cycle**, RDMA cycles for `MlxJaccl`, download-progress and leaf heuristics.

Modes: `Sharding.Pipeline` or `Sharding.Tensor`; the `min_nodes` parameter.

```
 4 Mac Studio, full Thunderbolt 5 mesh (JACCL):

      A ───────── B          6 cables = 4·3/2
      │ ╲       ╱ │          every pair has its own link
      │   ╲   ╱   │          (the "fully connected" requirement)
      │     ╳     │
      │   ╱   ╲   │          tensor parallelism: every layer
      │ ╱       ╲ │          cut into 4, all_sum after every
      C ───────── D          block → needs low RDMA latency
```

**Parallel execution** (`worker/engines/mlx/auto_parallel.py`, 64 KB):

- `pipeline_auto_parallel` wraps layers in `PipelineFirstLayer/LastLayer` (send/recv of activations; a pipelined prefill queue);
- `tensor_auto_parallel` with `TensorParallelShardingStrategy` classes per architecture (Llama, DeepSeek V3, **DeepSeek V4**, GLM4 MoE (Lite), MiniMax, Qwen, GPT-OSS, Step 3.5, NemotronH, Gemma 4) that split linear layers, attention heads and MoE experts and insert `all_sum` collectives (`_AllSumLinear`, `ShardedMoE`);
- backends: MLX **ring (TCP)** or **MLX JACCL (RDMA over Thunderbolt 5)**; the macOS app installs a network profile and expects `rdma_ctl enable` from Recovery (macOS ≥ 26.2).
- There are "disaggregated inference" directories (`worker/disaggregated`, `engines/mlx/disaggregated`) — a prefill/decode split; maturity unknown *(unverified)*.
- API: OpenAI Chat Completions, Claude Messages, OpenAI Responses, Ollama; HF models; image models (flux, qwen) behind `EXO_ENABLE_IMAGE_MODELS`; the `EXO_OFFLINE` variable for offline work.

### 7.3 What limits exo

The README claims "up to 1.8x speedup on 2 devices and 3.2x speedup on 4 devices" for tensor parallelism and a "99% reduction in latency between devices" with RDMA *(project's own claim)*; the benchmark images refer to Jeff Geerling's cluster of 4 × M3 Ultra (Qwen3-235B 8-bit, DeepSeek V3.1 671B 8-bit, Kimi K2 Thinking 4-bit) *(project's own claim / third-party source — I read the claims, not the charts themselves)*. Constraints from the code and documents:

- **JACCL requires a full mesh** of Thunderbolt with TB5 cables, identical macOS versions on all nodes (even beta versions) and not all Mac Studio ports are suitable;
- **a pipeline gives capacity, not the speed** of a single decoding stream — every token passes through all the stages;
- tensor parallelism needs divisible heads/dimensions and per-architecture code;
- master election briefly pauses the cluster;
- Linux CPU only; no AMD path.

The Apple post from October 2026 shows the same MLX + JACCL mechanism on 4 × M5 Ultra (§2.6) — **so exo's central trick has been confirmed by the vendor**.

> **Check it yourself #5 — how exo chooses the layout.** Read `src/exo/master/placement.py`, function `place_instance`:
> ```bash
> gh api repos/exo-explore/exo/contents/src/exo/master/placement.py --jq .content | base64 -d | sed -n '1,120p'
> ```
> Look for `get_cycles`, the memory and divisibility filters (`hidden_size % n`). *(The command is assembled from the path in the notes; not run by me.)*

---

## 8. What this means for the reference setup

### 8.1 On a Mac — what you can deploy today

The memory configuration of the Mac decides the choice. The rule from §1: look at **GB/s and GB of RAM**, not at cores.

| If… | consider | Why / note |
|---|---|---|
| you just want to run a model on a Mac and have a wide choice | **mlx-lm** (`mlx_lm.convert`, `mlx_lm.server`) | the widest model coverage (137 architectures); models in `mlx-community` |
| you use coding agents (Claude Code, OpenCode, Codex) and have long histories | **oMLX** | the KV cache on SSD survives a restart, Anthropic API, model pinning and TTL, menu bar; remember the single maintainer and the patches |
| you have a Mac with ≥ 96 GB (ds4 README: "64 GB for Qwen and 96 GB or more") and want DeepSeek V4 Flash locally with an on-disk KV | **ds4** | an engine built for this class of models (the project does not publish comparisons with other engines), but beta, one model per process, no authentication |
| you have two to four large Macs connected by TB5 and want a bigger model | **exo** (or `mlx_lm.server --pipeline`) | remember: pipeline = capacity, not speed; full mesh = 6 cables for 4 machines |
| you need an app with a GUI and an API | LM Studio, Ollama | see [`05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md`](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) — both have MLX paths |

Practical rules that follow from the chapter:

1. **Before you buy/choose a Mac, calculate the ceiling** from §1.4 for the model you want to use; take ~50–70% as a realistic speed.
2. **An MoE with a small number of active parameters** (like DeepSeek V4 Flash: 13B out of 284B) is the best fit for large memory and medium bandwidth — RAM counts for the whole thing, and bandwidth for the active part.
3. With agents, **always enable a persistent prefix cache** (oMLX or the on-disk KV in ds4) — it is the difference between "the agent waits several tens of seconds for every step" and "it waits seconds".
4. With speculative decoding, **measure on your own prompts**: the gain depends on the content (§5.8), and both projects (ds4, oMLX) admit that it is sometimes slower than plain decoding.

### 8.2 On your AMD rig — honestly

You cannot run anything from this chapter (the box at the beginning). **That is why the ideas are the most valuable part**, which you can carry over to **llama.cpp + llama-swap**. A mapping to what llama.cpp has today (chapter 04; build 0ce8cd1 and the state from the notes):

| Idea from this chapter | Where it is in this chapter | Equivalent in llama.cpp (from the notes) | What you can do |
|---|---|---|---|
| **An SSD tier for KV / cache persistence** | oMLX §4.5, ds4 §5.7 | the RAM prompt cache `--cache-ram` (default 8192 MiB), `--cache-idle-slots`, context checkpoints (`--ctx-checkpoints`, default 32), the `/slots` endpoint for saving/restoring slot state | Increase `--cache-ram`; consider saving slot state through `/slots` to persistent storage between restarts. The `--slot-save-path` flag was not confirmed in the notes — check it in your build. There is no built-in SSD tier like in oMLX. |
| **A stable tool-call format so the prefix matches** | ds4 "tool ID replay" §5.7 | longest common prefix matching when choosing a slot | Make sure the agent client sends the history back **byte for byte** the same — any change in JSON serialization invalidates the prefix. |
| **Fast paths for a single model** | ds4 §5.2 | none; llama.cpp is generic | You can build model-specific settings for one model: tensor split, `-ot` (override tensor) for experts, pinning the context size (`-c` explicitly, because `--fit` changes the context). |
| **A cache of hot experts** | ds4 §5.6, oMLX §4.6 | the new `src/llama-moe-cache.{h,cpp}` — "recently used experts of host-resident MoE layers in a device buffer" | Worth a look when you keep an MoE partly in RAM. With 4 × 32 GB resident you do not need it. |
| **Model-native speculative decoding** | ds4 DSpark/MTP §5.8, oMLX MTP/DFlash §4.7 | `common_speculative_type`: `DRAFT_MTP`, `DRAFT_DFLASH`, `DRAFT_DSPARK`, `DRAFT_EAGLE3` and model-free n-gram variants (`NGRAM_*`, `examples/lookup`) | **You already do this** (DSpark on the rig). The n-gram variants "from the prompt" do not need a separate model and may give a gain where the agent quotes its own code — *my guess, measure it*. I did not check which of these variants you already have enabled in the speed-up guide. |
| **Asymmetric quantization and imatrix on experts** | ds4 §5.4, oQ §4.9 | `--tensor-type`/`-ot`, imatrix, Unsloth Dynamic quantizations | You already have UD-IQ3_XXS; you can compare it with your own "2-bit experts, Q8 for the rest" recipe. |
| **Model profiles (`model:profile`)** | oMLX §4.3 | `llama-swap` | Alias the same model with different sampling presets per agent. |

An additional note about architecture, not about the engine: **a compressed KV with an indexer (§5.5)** is a feature of the *model* (DeepSeek V4), not of ds4 — you benefit from it in llama.cpp too, as long as it implements that type of attention. That is why, when choosing models for long agentic contexts, the attention architecture matters, not only the number of parameters.

### 8.3 What not to do

- Do not treat ds4 as a replacement for llama.cpp on the rig: it will not build on gfx1201 without patches, and the only data point is 2–5 tok/s on a single card.
- Do not expose ds4 to the network: no authentication; the TP protocol has no encryption.
- Do not overrate the "project's" numbers (ds4, oMLX): they are the projects' own measurements, on selected machines and prompts.

### 8.4 The chapter summarized in five sentences

1. On a Mac, **GB/s decide tok/s**; the M5 Ultra has about 1.2 TB/s, but even the M5 Ultra gives a ceiling of "only" about 117 tok/s for a 13B-active MoE at 4 bits (my calculation, @70%).
2. MLX is a framework (it has a Metal and a CUDA backend, **no HIP**), mlx-lm is the LLMs on top of it, oMLX is a server with a KV cache on SSD, exo is a cluster.
3. ds4/DwarfStar is a deliberately narrow engine in C: a graph hard-coded per model, expert streaming from SSD, an on-disk KV, DSpark/MTP.
4. On the reference rig (gfx1201) ds4 works today only with unmerged patches and with SSD streaming (2–5 tok/s on a single card); the reference rig's roughly 50 tok/s in llama.cpp is a **different** setup (weights resident across 4 cards), so the comparison is not like-for-like.
5. Carry over the ideas, not the code: a persistent prefix cache, stable tool calls, model-native speculation and asymmetric quantization.

---

*Sources for this chapter: see `07-APPLE-MLX-OMLX-AND-DS4.md.sources.txt`. The full list of all the course's sources: [`SOURCES.md`](SOURCES.md). For context: [`01-MAP-AND-LAYERS.md`](01-MAP-AND-LAYERS.md), [`02-HOW-INFERENCE-WORKS.md`](02-HOW-INFERENCE-WORKS.md), [`03-QUANTIZATION-AND-FORMATS.md`](03-QUANTIZATION-AND-FORMATS.md), [`04-LLAMA-CPP-AND-THE-GGML-FAMILY.md`](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md), [`09-COMPARISON-AND-CHOICE.md`](09-COMPARISON-AND-CHOICE.md), the guide [`../speeding-up-generation/README.md`](../speeding-up-generation/README.md).*
