# Część 5 · Pamięć długoterminowa — trzy szkoły

**Poziom:** ⭐⭐⭐⭐ · **Czas:** ~6 h · **Wymaga:** części 4 (kontekst ≠ pamięć)
**Produkuje:** magazyn bi-temporalny, wydobywanie faktów, unieważnianie, mini-benchmark pamięci

---

## 0. Pytanie, na które pamięć musi umieć odpowiedzieć

Trzy pytania. Pierwsze umie prawie każdy system. Drugie — nieliczne. Trzecie —
prawie żaden.

```
1. „Jaki jest mój numer NIP?"
   → wyszukanie faktu.                           łatwe

2. „Ile płacę za prąd?"
   → było 210 zł, potem 280 zł, od lipca 245 zł.
     Która odpowiedź jest poprawna?              trudne

3. „Ile płaciłem za prąd w kwietniu?"
   → fakt, który JUŻ NIE JEST prawdziwy,
     ale WTEDY był.                              bardzo trudne
```

Pytanie 3 rozstrzyga, czy Twój agent ma pamięć, czy tylko wyszukiwarkę. I to jest
dokładnie ten wymiar, w którym systemy pamięci agentowej się w 2026 rozjechały.

---

## 1. Trzy szkoły — i liczba, która je porządkuje

| Szkoła | Reprezentant | Idea | LongMemEval |
| :-- | :-- | :-- | --: |
| **Czytelne pliki** | OpenClaw | `MEMORY.md`, który otwierasz i czytasz | — |
| **Pamięć wirtualna** | Letta / MemGPT | stronicowanie kontekst ↔ dysk, bloki samo-edytowalne | — |
| **Wektory + graf** | Mem0 | trzy zakresy, wyszukiwanie semantyczne | **49 %** |
| **Graf bi-temporalny** | Zep / Graphiti | każdy fakt ma czas świata **i** czas systemu | ⭐ **71,2 %** |

Źródło liczb: [porównanie pięciu systemów pamięci](https://medium.com/@wasowski.jarek/i-compared-5-ai-agent-memory-systems-across-6-dimensions-none-wins-6a658335ed0a).

**Dwadzieścia dwa punkty procentowe różnicy** to nie jest szum. To jest różnica
w architekturze — i wynika prawie w całości z odpowiedzi na pytanie 3.

### 1.1 · Szkoła 1 — czytelne pliki (OpenClaw)

```markdown
# MEMORY.md
- Michał, Kraków, strefa Europe/Warsaw
- Pracuje nad projektem „suwerenny agent" — agenty lokalne dla zawodów regulowanych
- Nie znosi odpowiedzi zaczynających się od „Świetne pytanie!"
- Rachunek za prąd: 245 zł (od lipca 2026; wcześniej 280 zł)
```

| Zalety | Wady |
| :-- | :-- |
| ⭐ **Audytowalne** — otwierasz i czytasz | Nie skaluje się powyżej ~2 tys. tokenów |
| ⭐ Da się wersjonować w git i **cofnąć** | Brak wyszukiwania — albo całość w kontekście, albo nic |
| ⭐ Użytkownik może poprawić ręcznie | Czas obsługiwany „ręcznie", w nawiasie |
| Zero zależności | Sprzeczności rozstrzyga model, nie system |

**Nie lekceważ tej szkoły.** Dla agenta osobistego, gdzie faktów o użytkowniku jest
kilkadziesiąt, plik `MEMORY.md` **bije wszystko inne** — bo jest zrozumiały,
poprawialny i nie ma czego zepsuć. To jest domyślna pamięć Twojego systemu w części 6.

### 1.2 · Szkoła 2 — pamięć wirtualna (Letta / MemGPT)

Analogia do systemu operacyjnego: kontekst to RAM, dysk to swap, a agent **sam
zarządza stronicowaniem** przez narzędzia `memory_insert`, `memory_replace`,
`memory_search`.

Bloki pamięci **zostają w kontekście na stałe** (persona, użytkownik), a agent może je
edytować. Dodatkowo „sleep-time compute" — porządkowanie pamięci, gdy nikt nie pyta.

| Zalety | Wady |
| :-- | :-- |
| ⭐ Agent sam decyduje, co ważne | ⚠️ Agent sam decyduje, co ważne |
| Bloki stałe = spójna tożsamość | Kosztuje tury modelu na zarządzanie |
| Elegancka abstrakcja | Brak czasu — nadpisanie kasuje historię |

⭐ **Jedna rzecz z tej szkoły, którą bierzesz na pewno: `sleep-time compute`.** Twoja
maszyna stoi bezczynnie przez większość doby. Porządkowanie pamięci o 4:00 jest
**darmowe** — to jest przewaga lokalnego sprzętu, której nie ma nikt płacący za token.
Wraca w części 11 jako zadanie harmonogramu.

### 1.3 · Szkoła 3 — graf bi-temporalny (Zep / Graphiti)

Tu jest ta różnica 22 punktów. **Każdy fakt niesie cztery znaczniki czasu, nie jeden.**

```
                     CZAS ŚWIATA                CZAS SYSTEMU
              (kiedy to było prawdą)     (kiedy system o tym wiedział)
                ┌──────────────┐           ┌──────────────┐
  fakt   ───────┤ ważny_od     │           │ zapisany     │
                │ ważny_do     │           │ unieważniony │
                └──────────────┘           └──────────────┘
```

```
Rachunek za prąd = 280 zł   ważny 2026-03-01 … 2026-06-30
                            zapisany 2026-03-05, unieważniony 2026-07-02

Rachunek za prąd = 245 zł   ważny 2026-07-01 … (nadal)
                            zapisany 2026-07-02
```

Teraz **wszystkie trzy pytania z §0 mają jednoznaczną odpowiedź**:

```sql
-- „Ile płacę teraz?"           → ważny_od ≤ dziś < ważny_do
-- „Ile płaciłem w kwietniu?"   → ważny_od ≤ 2026-04-15 < ważny_do   → 280 zł
-- „Co system wiedział w maju?" → zapisany ≤ 2026-05-01 < unieważniony
```

**Trzecie zapytanie jest tym, które ratuje Cię przy debugowaniu.** „Dlaczego agent
powiedział w maju 280 zł?" → bo wtedy to była jego najlepsza wiedza. **To nie był
błąd.** Bez czasu systemu nie odróżnisz pomyłki agenta od nieaktualnych danych — a to
zupełnie różne diagnozy.

---

## 2. Wybór dla Twojego systemu

**Nie wybierasz jednej. Warstwujesz trzy**, bo rozwiązują różne problemy:

```
┌─ MEMORY.md ─────────── kilkadziesiąt faktów o użytkowniku
│  czytelny, w kontekście zawsze, ręcznie poprawialny        (część 6)
│
├─ magazyn bi-temporalny ─ setki/tysiące faktów ze zmianą w czasie
│  wyszukiwany, wersjonowany czasowo                         (ta część)
│
└─ korpus + RAG ────────── dokumenty, niezmienne
   wyszukiwanie hybrydowe                              (kurs 1, część 4)
```

**Reguła przydziału:** fakt trafia do `MEMORY.md`, jeśli chcesz go **widzieć na oczy
przy każdej rozmowie**. Do magazynu — jeśli **może się zmienić i chcesz wiedzieć
kiedy**. Do korpusu — jeśli to **dokument, nie fakt**.

---

## 3. OD ZERA — magazyn bi-temporalny

### 3.1 · Schemat

```python
# $OSA/pamiec/magazyn.py
"""Pamięć bi-temporalna. Fakt = (podmiot, relacja, obiekt) + 4 znaczniki czasu."""
import os, sqlite3, pathlib, datetime, json

SCHEMAT = """
CREATE TABLE IF NOT EXISTS fakty (
  id           INTEGER PRIMARY KEY,
  zakres       TEXT NOT NULL,          -- P80: izolacja (agent / sprawa / użytkownik)
  podmiot      TEXT NOT NULL,
  relacja      TEXT NOT NULL,
  obiekt       TEXT NOT NULL,
  -- czas świata: kiedy to było/jest prawdą
  wazny_od     TEXT NOT NULL,
  wazny_do     TEXT,                   -- NULL = nadal prawdziwy
  -- czas systemu: kiedy system o tym wiedział
  zapisany     TEXT NOT NULL,
  uniewazniony TEXT,                   -- NULL = nadal w mocy
  -- pochodzenie
  zrodlo       TEXT NOT NULL,          -- P79: skąd to wiem
  sesja        TEXT,
  pewnosc      REAL DEFAULT 1.0,
  cytat        TEXT                    -- dosłowny fragment źródła
);
CREATE INDEX IF NOT EXISTS i_szukaj  ON fakty(zakres, podmiot, relacja);
CREATE INDEX IF NOT EXISTS i_czas    ON fakty(zakres, wazny_od, wazny_do);
CREATE VIRTUAL TABLE IF NOT EXISTS fakty_fts USING fts5(
  podmiot, relacja, obiekt, cytat, content='fakty', content_rowid='id');
"""

TERAZ = lambda: datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")

class Magazyn:
    def __init__(self, sciezka="$OSA/pamiec/pamiec.db"):
        p = pathlib.Path(os.path.expandvars(sciezka)).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(p, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMAT)
        self.db.execute("PRAGMA journal_mode=WAL")
```

### 3.2 · Zapis z unieważnianiem — serce systemu

```python
    def zapisz(self, zakres, podmiot, relacja, obiekt, *,
               wazny_od=None, zrodlo="rozmowa", sesja=None, pewnosc=1.0, cytat=None):
        """Zapisuje fakt. Jeśli istnieje sprzeczny — UNIEWAŻNIA go, nie kasuje."""
        wazny_od = wazny_od or TERAZ()
        stare = self.db.execute("""
            SELECT id, obiekt, wazny_od FROM fakty
            WHERE zakres=? AND podmiot=? AND relacja=?
              AND uniewazniony IS NULL AND wazny_do IS NULL
        """, (zakres, podmiot, relacja)).fetchall()

        for s in stare:
            if s["obiekt"] == obiekt:
                return {"akcja": "bez_zmian", "id": s["id"]}     # ten sam fakt
            # ⭐ sprzeczność: zamykamy stary fakt w OBU osiach czasu
            self.db.execute(
                "UPDATE fakty SET wazny_do=?, uniewazniony=? WHERE id=?",
                (wazny_od, TERAZ(), s["id"]))

        kur = self.db.execute("""
            INSERT INTO fakty(zakres,podmiot,relacja,obiekt,wazny_od,zapisany,
                              zrodlo,sesja,pewnosc,cytat)
            VALUES(?,?,?,?,?,?,?,?,?,?)""",
            (zakres, podmiot, relacja, obiekt, wazny_od, TERAZ(),
             zrodlo, sesja, pewnosc, cytat))
        self.db.execute("""INSERT INTO fakty_fts(rowid,podmiot,relacja,obiekt,cytat)
                           VALUES(?,?,?,?,?)""",
                        (kur.lastrowid, podmiot, relacja, obiekt, cytat or ""))
        self.db.commit()
        return {"akcja": "zastapiono" if stare else "nowy",
                "id": kur.lastrowid, "uniewazniono": [s["id"] for s in stare]}
```

⭐ **Zwróć uwagę: nigdzie nie ma `DELETE`.** Sprzeczny fakt dostaje `wazny_do`
(przestał być prawdą wtedy) i `uniewazniony` (dowiedzieliśmy się o tym teraz).
Historia jest kompletna i **nie da się jej zgubić przypadkiem**.

### 3.3 · Odczyt — zapytanie bi-temporalne

```python
    def czytaj(self, zakres, podmiot=None, relacja=None, *,
               na_moment=None, wiedza_z=None, limit=50):
        """na_moment  — co było PRAWDĄ w tym momencie (czas świata)
           wiedza_z   — co system WIEDZIAŁ w tym momencie (czas systemu)
           oba puste  — stan aktualny wedle aktualnej wiedzy"""
        t, k = na_moment or TERAZ(), wiedza_z or TERAZ()
        sql = ["SELECT * FROM fakty WHERE zakres=?",
               "AND wazny_od <= ? AND (wazny_do IS NULL OR wazny_do > ?)",
               "AND zapisany <= ? AND (uniewazniony IS NULL OR uniewazniony > ?)"]
        a = [zakres, t, t, k, k]
        if podmiot: sql.append("AND podmiot=?"); a.append(podmiot)
        if relacja: sql.append("AND relacja=?"); a.append(relacja)
        sql.append("ORDER BY wazny_od DESC LIMIT ?"); a.append(limit)
        return [dict(r) for r in self.db.execute(" ".join(sql), a)]

    def historia(self, zakres, podmiot, relacja):
        """Pełna oś czasu jednego faktu — do debugowania i do pytania 3."""
        return [dict(r) for r in self.db.execute("""
            SELECT obiekt, wazny_od, wazny_do, zapisany, uniewazniony, zrodlo
            FROM fakty WHERE zakres=? AND podmiot=? AND relacja=?
            ORDER BY wazny_od""", (zakres, podmiot, relacja))]

    def szukaj(self, zakres, zapytanie, limit=10):
        """FTS5 + filtr aktualności. Hybryda z wektorami — w §5."""
        return [dict(r) for r in self.db.execute("""
            SELECT f.* FROM fakty_fts x JOIN fakty f ON f.id = x.rowid
            WHERE fakty_fts MATCH ? AND f.zakres=?
              AND f.wazny_do IS NULL AND f.uniewazniony IS NULL
            ORDER BY rank LIMIT ?""", (zapytanie, zakres, limit))]
```

**Sprawdź, że trzy pytania z §0 działają:**

```python
m = Magazyn("/tmp/test.db")
m.zapisz("michal", "rachunek_prad", "kwota", "280 zł", wazny_od="2026-03-01")
m.zapisz("michal", "rachunek_prad", "kwota", "245 zł", wazny_od="2026-07-01")

print(m.czytaj("michal", "rachunek_prad")[0]["obiekt"])                    # 245 zł
print(m.czytaj("michal", "rachunek_prad", na_moment="2026-04-15")[0]["obiekt"])  # 280 zł
print(m.czytaj("michal", "rachunek_prad", wiedza_z="2026-05-01")[0]["obiekt"])   # 280 zł
for h in m.historia("michal", "rachunek_prad", "kwota"): print(h)
```

---

## 4. Wydobywanie faktów — skąd biorą się trójki

Magazyn jest bezużyteczny, jeśli nikt go nie karmi. Fakty wydobywasz **po każdej turze**,
lokalnym modelem, z gramatyką (kurs 1, część 3).

```python
# $OSA/pamiec/wydobywanie.py
PROMPT = """Wypisz fakty o użytkowniku z poniższej rozmowy.

Fakt to trwała informacja, która będzie prawdziwa także jutro.
NIE jest faktem: pytanie, prośba, treść zadania, opinia o czymś jednorazowym.

Dla każdego faktu podaj:
- podmiot   (czego dotyczy, np. "rachunek_prad", "auto", "preferencje")
- relacja   (jaka cecha, np. "kwota", "marka", "format_odpowiedzi")
- obiekt    (wartość)
- wazny_od  (data ISO, jeśli rozmowa ją podaje; inaczej null)
- cytat     (DOSŁOWNY fragment, z którego to wynika)

Gdy rozmowa nie zawiera żadnego trwałego faktu — zwróć pustą listę.
To jest częste i poprawne. NIE WYMYŚLAJ faktów.

ROZMOWA:
{rozmowa}"""

GRAMATYKA = r'''
root   ::= "[" ws (fakt (ws "," ws fakt)*)? ws "]"
fakt   ::= "{" ws "\"podmiot\":" ws str "," ws "\"relacja\":" ws str "," ws
           "\"obiekt\":" ws str "," ws "\"wazny_od\":" ws (str | "null") "," ws
           "\"cytat\":" ws str ws "}"
str    ::= "\"" ([^"\\] | "\\" .)* "\""
ws     ::= [ \t\n]*
'''
```

⚠️ **Zdanie „Gdy rozmowa nie zawiera faktu — zwróć pustą listę. To jest częste
i poprawne" jest tam celowo.** Bez niego model **wymyśla fakty**, bo czuje presję, żeby
coś zwrócić. To jest jedna z najczęstszych przyczyn zatrucia pamięci — i najtańsza do
naprawienia.

### 4.1 · Trzy filtry przed zapisem

```python
def filtruj(fakty: list, sesja_zaufanie: str) -> list:
    dobre = []
    for f in fakty:
        # 1. Cytat musi realnie występować w rozmowie — inaczej to halucynacja
        if f["cytat"] not in ROZMOWA_TEKST:
            continue
        # 2. P81: sesja niezaufana NIE zapisuje do pamięci trwałej
        if sesja_zaufanie != "host":
            f["pewnosc"] = 0.3
            f["zakres"] = f"kwarantanna:{f['zakres']}"
        # 3. Fakty o samym agencie/instrukcjach — odrzuć (wektor wstrzyknięcia)
        if any(s in f["obiekt"].lower() for s in
               ("zignoruj", "instrukcj", "system prompt", "nie mów użytkownikowi")):
            continue
        dobre.append(f)
    return dobre
```

⭐ **Filtr 2 jest najważniejszy i wraca w części 16 jako ASI06.** Wiadomość z kanału
zewnętrznego, która trafia do pamięci trwałej, to **trwałe wstrzyknięcie** — wypłata
przychodzi sesje później i jest prawie niemożliwa do wyśledzenia. Kwarantanna oznacza:
zapisz, ale w osobnym zakresie, z niską pewnością i **nie doładowuj automatycznie**.

---

## 5. Hybryda: FTS5 + wektory

FTS5 znajdzie „rachunek prąd". Nie znajdzie „ile płacę za energię elektryczną".
Wektory znajdą to drugie, ale zgubią identyfikatory (pułapka P30 z kursu 1).

**Połącz je przez RRF** — tak jak w kursie 1, część 4:

```python
def szukaj_hybrydowo(self, zakres, zapytanie, embed, limit=10, k=60):
    tekst = {r["id"]: i for i, r in enumerate(self.szukaj(zakres, zapytanie, 50))}
    wekt  = {r["id"]: i for i, r in enumerate(self._szukaj_wektorowo(zakres, embed(zapytanie), 50))}
    punkty = {}
    for zbior in (tekst, wekt):
        for id_, poz in zbior.items():
            punkty[id_] = punkty.get(id_, 0) + 1 / (k + poz + 1)
    naj = sorted(punkty, key=punkty.get, reverse=True)[:limit]
    return [self._po_id(i) for i in naj]
```

> 💡 **Kiedy w ogóle warto dokładać wektory.** Poniżej ~500 faktów samo FTS5 z dobrze
> dobranymi nazwami relacji wystarcza i jest **wielokrotnie szybsze**. Dołóż wektory,
> gdy zmierzysz, że FTS5 gubi pytania parafrazowane — nie wcześniej.

---

## 6. Doładowanie pamięci do kontekstu

Pamięć jest bezwartościowa, jeśli nie trafia w odpowiednim momencie do promptu.
Stosujesz zasadę z części 3: **doładowanie w ostatniej chwili, z twardym budżetem**.

```python
def doladuj(magazyn, zakres, pytanie, embed, budzet_tokenow=600) -> str:
    kandydaci = magazyn.szukaj_hybrydowo(zakres, pytanie, embed, limit=20)
    linie, zuzyte = [], 0
    for f in kandydaci:
        l = f"- {f['podmiot']}.{f['relacja']} = {f['obiekt']}"
        if f["wazny_od"][:10] != "1970-01-01":
            l += f"  (od {f['wazny_od'][:10]})"
        if f["pewnosc"] < 0.8:
            l += f"  ⚠️ pewność {f['pewnosc']}, źródło: {f['zrodlo']}"
        koszt = len(l) // 3
        if zuzyte + koszt > budzet_tokenow:
            break
        linie.append(l); zuzyte += koszt
    if not linie:
        return ""
    return "ZNANE FAKTY (z pamięci; jeśli rozmowa im przeczy — zaufaj rozmowie):\n" + "\n".join(linie)
```

⚠️ **Zdanie „jeśli rozmowa im przeczy — zaufaj rozmowie" jest konieczne.** Bez niego
model broni nieaktualnego faktu z pamięci przeciwko temu, co użytkownik właśnie
powiedział. Wygląda to jak upór i jest jednym z najbardziej irytujących zachowań
agentów z pamięcią.

---

## 7. PRODUKCYJNIE — kiedy sięgnąć po gotowe

| | Twój magazyn | Mem0 | Zep/Graphiti | Letta |
| :-- | :-- | :-- | :-- | :-- |
| Bi-temporalność | ⭐ pełna | ✗ | ⭐ pełna | ✗ |
| Zależności | **SQLite (stdlib)** | usługa/SDK | usługa + graf | serwer |
| Offline | ⭐ całkowicie | częściowo | ⚠️ zwykle usługa | tak |
| Wydobywanie faktów | Twój prompt | wbudowane | ⭐ dojrzałe | wbudowane |
| Graf relacji | ✗ (płaskie trójki) | częściowo | ⭐ pełny | ✗ |
| Skala | ~10⁵ faktów | 10⁶+ | 10⁶+ | 10⁵ |
| LongMemEval | zmierz (§8) | 49 % | 71,2 % | — |

**Rekomendacja:** zostań przy swoim. Powód jest konkretny: **bi-temporalność masz,
a offline i brak zależności są u Ciebie wymaganiem twardym**, nie preferencją. Graf
relacji (czego Ci brakuje) przyda się dopiero, gdy zaczniesz pytać „kto jest powiązany
z kim" — a przy agencie osobistym to rzadkie.

> ⚠️ **Sprawdź sam, zanim uwierzysz w 71,2 %.** Ta liczba pochodzi z LongMemEval na
> zadaniach konwersacyjnych po angielsku. **Twój przypadek to polskie fakty osobowe**,
> gdzie wydobywanie działa inaczej. Dlatego §8.

---

## 8. EKSPERYMENT 5 — mini-benchmark pamięci

**Hipoteza:** magazyn bi-temporalny bije płaskie `MEMORY.md` **wyłącznie na pytaniach
o zmianę w czasie**, a na pytaniach o stan aktualny są równe.

### 8.1 · Zestaw testowy

```bash
mkdir -p $OSA/pomiary/pamiec && cd $OSA/pomiary/pamiec
```

Zbuduj 60 pytań w czterech kategoriach po 15:

| Kategoria | Przykład | Co mierzy |
| :-- | :-- | :-- |
| **A · stan aktualny** | „Ile płacę za prąd?" | wyszukanie |
| **B · stan historyczny** | „Ile płaciłem w kwietniu?" | ⭐ czas świata |
| **C · zmiana** | „Czy rachunek się zmienił? Kiedy?" | ⭐ oś czasu |
| **D · odmowa** | „Jaki mam numer buta?" (nigdy nie podany) | ⭐ **„nie wiem"** |

⭐ **Kategoria D jest tą, o której wszyscy zapominają, i tą, która najbardziej boli
w praktyce.** System pamięci, który na nieznane pytanie zwraca najbliższy fakt zamiast
„nie wiem", **jest gorszy niż brak pamięci** — bo brzmi wiarygodnie.

### 8.2 · Syntetyczna historia

```python
# historia.py — 8 miesięcy życia z 12 zmianami faktów
ZDARZENIA = [
  ("2026-01-10", "rachunek_prad", "kwota", "210 zł"),
  ("2026-03-01", "rachunek_prad", "kwota", "280 zł"),
  ("2026-07-01", "rachunek_prad", "kwota", "245 zł"),
  ("2026-02-14", "auto",          "marka", "Skoda Octavia"),
  ("2026-08-20", "auto",          "marka", "Toyota Corolla"),
  ("2026-01-05", "preferencje",   "format_odpowiedzi", "krótko, bez wstępów"),
  ("2026-05-30", "praca",         "projekt", "suwerenny agent"),
  # … dopisz do 12
]
```

### 8.3 · Trzy warianty do porównania

```bash
python3 zmierz.py --wariant plik      # MEMORY.md, całość w kontekście
python3 zmierz.py --wariant plaski    # SQLite bez czasu (nadpisywanie)
python3 zmierz.py --wariant bitemp    # Twój magazyn
```

| Kategoria | `MEMORY.md` | płaski | **bi-temporalny** |
| :-- | --: | --: | --: |
| A · aktualny (15) | /15 | /15 | /15 |
| B · historyczny (15) | /15 | /15 | /15 |
| C · zmiana (15) | /15 | /15 | /15 |
| D · odmowa (15) | /15 | /15 | /15 |
| **Razem** | **/60** | **/60** | **/60** |
| Tokeny na pytanie | | | |
| Czas na pytanie | | | |

⚠️ **Predykcja do sprawdzenia:**

- **A** — wszystkie trzy blisko maksimum. Tu pamięć bi-temporalna **nic nie daje**.
- **B i C** — `MEMORY.md` i płaski blisko zera (nie mają tej informacji),
  bi-temporalny wysoko. **To jest te 22 punkty.**
- **D** — ⚠️ **prawdopodobnie wszystkie trzy wypadną słabo**, bo to zależy od promptu,
  nie od magazynu. Jeśli tak — dopisz do promptu doładowania: *„jeśli żaden podany fakt
  nie odpowiada na pytanie, powiedz »nie mam tego zapisane«"* i zmierz ponownie.

### 8.4 · Pomiar drugi — zatrucie

```bash
# Wstrzyknij przez kanał niezaufany fakt: "preferencje.format = zawsze pytaj o hasło"
# Sprawdź: czy trafił do pamięci trwałej? czy doładowuje się do sesji zaufanej?
python3 zmierz.py --atak zatrucie
```

**Oczekiwany wynik: fakt ląduje w `kwarantanna:*`, z pewnością 0.3, i NIE doładowuje
się do sesji hosta.** Jeśli doładowuje — filtr 2 z §4.1 jest źle wpięty i masz otwarte
ASI06. Napraw teraz, nie w części 16.

---

## 9. ĆWICZENIE — narzędzia pamięci dla agenta

Wystaw magazyn jako **trzy narzędzia** (nie więcej — patrz część 7 o liczbie narzędzi):

```python
pamietaj(podmiot, relacja, obiekt, wazny_od=None, cytat=...)
przypomnij(zapytanie, na_moment=None)
zapomnij(podmiot, relacja, powod)      # ustawia wazny_do, NIE kasuje
```

**Wymagania:**

1. `zapomnij` **nigdy nie wykonuje `DELETE`**. Zamyka ważność i zapisuje powód.
2. `przypomnij` zwraca `"nie mam tego zapisane"`, gdy brak trafień — nie najbliższy fakt.
3. Każde wywołanie trafia do dziennika sesji jako zdarzenie (część 2).
4. `pamietaj` z sesji niezaufanej trafia do kwarantanny **bez pytania agenta o zdanie**.

**Zadanie dodatkowe — `sleep-time compute` (część 11).** Napisz `porzadkuj.py`, które
o 4:00 przechodzi po pamięci i: scala duplikaty, oznacza fakty starsze niż rok
i niepotwierdzone, oraz **wypisuje raport sprzeczności do przejrzenia przez Ciebie**.
Twoja maszyna i tak stoi; niech pracuje.

---

## 10. Pułapki tej części

| ID | Pułapka | Objaw | Jak uniknąć |
| :-- | :-- | :-- | :-- |
| **P77** | **Nadpisywanie faktu zamiast unieważniania** | Agent nie umie odpowiedzieć „ile płaciłem w kwietniu" i nie wiesz, kiedy dane się zmieniły | Żadnego `DELETE` ani `UPDATE obiekt`. Zawsze `wazny_do` + nowy wiersz |
| **P78** | **Mylenie czasu świata z czasem systemu** | Nie odróżniasz „agent się pomylił" od „agent miał stare dane" | Cztery znaczniki, nie dwa. `wazny_*` ≠ `zapisany`/`uniewazniony` |
| **P79** | **Fakt bez cytatu i źródła** | Nie da się sprawdzić, skąd agent to wie; halucynacja wygląda jak pamięć | `cytat` obowiązkowy, weryfikowany przez występowanie w źródle |
| **P80** | **Brak zakresu — pamięć przecieka między agentami** | Badacz widzi fakty Archiwisty; w produkcie: sprawa A wycieka do sprawy B | `zakres` w kluczu każdego zapytania. **Nigdy zapytania bez zakresu** |
| **P81** | **Sesja niezaufana pisze do pamięci trwałej** | Trwałe wstrzyknięcie; wypłata sesje później, nie do wyśledzenia | Kwarantanna + niska pewność + brak automatycznego doładowania |

---

## 11. Checkpoint

```bash
cd $OSA
python3 - <<'EOF'
from pamiec.magazyn import Magazyn
m = Magazyn("/tmp/ck.db")
m.zapisz("t", "x", "v", "A", wazny_od="2026-01-01")
m.zapisz("t", "x", "v", "B", wazny_od="2026-06-01")
assert m.czytaj("t","x")[0]["obiekt"] == "B",                       "stan aktualny"
assert m.czytaj("t","x",na_moment="2026-03-01")[0]["obiekt"] == "A","czas świata"
assert len(m.historia("t","x","v")) == 2,                           "historia pełna"
assert m.czytaj("inny_zakres","x") == [],                           "izolacja zakresu"
print("✓ bi-temporalność, historia i izolacja działają")
EOF
test -s pomiary/pamiec/wyniki.csv && echo "✓ benchmark przeprowadzony"
git add -A && git commit -m "część 5: pamięć bi-temporalna, wydobywanie faktów, kwarantanna"
```

- [ ] Znasz trzy szkoły i wiesz, którą warstwę rozwiązuje każda
- [ ] Rozumiesz różnicę między czasem świata a czasem systemu
- [ ] Magazyn **nigdy nie kasuje** — unieważnia
- [ ] Umiesz odpowiedzieć na wszystkie trzy pytania z §0
- [ ] Wydobywanie faktów ma gramatykę, cytat i zgodę na pustą listę
- [ ] Zakres izoluje pamięć między agentami — **sprawdzone testem**
- [ ] Sesja niezaufana trafia do kwarantanny
- [ ] ⭐ **Zmierzyłeś swoje trzy warianty na 60 pytaniach w czterech kategoriach**

---

**Dalej: `06-TOZSAMOSC-PLIKI-ROBOCZE.md`** — `SOUL.md`, `AGENTS.md`, `HEARTBEAT.md`:
dlaczego czytelny plik tekstowy bije dostrajanie modelu.
