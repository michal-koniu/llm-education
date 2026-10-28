# Profile harnessów — 20 najlepszych i reszta stawki

**Stan na 11 października 2026.** Liczby z GitHuba (gwiazdki, wydania) pobrane z API tego dnia.
Wszystkie fakty pochodzą z dokumentacji, kodu, notatek wydań i zgłoszeń — źródła przy każdym profilu
i w [ZRODLA.md](ZRODLA.md). **Żadnego z tych harnessów nie testowałem na swojej maszynie** — to przegląd
dokumentacji, nie pomiar. Ranking i wagi: [README.md](README.md#jak-liczyłem-ranking).

Legenda wyniku: A — wielu agentów i hybryda (25%), B — jakość obsługi lokalnego modelu (20%),
C — pokrycie pięciu zastosowań (20%), D — dojrzałość (15%), E — wartość do nauki (10%),
F — bezpieczeństwo i kontrola (10%). Każde kryterium 1–5, wynik 0–100.

---

## Spis treści

- [Siedem pułapek wspólnych dla wszystkich](#siedem-pułapek-wspólnych-dla-wszystkich)
- Profile: [1. LangGraph](#1-langgraph) · [2. Goose](#2-goose) · [3. OpenHands](#3-openhands) ·
  [4. Hermes Agent](#4-hermes-agent) · [5. Pydantic AI](#5-pydantic-ai) · [6. Deep Agents](#6-deep-agents) ·
  [7. Strands Agents](#7-strands-agents) · [8. OpenCode](#8-opencode) · [9. DeerFlow](#9-deerflow) ·
  [10. ZeroClaw](#10-zeroclaw) · [11. Microsoft Agent Framework](#11-microsoft-agent-framework) ·
  [12. DeepSeek Harness](#12-deepseek-harness) · [13. Pi](#13-pi) · [14. gptme](#14-gptme) ·
  [15. Moltis](#15-moltis) · [16. QwenPaw](#16-qwenpaw) · [17. OpenAI Agents SDK](#17-openai-agents-sdk) ·
  [18. n8n](#18-n8n) · [19. LibreChat](#19-librechat) · [20. Kilo Code](#20-kilo-code)
- [Pozostali kandydaci (miejsca 21–64)](#pozostali-kandydaci-miejsca-2164)
- [Wykluczeni na wejściu](#wykluczeni-na-wejściu)
- [Poza rankingiem](#poza-rankingiem)

---

## Siedem pułapek wspólnych dla wszystkich

Te same problemy wracają w niemal każdym harnessie podłączonym do llama.cpp / llama-swap. Sprawdź je,
zanim uznasz, że „harness X nie działa z lokalnym modelem".

| # | Pułapka | Objaw | Co zrobić |
|---|---|---|---|
| H1 | **Responses API zamiast Chat Completions.** Coraz więcej narzędzi domyślnie woła `/v1/responses` (OpenAI Agents SDK, Microsoft Agent Framework — `OpenAIChatClient`, n8n — przełącznik w węźle, Windmill — dostawca OpenAI). Codex CLI od lutego 2026 obsługuje **tylko** Responses API. | błąd 400/404, „type must be output_text" | wybierz tryb `chat_completions` / dostawcę „OpenAI-compatible"; dla Codex CLI — inny harness |
| H2 | **`reasoning_content` DeepSeeka przy wywołaniach narzędzi.** W trybie myślenia DeepSeek V4 wymaga odesłania treści rozumowania w turach z narzędziami. Gubiły ją LangChain (#40219, otwarte), Microsoft Agent Framework (naprawione 09.2026), Pydantic AI (naprawione w v2). | błąd 400 przy drugiej turze z narzędziem | aktualna wersja frameworka; w LibreChat `includeReasoningContent: true`; albo wyłącz myślenie dla wykonawców |
| H3 | **Okno kontekstu zgadywane z nazwy modelu.** Harness bierze limit z katalogu chmurowego albo domyślne 128K/200K zamiast z serwera (z llama.cpp: QwenPaw #7979, LibreChat #14228; z własnym dostawcą OpenAI-compatible: Goose #12048; z Ollamą: Strands #4620; domyślne 128K w Hermesie). | kompakcja nie odpala albo odpala za wcześnie, ucięte odpowiedzi | ustaw jawnie `131072` (Twój slot) w konfiguracji modelu |
| H4 | **Zmienny początek promptu zabija prompt cache.** Znacznik czasu albo losowa kolejność narzędzi w prompcie systemowym unieważnia cache serwera w każdej turze (z llama.cpp: OpenClaw, LibreChat #16877; z Ollamą i innymi lokalnymi serwerami: nanobot #4867). | każda tura czyta cały kontekst od nowa — przy około 1 200 tok/s czytania promptu to dziesiątki sekund na turę | stały prefiks: data w wiadomości użytkownika, nie w systemie; sprawdzaj `cache_n` w logach llama-server |
| H5 | **Za dużo narzędzi naraz.** Lokalne modele tracą jakość przy długich listach narzędzi i schematów MCP. | wybór złego narzędzia, pętle | 5–15 narzędzi na wykonawcę; 2–3 serwery MCP, nie dziesięć |
| H6 | **Brak limitu współbieżności na endpoint.** Masz 4 sloty. Prawie wszystkie frameworki limitują równoległość w obrębie jednego uruchomienia, nie globalnie (wyjątek: Pydantic AI). | kolejka w llama-server rośnie, timeouty | jeden limit 4 w jednym miejscu, z kolejką: bramka (Bifrost), `ConcurrencyLimiter` albo kolejka zadań. Uwaga: `concurrencyLimit` w llama-swap nie kolejkuje — nadmiarowe zapytanie dostaje od razu 429 |
| H7 | **Schematy narzędzi, których gramatyka llama.cpp nie przyjmuje.** Np. `pattern` bez `^…$` (Kilo #12773, llama-server), regresje schematów w Qwen Code (#10435 i kolejne). Pokrewny przypadek z Ollamą: zmiana składni narzędzi w Cline 4.1 (#13008). | „Unable to generate parser for this template" (Kilo #12408) | przypinaj wersje harnessu, testuj po aktualizacji (promptfoo — patrz [02-KLOCKI.md](02-KLOCKI.md)) |

---

## 1. LangGraph

**Kategoria:** framework Python (graf stanów) · **Licencja:** MIT · ⭐ 43,1k · **Wydanie:** langgraph 1.2.14 (6.10.2026) ·
**Wynik: 86** (A5 B4 C4 D5 E3 F4)

**Czym jest.** Środowisko uruchomieniowe, w którym agent to graf: węzły to funkcje albo agenci, krawędzie
to logika przejść, a każdy krok można zapisać (checkpoint), przerwać, wznowić i odtworzyć. Na nim stoją
`create_agent` z LangChain v1 i Deep Agents (nr 6).

**Przewaga.** Najdojrzalszy w Pythonie model trwałości: checkpointy per wątek, trzy tryby zapisu
(`exit` / `async` / `sync`), cofanie w czasie, `interrupt()` dla człowieka w pętli, które przeżywa restart
procesu, rozgałęzianie `Send` i podgrafy.

**Lokalny model.**
```python
from langchain.chat_models import init_chat_model
local = init_chat_model("deepseek-v4-flash", model_provider="openai",
                        base_url="http://localhost:8080/v1", api_key="none")   # adres Twojego llama-swap
```
llama-server musi działać z szablonem obsługującym narzędzia (`--jinja`).

**Wielu agentów i hybryda.** Dokumentacja opisuje pięć wzorców: subagenci jako narzędzia, przekazania,
umiejętności, router, własny graf. Każdy węzeł ma własny model, więc planista na
`anthropic:claude-opus-5-5` i wykonawcy na llama-swap to zwykła konfiguracja. `max_concurrency` limituje
równoległość w obrębie jednego uruchomienia — globalny limit 4 zapytań trzeba dodać samemu (pułapka H6).

**Głos i obraz.** Brak głosu w czasie rzeczywistym; oficjalny przewodnik proponuje „kanapkę"
STT → agent → TTS. Obrazy przechodzą jako bloki multimodalne do modelu z wizją.

**Bezpieczeństwo.** Brak wbudowanej piaskownicy (dają ją Deep Agents). Middleware z limitami wywołań modelu
i narzędzi, wykrywaniem PII i człowiekiem w pętli; otwarte zgłoszenia o brakujących hakach przed wykonaniem
narzędzia (#8817, #8818).

**Słabe strony.** Warstwy LangChain to miejsce, gdzie psują się lokalne modele: gubienie
`reasoning_content` (#40219, otwarte), rozbite argumenty narzędzi w strumieniu (#35514). Serwer z cronem
w wersji self-hosted to płatny dodatek LangSmith. `langgraph-supervisor` zarchiwizowano w 2026 —
zamiast niego wzorzec „supervisor przez wywołania narzędzi".

**Co warto ukraść.** Checkpointy na `thread_id` z wybieralną trwałością; `interrupt()` + `Command(resume=…)`
jako mechanizm pytania człowieka; mały słownik decyzji człowieka (zatwierdź / edytuj / odrzuć / odpowiedz);
lista wbudowanych middleware (retry, fallback modelu, limity wywołań, wykrywanie PII) jako checklista tego,
co każdy harness musi mieć.

**Źródła:** [repozytorium](https://github.com/langchain-ai/langgraph) ·
[modele](https://docs.langchain.com/oss/python/langchain/models) ·
[trwałe wykonanie](https://docs.langchain.com/oss/python/langgraph/durable-execution) ·
[wzorce wieloagentowe](https://docs.langchain.com/oss/python/langchain/multi-agent) ·
[#40219](https://github.com/langchain-ai/langchain/issues/40219)

---

## 2. Goose

**Kategoria:** agent ogólnego przeznaczenia (CLI, desktop, serwer) · **Licencja:** Apache-2.0 · ⭐ 55,1k ·
**Wydanie:** v1.54.0 (8.10.2026) · **Wynik: 84** (A5 B4 C4 D5 E3 F3)

**Czym jest.** Agent w Ruście stworzony przez Block, od 7.04.2026 pod Agentic AI Foundation (Linux Foundation),
obok MCP i AGENTS.md. Ma CLI, aplikację desktop i serwer ACP; repozytorium przeniesiono do `aaif-goose/goose`.

**Przewaga.** Najszerszy zestaw „poza kodowaniem": receptury YAML (*recipes*) jako jednostka powtarzalnej pracy,
wbudowany harmonogram cron, subagenci z własnym dostawcą i modelem, *tool shim* dla modeli, które słabo wołają
narzędzia (eksperymentalny: osobny model-tłumacz działa domyślnie przez Ollamę albo przez wbudowany llama.cpp Goose'a,
więc z samym llama-swap go nie użyjesz — DeepSeek i tak ma natywne wywołania narzędzi), bramka Telegram, dyktowanie głosem (także lokalnym Whisperem), tryb Adversary — osobny model recenzuje
każde wywołanie narzędzia. Neutralne zarządzanie przez fundację.

**Lokalny model.** Plik dostawcy w `~/.config/goose/custom_providers/` z `"engine": "openai"`,
`"base_url": "http://localhost:8080/v1/chat/completions"` i `context_limit` per model. Dokumentacja uczciwie
pisze, że Goose „najlepiej działa z modelami Claude". Znane błędy: modele rozumujące zwracają pustą treść,
bo `max_tokens` jest dzielone między rozumowanie i odpowiedź (#11142); ignorowane okno kontekstu (#12048).

**Wielu agentów i hybryda.** `GOOSE_SUBAGENT_PROVIDER` / `GOOSE_SUBAGENT_MODEL` ustawiają model wykonawców,
a receptura może go nadpisać (`settings.goose_provider` / `goose_model`). Główna sesja na Anthropic, wykonawcy
na llama-swap — wspierane. Subagenci działają tylko w trybie autonomicznym.

**Głos i obraz.** Dyktowanie w aplikacji desktop (dostawcy chmurowi albo lokalny Whisper), bez syntezy mowy.
Obrazy, gdy model ma wizję; dla własnego endpointu trzeba włączyć `supports_vision` per model (#11998).

**Bezpieczeństwo.** Tryby `GOOSE_MODE` (auto, approve, smart_approve, chat), uprawnienia per narzędzie,
wykrywanie prompt injection, tryb Adversary, haki przed wywołaniem narzędzia.

**Harmonogram i tryb bezgłowy.** `goose schedule add --cron … --recipe-source …`, `goose run -t "…"`,
`goose serve` (serwer ACP z TLS).

**Słabe strony.** Eksperymentalną piaskownicę macOS usunięto — narzędzia działają z Twoimi uprawnieniami.
Tryb Adversary jest *fail-open* (gdy recenzent zawiedzie, akcja przechodzi). Architektura w przebudowie (2.0, ACP).

**Co warto ukraść.** Receptura jako jednostka pracy z parametrami, rozszerzeniami i modelem; *tool shim* — tani
model tłumaczy tekstowe wywołania narzędzi na strukturalne; recenzent-LLM bramkujący wywołania; parowanie
Telegrama jednorazowym kodem.

**Źródła:** [zmienne środowiskowe](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/environment-variables.md) ·
[subagenci](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/context-engineering/subagents.mdx) ·
[tool shim](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/tool-shim.md) ·
[Adversary](https://github.com/aaif-goose/goose/blob/main/documentation/docs/guides/security/adversary-mode.md) ·
[przeniesienie do AAIF](https://github.com/aaif-goose/goose/blob/main/documentation/blog/2026-04-07-goose-moves-to-aaif/index.md)

---

## 3. OpenHands

**Kategoria:** platforma agentów kodujących + SDK · **Licencja:** MIT · ⭐ 90,5k · **Wydanie:** v1.26.0 (8.10.2026) ·
**Wynik: 84** (A5 B4 C3 D5 E3 F5)

**Czym jest.** Platforma, której front „Agent Canvas" (2026) uruchamia OpenHands — albo Claude Code, Codex, Pi,
OpenCode przez ACP — lokalnie, w Dockerze, na VM albo w Kubernetesie. Pod spodem Software Agent SDK (Python)
i Agent Server (REST / WebSocket).

**Przewaga.** Najpełniejszy stos do osadzenia we własnej aplikacji: SDK + serwer z OpenAPI, kontener na każdą
rozmowę, subagenci z plików Markdown z polem `model:`, routery modeli, OpenTelemetry, automatyzacje (cron, webhook,
zdarzenia) i bramka OpenAI-compatible, która wystawia **całego agenta jako „model"**.

**Lokalny model.** Przez LiteLLM: model `openai/deepseek-v4-flash` + `base_url` llama-swap. W 2026 naprawiono
dwa błędy ważne dla Ciebie: globalna blokada serializowała wszystkie wywołania LLM między rozmowami — marnując
równoległe sloty (#16459), a błędne wywołanie narzędzia w historii blokowało llama-server (sdk#2887).

**Wielu agentów i hybryda.** Agenci z plików mają `model: inherit` albo nazwany profil LLM — orkiestrator na Claude,
subagenci na profilu lokalnym. `route_task_to_model` przełącza profil w trakcie rozmowy, MultimodalRouter wysyła
obrazy do modelu z wizją, a tekst do tańszego.

**Głos i obraz.** Canvas v1.25.0 (6.10.2026) dodał wejście głosowe: rozpoznawanie w przeglądarce albo dowolny
endpoint transkrypcji OpenAI-compatible (np. lokalny Whisper). Obrazy na wejściu i zrzuty ekranu z przeglądarki.

**Bezpieczeństwo.** Kontener na rozmowę, backendy VM / K8s, polityki potwierdzeń i analizator ryzyka.
Uwaga: tryb bezgłowy CLI zawsze zatwierdza wszystko, a instalacja bez Dockera ma pełny dostęp do dysku.

**Słabe strony.** Ciężki i szybko zmieniający się (V0 → SDK V1 → Agent Canvas; samodzielne CLI zepchnięte na bok).

**Co warto ukraść.** Agent jako „model" za bramką OpenAI — każdy klient, także platforma głosowa, może zawołać
całego agenta; subagenci w Markdown z `model: inherit | <profil>`; kontener na rozmowę; specyfikacja automatyzacji
(wyzwalacz, harmonogram, model, powiadomienia) jako plik JSON w repozytorium.

**Źródła:** [lokalne modele](https://docs.openhands.dev/openhands/usage/llms/local-llms) ·
[agenci z plików](https://github.com/OpenHands/docs/blob/main/sdk/guides/agent-file-based.mdx) ·
[bramka OpenAI](https://github.com/OpenHands/docs/blob/main/sdk/guides/agent-server/openai-gateway.mdx) ·
[#16459](https://github.com/OpenHands/OpenHands/issues/16459)

---

## 4. Hermes Agent

**Kategoria:** osobisty agent zawsze włączony · **Licencja:** MIT · ⭐ 252,7k · **Wydanie:** v0.21.6 (8.10.2026) ·
**Wynik: 81** (A5 B4 C4 D4 E2 F4)

**Czym jest.** Agent Nous Research z pętlą uczenia: sam pisze i poprawia swoje umiejętności (*skills*), dba o pamięć
i przeszukuje dawne sesje. Działa na terminalu lokalnym, w Dockerze, przez SSH albo w chmurowej piaskownicy;
odpowiada z 25+ komunikatorów (Telegram, Signal, WhatsApp, Discord, e-mail, Matrix i inne).

**Przewaga.** Wzorzec „planista z czołówki, tani wykonawcy" jest wpisany w konfigurację; najmocniejszy cron w swojej
kategorii (strażnicy bez agenta, ciągłość między uruchomieniami, deduplikacja incydentów); głos w CLI i komunikatorach.

**Lokalny model.**
```yaml
model:
  provider: custom
  base_url: http://localhost:8080/v1
  default: deepseek-v4-flash
  context_length: 131072      # ustaw jawnie — autodetekcja spada do 128K
```
Wbudowany runtime na AMD wybiera Vulkan — na R9700 zostań przy własnym llama-swap.

**Wielu agentów i hybryda.** Model główny na Anthropic (Opus 5.5 jest w katalogu), wykonawcy przez
`delegation: {provider, model, base_url}`. `delegation.max_concurrent_children` ma domyślnie 10 — zmniejsz do 4.
Zadania poboczne (wizja, kompresja, recenzja w tle) mają osobne modele; recenzję w tle przekieruj,
bo inaczej podwaja obciążenie slotów.

**Głos i obraz.** Push-to-talk w CLI, odpowiedzi głosowe na Telegramie i Discordzie. STT: lokalny faster-whisper
(język: `stt.local.language`). TTS: domyślnie Edge TTS — darmowa usługa w chmurze Microsoftu, z polskimi głosami;
do tego ElevenLabs, OpenAI albo lokalny NeuTTS (polski niepotwierdzony w dokumentacji). Czyli: rozpoznawanie mowy
lokalnie, synteza domyślnie w chmurze. Od v0.20 strumieniowanie z przerywaniem w pół zdania. Obrazy trafiają natywnie do modelu z wizją; dla tekstowego DeepSeeka opis robi
narzędzie `vision_analyze` z osobnym modelem wizyjnym.

**Bezpieczeństwo.** „Smart approvals" (pomocniczy LLM ocenia oznaczone komendy) plus twarda lista zakazów,
Docker bez uprawnień, usuwanie sekretów ze środowiska narzędzi, parowanie rozmów jednorazowym kodem.

**Słabe strony.** Ogromne tempo zmian (około 2100 PR między dwiema kolejnymi wersjami) — przypinaj wersje.
Repozytorium ma około 18 tys. plików, więc do nauki się nie nadaje. Uszkodzenia bazy stanu wymagały
osobnego wydania naprawczego. Płatny portal Nous promowany przy instalacji.

**Co warto ukraść.** Delegacja z `output_schema` i jedną turą naprawy; wykrywanie zawieszenia po braku postępu,
nie po zegarze; zamrożona migawka pamięci na sesję (stały prefiks = działający prompt cache); strażnicy cron
„bez agenta", którzy alarmują tylko przy niepustym wyniku; filtr halucynacji Whispera.

**Źródła:** [delegacja](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation) ·
[dostawcy](https://hermes-agent.nousresearch.com/docs/integrations/providers) ·
[głos](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode) ·
[cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) ·
[wydania](https://github.com/NousResearch/hermes-agent/releases)

---

## 5. Pydantic AI

**Kategoria:** framework Python (typowany) · **Licencja:** MIT · ⭐ 20,5k · **Wydanie:** v2.55.0 (9.10.2026) ·
**Wynik: 81** (A5 B4 C4 D4 E3 F3)

**Czym jest.** Framework od twórców Pydantic. Agent prowadzi walidowaną pętlę narzędzi i wyników; od v2 (23.06.2026)
„capabilities" łączą narzędzia, haki i ustawienia w moduły: subagenci, planowanie, pamięć, kompakcja, code mode,
głos w czasie rzeczywistym, trwałe wykonanie.

**Przewaga.** Najlepsze wyjście strukturalne (tryby tool / native / prompted z walidacją i ponowieniami) i — jako
jedyny sprawdzony framework — **współdzielony limiter współbieżności na model**. To dokładnie Twoje 4 sloty.
Trwałe wykonanie przez Temporal, DBOS, Prefect albo Restate.

**Lokalny model i limit 4 slotów.**
```python
from pydantic_ai import Agent, ConcurrencyLimitedModel, ConcurrencyLimiter
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

local = OpenAIProvider(base_url="http://localhost:8080/v1", api_key="none")
pool = ConcurrencyLimiter(max_running=4, name="llama-swap")          # 4 sloty, wspólne dla modeli
ds = ConcurrencyLimitedModel(OpenAIChatModel("deepseek-v4-flash", provider=local), limiter=pool)
worker = Agent(ds, name="worker")
planner = Agent("anthropic:claude-opus-5-5")
```
Uwaga: agent zagnieżdżony w narzędziu też zajmuje slot — licz pulę dla rodzica i dziecka.

**Wielu agentów i hybryda.** Delegacja przez narzędzia, przekazania w kodzie, grafy (`pydantic_graph`);
moduł subagentów daje orkiestratorowi menu modeli (`SubAgents(models={…})`), budżety, timeouty i `max_depth`.

**Głos i obraz.** `agent.realtime(...)` działa tylko z chmurowymi modelami (OpenAI Realtime, Gemini Live, xAI);
lokalnie zostaje kaskada STT → agent → TTS, którą składasz sam. Obrazy i dokumenty na wejściu.

**Bezpieczeństwo.** Narzędzia wymagające zatwierdzenia (*deferred tools*), limity użycia i budżety per delegacja.
Powłoka w module Coder jest nieograniczona — piaskownicę dodajesz sam.

**Słabe strony.** Heurystyki dla serwerów OpenAI-compatible (włączanie myślenia po pierwszym znaku nazwy modelu,
#4878); bardzo szybkie wydania i łamiąca migracja v2; ogromne pliki rdzenia.

**Co warto ukraść.** Opakowanie modelu wymuszające nazwaną, współdzieloną pulę — z głębokością kolejki widoczną
w śladach; tryby wyjścia wybierane według profilu modelu; budżety per delegacja z miękką i twardą porażką.

**Źródła:** [PR #4149 — limit współbieżności](https://github.com/pydantic/pydantic-ai/pull/4149) ·
[API zgodne z OpenAI](https://pydantic.dev/docs/ai/models/compatible-apis/index.md) ·
[subagenci](https://pydantic.dev/docs/ai/harness/subagents/index.md) ·
[#4878](https://github.com/pydantic/pydantic-ai/issues/4878)

---

## 6. Deep Agents

**Kategoria:** harness na LangGraph (w stylu Claude Code) · **Licencja:** MIT · ⭐ 30,1k ·
**Wydanie:** deepagents 0.7.23 (7.10.2026) · **Wynik: 81** (A5 B4 C3 D4 E4 F4)

**Czym jest.** „Agent harness z bateriami" od LangChain: `create_deep_agent()` daje planowanie (lista zadań),
system plików (wirtualny albo prawdziwy), subagentów z izolowanym kontekstem, kompakcję i odkładanie dużych wyników
do plików, umiejętności, pamięć w AGENTS.md i człowieka w pętli. Do tego terminalowy agent `dcode`.
Następca zarchiwizowanego (08.2026) Open Deep Research.

**Przewaga.** Gotowy przepis na „głębokiego agenta" postawiony na trwałości LangGraph, z wymiennymi backendami
(stan, lokalny system plików, magazyn LangGraph, zdalne piaskownice).

**Lokalny model.** Dowolny model LangChain, np. `ChatOpenAI(base_url="http://localhost:8080/v1", api_key="none")`.
Dziedziczy błędy LangChain z modelami lokalnymi (pułapka H2).

**Wielu agentów i hybryda.** Główny agent `model=ChatAnthropic(...)`, subagenci
`{"name": "researcher", "model": ChatOpenAI(base_url=...)}`. Kilka wywołań `task` w jednej turze to równoległość;
asynchroniczni subagenci (start / check / update / cancel) działają w tle na serwerze.

**Głos i obraz.** Brak głosu; obrazy jako wiadomości multimodalne LangChain.

**Bezpieczeństwo.** Backendy piaskownic (Modal, Runloop, własne), reguły uprawnień do plików,
`interrupt_on` per narzędzie.

**Słabe strony.** Wersje 0.x z dziesiątkami wydań; brak limitu współbieżności dla równoległych `task`; bez głosu.

**Co warto ukraść.** System plików jako notatnik agenta i odkładanie dużych wyników narzędzi do plików zamiast
do kontekstu; narzędzie `task` ze świeżym kontekstem; zestaw narzędzi do sterowania subagentami w tle.

**Źródła:** [przegląd](https://docs.langchain.com/oss/python/deepagents/overview) ·
[subagenci](https://docs.langchain.com/oss/python/deepagents/subagents) ·
[subagenci asynchroniczni](https://docs.langchain.com/oss/python/deepagents/async-subagents) ·
[repozytorium](https://github.com/langchain-ai/deepagents)

---

## 7. Strands Agents

**Kategoria:** SDK Python/TS + gotowy harness (AWS) · **Licencja:** Apache-2.0 · ⭐ 8,8k ·
**Wydanie:** harness 0.2.0 (8.10.2026) · **Wynik: 80** (A4 B5 C4 D4 E3 F3)

**Czym jest.** SDK od AWS, w którym model prowadzi prostą pętlę (narzędzia, haki, przerwania, sterowanie, sesje,
wzorce wieloagentowe), plus `create_harness()` — złożony agent z domyślnymi narzędziami (powłoka, pliki, sieć,
lista zadań, subagenci, checkpointy, pamięć). Repozytorium przemianowano na `harness-sdk`.

**Przewaga.** **Natywny dostawca `LlamaCppModel`**, który wykorzystuje funkcje llama.cpp (gramatyki, zaawansowane
próbkowanie, `cache_prompt`), zamiast traktować serwer jak „kolejne OpenAI". Do tego routing modeli (klasyfikator,
fallback) i OpenTelemetry domyślnie.

**Lokalny model.** `LlamaCppModel(base_url="http://localhost:8080", model_id="deepseek-v4-flash")`.
Znane: modele bez wpisu w tabeli okien kontekstu dostają domyślnie 200k (#4620, pułapka H3).

**Wielu agentów i hybryda.** `Agent(model=AnthropicModel(model_id="claude-opus-5-5"), tools=[worker_tool])`
orkiestruje wykonawców na `LlamaCppModel`; wzorce agents-as-tools, Swarm, Graph, A2A.

**Głos i obraz.** `BidiAgent` (GA 5.10.2026) — tylko modele chmurowe (Nova Sonic, OpenAI Realtime, Gemini Live).
Obrazy jako bloki treści.

**Bezpieczeństwo.** Moduł `sandbox`, guardrails, interwencje i sterowanie (*steering*) w pętli.

**Słabe strony.** Domyślne ustawienia pod AWS / Bedrock; limit współbieżności w Pythonie dopiero w PR (#3156);
około 40 wydań w 2026.

**Co warto ukraść.** Dostawca wykorzystujący gramatyki i `cache_prompt` llama.cpp; routing tanie / drogie
klasyfikatorem; śledzenie każdej decyzji pętli domyślnie.

**Źródła:** [dostawca llama.cpp](https://github.com/strands-agents/harness-sdk/blob/main/strands-py/src/strands/models/llamacpp.py) ·
[harness](https://github.com/strands-agents/harness-sdk/blob/main/site/src/content/docs/user-guide/harness/index.mdx) ·
[wzorce wieloagentowe](https://github.com/strands-agents/harness-sdk/tree/main/strands-py/src/strands/multiagent) ·
[#4620](https://github.com/strands-agents/harness-sdk/issues/4620)

---

## 8. OpenCode

**Kategoria:** agent kodujący (TUI, desktop, serwer HTTP) · **Licencja:** MIT · ⭐ 212,6k ·
**Wydanie:** v1.19.0 (11.10.2026) · **Wynik: 80** (A5 B4 C3 D5 E3 F3)

**Czym jest.** Agent kodujący od byłego zespołu SST (Anomaly Innovations); repozytorium przeniesiono z `sst/opencode`
do `anomalyco/opencode`. TUI jest tylko jednym z klientów serwera `opencode serve`.

**Przewaga.** Architektura klient–serwer (OpenAPI 3.1 + zdarzenia SSE, SDK w JS) i pierwszorzędni agenci oraz
subagenci z własnym modelem i uprawnieniami. Podłączenie llama-server jest proste i opisane w dokumentacji.

**Lokalny model** (`opencode.json`):
```json
"provider": {
  "llama": {
    "npm": "@ai-sdk/openai-compatible",
    "options": { "baseURL": "http://localhost:8080/v1" },
    "models": { "deepseek-v4-flash": { "limit": { "context": 131072, "output": 16384 } } }
  }
}
```
Znany błąd: dołączona biblioteka przerywa turę, gdy strumień niesie `function.name: null` (#52462).

**Wielu agentów i hybryda.** Agent `plan` / `build` na `anthropic/claude-opus-5-5`, subagenci na
`llama/deepseek-v4-flash` — model ustawiany per agent. Od 9.01.2026 Anthropic blokuje logowanie subskrypcją
Pro/Max w narzędziach firm trzecich — potrzebny klucz API.

**Głos i obraz.** Brak własnego głosu (prośba #33300; tylko wtyczki społeczności). Załączniki obrazów są
skalowane przed wysłaniem i działają z modelem, który ma wizję.

**Bezpieczeństwo.** Reguły `allow` / `ask` / `deny` z wzorcami, np.
`"bash": {"kubectl get *": "allow", "rm *": "deny"}`. Brak piaskownicy systemowej; zgłoszono obejścia
reguły `external_directory`.

**Słabe strony.** Szybkie zmiany i łamiące API serwera V2 (źle dla osadzania teraz); wycieki pamięci w trybie
serwera; brak głosu.

**Co warto ukraść.** Bezgłowy serwer z OpenAPI jako rdzeń, a każde UI jako klient; agenci jako pliki Markdown
z `model` / `permission` / `steps`; `permission.task` — które subagenty wolno wołać; hak przepisujący opisy
narzędzi per model (obejście problemów z gramatyką llama.cpp).

**Źródła:** [dostawcy](https://opencode.ai/docs/providers/) · [agenci](https://opencode.ai/docs/agents/) ·
[serwer](https://opencode.ai/docs/server/) · [#52462](https://github.com/anomalyco/opencode/issues/52462)

---

## 9. DeerFlow

**Kategoria:** „super-agent" do długich zadań (badania, kod, treści) · **Licencja:** MIT · ⭐ 83,7k ·
**Wydanie:** v2.1.0 (24.09.2026) · **Wynik: 79** (A5 B4 C3 D4 E3 F4)

**Czym jest.** Platforma ByteDance na LangGraph: agent prowadzący deleguje do subagentów działających
w piaskownicach (lokalnie, Docker, Kubernetes); pamięć długoterminowa, umiejętności, MCP, zadania planowane,
kanały komunikatorów. Wersja 2.0 (28.02.2026) to przepisanie od zera.

**Przewaga.** Rodowód deep research plus dojrzały runtime wieloagentowy; jawne nadpisanie modelu per subagent,
w przykładowej konfiguracji opisane wprost jako „lokalny model dla oszczędności".

**Lokalny model** (`config.yaml`):
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

**Wielu agentów i hybryda.** Agent prowadzący na `langchain_anthropic:ChatAnthropic`, subagenci z
`model: deepseek-local`. Limity: liczba subagentów na uruchomienie i sufity tokenów.

**Głos i obraz.** Brak głosu w wersji 2.0. `supports_vision: true` włącza narzędzie `view_image`;
przeglądarka Playwright robi zrzuty ekranu.

**Bezpieczeństwo.** Piaskownica lokalna, Docker albo Kubernetes; domyślnie nasłuch tylko na loopback; README
ostrzega, że administrator bramki to w praktyce wykonanie kodu.

**Harmonogram.** Zadania `once` / `cron` / `interval` z celem, warunkiem stopu i limitem uruchomień;
Telegram (long polling) i Slack.

**Słabe strony.** Trudne wdrożenie (Postgres i Redis przy wielu workerach); na lokalnych modelach wolny i podatny
na pętle (#1055); kanały nastawione na chińskie platformy; historia ucieczek z piaskownicy; brak głosu.

**Co warto ukraść.** Izolowany albo „migawkowy" kontekst przekazywany subagentowi; sufity tokenów per subagent;
zadania planowane z oceną celu i warunkiem stopu; komunikatory przez long polling, bez publicznego webhooka.

**Źródła:** [repozytorium](https://github.com/bytedance/deer-flow) ·
[config.example.yaml](https://github.com/bytedance/deer-flow/blob/main/config.example.yaml) ·
[#1055](https://github.com/bytedance/deer-flow/issues/1055)

---

## 10. ZeroClaw

**Kategoria:** osobisty agent (jeden plik binarny Rust) · **Licencja:** MIT lub Apache-2.0 · ⭐ 33,0k ·
**Wydanie:** v0.8.5 (5.09.2026) · **Wynik: 78** (A4 B4 C4 D4 E2 F5)

**Czym jest.** Runtime agenta w jednym pliku binarnym: 20+ dostawców LLM, 30+ kanałów, narzędzia powłoki,
przeglądarki, HTTP i MCP pod polityką bezpieczeństwa. Z rodziny „Claw" (alternatywy dla OpenClaw).
Uwaga na podróbki — oficjalne jest tylko `zeroclaw-labs/zeroclaw`.

**Przewaga.** Najgłębszy konfigurowalny model bezpieczeństwa: profile ryzyka, poziomy autonomii
ReadOnly / Supervised / Full (domyślnie `supervised`), automatyczny wybór piaskownicy (Landlock → Bubblewrap →
Firejail → Docker), podpisane HMAC potwierdzenia wywołań narzędzi, silnik procedur (SOP) z bramkami zatwierdzeń.

**Lokalny model.** Sekcja `[providers.models.llamacpp.<alias>]` z `uri`, `chat_template_kwargs`, `vision`.
Ustaw `native_tools = true` — domyślnie lokalne endpointy dostają narzędzia w trybie tekstowym.

**Wielu agentów i hybryda.** Każdy `[agents.<alias>]` ma własny profil dostawcy, więc koordynator na Claude może
`delegate` do agentów na slocie `llamacpp`. Delegacja jest domyślnie zabroniona — trzeba ją świadomie włączyć.

**Głos i obraz.** Piper jako lokalny TTS, rozmowy telefoniczne przez operatorów SIP. Obrazy dla tekstowego modelu
przekierowywane do osobnego dostawcy wizji.

**Bezpieczeństwo.** Domyślnie `supervised`: działania średniego ryzyka wymagają zatwierdzenia, wysokiego są
blokowane; zatwierdzenia kworum; tryb YOLO tylko na maszyny deweloperskie.

**Słabe strony.** Duża złożoność konfiguracji (cztery sekcje TOML), wiele otwartych zgłoszeń, rozdmuchiwanie
kontekstu przez powtarzanie rozumowania (#10396).

**Co warto ukraść.** Profile ryzyka oddzielone od agentów i delegacja domyślnie zabroniona; wspólne budżety
akcji i kosztów, których subagent nie obejdzie; przekierowanie obrazów do dedykowanego modelu.

**Źródła:** [konfiguracja dostawców](https://github.com/zeroclaw-labs/zeroclaw/blob/master/docs/book/src/providers/configuration.md) ·
[delegacja](https://github.com/zeroclaw-labs/zeroclaw/blob/master/docs/book/src/agents/delegation.md) ·
[wiele modeli](https://github.com/zeroclaw-labs/zeroclaw/blob/master/docs/book/src/getting-started/multi-model-setup.md)

---

## 11. Microsoft Agent Framework

**Kategoria:** SDK Python / .NET / Go z silnikiem workflow · **Licencja:** MIT · ⭐ 14,1k ·
**Wydanie:** python-1.21.0 (8.10.2026) · **Wynik: 77** (A5 B3 C3 D4 E3 F5)

**Czym jest.** Następca AutoGen i Semantic Kernel (AutoGen jest w trybie utrzymania; Python 1.0 GA 2.04.2026).
Agenci, klienci czatu dla wielu dostawców, middleware, sesje i typowany `WorkflowBuilder` z checkpointem
po każdym kroku.

**Przewaga.** Stabilne API 1.x z obietnicą długiego wsparcia; gotowe orkiestracje Sequential, Concurrent,
Handoff, Group Chat i Magentic (menedżer koordynujący specjalistów); najmocniejsza historia bezpieczeństwa:
etykiety przepływu informacji FIDES przeciw prompt injection i CodeAct w mikro-VM Hyperlight.

**Lokalny model.**
`OpenAIChatCompletionClient(model="deepseek-v4-flash", base_url="http://localhost:8080/v1", api_key="none")`.
Pułapka H1: w Pythonie `OpenAIChatClient` oznacza teraz Responses API. Gubienie `reasoning_content` naprawiono
dopiero we wrześniu 2026 (#8382).

**Wielu agentów i hybryda.** Menedżer Magentic albo planista na `AnthropicClient`, wykonawcy na kliencie
lokalnym — każdy agent ma własnego klienta.

**Głos i obraz.** Wejście audio do modeli, które je obsługują, ale bez agentów głosowych w czasie rzeczywistym
w Pythonie; obrazy jako treść wiadomości.

**Bezpieczeństwo.** FIDES (etykiety poufności i integralności, `SecureMCPToolProxy`) i CodeAct w mikro-VM
Hyperlight. FIDES nie działa wewnątrz zagnieżdżonych wywołań CodeAct (#9251).

**Słabe strony.** Przykłady nastawione na Azure / Foundry; zmiany łamiące nawet po GA; brak głosu w czasie
rzeczywistym w Pythonie.

**Co warto ukraść.** Checkpoint po każdym kroku z bezpiecznym deserializerem (lista dozwolonych typów);
haki `response_parser` / `message_preparer` na dziwactwa dostawców — idealne na pola rozumowania llama.cpp;
menedżer z rejestrem zadań (Magentic).

**Źródła:** [dostawca OpenAI](https://learn.microsoft.com/en-us/agent-framework/integrations/by-component/model-providers/openai) ·
[checkpointy](https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints) ·
[orkiestracje](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/) ·
[#8382](https://github.com/microsoft/agent-framework/issues/8382)

---

## 12. DeepSeek Harness

**Kategoria:** harness od DeepSeek (Web UI, tryb bezgłowy, SDK) · **Licencja:** MIT · ⭐ 247,3k ·
**Wydanie:** dsh-v0.2.1-alpha.2 (9.10.2026, przedpremierowe) · **Wynik: 76** (A5 B4 C3 D3 E3 F4)

**Czym jest.** Oficjalny harness DeepSeek (opublikowany 13.08.2026) zbudowany z wtyczek Cordis: adaptery modeli,
narzędzia, piaskownica, subagenci, harmonogram, UI, a nawet sama pętla agenta to wymienne wtyczki składane
w „profile". Warstwę LLM bierze z Pi (nr 13).

**Przewaga.** Strojenie pod DeepSeek V4 od producenta modelu (format myślenia, wysiłek rozumowania) i subagenci,
którymi mogą być **inne harnessy**: Claude Code, Codex, dowolny agent ACP albo kolejna instancja dsh.

**Lokalny model.** Settings → Models → „Custom model API": base URL i protokół `openai-completions`. Dla llama-server
zwykle `supportsDeveloperRole: false` i `maxTokensField: max_tokens`, a dla DeepSeek V4 `compat.thinkingFormat: deepseek`.
Znany błąd: obrazy WebP psują sesję llama.cpp (#7406).

**Wielu agentów i hybryda.** W obie strony: lokalny DeepSeek jako rodzic deleguje do dziecka Claude Code
(z ustalonym `permissionMode`), albo rodzic na Anthropic, a dzieci dsh na lokalnym modelu. `maxActiveSubagents`
ma domyślnie 8 — ustaw 4. To nie jest gotowy preset „Claude planuje, lokalni wykonują" — układ składasz
z wtyczek w profilu.

**Głos i obraz.** Eksperymentalne STT; lokalny SenseVoice nie obsługuje polskiego. Obrazy włączane per model
(`input: [text, image]`).

**Bezpieczeństwo.** Domyślna piaskownica `read-only`, zestawy uprawnień (piaskownica + polityka zatwierdzeń),
oczyszczone środowisko procesów potomnych.

**Słabe strony.** Wersja przedpremierowa — README ostrzega wielkimi literami przed zmianami łamiącymi zgodność.
Brak zakładki Issues (błędy trafiają do Discussions); słaba dokumentacja konfiguracji poza UI.

**Co warto ukraść.** Profil `compat` per model (rola developer, nazwa pola `max_tokens`, format myślenia)
zamiast zgadywania po adresie URL; subagent-dostawca opakowujący inne harnessy; bezpieczny domyślny tryb
tylko do odczytu.

**Źródła:** [README](https://github.com/deepseek-ai/deepseek-harness/blob/main/README.md) ·
[dostawcy](https://github.com/deepseek-ai/deepseek-harness/blob/main/docs/user/guide/providers.md) ·
[SAFETY.md](https://github.com/deepseek-ai/deepseek-harness/blob/main/SAFETY.md)

---

## 13. Pi

**Kategoria:** minimalny harness kodujący + biblioteki TS · **Licencja:** MIT · ⭐ 114,2k ·
**Wydanie:** v1.1.0 (7.10.2026) · **Wynik: 76** (A4 B5 C3 D4 E5 F1)

**Czym jest.** „Minimalny, rozszerzalny harness, który możesz uczynić swoim" (Mario Zechner, od 2026 w Earendil):
terminalowy agent `pi` i biblioteki, na których stoi (`pi-ai` — warstwa wielu dostawców, `pi-agent-core`,
`pi-durable`). Jego warstwy używają inne projekty, np. DeepSeek Harness.

**Przewaga.** Mały rdzeń z wyjątkowo głębokim API rozszerzeń: własne narzędzia, bramki uprawnień, przekierowanie
narzędzi przez SSH albo do mikro-VM, „wirtualne modele" kierujące każde zapytanie do innego fizycznego modelu.
Pierwszorzędna obsługa llama.cpp i cztery poziomy osadzania: TUI, `--print` / `--mode json`, `--mode rpc`, SDK.

**Lokalny model.** Dla llama-swap użyj ogólnej ścieżki `~/.pi/agent/models.json` (`baseUrl`,
`"api": "openai-completions"`) — wbudowane `/llama` zakłada llama-server w trybie routera.

**Wielu agentów i hybryda.** Subagenci (oficjalne rozszerzenie-przykład) w osobnych procesach, opisani w Markdown
z polem `model:` — jeden na Anthropic, drugi lokalnie. Wirtualne modele: łatwe tury lokalnie, trudne do Claude,
z kosztem per model w podsumowaniu sesji.

**Głos i obraz.** Brak głosu. Obrazy wklejane do terminala, `@obraz` w prompcie, narzędzie `read` czyta obrazy.

**Bezpieczeństwo.** **Brak** zatwierdzeń i piaskownicy — z założenia. Uruchamiaj w kontenerze albo piaskownicy
(patrz [02-KLOCKI.md](02-KLOCKI.md#piaskownice)).

**Słabe strony.** Subagenci to przykład, nie rdzeń; zgłoszenia nowych osób są automatycznie zamykane.

**Co warto ukraść.** Jeden rdzeń, wiele trybów osadzenia; wirtualne modele z zapisem fizycznego modelu przy każdej
wiadomości; *codemode* — model pisze JS, który woła narzędzia równolegle i filtruje wyniki, zanim trafią do kontekstu
(oszczędza tokeny na wolnym modelu lokalnym). Obok mini-swe-agent — najlepszy kod do nauki z całej listy.

**Źródła:** [README agenta](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/README.md) ·
[llama.cpp](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/llama-cpp.md) ·
[modele](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md) ·
[bezpieczeństwo](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md)

---

## 14. gptme

**Kategoria:** agent terminalowy + agenci autonomiczni · **Licencja:** MIT · ⭐ 4,4k ·
**Wydanie:** v0.34.0 (18.09.2026) · **Wynik: 75** (A4 B4 C4 D3 E4 F3)

**Czym jest.** „Osobisty agent AI, który działa wszędzie tam, gdzie terminal" — rozwijany od 2023, lokalny
w pierwszej kolejności: powłoka, Python, pliki, przeglądarka, wizja, subagenci, MCP.

**Przewaga.** Wymienny format narzędzi: domyślnie bloki kodu Markdown, do tego XML i natywny — działa więc tam,
gdzie parsowanie wywołań narzędzi w llama.cpp zawodzi. `gptme service init` generuje usługę i timer systemd
dla agenta działającego stale.

**Lokalny model.** `OPENAI_BASE_URL=http://localhost:8080/v1 gptme -m local/deepseek-v4-flash`;
przy zapętlaniu: `--tool-format xml`.

**Wielu agentów i hybryda.** Rodzic na `anthropic/claude-…`, subagenci na `local/…`; subagentem może być też
inny harness przez ACP (np. Claude Code). Izolacja w git worktree.

**Głos i obraz.** Rozmowa w czasie rzeczywistym tylko przez chmurowe API (OpenAI, xAI); lokalny TTS Kokoro
(bez polskiego). Wizja, zrzuty ekranu, sterowanie pulpitem, przeglądarka Playwright.

**Bezpieczeństwo.** Potwierdzenia domyślnie włączone; trzystopniowa polityka powłoki: komendy tylko do odczytu
przechodzą same, lista zakazów (np. `git push -f`, `| bash`) blokuje, reszta pyta. Piaskownica systemowa
jest niedojrzała.

**Słabe strony.** Heurystyczne parsowanie Markdown; mała społeczność; dużo zmian pisze jego własny agent
autonomiczny, więc tempo i rotacja kodu są wysokie.

**Co warto ukraść.** Format narzędzi jako parametr, z rankingiem model × format; trzy tryby izolacji subagenta
(wątek, podproces, ACP); szkielet usługi systemd z promptem i dziennikiem dla agenta stałego.

**Źródła:** [dostawcy](https://gptme.org/docs/providers.html) ·
[formaty narzędzi](https://github.com/gptme/gptme/blob/master/docs/tool-formats.rst) ·
[subagenci](https://github.com/gptme/gptme/blob/master/docs/tools/subagent.rst)

---

## 15. Moltis

**Kategoria:** osobisty serwer agenta (jeden plik binarny Rust) · **Licencja:** MIT · ⭐ 2,9k ·
**Wydanie:** 20260913.02 (14.09.2026) · **Wynik: 74** (A4 B4 C4 D2 E3 F5)

**Czym jest.** Jeden plik binarny z UI webowym, aplikacją PWA na telefon i bramką komunikatorów: pętla agenta,
pamięć, głos, harmonogram, MCP i piaskownice. Importuje konfigurację i umiejętności OpenClaw.

**Przewaga.** Najbardziej kompletny „jeden plik": wbudowane lokalne STT i TTS, wybór piaskownicy (Podman, Docker,
WASM, host z ograniczeniami), Prometheus / OTLP / Langfuse, podpisane wydania i brak marketplace'u wtyczek
(„nie ma przez co zostać zaatakowanym").

**Lokalny model.** `[providers.custom-llamaswap]` z `base_url = "http://localhost:8080/v1"` i
`tool_mode = "auto" | "native" | "text"`. Wbudowany backend GGUF nie ma ścieżki ROCm — użyj llama-swap.

**Wielu agentów i hybryda.** Koordynator na `anthropic/…`, presety wykonawców z
`model = "custom-llamaswap/deepseek-v4-flash"` (dokładny format nazwy dla własnego dostawcy niezweryfikowany —
sprawdź nazwy w `/v1/models`), własnymi narzędziami, piaskownicą i zakresem pamięci.
Preset `coordinator` ma `delegate_only = true`. Heartbeat może działać na osobnym, lokalnym modelu.

**Głos i obraz.** Najmocniejszy lokalny stos w kategorii: STT lokalnie (Whisper, Sherpa-ONNX, Voxtral), TTS
lokalnie (Piper z polskimi głosami, Coqui), odpowiedzi jako notatki głosowe na Telegramie. Obrazy przez dostawców
z wizją; zrzuty ekranu i przeglądarka.

**Bezpieczeństwo.** `backend = "auto"` wybiera piaskownicę (Podman → Docker → host z ograniczeniami);
`approval_mode`, zatwierdzanie zapisu i edycji, haki przed wywołaniem narzędzia, ochrona przed SSRF.

**Słabe strony.** **Praktycznie jeden opiekun** (około 3,6 tys. commitów lidera wobec <100 następnej osoby);
status alfa; obawy o samomodyfikujące się umiejętności.

**Co warto ukraść.** Presety łączące model, narzędzia, piaskownicę i zakres pamięci + koordynator, który tylko
deleguje — gotowy szablon „Opus planuje, lokalni wykonują"; znaczniki czasu poza promptem systemowym (pułapka H4);
automatyczny checkpoint przed zmianą pamięci albo umiejętności.

**Źródła:** [dostawcy](https://github.com/moltis-org/moltis/blob/main/docs/src/providers.md) ·
[presety agentów](https://github.com/moltis-org/moltis/blob/main/docs/src/agent-presets.md) ·
[głos](https://github.com/moltis-org/moltis/blob/main/docs/src/voice.md)

---

## 16. QwenPaw

**Kategoria:** osobisty „Agent OS" (Alibaba AgentScope) · **Licencja:** Apache-2.0 · ⭐ 35,6k ·
**Wydanie:** v2.2.1 (11.09.2026) · **Wynik: 74** (A4 B4 C3 D4 E3 F4)

**Czym jest.** Dawniej CoPaw: asystent z konsolą webową, TUI i aplikacją desktop, trójwarstwową pamięcią,
umiejętnościami, MCP / A2A / ACP, wieloma agentami i kanałami komunikatorów.

**Przewaga.** Wielowarstwowe bezpieczeństwo: piaskownica jądra (Bubblewrap / Landlock), Tool Guard z poziomami
zatwierdzeń, ochrona plików z sekretami, skaner umiejętności przed aktywacją. Routing modelu per agent od v2.2.1.

**Lokalny model.** Dostawca własny w trybie OpenAI `chat.completions`. Ustaw okno kontekstu ręcznie —
katalog chmurowy bywa stosowany do lokalnego aliasu (#7979, pułapka H3).

**Wielu agentów i hybryda.** Niezależni agenci z własnym modelem i pamięcią; `spawn_subagent` z izolacją
w git worktree.

**Głos i obraz.** Transkrypcja przez Whisper API albo lokalny Whisper (otwarte błędy, np. #8035); narzędzie
`view_media` i obrazy z kanałów — potrzebny model z wizją.

**Bezpieczeństwo.** Opisane w przewadze: piaskownica jądra, Tool Guard z poziomami STRICT / SMART / AUTO / OFF,
ochrona plików z sekretami, skaner umiejętności.

**Słabe strony.** Kanały nastawione na Chiny (DingTalk zalecany; brak WhatsAppa i Signala), ponad 1000 otwartych
zgłoszeń i PR, otwarte błędy transkrypcji.

**Co warto ukraść.** Silnik reguł Tool Guard z poziomami; skaner umiejętności przed aktywacją; „Scroll Context" —
indeksuj usunięte tury zamiast je stratnie streszczać; okno kontekstu brane z serwera, nigdy z katalogu nazw.

**Źródła:** [modele](https://github.com/agentscope-ai/QwenPaw/blob/main/website/public/docs/models.en.md) ·
[wielu agentów](https://github.com/agentscope-ai/QwenPaw/blob/main/website/public/docs/multi-agent.en.md) ·
[#7979](https://github.com/agentscope-ai/QwenPaw/issues/7979)

---

## 17. OpenAI Agents SDK

**Kategoria:** lekkie SDK wieloagentowe (Python) · **Licencja:** MIT · ⭐ 30,0k · **Wydanie:** v0.23.1 (2.10.2026) ·
**Wynik: 74** (A4 B3 C3 D4 E5 F4)

**Czym jest.** Mały zestaw prymitywów: `Agent`, `Runner`, narzędzia, przekazania (*handoffs*),
agenci-jako-narzędzia, *guardrails*, sesje, `RunState`; do tego agenci w piaskownicy i potok głosowy.

**Przewaga.** Najprostszy model mentalny z listy; serializowalny `RunState` (wstrzymaj → zatwierdź → wznów nawet po
godzinach); `VoicePipeline` z wymiennym STT i TTS.

**Lokalny model.**
`OpenAIChatCompletionsModel(model="deepseek-v4-flash", openai_client=AsyncOpenAI(base_url="http://localhost:8080/v1", api_key="none"))`
oraz `set_tracing_disabled(True)` — inaczej eksport śladów do OpenAI zwraca 401. Domyślne Responses API nie działa
z llama-server (pułapka H1).

**Wielu agentów i hybryda.** Każdy `Agent(model=...)` osobno; Claude przez adapter LiteLLM albo any-llm
(brak natywnego dostawcy Anthropic). Przy LiteLLM przypnij wersje — patrz [02-KLOCKI.md](02-KLOCKI.md#bramka-i-routing-modeli).

**Głos.** `VoicePipeline` = STT → Twój workflow → TTS; domyślnie modele OpenAI, ale interfejsy są wymienne,
więc lokalny Whisper i Piper wchodzą przez własne adaptery.

**Bezpieczeństwo.** Agenci w piaskownicy (lokalnie dla zaufanego kodu albo w Dockerze), guardrails wejścia
i wyjścia, redakcja błędów narzędzi (v0.23.0). Obrazy przechodzą jako części wiadomości.

**Słabe strony.** Domyślne ustawienia OpenAI do nadpisania; wyjście strukturalne tłumiło wywołania narzędzi
na ścisłych serwerach (#3709, naprawione); wersje 0.x.

**Co warto ukraść.** `RunState` z listą przerwań i API zatwierdź / odrzuć; filtry wejścia przy przekazaniach;
*guardrails* jako „bezpieczniki" działające równolegle z agentem.

**Źródła:** [modele](https://openai.github.io/openai-agents-python/models/) ·
[repozytorium](https://github.com/openai/openai-agents-python) ·
[wydanie v0.23.0](https://github.com/openai/openai-agents-python/releases/tag/v0.23.0)

---

## 18. n8n

**Kategoria:** platforma automatyzacji (wizualna, *fair-code*) · **Licencja:** Sustainable Use License · ⭐ 207,0k ·
**Wydanie:** n8n@2.42.6 (9.10.2026) · **Wynik: 73** (A4 B3 C4 D5 E3 F2)

**Czym jest.** Wizualny edytor przepływów z węzłami agentów, samodzielnie hostowany, z ogromnym katalogiem
integracji.

**Przewaga.** Najszerszy zestaw wyzwalaczy i integracji (cron, webhooki, RSS z deduplikacją, e-mail, Telegram,
Google Sheets…) i zatwierdzanie przez człowieka per narzędzie, wysyłane na Telegram, Slack albo e-mail.
Najszybsza droga od pomysłu do działającego alertu.

**Lokalny model.** Poświadczenie OpenAI ma pole „Base URL" → `http://localhost:8080/v1`. W węźle OpenAI Chat Model
**wyłącz „Use Responses API"** — z llama.cpp kończyło się błędem 400 (#26639, pułapka H1).

**Wielu agentów i hybryda.** Agent-orkiestrator z węzłem Anthropic Chat Model, agenci-narzędzia (AI Agent Tool)
z modelem lokalnym — model wybierany per węzeł.

**⚠️ Licencja.** Sustainable Use License to nie open source w rozumieniu OSI: wolno używać wewnętrznie i we własnych
procesach, nie wolno oferować n8n jako usługi; pliki `.ee.` są na licencji komercyjnej.

**⚠️ Bezpieczeństwo.** Krytyczna luka CVE-2026-21858 (7.01.2026): nieuwierzytelniony dostęp do plików przez
obsługę webhooków, który według ostrzeżenia australijskiego CERT-u (ACSC) pozwala na zdalne wykonanie kodu bez
logowania. Nie wystawiaj instancji do internetu bez aktualizacji. Limit współbieżności produkcyjnej nie obejmuje
podprzepływów.

**Głos i obraz.** Brak pętli głosowej (do zbudowania: notatka głosowa z Telegrama → lokalny Whisper → agent → TTS);
obrazy trafiają do modelu opcją „Automatically Passthrough Binary Images".

**Co warto ukraść.** Zatwierdzenie per narzędzie wysyłane na komunikator; wyzwalacze odpytujące z zapamiętanym
stanem (RSS odpala tylko nowe pozycje); osobna kolejka FIFO dla wykonań produkcyjnych.

**Źródła:** [licencja](https://docs.n8n.io/n8n-community-license/sustainable-use-license) ·
[AI Agent Tool](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolaiagent) ·
[człowiek w pętli](https://docs.n8n.io/advanced-ai/human-in-the-loop-tools) ·
[porady bezpieczeństwa](https://github.com/n8n-io/n8n/security/advisories)

---

## 19. LibreChat

**Kategoria:** wieloosobowa platforma czatu z agentami · **Licencja:** MIT · ⭐ 45,5k · **Wydanie:** v0.8.8 (1.10.2026) ·
**Wynik: 73** (A5 B3 C3 D4 E2 F4)

**Czym jest.** Platforma w stylu ChatGPT łącząca dostawców chmurowych i własne endpointy OpenAI-compatible:
agenci z narzędziami, MCP, kodem i pamięcią, zespoły subagentów i Agents API. Przejęta przez ClickHouse;
repozytorium przeniesiono do `LibreChat-AI`.

**Przewaga.** Prawdziwy wybór dostawcy i modelu per agent, zapisane zespoły subagentów jako małe grafy (DAG),
otwartoźródłowy interpreter kodu (NsJail albo mikro-VM libkrun), reguły zatwierdzeń, Prometheus / OpenTelemetry /
Langfuse.

**Lokalny model.** `librechat.yaml` → `endpoints.custom[]` z `baseURL: "http://localhost:8080/v1"`. Dla DeepSeeka
`customParams.includeReasoningContent: true` (pułapka H2); okno kontekstu ustaw jawnie (#14228).

**Wielu agentów i hybryda.** Agent-rodzic na Anthropic tworzy dzieci przypięte do endpointu llama.cpp
(`agent_ids` albo graf zespołu); `maxSubagents` domyślnie 10.

**Głos i harmonogram.** STT i TTS konfigurowalne, także lokalne usługi zgodne z OpenAI; bez rozmów na żywo.
„Scheduled Chats" — eksperymentalne, od v0.8.8.

**Bezpieczeństwo i obraz.** Reguły zatwierdzeń deny → ask → allow, egzekwowane też w uruchomieniach bezgłowych
i planowanych; tryby zatwierdzania kodu; interpreter w NsJail albo mikro-VM libkrun. Natywne przesyłanie obrazów,
OCR i generowanie obrazów.

**Słabe strony.** Ciężki stos (MongoDB, Meilisearch, pgvector); dużo funkcji w becie; powracające błędy schematów
narzędzi z llama.cpp; regresja prompt cache (#16877); krytyczne CVE w obszarze MCP.

**Co warto ukraść.** Reguły zatwierdzeń w kolejności deny → ask → allow; zespoły subagentów jako DAG z agentem
wejściowym i wynikowym; bezpieczniki harmonogramu (`minIntervalMinutes`, `autoDisableAfterFailures`).

**Źródła:** [agenci](https://www.librechat.ai/docs/features/agents) ·
[wydanie v0.8.8](https://www.librechat.ai/changelog/v0.8.8) ·
[wydania](https://github.com/LibreChat-AI/LibreChat/releases)

---

## 20. Kilo Code

**Kategoria:** agent kodujący (CLI, VS Code, JetBrains) · **Licencja:** MIT · ⭐ 27,6k ·
**Wydanie:** JetBrains 7.1.9 (8.10.2026) · **Wynik: 73** (A5 B3 C3 D4 E3 F3)

**Czym jest.** Rozwidlenie OpenCode; od 2.04.2026 rozszerzenie VS Code działa na tym samym rdzeniu serwera.
Naturalna ścieżka migracji dla użytkowników zarchiwizowanego Roo Code.

**Przewaga.** Rdzeń OpenCode + UI w VS Code i JetBrains, menedżer równoległych agentów w osobnych git worktree,
osobny tani model do pamięci i kompakcji.

**Lokalny model.** Settings → Providers → „OpenAI Compatible" z Base URL; w CLI `~/.config/kilo/kilo.jsonc`.
Powtarzające się niezgodności schematów narzędzi z llama.cpp (#12773 — naprawione, #12408 — pułapka H7).

**Wielu agentów i hybryda.** Każdy agent i subagent przypina `provider/model` — główny na `anthropic/claude-…`,
subagenci na llama-swap.

**Głos i obraz.** Eksperymentalne „Speech to Text" przez chmurowy Whisper OpenAI; obrazy w CLI prawdopodobnie
jak w OpenCode (niezweryfikowane).

**Bezpieczeństwo.** Reguły uprawnień z wzorcami per agent, izolacja w git worktree, tryb prywatności maskujący
dane osobowe; brak piaskownicy systemowej.

**Słabe strony.** Duża część funkcji „zawsze włączonych" (Cloud Agents, Slack) to płatna usługa; tryb Orchestrator
wycofany w trakcie życia; ryzyko rozjazdu z upstreamem.

**Co warto ukraść.** Menedżer agentów w osobnych worktree; czytelne kody wyjścia w CI (124 = timeout).

**Źródła:** [własni subagenci](https://kilo.ai/docs/customize/custom-subagents) ·
[CLI](https://kilo.ai/docs/code-with-ai/platforms/cli) · [#12773](https://github.com/Kilo-Org/kilocode/issues/12773)

---

## Pozostali kandydaci (miejsca 21–64)

Przeszli kryteria wejścia (Paperclip i Hive — tylko pośrednio, przez adaptery), ale przegrali punktacją.
Dla każdego jedno zdanie: dlaczego warto wiedzieć, że istnieje, i co go zatrzymało.

| # | Harness | Kategoria | Wynik | Za | Przeciw |
|---|---|---|---|---|---|
| 21 | [Vercel AI SDK](https://github.com/vercel/ai) | framework TS | 72 | standard warstwy modeli w TS, multimodalność | agent to cienka warstwa; harmonogram i integracje DIY |
| 22 | [Agent Zero](https://github.com/agent0ai/agent-zero) | osobisty | 71 | cały komputer w Dockerze na agenta, lokalny Whisper i Kokoro | częste regresje wersji 2.x |
| 23 | [nanobot](https://github.com/HKUDS/nanobot) | osobisty | 71 | czytelny rdzeń Python do forkowania, API OpenAI-compatible | subagenci dziedziczą model rodzica |
| 24 | [Google ADK](https://github.com/google/adk-python) | framework Py | 70 | najlepsze A2A, narzędzia ewaluacji, dev UI | modele spoza Gemini przez LiteLLM — źródło błędów |
| 25 | [Agno](https://github.com/agno-agi/agno) | framework Py | 70 | kompletny runtime: harmonogram, kolejka, kanały, FinanceTools | ogromny plik rdzenia, łamiąca v3 |
| 26 | [Qwen Code](https://github.com/QwenLM/qwen-code) | kodujący | 70 | mostek wizji dla modeli tekstowych, dyktowanie | częste regresje schematów z llama.cpp |
| 27 | [Haystack](https://github.com/deepset-ai/haystack) | framework Py | 70 | najlepszy stos RAG i wyszukiwania | limit współbieżności per potok, nie per model |
| 28 | [OpenJarvis](https://github.com/open-jarvis/OpenJarvis) | osobisty | 70 | lokalny w pierwszej kolejności, 15+ silników | młody, badawczy kod |
| 29 | [Open WebUI](https://github.com/open-webui/open-webui) | osobisty | 69 | najlepsze UI dla lokalnych modeli, głos | subagenci zawsze na modelu rodzica; 158 porad bezpieczeństwa w 2026; licencja z klauzulą marki |
| 30 | [Sim](https://github.com/simstudioai/sim) | workflow | 69 | wizualne przepływy wieloagentowe, RSS co minutę, Apache-2.0 | llama.cpp nieoficjalnie (#1637), pre-1.0 |
| 31 | [Codewhale](https://github.com/codewhale-hq/Codewhale) | kodujący | 69 | flota ról z modelami, lokalny `/voice` | dryf w stronę konta i chmury, telemetria domyślnie |
| 32 | [PicoClaw](https://github.com/sipeed/picoclaw) | osobisty | 69 | lekki Go na słaby sprzęt | brak piaskownicy systemowej, pre-1.0 |
| 33 | [Cline](https://github.com/cline/cline) | kodujący | 68 | świetny w IDE, podział Plan/Act na dwa modele | zmiany formatu narzędzi psuły lokalne modele (#13008); dyktowanie płatne |
| 34 | [CrewAI](https://github.com/crewAIInc/crewAI) | framework Py | 68 | najprostszy model ról i zadań | błędy „pusta odpowiedź" z lokalnymi modelami; telemetria domyślnie |
| 35 | [LlamaIndex Workflows](https://github.com/run-llama/llama_index) | framework Py | 68 | czytelny silnik zdarzeń, `num_workers` per krok | firma skupia się na dokumentach |
| 36 | [Reasonix](https://github.com/esengine/DeepSeek-Reasonix) | kodujący | 68 | natywny tryb planista + wykonawca | lokalne modele drugiej kategorii, jeden opiekun |
| 37 | [Kestra](https://github.com/kestra-io/kestra) | workflow | 68 | YAML, limit współbieżności w OSS, pauza do zatwierdzenia | Java, mniej wygodny do prototypów |
| 38 | [Mastra](https://github.com/mastra-ai/mastra) | framework TS | 68 | najpełniejszy stos TS | atak na łańcuch dostaw npm (06.2026); komunikaty systemowe w środku rozmowy |
| 39 | [Windmill](https://github.com/windmill-labs/windmill) | workflow | 68 | najlepszy dla DevOps: skrypty, cron, webhooki | limity współbieżności tylko w EE; AGPL + części zamknięte |
| 40 | [OpenAI Agents SDK (JS)](https://github.com/openai/openai-agents-js) | framework TS | 67 | najlepszy głos w czasie rzeczywistym w TS | głos tylko z modelami OpenAI |
| 41 | [Dify](https://github.com/langgenius/dify) | workflow | 66 | najlepsze RAG wśród narzędzi wizualnych | licencja zabrania SaaS dla wielu klientów; ciężkie aktualizacje |
| 42 | [LobeHub](https://github.com/lobehub/lobehub) | osobisty | 66 | najlepsze UI zespołów agentów | licencja ogranicza dzieła pochodne |
| 43 | [Langflow](https://github.com/langflow-ai/langflow) | workflow | 66 | każdy projekt to serwer MCP | brak harmonogramu, głos usunięty, seria porad bezpieczeństwa |
| 44 | [VoltAgent](https://github.com/VoltAgent/voltagent) | framework TS | 65 | równoległe delegowanie do wielu subagentów | wyzwalacze i konsola w płatnym SaaS |
| 45 | [Crush](https://github.com/charmbracelet/crush) | kodujący | 65 | natywny typ dostawcy llama.cpp | licencja FSL (nie OSI), brak piaskownicy |
| 46 | [Omnigent](https://github.com/omnigent-ai/omnigent) | meta-harness | 65 | łączy Claude Code, Codex i Pi w jednej sesji | status alfa |
| 47 | [OpenClaw](https://github.com/openclaw/openclaw) | osobisty | 64 | największy ekosystem, najwięcej kanałów, głos | patrz [README](README.md#dlaczego-nie-ma-ich-w-czołówce) |
| 48 | [BeeAI Framework](https://github.com/i-am-bee/beeai-framework) | framework Py | 63 | reguły użycia narzędzi pomagające słabym modelom | mała społeczność |
| 49 | [Cherry Studio](https://github.com/CherryHQ/cherry-studio) | osobisty | 62 | agent w stylu OpenClaw w aplikacji desktop | ścieżka lokalnych agentów zabugowana; AGPL |
| 50 | [NanoClaw](https://github.com/nanocoai/nanoclaw) | osobisty | 62 | kontener na grupę agentów | zbudowany wokół Claude; lokalnie tylko przez OpenCode |
| 51 | [AG2](https://github.com/ag2ai/ag2) | framework Py | 62 | wbudowany głos (kaskada i realtime) | v1 niekompatybilne ze starym AutoGen |
| 52 | [Open Interpreter](https://github.com/openinterpreter/openinterpreter) | kodujący | 61 | przepisany w Rust, „emulacja harnessu" per model | wersje 0.0.x |
| 53 | [Mistral Vibe](https://github.com/mistralai/mistral-vibe) | kodujący | 60 | wbudowany głos | głos chmurowy; brak Anthropic; błędy szablonów z llama.cpp |
| 54 | [Paperclip](https://github.com/paperclipai/paperclip) | meta-harness | 60 | „firma z agentów" z budżetami | lokalny model tylko pośrednio (przez adaptery OpenCode albo Pi) |
| 55 | [smolagents](https://github.com/huggingface/smolagents) | framework Py | 60 | najmniejszy czytelny rdzeń (CodeAgent) | spowolnione utrzymanie, brak trwałości |
| 56 | [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) | kodujący | 59 | 100 linii, tylko bash — świetny do nauki | brak MCP i subagentów z założenia |
| 57 | [CAMEL](https://github.com/camel-ai/camel) | framework Py | 58 | szeroki katalog narzędzi | od pół roku tylko wydania alfa |
| 58 | [Jan](https://github.com/janhq/jan) | osobisty | 58 | najlepsze UX lokalnych modeli na desktopie | brak głosu; MCP z własnymi endpointami zepsute |
| 59 | [Codex CLI](https://github.com/openai/codex) | kodujący | 57 | świetna piaskownica i CI | od 02.2026 tylko Responses API; brak Anthropic |
| 60 | [Letta Code](https://github.com/letta-ai/letta-code) | framework TS | 57 | pamięć jako rdzeń | teraz TypeScript, chmura domyślnie |
| 61 | [IronClaw](https://github.com/nearai/ironclaw) | osobisty | 55 | narzędzia w WASM, ochrona sekretów | przepisanie 1.0 zresetowało funkcje |
| 62 | [Activepieces](https://github.com/activepieces/activepieces) | workflow | 53 | MIT i ogromna biblioteka integracji | agenci wyłączeni w darmowej edycji Community |
| 63 | [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) | osobisty | 51 | najprostsza instalacja | brak wielu agentów (#2635) |
| 64 | [Hive](https://github.com/aden-hive/hive) | framework Py | 50 | „kolonie" agentów z odzyskiwaniem po awarii | lokalny model tylko pośrednio (przez LiteLLM), bezpośrednie wsparcie to otwarte zgłoszenie (#7324) |

## Wykluczeni na wejściu

Nie spełnili któregoś z czterech warunków (licencja pozwalająca na self-hosting, udokumentowany lokalny endpoint
OpenAI-compatible, aktywność: commit ≤ 3 miesiące i wydanie ≤ 6 miesięcy przed 11.10.2026, projekt nie jest
oficjalnie zakończony).

| Projekt | Powód |
|---|---|
| [Roo Code](https://github.com/RooCodeInc/Roo-Code) | zarchiwizowany 15.05.2026 (kontynuacja społeczności: Zoo Code; migracja: Kilo Code) |
| [Flowise](https://github.com/FlowiseAI/Flowise) | wygaszony, zarchiwizowany 10.08.2026; niezałatane krytyczne luki zostaną niezałatane |
| [Continue](https://github.com/continuedev/continue) | opiekunowie ogłosili koniec projektu (przejęcie przez Cursor; README: „no longer actively maintained"); ostatnie wydanie 2.0.0 z 19.06.2026 |
| [Plandex](https://github.com/plandex-ai/plandex) | brak commitów od 3.10.2025 |
| [Aider](https://github.com/Aider-AI/aider) | ostatni commit 22.05.2026, ostatnie wydanie 9.08.2025 — w praktyce wstrzymany |
| [Khoj](https://github.com/khoj-ai/khoj) | ostatnie wydanie 26.03.2026, tryb utrzymania |
| [Google ADK dla TypeScript](https://github.com/google/adk-js) | brak dostawcy OpenAI-compatible (zgłoszenie #533 otwarte) |
| [Grok Build](https://github.com/xai-org/grok-build) | brak wydań; pierwsze uruchomienie wymaga logowania do xAI (niezweryfikowane bez konta); w lipcu 2026 zgłoszono wysyłanie całych repozytoriów na serwer |

## Poza rankingiem

Świetne, ale to nie są harnessy — opisuję je w [02-KLOCKI.md](02-KLOCKI.md):

- **DSPy** — kompilacja programów LLM pod konkretny (także słaby, lokalny) model; Claude jako nauczyciel w GEPA.
- **forge** — warstwa niezawodności wywołań narzędzi dla modeli lokalnych i kolejka slotów.
- **Trigger.dev** — infrastruktura trwałych zadań z limitami współbieżności.
