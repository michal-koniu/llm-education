# Profile asystentów — piętnastka i reszta stawki

**Stan na 11 października 2026.** Każdy profil ma dziewięć obszarów: otwarty czy zamknięty, cel, funkcje, przewaga,
architektura, na czym zarabia, offline, co przenieść do siebie i warto wiedzieć. Liczby mają datę i źródło; dane
podawane przez firmy oznaczam *(dane firmy)*. Ranking i wagi: [README.md](README.md#jak-wybierałem). Legenda wyniku:
T — trakcja (35%), I — pomysł (25%), L — wartość do nauki (25%), A — przejrzystość architektury (15%), każde 1–5.

## Spis treści

- Profile: [1. OpenClaw](#1-openclaw) · [2. Claude](#2-claude) · [3. Abridge](#3-abridge) · [4. Harvey](#4-harvey) · [5. Hermes Agent](#5-hermes-agent) · [6. Manus](#6-manus) · [7. ChatGPT](#7-chatgpt) · [8. Gemini](#8-gemini) · [9. Cursor](#9-cursor) · [10. Granola](#10-granola) · [11. Sierra](#11-sierra) · [12. OpenEvidence](#12-openevidence) · [13. browser-use](#13-browser-use) · [14. Noxtua](#14-noxtua) · [15. Perplexity](#15-perplexity)
- [Warto znać — kto nie zmieścił się w piętnastce](#warto-znać--kto-nie-zmieścił-się-w-piętnastce)

---

## 1. OpenClaw

**Kategoria:** żyjący autonomicznie · **Kod:** otwarty (MIT) · ⭐ <!-- gh:openclaw/openclaw -->391,7k ·
**Firma:** OpenClaw Foundation (USA, non-profit 501(c)(3)); twórca Peter Steinberger · **Wynik: 100** (T5 I5 L5 A5)

> Demon na własnym komputerze, z którym rozmawiasz z WhatsAppa, Signala albo Teams i który sam się budzi (heartbeat,
> cron, e-mail) — archetyp asystenta „żyjącego własnym życiem" w 2026 roku i największy ekosystem w kategorii:
> najwięcej gwiazdek, kanałów i umiejętności, a od września 2026 także fundament produktu Microsoftu.

**Otwarty czy zamknięty.** Cały kod na MIT; ostatnie wydanie v2026.10.1 (10.10.2026). Self-hosting to tryb
podstawowy („runs on your hardware, your rules"). Na tym samym kodzie powstają dystrybucje firmowe: Microsoft
Autopilot (zamknięty produkt, poprawki wracają do upstreamu), NVIDIA NemoClaw (Apache-2.0) i OpenClaw Enterprise
(darmowy).

**Cel.** Osobisty agent pracujący 24/7 na sprzęcie właściciela i odpowiadający tam, gdzie właściciel już pisze —
bez nowej aplikacji. Na początku 2026 używali go majsterkowicze i programiści, potem freelancerzy i małe firmy
(np. pozyskiwanie leadów), a jesienią 2026 korporacje przez Microsoft Autopilot i OpenClaw Enterprise. Problem, który
rozwiązuje: „agent, który robi rzeczy, kiedy cię nie ma".

**Funkcje.**
- Jedna bramka (*Gateway*) dla kilkunastu kanałów: Discord, Google Chat, iMessage, Matrix, Microsoft Teams, Signal,
  Slack, Telegram, WhatsApp, Zalo, WeChat, Feishu, SMS, e-mail i inne.
- Automatyzacje: cron, webhooki, wyzwalacze Gmail Pub/Sub i IMAP oraz **heartbeat** (cykliczna tura agenta).
- **Standing orders** („stałe polecenia"): program z zakresem, wyzwalaczem, bramką zatwierdzenia i eskalacją,
  który agent prowadzi bez pytania o każde zadanie.
- Pamięć w SQLite (słowa kluczowe, wektory, hybryda) i nocne „śnienie" (*dreaming*), które ją konsoliduje.
- Umiejętności jako foldery `SKILL.md` i rejestr **ClawHub**; wtyczki dla kanałów, dostawców i narzędzi.
- Głos na Discordzie, „węzły" iOS/Android, przekaźnik przeglądarki, zespoły agentów, A2A; wersja 2.0 (v2026.8.1,
  30.08.2026) dodała prostszy instalator, nowe UI w przeglądarce i współdzielone sesje w chmurze.

**Przewaga.**
- **Dystrybucja i efekt sieci.** Najbardziej „ugwiazdkowane" repozytorium agentowe (391,7k ⭐, API GitHuba
  11.10.2026); ClawCon — 34 wydarzenia w 16 krajach, ok. 30 tys. zapisów *(dane fundacji, 8.07.2026)*.
- **UX komunikatora.** Agent mieszka w czacie, którego już używasz — próg wejścia jest bliski zera.
- **Platforma, nie produkt.** Wielcy gracze budują na nim zamiast z nim konkurować: Microsoft, NVIDIA, OpenAI,
  Tencent, Red Hat. Kto pisze wtyczkę albo umiejętność, trafia od razu do wszystkich dystrybucji.
- **Zachowanie w czytelnych plikach**, które właściciel może otworzyć, poprawić, wersjonować i cofnąć.

**Architektura.**
```
kanały (WhatsApp, Signal, Teams, e-mail…) ─┐
cron · webhook · IMAP · heartbeat ─────────┼─► Gateway: jeden długożyjący proces, domyślnie tylko loopback
                                           │     sesja z miejsca pochodzenia: konsola → main, DM → sesja DM,
                                           │     grupa → sesja grupy (każda z własnym zaufaniem i piaskownicą)
                                           └─► pętla agenta ─► model: dowolny dostawca albo lokalny
                                                 ├─ prompt z plików: AGENTS.md SOUL.md IDENTITY.md USER.md
                                                 │  BOOTSTRAP.md MEMORY.md (wstrzykiwane w każdej sesji)
                                                 ├─ narzędzia: powłoka, pliki, przeglądarka, skills, wtyczki
                                                 └─ pamięć: SQLite + dreaming → DREAMS.md → MEMORY.md
```
- **Bramka** jest jedynym źródłem prawdy o sesjach, routingu i kanałach. Nieznany nadawca DM dostaje kod parowania,
  w grupach działają listy dozwolonych i wymóg wzmianki; `openclaw security audit` sprawdza konfigurację.
  **Zaufanie to właściwość sesji** wyliczana ze źródła wiadomości, a nie flaga przy narzędziu.
- **Heartbeat** to zadanie systemowe: domyślnie co 30 min (co 1 h przy OAuth Anthropic) — „periodic agent turns
  in the main session"; wybudzenia zdarzeniami co najmniej 30 s od siebie, blokada po 5 startach w 60 s.
- **Dreaming**: fazy light, REM i deep w tle; wynik trafia do `DREAMS.md`, a do `MEMORY.md` awansują tylko mocne
  wpisy z wagą 1–10 i frazami-wyzwalaczami.
- **Rdzeń odchudzony** od IV 2026: kanały, dostawcy i ciężkie narzędzia przeszły do wtyczek; „plugins can act as
  harnesses" (np. Codex dla modeli GPT).
- **Piaskownica opcjonalna**: „the workspace is the default cwd, not a hard sandbox" — w 2.0 nadal domyślnie wyłączona.
- **Modele lokalne**: wtyczka llama.cpp dobierająca przepis do RAM/VRAM, Ollama (natywne `/api/chat`; endpoint `/v1`
  wg dokumentacji „breaks tool calling"), LM Studio, vLLM, MLX, `ds4` dla DeepSeek V4 Flash na Metalu.
- Rozbiór bramki i sesji: [kurs 2, część 1](../kurs_aplikacje_agentowe/01-ARCHITEKTURY-AGENTOWE.md); pułapki
  z lokalnym modelem: [przegląd harnessów](../harnessy-agentowe/README.md#dlaczego-nie-ma-ich-w-czołówce).

**Na czym zarabia.** Sam projekt nie zarabia — zarabiają na nim inni.
- **Fundacja** (ogłoszona 8.07.2026): amerykańska 501(c)(3), 12 pełnych etatów *(dane fundacji)*. Darczyńcy
  i partnerzy: University of Michigan (największy darczyńca; założył Institute for Agentic Computing), OpenAI
  („major donor", finansuje też inferencję), NVIDIA, Microsoft, Red Hat, Tencent, Atlassian; infrastruktura od
  Vercel, Cloudflare, GitHub i innych. **Kwot fundacja nie podaje.**
- **Dystrybucje komercyjne**: Microsoft Autopilot (ewolucja Microsoft Scout, część Copilota; ogłoszony 25.09.2026,
  prywatny podgląd od końca IX 2026, cena nieznana); NVIDIA NemoClaw (NVIDIA sprzedaje GPU i DGX); usługi Tencent
  i Z.ai w Chinach (III 2026, *wg prasy*). OpenClaw Enterprise (29.09.2026, z OpenAI, Red Hat i NVIDIA) „will always
  be free" *(dane fundacji)*. W ClawHub nie znalazłem płatnych listingów ani podziału przychodów.
- Twórca, Peter Steinberger, przeszedł do OpenAI 14–15.02.2026 i prowadzi tam „Claw Labs"; Sam Altman zapowiedział, że
  projekt zostanie w fundacji jako open source wspierany przez OpenAI.

**Offline.** **Częściowo** — rdzeń tak, kanały nie. Pętla agenta, pamięć, heartbeat i cron działają z lokalnym
modelem; CLI, TUI i lokalne UI w przeglądarce nie potrzebują sieci. Najmniejszy gotowy przepis llama.cpp wymaga
≥8 GiB pamięci przy 64K kontekstu. WhatsApp, Telegram, Signal i reszta komunikatorów z natury wymagają internetu.
Dokumentacja ostrzega: „local models do not provide hosted providers' safety filters". W przeglądzie harnessów
z llama.cpp wyszły dwa problemy: ciche gubienie wywołań narzędzi i zmienny początek promptu, który niszczy prompt
cache ([pułapka H4](../harnessy-agentowe/01-PROFILE.md#siedem-pułapek-wspólnych-dla-wszystkich)).

**Co przenieść do siebie.**
- **Zachowanie w plikach, które klient może przeczytać.** `SOUL.md` (ton), `USER.md` (kim jest klient), `MEMORY.md`
  (co asystent wie). W kancelarii to zarazem dokumentacja: „co system o mnie wie" otwiera się w edytorze.
- **Standing orders jako umowa kompetencyjna:** „prowadzisz codzienną selekcję skrzynki; nic nie wysyłasz poza
  kancelarię; pismo z sądu eskalujesz do mnie od razu". Cztery pola: zakres, wyzwalacz, bramka, eskalacja.
- **Zaufanie per sesja:** konsola właściciela — pełne uprawnienia; wiadomość z zewnętrznego kanału — sesja bez
  powłoki i bez akt. Dla zawodów z tajemnicą zawodową to wymaganie, nie opcja.
- **Heartbeat to zwykła zaplanowana tura** z krótką listą kontrolną i limitami antyspamowymi. Na rigu zarezerwuj
  jeden z 4 slotów DeepSeek-V4-Flash na heartbeat i cron, żeby tło nie blokowało rozmowy; pamięć konsoliduj w nocy
  (`DREAMS.md`), gdy wszystkie sloty są wolne.
- **Czego nie kopiować:** otwartego rynku umiejętności bez weryfikacji, piaskownicy „opcjonalnej" i sekretów bez
  szyfrowania. OpenClaw w kancelarii — tylko w opakowaniu typu NemoClaw (piaskownica, lista dozwolonych adresów,
  zatwierdzenia operatora).

**Warto wiedzieć.**
- **Pięć nazw w dwa miesiące:** Warelay (24.11.2025) → CLAWDIS → Clawdbot → Moltbot (27.01.2026, po skardze
  Anthropic na znak towarowy) → OpenClaw (29–30.01.2026). W pierwszym tygodniu >100 tys. gwiazdek i 2 mln odwiedzin;
  Cloudflare pisało o „flood of people buying Mac minis" pod agenta (29.01.2026).
- **Bezpieczeństwo to cena popularności:** 722 porady bezpieczeństwa opublikowane w 2026 (14 krytycznych, 249
  wysokich, 390 średnich, 69 niskich; API GitHuba, 11.10.2026). Steinberger (30.04.2026): z 1309 zgłoszeń od 10.01
  aż 746 było nieważnych, a z 109 „krytycznych" — 95 (87%). Audyty ClawHub: 341 złośliwych umiejętności na 2857
  (II 2026) i 1103 na 14 706 (III 2026) — *tylko źródło wtórne*. Cisco (28.01.2026): umiejętność po cichu wysyłała
  dane `curl`em; 26% z 31 tys. przeanalizowanych umiejętności miało co najmniej jedną podatność.
- **Odpowiedź ekosystemu:** skanowanie VirusTotal (7.02.2026), NVIDIA SkillSpector i Skill Cards (1.06.2026),
  Tencent AI-Infra-Guard w ClawScan (2.10.2026; 98,6% złośliwych umiejętności wykrytych na 556 przypadkach
  testowych, *dane fundacji*). Mimo to The Register (31.08.2026) o wersji 2.0: sekrety bez szyfrowania, piaskownica
  domyślnie wyłączona. Fundacja sama przyznaje, że domyślna postawa działów IT to zakaz takich agentów.
- **Autonomia bez nadzoru kompromituje:** MoltMatch (II 2026) — agent sam założył właścicielowi profil randkowy;
  inny „zhakował" listę oczekujących na siłowni. W Moltbooku, sieci tylko dla agentów, Wiz znalazł 1,5 mln
  odsłoniętych tokenów API; Meta i tak kupiła serwis (10.03.2026).
- **Od „wirusa" do produktu:** Nadella w II 2026 porównał OpenClaw do wirusa, we wrześniu Microsoft wypuścił na nim
  Autopilota i wysyła poprawki upstream (zgodność z polityką firmy, Windows/WinUI, Teams, ukrywanie sekretów w monitach
  o zatwierdzenie). Chiny w III 2026 ograniczyły OpenClaw w bankach i urzędach, a Shenzhen w tym samym czasie go dotował.
- **Ten sam projekt, inna ocena:** w [przeglądzie harnessów](../harnessy-agentowe/01-PROFILE.md#pozostali-kandydaci-miejsca-2164)
  OpenClaw jest na 47. miejscu (64 pkt), bo tam liczyły się praca z lokalnym modelem, hybryda i bezpieczeństwo.
  Tu oceniam asystenta jako produkt i lekcję rynkową — i tu wygrywa trakcją oraz ideą. Oba wnioski są zgodne:
  świetne studium architektury, ryzykowna baza produkcyjna.

**Źródła:** [GitHub](https://github.com/openclaw/openclaw) · [wprowadzenie](https://openclaw.ai/blog/introducing-openclaw) · [fundacja](https://openclaw.ai/blog/introducing-openclaw-foundation) · [OpenClaw Enterprise](https://openclaw.ai/blog/openclaw-enterprise) · [Microsoft Autopilot](https://openclaw.ai/blog/microsoft-autopilot-openclaw) · [bezpieczeństwo jawnie](https://openclaw.ai/blog/openclaw-security-in-public) · [trudny tydzień](https://openclaw.ai/blog/openclaw-rough-week) · [VirusTotal](https://openclaw.ai/blog/virustotal-partnership) · [NVIDIA SkillSpector](https://openclaw.ai/blog/openclaw-nvidia-skill-security) · [ClawScan](https://openclaw.ai/blog/tencent-aig-joins-clawscan) · [heartbeat](https://docs.openclaw.ai/gateway/heartbeat) · [standing orders](https://docs.openclaw.ai/automation/standing-orders) · [dreaming](https://docs.openclaw.ai/concepts/dreaming) · [workspace](https://docs.openclaw.ai/concepts/agent-workspace) · [modele lokalne](https://docs.openclaw.ai/gateway/local-models) · [Ollama](https://docs.openclaw.ai/providers/ollama) · [security](https://docs.openclaw.ai/gateway/security) · [TechCrunch: Steinberger w OpenAI](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/) · [The Register o 2.0](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) · [Cloudflare Moltworker](https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/) · [Cisco](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare) · [InsiderLLM: audyty ClawHub](https://insiderllm.com/guides/openclaw-clawhub-security-alert/) · [Wiz: Moltbook](https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys) · [Wikipedia: OpenClaw](https://en.wikipedia.org/wiki/OpenClaw) · [Wikipedia: Moltbook](https://en.wikipedia.org/wiki/Moltbook)


---

## 2. Claude

**Kategoria:** codzienny + profesjonalny + wykonawca · **Kod:** zamknięty (otwarte: demo computer use, schematy
narzędzi) · **Firma:** Anthropic (USA) · **Wynik: 97** (T5 I5 L5 A4)

> Jedna rodzina asystentów na jednym modelu — czat z pamięcią, Cowork do pracy na plikach, Claude in Chrome, computer
> use w API i Claude Code w terminalu — w której agent kodujący stał się szablonem dla całej reszty („Claude Code for
> the rest of your work").

**Otwarty czy zamknięty.** Modele i aplikacje są zamknięte. Otwarte: referencyjne demo computer use (kontener Docker
z Xvfb, Firefoxem, LibreOffice, pętlą agenta i UI) oraz publicznie opisane schematy narzędzi. Kod klienta Claude Code
wyciekł w III 2026 przez opublikowany plik source map (Ars Technica wg Wikipedii) — nie czyni go to otwartym.
Self-hostingu modelu nie ma; najbliżej suwerenności jest Bedrock, Vertex albo Microsoft Foundry w wybranym regionie.

**Cel.**
- **Czat** (Pro, Max, Team, Enterprise) — codzienny asystent z pamięcią, konektorami i umiejętnościami.
- **Cowork** — agent dla nietechnicznych pracowników wiedzy (dokumenty, arkusze, prezentacje we wskazanych folderach);
  **Claude in Chrome i computer use** — wykonawca w przeglądarce i na pulpicie, w API także dla twórców RPA i QA.
- **Claude Code** — programiści w terminalu, IDE, aplikacji desktop i webie; w II 2026 ponad połowa przychodu Claude
  Code pochodziła z firm *(dane firmy)*.
- **Wersje branżowe** — „Claude for Legal" z wtyczkami dla specjalizacji i konektorami MCP do Westlaw, Box i Docusign
  (12.05.2026).

**Funkcje.**
- **Pamięć** (25.08.2026): jedna dla czatu i Cowork, zapisana jako czytelne pliki tematyczne do edycji i usunięcia;
  tematy wrażliwe (zdrowie, przekonania itd.) **domyślnie nie są zapisywane**.
- **„Jeden Claude"** (16.09.2026): Cowork scalony z czatem; zadania pracują dalej „even after you've closed your
  laptop" i dają się planować („Schedule it for every Monday"); domyślnie Claude pyta przed działaniem. Wcześniej
  **Dispatch** (23.03.2026, z computer use, research preview w Pro i Max): zadanie z telefonu wykonywane na komputerze.
- **Claude in Chrome**: panel boczny, który nawiguje, wypełnia formularze, pracuje w kilku kartach we własnej grupie,
  uruchamia zadania w tle i według harmonogramu; GA na wszystkich płatnych planach.
- **Computer use i browser use w API** (GA, toolsety `*_20260801`): 17 narzędzi pulpitu z akcjami wsadowymi (stop na
  pierwszym błędzie) i 31 narzędzi przeglądarki opartych na drzewie dostępności; wykonuje je **Twoje** środowisko.
- **Claude Code**: pętla w terminalu (pliki, powłoka), MCP, subagenci, hooki, umiejętności, wtyczki, plik
  `CLAUDE.md`; sesje w chmurze (VM Anthropic albo środowisko klienta), Remote Control, Routines (14.04.2026).
  Konektory, umiejętności i wtyczki działają też w czacie, Cowork i Chrome.

**Przewaga.**
- **Model i agent z jednego laboratorium.** OSWorld: 14,9% (22.10.2024) → 61,4% (29.09.2025) → 72,5% (II 2026, przy
  poziomie człowieka 72,36%) → 81,8% „partial" na OSWorld 2.1 dla Opus 5.5 (22.09.2026) *(dane firmy)*.
- **Claude Code jako lokomotywa.** >2,5 mld USD run-rate (12.02.2026) i ok. 4% publicznych commitów na GitHubie
  (II 2026) *(dane firmy)*; w ankiecie Stack Overflow 2026 najczęściej używany agent kodujący (66% użytkowników
  agentów, 6.10.2026).
- **Wspólny harness pod wszystkim.** Cowork zbudowano na stosie Claude Code / Agent SDK; ten sam SDK wybrał Thomson
  Reuters pod nowy CoCounsel (VI 2026), a NanoClaw — jako rdzeń. Wzorce wygrane u programistów (plik projektu,
  umiejętności, hooki) przechodzą do biura.
- **Opublikowane liczby obrony przed prompt injection:** skuteczność ataku w Chrome 23,6% → 11,2% po zabezpieczeniach
  (25.08.2025); ok. 1% dla Opus 4.5 przy adaptacyjnym atakującym (24.11.2025) — Anthropic dodaje, że to „still
  represents meaningful risk". Do tego dystrybucja: Cowork, Chrome i Claude Code są w cenie planów Pro, Max i Team.

**Architektura.**
```
model w chmurze (Anthropic API / Bedrock / Vertex / Foundry)
   ▲  prompty, wyniki narzędzi, zrzuty ekranu
   │
   ├─ czat + Cowork ──── izolowane środowisko z udostępnionymi folderami + osobna przeglądarka agenta
   ├─ Claude in Chrome ─ rozszerzenie w prawdziwej, zalogowanej przeglądarce użytkownika
   ├─ API computer/browser use ─ akcje wykonuje piaskownica dewelopera („nothing executes on Anthropic's servers")
   └─ Claude Code ────── lokalny CLI: pliki, powłoka, hooki, MCP, subagenci; transkrypcje na dysku
```
- **Pętla computer use:** toolset → `tool_use` → aplikacja wykonuje akcję → odsyła zrzut (ok. 1000–1800 tokenów) →
  powtórka; zalecenia: 1024×768–1280×800, ≤20 obrazów, prompt caching, przycinanie starych zrzutów partiami.
- **Browser use** czyta drzewo dostępności (mniej tokenów niż zrzuty), a odwołania do elementów przetrwają przesunięcia
  układu. Walidacja URL (odrzucanie `javascript:`, `file:`, `data:`) należy do dewelopera; upload i JS domyślnie wyłączone.
- **Gdzie pracuje Cowork:** w styczniu 2026 (research preview) w **lokalnej VM Linux** na frameworku Apple
  Virtualization, z montowaniem tylko udostępnionych folderów i ograniczoną siecią (analiza Simona Willisona). Obecny
  artykuł pomocy mówi: „Cowork runs your tasks in the cloud" — w izolowanym środowisku na serwerach Anthropic;
  uprawnienia ruchu wychodzącego **nie obejmują** web fetch, web search ani MCP. Model zawsze działał w chmurze.
- **Chrome:** uprawnienia per witryna, potwierdzenia przed publikacją, zakupem i udostępnieniem danych osobowych,
  zablokowane kategorie (m.in. usługi finansowe), klasyfikatory wstrzyknięć, trening RL na wrogich treściach.
- **Claude Code — dane:** transkrypcje lokalnie przez 30 dni; retencja: firmy 30 dni, Enterprise — zero data retention
  po uzgodnieniu, konsumenci 30 dni albo 5 lat przy zgodzie na trening; `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`
  wyłącza zbędny ruch; w chmurowych VM dane logowania GitHuba nie wchodzą do maszyny.

**Na czym zarabia.**
- **Abonamenty** (wg stanu na 10.2026): Pro 20 USD/mies. (17 USD przy płatności rocznej), Max 100 i 200 USD,
  Team 20 USD za stanowisko (2–150 osób), Enterprise — indywidualnie. Chrome najpierw tylko w Max (pilot od
  25.08.2025), od 18.12.2025 także w Pro, Team i Enterprise.
- **API za tokeny:** Opus 5.5 — 4 / 20 USD za 1 mln tokenów wejścia/wyjścia (22.09.2026); Sonnet 4.6 — 3 / 15 USD;
  także przez AWS, Google Cloud i Azure.
- **Limity tygodniowe** w Claude Code (ogłoszone 28.07.2025, od 28.08.2025) jako odpowiedź na pracę 24/7 w tle
  i odsprzedaż kont; wg Anthropic dotyczyły <5% subskrybentów.
- **Finanse Anthropic:** seria G — 30 mld USD przy wycenie 380 mld USD post-money, run-rate 14 mld USD, Claude Code
  >2,5 mld USD (podwojenie od 1.01.2026), subskrypcje firmowe ×4 w tym samym okresie (12.02.2026, *dane firmy*).
  Ok. 44 mld USD run-rate w V 2026 *(szacunek SemiAnalysis za prasą, niezweryfikowany)*.
- **Przejęcia:** Vercept (25.02.2026) — percepcja i interakcja dla computer use.

**Offline.** **Nie.** Inferencja zawsze idzie do chmury (Anthropic albo regiony Bedrock/Vertex/Foundry). Lokalnie
wykonują się tylko „ręce": narzędzia computer/browser use z API w Twojej VM i klient Claude Code na Twoim dysku.
Lokalny odpowiednik potrzebuje: modelu lokalnego (do pulpitu — modelu z wizją, bo DeepSeek-V4-Flash obrazów nie
widzi), VM z montowaniem tylko wskazanych folderów, pamięci w plikach i lokalnych transkrypcji. Uwaga dla polskich
firm: w Microsoft 365 Copilot modele Anthropic są **wyłączone z EU Data Boundary** (dokumentacja Microsoftu,
8.10.2026) — sam wybór modelu potrafi po cichu wyprowadzić dane poza UE.

**Co przenieść do siebie.**
- **Rozdziel „mózg" i „ręce":** wykonawca (VM, przeglądarka, foldery) zostaje lokalnie, model jest wymienny.
  W hybrydzie Opus 5.5 dostaje zadanie i plan, a akta klienta czyta tylko lokalny DeepSeek — granicę opisuje
  [kurs 1, część 10](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md).
- **Pamięć jako pliki tematyczne z wyłączonymi kategoriami wrażliwymi.** Dla lekarza czy adwokata to gotowy wzorzec:
  dane o zdrowiu i inne szczególne kategorie danych (RODO, art. 9) domyślnie poza pamięcią długoterminową
  *(to nie jest porada prawna)*.
- **Uprawnienia na folder + „pytaj przed działaniem" domyślnie + zakaz usuwania bez zgody** — trzy ustawienia Cowork,
  które profesjonalista zrozumie bez szkolenia.
- **Drzewo dostępności zamiast zrzutów** — jedyna droga dla tekstowego DeepSeek-V4-Flash do pracy w przeglądarce;
  do tego akcje wsadowe ze stopem na pierwszym błędzie.
- **Jeden przełącznik „bez zbędnego ruchu" i lokalne transkrypcje z retencją** — regulowani klienci będą tego
  wymagać; lekcja z PromptArmor: lista dozwolonych adresów nie wystarczy, gdy dozwolony endpoint przyjmuje cudze
  klucze API.

**Warto wiedzieć.**
- **PromptArmor (I 2026):** biały tekst na białym tle w dokumencie kazał Cowork wysłać pliki ofiary na konto
  atakującego przez **dozwolone API Anthropic** z kluczem atakującego (zadziałało na Haiku i Opus 4.5). Anthropic
  zalecił nie udostępniać wrażliwych plików lokalnych.
- **BragJack (19.09.2026):** złośliwe rozszerzenie „wmusza" polecenia uprzywilejowanemu komponentowi AI — dotknęło
  m.in. Claude in Chrome (CVE-2026-0628 w Chrome). Anthropic sam odradza w Chrome bankowość, dokumentację medyczną
  i menedżery haseł.
- **Co ludzie delegują** (1,2 mln sesji Cowork z V 2026, publikacja 7.07.2026): 33,4% procesy biznesowe i operacje,
  16,4% treści, 8,7% programowanie, 7% DevOps, 6,4% research, 5,8% analiza danych — mniej więcej połowa to „the work
  around the work", a nie autonomiczne zarządzanie życiem.
- **Nadużycia:** Claude Code użyto w kampanii wymuszeń danych (VIII 2025) i w chińskiej kampanii szpiegowskiej
  (IX 2025), która zautomatyzowała 80–90% pracy (Wired i BBC wg Wikipedii).
- **Lekcja biznesowa:** computer use startował 22.10.2024 jako „experimental — at times cumbersome and error-prone",
  a abonament ryczałtowy plus agenci 24/7 skończył się limitami — policz to, zanim sprzedasz „nielimitowanego asystenta".

**Źródła:** [seria G](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation) · [pamięć](https://claude.com/resources/articles/claudes-memory-works-everywhere-and-you-decide-whats-in-it) · [Cowork to Claude](https://claude.com/resources/articles/cowork-is-now-claude) · [jak ludzie używają Cowork](https://claude.com/resources/articles/how-people-are-using-claude-cowork) · [Dispatch i computer use](https://claude.com/resources/articles/dispatch-and-computer-use) · [Routines](https://claude.com/resources/articles/introducing-routines-in-claude-code) · [Cowork research preview](https://claude.com/blog/cowork-research-preview) · [Cowork — pomoc](https://support.claude.com/en/articles/13345190-getting-started-with-cowork) · [Simon Willison o Cowork](https://simonwillison.net/2026/Jan/12/claude-cowork/) · [computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) · [browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) · [demo computer use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) · [Claude for Chrome](https://claude.com/blog/claude-for-chrome) · [Claude in Chrome](https://claude.com/chrome) · [obrona przed prompt injection](https://www.anthropic.com/research/prompt-injection-defenses) · [computer use 2024](https://www.anthropic.com/news/3-5-models-and-computer-use) · [Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5) · [Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6) · [Opus 5.5](https://www.anthropic.com/news/claude-opus-5-5) · [Vercept](https://www.anthropic.com/news/acquires-vercept) · [Claude Code — dane](https://code.claude.com/docs/en/data-usage) · [limity tygodniowe](https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/) · [Stack Overflow 2026](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/) · [SemiAnalysis za prasą](https://www.itiger.com/hans/news/1183910360) · [Claude for Legal](https://techcrunch.com/2026/05/12/the-ai-legal-services-industry-is-heating-up-anthropic-is-getting-in-on-the-action/) · [CoCounsel na Agent SDK](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html) · [EU Data Boundary](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) · [PromptArmor](https://www.promptarmor.com/resources/claude-cowork-exfiltrates-files) · [BragJack](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/) · [Wikipedia: Claude](https://en.wikipedia.org/wiki/Claude_(language_model)) · [Wikipedia: Claude (AI)](https://en.wikipedia.org/wiki/Claude_(AI))


---

## 3. Abridge

**Kategoria:** profesjonalny (medycyna) · **Kod:** zamknięty · **Firma:** Abridge AI Inc. (USA, Pittsburgh) ·
**Wynik: 94** (T5 I5 L5 A3)

> „Ambient scribe” dla amerykańskich szpitali: słucha wizyty, pisze notatkę do EHR i przy każdym zdaniu pokazuje,
> z którego miejsca rozmowy ono pochodzi. To najlepszy przykład na rynku, jak asystent zawodowy zdobywa zaufanie.

**Otwarty czy zamknięty.** Zamknięty, wyłącznie chmura (SaaS). Własny model rozpoznawania mowy (ASR) i własny model
„strażnika” halucynacji; dostawcy dużych modeli językowych nie są ujawnieni. Self-hostingu brak.

**Cel.** Lekarze, pielęgniarki i całe systemy ochrony zdrowia w USA, głównie klienci Epic. Abridge sprzedaje
organizacji, nie pojedynczemu lekarzowi. Problem: lekarz spędza wieczory na dokumentacji zamiast z pacjentem.
Od 11.06.2026 firma nazywa się „AI-native clinician intelligence platform” i wychodzi poza samą notatkę.

**Funkcje.**
- Notatka z wizyty generowana z nagrania rozmowy (szablony specjalizacji, SOAP).
- **Linked Evidence:** każde zdanie notatki prowadzi do fragmentu transkrypcji i nagrania.
- Dokumentacja pielęgniarska.
- Od 2026: zgodność rozliczeń i roszczeń (billing/claims), wsparcie decyzji klinicznych, procesy z płatnikami,
  kwalifikacja do badań klinicznych w trakcie wizyty.
- Zapis wprost do EHR po zatwierdzeniu przez lekarza.
- Partnerstwa: NVIDIA („foundation model for clinical conversations”), Artisight (czujniki w sali), inwestycja
  strategiczna Eli Lilly (warunki nieujawnione).

**Przewaga.**
- **Zaufanie wbudowane w interfejs.** Lekarz nie musi wierzyć modelowi — klika zdanie i słyszy, co padło w gabinecie.
  To przesuwa kontrolę z „czy AI ma rację” na „sprawdzam w 3 sekundy”.
- Głęboka integracja z Epic i wczesne wejście; #1 Best in KLAS dla Ambient AI w II 2026, drugi rok z rzędu
  *(za Sacra)*.
- Skala danych: ponad 100 mln rozmów rocznie *(Fortune, VI 2026)* — paliwo dla własnego ASR i strażnika.
- Uczciwie: w niezależnym badaniu na SOR (Webb i in., Appl Clin Inform, I 2026, n=18) użyteczność była równa
  (SUS 73,5 vs 73,5), ale DAX Microsoftu wypadł lepiej w jakości notatki (PDQI-9: 39 vs 36,5, p=0,011).

**Architektura.**
```
telefon / aplikacja EHR (np. Epic Haiku) ── nagranie ──▶ chmura Abridge
  └▶ własny medyczny ASR + diaryzacja (lekarz / pacjent)
     └▶ LLM: pierwszy szkic notatki w szablonie specjalizacji
        └▶ model-strażnik: wykrywa i poprawia zdania bez pokrycia w transkrypcji
           └▶ przegląd przez lekarza z Linked Evidence ──▶ podpis ──▶ zapis do EHR
```
- ASR: wg firmy 24% względnie mniej błędów (WER) niż „wiodący komercyjni konkurenci”, 83% mniej błędów na nowych
  lekach, 15% lepiej przy akcentach *(dane firmy, 6.08.2025)*.
- Strażnik: whitepaper „Science of Confabulation Elimination” (19.08.2025) — reguły zbudowane na 1 000+ godzin
  walidacji przez ludzi wyłapały 97% niepopartych twierdzeń na wewnętrznym zbiorze 10 000+ wizyt, wobec 82% dla
  GPT-4o *(dane firmy)*.
- Wszystko w chmurze; żaden lider rynku scribe'ów nie przetwarza nagrań na urządzeniu.

**Na czym zarabia.** Licencje korporacyjne na lekarza: ok. 2 500 USD rocznie *(szacunek Sacra)*.
- ARR: ok. 60 mln USD (koniec 2024), 100 mln USD (V 2025), 117 mln USD kontraktowego ARR w I kw. 2025
  *(Sacra, TechCrunch — dane z 2025, nowszych nie ma)*.
- Finansowanie: seria D 250 mln USD przy wycenie 2,75 mld (II 2025); seria E 300 mln USD przy 5,3 mld (VI 2025,
  a16z i Khosla); rozszerzenie serii E 316 mln USD (IV 2026); łącznie ok. 830 mln USD. Wycena z rynku wtórnego
  ok. 7 mld USD (V 2026) — niezweryfikowana.
- Klienci: 300+ systemów ochrony zdrowia, 250 mln+ objętych pacjentów (VI 2026), m.in. Kaiser Permanente
  (24 600 lekarzy), Mayo Clinic, Johns Hopkins *(dane firmy)*.
- Udział w rynku scribe'ów w 2025: ok. 30% (Microsoft/Nuance ok. 33%) *(Menlo Ventures, X 2025)*.

**Offline.** **Nie.** Tylko chmura. Lokalny odpowiednik potrzebuje: polskiego ASR z sygnaturami czasu
(np. Parakeet-TDT-0.6B-v3 — ok. 7,3% WER na polskich zbiorach wg karty modelu — albo Whisper), diaryzacji offline
(pyannote „community-1”, CC-BY-4.0), lokalnego LLM do notatki i drugiego przebiegu weryfikującego, a do integracji
z rozproszonymi polskimi systemami EDM — wtyczki przeglądarki (tę drogę wybrała Noa Notes). DeepSeek-V4-Flash
nie słyszy — mowa musi przejść przez osobny model STT (patrz [Głos](../harnessy-agentowe/02-KLOCKI.md#głos)).

**Co przenieść do siebie.**
- **Linked Evidence jako zasada, nie funkcja.** STT zwraca segmenty z ID i czasem (`[s12] 03:41–03:52`), prompt
  wymusza, by każde zdanie notatki kończyło się listą ID źródeł, a interfejs zamienia je w klikalne odtworzenie
  fragmentu. Zdanie bez ID = czerwone podkreślenie.
- **Przebieg weryfikujący na osobnym slocie.** Rig ma 4 sloty: slot 1 pisze szkic, slot 2 sprawdza zdanie po zdaniu
  „czy transkrypcja to popiera?” (tak/nie/częściowo + cytat). Kosztuje czas, nie pieniądze — marginalny koszt
  lokalnej inferencji jest bliski zera.
- **Własny test ASR na polskich nazwach leków** (lista z ChPL) — to tam leży największe ryzyko i najlepszy argument
  sprzedażowy.
- **Zakres: tylko dokumentacja.** Kodeks Etyki Lekarskiej art. 12 wymaga zgody pacjenta i certyfikowanego algorytmu
  przy AI w postępowaniu diagnostycznym lub leczniczym; notatka i pisma bez sugestii diagnozy są poza tym zakresem
  (szczegóły w [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md); to nie jest porada prawna).
- **Usuwanie nagrania po podpisaniu notatki** i wsparcie techniczne bez dostępu do danych: dostawca z dostępem
  zdalnym do komputera przychodni staje się podmiotem przetwarzającym (art. 28 RODO) związanym tajemnicą
  (art. 24 ust. 6 ustawy o prawach pacjenta).
- **Kotwica cenowa:** Noa Notes kosztuje 199 zł + VAT miesięcznie na lekarza (chmura AWS/Azure).

**Warto wiedzieć.**
- Założona w 2018 przez kardiologa Shiva Rao; wycena podwoiła się w cztery miesiące 2025.
- W II 2026 Epic uruchomił własny scribe (AI Charting), a szpitale zaczęły „przeliczać sens osobnych umów” —
  zwrot Abridge w stronę „platformy” (VI 2026) to odpowiedź na komodytyzację podstawowego scribe'a.
- Wejście w kodowanie i rozliczenia niesie nowe ryzyko: ubezpieczyciele w USA protestują przeciw AI-owemu
  „coding intensity” (nagłówki prasowe, III i IX 2026).
- Niezależne badania scribe'ów (PHTI, III 2025; RCT UCLA w NEJM AI, XII 2025) pokazują głównie mniej wypalenia
  i umiarkowany zysk czasu — sprzedawaj dobrostan i jakość, a jeśli obiecujesz „godzinę dziennie”, zmierz ją.

**Źródła:** [Fortune, 11.06.2026](https://fortune.com/2026/06/11/abridge-operating-system-medicine-nvidia-eli-lilly-artsight/) ·
[Sacra: Abridge](https://sacra.com/c/abridge/) ·
[blog Abridge: ASR](https://www.abridge.com/blog/becoming-the-benchmark-for-healthcare-ai) ·
[whitepaper o konfabulacjach](https://www.abridge.com/ai/science-confabulation-hallucination-elimination) ·
[Webb i in., PubMed](https://pubmed.ncbi.nlm.nih.gov/41734793/) ·
[MobiHealthNews: seria E](https://www.mobihealthnews.com/news/abridge-secures-300m-boosts-valuation-53b) ·
[Menlo Ventures: AI w ochronie zdrowia 2025](https://menlovc.com/perspective/2025-the-state-of-ai-in-healthcare/) ·
[HLTH: Epic AI Charting](https://hlth.com/insights/news/epic-releases-native-ai-charting-for-integrated-clinical-documentation-2026-02-06) ·
[Parakeet-TDT-0.6B-v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) ·
[pyannote community-1](https://huggingface.co/pyannote/speaker-diarization-community-1) ·
[Noa: cennik](https://noa.ai/pl/cennik) ·
[Fierce Healthcare: PHTI](https://www.fiercehealthcare.com/ai-and-machine-learning/early-evaluation-ai-scribes-finds-decreased-burnout-limited-financial-roi) ·
[RCT UCLA, PubMed](https://pubmed.ncbi.nlm.nih.gov/41497288/)


---

## 4. Harvey

**Kategoria:** profesjonalny (prawo) · **Kod:** zamknięty · **Firma:** Harvey AI (USA) · **Wynik: 94** (T5 I5 L5 A3)

> Asystent dla wielkich kancelarii i działów prawnych, który z „czatu nad dokumentami” stał się platformą agentów
> pracujących w przestrzeniach spraw — z routerem modeli, własnym modelem i polityką bezpieczeństwa poza LLM.

**Otwarty czy zamknięty.** Zamknięty SaaS w chmurze regionalnej (UE/Szwajcaria, USA, Australia); brak opcji
on-prem. Od 20.08.2026 działa własny model **Harvey Tenet** — wg Harvey pierwszy jej model dotrenowany na bazie
otwartych wag (Kimi K3); wagi samego Tenet nie są publiczne.

**Cel.** Duże kancelarie (BigLaw), działy prawne korporacji i firmy doradcze. Harvey deklaruje, że obsługuje 80%
kancelarii z Am Law 100 i pięć działów prawnych z Fortune 10 *(dane firmy, 9.09.2026)*. Problem: masowy przegląd
dokumentów, research i projekty pism w tempie i jakości, której oczekują elitarne kancelarie.

**Funkcje.**
- Assistant (czat nad dokumentami) i **Vault** — przestrzenie do masowego przeglądu dokumentów i pytań do data roomu.
- 500+ gotowych agentów dla dziedzin prawa i **Agent Builder** (wczesny dostęp od 5.05.2026); klienci zbudowali
  do tego czasu 25 000+ własnych agentów *(dane firmy)*.
- **Harvey II** (18.08.2026): agenci działają w „Spaces” sprawy — dokumenty, strony, zadania, uprawnienia, historia;
  osobista pamięć użytkownika przechodzi między Harvey, Wordem i Outlookiem; **ethical walls** (bariery konfliktu
  interesów) synchronizowane z systemów kancelarii.
- Własni agenci w Wordzie (23.09.2026) i agentowe wyszukiwanie w systemach zarządzania dokumentami (30.09.2026).
- Treści LexisNexis i weryfikacja cytatów Shepard's w Harvey (sojusz od 18.06.2025); wspólny workflow
  „Motion to Dismiss” (7.10.2026).

**Przewaga.**
- **Referencje elitarnych kancelarii:** A&O testowało Harvey od XI 2022 — ok. 3 500 prawników, ok. 40 000 zapytań.
  W prawie referencja prestiżowej firmy sprzedaje lepiej niż benchmark.
- **Treść + workflow:** sojusz z LexisNexis daje źródła prawa i weryfikację cytatów, a biblioteka agentów jest
  pisana językiem praktyki, nie inżynierów.
- **Kapitał:** łącznie ponad 1,55 mld USD *(TechCrunch, 9.09.2026)* — stać ją na własny model i przejęcia.
- **Bezpieczeństwo jako produkt:** certyfikaty SOC 2 Type II, ISO 27001/27701/42001, AIUC-1.

**Architektura.**
- **Wiele modeli z założenia** (10.03.2026): Claude Opus 4.6 i Sonnet 4.6, Gemini 3 Flash, GPT-5.2. Router wybiera
  model według zadania i przełącza na innego dostawcę podczas awarii; administrator decyduje, które modele są
  dozwolone. Mistral Large 3 dla klientów z UE we wczesnym dostępie — niezweryfikowane.
- **Własny model Tenet:** Kimi K3 dotrenowany asynchronicznym RL (GSPO) razem z Fireworks; dane syntetyczne,
  publiczne prawnicze i eksperckie — „We did not use any customer data”. Ok. 1/10 kosztu na komórkę w zadaniach
  Review Table, −90% kosztu zapytania o wiedzę kancelarii *(dane firmy)*.
- **Ewaluacja:** BigLaw Bench — własny benchmark, używany i do rozwoju, i w marketingu.
- **MCP Policy Engine** (7.10.2026): najmniejsze uprawnienia, kontrola każdego wywołania narzędzia, „tool pinning”
  (wykrycie podmienionej definicji narzędzia), reguły Rego blokujące **„lethal trifecta”** (dane prywatne + niezaufana
  treść + komunikacja na zewnątrz), sanitizer usuwający ukryte znaki Unicode z wyników narzędzi. Egzekwowanie
  działa **poza modelem**.
- **Dane:** dostawcy modeli muszą umownie zapewnić zero retencji, brak przeglądu przez ludzi i brak trenowania.

**Na czym zarabia.** Roczne kontrakty enterprise na stanowiska; cennik niepubliczny.
- Szacunki: ok. 1 200 USD/stanowisko/mies. przy małych wdrożeniach (min. 20 stanowisk) i 100–200 USD przy skali
  Am Law 100 *(szacunki firm trzecich, 2026, niezweryfikowane)*.
- ARR: 100 mln USD (VIII 2025), 190 mln USD (I 2026), ponad 400 mln USD i 3 000+ płacących organizacji (IX 2026)
  *(prasa wtórna; Harvey sam ARR nie podaje)*.
- Klienci: ok. 1 500 organizacji, 100 000+ prawników, 60+ krajów *(dane firmy za ITBrief, V 2026)*.
- Wyceny: 715 mln USD (XII 2023) → 3 mld (II 2025) → 8 mld (XII 2025) → 11 mld (III 2026) → **15,5 mld USD**
  (9.09.2026, runda 550 mln USD, prowadzący Diffusion i Lightspeed).

**Offline.** **Nie.** Chmura regionalna; strona bezpieczeństwa nie wymienia on-prem ani prywatnej chmury. Tenet
pokazuje ruch w stronę otwartych wag, ale nic nie wskazuje, że klient może go hostować. Lokalny odpowiednik
potrzebuje: indeksu dokumentów sprawy na dysku, lokalnego modelu z cytowaniem fragmentów, publicznych źródeł prawa
(ISAP/ELI, SAOS) zamiast Lexis i warstwy polityk dla narzędzi.

**Co przenieść do siebie.**
- **Przestrzeń sprawy = granica tajemnicy.** Każda sprawa to osobny katalog, osobny indeks RAG, osobna pamięć
  i lista uprawnień. Agent pracujący w sprawie A fizycznie nie widzi sprawy B — to lokalny odpowiednik ethical walls.
- **Polityka narzędzi poza modelem.** Bramka przed każdym wywołaniem: w sesji z danymi klienta nie ma narzędzi
  wysyłających cokolwiek na zewnątrz (zero „lethal trifecta”); definicje narzędzi MCP przypięte hashem.
  Patrz [16-BEZPIECZENSTWO-OWASP-ASI.md](../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md).
- **Router z twardą regułą:** Opus jako planista dostaje wyłącznie treść bez danych klienta (np. „przygotuj plan
  analizy umowy najmu pod kątem klauzul abuzywnych”), wykonanie i dokumenty zostają na DeepSeeku. Router z awaryjnym
  przełączeniem między slotami — [17-HYBRYDA-I-ROUTER.md](../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md).
- **Biblioteka agentów językiem praktyki:** „analiza umowy pod kątem klauzul niedozwolonych”, „chronologia sprawy
  z akt”, „projekt wezwania do zapłaty” — gotowe przepisy, które prawnik uruchamia bez promptowania.
- **Własny benchmark przed własnym modelem.** Harvey zaczął od BigLaw Bench, a dopiero potem dotrenował Tenet.
  Najpierw zbiór polskich zadań z oceną, potem ewentualne dotrenowanie (np. mniejszego Bielika) —
  [14-EWALUACJA.md](../kurs_aplikacje_agentowe/14-EWALUACJA.md).
- **Pamięć stylu użytkownika** (format cytowań, ulubione sformułowania) trzymana lokalnie, osobno od pamięci sprawy.

**Warto wiedzieć.**
- Założona latem 2022 przez Winstona Weinberga (były procesualista O'Melveny) i Gabriela Pereyrę (ex-DeepMind);
  seed od OpenAI Startup Fund (XI 2022).
- Przejęcia 2026: Hexus (23.01.2026), Guardrails AI (IX 2026, czwarte przejęcie w roku).
- Konkurencja rośnie z dwóch stron: szwedzka Legora (ponad 200 mln USD ARR wg założyciela, IX 2026) i Anthropic
  z „Claude for Legal” (wtyczki i konektory MCP do Westlaw, Box, Docusign, 12.05.2026).
- Tło popytu: baza Damiena Charlotina liczy 2 184 sprawy sądowe z halucynacjami AI (stan na 10.10.2026), w tym
  **6 w Polsce** — weryfikowalne cytaty to warunek wejścia, nie dodatek.

**Źródła:** [Harvey: wiele modeli](https://www.harvey.ai/en-US/blog/why-harvey-is-multi-model-by-design) ·
[Harvey Tenet](https://www.harvey.ai/blog/post-training-update-harvey-tenet) ·
[Harvey II](https://www.harvey.ai/blog/introducing-harvey-ii) ·
[MCP Policy Engine](https://www.harvey.ai/blog/building-harveys-mcp-policy-engine) ·
[bezpieczeństwo](https://www.harvey.ai/en-US/security) ·
[runda 550 mln USD](https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence) ·
[TechCrunch, 9.09.2026](https://techcrunch.com/2026/09/09/harvey-hits-15-5b-valuation-months-after-reaching-11b/) ·
[Wikipedia](https://en.wikipedia.org/wiki/Harvey_(software)) ·
[ITBrief: 500 agentów](https://itbrief.co.uk/story/harvey-launches-500-legal-ai-agents-builder-tool) ·
[raising.fi: ARR](https://raising.fi/news/harvey-undisclosed-september-2026) ·
[Vaquill: szacunek cen](https://www.vaquill.ai/blog/harvey-ai-review-honest-assessment) ·
[LexisNexis + Harvey](https://www.lexisnexis.com/community/pressroom/b/news/posts/lexisnexis-and-harvey-announce-strategic-alliance-to-integrate-trusted-high-quality-ai-technology-and-legal-content-and-develop-advanced-workflows) ·
[baza halucynacji](https://www.damiencharlotin.com/hallucinations/)


---

## 5. Hermes Agent

**Kategoria:** żyjący autonomicznie · **Kod:** otwarty (MIT) · ⭐ <!-- gh:NousResearch/hermes-agent -->252,7k ·
**Firma:** Nous Research (USA) · **Wynik: 93** (T4 I5 L5 A5)

> Osobisty agent „that grows with you": sam pisze i poprawia swoje umiejętności, a laboratorium, które go wydało,
> sprzedaje do niego modele — drugi po OpenClaw otwarty asystent „żyjący" i najlepszy punkt startu dla własnego
> asystenta z głosem i cronem.

**Otwarty czy zamknięty.** MIT; ostatnie wydanie v0.21.6 (8.10.2026). Nous pisze, że wydał agenta na MIT w lutym
2026; repozytorium założono 22.07.2025, a pierwszy tag wydania to v2026.3.12 (12.03.2026). Self-hosting: tak —
„on a $5 VPS, a GPU cluster, or serverless infrastructure". Zamknięte są usługi wokół: Nous Portal (modele
i kredyty), Hermes Business i Hermes Enterprise.

**Cel.** Dla osób, które chcą stałego agenta dostępnego z telefonu, bez przywiązania do jednego dostawcy modeli. Od
X 2026 także dla zespołów (Hermes Business) i firm z własną infrastrukturą (Hermes Enterprise). Rozwiązuje problem
„asystent zapomina, czego się nauczył": złożone zadanie zostawia po sobie umiejętność na następny raz.

**Funkcje.**
- TUI, aplikacja desktop (w Microsoft Store od 8.10.2026) i bramka komunikatorów: Telegram, Discord, Slack,
  WhatsApp, Signal, e-mail, Teams i inne — w sumie 25+ wg przeglądu harnessów.
- **Pętla uczenia:** umiejętności tworzone po złożonych zadaniach i poprawiane w użyciu; standard agentskills.io;
  instalacja z oficjalnego hubu i z ClawHub, ze skanowaniem bezpieczeństwa.
- Pamięć kuratorowana przez agenta, wyszukiwanie dawnych sesji (SQLite FTS5 + streszczenia LLM), modelowanie
  użytkownika przez Honcho.
- Cron w języku naturalnym z dostarczaniem na dowolny kanał; subagenci do pracy równoległej.
- Siedem backendów terminala: lokalny, Docker, SSH, Singularity, Modal, Daytona, Vercel Sandbox; backendy serverless
  „hibernate when idle".
- Głos: transkrypcja notatek głosowych, odpowiedzi głosowe na Telegramie i Discordzie.
- `hermes claw migrate` — import konfiguracji z OpenClaw.

**Przewaga.**
- **Zamknięta pętla uczenia.** Konkurenci mają umiejętności pisane przez ludzi; Hermes pisze je sam i poprawia — to
  pamięć proceduralna („jak to robię"), nie tylko pamięć faktów.
- **Laboratorium za plecami.** Nous trenuje własne modele (rodzina Hermes), ma portal inferencji, a agent generuje
  trajektorie do treningu — jest kanałem dystrybucji modeli.
- **„Planista z czołówki, tani wykonawcy" wpisany w konfigurację** i najmocniejszy cron w kategorii (strażnicy bez
  agenta, ciągłość między uruchomieniami, deduplikacja incydentów) — wg
  [przeglądu harnessów](../harnessy-agentowe/01-PROFILE.md#4-hermes-agent).
- **Niski koszt zmiany:** import z OpenClaw i zgodność z ClawHub.
- Zero porad bezpieczeństwa opublikowanych na GitHubie w 2026 (API, 11.10.2026) wobec 722 u OpenClaw — może to jednak
  odzwierciedlać sposób ujawniania, a nie dowodzić bezpieczeństwa.

**Architektura.** Krótko — pełny opis techniczny z konfiguracją lokalnego modelu jest w
[przeglądzie harnessów](../harnessy-agentowe/01-PROFILE.md#4-hermes-agent).
- **Bramka:** jeden proces obsługuje wszystkie komunikatory; rozmowy parowane jednorazowym kodem.
- **Pamięć ograniczona:** `MEMORY.md` (≤2200 znaków, notatki agenta) i `USER.md` (≤1375 znaków, profil użytkownika)
  wstrzykiwane jako **zamrożona migawka** na starcie sesji — stały prefiks, więc prompt cache działa. Gdy pamięć jest
  pełna, agent musi ją skonsolidować, a nie po cichu gubić wpisy; zapełnienie widać („67% — 1,474/2,200 chars").
- **Umiejętności:** katalog `~/.hermes/skills/`, skanowanie przy instalacji.
- **Proaktywność:** cron z zadaniami w języku naturalnym; strażnicy „bez agenta" alarmują tylko przy niepustym wyniku.
- **Wykonanie i zatwierdzenia:** lokalnie, w Dockerze bez uprawnień, przez SSH albo w chmurze; „smart approvals"
  (pomocniczy LLM ocenia oznaczone komendy) plus twarda lista zakazów; sekrety usuwane ze środowiska narzędzi.
- **Modele:** `hermes model` — Nous Portal, OpenRouter, OpenAI albo własny endpoint OpenAI-compatible; wykonawcy przez
  `delegation: {provider, model, base_url}`.
- **Głos:** STT lokalnie (faster-whisper), TTS domyślnie Edge TTS — **chmura** Microsoftu.

**Na czym zarabia.**
- **Agent darmowy (MIT); pieniądze z Nous Portal:** Plus 20 USD/mies., Super 100 USD, Ultra 200 USD, z kredytami na
  modele i narzędzia (strona Hermes, 11.10.2026, *dane firmy*). Instalator promuje portal.
- **Hermes Business** (X 2026): wspólne saldo zespołu z limitami wydatków na osobę, hostowani agenci dla członków
  zespołu, wspólna biblioteka umiejętności („the best skills anyone on your team discovers are automatically shared").
- **Hermes Enterprise:** na infrastrukturze klienta, z SSO i SLA; cennik nieznany.
- **Finansowanie:** Nous pozyskał 90 mln USD (ogłoszone X 2026; NVIDIA, M12 Microsoftu, Samsung, Robot Ventures,
  Union Square Ventures, Y Combinator, Menlo Ventures i inni). Wcześniejsze rundy — niezweryfikowane.
- **Zasięg wg Nous:** „cloned over 24 million times" i ok. 2,5% światowego zużycia tokenów *(dane firmy, wewnętrzne
  szacunki, X 2026)*. Przychody i liczba użytkowników — nieznane.

**Offline.** **Częściowo.** Pętla agenta z lokalnym endpointem OpenAI-compatible i backendem terminala „local"
działa bez internetu — razem z pamięcią, umiejętnościami i cronem. Rozpoznawanie mowy jest lokalne (faster-whisper),
ale **synteza mowy domyślnie idzie przez Edge TTS w chmurze**; do pracy bez sieci trzeba ją podmienić (lokalny NeuTTS
istnieje, polski głos niepotwierdzony; w pełni lokalny polski głos z Piperem ma
[Moltis](../harnessy-agentowe/01-PROFILE.md#15-moltis)). Komunikatory i narzędzia webowe wymagają sieci.

**Co przenieść do siebie.**
- **Pamięć z limitem i wskaźnikiem zapełnienia:** 2200 znaków wymusza kurację, a klient widzi, ile asystent o nim
  „wie". Zamrożona migawka na sesję to stały prefiks na llama.cpp — przy ok. 13,6 tok/s na slot nie stać Cię na
  ponowne czytanie promptu w każdej turze.
- **Umiejętności pisane po zadaniu, zatwierdzane przez człowieka:** asystent kancelarii po trzecim wezwaniu do
  zapłaty proponuje procedurę, mecenas ją akceptuje, procedura trafia do biblioteki.
- **Biblioteka umiejętności zespołu bez danych klientów** (wzorzec Hermes Business): procedury są wspólne dla firmy,
  akta zostają w sesji konkretnej sprawy.
- **Wykonawcy na lokalnym DeepSeeku, planista opcjonalnie w chmurze:** `delegation.max_concurrent_children` zmniejsz
  z domyślnych 10 do 4 (Twoje sloty), `context_length` ustaw jawnie na 131072.
- **Strażnicy crona bez modelu:** skrypt sprawdza, czy jest praca (nowa wiadomość z sądu, zbliżający się termin), a
  model budzi się tylko przy niepustym wyniku — oszczędza sloty
  ([kurs 2, część 11](../kurs_aplikacje_agentowe/11-HARMONOGRAM-PROAKTYWNOSC.md)).
- **Wymienne backendy wykonania:** dziś lokalny terminal, jutro SSH do serwera w kancelarii albo Docker per klient.

**Warto wiedzieć.**
- Nous Research to przede wszystkim laboratorium modeli; agent jest kanałem do portalu i źródłem danych treningowych
  (generowanie i kompresja trajektorii są w repozytorium).
- **Tempo zmian:** ok. 2100 PR między dwiema kolejnymi wersjami i ok. 18 tys. plików w repozytorium — **przypinaj
  wersje**; uszkodzenia bazy stanu wymagały osobnego wydania naprawczego.
- Nous przeprowadził refaktoryzację własnego kodu z udziałem 1393 agentów.
- NVIDIA NemoClaw obsługuje Hermesa jako jednego z trzech agentów (obok OpenClaw i LangChain Deep Agents) —
  w piaskownicy OpenShell z polityką ruchu wychodzącego zatwierdzaną przez operatora.
- **Ta sama ocena z innej strony:** w przeglądzie harnessów Hermes ma 81 pkt i 4. miejsce (tam liczyły się wielu
  agentów, lokalny model i bezpieczeństwo); tu — 93 pkt jako asystent-produkt. Wnioski są zgodne: najlepszy start dla
  głosu i crona; uważaj na chmurowy TTS i tempo zmian.

**Źródła:** [GitHub](https://github.com/NousResearch/hermes-agent) · [README](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/README.md) · [strona Hermes](https://hermes-agent.nousresearch.com/) · [pamięć](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) · [umiejętności](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) · [cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) · [delegacja](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation) · [głos](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode) · [indeks dokumentacji](https://hermes-agent.nousresearch.com/llms.txt) · [runda finansowania](https://nousresearch.com/a-note-on-our-fundraise) · [Nous Research](https://nousresearch.com/) · [blog Nous](https://nousresearch.com/blog) · [Hermes Business](https://portal.nousresearch.com/business) · [NemoClaw](https://github.com/NVIDIA/NemoClaw) · [przegląd harnessów](../harnessy-agentowe/01-PROFILE.md#4-hermes-agent)


---

## 6. Manus

**Kategoria:** wykonawca · **Kod:** zamknięty · **Firma:** Butterfly Effect Pte. Ltd. (Singapur; założyciele z Chin) ·
**Wynik: 93** (T4 I5 L5 A5)

> „Ogólny agent", który dla każdego zadania stawia osobny komputer w chmurze i oddaje gotowy plik, stronę albo
> prezentację — pierwszy na rynku (III 2025), 100 mln USD ARR po 8 miesiącach, a jego zespół najlepiej w branży
> opisał inżynierię kontekstu.

**Otwarty czy zamknięty.** Zamknięty SaaS zbudowany mocno na open source: na starcie używał biblioteki browser-use
i 29 narzędzi, a współzałożyciel Yichao „Peak" Ji mówił, że Manus „wouldn't exist without open source". Self-hostingu
nie ma. Otwarty klon to OpenManus (MIT, ok. 58,6k gwiazdek wg API GitHuba 11.10.2026), zbudowany w 3 godziny w dniu
premiery Manusa.

**Cel.** Pracownicy wiedzy, MŚP i prosumenci: raporty badawcze, analiza danych, prezentacje, strony i aplikacje
webowe, wideo, automatyzacja przeglądarki. Coraz częściej firmy (plan Team, API). W 2026 ruch w stronę asystenta
„żyjącego": automatyzacje na zdarzeniach, stały komputer w chmurze i aplikacja Cue.

**Funkcje.**
- **Manus 2.0** (28.09.2026): harness „Cascade", stały Cloud Computer, automatyzacje wyzwalane zdarzeniami (e-mail,
  kalendarz, Slack, Notion, zmiana wyników reklam), Manus Studio (dokumenty, arkusze, slajdy, web, kod, edytor
  wideo), sterowanie pulpitem z telefonu z zatwierdzaniem per aplikacja i plik.
- **Cue:** agenci osobiści z własnym adresem e-mail, numerem telefonu i portfelem z limitem wydatków ustawianym
  przez użytkownika (limit wg recenzji zewnętrznej).
- **Wide Research** (31.07.2025): główny agent dzieli zadanie, a każde podzadanie dostaje agenta „with its own fresh
  context window"; testowane do 250 pozycji.
- **Cloud Browser** z trwałymi sesjami i „Take Over" (człowiek przejmuje sterowanie przy CAPTCHA, SMS, MFA);
  **Browser Operator** (18.11.2025) działa w Twojej zalogowanej przeglądarce, z Twojego IP.
- **Manus Flex** (29.09.2026): własny klucz do modeli (OpenRouter, Fireworks, Modal); kredyty dalej za infrastrukturę,
  narzędzia i VM.
- Aplikacje full-stack z backendem, bazą i logowaniem (Manus 1.5, 16.10.2025), zadania planowane, konektory MCP
  (HubSpot, Shopify, Canva, Zoom, Supabase i inne), publiczne API, tryb planowania.

**Przewaga.**
- **Komputer na zadanie zamiast odpowiedzi:** wynikiem jest plik, strona albo talia slajdów. Skala do XII 2025:
  147 bilionów tokenów i 80 mln utworzonych wirtualnych komputerów *(dane firmy)*.
- **Inżynieria kontekstu zamiast własnych modeli:** zakład, że na modelach z czołówki zmiany wychodzą „in hours
  instead of weeks". Fosa leży w harnessie, infrastrukturze, UX i marce — nie w modelu (Flex pozwala podpiąć własny).
- **Pierwszeństwo i marka:** demo z >1 mln wyświetleń w 20 godzin, kody zaproszeń odsprzedawane po ~1000 USD
  i więcej (III 2025).

**Architektura.**
- **Modele:** na starcie Claude 3.5 Sonnet i dostrojone modele Qwen; skład w 2026 nieujawniony; od IX 2026 wymienny.
- **Wieloagentowość:** w 2025 użytkownik rozmawiał tylko z agentem-wykonawcą, który nie widział agentów planisty
  i wiedzy — to pilnuje długości kontekstu. Wide Research uruchamia równoległe pełne instancje ze świeżym kontekstem.
- **Cascade (2.0):** projekt startuje lekki, specjalistyczne zdolności są dociągane dopiero, gdy praca ich potrzebuje;
  −23,2% tokenów, −28,2% czasu, −32% kosztu „in tested configuration" *(dane firmy; recenzja zewnętrzna zauważa, że
  to jedna konfiguracja, nie średnia)*.
- **Piaskownica:** mikro-VM E2B na Firecrackerze, start ok. 150 ms; Docker odrzucony (10–20 s startu, niepełny
  system). Każda VM ma internet, trwały system plików i może instalować oprogramowanie.
- **Sześć zasad inżynierii kontekstu** (Ji, 18.07.2025) — patrz też
  [kurs 2, część 4](../kurs_aplikacje_agentowe/04-INZYNIERIA-KONTEKSTU.md):
  1. **Trafienia w KV-cache to najważniejsza metryka** — w Claude Sonnet wejście z cache kosztowało 0,30 zamiast
     3 USD za 1 mln tokenów; stosunek wejścia do wyjścia ok. 100:1; stały prefiks, kontekst tylko dopisywany.
  2. **Maskuj narzędzia, nie usuwaj ich** w trakcie pętli; wspólne prefiksy nazw (`browser_`, `shell_`).
  3. **System plików jako kontekst** — kompresja odwracalna: wyrzuć treść strony, zostaw URL i ścieżkę.
  4. **Recytacja celu:** agent przepisuje `todo.md`; typowe zadanie to ok. 50 wywołań narzędzi.
  5. **Zostaw błędy i stack trace w kontekście** — model aktualizuje swoje przekonania.
  6. **Nie daj się „few-shotować"** — wprowadzaj kontrolowaną różnorodność szablonów i sformułowań.
- **Logowania:** szyfrowane sesje per użytkownik, bez przechowywania haseł; IP centrów danych blokują antyboty, więc
  banki — przez lokalne rozszerzenie, które wymaga zgody na sesję i loguje każdą akcję. Rozumowanie zawsze w chmurze.

**Na czym zarabia.**
- **Abonament + kredyty:** kredyty płacą za tokeny, czas VM i zewnętrzne API, schodzą tylko w trakcie zadania;
  darmowi użytkownicy dostają dzienne odświeżenie (do 1500/mies.); kredyty miesięczne nie przechodzą.
- **Ceny:** III 2025 — Starter 39 USD (3900 kredytów), Pro 199 USD (19 900) *(Sacra)*; IX 2026 — 20 USD za 4000,
  40 USD za 8000 i 200 USD za 40 000 kredytów, plus 300 dziennie *(zrzut strony trzeciej; oficjalny cennik
  nieczytelny dla automatu)* — ok. 0,005 USD za kredyt. Stały Cloud Computer: 30 albo 50 USD/mies. (strona trzecia).
- **Przychody:** ok. 90 mln USD ARR (VIII 2025); 100 mln USD ARR i 125 mln USD run-rate całego przychodu przy wzroście
  >20% m/m i 105 pracownikach (XII 2025) *(dane firmy)*; ok. 450 mln USD rocznie w VI 2026 *(szacunek Sacra,
  źródło pierwotne niezweryfikowane)*.
- **Właściciele:** seria B ok. 75 mln USD (Benchmark) przy wycenie ok. 500 mln USD (IV 2025); Meta kupiła Manusa za
  >2 mld USD (XII 2025), a chińska NDRC zablokowała transakcję 27.04.2026; założyciele z Tencent, ZhenFund i HongShan
  odkupili udziały mniej więcej po pierwotnej cenie; Manus znów niezależny w Singapurze. 8.10.2026 runda >500 mln USD
  (Boyu Capital i IDG Capital; wycena nieujawniona, Bloomberg pisał o celu ok. 4 mld USD).

**Offline.** **Nie.** Rozumowanie w chmurowych API modeli, wykonanie w mikro-VM w chmurze. Browser Operator,
sterowanie pulpitem i Flex nadal wymagają orkiestracji Manusa — nawet z modelem na własnym endpoincie plan, VM
i kredyty zostają w chmurze. Lokalny odpowiednik: harness z zasadami kontekstu Manusa, kontener albo mikro-VM na
zadanie z zamontowanym katalogiem, lokalna przeglądarka i model lokalny; gotowy szkielet to OpenManus (MIT, obsługuje
Ollamę i piaskownicę Docker).

**Co przenieść do siebie.**
- **Sześć zasad to instrukcja obsługi llama.cpp:** lokalnie prefix cache decyduje, czy krok trwa 2 czy 40 sekund.
  Stały prompt systemowy i lista narzędzi, kontekst tylko dopisywany, zero znaczników czasu w prefiksie
  ([pułapka H4](../harnessy-agentowe/01-PROFILE.md#siedem-pułapek-wspólnych-dla-wszystkich)).
- **`todo.md` i błędy w kontekście** — tanie, a ratują długie zadania DeepSeek-V4-Flash przy 131k kontekstu.
- **Wide Research na 4 slotach:** przegląd 200 umów to 4 równoległych wykonawców z małym, świeżym kontekstem
  i agregacja wyników — zamiast jednego przepełnionego kontekstu.
- **Kontener na zadanie** z zamontowanym tylko katalogiem sprawy: izolacja, powtarzalność i ślad dla audytu.
- **„Take Over" na biurku:** agent pauzuje, człowiek loguje się do portalu (bank, system sądowy), oddaje sterowanie.
  Lokalna maszyna ma tu przewagę nad chmurą Manusa: zwykłe IP i istniejące sesje.
- **Żadnych narzędzi typu „wystaw port" bez bramki człowieka** — patrz atak niżej.

**Warto wiedzieć.**
- **Start i niezawodność:** premiera 6.03.2025 na zaproszenia. W testach TechCrunch (III 2025) zamówienie jedzenia
  padło po 10 min, a rezerwacja lotu dała zepsute linki. Do X 2025 średni czas zadania spadł z 15 do <4 min
  *(dane firmy)*.
- **Atak (25.08.2025):** Johann Rehberger pośrednim prompt injection w PDF zmusił Manusa do wywołania
  `deploy_expose_port`, wystawienia wewnętrznego VS Code Server do internetu i wycieku hasła — bez zatwierdzenia
  człowieka; status poprawki „unclear".
- **Geopolityka:** przeprowadzka z Pekinu i Wuhanu do Singapuru w połowie 2025 i blokada użytkowników z Chin
  kontynentalnych nie wystarczyły — zakaz NDRC był pierwszym publicznie ujawnionym zakazem w chińskim przeglądzie
  bezpieczeństwa inwestycji, a CEO Xiao Hong i główny naukowiec Ji Yichao mieli w III 2026 zakaz wyjazdu z Chin
  (wg TechCrunch). Restrukturyzacja offshore nie chroni przed jurysdykcją nad ludźmi i danymi.
- **Dane:** po ogłoszeniu powrotu do niezależności (11.08.2026, formalnie 1.09.2026) Manus usunął 23–24.08.2026 dane
  „certain users" z „specific jurisdictions"; dane trzyma w USA i Singapurze, deklaracji rezydencji w UE nie znalazłem
  — do danych objętych polską tajemnicą zawodową się nie nadaje.
- **Benchmark GAIA:** na starcie Manus twierdził, że bije OpenAI Deep Research; często cytowanych wyników per poziom
  (86,5 / 70,1 / 57,7) nie udało się potwierdzić na stronie pierwotnej.

**Źródła:** [inżynieria kontekstu](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) · [Manus 2.0](https://manus.im/blog/introducing-manus-2-0) · [Manus Flex](https://manus.im/blog/introducing-manus-flex) · [Wide Research](https://manus.im/blog/introducing-wide-research) · [Wide Research — docs](https://manus.im/docs/features/wide-research.md) · [Manus 1.5](https://manus.im/blog/manus-1.5-release) · [Browser Operator](https://manus.im/blog/manus-browser-operator) · [Cloud Browser](https://manus.im/docs/features/cloud-browser.md) · [100 mln ARR](https://manus.im/blog/manus-100m-arr) · [list do użytkowników](https://manus.im/blog/a-note-to-our-users) · [niezależność](https://manus.im/blog/manus-resumes-independent-operations) · [zasady kredytów](https://help.manus.im/en/articles/11711097-what-are-the-rules-for-credits-consumption-and-how-can-i-obtain-them) · [E2B](https://e2b.dev/blog/how-manus-uses-e2b-to-provide-agents-with-virtual-computers) · [The Decoder](https://the-decoder.com/chinese-ai-agent-manus-uses-claude-sonnet-and-open-source-technology/) · [TechCrunch III 2025](https://techcrunch.com/2025/03/09/manus-probably-isnt-chinas-second-deepseek-moment/) · [TechCrunch: weto Chin](https://techcrunch.com/2026/04/27/china-vetoes-metas-2b-manus-deal-after-months-long-probe/) · [TechCrunch: runda X 2026](https://techcrunch.com/2026/10/08/chinas-manus-raises-over-500m-in-first-funding-round-since-split-with-meta/) · [Bloomberg](https://www.bloomberg.com/news/articles/2026-04-27/china-blocks-meta-s-2-billion-acquisition-of-ai-startup-manus) · [Yahoo: wycena 4 mld](https://finance.yahoo.com/technology/ai/articles/manus-seeks-4b-valuation-beijing-183502124.html) · [Dahui Lawyers](https://www.dahuilawyers.com/en/news-insights/chinas-first-public-foreign-investment-security-review-prohibition-the-metamanus-decision/) · [Sacra](https://sacra.com/c/manus) · [recenzja 2.0](https://myclaw.ai/blog/manus-2-0) · [Embrace The Red](https://embracethered.com/blog/posts/2025/manus-ai-kill-chain-expose-port-vs-code-server-on-internet/) · [OpenManus](https://github.com/FoundationAgents/OpenManus) · [Wikipedia](https://en.wikipedia.org/wiki/Manus_(AI_agent))


---

## 7. ChatGPT

**Kategoria:** codzienny + wykonawca · **Kod:** zamknięty · **Firma:** OpenAI (USA) · **Wynik: 87** (T5 I4 L4 A4)

> Największy asystent świata (ok. 1,2 mld użytkowników tygodniowo, 29.09.2026), który w 2026 zamienił się z czatu
> w platformę „zrób to za mnie": agent w maszynie w chmurze, zadania w harmonogramie i stale działające „dots".
> W czołówce za skalę i za to, że OpenAI najdokładniej opisało, jak zatwierdzać działania agenta.

**Otwarty czy zamknięty.** Zamknięte są aplikacja, modele (GPT-6 Luna, Sol, Astra) i środowisko agenta. Obok OpenAI
publikuje otwarte wagi na Apache 2.0: gpt-oss-120b i gpt-oss-20b (VIII 2025), gpt-oss-safeguard oraz **privacy-filter**
(IV 2026), czyli klasyfikator danych osobowych (1,5 mld parametrów, 50 mln aktywnych), który działa na laptopie i w
przeglądarce. Na DevDay 2026 OpenAI miało otworzyć harness agenta Codex (wg Decrypt). Self-hosting ChatGPT: nie.

**Cel.** Asystent dla wszystkich: od darmowych użytkowników na rynkach wschodzących (plan Go) po profesjonalistów na
planach Pro i Business. W 2026 OpenAI przesuwa go z rozmowy w stronę wykonywania pracy: dokumenty, arkusze, maile,
monitorowanie spraw w tle, a w firmach agenci siedzący w Slacku i Teams.

**Funkcje.**
- **Pamięć:** zapisane wspomnienia (2024) + odwołania do historii (2025); od 4.06.2026 „Dreaming", czyli zadanie w tle,
  które przepisuje edytowalne *Memory Summary* i aktualizuje fakty z datą ważności (najpierw Plus i Pro w USA).
  Wewnętrzny test przypominania faktów miał wzrosnąć z 41,5% do 82,8% *(dane firmy, przez prasę wtórną)*.
- **Zadania w harmonogramie** (17.06.2026): przypomnienia, prace cykliczne i monitory, które odzywają się tylko przy
  zmianie; najczęściej raz na godzinę, nieużywane same się pauzują. Zastąpiły Pulse (poranny brief, 25.09.2025 – VI 2026).
- **Agent:** Operator (23.01.2025) → ChatGPT agent (17.07.2025) → **ChatGPT Work** (9.07.2026, GPT-5.6). Work ma tryb
  planu: zbiera kontekst, dopytuje, pokazuje plan do akceptacji, potem pracuje sam, także na zdarzenie i w ciągłym
  monitoringu. Oddaje arkusze, slajdy, dokumenty i „Sites"; 1400+ wtyczek; zapis do Gmaila, Kalendarza, Slacka, GitHuba.
- **Aplikacja desktopowa** (9.07.2026, macOS i Windows): czat, Work i Codex w jednym oknie; wbudowana przeglądarka z
  menedżerem haseł, lokalne „Computer Use" (klika, pisze, przenosi pliki) i osobna przeglądarka w chmurze OpenAI.
- **„dots"** (29.09.2026): stale działający agenci na GPT-6 Astra, każdy z własną maszyną w chmurze i przeglądarką;
  dostępni w ChatGPT, Slacku, Teams i przez rozmowę głosową, uczą się z informacji zwrotnej.
- **Wtyczki** (dawniej apps, od VII 2026): 4000+ aplikacji; 6.08.2026 otwarty standard **Agent Plugins** (Agent Skills +
  serwery MCP; komitet: Amazon, Cursor, Microsoft, OpenAI, Vercel). Custom GPTs znikają w XII 2026.
- **Głos** na GPT-6 z wtyczkami (23.09.2026) i „Intelligent UI": widżety, formularze, wykresy w odpowiedzi (7.10.2026).
- **Zdrowie:** ChatGPT Health (7.01.2026) — **niedostępny w EOG, Szwajcarii i UK**; ChatGPT for Clinicians (IV 2026,
  wg Sacra) wchodzi w rynek [OpenEvidence](#12-openevidence).

**Przewaga.**
- **Nawyk i zasięg:** 1,2 mld użytkowników tygodniowo *(dane firmy, DevDay 29.09.2026)*; Sensor Tower (V 2026):
  1,1 mld+ MAU i 46,4% rynku aplikacji asystentów — pierwszy raz poniżej 50%.
- Płacących subskrybentów w USA ok. 3× więcej niż Claude czy Gemini *(a16z, X 2026)*.
- Największy ekosystem wtyczek i własny standard ich pakowania.
- Pełny stos: modele trenowane RL pod narzędzia agenta (przeglądarka, terminal) i produkt na nich.
- Mechanizm najbardziej wart zrozumienia: **polityka działań**. Nie jeden przełącznik „pytaj / nie pytaj", tylko poziomy
  dla każdego typu akcji plus osobny system, który przegląda plan przed nieodwracalnym krokiem.

**Architektura.**
```
użytkownik ─▶ router modeli: Luna (mały, Free/Go) · Sol (średni) · Astra (największy) + suwak „Think"
   ├─ czat + pamięć dwuwarstwowa (jawne wspomnienia + profil z historii; nocne „Dreaming")
   ├─ harmonogram po stronie serwera (≤ 1×/h, auto-pauza)
   └─ agent / dot ─▶ izolowana VM Linux z Chrome w chmurze
        narzędzia: przeglądarka wizualna (piksele) · przeglądarka tekstowa · terminal (sieć: tylko GET)
                   · wtyczki (MCP + skills)
        bramki:    Custom Rules: sam / jeśli wcześniej zatwierdzone / zapytaj / oddaj człowiekowi
                   + osobny auto-review planu przed mailem lub zmianą plików
                   + przejęcie sterowania przy logowaniu i płatności (agent nie widzi hasła)
```
- **Karta systemowa ChatGPT agent (17.07.2025):** potwierdzenia przed akcjami zmieniającymi stan mają trafność 91,0%
  ogólnie, 100% dla transakcji finansowych, 99,9% dla komunikacji wysokiej stawki. „Watch mode" pauzuje na wrażliwych
  stronach (poczta, bank), gdy użytkownik odejdzie. **Pamięć ChatGPT jest wyłączona w trybie agenta**, żeby wstrzyknięcie
  ze strony nie wyciągnęło jej treści. Odporność samego modelu: ignoruje obce instrukcje w 95%, eksfiltrację z kontekstu
  odpiera w 78%, aktywną w 67%.
- **dots:** hasła, przelewy i kasowanie danych zawsze wymagają zatwierdzenia albo wracają do człowieka; tryb
  „proactive research" działa tylko do odczytu. Podłączenie własnego komputera jest opcjonalne i domyślnie wyłączone.
  Dot dziedziczy pamięć ChatGPT, ale pojedynczych wspomnień dota nie da się podejrzeć — można tylko wyczyścić wszystkie
  (wg eesel).
- **Computer use w API:** dla GPT-6 Astra OpenAI zaleca, żeby model **pisał kod Playwright lub PyAutoGUI** zamiast klikać
  w piksele; tańsza ścieżka to narzędzie zwracające ruchy myszy i klawiatury (gpt-6.1-sol).
- **Ewaluacja bezpieczeństwa:** atakujący trenowany RL szuka łańcuchów wstrzyknięć na dziesiątki do setek kroków
  (22.12.2025); ChatGPT Work ma bramkę auto-review przed ważnymi akcjami w podłączonych narzędziach.
- Inferencja zawsze w chmurze; wykonanie albo w VM OpenAI (agent, dots, przeglądarka w chmurze), albo lokalnie
  (desktop, wbudowana przeglądarka, rozszerzenie Chrome).

**Na czym zarabia.**
- **Plany (X 2026):** Free (z reklamami), Go 8 USD, Plus 20 USD, Pro 100 / 200 / 500 USD (Pro 500 ogłoszony 29.09.2026,
  25× limit Plus), Business 25 USD (Standard) i 125 USD (Premium) za stanowisko *(Go i Business wg agregatorów)*.
  Pierwszy dot jest w Pro i Business Premium — ale Pro w EOG, Szwajcarii i UK go na starcie nie ma.
- **Reklamy:** test w USA od 9.02.2026 (Free i Go, bez tematów zdrowia, polityki i osób poniżej 18 lat); od 24.08.2026
  w 31 krajach Europy, **także w Polsce**, na start wyłącznie kontekstowe. Tempo ok. 1 mld USD rocznie w VIII 2026 *(a16z)*.
- **Przychody:** 13,1 mld USD zaksięgowane w 2025; ok. 25 mld USD w ujęciu rocznym na koniec I 2026 *(prasa)*; ARR
  „blisko 70 mld USD" 29.09.2026 *(Axios przez Reuters, źródło anonimowe)*.
- **Subskrybenci:** 50 mln+ (II 2026, agregator); wewnętrzna prognoza 122 mln na koniec 2026 *(The Information)*.
- **API (29.09.2026):** GPT-6 Astra 10 / 50 USD za 1 mln tokenów wej./wyj., Sol 2 / 10, Luna 0,10 / 0,50 *(dane firmy
  wg relacji z DevDay)*. ChatGPT Work rozliczany za użycie, bez cennika za zadanie.
- **Finansowanie:** runda 122 mld USD przy wycenie 852 mld USD (zamknięta ok. 1.04.2026; Amazon 50, Nvidia 30,
  SoftBank 30 mld USD). Debiut giełdowy przesunięty na 2027.

**Offline.** **Nie.** Każde zapytanie i każdy krok agenta idą na serwery OpenAI; aplikacja desktopowa działa na lokalnych
plikach, ale model jest w chmurze. Lokalny odpowiednik potrzebuje: modelu z wywoływaniem narzędzi, VM lub kontenera z
przeglądarką, harmonogramu i pamięci w plikach. Klocki od OpenAI, które da się uruchomić u siebie: gpt-oss-20b (ok. 16 GB)
i gpt-oss-120b (jedna karta 80 GB) — rozmiary z karty modelu z 2025, niezweryfikowane — oraz privacy-filter. Na moim
rigu mózgiem jest DeepSeek-V4-Flash, ale tylko tekstowy: przeglądarka wizualna wymaga osobnego modelu wizji albo pracy na
DOM i drzewie dostępności (zob. [browser-use](#13-browser-use)).

**Co przenieść do siebie.**
- **Cztery poziomy zgody dla każdego typu akcji** + twarda lista „zawsze pytaj" (pieniądze, hasła, kasowanie, wysyłka do
  klienta) + drugi model-recenzent przed krokiem nieodwracalnym. Na rigu recenzentem może być jeden z 4 slotów DeepSeeka,
  który widzi tylko plan i cel, a nie surowe dokumenty.
- **Mierz „confirmation recall"** z osobnym celem 100% dla akcji krytycznych — na zestawie testów z prawdziwych zadań
  kancelarii albo biura rachunkowego ([ewaluacja](../kurs_aplikacje_agentowe/14-EWALUACJA.md)).
- **Nocne „dreaming":** cron o 3:00 przepisuje jeden edytowalny plik profilu i usuwa fakty po terminie. Rig w nocy i tak
  stoi ([pamięć długoterminowa](../kurs_aplikacje_agentowe/05-PAMIEC-DLUGOTERMINOWA.md)).
- **Monitory „odezwij się tylko przy zmianie"** z limitem częstotliwości i auto-pauzą zamiast ciężkiego porannego
  raportu — Pulse zamknięto po ok. 9 miesiącach ([harmonogram](../kurs_aplikacje_agentowe/11-HARMONOGRAM-PROAKTYWNOSC.md)).
- **Wyłącz pamięć długoterminową, gdy agent czyta niezaufane treści** (strony, maile od obcych); terminal z siecią tylko GET.
- **privacy-filter (Apache 2.0) jako maskownik danych osobowych** przed każdym zapytaniem do Opus 5.5 w trybie hybrydowym
  ([hybryda](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md)).

**Warto wiedzieć.**
- **Cmentarz produktów:** Operator (I–VIII 2025), Pulse (ok. 9 miesięcy), Atlas (21.10.2025 – 9.08.2026; tylko macOS,
  ok. 10 mln MAU wg szacunku 36Kr), Custom GPTs (XII 2026). Wg Wikipedii sam „ChatGPT agent" zniknął na początku VIII 2026
  na rzecz Work (niezweryfikowane gdzie indziej). Hasło OpenAI: „AI browsers should be a feature, not a destination";
  wszystkie AI-przeglądarki razem miały poniżej 1% rynku.
- **Atlas i bezpieczeństwo:** „Tainted Memories" (LayerX, X 2025; OpenAI kwestionuje), wstrzyknięcia i wycieki przez URL.
  OpenAI przyznało (22.12.2025), że prompt injection „is unlikely to ever be fully solved".
- **Europa w tyle:** Health i dots na Pro poza EOG; reklamy w UE domyślnie tylko kontekstowe.
- **Pozwy:** *Raine v. OpenAI* (26.08.2025, samobójstwo nastolatka) i kolejne; odpowiedzią była kontrola rodzicielska.
  UK AISI miało znaleźć „universal cyber jailbreaks" w GPT-5.6 (niezweryfikowane u źródła).
- **OpenClaw:** OpenAI zatrudniło jego twórcę (II 2026) i jest darczyńcą fundacji — zob. [OpenClaw](#1-openclaw).
- **Sprzęt:** io (Jony Ive) kupione w V 2025 za ok. 6,5 mld USD; pierwsze urządzenie nie przed końcem II 2027.

**Źródła:** [DevDay 2026 — Engadget](https://www.engadget.com/2271985/openai-dev-day-live-blog-chatgpt-news/) · [DevDay — Decrypt](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced) ·
[DevDay — emergent](https://emergent.sh/news/openai-devday-2026) · [dots — eesel](https://www.eesel.ai/blog/openai-dots) · [dots — TechCrunch](https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/) ·
[karta systemowa ChatGPT agent](https://cdn.openai.com/pdf/839e66fc-602c-48bf-81d3-b21eacc3459d/chatgpt_agent_system_card.pdf) · [ChatGPT Work](https://www.digitalapplied.com/blog/chatgpt-work-openai-agent-launch-2026) ·
[koniec Atlasa](https://9to5mac.com/2026/07/09/openai-is-discontinuing-chatgpt-atlas-its-standalone-desktop-browser/) ·
[Atlas — forum OpenAI](https://community.openai.com/t/atlas-is-scheduled-to-stop-working-on-august-9-2026/1389473) · [zadania w harmonogramie](https://9to5mac.com/2026/06/17/openai-launches-scheduled-tasks-in-chatgpt-details-here/) ·
[pamięć](https://www.thurrott.com/a-i/337052/openai-is-improving-how-chatgpts-memory-works) · [Agent Plugins](https://9to5mac.com/2026/08/06/gpt-5-turning-one-as-openai-shares-new-agent-plugins-standard/) ·
[computer use w API](https://developers.openai.com/api/docs/guides/tools-computer-use) · [prompt injection](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/) ·
[reklamy w Europie](https://www.pinmeto.com/news/chatgpt-ads-31-european-markets-2026/) · [a16z Top 100](https://a16z.com/100-gen-ai-apps-7/) ·
[ARR ~70 mld](https://www.investing.com/news/stock-market-news/openais-annual-recurring-revenue-nears-70-billion-axios-reports-4923088) ·
[runda 122 mld](https://news.bloomberglaw.com/tech-and-telecom-law/openai-valued-at-852-billion-after-closing-122-billion-round) · [Sensor Tower](https://techcrunch.com/2026/06/16/chatgpts-market-share-slips-below-50-for-first-time/) ·
[privacy-filter](https://huggingface.co/openai/privacy-filter) · [ChatGPT — Wikipedia](https://en.wikipedia.org/wiki/ChatGPT)


---

## 8. Gemini

**Kategoria:** codzienny + wykonawca · **Kod:** zamknięty (otwarta rodzina Gemma obok) · **Firma:** Google / Alphabet (USA) ·
**Wynik: 87** (T5 I4 L4 A4)

> Asystent wbudowany w Androida, Chrome i Workspace (950 mln MAU w II kw. 2026), z agentem, który pracuje w chmurze albo
> w Twoim zalogowanym Chrome. W czołówce za dystrybucję i za najlepiej opisaną publicznie architekturę bezpieczeństwa
> agenta przeglądarkowego: planista + krytyk + zbiory originów.

**Otwarty czy zamknięty.** Zamknięte są aplikacja, modele Gemini i agent w Chrome. Otwarte obok: rodzina **Gemma 4**
(IV 2026; E2B, E4B, 12B, 26B, 31B — licencji Gemma 4 nie zweryfikowałem, wcześniejsze Gemmy miały „Gemma Terms of Use"),
referencyjna implementacja narzędzia computer use w Gemini API z piaskownicą Docker i oczywiście Chromium. Gemini Nano
na telefonie jest zamknięty, ale aplikacje Androida dostają go przez AICore i ML Kit GenAI. Self-hosting Gemini: nie.

**Cel.** Warstwa AI nad Gmailem, Kalendarzem, Zdjęciami, Mapami i Dokumentami dla miliardów użytkowników Androida, Chrome
i Workspace. W 2026 Gemini nie tylko odpowiada, ale też załatwia: sprawunki w przeglądarce, zadania w tle, poranny brief.
Deweloperom Google sprzedaje model computer use do automatyzacji interfejsów.

**Funkcje.**
- **Aplikacja Gemini:** modele Gemini 3.5 Flash (19.05.2026) i Gemini 4 Argon (30.09.2026). Gemini Live (głos i kamera)
  od 26.08.2026 uruchamia zadania Spark głosem i korzysta z „Personal Intelligence" (pamięć + połączone aplikacje, za zgodą).
- **Daily Brief** (19.05.2026, USA, AI Plus / Pro / Ultra): poranny przegląd z Gmaila, Kalendarza i Tasks z propozycją
  kolejnych kroków.
- **Gemini Agent** (18.11.2025): Project Mariner + Gemini 3 w aplikacji; pyta przed zakupem i wysłaniem wiadomości,
  użytkownik może przejąć sterowanie w każdej chwili; na start US AI Ultra, tylko web.
- **Gemini Spark** (ogłoszony 19.05.2026): osobisty agent „24/7, nawet przy zablokowanym telefonie". Składa się z
  **Tasks** (jednorazowy cel), **Schedules** (wyzwalacz czasowy lub warunkowy) i **Skills** (procedura wielokrokowa); do 15
  zadań naraz; Gmail, Docs, Sheets, Slides, Keep i Tasks natywnie, reszta przez MCP. AI Pro w USA od 24.07.2026; od
  30.07.2026 integracja z Chrome i 160+ kolejnych krajów — **bez EOG, Szwajcarii, UK i Nigerii**.
- **Chrome auto browse** (28.01.2026; Android od 18.08.2026): porównanie cen hoteli i lotów, rezerwacje, formularze,
  zbieranie dokumentów podatkowych, kody rabatowe. Loguje się przez Menedżer haseł (za zgodą), płaci przez Universal
  Commerce Protocol, pyta przed zakupem i publikacją. Tylko USA.
- **Gemini Computer Use w API:** od 7.10.2025 (2.5, przeglądarka); w 2026 Gemini 3.8 Flash (zalecany), 3.5 Flash-Lite
  i 3 Flash Preview, w przeglądarce, na Androidzie i na desktopie.
- **Gems → Skills** wywoływane „/" w polu zapytania (migracja 17.11.2026).
- **Na urządzeniu:** Gemini Nano przez AICore — streszczanie, korekta, przepisywanie, opis obrazu, transkrypcja offline.

**Przewaga.**
- **Dystrybucja przez system:** od 4.09.2026 Gemini na stałe zastępuje Asystenta Google na Androidzie, Wear OS,
  słuchawkach i Android Auto; modele Gemini stoją też za Siri AI Apple'a.
- **Grawitacja danych:** Gmail, Kalendarz, Zdjęcia, Mapy, Menedżer haseł, Wallet. Agent pracuje tam, gdzie użytkownik
  jest już zalogowany.
- **Własna przeglądarka i płatności:** Chrome ma ok. 2/3 rynku; własny protokół zakupów (UCP); protokół płatności AP2
  przekazany FIDO Alliance (IV 2026).
- **Tanie, szybkie modele Flash** do computer use; Google podaje ok. 225 s przy 70%+ trafności (własny wykres, 7.10.2025).

**Architektura.**
```
 cel ─▶ planista (Gemini) widzi stronę i proponuje akcję
              ▼
        User Alignment Critic — osobny, zaufany model; widzi akcję i cel, NIE surową treść strony ── weto
              ▼
        Agent Origin Sets — dla zadania: originy tylko-do-odczytu  /  originy do zapisu (klik, pisanie)
              ▼
        deterministyczne potwierdzenia: bank i medycyna, logowanie hasłem, płatność, wysłanie wiadomości
        + klasyfikator prompt injection równolegle z planistą + dziennik pracy z pauzą i przejęciem
```
- Schemat z bloga bezpieczeństwa Chrome (8.12.2025); nagroda VRP do 20 000 USD za złamanie tych granic.
- **Spark:** dedykowane, odizolowane VM w chmurze (trwały stan, zadania wielogodzinne), harness agentowy Antigravity i
  Gemini 3.5 Flash. Przegląda albo przez lokalny Chrome użytkownika (zalogowane strony, zapisane hasła), albo przez zdalną
  przeglądarkę; strony logowania i płatności oddaje człowiekowi; wymaga 18+.
- **Zgoda według zakresu danych:** edycja **wspólnych** dokumentów wymaga ręcznego potwierdzenia, **prywatnych** idzie
  automatycznie.
- **Pętla API:** zapytanie + zrzut ekranu + historia akcji → wywołanie funkcji (click, type, scroll) → wykonanie po stronie
  dewelopera → nowy zrzut. Każdy krok zwraca `safety_decision`; `require_confirmation` wymusza pytanie do człowieka i
  `safety_acknowledgement`. Siedem wbudowanych kategorii polityk (transakcje, zmiana danych wrażliwych, komunikacja,
  zakładanie kont, modyfikacja danych, zgody, umowy prawne); `excluded_predefined_functions` podmienia akcje na własne.
  Google zaleca VM albo kontener.
- **Historia:** Mariner (11.12.2024) działał tylko w aktywnej karcie, WebVoyager 83,5%; od 20.05.2025 w maszynach w chmurze,
  do 10 zadań naraz; zamknięty 4.05.2026 i wchłonięty przez Gemini Agent/Spark, auto browse i API.
- **Na urządzeniu:** Nano jest izolowany, nie ma bezpośredniego dostępu do internetu, nie zapisuje wejść i wyjść;
  Firebase AI Logic Hybrid API przełącza na chmurę, gdy Nano jest niedostępny.

**Na czym zarabia.** Agenci są w pakietach Google AI, razem z dyskiem i YouTube:
- **USA (X 2026):** AI Plus 4,99 USD, AI Pro 19,99 USD (Spark, 5 TB), AI Ultra od 99,99 USD (199,99 USD za 20× limity;
  obniżka z 250 USD na I/O 2026).
- **Polska (X 2026):** AI Plus 23,99 zł, AI Pro 97,99 zł, AI Ultra 469,99–979,99 zł; Sparka na polskiej stronie planów nie ma.
- **Firmy:** Gemini Enterprise Business 21 USD za stanowisko; Standard i Plus od 30 USD.
- **API:** Gemini 4 Argon 2 / 10 USD za 1 mln tokenów na start, potem 4 / 20 USD (30.09.2026); computer use w cenie
  tokenów modelu.
- **Skala:** 900 mln+ MAU (19.05.2026) → 950 mln MAU (wyniki za II kw., 22.07.2026) → „ponad 1 mld miesięcznie" (blog
  Google, 11.08.2026) *(dane firmy)*; Sensor Tower (V 2026): 662 mln MAU, 27,7% rynku.
- Alphabet nie wydziela subskrypcji AI: segment „subscriptions, platforms and devices" dał 12,9 mld USD w II kw. 2026
  (+15% r/r).

**Offline.** **Częściowo.** Gemini Nano na wspieranych telefonach robi offline proste rzeczy (streszczenie, korekta,
transkrypcja), ale to nie jest asystent. Aplikacja, Live, Spark, Agent i auto browse działają tylko w chmurze. Gemmę 4
można postawić u siebie obok DeepSeeka (licencję trzeba sprawdzić). Lokalny odpowiednik Sparka to harmonogram + kolejka
zadań z limitem równoległości (u mnie 4 sloty) + przeglądarka w kontenerze + planista i krytyk.

**Co przenieść do siebie.**
- **Planista + krytyk.** Krytyk dostaje tylko proponowaną akcję i cel użytkownika, nigdy treść strony czy dokumentu —
  wstrzyknięcie z pisma przeciwnika nie ma jak go przekonać. Na rigu to drugi slot DeepSeeka z krótkim promptem
  ([bezpieczeństwo agentów](../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md)).
- **Zbiory originów na zadanie:** domeny tylko do odczytu (ISAP, SAOS, biała lista VAT) i do zapisu (np. KSeF — wyłącznie
  po potwierdzeniu).
- **Deterministyczne wyzwalacze potwierdzeń, nie LLM:** kategoria adresu, użycie hasła, formularz płatności, przycisk
  „wyślij".
- **Kontrakt `safety_decision`** między modelem a wykonawcą: wykonawca odmawia akcji wymagającej potwierdzenia, dopóki
  nie dostanie jawnego „ack" od człowieka.
- **Tasks / Schedules / Skills** jako model mentalny dla nietechnicznego prawnika czy księgowej; umiejętności pod „/".
- **Hybryda odwrócona:** Google robi „Nano najpierw, chmura w zapasie"; dla kancelarii — zawsze lokalnie, chmura tylko za
  jawną zgodą na konkretne zapytanie.

**Warto wiedzieć.**
- **Polska poza agentem:** Spark wyłączony w EOG, auto browse tylko w USA; wpisy o Gemini w Chrome nie wspominają UE
  (UK dostało go 14.07.2026).
- **DMA:** ugoda ma podobno wymagać, by konkurencyjni asystenci dostali na Androidzie porównywalne funkcje (słowo-klucz,
  akcje w aplikacjach) do VII 2027; 30.09.2026 Google poprosił sąd UE o wstrzymanie nakazu otwarcia na rywali.
- **BragJack** (19.09.2026): złośliwe rozszerzenie „wymusza prompt" na uprzywilejowanym komponencie AI przeglądarki;
  dotknęło m.in. Gemini w Chrome, CVE-2026-0628.
- Strona pomocy Sparka uczciwie ostrzega: „Gemini can share your info with websites" i opisuje ryzyko prompt injection.
- **Korporacyjny „Gemini agent"** (8.10.2026): trwali agenci-współpracownicy z własnym mailem, kalendarzem i Dyskiem,
  którzy mogą kierować pracę także do modeli **Claude**.
- **Spory:** pozew o śmierć (III 2026) zarzucający Gemini zachęcanie do samobójstwa; kara 250 mln EUR we Francji (III 2024)
  m.in. za trening Barda na treściach wydawców.

**Źródła:** [Alphabet II kw. 2026](https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000066/googexhibit991q22026.htm) · [I/O 2026 — 9to5Google](https://9to5google.com/2026/05/19/google-io-2026-news/) ·
[Gemini 3.5 Flash i agenci](https://techcrunch.com/2026/05/19/with-gemini-3-5-flash-google-bets-its-next-ai-wave-on-agents-not-chatbots/) ·
[Spark w AI Pro](https://www.androidheadlines.com/2026/07/google-gemini-spark-expands-to-ai-pro-subscribers.html) · [Spark — pomoc Google](https://support.google.com/gemini/answer/16596215) ·
[Spark VII 2026](https://blog.google/innovation-and-ai/products/gemini-app/gemini-spark-updates-july-2026/) · [Spark — analiza](https://www.efficientlyconnected.com/google-io-2026-gemini-spark-consumer-ai-agent/) ·
[architektura bezpieczeństwa Chrome](https://blog.google/security/architecting-security-for-agentic/) · [auto browse](https://blog.google/products-and-platforms/products/chrome/gemini-3-auto-browse/) ·
[auto browse Android](https://blog.google/products-and-platforms/products/chrome/gemini-in-chrome-android-auto-browse/) · [Gemini Agent](https://blog.google/products/gemini/gemini-3-gemini-app/) ·
[computer use API](https://ai.google.dev/gemini-api/docs/computer-use) · [Computer Use model](https://blog.google/technology/google-deepmind/gemini-computer-use-model/) ·
[Mariner](https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/) · [Mariner — Wikipedia](https://en.wikipedia.org/wiki/Project_Mariner) ·
[1 mld użytkowników](https://blog.google/innovation-and-ai/products/gemini-app/one-billion-monthly-users/) · [Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) ·
[ceny PL](https://gemini.google/subscriptions/) · [ceny USA](https://gemini.google/us/subscriptions/?hl=en) ·
[Gemini zamiast Asystenta](https://www.businesstoday.in/amp/technology/news/story/google-assistant-to-be-replaced-by-gemini-starting-september-on-android-and-wearos-547570-2026-08-06) ·
[Live, Spark i DMA](https://thenextweb.com/news/gemini-live-spark-voice-agentic-tasks-dma-rival-assistants) · [Gems → Skills](https://9to5google.com/2026/09/27/gemini-gems-skills/) ·
[Gemini Nano](https://developer.android.com/ai/gemini-nano) · [Gemma](https://deepmind.google/models/gemma/) · [Gemini agent dla firm](https://techgenyz.com/google-gemini-agent-enterprise-ai/) ·
[BragJack](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/) · [Google Gemini — Wikipedia](https://en.wikipedia.org/wiki/Google_Gemini)


---

## 9. Cursor

**Kategoria:** profesjonalny (programiści) · **Kod:** zamknięty · **Firma:** Anysphere (USA), od 14.08.2026 spółka
zależna SpaceX · **Wynik: 87** (T5 I4 L4 A4)

> Edytor kodu (fork VS Code), w którym podpowiedzi, agent i recenzja kodu są jednym produktem — najszybciej rosnący
> asystent zawodowy w historii oprogramowania i wzorzec „wielu agentów równolegle” dla każdej branży.

**Otwarty czy zamknięty.** Zamknięty, własnościowy fork VS Code. Własne modele (Tab, Composer) bez publicznych wag.
Od 2.09.2026 „Self-Hosted Machines” pozwalają wykonywać kod i narzędzia na infrastrukturze klienta, ale zapytania do
modeli i tak przechodzą przez chmurę Cursora.

**Cel.** Zawodowi programiści i coraz częściej firmy — ok. 60% przychodu od klientów korporacyjnych
*(Bloomberg za prasą, III 2026)*. Problem: pisanie, zmiana i przegląd kodu w dużych repozytoriach; od 2026 również
delegowanie całych zadań agentom w chmurze.

**Funkcje.**
- **Tab** — przewidywanie następnej edycji w edytorze; agent w edytorze.
- **Cursor 3** (2.04.2026): okno agentów — równolegli agenci lokalnie, na worktree, na zdalnych maszynach albo
  w chmurze (izolowane VM z Ubuntu); sesję można przenieść z chmury na lokalny komputer i z powrotem.
- **Projects** (beta, 10.09.2026): agent-koordynator rozdziela pracę na równoległych subagentów.
- Boty **Rollouts** i **Security Review** (23.09.2026), **Bugbot** do recenzji PR, obsługa MCP, skills i hooków.
- Zdalne sterowanie lokalnymi agentami z aplikacji iOS (6.10.2026); agenci w chmurze bez połączenia z GitHubem
  (27.08.2026).

**Przewaga.**
- **Własny edytor** — podpowiedź, agent i recenzja dzielą kontekst; konkurent-wtyczka tego nie ma.
- **Własne modele** dostrojone do zadań w edytorze: Composer 2 (19.03.2026) — 61,3 w CursorBench, 61,7
  w Terminal-Bench 2.0, 73,7 w SWE-bench Multilingual przy cenie 0,50 / 2,50 USD za mln tokenów wejścia/wyjścia
  *(dane firmy)*.
- **Wybór modeli wielu dostawców** — użytkownik nie jest przywiązany do jednego laboratorium.
- Od przejęcia: dostęp do mocy obliczeniowej SpaceX *(dane firmy)*.

**Architektura.**
```
edytor (fork VS Code) ──▶ backend Cursora: „final prompt building” (także z kluczem API użytkownika)
   ├─ Tab: własny model podpowiedzi (przejęty Supermaven, XI 2024)
   ├─ agent: Composer 2 albo modele innych dostawców (wybór użytkownika)
   └─ wykonanie: lokalnie · worktree · Self-Hosted Machines · VM w chmurze (przenoszenie sesji)
koordynator (Projects) ──▶ subagenci równolegle ──▶ Bugbot / Security Review jako recenzenci
```
- **Composer 2** to Kimi K2.5 (otwarte wagi Moonshot AI) plus dalszy pretrening i RL Cursora; ok. ćwierć mocy
  treningowej pochodziła z bazy Kimi. Cursor nie ujawnił tego na starcie — znalazł to użytkownik, firma przyznała
  20.03.2026.
- **Privacy Mode:** brak trenowania na danych użytkownika i umowy zero retencji ze wszystkimi dostawcami modeli;
  zapytania, które uruchomią klasyfikatory nadużyć, mogą być jednak przechowane. SOC 2 Type II.

**Na czym zarabia.** Subskrypcje z pulą użycia modeli i dopłatą za nadwyżkę (X 2026): Hobby 0, Individual 20 USD/mies.,
Teams 40 USD/użytkownik/mies., Enterprise indywidualnie; w VII 2026 wymieniano też Pro+ 60 USD i Ultra 200 USD.
- ARR: 100 mln USD (I 2025) → 500 mln (VI 2025) → ponad 1 mld (XI 2025) → 2 mld (II 2026, Bloomberg) → 3 mld USD
  (V 2026, Bloomberg za Wikipedią); ok. 4 mld w VI 2026 — niezweryfikowane.
- Finansowanie: seria C 900 mln USD przy 9,9 mld (5.06.2025), seria D 2,3 mld USD przy 29,3 mld (13.11.2025).
- **SpaceX:** opcja z 21.04.2026 (zakup za 60 mld USD albo 10 mld za wspólną pracę), wykonana 16.06.2026, transakcja
  w akcjach zamknięta 14.08.2026 — 389 289 254 akcji klasy A SpaceX.

**Offline.** **Nie.** Każde zapytanie przechodzi przez backend Cursora, nawet z własnym kluczem API. Self-Hosted
Machines trzymają kod i wykonanie narzędzi u klienta, lokalnej inferencji modelu nie znalazłem. W pełni lokalny
odpowiednik to otwarte harnessy z lokalnym modelem (Cline, OpenCode, Kilo Code — patrz
[przegląd harnessów](../harnessy-agentowe/README.md)).

**Co przenieść do siebie.**
- **Okno równoległych agentów, nie tylko dla kodu.** 4 sloty DeepSeeka = 4 agenci na jednej sprawie, każdy na
  własnej kopii roboczej (odpowiednik worktree): chronologia z akt, weryfikacja cytatów, projekt pisma, lista
  terminów. Prawnik widzi cztery karty postępu i scala wyniki — [13-FLOTA-WIELU-AGENTOW.md](../kurs_aplikacje_agentowe/13-FLOTA-WIELU-AGENTOW.md).
- **Koordynator + recenzent.** Wzorzec Projects/Bugbot: jeden agent dzieli pracę, osobny agent tylko recenzuje
  (np. „czy każdy przepis w piśmie istnieje w ISAP i ma właściwe brzmienie”).
- **Przenoszenie sesji jest proste tylko wtedy, gdy wiesz, co jest w kontekście.** W hybrydzie z Opusem przenosisz
  plan, nigdy dokumenty klienta.
- **Otwarta baza + dotrenowanie na śladach zadań** — tak powstał Composer; ta sama droga jest możliwa dla polskiego
  tekstu prawniczego czy medycznego. I ujawnij model bazowy — ukrycie Kimi kosztowało Cursora zaufanie.
- **Cennik:** u Cursora agenci zjadali marżę, stąd kredyty. Lokalny model na sprzęcie klienta ma koszt krańcowy bliski
  zera — stała licencja na stanowisko albo biuro to przewaga strukturalna, a zmiany cen ogłaszaj wcześnie i jasno.

**Warto wiedzieć.**
- 16.06.2025 plan Pro zmienił się z 500 zapytań na 20 USD kredytu po cenach API plus „nielimitowany” tryb Auto;
  użytkownicy nie wiedzieli, że „nielimitowany” dotyczy tylko Auto, dostali niespodziewane rachunki; 4.07.2025
  Cursor przeprosił i zwrócił pieniądze.
- IV 2025: firmowy bot wsparcia „Sam” wymyślił nieistniejącą zasadę logowania; użytkownicy rezygnowali — lekcja dla
  każdego, kto stawia agenta przed klientem.
- Po przejęciu zespół dołączył do SpaceXAI (Grok Build, Grok API); pierwszy wspólny efekt to Grok 4.6. Dla klientów
  z UE dostawcą jest teraz SpaceX.
- Przejęcia: Supermaven (XI 2024), Koala (VII 2025), Graphite (XII 2025).

**Źródła:** [cennik](https://cursor.com/pricing) · [changelog](https://cursor.com/changelog) ·
[Composer 2](https://cursor.com/blog/composer-2) · [czerwiec 2025: ceny](https://cursor.com/blog/june-2025-pricing) ·
[wykorzystanie danych](https://cursor.com/data-use) · [bezpieczeństwo](https://cursor.com/security) ·
[dołączenie do SpaceX](https://cursor.com/blog/joining-spacex) ·
[Wikipedia](https://en.wikipedia.org/wiki/Cursor_(company)) ·
[Bloomberg: 2 mld USD ARR](https://www.bloomberg.com/news/articles/2026-03-02/cursor-recurring-revenue-doubles-in-three-months-to-2-billion) ·
[Gigazine: Kimi](https://gigazine.net/gsc_news/en/20260323-cursor-admits-composer-2-kimi) ·
[DataCamp: Cursor 3](https://www.datacamp.com/blog/cursor-3) ·
[Silicon Canals: klienci korporacyjni](https://siliconcanals.com/t-cursor-100-million-2-billion-annualized-revenue-13-months/) ·
[Jetadmin: plany](https://www.jetadmin.io/blog/cursor-pricing-explained-plans-credit-system-and-real-costs-in-2026/)


---

## 10. Granola

**Kategoria:** profesjonalny (spotkania) · **Kod:** zamknięty · **Firma:** Granola Labs Ltd / Granola Inc.
(Wielka Brytania / USA) · **Wynik: 87** (T4 I5 L5 A3)

> „Notatnik AI” bez bota na spotkaniu: nagrywa dźwięk z własnego komputera, a model rozwija Twoje szkicowe notatki
> o to, co padło w rozmowie. Wzorzec najłatwiejszy do odtworzenia w pełni lokalnie — i przestroga o zgodzie.

**Otwarty czy zamknięty.** Zamknięty. Aplikacja przechwytuje dźwięk na urządzeniu, ale transkrypcja i modele
działają w chmurze. Self-hostingu brak.

**Cel.** Ludzie, którzy spędzają dzień na spotkaniach: założyciele, inwestorzy, sprzedaż, produkt, konsultanci.
Zamiast nagrania wideo — uporządkowana notatka i czat po wszystkich wcześniejszych spotkaniach.

**Funkcje.**
- Notatki z dźwięku urządzenia (mikrofon + dźwięk systemowy) — żaden bot nie dołącza do rozmowy.
- Szablony per typ spotkania; Granola Chat (do wyboru Claude, GPT lub Gemini).
- Team Spaces — wspólne notatki i wyszukiwanie w zespole.
- **Serwer MCP** oraz osobiste i firmowe API (od 25.03.2026).
- Briefy przed spotkaniem, maile follow-up, integracje CRM (HubSpot, Affinity, Attio; Salesforce w Enterprise),
  słownik firmowy.

**Przewaga.**
- **UX notatek:** piszesz kilka haseł, model rozwija je na podstawie transkrypcji — wynik odzwierciedla to, co Ty
  uznałeś za ważne, a nie streszczenie wszystkiego.
- **Brak bota** = brak społecznego tarcia na spotkaniu (patrz jednak „Warto wiedzieć”).
- **Wzrost oddolny:** klienci m.in. Vanta, Gusto, Asana, Cursor, Lovable, Mistral AI (III 2026). YipitData (IV 2026):
  Granola zabiera użytkowników Fathom, Otter i Fireflies, przejścia są jednokierunkowe, „near-zero churn”, przyrost
  nowych użytkowników ×9 między I a II 2026 *(blog dostawcy danych)*.

**Architektura.**
```
aplikacja desktop/mobilna: mikrofon („Me”) + dźwięk systemowy („Them”)
  └▶ strumień audio do chmurowego ASR ──▶ transkrypcja (audio nie jest zapisywane)
     └▶ LLM: notatki użytkownika + transkrypcja + szablon ──▶ notatka
        └▶ indeks spotkań ──▶ czat, MCP, API, CRM
```
- Diaryzacja: na Zoom, Meet i Teams z nazw uczestników; w innych przypadkach tylko „Me” (kanał mikrofonu) vs „Them”
  (dźwięk systemowy), a mówców model wnioskuje z kontekstu.
- ASR podobno Deepgram i AssemblyAI, streszczenia modelami OpenAI i Anthropic — niezweryfikowane przez Granolę.
- Aplikacja webowa nie nagrywa spotkań. SOC 2 Type II; Enterprise dodaje przestrzenie zgodne z HIPAA, SSO/SCIM,
  polityki automatycznego usuwania i API audytu.

**Na czym zarabia.** Freemium za stanowisko (cennik, X 2026): Basic 0 USD (historia 30 dni), Business 14 USD,
Enterprise 35 USD za użytkownika miesięcznie.
- Finansowanie: seed 4,25 mln USD (V 2023); seria A 20 mln (X 2024, przy 5 tys. użytkowników tygodniowo); seria B
  43 mln przy wycenie 250 mln (V 2025); **seria C 125 mln USD przy 1,5 mld** (25.03.2026, Index Ventures, Kleiner
  Perkins); łącznie 192 mln USD *(TNW)*.
- ARR nieujawniony; przychód ×2,5 między I a III 2026, ARR +ok. 250% w I kw. 2026 *(agregator za blogiem firmy)*;
  250 tys.+ aktywnych użytkowników w połowie 2025 — niezweryfikowane.

**Offline.** **Nie.** Przechwytywanie jest lokalne, ale ASR i LLM działają w chmurze. Lokalny odpowiednik jest
prosty: dwa kanały audio → lokalny STT (Whisper/Parakeet, zob. [Głos](../harnessy-agentowe/02-KLOCKI.md#głos)) →
lokalny LLM. Godzinna rozmowa po transkrypcji to, z mojego szacunku, kilkanaście–dwadzieścia kilka tysięcy tokenów —
mieści się w 131k kontekstu jednego slotu DeepSeeka z zapasem na notatki i szablon.

**Co przenieść do siebie.**
- **Darmowa diaryzacja z dwóch kanałów:** mikrofon = profesjonalista, dźwięk systemowy = klient na wideorozmowie.
  Przy spotkaniu w gabinecie potrzebna już prawdziwa diaryzacja (pyannote offline).
- **Notatki użytkownika jako rusztowanie.** Prawnik notuje „termin? / wysokość kary umownej / świadek Kowalski”,
  model rozwija każdy punkt i dokłada cytat z transkrypcji z czasem.
- **Usuwanie audio, zostaje tekst** — argument dla prawników i lekarzy; na desce można pójść dalej: transkrypcja
  szyfrowana w katalogu sprawy, z polityką retencji.
- **Szablony per typ spotkania** (pierwsza rozmowa z klientem, narada w sprawie, konsultacja podatkowa)
  i **serwer MCP z notatkami** — inne agenty na rigu (np. agent pism) korzystają z ustaleń spotkania.
- **Zgoda z założenia:** wyraźny komunikat dla wszystkich uczestników przed nagraniem i zapis tej zgody w notatce.
  Odciski głosu traktuj jak dane biometryczne (art. 9 RODO). To nie jest porada prawna.

**Warto wiedzieć.**
- Na początku 2025 badacze znaleźli w becie na macOS zaszyty na stałe klucz API AssemblyAI.
- 23.06.2026 zgłoszono podatność nawigacji w aplikacji desktop; poprawka serwera dzień później, obejście załatane
  26.06, pełne zamknięcie potwierdzone 29.06.
- VII 2026 (prasa): notatki były domyślnie udostępniane linkiem, a trenowanie modeli domyślnie włączone w planach
  Free i Business (Enterprise wyłączone).
- 30.07.2026: proponowany pozew zbiorowy *Chamberlain v. Granola* (N.D. Cal., 3:26-cv-07926-EMC) — zarzut nagrywania
  osób bez konta „niewidocznie” i trenowania na ich danych domyślnie. **Brak bota nie zwalnia z obowiązku zgody.**

**Źródła:** [TNW: seria C](https://thenextweb.com/news/granola-series-c-meeting-ai-enterprise-context) ·
[cennik](https://www.granola.ai/pricing) ·
[dokumentacja: transkrypcja](https://docs.granola.ai/help-center/taking-notes/transcription) ·
[YipitData](https://www.yipitdata.com/resources/blog/granola-vs-fathom-otter-fireflies-ai-notetaking) ·
[SoftwareTestingHelp: dostawcy ASR](https://www.softwaretestinghelp.com/?p=411472) ·
[ARR.club](https://www.arr.club/granola/granola-arr-grow-at-250-in-q1-2026) ·
[Sacra: użytkownicy](https://sacra.com/research/250m-year-granola-for-plumbers) ·
[klucz AssemblyAI](https://afadeev.substack.com/p/the-hidden-dangers-of-ai-note-taking) ·
[podatność VI 2026](https://docs.granola.ai/help-center/policies/security-contributions/desktop-app-navigation-vulnerability) ·
[Startup Fortune: prywatność](https://startupfortune.com/granola-ai-meeting-notes-are-not-as-private-as-you-might-think/) ·
[PPC Land: pozew](https://ppc.land/granola-sued-for-recording-meetings-without-consent-to-train-ai-models/)


---

## 11. Sierra

**Kategoria:** profesjonalny (obsługa klienta) · **Kod:** zamknięty · **Firma:** Sierra Technologies (USA) ·
**Wynik: 85** (T4 I5 L4 A4)

> Agenci obsługi klienta dla największych marek konsumenckich, rozliczani za wynik, a nie za tokeny — i firma, która
> dała rynkowi miarę niezawodności agentów (pass^k) oraz protokół dla osobistych agentów.

**Otwarty czy zamknięty.** Produkt zamknięty (chmura). Otwarte są benchmark **τ-bench** i **Personal Agent Protocol**
(z Metą). Dostawcy modeli, na których działają agenci, nie są opisani w moich źródłach; własny jest „fleming-1” —
model wykrywający dzwoniące AI (8.10.2026).

**Cel.** Duże firmy B2C: 25% Fortune 20, połowa klientów ma przychód ponad 1 mld USD (II 2026), ponad 40% Fortune 50
(V 2026) *(dane firmy / TechCrunch)*. Klienci m.in. Rocket Mortgage, SiriusXM, ADT, Cigna, DIRECTV, Gap, Rivian,
Sutter Health. Problem: rozwiązywanie spraw klientów (zwroty, zmiany planów, wnioski) w każdym kanale, bez kolejki.

**Funkcje.**
- **Agent OS 2.0** (5.11.2025): jeden agent we wszystkich kanałach, Agent Studio 2.0, Agent Data Platform
  (pamięć i kontekst klienta).
- **Horizon** (16.07.2026): agenci realizujący cel przez dni i miesiące, np. udzielenie kredytu hipotecznego albo
  autoryzacja świadczenia zdrowotnego.
- Voice Personas (7.08.2026); Ghostwriter w Slacku i Teams (28.09.2026).
- **Personal Agent Protocol** (6.10.2026) z Metą oraz m.in. Genesys, Shopify, Stripe, Walmart.
- „fleming-1” — wykrywanie, że po drugiej stronie dzwoni AI (8.10.2026).

**Przewaga.**
- **Cena za wynik** przenosi ryzyko na dostawcę — klientowi łatwiej kupić, a Sierra musi naprawdę rozwiązywać sprawy.
- **Metodyka wąskich zadań:** Sierra tłumaczy swój wzrost tym, że wygrywają wąskie „jobs to be done” ze zdefiniowaną
  miarą sukcesu (w kontrze do tezy MIT, że 95% pilotaży AI upada).
- **Dane z interakcji** jako fosa, „która się kumuluje” *(dane firmy)*; wiarygodność założycieli (Bret Taylor,
  Clay Bavor) przy sprzedaży do zarządów.

**Architektura.**
- **Context Engine** i planowanie długoterminowe między kolejnymi kontaktami (Horizon) — agent pamięta, na jakim
  etapie jest sprawa, i sam wraca do niej po dniach.
- **Jeden agent, wiele kanałów** (czat, głos, Slack/Teams) na wspólnej platformie danych.
- **Ewaluacja — τ-bench** (20.06.2024): symulowany użytkownik i symulowane API, zasady domenowe (np. polityka zwrotów).
  Miara **pass^k** — czy agent rozwiąże to samo zadanie k razy z rzędu. GPT-4o spadał w handlu detalicznym do ok. 25%
  przy pass^8, o 60% mniej niż przy pass^1.
- **Personal Agent Protocol:** otwarty standard oparty na OAuth — jak osobisty agent użytkownika (w stylu OpenClaw)
  uwierzytelnia się w firmie i działa przez stronę, API (MCP/OpenAPI) albo agenta firmy. „Konsument decyduje, jaki
  dostęp daje agentowi, firma ustala parametry.”

**Na czym zarabia.** **Opłata za wynik** (od 10.12.2024): rozwiązana rozmowa, uratowana rezygnacja, sprzedaż
dodatkowa; „jeśli rozmowa nie jest rozwiązana, w większości przypadków nie ma opłaty”. Przy Horizon: „płacisz za
wyniki, nie za tokeny”.
- ARR: 100 mln USD (koniec XI 2025, 7 kwartałów od startu w II 2024), ponad 150 mln USD i pierwszy kwartał
  z 50 mln USD (II 2026) *(dane firmy)*.
- Wycena: 10 mld USD (XI 2025, Forbes); **950 mln USD przy wycenie ponad 15 mld USD** (4.05.2026, Tiger Global i GV)
  *(TechCrunch)*.

**Offline.** **Nie.** Produkt chmurowy. Lokalny odpowiednik dla polskiego biura (rejestracja w przychodni,
recepcja kancelarii) potrzebowałby: lokalnego modelu z zasadami w prostym języku, ograniczonego zestawu narzędzi
(kalendarz, karta klienta), STT/TTS dla telefonu — i testów niezawodności przed wdrożeniem.

**Co przenieść do siebie.**
- **pass^k zamiast „działa na demo”.** Każdy scenariusz testowy uruchom 8 razy; 4 sloty DeepSeeka liczą to równolegle.
  Profesjonalista potrzebuje powtarzalności bardziej niż szczytowej jakości. Symulowany klient = drugi agent
  z opisem persony — [14-EWALUACJA.md](../kurs_aplikacje_agentowe/14-EWALUACJA.md).
- **Agent sprawy na miesiące (Horizon):** pamięć etapu sprawy, terminy procesowe i przypomnienia uruchamiane z
  harmonogramu — [11-HARMONOGRAM-PROAKTYWNOSC.md](../kurs_aplikacje_agentowe/11-HARMONOGRAM-PROAKTYWNOSC.md).
- **Cena za wynik tam, gdzie wynik da się policzyć:** za gotowy dokument, za zamknięty miesiąc księgowy, za
  rozliczony pakiet faktur KSeF — zamiast za tokeny, których lokalnie i tak prawie nie liczysz.
- **Wąskie zadanie ze zdefiniowaną miarą sukcesu** na start (np. „projekt odpowiedzi na wezwanie do zapłaty
  zatwierdzony bez poprawek”), a nie „asystent do wszystkiego”.
- **Protokół zamiast scrapingu:** gdy banki i urzędy zaczną wystawiać interfejsy dla osobistych agentów (PAP),
  agent biura będzie działał przez API z jawnie nadanym dostępem — warto już teraz oddzielać warstwę narzędzi od
  logiki agenta ([09-PROTOKOLY-MCP-CLI-A2A.md](../kurs_aplikacje_agentowe/09-PROTOKOLY-MCP-CLI-A2A.md)).

**Warto wiedzieć.**
- Założona przez Breta Taylora i Claya Bavora; start produktu w II 2024.
- Ekspansja do Francji i biuro w Tokio (XII 2025); przejęcie startupu Fragment z YC (23.04.2026).
- Bezpośredni konkurent Decagon (seria D 250 mln USD przy 4,5 mld, 27.01.2026) tego samego dnia co PAP ogłosił
  własny protokół zgody i zaufania dla osobistych agentów, PACT (6.10.2026) — standard nie jest jeszcze przesądzony.
- Rynek idzie w stronę ceny za wynik: Intercom Fin bierze 0,99 USD za rozwiązaną sprawę, Parloa — za minutę lub
  interakcję *(cenniki firm)*.

**Źródła:** [Sierra: blog](https://sierra.ai/blog) · [rok drugi](https://sierra.ai/blog/year-two-in-review) ·
[Horizon](https://sierra.ai/blog/horizon) ·
[cena za wynik](https://sierra.ai/blog/outcome-based-pricing-for-ai-agents) ·
[τ-bench](https://sierra.ai/blog/benchmarking-ai-agents) ·
[Personal Agent Protocol](https://sierra.ai/blog/introducing-personal-agent-protocol) ·
[TechCrunch, 4.05.2026](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/) ·
[Forbes, XI 2025](https://www.forbes.com/sites/richardnieva/2025/11/05/sierra-bret-taylor-clay-bavor/) ·
[Decagon: seria D](https://decagon.ai/blog/series-d-announcement) · [Decagon: blog](https://decagon.ai/blog) ·
[Intercom: cennik](https://www.intercom.com/pricing) · [Parloa: cennik](https://www.parloa.com/platform/pricing/)


---

## 12. OpenEvidence

**Kategoria:** profesjonalny (medycyna) · **Kod:** zamknięty · **Firma:** OpenEvidence Inc. (USA) ·
**Wynik: 84** (T5 I4 L4 A3)

> Wyszukiwarka wiedzy klinicznej dla lekarzy, która odpowiada z cytatami z licencjonowanych czasopism, jest darmowa
> dla zweryfikowanych lekarzy i zarabia na reklamach farmaceutycznych. Dowód, że licencjonowane źródła wygrywają
> z większym modelem.

**Otwarty czy zamknięty.** Zamknięty, chmura. Dostawcy modeli nie są publiczni.

**Cel.** Lekarze i inni zweryfikowani klinicyści w USA: szybka, cytowana odpowiedź na pytanie kliniczne w trakcie
pracy. Od 2025–2026 także scribe wizyt (Visits) i Doctor Dialer.

**Funkcje.**
- Odpowiedzi na pytania kliniczne z cytatami w tekście.
- DeepConsult (VII 2025) — dłuższe, wieloźródłowe opracowanie.
- Voice Mode (V 2026).
- **Visits** (scribe) i **Doctor Dialer**.
- Integracja z EHR w Cedars-Sinai (V 2026).
- Deklarowane 100% na egzaminie USMLE *(dane firmy, 2025)*.

**Przewaga.**
- **Licencjonowana treść:** NEJM, JAMA Network, NCCN, Wiley, Cochrane — tego nie skopiuje konkurent z „większym
  modelem”.
- **Darmowe dla lekarzy** po weryfikacji — próg wejścia zerowy.
- **Zasięg:** wg ankiety Offcall (XII 2025) z OpenEvidence korzysta więcej lekarzy w USA niż ze wszystkich innych
  narzędzi AI dla lekarzy razem *(za Sacra)*.

**Architektura.**
```
zweryfikowany lekarz ──▶ pytanie (tekst / głos)
  └▶ wyszukiwanie w kuratorowanym, licencjonowanym korpusie literatury (RAG)
     └▶ LLM: odpowiedź z cytatami w tekście ──▶ link do źródła
osobno: Visits (scribe) · Doctor Dialer · integracja z EHR
```
- Wartość jest w warstwie wyszukiwania i licencji, nie w modelu — modele nie są ujawnione.
- W VI 2025 firma pozwała Pathway o rzekome wydobycie promptów (prompt extraction) — sposób składania kontekstu
  traktuje jako wartość do ochrony.

**Na czym zarabia.** **Reklamy** farmaceutyczne i producentów wyrobów medycznych: 70–150 USD CPM (niektóre źródła
mówią o 1 000+ USD) *(Sacra)*.
- Przychód: ok. 7,9 mln USD (XII 2024) → 50 mln (VI 2025) → 150 mln (koniec 2025) → ok. 300 mln USD w ujęciu rocznym
  (VII–IX 2026); marża brutto ok. 90% *(szacunek Sacra)*.
- Finansowanie: 75 mln USD przy 1 mld (II 2025); 210 mln przy 3,5 mld (VII 2025); 200 mln przy 6 mld (X 2025);
  **250 mln USD przy 12 mld** (21.01.2026); łącznie ok. 700 mln USD *(prasa)*. Sacra podaje 15 mld USD (IX 2026) —
  niezweryfikowane.
- Użycie: 760 tys. lekarzy i 18 mln konsultacji miesięcznie (XII 2025); ok. 20 mln miesięcznie (I 2026); 1 mln
  w jeden dzień (10.03.2026) *(dane firmy za Sacra/Wikipedią)*.

**Offline.** **Nie.** Ale to wzorzec **najłatwiejszy do uruchomienia w pełni lokalnie**: RAG nad polskimi
wytycznymi towarzystw naukowych (np. PTK, PTD), Charakterystykami Produktów Leczniczych (ChPL) i rekomendacjami
AOTMiT. Trudne są licencje na treść i jej aktualizacja, nie model.

**Co przenieść do siebie.**
- **Źródła ważniejsze niż model.** Na rigu: indeks ChPL i wytycznych w katalogu tylko do odczytu, każda odpowiedź
  z cytatem (dokument, sekcja, data wersji), a brak źródła = „nie wiem”, nie domysł.
- **Wersjonowanie korpusu:** przy każdej odpowiedzi data wydania wytycznej; osobne zadanie z harmonogramu sprawdza
  nowe wersje (to jest „trudna część” — nie wiedza modelu).
- **Oddziel wiedzę od danych pacjenta.** Pytanie kliniczne bez danych osobowych może w hybrydzie trafić do Opusa;
  pytanie z dokumentacją pacjenta — wyłącznie DeepSeek na desce
  ([10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md)).
- **Uważaj na zakres:** odpowiedzi kliniczne są bliżej wsparcia decyzji niż scribe. Kodeks Etyki Lekarskiej art. 12
  wymaga przy AI w postępowaniu diagnostycznym lub leczniczym zgody pacjenta i certyfikowanego narzędzia — produkt
  „wyszukiwarka wytycznych z cytatami” musi to jasno opisać w przeznaczeniu (to nie jest porada prawna).
- **Model biznesowy „darmowe dla profesjonalisty, płaci ktoś inny”** wymaga ogromnej publiczności; dla lokalnego
  produktu realniejsza jest droga Noxtua — partnerstwo z wydawcą treści ([#14-noxtua](#14-noxtua)).

**Warto wiedzieć.**
- Założyciele: Daniel Nadler (wcześniej Kensho) i Zachary Ziegler.
- Konflikt z Doximity (spór wokół Pathway, przejętego przez Doximity w VIII 2025); obie firmy zmierzają do
  „asystenta lekarza do wszystkiego”.
- OpenAI uruchomił ChatGPT for Clinicians w IV 2026 — bezpośrednia konkurencja *(za Sacra)*.
- Tło: 81% lekarzy w USA użyło AI w 2026 (38% w 2023), najczęściej do streszczeń badań (39%) — ale 71% mówi, że ma
  mały lub żaden wpływ na wybór narzędzi w placówce *(ankieta AMA, III 2026)*. W polskich prywatnych gabinetach
  lekarz jest i użytkownikiem, i kupującym.

**Źródła:** [Wikipedia](https://en.wikipedia.org/wiki/OpenEvidence) ·
[Sacra: OpenEvidence](https://sacra.com/c/openevidence/) ·
[Rutland Herald: runda 250 mln USD](https://www.rutlandherald.com/news/business/openevidence-raises-250-million-to-build-medical-superintelligence-for-doctors/article_0960939c-ca41-5321-8417-54f84800ece6.html) ·
[Sacra: OpenEvidence vs Doximity](https://sacra.com/research/openevidence-vs-doximity/) ·
[Wikipedia: Doximity](https://en.wikipedia.org/wiki/Doximity) ·
[ASCO Post: ankieta AMA](https://ascopost.com/news/march-2026/ama-survey-finds-rapid-growth-in-physician-ai-adoption/) ·
[Physicians Practice: wpływ na wybór](https://www.physicianspractice.com/view/physician-ai-use-is-surging-is-your-practice-ready-) ·
[Kodeks Etyki Lekarskiej (PDF)](https://nil.org.pl/uploaded_images/1723037323_kel-2305.pdf)


---

## 13. browser-use

**Kategoria:** wykonawca · **Kod:** otwarty rdzeń (MIT) + zamknięta chmura ·
⭐ <!-- gh:browser-use/browser-use -->117,6k · **Firma:** Browser Use, Inc. (założyciele z ETH Zurych) ·
**Wynik: 83** (T4 I4 L4 A5)

> Najpopularniejsza otwarta biblioteka „rąk w przeglądarce": zamienia stronę na tekstowy opis klikalnych elementów,
> więc model działa na przyciskach i polach zamiast zgadywać z pikseli — fundament, na którym wystartował m.in. Manus.

**Otwarty czy zamknięty.** Otwarty rdzeń: biblioteka Python na MIT (ostatnie wydanie 0.13.11, 7.10.2026) i otwarte
wagi BU-30B-A3B-Preview (MoE: 30B parametrów, 3B aktywnych, 65k kontekstu, do uruchomienia w vLLM; 16.12.2025).
Zamknięte: Browser Use Cloud (agenci V3/V4, przeglądarki „stealth", proxy) i model BU 2.0 dostępny tylko przez API.
Self-hosting biblioteki — tak.

**Cel.** Programiści i firmy automatyzujący przepływy webowe: wypełnianie formularzy, zbieranie danych, research
przez wiele stron. Firmę założyli w 2024 Magnus Müller i Gregor Zunic (Student Project House ETH Zurych). W praktyce
to infrastruktura — „ręce", z których korzystają inni agenci (Manus na starcie, OpenManus jako domyślny serwer MCP
przeglądarki).

**Funkcje.**
- Obserwacja strony jako tekst/DOM interaktywnych elementów; zrzuty ekranu jako uzupełnienie.
- Sterowanie Chromium przez surowy **Chrome DevTools Protocol** („100% CDP-based" od 19.08.2025; wcześniej Playwright).
- Dowolny model przez endpoint OpenAI-compatible, także lokalny.
- Chmura — trzy generacje agentów *(dane firmy)*: V2 (ok. 0,70 USD/zadanie, 54% trafności), V3 „krok po kroku"
  (ok. 0,87 USD, 67%), V4 piszący i uruchamiający kod (ok. 1,64 USD, 76% „on difficult tasks", ok. 5 min).
- Profile przeglądarki z trwałym logowaniem; **sekrety przypięte do `allowedDomains`**.
- Harmonogram agentów V4 i umiejętność „Agency" (17.08.2026): praca proaktywna, zatwierdzenie tylko przed akcją
  zewnętrzną (wysłanie, publikacja).
- Proxy domowe, darmowy próg (od 3.04.2026), progi współbieżności od 10 do 1000 sesji.

**Przewaga.**
- **Największy zasięg wśród otwartych agentów przeglądarkowych** (117,6k ⭐, API GitHuba 11.10.2026).
- **Tekst zamiast pikseli** — taniej, odporniej i z modelami bez wizji.
- **Własne małe modele specjalistyczne:** na własnym Browser Use Bench v2.1 (180 długich zadań na żywym webie,
  7.10.2026) „BU fast" ma 72,9 pkt za 0,11 USD/zadanie — mniej więcej tyle co Claude Sonnet 5.5 high (72,7) za
  1,53 USD; Claude Opus 5.5 — 75,0; GPT-6.1 Sol — 79,6 *(benchmark producenta)*.
- **Koszt zadania obok trafności** — firma pokazuje USD/zadanie, a nie tylko procenty.

**Architektura.**
```
zadanie ─► agent: LLM (chmura / lokalny endpoint / BU-30B-A3B w vLLM)
              ▲  tekstowy opis interaktywnych elementów strony (+ zrzut, gdy trzeba)
              │  akcja na wskazanym elemencie
           Chromium ◄── Chrome DevTools Protocol (bez Playwrighta)
              └─ profil z ciasteczkami · sekrety wstrzykiwane tylko na allowedDomains
```
- **Pętla:** strona → skrócona reprezentacja elementów interaktywnych → model wybiera akcję → wykonanie przez CDP →
  nowa obserwacja. Model nie musi widzieć obrazu.
- **V4 (chmura):** agent pisze skrypt przeglądarki zamiast klikać krok po kroku — przy długich zbiorach danych mniej
  wywołań modelu.
- **Chmura:** zarządzane sesje Chromium „stealth" rozliczane za godzinę przeglądarki, proxy domowe, odsprzedaż tokenów.
- **Zatwierdzenia:** Agency pyta „only before an external action like sending or publishing".
- **Ewaluacja:** własny benchmark z kosztem na zadanie; niezależnie — leaderboard Princeton HAL Online-Mind2Web.

**Na czym zarabia.**
- **Open core:** biblioteka darmowa, przychód z Browser Use Cloud.
- **Cennik** (strona z 3.09.2026, *dane firmy*): kredyty pay-as-you-go, które nie wygasają, plus kontrakty enterprise;
  przeglądarka 0,02 USD/godz.; proxy domowe 5 USD/GB (obniżka z 10 USD/GB 3.04.2026); transfer 0,20 USD/GB; tokeny
  odsprzedawane (domyślny GPT-5.6 Luna 0,24 / 1,44 USD, BU 2.0 0,60 / 3,50 USD za 1 mln tokenów wejścia/wyjścia);
  stary V2 „od 0,006 USD/krok" plus 0,01 USD/zadanie.
- **Finansowanie:** 17 mln USD seed prowadzony przez Felicis (z YC, Paulem Grahamem, A Capital, Nexus, SV Angel),
  ogłoszony w III 2025. Późniejszych rund, ARR ani liczby użytkowników nie udało się potwierdzić.

**Offline.** **Częściowo.** Biblioteka MIT działa na Twojej maszynie z lokalną przeglądarką i lokalnym endpointem
OpenAI-compatible, a BU-30B-A3B to otwarte wagi do vLLM. Bez internetu da się więc obsługiwać **lokalne aplikacje
webowe** (intranet, system kancelarii w sieci lokalnej); strony publiczne z natury wymagają sieci. Przeglądarki
stealth, proxy, BU 2.0 i agenci V3/V4 — tylko w chmurze.

**Co przenieść do siebie.**
- **DOM i drzewo dostępności najpierw, zrzut awaryjnie** — to jedyna droga dla tekstowego DeepSeek-V4-Flash; model
  z wizją musiałby i tak iść na osobną kartę albo do chmury.
- **Mały model do rutynowych kroków, duży do planu** (wzorzec BU fast): u Ciebie DeepSeek klika i wypełnia, Opus 5.5
  wchodzi tylko przy trudnym planie albo po nieudanej próbie.
- **Agent piszący kod dla długich zbiorów danych** (wzorzec V4): zamiast 200 kliknięć jeden skrypt w piaskownicy —
  przy 13,6 tok/s to różnica między minutami a godziną.
- **Sekrety przypięte do domen:** hasło do portalu działa tylko na jego domenie, więc strona podszywająca się pod
  portal go nie dostanie; do tego profil agenta oddzielony od przeglądarki użytkownika.
- **Zatwierdzenie tylko przed akcją zewnętrzną** (wysłanie, publikacja) i **koszt na zadanie w każdej ewaluacji**
  ([kurs 2, część 14](../kurs_aplikacje_agentowe/14-EWALUACJA.md)).

**Warto wiedzieć.**
- **Marketing benchmarków:** w XII 2024 firma ogłosiła 89,1% na WebVoyager — po usunięciu 55 z 586 zadań i ręcznej
  korekcie werdyktów ewaluatora. Na niezależnym Princeton HAL Online-Mind2Web browser-use z Claude Sonnet 4 ma 40,0%
  (pełny przebieg 1577 USD; HAL zastrzega, że koszty mogą być zawyżone do 2×). Różnica producent–niezależni to zwykle
  ok. 2×.
- **BU 2.0** (27.01.2026) wg producenta dorównał Claude Opus 4.5 (83,3% vs 82,3%) przy ok. 40% krótszym czasie
  (62 vs 104 s na zadanie) — ale tylko jako API, bez wag.
- **Bezpieczeństwo całej kategorii:** OpenAI (22.12.2025) — prompt injection „unlikely to ever be fully 'solved'";
  Gartner (8.12.2025) zalecił firmom blokowanie przeglądarek AI. Lokalne wykonanie usuwa wyciek do chmury, ale nie
  wstrzyknięcia ([kurs 2, część 16](../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md)).
- **Rynek:** OpenAI zamknął przeglądarkę Atlas (ogłoszenie 9.07.2026, koniec 9.08.2026), bo „the browser is a
  feature, not the destination"; wszystkie przeglądarki AI razem miały <1% rynku (VIII 2026). Wygrywa warstwa „rąk" —
  biblioteki, rozszerzenia, chmurowe przeglądarki — a nie nowa przeglądarka.
- Kontrybutor browser-use (MagMueller) zintegrował Browser Use CLI 3.0 z OpenManus (VIII 2026) — biblioteka staje się
  domyślnym serwerem MCP przeglądarki dla innych agentów.

**Źródła:** [GitHub](https://github.com/browser-use/browser-use) · [API GitHuba](https://api.github.com/repos/browser-use/browser-use) · [cennik](https://browser-use.com/pricing.md) · [benchmarki](https://browser-use.com/benchmarks) · [changelog 3.04.2026](https://browser-use.com/changelog/3-4-2026) · [BU-30B-A3B](https://browser-use.com/changelog/16-12-2025) · [przejście na CDP](https://browser-use.com/changelog/19-8-2025) · [BU 2.0 — changelog](https://browser-use.com/changelog/27-1-2026) · [wybór agenta](https://docs.browser-use.com/cloud/choosing-an-agent) · [karta BU 2.0](https://docs.browser-use.com/open-source/bu-2-0-model-card) · [raport WebVoyager](https://browser-use.com/posts/sota-technical-report) · [Felicis](https://felicis.com/blog/browser-use-the-tool-making-it-easier-for-ai-agents-to-navigate-websites-raises-17m) · [ain.ua](https://en.ain.ua/2025/03/25/browser-use-raises-17m) · [HAL Online-Mind2Web](https://hal.cs.princeton.edu/online_mind2web) · [OpenAI o prompt injection](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/) · [Gartner](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/) · [koniec Atlasa](https://techcrunch.com/2026/07/09/openai-is-shutting-down-atlas-but-its-ai-browser-ambitions-are-still-growing/) · [udział przeglądarek AI](https://eu.36kr.com/en/p/3931781634260099) · [commity OpenManus](https://api.github.com/repos/FoundationAgents/OpenManus/commits?per_page=5)

---

## 14. Noxtua

**Kategoria:** profesjonalny (prawo, UE) · **Kod:** zamknięty · **Firma:** Noxtua SE (Niemcy, Berlin; dawniej Xayn) ·
**Wynik: 78** (T3 I4 L5 A4)

> Niemiecki asystent prawny w suwerennej chmurze UE, z poziomem „Athena” na otwartych modelach i treściami wydawcy
> C.H.Beck — jedyny w czołówce przykład „UE i prywatność najpierw”, dostępny w Polsce jako Beck-Noxtua.

**Otwarty czy zamknięty.** Platforma zamknięta. Poziom **Athena** działa na modelach open source w suwerennej
infrastrukturze europejskiej; klient może wybrać hosting wyłącznie w chmurze kontrolowanej przez Europejczyków na
otwartych modelach. W IV 2025 firma opisywała też własny model transformerowy trenowany na umowach prawnych
(hostowany w chmurze Northern Data we Frankfurcie). Instalacji na biurku ani w trybie air-gapped nie ma.

**Cel.** Prawnicy, działy prawne, administracja publiczna i sądownictwo w krajach niemieckojęzycznych i w Europie —
ludzie związani ścisłą tajemnicą zawodową, którzy nie chcą (albo nie mogą) wysyłać akt do amerykańskiej chmury.
Ponad 30 000 użytkowników *(dane firmy, IX 2026)*. W Polsce: Beck-Noxtua, sprzedawany przez Wydawnictwo C.H.Beck
na treściach Legalis.

**Funkcje.**
- Research prawny, **Matrix Analysis** (ustrukturyzowana analiza wielu dokumentów), edytor do redakcji i eksportu,
  Projects, Workflows.
- Dodatki do Worda i Outlooka.
- Wyszukiwanie w 210 mln+ dokumentów, w tym 15,8 mln+ orzeczeń, z kuratorowanych treści wydawców *(dane firmy)*.
- „Legal AI Workspaces” dla poszczególnych jurysdykcji, na treściach 8+ europejskich wydawców prawniczych.
- Beck-Noxtua (PL): research na treściach Legalis, analiza dokumentów, projekty pism; „bez limitów tokenów”.
- Praca bez anonimizacji akt — firma twierdzi, że prawnik może pracować „without requiring anonymization”.

**Przewaga.**
- **Treść, której nie ma konkurencja:** C.H.Beck — największy niemiecki wydawca prawniczy — jest większościowym
  udziałowcem; w 2026 dołączył austriacki MANZ. W Polsce dostęp do komentarzy Legalis.
- **Tajemnica zawodowa jako główny argument:** strona bezpieczeństwa wprost odnosi się do § 43e BRAO i § 203 StGB
  (niemieckie przepisy o tajemnicy adwokackiej i karnej odpowiedzialności za jej naruszenie).
- **Krajowe certyfikaty zaufania:** BSI C5, ISO 27001, ISO 42001; polska strona Beck-Noxtua wymienia ISO 9001, 27001,
  27017, 27018 i 42001.
- **Wybór poziomu modelu** zamiast jednej decyzji „chmura tak/nie”.

**Architektura.**
```
użytkownik (web, Word, Outlook)
  └▶ platforma Noxtua — hosting: Niemcy (Deutsche Telekom, IONOS) i Szwajcaria
     ├─ Athena Agent (Standard): modele open source w suwerennej infrastrukturze UE
     └─ Minerva Agent (Frontier): międzynarodowe modele frontier w „europejskim układzie”
           przez T Cloud Public / AI Foundation Services Deutsche Telekom
  └▶ treści wydawców (C.H.Beck, MANZ, …): 210 mln+ dokumentów ──▶ odpowiedź z cytatami
```
- Dane wejściowe i wyjściowe nie służą do trenowania; platforma deklaruje „no persistent access to plaintext data”.
- Opcja self-hostingu: wyłącznie w suwerennej chmurze kontrolowanej przez Europejczyków, na modelach open source.
- Beck-Noxtua w Czechach (8.12.2025): dane przetwarzane w IONOS i Open Telekom Cloud z BSI C5 — „niezależna,
  europejska infrastruktura” oznacza więc chmurę należącą do firm z UE, a nie serwer w kancelarii.

**Na czym zarabia.** Subskrypcje; w Niemczech cennik niepubliczny.
- **Polska: 590 zł netto miesięcznie za użytkownika**, bez limitów tokenów, wymaga subskrypcji Legalis w wariancie
  co najmniej Silver *(strona beck-noxtua.pl, sprawdzone 11.10.2026)*. Cena Legalis nie jest publiczna.
- Finansowanie: seria B 92,2 mln USD (81,2 mln EUR) 22.04.2025, prowadzona przez C.H.Beck, z Northern Data, CMS
  i Dentons *(TechCrunch; komunikat CMS podaje ok. 80,7 mln EUR, 23.04.2025)*. **Seria C ponad 100 mln EUR** od
  C.H.Beck i MANZ (23.09.2026); wycena nieujawniona.
- Ilustracyjny rachunek (ceny katalogowe, netto): 3 prawników × 590 zł × 24 miesiące = **42 480 zł** za dwa lata,
  plus Legalis — to punkt odniesienia dla wyceny pudełka na biurku z abonamentem wsparcia.

**Offline.** **Nie.** Nawet wariant „self-host” to suwerenna chmura UE, nie komputer w kancelarii. Lokalny
odpowiednik potrzebuje: modelu na biurku (np. DeepSeek-V4-Flash), indeksu własnych akt kancelarii, publicznych
źródeł prawa (ISAP/ELI, SAOS) z regularną aktualizacją offline, szyfrowania dysku i wsparcia bez dostępu do danych.
Komentarzy Legalis/LEX lokalnie nie odtworzysz — i nie trzeba (patrz niżej).

**Co przenieść do siebie.**
- **Dwa poziomy, wybór per sprawa.** „Suwerenny” = DeepSeek na desce, domyślny dla każdej sprawy z danymi klienta;
  „frontier” = Opus, włączany świadomie tylko dla treści bez tajemnicy (np. ogólne pytanie o wykładnię), z wpisem
  w dzienniku sprawy. To wprost wzorzec Athena/Minerva, przeniesiony z chmury na biurko.
- **Przepis o tajemnicy na pierwszej stronie produktu:** art. 6 Prawa o adwokaturze, art. 3 ustawy o radcach
  prawnych, a dla adwokatów nowy § 23e Zbioru Zasad Etyki (NRA, 12–13.06.2026: AI tylko pomocniczo, żadnych
  informacji poufnych w narzędziach bez należytej ochrony, osobista weryfikacja, na prośbę klienta — informacja
  o narzędziach). Lokalny asystent może eksportować „notę o użytych narzędziach” per sprawa. To nie jest porada prawna.
- **Uzupełniaj wydawców, nie konkuruj z nimi.** Beck-Noxtua i LEX Expert AI mają komentarze; asystent na desce
  pracuje na tym, czego oni nie widzą: aktach, korespondencji i projektach kancelarii.
- **Zaufanie bez budżetu na BSI C5:** gotowa DPIA, odpowiedzi na listy kontrolne UODO (6.08.2026), jednostronicowe
  mapowanie na § 23e / rekomendacje KIRP, a po wejściu w życie art. 12 ustawy o systemach sztucznej inteligencji
  (3 miesiące od publikacji, art. 127) — indywidualna opinia KRiBSI (30 dni, 60 w sprawach złożonych; brak opinii
  w terminie = opinia zgodna z wnioskiem).
- **Cytat przy każdej tezie** — w PL to już standard rynkowy (LEX Expert AI linkuje fragmenty źródeł), a baza
  Charlotina notuje 6 polskich spraw z halucynacjami AI (10.10.2026).

**Warto wiedzieć.**
- Xayn powstał w 2020 jako startup prywatności i AI działającej na urządzeniu, zanim zmienił branżę na prawo.
  Prezes Leif-Nissen Lundbæk: „you cannot just use an American AI model in a German legal context”.
- Beck-Noxtua ogłoszono dla Polski 3.12.2025 (start planowany na wiosnę 2026); wersja czeska — 8.12.2025.
- Biura: Berlin, Paryż, Sztokholm, Zagrzeb, Monachium, Fryburg.
- Konkurencja w PL: LEX Expert AI (Wolters Kluwer, od 19.11.2025, RAG wyłącznie na treściach LEX, serwery w UE),
  LexisNexis Protégé (demo, bez ceny) i Gaius-Lex — jedyny znaleziony polski gracz z pełnym wdrożeniem on-premise
  (dla kancelarii 20–99 prawników).
- Kapitał suwerennego AI w UE rośnie: Mistral 3 mld EUR przy wycenie ponad 21 mld EUR (IX 2026), Cohere + Aleph Alpha
  przy 20 mld USD (IV 2026).

**Źródła:** [Noxtua](https://www.noxtua.com/) · [Noxtua: bezpieczeństwo](https://www.noxtua.com/security) ·
[seria C](https://www.noxtua.com/news/press-releases/series-c) ·
[TechCrunch: seria B](https://techcrunch.com/2025/04/22/noxtua-raises-92m-for-its-sovereign-ai-tuned-for-the-german-legal-system/) ·
[CMS: C.H.Beck inwestorem](https://cms.law/en/deu/news-information/c.h.beck-becomes-leading-investor-in-legal-ai-noxtua) ·
[Beck-Noxtua: zapowiedź PL](https://www.noxtua.com/news/press-releases/beck-noxtua-poland) ·
[Beck-Noxtua: Czechy](https://www.noxtua.com/news/press-releases/beck-noxtua-for-the-czech-republic) ·
[beck-noxtua.pl](https://www.beck-noxtua.pl/) ·
[NRA: § 23e](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/) ·
[Prawo o adwokaturze (PDF)](https://api.sejm.gov.pl/eli/acts/DU/2024/1564/text.pdf) ·
[ustawa o radcach prawnych (PDF)](https://api.sejm.gov.pl/eli/acts/DU/2024/499/text.pdf) ·
[UODO: listy kontrolne AI](https://uodo.gov.pl/pl/138/4533) ·
[KIRP: rekomendacje AI](https://kirp.pl/rekomendacje-dotyczace-korzystania-z-ai/) ·
[prawo.pl: LEX Expert AI](https://www.prawo.pl/prawnicy-sady/lex-expert-ai-nowym-narzedziem-dla-prawnikow,535918.html) ·
[Gaius-Lex](https://gaius-lex.pl/) · [baza halucynacji](https://www.damiencharlotin.com/hallucinations/) ·
[Mistral: runda](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/) ·
[TechCrunch: Cohere + Aleph Alpha](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/)

---

## 15. Perplexity

**Kategoria:** codzienny + wykonawca · **Kod:** zamknięty (lokalny produkt na otwartych modelach) · **Firma:** Perplexity AI
(USA) · **Wynik: 77** (T4 I4 L4 A3)

> Wyszukiwarka, która odpowiada z przypisami, przeglądarka Comet z agentem i — od 25.08.2026 — **Portable Computer**:
> pierwszy produkt dużego gracza, w którym cały agent (model 27B, harness, piaskownica, narzędzia) działa na biurku
> użytkownika. W czołówce głównie za ten ruch: to najbliższy publiczny wzorzec tego, co sam chcę zbudować.

**Otwarty czy zamknięty.** Aplikacje, Comet i harness są zamknięte. Lokalny Portable Computer uruchamia **otwarte
modele**: Qwen 3.8 27B i dotrenowany przez Perplexity „PPLX 27B" (Nvidia Nemotron 3.5 Lightning zapowiedziany). Otwarty jest
też **BrowseSafe** — klasyfikator prompt injection na bazie Qwen3-30B-A3B wraz z benchmarkiem BrowseSafe-Bench (Hugging
Face, ok. 7.12.2025; licencji prasa nie podaje). Self-hosting: tak dla Portable Computer (na własnym GPU), nie dla reszty.

**Cel.** Dla ludzi, którzy dużo szukają i czytają: odpowiedź z cytatami zamiast listy linków. Na tym Perplexity zbudowała
agenta w przeglądarce (Comet), chmurowego orkiestratora wielu modeli (Computer, plan Max) i — dla tych, którzy nie chcą
wysyłać danych — agenta w pełni lokalnego.

**Funkcje.**
- **Answer engine:** odpowiedzi z cytatami źródeł; działy Discover, Spaces, Shopping, Travel, Finance.
- **Comet** (Chromium): 9.07.2025 tylko Max, 13.08.2025 Pro, od 2.10.2025 darmowy dla wszystkich; Android 20.11.2025,
  iOS 18.03.2026. Asystent w panelu streszcza karty, nawiguje, wypełnia formularze, wysyła maile, kupuje; w Max asystent w
  tle prowadzi kilka zadań naraz z jednego panelu.
- **Perplexity Computer** (27.02.2026, Max): chmurowy orkiestrator, który dzieli zadanie na subagentów i ok. 19 modeli
  (wg Computerworld: Opus 4.6 do rozumowania, Gemini do researchu, Nano Banana i Veo 3.1 do mediów, Grok do lekkich
  zadań, GPT-5.2 do długiego kontekstu).
- **„Personal Computer"** na urządzeniu użytkownika — źródła się rozjeżdżają: natywny agent macOS z dostępem do plików
  (IV 2026, Wikipedia z adnotacją „citation needed" i XDA) oraz wersja na Windows z routingiem ok. 20 modeli (28.07.2026,
  tylko zajawka MSN). Traktuję jako niezweryfikowane.
- **Portable Computer** (25.08.2026): model, harness, silnik inferencji, narzędzia, konektory i piaskownica — wszystko na
  maszynie użytkownika. Linux na start, Windows od IX 2026; wymaga Nvidia DGX Spark albo karty RTX z **≥ 24 GB VRAM**;
  Apple Silicon jeszcze nie.
- **Hybrydowy orkiestrator** (Computex, 2.06.2026): w locie decyduje, co zostaje na urządzeniu; dane finansowe i zdrowotne
  trzyma lokalnie i **pyta o zgodę, zanim wyśle wrażliwe zadanie do chmury**.
- **Samsung Galaxy S26:** wbudowany agent Perplexity ze słowem-kluczem („Hey Plex"), Bixby wzmocniony przez Perplexity
  (wg tytułów i zajawek prasy).

**Przewaga.**
- Szybkie wdrażanie i niezależność od jednego dostawcy modeli: routing per podzadanie.
- **Pierwszy duży gracz z w pełni lokalnym agentem** — i z publicznymi liczbami, ile to kosztuje i ile traci na jakości.
- Comet działa w prawdziwej sesji użytkownika (wszędzie już zalogowany), więc odpada problem logowania w VM.
- Dystrybucja przez producentów i operatorów: Samsung, Airtel.

**Architektura.** Portable Computer według VentureBeat (25.08.2026):
```
 zadanie ─▶ minimalny harness: krótki prompt systemowy, umiejętności (skills) ładowane na żądanie
              │                 └─ hooki samoweryfikacji pilnują „zdrowia" zadania
              ▼
          vLLM: Qwen 3.8 27B / PPLX 27B  (RTX ≥ 24 GB albo DGX Spark)
              ▼
          narzędzia: serwery MCP przepisane na zwięzłe narzędzia CLI (mniej tokenów) — Drive, Gmail, GitHub
              ▼
          obowiązkowa piaskownica systemowa — bez niej harness ODMAWIA startu (fail closed)

 opcja: eskalacja do Claude Opus 5 ─▶ klasyfikator PII filtruje wychodzący kontekst
        ─▶ chmurowy „doradca" zwraca TYLKO tekst; nie dotyka plików ani narzędzi
```
- **Jakość i koszt** (Terminal-Bench 2.1, *dane firmy*): sam Qwen 59,6% przy zerowym koszcie tokenów, z eskalacją 73,0%
  za ok. 0,415 USD za zadanie. Perplexity przyznaje, że małe modele „still trail the frontier meaningfully on hard reasoning".
- **Comet** (wg akt sprawy Amazon v. Perplexity): przeglądarka rozmawia ze stroną, agent robi zrzuty ekranu lokalnie,
  wysyła je na serwery Perplexity i dostaje z powrotem instrukcje nawigacji; serwery nie łączą się ze stroną docelową.
  **Wykonanie lokalne, rozumowanie w chmurze.** Jakie modele napędzają asystenta Comet — nieujawnione.
- **Obrona przed wstrzyknięciami** (BrowseSafe, XII 2025): wszystko, co przychodzi z sieci, jest niezaufane → szybki
  klasyfikator (91% wykrycia w < 0,5 s; dla porównania PromptGuard-2 35%, GPT-5 85%) → przypadki niepewne idą do modelu
  frontier. Ok. 10% ataków i tak przechodzi.
- Ukryte „Agentic Extension" z API MCP mogło uruchamiać lokalne komendy; po krytyce SquareX wyłączono je po cichu
  (ok. 19–20.11.2025).

**Na czym zarabia.**
- **Subskrypcje:** Pro 20 USD/mies. lub 200 USD/rok; Max 200 USD/mies. lub 2000 USD/rok (V 2026); Enterprise Max
  325 USD/mies. Portable Computer jest w cenie Pro, Max, Enterprise Pro i Enterprise Max.
- **Bez reklam** od II 2026 — model „najpierw subskrypcja".
- **Comet Plus:** 5 USD/mies. dla darmowych, w cenie Pro i Max; wydawcy mieli dostawać 80% przychodu z puli 42,5 mln USD
  (niezweryfikowane — tylko wtórny tracker).
- **Przychody:** ARR ok. 450 mln USD w III 2026 i 100 mln+ MAU *(dane firmy wg PYMNTS, 8.04.2026)*; ok. 750 mln USD w VIII
  2026, z poniżej 250 mln na początku roku *(The Information przez Reuters, 23.08.2026; Perplexity nie publikuje liczb,
  nieaudytowane)*. Wzrost przypisywany planowi Max za 200 USD z Computerem.
- **Wycena:** ok. 20 mld USD (IX 2025); ok. 200 mln USD nowego kapitału przy ok. 20 mld (VI 2026, tylko zajawka); Nvidia
  w rozmowach o inwestycji przy wycenie > 30 mld USD *(The Information, 23–24.08.2026)*.
- **Indie:** rok Pro za darmo z Airtel — MAU w szczycie ok. 22 mln (X 2025), ok. 14 mln w VII 2026 po końcu promocji;
  przychód z aplikacji w Indiach ok. 156 tys. USD/mies. *(Appfigures przez TechCrunch)*.
- Umowa chmurowa z Azure: 750 mln USD na 3 lata (I 2026). Udział w rynku aplikacji asystentów: poniżej 5% (V 2026).

**Offline.** **Częściowo — w pełni dla Portable Computer.** Wyszukiwarka, Comet (rozumowanie na serwerach) i Computer to
chmura. Portable Computer działa bez internetu: model 27B, narzędzia i piaskownica lokalnie, eskalacja do chmury jest
opcjonalna (konektory typu Gmail czy Drive oczywiście potrzebują sieci). Haczyk dla mnie: wymaga Nvidii, więc na 4× AMD
Radeon AI PRO R9700 gotowy produkt nie ruszy. Wzorzec za to przenosi się w całości — skoro Perplexity uruchamia model 27B
na 24 GB, karta R9700 z 32 GB pomieści go na jednym slocie.

**Co przenieść do siebie.**
- **Specyfikacja pudełka na biurku potwierdzona przez rynek:** model ~27B + vLLM + 24–32 GB VRAM. Na rigu jedna karta może
  trzymać agenta 27B obok DeepSeek-V4-Flash; Qwen3.8-27B deklaruje przy tym 84,3% na OSWorld-Verified (karta modelu, VIII
  2026, niezweryfikowane niezależnie) — uzupełnienie tekstowego DeepSeeka w zadaniach na ekranie.
- **Fail closed:** nie ma piaskownicy — agent nie startuje
  ([piaskownica](../kurs_lokalne_modele/07-SANDBOX-BEZPIECZENSTWO-MONITORING.md)).
- **Umiejętności ładowane na żądanie i MCP przepisane na zwięzłe CLI.** Przy 13,6 tok/s na slot każdy zbędny token
  w prompcie to realny czas czekania.
- **Eskalacja z filtrem PII, w której chmura tylko doradza tekstem** — Opus 5.5 nie dostaje plików ani narzędzi. To
  kompromis, który można zaproponować klientowi gotowemu na zanonimizowaną pomoc z USA
  ([router hybrydowy](../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md)).
- **Zgoda na każde wyjście do chmury** + stałe kategorie „zawsze lokalnie": zdrowie, finanse, tajemnica zawodowa.
- **Mierz jak Perplexity:** wynik lokalnie vs z eskalacją, plus koszt na zadanie — to są liczby, które przekonają klienta.

**Warto wiedzieć.**
- **Amazon v. Perplexity:** pozew 4.11.2025 (CFAA), nakaz sądu okręgowego w III 2026 (Jones Day datuje go na V 2026);
  4.08.2026 IX Okręg go uchylił — to „użytkownik, nie Perplexity" korzysta z komputerów Amazonu. Amazon wniósł o ponowne
  rozpatrzenie w pełnym składzie 19.08.2026. Logi agenta stały się przy tym sprawą e-discovery.
- **Dziury w Comet:** Brave (ukryty komentarz na Reddicie → wyciek maila i kodu OTP, VIII 2025), Guardio „Scamlexity"
  (zakup w fałszywym sklepie), LayerX „CometJacking" (X 2025, najpierw „Not Applicable"), Zenity „PleaseFix" (zero-click
  przez zaproszenie w kalendarzu → pliki `file://` i 1Password; łatka 23.01.2026, obejście, druga łatka 13.02.2026),
  BragJack (IX 2026). Gartner (8.12.2025) radził firmom na razie blokować AI-przeglądarki.
- **Spory o treści:** Dow Jones / NY Post, Reddit, NYT (wezwanie do zaprzestania), wydawcy japońscy; Cloudflare (VIII 2025)
  zarzucił ukryte crawlery i usunął Perplexity z listy zweryfikowanych botów.
- **Bielik:** przy liście intencyjnym z NVIDIA (VivaTech, VI 2025) zapowiadano dodanie polskiego Bielika do Perplexity
  (money.pl, 11.06.2025); wdrożenia nie potwierdziłem.
- **Kupiony zasięg nie zostaje:** po darmowym roku w Indiach użytkownicy odeszli — ta sama lekcja co subsydia Qwen w Chinach.

**Źródła:** [Portable Computer — VentureBeat](https://venturebeat.com/infrastructure/perplexity-partners-with-nvidia-to-launch-portable-computer-a-fully-local-ai-agent-with-zero-token-costs) ·
[hybryda na Computex](https://venturebeat.com/technology/perplexity-ai-unveils-hybrid-local-cloud-inference-system-at-computex-2026) ·
[Portable Computer na Windows](https://www.techrepublic.com/article/news-perplexity-portable-computer-windows/) ·
[Perplexity Computer — Computerworld](https://www.computerworld.com/article/4138723/perplexitys-new-computer-agent-will-run-other-agents-for-you.html) ·
[Perplexity Computer — TechCrunch](https://techcrunch.com/2026/02/27/perplexitys-new-computer-is-another-bet-that-users-need-many-ai-models/) ·
[Comet za darmo](https://techcrunch.com/2025/10/02/perplexitys-comet-ai-browser-now-free-max-users-get-new-background-assistant/) · [Comet — Wikipedia](https://en.wikipedia.org/wiki/Comet_(browser)) ·
[Perplexity — Wikipedia](https://en.wikipedia.org/wiki/Perplexity_AI) · [BrowseSafe](https://the-decoder.com/perplexitys-browsesafe-tries-to-patch-the-gaping-security-holes-inherent-in-ai-browser-agents/) ·
[ARR 450 mln — PYMNTS](https://www.pymnts.com/news/artificial-intelligence/2026/perplexitys-shift-to-ai-agents-boosts-revenue-50/) ·
[ARR 750 mln i Nvidia](https://finance.yahoo.com/technology/ai/articles/nvidia-discusses-perplexity-investment-30-031804276.html) · [Nvidia przy 30 mld](https://thenextweb.com/news/nvidia-perplexity-30bn-valuation-talks) ·
[Indie](https://techcrunch.com/2026/08/18/perplexitys-free-ai-offer-left-it-with-millions-more-users-in-india/) · [Comet Plus](https://www.vice.com/en/article/perplexity-comet-plus-announced/) ·
[IX Okręg — Jones Day](https://www.jonesday.com/en/insights/2026/09/ninth-circuit-vacates-cfaa-injunction-against-perplexitys-comet-ai-agent) · [Brave](https://brave.com/blog/comet-prompt-injection/) ·
[CometJacking](https://layerxsecurity.com/blog/cometjacking-how-one-click-can-turn-perplexitys-comet-ai-browser-against-you/) ·
[PleaseFix — The Register](https://www.theregister.com/2026/03/03/perplexity_comet_browser_hole_cal_invite/) · [MCP API — Help Net Security](https://www.helpnetsecurity.com/2025/11/20/perplexity-comet-browser-security-mcp-api/) ·
[Gartner](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/) · [Hey Plex](https://www.androidauthority.com/hey-perplexity-3655439/) ·
[Bielik i NVIDIA](https://www.money.pl/gospodarka/wielki-krok-dla-polskiego-ai-bielik-rozpoczyna-wspolprace-z-nvidia-7166523596470944a.html) ·
[R9700 — AMD](https://www.amd.com/en/products/graphics/workstations/radeon-ai-pro/ai-9000-series/amd-radeon-ai-pro-r9700.html) · [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)

---

## Warto znać — kto nie zmieścił się w piętnastce

Piętnastka ma po jednym reprezentancie na wzorzec, więc wiele dobrych pomysłów zostało poza nią: duplikaty kategorii,
produkty niedostępne w Polsce, świetne silniki bez własnego asystenta. **Poniżej to, co z nich warto podpatrzeć** — każdy
wiersz z jedną liczbą i datą, jeśli research ją potwierdził. Gwiazdki z API GitHuba z 11 października 2026.

### Następni w rankingu (wynik 58–76)

| Nazwa (wynik) | Kategoria | Kod | Dlaczego warto znać | Źródło |
|---|---|---|---|---|
| UI-TARS / UI-TARS-desktop (76) | wykonawca GUI | otwarty, Apache-2.0, ⭐ <!-- gh:bytedance/UI-TARS-desktop -->39,2k | Jedyny agent GUI dużego laboratorium z otwartymi wagami i gotową aplikacją; UI-TARS-1.5-7B ma 27,5% na OSWorld (IV 2025) i działa lokalnie przez vLLM lub Ollamę. Wzorzec: jeden interfejs dla 4 operatorów (lokalny komputer, lokalna przeglądarka, zdalna VM, zdalna przeglądarka). | [model](https://huggingface.co/ByteDance-Seed/UI-TARS-1.5-7B) · [repo](https://github.com/bytedance/UI-TARS-desktop) |
| Legora (74) | profesjonalny, prawo (Szwecja) | zamknięty | Europejski rywal [Harveya](01-PROFILE.md#4-harvey): ARR 100 mln USD w IV 2026, ponad 200 mln USD w IX 2026 *(wg założyciela, Bloomberg przez prasę wtórną)*; hosting w UE od pierwszego dnia i siatka „dokumenty × pytania" jako główny interfejs. | [TNW](https://thenextweb.com/news/legora-just-hit-100-million-in-revenue-it-took-18-months) |
| Heidi Health (74) | profesjonalny, medycyna (Australia, UK/UE) | zamknięty | ARR od 1 do 50 mln USD w ok. 24 miesiące (IV 2026), 340 mln USD finansowania (IX 2026); darmowa, nielimitowana transkrypcja, audio nigdy nie jest zapisywane, dane z UE zostają w UE. Agentów wypuściła z pominięciem UK i UE — przez regulacje. | [HLTH](https://hlth.com/insights/news/heidi-raises-340m-to-expand-clinical-ai-into-supervised-agentic-workflows) |
| Microsoft 365 Copilot (74) | profesjonalny, biuro | zamknięty | Kotwica cenowa w polskich firmach: 18–32 USD za użytkownika miesięcznie, ponad 30 mln płatnych stanowisk (VII 2026, *dane firmy*). Uczy też ostrożności: modele Anthropic są wyłączone z EU Data Boundary. | [dokumentacja](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) · [wyniki](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast) |
| Genspark (72) | wykonawca | zamknięty | Ok. 250 mln USD ARR w połowie 2026 *(dane firmy)* i wycena 2,6 mld USD (17.06.2026); „mixture of agents" po 30+ modelach, rozmowy telefoniczne za stałe 500 kredytów, Claw z trybem lokalnym ograniczonym do jednego folderu. Duplikat [Manusa](01-PROFILE.md#6-manus). | [Yahoo Finance](https://finance.yahoo.com/technology/ai/articles/genspark-ai-extends-series-b-131000248.html) |
| Poke (72) | codzienny, przez SMS/iMessage | zamknięty | Ponad 100 mln wiadomości w 3 miesiące, pierwszy agent zatwierdzony w Apple Messages for Business (4.06.2026), przejęty przez Cognition 23.07.2026. Interfejsem jest zwykła aplikacja do wiadomości, a automatyzacje to udostępniane tekstowe „przepisy". | [Cognition](https://cognition.com/blog/interaction) |
| NVIDIA NemoClaw (71, z Ghostem) | żyjący, lokalny | otwarty, Apache-2.0, ⭐ <!-- gh:NVIDIA/NemoClaw -->22,7k | Jedna komenda instaluje [OpenClaw](01-PROFILE.md#1-openclaw) w piaskownicy OpenShell z lokalnymi modelami Nemotron i zgodą operatora na ruch wychodzący. Prawdopodobnie najszybsza droga do pilotażu w kancelarii; status „alpha". | [repo](https://github.com/NVIDIA/NemoClaw) |
| Ghost (71, z NemoClaw) | żyjący, sprzęt | licencja nieznana | Pudełko za 3499 USD (przedsprzedaż od 5.10.2026) z RTX Pro 4000, preinstalowanymi Qwen-3.8-27B i Gemma-4-31B oraz zaporą wyjściową, która ma blokować eksfiltrację; 11 mln USD od a16z. Niemal dokładnie mój docelowy format — tylko USA. | [TechCrunch](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/) |
| Nabla (70) | profesjonalny, medycyna (Francja) | zamknięty | W RCT UCLA (NEJM AI, XII 2025) skróciła czas pisania notatek o 9,5% (p=0,02), a Dragon nie dał istotnej różnicy. ASR na bazie Whispera dotrenowany na 7000 h audio medycznego; audio nie jest przechowywane. | [PubMed](https://pubmed.ncbi.nlm.nih.gov/41497288/) · [Nabla](https://nabla.com/blog/assessing-the-reliability-of-nablas-speech-to-text-engine) |
| Basis (70) | profesjonalny, księgowość i podatki (USA) | zamknięty | „Behavior specs" (29.07.2026): otwarty standard oceny **przebiegu** pracy agenta, nie tylko wyniku — specyfikacji agent nigdy nie widzi. Series B 100 mln USD przy wycenie 1,15 mld USD (24.02.2026). | [specyfikacje](https://www.getbasis.ai/blogs/behavior-specs-an-open-standard-for-supervising-long-horizon-agents) |
| Hebbia (70) | profesjonalny, finanse | zamknięty | Wymyśliła interfejs „Matrix" (te same pytania × setki dokumentów, z cytatem w każdej komórce), który potem skopiowały Legora i CoCounsel; każda komórka to małe, równoległe zadanie — idealne dla 4 lokalnych slotów. 130 mln USD przy 700 mln wyceny (VII 2024). | [Matrix 2.0](https://www.hebbia.com/blog/introducing-matrix-2-0) |
| Glean (67) | profesjonalny, wiedza firmowa | zamknięty | ARR 300 mln USD (28.05.2026). Tau: 0,58 USD za zadanie wobec 2,98 USD w Claude Cowork *(benchmark firmy)* dzięki wcześniej zaindeksowanemu kontekstowi z uprawnieniami — argument, że indeks oszczędza tokeny małemu modelowi. | [TechCrunch](https://techcrunch.com/2026/05/28/gleans-top-line-crosses-300m-as-ai-budget-cutting-becomes-its-major-selling-point/) · [ITBrief](https://itbrief.asia/story/glean-launches-tau-to-cut-enterprise-ai-token-costs) |
| Lindy (65) | żyjący → zespołowy | zamknięty | Reguła „wszystko z efektem na zewnątrz czeka na zatwierdzenie, odczyt nie"; 49,99 USD za użytkownika za 5000 kredytów. Apple zbanowało ich Apple ID na iMessage w pół dnia (III 2026) — kanały konsumenckie są wrogie. | [cennik](https://www.lindy.ai/pricing) · [iMessage](https://www.lindy.ai/blog/imessage-api-three-rewrites-one-apple-ban-and-what-actually-works) |
| Gaius-Lex (58) | profesjonalny, prawo (PL) | zamknięty | Najbliższy polski odpowiednik „dane nie wychodzą z kancelarii": Gaius Vault jako SaaS w EOG, hybryda albo pełne on-premise, dla firm 20–99 prawników. Seed ok. 502 tys. USD (1.08.2025, *agregator*), 6 osób. | [gaius-lex.pl](https://gaius-lex.pl/) · [Signalbase](https://www.trysignalbase.com/news/funding/gaius-lex-secures-5) |

### Asystenci codzienni

| Nazwa | Kategoria | Kod | Dlaczego warto znać | Źródło |
|---|---|---|---|---|
| Meta AI + Muse | codzienny + żyjący | zamknięty | Muse (8.09.2026): osobna VM na użytkownika i agent „Sentinel", który zatwierdza **każdą** akcję wychodzącą do internetu; płatności jednorazowymi kartami Stripe, hasła w 1Password. 5 mln pobrań w 22 dni, ale tylko ok. 700 tys. DAU — retencja. Tylko USA i Kanada. | [Meta](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) · [retencja](https://cryptobriefing.com/meta-muse-app-store-retention/) |
| Muse Glimmer | model lokalny | otwarte wagi, Apache 2.0 | Ok. 29,6 mld parametrów (dense), 131k kontekstu, 100+ języków, w 4 bitach mieści się na karcie 24 GB (10.08.2026); strojony pod lokalnych agentów. Jakość po polsku niezweryfikowana. | [VentureBeat](https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now) |
| Amazon Alexa+ | codzienny, dom | zamknięty | „Experts" — paczki narzędzi per dziedzina zamiast jednej długiej listy, co pomaga małym modelom w wyborze narzędzia. W USA 19,99 USD lub za darmo z Prime; **w Polsce niedostępna**; od 28.03.2025 cały głos idzie do chmury. | [Amazon](https://www.aboutamazon.com/news/devices/new-alexa-generative-artificial-intelligence) · [kraje](https://www.aboutamazon.com/news/devices/alexa-plus-international-launch) |
| Apple Siri AI | codzienny, system | zamknięty | iOS 27 (14.09.2026) z listą oczekujących; model ok. 3 mld parametrów na urządzeniu (2-bitowe QAT) + Private Cloud Compute, zbudowane z Google Gemini. Nie ma go na iPhone'ach w UE (DMA), a Apple Intelligence nie obsługuje polskiego. | [TNW](https://thenextweb.com/news/apple-ios-27-siri-ai-release-icloud-plus-child-safety) · [języki](https://support.apple.com/en-us/121115) |
| Microsoft Copilot (konsumencki) | codzienny | zamknięty | Antywzorzec: awatar Mico, czaty grupowe i podcasty usunięte 18.08.2026 przy ok. 38,5 mln użytkowników miesięcznie. Za to Agent Workspace w Windows (agent jako osobne konto z „zawsze / pytaj / nigdy" per folder) warto skopiować. | [TNW](https://thenextweb.com/news/microsoft-copilot-mico-retired-features-killed-app-merge) · [Windows](https://support.microsoft.com/en-us/windows/experimental-agentic-features-a25ede8a-e4c2-4841-85a8-44839191dfb3) |
| Grok | codzienny | zamknięty (stare wagi otwarte) | Głównie lekcje negatywne: kryzys deepfake'ów (XII 2025 – I 2026), łatanie promptu systemowego na produkcji, wycieki czatów przez indeksowane linki. Grok Bot miał 418 tys. użytkowników 14.09.2026. | [Wikipedia](https://en.wikipedia.org/wiki/Grok_(chatbot)) · [Finbold](https://finbold.com/spacexais-grok-bot-agent-surpasses-400000-users-after-the-first-month/) |
| Doubao (ByteDance) | codzienny, Chiny | zamknięty | Ponad 200 mln DAU (IX 2026, LatePost przez TechNode); umiejętności uczone z nagrania ekranu i przekazanie zadania z telefonu na PC. Od 15.07.2026 chińskie przepisy zamknęły agentów tworzonych przez użytkowników. | [TechNode](https://technode.com/2026/09/23/bytedance-doubao-general-session-team-cuts/) |
| Qwen app (Alibaba) | codzienny, Chiny | aplikacja zamknięta, modele otwarte | Kampania za ok. 6 mld RMB dała skok DAU, ale sesja trwa ok. 1,3 min — kupieni użytkownicy nie zostają. 167 mln MAU (V–VI 2026). Ważniejszy jest model: Qwen 3.8 27B napędza lokalny Portable Computer [Perplexity](01-PROFILE.md#15-perplexity). | [TechTimes](https://www.techtimes.com/articles/323907/20260811/qwen-sells-paid-office-subscriptions-users-it-bought-with-free-bubble-tea.htm) |
| DeepSeek app | codzienny | aplikacja zamknięta, wagi MIT | 130 mln MAU (V 2026). Aplikacja jest słaba agentowo, ale wagi V4-Flash na MIT to silnik mojego rigu. Berliński urząd ochrony danych zażądał usunięcia aplikacji ze sklepów w Niemczech (27.06.2025) — liczy się, gdzie przetwarzane są dane. | [Hugging Face](https://huggingface.co/api/models?author=deepseek-ai&sort=lastModified) · [netzpolitik](https://netzpolitik.org/2025/datenschutzbehoerde-greift-ein-deepseek-fliegt-aus-den-app-stores/) |
| Mistral Vibe (dawniej Le Chat) | codzienny + firmowy (UE) | aplikacja zamknięta, wiele modeli otwartych | Dowód, że „suwerenne AI" to płacący rynek: 3 mld EUR przy wycenie ponad 21 mld EUR (8.09.2026), Pro za 14,99 USD, on-premise dla firm, 100+ konektorów z pełnym MCP. | [TechCrunch](https://techcrunch.com/2026/09/08/mistral-raises-e3b-as-sovereign-ai-becomes-big-business/) · [cennik](https://mistral.ai/pricing) |
| Instinct | codzienny, przez iMessage | zamknięty | Konsjerż w iMessage: dzwoni do firm, ma własne adresy e-mail, używa tymczasowych poświadczeń i izolowanych piaskownic. Seria C 1 mld USD przy wycenie 10 mld USD (28.09.2026). | [Pulse 2.0](https://pulse2.com/instinct-raises-1-billion-series-c-at-10-billion-valuation/) |

### Wykonawcy, przeglądarki i otwarte szkielety

| Nazwa | Kategoria | Kod | Dlaczego warto znać | Źródło |
|---|---|---|---|---|
| NanoClaw | żyjący | otwarty, MIT, ⭐ <!-- gh:nanocoai/nanoclaw -->30,9k | Minimalistyczna alternatywa OpenClaw: kontener na grupę agentów, „bramki skryptowe" przed każdym zaplanowanym wybudzeniem (model nie wstaje, gdy nie ma pracy), brama poświadczeń. Zbudowany na Claude Agent SDK; Ollama opcjonalnie. | [repo](https://github.com/nanocoai/nanoclaw) |
| OpenManus | wykonawca | otwarty, MIT, ok. 58,6k gwiazdek | Sklonowany z Manusa w 3 godziny (6.03.2025) — dowód, że wartość leży w infrastrukturze, nie w pętli. Mały, czytelny szkielet: Ollama + piaskownica Docker + lokalny Chrome + MCP. | [repo](https://github.com/FoundationAgents/OpenManus) |
| Suna / Kortix | wykonawca + zespołowy | source-available, Elastic License 2.0, ok. 20,3k gwiazdek | Piaskownica i gałąź git na sesję (rollback i audyt), broker poświadczeń — sekrety nigdy nie wchodzą do maszyny agenta. Licencja zmieniła się z Apache 2.0 na ELv2 — sprawdzaj licencję przed forkiem. | [README](https://raw.githubusercontent.com/kortix-ai/suna/main/README.md) |
| Agent S3 / Sai (Simular) | wykonawca GUI | Agent S otwarty (Apache-2.0), Sai zamknięty | S3 z Best-of-N osiągnął 72,6% na OSWorld wobec 72,36% ludzi (X 2025). Na długich zadaniach OSWorld 2.0 Sai kończy w pełni tylko 28,25% zadań, za 15,70 USD każde (28.08.2026) — realna skala problemu. | [repo](https://github.com/simular-ai/Agent-S) · [Simular](https://www.simular.ai/articles/sai-tops-osworld-2-0) |
| Microsoft Fara-7B + MagenticLite | wykonawca na urządzeniu | otwarty, MIT | Model computer use 7B (z Qwen2.5-VL) trenowany na 145 tys. syntetycznych trajektorii: WebVoyager 73,5%, ok. 16 kroków na zadanie wobec ok. 41 (XI 2025, *dane firmy*). Destylacja dużego agenta do małego modelu. | [MSR](https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/) |
| Open-AutoGLM (Z.ai) | wykonawca na telefonie | otwarty, Apache-2.0; model MIT | AutoGLM-Phone-9B steruje Androidem przez ADB i wymaga GPU 24 GB+; wersja chmurowa kosztowała ok. 0,2 USD za zadanie (VIII 2025). Telefon lub VM jako piaskownica zamiast prawdziwego pulpitu. | [repo](https://github.com/zai-org/Open-AutoGLM) |
| Skywork Desktop | wykonawca biurowy | zamknięty (części otwarte) | Pracuje na wskazanych folderach w lokalnej izolowanej VM, oddaje gotowe dokumenty, slajdy i arkusze; „AI tool business" Kunlun ma ponad 100 mln USD ARR (II kw. 2026). Modele w chmurze. | [Skywork](https://skywork.ai/desktop/en/index.html) · [36Kr](https://eu.36kr.com/en/p/3878113666724100) |
| Opera Neon | przeglądarka agentowa | zamknięty | Firma z Norwegii (EOG). Agent czyta DOM zamiast zrzutów ekranu; od 14.08.2026 darmowy plan dla zewnętrznych agentów przez MCP i Opera Browser CLI — lokalny agent może sterować prawdziwą przeglądarką. Neon za 19,90 USD/mies. Notatka w researchu wskazuje rozwój przeglądarki desktopowej w Polsce — bez źródła, niezweryfikowane. | [Opera](https://blogs.opera.com/news/2026/08/your-ai-agents-can-use-opera-neon-free-of-charge/) · [MCP](https://press.opera.com/2026/03/31/opera-neon-adds-mcp-connector/) |
| Fellou + Eko | przeglądarka agentowa | przeglądarka zamknięta, Eko MIT (ok. 4,96k gwiazdek) | Plan widoczny i edytowalny przed wykonaniem, koszt w kredytach pokazany przed startem (ok. 250 kredytów, czyli 2–2,4 USD na złożone zadanie, X 2026). Brave wykazało, że treść strony trafiała do modelu automatycznie. Brak nowości w 2026. | [cennik](https://fellou.ai/pricing) · [Eko](https://github.com/FellouAI/eko) |
| Amazon Nova Act | wykonawca firmowy | zamknięty | Rozliczenie 4,75 USD za godzinę pracy agenta, a czas czekania na człowieka jest darmowy; workflow łączy deterministyczny kod Pythona z krokami `act()` w języku naturalnym. | [cennik](https://aws.amazon.com/nova/pricing/) · [AWS](https://aws.amazon.com/blogs/aws/build-reliable-ai-agents-for-ui-workflow-automation-with-amazon-nova-act-now-generally-available/) |

### Profesjonalni: prawo, medycyna, programiści, obsługa klienta

| Nazwa | Kategoria | Kod | Dlaczego warto znać | Źródło |
|---|---|---|---|---|
| Thomson Reuters CoCounsel | prawo | zamknięty | 1 mln użytkowników w 107 krajach (24.02.2026, *dane firmy*). Nowa generacja przebudowana na Claude Agent SDK (VI 2026), obok własny model „Thomson" do zadań tabelarycznych; połączenie MCP z Claude. Hybryda: mały model domenowy + duży ogólny. | [LawNext](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html) · [BNN](https://www.bnnbloomberg.ca/business/2026/02/24/thomson-reuters-says-one-million-professionals-using-cocounsel-shares-soar/) |
| Lexis+ AI z Protégé | prawo | zamknięty | Rozdziela tryb „ogólny" od „prawnego z cytatami" (Shepard's), a administrator kancelarii może wyłączyć ogólny; produkty AI to 90% nowego biznesu (23.07.2026). Ma polską stronę Protégé z demem, bez ceny. | [LexisNexis](https://www.lexisnexis.com/community/pressroom/b/news/posts/legal-ai-propels-lexisnexis-to-fastest-growth-in-history) · [PL](https://www.lexisnexis.com/de-at/cee/protege-polska) |
| Microsoft Dragon Copilot | medycyna | zamknięty | Dyktowanie + nasłuch wizyty w jednym narzędziu, sprzedawany w DE, FR i NL; „na drodze do ponad 100 mln wizyt" w 2026 (Nadella, VII 2026). W RCT UCLA nie skrócił istotnie czasu notatek (−1,7%), ale poprawił samopoczucie lekarzy. | [Microsoft](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4) · [premiera](https://news.microsoft.com/source/2025/03/03/microsoft-dragon-copilot-provides-the-healthcare-industrys-first-unified-voice-ai-assistant-that-enables-clinicians-to-streamline-clinical-documentation-surface-information-and-automate-task/) · [PubMed](https://pubmed.ncbi.nlm.nih.gov/41497288/) |
| Doximity GPT, ChatGPT for Clinicians | medycyna, wiedza kliniczna | zamknięte | Konkurenci [OpenEvidence](01-PROFILE.md#12-openevidence): Doximity zrzesza ponad 80% lekarzy w USA (2021) i daje AI za darmo, finansując się marketingiem farmaceutycznym; OpenAI weszło z ChatGPT for Clinicians w IV 2026 (wg Sacra). | [Wikipedia](https://en.wikipedia.org/wiki/Doximity) · [Sacra](https://sacra.com/c/openevidence/) |
| Devin / Devin Desktop (Cognition) | programiści | zamknięty | Run-rate 1 mld USD przekroczony 25.09.2026, wycena 48 mld USD (8.09.2026); łączy IDE (dawny Windsurf) z agentem, któremu oddaje się całe zadania, i kupiło Poke. Dopełnienie [Cursora](01-PROFILE.md#9-cursor). | [Cognition](https://cognition.com/blog/1b-run-rate) |
| Lovable | programiści i nieprogramiści (Szwecja) | zamknięty | Europejska firma, która wygrywa globalnie: ARR na drodze do ok. 600 mln USD (VIII 2026), wycena 13,3 mld USD. Ostrzeżenie: źle ustawione reguły dostępu w Supabase w wygenerowanych aplikacjach ujawniały dane (III 2025). | [VKTR](https://www.vktr.com/ai-platforms/lovable-raises-400-million-at-133-billion-valuation/) · [Wikipedia](https://en.wikipedia.org/wiki/Lovable_(company)) |
| Decagon | obsługa klienta | zamknięty | „Agent Operating Procedures": procedury pisane językiem naturalnym przez zespół obsługi, bez sprintów programistycznych — u mnie „gdy klient przyśle wezwanie, najpierw sprawdź termin…". Wycena 4,5 mld USD (27.01.2026). | [Decagon](https://decagon.ai/blog/series-d-announcement) |
| Produkty na Claude Agent SDK | wzorzec | SDK zamknięte, produkty różne | CoCounsel (prawo) i NanoClaw (żyjący agent) stoją na harnessie laboratorium zamiast na własnym — szybka droga do produktu wertykalnego. Zob. [Claude](01-PROFILE.md#2-claude). | [LawNext](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html) · [NanoClaw](https://github.com/nanocoai/nanoclaw) |

### Dlaczego nie w czołówce

- **Duplikat kategorii.** Na każdy wzorzec bierzemy jednego najlepszego: Legora i Gaius-Lex przegrywają z Harveyem i Noxtuą,
  Heidi, Nabla i Dragon z Abridge, Genspark z Manusem, UI-TARS, Agent S i Fara z browser-use, NemoClaw i NanoClaw z
  OpenClaw.
- **Niedostępne w Polsce.** Muse (USA i Kanada), Alexa+ (brak Polski na liście krajów), Siri AI (nie na iPhone'ach w UE,
  bez polskiego), Ghost (USA). Uczą wzorców, ale czytelnik ich nie przetestuje.
- **Brak danych o architekturze.** Instinct, Grok, Doubao, aplikacja Qwen, Hebbia i Decagon publikują niewiele o tym, jak są
  zbudowane — dla tego przeglądu to główna wartość.
- **Brak trakcji albo za wcześnie.** Gaius-Lex (ok. 502 tys. USD seedu, 6 osób), Ghost (przedsprzedaż od 5.10.2026),
  Fellou (brak nowości w 2026), NemoClaw (status „alpha").
- **Silniki, nie asystenci.** DeepSeek, Muse Glimmer, Qwen i Gemma to modele — wracają w
  [03-WZORCE-TECHNICZNE.md](03-WZORCE-TECHNICZNE.md) i [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md).
- **Lekcje głównie negatywne.** Konsumencki Microsoft Copilot (osobowość nie sprzedała produktu) i Grok (bezpieczeństwo
  jako dodatek) to przestrogi, nie wzorce.
