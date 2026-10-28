# Part 08 · Pricing for scale: how the price looks to an investor

> **Goal of this part.** You see your pricing the way an investor — or an acquirer — sees it: not as a
> price per office, but as the **quality of the revenue** it produces. You learn the four numbers that
> decide that quality, and you plan how the price will change as the agent catalogue grows. You decide
> what to optimise depending on whether you bootstrap or raise money.
>
> **Time:** ~4 h · **Level:** ⭐⭐⭐⭐ · **Produces:** `pricing/08-scale.md` · **Tool:**
> `tools/pricing_model.py nrr`

---

## 0. The problem

Two companies each have PLN 2 million of revenue. One sold 150 boxes with a small margin and installation
fees. The other has 90 offices paying a subscription that grows every year as they add agents. An investor
will value the second at several times the first — even though the revenue is the same. If you want a
company that scales, the price list is not only how you earn money this year: it decides what the company
is worth.

---

## 1. Not all revenue is equal

| Kind of revenue | Repeats? | Margin | How investors treat it |
| :-- | :-- | :-- | :-- |
| **Subscription** (platform fee + agents) | ✅ monthly | high, rising with scale (part 02) | the core: annual recurring revenue (**ARR**) = monthly recurring × 12 |
| **Setup and pilot fees** | ❌ once | medium (labour) | useful cash, low value |
| **Resold hardware** | ❌ once | thin | close to zero value; can hurt, because it lowers the blended margin |
| **Rented hardware** (inside the subscription) | ✅ | medium | recurring, but capital-heavy; see the HaaS data below |

Valuation data (all self-reported or advisory data; check the dates):

| Data point | Value | Source |
| :-- | :-- | :-- |
| Private SaaS companies, valuation multiple | **4.8× ARR** bootstrapped, **5.3× ARR** equity-backed | SaaS Capital, Jan 2025 (no 2026 update found) |
| SaaS M&A median EV/revenue | 3.8× (2025), 3.1× (Q1 2026) | Aventis Advisors |
| M&A, 2015 to mid-2025, EV/revenue | software **3.0×**, hardware **1.4×**, IT services **1.3×** | Aventis Advisors |
| Hardware-as-a-service companies vs other frontier tech | median revenue multiple **59% higher**; typical payback ~15 months | SVB / First Citizens, *State of HaaS* 2024 |

Read the third row with your product in mind: the same złoty of revenue is worth roughly **twice as much**
if a buyer sees it as software than if they see it as hardware or IT services. Your price list decides which
one it looks like.

---

## 2. The four numbers

### 2.1 Annual recurring revenue (ARR)

Only the subscription counts. Report setup and hardware separately (pitfall B53 in part 05).

### 2.2 Gross margin

From part 02. Reference points: public SaaS median ~77% (PitchBook); AI products 45% in 2025, 53% expected
in 2026 (ICONIQ, *self-reported*); AI companies' median target ~50% (Growth Unhinged 2026). A SaaStr essay
argues that most SaaS metrics "only work" at 75%+ gross margin and 100%+ net revenue retention. For your box:
**55–65% in year 1–2, 70%+ as agents are added** is the plan from part 02.

### 2.3 Gross revenue retention (GRR)

The share of last year's recurring revenue you keep, counting only losses (offices leaving, downgrades).
Benchmarks: median GRR about **91%** for private B2B SaaS below USD 250k annual contract value (SaaS Capital
2025); Benchmarkit reports a fall from 88% to 84% in 2026 (*secondary*). For very small businesses, monthly
churn of **3–7%** is commonly cited (*secondary sources*), and SaaStr notes that businesses with very small
customers often churn 3%+ a month.

That last number is a threat to you: 3% a month is a third of your customers gone in a year. Professional
offices on 12-month contracts, with your box holding their indexed archive, should churn far less — but that
is a hypothesis. Measure it from the first cohort.

### 2.4 Net revenue retention (NRR)

The share of last year's recurring revenue that the **same** customers pay you this year, including what they
**added**. Above 100% means the business grows even if you sign no new customer.

Benchmarks: median NRR **101%** (Benchmarkit 2025); **102%** for contracts of USD 25–50k a year, rising with
contract size (SaaS Capital 2025); around 98% for the smallest contracts (read from a chart — uncertain).
Small-business SaaS is often below 100%.

**This is where your strategy lives.** The agent catalogue (part 04) is an NRR machine: every agent added to an
existing office is revenue without a new sale.

---

## 3. Run it: what does NRR depend on?

```bash
python3 pricing_model.py nrr                                  # base case
python3 pricing_model.py nrr --churn 0.03 --expansion 0.03    # small-business churn
python3 pricing_model.py nrr --churn 0.005 --expansion 0.06   # sticky offices, strong catalogue
```

One cohort of 100 offices on the *Office* package (PLN 1,790), 12 months, agents at PLN 390, indexation
3.6% at renewal (the 2025 GUS CPI):

| Monthly churn | Offices adding one agent per month | GRR | **NRR** |
| --: | --: | --: | --: |
| 1.0% | 0% (no catalogue), no indexation | 89% | **89%** |
| 3.0% | 3% | 69% | **78%** |
| 1.0% | 3% | 89% | **99%** |
| 1.0% | 6% | 89% | **106%** |
| 0.5% | 6% | 94% | **113%** |

Three lessons:

1. **Without new agents, you shrink.** Even with low churn, a box with a fixed set of features loses 11% of its
   revenue a year. Indexation alone does not save it.
2. **Churn beats expansion.** At small-business churn (3% a month), even a good catalogue cannot hold NRR at
   100%. Your first job is to make the box hard to leave: the indexed archive, the audit log, the measured
   hours, the relationship.
3. **A catalogue that ships an agent worth adding every month or two turns the business into a compounding
   one.** 6% of offices adding an agent each month is about 70% of offices adding one a year — plausible only
   if new agents are genuinely useful. That is a product commitment, not a pricing trick.

---

## 4. How the price should change as you grow

| Stage | What the price does | Why |
| :-- | :-- | :-- |
| **Pilots (0–5 offices)** | paid pilot; launch-partner price (−20%, ends after 12 months) | buys proof: case studies, measured hours |
| **First cohort (5–30)** | price book v1; no improvised discounts | measures real churn and real expansion |
| **Catalogue (30–100)** | new agents priced on their own measured value; packages re-cut so that Office includes the most-bought agents | keeps Office the obvious choice as the catalogue grows |
| **Proof of value (100+)** | raise list prices for new customers; consider **outcome pricing for one narrow agent** whose result you can count (an accepted letter summary, a filed document) | outcome pricing works for narrow, measurable jobs (Intercom Fin, USD 0.99 per resolution) — and many buyers still prefer predictability (Decagon) |

On raising prices: Marn & Rosiello's 1% → 11.1% profit result (part 01) applies most to a business that has
stopped selling on price. Your first price increase is a sign of strength, not of greed — if your NRR and
case studies support it.

---

## 5. Bootstrapping or venture: what to optimise

You said you can start with or without venture funding. The pricing priorities differ:

| | **Bootstrapped** | **Venture-funded** |
| :-- | :-- | :-- |
| The scarce resource | cash | time (growth speed) |
| Optimise | setup fees, annual prepayment, models A/C for hardware (part 05) | ARR growth, NRR, gross margin; rent (model D) becomes possible with investors' capital |
| Accept | slower growth | burning cash, more dilution if growth is slow |
| The price list should show | profitable from office one | a revenue model that compounds (catalogue, NRR > 100%) |
| The investor's question | — | *"Why does this become a software company and not an IT services company?"* — answer it with gross margin and NRR |

What investors say they prefer: in Growth Unhinged's 2026 survey, investors chose **hybrid** pricing (35%),
then outcome (26%), usage (24%), flat (10%) and seat (5%) (*self-reported*). Your platform fee plus a
catalogue of agents is a hybrid in the sense investors mean: a base fee plus a variable part that grows with
use.

For the Polish context of venture funding, check what pre-seed funds expect, the PFR Starter programme, and
whether your current contracts or employment allow you to raise while keeping them.

---

## 6. EXERCISE 08 — the scale plan

In `pricing/08-scale.md`:

1. Write your **ARR target** for month 12 and month 36, and how many offices × which package that means.
2. Run `nrr` with your assumptions. Write the churn and expansion rates you need for NRR ≥ 100%.
3. List the agents you would need to ship to reach that expansion rate — with a month for each.
4. Choose: *bootstrapped* or *venture*, for the next 12 months. Write the one pricing decision that follows
   from it (e.g. "rent only with annual prepayment").
5. Write the conditions for your first list-price increase.

---

## 7. ⭐ FIELD EXPERIMENT 08 — the first cohort, measured

**Hypothesis.** Over the first 6 months, the first cohort of paying offices (≥ 5) has monthly churn below 1%,
and at least one office in five adds an agent without being asked twice.

**Procedure.** From the first paying office on, keep `pricing/cohort.csv`: month, office code, package, agents,
monthly fee, cancelled (yes/no). Every month compute the cohort's revenue against month 0. At month 6, run
`nrr` with the measured monthly churn and expansion, and compare with your plan.

**Prediction (mine).** Churn 0 in the first six months (12-month contracts), and one or two offices adding an
agent — **only** if a new agent was actually shipped in those months.

| Month | Offices | MRR (PLN) | Agents added | Cancelled | Cohort revenue vs month 0 |
| --: | --: | --: | --: | --: | --: |
| 0 | | | — | — | 100% |
| 3 | | | | | |
| 6 | | | | | |

---

## 8. Pitfalls

**B67 · Total revenue instead of ARR.**
*Symptom:* "we did PLN 1.2M this year", most of it hardware and setup. *Remedy:* report ARR, gross margin and
hardware separately, always.

**B68 · Growth by discount.**
*Symptom:* new offices signed at −30% to hit a number. *Why it hurts:* discounts correlate with churn (part 07),
so the NRR you need falls. *Remedy:* the discount table, nothing else.

**B69 · A catalogue that stops.**
*Symptom:* the last agent shipped eight months ago. *Remedy:* NRR depends on it (section 3). Plan agents
like releases, with dates.

**B70 · Outcome pricing too early.**
*Symptom:* "PLN 5 per processed letter" before you can count reliably what a processed letter is. *Remedy:*
outcome pricing only for one narrow agent, after months of measured results — and only if customers ask.

---

## 9. Checkpoint — and the end of the course

- [ ] `pricing/08-scale.md` with ARR targets, the NRR calculation and the agent plan.
- [ ] A decision for the next 12 months: bootstrapped or venture, and the pricing rule that follows.
- [ ] `pricing/cohort.csv` exists, even if empty.
- [ ] **Open `pricing/00-gut-price.md` from part 01.** Compare your gut price with `price-book-v1.md`. Write
      one paragraph: what changed, and which part changed it most.

That last comparison is the grade for this course — the same idea as the repeated measurement at the end of
`course_agentic_apps/19-CAPSTONE.md`. If your price book is identical to your gut price, either your gut was
very good, or the course taught you nothing. Your measurements decide which.

Sources for this part: [SOURCES.md](SOURCES.md), section "Part 08".
