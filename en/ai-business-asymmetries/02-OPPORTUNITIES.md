# The top 15 opportunities, profile by profile

Each profile follows the same shape: the asymmetry, who pays and how much, the agentic app, how the work splits
between local open models and paid APIs, a competition table, a challenge from five angles (customer, incumbent,
frontier labs and big tech, regulator, unit economics), numbers, how to start, risks and kill criteria. Facts are as of
14 Oct 2026. The scoring (M market 20, G adoption gap 20, C competition room 15, L local-model fit 15, F feasibility
15, R durability and risk 15) is explained in the [README](README.md#how-i-scored). The ideas that did not survive the
challenge are at the end.

**Read the challenge before the pitch.** Every idea here looks good in its first paragraph. The score is set after the
challenge, not before it.

---

## 1. Private AI box for Polish professional offices

**Region:** PL, then EU · **Buyers:** law, notary, tax-advisory, accounting and medical offices with 5-50 staff · **Revenue model:** setup + hardware margin + monthly maintenance licence · **Competition:** medium · **Local-model fit:** high · **Score: 72** (M14 G16 C9 L14 F11 R8)

> The strongest local-first idea in this set: sell a configured box plus 2-3 narrow agent workflows, not "a server with a chatbot".

**The asymmetry.** Poland is near the bottom of the EU for business AI use: 8.36% of enterprises used AI in 2025 against an EU average of 19.95%; only Romania was lower (Eurostat, 2025 data). Small firms lag everywhere (17% of small vs 55.03% of large EU enterprises, 2025). The barriers named by non-adopters fit an on-site offer exactly: lack of expertise 70.89%, legal uncertainty 52.52%, privacy and data protection 48.83% (Eurostat, 2025). Professional offices bound by secrecy (attorney, notary, tax adviser, medical) cannot casually paste client files into a US cloud chat, so their document work (summaries, letters, comparisons, registers) stays manual. The gap stays open while cloud vendors cannot offer "data never leaves the room" and while local hardware keeps getting cheaper.

**Who pays and how much.** Buyer counts for PL professional offices: not found in this research pass (GUS/chamber registers to be checked). Today they pay staff hours for drafting and review; exact spend not found. Price points to test: 25,000-60,000 PLN setup including hardware, 800-2,500 PLN per month for updates, monitoring and new workflows (my assumption, to be tested, not market data). Channel: bar and tax-adviser chambers, accounting-office associations, local IT service firms that already run these offices.

**The agentic app.**
1. Ingest: watch a shared folder or the document system; OCR scans locally.
2. Extract: parties, dates, amounts, case numbers into a local index (RAG over the office's own files).
3. Reason: workflow-specific agent (for example "summarise new court letter and propose deadline", "compare contract draft to template").
4. Draft: letter, summary or checklist in Polish.
5. Verify: second pass checks citations to source pages; flags low confidence.
6. Act: **human approval gate** before anything leaves the office or enters a calendar; full local audit log.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| OCR and extraction | Yes (Qwen-VL class or Bielik 11B v3) | No | Client data under professional secrecy |
| Polish drafting | Yes (Bielik-11B-v3.0-Instruct, Apache 2.0) | No | Polish quality, no data transfer |
| Hard reasoning on anonymised text | Optional | Yes, only with consent | Better quality on rare complex cases |
| Workflow building by the integrator | No | Yes | Developer productivity, no client data |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| NVIDIA DGX Spark and GB10 OEM boxes (Dell, HP, Lenovo, ASUS) | global platform | global | 128 GB desktop AI box, "up to 200B parameters" (vendor claim) | Hardware only | not found on vendor page (2026-10) |
| Microsoft 365 Copilot | global platform | global | Cloud assistant in Office | High, cloud only | not checked |
| Polish IT service and integrator firms | consultancy | PL | Servers, networks, some "private AI" projects | Low to medium | not found |
| Asseco and other large PL integrators | incumbent | PL | Enterprise AI and voicebot projects | Medium | not found |
| Legal-tech SaaS (cloud) | startup | PL/EU | Cloud legal assistants | Medium | not found |

Gap: hardware vendors ship boxes without Polish workflows; cloud tools fail the secrecy test; big integrators do not sell 30k PLN projects. Win on "installed, Polish, audited, maintained" for one profession first.

**Challenge from five angles.**
- **Customer:** small offices fear IT projects and may say "we already have Copilot". Answer: start with one paid workflow and a demo on their own anonymised files.
- **Incumbent:** local IT service firms own the relationship and can resell a DGX Spark. Answer: partner with them as the AI layer, revenue share.
- **Frontier labs and big tech:** EU data-boundary clouds and sovereign-cloud offers weaken the "never leaves" argument over 2-3 years.
- **Regulator:** GDPR and secrecy rules help; liability for wrong drafts stays with the professional, keep the human gate and logs.
- **Unit economics:** hardware margin is thin and support is labour heavy; profit must come from the monthly licence and repeatable workflows.

**After the challenge.** Survives as a vertical (one profession, 2-3 workflows) with IT-partner distribution. Generic "AI box for anyone" does not survive. Score stays near 70.

**Numbers.**
- 8.36% of PL enterprises used AI in 2025 vs 19.95% EU (Eurostat, 2025 data, *official statistics*).
- EU small enterprises 17% vs large 55.03% AI use (Eurostat, 2025).
- Barriers: expertise 70.89%, legal 52.52%, privacy 48.83% (Eurostat, 2025).
- Bielik-11B-v3.0-Instruct under Apache 2.0, base dated 2025-07-30 (Hugging Face model card, read 2026-10-14).
- PLLuM 2512 family (4B, 8B, 12B, 70B) on Hugging Face, updated mid-2026; licence not confirmed in this pass.
- DGX Spark 128 GB, "up to 200B parameters", 4 units "up to 700B" (*vendor claim*, read 2026-10-14).

**How to start.**
1. Weeks 1-4: one workflow (incoming letter triage for law or tax offices) on the reader's rig, Bielik + Qwen, local OCR.
2. Weeks 5-8: package on a single small box; write the data-protection note and audit log.
3. First 10 customers: two pilots via personal network, then chamber events and two IT service partners.
4. Pricing test: paid pilot 3,000-5,000 PLN, then setup + monthly; drop the hardware margin if it blocks sales.

**Risks and limitations.**
- On-site support load grows with each box.
- Open-model quality on long legal Polish texts must be measured, not assumed.
- Hardware prices and supply move fast.
- Professional liability if staff skip the approval gate.

**Kill criteria.** Stop if fewer than 3 paying pilots after 4 months of active selling, or if monthly support exceeds 30% of revenue.

**Sources:** [Eurostat: use of AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Bielik-11B-v3.0-Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [SpeakLeash on Hugging Face](https://huggingface.co/speakleash) · [PLLuM (CYFRAGOVPL)](https://huggingface.co/CYFRAGOVPL) · [NVIDIA DGX Spark](https://www.nvidia.com/en-us/products/workstations/dgx-spark/)

---

## 2. On-prem document agent for Polish municipal offices

**Region:** PL · **Buyers:** gminy, powiaty and their IT integrators · **Revenue model:** setup + yearly licence per office (box at the customer), sold through procurement or an integrator · **Competition:** low · **Local-model fit:** high · **Score: 71** (M13 G16 C11 L15 F7 R9)

> The strongest local-model case on this list: personal data and administrative files must stay in the office, the government already ships an Apache-licensed Polish model, and the document-system incumbents show no AI, but the public sales cycle is slow.

**The asymmetry.** Poland has 2,477 gminy (GUS TERYT count, not re-verified this session) plus powiaty and other offices, each handling public-information requests, citizen letters, administrative decisions and document registration by hand. Polish enterprise AI use was 8.4% in 2025 (Eurostat, 11 Dec 2025); a public-sector figure was not found. The two document-system incumbents we checked do not show AI: NASK's free EZD RP page lists digital chancellery, e-signatures and search with no AI (gov.pl, Oct 2026), and Madkom (SIDAS EZD, BIP) claims 1,200 implementations and 120,000 users with no AI on its homepage *(vendor claim, Oct 2026)*. The gap stays open because offices cannot send citizen files to a US cloud without a GDPR and data-location analysis, and EZD becomes mandatory only from 1 Jan 2029 at the earliest (Ministry of Digital Affairs, as reported in search results, Oct 2026), so the document-flow modernisation is still ahead.

**Who pays and how much.** About 2,500 municipal offices plus about 380 powiaty (count not re-verified). Spend today is clerk time; municipal clerk salary data not found this session. Price points to test: 15,000-30,000 PLN setup (box with GPU + install) plus 6,000-12,000 PLN per year. Below the 130,000 PLN Pzp threshold the office can buy without a full tender, which keeps the sale small and fast. Channel: existing local IT integrators and the vendors of municipal software as resellers, voivodeship meetings of municipal secretaries.

**The agentic app.**
1. Ingest: incoming e-mail, ePUAP/e-Doręczenia letters and scanned paper from the chancellery.
2. Extract: sender, case type, deadline (14 days for public-information requests), personal data present.
3. Reason: classify to the JRWA file plan, route to a department, find similar past cases and decisions.
4. Draft: reply to a public-information request, a decision template, anonymised version for BIP publication.
5. Verify: legal-basis citations checked against a local corpus of acts; personal data redaction check.
6. Act: **human approval gate**: a clerk signs every outgoing letter and decision; the agent only registers and drafts.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| OCR and extraction | local | no | Citizen personal data, must stay in the office |
| Classification and routing | PLLuM 12B or Bielik 11B | no | Polish administrative language, government model is a selling point |
| Reply and decision drafts | PLLuM or a larger local model | no | Legal effect and personal data |
| Anonymisation for BIP | local | no | GDPR, cannot leave the building |
| Legal corpus updates | local | paid API only on public law texts | Public texts can use a paid model offline from citizen data |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| EZD RP (NASK) | incumbent | PL | Free government document-management system | none on product page | free |
| Madkom SIDAS | incumbent | PL | EZD, BIP, municipal software, 1,200 implementations | none on homepage | not public |
| PLLuM (Ministry of Digital Affairs) | incumbent | PL | Open Polish models for public administration, v2.2 Dec 2025 | model only, not an app | Apache 2.0, free |
| Sputnik Software, Asseco, Rekord | incumbent | PL | Municipal finance and ERP software | not verified, sites not checked or not reachable | not public |
| Microsoft 365 Copilot | global platform | global | Assistant inside Office for offices on M365 | high, cloud | per-seat licence |
| Local IT integrators | consultancy | PL | Hardware, networks, EZD rollouts | low | project-based |

Searched on 14 Oct 2026 (Bing, Polish queries on municipal AI assistants) and found no Polish vendor selling an on-prem drafting agent for gminy; not exhaustive. Avoid fighting EZD vendors: plug in next to them as an add-on, or sell through them.

**Challenge from five angles.**
- **Customer:** Small gminy have tiny IT budgets and fear of being first; the secretary must trust drafts with legal effect.
- **Incumbent:** NASK can add PLLuM to EZD RP for free, which would kill a paid add-on in EZD RP offices. Madkom could do the same for its 1,200 sites.
- **Frontier labs and big tech:** Microsoft Copilot reaches offices already on M365, but cloud processing of citizen files is the objection that keeps the local box relevant.
- **Regulator:** AI Act and GDPR duties (DPIA, records, human oversight) for a public body; decisions with legal effect must stay human. This is a cost, but also the reason for on-prem.
- **Unit economics:** A GPU box per office plus on-site install and support is expensive at 2,500 small customers; one person can maybe support 30-50 sites.

**After the challenge.** Survives as a narrow product: public-information requests, anonymisation for BIP and registration, sold through integrators, priced under the procurement threshold. Score stays at about 71 but F is low; plan for 9-12 month sales cycles.

**Numbers.**
- 2,477 gminy (GUS TERYT, not re-verified).
- PLLuM 4B, 12B, 8B and 70B models, v2.2 dated Dec 2025; PLLuM-12B-instruct-2512 is Apache 2.0 on Mistral-Nemo base (Hugging Face, Oct 2026).
- Bielik 11B v3.0 Instruct, Apache 2.0, base released 30 Jul 2025 (Hugging Face).
- Madkom: 1,200 implementations, 120,000 users *(vendor claim)*.
- EZD obligation earliest 1 Jan 2029 *(third-party estimate, search snippet citing the ministry)*.
- Poland 8.4% enterprise AI use in 2025 (Eurostat).

**How to start.**
1. Weeks 1-4: on the local rig, a pipeline for public-information requests: classify, draft reply, anonymise, with PLLuM 12B and a small corpus of law.
2. Weeks 5-6: pilot with one friendly gmina on anonymised archive letters; measure clerk minutes saved.
3. Weeks 7-8: package as a small box (one GPU) with a web UI and audit log; DPIA template ready.
4. First 10 customers: 2-3 integrators who already serve 20+ gminy each; free pilot, paid from month 3.
5. Pricing test: setup + yearly licence vs flat monthly fee, both under 130,000 PLN in total.

**Risks and limitations.**
- NASK or Madkom ships PLLuM features at no cost.
- Slow public buying; budgets set a year ahead.
- On-site hardware support for a 1-3 person company.
- Liability and AI Act obligations for drafts with legal effect.

**Kill criteria.** Stop if no gmina or integrator signs a paid pilot within 6 months, or if EZD RP announces built-in PLLuM drafting.

**Sources:** [EZD RP](https://www.gov.pl/web/ezd-rp) · [Madkom](https://www.madkom.pl) · [PLLuM collection](https://huggingface.co/CYFRAGOVPL) · [PLLuM 12B instruct 2512](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512) · [Bielik 11B v3](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [Eurostat AI use 2025](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2) · [UZP reports](https://www.gov.pl/web/uzp/sprawozdania-o-funkcjonowaniu-systemu-zamowien-publicznych)

---

## 3. NIS2 / KSC compliance documentation agent for newly covered Polish entities

**Region:** PL (then CEE) · **Buyers:** medium and large firms newly classed as "podmiot kluczowy" or "podmiot ważny" under the amended KSC act, and the IT/MSP firms that serve them · **Revenue model:** setup fee per entity + annual subscription for document upkeep, incident-report drafting and audit prep · **Competition:** medium · **Local-model fit:** high · **Score: 71** (M15 G13 C9 L13 F12 R9)

> A hard, dated deadline (3 April 2027) plus documents nobody wants to send to a US cloud make this the most bankable compliance wave in Poland right now, but the window for the "first ISMS" sale is about 6 months.

**The asymmetry.** Poland transposed NIS2 late: the Commission sent Poland a reasoned opinion on 7 May 2025 for missing transposition (EC NIS transposition page, updated 1 Jul 2025). The amending act is dated 23 Jan 2026 (Dz.U. 2026 poz. 252) and entered into force on 3 April 2026 (Sejm ELI API). Entities that met the criteria on that day must implement the chapter 3 obligations (risk analysis, ISMS, policies, incident handling) within 12 months, so by 3 April 2027, and key entities must pass their first audit within 24 months (art. 33 of the amending act). Thousands of mid-sized firms in 18 sectors (threshold starts at medium enterprise, 50+ staff, per nis2.org.pl, legal status 10 Jul 2026) have never run an ISMS. Only 8.36% of Polish enterprises used any AI in 2025 against 19.95% in the EU (Eurostat, Dec 2025). The work today is consultants writing policy sets in Word and Excel risk registers. The gap stays open until the first audits in 2027-2028 settle what "good enough" looks like.

**Who pays and how much.** Number of covered entities in Poland: no official count found (searched gov.pl, biznes.gov.pl, nis2.org.pl). Fines give the budget anchor: key entities up to 10 M EUR or 2% of revenue, important entities up to 7 M EUR or 1.4% of revenue, and up to 100 M PLN for serious threats; the head of the entity ("kierownik") carries personal responsibility (art. 8c, art. 73 as amended). Consulting prices: nis2.org.pl publishes an offer page but no figures found; quote-based elsewhere. A price a 50-250 person firm accepts: assume 15,000-40,000 PLN for the first document pack and 1,000-3,000 PLN/month for upkeep (my hypothesis, to be tested). Channel: MSPs, IT integrators and ISO 27001 auditors who already have these clients and lack staff.

**The agentic app.**
1. Ingest: questionnaire, asset list, network diagram, existing ISO 9001/27001 documents, supplier list.
2. Extract: build an asset and supplier register, map services to the KSC sector annex and size test (entity qualification memo).
3. Reason: risk analysis per asset (threat catalogue mapped to art. 8 measures), gap list against the regulation and its implementing acts.
4. Draft: policy set (ISMS, incident handling, BCP, supply chain, access control), risk treatment plan, register entry data.
5. Verify: a cross-check agent cites the article for every requirement; a human consultant signs off. **Human gate:** management approval of policies and risk acceptance (legal liability of the head of entity).
6. Act: incident mode drafts the 24 h early warning and 72 h notification texts for CSIRT; a person submits them.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| Asset, network and supplier ingest | yes | no | network maps and vulnerabilities are the most sensitive data the firm has |
| Qualification memo | yes | optional review | legal reasoning in Polish, low volume |
| Risk analysis and policy drafting | yes | no | contains weaknesses; buyers will ask where it is processed |
| Template authoring (generic, no client data) | no | yes | best quality for the master templates, no secrets inside |
| Incident report drafting | yes | no | time-critical, offline-capable, contains live incident data |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| Vanta | global platform | global | dedicated NIS 2 product: prebuilt controls, 400+ integrations, vendor risk, policy templates | AI control mapping, policy drafting, policy chatbot *(vendor claim)* | demo, not public |
| Drata, Sprinto and similar GRC SaaS | global platform | global | compliance automation for ISO 27001 and SOC 2 | not verified in this run | not verified in this run |
| nis2.org.pl | consultancy | PL | KSC guides, FAQ, implementation offer | not found | "indicative prices" page, no figures found |
| Big Four and ISO 27001 auditors in PL | consultancy | PL | gap analysis, policy packs, audits | manual | day rates, not public |
| Polish MSPs and integrators | incumbent | PL | security services bundled with NIS2 packs | not found | not found |

Vanta already ships NIS 2, so "no AI competitor" is false. The global GRC platforms are built around cloud integrations and the EU directive, not the Polish KSC registry, Polish CSIRT forms and Polish-language policies. Beat them on Polish legal mapping and on-prem processing; sell through MSPs rather than against them.

**Challenge from five angles.**
- **Customer:** many firms will buy the cheapest template pack, or ignore it until a fine lands; the manager wants a consultant's signature, not software.
- **Incumbent:** MSPs and auditors can buy the same open models and build this; Vanta or Drata may add a KSC framework mapping.
- **Frontier labs and big tech:** a general assistant can write a decent policy draft today; the moat is the Polish-specific mapping, registry data and audit evidence, not the drafting.
- **Regulator:** implementing regulations may change requirements; the tool must not claim "compliance", only evidence and drafts reviewed by a qualified person.
- **Unit economics:** the first-pack sale peaks before April 2027; after that, recurring revenue depends on audits, incident handling and supplier assessments.

**After the challenge.** Survives as a white-label tool for MSPs and ISO auditors, run on a box at the MSP or the client, priced per entity per year. Drop the "replace the consultant" pitch. R stays 9 because of the post-deadline cliff.

**Numbers.**
- Act of 23 Jan 2026 amending KSC, Dz.U. 2026 poz. 252, in force 3 Apr 2026 (Sejm ELI API, read 14 Oct 2026).
- Obligations within 12 months, first audit of key entities within 24 months (art. 33 of the act).
- Registration application within 6 months of meeting the criteria (art. 7c), early warning 24 h, notification 72 h.
- Fines: key up to 10 M EUR / 2%, important up to 7 M EUR / 1.4%, up to 100 M PLN in serious cases (amended art. 73).
- Poland 8.36% of enterprises using AI vs EU 19.95% in 2025 (Eurostat, Dec 2025).
- Number of covered entities in Poland: not found.

**How to start.**
1. Weeks 1-3: KSC requirement map (article to control to document), Polish template set, qualification test.
2. Weeks 3-6: local pipeline on the rig with Bielik or Qwen for drafting and a citation checker; one real pilot via an ISO auditor.
3. Weeks 6-8: incident report drafter and supplier questionnaire module.
4. First 10 customers: 3-5 MSPs or auditors in Poland, each bringing 2-5 entities.
5. Pricing test: 990 vs 2,490 PLN per entity per month for MSPs; fixed first pack at 9,900 PLN.

**Risks and limitations.**
- Liability if a drafted policy misses a requirement; contracts must keep the qualified human as author.
- Demand spike before 3 April 2027, then a slowdown.
- Implementing regulations and the national cybersecurity authority guidance may change templates.
- MSP channel takes margin and may copy the product.

**Kill criteria.** Stop if fewer than 3 MSPs or auditors pay for a pilot by end of January 2027.

**Sources:** [Dz.U. 2026 poz. 252 via Sejm ELI API](https://api.sejm.gov.pl/eli/acts/DU/2026/252/text.pdf) · [EC NIS2 transposition](https://digital-strategy.ec.europa.eu/en/policies/nis-transposition) · [nis2.org.pl FAQ](https://nis2.org.pl/faq-nis2) · [Vanta NIS 2](https://www.vanta.com/products/nis2) · [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

---

## 4. On-prem legacy code documentation and modernization for SMEs and regulated firms

**Region:** PL / EU · **Buyers:** CTOs and IT heads of SMEs, cooperative banks, regional insurers, municipal utilities running Delphi, Clarion, Visual FoxPro, old PHP or COBOL systems · **Revenue model:** fixed-price assessment + per-codebase documentation package + optional on-prem box licence · **Competition:** medium · **Local-model fit:** high · **Score: 70** (M12 G15 C11 L14 F11 R7)

> Strong local-first fit: the code cannot leave the building, the big modernization platforms target mainframes and the Fortune 500, and the mid-market long tail of Delphi/FoxPro is unserved, but AWS Transform being free sets the price anchor for the COBOL end.

**The asymmetry.** Only 8.36% of Polish enterprises used AI in 2025 against 19.95% in the EU, and 17% of small firms EU-wide (Eurostat, 2025). The systems in scope (inventory, billing, ERP add-ons written in Delphi, Clarion, FoxPro, PHP 5) were built by people who are retiring; documentation is usually the code itself. Mainframe-scale buyers already have AI tools (AWS Transform, IBM watsonx Code Assistant for Z, Mechanical Orchard), but those target COBOL/PL/I on mainframes and very large customers. Below that tier the work is still done by hand by software houses at day rates. The gap stays open while hyperscaler tools ignore 4GL/desktop stacks and while banks and insurers forbid sending source code to a public API.

**Who pays and how much.** Number of SMEs and cooperative banks still running Delphi/FoxPro/Clarion in PL/EU: not found (no census of legacy stacks exists). Proxy buyers: cooperative banks, regional insurers, utilities, manufacturers with in-house ERP. What they pay today: software-house day rates for reverse engineering (rate not found in a public source for this session). Price points to test: 3,000-8,000 EUR fixed-price "codebase X-ray" (architecture map, data dictionary, business-rule catalogue, test inventory), then 1,000-3,000 EUR per month during a migration. Channel: direct LinkedIn outreach to IT heads, partnerships with Polish software houses that sell the rewrite and lack the analysis capacity.

**The agentic app.**
1. Ingest: repo or file-share snapshot copied onto a box at the customer (no outbound network); parse with tree-sitter or language-specific parsers where they exist, fall back to chunked raw text for Clarion/FoxPro.
2. Extract: call graph, DB schema, forms, SQL embedded in code, configuration and batch jobs.
3. Reason: per-module agent writes purpose, inputs/outputs, business rules, dead-code flags; a second agent cross-checks claims against the call graph.
4. Draft: architecture document, data dictionary, business-rule catalogue in Polish or English, characterization test proposals.
5. Verify: generated tests run against the legacy system where it can be executed; unverifiable claims marked "unverified".
6. Act: human approval gate before any document is delivered as "as-is truth" or any rewritten module replaces production code.

**Local vs paid split.**
| Step | Local open model | Paid API | Why |
| --- | --- | --- | --- |
| Parsing and chunking | Not needed (deterministic tools) | Not needed | Code parsers are cheaper and exact |
| Per-module summaries | Yes, on the customer box | No | Source code is the confidential asset |
| Cross-module architecture reasoning | Yes by default | Only on sanitized summaries if the customer signs off | Long-context reasoning is stronger in frontier models |
| Polish documentation writing | Yes (Bielik 11B v3 or a multilingual model) | Optional | Language quality is good enough for technical prose |
| Rewrite proposals | Yes | Optional, with sanitized code | Rewrite quality matters but code may not leave |

**Competition.**
| Competitor | Type | Region | What it ships | AI depth | Price |
| --- | --- | --- | --- | --- | --- |
| AWS Transform | global platform | global | Agents for mainframe, Windows/.NET and VMware modernization | Deep, agentic | Mainframe agent free, custom transformation agent 0.035 USD per agent-minute (pricing page, Oct 2026) |
| IBM watsonx Code Assistant for Z | global platform | global | COBOL and PL/I understanding and COBOL-to-Java transformation | Deep | Not public |
| Mechanical Orchard (Imogen) | startup | US / global | Rewrites mainframe systems to cloud code with automated verification, targets Fortune 20-500 | Deep | Not public, free proof of concept |
| GitHub Copilot and Claude Code style assistants | global platform | global | General code assistants usable on any language | Medium for 4GL stacks | Per seat, cloud |
| Polish software houses doing rewrites | consultancy | PL | Manual analysis plus rewrite projects | Low to medium | Day rates, not public |
| Big consultancies (Accenture, Capgemini, Deloitte) | consultancy | EU | Modernization programmes with their own AI accelerators | Medium | Programme pricing, not public |

The gap: mid-market, non-mainframe 4GL stacks, on-prem only, Polish-language output, fixed price. Avoid the COBOL mainframe tier where AWS is free and IBM owns the platform.

**Challenge from five angles.**
- **Customer:** "We will do the rewrite one day" is a decade-old plan; documentation alone is easy to postpone. The trigger is usually a retiring developer or an audit finding, so sales must find those moments.
- **Incumbent:** The original vendor or local software house can add an LLM to its own analysis. Partnering with them (sell the X-ray, they sell the rewrite) turns the threat into a channel.
- **Frontier labs and big tech:** Coding agents get better every quarter and work on any language, so a customer with an approved cloud policy can do much of this alone. Only the "cannot leave the building" segment is defensible.
- **Regulator:** Banks and insurers fall under DORA and outsourcing rules; a box at the customer with no outbound network avoids most third-party-risk paperwork, which is a selling point, not a blocker.
- **Unit economics:** Each codebase is unique; parser work for Clarion or FoxPro is per-language one-off effort. Fixed-price packages must be scoped by lines of code to avoid losing money on spaghetti systems.

**After the challenge.** Survives as a niche: on-prem "codebase X-ray" for non-mainframe legacy stacks in regulated or secretive SMEs, sold through Polish software houses. Score drops on durability (R7) because coding agents commoditize generic understanding.

**Numbers.**
- EU enterprises using AI: 19.95% in 2025; small 17%, medium 30.36%, large 55.03% (Eurostat, 2025 data).
- Poland: 8.36% of enterprises used AI in 2025 (Eurostat, 2025 data).
- AWS Transform: mainframe, Windows and VMware agents at no cost; custom transformation agent 0.035 USD per agent-minute (AWS pricing page, read 14 Oct 2026) *(vendor claim)*.
- Mechanical Orchard: modernization cut from about 18 months to about 5 months *(vendor claim, website read 14 Oct 2026)*.
- Count of Delphi/FoxPro/Clarion systems in PL/EU: not found.

**How to start.**
1. Weeks 1-4: build the X-ray pipeline for old PHP and Delphi (best parser support) on the local rig; test on public open-source legacy repos.
2. Weeks 5-8: package as an air-gapped appliance (one GPU workstation or the customer's server) with a written data-handling statement.
3. First 10 customers: 3 Polish software houses as resellers, 7 direct (cooperative banks, regional manufacturers) via LinkedIn and local IT meetups.
4. Pricing test: offer the same package at 3,000 and 6,000 EUR to comparable prospects; track close rate and hours spent.

**Risks and limitations.**
- Hallucinated business rules in a document labelled "as-is" can mislead a migration; every claim needs a code reference.
- 4GL parsers are weak or missing; quality on Clarion/FoxPro may lag PHP and Delphi.
- Hardware cost and support of a box at the customer eat into margin on small deals.
- Long sales cycles in banks (security reviews) even when nothing leaves the building.

**Kill criteria.** Stop if after 6 months fewer than 3 paid X-rays are sold or delivery takes more than 2x the quoted hours on average.

**Sources:** [Eurostat: Use of AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [AWS Transform pricing](https://aws.amazon.com/transform/pricing/) · [IBM watsonx Code Assistant for Z](https://www.ibm.com/products/watsonx-code-assistant-z/pricing) · [Mechanical Orchard](https://www.mechanical-orchard.com/) · [SpeakLeash Bielik models](https://huggingface.co/speakleash)

---

## 5. Tender desk agent for Polish SME bidders

**Region:** PL first, then EU (TED) · **Buyers:** SME contractors that bid in public tenders (construction, supplies, services) and small tender-office consultancies · **Revenue model:** subscription per company + per-tender "SWZ pack" fee · **Competition:** medium · **Local-model fit:** medium · **Score: 70** (M17 G14 C9 L9 F12 R9)

> A real, large, paperwork-heavy market where Polish tender portals still sell search plus e-mail alerts, so an agent that reads the SWZ and builds the compliance checklist has a 1-2 year window.

**The asymmetry.** Polish public procurement under the Pzp law was worth about 330.4 bn PLN in 2024 (9.07% of GDP), across about 153,000 awarded contracts, with 130,002 notices in the BZP bulletin and 31,940 Polish notices in TED (UZP report for 2024, published 2025). SMEs submitted 95% of offers in sub-threshold works tenders and 84-85% in supplies and services. Every one of those offers means reading an SWZ (tender specification), forms (JEDZ/ESPD, declarations), contract terms and Q&A changes by hand. Polish enterprise AI use was 8.4% in 2025, among the lowest in the EU (Eurostat, 11 Dec 2025). The largest Polish tender database we checked, Oferent, sells search and alerts with no AI features on its price page (14 Oct 2026). The gap exists because the incumbents are publishers and aggregators, not software companies, and the work is legal-Polish text.

**Who pays and how much.** About 52,000 contractors won sub-threshold contracts in 2024 (UZP), which is a floor for active bidders. They already pay for tender databases: Oferent 900 PLN per quarter or 2,000 PLN per year (vendor price page, Oct 2026). The manual cost is a bid specialist's days per offer; salaries for that role not found this session. Price points to test: 249-499 PLN per month per company, or 99-199 PLN per analysed tender. Channel: direct outreach to repeat bidders found in BZP award notices (public data), regional construction associations, tender consultants as resellers.

**The agentic app.**
1. Ingest: poll e-Zamówienia/BZP and TED notices, download SWZ packages and later modifications.
2. Extract: conditions of participation, deadlines, wadium (bid bond), required documents, evaluation criteria, contract penalties.
3. Reason: bid/no-bid score against the company profile (turnover, references, certificates); flag risky clauses.
4. Draft: compliance checklist, list of documents, questions to the buyer, first draft of declarations and the offer form.
5. Verify: second pass cross-checks every checklist line against the cited SWZ paragraph; diff on SWZ changes.
6. Act: **human approval gate** before anything is signed or submitted; the agent never signs or files the offer.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| Notice triage and classification | Bielik 11B v3 or PLLuM 12B | no | High volume, short Polish text, cost per notice near zero |
| SWZ extraction to fields | DeepSeek-V4-Flash on the rig | fallback for long scanned PDFs | Bulk work; tender docs are public, so secrecy is not the driver |
| Risk clause reasoning | local first | Claude for hard contracts | Quality matters where a missed clause costs a bond |
| Offer draft with company data | local | optional | Company financials and pricing stay with the bidder |
| Verification pass | local | spot checks | Cheap second opinion, citations required |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| Oferent | incumbent | PL | Tender database since 2007, alerts, results | none on price page | 2,000 PLN per year |
| Portal ZP (Pressinfo) | incumbent | PL | Tender search, premium portal, webinars on AI for SWZ | content about AI, no SWZ agent seen | on request, 14-day trial |
| Biznes-Polska | incumbent | PL | Daily tender updates, B2B offers | not verified | not checked |
| Tendium | startup | Sweden, Norway, Finland | AI tender summaries, BidFlow, writing assistant | high | from 125 EUR per month |
| Stotles | startup | UK | AI notice summaries, bid/no-bid reports, drafting co-pilot | high | Bid Studio from 990 GBP per month |
| Brainial | startup | EU (NL, DE, SV) | Document analysis, risk flags, proposal writing | high | not public |
| ChatGPT or Copilot | global platform | global | General chat over uploaded SWZ | generic | consumer and business plans |

Searched on 14 Oct 2026 for a Polish product that analyses SWZ with AI (Bing, Polish queries): results showed portals only; tendersguru.pl did not resolve. Not exhaustive. The gap: Nordic, UK and Dutch AI tender tools have not localised for Pzp and Polish forms; Polish portals have not shipped agents. Win on Pzp-specific checklists and price below 500 PLN per month.

**Challenge from five angles.**
- **Customer:** Small builders buy on price and trust; many will paste the SWZ into ChatGPT for free. You must show a missed clause or a lost bond that the agent would have caught.
- **Incumbent:** Oferent and Pressinfo own the traffic and the alerts; bolting an LLM summary onto their listing is a quarter of work for them. Their slowness so far is the only moat.
- **Frontier labs and big tech:** Generic models already summarise PDFs well; the value must sit in the Pzp rule set, the company profile and the deadline workflow, not the summary.
- **Regulator:** Low risk, since tender documents are public. Liability risk if a checklist misses a required document and the offer is rejected: terms must make the human the signer.
- **Unit economics:** Long SWZ packs (hundreds of pages) make paid API costs bite at low prices; the local rig makes per-tender cost close to zero, which is the real reason to run local.

**After the challenge.** Survives as a niche: Pzp compliance checklist plus bid/no-bid for construction and supply SMEs, local-first for cost, sold through tender consultants. Score stays around 70, C is the weak point.

**Numbers.**
- 330.4 bn PLN Pzp procurement in 2024, 9.07% of GDP; about 153,000 contracts (UZP report 2024).
- 130,002 BZP notices and 31,940 Polish TED notices in 2024 (UZP report 2024).
- Average 2.89 offers per sub-threshold tender in 2024; SMEs 95% of offers in sub-threshold works (UZP report 2024).
- About 52,000 contractors won sub-threshold contracts in 2024 (UZP report 2024).
- Poland: 8.4% of enterprises (10+ staff) used AI in 2025 (Eurostat, 11 Dec 2025).
- Oferent 2,000 PLN per year, no AI listed *(vendor claim, Oct 2026)*; Tendium from 125 EUR per month *(vendor claim)*; Stotles Bid Studio from 990 GBP per month *(vendor claim)*.

**How to start.**
1. Weeks 1-4: pipeline for one CPV family (road and building works), BZP ingest, SWZ to checklist JSON, citations per line.
2. Weeks 5-6: test on 30 past tenders with known outcomes; measure missed requirements.
3. Weeks 7-8: web app with company profile and deadline calendar; human sign-off screen.
4. First 10 customers: contractors who lost an offer for formal reasons (visible in award notices), plus 2-3 tender consultants as resellers.
5. Pricing test: 149 PLN per tender vs 399 PLN per month, A/B across the first 20 leads.

**Risks and limitations.**
- Incumbent portals add AI summaries and bundle them into the existing 2,000 PLN subscription.
- Liability for a missed requirement; needs clear terms and visible citations.
- Scanned and badly structured SWZ files need OCR; quality varies.
- SME willingness to pay is low and churn is seasonal.

**Kill criteria.** Stop if fewer than 5 of the first 30 demo companies pay after a 4-week trial, or if Oferent or Pressinfo ship SWZ checklists at no extra charge.

**Sources:** [UZP report 2024](https://www.gov.pl/attachment/b61cce3a-f71c-4271-be11-d7eaa1a03f76) · [UZP reports index](https://www.gov.pl/web/uzp/sprawozdania-o-funkcjonowaniu-systemu-zamowien-publicznych) · [Eurostat AI use 2025](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2) · [Oferent price list](https://www.oferent.com.pl/cennik) · [Portal ZP](https://portalzp.pl) · [Tendium pricing](https://www.tendium.com/pricing) · [Stotles pricing](https://www.stotles.com/pricing) · [Brainial](https://www.brainial.com) · [Bielik 11B v3](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [PLLuM 12B instruct](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512)

---

## 6. On-prem legal assistant for small Polish law firms

**Region:** PL · **Buyers:** small kancelarie of adwokaci and radcowie prawni (1-15 lawyers) · **Revenue model:** setup + on-site box + monthly licence · **Competition:** medium · **Local-model fit:** high · **Score: 67** (M14 G13 C8 L13 F11 R8)

> Real but narrowing gap: sell a secrecy-first box plus Polish case-law workflows to small firms before the publishers' AI and Gaius-Lex reach them, and expect to compete on service, not on the model.

**The asymmetry.** Poland is near the bottom of EU AI adoption: 8.36% of Polish enterprises used AI in 2025 against 19.95% in the EU, and only 17% of small enterprises EU-wide did (Eurostat, published Dec 2025). Small firms still pay associates and trainees (aplikanci) to read judgments, compare contract versions and draft routine pleadings by hand. The gap exists because of professional secrecy (tajemnica adwokacka and tajemnica radcowska are statutory duties), distrust of US cloud tools, and Polish-language case law that global tools cover poorly. The bar is now actively discussing AI: the KIRP site lists "Rekomendacje dotyczące korzystania z AI" and a June 2026 conference on AI, ethics and European technological sovereignty (KIRP site, fetched Oct 2026). Expect the window to stay open 1-2 years for small firms: the publishers sell AI to firms that already pay for LEX or Legalis, and big firms buy Harvey or Legora first.

**Who pays and how much.** Buyers: the thousands of small Polish firms run by adwokaci and radcowie prawni (exact counts not found in this run; the bar registers publish them). They already pay a subscription for LEX (Wolters Kluwer) or Legalis (C.H.Beck); prices are quote-based and were not found publicly. A realistic offer: setup 6,000-12,000 PLN plus 600-1,500 PLN per month for a 3-10 lawyer firm (my price hypothesis, to test). Channel: regional bar chambers (izby), legal-tech meetups, IT firms that already serve law offices, and a free webinar on "AI and secrecy" built on the KIRP recommendations.

**The agentic app.**
1. Ingest: case files, contracts and correspondence from a firm share or DMS folder; judgments from the SAOS public REST API (JSON) and court portals.
2. Extract: parties, dates, deadlines, claims, clauses, cited articles, into a local index.
3. Reason: find similar judgments and contrary lines of case law; flag risky or missing clauses against the firm's own templates.
4. Draft: memo, clause redlines, a first draft of a pleading or a letter, with every citation linked to its source.
5. Verify: a second pass checks that each cited judgment and article exists and says what the draft claims.
6. Act: **human approval gate**: nothing leaves the firm until a lawyer signs off; no filing, no client email without review.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| Ingest and OCR of client files | yes | no | client data under professional secrecy |
| Extraction and indexing | yes (Bielik-11B v3, Qwen) | no | volume, secrecy |
| Case-law retrieval on public judgments | yes | optional | judgments are public, so a frontier model is allowed here |
| Drafting on client facts | yes | only with anonymised input | secrecy and GDPR |
| Citation check | yes | no | deterministic lookup plus small model |
| Template building and prompt design | no | yes (frontier model at build time) | no client data involved |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| Gaius-Lex (Gaius Vault) | startup | PL | private AI for legal teams: contract review, precedent search, correspondence, with on-prem and hybrid deployment | high | plans Lite, Standard, Pro, Edu; 7-day trial; amounts not visible |
| LEX (Wolters Kluwer Polska) | incumbent | PL | legal information system with LEX Navigator; AI features not confirmed in this run | medium (not verified) | quote-based, not found |
| Legalis (C.H.Beck) | incumbent | PL | commentaries, case law, templates; AI assistant not confirmed in this run | medium (not verified) | quote-based, not found |
| Harvey | global platform | global | legal AI platform, 3,500+ organisations in 85+ countries (vendor claim) | high | demo only, not public |
| Legora | global platform | EU (Sweden) | agentic legal OS, Word and Outlook add-ins | high | demo only, not public |
| SAOS | public database | PL | free court-judgment database with a public API | none (data source) | free |

Gap: Harvey and Legora target large firms and are cloud SaaS; the publishers lock AI into their own content; Gaius-Lex is the direct rival with on-prem already. Beat them on a physical box in the office, fixed price, local Polish service, and integration with the firm's own files, or partner with a publisher for content.

**Challenge from five angles.**
- **Customer:** small firms are price-sensitive and conservative; many will say "ChatGPT is enough" or "LEX will add it". Partners must trust a one-person vendor with client files.
- **Incumbent:** Wolters Kluwer and C.H.Beck own the commentaries and the customer relationship; once their AI is good, a solo vendor cannot match the content.
- **Frontier labs and big tech:** Copilot in Word and general chat models get better at Polish every quarter; secrecy is the only moat they do not cover for small firms.
- **Regulator:** bar recommendations on AI may tighten (or relax) the rules; liability for a wrong citation stays with the lawyer, but a vendor error is a reputational risk.
- **Unit economics:** hardware per customer plus on-site support costs time; at 1,000 PLN per month you need 40+ firms to replace a salary.

**After the challenge.** Survives as a niche: "secrecy-first box plus SAOS case-law workflows" for 3-15 lawyer firms, sold through bar chambers and IT integrators. Do not compete on commentary content; integrate with the publisher the firm already pays. Score stays 67 with a real risk that Gaius-Lex or a publisher closes the gap.

**Numbers.**
- EU enterprises using AI: 19.95% in 2025, Poland 8.36% (Eurostat, Dec 2025).
- Small EU enterprises using AI: 17%; large: 55.03% (Eurostat, 2025).
- Harvey: 3,500+ legal organisations, 200,000+ professionals, 85+ countries, $15.5 billion valuation *(vendor claim, Oct 2026)*.
- Gaius-Lex offers on-prem and hybrid deployment and four plans *(vendor claim, Oct 2026)*.
- Bielik-11B-v3.0-Instruct: Apache 2.0 licence, trained on 32 European languages with emphasis on Polish (Hugging Face model card, Oct 2026).
- Number of adwokaci and radcowie prawni: not found in this run.

**How to start.**
1. Weeks 1-3: pipeline over SAOS judgments plus one contract-review workflow, running on the local rig with Bielik and Qwen.
2. Weeks 4-6: pack it into a single-GPU office box with encrypted storage and an audit log; write a one-page "secrecy and GDPR" memo mapped to the KIRP recommendations.
3. Weeks 6-8: pilot with 3 firms for free in exchange for feedback and a quote.
4. First 10 customers: bar chamber webinars, legal-tech meetups, two IT integrators serving law offices.
5. Pricing test: compare setup + 900 PLN per month against a higher tier with case-law alerts.

**Risks and limitations.**
- Gaius-Lex already sells the same positioning.
- Hallucinated citations: a single fake judgment in a pleading ends the relationship.
- Hardware support on site does not scale for a 1-3 person company.
- Polish legal reasoning of 11B-30B local models may be too weak for drafting; keep them on extraction and retrieval.
- Long sales cycle with partners who rarely buy software.

**Kill criteria.** Stop if fewer than 3 of 10 pilot firms convert to paid within 4 months, or if a publisher ships on-prem AI inside its subscription.

**Sources:** [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Gaius-Lex](https://gaius-lex.pl/) · [Gaius-Lex pricing](https://gaius-lex.pl/cennik) · [KIRP AI search](https://kirp.pl/?s=sztuczna+inteligencja) · [Harvey](https://www.harvey.ai/) · [Legora](https://legora.com/) · [SAOS API](https://www.saos.org.pl/help/index.php/dokumentacja-api) · [Bielik-11B-v3.0-Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct)

---

## 7. Freight forwarding back-office agent for Polish SME forwarders

**Region:** PL (then EU) · **Buyers:** small and mid-sized Polish forwarders, carriers with a forwarding desk, customs agencies · **Revenue model:** subscription per desk + per processed order or declaration · **Competition:** medium · **Local-model fit:** medium · **Score: 67** (M16 G14 C8 L10 F10 R9)

> Poland is the EU's biggest road haulier and its forwarding desks still retype emails into TMS and customs forms; the money is real, but Digicust, Raft and Trans.eu are already moving in, so win on small Polish desks and Polish-language mail.

**The asymmetry.** Poland carried 20.2% of all EU road freight tonne-km in 2025, ahead of Germany (14.7%) and Spain (14.5%) (Eurostat, Jul 2026). Polish firms are among the slowest AI adopters: 8.36% of enterprises used AI in 2025 vs 19.95% EU, and only 17% of small firms EU-wide (Eurostat, Dec 2025). Forwarders receive orders as free-text emails and PDFs in Polish, German, English and Ukrainian, retype them into a TMS, build CMR documents, check carriers on exchanges and, for non-EU legs, prepare customs declarations. Trans.eu itself advertises reducing manual order handling "by up to 75%" *(vendor claim)*, which confirms the manual baseline. The gap stays open in the long tail of 1-20 person forwarders that cannot buy enterprise tools.

**Who pays and how much.** Number of Polish forwarders and customs agencies: not found in this run (GUS business register counts not fetched). Spend today: dispatcher and customs clerk salaries; Digicust's customer ZLS reports declaration time falling from 3-4 hours to 10-15 minutes *(vendor claim)*, which gives the size of the manual cost. A price a 5-desk forwarder accepts: assume 300-800 PLN per desk per month or 2-5 PLN per processed order (my hypothesis). Channel: TMS vendors, the Trans.eu ecosystem (API), freight associations, LinkedIn groups of dispatchers.

**The agentic app.**
1. Ingest: shared order mailbox, PDFs, WhatsApp exports, rate confirmations.
2. Extract: load and unload places, dates, goods, weight, ADR, price, references; normalise addresses.
3. Reason: match to customer, check carrier (VAT status, licence, insurance, exchange rating), flag fraud signs (new domain, changed bank account).
4. Draft: TMS order, carrier order, CMR data, customs declaration data with HS code proposal.
5. Verify: rule checks plus a second model pass on numbers; **human gate** for price, carrier choice, bank details and every customs submission (legal effect).
6. Act: push to TMS and exchange via API; the declarant files in PUESC.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| Email and PDF extraction | yes | fallback on hard scans | volume is high, cost per order matters |
| Multilingual normalisation (PL, DE, EN, UA) | yes | no | open models handle these languages well enough |
| Carrier fraud reasoning | yes | optional | needs client history, stays local |
| HS code proposal | partly | yes | hard reasoning, low volume, no personal data needed |
| Customs declaration data | yes | no | customer and price data, GDPR and trade secrets |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| Trans.eu | incumbent | PL / EU | freight exchange and TMS; "Powered by AI" freight assignment; 25,000 active spot carriers | AI on assignment and carrier checks *(vendor claim)* | demo only, not public |
| TIMOCOM | incumbent | DE / EU | freight exchange, tracking, messenger, API | no AI features described on its homepage (Oct 2026) | not public |
| Digicust | startup | AT / EU | AI customs declarations, tariff classification, email triage; lists Poland coverage; 100+ companies live | high *(vendor claim)* | not public |
| Raft | startup | UK / global | agentic AI for forwarders and customs brokers, email intake, AP; "up to 93% of customs documentation" | high *(vendor claim)* | not public |
| Polish customs agencies | incumbent | PL | manual declarations as a service | low | per declaration, not found |

The gap is the small Polish desk: Digicust and Raft sell to larger brokers with ERP integrations; Trans.eu automates inside its own exchange. Avoid competing on customs at first; start with email-to-order and carrier vetting, and integrate with Trans.eu rather than fight it.

**Challenge from five angles.**
- **Customer:** small forwarders are price-sensitive and loyal to their TMS; they buy only what saves a dispatcher's time in week one.
- **Incumbent:** Trans.eu already ships AI assignment and can add email intake; it owns the customers and the carrier data.
- **Frontier labs and big tech:** a generic mail assistant extracts orders well; the value is the TMS and exchange integration, not the extraction.
- **Regulator:** customs declarations carry legal effect and fines; the declarant must stay a human; the AI Act does not classify this as high risk.
- **Unit economics:** low price per desk; integration work per TMS can eat the margin.

**After the challenge.** Survives as a narrow "order email to TMS + carrier fraud check" tool for 1-20 person Polish forwarders, integrated with the two or three most used TMS. Customs comes later or through partnership. C stays 8.

**Numbers.**
- Poland 20.2% of EU road tkm in 2025, rank 1 (Eurostat, Jul 2026).
- AI use: PL 8.36%, EU 19.95% of enterprises in 2025 (Eurostat, Dec 2025).
- Trans.eu: 25,000 active spot carriers, "up to 75%" less manual order handling *(vendor claim, read Oct 2026)*.
- Digicust: 100+ companies live, 70-90% declaration automation, ZLS 3-4 h to 10-15 min *(vendor claim, read Oct 2026)*.
- Raft: 5M+ shipments a year, up to 93% of customs documentation automated *(vendor claim, read Oct 2026)*.
- Number of Polish forwarding firms: not found.

**How to start.**
1. Weeks 1-3: collect 300 anonymised order emails from 2 friendly forwarders; build the extractor on the local rig.
2. Weeks 3-6: TMS push for one popular Polish TMS plus a carrier check (VAT white list, exchange rating).
3. Weeks 6-8: fraud signals and a daily dashboard; measure minutes saved per order.
4. First 10 customers: dispatcher communities, freight fairs, one TMS partner.
5. Pricing test: 399 PLN per desk per month vs 3 PLN per order.

**Risks and limitations.**
- Trans.eu or a TMS vendor bundles the same feature for free.
- Integration effort per TMS; small vendors have weak APIs.
- Wrong extraction of a date or price causes real cost; the human gate is mandatory.
- Freight market downturns cut software budgets first.

**Kill criteria.** Stop if pilots save under 3 minutes per order or no TMS offers an API by month 4.

**Sources:** [Eurostat road freight](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Road_freight_transport_statistics) · [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Trans.eu enterprise](https://enterprise.trans.eu/en/) · [TIMOCOM](https://www.timocom.co.uk/) · [Digicust](https://www.digicust.com/en) · [Raft](https://www.raft.ai/)

---

## 8. On-prem maintenance and field-service knowledge agent for industrial SMEs in CEE

**Region:** PL / EU (CEE) · **Buyers:** maintenance managers and service directors at mid-size manufacturers, machine builders, water and heat utilities · **Revenue model:** setup fee + annual licence for an on-prem box, priced per site · **Competition:** medium · **Local-model fit:** high · **Score: 66** (M13 G16 C10 L13 F9 R5)

> A real gap in CEE industrial SMEs that will not send drawings and service logs to the cloud, but big platforms (Microsoft, Siemens, Aquant) are moving down-market and data preparation is the hard part.

**The asymmetry.** Polish enterprises used AI at 8.36% in 2025 against 19.95% in the EU, and small firms EU-wide at 17% (Eurostat, 2025). Maintenance knowledge sits in PDF manuals (often German or English), paper or Excel service logs and the heads of senior technicians. Siemens shows the direction with an Industrial Copilot chatbot for maintenance tasks in its own Erlangen factory, and Aquant sells to large OEMs (Makino, Terex, JLG, Stryker), but neither targets a 200-person Polish plant with mixed-brand machines. The gap exists because of plant-floor IT/OT separation, offline sites, mixed languages, and conservative buyers; it may stay open 2-3 years in the SME tier.

**Who pays and how much.** Number of manufacturing SMEs in PL and EU with a maintenance team: not found in a source read this session. What they pay today: technician time spent searching manuals and calling the OEM, and downtime cost; neither figure was found for PL. Benchmark: Microsoft Dynamics 365 Field Service lists 105 USD per user per month before Copilot credits (Oct 2026), which a small plant often does not buy at all. Price points to test: 5,000-10,000 EUR setup plus 500-1,500 EUR per month per site. Channel: maintenance trade fairs, CMMS resellers, machine-tool distributors.

**The agentic app.**
1. Ingest: manuals, wiring diagrams, CMMS exports, service logs, spare-part lists from a file share onto a box in the plant network.
2. Extract: OCR, table and part-number extraction, link fault codes to machines and parts.
3. Reason: technician asks in Polish ("press 3, alarm E-214, what next"); agent retrieves manual pages, past fixes on the same machine, part availability.
4. Draft: step-by-step procedure with citations to manual page and past work order.
5. Verify: safety-relevant steps (lockout/tagout, electrical work) flagged and never shortened; answers without a cited source are refused.
6. Act: draft work order or spare-part request created in the CMMS only after the maintenance lead approves.

**Local vs paid split.**
| Step | Local open model | Paid API | Why |
| --- | --- | --- | --- |
| OCR and extraction | Yes | No | Drawings and manuals are confidential and volume is high |
| Technician Q and A in Polish | Yes (Bielik 11B v3 or multilingual model) | No | Plant network often has no internet, low latency needed |
| Translation of German or English manuals | Yes | Optional for hard documents | Volume cost and secrecy |
| Fault-pattern analysis across logs | Yes | Optional on anonymized aggregates | Logs reveal production volumes |
| Product setup and prompt engineering | No | Yes | Developer-side work, no customer data |

**Competition.**
| Competitor | Type | Region | What it ships | AI depth | Price |
| --- | --- | --- | --- | --- | --- |
| Siemens Industrial Copilot | incumbent | global | Chatbot support for maintenance tasks, built with Microsoft | Deep in Siemens ecosystem | Not public |
| Aquant | startup | US / global | Conversational service AI with agent studio for equipment makers | Deep | Not public, free trial |
| Microsoft Dynamics 365 Field Service | global platform | global | Field service management with Copilot, guides, remote assist | Medium | 105 USD per user per month plus Copilot credits |
| CMMS vendors (local Polish and EU) | incumbent | PL / EU | Work orders and asset registers, AI add-ons varying | Low | Not found |

The gap: vendor-neutral, mixed-brand plants, on-prem and offline, Polish-language technician interface. Beat the platforms on deployment (one box, no cloud) and on data preparation done for the customer.

**Challenge from five angles.**
- **Customer:** Plant managers fund what cuts downtime, not what "organizes knowledge"; proof needs a measured before/after on one line, which takes months.
- **Incumbent:** CMMS vendors and OEMs will add retrieval chat on their own data; the agent wins only across brands and documents they do not own.
- **Frontier labs and big tech:** Microsoft Copilot over SharePoint already answers manual questions for firms on Microsoft 365; the on-prem and offline segment is what remains.
- **Regulator:** EU Machinery Regulation and safety rules make wrong maintenance advice a liability; the agent must cite and must not invent safety steps.
- **Unit economics:** Every plant has messy, scanned, multilingual documents; onboarding effort can exceed the first-year licence.

**After the challenge.** Survives as a narrow product: "service-log plus manual search" for one machine class (for example injection moulding or CNC) where documents look alike, sold with a fixed onboarding. Durability is the weakest score.

**Numbers.**
- Poland AI use 8.36% of enterprises vs EU 19.95% (Eurostat, 2025 data).
- EU small enterprises 17%, medium 30.36% using AI (Eurostat, 2025 data).
- Dynamics 365 Field Service 105 USD per user per month, contractor plan 50 USD (Microsoft pricing page, read 14 Oct 2026) *(vendor price)*.
- Aquant customers include Makino, Terex, JLG, Stryker, Siemens *(vendor claim, website read 14 Oct 2026)*.
- Count of PL manufacturing SMEs with maintenance teams: not found.

**How to start.**
1. Weeks 1-4: RAG with citations over a public set of machine manuals plus synthetic service logs; Polish chat UI.
2. Weeks 5-8: pilot on one plant with one machine class, measured time-to-answer for technicians.
3. First 10 customers: via machine distributors and maintenance associations; offer 3 discounted pilots in exchange for case studies.
4. Pricing test: setup-only vs setup plus monthly licence; watch which one closes.

**Risks and limitations.**
- Document preparation is manual and slow; can turn into consulting.
- Safety liability for wrong maintenance instructions.
- Sales cycle in manufacturing is long and seasonal.
- Strong local relationships matter; a newcomer lacks industrial credibility.

**Kill criteria.** Stop if two pilots do not show a measurable time saving technicians confirm, or onboarding per plant exceeds 30 days.

**Sources:** [Eurostat: Use of AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Siemens Industrial Copilot](https://www.siemens.com/global/en/products/automation/topic-areas/industrial-ai/industrial-copilot.html) · [Aquant](https://www.aquant.ai/) · [Dynamics 365 Field Service pricing](https://www.microsoft.com/en-us/dynamics-365/products/field-service/pricing) · [SpeakLeash Bielik models](https://huggingface.co/speakleash)

---

## 9. KSeF back-office agent for Polish accounting offices

**Region:** PL · **Buyers:** accounting offices (biura rachunkowe), 2-30 staff · **Revenue model:** setup fee + monthly licence per client entity served · **Competition:** high · **Local-model fit:** high · **Score: 65** (M16 G12 C6 L12 F11 R8)

> A real but crowded opportunity: win only as an add-on agent layer on top of the office's existing ledger software, sold local-first, never as a new accounting system.

**The asymmetry.** KSeF 2.0 became the only e-invoice channel on 1 Feb 2026 for large firms and all invoice recipients, mandatory for most issuers from 1 Apr 2026, and for the smallest firms (up to 10,000 PLN monthly sales) from 1 Jan 2027 (ksef.podatki.gov.pl, read Oct 2026). Structured XML invoices remove the OCR step, but the work that remains in an office is still manual: assigning cost categories, VAT treatment, matching to bank lines, chasing missing receipts that are not KSeF invoices (foreign invoices, fuel slips, contracts), and answering client questions by phone and email. Poland is a late AI adopter: 8.36% of Polish enterprises used AI in 2025 against 19.95% in the EU (Eurostat, 2025 data). The gap stays open while incumbents add features to their own suites one module at a time; I estimate 1-2 years before they ship agent-level booking (my estimate, not measured).

**Who pays and how much.** Number of accounting offices in Poland: not found in this run (GUS PKD 69.20 tables not retrieved). Offices are typically paid a monthly flat fee per client; prices not verified in this run. What offices already pay for software (vendor price lists, read 14 Oct 2026): wFirma 24 PLN net per client per month for the full office system, with a 2026 promotion of one free year for the office and 10 clients; SaldeoSMART office packages 289, 409 and 789 PLN net per month. A buyer would accept a tool that costs a fraction of one junior bookkeeper's monthly salary if it frees capacity for more clients. Test price: 300-1,000 PLN per office per month plus 5-15 PLN per client entity (hypothesis to test, not market data). Channels: regional accountant associations, Facebook groups of biura rachunkowe, partner programmes of ledger software vendors.

**The agentic app.**
1. Ingest: pull KSeF invoices (XML) for each client via the KSeF API token, bank statements (MT940/CSV), and emailed non-KSeF documents.
2. Extract: parse KSeF XML directly; OCR plus model extraction only for non-KSeF documents.
3. Reason: propose account, cost category, VAT code and KPiR/ledger column from the client's history and the office's chart-of-accounts rules.
4. Draft: booking proposal plus a list of missing documents and a client message in Polish.
5. Verify: rule checks (VAT rates, white-list bank account check, duplicate detection), confidence score per line.
6. Act: human approval gate, the bookkeeper accepts or edits; only then export to Comarch Optima, Symfonia, enova365 or Rachmistrz import format. No automatic filing of JPK or declarations.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| KSeF XML parsing | no model, code | none | structured data, deterministic |
| Non-KSeF document extraction | Qwen-VL class or Bielik 11B v3 (Apache 2.0) | fallback only | client financial data, volume cost |
| Booking proposal | local model with office rules in context | hard cases only, anonymised | professional secrecy, GDPR, steady volume |
| Client message drafts in Polish | Bielik 11B v3 | none | Polish fluency is enough at 11B |
| Rule design and eval sets | none | frontier model offline | one-off work, no client data |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| SaldeoSMART (BrainShare) | incumbent | PL | document flow, OCR, bank statements, free KSeF download and send, 300,000+ users (vendor claim) | AI sets parameters, dimensions and document type of KSeF invoices (vendor claim) | office packages 289 / 409 / 789 PLN net per month (Oct 2026) |
| Comarch ERP Optima / Betterfly | incumbent | PL | ledger, KPiR, VAT, office module, KSeF | not verified in this run | not found |
| Symfonia | incumbent | PL | ledger and HR for SMEs and offices | not verified in this run | not found |
| enova365 (Soneta) | incumbent | PL | ERP, office module | not verified in this run | not found |
| wFirma | incumbent | PL | online office system, ledger, payroll, unlimited KSeF and OCR, client portal | Magic Box document processing, SMART Lista, digital accounting assistant (vendor claim) | 24 PLN net per client per month (Oct 2026) |
| inFakt / Fakturownia | incumbent | PL | invoicing, online bookkeeping, free KSeF, VAT whitelist check, payment matching, OCR | inFakt: no AI claimed on KSeF page; Fakturownia: AI assistant integration (MCP) on all plans (vendor claim) | Fakturownia free plan 3 invoices per month; inFakt online accounting from 200 PLN per month (Oct 2026) |
| Rachmistrz / Rewizor (InsERT) | incumbent | PL | KPiR and ledger desktop software | not verified in this run | not found |

Gap: incumbents own the ledger and KSeF connection, so the room is in the judgement layer (classification, missing documents, client Q&A) that sits across several ledgers in one office; SaldeoSMART already types KSeF invoices with AI inside its own flow, so single-product classification is no longer a gap. Avoid head-on: integrate by import files, sell to offices running two or more ledger products.

**Challenge from five angles.**
- **Customer:** offices are conservative and liable for errors; they will not trust auto-booking until it proves accuracy on their own clients' history.
- **Incumbent:** Comarch, Saldeo and wFirma control the data path and can ship classification inside their product at zero marginal sales cost.
- **Frontier labs and big tech:** low direct threat; they do not build Polish ledger exports, but generic copilots lower the perceived value of "AI".
- **Regulator:** booking proposals do not change legal responsibility (the office signs); GDPR processing agreements and professional secrecy terms needed; KSeF tokens are sensitive credentials.
- **Unit economics:** local inference on a box in the office is cheap at volume; the cost is integration support per ledger product.

**After the challenge.** Survives as a narrow, local-first booking and missing-document assistant for multi-ledger offices; price per client entity, which must sit well below wFirma's 24 PLN per client for a whole office system; score drops to 65 (C6) because SaldeoSMART already ships AI classification of KSeF invoices.

**Numbers.**
- KSeF 2.0: 1 Feb 2026 large firms and recipients, 1 Apr 2026 most issuers, 1 Jan 2027 small issuers up to 10k PLN monthly (ksef.podatki.gov.pl, read 14 Oct 2026).
- AI use: 8.36% of Polish enterprises vs 19.95% EU, small enterprises 17% EU-wide (Eurostat, 2025 data).
- Professional, scientific and technical activities: 40.43% AI use EU-wide (Eurostat, 2025 data), so Polish offices are behind their EU peers (third-party estimate of the trend, sector split for PL not found).
- Number of Polish accounting offices and accountant shortage: not found in this run (GUS, KIDP and search result pages tried, 14 Oct 2026).
- wFirma office plan: 24 PLN net per client per month, unlimited KSeF and OCR (wfirma.pl, read 14 Oct 2026, vendor price list).
- SaldeoSMART: office packages 289 / 409 / 789 PLN net per month, KSeF at 0 PLN, AI typing of KSeF invoices, 300,000+ users and 6,300-7,000 firms and offices (two figures on the same site) (saldeosmart.pl, read 14 Oct 2026, vendor claim).

**How to start.**
1. Weeks 1-4: KSeF API reader plus booking proposal for one ledger (Comarch Optima import), tested on anonymised history of one friendly office.
2. Weeks 5-8: missing-document chaser and Polish client-message drafts; accuracy report per client.
3. First 10 customers: offices in one city via the local accountant association; free 60-day pilot on 20 clients each.
4. Pricing test: flat office fee vs per-entity fee, offered to alternating prospects.

**Risks and limitations.**
- Incumbent ships the same feature inside the ledger.
- Accuracy below what offices need for unattended booking; value then shrinks to suggestions.
- Integration support load across ledger versions.
- Liability claims if a wrong VAT code passes the human gate.

**Kill criteria.** Stop if after 3 months fewer than 3 offices pay or booking acceptance stays below 80% of lines.

**Sources:** [KSeF stages](https://ksef.podatki.gov.pl/etapy-wdrozenia-ksef/) · [Eurostat AI use in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [SaldeoSMART](https://www.saldeosmart.pl) · [Bielik 11B v3 Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [wFirma](https://wfirma.pl) · [wFirma office prices](https://wfirma.pl/cennik-dla-biur-rachunkowych) · [SaldeoSMART office prices](https://www.saldeosmart.pl/cennik/biuro) · [inFakt KSeF](https://www.infakt.pl/ksef) · [Fakturownia prices](https://fakturownia.pl/cennik)

---

## 10. Receivables and EPU paperwork agent for Polish SMEs

**Region:** PL · **Buyers:** SMEs with B2B invoices (wholesale, construction subcontractors, services), and the accounting offices serving them · **Revenue model:** monthly subscription per company + per-case fee for court filings · **Competition:** medium · **Local-model fit:** medium · **Score: 64** (M13 G13 C8 L9 F12 R9)

> Worth testing as a "before the collector" agent that reads KSeF and bank data, sends graded reminders and prepares the EPU claim for a human to file, priced below the 8% success fee of online collectors.

**The asymmetry.** Chasing late invoices in small firms is still a manual mix of phone calls, email templates and paper demand letters, and Polish firms are late AI adopters: 8.36% of Polish enterprises used AI in 2025 vs 19.95% in the EU, and EU-wide only 17% of small firms vs 55% of large ones (Eurostat, 2025 data). The state channel is already digital: the electronic order-for-payment court (EPU, e-sad.gov.pl) has handled 33,407,345 cases since 2010 and has about 373,160 users, of whom 341,882 are individual accounts and 16,916 professional representatives, with an API for mass plaintiffs (gov.pl, EPU 3.0 page, read Oct 2026). Most SMEs therefore file themselves or pay a collector. KSeF (mandatory for most issuers from 1 Apr 2026) gives every invoice a structured, machine-readable record, which makes overdue detection trivial for any tool with read access. The gap: existing services automate templates and a fixed workflow, not judgement (which debtor to call, what to say, when to escalate).

**Who pays and how much.** Number of SMEs with chronic overdue B2B invoices: not found in this run. BIG InfoMonitor holds 113.5 million pieces of debt information (BIG, Feb 2026, vendor claim). Reference price: Vindicat charges 8% of the recovered amount, or a subscription from 169 PLN per month for automatic SMS and email reminders, demand letters with interest and automatic BIG InfoMonitor entry (vendor pages, read 14 Oct 2026). Test price: 99-299 PLN per month per company for reminders and claim drafts, plus a fixed fee per prepared EPU claim (hypothesis). Channel: accounting offices as resellers, because they already see their clients' receivables.

**The agentic app.**
1. Ingest: KSeF sales invoices, bank statements, payment history per debtor.
2. Extract: overdue list, partial payments, disputes found in email threads.
3. Reason: debtor risk score from payment history plus KRD and BIG checks (via their paid APIs or manual lookup), choice of tone and next step.
4. Draft: reminder sequence in Polish, formal demand letter (wezwanie do zapłaty), interest calculation, and an EPU claim draft with the evidence list.
5. Verify: amounts, dates and interest checked by code; limitation period check.
6. Act: human approval gate before any formal demand, any registry entry (KRD/BIG) and any EPU filing; the owner or lawyer files.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| Overdue detection and interest | no model, code | none | deterministic |
| Email dispute reading | Bielik 11B v3 or Qwen class | none | debtor personal data under GDPR |
| Reminder and demand drafts in Polish | Bielik 11B v3 | none | templates plus tone, Polish quality enough |
| EPU claim justification | local model first | frontier model for hard disputes, anonymised | legal wording quality |
| Debtor registry checks | none | KRD or BIG paid service | data only they hold |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| KRD (Krajowy Rejestr Długów) | incumbent | PL | contractor checks, debtor listing, collection via Kaczmarski Group, RiskRadar, NFG factoring | not shown on homepage | not found |
| BIG InfoMonitor | incumbent | PL | firm and consumer checks, debtor entry, payment notices, monitoring | not shown on homepage | not found on homepage |
| Vindicat.pl | startup | PL | automated SMS and email reminders, demand letters with interest, lawsuits, online negotiation, debt marketplace, automatic BIG entry, 20,000+ firms (vendor claim) | "intelligent debt collection robot" (vendor claim), rule workflow, no LLM shown | 8% of recovered amount, or subscription from 169 PLN per month (Oct 2026) |
| Kaczmarski Inkasso | incumbent | PL | B2B debt collection agency, KRD group | not verified in this run | not found |
| Invoicing tools (inFakt, Fakturownia, wFirma) | incumbent | PL | invoicing with KSeF; Fakturownia sends automatic payment reminders on paid plans; inFakt matches bank transactions to invoices | Fakturownia: AI assistant integration (MCP) (vendor claim); others not verified | Fakturownia free plan 3 invoices per month, paid prices not visible (Oct 2026) |

Gap: collectors and registries earn from the late, formal stage; nobody found in this run sells an agent that works the early stage with judgement and hands a ready EPU file to the owner. Avoid competing with registries; integrate them.

**Challenge from five angles.**
- **Customer:** owners fear spoiling client relations; tone control and approval must be visible.
- **Incumbent:** Vindicat or invoicing apps can add LLM drafting quickly; KRD controls the registry asset.
- **Frontier labs and big tech:** a generic assistant can write a demand letter; the moat is data access (KSeF, bank) and the Polish procedure.
- **Regulator:** debt collection must respect consumer protection and GDPR; staying B2B-only and never filing without approval limits exposure; EPU filing rules and fees change with EPU 3.0.
- **Unit economics:** cheap to run locally; churn risk once the backlog is cleared.

**After the challenge.** Survives as a B2B-only early-stage agent sold through accounting offices; flat fee beats success fee for clients with regular volume, but Vindicat's 169 PLN subscription and free reminders inside invoicing tools cap the price; score drops to 64 (C8).

**Numbers.**
- EPU: 33,407,345 cases since 2010, about 373,160 users (gov.pl EPU page, read 14 Oct 2026).
- BIG InfoMonitor: 113.5 million debt records, 381.0 million reports downloaded since 2014 (big.pl, Feb 2026, vendor claim).
- Vindicat: 8% success fee, 93% settled amicably, 20,000+ firms (vindicat.pl, read Oct 2026, vendor claim); subscription from 169 PLN per month (vindicat.pl/cennik, read 14 Oct 2026, vendor price list).
- Fakturownia: automatic payment reminders on paid plans (fakturownia.pl/cennik, read 14 Oct 2026).
- Other Polish collection services seen in search results (KRUK, INDOS, CollectIn): offers and prices not verified, 14 Oct 2026.
- AI use: PL 8.36% vs EU 19.95% of enterprises (Eurostat, 2025 data).

**How to start.**
1. Weeks 1-4: KSeF plus bank overdue detector and Polish reminder sequence for one pilot firm.
2. Weeks 5-8: demand letter and EPU claim draft generator with interest calculator; lawyer review of templates.
3. First 10 customers: via two accounting offices that resell to their clients.
4. Pricing test: flat monthly fee vs 3% of recovered amount.

**Risks and limitations.**
- Legal templates need a lawyer's sign-off; errors cost court fees.
- Registry APIs are paid and contract-gated.
- Value is front-loaded; retention needs ongoing monitoring features.
- Consumer debts bring stricter rules; stay B2B.

**Kill criteria.** Stop if pilot clients do not recover at least 2x the subscription in overdue cash within 3 months.

**Sources:** [EPU gov.pl](https://www.gov.pl/web/sprawiedliwosc/epu) · [Vindicat](https://vindicat.pl/) · [Vindicat prices](https://vindicat.pl/cennik) · [Fakturownia prices](https://fakturownia.pl/cennik) · [BIG InfoMonitor](https://www.big.pl/) · [KRD](https://krd.pl/) · [KSeF stages](https://ksef.podatki.gov.pl/etapy-wdrozenia-ksef/) · [Eurostat AI use](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

---

## 11. CE technical file agent for SME machinery and product manufacturers

**Region:** PL (then EU) · **Buyers:** Polish SME manufacturers of machinery, equipment and consumer products, and their external CE consultants · **Revenue model:** per technical file + annual subscription for updates · **Competition:** medium · **Local-model fit:** high · **Score: 63** (M13 G13 C9 L12 F8 R8)

> The Machinery Regulation date (20 Jan 2027) forces every machine builder to rework its technical files, and designs are trade secrets that suit an on-prem model; the risk is liability and a long, expert-heavy MVP.

**The asymmetry.** Regulation (EU) 2023/1230 applies on a mandatory basis from 20 January 2027; until then the Machinery Directive 2006/42/EC applies (European Commission machinery page, read Oct 2026). It allows digital instructions and declarations of conformity, so documentation must be rebuilt anyway. The General Product Safety Regulation applies since 13 December 2024 and the Battery Regulation (EU) 2023/1542 adds the battery passport from February 2027 (dates from the regulations on EUR-Lex; not re-checked for 2026 amendments in this run). Poland: 8.36% of enterprises used AI in 2025 vs 19.95% EU (Eurostat, Dec 2025). Technical files are written by engineers and freelance CE consultants in Word: risk assessment per EN ISO 12100, list of harmonised standards, instructions, declaration of conformity.

**Who pays and how much.** Number of Polish machinery SMEs: not found in this run. Spend today: external CE consultants and engineer time; no public price list found. A price a 20-200 person manufacturer accepts: assume 3,000-10,000 PLN per machine file and an update subscription (my hypothesis). Channel: CE consultants (white label), industry clusters, trade fairs, notified bodies' training events.

**The agentic app.**
1. Ingest: BOM, drawings metadata, photos, old technical file, supplier declarations.
2. Extract: hazards, components, energy sources, safety functions.
3. Reason: map to the essential requirements of 2023/1230 annex III and harmonised standards; flag Annex I categories that need a notified body.
4. Draft: risk assessment table, instruction manual sections, EU declaration of conformity, GPSR product safety data.
5. Verify: every requirement cites a regulation article or standard clause; **human gate**: the manufacturer's responsible engineer signs the declaration (legal effect).
6. Act: export the file and a change log; watch for standard updates.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| Drawing and BOM ingest | yes | no | designs are trade secrets |
| Hazard extraction | yes | no | volume and secrecy |
| Requirement mapping | yes | optional second opinion | regulation text is public, client data is not |
| Manual and declaration drafting in PL, EN, DE | yes | no | open models write these languages well enough |
| Generic template authoring | no | yes | no client data involved |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| Safexpert (IBF Solutions) | incumbent | AT / EU | CE and risk assessment software for machine builders | not verified (site did not load in this run) | not found |
| TÜV SÜD / TÜV Rheinland | consultancy | global | conformity assessment, notified body services | manual | quote-based |
| Intertek | consultancy | global | product testing and certification | manual | quote-based |
| Polskie Centrum Badań i Certyfikacji | consultancy | PL | certification and testing | manual | quote-based |
| Freelance CE consultants | consultancy | PL | technical files by hand | low | not found |

No AI-native CE file tool for Polish SMEs was found, but the search was thin (one vendor site failed to load); treat C as provisional. Sell to the freelance consultants first: they are the bottleneck before January 2027.

**Challenge from five angles.**
- **Customer:** many SMEs copy last year's file and hope; they pay only when a customer or inspector demands it.
- **Incumbent:** Safexpert and notified bodies can add AI drafting; notified bodies own trust.
- **Frontier labs and big tech:** general models draft manuals well; the moat is standards mapping and evidence, and standards texts are paid (licensing limits what you can embed).
- **Regulator:** liability stays with the manufacturer; a wrong risk assessment after an accident is serious; the product must never sign anything.
- **Unit economics:** each machine type needs expert review; selling to consultants keeps the expert in the loop but caps price.

**After the challenge.** Survives as a consultant's co-pilot running on-prem, for one niche (e.g. food processing or woodworking machines). F and R stay low because of the domain depth and liability.

**Numbers.**
- Machinery Regulation 2023/1230 mandatory from 20 Jan 2027 (European Commission, read Oct 2026).
- PL 8.36% vs EU 19.95% of enterprises using AI in 2025 (Eurostat, Dec 2025).
- Count of Polish machinery SMEs and CE consulting prices: not found.

**How to start.**
1. Weeks 1-4: partner with 2 CE consultants; rebuild 5 real files on the local rig.
2. Weeks 4-8: requirement map for one machine niche, citation checker, PL/EN/DE manual drafts.
3. First 10 customers: consultants' clients before January 2027.
4. Pricing test: 2,500 vs 6,000 PLN per file.

**Risks and limitations.**
- Product liability after an accident; contracts must keep the engineer as author.
- Harmonised standards are copyrighted; licensing cost.
- Long expert review per file limits scale.
- Demand peak around January 2027.

**Kill criteria.** Stop if consultants do not cut file time by half on the first 5 files.

**Sources:** [EC machinery](https://single-market-economy.ec.europa.eu/sectors/mechanical-engineering/machinery_en) · [Regulation 2023/1230](https://eur-lex.europa.eu/eli/reg/2023/1230/oj) · [GPSR 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj) · [Battery Regulation 2023/1542](https://eur-lex.europa.eu/eli/reg/2023/1542/oj) · [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

---

## 12. Construction estimate and tender assistant for Polish contractors

**Region:** PL · **Buyers:** small and medium general contractors, installers, freelance cost estimators (kosztorysanci) · **Revenue model:** subscription per estimator + per-tender packs · **Competition:** medium · **Local-model fit:** medium · **Score: 63** (M12 G15 C10 L8 F8 R10)

> A real gap: global AI takeoff tools do not speak KNR and Polish tender rules, Polish estimating incumbents show no visible AI.

**The asymmetry.** Construction is a low-AI sector: 10.79% of EU construction enterprises used AI in 2025, about half the all-sector EU rate of 19.95% (Eurostat, 2025). Poland overall is at 8.36% (Eurostat, 2025). Estimating in Poland follows KNR/KNNR catalogue norms and public tender rules, so estimators still read drawings, build the bill of quantities (przedmiar) by hand and type positions into desktop programs. Global AI takeoff tools (Togal, Kreo) measure drawings but do not output KNR-coded Polish estimates. The gap lasts while incumbents keep desktop products and global tools ignore Polish norms.

**Who pays and how much.** Number of PL construction firms and estimators: not found in this pass (GUS REGON counts to check). Global price anchors: Togal $299 per user per month, Kreo Pro $175 per user per month (*vendor prices*, read 2026-10-14). Polish desktop estimating licences: prices not found in this pass. Test 300-900 PLN per estimator per month, or per-tender pricing for occasional bidders. Channel: estimator forums, training firms, builder merchants.

**The agentic app.**
1. Ingest: tender documents (SIWZ/SWZ, description of works, PDF drawings).
2. Extract: scope items, quantities from text, measurements from drawings (vision model).
3. Reason: map each item to KNR positions with confidence and alternatives.
4. Draft: bill of quantities and estimate export to the format the incumbent program imports.
5. Verify: diff against the description of works; list missing items and risky assumptions.
6. Act: **human estimator approval** before the price goes into a bid.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| Document parsing and OCR | Yes | No | Volume of pages, cost |
| Drawing measurement | Partly | Yes for hard drawings | Vision quality varies |
| KNR mapping | Yes, with retrieval over the catalogue | Optional | Repetitive, high volume |
| Risk review of tender terms | No | Yes | Better reasoning, data is not secret |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| Norma PRO / EXPERT (Athenasoft) | incumbent | PL | Desktop estimating on KNR | No AI found in this pass | not found |
| Zuzia | incumbent | PL | Desktop estimating | No AI found in this pass | not found |
| Rodos | incumbent | PL | Desktop estimating | No AI found in this pass | not found |
| Togal.AI | startup | global | AI takeoff from drawings, chat prompts | High for takeoff | $299 per user per month |
| Kreo | startup | global | Takeoff, Auto Measure, Ask AI for drawings | High for takeoff | $35-175 per user per month |

Gap: nobody found joining AI takeoff with KNR coding and Polish tender text. Avoid fighting incumbents: export into their formats.

**Challenge from five angles.**
- **Customer:** estimators distrust automatic quantities; one wrong item costs a bid. Answer: position as a checker and first draft, show every source.
- **Incumbent:** Athenasoft and others own the KNR data and could add AI; their pace is unknown.
- **Frontier labs and big tech:** general assistants can read tender PDFs but not price with KNR; low threat in 2 years.
- **Regulator:** low; liability for the bid stays with the contractor.
- **Unit economics:** small market, construction cycles hit willingness to pay; KNR catalogue licensing may cost money.

**After the challenge.** Survives as a "tender reader + przedmiar checker" that feeds incumbent programs, not a replacement. Needs an estimator co-founder or adviser. Score about 60.

**Numbers.**
- Construction AI use 10.79% vs all sectors 19.95%, EU 2025 (Eurostat, *official statistics*).
- Poland 8.36% of enterprises use AI, 2025 (Eurostat).
- Togal Growth $299 per user per month (*vendor price*, 2026-10-14).
- Kreo Lite $35, Plus $70, Pro $175 per user per month (*vendor price*, 2026-10-14).
- Number of Polish estimators and licence prices: not found.

**How to start.**
1. Weeks 1-3: interview 10 estimators; collect 5 past tenders with final estimates.
2. Weeks 4-8: MVP that reads the description of works and outputs a draft przedmiar with KNR suggestions; measure hit rate against real estimates.
3. First 10 customers: freelance estimators via forums and LinkedIn, free first tender.
4. Pricing test: per tender (100-300 PLN) vs monthly.

**Risks and limitations.**
- KNR catalogue rights and data access.
- Drawing quality varies; vision accuracy unproven for Polish drawings.
- Reader lacks domain knowledge.
- Cyclical buyers.

**Kill criteria.** Stop if KNR mapping is below 70% correct on real tenders after 8 weeks, or no estimator pays after a free trial.

**Sources:** [Eurostat: use of AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Togal pricing](https://www.togal.ai/pricing) · [Kreo pricing](https://www.kreo.net/pricing)

---

## 13. Local Polish medical scribe for private clinics

**Region:** PL · **Buyers:** private clinics, specialist practices, dentists, physiotherapy and occupational-medicine centres · **Revenue model:** per doctor per month + setup of an on-site box · **Competition:** medium · **Local-model fit:** high · **Score: 61** (M15 G13 C7 L12 F7 R7)

> Big pain and a clear secrecy argument, but Docplanner's Noa already sells AI notes to Polish doctors through ZnanyLekarz, so the only open lane is on-premise, EDM-integrated scribing for clinics that refuse the cloud.

**The asymmetry.** Polish doctors type visit notes into EDM (electronic medical records, mandatory in Poland since 2021) by hand during or after the visit. Polish firms adopt AI at 8.36% against 19.95% in the EU (Eurostat, 2025). Big global scribes skip Poland: Microsoft Dragon Copilot for physicians lists the US, Canada, UK, Ireland, France, Germany, Austria, Belgium, the Netherlands and Switzerland, not Poland (Microsoft, Oct 2026); Abridge shows only US health systems (Oct 2026). The gap exists because of language (Polish speech, Latin and drug names), medical secrecy and GDPR art. 9 health data, and small fragmented EDM vendors. It is closing: Docplanner's Noa Notes is live in Poland, and Tandem Health claims 10,000+ care organisations across Europe. Window: 12-24 months for the on-prem niche.

**Who pays and how much.** Buyers: the Polish private outpatient sector, thousands of clinics and individual practices; the doctor register (Centralny Rejestr Lekarzy, NIL) publishes counts dated 30 Jun 2026 (exact number not extracted in this run). What they pay now: doctor time spent typing, often 20-30% of the visit by common anecdote (not measured; no Polish survey found). Price a clinic may accept: 150-400 PLN per doctor per month plus a one-off box (my hypothesis, to test against Noa's price, which was not visible on its site). Channel: EDM vendors as resellers, regional medical chambers, private clinic networks, dental associations.

**The agentic app.**
1. Ingest: audio of the visit (with patient consent captured in the app), recorded on a tablet; audio never leaves the clinic LAN.
2. Extract: local Polish speech-to-text, then diarisation (doctor and patient), then structured facts: complaints, history, exam, drugs, doses, ICD-10 candidates.
3. Reason: map facts to the clinic's note template; propose ICD-10 codes and flag missing items (allergies, contraindications).
4. Draft: visit note, recommendations for the patient, referral text, draft of a sick-leave (e-zwolnienie) form fields.
5. Verify: drug names and doses checked against a local drug list; anything uncertain highlighted, never silently filled.
6. Act: **human approval gate**: the doctor reads, edits and signs; only then the note goes into EDM; e-zwolnienia and prescriptions are always issued by the doctor in the official system.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| Speech-to-text in Polish | yes | no | patient audio is art. 9 health data |
| Fact extraction and note draft | yes (Bielik-11B v3 or Qwen) | no | medical secrecy, volume cost |
| ICD-10 and drug checks | yes, plus lookup tables | no | deterministic check is safer |
| Template design per specialty | no | yes (frontier model on synthetic examples) | no patient data |
| Evaluation on anonymised transcripts | partly | yes, only after anonymisation | quality checks |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| Noa Notes (Docplanner, ZnanyLekarz) | startup | PL and 13 countries | AI notes for medical documentation; data in AWS and Azure cloud | high | not shown publicly |
| Tandem Health | startup | EU | ambient scribe, CE MDR Class IIa, EU data centres, 10,000+ care organisations (vendor claim) | high | not shown on homepage |
| Microsoft Dragon Copilot | global platform | 10 countries, no PL | ambient clinical documentation for physicians | high | quote only |
| Abridge | global platform | US | ambient scribe, 300+ health systems (vendor claim) | high | not public |
| Medfile and other Polish EDM vendors | incumbent | PL | EDM, scheduling, patient records; AI notes not confirmed in this run | low (not verified) | not found |

Searched for Polish ambient-scribe startups with Polish and English queries (asystent AI lekarza, transkrypcja wizyty, ambient AI scribe Poland): no other one found in this run. Gap: every scribe found is cloud; none advertises an on-site box. Partner with EDM vendors rather than fight Noa on distribution.

**Challenge from five angles.**
- **Customer:** doctors want it free or bundled; clinics already on ZnanyLekarz get Noa from the vendor they use for booking.
- **Incumbent:** Docplanner has the distribution and the brand; EDM vendors can bundle a cloud scribe in a release.
- **Frontier labs and big tech:** Microsoft could add Poland to Dragon Copilot at any time; general speech models keep improving in Polish.
- **Regulator:** a scribe that suggests codes or clinical content can drift into medical-device territory (Tandem holds MDR Class IIa); the EU AI Act adds obligations for AI in medical devices; liability for a wrong dose is serious.
- **Unit economics:** on-site hardware, per-clinic support and EDM integrations are expensive for a 1-3 person company; a 5-doctor clinic at 250 PLN per doctor gives 1,250 PLN per month.

**After the challenge.** Survives only as an on-prem product for clinics with a strict secrecy policy (occupational medicine, psychiatry and psychology, dental chains, hospitals' private wings), sold through one EDM partner, with strict "documentation only, no clinical advice" scope to stay outside MDR. Score 61; feasibility and durability are the weak points.

**Numbers.**
- Poland AI use 8.36% of enterprises vs EU 19.95% (Eurostat, 2025).
- Tandem Health: 10,000+ care organisations in Europe, MDR Class IIa, ISO 13485 and 27001 *(vendor claim, Oct 2026)*.
- Abridge: 300+ health systems, 100M+ conversations per year *(vendor claim, Oct 2026)*.
- Dragon Copilot physicians: 10 countries listed, Poland not among them (Microsoft, Oct 2026).
- Noa: data stored in AWS and Azure, active in 13 countries *(vendor claim, Oct 2026)*.
- Share of visit time spent on documentation in Poland: not found.

**How to start.**
1. Weeks 1-3: Polish speech-to-text plus note drafting on the local rig, tested on role-played visits (no real patients).
2. Weeks 4-6: templates for 2 specialties (for example occupational medicine and dentistry), export as text into one EDM.
3. Weeks 6-8: legal review of the "not a medical device" scope and a DPIA template for clinics.
4. First 10 customers: one EDM vendor partnership, then private clinics in one city; offer a 1-month paid pilot.
5. Pricing test: per doctor per month vs flat per clinic with the box included.

**Risks and limitations.**
- Noa and Tandem may already be good enough and cheaper than an on-site box.
- MDR or AI Act classification if the scope creeps into coding or clinical suggestions.
- Speech-to-text errors on drug names and doses are dangerous.
- EDM integration is vendor-by-vendor work.
- The reader has no medical background; a clinical co-founder or adviser is needed.

**Kill criteria.** Stop if no EDM vendor agrees to a pilot within 3 months, or if pilot doctors still edit more than half of each note.

**Sources:** [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Noa](https://noa.ai/pl) · [Tandem Health](https://www.tandemhealth.ai/) · [Dragon Copilot](https://www.microsoft.com/en-us/health-solutions/clinical-workflow/dragon-copilot) · [Abridge](https://www.abridge.com/) · [NIL doctor register statistics](https://nil.org.pl/rejestry/centralny-rejestr-lekarzy/informacje-statystyczne) · [Medfile search](https://www.bing.com/search?q=Medfile+AI+asystent+notatki+wizyta) · [Bielik-11B-v3.0-Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct)

---

## 14. On-site digitisation and search of paper archives

**Region:** PL / EU · **Buyers:** company archives and records offices, notaries, parishes and dioceses, local museums, genealogy services, municipal offices · **Revenue model:** per page or per batch project + optional on-site appliance licence · **Competition:** medium · **Local-model fit:** high · **Score: 60** (M9 G12 C8 L11 F11 R9)

> Feasible and defensible for documents that may not leave the building (notarial, personnel, parish registers with personal data), but budgets are small and Transkribus is cheap, so sell searchable archives as a project, not OCR as a commodity.

**The asymmetry.** Paper archives in Poland (company personnel files kept for decades, notarial repertoria, parish registers, municipal files) are still searched by a person reading folders. Polish firms use AI at 8.36% vs 19.95% EU (Eurostat, 2025). Handwritten-text recognition (HTR) exists, but the leading platform runs in the cloud: Transkribus processes on its servers in Austria and mentions no on-premise option (Oct 2026). Many holders cannot or will not upload personnel files, notarial deeds or church registers with sensitive data (religion is GDPR art. 9 data). Classic OCR such as ABBYY FineReader targets printed text and does not advertise handwriting. Vision-language models now read documents well (Qwen2.5-VL-7B scores 95.7% on DocVQA, model card), which opens a local route; quality on old Polish handwriting is not measured publicly (not found). Window: 2-3 years, because the work is project-based and messy, which big platforms avoid.

**Who pays and how much.** Buyers: companies with legacy archives (manufacturing, utilities, former state firms), notaries, dioceses and parishes, genealogy firms, museums and local governments (public tenders). Counts and current spend on manual indexing: not found in this run. Reference prices: Transkribus Scholar 99 EUR per year for 900 credits, Team 449 EUR per year for 1,500 credits and 5 seats, credit packs 250 for 59.50 EUR, 1 credit per handwritten page (Transkribus, Oct 2026), so cloud HTR is roughly 0.24-0.50 EUR per page at small volume. A local project must therefore charge for the whole outcome (scanning coordination, indexing, search, privacy) rather than per page: for example 15,000-60,000 PLN per archive project (my hypothesis, to test). Channel: archivists' associations, document-management integrators, genealogy communities, notary chambers.

**The agentic app.**
1. Ingest: scans or phone photos of folders; page order and folder metadata captured.
2. Extract: layout detection, then HTR or OCR with a local vision-language model (Qwen VL family, Apache 2.0) or Kraken models trained on the customer's own hand.
3. Reason: normalise names, dates and places; link records (same person across registers); classify document types.
4. Draft: index cards, summaries per folder, structured tables (births, deeds, employment records).
5. Verify: confidence scores per line; low-confidence lines go to a human correction queue; corrections retrain the model.
6. Act: **human approval gate** before any record is published or released to a requester, because personal data and legal records are involved; search portal stays on the customer's network.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| Layout and HTR of sensitive documents | yes (Qwen VL, Kraken) | no | personal and art. 9 data, volume cost |
| HTR of public historical material | yes | optional (Transkribus or frontier vision) | no secrecy, compare quality |
| Entity linking and indexing | yes (Bielik, Qwen) | no | volume |
| Hard pages (damaged, Latin, Cyrillic, German Kurrent) | yes first | yes on non-sensitive pages | frontier vision is stronger on rare scripts |
| Search interface and summaries | yes | no | stays on customer network |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| Transkribus (READ-COOP) | startup | EU (Austria) | cloud HTR, 300+ community models, 100+ languages, 500,000+ users (vendor claim) | high | free 50 credits per month; 99 to 449 EUR per year; organisation quote |
| eScriptorium with Kraken | open source | EU (France) | self-hostable HTR pipeline, Kraken 7.1 engine | high | free software |
| ABBYY FineReader PDF | incumbent | global | OCR and PDF editing; handwriting not advertised | medium | 99 to 165 EUR per year |
| Frontier vision models (general chat apps) | global platform | global | read photos of documents in chat | high | subscription or per-token |
| Local digitisation service bureaus | consultancy | PL | scanning and manual indexing | low (not verified) | quote-based, not found |

Gap: Transkribus is the quality and price benchmark but is cloud-only; eScriptorium is free but needs an operator. Beat them by delivering a turnkey on-site box plus the indexing and search layer, using open tools underneath.

**Challenge from five angles.**
- **Customer:** many holders have no budget; parishes and genealogists expect free tools; companies rarely see archive search as urgent.
- **Incumbent:** Transkribus is cheap, mature and could add an on-prem or EU-sovereign tier; service bureaus own scanning contracts.
- **Frontier labs and big tech:** general vision models already read handwriting in chat; for non-sensitive material they are good enough.
- **Regulator:** church and notarial records carry access rules; public archives buy through tenders with long cycles.
- **Unit economics:** per-page prices are low; profit only comes from project fees and recurring search licences; scanning logistics is labour.

**After the challenge.** Survives as a niche for sensitive archives that cannot use the cloud (personnel files, notarial records, diocesan registers) sold as a project with a search licence. Avoid competing on per-page HTR price. Score 60, limited by market size and budget.

**Numbers.**
- Poland AI use 8.36% vs EU 19.95% (Eurostat, 2025).
- Transkribus: 500,000+ users, 200M+ pages, 300+ models, servers in Austria *(vendor claim, Oct 2026)*.
- Transkribus price: Scholar 99 EUR per year 900 credits, Team 449 EUR per year 1,500 credits, 1 credit per handwritten page *(vendor pricing, Oct 2026)*.
- ABBYY FineReader PDF Standard 99 EUR per year, Corporate 165 EUR per year *(vendor pricing, Oct 2026)*.
- Qwen2.5-VL-7B: Apache 2.0, DocVQA 95.7% *(vendor claim, model card)*.
- HTR accuracy on Polish 19th-century parish handwriting with local models: not found.

**How to start.**
1. Weeks 1-3: benchmark Qwen VL, Kraken and Transkribus on 200 sample pages of each type (printed forms, typewriter, handwriting).
2. Weeks 4-6: pipeline with correction queue and local full-text search; package on a single-GPU box.
3. Weeks 6-8: one paid pilot with a company archive or a notary, one free pilot with a parish or genealogy society for a case study.
4. First 10 customers: archivists' associations, document-management integrators, notary chambers.
5. Pricing test: fixed project price vs per-folder price plus yearly search licence.

**Risks and limitations.**
- Local models may be clearly worse than Transkribus on old handwriting.
- Small budgets and slow public tenders.
- Scanning logistics and physical handling are labour, not software.
- Data-protection duties as processor of personal records.

**Kill criteria.** Stop if local accuracy stays far below Transkribus on the target documents after training, or if no paid pilot closes in 4 months.

**Sources:** [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Transkribus](https://www.transkribus.org/) · [Transkribus plans](https://www.transkribus.org/plans) · [eScriptorium](https://escriptorium.inria.fr/) · [ABBYY FineReader pricing](https://pdf.abbyy.com/pricing/) · [Qwen2.5-VL-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct)

---

## 15. Regulatory documentation agent for small medtech and pharma (MDR/IVDR tech files, PSURs, literature screening)

**Region:** EU · **Buyers:** regulatory affairs and quality heads at small medtech manufacturers, small pharma and generics firms, regulatory consultancies serving them · **Revenue model:** per document package (PSUR, literature review, tech-file gap check) + subscription for consultancies · **Competition:** medium-high · **Local-model fit:** medium · **Score: 60** (M14 G12 C8 L9 F8 R9)

> A paying, deadline-driven niche (MDR transition until 2027/2028) where small firms still buy consultant hours, but established AI tools already cover literature screening and the reader lacks regulatory domain credibility.

**The asymmetry.** EU MDR re-certification of legacy devices was extended to 2027 for most classes and 2028 for class III and IIb implantables (2023 amendment), so thousands of technical files, clinical evaluation reports and PSURs must be written or updated in a short window. The Commission is still changing the rules: Implementing Regulation (EU) 2026/977 on uniform conformity assessment requirements came in May 2026. Large manufacturers buy platforms (Veeva, IQVIA); small firms buy consultant days and do the rest in Word. Measured AI adoption for small medtech RA teams: not found. The gap exists because of liability (a notified body rejects a weak file), fragmented small buyers, and English-heavy but templated work. It closes as consultancies adopt AI tools themselves, likely within 2-3 years.

**Who pays and how much.** European medtech employs over 950,000 people and the market is about 173 billion EUR in 2025 (MedTech Europe, third-party estimate); the number of small manufacturers was not found in sources read. Notified bodies: Team-NB lists 57 member organizations (Aug 2026). What firms pay now: consultant day rates for CER and PSUR writing (not found in a public source this session). Price points to test: 1,500-4,000 EUR per PSUR or literature review package; 500-2,000 EUR per month for a consultancy seat. Channel: regulatory consultancies as resellers (they have the clients and the liability), RAPS and medtech cluster events.

**The agentic app.**
1. Ingest: device description, risk file, previous CER/PSUR, complaint and vigilance data, literature search exports (PubMed, Embase).
2. Extract: device characteristics, claims, complaint counts by period, adverse events.
3. Reason: screen literature against a written protocol (inclusion/exclusion with reasons), map evidence to MDR Annex I requirements, find gaps.
4. Draft: PSUR sections, literature review tables, gap list against Annex II/III.
5. Verify: every sentence linked to a source row; numbers recomputed from data; a second model checks claim-evidence consistency.
6. Act: a qualified RA person signs off before anything is submitted to a notified body or authority; the agent never submits.

**Local vs paid split.**
| Step | Local open model | Paid API | Why |
| --- | --- | --- | --- |
| Complaint and vigilance data extraction | Yes | No | May contain patient data, GDPR special category |
| Literature title and abstract screening | Yes | Optional | High volume, public data, cost matters |
| Evidence synthesis and drafting | Possible | Yes, preferred | Long, precise English reasoning; data mostly non-personal |
| Claim-evidence cross-check | Yes | Yes (second opinion) | Two different models reduce shared errors |
| Formatting into templates | Not needed (deterministic) | Not needed | Templates are fixed |

**Competition.**
| Competitor | Type | Region | What it ships | AI depth | Price |
| --- | --- | --- | --- | --- | --- |
| DistillerSR | global platform | global | Literature review for CER/PER under MDR/IVDR, AI screening, re-rank, evidence extraction, Part 11 and Annex 11 | Deep | Not public |
| Veeva Vault Safety | incumbent | global | Case safety management with Falcon Safety agents and Vault AI narratives, from emerging biotech up | Deep | Not public |
| IQVIA Vigilance Platform | incumbent | global | SaaS pharmacovigilance with AI and ML case processing and translation | Deep | Not public |
| Regulatory consultancies (EU-wide) | consultancy | EU | Human-written CERs, PSURs, tech files | Low to medium | Day rates, not public |

Gap: small medtech manufacturers needing PSUR and tech-file drafting at a fixed price; avoid literature screening alone (DistillerSR) and drug safety case processing (Veeva, IQVIA).

**Challenge from five angles.**
- **Customer:** RA heads are accountable to notified bodies; they will not trust a newcomer without regulatory credentials. A partner RA consultant is required.
- **Incumbent:** DistillerSR already ships AI screening with audit trail; Veeva and IQVIA move down to emerging biotech.
- **Frontier labs and big tech:** General models write good regulatory prose; consultancies can use them directly with templates, shrinking the tool layer.
- **Regulator:** Validation expectations (Part 11, Annex 11, GAMP) for tools touching quality records add cost; the EU AI Act may also apply to tools used in safety processes.
- **Unit economics:** Each device family is different; review time by a qualified person remains, so margin depends on the consultant partner.

**After the challenge.** Survives only as a tool sold to and with RA consultancies (they carry liability and clients), focused on PSUR drafting and gap checks. Local models matter less here because most inputs are non-personal; the score stays near 60.

**Numbers.**
- MDR transition extended to 2027 and 2028 depending on class (2023 amendment, Wikipedia summary of Regulation 2017/745).
- Implementing Regulation (EU) 2026/977 on conformity assessment and notified bodies, May 2026 (European Commission).
- Team-NB: 57 member notified bodies, Aug 2026.
- European medtech: over 950,000 jobs, market about 173 billion EUR in 2025 *(third-party estimate, MedTech Europe)*.
- DistillerSR: AI re-rank "potentially cutting screening time by up to 70%" *(vendor claim)*.

**How to start.**
1. Weeks 1-4: PSUR drafting pipeline for one device class using public data (FDA MAUDE, published PSUR templates).
2. Weeks 5-8: partner with 1-2 RA consultants; co-produce real PSURs with their sign-off.
3. First 10 customers: consultancies first (each brings several manufacturers).
4. Pricing test: per-PSUR price vs consultancy seat subscription.

**Risks and limitations.**
- Domain credibility gap; no RA background on the team.
- Liability if a submitted document contains an error.
- Validation and QMS documentation for the tool itself.
- Rules change (2026 implementing acts, possible MDR reform).

**Kill criteria.** Stop if no RA consultancy agrees to a paid pilot within 3 months.

**Sources:** [Regulation (EU) 2017/745 on Wikipedia](https://en.wikipedia.org/wiki/Regulation_(EU)_2017/745) · [European Commission: medical devices new regulations](https://health.ec.europa.eu/medical-devices-sector/new-regulations_en) · [Team-NB documents](https://www.team-nb.org/team-nb-documents/) · [MedTech Europe: about the industry](https://www.medtecheurope.org/about-the-industry/) · [DistillerSR](https://www.distillersr.com/products/distillersr-systematic-review-software) · [Veeva Vault Safety](https://www.veeva.com/products/vault-safety/) · [IQVIA safety and pharmacovigilance](https://www.iqvia.com/solutions/safety-regulatory-compliance/safety-and-pharmacovigilance)

---

## 16. Polish phone and chat agent for local service businesses

**Region:** PL · **Buyers:** private clinics, car workshops, salons, small hotels · **Revenue model:** monthly subscription + per-minute usage · **Competition:** high · **Local-model fit:** low · **Score: 59** (M15 G13 C6 L7 F11 R7)

> Real demand, but crowded and thin-margin; only a narrow vertical with deep calendar integration survives.

**The asymmetry.** Polish SMEs adopt AI slowly (8.36% of enterprises in 2025 vs 19.95% EU; small firms 17% EU-wide, Eurostat 2025). Small service firms still answer the phone by hand, miss calls while working, and re-type bookings. Booking platforms already digitised the calendar (Booksy Biz from 145 PLN net per month, 2026), but the phone line and messages remain manual for many. The gap is narrowing fast because voice-agent platforms make building a bot cheap for everyone.

**Who pays and how much.** Count of PL clinics, workshops and salons: not found in this pass. Cost anchors: Booksy Biz 145 PLN net per month + 35 PLN per extra staff (*vendor price*, 2026-10-14). Voice infrastructure cost: Retell quotes $0.07-0.31 per minute all-in (*vendor price*, 2026-10-14). Buyer price to test: 300-900 PLN per month including a minute allowance. Channel: booking-software partners, local marketing agencies, workshop and clinic associations.

**The agentic app.**
1. Ingest: incoming call or chat, speech-to-text in Polish.
2. Extract: intent, service, date wishes, client identity.
3. Reason: check live calendar slots, business FAQ, price list.
4. Draft: spoken answer and proposed slot.
5. Verify: confirm details back to the caller; escalate to a human on doubt.
6. Act: book in the calendar; **human approval** for medical triage, refunds or anything outside the price list. Patient data handling under GDPR.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| Speech-to-text | Possible | Usually | Latency and Polish accuracy |
| Dialogue reasoning | Possible (Bielik 11B v3) | Usually | Sub-second latency at peak hours |
| Text-to-speech | Rarely | Yes | Natural Polish voices |
| Call summaries and analytics | Yes | No | Batch, cheap locally |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| Booksy | incumbent | PL/global | Booking platform for salons | AI phone agent not found in this pass | from 145 PLN net per month |
| Docplanner (ZnanyLekarz) | incumbent | PL/global | Clinic booking, phone tools | AI features: details not found in this pass | not found |
| Retell AI | global platform | global | Voice-agent infrastructure | High | $0.07-0.31 per minute |
| Voicebot.pl | startup | PL | Voicebots for business processes | Medium to high | not found |
| EasyCall | startup | PL | Voicebot for customer service | Medium | not found |
| Asseco voicebot | incumbent | PL | Chatbot and voicebot | Medium | not found |

Gap: horizontal vendors are many; a vertical (for example car workshops with their workshop software) may still be open. Booking platforms are the biggest threat because they own the calendar.

**Challenge from five angles.**
- **Customer:** owners dislike paying monthly; bad voice experience loses clients.
- **Incumbent:** Booksy and Docplanner can add a voice agent to millions of calendars at once.
- **Frontier labs and big tech:** realtime voice models keep getting cheaper and better in Polish; differentiation shrinks.
- **Regulator:** AI Act transparency (caller must know it is AI), GDPR for health data, call recording consent.
- **Unit economics:** per-minute costs plus support on a 300-900 PLN ticket; churn high.

**After the challenge.** Survives only as a vertical add-on (one trade, one software integration) or as a white-label for an agency. Local models matter little here. Score below 60.

**Numbers.**
- PL 8.36% vs EU 19.95% enterprise AI use, 2025 (Eurostat).
- Booksy Biz 145 PLN net per month (*vendor price*, 2026-10-14).
- Retell $0.055 per minute infrastructure, $0.07-0.31 per minute total (*vendor price*, 2026-10-14).
- Number of target SMEs: not found.

**How to start.**
1. Weeks 1-4: pick car workshops; build on a voice platform; integrate one workshop calendar.
2. Weeks 5-8: 3 free pilots; measure missed-call recovery.
3. First 10 customers: door-to-door in one city plus a workshop software partner.
4. Pricing test: 399 vs 699 PLN per month with minute caps.

**Risks and limitations.**
- Platform risk from booking incumbents.
- Polish voice quality and latency.
- Thin margins and churn.
- Regulatory disclosure duties.

**Kill criteria.** Stop if pilots do not show more booked jobs than cost within 6 weeks, or a booking incumbent ships a cheaper built-in agent.

**Sources:** [Eurostat: use of AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Booksy Biz pricing](https://biz.booksy.com/pl-pl/cennik) · [Retell pricing](https://www.retellai.com/pricing) · [Bielik-11B-v3.0-Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct)

---

## 17. Grant application co-pilot for Polish consultancies

**Region:** PL · **Buyers:** small grant consultancies and SMEs applying to FENG, KPO, FEnIKS and regional programmes · **Revenue model:** subscription per consultant seat + per-application fee · **Competition:** medium · **Local-model fit:** medium · **Score: 58** (M12 G13 C8 L7 F11 R7)

> Real paperwork and real money, but the buyer is the consultancy that sells the manual work, the calls are lumpy, and generic chat models already do the drafting part, so it only works as a tool for consultants, not against them.

**The asymmetry.** Polish SMEs apply for EU money through long forms, business plans and criteria checklists written mostly by consultancies. FENG alone has about 7.9 bn EUR for 2021-2027 (programme portal, as shown in search results, Oct 2026), with grant calls scheduled through 2026. Polish enterprise AI use was 8.4% in 2025 (Eurostat, 11 Dec 2025). We found no Polish product that drafts FENG or KPO applications with AI (Bing searches in Polish, 14 Oct 2026; results showed only general chat tools). The gap exists because each call has its own criteria, forms and Polish legal language, and consultancies are small and conservative. It will close fast once consultancies standardise on general chat tools.

**Who pays and how much.** Buyers: Polish grant consultancies (count not found) and SMEs that apply directly. Consultancy fees (fixed fee plus success fee) not found this session; do not quote a percentage without a source. Price points to test: 300-600 PLN per seat per month for consultancies, or 500-1,500 PLN per application for SMEs. Channel: consultancies first (they have the pipeline), then SME associations.

**The agentic app.**
1. Ingest: call documentation (regulamin, criteria, form templates) and the client's documents (financials, project idea).
2. Extract: eligibility rules, scoring criteria, required annexes, budget limits and state-aid rules.
3. Reason: eligibility check and a criteria-by-criteria scoring estimate with gaps.
4. Draft: project description, market analysis, indicators table and budget justification per section.
5. Verify: every claim tied to a source document; criteria coverage matrix; character limits.
6. Act: **human approval gate**: the consultant or company signs and submits; the agent never submits.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| Call document parsing | local | no | Public texts, high volume each call |
| Client financials and know-how | local | no | Trade secrets of the applicant, unpublished R&D ideas |
| Narrative drafting | local first | Claude for flagship sections | Quality of Polish prose drives the score |
| Criteria coverage check | local | no | Rule-like, cheap |
| Final review | no | paid model optional | Second opinion on high-value applications |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| Grantable | startup | US | Prospecting, writing desk, pipeline, library | high | 50 to 150 USD per month, agency hub 300 USD |
| Polish grant consultancies | consultancy | PL | Full application writing for a fee and success fee | low or unknown | not found |
| ChatGPT, Claude, Copilot | global platform | global | General drafting over uploaded call documents | generic | business plans |
| PARP and EU funds information points | incumbent | PL | Free advice on calls and eligibility | none | free |
| Granter and other Polish AI grant tools | startup | PL | not found in search on 14 Oct 2026 | not found | not found |

Grantable is built for US foundations, not EU structural-fund forms. Polish consultancies are the market, not the enemy: sell them speed.

**Challenge from five angles.**
- **Customer:** Consultancies may see the tool as a threat to their fee; SMEs that buy it directly lack the know-how to judge drafts.
- **Incumbent:** Large consultancies can build their own prompt libraries on general chat tools in weeks.
- **Frontier labs and big tech:** General models already draft good Polish prose; the remaining value is call-specific criteria and annex checks.
- **Regulator:** Funding agencies may add AI-use declarations or penalise boilerplate; false statements in an application have legal consequences, so verification is critical.
- **Unit economics:** Demand peaks around call deadlines and drops between them; churn between calls is the main threat.

**After the challenge.** Survives only as a criteria-checker and drafting tool sold to 10-30 consultancies, with local processing as a confidentiality argument for client R&D ideas. Score 58, below the top-15 bar unless a consultancy partner joins.

**Numbers.**
- FENG about 7.9 bn EUR for 2021-2027 *(programme portal via search snippet, Oct 2026)*.
- Poland 8.4% enterprise AI use in 2025 (Eurostat, 11 Dec 2025).
- Grantable 50, 150 and 300 USD monthly plans *(vendor claim, Oct 2026)*.
- Consultancy fee levels: not found.

**How to start.**
1. Weeks 1-3: parse one FENG call and one regional call into a criteria matrix.
2. Weeks 4-6: drafting and coverage check for 5 past successful applications donated by a consultancy.
3. Weeks 7-8: seat-based web app with local processing option.
4. First 10 customers: small consultancies of 2-10 people, 1-month free use before a call deadline.
5. Pricing test: per seat vs per application.

**Risks and limitations.**
- Seasonal demand tied to call calendars.
- Funding period 2021-2027 ends; the next perspective may change forms.
- Consultancies build their own tools on general chat models.
- Liability for false statements in applications.

**Kill criteria.** Stop if fewer than 5 consultancies pay after the first major call cycle.

**Sources:** [FENG portal](https://www.nowoczesnagospodarka.gov.pl) · [Eurostat AI use 2025](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2) · [Grantable pricing](https://www.grantable.co/pricing) · [Bielik 11B v3](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [PLLuM 12B instruct](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512)

---

## 18. Polish tax interpretation and case-law research agent

**Region:** PL · **Buyers:** tax advisory firms (doradcy podatkowi), in-house tax teams of mid-size and large firms, accounting offices with advisory desks · **Revenue model:** monthly subscription per seat, on-prem licence for firms that keep files in-house · **Competition:** high · **Local-model fit:** high · **Score: 52** (M10 G10 C5 L11 F9 R7)

> Technically easy and well suited to local models, but it competes with the two legal publishers that own the commentary and the customer relationship; viable only as an on-prem research layer over the free public sources plus the firm's own opinions.

**The asymmetry.** The raw material is public and free: individual tax interpretations (KIS) in the Ministry of Finance Eureka database and administrative court rulings (NSA and WSA) in the CBOSA database at orzeczenia.nsa.gov.pl. Searching them is still keyword-based, and an advisor reads dozens of interpretations to find the line of reasoning for one client question. Poland is a late AI adopter overall (8.36% of enterprises in 2025 vs 19.95% in the EU, Eurostat), while the professional, scientific and technical sector is the second-highest AI user EU-wide (40.43%), so tax advisors are likely to adopt faster than other Polish SMEs and the gap may close quickly (my inference). Why a gap exists: professional secrecy of advisors makes them reluctant to paste client facts into foreign cloud tools.

**Who pays and how much.** Number of licensed tax advisors in Poland: not found in this run. Advisors already pay for LEX (Wolters Kluwer) or Legalis (C.H.Beck) subscriptions; LEX Księgowość "z czatem AI" is listed from 159.60 PLN net per month (promotional, regular 168.00 PLN; lex.pl, read 14 Oct 2026), Legalis prices not found (site not reachable in this run). A research agent must cost less than an extra publisher module or prove hours saved. Test price: 200-500 PLN per seat per month, on-prem box for 10+ seats (hypothesis). Channel: Krajowa Izba Doradców Podatkowych regional events, tax conferences, LinkedIn.

**The agentic app.**
1. Ingest: crawl Eureka interpretations and CBOSA rulings (respecting terms and rate limits), plus the firm's own past opinions.
2. Extract: facts, question, position of the taxpayer, position of the authority, legal basis, outcome, date.
3. Reason: retrieve interpretations and rulings with similar facts; group them by line of reasoning; flag changes in the line over time.
4. Draft: research memo in Polish with citations (signature, date, court) and quotes.
5. Verify: every citation is checked against the stored source text; uncited claims are removed.
6. Act: human approval gate, the advisor signs any opinion; the agent never sends advice to a client.

**Local vs paid split.**

| Step | Local open model | Paid API | Why |
|---|---|---|---|
| Crawl and index public sources | embeddings model run locally | none | public data, volume |
| Extraction of facts and outcome | Bielik 11B v3 or Qwen class | none | high volume, Polish legal text |
| Retrieval over client facts | local only | none | professional secrecy of the advisor |
| Memo drafting | local model | frontier model only with anonymised facts, opt-in | quality on hard reasoning |
| Citation verification | no model, string match | none | deterministic |

**Competition.**

| Competitor | Type | Region | What it ships | AI depth | Price |
|---|---|---|---|---|---|
| LEX (Wolters Kluwer Polska) | incumbent | PL | legal information system with tax content, interpretations, rulings; LEX Księgowość, LEX Kadry and LEX Biuro Rachunkowe "z czatem AI", LEX Flex "z Expert AI" | specialised AI chat inside the subscription (vendor claim), depth not tested | LEX Księgowość from 159.60 PLN net per month (Oct 2026, promotional) |
| Legalis (C.H.Beck) | incumbent | PL | commentaries, journals, large case-law base, templates | AI features not verified in this run | not found |
| Eureka (Ministry of Finance) | public | PL | free database of tax interpretations | keyword search | free |
| CBOSA (orzeczenia.nsa.gov.pl) | public | PL | free database of administrative court rulings | keyword search | free |
| Harvey | global platform | global | legal AI assistant for law and tax firms | high (vendor claim) | not public |

Gap: publishers sell content plus search; a firm-side agent that mixes public sources with the firm's private opinion archive, on the firm's own hardware, is not something found in this run. Beat them on privacy and on the private archive, not on content.

**Challenge from five angles.**
- **Customer:** advisors already pay for LEX or Legalis and will not add a second tool without clear time savings; trust in citations is the whole product.
- **Incumbent:** both publishers own commentary, brand and contracts; adding RAG over their own corpus is cheap for them.
- **Frontier labs and big tech:** general assistants with web search can find interpretations; the defensible part is the private archive and on-prem deployment.
- **Regulator:** advisor remains responsible; professional secrecy favours local deployment; crawling public databases must respect their terms.
- **Unit economics:** small seat counts per firm; on-prem boxes add hardware support cost.

**After the challenge.** Survives only as a niche on-prem tool for mid-size advisory firms with a large private opinion archive; LEX already bundles an AI chat into accounting and payroll subscriptions at about 160 PLN per month, below my 200-500 PLN test price, so score drops to 52 (C5) and stays outside the top tier.

**Numbers.**
- AI use: PL 8.36% vs EU 19.95% of enterprises; EU professional, scientific and technical sector 40.43% (Eurostat, 2025 data).
- Number of tax advisors and in-house tax teams in Poland: not found in this run (kidp.pl home, "poznaj KIDP" and "30 lat KIDP" pages, pl.wikipedia and search result pages checked 14 Oct 2026; none states a count).
- LEX: AI chat in LEX Księgowość, LEX Kadry, LEX Biuro Rachunkowe; LEX Księgowość from 159.60 PLN net per month, regular 168.00 PLN (lex.pl, read 14 Oct 2026, vendor claim); launch date of the AI chat not found.
- Legalis AI features and prices: not found (legalis.pl and beck.pl not reachable in this run, 14 Oct 2026).
- Bielik 11B v3 Instruct, Apache 2.0, base dated 30 Jul 2025 (Hugging Face model card).

**How to start.**
1. Weeks 1-4: index one tax topic (VAT on construction services) from Eureka and CBOSA; citation-checked memo generator.
2. Weeks 5-8: add private archive import and a local deployment script.
3. First 10 customers: boutique advisory firms met through KIDP events; free pilot on one live topic each.
4. Pricing test: seat price vs firm-wide on-prem licence.

**Risks and limitations.**
- Publishers add the same feature to their existing subscriptions.
- Hallucinated citations destroy trust instantly.
- Public database access can change or be rate-limited.
- Small market of buyers with budget.

**Kill criteria.** Stop if pilots show less than 30% time saved per research question or no firm converts after 2 months.

**Sources:** [Eureka](https://eureka.mf.gov.pl/) · [CBOSA](https://orzeczenia.nsa.gov.pl/) · [Legalis](https://legalis.pl) · [LEX](https://www.lex.pl) · [KIDP](https://kidp.pl/) · [Eurostat AI use](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Bielik 11B v3 Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [Harvey](https://www.harvey.ai)

---

## Ideas that did not survive the challenge

These candidates were researched with the same template. They failed on competition, budget, model quality or
regulation, or a stronger idea in the same space absorbed them. Each note names the reason and the evidence.

### Housing community and property manager back office

The idea: an agent for administrators of housing communities and cooperatives (wspólnoty mieszkaniowe, spółdzielnie) that reads resident letters, drafts resolutions and replies, reconciles fee payments and prepares annual reports. Score: **56** (M10 G14 C9 L9 F7 R7). Real estate is not a laggard on paper: 24.82% of EU real-estate enterprises used AI in 2025, above the 19.95% all-sector rate (Eurostat, 2025), although Poland overall is at 8.36%. Counts of Polish housing communities and managers, and what they pay today: not found in this pass (searches returned no usable results). Fails the challenge mostly on access: buyers are many tiny firms on entrenched accounting and administration programs, the reader has no domain knowledge, and the per-community budget is small. Local models help a little (resident personal data), but not enough to justify a box. Worth revisiting with a partner who manages buildings.

**Sources:** [Eurostat: use of AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

### Real estate due diligence from land registers and zoning plans

The idea: an agent that reads a księga wieczysta (land and mortgage register), the local zoning plan (MPZP) or zoning decision (WZ) and notarial deeds, and drafts a risk report for buyers, agents, banks and small developers. **Score: 55** (M11 G12 C10 L5 F9 R8). The register data is already sold cheaply and online: EKW+ searches 24.8+ million registers and 40+ million parcels and sells register reports from 35 PLN for one down to 12 PLN each in a pack of 100, plus a new "Raport o działce" (parcel report) *(vendor pricing, Oct 2026)*. Searching Bing for AI register-analysis and due-diligence tools ("sztuczna inteligencja analiza ksiąg wieczystych", "due diligence nieruchomości koszt raportu") found no dedicated AI product in this run, so there is some room. But it fails the local-model test: registers and zoning plans are public data, so a cloud frontier model is allowed and better. Only the deeds and the buyer's file are confidential. Liability for a missed mortgage or easement sits with whoever signs the report, so the real buyers are notaries and lawyers, who are covered by the legal profile. Data APIs (register access, zoning-plan geometry) also differ by municipality. Better sold as a module of the legal assistant than as a standalone business.

**Sources:** [EKW+](https://ekw.plus/) · [Bing search: AI land register analysis](https://www.bing.com/search?q=sztuczna+inteligencja+analiza+ksiąg+wieczystych+aplikacja) · [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

### Farm subsidy paperwork agent

The idea: an agent that prepares ARiMR applications (area payments, eco-schemes, ad-hoc aid such as the fertiliser and diesel aid call that opened on 1 Oct 2026 with a deadline of 23 Oct, as shown in search results) and farm records for farmers and ODR advisors. **Score: 54** (M11 G16 C10 L8 F5 R4).
Why it fails the challenge: ARiMR already pre-fills the eWniosekPlus application with parcel and map data, and state ODR advisory centres help with it for free or at low cost, so the paid gap is thin. Farmers' willingness to pay for software is low, and the sale is offline and seasonal. Searches for AI tools for Polish farm subsidy applications (Bing, 14 Oct 2026) returned only general chat tools, so competition is low. But the agency controls the form, can change it every year and can add its own assistant. Local models help with farm data privacy, but that is not a strong buying reason here. The number of farms (about 1.3 million, from the brief) and the number of applications were not verified this session.
**Sources:** [eWniosekPlus](https://ewniosek.arimr.gov.pl) · [Eurostat AI use 2025](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2)

### AI back-office agents for German tax advisor firms (Steuerberater)

The idea: agents that pre-book receipts, draft client letters and prepare returns for German Steuerberater firms facing staff shortages, run on-prem for professional secrecy. **Score: 52** (M15 G12 C6 L10 F4 R5).
Why it fails the challenge: the ecosystem is locked by DATEV, a cooperative with over 40,000 members and 9,000 staff (DATEV company page, read 14 Oct 2026). Any agent must integrate with DATEV, and DATEV decides how its own AI features roll out.
AI startups are already in the niche: Taxy.io ships an AI workspace for tax and legal questions and an MCP connector (website, Oct 2026), and receipt tools like Candis integrate with DATEV (pricing page not reachable this session).
For this reader the fatal point is feasibility: the sale, support and tax law are all in German, and the reader sells in Polish and English. Trust also depends on local presence and chamber networks.
A survey figure on AI use in Kanzleien and the count of Steuerberater were searched (BStBK, DATEV pages) but not retrieved this session: not found.
Better done by a German founder; a Polish version (biura rachunkowe) is a stronger fit for this reader.

**Sources:** [DATEV company](https://www.datev.de/web/de/m/ueber-datev/das-unternehmen/) · [Taxy.io](https://www.taxy.io/) · [Eurostat: Use of AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

### Transfer pricing documentation and TP-R agent for Polish mid-size groups

Idea: an agent that drafts the local file, prepares benchmarking narrative and fills the TP-R report from the ledger for Polish companies in groups. Score: 51 (M7 G10 C8 L12 F6 R8).
Why it fails the challenge: the buyers are few (only firms above the statutory transaction thresholds; filer count not found in this run) and they already buy the work from Big Four and boutique TP advisors, who keep the liability. Benchmarking needs paid company databases that a bootstrapped firm cannot license cheaply. Domain knowledge (OECD guidelines, Polish thresholds, TP-R schema) is deep and the reader lacks it, so time to an MVP is long and the sales cycle runs through CFOs once a year. Local models fit well (group financial data is confidential), but that is not enough to offset the small market. Better as a feature sold to TP advisory boutiques than as a product. Threshold and deadline details were not retrieved in this run (podatki.gov.pl redirect not followed in time).
Sources: [podatki.gov.pl transfer pricing](https://www.podatki.gov.pl/ceny-transferowe) · [Eurostat AI use](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

### CBAM and EUDR reporting for SME importers

The idea: an agent that collects supplier emissions data (CBAM) and geolocation and due diligence statements (EUDR) for SME importers. Score: **51** (M8 G12 C8 L6 F10 R7). Why it fails the challenge: the 2025 CBAM simplification (Regulation (EU) 2025/2083) added a 50 tonne annual import threshold; the Commission's Omnibus I material put the effect at about 90% of importers exempted with about 99% of emissions still covered (figures from the Feb 2025 proposal, not re-fetched in this run, so treat as unverified), so the SME market mostly disappeared; the remaining importers are larger and use brokers and ESG platforms. CBAM's definitive regime applies from 1 Jan 2026 (European Commission). EUDR was postponed again: large and medium operators from 30 Dec 2026, micro and small from 30 Jun 2027, with simplification amendments adopted in Dec 2024 and Dec 2025 (European Commission EUDR page, read Oct 2026). Repeated delays make buyers wait. Data is supplier data, not secret, so local models add little. Competitor scan was thin in this run (search engines returned nothing usable); not a credible "no competitor" claim.

**Sources:** [EC CBAM](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en) · [EC CBAM legislation](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-legislation-and-guidance_en) · [EC EUDR](https://environment.ec.europa.eu/topics/forests/deforestation/regulation-deforestation-free-products_en)

### European Accessibility Act audits and remediation

The idea: an agent that audits e-shops and service sites against EAA requirements (WCAG-based), then drafts fixes and the accessibility statement. Score: **48** (M11 G10 C5 L3 F12 R7). Why it fails the challenge: in Poland the EAA is the act of 26 Apr 2024 (Dz.U. 2024 poz. 731), in force 28 Jun 2025; enforcement sits with the President of PFRON and market surveillance authorities, fines go up to ten times the average monthly salary, and services offered by microenterprises are exempt (act text, Sejm ELI). So the fine anchor is small and the smallest shops are out of scope. Accessibility testing is a crowded, mature market (automated scanners, overlay vendors, accessibility agencies); competitors were not re-checked in this run, but the category is well known to be saturated. Public websites hold no secrets, so local models give no edge (L3).

**Sources:** [Dz.U. 2024 poz. 731 via Sejm ELI API](https://api.sejm.gov.pl/eli/acts/DU/2024/731/text.pdf)

### Cross-border marketplace listing operations

The idea: an agent that localises catalogues and runs listings for Polish SMEs selling on Allegro CZ/SK/HU, Amazon EU, Kaufland and eMAG. Score: **45** (M12 G6 C4 L5 F11 R7). Fails the challenge on saturation and on the adoption gap: online retail is one of the more AI-ready parts of the economy, marketplaces themselves push translation and listing tools to sellers, and listing integrators plus a large number of AI listing generators already exist. I could not confirm details of Allegro's own translation tooling in this pass (search returned only landing pages), so the saturation verdict rests on the visible number of vendors and on marketplace incentives, not on a measured count. Product texts are not secret, so local models add only cost savings at volume; frontier APIs do multilingual copy better and cheaply. A thin niche may remain in compliance-heavy categories (labels, safety data), but it is not an adoption-gap play.

**Sources:** [Eurostat: use of AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Allegro](https://allegro.pl)
