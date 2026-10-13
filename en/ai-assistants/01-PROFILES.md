# Assistant profiles — the fifteen and the rest of the field

**As of 11 October 2026.** Each profile has nine areas: open or closed, purpose, features, advantage, architecture,
how it makes money, offline, what to adopt, and worth knowing. Figures carry a date and a source; data supplied
by the companies themselves I mark *(company data)*. Ranking and weights: [README.md](README.md#how-i-chose). Score legend:
T — traction (35%), I — idea (25%), L — learning value (25%), A — architectural transparency (15%), each 1–5.

## Table of contents

- Profiles: [1. OpenClaw](#1-openclaw) · [2. Claude](#2-claude) · [3. Abridge](#3-abridge) · [4. Harvey](#4-harvey) · [5. Hermes Agent](#5-hermes-agent) · [6. Manus](#6-manus) · [7. ChatGPT](#7-chatgpt) · [8. Gemini](#8-gemini) · [9. Cursor](#9-cursor) · [10. Granola](#10-granola) · [11. Sierra](#11-sierra) · [12. OpenEvidence](#12-openevidence) · [13. browser-use](#13-browser-use) · [14. Noxtua](#14-noxtua) · [15. Perplexity](#15-perplexity)
- [Also worth knowing — who did not make the top fifteen](#worth-knowing--who-did-not-make-the-fifteen)

---

## 1. OpenClaw

**Category:** lives autonomously · **Code:** open (MIT) · ⭐ <!-- gh:openclaw/openclaw -->391.7k ·
**Company:** OpenClaw Foundation (USA, non-profit 501(c)(3)); creator Peter Steinberger · **Score: 100** (T5 I5 L5 A5)

> A daemon on your own computer that you talk to from WhatsApp, Signal or Teams and that wakes itself up (heartbeat,
> cron, e-mail) — the archetype of the assistant "living its own life" in 2026 and the largest ecosystem in the category:
> the most stars, channels and skills, and since September 2026 also the foundation of a Microsoft product.

**Open or closed.** All code is MIT; latest release v2026.10.1 (10 October 2026). Self-hosting is the
default mode ("runs on your hardware, your rules"). Company distributions are built on the same code: Microsoft
Autopilot (a closed product, fixes flow back upstream), NVIDIA NemoClaw (Apache-2.0) and OpenClaw Enterprise
(free).

**Purpose.** A personal agent that works 24/7 on the owner's hardware and answers wherever the owner already writes —
no new app. In early 2026 it was used by hobbyists and programmers, then freelancers and small businesses
(e.g. lead generation), and in autumn 2026 by large corporations through Microsoft Autopilot and OpenClaw Enterprise. The problem it
solves: "an agent that does things when you're not around".

**Features.**
- One gateway (*Gateway*) for a dozen or so channels: Discord, Google Chat, iMessage, Matrix, Microsoft Teams, Signal,
  Slack, Telegram, WhatsApp, Zalo, WeChat, Feishu, SMS, e-mail and others.
- Automations: cron, webhooks, Gmail Pub/Sub and IMAP triggers, and **heartbeat** (a periodic agent turn).
- **Standing orders**: a program with a scope, a trigger, an approval gate and an escalation path,
  which the agent runs without asking about every task.
- Memory in SQLite (keywords, vectors, hybrid) and nightly "dreaming" (*dreaming*) that consolidates it.
- Skills as `SKILL.md` folders and the **ClawHub** registry; plugins for channels, providers and tools.
- Voice on Discord, iOS/Android "nodes", a browser relay, agent teams, A2A; version 2.0 (v2026.8.1,
  30 August 2026) added a simpler installer, a new browser UI and shared cloud sessions.

**Advantage.**
- **Distribution and network effect.** The most "starred" agent repository (391.7k ⭐, GitHub API
  11 October 2026); ClawCon — 34 events in 16 countries, about 30 thousand sign-ups *(foundation data, 8 July 2026)*.
- **Messenger UX.** The agent lives in the chat you already use — the barrier to entry is close to zero.
- **A platform, not a product.** The big players build on it instead of competing with it: Microsoft, NVIDIA, OpenAI,
  Tencent, Red Hat. Whoever writes a plugin or a skill reaches all distributions at once.
- **Behavior in readable files** that the owner can open, edit, version and roll back.

**Architecture.**
```
channels (WhatsApp, Signal, Teams, e-mail…) ┐
cron · webhook · IMAP · heartbeat ──────────┼─► Gateway: one long-lived process, loopback only by default
                                            │     session from the point of origin: console → main, DM → DM session,
                                            │     group → group session (each with its own trust and sandbox)
                                            └─► agent loop ─► model: any provider or a local one
                                                  ├─ prompt from files: AGENTS.md SOUL.md IDENTITY.md USER.md
                                                  │  BOOTSTRAP.md MEMORY.md (injected in every session)
                                                  ├─ tools: shell, files, browser, skills, plugins
                                                  └─ memory: SQLite + dreaming → DREAMS.md → MEMORY.md
```
- The **gateway** is the single source of truth for sessions, routing and channels. An unknown DM sender gets a pairing code,
  groups use allowlists and a mention requirement; `openclaw security audit` checks the configuration.
  **Trust is a property of the session**, derived from the message source, not a flag on a tool.
- **Heartbeat** is a system task: every 30 min by default (every 1 h with Anthropic OAuth) — "periodic agent turns
  in the main session"; event wake-ups at least 30 s apart, lockout after 5 starts in 60 s.
- **Dreaming**: light, REM and deep phases in the background; the output goes to `DREAMS.md`, and only strong entries with a weight of 1–10 and trigger phrases
  get promoted to `MEMORY.md`.
- **Slimmed-down core** since Apr 2026: channels, providers and heavy tools moved into plugins; "plugins can act as
  harnesses" (e.g. Codex for GPT models).
- **Optional sandbox**: "the workspace is the default cwd, not a hard sandbox" — still off by default in 2.0.
- **Local models**: a llama.cpp plugin that picks a recipe for your RAM/VRAM, Ollama (native `/api/chat`; the `/v1` endpoint
  per the documentation "breaks tool calling"), LM Studio, vLLM, MLX, `ds4` for DeepSeek V4 Flash on Metal.
- Gateway and session breakdown: [course 2, part 1](../course_agentic_apps/01-AGENT-ARCHITECTURES.md); pitfalls
  with a local model: [harness survey](../agent-harnesses/README.md#why-they-are-not-at-the-top).

**How it makes money.** The project itself does not make money — others make money on it.
- **The foundation** (announced 8 July 2026): a US 501(c)(3), 12 full-time staff *(foundation data)*. Donors
  and partners: University of Michigan (the largest donor; it founded the Institute for Agentic Computing), OpenAI
  ("major donor", also funds inference), NVIDIA, Microsoft, Red Hat, Tencent, Atlassian; infrastructure from
  Vercel, Cloudflare, GitHub and others. **The foundation does not disclose amounts.**
- **Commercial distributions**: Microsoft Autopilot (an evolution of Microsoft Scout, part of Copilot; announced 25 September 2026,
  private preview since the end of Sep 2026, price unknown); NVIDIA NemoClaw (NVIDIA sells GPUs and DGX); Tencent
  and Z.ai services in China (Mar 2026, *per the press*). OpenClaw Enterprise (29 September 2026, with OpenAI, Red Hat and NVIDIA) "will always
  be free" *(foundation data)*. In ClawHub I found no paid listings or revenue sharing.
- The creator, Peter Steinberger, moved to OpenAI on 14–15 February 2026 and runs "Claw Labs" there; Sam Altman announced that the
  project will stay in the foundation as open source supported by OpenAI.

**Offline.** **Partially** — the core yes, the channels no. The agent loop, memory, heartbeat and cron work with a local
model; the CLI, TUI and local browser UI need no network. The smallest ready llama.cpp recipe requires
≥8 GiB of memory at 64K context. WhatsApp, Telegram, Signal and the rest of the messengers inherently require the internet.
The documentation warns: "local models do not provide hosted providers' safety filters". The harness survey
turned up two problems with llama.cpp: silently dropped tool calls and a variable prompt start that destroys the prompt
cache ([pitfall H4](../agent-harnesses/01-PROFILES.md#seven-pitfalls-common-to-all)).

**What to adopt.**
- **Behavior in files the client can read.** `SOUL.md` (tone), `USER.md` (who the client is), `MEMORY.md`
  (what the assistant knows). In a law firm this doubles as documentation: "what the system knows about me" opens in an editor.
- **Standing orders as a competence agreement:** "you run the daily inbox triage; you send nothing outside the
  firm; you escalate a court letter to me immediately". Four fields: scope, trigger, gate, escalation.
- **Trust per session:** the owner's console — full permissions; a message from an external channel — a session with no
  shell and no case files. For professions bound by professional secrecy this is a requirement, not an option.
- **Heartbeat is just a scheduled turn** with a short checklist and anti-spam limits. On the rig, reserve
  one of the 4 DeepSeek-V4-Flash slots for heartbeat and cron so the background does not block the conversation; consolidate memory at night
  (`DREAMS.md`), when all slots are free.
- **What not to copy:** an open skill marketplace without verification, an "optional" sandbox and unencrypted secrets.
  OpenClaw in a law firm — only in a wrapper like NemoClaw (sandbox, allowlist of addresses,
  operator approvals).

**Worth knowing.**
- **Five names in two months:** Warelay (24 November 2025) → CLAWDIS → Clawdbot → Moltbot (27 January 2026, after an
  Anthropic trademark complaint) → OpenClaw (29–30 January 2026). In the first week >100k stars and 2 million visits;
  Cloudflare wrote about a "flood of people buying Mac minis" to run the agent (29 January 2026).
- **Security is the price of popularity:** 722 security advisories published in 2026 (14 critical, 249
  high, 390 medium, 69 low; GitHub API, 11 October 2026). Steinberger (30 April 2026): of 1309 reports since 10 January,
  as many as 746 were invalid, and of 109 "critical" ones — 95 (87%). ClawHub audits: 341 malicious skills out of 2857
  (Feb 2026) and 1103 out of 14,706 (Mar 2026) — *secondary source only*. Cisco (28 January 2026): a skill quietly sent
  data out with `curl`; 26% of 31 thousand analyzed skills had at least one vulnerability.
- **The ecosystem's response:** VirusTotal scanning (7 February 2026), NVIDIA SkillSpector and Skill Cards (1 June 2026),
  Tencent AI-Infra-Guard in ClawScan (2 October 2026; 98.6% of malicious skills detected on 556 test
  cases, *foundation data*). Even so, The Register (31 August 2026) on version 2.0: unencrypted secrets, sandbox
  off by default. The foundation itself admits that IT departments' default stance is to ban such agents.
- **Autonomy without oversight compromises:** MoltMatch (Feb 2026) — an agent created a dating profile for its owner on its own;
  another "hacked" a gym waiting list. In Moltbook, an agents-only network, Wiz found 1.5 million
  exposed API tokens; Meta bought the service anyway (10 March 2026).
- **From "virus" to product:** Nadella compared OpenClaw to a virus in Feb 2026, and in September Microsoft shipped Autopilot built on it and sends fixes upstream (company-policy
  compliance, Windows/WinUI, Teams, hiding secrets in approval
  prompts). China in Mar 2026 restricted OpenClaw in banks and government offices, while Shenzhen was subsidizing it at the same time.
- **The same project, a different rating:** in the [harness survey](../agent-harnesses/01-PROFILES.md#remaining-candidates-ranks-2164)
  OpenClaw ranks 47th (64 pts), because what counted there was working with a local model, hybrid setups and security.
  Here I rate the assistant as a product and a market lesson — and here it wins on traction and idea. Both conclusions agree:
  an excellent architecture case study, a risky production base.

**Sources:** [GitHub](https://github.com/openclaw/openclaw) · [introduction](https://openclaw.ai/blog/introducing-openclaw) · [foundation](https://openclaw.ai/blog/introducing-openclaw-foundation) · [OpenClaw Enterprise](https://openclaw.ai/blog/openclaw-enterprise) · [Microsoft Autopilot](https://openclaw.ai/blog/microsoft-autopilot-openclaw) · [security in public](https://openclaw.ai/blog/openclaw-security-in-public) · [rough week](https://openclaw.ai/blog/openclaw-rough-week) · [VirusTotal](https://openclaw.ai/blog/virustotal-partnership) · [NVIDIA SkillSpector](https://openclaw.ai/blog/openclaw-nvidia-skill-security) · [ClawScan](https://openclaw.ai/blog/tencent-aig-joins-clawscan) · [heartbeat](https://docs.openclaw.ai/gateway/heartbeat) · [standing orders](https://docs.openclaw.ai/automation/standing-orders) · [dreaming](https://docs.openclaw.ai/concepts/dreaming) · [workspace](https://docs.openclaw.ai/concepts/agent-workspace) · [local models](https://docs.openclaw.ai/gateway/local-models) · [Ollama](https://docs.openclaw.ai/providers/ollama) · [security](https://docs.openclaw.ai/gateway/security) · [TechCrunch: Steinberger at OpenAI](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/) · [The Register on 2.0](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) · [Cloudflare Moltworker](https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/) · [Cisco](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare) · [InsiderLLM: ClawHub audits](https://insiderllm.com/guides/openclaw-clawhub-security-alert/) · [Wiz: Moltbook](https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys) · [Wikipedia: OpenClaw](https://en.wikipedia.org/wiki/OpenClaw) · [Wikipedia: Moltbook](https://en.wikipedia.org/wiki/Moltbook)


---

## 2. Claude

**Category:** everyday + professional + executor · **Code:** closed (open: the computer use demo, tool
schemas) · **Company:** Anthropic (USA) · **Score: 97** (T5 I5 L5 A4)

> One family of assistants on one model — chat with memory, Cowork for working on files, Claude in Chrome, computer
> use in the API and Claude Code in the terminal — in which the coding agent became the template for everything else ("Claude Code for
> the rest of your work").

**Open or closed.** The models and apps are closed. Open: the reference computer use demo (a Docker container
with Xvfb, Firefox, LibreOffice, an agent loop and a UI) and the publicly documented tool schemas. The Claude Code client code
leaked in Mar 2026 through a published source map file (Ars Technica per Wikipedia) — that does not make it open.
There is no model self-hosting; the closest to sovereignty is Bedrock, Vertex or Microsoft Foundry in a chosen region.

**Purpose.**
- **Chat** (Pro, Max, Team, Enterprise) — an everyday assistant with memory, connectors and skills.
- **Cowork** — an agent for non-technical knowledge workers (documents, spreadsheets, presentations in designated folders);
  **Claude in Chrome and computer use** — an executor in the browser and on the desktop, in the API also for RPA and QA builders.
- **Claude Code** — programmers in the terminal, IDE, desktop app and web; in Feb 2026 more than half of Claude
  Code revenue came from companies *(company data)*.
- **Industry editions** — "Claude for Legal" with plugins for specializations and MCP connectors to Westlaw, Box and Docusign
  (12 May 2026).

**Features.**
- **Memory** (25 August 2026): one for chat and Cowork, stored as readable topic files that can be edited and deleted;
  sensitive topics (health, beliefs, etc.) **are not saved by default**.
- **"One Claude"** (16 September 2026): Cowork merged with chat; tasks keep running "even after you've closed your
  laptop" and can be scheduled ("Schedule it for every Monday"); by default Claude asks before acting. Earlier came
  **Dispatch** (23 March 2026, with computer use, a research preview in Pro and Max): a task from your phone executed on your computer.
- **Claude in Chrome**: a side panel that navigates, fills in forms, works across several tabs in its own group,
  runs tasks in the background and on a schedule; GA on all paid plans.
- **Computer use and browser use in the API** (GA, `*_20260801` toolsets): 17 desktop tools with batched actions (stop on the
  first error) and 31 browser tools based on the accessibility tree; they are executed by **your** environment.
- **Claude Code**: a terminal loop (files, shell), MCP, subagents, hooks, skills, plugins, a
  `CLAUDE.md` file; cloud sessions (an Anthropic VM or the customer's environment), Remote Control, Routines (14 April 2026).
  Connectors, skills and plugins also work in chat, Cowork and Chrome.

**Advantage.**
- **Model and agent from one lab.** OSWorld: 14.9% (22 October 2024) → 61.4% (29 September 2025) → 72.5% (Feb 2026, against
  a human level of 72.36%) → 81.8% "partial" on OSWorld 2.1 for Opus 5.5 (22 September 2026) *(company data)*.
- **Claude Code as the locomotive.** >USD 2.5 bn run-rate (12 February 2026) and about 4% of public GitHub commits
  (Feb 2026) *(company data)*; in the 2026 Stack Overflow survey the most used coding agent (66% of agent
  users, 6 October 2026).
- **A shared harness under everything.** Cowork was built on the Claude Code / Agent SDK stack; the same SDK was chosen by Thomson
  Reuters for the new CoCounsel (Jun 2026), and by NanoClaw as its core. Patterns won among programmers (the project file,
  skills, hooks) carry over to the office.
- **Published prompt injection defense figures:** attack success in Chrome 23.6% → 11.2% after safeguards
  (25 August 2025); about 1% for Opus 4.5 against an adaptive attacker (24 November 2025) — Anthropic adds that this "still
  represents meaningful risk". On top of that, distribution: Cowork, Chrome and Claude Code are included in the price of the Pro, Max and Team plans.

**Architecture.**
```
cloud model (Anthropic API / Bedrock / Vertex / Foundry)
   ▲  prompts, tool results, screenshots
   │
   ├─ chat + Cowork ──── isolated environment with shared folders + a separate agent browser
   ├─ Claude in Chrome ─ an extension in the user's real, logged-in browser
   ├─ computer/browser use API ─ actions are executed by the developer's sandbox ("nothing executes on Anthropic's servers")
   └─ Claude Code ────── local CLI: files, shell, hooks, MCP, subagents; transcripts on disk
```
- **The computer use loop:** toolset → `tool_use` → the app performs the action → sends back a screenshot (about 1000–1800 tokens) →
  repeat; recommendations: 1024×768–1280×800, ≤20 images, prompt caching, trimming old screenshots in batches.
- **Browser use** reads the accessibility tree (fewer tokens than screenshots), and element references survive layout
  shifts. URL validation (rejecting `javascript:`, `file:`, `data:`) is the developer's job; upload and JS are off by default.
- **Where Cowork runs:** in January 2026 (research preview) in a **local Linux VM** on Apple's
  Virtualization framework, mounting only the shared folders and with restricted networking (Simon Willison's analysis). The current
  help article says: "Cowork runs your tasks in the cloud" — in an isolated environment on Anthropic's servers;
  outbound traffic permissions **do not cover** web fetch, web search or MCP. The model has always run in the cloud.
- **Chrome:** per-site permissions, confirmations before publishing, purchasing and sharing personal data,
  blocked categories (including financial services), injection classifiers, RL training on hostile content.
- **Claude Code — data:** transcripts stored locally for 30 days; retention: companies 30 days, Enterprise — zero data retention
  by agreement, consumers 30 days or 5 years if they consent to training; `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`
  turns off unnecessary traffic; in cloud VMs the GitHub credentials do not enter the machine.

**How it makes money.**
- **Subscriptions** (as of 10.2026): Pro USD 20/month (USD 17 with annual billing), Max USD 100 and 200,
  Team USD 20 per seat (2–150 people), Enterprise — custom. Chrome initially only in Max (pilot from
  25 August 2025), from 18 December 2025 also in Pro, Team and Enterprise.
- **API per token:** Opus 5.5 — USD 4 / 20 per 1 million input/output tokens (22 September 2026); Sonnet 4.6 — USD 3 / 15;
  also through AWS, Google Cloud and Azure.
- **Weekly limits** in Claude Code (announced 28 July 2025, effective 28 August 2025) in response to 24/7 background work
  and account resale; according to Anthropic they affected <5% of subscribers.
- **Anthropic's finances:** Series G — USD 30 bn at a USD 380 bn post-money valuation, run-rate USD 14 bn, Claude Code
  >USD 2.5 bn (doubled since 1 January 2026), business subscriptions ×4 over the same period (12 February 2026, *company data*).
  About USD 44 bn run-rate in May 2026 *(SemiAnalysis estimate via the press, unverified)*.
- **Acquisitions:** Vercept (25 February 2026) — perception and interaction for computer use.

**Offline.** **No.** Inference always goes to the cloud (Anthropic or Bedrock/Vertex/Foundry regions). Only the "hands" run locally:
the computer/browser use tools from the API in your VM and the Claude Code client on your disk.
A local equivalent needs: a local model (for the desktop — a vision model, since DeepSeek-V4-Flash cannot
see images), a VM mounting only designated folders, memory in files and local transcripts. A note for Polish
companies: in Microsoft 365 Copilot the Anthropic models are **excluded from the EU Data Boundary** (Microsoft documentation,
8 October 2026) — the choice of model alone can quietly take data out of the EU.

**What to adopt.**
- **Separate the "brain" and the "hands":** the executor (VM, browser, folders) stays local, the model is swappable.
  In the hybrid setup Opus 5.5 gets the task and a plan, while the client's case files are read only by the local DeepSeek — the boundary is described in
  [course 1, part 10](../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md).
- **Memory as topic files with sensitive categories switched off.** For a doctor or a lawyer this is a ready-made pattern:
  health data and other special categories of data (GDPR, Art. 9) kept out of long-term memory by default
  *(this is not legal advice)*.
- **Per-folder permissions + "ask before acting" by default + a ban on deleting without consent** — three Cowork settings
  that a professional will understand without training.
- **The accessibility tree instead of screenshots** — the only way for the text-only DeepSeek-V4-Flash to work in a browser;
  plus batched actions that stop at the first error.
- **A single "no unnecessary traffic" switch and local transcripts with retention** — regulated clients will
  demand this; the lesson from PromptArmor: an allowlist of addresses is not enough when an allowed endpoint accepts other people's API
  keys.

**Worth knowing.**
- **PromptArmor (Jan 2026):** white text on a white background in a document told Cowork to send the victim's files to the attacker's
  account through the **allowed Anthropic API** with the attacker's key (it worked on Haiku and Opus 4.5). Anthropic
  recommended not sharing sensitive local files.
- **BragJack (19 September 2026):** a malicious extension "forces" commands onto a privileged AI component — it affected
  among others Claude in Chrome (CVE-2026-0628 in Chrome). Anthropic itself advises against banking, medical records
  and password managers in Chrome.
- **What people delegate** (1.2 million Cowork sessions from May 2026, published 7 July 2026): 33.4% business processes and operations,
  16.4% content, 8.7% programming, 7% DevOps, 6.4% research, 5.8% data analysis — roughly half is "the work
  around the work", not autonomous management of life.
- **Abuse:** Claude Code was used in a data extortion campaign (Aug 2025) and in a Chinese espionage campaign
  (Sep 2025) that automated 80–90% of the work (Wired and BBC per Wikipedia).
- **A business lesson:** computer use launched on 22 October 2024 as "experimental — at times cumbersome and error-prone",
  and the flat-rate subscription plus 24/7 agents ended in limits — do the math before you sell an "unlimited assistant".

**Sources:** [Series G](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation) · [memory](https://claude.com/resources/articles/claudes-memory-works-everywhere-and-you-decide-whats-in-it) · [Cowork to Claude](https://claude.com/resources/articles/cowork-is-now-claude) · [how people use Cowork](https://claude.com/resources/articles/how-people-are-using-claude-cowork) · [Dispatch and computer use](https://claude.com/resources/articles/dispatch-and-computer-use) · [Routines](https://claude.com/resources/articles/introducing-routines-in-claude-code) · [Cowork research preview](https://claude.com/blog/cowork-research-preview) · [Cowork — help](https://support.claude.com/en/articles/13345190-getting-started-with-cowork) · [Simon Willison on Cowork](https://simonwillison.net/2026/Jan/12/claude-cowork/) · [computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) · [browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) · [computer use demo](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) · [Claude for Chrome](https://claude.com/blog/claude-for-chrome) · [Claude in Chrome](https://claude.com/chrome) · [prompt injection defenses](https://www.anthropic.com/research/prompt-injection-defenses) · [computer use 2024](https://www.anthropic.com/news/3-5-models-and-computer-use) · [Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5) · [Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6) · [Opus 5.5](https://www.anthropic.com/news/claude-opus-5-5) · [Vercept](https://www.anthropic.com/news/acquires-vercept) · [Claude Code — data](https://code.claude.com/docs/en/data-usage) · [weekly limits](https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/) · [Stack Overflow 2026](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/) · [SemiAnalysis via the press](https://www.itiger.com/hans/news/1183910360) · [Claude for Legal](https://techcrunch.com/2026/05/12/the-ai-legal-services-industry-is-heating-up-anthropic-is-getting-in-on-the-action/) · [CoCounsel on the Agent SDK](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html) · [EU Data Boundary](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) · [PromptArmor](https://www.promptarmor.com/resources/claude-cowork-exfiltrates-files) · [BragJack](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/) · [Wikipedia: Claude](https://en.wikipedia.org/wiki/Claude_(language_model)) · [Wikipedia: Claude (AI)](https://en.wikipedia.org/wiki/Claude_(AI))


---

## 3. Abridge

**Category:** professional (medicine) · **Code:** closed · **Company:** Abridge AI Inc. (USA, Pittsburgh) ·
**Score: 94** (T5 I5 L5 A3)

> An "ambient scribe" for American hospitals: it listens to the visit, writes the note into the EHR and next to every sentence shows
> where in the conversation it came from. It is the best example on the market of how a professional assistant earns trust.

**Open or closed.** Closed, cloud only (SaaS). Its own speech recognition (ASR) model and its own hallucination
"guard" model; the large language model providers are not disclosed. No self-hosting.

**Purpose.** Doctors, nurses and whole healthcare systems in the USA, mostly Epic customers. Abridge sells to
the organization, not to the individual doctor. The problem: doctors spend their evenings on documentation instead of with the patient.
Since 11 June 2026 the company calls itself an "AI-native clinician intelligence platform" and goes beyond the note itself.

**Features.**
- A visit note generated from a recording of the conversation (specialty templates, SOAP).
- **Linked Evidence:** every sentence of the note leads to a fragment of the transcript and the recording.
- Nursing documentation.
- Since 2026: billing and claims compliance, clinical decision support, workflows with payers,
  clinical trial eligibility screening during the visit.
- Direct write to the EHR after the doctor's approval.
- Partnerships: NVIDIA ("foundation model for clinical conversations"), Artisight (in-room sensors), a strategic
  investment from Eli Lilly (terms undisclosed).

**Advantage.**
- **Trust built into the interface.** The doctor does not have to believe the model — they click a sentence and hear what was said in the exam room.
  This shifts control from "is the AI right" to "I check it in 3 seconds".
- Deep Epic integration and early entry; #1 Best in KLAS for Ambient AI in Feb 2026, second year in a row
  *(per Sacra)*.
- Data scale: over 100 million conversations a year *(Fortune, Jun 2026)* — fuel for its own ASR and guard.
- To be fair: in an independent ED study (Webb et al., Appl Clin Inform, Jan 2026, n=18) usability was equal
  (SUS 73.5 vs 73.5), but Microsoft's DAX did better on note quality (PDQI-9: 39 vs 36.5, p=0.011).

**Architecture.**
```
phone / EHR app (e.g. Epic Haiku) ── recording ──▶ Abridge cloud
  └▶ own medical ASR + diarization (doctor / patient)
     └▶ LLM: first draft of the note in a specialty template
        └▶ guard model: detects and corrects sentences with no support in the transcript
           └▶ doctor's review with Linked Evidence ──▶ signature ──▶ write to the EHR
```
- ASR: per the company 24% relatively fewer errors (WER) than "leading commercial competitors", 83% fewer errors on new
  drugs, 15% better with accents *(company data, 6 August 2025)*.
- The guard: the whitepaper "Science of Confabulation Elimination" (19 August 2025) — rules built on 1,000+ hours
  of human validation caught 97% of unsupported claims on an internal set of 10,000+ visits, versus 82% for
  GPT-4o *(company data)*.
- Everything in the cloud; no market-leading scribe processes recordings on the device.

**How it makes money.** Enterprise licenses per doctor: about USD 2,500 a year *(Sacra estimate)*.
- ARR: about USD 60 million (end of 2024), USD 100 million (May 2025), USD 117 million of contracted ARR in Q1 2025
  *(Sacra, TechCrunch — 2025 data, nothing newer)*.
- Funding: Series D USD 250 million at a USD 2.75 bn valuation (Feb 2025); Series E USD 300 million at USD 5.3 bn (Jun 2025,
  a16z and Khosla); Series E extension USD 316 million (Apr 2026); about USD 830 million in total. A secondary-market valuation of
  about USD 7 bn (May 2026) — unverified.
- Customers: 300+ healthcare systems, 250 million+ patients covered (Jun 2026), including Kaiser Permanente
  (24,600 doctors), Mayo Clinic, Johns Hopkins *(company data)*.
- Scribe market share in 2025: about 30% (Microsoft/Nuance about 33%) *(Menlo Ventures, Oct 2025)*.

**Offline.** **No.** Cloud only. A local equivalent needs: Polish ASR with timestamps
(e.g. Parakeet-TDT-0.6B-v3 — about 7.3% WER on Polish datasets per the model card — or Whisper), offline diarization
(pyannote "community-1", CC-BY-4.0), a local LLM for the note and for a second, verifying pass, and for integration
with the fragmented Polish EDM systems (electronic medical records) — browser plugins (the route Noa Notes chose). DeepSeek-V4-Flash
cannot hear — speech has to go through a separate STT model (see [Voice](../agent-harnesses/02-BUILDING-BLOCKS.md#voice)).

**What to adopt.**
- **Linked Evidence as a principle, not a feature.** STT returns segments with an ID and a time (`[s12] 03:41–03:52`), the prompt
  forces every sentence of the note to end with a list of source IDs, and the interface turns them into a clickable replay
  of the fragment. A sentence without an ID = a red underline.
- **A verification pass on a separate slot.** The rig has 4 slots: slot 1 writes the draft, slot 2 checks sentence by sentence
  "does the transcript support this?" (yes/no/partially + a quote). It costs time, not money — the marginal cost of
  local inference is close to zero.
- **Your own ASR test on Polish drug names** (a list from the ChPL, the Summary of Product Characteristics) — that is where the biggest risk lies and the best
  sales argument.
- **Scope: documentation only.** The Kodeks Etyki Lekarskiej (Code of Medical Ethics, KEL) Art. 12 requires patient consent and a certified algorithm
  for AI in diagnosis or treatment; a note and letters without a diagnostic suggestion are — in my reading — outside the scope of Art. 12 KEL (the NIL, the Polish Chamber of Physicians and Dentists, has taken no position on scribes)
  (details in [04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md); this is not legal advice).
- **Deleting the recording after the note is signed** and technical support without access to the data: a vendor with
  remote access to a clinic's computer becomes a processor (GDPR Art. 28) bound by confidentiality
  (Art. 24(6) of the ustawa o prawach pacjenta, the Polish Patient Rights Act).
- **Price anchor:** Noa Notes costs PLN 199 + VAT a month per doctor (AWS/Azure cloud).

**Worth knowing.**
- Founded in 2018 by the cardiologist Shiva Rao; its valuation doubled in four months in 2025.
- In Feb 2026 Epic launched its own scribe (AI Charting), and hospitals began to "recalculate the sense of separate contracts" —
  Abridge's turn toward a "platform" (Jun 2026) is a response to the commoditization of the basic scribe.
- Moving into coding and billing carries a new risk: US insurers are protesting AI-driven
  "coding intensity" (press headlines, Mar and Sep 2026).
- Independent scribe studies (PHTI, Mar 2025; a UCLA RCT in NEJM AI, Dec 2025) mostly show less burnout
  and a moderate time saving — sell wellbeing and quality, and if you promise "an hour a day", measure it.

**Sources:** [Fortune, 11 June 2026](https://fortune.com/2026/06/11/abridge-operating-system-medicine-nvidia-eli-lilly-artsight/) ·
[Sacra: Abridge](https://sacra.com/c/abridge/) ·
[Abridge blog: ASR](https://www.abridge.com/blog/becoming-the-benchmark-for-healthcare-ai) ·
[confabulation whitepaper](https://www.abridge.com/ai/science-confabulation-hallucination-elimination) ·
[Webb et al., PubMed](https://pubmed.ncbi.nlm.nih.gov/41734793/) ·
[MobiHealthNews: Series E](https://www.mobihealthnews.com/news/abridge-secures-300m-boosts-valuation-53b) ·
[Menlo Ventures: AI in healthcare 2025](https://menlovc.com/perspective/2025-the-state-of-ai-in-healthcare/) ·
[HLTH: Epic AI Charting](https://hlth.com/insights/news/epic-releases-native-ai-charting-for-integrated-clinical-documentation-2026-02-06) ·
[Parakeet-TDT-0.6B-v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) ·
[pyannote community-1](https://huggingface.co/pyannote/speaker-diarization-community-1) ·
[Noa: pricing](https://noa.ai/pl/cennik) ·
[Fierce Healthcare: PHTI](https://www.fiercehealthcare.com/ai-and-machine-learning/early-evaluation-ai-scribes-finds-decreased-burnout-limited-financial-roi) ·
[UCLA RCT, PubMed](https://pubmed.ncbi.nlm.nih.gov/41497288/)


---

## 4. Harvey

**Category:** professional (law) · **Code:** closed · **Company:** Harvey AI (USA) · **Score: 94** (T5 I5 L5 A3)

> An assistant for large law firms and legal departments that grew from a "chat over documents" into a platform of agents
> working in matter spaces — with a model router, its own model and a security policy outside the LLM.

**Open or closed.** Closed SaaS in a regional cloud (EU/Switzerland, USA, Australia); no on-prem option. Since 20 August 2026 it runs its own model, **Harvey Tenet** — per Harvey its first model
post-trained on top of open weights (Kimi K3); the weights of Tenet itself are not public.

**Purpose.** Large law firms (BigLaw), corporate legal departments and advisory firms. Harvey claims to serve 80%
of the Am Law 100 firms and five Fortune 10 legal departments *(company data, 9 September 2026)*. The problem: mass review of
documents, research and drafting of letters at the pace and quality that elite firms expect.

**Features.**
- Assistant (chat over documents) and **Vault** — spaces for mass document review and data room questions.
- 500+ ready-made agents for areas of law and **Agent Builder** (early access since 5 May 2026); by then customers had built
  25,000+ agents of their own *(company data)*.
- **Harvey II** (18 August 2026): agents work in matter "Spaces" — documents, pages, tasks, permissions, history;
  the user's personal memory carries over between Harvey, Word and Outlook; **ethical walls** (conflict-of-interest
  barriers) synchronized from firm systems.
- Custom agents in Word (23 September 2026) and agentic search in document management systems (30 September 2026).
- LexisNexis content and Shepard's citation verification in Harvey (alliance since 18 June 2025); a joint
  "Motion to Dismiss" workflow (7 October 2026).

**Advantage.**
- **References from elite firms:** A&O tested Harvey from Nov 2022 — about 3,500 lawyers, about 40,000 queries.
  In law, a reference from a prestigious firm sells better than a benchmark.
- **Content + workflow:** the LexisNexis alliance provides the sources of law and citation verification, and the agent library
  is written in the language of practice, not of engineers.
- **Capital:** over USD 1.55 bn in total *(TechCrunch, 9 September 2026)* — it can afford its own model and acquisitions.
- **Security as a product:** SOC 2 Type II, ISO 27001/27701/42001, AIUC-1 certifications.

**Architecture.**
- **Multi-model by design** (10 March 2026): Claude Opus 4.6 and Sonnet 4.6, Gemini 3 Flash, GPT-5.2. A router picks a
  model by task and switches to another provider during an outage; the administrator decides which models are
  allowed. Mistral Large 3 for EU customers in early access — unverified.
- **Its own model Tenet:** Kimi K3 post-trained with asynchronous RL (GSPO) together with Fireworks; synthetic data,
  public legal and expert data — "We did not use any customer data". About 1/10 of the cost per cell in
  Review Table tasks, −90% cost of a firm-knowledge query *(company data)*.
- **Evaluation:** BigLaw Bench — its own benchmark, used both for development and in marketing.
- **MCP Policy Engine** (7 October 2026): least privilege, control of every tool call, "tool pinning"
  (detecting a swapped tool definition), Rego rules blocking the **"lethal trifecta"** (private data + untrusted
  content + external communication), a sanitizer removing hidden Unicode characters from tool results. Enforcement
  runs **outside the model**.
- **Data:** model providers must contractually guarantee zero retention, no human review and no training.

**How it makes money.** Annual enterprise per-seat contracts; pricing is not public.
- Estimates: about USD 1,200/seat/month for small deployments (min. 20 seats) and USD 100–200 at Am Law 100
  scale *(third-party estimates, 2026, unverified)*.
- ARR: USD 100 million (Aug 2025), USD 190 million (Jan 2026), over USD 400 million and 3,000+ paying organizations (Sep 2026)
  *(secondary press; Harvey itself does not disclose ARR)*.
- Customers: about 1,500 organizations, 100,000+ lawyers, 60+ countries *(company data via ITBrief, May 2026)*.
- Valuations: USD 715 million (Dec 2023) → USD 3 bn (Feb 2025) → USD 8 bn (Dec 2025) → USD 11 bn (Mar 2026) → **USD 15.5 bn**
  (9 September 2026, a USD 550 million round led by Diffusion and Lightspeed).

**Offline.** **No.** Regional cloud; the security page mentions neither on-prem nor a private cloud. Tenet
shows a move toward open weights, but nothing indicates that a customer can host it. A local equivalent
needs: an on-disk index of the matter's documents, a local model with passage citation, public sources of law
(ISAP/ELI, SAOS) instead of Lexis, and a policy layer for tools.

**What to adopt.**
- **A matter space = a confidentiality boundary.** Each matter is a separate directory, a separate RAG index, separate memory
  and a permissions list. An agent working on matter A physically does not see matter B — a local equivalent of ethical walls.
- **Tool policy outside the model.** A gate before every call: in a session with client data there are no tools
  sending anything outside (zero "lethal trifecta"); MCP tool definitions pinned by hash.
  See [16-SECURITY-OWASP-ASI.md](../course_agentic_apps/16-SECURITY-OWASP-ASI.md).
- **A router with a hard rule:** Opus as a planner gets only content without client data (e.g. "prepare a plan for
  analyzing a lease agreement for unfair clauses"), execution and documents stay on DeepSeek. A router with failover
  between slots — [17-HYBRID-AND-ROUTER.md](../course_agentic_apps/17-HYBRID-AND-ROUTER.md).
- **An agent library in the language of practice:** "analysis of an agreement for prohibited clauses", "case chronology
  from the files", "draft payment demand letter" — ready-made recipes a lawyer runs without prompting.
- **Your own benchmark before your own model.** Harvey started with BigLaw Bench and only then post-trained Tenet.
  First a set of Polish tasks with scoring, then possibly post-training (e.g. a smaller Bielik) —
  [14-EVALUATION.md](../course_agentic_apps/14-EVALUATION.md).
- **User style memory** (citation format, favorite phrasings) kept locally, separate from the matter's memory.

**Worth knowing.**
- Founded in summer 2022 by Winston Weinberg (a former O'Melveny litigator) and Gabriel Pereyra (ex-DeepMind);
  seed funding from the OpenAI Startup Fund (Nov 2022).
- 2026 acquisitions: Hexus (23 January 2026), Guardrails AI (Sep 2026, the fourth acquisition of the year).
- Competition is growing from two sides: Sweden's Legora (over USD 200 million ARR per its founder, Sep 2026) and Anthropic
  with "Claude for Legal" (plugins and MCP connectors to Westlaw, Box, Docusign, 12 May 2026).
- Demand backdrop: Damien Charlotin's database lists 2,184 court cases with AI hallucinations (as of 10 October 2026), including
  **6 in Poland** — verifiable citations are an entry requirement, not an add-on.

**Sources:** [Harvey: multi-model](https://www.harvey.ai/en-US/blog/why-harvey-is-multi-model-by-design) ·
[Harvey Tenet](https://www.harvey.ai/blog/post-training-update-harvey-tenet) ·
[Harvey II](https://www.harvey.ai/blog/introducing-harvey-ii) ·
[MCP Policy Engine](https://www.harvey.ai/blog/building-harveys-mcp-policy-engine) ·
[security](https://www.harvey.ai/en-US/security) ·
[USD 550 million round](https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence) ·
[TechCrunch, 9 September 2026](https://techcrunch.com/2026/09/09/harvey-hits-15-5b-valuation-months-after-reaching-11b/) ·
[Wikipedia](https://en.wikipedia.org/wiki/Harvey_(software)) ·
[ITBrief: 500 agents](https://itbrief.co.uk/story/harvey-launches-500-legal-ai-agents-builder-tool) ·
[raising.fi: ARR](https://raising.fi/news/harvey-undisclosed-september-2026) ·
[Vaquill: price estimate](https://www.vaquill.ai/blog/harvey-ai-review-honest-assessment) ·
[LexisNexis + Harvey](https://www.lexisnexis.com/community/pressroom/b/news/posts/lexisnexis-and-harvey-announce-strategic-alliance-to-integrate-trusted-high-quality-ai-technology-and-legal-content-and-develop-advanced-workflows) ·
[hallucination database](https://www.damiencharlotin.com/hallucinations/)


---

## 5. Hermes Agent

**Category:** lives autonomously · **Code:** open (MIT) · ⭐ <!-- gh:NousResearch/hermes-agent -->252.7k ·
**Company:** Nous Research (USA) · **Score: 93** (T4 I5 L5 A5)

> A personal agent "that grows with you": it writes and improves its own skills, and the lab that released it
> sells models for it — the second open "living" assistant after OpenClaw and the best starting point for your own
> assistant with voice and cron.

**Open or closed.** MIT; latest release v0.21.6 (8 October 2026). Nous says it released the agent under MIT in February
2026; the repository was created on 22 July 2025, and the first release tag is v2026.3.12 (12 March 2026). Self-hosting: yes —
"on a $5 VPS, a GPU cluster, or serverless infrastructure". The services around it are closed: Nous Portal (models
and credits), Hermes Business and Hermes Enterprise.

**Purpose.** For people who want a persistent agent available from their phone, without being tied to a single model provider. Since
Oct 2026 also for teams (Hermes Business) and companies with their own infrastructure (Hermes Enterprise). It solves the problem of
"the assistant forgets what it learned": a complex task leaves behind a skill for next time.

**Features.**
- TUI, a desktop app (in the Microsoft Store since 8 October 2026) and a messenger gateway: Telegram, Discord, Slack,
  WhatsApp, Signal, e-mail, Teams and others — 25+ in total per the harness survey.
- **Learning loop:** skills created after complex tasks and improved in use; the agentskills.io standard;
  installation from the official hub and from ClawHub, with security scanning.
- Memory curated by the agent, search of past sessions (SQLite FTS5 + LLM summaries), user modeling
  through Honcho.
- Cron in natural language with delivery to any channel; subagents for parallel work.
- Seven terminal backends: local, Docker, SSH, Singularity, Modal, Daytona, Vercel Sandbox; serverless backends
  "hibernate when idle".
- Voice: voice note transcription, voice replies on Telegram and Discord.
- `hermes claw migrate` — import configuration from OpenClaw.

**Advantage.**
- **A closed learning loop.** Competitors have skills written by humans; Hermes writes and improves them itself — it is
  procedural memory ("how I do it"), not just factual memory.
- **A lab behind it.** Nous trains its own models (the Hermes family), has an inference portal, and the agent generates
  trajectories for training — it is a distribution channel for models.
- **"A top-tier planner, cheap executors" built into the configuration** and the strongest cron in the category (agentless watchdogs,
  continuity between runs, incident deduplication) — per the
  [harness survey](../agent-harnesses/01-PROFILES.md#4-hermes-agent).
- **Low switching cost:** import from OpenClaw and ClawHub compatibility.
- Zero security advisories published on GitHub in 2026 (API, 11 October 2026) versus 722 for OpenClaw — though this may
  reflect how disclosure is done rather than prove security.

**Architecture.** In brief — the full technical description with local model configuration is in the
[harness survey](../agent-harnesses/01-PROFILES.md#4-hermes-agent).
- **Gateway:** one process serves all messengers; conversations are paired with a one-time code.
- **Bounded memory:** `MEMORY.md` (≤2200 characters, the agent's notes) and `USER.md` (≤1375 characters, the user profile)
  injected as a **frozen snapshot** at session start — a fixed prefix, so the prompt cache works. When memory is
  full, the agent has to consolidate it instead of silently dropping entries; fullness is visible ("67% — 1,474/2,200 chars").
- **Skills:** the `~/.hermes/skills/` directory, scanned on installation.
- **Proactivity:** cron with natural-language tasks; "agentless" watchdogs alert only on a non-empty result.
- **Execution and approvals:** locally, in an unprivileged Docker, over SSH or in the cloud; "smart approvals"
  (an auxiliary LLM assesses flagged commands) plus a hard denylist; secrets stripped from the tool environment.
- **Models:** `hermes model` — Nous Portal, OpenRouter, OpenAI or your own OpenAI-compatible endpoint; executors through
  `delegation: {provider, model, base_url}`.
- **Voice:** STT locally (faster-whisper), TTS by default Edge TTS — Microsoft's **cloud**.

**How it makes money.**
- **The agent is free (MIT); the money comes from Nous Portal:** Plus USD 20/month, Super USD 100, Ultra USD 200, with credits for
  models and tools (Hermes site, 11 October 2026, *company data*). The installer promotes the portal.
- **Hermes Business** (Oct 2026): a shared team balance with per-person spending limits, hosted agents for team
  members, a shared skills library ("the best skills anyone on your team discovers are automatically shared").
- **Hermes Enterprise:** on the customer's infrastructure, with SSO and an SLA; pricing unknown.
- **Funding:** Nous raised USD 90 million (announced Oct 2026; NVIDIA, Microsoft's M12, Samsung, Robot Ventures,
  Union Square Ventures, Y Combinator, Menlo Ventures and others). Earlier rounds — unverified.
- **Reach per Nous:** "cloned over 24 million times" and about 2.5% of worldwide token consumption *(company data, internal
  estimates, Oct 2026)*. Revenue and user numbers — unknown.

**Offline.** **Partially.** The agent loop with a local OpenAI-compatible endpoint and the "local" terminal backend
works without the internet — together with memory, skills and cron. Speech recognition is local (faster-whisper),
but **speech synthesis goes by default through Edge TTS in the cloud**; for offline work you have to swap it out (a local NeuTTS
exists, a Polish voice unconfirmed; a fully local Polish voice with Piper is offered by
[Moltis](../agent-harnesses/01-PROFILES.md#15-moltis)). Messengers and web tools require a network.

**What to adopt.**
- **Memory with a limit and a fullness indicator:** 2200 characters force curation, and the client sees how much the assistant
  "knows" about them. A frozen per-session snapshot is a fixed prefix on llama.cpp — at about 13.6 tok/s per slot you cannot afford
  to re-read the prompt on every turn.
- **Skills written after a task, approved by a human:** after the third payment demand letter, a law firm's assistant
  proposes a procedure, the attorney accepts it, and the procedure goes into the library.
- **A team skills library without client data** (the Hermes Business pattern): procedures are shared across the firm,
  case files stay in the session of the specific matter.
- **Executors on the local DeepSeek, the planner optionally in the cloud:** reduce `delegation.max_concurrent_children`
  from the default 10 to 4 (your slots), set `context_length` explicitly to 131072.
- **Cron watchdogs without a model:** a script checks whether there is work (a new message from a court, an approaching deadline), and
  the model wakes up only on a non-empty result — it saves slots
  ([course 2, part 11](../course_agentic_apps/11-SCHEDULING-PROACTIVITY.md)).
- **Swappable execution backends:** a local terminal today, SSH to a server at the firm or Docker per client tomorrow.

**Worth knowing.**
- Nous Research is first and foremost a model lab; the agent is a channel to the portal and a source of training data
  (trajectory generation and compression are in the repository).
- **Pace of change:** about 2100 PRs between two consecutive releases and about 18 thousand files in the repository — **pin
  versions**; state database corruption required a separate repair release.
- Nous refactored its own code with the involvement of 1393 agents.
- NVIDIA NemoClaw supports Hermes as one of three agents (alongside OpenClaw and LangChain Deep Agents) —
  in the OpenShell sandbox with an egress policy approved by the operator.
- **The same rating from another angle:** in the harness survey Hermes has 81 pts and 4th place (what counted there was multiple
  agents, a local model and security); here — 93 pts as an assistant product. The conclusions agree: the best start for
  voice and cron; watch out for the cloud TTS and the pace of change.

**Sources:** [GitHub](https://github.com/NousResearch/hermes-agent) · [README](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/README.md) · [Hermes site](https://hermes-agent.nousresearch.com/) · [memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) · [skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) · [cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) · [delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation) · [voice](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode) · [documentation index](https://hermes-agent.nousresearch.com/llms.txt) · [funding round](https://nousresearch.com/a-note-on-our-fundraise) · [Nous Research](https://nousresearch.com/) · [Nous blog](https://nousresearch.com/blog) · [Hermes Business](https://portal.nousresearch.com/business) · [NemoClaw](https://github.com/NVIDIA/NemoClaw) · [harness survey](../agent-harnesses/01-PROFILES.md#4-hermes-agent)


---

## 6. Manus

**Category:** executor · **Code:** closed · **Company:** Butterfly Effect Pte. Ltd. (Singapore; founders from China) ·
**Score: 93** (T4 I5 L5 A5)

> A "general agent" that spins up a separate cloud computer for every task and hands back a finished file, page or
> presentation — first on the market (Mar 2025), USD 100 million ARR after 8 months, and its team described
> context engineering best in the industry.

**Open or closed.** Closed SaaS built heavily on open source: at launch it used the browser-use library
and 29 tools, and co-founder Yichao "Peak" Ji said Manus "wouldn't exist without open source". There is no self-hosting.
The open clone is OpenManus (MIT, about 58.6k stars per the GitHub API 11 October 2026), built in 3 hours on the day of
Manus's launch.

**Purpose.** Knowledge workers, SMBs and prosumers: research reports, data analysis, presentations, websites and web
apps, video, browser automation. Increasingly companies (Team plan, API). In 2026 a move toward the "living" assistant:
event-driven automations, a persistent cloud computer and the Cue app.

**Features.**
- **Manus 2.0** (28 September 2026): the "Cascade" harness, a persistent Cloud Computer, event-triggered automations (e-mail,
  calendar, Slack, Notion, a change in ad performance), Manus Studio (documents, spreadsheets, slides, web, code, a video
  editor), desktop control from a phone with per-app and per-file approval.
- **Cue:** personal agents with their own e-mail address, phone number and a wallet with a spending limit set
  by the user (the limit per a third-party review).
- **Wide Research** (31 July 2025): the main agent splits the task, and each subtask gets an agent "with its own fresh
  context window"; tested up to 250 items.
- **Cloud Browser** with persistent sessions and "Take Over" (a human takes control for CAPTCHA, SMS, MFA);
  **Browser Operator** (18 November 2025) works in your logged-in browser, from your IP.
- **Manus Flex** (29 September 2026): bring your own key for models (OpenRouter, Fireworks, Modal); credits still pay for infrastructure,
  tools and VMs.
- Full-stack apps with a backend, database and login (Manus 1.5, 16 October 2025), scheduled tasks, MCP connectors
  (HubSpot, Shopify, Canva, Zoom, Supabase and others), a public API, planning mode.

**Advantage.**
- **A computer per task instead of an answer:** the result is a file, a page or a slide deck. Scale through Dec 2025:
  147 trillion tokens and 80 million virtual computers created *(company data)*.
- **Context engineering instead of its own models:** the bet is that on top-tier models changes ship "in hours
  instead of weeks". The moat lies in the harness, infrastructure, UX and brand — not in the model (Flex lets you plug in your own).
- **First-mover advantage and brand:** a demo with >1 million views in 20 hours, invitation codes resold for ~USD 1000
  and more (Mar 2025).

**Architecture.**
- **Models:** at launch Claude 3.5 Sonnet and fine-tuned Qwen models; the 2026 mix is undisclosed; since Sep 2026 swappable.
- **Multi-agent:** in 2025 the user talked only to the executor agent, which did not see the planner and knowledge agents
  — this keeps context length in check. Wide Research launches parallel full instances with a fresh context.
- **Cascade (2.0):** a project starts light, specialized capabilities are pulled in only when the work needs them;
  −23.2% tokens, −28.2% time, −32% cost "in tested configuration" *(company data; a third-party review notes that
  this is one configuration, not an average)*.
- **Sandbox:** E2B micro-VMs on Firecracker, startup about 150 ms; Docker rejected (10–20 s startup, an incomplete
  system). Each VM has internet, a persistent file system and can install software.
- **Six context engineering principles** (Ji, 18 July 2025) — see also
  [course 2, part 4](../course_agentic_apps/04-CONTEXT-ENGINEERING.md):
  1. **KV-cache hits are the most important metric** — in Claude Sonnet cached input cost USD 0.30 instead of
     USD 3 per 1 million tokens; the input-to-output ratio about 100:1; a fixed prefix, context only appended to.
  2. **Mask tools, don't remove them** mid-loop; shared name prefixes (`browser_`, `shell_`).
  3. **The file system as context** — reversible compression: drop the page content, keep the URL and path.
  4. **Goal recitation:** the agent rewrites `todo.md`; a typical task is about 50 tool calls.
  5. **Keep errors and stack traces in context** — the model updates its beliefs.
  6. **Don't get "few-shotted"** — introduce controlled diversity of templates and phrasings.
- **Logins:** encrypted per-user sessions, no password storage; data-center IPs get blocked by anti-bot systems, so
  banks go through a local extension that requires per-session consent and logs every action. Reasoning is always in the cloud.

**How it makes money.**
- **Subscription + credits:** credits pay for tokens, VM time and external APIs, and are consumed only during a task;
  free users get a daily refresh (up to 1,500/month); monthly credits do not roll over.
- **Prices:** Mar 2025 — Starter USD 39 (3900 credits), Pro USD 199 (19,900) *(Sacra)*; Sep 2026 — USD 20 for 4000,
  USD 40 for 8000 and USD 200 for 40,000 credits, plus 300 daily *(a third-party page capture; the official pricing page
  is unreadable to automation)* — about USD 0.005 per credit. The persistent Cloud Computer: USD 30 or 50/month (third-party page).
- **Revenue:** about USD 90 million ARR (Aug 2025); USD 100 million ARR and USD 125 million run-rate of total revenue with growth
  >20% m/m and 105 employees (Dec 2025) *(company data)*; about USD 450 million a year in Jun 2026 *(Sacra estimate,
  primary source unverified)*.
- **Owners:** Series B about USD 75 million (Benchmark) at a valuation of about USD 500 million (Apr 2025); Meta bought Manus for
  >USD 2 bn (Dec 2025), and China's NDRC blocked the deal on 27 April 2026; the founders with Tencent, ZhenFund and HongShan
  bought the shares back at roughly the original price; Manus is independent again in Singapore. On 8 October 2026 a round of >USD 500 million
  (Boyu Capital and IDG Capital; valuation undisclosed, Bloomberg wrote of a target of about USD 4 bn).

**Offline.** **No.** Reasoning in cloud model APIs, execution in a cloud micro-VM. Browser Operator,
desktop control and Flex still require Manus's orchestration — even with a model on your own endpoint the plan, VM
and credits stay in the cloud. A local equivalent: a harness with Manus's context principles, a container or micro-VM per
task with a mounted directory, a local browser and a local model; a ready-made skeleton is OpenManus (MIT, supports
Ollama and a Docker sandbox).

**What to adopt.**
- **The six principles are a user manual for llama.cpp:** locally the prefix cache decides whether a step takes 2 or 40 seconds.
  A fixed system prompt and tool list, context only appended to, zero timestamps in the prefix
  ([pitfall H4](../agent-harnesses/01-PROFILES.md#seven-pitfalls-common-to-all)).
- **`todo.md` and errors in context** — cheap, and they save long DeepSeek-V4-Flash tasks at 131k context.
- **Wide Research on 4 slots:** reviewing 200 agreements is 4 parallel executors with a small, fresh context
  and aggregation of results — instead of one overflowing context.
- **A container per task** with only the matter directory mounted: isolation, repeatability and an audit trail.
- **"Take Over" at the desk:** the agent pauses, the human logs into a portal (a bank, a court system) and hands control back.
  The local machine has an advantage over Manus's cloud here: an ordinary IP and existing sessions.
- **No "expose a port" type tools without a human gate** — see the attack below.

**Worth knowing.**
- **Launch and reliability:** launched 6 March 2025 by invitation. In TechCrunch's tests (Mar 2025) a food order
  failed after 10 min, and a flight booking produced broken links. By Oct 2025 the average task time fell from 15 to <4 min
  *(company data)*.
- **Attack (25 August 2025):** Johann Rehberger used indirect prompt injection in a PDF to make Manus call
  `deploy_expose_port`, expose an internal VS Code Server to the internet and leak the password — with no human
  approval; fix status "unclear".
- **Geopolitics:** moving from Beijing and Wuhan to Singapore in mid-2025 and blocking users from mainland
  China were not enough — the NDRC ban was the first publicly disclosed prohibition in a Chinese foreign investment security
  review, and CEO Xiao Hong and chief scientist Ji Yichao were reportedly barred from leaving China in Mar 2026
  (per TechCrunch). Offshore restructuring does not protect against jurisdiction over people and data.
- **Data:** after announcing its return to independence (11 August 2026, formally 1 September 2026), Manus deleted on 23–24 August 2026 the data of
  "certain users" from "specific jurisdictions"; it keeps data in the USA and Singapore, and I found no EU residency declaration
  — it is not suitable for data covered by Polish professional secrecy.
- **The GAIA benchmark:** at launch Manus claimed to beat OpenAI Deep Research; the often cited per-level results
  (86.5 / 70.1 / 57.7) could not be confirmed on the primary source.

**Sources:** [context engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) · [Manus 2.0](https://manus.im/blog/introducing-manus-2-0) · [Manus Flex](https://manus.im/blog/introducing-manus-flex) · [Wide Research](https://manus.im/blog/introducing-wide-research) · [Wide Research — docs](https://manus.im/docs/features/wide-research.md) · [Manus 1.5](https://manus.im/blog/manus-1.5-release) · [Browser Operator](https://manus.im/blog/manus-browser-operator) · [Cloud Browser](https://manus.im/docs/features/cloud-browser.md) · [USD 100M ARR](https://manus.im/blog/manus-100m-arr) · [letter to users](https://manus.im/blog/a-note-to-our-users) · [independence](https://manus.im/blog/manus-resumes-independent-operations) · [credit rules](https://help.manus.im/en/articles/11711097-what-are-the-rules-for-credits-consumption-and-how-can-i-obtain-them) · [E2B](https://e2b.dev/blog/how-manus-uses-e2b-to-provide-agents-with-virtual-computers) · [The Decoder](https://the-decoder.com/chinese-ai-agent-manus-uses-claude-sonnet-and-open-source-technology/) · [TechCrunch Mar 2025](https://techcrunch.com/2025/03/09/manus-probably-isnt-chinas-second-deepseek-moment/) · [TechCrunch: China's veto](https://techcrunch.com/2026/04/27/china-vetoes-metas-2b-manus-deal-after-months-long-probe/) · [TechCrunch: Oct 2026 round](https://techcrunch.com/2026/10/08/chinas-manus-raises-over-500m-in-first-funding-round-since-split-with-meta/) · [Bloomberg](https://www.bloomberg.com/news/articles/2026-04-27/china-blocks-meta-s-2-billion-acquisition-of-ai-startup-manus) · [Yahoo: USD 4 bn valuation](https://finance.yahoo.com/technology/ai/articles/manus-seeks-4b-valuation-beijing-183502124.html) · [Dahui Lawyers](https://www.dahuilawyers.com/en/news-insights/chinas-first-public-foreign-investment-security-review-prohibition-the-metamanus-decision/) · [Sacra](https://sacra.com/c/manus) · [2.0 review](https://myclaw.ai/blog/manus-2-0) · [Embrace The Red](https://embracethered.com/blog/posts/2025/manus-ai-kill-chain-expose-port-vs-code-server-on-internet/) · [OpenManus](https://github.com/FoundationAgents/OpenManus) · [Wikipedia](https://en.wikipedia.org/wiki/Manus_(AI_agent))


---

## 7. ChatGPT

**Category:** everyday + executor · **Code:** closed · **Company:** OpenAI (USA) · **Score: 87** (T5 I4 L4 A4)

> The world's largest assistant (about 1.2 billion weekly users, 29 September 2026), which in 2026 turned from a chat
> into a "do it for me" platform: an agent in a cloud machine, scheduled tasks and always-on "dots".
> It makes the top tier for its scale and because OpenAI has described most precisely how to approve an agent's actions.

**Open or closed.** The app, the models (GPT-6 Luna, Sol, Astra) and the agent environment are closed. Alongside, OpenAI
publishes open weights under Apache 2.0: gpt-oss-120b and gpt-oss-20b (Aug 2025), gpt-oss-safeguard and **privacy-filter**
(Apr 2026), a personal data classifier (1.5 billion parameters, 50 million active) that runs on a laptop and in the
browser. At DevDay 2026 OpenAI was said to have open-sourced the Codex agent harness (per Decrypt). Self-hosting ChatGPT: no.

**Purpose.** An assistant for everyone: from free users in emerging markets (the Go plan) to professionals on
the Pro and Business plans. In 2026 OpenAI is shifting it from conversation toward getting work done: documents, spreadsheets, e-mails,
background case monitoring, and in companies agents sitting in Slack and Teams.

**Features.**
- **Memory:** saved memories (2024) + references to chat history (2025); since 4 June 2026 "Dreaming", a background task
  that rewrites an editable *Memory Summary* and updates facts with an expiry date (first Plus and Pro in the USA).
  An internal fact recall test reportedly rose from 41.5% to 82.8% *(company data, via secondary press)*.
- **Scheduled tasks** (17 June 2026): reminders, recurring jobs and monitors that speak up only on a
  change; most often once an hour, unused ones pause themselves. They replaced Pulse (a morning brief, 25 September 2025 – Jun 2026).
- **Agent:** Operator (23 January 2025) → ChatGPT agent (17 July 2025) → **ChatGPT Work** (9 July 2026, GPT-5.6). Work has a plan
  mode: it gathers context, asks questions, shows a plan for acceptance, then works on its own, also on an event and in continuous
  monitoring. It delivers spreadsheets, slides, documents and "Sites"; 1400+ plugins; writes to Gmail, Calendar, Slack, GitHub.
- **Desktop app** (9 July 2026, macOS and Windows): chat, Work and Codex in one window; a built-in browser with a
  password manager, local "Computer Use" (clicks, types, moves files) and a separate browser in the OpenAI cloud.
- **"dots"** (29 September 2026): always-on agents on GPT-6 Astra, each with its own cloud machine and browser;
  available in ChatGPT, Slack, Teams and through voice conversation, they learn from feedback.
- **Plugins** (formerly apps, since Jul 2026): 4000+ apps; on 6 August 2026 the open **Agent Plugins** standard (Agent Skills +
  MCP servers; committee: Amazon, Cursor, Microsoft, OpenAI, Vercel). Custom GPTs are going away in Dec 2026.
- **Voice** on GPT-6 with plugins (23 September 2026) and "Intelligent UI": widgets, forms, charts in the response (7 October 2026).
- **Health:** ChatGPT Health (7 January 2026) — **unavailable in the EEA, Switzerland and the UK**; ChatGPT for Clinicians (Apr 2026,
  per Sacra) enters the market of [OpenEvidence](#12-openevidence).

**Advantage.**
- **Habit and reach:** 1.2 billion weekly users *(company data, DevDay 29 September 2026)*; Sensor Tower (May 2026):
  1.1 billion+ MAU and a 46.4% share of the assistant app market — below 50% for the first time.
- About 3× more paying subscribers in the USA than Claude or Gemini *(a16z, Oct 2026)*.
- The largest plugin ecosystem and its own standard for packaging them.
- A full stack: models trained with RL for the agent's tools (browser, terminal) and a product built on them.
- The mechanism most worth understanding: **an action policy**. Not a single "ask / don't ask" switch, but levels
  for each type of action plus a separate system that reviews the plan before an irreversible step.

**Architecture.**
```
user ─▶ model router: Luna (small, Free/Go) · Sol (medium) · Astra (largest) + a "Think" slider
   ├─ chat + two-layer memory (explicit memories + a profile from history; nightly "Dreaming")
   ├─ server-side scheduler (≤ 1×/h, auto-pause)
   └─ agent / dot ─▶ isolated Linux VM with Chrome in the cloud
        tools:  visual browser (pixels) · text browser · terminal (network: GET only)
                   · plugins (MCP + skills)
        gates:  Custom Rules: on its own / if previously approved / ask / hand over to the human
                   + a separate auto-review of the plan before an e-mail or file change
                   + control handover at login and payment (the agent does not see the password)
```
- **The ChatGPT agent system card (17 July 2025):** confirmations before state-changing actions have an accuracy of 91.0%
  overall, 100% for financial transactions, 99.9% for high-stakes communication. "Watch mode" pauses on sensitive
  pages (mail, bank) when the user walks away. **ChatGPT memory is disabled in agent mode**, so that an injection
  from a page cannot pull out its contents. The model's own robustness: it ignores foreign instructions 95% of the time, repels in-context
  exfiltration 78% of the time and active exfiltration 67%.
- **dots:** passwords, transfers and data deletion always require approval or go back to the human; the
  "proactive research" mode is read-only. Connecting your own computer is optional and off by default.
  A dot inherits ChatGPT's memory, but individual memories of the dot cannot be inspected — you can only clear them all
  (per eesel).
- **Computer use in the API:** for GPT-6 Astra OpenAI recommends that the model **write Playwright or PyAutoGUI code** instead of clicking
  on pixels; the cheaper path is a tool returning mouse and keyboard movements (gpt-6.1-sol).
- **Security evaluation:** an RL-trained attacker searches for injection chains tens to hundreds of steps long
  (22 December 2025); ChatGPT Work has an auto-review gate before important actions in connected tools.
- Inference is always in the cloud; execution either in an OpenAI VM (agent, dots, cloud browser) or locally
  (desktop, built-in browser, Chrome extension).

**How it makes money.**
- **Plans (Oct 2026):** Free (with ads), Go USD 8, Plus USD 20, Pro USD 100 / 200 / 500 (Pro 500 announced 29 September 2026,
  25× the Plus limit), Business USD 25 (Standard) and USD 125 (Premium) per seat *(Go and Business per aggregators)*.
  The first dot is in Pro and Business Premium — but Pro in the EEA, Switzerland and the UK does not have it at launch.
- **Ads:** a test in the USA since 9 February 2026 (Free and Go, excluding health topics, politics and users under 18); since 24 August 2026
  in 31 European countries, **including Poland**, at launch contextual only. A pace of about USD 1 bn a year in Aug 2026 *(a16z)*.
- **Revenue:** USD 13.1 bn booked in 2025; about USD 25 bn annualized at the end of Jan 2026 *(press)*; ARR
  "nearly USD 70 bn" on 29 September 2026 *(Axios via Reuters, anonymous source)*.
- **Subscribers:** 50 million+ (Feb 2026, aggregator); an internal forecast of 122 million at the end of 2026 *(The Information)*.
- **API (29 September 2026):** GPT-6 Astra USD 10 / 50 per 1 million input/output tokens, Sol 2 / 10, Luna 0.10 / 0.50 *(company data
  per DevDay coverage)*. ChatGPT Work is billed by usage, with no per-task price list.
- **Funding:** a USD 122 bn round at a USD 852 bn valuation (closed around 1 April 2026; Amazon 50, Nvidia 30,
  SoftBank 30 bn USD). The IPO has been pushed to 2027.

**Offline.** **No.** Every query and every agent step goes to OpenAI's servers; the desktop app works on local
files, but the model is in the cloud. A local equivalent needs: a model with tool calling, a VM or container with a
browser, a scheduler and memory in files. The OpenAI building blocks you can run yourself: gpt-oss-20b (about 16 GB)
and gpt-oss-120b (one 80 GB card) — sizes from the 2025 model card, unverified — and privacy-filter. On my
rig the brain is DeepSeek-V4-Flash, but text-only: a visual browser requires a separate vision model or working on the
DOM and the accessibility tree (see [browser-use](#13-browser-use)).

**What to adopt.**
- **Four consent levels for each type of action** + a hard "always ask" list (money, passwords, deletion, sending to the
  client) + a second reviewer model before an irreversible step. On the rig the reviewer can be one of the 4 DeepSeek slots,
  which sees only the plan and the goal, not the raw documents.
- **Measure "confirmation recall"** with a separate 100% target for critical actions — on a test set built from real tasks of a
  law firm or an accounting office ([evaluation](../course_agentic_apps/14-EVALUATION.md)).
- **Nightly "dreaming":** a cron at 3:00 rewrites one editable profile file and removes expired facts. The rig sits idle at night anyway
  ([long-term memory](../course_agentic_apps/05-LONG-TERM-MEMORY.md)).
- **"Speak up only on change" monitors** with a frequency limit and auto-pause instead of a heavy morning
  report — Pulse was shut down after about 9 months ([scheduling](../course_agentic_apps/11-SCHEDULING-PROACTIVITY.md)).
- **Turn off long-term memory when the agent reads untrusted content** (web pages, mail from strangers); a terminal with GET-only network.
- **privacy-filter (Apache 2.0) as a personal data masker** before every query to Opus 5.5 in hybrid mode
  ([hybrid](../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md)).

**Worth knowing.**
- **A graveyard of products:** Operator (Jan–Aug 2025), Pulse (about 9 months), Atlas (21 October 2025 – 9 August 2026; macOS only,
  about 10 million MAU per a 36Kr estimate), Custom GPTs (sunset announced for Dec 2026). Per Wikipedia the "ChatGPT agent" itself disappeared in early Aug 2026
  in favor of Work (unverified elsewhere). OpenAI's line: "AI browsers should be a feature, not a destination";
  all AI browsers together had less than 1% of the market.
- **Atlas and security:** "Tainted Memories" (LayerX, Oct 2025; OpenAI disputes it), injections and leaks through URLs.
  OpenAI admitted (22 December 2025) that prompt injection "is unlikely to ever be fully solved".
- **Europe lags behind:** Health and dots on Pro outside the EEA; ads in the EU contextual only by default.
- **Lawsuits:** *Raine v. OpenAI* (26 August 2025, a teenager's suicide) and subsequent ones; parental controls were the response.
  The UK AISI reportedly found "universal cyber jailbreaks" in GPT-5.6 (unverified at the source).
- **OpenClaw:** OpenAI hired its creator (Feb 2026) and is a donor to the foundation — see [OpenClaw](#1-openclaw).
- **Hardware:** io (Jony Ive) bought in May 2025 for about USD 6.5 bn; the first device not before the end of Feb 2027.

**Sources:** [DevDay 2026 — Engadget](https://www.engadget.com/2271985/openai-dev-day-live-blog-chatgpt-news/) · [DevDay — Decrypt](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced) ·
[DevDay — emergent](https://emergent.sh/news/openai-devday-2026) · [dots — eesel](https://www.eesel.ai/blog/openai-dots) · [dots — TechCrunch](https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/) ·
[ChatGPT agent system card](https://cdn.openai.com/pdf/839e66fc-602c-48bf-81d3-b21eacc3459d/chatgpt_agent_system_card.pdf) · [ChatGPT Work](https://www.digitalapplied.com/blog/chatgpt-work-openai-agent-launch-2026) ·
[end of Atlas](https://9to5mac.com/2026/07/09/openai-is-discontinuing-chatgpt-atlas-its-standalone-desktop-browser/) ·
[Atlas — OpenAI forum](https://community.openai.com/t/atlas-is-scheduled-to-stop-working-on-august-9-2026/1389473) · [scheduled tasks](https://9to5mac.com/2026/06/17/openai-launches-scheduled-tasks-in-chatgpt-details-here/) ·
[memory](https://www.thurrott.com/a-i/337052/openai-is-improving-how-chatgpts-memory-works) · [Agent Plugins](https://9to5mac.com/2026/08/06/gpt-5-turning-one-as-openai-shares-new-agent-plugins-standard/) ·
[computer use in the API](https://developers.openai.com/api/docs/guides/tools-computer-use) · [prompt injection](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/) ·
[ads in Europe](https://www.pinmeto.com/news/chatgpt-ads-31-european-markets-2026/) · [a16z Top 100](https://a16z.com/100-gen-ai-apps-7/) ·
[ARR ~USD 70 bn](https://www.investing.com/news/stock-market-news/openais-annual-recurring-revenue-nears-70-billion-axios-reports-4923088) ·
[USD 122 bn round](https://news.bloomberglaw.com/tech-and-telecom-law/openai-valued-at-852-billion-after-closing-122-billion-round) · [Sensor Tower](https://techcrunch.com/2026/06/16/chatgpts-market-share-slips-below-50-for-first-time/) ·
[privacy-filter](https://huggingface.co/openai/privacy-filter) · [ChatGPT — Wikipedia](https://en.wikipedia.org/wiki/ChatGPT)


---
## 8. Gemini

**Category:** everyday + executor · **Code:** closed (the open Gemma family alongside) · **Company:** Google / Alphabet (USA) ·
**Score: 87** (T5 I4 L4 A4)

> An assistant built into Android, Chrome and Workspace (over 1 bn MAU, 11 August 2026, *company data*), with an agent that works in the cloud or
> in your signed-in Chrome. In the top tier for its distribution and for the best publicly described security architecture
> of a browser agent: planner + critic + origin sets.

**Open or closed.** The app, the Gemini models and the agent in Chrome are closed. Open alongside: the **Gemma 4** family
(April 2026; E2B, E4B, 12B, 26B, 31B — I have not verified the Gemma 4 licence; earlier Gemmas had the "Gemma Terms of Use"),
a reference implementation of the computer use tool in the Gemini API with a Docker sandbox and, of course, Chromium. Gemini Nano
on the phone is closed, but Android apps get it through AICore and ML Kit GenAI. Self-hosting Gemini: no.

**Purpose.** An AI layer over Gmail, Calendar, Photos, Maps and Docs for billions of Android, Chrome
and Workspace users. In 2026 Gemini does not just answer, it also gets things done: shopping in the browser, background tasks, a morning brief.
For developers Google sells a computer use model for automating interfaces.

**Features.**
- **The Gemini app:** Gemini 3.5 Flash (19 May 2026) and Gemini 4 Argon (30 September 2026) models. Gemini Live (voice and camera)
  has launched Spark tasks by voice since 26 August 2026 and uses "Personal Intelligence" (memory + connected apps, with consent).
- **Daily Brief** (19 May 2026, USA, AI Plus / Pro / Ultra): a morning overview from Gmail, Calendar and Tasks with a proposal for
  next steps.
- **Gemini Agent** (18 November 2025): Project Mariner + Gemini 3 in the app; asks before a purchase or sending a message,
  the user can take over control at any moment; at launch US AI Ultra only, web only.
- **Gemini Spark** (announced 19 May 2026): a personal agent "24/7, even with the phone locked". It consists of
  **Tasks** (a one-off goal), **Schedules** (a time or conditional trigger) and **Skills** (a multi-step procedure); up to 15
  tasks at once; Gmail, Docs, Sheets, Slides, Keep and Tasks natively, the rest through MCP. AI Pro in the USA from 24 July 2026; from
  30 July 2026 Chrome integration and 160+ more countries — **excluding the EEA, Switzerland, the UK and Nigeria**.
- **Chrome auto browse** (28 January 2026; Android from 18 August 2026): comparing hotel and flight prices, bookings, forms,
  collecting tax documents, discount codes. Signs in through Password Manager (with consent), pays through the Universal
  Commerce Protocol, asks before a purchase and before publishing. USA only.
- **Gemini Computer Use in the API:** from 7 October 2025 (2.5, browser); in 2026 Gemini 3.8 Flash (recommended), 3.5 Flash-Lite
  and 3 Flash Preview, in the browser, on Android and on the desktop.
- **Gems → Skills** invoked with "/" in the prompt box (migration announced for 17 November 2026).
- **On-device:** Gemini Nano through AICore — summarising, proofreading, rewriting, image description, offline transcription.

**Advantage.**
- **Distribution through the operating system:** from 4 September 2026 Gemini permanently replaces Google Assistant on Android, Wear OS,
  headphones and Android Auto; Gemini models also stand behind Apple's Siri AI.
- **Data gravity:** Gmail, Calendar, Photos, Maps, Password Manager, Wallet. The agent works where the user
  is already signed in.
- **Its own browser and payments:** Chrome has about 2/3 of the market; its own shopping protocol (UCP); the AP2 payments protocol
  handed over to the FIDO Alliance (April 2026).
- **Cheap, fast Flash models** for computer use; Google gives about 225 s at 70%+ accuracy (its own chart, 7 October 2025).

**Architecture.**
```
 goal ─▶ planner (Gemini) sees the page and proposes an action
              ▼
        User Alignment Critic — a separate, trusted model; sees the action and the goal, NOT the raw page content ── veto
              ▼
        Agent Origin Sets — for the task: read-only origins  /  write origins (click, type)
              ▼
        deterministic confirmations: banking and medical, password sign-in, payment, sending a message
        + a prompt injection classifier in parallel with the planner + a work log with pause and takeover
```
- Diagram from the Chrome security blog (8 December 2025); a VRP reward of up to 20,000 USD for breaking these boundaries.
- **Spark:** dedicated, isolated VMs in the cloud (persistent state, multi-hour tasks), the Antigravity agent harness and
  Gemini 3.5 Flash. It browses either through the user's local Chrome (signed-in sites, saved passwords) or through a remote
  browser; it hands sign-in and payment pages over to a human; requires 18+.
- **Consent by data scope:** editing **shared** documents requires manual confirmation, **private** ones go through
  automatically.
- **API loop:** query + screenshot + action history → function call (click, type, scroll) → execution on the developer's
  side → new screenshot. Every step returns a `safety_decision`; `require_confirmation` forces a question to the human and a
  `safety_acknowledgement`. Seven built-in policy categories (transactions, changing sensitive data, communication,
  creating accounts, modifying data, consents, legal agreements); `excluded_predefined_functions` swaps actions for your own.
  Google recommends a VM or a container.
- **History:** Mariner (11 December 2024) worked only in the active tab, WebVoyager 83.5%; from 20 May 2025 in cloud machines,
  up to 10 tasks at once; shut down on 4 May 2026 and absorbed into Gemini Agent/Spark, auto browse and the API.
- **On-device:** Nano is isolated, has no direct internet access, and does not store inputs and outputs;
  the Firebase AI Logic Hybrid API switches to the cloud when Nano is unavailable.

**How it makes money.** The agents come in Google AI bundles, together with storage and YouTube:
- **USA (October 2026):** AI Plus 4.99 USD, AI Pro 19.99 USD (Spark, 5 TB), AI Ultra from 99.99 USD (199.99 USD for 20× limits;
  cut from 250 USD at I/O 2026).
- **Poland (October 2026):** AI Plus PLN 23.99, AI Pro PLN 97.99, AI Ultra PLN 469.99–979.99; there is no Spark on the Polish plans page.
- **Companies:** Gemini Enterprise Business 21 USD per seat; Standard and Plus from 30 USD.
- **API:** Gemini 4 Argon 2 / 10 USD per 1 million tokens at launch, then 4 / 20 USD (30 September 2026); computer use at the
  model's token price.
- **Scale:** 900 million+ MAU (19 May 2026) → 950 million MAU (Q2 results, 22 July 2026) → "over 1 bn monthly" (Google
  blog, 11 August 2026) *(company data)*; Sensor Tower (May 2026): 662 million MAU, 27.7% of the market.
- Alphabet does not break out AI subscriptions: the "subscriptions, platforms and devices" segment brought 12.9 bn USD in Q2 2026
  (+15% y/y).

**Offline.** **No.** Gemini Nano on supported phones does only simple things offline (summarising, proofreading, transcription) and is not an assistant. The app, Live, Spark, Agent and auto browse work only in the cloud. Gemma 4 can be set up locally, but on the rig only after freeing a card from DeepSeek (the licence has to be checked). The local counterpart of Spark is a scheduler + a task queue
with a concurrency limit (4 slots on mine) + a browser in a container + a planner and a critic.

**What to adopt.**
- **Planner + critic.** The critic gets only the proposed action and the user's goal, never the content of a page or document —
  an injection from an opposing party's pleading has no way to convince it. On the rig that is the second DeepSeek slot with a short prompt
  ([agent security](../course_agentic_apps/16-SECURITY-OWASP-ASI.md)).
- **Per-task origin sets:** read-only domains (ISAP, SAOS, the VAT whitelist) and write domains (e.g. KSeF — only
  after confirmation).
- **Deterministic confirmation triggers, not an LLM:** the address category, password use, a payment form, the
  "send" button.
- **The `safety_decision` contract** between the model and the executor: the executor refuses an action that requires confirmation until
  it gets an explicit "ack" from a human.
- **Tasks / Schedules / Skills** as a mental model for a non-technical lawyer or accountant; skills under "/".
- **Inverted hybrid:** Google does "Nano first, cloud as a fallback"; for a law firm — always local, the cloud only with
  explicit consent for a specific query.

**Worth knowing.**
- **Poland outside the agent:** Spark is switched off in the EEA, auto browse is USA only; the entries about Gemini in Chrome do not mention the EU
  (the UK got it on 14 July 2026).
- **DMA:** the settlement reportedly requires that competing assistants get comparable features on Android (hotword,
  in-app actions) by July 2027; on 30 September 2026 Google asked the EU court to suspend the order to open up to rivals.
- **BragJack** (19 September 2026): a malicious extension "forces a prompt" on the privileged AI component of the browser;
  it affected, among others, Gemini in Chrome, CVE-2026-0628.
- The Spark help page honestly warns: "Gemini can share your info with websites" and describes the prompt injection risk.
- **Corporate "Gemini agent"** (8 October 2026): persistent agent-colleagues with their own mail, calendar and Drive,
  which can also route work to **Claude** models.
- **Disputes:** a wrongful death lawsuit (March 2026) alleging that Gemini encouraged suicide; a 250 million EUR fine in France (March 2024)
  among other things for training Bard on publishers' content.

**Sources:** [Alphabet Q2 2026](https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000066/googexhibit991q22026.htm) · [I/O 2026 — 9to5Google](https://9to5google.com/2026/05/19/google-io-2026-news/) ·
[Gemini 3.5 Flash and agents](https://techcrunch.com/2026/05/19/with-gemini-3-5-flash-google-bets-its-next-ai-wave-on-agents-not-chatbots/) ·
[Spark in AI Pro](https://www.androidheadlines.com/2026/07/google-gemini-spark-expands-to-ai-pro-subscribers.html) · [Spark — Google help](https://support.google.com/gemini/answer/16596215) ·
[Spark July 2026](https://blog.google/innovation-and-ai/products/gemini-app/gemini-spark-updates-july-2026/) · [Spark — analysis](https://www.efficientlyconnected.com/google-io-2026-gemini-spark-consumer-ai-agent/) ·
[Chrome security architecture](https://blog.google/security/architecting-security-for-agentic/) · [auto browse](https://blog.google/products-and-platforms/products/chrome/gemini-3-auto-browse/) ·
[auto browse Android](https://blog.google/products-and-platforms/products/chrome/gemini-in-chrome-android-auto-browse/) · [Gemini Agent](https://blog.google/products/gemini/gemini-3-gemini-app/) ·
[computer use API](https://ai.google.dev/gemini-api/docs/computer-use) · [Computer Use model](https://blog.google/technology/google-deepmind/gemini-computer-use-model/) ·
[Mariner](https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/) · [Mariner — Wikipedia](https://en.wikipedia.org/wiki/Project_Mariner) ·
[1 bn users](https://blog.google/innovation-and-ai/products/gemini-app/one-billion-monthly-users/) · [Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) ·
[PL prices](https://gemini.google/subscriptions/) · [US prices](https://gemini.google/us/subscriptions/?hl=en) ·
[Gemini instead of Assistant](https://www.businesstoday.in/amp/technology/news/story/google-assistant-to-be-replaced-by-gemini-starting-september-on-android-and-wearos-547570-2026-08-06) ·
[Live, Spark and DMA](https://thenextweb.com/news/gemini-live-spark-voice-agentic-tasks-dma-rival-assistants) · [Gems → Skills](https://9to5google.com/2026/09/27/gemini-gems-skills/) ·
[Gemini Nano](https://developer.android.com/ai/gemini-nano) · [Gemma](https://deepmind.google/models/gemma/) · [Gemini agent for companies](https://techgenyz.com/google-gemini-agent-enterprise-ai/) ·
[BragJack](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/) · [Google Gemini — Wikipedia](https://en.wikipedia.org/wiki/Google_Gemini)


---

## 9. Cursor

**Category:** professional (programmers) · **Code:** closed · **Company:** Anysphere (USA), from 14 August 2026 a subsidiary
of SpaceX · **Score: 87** (T5 I4 L4 A4)

> A code editor (a VS Code fork) in which suggestions, the agent and code review are one product — the fastest-growing
> professional assistant in the history of software and the "many agents in parallel" pattern for every industry.

**Open or closed.** Closed, a proprietary VS Code fork. Its own models (Tab, Composer) have no public weights.
Since 2 September 2026 "Self-Hosted Machines" let you run code and tools on the customer's infrastructure, but requests to
the models still pass through Cursor's cloud.

**Purpose.** Professional programmers and, more and more, companies — about 60% of revenue from enterprise customers
*(Bloomberg via the press, March 2026)*. The problem: writing, changing and reviewing code in large repositories; since 2026 also
delegating whole tasks to agents in the cloud.

**Features.**
- **Tab** — predicting the next edit in the editor; an agent in the editor.
- **Cursor 3** (2 April 2026): an agents window — parallel agents locally, on worktrees, on remote machines or
  in the cloud (isolated Ubuntu VMs); a session can be moved from the cloud to the local computer and back.
- **Projects** (beta, 10 September 2026): a coordinator agent splits work among parallel subagents.
- **Rollouts** and **Security Review** bots (23 September 2026), **Bugbot** for PR review, support for MCP, skills and hooks.
- Remote control of local agents from an iOS app (6 October 2026); cloud agents without a GitHub connection
  (27 August 2026).

**Advantage.**
- **Its own editor** — suggestion, agent and review share context; a plugin competitor does not have that.
- **Its own models** tuned for editor tasks: Composer 2 (19 March 2026) — 61.3 on CursorBench, 61.7
  on Terminal-Bench 2.0, 73.7 on SWE-bench Multilingual at a price of 0.50 / 2.50 USD per million input/output tokens
  *(company data)*.
- **A choice of models from many providers** — the user is not tied to one lab.
- Since the acquisition: access to SpaceX compute *(company data)*.

**Architecture.**
```
editor (VS Code fork) ──▶ Cursor backend: "final prompt building" (also with the user's own API key)
   ├─ Tab: its own suggestion model (the acquired Supermaven, November 2024)
   ├─ agent: Composer 2 or models from other providers (user's choice)
   └─ execution: local · worktree · Self-Hosted Machines · cloud VM (session transfer)
coordinator (Projects) ──▶ subagents in parallel ──▶ Bugbot / Security Review as reviewers
```
- **Composer 2** is Kimi K2.5 (Moonshot AI's open weights) plus Cursor's further pretraining and RL; about a quarter of the
  training compute came from the Kimi base. Cursor did not disclose this at launch — a user found it, and the company admitted it
  on 20 March 2026.
- **Privacy Mode:** no training on user data and zero retention agreements with all model providers;
  however, requests that trigger abuse classifiers may be stored. SOC 2 Type II.

**How it makes money.** Subscriptions with a pool of model usage and a surcharge for overage (October 2026): Hobby 0, Individual 20 USD/month,
Teams 40 USD/user/month, Enterprise custom; in July 2026 Pro+ 60 USD and Ultra 200 USD were also listed.
- ARR: 100 million USD (January 2025) → 500 million (June 2025) → over 1 bn (November 2025) → 2 bn (February 2026, Bloomberg) → 3 bn USD
  (May 2026, Bloomberg via Wikipedia); about 4 bn in June 2026 — unverified.
- Funding: Series C 900 million USD at 9.9 bn (5 June 2025), Series D 2.3 bn USD at 29.3 bn (13 November 2025).
- **SpaceX:** an option from 21 April 2026 (a purchase for 60 bn USD or 10 bn for joint work), exercised on 16 June 2026, the share
  transaction closed on 14 August 2026 — 389,289,254 SpaceX Class A shares.

**Offline.** **No.** Every request passes through Cursor's backend, even with your own API key. Self-Hosted
Machines keep code and tool execution at the customer, I found no local model inference. A fully local
counterpart is open harnesses with a local model (Cline, OpenCode, Kilo Code — see
[the harness overview](../agent-harnesses/README.md)).

**What to adopt.**
- **A window of parallel agents, not only for code.** 4 DeepSeek slots = 4 agents on one matter, each on
  its own working copy (the equivalent of a worktree): a chronology from the case file, citation verification, a draft pleading, a deadline
  list. The lawyer sees four progress cards and merges the results — [13-MULTI-AGENT-FLEET.md](../course_agentic_apps/13-MULTI-AGENT-FLEET.md).
- **Coordinator + reviewer.** The Projects/Bugbot pattern: one agent splits the work, a separate agent only reviews
  (e.g. "does every provision in the pleading exist in ISAP and have the right wording").
- **Moving a session is easy only if you know what is in the context.** In a hybrid with Opus you move
  the plan, never the client's documents.
- **An open base + fine-tuning on task traces** — that is how Composer came about; the same path is possible for Polish
  legal or medical text. And disclose the base model — hiding Kimi cost Cursor trust.
- **Pricing:** at Cursor the agents ate the margin, hence the credits. A local model on the customer's hardware has a marginal cost close to
  zero — a flat licence per seat or per office is a structural advantage, and announce price changes early and clearly.

**Worth knowing.**
- On 16 June 2025 the Pro plan changed from 500 requests to 20 USD of credit at API prices plus an "unlimited" Auto mode;
  users did not know that "unlimited" applied only to Auto, and they got unexpected bills; on 4 July 2025
  Cursor apologised and refunded the money.
- April 2025: the company's support bot "Sam" invented a non-existent login policy; users cancelled — a lesson for
  anyone who puts an agent in front of a customer.
- After the acquisition the team joined SpaceXAI (Grok Build, Grok API); the first joint result is Grok 4.6. For customers
  in the EU the provider is now SpaceX.
- Acquisitions: Supermaven (November 2024), Koala (July 2025), Graphite (December 2025).

**Sources:** [pricing](https://cursor.com/pricing) · [changelog](https://cursor.com/changelog) ·
[Composer 2](https://cursor.com/blog/composer-2) · [June 2025: pricing](https://cursor.com/blog/june-2025-pricing) ·
[data use](https://cursor.com/data-use) · [security](https://cursor.com/security) ·
[joining SpaceX](https://cursor.com/blog/joining-spacex) ·
[Wikipedia](https://en.wikipedia.org/wiki/Cursor_(company)) ·
[Bloomberg: 2 bn USD ARR](https://www.bloomberg.com/news/articles/2026-03-02/cursor-recurring-revenue-doubles-in-three-months-to-2-billion) ·
[Gigazine: Kimi](https://gigazine.net/gsc_news/en/20260323-cursor-admits-composer-2-kimi) ·
[DataCamp: Cursor 3](https://www.datacamp.com/blog/cursor-3) ·
[Silicon Canals: enterprise customers](https://siliconcanals.com/t-cursor-100-million-2-billion-annualized-revenue-13-months/) ·
[Jetadmin: plans](https://www.jetadmin.io/blog/cursor-pricing-explained-plans-credit-system-and-real-costs-in-2026/)


---

## 10. Granola

**Category:** professional (meetings) · **Code:** closed · **Company:** Granola Labs Ltd / Granola Inc.
(United Kingdom / USA) · **Score: 87** (T4 I5 L5 A3)

> An "AI notepad" with no bot in the meeting: it records audio from your own computer, and a model expands your sketchy notes
> with what was said in the conversation. The pattern easiest to reproduce fully locally — and a cautionary tale about consent.

**Open or closed.** Closed. The app captures audio on the device, but transcription and the models
run in the cloud. No self-hosting.

**Purpose.** People who spend the day in meetings: founders, investors, sales, product, consultants.
Instead of a video recording — a structured note and a chat over all earlier meetings.

**Features.**
- Notes from device audio (microphone + system audio) — no bot joins the call.
- Templates per meeting type; Granola Chat (a choice of Claude, GPT or Gemini).
- Team Spaces — shared notes and search across the team.
- An **MCP server** and personal and company APIs (from 25 March 2026).
- Pre-meeting briefs, follow-up emails, CRM integrations (HubSpot, Affinity, Attio; Salesforce in Enterprise),
  a company glossary.

**Advantage.**
- **Note-taking UX:** you write a few keywords, the model expands them based on the transcript — the result reflects what you
  considered important, not a summary of everything.
- **No bot** = no social friction in the meeting (but see "Worth knowing").
- **Bottom-up growth:** customers include Vanta, Gusto, Asana, Cursor, Lovable, Mistral AI (March 2026). YipitData (April 2026):
  Granola is taking users from Fathom, Otter and Fireflies, the switches are one-directional, "near-zero churn", growth in
  new users ×9 between January and February 2026 *(data vendor's blog)*.

**Architecture.**
```
desktop/mobile app: microphone ("Me") + system audio ("Them")
  └▶ audio stream to cloud ASR ──▶ transcript (audio is not stored)
     └▶ LLM: user's notes + transcript + template ──▶ note
        └▶ meeting index ──▶ chat, MCP, API, CRM
```
- Diarization: on Zoom, Meet and Teams from participant names; otherwise only "Me" (the microphone channel) vs "Them"
  (system audio), and the model infers the speakers from context.
- ASR reportedly Deepgram and AssemblyAI, summaries by OpenAI and Anthropic models — not verified by Granola.
- The web app does not record meetings. SOC 2 Type II; Enterprise adds HIPAA-compliant spaces, SSO/SCIM,
  automatic deletion policies and an audit API.

**How it makes money.** Freemium per seat (pricing, October 2026): Basic 0 USD (30-day history), Business 14 USD,
Enterprise 35 USD per user per month.
- Funding: seed 4.25 million USD (May 2023); Series A 20 million (October 2024, at 5 thousand weekly users); Series B
  43 million at a valuation of 250 million (May 2025); **Series C 125 million USD at 1.5 bn** (25 March 2026, Index Ventures, Kleiner
  Perkins); 192 million USD in total *(TNW)*.
- ARR undisclosed; revenue ×2.5 between January and March 2026, ARR +about 250% in Q1 2026 *(an aggregator citing the company's blog)*;
  250 thousand+ active users in mid-2025 — unverified.

**Offline.** **No.** Capture is local, but ASR and the LLM run in the cloud. The local counterpart is
simple: two audio channels → local STT (Whisper/Parakeet, see [Voice](../agent-harnesses/02-BUILDING-BLOCKS.md#voice)) →
a local LLM. An hour-long conversation after transcription is, by my estimate, a dozen-odd to twenty-odd thousand tokens —
it fits in the 131k context of a single DeepSeek slot with room to spare for notes and the template.

**What to adopt.**
- **Free diarization from two channels:** microphone = the professional, system audio = the client on a video call.
  For a meeting in the office you already need real diarization (pyannote offline).
- **The user's notes as scaffolding.** The lawyer jots "deadline? / amount of the contractual penalty / witness Kowalski",
  the model expands each point and adds a quote from the transcript with a timestamp.
- **Delete the audio, keep the text** — an argument for lawyers and doctors; on the rig you can go further: a transcript
  encrypted in the case directory, with a retention policy.
- **Templates per meeting type** (first conversation with a client, a case conference, a tax consultation)
  and an **MCP server with the notes** — other agents on the rig (e.g. the pleadings agent) use what was agreed at the meeting.
- **Consent by design:** a clear notice to all participants before recording and a record of that consent in the note.
  Treat voiceprints as biometric data (Art. 9 GDPR). This is not legal advice.

**Worth knowing.**
- In early 2025 researchers found a hard-coded AssemblyAI API key in the macOS beta.
- On 23 June 2026 a navigation vulnerability in the desktop app was reported; a server fix a day later, the workaround patched
  on 26 June, full closure confirmed on 29 June.
- July 2026 (press): notes were shared by link by default, and model training was on by default on the Free and Business plans
  (off for Enterprise).
- 30 July 2026: a proposed class action *Chamberlain v. Granola* (N.D. Cal., 3:26-cv-07926-EMC) — alleging recording
  people without an account "invisibly" and training on their data by default. **No bot does not remove the obligation to get consent.**

**Sources:** [TNW: Series C](https://thenextweb.com/news/granola-series-c-meeting-ai-enterprise-context) ·
[pricing](https://www.granola.ai/pricing) ·
[documentation: transcription](https://docs.granola.ai/help-center/taking-notes/transcription) ·
[YipitData](https://www.yipitdata.com/resources/blog/granola-vs-fathom-otter-fireflies-ai-notetaking) ·
[SoftwareTestingHelp: ASR vendors](https://www.softwaretestinghelp.com/?p=411472) ·
[ARR.club](https://www.arr.club/granola/granola-arr-grow-at-250-in-q1-2026) ·
[Sacra: users](https://sacra.com/research/250m-year-granola-for-plumbers) ·
[AssemblyAI key](https://afadeev.substack.com/p/the-hidden-dangers-of-ai-note-taking) ·
[vulnerability June 2026](https://docs.granola.ai/help-center/policies/security-contributions/desktop-app-navigation-vulnerability) ·
[Startup Fortune: privacy](https://startupfortune.com/granola-ai-meeting-notes-are-not-as-private-as-you-might-think/) ·
[PPC Land: lawsuit](https://ppc.land/granola-sued-for-recording-meetings-without-consent-to-train-ai-models/)


---

## 11. Sierra

**Category:** professional (customer service) · **Code:** closed · **Company:** Sierra Technologies (USA) ·
**Score: 85** (T4 I5 L4 A4)

> Customer service agents for the biggest consumer brands, billed per outcome rather than per token — and the company that
> gave the market a measure of agent reliability (pass^k) and a protocol for personal agents.

**Open or closed.** A closed product (cloud). Open are the **τ-bench** benchmark and the **Personal Agent Protocol**
(with Meta). The model providers the agents run on are not described in my sources; Sierra's own is "fleming-1" —
a model that detects calling AIs (8 October 2026).

**Purpose.** Large B2C companies: 25% of the Fortune 20, half of the customers have revenue above 1 bn USD (February 2026), over 40% of the Fortune 50
(May 2026) *(company data / TechCrunch)*. Customers include Rocket Mortgage, SiriusXM, ADT, Cigna, DIRECTV, Gap, Rivian,
Sutter Health. The problem: resolving customers' cases (refunds, plan changes, applications) in every channel, with no queue.

**Features.**
- **Agent OS 2.0** (5 November 2025): one agent in all channels, Agent Studio 2.0, Agent Data Platform
  (memory and customer context).
- **Horizon** (16 July 2026): agents pursuing a goal over days and months, e.g. granting a mortgage or
  authorising a healthcare benefit.
- Voice Personas (7 August 2026); Ghostwriter in Slack and Teams (28 September 2026).
- **Personal Agent Protocol** (6 October 2026) with Meta and, among others, Genesys, Shopify, Stripe, Walmart.
- "fleming-1" — detecting that an AI is calling on the other end (8 October 2026).

**Advantage.**
- **Outcome-based pricing** shifts the risk to the vendor — it is easier for the customer to buy, and Sierra has to really resolve cases.
- **A narrow-task methodology:** Sierra explains its growth by narrow "jobs to be done" with a defined measure of success winning
  (in contrast to the MIT thesis that 95% of AI pilots fail).
- **Interaction data** as a moat "that compounds" *(company data)*; the founders' credibility (Bret Taylor,
  Clay Bavor) when selling to boards.

**Architecture.**
- **Context Engine** and long-term planning across successive contacts (Horizon) — the agent remembers what stage
  the case is at and returns to it on its own after days.
- **One agent, many channels** (chat, voice, Slack/Teams) on a shared data platform.
- **Evaluation — τ-bench** (20 June 2024): a simulated user and simulated APIs, domain rules (e.g. a refund policy).
  The **pass^k** measure — whether the agent solves the same task k times in a row. GPT-4o dropped in retail to about 25%
  at pass^8, 60% less than at pass^1.
- **Personal Agent Protocol:** an open OAuth-based standard — how a user's personal agent (in the style of OpenClaw)
  authenticates with a company and acts through the site, an API (MCP/OpenAPI) or the company's agent. "The consumer decides what
  access to give the agent, the company sets the parameters."

**How it makes money.** **An outcome fee** (since 10 December 2024): a resolved conversation, a saved cancellation, an
upsell; "if the conversation is not resolved, in most cases there is no charge". With Horizon: "you pay for
outcomes, not for tokens".
- ARR: 100 million USD (end of November 2025, 7 quarters after the launch in February 2024), over 150 million USD and the first quarter
  with 50 million USD (February 2026) *(company data)*.
- Valuation: 10 bn USD (November 2025, Forbes); **950 million USD at a valuation of over 15 bn USD** (4 May 2026, Tiger Global and GV)
  *(TechCrunch)*.

**Offline.** **No.** A cloud product. A local counterpart for a Polish office (registration at a clinic,
a law firm's reception) would need: a local model with rules in plain language, a limited set of tools
(calendar, client file), STT/TTS for the phone — and reliability tests before deployment.

**What to adopt.**
- **pass^k instead of "works in the demo".** Run every test scenario 8 times; 4 DeepSeek slots compute that in parallel.
  A professional needs repeatability more than peak quality. A simulated customer = a second agent
  with a persona description — [14-EVALUATION.md](../course_agentic_apps/14-EVALUATION.md).
- **A case agent for months (Horizon):** memory of the case stage, procedural deadlines and reminders triggered from
  the scheduler — [11-SCHEDULING-PROACTIVITY.md](../course_agentic_apps/11-SCHEDULING-PROACTIVITY.md).
- **Outcome-based pricing where the outcome can be counted:** per finished document, per closed accounting month, per
  settled batch of KSeF invoices — instead of per token, which you barely count locally anyway.
- **A narrow task with a defined measure of success** to start with (e.g. "a draft reply to a demand for payment
  approved without corrections"), not an "assistant for everything".
- **A protocol instead of scraping:** when banks and government offices start exposing interfaces for personal agents (Personal Agent Protocol),
  the office's agent will work through an API with explicitly granted access — it is worth separating the tools layer from
  the agent's logic already now ([09-PROTOCOLS-MCP-CLI-A2A.md](../course_agentic_apps/09-PROTOCOLS-MCP-CLI-A2A.md)).

**Worth knowing.**
- Founded by Bret Taylor and Clay Bavor; the product launched in February 2024.
- Expansion to France and an office in Tokyo (December 2025); the acquisition of the YC startup Fragment (23 April 2026).
- A direct competitor, Decagon (Series D: 250 million USD at 4.5 bn USD, 27 January 2026), announced its own consent and trust protocol PACT on 6 October 2026 — the same day Sierra announced the Personal Agent Protocol with Meta; the standard is not yet settled.
- The market is moving towards outcome-based pricing: Intercom Fin charges 0.99 USD per resolved case, Parloa — per minute or
  interaction *(company price lists)*.

**Sources:** [Sierra: blog](https://sierra.ai/blog) · [year two](https://sierra.ai/blog/year-two-in-review) ·
[Horizon](https://sierra.ai/blog/horizon) ·
[outcome-based pricing](https://sierra.ai/blog/outcome-based-pricing-for-ai-agents) ·
[τ-bench](https://sierra.ai/blog/benchmarking-ai-agents) ·
[Personal Agent Protocol](https://sierra.ai/blog/introducing-personal-agent-protocol) ·
[TechCrunch, 4 May 2026](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/) ·
[Forbes, November 2025](https://www.forbes.com/sites/richardnieva/2025/11/05/sierra-bret-taylor-clay-bavor/) ·
[Decagon: Series D](https://decagon.ai/blog/series-d-announcement) · [Decagon: blog](https://decagon.ai/blog) ·
[Intercom: pricing](https://www.intercom.com/pricing) · [Parloa: pricing](https://www.parloa.com/platform/pricing/)


---

## 12. OpenEvidence

**Category:** professional (medicine) · **Code:** closed · **Company:** OpenEvidence Inc. (USA) ·
**Score: 84** (T5 I4 L4 A3)

> A clinical knowledge search engine for doctors that answers with citations from licensed journals, is free
> for verified doctors and makes money from pharmaceutical advertising. Proof that licensed sources beat
> a bigger model.

**Open or closed.** Closed, cloud. Model providers are not public.

**Purpose.** Doctors and other verified clinicians in the USA: a fast, cited answer to a clinical question while
working. Since 2025–2026 also a visit scribe (Visits) and Doctor Dialer.

**Features.**
- Answers to clinical questions with in-text citations.
- DeepConsult (July 2025) — a longer, multi-source write-up.
- Voice Mode (May 2026).
- **Visits** (scribe) and **Doctor Dialer**.
- EHR integration at Cedars-Sinai (May 2026).
- A claimed 100% on the USMLE exam *(company data, 2025)*.

**Advantage.**
- **Licensed content:** NEJM, JAMA Network, NCCN, Wiley, Cochrane — a competitor with a "bigger model" will not copy that.
- **Free for doctors** after verification — a zero barrier to entry.
- **Reach:** according to an Offcall survey (December 2025), more doctors in the USA use OpenEvidence than all other
  AI tools for doctors combined *(via Sacra)*.

**Architecture.**
```
verified doctor ──▶ question (text / voice)
  └▶ search in a curated, licensed corpus of literature (RAG)
     └▶ LLM: answer with in-text citations ──▶ link to the source
separately: Visits (scribe) · Doctor Dialer · EHR integration
```
- The value is in the search layer and the licences, not in the model — the models are not disclosed.
- In June 2025 the company sued Pathway over alleged prompt extraction — it
  treats the way it assembles context as a value to protect.

**How it makes money.** **Advertising** from pharmaceutical and medical device companies: 70–150 USD CPM (some sources
say 1,000+ USD) *(Sacra)*.
- Revenue: about 7.9 million USD (December 2024) → 50 million (June 2025) → 150 million (end of 2025) → about 300 million USD annualised
  (July–September 2026); gross margin about 90% *(Sacra estimate)*.
- Funding: 75 million USD at 1 bn (February 2025); 210 million at 3.5 bn (July 2025); 200 million at 6 bn (October 2025);
  **250 million USD at 12 bn** (21 January 2026); about 700 million USD in total *(press)*. Sacra gives 15 bn USD (September 2026) —
  unverified.
- Usage: 760 thousand doctors and 18 million consultations a month (December 2025); about 20 million a month (January 2026); 1 million
  in a single day (10 March 2026) *(company data via Sacra/Wikipedia)*.

**Offline.** **No.** But this is the pattern **easiest to run fully locally**: RAG over Polish
guidelines of scientific societies (e.g. PTK, PTD), Summaries of Product Characteristics (ChPL) and AOTMiT
recommendations. What is hard is content licences and keeping the content up to date, not the model.

**What to adopt.**
- **Sources matter more than the model.** On the rig: an index of ChPL and guidelines in a read-only directory, every answer
  with a citation (document, section, version date), and no source = "I don't know", not a guess.
- **Corpus versioning:** with every answer the release date of the guideline; a separate scheduled task checks
  for new versions (that is the "hard part" — not the model's knowledge).
- **Separate knowledge from patient data.** A clinical question without personal data can go to Opus in the hybrid;
  a question with patient records — only DeepSeek on the board
  ([10-HYBRID-LOCAL-PLUS-CLAUDE.md](../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md)).
- **Watch the scope:** clinical answers are closer to decision support than a scribe is. The Code of Medical Ethics (Kodeks Etyki Lekarskiej) art. 12
  requires, for AI in diagnosis or treatment, the patient's consent and a certified tool — a product
  that is a "guideline search engine with citations" must state this clearly in its intended purpose (this is not legal advice).
- **The business model "free for the professional, someone else pays"** requires a huge audience; for a local
  product the Noxtua route is more realistic — a partnership with a content publisher ([#14-noxtua](#14-noxtua)).

**Worth knowing.**
- Founders: Daniel Nadler (formerly Kensho) and Zachary Ziegler.
- A conflict with Doximity (a dispute around Pathway, acquired by Doximity in August 2025); both companies are heading towards a
  "doctor's assistant for everything".
- OpenAI launched ChatGPT for Clinicians in April 2026 — direct competition *(via Sacra)*.
- Background: 81% of doctors in the USA used AI in 2026 (38% in 2023), most often for summaries of studies (39%) — but 71% say they have
  little or no influence on the choice of tools at their facility *(AMA survey, March 2026)*. In Polish private practices
  the doctor is both the user and the buyer.

**Sources:** [Wikipedia](https://en.wikipedia.org/wiki/OpenEvidence) ·
[Sacra: OpenEvidence](https://sacra.com/c/openevidence/) ·
[Rutland Herald: 250 million USD round](https://www.rutlandherald.com/news/business/openevidence-raises-250-million-to-build-medical-superintelligence-for-doctors/article_0960939c-ca41-5321-8417-54f84800ece6.html) ·
[Sacra: OpenEvidence vs Doximity](https://sacra.com/research/openevidence-vs-doximity/) ·
[Wikipedia: Doximity](https://en.wikipedia.org/wiki/Doximity) ·
[ASCO Post: AMA survey](https://ascopost.com/news/march-2026/ama-survey-finds-rapid-growth-in-physician-ai-adoption/) ·
[Physicians Practice: influence on choice](https://www.physicianspractice.com/view/physician-ai-use-is-surging-is-your-practice-ready-) ·
[Kodeks Etyki Lekarskiej (PDF)](https://nil.org.pl/uploaded_images/1723037323_kel-2305.pdf)


---

## 13. browser-use

**Category:** executor · **Code:** open core (MIT) + closed cloud ·
⭐ <!-- gh:browser-use/browser-use -->117.6k · **Company:** Browser Use, Inc. (founders from ETH Zurich) ·
**Score: 83** (T4 I4 L4 A5)

> The most popular open library of "hands in the browser": it turns a page into a text description of clickable elements,
> so the model works on buttons and fields instead of guessing from pixels — the foundation on which Manus, among others, launched.

**Open or closed.** An open core: a Python library under MIT (latest release 0.13.11, 7 October 2026) and the open
weights BU-30B-A3B-Preview (MoE: 30B parameters, 3B active, 65k context, runnable in vLLM; 16 December 2025).
Closed: Browser Use Cloud (V3/V4 agents, "stealth" browsers, proxies) and the BU 2.0 model available only through the API.
Self-hosting the library — yes.

**Purpose.** Developers and companies automating web workflows: filling in forms, collecting data, research
across many sites. The company was founded in 2024 by Magnus Müller and Gregor Zunic (Student Project House ETH Zurich). In practice
it is infrastructure — the "hands" used by other agents (Manus at launch, OpenManus as the default browser MCP
server).

**Features.**
- Observing the page as text/DOM of interactive elements; screenshots as a supplement.
- Controlling Chromium through the raw **Chrome DevTools Protocol** ("100% CDP-based" since 19 August 2025; earlier Playwright).
- Any model through an OpenAI-compatible endpoint, including a local one.
- Cloud — three generations of agents *(company data)*: V2 (about 0.70 USD/task, 54% accuracy), V3 "step by step"
  (about 0.87 USD, 67%), V4 writing and running code (about 1.64 USD, 76% "on difficult tasks", about 5 min).
- Browser profiles with persistent sign-in; **secrets pinned to `allowedDomains`**.
- V4 agent scheduling and the "Agency" skill (17 August 2026): proactive work, approval only before an
  external action (sending, publishing).
- Residential proxies, a free tier (from 3 April 2026), concurrency tiers from 10 to 1000 sessions.

**Advantage.**
- **The widest reach among open browser agents** (117.6k ⭐, GitHub API 11 October 2026).
- **Text instead of pixels** — cheaper, more robust and works with models without vision.
- **Its own small specialised models:** on its own Browser Use Bench v2.1 (180 long tasks on the live web,
  7 October 2026) "BU fast" scores 72.9 points at 0.11 USD/task — roughly the same as Claude Sonnet 5.5 high (72.7) at
  1.53 USD; Claude Opus 5.5 — 75.0; GPT-6.1 Sol — 79.6 *(vendor benchmark)*.
- **Cost per task next to accuracy** — the company shows USD/task, not just percentages.

**Architecture.**
```
task ─► agent: LLM (cloud / local endpoint / BU-30B-A3B in vLLM)
              ▲  text description of the page's interactive elements (+ screenshot when needed)
              │  action on the indicated element
           Chromium ◄── Chrome DevTools Protocol (no Playwright)
              └─ profile with cookies · secrets injected only on allowedDomains
```
- **Loop:** page → a condensed representation of interactive elements → the model picks an action → execution through CDP →
  a new observation. The model does not need to see an image.
- **V4 (cloud):** the agent writes a browser script instead of clicking step by step — for long data sets fewer
  model calls.
- **Cloud:** managed "stealth" Chromium sessions billed per browser hour, residential proxies, resale of tokens.
- **Approvals:** Agency asks "only before an external action like sending or publishing".
- **Evaluation:** its own benchmark with cost per task; independently — the Princeton HAL Online-Mind2Web leaderboard.

**How it makes money.**
- **Open core:** the library is free, revenue comes from Browser Use Cloud.
- **Pricing** (page from 3 September 2026, *company data*): pay-as-you-go credits that do not expire, plus enterprise contracts;
  browser 0.02 USD/hour; residential proxy 5 USD/GB (cut from 10 USD/GB on 3 April 2026); transfer 0.20 USD/GB; tokens
  resold (default GPT-5.6 Luna 0.24 / 1.44 USD, BU 2.0 0.60 / 3.50 USD per 1 million input/output tokens);
  the old V2 "from 0.006 USD/step" plus 0.01 USD/task.
- **Funding:** a 17 million USD seed led by Felicis (with YC, Paul Graham, A Capital, Nexus, SV Angel),
  announced in March 2025. Later rounds, ARR and user numbers could not be confirmed.

**Offline.** **Partially.** The MIT library runs on your machine with a local browser and a local OpenAI-compatible
endpoint, and BU-30B-A3B is open weights for vLLM. So without the internet you can operate **local web applications**
(an intranet, a law firm system on the local network); public sites by nature require a network. Stealth browsers,
proxies, BU 2.0 and the V3/V4 agents — only in the cloud.

**What to adopt.**
- **DOM and the accessibility tree first, a screenshot as a fallback** — this is the only route for the text-only DeepSeek-V4-Flash; a model
  with vision would have to go to a separate tab or to the cloud anyway.
- **A small model for routine steps, a big one for the plan** (the BU fast pattern): on your side DeepSeek clicks and fills in, Opus 5.5
  comes in only for a hard plan or after a failed attempt.
- **An agent that writes code for long data sets** (the V4 pattern): instead of 200 clicks a single script in a sandbox —
  at 13.6 tok/s that is the difference between minutes and an hour.
- **Secrets pinned to domains:** a portal password works only on its domain, so a site impersonating the
  portal will not get it; plus an agent profile separated from the user's browser.
- **Approval only before an external action** (sending, publishing) and **cost per task in every evaluation**
  ([course 2, part 14](../course_agentic_apps/14-EVALUATION.md)).

**Worth knowing.**
- **Benchmark marketing:** in December 2024 the company announced 89.1% on WebVoyager — after removing 55 of 586 tasks and manually
  correcting the evaluator's verdicts. On the independent Princeton HAL Online-Mind2Web, browser-use with Claude Sonnet 4 has 40.0%
  (a full run 1577 USD; HAL notes that costs may be inflated by up to 2×). The gap between vendor and independent results is usually
  about 2×.
- **BU 2.0** (27 January 2026) according to the vendor matched Claude Opus 4.5 (83.3% vs 82.3%) with about 40% less time
  (62 vs 104 s per task) — but only as an API, without weights.
- **Security of the whole category:** OpenAI (22 December 2025) — prompt injection "unlikely to ever be fully 'solved'";
  Gartner (8 December 2025) advised companies to block AI browsers. Local execution removes the leak to the cloud, but not
  injections ([course 2, part 16](../course_agentic_apps/16-SECURITY-OWASP-ASI.md)).
- **The market:** OpenAI shut down the Atlas browser (announced 9 July 2026, end on 9 August 2026) because "the browser is a
  feature, not the destination"; all AI browsers together had <1% of the market (August 2026). The "hands" layer wins —
  libraries, extensions, cloud browsers — not a new browser.
- A browser-use contributor (MagMueller) integrated Browser Use CLI 3.0 with OpenManus (August 2026) — the library is becoming
  the default browser MCP server for other agents.

**Sources:** [GitHub](https://github.com/browser-use/browser-use) · [GitHub API](https://api.github.com/repos/browser-use/browser-use) · [pricing](https://browser-use.com/pricing.md) · [benchmarks](https://browser-use.com/benchmarks) · [changelog 3 April 2026](https://browser-use.com/changelog/3-4-2026) · [BU-30B-A3B](https://browser-use.com/changelog/16-12-2025) · [switch to CDP](https://browser-use.com/changelog/19-8-2025) · [BU 2.0 — changelog](https://browser-use.com/changelog/27-1-2026) · [choosing an agent](https://docs.browser-use.com/cloud/choosing-an-agent) · [BU 2.0 card](https://docs.browser-use.com/open-source/bu-2-0-model-card) · [WebVoyager report](https://browser-use.com/posts/sota-technical-report) · [Felicis](https://felicis.com/blog/browser-use-the-tool-making-it-easier-for-ai-agents-to-navigate-websites-raises-17m) · [ain.ua](https://en.ain.ua/2025/03/25/browser-use-raises-17m) · [HAL Online-Mind2Web](https://hal.cs.princeton.edu/online_mind2web) · [OpenAI on prompt injection](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/) · [Gartner](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/) · [end of Atlas](https://techcrunch.com/2026/07/09/openai-is-shutting-down-atlas-but-its-ai-browser-ambitions-are-still-growing/) · [AI browser share](https://eu.36kr.com/en/p/3931781634260099) · [OpenManus commits](https://api.github.com/repos/FoundationAgents/OpenManus/commits?per_page=5)

---

## 14. Noxtua

**Category:** professional (law, EU) · **Code:** closed · **Company:** Noxtua SE (Germany, Berlin; formerly Xayn) ·
**Score: 78** (T3 I4 L5 A4)

> A German legal assistant in a sovereign EU cloud, with an "Athena" tier on open models and content from the publisher
> C.H.Beck — the only example in the top tier of "EU and privacy first", available in Poland as Beck-Noxtua.

**Open or closed.** A closed platform. The **Athena** tier runs on open source models in sovereign European
infrastructure; a customer can choose hosting exclusively in a cloud controlled by Europeans on
open models. In April 2025 the company also described its own transformer model trained on legal contracts
(hosted in the Northern Data cloud in Frankfurt). There is no desktop installation and no air-gapped mode.

**Purpose.** Lawyers, legal departments, public administration and the judiciary in German-speaking countries and in Europe —
people bound by strict professional secrecy who do not want to (or cannot) send case files to an American cloud.
Over 30,000 users *(company data, September 2026)*. In Poland: Beck-Noxtua, sold by the publisher C.H.Beck
on Legalis content.

**Features.**
- Legal research, **Matrix Analysis** (structured analysis of many documents), an editor for drafting and export,
  Projects, Workflows.
- Add-ins for Word and Outlook.
- Search across 210 million+ documents, including 15.8 million+ court decisions, from curated publisher content *(company data)*.
- "Legal AI Workspaces" for individual jurisdictions, on the content of 8+ European legal publishers.
- Beck-Noxtua (PL): research on Legalis content, document analysis, draft pleadings; "no token limits".
- Working without anonymising case files — the company claims a lawyer can work "without requiring anonymization".

**Advantage.**
- **Content the competition does not have:** C.H.Beck — the biggest German legal publisher — is the majority
  shareholder; in 2026 the Austrian MANZ joined. In Poland, access to Legalis commentaries.
- **Professional secrecy as the main argument:** the security page refers directly to § 43e BRAO and § 203 StGB
  (German provisions on lawyers' secrecy and criminal liability for breaching it).
- **National trust certifications:** BSI C5, ISO 27001, ISO 42001; the Polish Beck-Noxtua page lists ISO 9001, 27001,
  27017, 27018 and 42001.
- **A choice of model tier** instead of a single "cloud yes/no" decision.

**Architecture.**
```
user (web, Word, Outlook)
  └▶ Noxtua platform — hosting: Germany (Deutsche Telekom, IONOS) and Switzerland
     ├─ Athena Agent (Standard): open source models in sovereign EU infrastructure
     └─ Minerva Agent (Frontier): international frontier models in a "European setup"
           through T Cloud Public / AI Foundation Services of Deutsche Telekom
  └▶ publisher content (C.H.Beck, MANZ, …): 210 million+ documents ──▶ answer with citations
```
- Inputs and outputs are not used for training; the platform declares "no persistent access to plaintext data".
- A self-hosting option: only in a sovereign cloud controlled by Europeans, on open source models.
- Beck-Noxtua in the Czech Republic (8 December 2025): data processed in IONOS and Open Telekom Cloud with BSI C5 — "independent,
  European infrastructure" thus means a cloud owned by EU companies, not a server in the law firm.

**How it makes money.** Subscriptions; in Germany the price list is not public.
- **Poland: PLN 590 net per month per user**, no token limits, requires a Legalis subscription in the
  Silver variant at least *(beck-noxtua.pl page, checked 11 October 2026)*. The price of Legalis is not public.
- Funding: Series B 92.2 million USD (81.2 million EUR) on 22 April 2025, led by C.H.Beck, with Northern Data, CMS
  and Dentons *(TechCrunch; a CMS statement gives about 80.7 million EUR, 23 April 2025)*. **Series C of over 100 million EUR** from
  C.H.Beck and MANZ (23 September 2026); valuation undisclosed.
- An illustrative calculation (list prices, net): 3 lawyers × PLN 590 × 24 months = **PLN 42,480** for two years,
  plus Legalis — a reference point for pricing a box on the desk with a support subscription.

**Offline.** **No.** Even the "self-host" variant is a sovereign EU cloud, not a computer in the law firm. A local
counterpart needs: a model on the desk (e.g. DeepSeek-V4-Flash), an index of the firm's own case files, public
sources of law (ISAP/ELI, SAOS) with regular offline updates, disk encryption and support without access to the data.
You cannot reproduce Legalis/LEX commentaries locally — and you do not need to (see below).

**What to adopt.**
- **Two tiers, chosen per matter.** "Sovereign" = DeepSeek on the board, the default for every matter with client data;
  "frontier" = Opus, switched on deliberately only for content without secrecy (e.g. a general question about interpretation), with an entry
  in the matter log. This is directly the Athena/Minerva pattern, moved from the cloud to the desk.
- **The secrecy provision on the first page of the product:** art. 6 of the Law on the Bar (Prawo o adwokaturze), art. 3 of the Act on Legal
  Advisers (ustawa o radcach prawnych), and for advocates the new § 23e of the Collection of Ethical Rules (Zbiór Zasad Etyki) (NRA (Naczelna Rada Adwokacka, the Polish Bar Council), 12–13 June 2026: AI only as an aid, no
  confidential information in tools without due protection, personal verification, and on the client's request, information
  about the tools). A local assistant can export a "note on the tools used" per matter. This is not legal advice.
- **Complement the publishers, do not compete with them.** Beck-Noxtua and LEX Expert AI have the commentaries; the assistant on the desk
  works on what they do not see: the firm's case files, correspondence and drafts.
- **Trust without a BSI C5 budget:** a ready DPIA, answers to the UODO checklists (6 August 2026), a one-page
  mapping to § 23e / the KIRP recommendations, and, once art. 12 of the Act on Artificial Intelligence Systems enters into force
  (3 months from publication, art. 127), an individual opinion of KRiBSI (the Polish AI oversight commission) (30 days, 60 in complex matters; no opinion
  within the deadline = an opinion in line with the application).
- **A citation with every claim** — in PL this is already a market standard (LEX Expert AI links fragments of sources), and
  Charlotin's database records 6 Polish cases with AI hallucinations (10 October 2026).

**Worth knowing.**
- Xayn was founded in 2020 as a startup for privacy and on-device AI, before changing industry to law.
  The CEO Leif-Nissen Lundbæk: "you cannot just use an American AI model in a German legal context".
- Beck-Noxtua was announced for Poland on 3 December 2025 (launch planned for spring 2026); the Czech version — 8 December 2025.
- Offices: Berlin, Paris, Stockholm, Zagreb, Munich, Freiburg.
- Competition in PL: LEX Expert AI (Wolters Kluwer, since 19 November 2025, RAG exclusively on LEX content, servers in the EU),
  LexisNexis Protégé (a demo, no price) and Gaius-Lex — the only Polish player found with a full on-premise deployment
  (for law firms of 20–99 lawyers).
- Sovereign AI capital in the EU is growing: Mistral 3 bn EUR at a valuation of over 21 bn EUR (September 2026), Cohere + Aleph Alpha
  at 20 bn USD (April 2026).

**Sources:** [Noxtua](https://www.noxtua.com/) · [Noxtua: security](https://www.noxtua.com/security) ·
[Series C](https://www.noxtua.com/news/press-releases/series-c) ·
[TechCrunch: Series B](https://techcrunch.com/2025/04/22/noxtua-raises-92m-for-its-sovereign-ai-tuned-for-the-german-legal-system/) ·
[CMS: C.H.Beck as investor](https://cms.law/en/deu/news-information/c.h.beck-becomes-leading-investor-in-legal-ai-noxtua) ·
[Beck-Noxtua: PL announcement](https://www.noxtua.com/news/press-releases/beck-noxtua-poland) ·
[Beck-Noxtua: Czech Republic](https://www.noxtua.com/news/press-releases/beck-noxtua-for-the-czech-republic) ·
[beck-noxtua.pl](https://www.beck-noxtua.pl/) ·
[NRA: § 23e](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/) ·
[Prawo o adwokaturze (PDF)](https://api.sejm.gov.pl/eli/acts/DU/2024/1564/text.pdf) ·
[ustawa o radcach prawnych (PDF)](https://api.sejm.gov.pl/eli/acts/DU/2024/499/text.pdf) ·
[UODO: AI checklists](https://uodo.gov.pl/pl/138/4533) ·
[KIRP: AI recommendations](https://kirp.pl/rekomendacje-dotyczace-korzystania-z-ai/) ·
[prawo.pl: LEX Expert AI](https://www.prawo.pl/prawnicy-sady/lex-expert-ai-nowym-narzedziem-dla-prawnikow,535918.html) ·
[Gaius-Lex](https://gaius-lex.pl/) · [hallucination database](https://www.damiencharlotin.com/hallucinations/) ·
[Mistral: round](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/) ·
[TechCrunch: Cohere + Aleph Alpha](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/)

---

## 15. Perplexity

**Category:** everyday + executor · **Code:** closed (a local product on open models) · **Company:** Perplexity AI
(USA) · **Score: 77** (T4 I4 L4 A3)

> A search engine that answers with footnotes, the Comet browser with an agent and — since 25 August 2026 — **Portable Computer**:
> the first product from a major player in which the whole agent (a 27B model, harness, sandbox, tools) runs on the user's
> desk. In the top tier mainly for this move: it is the closest public pattern to what I want to build myself.

**Open or closed.** The apps, Comet and the harness are closed. The local Portable Computer runs **open
models**: Qwen 3.8 27B and "PPLX 27B" fine-tuned by Perplexity (Nvidia Nemotron 3.5 Lightning announced). Also open
is **BrowseSafe** — a prompt injection classifier based on Qwen3-30B-A3B together with the BrowseSafe-Bench benchmark (Hugging
Face, about 7 December 2025; the press does not give the licence). Running a licensed product locally: only Portable Computer (on your own Nvidia GPU), not the rest.

**Purpose.** For people who search and read a lot: an answer with citations instead of a list of links. On that Perplexity built
an agent in the browser (Comet), a cloud orchestrator of many models (Computer, the Max plan) and — for those who do not want to
send data away — a fully local agent.

**Features.**
- **Answer engine:** answers with source citations; sections Discover, Spaces, Shopping, Travel, Finance.
- **Comet** (Chromium): 9 July 2025 Max only, 13 August 2025 Pro, from 2 October 2025 free for everyone; Android 20 November 2025,
  iOS 18 March 2026. The assistant in the side panel summarises tabs, navigates, fills in forms, sends emails, buys; in Max a background
  assistant runs several tasks at once from a single panel.
- **Perplexity Computer** (27 February 2026, Max): a cloud orchestrator that splits a task among subagents and about 19 models
  (according to Computerworld: Opus 4.6 for reasoning, Gemini for research, Nano Banana and Veo 3.1 for media, Grok for light
  tasks, GPT-5.2 for long context).
- **"Personal Computer"** on the user's device — the sources diverge: a native macOS agent with access to files
  (April 2026, Wikipedia with a "citation needed" annotation, and XDA) and a Windows version routing about 20 models (28 July 2026,
  only an MSN teaser). I treat it as unverified.
- **Portable Computer** (25 August 2026): the model, harness, inference engine, tools, connectors and sandbox — all on the
  user's machine. Linux at launch, Windows from September 2026; requires an Nvidia DGX Spark or an RTX card with **≥ 24 GB VRAM**;
  Apple Silicon not yet.
- **Hybrid orchestrator** (Computex, 2 June 2026): decides on the fly what stays on the device; keeps financial and health data
  local and **asks for consent before sending a sensitive task to the cloud**.
- **Samsung Galaxy S26:** a built-in Perplexity agent with a hotword ("Hey Plex"), Bixby strengthened by Perplexity
  (according to press headlines and teasers).

**Advantage.**
- Fast rollout and independence from a single model provider: routing per subtask.
- **The first big player with a fully local agent** — and with public numbers on how much it costs and how much quality it loses.
- Comet works in the user's real session (already signed in everywhere), so the problem of logging in inside a VM goes away.
- Distribution through manufacturers and operators: Samsung, Airtel.

**Architecture.** Portable Computer according to VentureBeat (25 August 2026):
```
 task ─▶ minimal harness: a short system prompt, skills loaded on demand
              │                 └─ self-verification hooks watch the task's "health"
              ▼
          vLLM: Qwen 3.8 27B / PPLX 27B  (RTX ≥ 24 GB or DGX Spark)
              ▼
          tools: MCP servers rewritten as concise CLI tools (fewer tokens) — Drive, Gmail, GitHub
              ▼
          a mandatory system sandbox — without it the harness REFUSES to start (fail closed)

 option: escalation to Claude Opus 5 ─▶ a PII classifier filters the outgoing context
        ─▶ the cloud "advisor" returns ONLY text; it touches neither files nor tools
```
- **Quality and cost** (Terminal-Bench 2.1, *company data*): Qwen alone 59.6% at zero token cost, with escalation 73.0%
  at about 0.415 USD per task. Perplexity admits that small models "still trail the frontier meaningfully on hard reasoning".
- **Comet** (according to the Amazon v. Perplexity court filings): the browser talks to the site, the agent takes screenshots locally,
  sends them to Perplexity's servers and gets navigation instructions back; the servers do not connect to the target site.
  **Local execution, reasoning in the cloud.** Which models power the Comet assistant — undisclosed.
- **Defence against injections** (BrowseSafe, December 2025): everything that comes from the web is untrusted → a fast
  classifier (91% detection in < 0.5 s; for comparison PromptGuard-2 35%, GPT-5 85%) → uncertain cases go to a frontier
  model. About 10% of attacks still get through.
- A hidden "Agentic Extension" with an MCP API could run local commands; after SquareX's criticism it was quietly disabled
  (about 19–20 November 2025).

**How it makes money.**
- **Subscriptions:** Pro 20 USD/month or 200 USD/year; Max 200 USD/month or 2000 USD/year (May 2026); Enterprise Max
  325 USD/month. Portable Computer is included in Pro, Max, Enterprise Pro and Enterprise Max.
- **No ads** since February 2026 — a "subscription first" model.
- **Comet Plus:** 5 USD/month for free users, included in Pro and Max; publishers were to receive 80% of revenue from a pool of 42.5 million USD
  (unverified — only a secondary tracker).
- **Revenue:** ARR about 450 million USD in March 2026 and 100 million+ MAU *(company data per PYMNTS, 8 April 2026)*; about 750 million USD in August
  2026, from below 250 million at the start of the year *(The Information via Reuters, 23 August 2026; Perplexity does not publish numbers,
  unaudited)*. The growth is attributed to the 200 USD Max plan with Computer.
- **Valuation:** about 20 bn USD (September 2025); about 200 million USD of new capital at about 20 bn (June 2026, only a teaser); Nvidia
  in talks about an investment at a valuation > 30 bn USD *(The Information, 23–24 August 2026)*.
- **India:** a year of Pro free with Airtel — MAU at the peak about 22 million (October 2025), about 14 million in July 2026 after the end of the promotion;
  app revenue in India about 156 thousand USD/month *(Appfigures via TechCrunch)*.
- A cloud deal with Azure: 750 million USD over 3 years (January 2026). Share of the assistant app market: below 5% (May 2026).

**Offline.** **Partially.** The search engine, Comet (reasoning on servers) and Computer are the
cloud. Portable Computer does inference and tools locally (a 27B model, a sandbox), but the product is closed and included in the Pro/Max price; I have not verified operation without a network (subscription activation, model downloads, updates) — the only source is the press. Connectors (Gmail, Drive) and optional escalation to the cloud require a network. The catch for me: it requires Nvidia, so on 4× AMD
Radeon AI PRO R9700 the ready-made product will not run. The pattern, however, transfers entirely — since Perplexity runs a 27B model on 24 GB, that size will fit on a single 32 GB card, but only after freeing it: with DeepSeek-V4-Flash on 4 cards about 1.4 GB of VRAM per card stays free (see [harness architecture](../agent-harnesses/03-ARCHITECTURE.md)); for tests — swapping the model in llama-swap or a separate machine.

**What to adopt.**
- **A desk-box specification confirmed by the market:** a ~27B model + vLLM + 24–32 GB VRAM. On the rig a 27B agent (Q4 about 18.5 GB) will fit on a single card only after freeing it from DeepSeek; Qwen3.8-27B claims 84.3% on OSWorld-Verified (model card, August
  2026, not independently verified) — a complement to the text-only DeepSeek in on-screen tasks.
- **Fail closed:** no sandbox — the agent does not start
  ([sandbox](../course_local_models/07-SANDBOX-SECURITY-MONITORING.md)).
- **Skills loaded on demand and MCP rewritten as concise CLI.** At 13.6 tok/s per slot every unnecessary token
  in the prompt is real waiting time.
- **Escalation with a PII filter, where the cloud only advises with text** — Opus 5.5 gets neither files nor tools. This is a
  compromise that can be offered to a customer ready for anonymised help from the USA
  ([hybrid router](../course_agentic_apps/17-HYBRID-AND-ROUTER.md)).
- **Consent for every exit to the cloud** + fixed "always local" categories: health, finances, professional secrecy.
- **Measure like Perplexity:** the score locally vs with escalation, plus cost per task — those are the numbers that will convince a customer.

**Worth knowing.**
- **Amazon v. Perplexity:** a lawsuit on 4 November 2025 (CFAA), a district court injunction in March 2026 (Jones Day dates it to May 2026);
  on 4 August 2026 the Ninth Circuit vacated it — it is "the user, not Perplexity" who uses Amazon's computers. Amazon moved for a rehearing
  en banc on 19 August 2026. The agent's logs became an e-discovery matter as a result.
- **Holes in Comet:** Brave (a hidden comment on Reddit → a leak of email and an OTP code, August 2025), Guardio "Scamlexity"
  (a purchase in a fake shop), LayerX "CometJacking" (October 2025, at first "Not Applicable"), Zenity "PleaseFix" (zero-click
  through a calendar invitation → `file://` files and 1Password; patch 23 January 2026, a bypass, a second patch 13 February 2026),
  BragJack (September 2026). Gartner (8 December 2025) advised companies to block AI browsers for now.
- **Content disputes:** Dow Jones / NY Post, Reddit, NYT (a cease-and-desist), Japanese publishers; Cloudflare (August 2025)
  accused it of stealth crawlers and removed Perplexity from the list of verified bots.
- **Bielik:** with the letter of intent with NVIDIA (VivaTech, June 2025) it was announced that the Polish Bielik would be added to Perplexity
  (money.pl, 11 June 2025); I have not confirmed the deployment.
- **Bought reach does not stay:** after the free year in India users left — the same lesson as the Qwen subsidies in China.

**Sources:** [Portable Computer — VentureBeat](https://venturebeat.com/infrastructure/perplexity-partners-with-nvidia-to-launch-portable-computer-a-fully-local-ai-agent-with-zero-token-costs) ·
[hybrid at Computex](https://venturebeat.com/technology/perplexity-ai-unveils-hybrid-local-cloud-inference-system-at-computex-2026) ·
[Portable Computer on Windows](https://www.techrepublic.com/article/news-perplexity-portable-computer-windows/) ·
[Perplexity Computer — Computerworld](https://www.computerworld.com/article/4138723/perplexitys-new-computer-agent-will-run-other-agents-for-you.html) ·
[Perplexity Computer — TechCrunch](https://techcrunch.com/2026/02/27/perplexitys-new-computer-is-another-bet-that-users-need-many-ai-models/) ·
[Comet for free](https://techcrunch.com/2025/10/02/perplexitys-comet-ai-browser-now-free-max-users-get-new-background-assistant/) · [Comet — Wikipedia](https://en.wikipedia.org/wiki/Comet_(browser)) ·
[Perplexity — Wikipedia](https://en.wikipedia.org/wiki/Perplexity_AI) · [BrowseSafe](https://the-decoder.com/perplexitys-browsesafe-tries-to-patch-the-gaping-security-holes-inherent-in-ai-browser-agents/) ·
[ARR 450 million — PYMNTS](https://www.pymnts.com/news/artificial-intelligence/2026/perplexitys-shift-to-ai-agents-boosts-revenue-50/) ·
[ARR 750 million and Nvidia](https://finance.yahoo.com/technology/ai/articles/nvidia-discusses-perplexity-investment-30-031804276.html) · [Nvidia at 30 bn](https://thenextweb.com/news/nvidia-perplexity-30bn-valuation-talks) ·
[India](https://techcrunch.com/2026/08/18/perplexitys-free-ai-offer-left-it-with-millions-more-users-in-india/) · [Comet Plus](https://www.vice.com/en/article/perplexity-comet-plus-announced/) ·
[Ninth Circuit — Jones Day](https://www.jonesday.com/en/insights/2026/09/ninth-circuit-vacates-cfaa-injunction-against-perplexitys-comet-ai-agent) · [Brave](https://brave.com/blog/comet-prompt-injection/) ·
[CometJacking](https://layerxsecurity.com/blog/cometjacking-how-one-click-can-turn-perplexitys-comet-ai-browser-against-you/) ·
[PleaseFix — The Register](https://www.theregister.com/2026/03/03/perplexity_comet_browser_hole_cal_invite/) · [MCP API — Help Net Security](https://www.helpnetsecurity.com/2025/11/20/perplexity-comet-browser-security-mcp-api/) ·
[Gartner](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/) · [Hey Plex](https://www.androidauthority.com/hey-perplexity-3655439/) ·
[Bielik and NVIDIA](https://www.money.pl/gospodarka/wielki-krok-dla-polskiego-ai-bielik-rozpoczyna-wspolprace-z-nvidia-7166523596470944a.html) ·
[R9700 — AMD](https://www.amd.com/en/products/graphics/workstations/radeon-ai-pro/ai-9000-series/amd-radeon-ai-pro-r9700.html) · [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)

---

## Worth knowing — who did not make the fifteen

The fifteen has one representative per pattern, so many good ideas were left outside it: category duplicates,
products unavailable in Poland, great engines without an assistant of their own. **Below is what is worth borrowing from them** — each
row with one number and a date, if the research confirmed it. GitHub API stars as of 11 October 2026.

### Next in the ranking (score 58–76)

| Name (score) | Category | Code | Why it is worth knowing | Source |
|---|---|---|---|---|
| UI-TARS / UI-TARS-desktop (76) | GUI executor | open, Apache-2.0, ⭐ <!-- gh:bytedance/UI-TARS-desktop -->39.2k | The only GUI agent from a big lab with open weights and a ready app; UI-TARS-1.5-7B scores 27.5% on OSWorld (April 2025) and runs locally through vLLM or Ollama. The pattern: one interface for 4 operators (local computer, local browser, remote VM, remote browser). | [model](https://huggingface.co/ByteDance-Seed/UI-TARS-1.5-7B) · [repo](https://github.com/bytedance/UI-TARS-desktop) |
| Legora (74) | professional, law (Sweden) | closed | A European rival of [Harvey](01-PROFILES.md#4-harvey): ARR 100 million USD in April 2026, over 200 million USD in September 2026 *(according to the founder, Bloomberg via secondary press)*; hosting in the EU from day one and a "documents × questions" grid as the main interface. | [TNW](https://thenextweb.com/news/legora-just-hit-100-million-in-revenue-it-took-18-months) |
| Heidi Health (74) | professional, medicine (Australia, UK/EU) | closed | ARR from 1 to 50 million USD in about 24 months (April 2026), 340 million USD of funding (September 2026); free, unlimited transcription, audio is never stored, EU data stays in the EU. It released agents skipping the UK and EU — because of regulation. | [HLTH](https://hlth.com/insights/news/heidi-raises-340m-to-expand-clinical-ai-into-supervised-agentic-workflows) |
| Microsoft 365 Copilot (74) | professional, office | closed | The price anchor in Polish companies: 18–32 USD per user per month, over 30 million paid seats (July 2026, *company data*). It also teaches caution: Anthropic models are excluded from the EU Data Boundary. | [documentation](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) · [results](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast) |
| Genspark (72) | executor | closed | About 250 million USD ARR in mid-2026 *(company data)* and a valuation of 2.6 bn USD (17 June 2026); a "mixture of agents" across 30+ models, phone calls for a flat 500 credits, Claw with a local mode limited to a single folder. A duplicate of [Manus](01-PROFILES.md#6-manus). | [Yahoo Finance](https://finance.yahoo.com/technology/ai/articles/genspark-ai-extends-series-b-131000248.html) |
| Poke (72) | everyday, via SMS/iMessage | closed | Over 100 million messages in 3 months, the first agent approved in Apple Messages for Business (4 June 2026), acquired by Cognition on 23 July 2026. The interface is an ordinary messaging app, and the automations are shared text "recipes". | [Cognition](https://cognition.com/blog/interaction) |
| NVIDIA NemoClaw (71, with Ghost) | living, local | open, Apache-2.0, ⭐ <!-- gh:NVIDIA/NemoClaw -->22.7k | One command installs [OpenClaw](01-PROFILES.md#1-openclaw) in an OpenShell sandbox with local Nemotron models and operator approval of outbound traffic. Probably the fastest route to a pilot in a law firm; "alpha" status. | [repo](https://github.com/NVIDIA/NemoClaw) |
| Ghost (71, with NemoClaw) | living, hardware | licence unknown | A 3499 USD box (pre-order from 5 October 2026) with an RTX Pro 4000, preinstalled Qwen-3.8-27B and Gemma-4-31B, and an egress firewall meant to block exfiltration; 11 million USD from a16z. Almost exactly my target format — USA only. | [TechCrunch](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/) |
| Nabla (70) | professional, medicine (France) | closed | In a UCLA RCT (NEJM AI, December 2025) it cut note-writing time by 9.5% (p=0.02), while Dragon made no significant difference. Whisper-based ASR fine-tuned on 7000 h of medical audio; audio is not stored. | [PubMed](https://pubmed.ncbi.nlm.nih.gov/41497288/) · [Nabla](https://nabla.com/blog/assessing-the-reliability-of-nablas-speech-to-text-engine) |
| Basis (70) | professional, accounting and tax (USA) | closed | "Behavior specs" (29 July 2026): an open standard for evaluating the **process** of an agent's work, not just the outcome — the agent never sees the specification. Series B 100 million USD at a valuation of 1.15 bn USD (24 February 2026). | [specifications](https://www.getbasis.ai/blogs/behavior-specs-an-open-standard-for-supervising-long-horizon-agents) |
| Hebbia (70) | professional, finance | closed | Invented the "Matrix" interface (the same questions × hundreds of documents, with a citation in every cell), later copied by Legora and CoCounsel; every cell is a small, parallel task — ideal for 4 local slots. 130 million USD at a 700 million valuation (July 2024). | [Matrix 2.0](https://www.hebbia.com/blog/introducing-matrix-2-0) |
| Glean (67) | professional, company knowledge | closed | ARR 300 million USD (28 May 2026). Tau: 0.58 USD per task against 2.98 USD in Claude Cowork *(company benchmark)* thanks to previously indexed context with permissions — an argument that an index saves tokens for a small model. | [TechCrunch](https://techcrunch.com/2026/05/28/gleans-top-line-crosses-300m-as-ai-budget-cutting-becomes-its-major-selling-point/) · [ITBrief](https://itbrief.asia/story/glean-launches-tau-to-cut-enterprise-ai-token-costs) |
| Lindy (65) | living → team | closed | The rule "everything with an external effect waits for approval, reads do not"; 49.99 USD per user for 5000 credits. Apple banned their Apple ID on iMessage within half a day (March 2026) — consumer channels are hostile. | [pricing](https://www.lindy.ai/pricing) · [iMessage](https://www.lindy.ai/blog/imessage-api-three-rewrites-one-apple-ban-and-what-actually-works) |
| Gaius-Lex (58) | professional, law (PL) | closed | The closest Polish equivalent of "data does not leave the law firm": Gaius Vault as SaaS in the EEA, a hybrid or full on-premise, for firms of 20–99 lawyers. Seed about 502 thousand USD (1 August 2025, *aggregator*), 6 people. | [gaius-lex.pl](https://gaius-lex.pl/) · [Signalbase](https://www.trysignalbase.com/news/funding/gaius-lex-secures-5) |

### Everyday assistants

| Name | Category | Code | Why it is worth knowing | Source |
|---|---|---|---|---|
| Meta AI + Muse | everyday + living | closed | Muse (8 September 2026): a separate VM per user and a "Sentinel" agent that approves **every** outbound action to the internet; payments with one-time Stripe cards, passwords in 1Password. 5 million downloads in 22 days, but only about 700 thousand DAU — retention. USA and Canada only. | [Meta](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) · [retention](https://cryptobriefing.com/meta-muse-app-store-retention/) |
| Muse Glimmer | local model | open weights, Apache 2.0 | About 29.6 bn parameters (dense), 131k context, 100+ languages, fits on a 24 GB card at 4 bits (10 August 2026); tuned for local agents. Quality in Polish unverified. | [VentureBeat](https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now) |
| Amazon Alexa+ | everyday, home | closed | "Experts" — tool bundles per domain instead of one long list, which helps small models choose a tool. In the USA 19.99 USD or free with Prime; **unavailable in Poland**; since 28 March 2025 all voice goes to the cloud. | [Amazon](https://www.aboutamazon.com/news/devices/new-alexa-generative-artificial-intelligence) · [countries](https://www.aboutamazon.com/news/devices/alexa-plus-international-launch) |
| Apple Siri AI | everyday, system | closed | iOS 27 (14 September 2026) with a waitlist; a model of about 3 bn parameters on the device (2-bit QAT) + Private Cloud Compute, built from Google Gemini. It is not on iPhones in the EU (DMA), and Apple Intelligence does not support Polish. | [TNW](https://thenextweb.com/news/apple-ios-27-siri-ai-release-icloud-plus-child-safety) · [languages](https://support.apple.com/en-us/121115) |
| Microsoft Copilot (consumer) | everyday | closed | An anti-pattern: the Mico avatar, group chats and podcasts removed on 18 August 2026 at about 38.5 million users a month. On the other hand, Agent Workspace in Windows (the agent as a separate account with "always / ask / never" per folder) is worth copying. | [TNW](https://thenextweb.com/news/microsoft-copilot-mico-retired-features-killed-app-merge) · [Windows](https://support.microsoft.com/en-us/windows/experimental-agentic-features-a25ede8a-e4c2-4841-85a8-44839191dfb3) |
| Grok | everyday | closed (old weights open) | Mostly negative lessons: the deepfake crisis (December 2025 – January 2026), patching the system prompt in production, chat leaks through indexed links. Grok Bot had 418 thousand users on 14 September 2026. | [Wikipedia](https://en.wikipedia.org/wiki/Grok_(chatbot)) · [Finbold](https://finbold.com/spacexais-grok-bot-agent-surpasses-400000-users-after-the-first-month/) |
| Doubao (ByteDance) | everyday, China | closed | Over 200 million DAU (September 2026, LatePost via TechNode); skills learned from screen recording and handing a task over from the phone to a PC. Since 15 July 2026 Chinese regulations closed down agents created by users. | [TechNode](https://technode.com/2026/09/23/bytedance-doubao-general-session-team-cuts/) |
| Qwen app (Alibaba) | everyday, China | app closed, models open | A campaign worth about 6 bn RMB gave a DAU jump, but a session lasts about 1.3 min — bought users do not stay. 167 million MAU (May–June 2026). The model matters more: Qwen 3.8 27B powers the local Portable Computer of [Perplexity](01-PROFILES.md#15-perplexity). | [TechTimes](https://www.techtimes.com/articles/323907/20260811/qwen-sells-paid-office-subscriptions-users-it-bought-with-free-bubble-tea.htm) |
| DeepSeek app | everyday | app closed, weights MIT | 130 million MAU (May 2026). The app is weak as an agent, but the V4-Flash weights under MIT are the engine of my rig. The Berlin data protection authority demanded the app's removal from stores in Germany (27 June 2025) — what counts is where the data is processed. | [Hugging Face](https://huggingface.co/api/models?author=deepseek-ai&sort=lastModified) · [netzpolitik](https://netzpolitik.org/2025/datenschutzbehoerde-greift-ein-deepseek-fliegt-aus-den-app-stores/) |
| Mistral Vibe (formerly Le Chat) | everyday + corporate (EU) | app closed, many models open | Proof that "sovereign AI" is a paying market: 3 bn EUR at a valuation of over 21 bn EUR (8 September 2026), Pro 14.99 EUR excl. VAT (the USD version of the page gives 14.99 USD), on-premise for companies, 100+ connectors with full MCP. | [TechCrunch](https://techcrunch.com/2026/09/08/mistral-raises-e3b-as-sovereign-ai-becomes-big-business/) · [pricing](https://mistral.ai/pricing) |
| Instinct | everyday, via iMessage | closed | A concierge in iMessage: calls businesses, has its own email addresses, uses temporary credentials and isolated sandboxes. Series C 1 bn USD at a valuation of 10 bn USD (28 September 2026). | [Pulse 2.0](https://pulse2.com/instinct-raises-1-billion-series-c-at-10-billion-valuation/) |

### Executors, browsers and open frameworks

| Name | Category | Code | Why it is worth knowing | Source |
|---|---|---|---|---|
| NanoClaw | living | open, MIT, ⭐ <!-- gh:nanocoai/nanoclaw -->30.9k | A minimalist OpenClaw alternative: a container per agent group, "script gates" before every scheduled wake-up (the model does not get up when there is no work), a credentials gateway. Built on the Claude Agent SDK; Ollama optional. | [repo](https://github.com/nanocoai/nanoclaw) |
| OpenManus | executor | open, MIT, about 58.6k stars | Cloned from Manus in 3 hours (6 March 2025) — proof that the value lies in the infrastructure, not the loop. A small, readable framework: Ollama + a Docker sandbox + local Chrome + MCP. | [repo](https://github.com/FoundationAgents/OpenManus) |
| Suna / Kortix | executor + team | source-available, Elastic License 2.0, about 20.3k stars | A sandbox and a git branch per session (rollback and audit), a credentials broker — secrets never enter the agent's machine. The licence changed from Apache 2.0 to ELv2 — check the licence before forking. | [README](https://raw.githubusercontent.com/kortix-ai/suna/main/README.md) |
| Agent S3 / Sai (Simular) | GUI executor | Agent S open (Apache-2.0), Sai closed | S3 with Best-of-N reached 72.6% on OSWorld against 72.36% for humans (October 2025). On the long tasks of OSWorld 2.0 Sai fully completes only 28.25% of tasks, at 15.70 USD each (28 August 2026) — the real scale of the problem. | [repo](https://github.com/simular-ai/Agent-S) · [Simular](https://www.simular.ai/articles/sai-tops-osworld-2-0) |
| Microsoft Fara-7B + MagenticLite | on-device executor | open, MIT | A 7B computer use model (from Qwen2.5-VL) trained on 145 thousand synthetic trajectories: WebVoyager 73.5%, about 16 steps per task against about 41 (November 2025, *company data*). Distilling a large agent into a small model. | [MSR](https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/) |
| Open-AutoGLM (Z.ai) | phone executor | open, Apache-2.0; model MIT | AutoGLM-Phone-9B controls Android through ADB and requires a 24 GB+ GPU; the cloud version cost about 0.2 USD per task (August 2025). A phone or a VM as a sandbox instead of a real desktop. | [repo](https://github.com/zai-org/Open-AutoGLM) |
| Skywork Desktop | office executor | closed (parts open) | Works on designated folders in a local isolated VM, hands over finished documents, slides and spreadsheets; Kunlun's "AI tool business" has over 100 million USD ARR (Q2 2026). Models in the cloud. | [Skywork](https://skywork.ai/desktop/en/index.html) · [36Kr](https://eu.36kr.com/en/p/3878113666724100) |
| Opera Neon | agentic browser | closed | A company from Norway (EEA). The agent reads the DOM instead of screenshots; since 14 August 2026 a free plan for external agents through MCP and Opera Browser CLI — a local agent can drive a real browser. Neon at 19.90 USD/month. | [Opera](https://blogs.opera.com/news/2026/08/your-ai-agents-can-use-opera-neon-free-of-charge/) · [MCP](https://press.opera.com/2026/03/31/opera-neon-adds-mcp-connector/) |
| Fellou + Eko | agentic browser | browser closed, Eko MIT (about 4.96k stars) | The plan is visible and editable before execution, the cost in credits is shown before the start (about 250 credits, i.e. 2–2.4 USD for a complex task, October 2026). Brave showed that page content went to the model automatically. No news in 2026. | [pricing](https://fellou.ai/pricing) · [Eko](https://github.com/FellouAI/eko) |
| Amazon Nova Act | enterprise executor | closed | Billing of 4.75 USD per hour of agent work, and time spent waiting for a human is free; a workflow combines deterministic Python code with natural-language `act()` steps. | [pricing](https://aws.amazon.com/nova/pricing/) · [AWS](https://aws.amazon.com/blogs/aws/build-reliable-ai-agents-for-ui-workflow-automation-with-amazon-nova-act-now-generally-available/) |

### Professionals: law, medicine, programmers, customer service

| Name | Category | Code | Why it is worth knowing | Source |
|---|---|---|---|---|
| Thomson Reuters CoCounsel | law | closed | 1 million users in 107 countries (24 February 2026, *company data*). The new generation rebuilt on the Claude Agent SDK (June 2026), alongside its own "Thomson" model for tabular tasks; an MCP connection to Claude. A hybrid: a small domain model + a large general one. | [LawNext](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html) · [BNN](https://www.bnnbloomberg.ca/business/2026/02/24/thomson-reuters-says-one-million-professionals-using-cocounsel-shares-soar/) |
| Lexis+ AI with Protégé | law | closed | Separates a "general" mode from a "legal with citations" one (Shepard's), and a firm's administrator can switch off the general one; AI products are 90% of new business (23 July 2026). It has a Polish Protégé page with a demo, no price. | [LexisNexis](https://www.lexisnexis.com/community/pressroom/b/news/posts/legal-ai-propels-lexisnexis-to-fastest-growth-in-history) · [PL](https://www.lexisnexis.com/de-at/cee/protege-polska) |
| Microsoft Dragon Copilot | medicine | closed | Dictation + listening to the visit in one tool, sold in DE, FR and NL; "on track for over 100 million visits" in 2026 (Nadella, July 2026). In the UCLA RCT it did not significantly shorten note time (−1.7%), but improved doctors' wellbeing. | [Microsoft](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4) · [launch](https://news.microsoft.com/source/2025/03/03/microsoft-dragon-copilot-provides-the-healthcare-industrys-first-unified-voice-ai-assistant-that-enables-clinicians-to-streamline-clinical-documentation-surface-information-and-automate-task/) · [PubMed](https://pubmed.ncbi.nlm.nih.gov/41497288/) |
| Doximity GPT, ChatGPT for Clinicians | medicine, clinical knowledge | closed | Competitors of [OpenEvidence](01-PROFILES.md#12-openevidence): Doximity brings together over 80% of doctors in the USA (2021) and gives AI away for free, financed by pharmaceutical marketing; OpenAI entered with ChatGPT for Clinicians in April 2026 (per Sacra). | [Wikipedia](https://en.wikipedia.org/wiki/Doximity) · [Sacra](https://sacra.com/c/openevidence/) |
| Devin / Devin Desktop (Cognition) | programmers | closed | A run rate of 1 bn USD passed on 25 September 2026, a valuation of 48 bn USD (8 September 2026); combines an IDE (the former Windsurf) with an agent to which whole tasks are handed off, and bought Poke. A complement to [Cursor](01-PROFILES.md#9-cursor). | [Cognition](https://cognition.com/blog/1b-run-rate) |
| Lovable | programmers and non-programmers (Sweden) | closed | A European company winning globally: ARR on track for about 600 million USD (August 2026), a valuation of 13.3 bn USD. A warning: badly set access rules in Supabase in generated apps exposed data (March 2025). | [VKTR](https://www.vktr.com/ai-platforms/lovable-raises-400-million-at-133-billion-valuation/) · [Wikipedia](https://en.wikipedia.org/wiki/Lovable_(company)) |
| Decagon | customer service | closed | "Agent Operating Procedures": procedures written in natural language by the service team, without development sprints — on my side "when the client sends a demand, first check the deadline…". A valuation of 4.5 bn USD (27 January 2026). | [Decagon](https://decagon.ai/blog/series-d-announcement) |
| Products on the Claude Agent SDK | pattern | SDK closed, products vary | CoCounsel (law) and NanoClaw (a living agent) stand on a lab's harness instead of their own — a fast route to a vertical product. See [Claude](01-PROFILES.md#2-claude). | [LawNext](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html) · [NanoClaw](https://github.com/nanocoai/nanoclaw) |

### Why not in the top tier

- **A category duplicate.** For each pattern we take the one best: Legora and Gaius-Lex lose to Harvey and Noxtua,
  Heidi, Nabla and Dragon to Abridge, Genspark to Manus, UI-TARS, Agent S and Fara to browser-use, NemoClaw and NanoClaw to
  OpenClaw.
- **Unavailable in Poland.** Muse (USA and Canada), Alexa+ (Poland missing from the country list), Siri AI (not on iPhones in the EU,
  no Polish), Ghost (USA). They teach patterns, but the reader cannot test them.
- **No data on the architecture.** Instinct, Grok, Doubao, the Qwen app, Hebbia and Decagon publish little about how they are
  built — for this overview that is the main value.
- **No traction, or too early.** Gaius-Lex (about 502 thousand USD of seed, 6 people), Ghost (pre-order from 5 October 2026),
  Fellou (no news in 2026), NemoClaw ("alpha" status).
- **Engines, not assistants.** DeepSeek, Muse Glimmer, Qwen and Gemma are models — they return in
  [03-TECHNICAL-PATTERNS.md](03-TECHNICAL-PATTERNS.md) and [04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md).
- **Mostly negative lessons.** Consumer Microsoft Copilot (the personality did not sell the product) and Grok (security
  as an add-on) are cautionary tales, not patterns.
