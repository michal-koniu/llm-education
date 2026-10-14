# The top 10 opportunities, profile by profile

Each profile follows the same shape: how the money flows, where the asymmetry is, what the agent does, how the work
splits between my rig and paid APIs, real numbers, how to start, rules and tax, limitations, and a one-week test with
kill criteria. Facts are as of 14 Oct 2026. The scoring (E earnings 25, A asymmetry 25, F feasibility 15, L legal and
terms 20, R risk 15) is explained in the [README](README.md#how-i-scored). Profiles 11-15 are runners-up that scored below the cut; the rejected candidates are at the end.

**Read the numbers as medians, not promises.** Every platform here has a long tail: a few people earn a lot, most
earn little. My agents only move me up that tail if I measure results honestly
([02-HYBRID-ARCHITECTURE.md](02-HYBRID-ARCHITECTURE.md) shows the ledger I use).

---

## 1. Claiming money you are already owed

**Category:** claims · **Realistic income:** 20-80 USD/month averaged over a year (one or two flight claims plus a few refunds) · **Capital needed:** 0 USD · **Score: 57** (E3 A6 F14 L20 R14) · **Rules:** you file your own claims, so no platform automation rule applies; legal in Poland: yes (for your own claims only)

> An agent that watches your own bookings, receipts and tax forms and files the claims you are entitled to is fully legal and almost risk-free, but the yearly value is small, so it ranks as a useful habit rather than an income source.

**How the money flows.** Airlines pay EU261 compensation to the passenger by bank transfer after a written claim; shops and manufacturers pay refunds or replacements under warranty or price guarantees; the tax office refunds overpaid PIT after a corrected return. Doing it yourself avoids the commission that claim agencies keep. Filing for other people is a regulated business and is out of scope.

**The asymmetry.** Most people never claim: they do not know the rules, lose receipts or give up at the first airline refusal. The paperwork is pure text work (find the booking, check the delay, cite the article, write the letter, follow up after 2 months), which an agent does in minutes. The window does not close: the rights are in EU law. The edge is that you keep 100% instead of paying an agency.

**What the agent does.**
1. Watch: read a dedicated mailbox folder or exported booking confirmations and receipts (local only).
2. Filter: for each flight, check arrival delay of 3+ hours or cancellation under 14 days' notice; for purchases, flag warranty periods and price drops.
3. Work: draft the claim letter citing Regulation 261/2004 Article 7 and the right amount by distance.
4. Verify: paid model checks the "extraordinary circumstances" risk and the letter.
5. Submit: HUMAN GATE. I read and send every claim myself; the agent tracks deadlines and drafts the escalation to the national authority after 2 months.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Parse bookings, receipts, PIT data | all | none | personal data stays on the rig |
| Eligibility check | rules plus model | Opus 5.5 on borderline cases | extraordinary-circumstance calls need judgement |
| Letter drafting | draft | final polish | clear letters get paid faster |
| Deadline tracking | scheduler | none | deterministic |

**Numbers.**
- EU261 compensation: 250 EUR up to 1,500 km, 400 EUR for 1,500-3,500 km, 600 EUR above 3,500 km, for arrival 3+ hours late or cancellation under 14 days' notice; not due for extraordinary circumstances; technical problems and the airline's own staff strikes usually do not count as extraordinary, so compensation is still due *(Your Europe, EU, Oct 2026)*.
- Procedure: written claim to the airline, wait 2 months, then national enforcement body or ADR/small claims *(Your Europe, Oct 2026)*.
- At 4.38 PLN/EUR *(NBP, 13 Oct 2026)* one short-haul claim is about 1,095 PLN.
- Claim-agency commission rates: not found at writing time (agency pages blocked).
- Unclaimed funds and class-action settlements open to Polish residents: no reliable aggregate found; treat as occasional windfalls.

**How to start.**
1. Export the last 3 years of flight bookings and order confirmations to a local folder.
2. Build the parser and eligibility checker; run it on past flights first (claim time limits depend on the court's national law; check Polish limits before filing).
3. Add a yearly PIT checklist step: list the reliefs (ulgi) you may have missed and verify each on podatki.gov.pl before filing a correction.
4. First target: the oldest eligible delayed flight still inside the time limit.

**Rules, tax and risks.**
- Filing your own claims needs no licence; acting for others for a fee is a regulated activity.
- Tax: EU261 compensation is generally treated as compensation, not income, and refunds are not income; confirm in the rules chapter.
- Risks: almost none; airlines may refuse citing extraordinary circumstances, which can need an escalation.
- Privacy: bookings and tax data must stay local.

**Limitations.**
- Value depends on how much you fly and buy; a non-traveller gets near zero.
- Airlines often refuse first; escalation takes months.
- Tax reliefs are claimed once a year and only if you really qualify.
- No compounding: you cannot scale beyond your own life.

**First week test.** Run the checker over 3 years of bookings and receipts. Pass if it finds at least one claim worth 250 EUR or more that is still inside its time limit; send it.

**Kill criteria.** Nothing eligible found in the backlog; then keep only the yearly PIT check.

**Sources:** [Your Europe: air passenger rights](https://europa.eu/youreurope/citizens/travel/passenger-rights/air/index_en.htm) · [Regulation 261/2004](https://eur-lex.europa.eu/eli/reg/2004/261/oj/eng) · [Polish PIT reliefs finder](https://www.podatki.gov.pl/pit/ulgi-odliczenia-i-zwolnienia/) · [NBP EUR rate](https://api.nbp.pl/api/exchangerates/rates/a/eur/?format=json)

---

## 2. Per-task freelance gigs (Upwork, Fiverr, Useme)

**Category:** paid work · **Realistic income:** 0-300 USD/month in months 1-2, 200-800 USD/month median once a profile has reviews · **Capital needed:** ~0-50 USD (Upwork Connects) · **Score: 56** (E8 A9 F12 L16 R11) · **Rules:** AI-assisted allowed (the client buys the result; confidentiality and any client "no AI" instruction must be respected); legal in Poland: yes (Useme invoices for you without a company)

> Selling small fixed-price tasks (document conversion, data cleaning, Excel/Sheets automation, scraping-for-research, DevOps scripts) where an agent does 80% of the work and you review, a real but shrinking and competitive market, so it is a mid-table candidate rather than a gold mine.

**How the money flows.** A client posts a task or buys a gig, pays into escrow, you deliver, the platform
releases the money minus its fee. Upwork: variable 0-15% service fee per contract, locked at proposal time; Connects
cost 0.15 USD each, 10 free per month, standard jobs 2-6 Connects per proposal (2026). Fiverr takes a seller fee
on each order (classically 20%; not re-verified, see Numbers). Useme (Poland) issues the invoice to the client and pays
you on a contract (umowa o dzieło / zlecenie), so no company is needed. Payout: Upwork to PayPal (free on Upwork's side)
or wire (30 USD); Useme to a Polish bank account.

**The asymmetry.** Clients still pay per task for work that is mechanical for an agent: PDF/scan to structured
Excel, deduplicating a CRM export, writing a Google Apps Script, a bash/Terraform fix, a one-off scraper of public
pages. The catch: clients now have ChatGPT too, so the simplest tasks are disappearing. Upwork reported 763,000 active
clients in June 2026, down from earlier periods, and Q2 2026 declines in revenue and gross services volume; it laid off
25% of staff in May 2026 *(Wikipedia summary of company reports)*. The edge is not "using AI" (many sellers already do)
but delivering verified, tested output in hours for tasks with messy real data where a client's own chatbot attempt failed.
The window is narrowing for text tasks; it is wider for "messy data plus code plus verification" tasks.

**What the agent does.**
1. Watch: poll job feeds (Upwork saved searches/RSS where available, Useme listings) for target categories every 30 min.
2. Filter: local model scores each post (clear deliverable? budget per hour of agent+review? data you are allowed to process?
   red flags such as "test task for free" or off-platform payment). Keep the top 3-5 per day.
3. Draft: paid model writes a short, specific proposal plus a 3-line plan; **human approval gate**: you send it yourself
   (Connects are money; never auto-apply).
4. Work: agent converts/cleans/scripts on the rig; client data stays local unless the client agreed to cloud processing.
5. Verify: automated checks (row counts, schema, sample diff, unit tests for scripts), then a paid-model review pass.
6. Deliver: **human gate**: you read the diff/report, deliver, and answer messages yourself.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Feed watch and scoring | yes, 24/7 classification of every post | no | high volume, low difficulty |
| Proposal draft | first draft | final rewrite for tone and accuracy | proposals decide win rate |
| Data cleaning, conversion | yes, all bulk transforms | no | client data stays private, long files |
| Script or code generation | first version and test runs | review of tricky logic | quality where bugs cost reviews |
| Final QA | checklist checks | Opus review of the deliverable | one bad review hurts a new profile |

**Numbers.**
- Upwork service fee 0-15% variable, Connect 0.15 USD, 10 free/month, 2-6 Connects per standard proposal (2026, golance.com and Upwork resources page, verified 27 May 2026).
- Freelancer Plus 19.99 USD/month incl. 100 Connects (2026, Upwork pricing summary).
- Upwork withdrawal: wire 30 USD, PayPal free on Upwork's side (27 May 2026, golance.com).
- Upwork: 763,000 active clients June 2026; 25% layoff May 2026; Q2 2026 declines (Wikipedia, read 14 Oct 2026).
- Fiverr buyer fee about 5.5% + 2.50 USD per order (2026, golance.com). Fiverr seller fee: not re-verified (official terms page returned 403 on 14 Oct 2026).
- Useme fee level: not found (pricing page returned 403 on 14 Oct 2026).
- Proposal win rates for new profiles: not found from a fetchable source.

**How to start.**
1. Pick 2 narrow offers you can verify automatically: "messy Excel/CSV/PDF to clean dataset in 24 h" and "small DevOps/automation script with tests".
2. Create a Useme account (Polish clients, no company) and an Upwork profile; complete ID verification.
3. Build the job-scoring agent first (read-only, no auto-apply); log every post and score.
4. Prepare 2 portfolio samples on public/synthetic data that show before/after and the test report.
5. Send 3-5 hand-approved proposals per day for 2 weeks; take the first jobs at a low fixed price to earn reviews.

**Rules, tax and risks.**
- Platform rules: automated proposal sending and scraping of the platform itself are typically against marketplace terms; keep the agent on the work, not on the platform account. Respect a client's explicit "no AI" or confidentiality instruction (and NDAs) and do not paste client data into third-party APIs without consent; the local model avoids most of this.
- Polish law: via Useme you are paid on a civil-law contract (they handle invoicing). Directly from Upwork/Fiverr without a company you report the income yourself as income from other sources or under "działalność nierejestrowana" if within the limit; check 03-RULES-TAX-RISKS.
- Tax in one line: progressive PIT (12%/32%) on income from Useme/foreign platforms, settled in your annual return; details in the rules chapter.
- Risks: unpaid time on proposals, a bad early review, scope creep, clients who expect free revisions.

**Limitations.**
- Your human time (messages, revisions) caps volume at maybe 3-6 small jobs per week on 10 h.
- Demand for the easiest AI-able tasks is falling as clients self-serve with chatbots.
- Many competing sellers already use ChatGPT; the asymmetry is in verification and speed, not access to AI.
- New profiles face a cold start; first jobs often pay little.
- Connects and fees eat 10-20% of small tickets.

**First week test.** Run the scoring agent for 7 days and send 15 hand-approved proposals for the two offers; pass if at least 1 paid job is won and delivered with under 2 hours of your own time.

**Kill criteria.** Stop if after 6 weeks and 60 proposals the net is below 100 USD/month or your time per job exceeds 3 hours.

**Sources:** [Upwork: Is Upwork free (2026)](https://www.upwork.com/resources/is-upwork-free) · [goLance: Upwork fees explained 2026](https://golance.com/blogs/upwork-fees-explained-2026) · [Wikipedia: Upwork](https://en.wikipedia.org/wiki/Upwork)

---

## 3. Data science and AI competitions

**Category:** contests · **Realistic income:** 0-200 USD/month averaged over a year (median case: 0, with rare lumps of 1,000-10,000 USD) · **Capital needed:** 0 USD (the local rig covers training and offline inference) · **Score: 56** (E4 A10 F12 L18 R12) · **Rules:** AI-assisted coding allowed; external LLM APIs often banned at evaluation time; legal in Poland: yes

> Entering prize competitions (Kaggle, DrivenData, Zindi, AIcrowd, ARC Prize) with coding agents running many experiments in parallel on the local rig; fully legal and a real fit for 128 GB of VRAM, but prizes go to the top few of hundreds or thousands of teams, so the median month is zero.

**How the money flows.** A host (company, agency, foundation) funds a prize pool split across the top 3-5 leaderboard places, sometimes plus paper or special awards. Winners usually must hand over or open-source code and a write-up before payout. ARC Prize 2026 requires winners to "open source their solutions before receiving official private evaluation scores" under permissive licenses (arcprize.org, read 14 Oct 2026). Payout by bank transfer after identity and tax forms, typically weeks to months after the final leaderboard. Some government-funded prizes are restricted by country (check eligibility per competition; for the DOE GEMS challenge it was not stated on the listing page).

**The asymmetry.** Moderate, and it lives in the small competitions. The ML Contests report found the median competition had only 36 teams in 2025, against 3,700+ teams in the most popular one (Jane Street); more than half of 2025 winning teams were a single person and over 50% were first-time winners (third-party report). So the edge is: an agent that watches 30+ platforms, finds low-entry competitions, and runs dozens of experiments overnight on the local GPUs, where most entrants iterate by hand. On Kaggle's flagship competitions, top teams already use coding agents, so expect no edge there. Window: as long as small hosts keep posting niche tasks; slowly closing as agentic ML tooling spreads (estimate).

**What the agent does.**
1. Watch: aggregate new competitions daily (Kaggle, DrivenData, Zindi, AIcrowd, plus aggregator lists); store prize, teams, deadline, eligibility, rules on external data/models/APIs.
2. Filter: keep prize per team high (e.g. above $500 per team), Polish residents eligible, no evaluation-time API need, task fits local hardware.
3. Work: agent builds baseline, then runs an experiment queue (features, models, ensembles) across the 4 GPU slots 24/7; logs every run with CV score.
4. Verify: trust only cross-validation that tracks the public leaderboard; Opus 5.5 reviews leakage and overfitting risks weekly.
5. **Human gate:** you read the rules for each data source and model license, choose the final 2 submissions, and handle the winner's code and paperwork.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Competition watch and rules parsing | Yes, 24/7 | No | Bulk text, low stakes |
| Experiment code and overnight runs | Yes | No | GPU time is free locally |
| Strategy, leakage and CV review | No | Opus 5.5 weekly | Few calls, high leverage |
| Inference inside the submission | Local open-weight models only | Not allowed in many rules | ARC Prize 2026 bans API systems at evaluation |

**Numbers.**
- 2025 across 30+ platforms: over $16M in prizes, 390+ competitions, average ~$41,000 per competition, median 36 teams per competition; 23 competitions with $100k+ pools (ML Contests, State of ML Competitions 2025, third-party report).
- Kaggle in 2025: 68 competitions, $3.668M prize money, 29M+ users (same report).
- ARC Prize 2025: 1,455 teams, 15,154 entries; top-score prizes $25,000, $10,000, then $5,000 for 3rd-5th; two of the top five were solo; paper awards $50,000 / $20,000 / $5,000 (arcprize.org results, read 14 Oct 2026).
- ARC Prize 2026: $2M across 3 tracks, submissions due 2 Nov 2026, results 4 Dec 2026; "Internet access is not available during Kaggle evaluation (no API-based systems like GPT/Claude/etc.)" (arcprize.org, read 14 Oct 2026).
- DrivenData GEMS Prize Challenge (US DOE): $300,000, 593 joined, about 7 weeks left (drivendata.org, 14 Oct 2026).
- Hackathons: ETHGlobal's next hackathon (Mumbai, 5-7 Nov 2026) is in-person and its prize pool is not listed (ethglobal.com, 14 Oct 2026); the Devpost listing could not be read (HTTP 403). Not counted here.
- Winner text-model choice in 2025: nearly all text-competition winners used Qwen models (ML Contests 2025) which means open-weight models that run on a local rig like this one.

**How to start.**
1. Create Kaggle, DrivenData, Zindi and AIcrowd accounts; verify phone/identity where required.
2. Build the watcher and a rules checklist (eligibility, external data, model licenses, API use, team limits).
3. Pick one live competition with fewer than 100 teams and a deadline at least 4 weeks out.
4. Set up the experiment runner on the rig with fixed CV and experiment logging.
5. Use one "practice" competition to calibrate CV vs leaderboard before chasing money.

**Rules, tax and risks.**
- Rules differ per competition: some ban external APIs or prompting pre-trained LLMs (example: PARADOX ML Challenge, third-party listing); ARC Prize bans evaluation-time APIs. Check each rules page for limits on accounts, teams and private code sharing.
- Legal in Poland: yes. Tax: a prize from a foreign host is personal income for a Polish tax resident (PIT-36); details in the rules chapter.
- Risks: months of work with no prize; leaderboard shake-up between public and private scores; winner obligations (open-sourcing, license transfer).

**Limitations.**
- Top-heavy: prizes go to 3-5 teams per competition.
- Big Kaggle competitions are already full of agent-assisted teams.
- Some government prizes exclude non-US residents.
- 10 h/week of human time limits how many competitions you can follow.
- Evaluation-time API bans mean the paid model helps only offline.

**First week test.** Enter one live competition with fewer than 100 teams; run the agent for 7 days. Pass if your best submission is in the top 25% of the public leaderboard. **Kill criteria.** Stop after 3 competitions with no top-10% finish.

**Sources:** [ML Contests: State of ML Competitions 2025](https://mlcontests.com/state-of-machine-learning-competitions-2025/) · [ARC Prize 2026](https://arcprize.org/competitions/2026) · [ARC Prize 2025 results](https://arcprize.org/blog/arc-prize-2025-results-analysis) · [DrivenData competitions](https://www.drivendata.org/competitions/) · [ETHGlobal events](https://ethglobal.com/events) · [PARADOX ML Challenge](https://gdg.community.dev/events/details/google-gdg-on-campus-jamia-millia-islamia-delhi-india-presents-paradox-ml-challenge)

---

## 4. AI red-teaming bounties and arenas

**Category:** bounties / contests · **Realistic income:** 0-300 USD/month median (lumpy: most months 0, an occasional 500-2,500 USD finding) · **Capital needed:** ~0-100 USD (API judge tokens) · **Score: 55** (E5 A12 F13 L16 R9) · **Rules:** automation not banned in the 0DIN policy, but every report must be a reproducible human-written write-up; arena/competition rules vary per event and must be read each time; legal in Poland: yes (testing inside an authorized program)

> Paid jailbreak and prompt-injection research for AI labs and arenas; an agent with an uncensored local model can try thousands of attack variants a day, but payouts are rare, lumpy and dominated by a small expert group, so it is a skill-building side bet, not a steady income.

**How the money flows.** Three kinds of payer. (1) Open bug bounties: Mozilla's 0DIN pays 500-15,000 USD per verified GenAI flaw, paid within 30 days of agreement, ID and W-8BEN tax form required. (2) Lab programs: Anthropic (via HackerOne) and OpenAI run jailbreak bounties that are mostly invite-only. (3) Timed competitions with prize pools: Gray Swan Arena, HackAPrompt 2.0, Kaggle red-teaming challenges. Prizes go to leaderboard ranks or "first to break" a target.

**The asymmetry.** Most arena players still type attacks by hand in a chat box. An agent can generate, mutate and score attack variants around the clock on a local model that has no per-token cost and no safety filter of its own, while a paid model acts as an accurate judge ("did the target really leak the forbidden output?"). The catch is that the top of every leaderboard already uses scripts. Gray Swan reports more than three million attack attempts across its network *(platform claim, 2026)*. So the asymmetry is versus the casual majority, not versus the winners. Window: open while labs keep paying for human-found jailbreaks; it narrows as labs automate their own red-teaming.

**What the agent does.**
1. Watch: poll 0DIN scope pages, Gray Swan / HackAPrompt event pages and Kaggle for new targets; summarise rules (automation allowed? rate limits? disclosure?) for a human to read.
2. Filter: drop events whose rules forbid scripted submissions or API access; keep only in-scope models and harm categories.
3. Work: local model generates attack candidates from a seed library of public technique families; runs them against the target only through the official interface and within rate limits.
4. Verify: paid model judges each response against the program's success criteria; dedupe against known public jailbreaks (0DIN splits bounties on duplicates within 7 days).
5. Submit: HUMAN GATE. I read every candidate, reproduce it by hand, write the report (0DIN asks for a short abstract first) and submit myself.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Rules and scope digest | first-pass summary | Opus 5.5 check of automation clauses | a misread rule can disqualify everything |
| Attack generation | all variants, 24/7 | none | volume, no refusal, no token cost |
| Success judging | coarse filter | final judge on shortlist | judge accuracy decides what you report |
| Dedup vs public jailbreaks | embedding search | none | private and cheap |
| Report write-up | draft | Opus 5.5 review | report quality affects payout level |

**Numbers.**
- 0DIN reward tiers: Low up to 500, Medium up to 2,500, High up to 5,000, Severe up to 15,000 USD; payment within 30 days of agreement; 2-week validation; duplicates within 7 days split the bounty *(policy, updated 2 Oct 2026, 0din.ai)*.
- Anthropic: up to 15,000 USD for universal jailbreaks, invite-only, HackerOne *(Aug 2024)*; up to 25,000 USD on Claude 3.7 Sonnet classifiers, invite-only *(May 2025)*.
- OpenAI: only 6 safety findings rewarded since July 2024, average payout in the last 3 months 250 USD *(third-party report, EA Forum, 2 Jun 2025)*.
- HackAPrompt: "over 100,000 USD" given away, 30K+ competitors in 150+ countries; one top player won 28K+ USD across events *(platform claim, Oct 2026)*. With 30K competitors the median participant wins nothing.
- Gray Swan Arena: current prize pools not retrievable at writing time (site rate-limited, Oct 2026): check the live challenge page.

**How to start.**
1. Create accounts on 0DIN, Gray Swan Arena, HackAPrompt and Kaggle; read each event's rules and save them to a file.
2. Prepare for payout KYC: passport photo ID and a W-8BEN form (non-US person) for 0DIN.
3. Build the harness: target adapter (official API or web UI only where allowed), local generator, paid judge, SQLite log of every attempt.
4. First target: a live Gray Swan or HackAPrompt beginner challenge that allows API use, to calibrate the judge before going after 0DIN bounties.

**Rules, tax and risks.**
- 0DIN: no clause against automated tooling found, but payment needs a "contractual agreement" and photo ID; researchers in sanctioned regions excluded *(policy, Oct 2026)*.
- Lab programs: invite-only, NDA-bound; testing a production model outside a program is not covered by safe harbour and can break the provider's usage policy.
- Polish law: testing inside an authorized program is not unauthorized access; stay strictly inside scope (see `../course_agentic_apps/16-SECURITY-OWASP-ASI.md`).
- Tax: prizes from contests are taxed under PIT rules for prizes or other income depending on the form; bounties for reports are usually "other income" (details in the rules chapter).
- Risks: account bans for exceeding rate limits, duplicate findings, zero months.

**Limitations.**
- Winner-take-most: a few experts take most prize money.
- Generated harmful content must stay private: store it encrypted, never publish.
- Labs patch quickly; a working jailbreak can be dead before validation.
- Arena events are irregular; there is no steady flow of work.

**First week test.** Run the harness on one open challenge for 7 days. Pass if the judge-confirmed success rate is above 1 per 1,000 attempts AND at least one break is accepted by the arena scoreboard.

**Kill criteria.** No accepted break or paid finding after 8 weeks of agent runtime.

**Sources:** [0DIN policy](https://0din.ai/policy) · [0DIN announcement, Mozilla Hacks](https://hacks.mozilla.org/2024/08/0din-a-genai-bug-bounty-program-securing-tomorrows-ai-together/) · [Anthropic model safety bounty](https://www.anthropic.com/news/model-safety-bug-bounty) · [Anthropic 2025 bounty](https://www.anthropic.com/news/testing-our-safety-defenses-with-a-new-bug-bounty-program) · [EA Forum critique of AI safety bounties](https://forum.effectivealtruism.org/posts/xAWKpgiTFF9ruEpsz/critique-of-current-ai-safety-bug-bounty-programs) · [HackAPrompt](https://hackaprompt.com/) · [Gray Swan](https://www.grayswan.ai/)

---

## 5. AI forecasting tournaments (the legal side of prediction markets)

**Category:** contests · **Realistic income:** 0-150 USD/month median case (prizes are seasonal and lumpy) · **Capital needed:** 0 USD (sponsored LLM credits) · **Score: 55** (E3 A8 F13 L18 R13) · **Rules:** automation allowed (the FutureEval tournament is for bots only); legal in Poland: yes for prize tournaments, NO for real-money Polymarket/Kalshi trading

> Real-money prediction markets are closed to a Polish resident, so what remains is the Metaculus FutureEval bot tournament: legal, free to enter and built for agents, but the field is already 100+ bots, so it is a skill-building contest with small expected prize money, not an income line.

**How the money flows.** Metaculus pays a 50,000 USD prize pool per FutureEval season to non-Metaculus bot makers, about 175k USD a year across tournaments (Spring 2026 results post, Sept 2026). Prizes go to the top of the leaderboard after questions resolve. Spring 2026 resolved in May and payouts were targeted for June/July 2026, so money arrives months after the work. Winners must fill in a strategy survey to get paid. How the pool is split by rank: not found.

**The asymmetry.** There is none in the usual sense. This is a contest where every entrant is a bot: Spring 2026 had 173 bots, 111 of them external, on 297 scored questions (EA Forum, 9 Sept 2026). The edge here is agent scaffolding (research pipelines, ensembling, calibration), not "using AI at all". Metaculus reports the human-pro advantage is "nearly gone", and a plain non-agentic GPT-5.1 bot ranked only 18th, so better scaffolding beats a raw model. The real-money side (Polymarket) is where manual traders still dominate, but it is not legally open to the reader (see rules).

**What the agent does.**
1. Watch: poll the tournament API for newly opened questions.
2. Research: run several news searches per question, pull base rates and prior resolutions.
3. Forecast: 3-5 independent forecasts per question, then aggregate (median, extremised slightly).
4. Verify: sanity check (probabilities sum to 1 on multi-choice, no 0/1 extremes, dates parsed right).
5. Submit through the API. No money moves, so no human gate per forecast; a human reviews the weekly calibration report.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Question triage and news summarising | yes, 24/7 on 4 slots | no | bulk text, private, free |
| Base-rate lookup and draft rationale | yes | no | long context, many calls |
| Final probability | no | sponsored frontier models (credits from the organiser) | Spring 2026 top 10 all used GPT-5.x; a local model of Index 34 will not place |
| Weekly review of calibration | no | Opus 5.5 | hard reasoning, low volume |

**Numbers.**
- Prize pool: 50,000 USD per season; ~175k USD/year across FutureEval (EA Forum results post, 9 Sept 2026; Metaculus Substack).
- Field: 173 bots, 111 external, 297 scored questions in Spring 2026 (EA Forum, 9 Sept 2026).
- Summer 2026 season: started 18 May 2026, 300-500 questions; free credits from Anthropic, Google and OpenAI, with a request to use fewer OpenAI credits (LessWrong announcement, 2026).
- Winning stack: GreeneiBot2 used parallel research (AskNews, Perplexity, GPT-5 search); every top-10 survey responder used GPT-5.2 or newer (EA Forum, 9 Sept 2026).
- Prize by rank and median prize per bot: not found. With 111 external bots, most entrants win nothing.

**How to start.**
1. Create a Metaculus account and register a bot for the current FutureEval season; apply for sponsored credits.
2. Fork the Metaculus template bot, run it unchanged for one week to get a baseline.
3. Add the local research stage (news fetch + summarise on the rig), keep the final forecast on a sponsored frontier model.
4. Log every forecast; score against resolved questions; iterate weekly.

**Rules, tax and risks.**
- Polymarket lists Poland as "Close-Only": users "cannot open new positions" (Polymarket geoblock docs, read 14 Oct 2026). France blocked it via ISPs on 16 July 2026; the Netherlands also blocked it (press, 2026).
- Polish gambling act (ustawa o grach hazardowych, art. 2 ust. 2) treats bets on "zaistnienie różnych zdarzeń" as zakłady wzajemne needing a Polish licence; art. 107 of the fiscal penal code (kks) fines a player who takes part in unlicensed or foreign gambling. Using a VPN to reach Polymarket would break both its terms and Polish law. Kalshi: Poland not listed in its help pages (not found); treat as unavailable.
- Manifold is play money only; Metaculus Cup and FutureEval pay real prizes for forecasting skill, not wagers.
- Tax: a prize from a contest is taxed in Poland (details in 03-RULES-TAX-RISKS.md).
- Risks: zero prize for months, prize rules change each season, credit sponsorship can end.

**Limitations.**
- The tournament is already 100% bots; you are competing on scaffolding with research teams.
- Prize split by rank is not published in what I found; median entrant likely gets 0.
- Payout lag of 1-3 months after a season ends.
- Local model is too weak for the final call; the edge depends on sponsored frontier credits.
- Value is mainly portfolio and skill (forecasting agents), not cash.

**First week test.** Run the template bot plus local research stage on every open question for 7 days. Pass if the bot submits on ≥90% of open questions and its Brier/log score on already-resolved practice questions beats the template baseline.

**Kill criteria.** Stop if after one full season the bot is outside the top 20 of external bots.

**Sources:** [Polymarket geoblock](https://docs.polymarket.com/developers/CLOB/geoblock) · [FutureEval Spring 2026 results (EA Forum)](https://forum.effectivealtruism.org/posts/iJ3qBDwpWCfNy9ZGd/pros-beat-bots-but-the-gap-is-nearly-gone) · [Summer 2026 FutureEval announcement](https://www.lesswrong.com/posts/E7wxQnBvYxgB3rTTk/announcing-metaculus-summer-2026-futureeval-bot-tournament) · [Metaculus FutureEval](https://metaculus.substack.com/p/metaculus-futureeval-ai-forecasting-benchmark) · [France blocks Polymarket](https://xyz.pl/dzieje-sie/francja-blokuje-dostep-do-polymarket-1050) · [Netherlands blocks Polymarket](https://yellow.com/pl/news/niderlandy-blokują-polymarket-i-grożą-karami-do-840-tys-euro-–-rynki-predykcyjne-tracą-bezpieczne-przystanie) · [Ustawa o grach hazardowych (ISAP)](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU20092011540) · [Kodeks karny skarbowy (ISAP)](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19990830930)

---

## 6. Bailiff and public auctions

**Category:** arbitrage · **Realistic income:** 0-400 USD/month (median ~150 USD after a slow first quarter) · **Capital needed:** 1,000-2,000 USD revolving (deposits plus purchase price) · **Score: 52** (E7 A14 F8 L16 R7) · **Rules:** automation in ToS: not verified for the bailiff portal, use low-rate reading of public notices; legal in Poland: yes, bidding needs PESEL and real identity

> Reading hundreds of bailiff and state-agency auction notices and appraisals is slow, boring paperwork, which is exactly what an agent does well; the capital limit and thin, lumpy margins keep it mid-table.

**How the money flows.** You buy a seized or surplus item (car, tools, electronics, machinery) at a court-bailiff auction or a state-agency tender, then resell it on Allegro/OLX. In a bailiff auction of movables the starting price is fixed by law: "Cena wywołania w pierwszym terminie licytacji publicznej wynosi trzy czwarte wartości szacunkowej" and at the second term "połowę wartości szacunkowej" (art. 867 § 2 KPC, t.j. Dz.U. 2026, read 14 Oct 2026). Your margin is the gap between that price plus costs and the real resale price. Money arrives only when you resell, often weeks later.

**The asymmetry.** Notices sit on the bailiff portal (licytacje.komornik.pl), the Military Property Agency (AMW) site and its tender platform, and in PDFs of appraisals (operaty szacunkowe). Most bidders are local dealers who read a few notices in their own area by hand. An agent can read every new notice nationwide each day, extract the appraisal, condition notes and photos, and compare against resale prices. No source was found on how many bidders already automate this (not found); the paperwork-heavy format suggests few do. The window stays open as long as notices are PDFs and free text.

**What the agent does.**
1. Watch: once a day, read new notices from the bailiff portal and AMW listings at a polite rate (check each site's terms first).
2. Filter: keep categories you can resell and transport; drop items above your capital or outside driving range.
3. Work: extract appraisal value, starting price (3/4 or 1/2), deposit, viewing date, defects; estimate resale price from comparable listings you check by hand.
4. Verify: paid model re-reads the appraisal for legal traps (co-ownership, missing documents, VIN problems on cars).
5. Act: human approval gate. You decide, pay the deposit and bid yourself; the agent never bids.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Daily notice reading | Parse notices, OCR'd PDFs, extract fields | None | Bulk, cheap, 24/7 |
| Photo and condition check | First pass on photos | Vision check on shortlisted items | Quality matters only for the shortlist |
| Legal trap review | None | Opus 5.5 reads the full appraisal | Hard reasoning, few items per week |
| Resale price estimate | Draft from comparables you paste | Review of the top 3 deals | Final number decides real money |

**Numbers.**
- Deposit (rękojmia) for bailiff movables: "w wysokości jednej dziesiątej sumy oszacowania"; no deposit "jeżeli suma oszacowania jest niższa niż pięć tysięcy złotych" (art. 867¹ § 1 KPC, t.j. Dz.U. 2026, read 14 Oct 2026).
- Electronic auction: deposit must reach the bailiff's bank account "najpóźniej na 2 dni robocze przed rozpoczęciem przetargu", and the bidder must give PESEL, ID number and marital status (art. 879⁵ KPC).
- Real estate auctions need a deposit of one tenth of the appraisal (art. 962 § 1 KPC), far beyond a 2,000 USD budget.
- AMW sells surplus property and equipment by tender and through an online shop (amw.com.pl, read 14 Oct 2026; deposit rules are per notice).
- Typical resale margins: not found. Measure them in your first week from your own comparables.

**How to start.**
1. Read the bailiff portal rules and the AMW tender rules; note any clause on automated access.
2. Build a small reader for the newest notices in one category (for example cars or power tools) in your voivodeship.
3. Set a hard budget rule: only items with an appraisal under 5,000 PLN at first (no deposit, low loss).
4. Visit one viewing in person before bidding on anything.

**Rules, tax and risks.**
- Bidding is in your own name with PESEL (art. 879⁵ § 2 KPC); there is no anonymous or bot bidding.
- Buying to resell is business-like activity: in 2026 unregistered activity is allowed up to 10,813.50 PLN revenue per quarter, then you must register in CEIDG within 7 days (money.pl, 19 Aug 2026). Income goes on PIT-36 at the tax scale.
- Risks: items sold as-is, hidden defects, transport costs, slow resale, a debtor's challenge to the auction.

**Limitations.**
- Real estate is out of reach with this capital.
- You must collect items physically; travel time eats the 10 hours/week.
- Appraisals are often accurate, so the real gap is mostly at the second term (50%).
- No sourced data on median margins.

**First week test.** Let the agent read every new notice for 7 days in one category and region and produce a ranked list with estimated margin; check 10 of them by hand. Pass if ≥2 items show an estimated net margin ≥25% after fees and transport. **Kill criteria.** Stop if after 2 months and 3 purchases the net margin is below 10% or capital is stuck in unsold items.

**Sources:** [KPC consolidated text (ISAP)](https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19640430296/U/D19640296Lj.pdf) · [Bailiff auction portal](https://licytacje.komornik.pl/) · [Agencja Mienia Wojskowego](https://amw.com.pl/) · [money.pl: unregistered activity 2026](https://direct.money.pl/artykuly/porady/dzialalnosc-nierejestrowana-2026-limit-10-813,50-zl,-po-przekroczeniu-7-dni-na-ceidg)

---

## 7. Smart-contract audit contests and bug bounties

**Category:** contests · **Realistic income:** 0-500 USD/month (median case for a newcomer at 10 h/week: about 0-200) · **Capital needed:** 0 USD (plus API tokens; no funds at risk) · **Score: 52** (E6 A10 F10 L16 R10) · **Rules:** AI-assisted allowed, but AI/scanner reports without proven impact are banned (Immunefi); legal in Poland: yes, with KYC

> Reviewing Solidity code in time-boxed contests (Cantina, Sherlock, CodeHawks) and live bug bounties (Immunefi) with an agent that does the first pass and a human who proves impact; real prize pools and an agent multiplier on reading code, but a steep skill curve, duplicate-splitting and a shrinking contest market keep the median low.

**How the money flows.** A protocol funds a prize pool (contests) or a standing bounty table (Immunefi). In contests, valid High/Medium findings share the pool; the more people report the same bug, the smaller each share, which can drop "at times less than $1" for common low-severity bugs (Runtime Verification, Aug 2024). In bounties, the first valid report of a critical bug takes the full listed reward. Payouts are usually in stablecoins (USDC) after KYC; Immunefi says failing to provide KYC "may result in forfeiture of payment" (rules, read 14 Oct 2026). Timing: contests pay after judging and escalations, typically weeks after the end.

**The asymmetry.** Partial and narrowing. Agents are good at the tedious first pass (reading 5,000-20,000 lines, mapping invariants, listing suspicious paths), which is where manual beginners lose most time. But AI auditors are already a product: Zealynx's Krait claims 100% precision over 50 blind contests and the Pashov Auditor is a public baseline (Zealynx, 31 May 2026, vendor claim), while generic LLM scanners average about 8% precision, "5 real findings out of 60 reported" (same source). So the field has split: generic AI output is noise that platforms reject; a tuned agent plus a human who writes a working PoC is still ahead of the median manual entrant. Window: 6-18 months before tuned AI auditors flatten the duplicate pool (estimate).

**What the agent does.**
1. Watch: list upcoming contests and new bounty programs (Cantina, Sherlock, CodeHawks, Immunefi) daily; pull repos and scope at start.
2. Filter: pick contests by pool size per line of code and by your known protocol types (lending, AMM, vaults).
3. Work: agent maps contracts, external calls, access control and invariants; runs Slither/Foundry fuzzing; drafts hypotheses ranked by impact.
4. Verify: for each top hypothesis the agent writes a Foundry PoC test on a local fork; no PoC, no report.
5. **Human gate:** you read the code path yourself, confirm severity against the platform's judging rules, and submit only PoC-backed findings. Never test against mainnet or public testnets (Immunefi bans it permanently).

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Contest watch and code mapping | Yes, 24/7 | No | Long code, many files, cheap |
| Hypothesis generation | Bulk pass per file | Opus 5.5 on cross-contract logic | Hard bugs need deep reasoning |
| PoC writing and running | Draft tests | Opus 5.5 to fix failing PoCs | Correctness matters more than speed |
| Report and severity argument | Draft | Opus 5.5 final | Judges reward clear impact |

**Numbers.**
- Code4rena closed on 13 May 2026 after 512 audits, 26,898 reported vulnerabilities and 16,600+ registered researchers (shattered.io, 1 Oct 2026, third-party report). Fewer contest venues now.
- Cantina: $55.5M total payouts, 23,886 researchers, 51 live bounties and 1 live competition (a $50,000 USDC pool), 144 ended competitions (cantina.xyz, 14 Oct 2026, platform claim).
- Immunefi: $140.6M cumulative payouts, 92,000+ researchers, 650+ protocols (as of Jun 2026, via shattered.io, third-party report).
- Earnings spread: median participant under $50K/year, top-25 $200K-$500K, beginners $5K-$20K in 3-6 months of dedicated practice (Zealynx academy, third-party report; "dedicated" means far more than 10 h/week).
- Record single payout: one auditor took over $500,000 from the zkSync contest pool (Runtime Verification, Aug 2024).
- Typical contest size: about 5,342 lines of Solidity, 2-3 weeks (Runtime Verification, Aug 2024).

**How to start.**
1. Learn Foundry and the top 10 DeFi bug classes; replay 5 past contests with published findings and measure your agent's recall.
2. Open Cantina and Sherlock accounts; set up a wallet for USDC payouts; complete KYC when the first finding is valid.
3. Enter one small contest with a modest pool, where fewer top auditors compete.
4. Track per contest: hours, findings submitted, valid, duplicates, USD.

**Rules, tax and risks.**
- Immunefi bans "Submitting AI-generated/automated scanner bug reports that lack the required information regarding the vulnerability's impact" and "Automated testing of services that generates significant amounts of traffic"; "Testing on mainnet or public testnet is grounds for an immediate and permanent ban" (rules, read 14 Oct 2026).
- Sherlock's judging guidelines: no explicit AI clause found (read 14 Oct 2026); duplicates get the highest severity among them.
- Legal in Poland: reviewing published source code is not access to someone's system; keep to local forks. Payouts arrive as crypto, so the tax treatment (personal income at receipt vs PIT-38 at disposal) needs the rules chapter and possibly an advisor.
- Risks: weeks of work for zero valid findings; heavy duplicate dilution; KYC needed for payout; stablecoin off-ramp costs.

**Limitations.**
- Real skill barrier: Solidity and DeFi economics, not just coding.
- 10 h/week is thin for a 2-3 week contest of 5,000+ lines.
- AI auditor products already compete for the same easy bugs.
- Contest market shrank with Code4rena's closure.
- Crypto payouts add tax and off-ramp complexity.

**First week test.** Replay one past contest with public findings: run the pipeline for 7 days and compare. Pass if the agent plus you rediscover at least 2 of the published High/Medium findings with working PoCs. **Kill criteria.** Stop after 3 live contests with zero valid findings.

**Sources:** [Immunefi rules](https://immunefi.com/rules/) · [Cantina competitions](https://cantina.xyz/competitions) · [shattered.io platform comparison](https://shattered.io/fr/?p=1682) · [Zealynx: AI auditor benchmark](https://academy.zealynx.io/blog/ai-auditor-118-finding-benchmark) · [Zealynx: Code4rena vs self-directed training](https://academy.zealynx.io/blog/code4rena-vs-self-directed-security-training) · [Runtime Verification: limitations of audit competitions](https://runtimeverification.com/blog/on-the-limitations-of-audit-competitions) · [Sherlock judging guidelines](https://docs.sherlock.xyz/audits/judging/guidelines)

---

## 8. Prize contests with a creative task (Polish "konkursy", design contests)

**Category:** contests · **Realistic income:** 0-200 USD/month median, mostly in goods, very lumpy · **Capital needed:** 0 (more if you chase receipt-based contests) · **Score: 51** (E5 A13 F13 L11 R9) · **Rules:** check each regulamin: many demand an entry made "samodzielnie" and a transfer of copyright; AI-assisted drafting with human finishing is the defensible mode; legal in Poland: yes, with conditions (no purchase-to-enter if it is really a game of chance)

> An agent can read hundreds of contest rules a week and pre-draft entries, which few hobbyists do, but prizes are small, mostly in kind, and judged on originality, so it is a fun low-ceiling side line rather than a top earner.

**How the money flows.** A brand (or institution) runs a contest under a regulamin; a jury picks the best
"zadanie konkursowe" (a slogan, a short story, a photo, a video, an answer to a question). Prizes are usually goods
(appliances, tickets, vouchers), sometimes cash. The organizer withholds the 10% flat prize tax where due and often adds a
small cash top-up to cover it. Design marketplaces (99designs) pay the winning designer of a client-run contest.

**The asymmetry.** Most entrants find contests on aggregator sites and enter by hand; reading 4-8 pages of rules for each
contest is the boring part that filters people out. An agent can watch aggregators and brand pages, parse every
regulamin into a checklist (purchase required? receipt to keep? age/residency? deadline? AI or "samodzielnie" clause?
copyright transfer? jury vs random?) and draft 3 options for the ones that fit. Win rates are low because a jury picks one or
a few out of many; the agent increases the number of well-targeted entries, not the odds per entry. Adoption of such
pipelines by hobbyists: not measured (not found).

**What the agent does.**
1. Watch: crawl public listing pages (e.g. contest aggregators) and brand pages daily; store contest URL and regulamin PDF.
2. Filter: local model extracts a rules checklist; drop contests that need a purchase you would not make anyway, that are
   random draws (loteria, needs a permit and is a different game), or that ban AI or require a fully own work you cannot honestly provide.
3. Draft: paid model produces 3 short candidate entries per contest from your brief (your own story, photo idea, tone).
4. Verify: you rewrite the chosen entry in your own words, add your real experience or photo, and check it against the checklist.
5. Submit: **human gate**: you submit by hand, from your own single account, and keep receipts if required.
6. Track: log entries, results and prize value to compute value per hour.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Crawl and parse regulaminy | yes, all PDFs | no | bulk Polish legal text, 24/7 |
| Rules checklist extraction | yes | spot-check of edge cases | errors here make entries invalid |
| Entry ideas and drafts | first ideas | best 3 drafts | creativity and Polish style matter |
| Final entry | no | no | you finish it yourself (originality, copyright) |
| Results tracking | yes | no | simple bookkeeping |

**Numbers.**
- e-konkursy.info showed about 25-30 actively promoted contests on 14 Oct 2026; examples: washing machine for an answer to a question (no purchase, ends 31 Oct 2026), appliances for a product video (purchase required, ends 31 Dec 2026), socks for a comment (no purchase) (e-konkursy.info, 14 Oct 2026).
- Example B2B contest: Enigma's "Weź udział i wygraj konsultacje strategiczne!" (6-13 Mar 2026): prizes were consulting sessions, "nie podlegają wymianie na ekwiwalent pieniężny", entry "powinno być przygotowane samodzielnie", jury decision final (regulamin, Mar 2026).
- 99designs logo contests: Bronze 289 EUR with about 30 concepts, Silver 479 EUR about 60, Gold 859 EUR about 90 (99designs pricing, 14 Oct 2026), so a single design faces roughly 30-90 competing concepts per contest *(platform claim)*. 99designs terms (rev. 30 Jun 2025) put originality rules in a separate Originality Policy; an explicit AI clause was not found in the general terms.
- Realistic win rates per entry for Polish brand contests: not found from a public source.

**How to start.**
1. Build the regulamin parser first and run it on 50 current contests; check its checklist by hand on 10.
2. Pick contest types where your real life gives an edge (tech, DIY, travel, photos you actually take).
3. Enter 10 contests by hand-finished entries in week one; log time spent and outcome dates.
4. Only later consider design contests; they are crowded and need design skill beyond drafts.

**Rules, tax and risks.**
- Rules: many regulaminy require a work made "samodzielnie" and the transfer of author's economic rights; under Polish copyright law protection covers human creative work, so a raw model output is a weak fit for such a clause. Use the model for ideas and editing, keep the creative core your own; skip contests that ban AI.
- One person, one account, one entry unless the regulamin allows more; never multi-account.
- Polish law: a contest with a jury and a creative task is not a game of chance; random-draw "loterie promocyjne" are licensed games under the gambling act and a different category.
- Tax in one line: prizes from contests are taxed at a 10% flat rate withheld by the organizer, with an exemption for small sales-promotion prizes (art. 21 ust. 1 pkt 68 and art. 30 ust. 1 pkt 2 of the PIT act: exempt if the single prize "nie przekracza kwoty 2000 zł"; details in [03-RULES-TAX-RISKS.md](03-RULES-TAX-RISKS.md)).
- Risks: time sink, prizes you do not need (resale value is lower), purchase-required contests turn into spending.

**Limitations.**
- Ceiling is low and payouts are mostly goods, not cash.
- Jury contests reward originality; generic AI drafts lose.
- Many contests are social-media comment contests with tiny prizes.
- Receipt-based contests need purchases and kept receipts.
- Odds per entry stay low; results come weeks later, so feedback is slow.

**First week test.** Parse 50 regulaminy and submit 10 hand-finished entries; pass if the parser checklist is correct on at least 9 of 10 spot-checked rules and your time per entry is under 20 minutes. Judge wins after 6 weeks.

**Kill criteria.** Stop if after 8 weeks and 40 entries the prize value received is below 200 PLN.

**Sources:** [e-konkursy.info](https://www.e-konkursy.info/) · [Enigma contest regulamin (Mar 2026)](https://www.enigma.com.pl/wp-content/uploads/2026/03/regulamin-konkursu.pdf) · [99designs pricing](https://en.99designs.de/pricing) · [99designs terms of use](https://en.99designs.de/legal/terms-of-use) · [PIT act, ELI record (consolidated DU 2026 poz. 592)](https://api.sejm.gov.pl/eli/acts/DU/1991/350)

---

## 9. Bank promotion tracking (promocje bankowe)

**Category:** claims · **Realistic income:** 50-150 USD/month averaged over a year (about 2,500-6,000 PLN/year, median ~3,500 PLN) · **Capital needed:** 0 (you move your own salary and spending through the accounts) · **Score: 51** (E4 A6 F14 L17 R10) · **Rules:** automation in ToS: the agent only reads public terms, you act; legal in Poland: yes, one real identity, one account per bank as offered

> Polish banks pay real cash for opening and using accounts and cards; an agent that reads every term and tracks every deadline makes this low-effort and reliable, but the total is small and capped by "new customer" rules.

**How the money flows.** A bank pays a bonus (premia) for opening an account or card and meeting conditions: monthly inflows, a number of card payments, mobile app logins, sometimes a savings deposit. The bonus is paid to the account, usually in stages over a few months. You can only take each offer once per bank in its "new customer" window.

**The asymmetry.** Comparison sites already list the offers (kontomaniak.pl showed 11 promotions for private individuals in October 2026), so finding offers is not the edge. The edge is execution: reading 10-20 pages of terms per offer, logging the exact conditions, and never missing a monthly card-payment count or an inflow. People lose bonuses on small slips. An agent with a calendar and a checklist fixes that. Adoption of AI here: not measured (not found); the window is open as long as banks run acquisition campaigns.

**What the agent does.**
1. Watch: weekly, read the offer list on comparison sites and the banks' own promotion pages and terms PDFs.
2. Filter: drop offers where you are not a "new customer", business-only offers, and offers that need a credit product you do not want.
3. Work: turn each term sheet into a checklist with dates (inflow amount, card payments count, deadlines, exclusion clauses, account closing fees).
4. Verify: paid model re-reads the terms for traps (clawback if closed early, minimum keeping period, fees after the promo).
5. Act: human approval gate. You open the account yourself; the agent only reminds, tracks progress and checks the bonus arrived.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Read terms PDFs | Extract conditions and dates | None | Long documents, private context |
| Trap review | None | Opus 5.5 on each accepted offer | A missed clause costs the whole bonus |
| Monthly tracking | Compare your exported statements with the checklist | None | Bank statements stay on the rig |
| Reminders | Calendar entries and alerts | None | 24/7, trivial |

**Numbers.**
- Offers for private individuals on kontomaniak.pl (read 14 Oct 2026, *(third-party report)*): Erste Bank up to 1,050 PLN, BNP Paribas 1,100 PLN, mBank 1,010 PLN, Credit Agricole 1,000 PLN cashback, ING 800 PLN, BNP Paribas credit card 400 PLN, Pekao savings up to 2,700 PLN; several end in mid-October or November 2026.
- "New customer" means no account at the bank for a period of 6 to 36 months, depending on the bank (kontomaniak.pl, Oct 2026).
- Tax: prizes from "sprzedaż premiowa" are tax-free if the single value "nie przekracza kwoty 2000 zł" (art. 21 ust. 1 pkt 68 PIT act); above that a 10% flat tax applies ("w wysokości 10 % wygranej lub nagrody", art. 30 ust. 1 pkt 2). Kontomaniak says bonuses are paid "w pełnej wysokości netto" *(third-party report)*: check each term sheet for who pays the tax.
- Realistic yearly total: not measured by any source found; the estimate above assumes 3-5 offers per year at 700-1,100 PLN each.

**How to start.**
1. List the banks where you already have or recently had an account; they are out.
2. Let the agent build a table of open offers with "new customer" rules and deadlines.
3. Pick at most two offers at a time so the conditions fit your normal spending and salary flow.
4. Export statements monthly and let the local model check progress.

**Rules, tax and risks.**
- Use only your own identity and the number of accounts the offer allows; multi-accounting or fake referrals break terms and can be fraud.
- Exemption up to 2,000 PLN per prize under art. 21 ust. 1 pkt 68 PIT act; above it 10% flat tax (see Numbers). Referral rewards may be taxed differently; check each term sheet.
- Credit cards mean a credit check in BIK (bank practice, not re-verified this run); many new cards in a short time can lower your score before a mortgage.
- Risks: missed condition, bank refusing the bonus for "abuse" clauses, fees after the promo period.

**Limitations.**
- Hard cap: each bank once per 6-36 months.
- Totals are small next to a DevOps salary.
- Many cash flows to move each month; this is admin work.
- Comparison sites already do the finding.

**First week test.** Have the agent build the offer table and the checklist for one chosen offer, then compare it with your own reading of the terms. Pass if the agent's checklist catches every condition you find, and at least one you missed. **Kill criteria.** Stop if two bonuses in a row are lost or refused, or if open offers for you fall under 1,500 PLN a year.

**Sources:** [kontomaniak.pl: bank promotions](https://kontomaniak.pl/promocje-bankowe) · [PIT act consolidated text (ISAP)](https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19910800350/U/D19910350Lj.pdf)

---

## 10. Web and app bug bounty with AI-assisted recon

**Category:** bounties · **Realistic income:** 0-300 USD/month (median case: 0 in the first 2-3 months, then occasional low/medium payouts) · **Capital needed:** ~0-50 USD (API tokens, a VPS for out-of-band callbacks) · **Score: 48** (E6 A8 F12 L14 R8) · **Rules:** AI-assisted allowed, human validation required (HackerOne, Bugcrowd); legal in Poland: with conditions (only inside a program's published scope)

> Hunting for security bugs in programs on HackerOne, Bugcrowd, Intigriti or YesWeHack with agents doing the recon and triage; legal and permitted, but the AI edge is already shared by thousands of hunters and the "AI slop" backlash punishes exactly the volume play an agent invites, so it is a mid-table entry.

**How the money flows.** Companies run public or private programs on a platform and pay per valid, in-scope, non-duplicate finding, priced by severity in the program's table. The platform pays out (bank transfer, PayPal or similar, after tax/identity forms) once the program triages and rewards the report. Duplicates and out-of-scope reports pay nothing. Timing: from days to months, depending on triage. HackerOne paid $89.1M in bounties in July 2025-June 2026 (platform claim).

**The asymmetry.** It is weaker than it looks. AI-assisted hunting is mainstream: HackerOne's code of conduct "permits and encourages the responsible use of AI tools" for recon, discovery and proof-of-concept work (read 14 Oct 2026), so the tools are not an edge on their own. The remaining asymmetry is narrow: (1) agents reading large JS bundles, API specs and changelogs of newly added or newly widened scopes faster than humans; (2) AI-specific bug classes (prompt injection, system-prompt leakage, improper output handling) where valid reports grew 222% in two years (HackerOne 2026 report, platform claim). The window for "volume" closed in 2025-2026: curl ended its paid program on 31 Jan 2026 because confirmed-vulnerability rates fell from ~15% to under 5% under AI-generated reports, and HackerOne's Internet Bug Bounty paused new submissions on 27 Mar 2026 (third-party report).

**What the agent does.**
1. Watch: poll program pages and scope changes daily (new programs, new assets, raised bounty tables); store scope rules as structured data.
2. Filter: keep only assets that are explicitly in scope; drop anything listing "no automated scanning" for the asset type you would touch.
3. Work (passive first): read public JS, OpenAPI docs, release notes, and diff them between days; propose hypotheses (IDOR, auth bypass, LLM-feature prompt injection) with a test plan.
4. **Human gate:** you read the test plan and check it against the program's rules and rate limits before any request hits the target.
5. Verify: you reproduce manually; the agent drafts the report with exact steps, impact and a minimal PoC.
6. **Human gate:** you submit only reproduced, in-scope findings. One good report beats ten speculative ones.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Scope watch and diffing | Yes, 24/7 | No | Cheap, constant, private data |
| JS/API reading and hypothesis list | Yes, first pass | Opus 5.5 on the top 5 leads | Volume local, judgment paid |
| Test plan vs program rules | Draft | Opus 5.5 review | Legal risk needs the best reasoning |
| Report writing | Draft | Opus 5.5 final edit | Report quality decides triage |

**Numbers.**
- $89.1M bounty payouts on HackerOne, Jul 2025-Jun 2026; 92,194 valid reports analysed (HackerOne Security Research Report 2026, platform claim). Simple average about $970 per valid report; median per report not published (not found).
- Open valid reports up 131% from 2024 to 2026 and 30 hours to validate a critical finding (same report): triage is a bottleneck, so payout delays grow.
- curl: ~7 years, 87 confirmed vulnerabilities, over $100,000 paid; ended 31 Jan 2026 (BleepingComputer 22 Jan 2026; Pinggy blog, third-party report).
- Median hunter income: not found from a primary source. Most accounts on any platform never earn a bounty (widely reported, no current hard number found).
- Cost: local inference ~free; Opus review of 5 leads/week, a few USD/week (estimate).

**How to start.**
1. Create accounts on HackerOne and Intigriti (EU-based, euro payouts); complete tax/identity forms before the first payout.
2. Read the code of conduct of each platform; save the AI clauses.
3. Pick 2-3 programs with wide scope, an explicit safe-harbor statement and a published payout table; prefer programs with AI/LLM features in scope.
4. Build the scope-watcher and the passive JS/API reader first; no active testing tooling until a lead exists.
5. Do one manual end-to-end report on a low-severity finding to learn triage.

**Rules, tax and risks.**
- HackerOne prohibits "Generating large volumes of low-signal or non-actionable reports" and "Submitting unverified or fabricated vulnerability claims"; sanctions: final warning, 12-month ban, permanent ban (Code of Conduct, read 14 Oct 2026).
- Bugcrowd: "Manually review and validate any vulnerability report you've created with the help of GenAI tools before submitting it" (Code of Conduct, read 14 Oct 2026). Bugcrowd terms also require stopping automated tools at any sign of performance degradation.
- Polish law (consolidated Kodeks karny, ISAP text dated 28 Aug 2026): art. 267 (unauthorized access), 269a (disrupting systems) and 269b (tools/passwords for those crimes) apply. Art. 269c excuses only art. 267 § 2 and 269a when acting "wyłącznie w celu zabezpieczenia systemu" with immediate notification and no damage; art. 269b § 1a excuses tools made for protection. It does NOT cover 267 § 1 (breaking a safeguard) or acting outside the owner's consent. Practical rule: only test what a program authorizes in writing. No newer researcher-specific amendment found in that text.
- Tax: foreign platform payouts are personal income for a Polish tax resident (PIT-36, scale or via a sole proprietorship); details in the rules chapter.
- Risks: duplicates (most reports), N/A ratings hurting your signal score, bans for low-quality volume, legal exposure if the agent touches out-of-scope hosts.

**Limitations.**
- Everyone has the same AI tools; the asymmetry is speed on new scope, not capability.
- Triage backlogs mean money arrives weeks or months later.
- Real findings need manual reproduction, which eats most of the 10 h/week.
- Private invites (where competition is lower) require a track record you do not have yet.
- Many programs forbid automated scanning outright.

**First week test.** Watch 3 programs' scope for 7 days, generate leads locally, manually check the top 10; pass if at least 1 finding is reproduced and submitted with a PoC (acceptance not required in week 1). **Kill criteria.** Stop if after 8 weeks you have no accepted (triaged valid) report or any report closed as N/A for low quality twice.

**Sources:** [HackerOne Code of Conduct](https://www.hackerone.com/policies/code-of-conduct) · [HackerOne Security Research Report 2026](https://www.hackerone.com/report/hacker-powered-security) · [Bugcrowd Code of Conduct](https://www.bugcrowd.com/resources/essentials/code-of-conduct/) · [Bugcrowd Standard Disclosure Terms](https://www.bugcrowd.com/resources/standard-disclosure-terms/) · [BleepingComputer: curl ending bug bounty](https://www.bleepingcomputer.com/news/security/curl-ending-bug-bounty-program-after-flood-of-ai-slop-reports/) · [Pinggy: curl summer of bliss](https://pinggy.io/blog/curl_ai_slop_summer_of_bliss/) · [Kodeks karny, consolidated text (ISAP)](https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19970880553/U/D19970553Lj.pdf)

---

## 11. Expert AI-training work (Outlier, DataAnnotation, Alignerr, Mindrift)

**Category:** paid work · **Realistic income:** 300-900 USD/month for 10 h/week of your own time, median case, with empty weeks · **Capital needed:** 0 · **Score: 47** (E12 A2 F10 L15 R8) · **Rules:** human work only; agent allowed only around the work (finding projects, scheduling, your own learning), never to produce answers; legal in Poland: yes

> Well-paid human expert work (code review, Polish-language writing, RLHF rating) that AI labs buy precisely because it is human, so an agent cannot do the paid part and the asymmetry is near zero; listed for honesty, not as a top pick.

**How the money flows.** AI labs pay platforms for human judgments; platforms pay contributors per hour or per
task. Outlier pays weekly every Tuesday via PayPal, Airtm or ACH (Outlier FAQ, read 14 Oct 2026). DataAnnotation pays
via PayPal, delivered within a few days of a request (DataAnnotation FAQ, 2026). Most platforms require unpaid
qualification tests before any paid work.

**The asymmetry.** Inverted. The client's whole point is human data for training and evaluating models; using a model
to write your answers poisons that data. The only legitimate leverage is outside the task: an agent that monitors
which projects are open, tracks your effective hourly rate per project, and helps you study for qualification tests
in your strongest domain (DevOps/coding, Polish). That saves maybe 1-2 hours a week of hunting, not more.

**What the agent does.**
1. Watch: you paste or export the project list you already see into a local tracker (no automated access to the worker account).
2. Filter: local model ranks projects by stated rate, your skill match and your logged effective rate.
3. Prepare: paid model builds study notes and practice questions for the domain of a qualification test (not the test itself).
4. Work: **you** do every task by hand. No model touches task content.
5. Verify: tracker logs hours, task counts and payouts; flags projects whose effective rate falls below your floor.
6. Act: **human gate**: you decide which project to accept and when to quit one.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Project tracking and ranking | yes | no | private log of your own earnings |
| Effective rate analytics | yes | no | simple arithmetic and summaries |
| Study material for a domain | drafts | review for correctness | wrong study notes cost a failed test |
| Doing the tasks | never | never | the client pays for human judgment |

**Numbers.**
- Outlier: new workers 15-22 USD/h; floor 15-20, ceiling 35-50 USD/h (Breaking Even, Reddit-based analysis, data 29 May-17 Aug 2026) *(third-party report)*.
- Outlier by task type: general RLHF 18-28 USD/h, code review 28-45 USD/h, expert tier 35-60 USD/h (Breaking Even, May 2026, upd. Sep 2026) *(third-party report)*.
- Outlier, Polish writing experts: average about 15 USD/h for core project work (Outlier job listing seen in search results, Oct 2026; listing page now 404) *(platform claim)*.
- DataAnnotation: general 25-50+ USD/h, multilingual 20+ USD/h, coding 40-150+ USD/h (DataAnnotation FAQ, 2026) *(platform claim)*; country list not published.
- Alignerr: 25 USD/h floor, 80-125 USD/h ceiling, but many unpaid assessments (Breaking Even, Apr-Sep 2026) *(third-party report)*.
- "Empty queue" mentioned in 231 of 1,532 Reddit discussions; queue watching cuts effective pay 20-30% (Breaking Even, May 2026) *(third-party report)*.
- Effective rates run 20-40% below per-task math after task hunting (CareerSeeker, 7 Jul 2026) *(third-party report)*.

**How to start.**
1. Apply to Outlier (widest language/geo coverage, Polish projects exist) and Mindrift (reported as friendlier to non-US workers); try DataAnnotation, but expect a geo rejection.
2. Choose the coding or Polish-language track; take qualification tests yourself.
3. Set up a local spreadsheet or SQLite log of hours, tasks and pay per project.
4. Build the small local ranking agent over the project list you export by hand.

**Rules, tax and risks.**
- AI use: explicit public clauses not found in Outlier or DataAnnotation FAQs (checked 14 Oct 2026), but using LLMs to produce human-data answers defeats the contract's purpose and research platforms such as Prolific tell participants not to use LLMs unless permitted. Treat model-written answers as forbidden.
- Polish law: legal; you are an independent contractor of a foreign company.
- Tax in one line: income from a foreign platform is taxed under PIT on the annual return (scale 12%/32% or via a business); details in the rules chapter.
- Risks: removal from projects without explanation and unpaid invoices for 30+ days are reported (Breaking Even, Feb-Sep 2026) *(third-party report)*; Scale AI (Outlier's owner) faced wage-theft and misclassification suits in Dec 2024-Jan 2025 (Wikipedia).

**Limitations.**
- No agent leverage on the paid work: income is strictly hours × rate.
- It consumes your scarce 10 hours that could run agent-leveraged ideas.
- Queues are volatile; a project can vanish overnight.
- Geo lists exclude Poland on some platforms.
- Unpaid onboarding and assessments lower the real rate.

**First week test.** Pass at least one paid qualification and log 5 paid hours; pass if effective rate is at least 20 USD/h including hunting time.

**Kill criteria.** Stop if the effective rate stays under 15 USD/h for 3 weeks or you get no work for 2 weeks.

**Sources:** [Breaking Even: Outlier vs DataAnnotation vs Alignerr pay](https://breakingeven.online/blog/outlier-vs-dataannotation-vs-alignerr-pay-comparison) · [Breaking Even: Outlier pay per hour 2026](https://breakingeven.online/blog/outlier-ai-pay-per-hour-2026) · [Breaking Even: AI training jobs tier list 2026](https://breakingeven.online/blog/ai-training-jobs-2026-platform-tier-list) · [DataAnnotation FAQ](https://www.dataannotation.tech/faq) · [Outlier FAQ](https://outlier.ai/faq) · [AI Trainer: DataAnnotation vs Outlier](https://aitrainer.work/compare/dataannotation-vs-outlier) · [CareerSeeker: data annotation jobs 2026](https://careerseeker.ai/data-annotation-jobs/) · [Wikipedia: Scale AI](https://en.wikipedia.org/wiki/Scale_AI) · [WU Vienna: Detect and prevent AI in online surveys](https://www.wu.ac.at/fileadmin/wu/d/cc/exp/PDFs/Detect_and_Prevent_AI_in_Online_Surveys_Guide.pdf)

---

## 12. Marketplace arbitrage (OLX, Allegro, Vinted)

**Category:** arbitrage · **Realistic income:** 50-400 USD/month (median ~150 USD) · **Capital needed:** 500-1,500 USD stock · **Score: 45** (E7 A9 F11 L10 R8) · **Rules:** automation in ToS: scraping not allowed on Allegro, official API only for your own offers; legal in Poland: with conditions (trade limits, DAC7)

> Buying underpriced second-hand items and reselling them works, but the legal version cannot scan marketplaces with bots, so the agent helps you judge and list, not hunt at scale.

**How the money flows.** You buy an item that is listed too cheap (bad photos, wrong category, seller in a hurry) and resell it with a better listing, on the same or another marketplace. Buyers pay through the platform; Allegro and Vinted pay out to your bank account after delivery. Profit equals resale price minus purchase price, platform fees and shipping.

**The asymmetry.** Most private resellers still judge items by eye and write listings by hand. A vision model can read blurred photos, spot model numbers, and write a full listing in seconds. But the hunting side is already protected: Allegro uses DataDome, "one of the most common commercial anti-bot systems", which checks "your TLS signature, HTTP headers, and behavior patterns" (Scrapfly, 6 Oct 2026, *(third-party report)*). So the edge is only on judging and listing, not on finding.

**What the agent does.**
1. Watch: only through allowed channels: saved-search alerts you set up in each app, and the listings you open yourself.
2. Filter: you paste or forward a listing; the local model reads photos and text, identifies the exact model and condition.
3. Work: estimate resale price from sold or comparable listings you look up; compute net margin after fees and shipping.
4. Verify: human approval gate before every purchase.
5. Act: after purchase, the agent drafts the new listing (title, description, photo order); on Allegro you can publish your own offers through the REST API.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Read a listing | Text extraction and first price guess | None | Private, cheap, many per day |
| Photo analysis | None (rig model is text) | Cheap vision model | Needs vision |
| Margin decision | Draft calculation | Opus 5.5 check for items above 300 PLN | Real money |
| Listing text | Draft in Polish and English | None | Bulk text |

**Numbers.**
- eBay Buy APIs (Browse API) are "Limited Release" and "intended for eBay partners only"; production needs eBay Partner Network approval, "There is no guarantee that your application for production use of the APIs will be approved" (eBay developer docs, read 14 Oct 2026).
- Allegro REST API documentation lists seller endpoints such as `GET /sale/offers` for your own offers; no public search of other sellers' offers was found in the docs (read 14 Oct 2026).
- DAC7: a platform reports a seller to the tax office unless the seller has fewer than 30 sales and under 2,000 EUR in a year; two Polish articles describe the trigger differently (antyweb.pl says both conditions, fashionbiznes.pl says either), so plan for "either". In April 2025 the Polish tax office had DAC7 data on 487,000+ individuals from foreign-registered platforms such as Vinted (fashionbiznes.pl, 23 Apr 2025).
- Median margin per flip: not found. Measure it yourself.

**How to start.**
1. Pick one narrow niche you know (for example used GPUs or camera lenses).
2. Set saved-search alerts in OLX, Allegro and Vinted for that niche.
3. Build the agent as a "second opinion" tool: you paste a link or screenshot, it returns model, condition risks, price range and net margin.
4. Apply for Allegro REST API access to list your own items.

**Rules, tax and risks.**
- Allegro forbids scraping and extraction of its content without consent; automated access is only via its REST API (summary of Allegro rules, third-party; full terms returned HTTP 403 to our fetch, read them yourself).
- Selling your own personal items more than six months after the end of the month you bought them is not taxable income (art. 10 ust. 1 pkt 8 PIT act); buying to resell is trade.
- Trade without a company is allowed in 2026 up to 10,813.50 PLN revenue per quarter; above that you register in CEIDG within 7 days (money.pl, 19 Aug 2026). Tax on PIT-36.
- Risks: fakes, items damaged in shipping, returns, slow sales, account limits for "pro" behaviour on consumer platforms.

**Limitations.**
- No legal bot hunting on Allegro; the agent cannot beat human snipers to fresh listings.
- Quarterly revenue limit is small: about 3,600 PLN per month of sales before you must register a business.
- Your time goes into meetings, packing and shipping, not into AI work.
- Many experienced flippers already know prices in their niche by heart.

**First week test.** Run the agent on every listing your saved searches send you for 7 days. Pass if it finds ≥3 items with an estimated net margin ≥20% that you agree with after a manual check. Buy at most one. **Kill criteria.** Stop if after one month net profit per hour of your time is below the Polish minimum hourly wage.

**Sources:** [eBay Buy API requirements](https://developer.ebay.com/api-docs/buy/static/buy-requirements.html) · [Allegro REST API docs](https://developer.allegro.pl/documentation) · [Scrapfly: scraping Allegro](https://scrapfly.io/blog/posts/how-to-scrape-allegro) · [antyweb: DAC7 Allegro OLX Vinted](https://antyweb.pl/allegro-olx-vinted-dac7) · [fashionbiznes: DAC7 data](https://fashionbiznes.pl/urzad-skarbowy-ma-juz-dane-z-vinted-i-innych-platform-liczby-robia-wrazenie/) · [money.pl: unregistered activity 2026](https://direct.money.pl/artykuly/porady/dzialalnosc-nierejestrowana-2026-limit-10-813,50-zl,-po-przekroczeniu-7-dni-na-ceidg) · [PIT act consolidated (ISAP)](https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19910800350/U/D19910350Lj.pdf)

---

## 13. Open-source issue bounties

**Category:** bounties · **Realistic income:** 0-150 USD/month (median case: close to 0) · **Capital needed:** 0 USD (plus a few USD of API tokens) · **Score: 44** (E3 A5 F13 L14 R9) · **Rules:** AI-assisted allowed in most repos, disclosure often required, some projects ban AI PRs; legal in Poland: yes

> Fixing GitHub issues that carry a cash bounty (Algora, Opire, IssueHunt, Gitcoin, Polar-funded issues) with a coding agent; legal and simple, but by October 2026 every visible bounty is swarmed by other people's agents, so the asymmetry is mostly gone and it ranks low.

**How the money flows.** A maintainer or sponsor attaches money to a GitHub issue (Algora's label is "💎 Bounty"; Opire bounties start at $20). Many developers "attempt" it; the maintainer merges one PR and the bounty goes to that author through the platform (Algora marks it "💰 Rewarded"). Opire states payment is not automatic: "the creator arranges payment only if the pull request meets the issue requirements" (read 14 Oct 2026). Winner takes all; second-best PRs earn nothing. Payout rails and fees were not re-verified in this research (check each platform's docs before the first claim).

**The asymmetry.** Inverted. In 2024 a coding agent was an edge; in 2026 it is the default entrant. GitHub search on 14 Oct 2026: open tscircuit bounties had 40, 40 and 73 comments each, and one open bounty issue in another repo had 1,447 comments, most of them automated claims. A June 2026 write-up describes a fake "bounty" repo built as a trap that AI agents walked into, leaking their prompts (s-anand.net, third-party report). Maintainers are pushing back: GitHub shipped options on 27 Aug 2026 to disable PRs, restrict them to collaborators or cap concurrent external PRs; Ghostty went to a zero-tolerance policy with permanent bans in Jan 2026; Gentoo bans machine-generated contributions; NetBSD treats AI code as "tainted" (third-party reports). The only remaining edge is niche, hard bounties (Scala/ZIO, Rust, embedded) where a cheap agent fails and an expert plus agent succeeds.

**What the agent does.**
1. Watch: GitHub search for bounty labels every hour; record amount, repo, age, comment count, open PRs.
2. Filter: drop issues with more than 5 attempt comments or any open PR; drop repos whose CONTRIBUTING.md bans AI PRs or "/attempt" claims; keep repos you can build and test locally.
3. Work: agent reproduces the bug, writes a failing test, then the fix, in a sandbox.
4. Verify: full test suite plus Opus 5.5 review of the diff against the maintainer's style and the issue's acceptance criteria.
5. **Human gate:** you read the diff, disclose AI assistance where the repo asks, and open one PR per bounty. Never mass-claim.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Bounty watch and filtering | Yes, 24/7 | No | Pure volume, no reasoning needed |
| Repo reading and repro | Yes | No | Long context, private sandbox |
| Fix on hard issues | First attempt | Opus 5.5 or a cheap coding API | Hard issues are the only winnable ones |
| Diff review before PR | No | Opus 5.5 | Maintainer trust decides the payout |

**Numbers.**
- GitHub issues with Algora's "💎 Bounty" label, open: 549; issues labelled "💰 Rewarded" and closed in the last 12 months: 249 (GitHub search API, 14 Oct 2026). The 249 rewarded issues are the whole worldwide pie for a year on that label.
- Of the first 100 rewarded issues, most came from a few orgs: archestra-ai 36, zio 22, projectdiscovery 18, Cap-go 9 (same query, 14 Oct 2026).
- New "💎 Bounty" issues: 1,446 created in 2025, 496 so far in 2026, but only 1 created and 3 rewarded in the 3 months to 14 Oct 2026 (same query). Either sponsors left public label bounties mid-2026 or the platform changed how it labels issues; cause not found, so verify on the platform itself before investing time.
- Opire minimum bounty $20 (opire.dev, 14 Oct 2026).
- Of the top 1,000 GitHub repos, 118 have written AI policies and 51% of those require disclosure (third-party report, Jul 2026).
- Median earnings per participant: not found.

**How to start.**
1. Use your existing GitHub account; link it to Algora and Opire; complete payout onboarding and tax details.
2. Build the watcher with the filters above; log every bounty seen, its comment count and who won.
3. Pick a stack you know (Python, Go, Terraform/DevOps tooling) and only those repos.
4. Do one bounty fully by hand with agent help to learn the maintainer's review loop.

**Rules, tax and risks.**
- Repo rules decide: some ban AI PRs outright (Gentoo) or ban undisclosed AI use (Ghostty, Jan 2026, third-party report). Read CONTRIBUTING.md first.
- GitHub has suspended accounts for mass PR submissions (one engineer opened 130+ PRs in 72 hours; third-party report, Sep 2026). Mass-claiming risks your main GitHub identity, which is also your CV.
- Legal in Poland: plain paid programming work. Tax: personal income declared on PIT-36 (or via a sole proprietorship); details in the rules chapter.
- Risks: unpaid work when another PR is merged first; a maintainer may close the bounty without paying.

**Limitations.**
- Pool is small: about 249 rewarded label bounties a year worldwide.
- Winner-take-all against many agents.
- Easy issues are taken within hours; hard ones need real domain skill.
- Reputation damage from a rejected AI PR lasts longer than the bounty.

**First week test.** Run the watcher for 7 days and submit PRs to 3 bounties that pass the filters; pass if 1 is merged or the maintainer says it is the leading candidate. **Kill criteria.** Stop if 8 weeks bring under $100 total or any maintainer flags your PR as AI spam.

**Sources:** [GitHub search: open Algora bounties](https://github.com/search?q=label%3A%22%F0%9F%92%8E+Bounty%22+state%3Aopen&type=issues) · [Opire](https://opire.dev/) · [Crypto Briefing: GitHub PR controls](https://cryptobriefing.com/github-restricts-pull-requests-ai-slop/) · [Tianpan: agents are cheap, maintainer attention is not](https://tianpan.co/blog/2026/07/02/your-agents-are-cheap-maintainer-attention-isnt) · [s-anand: bounty hunting agent ecosystem](https://www.s-anand.net/blog/bounty-hunting-agent-ecosystem-2/)

---

## 14. Expired domain flipping

**Category:** arbitrage · **Realistic income:** 0-100 USD/month (median close to 0 in year one, often negative after renewals) · **Capital needed:** 300-1,500 USD per year for registrations and renewals · **Score: 37** (E3 A5 F12 L12 R5) · **Rules:** automation in ToS: registry and registrar APIs allowed within their terms; legal in Poland: yes, but trademark-based names can be lost in a dispute

> An agent can screen thousands of dropping names a day for meaning and brandability, but sales are rare, the market is old and already full of tools, so this belongs at the bottom of the list.

**How the money flows.** You register (or backorder) a name when it expires, list it for sale on marketplaces such as Sedo, Afternic or Dan, and wait for an end user to buy it. The marketplace takes a commission (current rates: not verified this run, the Afternic help page returned HTTP 403). You pay renewal every year until it sells.

**The asymmetry.** Valuing names is mostly judgement: is it a real word, a brand, a business type, a city plus service? A language model can do that judgement at scale, in Polish and other languages, where English-only investors are weak. But drop-catching and appraisal tools have existed for years, and big investors already run large automated portfolios. Adoption of AI by the competition: not measured (not found); assume high in .com, lower in .pl.

**What the agent does.**
1. Watch: daily lists of expiring and released names (registrar backorder lists; for .pl the registry publishes stats on names released for lack of renewal).
2. Filter: drop trademarks, personal names and typos of brands; keep generic Polish words, local services, short names.
3. Work: score each name (meaning, length, search interest, comparable sales you look up).
4. Verify: paid model reviews the top 20 for trademark and quality.
5. Act: human approval gate. You register a small number and set prices; never register a name that matches someone's trademark.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Screen daily drop lists | Score thousands of names | None | Bulk, 24/7, near zero cost |
| Trademark check | Flag obvious brand matches | Opus 5.5 review of the shortlist | Legal risk |
| Pricing | Draft price from comparables | None | Low stakes per name |
| Outreach | None | None | Cold outreach to buyers is spam-prone; avoid |

**Numbers.**
- The .pl registry held 2,736,154 domains with about 1,514 new ones a day (dns.pl, read 14 Oct 2026).
- DNJournal's 2026 year-to-date top 100 sales chart (through 4 Oct 2026) needs at least 95,000 USD to enter; top sale AI.com at 70,000,000 USD. These are outliers and say nothing about a typical name.
- Annual sell-through of an investor portfolio: no dated source found this run. The often-quoted figure of about 1% per year is folklore until you find a source; with that rate a 100-name portfolio sells about one name a year.
- Renewal cost per name per year: depends on registrar, not verified this run.

**How to start.**
1. Pick one niche you understand (Polish local services or tech words).
2. Run the agent on the daily drop list for a month without buying anything; record which names others catch.
3. Register at most 10 names and list them on one marketplace.
4. Track cost per name per year against sales.

**Rules, tax and risks.**
- Registering names that copy a trademark can be lost in a dispute (UDRP, or the Polish arbitration court for .pl) and may infringe trademark law; filter them out.
- A sale is income; repeated trading is business activity, taxed on PIT-36 (unregistered activity limit 10,813.50 PLN per quarter in 2026, money.pl 19 Aug 2026).
- Risks: renewals eat capital, most names never sell, long wait.

**Limitations.**
- Sales are rare and random; one year may bring zero.
- Good names are caught by professional drop-catchers before you see them.
- Capital is locked in renewals every year.
- The AI judgement edge is small because valuation tools already exist.

**First week test.** Let the agent score 7 days of drop lists and pick its top 20 names without buying; check which ones were caught by others. Pass if ≥5 of the 20 were caught by someone else (the agent sees value the market sees). **Kill criteria.** Stop if after 12 months renewals exceed sales.

**Sources:** [dns.pl registry](https://www.dns.pl/) · [DNJournal YTD sales chart](https://www.dnjournal.com/ytd-sales-charts.htm) · [money.pl: unregistered activity 2026](https://direct.money.pl/artykuly/porady/dzialalnosc-nierejestrowana-2026-limit-10-813,50-zl,-po-przekroczeniu-7-dni-na-ceidg)

---

## 15. Renting out the idle GPU rig

**Category:** compute · **Realistic income:** 0-50 USD/month net median (AMD cards find almost no renters) · **Capital needed:** 0 USD (rig already owned) · **Score: 36** (E3 A3 F6 L18 R6) · **Rules:** automation allowed (marketplaces expose host APIs/CLIs); legal in Poland: yes (income must be declared)

> Listing the 4x R9700 rig on GPU marketplaces is legal and easy to automate, but almost every marketplace is NVIDIA-only or has no AMD demand, and Polish electricity eats most of a consumer-GPU rental rate, so it does not make the top 10.

**How the money flows.** Renters pay the marketplace per GPU-hour; the marketplace keeps a fee and pays the host (Vast.ai in USD; Clore.ai and Nosana in their own tokens). Payout minimums and schedules differ per platform. Income only exists while a renter holds the machine, and while rented the rig cannot run my own agents.

**The asymmetry.** There is none worth having. GPU rental is a mature, price-competitive market where hosts already run automated repricing. The only edge an agent adds is switching the rig between own use and rental, which does not create demand for AMD cards.

**What the agent does.**
1. Watch: query marketplace offer APIs every hour for comparable-GPU prices and for any AMD listings.
2. Filter: compute break-even price = electricity cost + platform fee + wear; list only when the market price is above it.
3. Act: HUMAN GATE for first listing and price floor; afterwards the agent lists/unlists within the approved band.
4. Switch: unlist and resume own model serving when local agents have queued work.
5. Report: weekly earnings vs kWh used.

**Hybrid split.**

| Step | Local (DeepSeek-V4-Flash on the rig) | Paid API | Why |
|---|---|---|---|
| Price polling and break-even math | all, plain Python | none | deterministic, no model needed |
| Listing decisions | rule-based | Opus 5.5 weekly review | cheap; review only the policy |
| Own-use vs rent switch | scheduler | none | must react in minutes |

**Numbers.**
- AMD support: Vast.ai announced AMD Radeon/Instinct support but in beta, with ROCm templates *(Vast.ai, 2 Apr 2024)*. A live query of Vast's public offer API on 14 Oct 2026 returned no rentable offers under the names MI100, MI210, MI300X, Radeon Pro W7900, RX 7900 XTX or Radeon AI PRO R9700 *(own query, 14 Oct 2026)*.
- Clore.ai: "Any farm/server with an NVIDIA GPU" *(platform FAQ, Oct 2026)*; marketplace fee 1.8-2.5% spot, 5-10% on-demand.
- Nosana: NVIDIA only (RTX 30/40/50, A100, H100), Linux only, paid in NOS token *(docs, Oct 2026)*.
- Salad, io.net, Akash, Runpod community, TensorDock: AMD consumer-card hosting not confirmed in their docs at writing time (not found).
- Comparable NVIDIA rates on Vast (per GPU-hour, median of on-demand offers): RTX 3090 0.175 USD, RTX 4090 0.535 USD, RTX 5090 0.635 USD *(own API query, 64 offers each, 14 Oct 2026)*.
- Electricity: 2026 G11 household price about 0.95 PLN/kWh gross *(third-party report, voltflow.net, Apr 2026)*; supply part 495.16 PLN/MWh net *(URE, 10 Feb 2026)*. USD/PLN 3.9177 *(NBP, 13 Oct 2026)*.
- Break-even sketch: R9700 board power about 300 W *(vendor spec, not re-fetched)*; 4 cards plus host at about 1.4 kW cost about 1.33 PLN/h = 0.34 USD/h. Even if the cards rented at the RTX 3090 rate (0.70 USD/h for 4), 50% utilisation gives about 250 USD/month gross minus about 120 USD power minus platform fee: under 100 USD/month, and that assumes AMD demand that the market does not show.

**How to start.**
1. Do not buy anything. Check each marketplace's current host docs for AMD/ROCm support.
2. If one supports it: dual-boot or partition an Ubuntu host image as required; never expose the main workstation's data.
3. List one GPU at break-even plus 20% for 2 weeks to measure real demand.

**Rules, tax and risks.**
- Host agreements require a dedicated, clean environment; renters run arbitrary containers on your hardware, so isolate the network.
- Polish law: rental income from a private person is taxed as private-rental or other income; token payouts are crypto (details in the rules chapter).
- Risks: card wear, renter abuse traffic on a home IP, token price swings on token-paid networks.

**Limitations.**
- AMD consumer/workstation cards are effectively unrentable on the major marketplaces in 2026.
- Renting kills the main asset of this course: the free 24/7 local model.
- Home upload bandwidth and a residential IP lower the machine's reliability score.
- Polish household power prices are high by EU standards.

**First week test.** Query every listed marketplace's offer API for AMD cards. Pass if at least one marketplace shows 10+ rented AMD GPUs with 24+ GB VRAM at a rate above 0.35 USD/h.

**Kill criteria.** Fails the test, or under 30% utilisation after a 2-week listing.

**Sources:** [Vast.ai AMD announcement](https://vast.ai/article/announcing-amd-support) · [Vast.ai April 2024 update](https://vast.ai/article/vast-april-product-update) · [Vast.ai hosting docs](https://docs.vast.ai/documentation/host/hosting-overview) · [Clore.ai](https://clore.ai/) · [Nosana host docs](https://learn.nosana.com/hosts/grid.html) · [URE 2026 tariffs](https://www.ure.gov.pl/en/communication/news/501,The-President-of-the-Energy-Regulatory-Office-URE-has-approved-the-tariffs-for-t.html) · [Voltflow 2026 G11 price](https://www.voltflow.net/blog/obliczanie-zuzycia-energii-elektrycznej-dom-2026) · [NBP USD rate](https://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json)

---

## Rejected candidates

These came up in the research. The automated version either breaks the platform's terms or the law, or the money is
too small to justify an agent. Where a legitimate, smaller variant exists, it is named.

### Airdrop and points farming

What it is: using crypto protocols early so their later token airdrop rewards you. The AI-scaled version is multi-wallet ("sybil") farming: an agent running many wallets to look like many users.
Why rejected: the scaled version is exactly what projects filter out and forbid. Linea, with Nansen, flagged 516,960 of 1,297,203 eligible addresses as Sybils for "automated and coordinated activities across related wallets" (The Block, 21 Jan 2025). LayerZero said about 1 million of its 6 million wallets were sybil farmers and excluded them, offering self-reporters only 15% of their allocation (The Defiant, 2024). Galxe's terms let it "limit the number of User Accounts or Digital Wallets" and suspend accounts, with rewards forfeited (Galxe Terms, updated 10 Sept 2025). Multi-wallet farming = ToS violation = L0.
Legitimate small variant: one real identity, one or two wallets, genuine use of protocols you would use anyway. An agent only tracks campaigns, eligibility criteria, deadlines, gas costs and claim windows and checks claim URLs against official sources (never auto-signing). Value per real user is a lottery: often 0, sometimes a few hundred USD; median per-user amounts for 2025-2026 drops: not found. Gas and bridging fees eat small allocations.
Main extra risk: fake-airdrop phishing. Wallet drainers took 494M USD in 2024 and phishing losses were 84M USD in 2025 (Scam Sniffer annual reports). Never let an agent hold signing keys.
Tax: crypto disposals are taxed in Poland (see 03-RULES-TAX-RISKS.md).

**Sources:** [Linea sybil filter (The Block)](https://www.theblock.co/post/335979/linea-filters-over-half-a-million-sybil-addresses-from-upcoming-token-airdrop) · [LayerZero sybil self-report (The Defiant)](https://thedefiant.io/news/defi/layerzero-tells-sybil-farmers-to-out-themselves-or-face-airdrop-exclusion) · [Galxe Terms of Use](https://docs.galxe.com/about/legal) · [Scam Sniffer 2025 report](https://drops.scamsniffer.io/scam-sniffer-2025-crypto-phishing-losses-fall-83-to-84-million/) · [Scam Sniffer 2024 report](https://drops.scamsniffer.io/scam-sniffer-2024-web3-phishing-attacks-wallet-drainers-drain-494-million/)

### Paid surveys and microtasks (Prolific, MTurk, Swagbucks, Polish panels)

**What it is.** Getting paid a few dollars per survey or microtask on Prolific, Swagbucks, YouGov, Clickworker, Toloka or Polish panels (Ankieter.pl, Opinie.pl, Panel Ariadna). The "agentic" version would let an agent answer for you.

**Why rejected.** The paid product is a real human's answer, so agent-filled responses are fraud against the researcher and a ToS breach. MTurk's participation agreement: "you will not use robots, scripts, or other automated methods as a substitute for your human intelligence or independent judgment to perform Tasks" (last updated 25 Mar 2020). Prolific "reminds participants not to use LLMs unless explicitly permitted" (WU Vienna lab guide). Detection is strong: Prolific's bot authenticity check separated 125 humans from 5 AI agents with 100% accuracy (Prolific, 4 Feb 2026); a 2026 study found under 1% chatbot responses across 12 suppliers but 16% at a 13th (reported 30 Apr 2026). MTurk itself closed on 30 Sep 2026 (Wikipedia). Score 0.

**Legitimate small variant.** You answer surveys yourself; an agent may only read study listings you can already see and rank them by pay per minute and your eligibility (no answering, no auto-accepting). Earnings stay at survey rates (researchers are advised to pay at least about 12 USD/hour equivalent; WU guide), so it is not worth a course slot.

**Sources:** [Prolific: authenticity checks test (Feb 2026)](https://www.prolific.com/resources/authenticity-checks-how-we-tested-the-most-accurate-method-for-identifying-agentic-ai) · [MTurk participation agreement](https://www.mturk.com/participation-agreement) · [WU Vienna: Detect and prevent AI in online surveys](https://www.wu.ac.at/fileadmin/wu/d/cc/exp/PDFs/Detect_and_Prevent_AI_in_Online_Surveys_Guide.pdf) · [Let's Data Science: limited AI chatbot presence in surveys (Apr 2026)](https://letsdatascience.com/news/study-finds-limited-ai-chatbot-presence-in-online-surveys-c14178ff) · [Research Live: safeguards against AI in polls (Apr 2026)](https://www.research-live.com/article/opinion/the-right-safeguards-can-protect-public-opinion-polls-from-ai-pollution/id/5148723) · [Wikipedia: Amazon Mechanical Turk](https://en.wikipedia.org/wiki/Amazon_Mechanical_Turk)

### Crypto quest platforms (Galxe, Layer3, Zealy, Intract)

What it is: completing on-chain and social tasks ("quests") for points, NFTs or token rewards.
Why rejected: the only way an agent scales this is many accounts or scripted fake engagement, which the platforms forbid. Galxe's terms reserve the right to "limit the number of User Accounts or Digital Wallets", ban "Activity which operates to defraud Galxe, any Galxe user(s) or any other person", and allow it to "suspend or restrict your User Account" with rewards lost (Galxe Terms of Use, updated 10 Sept 2025). Quests are also the main lure for fake-airdrop phishing (drainers took 494M USD in 2024, Scam Sniffer). Layer3, Zealy and Intract clauses: not verified in this pass.
Legitimate small variant: do quests by hand on one account for protocols you actually use; an agent may only list campaigns and deadlines. Typical real payout per quest: not found; usually points with uncertain value.

**Sources:** [Galxe Terms of Use](https://docs.galxe.com/about/legal) · [Scam Sniffer 2024 report](https://drops.scamsniffer.io/scam-sniffer-2024-web3-phishing-attacks-wallet-drainers-drain-494-million/)

### DeFi bots (liquidations, arbitrage, MEV)

What it is: bots that liquidate undercollateralised loans, arbitrage prices between DEXes or between a CEX and a DEX, or capture other MEV.
Why rejected (feasibility and risk, not law): this is the opposite of an asymmetry. It is fully automated already and won by professional searchers with private orderflow, colocated infrastructure and large inventories; an LLM agent adds nothing to a latency race. With 2,000 USD the reader cannot hold inventory on both sides of a CEX-DEX trade, and failed or out-bid transactions still cost gas. Specific 2025-2026 figures on solo searcher profitability: not found in this research pass (no search budget left to verify), so no numbers are claimed here.
Legitimate small variant: none recommended. Building a liquidation bot on a testnet is a fine learning project, not income.
Tax: crypto gains are taxed in Poland (see 03-RULES-TAX-RISKS.md).

**Sources:** not found (no dated source verified in this pass; the verdict rests on the capital and latency constraints above)

### Bittensor subnet mining

What it is: running AI work (inference, models, data) for a Bittensor subnet and being paid in that subnet's alpha token, swappable to TAO.
Why rejected (feasibility and risk, not law): the best-known compute subnet, Chutes (SN64), needs NVIDIA-class GPUs (README examples A10, A6000, L40S, H100) on Intel TDX confidential-VM hardware with system RAM at least equal to total VRAM; AMD Radeon/ROCm is not listed (chutes-miner README, read 14 Oct 2026). Network pay is mostly inflation, not customers: 3,600 TAO/day after the Dec 2025 halving, 41% to miners, against an estimated 3-15M USD/year of external revenue across 128 subnets; Chutes alone pays about 52M USD/year of emissions against 1.3-2.4M USD of external revenue (Pine Analytics, 23 Mar 2026). Earnings therefore track the TAO price, and a new miner pays a registration fee in TAO on top of hardware: one operator described "roughly seven hours a day during the first months while paying both GPU and registration costs" (edgeX, 24 Aug 2026; *(third-party report)*). Exact current registration cost: not found. With 2,000 USD capital and AMD cards this is a speculative token bet, not income.
Legitimate small variant: none worth a profile; a reader curious about it can stake small amounts rather than mine, accepting price risk.
Tax: tokens received and later sold are taxed as crypto in Poland (see 03-RULES-TAX-RISKS.md).

**Sources:** [Bear case for Bittensor (Pine Analytics)](https://pineanalytics.substack.com/p/the-bear-case-for-bittensor-tao) · [chutes-miner README](https://github.com/chutesai/chutes-miner) · [Bittensor subnets and dTAO (edgeX)](https://pro.edgex.exchange/en-US/news/article/bittensor-subnets-miners-validators-dtao)

### Decentralized AI networks (Gensyn, Psyche, Prime Intellect, Nosana and others)

**What it is.** Networks that promise to pay people for contributing GPU time to distributed training or inference: Gensyn RL Swarm, Nous Psyche, Prime Intellect, Nosana, Hyperbolic, Ritual, Akash.

**Why rejected (not viable for this reader, not a ToS issue).** (1) Most pay points, not money: Gensyn RL Swarm runs on the "Gensyn Testnet" and participants earn leaderboard activity points, not tokens *(GitHub README, Oct 2026)*; Gensyn's Delphi testnet uses "valueless tokens" *(docs, Oct 2026)*. (2) Hardware: RL Swarm officially supports only NVIDIA RTX 3090/4090/5090, A100 and H100 *(README, Oct 2026)*; Nosana is NVIDIA-only *(docs, Oct 2026)*. No network checked documents AMD Radeon/ROCm hosting. (3) Prime Intellect is now a venture-funded company (130 M USD Series A, July 2026, third-party report) selling cloud compute; its docs show no paid public contributor programme (not found). (4) Running many nodes to farm future airdrop points is sybil farming and is out of scope for this course.

**Legitimate small variant.** Run one honest testnet node on CPU (RL Swarm allows a 32 GB RAM CPU node) only to learn the stack; count any future token as a windfall, not income.

**Sources:** [Gensyn RL Swarm](https://github.com/gensyn-ai/rl-swarm) · [Gensyn docs](https://docs.gensyn.ai/testnet) · [Nosana host docs](https://learn.nosana.com/hosts/grid.html) · [Prime Intellect Series A, KuCoin News](https://www.kucoin.com/news/flash/prime-intellect-completes-130m-a-round-at-1b-valuation-backed-by-nvidia-intel-and-dell) · [Prime Intellect docs](https://docs.primeintellect.ai/)

### Ticket resale and price-error hunting

**What it is.** An agent watches ticket drops and shops for price errors, buys tickets or mispriced goods, and resells them above the price paid.

**Why rejected.** Ticket resale for profit is an offence in Poland. Art. 133 § 1 of the Kodeks wykroczeń (consolidated text Dz.U. 2025 poz. 734, read 14 Oct 2026): "Kto nabywa w celu odprzedaży z zyskiem bilety wstępu na imprezy artystyczne, rozrywkowe lub sportowe albo kto bilety takie sprzedaje z zyskiem, podlega karze aresztu, ograniczenia wolności albo grzywny." § 2 adds that attempt and aiding are punishable too. So the automated version breaks Polish law: L=0.

**Price errors.** Buying at an obvious price error is legal to try, but the seller may refuse or cancel the order (Polish civil-law rules on mistake; no specific source re-verified this run), so value is low and unpredictable. No ToS or law needs breaking for personal deal alerts, but it is not an income stream.

**Legitimate small variant.** Personal deal alerts: the agent watches prices of items you already plan to buy and tells you when they drop. Savings, not income. Selling a ticket you cannot use at or below face value through the organiser's official resale is fine.

**Sources:** [Kodeks wykroczeń consolidated text (ISAP)](https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19710120114/U/D19710114Lj.pdf)
