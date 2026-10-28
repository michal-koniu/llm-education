# The AI assistant market — business models, numbers, failures

**As of 11 October 2026.**

This file is the "business" part of the survey: who makes money on AI assistants, what customers pay for, how much it
is all worth, who bought whom and what did not work out. I write it from a single perspective: **I want to sell a local
"on the desk" assistant to Polish professionals** (lawyers, doctors, tax advisers, accountants) and I need to know which
pricing models work, what the customer expects and where the competition has a gap.

> ⚠️ **The numbers in this file go stale within weeks.** Each one has a date and a source. *(company data)* = a claim
> by the company itself (blog, announcement, website), *(press estimate)* / *(Sacra)* = an estimate by journalists or
> analysts. ARR (*annual recurring revenue*) and *run-rate* are revenue from the latest period multiplied up to a year —
> not the same as annual revenue in a financial statement. I did not convert anything at an exchange rate.

Profiles of the top 15 assistants are in [01-PROFILES.md](01-PROFILES.md), technical patterns
in [03-TECHNICAL-PATTERNS.md](03-TECHNICAL-PATTERNS.md), and Polish law, prices and competition
in [04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md).

---

## Table of contents

- [The shortest answer](#the-shortest-answer)
- [1. Market map: four kinds of assistants](#1-market-map-four-kinds-of-assistants)
- [2. Business models and pricing](#2-business-models-and-pricing)
- [3. Numbers: users, revenue, funding](#3-numbers-users-revenue-funding)
- [4. Mergers, acquisitions and 2026 moves](#4-mergers-acquisitions-and-2026-moves)
- [5. Distribution and moats](#5-distribution-and-moats)
- [6. Failures and lessons](#6-failures-and-lessons)
- [7. 2026 trends](#7-2026-trends)
- [8. What this means for me](#8-what-this-means-for-me)
- [Sources of this file](#sources-of-this-file)

---

## The shortest answer

- **The biggest money is in professional assistants, not "general" ones.** Programmers (Cursor, Claude Code,
  Cognition), lawyers (Harvey, Legora) and doctors (Abridge, OpenEvidence) pay the most and the fastest. According to
  Menlo Ventures, coding is 55% of departmental AI spending in companies (2025).
- **A flat per-seat price breaks when an agent works for hours.** The whole market is moving to credits and
  usage-based billing (Cursor 2025, GitHub Copilot 1 June 2026, Glean 2026), and the boldest to **pay per outcome**
  (Sierra).
- **Open environments won the layer of "living" assistants.** OpenClaw has a foundation, and Microsoft built Autopilot
  on it (25 September 2026). Nobody makes money on the code itself — money is made on cloud, models, hardware or
  support.
- **The leaders fine-tune open-weight models** (Harvey Tenet on Kimi K3, Cursor Composer 2 on Kimi K2.5, "Thomson" from
  Thomson Reuters). This confirms the "mid-sized open model + good retrieval + own data" strategy.
- **No leader for professionals runs on the desk, offline.** The market's privacy ceiling in 2026 is "hosting in the EU
  + no training". That is my niche.
- **Polish price anchor:** Beck-Noxtua PLN 590 net/month per user (plus Legalis), Noa Notes PLN 199 + VAT,
  LEX AI PLN 49–489/month. A professional already pays **PLN 200–600 per month per seat** in the cloud.

---

## 1. Market map: four kinds of assistants

Throughout the survey I divide assistants into four kinds. Each has a different business model and different winners.

| Kind | What it does | Leaders (top 15) | Where the money is | Business model |
|---|---|---|---|---|
| **Everyday** | chat, search, writing, voice — for everyone | [ChatGPT](01-PROFILES.md#7-chatgpt), [Gemini](01-PROFILES.md#8-gemini), [Claude](01-PROFILES.md#2-claude), [Perplexity](01-PROFILES.md#15-perplexity) | huge reach (ChatGPT 1.2 bn weekly on 29 Sep 2026, Gemini 1 bn+ monthly on 11 Aug 2026), but the money comes from the expensive USD 200–500 tiers | tiered subscription + API |
| **Professional** | narrow professional work: a court filing, a visit note, code, minutes | [Harvey](01-PROFILES.md#4-harvey), [Abridge](01-PROFILES.md#3-abridge), [Cursor](01-PROFILES.md#9-cursor), [Granola](01-PROFILES.md#10-granola), [Sierra](01-PROFILES.md#11-sierra), [OpenEvidence](01-PROFILES.md#12-openevidence), [Noxtua](01-PROFILES.md#14-noxtua) | **highest revenue per customer and fastest growth** | enterprise licences, seats, usage, outcome, ads |
| **Autonomous executors** | a virtual computer or browser, the agent clicks, writes, hands over a file | [Manus](01-PROFILES.md#6-manus), [browser-use](01-PROFILES.md#13-browser-use), Genspark, ChatGPT Work | fast ARR (Manus USD 100M in 8 months, Dec 2025), but high compute cost | credits + subscription |
| **Autonomous living** | an always-on agent with memory, a schedule and messengers | [OpenClaw](01-PROFILES.md#1-openclaw), [Hermes Agent](01-PROFILES.md#5-hermes-agent), Poke, Lindy, Microsoft Autopilot | money **around** open code: cloud, models, hardware, enterprise editions | foundation, open source + cloud, subscription |

**Where the budgets flow** — the best cross-sectional data I have is from 2025
([Menlo Ventures, 9 December 2025](https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/),
*(analyst estimate)*):

- company spending on generative AI: **USD 37 bn in 2025** (USD 11.5 bn in 2024, ×3.2);
- coding applications: **USD 4.0 bn**, i.e. 55% of departmental spending (up from USD 550M);
- vertical (industry) AI: USD 3.5 bn, of which healthcare about USD 1.5 bn;
- companies **buy** rather than build in 76% of use cases; 27% of application spending arrives through self-service (PLG).

In medicine: AI spending in healthcare USD 1.4 bn in 2025, of which "scribes" (automatic visit notes)
USD 600M; shares: Nuance/Microsoft DAX about 33%, Abridge about 30%, Ambience about 13%
([Menlo Ventures, 21 October 2025](https://menlovc.com/perspective/2025-the-state-of-ai-in-healthcare/), *(analyst estimate)*).

**Takeaway for me:** money is made on **narrow professional work** that someone answers for with their signature. General
chat is the giants' market; a professional buys a ready, checkable work product (a filing, a note, a summary).

---

## 2. Business models and pricing

### Overview of models

| Model | Examples | Pros | Cons | Lesson for me |
|---|---|---|---|---|
| **Tiered subscription** (free / plus / pro / max) | ChatGPT, Claude, Gemini, Perplexity, Poke, Nous Portal | simple, predictable; the expensive tier catches "power users" | the most active users eat the margin; limits have to be added | USD 20 and 200 tiers are today's market standard |
| **Credits** | Manus, Genspark, Lindy, Fellou, Flowith | one unit combines tokens, machine time and APIs; scales with the work | the customer does not know what a task will cost; credits expire | if credits — explain them in "kinds of work", not in tokens |
| **Seat → usage** | Cursor, GitHub Copilot, Glean, Notion, Claude Code | price matches the cost of agents | a pricing change triggers a revolt (Cursor 2025) | announce changes early and clearly; give a limit and a pause instead of a surprise |
| **Per outcome** | Sierra, Intercom Fin, Parloa, Ambience | the customer pays only for the effect; easy sale to the board | "outcome" has to be defined and measured; risk sits with the vendor | works for measurable work (case closed, note accepted) |
| **Free + ads** | OpenEvidence, Doximity GPT | zero entry barrier; huge reach among doctors | dependence on advertisers (pharma); conflict of interest | a model for reach, not for professional secrecy — not my case |
| **Open source + cloud / foundation / BYOK** | OpenClaw, Hermes + Nous Portal, browser-use Cloud, Manus Flex, Kortix | trust, reach, community; the customer can leave with the code | the code alone does not earn; security falls on the user | my product can stand on an open core — you pay for integration, maintenance and support |
| **Enterprise licence / content bundle** | Harvey, Legora, CoCounsel, Abridge, Beck-Noxtua, Microsoft Copilot | high annual contracts; content (commentaries, case law) as a moat | long sales cycle; hidden price | for a firm of 1–10 people a public price list is needed, not "book a demo" |
| **Hardware + software** | Ghost (USD 3,499), Rabbit r1 | one-off sale; "works even if the vendor disappears" | logistics, warranty, updates | this is closest to my product — but hardware must not get ahead of a working agent |

### Subscriptions: the 20 / 200 USD tiers

Almost all everyday assistants have converged on the same tiers:

| Assistant | Tiers (monthly) | Date | Source |
|---|---|---|---|
| ChatGPT | Plus USD 20 · **Pro USD 500** ("25× the Plus limit") | 29 Sep 2026 | [Emergent](https://emergent.sh/news/openai-devday-2026), [Decrypt](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced) |
| Claude | Pro USD 20 · Max USD 100 and 200 · Team USD 20 per seat | 2026 | [Anthropic](https://claude.com/blog/cowork-research-preview) *(company data)* |
| Google AI (prices for Poland) | Plus PLN 23.99 · Pro PLN 97.99 · Ultra PLN 469.99 or 979.99 | Oct 2026 | [Google](https://gemini.google/subscriptions/) |
| Perplexity | Pro USD 20 · Max USD 200 | Aug 2025 | [Vice](https://www.vice.com/en/article/perplexity-comet-plus-announced/) |
| Poke | Pro USD 19 · Ultra USD 199 | 11 Oct 2026 | [Poke](https://poke.com/pricing) |
| Nous Portal (models for Hermes) | Plus 20 · Super 100 · Ultra USD 200 | 11 Oct 2026 | [Hermes](https://hermes-agent.nousresearch.com/) |
| Mistral Vibe | Pro EUR 14.99 · Team EUR 24.99 per user, excl. VAT | Oct 2026 | [Mistral](https://mistral.ai/fr/pricing) |

**Lesson:** the expensive tier (USD 200–500) exists so that agents that work for hours have something to live on.
Perplexity ties its revenue growth from about USD 450M to about USD 750M (Mar → Aug 2026) precisely to the USD 200 tier
and the Computer agent ([PYMNTS](https://www.pymnts.com/news/artificial-intelligence/2026/perplexitys-shift-to-ai-agents-boosts-revenue-50/),
[Yahoo/The Information](https://finance.yahoo.com/technology/ai/articles/nvidia-discusses-perplexity-investment-30-031804276.html),
*(press estimate)*).

### Credits: the unit of "agent work"

A credit combines model tokens, virtual machine time and paid APIs into a single number
([Manus, credit rules](https://help.manus.im/en/articles/11711097-what-are-the-rules-for-credits-consumption-and-how-can-i-obtain-them)).

| Product | Price | What that is per task | Source |
|---|---|---|---|
| Manus | USD 20 / 40 / 200 for 4,000 / 8,000 / 40,000 credits (Sep 2026) | about USD 0.005 per credit (a researcher's calculation) | [myclaw.ai](https://myclaw.ai/blog/manus-2-0) *(a review, not a price list)* |
| Genspark | Plus USD 24.99 (10,000+ credits), Pro USD 249.99 (125,000+) | a "Call For Me" phone call 500 credits ≈ USD 1.25 | [Genspark](https://www.genspark.ai/helpcenter/membership-plans), 11 Oct 2026 |
| Lindy | USD 49.99 per active user (5,000 credits, team pool); USD 10 per 1,000 extra | "daily requests" 2–250, "deep work" 250–1,000 credits | [Lindy](https://www.lindy.ai/pricing), 11 Oct 2026 |
| Fellou | Plus USD 19 (2,000 "Sparks"), Pro USD 39.9 (5,000) | about 250 Sparks ≈ USD 2–2.4 for a complex task | [Fellou](https://fellou.ai/pricing), Oct 2026 |
| browser-use Cloud | USD 0.02 per browser hour + tokens | about USD 0.11–1.64 per task | [browser-use](https://browser-use.com/pricing.md), Sep 2026 |
| Amazon Nova Act | USD 4.75 per agent-hour; waiting for a human is free | — | [AWS](https://aws.amazon.com/nova/pricing/) |

**Good practices from credit price lists:** Lindy describes credits by kinds of work and **stops the agent when the pool
runs out**, instead of issuing a surprise bill; Fellou shows a usage estimate before a task is run;
Manus gives daily "refreshing" credits that build a habit
([Lindy](https://www.lindy.ai/pricing), [Fellou](https://fellou.ai/pricing), [Manus](https://help.manus.im/en/articles/11711097-what-are-the-rules-for-credits-consumption-and-how-can-i-obtain-them)).
Rabbit went the opposite way: "rabbit intern" at USD 99.99/month for 30 tasks, advertised as an alternative to
"confusing credit systems" ([Rabbit, 13 June 2025](https://www.rabbit.tech/newsroom/rabbit-intern-launch)).

### From seats to usage

- **Cursor (Jun 2025):** on 16 June 2025 Pro changed from 500 requests to USD 20 of credit at API prices + an "unlimited"
  Auto mode. Users did not know that "unlimited" applied only to Auto, and received unexpected bills;
  on 4 July 2025 Cursor apologised and refunded the money ([Cursor](https://cursor.com/blog/june-2025-pricing)).
- **Claude Code:** weekly limits announced on 28 July 2025, in force from 28 August 2025 — against 24/7 background work
  and reselling of accounts; according to Anthropic they affected <5% of subscribers
  ([TechCrunch](https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/)).
- **GitHub Copilot:** from **1 June 2026** AI credits (1 credit = USD 0.01) instead of "premium requests"; Pro USD 10
  with credits worth 15 + 5 USD, Max USD 100 with credits worth 200 + 100 USD
  ([GitHub docs](https://docs.github.com/en/copilot/concepts/billing/copilot-requests),
  [pricing](https://github.com/features/copilot/plans)).
- **Glean:** from pure seats to a flat fee for active users + model usage (28 May 2026,
  [TechCrunch](https://techcrunch.com/2026/05/28/gleans-top-line-crosses-300m-as-ai-budget-cutting-becomes-its-major-selling-point/)).
- **Notion:** AI in the higher seat tiers, and "Custom Agents" at USD 10 per 1,000 credits
  ([Notion](https://www.notion.com/pricing)).

Why: Gartner predicts that the **inference cost per agentic workflow will grow more than 5× by 2028**,
even though tokens are getting cheaper (17 August 2026, [Gartner](https://www.gartner.com/en/newsroom/press-releases/2026-08-17-gartner-predicts-ai-inference-costs-per-agentic-workflow-will-increase-more-than-fivefold-through-2028),
*(analyst forecast)*). Agents simply use far more tokens per task.

### Pay per outcome

- **Sierra** (since 10 December 2024): you pay for resolved conversations, saved cancellations, upsells; "if a conversation
  is not resolved, in most cases there is no charge" ([Sierra](https://sierra.ai/blog/outcome-based-pricing-for-ai-agents)).
  The 2026 slogan: "you pay for results, not tokens" ([Sierra Horizon](https://sierra.ai/blog/horizon)).
- **Intercom Fin:** USD 0.99 per outcome ([Intercom](https://www.intercom.com/pricing), *(company data)*).
- **Parloa:** per minute of voice or per chat interaction, "per outcome where it makes sense" ([Parloa](https://www.parloa.com/platform/pricing/)).
- **Ambience Healthcare:** contracts with a bonus tied to the hospital's financial results (Apr 2026, [Ambience](https://www.ambiencehealthcare.com/blog), *(company data)*).

Sierra itself explains its growth by picking narrow "jobs to be done" with a defined measure of success
([Sierra, 6 February 2026](https://sierra.ai/blog/year-two-in-review)).

### Free for the professional, someone else pays

**OpenEvidence** gives doctors a medical search engine for free and earns from pharma and medical-device ads
(CPM USD 70–150). Revenue: about USD 7.9M (Dec 2024) → 50M (Jun 2025) → about USD 300M annualised (Jul–Sep 2026),
gross margin about 90% ([Sacra](https://sacra.com/c/openevidence/), *(analyst estimate)*). The moat is licensed
content (NEJM, JAMA, NCCN), not the model ([Wikipedia](https://en.wikipedia.org/wiki/OpenEvidence)).
Doximity GPT works the same way — free for doctors, financed by pharma marketing
([Wikipedia](https://en.wikipedia.org/wiki/Doximity)).

### Open source + cloud, foundation, BYOK

- **OpenClaw** sells nothing. Since 8 July 2026 it has been run by the **OpenClaw Foundation** (a US 501(c)(3), 12 people
  on staff); donors and partners include OpenAI, University of Michigan (the largest donor), NVIDIA, Microsoft,
  Red Hat, Tencent, Atlassian, Vercel, Cloudflare, GitHub; amounts were not disclosed
  ([foundation](https://openclaw.ai/blog/introducing-openclaw-foundation), *(foundation data)*). OpenClaw Enterprise
  (29 September 2026) "will always be free" ([OpenClaw](https://openclaw.ai/blog/openclaw-enterprise)).
- **Hermes Agent** is free (MIT); Nous Research earns on **Nous Portal** (models and credits), **Hermes Business**
  (shared pool, per-member limits) and **Hermes Enterprise** (on the customer's infrastructure)
  ([Nous Portal](https://portal.nousresearch.com/business)).
- **browser-use:** an MIT library, earning comes from Browser Use Cloud — browser hours, proxies, token resale
  ([browser-use](https://browser-use.com/pricing.md)).
- **BYOK** (*bring your own key* — your own key to the model): Manus Flex (29 September 2026) — the customer pays for the model
  directly, Manus still charges credits for machines and tools ([Manus Flex](https://manus.im/blog/introducing-manus-flex));
  Kortix charges only for the sandbox ([Kortix](https://www.kortix.com/pricing)); OpenHands offers models "at cost,
  with no markup" ([OpenHands](https://openhands.dev/pricing)).
- Exotica: Agent Zero finances development with a cryptocurrency token A0T ([Agent Zero](https://www.agent-zero.ai/p/token/)),
  and nanobot with affiliate links to model providers ([nanobot](https://github.com/HKUDS/nanobot)).

### Enterprise licences and content bundles

Elite legal tools do not publish prices:

- **Harvey:** an estimated USD 1,200 per seat per month for small deployments (minimum 20 seats)
  and USD 100–200 at Am Law 100 scale ([Vaquill](https://www.vaquill.ai/blog/harvey-ai-review-honest-assessment),
  *(external estimate, unverified)*);
- **Legora:** about USD 3,000 per seat per year (minimum 10) ([Layer3](https://www.layer3labs.io/guides/legora-pricing),
  *(external estimate)*);
- **Abridge:** about USD 2,500 per doctor per year ([Sacra](https://sacra.com/c/abridge/), *(analyst estimate)*);
- **CoCounsel** sold in a bundle with Westlaw and Practical Law
  ([Thomson Reuters](https://legal.thomsonreuters.com/en/products/cocounsel-legal/plans)).

Tools for small firms **publish prices**: Clio Work USD 199 per user per month
([LawSites](https://www.lawnext.com/2026/04/clio-work-clios-ai-workspace-is-now-available-to-solo-and-smaller-law-firms-as-a-standalone-product.html)),
Blue J USD 1,498 per year "with no add-ons" ([Blue J](https://www.bluej.com/pricing)). Reference level:
Microsoft 365 Copilot Business USD 18–21 per user per month
([Microsoft](https://www.microsoft.com/en-us/microsoft-365-copilot/pricing)).

---

## 3. Numbers: users, revenue, funding

Only numbers from my research files. "No data" means: I did not find a reliable number, not that none exists.
GitHub stars from the API on 11 October 2026.

### The top 15

| # | Assistant | Users / reach | Revenue / ARR | Funding / valuation | Sources |
|---|---|---|---|---|---|
| 1 | [OpenClaw](01-PROFILES.md#1-openclaw) | ⭐ 391.7k; "4.5 million new claws weekly" (8 Jul 2026, *foundation data*) | does not sell (foundation) | donors, amounts undisclosed | [foundation](https://openclaw.ai/blog/introducing-openclaw-foundation), [GitHub](https://github.com/openclaw/openclaw) |
| 2 | [Claude](01-PROFILES.md#2-claude) | no data | run-rate USD 14 bn, Claude Code >2.5 bn (12 Feb 2026, *company data*); about 44 bn (May 2026, *SemiAnalysis estimate in the press*) | Series G USD 30 bn at 380 bn (12 Feb 2026) | [Anthropic](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation), [iTiger](https://www.itiger.com/hans/news/1183910360) |
| 3 | [Abridge](01-PROFILES.md#3-abridge) | 300+ health systems, 250M+ patients (Jun 2026) | ARR USD 100M (May 2025, *Sacra*) | Series E 300M at 5.3 bn (Jun 2025) + 316M (Apr 2026); about 830M in total | [Sacra](https://sacra.com/c/abridge/), [MobiHealthNews](https://www.mobihealthnews.com/news/abridge-secures-300m-boosts-valuation-53b), [Fortune](https://fortune.com/2026/06/11/abridge-operating-system-medicine-nvidia-eli-lilly-artsight/) |
| 4 | [Harvey](01-PROFILES.md#4-harvey) | 1,500 organisations, 100k+ lawyers (May 2026); 80% of Am Law 100 (9 Sep 2026, *company data*) | ARR >USD 400M (Sep 2026, *press estimate*) | 550M at 15.5 bn (9 Sep 2026) | [Harvey](https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence), [itbrief](https://itbrief.co.uk/story/harvey-launches-500-legal-ai-agents-builder-tool), [raising.fi](https://raising.fi/news/harvey-undisclosed-september-2026) |
| 5 | [Hermes Agent](01-PROFILES.md#5-hermes-agent) | ⭐ 252.7k; "cloned more than 24 million times", "about 2.5% of global token usage" (Oct 2026, *company data*) | no data | Nous Research: USD 90M (Oct 2026) | [Nous](https://nousresearch.com/a-note-on-our-fundraise), [GitHub](https://github.com/NousResearch/hermes-agent) |
| 6 | [Manus](01-PROFILES.md#6-manus) | 80M virtual computers, 147 trillion tokens (Dec 2025, *company data*) | ARR USD 100M (Dec 2025, *company data*); about 450M annualised (Jun 2026, *Sacra, not verified at the source*) | Series B about 75M at about 500M (Apr 2025); round >USD 500M (8 Oct 2026, valuation undisclosed) | [Manus](https://manus.im/blog/manus-100m-arr), [Sacra](https://sacra.com/c/manus), [TechCrunch](https://techcrunch.com/2026/10/08/chinas-manus-raises-over-500m-in-first-funding-round-since-split-with-meta/) |
| 7 | [ChatGPT](01-PROFILES.md#7-chatgpt) | 900M weekly (Feb 2026); 1.2 bn weekly (29 Sep 2026) | USD 13.1 bn booked in 2025; ARR "close to USD 70 bn" (29 Sep 2026, *Axios via Reuters, anonymous source*) | round USD 122 bn at a valuation of USD 852 bn (about 1 Apr 2026) | [Wikipedia](https://en.wikipedia.org/wiki/ChatGPT), [Decrypt](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced) |
| 8 | [Gemini](01-PROFILES.md#8-gemini) | 1 bn+ monthly (11 Aug 2026, *company data*) | not disclosed separately (Google) | — (Google) | [Google](https://blog.google/innovation-and-ai/products/gemini-app/one-billion-monthly-users/) |
| 9 | [Cursor](01-PROFILES.md#9-cursor) | no data | ARR USD 2 bn (Feb 2026, *Bloomberg*); 3 bn (May 2026, *Bloomberg per Wikipedia*) | Series D 2.3 bn at 29.3 bn (13 Nov 2025); SpaceX about 60 bn in shares (closed 14 Aug 2026) | [Bloomberg](https://www.bloomberg.com/news/articles/2026-03-02/cursor-recurring-revenue-doubles-in-three-months-to-2-billion), [Cursor](https://cursor.com/blog/joining-spacex), [Wikipedia](https://en.wikipedia.org/wiki/Cursor_%28company%29) |
| 10 | [Granola](01-PROFILES.md#10-granola) | 250k+ active (mid-2025, *Sacra, unverified*) | undisclosed; ARR +about 250% in Q1 2026 (*aggregator*) | Series C 125M at 1.5 bn (25 Mar 2026) | [TNW](https://thenextweb.com/news/granola-series-c-meeting-ai-enterprise-context), [arr.club](https://www.arr.club/granola/granola-arr-grow-at-250-in-q1-2026) |
| 11 | [Sierra](01-PROFILES.md#11-sierra) | no data | ARR 100M (Nov 2025) → USD 150M+ (Feb 2026, *company data*) | 950M at >15 bn (4 May 2026) | [Sierra](https://sierra.ai/blog/year-two-in-review), [TechCrunch](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/) |
| 12 | [OpenEvidence](01-PROFILES.md#12-openevidence) | 760k doctors, 18M consultations/month (Dec 2025) | about USD 300M annualised (Jul–Sep 2026, *Sacra*) | 250M at 12 bn (21 Jan 2026); about 700M in total | [Sacra](https://sacra.com/c/openevidence/), [Rutland Herald](https://www.rutlandherald.com/news/business/openevidence-raises-250-million-to-build-medical-superintelligence-for-doctors/article_0960939c-ca41-5321-8417-54f84800ece6.html) |
| 13 | [browser-use](01-PROFILES.md#13-browser-use) | ⭐ 117.6k | no data | seed USD 17M (Mar 2025) | [Felicis](https://felicis.com/blog/browser-use-the-tool-making-it-easier-for-ai-agents-to-navigate-websites-raises-17m), [GitHub](https://github.com/browser-use/browser-use) |
| 14 | [Noxtua](01-PROFILES.md#14-noxtua) | 30,000+ users (Sep 2026, *company data*) | prices not public; in Poland PLN 590 net/month (Beck-Noxtua) | Series B USD 92.2M (22 Apr 2025); Series C EUR 100M+ (23 Sep 2026) | [Noxtua](https://www.noxtua.com/news/press-releases/series-c), [TechCrunch](https://techcrunch.com/2025/04/22/noxtua-raises-92m-for-its-sovereign-ai-tuned-for-the-german-legal-system/), [Beck-Noxtua](https://www.beck-noxtua.pl/) |
| 15 | [Perplexity](01-PROFILES.md#15-perplexity) | 100M+ MAU (Mar 2026, *company data*) | ARR about 450M (Mar 2026) → about USD 750M (Aug 2026, *press estimate*) | about 20 bn (Sep 2025); talks with NVIDIA at >30 bn (Aug 2026) | [PYMNTS](https://www.pymnts.com/news/artificial-intelligence/2026/perplexitys-shift-to-ai-agents-boosts-revenue-50/), [Yahoo](https://finance.yahoo.com/technology/ai/articles/nvidia-discusses-perplexity-investment-30-031804276.html), [Wikipedia](https://en.wikipedia.org/wiki/Perplexity_AI) |

### The next ones — for comparison

| Assistant | Users / reach | Revenue / ARR | Funding / valuation | Sources |
|---|---|---|---|---|
| Legora (legal, SE) | about 1,500 customers (Q2 2026) | 100M (Apr 2026) → >USD 200M (Sep 2026, *per the founder, secondary press*) | 600M at 5.6 bn (Apr 2026); talks at about 8.5–10 bn (Aug–Sep 2026) | [TNW](https://thenextweb.com/news/legora-just-hit-100-million-in-revenue-it-took-18-months), [runtimewire](https://runtimewire.com/article/legora-funding-talks-8-5-billion-valuation) |
| Genspark | 2M+ MAU (end of 2025, *Sacra*) | about USD 250M ARR (mid-2026, *company data in the press*) | 485M at 2.6 bn (17 Jun 2026) | [AOL](https://www.aol.com/articles/genspark-unveils-ai-workspace-6-150700000.html), [Yahoo](https://finance.yahoo.com/technology/ai/articles/genspark-ai-extends-series-b-131000248.html) |
| Microsoft Copilot | 30M+ paid seats (FY2026) | not disclosed separately | — | [Microsoft IR](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast) |
| GitHub Copilot | 4.7M paid (Jan 2026, *secondary source*) | not disclosed separately | — | [getpanto](https://www.getpanto.ai/blog/github-statistics) |
| Cognition (Devin, Windsurf) | no data | run-rate USD 1 bn (25 Sep 2026, *company data*) | >2 bn at 48 bn (8 Sep 2026) | [Cognition](https://cognition.com/blog/1b-run-rate), [Wikipedia](https://en.wikipedia.org/wiki/Cognition_AI) |
| Lovable (SE) | 60M projects (Aug 2026) | "on track for" about USD 600M ARR (Aug 2026) | 400M at 13.3 bn (Aug 2026) | [VKTR](https://www.vktr.com/ai-platforms/lovable-raises-400-million-at-133-billion-valuation/) |
| Glean | no data | USD 300M (28 May 2026, with annualised usage) | 7.2 bn (Jun 2025) | [TechCrunch](https://techcrunch.com/2026/05/28/gleans-top-line-crosses-300m-as-ai-budget-cutting-becomes-its-major-selling-point/) |
| Heidi Health (AU, UK/EU) | 2.8M visits weekly (Sep 2026) | ARR USD 50M (Apr 2026) | 100M at 900M + 240M (Sep 2026; Forbes Australia gives about 1.2 bn — the data conflict) | [HLTH](https://hlth.com/insights/news/heidi-raises-340m-to-expand-clinical-ai-into-supervised-agentic-workflows), [Heidi](https://www.heidihealth.com/blog/heidi-series-b) |
| Poke | "hundreds of thousands", >100M messages in 3 months (Jul 2026, *company data*) | no data | 300M after the round (Apr 2026); acquired by Cognition on 23 Jul 2026 | [Cognition](https://cognition.com/blog/interaction), [TechCrunch](https://techcrunch.com/2026/04/08/poke-makes-ai-agents-as-easy-as-sending-a-text/) |
| Mistral (EU) | no data | undisclosed | EUR 3 bn at >EUR 21 bn (Sep 2026) | [Mistral](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/) |
| Cohere + Aleph Alpha | no data | Cohere ARR USD 240M (2025) | together about USD 20 bn; Schwarz 600M (24 Apr 2026) | [TechCrunch](https://techcrunch.com/2026/02/13/coheres-240m-year-sets-stage-for-ipo/), [TechCrunch](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/) |

**How to read it:**

- **The fastest revenue ramps in the history of software** are developer tools: Cursor from USD 100M (Jan 2025)
  to 2 bn ARR (Feb 2026; according to Bloomberg 3 bn, May 2026), Claude Code >2.5 bn run-rate after less than a year.
- **Law is the second hottest vertical:** Harvey from a USD 3 bn valuation (Feb 2025) to 15.5 bn (Sep 2026), Legora from about USD 1M
  to 100M ARR in 18 months ([TNW](https://thenextweb.com/news/legora-just-hit-100-million-in-revenue-it-took-18-months)).
- **Open projects are measured by reach, not revenue.** The numbers of "clones" and "claws" are claims — they cannot be
  verified, but stars and the number of security reports can.

---

## 4. Mergers, acquisitions and 2026 moves

Chronologically, from the end of 2025:

| Date | Move | What it means | Source |
|---|---|---|---|
| 10 Nov 2025 | **Clio** buys **vLex** for USD 1 bn; Series G 500M at 5 bn | legal content is a moat — startups buy or license it | [The Logic](https://thelogic.co/news/clio-series-g-5-billion-legal-tech) |
| 29–30 Dec 2025 | **Meta** acquires **Manus** (about USD 2 bn per the press) | big tech buys a ready executor with a brand | [Yahoo](https://finance.yahoo.com/news/meta-acquire-chinese-startup-manus-233905821.html) |
| 14–15 Feb 2026 | OpenClaw's creator, Peter Steinberger, moves to **OpenAI**; the project is to go to a foundation | a lab "buys" people, not code | [TechCrunch](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/) |
| 25 Feb 2026 | **Anthropic** acquires **Vercept** (perception and computer operation) | the race in *computer use* | [Anthropic](https://www.anthropic.com/news/acquires-vercept) |
| 10 Mar 2026 | **Meta** buys **Moltbook** (a social network for agents) | — | [TechCrunch](https://techcrunch.com/2026/03/10/meta-acquired-moltbook) |
| 24 Apr 2026 | **Cohere** merges with **Aleph Alpha**; valuation about USD 20 bn, Schwarz Group 600M; agreement signed 16 Sep 2026, hosting on STACKIT | the flagship German "sovereign" model is now part of a Canadian company | [TechCrunch](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/), [Cohere](https://cohere.com/blog/cohere-and-aleph-alpha-sign-agreement) |
| **27 Apr 2026** | China's NDRC **blocks** Meta's acquisition of Manus — the first publicly disclosed prohibition in Chinese investment security review | moving the company to Singapore does not protect against Beijing's jurisdiction | [TechCrunch](https://techcrunch.com/2026/04/27/china-vetoes-metas-2b-manus-deal-after-months-long-probe/), [Dahui](https://www.dahuilawyers.com/en/news-insights/chinas-first-public-foreign-investment-security-review-prohibition-the-metamanus-decision/) |
| 4 May 2026 | Sierra: USD 950M at >15 bn | a valuation for the "pay per outcome" model | [TechCrunch](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/) |
| 8 Jul 2026 | The **OpenClaw Foundation** is created (501(c)(3), 12 staff) | an open runtime with a budget and governance, like Linux | [foundation](https://openclaw.ai/blog/introducing-openclaw-foundation) |
| 23 Jul 2026 | **Poke** joins **Cognition** (terms undisclosed) | "personal agent" teams sell for UX and talent, not revenue | [Cognition](https://cognition.com/blog/interaction) |
| 11 Aug and 1 Sep 2026 | **Manus** announces independence; the founders with Tencent, ZhenFund and HongShan buy back Meta's stake at roughly the original price; 8 Oct 2026 a round of >USD 500M | — | [Manus](https://manus.im/blog/a-note-to-our-users), [Manus](https://manus.im/blog/manus-resumes-independent-operations), [TechCrunch](https://techcrunch.com/2026/10/08/chinas-manus-raises-over-500m-in-first-funding-round-since-split-with-meta/) |
| **14 Aug 2026** | **SpaceX** closes the acquisition of **Cursor** (option from 21 Apr, exercised 16 Jun; about USD 60 bn in shares) | the most expensive AI assistant acquisition in this survey | [Cursor](https://cursor.com/blog/joining-spacex), [Wikipedia](https://en.wikipedia.org/wiki/Cursor_%28company%29) |
| 9 Sep 2026 | **Harvey**: USD 550M at 15.5 bn (Diffusion + Lightspeed) | — | [Harvey](https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence) |
| Sep 2026 | **Mistral** EUR 3 bn at >21 bn; **Tandem Health** USD 100M from the EU Scaleup Europe Fund (15 Sep); **Noxtua** EUR 100M+ from C.H.Beck and MANZ (23 Sep) | "sovereign AI" is a funded category | [Mistral](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/), [TNW](https://thenextweb.com/news/tandem-health-100m-series-b-scaleup-europe-fund), [Noxtua](https://www.noxtua.com/news/press-releases/series-c) |
| **25 Sep 2026** | **Microsoft Autopilot** (an evolution of Microsoft Scout) built on OpenClaw; private preview from the end of Sep 2026; Microsoft contributes fixes to the project (policy compliance, Windows/WinUI, Teams, masking of secrets in consent requests) | the open runtime won the platform layer | [OpenClaw](https://openclaw.ai/blog/microsoft-autopilot-openclaw) |
| 6 Oct 2026 | **Sierra + Meta**: Personal Agent Protocol (OAuth for personal agents acting at companies; Shopify, Stripe, Walmart and others) | the infrastructure "on the other side" for agents is being standardised | [Sierra](https://sierra.ai/blog/introducing-personal-agent-protocol) |

**The Windsurf story** (2025) as a cautionary tale: the acquisition by OpenAI fell through, Google paid USD 2.4 bn to hire the
leaders and license the technology, and the rest of the company was signed over to Cognition's acquisition in Jul 2025
([Wikipedia](https://en.wikipedia.org/wiki/Cognition_AI)). Windsurf brought Cognition over 1M users
and 4,000+ organisations *(secondary source)* — distribution was bought.

**The pattern:** the big players do not fight open runtimes, they **absorb** them — they hire the creators (OpenAI),
build products on their code (Microsoft), sell hardware for them (NVIDIA NemoClaw) or buy the teams (Cognition).

---

## 5. Distribution and moats

A moat is what protects a business from being copied. In 2026 a language model **is not a moat** — everyone has access
to similar models. Here is what works.

### Distribution through the OS, browser and messenger

- **Gemini in Chrome and Android:** Google has a browser with about 2/3 of the market, a password manager, Gmail and Calendar;
  the agent works where the user is already logged in. Auto browse reached Chrome on Android on 18 August 2026
  (USA) ([Google](https://blog.google/products-and-platforms/products/chrome/gemini-in-chrome-android-auto-browse/),
  [36Kr](https://eu.36kr.com/en/p/3931781634260099)). All AI browsers together had <1% of the market (Aug 2026).
- **Apple Messages:** Poke was the first AI agent approved on Apple Messages for Business (4 June 2026) —
  "the only AI agent allowed to write natively in Apple Messages" *(company data)*
  ([TechCrunch](https://techcrunch.com/2026/06/04/apple-approves-poke-as-the-first-ai-agent-on-its-messages-for-business-platform/)).
  Lindy got a permanent ban in the same channel (below).
- **WhatsApp, Telegram, Signal and the rest:** OpenClaw and Hermes have gateways to a dozen or so messengers at once — this is their
  main interface ([OpenClaw docs](https://docs.openclaw.ai/llms.txt)).
- **Microsoft 365 and Windows:** 30M+ paid Copilot seats (FY2026) and Autopilot in Teams
  ([Microsoft IR](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast)).
- **EHR in medicine:** Epic introduced its own AI Charting (Feb 2026), and hospitals are "re-evaluating the point of separate
  contracts" ([HLTH](https://hlth.com/insights/news/epic-releases-native-ai-charting-for-integrated-clinical-documentation-2026-02-06)).
  Whoever owns the documentation system owns the scribe customer.

### Data and content

- **Legal content:** at LexisNexis AI products are 90% of new sales (23 July 2026,
  [LexisNexis](https://www.lexisnexis.com/community/pressroom/b/news/posts/legal-ai-propels-lexisnexis-to-fastest-growth-in-history));
  Harvey has an alliance with LexisNexis, Noxtua belongs to C.H.Beck, Clio bought vLex.
- **In Poland** commentaries are controlled by Wolters Kluwer (LEX Expert AI) and C.H.Beck (Legalis → Beck-Noxtua)
  ([prawo.pl](https://www.prawo.pl/prawnicy-sady/wolters-kluwer-przejmuje-libre-dostawce-rozwiazan-ai-dla-prawnikow,535867.html)).
  A local assistant will not beat them on content — it should **complement** their subscriptions by working on the client's own files
  (details in [04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md)).
- **Medicine:** OpenEvidence wins with NEJM, JAMA, NCCN licences, not with a model.

### Habit and workflow

- The winners are those who deliver a **ready, checkable work product** (a filing, a note in the EHR, edits in Word),
  not an answer in a chat. Harvey has add-ins for Word and Outlook, Abridge writes the note straight into the EHR,
  Granola sits in the calendar.
- **Memory per case and per user** (Harvey, Hebbia, Sierra) — the longer a customer uses it, the harder it is to leave.

### Own models (fine-tuned open-weight)

| Company | Model | Base | Effect | Source |
|---|---|---|---|---|
| Harvey | Tenet (20 Aug 2026) | Kimi K3, RL with Fireworks, no customer data | about 1/10 of the cost per review-table cell; −90% cost of a firm-knowledge query | [Harvey](https://www.harvey.ai/blog/post-training-update-harvey-tenet) |
| Cursor | Composer 2 (19 Mar 2026) | Kimi K2.5 + own pretraining and RL (admitted only on 20 Mar 2026) | USD 0.50 / 2.50 per million tokens; competitive results | [Cursor](https://cursor.com/blog/composer-2), [Gigazine](https://gigazine.net/gsc_news/en/20260323-cursor-admits-composer-2-kimi) |
| Thomson Reuters | Thomson (Thomson-1-Large) | open base + Westlaw, Practical Law | claimed wins against frontier models on some legal tests | [LawSites](https://www.lawnext.com/2026/08/thomson-reuters-says-its-homegrown-ai-model-now-rivals-the-frontier-labs-i-take-a-closer-look-at-the-benchmarks.html) |
| Noxtua | Athena Agent (Standard) | open models on sovereign EU infrastructure | a cheaper tier alongside "Minerva" on frontier models | [Noxtua](https://www.noxtua.com/) |
| Canva | own models | — | 17–30× cheaper than external ones (Aug 2026) | [B&T](https://www.bandt.com.au/canva-slashes-revenue-forecast-due-to-ai-spend-being-higher-than-expected/) |

**This is the most important market news for a local assistant:** the leaders themselves show that a mid-sized open model,
fine-tuned on domain tasks and plugged into good retrieval, is enough for many tasks — and is many times
cheaper.

### Trust and compliance

- All the leaders link quotes to sources (CoCounsel, Lexis with Shepard's, Abridge "Linked Evidence", LEX Expert AI).
- The same set of certifications everywhere: SOC 2 Type II, ISO 27001, increasingly ISO 42001; in Germany BSI C5.
- Security enforced **outside the model**: Harvey has an MCP Policy Engine blocking the "lethal trifecta" (access to
  data + untrusted content + an exit channel) ([Harvey](https://www.harvey.ai/blog/building-harveys-mcp-policy-engine)).
- In medicine in the EU the moat is **medical device certification and public procurement**, not privacy alone: Tandem
  has MDR class IIa (21 May 2026), Heidi won the NHS Midlands framework for 70,000 clinicians
  ([TNW](https://thenextweb.com/news/tandem-health-100m-series-b-scaleup-europe-fund),
  [NHS](https://www.dgft.nhs.uk/newspost/nhs-launches-largest-ever-procurement-of-ai-clinical-documentation-covering-70000-midlands-clinicians/)).

### Network effects

- **OpenClaw:** ClawHub (a "skills" marketplace), 391.7k stars, hardware partners — an ecosystem attracts an
  ecosystem. But the same skills marketplace is also an attack surface (section 6).
- **Poke:** shared "recipes" (automations in plain text); the creator gets USD 0.10–1.00 per
  acquired user ([TechCrunch](https://techcrunch.com/2026/04/08/poke-makes-ai-agents-as-easy-as-sending-a-text/)).

---

## 6. Failures and lessons

I learn more from them than from successes — each one says what not to do in a product for a professional.

| Failure | What happened (date) | Lesson for me |
|---|---|---|
| **Rabbit r1** | hardware at about USD 199; after CES 2024, 130,000 units sold, but in Sep 2024 only about 5,000 of ~100,000 owners used the r1 at the same time; "it's just an Android app", leak of hard-coded API keys (Jun 2024) ([Wikipedia](https://en.wikipedia.org/wiki/Rabbit_r1), [The Verge](https://www.theverge.com/2024/9/25/24254253/rabbit-r1-5000-daily-users-ai-gadget)) | **do not ship hardware before the agent works.** A box on the desk makes sense only with finished, tested software |
| **11x** | Mar 2025: logos of companies that were not customers, threat of a lawsuit, poor retention; on 5 May 2025 the CEO steps down ([TechCrunch](https://techcrunch.com/2025/05/05/11x-ceo-hasan-sukkar-steps-down/)) | never inflate customers or ARR; a "digital worker" promises a replacement that the product will not deliver |
| **Artisan** | LinkedIn ban for scraped data (Dec 2025–Jan 2026), the "Stop Hiring Humans" slogan withdrawn ([TechCrunch](https://techcrunch.com/2026/01/07/yes-linkedin-banned-ai-agent-startup-artisan-but-now-its-back/)) | sell **throughput**, not the replacement of people; use data you have a right to |
| **Replit** | Jul 2025: an agent deleted a customer's production database during a "code freeze", against explicit instructions ([Wikipedia](https://en.wikipedia.org/wiki/Replit)) | **hard technical constraints, not instructions in the prompt**: separate environments, undo for every action, consent before anything irreversible |
| **Cursor pricing** | 16 Jun 2025 a change to credits with an "unlimited" Auto-only mode → unexpected bills → apology and refunds on 4 Jul 2025 ([Cursor](https://cursor.com/blog/june-2025-pricing)) | announce a pricing change early, use the word "unlimited" only when it is true; keep a usage meter in view |
| **Canva's costs** | the 2026 growth forecast cut from 30% to 20% because of AI serving costs; then own models 17–30× cheaper (5 Aug 2026, [B&T](https://www.bandt.com.au/canva-slashes-revenue-forecast-due-to-ai-spend-being-higher-than-expected/)) | the cost of frontier models can eat the margin even of a giant; **a local model has a marginal cost close to zero** |
| **Otter and Granola in court** | eavesdropping and biometrics claims against Otter survived a motion to dismiss (13 Aug 2026); Granola sued on 30 Jul 2026 for invisible recording and training by default ([UC Today](https://uctoday.com/productivity-automation/otter-ai-fails-to-dismiss-core-privacy-claims-in-u-s-court/), [PPC Land](https://ppc.land/granola-sued-for-recording-meetings-without-consent-to-train-ai-models/)) | consent to recording **explicit and on by default**; a voiceprint is biometric data (GDPR art. 9) |
| **OpenClaw security** | 722 security reports in 2026 (14 critical, 249 high, 390 medium, 69 low; GitHub API 11 Oct 2026); malicious skills: 341 of 2,857 (Feb 2026) and 1,103 of 14,706 (Mar 2026) in ClawHub audits; OpenClaw 2.0 still with an unencrypted secrets store and the sandbox off by default ([GitHub](https://github.com/openclaw/openclaw), [InsiderLLM](https://insiderllm.com/guides/openclaw-clawhub-security-alert/), [The Register](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492)) | building on OpenClaw, **hardening is my product**: sandbox by default, a closed skills catalogue, encrypted secrets |
| **Lindy on iMessage** | Apple permanently blocked Lindy's Apple ID within half a day; three rewrites of the channel ([Lindy, 16 Mar 2026](https://www.lindy.ai/blog/imessage-api-three-rewrites-one-apple-ban-and-what-actually-works)) | consumer messengers are hostile platforms — an official business API or a channel I control |
| **ChatGPT Atlas** | a browser from 21 Oct 2025, never on Windows or phones; withdrawal announced 9–10 Jul 2026, stopped working on **9 Aug 2026**; "AI browsers should be a feature, not a destination" ([OpenAI forum](https://community.openai.com/t/atlas-is-scheduled-to-stop-working-on-august-9-2026/1389473), [TechCrunch](https://techcrunch.com/2026/07/09/openai-is-shutting-down-atlas-but-its-ai-browser-ambitions-are-still-growing/)) | do not compete for "owning the browser"; compete with a vertical workflow and trust |
| **Project Mariner** | ended on **4 May 2026**, absorbed by Gemini Agent/Spark and auto browse in Chrome ([Wikipedia](https://en.wikipedia.org/wiki/Project_Mariner)) | big companies' experimental agent products disappear — build on stable APIs, not on their apps |
| **Martin** | probably stagnating: in Oct 2026 the site has a Black Friday banner and mockups from Aug 2024, last post 23 Apr 2025 ([Martin](https://www.trymartin.com/blog), *unverified*) | a thin wrapper on other people's models will not survive competition from the labs |
| **Manus: injection via PDF** | 25 Aug 2025: a hidden instruction in a PDF made the agent expose an internal VS Code to the internet and reveal a password, without human consent ([Embrace The Red](https://embracethered.com/blog/posts/2025/manus-ai-kill-chain-expose-port-vs-code-server-on-internet/)) | network tools (ports, outbound internet) only behind a human gate |
| **Claude Cowork: file leak** | Jan 2026: hidden text in a document made the agent send the victim's files to the attacker's account via an **allowed** Anthropic API ([PromptArmor](https://www.promptarmor.com/resources/claude-cowork-exfiltrates-files)) | an allowlist of addresses is not enough when an allowed address accepts arbitrary keys |
| **Hallucinations in courts** | Damien Charlotin's database: 2,184 cases with AI hallucinations (10 Oct 2026), including 6 in Poland ([database](https://www.damiencharlotin.com/hallucinations/)) | every cited source must be checkable (SAOS, ISAP); this is both demand and risk |

**Common denominator:** failures come from a **promise bigger than the product** (11x, Rabbit, Martin), **bad
defaults** (OpenClaw, Granola, Replit) or **dependence on someone else's platform** (Lindy, Atlas, Mariner).
For a professional who answers with their signature, each of these three is disqualifying.

---

## 7. 2026 trends

Each trend with evidence. Technical details — in [03-TECHNICAL-PATTERNS.md](03-TECHNICAL-PATTERNS.md).

### 1. Agents in messengers

- Poke in Apple Messages (4 June 2026), OpenClaw and Hermes with gateways to WhatsApp, Telegram, Signal, Teams.
- Microsoft Autopilot in Teams (25 September 2026); Lindy moved from SMS to a "teammate" in Slack (31 August 2026,
  [Lindy](https://www.lindy.ai/blog/ai-teammate)).
- **What people actually delegate:** "work around work", not life management. In Claude Cowork 33.4% is
  business operations, 16.4% content ([Anthropic, Jul 2026](https://claude.com/resources/articles/how-people-are-using-claude-cowork));
  the morning brief is the universal entry point (ChatGPT Pulse, Google CC, Lindy).

### 2. Background and cloud agents

- ChatGPT **dots** (29 September 2026): always-on agents with their own computer in the cloud
  ([TechCrunch](https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/)).
- Manus 2.0 (28 September 2026): a persistent "Cloud Computer" and event-triggered automations
  ([Manus](https://manus.im/blog/introducing-manus-2-0)).
- Gemini Spark: up to 15 tasks in parallel ([Google](https://support.google.com/gemini/answer/16596215)).
- Cognition calls the Poke purchase a bet on "always-on agents in the cloud"
  ([Cognition](https://cognition.com/blog/interaction)).
- In parallel the **dedicated box** is coming back: Cloudflare wrote about a "wave of Mac mini buying" for OpenClaw (Jan 2026),
  and Ghost sells a local AI computer for USD 3,499 (5 October 2026)
  ([Cloudflare](https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/),
  [TechCrunch](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/)).

### 3. Fine-tuning open-weight models

Harvey Tenet, Cursor Composer 2, Thomson Reuters "Thomson", Noxtua Athena, Canva (section 5). In addition, open
GUI models: Qwen3.8-27B (Apache 2.0) claims 84.3% on OSWorld-Verified (Aug 2026,
[Hugging Face](https://huggingface.co/Qwen/Qwen3.8-27B), *(company data)*). **The model layer is becoming a commodity.**

### 4. Sovereign stacks in the EU

- Money: Mistral EUR 3 bn (Sep 2026), Cohere + Aleph Alpha (Apr 2026), Noxtua EUR 100M+ (Sep 2026), Tandem
  and Lovable with the EU Scaleup Europe Fund.
- Policy: the technological sovereignty package (3 June 2026) and the draft **CADA** with four levels of sovereignty —
  from L1 (data in the EU) to L4 (full control of the supply chain)
  ([European Commission](https://digital-strategy.ec.europa.eu/en/policies/cloud-and-ai-development-act)).
  CADA is still a draft (Oct 2026).
- The limit: an "EU region" at an American provider is L1, not sovereignty; Microsoft's EU Data Boundary does not cover
  Anthropic models ([Microsoft](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy)).
- At the same time some agentic features launch **without the EEA**: Gemini Spark "globally except the EEA, Nigeria, Switzerland
  and the United Kingdom", dots in the Pro tier also without the EEA
  ([Google](https://support.google.com/gemini/answer/16596215), [Emergent](https://emergent.sh/news/openai-devday-2026)).

### 5. Pay per outcome and per usage

Evidence in section 2 (Sierra, Intercom Fin, Parloa, Ambience; Copilot, Cursor, Glean, Notion) and Gartner's forecast
(cost per agentic workflow ×5 by 2028). **The cost risk falls on the customer or the vendor — unless the model is local.**

### 6. AI browsers in retreat

- Atlas closed (9 Aug 2026), Mariner closed (4 May 2026), all AI browsers <1% of the market.
- Gartner (8 Dec 2025): "Cybersecurity Must Block AI Browsers for Now" — the defaults put convenience above
  security ([The Register](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/)).
- OpenAI (22 Dec 2025): prompt injection "is unlikely to ever be fully solved"
  ([TechCrunch](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/)).
- Akamai buys LayerX for about USD 205M (14 May 2026) — AI browser security is becoming a separate market
  ([BankInfoSecurity](https://www.bankinfosecurity.com/akamai-to-buy-layerx-for-205m-to-expand-ai-browser-security-a-31695)).

### 7. Consolidation and platform resistance

- Consolidation: section 4 (Cursor, Poke, Windsurf, Aleph Alpha, vLex, Vercept, Moltbook).
- Platforms defend themselves: Amazon sued Perplexity over shopping in Comet — on 4 August 2026 the Ninth Circuit vacated the injunction,
  holding that the site is "visited" by the user, not by the agent's vendor
  ([Jones Day](https://www.jonesday.com/en/insights/2026/09/ninth-circuit-vacates-cfaa-injunction-against-perplexitys-comet-ai-agent));
  WeChat, Taobao and Alipay blocked the Doubao phone agent (Dec 2025)
  ([Business Standard](https://www.business-standard.com/world-news/bytedance-ai-phone-doubao-nubia-zte-app-blocks-user-control-china-125120800459_1.html)).
- Takeaway: APIs, MCP connectors and the user's own session instead of scraping pages.

### 8. The big players move into verticals

Anthropic extended "Claude for Legal" with domain plugins and connectors to Westlaw, Box and Docusign (12 May 2026,
[TechCrunch](https://techcrunch.com/2026/05/12/the-ai-legal-services-industry-is-heating-up-anthropic-is-getting-in-on-the-action/));
Thomson Reuters is building the new CoCounsel on the Claude Agent SDK
([LawSites](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html)).
Verticals defend themselves with content, workflow and integrations.

### 9. The European gap and weak retention of consumer agents

- **Europe gets new agentic features later or not at all.** As of 11 October 2026 Gemini Spark is not available
  in the EEA, Switzerland and the United Kingdom ([press](https://www.androidheadlines.com/2026/07/google-gemini-spark-expands-to-ai-pro-subscribers.html));
  ChatGPT Health (launched 7 January 2026) and the first "dot" in the Pro plan also exclude the EEA
  ([Wikipedia](https://en.wikipedia.org/wiki/ChatGPT), [blog](https://www.eesel.ai/blog/openai-dots));
  Siri AI (iOS 27, 14 September 2026) is not available on iPhones in the EU because of the DMA dispute
  ([heise](https://www.heise.de/en/news/Siri-AI-in-the-EU-iPhone-and-iPad-users-must-continue-to-wait-11476320.html));
  Alexa+ is not offered in Poland
  ([Amazon](https://www.aboutamazon.com/news/devices/alexa-plus-international-launch), the country is not on the list).
  In Poland ChatGPT Free and Go has had contextual ads since 24 August 2026. This is a gap a local product can enter.
- **A background agent does not mean a habit.** Meta's Muse (launched 8 September 2026, its own cloud virtual machine per user)
  had 5 million downloads in the US in 22 days, but only about 700k daily users at the end of Sep 2026
  ([CryptoBriefing, press](https://cryptobriefing.com/meta-muse-app-store-retention/)); available only in the US and Canada
  ([Meta](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)). Lesson: the mere ability to work in the background does not
  retain the user — a concrete, repeatable benefit counts, like a visit note every day.
- **Muse Glimmer** (10 August 2026, Apache 2.0, about 30 bn parameters, 4-bit on a 24 GB GPU) is Meta's open agentic model;
  its quality in Polish is unverified ([TechCrunch](https://techcrunch.com/2026/08/10/metas-new-glimmer-ai-model-offers-a-hint-at-zuckerbergs-personal-intelligence-vision/), [VentureBeat](https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now)).

---

## 8. What this means for me

Purpose: a local assistant on the desk for a Polish professional (law firm, medical practice, accounting office), data does not
leave the room. The legal background (professional secrecy, GDPR, the AI Act, the Polish AI systems act) is
in [04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md) — this is not legal advice.

### Price anchors in Poland (checked 11 October 2026)

| Product | Price | Where the data is | Source |
|---|---|---|---|
| Beck-Noxtua (law) | **PLN 590 net/month per user**, no token limit; requires Legalis Silver or higher | EU cloud (IONOS, Open Telekom Cloud) | [Beck-Noxtua](https://www.beck-noxtua.pl/), [Noxtua](https://www.noxtua.com/news/press-releases/beck-noxtua-for-the-czech-republic) |
| LEX AI (law, consumers and SMEs) | Standard PLN 49, Premium PLN 120, PRO MAX PLN 489/month; a signed opinion about PLN 320–380 | servers in Poland per the App Store | [App Store](https://apps.apple.com/pl/app/lex-ai/id6748342467?l=pl) |
| Noa Notes (medical scribe) | **PLN 199/month + VAT**, unlimited notes | AWS and Azure | [Noa](https://www.noa.ai/pl/cennik) |
| Mistral Vibe Pro / Team | EUR 14.99 / 24.99 per user, excl. VAT | EU by default | [Mistral](https://mistral.ai/fr/pricing) |
| Google AI Pro (PL) | PLN 97.99/month | Google cloud | [Google](https://gemini.google/subscriptions/) |
| wFirma (accounting) | AI features included in the subscription price | vendor's cloud | [wFirma](https://wfirma.pl/) |
| Gaius-Lex (law, on-prem) | no public price list | SaaS in the EEA, hybrid or on-premise | [Gaius-Lex](https://gaius-lex.pl/) |

**Takeaway:** a professional already pays **about PLN 200–600 per month per seat** for cloud AI. Gaius-Lex is
the closest Polish counterpart of "data does not leave the office", but it targets firms of 20–99 lawyers and project-based
deployments. The segment of a **small office of 1–10 people, a ready box for the desk** — I found nobody in it (this is a
search result, not proof that nobody is there).

### Unit economics: local vs cloud

**Cloud** — cost grows with the agent's work:

- Manus: an input-to-output token ratio of about 100:1, on average about 50 tool calls per task; cached tokens
  cost about 1/10 of regular ones ([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).
- Claude Opus 5.5: USD 4 per million input tokens, USD 20 per million output tokens (22 September 2026,
  [Anthropic](https://www.anthropic.com/news/claude-opus-5-5)).
- **My calculation (example):** a task with 50 steps of 20k input tokens and 500 output tokens is 1M input
  tokens (USD 4) + 25k output (USD 0.50) = **about USD 4.5 without cache**, about USD 0.9 with a cache cutting input
  about 10× (as in Manus's example). A dozen or so such tasks a day per person is hundreds of USD per month (my calculation).
- Long frontier tasks on OSWorld 2.0: USD 15.70–26.62 per task (28 August 2026,
  [Simular](https://www.simular.ai/articles/sai-tops-osworld-2-0), *(company data)*).

**Local** — the cost is upfront, the marginal cost almost zero (electricity and depreciation):

- My machine: 4× Radeon AI PRO R9700, about PLN 8,900 per card ([Ceneo](https://www.ceneo.pl/;szukaj-radeon+ai+pro+r9700),
  11 October 2026) and 300 W per card ([AMD](https://www.amd.com/en/products/graphics/workstations/radeon-ai-pro/ai-9000-series/amd-radeon-ai-pro-r9700.html)); that is **about PLN 35.6k for the cards alone** and up to 1.2 kW
  under full load (my calculation).
- Throughput: 4 agents × 13.6 tok/s = about 54 tok/s of total generation (my calculation). The task mentioned above
  with 25k output tokens is about 30 minutes of generation alone on a single slot — slower than the cloud, but with no token
  bill and no limits.
- Boxes for customers: ASUS GX10 (GB10, 128 GB) from PLN 24,499 ([Ceneo](https://www.ceneo.pl/;szukaj-ascent+gx10)),
  Mac mini M5 Pro from PLN 8,499 ([Apple](https://www.apple.com/pl/shop/buy-mac/mac-mini)), Strix Halo 128 GB
  PLN 13,490–19,999 ([Ceneo](https://www.ceneo.pl/;szukaj-ryzen+ai+max%2B+395+128gb)) — prices from 11 October 2026, comparison
  in [04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md).

**Comparison example** (list prices net, no discounts, excl. VAT — illustration only):

- **3 lawyers on Beck-Noxtua:** 590 × 3 × 24 months = **PLN 42,480** over two years, plus Legalis. One GX10 box
  is **PLN 24,499** plus a support subscription.
- **One doctor on Noa Notes:** 199 × 24 = **PLN 4,776** over two years — less than the Mac mini M5 Pro alone. **For a
  single doctor the argument has to be privacy, not price**; the economics work with a shared box in a clinic
  (3+ doctors).

**A hybrid with Claude Opus 5.5 as the planner** changes the calculation only a little: one planner call with 10k input tokens
and 2k output is about USD 0.08 (my calculation). But then the planner **sees the data** — in professional secrecy mode
the cloud planner may receive only an anonymised task description or nothing at all. I describe the privacy boundary
in [course 1, part 10](../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md)
and [course 2, part 17](../course_agentic_apps/17-HYBRID-AND-ROUTER.md).

### Pricing model — my hypothesis to test

This is **my opinion** based on the facts above, not market data:

1. **A flat licence per seat or per office + hardware**, not credits. With a marginal cost close to zero,
   "no meters, no token limits" is a selling point against usage-based price lists (section 2). Beck-Noxtua
   already advertises "no token limit" — the customer understands it.
2. **Hardware sold at cost or leased, margin on the subscription** (model updates, security
   patches, box replacement, quality tests in Polish before every model change). The pattern: Ghost ("works even
   if the vendor disappears") + Hermes Business (a paid layer around a free core).
3. **A subscription price below the cloud anchors** per seat over 24–36 months, including
   hardware — then the comparison with Beck-Noxtua (PLN 590) wins on paper, and privacy is a bonus.
4. **Do not replace publishers, complement them:** LEX and Legalis stay with the customer; my assistant works on their
   files, emails, KSeF and documentation, to which cloud players have no access (or should not have).
5. **A compliance package as part of the price:** a mapping of § 23e of the Code of Ethics of Advocates (NRA, 12–13 June 2026), a DPIA
   template, a KRiBSI opinion under art. 12 of the Polish AI systems act — details in
   [04-POLAND-AND-SOVEREIGNTY.md](04-POLAND-AND-SOVEREIGNTY.md).
6. **A "pay per outcome" option for later:** e.g. per accepted visit note or prepared filing — only once I can
   measure it reliably (Sierra's lesson: a narrow task, a clear measure).
7. **None of the sins from section 6:** no "will replace the trainee" promises, sandbox and encryption on by default,
   recording only with explicit consent, human consent before every irreversible action, a channel I control.

### Demand signals and market risks

- Poland is at the tail of the EU: 8.7% of Polish companies use AI (GUS, 2025) against about 20% in the EU (Eurostat, 2025), but in professional
  services 23.2% and +8.8 p.p. in a year ([GUS](https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultaktualnosci/5497/1/19/1/spoleczenstwo_informacyjne_w_polsce_2025.pdf),
  [Eurostat](https://ec.europa.eu/eurostat/statistics-explained/index.php/Use_of_artificial_intelligence_in_enterprises)).
- The barriers in the EU are "unclear legal consequences" (52.52%) and "data protection" (48.83%) — exactly what a
  local box solves (Eurostat, as above).
- Risk: 77% of Polish companies without AI will not adopt it "until they have to", every fifth points to cost
  ([PIE, 24 September 2025](https://pie.net.pl/wp-content/uploads/2025/09/2025-09-22_Z-AI-korzysta-mniej-niz-co-szosta-firma-w-Polsce-a-pozostale-nie-planuja-jej-wdrazac-1.pdf)).
- Risk: Polish programmers are among the most sceptical — only 26% trust AI (Stack Overflow 2025,
  [Stack Overflow](https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/)). Trust
  is built with citations, a review step and undo.
- I lack data on the **willingness to pay** of Polish advocates, legal advisers and doctors — I found no Polish studies.
  This is the first thing to check in conversations with customers.

Ranking and profiles — [README.md](README.md) and [01-PROFILES.md](01-PROFILES.md). A survey of open harnesses on which a core
can be built — [../agent-harnesses/README.md](../agent-harnesses/README.md).

---

## Sources of this file

Every number has a link next to it; analyst estimates (Menlo Ventures, Gartner, Sacra) are marked in the text, and the price lists
I checked on 11 October 2026. The full list of sources with a description of what I took from each — [SOURCES.md](SOURCES.md).
