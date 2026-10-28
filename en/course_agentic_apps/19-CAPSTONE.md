# Part 19 · Capstone — a general-purpose personal assistant

**Level:** ⭐⭐⭐⭐⭐ · **Time:** ~10 h · **Requires:** parts 1–18
**Produces:** a working system, a repeated measurement from part 1, a plan for what comes next

---

## 0. What you have at this point

```
                      ┌──────────── CHANNELS ───────────┐        pt. 12
   socket (host) ─────┤  pairing · lists · limits       │
   HTTP (sandbox) ────┤  routing → agent + tools        │
   scheduler (cron) ──┘                                 │        pt. 11
                                  │
                      ┌───────────▼──────────────────────┐
                      │            GATEWAY               │        pt. 2
                      │  one per host · loopback         │
                      │  sessions = event log            │
                      │  trust level per session         │
                      └───────────┬──────────────────────┘
                                  │
                      ┌───────────▼──────────────────────┐
                      │            HARNESS               │        pt. 3
                      │  task registry · progress · git  │
                      │  5 stop conditions · error ladder│
                      └───────────┬──────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        ▼                         ▼                         ▼
  ┌───────────┐            ┌───────────┐            ┌───────────┐
  │ ARCHIVIST │            │RESEARCHER │            │   HOST    │   pt. 6
  │ documents │            │  network  │            │ calendar  │
  │ bwrap     │            │ ⭐ strict │            │  light    │   pt. 10
  │ no network│            │ proxy 4×  │            │ proactive │   pt. 11
  └─────┬─────┘            └─────┬─────┘            └─────┬─────┘
        └────────────────────────┼────────────────────────┘
                                 ▼
   context pt.4 · bi-temporal memory pt.5 · tools pt.7 · code-mode pt.8
   protocols pt.9 · fleet pt.13 · evaluation pt.14 · traces pt.15
   ASI01-10 pt.16 · router pt.17 · releases pt.18
```

**This is not a demo.** It is a system with a log from which you can reconstruct every
decision; with a memory that knows when something stopped being true; with a sandbox
you tried to break sixteen times; with a gate that will not let a degradation through;
and with a runbook written before it was needed.

---

## 1. The acceptance task

**One command that touches everything you have built:**

> *"Go through my documents from the last quarter. Find everything that has a deadline
> in the next 60 days. For things where the regulations may have changed — check it.
> Set reminders with appropriate lead time. Write me a one-page summary and tell me
> what you were not sure about."*

**Why this one.** The task requires:

| Requires | Part |
| :-- | :-- |
| work longer than one context window | 3, 4 |
| memory across sessions | 5 |
| three agents with **different permissions** | 6, 13 |
| network egress **with isolation** | 10, 12 |
| a loop over many documents → **code-mode** | 8 |
| write operations → **human consent** | 7, 16 |
| ⭐ **explicitly admitting uncertainty** | 14 |

---

## 2. Acceptance criteria

### 2.1 · Functional

- [ ] Finishes the task in **≤3 sessions**, with no intervention from you beyond approvals
- [ ] The summary **quotes the file and the passage** for every claim
- [ ] The "what I was not sure about" section is **non-empty and on point**
- [ ] Reminders in the calendar, each with lead time appropriate to the matter
- [ ] When one stage fails, returns a **partial result with an explicit annotation**

### 2.2 · Architectural — verified from traces, not from declarations

- [ ] The Researcher **did not touch** `~/dokumenty` — confirmed by traces (pt. 15)
- [ ] Nothing from `~/dokumenty` **left the machine** — egress audit (pt. 17)
- [ ] Every write operation had consent with a **summary built from code** (pt. 16)
- [ ] The Researcher's result reached the rest **wrapped as data** (pt. 13)
- [ ] Full trace: agent → workflow → model → tool (pt. 15)

### 2.3 · Operational

- [ ] `kontrola.py` — 12/12
- [ ] Golden set ≥50 questions, score **above the baseline**
- [ ] ASI attacks ≥18/20
- [ ] 16 escape attempts — all blocked
- [ ] Full offline — **zero failed tasks**
- [ ] Rollback to the previous release in under 5 minutes

---

## 3. EXPERIMENT 19 — measuring the whole course

⭐ **Go back to `pomiary/01-gdzie-peka.md` from part 1.** The same five tasks Z1–Z5, the
same model, the same hardware. **Only the system around the model has changed.**

```bash
python3 ewaluacja/uruchom.py --zestaw pomiary/01-gdzie-peka.md \
  --przebiegow 3 --porownaj-z pomiary/01-wyniki-bazowe.csv
```

| Task | Steps ~ | Part 1 (loop) | Part 19 (system) | Δ |
| :-- | --: | --: | --: | --: |
| Z1 · how many lines | 2 | /3 | /3 | |
| Z2 · find the PDFs | 4 | /3 | /3 | |
| Z3 · first line of each | 8 | /3 | /3 | |
| Z4 · write + verify | 12 | /3 | /3 | |
| Z5 · condition + state | 18 | /3 | /3 | |

**Failure-mode breakdown — did the ones that were supposed to disappear actually go:**

| Mode | Part 1 | Part 19 | What was meant to fix it |
| :-- | --: | --: | :-- |
| `KONTEKST` | | | pt. 3 harness, pt. 4 compaction |
| `NARZĘDZIE` | | | pt. 7 descriptions, pt. 8 code-mode |
| `PĘTLA` | | | pt. 3 state fingerprint |
| `CICHY` | | | pt. 3 registry, pt. 14 verification |
| `BŁĄD` | | | pt. 3 ladder, pt. 7 messages |
| `STAN` | | | pt. 2 log, pt. 5 memory |

⭐ **This is the only assessment of this course that means anything.** Not the number
of pages read — **the number of tasks that now finish and previously did not.**

⚠️ **If any failure mode did not disappear — go back to the indicated part.** That is
not a failure, just a diagnosis. The course is built so that every mode has a remedy
assigned.

---

## 4. How you know it is really yours

Six questions. If you cannot answer any of them without looking — go back to that part.

| # | Question | Part |
| --: | :-- | :-- |
| 1 | Why does 92% per step give 29% over 15 steps — and **three** ways to improve it? | 1, 3, 8, 14 |
| 2 | What exactly did the model see on turn 40 of a session from a week ago? | 2, 15 |
| 3 | How much did you pay for electricity in April — and **how** does the agent know? | 5 |
| 4 | Which isolation level stops a kernel exploit, and which does not? | 10 |
| 5 | Why **can't** the approval summary come from the model? | 16 |
| 6 | Did the harness or the model give the bigger improvement — and by how much? | 14 |

⭐ **Question 6 is the crux.** If you know your number, it means you **measure instead
of believing** — and that is the one habit from this course that really has to stay.

---

## 5. What next

### 5.1 · The next few weeks

| Step | Why | From |
| :-- | :-- | :-- |
| **Use it daily for a month** | tasks from real use are the best golden set | pt. 14 |
| **3 questions a month from failures** | the set grows with your experience | pt. 18 |
| **A fourth agent** | now it is an evening's work, not a project | pt. 6, 13 |
| **After adding cards 3–4** | ⚠️ repeat the parallelism and routing measurements | pt. 13 §5.3, 17 |

### 5.2 · Directions for growth — in order of return

| Direction | Return | Difficulty |
| :-- | :-- | :-- |
| ⭐ **Multimodality in the loop** (vision, voice from course 1 pt. 5) | high | medium |
| ⭐ **Sleep-time compute for real** — nightly tidying and pre-computing | high | low |
| **Speculative decoding in the loop** (course 1 pt. 8) | medium | low |
| **gVisor for the Researcher** | medium | medium |
| **LoRA on Polish material** | ⚠️ low, until the harness is exhausted | high |
| **A2A** | ⚠️ zero, as long as the agents are all yours | high |

⚠️ **The last two rows are traps with a strong pull.** Fine-tuning a model and
inter-agent protocols are **the most pleasant known ways to waste a quarter** — because
they sound like sophistication, and your bottleneck lies elsewhere. Postpone them until
a measurement says otherwise.

### 5.3 · Keeping it alive

Three things you do **always**. The rest is optional.

1. ⭐ **The regression gate before every change.** Without it the system degrades
   imperceptibly through good intentions.
2. ⭐ **The nightly job.** Evaluation, memory audit, drift detection, backup. Free.
3. ⭐ **Three new questions a month from real failures.**

> 💡 **One closing observation about how this system ages.** The code will work for
> years. **The numbers will age** — context thresholds, router levels, the limit of
> concurrent sessions. All of them come from measurements on two cards, on specific
> models, in September 2026. After every hardware or model change **repeat experiments
> 4, 7, 8, 13 and 17** — it is half a day's work and the only way to keep the system
> from living in the past.

---

## 6. Trap registry — P60–P139

Eighty traps from the whole course. **Go through them once when you finish** — half
will sound obvious, and the other half like something you just stepped in.

| Part | Range | Topic |
| :-- | :-- | :-- |
| 1 | P60–P62 | when not to build an agent, measurement, authorities |
| 2 | P63–P66 | stdout, `fsync`, event order, default trust |
| 3 | P67–P71 | test immutability, item size, baseline verification, progress, errors |
| 4 | P72–P76 | context window, cache prefix, compaction order, numbers, prompt growth |
| 5 | P77–P81 | invalidation, two times, quote, scope, quarantine |
| 6 | P82–P85 | boundaries vs enforcement, skills, self-editing, supply chain |
| 7 | P86–P90 | overlapping descriptions, errors, trust filter, idempotency, blast radius |
| 8 | P91–P94 | traceback, paths, call limit, printing content |
| 9 | P95–P98 | other people's numbers, `--help`, trust in MCP, three interfaces |
| 10 | P99–P103 | container ≠ sandbox, limits, environment, proxy, injection |
| 11 | P104–P108 | two instances, idempotency, silence, thresholds, circuit breaker |
| 12 | P109–P112 | channel trust, unknown senders, token comparison, splitting |
| 13 | P113–P117 | depth, result as a command, splitting, degradation, supervisor |
| 14 | P118–P122 | self-assessment, refusals, a single run, judge, set from the model |
| 15 | P123–P126 | attributes, content in traces, export, limits of observability |
| 16 | P127–P131 | pattern filter, quote, summary from the model, checksum, baseline |
| 17 | P132–P135 | gate in escalation, source vs pattern, `stop_reason`, offline |
| 18 | P136–P139 | repo cleanliness, backward migration, `cp` vs `.backup`, model checksum |

---

## 7. Final checkpoint

```bash
cd $OSA

python3 wydanie/kontrola.py                                    # 12/12
python3 ewaluacja/uruchom.py --przebiegow 3                    # > baseline
python3 testy/ataki/ataki.py --wszystkie                       # ≥18/20
python3 testy/ucieczka/proby.py --poziom scisly --wymagaj-porazki-wszystkich
python3 ewaluacja/uruchom.py --offline --wymagaj-zero-nieudanych
python3 router/audyt.py --okres 30d                            # Archivist: 0
python3 ewaluacja/uruchom.py --zestaw pomiary/01-gdzie-peka.md \
        --porownaj-z pomiary/01-wyniki-bazowe.csv              # ⭐ course assessment

bash wydanie/wydaj.sh 1.0.0
git tag -l && git log --oneline | wc -l
```

- [ ] The acceptance task passes in ≤3 sessions
- [ ] All the criteria from §2.1, §2.2 and §2.3
- [ ] ⭐ **Z1–Z5 measured again; the failure modes have gone**
- [ ] You can answer the six questions from §4
- [ ] Release 1.0.0 with a manifest and an evaluation result

---

## 8. In closing

You have built something that cannot be bought: **a system that you understand in its
entirety**. Every threshold comes from your own measurement, every boundary is in code
you wrote, and every decision has an ADR with a falsification condition.

The biggest lesson is not technical. It came back in every part, and it goes like this:

> ⭐ **The variable you have full control over — the system around the model — is more
> important than the variable you have no control over at all.**

That is why you measured the harness, not the weights. That is why you wrote boundaries
in code, not in the prompt. That is why the golden set has a "correct refusal"
category, and the approval summary is built by code, not by the model.

The model you use today will be obsolete in a year. **Everything else you built will
remain** — and will take on the next model without changing a single line.

**Now use it. The things it breaks in the first month will be a better teacher than
this course.**
