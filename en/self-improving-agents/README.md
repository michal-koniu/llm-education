# Self-improving agents without regressions

**As of 29 October 2026.** How to build an agent that improves its own instructions, memory or skills over weeks of
work, without slowly breaking the version that already worked, and how to make it recognise when it is good enough
and should stop changing itself. This directory is a **guide**: the survey of what exists, the statistics you cannot
skip, an architecture you can build, and the traps in the order you will meet them.

> ⚠️ **What this guide is and is not.** It is desk research: over 100 papers, docs and engineering posts read on
> 29 October 2026, plus statistics computed with a small script ([tools/](tools/README.md)). The architecture in
> [03](03-THE-SAFE-LOOP.md) is a design recommendation, grounded in those sources but **not** a measured result.
> Every important claim carries an evidence tag (below), so you can tell a paper's number from my inference.

---

## The problem in one paragraph

A self-improving loop has three parts: the agent works, something reflects on how it went, and the reflection edits
what the agent does next time (a prompt, a playbook, a skill file, a memory store, its own code). The papers show this
can work. They also show the same failure again and again: the loop **learns from noise or from its own opinion of
itself**, it edits by **rewriting whole documents** and loses what it knew, it **reaches the thing it is measured by**
and games it, and it **never stops**. When the outcome you care about is rare, all four get worse, because a handful
of rounds says almost nothing about whether a change helped. Most of this guide is about that last point.

## The running example: a scout with rare hits

To keep things concrete, the guide uses one agent throughout. It is deliberately generic.

**The scout** runs in *rounds*, say every 15 minutes, around the clock. In each round it searches a few public
marketplaces, extracts listings, compares each one with a reference price, and flags those that are priced well below
it. A flag that turns out to be right is a **hit**. Hits are rare: the guide assumes **0.1 to 0.3 hits per round**,
as an illustration. The scout keeps a **playbook** (which sources and queries to run, how to match items, red flags,
procedure notes), and a **reflection** step edits the playbook.

The same shape appears in many agents. If yours has a rare, valuable outcome and a cheap, frequent round, everything
here applies:

| Agent | Round | Rare hit | Denser signal you can use instead |
|---|---|---|---|
| Marketplace scout | one search pass | a confirmed underpriced listing | near-misses, qualified candidates, judgment on a labelled archive |
| Dependency advisory watcher | one scan of feeds | an advisory that really affects your code | correctly dismissed advisories on a labelled set |
| Literature scout | one query batch | a paper you actually needed | relevance labels on a fixed set of past results |
| Bug-hunting agent | one pass over a module | a confirmed real bug | seeded bugs, reproduction rate on known bugs |
| Support triage | one ticket batch | a correct escalation of a rare urgent case | agreement with a human on a frozen set of past tickets |

## The rules that matter most

These are the guide in short. Each links to the place where it is argued.

| # | Rule | Why | Where |
|---|---|---|---|
| 1 | **Never treat "nothing found" as evidence by itself.** | At 0.1–0.3 hits per round, three empty rounds happen 41–74% of the time with no change at all **(C)**. "Reflect after 2–3 empty rounds" reacts to noise. | [02 §1](02-MEASURING-WITH-RARE-EVENTS.md#1-how-noisy-is-nothing-found) |
| 2 | **Accept the arithmetic of rare events.** | Showing that a change *doubles* the hit rate takes about 58 hits in total, 65–194 rounds per arm at 0.1–0.3 hits per round. +25% is practically unmeasurable from hits **(C)**. | [02 §2](02-MEASURING-WITH-RARE-EVENTS.md#2-how-many-hits-to-show-a-change-helped) |
| 3 | **The LLM proposes; code and statistics dispose.** | Allocation (which source, which query) goes to a bandit. The LLM adds hypotheses. Accept, reject and rollback are deterministic code **(I)**. | [03 §5](03-THE-SAFE-LOOP.md#5-a-bandit-for-allocation-instead-of-rewrites) |
| 4 | **Freeze the measurement layer by construction, not by instruction.** | Systems that could reach their scorer gamed it: deleted markers, disabled sandboxes, hard-coded answers, patched graders. "Please do not cheat" still left 80% hacking **(V)**. | [03 §2](03-THE-SAFE-LOOP.md#2-what-may-change-and-through-which-door) |
| 5 | **Edit with deltas, never rewrites.** | One full rewrite collapsed an 18,282-token playbook to 122 tokens, below the no-playbook baseline **(V)**. | [03 §4](03-THE-SAFE-LOOP.md#4-the-playbook-itemised-and-delta-edited) |
| 6 | **One change in flight**, typed, with hypothesis, evidence, predicted effect and inverse delta. | Stacked changes make attribution and rollback impossible **(I)**. | [04 §2](04-KNOWING-WHEN-TO-STOP.md#2-one-change-in-flight) |
| 7 | **Gate cheapest first, and "fix more than you break".** | Schema → must-pass → paired golden set → replay → shadow or switchback → probation. Removing a "regressions < fixes" gate cost up to 12.5 points **(V)**. | [03 §6](03-THE-SAFE-LOOP.md#6-the-gate-cascade) |
| 8 | **Learn only from verified outcomes.** | Self-judged success poisons memory; self-feedback alone "induces recursive drift"; intrinsic self-correction lowers accuracy **(V)**. | [01 §3](01-WHAT-CAN-IMPROVE.md#3-what-the-survey-says-distilled) |
| 9 | **Use shadow mode for judgment changes.** | Champion and challenger score the same stream; only the champion acts. Disagreements are frequent, paired, cheap labels **(I)**. | [03 §7](03-THE-SAFE-LOOP.md#7-shadow-mode) |
| 10 | **Separate "the world changed" from "my change broke it".** | A never-modified sentinel, a CUSUM on the hit rate and plain health checks. Expect ~50–100 rounds to detect a halving at 0.3 hits per round **(C)**. | [03 §8](03-THE-SAFE-LOOP.md#8-sentinel-drift-and-rollback) |
| 11 | **Use small-sample statistics properly.** | Exact tests, sequential tests that allow peeking, the rule of three, no CLT error bars below a few hundred points, discount the winner's curse, pass^k on nondeterministic replays **(V/S/C)**. | [02 §4](02-MEASURING-WITH-RARE-EVENTS.md#4-decision-rules-for-small-noisy-samples) |
| 12 | **A system that works should stop changing itself.** | Probation, exponential backoff, maintenance mode. Late "gains" are disproportionately overfitting **(V/I)**. | [04](04-KNOWING-WHEN-TO-STOP.md) |
| 13 | **Match reflection to evaluation capacity, not to compute.** | Reflection is cheap; validated changes are scarce (a few per month). Mid-size models are near the threshold where reflection gains vanish **(V/I)**. | [03 §11](03-THE-SAFE-LOOP.md#11-who-reflects-and-how-often) |
| 14 | **Govern accumulation.** | Agent-authored skills scored *below no skills* (−8 to −11.5 points); 4 retrieved memories did worse than 1 **(V)**. Cap, archive, never auto-consolidate. | [01 §3](01-WHAT-CAN-IMPROVE.md#3-what-the-survey-says-distilled) |
| 15 | **Treat runtime changes as challengers.** | A new model, quantisation, chat template or runtime build is the largest playbook change you will ever make **(I)**. | [03 §12](03-THE-SAFE-LOOP.md#12-harness-and-runtime-notes) |

## What you build

By the end you have these pieces. None of them needs a framework; each is a small file or a few dozen lines of code.

| Piece | What it is | File |
|---|---|---|
| Frozen measurement module | hit definition, thresholds, metrics, dedup; the agent cannot write to it | [03 §2](03-THE-SAFE-LOOP.md#2-what-may-change-and-through-which-door) |
| Evaluation assets | golden set, must-pass subset, hidden slice, snapshot corpus, missed-hit log | [03 §3](03-THE-SAFE-LOOP.md#3-frozen-evaluation-assets) |
| Itemised playbook + proposal schema | YAML items with IDs and counters; one typed delta per proposal | [03 §4](03-THE-SAFE-LOOP.md#4-the-playbook-itemised-and-delta-edited) |
| Gatekeeper | pure code: gate cascade, McNemar, SPRT, promote / reject / rollback, git versions | [03 §6](03-THE-SAFE-LOOP.md#6-the-gate-cascade) |
| Bandit | discounted Gamma-Poisson Thompson sampling over (source × query) arms | [03 §5](03-THE-SAFE-LOOP.md#5-a-bandit-for-allocation-instead-of-rewrites) |
| Monitor | health checks, Poisson CUSUM, sentinel probe, attribution table | [03 §8](03-THE-SAFE-LOOP.md#8-sentinel-drift-and-rollback) |
| Stopping logic | evidence-gated triggers, cooldown, backoff, maintenance mode, prediction log | [04](04-KNOWING-WHEN-TO-STOP.md) |
| Calculator | the statistics behind every (C) number, for your own rates | [tools/](tools/README.md) |

## What is in this directory

| File | What is in it |
|---|---|
| [01-WHAT-CAN-IMPROVE](01-WHAT-CAN-IMPROVE.md) | **Survey.** 30+ self-improving systems: what each changes, how it evaluates a change, what guards it, how it failed |
| [02-MEASURING-WITH-RARE-EVENTS](02-MEASURING-WITH-RARE-EVENTS.md) | **Lesson.** Why rare outcomes defeat naive evaluation, the arithmetic, exact tests, SPRT, CUSUM, the winner's curse |
| [03-THE-SAFE-LOOP](03-THE-SAFE-LOOP.md) | **Build.** Components, what may change through which door, frozen evaluator, deltas, gates, shadow mode, bandit, sentinel, rollback, cadence |
| [04-KNOWING-WHEN-TO-STOP](04-KNOWING-WHEN-TO-STOP.md) | **Build.** Triggers, one change in flight, probation, backoff, maintenance mode, the lifecycle state machine |
| [05-PITFALLS](05-PITFALLS.md) | 25 failures in the order you will meet them, each with a symptom and a fix |
| [SOURCES](SOURCES.md) | every source with its URL and how carefully it was checked |
| [tools/](tools/README.md) | `rare_event_stats.py`: a standard-library calculator for your own rates |

Suggested order: this page, then [02](02-MEASURING-WITH-RARE-EVENTS.md) (it changes how you read everything else),
then [03](03-THE-SAFE-LOOP.md) and [04](04-KNOWING-WHEN-TO-STOP.md). Read [01](01-WHAT-CAN-IMPROVE.md) when you
want the evidence behind a rule.

## How to read the evidence tags

| Tag | Meaning |
|---|---|
| **(V)** | Verified: read in the primary source (paper, repository, official docs or post) on 29 October 2026 |
| **(S)** | Secondary: taken from a search snippet, a summary or a standard reference, not checked against the original |
| **(C)** | Computed for this guide with [`tools/rare_event_stats.py`](tools/README.md): exact binomial tests and simulation |
| **(I)** | Inference: my own reasoning or design recommendation, built on the sources but not measured |

A rule tagged (I) is a reasoned default, not a law. If your measurement says otherwise, your measurement wins.

## Related parts of the repository

- Course 2, [part 14: evaluation](../course_agentic_apps/00-INDEX.md) and part 18 (releases and maintenance): the
  evaluation harness and release discipline this guide assumes you have.
- Course 3, [indirect injection and memory poisoning](../course_llm_security/00-INDEX.md): why listing text must never
  be promoted into rules ([05, pitfall 22](05-PITFALLS.md)).
- [Agent harnesses survey](../agent-harnesses/README.md): Hermes Agent, OpenClaw and others whose memory and skill
  features are discussed in [01](01-WHAT-CAN-IMPROVE.md) and [03 §12](03-THE-SAFE-LOOP.md#12-harness-and-runtime-notes).
