# Where AI adoption is still low

This chapter is the evidence base for the whole course. An "asymmetry" exists where buyers still pay people for
slow manual work while AI that could do it is already cheap. The data below shows where that is true: by country,
by company size, by sector, and by the reasons firms give for not adopting.

All enterprise figures come from the EU ICT-usage survey (Eurostat datasets `isoc_eb_ai` and `isoc_eb_ain2`),
enterprises with 10+ employees, all sectors except agriculture, mining and finance, unless stated. I pulled them from
the Eurostat API on 14 Oct 2026; the dataset was last updated 15 Jun 2026. **The 2025 survey is the latest; 2026
values were not published at the time of writing.** Micro firms (under 10 people) are not in the EU headline numbers.

## 1. Europe: a three-to-one gap between the north and the east

Share of enterprises using at least one AI technology (indicator `E_AI_TANY`), 2023 to 2025
([Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table)):

| Country | 2023 | 2024 | 2025 | Note |
|---|---|---|---|---|
| Denmark | 15.2% | 27.6% | 42.0% | highest in the EU |
| Finland | 15.1% | 24.4% | 37.8% | |
| Sweden | 10.4% | 25.1% | 35.0% | |
| Netherlands | 14.1% | 23.1% | 33.2% | |
| Germany | 11.6% | 19.8% | 26.0% | |
| **EU-27 average** | 8.1% | 13.5% | **20.0%** | |
| France | 5.9% | 9.9% | 18.2% | |
| Czechia | 5.9% | 11.3% | 17.6% | |
| Italy | 5.1% | 8.2% | 16.4% | |
| Hungary | 3.7% | 7.4% | 10.4% | |
| Greece | 4.0% | 9.8% | 8.9% | |
| Bulgaria | 3.6% | 6.5% | 8.6% | |
| **Poland** | 3.7% | 5.9% | **8.4%** | second lowest in the EU |
| Romania | 1.5% | 3.1% | 5.2% | lowest in the EU |

What this means:
- Poland's adoption grew from 3.7% to 8.4% in two years, but the EU grew faster, so **the gap widened from 4.4 to
  11.6 percentage points** (2023 to 2025). The EU average is 2.4 times Poland's rate.
- Poland is below every Central European neighbour: Czechia 17.6%, Slovakia 18.0%, Lithuania 21.3% (2025).
- About **91.6% of Polish firms with 10+ staff used no AI in 2025**; only 4.3% of non-users had even considered it
  (EU: 14.2%) ([Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table)).

### By company size (2025)

| Size class | EU-27 | Poland | EU / PL |
|---|---|---|---|
| Small (10-49 staff) | 17.0% | 5.8% | 2.9x |
| Medium (50-249) | 30.4% | 14.8% | 2.1x |
| Large (250+) | 55.0% | 45.8% | 1.2x |
| All 10+ | 20.0% | 8.4% | 2.4x |

Source: [Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table), 2025.

The asymmetry is a **small and medium firm problem**. Large Polish firms are close to the EU (45.8% vs 55.0%). Small
Polish firms are at 5.8%, roughly where the EU average was in 2023. That is the segment this course targets.

## 2. Poland in detail

**GUS (Statistics Poland).** The yearly report "Społeczeństwo informacyjne w Polsce w 2025 r." (Warsaw and
Szczecin, 2025) says ([GUS PDF](https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultaktualnosci/5497/1/19/1/spoleczenstwo_informacyjne_w_polsce_2025.pdf)):
- 8.7% of enterprises used AI in 2025 (GUS counts a slightly wider set of sectors than the Eurostat headline, hence
  8.7% vs 8.4%).
- Highest: large firms 42.0% and the "Information and communication" section 37.8%.
- Lowest: small firms 6.1% and **construction 2.6%**.
- By region: Mazowieckie 12.5% (highest), Warmińsko-Mazurskie 5.1% (lowest).
- 91.3% of firms did not use AI; only 3.9% did not use it but were considering it.
- In public administration, 6.8% of units used AI in 2024 (central government 24.1%, local government 6.1%).

**Other Polish surveys disagree on the level, not on the direction.** The Polish Economic Institute (PIE) review
"AI w polskich przedsiębiorstwach" (press release 24 Sep 2025) puts AI use at "from almost 6 to 16 percent of firms
depending on the method"; PIE and Ministry of Development (MRiT) data show 16% of micro and 15% of small firms using
AI tools, and **77% of non-users do not plan to adopt AI "until it becomes necessary"**. Almost 90% of firms that do
not plan to adopt are fully Polish-owned. PIE also notes that AI use often starts bottom-up, from employees, so real
use (staff on free chatbots) is likely higher than the official numbers
([PIE, 24 Sep 2025](https://pie.net.pl/wp-content/uploads/2025/09/2025-09-22_Z-AI-korzysta-mniej-niz-co-szosta-firma-w-Polsce-a-pozostale-nie-planuja-jej-wdrazac-1.pdf)).
*(third-party estimate)* for the PIE/MRiT numbers; method differs from GUS.

My reading: individual employees in Polish SMEs already paste text into ChatGPT, but **firms have not bought or
built AI into their processes**. The gap is in process-level automation, not in awareness.

**What the few Polish adopters use it for (2025, share of AI-using firms).** Business administration and management
42.9% (EU 31.0%), accounting and finance 30.7% (EU 23.1%)
([Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table)). Back-office use
cases are where Polish adopters start, which supports back-office agents as an entry point.

**Text analysis is the widest gap.** Only 2.1% of Polish firms use AI text mining, vs 11.8% in the EU (2025), a 5.6x
gap ([Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table)). Reading
documents, the thing agents now do well, is the least adopted AI technology in Poland relative to the EU.

**Polish AI policy, briefly.**
- **PLLuM**: the government-funded Polish LLM family, published on Hugging Face by the Ministry of Digital Affairs
  organisation `CYFRAGOVPL` (e.g. [PLLuM-12B-instruct-2512](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512));
  licences differ per model (some non-commercial), so check each card. It backs an assistant in the mObywatel app
  ([iMagazine, 2 Jan 2026](https://imagazine.pl/2026/01/02/mobywatel-wchodzi-w-2026-rok-z-polskim-ai/)).
- **Bielik**: the community-built SpeakLeash model, v3 family including
  [Bielik-11B-v3.0-Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) (Apache-2.0 per its model
  card) ([bielik.ai](https://bielik.ai/)).
- **AI factories**: EuroHPC lists two Polish AI Factories, **PIAST** and **Gaia**; the Gaia project "aims to
  accelerate the development and increase the adoption of cutting-edge AI technologies in Poland"
  ([EuroHPC AI Factories](https://www.eurohpc-ju.europa.eu/ai-factories_en), read 14 Oct 2026). Budgets, host sites
  and SME access terms: not verified in this session.

For a vendor, policy matters in one way: Polish-language open models now exist with usable licences, so "Polish,
on-prem, no data leaves the office" is a buildable product, not a slogan. Chapter `03-LOCAL-FIRST.md` covers this.

## 3. By sector: who uses AI least

Share of enterprises using AI, 2025, selected NACE sectors
([Eurostat isoc_eb_ain2](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ain2/default/table)):

| Sector (NACE) | EU-27 | Poland | Comment |
|---|---|---|---|
| Construction (F) | 10.8% | 2.4% | lowest in both; huge paperwork load |
| Transport and storage (H) | 11.2% | 3.0% | freight docs, dispatch, customs |
| Real estate (L) | 24.8% | 4.1% | 6x gap to EU |
| Food manufacturing (C10-C12) | 12.5% | 5.0% | |
| Accommodation and food service (I) | 12.0% | 5.6% | |
| Motor vehicle trade and repair (G45) | 14.4% | 5.9% | |
| Waste and water (E) | 13.1% | 6.0% | |
| Retail (G47) | 15.5% | 7.1% | |
| Manufacturing, all (C) | 17.3% | 7.7% | |
| Wholesale (G46) | 23.4% | 11.2% | |
| Legal, accounting, consultancy (M69-M71) | 37.9% | 20.5% | high, but still half of EU |
| Professional, scientific, technical (M) | 40.4% | 22.2% | |
| Information and communication (J) | 62.5% | 38.1% | |
| Computer programming and IT services (J62-J63) | 65.7% | 42.0% | highest |

Patterns:
- **Low everywhere**: construction, transport, accommodation and food, traditional manufacturing. These sectors are
  low in the whole EU, not only in Poland, so a product built for them can sell in both markets.
- **Low in Poland only**: real estate (4.1% vs 24.8%) and legal and accounting (20.5% vs 37.9%). These are document
  businesses where the EU already shows demand, so the Polish gap is likely to close; the question is who closes it.
- **ICT is saturated**: IT firms already use AI at 42% to 66%. Selling AI to IT companies means competing with the
  buyer's own engineers.

## 4. Global comparison

- **United States (Census Bureau BTOS).** The Census Business Trends and Outlook Survey asks firms every two weeks
  whether they used AI to produce goods or services ([Census BTOS](https://www.census.gov/hfp/btos/data)). I could
  not retrieve the current rate in this session, so no figure is given here; read the latest value on that page. Note
  that BTOS covers all firm sizes including micro firms and uses a different question, so it is not directly
  comparable with Eurostat.
- **Large-company surveys** (McKinsey "The State of AI",
  [mckinsey.com](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai); Microsoft's AI
  diffusion reports) mostly sample large firms or individual users and report much higher usage. I could not load
  their current editions in this session: not verified, so no numbers are quoted.
- **The consistent pattern** in the data I could verify: large firms adopt 2x to 3x more than small ones (EU 55.0%
  vs 17.0%, Poland 45.8% vs 5.8%, Eurostat 2025). Headline "most companies use AI" figures describe large companies
  and individual staff, not small firms' processes. Do not use them to size an SME market.

## 5. Why firms do not adopt, and what each barrier means for a vendor

Eurostat asks firms that **considered AI but did not use it** why. Shares of those firms, 2025
([Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table), unit "% of
enterprises which ever considered AI"):

| Barrier | EU-27 | Poland | What an agentic-app vendor can offer |
|---|---|---|---|
| Lack of relevant expertise | 70.3% | 62.6% | Done-for-you service: the vendor configures, runs and maintains; the buyer never "learns AI" |
| Lack of clarity about legal consequences | 53.6% | 52.3% | AI Act and GDPR paperwork in the box: DPIA template, audit log, human approval step |
| Data protection and privacy concerns | 52.7% | 49.4% | Local models on a box at the customer or in a Polish/EU data centre; no data to US clouds |
| Data availability or quality | 43.5% | 33.4% | Start from the documents they already have (PDF, scans, e-mail), not from a data project |
| Incompatibility with existing systems | 41.6% | 40.9% | Integrate with Polish tools (KSeF e-invoicing, Subiekt, Optima, Symfonia) or work via e-mail and files |
| Costs seem too high | 38.4% | **55.5%** | Fixed monthly price, per-document pricing, cheap local inference at volume |
| Ethical considerations | 24.6% | 26.6% | Human-in-the-loop, explainable drafts, no autonomous decisions on people |
| AI not useful for the business | 17.8% | **34.6%** | Sell a measured outcome (hours saved, invoices processed), not "AI" |

Two Polish differences matter for pricing and sales:
- **Cost is the second barrier in Poland (55.5%) but sixth in the EU (38.4%).** Polish SMEs are price-sensitive;
  local inference that keeps the marginal cost near zero is a selling argument, not only a privacy one.
- **One in three Polish considerers thinks AI is "not useful"** (34.6% vs 17.8% EU). Pitch the task, not the
  technology. Combined with PIE's "77% will not adopt until necessary", Polish sales cycles will need proof on the
  buyer's own documents.

Caveat: only 4.3% of Polish non-users ever considered AI, so these percentages describe a small group. The other
roughly 87% of firms have not thought about it at all, which is both the opportunity and the sales problem.

## 6. Where AI is already saturated: avoid

These categories are crowded with global platforms and cheap or free tools. A small Polish vendor has no edge there
(my judgement, supported by Eurostat: generating language or code is used by 8.8% of EU firms and generating images,
video or audio by 9.6% in 2025, both above most other AI technologies, and marketing and sales is the top AI purpose at 6.9%
([Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table))):

| Category | Why to avoid |
|---|---|
| Customer-service chatbots on websites | Bundled into every helpdesk and CRM; many local chatbot agencies |
| Marketing copy, social posts, images | Built into Canva, Google, Meta and Microsoft tools; free tiers |
| Coding assistants | Dominated by frontier labs and IDE vendors; ICT firms already at 42% to 66% AI use |
| Meeting notes and transcription | Built into Teams, Zoom, Google Meet |
| Generic "chat with your documents" | Copilot, ChatGPT and Gemini enterprise plans ship it |
| Generic translation | DeepL and the big platforms; commodity price |

The test for a new idea: if Microsoft 365 or Google Workspace already does it in a menu, it is not an asymmetry.

## 7. The asymmetry map

| Segment | Adoption signal | Main barrier | What an agent vendor can offer |
|---|---|---|---|
| Polish small firms (10-49) overall | 5.8% vs EU 17.0% (2025) | Cost (55.5% of PL considerers) | Fixed low price, local inference, no setup project |
| Construction (PL and EU) | 2.4% PL, 10.8% EU (2025) | Expertise; field work, paper-heavy | Tender, bill of quantities and site-doc agents working from e-mail and scans |
| Transport and logistics | 3.0% PL, 11.2% EU (2025) | Incompatibility with TMS and paper flows | Freight-document and customs-paper extraction into existing systems |
| Real estate (PL) | 4.1% PL vs 24.8% EU (2025) | Expertise | Listing, lease and property-management document agents in Polish |
| Accommodation and food | 5.6% PL, 12.0% EU (2025) | Expertise and cost | Back-office (invoices, supplier orders, staffing paperwork), not guest chatbots |
| Food and traditional manufacturing SMEs | 5.0% to 7.7% PL (2025) | Data protection, incompatibility | On-prem agents for quality docs, orders and certificates |
| Legal and accounting (PL) | 20.5% PL vs 37.9% EU (2025) | Legal clarity, professional secrecy | Local-model drafting and document review with audit trail |
| Text-heavy back offices (PL) | text mining 2.1% PL vs 11.8% EU (2025) | Data protection (49.4%) | Document-reading agents on a local box; human approval before any action |
| Local public administration (PL) | 6.1% of local units (2024) | Legal clarity, procurement | Not a first target: slow procurement; revisit with a reference customer |

How to read it: the best cells combine **low measured adoption**, **document-heavy manual work**, and a barrier that
a small vendor can remove (expertise, privacy, cost). Chapter `02-OPPORTUNITIES.md` turns these cells into scored
business profiles; chapter `03-LOCAL-FIRST.md` covers the local-model argument; for the hybrid architecture see
[../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md](../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md).

## Limits of this data

- Eurostat excludes firms under 10 employees and the financial sector; most Polish businesses are micro firms, so
  the true picture for one-person firms is not measured here (PIE/MRiT suggest 16% of micro firms use some AI tool).
- "Uses AI" counts a firm that uses one tool once. It does not measure depth; real process automation is lower.
- 2025 figures were collected in early 2025. Adoption roughly doubled every year in 2023 to 2025, so in late 2026
  the levels are likely higher; the relative gaps (PL vs EU, small vs large, construction vs ICT) are the stable
  signal.
- The US and large-company comparisons (section 4) could not be verified in this session.
