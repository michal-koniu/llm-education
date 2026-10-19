# Speeding Up Token Generation — Speculative Decoding and Tensor Split Across 4 GPUs

**As of October 19, 2026.** How I sped up DeepSeek-V4-Flash from **23.5 to ~50 tok/s** (single agent) without changing the
model or its weights — and how to do the same with any other model I download in the future. This directory is
simultaneously a **lesson** (how it works under the hood) and a **guide** (exactly what I did, what to tune, how to revert).

> ⚠️ **What is measured here, and what is not.** Everything below was measured on a single machine (4× Radeon AI PRO R9700,
> ROCm, llama.cpp). I measured **speed** precisely. I did **not** measure **quality after the change** — whether the model got dumber
> (section [Quality](#quality-did-the-model-get-dumber)). Tensor split is labelled experimental by llama.cpp itself.

---

## Result in a Single Table

DeepSeek-V4-Flash-0731 (284 billion parameters, MoE, 13 billion active), UD-IQ3_XXS quantization, 4 GPUs. Single agent, average across 4 task
types (translation, tool call, code, prose) × 2 temperatures:

| Configuration | tok/s (average) | tool call (JSON) |
|---|---|---|
| start of day: old llama.cpp, layer split, no draft | **23.5** | 23.4 |
| + speculative decoding (DSpark, 3 tokens) | 35.2 | 43 |
| new llama.cpp, layer split, with draft | 37.9 | 48–50 |
| new llama.cpp, **tensor split**, with draft — **deployed** | **49.2** | **54–62** |

And with multiple agents running at once (deployed configuration, 2 slots):

| Concurrent agents | each | total |
|---|---|---|
| 1 | 49.7 tok/s | 46 |
| 2 | 34.5 | **63** |
| 4 (2 slots, rest waiting in queue) | 33 | 60 |

Cost: **prompt reading (prefill) is slower** — ~700 instead of ~960 tok/s — and **2 slots of 98,304 tokens** of
context remain instead of 4 of 131,072. Details and rationale: [02-DEEPSEEK-DEPLOYMENT.md](02-DEEPSEEK-DEPLOYMENT.md).

## The Three Levers That Made It Happen

1. **Speculative decoding** (+50 %): a small "guesser" proposes 3 tokens, the large model verifies them in a single pass.
   The guesser is DeepSeek's official **DSpark** head, hidden in the 0731 checkpoint; it had to be converted to GGUF.
2. **Tensor split** (`--split-mode tensor`, +30 % on top): all 4 GPUs compute every token in parallel, instead of
   sequentially as in a pipeline. I did it on an **updated llama.cpp** (499 commits ahead): the new code has explicit support for DeepSeek V4 compressed attention states in this mode. I did not attempt tensor mode on the old version.
3. **Memory tuning**: the draft costs ~4 GB per GPU, so I reduced the micro-batch (`--ubatch-size` 512) and the number of slots.

## What's in This Directory

| File | Purpose |
|---|---|
| [01-HOW-IT-WORKS.md](01-HOW-IT-WORKS.md) | **Lesson.** Why generation is slow, how speculative decoding works, how its variants differ, what tensor split is |
| [02-DEEPSEEK-DEPLOYMENT.md](02-DEEPSEEK-DEPLOYMENT.md) | **Deployment log.** What I did step by step, all measurements, final configuration, what to tune, pitfalls, how to revert |
| [03-PROCEDURE-NEW-MODEL.md](03-PROCEDURE-NEW-MODEL.md) | **Guide** for future models: decision tree, commands, gates, criteria |
| [04-USING-UI-CLI-OPENCLAW.md](04-USING-UI-CLI-OPENCLAW.md) | How to talk to the fast model: browser, terminal, agent applications (OpenClaw) |
| [05-REFERENCE-LLAMA-CPP-SPECULATIVE](https://github.com/ggml-org/llama.cpp/blob/0ce8cd11416c8840498e6701bcbe39ad4b858c2b/docs/speculative.md) | llama.cpp documentation on speculative decoding **translated into Polish by local DeepSeek** (with a description of how I verified it) |
| [tools/](tools/README.md) | Scripts: GGUF inspection, draft search, benchmarks, terminal chat, VRAM measurement loop |

## Quality: did the model get dumber?

**I did not measure it.** What I know and what I don't:

- **Speculative decoding by design does not change the results** — the large model approves every token, so the distribution of answers is the same.
- **Tensor split changes the order of floating-point summation**, so at temperature 0 the answers are no longer identical character for character to the old ones
  (0 of 4 identical; with layer split and a draft: 2 of 4). The answers I read were correct: a translation, code, a tool call with valid JSON.
- **A practical test, not a benchmark:** the deployed configuration translated 24 KB of documentation EN→PL and about 60 KB of my own documents PL→EN. Structure, code, numbers and URLs
  came out intact; there were factual slips (for example a mistranslated heading) and translated fragments of code that it was told to leave alone — described in the Polish
  [05](../../pl/przyspieszanie-generowania/05-ODNIESIENIE-LLAMA-CPP-SPECULATIVE.md). The model does not fall apart, but this is not a quality measurement.
- **The quality benchmark** (the "hard" suite: 20 tasks in Polish and English, k=3, 120 samples; this model scored PL 92 / EN 93 on 10 October) I did start, but **I stopped it after 11 samples**:
  the full run takes several hours, and 11 samples support no conclusion, so I do not publish them.

**Before you build agents on this**, repeat that measurement and compare it with the 10 October report:
`python3 -m qbench run --model deepseek-v4-flash-0731 --suite hard --k 3` (several hours; do not change the `llama-swap` configuration meanwhile — it unloads the model).
If the score drops, point clients at `deepseek-v4-flash-0731-layerspec` (layer split + draft) or `-nospec`.

## Related repository parts

- Course 1, part 8 "Speed" — [prompt cache, speculative decoding, quantization, multiple GPUs](../course_local_models/08-OPTIMIZATION-OFFLINE.md): theory; here is the practice on a specific model.
- [Harness overview](../agent-harnesses/README.md) and [assistant overview](../ai-assistants/README.md) — OpenClaw and company, which will use this model.
