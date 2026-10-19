# 08 · Specialists: KTransformers, mistral.rs, MLC and NPU stacks

This chapter describes engines that do not try to be "one program for everything". Each of them exists because the mainstream engine (llama.cpp, vLLM, SGLang) leaves some niche unserved: a model that does not fit in GPU memory; a Rust application that wants an engine inside it; a browser or a phone; an NPU chip in a laptop. After reading it you will be able to answer three questions. First: how the "experts in RAM, attention on the GPU" split really works and how it differs from `-ot` in llama.cpp. Second: when a Rust engine or a "compiled" engine makes sense. Third: which of these ideas touch your 284B MoE model on 4× R9700, and which you can safely skip.

> ⚠️ **I did not run anything here.** The whole chapter is *desk research* and reading source code (repository clones from 19 October 2026, the GitHub API, project documentation). I did not build or measure any of the engines described. Performance numbers come from the projects themselves and are marked *(project's own claim)*. Where I had no evidence, I write "I could not establish".

**Table of contents**

1. [What they have in common: the niche the mainstream leaves](#1-what-they-have-in-common-the-niche-the-mainstream-leaves)
2. [KTransformers in depth](#2-ktransformers-in-depth)
3. [Comparison: hybrid MoE offload (KT, llama.cpp, ik_llama.cpp, ds4)](#3-comparison-hybrid-moe-offload)
4. [mistral.rs](#4-mistralrs)
5. [MLC LLM and WebLLM](#5-mlc-llm-and-webllm)
6. [NPU stacks and vendor stacks](#6-npu-stacks-and-vendor-stacks)
7. [What this means for me](#7-what-this-means-for-me)

A note on sources: GitHub statistics (stars, commits) come from the API as of 19 October 2026. All file references from the code are paths relative to the root of the given repository. The full discussion of the money and people behind the projects is in [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md); here each section has only a short "Who is behind it" paragraph.

Two things I leave to other chapters: Unsloth and the quantization map (including what is really hiding inside the `UD-IQ3_XXS` file) are described in [`03-QUANTIZATION-AND-FORMATS.md`](03-QUANTIZATION-AND-FORMATS.md). The llama.cpp and ik_llama.cpp family (apart from the comparison in section 3) is described in [`04-LLAMA-CPP-AND-THE-GGML-FAMILY.md`](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md), and ds4 in [`07-APPLE-MLX-OMLX-AND-DS4.md`](07-APPLE-MLX-OMLX-AND-DS4.md).

---

## 1. What they have in common: the niche the mainstream leaves

A mainstream engine optimizes for one assumption. **llama.cpp** for "one program, any hardware, any GGUF file". **vLLM and SGLang** for "many parallel users on data-center cards". Each such assumption leaves a gap. The engines in this chapter move into exactly those gaps:

| Engine | The gap it fills | The price it pays |
|---|---|---|
| **KTransformers** | A huge MoE model (hundreds of billions of parameters), little VRAM, a lot of server RAM. | Needs a server CPU with a lot of memory, the GPU path is ready only for NVIDIA, poor scaling to many users. |
| **mistral.rs** | A Rust (or Python) application that wants the engine *inside the process*, with on-the-fly quantization and an agent server in one. | CUDA, Metal and CPU only. One main author. |
| **MLC LLM / WebLLM** | "Compile the model for the device": phone, browser, AMD/Intel/Apple cards from one stack. | Compilation per model per device, slow pace of development, no GGUF. |
| **NPU stacks** (ONNX Runtime GenAI, OpenVINO GenAI, Qualcomm GenieX, AMD Ryzen AI) | NPU chips in laptops and phones, which the main engines either do not support or have supported only recently. | Tied to a single vendor, proprietary model formats, often Windows. |

**A common theme explaining why this matters:** in 2026 the boundaries are blurring. llama.cpp already has the backends `ggml-hexagon` (Qualcomm NPU, 53 thousand lines), `ggml-openvino` (19.6 thousand) and `ggml-webgpu` (21 thousand) in its main tree *(read from the llama.cpp code, build `0ce8cd1`)*. So part of the mainstream's "niches" is already closing. The specialists stay alive where they have an advantage that a general engine will not catch up with in a reasonable time: custom compute kernels for experts on the CPU (KT), built-in quantization and an agent (mistral.rs), a compiler (MLC), vendor support (NPU).

Two observations that will be useful later:

1. **KTransformers itself stopped being a standalone engine.** It kept the CPU kernels and plugged them into SGLang. This is a pattern: the specialist hands serving (API, scheduler, tool calling) over to a mainstream engine and sticks to what it does best.
2. **NPU stacks converge on "llama.cpp plus the vendor's runtime".** Qualcomm GenieX is, inside, a vendored llama.cpp (section 6.3). This says that llama.cpp is today the common denominator, even for companies that have their own engine.

---

## 2. KTransformers in depth

### 2.1 Why it exists at all

A reminder from [`02-HOW-INFERENCE-WORKS.md`](02-HOW-INFERENCE-WORKS.md): in an MoE model (*Mixture of Experts*, **experts**) each token passes through only a few selected experts in each layer. The DeepSeek V4 Flash model has 284B parameters in total, but only 13B active per token *(project's own claim from ds4, model card synopsis in `MODEL_CARD.md`)*. Decoding is limited by memory bandwidth: per token you read only the active 13B, but **all 284B have to be stored somewhere**, because you do not know in advance which experts will be chosen.

An analogy: a library with a small reading room (VRAM) and a large warehouse (RAM). For each chapter of a book you need a few volumes, but which ones you only know after reading the table of contents. More precisely: the expert weights have to be where they can be read quickly, and generation speed depends on what fraction of reads hits the fast memory and what fraction hits the slow one.

KTransformers answers this in a specific way: **the experts stay in the CPU's RAM and are computed there** (not moved to the card), and the card does what it does best: attention, dense layers, the router and selected "hot" experts.

### 2.2 Identity and status as of 19 October 2026

- Repository `kvcache-ai/ktransformers`, **Apache-2.0** license, created 2024-07-26. Languages according to GitHub: Python 7.8 MB, C++ 4.9 MB, CUDA 0.59 MB.
- 19,619 stars, 1,604 forks, about 1,359 commits. Most commits: Atream (245), KMSorSMS (155), Azure-Tang (116), qiyuxinlin (100), ovowei (95).
- Latest release **v0.7.2 (2026-10-15)**, earlier v0.7.1 (2026-09-15) and v0.7.0.post4 (2026-09-13). Last push: 2026-10-19. The project is very active.
- Documentation: README, the `doc/` directory, `kt-kernel/README.md`, an online book https://kvcache-ai.github.io/ktransformers/.

**Who is behind it.** According to the README: the **MADSys lab at Tsinghua University**, the company **Approaching.AI**, the **9#AISoft** organization and the community. The maintainer list in `MAINTAINERS.md` has 11 people: 6 from Tsinghua and 5 from Approaching.AI, so a team, not one person. The `kvcache-ai` GitHub organization describes itself as a collaboration of MADSys with industry partners; the same organization hosts Mooncake, the serving platform for Kimi, developed with Moonshot AI. The Approaching.AI website was unreachable for me, so I **could not establish** the company's funding and revenue. Risks: the project is driven by a research agenda (the release headlines are mostly "day-zero support" for Chinese frontier models and tuning) and depends on the availability of Intel AMX. Details and context: [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

### 2.3 Two generations: the old "framework" and the new `kt-kernel`

This is the most common source of confusion, because tutorials for both circulate online.

**Generation 1 (2024 to mid-2025): a monolithic framework.** KT replaced the `nn.Module` modules from the HuggingFace library with its own operators according to YAML rules (`optimize_rules/*.yaml`, the `--optimize_config_path` flag), and on top of that it had its own server (`ktransformers/server/main.py --backend_type balance_serve`). The description is in `doc/en/AMX.md`.

**Generation 2 (from late autumn 2025): `kt-kernel` as a plugin.** The README (entry of 2025-10-10) mentions integration with SGLang; the roadmap is issue sgl-project/sglang#11425, and the LMSYS blog post is from 2025-10-22. The old code was moved to the `archive/` directory (in the 19 October clone: `archive/ktransformers/` 50.2 thousand lines, `archive/kt-sft/` 74.1 thousand, `archive/csrc/` 28.2 thousand, including the C++ `balance_serve` scheduler). The README says outright: "The original integrated KTransformers framework has been archived".

The living product today is:
- **`kt-kernel`**: a library of MoE kernels on the CPU, in the clone about 73.8 thousand lines in `kt-kernel/operators/` plus a Python layer (35.9 thousand),
- **the SGLang plugin**: on the SGLang side the file `python/sglang/srt/layers/moe/kt_ep_wrapper.py` (393 lines, Apache-2.0 license) already lives in *upstream* SGLang,
- **the SFT path**: fine-tuning MoE models with experts computed on the CPU, integrated with LLaMA-Factory.

A practical conclusion: if you are reading a guide with `--optimize_config_path` and `balance_serve`, it describes the **archived** generation.

### 2.4 How a request flows (kt-kernel in SGLang)

I verified everything below in the code: `kt-kernel/python/experts_base.py` (948 lines), `kt-kernel/python/experts.py` (466 lines) and `kt_ep_wrapper.py` in SGLang.

```
            GPU (NVIDIA)                              CPU + host RAM (several NUMA nodes)
  ┌───────────────────────────────┐            ┌──────────────────────────────────────────┐
  │ embedding, norm, attention    │            │  NUMA node 0          NUMA node 1        │
  │ (KV cache stays here)         │            │  ┌──────────────┐     ┌──────────────┐   │
  │ dense layers, router          │            │  │ slice of      │     │ slice of      │  │
  │ "hot" experts (mask)          │            │  │ EACH          │     │ EACH          │  │
  └──────────────┬────────────────┘            │  │ expert        │     │ expert        │  │
                 │ router picked top-k         │  │ (intermediate │     │ (intermediate │  │
                 │ experts                     │  │  dim. split)  │     │  dim. split)  │  │
                 │                             │  └──────┬───────┘     └──────┬───────┘   │
   hidden_states │ topk_ids, topk_weights      │         │ AMX / AVX512       │           │
   (D2H copy to  │ ─────────────────────────►  │         └────────┬───────────┘           │
   pinned        │                             │      partial results ──► reduction       │
   memory)       │                             │                  │                       │
                 │ ◄─────────────────────────  │                  ▼                       │
                 │   CPU experts' result       └──────────────────────────────────────────┘
                 ▼
     added to the GPU experts' result → onward, next layer

  Deferral: the experts with the lowest routing weights are NOT awaited in this layer;
  their result arrives only at the input of the NEXT layer, when the GPU is already computing its attention.
```

The steps, in order:

1. **SGLang computes in its own way** the attention, normalizations, the router and the experts resident on the GPU (with any quantization method; the wrapper is generic for "any MoE quantization method").
2. **Handoff to the CPU.** After routing, `kt_ep_wrapper` hands `(hidden_states, topk_ids, topk_weights)` to `KTMoEWrapper.submit_forward(...)`. The function `_prepare_forward_cpu_buffers` copies the data from the GPU into **pinned**, double-buffered CPU buffers (`KExpertsCPUBuffer`, `current_slot`/`next_slot`) and masks the IDs of the experts resident on the GPU (`gpu_experts_mask`) so they are not computed twice.
3. **Synchronization without busy waiting.** `CPUInfer.submit_with_cuda_stream(cuda_stream, task)` inserts the CPU task as a *host callback* on the CUDA stream. The ordering relative to GPU work is guaranteed by the stream, not by a loop waiting on the CPU; `sync_forward` later does the corresponding `sync_with_cuda_stream`. On Ascend NPUs this mechanism can be unreliable, so the code has a synchronous fallback path there (long comments at the top of `experts_base.py`).
4. **Expert deferral** (*expert deferral*; parameter `max_deferred_experts_per_token`, function `select_deferred_experts`). The least important (lowest routing weights) of the selected experts are not awaited in the current layer. They are computed as a second task, and their result is added to the input of the *next* layer. Thanks to this, CPU work overlaps with the next layer's attention on the GPU. According to the paper this raises CPU utilization from "usually below 75%" to nearly 100%, gives up to 1.45× throughput, and accuracy stays within 0.5% *(project's own claim, MADSys publication page)*. Note: deferral *changes the computation* (the result of the weaker experts arrives slightly later), so it is not a pure optimization without consequences; hence the declared accuracy tolerance.
5. **NUMA split.** The class `TP_MOE_Common<T>` (`kt-kernel/operators/moe-tp.hpp`) splits the *intermediate dimension of each expert* across NUMA sub-pools (`tp_count = pool->config.subpool_count`; the code throws an exception if `intermediate_size % tp_count != 0`). Each NUMA node keeps in its local memory its own slice of **every** expert, computes its partial result, and the results are reduced. The flag `--kt-threadpool-count` means the number of NUMA nodes. This means each node reads only local memory. In MoE decoding, which is limited by DRAM bandwidth, this is the crux.
6. **Threads.** `InNumaPool`/`WorkerPool` (`kt-kernel/cpu_backend/worker_pool.{h,cpp}`, 507 lines in the `.cpp`) pin one thread per *physical* core through `hwloc` (`hwloc_set_membind` with strict binding, thread names `numa_<id>_t_<n>`) and use a *work stealing* loop with an atomic counter (`do_work_stealing_job`). The documentation warns repeatedly: count physical cores, not hardware threads (*hyperthreading*).
7. **AMX kernels.** `kt-kernel/operators/amx/la/amx_kernels.hpp` contains hand-written loops over tiles (`_tile_loadd`, `_tile_dpbssd` for INT8, `_tile_dpbf16ps` for BF16) on tiles 0–7 (3 A tiles × 1 B tile → 3 C tiles). The weights are repacked into an AMX-friendly layout already at load time (`pack.hpp`, `amx_buffers.hpp`). The LMSYS blog gives "up to 21.3 TFLOPS" of sustained AMX kernel performance *(project's own claim)*.

**Expert placement** is a logical mask per layer (`generate_gpu_experts_masks`). Strategies: `uniform`, `frequency` (requires a `.pt` statistics file from the flag `--record-kt-gpu-expert-distribution`), `front-loading`, `random`, and a *dynamic update* during prefill (`--kt-gpu-prefill-token-threshold`) *(documentation `doc/en/kt-kernel/experts-sched-Tutorial.md`)*.

**Prefill (reading the prompt).** With long prompts the CPU is the bottleneck, so the project lets prefill chunks (`chunked_prefill_size`, an example of 25600 in a comment in the wrapper) use the GPU for experts, with weights streamed layer by layer (`fp8_layerwise_transport.cpp`, a file of 31.6 kB). I checked that the file exists; I **did not trace** the mechanism itself *(unverified)*.

### 2.5 What KT runs: hardware and formats

On the CPU side (source: `kt-kernel/README.md` and `doc/en/kt-kernel/kt-kernel_intro.md`; the list of methods is literally the set `INFERENCE_METHODS` in `kt-kernel/python/experts.py`):

| Method (`--kt-method`) | CPU requirement | Weight format |
|---|---|---|
| `AMXINT4`, `AMXINT8` | Intel AMX (from Sapphire Rapids) | converted INT4/INT8 (script `convert_cpu_weights.py`) |
| `RAWINT4`, `FP8`, `BF16`, `FP8_PERCHANNEL` ("native precision") | AVX512 (VNNI/BF16 variants), e.g. Ice Lake, Zen 4 | the checkpoint's own FP8/BF16/INT4, shared with the GPU path |
| `LLAMAFILE` | AVX2+ (Haswell 2013 / Zen+) | **GGUF** (Q4_K, Q4_K_M, Q5_K and others) through the bundled llamafile kernels |
| `GPTQ_INT4`, `MXFP4`, `NVFP4`, `MXFP8`, `MOE_INT4/8` | AVX2 / AVX512-VNNI | GPTQ, OCP MX, NVFP4 (ModelOpt) |
| AMD processors | BLIS INT8 path (`doc/en/kt-kernel/amd_blis.md`) | INT8 |
| ARM | KML (built from source) | I could not establish |

Important for you: **the GGUF format works only through the `LLAMAFILE` method**, that is, the slower AVX2 path, not AMX. Everything else (including AMX) uses safetensors formats. A historical curiosity: the README entry of 2025-03-05 "Support unsloth 1.58/2.51 bits weights and IQ1_S/FP8 hybrid weights" shows that Unsloth's dynamic GGUFs for DeepSeek-R1 were one of KT's early use cases.

On the GPU side:

- **The prebuilt wheel (`pip install kt-kernel`) supports NVIDIA only: SM 80/86/89/90** (A100, RTX 30/40, H100). V100/T4/GTX are not supported. Linux x86-64, Python 3.10–3.12, CUDA 12+ *(documentation `kt-kernel_intro.md`)*.
- `kt-kernel/CMakeLists.txt` has mutually exclusive build options `KTRANSFORMERS_USE_CUDA | MUSA | ROCM | MACA | SYCL | ASCEND_NPU` (lines 16–21 and 54). So ROCm, Moore Threads, MetaX, Intel XPU (SYCL XMX kernels for GPTQ-INT4, 9 files in `operators/sycl/`) and Huawei Ascend are targets **built from source**. The abstraction layer is `cpu_backend/vendors/{cuda,hip,musa,maca,ascend_npu}.h`.
- The old ROCm documentation (`doc/en/ROCm.md`, marked "Beta") concerns the **old framework**, tested on "EPYC 9274F + Radeon 7900 XTX" with PyTorch for ROCm 6.2.4. **There is not a word about gfx1201 or R9700 in the repository** (I checked with grep over the documents; I built nothing).

⚠️ **For your machine:** the KT path for AMD cards is "compile it yourself and see", with no declared support for RDNA4. Treat it as an **architecture you can learn from**, not as a tool to deploy on the R9700.

### 2.6 What KT needs: server hardware

The documentation gives a minimum of **256 GB** of DDR5 memory, tested on **512 GB** (README and `doc/`). The target user is a workstation or server with a lot of RAM and one or several NVIDIA cards, at low concurrency (one user or a small team). The paper itself says the project "targets scenarios with fewer concurrent requests, where the advantage is CPU memory capacity" *(project's own claim, MADSys publication page)*.

### 2.7 Performance (all of this is the project's own data; I never mix configurations)

- **Paper (SOSP 2025):** 4.62–19.74× faster prefill and 1.25–4.09× faster decoding versus "existing alternatives", plus up to 1.45× from expert deferral. In what I managed to download, the competing baselines are **not named**; I suspect llama.cpp and Fiddler, but that is *(unverified)*. DOI 10.1145/3731569.3764843 taken from the BibTeX in the README (the ACM page returned 403).
- **README:** DeepSeek-R1-0528 (FP8), 8× L20 + Xeon Gold 6454S, concurrency 8: **227.85 tok/s total, 87.58 tok/s on output**. The same numbers in the LMSYS blog (ShareGPT).
- **LMSYS blog:** two sockets of Xeon Platinum 8452Y (72 cores, 2 TB DDR5) + A100 40 GB in the single-card variant: "up to 20×" prefill and "up to 4×" decoding. With 8× L20 the advantage over a single card is 26% at concurrency 1 and 264% at 8.
- **Placement table (the project's own):** Qwen3-Next-80B-A3B-Instruct-FP8, 4× RTX 4090, Xeon Gold 6454S, TP=4, ShareGPT, tok/s:

| Fraction of experts on the GPU | Result (tok/s) |
|---|---|
| 0% (all on CPU) | 52.7–54.2 (all strategies) |
| 50% | random 70.4; uniform 65.3; front 73.7; by frequency 76.2; dynamic 81.2 |
| 100% | about 112–114 |

The conclusion that follows (from the project's data): throughput grows roughly linearly with the fraction of experts you manage to keep in VRAM, and placement by *usage frequency* beats uniform placement. This is the most valuable lesson from all of KT, and it can be (roughly) reproduced in llama.cpp, as discussed in section 7.

Limitations: GPU only NVIDIA in the prebuilt wheel; server RAM required; poor scaling with concurrency (the experts' CPU computation is shared); every new model family requires "day-zero" work, hence the long list of per-model tutorials.

### 2.8 Fine-tuning (SFT) in brief

`kt-kernel/python/sft` (14.4 thousand lines of Python) allows fine-tuning MoE models with LoRA and (since 2026-07) full-parameter fine-tuning in BF16, with experts computed on the CPU. It is integrated with LLaMA-Factory (YAML in `examples/ktransformers/...`). The README claims 6–12× speedups over ZeRO-Offload "in the tested MoE SFT tasks" and about 3.7 it/s for DeepSeek-V3/R1 on 4× RTX 4090 *(project's own claim)*. A second work, "KTransformers-FineTune (KT-FT)", is an author preprint from 2026-10-08. A curiosity: LLaMA-Factory lists KT together with Unsloth in its "Practical tricks" section. This thread is outside our main topic (running models), so I stop here.

### 2.9 Offline operation

In `kt-kernel` (py/cpp/hpp) I found no traces of telemetry (grep returned an empty result). Models have to be downloaded once from Hugging Face, wheels from PyPI; after that everything works offline. I did not audit SGLang itself here.

### Check it yourself: KT

> **Check it yourself 1: the list of methods and build options** *(not run by me; I read these files in the clone `kvcache-ai/ktransformers@a694e718`)*
> ```bash
> git clone --depth 1 https://github.com/kvcache-ai/ktransformers && cd ktransformers
> grep -n 'INFERENCE_METHODS' -A12 kt-kernel/python/experts.py
> grep -n 'KTRANSFORMERS_USE' kt-kernel/CMakeLists.txt
> ```
> You should see the set of method names from the table above and the mutually exclusive CUDA/MUSA/ROCM/MACA/SYCL/ASCEND_NPU options. Make sure yourself that nothing in `doc/` mentions gfx1201: `grep -rn -i 'gfx1201\|R9700' doc kt-kernel`.

> **Check it yourself 2: expert deferral and the hook in SGLang** *(not run by me)*
> In the SGLang repository open `python/sglang/srt/layers/moe/kt_ep_wrapper.py` and find `submit_forward`. Then in `kt-kernel/python/experts_base.py` look for `select_deferred_experts` and `_layer_has_pending_deferred`. This shows that the result of the deferred experts is added to the input of the next layer.

---

## 3. Comparison: hybrid MoE offload

Now that you know how KT works, let us set five approaches to the same problem side by side: **an MoE model larger than VRAM; part of the weights has to live somewhere else**. The approaches below differ in *where the cold weights live*, *at what level of granularity you decide on their placement*, and *who computes them*.

### 3.1 The four questions I compare by

1. **Where do the "cold" experts live?** (Host RAM or SSD.)
2. **What is the granularity of the decision?** (A whole layer tensor, or a single expert.)
3. **Who computes the experts that are not on the GPU?** (The CPU, or the GPU after loading.)
4. **Is the latency hidden?** (Overlapping work.)

### 3.2 Table of mechanisms

| | **llama.cpp `-ot` / `--cpu-moe` / `--n-cpu-moe`** | **llama.cpp `--moe-cache-mib`** | **ik_llama.cpp** | **KTransformers (kt-kernel)** | **ds4, streaming from SSD** |
|---|---|---|---|---|---|
| Where the cold experts live | Host RAM | Host RAM (+ an expert buffer on the GPU) | Host RAM | Host RAM, NUMA sub-pools | **GGUF file on SSD** + a limited in-memory expert cache |
| Granularity | **layer tensor**: in GGUF each layer has one 3-D tensor per projection (`blk.N.ffn_{gate,up,down}_exps.weight`), so you place *all of a layer's experts at once* | **single expert**: each layer has a slot map in host memory; missing experts are loaded by the scheduler's copy callback | like llama.cpp (`-ot`); plus its own expert cache (`Implement moe cache #2644`, 2026-10-12) and `--prefetch-experts` | **single expert**: a logical mask per layer (`generate_gpu_experts_masks`) | **single expert** in the cache; a starting "hot list" compiled into the binary |
| Who computes the experts outside the GPU | `ggml-cpu`, synchronously in the graph | the cached experts are computed by the card; those outside the cache arrive through a copy (see below) | CPU: its own kernels (`ggml/src/iqk/iqk_mul_mat*.cpp`) | CPU: its own AMX/AVX512 kernels with NUMA split | accelerator (Metal/CUDA/ROCm) after loading the expert (*follows from the description in the ds4 documentation*) |
| Hiding latency | none: the CPU computation is a step in the graph | the expert copy is invoked from the scheduler callback; I could not establish the degree of overlap with computation | I did not read the scheduler code | host callback on the CUDA stream + expert deferral | loading missing experts "hidden behind" the computation of shared experts (ds4 AGENT.md) |
| NUMA | I could not establish from the notes | I could not establish | I could not establish | yes, a slice of each expert in the node's local memory | not applicable |
| Format | GGUF | GGUF | GGUF; files with IQ_K/KT quants load **only** in ik_llama.cpp | safetensors (FP8/BF16/INT4/GPTQ/MXFP4/NVFP4), GGUF only through `LLAMAFILE` | special GGUF with asymmetric quantization, a narrow set of models |

Sources of the facts: llama.cpp, flags from `common/arg.cpp` lines 2758–2793 and `src/llama-moe-cache.h` in the `0ce8cd1` tree (header comment: "keeps recently and repeatedly used experts of host-resident MoE layers in a device buffer"); ik_llama.cpp from the README and commit history (I did not read the code); KT from section 2; ds4 from `docs/SSD_STREAMING.md` and `ds4_ssd.c`.

What happens in llama.cpp with experts outside the GPU on a large batch of tokens (**the *op-offload* rule**, `ggml-backend.cpp`, `ggml-cuda.cu` lines 180–183 and 6011–6015): if a weight lives in host memory and the scheduler has `op_offload` enabled, any backend with a higher priority may take over the operation when `offload_op` agrees. For CUDA/HIP the condition is `get_op_batch_size(op) >= op_offload_min_batch_size`, by default **32** (environment variable `GGML_OP_OFFLOAD_MIN_BATCH`). The effect: **prefill** on a partially offloaded model speeds up as `-ub` grows, because the weights are "streamed" to the GPU, while generation (batch of 1) stays on the CPU. KT has the opposite philosophy for prefill: AMX on the CPU is meant to be fast enough that prefill does not need to move weights (and with long prompts part of the work comes back to the GPU anyway, see 2.4).

### 3.3 Practical table: what this means for you

| | `-ot` / `--n-cpu-moe` | `--moe-cache-mib` | ik_llama.cpp | KTransformers | ds4 |
|---|---|---|---|---|---|
| AMD GPU (RDNA4, gfx1201) | works (HIP/ROCm backend, your current engine) | same backend; operation on your cards has not been checked | HIP exists but is secondary; no declaration for gfx1201 | build from source only, no declaration for gfx1201 | ROCm targets gfx1151 (Strix Halo); gfx1201 only through third-party PRs |
| What you need | host RAM | host RAM + some VRAM for the cache | host RAM | server CPU with AMX/AVX512, 256+ GB RAM, an NVIDIA card | a fast SSD and memory for the cache |
| Quick assessment | simplest, mature | new (described in the header, flag off by default) | fast CPU kernels according to the author, risk of a single maintainer and of diverging from upstream | most sophisticated, heaviest to deploy | most "frugal" (an SSD is enough), but slowest and narrowest |
| Throughput (project's own claim) | no numbers in my notes | no numbers | no independent benchmarks; only the author's reports | table in 2.7 | M5 Max 128 GB: 11.9–19.3 tok/s decoding on 145–178 GiB models; one R9700 32 GB with SSD: 4.70 tok/s generation |

Notes on the last row: the ds4 numbers come from its documentation `docs/SSD_STREAMING.md` (measurements of 2026-09-06 on an M5 Max 128 GB, automatic cache, a single run) and from PR #558 (2026-07-13), where the PR author, on **one R9700 32 GB** (Ryzen 9 9950X3D, 128 GB DDR5, ROCm 7.2.2), ran V4 Flash Q2 (about 81 GB) with SSD streaming and, after working around the hard-coded 16 GiB VRAM reserve, got 6.33 tok/s prefill and 4.70 tok/s generation *(PR author's data)*. These are the **only** data from gfx1201 cards in this comparison, and they must not be compared with the KT table (different model, different hardware, different metric).

### 3.4 Honest conclusions from the comparison

1. **Granularity matters.** `-ot` in llama.cpp makes the decision at the level of a layer tensor, so you cannot express "keep the 20 most frequent experts of layer 7 on the GPU". KT, `--moe-cache-mib` and ds4 work at the level of a single expert. This is the main conceptual difference.
2. **Who computes is a separate question.** KT invests in *computing on the CPU* (AMX/NUMA). The caches in llama.cpp and ds4 take a different route: *move the expert to where the fast accelerator is*. The first route wins when the CPU has strong matrix units and many memory channels. The second, when the link (PCIe, SSD) is relatively fast and the expert usage patterns are repeatable.
3. **None of this is "free".** Expert deferral in KT changes the computation. The hot list in ds4 is generated from profiling specific models. The cache in llama.cpp and ik_llama.cpp is fresh (ik_llama.cpp: 2026-10-12), so it has no bug history yet.
4. **ik_llama.cpp is a separate story.** Its README says the repository started as a llama.cpp fork in June 2024 and was **last synchronized with upstream in August 2024**. Models that appeared later are ported by hand. For hybrid MoE the README warns against using `-rtr` (runtime repacking) with experts on the CPU. More about the fork, friction with upstream and the license: [`04-LLAMA-CPP-AND-THE-GGML-FAMILY.md`](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md).

### Check it yourself: the comparison

> **Check it yourself 3: offload flags in llama.cpp** *(I ran the sed from these lines on a copy on my machine; the grep itself I did not)*
> In the llama.cpp tree (build `0ce8cd1`):
> ```bash
> grep -n -E 'override-tensor|cpu-moe|moe-cache-mib|n-cpu-ffn' common/arg.cpp
> sed -n 1,20p src/llama-moe-cache.h
> ```
> In `arg.cpp` you will see `-ot`, `-cmoe/--cpu-moe`, `-ncmoe/--n-cpu-moe`, `--moe-cache-mib` ("default: 0, disabled") and `-ncffn`. The header `llama-moe-cache.h` describes the cache in one sentence in a comment.
>
> **Check on your own machine too:** `llama-server --help | grep -i -E 'moe|override-tensor'`. If your build is older than `0ce8cd1`, the `--moe-cache-mib` flag may be missing.

---

## 4. mistral.rs

**In one sentence:** an inference engine written in Rust (a library + a server compatible with OpenAI and Anthropic + a Python SDK), built on Hugging Face's Candle tensor library, with its own quantization (ISQ/UQFF), PagedAttention and a built-in agent loop; **CUDA, Metal and CPU only**.

⚠️ **Most important for you, up front:** mistral.rs has **no ROCm or Vulkan backend at all**. A grep over all `.rs`, `.toml`, `.md`, `.mdx` files in the clone finds no occurrence of "rocm" or "vulkan". You will not run it on your R9700s.

### 4.1 Identity

- `EricLBuehler/mistral.rs`, **MIT** license, created 2024-02-26, Rust. Workspace version **0.9.5 of 2026-10-19**; earlier 0.9.4 (2026-09-24) and 0.9.3 (2026-09-07). Minimum Rust version: 1.94.
- 7,759 stars, 738 forks, about 3,486 commits. Most commits: EricLBuehler 3,073, lucasavila00 125, LLukas22 54.
- The README states: "mistral.rs is not affiliated with Mistral AI". Documentation: https://docs.mistralrs.dev/.

**Who is behind it.** It is maintained by one person, **Eric Buehler**. On their GitHub profile the company listed is `@huggingface`, and the endpoint `orgs/huggingface/members/EricLBuehler` returns 204 (meaning they are a public member of the organization). I did not check their position, so the strongest thing I can say is "affiliated with Hugging Face". They are also the fourth author of Candle (53 commits). **Funding, company, sponsors: I found none** (no `FUNDING.yml`, no sponsors section in the README). **The single-person factor** (*bus factor*): in the 90 days to 2026-10-19, as many as 75 of 82 commits (excluding bots) were theirs. The MIT license allows a fork, but not a painless takeover of a 550-thousand-line project. More in [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

### 4.2 Why it exists

One engine for text, images, video, audio input, speech output, image generation and embeddings, with quantization solved *inside* the engine: you load any checkpoint from Hugging Face and quantize on the fly. Target user: a builder of Rust applications (the `mistralrs` crate), a Python user (`pip install mistralrs`) and someone on **NVIDIA or Apple Silicon**. What it does not try to be: an engine compatible with all GGUF files like llama.cpp, an engine for AMD/Intel, or a distributed serving system like vLLM.

### 4.3 Features

- Models: "45+ architectures" *(project's own claim)*, automatic detection of the architecture, weight format and chat template. LoRA and X-LoRA with adapter choice per request, AnyMoE, speculative decoding (`mistralrs-core/src/speculative`, 12.7 thousand lines).
- API: OpenAI-compatible (`/v1`), **Anthropic-compatible (`/v1/messages`)**, a built-in `/ui` interface, Prometheus metrics `/metrics`, loading and unloading of multiple models at runtime.
- **Agent features:** tool calling with grammar and strict-schema enforcement (llguidance, `pipeline/llg.rs`), a **server-side agent loop** (`engine/agentic_loop.rs`, 1,583 lines, and `tool_dispatch.rs`), persistent Python sessions and a shell sandbox (`mistralrs-code-exec` 3.2 thousand lines, `mistralrs-sandbox` 1.7 thousand), web search with reranking, OpenAI-style "Skills" and an **MCP client** (`mistralrs-mcp`, 3.2 thousand lines) over Process / HTTP(+SSE) / WebSocket transports, with a bearer token and tool-name prefixes.
- CLI: `mistralrs run | serve | bench | tune | doctor`. The `tune` command "recommends quantization and device mapping" for your hardware.

### 4.4 Hardware and formats

- Cargo features in `mistralrs-core`: `cuda`, `cudnn`, `cutile`, `flash-attn`, `flash-attn-v3`, `metal`, `accelerate`, `mkl`, `nccl`, `ring`. No ROCm/HIP, Vulkan, SYCL or NPU. It inherits this from Candle (CPU, CUDA, Metal, WASM; there is no ROCm in the Candle README or tree).
- Formats: safetensors from HF, **GGUF** (`mistralrs-core/src/gguf`, 14.9 thousand lines; the README says "2–8 bits"), the older GGML, **UQFF** (*Universal Quantized File Format*, based on safetensors, metadata `uqff.version.*`, currently 1.2.0), as well as pre-quantized GPTQ, AWQ, HQQ, FP8, bitsandbytes and MXFP4.
- **ISQ** (*in-situ quantization*): the enum `IsqType` in `mistralrs-quant/src/lib.rs` (line 972) contains `Q4_0`…`Q8_1`, `Q2K`…`Q8K`, `HQQ8/4`, `F8E4M3`, `AFQ8/6/4/3/2`, `F8Q8`, `MXFP4`. The function `IsqBits::{Two..Eight}.resolve(device)` turns "N-bit" into **AFQ\* on Metal** (MLX-style group affine quantization) and **Q\*K (the ggml k-quant layout) on CUDA/CPU**. This is an interesting pattern: one "4 bits" knob, and the type depends on the platform. The ISQ types **do not include IQ quants** (i-quants), although the GGUF path may be able to read them (I did not check completeness). It also supports an importance matrix (`imatrix.rs`).

### 4.5 Architecture (clone `EricLBuehler/mistral.rs@465191d0`, 2026-10-19)

**Size.** About 550 thousand lines of Rust in the workspace, so more than llama.cpp's `src/` alone, because every model architecture is written by hand in Rust (in llama.cpp these are ggml graph builders). Largest directories: `mistralrs-core` 347.5 thousand (including `vision_models` 85.3 thousand, `pipeline` 62.8 thousand, `models` 25.0 thousand, `paged_attention` 22.6 thousand, `cuda` 17.6 thousand, `gguf` 14.9 thousand, `speculative` 12.7 thousand, `engine` 8.6 thousand, `scheduler` 1.0 thousand), `mistralrs-quant` 109.7 thousand lines of Rust plus about 63 thousand lines of CUDA/Metal/C kernels.

**Dependency on Candle.** `Cargo.toml` pins `candle-core/-nn/-flash-attn-v3/-metal-kernels` to a **git revision of upstream `huggingface/candle`** (`rev = 66a8cf18…`, version 0.11.0), not to a private fork. Candle 0.11.0 is the newest tag; `candle-core` has 56 thousand lines, `candle-transformers` (reference model ports) 83 thousand. mistral.rs adds: its own matrix multiplications for quantized weights, PagedAttention, FlashInfer integration, decoding with CUDA graphs, NCCL and "ring" distribution, and cuTile FP8 kernels (they require NVIDIA's `tileiras` tool).

**Request flow:** HTTP (axum 0.8, `mistralrs-server-core`) → the `MistralRs` handle → the `Engine` task (`engine/mod.rs`, 2,525 lines; the main loop `'lp: loop` in `Engine::run`, around line 1119). The engine (1) drains the request channel (`add_request.rs`, 1,242 lines: tokenization, template, multimodal features, prefix cache lookup, admission control in `admission.rs`), (2) calls `scheduler.schedule(...)` (around line 1414), (3) executes a **pipeline step** (`Pipeline::step`) for prefill or decoding, (4) samples (`sampler.rs`), streams tokens and handles tools or the agent loop. The pipelines are per modality: `normal.rs`, `gguf.rs`, `ggml.rs`, `multimodal.rs`, `diffusion.rs`, `speech.rs`, `embedding.rs`, `auto.rs`.

**Scheduler** (`scheduler/mod.rs`): two implementations. `DefaultScheduler` (FCFS with fixed buckets) and `PagedAttentionScheduler` (`paged_attention/scheduler.rs`; continuous batching with preemption, `max_num_seqs`, `max_num_batched_tokens` by default **4096**, `max_prefill_chunk_tokens` **512**, `max_decode_steps_before_prefill` **8**). Chunked prefill is interleaved with decoding using these knobs.

**KV cache:** PagedAttention = a block pool (`block_pool.rs`), block hashing for the prefix cache, also multimodal (`block_hash.rs`, `mm_prefix.rs`), and a separate pool for sliding-window layers (`windowed_pool.rs`). The CUDA kernels in `mistralrs-paged-attn/src/cuda` have the namespace `vllm::` in their sources, meaning they were ported from vLLM. **PagedAttention works only on CUDA and Metal** (README); the CPU path has a plain cache (`kv_cache/`).

**ISQ flow** (`pipeline/isq.rs`, `isq_flow/`): weights are loaded layer by layer in the original type, quantized on the target device (or CPU) as they arrive. Design assumption: "no separate conversion step". Peak memory use is therefore supposed to be on the order of one layer plus the sum of the quantized ones *(memory claim unverified)*. UQFF saves the result so that the cost of quantization is paid once.

**Five design decisions:**
1. Rust + Candle: memory safety, a single executable, easy embedding.
2. Quantization as an engine feature, not an ecosystem of file formats.
3. Its own server with agent tools (tools, MCP, sandbox), instead of leaving this to clients.
4. Platform-dependent quantization types (AFQ on Metal, k-quants on CUDA/CPU) behind one knob.
5. Mainly one process and one node (NCCL/ring for multiple cards).

### 4.6 Performance

The only numbers are the README's own benchmark (version 0.8.2): Gemma 4 E4B on a **B200**, Q8 prefill 27,705.6 tok/s versus 11,992.4 for llama.cpp; BF16 prefill 43,547.8 versus 39,431.2 for vLLM; decoding 202.6 versus 196.2 tok/s *(project's own claim)*. This is one data-center GPU class and one small model, so it is not representative for consumer or AMD cards. I found no independent measurements. Things affecting latency: decoding with CUDA graphs, FlashAttention V2/V3, FlashInfer, the prefix cache.

### 4.7 Strengths and weaknesses (relative to llama.cpp)

**Strengths:** one engine reads HF checkpoints *and* GGUF; ISQ means "download any model and run it in 4 bits" without conversion; embeddable SDKs in Rust and Python; OpenAI and Anthropic APIs plus a built-in agent loop and MCP; PagedAttention with continuous batching (the llama.cpp server has slot-based batching, but not KV paging in the vLLM sense) in one binary.

**Weaknesses:** no AMD/Intel/Vulkan (disqualifying on your R9700s); roughly 90% of commits from one person; model coverage and numerical parity chase upstream through manual porting; less battle-tested (7.8 thousand stars versus over 100 thousand for llama.cpp, *the llama.cpp value is unverified in my notes*).

**When does a Rust engine make sense?** When you ship a product written in Rust and want in-process inference without a C++ build chain and FFI. When memory-safe processing of untrusted model files and tool execution matters. And when you are on NVIDIA or Apple Silicon. When you need Vulkan/ROCm/Intel or the largest GGUF ecosystem, you take llama.cpp.

### 4.8 Offline operation

No telemetry code (grep over `.rs`/`.toml` finds only hits in server comments). It respects `HF_HUB_OFFLINE` (`pipeline/hf.rs:26`, `lib.rs:170`). `mistralrs doctor` checks CUDA/Metal and connectivity to HF. The install script downloads files from mistralrs.dev, and web search and MCP/remote fetching (`remote_fetch.rs`) reach outside if you enable them.

### 4.9 Candle in a few sentences

`huggingface/candle`: Apache-2.0 (MIT and Apache license files), 21.2 thousand stars, maintained by Hugging Face. The original author, **Laurent Mazare** (1,603 commits), now lists "Co-founder Kyutai & Gradium" in their profile; today the project is carried by, among others, Nicolas Patry (275 commits) and **Ivar Flakstad** (126). In the 3 months to 2026-10-19 there were about 40 commits there (dependabot 12, ivarflakstad 10, EricLBuehler 7). Conclusion: Candle is alive, but at low intensity, and depends on HF. mistral.rs tracks a git revision instead of crates.io releases.

### 4.10 What to take from this for your own applications

- **The `IsqBits → platform-dependent type` pattern** and the `tune` command (hardware → quantization + device map) are good UX ideas for your own local-model launcher.
- **The agent loop and MCP client inside the engine** are an alternative architecture to "the client runs the loop". Consider whether tool execution belongs to the engine (latency, reuse of the prefix cache between tool turns) or to your orchestrator (security, observability).
- **On Macs:** it is a credible second Metal engine next to MLX (the AFQ quants are in MLX's affine style). Measure on your own model before you trust the README.

### Check it yourself: mistral.rs

> **Check it yourself 4: no ROCm and Vulkan** *(I did not run this line; I established the "empty" result with the same grep on my clone)*
> ```bash
> git clone --depth 1 https://github.com/EricLBuehler/mistral.rs && cd mistral.rs
> grep -rniE 'rocm|vulkan' --include='*.rs' --include='*.toml' --include='*.md' --include='*.mdx' . | head
> grep -n -A12 '^\[features\]' mistralrs-core/Cargo.toml
> ```
> The first command should return nothing, the second will show the features `cuda`, `metal`, `mkl` and the rest of the list in 4.4. You will find the scheduler constants in `mistralrs-core/src/scheduler/mod.rs` (search for `4096`, `512`).

---

## 5. MLC LLM and WebLLM

### 5.1 The idea: compiling the model instead of an "interpreter"

An engine like llama.cpp is a kind of *interpreter*: one program knows many architectures and for every token walks the graph of operations, calling ready-made kernels for your backend. **MLC LLM** ("Universal LLM Deployment Engine with ML Compilation", which is how the repository description reads) goes another way: it **compiles** the model together with the choice of kernels for a specific device. The result is a library (a `.so`/`.dylib`/`.dll`/`.tar`/`.wasm` file) plus weights. The same model can be run this way through CUDA, ROCm, Vulkan, Metal, OpenCL, WebGPU, on iOS and Android.

An analogy: instead of an interpreter who translates a book into various languages on the fly, you print a separate edition of the book for each country. Faster reading, but separate work for each edition. Precisely: compilation per model *and* per device is both the source of portability and the main friction.

### 5.2 What the compilation flow looks like

Three steps (documentation `compilation/compile_models.rst`, https://llm.mlc.ai):

1. **`convert_weight`**: quantizing the weights to the MLC format.
2. **`gen_config`**: writing `mlc-chat-config.json`.
3. **`compile`**: Apache TVM lowers the program (Relax/TIR) to a model library for the chosen target.

Models are defined **in Python** using the `nn.Module` frontend from TVM (`python/mlc_llm/model/<arch>/`, about 29 thousand lines; instructions in `docs/compilation/define_new_models.rst`). The model directory shows, among others, Qwen3.5, Gemma 4, Ministral3, Llama 4 and DeepSeek-V2, so the project keeps up with new architectures with a delay.

The `QUANTIZATION` registry in `python/mlc_llm/quantization/quantization.py` contains, among others, `q0f16/q0bf16/q0f32` (no quantization), `q3f16_0/_1`, `q4f16_0/_1/_2`, `q4bf16_*`, `q4f32_1` (group quantization), `q4f16_autoawq`, `q4f16_ft` and FP8 and block-scaled variants. The name encodes the number of bits, the activation type and the variant. **MLC does not read GGUF.** That means the whole `UD-*` set from Hugging Face is useless for it; you have to convert from the original weights.

### 5.3 Runtime and dependencies

The serving part in C++ (`cpp/serve`, 7.3 thousand lines in `.cc` files): `engine.cc` (1,102 lines), `model.cc` (1,345), `threaded_engine.cc`, the `engine_actions/` directory (prefill of new requests, batched decoding, verification/draft for speculative decoding, EAGLE, "jump-forward" decoding for grammars, **disaggregated prefill and decoding** in the `disagg_*` files), `prefix_cache.cc` + `radix_tree.cc` (a prefix cache in a radix tree), `sampler/`, `logit_processor.cc`. The paged KV cache lives in the TVM runtime. Git submodules: `3rdparty/tvm` points to the **`mlc-ai/relax` fork** (175 stars, last push 2026-10-04), `tokenizers-cpp`, **`xgrammar`** (structured generation) and `argparse`. Python layer: `mlc_llm serve` (OpenAI-compatible REST), `MLCEngine`, `AsyncMLCEngine`, multiple GPUs through "disco".

The hardware matrix from the README: AMD GPU "Vulkan, ROCm" (Linux/Windows), NVIDIA "Vulkan, CUDA", Apple "Metal", Intel "Vulkan"/Metal iGPU, Web "WebGPU and WASM", iOS Metal, Android OpenCL (Adreno/Mali). **The quality of support in individual cells of this matrix is unknown to me**; in particular, performance on consumer ROCm cards is not documented in my sources.

### 5.4 Project status in 2026: alive, but slow

- `mlc-ai/mlc-llm`, **Apache-2.0**, created 2023-04-29, 23,258 stars, 2,292 forks; Python 62.9 thousand + C++ 22.5 thousand lines (clone `@8978ea9a`, 2026-10-06).
- Last commit 2026-10-06. Commits in time windows (API): **98 in the last 12 months, 26 in the last 6 months versus 72 in the 6 months before that**. 11 of the 26 recent commits are from a single month (2026-09), author `akaashrp`.
- **Versioning is unclear**: the GitHub Releases tab has only `v0.1.dev0` from 2023; the tags from the API are `v0.26.dev0`, `v0.20.0` and `v0.20.dev0` (tag commit dates 2026-06-28 and 2026-07-07, in inconsistent order). Distribution goes through `mlc-ai-nightly` nightly wheels (from the documentation; I did not check).

**Who is behind it.** No company, no funding, no revenue linked to the repository *(I did not find any)*. Lineage: Apache TVM (Tianqi Chen, 2016, UW; `apache/tvm` 13.8 thousand stars, active) and the MLC project from CMU Catalyst and OctoAI. **Tianqi Chen** is an assistant professor at CMU and a Distinguished Engineer at NVIDIA, and in 2019–2024 was Chief Technologist at OctoAI, which NVIDIA acquired *(tqchen.com page)*. Main commit authors: MasterJH5574 (Ruihang Lai, CMU), junrushao (Junru Shao), tqchen, CharlieFRuan (Charlie Ruan), vinx13, yzh119. The funded entity in this lineage (OctoAI) no longer exists independently. Details: [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

### 5.5 Strengths and weaknesses

**Strengths:** the only stack in this comparison that targets phones, the browser, AMD, Intel, NVIDIA and Apple from one compilation pipeline; a serious research lineage; xgrammar for structured outputs; the code has server-side patterns (a prefix cache in a radix tree, disaggregated prefill and decoding).

**Weaknesses:** compilation per device per model; a low and declining commit rate; no GGUF; dependence on a TVM fork; performance on ROCm cards undocumented in my sources.

**Offline operation:** after the model is downloaded, everything is local; there are no traces of telemetry in `python/` and `cpp/` (grep returns only unrelated hits). The documentation has a `privacy.rst` file.

### 5.6 WebLLM: the same stack in a browser tab

`mlc-ai/web-llm`, Apache-2.0, TypeScript, 19,284 stars, npm package `@mlc-ai/web-llm`, release **v0.2.86 (2026-10-11)**; a roughly monthly cadence (v0.2.85 of 2026-09-08, v0.2.83 of 2026-04-24).

It runs a model compiled by MLC as **WebGPU** kernels plus a WASM runtime, **entirely inside a browser tab**. It has a JS interface shaped like the OpenAI API, streaming, a JSON mode (xgrammar), preliminary function calling, hosting in a Web Worker and a Service Worker, and a Chrome extension example. The weights go to the Cache API, IndexedDB or OPFS. The research paper: *WebLLM: A High-Performance In-Browser LLM Inference Engine*, arXiv 2412.15803, Ruan et al. with Tianqi Chen; it claims "up to 80% of native performance on the same device" *(authors' claim, arXiv abstract)*. Commit authors: CharlieFRuan 192, akaashrp 49, Neet-Nestor 46.

Why it matters: zero installation, no server, the user's data never leaves the device. Limitations: WebGPU availability, VRAM limits per origin, a multi-gigabyte first download, small models. For a builder of agent applications this is a **private client-side fallback or a target for a demo**, not a server engine. Also remember that llama.cpp already has the `ggml-webgpu` backend (21 thousand lines in the `0ce8cd1` tree), so in-browser inference is not MLC's exclusive domain.

### Check it yourself: MLC

> **Check it yourself 5: the quantization registry and the lack of GGUF** *(not run by me)*
> ```bash
> git clone --depth 1 https://github.com/mlc-ai/mlc-llm && cd mlc-llm
> grep -n 'QUANTIZATION' -A40 python/mlc_llm/quantization/quantization.py | head -60
> grep -rli 'gguf' python | head
> ```
> The first command will show the registry (`q4f16_1` and company). The second checks whether the Python layer has any GGUF support at all (my reading: none; check yourself and do not treat an empty result as proof without going through the hits).

---

## 6. NPU stacks and vendor stacks

An NPU (*Neural Processing Unit*) is a unit in a laptop or phone processor, designed for matrix multiplication at low power draw. For you this is a side topic: **none of these stacks touches Radeon cards or Linux with ROCm**. Get to know them so that you understand the map and do not confuse the names.

### 6.1 Overview

| Stack | Vendor | Runs on | Model format | License | Version (API data) | Maturity |
|---|---|---|---|---|---|---|
| **ONNX Runtime GenAI** | Microsoft | CPU, CUDA, DirectML, NvTensorRtRtx, OpenVINO, **QNN**, WebGPU; AMD GPU "planned"; in the tree `src/ep/{amdgpu,ryzenai,vitisai}` | **ONNX** (from the built-in *model builder*) | MIT | v0.17.0 (2026-09-28) | production inside Microsoft products |
| **OpenVINO GenAI** | Intel | CPU, iGPU/Arc, **NPU** (Core Ultra); Linux/Windows/macOS | **OpenVINO IR** (via `optimum-cli export openvino`) | Apache-2.0 | 2026.4.1.0 (2026-10-01) | a solid corporate project |
| **Qualcomm GenieX** (formerly NexaSDK) | Qualcomm | **Hexagon NPU, Adreno GPU, CPU**; Windows ARM64, Android, Linux ARM64 | GGUF (through llama.cpp) or per-chipset packages from Qualcomm AI Hub (QAIRT) | BSD-3-Clause | v0.9.1 (2026-10-17) | very active, pre-1.0 ("developer preview" since 2026-06-30) |
| **AMD Ryzen AI / OGA** | AMD | NPU + iGPU "hybrid" or NPU alone; Strix and Krackan Point processors; Windows | ONNX through ONNX Runtime GenAI with the VitisAI/Ryzen AI provider | (from the ONNX Runtime GenAI table) | OGA 0.14.0 at the time of this page | AMD documentation |

In addition, **for completeness**: Apple Foundation Models is a Swift interface to the *on-device system model* with guided generation and tool calling. There is no model choice, it is tied to the platform and it is not a general engine (unlike MLX, chapter [`07-APPLE-MLX-OMLX-AND-DS4.md`](07-APPLE-MLX-OMLX-AND-DS4.md)). The description comes from Apple's page, which I downloaded only in fragmentary form.

### 6.2 ONNX Runtime GenAI and OpenVINO GenAI

**ONNX Runtime GenAI** (`microsoft/onnxruntime-genai`, MIT, C++ 107.7 thousand lines in `src/`, 1,140 stars). The README describes it as "the generative AI loop for ONNX models": pre- and post-processing, inference through ONNX Runtime, logits processing, search and sampling, and KV cache management. It powers Foundry Local, Windows ML and the AI Toolkit for VS Code. So it is a **loop library on top of ONNX Runtime's execution providers**, not a kernel library. Bindings: Python, C#, C/C++, Java. The `src/engine/` directory (13 thousand lines: `scheduler.cpp`, `paged_key_value_cache.cpp`, `prefix_cache.cpp`) already holds an engine with continuous batching and a paged KV next to the older `Generator` API (maturity unknown). No GGUF: models go through `src/python/py/models/builder.py` (1,273 lines), which produces optimized and quantized ONNX models.

⚠️ **Telemetry in the official packages is enabled by default** (the 1DS SDK, HTTPS to Microsoft). You turn it off with `ORT_DISABLE_TELEMETRY=1`, the `--no_telemetry` flag at build time, or through the API (`docs/Privacy.md`, `cmake/options.cmake`).

**OpenVINO GenAI** (`openvinotoolkit/openvino.genai`, Apache-2.0, C++, 602 stars, 481 forks; OpenVINO's calendar-based versioning). Pipelines: `LLMPipeline`, VLM, image generation (Diffusers), Whisper, SpeechT5, embeddings and reranking. Features: speculative decoding, KV eviction, sparse attention, **continuous batching**, prefix cache, multi-LoRA. APIs in C++/Python/Node.js. My clone of the repository was incomplete (the git-lfs checkout failed), so **I make no statements about the code**. Remember that llama.cpp now has `ggml-openvino` (19.6 thousand lines, `docs/backend/OPENVINO.md`), so you can reach Intel hardware by two routes. Intel archived `intel-extension-for-pytorch` (2026-03-30; the optimizations moved into PyTorch). I did not check OpenVINO GenAI's telemetry.

### 6.3 Qualcomm GenieX: a correction to the typical picture

`qualcomm/GenieX` **is not** a new engine written in Go from scratch. GitHub redirects `NexaAI/nexa-sdk` to `qualcomm/GenieX` (the same repository ID 843570824, created 2024-08-16, release tags reaching back to `v0.2.16` of 2025-08-07). The most frequent commit authors are `mengshengwu`, `RemiliaForever`, `zhycheng614`, `zhiyuan8`, `Davidqian123`, `alexchen4ai`, `alanzhuly` (the association of these names with Nexa AI is *unverified*). The README speaks of "a generative AI runtime on Qualcomm devices" and "the community edition of Qualcomm GENIE", without mentioning Nexa or the rename. The history has an `init commit` from 2026-04-10 and 2,475 commits; release **v0.9.1 (2026-10-17)**, 8,448 stars, **BSD-3-Clause** license. **I could not establish the terms of the transition from Nexa to Qualcomm (an acquisition? a collaboration?) in any available source.**

Architecture (`CONTRIBUTING.md`, `.gitmodules`, the tree): a **CLI in Go** (`cli/`, gin + cobra, built with Bazel) → a **C SDK bridge** (`sdk/`, CMake; `llm.cpp`, `vlm.cpp`, `ml.cpp`, `registry.cpp`) → **plugins** `sdk/plugins/llama_cpp` (a vendored submodule `third-party/llama.cpp`) and `sdk/plugins/qairt` (the vendored `qualcomm/geniex-qairt-plugin`, **Qualcomm AI Engine Direct / QAIRT** libraries, selected with the `--qairt-lib` flag), plus a `model-manager` in Rust, Python/Kotlin/Java/Docker bindings and an OpenAI-compatible server. Formats: **GGUF** (the README recommends **Q4_0**, because of "best Hexagon NPU support") or ready-made per-chipset packages from Qualcomm AI Hub through QAIRT, NPU only. The "Qualcomm Terms of Use" mentioned in the README and any telemetry I **leave unexamined**. The lesson: vendor NPU stacks converge on "llama.cpp plus the vendor's runtime"; at the same time llama.cpp itself has a `ggml-hexagon` backend (53 thousand lines, `docs/backend/snapdragon`).

### 6.4 AMD Ryzen AI

AMD runs LLMs on the NPU through **ONNX Runtime GenAI (OGA) with the Ryzen AI / VitisAI execution provider**. According to AMD's documentation only **Strix and Krackan Point** processors are supported (not Phoenix/Hawk), in **hybrid** mode (NPU + iGPU; "best TTFT and TPS during prefill and decoding") or NPU alone ("Token Fusion" up to 16K tokens, "Full Fusion" up to 4,096), with instructions for Windows only *(company's own claim: https://ryzenai.docs.amd.com/en/latest/hybrid_oga.html)*. AMD publishes pre-optimized Llama, Mistral, Qwen, Gemma and Phi models. Code in the ONNX Runtime GenAI tree (`src/ep/ryzenai`, `src/ep/vitisai`, `src/ep/amdgpu`, "Copyright 2026 Advanced Micro Devices") confirms the integration. **None of this touches discrete Radeon cards or Linux with ROCm.** Lemonade (described in [`05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md`](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md)) packages this stack together with llama.cpp.

### 6.5 Who is behind it (vendor stacks)

All four are **software that sells silicon**: Microsoft (the Windows platform), Intel (Core Ultra CPU/NPU), Qualcomm (Snapdragon), AMD (Ryzen AI). The business model is "the tool is free so that the hardware has software". Practical consequence: priorities follow the chips the vendor happens to be selling. For your R9700s, AMD's closest "ally" is Lemonade, but it targets APUs and consumer PCs, not servers with four cards *(my assessment from [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md), unverified)*.

### Check it yourself: NPU

> **Check it yourself 6: GenieX is the former NexaSDK** *(I did not run this line; I established the redirect through the GitHub API)*
> ```bash
> gh api repos/NexaAI/nexa-sdk --jq '{full_name, id, stargazers_count, license: .license.spdx_id}'
> ```
> It should return `qualcomm/GenieX` with ID 843570824. For `gh` you usually need a logged-in session. Then open `.gitmodules` in the repository and check that `third-party/llama.cpp` is a submodule.

---

## 7. What this means for me

### 7.1 Let us start with an honest question: do you even have a problem this solves?

Your model is DeepSeek-V4-Flash in the `UD-IQ3_XXS` quantization, 284B parameters, run in llama.cpp on 4× R9700 (4 × 32 GB nominally; in reality 4 × 34.2 GB = 136.8 GB) at about 50 tok/s. Hybrid MoE offload makes sense when the weights *do not fit* in VRAM — in your case they fit. Your file is 104.2 GB (4 GGUF parts; measured), which is on average about 2.9 bits per weight (104.2 GB × 8 / 284B, *my calculation*; see [`03-QUANTIZATION-AND-FORMATS.md`](03-QUANTIZATION-AND-FORMATS.md) — `UD-IQ3_XXS` is a mix of tensor types, so the average depends on the composition). The cards have 136.8 GB together (4 × 34.2 GB; see [`03`](03-QUANTIZATION-AND-FORMATS.md)), so the file fits and about 32 GB remains (*my calculation*) for the KV cache and buffers (which the 2 × 98,304-token context from production uses).

Two conclusions:

1. **If your model sits entirely in VRAM, none of the mechanisms from section 3 is needed for this model.** That is good news: 50 tok/s on such a configuration is a good sign that nothing travels over a slow link.
2. **Offload mechanisms start to matter when:** (a) you choose a larger quantization of the same model (e.g. something around Q4 that exceeds 128 GB), (b) you want a longer context at the expense of VRAM, (c) a larger model appears (the DeepSeek V4 PRO family has 1.6 trillion parameters in total, 49B active, according to `MODEL_CARD.md` in ds4).

### 7.2 Which ideas may matter

| Idea | Where from | How to use it in llama.cpp on your machine |
|---|---|---|
| **Placement by expert usage frequency** | KT: the `frequency` strategy; according to the project's data it beats uniform placement (table in 2.7) | You do not have this granularity in `-ot` (layer tensor), but you can *choose layers* for `--n-cpu-moe`/`-ot` guided by your own statistics (e.g. which layers have the "flattest" usage distribution). Measuring is your own work; **I did not check** whether llama.cpp has a ready-made tool for collecting expert usage statistics. |
| **Expert cache on the GPU** | llama.cpp `--moe-cache-mib` (off by default); ds4 (cache + hot list) | The closest equivalent of KT's idea on your stack. An experiment with a larger quantization: set the cache size and compare tok/s. **I do not know** how it works on gfx1201 (nobody measured it in my sources); this is for your own measurement. |
| **Thread pinning and NUMA** | KT: `hwloc`, a thread per physical core | If the host has two sockets, `numactl` or equivalent pinning matters for anything RAM-based. I do not know your machine's CPU configuration, so I only point it out. |
| **Expert deferral** | KT | **There is no equivalent in llama.cpp.** Remember it as an idea; you cannot do it without changes to the engine code. |
| **ISQ and `tune`: "one bits knob" + a recommendation from the hardware** | mistral.rs | A UX pattern for your own launcher on top of `llama-swap`. |
| **Agent loop and MCP in the engine** | mistral.rs | An architectural decision for your applications: where to execute tools (engine or orchestrator). For CUDA/Mac; not on the R9700. |
| **WebLLM** | MLC | A private client-side fallback or a browser demo; not a server runtime. |

### 7.3 What is irrelevant for you (skip consciously)

- **mistral.rs on the R9700**: no ROCm and Vulkan. On the other hand, **on Macs** it is a credible second Metal engine next to MLX, so possibly worth measuring there.
- **The prebuilt KTransformers wheel**: NVIDIA SM 80–90 only and needs server RAM (minimum 256 GB). On the R9700 this is a build from source with no declared support.
- **NPU stacks** (ONNX Runtime GenAI, OpenVINO GenAI, GenieX, Ryzen AI): these are Windows, Snapdragon, Core Ultra and AMD APUs. There is no path there for your cards.
- **MLC LLM as a server engine**: compilation per model per device, slow commits and no GGUF are a cost that llama.cpp spares you.
- **IQK quants from ik_llama.cpp**: files with IQ_K/KT quants load only there and lock you into the fork (see [`04-LLAMA-CPP-AND-THE-GGML-FAMILY.md`](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md)).

### 7.4 The "watch, do not deploy" list

| What to watch | What to look for | How I know |
|---|---|---|
| **KTransformers + ROCm** | Whether `kt-kernel` gets documented ROCm/RDNA4 support (the `KTRANSFORMERS_USE_ROCM` option is in CMake, but with no mention of gfx1201) and whether it lands in mainline SGLang with AMD documentation. | `kt-kernel/CMakeLists.txt`, no gfx1201 in the documents |
| **`--moe-cache-mib` in llama.cpp** | Measurements on ROCm and a description of when it helps. The flag is fresh and off by default. | `common/arg.cpp`, `src/llama-moe-cache.h` |
| **Expert cache in ik_llama.cpp** | Whether the cache implemented on 2026-10-12 aligns with mainline, or the fork diverges. | ik_llama.cpp, entry `Implement moe cache #2644` |
| **ds4 on gfx1201** | Whether PR #558 (and two other third-party PRs) lands in main. This is the only source of R9700 data in this group. | notes on ds4 (PR #558) |
| **llama.cpp: `ggml-hexagon`, `ggml-openvino`, `ggml-webgpu`** | How fast the mainstream absorbs the NPU and browser niches. | the `0ce8cd1` tree |
| **mistral.rs: a Vulkan or ROCm backend** | If one appears, an engine with a built-in agent and MCP becomes a candidate. Today: none. | grep over the tree |
| **MLC LLM: commit pace** | A drop from 72 to 26 commits in 6 months. A further decline means a risk of abandonment. | GitHub API |
| **Qualcomm GenieX: clarifying the relationship with Nexa AI** | The terms of the transition and any terms of use/telemetry. | README; I could not establish |

### 7.5 One sentence to finish

Take one concrete lesson from this chapter: **expert placement at the level of a single expert and by actual usage frequency** is what distinguishes KT (and the cache in ds4 and in the new llama.cpp) from `-ot`. If you ever run out of VRAM, check `--n-cpu-moe` first in llama.cpp, then `--moe-cache-mib`, and only when you build a separate machine with a server CPU and an NVIDIA card, consider KT through SGLang. A further comparison of all the engines and the choice: [`09-COMPARISON-AND-CHOICE.md`](09-COMPARISON-AND-CHOICE.md). On speeding up generation on your machine (speculative decoding, tensor split): [`../speeding-up-generation/README.md`](../speeding-up-generation/README.md).

---

## Open questions

- KTransformers: the names of the competing baselines in the SOSP paper (I suspect llama.cpp and Fiddler, unverified); the "layerwise transport" mechanism in prefill not traced; Approaching.AI's funding unknown (site unreachable).
- mistral.rs: Eric Buehler's position at Hugging Face has not been confirmed; completeness of reading IQ quants through the GGUF path not checked.
- MLC LLM: quality and performance on consumer ROCm cards undocumented in my sources; the exact release scheme unclear.
- Qualcomm GenieX: the relationship with Nexa AI and the terms of use.
- ik_llama.cpp: I did not read the server and scheduler code (no clone); I did not check telemetry.
- llama.cpp `--moe-cache-mib`: the degree of overlap of copies with computation and the behavior on gfx1201 not established.
- ds4: the "who computes the experts after loading" comparison I infer from the description in the documentation, not from reading `ds4_ssd.c`.
