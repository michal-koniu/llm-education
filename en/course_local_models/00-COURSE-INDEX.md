# Course: from a model to your own agent — index

**Created: 22 September 2026.** For Michał.

> **Purpose of the whole thing.** After working through this course you can **build from scratch
> your own agent in the OpenClaw / Claude Code class** — a loop that reads files, writes code,
> runs commands, sees images, listens and speaks, remembers context and **works offline on your
> own hardware** — and you understand every layer underneath it.
>
> Not "you can use a framework". You understand why a framework does what it does, and you can
> write it yourself. **Only then do you consciously choose off-the-shelf tools.**

---

## The path

```
  PART 1 ──► you talk to the model, you understand the stack
     │        tokens/weights/runtime/server, llama-cli, llama-server, curl
     ▼
  PART 2 ──► you FEEL the model
     │        tokenizer, logits, sampling, KV-cache, embeddings
     ▼
  PART 3 ──► you FORCE the model to obey
     │        chat template, GBNF grammars, determinism, evaluation
     ▼
  PART 4 ──► you give the model MEMORY
     │        embeddings, vector database, chunking, citations, compaction
     ▼
  PART 5 ──► you give it SENSES
     │        vision, Whisper (hearing), Piper (speech) — plus a hardware list
     ▼
  PART 6 ──► you build the AGENT LOOP          ◄── this is where "Your OpenClaw" is born
     │        tools, file editing, shell, errors, subagents, journal
     ▼
  PART 7 ──► you lock it in a CAGE
     │        bwrap, limits, network, prompt injection, audit, monitoring
     ▼
  PART 8 ──► you make it FAST
     │        prompt cache, speculative decoding, quantization, LoRA, 4 cards
     ▼
  PART 9 ──► you get to know the ECOSYSTEM
     │        alternative engines, OCR, databases, frameworks — rated for RDNA4
     ▼
  PART 10 ─► optional: a HYBRID with the Claude API
              routing, privacy boundary, offline-first
```

⚠️ **The order is not decoration.** Part 6 cannot be understood without part 3 (without
grammars a local model will not call a tool reliably). Part 8 cannot be understood without
part 2 (without the KV-cache you do not know what you are optimizing). **Do not skip ahead —
except for part 9, which you can read at any time.**

---

## Files

| # | File | Level | What you will learn | Time |
| :-- | :-- | :-- | :-- | :-- |
| 1 | `LOCAL-MODELS-FUNDAMENTALS.md` | ⭐ | ✅ **you have it** — the stack, downloading, `llama-cli`, `llama-server`, `llama-swap`, first tools | — |
| 2 | `02-MODEL-INTERNALS.md` | ⭐⭐ | tokenizer, logits, **sampling**, **KV-cache**, embeddings, perplexity | ~4 h |
| 3 | `03-CONTROL-AND-RELIABILITY.md` | ⭐⭐⭐ | raw chat template, ⭐ **GBNF grammars**, JSON Schema, determinism, **evaluation harness** | ~5 h |
| 4 | `04-MEMORY-RAG-AND-CONTEXT.md` | ⭐⭐⭐⭐ | embeddings, **vector database from scratch**, chunking, BM25, hybrid, citations, compaction | ~6 h |
| 5 | `05-MULTIMODALITY.md` | ⭐⭐⭐⭐ | **vision** (`llama-mtmd`), **Whisper**, **Piper**, voice loop + ⭐ **hardware shopping list** | ~6 h |
| 6 | `06-AGENT-LOOP-FROM-SCRATCH.md` | ⭐⭐⭐⭐ | ⭐⭐ **agent loop**, tool protocol, `read`/`edit`/`bash`, guard, subagents, journal | ~8 h |
| 7 | `07-SANDBOX-SECURITY-MONITORING.md` | ⭐⭐⭐⭐ | `bwrap`, `systemd-run`, network control, ⭐ **prompt injection**, audit, monitoring | ~5 h |
| 8 | `08-OPTIMIZATION-OFFLINE.md` | ⭐⭐⭐⭐⭐ | prompt cache, ⭐ **speculative decoding**, routing, custom quantization, LoRA, 4 cards | ~7 h |
| 9 | `09-TOOL-LANDSCAPE.md` | ⭐⭐⭐ | ⭐ **tool catalogue** rated for RDNA4: engines, OCR, databases, frameworks, evaluation | ~3 h |
| 10 | `10-HYBRID-LOCAL-PLUS-CLAUDE.md` | ⭐⭐⭐ | privacy boundary, hybrid router, costs, **offline-first** | ~3 h |

**Total: ~47 hours of hands-on-keyboard work.** This is not a course to be read.

---

## Conventions in all files

**The llama.cpp binaries are not in `PATH`.** Run this once per terminal session:

```bash
cd ~/Desktop/github_repos/llm-education   # the repository directory (yours may differ)
source rig-env.sh
```

Create this file once:

```bash
cat > $LLMEDU/rig-env.sh <<'EOF'
# Binaries
export LB=~/llama.cpp/build/bin
export WB=$NARZEDZIA/whisper.cpp/build/bin          # after part 5

# Models
export M=~/models
export BIELIK=$M/bielik-11b/Bielik-11B-v3.0-Instruct.Q8_0.gguf
export OSS20=$M/gpt-oss-20b/gpt-oss-20b-MXFP4.gguf
export QWEN32=$M/qwen3-32b/Qwen_Qwen3-32B-Q4_K_M.gguf
export QWEN80=$M/qwen3-next-80b/Q4_1/Qwen3-Next-80B-A3B-Instruct-Q4_1-00001-of-00002.gguf
export DRAFT=$M/gpt-oss-120b/eagle3-gpt-oss-120b-Q8_0.gguf
export EMB=$M/embed/bge-m3-f16.gguf        # after part 4
export VL=$M/vl/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf          # after part 5
export VLMM=$M/vl/mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf    # after part 5
export WMODEL=$NARZEDZIA/whisper.cpp/models/ggml-large-v3-turbo.bin  # after part 5

# P12/P32: the iGPU is GPU[2] — exclude it
export HIP_VISIBLE_DEVICES=0,1

# P4: P2P hangs the host with 4 cards
export NCCL_P2P_DISABLE=1
export NCCL_PROTO=Simple
EOF

source $LLMEDU/rig-env.sh
$LB/llama-cli --version    # → 0.4.1-dev (build 1, commit 987498f)
```

### Models I use in the examples

| Shorthand | Size | Role in the course |
| :-- | --: | :-- |
| `$BIELIK` | 11.9 GB | Polish, Q8 — language exercises |
| `$OSS20` | 12.1 GB | ⭐ **main agent model** — fast |
| `$QWEN32` | 19.8 GB | smarter, dense — the large one in the router |
| `$QWEN80` | 49.7 GB | MoE — experiments with `-cmoe` |
| `$DRAFT` | 849 MB | ⭐ **draft model** — speculative decoding (part 8) |

---

## Rules I follow throughout the course

1. **No frameworks until you have written it yourself.** You will meet frameworks in part 9
   and you will know what they hide.
2. **Pure Python, no `numpy` and no `torch`.** A dot product written as a loop teaches
   more than `np.dot()`. Where a library is needed, I say so openly.
3. **Every command has an explanation of what it does and what output to expect.**
4. **Every chapter ends with an exercise that actually produces something.**
5. **Do not optimize without measuring.** Every lever in part 8 has a number before and after.
6. **Pitfalls (`P…`) are numbered jointly with `TECHNIKA.md`.** Hardware: P1–P18.
   **Software, from this course: P20–P52.**

---

## Register of software pitfalls

| ID | Pitfall | Part |
| :-- | :-- | :-- |
| P20 | Counting tokens with another model's tokenizer | 2 |
| P21 | `repeat_penalty > 1.0` breaks JSON generation | 2 |
| P22 | Context is VRAM: weights + KV-cache together | 2 |
| P23 | Context overflow can be **silent** | 2 |
| P24 | A generative model used as an embedding model — weak | 2 |
| P25 | Not every model has a `system` role | 3 |
| P26 | A grammar with no exit loops the generation | 3 |
| P27 | A grammar costs 10–30% tok/s | 3 |
| P28 | One sampling profile for the whole agent | 3 |
| P29 | A chunk without metadata — poorly retrieved | 4 |
| P30 | Vectors are useless for identifiers | 4 |
| P31 | Compaction loses exact numbers | 4 |
| P32 | The iGPU as `GPU[2]` — models land on 2 GB | 5 |
| P33 | `mmproj` incompatible with the model | 5 |
| P34 | OuteTTS speaks Polish poorly | 5 |
| P35 | TTS without number normalization | 5 |
| P36 | Whisper hallucinates on silence and noise | 5 |
| P37 | The model forgets to call `odpowiedz` | 6 |
| P38 | No freshness check — the agent eats the human's changes | 6 |
| P39 | A command allowlist is **not** a sandbox | 6 |
| P40 | A single observation fills the whole context window | 6 |
| P41 | Delegation has a fixed cost | 6 |
| P42 | `--bind` instead of `--ro-bind` on a system directory | 7 |
| P43 | Mounting the home directory ends the sandbox | 7 |
| P44 | No `--new-session` — injection into the terminal | 7 |
| P45 | `HTTP_PROXY` is a convention, not enforcement | 7 |
| P46 | A changing system prompt kills the prompt cache | 8 |
| P47 | The draft model eats VRAM and may slow things down | 8 |
| P48 | Routing between servers invalidates the cache | 8 |
| P49 | PPL on calibration text is artificially good | 8 |
| P50 | `-np` splits the context, it does not multiply throughput | 8 |
| P51 | A regex filter lets through what you did not anticipate | 10 |
| P52 | Silent dependence on the cloud | 10 |

---

## Where things live

| File | Role |
| :-- | :-- |
| `HANDOFF.md` | **project state** — what is done, what is next |
| `TECHNIKA.md` | **procedures on this machine** — inventory, hardware pitfalls P1–P18 |
| `KARTY-3-I-4-PLAN-PODLACZENIA.md` | expansion to 4 cards |
| **course `00`–`10`** | **how it works and how to build an agent on it** |
| `BIZNES.md` | thesis, market, product |

**Directories that will appear during the course:**

```
$KURS/       measurement tools, RAG, evaluation sets
$AGENT/      ⭐ your agent loop, sandbox, audit, journals
$NARZEDZIA/whisper.cpp/  STT (part 5)
$NARZEDZIA/piper/      TTS (part 5)
~/models/     models: embed/, vl/, tts/, wlasne/
```

---

## Before you start — check the workstation

```bash
# 1. Cards visible? (expect 2x R9700 + the iGPU as GPU[2])
rocm-smi --showid

# 2. Binaries working?
source $LLMEDU/rig-env.sh && $LB/llama-cli --version

# 3. Models in place? (expect 7 files)
find ~/models -name '*.gguf' | wc -l

# 4. Disk space? (expect ~1.5 T)
df -h /home | tail -1
```

⚠️ **Pitfall P12/P32 — the iGPU is also a ROCm device.** `rocm-smi` shows three
devices: `GPU[0]`, `GPU[1]` are the R9700 cards (34.2 GB each), `GPU[2]` is the **integrated
graphics with 2 GB**. Small models can land there and run 50× slower.
**`HIP_VISIBLE_DEVICES=0,1` is in `rig-env.sh` precisely for this reason.**

⚠️ **After adding cards 3 and 4 the numbering will change again (P13).** Remap it with
`amd-smi list` and update `rig-env.sh`.

---

**Start: `02-MODEL-INTERNALS.md`.**

---

## After this course: course 2

**`course_agentic_apps/00-INDEX.md`** — ⭐ **agentic applications on local models.**
Nineteen parts, ~102 h. Course 1 teaches **how a model works**. Course 2 teaches
**how to build a system around it that can be trusted**:

```
a harness across many context windows · bi-temporal memory · code-mode
production sandbox · proactivity · a fleet of three agents
evaluation and traces · OWASP ASI01–ASI10 · releases and runbook
```

It builds **one growing system** `$OSA/` with three personal agents.
Every part has an **experiment with an empty table for your measurement**. Pitfalls **P60–P139**.

⚠️ **Do not start course 2 before part 6 of course 1** — the whole of course 2 stands on the
agent loop you build there.
