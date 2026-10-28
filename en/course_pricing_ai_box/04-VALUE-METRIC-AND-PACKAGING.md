# Part 04 · Value metric and packaging: what you charge for

> **Goal of this part.** You decide **what unit** the price is attached to (the office, the user, the
> agent, the document, the outcome) and how the offer is split into packages. You design the expert-agent
> catalogue as the engine that makes revenue per office grow without a new sale.
>
> **Time:** ~4 h · **Level:** ⭐⭐⭐⭐ · **Produces:** `pricing/04-packages.md`

---

## 0. The problem

Part 03 gave you a ceiling for Office K. But Office K is one office. The next one has eight lawyers, the one
after that is a two-person notary. If you charge a single flat amount, you overcharge the small ones (they
leave) and undercharge the big ones (you leave money on the table). If you charge per user, the box —
whose cost hardly depends on users — becomes expensive exactly where it is cheapest to serve.

The fix is the **value metric**: the unit that grows when the customer gets more value, and that the price
follows.

---

## 1. What a good value metric does

Patrick Campbell (ProfitWell, now Paddle) reports that companies that charge along a value metric grow
about 2× faster, with about half the churn and 2× the expansion revenue (*vendor self-reported*, but
consistent with the logic below). A good value metric:

1. **Grows with the customer's value**, so the price feels fair at every size.
2. **Is easy to understand and to predict** — the customer can budget it (part 01: unpredictable bills
   destroy trust faster than high prices).
3. **Is easy for you to count** without inspecting the customer's data. For an on-premise box this is not
   a detail: you must not need access to client files to bill.
4. **Grows without a new sale** — so revenue per customer rises over time (net revenue retention, part 08).

---

## 2. The candidates for the box

| Metric | Grows with value? | Predictable? | You can count it without seeing data? | Grows without a sale? | Verdict |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **Per office** (flat) | weakly | ✅ | ✅ | ❌ | the base, not the whole price |
| **Per user / seat** | ✅ for lawyers | ✅ | ✅ | slowly (hiring) | a size dimension, careful: AI can reduce seats |
| **Per expert agent** (workflow) | ✅ each agent is a named job | ✅ | ✅ | ✅ **when you ship new agents** | ⭐ the growth engine |
| **Per document / page processed** | ✅ | ❌ | needs counters, still fine | ✅ | a meter — scares small buyers |
| **Per outcome** (accepted summary, filed letter) | ✅✅ | ❌ | needs counters + definitions | ✅ | later, for one narrow agent |
| **Per token** | ❌ | ❌ | ✅ | — | ❌ never (pitfall B32) |

The recommended structure — my opinion, to be tested in part 06:

```
 price per month  =  platform fee (per office, includes the box service and N users)
                  +  Σ expert agents chosen (each priced separately)
                  +  extra users above N (small fee)
```

Why this shape:

- The **platform fee** covers your cost floor (part 02): support, updates, monitoring, the box. It makes
  every office profitable from month one.
- **Expert agents** carry the value (part 03). Each one is a named job the office recognises — *"incoming
  court letter triage"*, *"contract comparison against our template"*, *"KSeF invoice check"* — with a
  price the office can compare with the hours it saves.
- The **user dimension** handles the size difference between a 2-person and a 12-person office, without
  making the core price per head.

This is a "hybrid" in the sense of the 2025–2026 surveys (part 01), but with no meter: the variable part
is chosen by the customer, not counted by you.

---

## 3. The expert-agent catalogue: the engine of a scalable business

You told me you want a company that scales by adding expert AI agents. In pricing terms, that is a precise
statement:

> **Each new agent you build is sold to every office you already have, at almost zero additional COGS.**

The box, the support relationship and the update channel already exist. A new agent costs you development
time (OpEx, once) and an evaluation set (once), and then it is a remote update to every box. This is the
cheapest revenue you will ever earn, and it is why the agent catalogue — not the box — is the product.

### 3.1 Design rules for the catalogue

| Rule | Why |
| :-- | :-- |
| **One agent = one job a professional names in their own words** | "Court letter triage" sells; "RAG over your documents" does not |
| **Every agent has a measured time saving** (field experiment 03) | the price of the agent is justified by its own number |
| **Agents are profession-specific** | a law office does not pay for a KSeF agent; an accounting office does. Separate catalogues per profession |
| **Each agent has its own evaluation set before release** | your quality promise; ties to `course_agentic_apps/14-EVALUATION.md` |
| **No agent is free forever** | a free agent anchors the price of all agents at zero (pitfall B49) |

### 3.2 Leaders, fillers, killers (Ramanujam)

Before an agent goes into a package, classify it using the willingness-to-pay conversations of part 06:

| Type | Definition | For the box (examples, hypotheses) | Where it goes |
| :-- | :-- | :-- | :-- |
| **Leader** | the reason they buy; most buyers want it and would pay for it | incoming letter triage with a deadline proposal; contract comparison | in every package — it is why the package exists |
| **Filler** | nice to have, raises perceived value cheaply | a translation agent; meeting notes from a recording | in the upper packages |
| **Killer** | wanted by < 20% and **actively disliked** by > 20% | anything that sends data outside the office, even "optional"; an agent that talks to clients directly | **never in a package**; at most a separate add-on |

The "killer" category is not theoretical for you: a hybrid feature that sends anonymised text to a cloud
model is a great technical idea (course 1, part 10) and may be a killer for half of your buyers. Offer it as
an explicit, separately signed add-on, never inside a package.

---

## 4. Good / better / best

Three packages. Not two (no middle to anchor), rarely four (choice paralysis).

| | **Start** | **Office** ⭐ | **Office Pro** |
| :-- | :-- | :-- | :-- |
| For | 1–3 people, trying it | 4–10 people, the target | 10+ people or several workflows |
| Users included | 3 | 10 | 25 |
| Expert agents included | 1 leader | 2 leaders + 1 filler | 4 + all fillers |
| Support | e-mail, next business day | phone, same day | phone, 4 h, quarterly review |
| Updates & monitoring | ✅ | ✅ | ✅ |
| Audit log and compliance pack (§ 23e note, processing agreement, DPIA template) | basic | ✅ | ✅ + annual review |
| Extra agents | priced per agent | priced per agent | priced per agent, discounted |

The package names and contents above are an **illustration**. The prices come in part 07, after you
measure willingness to pay.

### 4.1 Targets to check after the first 20 customers

Ramanujam's targets for a healthy good/better/best split:

| Share of buyers on… | Healthy | What a miss tells you |
| :-- | :-- | :-- |
| Good (Start) | **< 30%** | > 50% on the entry tier: Start is too good, or the others too expensive |
| Better + Best (Office + Pro) | **> 70%** | the middle package is not the obvious choice |
| Best (Pro) | **> 10%** | 0%: Pro has nothing a real customer wants |

### 4.2 The compliance pack — your hidden gem

Part 01 named the risk of a **hidden gem**: a valuable thing you give away without noticing. For your
buyers, the compliance pack is a candidate:

- a written note mapping your box to § 23e of the advocates' Code of Ethics (or the KIRP recommendations for
  legal advisers);
- a data processing agreement template and a DPIA template for the office;
- an audit log the office can export when a client asks *"which tools did you use?"* — the exact question
  § 23e says the advocate must answer.

Do not give it away silently. Put it **visibly** in the package table, because it is part of why Office K
pays more than for ChatGPT. Whether it is worth a separate line on the invoice is a question for part 06.

---

## 5. One-off fees: setup and onboarding

A **setup fee** pays for installation, first indexing of the archive and the first agent tuned on the
office's own documents. Rules:

1. **Always charge it**, even if you discount it. A free setup tells the customer installation is trivial
   and trains them to expect free work.
2. **Price it from your measured installation time** (field experiment 02) × the hour cost, plus a margin.
   It is the one price where cost-plus is acceptable, because it pays for labour.
3. **Keep it below the "needs a meeting" threshold** of the office. Ask in part 06 what amount the senior
   partner can approve alone.

The repo's earlier guess of PLN 25,000–60,000 for setup *including hardware* (`ai-business-asymmetries`)
was made before the cost floor existed. With hardware handled separately (part 05) and an installation
measured in hours, the setup fee alone will likely be much smaller. Your field experiment decides it.

---

## 6. Contract length and billing period

| Choice | Effect for you | Effect for the customer |
| :-- | :-- | :-- |
| Monthly, cancel any time | easy to sell, high churn risk, no cash up front | low risk |
| **12 months, billed monthly** | predictable revenue, moderate commitment | familiar (LEX and Legalis sell like this) |
| 12 months, **billed annually up front** | cash up front — funds the next boxes (part 05) | wants a discount for it |
| 24–36 months tied to the hardware | matches a lease or rent term | a big decision for a small office |

**Recommendation (my opinion):** 12 months as the default, billed monthly; a modest discount for paying a
year up front; 24–36 months only when you provide the hardware (rent model, part 05). On discounts:
Campbell's ProfitWell data found discount size **almost perfectly correlated with churn**, and his rule is
never to discount more than about 20% (*vendor self-reported*). Part 07 builds the discount policy.

---

## 7. EXERCISE 04 — your packages

In `pricing/04-packages.md`:

1. Write your **value metric** in one sentence, and check it against the four tests of section 1.
2. List the expert agents you could build in the next 12 months for **one** profession. At least six.
   Mark each as *leader*, *filler* or *killer* — as a hypothesis, to be confirmed in part 06.
3. Draft the three packages as a table like section 4, without prices.
4. Decide what is in the platform fee and what is never free.
5. Draft the setup fee as: measured hours × hour cost × (1 + margin).

---

## 8. ⭐ FIELD EXPERIMENT 04 — which agents are leaders?

**Hypothesis.** Among the six agents on your list, at most two are leaders. Office K-type buyers will name
the same two.

**Procedure.** With five professionals from your target segment (the same people as in part 06 where
possible), show the six agent names, each with a one-line description. Ask them to:

1. sort them from *"must have"* to *"would not use"*;
2. mark any they would **not want** in the office at all;
3. for the top one: *"If this were the only thing the box did, would it be worth paying for?"*

**Prediction (mine).** Incoming-letter triage and contract comparison are leaders for law offices. Any agent
that drafts letters *to clients* is marked as unwanted by at least one in five (a killer candidate).

| Agent | Must-have votes (of 5) | Unwanted votes (of 5) | "Worth paying for alone"? | Type |
| :-- | --: | --: | :-- | :-- |
| | | | | |

---

## 9. Pitfalls

**B47 · Per-seat pricing for a box whose cost does not depend on seats.**
*Symptom:* a 12-person office pays 4× a 3-person office for the same box and support. *Remedy:* the
platform fee per office; users only as a size dimension with generous inclusions.

**B48 · A meter on a small buyer.**
*Symptom:* "PLN 0.50 per page processed." *Why it hurts:* the office cannot budget it and starts rationing
use — which kills the value you need to prove. *Remedy:* flat packages; meters only above a generous
included volume, if at all.

**B49 · The free agent.**
*Symptom:* "the first agent is included for free." *Why it hurts:* it anchors the price of every agent at
zero. *Remedy:* agents are included in a **priced** package, never "free".

**B50 · Killers inside a package.**
*Symptom:* the cloud-escalation feature is part of the Pro package. *Remedy:* a separate, explicitly signed
add-on.

**B51 · Packages designed by features, not by buyers.**
*Symptom:* Start/Office/Pro differ by technical limits (RAM, models). *Remedy:* packages differ by **who the
buyer is** (size, workflows, service level).

---

## 10. Checkpoint

- [ ] One-sentence value metric that passes the four tests.
- [ ] A catalogue of ≥ 6 agents for one profession, each with a hypothesis: leader / filler / killer.
- [ ] Three packages without prices, differing by buyer type.
- [ ] A written list: *never free*.
- [ ] Field experiment 04 has at least three filled rows.

Sources for this part: [SOURCES.md](SOURCES.md), section "Part 04".
