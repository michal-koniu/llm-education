# Sources — what this review stands on

**Checked on 11 October 2026.** For each entry: what I took from it and where it appears in the review.
Primary sources (documentation, code, release notes, GitHub issues, model cards) take precedence;
I mark blogs and marketing material *(blog)* or *(marketing)*. Each profile in [01-PROFILES.md](01-PROFILES.md)
also has its own source links.

> ⚠️ **Everything here goes stale within weeks.** Treat a number from this page as someone else's dated measurement — to be
> checked on your own before you base a decision on it.

---

## 1. Numbers from GitHub

- **GitHub API** — `GET /repos/{owner}/{repo}`, `GET /repos/{…}/releases/latest`,
  `GET /repos/{…}/security-advisories`, called on 11 October 2026 for 218 repositories.
  → stars, licences, dates of the latest releases and commits, the "archived" status in [README.md](README.md) and the profiles;
  the number of OpenClaw security advisories (722 in 2026: 14 critical, 249 high, 390 medium, 69 low)
  and Open WebUI (158 in 2026).
- `releases/latest` skips pre-releases, and in monorepos it returns a release of a different package. For
  LangGraph (the `langgraph` package), Strands Agents (harness), Kilo Code (JetBrains plugin), DeepSeek Harness
  and LibreChat I took the version from the project's release pages.

## 2. Top harnesses

| Harness | Sources | What I took |
|---|---|---|
| LangGraph | [models](https://docs.langchain.com/oss/python/langchain/models), [durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution), [multi-agent patterns](https://docs.langchain.com/oss/python/langchain/multi-agent), [#40219](https://github.com/langchain-ai/langchain/issues/40219), [#35514](https://github.com/langchain-ai/langchain/issues/35514) | OpenAI-compatible configuration, durability modes, five patterns, `reasoning_content` and streaming bugs |
| Goose | [environment variables](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/environment-variables.md), [subagents](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/context-engineering/subagents.mdx), [tool shim](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/tool-shim.md), [Adversary](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/security/adversary-mode.md), [move to AAIF](https://github.com/aaif-goose/goose/blob/main/documentation/blog/2026-04-07-goose-moves-to-aaif/index.md), [#11142](https://github.com/aaif-goose/goose/issues/11142) | subagent model, recipes and cron, security modes, the foundation, known bugs with local providers |
| OpenHands | [local models](https://docs.openhands.dev/openhands/usage/llms/local-llms), [file-based agents](https://github.com/OpenHands/docs/blob/main/sdk/guides/agent-file-based.mdx), [OpenAI gateway](https://github.com/OpenHands/docs/blob/main/sdk/guides/agent-server/openai-gateway.mdx), [Canvas v1.25.0](https://docs.openhands.dev/openhands/usage/agent-canvas/release-notes/v1.25.0), [#16459](https://github.com/OpenHands/OpenHands/issues/16459) | connecting via LiteLLM, `model: inherit`, an agent as a "model", voice input, the fixed concurrency lock |
| Hermes Agent | [delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation), [providers](https://hermes-agent.nousresearch.com/docs/integrations/providers), [configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration), [voice](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode), [cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron), [releases](https://github.com/NousResearch/hermes-agent/releases) | `delegation.provider/model/base_url`, 10 children by default, `context_length`, STT/TTS, cron without an agent, the pace of change |
| Pydantic AI | [PR #4149](https://github.com/pydantic/pydantic-ai/pull/4149) (merged 4 February 2026), [OpenAI-compatible APIs](https://pydantic.dev/docs/ai/models/compatible-apis/index.md), [subagents](https://pydantic.dev/docs/ai/harness/subagents/index.md), [release v2.0.0](https://github.com/pydantic/pydantic-ai/releases/tag/v2.0.0), [#4878](https://github.com/pydantic/pydantic-ai/issues/4878) | `ConcurrencyLimiter` / `ConcurrencyLimitedModel` (checked in the code: `pydantic_ai/concurrency.py`), capabilities v2, heuristics for llama.cpp |
| Deep Agents | [overview](https://docs.langchain.com/oss/python/deepagents/overview), [subagents](https://docs.langchain.com/oss/python/deepagents/subagents), [async subagents](https://docs.langchain.com/oss/python/deepagents/async-subagents), [Open Deep Research — archive](https://github.com/langchain-ai/open_deep_research) | model per subagent, `task` in parallel, the successor to Open Deep Research |
| Strands Agents | [llama.cpp provider](https://github.com/strands-agents/harness-sdk/blob/main/strands-py/src/strands/models/llamacpp.py), [harness](https://github.com/strands-agents/harness-sdk/blob/main/site/src/content/docs/user-guide/harness/index.mdx), [BidiAgent GA](https://github.com/strands-agents/harness-sdk/blob/main/site/src/content/blog/bidi-agents-now-ga.mdx), [#4620](https://github.com/strands-agents/harness-sdk/issues/4620) | native `LlamaCppModel`, a ready-made harness, cloud-only voice, 200k context by default |
| OpenCode | [providers](https://opencode.ai/docs/providers/), [agents](https://opencode.ai/docs/agents/), [server](https://opencode.ai/docs/server/), [#7410](https://github.com/anomalyco/opencode/issues/7410), [#52462](https://github.com/anomalyco/opencode/issues/52462) | `@ai-sdk/openai-compatible` configuration, model and permissions per agent, the Pro/Max login block (9 January 2026), the `function.name: null` bug |
| DeerFlow | [README](https://github.com/bytedance/deer-flow), [config.example.yaml](https://github.com/bytedance/deer-flow/blob/main/config.example.yaml), [#1055](https://github.com/bytedance/deer-flow/issues/1055) | llama.cpp example, model per subagent, scheduled tasks, problems with local models |
| ZeroClaw | [providers](https://github.com/zeroclaw-labs/zeroclaw/blob/master/docs/book/src/providers/configuration.md), [delegation](https://github.com/zeroclaw-labs/zeroclaw/blob/master/docs/book/src/agents/delegation.md), [multiple models](https://github.com/zeroclaw-labs/zeroclaw/blob/master/docs/book/src/getting-started/multi-model-setup.md), [#10396](https://github.com/zeroclaw-labs/zeroclaw/issues/10396) | `llamacpp` slot, `native_tools`, delegation forbidden by default, risk profiles |
| Microsoft Agent Framework | [OpenAI provider](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/openai), [checkpoints](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints), [orchestrations](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/), [#8382](https://github.com/microsoft/agent-framework/issues/8382) | the `OpenAIChatClient` = Responses API trap, orchestrations, the `reasoning_content` fix (September 2026) |
| DeepSeek Harness | [README](https://github.com/deepseek-ai/deepseek-harness/blob/main/README.md), [providers](https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/user/guide/providers.md), [SAFETY.md](https://github.com/deepseek-ai/deepseek-harness/blob/main/SAFETY.md) | `compat` profile, Claude Code / Codex / ACP subagents, read-only by default, pre-release status |
| Pi | [agent README](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md), [llama.cpp](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/llama-cpp.md), [models](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md), [security](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md) | llama.cpp router mode, `models.json`, virtual models, no approvals by design |
| gptme | [providers](https://gptme.org/docs/providers.html), [tool formats](https://github.com/gptme/gptme/blob/master/docs/tool-formats.rst), [subagents](https://github.com/gptme/gptme/blob/master/docs/tools/subagent.rst) | `OPENAI_BASE_URL`, `--tool-format xml`, subagent isolation modes |
| Moltis | [providers](https://github.com/moltis-org/moltis/blob/main/docs/src/providers.md), [agent presets](https://github.com/moltis-org/moltis/blob/main/docs/src/agent-presets.md), [voice](https://github.com/moltis-org/moltis/blob/main/docs/src/voice.md), [local LLM](https://github.com/moltis-org/moltis/blob/main/docs/src/local-llm.md) | presets with a model, `delegate_only`, local STT/TTS, no ROCm path in the built-in backend; number of commits — contributors API |
| QwenPaw | [models](https://github.com/agentscope-ai/QwenPaw/blob/main/website/public/docs/models.en.md), [multi-agent](https://github.com/agentscope-ai/QwenPaw/blob/main/website/public/docs/multi-agent.en.md), [channels](https://github.com/agentscope-ai/QwenPaw/blob/main/website/public/docs/channels.en.md), [#7979](https://github.com/agentscope-ai/QwenPaw/issues/7979) | `chat.completions` mode, model per agent, the list of channels, the context window bug |
| OpenAI Agents SDK | [models](https://openai.github.io/openai-agents-python/models/), [release v0.23.0](https://github.com/openai/openai-agents-python/releases/tag/v0.23.0), [repository](https://github.com/openai/openai-agents-python) | `OpenAIChatCompletionsModel`, disabling tracing, Claude via LiteLLM, voice pipeline |
| n8n | [licence](https://docs.n8n.io/n8n-community-license/sustainable-use-license), [AI Agent Tool](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolaiagent), [human in the loop](https://docs.n8n.io/advanced-ai/human-in-the-loop-tools), [concurrency](https://docs.n8n.io/hosting/scaling/concurrency-control), [security advisories](https://github.com/n8n-io/n8n/security/advisories), [ACSC alert](https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/critical-unauthenticated-remote-code-execution-vulnerability-in-n8n-workflow-automation-platform), [#26639](https://github.com/n8n-io/n8n/issues/26639), [OpenAI Chat Model node](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmchatopenai/) | licence terms, model per node, approvals, a limit that does not cover sub-workflows, CVE-2026-21858 (checked in the API: critical, 7 January 2026; per ACSC unauthenticated remote code execution), the "Use Responses API" switch (Chat Completions by default) |
| LibreChat | [agents](https://www.librechat.ai/docs/features/agents), [release v0.8.8](https://www.librechat.ai/changelog/v0.8.8), [config v1.3.15](https://www.librechat.ai/changelog/config_v1.3.15), [releases](https://github.com/LibreChat-AI/LibreChat/releases) | `endpoints.custom`, `includeReasoningContent`, subagent teams, approval rules, Scheduled Chats |
| Kilo Code | [custom subagents](https://kilo.ai/docs/customize/custom-subagents), [CLI](https://kilo.ai/docs/code-with-ai/platforms/cli), [licence](https://github.com/Kilo-Org/kilocode/blob/main/LICENSE), [#12773](https://github.com/Kilo-Org/kilocode/issues/12773) | model per subagent, OpenCode core, schema incompatibility with the llama.cpp grammar |

## 3. Verified separately in the primary source

I checked the claims that changed the ranking the most myself, outside the research agents:

| Claim | Source | Score |
|---|---|---|
| compromise of LiteLLM 1.82.7 and 1.82.8 | [BerriAI/litellm#24518](https://github.com/BerriAI/litellm/issues/24518) | confirmed, 24 March 2026 |
| Codex CLI removed Chat Completions | [openai/codex — discussion #7782](https://github.com/openai/codex/discussions/7782) | confirmed: an error with `wire_api = "chat"` since February 2026 |
| a request for local models for Claude Code subagents | [anthropics/claude-code#38698](https://github.com/anthropics/claude-code/issues/38698) | open |
| Flowise and Roo Code archived | GitHub API (`archived: true`) | confirmed |
| OpenBB under a new organization, licence | GitHub API (`OpenBB-finance/OpenBB` → `openbq-org/OpenBB`) | redirect confirmed; licence change to Apache-2.0 in V5 per the release notes |
| attack on Mastra npm packages | [BankInfoSecurity](https://www.bankinfosecurity.com/north-korean-hackers-poison-mastra-ai-framework-a-32042) *(press)* | 140+ packages, attributed to BlueNoroff by Microsoft |
| DeepSeek-V4-Flash: size, licence, no image input | [model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash) | 284B / 13B active, MIT, 1M context, no vision |
| Claude prices | [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing) | Opus 5.5 4 / 20, Sonnet 5.5 2 / 10, Haiku 5.5 0.10 / 0.50 USD per million tokens; Batch −50% |
| OpenClaw: hundreds of malicious skills, exposed instances | [insiderllm](https://insiderllm.com/guides/openclaw-clawhub-security-alert/) *(blog)*, [security advisories](https://github.com/openclaw/openclaw/security/advisories), [security documentation](https://docs.openclaw.ai/gateway/security) | number of advisories confirmed in the API; figures from industry reports (SecurityScorecard, Koi Security) from a secondary source only |

## 4. Building blocks

| Group | Key sources | What I took |
|---|---|---|
| gateways | [llama-swap](https://github.com/mostlygeek/llama-swap), [Bifrost — performance and concurrency](https://docs.getbifrost.ai/providers/performance), [Datadog Security Labs on LiteLLM](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/) | `concurrency` with a queue, the course of the compromise |
| search | [SearXNG — settings.yml](https://raw.githubusercontent.com/searxng/searxng/master/searx/settings.yml), [Crawl4AI — CHANGELOG](https://raw.githubusercontent.com/unclecode/crawl4ai/main/CHANGELOG.md), [Trafilatura](https://github.com/adbar/trafilatura), [Scrapling](https://github.com/D4Vinci/Scrapling), [Playwright MCP](https://github.com/microsoft/playwright-mcp) | JSON disabled by default, Docker server security fixes, the recommendation of CLI over MCP |
| deep research | [Local Deep Research](https://github.com/LearningCircuit/local-deep-research), [#6820](https://github.com/LearningCircuit/local-deep-research/issues/6820), [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | topic subscriptions, no subagent limit, BM25 instead of embeddings |
| prices and changes | [changedetection.io](https://github.com/dgtlmoon/changedetection.io), [Huginn](https://github.com/huginn/huginn), [urlwatch](https://github.com/thp/urlwatch) | price and availability mode, AI rules via llama.cpp |
| finance | [OpenBB ODP — MCP](https://docs.openbb.co/odp/python/quickstart/mcp), [edgartools](https://github.com/dgunning/edgartools), [CCXT](https://github.com/ccxt/ccxt), [TradingAgents v0.6.0](https://github.com/TauricResearch/TradingAgents/releases/tag/v0.6.0), [yfinance](https://github.com/ranaroussi/yfinance) | provider per tier (Opus `deep_think`), SEC limits, data terms |
| notifications | [ntfy — configuration](https://docs.ntfy.sh/config/), [Apprise — releases](https://github.com/caronc/apprise/releases), [Telegram Bot API — changes](https://core.telegram.org/bots/api-changelog) | `upstream-base-url`, breaking v2.0.0, new voice input options in Bot API 10.1–10.3 |
| scheduling | [Prefect — server](https://docs.prefect.io/v3/manage/server), [DBOS](https://github.com/dbos-inc/dbos-transact-py), [Temporal](https://github.com/temporalio/temporal), [systemd timers](https://github.com/systemd/systemd/blob/main/man/systemd.timer.xml) | SQLite without Docker, queues with a limit, `Persistent=true` |
| memory | [Cognee — LLM providers](https://docs.cognee.ai/setup-configuration/llm-providers), [Cognee v1.6.0](https://github.com/topoteretes/cognee/releases/tag/v1.6.0), [Graphiti](https://github.com/getzep/graphiti), [Mem0](https://github.com/mem0ai/mem0) | mode without a cloud key, removal of graph memory from Mem0 OSS |
| observability | [Phoenix — self-hosting](https://arize.com/docs/phoenix/self-hosting), [Langfuse](https://github.com/langfuse/langfuse), [OpenLIT](https://github.com/openlit/openlit), [promptfoo](https://github.com/promptfoo/promptfoo) | ELv2 licence, AMD GPU monitoring, the acquisition of promptfoo by OpenAI |
| sandboxes | [sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime), [microsandbox](https://github.com/superradcompany/microsandbox), [E2B runtime](https://github.com/e2b-dev/runtime), [Daytona](https://github.com/daytonaio/daytona) | no Docker, micro-VMs, the closing of Daytona's core |
| MCP for DevOps | [kubernetes-mcp-server — configuration](https://github.com/containers/kubernetes-mcp-server/blob/main/docs/configuration.md), [mcp-grafana — releases](https://github.com/grafana/mcp-grafana/releases), [github-mcp-server](https://github.com/github/github-mcp-server), [GitLab MCP](https://docs.gitlab.com/user/model_context_protocol/mcp_server/) | read-only modes, telemetry on by default in mcp-grafana 2.0 |

## 5. Voice and vision

| Topic | Sources | What I took |
|---|---|---|
| Pipecat and Polish | [Pipecat](https://github.com/pipecat-ai/pipecat), [Smart Turn](https://github.com/pipecat-ai/smart-turn), [LiveKit Agents](https://github.com/livekit/agents) | Smart Turn supports Polish (94.47% per the v3.0 announcement *(blog)*), LiveKit detectors do not |
| STT in Polish | [whisper.cpp](https://github.com/ggml-org/whisper.cpp), [Parakeet-TDT-0.6B-v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3), [Canary-1B-v2](https://huggingface.co/nvidia/canary-1b-v2), [Qwen3-ASR](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) | WER on FLEURS-pl: Whisper large-v3 4.74%, Canary 6.64%, Parakeet 7.31% (NVIDIA's table) |
| TTS in Polish | [Piper](https://github.com/OHF-Voice/piper1-gpl), [Chatterbox](https://github.com/resemble-ai/chatterbox), [VoxCPM](https://github.com/OpenBMB/VoxCPM), [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M), [F5-TTS](https://github.com/SWivid/F5-TTS) | which ones have Polish and under what licence; Chatterbox's watermark; F5 requires ROCm 7.x on RDNA4 |
| speech-to-speech | [Moshi](https://github.com/kyutai-labs/moshi), [Unmute](https://github.com/kyutai-labs/unmute) | no Polish, no ROCm path |
| DeepSeek and vision | [DeepSeek-V4-Flash-Vision-Exp](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp), [llama.cpp b10766](https://github.com/ggml-org/llama.cpp/releases/tag/b10766), [#28939](https://github.com/ggml-org/llama.cpp/issues/28939), [multimodal in llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md) | the variant with vision, the minimum llama.cpp version |
| vision models and OCR | [Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B), [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), [Holo4-35B-A3B](https://huggingface.co/Hcompany/Holo4-35B-A3B), [Docling](https://github.com/docling-project/docling), [PaddleOCR-VL-1.5](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5) | sizes, licences, llama.cpp support |
| image generation | [ComfyUI](https://github.com/comfyanonymous/ComfyUI), [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp), [Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511), [Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo), [FLUX.2 klein 4B](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B) | models under Apache-2.0 vs non-commercial |

## 6. Hybrid, routing and costs

| Topic | Sources | What I took |
|---|---|---|
| planner + executor in coding | [Aider: architect/editor](https://aider.chat/2024/09/26/architect.html) | 80.5% and 78.9% with DeepSeek as the editor |
| the cloud splits, the local model processes | [Minions — arXiv 2502.15964](https://arxiv.org/abs/2502.15964), [repository](https://github.com/HazyResearch/minions) | 5.7× lower cost at 97.9% of the quality |
| device / cloud routing | [Hera — arXiv 2605.24598](https://arxiv.org/abs/2605.24598) | 92.5% effectiveness with the cloud in 46.3% of steps |
| cost of local models alone | [OpenJarvis — arXiv 2605.17172](https://arxiv.org/abs/2605.17172) | −25 to −39 pp after swapping Opus for a small model |
| advisor tool | [The advisor strategy](https://claude.com/blog/the-advisor-strategy) *(vendor)* | +2.7 pp at 11.9% lower cost; Claude models only |
| Claude Code and local models | [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [LLM gateways](https://code.claude.com/docs/en/llm-gateway), [custom tools in the Agent SDK](https://code.claude.com/docs/en/agent-sdk/custom-tools) | no local model support for subagents; the "local agent as a tool" pattern |
| MCP servers delegating to local models | [mcp-llama-swap](https://github.com/oussama-kh/mcp-llama-swap), [PAL](https://github.com/BeehiveInnovations/pal-mcp-server) | Claude stays the orchestrator |
| Goose lead/worker | [multi-model in Goose](https://goose-docs.ai/docs/guides/multi-model/) | mode removed, explicit delegation remained |
| DeepSeek in llama.cpp | [#29008 — prompt cache in loops](https://github.com/ggml-org/llama.cpp/pull/29008), [#26398](https://github.com/ggml-org/llama.cpp/pull/26398), [#26269](https://github.com/ggml-org/llama.cpp/pull/26269), [b10217](https://github.com/ggml-org/llama.cpp/releases/tag/b10217) | DSML call parser, cache fixes |
| prices | [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing), [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) | the table in [03-ARCHITECTURE.md](03-ARCHITECTURE.md#5-costs-is-local-cheaper) |

## 7. Measurements of this machine

| Source | What I took |
|---|---|
| [local-llm-bench-results — PARALLEL.md](https://github.com/michal-koniu/local-llm-bench-results/blob/main/PARALLEL.md) | 22.6 tok/s for 1 agent, 13.6 tok/s per agent with 4 (54.3 in total); prompt reading 1,186 tok/s (1 agent) and 1,694 tok/s in total (4); optimum of 3 agents; 44 s of waiting with 4 agents at 16k tokens each; gpt-oss-20b 141 and 81 tok/s |
| [local-llm-bench-results — RESULTS.md](https://github.com/michal-koniu/local-llm-bench-results/blob/main/RESULTS.md) | hard task set: DeepSeek-V4-Flash 92 / 93, gpt-oss-20b 47 / 52 |
| this machine's llama-swap configuration | UD-IQ3_XXS quantization (104.2 GB), 512k context across 4 slots, at least 1.4 GB of free VRAM per card, card power limit of 250 W, the `gpt-oss-20b-cpu` variant |
