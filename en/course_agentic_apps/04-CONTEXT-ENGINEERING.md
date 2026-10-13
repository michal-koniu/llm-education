# Part 4 · Context engineering — the attention budget

**Level:** ⭐⭐⭐⭐ · **Time:** ~5 h · **Requires:** parts 2 and 3
**Produces:** a context manager, a measured degradation curve for your models, compaction that does not lose numbers

---

## 0. Context is not a container. It is an attention budget.

The costliest misunderstanding in working with local models goes like this: *"I have a window of
32k tokens, so I can put in 32k tokens"*.

You cannot. More precisely: you can, but **quality will drop long before the edge of the window**.

Anthropic calls this the **attention budget** and gives the mechanism:

> Models have a finite "attention budget" with diminishing marginal returns. This follows
> from the transformer architecture — **n² pairwise relationships between tokens** — and from the distribution
> of the training data, in which shorter sequences dominate.
> — [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

The practical consequence: **good context is the smallest set of tokens with the highest
signal**, not the largest one that fits.

```
       ANSWER QUALITY as a function of window fill
  100% ┤●●●●●●●●●
       │         ●●●●●●
   75% ┤               ●●●●
       │                   ●●●
   50% ┤                      ●●●
       │                         ●●●●
   25% ┤                             ●●●●●●
       └──┬────┬────┬────┬────┬────┬────┬────
         10%  25%  40%  55%  70%  85% 100%
                            ▲
                    you stop here (§4)
```

⚠️ **The shape of this curve is different for every model and you do not know yours.** That is why the
experiment in §8 is the most important exercise of this part — without it, every threshold
in your system will be a guess.

### 0.1 · Context versus memory — a distinction without which you will merge part 4 with part 5

| | Context (this part) | Memory (part 5) |
| :-- | :-- | :-- |
| Where it lives | in the model window, here and now | on disk, between sessions |
| Lifetime | one turn | months |
| Cost | tokens on every turn | disk space |
| Problem | **too little room** | **too many things to find** |
| Operation | selecting, trimming, summarizing | writing, indexing, searching |

**Context is working memory. Memory is the disk.** Confusing them leads to two typical
mistakes: loading all of memory into context (expensive and harmful) or keeping state
only in context (it dies on restart).

---

## 1. What an agent's context is made of

Break the budget into line items — otherwise it cannot be managed.

```
┌─ system prompt ───────────── 400–2000 tok.   fixed, cacheable
├─ tool definitions ────────── 200–8000 tok.   ⚠️ grows with the number of tools
├─ working files (SOUL etc.) ─ 300–1500 tok.   fixed, cacheable
├─ loaded memory ───────────── 0–3000 tok.     variable
├─ conversation history ────── 0–∞             ⚠️ grows without bound
├─ tool results ────────────── 0–∞             ⚠️⚠️ grows FASTEST
└─ user question ───────────── 10–500 tok.
```

⭐ **The two items with the double warning account for ~80 % of the problems.** A single
`ls -R` in a large directory can drop in 15k tokens and **eat half the window
in one move**. That is why "trimming observations" returns in parts 7 and 8.

### 1.1 · The assembly order matters financially

The prompt cache works on the **prefix**. Everything fixed must be **at the beginning**
and in an unchanging order:

```
✓ [system][tools][working files] │ [memory][history][question]
  └──── fixed, hits the cache ─┘   └── variable ──┘

✗ [system][date and time][tools][…]
                 ▲ a single variable value INVALIDATES THE ENTIRE prefix
```

This is pitfall P46 from course 1 and it returns here because in a multi-agent system it is **easier
to commit**: all it takes is injecting an agent name or a timestamp before the
tool definitions.

---

## 2. The altitude of the system prompt

Anthropic uses the term **"altitude"** — the height from which the prompt describes the task.
Two extreme mistakes:

**Too low — hard logic in the prompt:**

```
If the file has the .pdf extension, use the read_pdf tool. If .txt, use
read_file. If .docx, first convert via libreoffice, then read_file.
If the file is larger than 1 MB, read only the first 100 lines, unless
the user asked for all of it, in which case…
```

**Brittle and does not scale.** Every new case is a new branch; the model will still run into a
situation you did not anticipate, and you have taught it to wait for an instruction.

**Too high — fog:**

```
You are a helpful assistant. Do things well and think about the user.
```

**It assumes a shared context that does not exist.** The model does not know what "well" means to you.

**The right altitude — heuristics plus boundaries:**

```
You read the user's documents and answer questions about them.

Rules:
- Always cite the file and the passage on which you base a claim.
- When you cannot find the answer in the documents — say so directly.
  "It is not in the files searched" is a correct, complete answer.
- Read selectively. Start with headings and the table of contents, the whole thing only when needed.
- Do not guess dates, amounts or names. Either a quotation, or "I did not find it".

You have tools at your disposal — their descriptions say when to use them.
```

> 💡 **The altitude test.** Read the prompt and ask: *would I give this to a new
> colleague on their first day?* If it sounds like a toaster's instruction manual —
> too low. If it sounds like a line from a motivational poster — too high.

### 2.1 · How to write a system prompt so that it does not rot

A method that works and is boring:

1. **Start with the minimum** on the best model you have.
2. **Run the test set** (part 14). Record the failure modes.
3. **Add one sentence** addressing **one** observed mode.
4. **Measure again.** If it did not help — **remove that sentence**.

⚠️ **Step 4 is the one nobody does.** Prompts grow because sentences get added
and never subtracted. After half a year you have 3000 tokens, half of which do nothing or
do harm — and you do not know which half, because you never measured.

---

## 3. Just-in-time loading

Two philosophies of delivering data:

| | Up-front loading | **Just-in-time loading** |
| :-- | :-- | :-- |
| When | everything before the first turn | when the agent asks |
| The agent receives | content | **lightweight identifiers** (paths, names) |
| Cost at 100 files | 200k tokens | ~1k tokens |
| Risk | context rot, cost | an extra turn to fetch |

Anthropic points out that this mirrors human cognition: you do not remember the content of
all your files, you remember the **directory structure** and know where to look.

**Metadata is a signal.** `~/dokumenty/2026/03/faktura-orange.pdf` carries the date,
category and issuer **in 12 tokens**. The content of that file is 800 tokens. An agent that
receives 200 such paths knows a surprising amount about your archive for 2400 tokens.

```python
# Instead of: dump in 100 documents (200,000 tok.)
# Do:         dump in a map (1,200 tok.) + a read(path) tool

def mapa_korpusu(katalog, max_pozycji=200) -> str:
    """A lightweight identifier instead of content."""
    import pathlib
    p = pathlib.Path(katalog)
    linie = []
    for f in sorted(p.rglob("*"))[:max_pozycji]:
        if f.is_file():
            linie.append(f"{f.relative_to(p)}  ({f.stat().st_size // 1024} KB)")
    return "\n".join(linie)
```

> ⚠️ **When up-front loading wins after all.** When the corpus is small (<20k tokens)
> **and fixed**. Then it hits the prompt cache and costs once, while just-in-time loading would cost
> an extra turn every time. The boundary lies where the cost of a turn exceeds the
> cost of holding — compute it for yourself, do not guess.

---

## 4. Compaction — recall first, then precision

When the history has grown and you are approaching the threshold, you have four moves, from the cheapest:

### Move 1 · Clearing tool results (the lightest touch)

The result of `ls -R` from turn 3 is no longer needed in turn 20 — the agent made use of it long ago.
Replace it with a placeholder:

```python
def wyczysc_stare_wyniki(historia, zachowaj_ostatnie=3):
    """The cheapest compaction: tool results older than N lose their content."""
    indeksy = [i for i, w in enumerate(historia) if w.get("rola") == "tool"]
    for i in indeksy[:-zachowaj_ostatnie] if zachowaj_ostatnie else indeksy:
        oryg = len(historia[i]["tresc"])
        historia[i]["tresc"] = f"[result removed from context — {oryg} characters, seq in the journal]"
    return historia
```

⭐ **Always start with this.** In a typical agent session tool results are **50–70 %
of the history**, and their informational value drops practically to zero after 2–3 turns. This is
the best ratio of savings to risk in the whole chapter.

### Move 2 · Deduplication

Did the agent read the same file three times? Keep the last read.

### Move 3 · Summarizing the history

Only when 1 and 2 are not enough. **The order is crucial:**

> Start by maximizing **recall**, then iterate toward **precision**.
> — Anthropic

That means: the first version of the summarizing prompt should **keep too much**. Only
once you see that nothing important is lost do you start trimming. The reverse order — from
terseness toward completeness — guarantees that for the first weeks you will be losing things
and will not know which.

```python
PROMPT_KOMPAKCJI = """Summarize the agent work history below.

KEEP VERBATIM, without paraphrase:
- all numbers, amounts, dates, identifiers, file paths
- decisions that were made, together with the rationale
- errors that occurred, and what fixed them
- what has NOT been done yet

YOU MAY OMIT:
- repetitions and failed attempts that contributed nothing
- full file contents (leave the path and a one-sentence description)
- pleasantries

Format: bullet points. No introduction and no conclusion.

HISTORY:
{historia}"""
```

⚠️ **"KEEP VERBATIM ... numbers" is there for a specific reason** — it is pitfall P31
from course 1. A summarizing model **rounds**. "Processed 3847 files" becomes
"processed almost four thousand files", and in the next turn the agent does not know whether it
has finished. In §8 you will measure how often this happens.

### Move 4 · Closing the session and handoff

When a summary is not enough either — **that is not a compaction problem, it is a signal that the
task is too large for a session**. Use the harness from part 3: save progress, commit, new
session. This is cheaper and safer than a third compaction in a row.

---

## 5. Structured notes — memory outside the context

Instead of keeping everything in the window, the agent **writes notes to a file and reads them when needed**.
Anthropic shows this with the example of Claude playing Pokémon over thousands of steps.

For you this is the `POSTEP.md` from part 3 — but it can be formalized as a tool:

```python
def narzedzie_notatka(akcja: str, klucz: str, tresc: str = "") -> str:
    """The agent's notebook. Outside the context, persistent between turns."""
    import os, pathlib, json
    p = pathlib.Path(os.environ["OSA"], "notatnik.json")
    d = json.loads(p.read_text()) if p.exists() else {}
    if akcja == "zapisz":
        d[klucz] = tresc
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2))
        return f"saved '{klucz}' ({len(tresc)} characters)"
    if akcja == "czytaj":
        return d.get(klucz, f"no note '{klucz}'")
    if akcja == "lista":
        return "\n".join(f"{k} ({len(v)} ch.)" for k, v in d.items()) or "notebook empty"
    return "action: zapisz | czytaj | lista"
```

⭐ **The key difference from the memory in part 5:** the notebook is **explicitly driven by
the agent** and scoped to the task. The memory from part 5 is automatic and persistent.
The notebook is scratch paper; memory is the archive.

---

## 6. FROM SCRATCH — the context manager

```python
# $OSA/kontekst.py
"""Context budgeting: count, trim, compact — in that order."""
import json

class Budzet:
    def __init__(self, okno: int, licz_tokeny, prog_kompakcji=0.70, prog_twardy=0.85):
        self.okno, self.licz = okno, licz_tokeny
        self.prog_k, self.prog_t = prog_kompakcji, prog_twardy

    def rozbicie(self, czesci: dict) -> dict:
        """How much each budget item eats. Without this nothing can be optimized."""
        r = {k: self.licz(v) for k, v in czesci.items()}
        r["_razem"] = sum(r.values())
        r["_zapelnienie"] = round(r["_razem"] / self.okno, 3)
        return r

    def stan(self, razem: int) -> str:
        z = razem / self.okno
        if z >= self.prog_t: return "twardy"      # compact NOW
        if z >= self.prog_k: return "ostrzezenie" # plan a compaction
        return "ok"

def przytnij_obserwacje(tresc: str, limit_znakow=2000) -> str:
    """P40 from course 1: a single observation must not eat the window.
    Keeps the BEGINNING and the END — the middle is usually the least relevant."""
    if len(tresc) <= limit_znakow:
        return tresc
    pol = limit_znakow // 2
    ucieto = len(tresc) - limit_znakow
    return (tresc[:pol] + f"\n\n[… cut {ucieto} characters — "
            f"use the tool with a narrower query if you need the middle …]\n\n"
            + tresc[-pol:])

def kompaktuj(historia: list, wywolaj_model, zachowaj_ostatnie=4) -> tuple[list, dict]:
    """Move 1 → 2 → 3. Returns the new history and a savings report."""
    przed = sum(len(json.dumps(w, ensure_ascii=False)) for w in historia)

    # Move 1 — clearing old tool results
    idx = [i for i, w in enumerate(historia) if w.get("rola") == "tool"]
    for i in idx[:-2] if len(idx) > 2 else []:
        historia[i]["tresc"] = f"[result removed — {len(historia[i]['tresc'])} characters]"

    po_r1 = sum(len(json.dumps(w, ensure_ascii=False)) for w in historia)
    if po_r1 < przed * 0.6:                        # that was enough
        return historia, {"ruch": 1, "przed": przed, "po": po_r1}

    # Move 3 — summarizing everything except the tail
    glowa, ogon = historia[:-zachowaj_ostatnie], historia[-zachowaj_ostatnie:]
    streszczenie = wywolaj_model([{"rola": "user", "tresc": PROMPT_KOMPAKCJI.format(
        historia=json.dumps(glowa, ensure_ascii=False, indent=1))}])["tresc"]

    nowa = [{"rola": "system", "tresc": "SUMMARY OF EARLIER WORK:\n" + streszczenie}] + ogon
    po = sum(len(json.dumps(w, ensure_ascii=False)) for w in nowa)
    return nowa, {"ruch": 3, "przed": przed, "po": po, "streszczenie": streszczenie}
```

**Hook this into the journal from part 2** — compaction must leave a trace:

```python
d.dopisz("kompakcja", od_seq=pierwszy, do_seq=ostatni,
         streszczenie=raport["streszczenie"], zachowaj_ostatnie=4,
         znakow_przed=raport["przed"], znakow_po=raport["po"])
```

⭐ **Thanks to this, in part 15 you will answer the question "what did the agent see in turn 40",
even if it compacted that in turn 60.** The original never disappears from the file.

---

## 7. IN PRODUCTION — what others do

| Mechanism | Claude Agent SDK | LangGraph | **Yours** |
| :-- | :-- | :-- | :-- |
| Automatic compaction | ⭐ built in, at a threshold | ✗ | threshold + 3 moves |
| Clearing tool results | ⭐ `context editing` | ✗ | move 1 |
| Awareness of the remaining budget | ⭐ the model sees it | ✗ | `Budzet.stan()` |
| Notes outside the context | ⭐ `memory` tool | store | notebook |
| **Breaking the budget into items** | ✗ | ✗ | ⭐ `rozbicie()` |
| **Compaction trace in the journal** | partially | ✗ | ⭐ event |

> 💡 **One thing worth copying from Anthropic: tell the model how much it has left.**
> A model that knows it has 20 % of the window behaves differently — it starts summarizing
> and wrapping up instead of opening new threads. It costs 15 tokens in the prompt:
>
> ```
> Remaining context budget: ~22 %. Aim to wrap up the current item.
> ```

---

## 8. EXPERIMENT 4 — measure the degradation curve of your models

⭐ **This is the most important measurement in the whole course.** Every threshold in your system
(when to compact, when to close a session, how many tools to show) rests on this
single curve — and it is different for every model.

**Hypothesis:** accuracy drops nonlinearly with window fill, and the breaking point
lies **significantly below** the declared context length.

### 8.1 · The test task — two types, because they measure different things

```bash
mkdir -p $OSA/pomiary/kontekst && cd $OSA/pomiary/kontekst
cd ~/Desktop/github_repos/llm-education   # the repository directory (yours may differ)
source rig-env.sh
```

```python
# generuj.py — builds sets with increasing fill
import random, json, pathlib
random.seed(7)

WYPELNIACZ = ("Minutes of the community meeting. The technical condition of the building "
              "and the renovation plan were discussed. The report was approved. ")

def zestaw(zapelnienie_tok: int, typ: str) -> dict:
    """typ='igla' — retrieving a fact. typ='synteza' — combining 3 facts."""
    fakty = {
        "igla":    [("The boiler room access code is 7741.", "What is the boiler room code?", "7741")],
        "synteza": [("Advance payment in January: PLN 420.", None, None),
                    ("In March the advance payment was raised by PLN 85.", None, None),
                    ("From July a discount of PLN 30 applies.", 
                     "What is the advance payment from July?", "475")],
    }[typ]
    wypelniacz_n = max(1, zapelnienie_tok * 4 // len(WYPELNIACZ))
    bloki = [WYPELNIACZ] * wypelniacz_n
    # scatter the facts evenly — NOT all at the beginning
    for i, (f, _, _) in enumerate(fakty):
        bloki.insert(len(bloki) * (i + 1) // (len(fakty) + 1), f + " ")
    pytanie = [p for _, p, _ in fakty if p][0]
    odp     = [o for _, _, o in fakty if o][0]
    return {"kontekst": "".join(bloki), "pytanie": pytanie, "oczekiwane": odp}

if __name__ == "__main__":
    out = []
    for zap in (1000, 2000, 4000, 8000, 12000, 16000, 24000, 32000):
        for typ in ("igla", "synteza"):
            for powt in range(5):                    # 5 repetitions — P61
                z = zestaw(zap, typ)
                z.update(zapelnienie=zap, typ=typ, powt=powt)
                out.append(z)
    pathlib.Path("zestawy.jsonl").write_text(
        "\n".join(json.dumps(z, ensure_ascii=False) for z in out), encoding="utf-8")
    print(f"{len(out)} sets")
```

### 8.2 · Running it

```bash
python3 generuj.py
$LB/llama-server -m $OSS20 -c 32768 -ngl 99 --port 8080 --host 127.0.0.1 &
sleep 20
python3 zmierz.py --model gpt-oss-20b > wyniki-oss20.csv
# repeat for $QWEN32 and $BIELIK
```

```python
# zmierz.py
import json, sys, time, urllib.request

def pytaj(kontekst, pytanie):
    ciało = json.dumps({
        "messages": [{"role": "user",
                      "content": f"{kontekst}\n\nQuestion: {pytanie}\nAnswer with the number only."}],
        "temperature": 0, "max_tokens": 32,
    }).encode()
    r = urllib.request.Request("http://127.0.0.1:8080/v1/chat/completions", ciało,
                               {"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(r, timeout=300) as o:
        d = json.load(o)
    return (d["choices"][0]["message"]["content"].strip(),
            d["usage"]["prompt_tokens"], round(time.time() - t0, 2))

print("model,zapelnienie,typ,powt,tokeny,ms,trafne,odpowiedz")
model = sys.argv[2]
for linia in open("zestawy.jsonl", encoding="utf-8"):
    z = json.loads(linia)
    odp, tok, sek = pytaj(z["kontekst"], z["pytanie"])
    trafne = int(z["oczekiwane"] in odp)
    print(f'{model},{z["zapelnienie"]},{z["typ"]},{z["powt"]},{tok},{sek},{trafne},"{odp[:40]}"')
```

### 8.3 · The table to fill in

| Fill | `gpt-oss-20b` needle | `gpt-oss-20b` synthesis | `qwen3-32b` needle | `qwen3-32b` synthesis |
| --: | --: | --: | --: | --: |
| 1,000 | /5 | /5 | /5 | /5 |
| 2,000 | | | | |
| 4,000 | | | | |
| 8,000 | | | | |
| 12,000 | | | | |
| 16,000 | | | | |
| 24,000 | | | | |
| 32,000 | | | | |

### 8.4 · What to read from this

**Three numbers that you will extract and put into the configuration:**

1. **The needle breaking point** — where retrieval accuracy drops below 90 %.
2. **The synthesis breaking point** — the same for combining facts. ⚠️ **It will be considerably
   earlier** — usually 2–3× — because synthesis requires simultaneous attention to many places.
3. **The compaction threshold** = 80 % of the **synthesis** breaking point, not the needle's.

```bash
# put the result into the configuration
python3 - <<'EOF'
import json, pathlib
p = pathlib.Path.home() / "os-agenta/konfiguracja/system.json"
k = json.loads(p.read_text())
k["kontekst"] = {
    "gpt-oss-20b": {"okno": 32768, "zalamanie_igla": 0, "zalamanie_synteza": 0, "prog_kompakcji": 0},
    "qwen3-32b":   {"okno": 32768, "zalamanie_igla": 0, "zalamanie_synteza": 0, "prog_kompakcji": 0},
}
p.write_text(json.dumps(k, indent=2, ensure_ascii=False))
print("replace the zeros with the measured values")
EOF
```

⚠️ **Prediction to verify:** the needle will hold up for a long time — models are trained for
retrieval and "needle in a haystack" is easy. **Synthesis will break down much earlier**,
probably around 40–60 % of the window. Because your agent does synthesis (reads a tool
result, combines it with the goal, decides), **it is the second curve that is your real limit** —
and that is why you must not trust the declared context length.

### 8.5 · An additional experiment — does compaction lose numbers

```bash
# Take 20 real sessions from the journal, compact them, check number preservation
python3 - <<'EOF'
import re, json, pathlib
def liczby(t): return set(re.findall(r'\b\d[\d\s.,]{2,}\b', t))
# for each session: numbers(original) - numbers(summary) = numbers LOST
EOF
```

Note the **percentage of numbers lost in compaction**. If it exceeds 5 % — strengthen the
"KEEP VERBATIM" section in the prompt and measure again. This is pitfall P31 from course 1
and the only way to know whether it affects you.

---

## 9. EXERCISE — hook the budget into the gate

Extend the gate from part 2 so that on every turn it:

1. Computes the **budget breakdown** into items and appends it as a `budzet` event.
2. Injects into the prompt a line about the remaining budget when it falls below 40 %.
3. Triggers compaction automatically at the threshold **measured in §8**.
4. Refuses to start a turn when the system prompt + tools alone exceed 50 % of the window
   (which means you have too many tools — see part 7).

```bash
python3 sesja-cli.py budzet main
# expect:
#   systemowy       412  ( 1.3%)
#   narzedzia      3180  ( 9.7%)
#   pliki_robocze   890  ( 2.7%)
#   historia      11240  (34.3%)
#   wyniki         8100  (24.7%)
#   ─────────────────────────────
#   razem         23822  (72.7%)  ← state: ostrzezenie
```

> 💡 **This breakdown is the diagnostic you will return to most often.** When the agent
> starts behaving strangely, the first question is "what ate the context" — and here
> you have the answer in one command.

---

## 10. Pitfalls of this part

| ID | Pitfall | Symptom | How to avoid |
| :-- | :-- | :-- | :-- |
| **P72** | **Trusting the declared context length** | The model "supports 128k", yet gets things wrong from 30k | Measure **your own** curve (§8). The limit is synthesis, not the needle |
| **P73** | **A variable value before a fixed prefix** | The prompt cache never hits, TTFT constantly high | Date, agent name, counter — **always after** the tools and working files |
| **P74** | **Compacting straight away, without moves 1 and 2** | You lose details although clearing old tool results would have been enough | The order 1 → 2 → 3 → closing the session |
| **P75** | **The summary rounds numbers** | "almost four thousand files" instead of 3847; the agent does not know whether it has finished | "KEEP VERBATIM" + the measurement from §8.5 |
| **P76** | **The system prompt grows and never shrinks** | After half a year 3000 tokens, half of them do nothing | You measure every added sentence; did not help → **you remove it** |

---

## 11. Checkpoint

```bash
cd $OSA
python3 -c "from kontekst import Budzet, przytnij_obserwacje, kompaktuj; print('✓ import')"
test -s pomiary/kontekst/wyniki-oss20.csv && echo "✓ curve measured"
python3 -c "
import json,pathlib
k=json.loads((pathlib.Path.home()/'os-agenta/konfiguracja/system.json').read_text())
assert k['kontekst']['gpt-oss-20b']['prog_kompakcji']>0, 'threshold not set'
print('✓ threshold from measurement in the configuration')"
git add -A && git commit -m "part 4: context budget, compaction, degradation curve"
```

- [ ] You understand the difference: context = working memory, memory = disk
- [ ] You can break the budget into items and know which one grows fastest
- [ ] The system prompt has the right altitude and **you measure every added sentence**
- [ ] You use just-in-time loading instead of up-front loading
- [ ] You compact in the order 1 → 2 → 3, not straight to a summary
- [ ] Compaction leaves a trace in the journal; the original never disappears
- [ ] ⭐ **You have a measured degradation curve for both models and the threshold entered in the configuration**

---

**Next: `05-LONG-TERM-MEMORY.md`** — three schools of agent memory and a bi-temporal
graph that knows **when** something was true.
