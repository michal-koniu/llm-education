# Agent harnesses for local models — an overview

**As of 11 October 2026.** Which open harnesses turn a local model into an agent, how they differ,
which to pick for what — and when it is better to assemble your own. A ranking of the top 20 out of 72 examined, with profiles,
building blocks and an architecture for specific hardware.

> ⚠️ **This overview goes stale within weeks.** In 2026 some popular projects died or changed owners
> (Roo Code, Flowise, Continue, Aider), and new ones earned hundreds of thousands of stars in two months. I pulled the stars and releases
> from the GitHub API on 11 October 2026. **I have not tested anything here on my own machine** — this is a review of documentation,
> code, release notes and issues, not a measurement. Your measurement wins.

---

## Table of contents

- [Why this overview](#why-this-overview)
- [The shortest answer](#the-shortest-answer)
- [What a harness is](#what-a-harness-is)
- [Ranking: the top 20 harnesses](#ranking-the-top-20-harnesses)
- [Technical comparison](#technical-comparison)
- [Which one for which use case](#which-one-for-which-use-case)
- [Verdict: build on a harness or assemble your own?](#verdict-build-on-a-harness-or-assemble-your-own)
- [Why they are not at the top](#why-they-are-not-at-the-top)
- [How I computed the ranking](#how-i-computed-the-ranking)
- [Files in this directory](#files-in-this-directory)
- [Related course parts](#related-course-parts)

---

## Why this overview

I build multi-agent applications, local or hybrid:

- **locally** — up to 4 agents at once on DeepSeek-V4-Flash (4× AMD Radeon AI PRO R9700, llama-swap, 4 slots of 131k
  context each, about 13.6 tok/s per agent);
- **hybrid** — Claude Opus 5.5 as planner and orchestrator (the most intelligence), local agents as
  executors (the lowest cost of work).

Five use cases by which I rate every harness:

| Abbreviation | Use case | What it requires |
|---|---|---|
| **U1** | DevOps: development and diagnostics | shell, kubectl, logs and metrics, safe permissions, headless mode |
| **U2** | passive or nearly passive income | complex, long workflows, persistence, scheduling, approvals |
| **U3** | opportunities on financial markets and great sales deals | deep, precise and efficient search, monitoring, alerts |
| **U4** | talking to agents by voice | STT and TTS in Polish, short latency |
| **U5** | working with photos and images | vision model, OCR, generation and editing |

---

## The shortest answer

- **There is no single harness for everything.** The best setup has three layers: a ready-made coding agent for U1, your own
  framework-based applications for U2 and U3, and a personal assistant with voice as the interface.
- **U1 → [OpenCode](01-PROFILES.md#8-opencode)** (or [Goose](01-PROFILES.md#2-goose)): main agent on Opus 5.5,
  subagents on DeepSeek, permissions on command patterns. Do not build this yourself.
- **U2 and U3 → your own application on [Pydantic AI](01-PROFILES.md#5-pydantic-ai)** (the only framework with a built-in limit
  of 4 slots) **or [LangGraph](01-PROFILES.md#1-langgraph)** (the most mature persistence) + building blocks from [02-BUILDING-BLOCKS.md](02-BUILDING-BLOCKS.md).
  No code: [n8n](01-PROFILES.md#18-n8n).
- **U4 and U5 to start → [Hermes Agent](01-PROFILES.md#4-hermes-agent)**: voice notes on Telegram with local
  speech recognition (faster-whisper), a "vision bridge" for the text-only DeepSeek, the best cron. Note: speech synthesis
  goes through the cloud by default (Edge TTS), and a local Polish voice is not confirmed — a fully local voice with Polish
  Piper is offered by [Moltis](01-PROFILES.md#15-moltis). Live conversation in Polish — [Pipecat](02-BUILDING-BLOCKS.md#voice).
- **DeepSeek-V4-Flash cannot see images** and takes up practically all the VRAM — voice and vision must run on the CPU, on a freed-up
  card or in the cloud ([03-ARCHITECTURE.md](03-ARCHITECTURE.md#1-resources-what-you-really-have)).
- **Claude Code subagents on local models are not a supported feature.** It works the other way round: Claude orchestrates,
  local agents are its tools (MCP).
- **Local is not always cheaper.** With short contexts Claude Haiku 5.5 (USD 0.10 / 0.50 per million tokens)
  costs about as much as this machine's electricity at full load; with contexts above 100k tokens
  and compared with Sonnet or Opus, local DeepSeek comes out clearly cheaper. Certain local advantages are privacy,
  no limits and working offline ([costs](03-ARCHITECTURE.md#5-costs-is-local-cheaper)).

---

## What a harness is

A language model does nothing by itself — it answers with text. A **harness** is everything around it that turns it into an agent:
the loop (think → call a tool → read the result → again), tools, context and memory management,
permissions and sandbox, scheduling, channels (terminal, chat, voice), observability. You build the loop from scratch
in [course 1, part 6](../course_local_models/06-AGENT-LOOP-FROM-SCRATCH.md), and a long-task harness
in [course 2, part 3](../course_agentic_apps/03-HARNESS-LONG-RUNNING-TASKS.md).

The ranking contains four kinds of harnesses:

| Kind | Examples | When |
|---|---|---|
| **coding agent** — a ready-made program in the terminal / IDE | OpenCode, Goose, OpenHands, Pi | U1; as an executor in your application |
| **always-on personal agent** — a ready-made assistant with messengers | Hermes Agent, ZeroClaw, Moltis | U4, U5, simple U3 watchers |
| **framework** — a library for building your own agents | LangGraph, Pydantic AI, Strands, Microsoft Agent Framework | U2, U3 — your own applications |
| **workflow platform** — visually connecting integrations | n8n | U2, U3 without code |

---

## Ranking: the top 20 harnesses

The columns "What it is", "What it is for" and "What problem it solves" answer the question of what each one beats the competition at.
Details, local model configuration, weak points and ideas to steal — in [01-PROFILES.md](01-PROFILES.md).

<!-- main-table -->
| # | Harness | Category | What it is | What it is for | What problem it solves (advantage) | License |
|---|---|---|---|---|---|---|
| 1 | [LangGraph](01-PROFILES.md#1-langgraph) | Python framework | agent runtime built as state graphs with a checkpoint after every step | durable, resumable multi-agent workflows with a human in the loop | an interrupted task returns exactly where it stopped — even after a restart; the most mature persistence in Python | MIT |
| 2 | [Goose](01-PROFILES.md#2-goose) | coding | general-purpose agent in Rust, under the AAIF foundation (Linux Foundation) | code, automations and repeatable "recipes" on your own machine | recipes + cron + subagents with their own model in one tool; an experimental *tool shim* (translating via Ollama or built-in llama.cpp) rescues models that call tools poorly | Apache-2.0 |
| 3 | [OpenHands](01-PROFILES.md#3-openhands) | coding | platform of coding agents + SDK + agent server | an "engineering team" running continuously: conversations, automations from cron and webhooks | the fullest stack to embed in your own application; a container for every conversation; the agent exposed as an OpenAI "model" | MIT |
| 4 | [Hermes Agent](01-PROFILES.md#4-hermes-agent) | personal | self-learning assistant with 25+ messengers, voice and cron | a personal agent reachable from your phone, scheduled tasks, delegation | the "frontier planner, cheap executors" pattern built into the configuration; the strongest cron; voice in messengers with local speech recognition | MIT |
| 5 | [Pydantic AI](01-PROFILES.md#5-pydantic-ai) | Python framework | typed agent framework from the creators of Pydantic | production agents with validated structured output | the only shared per-model concurrency limiter — exactly 4 slots; the best structured output; persistence via Temporal / DBOS / Prefect | MIT |
| 6 | [Deep Agents](01-PROFILES.md#6-deep-agents) | Python framework | ready-made Claude Code-style harness on LangGraph | long tasks: research, code, ops — without building the plumbing | planning + file system + subagents + compaction in one call, on LangGraph persistence | MIT |
| 7 | [Strands Agents](01-PROFILES.md#7-strands-agents) | Python framework | agent SDK from AWS + a ready-made harness | your own loop without writing your own loop, any model and cloud | a native llama.cpp provider with grammars and `cache_prompt` instead of pretending to be OpenAI | Apache-2.0 |
| 8 | [OpenCode](01-PROFILES.md#8-opencode) | coding | coding agent with an HTTP server (the TUI is just one client) | programming and DevOps in the terminal; embedding via API | client–server architecture with OpenAPI; agents and subagents with their own model and permissions on command patterns | MIT |
| 9 | [DeerFlow](01-PROFILES.md#9-deerflow) | personal | ByteDance's "super-agent" for long tasks | research, code and content with subagents in sandboxes | deep research lineage + an explicit model per subagent (documented as "local to save money") + scheduled tasks with a goal and a stop condition | MIT |
| 10 | [ZeroClaw](01-PROFILES.md#10-zeroclaw) | personal | agent runtime in a single Rust binary, 30+ channels | a personal agent running on your tools under control | the deepest security model: risk profiles, autonomy levels, automatic sandbox, signed confirmations | MIT / Apache-2.0 |
| 11 | [Microsoft Agent Framework](01-PROFILES.md#11-microsoft-agent-framework) | Python framework | successor to AutoGen and Semantic Kernel with a workflow engine | enterprise multi-agent workflows with checkpoints | a stable API with long support; ready-made orchestrations (Magentic, Handoff); prompt injection protection (FIDES) | MIT |
| 12 | [DeepSeek Harness](01-PROFILES.md#12-deepseek-harness) | coding | DeepSeek's official harness built entirely from plugins | an agent on DeepSeek models, embedded in a Web UI, CLI or SDK | tuning for DeepSeek V4 from the vendor; subagents can be other harnesses, including Claude Code | MIT |
| 13 | [Pi](01-PROFILES.md#13-pi) | coding | a minimal coding harness + the libraries other harnesses are built on | your own agent on a small core; learning | a small core with the deepest extension API; native llama.cpp; "virtual models" routing each request where it should go | MIT |
| 14 | [gptme](01-PROFILES.md#14-gptme) | coding | terminal agent and a skeleton for autonomous agents | a personal agent in the terminal, agents running continuously under systemd | a swappable tool format (Markdown / XML / native) — works where call parsing in llama.cpp fails | MIT |
| 15 | [Moltis](01-PROFILES.md#15-moltis) | personal | personal agent server in a single Rust binary | an assistant with voice, scheduling and a sandbox without installing half the internet | the most complete "single file": local STT / TTS, sandbox choice, executor presets with their own model | MIT |
| 16 | [QwenPaw](01-PROFILES.md#16-qwenpaw) | personal | "Agent OS" from Alibaba AgentScope | a multi-agent assistant with memory and channels | layered security (kernel sandbox, Tool Guard, skill scanner) + a model per agent | Apache-2.0 |
| 17 | [OpenAI Agents SDK](01-PROFILES.md#17-openai-agents-sdk) | Python framework | lightweight SDK with a few primitives | simple multi-agent systems, voice pipelines | the simplest mental model; serializable state for approvals after hours; a voice pipeline with swappable STT / TTS | MIT |
| 18 | [n8n](01-PROFILES.md#18-n8n) | workflow | visual automation platform with agent nodes | gluing integrations, alerts, workflows without code | the widest set of triggers and integrations; per-tool approval sent to a messenger | ⚠️ Sustainable Use (fair-code) |
| 19 | [LibreChat](01-PROFILES.md#19-librechat) | personal | multi-user chat platform with agents | a shared chat for many providers and local models, with agents | a real model choice per agent and subagent teams as graphs; a code interpreter in a micro-VM | MIT |
| 20 | [Kilo Code](01-PROFILES.md#20-kilo-code) | coding | a fork of OpenCode with UI in VS Code and JetBrains | coding in the IDE with subagents | the OpenCode core in the IDE + a manager of parallel agents in separate worktrees; migration from the dead Roo Code | MIT |
<!-- /main-table -->

---

## Technical comparison

✅ present and works with a local model · ⚠️ partially or with a caveat · ❌ absent. "Hybrid" = whether one agent can run
on Claude and others on your llama-swap. Stars and releases: GitHub API, 11 October 2026.

| # | Harness | ⭐ GitHub | Latest release | Local model | Hybrid | MCP | Voice | Image | Scheduling | Sandbox / approvals |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | LangGraph | <!-- gh:langchain-ai/langgraph -->43.1k | 1.2.14 (6 Oct) | ✅ | ✅ model per node | ✅ | ⚠️ DIY cascade | ✅ | ⚠️ Agent Server | ⚠️ human in the loop, no sandbox |
| 2 | Goose | <!-- gh:aaif-goose/goose -->55.1k | 1.54.0 (8 Oct) | ✅ | ✅ `GOOSE_SUBAGENT_*` | ✅ | ⚠️ dictation, no TTS | ✅ | ✅ cron | ⚠️ approval modes, no sandbox |
| 3 | OpenHands | <!-- gh:OpenHands/OpenHands -->90.5k | 1.26.0 (8 Oct) | ✅ | ✅ profile per subagent | ✅ | ⚠️ input only | ✅ | ✅ cron, webhook | ✅ container per conversation |
| 4 | Hermes Agent | <!-- gh:NousResearch/hermes-agent -->252.7k | 0.21.6 (8 Oct) | ✅ | ✅ `delegation.*` | ✅ | ⚠️ STT local, TTS in the cloud by default (Edge) | ✅ vision bridge | ✅ best cron | ✅ smart approvals, Docker, SSH |
| 5 | Pydantic AI | <!-- gh:pydantic/pydantic-ai -->20.5k | 2.55.0 (9 Oct) | ✅ | ✅ + concurrency limit | ✅ | ⚠️ realtime cloud only | ✅ | ❌ (Prefect / DBOS) | ⚠️ tool approvals |
| 6 | Deep Agents | <!-- gh:langchain-ai/deepagents -->30.1k | 0.7.23 (7 Oct) | ✅ | ✅ model per subagent | ✅ | ❌ | ⚠️ | ⚠️ Agent Server | ✅ sandbox backends |
| 7 | Strands Agents | <!-- gh:strands-agents/harness-sdk -->8.8k | harness 0.2.0 (8 Oct) | ✅ native llama.cpp | ✅ | ✅ | ⚠️ cloud only | ✅ | ❌ | ⚠️ |
| 8 | OpenCode | <!-- gh:anomalyco/opencode -->212.6k | 1.19.0 (11 Oct) | ✅ | ✅ model per agent | ✅ | ❌ | ✅ | ❌ | ⚠️ allow / ask / deny rules |
| 9 | DeerFlow | <!-- gh:bytedance/deer-flow -->83.7k | 2.1.0 (24 Sep) | ✅ | ✅ model per subagent | ✅ | ❌ | ✅ | ✅ once / cron / interval | ✅ local, Docker, K8s |
| 10 | ZeroClaw | <!-- gh:zeroclaw-labs/zeroclaw -->33.0k | 0.8.5 (5 Sep) | ✅ `llamacpp` slot | ✅ agent per provider | ✅ | ✅ Piper, phone | ✅ vision redirect | ✅ cron + procedures | ✅ Landlock / Bubblewrap |
| 11 | Microsoft Agent Framework | <!-- gh:microsoft/agent-framework -->14.1k | py 1.21.0 (8 Oct) | ⚠️ beware the Responses API | ✅ | ✅ | ❌ in Python | ✅ | ❌ | ✅ FIDES, micro-VM |
| 12 | DeepSeek Harness | <!-- gh:deepseek-ai/deepseek-harness -->247.3k | 0.2.1-alpha.2 (9 Oct) | ✅ `compat` profile | ✅ also Claude Code as a child | ✅ | ⚠️ no Polish | ✅ | ✅ | ✅ read-only by default |
| 13 | Pi | <!-- gh:earendil-works/pi -->114.2k | 1.1.0 (7 Oct) | ✅ native llama.cpp | ✅ virtual models | ✅ | ❌ | ✅ | ❌ | ❌ by design |
| 14 | gptme | <!-- gh:gptme/gptme -->4.4k | 0.34.0 (18 Sep) | ✅ Markdown / XML formats | ✅ | ✅ | ⚠️ cloud realtime | ✅ | ✅ systemd | ⚠️ shell policy |
| 15 | Moltis | <!-- gh:moltis-org/moltis -->2.9k | 20260913.02 (14 Sep) | ✅ | ✅ presets | ✅ | ✅ local STT / TTS | ⚠️ | ✅ cron, heartbeat | ✅ sandbox choice |
| 16 | QwenPaw | <!-- gh:agentscope-ai/QwenPaw -->35.6k | 2.2.1 (11 Sep) | ✅ | ✅ model per agent | ✅ | ⚠️ transcription errors | ✅ | ✅ | ✅ kernel sandbox |
| 17 | OpenAI Agents SDK | <!-- gh:openai/openai-agents-python -->30.0k | 0.23.1 (2 Oct) | ⚠️ beware the Responses API | ✅ Claude via LiteLLM | ✅ | ⚠️ STT / TTS pipeline (local via custom adapters) | ✅ | ❌ | ✅ sandboxed agents |
| 18 | n8n | <!-- gh:n8n-io/n8n -->207.0k | 2.42.6 (9 Oct) | ⚠️ disable the Responses API | ✅ model per node | ✅ | ❌ to be assembled | ✅ | ✅ best triggers | ⚠️ approvals, CVE history |
| 19 | LibreChat | <!-- gh:LibreChat-AI/LibreChat -->45.5k | 0.8.8 (1 Oct) | ✅ | ✅ subagent teams | ✅ | ✅ STT / TTS | ✅ | ⚠️ experimental | ✅ interpreter in a micro-VM |
| 20 | Kilo Code | <!-- gh:Kilo-Org/kilocode -->27.6k | JetBrains 7.1.9 (8 Oct) | ⚠️ schema errors | ✅ model per subagent | ✅ | ⚠️ cloud Whisper | ⚠️ | ❌ | ⚠️ permission rules |

Before connecting any of them to llama-swap, read
[the seven pitfalls common to all](01-PROFILES.md#seven-pitfalls-common-to-all) — Responses API,
DeepSeek's `reasoning_content`, the context window, prompt cache, number of tools, concurrency limit, tool schemas.

---

## Which one for which use case

Rated 1–5 based on a documentation study (not a measurement). Bold — the best in the column. These numbers measure
how well the features fit the use case and are not a recommendation: the "What to pick" table below also takes into account
readiness for use (e.g. LangGraph has a 5 in U1, but for DevOps it is better to take the ready-made OpenCode than to build an agent
on a framework).

| # | Harness | U1 DevOps | U2 passive income | U3 markets and opportunities | U4 voice | U5 images |
|---|---|---|---|---|---|---|
| 1 | LangGraph | **5** | **5** | 4 | 2 | 3 |
| 2 | Goose | 4 | **5** | 4 | 3 | 3 |
| 3 | OpenHands | 4 | **5** | 3 | 2 | 3 |
| 4 | Hermes Agent | 4 | 4 | 4 | 4 | **4** |
| 5 | Pydantic AI | 4 | **5** | 4 | 4 | **4** |
| 6 | Deep Agents | **5** | 4 | 4 | 1 | 2 |
| 7 | Strands Agents | 4 | 4 | 4 | 3 | 3 |
| 8 | OpenCode | **5** | 4 | 2 | 1 | 3 |
| 9 | DeerFlow | 3 | **5** | 3 | 1 | 3 |
| 10 | ZeroClaw | 4 | 4 | 4 | 4 | **4** |
| 11 | Microsoft Agent Framework | 4 | 4 | 3 | 2 | 3 |
| 12 | DeepSeek Harness | 4 | 4 | 3 | 2 | 3 |
| 13 | Pi | 4 | 4 | 2 | 1 | 3 |
| 14 | gptme | 4 | 4 | 3 | 3 | **4** |
| 15 | Moltis | 4 | 4 | 4 | **5** | 3 |
| 16 | QwenPaw | 3 | 4 | 3 | 3 | 3 |
| 17 | OpenAI Agents SDK | 4 | 3 | 3 | 4 | 3 |
| 18 | n8n | 4 | **5** | **5** | 2 | 3 |
| 19 | LibreChat | 3 | 4 | 3 | 2 | **4** |
| 20 | Kilo Code | 4 | 4 | 2 | 2 | 2 |

What to pick — and with which building blocks:

| Use case | First choice | Alternative | Key building blocks ([02-BUILDING-BLOCKS.md](02-BUILDING-BLOCKS.md)) |
|---|---|---|---|
| **U1** DevOps | OpenCode (Opus as main, DeepSeek subagents) | Goose; or Claude Code + MCP to local agents | kubernetes-mcp-server, mcp-grafana (read-only), srt |
| **U2** passive income | your own application: Pydantic AI or LangGraph | n8n (no code), OpenHands SDK (workflows around code) | Prefect or DBOS, Cognee, ntfy |
| **U3** markets and opportunities | your own funnel (timers + Pydantic AI) or n8n | Hermes Agent (cron watchers), Local Deep Research | SearXNG, Crawl4AI, changedetection.io, OpenBB, ntfy / Telegram |
| **U4** voice | Hermes Agent (voice notes right away; TTS in the cloud) | Moltis (fully local, Piper in Polish); eventually your own Pipecat | Pipecat + Smart Turn, whisper.cpp / Parakeet, Piper → Chatterbox |
| **U5** images | Hermes Agent or ZeroClaw (vision bridge) | your own pipeline | DeepSeek Vision-Exp (test), Qwen3.6-35B-A3B, Docling + PaddleOCR-VL |

How to put it all together on this hardware: [03-ARCHITECTURE.md](03-ARCHITECTURE.md).

---

## Verdict: build on a harness or assemble your own?

**Both — but in different layers.**

| Layer | Decision | Why |
|---|---|---|
| Working agent (U1) | **take a ready-made one** — OpenCode or Goose | these are mature products with hundreds of maintainers; your own will not catch up with them in the shell, file editing and permissions |
| Your applications (U2, U3) | **build on a framework** — Pydantic AI or LangGraph | the advantage lies in fitting the workflow to the idea, and frameworks give persistence, limits and validation without imposing a product |
| Interface and voice (U4, U5) | **take a ready-made one to start** — Hermes Agent; then your own Pipecat | the fastest way to talk to an agent from your phone; pin versions, because the pace of change is enormous |
| Agent loop | **build it yourself once, to understand it** — courses 1 and 2 | whoever has built the loop from scratch knows what to look for in someone else's harness and when to abandon it |

**What to learn from other people's code** (readable core, good ideas): [Pi](01-PROFILES.md#13-pi) — a minimal core
and many embedding modes; [nanobot](https://github.com/HKUDS/nanobot) — readable Python to fork;
[mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) — an agent in 100 lines; [OpenCode](01-PROFILES.md#8-opencode) —
a server with an API and agents as files; [Hermes Agent](01-PROFILES.md#4-hermes-agent) — delegation with a result schema
and cron watchers; [ZeroClaw](01-PROFILES.md#10-zeroclaw) — the security model.

**What to avoid:** dead projects (Roo Code, Flowise, Continue, Plandex); Codex CLI with local models
(Responses API only); LiteLLM without pinned versions (PyPI compromise on 24 March 2026); n8n and OpenClaw exposed
to the internet.

---

## Why they are not at the top

| Project | Rank | Reason |
|---|---|---|
| [OpenClaw](https://github.com/openclaw/openclaw) | 47 (64 pts) | the most popular (391.7k ⭐) and with the most channels, but **722 security advisories published in 2026** (14 critical, counted via the GitHub API), according to industry reports from February 2026 hundreds of malicious skills in ClawHub and tens of thousands of instances exposed to the internet; with local models tool calls silently dropped and the prompt cache destroyed. As an architecture study — excellent: [course 2, part 1](../course_agentic_apps/01-AGENT-ARCHITECTURES.md) |
| [Open WebUI](https://github.com/open-webui/open-webui) | 29 (69 pts) | the best UI for local models, but subagents always run on the parent's model (no hybrid), 158 security advisories in 2026 and a license with a branding clause |
| [Cline](https://github.com/cline/cline) | 33 (68 pts) | tool format changes repeatedly broke local models; dictation is a paid service |
| [CrewAI](https://github.com/crewAIInc/crewAI) | 34 (68 pts) | recurring "empty responses" with local models, telemetry by default, scheduling only in the paid platform |
| [Codex CLI](https://github.com/openai/codex) | 59 (57 pts) | Responses API only since 1 February 2026 — brittle with llama.cpp; no Anthropic provider |
| Aider, Roo Code, Continue, Flowise, Plandex | excluded | halted or archived in 2025–2026 — [details](01-PROFILES.md#excluded-at-entry) |

---

## How I computed the ranking

**1. Entry conditions** (all four): public code and a license that allows self-hosting (source-available
allowed, but marked ⚠️); a documented connection of a local model through an OpenAI-compatible endpoint
(directly or — marked — indirectly, through an adapter); activity — a commit no older than 3 months and a release
(including pre-release) no older than 6 months before 11 October 2026; the project is not officially discontinued — which is why
Continue, for example, drops out: its maintainers announced the end of the project, although the last release dates from June 2026.
Examined: 72 projects, 64 passed, 8 dropped out.

**2. Six criteria, each 1–5, with weights according to my goals:**

| Criterion | Weight | What I assess |
|---|---|---|
| A — multiple agents and hybrid | 25% | subagents, model per agent, Claude as planner with local executors |
| B — local model support | 20% | tool calls with llama.cpp, documentation, known bugs, concurrency limit |
| C — use case coverage | 20% | average of the U1–U5 ratings (table above), rounded |
| D — maturity | 15% | stars, release rhythm, number of maintainers, API stability |
| E — learning value | 10% | readability of the core, documentation, size |
| F — security and control | 10% | sandbox, approvals, vulnerability history |

Score = (25·A + 20·B + 20·C + 15·D + 10·E + 10·F) / 5, that is 0–100. Ties are broken by C, then stars.

**3. Scores of the top** — change the weights and calculate for yourself:

| # | Harness | A | B | C | D | E | F | Score |
|---|---|---|---|---|---|---|---|---|
| 1 | LangGraph | 5 | 4 | 4 | 5 | 3 | 4 | 86 |
| 2 | Goose | 5 | 4 | 4 | 5 | 3 | 3 | 84 |
| 3 | OpenHands | 5 | 4 | 3 | 5 | 3 | 5 | 84 |
| 4 | Hermes Agent | 5 | 4 | 4 | 4 | 2 | 4 | 81 |
| 5 | Pydantic AI | 5 | 4 | 4 | 4 | 3 | 3 | 81 |
| 6 | Deep Agents | 5 | 4 | 3 | 4 | 4 | 4 | 81 |
| 7 | Strands Agents | 4 | 5 | 4 | 4 | 3 | 3 | 80 |
| 8 | OpenCode | 5 | 4 | 3 | 5 | 3 | 3 | 80 |
| 9 | DeerFlow | 5 | 4 | 3 | 4 | 3 | 4 | 79 |
| 10 | ZeroClaw | 4 | 4 | 4 | 4 | 2 | 5 | 78 |
| 11 | Microsoft Agent Framework | 5 | 3 | 3 | 4 | 3 | 5 | 77 |
| 12 | DeepSeek Harness | 5 | 4 | 3 | 3 | 3 | 4 | 76 |
| 13 | Pi | 4 | 5 | 3 | 4 | 5 | 1 | 76 |
| 14 | gptme | 4 | 4 | 4 | 3 | 4 | 3 | 75 |
| 15 | Moltis | 4 | 4 | 4 | 2 | 3 | 5 | 74 |
| 16 | QwenPaw | 4 | 4 | 3 | 4 | 3 | 4 | 74 |
| 17 | OpenAI Agents SDK | 4 | 3 | 3 | 4 | 5 | 4 | 74 |
| 18 | n8n | 4 | 3 | 4 | 5 | 3 | 2 | 73 |
| 19 | LibreChat | 5 | 3 | 3 | 4 | 2 | 4 | 73 |
| 20 | Kilo Code | 5 | 3 | 3 | 4 | 3 | 3 | 73 |

The full list of 64 candidates with scores and the eight excluded — [01-PROFILES.md](01-PROFILES.md#remaining-candidates-ranks-2164).

**4. How I gathered the facts.** Six research agents went through the documentation, READMEs, release notes
and GitHub issues in parallel (separate ones for personal agents, coding agents, Python frameworks, TypeScript and workflow
platforms, building blocks, and voice, vision and hybrid). I pulled the GitHub numbers myself from the API. The most surprising
claims I checked at the primary source (among others the number of security advisories for OpenClaw and Open WebUI, the compromise of
LiteLLM, the archiving of Flowise and Roo Code, the removal of Chat Completions from Codex CLI, the limiter in Pydantic AI, the attack on
Mastra packages, the DeepSeek-V4-Flash model card, Anthropic pricing). Claims based only on blogs and marketing materials
I mark in the profiles.

**Limitations.** Criteria A–F are an assessment, not a measurement. Stars are not quality (DeepSeek Harness collected 247k in two
months). The U1–U5 scores come from documentation analysis. No harness was run on this machine.

---

## Files in this directory

| File | What is in it |
|---|---|
| [README.md](README.md) | this overview: ranking, comparison, choice, verdict, method |
| [01-PROFILES.md](01-PROFILES.md) | the seven common pitfalls, 20 profiles (local model configuration, hybrid, voice, image, security, weak points, what to steal), other candidates and excluded ones |
| [02-BUILDING-BLOCKS.md](02-BUILDING-BLOCKS.md) | gateways, search, browsers, deep research, price monitoring, financial data, notifications, scheduling, memory, observability, sandboxes, MCP for DevOps, voice, image |
| [03-ARCHITECTURE.md](03-ARCHITECTURE.md) | this machine's resources, the planner–executors pattern, what is proven, five setups U1–U5, costs, build path |
| [SOURCES.md](SOURCES.md) | sources with the date checked and what I took from them |

## Related course parts

| Topic | Where |
|---|---|
| agent loop from scratch | [course 1, part 6](../course_local_models/06-AGENT-LOOP-FROM-SCRATCH.md) |
| tool landscape (an earlier, shorter overview of frameworks and coding agents) | [course 1, part 9](../course_local_models/09-TOOL-LANDSCAPE.md) |
| hybrid local + Claude | [course 1, part 10](../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md) |
| agent architectures and OpenClaw broken into parts | [course 2, part 1](../course_agentic_apps/01-AGENT-ARCHITECTURES.md) |
| long-task harness | [course 2, part 3](../course_agentic_apps/03-HARNESS-LONG-RUNNING-TASKS.md) |
| MCP, CLI, A2A | [course 2, part 9](../course_agentic_apps/09-PROTOCOLS-MCP-CLI-A2A.md) |
| multi-agent fleet | [course 2, part 13](../course_agentic_apps/13-MULTI-AGENT-FLEET.md) |
| hybrid router | [course 2, part 17](../course_agentic_apps/17-HYBRID-AND-ROUTER.md) |
| ready-made AI assistants (market, architecture, offline, Poland) | [AI assistants overview](../ai-assistants/README.md) |

Measurements of this machine: [local-llm-bench-results](https://github.com/michal-koniu/local-llm-bench-results)
(speed and quality, also [agents in parallel](https://github.com/michal-koniu/local-llm-bench-results/blob/main/PARALLEL.md)).

Text license: CC BY 4.0 — like the whole repository ([LICENSE.md](../../LICENSE.md)).
