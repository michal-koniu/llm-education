# Course: Pricing a private AI box — index

**Created 25 October 2026. For Michał.**
Part of the business track: the first course is
[From a B2B contract to a founder](../course_contract_to_founder/00-INDEX.md). This one assumes you have read
`ai-business-asymmetries/` (opportunity 1, *Private AI box for Polish professional offices*) and
`ai-assistants/02-MARKET.md`.

> **Purpose of the whole thing.** After this course you have a **price book** for the private AI box —
> packages, expert-agent prices, setup fees, hardware options, discounts and terms — where every number
> has a source: a calculation, a measurement or a conversation with a buyer. And you know how that price
> list turns into a company that grows by adding agents, not by adding boxes.

> **Not tax, legal or investment advice.** Prices, rules and market data change monthly. Facts are as of
> 25 Oct 2026; check again before acting.

---

## The thesis the whole course stands on

> **The box does not sell tokens. It sells permission, hours back and peace of mind — so it must be priced
> on value, not on hardware.**

The repo's own cost analysis already showed that a local box does not beat a cheap API on token cost
(`ai-business-asymmetries/03-LOCAL-FIRST.md`). That is not a weakness of the business; it is a statement about
what to charge for. If you price the box as hardware, you compete with Ceneo. If you price it as a solution for
secrecy and time, you compete with the office's alternatives — and the agent catalogue becomes the product.

⭐ **In part 03 you will test this thesis with numbers.** The result is less comfortable than the thesis: it
works for some offices and not others — which tells you who to sell to first.

---

## The path

```
  BLOCK I · THE THREE NUMBERS ─────────────────────── ~11 h
   01 foundations           floor, reference value, economic value; how AI is priced in 2026
   02 cost floor       ⭐   what one office costs you — support hours decide it, not hardware
   03 value ceiling   ⭐⭐  what the box is worth to Office K — and the targeting result
              │
  BLOCK II · THE OFFER ────────────────────────────── ~8 h
   04 value metric    ⭐⭐  per office + expert agents; good/better/best; the catalogue as engine
   05 hardware              customer buys / resell / lease / rent — and your cash
              │
  BLOCK III · PROOF AND PAPER ─────────────────────── ~10 h + weeks of conversations
   06 willingness     ⭐⭐  the ladder of evidence, Van Westendorp and Gabor-Granger in Polish, paid pilots
   07 price book            prices, discounts, indexation, support scope, partners
              │
   08 SCALE ───────────────► ARR, gross margin, NRR; bootstrapped vs venture; the grade for the course
```

⚠️ **Do not skip to part 07.** A price book written before parts 02, 03 and 06 is the gut price from part 01
with formatting.

---

## Files

| # | File | Level | What you will learn | Time |
| :-- | :-- | :-- | :-- | :-- |
| 01 | `01-PRICING-FOUNDATIONS.md` | ⭐⭐ | the three numbers; Ramanujam's failure modes; seat vs usage vs outcome pricing in 2025–2026 | ~3 h |
| 02 | `02-COST-FLOOR.md` | ⭐⭐⭐ | COGS vs OpEx, gross margin, **why support hours decide your floor** | ~4 h |
| 03 | `03-VALUE-CEILING.md` | ⭐⭐⭐ | Economic Value Estimation for a law office; § 23e; **the alternative decides everything** | ~4 h |
| 04 | `04-VALUE-METRIC-AND-PACKAGING.md` | ⭐⭐⭐⭐ | the value metric, the **expert-agent catalogue**, leader/filler/killer, good/better/best | ~4 h |
| 05 | `05-HARDWARE-AND-CASH.md` | ⭐⭐⭐⭐ | four hardware models, **your cash need**, leasing, the customer's tax and VAT view | ~4 h |
| 06 | `06-WILLINGNESS-TO-PAY.md` | ⭐⭐⭐⭐ | the ladder of evidence, **pricing questions in Polish**, paid pilots, small-sample honesty | ~6 h + weeks |
| 07 | `07-PRICE-BOOK-AND-TERMS.md` | ⭐⭐⭐ | the written price book, discount policy, CPI indexation, support scope, partner margins | ~4 h |
| 08 | `08-PRICING-FOR-SCALE-AND-INVESTORS.md` | ⭐⭐⭐⭐ | ARR, gross margin, **NRR from the agent catalogue**, valuation multiples, bootstrapped vs venture | ~4 h |
| — | `tools/pricing_model.py` | — | the calculator: `floor`, `value`, `cash`, `vw`, `gg`, `nrr` (Python standard library only) | — |
| — | `SOURCES.md` | — | every number with its source, date and label; **the weakest points listed first** | — |

**Total: ~33 hours at the desk, plus 2–4 weeks of conversations with offices.** Like the technical courses,
this is not a course to read. Most of the value is in the field experiments.

---

## The anatomy of every part

The same skeleton as the technical courses, translated to business:

```
0. Problem — why this question matters for the box
1-N. Theory — with a source for every number
   ⭐ "How others do it" — real companies and their prices
YOUR NUMBERS — the calculator, run with your assumptions
EXERCISE — produces a file in your pricing/ folder
⭐ FIELD EXPERIMENT — hypothesis, procedure, a table TO FILL IN, my prediction
Pitfalls — numbered B31–B70, with the symptom and the remedy
Checkpoint — what MUST exist before the next part
```

⭐ **The field experiment is the heart of each part.** Each has a **prediction** — what I expect you to find —
and an empty table. **When they differ, your measurement wins, and you fix the course.** A conversation with
one real office beats every number in this course.

---

## The rules I keep throughout the course

1. **Net prices, always.** All amounts are PLN net, excluding VAT, unless a column says *gross* (B38).
2. **Every number has a label:** *measured*, *researched (source)* or *assumed*. An unlabelled number is a
   guess pretending to be a fact.
3. **One price, not a range.** A range cannot be proven wrong (B35).
4. **Ask about the past, not the future.** People describe what they did honestly and what they would do
   optimistically (B57).
5. **Money is the only proof.** Words < commitment < money < renewal (part 06).
6. **Your working folder `pricing/` lives outside any public repo.** It will contain information about real
   offices (B36).
7. **Pitfalls are numbered across the business track:** B1–B30 in the founder course, **B31–B70 here**.

---

## The running example: Office K

A fictional law office in a mid-size Polish city: **two advocates, one trainee, two assistants**. It pays for a
legal database, some of its lawyers already paste things into ChatGPT, and the senior partner worries about
§ 23e. Every calculation in the course is done for Office K first. Replace it with a real office as soon as you
have interviewed one.

---

## Registry of pitfalls — B31–B70

| ID | Pitfall | Part |
| :-- | :-- | --: |
| B31 | Cost-plus pricing for a value product | 01 |
| B32 | Pricing the technology instead of the job | 01 |
| B33 | Copying a US price with an exchange rate | 01 |
| B34 | Deciding the price after building the product | 01 |
| B35 | A range instead of a price | 01 |
| B36 | Customer data in a public repository | 01 |
| B37 | Your own time priced at zero | 02 |
| B38 | Gross and net prices mixed | 02 |
| B39 | Development counted as COGS | 02 |
| B40 | Pricing from the floor of month one | 02 |
| B41 | Support creep | 02 |
| B42 | Value computed against the wrong alternative | 03 |
| B43 | Realisation assumed to be 100% | 03 |
| B44 | "The only legal option" claims | 03 |
| B45 | Risk value in the price | 03 |
| B46 | One price for all professions | 03 |
| B47 | Per-seat pricing for a box whose cost does not depend on seats | 04 |
| B48 | A meter on a small buyer | 04 |
| B49 | The free agent | 04 |
| B50 | Killers inside a package | 04 |
| B51 | Packages designed by features, not by buyers | 04 |
| B52 | Growing faster than your cash | 05 |
| B53 | Hardware revenue presented as growth | 05 |
| B54 | A hardware price with no validity date | 05 |
| B55 | Ignoring the customer's VAT position | 05 |
| B56 | Subletting leased boxes without the lessor's consent | 05 |
| B57 | "Would you buy this?" | 06 |
| B58 | Pitching before listening | 06 |
| B59 | Friends and family as the sample | 06 |
| B60 | A survey number read as a fact | 06 |
| B61 | The free pilot | 06 |
| B62 | The improvised discount | 07 |
| B63 | No indexation clause | 07 |
| B64 | A support scope only in your head | 07 |
| B65 | Prices without a version | 07 |
| B66 | Partner margin from the customer's pocket | 07 |
| B67 | Total revenue instead of ARR | 08 |
| B68 | Growth by discount | 08 |
| B69 | A catalogue that stops | 08 |
| B70 | Outcome pricing too early | 08 |

---

## What this course does not contain — and why

| What is missing | Why |
| :-- | :-- |
| **Customer discovery in depth** | Part 06 covers the pricing conversation. A full course on finding and interviewing buyers is planned separately (course 2 in the proposal) |
| **Contract law** | Part 07 says what clauses must achieve; the wording belongs to a lawyer and to the planned contracts course |
| **Your own taxes** | How *your* company books the revenue is in the founder course, part 04, and the planned legal-form course |
| **A financial model of the whole company** | The calculator covers per-office economics and cash for hardware; the full 36-month model is the planned finance course |

---

## Before you start

```bash
cd tools
python3 --version                       # expect >= 3.12
python3 pricing_model.py --help         # six subcommands
python3 pricing_model.py floor          # the defaults from part 02
mkdir -p ~/founder/pricing              # your private working folder — NOT in the public repo
```
