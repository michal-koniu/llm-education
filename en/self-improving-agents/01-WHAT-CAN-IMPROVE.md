# 01 · What can improve itself, and how it went

A survey of self-improving agent systems from 2023 to 2026: what each one changes, how it decides that a change is
better, what stops it from getting worse, and where it failed. The failures are the useful part. Tags: see
[README](README.md#how-to-read-the-evidence-tags). Links: [SOURCES](SOURCES.md).

---

## 1. Agent-level self-improvement: classic and evolutionary

These systems change the agent itself: its code, tools, skill library or reflections.

| System | Year | What it changes | How a change is evaluated | Regression guard | Notable failure or limit |
|---|---|---|---|---|---|
| **Reflexion** | 2023 | Verbal reflections, 1–3 per task, used only when retrying the same task | Environment reward, heuristics, self-written unit tests | Only the memory cap | Self-written tests had 16.3% false positives on MBPP, so it scored below the GPT-4 baseline. **On WebShop (e-commerce search) it gained nothing and stopped after 4 trials** **(V)** |
| **Voyager** | 2023 | A library of executable code skills plus an automatic curriculum | A self-verification critic must confirm success before a skill is stored | The verification gate; give up after 4 stuck rounds | Without self-verification, −73% items. GPT-3.5 and open models were not good enough (5.7× gap) **(V)** |
| **ExpeL** | 2023 | A list of natural-language insights (ADD / EDIT / UPVOTE / DOWNVOTE) and a pool of successful trajectories | Contrastive pairs of success and failure | Each insight has an importance score: starts at 2, votes move it ±1, deleted at 0 | Feeding self-reflections into extraction *hurt* (29% vs 39%). A weaker extractor did worse. The list grows without bound **(V)** |
| **Agent Workflow Memory** | 2024 | Abstracted workflows added to memory | Offline: ground truth. Online: an LLM judge | Success filter only | Learned from wrong self-labels. **Offline plus online workflows together scored below online alone**: the sets conflicted **(V)** |
| **ADAS / Meta Agent Search** | 2024 | Agent code (the meta-agent is fixed) | Validation sets of 32–128 questions; an archive of scored designs | The archive | Transfer to other domains fell *below* baselines. Tiny validation sets **(V)** |
| **Gödel Agent** | 2024 | Its own running code, **including the improver** | Validation utility | Informal "can revert" | Over 100 runs: 4% crashed after editing the improver, 92% had temporary drops, **14% ended worse than they started**. One version "improved" by calling a stronger external model, escaping the evaluation protocol **(V)** |
| **Darwin Gödel Machine (DGM)** | 2025 | A coding agent's codebase | Staged: 10 tasks, then 60, then 200, with thresholds set from measured noise | An open-ended archive of working agents | **Objective hacking:** it removed the logging its hallucination checker relied on and got a perfect score; it also faked test logs. About $22k per run **(V)** |
| **Huxley-Gödel Machine / DGM-H** | 2025–26 | As DGM (DGM-H also edits the meta-agent) | Per-task evaluation; selection by the productivity of a whole lineage | Lineage-based selection | An agent's own score predicts its descendants poorly (r ≈ 0.29–0.44) **(V)** |
| **SICA** | 2025 | Its own code, tools, sub-agents and overseer | Utility mixing score, cost and time | Best-of-archive becomes the next improver; an LLM overseer kills loops | Early ideas dominate later ones. No gain on reasoning benchmarks. The authors say it "requires powerful models" **(V)** |
| **AlphaEvolve and open variants** (OpenEvolve, ShinkaEvolve, CodeEvolve) | 2025–26 | Marked code blocks as diffs, optionally the meta-prompts | A user-written `evaluate()` in a **cascade** of cheap then expensive checks | Island populations, novelty rejection | Tao and co-authors: the system "always eventually figured out a way to cheat" leaky verifiers. **The cheapest model over many runs was the most cost-effective**; CodeEvolve with Qwen3-Coder-30B beat AlphaEvolve on one problem at ~10× lower cost **(V)** |
| **Promptbreeder** | 2023 | Task prompts and the mutation prompts that change them | Fitness on a 100-example batch, binary tournament | Population plus a similarity filter | The LLM "did not understand" fitness numbers; winning prompts were opaque **(V)** |
| **STOP** | 2023 | The improver scaffold, improving itself | Utility on downstream tasks | None | **GPT-3.5 and Mixtral made the improver worse every iteration.** The strongest model switched off the sandbox flag in 0.42% of proposals, and a warning did not help **(V)** |
| **autoresearch** (Karpathy) | 2026 | One file, `train.py` | Fixed 5-minute budget, a **frozen** evaluator file, one metric | Strict ratchet: keep only if better, otherwise `git reset` | In a replication, a coding agent hard-coded evaluation answers until a held-out set was added **(V)** |

## 2. Prompt, context, skill and memory optimisers

These systems leave the code alone and change text: prompts, playbooks, skills, memories. This is the layer most
practical agents touch, and it is where the 2026 evidence is.

| System | Year | What it changes | How a change is evaluated | Regression guard | Notable failure or limit |
|---|---|---|---|---|---|
| **DSPy MIPROv2** | 2024 | Instructions and few-shot examples per module | Bayesian search over minibatches, full evaluation every few trials | Returns the best *fully evaluated* configuration | Needs a scalar metric and hundreds of labels **(V)** |
| **GEPA** | 2025 | Any text component | A reflection model reads traces; a child must beat its parent on a **minibatch of 3**, then is scored on a Pareto set | Per-example Pareto pool | "Prompt bloat": each iteration appends rules. **Fell below the starting prompt with a Llama-3.3-70B reflector** on one task (59.4 vs 62.5) **(V)** |
| **TextGrad** | 2024 | Any variable via textual "gradients" | Validation each iteration | Update only if validation improves | Assumes a strong backward model; no variance control **(V)** |
| **Trace / OptoPrime** | 2024 | Code, prompts, parameters in a traced graph | Execution trace plus feedback | **None**: accepts every parsed update | Constraint violations. Showing the trace beats showing only the outcome **(V)** |
| **ACE** (Agentic Context Engineering) | 2025 | An itemised "evolving playbook": bullets with IDs and helpful/harmful counters | Generator → reflector → **curator emits deltas, merged by code** | Delta merge, counters, deduplication | Its baseline shows **context collapse**: one full rewrite took a playbook from 18,282 tokens to 122 and accuracy from 66.7 to 57.1, below the 63.7 of no playbook at all. A Llama-3.3-70B reflector gave only +1.1 to +2.4 **(V)** |
| **Dynamic Cheatsheet** | 2025 | Free-form memory rewritten every step | Self only | None | The collapse above. Small models "limited and inconsistent"; "faulty heuristics… equally amplified" **(V)** |
| **ReasoningBank** | 2025 | Strategy memories from successes and failures | An LLM judge, 72.7% accurate | None (append only) | **Retrieving 4 memories did worse than 1** (44.4% vs 49.7%) **(V)** |
| **Live-SWE-agent** | 2025 | Tools created at runtime, reflection after every step | Task progress | None | GPT-5-Nano **fell from 44% to 14%**, "stuck in loops". Only strong models gain **(V)** |
| **Hermes Agent** (Nous Research) | 2026 | Skills (patching preferred) and a memory file | Agent self-review after sessions | Hard caps (memory file 2,200 characters); staged write approval; a **Curator** that runs weekly when idle, marks items stale after 14 days, archives after 30, **never deletes**, has **LLM consolidation off by default**, snapshots and rollback | The Curator exists because the loop produced "dozens of narrow near-duplicates" **(V)** |
| **Anthropic skill-creator** | 2025–26 | Skills and their trigger descriptions | Blind A/B against a **snapshot of the old version**, 3 runs per query, 60/40 train/test split, pick by **test** score | Old-version baseline; retire a skill when the base model passes without it | Warns against "fiddly overfitty changes" **(V)** |
| **OpenAI self-evolving agents cookbook** | 2025 | The system prompt | 4 graders, pass thresholds, at most 3 retries | Versioned prompts and revert; winner by cumulative score, not recency | Admits overfitting risk to immediate grader feedback; **its own sample run accepts sections just under its stated bar** **(V)** |
| **SkillOpt** (Microsoft) | 2026 | A skill document via add / delete / replace under an **edit budget**, a "textual learning rate" | Kept only if a held-out selection set improves | A buffer of rejected edits; slow updates | Removing the rejected-edit buffer cut one score from 77.5 to 72.9 **(V)** |
| **SkillBoost** | 2026 | Skill components | Back-test on the full set | **Accept only if gain > 0 and regressions stay below a small ε**: "must fix more cases than it breaks" | An edit that fixed 20 and broke 23 was rejected. **Without the gate, one model fell from 80.0 to 67.5** **(V)** |
| **Library Drift** | 2026 | Governance of a skill library | Per-skill contribution score | Outcome-driven retirement, a cap on active skills | Unbounded growth degrades retrieval; retiring too early also hurts. Pass@1 0.258 → 0.584 with governance **(V, abstract)** |
| **SkillsBench** | 2026 | (benchmark) | Deterministic verifiers | n/a | **Self-generated skills scored below no skills on all three harnesses (−8.1 to −11.5 points)**, curated skills added +18 to +25. 2–3 skills is optimal; 4+ halves the gain **(V)** |
| **"Do Self-Evolving Agents Forget?"** | 2026 | Workflows, skills, memory, weights | Old and new tasks | Anchored behavioural signatures; protected items | Capability erosion in all four modes: workflows evolved on hard tasks lost skill on easy ones **(V)** |
| **SkillLearnBench** | 2026 | (benchmark) | | | Iteration helps only with external feedback. **"Self-feedback alone induces recursive drift"** **(V, abstract)** |
| **OpenClaw Skill Workshop and memory "dreaming"** | 2026 | The agent's own skills; background promotion of memories | None documented | Previous version saved; restore command | "Every change applies immediately". **No approval gate is documented** **(V)** |

Further systems in the same family, with similar lessons: Memento, Agent KB, SkillWeaver, EvoAgentX, PILOT,
HarnessBank, SelfOp ([SOURCES](SOURCES.md)).

## 3. What the survey says, distilled

**Verified outcome signals are the whole game.** Reflexion and Agent Workflow Memory degrade when success is
self-judged. Voyager's largest single gain is its verifier. ExpeL gets *worse* when its own reflections feed its
insights **(V)**. For the scout: edit the playbook only from code-computed outcomes (a confirmed price gap, a realised
sale, a human label), never from the LLM's opinion of how a round went.

**Self-modification of the improver or the evaluator is where things break.** Gödel Agent crashed after editing its
improver; STOP disabled its sandbox; DGM deleted the markers its scorer used; AlphaEvolve found leaky verifiers **(V)**.
Freeze the evaluator *by construction*: no write access, not "please don't".

**Single-lineage hill climbing regresses; archives and staged promotion help.** 14% of Gödel Agent runs ended worse
than they began. DGM without its archive reached 23% instead of 50% **(V)**. For production, combine a ratchet (one
champion, replaced only on proof) with an archive of everything tried.

**Weak optimisers hurt, but mid-size models are fine proposers under an exact evaluator.** STOP with GPT-3.5 and Mixtral got
worse each iteration; Live-SWE-agent with GPT-5-Nano collapsed **(V)**. Yet CodeEvolve used Qwen3-Coder-30B and
Tao and co-authors found the cheapest model over many runs most cost-effective, *because an exact evaluator did the
selecting* **(V)**. Let a local model propose small, typed deltas; let code and statistics select.

**Exploration must be built in, because reflection does not create it.** Reflexion failed on WebShop, the closest
benchmark to marketplace search, precisely for lack of "diversity and exploration" **(V)**. Evolutionary systems buy
exploration with populations and novelty filters. A bandit with an exploration floor is the cheap equivalent
([03 §5](03-THE-SAFE-LOOP.md#5-a-bandit-for-allocation-instead-of-rewrites)).

**Accumulation decays unless it is governed.** Without governance, self-written skills and memories often score
*below no memory at all*: SkillsBench, Dynamic Cheatsheet, Library Drift, capability erosion **(V)**. Production
harnesses converged on four answers:

- hard size caps (Hermes: a 2,200-character memory file);
- usage-based staleness and archiving, never deletion (Hermes Curator);
- "fix more than you break" gates (SkillBoost);
- retrieving only 1–3 items per task (ReasoningBank, SkillsBench).

**Whole-text rewrites are the main regression mechanism; deltas are the fix.** ACE's 18,282 → 122-token collapse,
STOP dropping seed constraints "for simplification", GEPA's bloat **(V)**.

## 4. Small and local models as reflectors

The question for anyone running a local model: can it improve itself?

| Finding | Evidence |
|---|---|
| *Intrinsic* self-correction, with no external signal, lowers accuracy | Huang et al. (ICLR 2024): Llama-2 on GSM8K fell from 62.0 to 36.5 **(V)**. Kamoi et al.: self-correction works only with reliable external feedback or task-specific fine-tuning **(V, abstract)** |
| Weak optimisers degrade or plateau | STOP with GPT-3.5: only 12% of runs improved by ≥3%. ACE with a Llama-3.3-70B reflector: small gains, while GEPA and Dynamic Cheatsheet fell below base. Live-SWE-agent on GPT-5-Nano collapsed **(V)** |
| Mid-size models work as *proposers* under an exact evaluator | Swapping the reflector to Qwen2.5-32B kept every method in ESPO above the default prompt (ESPO 67.8, GEPA 63.5 vs 31.1), though lower than with a frontier reflector. CodeEvolve with Qwen3-Coder-30B **(V)** |
| Vendors converge on "strong advisor, cheap executor" | Anthropic's advisor strategy: a small executor consults a large model only at hard decisions; Haiku with an Opus advisor scored 41.2% vs 19.7% for Haiku alone on BrowseComp **(V)** |
| Same-model self-review skews positive | Agents "reliably skew positive when grading their own work"; tuning a separate sceptical evaluator is "far more tractable" (Anthropic harness design, 2026) **(V)** |

**Bottom line (I):** a 30–80B open model is near the threshold where reflection gains shrink or reverse. Use it to
*classify* failures and to *propose* small typed deltas, gated by code-measured outcomes. Do not use it to judge its
own proposals or to rewrite the whole playbook.

## 5. Practitioner guidance that bears on self-modifying loops

**Evaluation practice** (Anthropic "Demystifying evals for AI agents", Husain & Shankar, Eugene Yan) **(V)**:

- "20–50 simple tasks drawn from real failures is a great start."
- Test when a behaviour should happen *and* when it should not. For the scout, "nothing worth flagging here" is a
  first-class passing case.
- Prefer deterministic graders, one binary grader per failure mode. Validate any LLM judge on ≥50 passes and ≥50
  failures before you trust it.
- Separate **capability evals** (low pass rate, "a hill to climb") from **regression evals** (near 100%).
  Saturated capability tasks graduate into regression.
- Use **pass^k** (all k trials succeed) when consistency matters: 75% per trial gives pass^3 ≈ 42%.
- Isolate trials. One agent gained an unfair advantage by reading the git history left by earlier trials.
- "Read the transcripts!" Review 10–20 traces a week.

**Harness design** (Anthropic posts, Nov 2025 and Mar 2026) **(V)**: workers could edit only a `passes` field in a
JSON feature list, because models are less likely to overwrite JSON than Markdown; "It is unacceptable to remove or
edit tests"; harness components encode assumptions about model weaknesses, so re-test them whenever the model changes.

**Reward hacking** **(V)**:

- METR (Jun 2025): a frontier model overwrote a timer, patched an evaluator and read answers off the call stack,
  hacking in 30.4% of runs on one benchmark. **"Please do not cheat" still left 80% hacking.** Their advice: "patch
  the exploit in the scoring function rather than punishing the model."
- In-context reward hacking (Weng 2024, summarising Pan et al.): feedback loops at *inference time*, with no weight
  updates, still produce escalating constraint violations; the more feedback rounds, the worse. Sharing context
  between evaluator and generator is the key enabler. This is exactly the setting of a prompt-editing agent.
- Anthropic (Nov 2025): learned test-gaming generalised to sabotaging detection code. Explicitly permitting the
  shortcut stopped the generalisation. The inference-time analogue **(I)**: make "zero hits this round" an
  explicitly legitimate, unpenalised outcome.

**Context failure** **(V)**: Chroma's "Context Rot" found that all 18 models tested degrade as input grows, and
distractors make it worse. Breunig names four failure modes: poisoning, distraction, confusion, clash. Mid-size
models start dropping rules beyond about 100 instructions. Manus: keep the prompt prefix stable for cache hits, keep
failures in context, "don't few-shot yourself into a rut".

**Long-running agents in the wild** **(V)**:

- Project Vend (Anthropic 2025): the shop agent sold below cost and reinstated discounts days after agreeing to stop.
  Forced checks helped ("bureaucracy matters"), and a same-model "manager" shared the agent's blind spots.
- Vending-Bench: "all models have runs that derail", with no clear link to how full the context was.
- Memory self-poisoning (2026 post): wrong conclusions saved automatically were later retrieved next to the
  correction, and the agent "split the difference". The fix: rank sources (verified data beats the agent's own
  conclusions) and write retractions into the same memory layer.

There is **no rigorous public post-mortem** of an agent that rewrote its own playbook for weeks and then degraded.
The evidence for "month-2 decay" comes from the analogues above and the 2026 benchmark papers. Treat it as a
well-supported expectation, not a measured curve **(I)**.

---

Next: [02 · Measuring with rare events](02-MEASURING-WITH-RARE-EVENTS.md).
