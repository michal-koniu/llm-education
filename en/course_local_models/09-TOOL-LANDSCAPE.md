# Part 9 — The open-source tool landscape

**Level: ⭐⭐⭐** (to be read at any time) · Time: ~3 h of reading + experiments

> **Why this chapter.** Parts 1–8 taught you to build everything from scratch — deliberately,
> so that you understand the mechanisms. **Now you can choose ready-made tools consciously**, because you know
> what they do under the hood and what they hide.
>
> This chapter is a **catalogue with assessments**, not a list of links. For every tool: what it does,
> when to take it, when not to — and **whether it will work on your RDNA4**, because that is the real sieve
> that filters out half of the ecosystem.

---

## ⚠️ Before you start: your hardware is a sieve

You have a **Radeon AI PRO R9700, `gfx1201`, RDNA4, ROCm 7.2.4.** This is a **new
and niche** architecture. A large part of the AI ecosystem assumes NVIDIA/CUDA.

**The three support levels I use to rate every tool:**

| Marking | Meaning |
| :-- | :-- |
| ✅ **works** | you can build it and run it without heroics |
| ⚠️ **with effort** | works after patches / an unofficial image / compiling from source |
| ❌ **not on RDNA4** | requires CUDA or has no gfx1201 support |

⚠️ **This is not a flaw in your hardware choice.** You have 65 GB of VRAM for a fraction of the price
of the NVIDIA equivalent. You pay for it with integration time. **Know that when choosing
a tool.**

---

## Table of contents

| § | Category |
| :-- | :-- |
| [1](#1-inference-engines) | ⭐ **Inference engines** — alternatives to llama.cpp |
| [2](#2-gateways-and-orchestration) | Gateways and model orchestration |
| [3](#3-user-interfaces) | User interfaces |
| [4](#4-enforcing-structure) | Enforcing output structure |
| [5](#5-vector-databases) | Vector databases |
| [6](#6-embeddings-and-reranking) | Embeddings and reranking |
| [7](#7-document-processing-and-ocr) | ⭐ Document processing and OCR |
| [8](#8-speech--stt-and-tts) | Speech — STT and TTS |
| [9](#9-agent-frameworks) | Agent frameworks |
| [10](#10-ready-made-coding-agents) | Ready-made coding agents |
| [11](#11-observability) | Observability |
| [12](#12-evaluation) | ⭐ Evaluation |
| [13](#13-fine-tuning) | Fine-tuning |
| [14](#14-quantization) | Quantization |
| [15](#15-what-to-start-with) | ⭐ Recommendations |

---

## 1. Inference engines

This is the category you asked about directly. `llama.cpp` is your starting point — here is the rest.

### 1.1 Comparison

| Engine | Format | RDNA4 | Strength | Weakness |
| :-- | :-- | :-- | :-- | :-- |
| **llama.cpp** | GGUF | ✅ | ⭐ works everywhere, all quantizations, grammars, speculation | lower throughput with many users |
| **vLLM** | safetensors, AWQ, GPTQ | ⚠️ | ⭐ **~2× throughput**, PagedAttention, continuous batching | heavy, difficult on gfx1201 |
| **SGLang** | safetensors | ⚠️ | RadixAttention (great prefix cache), complex workflows | younger, less documentation |
| **ExLlamaV2 / V3** | EXL2, EXL3 | ❌ | fastest on a single GPU, great quantizations | **CUDA only** |
| **TGI** (HuggingFace) | safetensors | ⚠️ | production-grade, good ecosystem | heavy, Rust + Python |
| **MLC-LLM** | own | ⚠️ | compiles for specific hardware, also runs on phones | exotic build chain |
| **Ollama** | GGUF | ✅ | ⭐ easiest start, model library | **its own llama.cpp** — see the warning |
| **KoboldCpp** | GGUF | ✅ | single file, many samplers, UI included | geared towards creative writing |
| **TabbyAPI** | EXL2 | ❌ | lightweight OpenAI server for ExLlama | CUDA only |
| **Aphrodite** | many | ⚠️ | vLLM fork with a ton of samplers | same as vLLM |

### 1.2 ⭐ vLLM — when it is really worth it

**What it does better than llama.cpp:**

| Mechanism | Gain |
| :-- | :-- |
| **PagedAttention** | KV cache paged like virtual memory → less fragmentation |
| **continuous batching** | new requests join the batch on the fly, they do not wait |
| **prefix caching** | shared prefix between requests (like `--cache-reuse`, but better) |

⭐ **When vLLM wins: MANY CONCURRENT USERS.** For a single agent
llama.cpp is perfectly sufficient and **much simpler**.

⚠️ **The reality on gfx1201** — this is knowledge you already have written down in the project:

| Problem | Workaround |
| :-- | :-- |
| no official gfx1201 support | the `kyuz0/vllm-therock-gfx1201` image with ready patches |
| **TP ≥ 2 deadlocks** | **`NCCL_PROTO=Simple` is mandatory** (RCCL LL has no RDNA4 fixes) |
| **FP8 silently falls back to FP32** | the AITER architecture table skipped gfx1201 — check `arch_info.py` **in the container** |
| **P2P hangs the host with 4 cards** | `NCCL_P2P_DISABLE=1` (trap **P4**) |
| pipeline-parallel unstable | **use TP, not PP** — the opposite of the usual advice |

```bash
# Launch sketch (requires Docker - which you do NOT have, see part 7 §2)
# sudo apt install -y docker.io
# docker run --rm -it --device=/dev/kfd --device=/dev/dri \
#   --group-add video --ipc=host --shm-size 16G \
#   -e NCCL_P2P_DISABLE=1 -e NCCL_PROTO=Simple \
#   -p 8000:8000 kyuz0/vllm-therock-gfx1201 \
#   --model /models/... --tensor-parallel-size 2
```

💡 **Recommendation: leave vLLM for later.** Come back to it when (a) you serve
many clients at once, or (b) llama.cpp turns out to be a bottleneck that you have **measured**, not
merely suspected.

### 1.3 ⛔ Ollama and LM Studio — why not for you

Both are convenient. Both **carry their own built-in engine**.

⚠️ **This wrecks your measurement methodology.** All your discipline records the **exact
llama.cpp commit and build flags** (`GGML_HIP=ON`, `GPU_TARGETS=gfx1201`). A second engine
with an unknown configuration means **the measurement no longer describes what you actually serve.**
On a fresh gfx1201 this is not a theoretical risk.

💡 **That does not mean they are bad.** For someone who wants to chat with a model — Ollama is
great. For someone who is **selling performance numbers to a client** — it is not.

---

## 2. Gateways and orchestration

| Tool | What it does | RDNA4 | Verdict |
| :-- | :-- | :-- | :-- |
| **llama-swap** | switches models behind a single address | ✅ | ⭐ **you have it, use it** |
| **LiteLLM** | one API for 100+ providers (local and cloud) | ✅ | ⭐ **take it for the hybrid** (part 10) |
| **OpenRouter** | cloud gateway | n/a | not for offline |
| **RouteLLM** | learns to route cheap/expensive | ✅ | interesting after part 8 §4 |

### 2.1 LiteLLM — worth attention

```bash
python3 -m venv $VENVS/litellm
$VENVS/litellm/bin/pip install 'litellm[proxy]'

cat > $KURS/litellm.yaml <<'EOF'
model_list:
  - model_name: lokalny-maly
    litellm_params:
      model: openai/gpt-oss-20b
      api_base: http://127.0.0.1:8081/v1
      api_key: nieuzywany
  - model_name: lokalny-duzy
    litellm_params:
      model: openai/qwen3-32b
      api_base: http://127.0.0.1:8082/v1
      api_key: nieuzywany
EOF

$VENVS/litellm/bin/litellm --config $KURS/litellm.yaml --port 4000
```

⭐ **Why this makes sense:** one API for local models **and** Claude (part 10).
Changing the model = changing one string. It also has built-in cost tracking and limits.

---

## 3. User interfaces

| Tool | Description | RDNA4 | Verdict |
| :-- | :-- | :-- | :-- |
| **Open WebUI** | ⭐ the most popular; chat, RAG, multi-user, plugins | ✅ | ⭐ **take it when you want a UI** |
| **LibreChat** | similar, stronger in user management | ✅ | good alternative |
| **AnythingLLM** | geared towards RAG over documents, desktop + server | ✅ | ⭐ good for a **client demo** |
| **Text Generation WebUI** | "oobabooga", many backends, lots of sliders | ⚠️ | for sampling experiments |
| **SillyTavern** | character management, very elaborate prompts | ✅ | not your case |
| **Chatbox / Jan** | lightweight desktop clients | ✅ | when you just want a window |

```bash
# Open WebUI - the simplest way (requires Docker or pip)
python3 -m venv $VENVS/webui
$VENVS/webui/bin/pip install open-webui
OPENAI_API_BASE_URL=http://127.0.0.1:8080/v1 \
  $VENVS/webui/bin/open-webui serve --port 3000
```

💡 **For an accounting product AnythingLLM is worth a look** — it has ready document
upload, "workspace" isolation per client and citations. **Before you take it, understand
that it does the same as your part 4 — only without your control over chunking.**

---

## 4. Enforcing structure

Part 3 did this with GBNF grammars. Alternatives:

| Tool | Approach | RDNA4 | When |
| :-- | :-- | :-- | :-- |
| **GBNF in llama.cpp** | grammar in the engine | ✅ | ⭐ **you have it, it is enough** |
| **XGrammar** | fast grammars, used by vLLM/SGLang | ⚠️ | when you move to vLLM |
| **Outlines** | Python library, regex/JSON/Pydantic | ⚠️ | when you need Pydantic |
| **Guidance** | template language with interleaved generation | ⚠️ | complex workflows |
| **lm-format-enforcer** | token filter, integrates with many backends | ⚠️ | alternative to Outlines |
| **Instructor** | Pydantic validation + retry (does not enforce!) | ✅ | ⚠️ **retry ≠ guarantee** |

⚠️ **A distinction that matters:** Outlines/XGrammar/GBNF **enforce at the sampling
level** — the result is guaranteed. Instructor **tries and repeats** — there is no guarantee.
For a local 20B model this difference is critical (part 3 §2.1).

---

## 5. Vector databases

| Tool | Type | RDNA4 | When |
| :-- | :-- | :-- | :-- |
| **sqlite + Python** (part 4) | file | ✅ | ⭐ **up to 100k chunks — you have it** |
| **sqlite-vec** | sqlite extension | ✅ | ⭐ when the linear scan slows down |
| **LanceDB** | file-based, columnar | ✅ | ⭐ **a good next step** — no server, fast |
| **Qdrant** | server (Rust) | ✅ | when you need filters and scale |
| **Chroma** | server/file (Python) | ✅ | popular, simple, slower |
| **Milvus** | distributed server | ✅ | overkill below millions of vectors |
| **pgvector** | PostgreSQL extension | ✅ | ⭐ when you **already have Postgres** |
| **FAISS** | library | ✅ (CPU) | when you want to control the index yourself |

### 5.1 Growth path

```
part 4 (sqlite + Python)  →  sqlite-vec  →  LanceDB  →  Qdrant
      < 100k chunks          < 1 mln       < 10 mln    above
```

```bash
# sqlite-vec - the smallest jump from part 4
python3 -m venv $VENVS/kurs
$VENVS/kurs/bin/pip install sqlite-vec
```

💡 **Do not jump straight to Qdrant.** Your database from part 4 is enough for tens of
thousands of chunks and **you understand it completely**. Migrate when you have measured that search
takes too long — not before.

---

## 6. Embeddings and reranking

### 6.1 Embedding models

| Model | Dimension | Polish | Notes |
| :-- | --: | :-- | :-- |
| **bge-m3** | 1024 | ⭐ very good | ⭐ **recommended in part 4**; up to 8192 tok |
| multilingual-e5-large | 1024 | good | requires `query:`/`passage:` prefixes |
| jina-embeddings-v3 | 1024 | good | great on long texts |
| Qwen3-Embedding | 1024–4096 | good | new, strong, several sizes |
| nomic-embed-text | 768 | average | open training data |
| **mmlw-roberta** (PL) | 1024 | ⭐ **dedicated Polish** | ⭐ **worth testing** |

⭐ **`mmlw` is a Polish embedding model** from the Wrocław University of Science and Technology (Politechnika Wrocławska). **Measure it
against `bge-m3`** using the "margin" method from part 4 §2.4 — on Polish accounting text
it may win.

### 6.2 Reranking

| Model / tool | Description |
| :-- | :-- |
| **bge-reranker-v2-m3** | ⭐ dedicated cross-encoder reranker, multilingual |
| **jina-reranker-v2** | fast, multilingual |
| LLM as a judge (part 4 §6.2) | works, but **slower** than a dedicated reranker |

💡 **A dedicated reranker is 10–50× faster than an LLM in this role** and usually more accurate.
If the reranking from part 4 is a bottleneck for you — this is the right replacement.

### 6.3 Embedding servers

| Tool | Notes |
| :-- | :-- |
| **llama-server `--embedding`** | ✅ **you have it** — it is enough |
| **Infinity** | fast server for embeddings and rerankers, OpenAI API |
| **TEI** (HuggingFace) | production-grade, ⚠️ limited ROCm support |

---

## 7. Document processing and OCR

⭐ **This is the category that means the most to you** — you work with invoices,
contracts and scans.

| Tool | What it does | RDNA4 | Verdict |
| :-- | :-- | :-- | :-- |
| **Docling** (IBM) | ⭐ PDF/DOCX/PPTX → structured Markdown; **understands tables and layout** | ✅ | ⭐⭐ **start with this** |
| **Marker** | PDF → Markdown, very good quality | ⚠️ (torch) | great for long documents |
| **Surya** | layout detection, OCR, tables; **supports Polish** | ⚠️ (torch) | strong OCR |
| **olmOCR** | OCR based on a VL model | ⚠️ | new, good results |
| **PaddleOCR** | classic OCR, many languages | ⚠️ | mature, fast |
| **Tesseract** | classic OCR | ✅ | ⭐ **easy start**, `apt install tesseract-ocr-pol` |
| **unstructured** | universal parser for many formats | ✅ | good for mixed sources |
| **PyMuPDF** (`fitz`) | fast text extraction from PDF | ✅ | ⭐ when the PDF **has** a text layer |
| **pdfplumber** | extracting tables from PDF | ✅ | ⭐ good for tables |
| **VL model** (part 5) | reads the image directly | ✅ | when the layout is unusual |

### 7.1 ⭐ Strategy for invoices — the cost hierarchy

```
1. Does the PDF have a text layer?     → PyMuPDF           (milliseconds, free)
2. PDF is a scan, typical layout?      → Docling/Tesseract (seconds)
3. Unusual layout, hand-held photo?    → VL model (part 5) (tens of seconds)
```

⚠️ **Do not send every invoice to a VL model.** It is the most expensive option. **Check
first whether the PDF already has text** — half of the invoices you receive by email do.

```bash
# Quick test: does the PDF have a text layer?
python3 -m venv $VENVS/dok
$VENVS/dok/bin/pip install pymupdf docling pdfplumber

$VENVS/dok/bin/python - <<'PYEOF'
import sys, fitz   # PyMuPDF
p = "/path/to/invoice.pdf"
try:
    d = fitz.open(p)
    tekst = "".join(page.get_text() for page in d)
    if len(tekst.strip()) > 100:
        print(f"✅ PDF HAS text ({len(tekst)} characters) — use PyMuPDF, not a VL model")
        print(tekst[:400])
    else:
        print("⚠️ PDF is a SCAN — OCR or a VL model is needed")
except Exception as e:
    print("error:", e)
PYEOF
```

```bash
# Docling: PDF -> Markdown with structure
sudo apt install -y tesseract-ocr tesseract-ocr-pol
$VENVS/dok/bin/python -c "
from docling.document_converter import DocumentConverter
r = DocumentConverter().convert('/path/invoice.pdf')
print(r.document.export_to_markdown()[:1500])
"
```

⭐ **Docling keeps tables as Markdown tables.** For invoices with line items this is a
huge difference compared with flat OCR — the model gets structure, not chaff.

---

## 8. Speech — STT and TTS

### 8.1 Speech recognition (STT)

| Tool | Description | RDNA4 | Verdict |
| :-- | :-- | :-- | :-- |
| **whisper.cpp** | ⭐ C++, GGUF, HIP | ✅ | ⭐ **part 5, you have it** |
| **faster-whisper** | CTranslate2, faster | ⚠️ (CUDA-centric) | great on NVIDIA |
| **WhisperX** | Whisper + alignment + **diarization** | ⚠️ (torch) | ⭐ when you need "who spoke" |
| **Whisper.cpp streaming** | live transcription | ✅ | for continuous dictation |
| **Vosk** | lightweight, offline, works on weak hardware | ✅ | when you want minimalism |

### 8.2 Speech synthesis (TTS)

| Tool | Polish | RDNA4 | Verdict |
| :-- | :-- | :-- | :-- |
| **Piper** | ⭐ **several PL voices** | ✅ (CPU) | ⭐⭐ **part 5, recommended** |
| **Kokoro** | ⚠️ limited | ✅ | very good EN quality, small |
| **XTTS v2** (Coqui) | ✅ + **voice cloning** | ⚠️ (torch) | when you want your own voice |
| **F5-TTS** | ⚠️ | ⚠️ | great quality, cloning |
| **espeak-ng** | ✅ | ✅ | ⛔ sounds robotic — emergency only |
| **`llama-tts`** | ⚠️ foreign accent | ✅ | you have it, but P34 |

⭐ **For Polish: Piper.** It runs on the CPU, does not compete for VRAM, has natural voices.
**XTTS v2 when you need a specific voice** (e.g. cloning your own).

---

## 9. Agent frameworks

⚠️ **Read this after parts 6–7, not before.** Then you will see that each of them does
what your `agent.py` does — and you will judge whether its abstractions help you or get in the way.

| Framework | Philosophy | Verdict |
| :-- | :-- | :-- |
| **LangChain / LangGraph** | everything for everyone; LangGraph = a state graph | ⚠️ **heavy**; LangGraph on its own is sensible |
| **LlamaIndex** | geared towards RAG and indexing | ⭐ good if RAG is the core |
| **smolagents** (HF) | ⭐ **minimalist**, the agent writes code | ⭐ **closest to your philosophy** |
| **Pydantic AI** | typing and validation as the foundation | ⭐ good for structured outputs |
| **CrewAI** | teams of agents with roles | nice demo, hard to debug |
| **AutoGen** (MS) | multi-agent conversations | research-oriented, heavy |
| **Haystack** | production pipelines | solid, less fashionable |
| **DSPy** | ⭐ **optimizes prompts automatically** | ⭐ interesting, a different category |

### 9.1 What is really worth taking from these frameworks

| Element | From | Why |
| :-- | :-- | :-- |
| **agent state machine** | LangGraph | Your `while` loop is simple; with branching a graph is more readable |
| **automatic prompt optimization** | DSPy | ⭐ **genuinely new value** — it tunes the prompt to your metrics |
| document parsers | LlamaIndex | ready loading of dozens of formats |
| **nothing else** | — | you have the rest in parts 3–8 |

⭐ **DSPy is the only item on this list that does something you have not written yourself.**
Instead of fixing the prompt by hand, you define a metric (you have it — part 3 §6) and DSPy
searches for a better prompt. **This is a natural continuation of your evaluation suite.**

---

## 10. Ready-made coding agents

| Tool | Description | Local model? |
| :-- | :-- | :-- |
| **Aider** | ⭐ terminal coding agent, strong git integration | ✅ **yes** |
| **OpenHands** (formerly OpenDevin) | agent in a container, browser + terminal | ✅ yes |
| **Continue** | VS Code / JetBrains plugin | ✅ yes |
| **Cline** | VS Code plugin, agentic | ✅ yes |
| **goose** (Block) | CLI agent with extensions | ✅ yes |

```bash
# Aider with your local model
python3 -m venv $VENVS/aider
$VENVS/aider/bin/pip install aider-install && $VENVS/aider/bin/aider-install

cd ~/project
OPENAI_API_BASE=http://127.0.0.1:8081/v1 OPENAI_API_KEY=x \
  $VENVS/aider/bin/aider --model openai/gpt-oss-20b
```

⭐ **Run Aider and compare it with your own `agent.py`.** See how it solved the same
problems: file editing, context, approvals. **This is the best design lesson
in this chapter** — and it will be understandable only because you wrote your own first.

---

## 11. Observability

| Tool | What it gives | Verdict |
| :-- | :-- | :-- |
| **Langfuse** | ⭐ traces, costs, evaluation; **self-hosted** | ⭐ **take it when the log from part 6 stops being enough** |
| **Phoenix** (Arize) | traces + evaluation, local | good alternative |
| **OpenLLMetry** | OpenTelemetry for LLMs | when you already have an OTel stack |
| **netdata** | system and GPU metrics | ⭐ **you have it** |
| own log (part 6) | full control | ⭐ **enough to start with** |

💡 **Langfuse makes sense when you have many users or want to compare prompt versions
on charts.** For a single agent your JSONL is more convenient — `grep` works
right away.

---

## 12. Evaluation

⭐ **The most underrated category in the whole ecosystem.**

| Tool | Description | Verdict |
| :-- | :-- | :-- |
| **promptfoo** | ⭐ declarative prompt tests in YAML, side-by-side comparisons | ⭐⭐ **take this** |
| **Ragas** | RAG-specific metrics (faithfulness, relevance) | ⭐ fits part 4 |
| **DeepEval** | LLM tests in pytest style | good if you like pytest |
| **lm-evaluation-harness** | standard academic benchmarks | for comparing models |
| **own harness** (part 3 §6) | full control, your domain | ⭐ **the foundation** |

```bash
# promptfoo - compare three models on the same suite
npm install -g promptfoo

cat > $KURS/promptfooconfig.yaml <<'EOF'
providers:
  - id: openai:chat:gpt-oss-20b
    config: { apiBaseUrl: http://127.0.0.1:8081/v1, apiKey: x }
  - id: openai:chat:qwen3-32b
    config: { apiBaseUrl: http://127.0.0.1:8082/v1, apiKey: x }

prompts:
  - "Wyciągnij z faktury numer, datę i kwotę brutto jako JSON:\n{{tekst}}"

tests:
  - vars:
      tekst: "FV/2025/01/0001 z 2025-01-10. Netto 1000 zł, VAT 23%, brutto 1230 zł."
    assert:
      - type: is-json
      - type: javascript
        value: JSON.parse(output).brutto === 1230
  - vars:
      tekst: "Rachunek A/12/2025 z 2025-06-30, zwolniony z VAT, 500,00 zł."
    assert:
      - type: is-json
      - type: contains
        value: "A/12/2025"
EOF

cd $KURS && promptfoo eval && promptfoo view
```

⭐ **`promptfoo view` gives a comparison table in the browser.** It is the same as your
harness from part 3, but with a UI and convenient comparison of many models at once. **Worth it —
especially when you will be showing results to a client.**

---

## 13. Fine-tuning

| Tool | Description | RDNA4 | Verdict |
| :-- | :-- | :-- | :-- |
| **llama-finetune** | ⭐ you have it, LoRA in llama.cpp | ✅ | for learning the mechanism (part 8 §6) |
| **Unsloth** | 2× faster, 70% less memory | ⚠️ (CUDA-first, ROCm experimental) | best on NVIDIA |
| **Axolotl** | YAML configuration, many methods | ⚠️ ROCm possible | mature |
| **torchtune** (PyTorch) | official, clean | ⚠️ ROCm via PyTorch-ROCm | ⭐ **the surest path on ROCm** |
| **LLaMA-Factory** | UI + CLI, many methods | ⚠️ | convenient |
| **PEFT** (HF) | base LoRA/QLoRA library | ⚠️ | foundation of the others |

⚠️ **The reality of fine-tuning on RDNA4:** PyTorch-ROCm supports gfx1201, but the ecosystem
(bitsandbytes, flash-attention, xformers) **is uneven**. Expect effort.

💡 **Before you start fine-tuning, re-read part 8 §6.1.** In 80% of cases
the answer is RAG (part 4) or a grammar (part 3), not LoRA.

---

## 14. Quantization

| Tool | Formats | RDNA4 | Verdict |
| :-- | :-- | :-- | :-- |
| **llama-quantize** | GGUF: Q2–Q8, K, IQ | ✅ | ⭐ **you have it** (part 8 §5) |
| **llama-imatrix** | importance matrix | ✅ | ⭐ **you have it** |
| **AutoAWQ** | AWQ (4-bit, for vLLM) | ⚠️ | when you move to vLLM |
| **GPTQModel** | GPTQ | ⚠️ | same as above |
| **ExLlamaV3 (EXL3)** | best quantizations | ❌ CUDA | unavailable |
| **llm-compressor** | quantization for vLLM | ⚠️ | vLLM ecosystem |

💡 **Stay with GGUF.** It is best supported on ROCm, you have all the tools for it
and your whole measurement methodology is built on it.

---

## 15. What to start with

### 15.1 Three things to take right away

| # | Tool | Why now |
| --: | :-- | :-- |
| **1** | **Docling** | invoices and contracts → structured Markdown; **the biggest gain for your domain** |
| **2** | **promptfoo** | comparing models and prompts with a UI; extends part 3 §6 |
| **3** | **Piper** | Polish TTS (part 5 §5.2) — if you do not have it yet |

### 15.2 To test second

| Tool | What for |
| :-- | :-- |
| **Aider** | see how others solved your part 6 |
| **mmlw** (PL embeddings) | may beat `bge-m3` on Polish |
| **bge-reranker-v2-m3** | faster reranking than LLM-as-a-judge |
| **LanceDB** | the next step after sqlite from part 4 |
| **DSPy** | automatic prompt optimization for your metrics |

### 15.3 Deliberately postponing

| Tool | Why not now |
| :-- | :-- |
| **vLLM** | a lot of effort on gfx1201; come back when you have measured that llama.cpp is a bottleneck |
| **LangChain** | heavy abstractions over what you can already write |
| **Ollama / LM Studio** | they wreck the measurement methodology |
| **Qdrant / Milvus** | overkill below a million vectors |
| **Unsloth** | CUDA-first |

### 15.4 ⭐ A rule worth remembering

> **Take a tool when you can describe exactly what it will not do for you.**

After parts 1–8 you can do that for every item in this catalogue. **This is the real
outcome of this course** — not that you wrote your own vector database, but that **you know what
you are buying** when you take someone else's.

---

## Exercises

1. **Docling on a real invoice.** Take an invoice PDF, run it through Docling and compare
   with what the VL model from part 5 produced. Measure time and accuracy. **Which one won and on what type of
   document?**
2. **promptfoo on the suite from part 3.** Move `faktury.jsonl` into a promptfoo configuration
   and compare three models in the UI.
3. **mmlw vs bge-m3.** Measure the "margin" using the method from part 4 §2.4 on Polish accounting
   text. Which one separates better?
4. **Aider vs your agent.** The same coding task on the same model. Compare the number
   of turns, the quality and **what Aider does differently**. Write down three things you will
   borrow from it.
5. **Define your stack.** Write one table in your project notes: layer → chosen tool →
   why → what you rejected. **This is the architecture document of your product.**

---

**Next part: `10-HYBRID-LOCAL-PLUS-CLAUDE.md`** — a short chapter: when and how to
add the Claude API to the local stack without losing control over privacy.
