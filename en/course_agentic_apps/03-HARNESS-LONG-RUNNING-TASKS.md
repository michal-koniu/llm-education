# Part 3 · Harness — a loop that survives long tasks

**Level:** ⭐⭐⭐⭐ · **Time:** ~6 h · **Requires:** parts 1 and 2
**Produces:** a harness, a task registry, a progress file, an agent that finishes the job across 5 context windows

> ⭐ **This is the most important part of the course.** If you read only one, read this one.
> Everything that follows — memory, tools, the fleet — is an extension of what gets built here.

---

## 0. What a harness is and why it is the product

The **harness** is everything around the model call: what the agent receives at the start of a turn,
when it stops, what it sees after an error, how it hands work to the next session, who checks
the result.

Recall the finding from part 1:

> **An agent's result changes more with the harness than with the model.** The same model under
> two scaffolds produces significantly different numbers.
> — [Prefactor, Agent Benchmarks](https://prefactor.tech/learn/agent-benchmarks)

And Steinberger's sentence:

> "Don't prompt agents. **Design loops that prompt agents.**"

Both statements say the same thing from two sides. **The harness is the variable you have
full control over.** The model weights are a variable you have no control over at all.

### 0.1 · The problem in one picture

The task: "tidy up my 2026 documents — read, classify, rename according to a
scheme, build an index". 340 files. Realistically ~6 hours of agent work.

```
WITHOUT A HARNESS (your loop from course 1):

 window 1 ████████████████████ full → the agent loses the goal, starts hallucinating
        ✗ the end. 41 files done. Nobody knows which.

WITH A HARNESS:

 window 1 ████████████████ → save progress → git commit → end of session
 window 2 ████████████████ → reads progress, knows where it stopped → continues
 window 3 ████████████████ → …
 window 4 ████████████████ → …
 window 5 ██████████       → all 340, index, tests green
```

**The difference is not in the model. It is that session 2 knows what session 1 did.**

---

## 1. The cold-start problem

Every time a session ends, the agent **loses all of its working memory**. A new session
starts with an empty context. Anthropic calls this the crux of the matter:

> The key is finding a way for the agent to **quickly understand the state of the work** when starting
> with a fresh context window.
> — [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

Within the **first ~2000 tokens**, a new session must answer four questions for itself:

| Question | Where the answer comes from |
| :-- | :-- |
| What am I supposed to do? | the **task registry** (`zadanie.json`) |
| What has already been done? | the **progress file** (`POSTEP.md`) + `git log` |
| Does what was done **work**? | **baseline tests** run at startup |
| What am I doing now? | the first unfinished registry item |

⭐ **These are four artifacts and all of them are files.** There is nothing here about the model, the context,
or prompts. **The agent's long-term memory is the file system** — and that is the whole
secret.

---

## 2. The task registry — the cure for "done!" when it isn't done

The most common and most infuriating agent failure mode: **it says it has finished when it
hasn't**. In the experiment in part 1 you named it `CICHY`.

The cause is structural, not a matter of prompting. The agent has no **objective definition of
completion** — so it uses a subjective one: "I've done a lot, this sounds like the end".

**The cure: break the task into a list of items with a binary state, with a test step for
each.**

```json
{
  "zadanie": "Tidy up the 2026 documents",
  "utworzone": "2026-09-23T08:00:00Z",
  "zasady": [
    "You MUST NOT delete or change the test steps.",
    "An item is 'zrobione' only when its test step passes.",
    "When in doubt leave it 'w_toku' and describe the blocker."
  ],
  "pozycje": [
    {
      "id": "P01",
      "opis": "Inventory all 2026 files into inwentarz.csv",
      "test": "wc -l < inwentarz.csv  → expect 340",
      "stan": "zrobione",
      "uwagi": "3 files without a date in metadata — taken from the name"
    },
    {
      "id": "P02",
      "opis": "Classify every file into one of 6 categories",
      "test": "python3 sprawdz.py kategorie  → 0 empty, 0 outside the dictionary",
      "stan": "w_toku",
      "uwagi": "done 180/340, last: faktura-2026-03-11.pdf"
    },
    {
      "id": "P03",
      "opis": "Rename according to the scheme YYYY-MM-DD_category_description",
      "test": "python3 sprawdz.py nazwy  → 0 non-conforming",
      "stan": "do_zrobienia",
      "uwagi": ""
    }
  ]
}
```

### 2.1 · Three rules without which this does not work

**1 · The test step must be an executable command, not a description.**

```
✗ "test": "check that the categories are correct"     ← the agent will grade itself
✓ "test": "python3 sprawdz.py kategorie"              ← a verdict from outside
```

This is a direct application of the finding on **external verification**: self-reflection
has a self-confirmation bias, because the judge sits in the same trajectory state as
the author ([arXiv 2603.02798](https://arxiv.org/pdf/2603.02798)). Code run in a shell
is not in that state. **Execution is the strongest verification signal you
have** — in part 14 you will expand this into a full evaluation.

**2 · The agent must not delete or change tests.**

Anthropic states this as a hard rule: *"It is unacceptable to remove or edit tests
because this could lead to missing or buggy functionality."* An agent under the pressure of a
failing test will **delete the test** — this is locally optimal and globally
catastrophic. A rule in a file is not enough; in §9 you enforce it in code.

**3 · The `w_toku` state must carry exactly where work was interrupted.**

`"done 180/340, last: faktura-2026-03-11.pdf"` is the difference between resuming
and starting over.

---

## 3. The progress file — a narrative for the next session

The registry says **what**. The progress file says **how, and what I learned**.

```markdown
# PROGRESS · Tidy up the 2026 documents

## State as of 2026-09-23 11:40 (session 3)

Done: P01. In progress: P02 (180/340).

## What I learned — read this before you start

- Files in `~/dokumenty/skan/` have the date **only in the name**, the metadata is empty.
  Use `parsuj_nazwe()`, not `os.path.getmtime`.
- The "contract" and "amendment" categories get confused. An amendment always has the word "aneks" or
  "zmieniający" in its first 200 characters. I added this to `sprawdz.py`.
- ⚠️ **Do NOT run `zmien_nazwy.py` without `--sucho`.** Once I overwrote two files
  with the same date. Fixed via a backup copy, but don't repeat it.

## Blocked

Nothing.

## Next step

`P02` starting from `faktura-2026-03-11.pdf`. The list of remaining ones is in `pozostale.txt`.
```

> 💡 **The "What I learned" section is the most valuable one here** and it is what distinguishes a harness from
> plain resuming. Without it, session 4 **will repeat the mistake of session 2** — because it has no way
> to know that someone already stepped in it. This is the agent's procedural memory and the first
> seed of what you will grow into long-term memory in part 5.

---

## 4. Git as the agent's memory

Anthropic uses git in the harness not for versioning but **as a memory mechanism**:

| For what | How |
| :-- | :-- |
| "What did the previous session do" | `git log --oneline -20` — cheaper than reading files |
| "Did I already change this" | `git diff HEAD~1` |
| "I broke it, roll back" | `git reset --hard` — **error recovery for free** |
| "When did this break" | `git bisect` |

**The rule: one commit per completed registry item**, with a message containing the `id`.

```
P01: inventory of 340 files into inwentarz.csv
P02: classification 180/340 (interrupted, resume from faktura-2026-03-11)
```

⭐ **Why commit on `w_toku`, not only on `zrobione`.** Because a session ends
in the middle of an item far more often than at its boundary. A commit "interrupted, resume from X"
is a **cheaper carrier of state than any file** you would have to write.

---

## 5. The startup sequence — the first 60 seconds of a session

Every working session performs an **identical, rigid sequence** before it touches the task.
This is not a prompt — it is code.

```
1. Establish location    pwd, check that it is the task directory
2. Read the history      git log -15, POSTEP.md, zadanie.json
3. Verify the baseline   run the tests of ALL 'zrobione' items
4. Pick the work         the first 'w_toku' item, then 'do_zrobienia'
5. Declare intent        append to POSTEP.md: "session N starts P0X"
6. → work
7. Close                 update the registry + progress, commit, final tests
```

**Step 3 is the one everyone skips, and the one that saves the project.**

If session 2 broke something that session 1 did correctly, **you will find out at the start
of session 3**, not after six hours. Cost: a dozen or so seconds per session. Return:
detecting a regression in a window in which it can still be attributed to its cause.

> ⚠️ **The failure mode this catches is insidious.** The agent fixes P02 and "while at it"
> refactors a function used by P01. P01 still has the `zrobione` state in the registry, but
> its test no longer passes. Without step 3 **the registry lies to the very end**.

---

## 6. Stopping — five conditions, not one

The loop from course 1 ended when the model stopped calling tools. That is one condition
and **decidedly too few**.

| # | Condition | Why | What to do after |
| :-- | :-- | :-- | :-- |
| 1 | **Task complete** | all items `zrobione` + tests green | commit, report |
| 2 | **Context budget** (~70 % of the window) | beyond that context rot begins (part 4) | **compaction or closing the session** |
| 3 | **Turn budget** (e.g. 40) | a safeguard against looping | save progress, close |
| 4 | **No progress** (3 turns without a state change) | the agent is going in circles | escalate: another model or a human |
| 5 | **Hard blocker** | no permissions, no file, no network | record the blocker, **call a human** |

⭐ **Condition 4 is the hardest to detect and the most valuable.** "No progress" does not
mean "no activity" — the agent may be diligently reading the same file for the fifth time. Measure
**the change in the state of the world**, not the number of turns:

```python
def odcisk_stanu(katalog: str) -> str:
    """Hash of the world state. It changed = there was progress."""
    import hashlib, subprocess
    h = hashlib.sha256()
    h.update(subprocess.run(["git", "status", "--porcelain"],
                            cwd=katalog, capture_output=True).stdout)
    h.update(pathlib.Path(katalog, "zadanie.json").read_bytes())
    return h.hexdigest()[:16]
```

Three turns with the same fingerprint = the agent is doing nothing useful, **no matter
how diligent it looks**.

---

## 7. The error-recovery ladder

Remember the arithmetic from part 1: 0.92¹⁵ = 29 %. With 15 steps **an error is the norm, not
the exception**. A harness that cannot pull itself together after an error is useless.

**The rule: escalate by cost, not straight to the maximum.**

| Rung | Reaction | Cost | When |
| :-- | :-- | :-- | :-- |
| 0 | **Show the error to the model and let it fix it** | 1 turn | always first |
| 1 | **Show the error + a structured hint** | 1 turn | second attempt of the same tool |
| 2 | **Undo the last action, try differently** | `git checkout` + 1 turn | third attempt |
| 3 | **Split the item into smaller ones** | rewriting the registry | task too large for one turn |
| 4 | **Switch to a stronger model** | ~3× time | rungs 0–3 exhausted |
| 5 | **Stop, call a human** | Your time | hard blocker or everything exhausted |

⚠️ **Rung 0 requires the error to be legible to the model.** This is directly the rule from
Steinberger's MCP Best Practices: *"on error, emit a message with information
that lets it recover"*. Compare:

```
✗  Traceback (most recent call last): … PermissionError: [Errno 13]
✓  ERROR: no write permission for /etc/hosts.
   The sandbox allows writing only in $OSA/ and /tmp/.
   If you want to save the result — use /tmp/wynik.txt.
```

The first message gives the model a 20 % chance of fixing it. The second — above 90 %.
**The error message is part of the prompt.** Write it like a prompt.

---

## 8. Loop engineering in practice — seven levers

Since you are designing a loop, not a prompt, it is worth knowing **what in the loop can be turned**.

| # | Lever | Question | Where in the course |
| :-- | :-- | :-- | :-- |
| 1 | **Turn input** | What does the agent see at the start of each turn? | this part, 4 |
| 2 | **Tool visibility** | All at once or loaded on demand? | 7, 8 |
| 3 | **Observation shape** | Raw output or trimmed and described? | 7 |
| 4 | **Stop condition** | When do you interrupt? | this part, §6 |
| 5 | **Reaction to error** | What does it see after a failure? | this part, §7 |
| 6 | **Handoff** | What does the next session receive? | this part, §2–4 |
| 7 | **Verification** | Who checks — and from outside? | 14 |

> 🎯 **A thought exercise worth doing at every agent error.** Instead of asking
> "how do I rephrase the prompt", ask: **"which of these seven levers should I
> turn?"** In 8 cases out of 10 the answer is not "the prompt".

---

## 9. FROM SCRATCH — the harness

```python
# $OSA/harness.py
"""Harness: a loop that survives multiple context windows."""
import json, pathlib, subprocess, hashlib, datetime, shutil

TERAZ = lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

class Rejestr:
    """zadanie.json — binary item state, tests inviolable."""
    def __init__(self, katalog):
        self.kat = pathlib.Path(katalog)
        self.plik = self.kat / "zadanie.json"
        self.dane = json.loads(self.plik.read_text(encoding="utf-8"))
        self._testy_odcisk = self._odcisk_testow()

    def _odcisk_testow(self) -> str:
        t = "|".join(f'{p["id"]}::{p["test"]}' for p in self.dane["pozycje"])
        return hashlib.sha256(t.encode()).hexdigest()

    def nastepna(self) -> dict | None:
        for stan in ("w_toku", "do_zrobienia"):
            for p in self.dane["pozycje"]:
                if p["stan"] == stan:
                    return p
        return None

    def ustaw(self, id_: str, stan: str, uwagi: str = ""):
        for p in self.dane["pozycje"]:
            if p["id"] == id_:
                p["stan"], p["uwagi"] = stan, uwagi or p["uwagi"]
        self.zapisz()

    def zapisz(self):
        # P67: the agent MUST NOT change or delete a test.
        if self._odcisk_testow() != self._testy_odcisk:
            raise PermissionError(
                "BLOCKED: attempt to change test steps in zadanie.json. "
                "Tests are inviolable. If a test is wrong — report it to a human.")
        self.plik.write_text(json.dumps(self.dane, indent=2, ensure_ascii=False),
                             encoding="utf-8")

    def test(self, poz: dict) -> tuple[bool, str]:
        polecenie = poz["test"].split("→")[0].strip()
        w = subprocess.run(polecenie, shell=True, cwd=self.kat,
                           capture_output=True, text=True, timeout=120)
        return w.returncode == 0, (w.stdout + w.stderr)[-800:]

    def weryfikuj_baze(self) -> list[str]:
        """Step 3 of the startup sequence. Returns the IDs that REGRESSED."""
        zepsute = []
        for p in self.dane["pozycje"]:
            if p["stan"] == "zrobione":
                ok, _ = self.test(p)
                if not ok:
                    zepsute.append(p["id"])
                    p["stan"] = "w_toku"
                    p["uwagi"] = f"REGRESSION detected {TERAZ()} — was 'zrobione'"
        if zepsute:
            self.zapisz()
        return zepsute
```

```python
# $OSA/harness.py (continued)

def git(kat, *a) -> str:
    return subprocess.run(["git", *a], cwd=kat, capture_output=True,
                          text=True).stdout.strip()

def odcisk_stanu(kat) -> str:
    h = hashlib.sha256()
    h.update(git(kat, "status", "--porcelain").encode())
    h.update((pathlib.Path(kat) / "zadanie.json").read_bytes())
    return h.hexdigest()[:16]

def sekwencja_startowa(kat: str) -> dict:
    """The first 60 seconds of a session. Returns the startup package for the model."""
    r = Rejestr(kat)
    postep = (pathlib.Path(kat) / "POSTEP.md")
    zepsute = r.weryfikuj_baze()                       # step 3
    poz = r.nastepna()                                 # step 4
    return {
        "katalog": kat,
        "zadanie": r.dane["zadanie"],
        "historia_git": git(kat, "log", "--oneline", "-15"),
        "postep": postep.read_text(encoding="utf-8") if postep.exists() else "(none)",
        "regresje": zepsute,
        "pozycja": poz,
        "pozostalo": sum(1 for p in r.dane["pozycje"] if p["stan"] != "zrobione"),
        "rejestr": r,
    }

SZABLON_STARTU = """You are working on a multi-stage task. This is a working session.

# Task
{zadanie}

# What was done earlier (git)
{historia_git}

# Notes from previous sessions — READ before you start
{postep}
{blok_regresji}
# Your item in this session
{pozycja_id}: {pozycja_opis}
Test step (you MUST NOT change it): {pozycja_test}
Notes for this item: {pozycja_uwagi}

Items remaining: {pozostalo}

# Rules
1. You work ONLY on this one item.
2. An item is complete only when the test step passes. Run it.
3. When you finish or get stuck — save the state to POSTEP.md and make a commit.
4. If the test is wrong — do NOT change it. Describe the problem and stop.
"""

def pakiet_startowy(s: dict) -> str:
    blok = ""
    if s["regresje"]:
        blok = (f"\n# ⚠️ REGRESSION\nItems {', '.join(s['regresje'])} were 'zrobione', "
                f"and their tests no longer pass. Fix them BEFORE any new work.\n")
    p = s["pozycja"] or {"id": "—", "opis": "no work", "test": "—", "uwagi": ""}
    return SZABLON_STARTU.format(
        zadanie=s["zadanie"], historia_git=s["historia_git"], postep=s["postep"],
        blok_regresji=blok, pozycja_id=p["id"], pozycja_opis=p["opis"],
        pozycja_test=p["test"], pozycja_uwagi=p["uwagi"] or "(none)",
        pozostalo=s["pozostalo"])
```

```python
# $OSA/harness.py (end) — the session loop with five stop conditions

MAX_TUR         = 40
BUDZET_KONTEKSTU = 0.70
BEZ_POSTEPU_MAX = 3

def sesja_robocza(kat: str, wywolaj_model, wykonaj_narzedzie, okno_tokenow=32768):
    s = sekwencja_startowa(kat)
    if s["pozycja"] is None:
        return {"powod": "ukonczone", "tur": 0}

    r: Rejestr = s["rejestr"]
    historia = [{"rola": "user", "tresc": pakiet_startowy(s)}]
    odcisk, bez_postepu, uzyte = odcisk_stanu(kat), 0, 0

    for tura in range(1, MAX_TUR + 1):
        odp = wywolaj_model(historia)
        uzyte = odp["tokeny_we"] + odp["tokeny_wy"]

        if odp.get("narzedzie"):
            wynik = wykonaj_narzedzie(odp["narzedzie"], odp["argumenty"])
            historia += [{"rola": "assistant", "tresc": odp["tresc"]},
                         {"rola": "tool", "tresc": wynik}]
        else:
            historia.append({"rola": "assistant", "tresc": odp["tresc"]})

        # --- stop conditions, in order of importance ---
        ok, wyjscie = r.test(s["pozycja"])
        if ok:                                                        # 1
            r.ustaw(s["pozycja"]["id"], "zrobione", f"completed {TERAZ()}")
            zamknij(kat, r, s["pozycja"], "zrobione", tura)
            return {"powod": "pozycja_ukonczona", "tur": tura}

        if uzyte > okno_tokenow * BUDZET_KONTEKSTU:                   # 2
            zamknij(kat, r, s["pozycja"], "context budget", tura)
            return {"powod": "kontekst", "tur": tura}

        nowy = odcisk_stanu(kat)                                      # 4
        bez_postepu = bez_postepu + 1 if nowy == odcisk else 0
        odcisk = nowy
        if bez_postepu >= BEZ_POSTEPU_MAX:
            zamknij(kat, r, s["pozycja"], "no progress — escalation", tura)
            return {"powod": "brak_postepu", "tur": tura}

    zamknij(kat, r, s["pozycja"], "turn limit", MAX_TUR)              # 3
    return {"powod": "limit_tur", "tur": MAX_TUR}

def zamknij(kat, r: Rejestr, poz, powod, tura):
    """Step 7. Progress + commit. Executed ALWAYS, also on failure."""
    p = pathlib.Path(kat) / "POSTEP.md"
    p.write_text((p.read_text(encoding="utf-8") if p.exists() else "# PROGRESS\n")
                 + f"\n## {TERAZ()} — {poz['id']} — {powod} (turns: {tura})\n"
                   f"State: {poz['stan']}. {poz['uwagi']}\n", encoding="utf-8")
    git(kat, "add", "-A")
    git(kat, "commit", "-m", f"{poz['id']}: {powod} ({poz['stan']})")
```

---

## 10. IN PRODUCTION — what off-the-shelf harnesses give you

| Element | Claude Agent SDK | LangGraph | **Yours** |
| :-- | :-- | :-- | :-- |
| Automatic compaction | ⭐ built in | ✗ | manual (part 4) |
| Checkpoints | sessions | ⭐ checkpointer + time-travel | journal + branches (part 2) |
| Resuming from a cold start | partially | via checkpointer | ⭐ **registry + progress + git** |
| **Test inviolability** | ✗ | ✗ | ⭐ **enforced in code** |
| No-progress detection | ✗ | manual | ⭐ state fingerprint |
| Baseline verification at startup | ✗ | ✗ | ⭐ step 3 |
| Maturity | high | high | Yours |

**Three stars in your column are no accident.** Off-the-shelf frameworks solve
the problem of "how to run an agent". You solve the problem of **"how to make the agent
finish the job and make you believe it"** — and that is a different and less often addressed problem.

> ⚠️ **Honestly: where your harness loses.** It has no automatic compaction (you build
> it in part 4), no streaming, and no time travel over graph state. If you
> ever start building flows approved by an auditor — LangGraph's checkpointer
> will be better, because **it can be drawn**.

---

## 11. EXPERIMENT 3 — a task spanning five context windows

**Hypothesis:** the same task that fails in the first window without a harness
succeeds across several sessions with a harness — **on the same model**.

**Test task** (does not require your private files):

```bash
mkdir -p $OSA/proby/korpus && cd $OSA/proby
python3 - <<'EOF'
import random, pathlib
random.seed(42)
kat = pathlib.Path("korpus"); kat.mkdir(exist_ok=True)
typy = ["faktura", "umowa", "aneks", "notatka", "raport", "pismo"]
for i in range(340):
    t = random.choice(typy)
    m, d = random.randint(1,9), random.randint(1,28)
    tresc = f"{'ANEKS zmieniający' if t=='aneks' else t.upper()} nr {i}\n" + "treść "*random.randint(20,200)
    (kat / f"dok_{i:03d}.txt").write_text(tresc, encoding="utf-8")
print("340 files ready")
EOF
git init && git add -A && git commit -q -m "starting corpus"
```

Build a `zadanie.json` with four items (inventory → classification → names → index),
each with an **executable** test step.

**Run A — without a harness.** Run the loop from course 1 with the full task description in one
prompt. Note where it died.

**Run B — with a harness.** Run `sesja_robocza()` in a loop until it returns
`ukonczone` or the same reason five times in a row.

**Results table:**

| Measure | A (without) | B (with harness) |
| :-- | --: | --: |
| Items completed /4 | | |
| Sessions | 1 | |
| Total turns | | |
| Total tokens | | |
| Total time | | |
| Regressions detected | 0 | |
| Termination mode | | |

⚠️ **Prediction to verify:** A finishes item 1, maybe starts 2, and dies on
`KONTEKST` or `CICHY`. B finishes all four in 4–7 sessions, using **more
tokens in total** (because every session reads the startup package) and **less of your time**.

⭐ **If B uses more tokens than A, that is not a failure.** It is the price
you pay for a finished task. You are comparing "more expensive and done" with "cheaper and unfinished" —
and those are not the same unit.

---

## 12. EXERCISE — the initializer agent

Anthropic splits agents into the **initializer** (the first session) and the **worker**
(all subsequent ones). You have built the worker. Write the initializer:

```bash
python3 harness.py inicjuj "Tidy up the 2026 documents" $OSA/proby
```

It is to produce:

1. **`zadanie.json`** — a breakdown into 4–8 items, each with an **executable** test
2. **`sprawdz.py`** — a script that implements those tests
3. **`POSTEP.md`** — empty, with section headings
4. **`init.sh`** — recreates the environment from scratch
5. **the first commit** — a baseline you can return to

**A quality criterion that really measures something:** delete everything except `korpus/`
and `init.sh`, run `init.sh`, and check whether the worker agent **starts without your
help**. If not — the initializer was too weak and that is the right diagnosis.

> 💡 **Why this separation makes sense.** The initializer and the worker have **conflicting
> goals**. The initializer is meant to be lavish: think the task through, break it down, write the tests —
> once, expensively, well. The worker is meant to be frugal: come in, do one thing, leave.
> One prompt cannot serve both, because they optimize for different things.

---

## 13. Pitfalls of this part

| ID | Pitfall | Symptom | How to avoid |
| :-- | :-- | :-- | :-- |
| **P67** | **The agent changes or deletes a test to make it pass** | Everything green, the functionality does not work | A test fingerprint checked on every registry write (`Rejestr.zapisz`) |
| **P68** | **A registry item too large for one session** | Always `w_toku`, never `zrobione`, progress is only apparent | An item must fit within ~60 % of the window. Too large → split (rung 3 of the ladder) |
| **P69** | **Skipping baseline verification at startup** | A regression from session 2 surfaces in session 9, when you no longer know why | Step 3 of the startup sequence. A dozen or so seconds |
| **P70** | **No progress mistaken for no activity** | The agent diligently reads the same file 5 times and the turn counter rises | Measure the **world-state fingerprint**, not the number of turns |
| **P71** | **An error message illegible to the model** | The agent gives up after the first failure instead of fixing it | Error = prompt. Write what went wrong, why, and **what is allowed instead** |

---

## 14. Checkpoint

```bash
cd $OSA
python3 -c "import harness; print('✓ import')"
python3 - <<'EOF'
from harness import Rejestr
r = Rejestr("proby")
r.dane["pozycje"][0]["test"] = "echo oszustwo"
try:
    r.zapisz(); print("✗ P67 DOES NOT WORK — tests can be swapped")
except PermissionError:
    print("✓ P67 — tests inviolable")
EOF
git add -A && git commit -m "part 3: harness, task registry, startup sequence"
```

- [ ] You understand why harness > model
- [ ] The task registry has binary states and **executable** tests
- [ ] Tests cannot be changed — enforced by code, not by a request
- [ ] `POSTEP.md` carries "what I learned", not only "what I did"
- [ ] Git is a memory mechanism, not only versioning
- [ ] The startup sequence **verifies the baseline** before new work
- [ ] Five stop conditions, including no-progress detection
- [ ] The recovery ladder escalates by cost
- [ ] **A task spanning 5 context windows runs from start to finish**

---

**Next: `04-CONTEXT-ENGINEERING.md`** — the attention budget, context rot measured on your
models, and compaction that does not lose numbers.
