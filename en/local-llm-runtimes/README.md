# Local LLM Engines — From the Big Picture to Code Details

**As of 19 October 2026.** A course on the programs that run language models on your own hardware: llama.cpp, Ollama, LM Studio, vLLM, SGLang, MLX and oMLX, ds4, llmman
and a dozen or so others. The goal: to understand **what they are, what they do, how they work inside, what they are for and how they differ** — from the market map down to the data structures in the source code —
and (in one separate, non-technical chapter) **how they make money and who is behind them**.

Most of the course is technical. The reference point is one concrete setup (the reference rig): 4× Radeon AI PRO R9700 (ROCm, gfx1201) with llama.cpp and llama-swap, plus a Mac.

> ⚠️ **How this course was made and what it does not promise.** This is **desk research and code reading**: documentation, the GitHub API, research papers, project websites and repositories cloned
> on the rig (read-only; commits in [`SOURCES.md`](SOURCES.md)). **I did not run or measure anything here** — the cards are in production use, so there are no new performance measurements.
> Web search was unavailable in this session (query limit exhausted), so the sources are pages and APIs fetched directly. Funding figures (rounds, valuations) are the weakest link:
> each one carries a source tag. This overview **goes stale within weeks**; some of the material (e.g. acquisitions) is fresh from the last few months.
> Tags: none = checked in the code or a primary source · *(project's own claim / company's own claim)* = a statement by the interested party · *(press report)* = a report not confirmed at the source ·
> *(my calculation)* = arithmetic on figures from the sources · *(unverified)* = a guess.

## Who this is for and how to read it

Each chapter starts with a goal and ends with a **"What this means for the reference setup"** section (practice on the reference hardware) and **"Check it yourself"** boxes — small exercises to do in the real code
(commands from my notes; the ones not run by me are marked as such).

| You want to… | Read |
|---|---|
| see everything in one table and choose an engine | [09 · Comparison and choice](09-COMPARISON-AND-CHOICE.md) |
| understand the structure of the local LLM world | [01 · Map and layers](01-MAP-AND-LAYERS.md) |
| understand why generation is the way it is | [02 · How inference works](02-HOW-INFERENCE-WORKS.md) → [03 · Quantization and formats](03-QUANTIZATION-AND-FORMATS.md) |
| get into the engine the reference setup runs on in production | [04 · llama.cpp and the ggml family](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) |
| understand the "ready-made" apps with a chat window | [05 · Wrappers: Ollama, LM Studio and others](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) |
| understand server engines and the status of AMD gfx1201 | [06 · Server engines: vLLM, SGLang](06-SERVING-ENGINES-VLLM-SGLANG.md) |
| have a plan for the Macs | [07 · Apple: MLX, oMLX, ds4, exo](07-APPLE-MLX-OMLX-AND-DS4.md) |
| learn the niches: huge MoE in RAM, Rust, the browser, NPUs | [08 · Specialists](08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS.md) |
| understand the money and the people (non-technical chapter) | [10 · Money and people](10-MONEY-AND-PEOPLE.md) |
| check where I know things from | [SOURCES.md](SOURCES.md) |

## Table of contents

| # | Chapter | What it covers | Type |
|---|---|---|---|
| 01 | [Map and layers](01-MAP-AND-LAYERS.md) | seven layers from the weights file to the chat window; about 35 projects in tables; the dependency network; five philosophies; a timeline | introduction |
| 02 | [How inference works](02-HOW-INFERENCE-WORKS.md) | prefill and decoding, the roofline on the reference rig, attention and KV cache, MoE, batching, parallelism, speculation, sampling, grammars, templates, measurement methodology, glossary | technical |
| 03 | [Quantization and formats](03-QUANTIZATION-AND-FORMATS.md) | what is in a GGUF file byte by byte; K-/i-quants, MXFP4, AWQ, GPTQ, FP8, oQ, Unsloth Dynamic; quality tables; analysis of your file | technical |
| 04 | [llama.cpp and the ggml family](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) | ggml, GGUF, libllama, KV, `llama-server` from the inside, speculation, multi-GPU split modes, HIP; ik_llama.cpp, llamafile, KoboldCpp, llama-swap | technical (deepest) |
| 05 | [Wrappers](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) | Ollama, LM Studio, llmman, Jan, GPT4All, LocalAI, Lemonade, Docker Model Runner, RamaLama; what breaks when the sponsor changes their mind | technical + market |
| 06 | [Server engines](06-SERVING-ENGINES-VLLM-SGLANG.md) | vLLM (PagedAttention, v1), SGLang (RadixAttention), TensorRT-LLM, TGI, Dynamo, llm-d; vLLM on the R9700 | technical |
| 07 | [Apple and ds4](07-APPLE-MLX-OMLX-AND-DS4.md) | unified memory, MLX, mlx-lm, oMLX, ds4/DwarfStar, exo | technical |
| 08 | [Specialists](08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS.md) | KTransformers, mistral.rs, MLC/WebLLM, NPU stacks; hybrid MoE compared | technical |
| 09 | [Comparison and choice](09-COMPARISON-AND-CHOICE.md) | the matrix, gfx1201, API/offline/telemetry, scenarios, ideas to borrow, experiment plan | practical |
| 10 | [Money and people](10-MONEY-AND-PEOPLE.md) | business models, funding, 2026 consolidation, a directory of people, licenses, dependency risks | **non-technical** |

## Ten things that surprised me (and why they are worth knowing)

1. **Almost all the "different" programs for local models run llama.cpp.** Ollama removed its own GGUF engine in May 2026 and runs the upstream `llama-server` (ch. 05).
2. **llama.cpp has grown from an engine into a platform**: a router mode with model swapping (LRU), Anthropic and Responses endpoints, built-in tools and an MCP client, and even desktop apps (ch. 04).
3. **Tensor mode in llama.cpp is officially "experimental, no guarantees for AMD"** — and on the reference 4× R9700 rig it worked and gave ~50 tok/s (ch. 04, 02 and the [guide on speeding up generation](../speeding-up-generation/README.md)).
4. **On the reference card (gfx1201) really only one engine works: llama.cpp.** vLLM has claimed support without measurements, SGLang has none, ds4 has unmerged patches, and MLX and exo are Mac-only (ch. 09).
5. **For MoE, batching is not "free"**: with 32 parallel sequences you touch about half of the experts, so speculation gives less than on dense models (ch. 02; *(my calculation)*).
6. **Most of the memory traffic per token in the reference model is the dense part, not the experts** — the experts' bits cost capacity, not bandwidth (ch. 03).
7. **ds4 shows a second path: a single-model engine with the disk as a memory tier** — 24k stars in five months; on the reference hardware, though, only with patches (ch. 07).
8. **The 2026 consolidation**: ggml.ai into Hugging Face (2026-02-20), Qualcomm buys Modular, reports of NVIDIA acquiring HF *(press report)*, TGI archived (ch. 10, 06).
9. **Two worlds of formats**: GGUF (one file, many quantizations) versus safetensors with calibrated quants; moving between them is not free (ch. 03).
10. **The biggest risk in a setup like this is not speed but exposure**: if `llama-swap` listens on all interfaces without a password and models start with `--agent` (built-in command execution), anyone on the LAN can run shell commands on the host (ch. 09 and 04).

## Related parts of the repository

- [Speeding up generation](../speeding-up-generation/README.md) — my own measurements and the deployment of speculation + tensor split on the rig (23.5 → ~50 tok/s).
- [AI assistants](../ai-assistants/README.md) and [Agent harnesses](../agent-harnesses/README.md) — the layer *above* the engines: where these engines are used.
- [Local models course](../course_local_models/) — the basics this course assumes you start from.
