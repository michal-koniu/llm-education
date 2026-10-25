# Part 03 · Clean IP: build so that nobody can claim your product

> **Goal of this part.** You set up a separation between the bank's work and the startup that would convince
> a sceptical lawyer: separate devices, accounts, time, data and AI tools, plus an evidence trail that
> shows when and how you built each piece. You decide what stays public in `llm-education` and what does
> not, and you prepare for the moment an investor asks: *"Who owns the code?"*
>
> **Time:** ~4 h to set up, then a habit · **Level:** ⭐⭐⭐ · **Produces:** `founder/03-separation.md`,
> `founder/03-ip-register.md`

> **Not legal advice.** The separation rules here are engineering hygiene based on the law summarised in
> part 02. A lawyer confirms whether they are enough for your contract.

---

## 0. The problem

Every investor, acquirer and serious customer will eventually ask who owns the product. The answer they need
is a **chain of title**: a clean, documented line from every author of every piece of code to the company. The
usual gaps, according to the IP due-diligence sources researched for this course (MaRS, Mondaq), are exactly
two: **code a founder wrote before the company existed**, and **code written by contractors**.

You have both, plus a third gap most founders do not have: a client — a bank — whose contract may contain a
broad IP clause (part 02). The cautionary tale every startup lawyer tells is *Mattel v. MGA* (the Bratz dolls):
the ownership of a multi-billion-dollar product turned on the wording of an assignment clause and on **when**
the designer had made the first drawings (Harvard JOLT summary). The defence is evidence, created at the time,
not memories reconstructed later.

---

## 1. The five separations

| Separation | Rule | Why |
| :-- | :-- | :-- |
| **Devices** | the startup is built only on your own machines (your rig, your own laptop). Never on the bank's laptop, VDI or cloud account | the bank's equipment and the DORA audit clause (part 02, §4) |
| **Accounts** | separate e-mail, GitHub organisation, cloud accounts, password manager vault, AI subscriptions — paid by you | logs and ownership of the accounts are evidence; the bank's AI tools may have their own terms on what you produce with them |
| **Time** | startup work outside the hours you bill or are available to the bank (part 01, §2) | "during the contract's working time" is a common hook in IP clauses and a reclassification indicator |
| **Data** | no bank data, documents, code, configuration, prompts, tickets or messages — in any form, ever | trade secrets (art. 11 UZNK), bank secrecy, the NDA (part 02, §3) |
| **Knowledge** | general skills are yours; the bank's specific solutions are not. If in doubt, rebuild from public sources and document which ones | independent creation is lawful (art. 11(7) UZNK); copying is not |

The fifth separation is the subtle one. You know how to build agents because you studied and built them —
the `llm-education` courses are public proof of that, dated by git. That knowledge is yours. A specific
internal design you saw at the bank is not, even if you could reproduce it from memory.

---

## 2. The evidence trail

Create evidence **while you work**, not afterwards:

| Evidence | How | Strength |
| :-- | :-- | :-- |
| **Git history** in your own organisation, with signed commits | `git config commit.gpgsign true` with your own key; commits on your own machines | strong for *when* and *by whom*, if the repository was never rewritten |
| **Design notes with dates** | an ADR (architecture decision record) per significant decision, as in the technical courses — in the product repository | shows independent reasoning and its sources |
| **Source list per component** | for each agent: which public papers, docs, open-source projects it is based on | proves independent creation (art. 11(7) UZNK) |
| **Time log** | the CSV from part 01, continued as a habit | shows startup work happened outside contract hours |
| **A certain date** for key documents | Polish law knows a "data pewna" (art. 81 of the Civil Code) — e.g. a notary's certification of the date; a **qualified electronic timestamp** under eIDAS is a common digital equivalent | very strong for the first design document and the IP register. *General knowledge, not from this course's research — confirm the method with your lawyer* |

Do the "certain date" once, at the start, for one document: the description of the product and the list of
everything you have built so far (the IP register, section 4). It costs little and it ends any argument about
what existed **before** a given date.

---

## 3. What stays public

`llm-education` is public under **CC BY 4.0** (lessons) and **MIT** (code). Those licences allow anyone —
including a competitor — to copy, modify and use the material **commercially**, with attribution. That is fine,
and it is valuable: the public repository is evidence of your competence and of *when* you knew what.

But from now on, decide deliberately what goes where:

| Public (`llm-education`) | Private (the product repository) |
| :-- | :-- |
| general courses, surveys, techniques, benchmarks | the agents for specific professions, their prompts and workflows |
| generic tools (e.g. this course's pricing calculator) | **the evaluation sets** built from professional documents — your quality moat |
| what helps your reputation and recruiting | integrations, installers, the box image, the update channel |
| | anything containing information about real customers |

A useful test: *would I be unhappy to see this in a competitor's product next month?* If yes, it is private.

And remember the licences you **receive**: Bielik is Apache 2.0 (`ai-business-asymmetries/02-OPPORTUNITIES.md`);
the repo itself warns to *"watch the licenses"* of PLLuM (`ai-assistants/04-POLAND-AND-SOVEREIGNTY.md`). Every
model and library inside the box goes into the IP register with its licence.

---

## 4. The IP register

`founder/03-ip-register.md` — one row per component of the product:

| Component | Author(s) | Created (from–to) | Where (device, account) | Based on (public sources) | Licence of dependencies | Transferred to | Document |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| letter-triage agent | me | 2026-11 → | own rig, own GitHub org | course_agentic_apps 03, 14; Bielik docs | Apache 2.0 (Bielik) | — (still mine) | — |
| box installer | me | | | | | | |
| Polish eval set, court letters | me + lawyer L01 (anonymised documents) | | | | | | **written agreement with L01?** |

Two rows deserve attention from the start:

- **Anyone else who contributes** — a freelancer, a friend who writes a script, a lawyer who designs an evaluation
  set. Without a written transfer listing the fields of exploitation (art. 41(2), art. 53), **they own their
  part**. Get the transfer signed when the work is delivered, not when an investor asks.
- **Documents from future customers** used for evaluation sets: they are covered by professional secrecy and
  GDPR. Use anonymised or public documents, with a written permission. That is the contracts course; for now,
  note in the register where every document came from.

---

## 5. When the company is formed

Today the IP belongs to you as a person (or your JDG). When you form a company — and you must, before taking
investment (part 06) — the IP must move into it **in writing**, with the fields of exploitation listed, as a
transfer, not a licence: investors expect the company to **own** the IP outright (research sources: Mondaq,
KS&K). The IP register is the attachment to that transfer.

How exactly to move it (sale, in-kind contribution, contribution in a simple joint-stock company (PSA), where
shares can be issued for work or services) has tax consequences. It belongs to the planned legal-form course.
What matters now: **if the register is complete and the evidence exists, the transfer is a formality. If not, it
is a negotiation.**

---

## 6. EXERCISE 03 — set up the separation

In `founder/03-separation.md`, write and then do:

1. The list of devices you use for the startup (and confirm none belongs to the bank).
2. The list of accounts: e-mail, GitHub organisation, cloud, AI subscriptions, domain — all in your name, paid
   by you.
3. Your commit-signing key and the confirmation that signing is on in the product repository.
4. The rule for time, copied from part 01, with the hours you will use.
5. The public/private split of section 3, applied to everything you plan to build in the next three months.
6. The first version of `founder/03-ip-register.md` — everything that exists today.
7. The decision on a "certain date" for the register and the product description, and the method your lawyer
   recommends.

---

## 7. ⭐ FIELD EXPERIMENT 03 — the hostile reviewer

**Hypothesis.** A reviewer who reads only your evidence trail (git history, IP register, time log, ADRs) cannot
find a component of the product whose origin is unclear.

**Procedure.** After one month of building, ask someone you trust — ideally a lawyer, otherwise a senior engineer
who does not know the project — to play an investor's lawyer. Give them read access to the evidence (not to bank
material, obviously). Ask them to list every component for which they cannot answer: *who wrote it, when, on what,
from which sources, and who owns it now?*

**Prediction (mine).** Two or three gaps: a helper script with no source note, a test document whose origin is not
recorded, and the first two weeks of commits made before signing was on.

| Gap found | Component | Why it is unclear | Fix | Fixed (date) |
| :-- | :-- | :-- | :-- | :-- |
| | | | | |

---

## 8. Pitfalls

**B11 · "Just testing it" on the bank's laptop.**
*Symptom:* the first prototype ran on the work machine "because it has the GPU / the VPN / the Copilot licence".
*Remedy:* nothing of the startup, not even a test, on the bank's equipment or accounts.

**B12 · The bank's AI tool writes your product.**
*Symptom:* a corporate Copilot or chat licence used for startup code. *Why it hurts:* account ownership, logs and
the tool's terms are under the bank's control. *Remedy:* your own subscriptions, paid by you.

**B13 · A contributor without a transfer.**
*Symptom:* a friend wrote the OCR pipeline "as a favour". *Remedy:* written transfer with fields of exploitation
at delivery (art. 53).

**B14 · Everything public by habit.**
*Symptom:* the evaluation sets and agent prompts pushed to the public repo with the courses. *Remedy:* the
public/private test of section 3.

**B15 · Rewriting history.**
*Symptom:* `git rebase` and force-push over months of startup commits "to clean up". *Why it hurts:* it destroys the
dates that are your evidence. *Remedy:* never rewrite published history of the product repository; squash only
feature branches before merging.

---

## 9. Checkpoint

- [ ] All five separations are in place and written down in `founder/03-separation.md`.
- [ ] Signed commits are on in the product repository.
- [ ] `founder/03-ip-register.md` lists every existing component, its sources and licences.
- [ ] You have decided what of your plans goes public and what stays private.
- [ ] Field experiment 03 is scheduled for one month from now.

Sources for this part: [SOURCES.md](SOURCES.md), section "Part 03".
