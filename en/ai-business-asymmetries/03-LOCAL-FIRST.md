# Local-first: when open models on your own hardware win

This chapter answers one question for every opportunity in [02-OPPORTUNITIES.md](02-OPPORTUNITIES.md): should the
agent run on open models at the customer site, in a private cloud in Poland or the EU, or can it just call a paid API?
The short version, checked on 14 Oct 2026: **local rarely wins on token cost, and often wins on the sale.** Buyers
under professional secrecy, public-sector rules or an IT department that has banned sending data to US and Chinese
clouds will pay for a box they can point at. Your margin comes from setup, updates and support, not from cheaper tokens.

All prices and versions below were checked on 14 Oct 2026 unless another date is given. Where a figure could not be
checked in this pass, the text says "not found".

## 1. Why buyers want local

### GDPR: the processor chain and transfers

- An AI vendor that processes client documents is a **processor** under GDPR art. 28: the buyer needs a data
  processing agreement and a list of sub-processors. Every extra cloud (the LLM API, its hosting provider) adds a link
  the buyer's data protection officer must review. A box on site removes most of them.
  ([GDPR, EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj))
- **Art. 9 special categories** (health, biometrics, union membership, beliefs) need an explicit legal basis. Medical,
  HR and insurance documents are full of them. "It never leaves the clinic" is the easiest answer to a DPO.
- **Transfers outside the EEA** (Chapter V) need an adequacy decision or standard contractual clauses plus a transfer
  impact assessment. The EU-US Data Privacy Framework (adopted 10 Jul 2023) is still the basis for US transfers, but it
  is under pressure: the Data Protection Review Court lost its Democratic members in Jan 2025, and after the US Supreme
  Court decision *Trump v. Slaughter* (Jun 2026) removed protections for FTC commissioners, noyb asked the Commission
  to repeal the framework and announced litigation ([Wikipedia summary, read 14 Oct 2026](https://en.wikipedia.org/wiki/EU%E2%80%93US_Data_Privacy_Framework)).
  For a buyer this means: "your data goes to a US API" now carries a real risk that the legal basis disappears
  mid-contract, as it did twice before (Safe Harbor 2015, Privacy Shield 2020).
- **China** has no adequacy decision. Calling the DeepSeek API from Poland with personal data is a Chapter V transfer
  with no easy basis. Running the same open weights locally is not a transfer at all. That is the core of the
  local-first pitch.

### Polish professional secrecy

Each of these duties is personal and criminally or disciplinarily enforced, which makes the buyer far more cautious than
GDPR alone would. Links go to the consolidated act in ISAP.

| Profession | Secrecy rule | What it means for an AI vendor |
| --- | --- | --- |
| Advocate (adwokat) | tajemnica adwokacka, [Prawo o adwokaturze art. 6](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19820160124) | Every external processor must be justified; on-prem removes the question |
| Legal adviser (radca prawny) | tajemnica radcowska, [ustawa o radcach prawnych art. 3](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19820190145) | Same logic as advocates; firms ask where the model runs |
| Physician | tajemnica lekarska, [ustawa o zawodach lekarza art. 40](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19970280152) | Patient data is also art. 9 GDPR; clinics prefer no cloud at all |
| Tax adviser | tajemnica doradcy podatkowego, [ustawa o doradztwie podatkowym art. 37](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19961020475) | Client books and correspondence stay in the office |
| Tax administration | tajemnica skarbowa, [Ordynacja podatkowa art. 293](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19971370926) | Tax-office data cannot go to commercial clouds without a legal basis |

The law does not forbid cloud AI for these professions. It makes the professional personally answerable for any leak,
so the cheapest way to close a deal is to remove the cloud from the conversation.

### Public sector

Polish public bodies buy through public procurement and must pass security and data-location reviews. The state funded
its own Polish model family (PLLuM, see below) explicitly "for Polish public sector applications" with about 18.5 M PLN
([PLLuM model card](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512)). A vendor that deploys a state-funded
open model on the office's own server is aligned with that policy, not fighting it.

### EU AI Act timeline (as of Oct 2026)

From the AI Act implementation timeline, page updated 31 Aug 2026
([artificialintelligenceact.eu](https://artificialintelligenceact.eu/implementation-timeline/)):

| Date | What applies |
| --- | --- |
| 2 Feb 2025 | Prohibited practices, AI literacy duty |
| 2 Aug 2025 | General-purpose AI model rules, governance, penalties |
| 2 Dec 2026 | New prohibitions on non-consensual intimate imagery and CSAM generation |
| 2 Dec 2027 | High-risk rules (Chapter III) for Annex III systems |
| 2 Aug 2028 | High-risk rules for Annex I (product-safety) systems |
| 2 Aug 2030 | Public-authority high-risk systems must comply |

The Annex III date of 2 Dec 2027 is later than the original 2 Aug 2026. That shift is the Digital Omnibus
postponement; the page lists the new dates but I did not find the final adoption text in this pass. Practical
meaning: most agentic back-office tools (document drafting, extraction, triage) are not high-risk, but anything that
scores people for credit, hiring or access to public benefits is Annex III. You have until Dec 2027, not forever.

### Data sovereignty demand

I did not find a dated, sourced survey on Polish or EU buyer demand for sovereign or local AI in this pass, so this
chapter makes no claim about its size. Treat it as a hypothesis to test in discovery calls: ask every prospect
"would you accept a cloud API if the contract is right?" and log the answer. The adoption numbers live in
[01-ADOPTION-GAPS.md](01-ADOPTION-GAPS.md).

## 2. Open models that are good enough today

### Polish-first models

| Model | Latest version found | Size | Licence | Note |
| --- | --- | --- | --- | --- |
| Bielik (SpeakLeash) | Bielik-11B-v3.0-Instruct, Bielik-Minitron-7B-v3.0-Instruct (updated Jul 2026) | 11B, 7B | Apache 2.0 | "32 European languages, optimized for Polish"; tech report Dec 2025 |
| PLLuM (state consortium) | 2512 family (Dec 2025): PLLuM-4B, Llama-PLLuM-8B, PLLuM-12B (Mistral-Nemo base), Llama-PLLuM-70B | 4B to 70B | Apache 2.0 for PLLuM-12B; the Llama-based ones inherit Llama terms (check each card) | Tuned for public-administration tasks |

Sources: [SpeakLeash on Hugging Face](https://huggingface.co/speakleash),
[Bielik-11B-v3.0-Instruct card](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct),
[CYFRAGOVPL on Hugging Face](https://huggingface.co/CYFRAGOVPL),
[PLLuM-12B-instruct-2512 card](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512), all read 14 Oct 2026.

Benchmarks: the [Open PL LLM Leaderboard](https://huggingface.co/spaces/speakleash/open_pl_llm_leaderboard) is the
reference, but its table did not load in my fetch on 14 Oct 2026, so I quote no scores. Before you promise Polish
quality to a customer, run your own 50-document test set from their domain against Bielik, PLLuM and one large
multilingual model. Small Polish models (7-12B) are strong at Polish style and short extraction, weaker at long
multi-step reasoning; the usual pattern is a large multilingual model for reasoning and a Polish model for final text.

### Multilingual open models

| Family | What to know | Licence trap |
| --- | --- | --- |
| gpt-oss-120b (OpenAI, Aug 2025) | 117B total, 5.1B active, fits one 80 GB GPU in MXFP4 ([card](https://huggingface.co/openai/gpt-oss-120b)) | Apache 2.0, none found |
| DeepSeek V4 family | The reader already runs DeepSeek-V4-Flash locally; API exists too ([pricing](https://api-docs.deepseek.com/quick_start/pricing)) | Check the licence on the exact weights you ship |
| Qwen, Mistral | Strong multilingual, many Apache 2.0 sizes | Some sizes use custom licences: check each card |
| Gemma (Google) | Good small multilingual and vision models | Custom terms (last modified 1 Apr 2026): use restrictions must be passed through to your customers, and Google may "restrict (remotely or otherwise)" use ([terms](https://ai.google.dev/gemma/terms)) |
| Llama 4 (Meta) | Popular base for fine-tunes | Multimodal Llama 4 rights "are not being granted to you if you are an individual domiciled in, or a company with a principal place of business in, the European Union" ([use policy](https://dev.meta.ai/llama/llama4/use-policy/)); end users of a product are exempt, but you as a Polish builder are not |

The Llama clause matters for this reader directly: a Polish sole trader cannot build on multimodal Llama 4. Prefer
Apache 2.0 or MIT weights for anything you install at a customer.

### Speech, vision, embeddings

- **Speech to text:** Whisper large-v3-turbo, MIT licence, 809M parameters, 99 languages including Polish, mean WER
  7.83 on the card's English-centred benchmarks; the card warns accuracy is uneven across languages
  ([card](https://huggingface.co/openai/whisper-large-v3-turbo)). No Polish-specific WER found in this pass: measure on
  the customer's own call recordings.
- **Vision and OCR:** Polish scanned documents (invoices, court letters, archives) need a vision-language model or a
  classic OCR step before the LLM. I did not benchmark candidates in this pass; Gemma and Qwen vision variants are the
  usual open options, with the licence notes above.
- **Embeddings:** for retrieval over Polish documents use a multilingual embedding model with an open licence and test
  recall on the customer's own queries. No Polish embedding benchmark checked in this pass.

## 3. Hardware tiers for a customer site

Token generation on a single box is mostly limited by memory bandwidth. A rough upper bound is
`tokens/s ≈ bandwidth ÷ bytes read per token`, where bytes per token ≈ active parameters × bytes per weight. A
mixture-of-experts model with about 5B active parameters at 4-bit (about 3 GB per token) is therefore far faster than a
dense 70B model (about 40 GB per token). The throughput column is this estimate, not a measurement.

| Tier | Example (price checked 14 Oct 2026) | Memory | Bandwidth | What it runs (estimate) |
| --- | --- | --- | --- | --- |
| Mini PC | Framework Desktop, Ryzen AI Max+ 395, 128 GB: zł 16,529 ([Framework](https://frame.work/products/desktop-diy-amd-aimax300)) | 128 GB unified | 256 GB/s (spec) | gpt-oss-120b class MoE at tens of tokens/s for 1-2 users; dense 70B is slow |
| Compact NVIDIA | DGX Spark, GB10: price not found on the vendor page ([NVIDIA](https://www.nvidia.com/en-us/products/workstations/dgx-spark/)) | 128 GB unified | 273 GB/s | Vendor: up to 200B parameters for inference *(vendor claim)*; speed similar to the mini PC; CUDA stack is the plus |
| Mac Studio | M5 Max up to 128 GB, M5 Ultra up to 512 GB; PLN prices not shown in my fetch ([Apple PL](https://www.apple.com/pl/mac-studio/)) | up to 512 GB | 614 GB/s (Max), 1.2 TB/s (Ultra) | Ultra holds the largest open MoE models; good single-user speed, weak at many parallel users |
| Multi-GPU workstation | The reader's rig: 4x Radeon AI PRO R9700, 128 GB VRAM; current price not found in this pass | 128 GB VRAM | per-card GDDR6 | DeepSeek-V4-Flash with 4 parallel slots today; best for an office of 10-30 users |
| EU rented GPU | Hetzner GEX131, RTX PRO 6000 Blackwell 96 GB, in Germany or Finland; monthly price not shown in my fetch ([Hetzner](https://www.hetzner.com/dedicated-rootserver/gex131/)) | 96 GB VRAM | n/a | Private-cloud tier: dedicated server, EU data centre, your contract with the buyer |

Polish data-centre GPU options (to keep data in Poland, not just in the EU) were not priced in this pass; ask
Polish hosting providers for a dedicated GPU quote before you sell a "data stays in Poland" promise.

Rules of thumb for picking a tier:
1. One professional or a small office, batch work overnight: mini PC or DGX Spark class (128 GB).
2. 10-30 concurrent users, chat plus document pipelines: a multi-GPU workstation like the reader's.
3. Customer has no server room or wants no hardware: dedicated GPU server in the EU, under your DPA.

## 4. Cost: local vs API

Assumptions (state them to the customer too):
- Workload: 50 M tokens per month, 3 input tokens per output token.
- API: DeepSeek-Flash list price on 14 Oct 2026, input cache miss $0.15 off-peak / $0.30 peak, output $0.60 / $1.20
  per 1 M tokens ([DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)).
- Local: Framework Desktop 128 GB at zł 16,529, amortised over 36 months (about zł 460 per month), plus about
  110 kWh per month of power (150 W average, 24/7) at an assumed zł 1.0 per kWh, so about zł 570 per month before your
  time.

| Line | Monthly cost |
| --- | --- |
| API, off-peak blended (about $0.26 per 1 M tokens) | about $13 |
| API, peak blended (about $0.53 per 1 M tokens) | about $26 |
| Local mini PC (hardware + power, no labour) | about zł 570 |

Honest result: **against cheap API models, local hardware does not break even on tokens at small-office volumes.**
At an assumed 3.8 PLN per USD, zł 570 is about $150, so one box matches the API only at roughly 300-600 M tokens a
month (peak vs off-peak prices). That is 115-230 tokens per second around the clock, more than a 128 GB mini PC
sustains and far more than a small office produces. Local wins only when:
- the cheap API is legally unusable (personal data to a Chinese or US API, professional secrecy), so the real
  comparison is local vs not doing it at all, or vs a premium EU-hosted API;
- the comparison is against expensive frontier-model pricing, not against DeepSeek-Flash;
- the site is offline or has unreliable internet (factories, archives, some clinics).

So price the box as compliance and control, not as a saving. The reader's own trade-off between local and paid models
is covered in [../cheap-free-models/README.md](../cheap-free-models/README.md).

## 5. Deployment patterns

1. **On-prem appliance.** A preconfigured box (mini PC or workstation) with the model server, the agent, a web UI and
   local document storage. Sold as setup fee plus monthly licence and support. Best for law firms, tax advisers,
   clinics.
2. **Private cloud in PL or EU.** A dedicated GPU server rented by you or by the customer, single-tenant, in an EU data
   centre, under your DPA. Best for customers without a server room or with several sites.
3. **Hybrid with local redaction.** A local model finds and replaces names, PESEL and NIP numbers, addresses and case
   numbers with placeholders, then the hard reasoning goes to a paid API, and the answer is re-identified locally.
   Pseudonymised data is still personal data under GDPR, so this lowers risk but does not remove the transfer question;
   tell the customer that. Pattern details: [../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md](../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md)
   and [../course_agentic_apps/17-HYBRID-AND-ROUTER.md](../course_agentic_apps/17-HYBRID-AND-ROUTER.md).
4. **Routing rules.** Write them down in the contract annex:
   - documents under professional secrecy or art. 9 data: local only;
   - redacted text, public law, templates: may go to the paid API;
   - anything with legal or money effect: a human approves before it leaves the system.

**The real recurring revenue** is not the hardware margin. It is:
- model updates (new Bielik or PLLuM versions, re-running the customer's test set before each switch);
- monitoring (disk, GPU health, queue length, failed jobs) with an alert to you, not to the customer;
- backups, security patches and a support line;
- extending the agent to the next workflow in the same office.

Security hardening for agents that read untrusted documents is in
[../course_agentic_apps/16-SECURITY-OWASP-ASI.md](../course_agentic_apps/16-SECURITY-OWASP-ASI.md); harness choices are
in [../agent-harnesses/README.md](../agent-harnesses/README.md).

## 6. Which opportunities are local-first

| Category | Default | Why | Polish open model good enough? |
| --- | --- | --- | --- |
| Legal (advocates, legal advisers) | Local-first | Professional secrecy, client trust is the sale | Drafting and extraction yes after testing; complex legal reasoning needs a large model, keep it local or redact |
| Medical (clinics, practices) | Local-first | Art. 9 data plus medical secrecy | Notes and summaries yes; anything clinical needs a doctor's sign-off |
| Tax and accounting | Local-first or hybrid | Tax-adviser secrecy; public rules and rates can go to an API | Yes for documents; numbers must be checked by code, not by the model |
| Public sector | Local-first | Procurement, data location, state-funded PLLuM | PLLuM tuned for this; verify on real cases |
| Manufacturing IP | Local-first | Trade secrets, sometimes offline sites | Language matters less; multilingual models fine |
| Archives and digitisation | Local-first | Volume plus personal data in old records | Depends on OCR quality on old scans: test first |
| SME voice (calls, reception) | Hybrid | Low latency needs; recordings are personal data | Whisper-class STT for Polish must be measured on real calls |
| E-commerce | API-fine | Product data is public; volume favours cheap APIs | Not the selling point here |

## 7. Risks

- **Polish quality gaps.** Small Polish models write good Polish but can miss multi-step reasoning; large multilingual
  models reason better but write stiffer Polish. Without a customer test set you are guessing. No current leaderboard
  scores were captured in this pass.
- **Hallucination liability.** A wrong citation in a legal brief or a wrong tax rate is the professional's liability
  first and yours second through the contract. Cap your liability, keep a human approval gate, and log every source
  the agent used.
- **Hardware support burden.** A box at a customer means driver updates, failed disks and "it stopped working" calls.
  With 1-3 people, cap the number of appliances per engineer and charge for support from day one. AMD ROCm stacks need
  more care than CUDA; the reader knows this from the R9700 rig.
- **Licence traps.** Llama 4 multimodal excludes EU-based companies; Gemma terms require pass-through restrictions and
  allow remote restriction; Llama-based PLLuM variants inherit Llama terms. Keep a licence register per deployment and
  prefer Apache 2.0 or MIT weights.
- **Regulatory drift.** The DPF may fall, the AI Act high-risk dates have already moved once. Build so the customer can
  switch API providers or go fully local without a rewrite.
- **Cost illusion.** Do not sell local as cheaper per token; on the numbers above it is not. Sell it as the reason the
  project is allowed to happen at all.
