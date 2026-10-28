# AI business asymmetries

Where is AI adoption still low enough that a small team with agentic apps and **local open models** can build a
business before the incumbents catch up? I looked at 26 candidates across Poland, the EU and global markets: back
offices, regulated professions, public sector, compliance deadlines, industry and SME operations. For each one I asked
three questions: **is the work still done by hand, who already sells AI into it, and does running the model locally
help the sale?** Then I argued against every idea from five angles before scoring it.

My setup: a local rig with DeepSeek-V4-Flash-0731 (4 parallel slots), Claude Opus 5.5 as planner and reviewer, cheap
online models for overflow ([../cheap-free-models/README.md](../cheap-free-models/README.md)). I live in Poland, can
sell in Polish and English, and assume a bootstrapped small business (1-3 people, about 20,000 EUR). Facts are as of
14 Oct 2026. The previous course looked at income without a company
([../ai-income-asymmetries/README.md](../ai-income-asymmetries/README.md)); this one is about building one.

> **Not investment, legal or tax advice.** Markets, regulations and vendor features change monthly. Check again before
> acting.

## The short answer

- **The gap is real and measurable.** In 2025, 8.4% of Polish enterprises used AI against 20.0% in the EU, the
  second lowest after Romania (Eurostat). Polish small firms: 5.8% (EU 17.0%); Polish construction: 2.4% (EU 10.8%).
  Cost blocked 55.5% of the Polish firms that considered AI ([01-ADOPTION-GAPS.md](01-ADOPTION-GAPS.md) has the full
  data). The firms that still do the work by hand are the customers.
- **The best openings are where data cannot leave the building.** Nine of the top 15 have high local-model fit: law
  firms, municipal offices, clinics, NIS2 security documents, legacy source code, machine drawings, archives. Here
  "it runs on a box in your office, on an Apache-licensed Polish model" is the sales argument, not a technical detail.
- **Local does not win on token cost; it wins on the sale.** At Oct 2026 prices a cheap API is cheaper per token
  than a local box for most SME volumes ([03-LOCAL-FIRST.md](03-LOCAL-FIRST.md)). The money is in setup, workflows,
  updates and support, priced per office or per entity.
- **Dated deadlines create budgets.** NIS2 in Poland (KSC amendment in force 3 Apr 2026, obligations by 3 Apr 2027),
  the Machinery Regulation (20 Jan 2027), KSeF e-invoicing (2026) and the MDR transition force firms to buy help now.
- **Polish law and language are a moat, but a thin one.** Tender rules (Pzp), KNR cost norms, EPU court filings and
  Polish email are where global AI tools do not reach yet. Polish incumbents are moving: SaldeoSMART classifies KSeF
  invoices with AI, Docplanner's Noa writes doctors' notes, Gaius-Lex sells private legal AI, LEX bundles an AI chat.
  The window is 12-24 months, not forever.
- **No idea scored above 72 out of 100.** Every one survived the challenge only in a narrower form: one profession,
  two or three workflows, sold through a partner who already has the customers.

## The top 15

Score out of 100. Competition is how crowded the AI side of the market is today; local-model fit is how much running
open models on-site helps the sale.

| # | Opportunity | Score | Region | Competition | Local-model fit |
|---|---|---|---|---|---|
| 1 | [Private AI box for Polish professional offices](02-OPPORTUNITIES.md#1-private-ai-box-for-polish-professional-offices) | 72 | PL, then EU | medium | high |
| 2 | [On-prem document agent for Polish municipal offices](02-OPPORTUNITIES.md#2-on-prem-document-agent-for-polish-municipal-offices) | 71 | PL | low | high |
| 3 | [NIS2 / KSC compliance documentation agent for newly covered Polish entities](02-OPPORTUNITIES.md#3-nis2--ksc-compliance-documentation-agent-for-newly-covered-polish-entities) | 71 | PL (then CEE) | medium | high |
| 4 | [On-prem legacy code documentation and modernization for SMEs and regulated firms](02-OPPORTUNITIES.md#4-on-prem-legacy-code-documentation-and-modernization-for-smes-and-regulated-firms) | 70 | PL / EU | medium | high |
| 5 | [Tender desk agent for Polish SME bidders](02-OPPORTUNITIES.md#5-tender-desk-agent-for-polish-sme-bidders) | 70 | PL first, then EU (TED) | medium | medium |
| 6 | [On-prem legal assistant for small Polish law firms](02-OPPORTUNITIES.md#6-on-prem-legal-assistant-for-small-polish-law-firms) | 67 | PL | medium | high |
| 7 | [Freight forwarding back-office agent for Polish SME forwarders](02-OPPORTUNITIES.md#7-freight-forwarding-back-office-agent-for-polish-sme-forwarders) | 67 | PL (then EU) | medium | medium |
| 8 | [On-prem maintenance and field-service knowledge agent for industrial SMEs in CEE](02-OPPORTUNITIES.md#8-on-prem-maintenance-and-field-service-knowledge-agent-for-industrial-smes-in-cee) | 66 | PL / EU (CEE) | medium | high |
| 9 | [KSeF back-office agent for Polish accounting offices](02-OPPORTUNITIES.md#9-ksef-back-office-agent-for-polish-accounting-offices) | 65 | PL | high | high |
| 10 | [Receivables and EPU paperwork agent for Polish SMEs](02-OPPORTUNITIES.md#10-receivables-and-epu-paperwork-agent-for-polish-smes) | 64 | PL | medium | medium |
| 11 | [CE technical file agent for SME machinery and product manufacturers](02-OPPORTUNITIES.md#11-ce-technical-file-agent-for-sme-machinery-and-product-manufacturers) | 63 | PL (then EU) | medium | high |
| 12 | [Construction estimate and tender assistant for Polish contractors](02-OPPORTUNITIES.md#12-construction-estimate-and-tender-assistant-for-polish-contractors) | 63 | PL | medium | medium |
| 13 | [Local Polish medical scribe for private clinics](02-OPPORTUNITIES.md#13-local-polish-medical-scribe-for-private-clinics) | 61 | PL | medium | high |
| 14 | [On-site digitisation and search of paper archives](02-OPPORTUNITIES.md#14-on-site-digitisation-and-search-of-paper-archives) | 60 | PL / EU | medium | high |
| 15 | [Regulatory documentation agent for small medtech and pharma](02-OPPORTUNITIES.md#15-regulatory-documentation-agent-for-small-medtech-and-pharma-mdrivdr-tech-files-psurs-literature-screening) | 60 | EU | medium-high | medium |

Runners-up, below the cut but fully profiled:

| # | Opportunity | Score | Region | Competition | Local-model fit |
|---|---|---|---|---|---|
| 16 | [Polish phone and chat agent for local service businesses](02-OPPORTUNITIES.md#16-polish-phone-and-chat-agent-for-local-service-businesses) | 59 | PL | high | low |
| 17 | [Grant application co-pilot for Polish consultancies](02-OPPORTUNITIES.md#17-grant-application-co-pilot-for-polish-consultancies) | 58 | PL | medium | medium |
| 18 | [Polish tax interpretation and case-law research agent](02-OPPORTUNITIES.md#18-polish-tax-interpretation-and-case-law-research-agent) | 52 | PL | high | high |

**How to read the ranking.** The scores are close: 60 to 72 for the top 15. Treat the list as three groups, not a
strict order.

| Group | Opportunities | Why they cluster |
|---|---|---|
| Local-first by law or secrecy | 1, 2, 4, 6, 8, 13, 14 | Data cannot go to a US or Chinese cloud; on-site open models are the pitch |
| Deadline-driven compliance | 3, 9, 11, 15 | A dated legal obligation creates a budget now; the window closes after the deadline |
| Polish law and language moats | 5, 7, 10, 12 | Global AI tools do not know Pzp, KNR, EPU or Polish freight email; local players sell search, not agents |

## How I scored

| Letter | What it measures | Points |
|---|---|---|
| M | Market: number of buyers in PL/EU, what they pay today for the manual work, willingness to pay | 20 |
| G | Adoption gap: measured low AI use in this sector, size class or country, plus the share of manual work | 20 |
| C | Competition room: higher means fewer credible AI competitors and slow incumbents | 15 |
| L | Local-model fit: secrecy law, GDPR, volume cost or offline sites make local open models a selling point, and the models are good enough in the language needed | 15 |
| F | Feasibility for me: time to an MVP, access to domain knowledge, sales cycle, capital | 15 |
| R | Durability and risk: higher means the edge lasts 2+ years and liability is manageable | 15 |

Ties are broken by L (local fit), then G. Every profile shows its letter scores, so you can re-weight them.

## The challenge, across all 15

Each profile argues against itself from five angles. The same objections came back again and again:

| Angle | The recurring objection | What survives |
|---|---|---|
| Customer | "We already pay for LEX / Saldeo / our EZD vendor; why another tool?" | Sell an add-on that feeds the system they already use, not a replacement |
| Incumbent | Polish incumbents are shipping AI in 2026 (SaldeoSMART, Noa, Gaius-Lex, LEX AI chat) | Go where they show no AI yet (EZD vendors, KNR estimating, tender portals) or below their price |
| Frontier labs and big tech | A general chat model already drafts the text | The value is ingestion, Polish rules, checklists, integration and the human gate, not the draft |
| Regulator | Legal, medical, CE and regulatory work carries liability; medical tools can fall under MDR | Keep a named human signing everything; scope as "documentation support", never advice |
| Unit economics | Local boxes cost more per token than cheap APIs; support eats margin | Price per office or entity per year, standardise one box image, sell through partners (MSPs, integrators, bar chambers, accounting offices) |

**Founder fit is the hidden filter.** As a DevOps engineer I can build the box, the deployment and the security side
myself. Opportunities 1, 3 and 4 fit my background directly; most others need a domain partner (an estimator, a tax
adviser, a regulatory consultant, a forwarder) on day one.

## Where I would start

1. **Build one local stack** ([03-LOCAL-FIRST.md](03-LOCAL-FIRST.md)): an installable box image with a Polish-capable
   open model, document ingestion, an agent runner and an audit log, plus a hybrid route that redacts locally
   before any paid API call ([../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md](../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md)).
2. **Point it at two verticals with a deadline or a secrecy rule:** NIS2 documentation sold white-label through MSPs
   (deadline 3 Apr 2027) and a legacy-code X-ray sold through Polish software houses. Both match my skills.
3. **Talk to 10 buyers before writing workflows.** Every profile has a "How to start" and a kill criterion; use them.
4. **Keep a third option warm:** public tenders or municipal offices, through an integrator who already sells to them.

## Ideas that did not survive

| Candidate | Why it dropped |
|---|---|
| Housing community and property manager back office | Many tiny buyers on entrenched software; needs a domain partner |
| Real estate due diligence from land registers | Public data, so local models add little; register reports already sell for 12-35 PLN |
| Farm subsidy paperwork | The agency pre-fills forms and ODR advisers help for free; low willingness to pay |
| German tax advisor back office | DATEV dominates and selling there needs German-language sales |
| Transfer pricing documentation | Few buyers, Big Four own the liability, benchmark data is paid |
| CBAM and EUDR reporting | The 2025 simplification (50 t threshold) removed most SME importers; EUDR delayed again |
| European Accessibility Act audits | Saturated audit market, microenterprises exempt, no local-model edge |
| Cross-border marketplace listings | Saturated, not an adoption gap; frontier APIs win on multilingual copy |

Full notes with sources are at the end of [02-OPPORTUNITIES.md](02-OPPORTUNITIES.md).

## Files

| File | What is in it |
|---|---|
| [01-ADOPTION-GAPS.md](01-ADOPTION-GAPS.md) | The data: AI adoption by EU country, company size and sector, Poland in detail, global comparison, barriers, where AI is already saturated |
| [02-OPPORTUNITIES.md](02-OPPORTUNITIES.md) | 18 profiles: asymmetry, buyers, the agentic app, local vs paid split, competition table, the five-angle challenge, numbers, how to start, kill criteria; then the dropped ideas |
| [03-LOCAL-FIRST.md](03-LOCAL-FIRST.md) | Why buyers want local, open models good enough today, hardware tiers, cost vs API, deployment patterns, which opportunities are local-first |
| [SOURCES.md](SOURCES.md) | All sources, accessed 14 Oct 2026 |

**Research limits.** The web search budget for this session ran out early, so the research relies on pages fetched
directly: Eurostat, the Polish legal acts (ISAP and the Sejm ELI API), EU pages and vendor sites. Several figures are
marked "not found" rather than guessed, for example the number of Polish accounting offices and law firms, and the
prices of several Polish incumbents. Competitor tables name real companies, but AI depth and prices are only stated
where a source confirms them. Related courses: [../agent-harnesses/README.md](../agent-harnesses/README.md),
[../course_agentic_apps/17-HYBRID-AND-ROUTER.md](../course_agentic_apps/17-HYBRID-AND-ROUTER.md).
