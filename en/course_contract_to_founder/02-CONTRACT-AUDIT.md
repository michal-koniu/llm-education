# Part 02 · Contract audit: what your B2B contract allows

> **Goal of this part.** You read your contract with the bank clause by clause and fill a matrix: what it
> says about IP, competition, confidentiality, availability, tools and termination — and what Polish law
> says about each of those clauses. You learn the new 2026 rules on reclassifying B2B contracts as
> employment. You decide whether to ask the client for a written confirmation, and you have the letter ready.
>
> **Time:** ~5 h + one hour with a lawyer · **Level:** ⭐⭐⭐⭐ · **Produces:** `founder/02-clause-matrix.md`,
> optionally `founder/02-letter-draft.md`

> **Not legal advice.** This part teaches you to **read** your contract and to ask the right questions. One
> paid hour with a lawyer who reads the actual contract is worth more than this whole part. Have it before
> you sign anything with a customer.

---

## 0. The problem

Your startup will produce software, prompts, evaluation sets and documentation, and it will sell into a
market adjacent to banking (professional offices, maybe financial advisers one day). Your contract with the
bank was written by the bank's lawyers to protect the bank. It probably contains:

- a clause transferring copyright in "works" to the bank;
- a confidentiality clause, possibly with bank secrecy;
- maybe a non-compete;
- contractual penalties for breaching them;
- DORA clauses (audit rights, security, subcontracting), because a bank's IT suppliers are now regulated.

None of these is a problem **if you know what they say**. Each is a serious problem if you find out when an
investor's lawyer asks (part 03) or when the bank's lawyer writes to you.

---

## 1. Copyright: who owns what you write

### 1.1 The rules

From the Copyright Act (Dz.U. 2025 poz. 24), as researched for this course:

| Rule | Article | What it means for you |
| :-- | :-- | :-- |
| A transfer or licence covers **only the fields of exploitation it expressly lists** | art. 41(2) | "all rights" without a list is weak; the bank owns only what is listed |
| A contract is **void in so far as it covers all future works** of the author, or all future works of a given kind | art. 41(3) | "everything you create during the contract" is at least partly void |
| Only fields of exploitation **known when the contract is signed** can be covered | art. 41(4) | |
| A transfer **must be in writing**, or it is void | art. 53 | no e-mail "you can have it" transfers |
| The employer owns works (art. 12) and programs (art. 74(3)) created by an **employee** as part of their duties | art. 12, 74(3) | **does not apply to you** as a B2B contractor — the bank gets only what the contract transfers |

Specific, well-identified future works *can* be transferred (PARP); what is void is the blanket "everything".

### 1.2 What to look for in your contract

The typical over-broad IT clause looks like this (an example from the research, not your contract):

> *„Wykonawca przenosi na Zamawiającego autorskie prawa majątkowe do wszelkich utworów, w tym programów
> komputerowych, stworzonych w okresie obowiązywania Umowy…"*

Problems with it: it covers **all** works, so it collides with art. 41(3); it does not separate work done
**for the client** from work done in your own time with your own tools; and its list of fields of exploitation
is often generic.

Being probably void in part is **not** a plan. A clause that is void "in part" still has to be argued in court.
What you want is a contract where the transfer is clearly tied to **deliverables made in performance of the
contract or of specific orders**, with an express carve-out for pre-existing IP and for independent work done
outside the contract, without the client's resources or confidential information. That is the purpose of the
letter in section 8.

---

## 2. Non-compete: what you may not do

### 2.1 The rules

- Between businesses, a non-compete is allowed by **freedom of contract** (art. 353¹ of the Civil Code),
  limited by art. 58 (void if contrary to law or to the principles of social coexistence).
- **No statute requires compensation** for a B2B non-compete. The Labour Code rules — a separate written
  agreement and at least **25%** compensation after the job ends (art. 101¹–101³) — apply to employees only.
- Case law:
  - **SN, 11 Sep 2003, III CKN 579/01:** a non-compete **during** the contract is valid. A **3-year
    post-termination** ban **with no compensation** was **void** as contrary to the principles of social
    coexistence, by analogy with the Labour Code.
  - **SN, 19 Nov 2015, IV CSK 804/14** (via Rzeczpospolita): between businesses, lack of compensation **alone**
    does not make the clause void — it becomes void if imposed by exploiting a superior bargaining position.

### 2.2 What to look for

1. **Is there one at all?** Many IT B2B contracts have none, or only a non-solicitation clause (you may not
   poach the bank's staff or customers).
2. **Scope:** "competitive activity" defined how? Banking? Financial software? "Any IT services"? An AI box for
   law offices does not compete with a bank — **unless** the clause is written as "any activity in the field of
   IT" or "for any financial institution". Write the exact wording into the matrix.
3. **Duration:** during the contract only, or after? For how long?
4. **Compensation:** none, or paid?

---

## 3. Confidentiality, trade secrets and bank secrecy

| Source | What it says | Effect on the startup |
| :-- | :-- | :-- |
| **Unfair Competition Act, art. 11** (Dz.U. 2026 poz. 85) | using or disclosing another's trade secret is unfair competition; binds you **by statute**, not only by contract. **Independent creation and reverse engineering of a lawfully obtained public product are lawful** (art. 11(7)) | the bank's architecture, code, prompts, vendor terms, data and internal documents must never appear in your product. Your own independently built work is yours |
| **Banking Law, art. 104** (Dz.U. 2026 poz. 38) | bank secrecy binds the bank, its staff and those through whom it acts; outsourcing providers who receive secret data may use it **only** to perform the contract (art. 104(5)) | criminal penalty for breach: a fine up to PLN 1,000,000 and up to 3 years in prison (art. 171(5)). Whether it binds a single IT contractor who never sees client data is **not settled** — banks impose it by contract anyway |
| **Your contract's NDA** | usually broader than both | read the definition of "confidential information" — it often includes "know-how" |

The practical rule is simple and strict: **nothing from the bank enters the startup.** Not code, not
documents, not data, not a Slack message, not a "pattern I saw there". Part 03 turns this rule into a
procedure.

---

## 4. DORA: why the bank's lawyers care about you

The Digital Operational Resilience Act (Regulation (EU) 2022/2554) applies to banks from **17 January 2025**.
It regulates the **bank**, not you — but it requires the bank to put certain terms into every contract for ICT
services, and those terms reach you:

| DORA requirement (art. 28, 30) | How it can appear in your contract |
| :-- | :-- |
| Register of all ICT contracts; risk assessment before contracting | the bank classifies your service — ask how |
| Termination rights for breach, weaknesses in ICT risk management, supervisory obstacles (art. 28(7)) | grounds on which the bank can end your contract |
| Rights and obligations in **one written document** (art. 30(1)) | an annex — "Aneks DORA" |
| Subcontracting allowed or not, and on what conditions (art. 30(2)(a)) | you may not let anyone else do the work |
| Data locations, confidentiality, incident assistance, cooperation with the authorities, security training (art. 30(2)) | duties to report incidents, take training |
| For critical or important functions: audit and access rights for the bank and the KNF, exit and transition (art. 30(3)) | the bank may audit "your systems" — read how they are defined |

Polish market templates of DORA annexes treat a sole trader who works personally as **personnel**, not as a
subcontractor (MessageFlow template, 2025). There is no guidance from the European authorities or the KNF on
one-person contractors.

**Why this matters for the startup:** an audit clause defined as "the contractor's ICT systems used to provide
the services" is fine. One defined as "all systems of the contractor" would, in theory, reach the machines you
build the startup on. One more reason for the separation in part 03.

---

## 5. Contractual penalties

From the Civil Code:

- A penalty can be agreed for breaching a **non-monetary** obligation — confidentiality, non-compete, IP
  (art. 483).
- It is due **regardless of the damage** (art. 484(1)); the Supreme Court confirmed it is due even with **no
  damage at all** (resolution of 7 judges, III CZP 61/03, 6 Nov 2003).
- A court may reduce a penalty that is **grossly excessive** or if the obligation was largely performed
  (art. 484(2)).

Write every penalty amount into the matrix. A PLN 100,000 penalty for a confidentiality breach, due without
damage, is the number that should shape your behaviour — not the probability of a lawsuit.

---

## 6. Reclassification: the 2026 rules

### 6.1 What changed

The amendment to the National Labour Inspectorate Act of 11 March 2026 (**Dz.U. 2026 poz. 473**) is **in force
since 8 July 2026**. Its key points, from the research:

| Rule | Detail |
| :-- | :-- |
| **A labour inspector can decide, by administrative decision, that an employment relationship exists** | where work is done in the conditions of art. 22 § 1 of the Labour Code: under the client's direction, at a place and time it sets, for pay |
| A prior **order** comes first | the inspector first orders the violation to be removed; the decision comes only if the order is not obeyed |
| **The parties' will counts** | it must be taken into account unless contrary to law or aimed at circumventing it (art. 33a(4)) |
| Effects **from the date of the decision** | for labour law, tax, social and health insurance; going back further needs a court case |
| Defaults where evidence is missing | indefinite term, full time, **minimum wage** |
| Appeal | to the labour court within one month |
| **Applies to existing contracts** | contracts concluded before 8 July 2026 and still running |
| "Amnesty" for the client | no fine if the client voluntarily converts a sham B2B contract into employment **by 8 July 2027** |
| Data sharing | PIP, ZUS and the tax administration (KAS) share data for risk analysis |
| Individual interpretations | the Chief Labour Inspector rules on a described relationship, fee **PLN 40** |

Art. 22 of the Labour Code itself did **not** change: employment is what it always was; the inspector now has a
faster tool to say so.

First practice: by 25 Aug 2026 the Chief Labour Inspector had issued 9 interpretations — 4 confirmed a civil-law
relationship, 5 found employment. One concerned **IT B2B work and found no employment**, because work was done on
separate orders that could be refused, the client set results and deadlines but not the method, and the provider
bore the economic risk and was paid per service (PIP, 30 Sep 2026).

### 6.2 Why it matters to a founder

If your contract were ever reclassified, from the date of the decision:

- **IP:** art. 12 and art. 74(3) of the Copyright Act would apply — works and programs you create **as part of
  your duties** would belong to the bank. A startup outside your duties stays yours, but "AI software" and
  "software for the bank" are close enough to argue about.
- **Non-compete:** the Labour Code rules would apply; during employment, an employer can bar competing
  activity without compensation (art. 101¹).
- **Tax:** a taxpayer loses ryczałt for the year if they invoice a current or former employer for work they did
  as its employee (art. 8(2) of the lump-sum tax act).

### 6.3 Your risk indicators — honestly

You told me the contract pays **per day** and the work takes **about an hour a day**. Read the table with that in mind:

| Points towards employment | Points away from employment |
| :-- | :-- |
| pay per day of availability rather than per result | few hours of actual work; no fixed place |
| fixed hours or availability windows set by the bank | you choose how to do the work |
| daily reporting, a manager who gives instructions on method | you bear economic risk (unpaid days off, your own equipment) |
| one client for years, integrated into the bank's team | other clients — **including your own startup** |

The last row is a useful irony: a real, separate business of your own is one of the signs that you are an
entrepreneur and not an employee. Build it cleanly (part 03), and it supports your B2B status rather than
threatening it.

---

## 7. EXERCISE 02 — the clause matrix

Create `founder/02-clause-matrix.md`. One row per clause; quote the clause **exactly**:

| # | Topic | Clause (exact text, § number) | What it covers | What the law says (section of this part) | Risk for the startup (L/M/H) | Action |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | IP transfer | | | §1 | | |
| 2 | Pre-existing IP / carve-out | | | §1 | | |
| 3 | Non-compete during the contract | | | §2 | | |
| 4 | Non-compete after the contract | | | §2 | | |
| 5 | Non-solicitation | | | §2 | | |
| 6 | Confidentiality / definition of confidential information | | | §3 | | |
| 7 | Bank secrecy | | | §3 | | |
| 8 | DORA annex: audit scope, subcontracting, incidents | | | §4 | | |
| 9 | Availability, working hours, reporting | | | §6 | | |
| 10 | Use of the bank's equipment, accounts, AI tools | | | §3 | | |
| 11 | Exclusivity / approval of other activities | | | §2 | | |
| 12 | Contractual penalties (amount per clause) | | | §5 | | |
| 13 | Termination and notice period | | | — | | |

Then book **one hour with a lawyer** (employment and IT contracts), send them the contract and your matrix,
and ask three questions: *Does the IP clause reach work I do in my own time with my own equipment? Is there any
clause my AI-box business would breach? What would you change?*

---

## 8. To ask or not to ask: the letter

You can ask the bank to confirm in writing that your separate business is outside the contract. Weigh it:

| Ask | Do not ask (yet) |
| :-- | :-- |
| a written carve-out removes the IP question for good — investors will ask for it (part 03) | it draws attention to the side business; some managers react badly |
| if the bank says no, you learn it now, not after you built the product | if the contract is already clean (lawyer's opinion), there is nothing to fix |
| it is honest and professional | |

**My recommendation:** have the lawyer read the contract first. If the IP or non-compete clauses are broad,
ask — before you write the product code, not after. If they are clean, keep the lawyer's written opinion in
your files and ask only when you are about to sign with an investor.

A draft for your lawyer to adapt (Polish, since the contract is Polish):

> **Szanowni Państwo,**
>
> w związku z umową nr … z dnia … informuję, że poza jej wykonywaniem prowadzę odrębną działalność
> polegającą na tworzeniu i sprzedaży oprogramowania do lokalnej analizy dokumentów dla kancelarii i biur
> rachunkowych. Działalność ta nie obejmuje usług dla instytucji finansowych, jest prowadzona poza czasem
> świadczenia usług na rzecz Państwa, na moim własnym sprzęcie i bez wykorzystania jakichkolwiek informacji,
> zasobów ani dokumentów Banku.
>
> Proszę o potwierdzenie, że (1) postanowienia § … umowy dotyczące przeniesienia autorskich praw majątkowych
> obejmują wyłącznie utwory stworzone w ramach wykonywania umowy i zleceń na jej podstawie, a nie utwory
> powstałe w ramach opisanej działalności, oraz (2) działalność ta nie stanowi działalności konkurencyjnej
> w rozumieniu § … umowy.
>
> Z poważaniem, …

The English meaning, for your notes: you inform the bank of a separate business making on-premise
document-analysis software for law and accounting offices, not serving financial institutions, done outside the
hours of service, on your own equipment, without any bank information; you ask them to confirm that the IP
clause covers only works made under the contract and its orders, and that the business is not competition under
the non-compete clause.

---

## 9. ⭐ FIELD EXPERIMENT 02 — what does the contract actually say?

**Hypothesis.** Your contract contains an IP clause broader than "deliverables under orders", no post-termination
non-compete, a confidentiality clause with a penalty, and a DORA annex added in 2025.

**Procedure.** Fill the matrix (exercise 02) from the signed contract and every annex, including any DORA annex
and any later amendment. Then compare with the lawyer's reading.

**Prediction (mine).** IP clause: broad ("all works created during the term"). Non-compete: during the term only,
scoped to banking or "services for competitors of the bank". Penalty: a fixed amount per breach of confidentiality.
DORA annex: present, with audit rights and a subcontracting ban.

| Clause | My prediction | What the contract says | Lawyer's view | Action |
| :-- | :-- | :-- | :-- | :-- |
| IP | broad | | | |
| Non-compete | during term, banking scope | | | |
| Penalties | fixed per breach | | | |
| DORA annex | present | | | |
| Availability | business hours | | | |

---

## 10. Pitfalls

**B6 · Relying on "that clause is probably void".**
*Symptom:* you build anyway because art. 41(3) makes the clause void in part. *Why it hurts:* you would have to
prove it in court, against a bank. *Remedy:* a carve-out in writing, or a lawyer's written opinion.

**B7 · Reading the contract but not the annexes.**
*Symptom:* the matrix is filled from the 2023 contract; the 2025 DORA annex is unread. *Remedy:* every annex,
every amendment, every policy the contract incorporates "by reference".

**B8 · Bank material in the startup.**
*Symptom:* "it's just a pattern I saw at work," a document template, a prompt. *Why it hurts:* trade secrets,
possibly bank secrecy, and penalties due without damage. *Remedy:* the rule of section 3 — nothing from the
bank, ever.

**B9 · Ignoring how the days are organised.**
*Symptom:* fixed hours, daily reports and instructions on method, paid per day — and no thought about it.
*Remedy:* know your indicators (section 6.3); a real separate business helps.

**B10 · Sending the letter before the lawyer reads the contract.**
*Symptom:* you ask the bank for a confirmation that the contract does not need, or phrase it badly.
*Remedy:* lawyer first, letter second (section 8).

---

## 11. Checkpoint

- [ ] `founder/02-clause-matrix.md` is filled with exact quotes from the contract **and** all annexes.
- [ ] Every penalty amount is written down.
- [ ] A lawyer has read the contract (or the meeting is booked, with a date).
- [ ] You have decided: letter now, letter later, or no letter needed — with a reason.
- [ ] You can name your three strongest and three weakest indicators in the reclassification table.

Sources for this part: [SOURCES.md](SOURCES.md), section "Part 02".
