# Część 4 — Pamięć: RAG i inżynieria kontekstu od zera

**Poziom: ⭐⭐⭐⭐** · Wymaga: części 2–3 · Czas: ~6 h

> **Po co ten rozdział.** Model nie wie nic o Twoich dokumentach. Kontekst masz skończony
> (część 2 §5.3). Rozwiązaniem jest **wyszukiwanie + wstrzykiwanie** — RAG.
>
> Napiszesz bazę wektorową **od zera, w czystym Pythonie**, bez `numpy`, bez `langchain`,
> bez `chromadb`. Nie dlatego, że tak jest lepiej na produkcji — dlatego, że potem będziesz
> **rozumiał**, co robi za Ciebie biblioteka i dlaczego czasem robi to źle.

```bash
cd ~/llm-education   # katalog repozytorium (u Ciebie może być inny)
source rig-env.sh
mkdir -p $KURS      # katalog roboczy kursu (jest już, jeśli robiłeś część 2)
```

---

## Spis treści

| § | Temat | Kluczowa myśl |
| :-- | :-- | :-- |
| [1](#1-czym-rag-naprawdę-jest-i-gdzie-zawodzi) | **Czym RAG jest** | to wyszukiwarka z modelem na końcu, nie magia |
| [2](#2-model-embeddingowy--pobierz-właściwy) | **Model embeddingowy** | dedykowany bije generatywny 10× |
| [3](#3-chunking--najważniejsza-decyzja-w-całym-rag-u) | **Chunking** | ⭐ ważniejszy niż wybór modelu |
| [4](#4-baza-wektorowa-w-sqlite--od-zera) | **Baza wektorowa** | jeden plik, czysty Python |
| [5](#5-bm25--dlaczego-same-wektory-nie-wystarczą) | **BM25** | wektory gubią numery faktur |
| [6](#6-wyszukiwanie-hybrydowe-i-reranking) | **Hybryda + rerank** | fuzja rankingów, potem model jako sędzia |
| [7](#7-cytowania-i-uziemienie) | **Cytowania** | ⭐ bez tego produkt księgowy jest bezwartościowy |
| [8](#8-inżynieria-kontekstu--budżet-i-kompakcja) | **Budżet kontekstu** | ⭐ fundament części 6 |
| [9](#9-ewaluacja-rag-u) | **Ewaluacja** | dwie osobne metryki, nie jedna |

---

## 1. Czym RAG naprawdę jest i gdzie zawodzi

```
  pytanie użytkownika
        │
        ├──► [1] embedding pytania
        │
        ├──► [2] szukaj podobnych fragmentów w bazie      ← to jest WYSZUKIWARKA
        │
        ├──► [3] weź K najlepszych
        │
        ├──► [4] wklej je do promptu razem z pytaniem      ← to jest "augmentacja"
        │
        └──► [5] model odpowiada TYLKO na podstawie wklejonego
```

⚠️ **Najważniejsza rzecz o RAG-u: jakość odpowiedzi jest ograniczona przez krok [2].**
Jeśli wyszukiwarka nie znajdzie właściwego fragmentu, **żaden model tego nie naprawi**.
Mądrzejszy model da Ci ładniejszą, pewniej brzmiącą, wciąż błędną odpowiedź.

### 1.1 Cztery sposoby, w jakie RAG zawodzi

| Awaria | Objaw | Gdzie naprawiać |
| :-- | :-- | :-- |
| **fragment nie znaleziony** | model mówi „nie mam informacji" mimo że jest w dokumentach | chunking (§3), hybryda (§6) |
| **fragment znaleziony, ale przycięty** | odpowiedź urwana w pół zdania, brak kontekstu | chunking + zakładka (§3) |
| **model ignoruje kontekst** | odpowiada z pamięci treningowej, nie z dokumentu | prompt + cytowania (§7) |
| **model zmyśla cytowanie** | podaje źródło, którego nie ma | weryfikacja w kodzie (§7.3) |

💡 **Gdy RAG nie działa, w 80 % przypadków problem jest w chunkingu, nie w modelu.**
Zapamiętaj tę proporcję — zaoszczędzi Ci tygodnie.

---

## 2. Model embeddingowy — pobierz właściwy

Część 2 §7 użyła Bielika i pokazała, że działa słabo (pułapka **P24**). Teraz bierzemy
narzędzie do zadania.

### 2.1 Co wybrać dla polskiego

| Model | Rozmiar | Wymiar | Dlaczego |
| :-- | --: | --: | :-- |
| **`bge-m3`** | ~1,2 GB (GGUF f16) | 1024 | ⭐ **polecam** — wielojęzyczny, mocny polski, długie fragmenty (8192 tok) |
| `multilingual-e5-large` | ~1,1 GB | 1024 | dobra alternatywa, lżejsza; wymaga prefiksów `query:`/`passage:` |
| `paraphrase-multilingual-MiniLM` | ~0,5 GB | 384 | najszybszy, najsłabszy — do prototypów |

💡 **Dlaczego to dobre wiadomości:** model embeddingowy jest **~20× mniejszy** od modelu
generatywnego. Zmieści się obok w VRAM bez walki o pamięć, a nawet pójdzie na CPU.

### 2.2 Pobierz

```bash
mkdir -p ~/models/embed
cd ~/models/embed

# GGUF bge-m3 w f16 (embeddingi lubią precyzję). W repo plik nazywa się bge-m3-FP16.gguf -
# wielkość liter ma znaczenie. hf to narzędzie z części 1 ($VENVS/hf).
$VENVS/hf/bin/hf download gpustack/bge-m3-GGUF bge-m3-FP16.gguf --local-dir .
ln -sfn bge-m3-FP16.gguf bge-m3-f16.gguf      # nazwa, której używa $LLMEDU/rig-env.sh ($EMB)

# Suma kontrolna z Hugging Face - musi wypisać "OK"
echo "daec91ffb5dd0c27411bd71f29932917c49cf529a641d0168496c3a501e3062c  bge-m3-FP16.gguf" | sha256sum -c -
ls -la ~/models/embed/
```

💡 **Bez `hf`?** Ten sam plik pobierzesz zwykłym curlem:
`curl -L -o bge-m3-FP16.gguf https://huggingface.co/gpustack/bge-m3-GGUF/resolve/main/bge-m3-FP16.gguf`

⚠️ **Nie kwantyzuj modelu embeddingowego agresywnie.** Wektory to liczby — Q4 psuje
geometrię przestrzeni i podobieństwa przestają być wiarygodne. **`f16` albo `Q8_0`, nigdy
niżej.**

`$LLMEDU/rig-env.sh` ma zmienną `$EMB` od początku kursu — nic nie dopisuj, tylko sprawdź:

```bash
source $LLMEDU/rig-env.sh
grep "EMB=" $LLMEDU/rig-env.sh
ls -laL $EMB      # -L: pokaż plik, na który wskazuje skrót
```

### 2.3 Uruchom jako serwer embeddingów

```bash
pkill -f "llama-server.*--port 8093"; sleep 1

$LB/llama-server -m $EMB \
  --embedding \
  -ngl 999 -c 8192 \
  --host 127.0.0.1 --port 8093 --no-warmup > /tmp/emb-8093.log 2>&1 &
sleep 15

# Test
curl -s http://127.0.0.1:8093/v1/embeddings -H "Content-Type: application/json" \
  -d '{"input":"faktura za usługi księgowe"}' \
| python3 -c 'import json,sys; d=json.load(sys.stdin); v=d["data"][0]["embedding"]; print(f"wymiar={len(v)}  pierwsze 5={[round(x,4) for x in v[:5]]}")'
```

🔧 **`--embedding`** przełącza serwer w tryb embeddingowy (nie generuje tekstu).
**Osobny port 8093** — bo model generatywny będzie na 8081, a 8090 zajmuje na tej maszynie
orkiestrator benchmarków (`agent-server.sh`). Dwa serwery, dwie role.

🔧 **Bez `--pooling`.** Serwer bierze sposób łączenia tokenów zapisany w pliku modelu. Dla
bge-m3 to **CLS** (wektor pierwszego tokenu), bo tak go wytrenowano. `--pooling mean` też
zadziała, ale wyszukiwanie będzie gorsze. Sprawdzisz to w logu:
`grep -m1 pooling /tmp/emb-8093.log`.

⚠️ **Na tej maszynie llama-swap (port 8080) może trzymać duży model na wszystkich kartach**
(DeepSeek zajmuje ~85 % VRAM każdej). Wtedy zwolnij GPU przed startem serwerów kursu:
`curl -s -X POST http://127.0.0.1:8080/api/models/unload`

### 2.4 Porównaj: dedykowany vs generatywny

Model generatywny musi do tego chodzić **w trybie embeddingowym** — serwer generujący tekst
nie zwraca wektorów. Uruchom więc Bielika tymczasowo, na osobnym porcie 8082, z `--pooling mean`
jak w części 2 §7:

```bash
$LB/llama-server -m $BIELIK --embedding --pooling mean -ngl 999 -c 2048 \
  --host 127.0.0.1 --port 8082 --no-warmup > /tmp/bielik-emb-8082.log 2>&1 &
sleep 25

cat > $KURS/porownaj-embed.py <<'PYEOF'
#!/usr/bin/env python3
"""Porownuje jakosc embeddingow: dedykowany bge-m3 (8093) vs generatywny Bielik (8082)."""
import json, math, urllib.request

PARY = [
    ("faktura za usługi księgowe", "rachunek za prowadzenie księgowości", "podobne"),
    ("stawka VAT 23 procent",      "podatek od towarów i usług 23%",      "podobne"),
    ("amortyzacja środka trwałego","odpis amortyzacyjny maszyny",          "podobne"),
    ("faktura za usługi księgowe", "przepis na sernik wiedeński",          "ROZNE"),
    ("bilans na koniec roku",      "rozkład jazdy autobusów",              "ROZNE"),
]

def embed(port, text):
    req = urllib.request.Request(f"http://127.0.0.1:{port}/v1/embeddings",
        data=json.dumps({"input": text}).encode(),
        headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=120))["data"][0]["embedding"]

def cos(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na  = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(y*y for y in b))
    return dot / (na*nb) if na and nb else 0.0

for port, nazwa in ((8093, "bge-m3 (dedykowany)"), (8082, "Bielik (generatywny)")):
    print(f"\n=== {nazwa} ===")
    podobne, rozne = [], []
    for a, b, typ in PARY:
        try:
            s = cos(embed(port, a), embed(port, b))
        except Exception as e:
            print(f"  (serwer {port} niedostepny: {e})"); break
        (podobne if typ == "podobne" else rozne).append(s)
        print(f"  {s:.4f}  [{typ:8s}]  {a[:32]!r} <-> {b[:32]!r}")
    if podobne and rozne:
        margines = min(podobne) - max(rozne)
        print(f"  --> MARGINES (min_podobne - max_rozne) = {margines:+.4f}  "
              f"{'✅ dobry rozdzial' if margines > 0.1 else '❌ slaby rozdzial'}")
PYEOF

python3 $KURS/porownaj-embed.py

pkill -f "llama-server.*--port 8082"     # Bielik-embedding już niepotrzebny
```

⭐ **Patrz na MARGINES, nie na same liczby.** Dobry model embeddingowy daje **wyraźną
przerwę** między parami podobnymi i różnymi. Model generatywny da wszystkim ~0,9 (na tej maszynie 0,87–0,95)
i nic nie rozdzieli. **To jest liczba, którą mierzysz, wybierając model embeddingowy.**

---

## 3. Chunking — najważniejsza decyzja w całym RAG-u

⭐ **Tu wygrywa się i przegrywa RAG.** Nie w wyborze modelu.

### 3.1 Dlaczego nie da się „po prostu podzielić na 500 znaków"

```
Dokument:  "...Stawka VAT wynosi 23%. | Zwolnienie stosuje się do usług
            ─────────────────────────┴─ granica fragmentu
            medycznych i edukacyjnych..."
```

Pytanie *„jakie usługi są zwolnione z VAT?"* trafi we fragment 2, który **nie zawiera słowa
VAT**. Wyszukiwarka go nie znajdzie. Odpowiedź: „nie mam informacji".

### 3.2 Trzy strategie i kiedy której używać

| Strategia | Jak | Do czego |
| :-- | :-- | :-- |
| **stały rozmiar + zakładka** | 800 znaków, 200 znaków nachodzenia | ⭐ domyślna, zawsze działa |
| **po strukturze** | dziel na akapitach / nagłówkach / paragrafach ustawy | dokumenty z wyraźną strukturą |
| **zdanie + okno** | grupuj po N zdań, nie łam zdania | tekst ciągły, umowy |

💡 **Zakładka (overlap) to najtańszy sposób na naprawienie 80 % problemów.**
Kosztuje ~25 % więcej miejsca w bazie i rozwiązuje problem przeciętych zdań.

### 3.3 Implementacja

```bash
cat > $KURS/chunk.py <<'PYEOF'
#!/usr/bin/env python3
"""Trzy strategie chunkingu. Czysty Python, bez zaleznosci."""
import re

def chunk_staly(tekst: str, rozmiar: int = 800, zakladka: int = 200) -> list[str]:
    """Staly rozmiar z nachodzeniem. Nie lamie w srodku slowa."""
    if zakladka >= rozmiar:
        raise ValueError("zakladka musi byc mniejsza niz rozmiar")
    out, i = [], 0
    while i < len(tekst):
        koniec = min(i + rozmiar, len(tekst))
        # cofnij sie do granicy slowa, jesli to nie koniec tekstu
        if koniec < len(tekst):
            sp = tekst.rfind(" ", i + rozmiar // 2, koniec)
            if sp > i:
                koniec = sp
        frag = tekst[i:koniec].strip()
        if frag:
            out.append(frag)
        if koniec >= len(tekst):
            break
        i = koniec - zakladka
        # poczatek nastepnego fragmentu tez na granicy slowa
        sp = tekst.find(" ", i, koniec)
        if sp != -1:
            i = sp + 1
    return out

def chunk_akapity(tekst: str, max_znakow: int = 1200) -> list[str]:
    """Po akapitach; zbyt dlugie akapity dzieli dalej po stalym rozmiarze."""
    out = []
    for ak in re.split(r"\n\s*\n", tekst):
        ak = ak.strip()
        if not ak:
            continue
        out.extend([ak] if len(ak) <= max_znakow else chunk_staly(ak, max_znakow, 150))
    return out

def chunk_zdania(tekst: str, zdan_na_frag: int = 5, zakladka_zdan: int = 1) -> list[str]:
    """Grupuje po N zdan z nachodzeniem. Nigdy nie lamie zdania."""
    zdania = [z.strip() for z in re.split(r"(?<=[.!?])\s+", tekst) if z.strip()]
    out, i = [], 0
    krok = max(1, zdan_na_frag - zakladka_zdan)
    while i < len(zdania):
        out.append(" ".join(zdania[i:i + zdan_na_frag]))
        if i + zdan_na_frag >= len(zdania):
            break
        i += krok
    return out

if __name__ == "__main__":
    PROBKA = """Ustawa o rachunkowości określa zasady prowadzenia księgi rachunkowej.
Jednostki gospodarcze mają obowiązek prowadzenia ksiąg w języku polskim.

Sprawozdanie finansowe składa się z bilansu oraz rachunku zysków i strat. Dodatkowo
wymagana jest informacja dodatkowa. Sprawozdanie zatwierdza organ zatwierdzający.

Stawka VAT wynosi 23 procent dla większości towarów i usług. Zwolnienie stosuje się
do usług medycznych i edukacyjnych. Stawka obniżona 5 procent dotyczy książek."""

    for nazwa, fn in (("staly 200/80", lambda t: chunk_staly(t, 200, 80)),
                      ("akapity",      chunk_akapity),
                      ("zdania 3/1",   lambda t: chunk_zdania(t, 3, 1))):
        frag = fn(PROBKA)
        print(f"\n=== {nazwa}: {len(frag)} fragmentow")
        for i, f in enumerate(frag):
            znak = "   <- zwolnienie z VAT" if "Zwolnienie" in f else ""
            print(f"  [{i}] ({len(f):4d} zn) {f[:60]!r}...{znak}")
PYEOF

python3 $KURS/chunk.py
```

**Przyjrzyj się wyjściu.** Zobacz, jak w wariancie „staly 200/80" zdanie o zwolnieniu z VAT
**pojawia się w dwóch fragmentach** (znacznik `<- zwolnienie z VAT`) — dzięki zakładce. To jest
dokładnie to, o co chodzi. Zwróć też uwagę, że żaden fragment nie zaczyna się ani nie kończy
w środku słowa.

### 3.4 ⚠️ Pułapka P29 (nowa): metadane fragmentu są ważniejsze niż sam fragment

Fragment bez kontekstu jest bezużyteczny w odpowiedzi. **Zawsze przechowuj razem z nim:**

```python
{
  "tekst":      "Stawka VAT wynosi 23 procent...",
  "zrodlo":     "ustawa-vat.pdf",      # <-- do cytowania (§7)
  "strona":     14,                     # <-- zeby czlowiek mogl sprawdzic
  "naglowek":   "Art. 41. Stawki",      # <-- kontekst dla modelu
  "pozycja":    3,                      # <-- kolejnosc w dokumencie
}
```

💡 **Wstrzykuj nagłówek na początek tekstu fragmentu przed embedowaniem.** Fragment
„Zwolnienie stosuje się do usług medycznych" embedowany jako
`"Art. 43. Zwolnienia | Zwolnienie stosuje się do usług medycznych"` jest **znacznie
łatwiejszy do znalezienia**. To jedna linia kodu i duża poprawa trafności.

---

## 4. Baza wektorowa w sqlite — od zera

Nie potrzebujesz Qdranta ani Chromy. Przy dziesiątkach tysięcy fragmentów **sqlite +
przeszukanie liniowe w Pythonie jest wystarczające** i całkowicie zrozumiałe.

```bash
cat > $KURS/baza.py <<'PYEOF'
#!/usr/bin/env python3
"""Baza wektorowa w sqlite. Czysty Python, bez numpy, bez sqlite-vec.

Wektory trzymamy jako BLOB (struct.pack), szukamy liniowo w Pythonie.
Przy <100k fragmentow to w pelni wystarcza i jest zrozumiale w calosci.
"""
import json, math, os, sqlite3, struct, sys, urllib.request

DB     = os.path.join(os.environ["KURS"], "wiedza.db")
EMB_URL = "http://127.0.0.1:8093/v1/embeddings"

# ---------- embeddingi ----------------------------------------------------
def embed(text: str) -> list[float]:
    req = urllib.request.Request(EMB_URL,
        data=json.dumps({"input": text}).encode(),
        headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=300))["data"][0]["embedding"]

def embed_wiele(teksty: list[str]) -> list[list[float]]:
    """Wsadowo - znacznie szybciej niz po jednym."""
    req = urllib.request.Request(EMB_URL,
        data=json.dumps({"input": teksty}).encode(),
        headers={"Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=900))
    return [e["embedding"] for e in sorted(d["data"], key=lambda x: x["index"])]

# ---------- serializacja --------------------------------------------------
def pak(v: list[float]) -> bytes:
    return struct.pack(f"{len(v)}f", *v)

def odpak(b: bytes) -> list[float]:
    return list(struct.unpack(f"{len(b)//4}f", b))

def znormalizuj(v: list[float]) -> list[float]:
    """Normalizacja do dlugosci 1. Wtedy cosinus == iloczyn skalarny (szybciej)."""
    n = math.sqrt(sum(x*x for x in v))
    return [x/n for x in v] if n else v

# ---------- schemat -------------------------------------------------------
def init(con):
    con.executescript("""
    CREATE TABLE IF NOT EXISTS fragmenty (
        id       INTEGER PRIMARY KEY,
        tekst    TEXT NOT NULL,
        zrodlo   TEXT NOT NULL,
        naglowek TEXT,
        pozycja  INTEGER,
        wektor   BLOB NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_zrodlo ON fragmenty(zrodlo);

    -- FTS5 dla wyszukiwania slowo-w-slowo (§5). Indeksuje naglowek + tekst,
    -- tak samo jak embedding (P29), wiec "Art. 43" znajdzie tresc artykulu.
    CREATE VIRTUAL TABLE IF NOT EXISTS fts USING fts5(tekst, tokenize='unicode61');
    """)
    con.commit()

# ---------- dodawanie -----------------------------------------------------
def dodaj(con, fragmenty: list[dict], wsad: int = 16):
    """fragmenty: [{tekst, zrodlo, naglowek?, pozycja?}, ...]"""
    for i in range(0, len(fragmenty), wsad):
        grupa = fragmenty[i:i+wsad]
        # Naglowek doklejamy PRZED embedowaniem - patrz P29
        do_embed = [((f.get("naglowek") or "") + " | " + f["tekst"]).strip(" |")
                    for f in grupa]
        wektory = embed_wiele(do_embed)
        for f, w, szukany in zip(grupa, wektory, do_embed):
            cur = con.execute(
                "INSERT INTO fragmenty(tekst,zrodlo,naglowek,pozycja,wektor) VALUES(?,?,?,?,?)",
                (f["tekst"], f["zrodlo"], f.get("naglowek"), f.get("pozycja"),
                 pak(znormalizuj(w))))
            con.execute("INSERT INTO fts(rowid, tekst) VALUES(?,?)",
                        (cur.lastrowid, szukany))
        con.commit()
        print(f"  dodano {min(i+wsad, len(fragmenty))}/{len(fragmenty)}", file=sys.stderr)

# ---------- szukanie wektorowe -------------------------------------------
def szukaj_wektorowo(con, pytanie: str, k: int = 5) -> list[dict]:
    q = znormalizuj(embed(pytanie))
    wyniki = []
    for rid, tekst, zrodlo, nagl, poz, blob in con.execute(
            "SELECT id,tekst,zrodlo,naglowek,pozycja,wektor FROM fragmenty"):
        v = odpak(blob)
        # oba znormalizowane => cosinus = iloczyn skalarny
        s = sum(a*b for a, b in zip(q, v))
        wyniki.append({"id": rid, "tekst": tekst, "zrodlo": zrodlo,
                       "naglowek": nagl, "pozycja": poz, "score": s})
    wyniki.sort(key=lambda x: x["score"], reverse=True)
    return wyniki[:k]

# ---------- szukanie slowne (BM25 z FTS5) --------------------------------
def szukaj_slownie(con, pytanie: str, k: int = 5) -> list[dict]:
    import re
    # UWAGA: `len(w) > 2` samo w sobie odrzucaloby "43" (len=2) i "5" (len=1) -
    # a to numery artykulow i stawek, czyli DOKLADNIE to, po co jest ta funkcja
    # (P30: wektory sa slepe na identyfikatory). Liczby przechodza zawsze.
    slowa = [w for w in re.findall(r"\w+", pytanie, flags=re.UNICODE)
             if len(w) > 2 or w.isdigit()]
    if not slowa:
        return []
    zapyt = " OR ".join(slowa)
    out = []
    try:
        for rid, rank in con.execute(
                "SELECT rowid, bm25(fts) FROM fts "
                "WHERE fts MATCH ? ORDER BY bm25(fts) LIMIT ?", (zapyt, k)):
            tekst, zrodlo, nagl, poz = con.execute(
                "SELECT tekst,zrodlo,naglowek,pozycja FROM fragmenty WHERE id=?", (rid,)).fetchone()
            out.append({"id": rid, "tekst": tekst, "zrodlo": zrodlo,
                        "naglowek": nagl, "pozycja": poz,
                        "score": -rank})   # bm25 zwraca ujemne: mniej = lepiej
    except sqlite3.OperationalError as e:
        print(f"  (FTS blad: {e})", file=sys.stderr)
    return out

if __name__ == "__main__":
    con = sqlite3.connect(DB); init(con)
    n = con.execute("SELECT COUNT(*) FROM fragmenty").fetchone()[0]
    print(f"Baza: {DB}\nFragmentow: {n}")
    if len(sys.argv) > 1:
        print(f"\nSzukam: {sys.argv[1]!r}\n")
        for r in szukaj_wektorowo(con, sys.argv[1], 5):
            print(f"  {r['score']:.4f}  [{r['zrodlo']}]  {r['tekst'][:80]!r}")
PYEOF
```

### 4.1 Napełnij bazę

```bash
cat > $KURS/indeksuj.py <<'PYEOF'
#!/usr/bin/env python3
"""Indeksuje pliki .txt/.md z katalogu do bazy wektorowej.

Uzycie:  python3 indeksuj.py $KURS/dokumenty
"""
import os, sqlite3, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from baza import DB, init, dodaj
from chunk import chunk_akapity

def main(katalog):
    con = sqlite3.connect(DB); init(con)
    frag = []
    for root, _, pliki in os.walk(os.path.expanduser(os.path.expandvars(katalog))):
        for p in sorted(pliki):
            if not p.endswith((".txt", ".md")):
                continue
            sciezka = os.path.join(root, p)
            tekst = open(sciezka, encoding="utf-8", errors="replace").read()
            naglowek = None
            for i, f in enumerate(chunk_akapity(tekst, 1000)):
                # Naglowek markdown to metadane kolejnych fragmentow (P29), nie osobny fragment
                if f.startswith("#"):
                    pierwsza, _, reszta = f.partition("\n")
                    naglowek = pierwsza.lstrip("# ")[:120]
                    f = reszta.strip()
                    if not f:
                        continue
                frag.append({"tekst": f, "zrodlo": p, "naglowek": naglowek, "pozycja": i})
    print(f"Do zaindeksowania: {len(frag)} fragmentow z {katalog}")
    if frag:
        dodaj(con, frag)
    print(f"Gotowe. W bazie: {con.execute('SELECT COUNT(*) FROM fragmenty').fetchone()[0]}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "$KURS/dokumenty")
PYEOF

# Przygotuj dokumenty testowe
mkdir -p $KURS/dokumenty
cat > $KURS/dokumenty/vat.md <<'EOF'
# Art. 41. Stawki podatku

Stawka podatku VAT wynosi 23 procent dla większości towarów i usług.

Stawka obniżona 8 procent stosuje się do usług budowlanych związanych
z budownictwem objętym społecznym programem mieszkaniowym, a także do
niektórych usług gastronomicznych.

Stawka obniżona 5 procent dotyczy książek, czasopism specjalistycznych
oraz podstawowych produktów żywnościowych.

# Art. 43. Zwolnienia

Zwolnione od podatku są usługi w zakresie opieki medycznej, służące
profilaktyce, zachowaniu, ratowaniu i przywracaniu zdrowia.

Zwolnione są również usługi kształcenia i wychowania świadczone przez
jednostki objęte systemem oświaty.
EOF

cat > $KURS/dokumenty/faktury.md <<'EOF'
# Elementy faktury VAT

Faktura powinna zawierać datę wystawienia oraz kolejny numer nadany
w ramach jednej lub więcej serii, który w sposób jednoznaczny identyfikuje
fakturę.

Faktura zawiera imiona i nazwiska lub nazwy podatnika i nabywcy oraz
ich adresy. Wymagany jest numer identyfikacji podatkowej NIP sprzedawcy.

# Faktura korygująca

Fakturę korygującą wystawia się, gdy po wystawieniu faktury udzielono
obniżki ceny, zwrócono towar albo podwyższono cenę lub stwierdzono pomyłkę
w cenie, stawce lub kwocie podatku.

Termin przechowywania faktur wynosi 5 lat licząc od końca roku
kalendarzowego, w którym upłynął termin płatności podatku.
EOF

cat > $KURS/dokumenty/rejestr.md <<'EOF'
# Rejestr faktur zakupowych - wrzesień 2025

FV/2025/09/0141 - Biuro Rachunkowe Kwadrat, usługi księgowe, 1 230,00 zł brutto.

FV/2025/09/0142 - Hurtownia Papieru, materiały biurowe, 456,00 zł brutto.

FV/2025/09/0143 - Chmurex S.A., hosting serwerów, 2 460,00 zł brutto.

FV/2025/09/0144 - Kancelaria Lex, porada prawna, 984,00 zł brutto.
EOF

# Indeksuj
cd $KURS && python3 indeksuj.py $KURS/dokumenty
```

### 4.2 Szukaj

```bash
cd $KURS
python3 baza.py "jaka stawka VAT na książki"
echo "---"
python3 baza.py "ile lat trzymać faktury"
echo "---"
python3 baza.py "czy usługi lekarskie są opodatkowane"
```

Trzecie pytanie jest ciekawe: **nie zawiera słowa „zwolnienie" ani „medyczna"**, a wektory
powinny i tak trafić w Art. 43. **To jest przewaga wektorów nad wyszukiwaniem słownym.**

---

## 5. BM25 — dlaczego same wektory nie wystarczą

```bash
cd $KURS
python3 - <<'PYEOF'
import sqlite3, sys, os
sys.path.insert(0, os.environ["KURS"])
from baza import DB, szukaj_wektorowo, szukaj_slownie

con = sqlite3.connect(DB)
for q in ["czy usługi lekarskie są opodatkowane", "Art. 43", "FV/2025/09/0143"]:
    print(f"\n=== {q!r}")
    print("  WEKTOROWO:")
    for r in szukaj_wektorowo(con, q, 3):
        print(f"    {r['score']:.3f}  {r['tekst'][:65]!r}")
    print("  SLOWNIE (BM25):")
    for r in szukaj_slownie(con, q, 3):
        print(f"    {r['score']:.3f}  {r['tekst'][:65]!r}")
PYEOF
```

⭐ **Zobacz, gdzie każda metoda wygrywa:**

| Zapytanie | Wektory | BM25 |
| :-- | :-- | :-- |
| „czy usługi lekarskie są opodatkowane" | ✅ rozumie synonim: właściwy fragment na 1. miejscu | ❌ łapie samo słowo „usługi": właściwy fragment dopiero 3. |
| „Art. 43" | ✅ tylko dlatego, że nagłówek jest doklejony do fragmentu (P29) | ✅ trafia dokładnie |
| „FV/2025/09/0143" | ❌ **właściwa faktura dopiero 3.** — 0141–0144 są dla wektorów „takie same" | ✅ trafia idealnie |

⚠️ **Pułapka P30 (nowa): wektory są bezużyteczne dla identyfikatorów.**
Numery faktur, NIP-y, symbole, kody — embedding nie ma pojęcia, że `FV/2025/0143`
to inna faktura niż `FV/2025/0144`. **Dla danych księgowych wyszukiwanie słowne jest
NIEZBĘDNE, nie opcjonalne.**

---

## 6. Wyszukiwanie hybrydowe i reranking

### 6.1 Fuzja rangowa (RRF) — łączy oba rankingi

```bash
cat > $KURS/hybryda.py <<'PYEOF'
#!/usr/bin/env python3
"""Wyszukiwanie hybrydowe: wektory + BM25, polaczone przez RRF.

RRF (Reciprocal Rank Fusion): score = suma po listach z 1/(k + pozycja).
Zaleta: nie trzeba normalizowac roznych skal score'ow - liczy sie tylko KOLEJNOSC.
"""
import os, sqlite3, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from baza import DB, szukaj_wektorowo, szukaj_slownie

def rrf(listy: list[list[dict]], k: int = 60, limit: int = 5) -> list[dict]:
    punkty, obiekty = {}, {}
    for lista in listy:
        for poz, r in enumerate(lista):
            punkty[r["id"]] = punkty.get(r["id"], 0.0) + 1.0 / (k + poz + 1)
            obiekty[r["id"]] = r
    naj = sorted(punkty.items(), key=lambda x: x[1], reverse=True)[:limit]
    out = []
    for rid, p in naj:
        r = dict(obiekty[rid]); r["rrf"] = p
        out.append(r)
    return out

def szukaj_hybrydowo(con, pytanie: str, limit: int = 5) -> list[dict]:
    w = szukaj_wektorowo(con, pytanie, limit * 3)
    s = szukaj_slownie(con, pytanie, limit * 3)
    return rrf([w, s], limit=limit)

if __name__ == "__main__":
    con = sqlite3.connect(DB)
    q = sys.argv[1] if len(sys.argv) > 1 else "stawka VAT na książki"
    print(f"Pytanie: {q!r}\n")
    for i, r in enumerate(szukaj_hybrydowo(con, q), 1):
        print(f"{i}. rrf={r['rrf']:.4f}  [{r['zrodlo']}]")
        print(f"   {r['tekst'][:100]!r}\n")
PYEOF

cd $KURS
python3 hybryda.py "Art. 43 zwolnienia medyczne"
python3 hybryda.py "ile procent podatku na książki"
```

💡 **Dlaczego RRF, a nie ważona suma score'ów.** Cosinus daje 0–1, BM25 daje dowolne
liczby. Normalizowanie ich do wspólnej skali jest arbitralne i kruche. **RRF patrzy tylko
na kolejność** — działa bez kalibracji i jest odporny na zmianę modelu embeddingowego.

### 6.2 Reranking — model jako sędzia trafności

Wyszukiwarka daje 20 kandydatów. Model ocenia każdego i zostawiasz 5 najlepszych.
**Wolniejsze, ale wyraźnie trafniejsze.**

Od tego miejsca potrzebny jest **model generatywny na porcie 8081**. Uruchom Bielika — serwer
embeddingów na 8093 zostaje włączony. **Nie używaj tu `pkill -f llama-server`** z poprzednich
części: zabiłoby oba serwery.

```bash
pkill -f "llama-server.*--port 8081"; sleep 2
$LB/llama-server -m $BIELIK -ngl 999 -c 8192 --port 8081 --host 127.0.0.1 --no-warmup \
  > /tmp/bielik-8081.log 2>&1 &
sleep 25
```

```bash
cat > $KURS/rerank.py <<'PYEOF'
#!/usr/bin/env python3
"""Reranking: model ocenia trafnosc kazdego kandydata w skali 0-10.

Wymuszony gramatyka (czesc 3) - model NIE MOZE zwrocic czegos innego niz liczba.
Przez endpoint czatu, zeby model dostal swoj szablon (czesc 3).
"""
import json, os, sqlite3, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from baza import DB
from hybryda import szukaj_hybrydowo

LLM = "http://127.0.0.1:8081"
GRAMATYKA = 'root ::= [0-9] | "10"'
SEDZIA = ("Oceniasz trafność fragmentu dokumentu względem pytania. Odpowiadasz jedną liczbą "
          "od 0 do 10: 0 = fragment nie ma związku z pytaniem, 5 = częściowo pomaga, "
          "10 = zawiera pełną odpowiedź.")

def ocen(pytanie: str, fragment: str) -> int:
    # Endpoint czatu, nie /v1/completions: model instrukcyjny bez swojego szablonu czatu
    # ocenia "na slepo" (wychodzilo 10 dla kazdego fragmentu).
    body = {"messages": [{"role": "system", "content": SEDZIA},
                         {"role": "user", "content": f"Pytanie: {pytanie}\n\n"
                                                     f"Fragment: {fragment[:900]}\n\nOcena (0-10):"}],
            "max_tokens": 4, "temperature": 0, "grammar": GRAMATYKA}
    req = urllib.request.Request(LLM + "/v1/chat/completions",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    try:
        return int(json.load(urllib.request.urlopen(req, timeout=180))["choices"][0]["message"]["content"].strip())
    except Exception:
        return 0

def szukaj_z_rerankiem(con, pytanie: str, kandydatow: int = 12, limit: int = 4):
    kand = szukaj_hybrydowo(con, pytanie, kandydatow)
    for r in kand:
        r["ocena"] = ocen(pytanie, r["tekst"])
    kand.sort(key=lambda x: x["ocena"], reverse=True)
    return [r for r in kand if r["ocena"] >= 4][:limit]

if __name__ == "__main__":
    con = sqlite3.connect(DB)
    q = sys.argv[1] if len(sys.argv) > 1 else "czy lekarz płaci VAT"
    print(f"Pytanie: {q!r}\n")
    print("PRZED rerankingiem (kolejnosc hybrydowa):")
    for i, r in enumerate(szukaj_hybrydowo(con, q, 6), 1):
        print(f"  {i}. {r['tekst'][:70]!r}")
    print("\nPO rerankingu:")
    for i, r in enumerate(szukaj_z_rerankiem(con, q), 1):
        print(f"  {i}. ocena={r['ocena']:2d}  {r['tekst'][:70]!r}")
PYEOF

cd $KURS && python3 rerank.py "czy lekarz płaci VAT"
```

⚠️ **Reranking kosztuje jeden forward pass na kandydata.** 12 kandydatów = 12 wywołań
modelu. Przy `max_tokens: 4` to jest tani prefill (część 2 §5), ale nie darmowy.
**Używaj, gdy trafność ma znaczenie; pomijaj, gdy liczy się czas odpowiedzi.**

---

## 7. Cytowania i uziemienie

⭐ **To jest rozdział, który decyduje, czy Twój produkt księgowy da się sprzedać.**
Odpowiedź bez możliwości sprawdzenia źródła jest w księgowości bezwartościowa.

### 7.1 Prompt, który wymusza uziemienie

```bash
cat > $KURS/odpowiedz.py <<'PYEOF'
#!/usr/bin/env python3
"""RAG z wymuszonymi cytowaniami i weryfikacja w kodzie."""
import json, os, re, sqlite3, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from baza import DB
from hybryda import szukaj_hybrydowo

LLM = "http://127.0.0.1:8081"

SYSTEM = """Odpowiadasz WYŁĄCZNIE na podstawie podanych fragmentów.

ZASADY:
1. Każde twierdzenie musi mieć odnośnik [n] do numeru fragmentu.
2. Jeśli fragmenty nie zawierają odpowiedzi — napisz dokładnie:
   "Nie znalazłem tej informacji w dostępnych dokumentach."
3. Nie korzystaj z wiedzy spoza fragmentów. Nie domyślaj się.
4. Nie podawaj odnośnika do fragmentu, którego nie użyłeś."""

def zbuduj_kontekst(fragmenty: list[dict]) -> str:
    czesci = []
    for i, f in enumerate(fragmenty, 1):
        nagl = f" ({f['naglowek']})" if f.get("naglowek") else ""
        czesci.append(f"[{i}] źródło: {f['zrodlo']}{nagl}\n{f['tekst']}")
    return "\n\n".join(czesci)

def odpowiedz(con, pytanie: str, k: int = 4):
    frag = szukaj_hybrydowo(con, pytanie, k)
    if not frag:
        return "Nie znalazłem tej informacji w dostępnych dokumentach.", [], []

    body = {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"FRAGMENTY:\n{zbuduj_kontekst(frag)}\n\nPYTANIE: {pytanie}"},
        ],
        "max_tokens": 500, "temperature": 0.2, "min_p": 0.05,
    }
    req = urllib.request.Request(LLM + "/v1/chat/completions",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    tekst = json.load(urllib.request.urlopen(req, timeout=300))["choices"][0]["message"]["content"]

    # --- WERYFIKACJA: czy cytowania istnieja? -------------------------
    uzyte = sorted({int(n) for n in re.findall(r"\[(\d+)\]", tekst)})
    zmyslone = [n for n in uzyte if n < 1 or n > len(frag)]
    return tekst, frag, zmyslone

if __name__ == "__main__":
    con = sqlite3.connect(DB)
    q = sys.argv[1] if len(sys.argv) > 1 else "Jaka jest stawka VAT na książki?"
    tekst, frag, zmyslone = odpowiedz(con, q)

    print(f"PYTANIE: {q}\n")
    print(f"ODPOWIEDŹ:\n{tekst}\n")
    print("ŹRÓDŁA:")
    for i, f in enumerate(frag, 1):
        print(f"  [{i}] {f['zrodlo']}" + (f" — {f['naglowek']}" if f.get('naglowek') else ""))
    if zmyslone:
        print(f"\n⚠️  MODEL ZMYŚLIŁ ODNOŚNIKI: {zmyslone} — ODRZUĆ TĘ ODPOWIEDŹ")
    else:
        print("\n✅ wszystkie odnośniki istnieją")
PYEOF

cd $KURS
python3 odpowiedz.py "Jaka jest stawka VAT na książki?"
echo "======================================"
python3 odpowiedz.py "Ile wynosi składka ZUS dla przedsiębiorcy?"
```

⭐ **Drugie pytanie to test najważniejszy w całym rozdziale.** Odpowiedzi **nie ma**
w dokumentach. Model **musi** powiedzieć „nie znalazłem". Jeśli zamiast tego coś wymyśli —
Twój prompt jest za słaby i nie wolno Ci iść dalej.

### 7.2 Weryfikacja odnośników w kodzie

Zwróć uwagę na `zmyslone` w skrypcie. **Model może podać `[7]`, gdy dałeś mu 4 fragmenty.**
Kod to wyłapuje i odrzuca odpowiedź. To jest tanie i konieczne.

### 7.3 Silniejsza weryfikacja — czy twierdzenie naprawdę jest we fragmencie

```bash
cat >> $KURS/odpowiedz.py <<'PYEOF'

# ---------- dodatkowa weryfikacja: uziemienie zdan ----------------------
def sprawdz_uziemienie(zdanie: str, fragment: str) -> bool:
    """Pyta model, czy zdanie WYNIKA z fragmentu. Gramatyka wymusza tak/nie."""
    req = urllib.request.Request(LLM + "/v1/chat/completions",
        data=json.dumps({
            "messages": [
                {"role": "system", "content": "Sprawdzasz, czy zdanie wynika z fragmentu. "
                                              "Odpowiadasz tylko: tak albo nie."},
                {"role": "user", "content": f"Fragment: {fragment[:800]}\n\nZdanie: {zdanie}\n\n"
                                            "Czy to zdanie wynika WYŁĄCZNIE z fragmentu?"}],
            "max_tokens": 4, "temperature": 0,
            "grammar": 'root ::= "tak" | "nie"',
        }).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=180))["choices"][0]["message"]["content"].strip() == "tak"
PYEOF

# Sprawdz: pierwsze zdanie wynika z fragmentu, drugie nie
cd $KURS && python3 -c "
from odpowiedz import sprawdz_uziemienie as s
f = 'Stawka obniżona 5 procent dotyczy książek i czasopism specjalistycznych.'
print('5 procent na książki :', s('Stawka VAT na książki wynosi 5 procent.', f))
print('23 procent na książki:', s('Stawka VAT na książki wynosi 23 procent.', f))
"
```

Oczekiwany wynik: `True`, potem `False`.

💡 **Kiedy tego użyć:** dla odpowiedzi, które idą do klienta bez przeglądu człowieka.
Kosztuje jedno wywołanie na zdanie. **Dla produktu księgowego to jest opłacalne.**

---

## 8. Inżynieria kontekstu — budżet i kompakcja

⭐ **Ta sekcja jest fundamentem części 6.** Agent bez zarządzania kontekstem przewraca się
po kilkunastu turach.

### 8.1 Budżet kontekstu — twarda arytmetyka

```bash
cat > $KURS/budzet.py <<'PYEOF'
#!/usr/bin/env python3
"""Budzet kontekstu. Liczy tokeny TYM tokenizerem, ktorego uzywa model (P20)."""
import os, subprocess

LB = os.path.expanduser("~/llama.cpp/build/bin")

class Budzet:
    def __init__(self, model_sciezka: str, n_ctx: int, rezerwa_wyjscia: int = 1024):
        self.model = os.path.expanduser(os.path.expandvars(model_sciezka))
        self.n_ctx = n_ctx
        self.rezerwa = rezerwa_wyjscia
        self._cache: dict[str, int] = {}

    def tokeny(self, tekst: str) -> int:
        """Liczy tokeny. Cache, bo llama-tokenize to proces."""
        if tekst in self._cache:
            return self._cache[tekst]
        out = subprocess.run([f"{LB}/llama-tokenize", "-m", self.model, "--stdin"],
                             input=tekst, capture_output=True, text=True, timeout=120)
        n = sum(1 for l in out.stdout.splitlines() if "->" in l or l.strip().startswith(("["))) \
            or len(out.stdout.splitlines())
        if len(self._cache) < 4096:
            self._cache[tekst] = n
        return n

    def dostepne(self, uzyte: int) -> int:
        return max(0, self.n_ctx - self.rezerwa - uzyte)

    def wtloczfragmenty(self, fragmenty: list[dict], limit_tokenow: int) -> list[dict]:
        """Pakuje fragmenty do limitu. NAJTRAFNIEJSZY NA KONIEC (czesc 2 §6.2)."""
        wybrane, suma = [], 0
        for f in fragmenty:                       # kolejnosc: od najtrafniejszego
            n = self.tokeny(f["tekst"])
            if suma + n > limit_tokenow:
                break
            wybrane.append(f); suma += n
        wybrane.reverse()                          # najtrafniejszy ostatni = blizej pytania
        return wybrane

if __name__ == "__main__":
    b = Budzet("~/models/bielik-11b/Bielik-11B-v3.0-Instruct.Q8_0.gguf", n_ctx=8192)
    SYS = "Odpowiadasz wyłącznie na podstawie fragmentów. Każde twierdzenie z odnośnikiem."
    PYT = "Jaka jest stawka VAT na książki i czasopisma specjalistyczne?"
    n_sys, n_pyt = b.tokeny(SYS), b.tokeny(PYT)
    print(f"n_ctx            = {b.n_ctx}")
    print(f"rezerwa wyjscia  = {b.rezerwa}")
    print(f"prompt systemowy = {n_sys}")
    print(f"pytanie          = {n_pyt}")
    print(f"--> na fragmenty = {b.dostepne(n_sys + n_pyt)} tokenow")
PYEOF

cd $KURS && python3 budzet.py
```

⭐ **Zwróć uwagę na `wybrane.reverse()`.** To jest bezpośrednie zastosowanie odkrycia
z części 2 §6.2 („zagubiony w środku"): **najtrafniejszy fragment ma stać najbliżej
pytania**, czyli na końcu listy. Jedna linia, mierzalna poprawa trafności.

### 8.2 Kompakcja — gdy rozmowa nie mieści się w kontekście

To jest mechanizm, którego agent w części 6 **musi** mieć.

```bash
cat > $KURS/kompakcja.py <<'PYEOF'
#!/usr/bin/env python3
"""Kompakcja historii rozmowy: streszcz stare tury, zachowaj swieze doslownie."""
import json, urllib.request

LLM = "http://127.0.0.1:8081"

SYSTEM_STRESZCZ = """Streszczasz historię pracy agenta. Zachowaj ZWIĘŹLE:
- jakie było zadanie
- co już ustalono (fakty, liczby, nazwy plików)
- co już próbowano i z jakim skutkiem
- co pozostało do zrobienia

Pomiń: uprzejmości, powtórzenia, pełne treści plików. Maksymalnie 300 słów."""

def streszcz(tury: list[dict]) -> str:
    tekst = "\n".join(f"{t['role']}: {t['content'][:1500]}" for t in tury)
    req = urllib.request.Request(LLM + "/v1/chat/completions",
        data=json.dumps({
            "messages": [{"role": "system", "content": SYSTEM_STRESZCZ},
                         {"role": "user", "content": tekst}],
            "max_tokens": 600, "temperature": 0.2,
        }).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=300))["choices"][0]["message"]["content"]

def skompaktuj(messages: list[dict], zostaw_swiezych: int = 6) -> list[dict]:
    """[system] + [streszczenie starych] + [N ostatnich doslownie]"""
    if len(messages) <= zostaw_swiezych + 1:
        return messages
    system = messages[0]
    stare  = messages[1:-zostaw_swiezych]
    swieze = messages[-zostaw_swiezych:]
    if not stare:
        return messages
    s = streszcz(stare)
    return [system,
            {"role": "user", "content": f"[STRESZCZENIE POPRZEDNICH {len(stare)} TUR]\n{s}"},
            *swieze]

if __name__ == "__main__":
    demo = [{"role": "system", "content": "Jesteś agentem księgowym."}]
    for i in range(1, 13):
        demo.append({"role": "user",      "content": f"Sprawdź fakturę numer {i}."})
        demo.append({"role": "assistant", "content": f"Faktura {i}: netto {i*100} zł, VAT 23%, brutto {i*123} zł. Zgodna."})
    print(f"PRZED: {len(demo)} wiadomosci")
    po = skompaktuj(demo, zostaw_swiezych=4)
    print(f"PO:    {len(po)} wiadomosci\n")
    for m in po:
        print(f"[{m['role']}] {m['content'][:180]}...")
PYEOF

cd $KURS && python3 kompakcja.py
```

⚠️ **Pułapka P31 (nowa): kompakcja gubi dokładne liczby.**
Streszczenie to model — może zaokrąglić kwotę albo przekręcić numer faktury. **Wszystko, co
musi być dokładne, zapisuj poza kontekstem**: do pliku, do bazy, do struktury w kodzie.
Kontekst to pamięć krótkotrwała, nie system zapisu.

💡 **Wzorzec, który wprowadzimy w części 6:** agent po każdym ważnym ustaleniu zapisuje je
do pliku `USTALENIA.md`. Kompakcja może zgubić szczegół z rozmowy — plik go nie zgubi.

---

## 9. Ewaluacja RAG-u

**Mierzysz dwie rzeczy osobno.** Mieszanie ich to najczęstszy błąd.

| Metryka | Co mierzy | Jak |
| :-- | :-- | :-- |
| **trafność wyszukiwania** (recall@k) | czy właściwy fragment **wszedł** do promptu | oznacz ręcznie, który fragment jest poprawny |
| **poprawność odpowiedzi** | czy model dobrze **wykorzystał** to, co dostał | porównaj z wzorcową odpowiedzią |

💡 **Dlaczego osobno.** Jeśli mierzysz tylko końcową odpowiedź i wynik jest zły — **nie
wiesz, czy winna wyszukiwarka, czy model**. Z dwiema metrykami wiesz od razu, co naprawiać.

```bash
mkdir -p $KURS/eval
cat > $KURS/eval/rag.jsonl <<'EOF'
{"id":"r1","pytanie":"Jaka jest stawka VAT na książki?","zrodlo_ok":"vat.md","musi_zawierac":["5"],"nie_moze":["23 procent dla książek"]}
{"id":"r2","pytanie":"Czy usługi medyczne są zwolnione z VAT?","zrodlo_ok":"vat.md","musi_zawierac":["zwolnion"],"nie_moze":[]}
{"id":"r3","pytanie":"Ile lat przechowuje się faktury?","zrodlo_ok":"faktury.md","musi_zawierac":["5"],"nie_moze":[]}
{"id":"r4","pytanie":"Jaki NIP musi być na fakturze?","zrodlo_ok":"faktury.md","musi_zawierac":["sprzedawc"],"nie_moze":[]}
{"id":"r5","pytanie":"Ile wynosi składka zdrowotna w 2025?","zrodlo_ok":null,"musi_zawierac":["Nie znalazłem"],"nie_moze":["%"]}
EOF

cat > $KURS/eval/rag.py <<'PYEOF'
#!/usr/bin/env python3
"""Ewaluacja RAG: trafnosc wyszukiwania ORAZ poprawnosc odpowiedzi - osobno."""
import json, os, sqlite3, sys
sys.path.insert(0, os.environ["KURS"])
from baza import DB
from hybryda import szukaj_hybrydowo
from odpowiedz import odpowiedz

ZBIOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rag.jsonl")

def main():
    con = sqlite3.connect(DB)
    przyp = [json.loads(l) for l in open(ZBIOR, encoding="utf-8") if l.strip()]
    trafne_szukanie = trafne_odp = 0
    n_ocenianych_szukan = 0

    for p in przyp:
        # --- METRYKA 1: czy wlasciwe zrodlo weszlo do top-k? ---
        frag = szukaj_hybrydowo(con, p["pytanie"], 4)
        zrodla = {f["zrodlo"] for f in frag}
        if p["zrodlo_ok"] is None:
            szuk = "n/d"      # pytanie bez odpowiedzi w bazie
        else:
            n_ocenianych_szukan += 1
            ok = p["zrodlo_ok"] in zrodla
            trafne_szukanie += ok
            szuk = "✅" if ok else "❌"

        # --- METRYKA 2: czy odpowiedz jest poprawna? ---
        tekst, _, zmyslone = odpowiedz(con, p["pytanie"], 4)
        low = tekst.lower()
        ma   = all(s.lower() in low for s in p["musi_zawierac"])
        niema= all(s.lower() not in low for s in p["nie_moze"])
        odp_ok = ma and niema and not zmyslone
        trafne_odp += odp_ok

        print(f"  {p['id']}: szukanie {szuk}  odpowiedz {'✅' if odp_ok else '❌'}")
        if not odp_ok:
            if not ma:     print(f"       brakuje: {[s for s in p['musi_zawierac'] if s.lower() not in low]}")
            if not niema:  print(f"       zakazane: {[s for s in p['nie_moze'] if s.lower() in low]}")
            if zmyslone:   print(f"       zmyslone odnosniki: {zmyslone}")
            print(f"       -> {tekst[:150]!r}")

    n = len(przyp)
    print(f"\n{'='*52}")
    if n_ocenianych_szukan:
        print(f"  recall@4 (wyszukiwanie): {trafne_szukanie}/{n_ocenianych_szukan} = {100*trafne_szukanie/n_ocenianych_szukan:.0f}%")
    print(f"  poprawnosc odpowiedzi:   {trafne_odp}/{n} = {100*trafne_odp/n:.0f}%")
    print("\n  Diagnoza:")
    print("   recall niski, odpowiedzi niskie  -> napraw CHUNKING (§3) i HYBRYDE (§6)")
    print("   recall wysoki, odpowiedzi niskie -> napraw PROMPT (§7) albo wez lepszy model")

if __name__ == "__main__":
    main()
PYEOF

cd $KURS && python3 eval/rag.py
```

⭐ **Przeczytaj diagnozę na końcu.** To jest mapa decyzyjna, która oszczędza dni błądzenia:
wysoki recall + słabe odpowiedzi = problem w modelu/prompcie. Niski recall = problem
w wyszukiwaniu. **Nigdy nie zgaduj, którą stronę naprawiać.**

---

## Ćwiczenie końcowe

1. **Zaindeksuj coś prawdziwego** — skopiuj własne notatki techniczne (`*.md`) do katalogu kursu:
   ```bash
   mkdir -p $KURS/dokumenty/projekt
   cp ~/sciezka/do/twoich/notatek/*.md $KURS/dokumenty/projekt/    # Twoje notatki, dowolne pliki *.md
   cd $KURS && python3 indeksuj.py $KURS/dokumenty/projekt
   ```
2. **Zapytaj o własną maszynę.** Przykładowe pytania — dostosuj je do tego, co naprawdę jest w Twoich notatkach:
   ```bash
   python3 odpowiedz.py "Jaki limit mocy jest ustawiony na kartach?"
   python3 odpowiedz.py "Jaki sterownik i jaka wersja ROCm są zainstalowane?"
   python3 odpowiedz.py "Co zrobić, gdy serwer modelu nie startuje po aktualizacji?"
   ```
   ⭐ **To jest moment, w którym RAG przestaje być ćwiczeniem.** Masz wyszukiwarkę po
   własnej dokumentacji technicznej, działającą offline.

   ⚠️ **Sprawdź pierwszą odpowiedź z dokumentem.** Żywe notatki często zawierają i starą procedurę,
   i nowszą poprawkę tego samego faktu (np. limit mocy, który później podniesiono).
   Jeśli model odpowiada starą wartością, wyszukiwarka podała mu tylko stare fragmenty, a on
   poprawnie je zacytował. To typowa wada RAG-u na żywej dokumentacji: **sprzeczne wersje
   tego samego faktu**. Dobry materiał na ćwiczenia 3–4.
3. **Porównaj trzy strategie chunkingu** na tym samym zbiorze pytań. Zmierz recall@4
   dla każdej. Zapisz wyniki.
4. **Zepsuj to celowo:** zaindeksuj z `chunk_staly(t, 150, 0)` (małe fragmenty, zero
   zakładki) i zmierz ponownie. Zobacz, jak spada recall. **Teraz rozumiesz, dlaczego
   chunking jest ważniejszy niż model.**

---

## Sprawdź się

- [ ] Dlaczego mądrzejszy model nie naprawi złego wyszukiwania?
- [ ] Dlaczego nie wolno kwantyzować modelu embeddingowego do Q4?
- [ ] Dlaczego doklejasz nagłówek do tekstu **przed** embedowaniem?
- [ ] Dlaczego wektory nie znajdą faktury `FV/2025/0143`?
- [ ] Dlaczego RRF jest lepszy od ważonej sumy score'ów?
- [ ] Dlaczego najtrafniejszy fragment ma być **na końcu** promptu?
- [ ] Co robisz, gdy recall jest wysoki, a odpowiedzi złe?
- [ ] Dlaczego kompakcji nie wolno ufać w kwestii dokładnych liczb?

## Nowe pułapki

| ID | Pułapka | § |
| :-- | :-- | :-- |
| **P29** | Fragment bez metadanych i nagłówka — słabo znajdowany, niecytowalny | §3.4 |
| **P30** | Wektory są bezużyteczne dla identyfikatorów (numery, NIP-y) | §5 |
| **P31** | Kompakcja gubi dokładne liczby — ważne fakty zapisuj poza kontekstem | §8.2 |

---

**Następna część: `05-MULTIMODALNOSC.md`** — agent, który widzi obrazy, słyszy Twój głos
i odpowiada na głos. Z listą sprzętu do kupienia.
