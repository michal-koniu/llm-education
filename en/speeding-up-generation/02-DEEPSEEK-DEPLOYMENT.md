# 02 · Deployment on DeepSeek-V4-Flash-0731 — log, measurements, configuration

A record of what I did on October 19, 2026, **including the paths that did not work**. Theory: [01-HOW-IT-WORKS.md](01-HOW-IT-WORKS.md).
Hardware: 4× Radeon AI PRO R9700 (32 GB each), ROCm 7.2, llama.cpp + `llama-swap` (serving with model switching on demand).

> **Measurement method** (scripts in [tools/](tools/README.md)): `bench_spec.py` sends 4 types of tasks (PL→EN translation, tool call,
> code, free-form prose) × temperature 0 and 1.0, 300 tokens each, and reads the time **from the server's own counters** (`timings.predicted_per_second`).
> The model "thinks" before answering — those tokens are counted too, because that is the real usage picture. One repetition ⇒ noise ±2 tok/s; I do not interpret smaller differences.

## 1. Starting point and diagnosis (read-only)

- State: llama.cpp `680a036` (Sep 28, 2026), DeepSeek-V4-Flash-0731 UD-IQ3_XXS (Unsloth), layer split, 4 slots × 131,072 context,
  **23.5 tok/s** per single agent (stable to within 0.3).
- Quick check: does this llama.cpp support speculative decoding? Yes — `--spec-type draft-mtp, draft-eagle3, draft-dflash, draft-dspark, ngram-*`.
- Does the GGUF have an MTP head? Headers: 43 blocks, **zero `nextn`/MTP tensors** (`gguf-inspect.py` script). The loader silently disables MTP when tensors are missing.
- Does the original checkpoint have anything for speculation? Yes: DSpark (`mtp.*` tensors, files 46–48 of 48, ~11 GB), the llama.cpp converter has a ready-made `--dspark` option.

## 2. Draft: DSpark → GGUF conversion (without stopping the model)

```bash
# separate Python environment for the converter (does not touch the system one); torch ≥ 2.7 is required (float8_e8m0fnu type)
python3 -m venv ~/spec-dspark/venv && . ~/spec-dspark/venv/bin/activate
pip install -r ~/llama.cpp/requirements/requirements-convert_hf_to_gguf.txt huggingface_hub safetensors
pip install -e ~/llama.cpp/gguf-py

# "target model": just config + tokenizer (so the draft has the same vocabulary)
mkdir -p ~/spec-dspark/target-hf   # config.json, tokenizer.json, tokenizer_config.json, generation_config.json, model.safetensors.index.json

# --remote: download only the 3 needed files (11 GB), not the whole checkpoint (167 GB)
export HF_HOME=~/spec-dspark/hf-cache
python ~/llama.cpp/convert_hf_to_gguf.py deepseek-ai/DeepSeek-V4-Flash-0731 --remote --dspark \
   --target-model-dir ~/spec-dspark/target-hf --outtype bf16 --outfile ~/spec-dspark/DeepSeek-V4-Flash-0731-DSpark.gguf
```

Result: **10.9 GB, 81 tensors**, `dflash` architecture, block 5, target layers 41–43 (1-based numbering). The warning "Transformers does not recognize deepseek_v4"
is harmless (the converter then reads `config.json`). Source: `deepseek-ai/DeepSeek-V4-Flash-0731`, revision `7872f01b1d1fe23eabc4c98b48bffcef5a386062`.
I keep the file next to the model: `~/models/DeepSeek-V4-Flash-0731-GGUF/DSpark/`, with a SHA256 sum.

## 3. Measurements — round 1: old llama.cpp, layer split

Single stream (`--parallel 1`, 131,072), average tok/s across all tasks:

| Variant | Average | Conclusion |
|---|---|---|
| no draft | **23.5** | baseline |
| DSpark n=5, p-min 0 | 33.2 | **prose slower than without draft** (19–22) |
| n=5, p-min 0.5 | 34.8 | confidence threshold saves prose |
| n=5, p-min 0.75 | 32.1 | too cautious |
| **n=3, p-min 0** | **36.1** | best average and best translation (34) |
| n=3, p-min 0.5 | 34.3 | no gain over p-min 0 |
| n=4 / n=2 (p-min 0) | 32.4 / 34.7 | n=2 the most even (no task below 28) |
| n=5, p-min 0.5 **+ `ngram-mod`** | 34.4 | n-grams added nothing (plain text does not repeat) |

`n` = `--spec-draft-n-max` (how many tokens the draft proposes), `p-min` = `--spec-draft-p-min` (head confidence threshold). I chose n=3, p-min 0.

**Multiple agents at once** (4 slots, temp. 0.2; `bench_conc.py`):

| Agents | no draft: each / total | with draft: each / total |
|---|---|---|
| 1 | 23.1 / 22 | 33.3 / 32 (+44 %) |
| 2 | 19.3 / 38 | 24.6 / 46 (+21 %) |
| 4 | 13.9 / 50.7 | 13.9 / 50.0 (±0) |

With 4 agents the GPU is already saturated by *batching* (4 tokens per step from 4 streams is essentially the same "speculation" done as a batch) — the draft adds nothing and takes nothing away.

**Draft cost:** prefill (6.2k prompt tokens) dropped from **~960 to ~490 tok/s** — the draft also has to read the prompt. Example: new 10,000 prompt tokens + 100
response tokens: without draft 10.4 + 4.3 ≈ **14.7 s**, with draft 20 + 3 ≈ **23 s** (slower); 2,000 + 300: 15.0 s vs **12.6 s** (faster).
Rule: **the more you generate relative to what you read, the more the draft pays off.**

**Memory:** the draft eats ~4 GB per card (2.7 GB weights + buffers), and card 0 also handles the desktop. It had **0.15 GB free** left at `--ubatch-size 1024`.
Levers, most effective first: `--ubatch-size 1024→512` (+0.7 GB on card 0, +1.2–2.0 GB on the others; cost: prefill −8 %), fewer slots/context, draft KV in q8_0 (negligible).
Shifting layers via `--tensor-split` in layer mode did not help: a layer is ~2.4 GB, so moving one overflows the neighbor.

## 4. Measurements — Round 2: new llama.cpp + tensor split

I built **separately** (old installation untouched) llama.cpp `0ce8cd1` from Oct 19, 2026 with the same HIP flags (thanks to `ccache` it took ~2 min):

```bash
git init ~/llama.cpp-0ce8cd1 && cd ~/llama.cpp-0ce8cd1
git remote add origin https://github.com/ggml-org/llama.cpp
git fetch --depth 1 origin 0ce8cd11416c8840498e6701bcbe39ad4b858c2b && git checkout FETCH_HEAD   # GitHub requires the full SHA
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DGGML_HIP=ON -DGPU_TARGETS=gfx1201 \
      -DGGML_HIP_GRAPHS=ON -DGGML_HIP_NO_VMM=ON -DCMAKE_HIP_COMPILER=/opt/rocm-7.2.4/lib/llvm/bin/clang++ -DGGML_CCACHE=ON
nice cmake --build build -j14 --target llama-server llama-bench llama-cli
```

2×2 matrix (1 slot, 131,072, `bench_spec.py`, average tok/s):

| | without draft | with draft (n=3) |
|---|---|---|
| layer split | 25.2 | 37.9 |
| **tensor split** | 29.1 | **46.2** |

Relative to the same mode without draft, the draft gives 1.5× (layers) and 1.6× (tensor); relative to the baseline of 25.2, both mechanisms together give 1.8×. Further, with the "production" configuration (`--ubatch-size 512`, equal split, n=3):

| Shape | tok/s | free VRAM on cards 0 / 1–3 | notes |
|---|---|---|---|
| 1 slot × 131k (u1024) | 46.2 | 0.35 / 1.5 | baseline |
| 2 slots × 131k | **49.6** | 0.37 / 1.17 | too little headroom on card 0 |
| **2 slots × 98k** | **49.2** | **0.73 / 1.68** | **selected** |
| 4 slots × 65k | 44.6 | 0.16 / 1.0 | slower and too tight |
| 4 slots × 131k | — | — | **out of memory** at load (`cudaMalloc failed: out of memory`) |

Selected configuration, per-task results (temp. 0 / 1.0): translation 51.9 / 43.9 · tool call 62.0 / 54.0 · code 58.5 / 50.9 · prose 37.8 / 34.6;
acceptance 0.70/0.59 · 0.95/0.80 · 0.82/0.73 · 0.40/0.36.

### Pitfalls of tensor mode (I measured each one)

1. **Uneven `--tensor-split` (`0.85,1,1,1`) hangs loading** — the server stays silent after the message that `--fit` is not implemented for tensor mode; `llama-swap` reports error 500 after 300 s.
   I diagnosed this by running `llama-server` directly with one change at a time: equal split + `ubatch 512` loads in 108 s and works; uneven split + `ubatch 1024` hangs.
2. **4 slots × 131,072 → out of memory** on card 0: allocation of ~2.75 GB failed (KV in tensor mode is unquantized, which increases demand). Hence 2 slots.
3. **Loading takes ~108 s** (instead of ~35 s in layer mode). After 10 min of inactivity `llama-swap` unloads the model (`ttl: 600`), so the first request waits ~2 min.
   If that's a problem, raise `ttl` in the config (at the cost of VRAM occupied while the model is unused).
4. The log shows `internal AllReduce init failed (n_devices != 2?); falling back to meta-backend butterfly` — with 4 cards the generic summation path works.

## 5. Gate before deployment

The `gate-test.py` script adds a temporary entry to `llama-swap`, measures, and compares with the model without draft:

| Test | Result |
|---|---|
| free VRAM after load / **after use** | 1.08 / 1.7 GB → **0.82** / 1.43 GB (card 0 / others; after real use drops by ~0.3 GB) |
| prefill (6.2k tokens) | **694–735 tok/s** (layers+draft: 490; without draft: ~960) |
| 1 agent | 49.7 tok/s |
| 2 agents | 34.5 each, **63 total** |
| 4 requests on 2 slots | 33 average, **60 total** |
| identity with model without draft (temp. 0) | **0 of 4** identical — divergence already in the first "thinking" tokens; final answers correct in substance |

That last row is why the speed measurement is **not** evidence of quality — and I did not measure the quality itself: see the "Quality" section in [README](README.md).
In layer mode with draft, 2 of 4 answers were character-identical, and the rest diverged on token "ties" (e.g., `*three*` vs `three`).
Tensor split changes the order of floating-point summation, so divergences are more frequent. I don't know whether this has any impact on quality — I did not finish a quality benchmark after the change.

## 6. Final Configuration

`~/.config/llama-swap/config.yaml`, entry `deepseek-v4-flash-0731` (aliases `deepseek`, `deepseek-v4`… unchanged — clients don't fix anything):

```yaml
    cmd: |
      ~/llama.cpp-0ce8cd1/build/bin/llama-server --port ${PORT} --jinja --agent -fa on
      -m  ~/models/DeepSeek-V4-Flash-0731-GGUF/UD-IQ3_XXS/DeepSeek-V4-Flash-0731-UD-IQ3_XXS-00001-of-00004.gguf
      -md ~/models/DeepSeek-V4-Flash-0731-GGUF/DSpark/DeepSeek-V4-Flash-0731-DSpark.gguf
      --spec-type draft-dspark --spec-draft-n-max 3 --spec-draft-p-min 0
      --split-mode tensor -ctk f16 -ctv f16
      -ngl 999 --ctx-size 196608 --load-mode dio
      --parallel 2 --ubatch-size 512
      --temp 1.0 --top-p 1.0 --top-k 0 --min-p 0
```

| Flag | What it does | Why this value |
|---|---|---|
| `-md FILE` | draft file | for `draft-dspark` this is a GGUF with the `dflash` architecture |
| `--spec-type draft-dspark` | selects the mechanism | see [01, §3](01-HOW-IT-WORKS.md); types can be combined with commas |
| `--spec-draft-n-max 3` | how many tokens the draft proposes per step (limit = block size = 5) | best average in round 1; **I did not re-tune n in tensor mode** |
| `--spec-draft-p-min 0` | head confidence threshold; blocks are truncated when predicted acceptance < p | 0 = disabled |
| `--split-mode tensor -ctk f16 -ctv f16` | tensor split; KV must be unquantized | see [01, §5](01-HOW-IT-WORKS.md) |
| `--ctx-size 196608 --parallel 2` | 2 slots × 98,304 | that's what fits with memory headroom |
| `--ubatch-size 512` | prefill micro-batch | **main memory lever**; prefill ~−8% vs. 1024 |
| `--load-mode dio` | bypasses `mmap` (ROCm error with large models) | unchanged from before |

Alongside these remain: `deepseek-v4-flash-0731-nospec` (old layout without draft, `ubatch 1024`, 4 slots) — for tasks with huge prompts and short answers, and
`deepseek-v4-flash-0731-layerspec` (old llama.cpp, layer split + draft, 4 slots) — emergency fallback. Copy of the pre-change configuration: `config.yaml.bak-20261019-przed-tensor`.

## 7. Manual Tuning

1. Change **one** thing in `config.yaml` (`llama-swap` will reload the config itself and free the loaded model).
2. `python3 bench_spec.py deepseek` (≈3 min; `BENCH_REPS=2` for less noise); compare average tok/s and `accept`.

| I want… | Change | Effect / pitfall |
|---|---|---|
| faster on tool calls and code | `--spec-draft-n-max 4` or `5` | more tokens per step at ~0.9 acceptance; **loses on prose** |
| never slower than without draft | `--spec-draft-n-max 2` | most even result |
| more free VRAM | lower `--ctx-size`, `--ubatch-size 256` | ubatch has the biggest effect; cost: prefill |
| faster prefill | `--ubatch-size 1024` | card 0 is left with <0.5 GB — risk of running out of memory |
| more slots | **not with this model on these cards** | 4 slots don't fit in tensor mode |
| disable draft | model `…-nospec` | |

**Live draft effectiveness view:** `curl -sN localhost:8080/logs/stream/upstream | grep "draft acceptance"` — average the `mean len`;
at `n=3` the draft pays off when `mean len > 2.05` ([01, §2](01-HOW-IT-WORKS.md)).
In the client set `temperature` 0–0.3 for tool/JSON calls: the draft guesses greedily, so at temp. 1.0 acceptance is lower (in my case 0.95 → 0.80 on tool calls).

## 8. Limitations

- **Prefill ~25% slower** than without a draft in tensor mode (700 vs 960) — for "read-heavy, write-light" workloads use `…-nospec`.
- **2 slots × 98,304** instead of 4 × 131,072. A third parallel agent waits in the queue.
- **Free VRAM on card 0: 0.82 GB** after real usage. Memory is reserved statically at startup, but do not add anything to this card.
- **"Empty" responses with small `max_tokens`:** the model first "thinks" (`reasoning_content`) and that consumes the limit — this is not a draft bug.
- **Experimental mode:** upstream explicitly recommends validating quality before deployment.
- Upstream documentation (DSpark section) still says "only Qwen3 backbones supported" — **it is outdated**: the DeepSeek-V4 DSpark converter and loader work (this deployment).

## 9. What's next (not tested)

1. **Tuning `n` in tensor mode** (step cost constants differ from layer mode).
2. **RCCL** (`-DGGML_HIP_RCCL=ON`) and **P2P** (`GGML_CUDA_P2P=1`) — would speed up inter-card reduction. Upstream warns that RCCL does not always help, and P2P can break results
   on some boards (IOMMU) — after enabling, output correctness must be verified.
3. **Other drafts** found by `find-drafts.sh`: EAGLE-3 for V4-Flash-0731, DFlash.
4. **Better quantization of the target model** (higher acceptance), if VRAM allows.

## 10. How to revert

```bash
# wróć do poprzedniego układu (stary llama.cpp, warstwy + draft): w kliencie użyj modelu deepseek-v4-flash-0731-layerspec
# albo bez draftu: deepseek-v4-flash-0731-nospec
# pełne cofnięcie: cp ~/.config/llama-swap/config.yaml.bak-20261019-przed-tensor ~/.config/llama-swap/config.yaml
```
