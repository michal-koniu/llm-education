# 05 · Wrappers: Ollama, LM Studio and the rest

**Why this chapter.** In chapters 02–04 you got to know the engine: how tokens turn into more tokens, what GGUF is, and what `llama-server` does. This chapter is about the layer **above the engine**: the programs that turn "running a model" into a single command or a single click. After reading it you will be able to say what exactly a wrapper adds to llama.cpp, what you pay for it (control, lag behind upstream, default values, dependence on a company), how Ollama, LM Studio, llmman, Jan, GPT4All, LocalAI, Lemonade, Docker Model Runner and RamaLama differ, which of them are not runtimes at all (Open WebUI, AnythingLLM), and what this knowledge changes on the reference setup: 4× Radeon AI PRO R9700 (gfx1201, ROCm), llama.cpp + llama-swap, plus a Mac.

> ⚠️ **I did not run anything here.** The whole survey is *desk research* and code reading: READMEs, documentation, the GitHub API, shallow clones of the repositories (as of 2026-10-19). I did not install any of the programs described and did not run a single benchmark. For Ollama and llmman I read the code in a clone; for Jan, LocalAI, Lemonade, Docker Model Runner, RamaLama, GPT4All, Open WebUI and AnythingLLM I read the README, files from the repository tree and selected source files fetched through the API, without a full checkout. Where something is not verified, I say so explicitly.

**How to read the evidence tags.** A fact without a tag = verified in a primary source (code, GitHub API, the project's document; I give the path or address). *(project's own claim)* / *(company's own claim)* = the author says so themselves, without independent verification. *(press report)* / *(third-party source)* = e.g. Wikipedia. *(unverified)* / *(my calculation)* = a conclusion, or something I cannot confirm.

## Table of contents

1. [The idea of a wrapper: what it adds, what it costs](#1-the-idea-of-a-wrapper)
2. [Ollama in depth](#2-ollama-in-depth)
3. [LM Studio in depth](#3-lm-studio-in-depth)
4. [llmman: models as OCI images](#4-llmman-models-as-oci-images)
5. [Jan, GPT4All, LocalAI, Lemonade, Docker Model Runner, RamaLama](#5-the-remaining-wrappers)
6. [Frontends that are not runtimes: Open WebUI and AnythingLLM](#6-frontends-that-are-not-runtimes)
7. [What breaks when the sponsor changes their mind](#7-what-breaks-when-the-sponsor-changes-their-mind)
8. [What this means for the reference setup](#8-what-this-means-for-the-reference-setup)
9. [What I could not establish](#9-what-i-could-not-establish)

Related chapters: the engine that all these programs wrap — [`04-LLAMA-CPP-AND-THE-GGML-FAMILY.md`](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md); the file format — [`03-QUANTIZATION-AND-FORMATS.md`](03-QUANTIZATION-AND-FORMATS.md); the MLX path on a Mac — [`07-APPLE-MLX-OMLX-AND-DS4.md`](07-APPLE-MLX-OMLX-AND-DS4.md); server engines that some of the wrappers can run — [`06-SERVING-ENGINES-VLLM-SGLANG.md`](06-SERVING-ENGINES-VLLM-SGLANG.md); money and people — [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md); the final choice — [`09-COMPARISON-AND-CHOICE.md`](09-COMPARISON-AND-CHOICE.md).

---

## 1. The idea of a wrapper

### 1.1 Where it sits in the stack

Think of the difference between a car engine and a car. `llama-server` is the engine: it receives a path to a `.gguf` file, a port and a handful of flags, and in return exposes an HTTP API for generating tokens. It does not know where to get a model from, does not remember which model you loaded last, and will not free VRAM after an hour of idleness (admittedly, `llama-server` now has its own router mode, more on that in section 8). **A wrapper is everything around that engine.**

To be precise: a wrapper is a program that does not multiply matrices itself, but launches and supervises another program that does.

```
 app / agent / IDE / Open WebUI
            │  HTTP: OpenAI / Anthropic / Ollama API
            ▼
 ┌────────────────────────────────────────────┐
 │  WRAPPER (Ollama, LM Studio, Jan, …)       │
 │  · model registry (pull / push / catalog)  │
 │  · lifecycle (load, keep, release)         │
 │  · defaults (context, parallelism)         │
 │  · API translation, chat templates         │
 │  · GUI / CLI / updates / packaging         │
 └───────────────┬────────────────────────────┘
                 │  child process, HTTP on 127.0.0.1:<random port>
                 ▼
 ┌────────────────────────────────────────────┐
 │  ENGINE: llama-server (llama.cpp), MLX, …  │  ← tokens are computed here
 └───────────────┬────────────────────────────┘
                 ▼
          ggml / MLX → CUDA, ROCm, Vulkan, Metal, CPU
```

The conclusion on which the whole chapter rests: **almost all wrappers run the same engine**. As of October 2026, Ollama (the GGUF part), LM Studio (the GGUF part), Jan, LocalAI (one of 60+ backends), Lemonade, Docker Model Runner, RamaLama and llmman run GGUF through llama.cpp; GPT4All through its own fork of llama.cpp. They differ in **packaging, model distribution, load scheduling, API overlays and money — not in matrix multiplication**.

### 1.2 What a wrapper adds

| Addition | What it means in practice | Example from this chapter |
|---|---|---|
| **Model registry** | `ollama pull qwen3` instead of searching for a file on Hugging Face, choosing a quantization and downloading by hand; metadata (template, parameters, license) travels together with the weights | manifest + blobs in Ollama; OCI images in llmman, Docker Model Runner, RamaLama |
| **Lifecycle** | The model loads on the first request, sits in memory for the *keep-alive* period, then is released; several models can coexist | `OLLAMA_KEEP_ALIVE` = 5 min; JIT + TTL in LM Studio |
| **Defaults** | It chooses for you the context window, number of slots, number of layers on the GPU, *flash attention* | context depending on the amount of VRAM in Ollama |
| **API translation** | One server speaks OpenAI, Anthropic and Ollama at the same time; chat messages are turned into a prompt with the right template, tool calls (*tool calls*) are parsed from the response | `model/renderers`, `model/parsers` in Ollama |
| **GUI and packaging** | Installer, updates, tray icon, model search, chat | LM Studio, Jan, the Ollama app |
| **Hardware detection** | It checks by itself what GPU you have and picks the matching engine build | `discover/` in Ollama; image selection by environment variable in RamaLama |

### 1.3 What it costs

1. **Control.** The flags you need (`--n-cpu-moe`, your own tensor split between cards, specific speculative decoding settings) are available only if the wrapper exposes them. There are fewer `OLLAMA_*` variables than `llama-server` flags.
2. **Lag behind upstream.** A wrapper pins the engine version: Ollama `LLAMA_CPP_VERSION` b11669 (in the clone I checked), llmman b11429, Docker Model Runner `LLAMA_SERVER_VERSION=b9879`. The lower the build number, the older the engine; b9879 vs b11669 is about 1800 builds of difference *(my calculation, I did not check tag dates)*. The production build of the reference rig, `0ce8cd1`, is identified by a hash, so I cannot compare it with `bNNNNN` numbers without the git history (the clones are shallow).
3. **Defaults that quietly spoil results.** The loudest one: a small context. Ollama now picks the context according to VRAM (section 2.6), but a user with a small card still gets 4k, and truncation of the history is sometimes not reported (issue #14259).
4. **On-disk format.** If a wrapper stores models as its own blobs, other programs cannot read them without an export.
5. **Dependence on the sponsor.** A wrapper is a product of somebody's company, and that company decides on the roadmap, cloud upsell, license and telemetry. Section 7 collects this in a table.

### 1.4 Comparison table (engine, license, who steers)

Stars from the GitHub API, 2026-10-19.

| Product | Engine underneath | License | Stars | Who steers the roadmap |
|---|---|---|---|---|
| **Ollama** | upstream `llama-server` (GGUF) + its own **MLX** runner (Apple Silicon, safetensors) | MIT | 183,857 | Ollama, Inc. (a VC-backed company) |
| **LM Studio** | closed-source "LM Runtimes": llama.cpp builds + the MLX engine (`mlx-engine`, MIT) | closed-source app (freeware); `lms`, SDK, `mlx-engine` MIT | `lms` 5,360; `mlx-engine` 1,189 | Element Labs, Inc. |
| **llmman** | untouched upstream llama.cpp / vLLM / SGLang / mlx-lm / ds4-server | Apache-2.0 | 563 | Eric Curtin (a Docker employee), one person |
| **Jan** | llama.cpp linked statically in the worker process (since v0.8.5) + its own `mlx-server` in Swift | Apache-2.0 + a request for attribution (GitHub: NOASSERTION) | 45,017 | Menlo Research |
| **GPT4All** | its own fork of llama.cpp (`llama.cpp-mainline`), Vulkan | MIT | 77,350 | Nomic AI (a de facto dormant project) |
| **LocalAI** | 60+ backends as OCI images behind gRPC (llama.cpp, vLLM, SGLang, MLX, whisper.cpp, diffusers…) | MIT | 49,695 | Ettore Di Giacinto (`mudler`) + sponsors |
| **Lemonade** | llama.cpp (Vulkan/ROCm/CUDA/Metal/CPU), FastFlowLM and Ryzen AI OGA (NPU), vLLM-ROCm, whisper.cpp… | Apache-2.0 | 5,936 | community + AMD engineers |
| **Docker Model Runner** | llama.cpp (default), vLLM, SGLang, MLX, Diffusers | Apache-2.0 | 658 | Docker, Inc. |
| **RamaLama** | llama.cpp / vLLM / stable-diffusion / OpenVINO in per-GPU images | MIT | 3,086 | the `containers` org, maintainers from Red Hat |
| **Open WebUI** | none (frontend) | custom: BSD-3 + a branding clause (since v0.6.6) | 156,189 | Open WebUI Inc. |
| **AnythingLLM** | none by default; optionally a built-in engine (llama.cpp/Lemonade) | MIT | 67,323 | Mintplex Labs |

### 1.5 Comparison table (API, interface, offline mode)

| Product | API | Interface | Offline |
|---|---|---|---|
| **Ollama** | its own `/api/*`, OpenAI (including `/v1/responses`), Anthropic `/v1/messages` | CLI + app (macOS/Windows); Linux: CLI/systemd | Inference works offline (`--offline`); it reaches the network for updates (app), models from the registry, optionally the cloud (`OLLAMA_NO_CLOUD=1` disables it) |
| **LM Studio** | native REST, OpenAI, Anthropic `/v1/messages`; port 1234 | GUI (Electron) + `lms` + the `llmster` daemon | Works offline once models are downloaded; network: updates, model search/download, cloud features; privacy statement *(company's own claim)* |
| **llmman** | Ollama, OpenAI, Anthropic, Gemini | CLI + web UI under `/` | Offline after engines are cached (`serve --pull-only`); I did not search for telemetry *(unverified)* |
| **Jan** | OpenAI on `localhost:1337` | GUI (Tauri) | Offline; analytics opt-in (PostHog EU) *(project's own claim)* |
| **GPT4All** | no description of an API server in my notes | GUI (Qt) + Python | Local models offline; I could not establish telemetry |
| **LocalAI** | OpenAI, Anthropic, Ollama, ElevenLabs, Realtime | server + `local-ai` CLI | Offline after the backend and model are downloaded (first use requires the network) |
| **Lemonade** | OpenAI, Anthropic, Ollama | CLI, tray, web/Electron app | Offline; backends and models downloaded on first use; "zero telemetry" *(project's own claim)* |
| **Docker Model Runner** | OpenAI (`:12434`), Ollama, Anthropic, Responses | `docker model …`, Docker Desktop | no description in my notes; models from Docker Hub, OCI registries or HF |
| **RamaLama** | `ramalama serve` (details not described) | CLI | Container without network by default; images from quay.io |
| **Open WebUI** | a consumer of other people's APIs | web (FastAPI + Svelte) | depends on the backend |
| **AnythingLLM** | a consumer of other people's APIs (Ollama, LM Studio, LocalAI…) | desktop + Docker | depends on the backend |

---

## 2. Ollama in depth

**In one sentence:** a Go daemon (`ollama serve`, port 11434) + CLI + desktop app + an OCI-like model registry (ollama.com) that starts a separate engine process for every model; as of 2026 that engine is the upstream `llama-server` (GGUF models) or its own MLX runner (Apple Silicon), plus a paid cloud, "Ollama Cloud".

### 2.1 Who is behind it

Ollama, Inc.; co-founders Jeffrey Morgan (`jmorganca`, previously Docker, Twitter, Google) and Michael Chiang (`mchiang0610`); both co-created Kitematic, bought by Docker in 2015. According to its own post of 2026-07-09, the company raised **88 million USD** (Benchmark, Theory Ventures, 8VC and others) *(company's own claim)*; Wikipedia gives 65 million *(third-party source)*. I did not resolve this discrepancy: I do not know whether 88 million is a single round or a sum. The code is under the MIT license, but the model registry, templates, parsers and the cloud are a separate matter. Revenue comes from cloud subscriptions (Free / Pro 20 USD / Max 100 USD / Team 500 USD per month, billed per token). Details in [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

### 2.2 What it is for

So that `ollama run <model>` works on a laptop without configuration: it downloads quantized weights, sets sensible defaults and exposes an always-on local REST API that every agent and every IDE talks to. As of 2026 it is also a ramp to the cloud: `ollama launch claude|codex|opencode` starts a coding agent against a local **or** cloud model (`docs/cloud.mdx`).

What Ollama deliberately is **not**: a high-throughput server (`NUM_PARALLEL` is 1 by default), a training tool or a multi-tenant gateway.

As of 2026-10-19: MIT, Go (app UI in TS/React, native parts in C/C++ via CMake), repository from 2023-06-26, **183,857 stars**, ~5,917 commits. Latest stable: **v0.40.6 (2026-10-16)**; the numbering jumped (0.24 → 0.30 on 13–14 May 2026 → 0.35 → 0.40 on 2026-09-25), a tag every 2–4 days. Sizes of the Go code (with tests): `cmd/` 63K lines, `server/` 40K, `model/` (parsers and renderers) 39K, `mlxrunner/` 32.6K, `app/` 26K, `llm/` 9.7K, `discover/` 5.4K; C++: `llama/compat/llama-ollama-compat.cpp` 3,507 lines.

### 2.3 What changed in 2026: Ollama no longer has its own GGUF engine

This is the most important change in this chapter and the place where older sources are out of date, so I write down exactly **what is verified and what is not**.

**Verified (GitHub API and the code in the clone):**

- PR **#16031** "runner: Remove CGO engines, use llama-server exclusively for GGML models" was merged on **2026-05-29**: +28K / −430K lines, ~1100 files. It removed the vendored ggml, the CGO runner and the Go-native model implementations ("Ollama's engine").
- The rationale in the PR description: adopting features from llama.cpp faster.
- Today GGUF is run by **upstream `llama-server` as a child process**. The version is pinned by the `LLAMA_CPP_VERSION` file (**b11669** in the clone). `llama/README.md` describes: fetching the pinned sources, applying the patches from `llama/compat/`, building `llama-server`. The main `CMakeLists.txt` says the same in a comment ("GGML backend for inference is provided by llama-server (built separately … using FetchContent from the pinned llama.cpp source)").
- The clone has **no** `ml/backend` directory (the old in-process engine). The only remnant of the name is a comment in `mlxrunner/embed.go` ("old ollamarunner"). The `ggml` tag in manifests is today only a legacy marker; such manifests also go to `llama-server`.
- Safetensors models on Apple Silicon run on **its own MLX runner** (`mlxrunner/`, 32.6K lines): this is still Ollama's own code, only about MLX, not ggml.

**What this means precisely.** Ollama does not ship an *unmodified* `llama-server` binary. It takes the upstream sources at a pinned version, applies a **small layer of patches** (`001-llama-cpp-hooks.patch`) plus the `llama-ollama-compat.cpp` code, and builds. This differs from llmman, which runs the engines without any modifications.

**Discrepancy with an older description.** The llmman README contains a comparison table in which Ollama is described as "Bundled llama.cpp/ggml fork plus Ollama's own engine". After 2026-05-29 that is untrue, so the llmman README is out of date on this point *(checked by comparing against Ollama's code)*. The same applies to every 2025 text about "Ollama's new engine versus llama.cpp". Until 29 May 2026 Ollama really did run its own engine in Go on a vendored ggml, so such texts were correct in their time.

**What the evidence does NOT settle:**

- **The chronology of the switch.** The v0.30.0 tag dates from 2026-05-13/14, PR #16031 was merged on 2026-05-29, and the blog post about faster work after the move to GGUF/llama.cpp is from 2026-06-05. The order of the tags suggests that the path through `llama-server` may have existed earlier alongside the old engine (behind a flag or in the 0.30 line) *(unverified)*. All that is established is that from 2026-05-29 the old engine was removed.
- **Performance.** Ollama's blog (2026-06-05) claims that after the move to llama.cpp it is "up to 20% faster on NVIDIA" (Gemma 4 26B, RTX 5090, Q4_K_M) *(company's own claim)*. I did not check an independent measurement; I read only this one range.
- **Whether the patches are "small".** `llama/compat/` alone is ~4.5K lines (the patch + `llama-ollama-compat.cpp` 3,507 lines). I call it a "small layer" following my notes; count it yourself when you read it.

> **Check it yourself #1: does Ollama really have no GGUF engine of its own.**
> In the clone `~/runtimes-src/ollama/` *(not run by me, paths from my notes)*:
> ```
> cat LLAMA_CPP_VERSION
> sed -n '1,60p' llama/README.md
> grep -rn "ollamarunner" --include=*.go . | head
> ls ml 2>/dev/null || echo "no ml/"
> ```
> Through the GitHub API (requires a logged-in `gh`): `gh api repos/ollama/ollama/pulls/16031` — title, merge date, number of changed files. For the other side of the dispute, open the comparison table in the llmman README (`grep -n -i ollama ~/runtimes-src/llmman/README.md`) and compare it with the above.

### 2.4 Request flow and runner processes

```
HTTP (gin, server/routes.go, 3,653 lines)
   │  GenerateHandler / ChatHandler: resolve the model (manifest → blobs)
   ▼
Scheduler.getRunner   (server/sched.go, 1,851 lines)
   │  runnerRef  ──►  llm.LlamaServer
   ▼
HTTP to a child process on 127.0.0.1:<random port>
   │  llama-server  (GGUF)      or      mlxrunner (safetensors, Apple Silicon)
   ▼
token stream → rewritten into Ollama / OpenAI / Anthropic JSON
```

**A child process: isolation as a design decision.** `llm/llama_server.go` starts `llama-server` with the flags: `--model <blob> --port N --host 127.0.0.1 --no-webui --offline`, `-c NumCtx×numParallel`, `-np numParallel`, optionally `--cache-type-k/v` (from `OLLAMA_KV_CACHE_TYPE`), `--flash-attn on|off|auto`, `--split-mode none --main-gpu N` for placement on a single card, `--mmproj` (vision), `--lora`, `--context-shift`, speculative decoding flags (`--spec-type`, `--spec-draft-model`) and `--load-mode dio|none`. The number of layers on the GPU, threads and the fit to memory (`LLAMA_ARG_FIT`, `LLAMA_ARG_FIT_TARGET`) are determined by `llama-server` itself.

Why a separate process? Because `GGML_ASSERT` calls `abort()`: an error in the engine must not kill the daemon that holds the state of all models. (The same decision stands behind the worker process in Jan, section 5.1.)

**The MLX runner.** Safetensors models go to a different child (`mlxrunner.Execute`, flags `--model --port`). This is a reimplementation of model architectures in Go on C bindings to MLX (`mlx/`, `mlxrunner/`): a trie for the prefix cache (`cache_trie.go`), grammar masks (`grammar.go`, xgrammar), speculative decoding (`speculate.go`, `dflash.go`, `mtp.go`), tokenizer, sampler. More about MLX in [`07-APPLE-MLX-OMLX-AND-DS4.md`](07-APPLE-MLX-OMLX-AND-DS4.md).

### 2.5 Which engine for which model

The manifest carries a "runner" marker: `mlx`, `llamacpp` or `ggml` (legacy). The order of preference depends on the platform:

| Platform | Preference | Effect |
|---|---|---|
| Apple Silicon (darwin/arm64) | **mlx > llamacpp > ggml** | since **v0.40.0 (2026-09-25)** architectures supported by MLX "run on MLX automatically" |
| Linux, Windows, Intel Mac, and on Apple Silicon models without an MLX implementation | **llamacpp > ggml > mlx** | GGUF through `llama-server` |

Architectures registered in `mlxrunner/model/architectures/architectures.go`: llama, qwen3, qwen3_5, qwen3_5_moe, qwen4_exp, gemma4 (+embedding), glm4_moe_lite, laguna, nemotron_h, cohere2_moe, and in addition "decider" models (clef, kev, laya, strands, pplxdecider, glimmer, dflash). The practical conclusion: if on a Mac you have a model outside this list, you get GGUF through llama.cpp, not MLX.

### 2.6 The scheduler and defaults

This part is the heart of a "wrapper": Ollama itself manages what you do by hand with llama-swap. Everything is from `server/sched.go` and `envconfig/config.go`.

- **Queue.** A single loop (goroutine) `processPending` consumes the `pendingReqCh` channel with a buffer of `OLLAMA_MAX_QUEUE` (default **512**); overflow yields `ErrMaxQueue`.
- **Loading.** A map `loaded map[string]*runnerRef`. If the model is loaded and `needsReload` is false (context, options, adapters and projectors unchanged), the request joins the existing runner (a reference counter). Otherwise a load happens, and **only one model loads at a time** (`activeLoading`), although requests to already loaded models proceed in parallel.
- **Limit of loaded models.** `OLLAMA_MAX_LOADED_MODELS`; when unset (0), it is `defaultModelsPerGPU (=3) × max(GPU count, 1)`. When the limit is reached, `findRunnerToUnload` evicts a model according to `ByDurationAndName` (shortest remaining session / longest idle). On out-of-memory at load time: `evictAllAndWait` + one retry (`oomRetryAttempted`).
- **Keep-alive.** `OLLAMA_KEEP_ALIVE` defaults to **5 minutes**; a negative value = forever, 0 = release immediately; `keep_alive` in the request takes precedence. Technically: an `expireTimer` counter on the runner.
- **Parallelism.** `OLLAMA_NUM_PARALLEL` defaults to **1** (`envconfig.NumParallel`); forced to 1 for embedding models and for architectures marked as unsafe (mllama, qwen3vl, qwen35, qwen3next, lfm2, nemotron_h…). Slots are `-np` in `llama-server`, and the allocated context is `NumCtx × numParallel`. So by default you have one slot per model: serving many parallel requests to the same model requires raising this parameter (and paying for it with the KV cache) *(my calculation from the parameter descriptions)*.
- **Placement on multiple GPUs** (`selectLlamaServerPlacement`). With several cards: it groups GPUs by library (`ml.ByLibrary`), then (unless `OLLAMA_SCHED_SPREAD` is set) **first tries to fit the whole model on one, the best card** (`bestSingleGPUFit` → `--split-mode none --main-gpu N`); if it does not fit, it uses the group with the most free memory, and `llama-server` splits the layers. The VRAM requirement is predicted from GGUF metadata (`llm.PredictServerVRAM`); when other models are present, the threshold is 80% of free memory. `mmap` is sometimes disabled heuristically (`disableMmapDefaultReason`); on lack of memory Ollama automatically reduces the batch size and the context (`reduceAutoNumCtxForLoadOOM`).
- **The default context window** depends on VRAM (`docs/context-length.mdx`): **< 24 GiB → 4k, 24–48 GiB → 32k, ≥ 48 GiB → 256k**; cloud models run at the maximum. The same documentation says that agents, coding and search "should have at least 64000 set". Override: `OLLAMA_CONTEXT_LENGTH`, `num_ctx`, the slider in the app. For the reference 4×32 GB rig *(my calculation)* the automatic threshold would land in the top bracket — but I could not establish whether the threshold is computed from the VRAM of one card or from the sum of the cards, so do not take that as certain.

Note the overlap with llama-swap's ideas: TTL = keep-alive, groups = a limit of models per GPU, but in what I read there is no equivalent of a *matrix* of eviction costs (cf. [`04-LLAMA-CPP-AND-THE-GGML-FAMILY.md`](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md), the section about llama-swap).

> **Check it yourself #2: the defaults.**
> In the Ollama clone *(not run by me)*: `grep -n "KeepAlive\|NumParallel\|MaxQueue" envconfig/config.go` shows 5 minutes, 1 and 512; `grep -rn "defaultModelsPerGPU" server/` — the multiplier 3; `sed -n '1,80p' docs/context-length.mdx` — the 4k/32k/256k thresholds and the sentence about 64000 for agents.

### 2.7 Modelfile

A Dockerfile-style file (`docs/modelfile.mdx`), instructions: `FROM`, `PARAMETER`, `TEMPLATE`, `SYSTEM`, `LICENSE`, `MESSAGE`, `REQUIRES`, `CAPABILITY`. Import from GGUF or safetensors. With `ollama create` you build a new model from it: the weights stay unchanged, and layers (template, parameters, system prompt) are added to the manifest. This is an important point: **the chat template and parameters are part of the model**, not a separate server configuration. In llama.cpp the equivalents are `--jinja`, `--chat-template` and the flags in `cmd` in the llama-swap configuration.

### 2.8 The registry: manifest and blobs

Models live under `~/.ollama/models`:

```
~/.ollama/models/
  blobs/sha256-<digest>                       ← GGUF weights, template, parameters… as files named by hash
  manifests/<host>/<namespace>/<name>/<tag>   ← JSON manifest
```

The manifest is the Docker distribution schema (`application/vnd.docker.distribution.manifest.v2+json`): `config` (JSON with the model format, family and quantization, type `application/vnd.docker.container.image.v1+json`) and a `layers[]` list with its own media types:

| Layer type | Content |
|---|---|
| `application/vnd.ollama.image.model` | GGUF weights |
| `.projector` | multimodal projector |
| `.adapter` | LoRA |
| `.embed`, `.tensor`, `.draft` | embeddings, safetensors, a draft model for speculative decoding |
| `.template`, `.system`, `.params`, `.messages`, `.license` | template, system prompt, parameters, example messages, license |

New: **manifest lists** (`application/vnd.ollama.manifest.list.v2+json`), whose children carry `runner` and `format` fields, so that one tag can offer both an MLX build and a GGUF one. Downloading and uploading go through the HTTP API of the ollama.com registry (OCI-like, with its own authorization; the `transfer/` package, `OLLAMA_MAX_TRANSFER_STREAMS=4`).

The consequence: **the model file does not lie on disk as `name.gguf`**, only as a `sha256-…` blob. Other programs do not recognize it without an export (this argument is raised by the llmman README *(project's own claim)*). The upside of this decision: layer deduplication and hash verification.

### 2.9 API

Registered in `server/routes.go` (around lines 2362–2425): **native** `/api/generate`, `/api/chat`, `/api/embed`, `/api/pull|push|create|copy|delete|show|tags|ps`, `/api/blobs/:digest`, account (`/api/me`, `/api/usage`…), experimental `web_search` and `web_fetch`; **OpenAI** `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/models`, `/v1/responses`, `/v1/audio/transcriptions`; **Anthropic** `/v1/messages` (`anthropic/anthropic.go`); `/v1/systemone` ("decider models", v0.35.0, 2026-09-28).

Tools, "thinking" (*thinking*), vision, embeddings and structured output (a JSON schema in the `format` field, passed to `llama-server` as `json_schema` or a GBNF grammar) are described in `docs/capabilities/`. Messages are turned into a prompt by **renderers and parsers in Go** (`model/renderers`, `model/parsers`, `harmony/`); models without them use the `chat_template` from `llama-server`. Integrations (`docs/integrations/`): Claude Code, Codex, OpenCode, Cline, Roo, Zed, JetBrains, VS Code, Xcode, n8n, goose and others.

This is Ollama's main strength: **every agent tool has an "Ollama provider"**. If you write your own agent applications, you most likely need only an OpenAI-compatible endpoint anyway, which `llama-server` has too.

### 2.10 The compat layer: translating GGUF in memory

Models published in Ollama's registry before 2026 may not fit the upstream loaders. That is why `llama/compat/` (≈4.5K lines) translates metadata and tensor layout **in memory, at load time**, for ~20 architectures (among others gemma3/3n/4, gpt-oss, qwen3.5/3-vl/3-next, mistral3, llama4, lfm2, olmo3, deepseek-ocr, glm-ocr, nemotron-h). `llama/compat/README.md` itself calls this layer "temporary … meant to live briefly". An idea worth remembering: translate at load time instead of forcing everyone to re-download all models.

### 2.11 Cloud, telemetry and offline mode

- **Inference is offline**: `llama-server` starts with `--offline`, the engine never touches the network.
- **The desktop app asks about updates:** `app/updater/updater.go` makes a GET to `https://ollama.com/api/update?os&arch&version&ts&nonce`, signed with a local key; on macOS a device identifier (`id`) is added.
- **Model downloads** come from ollama.com; optional login, cloud and web search use further endpoints.
- **Telemetry:** in the `app/` directory I found no analytics SDK (grep for posthog/segment/mixpanel). That is only a grep over the client code; telemetry on the ollama.com side cannot be audited.
- **Disabling the cloud:** `OLLAMA_NO_CLOUD=1` or `disable_ollama_cloud` in `~/.ollama/server.json` (`docs/faq.mdx`). For an environment cut off from the network: copy `~/.ollama/models`.
- **Exposure to the network:** the server listens on `127.0.0.1:11434` by default (`OLLAMA_HOST` changes this). Wikipedia describes Ollama servers exposed to the internet and found by SentinelOne and Censys *(third-party source)*. Conclusion: do not set `OLLAMA_HOST=0.0.0.0` without a firewall or authentication in front of it.

### 2.12 Criticism: both sides

Each charge was checked against primary sources where possible.

| Charge | What the source says | The other side | My conclusion |
|---|---|---|---|
| **1. No attribution of llama.cpp / license notices** | Issue **#3185** "ollama doesn't distribute notice licenses in its release artifacts" (opened 2024-03-16, still **open**, 59 comments): MIT requires preserving copyright notices in binary distribution; the reporter did not find "Georgi Gerganov" in the Linux/Windows installs | The README now has a "Supported backends" section with thanks to Georgi Gerganov's llama.cpp project; the blog for version 0.30 thanks the creators of llama.cpp and NVIDIA, AMD, Qualcomm, Intel *(company's own claim)*. After PR #16031 Ollama is a thin consumer of upstream, so the charge of a "fork obscuring the source" changes character | Whether the missing notices were fixed, **I could not establish** (the clone has no NOTICE/THIRD_PARTY files in the root). The 2024 charge is formal, not about code quality |
| **2. Model naming** | Issue **#8557** "Please separate deepseek-r1 from deepseek-r1-Distill!" (2025-01-24, open): distillates onto Qwen/Llama were presented as `deepseek-r1:7b` etc. | — | The existence of the issue is checked; the current state of the library is not *(unverified)*. A rule for the future: read the model card, not the tag |
| **3. Small default context** | Today the threshold depends on VRAM (4k / 32k / 256k). Before 2026 the defaults were 2048/4096 *(unverified, from the memory of the author of the notes)*. Issue **#14259** "Chat history and embedding truncation happens silently" (opened 2026-02-14) | The documentation openly says that agents need 64,000+ | Irrelevant for you with large VRAM, but important for people with small cards who read "Ollama is dumb" |
| **4. Slower than llama.cpp** | Until May 2026 its own engine in Go on a vendored ggml could produce differences | Its own claim "up to 20% faster on NVIDIA" after the move to llama.cpp indirectly confirms that there were differences *(company's own claim)* | Today the engine is the same, so the difference is mainly the defaults (parallel=1, context thresholds) and the hop through the proxy. I did not check independent measurements (among others I skipped the gpt-oss benchmarks from 2025) |
| **5. Coupling to the cloud** | Login, `ollama launch`, search and cloud models are first-class in the CLI and the app | There is a switch `OLLAMA_NO_CLOUD` | Reasonable: a local user can turn it off, but the default flow leads to an account |
| **6. Exposure and security** | Servers exposed to the internet *(third-party source)* | Loopback by default | The user's responsibility, but a mistake that is easy to make |
| **7. Release pace** | A tag every few days; open issue **#17878** (2026-08-19): embeddings silently returning zero vectors under load | — | Do not deploy `latest` to production; pin the version |

### 2.13 Performance

The latency of a single stream is roughly the same as in llama.cpp itself (the same engine) plus a hop through a Go proxy. Throughput is limited by the default configuration: `NUM_PARALLEL=1`, 3 models per GPU, one load at a time, 5 minutes of keep-alive. I did not read the posts about the MLX engine (2026-03-30, 06-11, 06-29) in full *(company's own claim)*. I do not give my own tok/s figure for Ollama.

### 2.14 Ollama and the reference rig with AMD cards

- `docs/gpu.mdx` lists the **Radeon AI PRO R9700 / R9600D** in the ROCm section. **ROCm v7 is required** (Linux and Windows). Vulkan is enabled by default ("no vendor library needed"). Variables: `HIP_VISIBLE_DEVICES`, `ROCR_VISIBLE_DEVICES`, `HSA_OVERRIDE_GFX_VERSION`, `GGML_VK_VISIBLE_DEVICES`, `OLLAMA_VULKAN=0`.
- So Ollama **should** work on the R9700 (gfx1201). The notes do not say whether anyone has checked this on their own machine; neither have I.
- Placement on multiple GPUs: first the whole model on one card, and if it does not fit, `llama-server` splits the layers. The notes **do not say** whether Ollama exposes the split modes known from the guide [`../speeding-up-generation/README.md`](../speeding-up-generation/README.md) (tensor parallel, per-card ratio). For a 284B model in IQ3_XXS on four cards it is exactly these settings that decide 50 tok/s, so check before switching.

### 2.15 When to choose Ollama

When you want the shortest path from zero to a working model on a Mac or laptop; when the tool you use has only an "Ollama provider"; when you want a library of models with ready-made templates and tool-call parsers; when on a Mac you want MLX without your own configuration. **Do not choose it** when you need full control over the engine flags, GGUF files in an ordinary directory, or strict pinning of the llama.cpp build.

---

## 3. LM Studio in depth

**In one sentence:** a closed-source desktop application (Electron) for finding, downloading and running models locally, with an engine layer in the form of closed "LM Runtimes" (llama.cpp builds + MLX) and an open CLI, SDK and MLX wrapper; since version 0.4.0 also a headless daemon (`llmster`); since July 2026 a second, separate product, **Bionic**, exists alongside.

### 3.1 Who is behind it

The company **Element Labs, Inc.** (terms of 2026-08-23). First release in May 2023 *(third-party source: Wikipedia)*; the GitHub organization `lmstudio-ai` was created on 2023-05-16. The text about free use at work is signed by Yagil Burowski; I did not verify their formal title. **I did not find funding or founders** on the company's pages or in Wikipedia: I leave this blank instead of guessing. In April 2026 the **Locally AI** team (an iOS/Mac app, Adrien Grondin) joined LM Studio, terms undisclosed. Money and people: [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

### 3.2 What is open and what is closed

This is the most common misunderstanding, so a table:

| Element | Status | Notes |
|---|---|---|
| Desktop application (Electron) | **closed**, free (freeware) | the source code is not in any repository; `lmstudio-bug-tracker` is only an issue tracker |
| The `llmster` daemon, llama.cpp builds ("LM Runtimes") | **closed** | the organization has no llama.cpp fork |
| Model hub backend, LM Link, Bionic | **closed** | SaaS / services |
| The `lms` CLI | MIT, 5,360 stars, TypeScript | part of the `lmstudio-js` monorepo; "cannot be built standalone" |
| The SDKs `lmstudio-js` (1,798), `lmstudio-python` (884; last push 2025-10-27) | MIT | |
| `mlx-engine` (1,189, Python) | MIT | built on mlx-lm, Outlines and mlx-vlm |
| `model-catalog` (803) | Apache-2.0 | model descriptions in JSON |
| `docs`, `configs`, `venvstacks`, `nq`, `localization` | open | `office-document-processor-sources` (MPL-2.0) appeared on 2026-10-06 |

Conclusion: **the clients and plugins are open, the middle is closed**. You cannot audit or patch the runtime, nor point to an arbitrary llama.cpp commit. `lms` and the SDKs still need a running closed-source app or daemon.

### 3.3 Three ways to use it: the app, `lms`, `llmster`

According to the documentation (`lmstudio-vs-llmster-vs-lms.md`):

- **The LM Studio app:** search and download from Hugging Face, chat, RAG over documents, presets, a local server, MCP.
- **`llmster`:** a screenless daemon: "a Linux server, a GPU rig without a monitor, CI/CD, a service starting with the system". Installation: `curl -fsSL https://lmstudio.ai/install.sh | bash` (Windows: `irm …/install.ps1 | iex`), then `lms daemon up` and `lms server start`. The installer comes from my notes and I did not run it; do not run `curl | bash` on the rig without reading the script.
- **`lms`:** the CLI: `get`, `load`, `ls`, `ps`, `server start`, `chat`, `log stream`, `runtime ls|get|select|remove|update`.

### 3.4 Server, API, MCP, parallelism

- **Default port 1234.** Native REST (`/api/v1/…`) with a stateful `/v1/chat` (fields `response_id`, `previous_response_id`, since 0.4.0): the server remembers the conversation and the client sends back only the identifier of the previous response.
- **OpenAI compatibility** (chat, completions, embeddings, structured output) and **Anthropic compatibility**: the documentation lists only `POST /v1/messages`; streaming and tools are not described on that page.
- **JIT and TTL:** the model loads on the first request and is released automatically after idleness (headless mode documentation). The same pattern is in Ollama and llama-swap.
- **MCP:** `mcp.json` in Cursor notation, local and remote servers, with a warning about arbitrary code; 0.4.0 added to REST "locally configured MCP with permission key control".
- **Parallel requests and continuous batching** (*continuous batching*) came with "llama.cpp engine 2.0.0" in version 0.4.0 ("max concurrent predictions" settings and a unified KV); MLX parallelism was described in January 2026 as "coming soon".
- **LM Link** (blog 2026-06-04): end-to-end encrypted remote access to local models from other devices, e.g. from an iPhone; the transport method is not disclosed.

Version: **0.4.0 released 2026-01-28** *(blog)*; I did not find a later "0.5".

### 3.5 Engines and hardware

- macOS: Apple Silicon only, macOS 14+; Intel Macs unsupported. Windows: x64 (AVX2) and ARM64 (Snapdragon X). Linux: x64 and ARM64, distributed as an AppImage, Ubuntu 20.04+.
- Engines: **llama.cpp (GGUF)** on all platforms and **MLX** on Apple Silicon. Runtimes are separately updated packages ("LM Runtimes", shortcut Ctrl/Cmd+Shift+R, `lms runtime …`).
- ⚠️ **ROCm and gfx1201:** I cannot confirm this. The "LM Runtimes" documentation page returned 404, and the repository with its source is a template with placeholder text. The list of backends (CUDA, Vulkan, ROCm, Metal, CPU) is "the usual set", but ROCm specifically for the R9700 is *(unverified)*. If you consider LM Studio on the rig, test on a single card first.
- A blog post from 2026-09-18 promotes "Splash Engine", **an open engine from the company Inco AI** (74 tok/s for short prompts and 54 at 32K on Qwen3.8-27B, 170 tok/s at 4 parallel requests, on a 48 GB M5 Pro) *(company's own claim)*; how it is plugged into LM Studio is unclear *(unverified)*.

### 3.6 Architecture (as much as is visible)

The closed core makes reading the code impossible, so this is an inference from the open elements: an Electron shell with a "core" in Node that talks to separate engine processes through the `lmstudio-js` SDK protocol (WebSocket-based, the same as in the SDK and `lms`). The engines are a runtime derived from llama.cpp and the Python `mlx-engine`. The app, `llmster` and Bionic have separate state directories, but "share the model and runtime store". The model catalog is open JSON, the Hub is a closed SaaS.

### 3.7 Terms, offline, Bionic

- **Terms (Element Labs, 2026-08-23):** software for "personal and/or internal company" use; a ban on use as a service (*service bureau*, ASP, SaaS), a ban on reverse engineering and redistribution; liability cap of **50 USD**. **Since 2025-07-08 it is free for work** ("no form and no contact"); earlier, business use required a form/license.
- **Offline:** "LM Studio can run entirely on your device… no messages, chat histories or documents are sent anywhere" *(company's own claim: lmstudio.ai/app-privacy)*. It connects to the network for: updates (app version, OS, IP), anonymized model search queries and downloads, optional cloud features, mail to support. After models are downloaded it works offline.
- **Bionic (2026-07-16):** "an AI agent for open models", "a new, separate app". It runs locally, through LM Link or in "LM Studio Secure Cloud" (requires an account for billing; zero data retention and no training on it *(company's own claim)*); it creates documents, slides, PDFs and software; skills (*skills*, 2026-08-17), Auto Review (2026-08-27). Per the home page, a Windows x64 version is available for download. The classic app, `llmster` and `lms` still exist; `lms` recognizes Bionic (it prefers a running LM Studio app or llmster).
- **Business model** *(company's own claim)*: organizations in the Hub (public free, team self-service **Teams**, **Enterprise** with SSO and model/MCP gating, no price list); Bionic + Secure Cloud (hosted open models with billing); acquisitions of teams (Locally AI).

### 3.8 Strengths and weaknesses

| + | − |
|---|---|
| the best GUI and the easiest model discovery | closed core: you cannot patch the runtime, point to an engine commit, or audit |
| MLX and GGUF side by side | the terms forbid reverse engineering and redistribution |
| `llmster` + `lms` = scriptable on a machine without a screen | fewer sampling and scheduling knobs than in `llama-server` |
| OpenAI and Anthropic endpoints | ROCm/gfx1201 unverified |
| model files lie in an ordinary directory (`~/.lmstudio/models`), low exit cost | the company may introduce paid tiers (until 2025-07 a license was needed for work) |

### 3.9 When to choose LM Studio

When you want **the same API on a Mac and on Ubuntu** and closed code does not bother you; when a non-technical person is to use models locally; when you want MLX and GGUF in one GUI. Do not choose it when you need a pinned, auditable engine or when the hardware is AMD cards, about which the documentation is silent.

> **Check it yourself #3: what is open in LM Studio.**
> `gh api orgs/lmstudio-ai/repos --paginate --jq '.[] | [.name,.license.spdx_id,.stargazers_count] | @tsv'` *(not run by me; the jq filter is mine, the command `gh api orgs/lmstudio-ai` was used in the research)*. You will find `lms`, `mlx-engine`, the SDKs and the tracker, but **no repository of the app and no llama.cpp fork**. For comparison, open `lmstudio.ai/terms` and find the clause banning reverse engineering.

---

## 4. llmman: models as OCI images

**In one sentence:** a single-file Rust program that treats models like OCI artifacts and can run `llmman launch claude --model qwen3.8`: it starts a local `serve` daemon, launches an **unmodified** upstream engine, exposes the Ollama, OpenAI, Anthropic and Gemini APIs, and then starts a coding agent pointed at that server.

### 4.1 Who is behind it, and what is real versus aspirational

The repository `llmmanorg/llmman`, Apache-2.0, created **2026-03-22**; first commit in the history **2026-05-02**; 567 commits; release **v0.1.567 of 2026-10-19** (CI sets the patch number to the number of commits: "every commit to main ships as a release"). 563 stars, 67 forks. The `llmmanorg` organization was created on 2026-08-14, with no description or links; the blog starts on 2026-08-31 with the post "Introducing llmman".

Main author: **Eric Curtin** (`ericcurtin`, 402 commits out of ~567; next: ricky-chaoju 57, HassanBahati 40, doringeman 14, maxgio92 12). The address on llmman's commits is `@docker.com`; earlier commits to RamaLama have an `@redhat.com` address (the last one 2025-08-11), and the first commit to `docker/model-runner` dates from 2025-08-18. So Red Hat → Docker, with the exact employment dates *(unverified)*. Curtin co-created RamaLama and is one of the main maintainers of Docker Model Runner.

**Is it a Docker product?** For: the author's employer, the image `docker.io/ai/llmman` (the `ai/` namespace is Docker's), Docker media types, a co-author from Docker (doringeman), Docker Agent and Sandboxes as first-class targets. Against: a separate GitHub organization without Docker branding, no Docker notices, the site does not say who is behind it. **Conclusion: a personal project of a Docker engineer using tools from the Docker ecosystem; no official sponsorship was found** *(unverified)*. There is no company, revenue or funding. *Bus factor* about 1 (402 of ~567 commits).

What is **real** (code read): ~98.9K lines of Rust; `src/cmd/serve/` 30.7K (the Ollama, OpenAI, Anthropic, Responses and Gemini API overlays, the scheduler `sched.rs`, `aggregation.rs`, `hybrid.rs`), `src/mediagen/` 10.3K (its own diffusion in ggml), `src/cmd/launch/` 9.2K (agent integrations and sandboxes), `src/storage/` 2.8K (OCI store + GC), `src/modelpack.rs`; a shim in Go (7.5K lines, `go-shim/`) compiled through CGO to handle registries and OCI transfer.

What is **aspirational or unproven:** the README and documents claim that changes are meant to "outperform all comparable solutions" (`AGENTS.md`), but there is **no data** for it *(project's own claim)*; no measurements of its own; version 0.1.x; a dominant author. The code is written with the help of coding agents (there is an `AGENTS.md`); 98K lines in five months at ~4 commits a day is consistent with that, but this is my inference *(unverified)*. I did not search the code for telemetry.

### 4.2 What it is for

For developers who want any agent (Claude Code, Codex, OpenCode, Cline, Aider, Gemini CLI, goose, Docker Agent and a dozen others) on any model, local or hosted, with a model supply chain that looks like a container supply chain: registry mirrors, cosign signatures, transfer to air-gapped environments. **It does not provide an engine**: "llmman does not ship an inference engine" (`docs/backends.md`).

### 4.3 Features

Commands: `pull|push|transfer|run|serve|launch|list|ps|stop|show|rm|search|build|verify|config|usage|log`. `serve` listens on `127.0.0.1:17434` and speaks **Ollama** (`/api/*`; the real `ollama` CLI works once `OLLAMA_HOST` is set), **OpenAI** (chat, completions, embeddings, models, responses, transcription, images/video/speech for diffusion) and **Anthropic** (`/v1/messages`), plus Gemini and `/v1/systemone`. Tools, vision, structured output, embeddings (GGUF), a UI at `/`, Prometheus metrics at `/metrics`.

Extras: **aggregation** (daemons join into a pool; a request goes to the node with the model loaded or the most free space), **hybrid** pairs (`--overflow-provider`: requests that are too large go to a hosted model), **sandboxes** (`--sandbox sbx|seatbelt|docker|podman|apple-container|microsandbox|openshell`), providers from models.dev.

### 4.4 Engines and hardware

From `docs/backends.md`:

| Format | Engine |
|---|---|
| GGUF | upstream `llama-server`: the image `ghcr.io/ggml-org/llama.cpp:server-{cuda,cuda13,rocm,vulkan}-<release>` on Linux via docker/podman; or a downloaded ready-made release asset (`--runtime bin`); or from `PATH` (`--runtime path`) |
| safetensors | `vllm` (on AMD x86_64 the image `rocm/vllm:latest`), `sglang`, `mlx_lm.server` on macOS (installs its own `uv` + mlx-lm) |
| optional | `ds4-server` |
| diffusion | in-process on ggml; Diffusers via vLLM-Omni |

Pinned versions: `LLAMA_CPP_RELEASE` = b11429, `MLX_LM_RELEASE` = 0.31.3. GPU probing order: CUDA, ROCm, OpenCL (Adreno), Vulkan, Metal; `LLMMAN_LLM_LIBRARY` overrides it. Llama.cpp does not ship a ready-made CUDA build for Linux, so on NVIDIA+Linux the `auto` mode prefers a container.

**AMD:** there is a ROCm path (the `server-rocm` image), but the notes **do not mention gfx1201** and it was not checked on an R9700 *(unverified)*.

### 4.5 Architecture

**OCI model images.** The local store is an *OCI Image Layout* (`<root>/oci-layout`, `manifests/<ref path>/<tag>` as a small JSON descriptor per reference "mirroring the layout of Ollama's manifests", `blobs/sha256/<hex>`): `src/storage/oci.rs`. Manifest media types: **CNCF ModelPack** (`application/vnd.cncf.model.config.v1+json`, files keyed by `org.cncf.model.filepath`) and Docker Model Runner's `application/vnd.docker.ai.gguf.v3` for GGUF layers (`src/modelpack.rs`, `HF_GGUF_MEDIA_TYPE`). `modelpack::resolve_model` returns `ModelPath::{Gguf(+mmproj), SafeTensors, Diffusion, Omni}` and picks the backend on that basis. Registry operations go through a shim in Go (docker/podman credential helpers, mirrors, cosign verification). `llmman transfer hf.co/... docker.io/...` streams without landing in the local store.

**Request flow.** HTTP (axum-style handling, `src/cmd/serve/*`) → `ensure_model` (`backend.rs`) starts a per-model backend process on a random port (`llama-server` flags: `--model --port --host --ctx-size --flash-attn --cache-type-k/v --parallel --threads --split-mode --mmproj --embeddings`) → proxying and translation. The idle reaper (`sched.rs`) mirrors Ollama's keep-alive (5 minutes by default, `LLMMAN_KEEP_ALIVE`); the environment variable names deliberately mirror Ollama (`LLMMAN_MAX_LOADED_MODELS`, `LLMMAN_NUM_PARALLEL`, `LLMMAN_SCHED_SPREAD`, `LLMMAN_KV_CACHE_TYPE`, `LLMMAN_FLASH_ATTENTION`). An API key is required when listening outside loopback; TLS is optional.

### 4.6 Strengths and weaknesses

+ Clean engines (no fork lag): the pin b11429 against b11669 in Ollama means both are within days of upstream; one command to start an agent; a signed OCI supply chain; aggregation between a Mac and a rig.
− Very young (first commit in May 2026), v0.1.x, one dominant author, "outperforms the competition" claims without data. The README describes Ollama as "Bundled llama.cpp/ggml fork plus Ollama's own engine", **which has been out of date since 2026-05-29** (section 2.3). The choice of media types ties the project to Docker's `ai/` namespace.

### 4.7 When to choose llmman

When you are interested in **distributing models through a container registry** (Harbor, Artifactory, ghcr), signatures and transfer to air-gapped environments, and when you accept the risk of a 0.1.x version. For the reference rig it is rather a **source of ideas** (section 8) than a replacement for llama-swap, although the author of the notes observes that it could replace llama-swap if you want models as OCI and the Anthropic/Ollama API.

---

## 5. The remaining wrappers

In brief: identity, architecture in a few sentences, a "Who is behind it" paragraph, a note on AMD (only what the notes say) and **"When to choose"**. For Jan, LocalAI, Lemonade, Docker Model Runner, RamaLama and GPT4All I rely on the README, file trees and selected files from the GitHub API, not on a full checkout.

### 5.1 Jan

**What it is:** an open-source ChatGPT-style desktop app (Tauri: Rust + React/TS), running GGUF through an embedded llama.cpp worker process, MLX on Macs, with the ability to connect to cloud providers. `janhq/jan`, created 2023-08-17, **45,017 stars**, **v0.8.6 (2026-10-09)**.

**License.** `LICENSE` is Apache-2.0 plus one added sentence: "Attribution is requested in user-facing documentation and materials, where appropriate." Because of this modification GitHub shows NOASSERTION; in practice it is Apache-2.0 with a non-binding request for attribution.

**Architecture.** `src-tauri/` (Rust + plugins `llamacpp`, `mlx`, `hardware`, `rag`, `websearch`, `agent-tools`), `extensions/` (TS), `mlx-server/` (a Swift package: an OpenAI- and Anthropic-shaped server on MLX-Swift, requires Xcode 26.2), `web-app/`. Since **v0.8.5 (2026-10-08)** llama.cpp is **statically linked** into `jan-llama-worker` (`engine/mod.rs`: "no llama-server child, no downloaded binary"; access to `server_routes` through a C++ shim), but still in a separate supervised process, because `GGML_ASSERT` calls `abort()` — the same reason as in Ollama. The version is pinned by `JAN_LLAMA_CPP_TAG`. The GUI exposes `--n-cpu-moe`, tensor split, `fit` and `models_max` (`extensions/llamacpp-extension/settings.json`).

**Features.** An OpenAI-compatible server on `localhost:1337`, MCP, cloud connectors (OpenAI, Anthropic, Mistral, Groq…), Menlo's own fine-tuned models on Hugging Face. **Offline:** yes; analytics opt-in (PostHog EU) *(project's own claim)*; the update plugin is present.

**AMD.** A **ROCm/HIP backend on Linux since v0.8.2 (2026-06-01)** (changelog); gfx1201 not mentioned.

**Who is behind it.** Menlo Research, today presenting itself as a maker of **humanoid robots** (Asimov 1). I **did not find** funding, founders or investors — I do not enter any numbers. Jan has no visible revenue *(project's own claim)*. Risk: the parent company's communication is about robots. See [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

**When to choose:** when you want an **open** counterpart of LM Studio with a GUI and local / cloud model switching. A pattern to copy: a supervised worker process with a router and presets.

### 5.2 GPT4All

**What it is:** a desktop app from Nomic AI (Qt/C++/QML) with local chat and *LocalDocs* (RAG on `usearch`). MIT, **77,350 stars**, created 2023-03-27; the engine is a **fork** of llama.cpp (`llama.cpp-mainline`), GPU through Vulkan (README: Q4_0/Q4_1 on NVIDIA and AMD).

**Verdict:** the last release **v3.10.0 of 2025-02-25**, the last commit **2025-05-27** (~17 months of silence), 775 open issues, a README without a word about maintenance mode. **De facto unmaintained; I did not find an official statement.** The engine fork stopped in mid-2025, so new model architectures are out.

**Who is behind it.** Nomic (CEO Andriy Mulyar; a 2023 Series A of 17 million USD led by Coatue *(company's own claim)*) today does "AI for AEC" (architecture, engineering, construction); GPT4All does not appear on nomic.ai. The product was a marketing funnel, and after the pivot the project froze. MIT allows a fork, but the real cost is a rotting engine fork.

**When to choose:** **not for new uses.**

### 5.3 LocalAI

**What it is:** a server in Go (API compatible with OpenAI, Anthropic, Ollama, ElevenLabs): **a small core + backends on demand**, each as an OCI image with a gRPC contract; text, vision, speech, image, video, distributed mode. `mudler/LocalAI`, MIT, **49,695 stars**, created 2023-03-18, **v4.11.0 (2026-10-02)**.

**Architecture** (`backend/backend.proto`, `pkg/model/process.go`): `core/http` → ModelLoader → a **per-model backend process** talking over gRPC (the `Backend` service, about 55 calls: `Predict`, `Embedding`, `GenerateImage`, `TTS`, `Rerank`…). Backends (60+) in `backend/{cpp,go,python,rust}`: llama-cpp, vllm, sglang, mlx, whisper, diffusers… **Published as OCI images from the Backend Gallery**, signed with cosign since v4.3.0; since v3.2.0 (2025-07) all outside the main binary. GPU detection selects the image (CUDA 12/13, ROCm, SYCL, Metal, Vulkan, Jetson). Distributed mode with VRAM-aware routing (v4.1.0, 2026-04), OIDC/keys/limits, MCP, Realtime API.

**AMD:** ROCm is on the hardware list; **the availability of a per-backend image for gfx1201 is unchecked** *(unverified)*. **Offline:** after the backend and model are downloaded; both are downloaded on demand.

**Strengths/weaknesses:** + the widest modality coverage, engine isolation, vLLM/SGLang per model; − thin polish per backend, a lot of YAML, one dominant maintainer, fast drift.

**Who is behind it.** Ettore Di Giacinto (`mudler`, ex-SUSE/Rancher); 3,507 commits are his, the rest mostly bots. The README lists sponsors covering CI (Spectro Cloud, solstone.app); no company or funding was disclosed. See [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md).

**When to choose:** when you need **one API for many modalities and many engines** (llama.cpp-ROCm next to vLLM-ROCm) and accept a complex configuration. The "backend as an OCI image + gRPC" template is the cleanest in this group.

### 5.4 Lemonade (AMD): the most important one in this group for you

**What it is:** a server/runtime in C++ with the OpenAI, Anthropic and Ollama APIs, which chooses among backends: llama.cpp (Vulkan/ROCm/CUDA/Metal/CPU), FastFlowLM and Ryzen AI OGA (**XDNA2 NPU**), vLLM-ROCm, whisper.cpp, stable-diffusion.cpp, Kokoro. Simply put: **AMD's answer to Ollama**. `lemonade-sdk/lemonade`, **Apache-2.0**, **5,936 stars**, created 2025-05-15, weekly releases (`v2026.42.1` of 2026-10-14). Most commits: `jeremyfowers` 569, `superm1` (Mario Limonciello) 150, `fl0rianr` 121, `ramkrishna2910` 111, `danielholanda` 81.

**The connection to AMD (verified).** README: "built by the community for every PC, with optimizations by AMD engineers to get the most from Ryzen AI, Radeon, and Strix Halo PCs". Jeremy Fowers, Daniel Holanda and Ramakrishnan Sivakumar list the company **AMD** on GitHub; Limonciello commits from `@amd.com`; 14 of the last 100 commits have `amd.com` addresses (59 are noreply, so the real share is higher). **FastFlowLM** (the NPU runtime) lives in `github.com/ROCm/FastFlowLM`, and its kernels are "Copyright (c) 2026 Advanced Micro Devices, Inc.", "not open source", freely redistributable unchanged. There is no sentence "Lemonade is an AMD project" (a separate organization `lemonade-sdk`), but the core is AMD employees; funding = AMD salaries *(terms unverified)*.

**Backend table** (`docs/dev/backends-reference.md`, generated from C++ descriptors; abridged):

| Backend | Targets | Notes |
|---|---|---|
| `llamacpp` | cpu, cuda (sm_75…sm_121), metal, **rocm** (gfx103X, gfx110X, gfx1150–1152, **gfx120X**, gfx908/90a/942/950), vulkan, system | `system` = your own `llama-server` |
| `llamacpp-hrx` | experimental: gfx1100/gfx1151 | |
| `flm` (FastFlowLM) | XDNA2 NPU, Windows and Linux | closed kernels |
| `ryzenai-llm` (OGA) | NPU, Windows only | |
| `vllm` rocm | experimental: gfx110X/1150/1151/**120X** | |
| `ds4` (guest) | gfx1151 | see [`07-APPLE-MLX-OMLX-AND-DS4.md`](07-APPLE-MLX-OMLX-AND-DS4.md) |
| `whispercpp`, `sd-cpp`, `kokoro`, `onnxruntime`… | various | |

**gfx1201 versus this table.** The R9700 is gfx1201, the table speaks of the **`gfx120X`** family; the notes infer that gfx1201 fits in it, i.e. llama.cpp-ROCm (Linux and Windows), vLLM-ROCm (experimental), sd.cpp and whisper. This is an inference from the family name, not a direct entry, and not checked on hardware *(unverified)*.

**How it differs from "llama.cpp-ROCm built yourself":** (1) it **distributes ready-made builds** of llama.cpp with ROCm 7 (`lemonade-sdk/llamacpp-rocm`, 786 stars; "Stable" and "Nightly" channels; also `vllm-rocm`, `whisper.cpp-rocm`, `ds4-rocm`); (2) it detects the device family and downloads the right backend (`lemonade backends`); (3) it adds NPU paths that llama.cpp does not have; (4) a model manager (`lemonade pull`, aliases with active-standby failover, OTLP telemetry); (5) an *embeddable* binary for apps. The documentation recommends Vulkan "for most GPU users", and ROCm "may outperform Vulkan". On a multi-card rig it is still llama.cpp underneath (`llamacpp.backend=system` lets you use your own `llama-server`).

**Weaknesses:** the NPU mainly on Windows; some backends experimental; AMD's priorities (Strix Halo first); a multi-card split is whatever llama.cpp/vLLM gives. **Offline:** locally yes; backends and models are downloaded on first use; FLM checks the version at startup unless `FLM_DISABLE_UPDATE_CHECK=1`; the site declares "zero telemetry" *(project's own claim)*.

**When to choose:** when the hardware is **Ryzen AI / Strix Halo / Radeon** and you want ready-made ROCm builds or an NPU path. On the reference rig it is above all a **cheat sheet**: the `gfx120X` support table and the ready-made builds as a reference point for your own build.

> **Check it yourself #4: what Lemonade says about gfx120X.**
> `gh api repos/lemonade-sdk/lemonade/contents/docs/dev/backends-reference.md --jq .content | base64 -d | grep -n -i "gfx120"` *(I did not run this command; I read the file through the API)*. Look for the `llamacpp` (rocm) and `vllm` (rocm) rows. The connection to AMD: `gh api users/jeremyfowers --jq .company`.

### 5.5 Docker Model Runner (DMR)

**What it is:** a "model as an OCI artifact" runner: `docker model pull|run|ls|ps …`, behind it a Go daemon managing llama.cpp / vLLM / SGLang / MLX / Diffusers engines; in Docker Desktop, Docker Engine (Linux) and as a standalone `dmr`. `docker/model-runner`, Apache-2.0, **658 stars**, created 2025-03-28, **v1.2.8 (2026-08-12)**. Most commits: `doringeman` 696, `ilopezluna` 387, **`ericcurtin` 318**.

**Engines pinned in `.versions`:** `LLAMA_SERVER_VERSION=b9879`, vLLM 0.19.1, SGLang 0.5.6. Llama.cpp is a submodule built by Docker; images: `cpu` (upstream `server-vulkan`), `rocm` (`server-rocm`), CUDA. **Architecture:** `pkg/inference/scheduling/` — a loader with **8 runner slots** and a **5-minute idle limit**, the runner key = (backend, model hash, draft hash, mode); `pkg/distribution` (126 files) — a client and store of OCI models (Docker Hub `ai/`, any registry, Hugging Face); API overlays `pkg/anthropic`, `pkg/ollama`, `pkg/responses`; OpenAI on `:12434` by default. On macOS/Windows the engines run as isolated host processes, on Linux in containers *(company's own claim)*.

**Money:** bundled with Docker Desktop/Engine; it is a feature that keeps developers on Docker Hub, not a product line *(unverified)*. **AMD:** ROCm on Linux only, gfx1201 not mentioned; multi-GPU tuning limited compared with `llama-server` itself.

**When to choose:** when you **already live in Docker** and want models as artifacts in the same registries as images. Note the pinned `b9879` — an older engine than b11669 in Ollama *(my calculation from the build numbers)*.

### 5.6 RamaLama

**What it is:** a CLI in Python (`ramalama run|serve|pull|push|bench`) that detects the GPU, pulls the **matching container image** with the engine inside and runs the model in a rootless podman/docker container **with no network by default**. The `containers` org (the Podman family), maintainers from Red Hat. MIT, **3,086 stars**, created 2024-07-24, **v0.25.0 (2026-09-25)**.

**Image selection by environment variable** (README): Vulkan/CPU → `quay.io/ramalama/ramalama`; **`HIP_VISIBLE_DEVICES` → `quay.io/ramalama/rocm`**; `CUDA_VISIBLE_DEVICES` → `…/cuda`; Asahi, Intel, CANN, MUSA — their own images. The tag = the minor version of RamaLama, override with `--image`. Model sources: `ollama://`, `huggingface://`, ModelScope, `oci://`. On macOS llama.cpp or MLX on the host.

**Who is behind it.** Red Hat (IBM) pays the maintainers (Dan Walsh, Mike Bonnet, Oliver Walsh) *(RHEL AI / Podman AI Lab strategy: unverified)*; no revenue of its own. Dan Walsh (`rhatdan`, 1,462 commits) has the status "Retired" on GitHub. Eric Curtin co-created the project (971 commits) and moved to Docker (section 4.1).

**AMD:** `quay.io/ramalama/rocm` is a ready-made clean ROCm userland; gfx1201 not mentioned. **Vs Ollama:** containers + upstream engines + rootless, without its own model library and cloud.

**When to choose:** when **isolation** matters more than convenience (an agent in a `--network none` sandbox), on Fedora/RHEL, and when you want per-GPU images without building.

---

## 6. Frontends that are not runtimes

They do not compute tokens: they are **clients** of everything I described above.

### 6.1 Open WebUI

A web chat/RAG (FastAPI + Svelte) talking to Ollama and OpenAI-compatible backends. **156,189 stars**, v0.12.3 (2026-10-16), main author `tjbck` (13,450 commits).

**License (a practical note).** MIT, then BSD-3-Clause; **since v0.6.6 (2025-04-19)** its own "Open WebUI License": BSD-3 plus clause 4 — you may not change, remove or obscure the name "Open WebUI", **unless** (i) you have at most 50 end users in a rolling 30-day window, (ii) you have written permission or (iii) an enterprise license. Contributors sign a CLA; the code from before the change stays under BSD/MIT (`LICENSE_HISTORY`). GitHub shows NOASSERTION; the license is **not approved by the OSI**. The rationale: to stop rebranding and commercial repackaging without contribution *(project's own claim)*. **Money:** enterprise/white-label licenses, support (prices not public) *(project's own claim)*; I did not verify funding.

**When to choose:** a browser chat for a team in front of your OpenAI-compatible server (e.g. llama-swap). For your own team with the original branding — no problem; white-label requires an agreement.

### 6.2 AnythingLLM

An all-in-one RAG/agents app (desktop + Docker, Node/React) with a vector database, MCP and an agent builder; it uses an external runtime or an optional built-in engine "powered by Lemonade and llama.cpp" (README). Mintplex Labs, MIT, **67,323 stars**, v1.18.0 (2026-10-13), author `timothycarambat`.

**Money** *(company's own claim: anythingllm.com/pricing)*: desktop free; cloud **50 USD/month (Basic)** and **99 USD/month (Pro, 72 h support SLA)**; Enterprise on request. I did not verify funding. It is a *client* of Ollama, LM Studio, LocalAI — not a competitor.

**When to choose:** RAG over documents and agents in one app, when you have the engine elsewhere.

---

## 7. What breaks when the sponsor changes their mind

A wrapper is a product of somebody's company or somebody's free time. This table answers the question: *what exactly stops working or stops being developed if whoever pays (or writes) changes plans — and how much does escape cost?* The description of funding models and people is in [`10-MONEY-AND-PEOPLE.md`](10-MONEY-AND-PEOPLE.md); here only the technical consequences.

| Product | Who steers | Engine | What breaks | What stays | Exit cost |
|---|---|---|---|---|---|
| **Ollama** | Ollama, Inc. (VC; 88 million USD per the company) | upstream `llama-server` + its own MLX | the model library and registry, templates and parsers, the cloud; cloud prices have already been changed once (from GPU time to tokens, 2026-08-31). If the registry or accounts stop working, new model downloads from the library stop | downloaded models keep working; the MIT code can be forked | **medium**: models are blobs (you must export to GGUF), and the moat is the library, not the code |
| **LM Studio** | Element Labs (closed-source; funding unknown) | closed-source llama.cpp + MLX runtimes | "free for work" may end (a license used to be required), runtimes will freeze as binaries, a Bionic/cloud direction | model files in an ordinary directory | **low** for models, but you cannot fork the GUI and the daemon |
| **llmman** | one person (a Docker employee) | upstream unchanged | project abandonment | the engines are upstream, models are standard OCI/HF | **very low** |
| **Jan** | Menlo Research (communication about robotics) | embedded llama.cpp + its own MLX | maintainers may shift; the updater and telemetry are under Menlo's control | Apache-2.0 code, ordinary GGUF | **low to medium** (a heavy fork: Rust+TS+Swift) |
| **GPT4All** | Nomic (pivot to AEC) | outdated llama.cpp fork | **already happened**: frozen since 2025-05 | MIT license, but the engine fork is rotting | not applicable: abandoned |
| **LocalAI** | mudler + sponsors | 60+ engines in OCI images | the maintainer's bandwidth | MIT, modularity | low |
| **Lemonade** | AMD engineers + community | llama.cpp (+ NPU FLM/OGA) | the closed NPU kernels (FLM binaries) and the ROCm images built by AMD would stop improving | generic llama.cpp backends keep working; the Apache-2.0 C++ core can be forked | low for GPU paths |
| **Docker Model Runner** | Docker, Inc. | llama.cpp / vLLM / SGLang / MLX / Diffusers | priorities (AMD and Metal coverage) | Apache-2.0, OCI artifacts compatible with ModelPack | low |
| **RamaLama** | Red Hat (maintainers) | llama.cpp / vLLM in per-GPU images | the images on quay.io would stop being refreshed | MIT; images can be built yourself from `container-images/` | low |
| **Open WebUI** | Open WebUI Inc. | none | a tightening of the license (**already done in 2025**) | versions up to v0.6.5 on BSD | an old fork can be pinned |
| **AnythingLLM** | Mintplex Labs | none / optional | cloud prices | MIT | low |

Two cases worth remembering. **GPT4All**: the company found a better market, and the open project froze. **Open WebUI**: the license changed twice (MIT → BSD-3 → BSD-3 + a branding clause); "open" does not mean "immutable".

---

## 8. What this means for the reference setup

### 8.1 Why you run llama.cpp + llama-swap directly

The reference rig is 4× R9700 (gfx1201, ROCm), a 284B MoE model (DeepSeek-V4-Flash, UD-IQ3_XXS) at ~50 tok/s, and that result is decided by settings that wrappers often hide. The reasons why this makes sense, in order of importance:

1. **Knobs.** The settings from the guide [`../speeding-up-generation/README.md`](../speeding-up-generation/README.md) (tensor split, speculative decoding) and flags such as `--n-cpu-moe` are `llama-server` flags. In Ollama only those are available that Ollama lets through via its own `OLLAMA_*` variables and the `options` field; in LM Studio — those that the GUI shows. For a model of this size, the difference between the default and a tuned placement on four cards is the difference between "works" and "works fast" *(my assessment, no measurement)*.
2. **A pinned build.** Production runs on the build `0ce8cd1`, which you choose. Ollama builds a pinned upstream version **with its own layer of patches** (b11669 in the clone I checked), LM Studio ships closed runtimes that it updates on its own rhythm.
3. **GPU placement.** llama-swap has **groups and a matrix** (with eviction costs): one entry "70B dense on four cards" (`HIP_VISIBLE_DEVICES=0,1,2,3`), a second "two 30B models on cards 0–1 and 2–3", a third "always-on embedding/rerank on a separate slice". Ollama has the heuristic "one card first, then a split" and `OLLAMA_SCHED_SPREAD`, but **has no equivalent of the matrix** *(my inference from reading `sched.go`, not from a document)*.
4. **Plain GGUF files.** Models lie as files that all your tools see (llama-bench, quantize, imatrix); in Ollama they are `sha256-…` blobs.
5. **Minimal dependencies.** llama-swap is a single static Go file, but to be fair: it is also a project with a *bus factor* of 1 (Benson Wong, about 82% of commits, MIT license), so you have the "one person" risk just as with llmman. The difference: it is small and easy to fork or replace.

**A note on newer llama.cpp:** `llama-server` itself now has a **router mode** (`--models-dir`, `--models-preset`, `--models-max`, 4 models at once by default): it starts a child `llama-server` process per model, evicts the least recently used idle model (LRU) and supports `--sleep-idle-seconds`. This is a "built-in mini llama-swap" without groups and a matrix. In light of this, the value of a "full" wrapper for model lifecycle is shrinking; the space that llama.cpp does not cover is the model registry, the GUI and API translation. Router details: [`04-LLAMA-CPP-AND-THE-GGML-FAMILY.md`](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md).

### 8.2 What you would gain and what you would lose

**If you switched to Ollama:**

| You gain | You lose |
|---|---|
| a model library with ready-made templates and tool parsers | the full set of `llama-server` flags and your own build |
| `ollama launch` for agents, an "Ollama provider" in every tool | the llama-swap GPU matrix (section 8.1, point 3) |
| on Macs: **its own MLX runner** and engine choice per tag (manifest lists) | plain `.gguf` files |
| lifecycle management without configuration | predictable defaults (a limit of 1 parallel request, 3 models/GPU, VRAM-dependent context, 5 min keep-alive) |
| (R9700 listed in `docs/gpu.mdx`, ROCm v7) | certainty that it will work for your 284B model: I did not check that |

**If you switched to LM Studio (`llmster` + `lms` on Ubuntu, the GUI on the Mac):**

| You gain | You lose |
|---|---|
| the same API (OpenAI + Anthropic) and the same program on the Mac and on Ubuntu | auditability and the freedom to choose the engine build |
| JIT + TTL, `lms runtime` to pin the engine version per machine | ROCm/gfx1201: no confirmation (the runtimes page returned 404) |
| stateful `/v1/chat` with `response_id` — convenient for agents | some of the knobs; the terms forbid reverse engineering |

### 8.3 What to borrow without switching

1. **Model distribution as OCI** (llmman, Docker Model Runner, RamaLama, Ollama): the CNCF ModelPack media types or `application/vnd.docker.ai.gguf.v3`, a local *OCI Image Layout*. Gain: Harbor/Artifactory/ghcr as a model store in your infrastructure, cosign signatures, transfer to air-gapped environments (`llmman transfer`).
2. **A manifest list with `runner` and `format` fields** (Ollama): one tag, two builds: GGUF for the AMD rig and MLX for the Mac.
3. **Model lifecycle:** keep-alive + reference counters + "one load at a time" (Ollama) is a minimal sensible schedule for a multi-model server; JIT + TTL (LM Studio); the idle reaper (llmman).
4. **A placement heuristic:** first try to fit the model on one card (`--split-mode none --main-gpu N`), only then split. Llama-swap can express this per model.
5. **The compat pattern:** translate GGUF at load time, not at download time (`llama/compat/` in Ollama), if you ever need to consume GGUF files from different sources together.
6. **Lemonade's backend matrix** (`docs/dev/backends-reference.md`) as a cross-check of your own gfx1201 build (the `gfx120X` rows), and its ready-made llama.cpp-ROCm builds (`lemonade-sdk/llamacpp-rocm`) as a reference point to compare with your `0ce8cd1`. Aliases with active-standby failover as an idea for the llama-swap configuration.
7. **A backend as an OCI image + a gRPC contract** (LocalAI): the cleanest template for "many engines, one API" (e.g. llama.cpp-ROCm and vLLM-ROCm chosen per model).
8. **Agent isolation:** RamaLama with `--network none` in a rootless container as a security baseline for agent sandboxes; llmman with the `--sandbox` flag.
9. **The UX "run an agent on a local model"** (`ollama launch`, `llmman launch`, `lemonade launch claude`): for your own agent applications a script that sets the environment variables and the endpoint address is enough.
10. **A stateful conversation API** (`response_id` in LM Studio): the server remembers state, the client sends back an identifier. It fits agents with long sessions.

### 8.4 Which wrappers can use gfx1201 cards

Only what the notes say. ⚠️ **I did not check any of these confirmations on hardware.**

| Product | What the notes say about AMD / R9700 |
|---|---|
| **Ollama** | `docs/gpu.mdx` lists the **Radeon AI PRO R9700 / R9600D** in the ROCm section (ROCm v7 required); Vulkan enabled by default. The R9700 is in the documentation, but gfx1201 is not named directly; **not tested here** |
| **LM Studio** | **unverified** (the runtimes documentation is unavailable) |
| **llmman** | a ROCm path exists (the `server-rocm` image, `rocm/vllm:latest`), gfx1201 not mentioned |
| **Jan** | a ROCm/HIP backend on Linux since v0.8.2, gfx1201 not mentioned |
| **GPT4All** | Vulkan on AMD in the README; the project is dormant |
| **LocalAI** | ROCm on the hardware list; per-backend image availability unchecked |
| **Lemonade** | the backend table lists the **`gfx120X`** family; llama.cpp-ROCm (Linux and Windows), vLLM-ROCm experimental, sd.cpp, whisper. The closest direct confirmation for the R9700 in this group, though as a family, not as gfx1201 |
| **Docker Model Runner** | ROCm on Linux (the `rocm` image); gfx1201 not mentioned; multi-GPU tuning limited |
| **RamaLama** | the `quay.io/ramalama/rocm` image selected through `HIP_VISIBLE_DEVICES`; gfx1201 not mentioned |

I did not check whether any of these wrappers will run your DeepSeek-V4-Flash model in UD-IQ3_XXS, nor at what speed.

Overall comparison and choice: [`09-COMPARISON-AND-CHOICE.md`](09-COMPARISON-AND-CHOICE.md).

---

## 9. What I could not establish

1. **Ollama:** whether the missing license notices (issue #3185) are in the artifacts today; the chronology of the switch to `llama-server` (tag v0.30.0 of 13–14 May vs PR #16031 of 29 May vs the blog of 5 June); whether 88 million USD is one round or a sum (Wikipedia: 65 million); earlier rounds; the default context from before 2026; independent performance measurements; whether the context threshold for ≥ 48 GiB is computed from one card or from the sum; whether Ollama exposes the split modes known from the guide on speeding up.
2. **LM Studio:** funding and the founders' titles; the list of backends and ROCm/gfx1201; the relationship with Inco AI's "Splash Engine"; Bionic and Teams prices; the version after 0.4.0.
3. **llmman:** whether Docker officially sponsors it; telemetry in the code; benchmarks.
4. **Jan:** Menlo's funding; the license history (AGPL earlier? — unverified); the updater's behavior.
5. **LocalAI:** mudler's employer; ROCm for gfx1201 per backend. **Lemonade:** formal AMD ownership; NPU maturity on Linux. **Docker Model Runner:** details of macOS and multi-GPU AMD. **RamaLama:** the staffing after Dan Walsh's departure, the date of Eric Curtin's departure from Red Hat. **Open WebUI, AnythingLLM:** funding and revenue.
6. **A limitation of the method:** for Jan, GPT4All, LocalAI, Lemonade, Docker Model Runner, RamaLama, Open WebUI and AnythingLLM I did not have full checkouts.

Sources of the chapter: [`SOURCES.md`](SOURCES.md) and the file `05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md.sources.txt` next to it.
