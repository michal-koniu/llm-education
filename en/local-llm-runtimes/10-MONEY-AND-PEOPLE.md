# 10 · Money and people: who is behind it and how it sustains itself

**Why this chapter.** This is the only chapter of the course that does not teach how an engine works, but **who maintains it, with what money, and why**. The reference stack — llama.cpp, llama-swap, GGUF quants from Unsloth, a DeepSeek model, and on a Mac LM Studio or MLX — is built from code backed by specific companies and specific people, and their interests change faster than the code does. After reading it you will be able to: (1) recognize **how a given project makes money** (or why it does not); (2) read from public sources **who pays its programmers**; (3) assess **what will happen to an installation like this** when a project is acquired, relicensed or abandoned; (4) draw lessons for your own plans (a local assistant in Polish) — solely from the cases described here.

> ⚠️ **A note on the nature of this chapter.** I did not run or test anything here. This is **desk research**: company pages and their blogs, project pages, the GitHub API (commit counts, profile fields, dates), `LICENSE` files in repository clones, and a few secondary sources (Wikipedia, TechCrunch). As of **19 October 2026**. **Funding amounts and valuations are the weakest facts in the whole survey** — most come from the companies themselves or from the press, not from registry documents. Every number has a provenance tag and a date in the text. The "employer" rows come from the **`company` field in the GitHub profile (self-declaration)** or from the e-mail domain in commits; that is not an HR extract and may be out of date. This chapter talks about **the motivations of organizations**, not the motives of individual people — about individuals I give only public professional facts (role, project, track record).

**Provenance tags used throughout the chapter:**

| Notation in the text | Meaning |
|---|---|
| (no tag) | checked in a primary source: the GitHub API, a file in the repository, a project/company page stating the fact as fact |
| *(project's own claim)* / *(company's own claim)* | a claim by the company or project itself (blog, site, README); no independent confirmation |
| *(press report)* / *(third-party source)* | a press report or Wikipedia; I did not find a statement from the company |
| *(GitHub profile)* | a self-declaration in the user's profile, may be out of date |
| *(unverified)* / *(my calculation)* | my own inference or arithmetic on API data |

**Table of contents**

1. [Five ways open-source AI infrastructure makes money (and two in which it does not)](#1-five-ways-open-source-ai-infrastructure-makes-money-and-two-in-which-it-does-not)
2. [Who pays the programmers — project by project](#2-who-pays-the-programmers--project-by-project)
3. [The 2026 consolidation: who is buying the maintainers of local AI](#3-the-2026-consolidation-who-is-buying-the-maintainers-of-local-ai)
4. [Hosted inference on top (briefly)](#4-hosted-inference-on-top-briefly)
5. [Who is who — a directory of people](#5-who-is-who--a-directory-of-people)
6. [Licenses: a table and gotchas](#6-licenses-a-table-and-gotchas)
7. [Dependency risk: what will happen to the reference stack](#7-dependency-risk-what-will-happen-to-the-reference-stack)
8. [What you can learn for your own plans](#8-what-you-can-learn-for-your-own-plans)

Technical chapters I refer to for the "how": the engine and its code — `04-LLAMA-CPP-AND-THE-GGML-FAMILY.md`; Ollama, LM Studio, Jan, llmman and company — `05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md`; vLLM, SGLang, TensorRT-LLM — `06-SERVING-ENGINES-VLLM-SGLANG.md`; MLX, oMLX, ds4 — `07-APPLE-MLX-OMLX-AND-DS4.md`; KTransformers, mistral.rs, Unsloth — `08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS.md`; formats and quants — `03-QUANTIZATION-AND-FORMATS.md`.

---

## 1. Five ways open-source AI infrastructure makes money (and two in which it does not)

The inference engine is usually **free and openly licensed**. The money appears next to it. Among the projects I reviewed, five recurring mechanisms can be singled out, plus two cases in which there is no money at all. You will find the full table of ten patterns with consequences for you in section 7; here is the "where the salaries come from" version.

### 1.1 Hardware pulls software

The software is free because it sells silicon. The manufacturer pays engineers so that every new model runs first on its cards.

- **NVIDIA:** TensorRT-LLM (Apache-2.0, repository fully open since March 2025 — an inference about the year from the order of entries in the README), Dynamo, NIM microservices. Software comes only second: **NVIDIA AI Enterprise** costs, per the company's price list, 4,500 USD per GPU per year (annual subscription), 22,500 USD per GPU as a perpetual license with 5 years of support, and 1 USD per GPU-hour in the cloud; a 75% discount for education and startups *(company's own claim: docs.nvidia.com, price list)*. This is the pattern "free engine, paid container with support". NVIDIA's revenue for the whole of fiscal 2026: 215.9 billion USD *(third-party source: Wikipedia)* — the assessment in the notes is that hardware comes first and software subscriptions second *(inference from the notes, unverified)*.
- **AMD:** Lemonade (Apache-2.0; README: "optimizations by AMD engineers" for Ryzen AI, Radeon, Strix Halo), and an AMD engineer is among the most active vLLM committers (AndreasKaratzas, 428 commits *(GitHub profile)*).
- **Apple:** MLX (MIT, "Copyright © 2023 Apple Inc.", README: "brought to you by Apple machine learning research"). **Why Apple funds this — I did not find any Apple statement; this is an inference *(unverified)*:** the framework makes Apple Silicon with unified memory a good laptop for open models.
- **Qualcomm:** bought Modular (Mojo, MAX) — announced 2026-06-24, closed 2026-07-29, price undisclosed. The company narrative: "silicon-agnostic compute layer" *(company's own claim)*.

### 1.2 The platform buys the maintainers (platform complement)

A platform that earns money some other way (a model hub, a container system, enterprise subscriptions) employs people who maintain a project that increases the platform's value.

- **Hugging Face:** ggml.ai (llama.cpp) 2026-02-20; the author of oMLX 2026-09-22; the author of mistral.rs has `@huggingface` in their profile *(GitHub profile; I did not find an announcement)*. Details in section 3.
- **Red Hat:** Neural Magic (a major contributor to vLLM) — announced 2024-11-12, closed 2025-01-13, terms undisclosed; Red Hat sells **Red Hat AI Inference** ("based on vLLM and llm-d") as a subscription **priced per accelerator**.
- **Docker:** Docker Model Runner (Apache-2.0, beta announced 2025-04-09 in Docker Desktop 4.40, models as OCI artifacts on Docker Hub). There is no separate revenue model; it is a feature that keeps developers in Docker Desktop/Hub *(unverified — my interpretation; Docker did not give such a rationale in the sources I saw)*.

### 1.3 A free local client, a paid cloud

The local application is a "funnel". The revenue is hosted usage.

- **Ollama Inc.:** free locally; cloud according to the ollama.com price list of 2026-10-19: Free 0 USD; **Pro 20 USD/month** (200 USD/year) with a 60 USD credit and 3 concurrent requests; **Max 100 USD/month** with a 300 USD credit and 10 requests; **Team 500 USD/month** (early access) with a 1,000 USD pool; Enterprise by quote; billing per token, 50% cheaper off-peak *(company's own claim)*. The notes record that billing changed from GPU time to tokens (blog of 2026-08-31) — pricing changes in months, not years.
- **LM Studio (Element Labs, Inc.):** a closed application; since 2025-07-08 "free for use at work" (blog post); revenue is supposed to come from **LM Studio Bionic** (hosted open models, cloud deployment with zero retention / on private infrastructure / on edge devices) and from **Teams and Enterprise plans** *(company's own claim)*. The acquisition of **Locally AI** (the team behind an iOS/iPadOS app) — *(company's own claim; Wikipedia)*, April 2026.
- **AnythingLLM (Mintplex Labs):** MIT; a free desktop application, a **paid hosted product** for teams and an enterprise version *(company's own claim)*; it declares Y Combinator backing.

### 1.4 Free engine → startup → hosting and support

The most "classic" scenario for server engines: an academic lab creates an engine, hands it to a neutral foundation, and the founders (with the largest block of committers) start a company that sells hosting and support.

- **vLLM → Inferact:** Berkeley Sky Computing Lab (repo since 2023-02-09, PagedAttention paper at SOSP 2023); since 2025-05-06 the project has been hosted by the **PyTorch Foundation**; the company **Inferact** — *(company's own claim)* a 150 million USD "seed" at an 800 million USD valuation, January 2026, led by a16z and Lightspeed. The 150 million figure is also confirmed by the press (Wikipedia citing TechCrunch); I found the valuation and the list of investors only in the company's materials.
- **SGLang → RadixArk:** SGLang is hosted by LMSYS (a 501(c)(3) non-profit organization, registered in September 2024); the company RadixArk — *(press report: TechCrunch 2026-01-21)* valuation about 400 million USD, round led by Accel, **round size unconfirmed**.
- Both companies sell things *next to* the engine: a managed cloud, a platform on your GPUs, certification of model providers, an RL stack (Miles at RadixArk). See `06-SERVING-ENGINES-VLLM-SGLANG.md`.

### 1.5 Open-core and licenses with a catch

The core is free, while the strategic element (brand, interface, binaries) is subject to a restriction.

- **Open WebUI:** since version 0.6.6 (2025-04-19) the "Open WebUI License": rights as in BSD-3 plus a clause forbidding removal/replacement of the "Open WebUI" branding, unless you have ≤ 50 end users within 30 days, written permission, or an enterprise license.
- **Unsloth:** core Apache-2.0, but the **Unsloth Studio** interface under AGPL-3.0 (`studio/LICENSE.AGPL-3.0`) — the README says that such a structure "supports further development".
- **Modular:** a repository under Apache-2.0 with LLVM exceptions, but **MAX** under the "Modular Community License".
- **LiteLLM:** MIT except for the `enterprise/` directory, which requires a BerriAI subscription in production.

### 1.6 (No profit) One person, a day job elsewhere

Numeric details are in the tables of section 2; here only the mechanism. **ds4 (antirez):** MIT, no company; the author returned to Redis in November 2024 as a part-time developer evangelist; GitHub Sponsors 10–12 people (1/5/25 USD a month), and the sponsorship revenue, as they write, they pass on to other OSS projects — nobody pays directly for the time spent on ds4. **LocalAI:** sponsors "cover CI costs" (among them Spectro Cloud), 14 sponsors, no company. **llama-swap:** a sponsors list exists, with 0 sponsors. **KoboldCpp, text-generation-webui:** one maintainer; for the latter the README mentions a "generous grant" from a16z in August 2023 *(project's own claim)*.

### 1.7 (No profit) Pivot or zombie

- **GPT4All (Nomic):** last push **2025-05-27**; the company moved to AI agents for architecture, engineering and construction *(company's own claim: nomic.ai/about)*. The application was a marketing funnel; when the company changed markets, the application froze.
- **Jan (Menlo Research):** the company now presents itself as a maker of humanoid robots (Asimov 1, 499 USD deposit) *(company's own claim: menlo.ai)*. I **did not find** Menlo's funding — I give no amount.
- **TGI (Hugging Face):** repository archived, last commit 2026-03-21, README: "maintenance mode"; HF *itself abandoned its own server engine* and recommends vLLM, SGLang and llama.cpp.

> **Check it yourself — is the project alive (zombie check).** Before you build anything important on a project, check the dates:
> ```bash
> gh api repos/huggingface/text-generation-inference --jq '{archived, pushed_at, license: .license.spdx_id}'
> gh api repos/ggml-org/llama.cpp --jq '{pushed_at, stargazers_count, forks_count}'
> ```
> (not run by me, these exact calls with `--jq`; the fields `archived`, `pushed_at`, `stargazers_count` are the ones the notes used). For the TGI repository, expect `archived: true`.

---

## 2. Who pays the programmers — project by project

**How to read the tables.** "Who pays" is an assessment based on GitHub profiles and e-mail domains in commits (self-declarations, which may diverge from reality). Commit shares are **my arithmetic** on API data from 2026-10-19 (the total number of commits in the repository's history, excluding bots where noted) — the number of commits measures activity, not the value of a contribution. The "sponsor's motivation" column is an inference about the organization, not about individuals, and where the sponsor gave no rationale, it is marked as unverified.

### 2.1 The ggml family and local tools

| Project (stars 2026-10-19) | Who pays the creators | Revenue model | Funding | Governance | Concentration |
|---|---|---|---|---|---|
| **llama.cpp / ggml** (131.7k; MIT) | since 2026-02-20 **Hugging Face** (the ggml.ai team); earlier ggml.ai on a pre-seed; plus contributions from NVIDIA engineers (Vulkan), academia (KIT), independents | none of its own; HF gains the ecosystem (GGUF on the Hub, llama.cpp in HF Inference Endpoints *(company's own claim)*) | pre-seed from Nat Friedman and Daniel Gross, 2023, **amount undisclosed** *(company's own claim: ggml.ai)*; acquisition price by HF **undisclosed** | `ggml-org` on GitHub; CODEOWNERS per area; no foundation | 7 of the 12 most active committers declare HF = 3,878 of 5,284 commits (73%); Gerganov alone 2,035 (about 39% of that twelve, about 17% of all ~11.7k) *(my calculation)* |
| **ik_llama.cpp** (3.3k; MIT) | nobody (a personal project + community) | none | I did not find any | one maintainer (Kawrakow, in the profile "Gentleman at large") | high |
| **llama-swap** (6.0k; MIT) | the maintainer works elsewhere (*(GitHub profile)*: "Tailscale and Elethink") | none | GitHub Sponsors list: 0 sponsors | one maintainer | 536 of about 653 commits = 82% |
| **llamafile** (26.4k; Apache-2.0) | **Mozilla.ai** (the project started in Mozilla Builders) | none (a funnel to Mozilla.ai offerings *(unverified)*) | *(company's own claim)* Mozilla announced on 2023-03-22 an "initial commitment" of 30 million USD to Mozilla.ai | Mozilla.ai; a small number of active maintainers | the original author (jart, 600 commits) is no longer a visible committer in 2026 |
| **KoboldCpp** (AGPL-3.0) | nobody | none | no sponsors list, no FUNDING.yml | one maintainer (4,374 own commits) | about 1 |
| **text-generation-webui** | a16z grant from 2023 *(project's own claim)* | none | a sponsors list exists | one maintainer | 82% of commits |
| **Ollama** (183.9k; MIT) | **Ollama Inc.** (VC) | cloud: subscriptions + per-token fees | 88 million USD *(company's own claim, blog 2026-07-09)* vs 65 million USD *(press report, Wikipedia citing TechCrunch)* — **not reconciled**, see below | a company, no foundation | the four most active = about 3.6k of about 5.9k commits (probably employees) |
| **LM Studio** (closed application; CLI `lms` MIT) | **Element Labs, Inc.** | Bionic, Teams, Enterprise | **I did not find any** (the site and blog are silent) | a closed company | a small team (4–6 visible committers) |
| **Jan** (45.0k; Apache-2.0 with a request for attribution) | **Menlo Research** | none visible for Jan; the company sells robots | **I did not find any** | a company | most active: urmauur 1,464, qnixsynapse 868 commits |
| **LocalAI** (49.7k; MIT) | CI sponsors + the author's own contribution | none | no company and no rounds | BDFL | mudler 3,507 commits, then bots |
| **Open WebUI** (156.2k; "Open WebUI License") | **Open WebUI Inc.** | enterprise edition, no branding, SSO/SCIM | **I did not find any** | a company, CLA for contributors | tjbck 13,450 commits |
| **AnythingLLM** (67.3k; MIT) | **Mintplex Labs** | hosted team product | YC *(company's own claim)*; no amounts | a company | timothycarambat 1,518 commits |
| **GPT4All** (77.4k; MIT) | **Nomic** (pivot) | AEC agents | Series A 17 million USD, Coatue, 2023 *(company's own claim)* | **froze 2025-05-27** | — |
| **Lemonade** (5.9k; Apache-2.0) | **AMD** | none (hardware) | — | AMD engineers + community | jeremyfowers (AMD) 569 commits |
| **llmman** (563; Apache-2.0) | the author is a Docker engineer (an `@docker.com` address in commits from October 2026) — **no statement about sponsorship** | none | none | a personal GitHub organization; the site names no company | Curtin 402 of about 550–570 commits (about 70%) |
| **RamaLama** (3.1k; MIT) | Red Hat employees (profiles, e-mail) | indirect (OpenShift, RHEL AI *(unverified)*) | — | the `containers` organization | rhatdan 1,462, ericcurtin 971 |
| **Docker Model Runner** (658; Apache-2.0) | Docker, Inc. | a product feature | — | a company | doringeman 696, ilopezluna 387 |

**An unresolved discrepancy in the notes: Ollama 88 vs 65 million USD.** The Ollama blog of 2026-07-09 says the company "raised 88 million USD" from Benchmark (Peter Fenton), Theory Ventures (Tomasz Tunguz), 8VC (Alex Kolicich), Y Combinator and angels (among them Solomon Hykes, Aaron Katz, Spencer Kimball, Quinn Slack) and that it serves "8.9 million developers" *(company's own claim)*. Wikipedia citing TechCrunch writes of "65 million dollars in July 2026" *(press report)*. It may be a round (65) versus a total (88), but **I cannot reconcile it** and I settle nothing here. The company did not disclose a valuation; I found no earlier rounds. The blog sentence about "85% of Fortune 500 companies" is also a company claim.

### 2.2 Server engines

| Project | Who pays | Revenue model | Funding | Governance | Concentration |
|---|---|---|---|---|---|
| **vLLM** (94.2k; Apache-2.0) | **Inferact** (the founders and the biggest committers), Red Hat/Neural Magic, AMD, Hugging Face, Mistral AI, Meta; compute sponsors on vllm.ai: Alibaba Cloud, AMD, Anyscale, AWS, Crusoe, Google Cloud, IBM, Intel, Lambda, Nebius, Novita AI, NVIDIA, Red Hat, Roblox, RunPod, UC Berkeley | Inferact Platform and Inferact Cloud *(company's own claim)*; Red Hat AI Inference (a per-accelerator subscription) | Inferact: 150 million USD at 800 million USD, January 2026 *(company's own claim; the amount also in the press)* | **PyTorch Foundation** since 2025-05-06; governance document: "nobody buys a seat in governance; committer status belongs to people, not to companies" | 8 committers linked to Inferact = 3,373 of the top-15's 6,945 commits = 49%; Red Hat (mgoin) 9% *(my calculation)* |
| **SGLang** (37.4k; Apache-2.0) | **RadixArk**, Meta, independents; LMSYS funded by NVIDIA, Google Cloud, a16z, AMD, Hugging Face, Together *(company's own claim: lmsys.org)* | hosting, Miles (RL) | RadixArk: about 400 million USD valuation, Accel, round size unknown *(press report, 2026-01-21)* | LMSYS (501(c)(3)) + the PyTorch ecosystem | 5 RadixArk committers = 3,193 of 7,978 (top-12) = 40% *(my calculation)* |
| **TensorRT-LLM** (14.9k; Apache-2.0 + notices) | NVIDIA employees | hardware + AI Enterprise / NIM | a public company | NVIDIA itself | not applicable |
| **Dynamo** (8.3k; Apache-2.0) | NVIDIA | as above | — | NVIDIA | — |
| **TGI** (10.9k; Apache-2.0) | Hugging Face | no separate one | — | **archived** | — |
| **KTransformers** (19.6k; Apache-2.0) | Tsinghua MADSys + Approaching.AI | publications + Approaching.AI services *(unverified)* | Approaching.AI: **I did not find any** (site unavailable) | a laboratory | 11 people in the maintainers list (6 Tsinghua + 5 Approaching.AI) |
| **LMDeploy** | a laboratory (Shanghai AI Laboratory *(unverified)*) | none | I did not find any | a laboratory | — |
| **Modular (MAX/Mojo)** | since 2026-07-29 **Qualcomm** | within Qualcomm | 250 million USD, 2025-09-24, valuation 1.6 billion USD, 380 million USD in total *(company's own claim)* | Qualcomm; Mojo, MAX and Modular Cloud "will remain separate products" *(company's own claim)* | — |

### 2.3 Mac and others

| Project | Who pays | Revenue model | Funding | Governance | Concentration |
|---|---|---|---|---|---|
| **MLX** (28.8k; MIT) | **Apple** (zcbenz, angeloskath, jagrit06 — *(GitHub profile)*: "Apple") | none; hardware *(unverified)* | — | Apple, no foundation | co-creator Awni Hannun (718 commits, #1) has in the profile "Research at Anthropic. Prev: co-created MLX at Apple"; I saw their last commit to MLX from an Apple address on 2026-02-24 |
| **mlx-lm** (7.4k; MIT) | Apple + community | none | — | as above | awni 291, angeloskath 63, then the community |
| **oMLX** (22.9k; Apache-2.0) | since 2026-09-22 **Hugging Face** employs the author; HF blog: the project "keeps the Apache 2.0 license and remains independent", becomes "fully maintained and funded" | none | — | the author | 2,110 of about 2,280 commits in the top-5 |
| **ds4 / DwarfStar** (24.0k; MIT) | nobody (the author's hobby) | none | none | BDFL | 523 commits by the author; the next 33 |
| **mistral.rs** (7.8k; MIT) | the author has `@huggingface` in their profile; I did not find an announcement; **no connection to the company Mistral AI** (the README denies affiliation) | none | none | one maintainer | 3,073 vs the next 125 |
| **exo** (48.0k; Apache-2.0) | exo labs | open source + deployments for teams *(company's own claim)* | **I did not find any** | a company | Alex Cheema 1,424 commits |
| **Unsloth** (78.3k; Apache-2.0 + AGPL Studio) | **Unsloth AI Inc.** (YC summer 2024, a team of 12 per the YC page — entry date unknown) | open-core; prices and plans **not found** | **I did not find any** (the `about` and `pricing` pages returned 403) | a company | Daniel Han 6,391 of about 11.4k commits (about 56%) |

> **Check it yourself — who really writes the code (commit arithmetic).** Repeat the calculations from this section for any repository:
> ```bash
> gh api 'repos/ggml-org/llama.cpp/contributors?per_page=15' --jq '.[] | [.login, .contributions] | @tsv'
> gh api users/ggerganov --jq '{login, name, company, location}'
> ```
> For each login on the list, run the second command and read the `company` field. Sum the commits of the people with the same employer and divide by the sum for the whole list. Remember: `company` is a self-declaration; the `contributors` list includes bots, and for forks that keep the history (like ik_llama.cpp), the author of the *upstream* is at the top. (I wrote the `--jq` syntax from memory and did not run it; the endpoints `contributors?per_page=15` and `users/LOGIN` are the ones used in the survey.)

---

## 3. The 2026 consolidation: who is buying the maintainers of local AI

In 2023, local AI looked like a collection of hobby projects and small startups. In 2026 we see the opposite: **the maintainers of the most important projects are moving into jobs at a few large companies**. Below is the story in chronological order, starting with the one closest to the reference stack.

### 3.1 Hugging Face and llama.cpp (2026-02-20)

**Facts.** Hugging Face published the post "GGML and llama.cpp join Hugging Face" (2026-02-20; authors: Georgi Gerganov, Xuan-Son Nguyen, Aleksander Grygier, Lysandre, Victor Mustar, Julien Chaumond) and a parallel discussion in the llama.cpp repository (no. 19759, a thread started by `ggerganov`). The ggml.ai site says: "the company was acquired by Hugging Face in 2026". **The terms (price, shares) were not disclosed** — the HF post gives no amount. HF's promises: the team "devotes 100% of its time" to maintaining llama.cpp and has "full autonomy" over technical directions; the project remains "100% open-source and community-driven"; HF provides "long-term, sustainable resources"; the goal is "seamless" integration of `transformers` with llama.cpp and better packaging for ordinary users.

**What follows for the maintenance structure.** Of the 12 most active llama.cpp committers, 7 declare HF as their employer, which gives 73% of that twelve's commits *(my calculation based on the API and profiles)*. That carries two meanings at once: **the risk of abandonment has fallen** (people have salaries), and **concentration in a single employer has risen**. In the discussion under the announcement, according to the notes, remarks appeared about "ownership of the code under corporate governance" and that "there was no prior public discussion" *(third-party source: a summary of discussion #19759, I did not read the thread in full)*.

**The organization's motivation (not individuals').** HF wants local models to live on its Hub, and wants "one click" from a model in `transformers` to llama.cpp *(HF blog)*. This speeds up coverage of new architectures and improves UX for casual users — and does not promise priority for AMD multi-GPU until an HF customer asks for it *(unverified — an inference, not a statement)*.

A new brand layer around llama.cpp: the site **llama.app**, the repositories `Llama-macOS`, `Llama-Windows`, `llama-install.sh`, `llama.brand` (with a NOASSERTION license, i.e. brand control, not MIT). Whether llama.app will be monetized: **I could not establish**. Technical details of the repository: `04-LLAMA-CPP-AND-THE-GGML-FAMILY.md`.

### 3.2 NVIDIA and Hugging Face (reports from August–September 2026)

> ⚠️ **The least well-documented fact of this chapter.** *According to press reports* NVIDIA is to buy Hugging Face for **12.93 billion USD**. The first reports are dated **2026-08-26**, and the TechCrunch article "Nvidia confirms it will buy Hugging Face for $12.9 billion" **2026-09-03**; the closing of the transaction would take place in the **first half of 2027**. The basis is **Wikipedia** (the entries "Hugging Face" and "Nvidia") and **this one TechCrunch article** *(press report)*. **I did not find a press release from either party** — neither on nvidianews.nvidia.com (the snapshot I got showed only entries from October 2026), nor on huggingface.co/blog. The TechCrunch summary quotes Jensen Huang: "Nvidia's compute will not be required to build on or deploy from Hugging Face" *(press report)*. **Verify this at the source before you quote the amount in any document.**

What this would mean for the ownership chain, *if the reports are confirmed*: the llama.cpp maintainers would be employees of a subsidiary of the dominant GPU supplier. The MIT license does not change (see section 7); what would change is **the direction of steering**: roadmap priorities, priority for CUDA. For the reference stack, though, this is less dramatic than it sounds, because the HIP backend in llama.cpp is compiled **from the same `.cu` sources as CUDA** (through the layer `ggml/src/ggml-cuda/vendors/hip.h`; there is no separate ROCm tree) — so priority for CUDA largely concerns your path too, as long as someone still maintains the RDNA4-specific branches (`gfx1201`). See `04-LLAMA-CPP-AND-THE-GGML-FAMILY.md`, the section on HIP.

### 3.3 HF is collecting maintainers, not only llama.cpp

| What | When | Fact | Source / tag |
|---|---|---|---|
| llama.cpp / ggml | 2026-02-20 | the ggml.ai team joins HF, terms undisclosed | HF blog, ggml.ai |
| **TGI** (HF's own server engine) | last commit 2026-03-21 | **archive**, "maintenance mode"; the README recommends vLLM, SGLang and local engines such as llama.cpp | repository |
| vLLM | currently | Harry Mellor (`hmellor`, HF) 601 commits — among the most active | API, profile |
| oMLX | 2026-09-22 | the author (Jun Kim) hired by HF; "remains Apache-2.0", "fully maintained and funded" | HF blog `/blog/omlx` |
| mistral.rs | no date | the author (Eric Buehler) has `@huggingface` in their profile; I did not find an announcement | GitHub profile |
| Candle (a Rust ML library) | — | maintained by HF; the original author in their profile: "Co-founder Kyutai & Gradium" | API, profile |

HF **abandoned its own server engine** (TGI) and instead funds open ones: people in vLLM, in llama.cpp, in MLX (through oMLX), in Rust (mistral.rs). The strategy it declares: `transformers` as the "source of truth for model definitions", and around it hosting and an enterprise offering. HF's public price list *(company's own claim, huggingface.co/pricing)*: PRO 9 USD/month; Team 20 USD/user/month; Enterprise Hub 50 USD/user/month; storage 12–18 USD/TB/month; GPUs in Spaces 0.40–23.50 USD/h; **Inference Endpoints** from 0.033 USD/h (CPU) to 4.50 USD/h (H100). The previous round: Series D 235 million USD, August 2023, valuation 4.5 billion USD *(press report, Wikipedia)*.

### 3.4 Other buyers

- **Qualcomm buys Modular** (Mojo, MAX): announced 2026-06-24, closed 2026-07-29, price undisclosed. Chris Lattner is now, according to the Modular site, "EVP, Advanced AI Software and Platforms" at Qualcomm, Tim Davis "SVP & GM of Modular, Qualcomm". The company writes that Mojo, MAX and Modular Cloud "will continue as separate products and brands" *(company's own claim)*. In the Qualcomm statement I read, **there is no commitment** that MAX/Mojo will remain open or that support for NVIDIA/AMD will be neutral — that is an absence of a provision, not an announcement of change. Treat MAX as **a product owned by a hardware vendor**.
- **Red Hat buys Neural Magic** (an earlier precedent): announced 2024-11-12, closed 2025-01-13, terms undisclosed; Neural Magic (an MIT spin-out, 2018) is described as a "leading contributor to vLLM".
- **Docker** enters through Model Runner (2025-04-09) and through people: Eric Curtin — a co-creator of RamaLama (an `@redhat.com` address in commits from July–August 2025), now in the profile "Docker, Inc", with commits to llmman and `docker/model-runner` from `@docker.com` (July–October 2026). Employment dates: I could not establish. Three tools (llmman, RamaLama, Docker Model Runner) have a similar function and a person in common — *expect consolidation (unverified)*.
- **LM Studio buys Locally AI** (April 2026; the team behind an iOS/iPadOS app; the "Locally" app in June 2026) *(company's own claim, Wikipedia)*.

### 3.5 A cross-cutting observation (my interpretation)

All these moves fall into one pattern: **whoever sells hardware or subscriptions buys the software layer that decides where the model will run** *(unverified — an inference from putting the facts together, none of the companies phrased it that way)*. On top of that comes a second thread: **the same ~30 people move between the same ~10 employers** — Awni Hannun from Apple to Anthropic, Eric Curtin from Red Hat to Docker, Ying Sheng from Databricks/xAI to RadixArk, Zhuohan Li and Lianmin Zheng to Meta, Gerganov/Buehler/Kim to HF *(GitHub profiles)*. The same Berkeley laboratory produced both competing engines (vLLM and SGLang) and both startups.

### 3.6 Timeline 2022–2026

Only dates checked in the notes: **(V)** = checked in the API/a primary source, **(F)** = announcement date given by the company, **(P)** = date given in the press.

| Date | Event | Tag |
|---|---|---|
| 2022-09-18 / 2022-09-25 | the ggml and whisper.cpp repositories created (Gerganov) | V (API) |
| 2023-02-09 | first vLLM commits (Berkeley) | V |
| 2023-03-10 | first llama.cpp commits (README; repo created 18:58 UTC) | V |
| 2023-03-22 | Mozilla announces Mozilla.ai and a 30 million USD commitment | F (Mozilla blog) |
| 2023 (month unknown) | ggml.ai founded; pre-seed from Friedman and Gross, amount undisclosed | F (ggml.ai) |
| 2023-06-26 / 2023-07-08 | Ollama repository / version v0.0.1 | V |
| 2023-08-16 / 2023-08-17 | TensorRT-LLM / Jan repositories | V |
| 2023-09-12 | PagedAttention/vLLM paper (SOSP 2023) on arXiv | V |
| 2023-11-28 | MLX: first commit (Apple) | V |
| 2024-01-08 | SGLang repository | V |
| 2024-03 | Redis switches to SSPL | V (Redis blog) |
| 2024-07 | post on open governance of vLLM; incubation at LF AI & Data | V (post title); details: press |
| 2024-09 | LMSYS Corp. registers as a non-profit | V (lmsys.org) |
| 2024-11 | antirez returns to Redis part-time | V |
| 2024-11-12 → 2025-01-13 | Red Hat announces, then closes the acquisition of Neural Magic | V (Red Hat announcements) |
| 2025-03 | TensorRT-LLM: development entirely on GitHub (year from the order of README entries) | V (year: inference) |
| 2025-04-09 | Docker Model Runner (beta, Docker Desktop 4.40) | V (Docker blog) |
| 2025-04-19 | Open WebUI: a license with a brand clause (v0.6.6) | V |
| 2025-05-01 | Redis 8: AGPLv3 option | V |
| 2025-05-06 | vLLM becomes a project hosted by the PyTorch Foundation | V |
| 2025-05-27 | last push to GPT4All | V (API) |
| 2025-07-08 | LM Studio "free for use at work" | V (blog) |
| 2025-09-24 | Modular: 250 million USD, valuation 1.6 billion USD | F |
| 2025-12-19 | last TGI release (v3.3.7) | V |
| 2026-01 (day not established) | Inferact launch, 150 million USD seed | F; the press confirms the amount |
| 2026-01-21 | TechCrunch: SGLang → RadixArk, valuation about 400 million USD | P |
| **2026-02-20** | **ggml.ai (llama.cpp) joins Hugging Face** | V |
| 2026-03-21 | last TGI commit; repository archived | V |
| 2026-03-30 | preview of the MLX engine in Ollama (Apple silicon) | V (list of blog entries) |
| 2026-05-06 | ds4 repository created | V |
| 2026-06-24 / 2026-07-29 | Qualcomm announces / closes the acquisition of Modular | V |
| 2026-07-01 | Together AI: Series C 800 million USD | F |
| 2026-07-09 | Ollama: "88 million USD", "8.9 million developers" | F |
| 2026-08-26 / 2026-09-03 | **reports of NVIDIA acquiring HF (12.93 billion USD)** / the "confirms" article | **P — no statement from the companies** |
| 2026-09-22 | the author of oMLX joins HF | V (HF blog) |
| 2026-10-14 | Modal: Series D 750 million USD, valuation 15.75 billion USD, ARR 1 billion USD | F |
| 2026-10 (day not established) | Inferact–AMD Instinct collaboration | F |

I left out of this timeline entries from a single secondary source (among them Fireworks AI's Series C and D, the beginning of LM Studio in May 2023, HF's 2023 rounds) — they return below with the appropriate tag.

---

## 4. Hosted inference on top (briefly)

Above the open engines operates a layer of companies that sell **GPU hours**. That is where the largest valuations are — and it explains why engines are an "add-on commodity" for many players.

| Company | What it sells | Money | Tag |
|---|---|---|---|
| **Together AI** | inference API, GPU clusters, post-training; its own stack (FlashAttention-4, "Together Megakernel", `together.compile`); the founders include Tri Dao, Percy Liang, Chris Ré, Ce Zhang, Vipul Ved Prakash (company site) | Series C **800 million USD, 2026-07-01**; investors including Aramco Ventures, NVIDIA, Vista Equity, General Catalyst, Salesforce Ventures; no valuation given; compute commitments of 500 MW | *(company's own claim)* |
| **Fireworks AI** | API for open models, training API, its own model "Ember-1" (September 2026) | Series B 52 million USD (July 2024, Sequoia); Series C 250 million USD at 4 billion USD (October 2025); **Series D 1.51 billion USD at 17.5 billion USD (July 2026)**; CEO Lin Qiao (previously Meta, PyTorch) | *(press report — only Wikipedia; I did not find the company's site)* |
| **Baseten** | dedicated inference, model APIs (DeepSeek/GLM/Kimi), training; customers: Cursor, Notion, Zed, Canva, Vercel | I **did not find** funding; the site does not name specific engines | *(company's own claim)* |
| **Modal** | serverless GPU: inference, sandboxes for agents, training | **Series D 750 million USD at 15.75 billion USD, 2026-10-14, Accel**; ARR 1 billion USD; usage "tripled" in 5 months | *(company's own claim)* |

**A cautious conclusion.** The valuations of hosted inference (15–18 billion USD, if we believe the companies and Wikipedia) are an order of magnitude larger than those of engine startups (0.4–0.8 billion USD); the notes read this to mean that **engines are bait and a talent funnel, and the cash is in GPU hours** *(unverified — an interpretation of the comparison, not a fact)*. All the amounts in this table are company claims or press; I checked none of them in registries.

---

## 5. Who is who — a directory of people

Rules: **only public, professional roles**; "role" is what the GitHub profile or the company site declares; "track record" is what could be checked in the API, an article or the repository. The employer from a profile may be out of date. Commit counts — from the API, 2026-10-19.

| Person | Role / affiliation | Project | Track record (checked) |
|---|---|---|---|
| **Georgi Gerganov** (`ggerganov`) | creator; profile: `@huggingface` | ggml, llama.cpp, whisper.cpp | repositories ggml (2022-09-18) and whisper.cpp (2022-09-25); 2,035 commits in llama.cpp (the most; the next 630); owner of the `ggml/include`, CPU and Metal directories in CODEOWNERS |
| **Xuan-Son Nguyen** (`ngxson`) | HF, France | llama.cpp | 630 commits; server and multimodality (CODEOWNER of `llama-server`, `llama-mtmd`) |
| **Aleksander Grygier** (`allozaur`) | HF | llama.cpp | 143 commits; the llama-server web interface (`llama-ui`) |
| **Johannes Gäßler** (`JohannesGaessler`) | KIT (Karlsruhe); independent of HF | llama.cpp | 402 commits; CUDA, multi-GPU, the GGUF module; author of the "meta backend" (tensor parallel) |
| **Diego Devesa** (`slaren`) | no employer in the profile | ggml | 362 commits; author of the ggml backend/allocator/scheduler |
| **Jeff Bolz** (`jeffbolznv`) | NVIDIA *(profile)* | llama.cpp | 316 commits; the Vulkan backend |
| **Iwan Kawrakow** (`ikawrakow`) | independent ("Gentleman at large") | ik_llama.cpp | author of the k-quants and i-quants; 100 commits in llama.cpp, left the project in March 2024 *(their own words in discussion #316)*; runs the ik_llama.cpp fork |
| **Benson Wong** (`mostlygeek`) | "Tailscale and Elethink" *(profile)* | llama-swap | 536 of about 653 commits; releases v262–v265 in October 2026 |
| **Jeffrey Morgan** (`jmorganca`) | co-founder of Ollama; previously Docker, Twitter, Google *(profile)* | Ollama | 928 commits; together with Chiang, Kitematic ("acquired by Docker in 2015") *(company's own claim)* |
| **Michael Chiang** (`mchiang0610`) | co-founder of Ollama | Ollama | Kitematic → Docker Desktop *(company's own claim)* |
| **Woosuk Kwon** (`WoosukKwon`) | Inferact | vLLM | first author of the PagedAttention paper (arXiv 2309.06180); 873 commits; "lead maintainer" per the governance document |
| **Simon Mo** | co-founder of Inferact, lead maintainer of vLLM *(profile, Inferact site)* | vLLM | among the Core Maintainers (the project's technical committee) |
| **Kaichao You** (`youkaichao`) | "Co-Founder & Chief Scientist" of Inferact; PhD at Tsinghua *(profile)* | vLLM | 471 commits |
| **Zhuohan Li** | profile: "vLLM / Meta" | vLLM | second author of the PagedAttention paper; lead maintainer of vLLM per the governance document |
| **Michael Goin** (`mgoin`) | Red Hat/Neural Magic *(profile)* | vLLM | 650 commits (9% of the top-15) |
| **Ying Sheng** | CEO and co-founder of RadixArk; previously xAI, Databricks *(press report)* | SGLang | last author of the SGLang paper; co-author of the vLLM paper |
| **Lianmin Zheng** (`merrymercy`) | profile: Meta | SGLang | first author of the SGLang paper; 1,267 commits |
| **Liangsheng Yin** (`hnyls2002`) | RadixArk *(profile)* | SGLang | 1,205 commits; second author of the paper |
| **Chris Lattner** | EVP, Advanced AI Software and Platforms, Qualcomm (co-founder of Modular) | Modular, MAX/Mojo | role confirmed on the Modular site and in the closing announcement; I do not describe earlier achievements because in the notes they are marked as unverified |
| **Tim Davis** | co-founder of Modular → "SVP & GM of Modular, Qualcomm" | Modular | as above |
| **Awni Hannun** (`awni`) | profile: "Research at Anthropic. Prev: co-created MLX at Apple" | MLX, mlx-lm | co-author of the MLX paper (with Digani, Katharopoulos, Collobert); 718 commits in MLX (#1), the last from an Apple address 2026-02-24 |
| **Jun Kim** (`jundot`) | engineer at Hugging Face since 2026-09-22 | oMLX | 2,110 of about 2,280 commits in the top-5; HF blog of 2026-09-22 |
| **Salvatore Sanfilippo** (antirez) | Redis, part-time developer evangelist since November 2024 | ds4 | creator of Redis; 523 commits in ds4; argued for Redis returning from SSPL to AGPL (Redis 8, 2025-05-01) |
| **Eric Buehler** (`EricLBuehler`) | profile: `@huggingface` | mistral.rs | 3,073 commits (the next 125); 75 of 82 non-bot commits in the last 90 days |
| **Eric Curtin** (`ericcurtin`) | profile: "Docker, Inc"; previously `@redhat.com` | llmman, RamaLama, Docker Model Runner | 402 commits in llmman; 971 in RamaLama (#2); 318 in model-runner (#3) |
| **Dan Walsh** (`rhatdan`) | profile: "Retired" | RamaLama | 1,462 commits (#1) |
| **Ettore Di Giacinto** (`mudler`) | "ex-SUSE/Rancher, ex-gentoo" *(profile)* | LocalAI | 3,507 commits |
| **Daniel Han** (`danielhanchen`) and **Michael Han** (`shimmyshimmer`) | co-founders of Unsloth AI Inc. (YC summer 2024) | Unsloth | 6,391 and 808 commits; Daniel Han previously at NVIDIA per the YC page |
| **Justine Tunney** (`jart`) | author of Cosmopolitan libc; Mozilla Builders | llamafile | 600 commits; 42 sponsors on GitHub Sponsors |
| **Timothy Baek** (`tjbck`) | founder of Open WebUI Inc. | Open WebUI | 13,450 commits; 42 sponsors |
| **Alex Cheema** | exo labs (profile: "University of Oxford", probably out of date) | exo | 1,424 commits |
| **Nat Friedman**, **Daniel Gross** | pre-seed investors in ggml.ai (2023) | ggml.ai | *(company's own claim: ggml.ai)*, amount undisclosed |

**What is not here.** People known in the notes only by a pseudonym (among them `kyuz0`, `mitsuhiko` in ds4) and any private details. Michael Chiang's full name comes from Wikipedia *(third-party source)*; I did not establish the title of Yagil Burowski (LM Studio).

> **Check it yourself — employers and e-mail addresses in commits.** A profile is a declaration, and the address in a commit is a clue independent of the profile:
> ```bash
> gh api 'repos/llmmanorg/llmman/commits?per_page=1' --jq '.[0].commit.author'
> gh api users/mostlygeek --jq '{name, company, location, bio}'
> gh api orgs/ggml-org --jq '{login, description, public_repos, created_at}'
> ```
> (not run in exactly this form). In the survey, exactly this kind of data showed that Eric Curtin's commits to llmman in October 2026 have the domain `@docker.com`, and those to RamaLama in July–August 2025 `@redhat.com`. The organization page github.com/ggml-org speaks of "16 core team members".

---

## 6. Licenses: a table and gotchas

I checked the licenses in the texts of the `LICENSE` files (in trees on the machine with the cards: `~/llama.cpp-0ce8cd1/LICENSE` and `~/runtimes-src/*/LICENSE` for nine projects; for the rest — the raw file from GitHub, 2026-10-19). The "SPDX" column is what the GitHub API returns; the value `NOASSERTION` means the automation did not recognize a single license, often because the file has the header of one license plus addenda.

| Project | SPDX (API) | What is allowed | Gotchas and notes |
|---|---|---|---|
| **llama.cpp, ggml, whisper.cpp** | MIT | almost everything, keeping the notice | "Copyright (c) 2023-2026 The ggml authors"; no patent clause; the organization is now owned by HF; the brand (`llama.brand`) has NOASSERTION, i.e. it is *not* covered by MIT |
| **ds4** | MIT | almost everything | LICENSE contains three copyright lines: the authors of ds4.c, the authors of ggml (2023–2026), DeepSeek (2023) — the notes tie this to adapted code and format |
| **Ollama** | MIT | almost everything | MIT covers the **code**; the cloud service, the model registry and the terms of hosted models are separate; **each model has its own license**; the notes record thread #3185, open since 2024-03-16, about not distributing license notices in release artifacts (state at the survey date: open; whether it was fixed — I could not establish) |
| **mistral.rs, LocalAI, MLX, mlx-lm, `lms` (LM Studio CLI), llama-swap, ik_llama.cpp, AnythingLLM, GPT4All, RamaLama** | MIT | almost everything | MLX: "Copyright © 2023 Apple Inc."; the hosted AnythingLLM product is separate |
| **vLLM, SGLang, llmman, oMLX, Lemonade, Docker Model Runner, exo, KTransformers, llm-d, LMCache, mlc-llm, TGI** | Apache-2.0 | commercial use, changes, **a patent grant** | patent retaliation clause; keep the NOTICE file; vLLM is owned by a foundation (PyTorch Foundation), SGLang — by LMSYS |
| **TensorRT-LLM** | NOASSERTION (in essence Apache-2.0 + notices) | as Apache-2.0 | LICENSE = an Apache-2.0 header + about 790 lines of third-party notices (MIT, BSD-3, Apache); **telemetry** enabled by default, opt-out described in the README (code in `tensorrt_llm/usage/`); works only on NVIDIA GPUs and depends on closed CUDA/TensorRT libraries *(unverified in the build files)* |
| **Dynamo** | NOASSERTION (Apache-2.0 + a note on test data) | as Apache-2.0 | orchestrates vLLM/SGLang/TRT-LLM |
| **Jan** | NOASSERTION (Apache-2.0 + a sentence on attribution) | as Apache-2.0 | "Attribution is requested in user-facing documentation" — a request, not a condition of the license; copyright Menlo Research 2025 |
| **llamafile** | NOASSERTION in the API; the LICENSE file = Apache-2.0, "Copyright 2023 Mozilla Foundation" | as Apache-2.0 | contains llama.cpp (MIT), whisper.cpp (MIT), Cosmopolitan; version 0.10 has a new build system |
| **Open WebUI** | NOASSERTION ("Open WebUI License") | BSD-3 rights **plus** clause 4 | **you may not change, remove or replace the "Open WebUI" branding**, unless: ≤ 50 end users within 30 days, written permission, or an enterprise license; CLA for contributors; code up to v0.6.5 remains BSD-3, earlier MIT (LICENSE_HISTORY); **this is not an OSI-approved license** |
| **Modular (repository)** | NOASSERTION: Apache-2.0 **with LLVM exceptions** | as Apache-2.0 + the LLVM exception | **MAX** is under the "Modular Community License": free, with no accelerator limit (the former limit of "eight accelerators outside x86, ARM and NVIDIA" is gone), but **offering MAX as a hosted service to other parties requires written permission and compliance with the trademark**; you may not use MAX as training data to build a replacement *(summary of the license page)* |
| **LiteLLM** | NOASSERTION (MIT + the `enterprise/` directory) | MIT outside `enterprise/` | the contents of `enterprise/` "for production only" with a BerriAI subscription (per seat) |
| **Unsloth** | Apache-2.0 (root) | core Apache-2.0 | `studio/` under **AGPL-3.0-only** (Unsloth AI Inc.) — network copyleft: embedding Studio in a closed hosted product is out |
| **LM Studio (application)** | — (closed EULA) | personal and "internal business" use (free for work since 2025-07-08) | no redistribution, no reverse engineering, no SaaS/service bureau; liability limited to 50 USD; terms may change; **the freedom "for work" is a blog post, not a contract** |
| **KoboldCpp** | AGPL-3.0 | use and changes | network copyleft for hosted forks |
| **Redis (context)** | AGPLv3 as an option since Redis 8 (2025-05-01) | — | history: SSPL (March 2024) → AGPL; relicensing can go both ways |

**Model weights are a separate legal layer.** All the licenses above concern **code**. A model file (e.g. your DeepSeek-V4-Flash in the `UD-IQ3_XXS` quant) has its own weights license and — if it comes from an Unsloth repository — is a *derivative* of the original weights, so the terms of the base model apply. **The notes contain neither the text of the DeepSeek weights license nor a description of the terms of the Unsloth repositories with GGUFs. I could not establish them** and I will not guess. Check them at the source (box below).

> **Check it yourself — licenses.**
> ```bash
> # 1. what GitHub says about the code license
> gh api repos/ggml-org/llama.cpp --jq '.license.spdx_id'
> gh api repos/open-webui/open-webui --jq '.license.spdx_id'      # expect NOASSERTION
> # 2. the full text — it decides, not the SPDX field
> curl -s https://raw.githubusercontent.com/open-webui/open-webui/main/LICENSE | head -60
> # 3. the history of Open WebUI license changes (a file mentioned in the notes)
> curl -s https://raw.githubusercontent.com/open-webui/open-webui/main/LICENSE_HISTORY | head -60
> # 4. on the machine with the cards
> head -5 ~/llama.cpp-0ce8cd1/LICENSE
> ```
> (I did not run these commands in this form; the file names `LICENSE` and `LICENSE_HISTORY` and the `main` branch are an assumption — if `main` does not exist, check the default branch). For the model: open the **model card and the LICENSE file** in the repository of the base DeepSeek-V4-Flash model on Hugging Face and in the Unsloth repository with your GGUF file, and compare. On this matter I have no data from the survey.

---

## 7. Dependency risk: what will happen to the reference stack

### 7.1 Ten "follow the money" patterns and their consequences

| # | Pattern | Mechanism | Examples | What it means for a dependent user |
|---|---|---|---|---|
| 1 | **The platform takes over the maintainers** | a hub or cloud absorbs a project run by its founder; the code stays open, the roadmap moves closer to the platform | ggml.ai→HF (2026-02-20); oMLX→HF (2026-09-22); mistral.rs→HF (profile); Neural Magic→Red Hat; Modular→Qualcomm | low risk of abandonment, **medium risk of steering**; keep the ability to fork MIT/Apache; watch the ownership chain (HF→NVIDIA — reports) |
| 2 | **Hardware pulls software** | software is free because it sells silicon | NVIDIA (TRT-LLM, Dynamo, NIM→AI Enterprise); AMD (Lemonade, contributions to vLLM-ROCm); Apple (MLX); Qualcomm (Modular); Intel/AMD/Google as vLLM sponsors | features follow the vendor's products; AMD paths are liked where AMD sells something (Instinct, Strix Halo, Ryzen AI) — the R9700 cards are in the middle |
| 3 | **Foundation neutrality** | a project moves to a neutral legal home | vLLM→PyTorch Foundation (2025-05-06), LF AI & Data (2024); SGLang→LMSYS; (llama.cpp is **not** in a foundation, the corporate home is HF) | the best protection against a license change; does **not** protect against employer concentration |
| 4 | **VC + free open source + cloud as an upsell** | the free runtime is a funnel; revenue from hosted usage | Ollama, LM Studio (Bionic/Teams), AnythingLLM (hosted), Inferact Cloud, RadixArk hosting | the local application is bait; watch default login windows, telemetry, "sign in to the cloud" screens |
| 5 | **Engine → startup → company platform** | the engine handed to a foundation, the founders make a company | Inferact, RadixArk, Together, Fireworks, Baseten, Modal | fine for a data center; for local machines relevant only through the shared engine code |
| 6 | **Open-core / source-available / a brand lock** | the core free, the strategic element restricted | Open WebUI (v0.6.6, 2025-04-19), LiteLLM (`enterprise/`), Unsloth (Studio AGPL), Modular Community License | read the license at every embedding and redistribution; "open source in the OSI sense" has stopped being a safe assumption |
| 7 | **A subscription to a distribution of an open engine** | customers pay for support, indemnification, certification | Red Hat AI Inference (per accelerator), NVIDIA AI Enterprise (4,500 USD/GPU/year), Docker Desktop (Model Runner as a feature) | adopters in corporations will go this way; hobbyist and devops machines do not have to |
| 8 | **A corporate project with employees** | one company writes most of the commits | Ollama, TRT-LLM, MLX (Apple), Lemonade (AMD), Docker Model Runner | fast and coherent; subject to the sponsor's strategy changes and layoffs (example: Awni Hannun's departure from Apple to Anthropic) |
| 9 | **A BDFL on sponsorship or after hours** | one person, little or no funding | antirez/ds4, mudler/LocalAI, llama-swap, llmman, ik_llama.cpp | high pace, *bus factor* = 1; MIT/Apache allow a fork, but not painlessly |
| 10 | **Pivot or zombie** | a company finds a better market, the OSS asset gets "parked" | Nomic→AEC (GPT4All: last push 2025-05-27); Menlo (Jan)→humanoid robots; TGI archived; llamafile "refreshed" by Mozilla.ai | do not base critical processes on marketing-driven projects without checking the date of the last commit |

### 7.2 The reference stack, element by element

The risk scale below is **my assessment** based on the facts of sections 2–6, not a measurement.

| Element | Who is behind it | If it is acquired | If it changes license | If it is abandoned | Exit cost |
|---|---|---|---|---|---|
| **llama.cpp** (MIT; build `0ce8cd1` on the reference machine — in the survey this is the production version) | the ggml.ai team at HF; 24.5k forks | HF→NVIDIA *(reports)*: license unchanged; the risk is **steering of the roadmap** | released MIT versions do not stop being MIT (a general rule; an example from the notes: Open WebUI — code ≤ v0.6.5 stayed BSD-3 despite the later change); the real threat concerns *future* versions | low: 73% of the top-12's commits from people on HF salaries; but **one employer** | **low**, if you pin the build and keep a copy of the sources |
| **HIP backend / gfx1201** | CUDA code compiled as HIP; RDNA4 branches in `common.cuh`; CODEOWNERS for CUDA: Gäßler, am17an, IMbackK, ORippler | CUDA-first at HF/NVIDIA affects you too, but the AMD path "rides" on the shared code | as above | depends the most on a few people; the notes do not give the employers of some of them | medium: a switch to Vulkan (the backend is maintained by, among others, 0cc4m and Jeff Bolz of NVIDIA) |
| **llama-swap** (MIT, 6.0k stars) | **one** maintainer (82% of commits), works elsewhere; 0 sponsors | not applicable (a person, not a company) | MIT, small Go code | **real**: a single point of failure; a release cycle of every few days is a plus today | **low–medium**: the built-in llama.cpp router (`--models-dir`, `--models-max` default 4, LRU eviction) covers ordinary switching; you lose groups/the matrix (`matrix`) for arranging models across four GPUs, upstreams other than llama, and the UI |
| **Unsloth GGUFs** (`UD-…`) | Unsloth AI Inc. (YC, 12 people per the YC page); Daniel Han ≈ 56% of the repo's commits | company bought: *existing files do not change*; the risk concerns future releases and terms | files already downloaded stay; a change would concern new ones | you lose **fast quants of new models and fixes** (docs: they helped fix llama.cpp bugs — *(company's own claim)*) | **low for operation**, **medium for reproducibility**: "UD-" and `_XL` are Unsloth labels (llama.cpp has no `Q4_K_XL` type; the GGUF header holds the nearest standard type, e.g. `file_type = 23` = `MOSTLY_IQ3_XXS`), so plain llama.cpp reads the file; **the recipe tooling is not in the public repo**, so you will not reproduce the identical mix — you can imitate it with `llama-quantize --imatrix … --tensor-type <regex>=<type>`; in the repository I checked (Qwen3-Coder-30B-A3B), the imatrix file (122 MB) is published; **I did not check this for your DeepSeek file** |
| **DeepSeek weights (license)** | DeepSeek; derivatives: Unsloth | — | — | — | **I could not establish** (absent from the notes); see section 6 |
| **Hugging Face as the Hub** | HF (valuation 4.5 billion USD in 2023 *(press report)*; reports of 12.93 billion from NVIDIA) | if the reports are confirmed: a change of owner of the provider you download models from; the Hub's terms and availability are not in the notes | — | — | keep local copies of the files (see the list below) |

**The Mac side.**

| Element | Sponsor and risk | Exit cost |
|---|---|---|
| **MLX / mlx-lm** (MIT) | Apple pays the core team (zcbenz, angeloskath, jagrit06 — *(profile)*); a co-creator has left; Apple can reduce its investment at any time. Mitigating: the ecosystem (HF/oMLX, LM Studio, the MLX preview in Ollama 2026-03-30) depends on it, so community maintenance is likely *(unverified)* | low (MIT) |
| **oMLX** (Apache-2.0) | funded by HF since 2026-09-22; the risk has shifted from "the hobbyist will burn out" to "the roadmap follows HF" | low |
| **LM Studio** (closed) | Element Labs, funding unknown; free-for-work is a post, not a contract; binaries frozen if the service goes down | **low**: models lie as ordinary files in `~/.lmstudio/models`; but you cannot fork the GUI and the daemon |
| **Ollama** (MIT code) | VC, cloud; the "moat" is the model library, templates, parsers, the cloud; pricing has already changed once (GPU time → tokens, 2026-08-31); the cloud login window is in the default flow, there is an `OLLAMA_NO_CLOUD` variable | **medium**: models in the blob layout require re-export; a fork of the code is possible |
| **ds4** (MIT) | one person's hobby; ~24k stars, about 2.3k forks; the code is small and readable; **on AMD, `gfx1151` (Strix Halo) is supported, not your `gfx1201`** — see `07-APPLE-MLX-OMLX-AND-DS4.md` | low |

**If you ever moved to vLLM:** the best-protected of the data-center engines (Apache-2.0 + a foundation + many corporate committers); half of the core work is today done by employees of one company (Inferact), and the second circle is Red Hat, AMD, HF and Meta. An AMD engineer is #9 among committers, so ROCm is funded by AMD — but Inferact's roadmap, according to the company's announcements, is TPU and Instinct, not RDNA4 *(unverified)*. **Telemetry enabled by default**: vLLM sends usage statistics (to disable: `VLLM_NO_USAGE_STATS=1` or `DO_NOT_TRACK=1`), and so does TensorRT-LLM (`TRTLLM_NO_USAGE_STATS=1`, `DO_NOT_TRACK=1`, `--no-telemetry`); for SGLang I found no telemetry. This is a small example, visible in the code, of an organization's motivation. See `06-SERVING-ENGINES-VLLM-SGLANG.md`.

### 7.3 A safeguards checklist

1. **Pin versions.** You already do this for llama.cpp (`0ce8cd1`). Record the llama-swap versions too (releases have consecutive integer numbers, e.g. v265 from 2026-10-14) and the hashes of the GGUF files.
2. **Keep a local copy** of the sources of the pinned commit, the `LICENSE` file and the GGUF files you base production on. The Hub is someone else's service.
3. **Write down who owns each element of the stack** (one sentence, with a date) — table 7.2 is a template. Repeat every quarter.
4. **Watch early signals**: a change of the `company` field for the main committers, new `LICENSE*` files, archiving of repositories (like TGI), a "pivot" in a company's description.
5. **Five questions for every new tool**: who pays the creators? what does the company earn from? what is the license (read the text)? what is the *bus factor*? what is the way out (model format, API)?
6. **Prefer open formats and APIs compatible with OpenAI/Anthropic** — this lowers the exit cost from any wrapper (see `05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md`).

> **Check it yourself — is the Ollama license thread still open.** The notes record that issue #3185 ("ollama doesn't distribute notice licenses in its release artifacts", opened 2024-03-16, 59 comments) was open at the survey date:
> ```bash
> gh api repos/ollama/ollama/issues/3185 --jq '{state, comments, title}'
> ```
> (I did not run this call). This is an example of "I check the state of the thread instead of repeating an opinion". The notes also record the other side's argument: the Ollama README today contains a "Supported backends" section with an acknowledgment of the llama.cpp project and Georgi Gerganov.

> **Check it yourself — is NVIDIA–HF confirmed at the source.** Open `nvidianews.nvidia.com` and `huggingface.co/blog` and look for an announcement from the end of August / the beginning of September 2026. At the time of the survey **I found none** — which is why the text says "according to press reports". If the announcement is already there, update section 3.2.

### 7.4 What this means for a 4× R9700 + Mac setup (with agentic applications)

- **The biggest single operational risk is not in what is loud** (HF/NVIDIA), but in what is quiet: **llama-swap = one person**. The good news: the exit is cheap, because llama.cpp has its own router; the bad scenario is losing the arrangement of models (`matrix`) across four GPUs, not losing the ability to run.
- **llama.cpp is today the best "funded" element of the reference stack** (salaries at HF), and at the same time the most exposed to a change of owner. For production, pinning the version and keeping a copy of the sources matter, not discussions about intentions.
- **The R9700 cards are probably nobody's strategic target** *(unverified — an inference from where AMD declares investments: Instinct, Strix Halo, Ryzen AI)*: neither NVIDIA nor Apple cares here, and AMD sells mainly those three lines. The HIP path in llama.cpp works because it shares the CUDA code. Do not count on anyone polishing it for RDNA4 for business reasons.
- **Mac:** the least risky are the formats (GGUF files and MLX weights lie on disk), the most risky — closed applications and cloud upsells. Choose tools you can leave with a file.

---

## 8. What you can learn for your own plans

This section is for readers who build agentic applications on local models and are thinking about an assistant in Polish. Below are **solely lessons from the cases described**. **The notes contain no data on the Polish market, on Polish-language models, on Polish funding programs, or on customers' readiness to pay** — I compute nothing of this here and estimate nothing. Where something would require such data, I write "for you to check".

### 8.1 Seven lessons from the cases

1. **First answer: who pays for your time a year from now?** The projects that (my synthesis of the cases in section 2) survived with paid maintainers had one of three things: a hardware maker (AMD, NVIDIA, Apple), a platform (HF, Red Hat, Docker) or a VC with a cloud (Ollama, Inferact). Projects run after hours (ds4, llama-swap, LocalAI) have a great pace and a bus factor of 1. This is not an assessment of quality, only a description of risk.
2. **A free local application is a funnel — it must have something paid at the end.** Ollama (cloud from 20 USD/month), LM Studio (Bionic, Teams), AnythingLLM (hosted team) sell **hosted models and team features**, not the application itself. The side cost: login windows and default paths to the cloud (which forced the `OLLAMA_NO_CLOUD` option). Users of local tools read such signals.
3. **Remove friction for individuals, charge organizations for control.** LM Studio removed the form for use at work (2025-07-08), and the Teams/Enterprise plans are paid (SSO, gating of models and MCP, zero retention); Open WebUI sells SSO/SCIM, white-labeling and isolated terminals; Red Hat sells support priced per accelerator; NVIDIA — a supported container. **What organizations pay for in these cases is control, compliance and support — not token speed itself.**
4. **A license is a business tool, choose it early and deliberately.** Open WebUI went from MIT to BSD-3 and then (v0.6.6, 2025-04-19) to a license with a brand clause, and the CLA allows further changes; Unsloth split the core (Apache-2.0) from Studio (AGPL-3.0); Redis went SSPL → AGPL. For a founder this is flexibility; for an adopter — a risk, which you write about in section 6. If you build your own tool, ask yourself the same question from the perspective of *your* user.
5. **A pivot is visible in the date of the last commit.** GPT4All (2025-05-27), Jan/Menlo (robots), TGI (archive) show that an application that is a funnel for another business freezes when the business changes. If your assistant is to be a funnel to something else, say so plainly to users.
6. **A neutral home protects the license, not the roadmap.** vLLM (PyTorch Foundation) and SGLang (LMSYS) have a low risk of relicensing, and yet the largest block of committers are employees of one company. If you want outside contributors, neutrality matters; if you want to control the direction, you have to do it deliberately.
7. **Services around deployment are a real model — but only where the customer has hardware or compliance requirements.** Inferact offers a "platform on your resources" and a cloud on your own GPUs, Red Hat — support, NVIDIA — supported containers. All three are built on **large-scale deployments**; whether this scales down to individual local companies — **does not follow from the notes**.

### 8.2 Hypotheses to test (not recommendations)

The table below sets revenue models against the cases that support them and those that warn against them, and against **what you would have to find out yourself**. No market numbers.

| Revenue model for a local assistant in Polish | A case for "yes" | A case for "caution" | For you to check |
|---|---|---|---|
| a free assistant + a paid team/enterprise version (SSO, policies, audit) | LM Studio (free-for-work + Teams/Enterprise), Open WebUI Enterprise | the "free" terms may change (a post, not a contract); Open WebUI tightened the license after adoption | whether your users are organizations that need control; who makes the purchasing decision |
| deployment services and support for companies running locally | Red Hat AI Inference, Inferact Platform, NVIDIA AI Enterprise | all rely on the scale and hardware of large customers | whether there is demand for support for small installations; what your time costs |
| a hosted version of the same models (cloud) next to the local one | Ollama Cloud, LM Studio Bionic, AnythingLLM hosted | you compete with the big hosts (Together, Fireworks, Baseten, Modal), whose valuations are an order of magnitude higher | who your customer is when local execution is their reason for buying |
| two licenses (an open core + an interface under AGPL) | Unsloth (Apache-2.0 + AGPL Studio) | "open source" in the OSI sense becomes less obvious (Open WebUI) | whether your customers accept AGPL; what about contributors (CLA?) |
| sponsorship / grants (funding without a product) | LocalAI (Spectro Cloud), oobabooga (a16z grant 2023), Mozilla.ai (30 million USD commitment) | small amounts and uncertain continuity; in the notes: 10–53 sponsors per project | whether Polish/EU programs exist — **the notes are silent on this** |

---

**Where next.** A comparison of the engines' technical properties and the choice for the reference machine: `09-COMPARISON-AND-CHOICE.md`. The list of sources and their assessment: `SOURCES.md`. Return to the map of layers: `01-MAP-AND-LAYERS.md`.
