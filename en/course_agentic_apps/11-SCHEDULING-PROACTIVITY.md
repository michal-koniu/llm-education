# Part 11 · Scheduling — an agent that wakes itself up

**Level:** ⭐⭐⭐⭐ · **Time:** ~5 h · **Requires:** parts 2 (gateway), 3 (harness), 10 (sandbox)
**Produces:** a scheduler, `HEARTBEAT.md`, silence suppression, a measurement of nudge accuracy

---

## 0. The threshold beyond which an agent becomes something else

So far your agent has **responded**. You ask, it acts. That is a tool.

An agent that wakes itself up is something else — and the difference is not technical, it is
**relational**. A tool that speaks up on its own has to earn every single time it does.
Two unnecessary notifications a day and you will switch it off within a week.

```
      Reactive agent               Proactive agent
   ─────────────────────        ─────────────────────
   You initiate                  It initiates
   Cost of error: your time      Cost of error: your TRUST
   Test: did it respond          Test: was it WORTH it
   Scale: how many questions     Scale: ⭐ unlimited
          you get to ask
```

⭐ **The right-hand column is the reason you are building this** — proactivity removes the
limit of "how many questions you have time to ask". And at the same time it is the reason
**most agent projects fall flat right here**.

> ⚠️ **The MoltMatch case.** A documented incident in which an OpenClaw agent created
> dating profiles **without the user's explicit consent**. It was not a break-in — the agent
> acted proactively within the permissions it was given, and **outside the intent** attributed
> to it. **Proactivity without boundaries is not sophistication, it is unpredictability.**

---

## 1. `HEARTBEAT.md` — cron expressed in plain language

A pattern from OpenClaw, and a very good one: instead of configuring tasks in YAML, **a list
of things to watch, written in sentences**.

```markdown
# HEARTBEAT — Gospodarz
# Read on every wake-up. Edited by the human; the agent only reads.

## Every morning (7:00)
- Check today's calendar. Speak up ONLY if:
  there is something before 10:00, OR two events overlap,
  OR there is something that requires bringing an item (ticket, document, gift).
- Do not summarize a quiet day. A quiet day means no message.

## Every hour (8:00–20:00)
- Check whether there is a reminder for the next 90 minutes.
  One reminder = one message. Do not repeat.

## Every evening (21:00)
- If tomorrow there is something before 9:00 — remind about it today.
- If tomorrow is waste collection — remind which type.

## Every Sunday (18:00)
- A week ahead: what needs preparation earlier than the day before.

## Overriding rule
When you have nothing **worth interrupting the human for** — reply with exactly
HEARTBEAT_OK and nothing else. That is the correct and the most common response.
```

### 1.1 · `HEARTBEAT_OK` — the mechanism that saves this

⭐ **This is the best single idea in the entire proactive architecture.**

```
wake-up → agent evaluates → reply "HEARTBEAT_OK" → GATEWAY SUPPRESSES, nothing gets through
                            └→ anything else       → delivered to the human
```

Why this works better than a condition in code:

1. **The default response is silence**, not a message. The opposite of a regular cron.
2. **The "is it worth it" judgment belongs to the model**, which sees the context — not to a
   rule, which does not.
3. **The gateway counts suppressions**, so you get a metric: *"today 24 wake-ups, 2 messages"*.
4. The agent does not have to "do nothing" — it has **a defined action for when all is calm**,
   and that is much easier for a model (the same principle as error messages in part 3 and
   the boundaries in part 6).

```python
def przetworz_przebudzenie(odpowiedz: str, dziennik) -> bool:
    """Returns True if something reached the human."""
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

⚠️ **The `len < 15` condition matters.** A model will sometimes reply "OK", "Nothing new",
"None". These are **intentional silences expressed differently**, and without this condition
you will send the human a message reading "OK" — the worst possible kind of notification.

---

## 2. The scheduler

```python
# $OSA/harmonogram/planista.py
"""Time-based and event-based triggers. A single instance — see P104."""
import re, datetime, pathlib, json, hashlib

WZORCE = [
    (r"co rano \((\d{1,2}):(\d{2})\)",        "dziennie"),
    (r"co wiecz[oó]r \((\d{1,2}):(\d{2})\)",  "dziennie"),
    (r"co godzin[ęe] \((\d{1,2}):\d{2}[–-](\d{1,2}):\d{2}\)", "godzinowo"),
    (r"co (\w+)\w* \((\d{1,2}):(\d{2})\)",    "tygodniowo"),
]
DNI = {"poniedziałek":0,"wtorek":1,"środ":2,"czwartek":3,"piątek":4,"sobot":5,"niedziel":6}

def parsuj(sciezka) -> list[dict]:
    """## headings in HEARTBEAT.md → triggers. Section body → task."""
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

### 2.1 · The scheduler loop — with safeguards

```python
def petla(brama, katalog_agentow, interwal_s=300):
    """Wakes up every 5 min, checks what has come due. Run by systemd."""
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
                if _juz_wykonane(klucz):                    # ⭐ P105 — idempotency
                    continue
                _uruchom(brama, kat.name, z, klucz)
                _zapisz_ostatnie(kat, z["naglowek"], teraz)
        _spij(interwal_s)

def _klucz_wykonania(agent, z, teraz) -> str:
    """A daily task runs once per day — regardless of scheduler restarts."""
    okno = {"dziennie": "%Y-%m-%d", "godzinowo": "%Y-%m-%d-%H",
            "tygodniowo": "%Y-W%W"}[z["typ"]]
    return hashlib.sha256(
        f"{agent}|{z['naglowek']}|{teraz.strftime(okno)}".encode()).hexdigest()[:16]
```

⭐ **`_klucz_wykonania` is what distinguishes a scheduler from `cron`.** A gateway restart
at 7:05 **must not** run the morning task again. A key based on the time window
(day/hour/week) guarantees execution **exactly once per window**, no matter how many times
the scheduler comes back up.

---

## 3. Event-driven wake-up

Time is not the only trigger, and usually not the best one.

| Trigger | Example | Latency | Cost |
| :-- | :-- | :-- | :-- |
| **Time** | "every morning 7:00" | up to the interval | low |
| **File** (`inotify`) | a new scan in `~/skany/` | ⭐ immediate | ⭐ zero when quiet |
| **Webhook** | an external system calls the gateway | immediate | zero |
| **Threshold** | graphics card temperature > 90 °C | up to the polling interval | low |
| **Another agent** | the Archivist found a gap (part 13) | immediate | zero |

```python
# file watcher — zero cost when nothing is happening
def obserwuj(katalog, na_zdarzenie, debounce_s=2.0):
    """New file → wake-up. Debounce, because copying generates many events."""
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

⭐ **Event-driven wake-up beats time-based wherever it can be used.** Polling every
5 minutes for "is there a new file" is 288 wake-ups a day, 287 of which do nothing. `inotify`
is zero wake-ups and an **immediate reaction**. Use time only when there is no event — that
is, for periodic reviews.

---

## 4. The nudge problem — signal versus noise

This is the **real difficulty** of this part. Not a technical one.

```
The agent speaks up 8× a day, 6 of them unnecessarily
   → after a week you ignore all of them, including the 2 important ones
   → the agent has become WORSE than no agent,
     because it gave you a false sense that something is being watched
```

### 4.1 · Measure it like a classifier

| | Spoke up | Stayed silent |
| :-- | :-- | :-- |
| **Worth it** | ⭐ hit (TP) | ⚠️ **miss (FN)** |
| **Not worth it** | ⚠️⚠️ **noise (FP)** | ⭐ rightly quiet (TN) |

⭐ **Noise costs more than a miss**, and this is counterintuitive. A miss costs one event.
Noise costs **trust in all future messages** — after five unnecessary ones you stop reading
the necessary ones too.

**Design conclusion: set the threshold high and lower it only on the basis of misses that
actually hurt.** Not the other way around.

### 4.2 · Three threshold levers

```python
PROGI = {
    "pilnosc_minimalna": 3,     # 1–5; below — silence
    "max_dziennie": 4,          # hard limit; the excess waits for the review
    "cisza_nocna": (22, 7),     # nothing except an ALARM
    "min_odstep_min": 45,       # no two messages in a row
}

PROMPT_OCENY = """Assess whether this is worth interrupting the human for.

Urgency scale:
5 — a loss if they do not find out within an hour (flight in 3 h, outage)
4 — they should know today (deadline tomorrow, calendar conflict)
3 — worth them knowing this week
2 — a curiosity, can wait for the weekly review
1 — not worth it at all

Today you have already spoken up {ile} times (limit {limit}).
Last message: {ile_temu} minutes ago.

When urgency < {prog} — reply with exactly HEARTBEAT_OK.

Situation: {sytuacja}"""
```

⚠️ **The line "Today you have already spoken up N times" really does change the model's
behavior.** A model that sees it has used up 3 of 4 nudges raises its own bar. This is the
same mechanism as telling it about the context budget in part 4, and it costs the same:
a dozen or so tokens.

### 4.3 · Queueing instead of giving up

A message with urgency 2 is not worthless — it is **not urgent**.

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

⭐ **A weekly review collecting everything that did not get through is a cheap way to have
your cake and eat it too.** Nothing is lost, and there are few interruptions.

---

## 5. Night work — an advantage nobody in the cloud has

Your machine sits idle ~16 h a day. For someone paying per token, night work is a cost.
**For you it is free.**

```markdown
## Every night (3:00) — never speak up, only work

- Tidy up memory: merge duplicate facts, flag contradictions (part 5)
- Recompute search indexes after new documents
- Run the golden set and write the result to $OSA/pomiary/nocne/ (part 14)
- Check for regressions against yesterday; if the score dropped by >5 pp — that is urgency 4
- Compact session logs older than 30 days

Result: a report to a file. Always HEARTBEAT_OK, unless a regression is detected.
```

⭐ **"Always `HEARTBEAT_OK`, unless a regression" is the best pattern for a night task.**
The work gets done, the report is in a file, and you find out **only when something went
wrong**.

> 💡 **Notice what this really means.** Every night your agent runs a full evaluation and
> compares it with yesterday. This is something product teams roll out as "continuous
> evaluation" and treat as a sign of operational maturity. For you it costs electricity.

---

## 6. Safety of proactivity

An agent acting without you is a different class of risk — and it returns in part 16 as
**ASI10 (rogue agents)**: an agent acts outside policy through compromise or drift,
**looking legitimate** and persisting between sessions.

**Four rules, each answering a specific failure:**

| Rule | What it protects against |
| :-- | :-- |
| **1.** A scheduled task **does not inherit** host permissions | a hijacked night task has a shell for 8 h with no witness |
| **2.** Irreversible operations **always** require a human | MoltMatch |
| **3.** Every wake-up leaves a trace, **including silence** | an agent that "does nothing" while doing something |
| **4.** Circuit breaker: N errors in a row → **disable and notify** | a failure loop through the night |

```python
BEZPIECZNIK = {"bledow_pod_rzad": 3, "akcja": "wylacz_i_powiadom"}

def po_przebudzeniu(agent, wynik, stan):
    if wynik["status"] == "blad":
        stan[agent]["bledy"] += 1
        if stan[agent]["bledy"] >= BEZPIECZNIK["bledow_pod_rzad"]:
            _wylacz_harmonogram(agent)
            _powiadom_czlowieka(
                f"⚠️ Schedule '{agent}' DISABLED after {stan[agent]['bledy']} errors. "
                f"Last: {wynik['blad'][:200]}\n"
                f"Re-enable: sesja-cli.py harmonogram wlacz {agent}")
    else:
        stan[agent]["bledy"] = 0
```

⚠️ **The circuit breaker is the element whose absence hurts most in practice.** An agent
with a broken task every hour over a weekend means 48 failed wake-ups, 48 log entries and —
if each tries to notify about the error — 48 messages.

---

## 7. EXPERIMENT 11 — a week of Gospodarz

**Hypothesis:** at urgency threshold 3 the agent speaks up 2–4 times a day, of which
**over 70% are worth interrupting for**.

### 7.1 · Procedure

Run Gospodarz for seven days. After every message, rate it **with a single keystroke** —
otherwise you will not last the week:

```bash
python3 sesja-cli.py ocen --ostatnia
# [t] worth it   [n] noise   [p] too late   [x] skipped (add manually)
```

Every evening add the misses: what happened, what the agent **should** have told you about
but stayed silent on.

### 7.2 · The weekly table

| Day | Wake-ups | Silences | Messages | Worth it (TP) | Noise (FP) | Misses (FN) |
| :-- | --: | --: | --: | --: | --: | --: |
| Mon | | | | | | |
| … | | | | | | |
| **Total** | | | | | | |

```
Precision = TP / (TP + FP)      ← ⭐ this number decides trust
Recall    = TP / (TP + FN)
Silence ratio = silences / wake-ups
```

⚠️ **Prediction to verify:** the silence ratio will come out **high** (0.85–0.95) and that is
as it should be. Precision in the first week will come out **lower than you expect** —
I'd guess 0.5–0.7 — because the model interprets "worth it" more broadly than you do.

### 7.3 · Calibration — and how not to spoil it

```bash
python3 sesja-cli.py kalibruj gospodarz --z-ocen
# proposes: pilnosc_minimalna 3 → 4 (because 6 of 9 noise messages had urgency 3)
```

**The most valuable product of this experiment is not a number, but the list of noise.**
Read all the FPs and look for a pattern — usually 2–3 categories account for most of them.
Add them **explicitly** to `HEARTBEAT.md` as exceptions:

```markdown
## Never report
- Recurring events I know by heart (gym Tue/Thu 18:00)
- Events with no location and no preparation
- Anything I talked about within the last 24 h
```

⭐ **This is the learning loop in this system: you measure → read the errors → add a rule to
the file → measure again.** No model fine-tuning, no weights. Three sentences in a text file
that you can read and revert (part 6).

---

## 8. IN PRODUCTION

| | `cron` | systemd timer | Celery/APScheduler | OpenClaw | **Yours** |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Time trigger | ⭐ | ⭐ | ⭐ | ⭐ | ⭐ |
| Event-driven | ✗ | partially | ⭐ | ⭐ | ⭐ |
| **Idempotency per window** | ✗ | partially | ⭐ | ? | ⭐ |
| **Silence suppression** | ✗ | ✗ | ✗ | ⭐ `HEARTBEAT_OK` | ⭐ |
| **Urgency assessment by the model** | ✗ | ✗ | ✗ | ⭐ | ⭐ |
| **Circuit breaker after errors** | ✗ | `StartLimitBurst` | partially | ? | ⭐ |
| Written in plain language | ✗ | ✗ | ✗ | ⭐ | ⭐ |

**Run the scheduler under systemd** — do not reinvent supervision:

```ini
# $OSA/systemd/osa-planista.service  (template: @OSA@ = full project path)
[Unit]
Description=OSA agent scheduler
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

systemd does not know the variables from `rig-env.sh`, so the unit file contains the `@OSA@`
placeholder. `init.sh` substitutes the real path for it and writes the ready units to
`systemd/wygenerowane/`:

```bash
cd $OSA && bash init.sh
cp systemd/wygenerowane/osa-planista.service ~/.config/systemd/user/ && systemctl --user daemon-reload
```

---

## 9. EXERCISE

1. Write `HEARTBEAT.md` for Gospodarz — with a **"Never report" section** right away.
2. Implement the scheduler with per-window idempotency and night silence.
3. Hook `HEARTBEAT_OK` into the gateway; add the events `heartbeat.cisza` and `.wiadomosc`.
4. Add a `~/skany/` watcher that wakes the Archivist on a new file.
5. Write the night task: evaluation + comparison with yesterday + silence unless a regression.
6. Run it for a week and fill in the table.

```bash
python3 sesja-cli.py harmonogram status
# gospodarz   ✓ enabled    5 tasks   last: 07:00 (silence)   today: 18 wake-ups, 2 messages
# archiwista  ✓ enabled    1 event-driven (~/skany)          today: 3 wake-ups, 0 messages
# badacz      ✗ disabled   (no HEARTBEAT.md — deliberately)
```

⭐ **The Researcher has no schedule, and that is a design decision.** An agent that reaches out
to the web, acting unsupervised, is the worst possible combination: hostile input plus no
witness. The Researcher runs **only when you ask it to**.

---

## 10. Pitfalls of this part

| ID | Pitfall | Symptom | How to avoid |
| :-- | :-- | :-- | :-- |
| **P104** | **Two scheduler instances** | The morning task runs twice, two messages | The lock file from part 2 **plus** per-window idempotency |
| **P105** | **No idempotency on restart** | A restart at 7:05 reruns the 7:00 task | A key from the time window, not from the moment of launch |
| **P106** | **Silence recognized only by an exact string** | The model writes "OK", the gateway sends you an "OK" message | Prefix matching **and** a minimum content length |
| **P107** | **No night silence and no daily limit** | The agent wakes you at 3:00 with urgency 2 | Night silence, daily limit, minimum gap — all three |
| **P108** | **No circuit breaker after a series of errors** | A broken task grinds on over the weekend and floods the log | 3 errors in a row → disable the schedule and notify **once** |

---

## 11. Checkpoint

```bash
cd $OSA
systemctl --user is-active osa-planista && echo "✓ scheduler running"
python3 - <<'EOF'
from harmonogram.planista import _klucz_wykonania, parsuj
import datetime
z = {"naglowek":"Co rano (7:00)","typ":"dziennie"}
a = _klucz_wykonania("gospodarz", z, datetime.datetime(2026,9,23,7,0))
b = _klucz_wykonania("gospodarz", z, datetime.datetime(2026,9,23,7,5))
assert a == b, "P105: restart will run the task again"
print("✓ per-window idempotency")
EOF
python3 sesja-cli.py harmonogram status
test -s pomiary/gospodarz-tydzien.csv && echo "✓ week measured"
git add -A && git commit -m "part 11: scheduler, HEARTBEAT, silence suppression, circuit breaker"
```

- [ ] `HEARTBEAT.md` written in sentences, with a "Never report" section
- [ ] `HEARTBEAT_OK` suppressed by the gateway; silence is the **default** response
- [ ] Per-window idempotency — a restart does not repeat the task
- [ ] Event triggers wherever possible; time triggers only for reviews
- [ ] Urgency threshold, daily limit, night silence, minimum gap
- [ ] The night task runs the evaluation and stays quiet unless a regression
- [ ] The circuit breaker disables the schedule after 3 errors and notifies once
- [ ] A scheduled task **does not have** host permissions
- [ ] ⭐ **Week measured: you know precision, recall and silence ratio**

---

**Next: `12-CHANNELS-INTERFACES.md`** — how you talk to the agent and why the channel is a
trust boundary, not just an input.
