# Part 8 · Code-mode — the agent writes a program instead of calling tools

**Level:** ⭐⭐⭐⭐⭐ · **Time:** ~6 h · **Requires:** part 7 (tools), course 1 part 7 (`bwrap`)
**Produces:** a code execution environment, a tool API, a comparison of both modes in numbers

> ⭐ **Alongside part 3, this is the most important part of the course, and the one that
> benefits you in particular.** I explain the reason in §2, and it is surprisingly
> simple.

---

## 1. A problem you cannot see until you measure it

The task: *"For each March invoice, check whether it has been paid, and list the unpaid
ones with the total."*

**Classic mode: one tool call per turn:**

```
turn  1  znajdz_dokumenty("faktury/2026/03")   → list of 23 files      [1,200 tok.]
turn  2  czytaj_dokument("…/f001.pdf")          → content               [  800 tok.]
turn  3  czytaj_dokument("…/f002.pdf")          → content               [  800 tok.]
   …
turn 24  czytaj_dokument("…/f023.pdf")          → content               [  800 tok.]
turn 25  the model adds up in its head                                  [   -- ]

TOTAL:  25 turns · ~24,000 tokens · ~90 s
RISK:   0.92²⁴ = 13% chance that the whole chain passes without an error
```

**Code-mode: one program:**

```
turn 1   the model writes:

         faktury = znajdz("faktury/2026/03")
         nieoplacone = []
         for f in faktury:
             t = czytaj(f)
             if "opłacono" not in t.lower():
                 nieoplacone.append((f, kwota(t)))
         print(f"{len(nieoplacone)} unpaid, total {sum(k for _, k in nieoplacone)} PLN")
         for f, k in nieoplacone: print(f"  {f}: {k} PLN")

turn 2   result: "3 unpaid, total 4,820 PLN / f007.pdf: 1200 PLN / …"   [120 tok.]

TOTAL:  2 turns · ~1,400 tokens · ~12 s
RISK:   0.92² = 85%
```

**Seventeen times fewer tokens. Six times faster. A six times higher chance of
success.**

Published context reductions for code-mode fall in the range of **85–94%**
([MCP Code Mode](https://medium.com/@amirkiarafiei/mcp-code-mode-context-engineering-for-efficient-tool-execution-in-llm-agents-c46e1ddf80ac)),
and smolagents reports **~30% fewer model calls**. ⚠️ **You will measure this yourself
in §8**, and there the number will mean something real.

### 1.1 · Where the saving comes from

Three independent mechanisms, and it is worth telling them apart:

| Mechanism | What it saves |
| :-- | :-- |
| **The loop runs in code, not in the model** | 23 turns × the full history = the main item |
| **Intermediate data does not enter the context** | 23 × 800 tokens of invoice content: the model sees only the result |
| **Tool schemas replaced by an API** | the model knows Python; there is no need to describe every tool in the prompt |

⭐ **The second mechanism is the strongest and the most often overlooked.** In classic
mode **every byte read by a tool passes through the context window**. In code-mode the
data stays in the process, and the model gets the result. This is a qualitative
difference, not a quantitative one: it lets you process 500 files, which in classic mode
**cannot be done at all**, regardless of patience.

---

## 2. Why this matters more for you than for others

Here is an observation worth remembering:

> **A small local model writes correct Python much more reliably than it emits long,
> correct JSON with nested arguments.**

The reason is in the training data. There is **orders of magnitude more** Python code in
the corpus than function calls in a given provider's JSON format. The model has seen
millions of `for` loops and a few tens of thousands of tool-calling schemas, if any.

The consequences are concrete:

| | JSON mode | Code-mode |
| :-- | :-- | :-- |
| Format in which the model is weak | ⚠️ long JSON with nesting | — |
| Format in which the model is strong | — | ⭐ Python |
| Syntax error | breaks the whole call | ⭐ **visible in the traceback, can be fixed** |
| Enforcing structure | GBNF grammar (10–30% slower) | ⭐ **unnecessary** |
| A loop over 20 elements | 20 turns | ⭐ 3 lines |
| An "if X then Y" condition | 2 turns | ⭐ 1 line |

⭐ **Code-mode shifts the burden from a format in which your model is weak to a format in
which it is strong.** For `gpt-oss-20b` this is not an optimization: it changes the
class of tasks that can be executed at all.

> ⚠️ **The price you pay is real and unavoidable: you need a sandbox.** A model that
> writes and runs arbitrary code **is exactly what ASI05 warns about** (Unexpected Code
> Execution). Without part 10, code-mode is remote code execution with a polite
> interface. This part assumes `bwrap` from course 1 as the minimum and **requires**
> part 10 before you let anything from the network in here.

---

## 3. Architecture

```
┌─ MODEL ─────────────────────────────────────────┐
│  receives: prompt + tool API (abridged)         │
│  returns:  a block of Python code               │
└──────────────────┬──────────────────────────────┘
                   │  code
┌──────────────────▼──────────────────────────────┐
│  SANDBOX (bwrap / container)                    │
│  ┌────────────────────────────────────────────┐ │
│  │ narzedzia.py  ← same functions as in pt. 7 │ │
│  │ agent code    ← executed here              │ │
│  └────────────────────────────────────────────┘ │
│  no network · only /tmp/praca writable          │
│  limit: 30 s CPU, 512 MB RAM, 200 MB disk       │
└──────────────────┬──────────────────────────────┘
                   │  stdout + stderr (TRIMMED)
┌──────────────────▼──────────────────────────────┐
│  MODEL sees the result                          │
└─────────────────────────────────────────────────┘
```

**The key decision: the tools are the same functions as in part 7.** You do not build a
second set. The registry exposes them in two ways, as JSON schemas (classic mode) and as
a Python module (code-mode), and the logic, limits and blast radius are shared.

---

## 4. FROM SCRATCH: the tool API inside the sandbox

```python
# $OSA/kod/narzedzia_api.py
"""The API seen by the agent's code. A thin layer over the registry from part 7.

Every function has a docstring: this is ALL the documentation the model will get.
Write them like tool descriptions: what it returns, edge behaviour, an example."""
import os, json, pathlib

KORZEN = pathlib.Path(os.environ["OSA_KORZEN"])     # set by the sandbox
_LICZNIK = {"wywolan": 0, "bajtow": 0}
_LIMIT_WYWOLAN = 500                                 # P93

def _licz(bajtow=0):
    _LICZNIK["wywolan"] += 1
    _LICZNIK["bajtow"] += bajtow
    if _LICZNIK["wywolan"] > _LIMIT_WYWOLAN:
        raise RuntimeError(
            f"Limit of {_LIMIT_WYWOLAN} tool calls in a single program exceeded. "
            f"Narrow the scope or split it into stages.")

def znajdz(wzorzec: str, limit: int = 200) -> list[str]:
    """Finds documents matching a pattern (glob) relative to the archive.

    Returns a sorted list of relative paths. At most `limit` entries.
    Example: znajdz("faktury/2026/03/*.pdf") -> ["faktury/2026/03/f001.pdf", ...]
    When nothing matches, it returns an empty list (not an error)."""
    _licz()
    return sorted(str(p.relative_to(KORZEN)) for p in KORZEN.glob(wzorzec))[:limit]

def czytaj(sciezka: str, max_znakow: int = 200_000) -> str:
    """Reads a document (txt/md/pdf) and returns the content as text.

    A PDF is converted automatically. For a document longer than `max_znakow`
    it returns the beginning; the rest is cut off with a note.
    Raises FileNotFoundError with a list of neighbours when the file does not exist."""
    p = (KORZEN / sciezka).resolve()
    if not str(p).startswith(str(KORZEN)):            # P92
        raise PermissionError(f"Path outside the archive: {sciezka}")
    if not p.exists():
        sasiedzi = [x.name for x in p.parent.glob("*")][:8] if p.parent.exists() else []
        raise FileNotFoundError(f"There is no '{sciezka}'. In the directory: {sasiedzi}")
    t = _do_tekstu(p)
    _licz(len(t))
    return t[:max_znakow]

def kwota(tekst: str) -> float | None:
    """Extracts the 'amount due' / 'total' from invoice text.

    Returns a number in PLN or None when nothing was found.
    It does NOT guess: no match means None, not 0."""
    import re
    m = re.search(r"(?:do zapłaty|razem|suma)[^\d]{0,20}([\d\s]+[,.]\d{2})",
                  tekst, re.I)
    return float(m.group(1).replace(" ", "").replace(",", ".")) if m else None

def zapisz_wynik(nazwa: str, tresc: str) -> str:
    """Saves the work result to /tmp/praca/<nazwa>. The only place to write.

    Returns the path. Use this instead of open(), otherwise the write will be blocked."""
    p = pathlib.Path("/tmp/praca") / nazwa
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(tresc, encoding="utf-8")
    _licz(len(tresc))
    return str(p)

def pomoc() -> str:
    """Prints all available functions with descriptions."""
    import inspect, sys
    m = sys.modules[__name__]
    return "\n\n".join(
        f"{n}{inspect.signature(f)}\n    {inspect.getdoc(f)}"
        for n, f in vars(m).items()
        if callable(f) and not n.startswith("_") and inspect.getdoc(f))
```

⭐ **`pomoc()` realizes Steinberger's thesis from part 1 in miniature.** Instead of
putting the schemas of all tools into the prompt (8k tokens in every turn), you give the
model **one line**: *"you have a `narzedzia` module; call `pomoc()` if you don't know
something"*. The model pays for documentation **only when it needs it**, and this is
exactly what he describes as "a CLI costs nothing, because the model will read
`--help`".

---

## 5. Running the code

```python
# $OSA/kod/wykonanie.py
"""Running the agent's code in a sandbox. Full isolation: part 10."""
import subprocess, pathlib, textwrap, os, shutil

SZABLON = '''
import sys, traceback
sys.path.insert(0, "/opt/osa")
from narzedzia_api import *          # noqa

try:
{kod}
except Exception:
    print("\\n--- EXECUTION ERROR ---", file=sys.stderr)
    traceback.print_exc(limit=3)     # P91: the model MUST see the traceback
    sys.exit(1)
'''

def uruchom(kod: str, korzen_archiwum: str, limit_s=30, limit_wyjscia=4000) -> dict:
    praca = pathlib.Path("/tmp/praca"); shutil.rmtree(praca, ignore_errors=True)
    praca.mkdir(parents=True)
    skrypt = praca / "_program.py"
    skrypt.write_text(SZABLON.format(kod=textwrap.indent(kod, "    ")), encoding="utf-8")

    cmd = [
        "sudo", "bwrap",                              # see the AppArmor note below the code
        "--unshare-all",                              # no network, no host PID
        "--die-with-parent", "--new-session",         # P44 from course 1
        "--ro-bind", "/usr", "/usr", "--ro-bind", "/lib", "/lib",
        "--ro-bind", "/lib64", "/lib64", "--ro-bind", "/bin", "/bin",
        "--ro-bind", str(pathlib.Path.home() / "os-agenta/kod"), "/opt/osa",
        "--ro-bind", korzen_archiwum, "/archiwum",    # ⭐ archive READ-ONLY
        "--bind", str(praca), "/tmp/praca",           # the only place to write
        "--proc", "/proc", "--dev", "/dev",
        "--setenv", "OSA_KORZEN", "/archiwum",
        "--setenv", "HOME", "/tmp/praca",
        "--chdir", "/tmp/praca",
        "python3", "/tmp/praca/_program.py",
    ]
    try:
        w = subprocess.run(cmd, capture_output=True, text=True, timeout=limit_s)
        kod_wy, out, err = w.returncode, w.stdout, w.stderr
    except subprocess.TimeoutExpired:
        kod_wy, out, err = 124, "", (
            f"TIMEOUT ({limit_s} s). The program was aborted.\n"
            f"Split the work into smaller batches or narrow the scope.")

    return {
        "kod_wyjscia": kod_wy,
        "wyjscie": _przytnij(out, limit_wyjscia),
        "blad":    _przytnij(err, 1500),
        "pliki":   [p.name for p in praca.glob("*") if p.name != "_program.py"],
    }

def _przytnij(t, limit):
    if len(t) <= limit: return t
    p = limit // 2
    return t[:p] + f"\n[… {len(t)-limit} characters cut …]\n" + t[-p:]
```

**Four decisions worth justifying:**

1. **`--unshare-all`**: the agent's code **has no network**. Even the Researcher does not
   get a network inside `exec`; downloading is done by a separate, controlled tool
   (part 10).
2. **The archive is mounted `--ro-bind`**: even buggy code will not destroy the
   documents. Writing only to `/tmp/praca`.
3. **The traceback goes back to the model**, trimmed to 3 frames. This is its main
   feedback channel and it **must not be swallowed**.
4. **A list of files in the result**: the model knows what it produced without reading
   the directory.

⚠️ **`sudo` in `cmd` is necessary here on this machine, but unlike in a shell script,
this is an AUTOMATIC call, with no human at the keyboard.** Ubuntu 24.04 blocks
`--unshare-all`/`--unshare-net` for unprivileged processes (there is no AppArmor profile
for `bubblewrap` in this release; full diagnosis: course 1,
`07-SANDBOX-SECURITY-MONITORING.md`, §2). An interactive `sudo bwrap` typed by hand in a
terminal simply asks for a password. **This code cannot do that**: it is called
repeatedly, in a loop, with nobody there to type the password.

Before you run it in the agent loop, do one of two things:

```bash
# Option A (faster, narrower): passwordless sudo ONLY for bwrap, for your user
echo "$(whoami) ALL=(root) NOPASSWD: /usr/bin/bwrap" | sudo tee /etc/sudoers.d/bwrap-osa
sudo chmod 440 /etc/sudoers.d/bwrap-osa
sudo visudo -c        # ⭐ always check the syntax BEFORE logging out
```

```bash
# Option B (cleaner, but outside the scope of this course): install a proper
# AppArmor profile for /usr/bin/bwrap, instead of working around the restrictions via sudo.
# Search for: "apparmor bubblewrap unprivileged_userns ubuntu 24.04".
```

**Option A is narrower than it looks.** `NOPASSWD` applies only to launching
`/usr/bin/bwrap` itself; it does not give general passwordless root. What `bwrap` can do
INSIDE the sandbox is still restricted by everything else in this part (`--ro-bind`,
`--unshare-all`, no network). Without one of these two options, `subprocess.run()` with
`sudo` in the agent loop **will hang on a password prompt** that nobody will type, until
the `timeout`.

---

## 6. The prompt for code-mode

```python
PROMPT_CODE_MODE = """You have Python and a tools module at your disposal.
Instead of calling tools one at a time, WRITE A PROGRAM that does the whole job.

Available functions (full descriptions: call `print(pomoc())`):
{skrot_api}

Rules:
1. Return ONLY a Python code block in ```python … ```. No commentary before or after.
2. Output the result with `print()`. It is the only thing you will see.
3. Print CONCISELY: summaries and numbers, not the raw content of documents.
   Your `print` goes into the context and costs tokens.
4. For large sets, print progress every N elements, so that an interruption
   can be diagnosed.
5. You have 30 s and 500 tool calls. For bigger jobs, split into stages
   and save intermediate state through `zapisz_wynik()`.
6. When you don't know something about the API, run `print(pomoc())` in a separate,
   short program.

Task: {zadanie}"""

SKROT_API = """znajdz(wzorzec, limit=200) -> list[str]
czytaj(sciezka, max_znakow=200000) -> str
kwota(tekst) -> float | None
zapisz_wynik(nazwa, tresc) -> str
pomoc() -> str"""
```

⭐ **Rule 3 is the one models break most often.** The model will write
`for f in faktury: print(czytaj(f))` and **dump 24k tokens into the context**, exactly
what code-mode was supposed to protect against. You enforce this in two ways: a rule in
the prompt **and** a hard `limit_wyjscia` in `uruchom()`. The rule alone is not enough.

---

## 7. When code-mode loses

An honest list, because this is not a solution to everything.

| Situation | Why it loses | What to do |
| :-- | :-- | :-- |
| **A single simple call** | the overhead of writing a program > the saving | classic mode |
| **An irreversible operation** | code is harder to review than a single call | ⭐ classic + confirmation |
| **No sandbox** | ASI05: execution of arbitrary code | ⭐⭐ **don't use it at all** |
| **The model writes code poorly** | ⚠️ measure; below ~7B it can go badly | classic or a bigger model |
| **An interactive task** | a program won't ask the user halfway through | classic |
| **Debugging the agent's behaviour** | the reasoning is harder to trace | classic for diagnosis |

### 7.1 · Hybrid mode: recommended

**Don't pick one. Expose both and let the model decide**, or decide yourself with a
rule:

```python
def wybierz_tryb(zadanie: str, narzedzia_dostepne: int) -> str:
    sygnaly_petli = ("każd", "wszystk", "dla listy", "porówn", "zsumuj",
                     "ile łącznie", "przejdź przez", "dla wszystkich")
    if any(s in zadanie.lower() for s in sygnaly_petli):
        return "code"
    if narzedzia_dostepne > 25:              # part 7, strategy C
        return "code"
    return "klasyczny"
```

⭐ **A rule based on loop signals catches most cases and costs nothing.** Before you
build a router trained on data, measure how far you get with eight keywords.

---

## 8. EXPERIMENT 8: the same task by two routes

⭐ **The most important measurement of this part. Don't take other people's 85–94% on
faith.**

### 8.1 · Setup

```bash
mkdir -p $OSA/pomiary/codemode && cd $OSA/pomiary/codemode
python3 - <<'EOF'
import random, pathlib
random.seed(11)
kat = pathlib.Path("archiwum/faktury/2026/03"); kat.mkdir(parents=True, exist_ok=True)
for i in range(1, 41):
    oplacona = random.random() < 0.7
    kwota = round(random.uniform(80, 3200), 2)
    tresc = (f"FAKTURA VAT nr FV/{i:03d}/03/2026\n"
             f"Data wystawienia: 2026-03-{random.randint(1,28):02d}\n"
             f"Kontrahent: Firma {random.choice('ABCDEFGH')}\n"
             + "pozycja rozliczeniowa\n" * random.randint(15, 60) +
             f"\nRazem do zapłaty: {kwota:.2f} PLN\n"
             + ("Opłacono przelewem\n" if oplacona else ""))
    (kat / f"f{i:03d}.txt").write_text(tresc, encoding="utf-8")
print("40 invoices ready")
EOF
```

### 8.2 · Five tasks of increasing complexity

| # | Task | Expected winner |
| :-- | :-- | :-- |
| Z1 | "How many invoices are there in March?" | classic (1 call) |
| Z2 | "What is the amount of invoice FV/007/03/2026?" | tie |
| Z3 | "Which invoices are unpaid?" | code-mode |
| Z4 | "Total of the unpaid ones + a list in descending order" | ⭐ code-mode |
| Z5 | "For each counterparty: count, total, % paid, sorted" | ⭐⭐ code-mode |

### 8.3 · Results table: 3 runs each

| Task | Mode | Turns | Tokens in | Tokens out | Time | Correct /3 |
| :-- | :-- | --: | --: | --: | --: | --: |
| Z1 | classic | | | | | |
| Z1 | code | | | | | |
| Z2 | classic | | | | | |
| … | | | | | | |
| Z5 | classic | | | | | |
| Z5 | code | | | | | |

### 8.4 · Repeat on both models

This is the part that will give you the decision for the router from part 17:

| Model | Z5 classic | Z5 code | Code syntactically correct on the 1st try |
| :-- | --: | --: | --: |
| `gpt-oss-20b` | /3 | /3 | /3 |
| `qwen3-32b` | /3 | /3 | /3 |

⚠️ **Prediction to check:**

- Z1–Z2: classic wins or ties. **Code-mode is not free**: writing a program costs output
  tokens.
- Z3–Z5: code-mode wins more and more clearly; at Z5 I expect that **classic will not
  finish at all** within the turn limit.
- The biggest unknown is the last column. If `gpt-oss-20b` writes syntactically correct
  code in fewer than 2/3 of cases, you need the repair loop from §9.

### 8.5 · An additional measurement: is the code safe

```bash
python3 audyt_kodu.py --z-dziennika 100
# count how many generated programs tried:
#   - open() outside /tmp/praca
#   - import socket / urllib / requests
#   - subprocess / os.system
#   - reading from outside /archiwum
```

⭐ **This measurement is more important than it seems.** Not because the model is
malicious, but because **the number of attempts shows how much you depend on the
sandbox**. If 12% of programs try to write outside `/tmp/praca`, it means that without
`bwrap` you would have 12% of programs doing something you did not consent to.

---

## 9. The repair loop: code that does not compile

```python
def uruchom_z_naprawa(kod, korzen, wywolaj_model, max_prob=3) -> dict:
    """A syntax or execution error → the model gets the traceback and fixes it."""
    historia = []
    for proba in range(1, max_prob + 1):
        w = uruchom(kod, korzen)
        if w["kod_wyjscia"] == 0:
            return {**w, "prob": proba}
        historia.append({"kod": kod, "blad": w["blad"]})
        if proba == max_prob:
            return {**w, "prob": proba, "poddano_sie": True}
        kod = _wyciagnij_kod(wywolaj_model([{"rola": "user", "tresc":
            f"This program failed to run.\n\nCODE:\n```python\n{kod}\n```\n\n"
            f"ERROR:\n{w['blad']}\n\n"
            f"Fix it. Return ONLY the fixed code in a ```python block.\n"
            f"If the error comes from missing permissions, don't work around it, "
            f"do it differently in an allowed way."}])["tresc"])
    return w
```

⚠️ **The sentence "don't work around it, do it differently" is necessary.** A model that
gets a `PermissionError` tries a **workaround** by default: another path, through
`subprocess`, through `/proc`. The sandbox will stop it, but you will waste three
attempts. Tell it directly what reaction is expected.

> 💡 **How many attempts.** Three. If the model does not fix the code in three tries, a
> fourth will not help either. That is a signal to escalate to a stronger model (the
> ladder from part 3, rung 4), not to try again.

---

## 10. IN PRODUCTION

| | smolagents | MS Agent Framework CodeAct | `code-mode` (UTCP) | **Yours** |
| :-- | :-- | :-- | :-- | :-- |
| Language | Python | C#/Python | TS/Python | Python |
| Sandbox | ⭐ built-in (E2B/local) | containers | configurable | ⭐ `bwrap` locally |
| Tools as an API | ⭐ yes | ⭐ yes | ⭐ yes | ⭐ yes |
| Offline | ⚠️ depends on the sandbox | ✗ cloud | partially | ⭐ **full** |
| Repair loop | ⭐ yes | yes | yes | ⭐ yes |
| Tool call limit | ✗ | ✗ | ✗ | ⭐ yes |
| Audit of generated code | ✗ | partially | ✗ | ⭐ §8.5 |

**smolagents is the closest ready-made implementation of what you have built.** It is
worth reading its code after this part, because you will recognize every decision. The
main reason to stay with your own: **the sandbox is yours and offline**, while in
smolagents it is configurable and by default points at an external service.

---

## 11. EXERCISE: switch the Archivist to hybrid mode

1. Expose the Archivist's tools as the `narzedzia_api.py` module with **docstrings
   written according to the rules from part 7** (what it returns, edges, an example).
2. Implement `wybierz_tryb()` and wire it into the loop.
3. Add a `kod.wykonanie` event to the log: code, result, number of attempts, time.
4. Run 20 real tasks and check in `sesja-cli.py` how the mode choice was distributed.

```bash
python3 sesja-cli.py tryby archiwista --ostatnie 20
# classic: 12 (60%)  avg 3.2 turns   avg 2,100 tok.
# code:     8 (40%)  avg 2.1 turns   avg 1,400 tok.   repair: 1.3 attempts
```

5. **A harder task:** find a task on which `wybierz_tryb()` decides wrongly, and add a
   signal that fixes it. Then check that you have not broken the other 19.

---

## 12. Pitfalls of this part

| ID | Pitfall | Symptom | How to avoid |
| :-- | :-- | :-- | :-- |
| **P91** | **A swallowed traceback** | The model gets "execution error" with no details and guesses blindly | The traceback (3 frames) goes back to the model. It is its main feedback channel |
| **P92** | **Paths not checked inside the API** | `czytaj("../../.ssh/id_rsa")` escapes the archive | `resolve()` + a prefix check in **every** function. The sandbox is the second layer, not the first |
| **P93** | **No call limit in a program** | `for f in znajdz("**/*")` over 40k files: a 30 s timeout with no result | A call counter + a limit + a readable message on what to do instead |
| **P94** | **The model prints raw content** | `print(czytaj(f))` in a loop: 24k tokens, exactly what was supposed to disappear | Rule 3 in the prompt **and** a hard `limit_wyjscia`. The rule alone is not enough |

---

## 13. Checkpoint

```bash
cd $OSA
python3 - <<'EOF'
from kod.wykonanie import uruchom
w = uruchom('print(len(znajdz("faktury/**/*.txt")))',
            korzen_archiwum="/home/USER/os-agenta/pomiary/codemode/archiwum")
print("✓ execution:", w["wyjscie"].strip())

z = uruchom('open("/etc/passwd").read()', korzen_archiwum="/tmp")
assert z["kod_wyjscia"] != 0, "✗ P92/sandbox: reading /etc/passwd went through!"
print("✓ the sandbox blocks reads from outside the archive")

s = uruchom('import socket; socket.create_connection(("1.1.1.1",80),2)',
            korzen_archiwum="/tmp")
assert s["kod_wyjscia"] != 0, "✗ network available in the sandbox!"
print("✓ no network in the sandbox")
EOF
test -s pomiary/codemode/wyniki.csv && echo "✓ mode comparison measured"
git add -A && git commit -m "part 8: code-mode, tool API, execution in a sandbox"
```

- [ ] You understand **three** savings mechanisms, not just "fewer turns"
- [ ] You know why code-mode helps **small local models** in particular
- [ ] The tools have one source of truth, two exposures
- [ ] `pomoc()` replaces the schemas in the prompt: documentation on demand
- [ ] Sandbox: no network, archive read-only, writes to `/tmp/praca`
- [ ] The traceback goes back to the model; the repair loop has 3 attempts and escalates
- [ ] You know the situations in which code-mode **loses**, and you have a hybrid mode
- [ ] ⭐ **You measured both modes on 5 tasks × 2 models: you have your own numbers**
- [ ] ⭐ You know how many generated programs tried to leave the sandbox

---

**Next: `09-PROTOCOLS-MCP-CLI-A2A.md`**: is MCP worth its tokens. We measure
Steinberger's thesis instead of arguing about it.
