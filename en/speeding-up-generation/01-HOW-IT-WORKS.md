# 01 · How It Works — Why Generation Is Slow and How to Speed It Up

Lesson. After reading it, you should be able to predict whether a given model will benefit from speculative decoding, and understand
every flag in the subsequent files. The numbers come from my measurements on 4× Radeon AI PRO R9700.

---

## 1. Generation Is Memory-Bound, Not Compute-Bound

A language model generates a response **one token at a time**. To compute a single token, you must go through all layers,
which means **reading from GPU memory all the weights that are active at that step**. With so little work per token
(a vector–matrix multiplication), the GPU spends most of its time **waiting for memory**. In other words: decoding is
**memory-bandwidth-bound** (*memory-bound*).

The math for DeepSeek-V4-Flash:

- 284 billion parameters, but it's a **MoE** (*Mixture of Experts*): 256 experts per layer, 6 active per token.
  So roughly **13 billion** parameters work per token.
- UD-IQ3_XXS quantization is ~3 bits per weight → ~**5 GB to read per token**.
- One R9700 card reads ~640 GB/s → theoretical ceiling ~100+ tok/s. **Measured: 23.5 tok/s.** The difference is eaten by
  inter-card transfers, kernel scheduling, and irregular expert reads.

**The conclusion the whole directory rests on:** since the cost of a step is mainly *reading weights*, checking **several tokens at once
costs barely more than one** — the weights are read once. Prefill (reading the prompt) works exactly this way and is ~40× faster
per token than generation.

### Pitfall: "GPU 100%" Does Not Mean "the Card Is Fully Utilized"

By default, llama.cpp splits the model **by layers** (`--split-mode layer`): card 0 has the first quarter of layers, card 1 the next, etc.
A token passes through the cards **in sequence** (pipeline), so at any given moment **one** card is working and three are waiting. The
"GPU usage 100%" indicator only means the card is busy in its own window — not that it's exhausting its memory bandwidth.
This is the second (after memory) reason for slow generation — and this is where tensor split comes in (§5).

---

## 2. Speculative Decoding

**Analogy.** An assistant writes a draft answer "by feel," the professor (large model) reads the whole draft at once and crosses out from the first mistake.
Reading the draft is cheap, because the professor has to load his knowledge (weights) anyway — he does it **once for the whole draft**, not once per word.

One step:

```
1. Draft (guesser) sees the large model's state and PROPOSES n tokens:      [A] [B] [C]
2. The large model in ONE pass computes what it would choose after:          the last token, A, A+B, A+B+C
3. Comparison from the left:   A ✔   B ✔   C ✘   →  we accept A, B, and in place of C we take the large model's token
4. Result: in one step we got 3 tokens (A, B + correction) instead of 1
```

### Why Quality Is Not Lost

Only a token that **the large model itself would have chosen** at that position is accepted. The draft may be wrong — then we only lose a
little time, not quality. (When sampling with temperature, an equivalent of this rule is used that preserves the model's probability
distribution.) A practical caveat: floating-point computations depend on batch shape, so on *ties* between two nearly equally
probable tokens the result may differ from the old one — without affecting correctness, but "bit-identical" output is not guaranteed.

### Two numbers you need to know how to read

In the server log after each request:

```
draft acceptance = 0.75214 (  88 accepted /  117 generated), mean len =  3.26
```

| Quantity | Meaning |
|---|---|
| `acceptance` | what fraction of **proposed** tokens was accepted (88 of 117) |
| **`mean len`** | **how many tokens come out of one step on average** (including the large model's token). This number determines speed. Without draft = 1.0 |

### Profitability rule (derived from my measurements)

For `n = 3` and `n = 5` draft tokens, the cost of one step is well described by the formula:

```
step time  ≈  43 ms  +  15 ms × n          (n = how many tokens the draft proposes)
tok/s       ≈  mean_len / step time
```

- without draft: 43 ms/token = 23.3 tok/s ✔ (measured 23.5)
- `n=3`: step ≈ 88 ms; `mean len 3.26` → **37 tok/s** (measured ~38 ✔)
- **Profitability threshold:** the draft pays off when `mean len > (43 + 15·n) / 43`. For `n=3` that is **2.05**; for `n=5` — **2.7**.

This explains all the tables in the next file: free-form text (prose) has low acceptance → `mean len` ≈ 2 → the draft gives nothing;
tool calls (JSON) have acceptance ~0.9 → `mean len` ~3.7 → almost 2×.
*(This is an approximation fitted to two points — a rule of thumb for tuning, not a law of physics. Measured before switching to tensor split;
there the constants differ, but the logic is the same.)*

### Why the gain for MoE is smaller than for dense models

Checking 4 tokens activates **more different experts** than one (each token picks its own six out of 256), so the step reads more weights.
That is why a step with a draft costs me ~2× a regular step, not ~1.1×. A dense model (32B) reads the same weights regardless of the number of tokens in the batch —
it gains more.

---

## 3. Variants of speculative decoding (llama.cpp, state as of October 19, 2026)

`--spec-type` accepts one or several types separated by commas:

| Type | Where proposals come from | Requires | When good |
|---|---|---|---|
| `draft-simple` (`-md small.gguf`) | **small model** with the same tokenizer (e.g. 0.6B for 32B) | separate small model | dense models, families with "younger siblings" |
| **`draft-mtp`** | **MTP head** (*Multi-Token Prediction*) — an extra layer built into the model, predicts token n+2 | `nextn.*` tensors in GGUF | when the model has them **and the GGUF didn't cut them out** |
| `draft-eagle3` | small one-layer network reading the model's hidden states | separate EAGLE-3 file for the specific model | when someone trained it for your model |
| `draft-dflash` | small network generating **an entire block of tokens in a single pass** (block diffusion) | separate DFlash file | as above |
| **`draft-dspark`** (mine) | **DFlash + "Markov head"** (dependence on the previous token) **+ confidence head** | separate DSpark file | as above; for DeepSeek-V4 it is provided by DeepSeek itself |
| `ngram-*` (`simple`, `map-k`, `map-k4v`, `mod`, `cache`) | **text history**: if a sequence repeats, it guesses it will continue the same way | nothing (zero weights, zero VRAM) | code rewriting, summarization with quotes |

Full description of the flags in the official documentation: [05-REFERENCE-LLAMA-CPP-SPECULATIVE](https://github.com/ggml-org/llama.cpp/blob/0ce8cd11416c8840498e6701bcbe39ad4b858c2b/docs/speculative.md).

### DSpark — what exactly is inside DeepSeek-V4-Flash-0731

- The official **0731** checkpoint does not have a regular MTP head; it has a **DSpark head** (in the HF repo, these are the `mtp.*` tensors in the last three
  safetensors files, ~11 GB). Model README: *"it comes with a speculative decoding module attached"*.
- Parameters from `config.json`: **5-token block**, reads hidden states from **layers 40, 41, 42** (the last three of 43), "Markov rank" 256,
  there is a confidence head (predicts whether a given block position will be accepted → flag `--spec-draft-p-min`).
- The draft **is not a standalone model**: it reads the hidden states of the large model, and borrows embeddings and the output head from it.
- Public GGUFs (including Unsloth UD-IQ3_XXS, which I use) **strip** these tensors — I checked the headers: 43 blocks, zero `nextn`/MTP tensors.
  Therefore `draft-mtp` on that file would do nothing, and the draft had to be converted from the original checkpoint.

---

## 4. Why the gain is "only" 1.5–2×, not 3×

- **MoE** (§2): verifying several tokens reads more experts.
- **The draft is not free**: it is itself a small MoE with 3 blocks; its run is included in those ~15 ms per token.
- **Target quantization**: the draft was trained at full precision, my target is IQ3_XXS. Hidden states differ slightly → acceptance is lower than in the publications
  (DSpark authors report +60–85% for V4; I averaged +50% with layer split).
- **Prefill cost**: the draft must "read" the entire prompt, because it needs hidden states from every position — prefill drops by ~25–50% (see file 02).

---

## 5. Tensor split (`--split-mode tensor`)

Two ways to distribute one model across multiple cards:

```
LAYER SPLIT (layer, default)                 TENSOR SPLIT (tensor, experimental)
  card 0: layers  0–10*  ─┐                  each layer cut into 4 parts
  card 1: layers 11–21    ├─ token goes      card 0: ¼ of each layer ┐
  card 2: layers 22–32    │  sequentially    card 1: ¼ of each layer ├─ all 4 compute
  card 3: layers 33–42   ─┘  (pipeline)       card 2: ¼ of each layer │  the same token at once,
                                             card 3: ¼ of each layer ┘  results summed (all-reduce)
  only 1 card works at a time                all 4 work — 4× more memory bandwidth
  (*layer numbers approximate)
  little inter-card communication            lots of communication: after each layer cards exchange results
```

- **Gain:** each token reads weights from **all four memories simultaneously**. In my case: without draft 25.2 → 29.1 tok/s (+15%), and **with draft 37.9 → 46–50 tok/s** —
  both mechanisms multiply, because a faster step makes verifying a larger batch relatively cheaper.
- **Cost:** communication. After each layer, results must be summed (*all-reduce*) over PCIe (in my case cards 1 and 3 are on x4). In the log I see
  `internal AllReduce init failed (n_devices != 2?); falling back to meta-backend butterfly` — i.e., with 4 cards the generic, slower path is used;
  the RCCL library or direct inter-card access (P2P) could improve this — **I did not test** (see file 02, "Next steps").
- **Limitations in llama.cpp (October 2026)** — each of them bit me:
  - requires `-fa on` and **unquantized KV** (`-ctk f16 -ctv f16`) — so you cannot save memory with KV quantization;
  - **auto-fitting does not work** (`--fit`): you must choose `--ctx-size`, `--parallel`, `--ubatch-size` yourself;
  - **uneven `--tensor-split` hangs loading** (in my case `0.85,1,1,1` → no response for 300 s); even split works;
  - not every architecture is supported (list in `docs/multi-gpu.md`); DeepSeek V4 is on the list, and the new code has separate handling for its compressed
    attention states. I did not test tensor mode on the old llama.cpp version;
  - marked as **experimental** — check quality before deployment (see README).

---

## 6. Glossary

| Term | Meaning |
|---|---|
| draft | "guesser": a small model/head proposing tokens |
| target model | the large model that approves tokens |
| acceptance, `mean len` | how much of the proposal was accepted; tokens per step (§2) |
| prefill | prompt processing (parallel, fast) — the opposite of generation |
| MTP / NextN | *Multi-Token Prediction* — a built-in head predicting subsequent tokens |
| layer split / tensor split | layer-wise split (pipeline) / split of each layer across GPUs (§5) |
| all-reduce | summing partial results from all GPUs after each layer |
| slot | a parallel "line" handling one request in `llama-server` (`--parallel`) |
| ubatch | micro-batch during prefill; it determines compute buffers (memory) and prefill speed |
