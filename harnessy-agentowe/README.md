# Harnessy agentowe dla lokalnych modeli — przegląd

**Stan na 11 października 2026.** Które otwarte harnessy zamieniają lokalny model w agenta, czym się różnią,
który do czego wybrać — i kiedy lepiej złożyć własny. Ranking 20 najlepszych z 72 sprawdzonych, z profilami,
klockami i architekturą pod konkretny sprzęt.

> ⚠️ **Ten przegląd starzeje się w tygodniach.** W 2026 część popularnych projektów umarła albo zmieniła właściciela
> (Roo Code, Flowise, Continue, Aider), a nowe dorobiły się setek tysięcy gwiazdek w dwa miesiące. Gwiazdki i wydania
> pobrałem z API GitHuba 11.10.2026. **Niczego tu nie testowałem na swojej maszynie** — to przegląd dokumentacji,
> kodu, notatek wydań i zgłoszeń, nie pomiar. Twój pomiar wygrywa.

---

## Spis treści

- [Po co ten przegląd](#po-co-ten-przegląd)
- [Najkrótsza odpowiedź](#najkrótsza-odpowiedź)
- [Czym jest harness](#czym-jest-harness)
- [Ranking: 20 najlepszych harnessów](#ranking-20-najlepszych-harnessów)
- [Porównanie techniczne](#porównanie-techniczne)
- [Który do którego zastosowania](#który-do-którego-zastosowania)
- [Werdykt: budować na harnessie czy składać własny?](#werdykt-budować-na-harnessie-czy-składać-własny)
- [Dlaczego nie ma ich w czołówce](#dlaczego-nie-ma-ich-w-czołówce)
- [Jak liczyłem ranking](#jak-liczyłem-ranking)
- [Pliki w tym katalogu](#pliki-w-tym-katalogu)
- [Powiązane części kursów](#powiązane-części-kursów)

---

## Po co ten przegląd

Buduję aplikacje wieloagentowe, lokalne albo hybrydowe:

- **lokalnie** — do 4 agentów naraz na DeepSeek-V4-Flash (4× AMD Radeon AI PRO R9700, llama-swap, 4 sloty po 131k
  kontekstu, około 13,6 tok/s na agenta);
- **hybrydowo** — Claude Opus 5.5 jako planista i orkiestrator (najwięcej inteligencji), lokalni agenci jako
  wykonawcy (najmniejszy koszt pracy).

Pięć zastosowań, według których oceniam każdy harness:

| Skrót | Zastosowanie | Czego wymaga |
|---|---|---|
| **U1** | DevOps: rozwój i diagnozowanie | powłoka, kubectl, logi i metryki, bezpieczne uprawnienia, tryb bezgłowy |
| **U2** | dochód pasywny lub prawie pasywny | złożone, długie przepływy, trwałość, harmonogram, zatwierdzenia |
| **U3** | okazje na rynkach finansowych i świetne oferty sprzedaży | głębokie, precyzyjne i wydajne wyszukiwanie, monitoring, alerty |
| **U4** | rozmowa z agentami głosem | STT i TTS po polsku, krótkie opóźnienie |
| **U5** | praca ze zdjęciami i obrazami | model wizji, OCR, generowanie i edycja |

---

## Najkrótsza odpowiedź

- **Nie ma jednego harnessu do wszystkiego.** Najlepszy układ to trzy warstwy: gotowy agent kodujący dla U1, własne
  aplikacje na frameworku dla U2 i U3, osobisty asystent z głosem jako interfejs.
- **U1 → [OpenCode](01-PROFILE.md#8-opencode)** (albo [Goose](01-PROFILE.md#2-goose)): agent główny na Opus 5.5,
  subagenci na DeepSeeku, uprawnienia na wzorcach komend. Nie buduj tego sam.
- **U2 i U3 → własna aplikacja na [Pydantic AI](01-PROFILE.md#5-pydantic-ai)** (jedyny framework z wbudowanym limitem
  4 slotów) **albo [LangGraph](01-PROFILE.md#1-langgraph)** (najdojrzalsza trwałość) + klocki z [02-KLOCKI.md](02-KLOCKI.md).
  Bez kodu: [n8n](01-PROFILE.md#18-n8n).
- **U4 i U5 na start → [Hermes Agent](01-PROFILE.md#4-hermes-agent)**: notatki głosowe na Telegramie z lokalnym
  rozpoznawaniem mowy (faster-whisper), „mostek wizji" dla tekstowego DeepSeeka, najlepszy cron. Uwaga: synteza mowy
  domyślnie idzie przez chmurę (Edge TTS), a lokalny polski głos nie jest potwierdzony — w pełni lokalny głos z polskim
  Piperem ma [Moltis](01-PROFILE.md#15-moltis). Rozmowa na żywo po polsku — [Pipecat](02-KLOCKI.md#głos).
- **DeepSeek-V4-Flash nie widzi obrazów** i zajmuje praktycznie cały VRAM — głos i wizja muszą iść na CPU, na zwolnioną
  kartę albo do chmury ([03-ARCHITEKTURA.md](03-ARCHITEKTURA.md#1-zasoby-co-naprawdę-masz)).
- **Subagenci Claude Code na lokalnych modelach to nie jest wspierana funkcja.** Działa odwrotnie: Claude orkiestruje,
  lokalni agenci są jego narzędziami (MCP).
- **Lokalnie nie zawsze jest taniej.** Przy krótkich kontekstach Claude Haiku 5.5 (0,10 / 0,50 USD za milion tokenów)
  kosztuje mniej więcej tyle co prąd tej maszyny przy pełnym obciążeniu; przy kontekstach powyżej 100 tys. tokenów
  i w porównaniu z Sonnetem czy Opusem lokalny DeepSeek wychodzi wyraźnie taniej. Pewne zalety lokalne to prywatność,
  brak limitów i praca offline ([koszty](03-ARCHITEKTURA.md#5-koszty-czy-lokalnie-jest-taniej)).

---

## Czym jest harness

Model językowy sam nic nie robi — odpowiada tekstem. **Harness** to wszystko wokół niego, co zamienia go w agenta:
pętla (myśl → wywołaj narzędzie → przeczytaj wynik → znowu), narzędzia, zarządzanie kontekstem i pamięcią,
uprawnienia i piaskownica, harmonogram, kanały (terminal, czat, głos), obserwowalność. Pętlę od zera budujesz
w [kursie 1, części 6](../kurs_lokalne_modele/06-PETLA-AGENTA-OD-ZERA.md), a harness długich zadań
w [kursie 2, części 3](../kurs_aplikacje_agentowe/03-HARNESS-DLUGIE-ZADANIA.md).

W rankingu są cztery rodzaje harnessów:

| Rodzaj | Przykłady | Kiedy |
|---|---|---|
| **agent kodujący** — gotowy program w terminalu / IDE | OpenCode, Goose, OpenHands, Pi | U1; jako wykonawca w Twojej aplikacji |
| **osobisty agent zawsze włączony** — gotowy asystent z komunikatorami | Hermes Agent, ZeroClaw, Moltis | U4, U5, proste strażniki U3 |
| **framework** — biblioteka do budowy własnych agentów | LangGraph, Pydantic AI, Strands, Microsoft Agent Framework | U2, U3 — własne aplikacje |
| **platforma przepływów** — wizualne łączenie integracji | n8n | U2, U3 bez kodu |

---

## Ranking: 20 najlepszych harnessów

Kolumny „Czym jest", „Do czego służy" i „Jaki problem rozwiązuje" odpowiadają na pytanie, czym każdy wygrywa z konkurencją.
Szczegóły, konfiguracja lokalnego modelu, słabe strony i pomysły do ukradzenia — w [01-PROFILE.md](01-PROFILE.md).

<!-- main-table -->
| # | Harness | Kategoria | Czym jest | Do czego służy | Jaki problem rozwiązuje (przewaga) | Licencja |
|---|---|---|---|---|---|---|
| 1 | [LangGraph](01-PROFILE.md#1-langgraph) | framework Py | runtime agentów jako grafów stanów z checkpointem po każdym kroku | trwałe, wznawialne przepływy wieloagentowe z człowiekiem w pętli | przerwane zadanie wraca dokładnie tam, gdzie stanęło — także po restarcie; najdojrzalsza trwałość w Pythonie | MIT |
| 2 | [Goose](01-PROFILE.md#2-goose) | kodujący | agent ogólnego przeznaczenia w Ruście, pod fundacją AAIF (Linux Foundation) | kod, automatyzacje i powtarzalne „receptury" na własnej maszynie | receptury + cron + subagenci z własnym modelem w jednym narzędziu; eksperymentalny *tool shim* (tłumacz przez Ollamę albo wbudowany llama.cpp) ratuje modele, które słabo wołają narzędzia | Apache-2.0 |
| 3 | [OpenHands](01-PROFILE.md#3-openhands) | kodujący | platforma agentów kodujących + SDK + serwer agentów | „zespół inżynierów" działający stale: rozmowy, automatyzacje z crona i webhooków | najpełniejszy stos do osadzenia we własnej aplikacji; kontener na każdą rozmowę; agent wystawiony jako „model" OpenAI | MIT |
| 4 | [Hermes Agent](01-PROFILE.md#4-hermes-agent) | osobisty | samouczący się asystent z 25+ komunikatorami, głosem i cronem | osobisty agent dostępny z telefonu, zadania planowane, delegowanie | wzorzec „planista z czołówki, tani wykonawcy" wpisany w konfigurację; najmocniejszy cron; głos w komunikatorach z lokalnym rozpoznawaniem mowy | MIT |
| 5 | [Pydantic AI](01-PROFILE.md#5-pydantic-ai) | framework Py | typowany framework agentów od twórców Pydantic | produkcyjne agenty z walidowanym wyjściem strukturalnym | jedyny współdzielony limiter współbieżności na model — dokładnie 4 sloty; najlepsze wyjście strukturalne; trwałość przez Temporal / DBOS / Prefect | MIT |
| 6 | [Deep Agents](01-PROFILE.md#6-deep-agents) | framework Py | gotowy harness w stylu Claude Code na LangGraph | długie zadania: research, kod, ops — bez budowania hydrauliki | planowanie + system plików + subagenci + kompakcja w jednym wywołaniu, na trwałości LangGraph | MIT |
| 7 | [Strands Agents](01-PROFILE.md#7-strands-agents) | framework Py | SDK agentów od AWS + gotowy harness | własna pętla bez pisania własnej pętli, dowolny model i chmura | natywny dostawca llama.cpp z gramatykami i `cache_prompt` zamiast udawania OpenAI | Apache-2.0 |
| 8 | [OpenCode](01-PROFILE.md#8-opencode) | kodujący | agent kodujący z serwerem HTTP (TUI to tylko jeden klient) | programowanie i DevOps w terminalu; osadzanie przez API | architektura klient–serwer z OpenAPI; agenci i subagenci z własnym modelem i uprawnieniami na wzorcach komend | MIT |
| 9 | [DeerFlow](01-PROFILE.md#9-deerflow) | osobisty | „super-agent" ByteDance do długich zadań | badania, kod i treści z subagentami w piaskownicach | rodowód deep research + jawny model per subagent (dokumentowany „lokalny dla oszczędności") + zadania planowane z celem i warunkiem stopu | MIT |
| 10 | [ZeroClaw](01-PROFILE.md#10-zeroclaw) | osobisty | runtime agenta w jednym pliku binarnym Rust, 30+ kanałów | osobisty agent działający na Twoich narzędziach pod kontrolą | najgłębszy model bezpieczeństwa: profile ryzyka, poziomy autonomii, automatyczna piaskownica, podpisane potwierdzenia | MIT / Apache-2.0 |
| 11 | [Microsoft Agent Framework](01-PROFILE.md#11-microsoft-agent-framework) | framework Py | następca AutoGen i Semantic Kernel z silnikiem workflow | korporacyjne przepływy wieloagentowe z checkpointami | stabilne API z długim wsparciem; gotowe orkiestracje (Magentic, Handoff); ochrona przed prompt injection (FIDES) | MIT |
| 12 | [DeepSeek Harness](01-PROFILE.md#12-deepseek-harness) | kodujący | oficjalny harness DeepSeek złożony w całości z wtyczek | agent na modelach DeepSeek, osadzany w Web UI, CLI albo SDK | strojenie pod DeepSeek V4 od producenta; subagentami mogą być inne harnessy, także Claude Code | MIT |
| 13 | [Pi](01-PROFILE.md#13-pi) | kodujący | minimalny harness kodujący + biblioteki, na których stoją inne harnessy | własny agent na małym rdzeniu; nauka | mały rdzeń z najgłębszym API rozszerzeń; natywny llama.cpp; „wirtualne modele" kierujące każde zapytanie gdzie trzeba | MIT |
| 14 | [gptme](01-PROFILE.md#14-gptme) | kodujący | agent terminalowy i szkielet agentów autonomicznych | osobisty agent w terminalu, agenci działający stale z systemd | wymienny format narzędzi (Markdown / XML / natywny) — działa tam, gdzie parsowanie wywołań w llama.cpp zawodzi | MIT |
| 15 | [Moltis](01-PROFILE.md#15-moltis) | osobisty | osobisty serwer agenta w jednym pliku binarnym Rust | asystent z głosem, harmonogramem i piaskownicą bez instalowania pół internetu | najbardziej kompletny „jeden plik": lokalne STT / TTS, wybór piaskownicy, presety wykonawców z własnym modelem | MIT |
| 16 | [QwenPaw](01-PROFILE.md#16-qwenpaw) | osobisty | „Agent OS" od Alibaba AgentScope | wieloagentowy asystent z pamięcią i kanałami | wielowarstwowe bezpieczeństwo (piaskownica jądra, Tool Guard, skaner umiejętności) + model per agent | Apache-2.0 |
| 17 | [OpenAI Agents SDK](01-PROFILE.md#17-openai-agents-sdk) | framework Py | lekkie SDK z kilkoma prymitywami | proste systemy wieloagentowe, potoki głosowe | najprostszy model mentalny; serializowalny stan do zatwierdzeń po godzinach; potok głosowy z wymiennym STT / TTS | MIT |
| 18 | [n8n](01-PROFILE.md#18-n8n) | workflow | wizualna platforma automatyzacji z węzłami agentów | sklejanie integracji, alerty, przepływy bez kodu | najszerszy zestaw wyzwalaczy i integracji; zatwierdzanie per narzędzie wysyłane na komunikator | ⚠️ Sustainable Use (fair-code) |
| 19 | [LibreChat](01-PROFILE.md#19-librechat) | osobisty | wieloosobowa platforma czatu z agentami | wspólny czat dla wielu dostawców i lokalnych modeli, z agentami | prawdziwy wybór modelu per agent i zespoły subagentów jako grafy; interpreter kodu w mikro-VM | MIT |
| 20 | [Kilo Code](01-PROFILE.md#20-kilo-code) | kodujący | rozwidlenie OpenCode z UI w VS Code i JetBrains | kodowanie w IDE z subagentami | rdzeń OpenCode w IDE + menedżer równoległych agentów w osobnych worktree; migracja z martwego Roo Code | MIT |
<!-- /main-table -->

---

## Porównanie techniczne

✅ jest i działa z lokalnym modelem · ⚠️ częściowo albo z zastrzeżeniem · ❌ brak. „Hybryda" = czy jeden agent może działać
na Claude, a inni na Twoim llama-swap. Gwiazdki i wydania: API GitHuba, 11.10.2026.

| # | Harness | ⭐ GitHub | Ostatnie wydanie | Lokalny model | Hybryda | MCP | Głos | Obraz | Harmonogram | Piaskownica / zatwierdzenia |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | LangGraph | <!-- gh:langchain-ai/langgraph -->43,1k | 1.2.14 (6.10) | ✅ | ✅ model per węzeł | ✅ | ⚠️ kaskada DIY | ✅ | ⚠️ Agent Server | ⚠️ człowiek w pętli, bez piaskownicy |
| 2 | Goose | <!-- gh:aaif-goose/goose -->55,1k | 1.54.0 (8.10) | ✅ | ✅ `GOOSE_SUBAGENT_*` | ✅ | ⚠️ dyktowanie, bez TTS | ✅ | ✅ cron | ⚠️ tryby zatwierdzeń, bez piaskownicy |
| 3 | OpenHands | <!-- gh:OpenHands/OpenHands -->90,5k | 1.26.0 (8.10) | ✅ | ✅ profil per subagent | ✅ | ⚠️ tylko wejście | ✅ | ✅ cron, webhook | ✅ kontener na rozmowę |
| 4 | Hermes Agent | <!-- gh:NousResearch/hermes-agent -->252,7k | 0.21.6 (8.10) | ✅ | ✅ `delegation.*` | ✅ | ⚠️ STT lokalnie, TTS domyślnie w chmurze (Edge) | ✅ mostek wizji | ✅ najlepszy cron | ✅ smart approvals, Docker, SSH |
| 5 | Pydantic AI | <!-- gh:pydantic/pydantic-ai -->20,5k | 2.55.0 (9.10) | ✅ | ✅ + limit współbieżności | ✅ | ⚠️ realtime tylko chmura | ✅ | ❌ (Prefect / DBOS) | ⚠️ zatwierdzenia narzędzi |
| 6 | Deep Agents | <!-- gh:langchain-ai/deepagents -->30,1k | 0.7.23 (7.10) | ✅ | ✅ model per subagent | ✅ | ❌ | ⚠️ | ⚠️ Agent Server | ✅ backendy piaskownic |
| 7 | Strands Agents | <!-- gh:strands-agents/harness-sdk -->8,8k | harness 0.2.0 (8.10) | ✅ natywny llama.cpp | ✅ | ✅ | ⚠️ tylko chmura | ✅ | ❌ | ⚠️ |
| 8 | OpenCode | <!-- gh:anomalyco/opencode -->212,6k | 1.19.0 (11.10) | ✅ | ✅ model per agent | ✅ | ❌ | ✅ | ❌ | ⚠️ reguły allow / ask / deny |
| 9 | DeerFlow | <!-- gh:bytedance/deer-flow -->83,7k | 2.1.0 (24.09) | ✅ | ✅ model per subagent | ✅ | ❌ | ✅ | ✅ once / cron / interval | ✅ lokalnie, Docker, K8s |
| 10 | ZeroClaw | <!-- gh:zeroclaw-labs/zeroclaw -->33,0k | 0.8.5 (5.09) | ✅ slot `llamacpp` | ✅ agent per dostawca | ✅ | ✅ Piper, telefon | ✅ przekierowanie wizji | ✅ cron + procedury | ✅ Landlock / Bubblewrap |
| 11 | Microsoft Agent Framework | <!-- gh:microsoft/agent-framework -->14,1k | py 1.21.0 (8.10) | ⚠️ uwaga na Responses API | ✅ | ✅ | ❌ w Pythonie | ✅ | ❌ | ✅ FIDES, mikro-VM |
| 12 | DeepSeek Harness | <!-- gh:deepseek-ai/deepseek-harness -->247,3k | 0.2.1-alpha.2 (9.10) | ✅ profil `compat` | ✅ także Claude Code jako dziecko | ✅ | ⚠️ bez polskiego | ✅ | ✅ | ✅ domyślnie tylko odczyt |
| 13 | Pi | <!-- gh:earendil-works/pi -->114,2k | 1.1.0 (7.10) | ✅ natywny llama.cpp | ✅ wirtualne modele | ✅ | ❌ | ✅ | ❌ | ❌ z założenia |
| 14 | gptme | <!-- gh:gptme/gptme -->4,4k | 0.34.0 (18.09) | ✅ formaty Markdown / XML | ✅ | ✅ | ⚠️ realtime chmurowy | ✅ | ✅ systemd | ⚠️ polityka powłoki |
| 15 | Moltis | <!-- gh:moltis-org/moltis -->2,9k | 20260913.02 (14.09) | ✅ | ✅ presety | ✅ | ✅ lokalne STT / TTS | ⚠️ | ✅ cron, heartbeat | ✅ wybór piaskownicy |
| 16 | QwenPaw | <!-- gh:agentscope-ai/QwenPaw -->35,6k | 2.2.1 (11.09) | ✅ | ✅ model per agent | ✅ | ⚠️ błędy transkrypcji | ✅ | ✅ | ✅ piaskownica jądra |
| 17 | OpenAI Agents SDK | <!-- gh:openai/openai-agents-python -->30,0k | 0.23.1 (2.10) | ⚠️ uwaga na Responses API | ✅ Claude przez LiteLLM | ✅ | ⚠️ potok STT / TTS (lokalnie przez własne adaptery) | ✅ | ❌ | ✅ agenci w piaskownicy |
| 18 | n8n | <!-- gh:n8n-io/n8n -->207,0k | 2.42.6 (9.10) | ⚠️ wyłącz Responses API | ✅ model per węzeł | ✅ | ❌ do złożenia | ✅ | ✅ najlepsze wyzwalacze | ⚠️ zatwierdzenia, historia CVE |
| 19 | LibreChat | <!-- gh:LibreChat-AI/LibreChat -->45,5k | 0.8.8 (1.10) | ✅ | ✅ zespoły subagentów | ✅ | ✅ STT / TTS | ✅ | ⚠️ eksperymentalny | ✅ interpreter w mikro-VM |
| 20 | Kilo Code | <!-- gh:Kilo-Org/kilocode -->27,6k | JetBrains 7.1.9 (8.10) | ⚠️ błędy schematów | ✅ model per subagent | ✅ | ⚠️ chmurowy Whisper | ⚠️ | ❌ | ⚠️ reguły uprawnień |

Przed podłączeniem któregokolwiek do llama-swap przeczytaj
[siedem pułapek wspólnych dla wszystkich](01-PROFILE.md#siedem-pułapek-wspólnych-dla-wszystkich) — Responses API,
`reasoning_content` DeepSeeka, okno kontekstu, prompt cache, liczba narzędzi, limit współbieżności, schematy narzędzi.

---

## Który do którego zastosowania

Ocena 1–5 według badania dokumentacji (nie pomiaru). Pogrubione — najlepsze w kolumnie. Te liczby mierzą
dopasowanie funkcji do zastosowania i nie są rekomendacją: tabela „Co wybrać" niżej bierze pod uwagę także
gotowość do użycia (np. LangGraph ma 5 w U1, ale do DevOps lepiej wziąć gotowy OpenCode, niż budować agenta
na frameworku).

| # | Harness | U1 DevOps | U2 dochód pasywny | U3 rynki i okazje | U4 głos | U5 obrazy |
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

Co wybrać — i z jakimi klockami:

| Zastosowanie | Pierwszy wybór | Alternatywa | Kluczowe klocki ([02-KLOCKI.md](02-KLOCKI.md)) |
|---|---|---|---|
| **U1** DevOps | OpenCode (Opus główny, DeepSeek subagenci) | Goose; albo Claude Code + MCP do lokalnych agentów | kubernetes-mcp-server, mcp-grafana (tylko odczyt), srt |
| **U2** dochód pasywny | własna aplikacja: Pydantic AI albo LangGraph | n8n (bez kodu), OpenHands SDK (przepływy wokół kodu) | Prefect albo DBOS, Cognee, ntfy |
| **U3** rynki i okazje | własny lejek (timery + Pydantic AI) albo n8n | Hermes Agent (strażnicy cron), Local Deep Research | SearXNG, Crawl4AI, changedetection.io, OpenBB, ntfy / Telegram |
| **U4** głos | Hermes Agent (notatki głosowe od razu; TTS w chmurze) | Moltis (w pełni lokalnie, Piper po polsku); docelowo własny Pipecat | Pipecat + Smart Turn, whisper.cpp / Parakeet, Piper → Chatterbox |
| **U5** obrazy | Hermes Agent albo ZeroClaw (mostek wizji) | własny potok | DeepSeek Vision-Exp (test), Qwen3.6-35B-A3B, Docling + PaddleOCR-VL |

Jak to złożyć w całość na tym sprzęcie: [03-ARCHITEKTURA.md](03-ARCHITEKTURA.md).

---

## Werdykt: budować na harnessie czy składać własny?

**Oba — ale w różnych warstwach.**

| Warstwa | Decyzja | Dlaczego |
|---|---|---|
| Agent do pracy (U1) | **weź gotowy** — OpenCode albo Goose | to dojrzałe produkty z setkami opiekunów; własny nie dogoni ich w powłoce, edycji plików i uprawnieniach |
| Twoje aplikacje (U2, U3) | **zbuduj na frameworku** — Pydantic AI albo LangGraph | przewaga jest w dopasowaniu przepływu do pomysłu, a frameworki dają trwałość, limity i walidację bez narzucania produktu |
| Interfejs i głos (U4, U5) | **weź gotowy na start** — Hermes Agent; potem własny Pipecat | najszybsza droga do rozmowy z agentem z telefonu; przypinaj wersje, bo tempo zmian jest ogromne |
| Pętla agenta | **zbuduj raz sam, dla zrozumienia** — kursy 1 i 2 | kto zbudował pętlę od zera, ten wie, czego szukać w cudzym harnessie i kiedy go porzucić |

**Czego się uczyć z cudzego kodu** (czytelny rdzeń, dobre pomysły): [Pi](01-PROFILE.md#13-pi) — minimalny rdzeń
i wiele trybów osadzenia; [nanobot](https://github.com/HKUDS/nanobot) — czytelny Python do forkowania;
[mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) — agent w 100 liniach; [OpenCode](01-PROFILE.md#8-opencode) —
serwer z API i agenci jako pliki; [Hermes Agent](01-PROFILE.md#4-hermes-agent) — delegacja ze schematem wyniku
i strażnicy cron; [ZeroClaw](01-PROFILE.md#10-zeroclaw) — model bezpieczeństwa.

**Czego unikać:** martwych projektów (Roo Code, Flowise, Continue, Plandex); Codex CLI z modelami lokalnymi
(tylko Responses API); LiteLLM bez przypiętych wersji (kompromitacja PyPI 24.03.2026); n8n i OpenClaw wystawionych
do internetu.

---

## Dlaczego nie ma ich w czołówce

| Projekt | Miejsce | Powód |
|---|---|---|
| [OpenClaw](https://github.com/openclaw/openclaw) | 47 (64 pkt) | najpopularniejszy (391,7k ⭐) i z największą liczbą kanałów, ale **722 porady bezpieczeństwa opublikowane w 2026** (14 krytycznych, policzone przez API GitHuba), wg raportów branżowych z lutego 2026 setki złośliwych umiejętności w ClawHub i dziesiątki tysięcy instancji wystawionych do internetu; z lokalnymi modelami cicho gubione wywołania narzędzi i niszczony prompt cache. Jako studium architektury — świetny: [kurs 2, część 1](../kurs_aplikacje_agentowe/01-ARCHITEKTURY-AGENTOWE.md) |
| [Open WebUI](https://github.com/open-webui/open-webui) | 29 (69 pkt) | najlepsze UI dla lokalnych modeli, ale subagenci zawsze działają na modelu rodzica (brak hybrydy), 158 porad bezpieczeństwa w 2026 i licencja z klauzulą marki |
| [Cline](https://github.com/cline/cline) | 33 (68 pkt) | zmiany formatu narzędzi wielokrotnie psuły lokalne modele; dyktowanie to płatna usługa |
| [CrewAI](https://github.com/crewAIInc/crewAI) | 34 (68 pkt) | powracające „puste odpowiedzi" z modelami lokalnymi, telemetria domyślnie, harmonogram tylko w płatnej platformie |
| [Codex CLI](https://github.com/openai/codex) | 59 (57 pkt) | od 1.02.2026 tylko Responses API — z llama.cpp kruche; brak dostawcy Anthropic |
| Aider, Roo Code, Continue, Flowise, Plandex | wykluczone | zatrzymane albo zarchiwizowane w latach 2025–2026 — [szczegóły](01-PROFILE.md#wykluczeni-na-wejściu) |

---

## Jak liczyłem ranking

**1. Warunki wejścia** (wszystkie cztery): kod publiczny i licencja pozwalająca na self-hosting (źródłowo-dostępne
dopuszczone, ale oznaczone ⚠️); udokumentowane podłączenie lokalnego modelu przez endpoint zgodny z OpenAI
(bezpośrednio albo — oznaczone — pośrednio, przez adapter); aktywność — commit nie starszy niż 3 miesiące i wydanie
(także przedpremierowe) nie starsze niż 6 miesięcy przed 11.10.2026; projekt nie jest oficjalnie zakończony — dlatego
odpada np. Continue, którego opiekunowie ogłosili koniec projektu, choć ostatnie wydanie pochodzi z czerwca 2026.
Sprawdzonych: 72 projekty, przeszło 64, odpadło 8.

**2. Sześć kryteriów, każde 1–5, z wagami według moich celów:**

| Kryterium | Waga | Co oceniam |
|---|---|---|
| A — wielu agentów i hybryda | 25% | subagenci, model per agent, Claude jako planista z lokalnymi wykonawcami |
| B — obsługa lokalnego modelu | 20% | wywołania narzędzi z llama.cpp, dokumentacja, znane błędy, limit współbieżności |
| C — pokrycie zastosowań | 20% | średnia ocen U1–U5 (tabela wyżej), zaokrąglona |
| D — dojrzałość | 15% | gwiazdki, rytm wydań, liczba opiekunów, stabilność API |
| E — wartość do nauki | 10% | czytelność rdzenia, dokumentacja, rozmiar |
| F — bezpieczeństwo i kontrola | 10% | piaskownica, zatwierdzenia, historia luk |

Wynik = (25·A + 20·B + 20·C + 15·D + 10·E + 10·F) / 5, czyli 0–100. Remisy rozstrzyga C, potem gwiazdki.

**3. Punktacja czołówki** — zmień wagi i policz po swojemu:

| # | Harness | A | B | C | D | E | F | Wynik |
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

Pełna lista 64 kandydatów z wynikami i ośmiu wykluczonych — [01-PROFILE.md](01-PROFILE.md#pozostali-kandydaci-miejsca-2164).

**4. Jak zbierałem fakty.** Sześciu agentów badawczych przeszło równolegle dokumentację, README, notatki wydań
i zgłoszenia na GitHubie (osobni dla agentów osobistych, kodujących, frameworków Pythona, TypeScriptu i platform
przepływów, klocków oraz głosu, wizji i hybrydy). Liczby z GitHuba pobrałem sam z API. Najbardziej zaskakujące
twierdzenia sprawdziłem w źródle pierwotnym (m.in. liczba porad bezpieczeństwa OpenClaw i Open WebUI, kompromitacja
LiteLLM, zarchiwizowanie Flowise i Roo Code, usunięcie Chat Completions z Codex CLI, limiter w Pydantic AI, atak na
pakiety Mastra, karta modelu DeepSeek-V4-Flash, cennik Anthropic). Twierdzenia oparte tylko na blogach i materiałach
marketingowych oznaczam w profilach.

**Ograniczenia.** Kryteria A–F to ocena, nie pomiar. Gwiazdki to nie jakość (DeepSeek Harness zebrał 247 tys. w dwa
miesiące). Wyniki U1–U5 pochodzą z analizy dokumentacji. Żaden harness nie był uruchomiony na tej maszynie.

---

## Pliki w tym katalogu

| Plik | Co w nim jest |
|---|---|
| [README.md](README.md) | ten przegląd: ranking, porównanie, wybór, werdykt, metoda |
| [01-PROFILE.md](01-PROFILE.md) | siedem pułapek wspólnych, 20 profili (konfiguracja lokalnego modelu, hybryda, głos, obraz, bezpieczeństwo, słabe strony, co ukraść), pozostali kandydaci i wykluczeni |
| [02-KLOCKI.md](02-KLOCKI.md) | bramki, wyszukiwanie, przeglądarki, deep research, monitoring cen, dane finansowe, powiadomienia, harmonogram, pamięć, obserwowalność, piaskownice, MCP dla DevOps, głos, obraz |
| [03-ARCHITEKTURA.md](03-ARCHITEKTURA.md) | zasoby tej maszyny, wzorzec planista–wykonawcy, co jest udowodnione, pięć układów U1–U5, koszty, ścieżka budowy |
| [ZRODLA.md](ZRODLA.md) | źródła z datą sprawdzenia i tym, co z nich wziąłem |

## Powiązane części kursów

| Temat | Gdzie |
|---|---|
| pętla agenta od zera | [kurs 1, część 6](../kurs_lokalne_modele/06-PETLA-AGENTA-OD-ZERA.md) |
| krajobraz narzędzi (wcześniejszy, krótszy przegląd frameworków i agentów kodujących) | [kurs 1, część 9](../kurs_lokalne_modele/09-KRAJOBRAZ-NARZEDZI.md) |
| hybryda lokalny + Claude | [kurs 1, część 10](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md) |
| architektury agentowe i OpenClaw rozłożony na części | [kurs 2, część 1](../kurs_aplikacje_agentowe/01-ARCHITEKTURY-AGENTOWE.md) |
| harness długich zadań | [kurs 2, część 3](../kurs_aplikacje_agentowe/03-HARNESS-DLUGIE-ZADANIA.md) |
| MCP, CLI, A2A | [kurs 2, część 9](../kurs_aplikacje_agentowe/09-PROTOKOLY-MCP-CLI-A2A.md) |
| flota wielu agentów | [kurs 2, część 13](../kurs_aplikacje_agentowe/13-FLOTA-WIELU-AGENTOW.md) |
| router hybrydowy | [kurs 2, część 17](../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md) |
| gotowi asystenci AI (rynek, architektura, offline, Polska) | [przegląd asystentów AI](../asystenci-ai/README.md) |

Pomiary tej maszyny: [local-llm-bench-results](https://github.com/michal-koniu/local-llm-bench-results)
(szybkość i jakość, także [agenci równolegle](https://github.com/michal-koniu/local-llm-bench-results/blob/main/PARALLEL.md)).

Licencja tekstu: CC BY 4.0 — jak całe repozytorium ([LICENSE.md](../LICENSE.md)).
