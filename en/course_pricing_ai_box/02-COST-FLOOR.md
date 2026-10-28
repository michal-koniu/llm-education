# Part 02 · The cost floor: what one office really costs you

> **Goal of this part.** You compute the lowest monthly price at which serving one office still makes
> business sense, and you discover which cost line decides it. Spoiler: it is not the hardware.
>
> **Time:** ~4 h · **Level:** ⭐⭐⭐ · **Produces:** `pricing/02-cost-floor.md`, the first filled section of
> `pricing/01-anchors.md` · **Tool:** `tools/pricing_model.py floor`

---

## 0. The problem

The box *looks* like a hardware business: a 128 GB mini PC on a lawyer's shelf. So the first instinct is
to price it like hardware: purchase price plus a margin. But the hardware is a one-off cost and the
customer can see its price on Ceneo. What keeps costing you every month, invisibly, is **your time**:
answering the phone, applying model updates, re-running the evaluation set, fixing a stuck OCR queue,
driving to the office when the box does not boot.

The repo already names this risk: *"hardware margin is thin and support is labour heavy; profit must come
from the monthly licence and repeatable workflows"* (`ai-business-asymmetries/02-OPPORTUNITIES.md`, profile
1), with the kill criterion *"monthly support exceeds 30% of revenue"*. This part turns those sentences
into a number.

---

## 1. Two kinds of cost

| | **Cost of goods sold (COGS)** | **Operating costs (OpEx)** |
| :-- | :-- | :-- |
| What | what you must spend to keep **one more** customer running | what you spend to run the company, whatever the number of customers |
| Box examples | support hours, model update share, monitoring, backup storage, hardware if you own it, spare parts | building new agents, sales, marketing, accounting office, your own salary, tools |
| Grows with | the number of offices | decisions you make |
| Paid from | the price | the **gross margin** (price − COGS) |

**Gross margin** = (price − COGS) ÷ price. It is the share of every złoty that is left to pay for
everything else: product development, sales and you.

Why the line matters: investors value a złoty of high-margin recurring revenue several times higher than a
złoty of low-margin revenue (part 08). And for you, before investors, the gross margin decides whether
adding customers makes you richer or just busier.

### Reference margins

| Kind of business | Typical gross margin | Source |
| :-- | :-- | :-- |
| Public SaaS companies (median) | ~77% | PitchBook, Q4 2025 |
| AI products (2025 → 2026 → 2027 plan) | 45% → 53% → 59% | ICONIQ *State of AI* 2026, *self-reported* |
| AI companies, target (median) | ~50% | Growth Unhinged 2026, *self-reported* |
| AI businesses, structural estimate | 50–60% vs 60–80%+ for classic SaaS | a16z, 2020 |
| Fast-scaling AI "Supernovas" | ~25% | Bessemer *State of AI* 2025 |
| Samsara (hardware sold inside a subscription) | ~77–78% non-GAAP | company results |
| Nutanix after moving appliances to subscription | 83% non-GAAP (Q4 FY2020) | company results |

The last two rows matter most to you. Samsara and Nutanix both ship hardware, and both reached software-like
margins **by treating hardware as a cost of the subscription, not as a product with its own margin**. Toast
went further and sold hardware at a loss (about −12% of recurring gross profit, per its earnings call),
because the subscription paid for it.

---

## 2. The cost lines of one office

All amounts are **PLN net, excluding VAT**. ⚠️ Ceneo and Apple show **gross** prices for consumers. Divide by
1.23 before using them (pitfall B38).

### 2.1 Hardware (prices checked 25 Oct 2026)

| Box | Gross (Ceneo / Apple) | **Net** | Fits under the 10,000 PLN one-off write-off? (part 05) |
| :-- | --: | --: | :-- |
| Minisforum MS-S1 MAX, Ryzen AI Max+ 395, 128 GB | 13,490–18,190 | **10,967–14,789** | no (just above) |
| HP Pro Max Edge, Ryzen AI Max+ 395, 128 GB | 19,999 | 16,259 | no |
| Mac mini M5 Pro, 64 GB | ~13,094 | ~10,645 | no (just above) |
| Mac mini M5 Pro, 48 GB | 11,099 | 9,024 | **yes** |
| ASUS Ascent GX10 (GB10, 128 GB / 1 TB) | from 26,999 | 21,950 | no |
| NVIDIA DGX Spark Founders Edition, 4 TB | 28,355 | 23,053 | no |
| Mac Studio M5 Max, 128 GB | ~24,734 | ~20,109 | no |

NVIDIA raised the DGX Spark 128 GB reference price from USD 3,999 to USD 4,699 in February 2026 because of
memory shortages (CHIP.pl). **Hardware prices move. Never print a hardware price in a contract without a
validity date.**

Which tier a given office needs is a technical decision covered in
`ai-business-asymmetries/03-LOCAL-FIRST.md`, section 3. For pricing, two facts matter:

- whether **you** own the box (the rent model) — then its amortisation is your COGS;
- or the **customer** owns it (they buy it, or lease it) — then it is not your COGS at all.

### 2.2 Installation

Unpacking, the box image, connecting the office's document folder, OCR of the existing archive, user
accounts, the first workflow tuned on their documents, a training hour. **Measure it** (field
experiment 02). Until you have a measurement, assume 16 hours for the first ten installations.

If the **setup fee** pays for installation (it should), installation is not in the monthly floor. Run the
calculator with `--install-h 0` in that case.

### 2.3 Support and monitoring

Phone and e-mail questions, a stuck queue, a user who forgot a password, a disk filling up, a remote
session. This is the line that decides your floor. The repo's own engineering — the health check, rollback
in under 5 minutes and the 3 a.m. runbook from `course_agentic_apps/18-RELEASE-AND-MAINTENANCE.md` — is
**directly a cost-of-goods reduction**: every check that runs automatically is an hour you do not bill
yourself for.

### 2.4 Model updates (shared)

A new Bielik or PLLuM version comes out. You download it, run it on your reference box, run your Polish
evaluation set (`course_agentic_apps/14-EVALUATION.md`), check every agent for regressions, prepare the
rollout and roll it out remotely. Assume 40 hours a quarter. **That work is done once and serves every
office**, so its cost per office falls as you grow. This is the first economy of scale in the business.

### 2.5 Other

Backup storage, a remote-management tool licence, an occasional spare part, professional liability
insurance (priced in the contracts course), travel. Assume PLN 100 per office per month and replace it with
real invoices.

### 2.6 The price of an hour

The calculator needs `--hour-cost`: what one hour of support work costs. Two traps:

- **It is not your own billing rate.** Example: a contractor billing a client PLN 1,500–2,000 per day. That is
  the price of *your* time to that client, not the cost of support work. If you price support at your own day
  rate, the floor becomes absurd and you will never sell.
- **It is not zero either.** "I do it myself in the evenings" is how founders end up with a business that
  needs them forever. Price the hour at **what you would pay someone else** to do first-line support and
  remote administration. I did not research a market rate for this; the default of PLN 200 per hour is an
  **assumption** — replace it with a quote from an IT services firm, which is also your future partner
  (`ai-business-asymmetries/02-OPPORTUNITIES.md`: *"partner with them as the AI layer, revenue share"*).

---

## 3. Run it

```bash
cd tools
python3 pricing_model.py floor                    # defaults: 10 offices, 2 h support, 75% margin
```

Default assumptions: hardware owned by the customer, 16 h installation spread over a 24-month contract,
2 h support per office per month at PLN 200, 40 h of model updates per quarter shared by all offices,
PLN 100 other costs, 75% target margin.

I ran it with different numbers of offices and support hours (all at PLN 200 per hour, customer-owned
hardware, installation still spread in the monthly figure):

| Scenario | COGS / office / month | Floor at 75% margin | Floor at 60% margin |
| :-- | --: | --: | --: |
| 5 offices, 2 h support | 1,167 | **4,667** | 2,917 |
| 20 offices, 2 h support | 767 | **3,067** | 1,917 |
| 100 offices, 2 h support | 660 | **2,640** | 1,650 |
| 20 offices, **1 h** support | 567 | **2,267** | 1,417 |
| 20 offices, **0.5 h** support | 467 | **1,867** | 1,167 |
| 20 offices, 1 h, **you own the box** (rent) | 871 | **3,485** | 2,178 |

Read the table slowly. Three lessons are in it:

1. **Support hours decide the floor.** Going from 2 h to 0.5 h per office per month lowers the floor more
   than going from 20 to 100 customers. Your strongest pricing move is an engineering move: a box that
   does not need you.
2. **The first offices are expensive to serve.** With five offices, the shared update cost is large per
   office. This is why early customers often get a "launch partner" price (part 07): you are not making
   money on them yet, and that is fine *if you know it*.
3. **A 75% software margin is hard at small-office prices.** Compare the floors with the reference prices
   from part 01: Beck-Noxtua at PLN 590 per seat is PLN 2,950 for a 5-seat office; LEX Kancelaria Prawna
   is PLN 298–722 per month. A floor of PLN 3,000+ for one office is above what Office K is used to paying
   for **all** its software. Either support falls to about 1 hour, or the margin target falls towards the
   AI-company norm of 50–60%, or the price must rest on a value argument strong enough to justify it
   (part 03).

### 3.1 A gross margin target — decide it now

Write one of these into `pricing/02-cost-floor.md` and say why:

| Target | When it is the right choice |
| :-- | :-- |
| **75%+** | You plan to raise venture money (part 08) and can push support below 1 h per office |
| **55–65%** | The AI-company norm in 2026. A realistic target for years 1–2 |
| **< 50%** | You are a services business. Fine for a lifestyle company, a problem for a scalable one |

You told me you want a company that scales with more expert agents. That points to 55–65% now and a plan
to reach 70%+ as agents are added — because a new agent sold to an existing office adds revenue with
**almost no new COGS** (the box, the support relationship and the update channel already exist). This is
the second economy of scale in the business, and it is the core of part 04.

---

## 4. How the floor falls over time

```
 COGS per office
   │█
   │█ █
   │█ █ ▆                       ← shared updates spread over more offices
   │█ █ █ ▆ ▅
   │█ █ █ █ █ ▅ ▄ ▄ ▃ ▃ ▃       ← support automation, standard box image
   │█ █ █ █ █ █ █ █ █ █ █ ▂ ▂   ← one more agent per office: revenue up, COGS flat
   └──────────────────────────► offices / time
```

Prices are much harder to raise than costs are to cut. So: **set the price from value (part 03), then make
sure the cost floor falls below it over time.** Never set the price from the floor of month one.

---

## 5. EXERCISE 02 — your floor

1. Copy the defaults into `pricing/02-cost-floor.md` as a table, one line per assumption.
2. Replace every assumption you can with a real number: a hardware quote, an IT firm's hourly rate,
   your measured installation time (field experiment 02).
3. Run `pricing_model.py floor` for 5, 20 and 100 offices, at your chosen margin.
4. Write into `pricing/01-anchors.md`, section *Cost floor*: **one number** for year 1 (at 10 offices) and
   one for year 3 (at your planned number of offices).

---

## 6. ⭐ FIELD EXPERIMENT 02 — how long does an installation take?

**Hypothesis.** Installing the box from a bare machine to a working first workflow takes more than a day
the first time and under half a day by the third time, if you script it.

**Procedure.** On a spare machine (or a VM if you have no spare box yet), install your full stack from
zero three times: OS, model server, the agent runner, the document ingestion, one workflow, a user
account, a backup job and the health check. Time each run with a stopwatch. After each run, script one
manual step.

**Prediction (mine).** Run 1: 10–16 h. Run 3: 3–5 h. The longest single step: OCR and indexing of a
realistic document archive, not the software.

| Run | Date | Total hours | Longest step | Steps scripted after this run |
| :-- | :-- | --: | :-- | :-- |
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

The difference between run 1 and run 3 is money: at 20 offices a year it is roughly 20 × (run 1 − run 3)
hours. Put the run-3 figure into `--install-h`.

---

## 7. Pitfalls

**B37 · Your own time priced at zero.**
*Symptom:* COGS has hardware and electricity but no hours. *Remedy:* every support hour is priced at the
rate you would pay someone else (section 2.6).

**B38 · Gross and net prices mixed.**
*Symptom:* a Ceneo price used as a cost. *Why it hurts:* 23% error on the largest line. *Remedy:* all
business calculations in PLN net. Write "net" in every column header.

**B39 · Development counted as COGS.**
*Symptom:* "every new agent costs me 80 hours, so the price must cover it." *Remedy:* building a new agent
is OpEx (an investment that serves all offices). Only the work needed to keep **one** office running is
COGS.

**B40 · Pricing from the floor of month one.**
*Symptom:* the first price is set to cover the costs of serving five offices. *Remedy:* the price comes from
value (part 03); the floor of month one tells you how many months you will lose money, not what to charge.

**B41 · Support creep.**
*Symptom:* "Could you also look at our printer?" — and you do, for free. *Why it hurts:* support is your
largest cost line and it grows silently. *Remedy:* a written support scope in the price book (part 07) and
a log of every support hour from the first pilot.

---

## 8. Checkpoint

- [ ] `pricing/02-cost-floor.md` has a table of assumptions, each marked *measured* or *assumed*.
- [ ] You ran the calculator for 5, 20 and 100 offices.
- [ ] You have chosen a gross margin target and written one sentence explaining why.
- [ ] `pricing/01-anchors.md`, *Cost floor*: one number for year 1 and one for year 3.
- [ ] Field experiment 02: at least run 1 is done.
- [ ] You can say which single cost line moves your floor the most, and what engineering would lower it.

Sources for this part: [SOURCES.md](SOURCES.md), section "Part 02".
