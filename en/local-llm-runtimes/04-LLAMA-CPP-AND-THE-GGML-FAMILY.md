# 04 · llama.cpp and the ggml family

**Why this chapter.** This is the deepest chapter of the course, because the reference production system stands on llama.cpp (four R9700 cards, `llama-swap`, DeepSeek-V4-Flash in UD-IQ3_XXS). After reading it you will be able to: (1) draw from memory the path of a single HTTP request all the way to a token in the SSE stream; (2) explain what a tensor, a graph, an allocator and the *scheduler* are in the ggml library, and why a matrix multiplication on weights sitting in RAM can end up on the GPU; (3) read the header of a GGUF file byte by byte; (4) understand why `-c 65536 -np 4` gives four slots of 16384 tokens each; (5) choose a multi-GPU split mode knowing what in it is experimental; (6) judge when to reach for ik_llama.cpp, llamafile, KoboldCpp, textgen or llama-swap instead of "plain" llama.cpp.

> ⚠️ **I ran nothing here.** All of it is desk research and code reading: the source tree at `0ce8cd1` (the production build, a commit from 2026-10-19) and the GitHub API from the same day. I have no speed measurements of my own, and the commands in the "Check it yourself" boxes are taken from research notes, not from my console. Line numbers refer to that tree and will drift — upstream ships several builds a day.

**Table of contents**
1. What llama.cpp is and where it sits in the stack (the dependency network)
2. The ggml library: tensor, graph, allocator, backend and *scheduler* — with an example of offloading one matmul
3. GGUF: the byte layout, annotated
4. libllama: per-architecture graph builders, batch/ubatch, context size, KV cache classes
5. Sampling and grammars
6. llama-server from the inside: the slot loop, prompt cache, checkpoints, router mode, built-in tools/MCP
7. Speculative decoding: the types
8. Multiple GPUs: three split modes and what that means for 4×R9700
9. HIP: how ROCm reuses CUDA code and what is specific to RDNA4
10. Tools: bench, quantize, imatrix, fit
11. The family: ik_llama.cpp, llamafile, KoboldCpp, textgen, whisper.cpp and ggml as a library, llama-swap
12. Who is behind it
13. Gotchas
14. What this means for the reference setup

---

## 1. What llama.cpp is and where it sits in the stack

**llama.cpp** is an inference engine written in C/C++: a library (`libllama`), several command-line tools and an HTTP server (`llama-server`). It loads a model from a GGUF file and runs it on the CPU and on about fifteen kinds of accelerators. It is built on the tensor library **ggml** (the `ggml-org` organization maintains it separately, and a copy of it sits in `ggml/` inside llama.cpp). Repository: `github.com/ggml-org/llama.cpp` (formerly `ggerganov/llama.cpp`), MIT license, created 2023-03-10. As of 2026-10-19, from the GitHub API: **131,716 stars, 24,555 forks, about 11,741 commits and about 2,138 contributors** (including anonymous ones). There are no semantic versions — the "version" is the build number `bNNNNN`; the newest tag on the day of the review is `b11741` (three releases in the preceding six hours). The reference production tree is commit `0ce8cd1` from the same day, so effectively the current HEAD.

### Three layers in one repository

It helps to separate three things that blur together into "llama.cpp" in conversation:

| Layer | Directory | Size (lines, my count from the rig) | What it does |
|---|---|---|---|
| **ggml** — tensors, compute graph, backends | `ggml/` (`ggml/src` ≈ 514k lines including backends and shaders) | ~514k | knows `ggml_tensor`, the operations, the allocator, the scheduler and all backends (CUDA, HIP, Metal, Vulkan, …) |
| **libllama** — model, context, KV cache, tokenizer, sampling | `src/`, `include/llama.h` | ~112k (of which `src/models/` ≈ 43k in 165 files) | loads GGUF, builds the graph for a given architecture, manages KV memory, turns logits into tokens |
| **applications** — `common/`, `tools/` | `common/` ~44k, `tools/server` ~36k, `tools/mtmd` ~31k, … | | flag parsing, chat templates, grammars from JSON schema, the server, bench, quantize |

The boundary has practical significance: **ggml has no notion of a KV cache, a tokenizer or sampling**. That is why, when someone embeds ggml (whisper.cpp, stable-diffusion.cpp), they write those pieces themselves; and when someone wants a decoder-only LLM, they take libllama.

### Dependency map

```
                    Hugging Face  (since 2026-02-20 employs the core ggml.ai team)
                          |
 ggml-org/ggml  <--sync--> ggml-org/llama.cpp (ggml/ + src/ + common/ + tools/) <--sync--> whisper.cpp
      |                         |
      |       +-----------------+--------------+-------------------+----------------+
      |       |                 |              |                   |                |
 stable-diffusion.cpp   Ollama (pin b11669)  LM Studio, Jan   llamafile (a copy,   KoboldCpp
 bark.cpp (dormant)     = llama-server process  (use         lagging by weeks)   = embedded fork
                         + `llama/compat` patches  llama.cpp)                      + Python launcher
      |
 ik_llama.cpp = a fork from 2024, developed separately (IQ*_K quants, trellis)
 textgen (oobabooga) = runs llama-server as a child process
 llama-swap = proxy + process manager in front of any OpenAI-compatible server
```

What on this map is verified in code or in a primary source:
- **Ollama** — the cloned tree contains a file with the pinned version `LLAMA_CPP_VERSION = b11669`, and `llama/README.md` says it downloads the pinned source, applies the patches from `llama/compat/` and builds `llama-server`. I did not find the `ml/backend` directory, i.e. the former Go engine on top of ggml is no longer there. According to this tree, Ollama in October 2026 is a Go orchestrator around a llama.cpp subprocess (plus an MLX path on the Mac). That is a change relative to 2025 — details in `05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md`; here I only note that the author of the notes asks for this to be confirmed with the Ollama researcher.
- **LM Studio** — documentation: it runs on llama.cpp, and on Apple Silicon also on MLX (`lmstudio.ai/docs/app`). The application is closed source.
- **Jan** — the README names llama.cpp as its foundation; the license per the API is NOASSERTION, while the README says Apache-2.0.
- **ramalama, LocalAI, lemonade, Docker Model Runner** — I did not check their dependence on llama.cpp in this chapter *(unverified)*; see chapter 05.

### What llama.cpp does *not* try to do

The project declares "plain C/C++ without dependencies" and "zero memory allocations at runtime" *(project's own claim, ggml README)*, and the contribution policy says it should be "as simple as possible" and run by a "small team" (`AGENTS.md`). It is not a datacenter-class server: it has no PagedAttention, no prefix tree, no mature tensor parallelism and no request priorities and preemption like vLLM/SGLang (chapter 06). It has continuous batching and slots, but a much simpler *scheduler*. This is a choice: the broadest hardware and format support at the cost of server sophistication.

---

## 2. The ggml library

### 2.1 A tensor is a graph node

In ggml, `struct ggml_tensor` (`ggml/include/ggml.h:685`) is at once the data and a node of the graph. The fields you need to know:

| Field | Meaning |
|---|---|
| `type` | element type (`ggml_type`: F32, F16, Q4_K, …) |
| `ne[4]` | number of elements in each dimension (`GGML_MAX_DIMS 4`) |
| `nb[4]` | **strides in bytes** — this is why views and transposes are free, and why quantized types are addressed per block |
| `op`, `op_params[]` | which operation (`enum ggml_op`) produced this tensor |
| `src[10]` | up to 10 inputs (`GGML_MAX_SRC 10`) |
| `view_src`, `view_offs` | if it is a view: whose, and at what offset |
| `buffer`, `data` | where the data physically sits |
| `name[64]`, `extra` | debug name; backend-private data |

**Analogy.** Writing `c = ggml_mul_mat(ctx, a, b)` is not a computation, it is *placing an order*: a tensor `c` is created with `op=MUL_MAT` and `src={a,b}`. The computing happens only when someone executes the whole graph. **Precisely:** `ggml_context` is an arena (bump allocator) holding only tensor metadata (with `no_alloc` — without data); the data lives in separate backend buffers.

An example of the steps (my calculation, assuming that the row stride is the number of blocks times the block size): a 4096×4096 weight matrix in Q4_K is 4096/256 = 16 blocks of 144 B per row, so `nb[1]` = 2304 B, and the whole thing is 16,777,216 / 256 · 144 B ≈ 9.4 MB. A block size of 144 B / 256 weights = 4.5 bits per weight — consistent with the comment in `ggml-common.h`.

### 2.2 The graph: `ggml_cgraph`

`struct ggml_cgraph` (`ggml/src/ggml-impl.h:341`) holds an array `nodes` (tensors to compute), `leafs` (constants and inputs), optionally gradients (training, `ggml-opt.cpp`), a set of visited tensors, use counters and a `uid`. This `uid` lets `llama_context` recognize an identical graph and **reuse** it (`can_reuse`, `src/llama-context.cpp:1521`) instead of building from scratch for every ubatch. Default size: `GGML_DEFAULT_GRAPH_SIZE = 2048` nodes.

### 2.3 Memory: buffers, buffer types, the allocator

Data lives in **backend buffers** (`ggml_backend_buffer`), and each buffer has a **buffer type** (`ggml_backend_buffer_type`): CPU, pinned CPU (host/pinned), a CUDA device, a CUDA "split" buffer, shared Metal, a Vulkan device, and so on. This distinction is the key to the rest of the chapter: *where an operation is computed* is decided, among other things, by *which buffer the weight sits in*.

`ggml-alloc.c` (1,173 lines) is the graph allocator: it computes tensor lifetimes and reclaims memory, and where an operation allows it (`ggml_op_can_inplace`), computes in place. "Zero allocations at runtime" is achieved like this: libllama **reserves the worst case of the graph once** (`llama_context::graph_reserve`, `sched_reserve`, `src/llama-context.cpp:715–830, 2621`), and every subsequent decode uses the ready-made compute buffers.

### 2.4 Backends

The backend registry (`ggml-backend-reg.cpp`) can load backends as shared libraries (`ggml-backend-dl.cpp`, the `GGML_BACKEND_DL` option). Each device (`ggml_backend_dev_*`) answers the questions: `supports_op` (can I do this operation on these tensors), `supports_buft` (do I know this buffer type), `offload_op` (is it worth handing the operation to me, even if the weight sits elsewhere). Executing a subgraph is `ggml_backend_*_graph_compute`.

The tree has these backends (directories under `ggml/src`): CPU (x86 AVX/AVX2/AVX512/AMX, ARM NEON/SVE/KleidiAI, RISC-V, POWER, s390x, LoongArch, WASM), CUDA, **HIP/ROCm**, MUSA (Moore Threads), Metal, Vulkan, SYCL, OpenCL (Adreno), WebGPU, CANN (Ascend), Hexagon (Qualcomm), OpenVINO, zDNN (IBM Z), ZenDNN (AMD CPU), BLAS/BLIS, RPC, VirtGPU and `ggml-et`, whose target I did not check *(unverified)*. The largest: `ggml-opencl` ~76k lines, `ggml-sycl` ~51k, `ggml-cuda` ~49k (164 files plus 121 template instances), `ggml-vulkan` ~48.6k (including 188 files of ~16.4k lines of GLSL shaders), `ggml-metal` ~33k (of which ~15k are `.metal` kernels), CPU ~95k. The `ggml-hip` directory has zero lines of code — it is only a `CMakeLists.txt` (see §9).

### 2.5 The scheduler: the heart of heterogeneity

`ggml_backend_sched` (`ggml/src/ggml-backend.cpp`, roughly lines 900–2300) takes one graph and **assigns a backend to every node**, then cuts the graph into **splits** — contiguous pieces executed by one backend — inserting tensor copies where the backend changes. Constants: `GGML_SCHED_MAX_BACKENDS 16`, `GGML_SCHED_MAX_SPLIT_INPUTS 30`, `GGML_SCHED_MAX_COPIES 4` (more than one copy only with `parallel=true`, which allows pipelining input copies and using events).

Assignment rules (function `ggml_backend_sched_backend_id_from_cur`, lines 1069–1130), in order:

1. **The destination is already allocated.** If the node's destination buffer (or the buffer of its `view_src`) is already assigned, the node is pinned to the backend of that buffer (debug messages "1.dst"/"1.vsrc"). If that buffer cannot execute the operation, the program aborts.
2. **Graph inputs** (tokens, positions) go to the **last backend — assumed to be the CPU** ("1.inp").
3. **"Operations with weights preferably on the same backend as the weights"** — except `ROPE` and `FLASH_ATTN_EXT`, whose small side tensors are not a reliable hint.
4. **The operation offload rule (op-offload).** If the weight sits in **host** memory (a CPU buffer type) and `sched->op_offload` is enabled, the scheduler asks the higher-priority backends in turn: `supports_op && offload_op`. The first one that agrees executes the operation ("1.off"). For CUDA/HIP, `offload_op` returns `get_op_batch_size(op) >= op_offload_min_batch_size`, where the threshold defaults to **32** and can be changed with the environment variable **`GGML_OP_OFFLOAD_MIN_BATCH`** (`ggml-cuda.cu:180–183, 6011–6015`).
5. **Further passes** propagate the assignment to nodes that are still unassigned, checking `supports_op` and buffer type compatibility (the checks are visible around lines ~1370 and ~1391; I did not work out the exact number of passes).

### 2.6 Example: how one matrix multiplication on weights from RAM ends up on the GPU

Imagine an MoE model in which you keep the expert tensors in RAM (the `-ot` flag with a regular expression pointing at tensors and the target buffer type; check the exact syntax in `--help`, I did not run it), and the rest — attention, norms — on the GPU. Take one `ffn_up` multiplication on a weight sitting in a CPU buffer. The walkthrough below I **assembled from the rules described above and from the code in `ggml-backend.cpp`; I did not trace it in a debugger** *(my inference)*:

```
(1) LOADING     llama-model-loader mmaps the GGUF; the ffn_up weight lands in a CPU-type buffer
                (because of override-tensor / no room on the GPU).
(2) BUILD       build_ffn()/build_lora_mm() -> ggml_mul_mat(ctx, W_ffn_up, cur)
                = a MUL_MAT node, src = {W_ffn_up [CPU buffer], cur [activations]}.
(3) RESERVE     graph_reserve: worst case (ubatch 512) -> the scheduler assigns
                backends and allocates the compute buffers once.
(4) SPLIT       split_graph, for this node:
                  rule 1: destination not yet allocated            -> does not apply
                  rule 3: weight in a CPU buffer                   -> candidate: CPU
                  rule 4: weight in host memory, op_offload on
                            -> ask the GPU: supports_op && offload_op?
                               offload_op = (op batch size >= 32)
                  prefill, ubatch 512 :  512 >= 32  -> YES -> node goes to the GPU ("1.off")
                  decoding, batch 1:       1 <  32  -> NO  -> node stays on the CPU
(5) COPIES      where neighboring nodes have a different backend, the scheduler inserts tensor
                copies; with offload the weight flies from RAM to the GPU (the notes say:
                "streamed to the GPU"). I did not read the copy mechanism byte by byte.
(6) EXECUTION   split by split: backend_graph_compute() on its own piece.
```

**A consequence you can measure yourself:** with a partially offloaded model, **prefill speeds up as `-ub` grows** (more rows in the operation ⇒ the threshold of 32 is exceeded and it pays to ship the weights to the GPU), while **token generation (batch 1) stays on the CPU**. For you this matters in one case: if any part of DeepSeek's experts ever lands in RAM, prefill and decoding will behave completely differently.

> **Check it yourself #1 — the offload rule.** Open `ggml/src/ggml-backend.cpp` and go to the function `ggml_backend_sched_backend_id_from_cur` (lines ~1069–1130); find the comments "1.dst", "1.inp", "1.off". Then `grep -n "GGML_OP_OFFLOAD_MIN_BATCH" ggml/src/ggml-cuda/ggml-cuda.cu` — you should land on the threshold of 32. *(Commands from the notes; not run by me.)*

### 2.7 Quantization blocks in one paragraph

The details of the formats are in chapter 03; here only what is needed to read the code. A quantized weight is a **block + a scale**. `block_q4_0` = fp16 `d` + 16 B of nibbles for 32 weights = 18 B / 32 = **4.5 bpw**. K-quants use **super-blocks of 256 weights** (`QK_K = 256`) with a second level of quantization: `block_q4_K` = fp16 `d`, fp16 `dmin`, 12 B of packed 6-bit scales and minimums, and 128 B of nibbles = 144 B / 256 = **4.5 bpw**; `block_q6_K` = 210 B = 6.5625 bpw. i-quants (IQ*) use lattice/codebook tables, e.g. `block_iq2_xxs` = 2.0625 bpw, and `IQ4_XS` = 4.25 bpw. **MXFP4**: 1 B of E8M0 scale + 16 B of E2M1 nibbles for 32 weights = 17 B = 4.25 bpw (the OCP format from gpt-oss); **NVFP4**: 64 weights = 4 UE4M3 scales + 32 B = 36 B = 4.5 bpw. The `ggml_type` enum has `GGML_TYPE_COUNT = 43` in this tree (new ones: Q1_0 at 1.125 bpw and Q2_0 at 2.25 bpw).

Why "block + scale" and not one scale per tensor? The multiplication kernels (`mmq`, `mmvq`, `vec_dot` on the CPU) **quantize the activation column on the fly** to Q8_0/Q8_1/Q8_K and compute dot products in int8 per block, then multiply by the two scales. The `block_q8_K` type exists solely as an activation format for K-quant dot products.

---

## 3. GGUF: the byte layout

GGUF is the only model format that llama.cpp loads (there remains the script `convert_llama_ggml_to_gguf.py` for old `.bin` files; HF checkpoints are converted by `convert_hf_to_gguf.py`). The definition: `ggml/include/gguf.h` (header comment) and `ggml/src/gguf.cpp` (module maintainer: Johannes Gäßler). Everything is little-endian:

```
offset 0
+----------------------------------------------------------------+
| magic  "GGUF"                                  (4 B)           |
| version  uint32  = 3  (GGUF_VERSION)                           |
| n_tensors  int64                                               |
| n_kv       int64                                               |
+----------------------------------------------------------------+
| n_kv times:                                                    |
|   key        : string  = uint64 length + bytes (no NUL)        |
|   value_type : enum gguf_type                                  |
|                u8,i8,u16,i16,u32,i32,f32,bool,string,array,    |
|                u64,i64,f64                                     |
|   value      : the value; for array: element type + u64 count  |
|                + elements                                      |
+----------------------------------------------------------------+
| n_tensors times (tensor description, NO data):                 |
|   name    : string                                             |
|   n_dims  : uint32                                             |
|   ne[]    : int64 x n_dims                                     |
|   type    : ggml_type                                          |
|   offset  : uint64  (offset within the data block)             |
+----------------------------------------------------------------+
| padding up to the general.alignment boundary (default 32)      |
+----------------------------------------------------------------+
| data block: tensors one after another, each also aligned       |
+----------------------------------------------------------------+
```

Three consequences worth remembering:

1. **The file is self-describing.** Hyperparameters sit in keys such as `<arch>.context_length`, `<arch>.block_count`, `<arch>.attention.head_count`, and so on; the tokenizer in `tokenizer.ggml.tokens`, `tokenizer.ggml.merges`, `tokenizer.chat_template`. No separate `config.json` is needed.
2. **Alignment enables `mmap`.** Since the data is contiguous and aligned, the loader (`llama-model-loader.cpp:560–691`, the alignment check at line 691) maps the file into memory and hands the backends pointers straight into it. Hence "the model loaded in a second", while the actual reading from disk happens lazily.
3. **Large models are split:** `llama-gguf-split` creates files `*-00001-of-0000N.gguf`.

Loading modes (`include/llama.h:207`): AUTO(-1), NONE, MMAP, MLOCK, MMAP_MLOCK and **DIRECT_IO**; additionally a *lazy* mode (OFF/AUTO/ON) reads from disk only the rows of large tensors marked by the architecture (e.g. MoE experts) and only for tensors larger than 4 GiB.

> **Check it yourself #2 — the GGUF header.** Read the comment at the start of `ggml/include/gguf.h` and compare it with the diagram above. For your own file: the first four bytes (`head -c 4 model.gguf`) should give `GGUF`. *(Not run by me.)*

---

## 4. libllama

### 4.1 One architecture = one C++ class

Each architecture is a class in `src/models/<arch>.cpp` (the model file: `src/models/llama.cpp`, 248 lines). It overrides three things:

1. `load_arch_hparams(ml)` — reads GGUF keys into `hparams`;
2. `load_arch_tensors(ml)` — declares the expected tensors, e.g. `create_tensor(tn(LLM_TENSOR_ATTN_NORM,"weight",i), {n_embd}, flags)`; MoE layers get three-dimensional tensors `ffn_{gate,up,down}_exps` of shape `{n_embd, n_ff, n_expert}`;
3. `build_arch_graph(params)` — returns a subclass of `llm_graph_context` whose **constructor is the forward pass**: embedding → for each layer {`build_norm`, QKV via `build_lora_mm` (adds LoRA corrections), RoPE, `build_attn` (writes K/V into the cache via `ggml_set_rows`, reads them back as views, calls `ggml_flash_attn_ext` or the non-fused version), `build_ffn` or `build_moe_ffn`} → output norm → `lm_head` only for the rows from `inp_out_ids`.

The shared building blocks are in `src/llama-graph.cpp` (4,265 lines); the rest of the infrastructure: `llama-model.cpp` (3,985), `llama-model-loader.cpp` (1,876), `llama-arch.{cpp,h}`, `llama-hparams`, `llama-vocab.cpp` (4,696 lines: BPE/SPM/WPM/Unigram/RWKV tokenizers). `src/llama-arch.h` has 163 hits of `LLM_ARCH_*` (guards included), and `src/models/` has 165 files — so about 160 architectures: dense and MoE, attention+SSM hybrids (Mamba/Mamba2, Jamba, Granite-hybrid, Nemotron-H, Falcon-H1, LFM2, Kimi-Linear, the Qwen3-Next type with delta-net), RWKV, BERT-type encoders, T5, diffusion models and the DeepSeek V2/V3.2/V4 families with special attention caches.

**Practical conclusion:** adding a new architecture is a new file with a graph, not a change to the engine. That explains why new models appear in llama.cpp within days — and why every release can break something in your particular architecture. The tree even contains `skills/add-new-model` (instructions for contributing agents).

### 4.2 Where layers land

With `LLAMA_SPLIT_MODE_LAYER` (the default), layers go to devices proportionally to free memory or per `--tensor-split`; **the weight buffer type of a layer and its KV cache follow it** (`llama_kv_cache` takes a `layer_filter_cb` and allocates the K/V of a given layer on its device). Weights can be pinned with a regular expression (`--override-tensor`, `-ot`) — the standard trick: FFN experts in RAM, attention on the GPU. The new file `src/llama-moe-cache.{h,cpp}` keeps **the most recently used experts of MoE layers from the host in a device buffer**, driven by the scheduler's copy callback (according to the comment in the header). The `--fit` automaton (`common/fit.cpp`, `common_fit_params`) picks `-ngl`, the tensor split and the overrides so that the model + context fit in free memory; it is enabled by default and **does not work with the tensor-parallelism split mode**.

### 4.3 Context, batch and ubatch

- **`llama_batch`** (`include/llama.h:264`): `n_tokens`, `token[]` or `embd[]`, `pos[]`, `n_seq_id[]`, `seq_id[][]` (a token may belong to several sequences — this is how a prompt is shared), `logits[]` (for which positions we want output).
- **`n_batch`** = logical batch (`-b`, default **2048**), **`n_ubatch`** = physical batch (`-ub`, default **512**) (`common/common.h:458–459`). `llama_batch_allocr` sanitizes the batch and **cuts it into `llama_ubatch`es** (`src/llama-batch.h:17`; fields `n_tokens`, `n_seq_tokens`, `n_seqs`, `n_seqs_unq`, `n_pos` — 4 for M-RoPE — and an `equal_seqs` flag required by recurrent models).
- **`llama_context::decode`** (`src/llama-context.cpp:1821`): `memory->init_batch(balloc, n_ubatch, embd_all)` creates a *memory context* that already knows where in the KV cache each ubatch will go; then a loop {`mctx->apply()` (commits the slot, may defragment or shift) → `process_ubatch` (build or **reuse** the graph, `ggml_backend_sched_alloc_graph`, set the inputs, `graph_compute`) → read the logits} until `mctx->next()` returns false (lines 1925–2165).

### 4.4 Context size: the `-c / -np` gotcha

This is the most common surprise with the server, so I take it apart in detail.

- In `llama-context.cpp:379–391`: **`n_ctx_seq = n_ctx / n_seq_max`** (rounded to 256), *unless* `kv_unified` is set. In `llama_context_default_params` (line 4012) `kv_unified` defaults to **false**; `n_seq_max` defaults to 1 (line 3981).
- The server passes `--parallel` as the number of slots. I did not trace exactly how the value reaches `n_seq_max` *(unverified)*, but the consequence is described in the flag code.
- **Effect:** with the default, non-unified cache, `-c 65536 -np 4` gives **4 slots × 16,384 tokens**, each with its own KV "stream". A single agent conversation that grows to 30k tokens will not fit in such a slot (what the server does then depends, among other things, on `--context-shift`, §6.4).
- **The way out:** `--kv-unified` — "a single unified KV buffer shared across all sequences; enabled by default if the number of slots is automatic" (`common/arg.cpp:1728`). Then every slot has access to the whole `n_ctx` pool, and the sequences interleave in a single stream. `--kv-unified-per-slot` limits a slot's context under a unified pool (`server-context.cpp:1357–1372`).
- By default `-np` = 1; the help text says `-1` = auto (`common/common.h:462`, `arg.cpp:2548`).

The trade-off: non-unified slots reserve `n_ctx / N` permanently, even when they stand empty; the unified pool is flexible, but the sequences compete for the same cells.

> **Check it yourself #3 — context splitting.** `grep -n "kv_unified" src/llama-context.cpp` and read the area around lines 379–391. Then `grep -n "kv-unified" common/arg.cpp`. In the startup log of your `llama-server`, look for the per-slot context information (I did not check how exactly it is worded). *(Not run by me.)*

### 4.5 KV memory classes (`src/llama-kv-cache*.{h,cpp}`, `llama-memory*.{h,cpp}`, ~11k lines)

The interface `llama_memory_i` / `llama_memory_context_i` (`llama-memory.h`): `init_batch`, `init_full`, `init_update` (defragmentation/shift), `seq_rm/cp/keep/add/div`, `state_read/write` (saving and reading a session), and a per-ubatch *context* object that applies the change.

| Class | What it stores | What for |
|---|---|---|
| `llama_kv_cache` (`llama-kv-cache.h:20`, `.cpp` 2,962 lines) | a ring of **cells** (`llama-kv-cells.h`), each with a position and a set of sequence ids; K and V per layer (types `-ctk/-ctv`, default f16, `q8_0`/`q4_0` possible with flash-attn) | standard attention; `slot_info` maps an ubatch token to a cell (written via `ggml_set_rows`, so non-contiguous placement is cheap); *unified* = one stream, non-unified = one stream per sequence |
| `llama_kv_cache_iswa` | **two** `llama_kv_cache` objects: a full one for global layers and a small one (≈ window + ubatch, unless `swa_full`) for sliding-window layers | Gemma-2/3, gpt-oss, Llama-4 style; tokens older than the window are **lost**, so reusing a prefix requires server checkpoints |
| `llama_memory_recurrent` (1,386 lines) | a fixed state per sequence (Mamba/RWKV: conv+ssm, delta-net) — "one cell per sequence" | cannot be rolled back by position ⇒ checkpoint/restore for speculative decoding and the prompt cache |
| `llama_memory_hybrid` (+ `-idx`, `-iswa`) | `llama_kv_cache` for attention layers + `llama_memory_recurrent` for SSM layers in one model | Jamba, Granite-hybrid, Nemotron-H, Falcon-H1, LFM2 |
| `llama_kv_cache_dsa`, `_dsv4` (2,257 lines), `_msa` | caches specific to DeepSeek attention schemes (sparse attention with a "lightning indexer", compressed KV with a compression state, block selection) | they show how fast new attention mechanisms land: the graph and the cache are per architecture; there are dedicated CUDA kernels (`lightning-indexer.cu`, `dsv4-hc.cu`) |

⚠️ The last row concerns the reference model: the production tree has a dedicated cache class `llama_kv_cache_dsv4`. I did not check which exact class and kernels DeepSeek-V4-Flash in UD-IQ3_XXS runs, nor whether the `dsv4-hc.cu` kernels are compiled for HIP *(unverified)*.

**What is not here:** libllama has no PagedAttention or block tables, and no prefix tree across requests. Prefix reuse is done by the server: (a) it keeps a slot's KV in place and matches the longest common prefix, (b) it has a RAM **prompt cache** of saved slot states, (c) it creates **context checkpoints** (§6).

---

## 5. Sampling and grammars

A **sampler** (`llama_sampler`, `src/llama-sampler.cpp`, 4,391 lines) is a virtual table (`accept`, `apply` on a `llama_token_data_array`, `reset`, `clone`), and a **chain** (`llama_sampler_chain`) applies them one after another. Implemented: greedy, dist (the final draw), top-k, top-p, min-p, typical, temp/temp_ext (dynamic temperature), XTC, mirostat v1/v2, top-n-sigma, **DRY**, penalties (repetition/frequency/presence), logit-bias, infill, **adaptive-p** and **grammar** (greedy and lazy). The default order in `common_params` (`common/common.h:265–271`): penalties → DRY → top-n-sigma → top-k → typical → top-p → min-p → … → temperature; `common/sampling.cpp` builds the chain from `--samplers`. There is also a GPU sampling path (`llama-context.cpp:1398`, blocked for tensor parallelism); its scope was not checked.

**GBNF grammars** (`src/llama-grammar.cpp`) are a stack automaton over UTF-8 code points. At every step **all vocabulary tokens that would break the grammar are masked** — with large vocabularies and complex grammars this can be slow. `common/json-schema-to-grammar.cpp` compiles a JSON schema into GBNF. **Lazy grammars** (`llama_sampler_init_grammar_lazy_patterns`) switch on only after a trigger (e.g. a token/regex marking the start of a tool call), so reasoning in free text stays unconstrained — this is the mechanism that tool calling stands on.

**LLGuidance**: an optional library in Rust (`-DLLAMA_LLGUIDANCE=ON`; grammars starting with `%llguidance` go to it); `docs/llguidance.md` gives ~50 µs on average per mask for a 128k vocabulary *(project's own claim)*.

Tool calling and the structure of the response also depend on: Jinja templates (`common/jinja/`), the "autoparser" (`common/chat-auto-parser*.cpp`, `docs/autoparser.md`), PEG parsers (`common/peg-parser.cpp`, `common/parsers/`) and the handling of the reasoning budget (`common/reasoning-budget.cpp`).

---

## 6. llama-server from the inside

### 6.1 The path of a request

```
 client (curl, agent)
    |  POST /v1/chat/completions   (OpenAI)  |  /v1/messages (Anthropic)  |  /v1/responses
    v
 server-http.cpp (cpp-httplib) ---> parsing, chat template, grammar --> server_task
    |
    v
 TASK QUEUE (server-queue.cpp)
    |
    v                                          +-----------------------------+
 SLOT LOOP  update_slots()  (one thread)       |  slots: server_slot x N     |
    |  pre_decode():                           |  prompt, sampler, LoRA,     |
    |   - context shift (if full)              |  draft context,             |
    |   - assembles the BATCH: 1 token per    |  checkpoints                |
    |     generating slot + prompt chunks of   +-----------------------------+
    |     slots in prefill, up to n_batch
    v
 batch.render() ---> llama_decode(ctx, batch)
    |                   |  cuts into ubatches (n_ubatch), memory->init_batch
    |                   v
    |              ggml graph (build_arch_graph) --> ggml_backend_sched
    |                   |        split by split: GPU0, GPU1, ..., CPU
    |                   v
    |              logits (only the rows from inp_out_ids)
    v
 post_decode():  slot sampler (chain + grammar) -> token
    |             stop conditions, checkpoint, possible draft verification
    v
 response queue (server_response) ---> SSE: "data: {...}\n\n" ---> client
```

Details that correspond to fields in the code (`tools/server/server-context.cpp`, ~6.3k lines; the whole `tools/server` directory ~36k, of which about 25k is C++ without tests):

- `server_context_impl` (line 941) owns `n_parallel` **`server_slot`** objects (line 245); each has its own prompt tokens, sampler chain, an optional draft context, a LoRA set and "context checkpoints".
- **`update_slots`** (line 3256): if all slots are idle — return; otherwise send a NEXT_RESPONSE task; `pre_decode()`; `batch.render(off, n)` and `decode(...)` in a loop over `n_batch` windows, with an automatic retry at a smaller batch when KV space runs out; `post_decode()`.
- **Continuous batching** is enabled by default (`cont_batching = true`, disable with `-nocb`; `common/common.h:575`). This is "iteration-level" batching: new requests join at the next iteration; there are no separate prefill/decode phases and no priority policy beyond the batch budget *(I did not read the details of the policy)*.
- **Slot selection**: a request with `id_slot` goes to the indicated slot; otherwise the server picks the slot with the **longest matching prompt prefix** (LCP), and when nothing matches — the least recently used free slot (around `server-context.cpp:1780–1815`; the general outline checked, not line by line).
- **Number of slots** (`-np/--parallel`): default 1; each slot gets `n_ctx / N` tokens unless `--kv-unified` (§4.4).

### 6.2 The prompt cache in RAM

When a slot is about to be used for a different prompt, its tokens and the **serialized llama state** (target + draft) are written to RAM (`prompt_save`), and `prompt_load` restores the best match for the new request (`server_prompt_cache`, `server-task.h:668`). The default is **`--cache-ram 8192` MiB** (`-1` = no limit, `0` = disabled), with a limit in tokens as well equal to `n_ctx`; `--cache-idle-slots` (enabled by default, requires `--cache-ram`) saves idle slots to the cache when a new task arrives (`common/common.h:642`, `arg.cpp:1719–1745`, `server-context.cpp:1494–1520`).

Why this matters for agents: an agent loop sends a **growing prefix** every time (system prompt + history + tools). Without the cache every request would compute it from scratch; with the cache you compute only the new tail.

### 6.3 Context checkpoints

`-ctxcp/--ctx-checkpoints N` (default **32** per slot), spacing `-cms/--checkpoint-min-step` (default **8192** tokens). Why: sliding-window (SWA) and recurrent/hybrid models **cannot "forget" the tail** — the state cannot be truncated to an earlier position (§4.5). So the server **takes snapshots of the memory state during prefill**, so that a later request with a shared prefix can restore the nearest earlier snapshot instead of computing everything from scratch. Checkpoints also go into the `/slots` save files and are used to roll back rejected tokens in speculative decoding (`server-context.cpp:2544–2700`, `arg.cpp:1701`). **Cost:** RAM.

### 6.4 Context shift

`--context-shift`: when a slot fills `n_ctx`, it discards the older half of the unprotected tokens and shifts the positions (`llama_memory_seq_rm/add`). Not all memory types support it. For agents this is quietly dangerous: the model "forgets" the beginning of the conversation without any message.

### 6.5 Router mode (multiple models)

Started **without `-m`**, but with `--models-dir PATH` (scan of a GGUF directory), `--models-preset FILE` (INI-style presets, `common/preset.cpp`, `docs/preset.md`) or from the HF cache. `--models-max N` (default **4**) limits the simultaneously loaded models (`server-models.{h,cpp}`, about 3,000 + 486 lines; `common/common.h:695–699`; `arg.cpp:3663–3680`).

The router is a thin process that **launches a separate child `llama-server` per model** (`common/subproc.cpp`; commands `cmd_router_to_child:exit`, `cmd_child_to_router:state:` over stdout), routes requests by the `"model"` field, tracks the states `DOWNLOADING/DOWNLOADED/UNLOADED/LOADING/LOADED/SLEEPING`, **evicts the least recently used idle model** when the queue needs room (`server_lru_sched`, `server-models.cpp:270–400`), and supports `--sleep-idle-seconds` (the child releases weights after idling and wakes up later). This is a built-in "mini llama-swap" with LRU instead of groups/matrices (comparison in §11.6). Additional endpoints: `POST /models`, `/models/load`, `/models/unload`, `GET /models/sse`, `DELETE /models`.

### 6.6 The API surface

Registered in `tools/server/server.cpp` (lines ~256–386): OpenAI-compatible `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/models`, **`/v1/responses`** (the Responses API), `/v1/audio/transcriptions`, `/v1/rerank`; **Anthropic `/v1/messages` and `/v1/messages/count_tokens`**; token counting (`/v1/chat/completions/input_tokens`, `/v1/responses/input_tokens`); the old `/completion`, `/infill`, `/embedding`, `/tokenize`, `/detokenize`, `/apply-template`; `/props`, `/slots` (GET and POST `/slots/:id_slot` for saving/restoring), `/lora-adapters`, `/metrics` (Prometheus), `/health`; resumable streams `/v1/stream`, `/v1/streams/lookup`; and `/v1/systemone` — typed "decision models" that answer choice/rating questions in a single pass without generating a token (`server-decision.h`). The built-in web UI (Svelte, `tools/ui`) is embedded in the server (`--ui/--no-ui`). No telemetry: `common`, `tools`, `src`, `ggml/src` were searched for telemetry/analytics/posthog/sentry — no hits; no update check was found *(I did not search exhaustively)*. The `--offline` / `LLAMA_ARG_OFFLINE` mode (`common/arg.cpp:3953`) blocks the network.

### 6.7 Built-in tools and MCP — and a warning

New: `llama-server --tools read_file,file_glob_search,grep_search,exec_shell_command,write_file,edit_file,get_info` (or `all`), `--tools-runtime docker:<image>|podman:<image>|docker-container:<id>|ssh:<target>` to isolate tool execution, `--mcp-servers-config PATH` / `--mcp-servers-json` (the `mcpServers` format compatible with Cursor; the MCP client on the server side in `server-mcp.cpp`), and `--agent` = all tools + CORS/MCP proxy. Everything is marked in the code as experimental, with the message "do not enable in untrusted environments", with `--cors-origins` restricted to localhost (`common/arg.cpp:3437–3490`; `tools/server/server-tools.{h,cpp}`, `server-mcp.{h,cpp}`).

> ⚠️ **Security warning.** `--tools` with `exec_shell_command`, `write_file` and `edit_file` is **code execution on the host for anyone who can reach the server's port**. Do not enable it on an instance reachable from the network, and if you must experiment — use `--tools-runtime docker:…` and the address `127.0.0.1`. Likewise `ggml-rpc-server` (`tools/rpc`): its README calls it "proof-of-concept … fragile and insecure; never on an open network".

---

## 7. Speculative decoding

The idea (from the speed-up catalog): decoding is limited by memory bandwidth, so **checking several tokens proposed by a cheap "draft" costs little more than checking one**. The server verifies the draft in a single batched decode; for hybrid/recurrent targets it uses **checkpoints** to roll back rejected tokens (`spec_ckpt`, `server-context.cpp:266, 1388`). Implementation: `common/speculative*.{h,cpp}` (`speculative.cpp` 3.1k lines + `ngram-*`), document `docs/speculative.md`. The types (`common_speculative_type`, `common/common.h:175–186`), selected with `--spec-type` and `--spec-draft-n-max`:

| Type | Where the proposals come from | Notes |
|---|---|---|
| `DRAFT_SIMPLE` | a separate small model (`-md`) | the classic variant; requires the same tokenizer |
| `DRAFT_EAGLE3` | a lightweight EAGLE-3 head | `docs/speculative.md` lists drafts for Llama-3.x, Qwen3, gpt-oss, Gemma-4; conversion with `convert_hf_to_gguf.py --target-model-dir` |
| `DRAFT_MTP` | multi-token-prediction heads **inside the model** (e.g. NextN layers) | `llama-imatrix` has flags `--nextn`/`--model-draft` for collecting statistics for these layers |
| `DRAFT_DFLASH` | a block diffusion draft, emits a whole block per pass | |
| `DRAFT_DSPARK` | DFlash + a Markov head | |
| `NGRAM_SIMPLE`, `NGRAM_MAP_K`, `NGRAM_MAP_K4V`, `NGRAM_MOD`, `NGRAM_CACHE` | **no draft model**: proposals from n-grams of the text already seen (`ngram-*.cpp`) | free; good for code and repeated fragments (e.g. echoed tool calls) |

The variants can be mixed ("an implementation with a draft model can be mixed with an implementation without a model"). The older `examples/{speculative,lookahead,lookup}` are still in the tree. Whether your model has MTP heads or whether an EAGLE-3/DFlash draft is available for it, **I did not check** *(unverified)*; results for the reference hardware and model are in `../speeding-up-generation/README.md`.

---

## 8. Multiple GPUs: three modes and 4×R9700

The flag `-sm/--split-mode` (`include/llama.h:200`, `docs/multi-gpu.md`, `ggml/src/ggml-backend-meta.cpp`). A picture of what each mode does (four GPUs, one layer = one rectangle):

```
LAYER (default) — pipeline                   TENSOR (experimental) — meta backend
 token -> GPU0 -> GPU1 -> GPU2 -> GPU3          every layer cut into 4 pieces at once
                                                                          
 GPU0: layers   0..15   [########]              GPU0: [shard 0 of every layer]
 GPU1: layers  16..31   [########]              GPU1: [shard 1 of every layer]
 GPU2: layers  32..47   [########]              GPU2: [shard 2 of every layer]
 GPU3: layers  48..63   [########]              GPU3: [shard 3 of every layer]
                                                          \  |  |  /
 between GPUs: 1 activation tensor per boundary     ALLREDUCE over partial sums
 at any moment ONE GPU computes (for 1 token)       (NCCL / RCCL / fallback version)
                                                    several reductions per layer

ROW (deprecated): rows of dense weights split across GPUs; avoid, `--fit` rejects it
NONE: the whole model on `--main-gpu`
```

(The layer counts in the picture are an illustration, not the parameters of the reference model.)

| Mode | What the code actually does | Consequences for 4×R9700 |
|---|---|---|
| `none` | the whole model on `--main-gpu` | |
| **`layer`** (default) | **pipeline parallelism**: contiguous slices of layers per GPU, the KV of layer *l* on the GPU that owns it; traffic between cards = one activation tensor per boundary; proportional to memory or `-ts` | best prompt throughput, tolerant of slow PCIe; **token generation does not speed up with the number of GPUs** — for a single token one GPU works at a time; the documentation: it scales well only with many tokens |
| `row` | **deprecated** older row split for dense weights (`llama-model.cpp:1198–1203`) | avoid; `--fit` refuses it |
| **`tensor`** | **tensor parallelism via the "meta backend"** (`ggml-backend-meta.cpp`, 2,546 lines): a *meta device* wraps N real ones; each tensor gets a split state (`SPLIT_AXIS_0..3`, `MIRRORED`, `PARTIAL` = each GPU holds a partial sum, `NONE`) from a per-architecture callback; operations are computed on each GPU on its piece, and `PARTIAL` results are combined by an **allreduce** — through NCCL (CUDA) or RCCL (HIP, `-DGGML_HIP_RCCL=ON`, **off by default**, because it was "not universally beneficial") with a universal fallback (`ggml_backend_comm_allreduce_tensor`, `allreduce_fallback`) | **EXPERIMENTAL**; requires flash-attn enabled and an **unquantized KV (f32/f16/bf16)**; `--fit` is not supported (set `-c` by hand); the documentation *explicitly* lists architectures without an implementation, among them DeepSeek2, GLM-DSA, Nemotron-H, Granite-hybrid, LFM2-MoE, Minimax-M2, Mistral4, Kimi-Linear, Jamba, Falcon-H1, Mamba/Mamba2, Gemma-3n, OLMoE; "performance should be good for multiple NVIDIA GPUs with the CUDA backend, **no guarantees beyond that**" (`docs/multi-gpu.md`). The variable `GGML_CUDA_P2P=1` enables peer-to-peer copies (opt-in; with IOMMU enabled it can corrupt the output) |

The documentation: the `tensor` mode is "much more limited by interconnect speed" and does many reductions per layer; the `layer` mode "minimizes transfers … but needs many tokens to scale well".

### What this means for the reference hardware

1. Four R9700s are AMD with the HIP backend — exactly the "no guarantees" case. The `tensor` mode has **no promise whatsoever** from the project here (project's own claim). Whether it works and whether it speeds up decoding on gfx1201 depends on your own measurements, not on this chapter.
2. The list of architectures without a `tensor` implementation includes `DeepSeek2` and `GLM-DSA`. **DeepSeek-V4 is not on it by name**, but the code also contains no explicit confirmation that it is supported (in practice, on the reference machine tensor mode with DeepSeek-V4-Flash did start and gave a measured speed increase; I did not measure quality after the change — see §14 and `../speeding-up-generation/`) — check the current list in `docs/multi-gpu.md` of your tree *(unverified)*.
3. In `layer` mode, adding cards increases capacity (128 GB of total VRAM, 4×32), not the speed of a single stream. Traffic between cards is only activations across 3 boundaries.
4. `tensor` requires an **unquantized KV** — that is more memory for context than `q8_0`. For a model that barely fits in memory anyway, this is a real cost.
5. Practical knowledge from tuning this hardware (speculation, tensor split) is in the directory `../speeding-up-generation/README.md`.

> **Check it yourself #4 — the status of tensor mode.** Read `docs/multi-gpu.md` in your tree: the section on `-sm tensor`, the list of unsupported architectures and the sentence about "no guarantees". Also check `grep -n "GGML_HIP_RCCL" ggml/src/ggml-hip/CMakeLists.txt`. *(Not run by me.)*

---

## 9. HIP: how ROCm reuses CUDA code

**There is no separate tree of ROCm kernels.** `ggml/src/ggml-hip/CMakeLists.txt` collects the glob `../ggml-cuda/*.cu` (plus `template-instances/fattn-tile*, fattn-mma*, mmq*, mmf*` and the generated `fattn-vec` instances) and **compiles the same sources as HIP** (`LANGUAGE HIP` or `hipcc` as C++), defines `GGML_USE_HIP` and links `hip`, `hipblas`, `rocblas` (HIP ≥ 6.1 required). The translation layer is `ggml/src/ggml-cuda/vendors/hip.h` (313 lines; siblings: `cuda.h` 28, `musa.h` 161) — about 300 `#define` macros mapping CUDA names to HIP: `cudaMalloc→hipMalloc`, `cudaStream_t→hipStream_t`, `cublasGemmEx→hipblasGemmEx`, `CUBLAS_COMPUTE_32F→HIPBLAS_COMPUTE_32F`, `__shfl_sync(mask,…)→__shfl(…)` (without the mask).

**Analogy:** it is like compiling the same program for a different operating system through a compatibility layer, instead of rewriting it. **Precisely:** every CUDA kernel in the tree is at the same time an AMD kernel; the AMD-specific paths are the blocks `#if defined(GGML_USE_HIP) && defined(RDNA4)…` in `common.cuh`.

### RDNA4 / gfx1201

- `common.cuh` (lines 83–94, 280–282): the constant `GGML_CUDA_CC_RDNA4` = AMD offset + 0x1200 ("RX 9000"); `AMD_WMMA_AVAILABLE` enabled for RDNA3/RDNA4 (matrix multiplication on WMMA units).
- A dedicated tuning header **`mmq-config-rdna4.cuh`** — next to `-rdna3`, `-rdna3-5`, `-rdna2`, `-cdna`, `-gcn`, `-ampere`, `-blackwell`, `-pascal-*`. So the quantized matrix multiplication (`mmq`) has separate tile parameters for the R9700 cards.
- CMake options: `GGML_HIP_GRAPHS`, `GGML_HIP_NO_VMM`, `GGML_HIP_MMQ_MFMA` (CDNA/MI series, not the R9700), `GGML_HIP_RCCL`, `GGML_HIP_EXPORT_METRICS`, `GGML_CUDA_FORCE_MMQ/CUBLAS`, `GGML_CUDA_FA`. The former option `GGML_HIP_ROCWMMA_FATTN` **does not appear** in the HIP CMake of this tree (checked by its absence) — if you see it in old guides, it is out of date.
- Building (`docs/build.md:387–427`, the documentation has examples for gfx1030/gfx1100):

```bash
HIPCXX="$(hipconfig -l)/clang" HIP_PATH="$(hipconfig -R)" \
  cmake -S . -B build -DGGML_HIP=ON -DGPU_TARGETS=gfx1201 -DCMAKE_BUILD_TYPE=Release
```

  `HIP_VISIBLE_DEVICES` selects the cards. The `GPU_TARGETS` target must be exactly your `gfx` (see the gotchas).
- **The alternative for AMD: Vulkan** (maintained by 0cc4m and Jeff Bolz from NVIDIA according to `CODEOWNERS`). I have no comparative data for HIP vs Vulkan on gfx1201.

---

## 10. Tools

- **`llama-bench`** (`tools/llama-bench/llama-bench.cpp`, 2.5k lines): sweeps `-p` (prompt lengths), `-n` (generation lengths), `-pg`, `-b/-ub`, `-t`, `-ngl`, `-sm`, `-ts`, `-fa`, `-ctk/-ctv`, `-r` (repetitions, default 5); outputs md/csv/json/jsonl/sql; supports `--rpc` and `--fit-target`. It reports **pp** (prefill) and **tg** (generation) in tok/s. It is the canonical benchmark; results from a `README` without a "hardware/model/precision" line are not comparable.
- **`llama-quantize`**: the `QUANT_OPTIONS` table has ~40 recipes (Q1_0, Q2_0, MXFP4_MOE, TQ1_0/TQ2_0, IQ1…IQ4, Q2_K…Q8_0, F16/BF16). The perplexity annotations in the source (e.g. Q4_K_M "4.58G, +0.1754 ppl @ Llama-3-8B", Q8_0 "7.96G, +0.0026") are the project's numbers *(project's own claim; `tools/quantize/quantize.cpp:34–71`)*.
- **`llama-imatrix`**: `llama-imatrix -m f16.gguf -f calib.txt -ngl 99 -o imatrix.gguf`, then `llama-quantize --imatrix imatrix.gguf in.gguf out.gguf Q4_K_M`. imatrix files are GGUF by default today (the old `.dat` when the extension indicates it); `--process-output` is off by default; `--nextn`/`--model-draft` collect statistics for MTP/NextN layers (`tools/imatrix/README.md`). The importance matrix tells the quantizer which weights hurt more when rounded — key for low-bit quants such as IQ3_XXS (chapter 03).
- **`llama-fit-params`** and `common/fit.cpp`: determines `-ngl`, the split and the overrides so that everything fits in memory (§4.2).
- The rest: `llama-cli` (1.3k lines), `llama-perplexity` (2.1k), `llama-batched-bench`, `llama-gguf-split`, `llama-export-lora`, `llama-cvector-generator`, `llama-tokenize`, `llama-tts`, `ggml-rpc-server`.

---

## 11. The family

### 11.1 ik_llama.cpp — a fork aimed at speed and quants

**What it is:** a fork by Iwan Kawrakow (the author of the k-quants and i-quants), created 2024-06-27; `github.com/ikawrakow/ik_llama.cpp`, MIT, **3,311 stars, 494 forks** (2026-10-19), about 5,080 commits (with the inherited llama.cpp history), the only tag `t0002` from 2025-07-22 — work happens on `main`. According to the README (*project's own claim*) the last sync with upstream was in August 2024, and later models (DeepSeek-V4, GLM-5, Qwen3.x, Gemma4, Mistral 4) were ported by hand (over 70 models).

**How it differs from upstream** *(project's own claim, README and `docs/parameters.md`)*:
- quants that upstream does not have: the `IQ2_K…IQ6_K` family, `IQ2_KS…IQ5_KS`, `IQ4_KSS`; row-interleaved variants for the CPU (`_R4/_R8/_R16`); **trellis quants** `IQ1_KT…IQ4_KT`; `IQ1_BN/IQ2_BN` (BitNet); `Q8_KV` (an 8-bit KV cache);
- flags: `-fmoe` (MoE fusion), `-muge`, `-mqkv`, `-ger`, `-ser` (fewer active experts), `-rtr` (repacking at load time), `-mla`/`-amb` (MLA variants for DeepSeek), `-khad/-vhad` (Hadamard transform of K/V), `-ot`, and **`-sm graph`** — "split mode graph" for multiple GPUs (splits the tensors *and* the compute graph; README: "very effective for dense and MoE models");
- MTP for GLM-4.x MoE, delta-net fusion for Qwen3-Next/Qwen3.5-MoE, an MoE expert cache (`Implement moe cache #2644`, 2026-10-12).

**When to choose it:** CPU or hybrid CPU+GPU with a large MoE on "128 GB RAM + one card". **For the reference rig:** the README emphasizes the CPU (AVX2+/NEON) and CUDA (Turing+); Metal and HIP exist, but as a second category; HIP for gfx1201 is not a documented target *(unverified)*. Files with IQ_K/KT quants load **only** in ik_llama.cpp — a format lock-in; I did not check whether the type numbers collide with the new mainline types (Q1_0, Q2_0, NVFP4, MXFP4). The server is forked from an older version; I did not find router mode. **Do not assume it beats mainline on AMD** — all the speed evidence is from the author or from user posts (varied setups), so I do not quote numbers.

**Who is behind it.** A private individual, with no company and no funding; Kawrakow left llama.cpp in March 2024. The tension with upstream is documented in his own words (discussions #316 "Mainline is now copying stuff from ik_llama.cpp" of 2025-04-06 and #319): the dispute concerns attribution and the interpretation of the MIT license; at the same time work flows in both directions (e.g. discussion #2417 from 2026-09 about moving the new quants to mainline). Details in `10-MONEY-AND-PEOPLE.md`.

### 11.2 llamafile — one file that runs everywhere

**What it is:** a Mozilla.ai package binding a build of llama.cpp (plus whisper.cpp, stable-diffusion.cpp and transcribe.cpp) into a single **"Actually Portable Executable"** built on Cosmopolitan Libc, which runs on six operating systems and two CPU architectures, optionally with the weights inside. `mozilla-ai/llamafile` (formerly `Mozilla-Ocho/llamafile`), created 2023-09-10, **26,441 stars**, latest release **0.10.6 from 2026-09-15**.

**How it differs from upstream:**
- **Weights inside the executable** through an aligned ZIP archive — after `mmap` the pointers go straight to the GPU; that is why the author wrote his own `zipalign` (`docs/technical_details.md`). Windows has a 4 GB limit per executable, so there the weights must be external.
- **A sandbox by default:** `pledge()` (SECCOMP-BPF on Linux, native on OpenBSD) with the promises `stdio anet rpath` — the process can `accept()` but not `connect()`, cannot write or launch new processes; optionally `unveil()` (Landlock) through `--confine-reads`; skipped in GPU mode (`docs/security.md`).
- **0.10.0** rewrote the build system (BUILD.mk, no cmake); llama.cpp and whisper.cpp as submodules with `llama.cpp.patches/` patches. Upstream is tracked by hand: "Update llama.cpp to b10441" (2026-08-21), "b11100" (a draft from 2026-09-30) against upstream's b11741 — **a lag on the order of 600 builds (weeks)**.
- The CPU kernels (tinyBLAS, `sgemm`, `iqk_mul_mat*`) made their way into upstream over time (`ggml-cpu/llamafile/`), so the 2024 CPU speed advantage has mostly disappeared. There is also a new `agentfile`.

**When:** to send a model to a colleague's laptop without installing anything. **For the rig:** not useful for serving (ROCm requires a manual build). A pattern to copy: refusing `connect()` for an inference server — you can reproduce it in systemd (`RestrictAddressFamilies`, seccomp) around `llama-server` *(my idea, not checked)*. License: GitHub shows NOASSERTION, because the `LICENSE` file contains only a short Apache-2.0 notice and not the full text; the README says: the project is Apache-2.0, the changes to llama.cpp and whisper.cpp are MIT.

**Who is behind it.** Mozilla.ai; the project started as Mozilla Builders with Justine Tunney as the main author (600 commits), and in 2026 almost all commits are made by `aittalam` (Davide Eynard, Mozilla.ai). I could not establish Mozilla.ai's funding amounts. See `10-MONEY-AND-PEOPLE.md`.

### 11.3 KoboldCpp — all-in-one for stories and roleplay

**What it is:** `LostRuins/koboldcpp`, AGPL-3.0, **12,032 stars**, created 2023-03-16, release **v1.123.1 from 2026-10-13** (two releases a month). "One File. Zero Install." The core: a single **`koboldcpp.py` file of about 786 KB** (HTTP server, a Tk launcher, a multi-user queue, admin mode, `ctypes` bindings) + a native library from `kcpp_src/` (`gpttype_adapter.cpp` 351 KB) linked with an **embedded fork of ggml/llama.cpp**; the `upstream` branch is merged into `concedo`. Added on top: stable-diffusion.cpp, whisper, TTS, image/video/music generation, the **KoboldAI Lite** interface, MCP and an agent.

**How it differs from upstream:** UX features on top of the same ggml — **Context Shifting** (enabled by default for GGUF, `--noshift`), `--smartcontext`, **SmartCache** (`--smartcache X`, KV snapshots in RAM per conversation), `--multiuser`, `--admin/--admindir` with `.kcpps` files, `--routermode` (model swapping by the `model` field) *(project's own claim, wiki)*. It keeps the older ggml v1/v2/v3 loaders (`otherarch/`: GPT-2, GPT-J, GPT-NeoX, MPT, RWKV) for very old models.

**Hardware:** CUDA, **Vulkan (the recommended path for AMD)**, Metal, CPU; **ROCm only through the third-party fork** `YellowRoseCx/koboldcpp-rocm` ("check the maintenance status"). **For the reference rig:** gfx1201 would mean Vulkan, and on the server side there is no reason to abandon mainline. Worth a look: the SmartCache ideas, `.kcpps` files as profiles and the set of `kcpp_adapters/*.json` for detecting chat templates. **A licensing note:** AGPL — exposing a modified version over the network obliges you to make the source available; for your own, unmodified internal use it is usually no problem, in a product it is a matter for legal review.

**Who is behind it.** A single creator (LostRuins, 4,374 own commits), no company, no observed funding (no hits in the README and FUNDING.yml; no GitHub Sponsors listing).

### 11.4 text-generation-webui, today "textgen" (oobabooga)

**What it is:** a web UI (Gradio) for local LLMs, renamed into a desktop application; the repository is `oobabooga/textgen` (the old name `text-generation-webui` still resolves), AGPL-3.0, **47,738 stars**, created 2022-12-21, release **v4.9 from 2026-05-20**, last push 2026-08-17. It is **not an engine**: it *drives* engines — llama.cpp through `llama-server`, ExLlamaV3, TensorRT-LLM and Transformers; switching without a restart. The llama.cpp path launches **`llama-server` as a child process** and talks over HTTP (commits: "Update llama.cpp", "Bind llama-server to parent process lifetime"). I did not read the integration code in depth.

**When:** tinkering, character templates, LoRA training, quick backend comparisons. **For the rig:** the value is the pattern "engine as a separate process, the UI does not link it" — thanks to which restarting the engine does not kill the UI. The release cadence has slowed (last release 2026-05).

**Who is behind it.** A pseudonymous single creator (oobabooga, about 82% of commits); the README mentions a grant from Andreessen Horowitz from August 2023 *(project's own claim)*; a GitHub Sponsors listing exists.

### 11.5 ggml as a library to embed, whisper.cpp

`ggml-org/ggml` (MIT, created 2022-09-18, **15,509 stars**) has recently had **numbered releases** (v0.26.0 from 2026-10-05 and v0.27.0 from 2026-10-15). The same code lives in `llama.cpp/ggml/` and `whisper.cpp/ggml/`; changes flow through "sync: ggml" PRs and **the copy in llama.cpp is fresher** than the standalone repository for the big backends. The API surface: `ggml.h` (operations), `ggml-backend.h` (devices, buffer types, scheduler), `ggml-alloc.h`, `ggml-opt.h` (optimizer), `gguf.h`. Who embeds it: **whisper.cpp** (54,489 stars, v1.9.5 from 2026-10-06), **stable-diffusion.cpp** (7,731 stars; diffusion: SD, Flux, Wan, Qwen Image…), bark.cpp (869 stars, dormant since 2024-11-16), and indirectly llamafile, KoboldCpp, ik_llama.cpp.

**When ggml, and when libllama:** ggml for non-LLM models (diffusion, speech, embeddings) and training experiments; libllama for decoders, because the KV cache, sampling and tokenizers **are not in ggml**.

**whisper.cpp** (MIT, 2022-09-25, about 5,588 commits; the most: ggerganov 1,444): speech recognition in ggml with CUDA, Metal, Core ML, Vulkan, HIP, OpenVINO, Ascend, Moore Threads, VAD, streaming and bindings (Rust, JS, Go, Java, Ruby, Swift, .NET, Python, R, Unity); models from tiny (75 MB) to large-v3-turbo (2.9 GB) *(project's own claim)*. For you: an STT front end for voice agents on Macs; it works as a library or as `whisper-server`.

### 11.6 llama-swap — a process switcher in front of the server

**What it is:** a single static binary in Go (`mostlygeek/llama-swap`, MIT, **6,015 stars**, created 2024-10-04, releases numbered with plain numbers: **v265 from 2026-10-14**), which is a **reverse proxy and process manager**: it exposes one OpenAI/Anthropic-compatible endpoint and, according to the `model` field of each request, starts or stops the right server (llama-server, vLLM, anything with HTTP). It does not touch tensors.

**How it works** (`internal/router/design.md`):
- YAML configuration: each model has `cmd` (must contain `${PORT}`, assigned from `startPort`, default 5800), optionally `cmdStop`, `proxy`, `env`, `ttl` (seconds of *idleness*; 0 disables), `unloadTimeout`, `checkEndpoint` (default `/health`, polled until HTTP 200; the server may return JSON with `progress` 0–1, which resets `healthCheckTimeout`), `aliases`, `filters` (`stripParams`, `setParams`), `concurrencyLimit`.
- Three swappable parts: `baseRouter` (process lifecycle), `Scheduler` (currently **FIFO**, a pure state machine in **a single goroutine**), `Swapper` (decides *what to evict*: a static `groupSwapper` or a cost-based `matrixSwapper`). Process states: stopped → starting → ready → stopping. Requests arriving during a swap **wait in the queue until the chosen model is ready**; when limits are exceeded you get HTTP 429.
- **Groups:** the flags `swap` (members are mutually exclusive), `exclusive` (loading a member unloads everything outside the group), `persistent` (cannot be evicted).
- **Matrix:** a DSL with `&`, `|`, parentheses, e.g. `"(g | q) & v"` ⇒ allowed sets `[gemma, voxtral]`, `[qwen, voxtral]`; `evict_costs` are the penalties for reloading; the solver sums the eviction costs of models outside each set and picks the cheapest. A hint from the documentation: groups when "these work together, those swap with each other"; a matrix when "a 70B needs all the GPUs by itself, or several small ones fit together, or a medium LLM plus TTS".
- Extras: a UI with a playground and live logs, Prometheus metrics, an MCP endpoint, peers, `cmd/kubeswap`, `cmd/wol-proxy`.

**Comparison with the built-in llama.cpp router (§6.5):**

| | llama-server router | llama-swap |
|---|---|---|
| What it launches | only `llama-server` | any HTTP server (vLLM, ComfyUI, audio) |
| Eviction | LRU among idle ones, `--models-max` (default 4) | groups (`swap/exclusive/persistent`) or a cost matrix |
| Pinning to GPUs | the notes do not describe such a mechanism *(unverified)* | through `env` per model, e.g. `HIP_VISIBLE_DEVICES` in `cmd` |
| Observability | `/metrics`, `/models/sse` | UI, logs, request inspector, Prometheus (GPU too) |
| Dependency | none, built in | a separate binary, maintained by one person |

Weaknesses of llama-swap: a stateful process manager is a single point of failure; a model swap = a full reload without carrying over the KV (unless the server has its own prompt cache); the most common configuration error is a port mismatch between `cmd` and `proxy`; a matrix lacking a needed combination causes unexpected evictions ("test every combination you want").

**Who is behind it.** Benson Wong (`mostlygeek`, per GitHub Vancouver, with "Tailscale and Elethink" in the company field), one person maintains the project (about 82% of commits), a GitHub Sponsors listing exists; no company and no known funding. See `10-MONEY-AND-PEOPLE.md`.

### Table: when to use what

| Need | Choice | Note |
|---|---|---|
| A production server on 4×R9700 | **upstream llama.cpp** (+ llama-swap) | HIP is a target maintained in the same tree as CUDA (§9) |
| A large MoE on CPU+one card | ik_llama.cpp | quants only for this fork; gfx1201 undocumented |
| Send a model to someone without installation | llamafile | lags behind upstream by weeks |
| Roleplay, images, TTS in one package | KoboldCpp | AGPL; AMD via Vulkan |
| A convenient GUI for backend comparisons | textgen | engine in a child process |
| STT/diffusion/your own model on ggml | whisper.cpp / stable-diffusion.cpp / ggml | no KV/tokenizer in ggml |
| Many models and GPUs behind one address | llama-swap or the llama-server router | see the table above |

---

## 12. Who is behind it (llama.cpp)

ggml.ai was founded in 2023 by Georgi Gerganov; the pre-seed was provided by Nat Friedman and Daniel Gross (`ggml.ai`). On **2026-02-20** Hugging Face announced that ggml and llama.cpp are joining it (the post "GGML and llama.cpp join Hugging Face": authors Georgi Gerganov, Xuan-Son Nguyen, Aleksander Grygier, Lysandre, Victor Mustar, Julien Chaumond). According to the post the team "continues to dedicate 100% of their time" to maintenance, has "full autonomy" on technical matters, and the project is to remain "100% open source and community driven" *(company's own claim)*; the ggml.ai page says outright that the company was acquired by Hugging Face in 2026. **I did not find the terms of the transaction** — treat them as undisclosed. Seven of the twelve largest contributors declare HF as their employer (GitHub profiles, self-declared information); others work for hardware companies (e.g. Jeff Bolz, NVIDIA, Vulkan). Governance is "BDFL plus CODEOWNERS" (maintainers per area: CUDA, Vulkan, Metal, server, etc.), with no foundation; about 17% of commits are Gerganov himself, so the team is broader than in 2023–25, but the project still revolves around a dozen or so people. A consumer layer is emerging: `llama.app` and the applications `Llama-macOS` and `Llama-Windows` (the ggml-org organization) — whether they will be monetized, I could not establish. The AI policy in `AGENTS.md`: AI-generated code only if a human fully understands it; PR descriptions and commit messages written by AI and automated PRs are forbidden. The full discussion: `10-MONEY-AND-PEOPLE.md`.

---

## 13. Gotchas

1. **`-c` is divided by `-np`** if the cache is not unified (`--kv-unified`) — §4.4.
2. **SWA and recurrent models do not "forget"** positions; prompt cache hits depend on checkpoints, which cost RAM — §6.3.
3. **The built-in `--tools`, MCP and `--agent` are unauthenticated code execution** if the port is reachable — do not expose them — §6.7.
4. **`-ngl auto` / `--fit` can change the context size**; in production pin `-c` explicitly. `--fit` does not work with the tensor split at all.
5. **The HIP target must be exactly your `gfx`** (`-DGPU_TARGETS=gfx1201`), otherwise the kernels will not run or will fall back to a fallback path — §9.
6. **`--models-max` in the router defaults to 4** — on 4×32 GB that is probably more than you want to hold at once.
7. **`-sm tensor` is experimental** and for AMD "no guarantees"; requires flash-attn and f16 KV — §8.
8. **The offload threshold of 32** (`GGML_OP_OFFLOAD_MIN_BATCH`): with partially offloaded models prefill depends on `-ub`, decoding does not — §2.6.
9. **The `llama.h` API often breaks**, and versions are build numbers; pin a `bNNNNN` tag, because upstream ships several builds a day, and open issues + PRs total 2,565.
10. **Quants and files are not portable in both directions** between mainline and ik_llama.cpp (IQ_K/KT formats only in the fork).
11. **Context shift** silently loses the beginning of the conversation — §6.4.
12. **Wrapper lag:** llamafile is weeks behind upstream, Ollama pins a specific build (b11669 vs b11741) — a new architecture may not work there yet, even though it is in upstream.
13. **The prompt cache in RAM defaults to 8 GiB** — with several models in router mode remember that each child process has its own.

---

## 14. What this means for the reference setup

**The reference stack:** llama.cpp (HIP, gfx1201) behind llama-swap, 4×32 GB, a 284B MoE in IQ3_XXS.

1. **Pin and build for a specific target.** `-DGGML_HIP=ON -DGPU_TARGETS=gfx1201`; keep the `llama-bench` output in JSONL in the repository, to detect regressions between `bNNNNN` tags.
2. **Choose the split mode for the workload — and measure.** `layer` for many parallel agents and long prompts (in the reference setup: 4 slots × 131k, the fastest prefill ~960 tok/s, but ~23.5 tok/s of generation). `-sm tensor -fa on -ctk f16 -ctv f16` is officially experimental and for AMD "no guarantees" (§8), and yet on the reference 4× R9700 rig with DeepSeek-V4-Flash it **worked and gave a measurable gain**: without a draft 25.2 → 29.1 tok/s, with a DSpark draft 37.9 → 46.2 tok/s, in production ~49–50 tok/s for a single agent *(my measurements, details and conditions in [`../speeding-up-generation/README.md`](../speeding-up-generation/README.md))*. The price: prefill ~700 instead of ~960 tok/s and 2 slots × 98,304 instead of 4 × 131,072. General conclusions: try tensor mode with your own measurement on your model (not all architectures support it — the list is in `docs/multi-gpu.md`), remember that I did not measure quality after switching to tensor mode, and set `-c` by hand (`--fit` does not work). RCCL (`-DGGML_HIP_RCCL=ON`) is off by default — I did not test it.
3. **The prompt cache for agent loops:** keep `--cache-ram` large (default 8 GiB), `--cache-idle-slots` enabled, `--ctx-checkpoints` ≥ 16 for SWA/hybrid models; route sessions to a fixed `id_slot` or rely on slot selection by LCP. Make the unified/per-slot decision based on whether context lengths are very uneven (`--kv-unified`).
4. **Structured output:** use lazy grammars / `response_format` with a JSON schema through the server; for large schemas consider a build with LLGuidance.
5. **Speculative decoding:** the n-gram variants (`--spec-type`) cost nothing (no draft model) and work well with code and repeated tool calls; EAGLE-3/MTP/DFlash only if a matching GGUF draft exists for your model.
6. **MoE on mixed hardware (e.g. a Mac):** `-ot` with a regex keeps experts in RAM; the new `llama_moe_cache` buffers hot experts on the GPU.
7. **The llama-server router or llama-swap?** The built-in router (`--models-dir --models-max`, LRU) is enough with a single GPU group. Stay with llama-swap when you need **pinning models to specific GPUs** (`HIP_VISIBLE_DEVICES` in `cmd`/`env`), groups/matrices, non-llama upstreams, metrics. A natural choice on the reference hardware: an entry "70B dense on all four" (`HIP_VISIBLE_DEVICES=0,1,2,3`, `-sm layer`), next to two 30B MoE models on pairs of cards and a permanently running embeddings/reranker model on a separate piece; eviction costs ≈ load times from disk. Put the shared `--parallel`, `--cache-ram`, `--ctx-checkpoints` into macros in each model's `cmd`; `filters.setParams` forces sampler settings for frameworks that send bad defaults.
8. **Agent tools:** read `server-tools.cpp` and `--tools-runtime docker:` as a pattern for isolated tool execution, but do not expose them.
9. **The Anthropic and Responses endpoints** let you plug a local model into tools written for those APIs without a translating proxy.
10. **On a Mac:** Metal is a full-fledged backend (~33k lines), and the `Llama-macOS` application (4 MB, `brew install --cask llama-app`, server at `localhost:9931/v1`) is the simplest path *(project's own claim)*; MLX is covered by chapter 07.
11. **What I do not know:** performance results on gfx1201 (I measured nothing), the number of scheduler passes, the priority policy in continuous batching, the target of the `ggml-et` backend, or whether `--tools`/MCP are stable enough for production. For comparison with other engines: `09-COMPARISON-AND-CHOICE.md`; datacenter servers (vLLM, SGLang) in `06-SERVING-ENGINES-VLLM-SGLANG.md`; wrappers in `05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md`; quants in `03-QUANTIZATION-AND-FORMATS.md`; people and money in `10-MONEY-AND-PEOPLE.md`.
