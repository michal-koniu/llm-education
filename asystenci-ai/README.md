# Asystenci AI — 15 najlepszych i czego się od nich nauczyć

**Stan na 11 października 2026.** Przegląd najlepszych istniejących asystentów AI — otwartych i zamkniętych — wybranych
po trakcji rynkowej i sile pomysłu. Cel: nauczyć się technicznych i rynkowych lekcji, zanim zbuduję własnego
asystenta — dla siebie i dla polskich profesjonalistów, którzy nie mogą wysyłać danych klientów do USA (lokalna maszyna
na biurku trzyma wszystkie dane).

> ⚠️ **Ten przegląd starzeje się w tygodniach.** Liczby (użytkownicy, przychody, wyceny) mają datę i źródło; dane
> podawane przez same firmy oznaczam *(dane firmy)*. Gwiazdki z API GitHuba z 11.10.2026. **Niczego tu nie testowałem
> na swojej maszynie** — to przegląd dokumentacji, ogłoszeń i analiz. Części prawne to materiał edukacyjny, **nie porada
> prawna**.

---

## Spis treści

- [Mapa rynku: cztery rodzaje asystentów](#mapa-rynku-cztery-rodzaje-asystentów)
- [Piętnastka](#piętnastka)
- [10 najważniejszych lekcji](#10-najważniejszych-lekcji)
- [Co to znaczy dla lokalnego asystenta dla polskich profesjonalistów](#co-to-znaczy-dla-lokalnego-asystenta-dla-polskich-profesjonalistów)
- [Jak wybierałem](#jak-wybierałem)
- [Pliki w tym katalogu](#pliki-w-tym-katalogu)
- [Powiązane części repozytorium](#powiązane-części-repozytorium)

---

## Mapa rynku: cztery rodzaje asystentów

| Rodzaj | Co robi | Liderzy w piętnastce | Gdzie są pieniądze |
|---|---|---|---|
| **Codzienni** | czat, wyszukiwanie, pamięć, głos, coraz częściej zadania w tle | ChatGPT, Gemini, Claude, Perplexity | subskrypcje konsumenckie i firmowe, dystrybucja przez system i przeglądarkę |
| **Profesjonalni** | jedna dziedzina, głęboko: prawo, medycyna, kod, spotkania, obsługa klienta | Harvey, Abridge, Cursor, Granola, OpenEvidence, Sierra, Noxtua | stanowiska, użycie, płatność za wynik, reklamy (OpenEvidence) |
| **Wykonawcy autonomiczni** | sami klikają, przeglądają, piszą pliki, kończą zadanie | Manus, browser-use (oraz tryby agentowe Claude, ChatGPT, Gemini, Perplexity) | kredyty za zadanie, API, chmura dla open source |
| **Żyjący autonomicznie** | działają stale, w tle, z rzadkimi poleceniami człowieka, przez komunikatory | OpenClaw, Hermes Agent | open source + fundacja, ekosystem, hostowane wersje i firmy budujące na nich |

Szczegóły rynku, liczby, przejęcia i porażki: [02-RYNEK.md](02-RYNEK.md).

---

## Piętnastka

Wynik 0–100 według wag z sekcji [Jak wybierałem](#jak-wybierałem). Pełne profile (9 obszarów każdy):
[01-PROFILE.md](01-PROFILE.md).

<!-- main-table -->
| # | Asystent | Kod | Rodzaj | Cel | Przewaga | Na czym zarabia | Offline | Wynik |
|---|---|---|---|---|---|---|---|---|
| 1 | [OpenClaw](01-PROFILE.md#1-openclaw) | otwarty, MIT, ⭐ <!-- gh:openclaw/openclaw -->391,7k | żyjący | osobisty agent działający stale, sterowany z komunikatorów | ekosystem, kanały, umiejętności, fundacja; baza dla Microsoft Autopilot | nie zarabia sam — fundacja non-profit; zarabiają firmy budujące na nim | **Częściowo** — rdzeń z lokalnym modelem tak, kanały komunikatorów wymagają sieci | 100 |
| 2 | [Claude](01-PROFILE.md#2-claude) | zamknięty | codzienny · profesjonalny · wykonawca | asystent do pracy: czat, Cowork, Claude Code, computer use | jakość modelu w zadaniach agentowych i kodzie; MCP i umiejętności | subskrypcje i API; Claude Code ponad 2,5 mld USD przychodu w skali roku (II 2026, *dane firmy*); szacunek prasy dla całej firmy: ok. 44 mld USD run-rate (V 2026) | Nie | 97 |
| 3 | [Abridge](01-PROFILE.md#3-abridge) | zamknięty | profesjonalny (medycyna) | notatka lekarska z rozmowy z pacjentem | „Linked Evidence" — każde zdanie notatki ma odnośnik do nagrania | licencje dla szpitali | Nie | 94 |
| 4 | [Harvey](01-PROFILE.md#4-harvey) | zamknięty | profesjonalny (prawo) | asystent kancelarii: analiza, przegląd dokumentów, przepływy | zaufanie dużych kancelarii, własny model Tenet | stanowiska w kancelariach; wycena 15,5 mld USD (IX 2026) | Nie | 94 |
| 5 | [Hermes Agent](01-PROFILE.md#5-hermes-agent) | otwarty, MIT, ⭐ <!-- gh:NousResearch/hermes-agent -->252,7k | żyjący | osobisty agent z pamięcią, cronem, głosem, kanałami | uczy się umiejętności z doświadczenia, dobry z lokalnymi modelami | open source; Nous Research zarabia na modelach i chmurze | **Częściowo** (głos TTS domyślnie w chmurze) | 93 |
| 6 | [Manus](01-PROFILE.md#6-manus) | zamknięty | wykonawca | ogólny agent wykonujący długie zadania w chmurowej maszynie | inżynieria kontekstu, maszyna wirtualna na zadanie | kredyty i subskrypcje | Nie | 93 |
| 7 | [ChatGPT](01-PROFILE.md#7-chatgpt) | zamknięty | codzienny · wykonawca | asystent ogólny dla wszystkich | zasięg i nawyk użytkowników | subskrypcje, firmy, API | Nie | 87 |
| 8 | [Gemini](01-PROFILE.md#8-gemini) | zamknięty | codzienny · wykonawca | asystent Google w Androidzie, Chrome i Workspace | dystrybucja przez system i dane Google; opublikowana architektura bezpieczeństwa agenta | subskrypcje Google, Workspace | Nie | 87 |
| 9 | [Cursor](01-PROFILE.md#9-cursor) | zamknięty | profesjonalny (programiści) | edytor kodu z agentami | najlepiej dopasowany przepływ pracy programisty, własny model Composer | subskrypcje i użycie; przejęty przez SpaceX (VIII 2026) | Nie | 87 |
| 10 | [Granola](01-PROFILE.md#10-granola) | zamknięty | profesjonalny (spotkania) | notatki ze spotkań bez bota na rozmowie | nagrywa lokalnie dźwięk z komputera, notatka = szkic użytkownika + transkrypcja | subskrypcje | Nie | 87 |
| 11 | [Sierra](01-PROFILE.md#11-sierra) | zamknięty | profesjonalny (obsługa klienta) | agent obsługi klienta dla firm | płatność za wynik, ewaluacja pass^k i symulacje | opłata za rozwiązaną sprawę | Nie | 85 |
| 12 | [OpenEvidence](01-PROFILE.md#12-openevidence) | zamknięty | profesjonalny (medycyna) | odpowiedzi medyczne z cytatami z literatury | licencje na źródła, cytaty, darmowy dla lekarzy | reklamy farmaceutyczne | Nie | 84 |
| 13 | [browser-use](01-PROFILE.md#13-browser-use) | otwarty, MIT, ⭐ <!-- gh:browser-use/browser-use -->117,6k | wykonawca | biblioteka do agentów obsługujących przeglądarkę | podejście przez DOM zamiast zrzutów ekranu — szybciej i taniej | open source + chmura i własny model | **Częściowo** — z lokalną przeglądarką i modelem tak, internet potrzebny do stron | 83 |
| 14 | [Noxtua](01-PROFILE.md#14-noxtua) | zamknięty | profesjonalny (prawo, UE) | asystent prawny na europejskiej, suwerennej chmurze | dane na chmurze UE/CH; poziom Athena na modelach open source, Minerva na modelach frontier w europejskim układzie; w Polsce jako Beck-Noxtua | licencje (Beck-Noxtua: 590 zł netto/mies.) | Nie (chmura UE) | 78 |
| 15 | [Perplexity](01-PROFILE.md#15-perplexity) | zamknięty | codzienny · wykonawca | wyszukiwanie z odpowiedzią i cytatami, przeglądarka Comet | cytaty, szybkość, agent lokalny Portable Computer | subskrypcje, firmy, API | **Częściowo** (Portable Computer) | 77 |
<!-- /main-table -->

Kto nie zmieścił się w piętnastce, a warto go znać: [01-PROFILE.md](01-PROFILE.md).

---

## 10 najważniejszych lekcji

1. **Zaufanie wygrywa z funkcjami.** Najlepsi profesjonalni asystenci (Abridge, OpenEvidence, Harvey) każdą odpowiedź
   wiążą ze źródłem. Dla prawnika i lekarza „pokaż, skąd to wiesz" jest ważniejsze niż elokwencja.
2. **Przepływ pracy, nie czat.** Granola, Cursor, Abridge wygrywają, bo siedzą tam, gdzie człowiek już pracuje — w
   edytorze, w gabinecie, na spotkaniu — a nie w osobnym oknie czatu.
3. **Kontekst to inżynieria.** Manus i OpenClaw pokazują, że jakość agenta zależy od tego, co i w jakiej kolejności
   trafia do kontekstu (stały prefiks, plik planu, pamięć w plikach) — ważne zwłaszcza przy lokalnym modelu.
4. **Kanał jest produktem.** Asystenci „żyjący" działają przez komunikatory (Telegram, WhatsApp, iMessage) i w tle; dla
   zwykłego użytkownika to bardziej naturalne niż aplikacja.
5. **Autonomia wymaga hamulców.** Zatwierdzenia skalowane do skutków zewnętrznych, piaskownica na zadanie, sekrety poza
   promptem. 722 porady bezpieczeństwa OpenClaw w 2026 to koszt szybkiego wzrostu bez tego.
6. **Własny model na otwartych wagach to fosa.** Harvey (Tenet) i Cursor (Composer) dotrenowują otwarte modele
   na swoich danych — taniej i lepiej w swojej dziedzinie niż ogólny model z czołówki.
7. **Ewaluacja w praktyce, nie w benchmarku.** Sierra mierzy pass^k — czy agent zrobi to samo dobrze k razy z rzędu.
   Dla asystenta, któremu ktoś powierza klientów, liczy się powtarzalność.
8. **Model biznesowy idzie za wartością.** Od stanowisk do użycia i do płatności za wynik; ale nagłe zmiany cennika
   (Cursor) i koszt modeli z czołówki (Canva) potrafią zaboleć.
9. **Europa jest niedoobsłużona.** Część nowych funkcji agentowych gigantów omija EOG, a tajemnica zawodowa (art. 6 Prawa o adwokaturze, art. 3 ustawy o radcach prawnych) i § 23e Kodeksu Etyki Adwokackiej wymagają „należytej ochrony" informacji poufnych, a chmura z USA niesie dodatkowo ryzyko z CLOUD Act — to luka dla lokalnego produktu ([04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md)).
10. **Lokalnie da się sensownie.** Otwarte harnessy (OpenClaw, Hermes, browser-use) z lokalnym modelem działają bez
    internetu w zakresie pracy na dokumentach i plikach; słabe miejsca to świeża wiedza z sieci, polski głos i wizja.

---

## Co to znaczy dla lokalnego asystenta dla polskich profesjonalistów

- **Zacznij od jednego zawodu i jednego przepływu** — np. kancelaria: przegląd umów i pism z cytatami do źródła;
  gabinet: notatka z wizyty. Wzorce: [Harvey](01-PROFILE.md#4-harvey), [Abridge](01-PROFILE.md#3-abridge),
  [Noxtua](01-PROFILE.md#14-noxtua).
- **Wszystko na biurku**: model, wyszukiwanie w dokumentach, transkrypcja, pamięć, logi. Chmurę traktuj jako wyjątek
  na danych niezwiązanych z klientem. Architektura i macierz offline: [03-WZORCE-TECHNICZNE.md](03-WZORCE-TECHNICZNE.md).
- **Cytaty i weryfikacja jako funkcja główna** — Kodeks Etyki Adwokackiej § 23e (przyjęty przez NRA 12–13.06.2026; data wejścia w życie nieustalona) wymaga osobistej weryfikacji wyników AI. Szczegóły prawne i ceny konkurencji: [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md).
- **Kotwice cenowe w Polsce**: Beck-Noxtua 590 zł netto/mies. za użytkownika, Noa Notes 199 zł/mies. + VAT — lokalny
  asystent z jednorazowym sprzętem musi się z tym porównać.
- **Mój rig** (4 sloty DeepSeek-V4-Flash, tylko tekst) nadaje się na prototyp; dla klienta liczy się mniejsza, cicha
  maszyna na biurko ([sprzęt i ceny](04-POLSKA-I-SUWERENNOSC.md)).

---

## Jak wybierałem

Przejrzałem około 60 kandydatów w pięciu obszarach badań (codzienni, wykonawcy, żyjący, profesjonalni w prawie i
finansach, profesjonalni w medycynie, kodzie i innych zawodach) plus rynek polski i europejski. Każdy dostał oceny 1–5:

| Kryterium | Waga | Co mierzy |
|---|---|---|
| T — trakcja | 35% | użytkownicy, przychody, adopcja, finansowanie |
| I — pomysł | 25% | jak bardzo różni się od konkurencji i czy pomysł się obronił |
| L — wartość do nauki | 25% | ile mogę przenieść do lokalnego asystenta dla polskich profesjonalistów |
| A — przejrzystość architektury | 15% | ile wiadomo, jak to jest zbudowane (kod, dokumentacja, publikacje) |

Wynik = 20 × (0,35·T + 0,25·I + 0,25·L + 0,15·A). Ograniczenia: każdy z czterech rodzajów co najmniej dwa razy, obecne
i otwarte, i zamknięte, co najmniej jeden przykład europejski stawiający na prywatność (Noxtua). Remisy rozstrzyga trakcja, potem kolejność redakcyjna (ChatGPT, Gemini i Cursor mają po 87 pkt i T=5). Następni w kolejce: UI-TARS 76, Legora 74, Heidi 74, M365 Copilot 74, Genspark 72, Poke 72.

---

## Pliki w tym katalogu

| Plik | Zawartość |
|---|---|
| [README.md](README.md) | mapa rynku, piętnastka, lekcje, metoda |
| [01-PROFILE.md](01-PROFILE.md) | 15 profili po 9 obszarów + „warto znać" |
| [02-RYNEK.md](02-RYNEK.md) | modele biznesowe, liczby, przejęcia, porażki, trendy |
| [03-WZORCE-TECHNICZNE.md](03-WZORCE-TECHNICZNE.md) | wzorce techniczne, macierz offline, architektura lokalnego asystenta |
| [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md) | prawo, tajemnice zawodowe, konkurencja w PL i UE, modele, sprzęt, szanse |
| [ZRODLA.md](ZRODLA.md) | źródła |

## Powiązane części repozytorium

- [Harnessy agentowe dla lokalnych modeli](../harnessy-agentowe/README.md) — techniczny przegląd harnessów, w tym
  [Hermes Agent](../harnessy-agentowe/01-PROFILE.md#4-hermes-agent).
- [Kurs: aplikacje agentowe](../kurs_aplikacje_agentowe/01-ARCHITEKTURY-AGENTOWE.md) — architektury, pamięć,
  [proaktywność](../kurs_aplikacje_agentowe/11-HARMONOGRAM-PROAKTYWNOSC.md),
  [kanały](../kurs_aplikacje_agentowe/12-KANALY-INTERFEJSY.md),
  [bezpieczeństwo](../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md).
- [Kurs: lokalne modele](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md) — hybryda lokalny model + Claude.
