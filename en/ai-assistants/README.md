# AI Assistants — the Top 15 and What to Learn from Them

**As of 11 October 2026.** A review of the best existing AI assistants — open and closed — chosen by market traction
and strength of idea. Purpose: to learn the technical and market lessons before I build my own assistant — for myself
and for Polish professionals who cannot send client data to the USA (a local machine on the desk keeps all the data).

> ⚠️ **This review goes stale within weeks.** Numbers (users, revenue, valuations) carry a date and a source; figures
> published by the companies themselves I mark *(company data)*. GitHub stars from the GitHub API on 11 October 2026.
> **I tested nothing here on my own machine** — this is a review of documentation, announcements and analyses. The
> legal parts are educational material, **not legal advice**.

---

## Table of contents

- [Market map: four kinds of assistants](#market-map-four-kinds-of-assistants)
- [The fifteen](#the-fifteen)
- [The 10 most important lessons](#the-10-most-important-lessons)
- [What this means for a local assistant for Polish professionals](#what-this-means-for-a-local-assistant-for-polish-professionals)
- [How I chose](#how-i-chose)
- [Files in this directory](#files-in-this-directory)
- [Related parts of the repository](#related-parts-of-the-repository)

---

## Market map: four kinds of assistants

| Type | What it does | Leaders among the fifteen | Where the money is |
|---|---|---|---|
| **Everyday** | chat, search, memory, voice, increasingly background tasks | ChatGPT, Gemini, Claude, Perplexity | consumer and business subscriptions, distribution through the OS and the browser |
| **Professional** | one domain, in depth: law, medicine, code, meetings, customer service | Harvey, Abridge, Cursor, Granola, OpenEvidence, Sierra, Noxtua | seats, usage, pay-per-outcome, ads (OpenEvidence) |
| **Autonomous executors** | click, browse, write files and finish the task themselves | Manus, browser-use (and the agentic modes of Claude, ChatGPT, Gemini, Perplexity) | credits per task, API, cloud for open source |
| **Autonomous, always-on** | run continuously in the background, with rare human commands, through messengers | OpenClaw, Hermes Agent | open source + foundation, ecosystem, hosted versions and companies building on them |

Market details, numbers, acquisitions and failures: [02-MARKET.md](02-MARKET.md).

---

## The fifteen

Score 0–100 using the weights from the section [How I chose](#how-i-chose). Full profiles (9 areas each):
[01-PROFILES.md](01-PROFILES.md).

<!-- main-table -->
| # | Assistant | Code | Type | Purpose | Advantage | How it makes money | Offline | Score |
|---|---|---|---|---|---|---|---|---|
| 1 | [OpenClaw](01-PROFILES.md#1-openclaw) | open, MIT, ⭐ <!-- gh:openclaw/openclaw -->391.7k | always-on | personal agent running continuously, controlled from messengers | ecosystem, channels, skills, foundation; the base for Microsoft Autopilot | does not earn by itself — non-profit foundation; companies building on it earn | **Partially** — the core works with a local model, messenger channels need the network | 100 |
| 2 | [Claude](01-PROFILES.md#2-claude) | closed | everyday · professional · executor | work assistant: chat, Cowork, Claude Code, computer use | model quality in agentic tasks and code; MCP and skills | subscriptions and API; Claude Code over USD 2.5 bn annualised revenue (Feb 2026, *company data*); press estimate for the whole company: about USD 44 bn run-rate (May 2026) | No | 97 |
| 3 | [Abridge](01-PROFILES.md#3-abridge) | closed | professional (medicine) | clinical note from the conversation with the patient | "Linked Evidence" — every sentence of the note links to the recording | licences for hospitals | No | 94 |
| 4 | [Harvey](01-PROFILES.md#4-harvey) | closed | professional (law) | law-firm assistant: analysis, document review, workflows | trust of large law firms, own model Tenet | seats in law firms; valuation USD 15.5 bn (Sep 2026) | No | 94 |
| 5 | [Hermes Agent](01-PROFILES.md#5-hermes-agent) | open, MIT, ⭐ <!-- gh:NousResearch/hermes-agent -->252.7k | always-on | personal agent with memory, cron, voice, channels | learns skills from experience, good with local models | open source; Nous Research earns on models and cloud | **Partially** (TTS voice in the cloud by default) | 93 |
| 6 | [Manus](01-PROFILES.md#6-manus) | closed | executor | general agent performing long tasks on a cloud machine | context engineering, a virtual machine per task | credits and subscriptions | No | 93 |
| 7 | [ChatGPT](01-PROFILES.md#7-chatgpt) | closed | everyday · executor | general assistant for everyone | reach and users' habit | subscriptions, businesses, API | No | 87 |
| 8 | [Gemini](01-PROFILES.md#8-gemini) | closed | everyday · executor | Google assistant in Android, Chrome and Workspace | distribution through the OS and Google data; published agent security architecture | Google subscriptions, Workspace | No | 87 |
| 9 | [Cursor](01-PROFILES.md#9-cursor) | closed | professional (developers) | code editor with agents | best-fitting developer workflow, own model Composer | subscriptions and usage; acquired by SpaceX (Aug 2026) | No | 87 |
| 10 | [Granola](01-PROFILES.md#10-granola) | closed | professional (meetings) | meeting notes without a bot on the call | records computer audio locally, note = user's draft + transcript | subscriptions | No | 87 |
| 11 | [Sierra](01-PROFILES.md#11-sierra) | closed | professional (customer service) | customer-service agent for businesses | pay-per-outcome, pass^k evaluation and simulations | fee per resolved case | No | 85 |
| 12 | [OpenEvidence](01-PROFILES.md#12-openevidence) | closed | professional (medicine) | medical answers with citations from the literature | source licences, citations, free for doctors | pharma advertising | No | 84 |
| 13 | [browser-use](01-PROFILES.md#13-browser-use) | open, MIT, ⭐ <!-- gh:browser-use/browser-use -->117.6k | executor | library for agents operating a browser | DOM-based approach instead of screenshots — faster and cheaper | open source + cloud and own model | **Partially** — works with a local browser and model, internet needed for websites | 83 |
| 14 | [Noxtua](01-PROFILES.md#14-noxtua) | closed | professional (law, EU) | legal assistant on a European sovereign cloud | data on EU/CH cloud; Athena tier on open-source models, Minerva on frontier models in a European setup; in Poland as Beck-Noxtua | licences (Beck-Noxtua: PLN 590 net/month) | No (EU cloud) | 78 |
| 15 | [Perplexity](01-PROFILES.md#15-perplexity) | closed | everyday · executor | search with an answer and citations, Comet browser | citations, speed, local agent Portable Computer | subscriptions, businesses, API | **Partially** (Portable Computer) | 77 |
<!-- /main-table -->

Who did not make the fifteen but is worth knowing: [01-PROFILES.md](01-PROFILES.md).

---

## The 10 most important lessons

1. **Trust beats features.** The best professional assistants (Abridge, OpenEvidence, Harvey) tie every answer to a
   source. For a lawyer and a doctor, "show where you know this from" matters more than eloquence.
2. **Workflow, not chat.** Granola, Cursor, Abridge win because they sit where the person already works — in the
   editor, in the consulting room, in the meeting — and not in a separate chat window.
3. **Context is engineering.** Manus and OpenClaw show that an agent's quality depends on what goes into the context
   and in what order (a stable prefix, a plan file, memory in files) — especially important with a local model.
4. **The channel is the product.** "Always-on" assistants work through messengers (Telegram, WhatsApp, iMessage) and in
   the background; for an ordinary user that is more natural than an app.
5. **Autonomy needs brakes.** Approvals scaled to external consequences, a sandbox per task, secrets outside the
   prompt. The 722 OpenClaw security advisories in 2026 are the cost of fast growth without these.
6. **A custom open-weight model is a moat.** Harvey (Tenet) and Cursor (Composer) fine-tune open models on their own
   data — cheaper and better in their domain than a general frontier model.
7. **Evaluation in practice, not in a benchmark.** Sierra measures pass^k — whether the agent does the same thing well
   k times in a row. For an assistant that someone trusts with their clients, repeatability is what counts.
8. **The business model follows the value.** From seats to usage to pay-per-outcome; but sudden pricing changes
   (Cursor) and the cost of frontier models (Canva) can hurt.
9. **Europe is underserved.** Some of the giants' new agentic features skip the EEA, and professional secrecy (art. 6 of the Prawo o adwokaturze (Act on the Bar), art. 3 of the ustawa o radcach prawnych (Act on Legal Advisers)) and § 23e of the Kodeks Etyki Adwokackiej (Code of Bar Ethics) require "due protection" of confidential information, while a cloud in the USA additionally carries CLOUD Act risk — this is a gap for a local product ([04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md)).
10. **Local can make sense.** Open harnesses (OpenClaw, Hermes, browser-use) with a local model work without the
    internet for work on documents and files; the weak spots are fresh knowledge from the web, Polish voice and vision.

---

## What this means for a local assistant for Polish professionals

- **Start with one profession and one workflow** — e.g. a law firm: review of contracts and pleadings with citations
  to the source; a consulting room: a visit note. Models: [Harvey](01-PROFILES.md#4-harvey),
  [Abridge](01-PROFILES.md#3-abridge), [Noxtua](01-PROFILES.md#14-noxtua).
- **Everything on the desk**: model, document search, transcription, memory, logs. Treat the cloud as an exception for
  data unrelated to the client. Architecture and the offline matrix: [03-TECHNICAL-PATTERNS.md](03-TECHNICAL-PATTERNS.md).
- **Citations and verification as a core feature** — the Kodeks Etyki Adwokackiej (Code of Bar Ethics) § 23e (adopted by the NRA (Naczelna Rada Adwokacka, National Bar Council) on 12–13 June 2026; date of entry into force not established) requires personal verification of AI outputs. Legal details and competitors' prices: [04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md).
- **Price anchors in Poland**: Beck-Noxtua PLN 590 net/month per user, Noa Notes PLN 199/month + VAT — a local
  assistant with one-off hardware has to compare with this.
- **My rig** (4 slots of DeepSeek-V4-Flash, text only) is good for a prototype; for a client, a smaller, quiet
  machine for the desk is what counts ([hardware and prices](04-POLAND-AND-SOVEREIGNTY.md)).

---

## How I chose

I reviewed about 60 candidates in five research areas (everyday, executors, always-on, professionals in law and
finance, professionals in medicine, code and other professions) plus the Polish and European market. Each received
scores of 1–5:

| Criterion | Weight | What it measures |
|---|---|---|
| T — traction | 35% | users, revenue, adoption, funding |
| I — idea | 25% | how different it is from competitors and whether the idea held up |
| L — learning value | 25% | how much I can carry over to a local assistant for Polish professionals |
| A — architecture transparency | 15% | how much is known about how it is built (code, documentation, publications) |

Score = 20 × (0.35·T + 0.25·I + 0.25·L + 0.15·A). Constraints: each of the four types at least twice, current products only,
both open and closed, at least one European example betting on privacy (Noxtua). Ties are broken by traction, then by
editorial order (ChatGPT, Gemini and Cursor have 87 pts each and T=5). Next in line: UI-TARS 76, Legora 74, Heidi 74, M365 Copilot 74, Genspark 72, Poke 72.

---

## Files in this directory

| File | Contents |
|---|---|
| [README.md](README.md) | market map, the fifteen, lessons, method |
| [01-PROFILES.md](01-PROFILES.md) | 15 profiles of 9 areas each + "worth knowing" |
| [02-MARKET.md](02-MARKET.md) | business models, numbers, acquisitions, failures, trends |
| [03-TECHNICAL-PATTERNS.md](03-TECHNICAL-PATTERNS.md) | technical patterns, offline matrix, architecture of a local assistant |
| [04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md) | law, professional secrecy, competition in PL and EU, models, hardware, opportunities |
| [SOURCES.md](SOURCES.md) | sources |

## Related parts of the repository

- [Agent harnesses for local models](../agent-harnesses/README.md) — a technical review of harnesses, including
  [Hermes Agent](../agent-harnesses/01-PROFILES.md#4-hermes-agent).
- [Course: agentic applications](../course_agentic_apps/01-AGENT-ARCHITECTURES.md) — architectures, memory,
  [proactivity](../course_agentic_apps/11-SCHEDULING-PROACTIVITY.md),
  [channels](../course_agentic_apps/12-CHANNELS-INTERFACES.md),
  [security](../course_agentic_apps/16-SECURITY-OWASP-ASI.md).
- [Course: local models](../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md) — hybrid of a local model + Claude.
