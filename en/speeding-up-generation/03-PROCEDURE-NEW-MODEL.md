# 03 · Procedure: speeding up a new model (speculative decoding + tensor split)

Instructions for every model I download in the future. Theory: [01-HOW-IT-WORKS.md](01-HOW-IT-WORKS.md) — **read §1–§2 once**, and the procedure becomes obvious;
worked example: [02-DEEPSEEK-DEPLOYMENT.md](02-DEEPSEEK-DEPLOYMENT.md). Tools: [tools/](tools/README.md) (verified on DeepSeek-V4-Flash 19 X 2026).

**Guiding principle:** speculative decoding **does not change quality** (the large model approves every token), so the only risk is **time** (prefill, VRAM, complexity), not correctness. That is why the procedure ends with *measurement and a decision*, not faith.

---

## Step 0 · Is it even worth it? (2 minutes)

Speculation speeds up **generation**, not prompt reading (prefill can actually be slower — with DeepSeek ~2×). Worth it when:

| Your task | Decision |
|---|---|
| agent: tool calls, JSON, code, short responses relative to context | **YES** — biggest gain here (DeepSeek: up to 2×) |
| translation, conversation, long responses | **YES** (DeepSeek: +40–45 %) |
| free-form/creative text | be careful — gain ~0 to +25 % |
| summarizing large documents (lots of reading, little writing) | **NO** — leave the model without a draft |
| 4+ parallel agents on one model | **gain ≈ 0** (GPU already saturated by batching) — check `bench_conc.py` |

**Dense** models (e.g. 32B) should gain *more* than MoE (verifying a few tokens costs almost as much as one there); **MoE** — less (a few tokens activate more experts). This follows from the mechanics, **not** from measurement: I have not measured dense models with this method.

---

## Step 0.5 · Is your llama.cpp new enough?

Speculative decoding and tensor split evolve week to week (for me: 499 commits of difference in 3 weeks). **Before you start**, check:

```bash
cd ~/llama.cpp && git fetch origin && git rev-list --count HEAD..origin/master      # how many commits behind you are
./build/bin/llama-server --help | grep -E "spec-type|split-mode"                      # what your version supports
```

Build the new llama.cpp **in a separate directory**, without overwriting the working one (with a full-SHA pin; details and commands: [02, section 4](02-DEEPSEEK-DEPLOYMENT.md)).
`llama-swap` entries can point to any binary, so old and new run side by side, and you switch back by changing one path.

---

## Step 1 · Measure the baseline

Add the model to `llama-swap` normally (as before), then:

```bash
cd tools
python3 bench_spec.py MODEL_NAME_FROM_CONFIG results-baseline.json      # ~3 min
```

Record the **average tok/s** (the `ALL` row) — that is your 100%. (For DeepSeek: 23.5; the result is very stable, noise <0.3.)
For measurements use the configuration with `--parallel 1` and the same `--ctx-size` as after the change — otherwise you are comparing apples to oranges.

> 🚦 **Gate:** you have a "no draft" number from the same configuration in which you will test the draft.

---

## Step 2 · Determine what options this model has

Go from the cheapest option to the most expensive. **Stop at the first one that works.**

### 2A · Does the GGUF itself have a built-in MTP/NextN head? (cheapest: zero downloads)

```bash
~/spec-dspark/venv/bin/python tools/gguf-inspect.py /path/model-00001-of-0000N.gguf
```

- You see `nextn_predict_layers`/`nextn.*` tensors → **YES**. The entry in `llama-swap` gets only: `--spec-type draft-mtp` (without `-md`; llama.cpp creates the MTP context on the model itself). Go to Step 4.
- You see `>>> BRAK glowicy…` → 2B.

> Note: not every model whose architecture *in code* supports MTP has these tensors in your GGUF. Many public quantizations **cut out** the head (DeepSeek-V4-Flash from Unsloth — cut out; verified). Always check the file, not the architecture.

### 2B · Did the model author include the head in the original checkpoint?

```bash
# on HF: config.json of the base model
curl -sL https://huggingface.co/ORG/MODEL/raw/main/config.json | grep -iE "nextn|mtp|dspark|speculat"
# and keys in the weight index
curl -sL https://huggingface.co/ORG/MODEL/raw/main/model.safetensors.index.json | python3 -c "import sys,json; k=json.load(sys.stdin)['weight_map']; print(sorted({x.split('.')[0]+'.'+x.split('.')[1] for x in k if x.startswith('mtp')}))"
```

`num_nextn_predict_layers > 0` or `mtp.*` keys ⇒ the head **is in the checkpoint**, just not in your GGUF ⇒ **convert it** (Step 3, the "head from checkpoint" path).

### 2C · Has anyone trained a draft for this model?

```bash
tools/find-drafts.sh MODEL-NAME      # e.g. Qwen3-30B-A3B, gpt-oss-120b
```

Searches HF for: `mtp`, `eagle3`, `dflash`, `dspark`, `speculator`, `draft`. This is a list of **candidates** — before downloading, check the card: for which **exact version** of the model (e.g., DeepSeek *0731* ≠ *preview*; acceptance drops when the version doesn't match), the same **tokenizer**, and whether a ready GGUF exists.

### 2D · Is there a small model with the same tokenizer?

Model families have "younger siblings" (e.g., Qwen3-0.6B/1.7B for Qwen3-32B). Regular draft (`draft-simple`):

```
-md maly-model-Q8_0.gguf --spec-type draft-simple --spec-draft-n-max 8
```

Requirements: **identical vocabulary (vocab)** as the large model; preferably the same generation/training data. A small model is slower at guessing than specialized heads, but it works everywhere. For dense models this is often the best option.

### 2E · None of the above → guessing from text history (zero weights, zero VRAM)

```
--spec-type ngram-mod --spec-ngram-mod-n-match 24 --spec-ngram-mod-n-min 48 --spec-ngram-mod-n-max 64
```

Works **only** when the text repeats: code rewriting/editing, summarization with quotes, an agent repeating file contents. For regular translation/conversation ≈ 0 (with DeepSeek, adding `ngram-mod` to DSpark did nothing). llama.cpp documentation warns: *"MoEs need long drafts"*.

> 🚦 **Gate:** you know which path you're taking (MTP in file / head conversion / ready draft / small model / n-grams).

---

## Step 3 · Get the draft file (if the path requires it)

The converter environment is already there: `~/spec-dspark/venv` (torch CPU 2.11, numpy, gguf). If it ever disappears: `narzedzia/convert-draft-from-hf.sh` contains the commands (it's a **template with DeepSeek's DSpark** — swap the repo name and the flag).

| What you convert | Command (all from `~/llama.cpp`) | Notes |
|---|---|---|
| **MTP head** from checkpoint | `python convert_hf_to_gguf.py ORG/MODEL --remote --mtp --outtype bf16 --outfile mtp-MODEL.gguf` | `--mtp` = export of the head alone as a separate draft (`-md`); works only for architectures with `supports_mtp_export` |
| **EAGLE-3** | `python convert_hf_to_gguf.py ORG/EAGLE3-MODEL --target-model-dir ORG/MODEL --outtype bf16 --outfile eagle3.gguf` | `--target-model-dir` = local directory with `config.json`+tokenizer of the **target** model |
| **DFlash / DSpark** | as above (for DeepSeek-V4: add `--dspark`) | DSpark: only architectures supported by the converter; check `grep -n dspark ~/llama.cpp/conversion/*.py` |
| **small model (`draft-simple`)** | download a ready GGUF from HF | check the same tokenizer |

Practical tips:

- **`--remote`** downloads only those safetensors files that contain the needed tensors (DeepSeek: 3 of 48 files = 11 GB instead of 167 GB). Set `HF_HOME=~/spec-dspark/hf-cache` so the cache doesn't spill into `~/.cache`.
- The warning *"Transformers does not recognize…"* for new architectures is harmless — the converter reads `config.json` then.
- After conversion **check the file**: `gguf-inspect.py plik.gguf` — the draft has architecture `dflash`/`eagle3`/or `…` with `nextn`; save `sha256sum` next to the file.
- Keep the draft **next to the model**: `~/models/<MODEL>-GGUF/<TYP-DRAFTU>/`.
- Draft in bf16/Q8, **don't quantize it harder** (it's small, and acceptance quality depends on it — DSpark authors' recommendation in llama.cpp).

> 🚦 **Gate:** the draft file exists, `gguf-inspect.py` recognizes it, you have `sha256`.

---

## Step 4 · VRAM budget — before you load anything

The draft costs **weights + its own context + buffers**. For DeepSeek: weights 10.9 GB (≈2.7 GB/card) **plus** approx. 1.3 GB/card of buffers → about 4 GB total on each of the 4 cards ([02, section 3](02-DEEPSEEK-DEPLOYMENT.md)).

**Rule:** after loading, **each card has ≥ 1 GB free** (the card with the desktop — ≥ 0.8 GB). Memory is reserved statically at startup, so what you measure after startup stays.

Measurement without risk: add a *temporary* entry in `config.yaml` (separate name), call it with a single request, read:

```bash
rocm-smi --showmeminfo vram | grep -E "Total Used|Total Memory"
```

A ready-made loop "add entries → load → measure → restore config" is `narzedzia/vram-try.py` (template: edit paths and the `V` dictionary at the top).

**Levers when memory is tight** (from most effective, measured on DeepSeek):

| # | Lever | Effect (DeepSeek) | Cost |
|---|---|---|---|
| 1 | `--ubatch-size` 1024 → **512** | **+0.7 GB** on card 0, +1.3 GB on the others | prefill −8 % |
| 2 | smaller `--parallel`/`--ctx-size` | ~0.1–0.4 GB/card on 131k context (DeepSeek's KV is cheap — with other models KV can be **dominant**) | fewer agents/context |
| 3 | `--spec-draft-type-k/v q8_0` | ~0 to +0.1 GB | negligible |
| 4 | draft on selected cards: `--spec-draft-device`, `-ngld` | depends | draft may land on a slower link |
| 5 | `--tensor-split` | **carefully** — a DeepSeek layer is ~2.4 GB, one shifted layer overflows the neighbor; `--fit` (default `on`) may then silently change the layout | measure tok/s precisely after the change |

> 🚦 **Gate:** the model with draft loads, each card has ≥ 1 GB free (0.8 for the desktop card), tok/s did not drop relative to Step 1 on an "empty" request.

---

## Step 5 · Entry in `llama-swap`

Always **two entries**: the speculative one (with the aliases you already have) and a `-nospec` twin (without draft, without aliases). This way the app selects by model name, and you have a fallback and a baseline.

```yaml
  "NAME":
    cmd: |
      ${server}
      -m  /path/model.gguf
      -md /path/draft.gguf                        # SKIP for draft-mtp on the model itself and for n-grams
      --spec-type draft-dspark                      # draft-mtp | draft-eagle3 | draft-dflash | draft-dspark | draft-simple | ngram-mod
      --spec-draft-n-max 3 --spec-draft-p-min 0     # see Step 7
      --spec-draft-type-k q8_0 --spec-draft-type-v q8_0
      -ngl 999 --split-mode layer --tensor-split … --ctx-size … --load-mode dio
      --parallel … --ubatch-size 512
    env: ["HIP_VISIBLE_DEVICES=0,1,2,3"]
    ttl: 600
    aliases: ["…old aliases…"]

  "NAME-nospec":      # copy of the old entry without --spec-*, without -md, without aliases
    …
```

Before editing: `cp ~/.config/llama-swap/config.yaml ~/.config/llama-swap/config.yaml.bak-$(date +%Y%m%d)-before-spec`.
Remember: saving `config.yaml` **reloads llama-swap and unloads the loaded model** (it returns on the next request, ~40 s) — don't do this during an important task.

## Step 6 · Measurement (three tests, ~15 min total)

```bash
cd tools

# (a) one stream, 4 task types × temp. 0 and 1.0, with acceptance       ~3 min
BENCH_REPS=2 python3 bench_spec.py NAME results-spec.json
# (b) 1, 2 and 4 agents at once (total and per-stream throughput)       ~2 min
python3 bench_conc.py NAME results-conc-spec.json   &&   python3 bench_conc.py NAME-nospec results-conc-nospec.json
# (c) gate before deployment: prefill, 1/2/4 agents, free VRAM after use, compatibility with the no-draft model — TEMPLATE: paths and arguments at the top of the file
python3 gate-test.py
```

How to read (thresholds from [01, §2](01-HOW-IT-WORKS.md)):

- `accept` and `tok/s` per task. **A task where spec < nospec** ⇒ route that traffic type to `-nospec`.
- `bench_conc`: did the gain at 1–2 agents disappear at 4? (For DeepSeek: yes.)
- Noise of a single repetition ≈ ±2 tok/s → decisions on differences < 2 are random.
- Remember that the model's **"thinking" tokens are also counted** (DeepSeek, Qwen3 in thinking mode) — this is usually the correct picture of your usage.

> 🚦 **Gate:** you have 3 sets of numbers: (a) tok/s on tasks, (b) scaling with the number of agents, (c) prefill and memory.

---

## Step 7 · Tuning (one change at a time)

Start from the initial values, then search for a better **one variable at a time** using `bench_spec.py`.

| Parameter | Start | Direction | Rule |
|---|---|---|---|
| `--spec-draft-n-max` (how many tokens it proposes) | MoE: **3** (measured); dense model: **5–8** (initial value from llama.cpp docs — I did not measure a dense model) | up when `accept` > 0.85; down when prose/translation has low `mean len` | draft pays off when `mean len > (c₀ + c₁·n)/c₀`, where c₀ = cost of a regular step, c₁ ≈ cost of one extra token in a step (DeepSeek: 43 ms and 15 ms) |
| `--spec-draft-p-min` (confidence threshold; only drafts with a confidence head, e.g. DSpark) | 0 | 0.5 if `n` is large and prose degrades | too high (≥0.75) cuts off too much |
| `--spec-type a,b` (combinations) | single | add `ngram-mod` **only** for tasks with repetitions | does nothing for regular text |
| `--spec-draft-n-min` | 0 | usually leave as is | |
| `--ubatch-size` | from Step 4 | | changes memory and prefill |

**Your own step-cost formula** (you can do it in 5 minutes for a new model): measure tok/s for `n=3` and `n=5` on a high-acceptance task (JSON). From these two points: `c₁ ≈ (T₅ − T₃)/2`, `c₀ ≈ T₃ − 3·c₁`, where `T = mean_len / tok_per_s` is the step time. Then search for the `n` that maximizes `mean_len(n)/(c₀ + c₁·n)` on your traffic.

---

## Step 7b · Tensor split (optional, big gain, more pitfalls)

With 2+ cards, try `--split-mode tensor` — all cards compute every token simultaneously ([01, §5](01-HOW-IT-WORKS.md)). For me: 37.9 → 46–50 tok/s with draft.

**Prerequisites** (otherwise an error at startup): `-fa on`, `-ctk f16 -ctv f16` (no KV quantization), architecture on the supported list (`docs/multi-gpu.md`).
**No auto-fitting** (`--fit`) — you size memory manually.

Procedure (measure `bench_spec.py` and `rocm-smi --showmeminfo vram` at each step):

1. Without draft, **equal split** (do not pass `--tensor-split`), `--parallel 1`, context as in step 1. Record tok/s and **load time** (for me 108 s vs 35 s).
2. Add the draft. Check free VRAM: target ≥ 1 GB per card (≥ 0.8 GB on a card with a desktop).
3. Not enough memory → reduce in this order: `--ubatch-size` (1024→512), `--ctx-size`, `--parallel`. **Do not** use an uneven `--tensor-split` (hangs loading) or KV quantization (forbidden).
4. Only now tune `--spec-draft-n-max`: step-cost constants in tensor mode differ from layer mode.
5. Optional: RCCL (`-DGGML_HIP_RCCL=ON`) and `GGML_CUDA_P2P=1` — **after every change verify output correctness**, because P2P can corrupt it on some boards.

**Quality in tensor mode:** the order of floating-point sums changes, so results at temp. 0 are no longer identical to layer mode (for me 0/4). Comparing texts proves nothing —
**run the quality benchmark** on the same set you used to measure the model before the change ([README](README.md#quality-did-the-model-get-dumber)). A change in the `llama-swap` configuration **unloads the loaded model**, so do not do it during such a run.

---

## Step 8 · Decision (write the criteria down BEFORE measuring)

**Keep spec**, if all of the following hold:

1. average across your typical tasks **≥ +20 %** vs Step 1;
2. **no typical task** is more than 5 % slower than the baseline (otherwise: route to `-nospec`);
3. each card has ≥ 1 GB free (card with desktop ≥ 0.8 GB) **after real usage** (in my case, free VRAM dropped by ~0.3 GB after tests);
4. prefill loss is acceptable for your applications (calculate: `new_prompt_tokens/prefill + response/tok_s` for a typical request, with and without);
5. responses are functionally correct (tool call → correct JSON; translation makes sense);
6. **quality benchmark without regression** relative to the measurement before the change (mandatory in tensor mode).

Otherwise: revert to `config.yaml.bak-…`, and the `-nospec` entry stays.

---

## Step 9 · Document (10 minutes — future you will be grateful)

In the file `SPECULATIVE-DECODING-<model>.md` (pattern: DeepSeek document) write:

1. **What** (spec type, draft source, revision/sha) and **why** this path;
2. **Commands** for conversion and `config.yaml` entries;
3. **Tables**: tok/s per task before/after, tuning, agent scaling, prefill, VRAM;
4. **Limitations** (when to route to `-nospec`);
5. **How to revert**.

And add one line in the comment of the entry in `config.yaml` (so that `config.yaml` explains itself what it does).

---

## Tips for agent applications (summary)

- **Temperature 0–0.3 in the client** for tool/JSON calls: higher acceptance and more stable results. Server-side `--temp 1.0` is only a default value — the client can override it in the request.
- **Route traffic by model name:** "interactive" agent → entry with spec; batch tasks with huge prompts → `-nospec`.
- **Number of parallel agents:** spec gives the most at 1–2. If your application launches 4+ agents at once anyway, the gain is zero — better to save VRAM and keep `-nospec`.
- **Large, repeated prompts** (system prompt, repository context): llama.cpp keeps the prompt cache in the slot — the second and subsequent turns read only the new fragment, so the speculative prefill loss hurts less often than raw numbers suggest.
- **`max_tokens` limit vs. thinking:** "thinking" models consume the limit on `reasoning_content` — with too small a limit you get an empty response (that is not a spec bug).
- **Don't measure only server `tok/s`** — measure the full agent turn time (prefill + generation + tools). Spec shortens only generation.

---

## Cheat sheet: tools

| Tool | Purpose | Example |
|---|---|---|
| `gguf-inspect.py` | whether the GGUF has an MTP head / what the file is | `~/spec-dspark/venv/bin/python gguf-inspect.py model-00001-of-0000N.gguf` |
| `find-drafts.sh` | search for ready drafts on HF | `./find-drafts.sh Qwen3-30B-A3B` |
| `convert-draft-from-hf.sh` | template for converting a draft from an HF checkpoint | see Step 3 |
| `bench_spec.py` | tok/s and acceptance, 1 stream | `BENCH_REPS=2 python3 bench_spec.py NAME out.json` |
| `vram-try.py` | free VRAM on cards for many setting variants (template) | edit `V` at the top |
| `bench_conc.py` | 1/2/4 agents at once | `python3 bench_conc.py NAME out.json` |
| `gate-test.py` | gate: prefill, agents, VRAM after use, consistency with baseline (template) | edit paths at the top |
| `dschat.py` | terminal chat with tok/s counter | `python3 dschat.py "question"` |
| `translate_doc.py`, `verify_translation.py` | local translation of a Markdown document + mechanical verification | see [05](https://github.com/ggml-org/llama.cpp/blob/0ce8cd11416c8840498e6701bcbe39ad4b858c2b/docs/speculative.md) |
| live log | acceptance in real time | `curl -sN localhost:8080/logs/stream/upstream \| grep "draft acceptance"` |
