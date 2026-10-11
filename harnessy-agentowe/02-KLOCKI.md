# Klocki — wszystko, czego harness nie daje sam

**Stan na 11 października 2026.** Harness to pętla, narzędzia i kontekst. Żeby agent szukał okazji, pilnował cen,
gadał po polsku albo oglądał zdjęcia, potrzebuje klocków: wyszukiwarki, crawlera, kolejki, powiadomień, modelu
mowy, modelu wizji. Tu są najlepsze z nich, wybrane pod Twój sprzęt. Źródła: [ZRODLA.md](ZRODLA.md).

**Zasady doboru** (te same w każdej sekcji):

- **Bez Dockera na start.** Na maszynie nie ma dziś Dockera, więc preferuję `pip`, `npx` / `uvx` albo pojedynczy plik
  binarny. Narzędzia „tylko Docker" oznaczam.
- **Lokalni wykonawcy dostają małe zestawy narzędzi tylko do odczytu.** Narzędzia, które piszą i zmieniają świat,
  trzyma planista (Opus) albo człowiek.
- **Jedna bramka przed Anthropic i llama-swap** — koszt i współbieżność widać w jednym miejscu.
- **Licencja ma znaczenie** dla zastosowań zarobkowych (U2): modele i narzędzia „tylko niekomercyjnie" oznaczam ⚠️.

Skróty zastosowań: **U1** DevOps, **U2** dochód pasywny (złożone przepływy), **U3** rynki i okazje (wyszukiwanie +
alerty), **U4** głos, **U5** obrazy.

---

## Spis treści

1. [Bramka i routing modeli](#bramka-i-routing-modeli)
2. [Wyszukiwanie i pobieranie stron](#wyszukiwanie-i-pobieranie-stron)
3. [Agenci przeglądarkowi](#agenci-przeglądarkowi)
4. [Deep research](#deep-research)
5. [Monitoring cen i zmian na stronach](#monitoring-cen-i-zmian-na-stronach)
6. [Dane finansowe](#dane-finansowe)
7. [Powiadomienia i kanały](#powiadomienia-i-kanały)
8. [Harmonogram i trwałe wykonanie](#harmonogram-i-trwałe-wykonanie)
9. [Pamięć](#pamięć)
10. [Obserwowalność i ewaluacja](#obserwowalność-i-ewaluacja)
11. [Piaskownice](#piaskownice)
12. [Serwery MCP dla DevOps](#serwery-mcp-dla-devops)
13. [Głos](#głos)
14. [Obraz](#obraz)
15. [Niezawodność wywołań narzędzi i strojenie promptów](#niezawodność-wywołań-narzędzi-i-strojenie-promptów)
16. [Minimalne zestawy na start](#minimalne-zestawy-na-start)

---

## Bramka i routing modeli

| Narzędzie | Do czego | Licencja | Lokalnie | Uwagi (2026) |
|---|---|---|---|---|
| [llama-swap](https://github.com/mostlygeek/llama-swap) ⭐ | podmiana modeli lokalnych, jeden adres dla czatu, embeddingów, audio i obrazów; mówi też API Anthropic `/v1/messages` | MIT | jeden plik binarny | już go masz; brak budżetów i rozliczeń; przekroczenie `concurrencyLimit` daje od razu 429 |
| [Bifrost](https://github.com/maximhq/bifrost) ⭐ | bramka przed Anthropic + llama-swap: fallbacki, wirtualne klucze z budżetami, kolejka | Apache-2.0 (rdzeń) | jeden plik binarny (Go) | `concurrency: 4` per dostawca z kolejką — dokładnie Twoje sloty; od v2.2.6 uwierzytelnianie domyślnie włączone |
| [LiteLLM](https://github.com/BerriAI/litellm) ⚠️ | najbogatsze budżety i rozliczenia per klucz / zespół | MIT + `enterprise/` | pip | **24.03.2026 skradzione poświadczenia PyPI → złośliwe wersje 1.82.7 i 1.82.8**; w 2026 kolejne porady bezpieczeństwa proxy. Jeśli używasz — przypinaj dokładne wersje z hashami |
| TensorZero | — | — | — | ⛔ zarchiwizowany 12.06.2026 |
| RouteLLM | — | — | — | ⛔ brak commitów od 2024 |

> 💡 **Uwaga do kursu 1.** [Część 9, §2.1](../kurs_lokalne_modele/09-KRAJOBRAZ-NARZEDZI.md) poleca LiteLLM — powstała
> przed incydentem z marca 2026. Dziś jako domyślną bramkę wybrałbym Bifrost, a LiteLLM tylko z przypiętymi wersjami.

---

## Wyszukiwanie i pobieranie stron

| Narzędzie | Do czego | Licencja | Lokalnie | Uwagi (2026) |
|---|---|---|---|---|
| [SearXNG](https://github.com/searxng/searxng) ⭐ | prywatne API wyszukiwania (U3, U1) | AGPL-3.0 | bez Dockera | **JSON domyślnie wyłączony** — dodaj `json` do `search.formats`, inaczej agent dostaje 403; publiczne instancje zwykle JSON blokują |
| [Crawl4AI](https://github.com/unclecode/crawl4ai) ⭐ | strona → czysty Markdown, ekstrakcja CSS/XPath bez LLM albo LLM przez llama-swap (U3, U2) | Apache-2.0 | biblioteka pip | używaj biblioteki, **nie wystawiaj serwera Docker API** — w 2026 seria poprawek bezpieczeństwa (RCE przez haki, ucieczki z piaskownicy) |
| [Trafilatura](https://github.com/adbar/trafilatura) | najtańsza ścieżka HTML → tekst dla newsów i RSS | Apache-2.0 | pip, bez przeglądarki | nie wykonuje JavaScriptu |
| [Scrapling](https://github.com/D4Vinci/Scrapling) | sklepy, które blokują zwykły crawler; wbudowany serwer MCP | BSD-3 | pip, Docker opcjonalnie | szanuj regulaminy stron; jeden opiekun; łamiące zmiany MCP w v0.4.15 |
| [Firecrawl](https://github.com/firecrawl/firecrawl) | API scrape / crawl / search | AGPL-3.0 | **Docker Compose** | wersja self-host nie ma silnika antybotowego chmury; obsługa lokalnych LLM „eksperymentalna" |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | przeglądarka przez drzewo dostępności — działa z modelami bez wizji | Apache-2.0 | `npx` | README samo zaleca Playwright CLI + skills dla agentów (mniej tokenów); „nie jest granicą bezpieczeństwa" |
| [agent-browser](https://github.com/vercel-labs/agent-browser) | przeglądarka jako CLI z referencjami elementów — mały kontekst dla lokalnych wykonawców | Apache-2.0 | npm / cargo | projekt eksperymentalny Vercel Labs |

---

## Agenci przeglądarkowi

| Narzędzie | Do czego | Licencja | Lokalnie | Uwagi (2026) |
|---|---|---|---|---|
| [browser-use](https://github.com/browser-use/browser-use) | domyślny otwarty agent przeglądarki: formularze, wieloetapowe zadania (U2, U3) | MIT | dowolny endpoint OpenAI-compatible | dokumentacja ostrzega, że małe modele zwracają złe schematy akcji; antybot i CAPTCHA tylko w płatnej chmurze |
| [Stagehand](https://github.com/browserbase/stagehand) | mieszanie skryptu z krokami LLM: `act` / `extract` / `observe` — przewidywalne przepływy (U2) | MIT | `baseURL` OpenAI-compatible | najlepsze funkcje (cache, Model Gateway) po stronie chmury Browserbase |
| [Skyvern](https://github.com/Skyvern-AI/skyvern) | powtarzalne formularze i portale, model wizyjny (U2) | AGPL-3.0 | `ENABLE_OPENAI_COMPATIBLE=true` | antybot i proxy tylko w chmurze; AGPL ważne przy wystawianiu jako usługa |
| [Nanobrowser](https://github.com/nanobrowser/nanobrowser) | rozszerzenie Chrome z agentami w Twojej zalogowanej przeglądarce (U3 doraźnie) | Apache-2.0 | własny dostawca OpenAI-compatible | nie działa bez okna — trudno planować i orkiestrować |

---

## Deep research

| Narzędzie | Do czego | Licencja | Lokalnie | Uwagi (2026) |
|---|---|---|---|---|
| [Local Deep Research](https://github.com/LearningCircuit/local-deep-research) ⭐ | planowane, cytowane raporty i „subskrypcje" tematów na SearXNG + llama-swap (U3, U2) | MIT | pip albo Docker | najbardziej lokalny z grupy, publikuje wyniki na modelach lokalnych; brak globalnego limitu subagentów (#6820) — ogranicz bramką |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | dojrzała biblioteka raportów z cytatami, którą woła orkiestrator (U3) | Apache-2.0 | `OPENAI_BASE_URL` + `FAST_LLM` / `SMART_LLM` | od v3.7.0 nie potrzebuje embeddingów (BM25); wymaga Pythona 3.12+ |
| [Vane](https://github.com/ItzCrazyKns/Vane) (dawniej Perplexica) | interaktywna wyszukiwarka z cytatami dla człowieka | MIT | OpenAI-compatible, Docker zalecany | słabszy jako klocek bez UI |
| [Deep Agents](https://github.com/langchain-ai/deepagents) | następca zarchiwizowanego (21.08.2026) Open Deep Research — framework, nie gotowa aplikacja | MIT | dowolny model LangChain | patrz [01-PROFILE.md](01-PROFILE.md#6-deep-agents) |
| STORM / Co-STORM | długie raporty w stylu Wikipedii | MIT | LiteLLM | ⛔ tryb utrzymania, brak aktywności w 2026 |

---

## Monitoring cen i zmian na stronach

| Narzędzie | Do czego | Licencja | Lokalnie | Uwagi (2026) |
|---|---|---|---|---|
| [changedetection.io](https://github.com/dgtlmoon/changedetection.io) ⭐ | pilnowanie cen i dostępności: tryb „Re-stock & Price", progi, historia cen, logowanie przez Browser Steps (U3) | Apache-2.0 | pip możliwy | od 0.55.x reguły AI („powiadom, gdy cena < 50") i streszczenia przez endpoint llama.cpp; REST API — agent sam zakłada obserwacje; powiadomienia przez Apprise |
| [Huginn](https://github.com/huginn/huginn) | wieloźródłowe potoki zdarzeń: RSS → filtr → LLM → Telegram (U3) | MIT | agent OpenAI z `base_url` | wrócił do życia w 2026 (wydania od 08.2026, głównie łatki bezpieczeństwa); Docker zalecany |
| [urlwatch](https://github.com/thp/urlwatch) | obserwacja adresów z crona albo timera systemd, bez Dockera i demona | BSD-3 | brak LLM (podepnij skrypt) | brak semantyki cen i UI |
| [PriceBuddy](https://github.com/jez500/pricebuddy) | tracker cen wielu sklepów z MCP | ⚠️ „GPL-3.0 z modyfikacjami" | Docker | AI tylko przez Ollama — sprawdź licencję przed użyciem zarobkowym |
| PriceGhost, Discount Bandit | — | ⛔ brak pliku licencji | — | prawnie „wszystkie prawa zastrzeżone" — omijaj |

---

## Dane finansowe

> ⚠️ Te narzędzia dają **dane i analizę**, nie porady inwestycyjne. Werdykty agentów (np. TradingAgents) to opinie,
> nie sygnały. Sprawdzaj warunki źródeł danych — część darmowych jest „tylko do użytku osobistego".

| Narzędzie | Do czego | Licencja | Lokalnie | Uwagi (2026) |
|---|---|---|---|---|
| [OpenBB ODP + openbb-mcp-server](https://github.com/openbq-org/OpenBB) ⭐ | jedna warstwa danych dla wielu dostawców (akcje, makro, opcje, krypto), oficjalny serwer MCP (U3) | **Apache-2.0 od V5** (30.09.2026; wcześniej AGPL) | pip | repozytorium przekierowuje teraz do `openbq-org/OpenBB`; dla małych modeli `--tool-discovery` i ograniczenie kategorii narzędzi |
| [edgartools](https://github.com/dgunning/edgartools) | raporty SEC, transakcje insiderów (Form 4), 13F; serwer MCP | MIT | pip | tylko spółki z USA; limit 10 zapytań/s (zasady SEC) |
| [CCXT + ccxt-mcp](https://github.com/ccxt/ccxt) | 100+ giełd krypto i rynków predykcyjnych, alerty cen i spreadów | MIT | `npx -y ccxt-mcp` | ⚠️ źle skonfigurowany serwer MCP **może składać zlecenia** — trzymaj agentów na poziomach tylko do odczytu |
| [TradingAgents](https://github.com/TauricResearch/TradingAgents) | „firma tradingowa" z analityków, debaty bull/bear i zarządcy ryzyka na jedną spółkę | Apache-2.0 | `llm_provider: "openai_compatible"` | od v0.6.0 osobny dostawca per poziom: Opus jako `deep_think`, lokalni analitycy jako `quick_think`; przy 13,6 tok/s wolny |
| [FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) | raporty o spółkach; liczby (DCF, WACC) liczy kod, LLM tylko pisze | Apache-2.0 | słabo — wymaga klucza API | dobry **wzorzec**: „LLM opowiada, kod liczy" |
| yfinance / Alpha Vantage / FRED | ceny, fundamenty, makro | kod Apache / MIT | pip / `uvx` | Yahoo: nieoficjalne endpointy, blokady 429, dane „do użytku osobistego"; Alpha Vantage free: 25 zapytań/dzień; FRED: darmowy klucz |

---

## Powiadomienia i kanały

| Narzędzie | Do czego | Licencja | Lokalnie | Uwagi (2026) |
|---|---|---|---|---|
| [ntfy](https://github.com/binwiederhier/ntfy) ⭐ | push na telefon jednym `curl -d "…" host/temat` — najprostsze narzędzie dla agenta | Apache-2.0 / GPLv2 | jeden plik binarny | dla natychmiastowych powiadomień na iOS ustaw `upstream-base-url` na ntfy.sh |
| [Apprise](https://github.com/caronc/apprise) ⭐ | jedna biblioteka → 100+ kanałów; routing w konfiguracji, nie w kodzie agenta | BSD-2 | pip | **v2.0.0 (26.09.2026) łamie API** (`notify()` zwraca obiekt) — przypnij 2.x |
| [Telegram Bot API](https://core.telegram.org/bots/api) | interaktywne alerty z przyciskami („odłóż", „otwórz ofertę"), rozmowa z agentem z telefonu, notatki głosowe jako wejście (wersje 10.1–10.3 z 2026 dodały m.in. formatowanie, wiadomości ulotne i nowe opcje wejścia głosowego) | darmowe | long polling — bez publicznego adresu | konto przypięte do numeru, usługa scentralizowana — nie wysyłaj tam danych służbowych |
| [Gotify](https://github.com/gotify/server) | w pełni samodzielny serwer wiadomości | MIT | jeden plik binarny | bez przekaźnika zewnętrznego |
| [Matrix](https://github.com/element-hq/synapse) | szyfrowane pokoje, które w całości są Twoje — dobre na incydenty U1 | AGPL-3.0 (Synapse) | pip / continuwuity jako plik binarny | największy narzut utrzymania |

---

## Harmonogram i trwałe wykonanie

| Narzędzie | Do czego | Licencja | Lokalnie | Uwagi (2026) |
|---|---|---|---|---|
| **timery systemd** ⭐ | „uruchom skrypt X co N minut"; `Persistent=true` nadrabia przegapione uruchomienia | system | natywnie | brak ponowień i współbieżności między zadaniami — skrypt musi być idempotentny |
| [Prefect](https://github.com/PrefectHQ/prefect) ⭐ | potoki Pythona: pobierz → wzbogać → alarmuj; ponowienia, cache, automatyzacje (U2, U3) | Apache-2.0 | `prefect server start` na SQLite, bez Dockera | oficjalny `PrefectAgent` w Pydantic AI |
| [DBOS Transact](https://github.com/dbos-inc/dbos-transact-py) | trwałe przepływy jako biblioteka, kolejki z limitem współbieżności (cap 4!) | MIT | tylko Postgres | backend trwałości Pydantic AI |
| [Temporal](https://github.com/temporalio/temporal) | wzorcowy silnik trwałego wykonania; długie przepływy z czekaniem na człowieka | MIT | `temporal server start-dev` | największy narzut i stroma krzywa nauki; integracje z większością frameworków |
| [Hatchet](https://github.com/hatchet-dev/hatchet) | zadania trwałe dla agentów, limity i klucze współbieżności | MIT | Postgres | — |
| [Trigger.dev](https://github.com/triggerdotdev/trigger.dev) | zadania TS z nazwanymi, współdzielonymi limitami współbieżności i cronem | Apache-2.0 | Docker / K8s | checkpointy i autoskalowanie tylko w chmurze |
| Inngest | zdarzeniowe funkcje krokowe | ⚠️ SSPL (każda wersja po 3 latach → Apache) | jeden plik binarny | licencja |

---

## Pamięć

| Narzędzie | Do czego | Licencja | Lokalnie | Uwagi (2026) |
|---|---|---|---|---|
| [Cognee](https://github.com/topoteretes/cognee) ⭐ | graf wiedzy + wektory z dokumentów, kodu i rozmów; serwer MCP (U1 runbooki, U2/U3 korpusy) | Apache-2.0 | wbudowany stos (SQLite + LanceDB), `LLM_PROVIDER=custom` | od v1.6.0 działa bez żadnego klucza chmurowego |
| [Graphiti](https://github.com/getzep/graphiti) | graf czasowy: fakty z oknem ważności („cena od–do", stan infrastruktury) | Apache-2.0 | `OpenAIGenericClient` | wymaga Neo4j (GPL) albo FalkorDB (SSPL); dużo wywołań LLM na epizod |
| [Mem0](https://github.com/mem0ai/mem0) | najprostsza pamięć preferencji i stanu asystenta | Apache-2.0 | dostawcy vLLM / LM Studio | **pamięć grafowa usunięta z wersji otwartej** (tylko platforma); OpenMemory MCP wygaszony (07.2026) |
| [Letta Code](https://github.com/letta-ai/letta-code) | agent z pamięcią jako rdzeniem, nie biblioteka | Apache-2.0 | lokalne: Ollama / LM Studio / llama.cpp | przeszedł na TypeScript; patrz [01-PROFILE.md](01-PROFILE.md#pozostali-kandydaci-miejsca-2164) |

---

## Obserwowalność i ewaluacja

| Narzędzie | Do czego | Licencja | Lokalnie | Uwagi (2026) |
|---|---|---|---|---|
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) ⭐ | ślady OpenTelemetry, ewaluacje, wbudowany serwer MCP — Opus może sam czytać ślady | ⚠️ Elastic License 2.0 | `pip install` + SQLite | najlżejsza pełna opcja; ELv2 OK do użytku własnego, nie jako usługa |
| [Langfuse](https://github.com/langfuse/langfuse) | najpełniejsza platforma: ślady, koszty, prompty, monitory z alertami | MIT (rdzeń) | Postgres + ClickHouse + Redis + S3 | ciężka do samodzielnego hostowania |
| [OpenLIT](https://github.com/openlit/openlit) | ślady + **monitoring GPU AMD** (użycie, pamięć, moc) skorelowany ze śladami; wykrywanie zapętlonych agentów | Apache-2.0 | ClickHouse | ciekawe dla 4× R9700 |
| [promptfoo](https://github.com/promptfoo/promptfoo) ⭐ | testy regresji promptów i wywołań narzędzi: DeepSeek kontra Opus na Twoich zadaniach, red teaming | MIT | dostawca llama.cpp | **przejęty przez OpenAI 9.03.2026**, nadal MIT; 0.124.0 przeniósł wiele SDK do instalacji opcjonalnej |

Kursy mają już własne narzędzia do ewaluacji — [kurs 2, część 14](../kurs_aplikacje_agentowe/14-EWALUACJA.md) i
[local-llm-quality-bench](https://github.com/michal-konik-human/local-llm-quality-bench).

---

## Piaskownice

| Narzędzie | Do czego | Licencja | Lokalnie | Uwagi (2026) |
|---|---|---|---|---|
| [sandbox-runtime (srt)](https://github.com/anthropic-experimental/sandbox-runtime) ⭐ | listy dozwolonych ścieżek i hostów dla dowolnego procesu — powłoki wykonawcy, lokalnych serwerów MCP | Apache-2.0 | bubblewrap + socat, bez Dockera | „wczesny podgląd badawczy"; przestrzenie nazw na wspólnym jądrze — słabsze niż mikro-VM |
| [bubblewrap](https://github.com/containers/bubblewrap) | prymityw pod srt; ręczne profile per komenda | LGPL | wymaga przestrzeni nazw użytkownika | to nie gotowa piaskownica — bezpieczeństwo zależy od argumentów; patrz [kurs 1, część 7](../kurs_lokalne_modele/07-SANDBOX-BEZPIECZENSTWO-MONITORING.md) |
| [microsandbox](https://github.com/superradcompany/microsandbox) ⭐ | mikro-VM (libkrun) dla niezaufanego kodu napisanego przez LLM; serwer MCP | Apache-2.0 | KVM, bez Dockera | beta, łamiące zmiany |
| [E2B runtime](https://github.com/e2b-dev/runtime) | standardowe SDK piaskownic dla frameworków | Apache-2.0 | Docker + KVM | tryb „Embed" na jednej maszynie |
| [gVisor](https://github.com/google/gvisor) | jądro w przestrzeni użytkownika dla kontenerów | Apache-2.0 | bez KVM | GPU tylko NVIDIA |
| Daytona | — | ⛔ rdzeń zamknięty 11.06.2026 | — | nie wybieraj do nowych projektów |

---

## Serwery MCP dla DevOps

Lokalne modele gubią się przy długich listach narzędzi — wybierz **2–3 serwery**, nie wszystkie (pułapka H5
w [01-PROFILE.md](01-PROFILE.md#siedem-pułapek-wspólnych-dla-wszystkich)).

| Serwer | Do czego | Licencja | Tryb bezpieczny | Uwagi (2026) |
|---|---|---|---|---|
| [kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) ⭐ | Kubernetes / OpenShift bezpośrednio przez API (nie nakładka na kubectl), wiele klastrów | Apache-2.0 | `read_only = true`, `disable_destructive = true`, `Secret` w `denied_resources` | `npx` / `uvx` / plik binarny; przed 1.0 |
| [mcp-grafana](https://github.com/grafana/mcp-grafana) ⭐ | Prometheus (PromQL), Loki (LogQL), Tempo, dashboardy, incydenty | Apache-2.0 | `--disable-write`, `--enabled-tools` | **v2.0.0 włączył anonimowe statystyki domyślnie** — wyłącz |
| [github-mcp-server](https://github.com/github/github-mcp-server) | CI, PR, issues, Dependabot | MIT | `--read-only`, wąskie `--toolsets` | v2.0.0 dodał typowane wyjścia dla „code mode" |
| GitLab MCP (wbudowany) | MR, CI, work items | GitLab | brak globalnego trybu tylko do odczytu | GA na wszystkich planach od GitLab 19.5; używaj konta o niskich uprawnieniach |
| [awslabs/mcp](https://github.com/awslabs/mcp) | EKS, ECS, IaC, CloudWatch | Apache-2.0 | wiele domyślnie tylko do odczytu | dziesiątki serwerów — wybierz 2–3 |
| [gcloud-mcp](https://github.com/googleapis/gcloud-mcp) | Cloud Logging, Monitoring, Trace | Apache-2.0 | lista zakazanych komend | podgląd, łamiące zmiany |
| [terraform-mcp-server](https://github.com/hashicorp/terraform-mcp-server) | dokumentacja dostawców i modułów, HCP Terraform | MPL-2.0 | — | `go install` bez Dockera |
| Datadog MCP | logi, metryki, ślady, monitory | zamknięty SaaS | role `mcp_read` / `mcp_write` | tylko zdalny |

---

## Głos

**Kluczowe ograniczenie:** DeepSeek-V4-Flash w 3 bitach zajmuje 104,2 GB, a z 4 slotami po 131k praktycznie
całe 128 GB VRAM. Każdy model mowy na GPU musi albo działać na CPU, albo dostać kartę zwolnioną przez llama-swap.

| Warstwa | Wybór | Licencja | Polski | Uwagi |
|---|---|---|---|---|
| Framework rozmowy | [Pipecat](https://github.com/pipecat-ai/pipecat) ⭐ | BSD-2 | ✅ przez Smart Turn | `base_url` dla LLM i STT — wpinasz llama-swap i whisper-server; pip, bez Dockera |
| Wykrywanie końca wypowiedzi | [Smart Turn v3.2](https://github.com/pipecat-ai/smart-turn) | BSD-2 | ✅ (94,47% wg ogłoszenia v3.0) | 8 MB, CPU, ~10–100 ms |
| Alternatywa frameworku | [LiveKit Agents](https://github.com/livekit/agents) | Apache-2.0 | ❌ detektory tury bez polskiego | tylko gdy potrzebujesz WebRTC albo telefonii |
| STT (główny) | [whisper.cpp](https://github.com/ggml-org/whisper.cpp) large-v3 | MIT | ✅ **WER 4,74% (FLEURS-pl)** — najlepszy otwarty | ROCm (HIP) udokumentowany; już go masz |
| STT (na CPU, odciąża GPU) | [Parakeet-TDT-0.6B-v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) przez parakeet.cpp / onnx-asr | CC-BY-4.0 | ✅ WER 7,31% | bardzo szybki, znaczniki czasu |
| STT do przetestowania | [Qwen3-ASR](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) w llama.cpp | Apache-2.0 | polski na liście, brak WER | działa w Twoim llama-swap (audio w llama.cpp eksperymentalne) |
| TTS polski (teraz) | [Piper](https://github.com/OHF-Voice/piper1-gpl) pl_PL | silnik GPL-3.0, głosy osobno | ✅ 5 głosów | CPU, prawie zero opóźnienia, brzmi robotycznie |
| TTS polski (lepszy) | [Chatterbox Multilingual V3](https://github.com/resemble-ai/chatterbox) | MIT (każde nagranie ma niewidoczny znak wodny) | ✅ | 0,5B; ROCm nieudokumentowany — zarezerwuj dzień na test |
| TTS polski (lepszy) | [VoxCPM2](https://github.com/OpenBMB/VoxCPM) | Apache-2.0 | ✅ | 2B, 48 kHz; wsparcie AMD niepotwierdzone |
| TTS angielski | [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) | Apache-2.0 | ❌ | mały i dobry — tylko EN |
| ⚠️ do omijania przy U2 | XTTS-v2, F5-TTS, Higgs Audio v3, Fish Audio S2 | niekomercyjne wagi | — | licencja blokuje użycie zarobkowe |

**Mowa-do-mowy (speech-to-speech) po polsku lokalnie na AMD — w październiku 2026 nie znalazłem działającego modelu.** Moshi to EN i CUDA,
Qwen3-Omni nie mówi po polsku, Unmute to EN/FR i CUDA. Działa tylko kaskada STT → LLM → TTS
(szczegóły i opóźnienia: [03-ARCHITEKTURA.md](03-ARCHITEKTURA.md#u4--rozmowa-głosowa-po-polsku)).

---

## Obraz

| Potrzeba | Wybór | Licencja | Uwagi |
|---|---|---|---|
| Czy główny wykonawca widzi? | **DeepSeek-V4-Flash jest tylko tekstowy.** Do testu: [DeepSeek-V4-Flash-Vision-Exp](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp) — ten sam rozmiar + ~0,93 GB mmproj | MIT | eksperymentalny, nietestowany na ROCm; wymaga llama.cpp ≥ b10766; obrazy + wywołania narzędzi naraz niezweryfikowane — trzymaj tekstowy GGUF jako zapas |
| Osobny wykonawca wizyjny (zrzuty ekranu, zdjęcia, wykresy) | [Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) (Q4 ~23 GB, 3B aktywnych) albo [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) (Q4 ~18,5 GB) | Apache-2.0 | mieści się na jednej R9700; zastępuje Qwen2.5-VL-7B z [kursu 1, części 5](../kurs_lokalne_modele/05-MULTIMODALNOSC.md); potrzebuje wolnej karty |
| Agent GUI (computer use) | [Holo4-35B-A3B](https://huggingface.co/Hcompany/Holo4-35B-A3B) | Apache-2.0 | ⚠️ omijaj Holo4-27B (CC-BY-NC) |
| Dokumenty i OCR | [Docling](https://github.com/docling-project/docling) + [PaddleOCR-VL-1.5](https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5) | MIT / Apache-2.0 | oficjalne wsparcie llama.cpp, mało VRAM; Docling ma serwer MCP |
| Generowanie i edycja obrazów | [ComfyUI](https://github.com/comfyanonymous/ComfyUI) na kołach PyTorch ROCm + [Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511), [Z-Image-Turbo](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo), [FLUX.2 klein 4B](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B) | ComfyUI GPL-3.0; modele Apache-2.0 | lżej: [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) `sd-server` za llama-swap; ⚠️ omijaj FLUX dev, Qwen-Image-2.1 (niekomercyjne) i modele Hunyuan (licencja wyklucza UE) |
| Trudne przypadki | wyślij obraz do Opusa 5.5 | — | kompromis koszt / prywatność |

---

## Niezawodność wywołań narzędzi i strojenie promptów

| Narzędzie | Do czego | Licencja | Uwagi |
|---|---|---|---|
| [forge](https://github.com/antoinezambelli/forge) | „warstwa niezawodności" dla lokalnych modeli: ratowanie zepsutych wywołań narzędzi, ponowienia, walidacja, wymuszone kroki; `SlotWorker` — kolejka priorytetowa do wspólnych slotów | MIT | wyniki (8B: z kilku do 84%) podaje sam autor; jeden opiekun; proxy przed llama-server |
| [DSPy](https://github.com/stanfordnlp/dspy) | „programowanie, nie promptowanie": optymalizator GEPA z Claude jako nauczycielem stroi prompty, które potem wykonuje lokalny model | MIT | najlepsze do precyzyjnej ekstrakcji i klasyfikacji ofert (U3); to nie runtime agentów |

---

## Minimalne zestawy na start

Wspólna baza dla U1–U3: **llama-swap** (masz) + **Bifrost** (limit 4, budżety) + **Phoenix** (ślady).

| Zastosowanie | Zestaw |
|---|---|
| **U1 — DevOps** | kubernetes-mcp-server (tylko odczyt) · mcp-grafana (`--disable-write`) · github-mcp-server albo GitLab MCP · srt wokół powłoki każdego wykonawcy · promptfoo do sprawdzenia, czy DeepSeek radzi sobie z Twoimi runbookami, zanim mu je oddasz |
| **U2 — dochód pasywny** | Prefect (albo DBOS z limitem kolejki 4) · Cognee jako pamięć · microsandbox dla kodu pisanego przez agentów · Apprise → ntfy dla „zatwierdź / gotowe / błąd" · promptfoo w CI |
| **U3 — rynki i okazje** | SearXNG (z JSON) · Crawl4AI jako biblioteka + Trafilatura · changedetection.io dla cen · OpenBB ODP + MCP, edgartools, CCXT tylko do odczytu · Local Deep Research dla cytowanych przeglądów · ntfy przez Apprise + bot Telegram · timery systemd, potem Prefect |
| **U4 — głos** | Pipecat + Smart Turn · whisper.cpp large-v3 (albo Parakeet na CPU) · gpt-oss-20b jako szybki „głos" delegujący do DeepSeeka / Opusa · Piper pl_PL, potem Chatterbox albo VoxCPM2 |
| **U5 — obrazy** | test Vision-Exp · Qwen3.6-35B-A3B jako wykonawca wizyjny · Docling + PaddleOCR-VL · stable-diffusion.cpp albo ComfyUI z modelami Apache-2.0 |

Jak te klocki łączą się z harnessem i planistą Opus — [03-ARCHITEKTURA.md](03-ARCHITEKTURA.md).
