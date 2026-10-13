# Technical patterns of assistants — what the best ones teach

**As of 11 October 2026.** The profiles in [01-PROFILES.md](01-PROFILES.md) say *what* the fifteen best assistants
do. This file extracts what can be carried over: twenty technical patterns — who does it, why
it works and how to do it yourself. Then an honest offline table, a reference architecture of a local assistant for
Polish professionals, and a chapter on evaluation and security.

What I do **not** repeat here: specific tools (search engines, sandboxes, voice, image) are in the
[building blocks of the harness overview](../agent-harnesses/02-BUILDING-BLOCKS.md), and the "Opus plans, local agents execute" pattern
on my hardware (4× R9700, DeepSeek-V4-Flash, 4 slots of 131k, ~13.6 tok/s per agent) in
[03-ARCHITECTURE.md](../agent-harnesses/03-ARCHITECTURE.md). Law and hardware prices:
[04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md). Sources: [SOURCES.md](SOURCES.md).

---

## Table of contents

1. [Anatomy of an assistant](#1-anatomy-of-an-assistant)
2. [Patterns](#2-patterns)
   - [2.1. Context engineering for the prompt cache](#21-context-engineering-for-the-prompt-cache)
   - [2.2. Plan file and goal recitation](#22-plan-file-and-goal-recitation)
   - [2.3. Planner, critic and origin sets](#23-planner-critic-and-origin-sets)
   - [2.4. Computer use: DOM first, then image](#24-computer-use-dom-first-then-image)
   - [2.5. Hands local, brain elsewhere](#25-hands-local-brain-elsewhere)
   - [2.6. A sandbox or VM per task](#26-a-sandbox-or-vm-per-task)
   - [2.7. Credential broker](#27-credential-broker)
   - [2.8. Approvals scaled by impact on the world](#28-approvals-scaled-by-impact-on-the-world)
   - [2.9. Skills and recipes](#29-skills-and-recipes)
   - [2.10. Bounded memory and memory in files](#210-bounded-memory-and-memory-in-files)
   - [2.11. Heartbeat, cron and the script gate](#211-heartbeat-cron-and-the-script-gate)
   - [2.12. The messenger as the interface](#212-the-messenger-as-the-interface)
   - [2.13. Voice](#213-voice)
   - [2.14. Linked evidence and citations](#214-linked-evidence-and-citations)
   - [2.15. Tabular review](#215-tabular-review)
   - [2.16. Procedures in natural language](#216-procedures-in-natural-language)
   - [2.17. Simulation and repeatability](#217-simulation-and-repeatability)
   - [2.18. Your own model from open weights](#218-your-own-model-from-open-weights)
   - [2.19. Router and model hybrid](#219-router-and-model-hybrid)
   - [2.20. Meeting notes without a bot](#220-meeting-notes-without-a-bot)
3. [Offline: what really works without the internet](#3-offline-what-really-works-without-the-internet)
4. [Reference architecture of a local assistant for the desk](#4-reference-architecture-of-a-local-assistant-for-the-desk)
5. [Evaluation and security](#5-evaluation-and-security)

---

## 1. Anatomy of an assistant

Every product in the ranking — from OpenClaw to Harvey — consists of the same eight layers. They differ in **which
layer is their advantage**: Harvey wins on content and evaluation, Manus on context and the virtual machine, OpenClaw
on channels and the heartbeat, Abridge on linked evidence.

```text
1. CHANNELS      chat / PWA · messenger · e-mail · voice · Word plugin
        |
2. ORCHESTRATOR  agent loop · plan (todo.md) · sessions · heartbeat and cron · procedures (AOP) · subagents
        |
        +--> 3. MODELS + ROUTER   large model · small fast one · critic · STT / TTS · vision
        |                         router rule: data sensitivity first, then difficulty
        +--> 4. TOOLS             files · RAG with citations · MCP · browser (DOM) · computer use
        |
5. MEMORY        USER.md / MEMORY.md (bounded) · case memory · index
6. EXECUTION     sandbox / VM per task · separate user · egress closed · credential broker
7. OVERSIGHT     approvals by impact · critic · origin sets · human takeover
8. EVALUATION    event log · golden sets · pass^k · traces
```

Two observations that steer the rest of the file:

- **The model is the least unique layer.** Manus bets on "context engineering on frontier models" instead of
  its own models ([Manus, 18 July 2025](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)),
  Harvey keeps several providers at once ([Harvey, 10 March 2026](https://www.harvey.ai/en-US/blog/why-harvey-is-multi-model-by-design)).
  **The advantage sits in layers 2, 4 and 6–8** — and exactly those can be built locally.
- **Layers 6–8 are now a separate product.** Google described six oversight mechanisms for the agent in Chrome
  ([Google, 8 December 2025](https://blog.google/security/architecting-security-for-agentic/)), Microsoft is adding to OpenClaw
  a company policy compliance check ([OpenClaw, 25 September 2026](https://openclaw.ai/blog/microsoft-autopilot-openclaw)).
  For a Polish professional these layers are a selling point, not a cost.

Course: [course 2, part 1](../course_agentic_apps/01-AGENT-ARCHITECTURES.md).

---

## 2. Patterns

Each pattern: **what it is**, **who** (with a link to the profile), **why it works**, **your setup** — how to do it locally.

### 2.1. Context engineering for the prompt cache

**What it is.** You design the context so that successive turns hit the prefix cache (KV cache). Manus's six
rules: a stable prefix (no timestamps down to the second); append-only context, with deterministic
serialization; **masking tools instead of removing them** (consistent prefixes `browser_`, `shell_`); the file system as
memory with "reversible compression" (you drop the page content, keep the URL); goal recitation in `todo.md`; errors stay
in the context; no repetitive examples ([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).

**Who.** [Manus](01-PROFILES.md#6-manus) calls cache hits "the most important metric of a production agent"; the input-to-output
ratio ~100:1, a typical task ~50 tool calls *(company data, 2025)*. [Hermes Agent](01-PROFILES.md#5-hermes-agent)
injects memory as a "frozen snapshot" at session start so as not to break the cache
([docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)). OpenHands, once a threshold is exceeded,
summarizes old events, keeping the goal, progress and task list — the cost of a turn dropped below half, with 54% versus 53%
of tasks solved *(project data)* ([OpenHands](https://openhands.dev/blog/openhands-context-condensensation-for-more-efficient-ai-agents)).

**Why it works.** An agent reads far more than it writes. In the cloud a cache read is ~10× cheaper; locally the difference
is in **time**: my rig reads a prompt at ~1,186 tok/s, so 50k tokens without cache is ~40 s to the first token
([03-ARCHITECTURE](../agent-harnesses/03-ARCHITECTURE.md#1-resources-what-you-really-have)).

**Your setup.** The date and variable data in the user message, not in the system prompt. A fixed tool list for the whole
session — you "disable" with a grammar or validation. The same session to the same llama-server slot (Manus routes by
session ID). Large observations to a file, only the path and a summary into the context. Course:
[course 2, part 4](../course_agentic_apps/04-CONTEXT-ENGINEERING.md),
[course 1, part 8](../course_local_models/08-OPTIMIZATION-OFFLINE.md); pitfall H4 in
[the harnesses](../agent-harnesses/01-PROFILES.md#seven-pitfalls-common-to-all).

### 2.2. Plan file and goal recitation

**What it is.** The agent keeps a plan file and rewrites it every few steps; for risky tasks a human
approves the plan **before** execution.

**Who.** [Manus](01-PROFILES.md#6-manus) rewrites `todo.md` because at ~50 steps the model loses the goal in the middle of the context.
[ChatGPT](01-PROFILES.md#7-chatgpt) Work (9 July 2026) has "Plan mode": it asks follow-up questions, shows a step-by-step plan, and the approved
plan becomes the boundary of the user's consent ([digitalapplied](https://www.digitalapplied.com/blog/chatgpt-work-openai-agent-launch-2026)).

**Why it works.** Recitation moves the goal to the end of the context, where the model pays the most attention; one approved
plan replaces dozens of "may I?" questions.

**Your setup.** `work/<task>/plan.md`: goal, a "done" criterion, steps with status, open questions. The orchestrator
forces a rewrite every N steps and before every action that writes. In the UI the plan is a checklist — and documentation for
the client.

### 2.3. Planner, critic and origin sets

**What it is.** Three Google mechanisms for the agent in Chrome ([Google](https://blog.google/security/architecting-security-for-agentic/)):
a **goal-alignment critic** — a separate model assesses every action and can veto it, and it sees only the action and the goal,
**not the page content**; **origin sets** (Agent Origin Sets) — domains per task, separately "read-only" and "read
and write"; **deterministic confirmations** before bank and medical pages, signing in through a password manager,
payment and sending a message. In addition an injection classifier in parallel with the planner and a work log with takeover.

**Who.** [Gemini](01-PROFILES.md#8-gemini). In the API every step returns a `safety_decision`, and 7 policy categories
(transactions, sensitive data, communication, contracts…) force a confirmation ([docs](https://ai.google.dev/gemini-api/docs/computer-use)).

**Why it works.** The critic is cheap, and cutting it off from the page content closes the main attack channel. Origin sets
limit the damage even after the agent is hijacked.

**Your setup.** The critic is a small model on the CPU (for me `gpt-oss-20b-cpu`): input `{goal, action, domain, action_class}`,
output `{approval, reason}`. Origin sets in the task configuration ("ISAP and SAOS — read; court portal — write after
approval"). Confirmation triggers in code, not in the model.

### 2.4. Computer use: DOM first, then image

**What it is.** The agent sees the page as text — an accessibility tree or a list of elements with identifiers — and a screenshot
is the fallback.

**Who.** [browser-use](01-PROFILES.md#13-browser-use): "text first" is the founding idea, since 8.2025 100% on Chrome
DevTools Protocol ([ain.ua](https://en.ain.ua/2025/03/25/browser-use-raises-17m),
[changelog](https://browser-use.com/changelog/19-8-2025)). [Claude](01-PROFILES.md#2-claude): `browser_toolset` reads the
accessibility tree and uses element references that are robust to layout shifts; a full screenshot is 1,000–1,800
input tokens ([browser use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool),
[computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)). The vision side:
[UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) (Apache-2.0) with a single vision model and a GUI + DOM hybrid;
Agent S3 separates the "where to click" model (UI-TARS-1.5-7B) from the reasoning model and, picking the best of several
runs, reaches 72.6% on OSWorld versus 72.36% for a human ([Agent S](https://github.com/simular-ai/Agent-S)).

**Why it works.** The DOM is cheaper, more stable and suits small models without vision; an image is needed only
for pixel-based interfaces.

**Your setup.** DeepSeek-V4-Flash is text-only, so the DOM is the natural path: Playwright MCP, agent-browser or
browser-use with a local endpoint ([building blocks](../agent-harnesses/02-BUILDING-BLOCKS.md#browser-agents)); vision via
a "bridge" — a separate model describes the screen ([03-ARCHITECTURE, U5](../agent-harnesses/03-ARCHITECTURE.md#u5--photos-and-images)).
**Beware of vendor numbers:** browser-use announced 89.1% on WebVoyager after removing 55 of 586 tasks, and on the independent
Online-Mind2Web leaderboard that stack with Claude Sonnet 4 scored 40.0% ([report](https://browser-use.com/posts/sota-technical-report),
[HAL](https://hal.cs.princeton.edu/online_mind2web)).

### 2.5. Hands local, brain elsewhere

**What it is.** Execution (browser, files, VM) runs on the user's machine, and only observations go to the model.

**Who.** [Perplexity](01-PROFILES.md#15-perplexity) Comet according to the *Amazon v. Perplexity* case file: the user's browser
talks to the page, takes screenshots locally and sends them to Perplexity's servers for instructions
([Jones Day](https://www.jonesday.com/en/insights/2026/09/ninth-circuit-vacates-cfaa-injunction-against-perplexitys-comet-ai-agent)).
[Claude](01-PROFILES.md#2-claude): computer use is executed by the developer's application, Cowork runs a local Linux VM through
Apple Virtualization — the model is in the cloud ([Simon Willison](https://simonwillison.net/2026/Jan/12/claude-cowork/)).
[Manus](01-PROFILES.md#6-manus) advises doing banking through a local browser, because data-center addresses trigger
blocks ([docs](https://manus.im/docs/features/cloud-browser.md)).

**Why it works.** Logins and cookies stay with the user; there is no "bot from a server room" problem.

**Your setup.** A ready-made template — **just swap the brain for a local one**. For client data both halves stay on
the desk; the cloud can be the "brain" only for content without client data (section 4). The planner pattern:
[03-ARCHITECTURE, section 2](../agent-harnesses/03-ARCHITECTURE.md#2-pattern-planner-and-executors).

### 2.6. A sandbox or VM per task

**What it is.** Every task or case gets an isolated environment with access only to the designated folders
and closed outbound traffic.

**Who.** [Manus](01-PROFILES.md#6-manus): Firecracker micro-VMs through E2B, start ~150 ms; Docker dropped out because of a 10–20 s
start ([E2B, 6 May 2025](https://e2b.dev/blog/how-manus-uses-e2b-to-provide-agents-with-virtual-computers)).
[Claude](01-PROFILES.md#2-claude) Cowork mounts only the folders the user allowed and restricts the network. Windows
gives the agent **its own account**, six known folders and a choice of "always / ask / never"
([Microsoft](https://support.microsoft.com/en-us/windows/experimental-agentic-features-a25ede8a-e4c2-4841-85a8-44839191dfb3)).
[NemoClaw](https://github.com/NVIDIA/NemoClaw) wraps OpenClaw in a sandbox **by default**, with outbound traffic accepted
by the operator.

**Why it works.** The damage after the agent is hijacked ends at a single folder. **But:** PromptArmor showed that Cowork
sent the victim's files to the attacker's account through the **allowed** Anthropic API with the attacker's key
([PromptArmor](https://www.promptarmor.com/resources/claude-cowork-exfiltrates-files)) — an allowlist of hosts is not
enough when the allowed host accepts arbitrary credentials.

**Your setup.** A sandbox per case: srt or bubblewrap for the shell, microsandbox for agent code
([building blocks](../agent-harnesses/02-BUILDING-BLOCKS.md#sandboxes)); a separate system user; egress closed by default,
and if needed — a domain list through a proxy that lets through only your credentials. Course:
[course 1, part 7](../course_local_models/07-SANDBOX-SECURITY-MONITORING.md),
[course 2, part 10](../course_agentic_apps/10-PRODUCTION-SANDBOX.md).

### 2.7. Credential broker

**What it is.** Passwords and tokens never reach the prompt or the sandbox. The agent gets a handle, and the substitution
is done by a trusted process out of the model's reach — only for the allowed domain.

**Who.** Kortix: credentials "are brokered server-side through a single narrowly scoped token and never
enter the machine" ([README](https://raw.githubusercontent.com/kortix-ai/suna/main/README.md)). Claude Code in cloud
VMs: GitHub credentials do not enter the VM, traffic leaves through a proxy ([docs](https://code.claude.com/docs/en/data-usage)).
[browser-use](01-PROFILES.md#13-browser-use): "secret bindings" pinned to `allowedDomains`
([docs](https://docs.browser-use.com/cloud/choosing-an-agent)). Login and 2FA are handed to a human — Manus
"Take Over", Gemini Spark hands over login and payments ([Google](https://support.google.com/gemini/answer/16596215)).
Microsoft added to OpenClaw secret masking in approval prompts
([OpenClaw](https://openclaw.ai/blog/microsoft-autopilot-openclaw)).

**Why it works.** A model that does not know the password will not leak it — neither through injection nor into a log.

**Your setup.** A vault (an encrypted file or keyring) + a tool proxy: the agent writes `{{secret:ksef}}`, the proxy substitutes
the value only in a request to that secret's domain and strips it from responses and logs. Trusted Profile (Profil Zaufany), court portals,
banking — the login is always done by a human in a taken-over session.

### 2.8. Approvals scaled by impact on the world

**What it is.** Whether the agent asks is decided by the **action's external impact** and its reversibility, not by the model's confidence.

**Who.** Lindy: "everything that has external impact waits for approval… read-only searches do not require
approval" ([Lindy](https://www.lindy.ai/pricing)). [browser-use](01-PROFILES.md#13-browser-use) "Agency" asks only
before sending or publishing ([changelog, 17 August 2026](https://browser-use.com/changelog/3-4-2026)).
[Claude](01-PROFILES.md#2-claude) in Chrome confirms publishing, purchase and sharing of personal data
([Anthropic](https://claude.com/blog/claude-for-chrome)). OpenHands has a `ConfirmRisky` mode, the model flags an action's risk,
and a pattern analyzer catches `rm -rf` and `curl | sh` ([docs](https://docs.openhands.dev/sdk/guides/security)). ZeroClaw has
autonomy levels and approvals signed with HMAC ([harnesses](../agent-harnesses/01-PROFILES.md#10-zeroclaw)). Microsoft
in Autopilot: an action with an **unknown outcome** is not retried automatically ([OpenClaw](https://openclaw.ai/blog/microsoft-autopilot-openclaw)).

**Why it works.** No questions about reads, and every irreversible action has a human.

**Your setup.**

| Action class | Example | Decision |
|---|---|---|
| Local read | searching the case file, OCR of a scan | automatic |
| Draft | a draft of a letter, a draft e-mail in the "Drafts" folder | automatic, stays a draft |
| Write in the sandbox | a new file in the case directory | automatic, with a restore point |
| External impact | sending an e-mail, filing a letter, a payment, deletion | always a human |
| Unknown outcome | an interrupted send, a portal timeout | stop, no retry, ask a human |

### 2.9. Skills and recipes

**What it is.** A repeatable procedure as a folder with a Markdown file (instructions, examples, scripts), loaded only
when needed.

**Who.** [OpenClaw](01-PROFILES.md#1-openclaw): `SKILL.md` and the ClawHub registry. [Hermes Agent](01-PROFILES.md#5-hermes-agent)
writes skills itself after complex tasks, improves them and scans them on installation
([docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)). Poke has "recipes" — automations in plain
text that users share ([TechCrunch, 8 April 2026](https://techcrunch.com/2026/04/08/poke-makes-ai-agents-as-easy-as-sending-a-text/)).
LexisNexis has skills of its own and its partners' in Protégé, and announces customers' own "soon" (24 August 2026,
[LexisNexis](https://www.lexisnexis.com/community/pressroom/b/news/posts/lexis-with-protege-accelerates-frictionless-agentic-productivity-from-first-idea-to-review-ready-legal-work-product)).

**Why it works.** The system prompt stays short (cache), and procedural knowledge is versioned. **The dark side:**
an open skill marketplace is a new attack surface (section 5).

**Your setup.** A `skills/` directory in git, one per procedure of the profession ("lease agreement review",
"closing the VAT month", "visit note — cardiology"). A skill written by the agent goes to review, not into use.
No public marketplace — Moltis gives it up deliberately ([harnesses](../agent-harnesses/01-PROFILES.md#15-moltis)).

### 2.10. Bounded memory and memory in files

**What it is.** Memory is readable files with a hard limit, which the owner can open, correct and revert.

**Who.** [Hermes Agent](01-PROFILES.md#5-hermes-agent): `MEMORY.md` ≤ 2,200 characters, `USER.md` ≤ 1,375 characters; full memory
forces consolidation instead of silently dropping entries ([docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)).
[OpenClaw](01-PROFILES.md#1-openclaw) injects `SOUL.md`, `USER.md`, `MEMORY.md`, `AGENTS.md` into every session and "dreams" in the background:
it writes `DREAMS.md` and promotes to `MEMORY.md` only strong entries with a weight of 1–10 ([docs](https://docs.openclaw.ai/concepts/dreaming)).
[Claude](01-PROFILES.md#2-claude) keeps memory as topic files and by default does not save sensitive topics
([Anthropic, 25 August 2026](https://claude.com/resources/articles/claudes-memory-works-everywhere-and-you-decide-whats-in-it)).
[Harvey](01-PROFILES.md#4-harvey) II (18 August 2026) confines work to a case's "Spaces" ([Harvey](https://www.harvey.ai/blog/introducing-harvey-ii)).

**Why it works.** The limit forces curation, a fixed snapshot does not break the cache, and a file can be shown to a client or
an inspector.

**Your setup.** A global `USER.md` (style, preferences — **no client data**) and `cases/<case-number>/memory.md` loaded
only in that case's session. A fill indicator in the UI ("67% — 1,474/2,200"). Everything in git, so "how does the agent know this?"
has an answer in the history. Course: [course 2, part 5](../course_agentic_apps/05-LONG-TERM-MEMORY.md) and
[part 6](../course_agentic_apps/06-IDENTITY-WORKING-FILES.md).

### 2.11. Heartbeat, cron and the script gate

**What it is.** The agent wakes up by itself — on a schedule or an event — but **a cheap script first checks whether there is
anything to do**, and only then is the model called.

**Who.** [OpenClaw](01-PROFILES.md#1-openclaw): heartbeat every 30 min by default, wake-ups at least 30 s apart and a lockout
after 5 starts in 60 s ([heartbeat](https://docs.openclaw.ai/gateway/heartbeat)); "standing orders" describe scope,
trigger, approval gate and escalation ([docs](https://docs.openclaw.ai/automation/standing-orders)). NanoClaw has
"script gates" that do not wake the model when there is no work ([README](https://github.com/nanocoai/nanoclaw)); Moltis can
serve the heartbeat with a separate small model ([harnesses](../agent-harnesses/01-PROFILES.md#15-moltis)). ChatGPT Pulse computes
the morning brief overnight ([TechCrunch](https://techcrunch.com/2025/09/25/openai-launches-chatgpt-pulse-to-proactively-write-you-morning-briefs/)),
Google CC sends a daily e-mail you reply to ([Google](https://blog.google/technology/google-labs/cc-ai-agent/)).

**Why it works.** Most wake-ups are "nothing new" — a script answers that for free.

**Your setup.** A systemd timer → a script (a new file in the case? a new message in the office mailbox? a new entry in the local
mirror of the Dziennik Ustaw (Journal of Laws)?) → a queue → the model. At night the GPU is idle — that is where briefs, tabular review and evaluations go. Course:
[course 2, part 11](../course_agentic_apps/11-SCHEDULING-PROACTIVITY.md);
[building blocks](../agent-harnesses/02-BUILDING-BLOCKS.md#scheduling-and-durable-execution).

### 2.12. The messenger as the interface

**What it is.** The assistant lives in an app the user uses anyway.

**Who.** [OpenClaw](01-PROFILES.md#1-openclaw): one gateway for WhatsApp, Telegram, Signal, iMessage, Teams, Matrix,
e-mail and others ([docs](https://docs.openclaw.ai/llms.txt)). Poke: the first AI agent approved on Apple Messages
for Business (4 June 2026), "over 100 million messages in 3 months" *(company data)*
([TechCrunch](https://techcrunch.com/2026/06/04/apple-approves-poke-as-the-first-ai-agent-on-its-messages-for-business-platform/),
[Cognition, 23 July 2026](https://cognition.com/blog/interaction)). **The other side:** Apple permanently blocked Lindy's
Apple ID account within half a day; the company rewrote the channel three times and keeps the ratio of sent to received below ~10:1
([Lindy, 16 March 2026](https://www.lindy.ai/blog/imessage-api-three-rewrites-one-apple-ban-and-what-actually-works)).

**Why it works.** Zero deployment on the user's side and natural proactivity — the agent writes first.

**Your setup.** Consumer messengers are someone else's cloud and a hostile platform — **you do not send client data there**
(the same goes for Telegram in the [building blocks](../agent-harnesses/02-BUILDING-BLOCKS.md#notifications-and-channels)). A professional's
channel is a web app on the office network, e-mail through the law firm's server (the "cc the assistant" pattern),
a Word plugin — that is where Spellbook and Noxtua live ([Spellbook](https://www.spellbook.com/press), [Noxtua](https://www.noxtua.com/))
— and Matrix on your own server. My personal assistant may use Telegram for non-sensitive matters. Course:
[course 2, part 12](../course_agentic_apps/12-CHANNELS-INTERFACES.md).

### 2.13. Voice

**What it is.** Speech as input (dictation, a voice note, a recording of a visit) and output (reading aloud, conversation).

**Who.** [Hermes Agent](01-PROFILES.md#5-hermes-agent): voice notes with local faster-whisper, but **speech synthesis
by default through the cloud Edge TTS**; Moltis: local STT and Piper with Polish voices, fully offline
([harnesses: Hermes](../agent-harnesses/01-PROFILES.md#4-hermes-agent), [Moltis](../agent-harnesses/01-PROFILES.md#15-moltis)).
[Abridge](01-PROFILES.md#3-abridge) and Nabla have their own medical ASR; Nabla trained on a Whisper base plus 7,000 hours
of medical recordings and **never pastes a raw transcript into the documentation**
([Nabla](https://nabla.com/blog/assessing-the-reliability-of-nablas-speech-to-text-engine)).

**Why it works.** A doctor and an advocate speak faster than they write; a recording is the richest source of facts.

**Your setup.** An STT → LLM → TTS cascade — I did not find local speech-to-speech in Polish on AMD in October 2026
([03-ARCHITECTURE, U4](../agent-harnesses/03-ARCHITECTURE.md#u4--voice-conversation-in-polish),
[building blocks](../agent-harnesses/02-BUILDING-BLOCKS.md#voice)). The transcript is an intermediate product: the LLM writes the note, every sentence
points to a fragment of the recording (2.14). Build a test of Polish drug names and legal terms before you sell this to anyone.

### 2.14. Linked evidence and citations

**What it is.** Every sentence of the output has a clickable pointer to the source: a transcript fragment, a document page, a provision.

**Who.** [Abridge](01-PROFILES.md#3-abridge) "Linked Evidence": every sentence of the note leads to the transcript or the recording;
a guard model corrects claims with no coverage and in an internal test on 10,000+ visits caught 97% of such claims
versus 82% for GPT-4o *(company data, 19 August 2025)* ([Abridge](https://www.abridge.com/ai/science-confabulation-hallucination-elimination)).
[OpenEvidence](01-PROFILES.md#12-openevidence): RAG over licensed literature (NEJM, JAMA, NCCN, Cochrane) with in-text citations
([Wikipedia](https://en.wikipedia.org/wiki/OpenEvidence)). Hebbia: "you can see where every number came from"
([Hebbia](https://www.hebbia.com/blog/introducing-matrix-2-0)). In Poland LEX Expert AI (19 November 2025) links answers
to sources and fragments in LEX — a bar Polish lawyers already know
([Prawo.pl](https://www.prawo.pl/prawnicy-sady/lex-expert-ai-nowym-narzedziem-dla-prawnikow)).

**Why it works.** Verifying a sentence takes seconds. For an advocate it is a condition: § 23e of the Zbiór Zasad Etyki Adwokackiej (Code of Ethics for Advocates, ZZEA)
requires personal verification of the output ([NRA, 12–13 June 2026](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/); NRA — Naczelna Rada Adwokacka, the National Council of the Bar).

**Your setup.** Every RAG fragment has an identifier `{document, page, offset}`; the model returns sentences with a list of
identifiers, and the code rejects a sentence without a citation. A second pass: a verifier gets **only** the sentence and the cited
fragment and answers "covered / not covered". "I don't know" is allowed and rewarded in evaluation. Course:
[course 1, part 4](../course_local_models/04-MEMORY-RAG-AND-CONTEXT.md).

### 2.15. Tabular review

**What it is.** An "N questions × M documents" grid: a row is a document, a column a question, a cell an answer with a citation.
The chat turns into a batch analyst.

**Who.** Hebbia Matrix invented this interface; Matrix 2.0 (26 August 2026) carries the analysis through to finished memos and presentations
with human checkpoints ([Hebbia](https://www.hebbia.com/blog/introducing-matrix-2-0)). Legora copied it,
Thomson Reuters (Tabular Analysis up to 10,000 documents × 100 questions — [CoCounsel](https://legal.thomsonreuters.com/en/products/cocounsel-legal))
and [Noxtua](01-PROFILES.md#14-noxtua) (Matrix Analysis). [Harvey](01-PROFILES.md#4-harvey) counts cost "per cell":
its own Tenet has ~1/10 of the cell cost in Review Table *(company data)* ([Harvey, 20 August 2026](https://www.harvey.ai/blog/post-training-update-harvey-tenet)).

**Why it works.** Every cell is a small, independent, easy-to-check task — ideal for a local model
and parallel slots — and the result is a spreadsheet the professional uses anyway.

**Your setup.** A queue of cells limited to 4 slots, ordered "document by document": in one slot the document as a
fixed prefix and the following questions, so the cache reads it once. A cell = JSON `{answer, quote, page, confidence}`
validated in code, export to XLSX with links to PDF pages. I have **not measured** throughput on my rig — a good
first measurement.

### 2.16. Procedures in natural language

**What it is.** The agent's behavior is described by an expert in plain language, and a separate specification, hidden from the agent,
assesses the **run**, not just the outcome.

**Who.** Decagon: "Agent Operating Procedures" — procedures in natural language that the support team changes "without
engineering sprints" ([Decagon](https://decagon.ai/blog/series-d-announcement)). Basis: "behavior specs"
(29 July 2026), an open standard with Braintrust — the specs assess the trajectory (true / false / not applicable) and
"are never shown to the agent", because "a correct outcome does not tell you whether the agent used a process we would trust
again" ([Basis](https://www.getbasis.ai/blogs/behavior-specs-an-open-standard-for-supervising-long-horizon-agents)).

**Why it works.** Control over behavior belongs to the lawyer or the accountant, not the programmer; a run specification catches
"a good result by accident".

**Your setup.** `procedures/payment-demand.md` in Polish, written by the professional ("when a client sends
a payment demand, first calculate the deadline…"), and next to it `evals/payment-demand.spec.md` with questions about the run ("did it check
the VAT white list", "did it cite the KIS interpretation") — the agent does not see this file.

### 2.17. Simulation and repeatability

**What it is.** Before the agent gets clients, it talks to simulated ones, and the measure is **pass^k** — whether it succeeded k times
in a row on the same task.

**Who.** [Sierra](01-PROFILES.md#11-sierra): τ-bench (20 June 2024) simulates users and APIs under domain rules; GPT-4o
fell in retail to ~25% at pass^8, 60% down from pass^1 ([Sierra](https://sierra.ai/blog/benchmarking-ai-agents)).

**Why it works.** A professional needs predictability more than peak quality. DeepSeek-V4-Flash on
my hard set scores 92/93, but repeatability only 83 ([03-ARCHITECTURE](../agent-harnesses/03-ARCHITECTURE.md#fully-local-mode)).

**Your setup.** A client simulator on a local model with personas per profession, run at night: k = 8 runs per
task, a pass^1 and pass^8 report. Locally, night-time compute is almost free.

### 2.18. Your own model from open weights

**What it is.** An open base model fine-tuned (pretraining, SFT, RL) on domain data and task traces instead of
a frontier model at every cell.

**Who.** [Harvey](01-PROFILES.md#4-harvey) Tenet (20 August 2026): Kimi K3 after RL (GSPO) with Fireworks, synthetic,
public and expert data — "we did not use customer data"; −90% cost of a firm-knowledge query *(company data)*; weights
not published ([Harvey](https://www.harvey.ai/blog/post-training-update-harvey-tenet)). [Cursor](01-PROFILES.md#9-cursor)
Composer 2 (19 March 2026): open Kimi K2.5 plus its own pretraining and RL; the base was not disclosed at launch, Cursor
admitted it after a user discovered it ([Cursor](https://cursor.com/blog/composer-2),
[Gigazine](https://gigazine.net/gsc_news/en/20260323-cursor-admits-composer-2-kimi)). [Noxtua](01-PROFILES.md#14-noxtua):
the "Athena" tier on open-source models in a sovereign EU infrastructure ([Noxtua](https://www.noxtua.com/)).
Microsoft Fara-7B: a small computer-use model trained on 145k synthetic trajectories of a larger agent
([MSR](https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/)).

**Why it works.** Narrow, measurable tasks (extraction, a table cell) need a fitted model, not the
largest one. Your own weights are also sovereignty.

**Your setup.** First prompts and DSPy with Opus as the teacher
([building blocks](../agent-harnesses/02-BUILDING-BLOCKS.md#tool-call-reliability-and-prompt-tuning)), then fine-tuning
a **smaller** model (Bielik-11B, Qwen 27B) for a single task. You will not fine-tune the 284-billion-parameter DeepSeek on 4× R9700.
Two rules from other people's mistakes: disclose the base model (Cursor) and do not train on client data without consent (Harvey makes
an argument of it).

### 2.19. Router and model hybrid

**What it is.** Code decides which model handles a step — by data sensitivity, difficulty and cost.

**Who.** [Harvey](01-PROFILES.md#4-harvey): routing by task, failover when a provider fails, the administrator chooses
the allowed models ([Harvey](https://www.harvey.ai/en-US/blog/why-harvey-is-multi-model-by-design)). Perplexity Computer:
19 models with subagents ([TechCrunch, 27 February 2026](https://techcrunch.com/2026/02/27/perplexitys-new-computer-is-another-bet-that-users-need-many-ai-models/)).
Glean Tau: USD 0.58 versus USD 2.98 per task compared with Claude Cowork *(vendor benchmark, 27 August 2026)*
([itbrief](https://itbrief.asia/story/glean-launches-tau-to-cut-enterprise-ai-token-costs)). [Noxtua](01-PROFILES.md#14-noxtua):
"Athena" (open, sovereign) or "Minerva" (frontier models in a European setup)
([Noxtua](https://www.noxtua.com/security)).

**Why it works.** Most steps are simple; the expensive model only where it pays off. **The trap:** model choice
can silently move data — in Microsoft 365 Copilot, Anthropic models as a subprocessor are excluded from the EU Data
Boundary ([Microsoft](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy)).

**Your setup.** The router's first rule is **sensitivity**, the second difficulty: "client data → local only" is a hard
rule in code, not a model decision. Gateway and limits: [building blocks](../agent-harnesses/02-BUILDING-BLOCKS.md#gateway-and-model-routing);
course: [course 2, part 17](../course_agentic_apps/17-HYBRID-AND-ROUTER.md),
[course 1, part 10](../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md).

### 2.20. Meeting notes without a bot

**What it is.** The app records the microphone and system audio on the device — no bot joins the call — and an LLM
expands the **user's notes** into a full note.

**Who.** [Granola](01-PROFILES.md#10-granola): two channels give free "Me / Them" diarization, the recording is not saved,
the transcript stays; ASR and LLM in the cloud ([docs](https://docs.granola.ai/help-center/taking-notes/transcription)).
The dark side: in 7.2026 the press described notes shared by link by default and training enabled by default on the
Free and Business plans ([Startup Fortune](https://startupfortune.com/granola-ai-meeting-notes-are-not-as-private-as-you-might-think/)),
and on 30 July 2026 a class action *Chamberlain v. Granola* was filed
([ppc.land](https://ppc.land/granola-sued-for-recording-meetings-without-consent-to-train-ai-models/)).

**Why it works.** The absence of a bot removes social friction, and the user's notes tell the model what mattered.

**Your setup.** The microphone and the system loopback as two paths → whisper.cpp or Parakeet → per-channel diarization → an LLM
merges with the notes and a template → audio deleted after transcription. Check the participants' consent to recording for your
situation — this is not legal advice.

---

## 3. Offline: what really works without the internet

**"Yes"** = the product itself works without the internet (open code + a local model). Cloud services get **"No"**, even
when part of the execution is local. Details in [01-PROFILES.md](01-PROFILES.md).

| Assistant | Code | Offline | What works locally | What is missing / what to replace |
|---|---|---|---|---|
| [OpenClaw](01-PROFILES.md#1-openclaw) | open (MIT) | Partially | loop, memory, heartbeat and cron with a local model; CLI, TUI, local web UI ([docs](https://docs.openclaw.ai/gateway/local-models)) | the WhatsApp / Telegram / Signal channels need a network; local models "do not have the providers' safety filters"; the sandbox is not the default |
| [Claude](01-PROFILES.md#2-claude) | closed | No | computer use / browser use is executed by your machine; the Cowork VM is local; the Claude Code client is local | the model is cloud-only — a local LLM + your own loop with the same "brain / hands" split |
| [Abridge](01-PROFILES.md#3-abridge) | closed | No | only recording on a phone or in the EHR app | whisper.cpp + a local LLM + a verifier + linked evidence (2.13, 2.14) |
| [Harvey](01-PROFILES.md#4-harvey) | closed | No | nothing — SaaS; Tenet without public weights | a local model + RAG with citations + tabular review (2.14, 2.15) |
| [Hermes Agent](01-PROFILES.md#5-hermes-agent) | open (MIT) | Partially | loop with a local endpoint, faster-whisper STT, memory in files, cron | **TTS is Edge TTS (cloud) by default** — replace with Piper; messenger channels need a network |
| [Manus](01-PROFILES.md#6-manus) | closed | No | a local browser as the actuator (Browser Operator) | a VM per task (microsandbox), a local model, context rules (2.1, 2.6) |
| [ChatGPT](01-PROFILES.md#7-chatgpt) | closed | No | nothing in the product (the press reports the opening of the Codex harness itself, 29 September 2026) | everything — loop, VM, browser, model |
| [Gemini](01-PROFILES.md#8-gemini) | closed | No | auto browse works in the user's Chrome, the model in the cloud; Gemini Spark unavailable in the EEA | carry the critic, origin sets and confirmations over to your own loop (2.3) |
| [Cursor](01-PROFILES.md#9-cursor) | closed | No | the editor; execution on "Self-Hosted Machines"; requests always go through Cursor's backend | Cline or [OpenCode](../agent-harnesses/01-PROFILES.md#8-opencode) with a local model |
| [Granola](01-PROFILES.md#10-granola) | closed | No | capturing the microphone and system audio | local STT + per-channel diarization + a local LLM (2.20) |
| [Sierra](01-PROFILES.md#11-sierra) | closed | No | nothing; the method (τ-bench) is open | a client simulator and pass^k on a local model (2.17) |
| [OpenEvidence](01-PROFILES.md#12-openevidence) | closed | No | nothing | local RAG over Polish society guidelines, ChPL (Charakterystyka Produktu Leczniczego, Summary of Product Characteristics) and AOTMiT recommendations |
| [browser-use](01-PROFILES.md#13-browser-use) | open (MIT) | Partially | a library with a local endpoint; intranet pages | the internet requires a network; BU 2.0, "stealth" browsers and V3 / V4 agents are cloud-only; small models break action schemas |
| [Noxtua](01-PROFILES.md#14-noxtua) | closed | No | the Word and Outlook plugins are clients; models in a sovereign EU cloud (DE, CH) | "sovereignty" here means an EU cloud, not the desk — an open model + RAG over ISAP and SAOS |
| [Perplexity](01-PROFILES.md#15-perplexity) | closed | Partially (Portable Computer only; the rest of the product is cloud) | a local 27B model, harness and sandbox on the desk (see the profile); Comet executes actions locally but reasons on servers | requires Nvidia (Apple Silicon and AMD unsupported); I did not verify offline operation; fresh search offline is impossible |

Sources of the rows: the profiles in [01-PROFILES.md](01-PROFILES.md); Codex — [Decrypt](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced);
Gemini Spark outside the EEA — [Google](https://support.google.com/gemini/answer/16596215); Cursor — [data](https://cursor.com/data-use);
browser-use — [BU 2.0](https://docs.browser-use.com/open-source/bu-2-0-model-card) and [building blocks](../agent-harnesses/02-BUILDING-BLOCKS.md#browser-agents).

**Conclusion:** of the fifteen, no product works fully offline. Four can be run partially locally: OpenClaw, Hermes and browser-use (open, with a local model; channels, Edge TTS and public pages require a network) and Perplexity Portable Computer (closed). These are not products for professionals. **Nobody at the top sells a Polish lawyer or doctor
an assistant that works on the desk** — section 4 fills that gap.

### Function → local replacement

| Function | Local replacement (open) | What is weak offline |
|---|---|---|
| LLM | my rig: DeepSeek-V4-Flash (text only); for the desk: Qwen3.6-27B, Gemma-4-31B, gpt-oss-120b; Bielik-11B-v3 for Polish style | the best open model on PLCC: 89.83 versus 92–97 for closed ones (8 October 2026); swapping Opus for a small model cost 25–39 pp in OpenJarvis |
| Embeddings and RAG | llama-swap serves embeddings; SQLite + BM25 + reranking ([course 1, part 4](../course_local_models/04-MEMORY-RAG-AND-CONTEXT.md)); FTS5 as in Hermes; Cognee without a cloud key | the best provision retrieval on bar-exam questions: 72.3% top-1 (BM25: 61.7%) |
| STT | whisper.cpp large-v3 (WER 4.74% FLEURS-pl), Parakeet-TDT-0.6B-v3 on CPU (7.31%), faster-whisper | Polish medical vocabulary and a microphone in the consulting room — unverified |
| TTS | Piper pl_PL (CPU, robotic), Chatterbox Multilingual V3 (MIT, watermark), VoxCPM2 | the quality of Polish TTS; Kokoro is EN only; no local speech-to-speech in Polish on AMD |
| OCR and vision | Docling + PaddleOCR-VL-1.5 (low VRAM, runs on CPU); Qwen3.6-35B-A3B; a test of DeepSeek-V4-Flash-Vision-Exp | DeepSeek-V4-Flash cannot see images; vision models make poor use of the image in Polish medical questions |
| Web search | SearXNG (needs the internet); offline: local mirrors of ISAP / ELI, SAOS, ChPL and guidelines, synchronized by a separate process | fresh knowledge from the web is impossible; a mirror has a date |
| Calendar and e-mail | IMAP / SMTP to the office server, CalDAV (e.g. Nextcloud on-prem), drafts directly in the mailbox, "cc the assistant" | sending by definition needs a network; cloud calendars drop out |
| Computer use | DOM: browser-use, Playwright MCP (no vision), agent-browser; GUI: UI-TARS-desktop + UI-TARS-1.5-7B, Holo4-35B-A3B, Fara-7B | on OSWorld 2.0 (6.2026) the best frontier model completed 20.6%; a 7B model has ~27.5% on OSWorld |
| Channels | a web app / PWA on the office network, Matrix on your own server, Gotify, self-hosted ntfy | WhatsApp, iMessage, Telegram are someone else's cloud; push on iOS requires the ntfy.sh relay |
| Moderation and injection | Bielik-Guard 0.5B (a Polish harm classifier), BrowseSafe (open weights) | BrowseSafe lets ~10% of attacks through (12.2025); Bielik-Guard: precision 75.28% |

Sources: [building blocks](../agent-harnesses/02-BUILDING-BLOCKS.md) (voice, image, search, channels, memory); OpenJarvis —
[03-ARCHITECTURE](../agent-harnesses/03-ARCHITECTURE.md#3-what-is-proven-and-what-is-not); [PLCC](https://huggingface.co/spaces/sdadas/plcc);
provisions — [arXiv 2608.30929](https://arxiv.org/abs/2608.30929); Polish medical vision — [arXiv 2608.12928](https://arxiv.org/abs/2608.12928);
OSWorld 2.0 — [arXiv 2606.29537](https://arxiv.org/abs/2606.29537); [UI-TARS-1.5-7B](https://huggingface.co/ByteDance-Seed/UI-TARS-1.5-7B);
[Bielik-Guard](https://huggingface.co/speakleash/Bielik-Guard-0.5B-v1.1);
BrowseSafe — [the-decoder](https://the-decoder.com/perplexitys-browsesafe-tries-to-patch-the-gaping-security-holes-inherent-in-ai-browser-agents/).

---

## 4. Reference architecture of a local assistant for the desk

The goal: an assistant for a law firm, a medical practice or an accounting office in which **client data does not leave the desk**. This is
a design assembled from the patterns of section 2 — **unmeasured** until you build it.

```text
OFFICE (local network)                                               | INTERNET
  PWA in the browser · Word plugin · office e-mail · recording       |
                          |                                          |
  +------------- BOX ON THE DESK (encrypted disk) ----------------+  |
  | ORCHESTRATOR   loop · plan.md · procedures · heartbeat + gates|  |
  |   router: client data -> local only                           |  |
  | MODELS (llama-swap)        TOOLS (MCP, read-only)             |  |
  |   main LLM · Bielik          case RAG with citations          |  |
  |   critic (small model)       tabular review -> XLSX           |  |
  |   STT · TTS · OCR            letter drafts · DOM browser      |  |
  | MEMORY     USER.md · cases/<case-number>/ · index · mirrors   |  |
  | EXECUTION  sandbox per case · separate user                   |  |
  | OVERSIGHT  approvals by impact · credential broker            |  |
  | LOG        append-only events · tools note                    |  |
  +---------------------------+-----------------------------------+  |
          egress firewall: default NO                                |
              +-- signed updates ------------------------------------+--> update server
              +-- ISAP / SAOS mirrors (separate process, no cases) ---+--> public sources
              +-- option, disabled: hybrid planner ------------------+--> Opus (content
                                                                     |    without client data only)
```

| Layer | Component | Pattern | Notes |
|---|---|---|---|
| Channels | PWA on the LAN, Word plugin, office e-mail | 2.12 | no consumer messengers for client data |
| Orchestrator | your own loop or Pydantic AI; `plan.md`; procedures per profession | 2.2, 2.16 | concurrency limit in one place |
| Models | main LLM + Bielik-11B-v3 + a small critic + STT / TTS / OCR | 2.3, 2.19 | only weights with a commercial license (Apache-2.0, MIT) |
| Knowledge | RAG over cases and the mailbox; ISAP / ELI and SAOS mirrors | 2.14 | a citation or "I don't know" |
| Batch work | tabular review, night briefs | 2.11, 2.15 | GPU at night |
| Memory | `USER.md` without client data, memory per case, git | 2.10 | character limit |
| Execution | a sandbox per case, a separate system user | 2.6 | egress closed by default |
| Oversight | approvals by impact, critic, credential broker | 2.7, 2.8 | a human does the login and 2FA |
| Log | append-only events, a "tools note" per case | section 5 | the log is personal data |
| Evaluation | golden sets, pass^k, PLCC / CPTUB | 2.17, section 5 | before every model change |

### Data flow rules

1. **Client data does not leave the box.** The model, index, logs and backups are local — then for the AI part there is no
   processor (Article 28 of the RODO (Rozporządzenie o Ochronie Danych Osobowych — GDPR)) and no transfer outside the EEA (Chapter V)
   ([RODO](https://eur-lex.europa.eu/eli/reg/2016/679/oj)). This works only if the vendor's service does not reach the data:
   signed update packages, no remote shell by default.
2. **Outbound traffic is one-way and without client data.** A separate process fetches updates and mirrors of public
   sources; the process with access to cases has no network. Ghost makes the egress firewall a feature of trust
   ([TechCrunch, 5 October 2026](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/)).
3. **The hybrid planner (Opus) is disabled by default and gets only content in which there was never any client data**:
   questions about provisions detached from the case, tool code, templates, procedures. Why not "anonymized case files":
   pseudonymized data is still personal data (recital 26 of the RODO); re-identification is a documented risk of LLM
   systems ([EDPB, 10 April 2025](https://www.edpb.europa.eu/our-work-tools/our-documents/support-pool-experts-projects/ai-privacy-risks-mitigations-large_pt));
   a US provider is subject to the CLOUD Act ([18 U.S.C. § 2713](https://www.law.cornell.edu/uscode/text/18/2713)); § 23e ZZEA
   prohibits sharing confidential information with tools without "due protection". The "local executor as a privacy filter" from
   [03-ARCHITECTURE](../agent-harnesses/03-ARCHITECTURE.md#fully-local-mode) is also a model —
   it can be wrong. More broadly: [04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md). This is not legal advice.
4. **Full disk encryption, separate accounts, encrypted backups.** A stolen unencrypted box is a breach
   within the meaning of Articles 33–34 of the RODO.

### Hardware size

Prices, availability and measurements of the boxes: [04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md). Here only what must
fit in memory — my estimate from weight sizes, not a measurement:

| Memory class | What fits | For whom |
|---|---|---|
| 16–24 GB | gpt-oss-20b (fits in 16 GB), Bielik-11B-v3 or Bielik-Minitron-7B | solo — chat and drafts, no heavy reasoning |
| 32–64 GB | Qwen3.8-27B (Q4 ~18.5 GB) or Qwen3.6-35B-A3B (Q4 ~23 GB) + Bielik + whisper | solo or 2–3 people, tabular review in a queue |
| 128 GB | gpt-oss-120b or Gemma-4-31B at higher precision + Bielik + vision + STT at once | an office of 1–5 people, RAG over case files |

Two hard rules: **for agents at least Q4** — in PolAgentBench Bielik-11B-v3, Bielik-Minitron-7B and Llama-PLLuM-8B
"fall off a cliff" between 3 and 2 bits ([arXiv 2609.32042](https://arxiv.org/abs/2609.32042)); **only weights
with a commercial license** — the PLLuM "-nc" models drop out. Sizes: [gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b),
[Bielik-11B-v3](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct), [building blocks: image](../agent-harnesses/02-BUILDING-BLOCKS.md#vision).

### Variant on my rig

4× R9700, DeepSeek-V4-Flash at 3 bits (104.2 GB), `--parallel 4` at 131k each, ~1.4 GB of free VRAM per card
([03-ARCHITECTURE](../agent-harnesses/03-ARCHITECTURE.md#1-resources-what-you-really-have)). The model is **text-only**,
so everything "sensory" goes alongside:

| Resource | Role |
|---|---|
| Slot 1 | orchestrator and planner (thinking on), synthesis of results |
| Slots 2–3 | executors: tabular review cells, extraction, drafts (3 at once is the measured optimum) |
| Slot 4 | reserve for interactive conversation, so the user does not wait behind batch work |
| CPU | `gpt-oss-20b-cpu` as the critic, router and heartbeat triage; Parakeet (STT), Piper (TTS), Smart Turn |
| CPU or a freed-up card | Docling + PaddleOCR-VL for scans; Qwen3.6-35B-A3B for screenshots after a swap in llama-swap |
| Option | a test of DeepSeek-V4-Flash-Vision-Exp (same size + ~0.93 GB), experimental |

Consequence: at ~13.6 tok/s per agent **the prompt cache and short JSON outputs matter more than the choice of harness**
(2.1), and the critic and heartbeat gates must run on the CPU, because the GPU is full.

### Minimum viable product (MVP)

1. A chat in Polish over the case folder — an answer with a citation to a document page or "I don't know" (2.14).
2. Tabular review "questions × documents" with export to XLSX (2.15).
3. Drafts of letters and e-mails — **never** sending (2.8).
4. Transcription of a recording (meeting, visit, dictation) and a note from a template with links to fragments (2.13, 2.20).
5. Procedures and skills per profession, written by the professional (2.9, 2.16).
6. An event log and a "tools note" per case (section 5).
7. Zero outbound traffic with data, an encrypted disk, backups (the rules above).

Outside the MVP: computer use on external portals, messengers, live voice conversation, the hybrid planner.

### Stages

| Stage | What | Exit criterion |
|---|---|---|
| 0 — evaluation | 30–50 real tasks per profession, run specifications, PLCC / CPTUB of the chosen models | you know pass^1 and pass^8 on your own tasks |
| 1 — MVP | points 1–7, one profession, one pilot office | the professional verifies an answer faster than writing it themselves |
| 2 — proactivity | timers + gates: a new letter in the folder, a new entry in the Dziennik Ustaw mirror, a morning brief | no "empty" model calls in the log |
| 3 — action | a DOM browser on portals (KSeF, e-Sąd, ePUAP) with origin sets, a critic and a broker | zero actions with external impact without approval |
| 4 — growth | dictation and voice, a fine-tuned small model for a single task, an optional hybrid without client data | the cell cost falls, the golden-set result does not |

---

## 5. Evaluation and security

### Prompt injection in browser agents

**The cause is structural:** the agent works with the user's sessions, so the same-origin policy no longer protects —
instructions can be carried by any page, e-mail, calendar invitation or image ([Brave](https://brave.com/blog/comet-prompt-injection/)).
OpenAI (22 December 2025): prompt injection is "unlikely to ever be fully solved"
([TechCrunch](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/));
Gartner (8 December 2025) advised companies to block AI browsers ([The Register](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/)).
What has already happened:

- **Comet:** a zero-click attack through a calendar invitation — a leak of local files and 1Password credentials
  ([The Register, 3 March 2026](https://www.theregister.com/2026/03/03/perplexity_comet_browser_hole_cal_invite/)).
- **BragJack** (19 September 2026): a single malicious extension "forces a prompt" in Chrome Gemini, Edge Copilot, Comet, Opera
  Neon and Claude in Chrome ([BleepingComputer](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/)).
- **Cowork:** hidden white text in a document → files sent through an allowed API (2.6).
- Defense helps but does not close the hole: Anthropic reduced the success rate of attacks on Claude in Chrome from 23.6% to 11.2%, and for Opus 4.5
  reports ~1% against an adaptive attacker *(company data, 2025)* ([Anthropic](https://www.anthropic.com/research/prompt-injection-defenses));
  BrowseSafe detects 91% in < 0.5 s, but ~10% of attacks get through *(12.2025)*.

The best described pattern on the execution side belongs to [Harvey](01-PROFILES.md#4-harvey) (7 October 2026): checking every tool
call, "pinning" tool definitions against swapping, Rego policies blocking the "lethal trifecta"
(private data + untrusted content + external communication), stripping hidden Unicode characters from results — **enforced
outside the model** ([Harvey](https://www.harvey.ai/blog/building-harveys-mcp-policy-engine)).

**Locally you remove the cloud leak, but not prompt injection.** Hence: the agent reads rather than writes; a separate
browser profile without the main sessions; origin sets; no `file://` and no password manager; a local classifier; and the trifecta rule
in code — a session that has read untrusted content loses its external communication tools. Course:
[course 2, part 16](../course_agentic_apps/16-SECURITY-OWASP-ASI.md).

### A lesson from OpenClaw's security advisories

[OpenClaw](01-PROFILES.md#1-openclaw) has **722 security advisories** in 2026 (14 critical, 249 high, 390
medium, 69 low; GitHub API, 11 October 2026). Steinberger reports that of 1,309 reports since 10 January as many as 746 were closed as
invalid, and 87% of the "critical" ones were invalid ([OpenClaw, 30 April 2026](https://openclaw.ai/blog/openclaw-security-in-public)).
The real problems were elsewhere:

- **The skill marketplace.** Cisco found at least one vulnerability in 26% of 31,000 agent skills and a skill
  that quietly sent data out with `curl` ([Cisco, 28 January 2026](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare)).
- **The sandbox is not the default** — "the workspace is the default working directory, not a hard sandbox", also in 2.0
  ([docs](https://docs.openclaw.ai/concepts/agent-workspace),
  [The Register](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492)).
- **Responses:** VirusTotal, NVIDIA SkillSpector, Tencent ClawScan (86.9% matching labels and 98.6% of malicious
  skills caught on 556 cases *(project data)* — [ClawScan](https://openclaw.ai/blog/tencent-aig-joins-clawscan)),
  moving channels and tools out of the core into plugins, a policy compliance check from Microsoft.

Conclusions: **a small core, no open marketplace, a sandbox by default, pinned versions, a configuration compliance check
with a record for the inspector**. The number of advisories does not measure security — Hermes has none published in 2026 (GitHub API,
11 October 2026), which may result from how reports are filed, not from an absence of bugs.

### pass^k and golden sets per profession

General benchmarks saturate: OSWorld exceeded the human level, but on OSWorld 2.0 (tasks of ~1.6 h) the best
model completed 20.6%, because agents "lose constraints, guess instead of asking and skip verification"
([arXiv 2606.29537](https://arxiv.org/abs/2606.29537)). **Your** set is what counts:

| Profession | Golden set (30–50 tasks) | What you measure | Reference point |
|---|---|---|---|
| Advocate / legal counsel | a provision matched to a set of facts, a contract review, a procedural deadline | citation accuracy, "I don't know" when needed | 72.3% top-1 on provision retrieval ([arXiv 2608.30929](https://arxiv.org/abs/2608.30929)); no LLM passed the practical part of the KIO (Krajowa Izba Odwoławcza, National Appeals Chamber) exam ([arXiv 2511.04205](https://arxiv.org/abs/2511.04205)) |
| Doctor | a note from a visit recording, a ChPL question, a diagnosis code | sentences with no coverage in the recording, drug names | stricter scoring lowered results by 31 pp on Polish exams ([arXiv 2606.12250](https://arxiv.org/abs/2606.12250)) |
| Tax advisor / accountant | a journal entry from KSeF XML, a VAT classification with a KIS interpretation | a run specification (white list, interpretation citation) | the "agent prepares, human reviews" pattern from Basis (2.16) |
| Everyone | understanding Polish | PLCC, CPTUB, PolAgentBench before a model or quantization change | [CPTUB](https://huggingface.co/spaces/speakleash/cptu_bench), [PLCC](https://huggingface.co/spaces/sdadas/plcc) |

Every task has an input, an expected result, required citations and a hidden run specification (2.16). You measure pass^1
and pass^8 (2.17), and in production — like Spellbook — the **share of accepted suggestions**
([LawNext](https://www.lawnext.com/2025/08/spellbook-becomes-one-of-the-first-legal-ai-platforms-to-launch-gpt-5.html)).
Harvey has its own BigLaw Bench; I did not find a Polish equivalent for law firms. Tools:
[building blocks](../agent-harnesses/02-BUILDING-BLOCKS.md#observability-and-evaluation), [course 2, part 14](../course_agentic_apps/14-EVALUATION.md).

### Event log

**Who.** OpenHands records every interaction as a typed event (action → observation), which gives audit and replay
([OpenHands](https://docs.openhands.dev/usage/architecture/runtime)); UI-TARS-desktop has an event stream viewer;
Manus Browser Operator logs every action ([Manus](https://manus.im/blog/manus-browser-operator)). In *Amazon v. Perplexity*
the agent's logs became evidence
([ComplexDiscovery](https://complexdiscovery.com/ninth-circuit-vacates-amazon-injunction-ai-agent-logs-emerge-as-ediscovery-issue/);
I know only the title).

**Your setup.**
- An append-only log: who, when, model and version, tool, citation, who approved.
- An export of a **"tools note"** per case — § 23e ZZEA requires naming the tools used and their purpose at the client's request
  ([NRA](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/)).
- The log is personal data: encryption (Article 32 of the RODO), retention, export and deletion per client. UODO (Urząd Ochrony Danych Osobowych, the Polish data protection authority) reminds that one should
  "regularly measure and test the implemented security measures" ([UODO, 26 June 2026](https://uodo.gov.pl/pl/138/4449)) —
  the log plus the golden set is exactly that measurement.
- Course: [course 2, part 15](../course_agentic_apps/15-OBSERVABILITY.md).

This is not legal advice — I discuss the regulations and professional obligations in [04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md).
