# Part 06 · Willingness to pay: measure it, do not guess it

> **Goal of this part.** You measure what your target offices will pay — first in words, then with a
> commitment, then with money. You run a structured pricing conversation with the Van Westendorp and
> Gabor-Granger questions in Polish, and you design a paid pilot that tells you more than any survey.
>
> **Time:** ~6 h plus 2–4 weeks of conversations · **Level:** ⭐⭐⭐⭐ · **Produces:**
> `pricing/06-interviews/`, `pricing/06-wtp.md` · **Tools:** `pricing_model.py vw`, `pricing_model.py gg`

---

## 0. The problem

Parts 02–05 gave you a floor, a ceiling and a structure. Everything between them is still your opinion.
The only people who know what Office K will pay are the people who run offices like Office K. Ask them —
but ask in a way that does not produce polite lies.

---

## 1. The ladder of evidence

Not all answers are equal. From weakest to strongest:

```
  5  RENEWAL            they paid, used it, and paid again          ← the only proof
  4  MONEY              a paid pilot, a deposit, a signed order
  3  COMMITMENT         a letter of intent, a meeting with the partner, their documents for a test
  2  STATED PRICE       answers to pricing questions (this part's surveys)
  1  OPINION            "interesting", "we would definitely use it"  ← worthless for pricing
```

Every step up costs the customer something — time, reputation, money — and that cost is what makes the
answer true. **Design every conversation to move at least one step up.** A conversation that ends at
level 1 was a pleasant chat, not research.

---

## 2. The conversation, before the questions

Madhavan Ramanujam (*Monetizing Innovation*) insists on talking about willingness to pay **before** you build
— and on doing it as a conversation about value, not as "how much would you pay?". The order that works:

1. **Their work, in the past tense.** *"Tell me about the last court letter that arrived. What did you do
   with it? How long did it take?"* (No product yet.)
2. **Their current spending.** *"What do you pay for software today? Who decided?"* (Field experiment 01.)
3. **The problem's weight.** *"If this took five minutes instead of twenty, what would you do with the
   time?"* — this is your *realisation* number from part 03.
4. **The concept, briefly.** One paragraph and, if you have it, a two-minute demo on public documents.
5. **The pricing questions** (sections 3–4).
6. **The ask** — a step up the ladder: *"Would you give me ten anonymised letters to test on?"*, *"Can we
   show this to your partner next week?"*, *"Would you start a paid pilot in January?"*

Never pitch before step 4. Once you pitch, they stop telling you about their work and start being polite
about your product.

---

## 3. Van Westendorp: four questions

The Price Sensitivity Meter (Peter van Westendorp, ESOMAR Congress, 1976). Ask the four questions about **one
specific package** described in one paragraph — for example, the *Office* package of part 04 with a monthly
price and a separate setup fee. Ask about the monthly price.

| Code | English | Polski (do rozmowy) |
| :-- | :-- | :-- |
| `too_cheap` | At what monthly price would it be so cheap that you would doubt its quality? | Przy jakiej miesięcznej cenie byłoby to tak tanie, że zaczął(-ęła)by Pan/Pani wątpić w jakość? |
| `cheap` | At what monthly price would it be a bargain — a good buy for the money? | Przy jakiej cenie uznał(a)by Pan/Pani, że to okazja — dobry zakup za te pieniądze? |
| `expensive` | At what monthly price would it start to feel expensive, but you would still consider it? | Przy jakiej cenie zaczęłoby to być drogie, ale nadal brał(a)by to Pan/Pani pod uwagę? |
| `too_expensive` | At what monthly price would it be so expensive that you would not consider it at all? | Przy jakiej cenie byłoby to tak drogie, że w ogóle nie brał(a)by Pan/Pani tego pod uwagę? |

Record the answers as a CSV, one row per person, PLN net per month:

```csv
too_cheap,cheap,expensive,too_expensive
300,600,1200,2000
500,800,1500,2500
```

Then:

```bash
python3 pricing_model.py vw pricing/06-interviews/vw.csv
```

### 3.1 How the tool reads the curves

From the four answers it builds four cumulative curves and finds four crossings:

| Point | Crossing (the convention this tool uses) | Meaning |
| :-- | :-- | :-- |
| **PMC** — point of marginal cheapness | "too cheap" × "not cheap" (1 − cheap) | below it, too many people doubt the quality |
| **OPP** — optimal price point | "too cheap" × "too expensive" | as many reject it for being too cheap as for being too expensive |
| **IPP** — indifference price point | "cheap" × "expensive" | as many call it a bargain as call it expensive — often read as the "normal" price |
| **PME** — point of marginal expensiveness | "too expensive" × "not expensive" (1 − expensive) | above it, too many reject it |

⚠️ Practitioners and vendor tools use **slightly different conventions**, especially for PMC, PME and OPP
(some cross "too cheap" with "expensive" instead of with "not cheap"). Only IPP is defined the same way
almost everywhere. Always state which convention you used, and compare results only within one convention.

**Acceptable range: PMC to PME.** If your differentiation is clear (part 03), price in the upper half of
the range, above IPP.

### 3.2 Sample size — your honest limit

Vendor guidance for Van Westendorp: **at least 30** respondents for the chart to mean anything, **100–200**
recommended (at least 100 per segment); Qualtrics uses 300. You will have **10–20** conversations. So:

- use the four questions as a **structured conversation**, not as a survey;
- read the result as a **direction** ("our range is roughly 900–1,600, not 300–600"), never as a number;
- the tool prints a warning below n = 30 for exactly this reason.

The basic method also does **not** estimate how many will buy at a price. For that you need the next
section — and, better, money (section 5).

---

## 4. Gabor-Granger: yes or no at a price

The Gabor-Granger method (André Gabor and Clive Granger, 1960s) asks a purchase question at a sequence of
prices and builds a demand curve. In a conversation:

> *"If the Office package cost PLN 1,200 net a month, would you take it?"* — yes → ask at a higher price; no →
> ask at a lower price. Stop at the first change of answer.
>
> *„Gdyby pakiet Office kosztował 1 200 zł netto miesięcznie, zdecydował(a)by się Pan/Pani?"*

Use four prices spread across your Van Westendorp range. **Start at a random one** for each person (or
start high), so that the first price does not anchor everyone.

Collect the share of "yes" at each price across all conversations and run:

```bash
python3 pricing_model.py gg 900:0.70 1200:0.55 1500:0.35 1800:0.20 --cost 570
```

The tool shows revenue and **gross profit** per prospect at each price, using your COGS from part 02, and
picks the price that maximises gross profit among those tested. Stated intent **overstates** real buying —
treat the shares as an upper bound and compare prices with each other, not with reality.

---

## 5. Money: the paid pilot

The strongest evidence you can get before launch. The repo's opportunity profile already suggests it: *"paid
pilot 3,000–5,000 PLN, then setup + monthly"*. Design it so that it tests the **price**, not only the
product.

| Element | Recommendation |
| :-- | :-- |
| **Duration** | 6–8 weeks — long enough for the office to stop being polite and start using it |
| **Price** | paid, never free. PLN 3,000–5,000 net is the repo's starting hypothesis |
| **Scope** | one leader agent (part 04), on the office's own documents, on your box or theirs |
| **Success criteria — written before the start** | e.g. "≥ 8 minutes saved per letter on ≥ 30 letters, ≤ 1 in 5 outputs needing a real correction" |
| **Conversion clause** | the pilot fee is **credited towards the setup fee** if they sign within 30 days of the end |
| **The price after the pilot** | **written in the pilot agreement**. A pilot without the after-price tests the product, not the price |
| **Exit** | if the criteria are missed, they owe nothing more and you take the box back |

Why the after-price must be in the pilot agreement: if you announce the price only after a successful pilot,
the office has already decided what it is "worth" in its head — usually the pilot price per month. You lose
the anchor.

A **letter of intent** (level 3) is the fallback when a pilot is too early: a one-page, non-binding letter
saying the office intends to buy the *Office* package at PLN X per month if the pilot criteria are met.
Non-binding, but people rarely sign a price they find absurd.

---

## 6. Reading the evidence with small numbers

With ten conversations, one person changes the result by 10 percentage points. Rules:

1. **Look for agreement, not averages.** "Seven of ten put *too expensive* above PLN 1,800" is a finding;
   "the mean is PLN 1,537" is noise with decimals.
2. **Segment before you average.** A notary and a 10-person firm in one average describe nobody (pitfall B46).
3. **Weight by the ladder.** One paid pilot at PLN 1,500 a month outweighs ten stated prices of PLN 800.
4. **Write down what would change your mind** before you look at the data — exactly like the predictions in
   the course experiments.

---

## 7. EXERCISE 06 — the interview kit

Create `pricing/06-interviews/`:

- `script.md` — the six-step conversation of section 2 in Polish, with your package description in one
  paragraph;
- `vw.csv` — empty, with the header row;
- `gg.md` — your four test prices and the yes/no table;
- `log.md` — one line per conversation: date, profession, size, city, the ladder level reached, next step.

Nobody's name goes into these files. Use a code (`L01`, `N02` for a lawyer or a notary).

---

## 8. ⭐ FIELD EXPERIMENT 06 — ten offices, two pilots

**Hypothesis.** Among ten law or tax offices of 4–15 people that already pay for software, the Van Westendorp
acceptable range for the *Office* package lies roughly between PLN 900 and PLN 2,000 net per month, and at
least two offices agree to a paid pilot at PLN 3,000–5,000.

**Procedure.** Ten conversations following `script.md`. Four Van Westendorp questions, then Gabor-Granger
at four prices, then the leader/killer sort from part 04, then the ask. Record everything in the files of
exercise 06. Offer a paid pilot to every office that reaches level 3.

**Prediction (mine).** IPP around PLN 1,200–1,500. Fewer than half of the offices reach level 3. Two pilots
— but only from offices that already pay for cloud legal AI or a premium legal database (the targeting
result of part 03).

| Result | Value |
| :-- | :-- |
| Conversations held | |
| PMC / OPP / IPP / PME (convention: this tool) | |
| Gabor-Granger: gross-profit-maximising price | |
| Offices at level 3 (commitment) | |
| Paid pilots agreed, at what price | |
| What surprised me | |

---

## 9. Pitfalls

**B57 · "Would you buy this?"**
*Symptom:* the key question is hypothetical and about the future. *Why it hurts:* people are kind and
optimistic. *Remedy:* ask about the past, and ask for a step up the ladder.

**B58 · Pitching before listening.**
*Symptom:* the demo starts in minute two. *Remedy:* steps 1–3 of section 2 first, always.

**B59 · Friends and family as the sample.**
*Symptom:* your cousin's law office is three of your ten answers. *Remedy:* at most one warm contact per
ten, and mark it in the log.

**B60 · A survey number read as a fact.**
*Symptom:* "the optimal price is PLN 1,347." *Remedy:* with n < 30, a range and a direction only.

**B61 · The free pilot.**
*Symptom:* "Let them try it for free for a month, then we will talk money." *Why it hurts:* it measures
nothing about price and anchors the value at zero. *Remedy:* a paid pilot with the after-price in the
agreement.

---

## 10. Checkpoint

- [ ] The interview kit exists in Polish and you have run it once with a friendly professional as a rehearsal.
- [ ] At least five real conversations are logged, with the ladder level each reached.
- [ ] `vw.csv` has at least five rows and you have run `pricing_model.py vw` on it.
- [ ] One pilot agreement draft exists, with success criteria and the after-price.
- [ ] `pricing/06-wtp.md` states your price range and what would change it.

Sources for this part: [SOURCES.md](SOURCES.md), section "Part 06".
