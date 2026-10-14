# AI income asymmetries

Where can an agentic AI app on a hybrid setup earn money online **without founding a company or selling a product**?
I looked at 22 candidates: bounties, contests, crypto airdrops, prediction markets, arbitrage, paid manual work,
surveys, compute rental and claims. For each one I asked a single question: **is money still paid for manual work
here that my agents can now do faster, while most competitors still do it by hand?**

My setup: a local rig with DeepSeek-V4-Flash-0731 (4 parallel slots, 24/7), Claude Opus 5.5 as planner and reviewer,
and cheap online models for overflow ([../cheap-free-models/README.md](../cheap-free-models/README.md)). I live in
Poland, so legality and tax are checked for a Polish resident. Facts are as of 14 Oct 2026.

> **Not financial, legal or tax advice.** Platforms, rules and prices change monthly. Re-check before acting, and
> ask a doradca podatkowy about your own case.

## The short answer

- **There is no easy money here, and the research shows it.** No candidate scored above 57 out of 100. Median
  realistic income per opportunity is tens to a few hundred USD a month, usually lumpy.
- **Where AI is already everywhere, the asymmetry has flipped.** Open-source bounties get swarmed by coding agents
  (40 to 1,447 comments per bounty), and bug bounty platforms now ban "AI slop" volume. Being fast is not an edge
  when everyone is fast.
- **The remaining asymmetry is in boring, local, paperwork-heavy niches:** Polish bailiff auction notices and
  appraisals, contest rules (regulaminy), bank promotion terms, small data science competitions with 36 teams, and
  AI red-teaming, where an uncensored local model generates attacks at no token cost.
- **The agent's real job is search and triage, not the final act.** It reads thousands of listings, rules and
  notices, and hands me the few worth my time. The approval click, the identity and the accountability stay mine.
- **The scaled versions of airdrops, surveys and quests are rejected.** They only scale through many accounts or
  bot answers, which break the terms and, for surveys, amount to fraud. The one-identity versions are too small.
- **A realistic portfolio** of 4-5 of the top 10, run in parallel on one agent pipeline, is my estimate of
  **about 500-1,300 USD a month after 3-6 months** (sum of the profile medians). That is a side income that also
  teaches me agent engineering, not a salary.

## The top 10

Score out of 100. Realistic income is the median case for 10 hours a week of my time plus agents running 24/7.

| # | Opportunity | Score | Realistic income | Capital needed |
|---|---|---|---|---|
| 1 | [Claiming money you are already owed](01-OPPORTUNITIES.md#1-claiming-money-you-are-already-owed) | 57 | 20-80 USD/month averaged over a year (one or two flight claims plus a few refunds) | 0 USD |
| 2 | [Per-task freelance gigs (Upwork, Fiverr, Useme)](01-OPPORTUNITIES.md#2-per-task-freelance-gigs-upwork-fiverr-useme) | 56 | 0-300 USD/month in months 1-2, 200-800 USD/month median once a profile has reviews | ~0-50 USD (Upwork Connects) |
| 3 | [Data science and AI competitions](01-OPPORTUNITIES.md#3-data-science-and-ai-competitions) | 56 | 0-200 USD/month averaged over a year (median case: 0, with rare lumps of 1,000-10,000 USD) | 0 USD (the local rig covers training and offline inference) |
| 4 | [AI red-teaming bounties and arenas](01-OPPORTUNITIES.md#4-ai-red-teaming-bounties-and-arenas) | 55 | 0-300 USD/month median (lumpy: most months 0, an occasional 500-2,500 USD finding) | ~0-100 USD (API judge tokens) |
| 5 | [AI forecasting tournaments (the legal side of prediction markets)](01-OPPORTUNITIES.md#5-ai-forecasting-tournaments-the-legal-side-of-prediction-markets) | 55 | 0-150 USD/month median case (prizes are seasonal and lumpy) | 0 USD (sponsored LLM credits) |
| 6 | [Bailiff and public auctions](01-OPPORTUNITIES.md#6-bailiff-and-public-auctions) | 52 | 0-400 USD/month (median ~150 USD after a slow first quarter) | 1,000-2,000 USD revolving (deposits plus purchase price) |
| 7 | [Smart-contract audit contests and bug bounties](01-OPPORTUNITIES.md#7-smart-contract-audit-contests-and-bug-bounties) | 52 | 0-500 USD/month (median case for a newcomer at 10 h/week: about 0-200) | 0 USD (plus API tokens; no funds at risk) |
| 8 | [Prize contests with a creative task (Polish "konkursy", design contests)](01-OPPORTUNITIES.md#8-prize-contests-with-a-creative-task-polish-konkursy-design-contests) | 51 | 0-200 USD/month median, mostly in goods, very lumpy | 0 (more if you chase receipt-based contests) |
| 9 | [Bank promotion tracking (promocje bankowe)](01-OPPORTUNITIES.md#9-bank-promotion-tracking-promocje-bankowe) | 51 | 50-150 USD/month averaged over a year (about 2,500-6,000 PLN/year, median ~3,500 PLN) | 0 (you move your own salary and spending through the accounts) |
| 10 | [Web and app bug bounty with AI-assisted recon](01-OPPORTUNITIES.md#10-web-and-app-bug-bounty-with-ai-assisted-recon) | 48 | 0-300 USD/month (median case: 0 in the first 2-3 months, then occasional low/medium payouts) | ~0-50 USD (API tokens, a VPS for out-of-band callbacks) |

Runners-up, below the cut but fully profiled:

| # | Opportunity | Score | Realistic income | Capital needed |
|---|---|---|---|---|
| 11 | [Expert AI-training work (Outlier, DataAnnotation, Alignerr, Mindrift)](01-OPPORTUNITIES.md#11-expert-ai-training-work-outlier-dataannotation-alignerr-mindrift) | 47 | 300-900 USD/month for 10 h/week of your own time, median case, with empty weeks | 0 |
| 12 | [Marketplace arbitrage (OLX, Allegro, Vinted)](01-OPPORTUNITIES.md#12-marketplace-arbitrage-olx-allegro-vinted) | 45 | 50-400 USD/month (median ~150 USD) | 500-1,500 USD stock |
| 13 | [Open-source issue bounties](01-OPPORTUNITIES.md#13-open-source-issue-bounties) | 44 | 0-150 USD/month (median case: close to 0) | 0 USD (plus a few USD of API tokens) |
| 14 | [Expired domain flipping](01-OPPORTUNITIES.md#14-expired-domain-flipping) | 37 | 0-100 USD/month (median close to 0 in year one, often negative after renewals) | 300-1,500 USD per year for registrations and renewals |
| 15 | [Renting out the idle GPU rig](01-OPPORTUNITIES.md#15-renting-out-the-idle-gpu-rig) | 36 | 0-50 USD/month net median (AMD cards find almost no renters) | 0 USD (rig already owned) |

**How to read the ranking.** The score rewards safety and legality as much as money. That is why "claiming money you
are already owed" is first: it is clean and certain but small. If I sort by **earnings plus asymmetry** (E + A), the
order changes: bailiff and public auctions (21), prize contests (18), freelance gigs and AI red-teaming (17),
audit contests (16). Expert AI-training work pays the most per hour (300-900 USD a month) but has almost no agent
leverage, because the paid part must be done by a human.

## How I scored

| Letter | What it measures | Points |
|---|---|---|
| E | Realistic net earnings per month, median case (under 100 USD = 3, 100-500 = 8, 500-1,500 = 14, 1,500-4,000 = 20, above 4,000 = 25) | 25 |
| A | Asymmetry: how much an agent multiplies output vs manual competitors, and how few already automate | 25 |
| F | Feasibility: capital, skills, setup time, access from Poland | 15 |
| L | Legal and terms: how clean the automated version is in Poland and the EU (a violation means rejection) | 20 |
| R | Risk: variance, capital loss, ban risk, how fast the window closes (higher is safer) | 15 |

Ties are broken by E + A. Every profile shows its letter scores, so you can re-weight them for yourself.

## Where I would start

1. **Build the pipeline once** ([02-HYBRID-ARCHITECTURE.md](02-HYBRID-ARCHITECTURE.md)): watchers, local triage,
   Opus review, a human approval gate and an SQLite ledger of every attempt.
2. **Run three one-week tests in parallel**, each profile has one: one zero-capital asymmetry play (AI red-teaming or a
   small data science competition), one steady earner (freelance gigs on Useme or Upwork), and one Polish paperwork
   niche (bailiff auctions or prize contests).
3. **Add the "free money" habits** that need almost no agent time: claims and bank promotions.
4. **Apply the kill criteria** at the end of each test. Keep what clears them, drop the rest, and move the freed
   slot to the next candidate on the list.

## Rejected candidates

| Candidate | Why rejected |
|---|---|
| Airdrop and points farming | The scaled version is multi-wallet sybil farming: filtered and banned (Linea, LayerZero). One real wallet with a tracker is legal but small. |
| Paid surveys and microtasks | Agent-filled answers breach MTurk and Prolific rules, are detected, and defraud the researcher. Manual surveys pay survey rates. |
| Crypto quest platforms | Scaling needs many accounts or fake engagement, forbidden by Galxe's terms. |
| DeFi bots (liquidations, arbitrage, MEV) | Fully automated by professional searchers already; needs capital and low latency; no agent edge. |
| Bittensor subnet mining | Main subnets need NVIDIA cards and Intel TDX; pay tracks the TAO price. Not feasible on AMD with 2,000 USD. |
| Decentralized AI networks | Mostly testnet points, NVIDIA-only clients, and node farming is sybil behaviour. |
| Ticket resale and price errors | Reselling tickets above face value is an offence in Poland (art. 133 Kodeks wykroczeń); price errors are not income. |

Full notes with sources are at the end of [01-OPPORTUNITIES.md](01-OPPORTUNITIES.md).

## Files

| File | What is in it |
|---|---|
| [01-OPPORTUNITIES.md](01-OPPORTUNITIES.md) | 15 profiles: money flow, asymmetry, agent pipeline, hybrid split, numbers, how to start, rules, a one-week test, kill criteria; then the rejected notes |
| [02-HYBRID-ARCHITECTURE.md](02-HYBRID-ARCHITECTURE.md) | One agent pipeline for all opportunities, routing local vs paid, cost math, the edge ledger, safety rails, rig scheduling |
| [03-RULES-TAX-RISKS.md](03-RULES-TAX-RISKS.md) | Polish tax for each income type, DAC7 and DAC8 reporting, gambling law, security research law, platform terms, operational risks |
| [SOURCES.md](SOURCES.md) | All sources, accessed 13-14 Oct 2026 |

**Research limits.** Some figures were not published anywhere I could reach, such as Fiverr and Useme fees, Gray Swan
prize pools and median bug bounty earnings. The profiles mark them "not found" rather than guess. Related courses:
[../course_agentic_apps/17-HYBRID-AND-ROUTER.md](../course_agentic_apps/17-HYBRID-AND-ROUTER.md),
[../course_agentic_apps/16-SECURITY-OWASP-ASI.md](../course_agentic_apps/16-SECURITY-OWASP-ASI.md),
[../agent-harnesses/README.md](../agent-harnesses/README.md).
