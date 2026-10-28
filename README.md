# llm-education

**Two courses on how local language models really work and how to build an agent around them
that you can trust — plus a survey of ready-made agent harnesses.**

> **Structure:** the course content exists in two languages. English: [`en/`](en/). Polish (the original): [`pl/`](pl/).
> Polish version of this page: [README_PL.md](README_PL.md).

![Language: English and Polish](https://img.shields.io/badge/language-English%20%2B%20Polish-red)
![Course 1: 10 parts, ~47 h](https://img.shields.io/badge/course%201-10%20parts%20·%20~47%20h-blue)
![Course 2: 19 parts, ~102 h](https://img.shields.io/badge/course%202-19%20parts%20·%20~102%20h-blue)
![Survey: 20 agent harnesses](https://img.shields.io/badge/survey-20%20agent%20harnesses-orange)
![Survey: 15 AI assistants](https://img.shields.io/badge/survey-15%20AI%20assistants-orange)
![License: CC BY 4.0 + MIT](https://img.shields.io/badge/license-CC%20BY%204.0%20%2B%20MIT-lightgrey)

No frameworks to start with and no magic. You build every mechanism yourself, from scratch, on models running
**on your own computer**: tokenizer, sampling, grammars, a vector database, the agent loop, a sandbox,
a scheduler, evaluation. Only once you understand what a library does do you choose ready-made tools consciously.

The courses began as my own study plan on a home machine with AMD Radeon AI PRO R9700 cards
(ROCm + [llama.cpp](https://github.com/ggml-org/llama.cpp)). I am sharing them in the hope that they will be useful to
others who are learning.

---

## What is inside

Every link below has two versions: the English one under `en/` and the Polish original under `pl/`
(the same file layout, with Polish directory and file names).

### Course 1 — [from a model to your own agent](en/course_local_models/00-COURSE-INDEX.md) (`en/course_local_models/`, Polish: [`pl/kurs_lokalne_modele/`](pl/kurs_lokalne_modele/00-KURS-INDEKS.md))

After this course you can build from scratch your own agent that reads files, writes code, runs commands,
sees images, listens and speaks, remembers context and works offline — and you understand every layer underneath it.

| Part | Topic | What you build |
|---|---|---|
| [01](en/course_local_models/LOCAL-MODELS-FUNDAMENTALS.md) | Fundamentals | tokens, weights, runtime, server; `llama-cli`, `llama-server`, `curl` |
| [02](en/course_local_models/02-MODEL-INTERNALS.md) | Model internals | tokenizer, logits, sampling, KV-cache, embeddings — computed by hand |
| [03](en/course_local_models/03-CONTROL-AND-RELIABILITY.md) | Control | chat template, GBNF grammars, determinism, an evaluation harness |
| [04](en/course_local_models/04-MEMORY-RAG-AND-CONTEXT.md) | Memory (RAG) | a vector database in sqlite from scratch, chunking, BM25, reranking, citations |
| [05](en/course_local_models/05-MULTIMODALITY.md) | Senses | vision, Whisper (hearing), Piper (speech) + a hardware list |
| [06](en/course_local_models/06-AGENT-LOOP-FROM-SCRATCH.md) | **The agent loop** | tools, file editing, shell, errors, a log — the heart of the course |
| [07](en/course_local_models/07-SANDBOX-SECURITY-MONITORING.md) | Sandbox | bwrap, limits, network, prompt injection, audit, monitoring |
| [08](en/course_local_models/08-OPTIMIZATION-OFFLINE.md) | Speed | prompt cache, speculative decoding, quantization, multiple cards |
| [09](en/course_local_models/09-TOOL-LANDSCAPE.md) | Tool catalogue | vLLM, Docling, promptfoo and others — assessed for this hardware |
| [10](en/course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md) | Hybrid | the privacy boundary, when to use a cloud model, offline-first |

### Course 2 — [agentic applications](en/course_agentic_apps/00-INDEX.md) (`en/course_agentic_apps/`, Polish: [`pl/kurs_aplikacje_agentowe/`](pl/kurs_aplikacje_agentowe/00-INDEKS.md))

Course 1 teaches **how a model works**. Course 2 teaches **how to build a system around it that you can trust**.
You build one growing system and run on it three personal agents that work for weeks,
wake up on their own, remember, are measured and cannot do you harm:
**the Archivist** (local documents, no network), **the Researcher** (network, strict sandbox) and **the Steward**
(calendar and reminders).

| Block | Parts | Topics |
|---|---|---|
| Foundation | 01–03 | agent architectures, the gateway and configuration, **a harness for long-running tasks** |
| Context and memory | 04–06 | the attention budget, bi-temporal memory, identity in files |
| Action | 07–10 | tool ergonomics, **code-mode**, MCP / CLI / A2A, a production sandbox |
| Proactivity | 11–13 | scheduling, channels, a fleet of multiple agents |
| Quality and trust | 14–16 | **evaluation**, observability (OTel), security (OWASP ASI) |
| Production | 17–19 | a hybrid router, releases and maintenance, the capstone project |

⚠️ **Start Course 2 only after part 6 of Course 1** — the whole of it stands on the agent loop that you build there.

### Survey — [agent harnesses for local models](en/agent-harnesses/README.md) (`en/agent-harnesses/`, Polish: [`pl/harnessy-agentowe/`](pl/harnessy-agentowe/README.md))

The courses teach building from scratch. The survey answers the question of **what already exists**: a ranking of the 20 best open
harnesses (out of 72 examined) that turn a local model into an agent — how they differ, what problem each one solves
better than the competition, how to connect it to llama-swap and how to assemble hybrid applications from them: Claude Opus as the planner,
local agents as the executors. As of 11 October 2026.

| File | What is in it |
|---|---|
| [README](en/agent-harnesses/README.md) | the ranking, a technical comparison, choosing by use case, the verdict "build or take off the shelf" |
| [01-PROFILES](en/agent-harnesses/01-PROFILES.md) | 20 profiles with local-model configuration and seven pitfalls common to all of them |
| [02-BUILDING-BLOCKS](en/agent-harnesses/02-BUILDING-BLOCKS.md) | search, price monitoring, financial data, notifications, scheduling, memory, voice, vision |
| [03-ARCHITECTURE](en/agent-harnesses/03-ARCHITECTURE.md) | the planner–executors pattern on 4× R9700, a fully local mode, five ready-made layouts, costs |
| [SOURCES](en/agent-harnesses/SOURCES.md) | sources with the date checked and what I took from them |

### Survey — [AI assistants: the 15 best](en/ai-assistants/README.md) (`en/ai-assistants/`, Polish: [`pl/asystenci-ai/`](pl/asystenci-ai/README.md))

What the best existing AI assistants teach — everyday, professional, ones that carry out tasks autonomously and ones that "live"
in the background: open and closed, their architecture, business models, ability to work offline and lessons for a local assistant
for Polish professionals who cannot send data to the USA. As of 11 October 2026.

| File | What is in it |
|---|---|
| [README](en/ai-assistants/README.md) | a market map, the fifteen in a table, 10 lessons, a selection method |
| [01-PROFILES](en/ai-assistants/01-PROFILES.md) | 15 profiles across nine areas and a "worth knowing" list |
| [02-MARKET](en/ai-assistants/02-MARKET.md) | business models, price lists, numbers, acquisitions, failures, 2026 trends |
| [03-TECHNICAL-PATTERNS](en/ai-assistants/03-TECHNICAL-PATTERNS.md) | technical patterns, an offline matrix, the architecture of a local desktop assistant |
| [04-POLAND-AND-SOVEREIGNTY](en/ai-assistants/04-POLAND-AND-SOVEREIGNTY.md) | GDPR, the AI Act, professional secrecy, competition in Poland and the EU, Polish models, hardware, opportunities |
| [SOURCES](en/ai-assistants/SOURCES.md) | sources with the date checked |

### Practice — [speeding up token generation](en/speeding-up-generation/README.md) (`en/speeding-up-generation/`, Polish: [`pl/przyspieszanie-generowania/`](pl/przyspieszanie-generowania/README.md))

How I took DeepSeek-V4-Flash from 23.5 to about 50 tok/s for one agent on 4× R9700 without touching the model: **speculative decoding** with the model's own
draft head, plus **tensor split** across the four cards — and a procedure for doing the same with any model I download later. Measured, with the failures included.
As of 19 October 2026.

| File | What is in it |
|---|---|
| [README](en/speeding-up-generation/README.md) | the result in one table, the three levers, what is measured and what is not |
| [01-HOW-IT-WORKS](en/speeding-up-generation/01-HOW-IT-WORKS.md) | a lesson: why generation is slow, how speculative decoding and tensor split work, the variants |
| [02-DEEPSEEK-DEPLOYMENT](en/speeding-up-generation/02-DEEPSEEK-DEPLOYMENT.md) | a case study: every step, every measurement, the final configuration, the traps |
| [03-PROCEDURE-NEW-MODEL](en/speeding-up-generation/03-PROCEDURE-NEW-MODEL.md) | a runbook for the next model: decision tree, commands, gates, criteria |
| [04-USING-UI-CLI-OPENCLAW](en/speeding-up-generation/04-USING-UI-CLI-OPENCLAW.md) | talking to the fast model: browser, terminal, agentic apps |
| [tools/](en/speeding-up-generation/tools/README.md) | the scripts: GGUF inspection, draft search, benchmarks, a terminal chat |

### Survey — [local LLM runtimes: from the map to the source code](en/local-llm-runtimes/README.md) (`en/local-llm-runtimes/`, Polish: [`pl/silniki-lokalnych-llm/`](pl/silniki-lokalnych-llm/README.md))

What llama.cpp, Ollama, LM Studio, vLLM, SGLang, MLX and oMLX, ds4, llmman and a dozen other programs for running models on your own hardware are, what they do inside,
what they are for and how they differ — from the market map down to the data structures in the code. Plus one non-technical chapter: how they make money and who is behind them.
Desk research and source-code reading, no benchmarks of my own. As of 19 October 2026. The English text was translated from the Polish original by the local DeepSeek model and checked mechanically.

| File | What is in it |
|---|---|
| [README](en/local-llm-runtimes/README.md) | the course map, ten surprises, how to read it |
| [01-MAP-AND-LAYERS](en/local-llm-runtimes/01-MAP-AND-LAYERS.md) | seven layers from weights file to chat window, project tables, dependency web, timeline |
| [02-HOW-INFERENCE-WORKS](en/local-llm-runtimes/02-HOW-INFERENCE-WORKS.md) | prefill and decoding, KV cache, MoE, batching, parallelism, speculation, sampling, glossary |
| [03-QUANTIZATION-AND-FORMATS](en/local-llm-runtimes/03-QUANTIZATION-AND-FORMATS.md) | what is inside a GGUF file, quantization families, quality tables, analysis of the DeepSeek file |
| [04-LLAMA-CPP-AND-THE-GGML-FAMILY](en/local-llm-runtimes/04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) | ggml, GGUF, `llama-server` internals, multi-GPU split modes, HIP; ik_llama.cpp, llamafile, llama-swap |
| [05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS](en/local-llm-runtimes/05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md) | Ollama, LM Studio, llmman, Jan, LocalAI, Lemonade, Docker Model Runner, RamaLama |
| [06-SERVING-ENGINES-VLLM-SGLANG](en/local-llm-runtimes/06-SERVING-ENGINES-VLLM-SGLANG.md) | vLLM, SGLang, TensorRT-LLM, TGI; status on AMD gfx1201 |
| [07-APPLE-MLX-OMLX-AND-DS4](en/local-llm-runtimes/07-APPLE-MLX-OMLX-AND-DS4.md) | unified memory, MLX, mlx-lm, oMLX, ds4, exo |
| [08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS](en/local-llm-runtimes/08-SPECIALISTS-KTRANSFORMERS-AND-OTHERS.md) | KTransformers, mistral.rs, MLC, NPU stacks |
| [09-COMPARISON-AND-CHOICE](en/local-llm-runtimes/09-COMPARISON-AND-CHOICE.md) | matrix, scenarios, what runs on gfx1201, experiments |
| [10-MONEY-AND-PEOPLE](en/local-llm-runtimes/10-MONEY-AND-PEOPLE.md) | **non-technical:** business models, funding, people, licences, dependency risks |
| [SOURCES](en/local-llm-runtimes/SOURCES.md) | sources, pinned commits, the weakest-verified points |

### Survey — [cheap and free online models for agents](en/cheap-free-models/README.md) (`en/cheap-free-models/`, Polish: [`pl/tanie-i-darmowe-modele/`](pl/tanie-i-darmowe-modele/README.md))

The third leg next to frontier APIs and local models: where to get online inference for little or no money on models at
least as smart as a local DeepSeek-V4-Flash, and how far it can be trusted in an agent loop. The top 20 routes, which
models really clear the bar, and how to wire them into agentic apps. As of 13 October 2026.

| File | What is in it |
|---|---|
| [README](en/cheap-free-models/README.md) | the short answer, the top 20 ranking, scoring, which route for which job |
| [01-PROFILES](en/cheap-free-models/01-PROFILES.md) | 20 profiles: prices, limits, terms, how to call each route |
| [02-MODELS](en/cheap-free-models/02-MODELS.md) | which models are really at least as smart as DeepSeek-V4-Flash, on one index version |
| [03-AGENTIC-USE](en/cheap-free-models/03-AGENTIC-USE.md) | a LiteLLM router config, free-tier quotas, cost math, quality traps, a 15-minute acceptance test |
| [SOURCES](en/cheap-free-models/SOURCES.md) | sources with the date checked |

### Survey — [AI income asymmetries](en/ai-income-asymmetries/README.md) (`en/ai-income-asymmetries/`, Polish: [`pl/asymetrie-zarobkowe-ai/`](pl/asymetrie-zarobkowe-ai/README.md))

Where can an agentic app on a hybrid setup earn money online without founding a company: 22 candidates (bounties,
contests, prediction markets, arbitrage, paid manual work, compute rental and more), each checked for whether manual
work is still paid that agents can now do faster. Legality and tax checked for a Polish resident. As of 14 October 2026.

| File | What is in it |
|---|---|
| [README](en/ai-income-asymmetries/README.md) | the short answer, the top 10, scoring, where to start, rejected candidates |
| [01-OPPORTUNITIES](en/ai-income-asymmetries/01-OPPORTUNITIES.md) | the top 10 opportunities, profile by profile |
| [02-HYBRID-ARCHITECTURE](en/ai-income-asymmetries/02-HYBRID-ARCHITECTURE.md) | one hybrid agent pattern: routing local vs paid, cost math, safety rails |
| [03-RULES-TAX-RISKS](en/ai-income-asymmetries/03-RULES-TAX-RISKS.md) | Polish tax, reporting, gambling and security-work rules, platform terms, operational risks |
| [SOURCES](en/ai-income-asymmetries/SOURCES.md) | sources with the date checked |

### Survey — [AI business asymmetries](en/ai-business-asymmetries/README.md) (`en/ai-business-asymmetries/`, Polish: [`pl/asymetrie-biznesowe-ai/`](pl/asymetrie-biznesowe-ai/README.md))

Where AI adoption is still low enough that a small team with agentic apps and local open models can build a business
before the incumbents catch up: 26 candidates across Poland, the EU and global markets, each argued against from five
angles before scoring. As of 14 October 2026.

| File | What is in it |
|---|---|
| [README](en/ai-business-asymmetries/README.md) | the short answer, the top 15, scoring, the challenge, where to start |
| [01-ADOPTION-GAPS](en/ai-business-asymmetries/01-ADOPTION-GAPS.md) | where AI adoption is still low: Eurostat and GUS data by country, size and sector |
| [02-OPPORTUNITIES](en/ai-business-asymmetries/02-OPPORTUNITIES.md) | the top 15 opportunities, profile by profile |
| [03-LOCAL-FIRST](en/ai-business-asymmetries/03-LOCAL-FIRST.md) | why buyers want local, good-enough open models, hardware tiers, local vs API cost |
| [SOURCES](en/ai-business-asymmetries/SOURCES.md) | sources with the date checked |

### Business track — [pricing a private AI box](en/course_pricing_ai_box/00-INDEX.md) (`en/course_pricing_ai_box/`, Polish: [`pl/kurs_wycena_ai_box/`](pl/kurs_wycena_ai_box/00-INDEKS.md))

A price book for the on-premise AI box for Polish professional offices, where every number has a source: the cost
floor, the value ceiling for a law office, the expert-agent catalogue as the growth engine, four hardware models and
your cash, willingness-to-pay conversations in Polish, and how the price list looks to an investor. With a
standard-library calculator (`floor`, `value`, `cash`, `vw`, `gg`, `nrr`). As of 25 October 2026.

| Part | Topic | What you produce |
|---|---|---|
| [01](en/course_pricing_ai_box/01-PRICING-FOUNDATIONS.md) | Foundations | a pre-registered gut price, three anchors |
| [02](en/course_pricing_ai_box/02-COST-FLOOR.md) | Cost floor | COGS per office, a margin target |
| [03](en/course_pricing_ai_box/03-VALUE-CEILING.md) | Value ceiling | economic value for three offices, the first target customer |
| [04](en/course_pricing_ai_box/04-VALUE-METRIC-AND-PACKAGING.md) | Value metric | the agent catalogue, good/better/best packages |
| [05](en/course_pricing_ai_box/05-HARDWARE-AND-CASH.md) | Hardware and cash | the hardware model and your cash need |
| [06](en/course_pricing_ai_box/06-WILLINGNESS-TO-PAY.md) | Willingness to pay | an interview kit, Van Westendorp, a paid pilot |
| [07](en/course_pricing_ai_box/07-PRICE-BOOK-AND-TERMS.md) | Price book | `price-book-v1.md` with discounts and terms |
| [08](en/course_pricing_ai_box/08-PRICING-FOR-SCALE-AND-INVESTORS.md) | Scale | ARR, NRR and the bootstrapped-or-venture decision |

---

## Getting started

```bash
git clone https://github.com/michal-koniu/llm-education.git
cd llm-education
source rig-env.sh        # sets the paths for the courses, models and llama.cpp
```

Then open [part 1 of Course 1](en/course_local_models/LOCAL-MODELS-FUNDAMENTALS.md). Every lesson begins with
`source rig-env.sh` in the repository directory — the lesson commands assume the repo is at `~/llm-education`;
adjust if yours differs.

**Adapt `rig-env.sh` to your machine:** the paths to the models (`$M`, `$BIELIK`, …), to llama.cpp (`$LB`)
and the visible cards (`HIP_VISIBLE_DEVICES`). It is a template: edit the defaults at the top, or set any of these
variables in your shell before `source rig-env.sh`.

## Where files are created

Everything the courses create is created **inside the repository**, in directories ignored by git:

| Variable | Directory | What goes there |
|---|---|---|
| `$KURS` | `pl/kurs_lokalne_modele/praca/` | scripts, databases, evaluations, grammars from Course 1 |
| `$AGENT` | `pl/kurs_lokalne_modele/praca/agent/` | the agent built from part 6 onwards |
| `$OSA` | `pl/kurs_aplikacje_agentowe/praca/os-agenta/` | the system from Course 2 (with its own git repository) |
| `$VENVS` | `.venvs/` | the Python environments used in the lessons |
| `$NARZEDZIA` | `narzedzia/` | whisper.cpp and piper from part 5 |

(The working directories live under `pl/` — the variables in `rig-env.sh` point there, for both language versions.)

**Deliberate exceptions** — these things are not kept in the project directory:

- **models** (`~/models`) and **llama.cpp** (`~/llama.cpp`) — large, shared with other tools on the machine;
- **systemd units** (`~/.config/systemd/user/`) — systemd reads them only from there; `init.sh` generates them
  with the full project path;
- **secrets** (`~/.config/osa/sekrety.json`, permissions 0600) — secrets are not kept in the repository,
  not even an ignored one;
- **the socket** (`~/.local/run/osa.sock`) — a socket path has a limit of 108 characters;
- **Your data** that the agents work on (`~/dokumenty`, `~/skany`) — these are your files, not products of the course;
- **the business track's working folder** (`~/founder/`) — your price notes and data about real customers are
  private and never go into a public repository.

## Hardware and software

- The courses were written and tested on: Ubuntu 24.04, ROCm, llama.cpp (+ llama-swap), AMD Radeon AI PRO R9700 cards.
- Most exercises require a card with **at least 16 GB of VRAM** (Bielik 11B in Q8, gpt-oss-20b). Parts with multiple
  cards and large models (e.g. 8) — correspondingly more.
- Other cards (NVIDIA, Apple Silicon) will work wherever llama.cpp works — you will change `rig-env.sh`
  and ignore the notes specific to ROCm.
- Python 3.12, `sqlite3`, `bwrap` (the sandbox parts).

## How to read the lessons

- **Pitfalls** are numbered (`P4`, `P29`, …) — these are errors that really occurred on this machine, with the symptom
  and the fix. The course indexes collect them in one place.
- **Experiments** have an empty table for your measurement and my prediction. When they diverge, **your measurement
  wins** — correct the course.
- The numbers in the lessons come from my machine; yours will differ. The direction and order of magnitude are what matter.

## Related repositories

| Repository | What it is |
|---|---|
| [local-llm-perf-bench](https://github.com/michal-koniu/local-llm-perf-bench) | measuring the speed of models in llama.cpp |
| [local-llm-quality-bench](https://github.com/michal-koniu/local-llm-quality-bench) | measuring the quality of models as agents, in Polish and English |
| [local-llm-bench-results](https://github.com/michal-koniu/local-llm-bench-results) | the results of both benchmarks from this machine |
| [radeon-r9700-rocm-notes](https://github.com/michal-koniu/radeon-r9700-rocm-notes) | hardware notes: 4× R9700 + ROCm |

## License

The whole repository is licensed: all content (lessons, surveys, guides - every `*.md`, both languages) under **CC BY 4.0** —
you may copy, modify and use it, also commercially, with attribution to the author. All code (scripts, `rig-env.sh`,
`skeleton/`, `narzedzia/`, `tools/`, snippets in the lessons): **MIT**. Details: [LICENSE.md](LICENSE.md).

Found a mistake, or does your measurement say something different from the lesson? Open an issue — that is exactly why
the lessons have tables for measurements.
