# 04 · Knowing when to stop

A self-improving agent needs a way to tell that it is working well and should leave itself alone. This cannot be the
LLM's own judgment: same-model self-assessment "reliably skew[s] positive" **(V)**, and after a few unlucky rounds it
skews the other way. **"Working well" has to be a state that code computes from evidence.** This page defines that
state and the controller around it. Everything here is a design recommendation **(I)** unless tagged otherwise.

---

## What the evidence says about stopping

- autoresearch keeps a change only if it is strictly better and resets otherwise: a ratchet **(V)**.
- In Askarbekuly et al. (2026), the protocol's plateau rule was about 15 non-improving experiments. The agent the
  authors called the **generalizer** stopped by itself after 12–13, refused per-row special cases and labelled the
  residual failures "structurally unwinnable". The **metric-maximizer** kept going and turned failures into special
  cases **(V)**.
- Anthropic's skill-creator retires a skill when the base model passes without it **(V)**; Hermes Agent's Curator
  archives unused items and keeps LLM consolidation **off by default** **(V)**.
- Gao, Schulman & Hilton: optimising an imperfect proxy first helps the true objective, then hurts it **(V, abstract)**.

**Lesson (I): late-stage gains are disproportionately overfitting.** The longer a loop runs past its plateau, the more
of its "improvements" are noise it has memorised.

## When does the agent "know" it works well?

All five of these hold, each computed by code:

| Signal | Computed as | Why it means "leave it alone" |
|---|---|---|
| The champion is **within its band** | the posterior interval of its hit rate overlaps the trailing 30-day rate | nothing measurable has changed |
| **No alarm** is active | CUSUM, Page–Hinkley and health checks are all quiet | no evidence of a problem to fix |
| The **sentinel is stable** | its own metrics within band | the world has not shifted under you |
| **Recent challengers were rejected** | ≥3 rejections in a row | the local search around the champion is exhausted |
| **Remaining ideas are too small to measure** | predicted effect of every queued idea < the minimum detectable effect in 2 weeks (§5) | testing them would be a coin toss with a regression risk attached |

When they hold, the controller is in **maintenance** and the reflector is not even called. "Nothing found this round"
is not on the list, and never should be.

## 1. Evidence-gated triggers

A proposal is allowed only when at least one of these holds:

- a CUSUM or health alarm fired ([02 §5](02-MEASURING-WITH-RARE-EVENTS.md#5-watching-for-a-drop-poisson-cusum));
- the log holds a cluster of **≥3 same-cause failures** (missed hits, false positives, tool failures), as classified by
  the daily triage;
- a **new opportunity** appeared (a new source, a new item category);
- a **scheduled review** is due (weekly in the gated phase, monthly in maintenance);
- a **human** asked.

**Empty rounds alone are never a trigger.** Make "zero hits this round" an explicitly legitimate, unpenalised outcome,
both in the code and in the worker's prompt. Anthropic found that explicitly permitting a shortcut stopped learned
gaming from generalising **(V)**; the inference-time analogue is to stop treating silence as failure.

## 2. One change in flight

Never stack challengers. While a challenger is under test, the reflector may only **queue** ideas. Two edits landing
before either was evaluated make attribution impossible and rollback a guess. autoresearch's single editable file and
SkillOpt's edit budget enforce the same discipline **(V)**.

## 3. Probation and cooldown

After a promotion, the new champion is on **probation** for at least the CUSUM's detection time for a halving:
**~50–100 rounds at λ ≈ 0.3** ([02 §5](02-MEASURING-WITH-RARE-EVENTS.md#5-watching-for-a-drop-poisson-cusum)) **(C)**.
No proposals during probation. An alarm during probation, with the sentinel stable, rolls back automatically
([03 §8](03-THE-SAFE-LOOP.md#8-sentinel-drift-and-rollback)).

## 4. Exponential backoff after rejections

After each rejected challenger, **double the minimum interval** between reflections: 1 → 2 → 4 → 8 days, capped at 14.
Reset to the base interval after an accepted change or a drift alarm. A run of rejections is the system telling you
the easy improvements are gone.

## 5. Maintenance mode

Enter maintenance when either holds:

- **≥3 consecutive challengers were rejected**; or
- the **largest plausible effect** of the queued ideas is **below the minimum detectable effect within 2 weeks**.

A worked example of the second rule **(C)**: at one round every 15 minutes, 2 weeks is 1,344 rounds, 672 per arm.
From the table in [02 §2](02-MEASURING-WITH-RARE-EVENTS.md#2-how-many-hits-to-show-a-change-helped), at λ = 0.1 a +50%
change needs 632 rounds per arm (just detectable) and +25% needs 2,232 (not). At λ = 0.3, +50% needs 211 and +25%
needs 744 (not quite). So unless the reflector can argue for a gain of roughly +50% or more, an online test is not
worth running; the idea goes to the offline-only path or the backlog. Check your own numbers with
`python3 tools/rare_event_stats.py power --rates <your λ>`.

**In maintenance:**

- the **playbook is frozen**;
- the **bandit keeps adapting** allocation inside its safe bounds, so the agent still follows the market;
- monitors, the sentinel and the daily golden-set re-run keep running;
- only an alarm, a health failure, a human request or the monthly review reopens the playbook, and then only for
  **one targeted, gated change** (the ADAPT state below).

This is the target state. A working system should spend most of its life here.

## 6. The prediction log

Every proposal records its predicted effect (metric, direction, size). The log tracks:

- the reflector's **hit rate**: the share of proposals that pass all gates;
- the **calibration**: predicted vs measured effect for those that did.

If fewer than ~20% of proposals pass for a month, cut reflection frequency further or escalate reflection to a
stronger model ([03 §11](03-THE-SAFE-LOOP.md#11-who-reflects-and-how-often)). The log is also what the reflector
reads instead of its own past narratives.

## 7. The lifecycle

```
BOOTSTRAP ──(≥20 hits or 2 weeks, golden set ≥200)──► GATED IMPROVEMENT
    ▲                                                     │  ≥3 rejections in a row, or
    │                                                     │  plausible gain < 2-week MDE
    │                                                     ▼
 major world change ◄──(sentinel and champion drift)── MAINTENANCE  (playbook frozen;
 (new marketplace,                                     bandit and monitors keep running;
  model swap)                                          monthly human review)
                                                          │ alarm, health failure, human request
                                                          ▼
                                                   ADAPT (one targeted, gated change)
                                                          └──► back to MAINTENANCE
```

| State | What is allowed | Goal |
|---|---|---|
| **Bootstrap** | larger edits, evaluated mostly offline and by human review of flags; no online A/B (there is no baseline yet) | build the golden set, snapshot corpus, sentinel and the λ0 estimate |
| **Gated improvement** | everything in [03](03-THE-SAFE-LOOP.md): one change in flight, gates, probation, backoff | climb while the climb is measurable |
| **Maintenance** | bandit, monitors, sentinel; no playbook edits | stay good; this is where a working agent lives |
| **Adapt** | one change, scoped to the evidence that triggered it, through the full gates | respond to a real problem, then go back to maintenance |

A model or runtime swap, or a new marketplace, sends the system back to bootstrap for that part: it is a new baseline.

## 8. The controller in code

A sketch of the stopping logic. Triggers are a set of strings computed by the monitor; empty rounds never produce one.

```python
from dataclasses import dataclass
from datetime import datetime, timedelta

BASE, CAP = timedelta(days=1), timedelta(days=14)
REOPEN = {"cusum_alarm", "health_alarm", "human_request", "monthly_review"}


@dataclass
class Controller:
    state: str = "BOOTSTRAP"            # BOOTSTRAP | GATED | MAINTENANCE | ADAPT
    in_flight: str | None = None        # id of the one challenger under test
    probation_until: int = 0            # round number
    backoff: timedelta = BASE
    next_reflection: datetime = datetime.min
    rejections_in_row: int = 0

    def may_reflect(self, now: datetime, rnd: int, triggers: set[str]) -> bool:
        if self.in_flight or rnd < self.probation_until:
            return False                                  # one change in flight; cooldown
        if self.state == "MAINTENANCE":
            if triggers & REOPEN:
                self.state = "ADAPT"
                return True
            return False
        return now >= self.next_reflection and bool(triggers)

    def on_decision(self, now: datetime, rnd: int, accepted: bool, probation_rounds: int = 100):
        self.in_flight = None
        if accepted:
            self.rejections_in_row, self.backoff = 0, BASE
            self.probation_until = rnd + probation_rounds
        else:
            self.rejections_in_row += 1
            self.backoff = min(self.backoff * 2, CAP)
        self.next_reflection = now + self.backoff
        if self.state == "ADAPT" or (self.state == "GATED" and self.rejections_in_row >= 3):
            self.state = "MAINTENANCE"

    def on_alarm(self):
        self.backoff = BASE                               # alarms reset the backoff
```

The move from BOOTSTRAP to GATED, and back to BOOTSTRAP after a model swap, is a human decision: it needs the
evaluation assets to exist, which code cannot judge. The "plausible gain < 2-week MDE" rule belongs in the gatekeeper: it rejects a proposal before any test when its
predicted effect is below what the test could detect, and that rejection counts towards the three.

## 9. Checklist

- [ ] No code path turns "N empty rounds" into a reflection.
- [ ] The controller, not the LLM, decides whether a reflection happens.
- [ ] At most one challenger exists at any time.
- [ ] Probation length is derived from the measured CUSUM detection time, not guessed.
- [ ] Backoff doubles on rejection and resets on acceptance or alarm.
- [ ] Maintenance mode exists, is the default destination, and freezes the playbook while the bandit keeps working.
- [ ] Every proposal has a predicted effect in the log, and the monthly review reads it.

---

Next: [05 · Pitfalls](05-PITFALLS.md).
