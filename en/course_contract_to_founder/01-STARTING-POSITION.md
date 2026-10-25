# Part 01 · Your starting position: what the contract really gives you

> **Goal of this part.** You write down, in numbers, what you are starting with — money, time, skills,
> contacts — and what you could lose. You discover that your most valuable asset is not a skill or an idea,
> but the contract itself, and you decide to protect it while you build.
>
> **Time:** ~3 h + a 2-week log · **Level:** ⭐⭐ · **Produces:** `founder/01-position.md`,
> `founder/01-time-log.csv`

> **Not legal, tax or financial advice.** Numbers and rules as of 25 Oct 2026. Your accountant and your
> lawyer decide your case.

---

## 0. The problem

Most advice for first-time founders assumes one of two people: an employee who must "take the leap", or a
student with nothing to lose. You are neither. You run a sole-trader business (JDG) and invoice a bank
**PLN 1,700 net per day** on a B2B contract, and you told me the actual work takes **about one hour a day**.

That is an unusual and very strong position — if you handle it well. It is also easy to damage: by building
the startup in a way that breaches the contract, by mixing the two activities in your tax records, or by
quitting too early because "real founders go all in". This course is about using the position, not
escaping it.

---

## 1. Money: what the contract pays you

### 1.1 Revenue

At 21 billed days a month on average (a B2B contract usually pays no holidays — check yours):

```
 1,700 PLN × 21 days = 35,700 PLN net (excl. VAT) per month
 35,700 × 12         = 428,400 PLN a year
```

### 1.2 What stays with you

The money that reaches your private account depends on your tax form. I computed the three forms for a JDG
with PLN 428,400 of revenue in 2026, full ZUS social contributions (PLN 1,926.76 a month, including the
voluntary sickness insurance), and — for the two forms that allow costs — business costs of 2% of revenue.
The rules and rates are from the research for this course ([SOURCES.md](SOURCES.md), part 04):

| | **Ryczałt 12%** (IT services) | **Flat tax 19%** (liniowy) | **Tax scale 12/32%** (skala) |
| :-- | --: | --: | --: |
| Social contributions (ZUS), year | 23,121 | 23,121 | 23,121 |
| Health contribution, year | 17,940 (tier above PLN 300k: 1,495.04/month) | 19,439 (4.9%) | 35,704 (9%) |
| Income tax, year | 47,557 | 72,696 | 99,348 |
| Business costs, year | — (not deductible) | 8,568 | 8,568 |
| **Net to you, year** | **≈ 339,800** | **≈ 304,600** | **≈ 261,700** |
| **Net to you, month** | **≈ 28,300** | **≈ 25,400** | **≈ 21,800** |

This is a simplified model: no other income, no joint filing, and none of the reliefs that need a closer look.
Use it to understand the order of magnitude, then put your accountant's real figures into
`founder/01-position.md`.

**What it means:** on ryczałt the contract leaves you roughly **PLN 28,000 a month**. Whatever your living
costs are, the difference is money that can fund the startup — the subject of part 04.

### 1.3 Your effective hourly rate

If the contract really needs about an hour a day, you earn about **PLN 1,700 per hour of work**. Keep this
number in mind every time you are tempted to do something for the startup that someone else could do for
PLN 150 an hour. It also means: **almost nothing you can do in year one of the startup will earn you more per
hour than the contract.** That is why the contract is worth protecting.

---

## 2. Time: the hours that are actually yours

"One hour of work a day" and "seven free hours a day" are not the same thing. What matters is what the
contract says about **availability**:

| If the contract says… | Then your free time is… |
| :-- | :-- |
| you deliver results, no working hours, no availability window | genuinely yours, any time of day |
| you are available during business hours (e.g. 9:00–17:00) to respond within N minutes | **interruptible** — fine for coding and thinking, risky for client meetings |
| you are paid per day "of work" with daily reporting, and a "day" is defined (e.g. 8 hours) | **not clearly yours** — doing other paid work during reported hours may breach the contract |

Part 02 audits these clauses. Until then, assume the third row and keep startup work outside the hours you
bill. This matters especially because **your future customers work 9:00–17:00**: lawyers take meetings during
the day, exactly when the bank may expect you to be available. Part 05 deals with that conflict.

There is a second reason to be careful with time. Since **8 July 2026**, labour inspectors can decide by an
administrative decision that a B2B contract is really an employment relationship (part 02). Work under the
client's direction, at a time and place the client sets, is the core test of employment (art. 22 § 1 of the
Labour Code). How your days are organised is evidence, either way.

---

## 3. Skills: what you already have

You are not starting from zero. Be specific — this list goes into every conversation with a co-founder, a
partner or an investor:

| Asset | Evidence |
| :-- | :-- |
| Building agents that run for weeks, are measured and cannot do harm | two courses in `llm-education` (~150 h), built and tested on your own rig |
| Local inference at production quality on AMD hardware | `speeding-up-generation/` (DeepSeek from 23.5 to ~50 tok/s), `local-llm-runtimes/` |
| DevOps: deployment, monitoring, security, release and rollback | your profession; `course_agentic_apps/15–18` |
| Market research with a scoring method | `ai-business-asymmetries/`, `ai-income-asymmetries/`, `ai-assistants/` |
| Public proof of competence | a public repository others can read — a sales and hiring asset |

And the gaps — the reason for this business track: selling, pricing, contracts, finance, and **domain knowledge
of the professions you want to sell to**. The repo itself says so: *"most others need a domain partner on day
one"* (`ai-business-asymmetries/README.md`).

---

## 4. Contacts and reputation

Write down three groups, with names in your private file only:

1. **People in your target professions** you could ask for 30 minutes: lawyers, notaries, tax advisers,
   accountants — friends, family, your own accountant.
2. **People who sell to them**: IT service firms that run small offices, your accountant's software vendor.
3. **People who have built a company**: anyone who has hired, raised money or sold one.

A pricing course and a customer-discovery course both start by asking you for ten conversations. This list is
where they come from.

---

## 5. What you can lose

| Risk | How it happens | Likelihood if you are careless |
| :-- | :-- | :-- |
| **Losing the contract** | the client ends it after learning about a side business it did not expect, or because the startup visibly takes your attention | medium |
| **A breach-of-contract claim** | the startup uses something the contract assigns to the client (IP, confidential information), or competes where a non-compete forbids it; contractual penalties apply even without damage | low to medium — part 02 |
| **Reclassification** | a labour inspector decides the B2B contract is employment; the IP and non-compete rules of the Labour Code then apply from that date | low, but new since July 2026 — part 02 |
| **Tax mess** | startup revenue and costs mixed into the contract JDG on the wrong ryczałt rate, or startup costs that ryczałt does not let you deduct | medium — part 04 |
| **IP that investors will not accept** | product code written on the client's laptop, during billed hours, or with no clear owner | medium — part 03 |
| **Burnout** | contract + startup + life, for two years | high for most founders — part 05 |

Every risk in this table is cheap to prevent now and expensive to fix later. That is the whole argument of
parts 02–05.

---

## 6. EXERCISE 01 — the position sheet

Create `founder/01-position.md` in a **private** folder (not the public repo):

```markdown
# Starting position — <date>

## Money
Contract revenue per month (net):        ____ PLN
Tax form 2026:                           ____
Net to me per month (accountant's data): ____ PLN
My living costs per month:               ____ PLN
Savings today (liquid):                  ____ PLN
Surplus per month (net − living costs):  ____ PLN

## Time
Contract: required hours / availability window / reporting:  ____
Hours per week I can give the startup without touching contract hours: ____

## Contract (to be filled in part 02)
Notice period: ____   IP clause: ____   Non-compete: ____   Penalties: ____

## Skills (with evidence) / Gaps
...

## Contacts (codes only here, names in a separate private file)
Professions: __   Sellers to them: __   Founders: __
```

---

## 7. ⭐ FIELD EXPERIMENT 01 — where do your hours really go?

**Hypothesis.** Over two working weeks, the contract takes fewer than 10 hours a week of real work, but its
availability requirements fragment the working day so that fewer than 15 hours a week are usable for deep
startup work during business hours.

**Procedure.** For ten working days, log every block of 30 minutes or more in `founder/01-time-log.csv`:

```csv
date,start,end,category,energy_1to5,note
2026-11-03,09:00,09:40,contract,3,standup + review
2026-11-03,10:00,12:30,startup-deep,4,eval set for letter triage
```

Categories: `contract`, `contract-standby` (available but not working), `startup-deep`, `startup-shallow`
(e-mail, admin), `life`.

**Prediction (mine).** Contract 6–10 h a week. Contract standby takes most of 9:00–17:00. Startup deep work
happens mainly before 9:00 and after 17:00, 10–15 h a week, with higher energy in the morning.

| Week | Contract h | Standby h | Startup deep h | Startup shallow h | Best block (time of day) |
| :-- | --: | --: | --: | --: | :-- |
| 1 | | | | | |
| 2 | | | | | |

The result tells you how much startup you can realistically run before changing anything in the contract.

---

## 8. Pitfalls

**B1 · Treating the contract as a temporary inconvenience.**
*Symptom:* "I'll just keep it until the startup takes off," with no care for how it is performed. *Why it
hurts:* at about PLN 1,700 per hour of work, it is the best-paid hour you have and the funding of the startup.
*Remedy:* protect it deliberately (parts 02–03).

**B2 · Counting "free" hours that are not free.**
*Symptom:* the plan assumes seven startup hours a day because the contract work takes one. *Remedy:* read
the availability clause, and run field experiment 01.

**B3 · No written number for living costs.**
*Symptom:* "I earn plenty, I can fund it." *Why it hurts:* without a number, you cannot set a risk budget
(part 04) or a quit condition (part 06). *Remedy:* three months of real spending, written down.

**B4 · Skills described as adjectives.**
*Symptom:* "strong technical background". *Remedy:* every skill with a piece of evidence someone can look
at (section 3).

**B5 · A public file with private information.**
*Symptom:* `founder/` committed to the public `llm-education` repo. *Remedy:* a separate private folder or
repository, from the first file.

---

## 9. Checkpoint

- [ ] `founder/01-position.md` exists, with your accountant's real net figure (not my model).
- [ ] You know your monthly surplus in PLN.
- [ ] Field experiment 01 is running (or done): ten days of time log.
- [ ] You have listed at least five people in your target professions you could ask for 30 minutes.
- [ ] You can say in one sentence why the contract is your most valuable asset right now.

Sources for this part: [SOURCES.md](SOURCES.md), sections "Part 01" and "Part 04".
