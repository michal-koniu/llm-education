# Part 7 · Tools — design and ergonomics

**Level:** ⭐⭐⭐⭐ · **Time:** ~5 h · **Requires:** parts 4 (budget) and 6 (prompt assembly)
**Produces:** a tool registry, observation trimming, idempotency keys, a tool-count ablation

---

## 0. A tool is a user interface whose user is the model

You write a tool as if you were writing it for a junior who:

- will read **only the description**, never the code,
- will not remember anything between turns,
- under pressure will **guess** instead of asking,
- and on an error will either give up or repeat the same thing.

Each of these four traits has a corresponding design rule. This whole part is their
elaboration.

> ⭐ **The arithmetic from part 1 returns here and is the heart of the matter.** At 92%
> success per step, 15 steps give 29%. **Tool design is the main lever for raising
> that 92%**, and at the same time a lever for shortening the chain, because a better
> tool does in one step what a worse one does in three.

---

## 1. Anatomy of a tool

```python
{
  "nazwa": "czytaj_dokument",
  "opis": ("Reads a text document or PDF from the archive. Returns the content. "
           "For documents > 500 lines it returns the beginning and the end — "
           "then use `szukaj_w_dokumencie` to get the middle."),
  "parametry": {
    "sciezka": {
      "typ": "string",
      "opis": "Path relative to ~/dokumenty, e.g. 'faktury/2026/03/orange.pdf'. "
              "Absolute paths are rejected.",
      "wymagany": True
    },
    "od_linii": {
      "typ": "integer",
      "opis": "Number of the first line (from 1). Defaults to 1.",
      "wymagany": False, "domyslnie": 1
    }
  }
}
```

**Five things this description does well:**

1. **It says what it returns**, not only what it does.
2. **It warns about the edge behaviour**: truncation at >500 lines.
3. **It points to the next tool**: "then use `szukaj_w_dokumencie`". This is the
   cheapest way to teach the model a sequence.
4. **It gives a format example**: `'faktury/2026/03/orange.pdf'` says more than a sentence.
5. **It says what is rejected**: the model does not waste a turn on an attempt.

### 1.1 · Naming

| Rule | ✗ | ✓ |
| :-- | :-- | :-- |
| Verb + noun | `dokument`, `pdf_handler` | `czytaj_dokument` |
| No abbreviations | `rd_doc`, `get_fl` | `czytaj_dokument` |
| Unambiguous relative to the rest | `szukaj` and `znajdz` side by side | `szukaj_w_dokumencie`, `znajdz_dokumenty` |
| Consistent language | `read_file` next to `zapisz_plik` | one language across the whole set |

⚠️ **The third row is the one that hurts most.** Two tools with similar names and
overlapping descriptions are a **guaranteed selection error**, and one you will not fix
with a better prompt. Anthropic says this outright: tools should **minimize overlap in
functionality**. If you cannot say in one sentence when to use A and when to use B,
**merge them or remove one**.

---

## 2. Lenient input, strict output

Steinberger's rule from the MCP Best Practices, paraphrased:

> Parameter parsing should be lenient (e.g. accept `path` when `project_path` is
> formally defined).

```python
ALIASY = {
    "sciezka": ["path", "plik", "file", "sciezka_pliku", "filepath"],
    "od_linii": ["from_line", "start", "od"],
}

def normalizuj(argumenty: dict, schemat: dict) -> dict:
    """The model will get a parameter name wrong. Don't punish it with a turn."""
    wynik = {}
    for kanon, spec in schemat.items():
        if kanon in argumenty:
            wynik[kanon] = argumenty[kanon]
            continue
        for alias in ALIASY.get(kanon, []):
            if alias in argumenty:
                wynik[kanon] = argumenty[alias]
                break
        else:
            if spec.get("wymagany"):
                raise BladNarzedzia(
                    f"Missing required parameter '{kanon}'. "
                    f"You passed: {list(argumenty)}. "
                    f"Expected: {list(schemat)}.")
            if "domyslnie" in spec:
                wynik[kanon] = spec["domyslnie"]
    return wynik
```

⭐ **One turn wasted on a typo in a parameter name costs you ~2 seconds and ~400
tokens.** Thirty lines of aliases pay for themselves on the first day.

**But the output must be strict and predictable.** Leniency on input, rigour on
output, because the model reads the output and every inconsistency confuses it.

---

## 3. Shaping observations: where context dies

This is the place where agents lose most often, and also the easiest to fix.

```
ls -R ~/dokumenty        → 14,200 tokens      ← half the window, in one call
cat duza-umowa.pdf       →  8,900 tokens
git log                  →  6,100 tokens
```

### 3.1 · Four techniques, in order of use

**1 · Trimming that keeps both ends**

```python
def przytnij(tresc: str, limit=2000) -> str:
    if len(tresc) <= limit:
        return tresc
    p = limit // 2
    return (tresc[:p] +
            f"\n\n[… cut {len(tresc)-limit} characters. "
            f"Use a narrower query if you need the middle …]\n\n" +
            tresc[-p:])
```

⭐ **The middle is cut deliberately.** In command output, information concentrates at
the edges: the beginning is the header and structure, the end is the summary, errors and
status. The middle is usually a repetitive list.

**2 · A structured summary instead of the raw result**

```python
def podsumuj_liste_plikow(sciezki: list) -> str:
    """Instead of a 14k-token list, 200 tokens of structure."""
    from collections import Counter
    katalogi = Counter(str(pathlib.Path(s).parent) for s in sciezki)
    rozszerz = Counter(pathlib.Path(s).suffix for s in sciezki)
    return (f"{len(sciezki)} files in {len(katalogi)} directories.\n"
            f"Largest directories: " +
            ", ".join(f"{k} ({n})" for k, n in katalogi.most_common(8)) + "\n"
            f"Types: " + ", ".join(f"{e or '(none)'} ({n})" for e, n in rozszerz.most_common()) +
            "\n\nUse `znajdz_dokumenty(wzorzec)` to narrow down.")
```

**3 · Pagination with an explicit pointer**

```
Results 1–20 of 340. To see more: znajdz_dokumenty(..., od=21).
```

**4 · A pointer instead of the content**: the result lands in a file, and the model
gets the path and a header. This is the just-in-time loading from part 4, applied to
tool output.

### 3.2 · A budget per tool

```python
LIMITY = {
    "czytaj_dokument":   4000,   # sometimes you really do need a lot
    "znajdz_dokumenty":   800,   # a list: a summary is enough
    "powloka":           2000,
    "szukaj_w_sieci":    1500,   # ⚠️ the most untrusted, so the shortest
}
```

⚠️ **`szukaj_w_sieci` has the lowest limit for a reason.** The less foreign text you
let into the context, the smaller the injection surface. **The token limit here is a
security measure, not just a saving.** It comes back in parts 10 and 16.

---

## 4. The error is a prompt

An elaboration of the ladder from part 3. A good error message has **three parts**:

```
WHAT went wrong    +    WHY    +    WHAT IS ALLOWED INSTEAD
```

| ✗ Bad | ✓ Good |
| :-- | :-- |
| `FileNotFoundError: faktury/orange.pdf` | `There is no file 'faktury/orange.pdf'. The directory 'faktury/' contains subdirectories: 2025/, 2026/. Try 'faktury/2026/orange.pdf' or use znajdz_dokumenty("orange").` |
| `PermissionError: [Errno 13]` | `No write permission for /etc/hosts. Writing is allowed only in ~/dokumenty and /tmp. If this is an intermediate result, use /tmp/wynik.txt.` |
| `TimeoutError` | `The command exceeded 30 s and was aborted. If you are processing many files, split them into batches of 50 and call it several times.` |
| `JSONDecodeError: line 1 col 1` | `You returned text, but JSON was expected. Your answer started with 'Sure, here is...'. Return ONLY the JSON object, with no preamble.` |

```python
class BladNarzedzia(Exception):
    def __init__(self, co, dlaczego="", zamiast=""):
        self.tresc = co + (f" {dlaczego}" if dlaczego else "") + \
                     (f"\nTry: {zamiast}" if zamiast else "")
        super().__init__(self.tresc)

# Usage: note that the hint is COMPUTED, not constant:
raise BladNarzedzia(
    co=f"There is no file '{s}'.",
    dlaczego=f"'{rodzic}' contains: {', '.join(sasiedzi[:6])}.",
    zamiast=f"znajdz_dokumenty('{pathlib.Path(s).stem}')")
```

⭐ **"Computed, not constant" matters here.** A hint containing the **actual contents of
the directory** raises the chance of a fix from ~20% to over 90%. A constant hint
("check the path") gives almost nothing.

---

## 5. Idempotency: a tool that may safely be repeated

An agent repeats calls: after a timeout, after an unclear result, after a session
restart. If a tool has a side effect, a repeat **does that effect twice**.

```python
import hashlib, json, os, pathlib

def klucz_idempotencji(narzedzie: str, argumenty: dict) -> str:
    return hashlib.sha256(
        (narzedzie + json.dumps(argumenty, sort_keys=True)).encode()).hexdigest()[:16]

class RejestrSkutkow:
    """Executed operations with a side effect. A repeat returns the previous result."""
    def __init__(self, plik="$OSA/skutki.json"):
        self.p = pathlib.Path(os.path.expandvars(plik)).expanduser()
        self.d = json.loads(self.p.read_text()) if self.p.exists() else {}

    def wykonaj_raz(self, narzedzie, argumenty, funkcja):
        k = klucz_idempotencji(narzedzie, argumenty)
        if k in self.d:
            return (f"[already executed {self.d[k]['kiedy']}] {self.d[k]['wynik']}")
        wynik = funkcja(**argumenty)
        self.d[k] = {"kiedy": TERAZ(), "wynik": str(wynik)[:500]}
        self.p.write_text(json.dumps(self.d, ensure_ascii=False, indent=1))
        return wynik
```

| Tool | Idempotent? | Note |
| :-- | :-- | :-- |
| `czytaj_dokument` | ⭐ yes | a read: repeat freely |
| `znajdz_dokumenty` | ⭐ yes | — |
| `zmien_nazwe` | ✗ **no** | ⚠️ the second call renames the already renamed file |
| `wyslij_wiadomosc` | ✗ **no** | ⚠️⚠️ a double send is visible to people |
| `dopisz_do_pliku` | ✗ **no** | the entry appears twice |

⚠️ **Record in the tool registry which tools are idempotent, and treat it as a
mandatory field.** A tool without a declared idempotency is by default considered
non-idempotent and is passed through `wykonaj_raz`.

---

## 6. How many tools is too many

Here is a hard trade-off, and hardly anyone measures it.

```
     TOOL SELECTION ACCURACY vs NUMBER OF TOOLS  (expected shape)

  95% ┤●●●●●●
      │      ●●●●●
  85% ┤           ●●●●
      │               ●●●●
  70% ┤                   ●●●●●
      │                        ●●●●●●●
  50% ┤                               ●●●●
      └──┬─────┬─────┬─────┬─────┬─────┬───
         3     8    15    25    40    60
```

Two mechanisms operate at once, and both make things worse:

1. **Context cost**: 40 tools × ~200 tokens = 8k tokens **in every turn**.
2. **Selection ambiguity**: the more tools, the more pairs with overlapping
   descriptions.

### 6.1 · Three strategies

| Strategy | How | Cost | When |
| :-- | :-- | :-- | :-- |
| **A · fewer tools** | merge similar ones, remove unused ones | zero | ⭐ always first |
| **B · just-in-time loading** | show 5 core tools + `znajdz_narzedzie(opis)` | 1 turn for rare ones | >15 tools |
| **C · code-mode** | tools as functions in code, not in the prompt | see part 8 | ⭐⭐ >25 tools |

**Strategy A is underrated.** Before you add a mechanism, check the log: how many tools
did the agent use **at least once** in the last 100 sessions?

```bash
python3 sesja-cli.py statystyki-narzedzi --ostatnie 100
# name               uses   % sessions   errors
# czytaj_dokument     412      94%       3%
# znajdz_dokumenty    388      91%       1%
# powloka             201      44%      12%   ← high error rate, see §4
# konwertuj_docx        4       2%      50%   ← ⚠️ candidate for removal
# ocr_skan              0       0%        —   ← ⚠️⚠️ remove
```

⭐ **A tool used in 2% of sessions costs context in 100% of sessions.** This is a bad
deal and the simplest optimization in the whole course.

### 6.2 · Blast radius as a design criterion

Steinberger plans changes by **blast radius**: how many files they will touch. The same
unit works very well when designing tools:

| Radius | Example | Requirements |
| :-- | :-- | :-- |
| **Zero** (read) | `czytaj_dokument` | none; idempotent by definition |
| **Point** (1 object) | `zmien_nazwe(plik)` | log, idempotency |
| **Local** (up to 10) | `zmien_nazwy(wzorzec)` | ⭐ **`--sucho` (dry-run) mode mandatory** |
| **Wide** (>10) | `przenies_katalog` | ⭐⭐ human confirmation + a backup |
| **Irreversible** | `wyslij_mail`, `usun` | ⭐⭐⭐ confirmation + **don't give it to the agent** |

```python
def wymaga_zgody(narzedzie: dict, argumenty: dict, granice: dict) -> bool:
    promien = narzedzie["promien"](argumenty)       # computed, not constant
    return promien >= granice.get("prog_zgody", 10)
```

⚠️ **The radius must be computed from the arguments, not from the tool name.**
`zmien_nazwy("*.txt")` has a radius of 3 or 3000 depending on the directory, and this
is exactly the difference that decides whether to ask.

---

## 7. FROM SCRATCH: the tool registry

```python
# $OSA/narzedzia/rejestr.py
"""Registry: one place for the schema, limits, radius and idempotency."""
import json, time, inspect

class Rejestr:
    def __init__(self, budzet_obserwacji=2000):
        self.n, self.budzet = {}, budzet_obserwacji

    def dodaj(self, nazwa, opis, parametry, funkcja, *,
              limit=None, idempotentne=False, promien=lambda a: 0, zaufanie="host"):
        self.n[nazwa] = dict(nazwa=nazwa, opis=opis, parametry=parametry,
                             funkcja=funkcja, limit=limit or self.budzet,
                             idempotentne=idempotentne, promien=promien,
                             zaufanie=zaufanie)

    def schemat(self, poziom_zaufania="host", tylko=None) -> list:
        """What goes into the prompt. Filtered by session trust: P88."""
        rzad = {"piaskownica": 0, "host": 1}
        out = []
        for n in self.n.values():
            if rzad[poziom_zaufania] < rzad[n["zaufanie"]]:
                continue                       # an untrusted session DOES NOT SEE the tool
            if tylko and n["nazwa"] not in tylko:
                continue
            out.append({k: n[k] for k in ("nazwa", "opis", "parametry")})
        return out

    def wywolaj(self, nazwa, argumenty, kontekst) -> dict:
        if nazwa not in self.n:
            bliskie = [k for k in self.n if nazwa[:4] in k]
            raise BladNarzedzia(f"There is no tool '{nazwa}'.",
                                f"Available: {', '.join(self.schemat_nazw(kontekst))}.",
                                bliskie[0] if bliskie else "")
        n = self.n[nazwa]
        if kontekst["zaufanie"] == "piaskownica" and n["zaufanie"] == "host":
            raise BladNarzedzia(f"'{nazwa}' is unavailable in this session.",
                                "The session has the 'piaskownica' (sandbox) level.", "")
        arg = normalizuj(argumenty, n["parametry"])
        if n["promien"](arg) >= kontekst.get("prog_zgody", 10) and not kontekst.get("zgoda"):
            return {"status": "wymaga_zgody",
                    "tresc": f"The operation will touch ~{n['promien'](arg)} objects. "
                             f"Confirm to execute."}
        t0 = time.time()
        try:
            wynik = (kontekst["skutki"].wykonaj_raz(nazwa, arg, n["funkcja"])
                     if not n["idempotentne"] else n["funkcja"](**arg))
            status = "ok"
        except BladNarzedzia as e:
            wynik, status = e.tresc, "blad"
        except Exception as e:
            wynik, status = f"Unexpected error: {type(e).__name__}: {e}", "blad"
        return {"status": status, "tresc": przytnij(str(wynik), n["limit"]),
                "ms": int((time.time() - t0) * 1000)}
```

**Three things this registry does that most implementations do not:**

1. **It filters tools by the session's trust level.** A session from the sandbox does
   not even **see** the host's tools. An invisible tool will be neither called nor
   described to an attacker.
2. **It computes the radius from the arguments** and asks for consent.
3. **It never lets a raw traceback out**: every exception comes back as readable text.

---

## 8. IN PRODUCTION

| | Anthropic tool use | MCP | LangChain | **Your registry** |
| :-- | :-- | :-- | :-- | :-- |
| Schema | JSON Schema | JSON Schema | Pydantic | dict |
| `strict` validation | ⭐ yes | partially | ⭐ yes | manual |
| **Lenient aliases** | ✗ | ✗ | ✗ | ⭐ yes |
| **Trust filter** | ✗ | ✗ | ✗ | ⭐ yes |
| **Blast radius** | ✗ | ✗ | ✗ | ⭐ yes |
| **Idempotency** | manual | ⭐ convention | ✗ | ⭐ enforced |
| Just-in-time tool loading | ⭐ tool search | ⭐ since 2026-07 | ✗ | manual |

> 💡 **One thing worth taking from outside: JSON Schema instead of your own dict.**
> Not because it is prettier, but because **`llama-server` can enforce a JSON Schema
> at the sampling level** (grammars from course 1, part 3). Structural enforcement is
> not a request to the model, it is a guarantee. With local models this difference is
> much larger than with frontier ones.

---

## 9. EXPERIMENT 7: tool-count ablation

⭐ **This experiment will give you a number you will not find in any documentation: how
many tools your models can handle.**

**Hypothesis:** tool selection accuracy drops nonlinearly with their number, and the
threshold is **much lower** for local models than for frontier ones.

### 9.1 · Setup

```bash
mkdir -p $OSA/pomiary/narzedzia && cd $OSA/pomiary/narzedzia
```

- **5 real tools**: the ones the agent actually uses.
- **35 decoys**: working, but irrelevant (`sprawdz_pogode`, `konwertuj_waluty`,
  `generuj_qr`…). ⚠️ **The descriptions must be plausible**, not "decoy 7", otherwise
  you are measuring something else.
- **40 tasks** with an unambiguously correct tool.

```python
# zadania.py
ZADANIA = [
  ("How many lines does umowa-najem.txt have?",       "czytaj_dokument"),
  ("Find all invoices from March",                    "znajdz_dokumenty"),
  ("Rename skan001.pdf to faktura.pdf",               "zmien_nazwe"),
  ("How many files are in ~/dokumenty?",              "powloka"),
  ("What do you remember about my electricity bill?", "przypomnij"),
  # … up to 40, 8 for each real tool
]
```

### 9.2 · Run

```bash
for n in 5 10 15 25 40; do
  python3 ablacja.py --narzedzi $n --model gpt-oss-20b --powtorzen 3
done
```

| Tools in the prompt | Selection accuracy | Tokens (schemas) | Time to 1st token | Wrong arguments |
| --: | --: | --: | --: | --: |
| 5 | /40 | | | |
| 10 | /40 | | | |
| 15 | /40 | | | |
| 25 | /40 | | | |
| 40 | /40 | | | |

**Repeat for `qwen3-32b`.** Expect the denser model to hold up longer, and that is a
concrete argument for the routing from part 17.

### 9.3 · Additional experiment: which pairs get confused

```bash
python3 ablacja.py --narzedzi 40 --macierz-pomylek
# list the 10 most frequent pairs (expected → chosen)
```

⭐ **This is the most practical result of this whole part.** You get a concrete list of
tool pairs with overlapping descriptions. For each pair do one of three things:
**merge**, **remove one**, or **rewrite both descriptions so the difference is in the
first sentence**. Then measure again.

⚠️ **Prediction to check:** with `gpt-oss-20b` I expect a clear drop already between 15
and 25 tools, and most mistakes **concentrated in 3–4 pairs**, not spread evenly. If
so, fixing four descriptions will buy you most of the lost accuracy without any
mechanism.

---

## 10. EXERCISE: rewrite the Archivist's tool set

1. List all the tools it has today, with usage statistics.
2. **Remove each one used in fewer than 5% of sessions.** No sentimentality.
3. For each remaining one fill in: `limit`, `idempotentne`, `promien`, `zaufanie`.
4. Rewrite the descriptions following the five rules from §1: what it returns, edge
   behaviour, pointer to the next tool, format example, what is rejected.
5. Write **three error messages** in the WHAT + WHY + WHAT INSTEAD format, with a hint
   **computed** from the actual state.
6. Re-measure the tasks from §9 on the new set.

```bash
python3 sesja-cli.py narzedzia archiwista --sprawdz
# expect it to detect:
#   ⚠️ 'szukaj' and 'znajdz': descriptions overlap by 71%
#   ⚠️ 'zmien_nazwe': no declared idempotency
#   ⚠️ 'powloka': constant radius, should be computed from arguments
#   ⚠️ 'ocr_skan': 0 uses in 100 sessions
```

---

## 11. Pitfalls of this part

| ID | Pitfall | Symptom | How to avoid |
| :-- | :-- | :-- | :-- |
| **P86** | **Two tools with overlapping descriptions** | The model picks the wrong one at random; the prompt doesn't help | Confusion matrix (§9.3). If you can't say in a sentence when A and when B, merge |
| **P87** | **A raw traceback as a tool result** | The agent sees `Errno 13`, gives up or repeats the same thing | Every exception → WHAT + WHY + WHAT INSTEAD, with a computed hint |
| **P88** | **Tools not filtered by session trust** | A channel session sees `powloka`; an injection gets a shell | Filter in `schemat()`: an untrusted session **does not see** host tools |
| **P89** | **No idempotency with a side effect** | After a timeout the agent sends the message a second time | Mandatory `idempotentne` field; missing = pass through `wykonaj_raz` |
| **P90** | **Constant blast radius instead of computed** | `zmien_nazwy("*")` passes without asking, because "it's just a rename" | `promien` is a function of the arguments, always |

---

## 12. Checkpoint

```bash
cd $OSA
python3 - <<'EOF'
from narzedzia.rejestr import Rejestr
r = Rejestr()
r.dodaj("powloka", "…", {}, lambda: None, zaufanie="host")
r.dodaj("czytaj",  "…", {}, lambda: None, zaufanie="piaskownica")
assert len(r.schemat("piaskownica")) == 1, "P88: trust filter does not work"
assert len(r.schemat("host")) == 2
print("✓ trust filter")
EOF
python3 sesja-cli.py narzedzia archiwista --sprawdz
test -s pomiary/narzedzia/ablacja.csv && echo "✓ ablation done"
git add -A && git commit -m "part 7: tool registry, observations, radius, idempotency"
```

- [ ] The tool description says what it returns and points to the next tool
- [ ] Lenient input (aliases), strict output
- [ ] Observations trimmed keeping both ends, a budget per tool
- [ ] The error has three parts, and the hint is **computed** from state
- [ ] Non-idempotent tools go through the effects registry
- [ ] Blast radius computed from arguments, the consent threshold works
- [ ] Tools filtered by session trust level, **verified by a test**
- [ ] ⭐ **You know your tool-count threshold and have a confusion matrix**

---

**Next: `08-CODE-MODE.md`**: the biggest change of 2026. The agent writes a program
instead of calling tools, and your small model suddenly gets much better.
