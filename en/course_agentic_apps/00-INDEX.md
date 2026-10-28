# Course 2: agentic applications on local models — index

**Created 23 September 2026.**
A continuation of course 1 — [`../course_local_models/00-COURSE-INDEX.md`](../course_local_models/00-COURSE-INDEX.md),
parts 1–10.

> **Purpose of the whole thing.** After this course you **design and maintain agentic systems**, rather than
> merely running an agent. You build one growing system — `$OSA/` — and on top of it you stand up
> three cooperating personal agents that **work for weeks,
> wake up on their own, remember, are measured, and cannot do you any harm.**
>
> Course 1 taught **how a model works**. Course 2 teaches **how to build a system around it
> that can be trusted.**

---

## The thesis the whole course stands on

> **An agent's result changes more with the harness than with the model.** The same model
> under two scaffolds gives significantly different numbers.

The variable over which you have **full control** — the system around the model — matters more than
the variable over which you have **none** — the weights. That is why this course has no part
on fine-tuning models, and has six parts on measurement.

⭐ **In part 14 you will verify this thesis on your own hardware.** If it does not hold up, the
course tells you outright: fix the course.

---

## The path

```
  BLOCK I · FOUNDATION ───────────────────────────── ~14 h
   01 architectures         map of the terrain, OpenClaw taken apart, loop engineering
   02 skeleton              gateway, configuration, the session as an event log
   03 harness         ⭐⭐  a loop that survives five context windows
              │
  BLOCK II · CONTEXT AND MEMORY ──────────────────── ~16 h
   04 context               attention budget, context rot MEASURED, compaction
   05 memory           ⭐  three schools, a bi-temporal graph from scratch
   06 identity              SOUL/AGENTS/GRANICE — files instead of fine-tuning
              │
  BLOCK III · ACTION ─────────────────────────────── ~20 h
   07 tools                 ergonomics, blast radius, how many is too many
   08 code-mode       ⭐⭐  the agent writes a program — the biggest change of 2026
   09 protocols             MCP vs CLI vs function — measured, not debated
   10 sandbox               isolation ladder, proxy, secrets, escape attempts
              │
  BLOCK IV · PROACTIVITY AND MULTIPLICITY ────────── ~16 h
   11 scheduling       ⭐  the agent wakes up on its own and does NOT nag
   12 channels              a channel as a trust boundary
   13 fleet            ⭐  three agents, permission boundaries, cascade
              │
  BLOCK V · QUALITY AND TRUST ────────────────────── ~14 h
   14 evaluation      ⭐⭐  golden set, judge, pass^k, regression gate
   15 observability         OTel traces, replay, post-failure investigation
   16 security         ⭐  OWASP ASI01–ASI10, 20 attacks on your own fleet
              │
  BLOCK VI · PRODUCTION ──────────────────────────── ~12 h
   17 hybrid                local by default, the privacy boundary in code
   18 release               versioning, rollback, runbook
              │
   19 CAPSTONE ─────────► a personal assistant + the repeated measurement from part 1
```

⚠️ **The order is not decoration.** Part 8 (code-mode) without part 10 (sandbox)
is remote code execution with a polite interface. Part 13 (fleet) without parts 10 and 7
is a single target with the sum of all permissions. **Do not skip ahead in blocks III and IV.**

---

## The three agents you will build

They differ in **boundaries, not intelligence** — and that is the main architectural lesson
of this course.

| | **Archivist** | **Researcher** | **Steward** |
| :-- | :-- | :-- | :-- |
| Domain | local documents | searching the web | calendar, home, reminders |
| Network | ✗ none | ⭐ 4 domains via proxy | local |
| Trust in input | high | ⚠️ **zero** | medium |
| Sandbox | light | ⭐ strict | medium |
| Proactive | ✗ | ✗ **deliberately** | ⭐ yes |
| Appears from | part 2 | part 10 | part 11 |

---

## Files

| # | File | Level | What you will learn | Time |
| :-- | :-- | :-- | :-- | :-- |
| 01 | `01-AGENT-ARCHITECTURES.md` | ⭐⭐ | when **not** to build an agent, four topologies, **OpenClaw taken apart**, loop engineering | ~5 h |
| 02 | `02-SKELETON-SESSIONS-CONFIG.md` | ⭐⭐⭐ | a loopback gateway, configuration as data, **an event log with replay and branches** | ~5 h |
| 03 | `03-HARNESS-LONG-RUNNING-TASKS.md` | ⭐⭐⭐⭐ | ⭐⭐ **the most important part.** The task registry, the progress file, git as memory, five stop conditions, the error ladder | ~6 h |
| 04 | `04-CONTEXT-ENGINEERING.md` | ⭐⭐⭐⭐ | the attention budget, **a measured degradation curve of your models**, compaction in four moves | ~5 h |
| 05 | `05-LONG-TERM-MEMORY.md` | ⭐⭐⭐⭐ | three schools of memory, ⭐ **a bi-temporal graph from scratch**, fact extraction, quarantine | ~6 h |
| 06 | `06-IDENTITY-WORKING-FILES.md` | ⭐⭐⭐ | `SOUL/AGENTS/GRANICE/MEMORY/SKILL`, on-demand skills, a personality regression test | ~4 h |
| 07 | `07-TOOL-DESIGN-AND-ERGONOMICS.md` | ⭐⭐⭐⭐ | descriptions, lenient input, **the error as a prompt**, idempotency, blast radius, an ablation of the number of tools | ~5 h |
| 08 | `08-CODE-MODE.md` | ⭐⭐⭐⭐⭐ | ⭐⭐ the agent writes a program instead of calling tools. **Why this helps small models in particular** | ~6 h |
| 09 | `09-PROTOCOLS-MCP-CLI-A2A.md` | ⭐⭐⭐ | fixed cost vs discovery cost, MCP 2026-07-28, **Steinberger's thesis measured** | ~4 h |
| 10 | `10-PRODUCTION-SANDBOX.md` | ⭐⭐⭐⭐ | five rungs of isolation, **what each one stops**, proxy, secrets, 16 escape attempts | ~5 h |
| 11 | `11-SCHEDULING-PROACTIVITY.md` | ⭐⭐⭐⭐ | ⭐ `HEARTBEAT.md`, silence suppression, precision of nudges, night work, the circuit breaker | ~5 h |
| 12 | `12-CHANNELS-INTERFACES.md` | ⭐⭐⭐ | a channel as a trust boundary, pairing, routing, streaming | ~4 h |
| 13 | `13-MULTI-AGENT-FLEET.md` | ⭐⭐⭐⭐⭐ | ⭐ supervisor and fan-out, **the trust boundary between agents**, four circuit breakers, cascade | ~6 h |
| 14 | `14-EVALUATION.md` | ⭐⭐⭐⭐ | ⭐⭐ golden set, trajectory, `pass^k`, **a judge in an isolated context**, regression gate | ~5 h |
| 15 | `15-OBSERVABILITY.md` | ⭐⭐⭐⭐ | OTel GenAI traces, six metrics, **prompt replay from any turn**, investigation | ~4 h |
| 16 | `16-SECURITY-OWASP-ASI.md` | ⭐⭐⭐⭐⭐ | ⭐ ASI01–ASI10 on your system, sequence policy, **20 attacks on your own fleet** | ~5 h |
| 17 | `17-HYBRID-AND-ROUTER.md` | ⭐⭐⭐ | privacy → capability → cost, **the boundary in code**, output audit, offline test | ~4 h |
| 18 | `18-RELEASE-AND-MAINTENANCE.md` | ⭐⭐⭐⭐ | seven components of a release, rollback <5 min, memory migration, **runbook** | ~4 h |
| 19 | `19-CAPSTONE.md` | ⭐⭐⭐⭐⭐ | putting it all together + ⭐ **the repeated measurement from part 1 — the grade for the course** | ~10 h |
| — | `SOURCES.md` | — | the full annotated bibliography: **what came from where and went where** | — |

**Total: ~102 hours at the keyboard.** This is not a course to read.

---

## The anatomy of every part

A fixed structure, so that you can navigate:

```
0. Problem — why this layer exists
1-N. Theory — with a link to the source
   ⭐ "How the best do it" — OpenClaw, Anthropic, Steinberger
FROM SCRATCH — you write the mechanism yourself, with no dependencies
IN PRODUCTION — a "Yours vs off-the-shelf" table: what they add, what they cost
⭐ EXPERIMENT — hypothesis, procedure, a table TO FILL IN, a prediction
EXERCISE — produces something in the growing system
Pitfalls — numbered, with the symptom and the remedy
Checkpoint — a script that MUST pass before the next part
```

⭐ **The EXPERIMENT section is the heart of this course.** Each one has a **prediction** — what I
expect to see — and an **empty table** for your result. When they diverge,
**your measurement wins, and you fix the course.** The files are yours.

---

## The rules I keep throughout the course

1. **The mechanism from scratch, then the library.** First you write it yourself (~80 lines), then
   I show the ready-made ones: what they add, what they cost, when it is worth switching.
2. **Nothing without a measurement.** Every threshold in your system comes from an experiment, not
   from this course. Other people's numbers are a starting point, not a conclusion.
3. **At least three runs.** Agents are non-deterministic; a single run is
   an anecdote (P61).
4. **Narrowest by default.** No rule = least privilege. Everywhere (P66).
5. **Security in code, not in the prompt.** The prompt is the last line of defence,
   never the first.
6. **Every decision gets an ADR** with a falsification condition:
   *"how will I know this was a bad decision"*.
7. **Pitfalls are numbered on from course 1.** Hardware P1–P18 (pitfalls of the reference rig),
   software in course 1: P20–P52, **course 2: P60–P139**.

---

## What this course does not contain — and why

| What is missing | Why |
| :-- | :-- |
| **Repeats of course 1** | GBNF, RAG from scratch, `bwrap`, speculative decoding, multimodality — you have these. Course 2 refers back and goes higher |
| **A survey of frameworks** | LangGraph/CrewAI appear as a **point of reference in tables**, not as an excursion. The catalogue is in course 1, part 9 |
| **Fine-tuning models** | A different course. Here the model is given and the variable is the system — which the thesis in the introduction confirms |
| **A2A** | Covered in part 9, but **not needed as long as all the agents are yours** |

---

## Before you start

```bash
cd ~/llm-education   # the repository directory (yours may differ)
source rig-env.sh
$LB/llama-cli --version                     # expect: a build from commit 987498f
rocm-smi --showid                           # 2× R9700 + iGPU as GPU[2]
python3 --version                           # expect ≥ 3.12
which bwrap systemd-run sqlite3 git         # all four required
test -f $AGENT/agent.py && echo "✓ the loop from course 1 — the starting point"
```

⚠️ **`HIP_VISIBLE_DEVICES=0,1` must be set** (P12/P32 from course 1) — otherwise small
models land on the iGPU with 2 GB.

⚠️ **After you add cards 3 and 4 the numbering will change (P13).** Remap through `amd-smi
list`, update `rig-env.sh` and **repeat experiments 4, 7, 8, 13 and 17** — all
the thresholds come from measurements on two cards.

---

## Registry of software pitfalls — P60–P139

Eighty pitfalls. Each has its symptom and remedy in its own part.

| ID | Pitfall | Part |
| :-- | :-- | --: |
| P60 | Building an agent where a workflow is enough | 1 |
| P61 | Measuring with a single run | 1 |
| P62 | Accepting an authority's claims without checking the context | 1 |
| P63 | Printing to `stdout` in the gateway process | 2 |
| P64 | Writing without `fsync` | 2 |
| P65 | Sorting events by `ts` instead of by `seq` | 2 |
| P66 | The default trust level = the wider one | 2 |
| P67 | The agent changes or deletes a test to make it pass | 3 |
| P68 | A registry entry too big for one session | 3 |
| P69 | Skipping the baseline verification at startup | 3 |
| P70 | Lack of progress mistaken for lack of activity | 3 |
| P71 | An error message unreadable to the model | 3 |
| P72 | Trusting the declared context length | 4 |
| P73 | A variable value before a constant prefix | 4 |
| P74 | Compaction right away, without moves 1 and 2 | 4 |
| P75 | The summary rounds off numbers | 4 |
| P76 | The system prompt grows and never shrinks | 4 |
| P77 | Overwriting a fact instead of invalidating it | 5 |
| P78 | Confusing world time with system time | 5 |
| P79 | A fact without a quote and a source | 5 |
| P80 | No scope — memory leaks between agents | 5 |
| P81 | An untrusted session writes to persistent memory | 5 |
| P82 | Boundaries only in the prompt, with no enforcement | 6 |
| P83 | All skills loaded always | 6 |
| P84 | The agent edits `AGENTS.md` or `GRANICE.md` | 6 |
| P85 | A `SKILL.md` from an unread source | 6 |
| P86 | Two tools with overlapping descriptions | 7 |
| P87 | A raw traceback as a tool result | 7 |
| P88 | Tools not filtered by session trust | 7 |
| P89 | No idempotency for a side effect | 7 |
| P90 | A fixed blast radius instead of a computed one | 7 |
| P91 | A swallowed traceback | 8 |
| P92 | Paths not checked inside the API | 8 |
| P93 | No limit on calls in the program | 8 |
| P94 | The model prints raw content | 8 |
| P95 | Accepting the "23k tokens" figure without checking your own configuration | 9 |
| P96 | Assuming the model will cope with `--help` | 9 |
| P97 | An MCP server as a trusted element of the system | 9 |
| P98 | Three interfaces to one capability maintained in parallel | 9 |
| P99 | Confusing a container with a sandbox | 10 |
| P100 | No resource limits with `bwrap` | 10 |
| P101 | The environment inherited into the sandbox | 10 |
| P102 | `HTTP_PROXY` as a network control | 10 |
| P103 | Believing the sandbox protects against injection | 10 |
| P104 | Two instances of the scheduler | 11 |
| P105 | No idempotency on restart | 11 |
| P106 | Silence recognised only by an exact string | 11 |
| P107 | No quiet hours and no daily limit | 11 |
| P108 | No circuit breaker after a series of errors | 11 |
| P109 | A channel as mere input, with no trust | 12 |
| P110 | Replying to unknown senders | 12 |
| P111 | Comparing a token with `==` | 12 |
| P112 | Splitting a message in the middle of a code block | 12 |
| P113 | No limit on delegation depth | 13 |
| P114 | A subagent's result treated as a command | 13 |
| P115 | Splitting along tasks instead of permissions | 13 |
| P116 | No partial degradation | 13 |
| P117 | A supervisor with domain tools | 13 |
| P118 | The agent grades itself | 14 |
| P119 | No "correct refusal" category | 14 |
| P120 | A single run per question | 14 |
| P121 | An uncalibrated judge | 14 |
| P122 | A golden set generated by the model under test | 14 |
| P123 | Alerts built directly on `gen_ai.*` | 15 |
| P124 | Traces with full content forever | 15 |
| P125 | Telemetry export done synchronously | 15 |
| P126 | Believing that traces will show everything | 15 |
| P127 | A pattern filter as the main defence against injection | 16 |
| P128 | A fact in memory without a quote and a source | 16 |
| P129 | A summary for approval generated by the model | 16 |
| P130 | The checksum verified only at installation | 16 |
| P131 | No behavioural baseline | 16 |
| P132 | The privacy gate bypassed in escalation | 17 |
| P133 | A boundary based on patterns instead of on the source | 17 |
| P134 | An unread `stop_reason` | 17 |
| P135 | A silent dependence on the cloud | 17 |
| P136 | A release with uncommitted changes | 18 |
| P137 | Rolling back code without a backward memory migration | 18 |
| P138 | `cp` instead of `sqlite3 .backup` | 18 |
| P139 | A model not versioned by checksum | 18 |

---

## Where things live

| Path | Role |
| :-- | :-- |
| `00-INDEX.md` | this file — the map and the pitfall registry |
| `01`–`19` | the parts of the course, in order |
| [`SOURCES.md`](SOURCES.md) | **the annotated bibliography** — what was taken from what and where it was used |
| [`skeleton/`](skeleton/) | the starter skeleton of `$OSA/` to copy |
| [`../course_local_models/00-COURSE-INDEX.md`](../course_local_models/00-COURSE-INDEX.md) | ⬅️ **course 1** — the model from the inside |
| `../../rig-env.sh` | paths to models and binaries, visible cards |

**What will come into being along the way:**

```
$OSA/
├── brama.py konfig.py sesje.py harness.py kontekst.py     pt. 2–4
├── decyzje/          ADRs with a falsification condition   pt. 1
├── pomiary/          ⭐ experiment results — one file per part
├── dziennik/         sessions + OTel traces                pt. 2, 15
├── agenci/           archiwista/ badacz/ gospodarz/        pt. 6
├── narzedzia/        registry, radius, idempotency         pt. 7
├── kod/              code-mode: API + execution            pt. 8
├── piaskownica/      levels, proxy, secrets                pt. 10
├── harmonogram/      scheduler                             pt. 11
├── kanaly/           socket, HTTP, routing                 pt. 12
├── flota/            delegation, trust, circuit breakers   pt. 13
├── ewaluacja/        golden set, judge, gate               pt. 14
├── obserwacja/       tracer, metrics, replay               pt. 15
├── bezpieczenstwo/   isolation, sequences, drift, consents pt. 16
├── router/           privacy boundary, output audit        pt. 17
├── wydanie/          manifest, release, rollback, check    pt. 18
├── testy/            golden set, escapes, 20 attacks
├── RUNBOOK.md        ⭐ what to do at 3:00
└── STOP.sh           ⭐ the emergency stop
```

---

## Three numbers you will know after this course

Nobody else knows them, because they come from your machine:

1. **Where the synthesis of your models breaks down** — the real context limit, not the
   declared one (part 4).
2. **How many tools they withstand** — before the choice starts to degrade (part 7).
3. **By how much the harness beats the model** — and whether it is worth buying a bigger one (part 14).

⭐ **The third is the most important.** If you know it, you stop guessing and start
engineering.

---

**Start: `01-AGENT-ARCHITECTURES.md`.**
The first experiment will find five places where your current loop breaks.
**That is the programme for the rest of the course.**
