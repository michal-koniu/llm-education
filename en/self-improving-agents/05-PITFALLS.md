# 05 · Pitfalls, in the order you will meet them

Twenty-five ways a self-improving loop goes wrong, grouped by when they usually show up. Items without a tag are
inference **(I)**; tagged items have direct evidence in [01](01-WHAT-CAN-IMPROVE.md) and [SOURCES](SOURCES.md).

---

## Weeks 1–2: design mistakes

| # | Pitfall | Symptom | Fix |
|---|---|---|---|
| 1 | **Reflecting on noise** | the playbook changes after a few empty rounds; each change is then credited or blamed by the next lucky or unlucky round | calibrated triggers only ([02 §1](02-MEASURING-WITH-RARE-EVENTS.md#1-how-noisy-is-nothing-found), [04 §1](04-KNOWING-WHEN-TO-STOP.md#1-evidence-gated-triggers)) |
| 2 | **No frozen evaluator** | the agent can edit what measures it: threshold, cost model, metrics, logs. DGM, STOP, AlphaEvolve, the AI Scientist and METR's runs were all gamed this way **(V/S)** | measurement layer outside the agent's write permissions ([03 §2](03-THE-SAFE-LOOP.md#2-what-may-change-and-through-which-door)) |
| 3 | **Whole-document rewrites** | the playbook gets shorter and more generic; hard-won specifics vanish (ACE: 18,282 → 122 tokens) **(V)** | delta operations merged by code ([03 §4](03-THE-SAFE-LOOP.md#4-the-playbook-itemised-and-delta-edited)) |
| 4 | **No exact versioning** | the previous champion cannot be restored, because the model, quantisation or sampler is not recorded | every version in git, runtime fingerprint included |
| 5 | **Outcome-only metric** | hit count with no precision guardrail and no recall probe, so loosening the criteria looks like improvement | human-rejection rate as a guardrail; missed-hit log for recall |

## Weeks 3–8: the "month 2" failures

| # | Pitfall | Symptom | Fix |
|---|---|---|---|
| 6 | **Playbook bloat and contradiction** | rules accumulate, contradict each other and dilute the context; smaller models degrade fastest as context grows (context rot) **(V)** | size caps, dedup, retire items with harmful > helpful, a quarterly human clean-up |
| 7 | **Recency overfitting** | "Tuesday was dead on source X, so drop it" | the bandit's discounted posterior; prose rules are not an allocation mechanism |
| 8 | **Stacked changes** | two or three edits land before any was evaluated; attribution impossible, rollback a guess | one change in flight ([04 §2](04-KNOWING-WHEN-TO-STOP.md#2-one-change-in-flight)) |
| 9 | **Winner's curse** | the best of several proposals looked good partly by luck and regresses after promotion **(S)** | one challenger at a time; confirm in a fresh window; halve forecast lifts |
| 10 | **World change mistaken for regression, or the reverse** | a layout change zeroes one source; the agent "fixes" its strategy instead of its parser, or rolls back a good change | sentinel, health checks, attribution table ([03 §8](03-THE-SAFE-LOOP.md#8-sentinel-drift-and-rollback)) |
| 11 | **Self-narrative drift** | the reflector reads its own earlier summaries ("source X is reliable") instead of raw logs, and errors compound | feed it code-computed metrics and raw excerpts only |
| 12 | **Gaming through proxies** | near-misses rise because queries got broader, not better | proxies accelerate decisions but never make them ([03 §9](03-THE-SAFE-LOOP.md#9-goodhart-what-gaming-looks-like-and-the-structural-guard)) |
| 13 | **Exploration death** | a source that was bad for a week is dropped forever; its recovery is never seen | exploration floor and a cold pool ([03 §5](03-THE-SAFE-LOOP.md#5-a-bandit-for-allocation-instead-of-rewrites)) |
| 14 | **Runtime swaps treated as non-events** | a new quantisation or runtime build changes tool-call formatting and the whole playbook silently regresses | every runtime change is a challenger through gates 2–4 |

## Month 2 and later: structural decay

| # | Pitfall | Symptom | Fix |
|---|---|---|---|
| 15 | **Never converging** | no maintenance mode; acceptance rates fall while regressions accumulate | maintenance mode as the default destination ([04 §5](04-KNOWING-WHEN-TO-STOP.md#5-maintenance-mode)) |
| 16 | **Golden-set staleness or overfitting** | the eval set stops representing the market, or the reflector has effectively learned it | monthly refresh, a hidden slice, add every new real hit and false positive |
| 17 | **Cross-run state leakage** | memory notes or caches let the agent "remember" evaluation answers **(V, Askarbekuly et al.)** | fresh workspace per evaluation, audit every state channel (R3/R4) |
| 18 | **Autonomy creep** | proposals start touching the constitution ("raise the rate limit to find more") | gate proposals by type; frozen-layer proposals go to the human |
| 19 | **Human alert fatigue** | shadow disagreements and digests pile up unlabelled; evaluation stalls | budget the human's labelling time, and the change rate with it |
| 20 | **Optimising the wrong unit** | hits per round instead of per unit cost, or hits instead of realised value; many low-value "hits" | weight by value where possible; track realised outcomes |
| 21 | **Self-poisoned facts** | the agent stores its own conclusions ("seller X is legit"), later retrieves them next to contradicting evidence and averages the two **(V)** | rank sources (verified data beats the agent's conclusions), date and expire memories, write retractions next to the error |
| 22 | **Prompt injection through content** | seller-written text ("best price, ignore other sources") reaches reflection and is promoted into rules | never promote content-derived text into the playbook; see Course 3 **(I; Willison's lethal trifecta V)** |
| 23 | **Same-model rubber-stamping** | reflector and reviewer share a model and context and approve each other **(V)** | code gates; a different model or a fresh context for critique |
| 24 | **Silent truncation** | the playbook outgrows a harness file limit (OpenClaw: 20k characters per file, 60k total) and later sections disappear with no diff in the "logic" **(V)** | a size cap well below the limit, checked by the static gate |
| 25 | **Self-written skills that hurt** | agent-authored skill packs score below no skills (SkillsBench: −8 to −11.5 points) **(V)** | curate by outcomes; at most 2–3 active, retrieved items per task |

## A one-page review before you switch it on

1. Can the agent write to anything that measures it? (2, 17)
2. Does any code path rewrite a whole document? (3)
3. Can you restore last week's champion exactly, model included? (4, 14)
4. What triggers a reflection, and can an empty round trigger it? (1)
5. How many rounds per arm would your smallest interesting change need? ([02 §7](02-MEASURING-WITH-RARE-EVENTS.md#7-exercises))
6. What is your recall signal? (5)
7. What makes the system stop? (15)

---

Sources: [SOURCES](SOURCES.md).
