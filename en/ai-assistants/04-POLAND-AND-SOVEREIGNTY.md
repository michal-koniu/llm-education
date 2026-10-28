# Poland and data sovereignty — an assistant that does not send data to the US

**As of 11 October 2026.**

> ⚖️ **This is not legal advice.** This is educational material: I summarize statutes, guidelines of professional
> self-governing bodies and commentary, always pointing to the act and article or the document. Regulations and their
> interpretations change fast (the AI Act after the Omnibus, the new Polish act, the appeal over the DPF). Before you
> base a product, a contract or a professional decision on this — ask a legal adviser (radca prawny) or an advocate
> (adwokat). Prices and figures carry a date and a source; the hardware and models were not measured on my machine —
> these are numbers from community benchmarks and manufacturers' websites.

This part answers the question I ask myself about every assistant for a lawyer, a doctor or a tax adviser: **what has
to happen so that the client's data does not leave the office — and will anyone pay for it?** First the law (why "not
to the US" is not a whim), then professional secrecy, the AI Act and the Polish act, competition, the market, models,
hardware and finally opportunities and risks. Product profiles are in [01-PROFILES.md](01-PROFILES.md), technical
patterns in [03-TECHNICAL-PATTERNS.md](03-TECHNICAL-PATTERNS.md).

---

## Table of contents

- [The shortest answer](#the-shortest-answer)
- [1. Why not the USA](#1-why-not-the-usa)
- [2. Professional secrecy](#2-professional-secrecy)
- [3. The AI Act and the Polish act](#3-the-ai-act-and-the-polish-act)
- [4. Competition in the EU and in Poland](#4-competition-in-the-eu-and-in-poland)
- [5. Adoption in Poland](#5-adoption-in-poland)
- [6. Polish and open models for local work](#6-polish-and-open-models-for-local-work)
- [7. Desktop hardware](#7-desktop-hardware)
- [8. Product opportunities, risks and market entry](#8-product-opportunities-risks-and-market-entry)
- [Sources for this part](#sources-for-this-part)

---

## The shortest answer

- **An EU region of a US provider is not sovereignty.** The CLOUD Act (18 U.S.C. § 2713) reaches data that a US company
  "controls", regardless of where the server is located. Microsoft France under oath: "Non, je ne peux pas le garantir".
- **A box on the desk removes three problems at once:** no processor (Art. 28 GDPR, in Polish RODO) for the AI part,
  no transfer outside the EEA (Art. 44–49 GDPR) and no dependence on the fate of the DPF (appeal C-703/25 P pending).
- **Every profession of public trust has a statutory secrecy with no time limit** (advocate, legal adviser, doctor, tax
  adviser, notary, statutory auditor), and breaching it can be a crime (Art. 266 § 1 of the Criminal Code, KK). The
  professional bodies have already added rules for AI: NRA § 23e (June 2026), KIDP (January 2026), KEL Art. 12 (from
  1 January 2025).
- **The AI Act today:** Art. 4 (competence), Art. 5 (prohibitions), Art. 50 (transparency, from 2 August 2026).
  High risk under Annex III only from 2 December 2027 — and only if the functions move into triage, scoring or the
  administration of justice.
- **The Polish act (Dz.U. 2026 item 1003)** gives, from 28 October 2026, a binding individual opinion from KRiBSI for
  PLN 150; no answer within the deadline = an opinion consistent with the application (Art. 12(3)).
- **The market is "EU cloud", not "on the desk".** Beck-Noxtua (PLN 590 net/month), Noa Notes (PLN 199 + VAT, AWS and
  Azure), LEX Expert AI — all in the cloud. Closest to "on-prem" is Gaius-Lex, but for firms of 20–99 lawyers.
- **The models are ready:** Qwen3.5/3.6-27B and Gemma-4-31B for reasoning, Bielik v3 for Polish, Whisper for speech.
  Hardware: from the Mac mini M5 Pro (PLN 8,499) to the ASUS GX10 (PLN 24,499) for law firms.

---

## 1. Why not the USA

### CLOUD Act: control counts, not the server's address

**18 U.S.C. § 2713** (CLOUD Act, 23 March 2018) requires a provider to disclose data "within such provider's possession,
custody, or control, regardless of whether such communication, record, or other information is located within or
outside of the United States" ([Cornell LII](https://www.law.cornell.edu/uscode/text/18/2713)).

- **EDPB and EDPS (joint response to the LIBE committee, 12 July 2019):** without an international agreement (e.g. an
  MLAT) a provider subject to EU law "cannot legally base the disclosure and transfer of personal data to the US on such
  requests" ([EDPB PDF](https://www.edpb.europa.eu/sites/default/files/files/file2/edpb_edps_joint_response_us_cloudact_annex.pdf)).
  In practice: a US provider can end up between a US order and the GDPR, and **a professional client will not resolve
  that conflict**.
- **Art. 48 GDPR** says the same from the EU side: a judgment or decision of a third-country authority is recognized
  only on the basis of an international agreement ([GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj)).
- **French Senate, June 2025:** Microsoft France's legal director Anton Carniaux, asked under oath whether French
  citizens' data would never reach US authorities without France's consent, answered: **"Non, je ne peux pas le
  garantir"** — adding that it had not happened so far ([The Register, 25 July 2025](https://www.theregister.com/2025/07/25/microsoft_admits_it_cannot_guarantee/)).
- **Microsoft's "European digital commitments" (30 April 2025):** a promise to challenge orders and to pay damages —
  that is a **contractual safeguard, not legal immunity** ([Microsoft blog](https://blogs.microsoft.com/on-the-issues/2025/04/30/european-digital-commitments/), *company data*).

**What this means for a desk assistant:** data that lies only on a device the professional physically controls is
reachable only through Polish procedure, with its guarantees of secrecy. US hardware (a Mac, an NVIDIA box) is not a US
service — provided telemetry is turned off and documented.

### DPF: a third invalidation is a real scenario for 2027

| Date | Event | Source |
|---|---|---|
| 10 July 2023 | The Commission adopts the adequacy decision for the EU–US Data Privacy Framework (DPF) | [European Commission](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/eu-us-data-transfers_en) |
| 3 September 2025 | The EU General Court dismisses the Latombe action (T-553/23), the DPF stands | [WilmerHale (blog)](https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20251201-european-court-of-justice-to-review-challenge-to-eu-us-data-privacy-framework) |
| 31 October 2025 | Appeal to the CJEU, case **C-703/25 P** — pending, no hearing date (July–August 2026) | [secureprivacy (blog)](https://secureprivacy.ai/blog/is-the-eu-us-data-privacy-framework-at-risk-the-ftc-ruling-explained-2026) |
| 29 June 2026 | US Supreme Court, Trump v. Slaughter: protection of FTC commissioners from removal is unconstitutional; the 2023 decision relies on the FTC's independence | [Skadden (blog)](https://www.skadden.com/insights/publications/2026/07/supreme-court-decision-raises-new-questions) |
| early to mid 2027 | Expected CJEU judgment (Skadden's estimate, July 2026) | ibid. |

- Microsoft was reportedly to be admitted as an intervener on the Commission's side (4 June 2026) — **unverified** (only
  a DataGuidance headline). The expiry of FISA 702 on 12 June 2026 — **unverified** in a primary source (only Wikipedia).
- After Safe Harbor (2015) and Privacy Shield (2020), **every US cloud assistant lives on the DPF or on SCCs with a
  transfer assessment**. A box on the desk does not depend on the judgment — that is a lasting sales argument, not a
  momentary one.

### GDPR in practice for a desk assistant

| Provision | What it says | What it means for the assistant |
|---|---|---|
| Art. 9(1), (2)(h), (3) GDPR | Ban on processing special categories of data (health etc.); exception for health care when processed by a person bound by secrecy | A medical scribe processes health data lawfully only "under the responsibility" of the doctor — the provider should not see it |
| Art. 10 GDPR | Data on convictions and offences | Concerns defense counsel in criminal cases — the same rules as for special-category data in the project |
| Art. 28 GDPR | A processor needs a contract under Art. 28(3); a sub-processor — consent | Every cloud API is a processor. **A box vendor with remote service access also becomes a processor** — hence "support without access" or a ready data-processing agreement |
| Art. 32 GDPR | Security of processing | Disk encryption, per-user accounts, logs, backups — locally this is the obligation of the client and the product |
| Art. 33–34 GDPR | Reporting breaches | Theft of the box is a personal data breach (Art. 4(12)); notification to UODO (the Polish data protection authority) within 72 h (Art. 33), unless the risk is unlikely. Lack of encryption usually also means a duty to notify individuals (Art. 34); encryption can exempt from it (Art. 34(3)(a)) |
| Art. 35(3)(b) + recital 91 GDPR | DPIA for large-scale special-category data; recital 91: a single doctor or lawyer is not "large scale" | A solo practice usually has no mandatory DPIA; a clinic and a larger law firm do. **A ready DPIA template is a cheap sales asset** |
| Art. 44–49 GDPR | Transfers outside the EEA: adequacy (Art. 45), SCCs (Art. 46), derogations (Art. 49) | A local model = no transfer for the AI part; US cloud = DPF or SCCs + transfer assessment |
| Art. 48 GDPR | A third-country court order only through an international agreement | See the CLOUD Act above — the conflict of laws lies on the provider's side |
| Art. 24(2)–(6) of the Patients' Rights Act (Dz.U. 2024 item 581) | IT staff and the processor of medical records act on authorization and are bound by secrecy, also after the patient's death | A company servicing the box in a practice enters the medical secrecy regime |

Sources: [GDPR, EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [recital 91](https://gdpr-info.eu/recitals/no-91/),
[Patients' Rights Act](https://api.sejm.gov.pl/eli/acts/DU/2024/581/text.pdf). Additionally EDPB, Opinion 28/2024
(17 December 2024): a model's anonymity is assessed case by case, and legitimate interest (Art. 6(1)(f)) is not a
"default" basis ([CMS, blog](https://cms.law/en/int/legal-updates/edpb-opinion-28-2024-key-takeaways-on-processing-personal-data-in-the-context-of-ai-models)).

**Practical note:** local chat logs and the RAG index are still personal data. The product needs retention settings,
encryption and tools for exporting and deleting data per client.

### An EU region of a US provider is not sovereignty

| Offer | Who controls | What it gives | What it does not give |
|---|---|---|---|
| Microsoft EU Data Boundary (completed 26 February 2025), Azure Poland Central | Microsoft (USA) | Customer data and support data in the EU/EFTA, apart from "limited security instances" | Protection against § 2713; Anthropic models in Copilot are excluded from the EU Data Boundary |
| Microsoft Sovereign Cloud (16 June 2025): Data Guardian, keys in the customer's HSM, Azure Local, M365 Local | Microsoft (USA) | Access only for staff from Europe, disconnected versions | Changes in the parent company's jurisdiction |
| AWS European Sovereign Cloud (GA 15 January 2026, Brandenburg) | Amazon's German GmbH | Operation "exclusively by EU residents", 90+ services | The announcement does not mention the CLOUD Act |
| S3NS (Thales + Google), Bleu (FR), Delos (DE) | Companies with an EU operator | S3NS PREMI3NS has SecNumCloud 3.2, which aims at protection against "lois extraterritoriales" | It is still hyperscaler technology, price and availability for a small firm |
| OVHcloud AI Endpoints, STACKIT, IONOS AI Model Hub | EU companies | No US parent company; cheap open-model APIs | The data still leaves the office for the cloud |
| A box on the desk | The professional | No processor and no transfer for the AI part | Cloud conveniences: updates, scaling, support — you have to build them |

Sources: [Microsoft EU Data Boundary](https://blogs.microsoft.com/on-the-issues/2025/02/26/microsoft-completes-landmark-eu-data-boundary-offering-enhanced-data-residency-and-transparency/),
[Microsoft Sovereign Cloud](https://blogs.microsoft.com/blog/2025/06/16/announcing-comprehensive-sovereign-solutions-empowering-european-organizations/),
[Copilot and the EU Data Boundary](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy),
[AWS European Sovereign Cloud](https://press.aboutamazon.com/aws/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe),
[S3NS](https://www.s3ns.io/en), [ANSSI SecNumCloud](https://cyber.gouv.fr/enjeux-technologiques/cloud/),
[OVHcloud](https://www.ovhcloud.com/en/public-cloud/ai-endpoints/), [STACKIT](https://stackit.com/en/),
[IONOS](https://cloud.ionos.com/managed/ai-model-hub), [Azure regions](https://learn.microsoft.com/en-us/azure/reliability/regions-list)
— company websites, *company data*.

**The CADA says it outright.** The draft Cloud and AI Development Act (the technological sovereignty package,
3 June 2026; in October 2026 **still a draft**) defines 4 sovereignty levels for public procurement
([European Commission](https://digital-strategy.ec.europa.eu/en/policies/cloud-and-ai-development-act)):

- **L1** — data processed and stored in the EU;
- **L2** — independence from third countries and supply-chain transparency;
- **L3** — EU ownership and control, staff citizenship criteria;
- **L4** — full supply-chain control, "no interference from a third country".

An "EU region" is L1. An assistant on open weights, running on the client's hardware, can describe itself in L3/L4
terms (my assessment — check the final text of the CADA once adopted). A Polish example that the label sells:
Operator Chmury Krajowej (the National Cloud Operator) advertises a "100% Polish cloud solution" while reselling Gemini
and Azure OpenAI ([OChK](https://ochk.cloud/pl/), *company data*).

---

## 2. Professional secrecy

The common denominator: **statutory secrecy, with no time limit, often without the possibility of release, plus human
verification of the AI output.** This lets you build one product core and different "compliance packs" for the
professions.

| Profession | Basis | What it means for AI | Practical rule for the assistant |
|---|---|---|---|
| Advocate | Art. 6(1)–(4) of the Law on the Bar (Prawo o adwokaturze, Dz.U. 2024 item 1564): everything learned "in connection with providing legal aid"; no time limit; no release. Code of Ethics (Zbiór Zasad Etyki) § 23e (NRA, 12–13 June 2026) and § 19(6) | § 23e: AI only as an aid; ban on disclosing confidential information to tools without adequate protection; personal verification; naming the tools at the client's request; § 19(6): particular diligence in electronic transmission | Data local and encrypted; drafts only, nothing leaves automatically; citations to the file and the provisions; an exportable "note on the tools used" per case |
| Legal adviser (radca prawny) | Art. 3(3)–(6) of the Legal Advisers Act (Dz.U. 2024 item 499) — as for advocates. KIRP, "Recommendations on using AI" (13 May 2025), 22 points | The recommendations (co-created with Microsoft Polska and SK&S) allow the cloud with contractual safeguards; checking the place of processing, training on data, rights to outputs; informing the client in sensitive matters | Do not sell "the cloud is forbidden" — sell simplicity and certainty; attach a one-page answer to the KIRP list |
| Doctor, dentist | Art. 40 of the Medical Profession Act (Dz.U. 2026 item 37); Art. 13–14 and 24 of the Patients' Rights Act; Code of Medical Ethics (KEL) Art. 12 (from 1 January 2025) | KEL Art. 12: AI in diagnosis, treatment and prevention only when the patient is informed, has given informed consent, the algorithm is approved for medical use and certified, and the decision rests with the doctor | The scope "documentation and administration" (transcription, note, referral); no diagnosis suggestions; a clearly described intended purpose; recordings only with consent |
| Tax adviser | Art. 37 of the Tax Advisory Act (Dz.U. 2026 item 1274): no time limit, covers employees (para. 3); limited GDPR rights (paras. 5–6). Changes to KIDP's ethics rules (January 2026) | According to the KIDP president: a duty to ensure confidentiality with AI tools and to verify results before use, with disciplinary liability (paragraph numbers unverified) | Every number in an answer with a pointer to a line in the KSeF XML, JPK or the contract; anonymization unnecessary, because no third party sees the data |
| Notary | Art. 18 of the Notary Law (Prawo o notariacie, Dz.U. 2026 item 614): secrecy of the circumstances of the case, continues after dismissal; release by the Minister of Justice | No KRN guidelines on AI found (the KRN website unavailable) | Local only; treat like an advocate until the KRN speaks |
| Statutory auditor | Art. 78 of the Statutory Auditors Act (Dz.U. 2025 item 1891): all information and documents from assurance services, no time limit, also for persons with access | No PIBR guidelines on AI (PIBR website, 11 October 2026) | Audit documentation does not leave the firm; an audit trail of every query |
| All of the above | Art. 266 § 1 of the Criminal Code: disclosing or using information "contrary to the provisions of an act or to an obligation undertaken" — a fine, restriction of liberty or imprisonment of up to 2 years | Personal criminal liability of the professional, not only disciplinary | The "nothing leaves the room" argument hits the client's real risk |

Sources: [Law on the Bar](https://api.sejm.gov.pl/eli/acts/DU/2024/1564/text.pdf),
[NRA on § 23e](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/),
[Rzeczpospolita, 16 June 2026](https://www.rp.pl/zawody-prawnicze/art44636171-nra-zmienila-kodeks-etyki-adwokat-moze-korzystac-z-ai-ale-tylko-pomocniczo),
[Legal Advisers Act](https://api.sejm.gov.pl/eli/acts/DU/2024/499/text.pdf),
[KIRP recommendations](https://kirp.pl/rekomendacje-dotyczace-korzystania-z-ai/),
[prawo.pl on KIRP](https://www.prawo.pl/prawnicy-sady/rekomendacje-korzystania-z-ai-dla-radcow-prawnych,532905.html),
[Medical Profession Act](https://api.sejm.gov.pl/eli/acts/DU/2026/37/text.pdf),
[KEL (NIL PDF)](https://nil.org.pl/uploaded_images/1723037323_kel-2305.pdf),
[Tax Advisory Act](https://api.sejm.gov.pl/eli/acts/DU/2026/1274/text.pdf),
[Rzeczpospolita on KIDP, 12 January 2026](https://www.rp.pl/zawody-prawnicze/art43622191-michna-doradcy-podatkowi-beda-bardziej-widoczni-w-terenie),
[Notary Law](https://api.sejm.gov.pl/eli/acts/DU/2026/614/text.pdf),
[Statutory Auditors Act](https://api.sejm.gov.pl/eli/acts/DU/2025/1891/text.pdf),
[Criminal Code (ISAP)](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19970880553).

Three notes that are easy to miss:

- **The exceptions to secrecy are narrow and do not concern AI.** For advocates, legal advisers, tax advisers and
  notaries they are mainly the AML rules and the reporting of tax schemes (MDR). "Convenience" is not an exception.
- **KEL Art. 12 has been criticized** as impractical (patient consent added just before the vote); Ligia Kornowska
  proposes reading it only for AI that substantially affects treatment ([OSOZ blog](https://blog.osoz.pl/nowy-kodeks-etyki-lekarskiej-z-niejasnym-zapisem-o-ai)).
  The sources of 11 October 2026 show no change to the KEL and no NIL position on scribes. The safe course: stay with
  documentation.
- **The date the NRA changes take effect did not appear in the sources**, and a practitioner from the Institute of
  Accounting and Tax Advisory (Instytut Księgowości i Doradztwa Podatkowego) warns that pasting opinions and contracts
  into public AI tools may be a disclosure of secrets
  ([IKiDP, 9 August 2026](https://ikidp.pl/blog/ai-tajemnica-zawodowa-doradcy-podatkowego/)).

**Hallucinations are not theory.** Damien Charlotin's database counts **2,184 court cases with AI hallucinations**
(as of 10 October 2026), including **6 in Poland**; 864 involving lawyers ([database](https://www.damiencharlotin.com/hallucinations/)).
That is why § 23e and the KIDP rules speak of personal verification — and the product must make it easy (citation →
source in ISAP or SAOS).

---

## 3. The AI Act and the Polish act

### The AI Act calendar after the Omnibus

The AI Act is Regulation (EU) 2024/1689; the deadlines were changed by the **AI Omnibus — Regulation (EU) 2026/1744**,
published in the Official Journal of the EU on 24 July 2026, in force from 27 July 2026 ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601744),
[FPF](https://fpf.org/blog/the-ai-act-implementation-timeline-what-changes-under-the-ai-omnibus/),
[Lewis Silkin, 27 July 2026](https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo)).

| From | What applies | Does it concern an assistant for professionals |
|---|---|---|
| 2 February 2025 | Prohibited practices (Art. 5), AI competence (Art. 4) | Yes — Art. 4 softened after the Omnibus: "support the development of" competence |
| 2 August 2025 | Obligations of providers of general-purpose AI (GPAI) models (Art. 53–55), penalties | For the model's creator (e.g. SpeakLeash, Mistral), not for the integrator |
| 2 August 2026 | General application, including transparency under Art. 50 | **Yes** — Art. 50(1) in a chat for a client or patient |
| 2 December 2026 | A new prohibition (generating CSAM and intimate images without consent); Art. 50(2) for systems already on the market | Art. 50(2) only when generating synthetic content |
| 2 August 2027 | GPAI models from before 2 August 2025; a sandbox in every Member State | Indirectly |
| 2 December 2027 | High risk under **Annex III** | Only if the functions move into it |
| 2 August 2028 | High risk under **Annex I** (e.g. medical devices) | When the software is a medical device (MDR) |

Other changes in the Omnibus: a new **Art. 4a** (special categories of data only when "strictly necessary" for detecting
and correcting bias) and SME simplifications extended to "small mid-caps" (up to 750 people, up to EUR 150 million turnover).

### What actually concerns the assistant

- **Roles.** You as the creator are the **provider of an AI system** (Art. 3(3)), the law firm or clinic is the
  **deployer** (Art. 3(4)). Purely personal use is outside the regulation (Art. 2(10))
  ([AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)).
- **Art. 50.** Para. 1: a person must know they are talking to an AI (a client chat, reception). Para. 4: labelling of
  texts published on matters of public interest **does not apply** to content that has undergone human editing with
  editorial responsibility — an internal draft of a letter that a lawyer checks and signs is in practice outside
  para. 4 ([Art. 50](https://artificialintelligenceact.eu/article/50/)).
- **Annex III — high risk only if…**
  - point 8(a): AI used **by or on behalf of a judicial authority** or in ADR — courts and arbitrators, not law firms;
  - point 5: eligibility for benefits, credit scoring, pricing of health and life insurance,
    **emergency patient triage**;
  - point 4: employment and HR (CV screening)
  ([Annex III](https://artificialintelligenceact.eu/annex/3/)).
- **Art. 6(3):** an Annex III system is not high-risk when it performs a narrow procedural task, improves the result of
  a completed human activity, detects patterns without replacing human assessment or performs a preparatory task.
  **Profiling of persons is always high-risk** ([Art. 6](https://artificialintelligenceact.eu/article/6/)).
- **Medicine:** software providing information for diagnostic or therapeutic decisions is at least class IIa under the
  MDR (Annex VIII, rule 11), and therefore high-risk from 2 August 2028
  ([MDR](https://eur-lex.europa.eu/eli/reg/2017/745/oj)). A scribe without a diagnostic purpose usually is not a device —
  the declared intended purpose decides.
- **Fine-tuning a model.** An integrator becomes a GPAI provider only with "significant modifications"
  ([Commission guidelines](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers)). A light LoRA on Bielik
  or Qwen almost certainly does not exceed that (the compute threshold — unverified).

**Product rule:** no automatic triage, no "diagnosis suggestions", no client scoring, no CV-screening module. If ever —
then as a separate product with a separate intended purpose. Plus an Art. 50(1) notice in every client chat and a short
Art. 4 training pack for staff.

### The Polish Act on Artificial Intelligence Systems

**Act of 3 July 2026 on artificial intelligence systems (ustawa o systemach sztucznej inteligencji), Dz.U. 2026 item 1003**
(promulgated 27 July 2026) ([text, api.sejm.gov.pl](https://api.sejm.gov.pl/eli/acts/DU/2026/1003/text.pdf)):

| Provision | Content | Meaning for the assistant's provider |
|---|---|---|
| Art. 5 | **KRiBSI** (Komisja Rozwoju i Bezpieczeństwa Sztucznej Inteligencji, the Commission for the Development and Safety of Artificial Intelligence) — the market surveillance authority under Art. 70(1) of the AI Act and the single point of contact | This is where you ask and where someone inspects you |
| Art. 9 | An entity covered by the AI Act **or planning to become one** may apply for an opinion; a factual situation or a future event; the same entity again no earlier than after 30 days (para. 5) | You can ask before sales start |
| Art. 11 | A fee of **PLN 150**; a refund, among others, when the Commission does not issue the opinion on time | Negligible cost |
| Art. 12 | The opinion within 30 days, in particularly complex cases 60 days (para. 1); **no opinion on time = an opinion consistent with the applicant's position** (para. 3) | Tacit approval works in your favor |
| Art. 13 | The opinion binds KRiBSI and the authorities and bodies referred to in Art. 12(2) (those whose opinion the Commission sought) — for the stated factual situation (para. 1); it cannot be changed once irreversible effects have occurred (para. 2). The act says nothing about binding courts or professional chambers | A document to show the chamber and the client |
| Art. 15 | The Commission may amend or revoke an opinion, among other things after a change in law or EU guidelines | The opinion is not eternal — track changes |
| Art. 127 | Entry into force 14 days after promulgation (**11 August 2026**); Art. 8–18 and chapters 3–5, 8, 9 after 3 months (**28 October 2026**) | Individual opinions from 28 October 2026 |

The dates are also confirmed by [gdpr.pl](https://gdpr.pl/ustawa-o-systemach-sztucznej-inteligencji-weszla-w-zycie) and
[infor.pl](https://www.infor.pl/prawo/nowosci-prawne/7668177,ustawa-o-systemach-sztucznej-inteligencji-od-28-pazdziernika-2026-obowiazki-firm-i-kary-co-to-jest-kribsi.html).
The act also provides for a regulatory sandbox (Art. 91) and penalties under Chapter XII of the AI Act (Art. 104).

**A question worth asking KRiBSI after 28 October 2026** (an example, not an application template): "Is a local assistant for drafting, summarizing and transcription for law firms and practices, without triage, scoring and diagnosis suggestions, outside Annex III?" (a separate application: whether it falls under Art. 6(3) — one issue per application, Art. 9(3)(1)) For PLN 150, with tacit approval after 30–60 days, it is the cheapest
risk-reducing document you can show a cautious chamber.

### If you sell the assistant: PLD and CRA

| Act | From | What it means for the box seller |
|---|---|---|
| Directive (EU) 2024/2853 on liability for defective products (PLD) | Products placed on the market from **9 December 2026** (also the transposition deadline) | Covers "all types of software … including … AI-systems"; the manufacturer is liable for defects, also from updates and from machine-learning behavior. Check the Polish transposition; it was not checked whether the loss of professional data is damage covered by the directive |
| Regulation (EU) 2024/2847, Cyber Resilience Act (CRA) | In force since 10 December 2024; **reporting from 11 September 2026**; main obligations from **11 December 2027** | A product with digital elements: CE marking, security updates throughout the life cycle, vulnerability handling, SBOM. Already today: a process for reporting actively exploited vulnerabilities |

Sources: [Commission — PLD](https://single-market-economy.ec.europa.eu/single-market/goods/free-movement-sectors/liability-defective-products_en),
[Commission — CRA](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act).

**Conclusion:** selling a box with a model, you sell a **product**, not only a service. You need: a clear statement of
intended purpose ("help with drafting and documentation, the result is verified by the professional"), a limitation of
liability in the B2B contract, liability insurance, signed offline updates and a bill of materials (SBOM). Agent
security is described in [the course, part 16](../course_agentic_apps/16-SECURITY-OWASP-ASI.md).

### UODO: checklists and the MyDr lesson

- **On 6 August 2026 UODO published lists of "initial questions"**: "Before you deploy an AI tool, check whether it
  complies with the GDPR" — four versions: for AI developers, for SMEs using ready-made tools, for the public sector
  and an extended one (GDPR + AI Act). UODO stresses that they do not replace a risk analysis or a DPIA; consultations
  ran until 30 September 2026 ([UODO](https://uodo.gov.pl/pl/138/4533)). **Include ready answers to the SME version
  with the product** — the client saves a day of work.
- **On 13 August 2026 UODO opened an inspection of MyDr** — cloud-based medical software — after a patient data breach;
  roughly **12,000 healthcare entities** were potentially affected ([UODO](https://uodo.gov.pl/pl/138/4540)).
  The lesson: one SaaS cloud = one point of failure for thousands of practices. Data distributed across desks reduces
  the scale of a single leak — but **shifts responsibility for safeguards onto the practice and onto you**.
- UODO reminds controllers that they must "regularly measure and test the implemented security measures"
  (26 June 2026, [UODO](https://uodo.gov.pl/pl/138/4449)).

---

## 4. Competition in the EU and in Poland

### European "sovereign" and private offerings

| Product | For whom | Where the data is | Price (with date) | Lesson |
|---|---|---|---|---|
| [Noxtua](01-PROFILES.md#14-noxtua) (DE, C.H.Beck) | Lawyers, legal departments, administration in DACH and the EU; 30,000+ users (September 2026, *company data*) | Germany (Deutsche Telekom, IONOS) and Switzerland; the "Athena" tier on open models, "Minerva" on frontier models in a European setup; no desk version | Non-public subscription; Series B about EUR 81 million (April 2025), Series C EUR 100+ million (23 September 2026) | Two tiers (sovereign and frontier) to choose per case; the secrecy act on the security page; the publisher's content as a moat |
| Mistral Vibe (formerly Le Chat, renamed 28–29 May 2026) | Companies and individuals in the EU | EU by default; Enterprise self-hosted or on-prem | Pro EUR 14.99, Team EUR 24.99/user/month (min. EUR 50), excluding VAT (October 2026) | The main "EU, but cloud" competitor; its small Apache-2.0 models (Ministral 3) are candidates for the box's engine |
| Proton Lumo (since 23 July 2025; 2.0 since 1 July 2026) | Privacy-conscious consumers | Germany and Norway; a story of zero-access encryption, but the GPU server sees the prompt while answering | Lumo Plus USD 12.99/month or USD 9.99 yearly | The "privacy AI" pattern for the consumer — still trust in the operator; Qwen 3.5, GLM 5.3, Apertus 1.5 models |
| Nextcloud Assistant (Nextcloud 36) | Companies with their own Nextcloud | The client's server: llm2, stt_whisper2, Context Chat (RAG), Context Agent with MCP | Support price: not checked | The closest open equivalent; default models of 9B and smaller — room for better Polish on stronger hardware |
| Cohere North 2 + Aleph Alpha | Banks, public sector, telecoms | On-prem, air-gapped, VPC, hybrid; Cohere is to run on STACKIT | Non-public licenses; Cohere ARR USD 240 million (2025); combined valuation about USD 20 billion, USD 600 million from Schwarz Group (April 2026) | Regulated clients pay for air-gap — but in large contracts; the small-office segment stays free |
| DeepL Pro and DeepL Agent | Translation in companies; 200,000+ business customers (*company data*) | European ISO 27001 data centers, texts deleted | Individual EUR 7.49, Team EUR 24.99, Business EUR 49.99/user/month (yearly, October 2026) | Translating contracts is a common desk data leak — a local translator in the assistant closes it |
| Langdock | Companies wanting many models in one place | EU hosting (per reviews Azure Frankfurt), self-hosted option; inference at US providers | Business EUR 25/user/month (October 2026) | An "EU overlay" on US models — data in the EU, but inference not |
| Heidi Health (AU, strong in UK/EU) | Doctors, practices, NHS | EU data in the EU/EEA; "No audio recordings are ever saved" | Clinician about USD 150/user/month (USA, 2026) | Residency + no recordings is the privacy ceiling of the scribe market in 2026 |
| Nabla (FR) | Hospital systems, mainly USA | Audio processed in the browser, not stored on servers; transcripts 14 days by default | Non-public prices; USD 120 million in total (June 2025) | Data minimization in the architecture is an argument you can demonstrate |
| Microsoft 365 Copilot (US reference point) | Every company on M365; 30+ million paid seats (FY2026, *company data*) | EU Data Boundary, except Anthropic models | Business USD 18/user/month yearly (reduced from USD 21 until December 2026) | You will not win on price per seat — you win on secrecy, Polish law and offline work |

Sources: [Noxtua](https://www.noxtua.com/), [Noxtua security](https://www.noxtua.com/security),
[Noxtua Series C](https://www.noxtua.com/news/press-releases/series-c),
[TechCrunch on Noxtua](https://techcrunch.com/2025/04/22/noxtua-raises-92m-for-its-sovereign-ai-tuned-for-the-german-legal-system/),
[Mistral pricing](https://mistral.ai/fr/pricing), [heise on Vibe](https://heise.de/-11311685),
[Proton Lumo pricing](https://proton.me/lumo/pricing), [Lumo privacy](https://proton.me/support/lumo-privacy),
[Help Net Security on Lumo 2.0](https://www.helpnetsecurity.com/2026/07/01/proton-lumo-2-0-ai/),
[Nextcloud AI](https://docs.nextcloud.com/server/latest/admin_manual/ai/index.html),
[Nextcloud llm2](https://docs.nextcloud.com/server/latest/admin_manual/ai/app_llm2.html),
[Cohere North 2](https://cohere.com/blog/introducing-north-2),
[TechCrunch on Cohere](https://techcrunch.com/2026/02/13/coheres-240m-year-sets-stage-for-ipo/),
[TechCrunch on Aleph Alpha](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/),
[DeepL Pro](https://www.deepl.com/en/pro), [Langdock](https://www.langdock.com/pricing),
[Heidi safety](https://heidihealth.com/safety), [Heidi GDPR](https://www.heidihealth.com/au/compliance/gdpr),
[Heidi plans](https://support.heidihealth.com/en/articles/8885129-which-heidi-plan-is-right-for-you),
[Nabla (a competitor's review)](https://www.commure.com/blog-scribe/nabla-ai-review),
[STAT on Nabla](https://www.statnews.com/2025/06/17/nabla-raises-70-million-ambient-market-heats-up/),
[Copilot pricing](https://www.microsoft.com/en-us/microsoft-365-copilot/pricing),
[Microsoft FY26 Q4](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast).
The difference in Noxtua's Series B amount: about EUR 80.7 million (CMS) and USD 92.2 million / EUR 81.2 million (TechCrunch) — I give a rounding.

More on the US leaders: [Harvey](01-PROFILES.md#4-harvey) (post-training of an open model, Tenet) and
[Abridge](01-PROFILES.md#3-abridge) (a medical scribe).

### The Polish market

| Product | For whom | Where the data is | Price (with date) | Lesson |
|---|---|---|---|---|
| Beck-Noxtua (C.H.Beck + Noxtua) | Lawyers with Legalis | "Independent, European infrastructure" — per the Czech edition IONOS and Open Telekom Cloud, BSI C5 | **PLN 590 net/month/user**, no token limit, requires Legalis Silver+ (11 October 2026) | A price anchor for lawyers; the moat is the Legalis content, not locality |
| LEX Expert AI (Wolters Kluwer) | LEX subscribers; since 14 July 2026 also finance, taxes, HR, compliance | EU servers, SOC 2, "not for public models"; model undisclosed | Non-public (launched 19 November 2025) | Polish lawyers expect a pointer to a source fragment with every answer |
| LexisNexis Protégé (PL/CEE) | Law firms and tax advisers | "A private workspace … in line with European standards" | Demo only, no price (11 October 2026) | The third international player in the cloud |
| Gaius-Lex ("Gaius Vault") | Law firms of 20–99 lawyers (PL, CZ, AT, DE) | SaaS in the EEA, hybrid or "full on-premise deployment" | No price; seed about USD 502 thousand (August 2025, aggregator), 6 people | **The closest Polish equivalent of "data does not leave the office"** — study the positioning |
| LEX AI (LEX Secure AI, Navimor) | Consumers and small firms | Per the App Store, servers only in Poland; a "closed model" with Gdańsk University of Technology | Standard PLN 49, Premium PLN 120, PRO MAX PLN 489/month; a signed opinion about PLN 320–380 (v1.4.0, 21 September 2026) | A price ladder in zloty for the individual client |
| Noa Notes (Docplanner / ZnanyLekarz) | Private doctors; "over 13,000 specialists" (*company data*) | AWS and Microsoft Azure cloud | **PLN 199/month + VAT**, no note limit (October 2026) | The scribe's price anchor; a Chrome plugin as an integration with any EMR; dependence on US hyperscalers is a gap |
| Medidesk | Facilities: manager assistant, chatbot, voicebot | EEA, no training | Not checked | The patient-service market is going into AI too |
| Comarch ChatERP (Optima, beta) | Comarch ERP users | On PLLuM, which "can be hosted locally"; data goes to "technology subcontractors" | Not given | A Polish model in a commercial product — but the beta forbids personal data and secrets in questions |
| Comarch AI | Companies | SaaS, Comarch's data center in Kraków | Not given | "Data does not leave the infrastructure" as a slogan |
| wFirma | About 4,000 accounting offices, 130k+ companies (*company data*) | wFirma cloud | AI features at no extra charge | AI is becoming an add-on to the package — hard to sell the same thing separately |
| inFakt | Small firms | Connecting accounting data to Claude or ChatGPT (USA) | Not given | Providers send data to US models — a gap for offices bound by secrecy |
| SentiOne | Banks, debt collection (Alior Bank, Kruk) | On-prem or cloud | Not given | A Polish on-prem tradition exists in bots |

Sources: [Beck-Noxtua](https://www.beck-noxtua.pl/), [Noxtua PL](https://www.noxtua.com/news/press-releases/beck-noxtua-poland),
[Noxtua CZ](https://www.noxtua.com/news/press-releases/beck-noxtua-for-the-czech-republic),
[prawo.pl on LEX Expert AI](https://www.prawo.pl/prawnicy-sady/lex-expert-ai-nowym-narzedziem-dla-prawnikow,535918.html),
[Wolters Kluwer, 14 July 2026](https://www.wolterskluwer.com/pl-pl/news/lex-expert-ai-wspiera-specjalistow-ktorzy-nie-sa-prawnikami),
[Protégé Polska](https://www.lexisnexis.com/de-at/cee/protege-polska), [Gaius-Lex](https://gaius-lex.pl/),
[Legal Technology Hub](https://www.legaltechnologyhub.com/vendors/gaius-lex/),
[Signalbase](https://www.trysignalbase.com/news/funding/gaius-lex-secures-5),
[LEX AI in the App Store](https://apps.apple.com/pl/app/lex-ai/id6748342467?l=pl), [lexai.pl](https://lexai.pl/),
[Noa pricing](https://www.noa.ai/pl/cennik), [Noa Notes](https://noa.ai/pl/noa-notes),
[Medidesk](https://www.medidesk.com/), [Comarch ChatERP](https://www.comarch.pl/erp/asystent-ai/),
[Comarch AI](https://www.comarch.ai/), [wFirma](https://wfirma.pl/), [inFakt](https://www.infakt.pl/),
[SentiOne](https://sentione.com/) — company websites, *company data*.

**The KSeF context:** e-invoices are mandatory from 1 February 2026 (sales for 2024 above PLN 200 million) and from
1 April 2026 for the rest; until the end of 2026 invoices of up to PLN 10,000 a month may stay outside KSeF (act of
5 August 2025, Dz.U. 2025 item 1203)
([KSeF](https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/podstawy-prawne-oraz-kluczowe-terminy/)). So every company
has structured invoice XMLs — ideal material for a local model.

**The state avoids personal data too.** The mObywatel assistant on PLLuM (for everyone since 31 December 2025)
deliberately has no access to PESEL, prescriptions or fines, and users are told not to enter sensitive data
([iMagazine](https://imagazine.pl/2026/01/02/mobywatel-wchodzi-w-2026-rok-z-polskim-ai/)). That is exactly the gap
that a desk assistant fills.

**Conclusion from both tables:** on 11 October 2026 none of those listed sells a **ready box for an office of 1–10 people**.
That is the result of a negative search, not proof that no such product exists.

---

## 5. Adoption in Poland

| Indicator | Poland | EU | Source |
|---|---|---|---|
| Companies with 10+ people using AI (2025) | 8.36% (Eurostat); 8.7% (GUS, up from 5.9% in 2024) | 19.95% (up from 13.5%); Denmark 42.03% | [Eurostat](https://ec.europa.eu/eurostat/statistics-explained/index.php/Use_of_artificial_intelligence_in_enterprises), [GUS](https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultaktualnosci/5497/1/19/1/spoleczenstwo_informacyjne_w_polsce_2025.pdf) |
| Professional, scientific and technical activities (2025) | **23.2%** (up from 14.4%) | **40.43%** | ibid. |
| Companies by size (2025) | large 42.0%, medium 15.6%, small 6.1% | large 55.03%, medium 30.36%, small 17% | ibid. |
| Text generation (the most common type of AI) | 5.3% of companies (from 2.4%) | — | GUS |
| Where the AI comes from: ready-made / open-source adaptation / own | 6.4% / 2.4% / 2.3% | — | GUS |
| Barriers among companies that considered AI | — | lack of knowledge 70.89%, unclear legal consequences 52.52%, data protection 48.83% | Eurostat |
| Non-users who will not adopt AI "until they have to" | 77% (about one in five cites cost) | — | [PIE, 24 September 2025](https://pie.net.pl/wp-content/uploads/2025/09/2025-09-22_Z-AI-korzysta-mniej-niz-co-szosta-firma-w-Polsce-a-pozostale-nie-planuja-jej-wdrazac-1.pdf) |
| Lawyers using at least one AI tool daily | over 92% (a sample of 810 people from the USA, China and 9 European countries, including Poland; only 34% feel ready for regulation) | — | [Future Ready Lawyer 2026 (prawo.pl)](https://www.prawo.pl/prawnicy-sady/prawnicy-na-co-dzien-korzystaja-z-ai-a-ai-zmienia-model-ich-zawodu,1540345.html) |

**The size of the opportunity:**

- **Doctors:** the NIL register (30 June 2026) — **164,456 doctors and 42,903 dentists** practicing, **207,821** in total
  ([NIL](https://nil.org.pl/uploaded_files/1783510889_30062026-zestawienie-nr-1.pdf)). NIL runs AI training
  for doctors (29 September and 20 October 2026); no NIL survey on AI was found.
- **Lawyers and advisers:** the numbers of advocates and legal advisers were not verified in this review; no Polish
  surveys on AI in the legal, medical and tax professions were found (NRA, KRRP, NIL, KIDP, SKwP).
- **Reading the numbers:** Polish professional firms are about two years behind the EU, but in one year they gained
  8.8 percentage points. Two of the three main barriers in the EU (legal consequences, data protection) are exactly
  what a desk assistant solves. The third (lack of knowledge) says: **sell deployment and training, not just
  software.**
- **"Shadow AI":** PIE notes that employees use free tools on their own, so real use is higher than reported. For a law
  firm this is a secrecy risk — an approved local assistant replaces it.

---

## 6. Polish and open models for local work

### Bielik v3 — Polish under the Apache-2.0 license

| Model | Size | License | What sets it apart |
|---|---|---|---|
| Bielik-11B-v3.0-Instruct (30 December 2025) | 11.2 bn, 50 layers (from Mistral-7B-v0.2 by layer stacking) | Apache-2.0 | 32 languages with an emphasis on Polish; context 32,768 tokens, 131,072 with YaRN |
| Bielik-Minitron-7B-v3.0 (March 2026) | 7.35 bn (−33.4% through pruning and distillation) | Apache-2.0 | About 90% of the 11B's quality, up to about 50% faster; official GGUF and FP8 |
| Bielik-PL-11B-v3.0 and PL-Minitron-7B (April 2026) | 11B / 7B | Apache-2.0 | The **APT4** tokenizer for Polish: fewer tokens per word, more text in the context |
| Bielik DFlash (24 June 2026) | about 1 bn | Apache-2.0 | Small draft models for speculative decoding in vLLM and SGLang |
| Bielik-Guard "Sójka" v1.1 | 0.5 bn | Apache-2.0 | A Polish safety classifier, 5 harm categories, precision 75.28% at 0.73% false alarms |

Sources: [Bielik-11B-v3.0](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct),
[arXiv 2601.11579](https://arxiv.org/abs/2601.11579),
[Minitron-7B](https://huggingface.co/speakleash/Bielik-Minitron-7B-v3.0-Instruct),
[Bielik-PL-11B](https://huggingface.co/speakleash/Bielik-PL-11B-v3.0-Instruct), [arXiv 2604.10799](https://arxiv.org/abs/2604.10799),
[DFlash](https://huggingface.co/speakleash/Bielik-11B-v3.0-DFlash), [Bielik-Guard](https://huggingface.co/speakleash/Bielik-Guard-0.5B-v1.1).
Bielik v3.1 (50 languages) was announced for June 2026 — on 11 October 2026 only v3.0 models are on Hugging Face.
Bielik claims 4.7 million+ downloads (*project data*), and on Ollama the 11B version has 13.5 thousand downloads (11 October 2026)
([bielik.ai](https://bielik.ai/), [Ollama](https://ollama.com/SpeakLeash)). **No support contract and no SLA** — you
have to provide the support yourself.

### PLLuM — watch the licenses

- **1st generation (2412):** 12B on Mistral-Nemo and 8x7B on Mixtral — Apache-2.0; the "-nc" variants — CC-BY-NC-4.0
  (non-commercial); Llama-PLLuM 8B and 70B — the Llama 3.1 license.
- **HIVE AI, July 2025:** PLLuM-12B-nc-250715 under its own pllum-1.x licenses — **non-commercial**.
- **2nd generation (2512):** PLLuM-4B (on Gemma-3-4B) and PLLuM-12B — Apache-2.0 per the cards; but the 4B inherits
  Gemma's terms.
- **The paradox:** the commercial PLLuM-12B-chat-2512 has a PLCC of 41.17, and the non-commercial 250715 — 69.67. The best
  PLLuM Polish is under a license you cannot use in a paid product.

Sources: [PLLuM-12B-chat](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-chat),
[pllum-12b-nc-chat-250715](https://huggingface.co/CYFRAGOVPL/pllum-12b-nc-chat-250715),
[PLLuM-12B-instruct-2512](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512),
[PLLuM-4B-instruct-2512](https://huggingface.co/CYFRAGOVPL/PLLuM-4B-instruct-2512).

### Who wins in Polish (benchmarks with dates)

| Model | CPTUB (1–5; understanding of complex text; data of 11 August 2026) | PLCC (culture and language; data of 8 October 2026) | License |
|---|---|---|---|
| Qwen3.6-27B (reasoning) | 4.41 | — | unverified |
| Qwen3.5-122B-A10B | 4.36 | 68.33 | unverified |
| Qwen3.5-27B (thinking) | 4.34 | 54.33 | Apache-2.0, 262k context |
| Gemma-4-31B | 4.32 | 69.33 with reasoning / 59.17 without | Apache-2.0, 256k context |
| DeepSeek-V3.2 | 4.14 | — | — |
| gpt-oss-120b | 3.82 | 54.33 | — |
| Bielik-11B-v3 | 3.73 | **70.67** | Apache-2.0 |
| PLLuM-12B-nc-250715 | 3.67 | 69.67 | non-commercial |
| Bielik-Minitron-7B | — | 53.00 | Apache-2.0 |
| gpt-oss-20b | — | 32.33 | Apache-2.0 |

Sources: [CPTUB](https://huggingface.co/spaces/speakleash/cptu_bench), [PLCC](https://huggingface.co/spaces/sdadas/plcc),
[Qwen3.5-27B](https://huggingface.co/Qwen/Qwen3.5-27B), [Gemma 4 31B](https://huggingface.co/google/gemma-4-31B-it),
[gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b). The best open model on PLCC is DeepSeek-V4-Pro-0813
(1.7 trillion parameters) with 89.83 — closed models score 92–97.

**Professional tasks in Polish — the quality ceiling:**

- retrieval of provisions on questions from the entrance exams for the advocate and legal-adviser traineeships: **72.3%
  top-1 hits** versus 61.7% for BM25 (31 August 2026, [arXiv 2608.30929](https://arxiv.org/abs/2608.30929));
- the KIO qualification exam (the National Appeals Chamber, public procurement): **no model passed the practical part** (6 November 2025, [arXiv 2511.04205](https://arxiv.org/abs/2511.04205));
- Polish medical exams: the best of 21 models is the open Qwen3.5-122B, but under stricter grading the results
  dropped by 31 percentage points (10 June 2026, [arXiv 2606.12250](https://arxiv.org/abs/2606.12250));
- Polish Medical Leaderboard: Bielik-11B-v3 50.21%, the leader Llama-3.1-405B 69.2% (19 September 2026,
  [HF](https://huggingface.co/spaces/speakleash/polish_medical_leaderboard)).

**Conclusion:** in law, the quality of retrieval over Polish provisions matters more than the raw strength of the model.

### Quantization: 2 bits break agents

- Bielik-11B-v2.3 in 2-bit QuIP# (3.26 GB) holds 71.92% against 72.07% on 22 Polish tests
  ([arXiv 2603.04162](https://arxiv.org/abs/2603.04162)) — but these are multiple-choice tests.
- **PolAgentBench (25 September 2026)**, 67 Polish agentic tasks with tools: Bielik-11B-v3, Bielik-Minitron-7B
  and Llama-PLLuM-8B **"fall off a cliff" between 3 and 2 GGUF bits** ([arXiv 2609.32042](https://arxiv.org/abs/2609.32042)).
- **Rule:** Q4–Q8 for chat and tools; never Q2 for an agent.

### Which model for what (recommendation)

| Task | I recommend | Why |
|---|---|---|
| Reasoning, case-file analysis, letters (a 32–64 GB box) | Qwen3.5-27B or Gemma-4-31B (Q4–Q8); Qwen3.6-27B after checking the license | Top of CPTUB, Apache-2.0, long context |
| The same on a 128 GB box | Qwen3.5-122B-A10B or gpt-oss-120b | MoE — fast decoding with large memory; Qwen3.5-122B is the best open model on medical exams |
| Polish style, drafting letters to a client, text "in a human voice" | Bielik-11B-v3 or Bielik-PL-11B (APT4); on small hardware Minitron-7B | PLCC leader in its size class, Apache-2.0 |
| Input and output safety filter | Bielik-Guard 0.5B | Polish, small, Apache-2.0 |
| Contract translation | EuroLLM-22B-Instruct (Apache-2.0, 35 languages) | The authors claim the level of Gemma-3-27B and Qwen-3-32B in translation ([HF](https://huggingface.co/utter-project/EuroLLM-22B-Instruct-2512)) |
| Speech to text (a visit, dictation) | Whisper large-v3-turbo (whisper.cpp) | 30 s of audio in about 618 ms on an M1 Ultra ([whisper.cpp](https://github.com/ggml-org/whisper.cpp/issues/89)); Polish medical vocabulary not verified — a pilot with recordings made with consent |
| What to avoid in a paid product | PLLuM "-nc" and pllum-1.x; Q2 for agents | License and quality |

**My setup (4× R9700, DeepSeek-V4-Flash, 4 slots of 131k, about 13.6 tok/s per agent, text only):**
DeepSeek-V4-Flash does not appear in the PLCC or CPTUB data I cite here — the tables have only V4-Pro (PLCC 89.83)
and V3.2 (CPTUB 4.14). That is why I treat this machine as a **laboratory**: I run PLCC, CPTUB and my own legal and
medical sets on it for every candidate before it goes into a client's box. The V4-Flash license was not
verified in this review — check it before commercial use. The model is text-only, so speech is handled by a
separate Whisper. A hybrid with [Claude](01-PROFILES.md#2-claude) as the planner makes sense only for matters the client
marks as non-confidential — see [the course, hybrid local + Claude](../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md)
and [03-TECHNICAL-PATTERNS.md](03-TECHNICAL-PATTERNS.md). Evaluation is described in [the course, part 14](../course_agentic_apps/14-EVALUATION.md).

---

## 7. Desktop hardware

Prices from apple.com/pl and ceneo.pl, **checked on 11 October 2026**; speeds from community benchmarks (llama.cpp, LMSYS)
and blogs — not from my own measurement. Prices of high-memory hardware are rising: DGX Spark +17.5% (from USD 3,999 to
USD 4,699, February 2026), RTX PRO 6000 about +87% since launch — **give the client quotes with an expiry date**
([NVIDIA forum](https://forums.developer.nvidia.com/t/2-23-2026-price-change-announcement/361713),
[tech-insider](https://tech-insider.org/nvidia-rtx-pro-6000-blackwell-price-2026/)).

| Device | Memory / bandwidth | Price in Poland (11 October 2026) | Which models | Decoding speed (examples) | Power draw / noise | For whom |
|---|---|---|---|---|---|---|
| Mac mini M5 Pro | 24–64 GB / 307 GB/s | from **PLN 8,499** (24 GB); 18/20 cores from PLN 9,499; the 64 GB price not captured | 8–14B dense, 30B-A3B MoE (the 35B-A3B MoE needs over 32 GB) | 7B Q4 about 67 tok/s; Qwen3.5-35B-A3B 112 tok/s on the M5 family (MLX) | no data / very quiet (unmeasured) | A solo advocate or doctor |
| Mac Studio M5 Max | 36–128 GB / up to 614 GB/s | from **PLN 12,499** (36 GB); 40-core GPU from PLN 15,499 | up to gpt-oss-120b (128 GB); 70B Q4 from 64 GB | 7B Q4 about 120 tok/s; 120B about 40–60 (a blog's estimate) | 7 W idle / 200 W max; quiet | A solo practitioner with a large model, a small clinic |
| Mac Studio M5 Ultra | 96–256 GB (512 GB from the end of October) / 1.2 TB/s | from **PLN 27,999** (96 GB); 80-core GPU from PLN 34,499 | 235B-A22B MoE, 70B Q8 | 7B Q4 about 179 tok/s; 235B about 25–35 (estimate) | 9 W / 385 W; quiet | A law firm on Macs, 1–5 people |
| ASUS Ascent GX10 (GB10, like the DGX Spark) | 128 GB / 273 GB/s | from **PLN 24,499** (1 TB); Dell about PLN 27,992; NVIDIA FE about PLN 30,506 | gpt-oss-120b, 30B-A3B; 70B too slow | 120B about 35–56 tok/s; prefill about 1.8–2 thousand tok/s; 70B FP8 2.7 tok/s | up to 240 W; quiet, the fan audible under load | A law firm of 1–5 people, RAG over long case files; OEM business warranty |
| Strix Halo (Ryzen AI Max+ 395) 128 GB | 128 GB / 256 GB/s | **PLN 13,490** (Minisforum MS-S1 Max) – PLN 16,999 (GMKtec EVO-X2); Framework PLN 16,529 (out of stock) | The same class as the GB10 | 120B about 31–47 tok/s; 30B MoE 70–100 tok/s | about 100–120 W; 29–43 dBA | A solo user on Windows or Linux — the cheapest 128 GB; weaker prefill |
| Tower + RTX PRO 6000 Blackwell | 96 GB / 1,792 GB/s | the card alone: Max-Q from **PLN 65,999**, Workstation PLN 84,630–97,156 | 120B, 70B Q8, many users at once | 120B about 196 tok/s; prefill about 5.5 thousand tok/s | card 600 W; a loud tower | An office of 5–10 people, a server cabinet |
| Tower + 1–2× Radeon AI PRO R9700 | 32 GB per card / 640 GB/s | about **PLN 8,900** – 10,321 per card | 14–32B, 30B-A3B | 7B Q4 about 146 tok/s (Vulkan) | 300 W per card; blower, loud | A budget option for a few people; ROCm and Vulkan maturity lower than CUDA |

Sources: [Mac mini](https://www.apple.com/pl/shop/buy-mac/mac-mini), [Mac Studio](https://www.apple.com/pl/shop/buy-mac/mac-studio),
[Apple newsroom](https://www.apple.com/newsroom/2026/08/apple-introduces-new-mac-studio-with-m5-max-and-m5-ultra/),
[Apple power consumption](https://support.apple.com/en-us/102027), [llama.cpp Apple](https://github.com/ggml-org/llama.cpp/discussions/4167),
[Ollama MLX](https://ollama.com/blog/mlx), [bestllmfor (estimates)](https://bestllmfor.com/ai-hardware/mac-studio-m5/),
[ceneo GX10](https://www.ceneo.pl/;szukaj-ascent+gx10), [ceneo DGX Spark](https://www.ceneo.pl/;szukaj-dgx+spark),
[LMSYS DGX Spark](https://www.lmsys.org/blog/2025-10-13-nvidia-dgx-spark), [llama.cpp gpt-oss-120b](https://github.com/ggml-org/llama.cpp/discussions/16578),
[Framework forum](https://community.frame.work/t/dgx-spark-vs-strix-halo-initial-impressions/77055),
[ceneo Strix Halo](https://www.ceneo.pl/;szukaj-ryzen+ai+max%2B+395+128gb), [runaihome (blog)](https://runaihome.com/blog/framework-desktop-vs-gmktec-evo-x2-local-ai-2026/),
[ceneo RTX PRO 6000](https://www.ceneo.pl/;szukaj-rtx+pro+6000+blackwell), [llama.cpp RTX PRO 6000](https://github.com/ggml-org/llama.cpp/discussions/15396),
[ceneo R9700](https://www.ceneo.pl/;szukaj-radeon+ai+pro+r9700), [llama.cpp Vulkan](https://github.com/ggml-org/llama.cpp/discussions/10879).

**How to choose:**

- **A solo professional** (one person, letters and questions about their own files): a Mac mini M5 Pro 48–64 GB or a
  Mac Studio M5 Max 128 GB for gpt-oss-120b-class quality. Idle draw below 10 W and silence suit a room with a client.
  On Windows: Strix Halo 128 GB.
- **A firm of 1–5 people, RAG over case files:** prefill and concurrency matter → GB10 (ASUS GX10, about PLN 24.5 thousand):
  CUDA, vLLM, OEM warranty. An office on Macs → M5 Ultra. More than 5 people at once → a tower with an RTX PRO 6000 (in total
  about PLN 90–120 thousand at ceneo.pl prices).
- **A medical practice** (Whisper + a note, usually one doctor at a time): a Mac mini M5 Pro 48–64 GB or a Mac Studio M5 Max;
  with several practices — one GB10 as a server.
- **Energy (approximate, without the electricity price):** Strix Halo under load about 110 W × 8 h × 21 days ≈ 18.5 kWh
  a month; the RTX PRO 6000 Workstation card alone draws up to 600 W, and the Mac Studio M5 Max at idle 7 W.

**My setup for comparison:** 4× R9700 is 128 GB of VRAM for about PLN 35.6 thousand (the cards alone, 4 × about PLN 8,900, ceneo
11 October 2026), up to 1,200 W TBP on the cards. Great for tests and many agents at once, **but it is not a product for a
client's desk**: loud, hot and demanding ROCm care. Details of the layout: [harnesses — costs](../agent-harnesses/03-ARCHITECTURE.md#5-costs-is-local-cheaper).

---

## 8. Product opportunities, risks and market entry

### Opportunities by profession

| Profession | What the assistant does locally | What sets it apart | Price anchor |
|---|---|---|---|
| Advocate, legal adviser (1–10 people) | Case-file analysis, case chronology, drafts of letters, comparing versions of contracts, contract translation, answers with a citation to the file and ISAP/SAOS | Meets § 23e "by construction": local data, drafts only, verifiable citations, a note on tools for the client | Beck-Noxtua PLN 590 net/month/user + Legalis; LEX AI PLN 49–489 |
| Tax adviser, accounting office | Reading KSeF XML and JPK, classification, answers about a specific invoice with a pointer to the line, monitoring KIS interpretations | Incumbents send data to US models (inFakt) or forbid personal data (Comarch beta) | wFirma — AI in the package; M365 Copilot USD 18/user/month |
| Doctor, clinic | Visit transcription (Whisper) and a note, referrals, letters; integration through a browser plugin as in Noa | Audio and data do not leave the practice; no diagnoses (KEL Art. 12, MDR) | Noa Notes PLN 199/month + VAT per doctor |
| Notary | Drafts and comparisons of documents, searching the office archive | Secrecy under Art. 18; no KRN guidelines — an opportunity and an uncertainty at once | No data |
| Statutory auditor | Review of audit documentation, searching working papers, an audit trail | Art. 78 with no time limit | No data |

**Seven promises that can be proven** (based on the sources in this review):

1. **"Nothing leaves the room"** — no processor (Art. 28) and no transfer (Art. 44–49) for the AI part, no CLOUD Act,
   no dependence on the DPF.
2. **Working on what others forbid** — full case files, non-anonymized medical documentation, clients' books.
3. **Built-in compliance** — a citation with every answer, a note on tools per case, a medical scope without diagnoses.
4. **Polish** — Bielik for style, a 27–35B model for reasoning.
5. **An offline mode** — works during a connection outage; consistent with the offline principle of
   [the course, part 07](../course_local_models/07-SANDBOX-SECURITY-MONITORING.md).
6. **Documents for the cautious** — a DPIA template, answers to the UODO list, a KRiBSI opinion.
7. **A cost calculation** — below.

### The calculation: local or cloud (2 years, list prices net, no discounts)

| Scenario | Cloud for 24 months | Local hardware (one-off) | Conclusion |
|---|---|---|---|
| 1 advocate, Beck-Noxtua | 590 × 24 = **PLN 14,160** + Legalis | Mac mini M5 Pro from PLN 8,499 or Strix Halo PLN 13,490 | The hardware is cheaper, but Beck-Noxtua provides Legalis content that the box lacks — sell it as a complement |
| 3 lawyers, Beck-Noxtua | 590 × 3 × 24 = **PLN 42,480** + Legalis | ASUS GX10 **PLN 24,499** + a support subscription | A margin for support, deployment and updates |
| 1 doctor, Noa Notes | 199 × 24 = **PLN 4,776** | Mac mini M5 Pro from PLN 8,499 | **Price loses** — only privacy sells here |
| A clinic, 5 doctors, Noa Notes | 199 × 5 × 24 = **PLN 23,880** | Mac Studio M5 Max (40-core GPU) from PLN 15,499 or a GX10 PLN 24,499 as a shared server | A shared box adds up |
| An office of 10 people, M365 Copilot Business | USD 18 × 10 × 24 = **USD 4,320** | GX10 PLN 24,499 | You will not beat Copilot on price per seat — you win on secrecy |

Add to the local cost: a support and updates subscription, deployment, electricity, VAT and the risk of a hardware price change.
For comparison, the cost of an EU cloud outside the USA: IONOS charges USD 0.11/0.17 per million input/output tokens for Qwen3.5-9B
([IONOS](https://cloud.ionos.com/managed/ai-model-hub), *company data*) — **the cloud is cheap; the box has to win on
secrecy and control, not on the token price.** The pricing model that follows from the table: hardware once + an annual subscription
(model updates, patches, hardware replacement), priced against 2–3 years of per-seat cloud fees.

### Market entry: channels

- **The order of beachheads (a hypothesis to test):** (1) small advocate and legal-adviser firms — the sharpest
  secrecy, a clear anchor of PLN 590, competition only in the cloud; (2) tax and accounting offices — KSeF XML
  and the duty of verification; (3) clinics with 3+ doctors — a shared box instead of PLN 199 per doctor.
- **Through the professional bodies:** training on Art. 4 of the AI Act and on § 23e for the bar associations, OIRP (the regional chambers of legal advisers), KIDP; NIL already runs
  AI training (29 September and 20 October 2026). **Do not claim that the NRA or KIRP recommends the product** — say
  "designed for § 23e".
- **Through software vendors:** law-firm management systems, EMRs in practices (a browser plugin like
  Noa), the ERP ecosystem. Publishers (LEX, Legalis) have the content — **complement them**, working on the client's own files.
- **Through IT integrators and hardware makers:** Dell is a Bielik partner ([bielik.ai](https://bielik.ai/)),
  and OEM versions of the GB10 (ASUS, Dell, HP) have a business warranty and on-site service — important for a client who has
  no IT person.
- **Fine-tuning away from the desk:** legal and medical adapters can be trained on public data in the EuroHPC AI
  factories (PIAST in Poznań, Gaia) or on Beyond.pl GPUs, while inference at the client stays local
  ([EuroHPC](https://www.eurohpc-ju.europa.eu/ai-factories_en), [Beyond.pl](https://beyond.pl/en/)).
- **Learn from Noxtua:** two tiers (local and an optional frontier under an EU contract) chosen per case, and the secrecy
  act in the foreground of the security page ([profile](01-PROFILES.md#14-noxtua)).

### Risks and how to limit them

| Risk | Source | Mitigation |
|---|---|---|
| Product liability | The PLD from 9 December 2026 covers AI and updates; the professional is personally liable (§ 23e, KIRP, KIDP) and will pass this on to the provider in negotiations | A statement of intended purpose, a limitation of liability in the B2B contract, the provider's liability insurance, tracking the Polish PLD transposition |
| Hallucinations before a court | 2,184 cases in Charlotin's database, 6 in Poland (10 October 2026); 72.3% top-1 in provision retrieval; the KIO exam failed | A citation with every answer, an allowed "I don't know", Polish acceptance tests before every model change |
| Support and updates | Bielik without an SLA; top models changed several times in 2026 (Qwen 3.5 → 3.6 → 3.8, Gemma 4) | A subscription with updates, a license register, pinned versions, signed offline packages |
| CRA | Reporting from 11 September 2026, full obligations from 11 December 2027 | SBOM, a vulnerability-handling process, updates throughout the life cycle |
| Local security | MyDr shows that UODO inspects; theft of a box without encryption = a breach (Art. 33–34 GDPR) | FileVault or LUKS, per-user accounts and logs, encrypted backups, a security cable lock, no remote access by default, telemetry off — cf. [the course, part 16](../course_agentic_apps/16-SECURITY-OWASP-ASI.md) |
| Entering high risk | Triage, scoring, HR, diagnosis suggestions (Annex III from 2 December 2027, MDR and Annex I from 2 August 2028) | Hard limits on functions; a KRiBSI opinion |
| Model licenses | PLLuM "-nc", pllum-1.x, Gemma in PLLuM-4B, Llama in Llama-PLLuM | Only Apache-2.0 or commercially cleaned weights; a license list for the client |
| Hardware | Memory prices +17–87% in 2026; Framework unavailable in Poland; the 512 GB Mac Studio not yet on sale | Quotes with an expiry date, two hardware variants in the offer |
| Demand | 77% of non-users will not adopt AI "until they have to" (PIE) | Sell the solution to a risk (secrecy, shadow AI), not "AI" |

---

## Sources for this part

All sources with links are given next to the tables and paragraphs above and in the collected [SOURCES.md](SOURCES.md).
The most important legal texts: [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj),
[AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj), [AI Omnibus 2026/1744](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601744),
[Act on AI systems, Dz.U. 2026 item 1003](https://api.sejm.gov.pl/eli/acts/DU/2026/1003/text.pdf),
[18 U.S.C. § 2713](https://www.law.cornell.edu/uscode/text/18/2713). Information marked as unverified
(Microsoft's intervention in C-703/25 P, the expiry of FISA 702, the paragraph numbers of the KIDP rules, the Qwen3.6 and DeepSeek-V4-Flash license,
the number of advocates and legal advisers) must be checked before use in sales materials.
