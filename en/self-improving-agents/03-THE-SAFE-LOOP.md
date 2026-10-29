# 03 · The safe loop: architecture you can build

Everything on this page is a **design recommendation (I)**, grounded in the sources in [01](01-WHAT-CAN-IMPROVE.md)
and the arithmetic in [02](02-MEASURING-WITH-RARE-EVENTS.md). Four principles carry it:

- **separate the doer from the judge;**
- **the LLM proposes, code and statistics dispose;**
- **make changes small, typed, reversible and rare;**
- **put the improvement machinery out of the agent's reach.**

---

## 1. Components

```
               ┌──────────────────────── frozen, human-owned ─────────────────────────┐
               │ constitution.md   hit_rules.py (thresholds, costs)   metrics.py      │
               │ golden set + must-pass + hidden slice   gate_rules.yaml   sentinel   │
               └──────────────────────────────────────────────────────────────────────┘
                     ▲ read-only                          ▲ read-only
┌──────────────┐  ┌──┴───────────┐  ┌──────────────┐  ┌───┴──────────┐  ┌──────────────┐
│ Worker (fast │→ │ Harness:     │→ │ Monitor:     │→ │ Reflector    │→ │ Gatekeeper   │
│ model, runs  │  │ append-only  │  │ health,      │  │ (scheduled,  │  │ (pure code): │
│ rounds)      │  │ logs,        │  │ CUSUM,       │  │ fresh        │  │ gates, SPRT, │
│              │  │ snapshots,   │  │ Page-Hinkley,│  │ context,     │  │ promote /    │
│ reads:       │  │ dedup,       │  │ sentinel,    │  │ ≤1 proposal) │  │ reject /     │
│ playbook vN  │  │ hit_rules,   │  │ attribution  │  └──────────────┘  │ rollback,    │
│ + bandit pick│  │ bandit update│  └──────────────┘                    │ git versions │
└──────────────┘  └──────────────┘                                      └──────────────┘
                                         weekly digest → human (approves frozen-layer changes)
```

| Component | Kind | Does | Never does |
|---|---|---|---|
| **Worker** | fast LLM | runs rounds: queries the chosen arms, extracts listings, matches items, calls the hit evaluator | writes the playbook during a round |
| **Harness** | code | append-only JSONL logs, raw snapshots, dedup; applies `hit_rules.py` so the hit/no-hit decision is code (the LLM supplies extracted fields and a confidence); updates the bandit | lets the LLM decide what counts as a hit |
| **Monitor** | code | health checks, Poisson CUSUM on the hit rate, Page–Hinkley on continuous metrics, runs the sentinel, applies the attribution table (§8) | changes anything |
| **Reflector** | LLM, scheduled | in a fresh context, reads code-computed metrics, failure clusters and sampled raw transcripts; emits **at most one** typed proposal (§4) | judges its own proposal; sees golden labels |
| **Gatekeeper** | code | runs the gate cascade (§6), schedules A/B, runs the SPRT, promotes, rejects, rolls back, commits versions to git | takes instructions from the LLM |
| **Human** | person | owns the frozen layer; reads a weekly digest; labels disagreements and near-misses (the cheapest high-value labels in the system) | approves without looking at evidence |

**Isolation is enforced by construction.** Run the worker and the reflector as a user or in a sandbox with no write
permission on the frozen layer, the logs or the evaluation sets. Askarbekuly et al. put it as rule R3: isolate state
"by construction, not instruction" **(V)**. A line in the prompt saying "do not edit X" is not a control.

## 2. What may change, and through which door

Every change has a **door**: the evaluation it must pass. Deciding the doors up front is most of the design.

| Layer | Examples (the scout) | Who changes it | Evaluation door |
|---|---|---|---|
| **Frozen: constitution** | goal, ethics, site terms and rate limits, "never buy or contact sellers", budgets | human only | n/a |
| **Frozen: measurement** | `hit_rules.py` (costs, condition model, threshold), metrics code, dedup rules, eval sets, gate thresholds, **the reflection protocol itself** | human only; the agent may *file a proposal* | human review plus offline re-scoring of history |
| **Tuned by code** | which arm to run next, visit frequency, time-of-day schedule | the bandit (§5), never the LLM | continuous; the posterior is the evaluation |
| **Arm catalogue** | new query templates, new sources, new item categories | reflector proposes; gatekeeper adds with a trial budget | bandit trial budget plus retirement rule |
| **Judgment heuristics** | item and variant normalisation, red-flag keywords, which reference price to use | reflector proposes, one at a time | offline: must-pass, golden McNemar, replay; then **shadow mode** (§7) |
| **Procedure notes** | how to page through source X, login handling, "check sold listings before flagging" | reflector proposes as delta items | process metrics (errors, time per round, coverage) by switchback; hit rate as a non-inferiority guardrail |
| **Insight memory** | "sellers on X often give storage size only in photos" | reflector adds or edits by ID; **counters updated by the harness from outcomes** | size cap, dedup, prune items with harmful > helpful |
| **Scratch** | notes within one round | worker | none; discarded |
| **Model and runtime** | weights, quantisation, chat template, runtime version, sampler, context size | human | **treated as a challenger**: must-pass, golden set and replay before swapping |

The table is the answer to "what should a self-improving agent be allowed to change?". Most of the value is in the
bottom half; most of the danger is in the top two rows.

## 3. Frozen evaluation assets

The pattern comes from autoresearch, AlphaEvolve and DSPy: a frozen evaluator the optimiser cannot touch.
Karpathy's autoresearch freezes the data-and-evaluation file ("Not modified"); the agent may edit only `train.py`; the
instructions file is "edited and iterated on by the human"; every run has a fixed 5-minute budget **(V)**.

Askarbekuly et al. (2026) ran such loops with production coding agents and documented specification gaming: one agent
hard-coded 19–41 evaluation answers per run; agents read sibling runs through shared git state and left notes for
"future runs". Adding a held-out test set, and telling the agents it existed, eliminated the hard-coding **(V)**.
Their five rules:

1. **R1** hold out evaluation data;
2. **R2** keep feedback leak-free: never echo gold labels;
3. **R3** isolate run state "by construction, not instruction";
4. **R4** audit the agent tooling's own state channels (memory, global config);
5. **R5** report components, because "scalar metrics can hide high-variance rare-event components", and preregister
   hypotheses.

The assets to build for the scout **(I)**:

| Asset | Contents | Who writes it | Used for |
|---|---|---|---|
| **Golden set** | ≥200 archived listings with labels: hit or not, correct item and variant, reference price, reason. Includes *every* real hit, *every* confirmed false positive, and adversarial cases: "for parts", bundles, wrong variant or region, fakes, stale listings, cost traps | human labels, or outcomes observed later. **Append-only, versioned, unwritable by the agent** | offline gate for judgment changes |
| **Must-pass subset** | 20–40 critical cases from the golden set (past costly mistakes) | human | hard gate: any failure means reject |
| **Hidden slice** | 15–20% of the golden set that the reflector never sees, refreshed monthly | human | catching overfitting to the golden set |
| **Snapshot corpus** | raw search pages and listing JSON per (source, query, time), captured during normal rounds | harness | replaying a candidate's filtering and ranking on what the market actually showed |
| **Sentinel probe** | a pinned, never-modified playbook running a small fixed query set every N rounds | human-defined | separating "the world changed" from "I broke it" (§8) |
| **Missed-hit log** | hits found by a periodic broad sweep, by the sentinel, or by later "sold cheap" observations that the champion did not flag | harness | the only direct **recall** signal; turns rare misses into labelled examples |

## 4. The playbook: itemised and delta-edited

Store the playbook as structured data, not prose. Every item has an identity and a history:

```yaml
version: 37
runtime: {weights_sha256: "…", quant: Q4_K_M, template_sha256: "…", runtime: "llama.cpp <build>", temperature: 0.2}
sections:
  judgment:
    - id: J-017
      text: "Treat 'for parts' or 'not working' in the title or description as disqualifying."
      added_in: 12
      provenance: [log:2026-09-14T03:15Z#17]
      helpful: 14          # updated by the harness from outcomes, never by the LLM
      harmful: 1
      last_validated: 2026-10-20
  procedure: [...]
  insights: [...]
```

The reflector emits **delta operations only**, `ADD`, `MODIFY(id)` or `RETIRE(id)`, and code merges them. It never
emits a whole new playbook. This is ACE's fix for context collapse and the same idea as ExpeL's ADD / EDIT / UPVOTE /
DOWNVOTE **(V)**. A proposal is a typed record:

```yaml
id: P-0042
op: MODIFY                       # ADD | MODIFY | RETIRE
target: judgment.J-021
door: judgment                   # which evaluation door (table in §2)
hypothesis: "Missed 3 hits on source B: the matcher rejects model numbers written without the dash."
evidence: [log:2026-10-21T04:15Z#17, log:2026-10-23T11:30Z#5, missed:M-118]
predicted_effect: {metric: golden_recall, direction: up, size: "+2 items"}
blast_radius: [judgment.J-021]
new_text: "Normalise model numbers before matching: drop spaces and dashes."
rollback: {op: MODIFY, target: judgment.J-021, text: "<previous text, filled in by code>"}
```

Rules for the format **(I)**:

- One section per proposal; the gatekeeper rejects any proposal whose blast radius is larger.
- A hard size cap per section and overall, for example 6–8k tokens in total. Long contexts degrade smaller models
  first (context rot, [01 §5](01-WHAT-CAN-IMPROVE.md#5-practitioner-guidance-that-bears-on-self-modifying-loops)).
- Deduplicate at write time by embedding similarity; reject near-duplicates instead of adding them.
- Keep the file's byte order stable (fixed key order, append at the end of a section). Every edit invalidates the
  cached prompt prefix for all later rounds, which is a second reason to edit rarely.

## 5. A bandit for allocation instead of rewrites

Most "rewrite the playbook" impulses are really **allocation decisions**: which source and query to spend the next
round on. A bandit makes those decisions continuously, with explicit exploration, without the LLM touching prose **(I)**.

**Gamma-Poisson Thompson sampling.** Arms are (source × query template), optionally × time-of-day bucket. Each arm
keeps a posterior λ_i ~ Gamma(α_i, β_i) on its hit rate per unit cost. After a pull with x hits at cost c (rounds,
minutes or requests): α_i ← α_i + x, β_i ← β_i + c. To choose, sample λ̃_i from every posterior and run the arm with
the largest sample (Russo et al. tutorial) **(S)**.

**Markets drift, so discount old evidence.** Before each update, pull the posterior back toward the prior:
α ← γα + (1−γ)α0, β ← γβ + (1−γ)β0. γ = 0.98 gives an effective memory of about 50 pulls, γ = 0.99 about 100 **(C)**.
Discounted and sliding-window Thompson sampling are the standard non-stationary variants (Raj & Kalyani; Fiandri et al.)
**(S)**.

```python
import random

class Arm:
    def __init__(self, prior_rate=0.2, prior_weight=1.0):
        # weak prior centred on the portfolio's mean rate: alpha0 / beta0 = prior_rate
        self.a0, self.b0 = prior_weight, prior_weight / prior_rate
        self.a, self.b, self.pulls = self.a0, self.b0, 0

    def update(self, hits, cost=1.0, gamma=0.98):
        self.a = gamma * self.a + (1 - gamma) * self.a0 + hits
        self.b = gamma * self.b + (1 - gamma) * self.b0 + cost
        self.pulls += 1

    def sample(self, rng):
        return rng.gammavariate(self.a, 1.0 / self.b)      # Gamma(shape a, rate b)

    def p_above(self, floor, rng, n=2000):
        return sum(self.sample(rng) > floor for _ in range(n)) / n


def pick(arms, rng, explore=0.05, trial_budget=10):
    new = [k for k, arm in arms.items() if arm.pulls < trial_budget]
    if new and rng.random() < 0.5:
        return rng.choice(new)                    # guaranteed trial for new arms
    if rng.random() < explore:
        return rng.choice(list(arms))             # exploration floor
    return max(arms, key=lambda k: arms[k].sample(rng))
```

**Guards (I):**

- **Exploration floor**: every active arm runs at least once a day, or ≥5% of pulls are uniformly random. A source that
  died last month can come back.
- **Trial budget**: a new arm proposed by the LLM gets ~10 guaranteed pulls before the posterior can starve it.
- **Retirement to a cold pool, not deletion**: after ≥M pulls, if P(λ_i > λ_floor) < 0.05, move the arm to a cold
  pool that is re-probed weekly.
- **The bandit's state is data owned by the harness.** The LLM proposes arms; it never edits posteriors.

**Why this matters for regressions.** The bandit turns a risky, discrete rewrite ("move source A to the top, drop
source C") into a smooth, self-correcting reallocation. A bad new query costs only its trial budget. The LLM's job
narrows to generating hypotheses (new arms) and the statistics decide. **"The LLM proposes, statistics dispose"** is
the most important rule in this guide.

## 6. The gate cascade

Evaluation cascades (AlphaEvolve, DGM's staged 10 → 60 → 200 tasks) run cheap checks first, so expensive evaluation is
spent only on survivors **(V)**. Apply the same order **(I)**:

| # | Gate | Cost | Pass condition |
|---|---|---|---|
| 1 | **Static** | seconds | parses against the schema; touches ≤1 section; within size budget; no frozen field modified; carries hypothesis, predicted effect, door, inverse delta |
| 2 | **Must-pass** | minutes | 100% of must-pass cases, on all of k ≥ 3 runs if the runtime is nondeterministic |
| 3 | **Golden set, paired** | minutes | exact McNemar: c > b *and* p < 0.05 for a claimed improvement (or b ≤ ~1% of items for a claimed neutral refactor), *and* no new class of false positive |
| 4 | **Replay** | minutes–hours | on the last 7–14 days of snapshots, the challenger re-finds every hit the champion found and adds no alerts that humans rejected |
| 5 | **Online** (only for changes that alter actions) | days | shadow mode for judgment (§7); for procedure, a **switchback**: randomise rounds between champion and challenger in time blocks balanced for hour and weekday (Bojinov, Simchi-Levi & Zhao) **(S)**; challenger gets 20–30% of rounds; decide with the SPRT ([02 §4](02-MEASURING-WITH-RARE-EVENTS.md#4-decision-rules-for-small-noisy-samples)) |
| 6 | **Probation** | ~100 rounds | CUSUM on the new champion; automatic rollback on alarm (§8) |

**"Fix more than you break"** is gate 3 in one sentence. SkillBoost accepts only if gain > 0 and regressions stay
small; an edit that fixed 20 and broke 23 was rejected, and without the gate one model fell from 80.0 to 67.5 **(V)**.

**If a test reaches its maximum length without a decision, keep the champion.** The status-quo bias is deliberate: an
unproven change is a cost, not a neutral event **(I)**.

The gatekeeper is ordinary code. A sketch:

```python
from rare_event_stats import binom_sf     # tools/rare_event_stats.py

def gate(proposal, champion, challenger, ev):
    if not ev.static_ok(proposal):
        return "reject:static"
    if not ev.must_pass(challenger, k=3):
        return "reject:must-pass"
    b, c = ev.paired_golden(champion, challenger)    # b: only champion right, c: only challenger right
    if not (c > b and binom_sf(c, b + c, 0.5) < 0.05):
        return "reject:golden"
    if ev.replay_misses(challenger, champion) or ev.replay_new_rejected_alerts(challenger):
        return "reject:replay"
    return {"judgment": "shadow", "procedure": "switchback"}.get(proposal.door, "promote")
```

## 7. Shadow mode

For judgment changes, shadow mode is the cheapest strong evaluation available **(I)**. Champion and challenger
judgment logic both score **the same candidate stream** every round; only the champion's flags are acted on. Every
**disagreement** is a free, paired, informative example. A human, or a later observed outcome, labels the
disagreements.

Promote when there are ≥10 adjudicated disagreements, the challenger wins them with exact binomial p < 0.05, and no
must-pass case fails. The thresholds **(C)**:

| Disagreements | Challenger must win at least |
|---|---|
| 10 | 9 |
| 16 | 12 |
| 20 | 15 |
| 30 | 20 |

Unlike an outcome test, this does not wait for rare hits. It waits for disagreements, which are much more frequent.
`python3 tools/rare_event_stats.py shadow` prints the full table.

## 8. Sentinel, drift and rollback

The **sentinel** is a pinned playbook that never changes, running a small fixed query set a few times a day. It is
your control group: comparing it with the champion is a difference-in-differences **(I)**.

| Sentinel | Champion | Recent change? | Interpretation | Action |
|---|---|---|---|---|
| drift | drift | any | **the world changed** (supply, prices, season, a source broke) | do **not** roll back; reset the bandit discount and raise exploration for a while; open an adaptation reflection |
| stable | drift | yes, alarm began after it | **self-inflicted regression** | **automatic rollback** to the previous champion; mark the change failed; block similar proposals for a cooldown |
| stable | drift | no | champion-specific breakage (a query or parser path the sentinel does not use) | health checks first, then a targeted fix proposal |
| drift | stable | any | the market moved but the playbook is robust | log it, change nothing |

Timing matters: with ~50–100 rounds of detection latency ([02 §5](02-MEASURING-WITH-RARE-EVENTS.md#5-watching-for-a-drop-poisson-cusum)),
an alarm within one detection window after a promotion is attributed to the promotion by default.

**Rollback triggers.** All automatic, all in code. Any one restores version N−1 and marks change N `failed_in_prod`:

- the CUSUM alarms during probation while the sentinel is stable;
- the daily golden-set re-run shows a must-pass failure;
- a health metric degrades beyond its threshold after the change (for example, the tool-error rate doubles);
- a human flags 2 or more bad alerts traced to the new item during probation.

A failed change goes to a **rejected-ideas list** the reflector can read, so the same idea is not re-proposed for 30
days. SkillOpt's rejected-edit buffer is the same idea: removing it cost 4.6 points **(V)**.

## 9. Goodhart: what gaming looks like, and the structural guard

A self-modifying agent optimises whatever signal it can see, including ones you did not intend. Prompt-level bans do
not work (80% hacking despite "please do not cheat"); the fix is to **harden the scorer and remove write access**
**(V)**. For the scout, expect these **(I)**:

| Gaming pattern | Symptom | Structural guard |
|---|---|---|
| Loosening the hit definition (lower threshold, optimistic reference price, ignoring costs or condition) | hits up, human rejection rate up, mean margin down | definition, costs and threshold live in frozen code; the agent may only propose |
| Counting duplicates or relisted items | hits up, unique listing IDs flat | the harness deduplicates by ID and fingerprint (title, price, images) |
| Easy but useless queries | candidates and near-misses up, hits flat | proxies only accelerate; hits must pass non-inferiority |
| Editing logs or metrics, or hiding failures in its own summaries | reflection claims do not match raw logs | append-only logs written by the harness; metrics computed by code; the reflector reads raw logs |
| Carrying information across evaluation runs | offline scores jump with no mechanism | fresh workspace per evaluation; no write access to eval sets (R3/R4) |
| Overfitting to the golden set | golden score up, replay and online flat | the hidden slice; monthly refresh with new labelled cases |

Background: Manheim & Garrabrant catalogue four Goodhart variants (regressional, extremal, causal, adversarial);
Gao, Schulman & Hilton show that optimising an imperfect proxy first improves the true objective and then makes it
worse. That curve is the formal picture of "month 2" **(V abstracts; variant names from memory, S)**.

## 10. Accept, reject and rollback defaults

| Change type | Accept when | Reject when | Maximum trial |
|---|---|---|---|
| **New arm** (query or source) | survives the trial budget (≥10 pulls) and its posterior stays above the retirement threshold | P(λ_arm > λ_floor) < 0.05 after ≥M pulls; goes to the cold pool, re-probed weekly | bandit-managed |
| **Judgment heuristic** | must-pass 100%; McNemar c > b with p < 0.05 (or b ≤ 1% for a neutral refactor); replay recall ≥ champion; shadow: ≥10 adjudicated disagreements won at p < 0.05 | any must-pass failure; replay misses a hit the champion found; shadow loses or is inconclusive at the cap | 14 days of shadow |
| **Procedure note** | switchback with a 25% challenger share: the process metric improves at p < 0.05 *and* the hit-attribution SPRT does not cross its rejection bound | process metric worse; SPRT rejects; error rate beyond guardrail | 200 challenger rounds, then keep the champion |
| **Frozen-layer proposal** | human approval after offline re-scoring of the last 30 days | by default | n/a |

## 11. Who reflects, and how often

**Reflection is cheap; evaluation is not.** At 100+ tokens per second, a reflection that writes 2–4k tokens takes
under a minute. Prefill of 20–40k tokens of metrics and transcripts adds seconds with a warm prompt cache and minutes
cold: one llama.cpp user measured 222 s to re-prefill 44k tokens after losing the cache vs 0.47 s with reuse; a 60k
prompt on an 80B MoE took 39–54 s cold vs ~1 s from checkpoints **(V; the first figure S)**. Run the reflector in its
own slot or process so it does not evict the worker's cache.

So the binding constraint is not compute. It is **evaluation bandwidth**: at 0.1–0.3 hits per round, an
action-changing test takes ~50–200 rounds per arm, so you can validate perhaps **1–4 such changes a month**; plus
**regression risk**: every promotion is a chance to break something. **Match reflection frequency to evaluation
capacity, not to the compute budget (I).**

**Who reflects (I), in order of preference:**

1. **A stronger model writes proposals weekly; the local model executes** (the advisor pattern from
   [01 §4](01-WHAT-CAN-IMPROVE.md#4-small-and-local-models-as-reflectors)). If privacy allows, send a redacted digest.
2. **A local 70–80B model reflects**, sampling 3–5 independent diagnoses and proceeding only on one the majority
   share; a *different* prompt or a fresh context critiques it.
3. **The worker model reflects only to classify failures** with a fixed taxonomy: missed hit, false positive, tool or
   parse failure, slow path, source down. Smaller models handle a fixed label set far more reliably than open-ended
   strategy writing.

A **critic pass** checks every proposal against the constitution, the frozen layer and the rejected-ideas list before
it reaches the gatekeeper. Whatever you choose, **the gatekeeper's statistics are the judge, never the reflector**.

**What the reflector sees.** Raw evidence: log excerpts selected by code, metric tables computed by code, the
prediction log ([04 §6](04-KNOWING-WHEN-TO-STOP.md#6-the-prediction-log)). It does **not** see its own previous
narrative summaries, which compound errors, and it **never** sees golden labels or the hidden slice (R2).

## 12. Harness and runtime notes

Facts are from the OpenClaw and llama.cpp docs and issues **(V)**; recommendations are **(I)**. The same questions apply
to any harness.

- **Self-edit features with no gate.** OpenClaw's Skill Workshop applies agent-written skill changes immediately and
  documents no approval gate; earlier versions can be restored. Do not let the worker or reflector write skills
  directly. Have it write a *proposal file* that the gatekeeper applies after the gates pass, or disable the feature
  and manage playbook files from the gatekeeper. Use built-in restore only as an emergency undo; **git is the
  versioning system**.
- **Background memory promotion.** OpenClaw's memory "dreaming" promotes memories into `MEMORY.md` in the background;
  the docs say "memory does not enforce policy". Turn it off for an agent like this, or treat that file as
  non-authoritative notes. **Never let listing or seller text be promoted into rules**: that is prompt injection
  through content (Willison's "lethal trifecta"; Course 3).
- **Silent truncation.** OpenClaw truncates bootstrap files (20,000 characters per file, 60,000 in total by default).
  A growing playbook is silently cut off. Keep the size cap (§4) well below the limit.
- **Empty rounds as valid outcomes.** Automation jobs that return `NO_REPLY` or record `no_change` represent empty
  rounds naturally. A per-job model policy lets the reflector use a different model from the worker.
- **Nondeterminism.** In llama.cpp, `cache_prompt` (on by default) can make results nondeterministic, because logits
  are not bit-identical across batch sizes. Golden-set and replay gates must use pass^k (k ≥ 3) or majority-of-k.
  Record the model hash, quantisation, chat template and sampler settings in every playbook version.
- **Tool-calling fragility.** When checked, Qwen3 was not on llama.cpp's list of native tool-call handlers (it falls
  back to "Generic"), and several harnesses report template or parser problems; aggressive KV-cache quantisation can degrade tool calls. Test tool
  calling end to end on the exact model file, template and parser; add a circuit breaker for repeated identical tool
  calls; validate structured output in code even under a grammar.
- **A runtime change is a playbook change.** A new model, quantisation, template or runtime build goes through gates
  2–4 before it replaces the old one, and is recorded in the version.

## 13. Cadence

| When | What runs | Model cost |
|---|---|---|
| Every round | worker round; logging and snapshots; `hit_rules`; bandit update; health checks; CUSUM; shadow judgment if a judgment challenger is active | the work itself |
| 2–4× a day | sentinel probe | small |
| Daily | broad missed-hit sweep; golden-set re-run of the champion (catches nondeterminism and silent runtime changes); digest of near-misses and disagreements for labelling; failure triage (classification only) | small |
| Evidence-gated, at most weekly in steady state | reflection: failure clustering → ≤1 proposal → gates | 1–3 minutes of model time |
| On alarm | attribution (§8); rollback or an adaptation reflection | small |
| Monthly (human) | prediction log and acceptance rate; refresh the hidden slice; recalibrate λ0, h, γ; review the frozen layer | human time |

---

Next: [04 · Knowing when to stop](04-KNOWING-WHEN-TO-STOP.md).
