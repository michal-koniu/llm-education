# Wzorce techniczne asystentów — czego uczą najlepsi

**Stan na 11 października 2026.** Profile w [01-PROFILE.md](01-PROFILE.md) mówią, *co* robi piętnastu najlepszych
asystentów. Ten plik wyciąga z nich to, co da się przenieść: dwadzieścia wzorców technicznych — kto to robi, dlaczego
działa i jak to zrobić u siebie. Potem uczciwa tabela offline, architektura referencyjna lokalnego asystenta dla
polskich profesjonalistów i rozdział o ewaluacji i bezpieczeństwie.

Czego tu **nie** powtarzam: konkretne narzędzia (wyszukiwarki, piaskownice, głos, obraz) są w
[klockach przeglądu harnessów](../harnessy-agentowe/02-KLOCKI.md), a wzorzec „Opus planuje, lokalni agenci wykonują"
na moim sprzęcie (4× R9700, DeepSeek-V4-Flash, 4 sloty po 131k, ~13,6 tok/s na agenta) w
[03-ARCHITEKTURA.md](../harnessy-agentowe/03-ARCHITEKTURA.md). Prawo i ceny sprzętu:
[04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md). Źródła: [ZRODLA.md](ZRODLA.md).

---

## Spis treści

1. [Anatomia asystenta](#1-anatomia-asystenta)
2. [Wzorce](#2-wzorce)
   - [2.1. Inżynieria kontekstu pod prompt cache](#21-inżynieria-kontekstu-pod-prompt-cache)
   - [2.2. Plik planu i recytacja celu](#22-plik-planu-i-recytacja-celu)
   - [2.3. Planista, krytyk i zbiory źródeł](#23-planista-krytyk-i-zbiory-źródeł)
   - [2.4. Computer use: najpierw DOM, potem obraz](#24-computer-use-najpierw-dom-potem-obraz)
   - [2.5. Ręce lokalnie, mózg gdzie indziej](#25-ręce-lokalnie-mózg-gdzie-indziej)
   - [2.6. Piaskownica albo VM na zadanie](#26-piaskownica-albo-vm-na-zadanie)
   - [2.7. Broker poświadczeń](#27-broker-poświadczeń)
   - [2.8. Zatwierdzenia skalowane wpływem na świat](#28-zatwierdzenia-skalowane-wpływem-na-świat)
   - [2.9. Umiejętności i przepisy](#29-umiejętności-i-przepisy)
   - [2.10. Pamięć ograniczona i pamięć w plikach](#210-pamięć-ograniczona-i-pamięć-w-plikach)
   - [2.11. Puls, cron i bramka skryptowa](#211-puls-cron-i-bramka-skryptowa)
   - [2.12. Komunikator jako interfejs](#212-komunikator-jako-interfejs)
   - [2.13. Głos](#213-głos)
   - [2.14. Powiązane dowody i cytaty](#214-powiązane-dowody-i-cytaty)
   - [2.15. Przegląd tabelaryczny](#215-przegląd-tabelaryczny)
   - [2.16. Procedury w języku naturalnym](#216-procedury-w-języku-naturalnym)
   - [2.17. Symulacja i powtarzalność](#217-symulacja-i-powtarzalność)
   - [2.18. Własny model z otwartych wag](#218-własny-model-z-otwartych-wag)
   - [2.19. Router i hybryda modeli](#219-router-i-hybryda-modeli)
   - [2.20. Notatki ze spotkań bez bota](#220-notatki-ze-spotkań-bez-bota)
3. [Offline: co naprawdę działa bez internetu](#3-offline-co-naprawdę-działa-bez-internetu)
4. [Architektura referencyjna lokalnego asystenta na biurko](#4-architektura-referencyjna-lokalnego-asystenta-na-biurko)
5. [Ewaluacja i bezpieczeństwo](#5-ewaluacja-i-bezpieczeństwo)

---

## 1. Anatomia asystenta

Każdy produkt z rankingu — od OpenClaw po Harvey — składa się z tych samych ośmiu warstw. Różnią się tym, **która
warstwa jest ich przewagą**: Harvey wygrywa treścią i ewaluacją, Manus kontekstem i maszyną wirtualną, OpenClaw
kanałami i pulsem, Abridge powiązanymi dowodami.

```text
1. KANAŁY        czat / PWA · komunikator · e-mail · głos · wtyczka Word
        |
2. ORKIESTRATOR  pętla agenta · plan (todo.md) · sesje · puls i cron · procedury (AOP) · podagenci
        |
        +--> 3. MODELE + ROUTER   duży model · mały szybki · krytyk · STT / TTS · wizja
        |                         reguła routera: najpierw wrażliwość danych, potem trudność
        +--> 4. NARZĘDZIA         pliki · RAG z cytatami · MCP · przeglądarka (DOM) · computer use
        |
5. PAMIĘĆ        USER.md / MEMORY.md (ograniczone) · pamięć sprawy · indeks
6. WYKONANIE     piaskownica / VM na zadanie · osobny użytkownik · egress zamknięty · broker poświadczeń
7. NADZÓR        zatwierdzenia wg wpływu · krytyk · zbiory źródeł · przejęcie przez człowieka
8. EWALUACJA     dziennik zdarzeń · złote zestawy · pass^k · ślady
```

Dwie obserwacje, które sterują resztą pliku:

- **Model jest najmniej unikalną warstwą.** Manus stawia na „inżynierię kontekstu na modelach z czołówki" zamiast
  własnych modeli ([Manus, 18.07.2025](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)),
  Harvey trzyma kilku dostawców naraz ([Harvey, 10.03.2026](https://www.harvey.ai/en-US/blog/why-harvey-is-multi-model-by-design)).
  **Przewaga siedzi w warstwach 2, 4 i 6–8** — i dokładnie te da się zbudować lokalnie.
- **Warstwy 6–8 to dziś osobny produkt.** Google opisał dla agenta w Chrome sześć mechanizmów nadzoru
  ([Google, 8.12.2025](https://blog.google/security/architecting-security-for-agentic/)), Microsoft dosyła do OpenClaw
  kontrolę zgodności z polityką firmy ([OpenClaw, 25.09.2026](https://openclaw.ai/blog/microsoft-autopilot-openclaw)).
  Dla polskiego profesjonalisty te warstwy są argumentem sprzedażowym, nie kosztem.

Kurs: [kurs 2, część 1](../kurs_aplikacje_agentowe/01-ARCHITEKTURY-AGENTOWE.md).

---

## 2. Wzorce

Każdy wzorzec: **co to jest**, **kto** (z linkiem do profilu), **dlaczego działa**, **u siebie** — jak to zrobić lokalnie.

### 2.1. Inżynieria kontekstu pod prompt cache

**Co to jest.** Kontekst projektujesz tak, by kolejne tury trafiały w pamięć podręczną prefiksu (KV-cache). Sześć
reguł Manusa: stały prefiks (żadnych znaczników czasu co do sekundy); kontekst tylko dopisywany, z deterministyczną
serializacją; **maskowanie narzędzi zamiast usuwania** (spójne prefiksy `browser_`, `shell_`); system plików jako
pamięć z „odwracalną kompresją" (wyrzucasz treść strony, zostawiasz URL); recytacja celu w `todo.md`; błędy zostają
w kontekście; zero powtarzalnych przykładów ([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).

**Kto.** [Manus](01-PROFILE.md#6-manus) nazywa trafienia w cache „najważniejszą metryką agenta w produkcji"; wejście
do wyjścia ~100:1, typowe zadanie ~50 wywołań narzędzi *(dane firmy, 2025)*. [Hermes Agent](01-PROFILE.md#5-hermes-agent)
wstrzykuje pamięć jako „zamrożoną migawkę" na starcie sesji, żeby nie psuć cache
([docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)). OpenHands po przekroczeniu progu
streszcza stare zdarzenia, zostawiając cel, postęp i listę zadań — koszt tury spadł poniżej połowy przy 54% wobec 53%
rozwiązanych zadań *(dane projektu)* ([OpenHands](https://openhands.dev/blog/openhands-context-condensensation-for-more-efficient-ai-agents)).

**Dlaczego działa.** Agent czyta dużo więcej, niż pisze. W chmurze odczyt z cache jest ~10× tańszy, lokalnie różnica
jest w **czasie**: mój rig czyta prompt ~1 186 tok/s, więc 50 tys. tokenów bez cache to ~40 s do pierwszego tokenu
([03-ARCHITEKTURA](../harnessy-agentowe/03-ARCHITEKTURA.md#1-zasoby-co-naprawdę-masz)).

**U siebie.** Data i zmienne dane w wiadomości użytkownika, nie w prompcie systemowym. Stała lista narzędzi na całą
sesję — „wyłączasz" gramatyką albo walidacją. Ta sama sesja do tego samego slotu llama-server (Manus robi routing po
ID sesji). Duże obserwacje do pliku, do kontekstu tylko ścieżka i streszczenie. Kurs:
[kurs 2, część 4](../kurs_aplikacje_agentowe/04-INZYNIERIA-KONTEKSTU.md),
[kurs 1, część 8](../kurs_lokalne_modele/08-OPTYMALIZACJA-OFFLINE.md); pułapka H4 w
[harnessach](../harnessy-agentowe/01-PROFILE.md#siedem-pułapek-wspólnych-dla-wszystkich).

### 2.2. Plik planu i recytacja celu

**Co to jest.** Agent prowadzi plik planu i co kilka kroków go przepisuje; przy zadaniach ryzykownych człowiek
zatwierdza plan **przed** wykonaniem.

**Kto.** [Manus](01-PROFILE.md#6-manus) przepisuje `todo.md`, bo przy ~50 krokach model gubi cel w środku kontekstu.
[ChatGPT](01-PROFILE.md#7-chatgpt) Work (9.07.2026) ma „Plan mode": dopytuje, pokazuje plan krok po kroku, a zatwierdzony
plan staje się granicą zgody użytkownika ([digitalapplied](https://www.digitalapplied.com/blog/chatgpt-work-openai-agent-launch-2026)).

**Dlaczego działa.** Recytacja przesuwa cel na koniec kontekstu, gdzie model patrzy najuważniej; jeden zatwierdzony
plan zastępuje dziesiątki pytań „czy mogę?".

**U siebie.** `praca/<zadanie>/plan.md`: cel, kryterium „gotowe", kroki ze statusem, otwarte pytania. Orkiestrator
wymusza przepisanie co N kroków i przed każdą akcją z zapisem. W UI plan to lista do odhaczenia — i dokumentacja dla
klienta.

### 2.3. Planista, krytyk i zbiory źródeł

**Co to jest.** Trzy mechanizmy Google dla agenta w Chrome ([Google](https://blog.google/security/architecting-security-for-agentic/)):
**krytyk zgodności z celem** — osobny model ocenia każdą akcję i może ją zawetować, a widzi tylko akcję i cel,
**nie treść strony**; **zbiory źródeł** (Agent Origin Sets) — domeny per zadanie, osobno „tylko odczyt" i „odczyt
i zapis"; **deterministyczne potwierdzenia** przed stronami banków i medycznymi, logowaniem przez menedżer haseł,
płatnością i wysłaniem wiadomości. Do tego klasyfikator injection równolegle z planistą i dziennik pracy z przejęciem.

**Kto.** [Gemini](01-PROFILE.md#8-gemini). W API każdy krok zwraca `safety_decision`, a 7 kategorii polityk
(transakcje, dane wrażliwe, komunikacja, umowy…) wymusza potwierdzenie ([docs](https://ai.google.dev/gemini-api/docs/computer-use)).

**Dlaczego działa.** Krytyk jest tani, a odcięcie go od treści strony zamyka główny kanał ataku. Zbiory źródeł
ograniczają szkody nawet po przejęciu agenta.

**U siebie.** Krytyk to mały model na CPU (u mnie `gpt-oss-20b-cpu`): wejście `{cel, akcja, domena, klasa_akcji}`,
wyjście `{zgoda, powód}`. Zbiory źródeł w konfiguracji zadania („ISAP i SAOS — odczyt; portal sądowy — zapis po
zatwierdzeniu"). Wyzwalacze potwierdzeń w kodzie, nie w modelu.

### 2.4. Computer use: najpierw DOM, potem obraz

**Co to jest.** Agent widzi stronę jako tekst — drzewo dostępności albo listę elementów z identyfikatorami — a zrzut
ekranu jest planem awaryjnym.

**Kto.** [browser-use](01-PROFILE.md#13-browser-use): „tekst najpierw" to idea założycielska, od 8.2025 w 100% na Chrome
DevTools Protocol ([ain.ua](https://en.ain.ua/2025/03/25/browser-use-raises-17m),
[changelog](https://browser-use.com/changelog/19-8-2025)). [Claude](01-PROFILE.md#2-claude): `browser_toolset` czyta
drzewo dostępności i używa referencji elementów odpornych na przesunięcia układu; pełny zrzut ekranu to 1 000–1 800
tokenów wejścia ([browser use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool),
[computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). Strona wizji:
[UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) (Apache-2.0) z jednym modelem wizyjnym i hybrydą GUI + DOM;
Agent S3 rozdziela model „gdzie kliknąć" (UI-TARS-1.5-7B) od modelu rozumującego i z wyborem najlepszego z kilku
przebiegów osiąga 72,6% w OSWorld wobec 72,36% człowieka ([Agent S](https://github.com/simular-ai/Agent-S)).

**Dlaczego działa.** DOM jest tańszy, stabilniejszy i pasuje do małych modeli bez wizji; obraz jest potrzebny tylko
dla pikselowych interfejsów.

**U siebie.** DeepSeek-V4-Flash jest tylko tekstowy, więc DOM to naturalna ścieżka: Playwright MCP, agent-browser albo
browser-use z lokalnym endpointem ([klocki](../harnessy-agentowe/02-KLOCKI.md#agenci-przeglądarkowi)); wizja przez
„mostek" — osobny model opisuje ekran ([03-ARCHITEKTURA, U5](../harnessy-agentowe/03-ARCHITEKTURA.md#u5--zdjęcia-i-obrazy)).
**Uwaga na liczby producentów:** browser-use ogłosił 89,1% na WebVoyager po usunięciu 55 z 586 zadań, a na niezależnej
tablicy Online-Mind2Web ten stos z Claude Sonnet 4 miał 40,0% ([raport](https://browser-use.com/posts/sota-technical-report),
[HAL](https://hal.cs.princeton.edu/online_mind2web)).

### 2.5. Ręce lokalnie, mózg gdzie indziej

**Co to jest.** Wykonanie (przeglądarka, pliki, VM) działa na maszynie użytkownika, do modelu idą tylko obserwacje.

**Kto.** [Perplexity](01-PROFILE.md#15-perplexity) Comet według akt *Amazon v. Perplexity*: przeglądarka użytkownika
rozmawia ze stroną, robi zrzuty lokalnie i wysyła je na serwery Perplexity po instrukcje
([Jones Day](https://www.jonesday.com/en/insights/2026/09/ninth-circuit-vacates-cfaa-injunction-against-perplexitys-comet-ai-agent)).
[Claude](01-PROFILE.md#2-claude): computer use wykonuje aplikacja dewelopera, Cowork uruchamia lokalną VM Linuksa przez
Apple Virtualization — model w chmurze ([Simon Willison](https://simonwillison.net/2026/Jan/12/claude-cowork/)).
[Manus](01-PROFILE.md#6-manus) radzi bankowość robić przez lokalną przeglądarkę, bo adresy centrów danych wywołują
blokady ([docs](https://manus.im/docs/features/cloud-browser.md)).

**Dlaczego działa.** Loginy i ciasteczka zostają u użytkownika; nie ma problemu „bota z serwerowni".

**U siebie.** Gotowy szablon — **wystarczy podmienić mózg na lokalny**. Dla danych klienta obie połowy zostają na
biurku; chmura może być „mózgiem" tylko dla treści bez danych klienta (sekcja 4). Wzorzec planisty:
[03-ARCHITEKTURA, sekcja 2](../harnessy-agentowe/03-ARCHITEKTURA.md#2-wzorzec-planista-i-wykonawcy).

### 2.6. Piaskownica albo VM na zadanie

**Co to jest.** Każde zadanie albo sprawa dostaje odizolowane środowisko z dostępem tylko do wskazanych folderów
i zamkniętym ruchem wychodzącym.

**Kto.** [Manus](01-PROFILE.md#6-manus): mikro-VM Firecracker przez E2B, start ~150 ms; Docker odpadł przez 10–20 s
startu ([E2B, 6.05.2025](https://e2b.dev/blog/how-manus-uses-e2b-to-provide-agents-with-virtual-computers)).
[Claude](01-PROFILE.md#2-claude) Cowork montuje tylko foldery, na które pozwolił użytkownik, i ogranicza sieć. Windows
daje agentowi **własne konto**, sześć znanych folderów i wybór „zawsze / pytaj / nigdy"
([Microsoft](https://support.microsoft.com/en-us/windows/experimental-agentic-features-a25ede8a-e4c2-4841-85a8-44839191dfb3)).
[NemoClaw](https://github.com/NVIDIA/NemoClaw) owija OpenClaw piaskownicą **domyślnie**, z akceptacją ruchu wychodzącego
przez operatora.

**Dlaczego działa.** Szkoda po przejęciu agenta kończy się na jednym folderze. **Ale:** PromptArmor pokazał, że Cowork
wysłał pliki ofiary na konto atakującego przez **dozwolone** API Anthropic z kluczem atakującego
([PromptArmor](https://www.promptarmor.com/resources/claude-cowork-exfiltrates-files)) — lista dozwolonych hostów nie
wystarcza, gdy dozwolony host przyjmuje dowolne poświadczenia.

**U siebie.** Piaskownica na sprawę: srt albo bubblewrap dla powłoki, microsandbox dla kodu agenta
([klocki](../harnessy-agentowe/02-KLOCKI.md#piaskownice)); osobny użytkownik systemu; egress domyślnie zamknięty,
a jeśli potrzebny — lista domen przez proxy, które wpuszcza tylko Twoje poświadczenia. Kurs:
[kurs 1, część 7](../kurs_lokalne_modele/07-SANDBOX-BEZPIECZENSTWO-MONITORING.md),
[kurs 2, część 10](../kurs_aplikacje_agentowe/10-PIASKOWNICA-PRODUKCYJNA.md).

### 2.7. Broker poświadczeń

**Co to jest.** Hasła i tokeny nigdy nie trafiają do promptu ani piaskownicy. Agent dostaje uchwyt, a podstawienie
robi zaufany proces poza zasięgiem modelu — tylko dla dozwolonej domeny.

**Kto.** Kortix: poświadczenia „są pośredniczone po stronie serwera przez jeden token o wąskim zakresie i nigdy nie
wchodzą do maszyny" ([README](https://raw.githubusercontent.com/kortix-ai/suna/main/README.md)). Claude Code w chmurowych
VM: poświadczenia GitHuba nie wchodzą do VM, ruch wychodzi przez proxy ([docs](https://code.claude.com/docs/en/data-usage)).
[browser-use](01-PROFILE.md#13-browser-use): „secret bindings" przypięte do `allowedDomains`
([docs](https://docs.browser-use.com/cloud/choosing-an-agent)). Logowanie i 2FA oddaje się człowiekowi — Manus
„Take Over", Gemini Spark oddaje logowanie i płatności ([Google](https://support.google.com/gemini/answer/16596215)).
Microsoft dosłał do OpenClaw maskowanie sekretów w promptach zatwierdzeń
([OpenClaw](https://openclaw.ai/blog/microsoft-autopilot-openclaw)).

**Dlaczego działa.** Model, który nie zna hasła, nie wycieknie go — ani przez injection, ani do dziennika.

**U siebie.** Sejf (szyfrowany plik albo keyring) + proxy narzędzi: agent pisze `{{sekret:ksef}}`, proxy podstawia
wartość tylko w żądaniu do domeny tego sekretu i wycina ją z odpowiedzi i logów. Profil zaufany, portale sądowe,
bankowość — logowanie zawsze robi człowiek w przejętej sesji.

### 2.8. Zatwierdzenia skalowane wpływem na świat

**Co to jest.** O tym, czy agent pyta, decyduje **wpływ akcji na zewnątrz** i jej odwracalność, a nie pewność modelu.

**Kto.** Lindy: „wszystko, co ma wpływ na zewnątrz, czeka na zatwierdzenie… wyszukiwania tylko do odczytu nie wymagają
zatwierdzenia" ([Lindy](https://www.lindy.ai/pricing)). [browser-use](01-PROFILE.md#13-browser-use) „Agency" pyta tylko
przed wysłaniem albo publikacją ([changelog, 17.08.2026](https://browser-use.com/changelog/3-4-2026)).
[Claude](01-PROFILE.md#2-claude) w Chrome potwierdza publikację, zakup i udostępnienie danych osobowych
([Anthropic](https://claude.com/blog/claude-for-chrome)). OpenHands ma tryb `ConfirmRisky`, model oznacza ryzyko akcji,
a analizator wzorców łapie `rm -rf` i `curl | sh` ([docs](https://docs.openhands.dev/sdk/guides/security)). ZeroClaw ma
poziomy autonomii i zatwierdzenia podpisane HMAC ([harnessy](../harnessy-agentowe/01-PROFILE.md#10-zeroclaw)). Microsoft
w Autopilocie: akcji o **nieznanym wyniku** nie ponawia się automatycznie ([OpenClaw](https://openclaw.ai/blog/microsoft-autopilot-openclaw)).

**Dlaczego działa.** Brak pytań o odczyty, a każda nieodwracalna akcja ma człowieka.

**U siebie.**

| Klasa akcji | Przykład | Decyzja |
|---|---|---|
| Odczyt lokalny | przeszukanie akt, OCR skanu | automatycznie |
| Szkic | projekt pisma, szkic e-maila w folderze „Szkice" | automatycznie, zostaje szkicem |
| Zapis w piaskownicy | nowy plik w katalogu sprawy | automatycznie, z punktem przywracania |
| Wpływ na zewnątrz | wysłanie e-maila, złożenie pisma, płatność, usunięcie | zawsze człowiek |
| Wynik nieznany | przerwana wysyłka, timeout portalu | stop, bez ponowienia, pytanie do człowieka |

### 2.9. Umiejętności i przepisy

**Co to jest.** Powtarzalna procedura jako folder z plikiem Markdown (instrukcja, przykłady, skrypty), ładowany dopiero,
gdy jest potrzebny.

**Kto.** [OpenClaw](01-PROFILE.md#1-openclaw): `SKILL.md` i rejestr ClawHub. [Hermes Agent](01-PROFILE.md#5-hermes-agent)
sam pisze umiejętności po złożonych zadaniach, poprawia je i skanuje przy instalacji
([docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)). Poke ma „przepisy" — automatyzacje zwykłym
tekstem, którymi użytkownicy się dzielą ([TechCrunch, 8.04.2026](https://techcrunch.com/2026/04/08/poke-makes-ai-agents-as-easy-as-sending-a-text/)).
LexisNexis ma w Protégé umiejętności swoje i partnerów, a własne klientów zapowiada „wkrótce" (24.08.2026,
[LexisNexis](https://www.lexisnexis.com/community/pressroom/b/news/posts/lexis-with-protege-accelerates-frictionless-agentic-productivity-from-first-idea-to-review-ready-legal-work-product)).

**Dlaczego działa.** Prompt systemowy zostaje krótki (cache), a wiedza proceduralna jest wersjonowana. **Ciemna strona:**
otwarty rynek umiejętności to nowa powierzchnia ataku (sekcja 5).

**U siebie.** Katalog `umiejetnosci/` w gicie, po jednej na procedurę zawodu („przegląd umowy najmu", „zamknięcie
miesiąca VAT", „notatka z wizyty — kardiologia"). Umiejętność napisana przez agenta idzie do przeglądu, nie do użycia.
Bez publicznego rynku — Moltis rezygnuje z niego celowo ([harnessy](../harnessy-agentowe/01-PROFILE.md#15-moltis)).

### 2.10. Pamięć ograniczona i pamięć w plikach

**Co to jest.** Pamięć to czytelne pliki z twardym limitem, które właściciel może otworzyć, poprawić i cofnąć.

**Kto.** [Hermes Agent](01-PROFILE.md#5-hermes-agent): `MEMORY.md` ≤ 2 200 znaków, `USER.md` ≤ 1 375 znaków; pełna pamięć
wymusza konsolidację zamiast cichego gubienia wpisów ([docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)).
[OpenClaw](01-PROFILE.md#1-openclaw) wstrzykuje `SOUL.md`, `USER.md`, `MEMORY.md`, `AGENTS.md` w każdej sesji, a w tle
„śni": pisze `DREAMS.md` i promuje do `MEMORY.md` tylko mocne wpisy z wagą 1–10 ([docs](https://docs.openclaw.ai/concepts/dreaming)).
[Claude](01-PROFILE.md#2-claude) trzyma pamięć jako pliki tematyczne i domyślnie nie zapisuje tematów wrażliwych
([Anthropic, 25.08.2026](https://claude.com/resources/articles/claudes-memory-works-everywhere-and-you-decide-whats-in-it)).
[Harvey](01-PROFILE.md#4-harvey) II (18.08.2026) zamyka pracę w „Spaces" sprawy ([Harvey](https://www.harvey.ai/blog/introducing-harvey-ii)).

**Dlaczego działa.** Limit wymusza kurację, stała migawka nie psuje cache, a plik da się pokazać klientowi albo
inspektorowi.

**U siebie.** Globalny `USER.md` (styl, preferencje — **bez danych klientów**) i `sprawy/<sygnatura>/pamiec.md` ładowany
tylko w sesji tej sprawy. Wskaźnik zapełnienia w UI („67% — 1 474/2 200"). Wszystko w gicie, więc „skąd agent to wie?"
ma odpowiedź w historii. Kurs: [kurs 2, część 5](../kurs_aplikacje_agentowe/05-PAMIEC-DLUGOTERMINOWA.md) i
[część 6](../kurs_aplikacje_agentowe/06-TOZSAMOSC-PLIKI-ROBOCZE.md).

### 2.11. Puls, cron i bramka skryptowa

**Co to jest.** Agent budzi się sam — z harmonogramu albo zdarzenia — ale **najpierw tani skrypt sprawdza, czy jest
co robić**, i dopiero wtedy wołany jest model.

**Kto.** [OpenClaw](01-PROFILE.md#1-openclaw): puls domyślnie co 30 min, wybudzenia co najmniej 30 s od siebie i blokada
po 5 startach w 60 s ([heartbeat](https://docs.openclaw.ai/gateway/heartbeat)); „standing orders" opisują zakres,
wyzwalacz, bramkę zatwierdzenia i eskalację ([docs](https://docs.openclaw.ai/automation/standing-orders)). NanoClaw ma
„bramki skryptowe", które nie budzą modelu bez pracy ([README](https://github.com/nanocoai/nanoclaw)); Moltis może
obsługiwać puls osobnym małym modelem ([harnessy](../harnessy-agentowe/01-PROFILE.md#15-moltis)). ChatGPT Pulse liczy
poranny brief nocą ([TechCrunch](https://techcrunch.com/2025/09/25/openai-launches-chatgpt-pulse-to-proactively-write-you-morning-briefs/)),
Google CC wysyła codzienny e-mail, na który się odpowiada ([Google](https://blog.google/technology/google-labs/cc-ai-agent/)).

**Dlaczego działa.** Większość przebudzeń to „nic nowego" — skrypt odpowiada na to za darmo.

**U siebie.** Timer systemd → skrypt (nowy plik w sprawie? nowa wiadomość w skrzynce biura? nowa pozycja w lokalnym
lustrze Dziennika Ustaw?) → kolejka → model. Nocą GPU stoi — tam idą briefy, przegląd tabelaryczny i ewaluacje. Kurs:
[kurs 2, część 11](../kurs_aplikacje_agentowe/11-HARMONOGRAM-PROAKTYWNOSC.md);
[klocki](../harnessy-agentowe/02-KLOCKI.md#harmonogram-i-trwałe-wykonanie).

### 2.12. Komunikator jako interfejs

**Co to jest.** Asystent mieszka w aplikacji, której użytkownik i tak używa.

**Kto.** [OpenClaw](01-PROFILE.md#1-openclaw): jedna bramka dla WhatsApp, Telegram, Signal, iMessage, Teams, Matrix,
e-maila i innych ([docs](https://docs.openclaw.ai/llms.txt)). Poke: pierwszy agent AI zatwierdzony na Apple Messages
for Business (4.06.2026), „ponad 100 mln wiadomości w 3 miesiące" *(dane firmy)*
([TechCrunch](https://techcrunch.com/2026/06/04/apple-approves-poke-as-the-first-ai-agent-on-its-messages-for-business-platform/),
[Cognition, 23.07.2026](https://cognition.com/blog/interaction)). **Druga strona:** Apple na stałe zablokował Lindy
konto Apple ID w pół dnia; firma przepisała kanał trzy razy i pilnuje stosunku wysłanych do odebranych poniżej ~10:1
([Lindy, 16.03.2026](https://www.lindy.ai/blog/imessage-api-three-rewrites-one-apple-ban-and-what-actually-works)).

**Dlaczego działa.** Zero wdrożenia u użytkownika i naturalna proaktywność — agent pisze pierwszy.

**U siebie.** Komunikatory konsumenckie to cudza chmura i wroga platforma — **danych klienta tam nie wysyłasz**
(to samo przy Telegramie w [klockach](../harnessy-agentowe/02-KLOCKI.md#powiadomienia-i-kanały)). Kanałem
profesjonalisty jest aplikacja webowa w sieci biura, e-mail przez serwer kancelarii (wzorzec „DW do asystenta"),
wtyczka Word — tam siedzą Spellbook i Noxtua ([Spellbook](https://www.spellbook.com/press), [Noxtua](https://www.noxtua.com/))
— i Matrix na własnym serwerze. Mój osobisty asystent może używać Telegrama do spraw niewrażliwych. Kurs:
[kurs 2, część 12](../kurs_aplikacje_agentowe/12-KANALY-INTERFEJSY.md).

### 2.13. Głos

**Co to jest.** Mowa jako wejście (dyktowanie, notatka głosowa, nagranie wizyty) i wyjście (odczyt, rozmowa).

**Kto.** [Hermes Agent](01-PROFILE.md#5-hermes-agent): notatki głosowe z lokalnym faster-whisper, ale **synteza mowy
domyślnie przez chmurowy Edge TTS**; Moltis: lokalne STT i Piper z polskimi głosami, w pełni offline
([harnessy: Hermes](../harnessy-agentowe/01-PROFILE.md#4-hermes-agent), [Moltis](../harnessy-agentowe/01-PROFILE.md#15-moltis)).
[Abridge](01-PROFILE.md#3-abridge) i Nabla mają własne medyczne ASR; Nabla trenowała na bazie Whispera plus 7 000 godzin
nagrań medycznych i **nigdy nie wkleja surowej transkrypcji do dokumentacji**
([Nabla](https://nabla.com/blog/assessing-the-reliability-of-nablas-speech-to-text-engine)).

**Dlaczego działa.** Lekarz i adwokat mówią szybciej, niż piszą; nagranie to najbogatsze źródło faktów.

**U siebie.** Kaskada STT → LLM → TTS — lokalnej mowy-do-mowy po polsku na AMD w październiku 2026 nie znalazłem
([03-ARCHITEKTURA, U4](../harnessy-agentowe/03-ARCHITEKTURA.md#u4--rozmowa-głosowa-po-polsku),
[klocki](../harnessy-agentowe/02-KLOCKI.md#głos)). Transkrypcja to produkt pośredni: notatkę pisze LLM, każde zdanie
wskazuje fragment nagrania (2.14). Zbuduj test polskich nazw leków i terminów prawniczych, zanim komuś to sprzedasz.

### 2.14. Powiązane dowody i cytaty

**Co to jest.** Każde zdanie wyniku ma klikalny wskaźnik do źródła: fragmentu transkrypcji, strony dokumentu, przepisu.

**Kto.** [Abridge](01-PROFILE.md#3-abridge) „Linked Evidence": każde zdanie notatki prowadzi do transkrypcji albo nagrania;
model-strażnik poprawia twierdzenia bez pokrycia i w wewnętrznym teście na 10 000+ wizyt złapał 97% takich twierdzeń
wobec 82% dla GPT-4o *(dane firmy, 19.08.2025)* ([Abridge](https://www.abridge.com/ai/science-confabulation-hallucination-elimination)).
[OpenEvidence](01-PROFILE.md#12-openevidence): RAG nad licencjonowaną literaturą (NEJM, JAMA, NCCN, Cochrane) z cytatami
w tekście ([Wikipedia](https://en.wikipedia.org/wiki/OpenEvidence)). Hebbia: „widać, skąd wzięła się każda liczba"
([Hebbia](https://www.hebbia.com/blog/introducing-matrix-2-0)). W Polsce LEX Expert AI (19.11.2025) linkuje odpowiedzi
do źródeł i fragmentów w LEX — tę poprzeczkę polscy prawnicy już znają
([Prawo.pl](https://www.prawo.pl/prawnicy-sady/lex-expert-ai-nowym-narzedziem-dla-prawnikow)).

**Dlaczego działa.** Weryfikacja zdania trwa sekundy. Dla adwokata to warunek: § 23e Zbioru Zasad Etyki Adwokackiej
wymaga osobistej weryfikacji wyniku ([NRA, 12–13.06.2026](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/)).

**U siebie.** Każdy fragment z RAG ma identyfikator `{dokument, strona, przesunięcie}`; model zwraca zdania z listą
identyfikatorów, kod odrzuca zdanie bez cytatu. Drugie przejście: weryfikator dostaje **tylko** zdanie i cytowany
fragment i odpowiada „pokryte / niepokryte". „Nie wiem" jest dozwolone i nagradzane w ewaluacji. Kurs:
[kurs 1, część 4](../kurs_lokalne_modele/04-PAMIEC-RAG-I-KONTEKST.md).

### 2.15. Przegląd tabelaryczny

**Co to jest.** Siatka „N pytań × M dokumentów": wiersz to dokument, kolumna pytanie, komórka odpowiedź z cytatem.
Czat zamienia się w analityka wsadowego.

**Kto.** Hebbia Matrix wymyśliła ten interfejs; Matrix 2.0 (26.08.2026) prowadzi analizę do gotowych memo i prezentacji
z punktami kontroli człowieka ([Hebbia](https://www.hebbia.com/blog/introducing-matrix-2-0)). Skopiowali go Legora,
Thomson Reuters (Tabular Analysis do 10 000 dokumentów × 100 pytań — [CoCounsel](https://legal.thomsonreuters.com/en/products/cocounsel-legal))
i [Noxtua](01-PROFILE.md#14-noxtua) (Matrix Analysis). [Harvey](01-PROFILE.md#4-harvey) liczy koszt „na komórkę":
własny Tenet ma ~1/10 kosztu komórki w Review Table *(dane firmy)* ([Harvey, 20.08.2026](https://www.harvey.ai/blog/post-training-update-harvey-tenet)).

**Dlaczego działa.** Każda komórka to małe, niezależne, łatwe do sprawdzenia zadanie — idealne dla lokalnego modelu
i równoległych slotów — a wynik jest arkuszem, którego profesjonalista i tak używa.

**U siebie.** Kolejka komórek z limitem 4 slotów, kolejność „dokument po dokumencie": w jednym slocie dokument jako
stały prefiks i kolejne pytania, więc cache czyta go raz. Komórka = JSON `{odpowiedź, cytat, strona, pewność}`
walidowany w kodzie, eksport do XLSX z linkami do stron PDF. Przepustowości na moim rigu **nie mierzyłem** — dobry
pierwszy pomiar.

### 2.16. Procedury w języku naturalnym

**Co to jest.** Zachowanie agenta opisuje ekspert zwykłym językiem, a osobna, ukryta przed agentem specyfikacja ocenia
**przebieg**, nie tylko wynik.

**Kto.** Decagon: „Agent Operating Procedures" — procedury w języku naturalnym, które zespół obsługi zmienia „bez
sprintów inżynierskich" ([Decagon](https://decagon.ai/blog/series-d-announcement)). Basis: „behavior specs"
(29.07.2026), otwarty standard z Braintrust — specyfikacje oceniają trajektorię (prawda / fałsz / nie dotyczy) i
„nigdy nie są pokazywane agentowi", bo „poprawny wynik nie mówi, czy agent użył procesu, któremu zaufalibyśmy
ponownie" ([Basis](https://www.getbasis.ai/blogs/behavior-specs-an-open-standard-for-supervising-long-horizon-agents)).

**Dlaczego działa.** Kontrolę nad zachowaniem ma prawnik albo księgowa, nie programista; specyfikacja przebiegu łapie
„dobry wynik z przypadku".

**U siebie.** `procedury/wezwanie-do-zaplaty.md` po polsku, pisane przez profesjonalistę („gdy klient przysyła
wezwanie, najpierw policz termin…"), a obok `oceny/wezwanie-do-zaplaty.spec.md` z pytaniami o przebieg („czy sprawdził
białą listę VAT", „czy zacytował interpretację KIS") — tego pliku agent nie widzi.

### 2.17. Symulacja i powtarzalność

**Co to jest.** Zanim agent dostanie klientów, rozmawia z symulowanymi, a miarą jest **pass^k** — czy udało się k razy
z rzędu na tym samym zadaniu.

**Kto.** [Sierra](01-PROFILE.md#11-sierra): τ-bench (20.06.2024) symuluje użytkowników i API pod regułami domeny; GPT-4o
spadł w handlu detalicznym do ~25% przy pass^8, o 60% względem pass^1 ([Sierra](https://sierra.ai/blog/benchmarking-ai-agents)).

**Dlaczego działa.** Profesjonalista potrzebuje przewidywalności bardziej niż szczytowej jakości. DeepSeek-V4-Flash na
moim trudnym zestawie ma 92/93, ale powtarzalność tylko 83 ([03-ARCHITEKTURA](../harnessy-agentowe/03-ARCHITEKTURA.md#tryb-w-pełni-lokalny)).

**U siebie.** Symulator klienta na lokalnym modelu z personami per zawód, uruchamiany nocą: k = 8 przebiegów na
zadanie, raport pass^1 i pass^8. Lokalnie nocne obliczenia są prawie darmowe.

### 2.18. Własny model z otwartych wag

**Co to jest.** Otwarty model bazowy dotrenowany (pretrening, SFT, RL) na danych dziedziny i śladach zadań zamiast
modelu z czołówki przy każdej komórce.

**Kto.** [Harvey](01-PROFILE.md#4-harvey) Tenet (20.08.2026): Kimi K3 po RL (GSPO) z Fireworks, dane syntetyczne,
publiczne i eksperckie — „nie użyliśmy danych klientów"; −90% kosztu zapytania o wiedzę firmy *(dane firmy)*; wag
nie opublikowano ([Harvey](https://www.harvey.ai/blog/post-training-update-harvey-tenet)). [Cursor](01-PROFILE.md#9-cursor)
Composer 2 (19.03.2026): otwarty Kimi K2.5 plus własny pretrening i RL; bazy nie ujawniono przy premierze, Cursor
przyznał po odkryciu przez użytkownika ([Cursor](https://cursor.com/blog/composer-2),
[Gigazine](https://gigazine.net/gsc_news/en/20260323-cursor-admits-composer-2-kimi)). [Noxtua](01-PROFILE.md#14-noxtua):
poziom „Athena" na modelach open source w suwerennej infrastrukturze UE ([Noxtua](https://www.noxtua.com/)).
Microsoft Fara-7B: mały model computer use trenowany na 145 tys. syntetycznych trajektorii większego agenta
([MSR](https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/)).

**Dlaczego działa.** Wąskie, mierzalne zadania (ekstrakcja, komórka tabeli) potrzebują modelu dopasowanego, nie
największego. Własne wagi to też suwerenność.

**U siebie.** Najpierw prompty i DSPy z Opusem jako nauczycielem
([klocki](../harnessy-agentowe/02-KLOCKI.md#niezawodność-wywołań-narzędzi-i-strojenie-promptów)), potem dotrenowanie
**mniejszego** modelu (Bielik-11B, Qwen 27B) do jednej czynności. 284-miliardowego DeepSeeka na 4× R9700 nie dotrenujesz.
Dwie zasady z cudzych błędów: ujawniaj model bazowy (Cursor) i nie trenuj na danych klientów bez zgody (Harvey robi
z tego argument).

### 2.19. Router i hybryda modeli

**Co to jest.** Kod decyduje, który model obsłuży krok — według wrażliwości danych, trudności i kosztu.

**Kto.** [Harvey](01-PROFILE.md#4-harvey): routing po zadaniu, przełączenie przy awarii dostawcy, administrator wybiera
dozwolone modele ([Harvey](https://www.harvey.ai/en-US/blog/why-harvey-is-multi-model-by-design)). Perplexity Computer:
19 modeli z podagentami ([TechCrunch, 27.02.2026](https://techcrunch.com/2026/02/27/perplexitys-new-computer-is-another-bet-that-users-need-many-ai-models/)).
Glean Tau: 0,58 USD wobec 2,98 USD za zadanie w porównaniu z Claude Cowork *(benchmark producenta, 27.08.2026)*
([itbrief](https://itbrief.asia/story/glean-launches-tau-to-cut-enterprise-ai-token-costs)). [Noxtua](01-PROFILE.md#14-noxtua):
„Athena" (otwarte, suwerenne) albo „Minerva" (modele z czołówki w układzie europejskim)
([Noxtua](https://www.noxtua.com/security)).

**Dlaczego działa.** Większość kroków jest prosta; drogi model tylko tam, gdzie się zwraca. **Pułapka:** wybór modelu
potrafi po cichu przenieść dane — w Microsoft 365 Copilot modele Anthropic jako podprocesor są wyłączone z EU Data
Boundary ([Microsoft](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy)).

**U siebie.** Pierwsza reguła routera to **wrażliwość**, druga trudność: „dane klienta → tylko lokalnie" jest twardą
regułą w kodzie, nie decyzją modelu. Bramka i limity: [klocki](../harnessy-agentowe/02-KLOCKI.md#bramka-i-routing-modeli);
kurs: [kurs 2, część 17](../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md),
[kurs 1, część 10](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md).

### 2.20. Notatki ze spotkań bez bota

**Co to jest.** Aplikacja nagrywa mikrofon i dźwięk systemu na urządzeniu — żaden bot nie dołącza do rozmowy — a LLM
rozwija **notatki użytkownika** w pełną notatkę.

**Kto.** [Granola](01-PROFILE.md#10-granola): dwa kanały dają darmową diaryzację „Ja / Oni", nagranie nie jest zapisywane,
zostaje transkrypcja; ASR i LLM w chmurze ([docs](https://docs.granola.ai/help-center/taking-notes/transcription)).
Ciemna strona: w 7.2026 prasa opisała notatki domyślnie udostępniane linkiem i trenowanie domyślnie włączone w planach
Free i Business ([Startup Fortune](https://startupfortune.com/granola-ai-meeting-notes-are-not-as-private-as-you-might-think/)),
a 30.07.2026 złożono pozew zbiorowy *Chamberlain v. Granola*
([ppc.land](https://ppc.land/granola-sued-for-recording-meetings-without-consent-to-train-ai-models/)).

**Dlaczego działa.** Brak bota usuwa tarcie społeczne, a notatki użytkownika mówią modelowi, co było ważne.

**U siebie.** Mikrofon i pętla systemowa jako dwie ścieżki → whisper.cpp albo Parakeet → diaryzacja po kanale → LLM
scala z notatkami i szablonem → audio kasowane po transkrypcji. Zgodę uczestników na nagrywanie sprawdź dla swojej
sytuacji — to nie jest porada prawna.

---

## 3. Offline: co naprawdę działa bez internetu

**„Tak"** = produkt sam działa bez internetu (otwarty kod + lokalny model). Usługi chmurowe dostają **„Nie"**, nawet
gdy część wykonania jest lokalna. Szczegóły w [01-PROFILE.md](01-PROFILE.md).

| Asystent | Kod | Offline | Co działa lokalnie | Czego brakuje / co podmienić |
|---|---|---|---|---|
| [OpenClaw](01-PROFILE.md#1-openclaw) | otwarty (MIT) | Częściowo | pętla, pamięć, puls i cron z lokalnym modelem; CLI, TUI, lokalny web UI ([docs](https://docs.openclaw.ai/gateway/local-models)) | kanały WhatsApp / Telegram / Signal wymagają sieci; lokalne modele „nie mają filtrów bezpieczeństwa dostawców"; piaskownica nie jest domyślna |
| [Claude](01-PROFILE.md#2-claude) | zamknięty | Nie | computer use / browser use wykonuje Twoja maszyna; VM Cowork lokalna; klient Claude Code lokalny | model tylko w chmurze — lokalny LLM + własna pętla z tym samym podziałem „mózg / ręce" |
| [Abridge](01-PROFILE.md#3-abridge) | zamknięty | Nie | tylko nagrywanie na telefonie lub w aplikacji EHR | whisper.cpp + lokalny LLM + weryfikator + powiązane dowody (2.13, 2.14) |
| [Harvey](01-PROFILE.md#4-harvey) | zamknięty | Nie | nic — SaaS; Tenet bez publicznych wag | lokalny model + RAG z cytatami + przegląd tabelaryczny (2.14, 2.15) |
| [Hermes Agent](01-PROFILE.md#5-hermes-agent) | otwarty (MIT) | Częściowo | pętla z lokalnym endpointem, STT faster-whisper, pamięć w plikach, cron | **TTS domyślnie Edge TTS (chmura)** — zamień na Piper; kanały komunikatorów wymagają sieci |
| [Manus](01-PROFILE.md#6-manus) | zamknięty | Nie | lokalna przeglądarka jako aktuator (Browser Operator) | VM na zadanie (microsandbox), lokalny model, reguły kontekstu (2.1, 2.6) |
| [ChatGPT](01-PROFILE.md#7-chatgpt) | zamknięty | Nie | nic w produkcie (prasa podaje otwarcie samego harnessu Codex, 29.09.2026) | wszystko — pętla, VM, przeglądarka, model |
| [Gemini](01-PROFILE.md#8-gemini) | zamknięty | Nie | auto browse działa w Chrome użytkownika, model w chmurze; Gemini Spark niedostępny w EOG | krytyk, zbiory źródeł i potwierdzenia przenieś do własnej pętli (2.3) |
| [Cursor](01-PROFILE.md#9-cursor) | zamknięty | Nie | edytor; wykonanie na „Self-Hosted Machines"; zapytania zawsze przez backend Cursora | Cline albo [OpenCode](../harnessy-agentowe/01-PROFILE.md#8-opencode) z lokalnym modelem |
| [Granola](01-PROFILE.md#10-granola) | zamknięty | Nie | przechwycenie mikrofonu i dźwięku systemowego | lokalne STT + diaryzacja po kanale + lokalny LLM (2.20) |
| [Sierra](01-PROFILE.md#11-sierra) | zamknięty | Nie | nic; otwarta jest metoda (τ-bench) | symulator klienta i pass^k na lokalnym modelu (2.17) |
| [OpenEvidence](01-PROFILE.md#12-openevidence) | zamknięty | Nie | nic | lokalny RAG nad polskimi wytycznymi towarzystw, ChPL i rekomendacjami AOTMiT |
| [browser-use](01-PROFILE.md#13-browser-use) | otwarty (MIT) | Częściowo | biblioteka z lokalnym endpointem; strony w intranecie | internet wymaga sieci; BU 2.0, przeglądarki „stealth" i agenci V3 / V4 tylko w chmurze; małe modele psują schematy akcji |
| [Noxtua](01-PROFILE.md#14-noxtua) | zamknięty | Nie | wtyczki Word i Outlook to klienci; modele w suwerennej chmurze UE (DE, CH) | „suwerenność" to tu chmura UE, nie biurko — otwarty model + RAG nad ISAP i SAOS |
| [Perplexity](01-PROFILE.md#15-perplexity) | zamknięty | Częściowo (tylko Portable Computer; reszta produktu to chmura) | lokalny model 27B, harness i piaskownica na biurku (zob. profil); Comet wykonuje akcje lokalnie, ale rozumuje na serwerach | wymaga Nvidii (Apple Silicon i AMD nieobsługiwane); działania offline nie zweryfikowałem; świeże wyszukiwanie offline jest niemożliwe |

Źródła wierszy: profile w [01-PROFILE.md](01-PROFILE.md); Codex — [Decrypt](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced);
Gemini Spark poza EOG — [Google](https://support.google.com/gemini/answer/16596215); Cursor — [dane](https://cursor.com/data-use);
browser-use — [BU 2.0](https://docs.browser-use.com/open-source/bu-2-0-model-card) i [klocki](../harnessy-agentowe/02-KLOCKI.md#agenci-przeglądarkowi).

**Wniosek:** z piętnastu żaden produkt nie działa w pełni offline. Częściowo lokalnie da się uruchomić cztery: OpenClaw, Hermes i browser-use (otwarte, z lokalnym modelem; kanały, TTS Edge i strony publiczne wymagają sieci) oraz Perplexity Portable Computer (zamknięty). To nie są produkty dla profesjonalistów. **Nikt z czołówki nie sprzedaje polskiemu prawnikowi czy lekarzowi
asystenta, który działa na biurku** — tę lukę wypełnia sekcja 4.

### Funkcja → lokalny zamiennik

| Funkcja | Lokalny zamiennik (otwarty) | Co jest słabe offline |
|---|---|---|
| LLM | mój rig: DeepSeek-V4-Flash (tylko tekst); na biurko: Qwen3.6-27B, Gemma-4-31B, gpt-oss-120b; Bielik-11B-v3 do polskiego stylu | najlepszy otwarty model w PLCC: 89,83 wobec 92–97 dla zamkniętych (8.10.2026); zamiana Opusa na mały model kosztowała w OpenJarvis 25–39 pp |
| Embeddingi i RAG | llama-swap serwuje embeddingi; SQLite + BM25 + reranking ([kurs 1, część 4](../kurs_lokalne_modele/04-PAMIEC-RAG-I-KONTEKST.md)); FTS5 jak w Hermesie; Cognee bez klucza chmurowego | najlepsze wyszukiwanie przepisów na pytaniach z egzaminów na aplikacje: 72,3% top-1 (BM25: 61,7%) |
| STT | whisper.cpp large-v3 (WER 4,74% FLEURS-pl), Parakeet-TDT-0.6B-v3 na CPU (7,31%), faster-whisper | polskie słownictwo medyczne i mikrofon w gabinecie — niezweryfikowane |
| TTS | Piper pl_PL (CPU, robotyczny), Chatterbox Multilingual V3 (MIT, znak wodny), VoxCPM2 | jakość polskiego TTS; Kokoro tylko EN; brak lokalnej mowy-do-mowy po polsku na AMD |
| OCR i wizja | Docling + PaddleOCR-VL-1.5 (mało VRAM, działa na CPU); Qwen3.6-35B-A3B; test DeepSeek-V4-Flash-Vision-Exp | DeepSeek-V4-Flash nie widzi obrazów; modele wizyjne słabo wykorzystują obraz w polskich pytaniach medycznych |
| Wyszukiwanie w sieci | SearXNG (wymaga internetu); offline: lokalne lustra ISAP / ELI, SAOS, ChPL i wytycznych, synchronizowane osobnym procesem | świeża wiedza z sieci jest niemożliwa; lustro ma datę |
| Kalendarz i e-mail | IMAP / SMTP do serwera biura, CalDAV (np. Nextcloud on-prem), szkice wprost w skrzynce, „DW do asystenta" | wysyłka z definicji wymaga sieci; kalendarze w chmurze odpadają |
| Computer use | DOM: browser-use, Playwright MCP (bez wizji), agent-browser; GUI: UI-TARS-desktop + UI-TARS-1.5-7B, Holo4-35B-A3B, Fara-7B | w OSWorld 2.0 (6.2026) najlepszy model z czołówki ukończył 20,6%; model 7B ma w OSWorld ~27,5% |
| Kanały | aplikacja webowa / PWA w sieci biura, Matrix na własnym serwerze, Gotify, ntfy hostowany samemu | WhatsApp, iMessage, Telegram to cudza chmura; push na iOS wymaga przekaźnika ntfy.sh |
| Moderacja i injection | Bielik-Guard 0.5B (polski klasyfikator szkód), BrowseSafe (otwarte wagi) | BrowseSafe przepuszcza ~10% ataków (12.2025); Bielik-Guard: precyzja 75,28% |

Źródła: [klocki](../harnessy-agentowe/02-KLOCKI.md) (głos, obraz, wyszukiwanie, kanały, pamięć); OpenJarvis —
[03-ARCHITEKTURA](../harnessy-agentowe/03-ARCHITEKTURA.md#3-co-jest-udowodnione-a-co-nie); [PLCC](https://huggingface.co/spaces/sdadas/plcc);
przepisy — [arXiv 2608.30929](https://arxiv.org/abs/2608.30929); wizja medyczna PL — [arXiv 2608.12928](https://arxiv.org/abs/2608.12928);
OSWorld 2.0 — [arXiv 2606.29537](https://arxiv.org/abs/2606.29537); [UI-TARS-1.5-7B](https://huggingface.co/ByteDance-Seed/UI-TARS-1.5-7B);
[Bielik-Guard](https://huggingface.co/speakleash/Bielik-Guard-0.5B-v1.1);
BrowseSafe — [the-decoder](https://the-decoder.com/perplexitys-browsesafe-tries-to-patch-the-gaping-security-holes-inherent-in-ai-browser-agents/).

---

## 4. Architektura referencyjna lokalnego asystenta na biurko

Cel: asystent dla kancelarii, gabinetu albo biura rachunkowego, w którym **dane klienta nie opuszczają biurka**. To
projekt złożony z wzorców z sekcji 2 — **niezmierzony**, dopóki go nie zbudujesz.

```text
BIURO (sieć lokalna)                                                 | INTERNET
  PWA w przeglądarce · wtyczka Word · e-mail biura · nagrywanie      |
                          |                                          |
  +------------- PUDEŁKO NA BIURKU (szyfrowany dysk) -------------+  |
  | ORKIESTRATOR   pętla · plan.md · procedury · puls + bramki    |  |
  |   router: dane klienta -> tylko lokalnie                      |  |
  | MODELE (llama-swap)        NARZĘDZIA (MCP, tylko odczyt)      |  |
  |   główny LLM · Bielik        RAG sprawy z cytatami            |  |
  |   krytyk (mały model)        przegląd tabelaryczny -> XLSX    |  |
  |   STT · TTS · OCR            szkice pism · DOM-przeglądarka   |  |
  | PAMIĘĆ     USER.md · sprawy/<sygnatura>/ · indeks · lustra    |  |
  | WYKONANIE  piaskownica na sprawę · osobny użytkownik          |  |
  | NADZÓR     zatwierdzenia wg wpływu · broker poświadczeń       |  |
  | DZIENNIK   zdarzenia append-only · notatka o narzędziach      |  |
  +---------------------------+-----------------------------------+  |
          zapora wyjścia: domyślnie NIE                              |
              +-- podpisane aktualizacje ----------------------------+--> serwer aktualizacji
              +-- lustra ISAP / SAOS (osobny proces, bez spraw) -----+--> źródła publiczne
              +-- opcja, wyłączona: planista hybrydowy --------------+--> Opus (tylko treść
                                                                     |    bez danych klienta)
```

| Warstwa | Komponent | Wzorzec | Uwagi |
|---|---|---|---|
| Kanały | PWA w LAN, wtyczka Word, e-mail biura | 2.12 | bez komunikatorów konsumenckich dla danych klienta |
| Orkiestrator | własna pętla albo Pydantic AI; `plan.md`; procedury per zawód | 2.2, 2.16 | limit współbieżności w jednym miejscu |
| Modele | główny LLM + Bielik-11B-v3 + mały krytyk + STT / TTS / OCR | 2.3, 2.19 | tylko wagi z licencją komercyjną (Apache-2.0, MIT) |
| Wiedza | RAG nad sprawami i skrzynką; lustra ISAP / ELI i SAOS | 2.14 | cytat albo „nie wiem" |
| Praca wsadowa | przegląd tabelaryczny, briefy nocne | 2.11, 2.15 | GPU nocą |
| Pamięć | `USER.md` bez danych klientów, pamięć per sprawa, git | 2.10 | limit znaków |
| Wykonanie | piaskownica na sprawę, osobny użytkownik systemu | 2.6 | egress domyślnie zamknięty |
| Nadzór | zatwierdzenia wg wpływu, krytyk, broker poświadczeń | 2.7, 2.8 | logowanie i 2FA robi człowiek |
| Dziennik | zdarzenia append-only, „notatka o narzędziach" per sprawa | sekcja 5 | dziennik to dane osobowe |
| Ewaluacja | złote zestawy, pass^k, PLCC / CPTUB | 2.17, sekcja 5 | przed każdą zmianą modelu |

### Zasady przepływu danych

1. **Dane klienta nie wychodzą z pudełka.** Model, indeks, dzienniki i kopie są lokalne — wtedy dla części AI nie ma
   podmiotu przetwarzającego (art. 28 RODO) ani transferu poza EOG (rozdział V)
   ([RODO](https://eur-lex.europa.eu/eli/reg/2016/679/oj)). Działa to tylko, jeśli serwis dostawcy nie sięga do danych:
   podpisane paczki aktualizacji, bez zdalnej powłoki domyślnie.
2. **Ruch wychodzący jest jednokierunkowy i bez danych klienta.** Osobny proces pobiera aktualizacje i lustra źródeł
   publicznych; proces z dostępem do spraw nie ma sieci. Ghost robi z zapory wyjścia funkcję zaufania
   ([TechCrunch, 5.10.2026](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/)).
3. **Planista hybrydowy (Opus) jest wyłączony domyślnie i dostaje tylko treść, w której nigdy nie było danych klienta**:
   pytania o przepisy w oderwaniu od sprawy, kod narzędzi, szablony, procedury. Dlaczego nie „zanonimizowane akta":
   dane spseudonimizowane nadal są danymi osobowymi (motyw 26 RODO); ponowna identyfikacja to opisane ryzyko systemów
   LLM ([EDPB, 10.04.2025](https://www.edpb.europa.eu/our-work-tools/our-documents/support-pool-experts-projects/ai-privacy-risks-mitigations-large_pt));
   dostawca z USA podlega CLOUD Act ([18 U.S.C. § 2713](https://www.law.cornell.edu/uscode/text/18/2713)); § 23e ZZEA
   zabrania udostępniania informacji poufnych narzędziom bez „należytej ochrony". „Lokalny wykonawca jako filtr
   prywatności" z [03-ARCHITEKTURA](../harnessy-agentowe/03-ARCHITEKTURA.md#tryb-w-pełni-lokalny) też jest modelem —
   może się pomylić. Szerzej: [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md). To nie jest porada prawna.
4. **Pełne szyfrowanie dysku, osobne konta, szyfrowane kopie.** Skradzione pudełko bez szyfrowania to naruszenie
   w rozumieniu art. 33–34 RODO.

### Rozmiar sprzętu

Ceny, dostępność i pomiary pudełek: [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md). Tu tylko, co musi się
zmieścić w pamięci — mój szacunek z rozmiarów wag, nie pomiar:

| Klasa pamięci | Co się mieści | Dla kogo |
|---|---|---|
| 16–24 GB | gpt-oss-20b (mieści się w 16 GB), Bielik-11B-v3 albo Bielik-Minitron-7B | solo — czat i szkice, bez ciężkiego rozumowania |
| 32–64 GB | Qwen3.8-27B (Q4 ~18,5 GB) albo Qwen3.6-35B-A3B (Q4 ~23 GB) + Bielik + whisper | solo albo 2–3 osoby, przegląd tabelaryczny w kolejce |
| 128 GB | gpt-oss-120b albo Gemma-4-31B w wyższej precyzji + Bielik + wizja + STT naraz | biuro 1–5 osób, RAG nad aktami |

Dwie twarde reguły: **dla agentów co najmniej Q4** — w PolAgentBench Bielik-11B-v3, Bielik-Minitron-7B i Llama-PLLuM-8B
„spadają z klifu" między 3 a 2 bitami ([arXiv 2609.32042](https://arxiv.org/abs/2609.32042)); **tylko wagi
z licencją komercyjną** — modele PLLuM „-nc" odpadają. Rozmiary: [gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b),
[Bielik-11B-v3](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct), [klocki: obraz](../harnessy-agentowe/02-KLOCKI.md#obraz).

### Wariant na moim rigu

4× R9700, DeepSeek-V4-Flash w 3 bitach (104,2 GB), `--parallel 4` po 131k, ~1,4 GB wolnego VRAM na kartę
([03-ARCHITEKTURA](../harnessy-agentowe/03-ARCHITEKTURA.md#1-zasoby-co-naprawdę-masz)). Model jest **tylko tekstowy**,
więc wszystko „zmysłowe" idzie obok:

| Zasób | Rola |
|---|---|
| Slot 1 | orkiestrator i planista (myślenie włączone), synteza wyników |
| Sloty 2–3 | wykonawcy: komórki przeglądu tabelarycznego, ekstrakcja, szkice (3 naraz to zmierzone optimum) |
| Slot 4 | rezerwa na rozmowę interaktywną, żeby użytkownik nie czekał za pracą wsadową |
| CPU | `gpt-oss-20b-cpu` jako krytyk, router i triaż pulsu; Parakeet (STT), Piper (TTS), Smart Turn |
| CPU albo zwolniona karta | Docling + PaddleOCR-VL do skanów; Qwen3.6-35B-A3B do zrzutów ekranu po wymianie w llama-swap |
| Opcja | test DeepSeek-V4-Flash-Vision-Exp (ten sam rozmiar + ~0,93 GB), eksperymentalny |

Konsekwencja: przy ~13,6 tok/s na agenta **prompt cache i krótkie wyjścia JSON są ważniejsze niż wybór harnessu**
(2.1), a krytyk i bramki pulsu muszą działać na CPU, bo GPU jest pełne.

### Minimalny produkt (MVP)

1. Czat po polsku nad folderem sprawy — odpowiedź z cytatem do strony dokumentu albo „nie wiem" (2.14).
2. Przegląd tabelaryczny „pytania × dokumenty" z eksportem do XLSX (2.15).
3. Szkice pism i e-maili — **nigdy** wysyłka (2.8).
4. Transkrypcja nagrania (spotkanie, wizyta, dyktowanie) i notatka z szablonu z linkami do fragmentów (2.13, 2.20).
5. Procedury i umiejętności per zawód pisane przez profesjonalistę (2.9, 2.16).
6. Dziennik zdarzeń i „notatka o narzędziach" per sprawa (sekcja 5).
7. Zero ruchu wychodzącego z danymi, szyfrowany dysk, kopie (zasady wyżej).

Poza MVP: computer use na zewnętrznych portalach, komunikatory, rozmowa głosowa na żywo, planista hybrydowy.

### Etapy

| Etap | Co | Kryterium przejścia |
|---|---|---|
| 0 — ewaluacja | 30–50 prawdziwych zadań na zawód, specyfikacje przebiegu, PLCC / CPTUB wybranych modeli | znasz pass^1 i pass^8 na własnych zadaniach |
| 1 — MVP | punkty 1–7, jeden zawód, jedno biuro pilotażowe | profesjonalista weryfikuje odpowiedź szybciej, niż pisze sam |
| 2 — proaktywność | timery + bramki: nowe pismo w folderze, nowa pozycja w lustrze Dziennika Ustaw, poranny brief | brak „pustych" wywołań modelu w dzienniku |
| 3 — działanie | DOM-przeglądarka na portalach (KSeF, e-Sąd, ePUAP) ze zbiorami źródeł, krytykiem i brokerem | zero akcji z wpływem na zewnątrz bez zatwierdzenia |
| 4 — rozwój | dyktowanie i głos, dotrenowany mały model do jednej czynności, opcjonalna hybryda bez danych klienta | koszt komórki spada, wynik w złotym zestawie nie |

---

## 5. Ewaluacja i bezpieczeństwo

### Prompt injection w agentach przeglądarkowych

**Przyczyna jest strukturalna:** agent działa z sesjami użytkownika, więc polityka same-origin już nie chroni —
instrukcje może nieść każda strona, e-mail, zaproszenie z kalendarza czy obraz ([Brave](https://brave.com/blog/comet-prompt-injection/)).
OpenAI (22.12.2025): prompt injection jest „mało prawdopodobne, by kiedykolwiek został w pełni rozwiązany"
([TechCrunch](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/));
Gartner (8.12.2025) radził firmom blokować przeglądarki AI ([The Register](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/)).
Co już się wydarzyło:

- **Comet:** atak bez kliknięcia przez zaproszenie z kalendarza — wyciek lokalnych plików i poświadczeń z 1Password
  ([The Register, 3.03.2026](https://www.theregister.com/2026/03/03/perplexity_comet_browser_hole_cal_invite/)).
- **BragJack** (19.09.2026): jedno złośliwe rozszerzenie „wymusza prompt" w Chrome Gemini, Edge Copilot, Comet, Opera
  Neon i Claude w Chrome ([BleepingComputer](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/)).
- **Cowork:** ukryty biały tekst w dokumencie → wysyłka plików przez dozwolone API (2.6).
- Obrona pomaga, ale nie domyka: Anthropic obniżył skuteczność ataków na Claude w Chrome z 23,6% do 11,2%, a dla Opus 4.5
  podaje ~1% przy adaptacyjnym atakującym *(dane firmy, 2025)* ([Anthropic](https://www.anthropic.com/research/prompt-injection-defenses));
  BrowseSafe wykrywa 91% w < 0,5 s, ale ~10% ataków przechodzi *(12.2025)*.

Najlepszy opisany wzorzec po stronie wykonania ma [Harvey](01-PROFILE.md#4-harvey) (7.10.2026): sprawdzenie każdego
wywołania narzędzia, „przypinanie" definicji narzędzi przeciw podmianie, polityki Rego blokujące „śmiertelną trójcę"
(dane prywatne + niezaufana treść + komunikacja na zewnątrz), usuwanie ukrytych znaków Unicode z wyników — **egzekwowane
poza modelem** ([Harvey](https://www.harvey.ai/blog/building-harveys-mcp-policy-engine)).

**Lokalnie usuwasz wyciek do chmury, ale nie prompt injection.** Stąd: agent czyta, a nie pisze; osobny profil
przeglądarki bez głównych sesji; zbiory źródeł; bez `file://` i menedżera haseł; lokalny klasyfikator; i reguła trójcy
w kodzie — sesja, która czytała niezaufaną treść, traci narzędzia komunikacji na zewnątrz. Kurs:
[kurs 2, część 16](../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md).

### Lekcja z porad bezpieczeństwa OpenClaw

[OpenClaw](01-PROFILE.md#1-openclaw) ma w 2026 roku **722 porady bezpieczeństwa** (14 krytycznych, 249 wysokich, 390
średnich, 69 niskich; API GitHuba, 11.10.2026). Steinberger podaje, że z 1 309 zgłoszeń od 10.01 aż 746 zamknięto jako
nieważne, a 87% „krytycznych" było nieważnych ([OpenClaw, 30.04.2026](https://openclaw.ai/blog/openclaw-security-in-public)).
Prawdziwe problemy były gdzie indziej:

- **Rynek umiejętności.** Cisco znalazł co najmniej jedną podatność w 26% z 31 000 umiejętności agentów i umiejętność,
  która po cichu wysyłała dane `curl`em ([Cisco, 28.01.2026](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare)).
- **Piaskownica nie jest domyślna** — „workspace to domyślny katalog roboczy, nie twarda piaskownica", także w 2.0
  ([docs](https://docs.openclaw.ai/concepts/agent-workspace),
  [The Register](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492)).
- **Odpowiedzi:** VirusTotal, NVIDIA SkillSpector, Tencent ClawScan (86,9% zgodnych etykiet i 98,6% złapanych złośliwych
  umiejętności na 556 przypadkach *(dane projektu)* — [ClawScan](https://openclaw.ai/blog/tencent-aig-joins-clawscan)),
  wyniesienie kanałów i narzędzi z rdzenia do wtyczek, kontrola zgodności z polityką od Microsoftu.

Wnioski: **mały rdzeń, brak otwartego rynku, piaskownica domyślnie, przypięte wersje, kontrola zgodności konfiguracji
z zapisem dla inspektora**. Liczba porad nie mierzy bezpieczeństwa — Hermes nie ma żadnej opublikowanej w 2026 (API GitHuba,
11.10.2026), co może wynikać ze sposobu zgłaszania, nie z braku błędów.

### pass^k i złote zestawy per zawód

Benchmarki ogólne nasycają się: OSWorld przekroczył poziom człowieka, ale na OSWorld 2.0 (zadania ~1,6 h) najlepszy
model ukończył 20,6%, bo agenci „gubią ograniczenia, zgadują zamiast pytać i pomijają weryfikację"
([arXiv 2606.29537](https://arxiv.org/abs/2606.29537)). Liczy się **Twój** zestaw:

| Zawód | Złoty zestaw (30–50 zadań) | Co mierzysz | Punkt odniesienia |
|---|---|---|---|
| Adwokat / radca | przepis do stanu faktycznego, przegląd umowy, termin procesowy | trafność cytatu, „nie wiem" gdy trzeba | 72,3% top-1 przy wyszukiwaniu przepisów ([arXiv 2608.30929](https://arxiv.org/abs/2608.30929)); żaden LLM nie zdał części praktycznej egzaminu KIO ([arXiv 2511.04205](https://arxiv.org/abs/2511.04205)) |
| Lekarz | notatka z nagrania wizyty, pytanie o ChPL, kod rozpoznania | zdania bez pokrycia w nagraniu, nazwy leków | ostrzejsze punktowanie obniżyło wyniki o 31 pp na polskich egzaminach ([arXiv 2606.12250](https://arxiv.org/abs/2606.12250)) |
| Doradca / księgowa | dekretacja z KSeF XML, kwalifikacja VAT z interpretacją KIS | specyfikacja przebiegu (biała lista, cytat interpretacji) | wzorzec „agent przygotowuje, człowiek przegląda" z Basis (2.16) |
| Wszyscy | rozumienie polszczyzny | PLCC, CPTUB, PolAgentBench przed zmianą modelu lub kwantyzacji | [CPTUB](https://huggingface.co/spaces/speakleash/cptu_bench), [PLCC](https://huggingface.co/spaces/sdadas/plcc) |

Każde zadanie ma wejście, oczekiwany wynik, wymagane cytaty i ukrytą specyfikację przebiegu (2.16). Mierzysz pass^1
i pass^8 (2.17), a w produkcji — jak Spellbook — **odsetek przyjętych sugestii**
([LawNext](https://www.lawnext.com/2025/08/spellbook-becomes-one-of-the-first-legal-ai-platforms-to-launch-gpt-5.html)).
Harvey ma własny BigLaw Bench; polskiego odpowiednika dla kancelarii nie znalazłem. Narzędzia:
[klocki](../harnessy-agentowe/02-KLOCKI.md#obserwowalność-i-ewaluacja), [kurs 2, część 14](../kurs_aplikacje_agentowe/14-EWALUACJA.md).

### Dziennik zdarzeń

**Kto.** OpenHands zapisuje każdą interakcję jako typowane zdarzenie (akcja → obserwacja), co daje audyt i odtworzenie
([OpenHands](https://docs.openhands.dev/usage/architecture/runtime)); UI-TARS-desktop ma przeglądarkę strumienia zdarzeń;
Manus Browser Operator loguje każdą akcję ([Manus](https://manus.im/blog/manus-browser-operator)). W sprawie
*Amazon v. Perplexity* dzienniki agenta stały się materiałem dowodowym
([ComplexDiscovery](https://complexdiscovery.com/ninth-circuit-vacates-amazon-injunction-ai-agent-logs-emerge-as-ediscovery-issue/);
znam tylko tytuł).

**U siebie.**
- Dziennik tylko do dopisywania: kto, kiedy, model i wersja, narzędzie, cytat, kto zatwierdził.
- Eksport **„notatki o narzędziach"** per sprawa — § 23e ZZEA każe na prośbę klienta wskazać użyte narzędzia i ich cel
  ([NRA](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/)).
- Dziennik to dane osobowe: szyfrowanie (art. 32 RODO), retencja, eksport i usunięcie per klient. UODO przypomina, by
  „regularnie mierzyć i testować wdrożone środki bezpieczeństwa" ([UODO, 26.06.2026](https://uodo.gov.pl/pl/138/4449)) —
  dziennik plus złoty zestaw to właśnie ten pomiar.
- Kurs: [kurs 2, część 15](../kurs_aplikacje_agentowe/15-OBSERWOWALNOSC.md).

To nie jest porada prawna — przepisy i obowiązki zawodowe omawiam w [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md).
