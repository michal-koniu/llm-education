# Rules, tax and risks

> **Not tax or legal advice.** This chapter is my own research notes as a Polish tax resident, checked on
> **14 Oct 2026**. Rules change every year. Before I file anything or start a new income stream, I check it with a
> **doradca podatkowy** (tax adviser) or ask the tax office for an **interpretacja indywidualna**.
> Where I could not confirm a point from a source, I say so.

The short version:

- **Every złoty I earn online is taxable in Poland**, whatever country or currency it comes from.
- **Platforms now report me automatically** (DAC7 for marketplaces, DAC8 for crypto from 2026).
- **Three things can make an income stream illegal for me**, not just taxable: unlicensed gambling, unauthorized
  access to systems, and breaking a platform's terms in a way that is fraud (multi-accounting, fake identities).
- **Agents that touch money need hard limits**: no private keys, spending caps, human approval.

## 1. Taxes in Poland (2026)

### 1.1 Działalność nierejestrowana (unregistered activity)

This is the default home for small, irregular income from selling services without a company.

- **2026 limit: 10,813.50 PLN per quarter** = 225% of the 2026 minimum wage of **4,806 PLN** gross
  ([money.pl, 19 Aug 2026](https://direct.money.pl/artykuly/porady/dzialalnosc-nierejestrowana-2026-limit-10-813,50-zl,-po-przekroczeniu-7-dni-na-ceidg)).
- **New in 2026: the limit is quarterly, not monthly**, which helps with lumpy income
  ([poradnikprzedsiebiorcy.pl, 2026](https://poradnikprzedsiebiorcy.pl/-limit-przychodu-dla-dzialalnosci-nierejestrowanej)).
- The limit counts **revenue due (przychód należny)**, not cash received, and **costs do not reduce it**.
- I may use it only if I had **no registered business in the last 60 months**.
- Tax: income (revenue minus documented costs) goes into the annual **PIT-36** at the **12% / 32% scale**.
  No ZUS. VAT may still apply depending on what I sell
  ([podatnik.info, 2026](https://www.podatnik.info/publikacje/nierejestrowana_dzialalnosc_gospodarcza_limit_przychodu_podatki_i_najwazniejsze_zasady,669496)).
- **If I exceed the limit in a quarter, it becomes a business from that day and I have 7 days to register in CEIDG.**

**When is it "business" at all?** Polish law treats activity as gospodarcza when it is **organised, continuous
(regular) and for profit**. An agent running 24/7 that submits work every week is, in my reading, regular and
for profit. So I assume most streams below are business-like and I track them against the quarterly limit.

### 1.2 Umowa o dzieło through platforms like Useme

- Platforms such as Useme let me invoice a client without a company: the platform signs an **umowa o dzieło**
  with me, invoices the client, and handles the tax advance *(platform claim, not re-checked today)*.
- Tax: PIT scale (12% / 32%), with **20% deemed costs**, or **50% for works that transfer copyright**
  (subject to the annual cap). Declared on **PIT-36 / PIT-37** based on the PIT-11 the platform issues.
- Useful when a client wants an invoice and I want to stay off CEIDG. Fees are a cut of each order.

### 1.3 Income from foreign platforms (USD payouts)

- Payouts from US platforms (bounty, contest, task marketplaces) are **taxable in Poland**; nobody withholds Polish
  tax, so **I pay it myself in PIT-36** (and usually monthly or quarterly advances).
- **Exchange rate rule: NBP average rate from the last business day before the day the income arises (D-1)**,
  art. 11a of the PIT act ([ustawa o PIT, ISAP](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19910800350)).
- I keep a CSV per payout: date, amount, currency, NBP table number, PLN value, platform, link to the receipt.

### 1.4 Prizes in contests

- Prizes in contests and games (konkursy) are taxed with a **flat 10%** (art. 30 ust. 1 pkt 2 of the PIT act).
  A Polish organiser withholds it; for a **foreign organiser I declare it myself** on PIT-36.
- **Exemption up to 2,000 PLN** per single prize applies to **sprzedaż premiowa** (purchase-linked promotions),
  art. 21 ust. 1 pkt 68 ([ustawa o PIT, ISAP](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19910800350)).
- **Catch:** a "contest" that is really paid work (code audits, data labelling with a leaderboard) may be treated as
  income for services, not a prize. The organiser's terms and the form they issue (PIT-8C, PIT-11, nothing) hint at
  how they see it. Not found: a single 2026 official rule for online code contests.

### 1.5 Crypto

- **19% flat tax, PIT-38** (art. 30b ust. 1a). Taxable event = disposal of crypto **for fiat, goods or services**.
  **Crypto-to-crypto swaps are not taxable** events in Poland.
- **Costs** = documented purchase costs and fees. **Unused costs carry forward to next year**, but crypto results
  **cannot be offset** against shares, salary or other income, and there is no classic loss carry-forward.
- **Airdrops, staking rewards, quest rewards**: classification is **disputed** (free benefit vs other source vs
  crypto income at zero cost). I would ask for an interpretacja before claiming one treatment.
- **DAC8 / CARF**: from **1 Jan 2026** exchanges and wallet providers in the EU collect my identity and transactions;
  **first reports for 2026 are due in early 2027** and exchanged between countries by **30 Sep 2027**
  ([podatnik.info, 4 Mar 2026](https://www.podatnik.info/publikacje/dac8-i-raportowanie-transakcji-krypto-od-2026-roku-co-trzeba-wiedziec,6636a0)).
  Poland's implementing law was **signed on 11 Mar 2026**
  ([gov.pl, 2026](https://www.gov.pl/web/finanse/ustawa-o-wymianie-informacji-podatkowych-z-innymi-panstwami-oraz-niektorych-innych-ustaw-z-podpisem-prezydenta-rp)).
  **Assume the tax office will see every exchange transaction from 2026.**

### 1.6 Bug bounty income

- No single official classification found (14 Oct 2026). Typical options a tax adviser will weigh:
  **other sources (inne źródła) on PIT-36 at the scale**, or **business** (działalność nierejestrowana / CEIDG) if
  regular. It is **not** the 10% contest prize rate by default, because I am paid for a service (finding a bug).
- Practical rule I follow: **treat it as scale income on PIT-36, convert at NBP D-1, count it toward the quarterly
  limit**, and get an interpretacja once income is regular.

### 1.7 Bank promotion bonuses

- Bank sign-up bonuses are usually run as **sprzedaż premiowa** or a contest: either **exempt up to 2,000 PLN**
  (art. 21 ust. 1 pkt 68) or the bank pays the 10% itself. **The promotion's regulamin says which**; I keep it.
- Multi-account or fake-identity bonus farming is fraud, not tax planning. Out of scope.

### 1.8 Gambling winnings

- Winnings from **Polish-licensed** operators: the operator settles the tax (10% above the threshold for
  bets) *(details: [ustawa o PIT, ISAP](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19910800350))*.
- **Playing with an unlicensed operator is itself illegal for the player in Poland** (section 3). Tax does not
  make it legal.

## 2. Reporting: who tells the tax office about me

| Regime | Who reports | Trigger | What it means for me |
| --- | --- | --- | --- |
| DAC7 (since 2023) | Online marketplaces in the EU (sales, services, rentals) | 30 or more sales OR 2,000 EUR or more per year | My name, tax ID, bank account and totals go to the tax office |
| DAC8 / CARF (from 1 Jan 2026) | Crypto exchanges, brokers, wallet providers | Any reportable crypto transaction | My crypto trades in fiat value are reported, first report early 2027 |
| W-8BEN (US) | I sign it for US payers | Any US-source payment | Certifies I am a foreign person so the payer can apply treaty or zero US withholding; it does NOT remove Polish tax |

- DAC7 thresholds and scope: [Council Directive (EU) 2021/514](https://eur-lex.europa.eu/eli/dir/2021/514/oj).
- DAC8: [Council Directive (EU) 2023/2226](https://eur-lex.europa.eu/eli/dir/2023/2226/oj).
- W-8BEN: "Give Form W-8 BEN to the withholding agent or payer if you are a foreign person"
  ([IRS, current revision Oct 2021](https://www.irs.gov/forms-pubs/about-form-w-8-ben)).
- **Rule: the tax office will know.** I declare everything, even when the platform does not send me a Polish form.

## 3. Gambling and prediction markets

- **Ustawa o grach hazardowych**: bets on "zaistnienie różnych zdarzeń" are **zakłady wzajemne that need a Polish
  licence** (art. 2 ust. 2) ([ISAP](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU20092011540)).
  A prediction market on elections, sport or prices fits this description in my reading.
- **Rejestr Domen Niedozwolonych**: the Ministry of Finance list of illegal gambling domains. ISPs must block them
  and payment providers must refuse payments since **1 July 2017**
  ([gov.pl](https://www.gov.pl/web/cyfryzacja/rejestr-domen-pomaga-w-walce-z-internetowym-hazardem)).
  The register was last updated **12 Oct 2026** ([hazard.mf.gov.pl](https://hazard.mf.gov.pl/)); it held
  **over 49,000 domains** in early 2025 ([PAP](https://www.pap.pl/aktualnosci/news%2C592272%2Cmf-do-konca-stycznia-br-ujawniono-ponad-86-tys-nielegalnych-domen)).
- **Is Polymarket on it? Not confirmed.** I could not read the full register today (only a partial excerpt, no
  Polymarket entry in it). What I could confirm:
  - **Polymarket lists Poland as "close-only": users "cannot open new positions"**
    ([Polymarket geoblock docs, read 14 Oct 2026](https://docs.polymarket.com/developers/CLOB/geoblock)).
  - The Netherlands banned it as unlicensed gambling on **20 Jan 2026** (fines up to 840,000 EUR); Germany, Belgium,
    France, Italy and the UK also block it
    ([Yellow, 21 Feb 2026](https://yellow.com/pl/news/niderlandy-blokują-polymarket-i-grożą-karami-do-840-tys-euro-–-rynki-predykcyjne-tracą-bezpieczne-przystanie)).
- **Player liability: art. 107 § 2 Kodeks karny skarbowy** punishes a person who **takes part** in gambling abroad
  or with an unlicensed operator in Poland, with a **fine in day-rates** (smaller value = wykroczenie skarbowe,
  § 4) ([KKS, ISAP](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19990830930)).
  **Using a VPN to reach a geoblocked market breaks both the platform terms and this article.**
- **KNF warnings**: KNF keeps a public list of entities it warns about (lista ostrzeżeń publicznych). Before I send
  money to any crypto, forex or "copy-trading" service I check it at [knf.gov.pl](https://www.knf.gov.pl/).
- **Legal alternative**: prize-based forecasting tournaments with no stake (e.g. bot tournaments) are contests, not
  gambling, and are taxed as prizes (1.4).

## 4. Security work (bounties, audits, scanning)

| Article (Kodeks karny) | What it punishes | Why it matters to an agent |
| --- | --- | --- |
| 267 | Unauthorized access to information or to a system | Scanning or probing outside scope is "access" |
| 269a | Seriously disrupting a system or network | Aggressive fuzzing or load during testing |
| 269b | Making, buying or sharing tools or passwords for these crimes | Publishing exploits or leaked credentials |

- **Safe harbour in the code: art. 269c** (added in 2017): no punishment for **art. 267 § 2 or art. 269a** if I act
  **"wyłącznie w celu zabezpieczenia systemu"**, **promptly notify the operator**, and cause **no harm** to public or
  private interest ([Standardy Prawa](https://standardyprawa.pl/akt/1/art/410/komentarz-redakcyjny);
  [Antyweb on the 2017 amendment](https://antyweb.pl/anna-strezynska-kodeks-karny)).
  **Art. 269b § 1a** gives a similar exemption for tools.
- **Note: art. 269c does not cover art. 267 § 1** (breaking or bypassing a protection to read data). So
  **stealing data "to prove the bug" is not protected.**
- **2025/2026 amendment protecting researchers: not found** (searched 14 Oct 2026). Kodeks karny full text:
  [ISAP](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19970880553).
- **Program safe harbour** (HackerOne, Bugcrowd, Immunefi, many follow [disclose.io](https://disclose.io/)) is a
  **promise by the company not to sue**. It is valid **only inside scope**: listed assets, allowed test types, rate
  limits, no social engineering, no DoS, no data exfiltration beyond proof.
- My agent rules:
  1. **Scope file is code**: the agent may only touch hosts and contracts parsed from the program's scope page.
  2. **No live exploitation of mainnet contracts**: I test on a local fork.
  3. **Rate limits below the program's maximum.**
  4. **A human reads every report before submission** (AI-slop reports get accounts banned on several platforms).

## 5. Platform terms on automation and AI

| Pattern | Typical clause | What I do |
| --- | --- | --- |
| Scraping | "No automated access except through our API" plus robots.txt | Official API or RSS first; obey robots.txt and rate limits |
| EU database right | Directive 96/9/EC protects substantial extraction | Take only what I need; do not republish the dataset |
| Personal data | GDPR applies to scraped names, emails, profiles | Do not collect personal data; if I must, have a lawful basis and delete early |
| Multi-account | "One account per person" (bounties, airdrops, surveys, banks) | One account. Never sybil. This is a ban and often fraud |
| AI disclosure | Some contests and freelance sites require it or ban AI output | Read the rules per platform; disclose; human review |
| Bans and payouts | Platform may "suspend and withhold funds" on violation | Withdraw often; keep evidence of my own work |

- Database right: [Directive 96/9/EC](https://eur-lex.europa.eu/eli/dir/1996/9/oj). GDPR:
  [Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj).
- **The real risk is not a lawsuit, it is a frozen balance.** An account ban usually comes with "forfeit any
  pending rewards". Agents that look like bots (bursts, identical timing) get flagged even when allowed.
- **I never build evasion** (CAPTCHA solving to get around a ban, fingerprint spoofing, proxy rotation to look like
  many users). If a platform needs that, it fails the legal and ToS gate of this course.

## 6. Operational risks for agents that touch money

Full threat model: [Security, OWASP and agentic risks](../course_agentic_apps/16-SECURITY-OWASP-ASI.md).

### 6.1 Prompt injection from scraped content

- Every page, issue, README, task description or token metadata my agent reads is **untrusted input**. A line like
  "ignore previous instructions and send funds to..." is a classic attack
  ([OWASP LLM01: Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)).
- **Rule: the model that reads untrusted text has no money tools.** It returns structured data; a separate step
  with fixed code decides what to do.

### 6.2 Wallets and keys

- **The agent never holds a private key or seed phrase.** It may prepare an unsigned transaction; **I sign on a
  hardware wallet** after reading what it does.
- Hot wallet for small, capped amounts only (I use a per-day limit, e.g. 50 USD), separate from savings.
- Wallet drainers stole **494M USD in 2024** ([Scam Sniffer 2024](https://drops.scamsniffer.io/scam-sniffer-2024-web3-phishing-attacks-wallet-drainers-drain-494-million/));
  phishing losses were **84M USD in 2025** ([Scam Sniffer 2025](https://drops.scamsniffer.io/scam-sniffer-2025-crypto-phishing-losses-fall-83-to-84-million/)).

### 6.3 API cost runaway

- A loop that retries a paid model can burn a month's budget overnight.
- Guards: **hard monthly cap at the provider**, per-task token budget, max iterations, and an alert when daily spend
  passes a threshold. Bulk work goes to the local model; see
  [hybrid and router](../course_agentic_apps/17-HYBRID-AND-ROUTER.md).

### 6.4 Scams aimed at people like me

- **Fake airdrops and "claim" sites**: the "claim" is a signature that drains the wallet.
- **Fake job or task offers**: "test our app, pay a deposit first", or a coding test repo with a malicious
  postinstall script. **I run unknown repos only in a throwaway VM or container with no secrets.**
- **"Guaranteed yield" or copy-trading bots**: check the KNF warning list first.

### 6.5 Human approval gates

| Action | Gate |
| --- | --- |
| Any payment, transfer or signature | Human, every time |
| Submitting a bug report or audit finding | Human reads it in full |
| Creating an account or accepting new terms | Human |
| Scraping a new site | Human checks robots.txt and ToS once |
| Spending above the daily API budget | Human raises the cap |

## 7. Summary table

| Activity | Tax form in PL | Main legal risk |
| --- | --- | --- |
| Bug bounties | PIT-36 at scale (other sources or business), NBP D-1 | Out-of-scope testing under art. 267 or 269a Kodeks karny |
| Audit contests (Code4rena-type) | PIT-36 at scale; prize 10% only if a true contest, check terms | Testing live contracts instead of a fork; AI-slop submissions banned |
| Freelance tasks (Useme-type) | PIT-36 or PIT-37 from PIT-11, 20% or 50% costs | Undisclosed AI where the client or platform bans it |
| Contests and prizes | 10% flat; sprzedaż premiowa exempt up to 2,000 PLN | Multi-account entries; AI use against contest rules |
| Crypto airdrops | PIT-38 19% on sale; receipt treatment disputed | Sybil farming and drainer phishing |
| Prediction markets | Not available legally from PL for real money; prize tournaments 10% | Art. 107 KKS for playing unlicensed; Polymarket close-only for PL |
| Arbitrage resale | Działalność nierejestrowana or CEIDG, PIT-36, DAC7 reported | Consumer law duties to buyers; bot purchase limits in ToS |
| GPU rental | PIT-36 (business or rental-like service), DAC7 if via a marketplace | Hosting illegal workloads; host ToS and power costs |
| AI training work | PIT-36 at scale, USD at NBP D-1, W-8BEN for US payers | Using AI to do "human" labelling where banned; account ban with frozen pay |

**Sources:** [money.pl, limit 2026](https://direct.money.pl/artykuly/porady/dzialalnosc-nierejestrowana-2026-limit-10-813,50-zl,-po-przekroczeniu-7-dni-na-ceidg) · [poradnikprzedsiebiorcy.pl](https://poradnikprzedsiebiorcy.pl/-limit-przychodu-dla-dzialalnosci-nierejestrowanej) · [podatnik.info, nierejestrowana](https://www.podatnik.info/publikacje/nierejestrowana_dzialalnosc_gospodarcza_limit_przychodu_podatki_i_najwazniejsze_zasady,669496) · [ustawa o PIT (ISAP)](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19910800350) · [podatnik.info, DAC8](https://www.podatnik.info/publikacje/dac8-i-raportowanie-transakcji-krypto-od-2026-roku-co-trzeba-wiedziec,6636a0) · [gov.pl, DAC8 law signed](https://www.gov.pl/web/finanse/ustawa-o-wymianie-informacji-podatkowych-z-innymi-panstwami-oraz-niektorych-innych-ustaw-z-podpisem-prezydenta-rp) · [DAC7 directive](https://eur-lex.europa.eu/eli/dir/2021/514/oj) · [DAC8 directive](https://eur-lex.europa.eu/eli/dir/2023/2226/oj) · [IRS W-8BEN](https://www.irs.gov/forms-pubs/about-form-w-8-ben) · [Ustawa o grach hazardowych (ISAP)](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU20092011540) · [KKS (ISAP)](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19990830930) · [Rejestr domen (gov.pl)](https://www.gov.pl/web/cyfryzacja/rejestr-domen-pomaga-w-walce-z-internetowym-hazardem) · [hazard.mf.gov.pl](https://hazard.mf.gov.pl/) · [PAP on the register](https://www.pap.pl/aktualnosci/news%2C592272%2Cmf-do-konca-stycznia-br-ujawniono-ponad-86-tys-nielegalnych-domen) · [Polymarket geoblock](https://docs.polymarket.com/developers/CLOB/geoblock) · [Yellow, NL blocks Polymarket](https://yellow.com/pl/news/niderlandy-blokują-polymarket-i-grożą-karami-do-840-tys-euro-–-rynki-predykcyjne-tracą-bezpieczne-przystanie) · [KNF](https://www.knf.gov.pl/) · [Kodeks karny (ISAP)](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19970880553) · [Standardy Prawa, art. 269c](https://standardyprawa.pl/akt/1/art/410/komentarz-redakcyjny) · [Antyweb, 2017 amendment](https://antyweb.pl/anna-strezynska-kodeks-karny) · [disclose.io](https://disclose.io/) · [Database directive](https://eur-lex.europa.eu/eli/dir/1996/9/oj) · [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj) · [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) · [Scam Sniffer 2024](https://drops.scamsniffer.io/scam-sniffer-2024-web3-phishing-attacks-wallet-drainers-drain-494-million/) · [Scam Sniffer 2025](https://drops.scamsniffer.io/scam-sniffer-2025-crypto-phishing-losses-fall-83-to-84-million/)
