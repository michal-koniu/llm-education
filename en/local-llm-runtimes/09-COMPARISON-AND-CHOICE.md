# 09 · Comparison and choice — what for what, and what to do on your hardware

A practical chapter: it gathers the conclusions of chapters 04–08 into tables and scenarios. After reading it you will be able to name an engine for each of your use cases,
know **what of this will run on your AMD rig (4× R9700, gfx1201)** and what only on a Mac, and have a list of experiments worth doing (I have not run any of them).

> ⚠️ **What is not here.** I do not have a single measurement that compares engines on one piece of hardware, one model and one workload — and without such a measurement you must not
> compare tok/s figures from different sources (see chapter [02](02-HOW-INFERENCE-WORKS.md), the section on methodology). That is why **there is no "speed" column here**. What there is: features established in the code and documentation,
> conclusions drawn from them, and a risk assessment. My own measurements concern only llama.cpp on the reference rig: [`../speeding-up-generation/README.md`](../speeding-up-generation/README.md).
> As of **19 October 2026**.

## Table of contents

1. [The main matrix](#1-the-main-matrix)
2. [What of this will run on gfx1201 (R9700)](#2-what-of-this-will-run-on-gfx1201-r9700)
3. [API, offline mode, telemetry and security](#3-api-offline-mode-telemetry-and-security)
4. [Choosing by scenario](#4-choosing-by-scenario)
5. [What to borrow from the whole overview](#5-what-to-borrow-from-the-whole-overview)
6. [Experiments to run (not run)](#6-experiments-to-run-not-run)
7. [Recommendation for two reference environments](#7-recommendation-for-two-reference-environments)

---

## 1. The main matrix

One table, all the main engines. Details and evidence: the chapters in the last column. "KV management" = how the KV cache is divided among requests.

| Engine | What it is for | Hardware | Model format | Many users | KV management | License | Ch. |
|---|---|---|---|---|---|---|---|
| **llama.cpp** | one user / small team, any hardware | CPU + about 15 backends (CUDA, **HIP**, Metal, Vulkan, SYCL, …) | **GGUF** | `-np` slots, simple scheduler | contiguous KV per slot, prompt cache in RAM, checkpoints; **no PagedAttention** | MIT | [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |
| **ik_llama.cpp** | fork: more quantizations and kernels, CPU/hybrid | like llama.cpp (narrower range) | GGUF (+ its own IQ_K types — fork only) | like llama.cpp | like llama.cpp | MIT | [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |
| **vLLM** | throughput, many users, server GPUs | NVIDIA, ROCm, Intel XPU, CPU, TPU + plugins | HF/safetensors (+ AWQ, GPTQ, FP8…); GGUF = experimental plugin | **yes**, continuous batching with a token budget | blocks + prefix hash | Apache-2.0 | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| **SGLang** | agents, shared prefixes, MoE | NVIDIA, AMD Instinct, TPU, Intel, Ascend | HF/safetensors | **yes** | radix tree | Apache-2.0 | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| **TensorRT-LLM** | maximum on NVIDIA | **NVIDIA only** | HF + FP8/NVFP4 | **yes** | paged KV | Apache-2.0 + notices | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| **MLX / mlx-lm** | Apple Silicon (natively) | Metal; CUDA backend; **no HIP** | MLX (safetensors) | server with batching in mlx-lm | cache classes (rotating, quantized) | MIT | [07](07-APPLE-MLX-OMLX-AND-DS4.md) |
| **oMLX** | Mac + coding agents, persistent cache | Apple Silicon | MLX, oQ formats | **yes**, continuous batching | paged, RAM tier + **SSD** | Apache-2.0 | [07](07-APPLE-MLX-OMLX-AND-DS4.md) |
| **ds4 / DwarfStar** | narrow engine: the DeepSeek V4 family (+ a few models) | Metal, CUDA, ROCm (**gfx1151**) | its own GGUF layout | weak (one model per process) | **disk**: KV on SSD, expert streaming | MIT | [07](07-APPLE-MLX-OMLX-AND-DS4.md) |
| **KTransformers** | huge MoE: experts in RAM, attention on GPU | NVIDIA (wheel), ROCm from source | HF | yes (through SGLang) | like SGLang | Apache-2.0 | [08](08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS.md) |
| **mistral.rs** | a Rust engine for embedding | CUDA, Metal, CPU; **no ROCm or Vulkan** | HF, GGUF, ISQ | yes | PagedAttention | MIT | [08](08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS.md) |
| **MLC LLM / WebLLM** | compilation for any device, the browser | many (through TVM) | compiled MLC artifacts | limited | its own | Apache-2.0 | [08](08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS.md) |
| **Ollama / LM Studio / Jan / Lemonade / …** | wrappers with a registry and GUI | depends on the engine underneath | GGUF (and MLX on Mac) | depends | depends | various | [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |

Reading rule: **if the "Many users" column does not say "yes", the engine is built for one conversation at a time** — which for an agent with a few parallel calls is sometimes enough (on the reference rig: 2 slots × 98,304 tokens, 63 tok/s in total with two agents — my measurement).

---

## 2. What of this will run on gfx1201 (R9700)

The most important table for the reference rig. Sources: the code and documentation from chapters 04–08. ⚠️ **I did not run any of these programs on the R9700 except llama.cpp, which runs in production.**

| Engine | Status on gfx1201 according to the notes | What it means for the reference rig |
|---|---|---|
| **llama.cpp** | **works** (the reference production setup: a HIP build for exactly `gfx1201`; the code has a dedicated tuning file `mmq-config-rdna4.cuh` and WMMA paths for RDNA4) | the reference point |
| **vLLM** | *claimed*: R9700 recognized by PCI id, gfx1201 among the default build architectures, INT4 kernels for RDNA; **no measurement at all** in the notes; the documentation says AWQ/GPTQ do not work on AMD, the code says otherwise | the only server engine with documented RDNA4 support — but test first, see §6 |
| **SGLang** | **unsupported**: the ROCm build accepts only gfx942, gfx950, gfx1250 (and gfx1250 is not RDNA4) | come back when `setup_rocm.py` lists gfx12xx |
| **TensorRT-LLM** | not applicable (NVIDIA only) | skip |
| **ds4** | ROCm only **gfx1151** (Strix Halo); three PRs and one issue for gfx1201 open, unmerged; the only data point: one R9700 with SSD streaming, **2.3–4.7 tok/s**; the ROCm path in the code looks single-card | not a replacement for llama.cpp on the rig; comparing with your ~50 tok/s is **not like-for-like** (for you the weights sit in the VRAM of four cards) |
| **MLX, mlx-lm, oMLX, exo** | no HIP backend in MLX; exo on Linux is CPU only | Mac only |
| **KTransformers** | a ready wheel only for NVIDIA (SM 80–90, server RAM ≥ 256 GB); ROCm = a build from source with no declared support | skip |
| **mistral.rs** | no ROCm or Vulkan backends | skip on the rig; an option on a Mac |
| **MLC / WebLLM** | quality and performance on consumer ROCm cards undocumented in my sources; a low and falling commit rate | *(I could not establish)* |
| **Ollama** | `docs/gpu.mdx` lists the **Radeon AI PRO R9700** in the ROCm section (ROCm v7); Vulkan enabled by default | possible, **unchecked** for your 284B model |
| **Lemonade** | the backend table lists the `gfx120X` family (llama.cpp-ROCm, vLLM-ROCm experimental) | the closest confirmation among the wrappers, as a family |
| **LM Studio** | unverified (the runtimes page returned 404) | *(I could not establish)* |
| **Docker Model Runner, RamaLama, Jan, llmman** | ROCm exists as a path; gfx1201 is not listed | *(unchecked)* |

Conclusion: **on an AMD rig the real alternative to llama.cpp today is (potentially) only vLLM**, and only for models in HF format that fit in 128 GB together with the KV pool.
The reference model (284B, GGUF UD-IQ3_XXS, 104.2 GB) does not have this path: in INT4 it would be ≈ 142 GB of weights alone *(my calculation: 284 billion × 0.5 B)*, more than 4 × 32 GB.

---

## 3. API, offline mode, telemetry and security

### 3.1 The protocols the servers speak

| | OpenAI Chat | OpenAI Responses | Anthropic `/v1/messages` | Ollama API | Notes |
|---|---|---|---|---|---|
| **llama-server** | ✔ | ✔ | ✔ (+ `count_tokens`) | — | + `/v1/rerank`, `/v1/embeddings`, `/slots`, `/metrics` |
| **vLLM** | ✔ | — (I could not establish) | ✔ | **no** | + Cohere, gRPC |
| **SGLang** | ✔ | — (I could not establish) | ✔ | ✔ | + gRPC |
| **TensorRT-LLM** | ✔ | ✔ | adapter | — | |
| **Ollama** | ✔ (including `/v1/responses`) | ✔ | ✔ | native `/api/*` | |
| **LM Studio** | ✔ | — | ✔ | — | + native REST, stateful `/v1/chat` (`response_id`) |
| **llmman** | ✔ | — | ✔ | ✔ | + Gemini |
| **Lemonade** | ✔ | — | ✔ | ✔ | |

("—" = not listed in the notes, not "does not exist".) In practice: if your agent (e.g. a Claude Code-like one) speaks Anthropic and you do not want a proxy, `llama-server` can serve it directly.

### 3.2 Offline and telemetry

| Engine | Fully offline after downloading the model? | Telemetry / "phone home" connections |
|---|---|---|
| **llama.cpp** | yes; the `--offline` flag | in the code of `common`, `tools`, `src`, `ggml/src` I **did not find** telemetry or update checks (a grep search, not a negative proof) |
| **vLLM** | yes | usage statistics **enabled by default**, disabled by opt-out |
| **TensorRT-LLM** | yes | usage statistics **enabled by default**, opt-out |
| **SGLang** | yes | none found |
| **Ollama** | inference yes (`--offline`) | the app checks for updates; models from the registry; cloud optional (`OLLAMA_NO_CLOUD=1` disables it) |
| **LM Studio** | yes | updates, model search, cloud features; privacy statement *(company's own claim)* |
| **Jan** | yes | opt-in analytics (PostHog EU) *(project's own claim)* |
| **Lemonade** | yes (backends and models downloaded on first use) | "zero telemetry" *(project's own claim)* |
| **ONNX Runtime GenAI** | yes | telemetry **enabled by default** in the official packages |

### 3.3 Attack surfaces worth knowing

- **`llama-server --agent` / `--tools` / `--mcp-servers-config`** (chapter [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) §6): unauthenticated execution of shell commands with the server user's privileges if the port is reachable. If `llama-swap` listens on all interfaces without a password and the models start with `--agent`, anyone on the LAN can run shell commands on the host — **this is the most important risk of a stack like this** (see also [`../speeding-up-generation/04-USING-UI-CLI-OPENCLAW.md`](../speeding-up-generation/04-USING-UI-CLI-OPENCLAW.md)). I did not check whether this can be exploited from the network.
- **ds4:** a server without authentication; a tensor-parallelism protocol without encryption.
- **`ggml-rpc-server`:** the README warns that it is a "proof-of-concept, fragile and insecure"; do not run it on an open network.
- **The model supply chain:** you download weights and chat templates from other people's repositories. A Jinja template is code executed on every request; a GGUF from strangers calls for the same caution as any executable *(a general conclusion, not from the notes)*.

---

## 4. Choosing by scenario

| Scenario | Choice | Why | What to avoid |
|---|---|---|---|
| **AMD rig 4×R9700, one big MoE for agents** (the reference setup) | **llama.cpp + llama-swap**, tensor mode + draft; `layer` + 4 slots as the fallback | the only engine with confirmed operation on gfx1201 and with a GGUF IQ3 for the 284B; the knobs you need | swapping for a wrapper that hides the flags |
| **Many agents in parallel with a shared long prefix** (on the same rig) | first **`--parallel` / `--cache-ram` / `--ctx-checkpoints` in llama.cpp**; only then a one-day vLLM test on a smaller HF model | prefixes and slots in llama.cpp cover a large part of the needs; vLLM has no measurement on RDNA4 | moving blind |
| **Mac (≥ 64 GB) — daily work and coding agents** | **oMLX** (persistent KV cache on SSD, Anthropic API) or **mlx-lm** | the prefix cache survives a restart; MLX is native to Apple | llama.cpp on a Mac only when you need GGUF |
| **Mac with ≥ 96 GB and a wish for DeepSeek V4 locally with a disk-backed KV** | **ds4** (beta) | an engine built for this class of models *(project's own claim)* | exposing it to the network (no authentication) |
| **Quick start, a chat window, first models** | **LM Studio** or **Ollama** | registry, GUI, minimal configuration | expecting to squeeze out of them everything you get from `llama-server` |
| **Team, an NVIDIA server, dozens of users** | **vLLM** (or SGLang with shared prefixes and MoE) | throughput, paged KV, ecosystem | llama.cpp as a multi-user server |
| **Maximum on NVIDIA GPUs, a fixed configuration** | **TensorRT-LLM** (or vLLM) | FP8/NVFP4 kernels | AMD |
| **Huge MoE in RAM, little VRAM** | **llama.cpp with `-ot`/`--n-cpu-moe`**, ik_llama.cpp, KTransformers (NVIDIA) | experts in RAM, attention on GPU | KTransformers on AMD |
| **Models in the browser / on a phone / on an NPU** | **WebLLM**, **Qualcomm GenieX**, ONNX Runtime GenAI, Lemonade (Ryzen AI NPU) | niches | skipping the telemetry check |
| **A network-isolated environment (air-gap)** | llama.cpp (`--offline`) or **llmman/OCI** (transfer of model images) | no telemetry; models as OCI artifacts | products with a background updater |
| **One API for many different engines** | **llama-swap**, LiteLLM, LocalAI (60+ backends) | a single routing layer | — |

---

## 5. What to borrow from the whole overview

The most valuable ideas, in order of usefulness for the reference stack (each has a source in the chapter given in parentheses):

1. **A stable prefix and a byte-for-byte identical history** in agent applications — every change of serialization invalidates the cache (ds4, oMLX, vLLM; [07](07-APPLE-MLX-OMLX-AND-DS4.md), [06](06-SERVING-ENGINES-VLLM-SGLANG.md)).
2. **llama.cpp settings that implement the same ideas as the server engines:** `--parallel` + a fixed `id_slot`, `--cache-ram` (default 8192 MiB), `--cache-idle-slots`, `--ctx-checkpoints` ([04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md)).
3. **A persistent prefix cache on disk** (oMLX, ds4): today in llama.cpp only manually through `/slots` (saving/restoring a slot's state) — worth testing before building your own mechanism ([07](07-APPLE-MLX-OMLX-AND-DS4.md)).
4. **Model-native speculative decoding** (DSpark/MTP — you already have it) and n-gram variants without a draft — cheap for code and repeated tool calls ([04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md), [02](02-HOW-INFERENCE-WORKS.md)).
5. **Routing requests with a shared prefix to the same backend** (the `cache_aware` policy in the SGLang gateway) — for your own orchestrator ([06](06-SERVING-ENGINES-VLLM-SGLANG.md)).
6. **Distributing models as OCI artifacts** (llmman, Docker Model Runner, RamaLama, Ollama): a Harbor/Artifactory/ghcr registry as a model store in your infrastructure, cosign signatures ([05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md)).
7. **A placement heuristic:** first try to fit the model on one card, only then split ([05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md)); in llama-swap you express this as a separate entry per model.
8. **Isolation of the agent's tools:** `--tools-runtime docker:<image>` in llama-server, `--network none` in a rootless container (RamaLama), the `--sandbox` flag in llmman ([04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md), [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md)).
9. **A registry of tool and reasoning parsers per model family**, separate from the engine (vLLM) — your own glue code in agent applications ([06](06-SERVING-ENGINES-VLLM-SGLANG.md)).
10. **Always measure your own quantization with your own metric** — the quality data you have today for UD-IQ3_XXS after the speedup is 11 out of 120 samples ([03](03-QUANTIZATION-AND-FORMATS.md)).

---

## 6. Experiments to run (not run)

Each of them is designed to give a number or an unambiguous "does not work". I ran none of them — they require isolating the cards from production.

| # | Question | Method | Approximate cost | Ch. |
|---|---|---|---|---|
| 1 | How much quality do you lose after moving to tensor mode + DSpark? | finish the quality benchmark (it was interrupted after 11 of 120 samples) or compare the KL divergence against a higher quantization on the same prompts | a few GPU hours | [03](03-QUANTIZATION-AND-FORMATS.md) |
| 2 | Does RCCL improve tensor mode on 4×R9700? | build with `-DGGML_HIP_RCCL=ON`, compare tok/s | ~2 min of build + measurements | [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |
| 3 | Does P2P between cards (`GGML_CUDA_P2P=1`) help without corrupting results? | a test comparing the text; risk: corrupted output with IOMMU enabled | an hour | [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |
| 4 | Does vLLM even start on gfx1201 and how does it do with many agents? | a small HF model (FP8/INT4) in 128 GB; `vllm bench` at *your* number of parallel requests; isolated cards | a day | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| 5 | Do n-gram variants (`--spec-type ngram-*`) add anything to DSpark on agent code? | the same prompts, separate runs | an hour | [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |
| 6 | Does saving/restoring a slot through `/slots` shorten the start of a long agent session? | measure prefill time with and without restoring | an hour | [07](07-APPLE-MLX-OMLX-AND-DS4.md) |
| 7 | Do `--cache-ram` and `--ctx-checkpoints` improve cache hits in your agent loops? | `/metrics` before and after | an hour | [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |
| 8 | What does moving to a larger quantization (e.g. around Q4) give, if it fits? | tok/s and quality; remember 128 GB of VRAM and the KV pool | requires downloading a model | [03](03-QUANTIZATION-AND-FORMATS.md) |

---

## 7. Recommendation for two reference environments

**The AMD rig (4× R9700):** stay with **llama.cpp + llama-swap**. It is the only engine with confirmed operation, and there is a measured result for it (from 23.5 to about 50 tok/s for one agent, 63 tok/s in total with two).
Improve it with what is already in it: experiments 1–3 and 5–7 from §6. Consider moving to vLLM only for a *different, smaller* model in HF format and only after the test from §6 (no. 4).
The most urgent matter is not speed but **exposure security** (`--agent` on a port reachable from the network, §3.3) and **quality after the change** (no. 1).

**A Mac:** for daily work and coding agents start with **oMLX** (or **mlx-lm**, if you prefer less magic); for simple conversations **LM Studio** or **Ollama** (both have MLX paths). Treat **ds4** as an interesting, fast, but young engine for one kind of model — good to try on a Mac with a lot of memory,
not as a foundation. When choosing a Mac, go by **GB/s and GB of RAM**, not the number of cores (chapter [07](07-APPLE-MLX-OMLX-AND-DS4.md), §1).

**In general:** the engine is a replaceable element; what lasts is **the model format, the API protocol and your agent loops**. Stick to standard APIs (OpenAI/Anthropic), GGUF files and configuration kept in the repository —
then changing the engine in a year (or a change of the project's owner, chapter [10](10-MONEY-AND-PEOPLE.md)) costs an hour, not a week.
