# Źródła — na czym stoi ten przegląd

**Sprawdzone 11 października 2026.** Przy każdej pozycji: co z niej wziąłem. Źródła pierwotne (strony produktów,
cenniki, dokumentacja, ogłoszenia firm, akty prawne) mają pierwszeństwo; dane podawane przez same firmy i szacunki prasy
oznaczam w tekście. Każdy profil w [01-PROFILE.md](01-PROFILE.md) ma też własne linki źródłowe.

## Liczby z GitHuba

- **API GitHuba** — `GET /repos/{właściciel}/{repo}` i `GET /repos/{…}/releases/latest`, wywołane 11.10.2026:
  openclaw/openclaw, NousResearch/hermes-agent, browser-use/browser-use, NVIDIA/NemoClaw, nanocoai/nanoclaw,
  bytedance/UI-TARS-desktop, cline/cline, nextcloud/assistant → gwiazdki, licencje, wydania.

## Profile 1, 2, 5, 6, 13

| Źródło | Co wziąłem |
|---|---|
| [OpenClaw — GitHub](https://github.com/openclaw/openclaw) | licencja MIT, gwiazdki, wydania, porady bezpieczeństwa 2026 (API GitHuba, 11.10.2026) |
| [OpenClaw — wprowadzenie](https://openclaw.ai/blog/introducing-openclaw) | zmiana nazwy na OpenClaw, >100 tys. gwiazdek i 2 mln odwiedzin w tydzień, finansowanie opiekunów |
| [OpenClaw Foundation](https://openclaw.ai/blog/introducing-openclaw-foundation) | fundacja 501(c)(3) z 8.07.2026, darczyńcy i partnerzy, ClawCon, „4.5 million new claws", NemoClaw |
| [OpenClaw Enterprise](https://openclaw.ai/blog/openclaw-enterprise) | dystrybucja firmowa z 29.09.2026, „will always be free", IT domyślnie zakazuje agentów |
| [Microsoft Autopilot na OpenClaw](https://openclaw.ai/blog/microsoft-autopilot-openclaw) | Autopilot z 25.09.2026, prywatny podgląd, poprawki upstream (Policy plugin, Teams, Windows) |
| [OpenClaw — bezpieczeństwo jawnie](https://openclaw.ai/blog/openclaw-security-in-public) | statystyka zgłoszeń Steinbergera, przeniesienie kanałów i dostawców do wtyczek |
| [OpenClaw — trudny tydzień](https://openclaw.ai/blog/openclaw-rough-week) | zepsute wydania IV 2026, „too founder-driven" |
| [OpenClaw — VirusTotal](https://openclaw.ai/blog/virustotal-partnership) | skanowanie umiejętności od 7.02.2026 |
| [OpenClaw — NVIDIA SkillSpector](https://openclaw.ai/blog/openclaw-nvidia-skill-security) | SkillSpector i Skill Cards (1.06.2026) |
| [OpenClaw — ClawScan](https://openclaw.ai/blog/tencent-aig-joins-clawscan) | Tencent AI-Infra-Guard, 98,6% wykrytych złośliwych umiejętności na 556 przypadkach |
| [OpenClaw docs — heartbeat](https://docs.openclaw.ai/gateway/heartbeat) | interwał 30 min / 1 h, limity wybudzeń |
| [OpenClaw docs — standing orders](https://docs.openclaw.ai/automation/standing-orders) | zakres, wyzwalacz, bramka, eskalacja; pliki wstrzykiwane w sesję |
| [OpenClaw docs — dreaming](https://docs.openclaw.ai/concepts/dreaming) | fazy konsolidacji pamięci, DREAMS.md, wagi 1–10 |
| [OpenClaw docs — workspace](https://docs.openclaw.ai/concepts/agent-workspace) | workspace to nie twarda piaskownica |
| [OpenClaw docs — modele lokalne](https://docs.openclaw.ai/gateway/local-models) | llama.cpp, Ollama, vLLM, ds4; ≥8 GiB i 64K; brak filtrów bezpieczeństwa lokalnie |
| [OpenClaw docs — Ollama](https://docs.openclaw.ai/providers/ollama) | natywne /api/chat, /v1 psuje wywołania narzędzi |
| [OpenClaw docs — security](https://docs.openclaw.ai/gateway/security) | kody parowania, listy dozwolonych, security audit |
| [TechCrunch: Steinberger w OpenAI](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/) | przejście do OpenAI 14–15.02.2026, zapowiedź fundacji |
| [The Register o OpenClaw 2.0](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) | nowości 2.0, sekrety bez szyfrowania, piaskownica domyślnie wyłączona, incydent z siłownią |
| [Cloudflare — Moltworker](https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/) | hosting na Workers, „flood of people buying Mac minis" |
| [Cisco o OpenClaw](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare) | eksfiltracja przez umiejętność, 26% z 31 tys. umiejętności z podatnością |
| [InsiderLLM — audyty ClawHub](https://insiderllm.com/guides/openclaw-clawhub-security-alert/) | liczby złośliwych umiejętności (źródło wtórne) |
| [Wiz — Moltbook](https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys) | odsłonięte tokeny API i e-maile |
| [Wikipedia — OpenClaw](https://en.wikipedia.org/wiki/OpenClaw) | historia nazw, MoltMatch, ograniczenia w Chinach, Nadella, 247 tys. gwiazdek w III 2026 |
| [Wikipedia — Moltbook](https://en.wikipedia.org/wiki/Moltbook) | start 28.01.2026, przejęcie przez Metę |
| [Anthropic — seria G](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation) | 30 mld USD przy 380 mld USD, run-rate 14 mld USD, Claude Code >2,5 mld USD, 4% commitów |
| [Claude — pamięć](https://claude.com/resources/articles/claudes-memory-works-everywhere-and-you-decide-whats-in-it) | pamięć w plikach tematycznych, tematy wrażliwe domyślnie poza pamięcią (25.08.2026) |
| [Claude — Cowork to Claude](https://claude.com/resources/articles/cowork-is-now-claude) | scalenie z czatem 16.09.2026, harmonogram, pytanie przed działaniem |
| [Claude — jak ludzie używają Cowork](https://claude.com/resources/articles/how-people-are-using-claude-cowork) | 1,2 mln sesji, podział kategorii zadań |
| [Claude — Dispatch i computer use](https://claude.com/resources/articles/dispatch-and-computer-use) | Dispatch z computer use od 23.03.2026 |
| [Claude — Routines](https://claude.com/resources/articles/introducing-routines-in-claude-code) | Routines w Claude Code (14.04.2026) |
| [Claude — Cowork research preview](https://claude.com/blog/cowork-research-preview) | ceny planów, foldery, osobna przeglądarka, zatwierdzenia |
| [Claude — pomoc Cowork](https://support.claude.com/en/articles/13345190-getting-started-with-cowork) | wykonanie w chmurze Anthropic, zakres uprawnień ruchu wychodzącego |
| [Simon Willison o Cowork](https://simonwillison.net/2026/Jan/12/claude-cowork/) | lokalna VM Apple Virtualization w I 2026 |
| [Docs — computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) | toolset GA, 17 narzędzi, akcje wsadowe, koszt zrzutów, zalecenia |
| [Docs — browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) | 31 narzędzi, drzewo dostępności, wykonanie po stronie dewelopera |
| [Demo computer use](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) | otwarty kontener referencyjny |
| [Claude for Chrome](https://claude.com/blog/claude-for-chrome) | zabezpieczenia, 23,6% → 11,2%, harmonogram dostępności |
| [Claude in Chrome](https://claude.com/chrome) | funkcje 2026, GA na płatnych planach, odradzane zastosowania |
| [Anthropic — obrona przed prompt injection](https://www.anthropic.com/research/prompt-injection-defenses) | ok. 1% dla Opus 4.5 przy adaptacyjnym atakującym |
| [Anthropic — computer use 2024](https://www.anthropic.com/news/3-5-models-and-computer-use) | start 22.10.2024, 14,9% OSWorld |
| [Anthropic — Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5) | 61,4% OSWorld |
| [Anthropic — Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6) | ceny 3 / 15 USD |
| [Anthropic — Opus 5.5](https://www.anthropic.com/news/claude-opus-5-5) | 81,8% OSWorld 2.1, ceny 4 / 20 USD (22.09.2026) |
| [Anthropic — Vercept](https://www.anthropic.com/news/acquires-vercept) | przejęcie 25.02.2026, 72,5% OSWorld |
| [Claude Code — dane](https://code.claude.com/docs/en/data-usage) | dostawcy modeli, retencja, przełącznik zbędnego ruchu, VM w chmurze |
| [TechCrunch — limity Claude Code](https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/) | limity tygodniowe od 28.08.2025, <5% subskrybentów |
| [Stack Overflow 2026](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/) | Claude Code — 66% użytkowników agentów kodujących |
| [iTiger — SemiAnalysis](https://www.itiger.com/hans/news/1183910360) | szacunek ok. 44 mld USD run-rate w V 2026 (wtórne) |
| [TechCrunch — Claude for Legal](https://techcrunch.com/2026/05/12/the-ai-legal-services-industry-is-heating-up-anthropic-is-getting-in-on-the-action/) | wtyczki i konektory MCP do Westlaw, Box, Docusign (12.05.2026) |
| [LawNext — CoCounsel na Agent SDK](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html) | nowy CoCounsel zbudowany na Claude Agent SDK |
| [Microsoft — prywatność Copilota](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) | modele Anthropic poza EU Data Boundary (stan 8.10.2026) |
| [PromptArmor — Cowork](https://www.promptarmor.com/resources/claude-cowork-exfiltrates-files) | eksfiltracja plików przez dozwolone API |
| [BleepingComputer — BragJack](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/) | atak przez rozszerzenia, CVE-2026-0628, m.in. Claude in Chrome |
| [Wikipedia — Claude (language model)](https://en.wikipedia.org/wiki/Claude_(language_model)) | obawy Ars Technica o Chrome, Cowork w Chrome |
| [Wikipedia — Claude (AI)](https://en.wikipedia.org/wiki/Claude_(AI)) | wyciek kodu Claude Code, nadużycia (Wired, BBC), Claude Design |
| [Hermes Agent — GitHub](https://github.com/NousResearch/hermes-agent) | MIT, gwiazdki, wydania, zero porad bezpieczeństwa w 2026 |
| [Hermes Agent — README](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/README.md) | funkcje, backendy, FTS5, migracja z OpenClaw, trajektorie |
| [Hermes Agent — strona](https://hermes-agent.nousresearch.com/) | ceny Nous Portal Plus / Super / Ultra (11.10.2026) |
| [Hermes docs — pamięć](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) | limity MEMORY.md i USER.md, zamrożona migawka |
| [Hermes docs — umiejętności](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) | katalog umiejętności, hub, ClawHub, skanowanie |
| [Hermes docs — cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) | zadania w języku naturalnym |
| [Hermes docs — delegacja](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation) | wykonawcy z osobnym dostawcą, limit dzieci (za przeglądem harnessów) |
| [Hermes docs — głos](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode) | faster-whisper lokalnie, Edge TTS domyślnie (za przeglądem harnessów) |
| [Hermes docs — indeks](https://hermes-agent.nousresearch.com/llms.txt) | Nous Portal jako dostawca modeli i kredytów |
| [Nous — runda finansowania](https://nousresearch.com/a-note-on-our-fundraise) | 90 mln USD, inwestorzy, 24 mln klonów, 2,5% tokenów, MIT od II 2026 |
| [Nous Research](https://nousresearch.com/) | aplikacja w Microsoft Store od 8.10.2026 |
| [Nous — blog](https://nousresearch.com/blog) | refaktoryzacja z 1393 agentami |
| [Hermes Business](https://portal.nousresearch.com/business) | wspólne saldo, limity na osobę, biblioteka umiejętności, Enterprise |
| [NVIDIA NemoClaw](https://github.com/NVIDIA/NemoClaw) | obsługiwane agenty (OpenClaw, Hermes, Deep Agents), piaskownica OpenShell |
| [Manus — inżynieria kontekstu](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) | sześć zasad, KV-cache, 100:1, todo.md, ok. 50 wywołań na zadanie |
| [Manus 2.0](https://manus.im/blog/introducing-manus-2-0) | Cascade, Cloud Computer, automatyzacje, Cue, deklarowane oszczędności |
| [Manus Flex](https://manus.im/blog/introducing-manus-flex) | własny klucz do modeli, kredyty za infrastrukturę |
| [Manus — Wide Research](https://manus.im/blog/introducing-wide-research) | równolegli agenci ze świeżym kontekstem |
| [Manus docs — Wide Research](https://manus.im/docs/features/wide-research.md) | do 250 pozycji |
| [Manus 1.5](https://manus.im/blog/manus-1.5-release) | aplikacje full-stack, czas zadania 15 → <4 min |
| [Manus — Browser Operator](https://manus.im/blog/manus-browser-operator) | rozszerzenie w lokalnej przeglądarce, zgoda na sesję, log akcji |
| [Manus docs — Cloud Browser](https://manus.im/docs/features/cloud-browser.md) | trwałe sesje, Take Over, blokady IP centrów danych |
| [Manus — 100 mln ARR](https://manus.im/blog/manus-100m-arr) | ARR, run-rate, 147 bilionów tokenów, 80 mln komputerów, 105 pracowników |
| [Manus — list do użytkowników](https://manus.im/blog/a-note-to-our-users) | powrót do niezależności, usunięcie danych 23–24.08.2026, dane w USA i Singapurze |
| [Manus — niezależność](https://manus.im/blog/manus-resumes-independent-operations) | formalna niezależność 1.09.2026, dostępność w UE |
| [Manus — zasady kredytów](https://help.manus.im/en/articles/11711097-what-are-the-rules-for-credits-consumption-and-how-can-i-obtain-them) | co zużywa kredyty, dzienne odświeżenie, brak przenoszenia |
| [E2B — studium Manusa](https://e2b.dev/blog/how-manus-uses-e2b-to-provide-agents-with-virtual-computers) | mikro-VM Firecracker, ok. 150 ms startu, odrzucenie Dockera |
| [The Decoder](https://the-decoder.com/chinese-ai-agent-manus-uses-claude-sonnet-and-open-source-technology/) | modele na starcie, browser-use, układ wykonawca–planista |
| [TechCrunch — Manus III 2025](https://techcrunch.com/2025/03/09/manus-probably-isnt-chinas-second-deepseek-moment/) | testy niezawodności, deklaracja GAIA |
| [TechCrunch — weto Chin](https://techcrunch.com/2026/04/27/china-vetoes-metas-2b-manus-deal-after-months-long-probe/) | decyzja NDRC 27.04.2026, zakaz wyjazdu założycieli |
| [TechCrunch — runda X 2026](https://techcrunch.com/2026/10/08/chinas-manus-raises-over-500m-in-first-funding-round-since-split-with-meta/) | >500 mln USD, Boyu i IDG, cel ok. 4 mld USD |
| [Bloomberg — blokada przejęcia](https://www.bloomberg.com/news/articles/2026-04-27/china-blocks-meta-s-2-billion-acquisition-of-ai-startup-manus) | potwierdzenie blokady |
| [Yahoo — wycena Manusa](https://finance.yahoo.com/technology/ai/articles/manus-seeks-4b-valuation-beijing-183502124.html) | odkup udziałów, separacja operacyjna |
| [Dahui Lawyers](https://www.dahuilawyers.com/en/news-insights/chinas-first-public-foreign-investment-security-review-prohibition-the-metamanus-decision/) | pierwszy publiczny zakaz w chińskim przeglądzie inwestycji |
| [Sacra — Manus](https://sacra.com/c/manus) | ceny z III 2025, szacunek 450 mln USD w VI 2026 |
| [MyClaw — recenzja Manus 2.0](https://myclaw.ai/blog/manus-2-0) | ceny z IX 2026, Cloud Computer, limity portfela Cue (strona trzecia) |
| [Embrace The Red](https://embracethered.com/blog/posts/2025/manus-ai-kill-chain-expose-port-vs-code-server-on-internet/) | atak z wystawieniem portu (25.08.2025) |
| [OpenManus](https://github.com/FoundationAgents/OpenManus) | otwarty klon MIT, gwiazdki, obsługa Ollamy |
| [Wikipedia — Manus](https://en.wikipedia.org/wiki/Manus_(AI_agent)) | premiera, seria B, przeprowadzka do Singapuru, odsprzedaż zaproszeń |
| [browser-use — GitHub](https://github.com/browser-use/browser-use) | MIT, gwiazdki, wydanie 0.13.11 |
| [browser-use — API GitHuba](https://api.github.com/repos/browser-use/browser-use) | data utworzenia repozytorium, forki |
| [browser-use — cennik](https://browser-use.com/pricing.md) | stawki za przeglądarkę, proxy, tokeny, progi współbieżności (3.09.2026) |
| [browser-use — benchmarki](https://browser-use.com/benchmarks) | Browser Use Bench v2.1 z kosztem na zadanie (7.10.2026) |
| [browser-use — changelog 3.04.2026](https://browser-use.com/changelog/3-4-2026) | darmowy próg, harmonogram V4, umiejętność Agency |
| [browser-use — BU-30B-A3B](https://browser-use.com/changelog/16-12-2025) | otwarte wagi, 3B aktywnych, vLLM |
| [browser-use — przejście na CDP](https://browser-use.com/changelog/19-8-2025) | „100% CDP-based" |
| [browser-use — BU 2.0](https://browser-use.com/changelog/27-1-2026) | porównanie z Opus 4.5 (deklaracja producenta) |
| [browser-use — wybór agenta](https://docs.browser-use.com/cloud/choosing-an-agent) | V2 / V3 / V4: koszt, trafność, czas; profile i sekrety |
| [browser-use — karta BU 2.0](https://docs.browser-use.com/open-source/bu-2-0-model-card) | model tylko przez API |
| [browser-use — raport WebVoyager](https://browser-use.com/posts/sota-technical-report) | 89,1% po usunięciu 55 zadań |
| [Felicis](https://felicis.com/blog/browser-use-the-tool-making-it-easier-for-ai-agents-to-navigate-websites-raises-17m) | seed 17 mln USD, inwestorzy |
| [ain.ua](https://en.ain.ua/2025/03/25/browser-use-raises-17m) | założyciele, ETH Zurych, idea „tekst zamiast pikseli" |
| [Princeton HAL — Online-Mind2Web](https://hal.cs.princeton.edu/online_mind2web) | niezależny wynik 40,0% dla browser-use + Sonnet 4 |
| [TechCrunch — OpenAI o prompt injection](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/) | „unlikely to ever be fully solved" (22.12.2025) |
| [The Register — Gartner](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/) | zalecenie blokowania przeglądarek AI (8.12.2025) |
| [TechCrunch — koniec Atlasa](https://techcrunch.com/2026/07/09/openai-is-shutting-down-atlas-but-its-ai-browser-ambitions-are-still-growing/) | zamknięcie Atlasa, „feature, not the destination" |
| [36Kr — udział przeglądarek AI](https://eu.36kr.com/en/p/3931781634260099) | <1% rynku przeglądarek (VIII 2026) |
| [OpenManus — commity](https://api.github.com/repos/FoundationAgents/OpenManus/commits?per_page=5) | integracja Browser Use CLI 3.0 (VIII 2026) |
| [Przegląd harnessów — profile](../harnessy-agentowe/01-PROFILE.md) | Hermes (81 pkt, 4. miejsce), OpenClaw (47. miejsce), pułapka H4, Moltis z polskim Piperem |

## Profile 3, 4, 9–12, 14

| Źródło | Co wziąłem |
|---|---|
| [Fortune, 11.06.2026 — Abridge](https://fortune.com/2026/06/11/abridge-operating-system-medicine-nvidia-eli-lilly-artsight/) | zwrot Abridge w „platformę”, Lilly, NVIDIA, Artisight, 100 mln+ rozmów rocznie, wycena 5,3 mld USD |
| [Sacra: Abridge](https://sacra.com/c/abridge/) | szacunek ceny ok. 2 500 USD na lekarza rocznie, ARR 2024–2025, Best in KLAS II 2026 |
| [Abridge: benchmark ASR](https://www.abridge.com/blog/becoming-the-benchmark-for-healthcare-ai) | deklarowane wyniki własnego ASR (6.08.2025) |
| [Abridge: eliminacja konfabulacji](https://www.abridge.com/ai/science-confabulation-hallucination-elimination) | model-strażnik, 97% vs 82% GPT-4o (dane firmy) |
| [Webb i in., Appl Clin Inform 2026](https://pubmed.ncbi.nlm.nih.gov/41734793/) | niezależne porównanie Abridge i DAX na SOR |
| [MobiHealthNews: seria E Abridge](https://www.mobihealthnews.com/news/abridge-secures-300m-boosts-valuation-53b) | rundy D i E, wyceny 2025 |
| [Menlo Ventures: AI w ochronie zdrowia 2025](https://menlovc.com/perspective/2025-the-state-of-ai-in-healthcare/) | udziały w rynku scribe'ów (Microsoft ok. 33%, Abridge ok. 30%) |
| [HLTH: Epic AI Charting](https://hlth.com/insights/news/epic-releases-native-ai-charting-for-integrated-clinical-documentation-2026-02-06) | natywny scribe Epic (II 2026) i presja na dostawców |
| [Fierce Healthcare: PHTI o scribe'ach](https://www.fiercehealthcare.com/ai-and-machine-learning/early-evaluation-ai-scribes-finds-decreased-burnout-limited-financial-roi) | mniej wypalenia, ograniczony zwrot finansowy |
| [Lukac i in., NEJM AI (RCT UCLA)](https://pubmed.ncbi.nlm.nih.gov/41497288/) | umiarkowany zysk czasu przy scribe'ach |
| [Parakeet-TDT-0.6B-v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) | lokalny ASR z polskim, ok. 7,3% WER wg karty modelu |
| [pyannote community-1](https://huggingface.co/pyannote/speaker-diarization-community-1) | diaryzacja offline, CC-BY-4.0 |
| [Noa: cennik](https://noa.ai/pl/cennik) | Noa Notes 199 zł + VAT miesięcznie, kotwica cenowa dla scribe'a |
| [Harvey: wiele modeli z założenia](https://www.harvey.ai/en-US/blog/why-harvey-is-multi-model-by-design) | router modeli, failover, BigLaw Bench |
| [Harvey Tenet](https://www.harvey.ai/blog/post-training-update-harvey-tenet) | Kimi K3 + RL (GSPO), brak danych klientów, ok. 1/10 kosztu |
| [Harvey II](https://www.harvey.ai/blog/introducing-harvey-ii) | Spaces, pamięć osobista, ethical walls |
| [Harvey: MCP Policy Engine](https://www.harvey.ai/blog/building-harveys-mcp-policy-engine) | polityki poza modelem, lethal trifecta, tool pinning |
| [Harvey: bezpieczeństwo](https://www.harvey.ai/en-US/security) | regiony przetwarzania, zero retencji, certyfikaty, brak on-prem |
| [Harvey: runda 550 mln USD](https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence) | 15,5 mld USD (9.09.2026), 80% Am Law 100 |
| [TechCrunch, 9.09.2026 — Harvey](https://techcrunch.com/2026/09/09/harvey-hits-15-5b-valuation-months-after-reaching-11b/) | łączny kapitał ponad 1,55 mld USD |
| [Wikipedia: Harvey](https://en.wikipedia.org/wiki/Harvey_(software)) | historia wycen, założyciele, test A&O |
| [ITBrief: 500 agentów Harvey](https://itbrief.co.uk/story/harvey-launches-500-legal-ai-agents-builder-tool) | Agent Builder, liczba klientów (V 2026) |
| [raising.fi: Harvey IX 2026](https://raising.fi/news/harvey-undisclosed-september-2026) | ARR ponad 400 mln USD (prasa wtórna), przejęcie Guardrails AI |
| [Vaquill: przegląd Harvey](https://www.vaquill.ai/blog/harvey-ai-review-honest-assessment) | szacunki cen stanowisk (niezweryfikowane) |
| [LexisNexis + Harvey](https://www.lexisnexis.com/community/pressroom/b/news/posts/lexisnexis-and-harvey-announce-strategic-alliance-to-integrate-trusted-high-quality-ai-technology-and-legal-content-and-develop-advanced-workflows) | sojusz treściowy, Shepard's |
| [Baza halucynacji D. Charlotina](https://www.damiencharlotin.com/hallucinations/) | 2 184 sprawy, 6 w Polsce (10.10.2026) |
| [Cursor: cennik](https://cursor.com/pricing) | plany i ceny (X 2026), Bugbot, MCP |
| [Cursor: changelog](https://cursor.com/changelog) | Self-Hosted Machines, Projects, Rollouts, iOS (VIII–X 2026) |
| [Cursor: Composer 2](https://cursor.com/blog/composer-2) | wyniki benchmarków i ceny tokenów (dane firmy) |
| [Cursor: ceny w czerwcu 2025](https://cursor.com/blog/june-2025-pricing) | zmiana planu Pro, przeprosiny i zwroty |
| [Cursor: wykorzystanie danych](https://cursor.com/data-use) | każde zapytanie przez backend, Privacy Mode |
| [Cursor: bezpieczeństwo](https://cursor.com/security) | SOC 2 Type II |
| [Cursor: dołączenie do SpaceX](https://cursor.com/blog/joining-spacex) | zamknięcie przejęcia 14.08.2026, SpaceXAI, Grok |
| [Wikipedia: Cursor](https://en.wikipedia.org/wiki/Cursor_(company)) | rundy, harmonogram transakcji SpaceX, przejęcia, bot „Sam” |
| [Bloomberg: ARR Cursora 2 mld USD](https://www.bloomberg.com/news/articles/2026-03-02/cursor-recurring-revenue-doubles-in-three-months-to-2-billion) | ARR II 2026 |
| [Gigazine: Composer 2 na Kimi](https://gigazine.net/gsc_news/en/20260323-cursor-admits-composer-2-kimi) | nieujawniona baza Kimi K2.5 |
| [DataCamp: Cursor 3](https://www.datacamp.com/blog/cursor-3) | okno agentów, VM w chmurze, przenoszenie sesji |
| [Silicon Canals: Cursor](https://siliconcanals.com/t-cursor-100-million-2-billion-annualized-revenue-13-months/) | ok. 60% przychodu od firm (III 2026) |
| [Jetadmin: plany Cursora](https://www.jetadmin.io/blog/cursor-pricing-explained-plans-credit-system-and-real-costs-in-2026/) | Pro+ i Ultra (VII 2026) |
| [TNW: seria C Granoli](https://thenextweb.com/news/granola-series-c-meeting-ai-enterprise-context) | rundy, MCP i API, klienci |
| [Granola: cennik](https://www.granola.ai/pricing) | plany per stanowisko, integracje, funkcje Enterprise |
| [Granola: transkrypcja](https://docs.granola.ai/help-center/taking-notes/transcription) | audio nie jest zapisywane, diaryzacja Me/Them |
| [YipitData: Granola vs konkurencja](https://www.yipitdata.com/resources/blog/granola-vs-fathom-otter-fireflies-ai-notetaking) | przejmowanie użytkowników, niski churn |
| [SoftwareTestingHelp: Granola](https://www.softwaretestinghelp.com/?p=411472) | podawani dostawcy ASR i LLM (niezweryfikowane) |
| [ARR.club: Granola](https://www.arr.club/granola/granola-arr-grow-at-250-in-q1-2026) | wzrost przychodu w I kw. 2026 |
| [Sacra: Granola](https://sacra.com/research/250m-year-granola-for-plumbers) | 250 tys.+ użytkowników (niezweryfikowane) |
| [Substack: zagrożenia notatników AI](https://afadeev.substack.com/p/the-hidden-dangers-of-ai-note-taking) | zaszyty klucz AssemblyAI w becie |
| [Granola: podatność VI 2026](https://docs.granola.ai/help-center/policies/security-contributions/desktop-app-navigation-vulnerability) | przebieg łatania |
| [Startup Fortune: prywatność Granoli](https://startupfortune.com/granola-ai-meeting-notes-are-not-as-private-as-you-might-think/) | domyślne udostępnianie i trenowanie |
| [PPC Land: pozew Chamberlain v. Granola](https://ppc.land/granola-sued-for-recording-meetings-without-consent-to-train-ai-models/) | pozew zbiorowy 30.07.2026 |
| [Sierra: blog](https://sierra.ai/blog) | Agent OS 2.0, Voice Personas, Ghostwriter, fleming-1 |
| [Sierra: rok drugi](https://sierra.ai/blog/year-two-in-review) | ARR, klienci, Fortune 20, ekspansja |
| [Sierra: Horizon](https://sierra.ai/blog/horizon) | agenci długoterminowi, „płacisz za wyniki” |
| [Sierra: cena za wynik](https://sierra.ai/blog/outcome-based-pricing-for-ai-agents) | model rozliczeń (10.12.2024) |
| [Sierra: τ-bench](https://sierra.ai/blog/benchmarking-ai-agents) | pass^k, spadek GPT-4o przy pass^8 |
| [Sierra: Personal Agent Protocol](https://sierra.ai/blog/introducing-personal-agent-protocol) | protokół z Metą (6.10.2026) |
| [TechCrunch, 4.05.2026 — Sierra](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/) | 950 mln USD przy ponad 15 mld, 40% Fortune 50 |
| [Forbes, XI 2025 — Sierra](https://www.forbes.com/sites/richardnieva/2025/11/05/sierra-bret-taylor-clay-bavor/) | wycena 10 mld USD |
| [Decagon: seria D](https://decagon.ai/blog/series-d-announcement) | konkurent Sierry, 4,5 mld USD |
| [Decagon: blog](https://decagon.ai/blog) | protokół PACT (6.10.2026) |
| [Intercom: cennik](https://www.intercom.com/pricing) | 0,99 USD za wynik |
| [Parloa: cennik](https://www.parloa.com/platform/pricing/) | rozliczenie za minutę lub interakcję |
| [Wikipedia: OpenEvidence](https://en.wikipedia.org/wiki/OpenEvidence) | funkcje, licencjonowane treści, pozew przeciw Pathway |
| [Sacra: OpenEvidence](https://sacra.com/c/openevidence/) | przychód, CPM, marża, użycie, ChatGPT for Clinicians |
| [Rutland Herald: runda OpenEvidence](https://www.rutlandherald.com/news/business/openevidence-raises-250-million-to-build-medical-superintelligence-for-doctors/article_0960939c-ca41-5321-8417-54f84800ece6.html) | 250 mln USD przy 12 mld (21.01.2026) |
| [Sacra: OpenEvidence vs Doximity](https://sacra.com/research/openevidence-vs-doximity/) | konflikt i konwergencja produktów |
| [Wikipedia: Doximity](https://en.wikipedia.org/wiki/Doximity) | przejęcie Pathway (VIII 2025) |
| [ASCO Post: ankieta AMA](https://ascopost.com/news/march-2026/ama-survey-finds-rapid-growth-in-physician-ai-adoption/) | 81% lekarzy w USA używa AI (2026) |
| [Physicians Practice: ankieta AMA](https://www.physicianspractice.com/view/physician-ai-use-is-surging-is-your-practice-ready-) | 71% bez wpływu na wybór narzędzi |
| [Kodeks Etyki Lekarskiej (PDF)](https://nil.org.pl/uploaded_images/1723037323_kel-2305.pdf) | art. 12 — AI w diagnostyce i leczeniu |
| [Noxtua](https://www.noxtua.com/) | funkcje, Athena i Minerva, liczba dokumentów |
| [Noxtua: bezpieczeństwo](https://www.noxtua.com/security) | hosting, self-host w suwerennej chmurze, § 43e BRAO, § 203 StGB |
| [Noxtua: seria C](https://www.noxtua.com/news/press-releases/series-c) | 100 mln+ EUR (23.09.2026), 30 000+ użytkowników, certyfikaty |
| [TechCrunch: seria B Noxtua](https://techcrunch.com/2025/04/22/noxtua-raises-92m-for-its-sovereign-ai-tuned-for-the-german-legal-system/) | 92,2 mln USD, własny model 2025, historia Xayn |
| [CMS: C.H.Beck inwestorem Noxtua](https://cms.law/en/deu/news-information/c.h.beck-becomes-leading-investor-in-legal-ai-noxtua) | kwota serii B wg CMS, praca bez anonimizacji |
| [Noxtua: Beck-Noxtua w Polsce](https://www.noxtua.com/news/press-releases/beck-noxtua-poland) | zapowiedź 3.12.2025 |
| [Noxtua: Beck-Noxtua w Czechach](https://www.noxtua.com/news/press-releases/beck-noxtua-for-the-czech-republic) | hosting IONOS i Open Telekom Cloud, BSI C5 |
| [beck-noxtua.pl](https://www.beck-noxtua.pl/) | 590 zł netto/mies., wymóg Legalis Silver+, certyfikaty ISO |
| [NRA: § 23e Zbioru Zasad Etyki](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/) | zasady korzystania z AI przez adwokatów |
| [Prawo o adwokaturze (PDF)](https://api.sejm.gov.pl/eli/acts/DU/2024/1564/text.pdf) | art. 6 — tajemnica adwokacka |
| [Ustawa o radcach prawnych (PDF)](https://api.sejm.gov.pl/eli/acts/DU/2024/499/text.pdf) | art. 3 — tajemnica radcowska |
| [UODO: listy kontrolne AI](https://uodo.gov.pl/pl/138/4533) | „pytania inicjalne” przed wdrożeniem AI (6.08.2026) |
| [KIRP: rekomendacje AI](https://kirp.pl/rekomendacje-dotyczace-korzystania-z-ai/) | rekomendacje dla radców prawnych |
| [prawo.pl: LEX Expert AI](https://www.prawo.pl/prawnicy-sady/lex-expert-ai-nowym-narzedziem-dla-prawnikow,535918.html) | konkurent w PL, linki do fragmentów źródeł |
| [Gaius-Lex](https://gaius-lex.pl/) | polski gracz z wdrożeniem on-premise |
| [Mistral: runda IX 2026](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/) | kapitał suwerennego AI w UE |
| [TechCrunch: Cohere + Aleph Alpha](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/) | fuzja przy 20 mld USD |

## Profile 7, 8, 15 i „warto znać”

Stan na 11 października 2026. Strony openai.com, chatgpt.com i perplexity.ai blokowały pobieranie, więc część faktów o
OpenAI i Perplexity pochodzi z prasy, karty systemowej (PDF) i Wikipedii; oznaczyłem to w tekście.

| Źródło | Co wziąłem |
|---|---|
| [Engadget — DevDay 2026](https://www.engadget.com/2271985/openai-dev-day-live-blog-chatgpt-news/) | 1,2 mld użytkowników tygodniowo, dots, Pro 500 (29.09.2026) |
| [Decrypt — DevDay 2026](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced) | 1,2 mld użytkowników, otwarcie harnessu Codex |
| [emergent — DevDay 2026](https://emergent.sh/news/openai-devday-2026) | ceny API GPT-6, dots poza EOG na Pro, OSWorld 2.0 Sol vs Astra |
| [eesel — dots](https://www.eesel.ai/blog/openai-dots) | VM na dota, Custom Rules, auto-review, pamięć dotów |
| [TechCrunch — dots](https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/) | dots na GPT-6 Astra, 4000+ aplikacji |
| [Karta systemowa ChatGPT agent](https://cdn.openai.com/pdf/839e66fc-602c-48bf-81d3-b21eacc3459d/chatgpt_agent_system_card.pdf) | narzędzia agenta, trafność potwierdzeń, watch mode, wyłączona pamięć, odporność na wstrzyknięcia |
| [digitalapplied — ChatGPT Work](https://www.digitalapplied.com/blog/chatgpt-work-openai-agent-launch-2026) | tryb planu, 1400+ wtyczek, auto-review, rozliczanie za użycie |
| [9to5Mac — koniec Atlasa](https://9to5mac.com/2026/07/09/openai-is-discontinuing-chatgpt-atlas-its-standalone-desktop-browser/) | deprecjacja Atlasa, nowa aplikacja desktopowa |
| [Forum OpenAI — Atlas](https://community.openai.com/t/atlas-is-scheduled-to-stop-working-on-august-9-2026/1389473) | data wyłączenia Atlasa 9.08.2026 |
| [36Kr — Atlas](https://eu.36kr.com/en/p/3931781634260099) | „feature, not a destination", ok. 10 mln MAU Atlasa, udział AI-przeglądarek < 1% |
| [9to5Mac — zadania w harmonogramie](https://9to5mac.com/2026/06/17/openai-launches-scheduled-tasks-in-chatgpt-details-here/) | zadania, limit raz na godzinę, koniec Pulse |
| [Thurrott — pamięć](https://www.thurrott.com/a-i/337052/openai-is-improving-how-chatgpts-memory-works) | „Dreaming" od 4.06.2026 |
| [9to5Mac — Agent Plugins](https://9to5mac.com/2026/08/06/gpt-5-turning-one-as-openai-shares-new-agent-plugins-standard/) | standard wtyczek i komitet |
| [OpenAI — computer use w API](https://developers.openai.com/api/docs/guides/tools-computer-use) | zalecenie „kod zamiast kliknięć" |
| [TechCrunch — prompt injection](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/) | atakujący trenowany RL, „unlikely to ever be fully solved" |
| [PinMeTo — reklamy w Europie](https://www.pinmeto.com/news/chatgpt-ads-31-european-markets-2026/) | reklamy w Polsce od 24.08.2026, tylko kontekstowe |
| [a16z — Top 100](https://a16z.com/100-gen-ai-apps-7/) | reklamy 1 mld USD rocznie, subskrybenci 3× vs Claude i Gemini |
| [Investing.com — ARR OpenAI](https://www.investing.com/news/stock-market-news/openais-annual-recurring-revenue-nears-70-billion-axios-reports-4923088) | ARR „blisko 70 mld USD" (Axios/Reuters) |
| [Bloomberg Law — runda OpenAI](https://news.bloomberglaw.com/tech-and-telecom-law/openai-valued-at-852-billion-after-closing-122-billion-round) | 122 mld USD przy 852 mld USD |
| [TechCrunch — Sensor Tower](https://techcrunch.com/2026/06/16/chatgpts-market-share-slips-below-50-for-first-time/) | MAU i udziały ChatGPT, Gemini, Perplexity, Grok, DeepSeek (V 2026) |
| [Hugging Face — privacy-filter](https://huggingface.co/openai/privacy-filter) | otwarty klasyfikator PII OpenAI |
| [Wikipedia — ChatGPT](https://en.wikipedia.org/wiki/ChatGPT) | ChatGPT Health poza EOG, zmiana nazwy na wtyczki |
| [Alphabet — wyniki II kw. 2026](https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000066/googexhibit991q22026.htm) | 950 mln MAU, segment subskrypcji 12,9 mld USD |
| [9to5Google — I/O 2026](https://9to5google.com/2026/05/19/google-io-2026-news/) | Daily Brief, Spark, Live, ceny Ultra |
| [TechCrunch — Gemini 3.5 Flash](https://techcrunch.com/2026/05/19/with-gemini-3-5-flash-google-bets-its-next-ai-wave-on-agents-not-chatbots/) | Antigravity, pauzy na decyzje |
| [Android Headlines — Spark w AI Pro](https://www.androidheadlines.com/2026/07/google-gemini-spark-expands-to-ai-pro-subscribers.html) | Tasks/Schedules/Skills, zgoda wg zakresu danych, wyłączenia krajów |
| [Google — pomoc Spark](https://support.google.com/gemini/answer/16596215) | lokalny vs zdalny Chrome, 15 zadań, poza EOG, ostrzeżenia |
| [Google — Spark VII 2026](https://blog.google/innovation-and-ai/products/gemini-app/gemini-spark-updates-july-2026/) | integracja z Chrome, 160+ krajów |
| [Efficiently Connected — Spark](https://www.efficientlyconnected.com/google-io-2026-gemini-spark-consumer-ai-agent/) | dedykowane VM w chmurze |
| [Google — bezpieczeństwo agenta w Chrome](https://blog.google/security/architecting-security-for-agentic/) | planista + User Alignment Critic, Origin Sets, potwierdzenia, VRP |
| [Google — auto browse](https://blog.google/products-and-platforms/products/chrome/gemini-3-auto-browse/) | funkcje auto browse, UCP, tylko USA |
| [Google — auto browse na Androidzie](https://blog.google/products-and-platforms/products/chrome/gemini-in-chrome-android-auto-browse/) | Android od 18.08.2026 |
| [Google — Gemini Agent](https://blog.google/products/gemini/gemini-3-gemini-app/) | Gemini Agent z 18.11.2025 |
| [Gemini API — computer use](https://ai.google.dev/gemini-api/docs/computer-use) | pętla, `safety_decision`, 7 kategorii polityk |
| [Google — Computer Use model](https://blog.google/technology/google-deepmind/gemini-computer-use-model/) | start 7.10.2025, opóźnienie ok. 225 s |
| [Google — Mariner](https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/) | Mariner, WebVoyager 83,5% |
| [Wikipedia — Project Mariner](https://en.wikipedia.org/wiki/Project_Mariner) | zamknięcie 4.05.2026 |
| [Google — 1 mld użytkowników](https://blog.google/innovation-and-ai/products/gemini-app/one-billion-monthly-users/) | ponad 1 mld miesięcznie (11.08.2026) |
| [Google — Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) | ceny API Argon |
| [Gemini — ceny PL](https://gemini.google/subscriptions/) · [ceny USA](https://gemini.google/us/subscriptions/?hl=en) | plany w złotych i dolarach |
| [Business Today — Gemini zamiast Asystenta](https://www.businesstoday.in/amp/technology/news/story/google-assistant-to-be-replaced-by-gemini-starting-september-on-android-and-wearos-547570-2026-08-06) | zastąpienie Asystenta od 4.09.2026 |
| [TNW — Live, Spark i DMA](https://thenextweb.com/news/gemini-live-spark-voice-agentic-tasks-dma-rival-assistants) | Personal Intelligence, termin DMA VII 2027 |
| [9to5Google — Gems → Skills](https://9to5google.com/2026/09/27/gemini-gems-skills/) | migracja 17.11.2026 |
| [Android Developers — Gemini Nano](https://developer.android.com/ai/gemini-nano) | AICore, offline, Hybrid API |
| [Google DeepMind — Gemma](https://deepmind.google/models/gemma/) | rozmiary Gemma 4 |
| [TechGenyz — Gemini agent dla firm](https://techgenyz.com/google-gemini-agent-enterprise-ai/) | agenci-współpracownicy, routing do Claude |
| [BleepingComputer — BragJack](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/) | atak na Gemini w Chrome, Comet, Neon; CVE-2026-0628 |
| [Wikipedia — Google Gemini](https://en.wikipedia.org/wiki/Google_Gemini) | pozwy i kara we Francji |
| [VentureBeat — Portable Computer](https://venturebeat.com/infrastructure/perplexity-partners-with-nvidia-to-launch-portable-computer-a-fully-local-ai-agent-with-zero-token-costs) | architektura, modele, sprzęt, Terminal-Bench, eskalacja z filtrem PII |
| [VentureBeat — hybryda na Computex](https://venturebeat.com/technology/perplexity-ai-unveils-hybrid-local-cloud-inference-system-at-computex-2026) | zgoda przed wysłaniem do chmury |
| [TechRepublic — Portable Computer na Windows](https://www.techrepublic.com/article/news-perplexity-portable-computer-windows/) | Windows od IX 2026 (zajawka) |
| [Computerworld — Perplexity Computer](https://www.computerworld.com/article/4138723/perplexitys-new-computer-agent-will-run-other-agents-for-you.html) | podział modeli, Enterprise Max 325 USD |
| [TechCrunch — Perplexity Computer](https://techcrunch.com/2026/02/27/perplexitys-new-computer-is-another-bet-that-users-need-many-ai-models/) | 19 modeli, Max 200 USD |
| [TechCrunch — Comet za darmo](https://techcrunch.com/2025/10/02/perplexitys-comet-ai-browser-now-free-max-users-get-new-background-assistant/) | darmowy Comet, asystent w tle |
| [Wikipedia — Comet](https://en.wikipedia.org/wiki/Comet_(browser)) · [Perplexity AI](https://en.wikipedia.org/wiki/Perplexity_AI) | platformy, rezygnacja z reklam, Azure, Personal Computer |
| [The Decoder — BrowseSafe](https://the-decoder.com/perplexitys-browsesafe-tries-to-patch-the-gaping-security-holes-inherent-in-ai-browser-agents/) | otwarty klasyfikator, 91% wykrycia, ok. 10% przecieka |
| [PYMNTS — przychody Perplexity](https://www.pymnts.com/news/artificial-intelligence/2026/perplexitys-shift-to-ai-agents-boosts-revenue-50/) | ARR ok. 450 mln USD w III 2026, 100 mln+ MAU |
| [Yahoo Finance — Nvidia i Perplexity](https://finance.yahoo.com/technology/ai/articles/nvidia-discusses-perplexity-investment-30-031804276.html) | ARR ok. 750 mln USD, wycena > 30 mld USD |
| [TNW — rozmowy z Nvidią](https://thenextweb.com/news/nvidia-perplexity-30bn-valuation-talks) | brak publikowanych liczb |
| [TechCrunch — Indie](https://techcrunch.com/2026/08/18/perplexitys-free-ai-offer-left-it-with-millions-more-users-in-india/) | Airtel, MAU, przychód z aplikacji |
| [Vice — Comet Plus](https://www.vice.com/en/article/perplexity-comet-plus-announced/) | ceny Pro/Max, Comet Plus |
| [Jones Day — IX Okręg](https://www.jonesday.com/en/insights/2026/09/ninth-circuit-vacates-cfaa-injunction-against-perplexitys-comet-ai-agent) | uchylenie nakazu, przepływ danych w Comet |
| [Brave — Comet](https://brave.com/blog/comet-prompt-injection/) | wstrzyknięcie pośrednie, zalecenia |
| [LayerX — CometJacking](https://layerxsecurity.com/blog/cometjacking-how-one-click-can-turn-perplexitys-comet-ai-browser-against-you/) | eksfiltracja przez parametr URL |
| [The Register — PleaseFix](https://www.theregister.com/2026/03/03/perplexity_comet_browser_hole_cal_invite/) | zero-click przez kalendarz, łatki |
| [Help Net Security — MCP API w Comet](https://www.helpnetsecurity.com/2025/11/20/perplexity-comet-browser-security-mcp-api/) | ukryte rozszerzenie, wyłączenie |
| [The Register — Gartner](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/) | rada blokowania AI-przeglądarek |
| [Android Authority — Hey Plex](https://www.androidauthority.com/hey-perplexity-3655439/) | Perplexity w Galaxy S26 (zajawka) |
| [money.pl — Bielik i NVIDIA](https://www.money.pl/gospodarka/wielki-krok-dla-polskiego-ai-bielik-rozpoczyna-wspolprace-z-nvidia-7166523596470944a.html) | zapowiedź Bielika w Perplexity |
| [AMD — Radeon AI PRO R9700](https://www.amd.com/en/products/graphics/workstations/radeon-ai-pro/ai-9000-series/amd-radeon-ai-pro-r9700.html) | 32 GB na kartę |
| [Hugging Face — Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | 84,3% OSWorld-Verified (deklaracja), Apache 2.0 |
| [UI-TARS-1.5-7B](https://huggingface.co/ByteDance-Seed/UI-TARS-1.5-7B) · [UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) | wyniki OSWorld, operatorzy, uruchamianie lokalne |
| [TNW — Legora](https://thenextweb.com/news/legora-just-hit-100-million-in-revenue-it-took-18-months) | ARR, finansowanie, tabular review |
| [HLTH — Heidi](https://hlth.com/insights/news/heidi-raises-340m-to-expand-clinical-ai-into-supervised-agentic-workflows) | ARR 50 mln USD, 340 mln USD, agenci poza UK/UE |
| [Microsoft — prywatność Copilot](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) · [wyniki FY26 Q4](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast) | EU Data Boundary, 30 mln stanowisk |
| [Yahoo Finance — Genspark](https://finance.yahoo.com/technology/ai/articles/genspark-ai-extends-series-b-131000248.html) | ARR, wycena 2,6 mld USD |
| [Cognition — Poke](https://cognition.com/blog/interaction) | przejęcie, 100 mln wiadomości |
| [NVIDIA NemoClaw](https://github.com/NVIDIA/NemoClaw) | piaskownica OpenShell, status alpha |
| [TechCrunch — Ghost](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/) | cena, sprzęt, modele, zapora |
| [PubMed — RCT UCLA](https://pubmed.ncbi.nlm.nih.gov/41497288/) | wyniki Nabla i DAX/Dragon |
| [Nabla — ASR](https://nabla.com/blog/assessing-the-reliability-of-nablas-speech-to-text-engine) | Whisper + 7000 h audio |
| [Basis — behavior specs](https://www.getbasis.ai/blogs/behavior-specs-an-open-standard-for-supervising-long-horizon-agents) | standard oceny przebiegu agenta |
| [Hebbia — Matrix 2.0](https://www.hebbia.com/blog/introducing-matrix-2-0) | interfejs Matrix, checkpointy |
| [TechCrunch — Glean](https://techcrunch.com/2026/05/28/gleans-top-line-crosses-300m-as-ai-budget-cutting-becomes-its-major-selling-point/) · [ITBrief — Tau](https://itbrief.asia/story/glean-launches-tau-to-cut-enterprise-ai-token-costs) | ARR 300 mln USD, koszt zadania |
| [Lindy — cennik](https://www.lindy.ai/pricing) · [iMessage](https://www.lindy.ai/blog/imessage-api-three-rewrites-one-apple-ban-and-what-actually-works) | reguła zatwierdzeń, ban Apple |
| [gaius-lex.pl](https://gaius-lex.pl/) · [Signalbase](https://www.trysignalbase.com/news/funding/gaius-lex-secures-5) | Gaius Vault on-prem, seed |
| [Meta — Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) · [retencja Muse](https://cryptobriefing.com/meta-muse-app-store-retention/) | Sentinel, VM, płatności; 5 mln pobrań vs 700 tys. DAU |
| [VentureBeat — Muse Glimmer](https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now) | parametry i licencja modelu |
| [Amazon — Alexa+](https://www.aboutamazon.com/news/devices/new-alexa-generative-artificial-intelligence) · [kraje](https://www.aboutamazon.com/news/devices/alexa-plus-international-launch) | Experts, rynki bez Polski |
| [TNW — Siri AI](https://thenextweb.com/news/apple-ios-27-siri-ai-release-icloud-plus-child-safety) · [Apple — języki](https://support.apple.com/en-us/121115) | iOS 27, UE, brak polskiego |
| [TNW — Microsoft Copilot](https://thenextweb.com/news/microsoft-copilot-mico-retired-features-killed-app-merge) · [Windows Agent Workspace](https://support.microsoft.com/en-us/windows/experimental-agentic-features-a25ede8a-e4c2-4841-85a8-44839191dfb3) | usunięte funkcje, 38,5 mln, konto agenta |
| [Wikipedia — Grok](https://en.wikipedia.org/wiki/Grok_(chatbot)) · [Finbold — Grok Bot](https://finbold.com/spacexais-grok-bot-agent-surpasses-400000-users-after-the-first-month/) | incydenty, 418 tys. użytkowników |
| [TechNode — Doubao](https://technode.com/2026/09/23/bytedance-doubao-general-session-team-cuts/) | 200 mln DAU |
| [TechTimes — Qwen](https://www.techtimes.com/articles/323907/20260811/qwen-sells-paid-office-subscriptions-users-it-bought-with-free-bubble-tea.htm) | kampania 6 mld RMB, długość sesji, MAU |
| [Hugging Face — DeepSeek](https://huggingface.co/api/models?author=deepseek-ai&sort=lastModified) · [netzpolitik](https://netzpolitik.org/2025/datenschutzbehoerde-greift-ein-deepseek-fliegt-aus-den-app-stores/) | wagi MIT, żądanie usunięcia aplikacji |
| [TechCrunch — Mistral](https://techcrunch.com/2026/09/08/mistral-raises-e3b-as-sovereign-ai-becomes-big-business/) · [cennik](https://mistral.ai/pricing) | runda 3 mld EUR, Pro 14,99 USD |
| [Pulse 2.0 — Instinct](https://pulse2.com/instinct-raises-1-billion-series-c-at-10-billion-valuation/) | seria C, piaskownice, poświadczenia |
| [NanoClaw](https://github.com/nanocoai/nanoclaw) | kontenery, bramki skryptowe, Claude Agent SDK |
| [OpenManus](https://github.com/FoundationAgents/OpenManus) | szkielet, gwiazdki, Ollama |
| [Kortix — README](https://raw.githubusercontent.com/kortix-ai/suna/main/README.md) | piaskownica na sesję, broker poświadczeń, licencja |
| [Agent S](https://github.com/simular-ai/Agent-S) · [Simular — OSWorld 2.0](https://www.simular.ai/articles/sai-tops-osworld-2-0) | 72,6% OSWorld, 28,25% binarnie na OSWorld 2.0 |
| [Microsoft Research — Fara-7B](https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/) | model 7B, WebVoyager, liczba kroków |
| [Open-AutoGLM](https://github.com/zai-org/Open-AutoGLM) | sterowanie Androidem, wymagania GPU |
| [Skywork Desktop](https://skywork.ai/desktop/en/index.html) · [36Kr — Kunlun](https://eu.36kr.com/en/p/3878113666724100) | lokalna VM, ARR działu narzędzi |
| [Opera — darmowy plan dla agentów](https://blogs.opera.com/news/2026/08/your-ai-agents-can-use-opera-neon-free-of-charge/) · [MCP](https://press.opera.com/2026/03/31/opera-neon-adds-mcp-connector/) | MCP i CLI dla zewnętrznych agentów |
| [Fellou — cennik](https://fellou.ai/pricing) · [Eko](https://github.com/FellouAI/eko) | koszt zadania, otwarty framework |
| [AWS — Nova Act](https://aws.amazon.com/nova/pricing/) · [blog AWS](https://aws.amazon.com/blogs/aws/build-reliable-ai-agents-for-ui-workflow-automation-with-amazon-nova-act-now-generally-available/) | cena za godzinę agenta, kod + `act()` |
| [LawNext — CoCounsel](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html) · [BNN Bloomberg](https://www.bnnbloomberg.ca/business/2026/02/24/thomson-reuters-says-one-million-professionals-using-cocounsel-shares-soar/) | Claude Agent SDK, 1 mln użytkowników |
| [LexisNexis — wzrost](https://www.lexisnexis.com/community/pressroom/b/news/posts/legal-ai-propels-lexisnexis-to-fastest-growth-in-history) · [Protégé PL](https://www.lexisnexis.com/de-at/cee/protege-polska) | 90% nowego biznesu, oferta w Polsce |
| [Microsoft — FY26 Q4](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4) | Dragon Copilot, 100 mln wizyt |
| [Wikipedia — Doximity](https://en.wikipedia.org/wiki/Doximity) · [Sacra — OpenEvidence](https://sacra.com/c/openevidence/) | zasięg Doximity, ChatGPT for Clinicians |
| [Cognition — 1 mld run-rate](https://cognition.com/blog/1b-run-rate) | run-rate Devina |
| [VKTR — Lovable](https://www.vktr.com/ai-platforms/lovable-raises-400-million-at-133-billion-valuation/) | ARR, wycena |
| [Decagon — seria D](https://decagon.ai/blog/series-d-announcement) | AOP, wycena 4,5 mld USD |

## Rynek (02-RYNEK.md)

| Źródło | Co wziąłem |
|---|---|
| [menlovc.com](https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/) | Menlo Ventures (analityk), 9.12.2025: 37 mld USD wydatków firm na genAI, kodowanie 55% wydatków działowych |
| [menlovc.com](https://menlovc.com/perspective/2025-the-state-of-ai-in-healthcare/) | Menlo Ventures, 21.10.2025: AI w ochronie zdrowia 1,4 mld USD, skryby 600 mln, udziały DAX/Abridge/Ambience |
| [emergent.sh](https://emergent.sh/news/openai-devday-2026) | blog: ChatGPT Pro 500 (500 USD), dots bez EOG, DevDay 29.09.2026 |
| [decrypt.co](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced) | prasa: 1,2 mld tygodniowych użytkowników ChatGPT (29.09.2026) |
| [claude.com](https://claude.com/blog/cowork-research-preview) | Anthropic: ceny Pro/Max/Team |
| [gemini.google](https://gemini.google/subscriptions/) | Google: ceny AI Plus/Pro/Ultra w złotych (X 2026) |
| [vice.com](https://www.vice.com/en/article/perplexity-comet-plus-announced/) | prasa: Perplexity Pro 20 USD, Max 200 USD (VIII 2025) |
| [poke.com](https://poke.com/pricing) | Poke: Pro 19 USD, Ultra 199 USD (11.10.2026) |
| [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/) | Nous: progi Nous Portal 20/100/200 USD |
| [mistral.ai](https://mistral.ai/fr/pricing) | Mistral: Vibe Pro 14,99 EUR, Team 24,99 EUR bez VAT |
| [pymnts.com](https://www.pymnts.com/news/artificial-intelligence/2026/perplexitys-shift-to-ai-agents-boosts-revenue-50/) | prasa: Perplexity ARR 450 mln USD i 100 mln+ MAU (III 2026) |
| [finance.yahoo.com](https://finance.yahoo.com/technology/ai/articles/nvidia-discusses-perplexity-investment-30-031804276.html) | The Information przez Yahoo: ARR ok. 750 mln USD, rozmowy z NVIDIA przy >30 mld (VIII 2026) |
| [help.manus.im](https://help.manus.im/en/articles/11711097-what-are-the-rules-for-credits-consumption-and-how-can-i-obtain-them) | Manus: zasady kredytów (tokeny + maszyna + API, kolejność zużycia) |
| [myclaw.ai](https://myclaw.ai/blog/manus-2-0) | recenzja: ceny Manusa 20/40/200 USD (IX 2026), wyliczenie ceny kredytu |
| [genspark.ai](https://www.genspark.ai/helpcenter/membership-plans) | Genspark: progi Plus/Pro/Team, kredyty |
| [lindy.ai](https://www.lindy.ai/pricing) | Lindy: 49,99 USD za użytkownika, 5 000 kredytów, pauza przy końcu puli, reguła zgód |
| [fellou.ai](https://fellou.ai/pricing) | Fellou: progi i ok. 250 Sparks na zadanie |
| [browser-use.com](https://browser-use.com/pricing.md) | browser-use: 0,02 USD za godzinę przeglądarki, koszt na zadanie |
| [aws.amazon.com](https://aws.amazon.com/nova/pricing/) | AWS: Nova Act 4,75 USD za godzinę agenta |
| [rabbit.tech](https://www.rabbit.tech/newsroom/rabbit-intern-launch) | Rabbit: intern 99,99 USD za 30 zadań, cena „za zadanie" |
| [cursor.com](https://cursor.com/blog/june-2025-pricing) | Cursor: zmiana cennika 16.06.2025 i przeprosiny 4.07.2025 |
| [techcrunch.com](https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/) | prasa: tygodniowe limity Claude Code od 28.08.2025 |
| [docs.github.com](https://docs.github.com/en/copilot/concepts/billing/copilot-requests) | GitHub docs: kredyty AI od 1.06.2026 |
| [github.com](https://github.com/features/copilot/plans) | GitHub: progi Copilota i kredyty w cenie |
| [techcrunch.com](https://techcrunch.com/2026/05/28/gleans-top-line-crosses-300m-as-ai-budget-cutting-becomes-its-major-selling-point/) | prasa: Glean 300 mln USD, model stała opłata + zużycie |
| [notion.com](https://www.notion.com/pricing) | Notion: Custom Agents 10 USD za 1 000 kredytów |
| [gartner.com](https://www.gartner.com/en/newsroom/press-releases/2026-08-17-gartner-predicts-ai-inference-costs-per-agentic-workflow-will-increase-more-than-fivefold-through-2028) | Gartner, 17.08.2026: koszt na agentowy przepływ ×5 do 2028 |
| [sierra.ai](https://sierra.ai/blog/outcome-based-pricing-for-ai-agents) | Sierra: zasady płatności za wynik (10.12.2024) |
| [sierra.ai](https://sierra.ai/blog/horizon) | Sierra: „płacisz za wyniki, nie za tokeny" |
| [intercom.com](https://www.intercom.com/pricing) | Intercom: Fin 0,99 USD za wynik |
| [parloa.com](https://www.parloa.com/platform/pricing/) | Parloa: rozliczenie za minutę lub interakcję |
| [ambiencehealthcare.com](https://www.ambiencehealthcare.com/blog) | Ambience: kontrakty z premią za wyniki (IV 2026) |
| [sierra.ai](https://sierra.ai/blog/year-two-in-review) | Sierra: ARR 100 → 150 mln+ USD, wąskie „zadania do wykonania" |
| [sacra.com](https://sacra.com/c/openevidence/) | Sacra (analityk): przychody OpenEvidence, CPM, marża |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/OpenEvidence) | encyklopedia: licencjonowane treści NEJM, JAMA, NCCN |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Doximity) | encyklopedia: Doximity finansowany marketingiem farmacji |
| [openclaw.ai](https://openclaw.ai/blog/introducing-openclaw-foundation) | OpenClaw Foundation: 501(c)(3), darczyńcy, „4,5 mln clawów tygodniowo" |
| [openclaw.ai](https://openclaw.ai/blog/openclaw-enterprise) | OpenClaw Enterprise „zawsze darmowy" (29.09.2026) |
| [portal.nousresearch.com](https://portal.nousresearch.com/business) | Nous: Hermes Business i Enterprise |
| [manus.im](https://manus.im/blog/introducing-manus-flex) | Manus Flex: własny klucz do modelu (29.09.2026) |
| [kortix.com](https://www.kortix.com/pricing) | Kortix: kredyty tylko za piaskownicę, BYOK |
| [openhands.dev](https://openhands.dev/pricing) | OpenHands: modele „po kosztach, bez marży" |
| [agent-zero.ai](https://www.agent-zero.ai/p/token/) | Agent Zero: token A0T jako finansowanie |
| [github.com](https://github.com/HKUDS/nanobot) | nanobot: linki partnerskie do dostawców modeli |
| [vaquill.ai](https://www.vaquill.ai/blog/harvey-ai-review-honest-assessment) | szacunek zewnętrzny: cena stanowiska Harvey |
| [layer3labs.io](https://www.layer3labs.io/guides/legora-pricing) | szacunek zewnętrzny: cena stanowiska Legora |
| [sacra.com](https://sacra.com/c/abridge/) | Sacra: Abridge ok. 2 500 USD za lekarza rocznie, ARR |
| [legal.thomsonreuters.com](https://legal.thomsonreuters.com/en/products/cocounsel-legal/plans) | Thomson Reuters: CoCounsel w pakietach z Westlaw |
| [lawnext.com](https://www.lawnext.com/2026/04/clio-work-clios-ai-workspace-is-now-available-to-solo-and-smaller-law-firms-as-a-standalone-product.html) | LawSites: Clio Work 199 USD za użytkownika |
| [bluej.com](https://www.bluej.com/pricing) | Blue J: 1 498 USD rocznie |
| [microsoft.com](https://www.microsoft.com/en-us/microsoft-365-copilot/pricing) | Microsoft: Copilot Business 18–21 USD |
| [github.com](https://github.com/openclaw/openclaw) | GitHub: repozytorium OpenClaw (gwiazdki, zgłoszenia bezpieczeństwa przez API 11.10.2026) |
| [anthropic.com](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation) | Anthropic: seria G 30 mld przy 380 mld, run-rate 14 mld, Claude Code >2,5 mld (12.02.2026) |
| [itiger.com](https://www.itiger.com/hans/news/1183910360) | prasa wtórna: run-rate Anthropic ok. 44 mld USD (V 2026, SemiAnalysis) |
| [mobihealthnews.com](https://www.mobihealthnews.com/news/abridge-secures-300m-boosts-valuation-53b) | prasa: Abridge seria E przy 5,3 mld |
| [fortune.com](https://fortune.com/2026/06/11/abridge-operating-system-medicine-nvidia-eli-lilly-artsight/) | prasa: Abridge jako „platforma", skala klientów (VI 2026) |
| [harvey.ai](https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence) | Harvey: 550 mln przy 15,5 mld, 80% Am Law 100 (9.09.2026) |
| [itbrief.co.uk](https://itbrief.co.uk/story/harvey-launches-500-legal-ai-agents-builder-tool) | prasa: Harvey 1 500 organizacji, 100k+ prawników (V 2026) |
| [raising.fi](https://raising.fi/news/harvey-undisclosed-september-2026) | prasa wtórna: Harvey ARR >400 mln USD (IX 2026) |
| [nousresearch.com](https://nousresearch.com/a-note-on-our-fundraise) | Nous: 90 mln USD, „24 mln klonów", „2,5% tokenów" (X 2026) |
| [github.com](https://github.com/NousResearch/hermes-agent) | GitHub: repozytorium Hermes Agent |
| [manus.im](https://manus.im/blog/manus-100m-arr) | Manus: 100 mln USD ARR, 147 bln tokenów, 80 mln komputerów (XII 2025) |
| [sacra.com](https://sacra.com/c/manus) | Sacra: Manus ok. 450 mln annualizowane (VI 2026), odkupienie udziałów |
| [techcrunch.com](https://techcrunch.com/2026/10/08/chinas-manus-raises-over-500m-in-first-funding-round-since-split-with-meta/) | prasa: runda Manusa >500 mln USD (8.10.2026) |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/ChatGPT) | encyklopedia: 900 mln tygodniowych użytkowników (II 2026) |
| [blog.google](https://blog.google/innovation-and-ai/products/gemini-app/one-billion-monthly-users/) | Google: Gemini 1 mld+ miesięcznie (11.08.2026) |
| [bloomberg.com](https://www.bloomberg.com/news/articles/2026-03-02/cursor-recurring-revenue-doubles-in-three-months-to-2-billion) | prasa: Cursor ARR 2 mld USD |
| [cursor.com](https://cursor.com/blog/joining-spacex) | Cursor: dołączenie do SpaceX |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Cursor_%28company%29) | encyklopedia: harmonogram transakcji SpaceX, ARR 3 mld (V 2026) |
| [thenextweb.com](https://thenextweb.com/news/granola-series-c-meeting-ai-enterprise-context) | prasa: Granola seria C 125 mln przy 1,5 mld |
| [arr.club](https://www.arr.club/granola/granola-arr-grow-at-250-in-q1-2026) | agregator: wzrost ARR Granoli w I kw. 2026 |
| [techcrunch.com](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/) | prasa: Sierra 950 mln przy >15 mld |
| [rutlandherald.com](https://www.rutlandherald.com/news/business/openevidence-raises-250-million-to-build-medical-superintelligence-for-doctors/article_0960939c-ca41-5321-8417-54f84800ece6.html) | prasa: OpenEvidence 250 mln przy 12 mld |
| [felicis.com](https://felicis.com/blog/browser-use-the-tool-making-it-easier-for-ai-agents-to-navigate-websites-raises-17m) | Felicis: seed browser-use 17 mln USD |
| [github.com](https://github.com/browser-use/browser-use) | GitHub: repozytorium browser-use |
| [noxtua.com](https://www.noxtua.com/news/press-releases/series-c) | Noxtua: seria C 100+ mln EUR, 30 000+ użytkowników |
| [techcrunch.com](https://techcrunch.com/2025/04/22/noxtua-raises-92m-for-its-sovereign-ai-tuned-for-the-german-legal-system/) | prasa: Noxtua seria B 92,2 mln USD |
| [beck-noxtua.pl](https://www.beck-noxtua.pl/) | Beck-Noxtua: 590 zł netto, wymóg Legalis Silver, certyfikaty |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Perplexity_AI) | encyklopedia: wycena Perplexity ok. 20 mld (IX 2025) |
| [thenextweb.com](https://thenextweb.com/news/legora-just-hit-100-million-in-revenue-it-took-18-months) | prasa: Legora 100 mln ARR w 18 miesięcy, finansowanie |
| [runtimewire.com](https://runtimewire.com/article/legora-funding-talks-8-5-billion-valuation) | prasa wtórna: Legora >200 mln ARR, rozmowy o wycenie |
| [aol.com](https://www.aol.com/articles/genspark-unveils-ai-workspace-6-150700000.html) | prasa: Genspark ok. 250 mln ARR |
| [finance.yahoo.com](https://finance.yahoo.com/technology/ai/articles/genspark-ai-extends-series-b-131000248.html) | prasa: Genspark 485 mln przy 2,6 mld (17.06.2026) |
| [microsoft.com](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast) | Microsoft IR: 30 mln+ płatnych stanowisk Copilota |
| [getpanto.ai](https://www.getpanto.ai/blog/github-statistics) | źródło wtórne: 4,7 mln płatnych GitHub Copilot |
| [cognition.com](https://cognition.com/blog/1b-run-rate) | Cognition: run-rate 1 mld USD (25.09.2026) |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Cognition_AI) | encyklopedia: wyceny Cognition, historia Windsurf |
| [vktr.com](https://www.vktr.com/ai-platforms/lovable-raises-400-million-at-133-billion-valuation/) | prasa: Lovable 400 mln przy 13,3 mld |
| [hlth.com](https://hlth.com/insights/news/heidi-raises-340m-to-expand-clinical-ai-into-supervised-agentic-workflows) | prasa: Heidi ARR 50 mln, runda 340 mln (IX 2026) |
| [heidihealth.com](https://www.heidihealth.com/blog/heidi-series-b) | Heidi: seria B (X 2025) |
| [cognition.com](https://cognition.com/blog/interaction) | Cognition: przejęcie Poke, >100 mln wiadomości |
| [techcrunch.com](https://techcrunch.com/2026/04/08/poke-makes-ai-agents-as-easy-as-sending-a-text/) | prasa: Poke 300 mln po rundzie, „przepisy", wynagrodzenie twórców |
| [mistral.ai](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/) | Mistral: 3 mld EUR przy >21 mld |
| [techcrunch.com](https://techcrunch.com/2026/02/13/coheres-240m-year-sets-stage-for-ipo/) | prasa: Cohere ARR 240 mln USD (2025) |
| [techcrunch.com](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/) | prasa: Cohere + Aleph Alpha, 20 mld, Schwarz 600 mln |
| [thelogic.co](https://thelogic.co/news/clio-series-g-5-billion-legal-tech) | prasa: Clio kupuje vLex za 1 mld, seria G |
| [finance.yahoo.com](https://finance.yahoo.com/news/meta-acquire-chinese-startup-manus-233905821.html) | prasa: Meta przejmuje Manus (XII 2025) |
| [techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/) | prasa: Steinberger w OpenAI |
| [anthropic.com](https://www.anthropic.com/news/acquires-vercept) | Anthropic: przejęcie Vercept |
| [techcrunch.com](https://techcrunch.com/2026/03/10/meta-acquired-moltbook) | prasa: Meta kupuje Moltbook |
| [cohere.com](https://cohere.com/blog/cohere-and-aleph-alpha-sign-agreement) | Cohere: umowa z Aleph Alpha (16.09.2026) |
| [techcrunch.com](https://techcrunch.com/2026/04/27/china-vetoes-metas-2b-manus-deal-after-months-long-probe/) | prasa: NDRC blokuje przejęcie Manusa (27.04.2026) |
| [dahuilawyers.com](https://www.dahuilawyers.com/en/news-insights/chinas-first-public-foreign-investment-security-review-prohibition-the-metamanus-decision/) | kancelaria: pierwszy publiczny zakaz w chińskim przeglądzie bezpieczeństwa |
| [manus.im](https://manus.im/blog/a-note-to-our-users) | Manus: niezależność, usunięcie danych, dane w USA i Singapurze |
| [manus.im](https://manus.im/blog/manus-resumes-independent-operations) | Manus: formalna niezależność (1.09.2026) |
| [thenextweb.com](https://thenextweb.com/news/tandem-health-100m-series-b-scaleup-europe-fund) | prasa: Tandem 100 mln z Scaleup Europe Fund, MDR IIa |
| [openclaw.ai](https://openclaw.ai/blog/microsoft-autopilot-openclaw) | OpenClaw: Microsoft Autopilot na OpenClaw (25.09.2026) |
| [sierra.ai](https://sierra.ai/blog/introducing-personal-agent-protocol) | Sierra: Personal Agent Protocol z Metą (6.10.2026) |
| [blog.google](https://blog.google/products-and-platforms/products/chrome/gemini-in-chrome-android-auto-browse/) | Google: auto browse w Chrome na Androidzie (18.08.2026) |
| [eu.36kr.com](https://eu.36kr.com/en/p/3931781634260099) | prasa: przeglądarki AI <1% rynku, Chrome ok. 2/3 (VIII 2026) |
| [techcrunch.com](https://techcrunch.com/2026/06/04/apple-approves-poke-as-the-first-ai-agent-on-its-messages-for-business-platform/) | prasa: Poke pierwszym agentem na Apple Messages for Business |
| [docs.openclaw.ai](https://docs.openclaw.ai/llms.txt) | dokumentacja OpenClaw: lista komunikatorów w bramce |
| [hlth.com](https://hlth.com/insights/news/epic-releases-native-ai-charting-for-integrated-clinical-documentation-2026-02-06) | prasa: Epic AI Charting (II 2026) |
| [lexisnexis.com](https://www.lexisnexis.com/community/pressroom/b/news/posts/legal-ai-propels-lexisnexis-to-fastest-growth-in-history) | LexisNexis: AI to 90% nowej sprzedaży |
| [prawo.pl](https://www.prawo.pl/prawnicy-sady/wolters-kluwer-przejmuje-libre-dostawce-rozwiazan-ai-dla-prawnikow,535867.html) | prasa: Wolters Kluwer i treści prawnicze w Polsce |
| [harvey.ai](https://www.harvey.ai/blog/post-training-update-harvey-tenet) | Harvey: Tenet na Kimi K3, koszt ok. 1/10 |
| [cursor.com](https://cursor.com/blog/composer-2) | Cursor: Composer 2, ceny i wyniki |
| [gigazine.net](https://gigazine.net/gsc_news/en/20260323-cursor-admits-composer-2-kimi) | prasa: Composer 2 zbudowany na Kimi K2.5 |
| [lawnext.com](https://www.lawnext.com/2026/08/thomson-reuters-says-its-homegrown-ai-model-now-rivals-the-frontier-labs-i-take-a-closer-look-at-the-benchmarks.html) | LawSites: model „Thomson" na otwartej bazie |
| [noxtua.com](https://www.noxtua.com/) | Noxtua: progi Athena (otwarte modele) i Minerva |
| [bandt.com.au](https://www.bandt.com.au/canva-slashes-revenue-forecast-due-to-ai-spend-being-higher-than-expected/) | prasa: Canva tnie prognozę przez koszty AI, własne modele 17–30× tańsze |
| [harvey.ai](https://www.harvey.ai/blog/building-harveys-mcp-policy-engine) | Harvey: MCP Policy Engine |
| [dgft.nhs.uk](https://www.dgft.nhs.uk/newspost/nhs-launches-largest-ever-procurement-of-ai-clinical-documentation-covering-70000-midlands-clinicians/) | NHS: ramówka na 70 000 klinicystów |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Rabbit_r1) | encyklopedia: Rabbit r1, sprzedaż, wycieki kluczy |
| [theverge.com](https://www.theverge.com/2024/9/25/24254253/rabbit-r1-5000-daily-users-ai-gadget) | prasa: ok. 5 000 aktywnych z ~100 000 właścicieli r1 |
| [techcrunch.com](https://techcrunch.com/2025/05/05/11x-ceo-hasan-sukkar-steps-down/) | prasa: 11x, fałszywe logotypy, odejście CEO |
| [techcrunch.com](https://techcrunch.com/2026/01/07/yes-linkedin-banned-ai-agent-startup-artisan-but-now-its-back/) | prasa: ban Artisan na LinkedIn |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Replit) | encyklopedia: agent Replit usunął produkcyjną bazę (VII 2025) |
| [uctoday.com](https://uctoday.com/productivity-automation/otter-ai-fails-to-dismiss-core-privacy-claims-in-u-s-court/) | prasa: zarzuty wobec Otter przetrwały (13.08.2026) |
| [ppc.land](https://ppc.land/granola-sued-for-recording-meetings-without-consent-to-train-ai-models/) | prasa: pozew przeciw Granoli (30.07.2026) |
| [insiderllm.com](https://insiderllm.com/guides/openclaw-clawhub-security-alert/) | źródło wtórne: audyty złośliwych umiejętności w ClawHub |
| [theregister.com](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) | prasa: OpenClaw 2.0, nieszyfrowane sekrety, piaskownica wyłączona |
| [lindy.ai](https://www.lindy.ai/blog/imessage-api-three-rewrites-one-apple-ban-and-what-actually-works) | Lindy: ban Apple ID na iMessage |
| [community.openai.com](https://community.openai.com/t/atlas-is-scheduled-to-stop-working-on-august-9-2026/1389473) | forum OpenAI: Atlas przestaje działać 9.08.2026 |
| [techcrunch.com](https://techcrunch.com/2026/07/09/openai-is-shutting-down-atlas-but-its-ai-browser-ambitions-are-still-growing/) | prasa: zamknięcie Atlasa ogłoszone 9.07.2026 |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Project_Mariner) | encyklopedia: koniec Project Mariner 4.05.2026 |
| [trymartin.com](https://www.trymartin.com/blog) | Martin: ostatni wpis 23.04.2025 (zastój) |
| [embracethered.com](https://embracethered.com/blog/posts/2025/manus-ai-kill-chain-expose-port-vs-code-server-on-internet/) | blog bezpieczeństwa: wstrzyknięcie przez PDF w Manusie |
| [promptarmor.com](https://www.promptarmor.com/resources/claude-cowork-exfiltrates-files) | blog bezpieczeństwa: wyciek plików w Claude Cowork |
| [damiencharlotin.com](https://www.damiencharlotin.com/hallucinations/) | baza spraw z halucynacjami AI (10.10.2026) |
| [lindy.ai](https://www.lindy.ai/blog/ai-teammate) | Lindy: zwrot w stronę „kolegi w Slacku" (31.08.2026) |
| [claude.com](https://claude.com/resources/articles/how-people-are-using-claude-cowork) | Anthropic: do czego ludzie używają Cowork (VII 2026) |
| [techcrunch.com](https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/) | prasa: ChatGPT dots |
| [manus.im](https://manus.im/blog/introducing-manus-2-0) | Manus 2.0: Cloud Computer, automatyzacje (28.09.2026) |
| [support.google.com](https://support.google.com/gemini/answer/16596215) | Google: Gemini Spark, 15 zadań, wyłączenie EOG |
| [blog.cloudflare.com](https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/) | Cloudflare: „fala kupowania Mac minis" (I 2026) |
| [techcrunch.com](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/) | prasa: Ghost, komputer AI za 3 499 USD |
| [huggingface.co](https://huggingface.co/Qwen/Qwen3.8-27B) | karta modelu: Qwen3.8-27B 84,3% OSWorld-Verified (dane firmy) |
| [digital-strategy.ec.europa.eu](https://digital-strategy.ec.europa.eu/en/policies/cloud-and-ai-development-act) | Komisja Europejska: projekt CADA i poziomy suwerenności |
| [learn.microsoft.com](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) | Microsoft docs: EU Data Boundary bez modeli Anthropic |
| [theregister.com](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/) | prasa: Gartner zaleca blokowanie przeglądarek AI (8.12.2025) |
| [techcrunch.com](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/) | prasa: OpenAI o trwałości wstrzykiwania poleceń |
| [bankinfosecurity.com](https://www.bankinfosecurity.com/akamai-to-buy-layerx-for-205m-to-expand-ai-browser-security-a-31695) | prasa: Akamai kupuje LayerX za ok. 205 mln USD |
| [jonesday.com](https://www.jonesday.com/en/insights/2026/09/ninth-circuit-vacates-cfaa-injunction-against-perplexitys-comet-ai-agent) | kancelaria: Amazon przeciw Perplexity, uchylenie zakazu (4.08.2026) |
| [business-standard.com](https://www.business-standard.com/world-news/bytedance-ai-phone-doubao-nubia-zte-app-blocks-user-control-china-125120800459_1.html) | prasa: blokada agenta Doubao w chińskich aplikacjach |
| [techcrunch.com](https://techcrunch.com/2026/05/12/the-ai-legal-services-industry-is-heating-up-anthropic-is-getting-in-on-the-action/) | prasa: Claude for Legal (12.05.2026) |
| [lawnext.com](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html) | LawSites: nowy CoCounsel na Claude Agent SDK |
| [noxtua.com](https://www.noxtua.com/news/press-releases/beck-noxtua-for-the-czech-republic) | Noxtua: hosting Beck-Noxtua na IONOS i Open Telekom Cloud |
| [apps.apple.com](https://apps.apple.com/pl/app/lex-ai/id6748342467?l=pl) | App Store: ceny LEX AI 49/120/489 zł, serwery w Polsce |
| [noa.ai](https://www.noa.ai/pl/cennik) | Noa: Noa Notes 199 zł + VAT |
| [wfirma.pl](https://wfirma.pl/) | wFirma: funkcje AI w cenie abonamentu |
| [gaius-lex.pl](https://gaius-lex.pl/) | Gaius-Lex: Gaius Vault on-premise, brak cennika |
| [manus.im](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) | Manus: stosunek tokenów 100:1, ok. 50 wywołań na zadanie, cache ok. 10× taniej |
| [anthropic.com](https://www.anthropic.com/news/claude-opus-5-5) | Anthropic: ceny Opus 5.5 4/20 USD za mln tokenów |
| [simular.ai](https://www.simular.ai/articles/sai-tops-osworld-2-0) | Simular: koszt długich zadań OSWorld 2.0 (dane firmy) |
| [stat.gov.pl](https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultaktualnosci/5497/1/19/1/spoleczenstwo_informacyjne_w_polsce_2025.pdf) | GUS: 8,7% firm z AI, 23,2% w usługach profesjonalnych (2025) |
| [ec.europa.eu](https://ec.europa.eu/eurostat/statistics-explained/index.php/Use_of_artificial_intelligence_in_enterprises) | Eurostat: AI w firmach UE 19,95%, bariery adopcji (2025) |
| [pie.net.pl](https://pie.net.pl/wp-content/uploads/2025/09/2025-09-22_Z-AI-korzysta-mniej-niz-co-szosta-firma-w-Polsce-a-pozostale-nie-planuja-jej-wdrazac-1.pdf) | PIE: 77% firm bez AI nie wdroży „dopóki nie trzeba" |
| [stackoverflow.co](https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/) | Stack Overflow 2025: zaufanie do AI 26% w Polsce |
| [ceneo.pl](https://www.ceneo.pl/;szukaj-radeon+ai+pro+r9700) | ceny Radeon AI PRO R9700 w Polsce, ok. 8 900 zł (11.10.2026) |
| [amd.com](https://www.amd.com/en/products/graphics/workstations/radeon-ai-pro/ai-9000-series/amd-radeon-ai-pro-r9700.html) | AMD: R9700, 300 W TBP |
| [ceneo.pl](https://www.ceneo.pl/;szukaj-ascent+gx10) | ASUS Ascent GX10 od 24 499 zł (11.10.2026) |
| [apple.com](https://www.apple.com/pl/shop/buy-mac/mac-mini) | Mac mini M5 Pro od 8 499 zł |
| [ceneo.pl](https://www.ceneo.pl/;szukaj-ryzen+ai+max%2B+395+128gb) | mini PC Strix Halo 128 GB, 13 490–19 999 zł |

## Wzorce techniczne (03-WZORCE-TECHNICZNE.md)

Sprawdzone przez zespół researchu 11.10.2026 (pliki `research/2–6`); dane firm oznaczone w tekście *(dane firmy)*.

| Źródło | Co wziąłem |
|---|---|
| [Manus: Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) | sześć reguł kontekstu, KV-cache jako główna metryka, `todo.md`, stosunek wejścia do wyjścia ~100:1 |
| [Manus: Browser Operator](https://manus.im/blog/manus-browser-operator) · [Cloud Browser](https://manus.im/docs/features/cloud-browser.md) | lokalna przeglądarka jako aktuator, logowanie każdej akcji, „Take Over", bankowość przez lokalną przeglądarkę |
| [E2B: jak Manus używa E2B](https://e2b.dev/blog/how-manus-uses-e2b-to-provide-agents-with-virtual-computers) | mikro-VM Firecracker ~150 ms, rezygnacja z Dockera |
| [Harvey: multi-model by design](https://www.harvey.ai/en-US/blog/why-harvey-is-multi-model-by-design) | routing po zadaniu, przełączanie przy awarii, lista modeli administratora, BigLaw Bench |
| [Harvey: Tenet](https://www.harvey.ai/blog/post-training-update-harvey-tenet) | Kimi K3 + RL, bez danych klientów, koszt komórki ~1/10, −90% na zapytaniu |
| [Harvey II](https://www.harvey.ai/blog/introducing-harvey-ii) | „Spaces" sprawy |
| [Harvey: MCP Policy Engine](https://www.harvey.ai/blog/building-harveys-mcp-policy-engine) | „śmiertelna trójca", przypinanie narzędzi, Rego, sanitizer Unicode poza modelem |
| [Google: architektura bezpieczeństwa agenta w Chrome](https://blog.google/security/architecting-security-for-agentic/) | krytyk zgodności z celem, Agent Origin Sets, deterministyczne potwierdzenia, dziennik pracy |
| [Gemini API: computer use](https://ai.google.dev/gemini-api/docs/computer-use) | `safety_decision`, 7 kategorii polityk |
| [Google: Gemini Spark](https://support.google.com/gemini/answer/16596215) | oddawanie logowania i płatności, niedostępność w EOG |
| [Google: CC](https://blog.google/technology/google-labs/cc-ai-agent/) | codzienny e-mail jako interfejs |
| [OpenClaw: Microsoft Autopilot](https://openclaw.ai/blog/microsoft-autopilot-openclaw) | kontrola zgodności z polityką, maskowanie sekretów w zatwierdzeniach, „nieznany wynik — bez ponowienia" |
| [OpenClaw docs: heartbeat](https://docs.openclaw.ai/gateway/heartbeat) · [standing orders](https://docs.openclaw.ai/automation/standing-orders) · [dreaming](https://docs.openclaw.ai/concepts/dreaming) · [workspace](https://docs.openclaw.ai/concepts/agent-workspace) · [local models](https://docs.openclaw.ai/gateway/local-models) · [indeks](https://docs.openclaw.ai/llms.txt) | puls co 30 min i limity wybudzeń, kontrakt programu, pamięć w plikach, brak twardej piaskownicy, praca offline, kanały |
| [OpenClaw: security in public](https://openclaw.ai/blog/openclaw-security-in-public) · [ClawScan](https://openclaw.ai/blog/tencent-aig-joins-clawscan) | statystyka zgłoszeń (1 309 / 746 / 87%), skanowanie umiejętności |
| [The Register: OpenClaw 2.0](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) | piaskownica nadal nie domyślna |
| [Cisco: OpenClaw security nightmare](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare) | 26% z 31 000 umiejętności z podatnością, eksfiltracja przez `curl` |
| [Hermes docs: memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) · [skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) | limity 2 200 / 1 375 znaków, zamrożona migawka, umiejętności skanowane przy instalacji |
| [OpenHands: condenser](https://openhands.dev/blog/openhands-context-condensensation-for-more-efficient-ai-agents) · [runtime](https://docs.openhands.dev/usage/architecture/runtime) · [security](https://docs.openhands.dev/sdk/guides/security) | kondensacja kontekstu, strumień zdarzeń, `ConfirmRisky` i analizatory ryzyka |
| [digitalapplied: ChatGPT Work](https://www.digitalapplied.com/blog/chatgpt-work-openai-agent-launch-2026) | „Plan mode" jako granica zgody |
| [Decrypt: DevDay 2026](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced) | otwarcie harnessu Codex |
| [TechCrunch: ChatGPT Pulse](https://techcrunch.com/2025/09/25/openai-launches-chatgpt-pulse-to-proactively-write-you-morning-briefs/) | nocny brief |
| [Claude: browser use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) · [computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) | drzewo dostępności, referencje elementów, koszt zrzutu 1 000–1 800 tokenów |
| [Simon Willison: Claude Cowork](https://simonwillison.net/2026/Jan/12/claude-cowork/) | lokalna VM, montowanie wybranych folderów |
| [PromptArmor: Cowork exfiltration](https://www.promptarmor.com/resources/claude-cowork-exfiltrates-files) | eksfiltracja przez dozwolone API |
| [Claude for Chrome](https://claude.com/blog/claude-for-chrome) · [Anthropic: prompt injection defenses](https://www.anthropic.com/research/prompt-injection-defenses) | potwierdzenia przed publikacją i zakupem; 23,6% → 11,2%, ~1% dla Opus 4.5 |
| [Claude: pamięć](https://claude.com/resources/articles/claudes-memory-works-everywhere-and-you-decide-whats-in-it) | pamięć w plikach tematycznych, tematy wrażliwe domyślnie niezapisywane |
| [Claude Code: data usage](https://code.claude.com/docs/en/data-usage) | poświadczenia poza VM, proxy ruchu |
| [browser-use: ain.ua](https://en.ain.ua/2025/03/25/browser-use-raises-17m) · [changelog CDP](https://browser-use.com/changelog/19-8-2025) · [changelog Agency](https://browser-use.com/changelog/3-4-2026) · [docs](https://docs.browser-use.com/cloud/choosing-an-agent) · [BU 2.0](https://docs.browser-use.com/open-source/bu-2-0-model-card) · [raport WebVoyager](https://browser-use.com/posts/sota-technical-report) | „tekst najpierw", CDP, zatwierdzenia tylko przed akcją zewnętrzną, secret bindings, funkcje tylko w chmurze, 89,1% po usunięciu 55 zadań |
| [HAL: Online-Mind2Web](https://hal.cs.princeton.edu/online_mind2web) | niezależne 40,0% dla browser-use + Sonnet 4 |
| [UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) · [UI-TARS-1.5-7B](https://huggingface.co/ByteDance-Seed/UI-TARS-1.5-7B) | model wizyjny GUI, hybryda GUI + DOM, przeglądarka zdarzeń, ~27,5% OSWorld dla 7B |
| [Agent S](https://github.com/simular-ai/Agent-S) | osobny model „gdzie kliknąć", wybór najlepszego przebiegu, 72,6% OSWorld |
| [MSR: Fara-7B](https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/) | trening małego modelu na syntetycznych trajektoriach |
| [Microsoft: agent workspace](https://support.microsoft.com/en-us/windows/experimental-agentic-features-a25ede8a-e4c2-4841-85a8-44839191dfb3) | osobne konto Windows dla agenta, sześć folderów |
| [Microsoft 365 Copilot: prywatność](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) | modele Anthropic poza EU Data Boundary |
| [Jones Day: Amazon v. Perplexity](https://www.jonesday.com/en/insights/2026/09/ninth-circuit-vacates-cfaa-injunction-against-perplexitys-comet-ai-agent) | wykonanie lokalne, rozumowanie w chmurze w Comet |
| [the-decoder: BrowseSafe](https://the-decoder.com/perplexitys-browsesafe-tries-to-patch-the-gaping-security-holes-inherent-in-ai-browser-agents/) | 91% wykrywalności, ~10% ataków przechodzi |
| [TechCrunch: Perplexity Computer](https://techcrunch.com/2026/02/27/perplexitys-new-computer-is-another-bet-that-users-need-many-ai-models/) | 19 modeli z podagentami |
| [NVIDIA NemoClaw](https://github.com/NVIDIA/NemoClaw) · [NanoClaw](https://github.com/nanocoai/nanoclaw) | piaskownica domyślnie i akceptacja egress; kontener na agenta, bramki skryptowe, bramka poświadczeń |
| [Kortix README](https://raw.githubusercontent.com/kortix-ai/suna/main/README.md) | broker poświadczeń z jednym tokenem |
| [Lindy: cennik](https://www.lindy.ai/pricing) · [Lindy: iMessage](https://www.lindy.ai/blog/imessage-api-three-rewrites-one-apple-ban-and-what-actually-works) | zatwierdzenia wg wpływu na zewnątrz; blokada Apple ID, stosunek ~10:1 |
| [TechCrunch: Poke przepisy](https://techcrunch.com/2026/04/08/poke-makes-ai-agents-as-easy-as-sending-a-text/) · [TechCrunch: Poke w Apple Messages](https://techcrunch.com/2026/06/04/apple-approves-poke-as-the-first-ai-agent-on-its-messages-for-business-platform/) · [Cognition](https://cognition.com/blog/interaction) | przepisy tekstowe, pierwszy agent w Messages for Business, >100 mln wiadomości |
| [LexisNexis: Protégé](https://www.lexisnexis.com/community/pressroom/b/news/posts/lexis-with-protege-accelerates-frictionless-agentic-productivity-from-first-idea-to-review-ready-legal-work-product) | umiejętności partnerów, klientów „wkrótce" |
| [Spellbook](https://www.spellbook.com/press) · [LawNext: Spellbook](https://www.lawnext.com/2025/08/spellbook-becomes-one-of-the-first-legal-ai-platforms-to-launch-gpt-5.html) | wtyczka Word; odsetek przyjętych sugestii jako metryka |
| [Noxtua](https://www.noxtua.com/) · [Noxtua security](https://www.noxtua.com/security) | Athena / Minerva, suwerenna chmura UE, wtyczki Word i Outlook |
| [Nabla: niezawodność STT](https://nabla.com/blog/assessing-the-reliability-of-nablas-speech-to-text-engine) | Whisper + 7 000 h audio medycznego, surowa transkrypcja nie trafia do dokumentacji |
| [Abridge: confabulation elimination](https://www.abridge.com/ai/science-confabulation-hallucination-elimination) | Linked Evidence, strażnik 97% wobec 82% |
| [Wikipedia: OpenEvidence](https://en.wikipedia.org/wiki/OpenEvidence) | RAG nad licencjonowaną literaturą z cytatami |
| [Hebbia: Matrix 2.0](https://www.hebbia.com/blog/introducing-matrix-2-0) | interfejs siatki, punkty kontroli człowieka, „widać, skąd każda liczba" |
| [CoCounsel Legal](https://legal.thomsonreuters.com/en/products/cocounsel-legal) | Tabular Analysis 10 000 × 100 |
| [Prawo.pl: LEX Expert AI](https://www.prawo.pl/prawnicy-sady/lex-expert-ai-nowym-narzedziem-dla-prawnikow) | odpowiedzi z linkami do fragmentów LEX |
| [Decagon: Series D](https://decagon.ai/blog/series-d-announcement) | Agent Operating Procedures |
| [Basis: behavior specs](https://www.getbasis.ai/blogs/behavior-specs-an-open-standard-for-supervising-long-horizon-agents) | ocena trajektorii, specyfikacje ukryte przed agentem |
| [Sierra: τ-bench](https://sierra.ai/blog/benchmarking-ai-agents) | pass^k, spadek do ~25% przy pass^8 |
| [Cursor: Composer 2](https://cursor.com/blog/composer-2) · [Gigazine](https://gigazine.net/gsc_news/en/20260323-cursor-admits-composer-2-kimi) · [Cursor: data use](https://cursor.com/data-use) | otwarta baza Kimi, nieujawniona przy premierze; zapytania przez backend |
| [itbrief: Glean Tau](https://itbrief.asia/story/glean-launches-tau-to-cut-enterprise-ai-token-costs) | routing, 0,58 wobec 2,98 USD na zadanie (benchmark producenta) |
| [Granola: transkrypcja](https://docs.granola.ai/help-center/taking-notes/transcription) · [Startup Fortune](https://startupfortune.com/granola-ai-meeting-notes-are-not-as-private-as-you-might-think/) · [ppc.land](https://ppc.land/granola-sued-for-recording-meetings-without-consent-to-train-ai-models/) | dwa kanały „Ja / Oni", brak zapisu audio; domyślne udostępnianie i trening; pozew *Chamberlain v. Granola* |
| [TechCrunch: Ghost](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/) | zapora wyjścia jako funkcja zaufania |
| [Brave: Comet prompt injection](https://brave.com/blog/comet-prompt-injection/) | przyczyna strukturalna, same-origin nie chroni |
| [TechCrunch: OpenAI o prompt injection](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/) · [The Register: Gartner](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/) | „mało prawdopodobne, by został w pełni rozwiązany"; zalecenie blokady przeglądarek AI |
| [The Register: Comet kalendarz](https://www.theregister.com/2026/03/03/perplexity_comet_browser_hole_cal_invite/) · [BleepingComputer: BragJack](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/) | atak bez kliknięcia; „wymuszanie promptu" w pięciu produktach |
| [ComplexDiscovery](https://complexdiscovery.com/ninth-circuit-vacates-amazon-injunction-ai-agent-logs-emerge-as-ediscovery-issue/) | dzienniki agenta jako dowód (tylko tytuł) |
| [NRA: § 23e ZZEA](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/) | osobista weryfikacja, „należyta ochrona", wskazanie narzędzi na prośbę klienta |
| [RODO](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | art. 28, rozdział V, art. 32, art. 33–34, motyw 26 |
| [EDPB: AI Privacy Risks – LLMs](https://www.edpb.europa.eu/our-work-tools/our-documents/support-pool-experts-projects/ai-privacy-risks-mitigations-large_pt) | ryzyko ponownej identyfikacji |
| [18 U.S.C. § 2713](https://www.law.cornell.edu/uscode/text/18/2713) | CLOUD Act |
| [UODO, 26.06.2026](https://uodo.gov.pl/pl/138/4449) | „regularnie mierzyć i testować wdrożone środki bezpieczeństwa" |
| [PLCC](https://huggingface.co/spaces/sdadas/plcc) · [CPTUB](https://huggingface.co/spaces/speakleash/cptu_bench) | polskie testy akceptacyjne; najlepszy otwarty 89,83 wobec 92–97 |
| [arXiv 2609.32042: PolAgentBench](https://arxiv.org/abs/2609.32042) | klif między 3 a 2 bitami w zadaniach agentowych |
| [arXiv 2608.30929](https://arxiv.org/abs/2608.30929) · [arXiv 2511.04205](https://arxiv.org/abs/2511.04205) · [arXiv 2606.12250](https://arxiv.org/abs/2606.12250) · [arXiv 2608.12928](https://arxiv.org/abs/2608.12928) | wyszukiwanie przepisów 72,3% / BM25 61,7%; egzamin KIO; −31 pp na egzaminach medycznych; słaba wizja w polskich pytaniach medycznych |
| [arXiv 2606.29537: OSWorld 2.0](https://arxiv.org/abs/2606.29537) | 20,6% ukończonych długich zadań, przyczyny porażek |
| [Bielik-11B-v3](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [Bielik-Guard](https://huggingface.co/speakleash/Bielik-Guard-0.5B-v1.1) · [gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) | licencja Apache-2.0, rozmiary, precyzja klasyfikatora 75,28% |
| [Przegląd harnessów: 02-KLOCKI](../harnessy-agentowe/02-KLOCKI.md) · [03-ARCHITEKTURA](../harnessy-agentowe/03-ARCHITEKTURA.md) · [01-PROFILE](../harnessy-agentowe/01-PROFILE.md) | narzędzia lokalne (głos, obraz, piaskownice, kanały), liczby rigu (1 186 tok/s, 13,6 tok/s, 104,2 GB, powtarzalność 83), Moltis, ZeroClaw, OpenCode, Hermes TTS |

## Polska i suwerenność (04-POLSKA-I-SUWERENNOSC.md)

| Źródło | Co wziąłem |
|---|---|
| [18 U.S.C. § 2713 (Cornell LII)](https://www.law.cornell.edu/uscode/text/18/2713) | Treść CLOUD Act: „possession, custody, or control" niezależnie od lokalizacji |
| [EDPB–EDPS, odpowiedź dla LIBE (12.07.2019)](https://www.edpb.europa.eu/sites/default/files/files/file2/edpb_edps_joint_response_us_cloudact_annex.pdf) | Żądanie z CLOUD Act bez umowy międzynarodowej nie jest podstawą z RODO |
| [The Register (25.07.2025)](https://www.theregister.com/2025/07/25/microsoft_admits_it_cannot_guarantee/) | Zeznanie Microsoft France w Senacie: „Non, je ne peux pas le garantir" |
| [Microsoft — European digital commitments](https://blogs.microsoft.com/on-the-issues/2025/04/30/european-digital-commitments/) | Zobowiązania umowne, nie immunitet |
| [RODO (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Art. 9, 10, 28, 32–35, 44–49, 48 |
| [Motyw 91 RODO](https://gdpr-info.eu/recitals/no-91/) | Pojedynczy lekarz lub prawnik to nie „duża skala" — DPIA nieobowiązkowa |
| [CMS o opinii EDPB 28/2024](https://cms.law/en/int/legal-updates/edpb-opinion-28-2024-key-takeaways-on-processing-personal-data-in-the-context-of-ai-models) | Anonimowość modelu i uzasadniony interes |
| [Ustawa o prawach pacjenta (Dz.U. 2024 poz. 581)](https://api.sejm.gov.pl/eli/acts/DU/2024/581/text.pdf) | Art. 13–14 i 24 ust. 2–6: informatycy i procesor związani tajemnicą |
| [Komisja Europejska — transfery UE–USA](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/eu-us-data-transfers_en) | Data decyzji DPF (10.07.2023) |
| [WilmerHale (blog)](https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20251201-european-court-of-justice-to-review-challenge-to-eu-us-data-privacy-framework) | Wyrok T-553/23 Latombe (3.09.2025) |
| [secureprivacy (blog)](https://secureprivacy.ai/blog/is-the-eu-us-data-privacy-framework-at-risk-the-ftc-ruling-explained-2026) | Odwołanie C-703/25 P w toku |
| [Skadden (VII 2026)](https://www.skadden.com/insights/publications/2026/07/supreme-court-decision-raises-new-questions) | Trump v. Slaughter i szacowany termin wyroku TSUE |
| [Microsoft EU Data Boundary](https://blogs.microsoft.com/on-the-issues/2025/02/26/microsoft-completes-landmark-eu-data-boundary-offering-enhanced-data-residency-and-transparency/) | Zakończenie 26.02.2025 i wyjątki |
| [Microsoft Sovereign Cloud](https://blogs.microsoft.com/blog/2025/06/16/announcing-comprehensive-sovereign-solutions-empowering-european-organizations/) | Data Guardian, Azure Local, Bleu, Delos |
| [Copilot — prywatność](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) | Modele Anthropic poza EU Data Boundary |
| [Copilot — cennik](https://www.microsoft.com/en-us/microsoft-365-copilot/pricing) | Business 18 USD/os./mies. |
| [Microsoft FY26 Q4](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast) | 30+ mln płatnych stanowisk Copilota |
| [AWS European Sovereign Cloud](https://press.aboutamazon.com/aws/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe) | GA 15.01.2026, Brandenburgia, personel z UE |
| [S3NS](https://www.s3ns.io/en) i [ANSSI SecNumCloud](https://cyber.gouv.fr/enjeux-technologiques/cloud/) | SecNumCloud 3.2 i ochrona przed prawem eksterytorialnym |
| [OVHcloud AI Endpoints](https://www.ovhcloud.com/en/public-cloud/ai-endpoints/), [STACKIT](https://stackit.com/en/), [IONOS AI Model Hub](https://cloud.ionos.com/managed/ai-model-hub) | Chmury z UE bez spółki matki w USA; ceny tokenów IONOS |
| [Azure — lista regionów](https://learn.microsoft.com/en-us/azure/reliability/regions-list), [OChK](https://ochk.cloud/pl/) | Poland Central; „100% polskie" przy odsprzedaży AI z USA |
| [CADA (Komisja Europejska)](https://digital-strategy.ec.europa.eu/en/policies/cloud-and-ai-development-act) | Poziomy suwerenności L1–L4, status projektu |
| [Prawo o adwokaturze (Dz.U. 2024 poz. 1564)](https://api.sejm.gov.pl/eli/acts/DU/2024/1564/text.pdf) | Art. 6 |
| [NRA — zmiany ZZEA](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/) i [Rzeczpospolita (16.06.2026)](https://www.rp.pl/zawody-prawnicze/art44636171-nra-zmienila-kodeks-etyki-adwokat-moze-korzystac-z-ai-ale-tylko-pomocniczo) | § 23e i § 19 ust. 6 |
| [Ustawa o radcach prawnych (Dz.U. 2024 poz. 499)](https://api.sejm.gov.pl/eli/acts/DU/2024/499/text.pdf) | Art. 3 ust. 3–6 |
| [KIRP — rekomendacje](https://kirp.pl/rekomendacje-dotyczace-korzystania-z-ai/) i [prawo.pl](https://www.prawo.pl/prawnicy-sady/rekomendacje-korzystania-z-ai-dla-radcow-prawnych,532905.html) | 22 rekomendacje, współautorzy, zakres |
| [Ustawa o zawodach lekarza (Dz.U. 2026 poz. 37)](https://api.sejm.gov.pl/eli/acts/DU/2026/37/text.pdf) | Art. 40 |
| [Kodeks Etyki Lekarskiej (NIL)](https://nil.org.pl/uploaded_images/1723037323_kel-2305.pdf) i [blog OSOZ](https://blog.osoz.pl/nowy-kodeks-etyki-lekarskiej-z-niejasnym-zapisem-o-ai) | Art. 12 i krytyka |
| [Ustawa o doradztwie podatkowym (Dz.U. 2026 poz. 1274)](https://api.sejm.gov.pl/eli/acts/DU/2026/1274/text.pdf) | Art. 37 |
| [Rzeczpospolita o KIDP (12.01.2026)](https://www.rp.pl/zawody-prawnicze/art43622191-michna-doradcy-podatkowi-beda-bardziej-widoczni-w-terenie) i [IKiDP (9.08.2026)](https://ikidp.pl/blog/ai-tajemnica-zawodowa-doradcy-podatkowego/) | Weryfikacja wyników AI; ryzyko wklejania dokumentów |
| [Prawo o notariacie (Dz.U. 2026 poz. 614)](https://api.sejm.gov.pl/eli/acts/DU/2026/614/text.pdf) | Art. 18 |
| [Ustawa o biegłych rewidentach (Dz.U. 2025 poz. 1891)](https://api.sejm.gov.pl/eli/acts/DU/2025/1891/text.pdf) | Art. 78 |
| [Kodeks karny (ISAP)](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19970880553) | Art. 266 § 1 |
| [Baza halucynacji Charlotina](https://www.damiencharlotin.com/hallucinations/) | 2 184 sprawy, 6 w Polsce (10.10.2026) |
| [AI Act (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj), [art. 50](https://artificialintelligenceact.eu/article/50/), [art. 6](https://artificialintelligenceact.eu/article/6/), [załącznik III](https://artificialintelligenceact.eu/annex/3/) | Role, przejrzystość, wyjątek art. 6 ust. 3, kategorie wysokiego ryzyka |
| [AI Omnibus (Dz.Urz. UE)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601744), [FPF](https://fpf.org/blog/the-ai-act-implementation-timeline-what-changes-under-the-ai-omnibus/), [Lewis Silkin](https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo) | Kalendarz po Omnibusie, art. 4 i 4a |
| [Wytyczne GPAI (Komisja)](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers) | „Significant modifications" |
| [MDR (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2017/745/oj) | Reguła 11 |
| [Ustawa o systemach SI (Dz.U. 2026 poz. 1003)](https://api.sejm.gov.pl/eli/acts/DU/2026/1003/text.pdf) | Art. 5, 9, 11, 12, 13, 15, 127 (tekst przeczytany) |
| [gdpr.pl](https://gdpr.pl/ustawa-o-systemach-sztucznej-inteligencji-weszla-w-zycie) i [infor.pl](https://www.infor.pl/prawo/nowosci-prawne/7668177,ustawa-o-systemach-sztucznej-inteligencji-od-28-pazdziernika-2026-obowiazki-firm-i-kary-co-to-jest-kribsi.html) | Potwierdzenie dat 11.08 i 28.10.2026 |
| [PLD (Komisja)](https://single-market-economy.ec.europa.eu/single-market/goods/free-movement-sectors/liability-defective-products_en) | Oprogramowanie i AI jako produkt, od 9.12.2026 |
| [CRA (Komisja)](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act) | Zgłaszanie od 11.09.2026, obowiązki od 11.12.2027 |
| [UODO — listy kontrolne](https://uodo.gov.pl/pl/138/4533), [UODO — MyDr](https://uodo.gov.pl/pl/138/4540), [UODO — testowanie zabezpieczeń](https://uodo.gov.pl/pl/138/4449) | Pytania inicjalne (6.08.2026), kontrola MyDr, testowanie środków |
| [Noxtua](https://www.noxtua.com/), [security](https://www.noxtua.com/security), [seria C](https://www.noxtua.com/news/press-releases/series-c), [TechCrunch](https://techcrunch.com/2025/04/22/noxtua-raises-92m-for-its-sovereign-ai-tuned-for-the-german-legal-system/) | Tiery, hosting, użytkownicy, finansowanie |
| [Beck-Noxtua](https://www.beck-noxtua.pl/), [Noxtua PL](https://www.noxtua.com/news/press-releases/beck-noxtua-poland), [Noxtua CZ](https://www.noxtua.com/news/press-releases/beck-noxtua-for-the-czech-republic) | 590 zł netto, Legalis Silver+, IONOS i Open Telekom Cloud |
| [Mistral cennik](https://mistral.ai/fr/pricing), [heise](https://heise.de/-11311685) | Vibe i ceny |
| [Proton Lumo cennik](https://proton.me/lumo/pricing), [prywatność](https://proton.me/support/lumo-privacy), [Help Net Security](https://www.helpnetsecurity.com/2026/07/01/proton-lumo-2-0-ai/) | Cena, szyfrowanie, modele, Lumo 2.0 |
| [Nextcloud AI](https://docs.nextcloud.com/server/latest/admin_manual/ai/index.html), [llm2](https://docs.nextcloud.com/server/latest/admin_manual/ai/app_llm2.html) | Aplikacje AI on-prem i domyślne modele |
| [Cohere North 2](https://cohere.com/blog/introducing-north-2), [TechCrunch (II 2026)](https://techcrunch.com/2026/02/13/coheres-240m-year-sets-stage-for-ipo/), [TechCrunch (IV 2026)](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/) | Air-gap, ARR, połączenie z Aleph Alpha |
| [DeepL Pro](https://www.deepl.com/en/pro), [Langdock](https://www.langdock.com/pricing) | Ceny i hosting |
| [Heidi safety](https://heidihealth.com/safety), [Heidi GDPR](https://www.heidihealth.com/au/compliance/gdpr), [Heidi plany](https://support.heidihealth.com/en/articles/8885129-which-heidi-plan-is-right-for-you) | Brak nagrań, rezydencja UE, ceny |
| [Nabla (Commure, recenzja konkurenta)](https://www.commure.com/blog-scribe/nabla-ai-review), [STAT](https://www.statnews.com/2025/06/17/nabla-raises-70-million-ambient-market-heats-up/) | Audio w przeglądarce, retencja 14 dni, finansowanie |
| [prawo.pl o LEX Expert AI](https://www.prawo.pl/prawnicy-sady/lex-expert-ai-nowym-narzedziem-dla-prawnikow,535918.html), [Wolters Kluwer](https://www.wolterskluwer.com/pl-pl/news/lex-expert-ai-wspiera-specjalistow-ktorzy-nie-sa-prawnikami) | Start 19.11.2025, serwery UE, rozszerzenie 14.07.2026 |
| [Protégé Polska](https://www.lexisnexis.com/de-at/cee/protege-polska) | Oferta w Polsce, tylko demo |
| [Gaius-Lex](https://gaius-lex.pl/), [Legal Technology Hub](https://www.legaltechnologyhub.com/vendors/gaius-lex/), [Signalbase](https://www.trysignalbase.com/news/funding/gaius-lex-secures-5) | On-prem, segment 20–99 prawników, seed |
| [LEX AI (App Store)](https://apps.apple.com/pl/app/lex-ai/id6748342467?l=pl), [lexai.pl](https://lexai.pl/) | Ceny 49/120/489 zł, serwery w Polsce |
| [Noa cennik](https://www.noa.ai/pl/cennik), [Noa Notes](https://noa.ai/pl/noa-notes) | 199 zł + VAT, AWS i Azure, 13 000+ specjalistów |
| [Medidesk](https://www.medidesk.com/), [Comarch ChatERP](https://www.comarch.pl/erp/asystent-ai/), [Comarch AI](https://www.comarch.ai/), [wFirma](https://wfirma.pl/), [inFakt](https://www.infakt.pl/), [SentiOne](https://sentione.com/) | Polski rynek: hosting i podejście do danych |
| [KSeF](https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/podstawy-prawne-oraz-kluczowe-terminy/) | Terminy obowiązku i podstawa prawna |
| [iMagazine o mObywatelu](https://imagazine.pl/2026/01/02/mobywatel-wchodzi-w-2026-rok-z-polskim-ai/) | Asystent na PLLuM bez danych osobowych |
| [Eurostat](https://ec.europa.eu/eurostat/statistics-explained/index.php/Use_of_artificial_intelligence_in_enterprises), [GUS](https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultaktualnosci/5497/1/19/1/spoleczenstwo_informacyjne_w_polsce_2025.pdf), [PIE](https://pie.net.pl/wp-content/uploads/2025/09/2025-09-22_Z-AI-korzysta-mniej-niz-co-szosta-firma-w-Polsce-a-pozostale-nie-planuja-jej-wdrazac-1.pdf) | Adopcja AI w firmach, bariery, sektor usług profesjonalnych |
| [Future Ready Lawyer 2026 (prawo.pl)](https://www.prawo.pl/prawnicy-sady/prawnicy-na-co-dzien-korzystaja-z-ai-a-ai-zmienia-model-ich-zawodu,1540345.html) | 92% prawników używa AI codziennie |
| [NIL — zestawienie (30.06.2026)](https://nil.org.pl/uploaded_files/1783510889_30062026-zestawienie-nr-1.pdf) | Liczba lekarzy i dentystów |
| [Bielik-11B-v3.0](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct), [arXiv 2601.11579](https://arxiv.org/abs/2601.11579), [Minitron-7B](https://huggingface.co/speakleash/Bielik-Minitron-7B-v3.0-Instruct), [Bielik-PL-11B](https://huggingface.co/speakleash/Bielik-PL-11B-v3.0-Instruct), [arXiv 2604.10799](https://arxiv.org/abs/2604.10799), [DFlash](https://huggingface.co/speakleash/Bielik-11B-v3.0-DFlash), [Bielik-Guard](https://huggingface.co/speakleash/Bielik-Guard-0.5B-v1.1) | Rodzina Bielik v3: rozmiary, licencje, APT4 |
| [bielik.ai](https://bielik.ai/), [Ollama SpeakLeash](https://ollama.com/SpeakLeash) | Pobrania, partnerzy (Dell) |
| [PLLuM-12B-chat](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-chat), [250715](https://huggingface.co/CYFRAGOVPL/pllum-12b-nc-chat-250715), [12B-2512](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512), [4B-2512](https://huggingface.co/CYFRAGOVPL/PLLuM-4B-instruct-2512) | Mozaika licencji PLLuM |
| [CPTUB](https://huggingface.co/spaces/speakleash/cptu_bench), [PLCC](https://huggingface.co/spaces/sdadas/plcc), [Polish Medical Leaderboard](https://huggingface.co/spaces/speakleash/polish_medical_leaderboard) | Wyniki polskich benchmarków z datą danych |
| [Qwen3.5-27B](https://huggingface.co/Qwen/Qwen3.5-27B), [Gemma 4 31B](https://huggingface.co/google/gemma-4-31B-it), [gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b), [EuroLLM-22B](https://huggingface.co/utter-project/EuroLLM-22B-Instruct-2512) | Licencje i kontekst modeli otwartych |
| [arXiv 2608.30929](https://arxiv.org/abs/2608.30929), [arXiv 2511.04205](https://arxiv.org/abs/2511.04205), [arXiv 2606.12250](https://arxiv.org/abs/2606.12250) | Wyszukiwanie przepisów, egzamin KIO, egzaminy lekarskie |
| [arXiv 2603.04162](https://arxiv.org/abs/2603.04162), [PolAgentBench arXiv 2609.32042](https://arxiv.org/abs/2609.32042) | Kwantyzacja 2-bitowa: testy wyboru vs agenci |
| [whisper.cpp](https://github.com/ggml-org/whisper.cpp/issues/89) | Szybkość large-v3-turbo |
| [Mac mini](https://www.apple.com/pl/shop/buy-mac/mac-mini), [Mac Studio](https://www.apple.com/pl/shop/buy-mac/mac-studio), [Apple newsroom](https://www.apple.com/newsroom/2026/08/apple-introduces-new-mac-studio-with-m5-max-and-m5-ultra/), [Apple pobór mocy](https://support.apple.com/en-us/102027) | Ceny w Polsce, pamięć, pobór mocy |
| [llama.cpp #4167](https://github.com/ggml-org/llama.cpp/discussions/4167), [#15396](https://github.com/ggml-org/llama.cpp/discussions/15396), [#16578](https://github.com/ggml-org/llama.cpp/discussions/16578), [#10879](https://github.com/ggml-org/llama.cpp/discussions/10879), [Ollama MLX](https://ollama.com/blog/mlx), [LMSYS](https://www.lmsys.org/blog/2025-10-13-nvidia-dgx-spark), [Framework forum](https://community.frame.work/t/dgx-spark-vs-strix-halo-initial-impressions/77055) | Prędkości dekodowania i prefill |
| [bestllmfor (szacunki)](https://bestllmfor.com/ai-hardware/mac-studio-m5/), [runaihome (blog)](https://runaihome.com/blog/framework-desktop-vs-gmktec-evo-x2-local-ai-2026/) | Szacunki dla M5 i Strix Halo, hałas i pobór |
| [ceneo GX10](https://www.ceneo.pl/;szukaj-ascent+gx10), [ceneo DGX Spark](https://www.ceneo.pl/;szukaj-dgx+spark), [ceneo Strix Halo](https://www.ceneo.pl/;szukaj-ryzen+ai+max%2B+395+128gb), [ceneo RTX PRO 6000](https://www.ceneo.pl/;szukaj-rtx+pro+6000+blackwell), [ceneo R9700](https://www.ceneo.pl/;szukaj-radeon+ai+pro+r9700) | Ceny w Polsce 11.10.2026 |
| [NVIDIA forum (zmiana ceny)](https://forums.developer.nvidia.com/t/2-23-2026-price-change-announcement/361713), [tech-insider](https://tech-insider.org/nvidia-rtx-pro-6000-blackwell-price-2026/) | Wzrost cen sprzętu z dużą pamięcią |
| [EuroHPC AI Factories](https://www.eurohpc-ju.europa.eu/ai-factories_en), [Beyond.pl](https://beyond.pl/en/) | Gdzie dostrajać modele poza biurkiem |

## Uzupełnienie: luka europejska i retencja agentów (02-RYNEK.md)

| Źródło | Co wziąłem |
|---|---|
| [cryptobriefing.com](https://cryptobriefing.com/meta-muse-app-store-retention/) | prasa: Muse — 5 mln pobrań w USA w 22 dni, ok. 700 tys. dziennych użytkowników pod koniec IX 2026 (02-RYNEK, 9. Luka europejska) |
| [about.fb.com](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | Meta (dane firmy): Muse z 8.09.2026, chmurowa maszyna wirtualna, dostępność USA i Kanada |
| [techcrunch.com](https://techcrunch.com/2026/08/10/metas-new-glimmer-ai-model-offers-a-hint-at-zuckerbergs-personal-intelligence-vision/) | prasa: Muse Glimmer, 10.08.2026 |
| [venturebeat.com](https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now) | prasa: Glimmer — Apache 2.0, ok. 30 mld parametrów, 4-bit na GPU 24 GB |
| [heise.de](https://www.heise.de/en/news/Siri-AI-in-the-EU-iPhone-and-iPad-users-must-continue-to-wait-11476320.html) | prasa: Siri AI (iOS 27, 14.09.2026) niedostępna na iPhone'ach w UE (DMA) |
| [aboutamazon.com](https://www.aboutamazon.com/news/devices/alexa-plus-international-launch) | Amazon: lista krajów Alexa+ — bez Polski |
| [androidheadlines.com](https://www.androidheadlines.com/2026/07/google-gemini-spark-expands-to-ai-pro-subscribers.html) | prasa: Gemini Spark niedostępny w EOG, Szwajcarii i Wielkiej Brytanii |
