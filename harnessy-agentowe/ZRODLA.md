# Źródła — na czym stoi ten przegląd

**Sprawdzone 11 października 2026.** Przy każdej pozycji: co z niej wziąłem i gdzie to jest w przeglądzie.
Źródła pierwotne (dokumentacja, kod, notatki wydań, zgłoszenia na GitHubie, karty modeli) mają pierwszeństwo;
blogi i materiały marketingowe oznaczam *(blog)* albo *(marketing)*. Każdy profil w [01-PROFILE.md](01-PROFILE.md)
ma też własne linki źródłowe.

> ⚠️ **Wszystko tutaj starzeje się w tygodniach.** Liczbę z tej strony traktuj jako pomiar cudzy, z datą — do sprawdzenia
> u siebie, zanim na niej oprzesz decyzję.

---

## 1. Liczby z GitHuba

- **API GitHuba** — `GET /repos/{właściciel}/{repo}`, `GET /repos/{…}/releases/latest`,
  `GET /repos/{…}/security-advisories`, wywołane 11.10.2026 dla 218 repozytoriów.
  → gwiazdki, licencje, daty ostatnich wydań i commitów, status „archived" w [README.md](README.md) i profilach;
  liczba porad bezpieczeństwa OpenClaw (722 w 2026: 14 krytycznych, 249 wysokich, 390 średnich, 69 niskich)
  i Open WebUI (158 w 2026).
- `releases/latest` pomija wydania przedpremierowe, a w monorepozytoriach zwraca wydanie innego pakietu. Dla
  LangGraph (pakiet `langgraph`), Strands Agents (harness), Kilo Code (wtyczka JetBrains), DeepSeek Harness
  i LibreChat wersję wziąłem ze stron wydań projektu.

## 2. Harnessy z czołówki

| Harness | Źródła | Co wziąłem |
|---|---|---|
| LangGraph | [modele](https://docs.langchain.com/oss/python/langchain/models), [trwałe wykonanie](https://docs.langchain.com/oss/python/langgraph/durable-execution), [wzorce wieloagentowe](https://docs.langchain.com/oss/python/langchain/multi-agent), [#40219](https://github.com/langchain-ai/langchain/issues/40219), [#35514](https://github.com/langchain-ai/langchain/issues/35514) | konfiguracja OpenAI-compatible, tryby trwałości, pięć wzorców, błędy `reasoning_content` i strumieniowania |
| Goose | [zmienne środowiskowe](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/environment-variables.md), [subagenci](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/context-engineering/subagents.mdx), [tool shim](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/tool-shim.md), [Adversary](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/security/adversary-mode.md), [przejście do AAIF](https://github.com/aaif-goose/goose/blob/main/documentation/blog/2026-04-07-goose-moves-to-aaif/index.md), [#11142](https://github.com/aaif-goose/goose/issues/11142) | model subagentów, receptury i cron, tryby bezpieczeństwa, fundacja, znane błędy lokalnych dostawców |
| OpenHands | [lokalne modele](https://docs.openhands.dev/openhands/usage/llms/local-llms), [agenci z plików](https://github.com/OpenHands/docs/blob/main/sdk/guides/agent-file-based.mdx), [bramka OpenAI](https://github.com/OpenHands/docs/blob/main/sdk/guides/agent-server/openai-gateway.mdx), [Canvas v1.25.0](https://docs.openhands.dev/openhands/usage/agent-canvas/release-notes/v1.25.0), [#16459](https://github.com/OpenHands/OpenHands/issues/16459) | podłączenie przez LiteLLM, `model: inherit`, agent jako „model", wejście głosowe, naprawiona blokada współbieżności |
| Hermes Agent | [delegacja](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation), [dostawcy](https://hermes-agent.nousresearch.com/docs/integrations/providers), [konfiguracja](https://hermes-agent.nousresearch.com/docs/user-guide/configuration), [głos](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode), [cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron), [wydania](https://github.com/NousResearch/hermes-agent/releases) | `delegation.provider/model/base_url`, domyślnie 10 dzieci, `context_length`, STT/TTS, cron bez agenta, tempo zmian |
| Pydantic AI | [PR #4149](https://github.com/pydantic/pydantic-ai/pull/4149) (scalony 4.02.2026), [API zgodne z OpenAI](https://pydantic.dev/docs/ai/models/compatible-apis/index.md), [subagenci](https://pydantic.dev/docs/ai/harness/subagents/index.md), [wydanie v2.0.0](https://github.com/pydantic/pydantic-ai/releases/tag/v2.0.0), [#4878](https://github.com/pydantic/pydantic-ai/issues/4878) | `ConcurrencyLimiter` / `ConcurrencyLimitedModel` (sprawdzone w kodzie: `pydantic_ai/concurrency.py`), capabilities v2, heurystyki dla llama.cpp |
| Deep Agents | [przegląd](https://docs.langchain.com/oss/python/deepagents/overview), [subagenci](https://docs.langchain.com/oss/python/deepagents/subagents), [asynchroniczni subagenci](https://docs.langchain.com/oss/python/deepagents/async-subagents), [Open Deep Research — archiwum](https://github.com/langchain-ai/open_deep_research) | model per subagent, `task` równolegle, następca Open Deep Research |
| Strands Agents | [dostawca llama.cpp](https://github.com/strands-agents/harness-sdk/blob/main/strands-py/src/strands/models/llamacpp.py), [harness](https://github.com/strands-agents/harness-sdk/blob/main/site/src/content/docs/user-guide/harness/index.mdx), [BidiAgent GA](https://github.com/strands-agents/harness-sdk/blob/main/site/src/content/blog/bidi-agents-now-ga.mdx), [#4620](https://github.com/strands-agents/harness-sdk/issues/4620) | natywny `LlamaCppModel`, gotowy harness, głos tylko chmurowy, domyślne 200k kontekstu |
| OpenCode | [dostawcy](https://opencode.ai/docs/providers/), [agenci](https://opencode.ai/docs/agents/), [serwer](https://opencode.ai/docs/server/), [#7410](https://github.com/anomalyco/opencode/issues/7410), [#52462](https://github.com/anomalyco/opencode/issues/52462) | konfiguracja `@ai-sdk/openai-compatible`, model i uprawnienia per agent, blokada logowania Pro/Max (9.01.2026), błąd `function.name: null` |
| DeerFlow | [README](https://github.com/bytedance/deer-flow), [config.example.yaml](https://github.com/bytedance/deer-flow/blob/main/config.example.yaml), [#1055](https://github.com/bytedance/deer-flow/issues/1055) | przykład llama.cpp, model per subagent, zadania planowane, problemy z lokalnymi modelami |
| ZeroClaw | [dostawcy](https://github.com/zeroclaw-labs/zeroclaw/blob/master/docs/book/src/providers/configuration.md), [delegacja](https://github.com/zeroclaw-labs/zeroclaw/blob/master/docs/book/src/agents/delegation.md), [wiele modeli](https://github.com/zeroclaw-labs/zeroclaw/blob/master/docs/book/src/getting-started/multi-model-setup.md), [#10396](https://github.com/zeroclaw-labs/zeroclaw/issues/10396) | slot `llamacpp`, `native_tools`, delegacja domyślnie zabroniona, profile ryzyka |
| Microsoft Agent Framework | [dostawca OpenAI](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/openai), [checkpointy](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints), [orkiestracje](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/), [#8382](https://github.com/microsoft/agent-framework/issues/8382) | pułapka `OpenAIChatClient` = Responses API, orkiestracje, naprawa `reasoning_content` (09.2026) |
| DeepSeek Harness | [README](https://github.com/deepseek-ai/deepseek-harness/blob/main/README.md), [dostawcy](https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/user/guide/providers.md), [SAFETY.md](https://github.com/deepseek-ai/deepseek-harness/blob/main/SAFETY.md) | profil `compat`, subagenci Claude Code / Codex / ACP, domyślnie tylko odczyt, status przedpremierowy |
| Pi | [README agenta](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md), [llama.cpp](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/llama-cpp.md), [modele](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md), [bezpieczeństwo](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md) | tryb routera llama.cpp, `models.json`, wirtualne modele, brak zatwierdzeń z założenia |
| gptme | [dostawcy](https://gptme.org/docs/providers.html), [formaty narzędzi](https://github.com/gptme/gptme/blob/master/docs/tool-formats.rst), [subagenci](https://github.com/gptme/gptme/blob/master/docs/tools/subagent.rst) | `OPENAI_BASE_URL`, `--tool-format xml`, tryby izolacji subagentów |
| Moltis | [dostawcy](https://github.com/moltis-org/moltis/blob/main/docs/src/providers.md), [presety agentów](https://github.com/moltis-org/moltis/blob/main/docs/src/agent-presets.md), [głos](https://github.com/moltis-org/moltis/blob/main/docs/src/voice.md), [lokalny LLM](https://github.com/moltis-org/moltis/blob/main/docs/src/local-llm.md) | presety z modelem, `delegate_only`, lokalne STT/TTS, brak ścieżki ROCm we wbudowanym backendzie; liczba commitów — API kontrybutorów |
| QwenPaw | [modele](https://github.com/agentscope-ai/QwenPaw/blob/main/website/public/docs/models.en.md), [wielu agentów](https://github.com/agentscope-ai/QwenPaw/blob/main/website/public/docs/multi-agent.en.md), [kanały](https://github.com/agentscope-ai/QwenPaw/blob/main/website/public/docs/channels.en.md), [#7979](https://github.com/agentscope-ai/QwenPaw/issues/7979) | tryb `chat.completions`, model per agent, lista kanałów, błąd okna kontekstu |
| OpenAI Agents SDK | [modele](https://openai.github.io/openai-agents-python/models/), [wydanie v0.23.0](https://github.com/openai/openai-agents-python/releases/tag/v0.23.0), [repozytorium](https://github.com/openai/openai-agents-python) | `OpenAIChatCompletionsModel`, wyłączenie śledzenia, Claude przez LiteLLM, potok głosowy |
| n8n | [licencja](https://docs.n8n.io/n8n-community-license/sustainable-use-license), [AI Agent Tool](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolaiagent), [człowiek w pętli](https://docs.n8n.io/advanced-ai/human-in-the-loop-tools), [współbieżność](https://docs.n8n.io/hosting/scaling/concurrency-control), [porady bezpieczeństwa](https://github.com/n8n-io/n8n/security/advisories), [ostrzeżenie ACSC](https://www.cyber.gov.au/about-us/view-all-content/alerts-and-advisories/critical-unauthenticated-remote-code-execution-vulnerability-in-n8n-workflow-automation-platform), [#26639](https://github.com/n8n-io/n8n/issues/26639), [węzeł OpenAI Chat Model](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.lmchatopenai/) | warunki licencji, model per węzeł, zatwierdzenia, limit nieobejmujący podprzepływów, CVE-2026-21858 (sprawdzone w API: krytyczne, 7.01.2026; wg ACSC zdalne wykonanie kodu bez logowania), przełącznik „Use Responses API" (domyślnie Chat Completions) |
| LibreChat | [agenci](https://www.librechat.ai/docs/features/agents), [wydanie v0.8.8](https://www.librechat.ai/changelog/v0.8.8), [config v1.3.15](https://www.librechat.ai/changelog/config_v1.3.15), [wydania](https://github.com/LibreChat-AI/LibreChat/releases) | `endpoints.custom`, `includeReasoningContent`, zespoły subagentów, reguły zatwierdzeń, Scheduled Chats |
| Kilo Code | [własni subagenci](https://kilo.ai/docs/customize/custom-subagents), [CLI](https://kilo.ai/docs/code-with-ai/platforms/cli), [licencja](https://github.com/Kilo-Org/kilocode/blob/main/LICENSE), [#12773](https://github.com/Kilo-Org/kilocode/issues/12773) | model per subagent, rdzeń OpenCode, niezgodność schematów z gramatyką llama.cpp |

## 3. Zweryfikowane osobno w źródle pierwotnym

Twierdzenia, które najbardziej zmieniały ranking, sprawdziłem sam, poza agentami badawczymi:

| Twierdzenie | Źródło | Wynik |
|---|---|---|
| kompromitacja LiteLLM 1.82.7 i 1.82.8 | [BerriAI/litellm#24518](https://github.com/BerriAI/litellm/issues/24518) | potwierdzone, 24.03.2026 |
| Codex CLI usunął Chat Completions | [openai/codex — dyskusja #7782](https://github.com/openai/codex/discussions/7782) | potwierdzone: od lutego 2026 błąd przy `wire_api = "chat"` |
| prośba o lokalne modele dla subagentów Claude Code | [anthropics/claude-code#38698](https://github.com/anthropics/claude-code/issues/38698) | otwarta |
| Flowise i Roo Code zarchiwizowane | API GitHuba (`archived: true`) | potwierdzone |
| OpenBB pod nową organizacją, licencja | API GitHuba (`OpenBB-finance/OpenBB` → `openbq-org/OpenBB`) | przekierowanie potwierdzone; zmiana licencji na Apache-2.0 w V5 wg notatek wydania |
| atak na pakiety npm Mastra | [BankInfoSecurity](https://www.bankinfosecurity.com/north-korean-hackers-poison-mastra-ai-framework-a-32042) *(prasa)* | 140+ pakietów, przypisane BlueNoroff przez Microsoft |
| DeepSeek-V4-Flash: rozmiar, licencja, brak wejścia obrazów | [karta modelu](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash) | 284B / 13B aktywnych, MIT, kontekst 1M, brak wizji |
| ceny Claude | [cennik Anthropic](https://platform.claude.com/docs/en/about-claude/pricing) | Opus 5.5 4 / 20, Sonnet 5.5 2 / 10, Haiku 5.5 0,10 / 0,50 USD za mln tokenów; Batch −50% |
| OpenClaw: setki złośliwych umiejętności, wystawione instancje | [insiderllm](https://insiderllm.com/guides/openclaw-clawhub-security-alert/) *(blog)*, [porady bezpieczeństwa](https://github.com/openclaw/openclaw/security/advisories), [dokumentacja bezpieczeństwa](https://docs.openclaw.ai/gateway/security) | liczba porad potwierdzona w API; liczby z raportów branżowych (SecurityScorecard, Koi Security) tylko ze źródła wtórnego |

## 4. Klocki

| Grupa | Najważniejsze źródła | Co wziąłem |
|---|---|---|
| bramki | [llama-swap](https://github.com/mostlygeek/llama-swap), [Bifrost — wydajność i współbieżność](https://docs.getbifrost.ai/providers/performance), [Datadog Security Labs o LiteLLM](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/) | `concurrency` z kolejką, przebieg kompromitacji |
| wyszukiwanie | [SearXNG — settings.yml](https://raw.githubusercontent.com/searxng/searxng/master/searx/settings.yml), [Crawl4AI — CHANGELOG](https://raw.githubusercontent.com/unclecode/crawl4ai/main/CHANGELOG.md), [Trafilatura](https://github.com/adbar/trafilatura), [Scrapling](https://github.com/D4Vinci/Scrapling), [Playwright MCP](https://github.com/microsoft/playwright-mcp) | JSON domyślnie wyłączony, poprawki bezpieczeństwa serwera Docker, zalecenie CLI zamiast MCP |
| deep research | [Local Deep Research](https://github.com/LearningCircuit/local-deep-research), [#6820](https://github.com/LearningCircuit/local-deep-research/issues/6820), [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | subskrypcje tematów, brak limitu subagentów, BM25 zamiast embeddingów |
| ceny i zmiany | [changedetection.io](https://github.com/dgtlmoon/changedetection.io), [Huginn](https://github.com/huginn/huginn), [urlwatch](https://github.com/thp/urlwatch) | tryb ceny i dostępności, reguły AI przez llama.cpp |
| finanse | [OpenBB ODP — MCP](https://docs.openbb.co/odp/python/quickstart/mcp), [edgartools](https://github.com/dgunning/edgartools), [CCXT](https://github.com/ccxt/ccxt), [TradingAgents v0.6.0](https://github.com/TauricResearch/TradingAgents/releases/tag/v0.6.0), [yfinance](https://github.com/ranaroussi/yfinance) | dostawca per poziom (Opus `deep_think`), limity SEC, warunki danych |
| powiadomienia | [ntfy — konfiguracja](https://docs.ntfy.sh/config/), [Apprise — wydania](https://github.com/caronc/apprise/releases), [Telegram Bot API — zmiany](https://core.telegram.org/bots/api-changelog) | `upstream-base-url`, łamiące v2.0.0, nowe opcje wejścia głosowego w Bot API 10.1–10.3 |
| harmonogram | [Prefect — serwer](https://docs.prefect.io/v3/manage/server), [DBOS](https://github.com/dbos-inc/dbos-transact-py), [Temporal](https://github.com/temporalio/temporal), [timery systemd](https://github.com/systemd/systemd/blob/main/man/systemd.timer.xml) | SQLite bez Dockera, kolejki z limitem, `Persistent=true` |
| pamięć | [Cognee — dostawcy LLM](https://docs.cognee.ai/setup-configuration/llm-providers), [Cognee v1.6.0](https://github.com/topoteretes/cognee/releases/tag/v1.6.0), [Graphiti](https://github.com/getzep/graphiti), [Mem0](https://github.com/mem0ai/mem0) | tryb bez klucza chmurowego, usunięcie pamięci grafowej z Mem0 OSS |
| obserwowalność | [Phoenix — self-hosting](https://arize.com/docs/phoenix/self-hosting), [Langfuse](https://github.com/langfuse/langfuse), [OpenLIT](https://github.com/openlit/openlit), [promptfoo](https://github.com/promptfoo/promptfoo) | licencja ELv2, monitoring GPU AMD, przejęcie promptfoo przez OpenAI |
| piaskownice | [sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime), [microsandbox](https://github.com/superradcompany/microsandbox), [E2B runtime](https://github.com/e2b-dev/runtime), [Daytona](https://github.com/daytonaio/daytona) | bez Dockera, mikro-VM, zamknięcie rdzenia Daytony |
| MCP dla DevOps | [kubernetes-mcp-server — konfiguracja](https://github.com/containers/kubernetes-mcp-server/blob/main/docs/configuration.md), [mcp-grafana — wydania](https://github.com/grafana/mcp-grafana/releases), [github-mcp-server](https://github.com/github/github-mcp-server), [GitLab MCP](https://docs.gitlab.com/user/model_context_protocol/mcp_server/) | tryby tylko do odczytu, telemetria domyślna w mcp-grafana 2.0 |

## 5. Głos i obraz

| Temat | Źródła | Co wziąłem |
|---|---|---|
| Pipecat i polski | [Pipecat](https://github.com/pipecat-ai/pipecat), [Smart Turn](https://github.com/pipecat-ai/smart-turn), [LiveKit Agents](https://github.com/livekit/agents) | Smart Turn obsługuje polski (94,47% wg ogłoszenia v3.0 *(blog)*), detektory LiveKit — nie |
| STT po polsku | [whisper.cpp](https://github.com/ggml-org/whisper.cpp), [Parakeet-TDT-0.6B-v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3), [Canary-1B-v2](https://huggingface.co/nvidia/canary-1b-v2), [Qwen3-ASR](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) | WER na FLEURS-pl: Whisper large-v3 4,74%, Canary 6,64%, Parakeet 7,31% (tabela NVIDII) |
| TTS po polsku | [Piper](https://github.com/OHF-Voice/piper1-gpl), [Chatterbox](https://github.com/resemble-ai/chatterbox), [VoxCPM](https://github.com/OpenBMB/VoxCPM), [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M), [F5-TTS](https://github.com/SWivid/F5-TTS) | które mają polski i jaką licencję; znak wodny Chatterboxa; F5 wymaga ROCm 7.x na RDNA4 |
| mowa-do-mowy | [Moshi](https://github.com/kyutai-labs/moshi), [Unmute](https://github.com/kyutai-labs/unmute) | brak polskiego, brak ścieżki ROCm |
| DeepSeek i wizja | [DeepSeek-V4-Flash-Vision-Exp](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp), [llama.cpp b10766](https://github.com/ggml-org/llama.cpp/releases/tag/b10766), [#28939](https://github.com/ggml-org/llama.cpp/issues/28939), [multimodal w llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/docs/multimodal.md) | wariant z wizją, minimalna wersja llama.cpp |
| modele wizyjne i OCR | [Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B), [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), [Holo4-35B-A3B](https://huggingface.co/Hcompany/Holo4-35B-A3B), [Docling](https://github.com/docling-project/docling), [PaddleOCR-VL-1.5](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5) | rozmiary, licencje, wsparcie llama.cpp |
| generowanie obrazów | [ComfyUI](https://github.com/comfyanonymous/ComfyUI), [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp), [Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511), [Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo), [FLUX.2 klein 4B](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B) | modele na Apache-2.0 vs niekomercyjne |

## 6. Hybryda, routing i koszty

| Temat | Źródła | Co wziąłem |
|---|---|---|
| planista + wykonawca w kodowaniu | [Aider: architect/editor](https://aider.chat/2024/09/26/architect.html) | 80,5% i 78,9% z DeepSeekiem jako edytorem |
| chmura dzieli, lokalny przerabia | [Minions — arXiv 2502.15964](https://arxiv.org/abs/2502.15964), [repozytorium](https://github.com/HazyResearch/minions) | 5,7× niższy koszt przy 97,9% jakości |
| routing urządzenie / chmura | [Hera — arXiv 2605.24598](https://arxiv.org/abs/2605.24598) | 92,5% skuteczności przy chmurze w 46,3% kroków |
| koszt samych lokalnych modeli | [OpenJarvis — arXiv 2605.17172](https://arxiv.org/abs/2605.17172) | −25 do −39 pp po zamianie Opusa na mały model |
| advisor tool | [The advisor strategy](https://claude.com/blog/the-advisor-strategy) *(producent)* | +2,7 pp przy 11,9% niższym koszcie; tylko modele Claude |
| Claude Code i lokalne modele | [subagenci Claude Code](https://code.claude.com/docs/en/sub-agents), [bramki LLM](https://code.claude.com/docs/en/llm-gateway), [własne narzędzia w Agent SDK](https://code.claude.com/docs/en/agent-sdk/custom-tools) | brak wsparcia lokalnych modeli dla subagentów; wzorzec „lokalny agent jako narzędzie" |
| serwery MCP delegujące do lokalnych modeli | [mcp-llama-swap](https://github.com/oussama-kh/mcp-llama-swap), [PAL](https://github.com/BeehiveInnovations/pal-mcp-server) | Claude zostaje orkiestratorem |
| Goose lead/worker | [multi-model w Goose](https://goose-docs.ai/docs/guides/multi-model/) | tryb usunięty, została jawna delegacja |
| DeepSeek w llama.cpp | [#29008 — prompt cache w pętlach](https://github.com/ggml-org/llama.cpp/pull/29008), [#26398](https://github.com/ggml-org/llama.cpp/pull/26398), [#26269](https://github.com/ggml-org/llama.cpp/pull/26269), [b10217](https://github.com/ggml-org/llama.cpp/releases/tag/b10217) | parser wywołań DSML, poprawki cache |
| ceny | [cennik Anthropic](https://platform.claude.com/docs/en/about-claude/pricing), [cennik DeepSeek](https://api-docs.deepseek.com/quick_start/pricing) | tabela w [03-ARCHITEKTURA.md](03-ARCHITEKTURA.md#5-koszty-czy-lokalnie-jest-taniej) |

## 7. Pomiary tej maszyny

| Źródło | Co wziąłem |
|---|---|
| [local-llm-bench-results — PARALLEL.md](https://github.com/michal-konik-human/local-llm-bench-results/blob/main/PARALLEL.md) | 22,6 tok/s dla 1 agenta, 13,6 tok/s na agenta przy 4 (54,3 łącznie); czytanie promptu 1 186 tok/s (1 agent) i 1 694 tok/s łącznie (4); optimum 3 agentów; 44 s oczekiwania przy 4 agentach po 16 tys. tokenów; gpt-oss-20b 141 i 81 tok/s |
| [local-llm-bench-results — RESULTS.md](https://github.com/michal-konik-human/local-llm-bench-results/blob/main/RESULTS.md) | trudny zestaw zadań: DeepSeek-V4-Flash 92 / 93, gpt-oss-20b 47 / 52 |
| konfiguracja llama-swap tej maszyny | kwantyzacja UD-IQ3_XXS (104,2 GB), kontekst 512k na 4 sloty, co najmniej 1,4 GB wolnego VRAM na kartę, limit mocy kart 250 W, wariant `gpt-oss-20b-cpu` |
