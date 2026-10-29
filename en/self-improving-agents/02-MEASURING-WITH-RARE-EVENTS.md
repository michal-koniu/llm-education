# 02 · Measuring with rare events

**The central fact:** when the outcome you care about is rare, a handful of rounds says almost nothing about whether a
change helped. Every rule in [03](03-THE-SAFE-LOOP.md) and [04](04-KNOWING-WHEN-TO-STOP.md) follows from this page.
All (C) numbers come from [`tools/rare_event_stats.py`](tools/README.md); run it with your own rates.

The model throughout: hits arrive as a **Poisson process** with rate λ per round. That is a simplification (markets
have hours, weekdays and seasons), but it is the right first approximation, and reality is noisier, not cleaner.

---

## 1. How noisy is "nothing found"?

If the current playbook finds hits at rate λ per round, the probability of k empty rounds in a row is e^(−λk) **(C)**:

| λ (hits/round) | P(2 empty) | P(3 empty) | P(5 empty) | P(10 empty) | empty run needed for p < 0.05 | for p < 0.01 |
|---|---|---|---|---|---|---|
| 0.1 | 0.82 | 0.74 | 0.61 | 0.37 | 30 | 47 |
| 0.2 | 0.67 | 0.55 | 0.37 | 0.14 | 15 | 24 |
| 0.3 | 0.55 | 0.41 | 0.22 | 0.05 | 10 | 16 |
| 0.5 | 0.37 | 0.22 | 0.08 | 0.01 | 6 | 10 |
| 1.0 | 0.14 | 0.05 | 0.01 | ~0 | 3 | 5 |

**What this means (I).** A trigger like "reflect and rewrite after 2–3 empty rounds" fires on pure chance unless the
agent already finds about one hit per round. Each rewrite is a fresh chance to break something, and the next lucky
round then "confirms" the rewrite. That is the recipe for an agent that drifts while believing it improves: a random
walk with a story attached.

Replace the trigger with one of:

- a run-length rule calibrated to the measured rate: k ≥ ln(1/p) / λ̂, with p = 0.01;
- better, the Poisson CUSUM in [§5](#5-watching-for-a-drop-poisson-cusum), which also uses the hits that do occur;
- for anything else, the evidence-gated triggers in [04 §1](04-KNOWING-WHEN-TO-STOP.md#1-evidence-gated-triggers).

## 2. How many hits to show a change helped?

Run the **champion** (current playbook, A) and a **challenger** (B) with equal exposure, for example by alternating
or randomising rounds. Now condition on the total number of hits n. If B is no better, each hit is equally likely to
have come from A or B, so the comparison is an exact binomial test with p0 = 0.5. If B's rate is R times A's, a hit
comes from B with probability p1 = R/(1+R). This is the conditional test that R's `poisson.test` implements **(S)**.

Total hits needed for 80% power, one-sided **(C)**:

| Effect to detect | α = 0.05: total hits | rounds per arm at λ = 0.1 / 0.3 / 1.0 | α = 0.10: total hits | rounds per arm at λ = 0.1 / 0.3 / 1.0 |
|---|---|---|---|---|
| +25% (R = 1.25) | 502 | 2232 / 744 / 224 | 370 | 1645 / 549 / 165 |
| +50% (R = 1.5) | 158 | 632 / 211 / 64 | 115 | 460 / 154 / 46 |
| ×2 | 58 | 194 / 65 / 20 | 39 | 130 / 44 / 13 |
| ×3 | 23 | 58 / 20 / 6 | 19 | 48 / 16 / 5 |

**Read this table before you design anything (I):**

- At 0.1–0.3 hits per round, even a *doubling* needs 44–194 rounds per arm to confirm. At one round every 15 minutes
  that is about half a day to two days per arm, *if the world holds still*.
- A +25% gain is practically unmeasurable from hit counts.
- An agent that rewrites its playbook every few rounds therefore cannot know whether any rewrite helped.
- Unequal splits cost extra. Giving the challenger a fraction f of rounds instead of half inflates the total by about
  1/(4f(1−f)): ×1.33 at f = 0.25 **(C)**. It is still worth doing to cap the downside of a bad challenger.

## 3. Ways out, in order of value

**1. Evaluate whatever you can offline, on frozen data.** Judgment logic (item matching, the reference price, red
flags, the hit threshold) can be replayed on archived listings. Every candidate the agent ever looked at becomes a
labelled example: hundreds per week instead of a few hits. See the golden set and snapshot corpus in
[03 §3](03-THE-SAFE-LOOP.md#3-frozen-evaluation-assets).

**2. Use denser leading indicators online.** For example near-misses (listings within some percentage of the hit
threshold), qualified candidates per round, catalogue coverage. At 5 near-misses per round, a +25% change needs about
502 / (5 × 2.25) ≈ 45 rounds per arm instead of 744 **(C)**. Proxies are easy to game
([03 §9](03-THE-SAFE-LOOP.md#9-goodhart-what-gaming-looks-like-and-the-structural-guard)), so use them only to
*accelerate* a decision; the primary metric must still pass a non-inferiority check.

**3. Do not test small changes online at all.** Batch them into an offline-validated release, or let the bandit
([03 §5](03-THE-SAFE-LOOP.md#5-a-bandit-for-allocation-instead-of-rewrites)) absorb them as allocation.

**Replay has a hard limit (S, Li et al. 2011).** Offline replay of logged data is unbiased only where the new policy
would have taken the same action as the logged one. A replay can score a new *filter* on old search results. It
cannot score a *query nobody ran*. So **changes to judgment can be tested offline; changes to queries and sources must
be tested online**, through the bandit or a switchback **(I)**.

## 4. Decision rules for small, noisy samples

**Use exact or Bayesian methods, not CLT error bars, when n is small.** Bowyer, Aitchison & Ivanova (ICML 2025) show
that the usual mean ± 1.96·SE intervals "dramatically underestimat[e] uncertainty" below "a few hundred datapoints"
**(V, abstract)**.

**Pair everything you can.** Score champion and challenger on *the same* items. Miller ("Adding Error Bars to Evals")
gives paired and clustered standard errors; clustered ones can be more than 3× the naive ones **(S)**. For an agent,
cluster by day or by source, because rounds on the same day share market conditions **(I)**.

**For a golden set, use an exact McNemar test.** Count b = items the champion gets right and the challenger wrong,
and c = the reverse. Items both get right or both get wrong carry no information. Under "no difference", c is
Binomial(b + c, 0.5). Accept a claimed improvement only if c > b and the one-sided p < 0.05:

```bash
python3 tools/rare_event_stats.py mcnemar --b 3 --c 11      # p = 0.029 → accept
python3 tools/rare_event_stats.py mcnemar --b 20 --c 23     # fixes 23, breaks 20 → p = 0.38 → reject
```

**You will peek, so use a sequential test.** You will look at results after every round, and a fixed-horizon p-value
is invalid under continuous monitoring. Johari, Pekelis & Walsh's mixture SPRT gives "always-valid" p-values **(S)**.
The simplest valid option for hit attribution is **Wald's SPRT on which arm each hit came from (C)**:

- Design for a ratio R. With challenger share f of the rounds: p0 = f and p1 = Rf / (1 − f + Rf). With equal
  exposure this is p0 = 0.5, p1 = R/(1+R).
- Each challenger hit adds ln(p1/p0). Each champion hit adds ln((1−p1)/(1−p0)). Empty rounds add nothing.
- Accept the challenger when the sum reaches ln((1−β)/α); reject it when it falls to ln(β/(1−α)).
  With α = 0.05, β = 0.2 the bounds are **+2.77 and −1.56**.

Simulated behaviour, equal exposure **(C)**:

| Design | Per challenger hit | Per champion hit | If the challenger is no better | If the challenger is as good as designed |
|---|---|---|---|---|
| R = 2 | +0.288 | −0.405 | wrongly accepted 4.6%; decides after ~26 hits (90th percentile 54) | accepted 83%; after ~37 hits (90th percentile 70) |
| R = 1.5 | +0.182 | −0.223 | wrongly accepted 4.6%; ~71 hits | accepted 82%; ~101 hits |

That is roughly half the 58 hits of the fixed test in §2, *and* you are allowed to look after every hit.

**The Bayesian alternative.** Keep a Gamma posterior per arm, compute P(λ_B > λ_A | data), and stop when the expected
loss of picking the leader drops below a "threshold of caring" (Stucchio). It is easy to explain but does *not* control
false positives under optional stopping **(S)**. Combine it with a minimum sample and a maximum duration **(I)**.

**Bootstrap only for heavy-tailed value metrics**, such as value per round, and only as a **block bootstrap by day**.
It is unreliable with fewer than ~20 hits per arm, so treat value as a guardrail, not as the decision metric **(I)**.

**Discount the winner's curse.** If the reflector generates k candidate changes and you keep the best-looking one,
its measured lift is biased upwards (Lee & Shen, KDD 2018) **(S)**. Test one challenger at a time; if several were
screened offline, require confirmation in a fresh window; when forecasting, halve the measured lift **(I)**.

**Twyman's law.** Any figure that looks interesting or different is usually wrong (Kohavi et al.). A challenger that
"triples hits" should trigger an audit for gaming, a logging bug or a changed definition before it triggers promotion.

**pass^k on nondeterministic runs.** If your runtime is not bit-reproducible (llama.cpp with prompt caching is not,
see [03 §12](03-THE-SAFE-LOOP.md#12-harness-and-runtime-notes)), a single run of the golden set is one sample, not a
score. Require all of k ≥ 3 runs to pass on must-pass items, or a majority of k elsewhere.

## 5. Watching for a drop: Poisson CUSUM

To notice that the hit rate fell from λ0 to λ1, keep one number S, starting at 0, and after each round with x hits
update (Page 1954; Lucas 1985, "Counted Data CUSUMs") **(S)**:

```
S = max(0, S + x·ln(λ1/λ0) − (λ1 − λ0))        alarm when S > h
```

Each empty round adds λ0 − λ1; each hit subtracts. In code it is three lines:

```python
import math
def cusum_step(S, hits, lam0=0.3, lam1=0.15):
    return max(0.0, S + hits * math.log(lam1 / lam0) - (lam1 - lam0))
```

Simulated run lengths **(C)**:

| Watching for | h | Mean rounds to a false alarm | 10th percentile of false alarm | Mean rounds to detect the drop |
|---|---|---|---|---|
| 0.3 → 0.15 | 3 | ~430 | 71 | ~51 |
| 0.3 → 0.15 | 4 | ~1270 | 178 | ~72 |
| 0.3 → 0.15 | 5 | ~3590 | 448 | ~95 |
| 1.0 → 0.5 | 3 | ~180 | 27 | ~17 |
| 1.0 → 0.5 | 4 | ~530 | 73 | ~23 |

Even a well-tuned detector needs **~50–100 rounds** to confirm that a 0.3 rate has halved. That is the honest latency
of rare-event monitoring, and no cleverness removes it. A reasonable default at λ0 = 0.3 is h ≈ 4: a false alarm
roughly every 1,300 rounds. Recompute λ0 whenever the champion changes **(C/I)**.

**For continuous metrics** (median price gap, listings per query, seconds per round), use **Page–Hinkley**:
m_T = Σ(x_t − x̄_T − δ), M_T = min m_t, alarm when m_T − M_T > λ. δ tolerates small fluctuations; λ trades false
alarms against delay (Gama et al. 2014 survey; scikit-multiflow defaults δ = 0.005, λ = 50) **(S)**.

**Health checks come before statistics.** Most "drift" in a scraping agent is breakage: a changed page layout, a
block or rate limit, an expired login. Track zero-result queries, parse-error rate and HTTP error rate with plain
thresholds. These events are frequent and binary; they need no CUSUM **(I)**.

## 6. Zero events and new sources

With 0 hits in n rounds, the 95% upper bound on the rate is about **3/n** (the "rule of three") **(C)**. 30 empty
rounds on a new source still allow a rate of up to 0.1 per round, which may be as good as your best source. Never
retire a new source on a short empty run; give it a guaranteed trial budget
([03 §5](03-THE-SAFE-LOOP.md#5-a-bandit-for-allocation-instead-of-rewrites)).

## 7. Exercises

Run these with *your* agent's numbers. Write the answers down before you design the loop.

```bash
cd en/self-improving-agents/tools
python3 rare_event_stats.py empty --rates 0.15                  # how long an empty run is real evidence?
python3 rare_event_stats.py power --ratios 1.25 1.5 2 --rates 0.15 --proxy 4
python3 rare_event_stats.py sprt --ratio 1.5 --share 0.25       # a 25% challenger share
python3 rare_event_stats.py cusum --rate0 0.15 --rate1 0.075 --h 3 4
python3 rare_event_stats.py shadow --max-n 30                   # see 03 §7
```

1. With your measured λ, how many rounds per arm would a +50% change need? How many calendar days is that?
2. How many changes of that size could you validate in a month? That number is your **evaluation budget**, and the
   reflection rate should match it ([03 §11](03-THE-SAFE-LOOP.md#11-who-reflects-and-how-often)).
3. Which denser proxy could you log from tomorrow, and what would it do to question 1?

---

Next: [03 · The safe loop](03-THE-SAFE-LOOP.md).
