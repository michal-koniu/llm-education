# 01 · Map and layers — what a "runtime" is and who is who

The opening chapter. After reading it you will be able to answer the question of **which program we are even talking about** when someone writes "I run a model locally":
the weights file, the library that computes matrices, the inference engine, the HTTP server, the app with a window, or the gateway in front of them.
All the following chapters rely on this map.

> ⚠️ **What is not here.** The whole course is **desk research and reading source code**: documentation, the GitHub API, research papers and repositories cloned on the rig
> (read-only). **I did not run or measure anything** — the rig's GPUs are in production use. Figures carry a date and a source; data given by the projects
> themselves I mark *(project's own claim)*, press reports *(press report)*, my own calculations *(my calculation)*. As of **19 October 2026**; this overview goes stale within weeks.
> Stars, licenses and creation dates come from the GitHub API on that day.

## Table of contents

1. [Seven layers: from the weights file to the chat window](#1-seven-layers-from-the-weights-file-to-the-chat-window)
2. [Project map: who sits in which layer](#2-project-map-who-sits-in-which-layer)
3. [The dependency network: who runs whose code](#3-the-dependency-network-who-runs-whose-code)
4. [Five philosophies: why more engines keep appearing](#4-five-philosophies-why-more-engines-keep-appearing)
5. [The journey of one request through all the layers](#5-the-journey-of-one-request-through-all-the-layers)
6. [How it came about: a timeline](#6-how-it-came-about-a-timeline)
7. [How to read the rest of the course](#7-how-to-read-the-rest-of-the-course)

---

## 1. Seven layers: from the weights file to the chat window

The word "runtime" (or "engine", "inference engine") gets used for everything from a library of kernels to an app with an icon in the menu bar.
To avoid confusion, the **layers** have to be separated. One truck, several different things: the field with the raw material, the factory, the warehouse, the shop.

```
 ┌───────────────────────────────────────────────────────────────────────────────┐
 │ 7  Orchestration & gateways  llama-swap, LiteLLM, llm-d, Dynamo, LMCache       │ many servers, routing,
 │                            (several processes / machines as one API)           │ model swapping, KV cache
 ├───────────────────────────────────────────────────────────────────────────────┤
 │ 6  Apps and frontends      Open WebUI, AnythingLLM, LM Studio UI, Jan         │ chat window, agents,
 │                            (talk to the API, do not compute themselves)       │ conversation history
 ├───────────────────────────────────────────────────────────────────────────────┤
 │ 5  Wrappers                Ollama, LM Studio, Jan, LocalAI, Lemonade,          │ model registry, lifecycle,
 │                            Docker Model Runner, RamaLama, llmman               │ defaults, GUI
 ├───────────────────────────────────────────────────────────────────────────────┤
 │ 4  Server                  llama-server, vLLM API server, SGLang, ds4-server   │ HTTP: /v1/chat/completions,
 │                            (request queue, slots, SSE streaming)               │ chat templates, tool calls
 ├───────────────────────────────────────────────────────────────────────────────┤
 │ 3  Inference engine        libllama, vLLM EngineCore, SGLang scheduler,        │ scheduler, KV cache,
 │                            mlx-lm, ds4, mistral.rs, TensorRT-LLM               │ sampling, batching, parallelism
 ├───────────────────────────────────────────────────────────────────────────────┤
 │ 2  Tensor library          ggml, MLX, PyTorch, Candle, + kernels:              │ matrix multiplication, attention,
 │    and kernels             FlashAttention, FlashInfer, hipBLAS/cuBLAS          │ quantized GPU kernels
 ├───────────────────────────────────────────────────────────────────────────────┤
 │ 1  Model and format        HF checkpoint (safetensors), GGUF, MLX, AWQ/GPTQ    │ weights + tokenizer + template;
 │                            (+ quantization: Unsloth UD, imatrix, oQ…)          │ "what is in the file"
 └───────────────────────────────────────────────────────────────────────────────┘
        hardware: CUDA · ROCm/HIP · Metal · Vulkan · SYCL · CPU · NPU
```

Two remarks without which the rest of the course will be confusing:

1. **The layer boundaries are blurred, because projects readily cross them.** llama.cpp is at once layer 2 (ggml), 3 (libllama), 4 (`llama-server`) and — since 2026 — a piece of 5 and 7
   (a built-in router mode with LRU model swapping, built-in tools and an MCP client; see [`04-LLAMA-CPP-AND-THE-GGML-FAMILY.md`](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md)).
   vLLM and SGLang are 3 + 4. LM Studio is 5 + 6, with closed code. So "what is in which layer" is really an answer to the question "whose code is responsible for what".
2. **Generation speed (tok/s) is decided in layers 1–3.** Layers 4–7 can spoil it (bad defaults, copying, a cache that does not hit),
   but can improve it only indirectly (e.g. through prompt-cache hits). That is why the technical chapters of the course mostly cover layers 1–4, and I describe the "wrappers" separately
   (chapter [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md)).

---

## 2. Project map: who sits in which layer

The table below covers the projects to which the course devotes more than a sentence. **Layer** refers to the diagram in §1 (the most important of several). Stars: GitHub API, 2026-10-19.
The "archive" mark = the repository is archived.

### 2.1 Engines and libraries (layers 2–4)

| Project | Layer | License | Stars | Created | Language | Where covered |
|---|---|---|---|---|---|---|
| **llama.cpp** (+ **ggml**) | 2–4 | MIT | 131,716 (ggml: 15,508) | 2023-03-10 | C/C++ | [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |
| **ik_llama.cpp** (fork) | 2–4 | MIT | 3,311 | 2024-06-27 | C++ | [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |
| **llamafile** | 5 on llama.cpp | NOASSERTION (see [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md)) | 26,441 | 2023-09-10 | C++ | [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |
| **KoboldCpp** | 5 on llama.cpp | AGPL-3.0 | 12,032 | 2023-03-16 | C++ | [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |
| **vLLM** | 3–4 | Apache-2.0 | 94,152 | 2023-02-09 | Python | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| **SGLang** | 3–4 | Apache-2.0 | 37,444 | 2024-01-08 | Python | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| **TensorRT-LLM** | 3–4 (NVIDIA only) | Apache-2.0 + third-party code notices (GitHub: NOASSERTION) | 14,859 | 2023-08-16 | Python/C++ | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| **TGI** (Hugging Face) | 3–4 | Apache-2.0 | 10,879 (**archive**) | 2022-10-08 | Python/Rust | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| **MLX** | 2 | MIT | 28,845 | 2023-11-28 | C++/Python | [07](07-APPLE-MLX-OMLX-AND-DS4.md) |
| **mlx-lm** | 3–4 | MIT | 7,405 | 2025-03-11 | Python | [07](07-APPLE-MLX-OMLX-AND-DS4.md) |
| **oMLX** | 3–5 (Mac) | Apache-2.0 | 22,936 | 2026-02-13 | Python | [07](07-APPLE-MLX-OMLX-AND-DS4.md) |
| **ds4 / DwarfStar** | 2–4 (narrow) | MIT | 23,955 | 2026-05-06 | C | [07](07-APPLE-MLX-OMLX-AND-DS4.md) |
| **exo** | 7 (cluster of Macs) | Apache-2.0 | 47,965 | 2024-06-24 | Python | [07](07-APPLE-MLX-OMLX-AND-DS4.md) |
| **KTransformers** | 3 (hybrid MoE) | Apache-2.0 | 19,619 | 2024-07-26 | Python/C++ | [08](08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS.md) |
| **mistral.rs** | 3–4 | MIT | 7,759 | 2024-02-26 | Rust | [08](08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS.md) |
| **MLC LLM** | 2–3 | Apache-2.0 | 23,258 | 2023-04-29 | Python/C++ | [08](08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS.md) |
| **LMDeploy** | 3–4 | Apache-2.0 | 8,108 | 2023-06-15 | Python | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |

### 2.2 Wrappers and frontends (layers 5–6)

| Project | Engine underneath | License | Stars | Created | Where covered |
|---|---|---|---|---|---|
| **Ollama** | upstream `llama-server` (GGUF) + its own MLX runner (Apple) | MIT | 183,857 | 2023-06-26 | [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |
| **LM Studio** | closed llama.cpp + MLX runtimes | closed app; `lms` (CLI) MIT | `lms`: 5,360 | — | [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |
| **Jan** | llama.cpp (+ MLX on Mac) | Apache-2.0 in the README, GitHub: NOASSERTION | 45,017 | 2023-08-17 | [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |
| **GPT4All** | its own llama.cpp fork; **dormant project** (last commit 2025-05-27) | MIT | 77,350 | 2023-03-27 | [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |
| **LocalAI** | 60+ backends in OCI images | MIT | 49,695 | 2023-03-18 | [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |
| **Lemonade** | llama.cpp (ROCm/Vulkan), AMD NPU | Apache-2.0 | 5,936 | 2025-05-15 | [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |
| **Docker Model Runner** | llama.cpp / vLLM / SGLang / MLX | Apache-2.0 | 658 | 2025-03-28 | [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |
| **RamaLama** | llama.cpp / vLLM in per-GPU images | MIT | 3,086 | 2024-07-24 | [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |
| **llmman** | upstream llama.cpp / vLLM / SGLang / mlx-lm / ds4 | Apache-2.0 | 563 | 2026-03-22 | [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |
| **Open WebUI** (frontend) | — | BSD-3 + branding clause | 156,189 | 2023-10-06 | [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |
| **AnythingLLM** (frontend) | — | MIT | 67,323 | 2023-06-04 | [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |

### 2.3 Orchestration and surrounding tools (layer 7 and the sides)

| Project | Role | License | Stars | Where |
|---|---|---|---|---|
| **llama-swap** | proxy + process manager: model swapping, groups, TTL (you use it in production) | MIT | 6,015 | [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |
| **NVIDIA Dynamo** | routing and prefill/decode separation in a cluster | NOASSERTION | 8,332 | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| **llm-d** | inference on Kubernetes | Apache-2.0 | 4,866 | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| **LMCache** | KV cache layer (offload) | Apache-2.0 | 12,116 | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| **FlashInfer**, **FlashAttention** | attention kernel libraries | Apache-2.0 / BSD-3 | 6,708 / 25,161 | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| **Unsloth** | training + "Dynamic" (UD) GGUF quantizations, local UI | Apache-2.0 | 78,273 | [03](03-QUANTIZATION-AND-FORMATS.md) |

**Check it yourself — count the stars and licenses on your own** (I did not run exactly this loop; I used individual calls of this kind to collect the data above):

```bash
for r in ggml-org/llama.cpp vllm-project/vllm sgl-project/sglang ollama/ollama antirez/ds4 jundot/omlx llmmanorg/llmman; do
  gh api repos/$r --jq '"\(.stargazers_count)\t\(.full_name)\t\(.license.spdx_id)\t\(.created_at[:10])\t\(.pushed_at[:10])\t\(.archived)"'
done
```

---

## 3. The dependency network: who runs whose code

The most important market fact of this map: **most of the "different" programs for local models run the same engine — llama.cpp.**
The diagram below shows the paths according to the notes from 19 October 2026 (details and evidence in chapters 04–05).

```
                        ┌─────────────────────────── layer 5/6: products ───────────────────────────┐
                        │                                                                           │
   Ollama ──(GGUF)──────┤                                                                           │
   LM Studio ───────────┤                                                                           │
   Jan ─────────────────┤──────────►  llama.cpp  (libllama + llama-server; ggml; backends:          │
   LocalAI (1 of 60+) ──┤                          CUDA · HIP · Metal · Vulkan · SYCL · CPU …)      │
   Lemonade ────────────┤                          ▲                    ▲                           │
   Docker Model Runner ─┤                          │ fork                │ fork / embedded            │
   RamaLama ────────────┤                   ik_llama.cpp          GPT4All (frozen), llamafile,       │
   llmman ──────────────┘                                          KoboldCpp                        │
                                                                                                    │
   Ollama (Apple Silicon, safetensors) ─┐                                                           │
   LM Studio (mlx-engine) ──────────────┼──────►  MLX / mlx-lm  ◄── oMLX (server with SSD cache)    │
   Jan (its own mlx-server) ────────────┘                                                           │
                                                                                                    │
   Docker Model Runner, LocalAI, RamaLama, llmman, Lemonade ──►  vLLM  /  SGLang  (optionally)      │
                                                                                                    │
   ds4 / DwarfStar — a standalone single-model engine (+ forks: GB10, CPU/NVMe, a menu bar app)     │
   TensorRT-LLM — a standalone NVIDIA engine; KTransformers — a plugin for SGLang + its own CPU kernels │
```

Three conclusions:

1. **"Ollama versus llama.cpp" has stopped being a comparison of two engines.** According to the notes, Ollama removed its own GGUF engine in May 2026 (PR #16031 merged 2026-05-29, about −430k lines)
   and now runs the upstream `llama-server` at a pinned version (in the clone I checked: `LLAMA_CPP_VERSION` b11669, while upstream was at b11741 that day) with its own patch layer;
   it has its own runner only for MLX on Apple Silicon. The llmman project's README still describes an older state and is out of date on this point (chapter [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md)).
2. **Two worlds of formats.** GGUF (the llama.cpp world, one file, many quantizations) and HF/safetensors checkpoints with calibrated quantizations (the vLLM/SGLang/TensorRT-LLM/MLX world).
   Moving between them requires conversion and often a change of quantization — chapter [03](03-QUANTIZATION-AND-FORMATS.md).
3. **Concentration of maintainers.** About seven of the twelve largest llama.cpp contributors state in their profiles that they work at Hugging Face (*data from GitHub profiles, self-declared*); ggml.ai joined HF on 2026-02-20.
   This does not change the license (MIT), but it does change who pays for development — chapter [10](10-MONEY-AND-PEOPLE.md).

---

## 4. Five philosophies: why more engines keep appearing

If one engine were best at everything, there would not be a dozen or so of them. They differ in **what they optimize and what they consciously give up**:

| # | Philosophy | What it optimizes | What it gives up | Examples |
|---|---|---|---|---|
| **A** | **One user, any hardware** | single-stream latency; hardware breadth (CPU, AMD, Apple, Vulkan, phones); 1–16-bit quantizations; one file | maximum throughput with hundreds of users; paged KV; mature tensor parallelism | llama.cpp, ik_llama.cpp, KoboldCpp, llamafile |
| **B** | **Many users, server GPUs** | throughput (total tokens per second), memory use through paged KV, shared prefixes, parallelism across many GPUs and nodes | simplicity, low memory use, niche hardware, rich quantizations | vLLM, SGLang, TensorRT-LLM, LMDeploy, (TGI — archive) |
| **C** | **One platform, natively** | full use of one vendor's hardware (Apple unified memory) | portability | MLX, mlx-lm, oMLX |
| **D** | **One model, hard-wired** | speed and memory for *one* model family (graph, quantization and cache written into the code) | generality: every new model is new work | ds4 / DwarfStar |
| **E** | **A narrow niche** | an unusual problem (huge MoE in RAM, the browser, NPUs, embedding in Rust, a cluster of a few Macs) | everything outside the niche | KTransformers, MLC/WebLLM, mistral.rs, exo, NPU stacks |

On top of that comes the **wrapper philosophy** (layer 5): do not optimize the computation, optimize *getting from question to answer* — a model registry, default settings, a chat window.

A table of the dimensions that really matter when choosing ("+" direction = better; this is **my synthesis of chapters 04–08**, not a measurement):

| | A (llama.cpp) | B (vLLM/SGLang) | C (MLX) | D (ds4) | Wrappers |
|---|---|---|---|---|---|
| single-stream speed (batch 1) | + | ± | + (Mac) | + (one model) | depends on the engine underneath |
| total throughput with many requests | ± | **+** | ± (oMLX) | − | depends |
| hardware breadth | **+** | − (NVIDIA > AMD Instinct > the rest) | − (Apple only, a CUDA backend in MLX) | − | depends |
| richness of quantizations (1–8 bit, imatrix) | **+** | ± (FP8/INT4/AWQ) | ± | own layout | depends |
| fresh models "right away" | + (165 architecture files) | + (usually first) | ± | selected | lag (pinned versions) |
| control through flags and build | **+** | + | ± | ± | − (hidden) |
| time to first answer for a newcomer | − | − | ± | − | **+** |

---

## 5. The journey of one request through all the layers

This is what one agent request looks like on your rig (names from your stack; each step has a chapter where it is described in more detail):

```
 agent (Python/TS)                                                       layer 6
   │  POST /v1/chat/completions  {"model":"deepseek", "messages":[…], "tools":[…]}
   ▼
 llama-swap :8080   — reads the "model" field, finds the entry in config.yaml,    layer 7
   │                  if needed unloads another model and starts this one (loading ~110 s)
   ▼
 llama-server       — chat template (Jinja) → prompt; slot selection      layer 4   (ch. 04 §6)
   │                  by longest common prefix; task queue
   ▼
 libllama           — tokenization → ubatch → ggml graph construction      layer 3   (ch. 04 §4)
   │                  writing K/V to the KV cache, context/slots
   ▼
 ggml + HIP backend — graph split across 4 cards (tensor mode),            layer 2   (ch. 04 §2, §8)
   │                  CUDA kernels compiled as HIP for gfx1201
   ▼
 sampling           — a chain of samplers (top-k/top-p/min-p/grammar);     layer 3   (ch. 04 §5)
   │                  verification of the DSpark draft (speculative decoding)
   ▼
 SSE ──► llama-swap ──► agent        the tool-call parser reconstructs `tool_calls`
```

For comparison — the same request in **Ollama** goes through the Ollama server (template, scheduler, parsers) and only then through a child `llama-server` process;
in **vLLM** through the API server → `EngineCore` → scheduler → KV block manager → executor → kernels (chapter [06](06-SERVING-ENGINES-VLLM-SGLANG.md)).

---

## 6. How it came about: a timeline

Repository creation dates come from the GitHub API (verified 2026-10-19); the other events come from the notes, with sources in [`SOURCES.md`](SOURCES.md).

| Date | Event |
|---|---|
| 2022-10-08 | Text Generation Inference (HF) repository created — later archived |
| 2023-02-09 | vLLM repository created (the PagedAttention paper — SOSP 2023) |
| 2023-03-10 | first llama.cpp commit |
| 2023-06-26 | Ollama created |
| 2023-11-28 | MLX repository created (Apple team) |
| 2024-01-08 | SGLang created (RadixAttention) |
| 2024-06-27 | ik_llama.cpp fork |
| 2025-03 | Docker Model Runner, `mlx-lm` as a separate repository |
| 2025-05-06 | vLLM moves under the PyTorch Foundation |
| 2026-02-13 | oMLX created |
| 2026-02-20 | ggml.ai (the creators of llama.cpp) joins Hugging Face |
| 2026-03-22 | llmman created |
| 2026-05-06 | ds4 created (after 5 months ~24k stars) |
| 2026-05-29 | Ollama removes its own GGUF engine (PR #16031) |
| 2026-06-24 / 07-29 | Qualcomm announces / completes the Modular acquisition *(company's own claim; price undisclosed)* |
| 2026-08-26 / 09-03 | press reports of NVIDIA acquiring Hugging Face (see [10](10-MONEY-AND-PEOPLE.md); *I could not establish a statement from either party*) |

The pattern that shows: **2023 = the birth of the engines, 2024–25 = wrappers and specialization, 2026 = consolidation and single-model engines.**

---

## 7. How to read the rest of the course

| If you want to… | Read |
|---|---|
| quickly know what to choose for your use cases | [09](09-COMPARISON-AND-CHOICE.md) (skipping the rest) |
| understand *why* generation has the speed it has (roofline, KV cache, batching, speculation) | [02](02-HOW-INFERENCE-WORKS.md), then [03](03-QUANTIZATION-AND-FORMATS.md) |
| go deep into the engine your production runs on | [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |
| compare the "ready-made" apps with a chat window | [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |
| understand server engines and what works on AMD gfx1201 | [06](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| have a plan for the Macs | [07](07-APPLE-MLX-OMLX-AND-DS4.md) |
| huge MoE in RAM, Rust, the browser, NPUs | [08](08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS.md) |
| understand the market: who pays, who is behind it, the risks | [10](10-MONEY-AND-PEOPLE.md) |
| check the sources | [`SOURCES.md`](SOURCES.md) |

My own measurements on the rig (how I got from 23.5 to about 50 tok/s in llama.cpp) are outside this course: [`../speeding-up-generation/README.md`](../speeding-up-generation/README.md).
This course **contains no new measurements** — it is a map and a reading of the code.

**How to read the confidence tags:** no tag = checked in the code or in a primary source; *(project's own claim / company's own claim)* = a statement by the interested party;
*(press report)* = a report I did not confirm at the source; *(my calculation)* = arithmetic on figures from the sources; *(unverified)* = a guess.
