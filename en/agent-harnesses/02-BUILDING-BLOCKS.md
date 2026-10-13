# Building blocks — everything the harness does not provide on its own

**As of 11 October 2026.** A harness is a loop, tools and context. For an agent to hunt for opportunities, watch
prices, talk in Polish or look at photos, it needs building blocks: a search engine, a crawler, a queue, notifications,
a speech model, a vision model. Here are the best of them, picked for your hardware. Sources: [SOURCES.md](SOURCES.md).

**Selection rules** (the same in every section):

- **No Docker to start with.** There is no Docker on the machine today, so I prefer `pip`, `npx` / `uvx` or a single
  binary. I flag "Docker-only" tools.
- **Local executors get small, read-only toolsets.** Tools that write and change the world are kept by the planner
  (Opus) or a human.
- **One gateway in front of Anthropic and llama-swap** — cost and concurrency visible in one place.
- **The license matters** for commercial use (U2): models and tools that are "non-commercial only" are marked ⚠️.

Use-case abbreviations: **U1** DevOps, **U2** passive income (complex workflows), **U3** markets and opportunities
(search + alerts), **U4** voice, **U5** images.

---

## Table of contents

1. [Gateway and model routing](#gateway-and-model-routing)
2. [Search and page fetching](#search-and-page-fetching)
3. [Browser agents](#browser-agents)
4. [Deep research](#deep-research)
5. [Price and page-change monitoring](#price-and-page-change-monitoring)
6. [Financial data](#financial-data)
7. [Notifications and channels](#notifications-and-channels)
8. [Scheduling and durable execution](#scheduling-and-durable-execution)
9. [Memory](#memory)
10. [Observability and evaluation](#observability-and-evaluation)
11. [Sandboxes](#sandboxes)
12. [MCP servers for DevOps](#mcp-servers-for-devops)
13. [Voice](#voice)
14. [Vision](#vision)
15. [Tool-call reliability and prompt tuning](#tool-call-reliability-and-prompt-tuning)
16. [Minimal starter sets](#minimal-starter-sets)

---

## Gateway and model routing

| Tool | Purpose | License | Local | Notes (2026) |
|---|---|---|---|---|
| [llama-swap](https://github.com/mostlygeek/llama-swap) ⭐ | swapping local models, one address for chat, embeddings, audio and images; also speaks the Anthropic `/v1/messages` API | MIT | single binary | you already have it; no budgets or billing; exceeding `concurrencyLimit` returns 429 immediately |
| [Bifrost](https://github.com/maximhq/bifrost) ⭐ | gateway in front of Anthropic + llama-swap: fallbacks, virtual keys with budgets, a queue | Apache-2.0 (core) | single binary (Go) | `concurrency: 4` per provider with a queue — exactly your slots; authentication enabled by default since v2.2.6 |
| [LiteLLM](https://github.com/BerriAI/litellm) ⚠️ | the richest budgets and billing per key / team | MIT + `enterprise/` | pip | **24 March 2026 stolen PyPI credentials → malicious versions 1.82.7 and 1.82.8**; more proxy security advisories in 2026. If you use it — pin exact versions with hashes |
| TensorZero | — | — | — | ⛔ archived 12 June 2026 |
| RouteLLM | — | — | — | ⛔ no commits since 2024 |

> 💡 **Note on course 1.** [Part 9, §2.1](../course_local_models/09-TOOL-LANDSCAPE.md) recommends LiteLLM — it was written
> before the March 2026 incident. Today I would pick Bifrost as the default gateway, and LiteLLM only with pinned versions.

---

## Search and page fetching

| Tool | Purpose | License | Local | Notes (2026) |
|---|---|---|---|---|
| [SearXNG](https://github.com/searxng/searxng) ⭐ | private search API (U3, U1) | AGPL-3.0 | no Docker | **JSON disabled by default** — add `json` to `search.formats`, otherwise the agent gets 403; public instances usually block JSON |
| [Crawl4AI](https://github.com/unclecode/crawl4ai) ⭐ | page → clean Markdown, CSS/XPath extraction without an LLM or with an LLM via llama-swap (U3, U2) | Apache-2.0 | pip library | use the library, **do not expose the Docker API server** — a series of security fixes in 2026 (RCE via hooks, sandbox escapes) |
| [Trafilatura](https://github.com/adbar/trafilatura) | the cheapest HTML → text path for news and RSS | Apache-2.0 | pip, no browser | does not execute JavaScript |
| [Scrapling](https://github.com/D4Vinci/Scrapling) | shops that block an ordinary crawler; built-in MCP server | BSD-3 | pip, Docker optional | respect sites' terms of service; a single maintainer; breaking MCP changes in v0.4.15 |
| [Firecrawl](https://github.com/firecrawl/firecrawl) | scrape / crawl / search API | AGPL-3.0 | **Docker Compose** | the self-host version lacks the cloud's anti-bot engine; local LLM support is "experimental" |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | browser via the accessibility tree — works with models without vision | Apache-2.0 | `npx` | the README itself recommends Playwright CLI + skills for agents (fewer tokens); "not a security boundary" |
| [agent-browser](https://github.com/vercel-labs/agent-browser) | browser as a CLI with element references — small context for local executors | Apache-2.0 | npm / cargo | an experimental Vercel Labs project |

---

## Browser agents

| Tool | Purpose | License | Local | Notes (2026) |
|---|---|---|---|---|
| [browser-use](https://github.com/browser-use/browser-use) | the default open browser agent: forms, multi-step tasks (U2, U3) | MIT | any OpenAI-compatible endpoint | the docs warn that small models return wrong action schemas; anti-bot and CAPTCHA only in the paid cloud |
| [Stagehand](https://github.com/browserbase/stagehand) | mixing a script with LLM steps: `act` / `extract` / `observe` — predictable flows (U2) | MIT | OpenAI-compatible `baseURL` | the best features (cache, Model Gateway) are on the Browserbase cloud side |
| [Skyvern](https://github.com/Skyvern-AI/skyvern) | repeatable forms and portals, vision model (U2) | AGPL-3.0 | `ENABLE_OPENAI_COMPATIBLE=true` | anti-bot and proxy only in the cloud; AGPL matters when exposing it as a service |
| [Nanobrowser](https://github.com/nanobrowser/nanobrowser) | Chrome extension with agents in your logged-in browser (U3 ad hoc) | Apache-2.0 | own OpenAI-compatible provider | does not work without a window — hard to schedule and orchestrate |

---

## Deep research

| Tool | Purpose | License | Local | Notes (2026) |
|---|---|---|---|---|
| [Local Deep Research](https://github.com/LearningCircuit/local-deep-research) ⭐ | planned, cited reports and topic "subscriptions" on SearXNG + llama-swap (U3, U2) | MIT | pip or Docker | the most local of the group, publishes results on local models; no global subagent limit (#6820) — limit it with the gateway |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | a mature report library with citations, called by the orchestrator (U3) | Apache-2.0 | `OPENAI_BASE_URL` + `FAST_LLM` / `SMART_LLM` | since v3.7.0 it does not need embeddings (BM25); requires Python 3.12+ |
| [Vane](https://github.com/ItzCrazyKns/Vane) (formerly Perplexica) | interactive search engine with citations for a human | MIT | OpenAI-compatible, Docker recommended | weaker as a building block without a UI |
| [Deep Agents](https://github.com/langchain-ai/deepagents) | successor to the archived (21 August 2026) Open Deep Research — a framework, not a finished app | MIT | any LangChain model | see [01-PROFILES.md](01-PROFILES.md#6-deep-agents) |
| STORM / Co-STORM | long Wikipedia-style reports | MIT | LiteLLM | ⛔ maintenance mode, no activity in 2026 |

---

## Price and page-change monitoring

| Tool | Purpose | License | Local | Notes (2026) |
|---|---|---|---|---|
| [changedetection.io](https://github.com/dgtlmoon/changedetection.io) ⭐ | watching prices and availability: "Re-stock & Price" mode, thresholds, price history, login via Browser Steps (U3) | Apache-2.0 | pip possible | since 0.55.x AI rules ("notify me when the price < 50") and summaries via a llama.cpp endpoint; REST API — the agent creates watches itself; notifications via Apprise |
| [Huginn](https://github.com/huginn/huginn) | multi-source event pipelines: RSS → filter → LLM → Telegram (U3) | MIT | OpenAI agent with `base_url` | came back to life in 2026 (releases since 08.2026, mostly security patches); Docker recommended |
| [urlwatch](https://github.com/thp/urlwatch) | watching URLs from cron or a systemd timer, no Docker and no daemon | BSD-3 | no LLM (hook in a script) | no price semantics and no UI |
| [PriceBuddy](https://github.com/jez500/pricebuddy) | multi-shop price tracker with MCP | ⚠️ "GPL-3.0 with modifications" | Docker | AI only via Ollama — check the license before commercial use |
| PriceGhost, Discount Bandit | — | ⛔ no license file | — | legally "all rights reserved" — avoid |

---

## Financial data

> ⚠️ These tools provide **data and analysis**, not investment advice. Agents' verdicts (e.g. TradingAgents) are opinions,
> not signals. Check the terms of the data sources — some free ones are "personal use only".

| Tool | Purpose | License | Local | Notes (2026) |
|---|---|---|---|---|
| [OpenBB ODP + openbb-mcp-server](https://github.com/openbq-org/OpenBB) ⭐ | one data layer for many providers (equities, macro, options, crypto), official MCP server (U3) | **Apache-2.0 since V5** (30 September 2026; AGPL before) | pip | the repository now redirects to `openbq-org/OpenBB`; for small models use `--tool-discovery` and limit the tool categories |
| [edgartools](https://github.com/dgunning/edgartools) | SEC reports, insider transactions (Form 4), 13F; MCP server | MIT | pip | US companies only; limit of 10 requests/s (SEC rules) |
| [CCXT + ccxt-mcp](https://github.com/ccxt/ccxt) | 100+ crypto exchanges and prediction markets, price and spread alerts | MIT | `npx -y ccxt-mcp` | ⚠️ a misconfigured MCP server **can place orders** — keep agents at read-only levels |
| [TradingAgents](https://github.com/TauricResearch/TradingAgents) | a "trading firm" of analysts, bull/bear debates and a risk manager for a single company | Apache-2.0 | `llm_provider: "openai_compatible"` | since v0.6.0 a separate provider per tier: Opus as `deep_think`, local analysts as `quick_think`; slow at 13.6 tok/s |
| [FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) | company reports; the numbers (DCF, WACC) are computed by code, the LLM only writes | Apache-2.0 | poorly — requires an API key | a good **pattern**: "the LLM narrates, code computes" |
| yfinance / Alpha Vantage / FRED | prices, fundamentals, macro | code Apache / MIT | pip / `uvx` | Yahoo: unofficial endpoints, 429 blocks, data "for personal use"; Alpha Vantage free: 25 requests/day; FRED: free key |

---

## Notifications and channels

| Tool | Purpose | License | Local | Notes (2026) |
|---|---|---|---|---|
| [ntfy](https://github.com/binwiederhier/ntfy) ⭐ | phone push with a single `curl -d "…" host/topic` — the simplest tool for an agent | Apache-2.0 / GPLv2 | single binary | for instant notifications on iOS set `upstream-base-url` to ntfy.sh |
| [Apprise](https://github.com/caronc/apprise) ⭐ | one library → 100+ channels; routing in configuration, not in agent code | BSD-2 | pip | **v2.0.0 (26 September 2026) breaks the API** (`notify()` returns an object) — pin 2.x |
| [Telegram Bot API](https://core.telegram.org/bots/api) | interactive alerts with buttons ("snooze", "open the offer"), talking to the agent from a phone, voice notes as input (the 2026 versions 10.1–10.3 added, among other things, formatting, ephemeral messages and new voice-input options) | free | long polling — no public address | the account is tied to a phone number, the service is centralized — do not send work data there |
| [Gotify](https://github.com/gotify/server) | a fully self-contained message server | MIT | single binary | no external relay |
| [Matrix](https://github.com/element-hq/synapse) | encrypted rooms that are entirely yours — good for U1 incidents | AGPL-3.0 (Synapse) | pip / continuwuity as a binary | the highest maintenance overhead |

---

## Scheduling and durable execution

| Tool | Purpose | License | Local | Notes (2026) |
|---|---|---|---|---|
| **systemd timers** ⭐ | "run script X every N minutes"; `Persistent=true` catches up on missed runs | system | native | no retries and no concurrency between jobs — the script must be idempotent |
| [Prefect](https://github.com/PrefectHQ/prefect) ⭐ | Python pipelines: fetch → enrich → alert; retries, cache, automations (U2, U3) | Apache-2.0 | `prefect server start` on SQLite, no Docker | official `PrefectAgent` in Pydantic AI |
| [DBOS Transact](https://github.com/dbos-inc/dbos-transact-py) | durable workflows as a library, queues with a concurrency limit (cap 4!) | MIT | Postgres only | Pydantic AI's durability backend |
| [Temporal](https://github.com/temporalio/temporal) | the reference durable-execution engine; long workflows that wait for a human | MIT | `temporal server start-dev` | the largest overhead and a steep learning curve; integrations with most frameworks |
| [Hatchet](https://github.com/hatchet-dev/hatchet) | durable tasks for agents, concurrency limits and keys | MIT | Postgres | — |
| [Trigger.dev](https://github.com/triggerdotdev/trigger.dev) | TS tasks with named, shared concurrency limits and cron | Apache-2.0 | Docker / K8s | checkpoints and autoscaling only in the cloud |
| Inngest | event-driven step functions | ⚠️ SSPL (each version → Apache after 3 years) | single binary | license |

---

## Memory

| Tool | Purpose | License | Local | Notes (2026) |
|---|---|---|---|---|
| [Cognee](https://github.com/topoteretes/cognee) ⭐ | knowledge graph + vectors from documents, code and conversations; MCP server (U1 runbooks, U2/U3 corpora) | Apache-2.0 | built-in stack (SQLite + LanceDB), `LLM_PROVIDER=custom` | since v1.6.0 it works without any cloud key |
| [Graphiti](https://github.com/getzep/graphiti) | temporal graph: facts with a validity window ("price from–to", infrastructure state) | Apache-2.0 | `OpenAIGenericClient` | requires Neo4j (GPL) or FalkorDB (SSPL); many LLM calls per episode |
| [Mem0](https://github.com/mem0ai/mem0) | the simplest memory for assistant preferences and state | Apache-2.0 | vLLM / LM Studio providers | **graph memory removed from the open version** (platform only); OpenMemory MCP phased out (07.2026) |
| [Letta Code](https://github.com/letta-ai/letta-code) | an agent with memory as its core, not a library | Apache-2.0 | local: Ollama / LM Studio / llama.cpp | moved to TypeScript; see [01-PROFILES.md](01-PROFILES.md#remaining-candidates-ranks-2164) |

---

## Observability and evaluation

| Tool | Purpose | License | Local | Notes (2026) |
|---|---|---|---|---|
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) ⭐ | OpenTelemetry traces, evaluations, a built-in MCP server — Opus can read the traces itself | ⚠️ Elastic License 2.0 | `pip install` + SQLite | the lightest full option; ELv2 is fine for your own use, not as a service |
| [Langfuse](https://github.com/langfuse/langfuse) | the most complete platform: traces, costs, prompts, monitors with alerts | MIT (core) | Postgres + ClickHouse + Redis + S3 | heavy to self-host |
| [OpenLIT](https://github.com/openlit/openlit) | traces + **AMD GPU monitoring** (usage, memory, power) correlated with traces; detecting looping agents | Apache-2.0 | ClickHouse | interesting for 4× R9700 |
| [promptfoo](https://github.com/promptfoo/promptfoo) ⭐ | regression tests for prompts and tool calls: DeepSeek versus Opus on your tasks, red teaming | MIT | llama.cpp provider | **acquired by OpenAI on 9 March 2026**, still MIT; 0.124.0 moved many SDKs to optional install |

The courses already have their own evaluation tooling — [course 2, part 14](../course_agentic_apps/14-EVALUATION.md) and
[local-llm-quality-bench](https://github.com/michal-koniu/local-llm-quality-bench).

---

## Sandboxes

| Tool | Purpose | License | Local | Notes (2026) |
|---|---|---|---|---|
| [sandbox-runtime (srt)](https://github.com/anthropic-experimental/sandbox-runtime) ⭐ | allowlists of paths and hosts for any process — the executor's shell, local MCP servers | Apache-2.0 | bubblewrap + socat, no Docker | "early research preview"; namespaces on a shared kernel — weaker than a micro-VM |
| [bubblewrap](https://github.com/containers/bubblewrap) | primitive under srt; manual per-command profiles | LGPL | requires user namespaces | not a ready-made sandbox — security depends on the arguments; see [course 1, part 7](../course_local_models/07-SANDBOX-SECURITY-MONITORING.md) |
| [microsandbox](https://github.com/superradcompany/microsandbox) ⭐ | micro-VMs (libkrun) for untrusted LLM-written code; MCP server | Apache-2.0 | KVM, no Docker | beta, breaking changes |
| [E2B runtime](https://github.com/e2b-dev/runtime) | standard sandbox SDK for frameworks | Apache-2.0 | Docker + KVM | "Embed" mode on a single machine |
| [gVisor](https://github.com/google/gvisor) | a user-space kernel for containers | Apache-2.0 | no KVM | GPU only NVIDIA |
| Daytona | — | ⛔ core closed 11 June 2026 | — | do not pick for new projects |

---

## MCP servers for DevOps

Local models get lost with long tool lists — pick **2–3 servers**, not all of them (pitfall H5
in [01-PROFILES.md](01-PROFILES.md#seven-pitfalls-common-to-all)).

| Server | Purpose | License | Safe mode | Notes (2026) |
|---|---|---|---|---|
| [kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) ⭐ | Kubernetes / OpenShift directly via the API (not a kubectl wrapper), multiple clusters | Apache-2.0 | `read_only = true`, `disable_destructive = true`, `Secret` in `denied_resources` | `npx` / `uvx` / binary; pre-1.0 |
| [mcp-grafana](https://github.com/grafana/mcp-grafana) ⭐ | Prometheus (PromQL), Loki (LogQL), Tempo, dashboards, incidents | Apache-2.0 | `--disable-write`, `--enabled-tools` | **v2.0.0 turned on anonymous statistics by default** — turn them off |
| [github-mcp-server](https://github.com/github/github-mcp-server) | CI, PRs, issues, Dependabot | MIT | `--read-only`, narrow `--toolsets` | v2.0.0 added typed outputs for "code mode" |
| GitLab MCP (built in) | MRs, CI, work items | GitLab | no global read-only mode | GA on all plans since GitLab 19.5; use a low-privilege account |
| [awslabs/mcp](https://github.com/awslabs/mcp) | EKS, ECS, IaC, CloudWatch | Apache-2.0 | many read-only by default | dozens of servers — pick 2–3 |
| [gcloud-mcp](https://github.com/googleapis/gcloud-mcp) | Cloud Logging, Monitoring, Trace | Apache-2.0 | deny list of commands | preview, breaking changes |
| [terraform-mcp-server](https://github.com/hashicorp/terraform-mcp-server) | provider and module documentation, HCP Terraform | MPL-2.0 | — | `go install` without Docker |
| Datadog MCP | logs, metrics, traces, monitors | closed SaaS | `mcp_read` / `mcp_write` roles | remote only |

---

## Voice

**Key constraint:** DeepSeek-V4-Flash at 3 bits takes 104.2 GB, and with 4 slots of 131k it takes practically all
128 GB of VRAM. Every speech model on a GPU must either run on the CPU or get a card freed by llama-swap.

| Layer | Choice | License | Polish | Notes |
|---|---|---|---|---|
| Conversation framework | [Pipecat](https://github.com/pipecat-ai/pipecat) ⭐ | BSD-2 | ✅ via Smart Turn | `base_url` for the LLM and STT — you plug in llama-swap and whisper-server; pip, no Docker |
| End-of-utterance detection | [Smart Turn v3.2](https://github.com/pipecat-ai/smart-turn) | BSD-2 | ✅ (94.47% per the v3.0 announcement) | 8 MB, CPU, ~10–100 ms |
| Framework alternative | [LiveKit Agents](https://github.com/livekit/agents) | Apache-2.0 | ❌ turn detectors without Polish | only when you need WebRTC or telephony |
| STT (main) | [whisper.cpp](https://github.com/ggml-org/whisper.cpp) large-v3 | MIT | ✅ **WER 4.74% (FLEURS-pl)** — the best open one | ROCm (HIP) documented; you already have it |
| STT (on CPU, offloads the GPU) | [Parakeet-TDT-0.6B-v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) via parakeet.cpp / onnx-asr | CC-BY-4.0 | ✅ WER 7.31% | very fast, timestamps |
| STT to test | [Qwen3-ASR](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) in llama.cpp | Apache-2.0 | Polish on the list, no WER | works in your llama-swap (audio in llama.cpp is experimental) |
| Polish TTS (now) | [Piper](https://github.com/OHF-Voice/piper1-gpl) pl_PL | engine GPL-3.0, voices separately | ✅ 5 voices | CPU, almost zero latency, sounds robotic |
| Polish TTS (better) | [Chatterbox Multilingual V3](https://github.com/resemble-ai/chatterbox) | MIT (every recording carries an inaudible watermark) | ✅ | 0.5B; ROCm undocumented — reserve a day for testing |
| Polish TTS (better) | [VoxCPM2](https://github.com/OpenBMB/VoxCPM) | Apache-2.0 | ✅ | 2B, 48 kHz; AMD support unconfirmed |
| English TTS | [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) | Apache-2.0 | ❌ | small and good — EN only |
| ⚠️ to avoid for U2 | XTTS-v2, F5-TTS, Higgs Audio v3, Fish Audio S2 | non-commercial weights | — | the license blocks commercial use |

**Speech-to-speech in Polish locally on AMD — in October 2026 I did not find a working model.** Moshi is EN and CUDA,
Qwen3-Omni does not speak Polish, Unmute is EN/FR and CUDA. Only the STT → LLM → TTS cascade works
(details and latencies: [03-ARCHITECTURE.md](03-ARCHITECTURE.md#u4--voice-conversation-in-polish)).

---

## Vision

| Need | Choice | License | Notes |
|---|---|---|---|
| Can the main executor see? | **DeepSeek-V4-Flash is text-only.** To test: [DeepSeek-V4-Flash-Vision-Exp](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp) — the same size + ~0.93 GB mmproj | MIT | experimental, untested on ROCm; requires llama.cpp ≥ b10766; images + tool calls at the same time unverified — keep the text GGUF as a fallback |
| A separate vision executor (screenshots, photos, charts) | [Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) (Q4 ~23 GB, 3B active) or [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) (Q4 ~18.5 GB) | Apache-2.0 | fits on a single R9700; replaces Qwen2.5-VL-7B from [course 1, part 5](../course_local_models/05-MULTIMODALITY.md); needs a free card |
| GUI agent (computer use) | [Holo4-35B-A3B](https://huggingface.co/Hcompany/Holo4-35B-A3B) | Apache-2.0 | ⚠️ avoid Holo4-27B (CC-BY-NC) |
| Documents and OCR | [Docling](https://github.com/docling-project/docling) + [PaddleOCR-VL-1.5](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5) | MIT / Apache-2.0 | official llama.cpp support, little VRAM; Docling has an MCP server |
| Image generation and editing | [ComfyUI](https://github.com/comfyanonymous/ComfyUI) on PyTorch ROCm wheels + [Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511), [Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo), [FLUX.2 klein 4B](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B) | ComfyUI GPL-3.0; models Apache-2.0 | lighter: [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) `sd-server` behind llama-swap; ⚠️ avoid FLUX dev, Qwen-Image-2.1 (non-commercial) and Hunyuan models (the license excludes the EU) |
| Hard cases | send the image to Opus 5.5 | — | a cost / privacy trade-off |

---

## Tool-call reliability and prompt tuning

| Tool | Purpose | License | Notes |
|---|---|---|---|
| [forge](https://github.com/antoinezambelli/forge) | a "reliability layer" for local models: rescuing broken tool calls, retries, validation, forced steps; `SlotWorker` — a priority queue for shared slots | MIT | results (8B: from a few to 84%) reported by the author himself; a single maintainer; a proxy in front of llama-server |
| [DSPy](https://github.com/stanfordnlp/dspy) | "programming, not prompting": the GEPA optimizer with Claude as the teacher tunes prompts that the local model then executes | MIT | best for precise extraction and classification of offers (U3); not an agent runtime |

---

## Minimal starter sets

A common base for U1–U3: **llama-swap** (you have it) + **Bifrost** (limit 4, budgets) + **Phoenix** (traces).

| Use case | Set |
|---|---|
| **U1 — DevOps** | kubernetes-mcp-server (read-only) · mcp-grafana (`--disable-write`) · github-mcp-server or GitLab MCP · srt around each executor's shell · promptfoo to check whether DeepSeek copes with your runbooks before you hand them over |
| **U2 — passive income** | Prefect (or DBOS with a queue limit of 4) · Cognee as memory · microsandbox for agent-written code · Apprise → ntfy for "approve / done / error" · promptfoo in CI |
| **U3 — markets and opportunities** | SearXNG (with JSON) · Crawl4AI as a library + Trafilatura · changedetection.io for prices · OpenBB ODP + MCP, edgartools, read-only CCXT · Local Deep Research for cited overviews · ntfy via Apprise + a Telegram bot · systemd timers, then Prefect |
| **U4 — voice** | Pipecat + Smart Turn · whisper.cpp large-v3 (or Parakeet on CPU) · gpt-oss-20b as a fast "voice" delegating to DeepSeek / Opus · Piper pl_PL, then Chatterbox or VoxCPM2 |
| **U5 — images** | Vision-Exp test · Qwen3.6-35B-A3B as the vision executor · Docling + PaddleOCR-VL · stable-diffusion.cpp or ComfyUI with Apache-2.0 models |

How these blocks connect with the harness and the Opus planner — [03-ARCHITECTURE.md](03-ARCHITECTURE.md).
