# Wzorce techniczne asystentów — czego uczą najlepsi

**Stan na 11 października 2026.** Profile w [01-PROFILE.md](01-PROFILE.md) mówią, *co* robi piętnastu najlepszych
asystentów. Ten plik wyciąga z nich to, co da się przenieść: dwadzieścia wzorców technicznych, każdy z odpowiedzią
„kto to robi, dlaczego działa i jak to zrobić u siebie na biurku". Potem uczciwa tabela offline, architektura
referencyjna lokalnego asystenta dla polskich profesjonalistów i rozdział o ewaluacji i bezpieczeństwie.

Czego tu **nie** powtarzam: konkretne narzędzia (wyszukiwarki, piaskownice, głos, obraz) opisałem
w [przeglądzie harnessów — klockach](../harnessy-agentowe/02-KLOCKI.md), a wzorzec „Opus planuje, lokalni agenci
wykonują" na moim sprzęcie (4× R9700, DeepSeek-V4-Flash, 4 sloty po 131k, ~13,6 tok/s na agenta)
w [03-ARCHITEKTURA.md](../harnessy-agentowe/03-ARCHITEKTURA.md). Tu linkuję do nich zamiast przepisywać. Prawo i ceny
sprzętu są w [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md). Źródła: [ZRODLA.md](ZRODLA.md).

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
warstwa jest ich przewagą**: Harvey wygrywa treścią i ewaluacją, Manus inżynierią kontekstu i maszyną wirtualną,
OpenClaw kanałami i pulsem, Abridge powiązanymi dowodami.

```text
+--------------------------------------------------------------------------------+
| 1. KANAŁY      czat / aplikacja · komunikator · e-mail · głos · wtyczka Word   |
+---------------------------------------+----------------------------------------+
                                        |
+---------------------------------------v----------------------------------------+
| 2. ORKIESTRATOR   pętla agenta · plan (todo.md) · sesje · puls i cron          |
|                   procedury (AOP, standing orders) · podagenci                 |
+-----------+-------------------------------------------------------+------------+
            |                                                       |
+-----------v-----------------------+       +-------------------------v-----------+
| 3. MODELE + ROUTER                |       | 4. NARZĘDZIA                        |
|  duży model · mały szybki model   |       |  pliki · RAG z cytatami · MCP       |
|  krytyk · STT / TTS · wizja       |       |  przeglądarka (DOM) · computer use  |
|  reguła: wrażliwość -> trudność   |       |  szkice e-mail · eksport XLSX/DOCX  |
+-----------+-----------------------+       +-------------------------+-----------+
            |                                                       |
+-----------v-------------------------------------------------------v------------+
| 5. PAMIĘĆ        USER.md / MEMORY.md (ograniczone) · pamięć sprawy · indeks     |
+---------------------------------------+----------------------------------------+
                                        |
+---------------------------------------v----------------------------------------+
| 6. WYKONANIE     piaskownica / VM na zadanie · osobny użytkownik systemu        |
|                  egress domyślnie zamknięty · broker poświadczeń               |
+---------------------------------------+----------------------------------------+
                                        |
+---------------------------------------v----------------------------------------+
| 7. NADZÓR        zatwierdzenia wg wpływu · krytyk · zbiory źródeł · przejęcie   |
+---------------------------------------+----------------------------------------+
                                        |
+---------------------------------------v----------------------------------------+
| 8. EWALUACJA I TELEMETRIA   dziennik zdarzeń · złote zestawy · pass^k · ślady  |
+--------------------------------------------------------------------------------+
```

Dwie obserwacje, które sterują resztą pliku:

- **Model jest najmniej unikalną warstwą.** Manus stawia na „inżynierię kontekstu na modelach z czołówki" zamiast
  trenowania własnych ([blog Manus, 18.07.2025](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)),
  Harvey trzyma kilku dostawców naraz ([Harvey, 10.03.2026](https://www.harvey.ai/en-US/blog/why-harvey-is-multi-model-by-design)).
  **Przewaga siedzi w warstwach 2, 4, 6–8** — i dokładnie te warstwy da się zbudować lokalnie.
- **Warstwy 6–8 to dziś osobny produkt.** Google opisał dla agenta w Chrome sześć mechanizmów nadzoru
  ([blog Google, 8.12.2025](https://blog.google/security/architecting-security-for-agentic/)), Microsoft buduje Autopilota
  na OpenClaw i dosyła do niego kontrolę zgodności z polityką
  ([OpenClaw, 25.09.2026](https://openclaw.ai/blog/microsoft-autopilot-openclaw)). Dla polskiego profesjonalisty
  te warstwy są argumentem sprzedażowym, nie kosztem.

Kurs: [kurs 2, część 1](../kurs_aplikacje_agentowe/01-ARCHITEKTURY-AGENTOWE.md) (architektury agentowe).

---

## 2. Wzorce

Każdy wzorzec ma cztery części: **co to jest**, **kto** (z linkiem do profilu), **dlaczego działa** i **u siebie** —
jak to zrobić na lokalnym sprzęcie.

### 2.1. Inżynieria kontekstu pod prompt cache

**Co to jest.** Projektujesz kontekst tak, by kolejne tury agenta trafiały w pamięć podręczną prefiksu (KV-cache).
Manus podaje sześć reguł: stały prefiks promptu (żadnych znaczników czasu co do sekundy), kontekst tylko dopisywany
z deterministyczną serializacją, **maskowanie narzędzi zamiast ich usuwania** (spójne prefiksy `browser_`, `shell_`),
system plików jako pamięć z „odwracalną kompresją" (wyrzucasz treść strony, zostawiasz URL i ścieżkę), recytacja celu
w `todo.md`, zostawianie błędów w kontekście i unikanie powtarzalnych przykładów
([Manus, 18.07.2025](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).

**Kto.** [Manus](01-PROFILE.md#6-manus) — trafienia w cache nazywa „najważniejszą metryką agenta w produkcji";
stosunek wejścia do wyjścia ma ~100:1, typowe zadanie to ~50 wywołań narzędzi *(dane firmy, 2025)*. Manus 2.0
z harnessem „Cascade", który dociąga możliwości dopiero gdy są potrzebne, deklaruje −32% kosztu operacyjnego
*(dane firmy, 28.09.2026; recenzja zewnętrzna zaznacza, że to jedna konfiguracja, nie średnia)*
([Manus 2.0](https://manus.im/blog/introducing-manus-2-0), [myclaw.ai](https://myclaw.ai/blog/manus-2-0)).
[Hermes Agent](01-PROFILE.md#5-hermes-agent) wstrzykuje pamięć jako „zamrożoną migawkę" na starcie sesji właśnie po to,
by nie psuć cache ([dokumentacja](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)).
OpenHands dokłada „kondenser": po przekroczeniu progu streszcza stare zdarzenia, zostawiając cel, postęp i listę
rzeczy do zrobienia — koszt tury spadł poniżej połowy przy 54% wobec 53% rozwiązanych zadań na próbce SWE-bench
*(dane projektu)* ([OpenHands](https://openhands.dev/blog/openhands-context-condensensation-for-more-efficient-ai-agents)).

**Dlaczego działa.** Agent czyta znacznie więcej, niż pisze. W chmurze odczyt z cache jest ~10× tańszy, lokalnie
różnica jest w **czasie**: na moim rigu jeden agent czyta prompt z prędkością ~1 186 tok/s, więc 50 tys. tokenów bez
cache to ~40 s czekania na pierwszy token, a 4 agentów startujących z 16 tys. tokenów czeka 44 s
([03-ARCHITEKTURA, sekcja 1](../harnessy-agentowe/03-ARCHITEKTURA.md#1-zasoby-co-naprawdę-masz)).

**U siebie.**
- Data, godzina i zmienne dane — w wiadomości użytkownika, nigdy w prompcie systemowym.
- Lista narzędzi stała przez całą sesję; „wyłączanie" narzędzia robisz gramatyką albo walidacją, nie usuwaniem.
- Ta sama sesja trafia do tego samego slotu llama-server (Manus robi to samo: routing po ID sesji przy prefix cache).
- Duże obserwacje (strona, PDF) idą do pliku w katalogu roboczym, do kontekstu trafia ścieżka i streszczenie.
- Kurs: [kurs 2, część 4](../kurs_aplikacje_agentowe/04-INZYNIERIA-KONTEKSTU.md),
  [kurs 1, część 8](../kurs_lokalne_modele/08-OPTYMALIZACJA-OFFLINE.md); pułapka H4
  w [harnessach](../harnessy-agentowe/01-PROFILE.md#siedem-pułapek-wspólnych-dla-wszystkich).

### 2.2. Plik planu i recytacja celu

**Co to jest.** Agent prowadzi plik z planem i co kilka kroków go przepisuje, a przy zadaniach ryzykownych
człowiek zatwierdza plan **przed** wykonaniem.

**Kto.** [Manus](01-PROFILE.md#6-manus) przepisuje `todo.md`, bo przy ~50 krokach model gubi cel „w środku" kontekstu
([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).
[ChatGPT](01-PROFILE.md#7-chatgpt) Work (9.07.2026) ma „Plan mode": zbiera kontekst, dopytuje, pokazuje plan krok po
kroku, a zatwierdzony plan staje się granicą zgody użytkownika
([digitalapplied](https://www.digitalapplied.com/blog/chatgpt-work-openai-agent-launch-2026)). Fellou pozwala edytować
plan przed i w trakcie wykonania ([Eko, MIT](https://github.com/FellouAI/eko)).

**Dlaczego działa.** Recytacja przesuwa cel na koniec kontekstu, gdzie model patrzy najuważniej. Zatwierdzony plan
zamienia dziesiątki pytań „czy mogę?" w jedno.

**U siebie.** `praca/<zadanie>/plan.md` z polami: cel, kryterium „gotowe", kroki ze statusem, otwarte pytania.
Orkiestrator wymusza przepisanie co N kroków (np. 8) i przed każdą akcją z zapisem. U profesjonalisty plan pokazujesz
w UI jako listę do odhaczenia — to jednocześnie dokumentacja dla klienta.

### 2.3. Planista, krytyk i zbiory źródeł

**Co to jest.** Trzy mechanizmy Google dla agenta w Chrome
([blog Google, 8.12.2025](https://blog.google/security/architecting-security-for-agentic/)):
1. **Krytyk zgodności z celem** — osobny, zaufany model ocenia każdą proponowaną akcję i może ją zawetować. Widzi
   tylko akcję i cel użytkownika, **nie surową treść strony**, więc wstrzyknięty tekst do niego nie trafia.
2. **Zbiory źródeł** (Agent Origin Sets) — lista domen per zadanie, podzielona na „tylko odczyt" i „odczyt i zapis"
   (gdzie wolno klikać i pisać).
3. **Deterministyczne potwierdzenia** przed wejściem na strony banków i medyczne, logowaniem przez menedżer haseł,
   płatnością i wysłaniem wiadomości — wyzwalane regułą, nie decyzją modelu.

Do tego klasyfikator prompt injection równolegle z planistą, dziennik pracy z pauzą i przejęciem oraz nagroda do
20 000 USD za obejście granic.

**Kto.** [Gemini](01-PROFILE.md#8-gemini) (Chrome auto browse). W API Gemini każdy krok zwraca `safety_decision`,
a 7 kategorii polityk (transakcje, dane wrażliwe, komunikacja, umowy…) wymusza potwierdzenie
([dokumentacja](https://ai.google.dev/gemini-api/docs/computer-use)).

**Dlaczego działa.** Krytyk jest tani (mało tokenów), a izolacja od treści strony zamyka główny kanał ataku.
Zbiory źródeł ograniczają szkody, nawet gdy agent zostanie przejęty.

**U siebie.** Krytyk to mały model na CPU (u mnie `gpt-oss-20b-cpu`) z wejściem JSON
`{cel, akcja, domena, klasa_akcji}` i wyjściem `{zgoda, powód}`. Zbiory źródeł trzymasz w konfiguracji zadania
(np. „ISAP i SAOS — odczyt; portal sądowy — zapis tylko po zatwierdzeniu"). Wyzwalacze potwierdzeń piszesz w kodzie
(lista domen, typy formularzy, przycisk „wyślij").

### 2.4. Computer use: najpierw DOM, potem obraz

**Co to jest.** Agent widzi stronę jako tekst — drzewo dostępności albo listę interaktywnych elementów z
identyfikatorami — a zrzut ekranu jest tylko planem awaryjnym.

**Kto.**
- [browser-use](01-PROFILE.md#13-browser-use) — „tekst najpierw" to idea założycielska; od 8.2025 w 100% na Chrome
  DevTools Protocol ([ain.ua](https://en.ain.ua/2025/03/25/browser-use-raises-17m),
  [changelog](https://browser-use.com/changelog/19-8-2025)).
- [Claude](01-PROFILE.md#2-claude) — `browser_toolset` czyta drzewo dostępności i używa referencji elementów, które
  przeżywają przesunięcia układu; współrzędne tylko w ostateczności. Pełny zrzut ekranu kosztuje 1 000–1 800 tokenów
  wejścia ([browser use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool),
  [computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)).
- Opera Neon reklamuje agenta „na DOM, nie na zrzutach" ([Opera, 3.03.2025](https://blogs.opera.com/news/2025/03/opera-browser-operator-ai-agentics/)).
- Strona wizji: [UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) (Apache-2.0) — jeden model
  wizyjny czyta zrzuty, a Agent TARS łączy GUI z DOM. Agent S3 rozdziela model „gdzie kliknąć" (UI-TARS-1.5-7B) od
  modelu rozumującego i z wyborem najlepszego z kilku przebiegów osiąga 72,6% w OSWorld wobec 72,36% człowieka
  ([Agent S](https://github.com/simular-ai/Agent-S)).

**Dlaczego działa.** DOM jest tańszy, stabilniejszy i pasuje do małych modeli bez wizji. Obraz jest potrzebny tylko
tam, gdzie interfejs to piksele (stare aplikacje, canvas, PDF w przeglądarce).

**U siebie.** DeepSeek-V4-Flash jest tylko tekstowy — więc DOM to naturalna ścieżka: Playwright MCP, agent-browser
albo browser-use z lokalnym endpointem ([klocki: agenci przeglądarkowi](../harnessy-agentowe/02-KLOCKI.md#agenci-przeglądarkowi)).
Wizja przez „mostek": osobny model wizyjny opisuje ekran, tekstowy wykonawca decyduje
([03-ARCHITEKTURA, U5](../harnessy-agentowe/03-ARCHITEKTURA.md#u5--zdjęcia-i-obrazy)).
**Uwaga na liczby producentów:** browser-use ogłosił 89,1% na WebVoyager po usunięciu 55 z 586 zadań, a na niezależnej
tablicy Online-Mind2Web ten sam stos z Claude Sonnet 4 miał 40,0%
([raport](https://browser-use.com/posts/sota-technical-report), [HAL](https://hal.cs.princeton.edu/online_mind2web)).

### 2.5. Ręce lokalnie, mózg gdzie indziej

**Co to jest.** Wykonanie (przeglądarka, pliki, VM) działa na maszynie użytkownika, a do modelu idą tylko obserwacje.

**Kto.** [Perplexity](01-PROFILE.md#15-perplexity) Comet według akt sprawy *Amazon v. Perplexity*: przeglądarka
użytkownika rozmawia ze stroną, robi zrzuty lokalnie, wysyła je na serwery Perplexity i dostaje instrukcje nawigacji
([Jones Day](https://www.jonesday.com/en/insights/2026/09/ninth-circuit-vacates-cfaa-injunction-against-perplexitys-comet-ai-agent)).
[Claude](01-PROFILE.md#2-claude): narzędzia computer use i browser use wykonuje aplikacja dewelopera, a Cowork uruchamia
lokalną maszynę wirtualną Linuksa przez Apple Virtualization — model nadal w chmurze
([Simon Willison](https://simonwillison.net/2026/Jan/12/claude-cowork/)). [Manus](01-PROFILE.md#6-manus) Browser Operator
używa lokalnej przeglądarki jako „aktuatora" ([Manus](https://manus.im/blog/manus-browser-operator)).

**Dlaczego działa.** Loginy i ciasteczka zostają u użytkownika, nie ma problemu „bot z serwerowni" (Manus sam radzi
bankowość robić przez lokalną przeglądarkę, bo adresy centrów danych wywołują blokady —
[dokumentacja](https://manus.im/docs/features/cloud-browser.md)).

**U siebie.** Ten podział jest gotowym szablonem — **wystarczy podmienić mózg na lokalny**. Dla danych klienta
obie połowy zostają na biurku; chmura może być „mózgiem" tylko dla treści, w której nigdy nie było danych klienta
(sekcja 4). Wzorzec planisty w chmurze i lokalnych wykonawców jest w
[03-ARCHITEKTURA, sekcja 2](../harnessy-agentowe/03-ARCHITEKTURA.md#2-wzorzec-planista-i-wykonawcy).

### 2.6. Piaskownica albo VM na zadanie

**Co to jest.** Każde zadanie (albo każda sprawa klienta) dostaje własne, odizolowane środowisko z dostępem tylko do
wskazanych folderów i z zamkniętym ruchem wychodzącym.

**Kto.**
- [Manus](01-PROFILE.md#6-manus) — mikro-VM Firecracker przez E2B, start ~150 ms; Docker odpadł przez 10–20 s startu
  ([E2B, 6.05.2025](https://e2b.dev/blog/how-manus-uses-e2b-to-provide-agents-with-virtual-computers)).
- [Claude](01-PROFILE.md#2-claude) Cowork — lokalna VM montuje tylko foldery, na które pozwolił użytkownik, i ogranicza
  sieć ([Simon Willison](https://simonwillison.net/2026/Jan/12/claude-cowork/)).
- Windows „agent workspace" — agent dostaje **własne konto Windows**, sześć znanych folderów i wybór „zawsze /
  pytaj za każdym razem / nigdy" ([Microsoft](https://support.microsoft.com/en-us/windows/experimental-agentic-features-a25ede8a-e4c2-4841-85a8-44839191dfb3)).
- NVIDIA [NemoClaw](https://github.com/NVIDIA/NemoClaw) owija OpenClaw piaskownicą OpenShell **domyślnie**, z akceptacją
  ruchu wychodzącego przez operatora; [NanoClaw](https://github.com/nanocoai/nanoclaw) daje kontener na grupę agentów.

**Dlaczego działa.** Szkoda po przejęciu agenta jest ograniczona do jednego folderu. **Ale:** PromptArmor pokazał, że
Cowork wysłał pliki ofiary na konto atakującego przez **dozwolone** API Anthropic z kluczem atakującego
([PromptArmor](https://www.promptarmor.com/resources/claude-cowork-exfiltrates-files)). Lista dozwolonych hostów
nie wystarcza, gdy dozwolony host przyjmuje dowolne poświadczenia.

**U siebie.** Jedna piaskownica na sprawę: srt albo bubblewrap dla powłoki, microsandbox dla kodu pisanego przez
agenta ([klocki: piaskownice](../harnessy-agentowe/02-KLOCKI.md#piaskownice)). Osobny użytkownik systemu dla agenta.
Ruch wychodzący domyślnie zamknięty; jeśli sprawa wymaga sieci — tylko lista domen i tylko przez proxy, które wpuszcza
wyłącznie Twoje poświadczenia. Kurs: [kurs 1, część 7](../kurs_lokalne_modele/07-SANDBOX-BEZPIECZENSTWO-MONITORING.md),
[kurs 2, część 10](../kurs_aplikacje_agentowe/10-PIASKOWNICA-PRODUKCYJNA.md).

### 2.7. Broker poświadczeń

**Co to jest.** Hasła i tokeny nigdy nie trafiają do promptu ani do piaskownicy. Agent dostaje uchwyt, a podstawienie
robi zaufany proces poza zasięgiem modelu — i tylko dla dozwolonej domeny.

**Kto.**
- Kortix: poświadczenia „są pośredniczone po stronie serwera przez jeden token o wąskim zakresie i nigdy nie wchodzą do
  maszyny" ([README](https://raw.githubusercontent.com/kortix-ai/suna/main/README.md)).
- Claude Code w chmurowych VM: poświadczenia GitHuba nie wchodzą do VM, cały ruch wychodzi przez proxy
  ([dokumentacja](https://code.claude.com/docs/en/data-usage)).
- [browser-use](01-PROFILE.md#13-browser-use): „secret bindings" przypięte do `allowedDomains`
  ([dokumentacja](https://docs.browser-use.com/cloud/choosing-an-agent)); NanoClaw ma bramkę poświadczeń
  ([README](https://github.com/nanocoai/nanoclaw)).
- Logowanie i 2FA oddaje się człowiekowi: Manus „Take Over", Gemini Spark oddaje strony logowania i płatności
  ([Manus](https://manus.im/docs/features/cloud-browser.md), [Google](https://support.google.com/gemini/answer/16596215)).
- Microsoft dosłał do OpenClaw maskowanie sekretów w promptach zatwierdzeń
  ([OpenClaw, 25.09.2026](https://openclaw.ai/blog/microsoft-autopilot-openclaw)).

**Dlaczego działa.** Model, który nie zna hasła, nie może go wyciec — ani przez prompt injection, ani do dziennika.

**U siebie.** Sejf (plik szyfrowany albo systemowy keyring) + proxy narzędzi: agent pisze `{{sekret:ksef}}`, proxy
podstawia wartość tylko w żądaniu do domeny przypisanej temu sekretowi i wycina ją z odpowiedzi i logów. Profil
zaufany (ePUAP), portale sądowe i bankowość — logowanie zawsze robi człowiek w przejętej sesji.

### 2.8. Zatwierdzenia skalowane wpływem na świat

**Co to jest.** O tym, czy agent pyta, decyduje **wpływ akcji na zewnątrz** i jej odwracalność, a nie to, czy model
„czuje się pewnie".

**Kto.**
- Lindy: „wszystko, co ma wpływ na zewnątrz, czeka na zatwierdzenie… wyszukiwania tylko do odczytu nie wymagają
  zatwierdzenia" ([cennik i FAQ](https://www.lindy.ai/pricing)).
- [browser-use](01-PROFILE.md#13-browser-use) — umiejętność „Agency" pyta tylko przed wysłaniem albo publikacją
  ([changelog, 17.08.2026](https://browser-use.com/changelog/3-4-2026)).
- [Claude](01-PROFILE.md#2-claude) w Chrome — potwierdzenia przed publikacją, zakupem i udostępnieniem danych osobowych
  oraz zablokowane kategorie stron ([Anthropic](https://claude.com/blog/claude-for-chrome)).
- OpenHands — tryby `AlwaysConfirm` / `ConfirmRisky`, model oznacza ryzyko akcji, a analizator wzorców łapie
  `rm -rf` i `curl | sh` ([dokumentacja](https://docs.openhands.dev/sdk/guides/security)).
- ZeroClaw — poziomy autonomii ReadOnly / Supervised / Full i podpisane HMAC zatwierdzenia
  ([harnessy](../harnessy-agentowe/01-PROFILE.md#10-zeroclaw)).
- Microsoft w Autopilocie: akcja o **nieznanym wyniku** nie jest automatycznie ponawiana
  ([OpenClaw](https://openclaw.ai/blog/microsoft-autopilot-openclaw)).

**Dlaczego działa.** Użytkownik nie jest zasypywany pytaniami o odczyty, a każda nieodwracalna akcja ma człowieka.
Akamai rekomenduje wiązać autonomię z odwracalnością akcji
([dqindia, 24.09.2026](https://www.dqindia.com/cybersecurity/akamai-warns-of-ai-browser-risks-as-enterprise-adoption-crosses-40-12570823)).

**U siebie.**

| Klasa akcji | Przykład | Decyzja |
|---|---|---|
| Odczyt lokalny | przeszukanie akt sprawy, OCR skanu | automatycznie |
| Szkic | projekt pisma, szkic e-maila w folderze „Szkice" | automatycznie, zostaje szkicem |
| Zapis w piaskownicy | nowy plik w katalogu sprawy | automatycznie, z punktem przywracania |
| Wpływ na zewnątrz | wysłanie e-maila, złożenie pisma, płatność, usunięcie | zawsze człowiek |
| Wynik nieznany | przerwane wysyłanie, timeout portalu | stop, bez ponowienia, pytanie do człowieka |

### 2.9. Umiejętności i przepisy

**Co to jest.** Powtarzalna procedura zapisana jako folder z plikiem Markdown (instrukcja, przykłady, skrypty), który
agent ładuje dopiero, gdy jest potrzebny.

**Kto.** [OpenClaw](01-PROFILE.md#1-openclaw) — `SKILL.md` i rejestr ClawHub; [Hermes Agent](01-PROFILE.md#5-hermes-agent)
sam pisze umiejętności po złożonych zadaniach, poprawia je w użyciu i skanuje przy instalacji
([dokumentacja](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)), a Hermes Business dzieli
„najlepsze umiejętności" w zespole ([Nous](https://portal.nousresearch.com/business)). Poke ma „przepisy" — automatyzacje
zwykłym tekstem, którymi użytkownicy się dzielą ([TechCrunch, 8.04.2026](https://techcrunch.com/2026/04/08/poke-makes-ai-agents-as-easy-as-sending-a-text/)).
LexisNexis ma w Protégé umiejętności swoje i partnerów, a własne umiejętności klientów zapowiada „wkrótce" (24.08.2026,
[LexisNexis](https://www.lexisnexis.com/community/pressroom/b/news/posts/lexis-with-protege-accelerates-frictionless-agentic-productivity-from-first-idea-to-review-ready-legal-work-product));
Cohere North 2 (5.10.2026) ma umiejętności wielokrotnego użytku ([Cohere](https://cohere.com/blog/introducing-north-2)).

**Dlaczego działa.** Prompt systemowy zostaje krótki (cache), a wiedza proceduralna jest wersjonowana i do przejrzenia.
**Ciemna strona:** otwarty rynek umiejętności to nowa powierzchnia ataku — sekcja 5.

**U siebie.** Katalog `umiejetnosci/` w gicie, po jednej na procedurę zawodu („przegląd umowy najmu", „zamknięcie
miesiąca VAT", „notatka z wizyty — kardiologia"). Nowa umiejętność napisana przez agenta trafia do kolejki do
przeglądu, nie od razu do użycia. Bez publicznego rynku — Moltis rezygnuje z niego celowo
([harnessy](../harnessy-agentowe/01-PROFILE.md#15-moltis)).

### 2.10. Pamięć ograniczona i pamięć w plikach

**Co to jest.** Pamięć to czytelne pliki z twardym limitem rozmiaru, które właściciel może otworzyć, poprawić i cofnąć.

**Kto.** [Hermes Agent](01-PROFILE.md#5-hermes-agent): `MEMORY.md` ≤ 2 200 znaków i `USER.md` ≤ 1 375 znaków; gdy
pamięć jest pełna, agent musi skonsolidować wpisy zamiast cicho je gubić
([dokumentacja](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)).
[OpenClaw](01-PROFILE.md#1-openclaw) wstrzykuje `SOUL.md`, `USER.md`, `MEMORY.md`, `AGENTS.md` w każdej sesji, a w tle
„śni": zapisuje `DREAMS.md` i promuje do `MEMORY.md` tylko mocne wpisy z wagą 1–10
([dreaming](https://docs.openclaw.ai/concepts/dreaming)). [Claude](01-PROFILE.md#2-claude) trzyma pamięć jako pliki
tematyczne do edycji, a tematów wrażliwych (zdrowie, przekonania) domyślnie nie zapisuje
([Anthropic, 25.08.2026](https://claude.com/resources/articles/claudes-memory-works-everywhere-and-you-decide-whats-in-it)).
[Harvey](01-PROFILE.md#4-harvey) II (18.08.2026) zamyka pracę w „Spaces" sprawy — dokumenty, strony, zadania, uprawnienia
([Harvey](https://www.harvey.ai/blog/introducing-harvey-ii)).

**Dlaczego działa.** Limit wymusza kurację (mniej śmieci w kontekście), stała migawka nie psuje cache, a plik da się
pokazać klientowi albo inspektorowi.

**U siebie.** Dwa poziomy: globalny `USER.md` (styl, preferencje — **bez danych klientów**) i `sprawy/<sygnatura>/pamiec.md`
ładowany tylko w sesji tej sprawy. Wskaźnik zapełnienia w UI („67% — 1 474/2 200"). Wszystko w gicie, więc „dlaczego
agent to wie?" ma odpowiedź w historii. Kurs: [kurs 2, części 5–6](../kurs_aplikacje_agentowe/05-PAMIEC-DLUGOTERMINOWA.md)
i [część 6](../kurs_aplikacje_agentowe/06-TOZSAMOSC-PLIKI-ROBOCZE.md).

### 2.11. Puls, cron i bramka skryptowa

**Co to jest.** Agent budzi się sam — z harmonogramu albo zdarzenia — ale **najpierw tani skrypt sprawdza, czy jest
co robić**, i dopiero wtedy wołany jest model.

**Kto.** [OpenClaw](01-PROFILE.md#1-openclaw): puls domyślnie co 30 min, wybudzenia zdarzeniami co najmniej 30 s
odstępu i blokada po 5 startach w 60 s ([heartbeat](https://docs.openclaw.ai/gateway/heartbeat)); „standing orders"
opisują zakres, wyzwalacz, bramkę zatwierdzenia i eskalację programu
([standing orders](https://docs.openclaw.ai/automation/standing-orders)). NanoClaw ma „bramki skryptowe", które nie
budzą modelu, gdy nie ma pracy ([README](https://github.com/nanocoai/nanoclaw)). Moltis może obsługiwać puls osobnym,
małym modelem lokalnym ([harnessy](../harnessy-agentowe/01-PROFILE.md#15-moltis)). ChatGPT Pulse liczy poranny brief
nocą ([TechCrunch](https://techcrunch.com/2025/09/25/openai-launches-chatgpt-pulse-to-proactively-write-you-morning-briefs/)),
a Google CC wysyła codzienny e-mail, na który się odpowiada ([Google](https://blog.google/technology/google-labs/cc-ai-agent/)).

**Dlaczego działa.** 9 na 10 przebudzeń to „nic nowego" — skrypt odpowiada na to za darmo, a model dostaje tylko
prawdziwe zdarzenia.

**U siebie.** Timer systemd → skrypt (nowy plik w folderze sprawy? nowa wiadomość w skrzynce kancelarii? nowa pozycja
w lokalnym lustrze Dziennika Ustaw?) → kolejka → model. Nocą GPU stoi bezczynnie — tam idą briefy, przegląd
tabelaryczny i ewaluacje. Kurs: [kurs 2, część 11](../kurs_aplikacje_agentowe/11-HARMONOGRAM-PROAKTYWNOSC.md);
klocki: [harmonogram](../harnessy-agentowe/02-KLOCKI.md#harmonogram-i-trwałe-wykonanie).

### 2.12. Komunikator jako interfejs

**Co to jest.** Asystent mieszka w aplikacji, której użytkownik i tak używa — nie trzeba instalować nic nowego.

**Kto.** [OpenClaw](01-PROFILE.md#1-openclaw) — jedna bramka dla WhatsApp, Telegram, Signal, iMessage, Teams, Matrix,
e-maila i innych ([dokumentacja](https://docs.openclaw.ai/llms.txt)). Poke — iMessage, SMS, Telegram, WhatsApp;
pierwszy agent AI zatwierdzony na Apple Messages for Business (4.06.2026) i „ponad 100 mln wiadomości w 3 miesiące"
*(dane firmy)* ([TechCrunch](https://techcrunch.com/2026/06/04/apple-approves-poke-as-the-first-ai-agent-on-its-messages-for-business-platform/),
[Cognition, 23.07.2026](https://cognition.com/blog/interaction)). **Lekcja z drugiej strony:** Apple na stałe zablokował
Lindy konto Apple ID w pół dnia; firma przepisała kanał trzy razy i pilnuje stosunku wysłanych do odebranych poniżej
~10:1 ([Lindy, 16.03.2026](https://www.lindy.ai/blog/imessage-api-three-rewrites-one-apple-ban-and-what-actually-works)).

**Dlaczego działa.** Zero wdrożenia po stronie użytkownika i naturalna proaktywność („agent pisze pierwszy").

**U siebie.** Komunikatory konsumenckie to cudza chmura i wroga platforma — **danych klienta tam nie wysyłasz**
(to samo ostrzeżenie przy Telegramie w [klockach](../harnessy-agentowe/02-KLOCKI.md#powiadomienia-i-kanały)).
Dla profesjonalisty kanałem jest: lokalna aplikacja webowa w sieci biura, e-mail przez serwer kancelarii (wzorzec
„DW do asystenta"), wtyczka Word — Spellbook i Noxtua siedzą w Wordzie
([Spellbook](https://www.spellbook.com/press), [Noxtua](https://www.noxtua.com/)) — i Matrix na własnym serwerze. Dla mojego osobistego asystenta Telegram jest OK
dla spraw niewrażliwych. Kurs: [kurs 2, część 12](../kurs_aplikacje_agentowe/12-KANALY-INTERFEJSY.md).

### 2.13. Głos

**Co to jest.** Mowa jako wejście (dyktowanie, notatki głosowe, nagranie wizyty) i wyjście (odczyt, rozmowa).

**Kto.** [Hermes Agent](01-PROFILE.md#5-hermes-agent) — notatki głosowe w komunikatorach z lokalnym faster-whisper, ale
**synteza mowy domyślnie przez chmurowy Edge TTS** ([harnessy](../harnessy-agentowe/01-PROFILE.md#4-hermes-agent)).
Moltis — lokalne STT i Piper z polskimi głosami, w pełni offline ([harnessy](../harnessy-agentowe/01-PROFILE.md#15-moltis)).
[Abridge](01-PROFILE.md#3-abridge) i Nabla mają własne medyczne ASR; Nabla trenowała na bazie Whispera plus 7 000 godzin
nagrań medycznych i **nigdy nie wkleja surowej transkrypcji do dokumentacji**
([Nabla](https://nabla.com/blog/assessing-the-reliability-of-nablas-speech-to-text-engine)).
[Sierra](01-PROFILE.md#11-sierra) dodała Voice Personas, a Decagon własny model mowy Chord
([Sierra](https://sierra.ai/blog), [Decagon](https://decagon.ai/blog)).

**Dlaczego działa.** Lekarz i adwokat mówią szybciej, niż piszą; nagranie to też najbogatsze źródło faktów.

**U siebie.** Kaskada STT → LLM → TTS, bo lokalnej mowy-do-mowy po polsku na AMD w październiku 2026 nie znalazłem;
szczegóły i opóźnienia w [03-ARCHITEKTURA, U4](../harnessy-agentowe/03-ARCHITEKTURA.md#u4--rozmowa-głosowa-po-polsku),
narzędzia w [klockach: głos](../harnessy-agentowe/02-KLOCKI.md#głos). Transkrypcja to produkt pośredni — notatkę
pisze LLM, a każde zdanie wskazuje fragment nagrania (2.14). Zbuduj własny test nazw leków i terminów prawniczych
po polsku, zanim komuś to sprzedasz.

### 2.14. Powiązane dowody i cytaty

**Co to jest.** Każde zdanie wyniku ma klikalny wskaźnik do źródła: fragmentu transkrypcji, strony dokumentu, przepisu.

**Kto.** [Abridge](01-PROFILE.md#3-abridge) — „Linked Evidence": każde zdanie notatki prowadzi do transkrypcji albo
nagrania; dodatkowy model-strażnik poprawia twierdzenia bez pokrycia i w wewnętrznym teście na 10 000+ wizyt złapał
97% takich twierdzeń wobec 82% dla GPT-4o *(dane firmy, 19.08.2025)*
([Abridge](https://www.abridge.com/ai/science-confabulation-hallucination-elimination)).
[OpenEvidence](01-PROFILE.md#12-openevidence) — RAG nad licencjonowaną literaturą (NEJM, JAMA, NCCN, Cochrane) z cytatami
w tekście ([Wikipedia](https://en.wikipedia.org/wiki/OpenEvidence)). Hebbia: „widać, skąd wzięła się każda liczba"
([Hebbia](https://www.hebbia.com/blog/introducing-matrix-2-0)); AlphaSense cytuje na poziomie zdania
([AlphaSense](https://www.alpha-sense.com/)). W Polsce LEX Expert AI (19.11.2025) linkuje każdą odpowiedź do źródeł
i fragmentów w LEX — to poprzeczka, do której polscy prawnicy są już przyzwyczajeni
([Prawo.pl](https://www.prawo.pl/prawnicy-sady/lex-expert-ai-nowym-narzedziem-dla-prawnikow)).

**Dlaczego działa.** Weryfikacja zdania trwa sekundy zamiast minut. Dla adwokata to warunek: § 23e Zbioru Zasad
Etyki Adwokackiej wymaga osobistej weryfikacji wyniku ([NRA, 12–13.06.2026](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/)).

**U siebie.** Każdy fragment z RAG ma identyfikator `{dokument, strona, przesunięcie}`; model musi zwrócić zdania
z listą identyfikatorów, a kod odrzuca zdanie bez cytatu. Drugie przejście — weryfikator dostaje **tylko** zdanie
i cytowany fragment i odpowiada „pokryte / niepokryte". Odpowiedź „nie wiem" jest dozwolona i nagradzana w ewaluacji.
Kurs: [kurs 1, część 4](../kurs_lokalne_modele/04-PAMIEC-RAG-I-KONTEKST.md) (cytowania).

### 2.15. Przegląd tabelaryczny

**Co to jest.** Siatka „N pytań × M dokumentów": wiersz to dokument, kolumna to pytanie, komórka to odpowiedź
z cytatem. Chat zamienia się w analityka wsadowego.

**Kto.** Hebbia Matrix wymyśliła ten interfejs; Matrix 2.0 (26.08.2026) prowadzi analizę do gotowych modeli, prezentacji
i memo z punktami kontroli człowieka przed każdym krokiem ([Hebbia](https://www.hebbia.com/blog/introducing-matrix-2-0)).
Skopiowali go Legora (Tabular Review), Thomson Reuters (Tabular Analysis do 10 000 dokumentów × 100 pytań —
[CoCounsel](https://legal.thomsonreuters.com/en/products/cocounsel-legal)) i [Noxtua](01-PROFILE.md#14-noxtua)
(Matrix Analysis). [Harvey](01-PROFILE.md#4-harvey) liczy koszt „na komórkę" — własny model Tenet ma ~1/10 kosztu
komórki w Review Table *(dane firmy)* ([Harvey, 20.08.2026](https://www.harvey.ai/blog/post-training-update-harvey-tenet)).

**Dlaczego działa.** Każda komórka to małe, niezależne, łatwe do sprawdzenia zadanie — idealne dla lokalnego modelu
i równoległych slotów. Wynik jest w formacie, którego profesjonalista używa (arkusz).

**U siebie.** Kolejka komórek z limitem 4 (sloty). Kolejność „dokument po dokumencie": w jednym slocie jeden dokument
jako stały prefiks i kolejne pytania, więc cache czyta dokument raz. Komórka = JSON
`{odpowiedź, cytat, strona, pewność}`, walidowany w kodzie; eksport do XLSX z linkami do stron PDF. Przepustowości
na moim rigu jeszcze **nie mierzyłem** — to dobry pierwszy pomiar.

### 2.16. Procedury w języku naturalnym

**Co to jest.** Zachowanie agenta opisuje ekspert dziedzinowy zwykłym językiem, a osobna, ukryta przed agentem
specyfikacja ocenia **przebieg**, nie tylko wynik.

**Kto.** Decagon — „Agent Operating Procedures": procedury w języku naturalnym, które zespół obsługi klienta zmienia
„bez sprintów inżynierskich" ([Decagon](https://decagon.ai/blog/series-d-announcement)). Basis — „behavior specs"
(29.07.2026), otwarty standard z Braintrust: specyfikacje oceniają trajektorię (prawda / fałsz / nie dotyczy) i „nigdy
nie są pokazywane agentowi", bo „poprawny wynik nie mówi, czy agent użył procesu, któremu zaufalibyśmy ponownie"
([Basis](https://www.getbasis.ai/blogs/behavior-specs-an-open-standard-for-supervising-long-horizon-agents)).
[OpenClaw](01-PROFILE.md#1-openclaw) — standing orders jako kontrakt uprawnień programu.

**Dlaczego działa.** Kontrolę nad zachowaniem ma prawnik albo księgowa, nie programista. Specyfikacja przebiegu łapie
„dobry wynik z przypadku".

**U siebie.** `procedury/wezwanie-do-zaplaty.md` pisane po polsku przez profesjonalistę („gdy klient przysyła
wezwanie sądowe, najpierw policz termin…") i obok `oceny/wezwanie-do-zaplaty.spec.md` z pytaniami o przebieg („czy
sprawdził białą listę VAT", „czy zacytował interpretację KIS") — tego pliku agent nie widzi.

### 2.17. Symulacja i powtarzalność

**Co to jest.** Zanim agent dostanie prawdziwych klientów, rozmawia z symulowanymi, a miarą jest nie „udało się raz",
tylko **pass^k** — czy udało się k razy z rzędu na tym samym zadaniu.

**Kto.** [Sierra](01-PROFILE.md#11-sierra) — τ-bench (20.06.2024) symuluje użytkowników i API pod regułami domeny;
GPT-4o spadł w handlu detalicznym do ~25% przy pass^8, o 60% względem pass^1
([Sierra](https://sierra.ai/blog/benchmarking-ai-agents)). Agent S3 kupuje niezawodność obliczeniami: kilka przebiegów
i sędzia wybierający najlepszy ([Agent S](https://github.com/simular-ai/Agent-S)).

**Dlaczego działa.** Profesjonalista potrzebuje przewidywalności bardziej niż szczytowej jakości. DeepSeek-V4-Flash
na moim trudnym zestawie ma 92/93 punktów, ale powtarzalność tylko 83
([03-ARCHITEKTURA](../harnessy-agentowe/03-ARCHITEKTURA.md#tryb-w-pełni-lokalny)).

**U siebie.** Symulator klienta na lokalnym modelu z personami per zawód, uruchamiany nocą: k = 8 przebiegów na zadanie,
raport pass^1 i pass^8. Lokalnie obliczenia nocą są prawie darmowe — w chmurze to by bolało (sekcja 5).

### 2.18. Własny model z otwartych wag

**Co to jest.** Bierzesz otwarty model bazowy i dotrenowujesz go (dalszy pretrening, SFT, RL) na danych dziedziny
i śladach zadań, zamiast płacić za model z czołówki przy każdej komórce.

**Kto.**
- [Harvey](01-PROFILE.md#4-harvey) Tenet (20.08.2026) — Kimi K3 po RL (GSPO) z Fireworks; dane syntetyczne, publiczne
  i eksperckie, „nie użyliśmy danych klientów"; −90% kosztu zapytania o wiedzę firmy *(dane firmy)*
  ([Harvey](https://www.harvey.ai/blog/post-training-update-harvey-tenet)). Wag nie opublikowano.
- [Cursor](01-PROFILE.md#9-cursor) Composer 2 (19.03.2026) — na otwartym Kimi K2.5 plus własny pretrening i RL; Cursor
  nie ujawnił bazy przy premierze, przyznał po odkryciu przez użytkownika
  ([Cursor](https://cursor.com/blog/composer-2), [Gigazine](https://gigazine.net/gsc_news/en/20260323-cursor-admits-composer-2-kimi)).
- Thomson Reuters — model „Thomson" na otwartej bazie, trenowany na Westlaw i Practical Law, pierwszy produkcyjny
  użytek to Tabular Analysis ([LawNext](https://www.lawnext.com/2026/08/thomson-reuters-says-its-homegrown-ai-model-now-rivals-the-frontier-labs-i-take-a-closer-look-at-the-benchmarks.html)).
- [Noxtua](01-PROFILE.md#14-noxtua) — poziom „Athena" na modelach open source w suwerennej infrastrukturze UE
  ([Noxtua](https://www.noxtua.com/)); w 2025 opisywała własny model trenowany na umowach
  ([TechCrunch](https://techcrunch.com/2025/04/22/noxtua-raises-92m-for-its-sovereign-ai-tuned-for-the-german-legal-system/)).
- Microsoft Fara-7B — mały model computer use trenowany na 145 tys. syntetycznych trajektorii z większego agenta
  ([MSR](https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/)).

**Dlaczego działa.** Wąskie, mierzalne zadania (ekstrakcja, komórka tabeli) nie potrzebują modelu z czołówki — potrzebują
modelu dopasowanego. Własne wagi to też suwerenność.

**U siebie.** Kolejność: najpierw prompty i DSPy z Opusem jako nauczycielem
([klocki](../harnessy-agentowe/02-KLOCKI.md#niezawodność-wywołań-narzędzi-i-strojenie-promptów)), potem dotrenowanie
**mniejszego** modelu (Bielik-11B, Qwen 27B) na własnych śladach do jednej czynności. 284-miliardowego DeepSeeka na
4× R9700 nie dotrenujesz — tego nawet nie próbuję. Dwie zasady z cudzych błędów: ujawniaj model bazowy (Cursor)
i nie trenuj na danych klientów bez zgody (Harvey robi z tego argument).

### 2.19. Router i hybryda modeli

**Co to jest.** Kod decyduje, który model obsłuży krok — według wrażliwości danych, trudności i kosztu.

**Kto.** [Harvey](01-PROFILE.md#4-harvey) — routing po zadaniu, przełączenie przy awarii dostawcy, administrator wybiera
dozwolone modele ([Harvey](https://www.harvey.ai/en-US/blog/why-harvey-is-multi-model-by-design)). Genspark — „mixture
of agents" na 30+ modelach; Perplexity Computer — 19 modeli z podagentami
([TechCrunch, 27.02.2026](https://techcrunch.com/2026/02/27/perplexitys-new-computer-is-another-bet-that-users-need-many-ai-models/)).
Glean Tau: 0,58 USD wobec 2,98 USD za zadanie w porównaniu z Claude Cowork *(benchmark producenta, 27.08.2026)*
([itbrief](https://itbrief.asia/story/glean-launches-tau-to-cut-enterprise-ai-token-costs)).
[Noxtua](01-PROFILE.md#14-noxtua): „Athena" (otwarte modele, suwerenne) albo „Minerva" (modele z czołówki w układzie
europejskim) — wybór per sprawa ([Noxtua](https://www.noxtua.com/security)).

**Dlaczego działa.** Większość kroków jest prosta; drogi model tylko tam, gdzie się zwraca. **Pułapka:** wybór modelu
potrafi po cichu przenieść dane — w Microsoft 365 Copilot modele Anthropic jako podprocesor są wyłączone z EU Data
Boundary ([Microsoft](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy)).

**U siebie.** Pierwsza reguła routera to **wrażliwość**, druga trudność: „dane klienta → tylko lokalnie" jest twardą
regułą w kodzie, nie decyzją modelu. Bramka i limity: [klocki](../harnessy-agentowe/02-KLOCKI.md#bramka-i-routing-modeli),
kurs: [kurs 2, część 17](../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md),
[kurs 1, część 10](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md).

### 2.20. Notatki ze spotkań bez bota

**Co to jest.** Aplikacja nagrywa dźwięk z mikrofonu i systemu na urządzeniu — żaden bot nie dołącza do rozmowy — a LLM
rozwija **notatki użytkownika** w pełną notatkę.

**Kto.** [Granola](01-PROFILE.md#10-granola): dwa kanały dają darmową diaryzację „Ja / Oni", nagranie nie jest zapisywane,
zostaje tylko transkrypcja; ASR i LLM w chmurze ([dokumentacja](https://docs.granola.ai/help-center/taking-notes/transcription)).
Ciemna strona: w 7.2026 prasa opisała notatki domyślnie udostępniane linkiem i trenowanie domyślnie włączone w planach
Free i Business, a 30.07.2026 złożono pozew zbiorowy *Chamberlain v. Granola*
([ppc.land](https://ppc.land/granola-sued-for-recording-meetings-without-consent-to-train-ai-models/)).
Jamie (UE) też nagrywa na urządzeniu, ale przetwarza w chmurze i kasuje audio ([Jamie](https://www.meetjamie.ai/)).

**Dlaczego działa.** Brak bota usuwa tarcie społeczne, a notatki użytkownika mówią modelowi, co było ważne.

**U siebie.** Nagrywanie mikrofonu i pętli systemowej jako dwóch ścieżek → whisper.cpp albo Parakeet → diaryzacja po
kanale → LLM scala z notatkami i szablonem typu spotkania → audio kasowane po transkrypcji. Zgoda uczestników na
nagrywanie to kwestia prawna, którą musisz sprawdzić dla swojej sytuacji — to nie jest porada prawna.

---

## 3. Offline: co naprawdę działa bez internetu

**„Tak"** oznacza: produkt sam działa bez internetu (otwarty kod + lokalny model). Usługi chmurowe dostają **„Nie"** —
nawet jeśli część wykonania jest lokalna. Szczegóły w profilach [01-PROFILE.md](01-PROFILE.md).

| Asystent | Kod | Offline | Co działa lokalnie | Czego brakuje / co podmienić |
|---|---|---|---|---|
| [OpenClaw](01-PROFILE.md#1-openclaw) | otwarty (MIT) | Tak | pętla, pamięć, puls i cron z lokalnym modelem; CLI, TUI i lokalny web UI ([docs](https://docs.openclaw.ai/gateway/local-models)) | kanały WhatsApp / Telegram / Signal wymagają sieci; lokalne modele „nie mają filtrów bezpieczeństwa dostawców"; piaskownica nie jest domyślna — dodaj NemoClaw albo srt |
| [Claude](01-PROFILE.md#2-claude) | zamknięty | Nie | narzędzia computer use / browser use wykonuje Twoja maszyna; VM Cowork jest lokalna; klient Claude Code lokalny | model tylko w chmurze — lokalny LLM + własna pętla z tym samym podziałem „mózg / ręce" |
| [Abridge](01-PROFILE.md#3-abridge) | zamknięty | Nie | tylko nagrywanie na telefonie lub w aplikacji EHR | whisper.cpp + lokalny LLM + weryfikator + powiązane dowody (2.13, 2.14) |
| [Harvey](01-PROFILE.md#4-harvey) | zamknięty | Nie | nic — SaaS; Tenet bez publicznych wag | lokalny model + RAG z cytatami + przegląd tabelaryczny (2.14, 2.15) |
| [Hermes Agent](01-PROFILE.md#5-hermes-agent) | otwarty (MIT) | Tak | pętla z lokalnym endpointem, STT faster-whisper, pamięć w plikach, cron | **TTS domyślnie Edge TTS (chmura)** — zamień na Piper; kanały komunikatorów wymagają sieci; instalator promuje płatny Nous Portal |
| [Manus](01-PROFILE.md#6-manus) | zamknięty | Nie | lokalna przeglądarka jako aktuator (Browser Operator) | VM na zadanie lokalnie (microsandbox), lokalny model, sześć reguł kontekstu (2.1, 2.6) |
| [ChatGPT](01-PROFILE.md#7-chatgpt) | zamknięty | Nie | nic w produkcie (prasa podaje otwarcie samego harnessu Codex, 29.09.2026) | wszystko — pętla, VM, przeglądarka, model |
| [Gemini](01-PROFILE.md#8-gemini) | zamknięty | Nie | Chrome auto browse działa w przeglądarce użytkownika; model w chmurze; Gemini Spark niedostępny w EOG | krytyk, zbiory źródeł i deterministyczne potwierdzenia przenieś do własnej pętli (2.3) |
| [Cursor](01-PROFILE.md#9-cursor) | zamknięty | Nie | edytor; wykonanie na „Self-Hosted Machines"; każde zapytanie przechodzi przez backend Cursora, nawet z własnym kluczem | Cline albo OpenCode z lokalnym modelem ([harnessy](../harnessy-agentowe/01-PROFILE.md#8-opencode)) |
| [Granola](01-PROFILE.md#10-granola) | zamknięty | Nie | przechwycenie mikrofonu i dźwięku systemowego | lokalne STT + diaryzacja po kanale + lokalny LLM (2.20) |
| [Sierra](01-PROFILE.md#11-sierra) | zamknięty | Nie | nic; otwarta jest metoda (τ-bench) | symulator klienta i pass^k na lokalnym modelu (2.17) |
| [OpenEvidence](01-PROFILE.md#12-openevidence) | zamknięty | Nie | nic | lokalny RAG nad polskimi wytycznymi towarzystw, ChPL i rekomendacjami AOTMiT — łatwy do zrobienia offline |
| [browser-use](01-PROFILE.md#13-browser-use) | otwarty (MIT) | Częściowo | biblioteka z lokalnym endpointem zgodnym z OpenAI; strony w intranecie | strony w internecie wymagają sieci; BU 2.0, przeglądarki „stealth" i agenci V3/V4 tylko w chmurze; małe modele zwracają złe schematy akcji |
| [Noxtua](01-PROFILE.md#14-noxtua) | zamknięty | Nie | wtyczki Word i Outlook to klienci; modele w suwerennej chmurze UE (DE, CH) | „suwerenność" to tu chmura UE, nie biurko — lokalny odpowiednik: otwarty model + RAG nad ISAP i SAOS |
| [Perplexity](01-PROFILE.md#15-perplexity) | zamknięty | Nie | Comet wykonuje akcje i robi zrzuty w lokalnej przeglądarce; rozumowanie na serwerach Perplexity | ta sama architektura z lokalnym modelem; świeże wyszukiwanie offline jest niemożliwe |

Źródła wierszy: profile w [01-PROFILE.md](01-PROFILE.md); ChatGPT/Codex — [Decrypt](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced);
Gemini Spark poza EOG — [Google](https://support.google.com/gemini/answer/16596215); Cursor —
[dane i prywatność](https://cursor.com/data-use); browser-use — [model BU 2.0](https://docs.browser-use.com/open-source/bu-2-0-model-card)
i [klocki](../harnessy-agentowe/02-KLOCKI.md#agenci-przeglądarkowi).

**Wniosek:** z piętnastu tylko trzy da się uruchomić lokalnie (dwa w pełni, browser-use częściowo), i wszystkie trzy
to otwarte narzędzia, nie produkty dla profesjonalistów. **Nikt z czołówki nie sprzedaje polskiemu prawnikowi czy lekarzowi asystenta, który działa na
biurku** — to jest luka, którą opisuję w sekcji 4.

### Funkcja → lokalny zamiennik

| Funkcja | Lokalny zamiennik (otwarty) | Co jest słabe offline |
|---|---|---|
| LLM — rozumowanie | mój rig: DeepSeek-V4-Flash (tylko tekst); na biurko: Qwen3.6-27B, Gemma-4-31B, gpt-oss-120b; Bielik-11B-v3 do polskiego stylu | najlepszy otwarty model w PLCC ma 89,83 wobec 92–97 dla zamkniętych (8.10.2026); zamiana Opusa na mały model kosztowała w OpenJarvis 25–39 pp |
| Embeddingi i RAG | llama-swap serwuje też embeddingi; baza wektorowa w SQLite + BM25 + reranking ([kurs 1, część 4](../kurs_lokalne_modele/04-PAMIEC-RAG-I-KONTEKST.md)); SQLite FTS5 jak w Hermesie; Cognee bez klucza chmurowego | najlepsze wyszukiwanie przepisów na pytaniach z egzaminów na aplikacje: 72,3% top-1 (BM25: 61,7%) — wyszukiwanie wymaga własnych testów |
| STT | whisper.cpp large-v3 (WER 4,74% FLEURS-pl), Parakeet-TDT-0.6B-v3 na CPU (7,31%), faster-whisper | polskie słownictwo medyczne i jakość mikrofonu w gabinecie — niezweryfikowane |
| TTS | Piper pl_PL (CPU, brzmi robotycznie), Chatterbox Multilingual V3 (MIT, znak wodny), VoxCPM2 | jakość polskiego TTS; Kokoro tylko EN; brak lokalnej mowy-do-mowy po polsku na AMD |
| OCR i wizja | Docling + PaddleOCR-VL-1.5 (mało VRAM, działa na CPU); Qwen3.6-35B-A3B; test DeepSeek-V4-Flash-Vision-Exp | DeepSeek-V4-Flash nie widzi obrazów; modele wizyjne słabo wykorzystują obraz w polskich pytaniach medycznych |
| Wyszukiwanie w sieci | SearXNG (wymaga internetu); offline: lokalne lustra ISAP / ELI, SAOS, ChPL, wytycznych — synchronizowane osobnym procesem | świeża wiedza z sieci offline jest niemożliwa; lustro ma datę |
| Kalendarz i e-mail | IMAP / SMTP do serwera biura, CalDAV (np. Nextcloud on-prem), szkice wprost w skrzynce, wzorzec „DW do asystenta" | wysłanie wiadomości z definicji wymaga sieci; kalendarze w chmurze odpadają |
| Computer use | DOM: browser-use, Playwright MCP (drzewo dostępności, bez wizji), agent-browser; GUI: UI-TARS-desktop + UI-TARS-1.5-7B, Holo4-35B-A3B, Fara-7B | długie zadania: w OSWorld 2.0 (6.2026) najlepszy model z czołówki ukończył 20,6%; 7B na OSWorld ~27,5% |
| Kanały | lokalna aplikacja webowa / PWA w sieci biura, Matrix na własnym serwerze, Gotify, ntfy hostowany samemu | WhatsApp, iMessage, Telegram to cudza chmura z definicji; natychmiastowe push na iOS wymaga przekaźnika ntfy.sh |
| Moderacja i injection | Bielik-Guard 0.5B (polski klasyfikator szkód), BrowseSafe (otwarte wagi, wykrywanie injection) | BrowseSafe przepuszcza ~10% ataków (12.2025); Bielik-Guard: precyzja 75,28% |

Źródła: [klocki](../harnessy-agentowe/02-KLOCKI.md) (głos, obraz, wyszukiwanie, kanały, pamięć);
[03-ARCHITEKTURA, sekcja 3](../harnessy-agentowe/03-ARCHITEKTURA.md#3-co-jest-udowodnione-a-co-nie) (OpenJarvis);
PLCC — [sdadas/plcc](https://huggingface.co/spaces/sdadas/plcc); wyszukiwanie przepisów —
[arXiv 2608.30929](https://arxiv.org/abs/2608.30929); wizja medyczna PL — [arXiv 2608.12928](https://arxiv.org/abs/2608.12928);
OSWorld 2.0 — [arXiv 2606.29537](https://arxiv.org/abs/2606.29537); UI-TARS-1.5-7B —
[karta modelu](https://huggingface.co/ByteDance-Seed/UI-TARS-1.5-7B); Bielik-Guard —
[karta modelu](https://huggingface.co/speakleash/Bielik-Guard-0.5B-v1.1); BrowseSafe —
[the-decoder](https://the-decoder.com/perplexitys-browsesafe-tries-to-patch-the-gaping-security-holes-inherent-in-ai-browser-agents/).

---

## 4. Architektura referencyjna lokalnego asystenta na biurko

Cel: asystent dla kancelarii, gabinetu albo biura rachunkowego, w którym **dane klienta nie opuszczają biurka**.
To projekt złożony z wzorców z sekcji 2 — **niezmierzony**, dopóki go nie zbudujesz.

```text
              BIURO (sieć lokalna)                                 |  INTERNET
                                                                   |
  przeglądarka / PWA   wtyczka Word   e-mail biura   nagrywanie    |
        \                 |              |             /           |
         +----------------+------+-------+------------+            |
                                 v                                 |
  +------------------- SKRZYNKA NA BIURKU (szyfrowany dysk) ----+  |
  | ORKIESTRATOR  pętla · plan.md · procedury · puls + bramki   |  |
  |   |  router: dane klienta -> tylko lokalnie                 |  |
  |   v                                                         |  |
  | MODELE (llama-swap)       NARZĘDZIA (MCP, tylko odczyt)     |  |
  |  główny LLM               RAG sprawy z cytatami             |  |
  |  Bielik (styl PL)         przegląd tabelaryczny -> XLSX     |  |
  |  mały model: krytyk       szkice pism i e-maili             |  |
  |  STT · TTS · OCR          DOM-przeglądarka (lista domen)    |  |
  |   |                         |                               |  |
  | PAMIĘĆ: USER.md · sprawy/<sygnatura>/ · indeks · lustra     |  |
  | WYKONANIE: piaskownica na sprawę · osobny użytkownik        |  |
  | NADZÓR: zatwierdzenia wg wpływu · broker poświadczeń        |  |
  | DZIENNIK: zdarzenia append-only · notatka o narzędziach     |  |
  +--------------------------+----------------------------------+  |
                             | firewall wyjścia: domyślnie NIE    |
                             +--- tylko: aktualizacje podpisane ---+--> serwer aktualizacji
                             +--- tylko: lustra ISAP / SAOS -------+--> źródła publiczne
                             +--- opcja: planista hybrydowy -------+--> Opus (tylko dane
                                  (wyłączona domyślnie)            |    bez klienta)
```

| Warstwa | Komponent | Wzorzec | Uwagi |
|---|---|---|---|
| Kanały | aplikacja webowa / PWA w LAN, wtyczka Word, e-mail biura | 2.12 | bez komunikatorów konsumenckich dla danych klienta |
| Orkiestrator | własna pętla albo Pydantic AI; `plan.md`; procedury per zawód | 2.2, 2.16 | limit współbieżności w jednym miejscu |
| Modele | główny LLM + Bielik-11B-v3 + mały model krytyka + STT / TTS / OCR | 2.3, 2.19 | tylko wagi z licencją komercyjną (Apache-2.0, MIT) |
| Wiedza | RAG nad folderami spraw i skrzynką; lokalne lustra ISAP / ELI i SAOS | 2.14 | cytat albo „nie wiem" |
| Praca wsadowa | przegląd tabelaryczny, briefy nocne | 2.11, 2.15 | GPU nocą |
| Pamięć | `USER.md` bez danych klientów, pamięć per sprawa, git | 2.10 | limit znaków i wskaźnik zapełnienia |
| Wykonanie | piaskownica na sprawę, osobny użytkownik systemu | 2.6 | egress domyślnie zamknięty |
| Nadzór | zatwierdzenia wg wpływu, krytyk, broker poświadczeń | 2.7, 2.8 | logowanie i 2FA zawsze człowiek |
| Dziennik | zdarzenia append-only, eksport „notatki o narzędziach" per sprawa | sekcja 5 | sam dziennik to dane osobowe — retencja i szyfrowanie |
| Ewaluacja | złote zestawy per zawód, pass^k, testy PLCC / CPTUB przed zmianą modelu | 2.17, sekcja 5 | przed każdą aktualizacją modelu |

### Zasady przepływu danych

1. **Dane klienta nie wychodzą z pudełka.** Model, indeks, dzienniki i kopie są lokalne. Wtedy dla części AI nie ma
   podmiotu przetwarzającego (art. 28 RODO) ani transferu poza EOG (rozdział V RODO)
   ([RODO](https://eur-lex.europa.eu/eli/reg/2016/679/oj)). To działa tylko, jeśli serwis i aktualizacje dostawcy
   nie sięgają do danych — więc podpisane paczki aktualizacji, bez zdalnej powłoki domyślnie.
2. **Ruch wychodzący jest jednokierunkowy i nie niesie danych klienta.** Osobny proces pobiera aktualizacje i lustra
   źródeł publicznych; proces z dostępem do spraw nie ma sieci. Wzorzec znany z Ghost (zapora wyjścia jako funkcja
   zaufania — [TechCrunch, 5.10.2026](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/)).
3. **Planista hybrydowy (Opus) jest opcją, wyłączoną domyślnie, i dostaje tylko treść, w której nigdy nie było danych
   klienta**: pytania o przepisy w oderwaniu od sprawy, kod narzędzi, szablony, procedury. Dlaczego nie „zanonimizowane
   akta": dane spseudonimizowane nadal są danymi osobowymi (motyw 26 RODO), ponowna identyfikacja to opisane ryzyko
   systemów LLM ([EDPB, 10.04.2025](https://www.edpb.europa.eu/our-work-tools/our-documents/support-pool-experts-projects/ai-privacy-risks-mitigations-large_pt)),
   dostawca z USA podlega CLOUD Act ([18 U.S.C. § 2713](https://www.law.cornell.edu/uscode/text/18/2713)), a § 23e
   ZZEA zabrania udostępniania informacji poufnych narzędziom bez „należytej ochrony". „Lokalny wykonawca jako filtr
   prywatności" z [03-ARCHITEKTURA](../harnessy-agentowe/03-ARCHITEKTURA.md#tryb-w-pełni-lokalny) też jest modelem —
   może się pomylić. Szerzej: [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md). To nie jest porada prawna.
4. **Pełne szyfrowanie dysku, osobne konta, kopie szyfrowane.** Skradzione pudełko bez szyfrowania to naruszenie
   w rozumieniu art. 33–34 RODO.

### Rozmiar sprzętu

Ceny, dostępność i pomiary konkretnych pudełek są w [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md). Tu
tylko, co musi się zmieścić w pamięci — to mój szacunek z rozmiarów wag, nie pomiar:

| Klasa pamięci | Co się mieści | Dla kogo |
|---|---|---|
| 16–24 GB | gpt-oss-20b (mieści się w 16 GB), Bielik-11B-v3 albo Bielik-Minitron-7B | solo — czat i szkice, bez ciężkiego rozumowania |
| 32–64 GB | Qwen3.8-27B (Q4 ~18,5 GB) albo Qwen3.6-35B-A3B (Q4 ~23 GB) + Bielik + whisper | solo albo 2–3 osoby, przegląd tabelaryczny w kolejce |
| 128 GB | gpt-oss-120b albo Gemma-4-31B w wyższej precyzji + Bielik + wizja + STT naraz | biuro 1–5 osób, RAG nad aktami |

Dwie twarde reguły: **dla agentów co najmniej Q4** — w PolAgentBench Bielik-11B-v3, Bielik-Minitron-7B i
Llama-PLLuM-8B „spadają z klifu" między 3 a 2 bitami ([arXiv 2609.32042](https://arxiv.org/abs/2609.32042));
i **tylko wagi z licencją komercyjną** — modele PLLuM „-nc" odpadają. Rozmiary modeli: [karta gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b),
[Bielik-11B-v3](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct), [klocki: obraz](../harnessy-agentowe/02-KLOCKI.md#obraz).

### Wariant na moim rigu

4× R9700, DeepSeek-V4-Flash w 3 bitach (104,2 GB), `--parallel 4` po 131k, ~1,4 GB wolnego VRAM na kartę
([03-ARCHITEKTURA, sekcja 1](../harnessy-agentowe/03-ARCHITEKTURA.md#1-zasoby-co-naprawdę-masz)). Model jest
**tylko tekstowy**, więc wszystko „zmysłowe" idzie obok:

| Zasób | Rola |
|---|---|
| Slot 1 | orkiestrator i planista (myślenie włączone), synteza wyników |
| Sloty 2–3 | wykonawcy: komórki przeglądu tabelarycznego, ekstrakcja, szkice (3 naraz to zmierzone optimum) |
| Slot 4 | rezerwa na rozmowę interaktywną, żeby użytkownik nie czekał w kolejce za pracą wsadową |
| CPU | `gpt-oss-20b-cpu` jako krytyk, router i triaż pulsu; Parakeet (STT), Piper (TTS), Smart Turn |
| CPU albo zwolniona karta | Docling + PaddleOCR-VL do skanów; Qwen3.6-35B-A3B do zrzutów ekranu po wymianie w llama-swap |
| Opcja | test DeepSeek-V4-Flash-Vision-Exp (ten sam rozmiar + ~0,93 GB) — eksperymentalny |

Konsekwencja dla wzorców: przy ~13,6 tok/s na agenta **prompt cache i krótkie wyjścia JSON są ważniejsze niż wybór
harnessu** (2.1), a krytyk i bramki pulsu muszą działać na CPU, bo GPU jest pełne.

### Minimalny produkt (MVP)

1. Czat po polsku nad folderem sprawy — każda odpowiedź z cytatem do strony dokumentu albo „nie wiem" (2.14).
2. Przegląd tabelaryczny „pytania × dokumenty" z eksportem do XLSX (2.15).
3. Szkice pism i e-maili — **nigdy** wysyłka (2.8).
4. Transkrypcja nagrania (spotkanie, wizyta, dyktowanie) i notatka z szablonu z linkami do fragmentów (2.13, 2.20).
5. Procedury i umiejętności per zawód pisane przez profesjonalistę (2.9, 2.16).
6. Dziennik zdarzeń i eksport „notatki o narzędziach" per sprawa (sekcja 5).
7. Zero ruchu wychodzącego z danymi, szyfrowany dysk, kopie (sekcja 4, zasady).

Poza MVP: computer use na zewnętrznych portalach, komunikatory, rozmowa głosowa na żywo, planista hybrydowy.

### Etapy

| Etap | Co | Kryterium przejścia |
|---|---|---|
| 0 — ewaluacja | 30–50 prawdziwych zadań na zawód, specyfikacje przebiegu, test PLCC / CPTUB wybranych modeli | znasz pass^1 i pass^8 na własnych zadaniach |
| 1 — MVP | punkty 1–7 wyżej, jeden zawód, jedno biuro pilotażowe | profesjonalista weryfikuje odpowiedź szybciej niż pisze sam |
| 2 — proaktywność | timery + bramki skryptowe: nowe pismo w folderze, nowa pozycja w lustrze Dziennika Ustaw, poranny brief | brak „pustych" wywołań modelu w dzienniku |
| 3 — działanie | DOM-przeglądarka na portalach (KSeF, e-Sąd, ePUAP) ze zbiorami źródeł, krytykiem i brokerem poświadczeń | zero akcji z wpływem na zewnątrz bez zatwierdzenia |
| 4 — rozwój | dyktowanie i głos, dotrenowany mały model do jednej czynności, opcjonalna hybryda dla treści bez danych klienta | koszt komórki spada, jakość w złotym zestawie nie |

---

## 5. Ewaluacja i bezpieczeństwo

### Prompt injection w agentach przeglądarkowych

**Przyczyna jest strukturalna:** agent działa z sesjami użytkownika, więc polityka same-origin już nie chroni —
instrukcje może nieść każda strona, e-mail, zaproszenie z kalendarza czy obraz
([Brave](https://brave.com/blog/comet-prompt-injection/)). OpenAI (22.12.2025): prompt injection jest „mało
prawdopodobne, by kiedykolwiek został w pełni rozwiązany"
([TechCrunch](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/)).
Gartner (8.12.2025) radził firmom blokować przeglądarki AI
([The Register](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/)).

Co już się wydarzyło:
- **Comet:** atak bez kliknięcia przez zaproszenie z kalendarza — wyciek lokalnych plików i poświadczeń z 1Password
  ([The Register, 3.03.2026](https://www.theregister.com/2026/03/03/perplexity_comet_browser_hole_cal_invite/)).
- **BragJack** (19.09.2026): jedno złośliwe rozszerzenie „wymusza prompt" w Chrome Gemini, Edge Copilot, Comet, Opera Neon
  i Claude w Chrome ([BleepingComputer](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/)).
- **Cowork:** ukryty biały tekst w dokumencie → wysyłka plików przez dozwolone API (2.6).
- Obrona działa, ale nie do końca: Anthropic obniżył skuteczność ataków na Claude w Chrome z 23,6% do 11,2%, a dla
  Opus 4.5 podaje ~1% przy adaptacyjnym atakującym *(dane firmy, 2025)*
  ([Anthropic](https://www.anthropic.com/research/prompt-injection-defenses)); BrowseSafe wykrywa 91% w < 0,5 s, ale
  ~10% ataków przechodzi *(12.2025)*.

Najlepszy opisany wzorzec po stronie wykonania ma [Harvey](01-PROFILE.md#4-harvey) (7.10.2026): sprawdzenie każdego
wywołania narzędzia, „przypinanie" definicji narzędzi przeciw ich podmianie, polityki Rego blokujące „śmiertelną
trójcę" (dane prywatne + niezaufana treść + komunikacja na zewnątrz) i usuwanie ukrytych znaków Unicode z wyników
narzędzi — **egzekwowane poza modelem** ([Harvey](https://www.harvey.ai/blog/building-harveys-mcp-policy-engine)).

**Lokalnie usuwasz wyciek do chmury, ale nie prompt injection.** Stąd: agent czyta, a nie pisze; osobny profil
przeglądarki bez głównych sesji użytkownika; zbiory źródeł; brak `file://` i menedżera haseł; klasyfikator injection
lokalnie; i reguła trójcy w kodzie — sesja, która czytała niezaufaną treść, traci narzędzia komunikacji na zewnątrz.
Kurs: [kurs 2, część 16](../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md).

### Lekcja z porad bezpieczeństwa OpenClaw

[OpenClaw](01-PROFILE.md#1-openclaw) opublikował w 2026 roku **722 porady bezpieczeństwa** (14 krytycznych, 249 wysokich,
390 średnich, 69 niskich; API GitHuba, 11.10.2026). Steinberger podaje, że z 1 309 zgłoszeń od 10.01 aż 746 zamknięto
jako nieważne, a 87% „krytycznych" było nieważnych
([OpenClaw, 30.04.2026](https://openclaw.ai/blog/openclaw-security-in-public)). Prawdziwe problemy były gdzie indziej:
- **Rynek umiejętności.** Cisco znalazł co najmniej jedną podatność w 26% z 31 000 przeanalizowanych umiejętności
  agentów i umiejętność, która po cichu wysyłała dane `curl`em
  ([Cisco, 28.01.2026](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare)).
- **Piaskownica nie jest domyślna** — „workspace to domyślny katalog roboczy, nie twarda piaskownica", nawet w 2.0
  ([docs](https://docs.openclaw.ai/concepts/agent-workspace),
  [The Register](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492)).
- **Odpowiedzi:** skanowanie VirusTotal, NVIDIA SkillSpector, Tencent ClawScan (86,9% zgodnych etykiet, 98,6%
  złośliwych umiejętności złapanych na 556 przypadkach *(dane projektu)*), wyniesienie kanałów i narzędzi z rdzenia do
  wtyczek ([ClawScan](https://openclaw.ai/blog/tencent-aig-joins-clawscan)) — a Microsoft dosłał kontrolę zgodności
  instalacji z polityką firmy.

Wnioski dla mnie: **mały rdzeń, brak otwartego rynku, piaskownica domyślnie, przypięte wersje, kontrola zgodności
konfiguracji z zapisem dla inspektora**. Liczba porad nie mierzy bezpieczeństwa — Hermes nie ma żadnej opublikowanej
w 2026, co może wynikać ze sposobu zgłaszania, nie z braku błędów.

### pass^k i złote zestawy per zawód

Benchmarki ogólne nasycają się: OSWorld przekroczył poziom człowieka, ale na OSWorld 2.0 (zadania ~1,6 h) najlepszy model
ukończył 20,6%, bo agenci „gubią ograniczenia, zgadują zamiast pytać i pomijają weryfikację"
([arXiv 2606.29537](https://arxiv.org/abs/2606.29537)). Liczy się **Twój** zestaw:

| Zawód | Złoty zestaw (30–50 zadań) | Co mierzysz | Punkt odniesienia |
|---|---|---|---|
| Adwokat / radca | wyszukanie przepisu do stanu faktycznego, przegląd umowy, termin procesowy | trafność cytatu, „nie wiem" gdy trzeba | 72,3% top-1 przy wyszukiwaniu przepisów ([arXiv 2608.30929](https://arxiv.org/abs/2608.30929)); żaden LLM nie zdał części praktycznej egzaminu KIO ([arXiv 2511.04205](https://arxiv.org/abs/2511.04205)) |
| Lekarz | notatka z nagrania wizyty, pytanie o ChPL, kod rozpoznania | zdania bez pokrycia w nagraniu, nazwy leków | ostrzejsze punktowanie obniżyło wyniki o 31 pp na polskich egzaminach ([arXiv 2606.12250](https://arxiv.org/abs/2606.12250)) |
| Doradca / księgowa | dekretacja z KSeF XML, kwalifikacja VAT z interpretacją KIS | specyfikacja przebiegu (biała lista, cytat interpretacji) | wzorzec „agent przygotowuje, człowiek przegląda" z Basis |
| Wszyscy | rozumienie polszczyzny | PLCC, CPTUB, PolAgentBench przed zmianą modelu lub kwantyzacji | [CPTUB](https://huggingface.co/spaces/speakleash/cptu_bench), [PLCC](https://huggingface.co/spaces/sdadas/plcc) |

Każde zadanie ma: wejście, oczekiwany wynik, wymagane cytaty i ukrytą specyfikację przebiegu (2.16). Mierzysz pass^1
i pass^8 (2.17), a w produkcji — jak Spellbook — **odsetek przyjętych sugestii**
([LawNext](https://www.lawnext.com/2025/08/spellbook-becomes-one-of-the-first-legal-ai-platforms-to-launch-gpt-5.html)).
Harvey ma własny BigLaw Bench — polskiego odpowiednika dla kancelarii nie znalazłem. Narzędzia:
[klocki: obserwowalność i ewaluacja](../harnessy-agentowe/02-KLOCKI.md#obserwowalność-i-ewaluacja),
[kurs 2, część 14](../kurs_aplikacje_agentowe/14-EWALUACJA.md).

### Dziennik zdarzeń

**Kto.** OpenHands zapisuje każdą interakcję jako typowane zdarzenie (akcja → obserwacja), co daje audyt i odtworzenie
([OpenHands](https://docs.openhands.dev/usage/architecture/runtime)); UI-TARS-desktop ma przeglądarkę strumienia
zdarzeń ([GitHub](https://github.com/bytedance/UI-TARS-desktop)); Google prowadzi dziennik pracy z pauzą i przejęciem;
Manus Browser Operator loguje każdą akcję ([Manus](https://manus.im/blog/manus-browser-operator)). W sprawie
*Amazon v. Perplexity* dzienniki agenta stały się materiałem dowodowym
([ComplexDiscovery](https://complexdiscovery.com/ninth-circuit-vacates-amazon-injunction-ai-agent-logs-emerge-as-ediscovery-issue/);
znam tylko tytuł).

**U siebie.**
- Dziennik tylko do dopisywania: kto, kiedy, jaki model i wersja, jakie narzędzie, jaki cytat, kto zatwierdził.
- Eksport **„notatki o narzędziach"** per sprawa — § 23e ZZEA każe na prośbę klienta wskazać użyte narzędzia i ich cel
  ([NRA](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/)).
- Dziennik to dane osobowe: szyfrowanie (art. 32 RODO), retencja, eksport i usunięcie per klient. UODO przypomina, że
  administrator powinien „regularnie mierzyć i testować wdrożone środki bezpieczeństwa"
  ([UODO, 26.06.2026](https://uodo.gov.pl/pl/138/4449)) — dziennik plus złoty zestaw to właśnie ten pomiar.
- Kurs: [kurs 2, część 15](../kurs_aplikacje_agentowe/15-OBSERWOWALNOSC.md).

To nie jest porada prawna — przepisy i obowiązki zawodowe omawiam szerzej w
[04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md).
