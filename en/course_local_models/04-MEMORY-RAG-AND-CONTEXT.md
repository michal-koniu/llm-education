# Part 4 — Memory: RAG and context engineering from scratch

**Level: ⭐⭐⭐⭐** · Requires: parts 2–3 · Time: ~6 h

> **Why this chapter.** The model knows nothing about your documents. Your context is
> finite (part 2 §5.3). The solution is **retrieval + injection** — RAG.
>
> You will write a vector database **from scratch, in pure Python**, with no `numpy`, no
> `langchain`, no `chromadb`. Not because it is better in production — but because afterwards
> you will **understand** what the library does for you and why it sometimes does it badly.

```bash
cd ~/Desktop/github_repos/llm-education   # repository directory (yours may differ)
source rig-env.sh
mkdir -p $KURS      # course working directory (already there if you did part 2)
```

---

## Table of contents

| § | Topic | Key idea |
| :-- | :-- | :-- |
| [1](#1-what-rag-really-is-and-where-it-fails) | **What RAG is** | a search engine with a model at the end, not magic |
| [2](#2-embedding-model--download-the-right-one) | **Embedding model** | a dedicated one beats a generative one 10× |
| [3](#3-chunking--the-most-important-decision-in-all-of-rag) | **Chunking** | ⭐ more important than the choice of model |
| [4](#4-a-vector-database-in-sqlite--from-scratch) | **Vector database** | one file, pure Python |
| [5](#5-bm25--why-vectors-alone-are-not-enough) | **BM25** | vectors lose invoice numbers |
| [6](#6-hybrid-search-and-reranking) | **Hybrid + rerank** | rank fusion, then a model as judge |
| [7](#7-citations-and-grounding) | **Citations** | ⭐ without them an accounting product is worthless |
| [8](#8-context-engineering--budget-and-compaction) | **Context budget** | ⭐ the foundation of part 6 |
| [9](#9-evaluating-rag) | **Evaluation** | two separate metrics, not one |

---

## 1. What RAG really is and where it fails

```
  user question
        │
        ├──► [1] embed the question
        │
        ├──► [2] look for similar fragments in the database   ← this is the SEARCH ENGINE
        │
        ├──► [3] take the K best
        │
        ├──► [4] paste them into the prompt together with the question   ← this is the "augmentation"
        │
        └──► [5] the model answers ONLY on the basis of what was pasted
```

⚠️ **The most important thing about RAG: answer quality is bounded by step [2].**
If the search engine does not find the right fragment, **no model will fix that**.
A smarter model will give you a nicer, more confident-sounding, still wrong answer.

### 1.1 Four ways RAG fails

| Failure | Symptom | Where to fix it |
| :-- | :-- | :-- |
| **fragment not found** | the model says "I have no information" even though it is in the documents | chunking (§3), hybrid (§6) |
| **fragment found, but truncated** | the answer breaks off mid-sentence, context missing | chunking + overlap (§3) |
| **model ignores the context** | it answers from its training memory, not from the document | prompt + citations (§7) |
| **model makes up a citation** | it gives a source that does not exist | verification in code (§7.3) |

💡 **When RAG does not work, in 80% of cases the problem is in the chunking, not in the model.**
Remember that proportion — it will save you weeks.

---

## 2. Embedding model — download the right one

Part 2 §7 used Bielik and showed that it works poorly (trap **P24**). Now we pick
the right tool for the job.

### 2.1 What to choose for Polish

| Model | Size | Dimension | Why |
| :-- | --: | --: | :-- |
| **`bge-m3`** | ~1.2 GB (GGUF f16) | 1024 | ⭐ **recommended** — multilingual, strong Polish, long fragments (8192 tok) |
| `multilingual-e5-large` | ~1.1 GB | 1024 | a good alternative, lighter; requires the `query:`/`passage:` prefixes |
| `paraphrase-multilingual-MiniLM` | ~0.5 GB | 384 | fastest, weakest — for prototypes |

💡 **Why this is good news:** an embedding model is **~20× smaller** than a generative
model. It fits next to it in VRAM without a fight over memory, and it can even run on the CPU.

### 2.2 Download

```bash
mkdir -p ~/models/embed
cd ~/models/embed

# bge-m3 GGUF in f16 (embeddings like precision). In the repo the file is called bge-m3-FP16.gguf -
# letter case matters. hf is the tool from part 1 ($VENVS/hf).
$VENVS/hf/bin/hf download gpustack/bge-m3-GGUF bge-m3-FP16.gguf --local-dir .
ln -sfn bge-m3-FP16.gguf bge-m3-f16.gguf      # the name used by $LLMEDU/rig-env.sh ($EMB)

# Checksum from Hugging Face - must print "OK"
echo "daec91ffb5dd0c27411bd71f29932917c49cf529a641d0168496c3a501e3062c  bge-m3-FP16.gguf" | sha256sum -c -
ls -la ~/models/embed/
```

💡 **No `hf`?** You can fetch the same file with plain curl:
`curl -L -o bge-m3-FP16.gguf https://huggingface.co/gpustack/bge-m3-GGUF/resolve/main/bge-m3-FP16.gguf`

⚠️ **Do not quantize an embedding model aggressively.** Vectors are numbers — Q4 wrecks
the geometry of the space and similarities stop being reliable. **`f16` or `Q8_0`, never
lower.**

`$LLMEDU/rig-env.sh` has had the `$EMB` variable since the start of the course — do not add anything, just check:

```bash
source $LLMEDU/rig-env.sh
grep "EMB=" $LLMEDU/rig-env.sh
ls -laL $EMB      # -L: show the file the shortcut points to
```

### 2.3 Run it as an embedding server

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
| python3 -c 'import json,sys; d=json.load(sys.stdin); v=d["data"][0]["embedding"]; print(f"dimension={len(v)}  first 5={[round(x,4) for x in v[:5]]}")'
```

🔧 **`--embedding`** switches the server into embedding mode (it does not generate text).
**A separate port, 8093** — because the generative model will be on 8081, and 8090 is taken on this machine
by the benchmark orchestrator (`agent-server.sh`). Two servers, two roles.

🔧 **No `--pooling`.** The server takes the token-pooling method stored in the model file. For
bge-m3 that is **CLS** (the vector of the first token), because that is how it was trained. `--pooling mean` would also
work, but search would be worse. You can check it in the log:
`grep -m1 pooling /tmp/emb-8093.log`.

⚠️ **On this machine llama-swap (port 8080) may hold a large model on all the cards**
(DeepSeek takes ~85% of each card's VRAM). In that case free the GPUs before starting the course servers:
`curl -s -X POST http://127.0.0.1:8080/api/models/unload`

### 2.4 Compare: dedicated vs generative

A generative model has to run **in embedding mode** for this — a server that generates text
does not return vectors. So start Bielik temporarily, on a separate port 8082, with `--pooling mean`
as in part 2 §7:

```bash
$LB/llama-server -m $BIELIK --embedding --pooling mean -ngl 999 -c 2048 \
  --host 127.0.0.1 --port 8082 --no-warmup > /tmp/bielik-emb-8082.log 2>&1 &
sleep 25

cat > $KURS/porownaj-embed.py <<'PYEOF'
#!/usr/bin/env python3
"""Compares embedding quality: dedicated bge-m3 (8093) vs generative Bielik (8082)."""
import json, math, urllib.request

PARY = [
    ("faktura za usługi księgowe", "rachunek za prowadzenie księgowości", "podobne"),
    ("stawka VAT 23 procent",      "podatek od towarów i usług 23%",      "podobne"),
    ("amortyzacja środka trwałego","odpis amortyzacyjny maszyny",          "podobne"),
    ("faktura za usługi księgowe", "przepis na sernik wiedeński",          "ROZNE"),
    ("bilans na koniec roku",      "rozkład jazdy autobusów",              "ROZNE"),
]
# ("podobne" = similar pairs, "ROZNE" = different pairs)

def embed(port, text):
    req = urllib.request.Request(f"http://127.0.0.1:{port}/v1/embeddings",
        data=json.dumps({"input": text}).encode(),
        headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=120))["data"][0]["embedding"]

def cos(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na  = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(y*y for y in b))
    return dot / (na*nb) if na and nb else 0.0

for port, nazwa in ((8093, "bge-m3 (dedicated)"), (8082, "Bielik (generative)")):
    print(f"\n=== {nazwa} ===")
    podobne, rozne = [], []
    for a, b, typ in PARY:
        try:
            s = cos(embed(port, a), embed(port, b))
        except Exception as e:
            print(f"  (server {port} unavailable: {e})"); break
        (podobne if typ == "podobne" else rozne).append(s)
        print(f"  {s:.4f}  [{typ:8s}]  {a[:32]!r} <-> {b[:32]!r}")
    if podobne and rozne:
        margines = min(podobne) - max(rozne)
        print(f"  --> MARGIN (min_similar - max_different) = {margines:+.4f}  "
              f"{'✅ good separation' if margines > 0.1 else '❌ poor separation'}")
PYEOF

python3 $KURS/porownaj-embed.py

pkill -f "llama-server.*--port 8082"     # the Bielik embedding server is no longer needed
```

⭐ **Look at the MARGIN, not at the bare numbers.** A good embedding model gives a **clear
gap** between similar and different pairs. A generative model will give everything ~0.9 (on this machine 0.87–0.95)
and separate nothing. **This is the number you measure when choosing an embedding model.**

---

## 3. Chunking — the most important decision in all of RAG

⭐ **This is where RAG is won and lost.** Not in the choice of model.

### 3.1 Why you cannot "just split into 500 characters"

```
Document:  "...Stawka VAT wynosi 23%. | Zwolnienie stosuje się do usług
            ─────────────────────────┴─ fragment boundary
            medycznych i edukacyjnych..."
```

The question *"which services are exempt from VAT?"* (Polish: *„jakie usługi są zwolnione z VAT?"*) will hit fragment 2, which **does not contain the word
VAT**. The search engine will not find it. Answer: "I have no information".

### 3.2 Three strategies and when to use which

| Strategy | How | What for |
| :-- | :-- | :-- |
| **fixed size + overlap** | 800 characters, 200 characters of overlap | ⭐ the default, always works |
| **by structure** | split on paragraphs / headings / sections of a statute | documents with a clear structure |
| **sentence + window** | group by N sentences, never break a sentence | continuous text, contracts |

💡 **Overlap is the cheapest way to fix 80% of problems.**
It costs ~25% more space in the database and solves the problem of cut sentences.

### 3.3 Implementation

```bash
cat > $KURS/chunk.py <<'PYEOF'
#!/usr/bin/env python3
"""Three chunking strategies. Pure Python, no dependencies."""
import re

def chunk_staly(tekst: str, rozmiar: int = 800, zakladka: int = 200) -> list[str]:
    """Fixed size with overlap. Does not break in the middle of a word."""
    if zakladka >= rozmiar:
        raise ValueError("the overlap must be smaller than the size")
    out, i = [], 0
    while i < len(tekst):
        koniec = min(i + rozmiar, len(tekst))
        # back up to a word boundary, unless this is the end of the text
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
        # the start of the next fragment is also on a word boundary
        sp = tekst.find(" ", i, koniec)
        if sp != -1:
            i = sp + 1
    return out

def chunk_akapity(tekst: str, max_znakow: int = 1200) -> list[str]:
    """By paragraph; paragraphs that are too long are split further by fixed size."""
    out = []
    for ak in re.split(r"\n\s*\n", tekst):
        ak = ak.strip()
        if not ak:
            continue
        out.extend([ak] if len(ak) <= max_znakow else chunk_staly(ak, max_znakow, 150))
    return out

def chunk_zdania(tekst: str, zdan_na_frag: int = 5, zakladka_zdan: int = 1) -> list[str]:
    """Groups N sentences with overlap. Never breaks a sentence."""
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

    for nazwa, fn in (("fixed 200/80", lambda t: chunk_staly(t, 200, 80)),
                      ("paragraphs",   chunk_akapity),
                      ("sentences 3/1", lambda t: chunk_zdania(t, 3, 1))):
        frag = fn(PROBKA)
        print(f"\n=== {nazwa}: {len(frag)} fragments")
        for i, f in enumerate(frag):
            znak = "   <- VAT exemption" if "Zwolnienie" in f else ""
            print(f"  [{i}] ({len(f):4d} ch) {f[:60]!r}...{znak}")
PYEOF

python3 $KURS/chunk.py
```

**Study the output.** See how in the "fixed 200/80" variant the sentence about the VAT exemption
**appears in two fragments** (the `<- VAT exemption` marker) — thanks to the overlap. That is
exactly the point. Also note that no fragment starts or ends
in the middle of a word.

### 3.4 ⚠️ Trap P29 (new): fragment metadata matters more than the fragment itself

A fragment without context is useless in an answer. **Always store with it:**

```python
{
  "tekst":      "Stawka VAT wynosi 23 procent...",
  "zrodlo":     "ustawa-vat.pdf",      # <-- for citing (§7)
  "strona":     14,                     # <-- so a human can check
  "naglowek":   "Art. 41. Stawki",      # <-- context for the model
  "pozycja":    3,                      # <-- order in the document
}
```

💡 **Inject the heading at the start of the fragment text before embedding.** The fragment
"Zwolnienie stosuje się do usług medycznych" embedded as
`"Art. 43. Zwolnienia | Zwolnienie stosuje się do usług medycznych"` is **much
easier to find**. It is one line of code and a large improvement in relevance.

---

## 4. A vector database in sqlite — from scratch

You do not need Qdrant or Chroma. With tens of thousands of fragments **sqlite +
a linear scan in Python is sufficient** and completely understandable.

```bash
cat > $KURS/baza.py <<'PYEOF'
#!/usr/bin/env python3
"""A vector database in sqlite. Pure Python, no numpy, no sqlite-vec.

Vectors are stored as a BLOB (struct.pack), searched linearly in Python.
With <100k fragments that is entirely sufficient and understandable as a whole.
"""
import json, math, os, sqlite3, struct, sys, urllib.request

DB     = os.path.join(os.environ["KURS"], "wiedza.db")
EMB_URL = "http://127.0.0.1:8093/v1/embeddings"

# ---------- embeddings ----------------------------------------------------
def embed(text: str) -> list[float]:
    req = urllib.request.Request(EMB_URL,
        data=json.dumps({"input": text}).encode(),
        headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=300))["data"][0]["embedding"]

def embed_wiele(teksty: list[str]) -> list[list[float]]:
    """In batches - much faster than one at a time."""
    req = urllib.request.Request(EMB_URL,
        data=json.dumps({"input": teksty}).encode(),
        headers={"Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=900))
    return [e["embedding"] for e in sorted(d["data"], key=lambda x: x["index"])]

# ---------- serialization -------------------------------------------------
def pak(v: list[float]) -> bytes:
    return struct.pack(f"{len(v)}f", *v)

def odpak(b: bytes) -> list[float]:
    return list(struct.unpack(f"{len(b)//4}f", b))

def znormalizuj(v: list[float]) -> list[float]:
    """Normalization to length 1. Then cosine == dot product (faster)."""
    n = math.sqrt(sum(x*x for x in v))
    return [x/n for x in v] if n else v

# ---------- schema --------------------------------------------------------
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

    -- FTS5 for word-for-word search (§5). Indexes heading + text,
    -- the same as the embedding (P29), so "Art. 43" will find the article's content.
    CREATE VIRTUAL TABLE IF NOT EXISTS fts USING fts5(tekst, tokenize='unicode61');
    """)
    con.commit()

# ---------- adding --------------------------------------------------------
def dodaj(con, fragmenty: list[dict], wsad: int = 16):
    """fragmenty: [{tekst, zrodlo, naglowek?, pozycja?}, ...]"""
    for i in range(0, len(fragmenty), wsad):
        grupa = fragmenty[i:i+wsad]
        # We prepend the heading BEFORE embedding - see P29
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
        print(f"  added {min(i+wsad, len(fragmenty))}/{len(fragmenty)}", file=sys.stderr)

# ---------- vector search ------------------------------------------------
def szukaj_wektorowo(con, pytanie: str, k: int = 5) -> list[dict]:
    q = znormalizuj(embed(pytanie))
    wyniki = []
    for rid, tekst, zrodlo, nagl, poz, blob in con.execute(
            "SELECT id,tekst,zrodlo,naglowek,pozycja,wektor FROM fragmenty"):
        v = odpak(blob)
        # both normalized => cosine = dot product
        s = sum(a*b for a, b in zip(q, v))
        wyniki.append({"id": rid, "tekst": tekst, "zrodlo": zrodlo,
                       "naglowek": nagl, "pozycja": poz, "score": s})
    wyniki.sort(key=lambda x: x["score"], reverse=True)
    return wyniki[:k]

# ---------- word search (BM25 from FTS5) ---------------------------------
def szukaj_slownie(con, pytanie: str, k: int = 5) -> list[dict]:
    import re
    # NOTE: `len(w) > 2` on its own would reject "43" (len=2) and "5" (len=1) -
    # and those are article numbers and rates, i.e. EXACTLY what this function is for
    # (P30: vectors are blind to identifiers). Numbers always pass.
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
                        "score": -rank})   # bm25 returns negatives: lower = better
    except sqlite3.OperationalError as e:
        print(f"  (FTS error: {e})", file=sys.stderr)
    return out

if __name__ == "__main__":
    con = sqlite3.connect(DB); init(con)
    n = con.execute("SELECT COUNT(*) FROM fragmenty").fetchone()[0]
    print(f"Database: {DB}\nFragments: {n}")
    if len(sys.argv) > 1:
        print(f"\nSearching: {sys.argv[1]!r}\n")
        for r in szukaj_wektorowo(con, sys.argv[1], 5):
            print(f"  {r['score']:.4f}  [{r['zrodlo']}]  {r['tekst'][:80]!r}")
PYEOF
```

### 4.1 Fill the database

```bash
cat > $KURS/indeksuj.py <<'PYEOF'
#!/usr/bin/env python3
"""Indexes the .txt/.md files from a directory into the vector database.

Usage:  python3 indeksuj.py $KURS/dokumenty
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
                # A markdown heading is metadata for the following fragments (P29), not a separate fragment
                if f.startswith("#"):
                    pierwsza, _, reszta = f.partition("\n")
                    naglowek = pierwsza.lstrip("# ")[:120]
                    f = reszta.strip()
                    if not f:
                        continue
                frag.append({"tekst": f, "zrodlo": p, "naglowek": naglowek, "pozycja": i})
    print(f"To index: {len(frag)} fragments from {katalog}")
    if frag:
        dodaj(con, frag)
    print(f"Done. In the database: {con.execute('SELECT COUNT(*) FROM fragmenty').fetchone()[0]}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "$KURS/dokumenty")
PYEOF

# Prepare test documents
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

# Index
cd $KURS && python3 indeksuj.py $KURS/dokumenty
```

### 4.2 Search

```bash
cd $KURS
python3 baza.py "jaka stawka VAT na książki"
echo "---"
python3 baza.py "ile lat trzymać faktury"
echo "---"
python3 baza.py "czy usługi lekarskie są opodatkowane"
```

(The three queries mean: "what VAT rate on books", "how many years to keep invoices", "are doctors' services taxed".)

The third question is interesting: **it contains neither the word "zwolnienie" (exemption) nor "medyczna" (medical)**, and vectors
should still hit Art. 43. **That is the advantage of vectors over word search.**

---

## 5. BM25 — why vectors alone are not enough

```bash
cd $KURS
python3 - <<'PYEOF'
import sqlite3, sys, os
sys.path.insert(0, os.environ["KURS"])
from baza import DB, szukaj_wektorowo, szukaj_slownie

con = sqlite3.connect(DB)
for q in ["czy usługi lekarskie są opodatkowane", "Art. 43", "FV/2025/09/0143"]:
    print(f"\n=== {q!r}")
    print("  VECTOR:")
    for r in szukaj_wektorowo(con, q, 3):
        print(f"    {r['score']:.3f}  {r['tekst'][:65]!r}")
    print("  WORD (BM25):")
    for r in szukaj_slownie(con, q, 3):
        print(f"    {r['score']:.3f}  {r['tekst'][:65]!r}")
PYEOF
```

⭐ **See where each method wins:**

| Query | Vectors | BM25 |
| :-- | :-- | :-- |
| "czy usługi lekarskie są opodatkowane" | ✅ understands the synonym: the right fragment is 1st | ❌ catches only the word "usługi": the right fragment only 3rd |
| "Art. 43" | ✅ only because the heading is attached to the fragment (P29) | ✅ hits exactly |
| "FV/2025/09/0143" | ❌ **the right invoice only 3rd** — 0141–0144 are "the same" to vectors | ✅ hits perfectly |

⚠️ **Trap P30 (new): vectors are useless for identifiers.**
Invoice numbers, tax IDs (NIP), symbols, codes — an embedding has no idea that `FV/2025/0143`
is a different invoice than `FV/2025/0144`. **For accounting data word search is
ESSENTIAL, not optional.**

---

## 6. Hybrid search and reranking

### 6.1 Rank fusion (RRF) — combines both rankings

```bash
cat > $KURS/hybryda.py <<'PYEOF'
#!/usr/bin/env python3
"""Hybrid search: vectors + BM25, combined through RRF.

RRF (Reciprocal Rank Fusion): score = sum over the lists of 1/(k + position).
Advantage: no need to normalize the different score scales - only the ORDER matters.
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
    print(f"Question: {q!r}\n")
    for i, r in enumerate(szukaj_hybrydowo(con, q), 1):
        print(f"{i}. rrf={r['rrf']:.4f}  [{r['zrodlo']}]")
        print(f"   {r['tekst'][:100]!r}\n")
PYEOF

cd $KURS
python3 hybryda.py "Art. 43 zwolnienia medyczne"
python3 hybryda.py "ile procent podatku na książki"
```

💡 **Why RRF and not a weighted sum of scores.** Cosine gives 0–1, BM25 gives arbitrary
numbers. Normalizing them to a common scale is arbitrary and brittle. **RRF looks only
at the order** — it works without calibration and is robust to swapping the embedding model.

### 6.2 Reranking — a model as relevance judge

The search engine gives 20 candidates. The model scores each one and you keep the 5 best.
**Slower, but clearly more relevant.**

From this point on you need a **generative model on port 8081**. Start Bielik — the embedding
server on 8093 stays on. **Do not use `pkill -f llama-server` here** from the previous
parts: it would kill both servers.

```bash
pkill -f "llama-server.*--port 8081"; sleep 2
$LB/llama-server -m $BIELIK -ngl 999 -c 8192 --port 8081 --host 127.0.0.1 --no-warmup \
  > /tmp/bielik-8081.log 2>&1 &
sleep 25
```

```bash
cat > $KURS/rerank.py <<'PYEOF'
#!/usr/bin/env python3
"""Reranking: the model scores the relevance of each candidate on a 0-10 scale.

Grammar-constrained (part 3) - the model CANNOT return anything other than a number.
Through the chat endpoint, so that the model gets its template (part 3).
"""
import json, os, sqlite3, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from baza import DB
from hybryda import szukaj_hybrydowo

LLM = "http://127.0.0.1:8081"
GRAMATYKA = 'root ::= [0-9] | "10"'
# The judge prompt below is in Polish, like the documents. It says: "You rate the relevance of a
# document fragment to the question. You answer with a single number from 0 to 10: 0 = the fragment
# has nothing to do with the question, 5 = partly helps, 10 = contains the full answer."
SEDZIA = ("Oceniasz trafność fragmentu dokumentu względem pytania. Odpowiadasz jedną liczbą "
          "od 0 do 10: 0 = fragment nie ma związku z pytaniem, 5 = częściowo pomaga, "
          "10 = zawiera pełną odpowiedź.")

def ocen(pytanie: str, fragment: str) -> int:
    # Chat endpoint, not /v1/completions: an instruct model without its chat template
    # scores "blindly" (it came out as 10 for every fragment).
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
    print(f"Question: {q!r}\n")
    print("BEFORE reranking (hybrid order):")
    for i, r in enumerate(szukaj_hybrydowo(con, q, 6), 1):
        print(f"  {i}. {r['tekst'][:70]!r}")
    print("\nAFTER reranking:")
    for i, r in enumerate(szukaj_z_rerankiem(con, q), 1):
        print(f"  {i}. score={r['ocena']:2d}  {r['tekst'][:70]!r}")
PYEOF

cd $KURS && python3 rerank.py "czy lekarz płaci VAT"
```

⚠️ **Reranking costs one forward pass per candidate.** 12 candidates = 12 calls to the
model. With `max_tokens: 4` that is a cheap prefill (part 2 §5), but not free.
**Use it when relevance matters; skip it when response time matters.**

---

## 7. Citations and grounding

⭐ **This is the chapter that decides whether your accounting product can be sold.**
An answer whose source cannot be checked is worthless in accounting.

### 7.1 A prompt that enforces grounding

```bash
cat > $KURS/odpowiedz.py <<'PYEOF'
#!/usr/bin/env python3
"""RAG with enforced citations and verification in code."""
import json, os, re, sqlite3, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from baza import DB
from hybryda import szukaj_hybrydowo

LLM = "http://127.0.0.1:8081"

# The prompt is in Polish, like the documents. It says: "You answer EXCLUSIVELY on the basis of the
# given fragments. RULES: 1. Every claim must have a reference [n] to the fragment number.
# 2. If the fragments do not contain the answer - write exactly: "I did not find this information
# in the available documents." 3. Do not use knowledge from outside the fragments. Do not guess.
# 4. Do not cite a fragment you did not use."
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

    # --- VERIFICATION: do the citations exist? -----------------------
    uzyte = sorted({int(n) for n in re.findall(r"\[(\d+)\]", tekst)})
    zmyslone = [n for n in uzyte if n < 1 or n > len(frag)]
    return tekst, frag, zmyslone

if __name__ == "__main__":
    con = sqlite3.connect(DB)
    q = sys.argv[1] if len(sys.argv) > 1 else "Jaka jest stawka VAT na książki?"
    tekst, frag, zmyslone = odpowiedz(con, q)

    print(f"QUESTION: {q}\n")
    print(f"ANSWER:\n{tekst}\n")
    print("SOURCES:")
    for i, f in enumerate(frag, 1):
        print(f"  [{i}] {f['zrodlo']}" + (f" — {f['naglowek']}" if f.get('naglowek') else ""))
    if zmyslone:
        print(f"\n⚠️  THE MODEL MADE UP REFERENCES: {zmyslone} — REJECT THIS ANSWER")
    else:
        print("\n✅ all references exist")
PYEOF

cd $KURS
python3 odpowiedz.py "Jaka jest stawka VAT na książki?"
echo "======================================"
python3 odpowiedz.py "Ile wynosi składka ZUS dla przedsiębiorcy?"
```

(The questions mean: "What is the VAT rate on books?" and "How much is the ZUS social insurance contribution for a self-employed person?")

⭐ **The second question is the most important test in the whole chapter.** The answer is **not**
in the documents. The model **must** say "I did not find it". If it makes something up instead —
your prompt is too weak and you must not go further.

### 7.2 Verifying references in code

Note `zmyslone` ("made up") in the script. **The model may cite `[7]` when you gave it 4 fragments.**
The code catches this and rejects the answer. This is cheap and necessary.

### 7.3 Stronger verification — whether the claim is really in the fragment

```bash
cat >> $KURS/odpowiedz.py <<'PYEOF'

# ---------- additional verification: sentence grounding -----------------
def sprawdz_uziemienie(zdanie: str, fragment: str) -> bool:
    """Asks the model whether the sentence FOLLOWS from the fragment. A grammar forces yes/no."""
    # Polish prompt: "You check whether the sentence follows from the fragment. You answer only:
    # yes or no." / "Does this sentence follow EXCLUSIVELY from the fragment?" (answers: tak = yes, nie = no)
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

# Check: the first sentence follows from the fragment, the second does not
cd $KURS && python3 -c "
from odpowiedz import sprawdz_uziemienie as s
f = 'Stawka obniżona 5 procent dotyczy książek i czasopism specjalistycznych.'
print('5 percent on books :', s('Stawka VAT na książki wynosi 5 procent.', f))
print('23 percent on books:', s('Stawka VAT na książki wynosi 23 procent.', f))
"
```

Expected result: `True`, then `False`.

💡 **When to use it:** for answers that go to a customer without human review.
It costs one call per sentence. **For an accounting product it is worth it.**

---

## 8. Context engineering — budget and compaction

⭐ **This section is the foundation of part 6.** An agent without context management falls over
after a dozen or so turns.

### 8.1 Context budget — hard arithmetic

```bash
cat > $KURS/budzet.py <<'PYEOF'
#!/usr/bin/env python3
"""Context budget. Counts tokens with THE tokenizer the model uses (P20)."""
import os, subprocess

LB = os.path.expanduser("~/llama.cpp/build/bin")

class Budzet:
    def __init__(self, model_sciezka: str, n_ctx: int, rezerwa_wyjscia: int = 1024):
        self.model = os.path.expanduser(os.path.expandvars(model_sciezka))
        self.n_ctx = n_ctx
        self.rezerwa = rezerwa_wyjscia
        self._cache: dict[str, int] = {}

    def tokeny(self, tekst: str) -> int:
        """Counts tokens. Cached, because llama-tokenize is a process."""
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
        """Packs fragments up to the limit. MOST RELEVANT LAST (part 2 §6.2)."""
        wybrane, suma = [], 0
        for f in fragmenty:                       # order: from the most relevant
            n = self.tokeny(f["tekst"])
            if suma + n > limit_tokenow:
                break
            wybrane.append(f); suma += n
        wybrane.reverse()                          # most relevant last = closer to the question
        return wybrane

if __name__ == "__main__":
    b = Budzet("~/models/bielik-11b/Bielik-11B-v3.0-Instruct.Q8_0.gguf", n_ctx=8192)
    SYS = "Odpowiadasz wyłącznie na podstawie fragmentów. Każde twierdzenie z odnośnikiem."
    PYT = "Jaka jest stawka VAT na książki i czasopisma specjalistyczne?"
    n_sys, n_pyt = b.tokeny(SYS), b.tokeny(PYT)
    print(f"n_ctx            = {b.n_ctx}")
    print(f"output reserve   = {b.rezerwa}")
    print(f"system prompt    = {n_sys}")
    print(f"question         = {n_pyt}")
    print(f"--> for fragments = {b.dostepne(n_sys + n_pyt)} tokens")
PYEOF

cd $KURS && python3 budzet.py
```

⭐ **Note `wybrane.reverse()`.** This is a direct application of the finding
from part 2 §6.2 ("lost in the middle"): **the most relevant fragment should stand closest to
the question**, i.e. at the end of the list. One line, a measurable improvement in relevance.

### 8.2 Compaction — when the conversation does not fit in the context

This is a mechanism the agent in part 6 **must** have.

```bash
cat > $KURS/kompakcja.py <<'PYEOF'
#!/usr/bin/env python3
"""Conversation history compaction: summarize old turns, keep recent ones verbatim."""
import json, urllib.request

LLM = "http://127.0.0.1:8081"

# Polish prompt. It says: "You summarize the history of an agent's work. Keep CONCISELY: what the
# task was; what has already been established (facts, numbers, file names); what has already been
# tried and with what result; what remains to be done. Omit: pleasantries, repetitions, full file
# contents. At most 300 words."
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
    """[system] + [summary of the old ones] + [the N most recent verbatim]"""
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
    print(f"BEFORE: {len(demo)} messages")
    po = skompaktuj(demo, zostaw_swiezych=4)
    print(f"AFTER:  {len(po)} messages\n")
    for m in po:
        print(f"[{m['role']}] {m['content'][:180]}...")
PYEOF

cd $KURS && python3 kompakcja.py
```

⚠️ **Trap P31 (new): compaction loses exact numbers.**
A summary is a model — it may round an amount or garble an invoice number. **Anything that
must be exact, store outside the context**: in a file, in a database, in a structure in code.
Context is short-term memory, not a system of record.

💡 **The pattern we will introduce in part 6:** after every important finding the agent writes it
to a `USTALENIA.md` file (Polish for "findings"). Compaction may lose a detail from the conversation — the file will not.

---

## 9. Evaluating RAG

**You measure two things separately.** Mixing them is the most common mistake.

| Metric | What it measures | How |
| :-- | :-- | :-- |
| **retrieval relevance** (recall@k) | whether the right fragment **made it** into the prompt | mark by hand which fragment is correct |
| **answer correctness** | whether the model **used** well what it received | compare with a reference answer |

💡 **Why separately.** If you measure only the final answer and the result is bad — **you do not
know whether the search engine or the model is to blame**. With two metrics you know at once what to fix.

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
"""RAG evaluation: retrieval relevance AND answer correctness - separately."""
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
        # --- METRIC 1: did the right source make it into the top-k? ---
        frag = szukaj_hybrydowo(con, p["pytanie"], 4)
        zrodla = {f["zrodlo"] for f in frag}
        if p["zrodlo_ok"] is None:
            szuk = "n/a"      # a question with no answer in the database
        else:
            n_ocenianych_szukan += 1
            ok = p["zrodlo_ok"] in zrodla
            trafne_szukanie += ok
            szuk = "✅" if ok else "❌"

        # --- METRIC 2: is the answer correct? ---
        tekst, _, zmyslone = odpowiedz(con, p["pytanie"], 4)
        low = tekst.lower()
        ma   = all(s.lower() in low for s in p["musi_zawierac"])
        niema= all(s.lower() not in low for s in p["nie_moze"])
        odp_ok = ma and niema and not zmyslone
        trafne_odp += odp_ok

        print(f"  {p['id']}: retrieval {szuk}  answer {'✅' if odp_ok else '❌'}")
        if not odp_ok:
            if not ma:     print(f"       missing: {[s for s in p['musi_zawierac'] if s.lower() not in low]}")
            if not niema:  print(f"       forbidden: {[s for s in p['nie_moze'] if s.lower() in low]}")
            if zmyslone:   print(f"       made-up references: {zmyslone}")
            print(f"       -> {tekst[:150]!r}")

    n = len(przyp)
    print(f"\n{'='*52}")
    if n_ocenianych_szukan:
        print(f"  recall@4 (retrieval): {trafne_szukanie}/{n_ocenianych_szukan} = {100*trafne_szukanie/n_ocenianych_szukan:.0f}%")
    print(f"  answer correctness:   {trafne_odp}/{n} = {100*trafne_odp/n:.0f}%")
    print("\n  Diagnosis:")
    print("   low recall, low answers   -> fix the CHUNKING (§3) and the HYBRID (§6)")
    print("   high recall, low answers  -> fix the PROMPT (§7) or get a better model")

if __name__ == "__main__":
    main()
PYEOF

cd $KURS && python3 eval/rag.py
```

⭐ **Read the diagnosis at the end.** It is a decision map that saves days of wandering:
high recall + weak answers = a problem in the model/prompt. Low recall = a problem
in retrieval. **Never guess which side to fix.**

---

## Final exercise

1. **Index something real** — e.g. `TECHNIKA.md` and `HANDOFF.md` from your project:
   ```bash
   mkdir -p $KURS/dokumenty/projekt
   cp ~/Desktop/local_agents_project/lokalne/TECHNIKA.md $KURS/dokumenty/projekt/
   cp ~/Desktop/local_agents_project/lokalne/HANDOFF.md $KURS/dokumenty/projekt/
   cd $KURS && python3 indeksuj.py $KURS/dokumenty/projekt
   ```
2. **Ask about your own machine:**
   ```bash
   python3 odpowiedz.py "Jaki limit mocy jest ustawiony na kartach?"
   python3 odpowiedz.py "Co to jest pułapka P4?"
   python3 odpowiedz.py "Jakie gniazdo zasilania ma płytka F3G?"
   ```
   (These ask: "What power limit is set on the cards?", "What is trap P4?", "What power connector does the F3G board have?")

   ⭐ **This is the moment when RAG stops being an exercise.** You have a search engine over
   your own technical documentation, working offline.

   ⚠️ **Check the first answer against the document.** `TECHNIKA.md` has both the old procedure (§8,
   210 W) and a newer section §16.3 "Limit mocy 250 W — i dlaczego to NIE jest już 210 W" (the 250 W power limit — and why it is NO LONGER 210 W).
   If the model answers "210 W", the search engine gave it only the old fragments, and it
   correctly cited them. That is a typical flaw of RAG over living documentation: **contradictory versions
   of the same fact**. Good material for exercises 3–4.
3. **Compare the three chunking strategies** on the same set of questions. Measure recall@4
   for each. Write down the results.
4. **Break it on purpose:** index with `chunk_staly(t, 150, 0)` (small fragments, zero
   overlap) and measure again. See how recall drops. **Now you understand why
   chunking is more important than the model.**

---

## Check yourself

- [ ] Why will a smarter model not fix bad retrieval?
- [ ] Why must you not quantize an embedding model to Q4?
- [ ] Why do you prepend the heading to the text **before** embedding?
- [ ] Why will vectors not find the invoice `FV/2025/0143`?
- [ ] Why is RRF better than a weighted sum of scores?
- [ ] Why should the most relevant fragment be **at the end** of the prompt?
- [ ] What do you do when recall is high but the answers are bad?
- [ ] Why must compaction not be trusted with exact numbers?

## New traps

| ID | Trap | § |
| :-- | :-- | :-- |
| **P29** | A fragment without metadata and heading — poorly found, not citable | §3.4 |
| **P30** | Vectors are useless for identifiers (numbers, tax IDs) | §5 |
| **P31** | Compaction loses exact numbers — store important facts outside the context | §8.2 |

---

**Next part: `05-MULTIMODALITY.md`** — an agent that sees images, hears your voice
and answers by voice. With a list of hardware to buy.
