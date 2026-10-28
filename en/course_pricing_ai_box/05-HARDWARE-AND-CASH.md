# Part 05 · Hardware and cash: who owns the box?

> **Goal of this part.** You choose how the hardware reaches the office — the customer buys it, you
> resell it, a leasing company finances it, or you rent it out — and you compute what each choice does to
> **your cash**, to **the customer's taxes** and to **how an investor reads your revenue**.
>
> **Time:** ~4 h · **Level:** ⭐⭐⭐⭐ · **Produces:** `pricing/05-hardware.md` · **Tool:**
> `tools/pricing_model.py cash`

> **Not tax or legal advice.** The tax rules below are summarised from public sources as of 25 Oct 2026.
> The customer's accountant decides how they book the box; your accountant decides how you do.

---

## 0. The problem

A box costs PLN 9,000–23,000 net (part 02). Somebody has to pay for it on day one. If that is you, every new
customer costs you a box before they pay you anything, and **the faster you grow, the more cash you need** —
the classic way small hardware companies die while their sales look great. If it is the customer, a
PLN 15,000 purchase may need a partner meeting, and the sale slows down.

There is no free option. There are four options with different costs, and the choice is a pricing decision
because it changes what the customer sees on the invoice.

---

## 1. The four models

| | **A. Customer buys** | **B. You resell** | **C. Leasing** | **D. Rent (hardware-as-a-service)** |
| :-- | :-- | :-- | :-- | :-- |
| Who owns the box | customer | customer | leasing company → customer after buyout | **you** |
| Who pays on day one | customer, to a shop | you pay the shop; customer pays your invoice | leasing company pays you | **you** |
| Customer sees | a shop invoice + your setup + subscription | your invoice for the box + subscription | a lease instalment + your subscription | **one monthly fee** |
| Your cash need | none | the box until the customer pays | none (paid on delivery) | **the box, recovered over 24–36 months** |
| Warranty and swaps | the shop | **you** | the shop / you | **you** |
| Your revenue | setup + subscription | + low-margin hardware revenue | setup + subscription (+ hardware sale to the lessor) | all recurring |
| Best for | price-sensitive, tax-savvy offices | nobody, usually | most small offices | fast sales, investor story — if you have capital |

### 1.1 A — the customer buys

You publish a short list of approved boxes (part 02, the hardware table) and the customer buys one from a
shop. You install it. Cleanest for you: no capital, no warranty, no hardware revenue that dilutes your
margin. The friction is the purchase itself, and the risk that they buy the wrong model. Mitigate it by
naming two exact models and checking the order before they place it.

### 1.2 B — you resell

You buy the box and put it on your invoice. This **looks** like extra revenue and is usually a trap:

- you pay the shop at once and the customer pays you after the payment term (up to 60 days between
  businesses — section 4);
- the warranty, the courier and the broken unit become your problem;
- the hardware revenue has a thin margin and makes your gross margin look worse (part 08).

Resell only when the customer insists on one invoice, and price the box at shop price plus a margin that
pays for the warranty handling.

### 1.3 C — leasing through a partner

A leasing company buys the box (from you or from the shop) and the customer pays it monthly. You are paid
on delivery. What the research found (25 Oct 2026; details in [SOURCES.md](SOURCES.md)):

| Fact | Source |
| :-- | :-- |
| EFL: leasing from PLN 1,000 net, up to 36 months, 0–45% down payment, **new equipment only** | EFL product page |
| Online leasing from PLN 500; traditional leasing usually from PLN 4,500 | Leason (broker overview), Feb 2026 |
| IT equipment is usually leased for **16–36 months**, buyout from 1% | Leason |
| Online leasing (Leaselink) can finance used equipment up to PLN 250,000 net without a valuation | Leason |
| Rental of laptops: Netland365, PLN 99 net per device per month, 24-month terms | Netland365 |
| A device-as-a-service offer for **AI servers** in Poland | **not found** — a gap, or a sign the market does not exist yet |

For the customer, an **operating lease** instalment is a tax-deductible cost when (summary of the research,
check with an accountant):

- the lease lasts at least **40% of the normative depreciation period** — for computers (KŚT group 4,
  item 487, 30% a year) that is about **16 months**; and
- the sum of instalments is at least the initial value of the asset.

**Practical step:** before your first sale, ask two leasing companies whether they will finance *your*
configured box (a PC plus your installed software) as one asset, and at what minimum value. Some will lease
the hardware but not the software or services, so your setup fee and subscription stay separate invoices.

### 1.4 D — rent (hardware-as-a-service)

You own the box and charge one monthly fee that includes it. For the customer this is the easiest
purchase: no capital expense, one number, "it is your problem if it breaks". It is also the model of
Lemony AI: USD 499 per month for the box, updates and support, up to 5 users (TechCrunch, June 2025).

For investors it is attractive: Silicon Valley Bank's (now First Citizens) *State of HaaS* 2024 report
found a **median revenue multiple 59% higher** for hardware-as-a-service companies than for other frontier-tech
models, with a typical system paying back in about **15 months** (*report data*).

For you it is the most capital-hungry model by far (section 2). Do it only when you know where the money
for the boxes comes from (section 3).

---

## 2. Run the cash model

```bash
python3 pricing_model.py cash                          # 2 new offices a month, 36 months
python3 pricing_model.py cash --payment-days 60        # customers pay late
python3 pricing_model.py cash --hardware 21950         # a GX10 / DGX Spark class box
```

Defaults (all assumptions — replace them): hardware PLN 10,967 net, 10% hardware markup, setup PLN 6,000,
subscription PLN 1,500 per month, support cost PLN 500 per office per month, 1% monthly churn, **fixed
costs PLN 15,000 per month** (development, sales, tools, your pay), rent recovers the box over 36 months.

The results I got:

| Scenario | A. customer buys | B. resell | C. lease | D. rent |
| :-- | --: | --: | --: | --: |
| Lowest cash, 2 offices/month, 14-day payment term | −1,000 | 0 | 0 | **−107,396** (month 9) |
| Lowest cash, 2 offices/month, **60-day** payment term | −1,000 | **−43,888** (month 2) | 0 | −107,396 |
| Lowest cash, **5** offices/month | 0 | 0 | 0 | −101,137 (month 6) |
| Lowest cash, **GX10-class box** (PLN 21,950) | −1,000 | 0 | 0 | **−320,651** (month 15) |
| Cash after 36 months, base case | 1,080,982 | 1,159,944 | 1,159,944 | 689,789 |

How to read it:

- **"Lowest cash" is the money you must already have**, or borrow, to survive the model. Rent needs about
  PLN 100,000 for a small box and over PLN 300,000 for a GX10-class box at two offices a month.
- **The rent model ends with less cash after 36 months** but owns the boxes (a residual value the model
  does not count) and the most predictable revenue. It is a trade of cash now for quality of revenue later.
- **Reselling with long payment terms** quietly turns you into a bank for your customers.
- In models A–C, the **setup fee is what keeps you alive early**: with two new offices a month, setup fees
  pay most of the fixed costs before the subscription base is large. Do not give setup away.

---

## 3. Where the money for rent boxes would come from

If you choose rent, you need capital before you need customers. The options, in order of cost:

1. **Your current income.** Example: a contractor billing PLN 1,500–2,000 net per day. A month of that income
   buys roughly two or three small boxes. Decide in advance how much of it you can put at risk
   without touching your safety buffer.
2. **Leasing the boxes to yourself** and renting them on. Check the leasing contract: many forbid
   subletting without the lessor's consent. Ask for that consent in writing.
3. **Customer prepayment.** A year of subscription paid up front (part 04, section 6) pays for the box.
   Offer the annual-prepay discount only together with the rent model.
4. **Investors.** Hardware is the classic reason a capital-light software company needs money. Part 08 covers
   when that makes sense.

**My recommendation:** start with **C (leasing) and A (customer buys)** side by side; offer **D (rent)**
only to customers who prepay a year, until you have capital or investors. Keep **B** for the rare customer
who insists on a single invoice.

---

## 4. Payment terms and late payment

From the Act on preventing excessive delays in commercial transactions (Dz.U. 2023 poz. 1790), as
summarised in the research:

| Rule | Value |
| :-- | :-- |
| Maximum payment term between businesses | **60 days**, unless expressly agreed otherwise and not grossly unfair to the creditor (art. 7(2)) |
| Large enterprise paying an SME | hard maximum of 60 days (art. 7(2a)) |
| Public entities | 30 days |
| Statutory late-payment interest | NBP reference rate + 10 percentage points: **13.75%** a year from 1 Jul to 31 Dec 2026 (M.P. 2026 poz. 642) |
| Flat recovery compensation | EUR 40 (claims up to PLN 5,000), EUR 70 (PLN 5,000–50,000), EUR 100 (PLN 50,000+) |

**Write a 14-day payment term into your price book** (part 07). Small offices pay their software monthly;
14 days is normal for them and keeps you out of the "bank for customers" row in the table above.

---

## 5. The customer's tax view — why the model changes the price they feel

The same PLN 13,000 box feels different depending on how the customer can book it. From the research (check
with an accountant):

| Situation for the customer | What they can do |
| :-- | :-- |
| Asset up to **PLN 10,000 net** | expense it at once |
| Computer above PLN 10,000 | depreciate at **30% a year** (KŚT 487) — or use a one-off write-off below |
| **New** fixed assets in KŚT groups 3–6 and 8 | one-off write-off up to **PLN 100,000 a year** |
| Small taxpayers and start-ups | de minimis one-off depreciation up to **EUR 50,000** (PLN 213,000 in 2026) |
| Operating lease, ≥ 16 months for computers | instalments are a cost as they are paid |

And VAT:

- An office that is an active VAT payer recovers the 23% VAT on the box and on your subscription. For
  them, your net price is the real price.
- An office that **cannot** recover VAT pays 23% more for everything you sell. Medical services are
  generally VAT-exempt, so a private clinic usually cannot recover VAT on the box; a small office using
  the VAT exemption for small businesses cannot either. Legal advisory services, as I understand the VAT Act,
  cannot use that small-business exemption (art. 113(13)), so most law offices are active VAT payers —
  **verify this with an accountant before you rely on it in a sales conversation.**

**For pricing this means:** quote net to law offices and tax advisers; for clinics and small exempt offices,
show the gross price too, because that is the number they will feel.

---

## 6. EXERCISE 05 — choose and justify

In `pricing/05-hardware.md`:

1. Run the cash model with **your** numbers from parts 02–04.
2. Fill the table of section 2 for your scenario.
3. Choose the model(s) you will offer first, and write the condition under which you would add rent.
4. Write the exact two box models you will support at the start, with net prices and a "price valid until"
   date.
5. Write the questions for the leasing companies (section 1.3, "practical step").

---

## 7. ⭐ FIELD EXPERIMENT 05 — will a leasing company finance the box?

**Hypothesis.** At least one of two leasing companies will finance a PLN 11,000–22,000 net configured box
for a small law office, over 24–36 months, without asking for the software to be leased with it.

**Procedure.** Contact two leasing companies (one traditional, one online). Describe the deal as it will
really be: a mini PC bought from a named shop or from you, installed by you, for a law office with two
years of history. Ask: minimum value, term, down payment, monthly instalment, whether used or reconditioned
units are possible, whether a vendor programme exists (they pay you on delivery), and what documents the
office needs.

**Prediction (mine).** Both will finance the hardware. Neither will finance the software or setup. The
monthly instalment for an PLN 11,000 net box over 36 months will be roughly PLN 350–400 net.

| Company | Min. value | Term | Down payment | Instalment (net) | Finances software? | Vendor programme? |
| :-- | --: | :-- | --: | --: | :-- | :-- |
| | | | | | | |
| | | | | | | |

---

## 8. Pitfalls

**B52 · Growing faster than your cash.**
*Symptom:* the rent model, more customers than planned, and an empty bank account in month 9. *Remedy:* run
`cash` before you choose rent, and set a maximum number of rent boxes per month that your capital allows.

**B53 · Hardware revenue presented as growth.**
*Symptom:* "Revenue PLN 400,000" of which PLN 300,000 is resold boxes. *Why it hurts:* investors and your
own decisions look at recurring revenue and gross margin (part 08). *Remedy:* report hardware revenue
separately, always.

**B54 · A hardware price with no validity date.**
*Symptom:* a quote from March honoured in October after a 17% price increase (the DGX Spark example from
part 02). *Remedy:* every hardware price says "valid until".

**B55 · Ignoring the customer's VAT position.**
*Symptom:* a clinic is surprised by a 23% higher price. *Remedy:* ask "do you recover VAT?" in the first
meeting; show gross prices where they do not.

**B56 · Subletting leased boxes without the lessor's consent.**
*Symptom:* rent model financed by leasing, no clause allowing it. *Remedy:* written consent first.

---

## 9. Checkpoint

- [ ] `pricing/05-hardware.md` has the cash table for your numbers.
- [ ] You have chosen the hardware model(s) for the first year, with a written condition for adding rent.
- [ ] Two supported box models with net prices and validity dates.
- [ ] Field experiment 05: at least one leasing company has answered.
- [ ] You can explain to Office K, in two sentences, how they can book the box for tax.

Sources for this part: [SOURCES.md](SOURCES.md), section "Part 05".
