# Part 07 · The price book: prices, discounts and terms on paper

> **Goal of this part.** You turn parts 02–06 into one written document — the **price book** — that any
> conversation, proposal and contract can point to. It holds the prices, what each includes, the discount
> rules, the payment and indexation terms, and the margins for partners. Once it exists, you stop inventing
> prices in meetings.
>
> **Time:** ~4 h · **Level:** ⭐⭐⭐ · **Produces:** `pricing/price-book-v1.md`

> **Not legal advice.** The sample clauses below show *what* a clause must achieve. Have a lawyer write the
> final contract text — the contracts course covers that.

---

## 0. The problem

Without a price book, every price is negotiated from zero, every discount is a mood, and after ten customers
you have ten different deals that you cannot remember, defend or raise. The price book is to pricing what
the release manifest is to deployment in `course_agentic_apps/18-RELEASE-AND-MAINTENANCE.md`: a versioned
record of the current truth, so that decisions are deliberate and changes can be traced.

---

## 1. What goes into the price book

```
 price-book-v1.md
 ├─ 1. Packages          prices, what is included, who it is for
 ├─ 2. Expert agents     catalogue with prices per agent
 ├─ 3. One-off fees      setup, pilot, extra training, on-site visit
 ├─ 4. Hardware          supported boxes, the four models (part 05), "valid until"
 ├─ 5. Support scope     what is included, what is not, response times
 ├─ 6. Commercial terms  contract length, billing, payment term, indexation, notice
 ├─ 7. Discount policy   who may get what, for what in return, and the maximum
 ├─ 8. Partner terms     referral and resale margins
 └─ 9. Change log        version, date, what changed, why
```

---

## 2. An example price book for the law-office segment

The numbers below are **an illustration** that is consistent with the course's example calculations. They
are not a recommendation. Replace every number with the results of your own parts 02–06, and keep a line
saying where each number came from.

Why these numbers (the chain of reasoning, so you can redo it with yours):

- Floor with installation paid by the setup fee, 20 offices, 60% margin (`pricing_model.py floor
  --install-h 0`): **PLN 833** per month at 0.5 h support, **PLN 1,083** at 1 h.
- Office K's 20%-capture price against cloud legal AI (part 03): **PLN 1,804**.
- The illustrative Van Westendorp range from part 06's sample: roughly PLN 600–1,600, IPP near PLN 1,000.
  (Your real range replaces this.)

### 2.1 Packages (PLN net per month, 12-month contract)

| | **Start** | **Office** ⭐ | **Office Pro** |
| :-- | --: | --: | --: |
| Monthly fee | **1,190** | **1,790** | **3,290** |
| Users included | 3 | 10 | 25 |
| Expert agents included | 1 | 3 | 6 |
| Support | e-mail, next business day | phone, same business day | phone, 4 business hours, quarterly review |
| Compliance pack (§ 23e note, processing agreement, DPIA template, audit-log export) | basic | full | full + annual review |
| Extra user | 59 | 49 | 39 |
| Extra agent | 490 | 390 | 290 |
| Setup fee (one-off) | 3,900 | 6,900 | 11,900 |

Checks against the earlier parts:

- **Start** is just above the floor at 0.5 h of support. It exists so that small offices can say yes and to
  make **Office** look like the sensible choice. It is not where you make money.
- **Office** sits at the 20%-capture price for Office K. It is the package you want 50%+ of customers on.
- **Pro** roughly doubles Office for 2.5× the users and twice the agents — the "best" anchor that makes
  Office look reasonable, and the home of the 10%+ of customers who need more.

### 2.2 Expert agents (law offices)

| Agent | Type (part 04) | Price as an extra |
| :-- | :-- | :-- |
| Incoming court letter triage (summary, deadline proposal, next step) | leader | package price above |
| Contract comparison against the office template | leader | package price above |
| Case-file chronology from scanned documents | filler | package price above |
| Translation of documents (PL ↔ EN/DE) | filler | package price above |
| Cloud escalation of anonymised text for hard questions | **killer candidate** | **not offered in packages**; separate signed add-on |

### 2.3 One-off fees

| Item | Price (PLN net) | Note |
| :-- | --: | :-- |
| Paid pilot, 6–8 weeks, one leader agent | 4,000 | **credited to the setup fee** if signed within 30 days of the end |
| Extra training session (remote, 1 h) | 400 | |
| On-site visit outside the setup | 900 + travel | after the first year |
| Archive indexing above 50,000 pages | quoted | measured in the pilot |

### 2.4 Hardware (prices valid until 31 Dec 2026)

| Box | Model A: you buy it from a shop | Model C: leasing | Model D: rent (only with annual prepayment) |
| :-- | :-- | :-- | :-- |
| Minisforum MS-S1 MAX 128 GB | ~PLN 10,967 net (Ceneo, 25 Oct 2026) | via partner | + PLN 390 per month |
| ASUS Ascent GX10 128 GB | ~PLN 21,950 net | via partner | + PLN 750 per month |

---

## 3. The support scope — the price of saying no

Support is your largest cost line (part 02). The scope protects it:

| Included | Not included (billed at the hourly rate or declined) |
| :-- | :-- |
| the box, its software, models and agents | the office's printers, network, PCs, e-mail |
| model and security updates, monitoring, backups of the box | data recovery from the office's own devices |
| questions about using the agents | writing new agents for one office (that is a catalogue request) |
| one remote session per incident | on-site visits after setup (price in 2.3) |

Write the response times **in business hours** and the support channel. Then keep a log of every support
hour from the first pilot (pitfall B41). After six months, the log tells you whether your floor was right.

---

## 4. Commercial terms

### 4.1 Contract length, billing, payment

- **12 months**, renewing for another 12 unless cancelled with **3 months' notice**.
- Billed **monthly in advance**, payment term **14 days** (the legal maximum between businesses is 60 days —
  part 05, section 4; you do not want to be anywhere near it).
- **Annual prepayment: two months free** (≈ 16.7% discount — inside the 20% rule of section 5).

### 4.2 Indexation

Prices that cannot rise will fall in real terms. Polish inflation (GUS): **3.6%** average in 2025; in 2026
year-on-year between 2.1% (January) and 4.1% (September); service prices rose 5.7% year-on-year in May 2026.
A two-year contract without indexation loses 6–8% of its real value.

What the clause must achieve (wording for your lawyer):

> *EN:* Once a year, at renewal, the monthly fees change by the average annual consumer price index for the
> previous calendar year published by GUS (Statistics Poland). The fee does not decrease. We notify the
> customer of the new fees at least 30 days before they apply.
>
> *PL:* Raz w roku, przy odnowieniu umowy, opłaty miesięczne zmieniają się o średnioroczny wskaźnik cen
> towarów i usług konsumpcyjnych za poprzedni rok kalendarzowy ogłoszony przez Prezesa GUS. Opłaty nie ulegają
> obniżeniu. O nowych opłatach informujemy klienta co najmniej 30 dni przed ich zastosowaniem.

### 4.3 Price changes beyond indexation

- New prices apply to **new** customers at once.
- Existing customers keep their price until the next renewal and get **at least 60 days' notice**.
- Launch-partner prices (section 5) are written with an end date from day one.

---

## 5. The discount policy

Patrick Campbell's ProfitWell data: discount size is **"almost perfectly correlated" with churn**; his
rule is never to discount more than about 20% (*vendor self-reported*). A discounted customer has told you
the product is worth less than your price — and behaves accordingly.

The rule for your price book: **every discount buys something specific, has a maximum, and has an end.**

| Discount | What you get in return | Maximum | Ends |
| :-- | :-- | :-- | :-- |
| Annual prepayment | cash for boxes (part 05) | 2 months (~17%) | — |
| **Launch partner** (first 5 offices) | a written case study, a reference call per quarter, their measured hours (part 03) | 20% of the monthly fee | after 12 months, written in the contract |
| Pilot fee credited | they sign within 30 days of the pilot end | the pilot fee | 30 days after the pilot |
| Multi-office (same owner, 3+ locations) | one decision, several boxes | 15% | — |
| **Not allowed** | "they are small", "they asked", "the end of the month" | 0% | — |

Anything outside this table is a change to the price book, with a version number and a reason — not a
favour in a meeting.

---

## 6. Partner terms

The repo's challenge of the box idea concludes: *"partner with [IT service firms] as the AI layer, revenue
share"*. Partners need to know what they earn before they will introduce you. Two common structures — I did
**not** find Polish market data on margins for this kind of product, so the percentages are **assumptions to
test** with the first two partners:

| Structure | What the partner does | What they earn (assumption) |
| :-- | :-- | :-- |
| **Referral** | introduces the office; you sell and serve | 10–15% of the first year's subscription |
| **Resale** | sells, invoices, does first-line support; you do updates and second line | 20–30% discount on your list price, ongoing |

Whatever you pay a partner comes out of your gross margin, not the customer's price. Run the floor (part 02)
again with the partner margin as an extra cost line before you sign.

---

## 7. How to present the price to a lawyer

- **Net, per month, per office.** Lawyers compare with LEX (PLN 298–722 per month) and with cloud seats (PLN
  590 per user per month for Beck-Noxtua). Show yours in the same unit.
- **Lead with the package, not the hardware.** The box is an annex.
- **Put the comparison in the proposal**: what the office pays today, what the alternative costs, what the
  measured hours are worth (part 03). The economic value is your argument; the price is the conclusion.
- **Name the risk once, calmly**: the § 23e question *"which tools did you use?"* and the audit log that
  answers it. Then stop (pitfall B44 in part 03).
- **Publish Start and Office** on your website; Pro "on request". Small offices trust a vendor that shows its
  prices, and you skip a meeting with those who cannot afford it.

---

## 8. EXERCISE 07 — write `price-book-v1.md`

Use the nine sections of section 1. For every number, add a column *source*: *part 02 calculation*, *part 03
value*, *part 06 interviews (n = …)*, *pilot*, or *assumption*. Version it as `v1`, with today's date and a
change log. From now on, every proposal says *"according to price book v1"*.

---

## 9. ⭐ FIELD EXPERIMENT 07 — does the price book survive a real proposal?

**Hypothesis.** Sent to three offices that reached level 3 in part 06, a proposal based strictly on the price
book (no improvised discounts) gets at least one "yes" or a request for a specific change you can map to a
row of the discount table.

**Procedure.** Write three proposals using only the price book. Send them. Record each reply verbatim (in
your private notes). For every objection, note whether the price book had an answer.

**Prediction (mine).** No objection about the Office price itself; one objection about the setup fee; one
request to start with Start and move up later.

| Office (code) | Package offered | Reply | Objection | Price book had an answer? | Change to v2? |
| :-- | :-- | :-- | :-- | :-- | :-- |
| | | | | | |

---

## 10. Pitfalls

**B62 · The improvised discount.**
*Symptom:* "OK, 25% off because you are the first." *Remedy:* the launch-partner row: 20%, a case study in
return, an end date.

**B63 · No indexation clause.**
*Symptom:* the 2026 price still applies in 2029. *Remedy:* the GUS CPI clause, from the first contract.

**B64 · A support scope only in your head.**
*Symptom:* the office calls about the printer. *Remedy:* section 3 of the price book, attached to the contract.

**B65 · Prices without a version.**
*Symptom:* you cannot tell which customer has which price and why. *Remedy:* the change log, and the price
book version written into every contract.

**B66 · Partner margin from the customer's pocket.**
*Symptom:* the partner adds 25% on top of your list price and the office finds your website price.
*Remedy:* one public list price; the partner's margin comes from your side.

---

## 11. Checkpoint

- [ ] `price-book-v1.md` exists with all nine sections and a source for every number.
- [ ] The discount table has a maximum and a "not allowed" row.
- [ ] The indexation and notice clauses are ready for your lawyer (PL and EN).
- [ ] Field experiment 07: at least one proposal sent strictly from the price book.

Sources for this part: [SOURCES.md](SOURCES.md), section "Part 07".
