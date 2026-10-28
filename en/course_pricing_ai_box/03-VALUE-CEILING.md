# Part 03 · The value ceiling: what the box is worth to Office K

> **Goal of this part.** You estimate, in PLN per month, what the box is worth to one specific office:
> the price of its next-best alternative plus the value of what the box does better. You find out that the
> answer depends more on **which office** you sell to than on what the box does — and that this decides
> your target customer.
>
> **Time:** ~4 h · **Level:** ⭐⭐⭐ · **Produces:** `pricing/03-value.md`, the *Reference value* and
> *Economic value* sections of `pricing/01-anchors.md` · **Tool:** `tools/pricing_model.py value`

---

## 0. The problem

In part 02 the floor came out at roughly PLN 1,400–3,000 per office per month, depending on support hours
and the margin target. Is that a lot? You cannot know from the cost side. The only way to know is to
estimate what the box is worth to the person who pays — and what they would do instead.

Engineers usually skip this step for a good reason: "value" sounds unmeasurable. It is not. It is a sum of
a few numbers, each of which you can look up or ask about. They are uncertain, so you compute a range and
you write the assumptions down. That is still far better than no number.

---

## 1. The method: Economic Value Estimation

From Nagle & Müller, *The Strategy and Tactics of Pricing* (6th ed., 2018):

```
 economic value  =  reference value  +  differentiation value
                    (price of the        (what is better about yours, in PLN,
                     next-best            minus what is worse)
                     alternative)
```

Four steps:

1. **Name the next-best alternative** the customer would really use. Not the one you would compare yourself
   with; the one *they* would choose.
2. **Price it** for this customer, per month.
3. **List the differences** between your box and that alternative, positive and negative.
4. **Put a PLN value on each difference**, with the assumption written next to it.

The result is a ceiling. Your price must be **below** it, leaving the customer a reason to switch. How far
below is a negotiation and positioning choice (section 5).

---

## 2. Who is Office K, and who else could be

The market, from the research for this course (25 Oct 2026; details and caveats in [SOURCES.md](SOURCES.md)):

| Profession | How many in Poland | Notes for pricing |
| :-- | --: | :-- |
| Advocates (adwokaci) | 29,506 hold the title; ~23,600 practise (2025) | rp.pl, citing a Watchdog Polska report, 2 Sep 2026; no official NRA count of practising advocates found |
| Legal advisers (radcowie prawni) | 56,415 on the lists (2025) | same source; practising share not found |
| Notaries | 4,297 notaries, 3,507 offices (31 Dec 2025) | KRN. In H1 2025, 23% of notaries had no employees and 35% had exactly one (rp.pl). **Notarial fees frozen since 2004** |
| Tax advisers | 9,220 (18 Dec 2025) | KIDP |
| Accounting offices | ~70,000 (**estimate**) | KIBR, 2022, repeated by Infor in 2026; KIBR says the true number is unknown |
| Firm size | ~99% of legal, accounting and tax firms employ ≤ 9 people | GUS, **2014** — no recent split found |

Two conclusions before any calculation:

- The **market is large in count and small per buyer**. Tens of thousands of offices, almost all under ten
  people. A price that needs a 20-person firm describes a small minority.
- **Notaries look weak for pricing**: most offices are one or two people, and their own prices are frozen.
  Their willingness to pay is likely lower than their secrecy need suggests. (A hypothesis — test it in
  part 06 before you drop them.)

**Office K** (our running example) is a five-person law office in a mid-size city: two advocates, one
trainee, two assistants.

---

## 3. Step 1–2: the reference value

What would Office K use instead of your box? There are three honest candidates.

### 3.1 Alternative A: a professional cloud legal AI

| Product | Price (net) | Note |
| :-- | :-- | :-- |
| Beck-Noxtua | PLN 590 per user per month, unlimited use; **requires Legalis Silver or higher** | beck-noxtua.pl; one trade site (TAX.PL, ~Aug 2026) still described it as "coming soon" |
| LEX Kancelaria Prawna | Standard PLN 298.30; Optimum PLN 525; Premium PLN 722 per month | lex.pl; the price of the *LEX Expert AI* add-on is not published |
| Gaius-Lex "Gaius Vault" | on-premise / air-gapped; **no public price** | the closest Polish competitor to your positioning |

For Office K: two advocates on Beck-Noxtua = **PLN 1,180 per month**, on top of the legal database they
already pay for.

### 3.2 Alternative B: a general cloud assistant

ChatGPT Business USD 20–25 per seat, Claude Team USD 20–25 per standard seat, Microsoft 365 Copilot
USD 30 (Business: USD 21 list, USD 18 promotional to end of 2026). For five people: roughly **PLN 400–550
per month**.

This is cheap, and many lawyers already use it: in the Fundacja SET / Logit survey of Polish advocates and
legal advisers (Feb 2026), **53.6% use free or open tools, often without a data processing agreement and
outside secure environments**. At the same time **81% name client data security and confidentiality as a
concern**.

The rule that now applies to advocates: **§ 23e of the Code of Ethics** (adopted by the NRA on 12–13 June
2026, published 15 June 2026). As summarised in the research: AI may be used only in a supporting role;
information covered by professional secrecy must not be entered into tools that do not protect it
adequately; outputs must be verified; and on request the advocate must tell the client which tools were
used. The KIRP recommendations for legal advisers (2025) ask them to check whether processing stays in the
EEA, whether data is used for training and whether a processing agreement is needed — and note that
on-premise AI is possible but **"extremely rare"** in practice.

⚠️ § 23e does **not** ban cloud AI. A cloud tool with an EEA data location and a proper processing agreement
can be "adequate". Do not sell the box as "the only legal option" — it is false, and a lawyer will know it
(pitfall B44). Sell it as **the option where the question does not arise**.

### 3.3 Alternative C: doing it by hand

Price: PLN 0 in cash, paid in hours. For an office that has decided cloud AI is not acceptable for client
files, this is the true alternative, and its reference value is **zero**.

### 3.4 Which one is Office K's?

You do not know until you ask (part 06, and field experiment 01 from part 01). The choice matters enormously,
as section 6 shows. Write all three into `pricing/03-value.md` and mark which one you believe applies.

---

## 4. Step 3–4: the differentiation value

### 4.1 Time

The largest positive line. You need three numbers per role:

| Number | Where it comes from |
| :-- | :-- |
| **Hours saved per person per week** | Measure in the pilot. Until then: Wolters Kluwer *Future Ready Lawyer 2026* (810 lawyers, 11 countries, incl. Poland): over 60% of respondents say AI saves them **6–20% of weekly working time** (*self-reported*). 3 hours of a 40-hour week is 7.5% — inside that range, at the cautious end |
| **What an hour is worth** | For lawyers, the billing rate. No authoritative Polish survey of hourly rates exists for 2025–2026; indicative ranges from blog and marketing sources: **PLN 150–250** net in towns under 100,000 people, **PLN 250–400** in mid-size cities, **PLN 350–600** in Warsaw, Kraków and Wrocław. For assistants, their cost per hour to the office — ask, do not guess |
| **Realisation** | The share of saved hours that turn into money: billed to a client, or used for billable work. **This is the number most value calculations get wrong.** A saved hour that becomes a longer lunch is worth PLN 0 to the office's bank account. Start at 0.3–0.5 |

Run it for Office K's two advocates (3 h/week each, PLN 300/h — a mid-size city, realisation 40%):

```bash
python3 pricing_model.py value --people 2 --hours-saved 3 --rate 300 --realisation 0.4 --alternative 1180
```

Time value: **PLN 3,118 per month** for the two advocates.

The same for the trainee and two assistants, at an **assumed** PLN 60 per hour of their cost and a 30%
realisation, adds about **PLN 700**. Their saved time is real but rarely turns into money, unless it lets
the office avoid a hire.

### 4.2 Permission and risk

The box makes something possible that otherwise is not: AI on client files with no transfer question at
all. How much is that worth?

- If Office K has decided **never to put client files into a cloud tool**, then *all* of the time value
  above depends on the box. Without it the value is not "less AI", it is "no AI".
- If Office K **already uses ChatGPT on client files**, as more than half of surveyed lawyers do with free
  tools, the box removes a risk they may not have priced: a disciplinary question under § 23e, a GDPR
  incident, a client asking "which tools did you use?".

**Do not put a risk number into the price.** Expected-loss calculations (probability × fine) look rigorous
and are not: you have no probability. Use risk in the *sales story* (part 07) and keep
`--risk-value 0` in the calculator. That keeps your price defensible.

### 4.3 The negative lines

Subtract them honestly, at least as words in `03-value.md`:

| Negative difference vs the cloud | How large |
| :-- | :-- |
| A smaller model than the frontier cloud models | depends on the workflow; measure on their documents |
| Hardware in the office: space, noise, power, a thing that can break | small but felt |
| A one-person vendor: "what if you disappear?" | **large** for a cautious buyer — answer it in the contract (escrow of the box image, a partner who can take over) |
| Installation and a learning curve | a one-off, but it delays value by weeks |

---

## 5. From the ceiling to a price

The calculator prints three candidate prices: the reference value plus 10%, 20% or 30% of the
differentiation value. Why only a fraction?

- The customer must **see a gain** after paying you, or there is no reason to change anything.
- Your value estimate is **uncertain**, and the customer's own estimate is lower than yours.
- Switching has a cost (time, risk) that does not appear in the calculation.

A capture of 10–30% of the differentiation value is a common starting range for a new vendor with no
references. It rises as you collect proof (references, measured hours from pilots).

---

## 6. The result: the alternative decides everything

Same box, same time saved, same office — only the alternative changes (two advocates, 3 h/week each,
PLN 300/h, 40% realisation; from `pricing_model.py value`):

| Office K's alternative | Reference value | Economic value (ceiling) | Price at 10% / 20% / 30% capture |
| :-- | --: | --: | :-- |
| A — Beck-Noxtua for both advocates | 1,180 | **4,298** | 1,492 / **1,804** / 2,115 |
| C — by hand (cloud AI not acceptable) | 0 | **3,118** | 312 / **624** / 935 |

Now put part 02 next to it. The floor at 20 offices, 1 hour of support and a 60% margin was **PLN 1,417**.

- Against an office that **would otherwise buy cloud legal AI**, a price of PLN 1,500–2,100 sits above your
  floor and below their ceiling. **The business works.**
- Against an office that **would otherwise do it by hand**, the comfortable price (PLN 300–900) is **below
  your floor**. The business does not work with the advocates' time alone — unless the office is bigger,
  their rate is higher, realisation is higher or support is lower.

This is the most important result of the course so far, and it is a **targeting** result, not a pricing
result:

> **Sell first to offices that already pay, or are ready to pay, for AI — and are uneasy about where their
> data goes.** They have a reference value above zero and a reason to switch. An office that has never paid
> for AI has to be convinced twice: that AI is worth money, and that your box is the right AI.

In practice that points to: offices of **5–15 people** in cities with higher rates, already on LEX or
Legalis, and already experimenting with ChatGPT or Copilot. That matches the buyer range in the repo's
profile (5–50 staff), narrowed from the bottom.

---

## 7. EXERCISE 03 — value for three offices

In `pricing/03-value.md`, compute the economic value for three offices:

1. **Office K** as described.
2. **A two-person notary office** (one notary, one assistant), alternative C, an hourly value you choose
   and justify.
3. **A ten-person tax-advisory or accounting office**, the alternative you think is most likely.

For each: the alternative, the reference value, the differentiation lines (positive and negative), the
calculator output, and the price at 20% capture. Then compare each 20%-capture price with your floor from
part 02. Write one sentence per office: *works / does not work / works only if …*.

Fill `pricing/01-anchors.md`: *Reference value* and *Economic value* for Office K.

---

## 8. ⭐ FIELD EXPERIMENT 03 — measure the hours, not the opinion

**Hypothesis.** On one real workflow (for example, triage of incoming court letters: summary, deadline,
proposed next step), the box saves a lawyer at least 10 minutes per document compared with doing it by hand.

**Procedure.** With one friendly lawyer, take 20 anonymised or public documents of the kind they really
receive. They process 10 by hand and 10 with your workflow, alternating. Time each one. Record how many of
the AI outputs needed correction, and how long the correction took. Do it on your own rig — this is a
measurement, not a pilot.

**Prediction (mine).** By hand: 15–25 minutes per document. With the workflow: 5–10 minutes including
checking. Two or three outputs out of ten need a real correction.

| Document | Method | Minutes | Correction needed? | Minutes of correction |
| :-- | :-- | --: | :-- | --: |
| 1 | by hand | | — | — |
| 2 | workflow | | | |
| … | | | | |

Turn the result into `--hours-saved`: minutes saved per document × documents per week ÷ 60. **Your measurement
replaces the survey figure from section 4.1.** One measured workflow is the strongest argument you will
ever bring to a sales meeting.

---

## 9. Pitfalls

**B42 · Value computed against the wrong alternative.**
*Symptom:* you compare the box with Harvey (estimated by third parties at USD 1,000–2,000 per user per month)
and conclude it is cheap. *Remedy:* the alternative is what **this** customer would use, usually "by hand"
or a PLN 100 per month assistant.

**B43 · Realisation assumed to be 100%.**
*Symptom:* "3 hours saved × PLN 300 = PLN 900 a week of value." *Remedy:* only hours that turn into money
count. Start at 30–50% and ask the customer what they would do with the time.

**B44 · "The only legal option" claims.**
*Symptom:* the pitch says cloud AI is forbidden for lawyers. *Why it hurts:* § 23e does not say that, the
lawyer knows it, and you have just lost credibility. *Remedy:* "with the box the question does not arise".

**B45 · Risk value in the price.**
*Symptom:* "a GDPR fine could be PLN 1M, so 1% of that is worth PLN 10,000." *Remedy:* risk belongs in the
story, not in the number. `--risk-value 0`.

**B46 · One price for all professions.**
*Symptom:* the same price list for a notary and a 10-person law firm. *Remedy:* the economic value differs by
a factor of 5–10. Different packages, or different target customers (part 04).

---

## 10. Checkpoint

- [ ] `pricing/03-value.md` has three offices with all four EVE steps written out.
- [ ] Every number is marked *measured*, *researched (source)* or *assumed*.
- [ ] You can state Office K's ceiling and your 20%-capture price from memory.
- [ ] You have written down which kind of office you will sell to **first**, and why (section 6).
- [ ] Field experiment 03 is planned with a named lawyer and a date.

Sources for this part: [SOURCES.md](SOURCES.md), section "Part 03".
