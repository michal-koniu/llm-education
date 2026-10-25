# Part 01 · Pricing foundations: three numbers, not one

> **Goal of this part.** You stop thinking about "the price" as one number you guess. You learn the
> three numbers every price sits between — **the cost floor, the reference value and the economic value**
> — and the order in which this course will measure them for the private AI box.
>
> **Time:** ~3 h · **Level:** ⭐⭐ · **Produces:** `pricing/00-gut-price.md`, `pricing/01-anchors.md`

---

## 0. The problem

The repo already contains a price for the box. In `ai-business-asymmetries/02-OPPORTUNITIES.md` it says:
*"25,000-60,000 PLN setup including hardware, 800-2,500 PLN per month … (my assumption, to be tested,
not market data)."* That is an honest sentence, and also the typical engineer's price: a range wide
enough to be safe (a factor of 2.4 on setup, 3.1 on the subscription) and derived from what the
hardware costs plus "something for my time".

There are three problems with a price made like that:

1. **It starts from your cost.** The customer does not know or care what the box cost you. They compare
   your price with what they would do otherwise and with what the box is worth to them.
2. **It is one number for everyone.** A 2-person notary office and a 10-person law firm get very
   different value from the same box.
3. **It cannot be falsified.** "800-2,500" survives any interview. A price you cannot prove wrong
   teaches you nothing.

This course replaces the guess with three measured numbers and one tested decision.

---

## 1. Why price deserves a whole course

Price is the strongest lever on profit that you control, and the one engineers spend the least time on.

| Study | Change of 1% in… | Effect on profit | Source |
| :-- | :-- | :-- | :-- |
| Marn & Rosiello, HBR 1992 (large companies) | price | **+11.1%** operating profit | primary (HBR) |
| | sales volume | +3.3% | |
| ProfitWell / Paddle, 512 SaaS companies | monetisation (pricing) | **+12.7%** bottom line | *vendor self-reported* |
| | retention | +6.7% | |
| | acquisition | +3.3% | |

The mechanism is simple arithmetic. If your margin is thin, a small price change is a large share of
the profit. If you sell a box with 20% gross margin, raising the price by 5% raises your gross profit by 25%.

**For you this means:** an hour spent on pricing before the first sale is worth more than an hour spent on a
fourth agent. That is not an opinion about business; it is the ratio in the table.

---

## 2. The three numbers

Every price sits between a floor and a ceiling.

```
 PLN / month per office
   │
   │   ┌──────────────────────────────┐  ← ECONOMIC VALUE (ceiling)
   │   │  differentiation value        │     what the box is worth to THIS office:
   │   │  (time saved, risk removed,   │     alternative + what is better about yours
   │   │   things the alternative       │
   │   │   cannot do)                   │
   │   ├──────────────────────────────┤  ← REFERENCE VALUE
   │   │  next-best alternative         │     what they would pay instead
   │   │  (Beck-Noxtua seats, Copilot,  │     (or the cost of doing it by hand)
   │   │   a trainee's hours)           │
   │   └──────────────────────────────┘
   │          ↕ your price lives somewhere here
   │   ════════════════════════════════  ← COST FLOOR
   │                                        your cost to serve one office ÷ (1 − target margin)
   └────────────────────────────────────
```

### 2.1 The cost floor — part 02

Your cost to serve one office for one month: support hours, model updates, monitoring, hardware if you
own it. Divide by `(1 − target gross margin)` and you get the lowest price at which the business
works. **Below the floor you lose money on every customer. Above it you are only choosing how much of the
value you take.**

The floor is the number engineers compute well. The trap is to stop there and add a markup.

### 2.2 The reference value — part 03

What the office would pay for the **next-best alternative**. Nagle & Müller (*The Strategy and Tactics of
Pricing*, 6th ed., 2018) call this the reference value. For your buyer it can be:

- cloud legal AI per seat (the repo's anchors: Beck-Noxtua PLN 590 net per user per month, LEX AI tiers
  PLN 49–489 per month, checked 11 Oct 2026 in `ai-assistants/02-MARKET.md`);
- a general assistant: Microsoft 365 Copilot USD 30 per user per month; Copilot Business for up to 300
  users USD 21 list from 1 Dec 2025 (Computerworld), USD 18 promotional until 31 Dec 2026 (secondary
  sources); ChatGPT Business USD 20–25 and Claude Team USD 20–25 per standard seat;
- **doing it by hand** — the hours of a trainee or an assistant. For many small offices this is the true
  alternative, because the cloud tools fail the professional-secrecy test.

### 2.3 The economic value — part 03

Reference value **plus differentiation value**: what is better (or worse — it can be negative) about your
box compared with that alternative. For the box the positive differentiation is concrete:

- data never leaves the room (secrecy, GDPR, no CLOUD Act exposure — the argument in
  `ai-assistants/04-POLAND-AND-SOVEREIGNTY.md`);
- no per-seat meter, no token limit;
- Polish workflows on the office's own files;
- an audit log the office can show its bar chamber or a client.

Negative differentiation also exists and you must subtract it: hardware in the office, a smaller model than
the cloud frontier, a one-person vendor (you), installation effort.

**The economic value is the ceiling.** No rational buyer pays more than the alternative plus the net
advantage. A price a customer says yes to without long hesitation usually captures **a fraction** of the
differentiation value — you leave the rest to them as the reason to switch. Part 03 computes this fraction
with `tools/pricing_model.py value`.

---

## 3. Price is a product decision, not a sales decision

Madhavan Ramanujam and Georg Tacke (*Monetizing Innovation*, Wiley, 2016; both of Simon-Kucher) argues that most new products fail
on monetisation, and that the fix is to **design the product around the price** — to have the
willingness-to-pay conversation *before* you build. His four failure modes map directly onto the box:

| Failure mode | What it means | How it looks for the AI box |
| :-- | :-- | :-- |
| **Feature shock** | too many features, nobody understands the value, price feels too high | a box with 15 agents, a chatbot, OCR, a calendar and a RAG over everything — the lawyer sees "an IT project" |
| **Minivation** | the right product priced too low; money left on the table | the box sold at the price of hardware plus a bit, because "they are small offices" |
| **Hidden gem** | a valuable feature nobody sells because you did not see its value | the **audit log and secrecy compliance package** — possibly worth more to a bar-regulated office than the agents themselves |
| **Undead** | a product nobody wants at any price | "a server with a chatbot" — the generic box the repo itself already rejected |

Two more of his tools appear later in this course:

- **Leader / filler / killer** feature split (part 04): *leaders* drive the purchase, *fillers* are nice
  extras, *killers* are wanted by under 20% of buyers and actively disliked by over 20% — they must never be
  forced into a package.
- **Good / better / best** packaging targets (part 04): under 30% of buyers on Good, over 70% on Better or
  Best, over 10% on Best. More than half the buyers on the entry tier is a warning sign that the entry tier
  is too good or the upper tiers too weak.

---

## 4. What the AI box actually sells

Before you price, name the **job** the office pays for. The repo's own cost analysis
(`ai-business-asymmetries/03-LOCAL-FIRST.md`, section 4) gives the honest answer: *"against cheap API models,
local hardware does not break even on tokens at small-office volumes … price the box as compliance and
control, not as a saving."*

So the box does **not** sell tokens, compute or "AI". It sells three things:

1. **Permission** — the office can use AI on client files at all, without breaching secrecy. Without the
   box, the alternative for that work is often "no AI".
2. **Hours back** — specific workflows (incoming letter triage, contract comparison, deadline proposals)
   done in minutes instead of an hour.
3. **Peace of mind** — someone else keeps it updated, measured and patched, and there is a log.

Each of these suggests a different way of charging (part 04): permission suggests a flat fee per office,
hours back suggest pricing per workflow or per expert agent, peace of mind suggests a maintenance
subscription. Your package will combine them.

---

## 5. How AI products charge in 2025–2026

The market moved fast. What you need from it is not a fashion to copy, but a sense of what buyers are
already used to and what went wrong.

| Model | Example (with source) | What it teaches you |
| :-- | :-- | :-- |
| **Per seat** | Microsoft 365 Copilot USD 30/user/month; Copilot Business USD 21 list (from 1 Dec 2025, Computerworld), USD 18 promotional to end of 2026. Clio publishes EasyStart at USD 49/user/month and bundles AI into higher tiers | Buyers understand it. It punishes you when AI replaces seats, and a 3-person office is a small sale |
| **Usage / credits** | Salesforce Agentforce: USD 2 per conversation → Flex Credits USD 500 per 100k credits (about USD 0.10 per action) → per-user add-ons USD 125/month (Salesforce pricing page) | Even Salesforce changed the meter three times. Small buyers cannot budget a meter |
| **Usage backlash** | Cursor, 16 Jun 2025: Pro moved to a usage pool; the company apologised and refunded charges for 16 Jun–4 Jul (Cursor blog). Replit's effort-based pricing: users reported ~USD 1,000 in a week vs ~USD 200 a month before (The Register, 18 Sep 2025) | **Unpredictable bills destroy trust faster than high prices** |
| **Per outcome** | Intercom Fin USD 0.99 per resolution, minimum 50 per month (Intercom pricing page). Sierra charges for completed outcomes and reported USD 100M ARR in Nov 2025 (*self-reported*) | Works when the outcome is narrow and measurable |
| **Counterpoint** | Decagon says "the vast majority" of its customers chose per-conversation over per-resolution, for predictability (*self-reported*) | Even when outcome pricing is offered, buyers often prefer what they can forecast |
| **Hardware + subscription** | Lemony AI: USD 499/month covering the box, updates and support, up to 5 users; USD 2M seed (TechCrunch, Jun 2025) | **The closest analogue to your product.** About PLN 1,900 per month at an assumed 3.8 PLN/USD |

**Surveys** (all self-reported by the companies that answered):

- Growth Unhinged 2025 (240+ companies): hybrid pricing (a base fee plus usage) rose from 27% to 41% as the
  primary model; per-seat fell from 21% to 15%; outcome-based is primary for 5%, and 25% expect it to be by 2028.
- Growth Unhinged 2026 (230+ companies, 13 May 2026): hybrid 37% as the primary model (a different sample,
  not directly comparable); 29% use AI credits; investors say they prefer hybrid (35%) over outcome (26%),
  usage (24%), flat (10%) and seat (5%).
- ICONIQ *State of AI* 2026 (~300 executives): consumption pricing 35% → 42%, outcome pricing 18% → 23%.

**What this means for the box (my opinion, to be tested in part 06):** your buyers are small offices that
budget per month and fear surprises. Start with a **flat, predictable fee per office plus priced add-ons**
(the expert agents). Keep outcome pricing for later, for one narrow workflow you can measure reliably.
That is a "hybrid" in the surveys' sense, but with the variable part chosen by the customer (which agents
they add), not by a meter.

---

## 6. The order of this course

```
 02 cost floor ─────► the lowest price that keeps the business alive
 03 value ceiling ──► what it is worth to Office K, and the reference value
 04 value metric ───► what you charge FOR: office, agent, seat, outcome; good/better/best
 05 hardware ───────► who owns the box, and how much cash you need
 06 willingness ────► measure, do not guess: conversations, Van Westendorp, paid pilots
 07 price book ─────► the written price list, discounts, contract terms
 08 scale ──────────► how this pricing looks to an investor and as you add agents
```

**The running example.** Through the whole course you price the box for **Office K**: a fictional law
firm in a regional Polish city, five people — two advocates (adwokaci), one trainee (aplikant) and two
assistants. Replace Office K with a real office as soon as you have interviewed one.

---

## 7. EXERCISE 01 — pre-register your gut price

Before you learn anything else, write down what you would charge today. You will compare it with the
measured price at the end of the course. This is the business version of the course rule *"a prediction
before every experiment"*.

Create `pricing/00-gut-price.md`, **outside the public repo** (it will hold customer information later):

```markdown
# Gut price — written <date>, before part 02

Setup fee (one-off):          ____ PLN net
Hardware (who pays, how):     ____
Monthly fee per office:       ____ PLN net
What is included:             ____
Why this number (one line):   ____
Confidence (0–100%):          ____
```

Then create `pricing/01-anchors.md` with three empty sections — *Cost floor*, *Reference value*,
*Economic value* — that parts 02 and 03 will fill in.

---

## 8. ⭐ FIELD EXPERIMENT 01 — what do they pay for software today?

**Hypothesis.** A small Polish law office already spends at least PLN 500 net per month on software
(legal database, case management, office suite) and thinks of software as a monthly cost, not a purchase.

**Procedure.** Ask three people who work in or run small professional offices (your network is enough —
this is not a sales call). Ask only about the past, never about your product:

1. *"Which programs does your office pay for every month or every year?"*
2. *"Roughly how much is that per month, all together?"*
3. *"Who decided to buy the last one, and how long did it take?"*

**Prediction (mine).** Two of three spend PLN 500–1,500 per month in total; the legal database (LEX or
Legalis) is the largest item; the decision was made by the senior partner alone, within weeks.

| Office | People | Programs paid | PLN / month total | Largest item | Who decided | How long |
| :-- | --: | :-- | --: | :-- | :-- | :-- |
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

**When the result differs from my prediction, your measurement wins** — correct `01-anchors.md`, not the
data.

---

## 9. Pitfalls

**B31 · Cost-plus pricing for a value product.**
*Symptom:* the price is "hardware + 20% + my hours". *Why it hurts:* it ignores the reference value and
caps you at a services margin. *Remedy:* compute the floor, then forget it until you have the ceiling.

**B32 · Pricing the technology instead of the job.**
*Symptom:* the price list mentions tokens, model sizes or GPU memory. *Remedy:* price permission, hours
back and peace of mind (section 4). Technical specs go in an annex.

**B33 · Copying a US price with an exchange rate.**
*Symptom:* "Lemony charges USD 499, so PLN 1,900." *Why it hurts:* different buyer, different alternative,
different wage level. *Remedy:* use foreign prices only as one reference point next to Polish ones.

**B34 · Deciding the price after building the product.**
*Symptom:* the box has ten features and you are now wondering what to charge. *Remedy:* the
willingness-to-pay conversation (part 06) happens before you build the second workflow.

**B35 · A range instead of a price.**
*Symptom:* "800–2,500 per month". *Why it hurts:* a range cannot be falsified, so it teaches you nothing.
*Remedy:* one price per package, with a written condition under which you will change it.

**B36 · Customer data in a public repository.**
*Symptom:* interview notes committed next to the course files. *Remedy:* `pricing/` lives outside any
public repo, and you never write a client's name in a file that goes to GitHub.

---

## 10. Checkpoint

Do not start part 02 until all of these are true:

- [ ] `pricing/00-gut-price.md` exists, with a single number per line and a confidence.
- [ ] `pricing/01-anchors.md` exists with the three empty sections.
- [ ] You can explain, without notes, the difference between reference value and economic value.
- [ ] Field experiment 01 has at least one filled row (three is the target).
- [ ] You can name the three things the box sells (section 4) in one sentence each.

Sources for this part: [SOURCES.md](SOURCES.md), section "Part 01".
