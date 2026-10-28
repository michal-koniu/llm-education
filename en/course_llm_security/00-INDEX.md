# Course 3: security of LLMs, agentic apps and local models — index

**Created 28 October 2026.**
A continuation of course 1 — [`../course_local_models/00-COURSE-INDEX.md`](../course_local_models/00-COURSE-INDEX.md) —
and course 2 — [`../course_agentic_apps/00-INDEX.md`](../course_agentic_apps/00-INDEX.md).

> **Purpose of the whole thing.** After this course you can **attack your own models, apps and setups the way an
> attacker would, understand why each attack works down to the tokens, and close it with a defence whose effect you
> have measured.** Before you let other people use what you built, you know exactly where it is weak.
>
> Course 1 taught **how a model works**. Course 2 taught **how to build a system around it**. Course 3 teaches
> **how that system breaks — and how to make it hold.**

---

## The thesis the whole course stands on

> **A language model cannot tell instructions from data. Everything it reads can steer it.** There is no
> equivalent of a parameterised SQL query for prompts, and none is coming soon.

So the security of an LLM application is decided **outside the model**: in what the model is allowed to read,
which tools it holds, where its output goes, and what happens when it is wrong. A system prompt that says
"never do X" is a wish, not a control. Safety training of an open-weight model you run yourself is a habit,
not a boundary.

⭐ **Every defence in this course is measured.** You run the same attacks k times against the lab, before and
after the defence, and read the attack success rate (ASR) with a confidence interval. A defence that does not
move the number is decoration — the course tells you so when that happens.

---

## Who this is for and what it is not

- **For:** people who build agents and run local models (llama.cpp / llama-server, Ollama, vLLM, Open WebUI-style
  chat UIs, MCP tools, skills) and want to ship them to other people without being the next incident report.
- **Defensive by design.** You attack **only the lab on 127.0.0.1 and your own machines**. Success is shown with
  canary strings, marker files and requests to the lab's own "attacker" server — never with real malware, real
  victims or harmful content. Jailbreak experiments target the lab's harmless topic policy.
- **Not a catalogue of payloads.** Attack techniques are explained so that you recognise them and can test for
  them. Where a technique is only described (optimisation attacks, adaptive attacks, removing safety training,
  inferring other users' data), the course says why.

---

## The path

```
  BLOCK I · FOUNDATIONS ──────────────────────────── ~13 h
   01 threat landscape          trifecta, OWASP LLM / ASI, ATLAS, NIST, DFD + STRIDE
   02 the lab              ⭐⭐  Sieve: a deliberately vulnerable assistant + ASR harness
   03 mechanics            ⭐   templates, special tokens, roles, why no "prepared statement"
              │
  BLOCK II · THE MODEL ITSELF ────────────────────── ~9 h
   04 jailbreaks                families, optimisation attacks, alignment is not a boundary
   05 direct injection          goal hijack, system-prompt leaks, policy in code
              │
  BLOCK III · THE APP AROUND THE MODEL ───────────── ~23 h
   06 indirect injection   ⭐⭐  web, documents, hidden carriers, RAG poisoning
   07 agents & exfiltration ⭐⭐ excessive agency, exfil channels, taint, CaMeL-style agent
   08 MCP, skills, memory       tool poisoning, rug pulls, memory persistence, multi-agent
   09 output & resources        XSS / SQL / code from model output, runaway loops, quotas
              │
  BLOCK IV · MODELS, DATA, INFRASTRUCTURE ────────── ~13 h
   10 model supply chain   ⭐   pickle, GGUF, chat templates, backdoors, hash pinning
   11 privacy                   memorisation, embeddings, tenants, caches, logs
   12 local infrastructure      exposed servers, 0.0.0.0, DNS rebinding, proxy + auth
              │
  BLOCK V · DEFENCE AS ENGINEERING ───────────────── ~19 h
   13 guardrails & red-teaming  guards as classifiers, adaptive attacks, CI gate
   14 detection & response      audit log, canary tripwires, lockdown, runbook, replay
   15 CAPSTONE ────────────────► the hardened stack, final scoreboard, red-team report
```

⚠️ **Part 02 is mandatory before anything with a lab.** Parts 06 and 07 are the core of the course: most real
incidents of 2023–2026 are indirect injection plus an exfiltration channel. Do not skip them.

---

## Files

| # | File | Level | What you will learn | Time |
| :-- | :-- | :-- | :-- | :-- |
| 01 | [`01-THREAT-LANDSCAPE-AND-MODELLING.md`](01-THREAT-LANDSCAPE-AND-MODELLING.md) | ⭐⭐⭐ | why LLM security differs, the model as a confused deputy, **the lethal trifecta**, OWASP LLM 2025 / ASI / MITRE ATLAS / NIST AI 100-2, an incident timeline, DFD + STRIDE, a threat model of the lab | ~4 h |
| 02 | [`02-THE-LAB.md`](02-THE-LAB.md) | ⭐⭐⭐ | ⭐⭐ **the lab:** Sieve, tools, canaries, the attacker server, the harness, ASR with Wilson intervals, your first baseline | ~4 h |
| 03 | [`03-WHY-MODELS-ARE-ATTACKABLE.md`](03-WHY-MODELS-ARE-ATTACKABLE.md) | ⭐⭐⭐⭐ | chat templates → tokens, special tokens and role forgery, instruction hierarchy and its limits, safety training as learned behaviour, **why prompts have no parameterised query** | ~5 h |
| 04 | [`04-JAILBREAKS-AND-ALIGNMENT.md`](04-JAILBREAKS-AND-ALIGNMENT.md) | ⭐⭐⭐ | jailbreak families (role-play, many-shot, Crescendo, encodings, prefill, GCG/AutoDAN/PAIR/TAP), **why open-weight alignment is not a boundary**, a gateway role check and an output policy gate | ~5 h |
| 05 | [`05-DIRECT-PROMPT-INJECTION-AND-PROMPT-LEAKS.md`](05-DIRECT-PROMPT-INJECTION-AND-PROMPT-LEAKS.md) | ⭐⭐⭐ | goal hijack and system-prompt extraction, **why a secret in a prompt is already leaked**, a measured defence ladder: canary checks, no secrets in prompts, policy in code | ~4 h |
| 06 | [`06-INDIRECT-PROMPT-INJECTION-AND-RAG-POISONING.md`](06-INDIRECT-PROMPT-INJECTION-AND-RAG-POISONING.md) | ⭐⭐⭐⭐ | ⭐⭐ injection through pages, documents and tool results, hidden carriers, PoisonedRAG, sanitising, spotlighting, detectors, an ingest scanner — **before/after ASR** | ~6 h |
| 07 | [`07-AGENTS-TOOLS-AND-EXFILTRATION.md`](07-AGENTS-TOOLS-AND-EXFILTRATION.md) | ⭐⭐⭐⭐⭐ | ⭐⭐ excessive agency, exfiltration channels (images, links, tool arguments, e-mail), real cases incl. EchoLeak, renderer policy, egress allowlist, **taint-based tool gating, a CaMeL-style agent** | ~7 h |
| 08 | [`08-MCP-SKILLS-MEMORY-AND-MULTI-AGENT.md`](08-MCP-SKILLS-MEMORY-AND-MULTI-AGENT.md) | ⭐⭐⭐⭐ | MCP threat model (tool poisoning, rug pulls, shadowing), skills as supply chain, **memory poisoning and persistence**, agent-to-agent trust, pinning and memory quarantine | ~5 h |
| 09 | [`09-OUTPUT-HANDLING-CODE-AND-RESOURCES.md`](09-OUTPUT-HANDLING-CODE-AND-RESOURCES.md) | ⭐⭐⭐⭐ | model output as untrusted input: XSS, SQL, shell, code execution, package hallucination; **unbounded consumption** on a local GPU server; quotas and circuit breakers | ~5 h |
| 10 | [`10-MODEL-SUPPLY-CHAIN.md`](10-MODEL-SUPPLY-CHAIN.md) | ⭐⭐⭐⭐ | ⭐ **model files are programs:** pickle opcodes, `weights_only`, safetensors, GGUF and template CVEs, `trust_remote_code`, backdoors; an opcode scanner, a GGUF reader and hash pinning from scratch | ~5 h |
| 11 | [`11-PRIVACY-AND-DATA-LEAKAGE.md`](11-PRIVACY-AND-DATA-LEAKAGE.md) | ⭐⭐⭐⭐ | memorisation, membership inference, embedding inversion, **leaks between tenants**, shared prompt caches, logs; ownership checks in code, a secrets sweep, a guest-user experiment | ~4 h |
| 12 | [`12-LOCAL-INFRASTRUCTURE.md`](12-LOCAL-INFRASTRUCTURE.md) | ⭐⭐⭐ | exposed inference servers and chat UIs, `0.0.0.0`, CORS and **DNS rebinding against localhost**, reverse proxy + TLS + auth, GPU containers, secrets — scan and close **your own** setup | ~4 h |
| 13 | [`13-GUARDRAILS-RED-TEAMING-AND-EVALUATING-DEFENCES.md`](13-GUARDRAILS-RED-TEAMING-AND-EVALUATING-DEFENCES.md) | ⭐⭐⭐⭐⭐ | guards measured as classifiers, **why static tests overstate defences** (adaptive attacks), garak / PyRIT / promptfoo against the lab, a regression gate in CI | ~6 h |
| 14 | [`14-DETECTION-MONITORING-AND-INCIDENT-RESPONSE.md`](14-DETECTION-MONITORING-AND-INCIDENT-RESPONSE.md) | ⭐⭐⭐⭐ | what to log and never log, canary tripwires on every way out, a lockdown that works without the model, **an incident runbook** ending in counterfactual replay | ~5 h |
| 15 | [`15-CAPSTONE.md`](15-CAPSTONE.md) | ⭐⭐⭐⭐⭐ | every defence in one stack, the whole suite against baseline and hardened, **the cost on normal requests**, the red-team report, the review before other people use your app | ~8 h |
| — | [`SOURCES.md`](SOURCES.md) | — | the annotated bibliography: **what came from where and went into which part** | — |
| — | [`lab/`](lab/) | — | the lab code (part 02); later parts tell you which files to add | — |

**Total: ~77 hours at the keyboard**, plus model time for the experiments.

---

## The anatomy of every part

```
0. The problem — why this matters, in plain words
1-N. Theory from the high level down to the mechanism
   "In the real world" — dated incidents and research, with links
   Defences — what works, what does not, and why
LAB — code you add to the lab (defences, attack cases, tools)
⭐ EXPERIMENT — hypothesis, procedure, a prediction, an empty table for YOUR result
EXERCISES
Traps of this part — symptom → remedy
Checkpoint — what must be true before the next part
```

⭐ **The scoreboard is the thread through the course.** Every part adds attack cases (`lab/cases/partNN.jsonl`)
and defence configurations (`pNN-…`). By part 15 you have one table: every attack × every defence, on **your**
model, with confidence intervals. When your numbers disagree with the predictions in the text, **your measurement
wins.**

---

## The rules of the lab

1. **Everything listens on 127.0.0.1.** The chat UI refuses foreign `Host`/`Origin` headers; `fetch_url` can only
   reach the lab's own fixture site and attacker server.
2. **Canaries, not secrets.** The lab generates random `CANARY-…` strings; an attack "succeeds" when a canary
   reaches somewhere it should not. Never put real credentials into the lab.
3. **Your own systems only.** The scanning and probing scripts in part 12 refuse public addresses. Scan only
   machines you own.
4. **Defences are measured, not believed.** Run k ≥ 5 repetitions, read the interval, keep the numbers.

---

## How this course relates to the other two

| Topic | Course 1 | Course 2 | Course 3 |
| :-- | :-- | :-- | :-- |
| Sandbox, limits, network | part 07 (bwrap, systemd-run) | part 10 (isolation ladder) | parts 09, 12 use them |
| Prompt injection | part 07 §6 (intro) | part 16 (ASI01) | parts 03, 05, 06, 07 (in depth) |
| OWASP for agents | — | part 16 (ASI01–ASI10) | part 01 (map), parts 06–09, 14 |
| Evaluation | part 03 (harness) | part 14 (golden set) | parts 02, 13 (ASR, CI gate) |
| Observability | part 07 §7–8 | part 15 (OTel) | part 14 (detection, response) |
