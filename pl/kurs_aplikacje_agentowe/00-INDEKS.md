# Kurs 2: aplikacje agentowe na modelach lokalnych — indeks

**Utworzony 23 września 2026.**
Kontynuacja kursu 1 — [`../kurs_lokalne_modele/00-KURS-INDEKS.md`](../kurs_lokalne_modele/00-KURS-INDEKS.md),
części 1–10.

> **Cel całości.** Po tym kursie **projektujesz i utrzymujesz systemy agentowe**, a nie
> tylko uruchamiasz agenta. Budujesz jeden rosnący system — `$OSA/` — i stawiasz
> na nim trzech współpracujących agentów osobistych, którzy **działają tygodniami,
> budzą się sami, pamiętają, są mierzeni i nie mogą zrobić Ci krzywdy.**
>
> Kurs 1 uczył, **jak działa model**. Kurs 2 uczy, **jak zbudować wokół niego system,
> któremu można zaufać.**

---

## Teza, na której stoi cały kurs

> **Wynik agenta zmienia się bardziej wraz z harnessem niż z modelem.** Ten sam model
> pod dwoma szkieletami daje istotnie różne liczby.

Zmienna, nad którą masz **pełną kontrolę** — system wokół modelu — jest ważniejsza niż
zmienna, nad którą nie masz **żadnej** — wagi. Dlatego w tym kursie nie ma części
o dostrajaniu modeli, a jest sześć części o pomiarze.

⭐ **W części 14 zweryfikujesz tę tezę na własnym sprzęcie.** Jeśli się nie potwierdzi,
kurs mówi Ci wprost: popraw kurs.

---

## Droga

```
  BLOK I · FUNDAMENT ─────────────────────────────── ~14 h
   01 architektury          mapa terenu, OpenClaw rozłożony, loop engineering
   02 szkielet              brama, konfiguracja, sesja jako dziennik zdarzeń
   03 harness         ⭐⭐  pętla, która przeżywa pięć okien kontekstu
              │
  BLOK II · KONTEKST I PAMIĘĆ ────────────────────── ~16 h
   04 kontekst              budżet uwagi, context rot ZMIERZONY, kompakcja
   05 pamięć           ⭐  trzy szkoły, graf bi-temporalny od zera
   06 tożsamość            SOUL/AGENTS/GRANICE — pliki zamiast dostrajania
              │
  BLOK III · DZIAŁANIE ───────────────────────────── ~20 h
   07 narzędzia            ergonomia, promień rażenia, ile to za dużo
   08 code-mode       ⭐⭐  agent pisze program — największa zmiana 2026
   09 protokoły            MCP vs CLI vs funkcja — mierzone, nie dyskutowane
   10 piaskownica          drabina izolacji, proxy, sekrety, próby ucieczki
              │
  BLOK IV · PROAKTYWNOŚĆ I WIELOŚĆ ───────────────── ~16 h
   11 harmonogram      ⭐  agent budzi się sam i NIE zawraca głowy
   12 kanały               kanał jako granica zaufania
   13 flota            ⭐  trzej agenci, granice uprawnień, kaskada
              │
  BLOK V · JAKOŚĆ I ZAUFANIE ─────────────────────── ~14 h
   14 ewaluacja       ⭐⭐  zbiór złoty, sędzia, pass^k, bramka regresji
   15 obserwowalność       ślady OTel, odtwarzanie, śledztwo po awarii
   16 bezpieczeństwo   ⭐  OWASP ASI01–ASI10, 20 ataków na własną flotę
              │
  BLOK VI · PRODUKCJA ────────────────────────────── ~12 h
   17 hybryda              lokalny domyślnie, granica prywatności w kodzie
   18 wydanie              wersjonowanie, wycofanie, runbook
              │
   19 CAPSTONE ─────────► osobisty asystent + powtórzony pomiar z części 1
```

⚠️ **Kolejność nie jest dekoracją.** Część 8 (code-mode) bez części 10 (piaskownica)
to zdalne wykonanie kodu z uprzejmym interfejsem. Część 13 (flota) bez części 10 i 7
to jeden cel ataku z sumą wszystkich uprawnień. **Nie przeskakuj w blokach III i IV.**

---

## Trzej agenci, których zbudujesz

Różnią się **granicami, nie inteligencją** — i to jest główna nauka architektoniczna
tego kursu.

| | **Archiwista** | **Badacz** | **Gospodarz** |
| :-- | :-- | :-- | :-- |
| Dziedzina | dokumenty lokalne | szukanie w sieci | kalendarz, dom, przypomnienia |
| Sieć | ✗ zero | ⭐ 4 domeny przez proxy | lokalna |
| Zaufanie do wejścia | wysokie | ⚠️ **zerowe** | średnie |
| Piaskownica | lekka | ⭐ ścisła | średnia |
| Proaktywny | ✗ | ✗ **celowo** | ⭐ tak |
| Pojawia się od | części 2 | części 10 | części 11 |

---

## Pliki

| # | Plik | Poziom | Czego się nauczysz | Czas |
| :-- | :-- | :-- | :-- | :-- |
| 01 | `01-ARCHITEKTURY-AGENTOWE.md` | ⭐⭐ | kiedy **nie** budować agenta, cztery topologie, **OpenClaw rozłożony**, loop engineering | ~5 h |
| 02 | `02-SZKIELET-SESJE-KONFIGURACJA.md` | ⭐⭐⭐ | brama na pętli zwrotnej, konfiguracja jako dane, **dziennik zdarzeń z odtwarzaniem i gałęziami** | ~5 h |
| 03 | `03-HARNESS-DLUGIE-ZADANIA.md` | ⭐⭐⭐⭐ | ⭐⭐ **najważniejsza część.** Rejestr zadań, plik postępu, git jako pamięć, pięć warunków stopu, drabina błędu | ~6 h |
| 04 | `04-INZYNIERIA-KONTEKSTU.md` | ⭐⭐⭐⭐ | budżet uwagi, **zmierzona krzywa degradacji Twoich modeli**, kompakcja w czterech ruchach | ~5 h |
| 05 | `05-PAMIEC-DLUGOTERMINOWA.md` | ⭐⭐⭐⭐ | trzy szkoły pamięci, ⭐ **graf bi-temporalny od zera**, wydobywanie faktów, kwarantanna | ~6 h |
| 06 | `06-TOZSAMOSC-PLIKI-ROBOCZE.md` | ⭐⭐⭐ | `SOUL/AGENTS/GRANICE/MEMORY/SKILL`, doładowywane umiejętności, test regresji osobowości | ~4 h |
| 07 | `07-NARZEDZIA-PROJEKT-I-ERGONOMIA.md` | ⭐⭐⭐⭐ | opisy, pobłażliwe wejście, **błąd jako prompt**, idempotencja, promień rażenia, ablacja liczby narzędzi | ~5 h |
| 08 | `08-CODE-MODE.md` | ⭐⭐⭐⭐⭐ | ⭐⭐ agent pisze program zamiast wołać narzędzia. **Dlaczego to pomaga zwłaszcza małym modelom** | ~6 h |
| 09 | `09-PROTOKOLY-MCP-CLI-A2A.md` | ⭐⭐⭐ | koszt stały vs koszt odkrycia, MCP 2026-07-28, **teza Steinbergera zmierzona** | ~4 h |
| 10 | `10-PIASKOWNICA-PRODUKCYJNA.md` | ⭐⭐⭐⭐ | pięć szczebli izolacji, **co każdy zatrzymuje**, proxy, sekrety, 16 prób ucieczki | ~5 h |
| 11 | `11-HARMONOGRAM-PROAKTYWNOSC.md` | ⭐⭐⭐⭐ | ⭐ `HEARTBEAT.md`, tłumienie ciszy, precyzja zaczepek, praca nocna, bezpiecznik | ~5 h |
| 12 | `12-KANALY-INTERFEJSY.md` | ⭐⭐⭐ | kanał jako granica zaufania, parowanie, routing, strumieniowanie | ~4 h |
| 13 | `13-FLOTA-WIELU-AGENTOW.md` | ⭐⭐⭐⭐⭐ | ⭐ nadzorca i wachlarz, **granica zaufania między agentami**, cztery bezpieczniki, kaskada | ~6 h |
| 14 | `14-EWALUACJA.md` | ⭐⭐⭐⭐ | ⭐⭐ zbiór złoty, trajektoria, `pass^k`, **sędzia w izolowanym kontekście**, bramka regresji | ~5 h |
| 15 | `15-OBSERWOWALNOSC.md` | ⭐⭐⭐⭐ | ślady OTel GenAI, sześć metryk, **odtwarzanie promptu z dowolnej tury**, śledztwo | ~4 h |
| 16 | `16-BEZPIECZENSTWO-OWASP-ASI.md` | ⭐⭐⭐⭐⭐ | ⭐ ASI01–ASI10 na Twoim systemie, polityka sekwencji, **20 ataków na własną flotę** | ~5 h |
| 17 | `17-HYBRYDA-I-ROUTER.md` | ⭐⭐⭐ | prywatność → zdolność → koszt, **granica w kodzie**, audyt wyjścia, test offline | ~4 h |
| 18 | `18-WYDANIE-I-UTRZYMANIE.md` | ⭐⭐⭐⭐ | siedem składników wydania, wycofanie <5 min, migracja pamięci, **runbook** | ~4 h |
| 19 | `19-CAPSTONE.md` | ⭐⭐⭐⭐⭐ | złożenie całości + ⭐ **powtórzony pomiar z części 1 — ocena kursu** | ~10 h |
| — | `ZRODLA.md` | — | pełna bibliografia z adnotacjami: **co z czego weszło i gdzie** | — |

**Razem: ~102 godziny przy klawiaturze.** To nie jest kurs do przeczytania.

---

## Anatomia każdej części

Stała, żeby dało się nawigować:

```
0. Problem — po co ta warstwa istnieje
1-N. Teoria — z odnośnikiem do źródła
   ⭐ „Jak robią to najlepsi" — OpenClaw, Anthropic, Steinberger
OD ZERA — piszesz mechanizm sam, bez zależności
PRODUKCYJNIE — tabela „Twoje vs gotowe": co dokładają, co kosztują
⭐ EKSPERYMENT — hipoteza, procedura, tabela DO WYPEŁNIENIA, predykcja
ĆWICZENIE — produkuje coś w rosnącym systemie
Pułapki — ponumerowane, z objawem i lekarstwem
Checkpoint — skrypt, który MUSI przejść przed następną częścią
```

⭐ **Sekcja EKSPERYMENT jest sednem tego kursu.** Każda ma **predykcję** — co
spodziewam się zobaczyć — i **pustą tabelę** na Twój wynik. Gdy się rozjadą,
**Twój pomiar wygrywa i popraw kurs.** Pliki są Twoje.

---

## Zasady, których trzymam się w całym kursie

1. **Mechanizm od zera, potem biblioteka.** Najpierw piszesz sam (~80 linii), potem
   pokazuję gotowe: co dokłada, co kosztuje, kiedy warto się przełączyć.
2. **Nic bez pomiaru.** Każdy próg w Twoim systemie pochodzi z eksperymentu, nie
   z tego kursu. Cudze liczby są punktem wyjścia, nie wnioskiem.
3. **Minimum trzy przebiegi.** Agenci są niedeterministyczni; jedno uruchomienie to
   anegdota (P61).
4. **Domyślnie najwęziej.** Brak reguły = najmniejsze uprawnienia. Wszędzie (P66).
5. **Bezpieczeństwo w kodzie, nie w prompcie.** Prompt jest ostatnią linią obrony,
   nigdy pierwszą.
6. **Każda decyzja dostaje ADR** z warunkiem falsyfikacji: *„jak poznam, że to była
   zła decyzja"*.
7. **Pułapki numerowane dalej po kursie 1.** Sprzętowe P1–P18 (pułapki maszyny referencyjnej),
   programowe kurs 1: P20–P52, **kurs 2: P60–P139**.

---

## Czego w tym kursie nie ma — i dlaczego

| Czego brak | Dlaczego |
| :-- | :-- |
| **Powtórek z kursu 1** | GBNF, RAG od zera, `bwrap`, dekodowanie spekulatywne, multimodalność — masz to. Kurs 2 odwołuje się i idzie wyżej |
| **Przeglądu frameworków** | LangGraph/CrewAI pojawiają się jako **punkt odniesienia w tabelach**, nie jako wycieczka. Katalog jest w kursie 1, część 9 |
| **Dostrajania modeli** | Inny kurs. Tu model jest dany, zmienną jest system — co potwierdza teza ze wstępu |
| **A2A** | Omówione w części 9, ale **niepotrzebne, dopóki wszyscy agenci są Twoi** |

---

## Zanim zaczniesz

```bash
cd ~/llm-education   # katalog repozytorium (u Ciebie może być inny)
source rig-env.sh
$LB/llama-cli --version                     # oczekuj: build z commita 987498f
rocm-smi --showid                           # 2× R9700 + iGPU jako GPU[2]
python3 --version                           # oczekuj ≥ 3.12
which bwrap systemd-run sqlite3 git         # wszystkie cztery wymagane
test -f $AGENT/agent.py && echo "✓ pętla z kursu 1 — punkt wyjścia"
```

⚠️ **`HIP_VISIBLE_DEVICES=0,1` musi być ustawione** (P12/P32 z kursu 1) — inaczej małe
modele lądują na iGPU z 2 GB.

⚠️ **Po dołożeniu kart 3 i 4 numeracja się zmieni (P13).** Przemapuj przez `amd-smi
list`, zaktualizuj `rig-env.sh` i **powtórz eksperymenty 4, 7, 8, 13 i 17** — wszystkie
progi pochodzą z pomiarów na dwóch kartach.

---

## Rejestr pułapek programowych — P60–P139

Osiemdziesiąt pułapek. Każda ma w swojej części objaw i lekarstwo.

| ID | Pułapka | Część |
| :-- | :-- | --: |
| P60 | Budowanie agenta tam, gdzie wystarczy workflow | 1 |
| P61 | Mierzenie jednym przebiegiem | 1 |
| P62 | Przyjęcie tez autorytetu bez sprawdzenia kontekstu | 1 |
| P63 | Wypisywanie na `stdout` w procesie bramy | 2 |
| P64 | Zapis bez `fsync` | 2 |
| P65 | Sortowanie zdarzeń po `ts` zamiast po `seq` | 2 |
| P66 | Domyślny poziom zaufania = szerszy | 2 |
| P67 | Agent zmienia lub kasuje test, żeby przeszedł | 3 |
| P68 | Pozycja rejestru za duża na jedną sesję | 3 |
| P69 | Pominięcie weryfikacji bazy na starcie | 3 |
| P70 | Brak postępu mylony z brakiem aktywności | 3 |
| P71 | Komunikat błędu nieczytelny dla modelu | 3 |
| P72 | Ufanie deklarowanej długości kontekstu | 4 |
| P73 | Zmienna wartość przed stałym prefiksem | 4 |
| P74 | Kompakcja od razu, bez ruchu 1 i 2 | 4 |
| P75 | Streszczenie zaokrągla liczby | 4 |
| P76 | Prompt systemowy rośnie i nigdy nie maleje | 4 |
| P77 | Nadpisywanie faktu zamiast unieważniania | 5 |
| P78 | Mylenie czasu świata z czasem systemu | 5 |
| P79 | Fakt bez cytatu i źródła | 5 |
| P80 | Brak zakresu — pamięć przecieka między agentami | 5 |
| P81 | Sesja niezaufana pisze do pamięci trwałej | 5 |
| P82 | Granice tylko w prompcie, bez egzekucji | 6 |
| P83 | Wszystkie umiejętności ładowane zawsze | 6 |
| P84 | Agent edytuje `AGENTS.md` albo `GRANICE.md` | 6 |
| P85 | `SKILL.md` z nieprzeczytanego źródła | 6 |
| P86 | Dwa narzędzia o nakładających się opisach | 7 |
| P87 | Surowy traceback jako wynik narzędzia | 7 |
| P88 | Narzędzia niefiltrowane po zaufaniu sesji | 7 |
| P89 | Brak idempotencji przy skutku ubocznym | 7 |
| P90 | Promień rażenia stały zamiast wyliczanego | 7 |
| P91 | Połknięty traceback | 8 |
| P92 | Ścieżki niesprawdzane wewnątrz API | 8 |
| P93 | Brak limitu wywołań w programie | 8 |
| P94 | Model drukuje surowe treści | 8 |
| P95 | Przyjęcie liczby „23 tys. tokenów" bez sprawdzenia własnej konfiguracji | 9 |
| P96 | Założenie, że model poradzi sobie z `--help` | 9 |
| P97 | Serwer MCP jako zaufany element systemu | 9 |
| P98 | Trzy interfejsy do jednej zdolności utrzymywane równolegle | 9 |
| P99 | Mylenie kontenera z piaskownicą | 10 |
| P100 | Brak limitów zasobów przy `bwrap` | 10 |
| P101 | Środowisko dziedziczone do piaskownicy | 10 |
| P102 | `HTTP_PROXY` jako kontrola sieci | 10 |
| P103 | Przekonanie, że piaskownica chroni przed wstrzyknięciem | 10 |
| P104 | Dwie instancje planisty | 11 |
| P105 | Brak idempotencji przy restarcie | 11 |
| P106 | Cisza rozpoznawana tylko po dokładnym ciągu | 11 |
| P107 | Brak ciszy nocnej i limitu dziennego | 11 |
| P108 | Brak bezpiecznika po serii błędów | 11 |
| P109 | Kanał jako samo wejście, bez zaufania | 12 |
| P110 | Odpowiadanie nieznanym nadawcom | 12 |
| P111 | Porównanie tokenu przez `==` | 12 |
| P112 | Dzielenie wiadomości w środku bloku kodu | 12 |
| P113 | Brak limitu głębokości delegacji | 13 |
| P114 | Wynik subagenta traktowany jak polecenie | 13 |
| P115 | Podział wzdłuż zadań zamiast uprawnień | 13 |
| P116 | Brak degradacji częściowej | 13 |
| P117 | Nadzorca z narzędziami dziedzinowymi | 13 |
| P118 | Agent ocenia sam siebie | 14 |
| P119 | Brak kategorii „poprawna odmowa" | 14 |
| P120 | Jeden przebieg na pytanie | 14 |
| P121 | Nieskalibrowany sędzia | 14 |
| P122 | Zbiór złoty wygenerowany testowanym modelem | 14 |
| P123 | Alerty zbudowane wprost na `gen_ai.*` | 15 |
| P124 | Ślady z pełną treścią na zawsze | 15 |
| P125 | Eksport telemetrii synchronicznie | 15 |
| P126 | Wiara, że ślady pokażą wszystko | 15 |
| P127 | Filtr wzorców jako główna obrona przed wstrzyknięciem | 16 |
| P128 | Fakt w pamięci bez cytatu i źródła | 16 |
| P129 | Streszczenie do zatwierdzenia generowane przez model | 16 |
| P130 | Suma kontrolna sprawdzana tylko przy instalacji | 16 |
| P131 | Brak linii bazowej zachowania | 16 |
| P132 | Bramka prywatności omijana w eskalacji | 17 |
| P133 | Granica oparta na wzorcach zamiast na źródle | 17 |
| P134 | Nieprzeczytany `stop_reason` | 17 |
| P135 | Ciche uzależnienie od chmury | 17 |
| P136 | Wydanie z niezacommitowanymi zmianami | 18 |
| P137 | Wycofanie kodu bez migracji pamięci wstecz | 18 |
| P138 | `cp` zamiast `sqlite3 .backup` | 18 |
| P139 | Model niewersjonowany sumą kontrolną | 18 |

---

## Gdzie co leży

| Ścieżka | Rola |
| :-- | :-- |
| `00-INDEKS.md` | ten plik — mapa i rejestr pułapek |
| `01`–`19` | części kursu, po kolei |
| [`ZRODLA.md`](ZRODLA.md) | **bibliografia z adnotacjami** — co z czego wzięte i gdzie użyte |
| [`szkielet/`](szkielet/) | startowy szkielet `$OSA/` do skopiowania |
| [`../kurs_lokalne_modele/00-KURS-INDEKS.md`](../kurs_lokalne_modele/00-KURS-INDEKS.md) | ⬅️ **kurs 1** — model od środka |
| `../../rig-env.sh` | ścieżki do modeli i binarek, widoczne karty |

**Co powstanie w trakcie:**

```
$OSA/
├── brama.py konfig.py sesje.py harness.py kontekst.py     cz. 2–4
├── decyzje/          ADR z warunkiem falsyfikacji         cz. 1
├── pomiary/          ⭐ wyniki eksperymentów — plik na część
├── dziennik/         sesje + ślady OTel                   cz. 2, 15
├── agenci/           archiwista/ badacz/ gospodarz/       cz. 6
├── narzedzia/        rejestr, promień, idempotencja       cz. 7
├── kod/              code-mode: API + wykonanie           cz. 8
├── piaskownica/      poziomy, proxy, sekrety              cz. 10
├── harmonogram/      planista                             cz. 11
├── kanaly/           gniazdo, HTTP, routing               cz. 12
├── flota/            delegacja, zaufanie, bezpieczniki    cz. 13
├── ewaluacja/        zbiór złoty, sędzia, bramka          cz. 14
├── obserwacja/       tracer, metryki, odtwarzanie         cz. 15
├── bezpieczenstwo/   izolacja, sekwencje, dryf, zgody     cz. 16
├── router/           granica prywatności, audyt wyjścia   cz. 17
├── wydanie/          manifest, wydaj, wycofaj, kontrola   cz. 18
├── testy/            zbiór złoty, ucieczki, 20 ataków
├── RUNBOOK.md        ⭐ co robić o 3:00
└── STOP.sh           ⭐ wyłącznik awaryjny
```

---

## Trzy liczby, które będziesz znał po tym kursie

Nikt inny ich nie zna, bo pochodzą z Twojej maszyny:

1. **Gdzie załamuje się synteza Twoich modeli** — realny limit kontekstu, nie
   deklarowany (część 4).
2. **Ile narzędzi wytrzymują** — zanim wybór zacznie się psuć (część 7).
3. **O ile harness bije model** — i czy warto kupować większy (część 14).

⭐ **Trzecia jest najważniejsza.** Jeśli ją znasz, przestajesz zgadywać i zaczynasz
inżynierię.

---

**Start: `01-ARCHITEKTURY-AGENTOWE.md`.**
Pierwszy eksperyment znajdzie pięć miejsc, w których pęka Twoja obecna pętla.
**To jest program reszty kursu.**
