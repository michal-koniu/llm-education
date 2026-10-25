# Part 04 · Money, runway and risk budget

> **Goal of this part.** You decide how much of the contract income goes to the startup, how much stays as a
> safety buffer, and how much you are willing to lose before you stop. You learn what your tax form does to
> startup spending, where the startup should live for tax purposes now, and which administrative deadlines
> are already running.
>
> **Time:** ~4 h + one meeting with your accountant · **Level:** ⭐⭐⭐ · **Produces:** `founder/04-budget.md`,
> `founder/04-accountant-questions.md`

> **Not tax advice.** The figures are a simplified model built on rules researched on 25 Oct 2026. Your
> accountant computes your real numbers. Several rate questions below are explicitly **unresolved** — ask them.

---

## 0. The problem

The contract pays well, so money feels like the one thing you do not need to plan. That is exactly how founders
in your position lose a year's savings slowly: no budget, no limit, purchases made "for the startup" that the
tax form does not let you deduct, and no point at which you would admit the idea is not working.

A **risk budget** fixes this. It is a number of złoty and a number of hours you are willing to lose, decided
**before** you spend them, with a condition attached to each next step.

---

## 1. Three pots

```
 net income from the contract (part 01: ≈ 28,300 PLN/month on ryczałt — your accountant's figure replaces it)
   │
   ├── 1. LIFE           your real monthly costs (part 01, written number)
   ├── 2. SAFETY BUFFER  months of living costs in cash, untouched by the startup
   └── 3. STARTUP        the risk budget, released stage by stage
```

### 1.1 The safety buffer

How many months of living costs to hold, untouched? There is no researched rule for this course; my opinion is
**6–12 months**, more if you have dependants or a mortgage, because the contract can end on its notice period —
and a bank can end it for reasons that have nothing to do with you (part 02, §4: DORA gives banks explicit
termination rights).

Fill the buffer before the startup budget grows beyond the validation stage.

### 1.2 The risk budget, by stage

Release money in stages. Each stage has a cap and a **gate** — a condition that must be true before the next
stage's money is spent:

| Stage | What you buy | Cap (example — set yours) | Gate to the next stage |
| :-- | :-- | --: | :-- |
| **0 · Validation** (now → 3 months) | a lawyer's hour (part 02), accountant's hour, travel to interviews, a domain, your own AI subscriptions. The rig you already own | PLN 10,000 | ≥ 10 conversations, ≥ 2 offices at the "commitment" level (pricing course, part 06) |
| **1 · Pilots** (3 → 9 months) | one or two pilot boxes (PLN 9,000–23,000 net each — pricing course, part 02), insurance, a simple website, a lawyer for the pilot agreement | PLN 50,000 | ≥ 3 paying pilots (the repo's own kill criterion: *"fewer than 3 paying pilots after 4 months of active selling"*), support under 30% of revenue |
| **2 · First cohort** (9 → 18 months) | boxes for paying customers (or leasing — pricing course, part 05), a part-time helper, a company (part 06) | PLN 150,000 | ≥ 10 paying offices, monthly churn < 1%, NRR plan credible |

Write the caps **now**, while you are calm. Spending beyond a cap needs the gate to be met — not a good mood.

---

## 2. What your tax form does to startup spending

### 2.1 On ryczałt, startup costs are not deductible

Ryczałt taxes **revenue**, not income: costs are not deductible at all (art. 12(2) of the lump-sum tax act).
If the startup lives in your contract JDG and you are on ryczałt, a PLN 13,000 pilot box comes entirely out of
taxed money.

On the flat 19% tax (liniowy) the same box would reduce income tax and the 4.9% health contribution — roughly a
quarter of its price back.

### 2.2 So should you switch? The break-even

I extended the part 01 model: same contract revenue (PLN 428,400 a year), startup costs `S` spent through the JDG,
other business costs 2% of revenue in both cases:

| Startup spending per year, `S` | Net after everything — ryczałt 12% | Net — flat 19% | Ryczałt better by |
| --: | --: | --: | --: |
| 0 | 331,213 | 304,576 | **26,637** |
| 50,000 | 281,213 | 266,526 | **14,687** |
| 100,000 | 231,213 | 228,476 | **2,737** |
| 150,000 | 181,213 | 190,044 | −8,830 |
| 200,000 | 131,213 | 151,528 | −20,315 |

**Result:** with this contract, ryczałt stays cheaper unless the startup's deductible costs exceed roughly
**PLN 110,000 a year**. In stages 0 and 1 of section 1.2 you are well below that. So: **do not change your tax form
for the startup's sake** in the first year. Revisit it when stage 2 is in sight.

Two more facts change this later:

- **IP Box (5% on qualified IP income)** is available only on the tax scale or the flat tax, **not on ryczałt**
  (tax ruling 0114-KDIP3-3.4011.427.2019.1.MT). It matters once the product earns licence income — usually inside
  a company by then.
- **The tax form is chosen for the whole year**: by the 20th day of the month after the month of the first revenue
  in the year, with no voluntary switch during the year (art. 9). For 2027 that is most likely **by 20 February
  2027**. Put it in your calendar now.

### 2.3 If the startup earns money in the same JDG

You may sell pilots through your existing JDG before a company exists. Then the ryczałt **rate depends on what you
sell** — and some of it is genuinely unresolved:

| What you sell | Ryczałt rate (research, 25 Oct 2026) | Certainty |
| :-- | :-- | :-- |
| installation, configuration, IT consulting, systems management | 12% | clear |
| pure technical IT support | 8.5% allowed in one tax-office ruling (1 Sep 2026, *secondary source*) | one ruling |
| **software licences** (PKWiU 58.29.50.0) | **15%** — not 12% | clear |
| hosting, data processing | 15% | clear |
| **online software / SaaS** (58.29.40.0) | expressly excluded from 12%; by elimination **8.5%**, reportedly confirmed by two 2023 rulings (not verified) | **unresolved** |
| reselling a box unchanged | 3% (trade in goods) | clear for unprocessed goods |
| a box you **configure into a new product** | possibly 5.5% (manufacturing) | **unresolved — no ruling found** |

And the rule that makes it dangerous: different rates per activity are allowed **only if your revenue records
separate the streams**; otherwise the **highest** applicable rate applies to everything (art. 12(3)). The health
contribution tier is based on total revenue — you are already in the top tier (above PLN 300,000).

**Practical rule:** before the first startup invoice from the JDG, ask your accountant to set up a separate
revenue category per stream, and get their opinion on the rate for "box + installation + monthly subscription".

---

## 3. VAT and administration that already concern you

| Item | Fact (research, 25 Oct 2026) | What to do |
| :-- | :-- | :-- |
| **You are an active VAT payer** | the small-business exemption limit is PLN 240,000 from 2026; your contract revenue is far above it | VAT on startup purchases used for your taxed sales is deductible (art. 86 VAT Act) — another reason to buy startup equipment through the JDG, **after** the PKD codes cover the activity |
| **PKD 2025** | every JDG must update its activity codes to PKD 2025 **by 31 Dec 2026**; from 1 Jan 2027 CEIDG reclassifies automatically, possibly wrongly (gov.pl, 20 Oct 2026) | update now, and add the startup's codes in the same step |
| **KSeF** | mandatory e-invoicing for everyone from **1 Apr 2026**; penalties from 1 Jan 2027 | you already invoice the bank in KSeF; the startup invoices go the same way |

Code mapping for the update (GUS transition key, via the research):

| Activity | PKD 2007 | PKD 2025 |
| :-- | :-- | :-- |
| software development (your bank work, the agents) | 62.01.Z | 62.10.B |
| IT consulting | 62.02.Z | 62.20.A or 62.20.B |
| managing IT equipment | 62.03.Z | 62.20.Z |
| other IT services | 62.09.Z | 62.90.Z |
| data processing, hosting | 63.11.Z | 63.10.A–D |
| wholesale of ICT equipment | 46.51.Z | 46.50.Z |
| retail sale of ICT equipment | 47.41.Z | 47.40.Z |

Which of these you need is for your accountant to confirm; the deadline is not.

---

## 4. Social contributions: what does not apply to you

For completeness, so you do not chase reliefs you cannot get:

- **Full ZUS** in 2026: PLN 1,926.76 a month (base PLN 5,652; PLN 1,788.29 without sickness insurance).
- **Start-up relief** (6 months) and **preferential ZUS** (PLN 456.18): only for a new or long-dormant JDG — not
  yours.
- **Mały ZUS Plus**: needs prior-year revenue of at most PLN 120,000 — not yours.

Those reliefs will matter for a co-founder starting a fresh JDG, and they shape the legal-form decision later.

---

## 5. EXERCISE 04 — the budget

`founder/04-budget.md`:

```markdown
# Budget — <date>

Net income per month (accountant):            ____ PLN
Life per month:                               ____ PLN
Surplus per month:                            ____ PLN

Safety buffer target: __ months × life = ____ PLN   | today: ____ PLN
Monthly transfer to buffer until full:        ____ PLN
Monthly transfer to startup:                  ____ PLN

Risk budget
| Stage | Cap PLN | Hours/week | Gate | Deadline |
| 0 | | | | |
| 1 | | | | |
| 2 | | | | |

Stop condition (written now): I stop if ____________ by ________.
```

And `founder/04-accountant-questions.md` — at least these:

1. My real net income in 2026 and the projection for 2027 on ryczałt vs flat tax, with startup costs of PLN 20k,
   50k, 100k.
2. Can I buy startup equipment through my JDG and deduct VAT? Which PKD codes do I need to add?
3. Which ryczałt rate applies to a configured box, to its installation, to the monthly subscription, to a licence?
   How do we keep separate revenue records?
4. At what point would you move the startup into a company, and which form?
5. The deadline for choosing my 2027 tax form.

---

## 6. ⭐ FIELD EXPERIMENT 04 — the real spend

**Hypothesis.** Over three months of stage 0, real startup spending stays under PLN 10,000, but the hours exceed your
plan by at least 30%.

**Procedure.** Log every złoty and every hour spent on the startup in `founder/04-spend.csv`
(`date,category,amount_pln_net,hours,note`). Categories: `legal`, `accounting`, `hardware`, `software`, `travel`,
`marketing`, `other`. At the end of each month compare with the plan.

**Prediction (mine).** Month 1: legal and accounting dominate. Hours: plan 10 a week, reality 13–15, mostly building
rather than talking to customers — which is the wrong way round at stage 0.

| Month | Planned PLN | Real PLN | Planned h | Real h | Share of hours with customers |
| --: | --: | --: | --: | --: | --: |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

The last column is the one to watch. At stage 0, at least a third of startup hours should be spent with people in
your target professions.

---

## 7. Pitfalls

**B16 · No stop condition.**
*Symptom:* "I'll know when it's not working." *Why it hurts:* you won't — sunk cost makes every month feel like the
one before success. *Remedy:* a written stop condition with a date, set before stage 0 begins.

**B17 · Changing the tax form for the startup too early.**
*Symptom:* switching to flat tax to deduct a PLN 13,000 box. *Why it hurts:* on your contract revenue, ryczałt is
better unless startup costs exceed about PLN 110,000 a year. *Remedy:* the table in §2.2, recomputed by your
accountant.

**B18 · Mixed revenue records.**
*Symptom:* pilot invoices and bank invoices in one revenue column. *Why it hurts:* the highest ryczałt rate may apply to
everything (art. 12(3)). *Remedy:* separate categories before the first startup invoice.

**B19 · Missing the PKD 2025 deadline.**
*Symptom:* nothing done by 31 Dec 2026. *Remedy:* update the codes now and add the startup activity in the same step.

**B20 · The buffer spent on the startup.**
*Symptom:* "just this once" — a box bought from the safety buffer. *Remedy:* separate accounts for the three pots;
the buffer account has no card.

---

## 8. Checkpoint

- [ ] `founder/04-budget.md` with three pots, three stages, caps, gates and a stop condition with a date.
- [ ] Separate bank accounts (or sub-accounts) for the buffer and the startup.
- [ ] The accountant meeting is booked; the question list is written.
- [ ] The PKD 2025 update is done or scheduled before 31 Dec 2026.
- [ ] The 2027 tax-form deadline is in your calendar.

Sources for this part: [SOURCES.md](SOURCES.md), section "Part 04".
