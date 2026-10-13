# Harness profiles — the top 20 and the rest of the field

**As of 11 October 2026.** GitHub numbers (stars, releases) pulled from the API on that day.
All facts come from documentation, code, release notes and issues — sources are given with each profile
and in [SOURCES.md](SOURCES.md). **I have not tested any of these harnesses on my machine** — this is a review
of documentation, not a measurement. Ranking and weights: [README.md](README.md#how-i-computed-the-ranking).

Score legend: A — multiple agents and hybrid (25%), B — quality of local model support (20%),
C — coverage of the five use cases (20%), D — maturity (15%), E — value for learning (10%),
F — security and control (10%). Each criterion 1–5, score 0–100.

---

## Table of contents

- [Seven pitfalls common to all](#seven-pitfalls-common-to-all)
- Profiles: [1. LangGraph](#1-langgraph) · [2. Goose](#2-goose) · [3. OpenHands](#3-openhands) ·
  [4. Hermes Agent](#4-hermes-agent) · [5. Pydantic AI](#5-pydantic-ai) · [6. Deep Agents](#6-deep-agents) ·
  [7. Strands Agents](#7-strands-agents) · [8. OpenCode](#8-opencode) · [9. DeerFlow](#9-deerflow) ·
  [10. ZeroClaw](#10-zeroclaw) · [11. Microsoft Agent Framework](#11-microsoft-agent-framework) ·
  [12. DeepSeek Harness](#12-deepseek-harness) · [13. Pi](#13-pi) · [14. gptme](#14-gptme) ·
  [15. Moltis](#15-moltis) · [16. QwenPaw](#16-qwenpaw) · [17. OpenAI Agents SDK](#17-openai-agents-sdk) ·
  [18. n8n](#18-n8n) · [19. LibreChat](#19-librechat) · [20. Kilo Code](#20-kilo-code)
- [Remaining candidates (ranks 21–64)](#remaining-candidates-ranks-2164)
- [Excluded at entry](#excluded-at-entry)
- [Outside the ranking](#outside-the-ranking)

---

## Seven pitfalls common to all

The same problems come back in almost every harness connected to llama.cpp / llama-swap. Check them
before you conclude that "harness X does not work with a local model".

| # | Pitfall | Symptom | What to do |
|---|---|---|---|
| H1 | **Responses API instead of Chat Completions.** More and more tools call `/v1/responses` by default (OpenAI Agents SDK, Microsoft Agent Framework — `OpenAIChatClient`, n8n — a switch in the node, Windmill — the OpenAI provider). Since February 2026 Codex CLI supports **only** the Responses API. | 400/404 error, "type must be output_text" | pick the `chat_completions` mode / the "OpenAI-compatible" provider; for Codex CLI — a different harness |
| H2 | **DeepSeek's `reasoning_content` in tool calls.** In thinking mode DeepSeek V4 requires the reasoning content to be sent back in turns with tools. It was dropped by LangChain (#40219, open), Microsoft Agent Framework (fixed in September 2026), Pydantic AI (fixed in v2). | 400 error on the second turn with a tool | a current framework version; in LibreChat `includeReasoningContent: true`; or turn thinking off for executors |
| H3 | **Context window guessed from the model name.** The harness takes the limit from the cloud catalogue or defaults to 128K/200K instead of asking the server (with llama.cpp: QwenPaw #7979, LibreChat #14228; with a custom OpenAI-compatible provider: Goose #12048; with Ollama: Strands #4620; default 128K in Hermes). | compaction does not fire or fires too early, truncated answers | set `131072` (your slot) explicitly in the model configuration |
| H4 | **A changing start of the prompt kills the prompt cache.** A timestamp or a random tool order in the system prompt invalidates the server cache on every turn (with llama.cpp: OpenClaw, LibreChat #16877; with Ollama and other local servers: nanobot #4867). | every turn reads the whole context from scratch — at about 1,200 tok/s of prompt reading that is tens of seconds per turn | a stable prefix: the date in the user message, not in the system prompt; check `cache_n` in the llama-server logs |
| H5 | **Too many tools at once.** Local models lose quality with long tool lists and MCP schemas. | picking the wrong tool, loops | 5–15 tools per executor; 2–3 MCP servers, not ten |
| H6 | **No per-endpoint concurrency limit.** You have 4 slots. Almost all frameworks limit parallelism within a single run, not globally (exception: Pydantic AI). | the queue in llama-server grows, timeouts | one limit of 4 in one place, with a queue: a gateway (Bifrost), `ConcurrencyLimiter` or a task queue. Note: `concurrencyLimit` in llama-swap does not queue — an excess request gets 429 immediately |
| H7 | **Tool schemas that the llama.cpp grammar does not accept.** E.g. `pattern` without `^…$` (Kilo #12773, llama-server), schema regressions in Qwen Code (#10435 and subsequent). A related case with Ollama: the tool syntax change in Cline 4.1 (#13008). | "Unable to generate parser for this template" (Kilo #12408) | pin harness versions, test after updating (promptfoo — see [02-BUILDING-BLOCKS.md](02-BUILDING-BLOCKS.md)) |

---

## 1. LangGraph

**Category:** Python framework (state graph) · **License:** MIT · ⭐ 43.1k · **Release:** langgraph 1.2.14 (6 October 2026) ·
**Score: 86** (A5 B4 C4 D5 E3 F4)

**What it is.** A runtime in which an agent is a graph: nodes are functions or agents, edges
are the transition logic, and every step can be saved (checkpoint), interrupted, resumed and replayed. `create_agent`
from LangChain v1 and Deep Agents (no. 6) are built on it.

**Advantage.** The most mature persistence model in Python: per-thread checkpoints, three write modes
(`exit` / `async` / `sync`), time travel, `interrupt()` for a human in the loop that survives a process
restart, `Send` branching and subgraphs.

**Local model.**
```python
from langchain.chat_models import init_chat_model
local = init_chat_model("deepseek-v4-flash", model_provider="openai",
                        base_url="http://localhost:8080/v1", api_key="none")   # the address of your llama-swap
```
llama-server must run with a template that supports tools (`--jinja`).

**Multiple agents and hybrid.** The documentation describes five patterns: subagents as tools, handoffs,
skills, router, custom graph. Every node has its own model, so a planner on
`anthropic:claude-opus-5-5` and executors on llama-swap is an ordinary configuration. `max_concurrency` limits
parallelism within a single run — a global limit of 4 requests you have to add yourself (pitfall H6).

**Voice and vision.** No real-time voice; the official guide proposes a "sandwich"
STT → agent → TTS. Images pass as multimodal blocks to a model with vision.

**Security.** No built-in sandbox (Deep Agents provide one). Middleware with model-call and tool-call limits,
PII detection and a human in the loop; open issues about missing hooks before tool execution
(#8817, #8818).

**Weaknesses.** The LangChain layers are where local models break: dropping
`reasoning_content` (#40219, open), tool arguments split across the stream (#35514). A server with cron
in the self-hosted version is a paid LangSmith add-on. `langgraph-supervisor` was archived in 2026 —
in its place the "supervisor via tool calls" pattern.

**What to steal.** Checkpoints per `thread_id` with selectable durability; `interrupt()` + `Command(resume=…)`
as the mechanism for asking a human; a small vocabulary of human decisions (approve / edit / reject / reply);
the list of built-in middleware (retry, model fallback, call limits, PII detection) as a checklist of
what every harness must have.

**Sources:** [repository](https://github.com/langchain-ai/langgraph) ·
[models](https://docs.langchain.com/oss/python/langchain/models) ·
[durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution) ·
[multi-agent patterns](https://docs.langchain.com/oss/python/langchain/multi-agent) ·
[#40219](https://github.com/langchain-ai/langchain/issues/40219)

---

## 2. Goose

**Category:** general-purpose agent (CLI, desktop, server) · **License:** Apache-2.0 · ⭐ 55.1k ·
**Release:** v1.54.0 (8 October 2026) · **Score: 84** (A5 B4 C4 D5 E3 F3)

**What it is.** An agent in Rust created by Block, since 7 April 2026 under the Agentic AI Foundation (Linux Foundation),
alongside MCP and AGENTS.md. It has a CLI, a desktop app and an ACP server; the repository was moved to `aaif-goose/goose`.

**Advantage.** The broadest "beyond coding" set: YAML recipes (*recipes*) as the unit of repeatable work,
a built-in cron scheduler, subagents with their own provider and model, a *tool shim* for models that call
tools poorly (experimental: a separate translator model runs by default through Ollama or through Goose's built-in llama.cpp,
so you cannot use it with llama-swap alone — DeepSeek has native tool calls anyway), a Telegram gateway, voice dictation (also with a local Whisper), Adversary mode — a separate model reviews
every tool call. Neutral governance by the foundation.

**Local model.** A provider file in `~/.config/goose/custom_providers/` with `"engine": "openai"`,
`"base_url": "http://localhost:8080/v1/chat/completions"` and `context_limit` per model. The documentation honestly
says that Goose "works best with Claude models". Known bugs: reasoning models return empty content
because `max_tokens` is shared between reasoning and the answer (#11142); the context window is ignored (#12048).

**Multiple agents and hybrid.** `GOOSE_SUBAGENT_PROVIDER` / `GOOSE_SUBAGENT_MODEL` set the executors' model,
and a recipe can override it (`settings.goose_provider` / `goose_model`). The main session on Anthropic, executors
on llama-swap — supported. Subagents work only in autonomous mode.

**Voice and vision.** Dictation in the desktop app (cloud providers or a local Whisper), no speech synthesis.
Images when the model has vision; for a custom endpoint you have to enable `supports_vision` per model (#11998).

**Security.** `GOOSE_MODE` modes (auto, approve, smart_approve, chat), per-tool permissions,
prompt injection detection, Adversary mode, hooks before a tool call.

**Scheduling and headless mode.** `goose schedule add --cron … --recipe-source …`, `goose run -t "…"`,
`goose serve` (ACP server with TLS).

**Weaknesses.** The experimental macOS sandbox was removed — tools run with your permissions.
Adversary mode is *fail-open* (when the reviewer fails, the action goes through). The architecture is being rebuilt (2.0, ACP).

**What to steal.** A recipe as a unit of work with parameters, extensions and a model; the *tool shim* — a cheap
model translates textual tool calls into structured ones; an LLM reviewer gating calls; pairing
Telegram with a one-time code.

**Sources:** [environment variables](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/environment-variables.md) ·
[subagents](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/context-engineering/subagents.mdx) ·
[tool shim](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/tool-shim.md) ·
[Adversary](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/security/adversary-mode.md) ·
[move to AAIF](https://github.com/aaif-goose/goose/blob/main/documentation/blog/2026-04-07-goose-moves-to-aaif/index.md)

---

## 3. OpenHands

**Category:** coding agent platform + SDK · **License:** MIT · ⭐ 90.5k · **Release:** v1.26.0 (8 October 2026) ·
**Score: 84** (A5 B4 C3 D5 E3 F5)

**What it is.** A platform whose "Agent Canvas" front end (2026) runs OpenHands — or Claude Code, Codex, Pi,
OpenCode via ACP — locally, in Docker, on a VM or in Kubernetes. Underneath are the Software Agent SDK (Python)
and the Agent Server (REST / WebSocket).

**Advantage.** The most complete stack to embed in your own application: an SDK + a server with OpenAPI, a container for every
conversation, subagents from Markdown files with a `model:` field, model routers, OpenTelemetry, automations (cron, webhook,
events) and an OpenAI-compatible gateway that exposes **the whole agent as a "model"**.

**Local model.** Via LiteLLM: model `openai/deepseek-v4-flash` + the llama-swap `base_url`. In 2026 two bugs important to you
were fixed: a global lock serialized all LLM calls across conversations — wasting
parallel slots (#16459), and a malformed tool call in the history blocked llama-server (sdk#2887).

**Multiple agents and hybrid.** Agents from files have `model: inherit` or a named LLM profile — an orchestrator on Claude,
subagents on a local profile. `route_task_to_model` switches the profile mid-conversation, MultimodalRouter sends
images to a model with vision and text to a cheaper one.

**Voice and vision.** Canvas v1.25.0 (6 October 2026) added voice input: recognition in the browser or any
OpenAI-compatible transcription endpoint (e.g. a local Whisper). Images as input and browser screenshots.

**Security.** A container per conversation, VM / K8s backends, confirmation policies and a risk analyzer.
Note: the headless CLI mode always approves everything, and an install without Docker has full disk access.

**Weaknesses.** Heavy and fast-changing (V0 → SDK V1 → Agent Canvas; the standalone CLI pushed aside).

**What to steal.** An agent as a "model" behind an OpenAI gateway — any client, including a voice platform, can call
the whole agent; subagents in Markdown with `model: inherit | <profile>`; a container per conversation; an automation
spec (trigger, schedule, model, notifications) as a JSON file in the repository.

**Sources:** [local models](https://docs.openhands.dev/openhands/usage/llms/local-llms) ·
[file-based agents](https://github.com/OpenHands/docs/blob/main/sdk/guides/agent-file-based.mdx) ·
[OpenAI gateway](https://github.com/OpenHands/docs/blob/main/sdk/guides/agent-server/openai-gateway.mdx) ·
[#16459](https://github.com/OpenHands/OpenHands/issues/16459)

---

## 4. Hermes Agent

**Category:** always-on personal agent · **License:** MIT · ⭐ 252.7k · **Release:** v0.21.6 (8 October 2026) ·
**Score: 81** (A5 B4 C4 D4 E2 F4)

**What it is.** An agent from Nous Research with a learning loop: it writes and improves its own skills (*skills*), maintains memory
and searches past sessions. It runs on a local terminal, in Docker, over SSH or in a cloud sandbox;
it replies from 25+ messengers (Telegram, Signal, WhatsApp, Discord, email, Matrix and others).

**Advantage.** The "frontier planner, cheap executors" pattern is built into the configuration; the strongest cron in its
category (agent-less watchdogs, continuity between runs, incident deduplication); voice in the CLI and messengers.

**Local model.**
```yaml
model:
  provider: custom
  base_url: http://localhost:8080/v1
  default: deepseek-v4-flash
  context_length: 131072      # set explicitly — autodetection falls back to 128K
```
The built-in AMD runtime picks Vulkan — on the R9700 stay with your own llama-swap.

**Multiple agents and hybrid.** The main model on Anthropic (Opus 5.5 is in the catalogue), executors via
`delegation: {provider, model, base_url}`. `delegation.max_concurrent_children` defaults to 10 — reduce it to 4.
Side tasks (vision, compression, background review) have separate models; redirect the background review,
otherwise it doubles the load on the slots.

**Voice and vision.** Push-to-talk in the CLI, voice replies on Telegram and Discord. STT: local faster-whisper
(language: `stt.local.language`). TTS: by default Edge TTS — a free Microsoft cloud service, with Polish voices;
plus ElevenLabs, OpenAI or a local NeuTTS (Polish not confirmed in the documentation). That is: speech recognition
local, synthesis in the cloud by default. Since v0.20 streaming with mid-sentence interruption. Images go natively to a model with vision; for the text-only DeepSeek the description is made by
the `vision_analyze` tool with a separate vision model.

**Security.** "Smart approvals" (an auxiliary LLM judges flagged commands) plus a hard deny list,
rootless Docker, stripping secrets from the tool environment, pairing conversations with a one-time code.

**Weaknesses.** An enormous pace of change (about 2,100 PRs between two consecutive versions) — pin versions.
The repository has about 18k files, so it is unsuitable for learning. Corruption of the state database required
a separate repair release. A paid Nous portal promoted during installation.

**What to steal.** Delegation with `output_schema` and one repair turn; hang detection by lack of progress,
not by a clock; a frozen memory snapshot per session (stable prefix = a working prompt cache); "agent-less"
cron watchdogs that alert only on a non-empty result; a Whisper hallucination filter.

**Sources:** [delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation) ·
[providers](https://hermes-agent.nousresearch.com/docs/integrations/providers) ·
[voice](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode) ·
[cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) ·
[releases](https://github.com/NousResearch/hermes-agent/releases)

---

## 5. Pydantic AI

**Category:** Python framework (typed) · **License:** MIT · ⭐ 20.5k · **Release:** v2.55.0 (9 October 2026) ·
**Score: 81** (A5 B4 C4 D4 E3 F3)

**What it is.** A framework from the creators of Pydantic. An agent runs a validated loop of tools and results; since v2 (23 June 2026)
"capabilities" combine tools, hooks and settings into modules: subagents, planning, memory, compaction, code mode,
real-time voice, durable execution.

**Advantage.** The best structured output (tool / native / prompted modes with validation and retries) and — as the
only framework checked — **a shared concurrency limiter per model**. That is exactly your 4 slots.
Durable execution via Temporal, DBOS, Prefect or Restate.

**Local model and the 4-slot limit.**
```python
from pydantic_ai import Agent, ConcurrencyLimitedModel, ConcurrencyLimiter
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

local = OpenAIProvider(base_url="http://localhost:8080/v1", api_key="none")
pool = ConcurrencyLimiter(max_running=4, name="llama-swap")          # 4 slots, shared across models
ds = ConcurrencyLimitedModel(OpenAIChatModel("deepseek-v4-flash", provider=local), limiter=pool)
worker = Agent(ds, name="worker")
planner = Agent("anthropic:claude-opus-5-5")
```
Note: an agent nested in a tool also takes a slot — size the pool for both parent and child.

**Multiple agents and hybrid.** Delegation via tools, handoffs in code, graphs (`pydantic_graph`);
the subagents module gives the orchestrator a menu of models (`SubAgents(models={…})`), budgets, timeouts and `max_depth`.

**Voice and vision.** `agent.realtime(...)` works only with cloud models (OpenAI Realtime, Gemini Live, xAI);
locally what remains is the STT → agent → TTS cascade that you assemble yourself. Images and documents as input.

**Security.** Tools requiring approval (*deferred tools*), usage limits and per-delegation budgets.
The shell in the Coder module is unrestricted — you add the sandbox yourself.

**Weaknesses.** Heuristics for OpenAI-compatible servers (enabling thinking based on the first character of the model name,
#4878); very fast releases and a breaking v2 migration; huge core files.

**What to steal.** A model wrapper enforcing a named, shared pool — with the queue depth visible
in traces; output modes chosen by model profile; per-delegation budgets with soft and hard failure.

**Sources:** [PR #4149 — concurrency limit](https://github.com/pydantic/pydantic-ai/pull/4149) ·
[OpenAI-compatible APIs](https://pydantic.dev/docs/ai/models/compatible-apis/index.md) ·
[subagents](https://pydantic.dev/docs/ai/harness/subagents/index.md) ·
[#4878](https://github.com/pydantic/pydantic-ai/issues/4878)

---

## 6. Deep Agents

**Category:** harness on LangGraph (Claude Code style) · **License:** MIT · ⭐ 30.1k ·
**Release:** deepagents 0.7.23 (7 October 2026) · **Score: 81** (A5 B4 C3 D4 E4 F4)

**What it is.** A "batteries-included agent harness" from LangChain: `create_deep_agent()` gives planning (a todo list),
a file system (virtual or real), subagents with isolated context, compaction and offloading of large results
to files, skills, memory in AGENTS.md and a human in the loop. Plus the terminal agent `dcode`.
The successor to Open Deep Research, archived (August 2026).

**Advantage.** A ready recipe for a "deep agent" built on LangGraph's durability, with swappable backends
(state, local file system, LangGraph store, remote sandboxes).

**Local model.** Any LangChain model, e.g. `ChatOpenAI(base_url="http://localhost:8080/v1", api_key="none")`.
It inherits LangChain's bugs with local models (pitfall H2).

**Multiple agents and hybrid.** The main agent `model=ChatAnthropic(...)`, subagents
`{"name": "researcher", "model": ChatOpenAI(base_url=...)}`. Several `task` calls in one turn mean parallelism;
asynchronous subagents (start / check / update / cancel) run in the background on the server.

**Voice and vision.** No voice; images as LangChain multimodal messages.

**Security.** Sandbox backends (Modal, Runloop, your own), file permission rules,
`interrupt_on` per tool.

**Weaknesses.** 0.x versions with dozens of releases; no concurrency limit for parallel `task` calls; no voice.

**What to steal.** The file system as the agent's notepad and offloading large tool results to files instead of
the context; the `task` tool with a fresh context; a toolset for controlling background subagents.

**Sources:** [overview](https://docs.langchain.com/oss/python/deepagents/overview) ·
[subagents](https://docs.langchain.com/oss/python/deepagents/subagents) ·
[async subagents](https://docs.langchain.com/oss/python/deepagents/async-subagents) ·
[repository](https://github.com/langchain-ai/deepagents)

---

## 7. Strands Agents

**Category:** Python/TS SDK + ready-made harness (AWS) · **License:** Apache-2.0 · ⭐ 8.8k ·
**Release:** harness 0.2.0 (8 October 2026) · **Score: 80** (A4 B5 C4 D4 E3 F3)

**What it is.** An SDK from AWS in which the model runs a simple loop (tools, hooks, interrupts, steering, sessions,
multi-agent patterns), plus `create_harness()` — an assembled agent with default tools (shell, files, web,
todo list, subagents, checkpoints, memory). The repository was renamed to `harness-sdk`.

**Advantage.** A **native `LlamaCppModel` provider** that uses llama.cpp features (grammars, advanced
sampling, `cache_prompt`) instead of treating the server as "just another OpenAI". Plus model routing (classifier,
fallback) and OpenTelemetry by default.

**Local model.** `LlamaCppModel(base_url="http://localhost:8080", model_id="deepseek-v4-flash")`.
Known: models without an entry in the context window table get 200k by default (#4620, pitfall H3).

**Multiple agents and hybrid.** `Agent(model=AnthropicModel(model_id="claude-opus-5-5"), tools=[worker_tool])`
orchestrates executors on `LlamaCppModel`; patterns agents-as-tools, Swarm, Graph, A2A.

**Voice and vision.** `BidiAgent` (GA 5 October 2026) — cloud models only (Nova Sonic, OpenAI Realtime, Gemini Live).
Images as content blocks.

**Security.** A `sandbox` module, guardrails, interventions and steering (*steering*) in the loop.

**Weaknesses.** Defaults geared to AWS / Bedrock; a concurrency limit in Python only in a PR (#3156);
about 40 releases in 2026.

**What to steal.** A provider that uses llama.cpp grammars and `cache_prompt`; cheap / expensive routing
by a classifier; tracing every loop decision by default.

**Sources:** [llama.cpp provider](https://github.com/strands-agents/harness-sdk/blob/main/strands-py/src/strands/models/llamacpp.py) ·
[harness](https://github.com/strands-agents/harness-sdk/blob/main/site/src/content/docs/user-guide/harness/index.mdx) ·
[multi-agent patterns](https://github.com/strands-agents/harness-sdk/tree/main/strands-py/src/strands/multiagent) ·
[#4620](https://github.com/strands-agents/harness-sdk/issues/4620)

---

## 8. OpenCode

**Category:** coding agent (TUI, desktop, HTTP server) · **License:** MIT · ⭐ 212.6k ·
**Release:** v1.19.0 (11 October 2026) · **Score: 80** (A5 B4 C3 D5 E3 F3)

**What it is.** A coding agent from the former SST team (Anomaly Innovations); the repository was moved from `sst/opencode`
to `anomalyco/opencode`. The TUI is just one of the clients of the `opencode serve` server.

**Advantage.** A client–server architecture (OpenAPI 3.1 + SSE events, a JS SDK) and first-class agents and
subagents with their own model and permissions. Connecting llama-server is simple and described in the documentation.

**Local model** (`opencode.json`):
```json
"provider": {
  "llama": {
    "npm": "@ai-sdk/openai-compatible",
    "options": { "baseURL": "http://localhost:8080/v1" },
    "models": { "deepseek-v4-flash": { "limit": { "context": 131072, "output": 16384 } } }
  }
}
```
Known bug: the bundled library aborts the turn when the stream carries `function.name: null` (#52462).

**Multiple agents and hybrid.** A `plan` / `build` agent on `anthropic/claude-opus-5-5`, subagents on
`llama/deepseek-v4-flash` — the model is set per agent. Since 9 January 2026 Anthropic blocks logging in with a Pro/Max
subscription in third-party tools — an API key is needed.

**Voice and vision.** No voice of its own (request #33300; community plugins only). Image attachments are
scaled before sending and work with a model that has vision.

**Security.** `allow` / `ask` / `deny` rules with patterns, e.g.
`"bash": {"kubectl get *": "allow", "rm *": "deny"}`. No system sandbox; bypasses of the
`external_directory` rule have been reported.

**Weaknesses.** Fast changes and the breaking V2 server API (bad for embedding right now); memory leaks in
server mode; no voice.

**What to steal.** A headless server with OpenAPI as the core, and every UI as a client; agents as Markdown files
with `model` / `permission` / `steps`; `permission.task` — which subagents may be called; a hook rewriting tool
descriptions per model (a workaround for llama.cpp grammar problems).

**Sources:** [providers](https://opencode.ai/docs/providers/) · [agents](https://opencode.ai/docs/agents/) ·
[server](https://opencode.ai/docs/server/) · [#52462](https://github.com/anomalyco/opencode/issues/52462)

---

## 9. DeerFlow

**Category:** "super-agent" for long tasks (research, code, content) · **License:** MIT · ⭐ 83.7k ·
**Release:** v2.1.0 (24 September 2026) · **Score: 79** (A5 B4 C3 D4 E3 F4)

**What it is.** A ByteDance platform on LangGraph: a lead agent delegates to subagents running
in sandboxes (local, Docker, Kubernetes); long-term memory, skills, MCP, scheduled tasks,
messenger channels. Version 2.0 (28 February 2026) is a rewrite from scratch.

**Advantage.** A deep research pedigree plus a mature multi-agent runtime; an explicit model override per subagent,
described in the sample configuration plainly as "local model to save money".

**Local model** (`config.yaml`):
```yaml
models:
  - name: deepseek-local
    use: langchain_openai:ChatOpenAI
    model: deepseek-v4-flash
    api_key: no-key
    base_url: http://localhost:8080/v1
    request_timeout: 600.0
    supports_vision: false
```

**Multiple agents and hybrid.** The lead agent on `langchain_anthropic:ChatAnthropic`, subagents with
`model: deepseek-local`. Limits: the number of subagents per run and token ceilings.

**Voice and vision.** No voice in version 2.0. `supports_vision: true` enables the `view_image` tool;
the Playwright browser takes screenshots.

**Security.** A local sandbox, Docker or Kubernetes; listening on loopback only by default; the README
warns that a gateway administrator is in practice code execution.

**Scheduling.** `once` / `cron` / `interval` tasks with a goal, a stop condition and a run limit;
Telegram (long polling) and Slack.

**Weaknesses.** Difficult deployment (Postgres and Redis with multiple workers); on local models slow and prone
to loops (#1055); channels geared toward Chinese platforms; a history of sandbox escapes; no voice.

**What to steal.** An isolated or "snapshot" context passed to a subagent; token ceilings per subagent;
scheduled tasks with goal evaluation and a stop condition; messengers via long polling, without a public webhook.

**Sources:** [repository](https://github.com/bytedance/deer-flow) ·
[config.example.yaml](https://github.com/bytedance/deer-flow/blob/main/config.example.yaml) ·
[#1055](https://github.com/bytedance/deer-flow/issues/1055)

---

## 10. ZeroClaw

**Category:** personal agent (a single Rust binary) · **License:** MIT or Apache-2.0 · ⭐ 33.0k ·
**Release:** v0.8.5 (5 September 2026) · **Score: 78** (A4 B4 C4 D4 E2 F5)

**What it is.** An agent runtime in a single binary: 20+ LLM providers, 30+ channels, shell, browser, HTTP and MCP tools
under a security policy. From the "Claw" family (alternatives to OpenClaw).
Beware of fakes — only `zeroclaw-labs/zeroclaw` is official.

**Advantage.** The deepest configurable security model: risk profiles, autonomy levels
ReadOnly / Supervised / Full (default `supervised`), automatic sandbox selection (Landlock → Bubblewrap →
Firejail → Docker), HMAC-signed tool-call confirmations, a procedure engine (SOP) with approval gates.

**Local model.** A `[providers.models.llamacpp.<alias>]` section with `uri`, `chat_template_kwargs`, `vision`.
Set `native_tools = true` — by default local endpoints get tools in text mode.

**Multiple agents and hybrid.** Every `[agents.<alias>]` has its own provider profile, so a coordinator on Claude can
`delegate` to agents on the `llamacpp` slot. Delegation is forbidden by default — you have to enable it deliberately.

**Voice and vision.** Piper as local TTS, phone calls via SIP operators. Images for a text-only model
redirected to a separate vision provider.

**Security.** `supervised` by default: medium-risk actions require approval, high-risk ones are
blocked; quorum approvals; YOLO mode only on development machines.

**Weaknesses.** High configuration complexity (four TOML sections), many open issues, context bloat
from repeated reasoning (#10396).

**What to steal.** Risk profiles separated from agents and delegation forbidden by default; shared action
and cost budgets that a subagent cannot bypass; redirecting images to a dedicated model.

**Sources:** [provider configuration](https://github.com/zeroclaw-labs/zeroclaw/blob/master/docs/book/src/providers/configuration.md) ·
[delegation](https://github.com/zeroclaw-labs/zeroclaw/blob/master/docs/book/src/agents/delegation.md) ·
[multiple models](https://github.com/zeroclaw-labs/zeroclaw/blob/master/docs/book/src/getting-started/multi-model-setup.md)

---

## 11. Microsoft Agent Framework

**Category:** Python / .NET / Go SDK with a workflow engine · **License:** MIT · ⭐ 14.1k ·
**Release:** python-1.21.0 (8 October 2026) · **Score: 77** (A5 B3 C3 D4 E3 F5)

**What it is.** The successor to AutoGen and Semantic Kernel (AutoGen is in maintenance mode; Python 1.0 GA 2 April 2026).
Agents, chat clients for many providers, middleware, sessions and a typed `WorkflowBuilder` with a checkpoint
after every step.

**Advantage.** A stable 1.x API with a long-support promise; ready orchestrations Sequential, Concurrent,
Handoff, Group Chat and Magentic (a manager coordinating specialists); the strongest security story:
FIDES information-flow labels against prompt injection and CodeAct in Hyperlight micro-VMs.

**Local model.**
`OpenAIChatCompletionClient(model="deepseek-v4-flash", base_url="http://localhost:8080/v1", api_key="none")`.
Pitfall H1: in Python `OpenAIChatClient` now means the Responses API. Dropping `reasoning_content` was fixed
only in September 2026 (#8382).

**Multiple agents and hybrid.** A Magentic manager or a planner on `AnthropicClient`, executors on a local
client — every agent has its own client.

**Voice and vision.** Audio input to models that support it, but no real-time voice agents
in Python; images as message content.

**Security.** FIDES (confidentiality and integrity labels, `SecureMCPToolProxy`) and CodeAct in Hyperlight
micro-VMs. FIDES does not work inside nested CodeAct calls (#9251).

**Weaknesses.** Examples geared toward Azure / Foundry; breaking changes even after GA; no real-time voice
in Python.

**What to steal.** A checkpoint after every step with a safe deserializer (an allow-list of types);
`response_parser` / `message_preparer` hooks for provider quirks — ideal for llama.cpp reasoning fields;
a manager with a task ledger (Magentic).

**Sources:** [OpenAI provider](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/openai) ·
[checkpoints](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints) ·
[orchestrations](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/) ·
[#8382](https://github.com/microsoft/agent-framework/issues/8382)

---

## 12. DeepSeek Harness

**Category:** harness from DeepSeek (Web UI, headless mode, SDK) · **License:** MIT · ⭐ 247.3k ·
**Release:** dsh-v0.2.1-alpha.2 (9 October 2026, pre-release) · **Score: 76** (A5 B4 C3 D3 E3 F4)

**What it is.** The official DeepSeek harness (published 13 August 2026) built from Cordis plugins: model adapters,
tools, sandbox, subagents, scheduler, UI, and even the agent loop itself are swappable plugins assembled
into "profiles". It takes its LLM layer from Pi (no. 13).

**Advantage.** Tuning for DeepSeek V4 from the model's maker (thinking format, reasoning effort) and subagents
that can be **other harnesses**: Claude Code, Codex, any ACP agent or another dsh instance.

**Local model.** Settings → Models → "Custom model API": base URL and the `openai-completions` protocol. For llama-server
usually `supportsDeveloperRole: false` and `maxTokensField: max_tokens`, and for DeepSeek V4 `compat.thinkingFormat: deepseek`.
Known bug: WebP images break the llama.cpp session (#7406).

**Multiple agents and hybrid.** Both ways: a local DeepSeek as parent delegates to a Claude Code child
(with a fixed `permissionMode`), or a parent on Anthropic and dsh children on a local model. `maxActiveSubagents`
defaults to 8 — set it to 4. It is not a ready "Claude plans, local executes" preset — you assemble the layout
from plugins in a profile.

**Voice and vision.** Experimental STT; the local SenseVoice does not support Polish. Images enabled per model
(`input: [text, image]`).

**Security.** The default sandbox is `read-only`, permission sets (sandbox + approval policy),
a sanitized environment for child processes.

**Weaknesses.** A pre-release version — the README warns in capital letters about breaking changes.
No Issues tab (bugs go to Discussions); poor configuration documentation outside the UI.

**What to steal.** A `compat` profile per model (developer role, the `max_tokens` field name, thinking format)
instead of guessing from the URL; a provider-subagent wrapping other harnesses; a safe default read-only
mode.

**Sources:** [README](https://github.com/deepseek-ai/deepseek-harness/blob/main/README.md) ·
[providers](https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/user/guide/providers.md) ·
[SAFETY.md](https://github.com/deepseek-ai/deepseek-harness/blob/main/SAFETY.md)

---

## 13. Pi

**Category:** minimal coding harness + TS libraries · **License:** MIT · ⭐ 114.2k ·
**Release:** v1.1.0 (7 October 2026) · **Score: 76** (A4 B5 C3 D4 E5 F1)

**What it is.** "A minimal, extensible harness you can make your own" (Mario Zechner, since 2026 at Earendil):
the terminal agent `pi` and the libraries it is built on (`pi-ai` — the multi-provider layer, `pi-agent-core`,
`pi-durable`). Its layers are used by other projects, e.g. DeepSeek Harness.

**Advantage.** A small core with an exceptionally deep extension API: custom tools, permission gates, redirecting
tools over SSH or into a micro-VM, "virtual models" routing each request to a different physical model.
First-class llama.cpp support and four levels of embedding: TUI, `--print` / `--mode json`, `--mode rpc`, SDK.

**Local model.** For llama-swap use the generic path `~/.pi/agent/models.json` (`baseUrl`,
`"api": "openai-completions"`) — the built-in `/llama` assumes llama-server in router mode.

**Multiple agents and hybrid.** Subagents (an official example extension) in separate processes, described in Markdown
with a `model:` field — one on Anthropic, another locally. Virtual models: easy turns locally, hard ones to Claude,
with per-model cost in the session summary.

**Voice and vision.** No voice. Images pasted into the terminal, `@image` in the prompt, the `read` tool reads images.

**Security.** **No** approvals and no sandbox — by design. Run it in a container or a sandbox
(see [02-BUILDING-BLOCKS.md](02-BUILDING-BLOCKS.md#sandboxes)).

**Weaknesses.** Subagents are an example, not the core; issues from new contributors are closed automatically.

**What to steal.** One core, many embedding modes; virtual models that record the physical model with every
message; *codemode* — the model writes JS that calls tools in parallel and filters results before they reach the context
(saves tokens on a slow local model). Alongside mini-swe-agent — the best code to learn from on the whole list.

**Sources:** [agent README](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md) ·
[llama.cpp](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/llama-cpp.md) ·
[models](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md) ·
[security](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md)

---

## 14. gptme

**Category:** terminal agent + autonomous agents · **License:** MIT · ⭐ 4.4k ·
**Release:** v0.34.0 (18 September 2026) · **Score: 75** (A4 B4 C4 D3 E4 F3)

**What it is.** "A personal AI agent that runs anywhere there is a terminal" — developed since 2023, local
first: shell, Python, files, browser, vision, subagents, MCP.

**Advantage.** A swappable tool format: Markdown code blocks by default, plus XML and native — so it works
where llama.cpp's tool-call parsing fails. `gptme service init` generates a systemd service and timer
for an agent that runs continuously.

**Local model.** `OPENAI_BASE_URL=http://localhost:8080/v1 gptme -m local/deepseek-v4-flash`;
when it loops: `--tool-format xml`.

**Multiple agents and hybrid.** A parent on `anthropic/claude-…`, subagents on `local/…`; a subagent can also be
another harness via ACP (e.g. Claude Code). Isolation in a git worktree.

**Voice and vision.** Real-time conversation only through cloud APIs (OpenAI, xAI); local TTS Kokoro
(no Polish). Vision, screenshots, desktop control, the Playwright browser.

**Security.** Confirmations on by default; a three-tier shell policy: read-only commands
pass on their own, a deny list (e.g. `git push -f`, `| bash`) blocks, the rest asks. The system sandbox
is immature.

**Weaknesses.** Heuristic Markdown parsing; a small community; a lot of the changes are written by its own autonomous
agent, so the pace and code churn are high.

**What to steal.** The tool format as a parameter, with a model × format ranking; three subagent isolation modes
(thread, subprocess, ACP); a systemd service skeleton with a prompt and a journal for a persistent agent.

**Sources:** [providers](https://gptme.org/docs/providers.html) ·
[tool formats](https://github.com/gptme/gptme/blob/master/docs/tool-formats.rst) ·
[subagents](https://github.com/gptme/gptme/blob/master/docs/tools/subagent.rst)

---

## 15. Moltis

**Category:** personal agent server (a single Rust binary) · **License:** MIT · ⭐ 2.9k ·
**Release:** 20260913.02 (14 September 2026) · **Score: 74** (A4 B4 C4 D2 E3 F5)

**What it is.** A single binary with a web UI, a PWA phone app and a messenger gateway: agent loop,
memory, voice, scheduler, MCP and sandboxes. It imports OpenClaw configuration and skills.

**Advantage.** The most complete "single file": built-in local STT and TTS, a choice of sandbox (Podman, Docker,
WASM, restricted host), Prometheus / OTLP / Langfuse, signed releases and no plugin marketplace
("nothing to get attacked through").

**Local model.** `[providers.custom-llamaswap]` with `base_url = "http://localhost:8080/v1"` and
`tool_mode = "auto" | "native" | "text"`. The built-in GGUF backend has no ROCm path — use llama-swap.

**Multiple agents and hybrid.** A coordinator on `anthropic/…`, executor presets with
`model = "custom-llamaswap/deepseek-v4-flash"` (the exact name format for a custom provider is unverified —
check the names in `/v1/models`), their own tools, sandbox and memory scope.
The `coordinator` preset has `delegate_only = true`. The heartbeat can run on a separate, local model.

**Voice and vision.** The strongest local stack in the category: STT locally (Whisper, Sherpa-ONNX, Voxtral), TTS
locally (Piper with Polish voices, Coqui), replies as voice notes on Telegram. Images via providers
with vision; screenshots and a browser.

**Security.** `backend = "auto"` picks the sandbox (Podman → Docker → restricted host);
`approval_mode`, approval of writes and edits, hooks before a tool call, SSRF protection.

**Weaknesses.** **Practically a single maintainer** (about 3.6k commits from the lead versus <100 from the next person);
alpha status; concerns about self-modifying skills.

**What to steal.** Presets combining model, tools, sandbox and memory scope + a coordinator that only
delegates — a ready template for "Opus plans, local executes"; timestamps kept out of the system prompt (pitfall H4);
an automatic checkpoint before a memory or skill change.

**Sources:** [providers](https://github.com/moltis-org/moltis/blob/main/docs/src/providers.md) ·
[agent presets](https://github.com/moltis-org/moltis/blob/main/docs/src/agent-presets.md) ·
[voice](https://github.com/moltis-org/moltis/blob/main/docs/src/voice.md)

---

## 16. QwenPaw

**Category:** personal "Agent OS" (Alibaba AgentScope) · **License:** Apache-2.0 · ⭐ 35.6k ·
**Release:** v2.2.1 (11 September 2026) · **Score: 74** (A4 B4 C3 D4 E3 F4)

**What it is.** Formerly CoPaw: an assistant with a web console, a TUI and a desktop app, three-layer memory,
skills, MCP / A2A / ACP, multiple agents and messenger channels.

**Advantage.** Layered security: a kernel sandbox (Bubblewrap / Landlock), Tool Guard with approval
levels, protection of files with secrets, a skill scanner before activation. Per-agent model routing since v2.2.1.

**Local model.** A custom provider in OpenAI `chat.completions` mode. Set the context window manually —
the cloud catalogue is sometimes applied to a local alias (#7979, pitfall H3).

**Multiple agents and hybrid.** Independent agents with their own model and memory; `spawn_subagent` with isolation
in a git worktree.

**Voice and vision.** Transcription via the Whisper API or a local Whisper (open bugs, e.g. #8035); the
`view_media` tool and images from channels — a model with vision is needed.

**Security.** Described under Advantage: a kernel sandbox, Tool Guard with STRICT / SMART / AUTO / OFF levels,
protection of files with secrets, a skill scanner.

**Weaknesses.** Channels geared toward China (DingTalk recommended; no WhatsApp or Signal), over 1,000 open
issues and PRs, open transcription bugs.

**What to steal.** The Tool Guard rule engine with levels; a skill scanner before activation; "Scroll Context" —
index removed turns instead of lossily summarizing them; the context window taken from the server, never from a name catalogue.

**Sources:** [models](https://github.com/agentscope-ai/QwenPaw/blob/main/website/public/docs/models.en.md) ·
[multi-agent](https://github.com/agentscope-ai/QwenPaw/blob/main/website/public/docs/multi-agent.en.md) ·
[#7979](https://github.com/agentscope-ai/QwenPaw/issues/7979)

---

## 17. OpenAI Agents SDK

**Category:** lightweight multi-agent SDK (Python) · **License:** MIT · ⭐ 30.0k · **Release:** v0.23.1 (2 October 2026) ·
**Score: 74** (A4 B3 C3 D4 E5 F4)

**What it is.** A small set of primitives: `Agent`, `Runner`, tools, handoffs (*handoffs*),
agents-as-tools, *guardrails*, sessions, `RunState`; plus sandboxed agents and a voice pipeline.

**Advantage.** The simplest mental model on the list; a serializable `RunState` (pause → approve → resume even after
hours); `VoicePipeline` with swappable STT and TTS.

**Local model.**
`OpenAIChatCompletionsModel(model="deepseek-v4-flash", openai_client=AsyncOpenAI(base_url="http://localhost:8080/v1", api_key="none"))`
and `set_tracing_disabled(True)` — otherwise the trace export to OpenAI returns 401. The default Responses API does not work
with llama-server (pitfall H1).

**Multiple agents and hybrid.** Every `Agent(model=...)` separately; Claude via a LiteLLM adapter or any-llm
(no native Anthropic provider). With LiteLLM pin versions — see [02-BUILDING-BLOCKS.md](02-BUILDING-BLOCKS.md#gateway-and-model-routing).

**Voice.** `VoicePipeline` = STT → your workflow → TTS; OpenAI models by default, but the interfaces are swappable,
so a local Whisper and Piper come in through custom adapters.

**Security.** Sandboxed agents (local for trusted code or in Docker), input and output guardrails,
tool error redaction (v0.23.0). Images pass as message parts.

**Weaknesses.** OpenAI defaults that need overriding; structured output suppressed tool calls
on strict servers (#3709, fixed); 0.x versions.

**What to steal.** `RunState` with a list of interruptions and an approve / reject API; input filters on handoffs;
*guardrails* as "circuit breakers" running in parallel with the agent.

**Sources:** [models](https://openai.github.io/openai-agents-python/models/) ·
[repository](https://github.com/openai/openai-agents-python) ·
[release v0.23.0](https://github.com/openai/openai-agents-python/releases/tag/v0.23.0)

---

## 18. n8n

**Category:** automation platform (visual, *fair-code*) · **License:** Sustainable Use License · ⭐ 207.0k ·
**Release:** n8n@2.42.6 (9 October 2026) · **Score: 73** (A4 B3 C4 D5 E3 F2)

**What it is.** A visual workflow editor with agent nodes, self-hosted, with a huge catalogue of
integrations.

**Advantage.** The broadest set of triggers and integrations (cron, webhooks, RSS with deduplication, email, Telegram,
Google Sheets…) and per-tool human approval, sent to Telegram, Slack or email.
The fastest path from an idea to a working alert.

**Local model.** The OpenAI credential has a "Base URL" field → `http://localhost:8080/v1`. In the OpenAI Chat Model node
**turn off "Use Responses API"** — with llama.cpp it ended in a 400 error (#26639, pitfall H1).

**Multiple agents and hybrid.** An orchestrator agent with an Anthropic Chat Model node, agents-as-tools (AI Agent Tool)
with a local model — the model is chosen per node.

**⚠️ License.** The Sustainable Use License is not open source in the OSI sense: you may use it internally and in your own
processes, you may not offer n8n as a service; `.ee.` files are under a commercial license.

**⚠️ Security.** The critical vulnerability CVE-2026-21858 (7 January 2026): unauthenticated file access through
webhook handling, which according to the Australian CERT (ACSC) advisory allows remote code execution without
logging in. Do not expose an instance to the internet without updating. The production concurrency limit does not cover
sub-workflows.

**Voice and vision.** No voice loop (to build: a Telegram voice note → a local Whisper → agent → TTS);
images reach the model via the "Automatically Passthrough Binary Images" option.

**What to steal.** Per-tool approval sent to a messenger; polling triggers with remembered
state (RSS fires only on new items); a separate FIFO queue for production executions.

**Sources:** [license](https://docs.n8n.io/n8n-community-license/sustainable-use-license) ·
[AI Agent Tool](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolaiagent) ·
[human in the loop](https://docs.n8n.io/advanced-ai/human-in-the-loop-tools) ·
[security advisories](https://github.com/n8n-io/n8n/security/advisories)

---

## 19. LibreChat

**Category:** multi-user chat platform with agents · **License:** MIT · ⭐ 45.5k · **Release:** v0.8.8 (1 October 2026) ·
**Score: 73** (A5 B3 C3 D4 E2 F4)

**What it is.** A ChatGPT-style platform combining cloud providers and custom OpenAI-compatible endpoints:
agents with tools, MCP, code and memory, subagent teams and an Agents API. Acquired by ClickHouse;
the repository was moved to `LibreChat-AI`.

**Advantage.** A real choice of provider and model per agent, saved subagent teams as small graphs (DAGs),
an open-source code interpreter (NsJail or the libkrun micro-VM), approval rules, Prometheus / OpenTelemetry /
Langfuse.

**Local model.** `librechat.yaml` → `endpoints.custom[]` with `baseURL: "http://localhost:8080/v1"`. For DeepSeek
`customParams.includeReasoningContent: true` (pitfall H2); set the context window explicitly (#14228).

**Multiple agents and hybrid.** A parent agent on Anthropic creates children pinned to the llama.cpp endpoint
(`agent_ids` or a team graph); `maxSubagents` defaults to 10.

**Voice and scheduling.** STT and TTS configurable, including local OpenAI-compatible services; no live conversations.
"Scheduled Chats" — experimental, since v0.8.8.

**Security and vision.** Approval rules deny → ask → allow, enforced also in headless and scheduled runs;
code approval modes; the interpreter in NsJail or the libkrun micro-VM. Native image upload,
OCR and image generation.

**Weaknesses.** A heavy stack (MongoDB, Meilisearch, pgvector); many features in beta; recurring tool schema
bugs with llama.cpp; a prompt cache regression (#16877); critical CVEs in the MCP area.

**What to steal.** Approval rules in the order deny → ask → allow; subagent teams as a DAG with an entry
and an output agent; schedule circuit breakers (`minIntervalMinutes`, `autoDisableAfterFailures`).

**Sources:** [agents](https://www.librechat.ai/docs/features/agents) ·
[release v0.8.8](https://www.librechat.ai/changelog/v0.8.8) ·
[releases](https://github.com/LibreChat-AI/LibreChat/releases)

---

## 20. Kilo Code

**Category:** coding agent (CLI, VS Code, JetBrains) · **License:** MIT · ⭐ 27.6k ·
**Release:** JetBrains 7.1.9 (8 October 2026) · **Score: 73** (A5 B3 C3 D4 E3 F3)

**What it is.** A fork of OpenCode; since 2 April 2026 the VS Code extension runs on the same server core.
A natural migration path for users of the archived Roo Code.

**Advantage.** The OpenCode core + a UI in VS Code and JetBrains, a manager of parallel agents in separate git worktrees,
a separate cheap model for memory and compaction.

**Local model.** Settings → Providers → "OpenAI Compatible" with a Base URL; in the CLI `~/.config/kilo/kilo.jsonc`.
Recurring tool schema incompatibilities with llama.cpp (#12773 — fixed, #12408 — pitfall H7).

**Multiple agents and hybrid.** Every agent and subagent pins a `provider/model` — the main one on `anthropic/claude-…`,
subagents on llama-swap.

**Voice and vision.** Experimental "Speech to Text" via OpenAI's cloud Whisper; images in the CLI probably
as in OpenCode (unverified).

**Security.** Permission rules with patterns per agent, isolation in a git worktree, a privacy mode masking
personal data; no system sandbox.

**Weaknesses.** A large part of the "always-on" features (Cloud Agents, Slack) is a paid service; the Orchestrator mode
was withdrawn during its lifetime; risk of diverging from upstream.

**What to steal.** A manager of agents in separate worktrees; readable exit codes in CI (124 = timeout).

**Sources:** [custom subagents](https://kilo.ai/docs/customize/custom-subagents) ·
[CLI](https://kilo.ai/docs/code-with-ai/platforms/cli) · [#12773](https://github.com/Kilo-Org/kilocode/issues/12773)

---

## Remaining candidates (ranks 21–64)

They passed the entry criteria (Paperclip and Hive — only indirectly, via adapters), but lost on scoring.
One sentence for each: why it is worth knowing it exists, and what held it back.

| # | Harness | Category | Score | Pros | Cons |
|---|---|---|---|---|---|
| 21 | [Vercel AI SDK](https://github.com/vercel/ai) | TS framework | 72 | the standard model layer in TS, multimodality | the agent is a thin layer; scheduling and integrations are DIY |
| 22 | [Agent Zero](https://github.com/agent0ai/agent-zero) | personal | 71 | a whole computer in Docker per agent, local Whisper and Kokoro | frequent regressions in the 2.x versions |
| 23 | [nanobot](https://github.com/HKUDS/nanobot) | personal | 71 | a readable Python core to fork, an OpenAI-compatible API | subagents inherit the parent's model |
| 24 | [Google ADK](https://github.com/google/adk-python) | Py framework | 70 | the best A2A, evaluation tools, a dev UI | non-Gemini models via LiteLLM — a source of bugs |
| 25 | [Agno](https://github.com/agno-agi/agno) | Py framework | 70 | a complete runtime: scheduler, queue, channels, FinanceTools | a huge core file, a breaking v3 |
| 26 | [Qwen Code](https://github.com/QwenLM/qwen-code) | coding | 70 | a vision bridge for text models, dictation | frequent schema regressions with llama.cpp |
| 27 | [Haystack](https://github.com/deepset-ai/haystack) | Py framework | 70 | the best RAG and search stack | concurrency limit per pipeline, not per model |
| 28 | [OpenJarvis](https://github.com/open-jarvis/OpenJarvis) | personal | 70 | local first, 15+ engines | young, research-grade code |
| 29 | [Open WebUI](https://github.com/open-webui/open-webui) | personal | 69 | the best UI for local models, voice | subagents always on the parent's model; 158 security advisories in 2026; a license with a branding clause |
| 30 | [Sim](https://github.com/simstudioai/sim) | workflow | 69 | visual multi-agent workflows, RSS every minute, Apache-2.0 | llama.cpp unofficial (#1637), pre-1.0 |
| 31 | [Codewhale](https://github.com/codewhale-hq/Codewhale) | coding | 69 | a fleet of roles with models, a local `/voice` | drift toward accounts and the cloud, telemetry by default |
| 32 | [PicoClaw](https://github.com/sipeed/picoclaw) | personal | 69 | lightweight Go for weak hardware | no system sandbox, pre-1.0 |
| 33 | [Cline](https://github.com/cline/cline) | coding | 68 | great in the IDE, a Plan/Act split across two models | tool format changes broke local models (#13008); dictation is paid |
| 34 | [CrewAI](https://github.com/crewAIInc/crewAI) | Py framework | 68 | the simplest model of roles and tasks | "empty response" bugs with local models; telemetry by default |
| 35 | [LlamaIndex Workflows](https://github.com/run-llama/llama_index) | Py framework | 68 | a readable event engine, `num_workers` per step | the company focuses on documents |
| 36 | [Reasonix](https://github.com/esengine/DeepSeek-Reasonix) | coding | 68 | a native planner + executor mode | local models are second class, a single maintainer |
| 37 | [Kestra](https://github.com/kestra-io/kestra) | workflow | 68 | YAML, a concurrency limit in OSS, a pause for approval | Java, less convenient for prototypes |
| 38 | [Mastra](https://github.com/mastra-ai/mastra) | TS framework | 68 | the fullest TS stack | an npm supply-chain attack (June 2026); system messages in the middle of a conversation |
| 39 | [Windmill](https://github.com/windmill-labs/windmill) | workflow | 68 | the best for DevOps: scripts, cron, webhooks | concurrency limits only in EE; AGPL + closed parts |
| 40 | [OpenAI Agents SDK (JS)](https://github.com/openai/openai-agents-js) | TS framework | 67 | the best real-time voice in TS | voice only with OpenAI models |
| 41 | [Dify](https://github.com/langgenius/dify) | workflow | 66 | the best RAG among visual tools | the license forbids multi-tenant SaaS; heavy updates |
| 42 | [LobeHub](https://github.com/lobehub/lobehub) | personal | 66 | the best UI for agent teams | the license restricts derivative works |
| 43 | [Langflow](https://github.com/langflow-ai/langflow) | workflow | 66 | every project is an MCP server | no scheduler, voice removed, a series of security advisories |
| 44 | [VoltAgent](https://github.com/VoltAgent/voltagent) | TS framework | 65 | parallel delegation to multiple subagents | triggers and console in a paid SaaS |
| 45 | [Crush](https://github.com/charmbracelet/crush) | coding | 65 | a native llama.cpp provider type | FSL license (not OSI), no sandbox |
| 46 | [Omnigent](https://github.com/omnigent-ai/omnigent) | meta-harness | 65 | combines Claude Code, Codex and Pi in one session | alpha status |
| 47 | [OpenClaw](https://github.com/openclaw/openclaw) | personal | 64 | the largest ecosystem, the most channels, voice | see [README](README.md#why-they-are-not-at-the-top) |
| 48 | [BeeAI Framework](https://github.com/i-am-bee/beeai-framework) | Py framework | 63 | tool-use rules that help weak models | a small community |
| 49 | [Cherry Studio](https://github.com/CherryHQ/cherry-studio) | personal | 62 | an OpenClaw-style agent in a desktop app | the local agents path is buggy; AGPL |
| 50 | [NanoClaw](https://github.com/nanocoai/nanoclaw) | personal | 62 | a container per agent group | built around Claude; local only via OpenCode |
| 51 | [AG2](https://github.com/ag2ai/ag2) | Py framework | 62 | built-in voice (cascade and realtime) | v1 incompatible with the old AutoGen |
| 52 | [Open Interpreter](https://github.com/openinterpreter/openinterpreter) | coding | 61 | rewritten in Rust, per-model "harness emulation" | 0.0.x versions |
| 53 | [Mistral Vibe](https://github.com/mistralai/mistral-vibe) | coding | 60 | built-in voice | cloud voice; no Anthropic; template bugs with llama.cpp |
| 54 | [Paperclip](https://github.com/paperclipai/paperclip) | meta-harness | 60 | a "company of agents" with budgets | local model only indirectly (via OpenCode or Pi adapters) |
| 55 | [smolagents](https://github.com/huggingface/smolagents) | Py framework | 60 | the smallest readable core (CodeAgent) | slowed maintenance, no durability |
| 56 | [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) | coding | 59 | 100 lines, bash only — great for learning | no MCP or subagents by design |
| 57 | [CAMEL](https://github.com/camel-ai/camel) | Py framework | 58 | a broad tool catalogue | only alpha releases for half a year |
| 58 | [Jan](https://github.com/janhq/jan) | personal | 58 | the best local model UX on the desktop | no voice; MCP with custom endpoints broken |
| 59 | [Codex CLI](https://github.com/openai/codex) | coding | 57 | a great sandbox and CI | Responses API only since February 2026; no Anthropic |
| 60 | [Letta Code](https://github.com/letta-ai/letta-code) | TS framework | 57 | memory as the core | now TypeScript, cloud by default |
| 61 | [IronClaw](https://github.com/nearai/ironclaw) | personal | 55 | tools in WASM, secret protection | the 1.0 rewrite reset the features |
| 62 | [Activepieces](https://github.com/activepieces/activepieces) | workflow | 53 | MIT and a huge integration library | agents disabled in the free Community edition |
| 63 | [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) | personal | 51 | the simplest installation | no multi-agent (#2635) |
| 64 | [Hive](https://github.com/aden-hive/hive) | Py framework | 50 | agent "colonies" with failure recovery | local model only indirectly (via LiteLLM), direct support is an open issue (#7324) |

## Excluded at entry

They failed one of the four conditions (a license that allows self-hosting, a documented local OpenAI-compatible
endpoint, activity: a commit ≤ 3 months and a release ≤ 6 months before 11 October 2026, the project not
officially discontinued).

| Project | Reason |
|---|---|
| [Roo Code](https://github.com/RooCodeInc/Roo-Code) | archived 15 May 2026 (community continuation: Zoo Code; migration: Kilo Code) |
| [Flowise](https://github.com/FlowiseAI/Flowise) | sunset, archived 10 August 2026; unpatched critical vulnerabilities will stay unpatched |
| [Continue](https://github.com/continuedev/continue) | the maintainers announced the end of the project (acquisition by Cursor; README: "no longer actively maintained"); last release 2.0.0 from 19 June 2026 |
| [Plandex](https://github.com/plandex-ai/plandex) | no commits since 3 October 2025 |
| [Aider](https://github.com/Aider-AI/aider) | last commit 22 May 2026, last release 9 August 2025 — effectively on hold |
| [Khoj](https://github.com/khoj-ai/khoj) | last release 26 March 2026, maintenance mode |
| [Google ADK for TypeScript](https://github.com/google/adk-js) | no OpenAI-compatible provider (issue #533 open) |
| [Grok Build](https://github.com/xai-org/grok-build) | no releases; first launch requires logging in to xAI (unverified without an account); in July 2026 uploading entire repositories to a server was reported |

## Outside the ranking

Great, but not harnesses — I describe them in [02-BUILDING-BLOCKS.md](02-BUILDING-BLOCKS.md):

- **DSPy** — compiling LLM programs for a specific (also weak, local) model; Claude as the teacher in GEPA.
- **forge** — a tool-call reliability layer for local models and a slot queue.
- **Trigger.dev** — durable task infrastructure with concurrency limits.
