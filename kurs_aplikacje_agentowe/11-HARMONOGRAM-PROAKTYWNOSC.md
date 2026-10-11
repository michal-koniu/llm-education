# Część 11 · Harmonogram — agent, który budzi się sam

**Poziom:** ⭐⭐⭐⭐ · **Czas:** ~5 h · **Wymaga:** części 2 (brama), 3 (harness), 10 (piaskownica)
**Produkuje:** planistę, `HEARTBEAT.md`, tłumienie ciszy, pomiar trafności zaczepek

---

## 0. Próg, za którym agent staje się czymś innym

Do tej pory Twój agent **odpowiadał**. Ty pytasz, on działa. To jest narzędzie.

Agent, który budzi się sam, jest czymś innym — i różnica nie jest techniczna, tylko
**relacyjna**. Narzędzie, które odzywa się samo, musi zasłużyć na każde odezwanie się.
Dwa niepotrzebne powiadomienia dziennie i wyłączysz je w tydzień.

```
      Agent reaktywny              Agent proaktywny
   ─────────────────────        ─────────────────────
   Ty inicjujesz                 On inicjuje
   Koszt błędu: Twój czas        Koszt błędu: Twoje ZAUFANIE
   Test: czy odpowiedział        Test: czy WARTO było
   Skala: ile pytań zadasz       Skala: ⭐ nieograniczona
```

⭐ **Prawa kolumna jest powodem, dla którego to budujesz** — proaktywność zdejmuje
limit „ile zdążysz zapytać". I jednocześnie powodem, dla którego **większość
projektów agentowych wykłada się właśnie tutaj**.

> ⚠️ **Przypadek MoltMatch.** Udokumentowany incydent, w którym agent OpenClaw zakładał
> profile randkowe **bez wyraźnej zgody użytkownika**. Nie było to włamanie — agent
> działał proaktywnie w ramach uprawnień, które dostał, i **poza intencją**, którą mu
> przypisano. **Proaktywność bez granic to nie zaawansowanie, tylko nieprzewidywalność.**

---

## 1. `HEARTBEAT.md` — cron wyrażony po polsku

Wzorzec z OpenClaw i jest bardzo dobry: zamiast konfiguracji zadań w YAML-u, **lista
spraw do pilnowania napisana zdaniami**.

```markdown
# HEARTBEAT — Gospodarz
# Czytane przy każdym przebudzeniu. Edytuje człowiek; agent tylko czyta.

## Co rano (7:00)
- Sprawdź kalendarz na dziś. Odezwij się TYLKO jeśli:
  jest coś przed 10:00, ALBO dwa wydarzenia nachodzą na siebie,
  ALBO jest coś, do czego trzeba zabrać rzecz (bilet, dokument, prezent).
- Nie streszczaj spokojnego dnia. Spokojny dzień to brak wiadomości.

## Co godzinę (8:00–20:00)
- Sprawdź, czy nie ma przypomnienia na najbliższe 90 minut.
  Jedno przypomnienie = jedna wiadomość. Nie powtarzaj.

## Co wieczór (21:00)
- Jeśli jutro jest coś przed 9:00 — przypomnij o tym dziś.
- Jeśli jutro wywóz odpadów — przypomnij, który rodzaj.

## Co niedzielę (18:00)
- Tydzień do przodu: co wymaga przygotowania wcześniej niż dzień przed.

## Zasada nadrzędna
Gdy nie masz nic **wartego przerwania człowiekowi** — odpowiedz dokładnie
HEARTBEAT_OK i nic więcej. To jest poprawna i najczęstsza odpowiedź.
```

### 1.1 · `HEARTBEAT_OK` — mechanizm, który to ratuje

⭐ **To jest najlepszy pojedynczy pomysł w całej architekturze proaktywnej.**

```
przebudzenie → agent ocenia → odpowiedź "HEARTBEAT_OK" → BRAMA TŁUMI, nic nie dociera
                            └→ cokolwiek innego        → dostarczane człowiekowi
```

Dlaczego to działa lepiej niż warunek w kodzie:

1. **Domyślną odpowiedzią jest cisza**, a nie wiadomość. Odwrotność zwykłego cron-a.
2. **Ocena „czy warto" należy do modelu**, który widzi kontekst — a nie do reguły,
   która go nie widzi.
3. **Brama liczy tłumienia**, więc masz metrykę: *„dziś 24 przebudzenia, 2 wiadomości"*.
4. Agent nie musi „nie robić nic" — ma **zdefiniowaną akcję na wypadek spokoju**,
   a to jest dla modelu znacznie łatwiejsze (ta sama zasada co przy komunikatach
   błędu w części 3 i granicach w części 6).

```python
def przetworz_przebudzenie(odpowiedz: str, dziennik) -> bool:
    """Zwraca True, jeśli coś dotarło do człowieka."""
    czysta = odpowiedz.strip()
    if czysta == "HEARTBEAT_OK" or czysta.startswith("HEARTBEAT_OK"):
        dziennik.dopisz("heartbeat.cisza")
        return False
    if len(czysta) < 15:                          # ⚠️ P106
        dziennik.dopisz("heartbeat.podejrzane", tresc=czysta)
        return False
    dziennik.dopisz("heartbeat.wiadomosc", tresc=czysta)
    return True
```

⚠️ **Warunek `len < 15` jest istotny.** Model czasem odpowie „OK", „Nic nowego", „Brak".
To są **intencjonalne ciszy wyrażone inaczej** i bez tego warunku wyślesz człowiekowi
wiadomość o treści „OK" — czyli najgorszy możliwy rodzaj powiadomienia.

---

## 2. Planista

```python
# $OSA/harmonogram/planista.py
"""Wyzwalacze czasowe i zdarzeniowe. Jedna instancja — patrz P104."""
import re, datetime, pathlib, json, hashlib

WZORCE = [
    (r"co rano \((\d{1,2}):(\d{2})\)",        "dziennie"),
    (r"co wiecz[oó]r \((\d{1,2}):(\d{2})\)",  "dziennie"),
    (r"co godzin[ęe] \((\d{1,2}):\d{2}[–-](\d{1,2}):\d{2}\)", "godzinowo"),
    (r"co (\w+)\w* \((\d{1,2}):(\d{2})\)",    "tygodniowo"),
]
DNI = {"poniedziałek":0,"wtorek":1,"środ":2,"czwartek":3,"piątek":4,"sobot":5,"niedziel":6}

def parsuj(sciezka) -> list[dict]:
    """Nagłówki ## w HEARTBEAT.md → wyzwalacze. Treść sekcji → zadanie."""
    tekst = pathlib.Path(sciezka).read_text(encoding="utf-8")
    zadania = []
    for blok in re.split(r"\n## ", tekst)[1:]:
        naglowek, _, tresc = blok.partition("\n")
        for wzor, typ in WZORCE:
            if (m := re.search(wzor, naglowek.lower())):
                zadania.append({"naglowek": naglowek.strip(), "typ": typ,
                                "dopasowanie": m.groups(), "tresc": tresc.strip()})
                break
    return zadania

def nalezy_uruchomic(z: dict, teraz: datetime.datetime, ostatnie: dict) -> bool:
    klucz = z["naglowek"]
    poprz = ostatnie.get(klucz)
    poprz = datetime.datetime.fromisoformat(poprz) if poprz else None

    if z["typ"] == "dziennie":
        g, mi = int(z["dopasowanie"][0]), int(z["dopasowanie"][1])
        cel = teraz.replace(hour=g, minute=mi, second=0, microsecond=0)
        return teraz >= cel and (poprz is None or poprz < cel)
    if z["typ"] == "godzinowo":
        od, do = int(z["dopasowanie"][0]), int(z["dopasowanie"][1])
        if not (od <= teraz.hour <= do):
            return False
        return poprz is None or (teraz - poprz).total_seconds() >= 3600
    if z["typ"] == "tygodniowo":
        dzien = next((v for k, v in DNI.items() if k in z["dopasowanie"][0]), None)
        if dzien is None or teraz.weekday() != dzien:
            return False
        g, mi = int(z["dopasowanie"][1]), int(z["dopasowanie"][2])
        cel = teraz.replace(hour=g, minute=mi, second=0, microsecond=0)
        return teraz >= cel and (poprz is None or poprz < cel)
    return False
```

### 2.1 · Pętla planisty — z zabezpieczeniami

```python
def petla(brama, katalog_agentow, interwal_s=300):
    """Budzi się co 5 min, sprawdza, co dojrzało. Uruchamiana przez systemd."""
    while True:
        teraz = datetime.datetime.now()
        for kat in pathlib.Path(katalog_agentow).iterdir():
            hb = kat / "HEARTBEAT.md"
            if not hb.exists():
                continue
            ostatnie = _wczytaj_ostatnie(kat)
            for z in parsuj(hb):
                if not nalezy_uruchomic(z, teraz, ostatnie):
                    continue
                if _w_ciszy_nocnej(teraz, kat):            # P107
                    continue
                klucz = _klucz_wykonania(kat.name, z, teraz)
                if _juz_wykonane(klucz):                    # ⭐ P105 — idempotencja
                    continue
                _uruchom(brama, kat.name, z, klucz)
                _zapisz_ostatnie(kat, z["naglowek"], teraz)
        _spij(interwal_s)

def _klucz_wykonania(agent, z, teraz) -> str:
    """Zadanie dzienne wykonane raz na dobę — niezależnie od restartów planisty."""
    okno = {"dziennie": "%Y-%m-%d", "godzinowo": "%Y-%m-%d-%H",
            "tygodniowo": "%Y-W%W"}[z["typ"]]
    return hashlib.sha256(
        f"{agent}|{z['naglowek']}|{teraz.strftime(okno)}".encode()).hexdigest()[:16]
```

⭐ **`_klucz_wykonania` jest tym, co odróżnia planistę od `cron`-a.** Restart bramy
o 7:05 **nie może** ponownie uruchomić zadania porannego. Klucz oparty na oknie
czasowym (dzień/godzina/tydzień) gwarantuje wykonanie **dokładnie raz na okno**,
niezależnie od tego, ile razy planista wstanie.

---

## 3. Przebudzenie na zdarzenie

Czas to nie jedyny wyzwalacz i zwykle nie najlepszy.

| Wyzwalacz | Przykład | Opóźnienie | Koszt |
| :-- | :-- | :-- | :-- |
| **Czas** | „co rano 7:00" | do interwału | niski |
| **Plik** (`inotify`) | nowy skan w `~/skany/` | ⭐ natychmiast | ⭐ zero, gdy cicho |
| **Webhook** | zewnętrzny system woła bramę | natychmiast | zero |
| **Próg** | temperatura karty > 90 °C | do sondowania | niski |
| **Inny agent** | Archiwista znalazł brak (część 13) | natychmiast | zero |

```python
# obserwator plików — zero kosztu, gdy nic się nie dzieje
def obserwuj(katalog, na_zdarzenie, debounce_s=2.0):
    """Nowy plik → przebudzenie. Debounce, bo kopiowanie generuje wiele zdarzeń."""
    import time
    widziane, ostatnia = {}, 0
    while True:
        time.sleep(1)
        biezace = {p: p.stat().st_mtime for p in pathlib.Path(katalog).glob("*")}
        nowe = [p for p in biezace if p not in widziane]
        if nowe and time.time() - ostatnia > debounce_s:
            na_zdarzenie(nowe); ostatnia = time.time()
        widziane = biezace
```

⭐ **Przebudzenie na zdarzenie jest lepsze od czasowego wszędzie, gdzie się da.**
Sondowanie co 5 minut „czy jest nowy plik" to 288 przebudzeń dziennie, z których 287
nic nie robi. `inotify` to zero przebudzeń i **natychmiastowa reakcja**. Używaj czasu
tylko wtedy, gdy zdarzenia nie ma — czyli dla przeglądów okresowych.

---

## 4. Problem zaczepek — sygnał kontra hałas

To jest **prawdziwa trudność** tej części. Nie techniczna.

```
Agent odzywa się 8× dziennie, z czego 6 razy bez potrzeby
   → po tygodniu ignorujesz wszystkie, w tym te 2 ważne
   → agent stał się GORSZY niż brak agenta,
     bo dał Ci fałszywe poczucie, że coś jest pilnowane
```

### 4.1 · Mierz jak klasyfikator

| | Odezwał się | Zamilczał |
| :-- | :-- | :-- |
| **Warto było** | ⭐ trafienie (TP) | ⚠️ **przeoczenie (FN)** |
| **Nie warto** | ⚠️⚠️ **hałas (FP)** | ⭐ słusznie cicho (TN) |

⭐ **Hałas kosztuje więcej niż przeoczenie**, i to jest kontrintuicyjne. Przeoczenie
kosztuje jedno zdarzenie. Hałas kosztuje **zaufanie do wszystkich przyszłych
wiadomości** — po pięciu niepotrzebnych przestajesz czytać także te potrzebne.

**Wniosek projektowy: ustawiaj próg wysoko i obniżaj go dopiero na podstawie
przeoczeń, które faktycznie zabolały.** Nie odwrotnie.

### 4.2 · Trzy dźwignie progu

```python
PROGI = {
    "pilnosc_minimalna": 3,     # 1–5; poniżej — cisza
    "max_dziennie": 4,          # twardy limit; nadmiar czeka na przegląd
    "cisza_nocna": (22, 7),     # nic poza ALARMEM
    "min_odstep_min": 45,       # nie dwie wiadomości pod rząd
}

PROMPT_OCENY = """Oceń, czy to jest warte przerwania człowiekowi.

Skala pilności:
5 — strata, jeśli nie dowie się w ciągu godziny (odlot za 3 h, awaria)
4 — dziś powinien wiedzieć (termin jutro, konflikt w kalendarzu)
3 — warto, żeby wiedział w tym tygodniu
2 — ciekawostka, może poczekać na przegląd tygodniowy
1 — nie warto w ogóle

Dzisiaj odezwałeś się już {ile} razy (limit {limit}).
Ostatnia wiadomość: {ile_temu} minut temu.

Gdy pilność < {prog} — odpowiedz dokładnie HEARTBEAT_OK.

Sytuacja: {sytuacja}"""
```

⚠️ **Linia „Dzisiaj odezwałeś się już N razy" realnie zmienia zachowanie modelu.**
Model widzący, że wyczerpał 3 z 4 zaczepek, sam podnosi sobie poprzeczkę. To jest ten
sam mechanizm co informowanie o budżecie kontekstu w części 4 i kosztuje tyle samo:
kilkanaście tokenów.

### 4.3 · Kolejkowanie zamiast rezygnacji

Wiadomość o pilności 2 nie jest bezwartościowa — jest **niepilna**.

```python
def dostarcz_lub_odloz(wiadomosc, pilnosc, stan):
    if pilnosc >= 5:
        return "natychmiast"
    if _cisza_nocna() or stan["dzis"] >= PROGI["max_dziennie"]:
        _do_kolejki(wiadomosc, pilnosc); return "odlozone"
    if pilnosc >= PROGI["pilnosc_minimalna"]:
        return "natychmiast"
    _do_kolejki(wiadomosc, pilnosc); return "przeglad_tygodniowy"
```

⭐ **Przegląd tygodniowy zbierający wszystko, co nie dotarło, jest tanim sposobem na
zjedzenie ciastka i posiadanie ciastka.** Nic nie ginie, a przerwań jest mało.

---

## 5. Praca nocna — przewaga, której nie ma nikt w chmurze

Twoja maszyna stoi bezczynnie ~16 h na dobę. Dla kogoś płacącego za token praca nocna
jest kosztem. **Dla Ciebie jest darmowa.**

```markdown
## Co noc (3:00) — nie odzywaj się nigdy, tylko pracuj

- Porządkuj pamięć: scal duplikaty faktów, oznacz sprzeczności (część 5)
- Przelicz indeksy wyszukiwania po nowych dokumentach
- Uruchom zbiór złoty i zapisz wynik do $OSA/pomiary/nocne/ (część 14)
- Sprawdź regresje względem wczoraj; jeśli wynik spadł >5 pp — to jest pilność 4
- Skompaktuj dzienniki sesji starszych niż 30 dni

Wynik: raport do pliku. HEARTBEAT_OK zawsze, chyba że wykryto regresję.
```

⭐ **„Zawsze `HEARTBEAT_OK`, chyba że regresja" to najlepszy wzorzec zadania nocnego.**
Praca się dzieje, raport jest w pliku, a Ty dowiadujesz się **tylko wtedy, gdy coś
poszło nie tak**.

> 💡 **Zwróć uwagę, co to naprawdę znaczy.** Twój agent co noc uruchamia pełną
> ewaluację i porównuje z wczoraj. To jest rzecz, którą zespoły produktowe wdrażają
> jako „ciągłą ewaluację" i uznają za dojrzałość operacyjną. U Ciebie kosztuje prąd.

---

## 6. Bezpieczeństwo proaktywności

Agent działający bez Ciebie to inna klasa ryzyka — i wraca w części 16 jako **ASI10
(agenci zbuntowani)**: agent działa poza polityką przez kompromitację albo dryf,
**wyglądając na uprawnionego** i utrzymując się między sesjami.

**Cztery reguły, każda odpowiada na konkretną porażkę:**

| Reguła | Przed czym chroni |
| :-- | :-- |
| **1.** Zadanie z harmonogramu **nie dziedziczy** uprawnień hosta | przejęte zadanie nocne ma shell przez 8 h bez świadka |
| **2.** Operacje nieodwracalne **zawsze** wymagają człowieka | MoltMatch |
| **3.** Każde przebudzenie zostawia ślad, **także cisza** | agent, który „nic nie robi", a coś robi |
| **4.** Bezpiecznik: N błędów pod rząd → **wyłącz i powiadom** | pętla awarii przez noc |

```python
BEZPIECZNIK = {"bledow_pod_rzad": 3, "akcja": "wylacz_i_powiadom"}

def po_przebudzeniu(agent, wynik, stan):
    if wynik["status"] == "blad":
        stan[agent]["bledy"] += 1
        if stan[agent]["bledy"] >= BEZPIECZNIK["bledow_pod_rzad"]:
            _wylacz_harmonogram(agent)
            _powiadom_czlowieka(
                f"⚠️ Harmonogram '{agent}' WYŁĄCZONY po {stan[agent]['bledy']} błędach. "
                f"Ostatni: {wynik['blad'][:200]}\n"
                f"Włącz ponownie: sesja-cli.py harmonogram wlacz {agent}")
    else:
        stan[agent]["bledy"] = 0
```

⚠️ **Bezpiecznik jest tym elementem, którego brak boli najbardziej w praktyce.** Agent
z zepsutym zadaniem co godzinę przez weekend to 48 nieudanych przebudzeń, 48 wpisów
w dzienniku i — jeśli każde próbuje powiadomić o błędzie — 48 wiadomości.

---

## 7. EKSPERYMENT 11 — tydzień Gospodarza

**Hipoteza:** przy progu pilności 3 agent odzywa się 2–4 razy dziennie, z czego
**ponad 70 % jest warte przerwania**.

### 7.1 · Procedura

Uruchom Gospodarza na siedem dni. Po każdej wiadomości oceń ją **jednym klawiszem**
— inaczej nie wytrzymasz tygodnia:

```bash
python3 sesja-cli.py ocen --ostatnia
# [t] warto było   [n] hałas   [p] za późno   [x] pominięte (dopisz ręcznie)
```

Codziennie wieczorem dopisz przeoczenia: co się wydarzyło, o czym agent **powinien**
był powiedzieć, a zamilczał.

### 7.2 · Tabela tygodnia

| Dzień | Przebudzeń | Cisz | Wiadomości | Warto (TP) | Hałas (FP) | Przeoczeń (FN) |
| :-- | --: | --: | --: | --: | --: | --: |
| pon | | | | | | |
| … | | | | | | |
| **Razem** | | | | | | |

```
Precyzja = TP / (TP + FP)      ← ⭐ ta liczba decyduje o zaufaniu
Pełnia   = TP / (TP + FN)
Stosunek ciszy = cisze / przebudzenia
```

⚠️ **Predykcja do sprawdzenia:** stosunek ciszy wyjdzie **wysoki** (0,85–0,95) i tak
ma być. Precyzja w pierwszym tygodniu wyjdzie **niższa, niż się spodziewasz** —
obstawiam 0,5–0,7 — bo model interpretuje „warto" szerzej niż Ty.

### 7.3 · Kalibracja — i jak jej nie zepsuć

```bash
python3 sesja-cli.py kalibruj gospodarz --z-ocen
# proponuje: pilnosc_minimalna 3 → 4 (bo 6 z 9 hałasów miało pilność 3)
```

**Najcenniejszy produkt tego eksperymentu to nie liczba, tylko lista hałasów.**
Przeczytaj wszystkie FP i poszukaj wzorca — zwykle 2–3 kategorie odpowiadają za
większość. Dopisz je **wprost** do `HEARTBEAT.md` jako wyjątki:

```markdown
## Nigdy nie zgłaszaj
- Wydarzeń cyklicznych, które znam na pamięć (siłownia wt/czw 18:00)
- Wydarzeń bez miejsca i bez przygotowania
- Czegokolwiek, o czym mówiłeś w ciągu ostatnich 24 h
```

⭐ **To jest pętla uczenia się w tym systemie: mierzysz → czytasz błędy → dopisujesz
regułę do pliku → mierzysz ponownie.** Żadnego dostrajania modelu, żadnych wag. Trzy
zdania w pliku tekstowym, który możesz przeczytać i cofnąć (część 6).

---

## 8. PRODUKCYJNIE

| | `cron` | systemd timer | Celery/APScheduler | OpenClaw | **Twój** |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Wyzwalacz czasowy | ⭐ | ⭐ | ⭐ | ⭐ | ⭐ |
| Zdarzeniowy | ✗ | częściowo | ⭐ | ⭐ | ⭐ |
| **Idempotencja per okno** | ✗ | częściowo | ⭐ | ? | ⭐ |
| **Tłumienie ciszy** | ✗ | ✗ | ✗ | ⭐ `HEARTBEAT_OK` | ⭐ |
| **Ocena pilności modelem** | ✗ | ✗ | ✗ | ⭐ | ⭐ |
| **Bezpiecznik po błędach** | ✗ | `StartLimitBurst` | częściowo | ? | ⭐ |
| Zapis po polsku | ✗ | ✗ | ✗ | ⭐ | ⭐ |

**Uruchom planistę pod systemd** — nie wymyślaj nadzoru na nowo:

```ini
# $OSA/systemd/osa-planista.service  (szablon: @OSA@ = pełna ścieżka projektu)
[Unit]
Description=Planista agentów OSA
After=osa-brama.service
[Service]
ExecStart=@OSA@/.venv/bin/python @OSA@/harmonogram/planista.py
Restart=on-failure
RestartSec=30
StartLimitBurst=5
StartLimitIntervalSec=600
[Install]
WantedBy=default.target
```

systemd nie zna zmiennych z `rig-env.sh`, więc w pliku jednostki stoi znacznik `@OSA@`. `init.sh`
wstawia za niego prawdziwą ścieżkę i zapisuje gotowe jednostki w `systemd/wygenerowane/`:

```bash
cd $OSA && bash init.sh
cp systemd/wygenerowane/osa-planista.service ~/.config/systemd/user/ && systemctl --user daemon-reload
```

---

## 9. ĆWICZENIE

1. Napisz `HEARTBEAT.md` dla Gospodarza — z **sekcją „Nigdy nie zgłaszaj"** od razu.
2. Zaimplementuj planistę z idempotencją per okno i ciszą nocną.
3. Wepnij `HEARTBEAT_OK` w bramę; dodaj zdarzenia `heartbeat.cisza` i `.wiadomosc`.
4. Dodaj obserwator `~/skany/` budzący Archiwistę na nowy plik.
5. Napisz zadanie nocne: ewaluacja + porównanie z wczoraj + cisza, chyba że regresja.
6. Uruchom na tydzień i wypełnij tabelę.

```bash
python3 sesja-cli.py harmonogram status
# gospodarz   ✓ włączony   5 zadań   ostatnie: 07:00 (cisza)   dziś: 18 przebudzeń, 2 wiadomości
# archiwista  ✓ włączony   1 zdarzeniowe (~/skany)             dziś: 3 przebudzenia, 0 wiadomości
# badacz      ✗ wyłączony  (brak HEARTBEAT.md — celowo)
```

⭐ **Badacz nie ma harmonogramu i to jest decyzja projektowa.** Agent wychodzący do
sieci, działający bez nadzoru, to najgorsze możliwe połączenie: wrogie wejście plus
brak świadka. Badacz działa **tylko wtedy, gdy go poprosisz**.

---

## 10. Pułapki tej części

| ID | Pułapka | Objaw | Jak uniknąć |
| :-- | :-- | :-- | :-- |
| **P104** | **Dwie instancje planisty** | Zadanie poranne wykonane dwa razy, dwie wiadomości | Plik blokady z częścią 2 **plus** idempotencja per okno |
| **P105** | **Brak idempotencji przy restarcie** | Restart o 7:05 uruchamia ponownie zadanie z 7:00 | Klucz z okna czasowego, nie z momentu uruchomienia |
| **P106** | **Cisza rozpoznawana tylko po dokładnym ciągu** | Model pisze „OK", brama wysyła Ci wiadomość „OK" | Dopasowanie po prefiksie **i** minimalna długość treści |
| **P107** | **Brak ciszy nocnej i limitu dziennego** | Agent budzi Cię o 3:00 z pilnością 2 | Cisza nocna, limit dzienny, minimalny odstęp — wszystkie trzy |
| **P108** | **Brak bezpiecznika po serii błędów** | Zepsute zadanie mieli przez weekend i zalewa dziennik | 3 błędy pod rząd → wyłącz harmonogram i powiadom **raz** |

---

## 11. Checkpoint

```bash
cd $OSA
systemctl --user is-active osa-planista && echo "✓ planista działa"
python3 - <<'EOF'
from harmonogram.planista import _klucz_wykonania, parsuj
import datetime
z = {"naglowek":"Co rano (7:00)","typ":"dziennie"}
a = _klucz_wykonania("gospodarz", z, datetime.datetime(2026,9,23,7,0))
b = _klucz_wykonania("gospodarz", z, datetime.datetime(2026,9,23,7,5))
assert a == b, "P105: restart uruchomi zadanie ponownie"
print("✓ idempotencja per okno")
EOF
python3 sesja-cli.py harmonogram status
test -s pomiary/gospodarz-tydzien.csv && echo "✓ tydzień zmierzony"
git add -A && git commit -m "część 11: planista, HEARTBEAT, tłumienie ciszy, bezpiecznik"
```

- [ ] `HEARTBEAT.md` napisany zdaniami, z sekcją „Nigdy nie zgłaszaj"
- [ ] `HEARTBEAT_OK` tłumione przez bramę; cisza jest **domyślną** odpowiedzią
- [ ] Idempotencja per okno — restart nie powtarza zadania
- [ ] Wyzwalacze zdarzeniowe tam, gdzie się da; czasowe tylko dla przeglądów
- [ ] Próg pilności, limit dzienny, cisza nocna, minimalny odstęp
- [ ] Zadanie nocne robi ewaluację i milczy, chyba że regresja
- [ ] Bezpiecznik wyłącza harmonogram po 3 błędach i powiadamia raz
- [ ] Zadanie z harmonogramu **nie ma** uprawnień hosta
- [ ] ⭐ **Tydzień zmierzony: znasz precyzję, pełnię i stosunek ciszy**

---

**Dalej: `12-KANALY-INTERFEJSY.md`** — jak z agentem rozmawiasz i dlaczego kanał jest
granicą zaufania, a nie tylko wejściem.
