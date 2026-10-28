# Part 1 · Agent architectures — a map of the terrain

**Level:** ⭐⭐ · **Time:** ~5 h · **Requires:** course 1, part 6 (the agent loop)
**Produces:** a diagnosis of your loop from course 1, an architectural decision in writing, the `$OSA/` directory

---

## 0. What changes between course 1 and course 2

In course 1 you built a **loop**. It reads a file, writes a file, runs a command, remembers
a dozen or so turns, and runs inside `bwrap`. That is a real agent and it is not a toy.

But try to make it do what you announced: **several agents that work
for weeks, wake up on their own and cooperate**. It will break in five places, and not
because it is badly written:

| What breaks | Why | The part that fixes it |
| :-- | :-- | :-- |
| The context runs out after ~40 minutes of work | The loop has no compaction and no external memory | 3, 4, 5 |
| After a restart it does not know what it was doing | The history lives in process memory | 2, 3 |
| You cannot ask it "why did you do that" | There are no traces, only the result | 15 |
| Adding the 20th tool spoils the choice of the first 19 | Tool descriptors eat the context and confuse the model | 7, 8 |
| Two agents at once are two independent worlds | There is no gateway, no session and no shared state | 2, 12, 13 |

**Course 2 does not teach a better loop. It teaches a system in which the loop is one of eight
elements** — and not the hardest one.

> ⭐ **One sentence that sums up the whole course.**
> The loop is 10% of the work. Sessions, memory, scheduling, the sandbox, observability
> and evaluation are the other 90% — and they decide whether an agent is a tool
> or a curiosity.

---

## 1. Before you build an agent — four questions that save a month

In [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
Anthropic gives four criteria. I am rewriting them, because **three of the four answers sound
different for you than for a company with a cloud**.

**1 · Complexity.** Is the task multi-step and hard to describe fully up front?

- "Extract the title from this PDF" → **this is not a task for an agent.** It is a single call
  with a grammar. An agent will add 30× the cost and introduce uncertainty where there was none.
- "Go through my documents from the last quarter and tell me what I forgot about" →
  **this is a task for an agent.** You do not know up front how many files need to be read or what to
  look for.

**2 · Value.** Does the result justify the cost and the latency?

For you, "cost" means something different than for others. **You do not pay per token.** You pay
**in card time and electricity** — and that is a real budget, but a completely differently shaped one.
An agent that grinds for 40 minutes at night costs you pennies. The same agent in the cloud
would cost a dozen or so dollars. **This moves the profitability line very strongly in your
favour** and is the main reason it is worth building locally.

**3 · Feasibility.** Can the model do it at all?

Here you have a harder constraint than someone on a frontier model. `gpt-oss-20b` will call a
tool correctly in over 90% of simple cases, but **end-to-end on a multi-step task the published
numbers drop to 80–90%**
([LLM Configurator](https://llmconfigurator.com/en/guides/coding-agents/tool-calling-local-models)),
because tool-selection errors and argument errors **multiply across the number of steps**.

Work it out on a napkin. At 92% success per step:

```
 3 steps  →  0.92³  =  78 %
 8 steps  →  0.92⁸  =  51 %
15 steps  →  0.92¹⁵ =  29 %
```

⭐ **This is the most important arithmetic in the whole course.** You will not fix it with a better
prompt. You fix it by **shortening the chain** (part 8, code-mode), **verifying along the
way** (part 14) and **recovering from errors** (part 3). All three are work
on the system, not on the model.

**4 · Cost of error.** Can an error be detected and undone?

This question decides **what the agent is allowed to do**, and it returns in parts 10, 12 and 16. Remember
the rule: *if you cannot detect that the agent made a mistake, do not give it that tool.*

---

## 2. The spectrum: from workflow to agent

The market calls everything an "agent". The distinction that matters from an engineering standpoint is
one: **who decides the next step — your code or the model?**

```
  YOUR CODE DECIDES                              THE MODEL DECIDES
  ├───────────────┼──────────────┼──────────────┼───────────────┤
  1 call          chain          router         loop            fleet
                  (chain)        (routing)      (agent)         (multi-agent)

  predictable     predictable    semi-pred.     unpredictable   unpredictable²
  1 call          N calls        1-2 calls      ? calls         ?? calls
  known cost      known cost     known cost     unknown cost    unknown cost
  easy tests      easy tests     easy tests     hard tests      very hard
```

**The rule I keep throughout the course:** *move right only when the left
side has proven it is not enough.* Every step to the right buys flexibility at the price of
predictability — and predictability is what lets you sleep.

> 💡 **In practice.** In the system you will build, **most of the work will be done by workflows, not
> agents.** A Steward checking the calendar is a workflow. A Steward that noticed a
> conflict and is looking for how to resolve it is an agent. **The same "agentic application" contains
> both layers** and that is healthy — not a shortcoming.

---

## 3. Four ways to build an agent

It is worth knowing all four, because **they get confused with one another even by the people who build them**.
One question separates them: **who supplies the harness, and who supplies the deployment?**

| # | Way | You write | Harness | Deployment | When |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | **Hand-written loop** | everything | Yours | Yours | When you want to understand. **This is course 1 and the base of course 2** |
| 2 | **Tool runner from an SDK** | only the tools | SDK | Yours | When you want it fast, but with control over the hooks |
| 3 | **Managed agent** | the configuration | the vendor's | the vendor's | When state and sessions should be someone else's problem |
| 4 | **Ready-made coding harness** (Claude Agent SDK, OpenHands) | the prompt | libraries | Yours | When you want a coding agent, not to build an agent |

**For you 3 and 4 are out**, and not for ideological reasons:

- **3 is out** by definition — a managed agent means someone else's process, someone else's state and someone else's
  availability. The whole thesis of your project is the opposite.
- **4 is out as a goal**, but **not as a point of reference**. The Claude Agent SDK is
  superbly designed and in parts 3, 7 and 13 I compare your solutions with it.

What remains is **1 with elements of 2**: you write the loop yourself, but you do not reject libraries where
they hide nothing. That is exactly what we established as the course's rule.

---

## 4. Topologies — how agents arrange themselves relative to one another

Four layouts. Each has a place where it dies.

### 4.1 · Hub-and-spoke (star) — one gateway, many channels and tools

```
        channels                GATEWAY                tools
    CLI  ─────┐            ┌──────────────┐        ┌──── files
    HTTP ─────┼───────────►│   sessions   │◄───────┼──── shell
    Signal ───┤            │   routing    │        ├──── network
    cron ─────┘            │   policies   │        └──── memory
                           └──────┬───────┘
                                  │
                           ┌──────▼───────┐
                           │  RUNTIME     │  ← the agent loop
                           └──────────────┘
```

**This is how OpenClaw is built** and this is how you will build your system. Advantages: one place for the
security policy, one for session state, one to observe. Drawback: the gateway is a
single point of failure — which is why in part 18 you learn to restart it without losing state.

### 4.2 · A graph with typed state

The nodes are functions or agents, the edges are transitions, and the state is explicit and typed. This is how
LangGraph works. Great when the flow is **known up front and must be auditable**.
Weak when you do not know the shape of the task — and in a personal agent you usually do not.

### 4.3 · Hierarchy (supervisor and executors)

The supervisor breaks the task down, the executors carry it out in a **clean context** and return
a summary of 1–2k tokens. This is the subagent pattern from
[Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
It works great for parallel searching. **It costs a fixed delegation fee**
(pitfall P41 from course 1) and therefore loses on short tasks.

### 4.4 · Swarm / bulletin board

Agents write to and read from a shared board, with no central supervisor. Elegant
and **almost always a bad choice to start with**: unpredictable, hard to debug, and
maximally prone to cascading failure.

> ⚠️ **A number that should intimidate you.** According to OWASP, one compromised server
> **in 72.4% of cases dragged further ones into acting**
> ([Teleport](https://goteleport.com/blog/owasp-top-10-agentic-applications/)).
> A topology in which everyone talks to everyone is a topology in which a single
> mistake becomes everyone's mistake. We return to this in parts 13 and 16.

---

## 5. OpenClaw taken apart

You asked me to check it — and rightly so, because it is the best-documented working
system of its class. We are not copying it. **We take it apart to see which decisions have to be
made**, and some of them we will make differently.

### 5.1 · Four blocks

| Block | What it does | Where in the course |
| :-- | :-- | :-- |
| **Gateway** | The single source of truth about sessions, routing and channels. Listens on `127.0.0.1:18789`, **on the loopback only** | part 2, 12 |
| **Brain** (runtime) | Assembles the system prompt from the working files, calls the model with failover, intercepts tool calls | part 3, 6 |
| **Hands** (tools) | Executes — on the host or in a sandbox, depending on the session's trust level | part 7, 10 |
| **Memory** | SQLite with hybrid search: vectors + BM25 | part 5 |

### 5.2 · Six phases of handling a message

This is the skeleton you will implement in part 2. It is worth knowing the times, because they show
**where the time really goes** (figures from the OpenClaw description, to be verified on your own):

```
1. Intake                 the channel adapter receives the message
2. Access control         allowlist, pairing, session type           < 10 ms
3. Context assembly       working files + history + memory           < 100 ms
4. Model call             streaming from the provider           200–500 ms to the 1st token
5. Tool execution         shell, files, browser                 100 ms – 3 s
6. Delivery               formatting, splitting, saving state
```

⭐ **Note the proportions.** Security costs **under 10 ms**. Context assembly
**under 100 ms**. Everything else is the model and the tools. This means that **you have no
excuse to economise on access control** — it is free compared with
what you are doing anyway.

### 5.3 · Session resolution — an idea I am stealing whole

OpenClaw maps a message to a session with an **explicitly named trust level**:

```
message from the console       →  main                          (host, full permissions)
private from a channel         →  agent:main:<channel>:dm:<id>     (sandbox)
from a group                   →  agent:main:<channel>:group:<id>  (sandbox, narrower)
```

**This is the best single decision in this architecture.** The trust level is not
a flag stuck onto a tool — it is **a property of the session, following from where the message
came from**. You cannot forget about it, because without a session there is no call.
You implement this in part 2, you enforce it in part 10.

### 5.4 · Working files as the program

```
AGENTS.md     core instructions         ← what the agent is to do
SOUL.md       personality and tone      ← how it is to do it, grows over time
MEMORY.md     what it knows about you   ← auditable, you open it and read it
HEARTBEAT.md  a list of things to watch ← cron expressed in plain language
SKILL.md      a single capability       ← loaded on demand when needed
```

⭐ **Why this is brilliant, not primitive.** The agent's behaviour is **a text
file that you open, read, version in git and roll back**. The alternative —
fine-tuning the model — gives the same behaviour in a form that **cannot be read,
shown to anyone or rolled back**. For an agent touching your affairs this is not an aesthetic
choice.

### 5.5 · What OpenClaw teaches by counterexample

I am not idealising it. Three documented problems (plus a fourth incident), each of which is material for
part 16:

| Problem | What it teaches |
| :-- | :-- |
| The Secret Store **not encrypted at rest** in 2.0 | Secrets are a separate layer, not a field in the configuration (part 10) |
| The sandbox **not enabled by default** | The default value is a security policy. For you it is **enabled** by default (part 10) |
| Cisco: third-party skills with **real exfiltration** | The skills supply chain is ASI04. A closed, signed set (part 16) |
| The MoltMatch incident — the agent acted outside its intent | Proactivity requires boundaries, not just capabilities (part 11) |

---

## 6. Loop engineering — a counterpoint you have to know

Peter Steinberger, the author of OpenClaw, wrote in June 2026:

> "Here's your monthly reminder that you shouldn't be prompting coding agents anymore.
> You should be designing loops that prompt your agents."

**This is the most important sentence about agents that I found in the whole research**, and it is worth
unpacking, because it sounds like a slogan and is not one.

**Prompting** = you optimise a single input to the model. You improve the wording,
add examples, ask it to "take your time".
**Loop engineering** = you optimise **the machine that generates the inputs**. What the agent
gets at the start of every turn. When it stops. What it sees after an error. How it
hands the work to the next session. Who checks the result.

The difference is like that between writing one good SQL query and designing a database
schema. **The first scales linearly with your time. The second scales by itself.**

### 6.1 · The rest of Steinberger's theses — and where I disagree with him

| His thesis | Rationale | My comment for you |
| :-- | :-- | :-- |
| **MCP and RAG are context poison** | GitHub MCP ≈ 23k tokens. A CLI costs **zero**, because the model already knows it and will read `--help` | ⭐ A strong thesis, testable — **we measure it in part 9**. For you context is more expensive than for him (smaller models), so the argument is even stronger |
| **Prompts of 1–2 sentences + a picture** | A good model will read the code itself | ⚠️ **This depends on the model.** He uses a frontier one. `gpt-oss-20b` needs more guidance. Do not copy this without a measurement |
| **No planning mode** | Good models do not need the theatre | ⚠️ For your models **an explicit plan really helps** — it returns in part 3 as a feature list |
| **No subagents** | "Working around a broken system" | ⚠️ I disagree for small models: a subagent's clean context is **the only way to recover the attention budget**. You settle it by measurement in part 13 |
| **Blast radius** as a planning unit | How many files this change will touch | ⭐ **Unquestionably good.** It enters parts 7 and 16 as a tool design criterion |
| **3–8 agents in parallel, atomic commits** | No branches, faster | ⭐ Good and feasible for you too — part 13 |

> 🎯 **How to use this.** Steinberger is right **in his context**: an experienced
> engineer, a frontier model, programming tasks, full trust in the machine.
> **Three of those four conditions do not hold for you.** That is why throughout the course I
> put his theses next to a measurement and make you settle it yourself. **The ability
> to settle it is worth more than choosing a side.**

---

## 7. A finding that changes priorities

From research on agent benchmarks
([Prefactor](https://prefactor.tech/learn/agent-benchmarks)):

> **An agent's result changes more with the harness than with the model.** The same model under
> two different scaffolds gives significantly different numbers. The harness decides how
> tools are exposed, how errors are shown and how many attempts the agent gets.

Read that again, because it has a financial consequence. **The variable over which you have
full control — the harness — is more important than the variable over which you have zero control —
the model weights.** The time spent choosing a model is largely wasted as long as the
harness is weak.

⭐ **This is the justification for this course existing** and the reason it has no
part on fine-tuning models.

---

## 8. FROM SCRATCH — an architectural decision in writing

Before you write a line of code, write an **ADR** (Architecture Decision Record). It is one
page that in six months will answer the question "why is this done this way".

```bash
mkdir -p $OSA/decyzje
cd $OSA
```

```bash
cat > $OSA/decyzje/0001-topologia.md <<'EOF'
# ADR 0001 · System topology

- **Date:** <today>
- **Status:** accepted
- **Context:** I am building a system for 3+ personal agents working for weeks
  on my own hardware, some of which reach out to the network.

## Decision

Hub-and-spoke with a single gateway on the loopback.

## Why not otherwise

- **A graph with typed state** — rejected, because I do not know the shape of the tasks up front.
- **Swarm / bulletin board** — rejected, because of cascading failure (72.4% per OWASP) and no
  single place for policy.
- **Hierarchy** — not as the system's topology, only as a pattern inside
  a single task (subagents, part 13).

## Consequences

- (+) one place for the security policy, sessions and observability
- (+) every conversation can be replayed from a single log
- (−) the gateway is a single point of failure → needs a restart without losing state (part 18)
- (−) everything passes through a single process → a throughput limit (I measure it in part 13)

## How I will know this was a bad decision

When the gateway becomes a bottleneck with >3 parallel sessions — then the
runtime moves out into a separate process and the gateway stays.
EOF
```

> 💡 **The last section is the most important and almost nobody writes it.** "How I will know
> this was a bad decision" turns an opinion into **a hypothesis with a falsification condition**. Without it
> an ADR is just a nicely formatted prejudice.

---

## 9. IN PRODUCTION — what the frameworks do that you do not

To know what you are rejecting, you have to know what you are getting.

| Layer | LangGraph | CrewAI | Claude Agent SDK | **You** |
| :-- | :-- | :-- | :-- | :-- |
| Loop | graph, typed state | roles and tasks | full, built in | you write it (course 1) |
| Persistence | checkpointer | limited | sessions | event log (pt. 2) |
| Tools | decorator | decorator | built in + MCP | registry (pt. 7) |
| Sandbox | none | none | permissions | isolation ladder (pt. 10) |
| Memory | LangMem | basic | files + compaction | bi-temporal (pt. 5) |
| Scheduling | none | none | none | ⭐ heartbeat (pt. 11) |
| Traces | LangSmith | OTel | built in | OTel (pt. 15) |
| **Local model** | via an adapter | via LiteLLM | ⚠️ designed for Claude | ⭐ **first-class** |

**The two starred rows are the reason you build it yourself.** No framework
treats scheduling as a first-class layer, and all of them treat a local model
as an adapter bolted on from the side. For you it is **the core, not a plugin**.

> ⚠️ **Honestly: when a framework beats you.** When you need a flow that is
> to be auditable and approved by someone from outside — a graph with typed state is
> better than your loop, because **it can be drawn and shown**. Remember this for the moment
> when your product meets a compliance requirement.

---

## 10. EXPERIMENT 1 — where your loop from course 1 breaks

**Hypothesis:** the loop from `$AGENT/agent.py` copes with tasks of up to ~5 steps, and above
~10 steps it fails **not because of model quality, but because of the lack of system layers**.

**Procedure.** Prepare five tasks of increasing chain length and run each **three
times** (because what interests you is repeatability, not a one-off success):

```bash
cd ~/llm-education   # the repository directory (yours may differ)
source rig-env.sh
mkdir -p $OSA/pomiary
```

| # | Task | Steps ~ | What it checks |
| :-- | :-- | --: | :-- |
| Z1 | "Read `plik.txt` and tell me how many lines it has" | 2 | the reference point |
| Z2 | "Find all the PDFs from 2026 in `~/dokumenty` and list their names" | 4 | tool choice |
| Z3 | "For each of those PDFs give the first line" | 8 | a loop over results |
| Z4 | "Do the same, but save the result to a CSV and check that it was saved" | 12 | writing + verification |
| Z5 | "Repeat Z4, but if the file already exists, append only the new ones" | 18 | state + a condition |

For every run, note:

```
task    | attempt | success | steps | tokens | time | failure mode
--------|---------|---------|-------|--------|------|-------------
Z1      | 1       | yes     | 2     |  1,840 | 4 s  | —
...
```

**Name the failure modes from this list** — it will be your map for the rest of the course:

| Code | Failure mode | Part that fixes it |
| :-- | :-- | :-- |
| `KONTEKST` | the window filled up, the agent forgot the goal | 3, 4 |
| `NARZĘDZIE` | it chose the wrong tool or the wrong arguments | 7, 8 |
| `PĘTLA` | it got stuck in a loop, repeating the same step | 3 |
| `CICHY` | it said "done", and did not do it | 3, 14 |
| `BŁĄD` | it got an error and gave up instead of correcting | 3 |
| `STAN` | it lost track of what it had already done | 2, 5 |

**What I expect** (⚠️ to be checked on your own, this is a prediction, not a measurement):

```
Z1  ███████████████████████  100 %
Z2  ████████████████████     ~90 %
Z3  ██████████████           ~65 %     ← NARZĘDZIE starts here
Z4  ███████                  ~35 %     ← CICHY and BŁĄD come in here
Z5  ██                       ~10 %     ← KONTEKST and STAN dominate here
```

**Keep this file.** In part 19 you will repeat exactly the same experiment on the finished
system and **this comparison is the grade for the whole course**.

---

## 11. EXERCISE — setting up the system

```bash
mkdir -p $OSA/{decyzje,pomiary,dziennik,konfiguracja,agenci,narzedzia,pamiec,testy}
cd $OSA && git init && git add -A && git commit -m "part 1: directory skeleton"
```

```
$OSA/
├── decyzje/        ADRs — why it is this way and not another
├── pomiary/        experiment results, one file per part
├── dziennik/       session logs (part 2)
├── konfiguracja/   configuration as data (part 2)
├── agenci/         Archivist, Researcher, Steward — working files (part 6)
├── narzedzia/      tool registry (part 7)
├── pamiec/         bi-temporal store (part 5)
└── testy/          golden set and the evaluation harness (part 14)
```

⭐ **`git init` is not decoration.** In part 3 git becomes the **agent's memory
mechanism** — the way a new session learns what the previous one did. Start
committing from today.

**Homework:** write `decyzje/0002-modele.md`. Which model will be the default for the
loop, which for hard tasks, and **how you will know you chose wrong**. Without this
you will not build the router in part 17, because you will have no criterion.

---

## 12. Pitfalls of this part

| ID | Pitfall | Symptom | How to avoid it |
| :-- | :-- | :-- | :-- |
| **P60** | **Building an agent where a workflow is enough** | The task works, but 30× more expensively and sometimes fails randomly | The four criteria from §1. If you can draw the flow, you do not need an agent |
| **P61** | **Measuring with a single run** | "It works!" — and on the third run it does not | Always ≥3 runs. Agents are non-deterministic **by definition**, a single run is an anecdote |
| **P62** | **Accepting an authority's claims without checking the context** | You copy "no MCP, no subagents" and lose a month | Check whether the author's conditions hold for you. Usually they do not — the model, the scale and the risk are different |

---

## 13. Checkpoint — what you have after this part

```bash
# Should pass in full:
test -d $OSA/decyzje            && echo "✓ directories"
test -f $OSA/decyzje/0001-topologia.md && echo "✓ ADR 0001"
test -f $OSA/decyzje/0002-modele.md    && echo "✓ ADR 0002"
test -f $OSA/pomiary/01-gdzie-peka.md  && echo "✓ baseline measurement"
git -C $OSA log --oneline | head -3
```

- [ ] You know when **not** to build an agent
- [ ] You can calculate why a 15-step chain at 92%/step gives 29%
- [ ] You know the four topologies and which one dies and how
- [ ] You have taken OpenClaw apart into Gateway / Runtime / Tools / Memory
- [ ] You understand the difference between prompting and designing a loop
- [ ] **You have measured where your current loop breaks** — that is the map for the rest of the course

---

**Next: `02-SKELETON-SESSIONS-CONFIG.md`** — you build the gateway, configuration as data
and an event log from which you will replay any conversation down to the bit.
