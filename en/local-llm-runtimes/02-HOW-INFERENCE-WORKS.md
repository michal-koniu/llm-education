# 02 · How inference works: from token to token

**Why this chapter.** This is the foundation of the entire course. Every subsequent chapter — about llama.cpp, Ollama, vLLM, MLX, ds4 — describes *how a given program solves one of the problems covered here*: how to compute the next token, not compute the same thing twice, pack many users into a single card, split a model across four cards, and guess several tokens ahead. After reading it, you will be able to: trace a single request from text to text and point out where time and memory leak; calculate on paper how many tokens per second a model *can* produce on given hardware and why your four R9700s give ~50, not ~500; compute the KV cache size for any architecture; explain why "batching is free" is false for MoE; calculate the gain from speculative decoding; honestly compare two runtimes. I assume you can program and know hardware, but not the "ML" side — everything is explained from scratch.

> ⚠️ **Nothing here was run by me.** The entire overview is *desk research* and code reading: paper abstracts (arXiv), project documentation, GitHub APIs, and code cloned onto your machine (llama.cpp at version `0ce8cd1` — the production one — as well as vLLM, SGLang, mlx-lm, ds4, TensorRT-LLM). I ran no benchmark and loaded no model. Figures marked *(my calculation)* are arithmetic on the given data — you can repeat them on a calculator. The only **measurements** in this chapter are your own, from the directory [`../speeding-up-generation/README.md`](../speeding-up-generation/README.md).

**Credibility markers.** A fact without a marker = verified in a primary source (code, project documentation, abstract; I give a path or arXiv number). *(author's own claim)* / *(project's own claim)* / *(company's own claim)* = a claim by the author himself (e.g., a number from an abstract), without independent verification. *(third-party source)* = e.g., Wikipedia. *(unverified)* = from memory or inferred. *(my calculation)* = arithmetic on verified or explicitly named data.

**What is not here.** File formats (GGUF, safetensors, MLX) and everything about quantization — that is chapter [`03-QUANTIZATION-AND-FORMATS.md`](03-QUANTIZATION-AND-FORMATS.md). Here I use only one number from that world: *how many bytes one weight takes* (3 bits = 0.375 bytes), because without it you cannot compute speed. The commands in the "Check it yourself" boxes are read-only; they come from research notes, not run by me personally.

## Table of contents

1. [The journey of a single request](#1-the-journey-of-a-single-request)
2. [Prefill and decoding; roofline on your hardware](#2-prefill-and-decoding-roofline-on-your-hardware)
3. [Attention variants (MHA, MQA, GQA, MLA…) and KV size](#3-attention-variants-and-kv-size)
4. [Experts (MoE): why batching is not free](#4-experts-moe-why-batching-is-not-free)
5. [KV cache management](#5-kv-cache-management)
6. [Generation batching and what `--parallel` really is](#6-batching-generation-and-what---parallel-really-is)
7. [Attention kernels](#7-attention-kernels)
8. [Multi-GPU parallelism and your measurement](#8-multi-gpu-parallelism-and-your-measurement)
9. [Speculative decoding](#9-speculative-decoding)
10. [Sampling](#10-sampling)
11. [Grammar and tool calling](#11-grammar-and-tool-calling)
12. [Chat templates and reasoning parsers](#12-chat-templates-and-reasoning-parsers)
13. [Determinism and numerics](#13-determinism-and-numerics)
14. [How to measure fairly](#14-how-to-measure-fairly)
15. [What this means for me](#15-what-this-means-for-me) · 16. [What I could not establish](#16-what-i-could-not-establish) · 17. [Glossary](#17-glossary)

Related: [`01-MAP-AND-LAYERS.md`](01-MAP-AND-LAYERS.md) · [`04-LLAMA-CPP-AND-THE-GGML-FAMILY.md`](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md) · [`06-SERVING-ENGINES-VLLM-SGLANG.md`](06-SERVING-ENGINES-VLLM-SGLANG.md) · [`07-APPLE-MLX-OMLX-AND-DS4.md`](07-APPLE-MLX-OMLX-AND-DS4.md) · [`09-COMPARISON-AND-CHOICE.md`](09-COMPARISON-AND-CHOICE.md) · [`SOURCES.md`](SOURCES.md).

---
## 1. The journey of a single request

A *decoder-only* model (which is what all models in this course are) defines one thing: **the probability distribution of the next token, given all the previous ones**. Generation is a loop: run the network on tokens it has not processed yet, take the output from the last position, pick a token, append, repeat.

```
 text: "Napisz funkcję sortującą"                       (UTF-8)
   │  1. TOKENIZER  (text -> ids; V4-Flash vocabulary: 129,280 entries)
   ▼
 [ t1  t2  t3  t4  t5 ]                                  n prompt tokens
   │  2. EMBEDDING  (row of the tok_embd[id] table -> vector of length d = 4096)
   ▼
 ┌──────────── repeat × N layers (V4-Flash: 43) ───────────────────────────┐
 │  RMSNorm                                                                  │
 │  ATTENTION: Q,K,V = project(x); RoPE(Q,K); K,V -> into KV CACHE;         │
 │         output = softmax(Q·Kᵀ)·V over all positions seen so far          │
 │  + residual (x + output)                                                 │
 │  RMSNorm                                                                  │
 │  FFN (dense) or MoE (router picks 6 of 256 experts + 1 shared)           │
 │  + residual                                                              │
 └───────────────────────────────────────────────────────────────────────────┘
   │  3. FINAL NORM + lm_head ([d] -> [vocabulary]) — only for positions
   │     whose output is needed (when reading the prompt: only the last one)
   ▼
 LOGITS: 129,280 numbers ("score" of each possible next token)
   │  4. SAMPLER CHAIN (penalties, top-k, top-p, min-p, temperature, sampling;
   │     optionally grammar mask, reasoning budget)
   ▼
 token t6 ──► detokenization ──► text stream to the client
   │
   └── append t6 and return to step 2 — now for only ONE new token
```

- **Tokenizer** splits text into pieces from a fixed vocabulary. The model sees ids, not letters; "tok/s" is therefore a unit of the model, not of human text (how many tokens per Polish word — I did not measure).
- **Layer** (*pre-norm*): normalization → attention → add to input → normalization → FFN or experts → add to input. Model = embedding table + N layers + final norm + `lm_head`. In llama.cpp each architecture is a separate ggml graph in `src/models/*.cpp` (165 files in this build; incl. `qwen3moe.cpp`, `deepseek2.cpp`, `deepseek4.cpp`), built from shared blocks in `src/llama-graph.cpp` (`build_attn*`, `build_ffn`, `build_moe_ffn`).
- **Attention** is the only place where a token "looks at" other tokens. To avoid recomputing other tokens' K and V at every step, they are stored in the **KV cache** — most of this chapter is devoted to it.
- **Sampler** is the only place with randomness and the only one that works the CPU hard (§10, §11). The rest is matrix multiplication on the GPU.

Three takeaways: (1) generation is **sequential** (*autoregressive*) — token t+1 depends on t, so it can only be sped up by *guessing* and checking (§9); (2) **reading the prompt can be parallelized**, because all its tokens are known — hence the prefill/decoding distinction (§2); (3) **the only state that grows with conversation length is the KV cache** (§3, §5).

In code, both modes are one function, `llama_decode`. The llama.cpp server (`tools/server/server-context.cpp`, `update_slots()`) builds **one** batch per iteration: one token from each slot that is generating, and fills the rest of `n_batch` with prompt tokens from slots that are still reading. vLLM says it in a comment in `vllm/v1/core/sched/scheduler.py`: "There's no 'decoding phase' nor 'prefill phase' in the scheduler. Each request just has the num_computed_tokens and num_tokens_with_spec…".

> **Check it yourself (1)**
> ```bash
> grep -n "batch.size() < n_batch" ~/llama.cpp-0ce8cd1/tools/server/server-context.cpp
> sed -n 620,631p ~/runtimes-src/vllm/vllm/v1/core/sched/scheduler.py
> ls ~/llama.cpp-0ce8cd1/src/models | wc -l          # notes: 165
> ```
> Line numbers may differ slightly — search by phrase.
## 2. Prefill and decoding; roofline on your hardware

### 2.1 Two modes of the same network

- **Prefill** (*prompt processing*, pp): all n tokens of the prompt at once. Matrix × matrix multiplications (GEMM): weights are read from memory **once**, used n times. Work ≈ 2 FLOP × active parameters × n. With n on the order of hundreds of tokens, it is **compute-bound**.
- **Decoding** (*decode*, *token generation*, tg): one new token per sequence per step. Matrix × vector multiplications (GEMV): every byte of weights read from VRAM serves **2 operations** (one multiply-add) per sequence in the batch. It is **memory-bound**.

Analogy: prefill is a cook who reaches into the pantry once for ingredients for a hundred servings; decoding is a cook who goes back to the pantry for every single serving. Precisely: the time of a decoding step is mostly *the time to read the weights*.

> **The conclusion the whole course rests on:** since the cost of a step is mostly reading the weights, checking **several tokens at once costs barely more than one**. Both user batching and speculative decoding rest on this. (With a caveat for MoE — §4.)

### 2.2 Roofline

Achievable kernel speed = min(peak FLOPS, arithmetic intensity × memory bandwidth); AI intensity = FLOP / bytes from memory. **Ridge point** AI\* = peak FLOPS / bandwidth: below it the kernel is memory-bound, above it — compute-bound. (Model: Williams, Waterman, Patterson 2009 *(from memory, unverified)*. For LLMs the best source is Pope et al., arXiv 2211.05102: PaLM-540B — 29 ms/token at small batch with int8 weights and 76% MFU at large batch *(authors' own claim)*.)

For weights of *b* bytes (FP16: 2; 8 bits: ~1; 4 bits: 0.5; 3 bits: 0.375), a decoding step with B sequences performs 2B FLOP per weight and reads b bytes, so **AI = 2B/b**, and the batch at the ridge point is **B\* = AI\* × b / 2** *(my calculation)*.

### 2.3 Your card — what we know about it

| Fact | Value | State of knowledge |
|---|---|---|
| GPU | AMD Radeon AI PRO R9700, target `gfx1201`, RDNA4 | verified: `rocminfo`, architecture table in ROCm documentation |
| VRAM | 34,208,743,424 B = 31.86 GiB per card | verified: `/sys/class/drm/card*/device/mem_info_vram_total` (4 cards) |
| Units / cache | 64 CUs, 8 MiB L2, 64 MiB Infinity Cache | verified: ROCm documentation |
| Memory clock | states 96…1258 MHz | verified: `pp_dpm_mclk` |
| **Memory bandwidth** | **~640 GB/s** (256-bit GDDR6, ~20 Gbps) | **third-party source + calculation**: Wikipedia on the RX 9000 series reports "up to 640 GB/s depending on model"; 1258 MHz × 16 = 20.1 Gbps agrees with 20 Gbps GDDR6 *(×16 multiplier unverified)*. **AMD's page could not be fetched.** |
| FP16 peak | ~96 TFLOPS dense | *(unverified)* — from memory; treat as a parameter |
| Host link | sysfs: 32 GT/s (PCIe 5.0), x16 on all four | verified read — **but** see below |
| Card-to-card | PCIe only (no XGMI on RDNA4 cards) | *(unverified)* |

**A note on PCIe.** The CPU is a Ryzen 7 9700X (from `rocminfo`), with about 28 usable PCIe lanes, so four true x16 Gen5 links are impossible *(unverified)*. Your log says outright that **cards 1 and 3 run at x4** ([`../speeding-up-generation/01-JAK-TO-DZIALA.md`](../speeding-up-generation/01-JAK-TO-DZIALA.md)). The sources disagree — trust your own observation and confirm with `lspci -vv` (`LnkSta`). PCIe 5.0 x16 peak ≈ 32 GT/s × 16 × 128/130 / 8 = **63 GB/s per direction**; 4.0 x16 = 31.5 GB/s *(my calculation)*.
### 2.4 The breaking point on your card

At 96 TFLOPS and 640 GB/s: **AI\* = 150 FLOP/B** *(calculated from unverified data)*. Hence B\*: FP16 → 150; 8 bits → 75; 4 bits → 38; 3 bits → 28 *(my calculation)*. The fewer bits, the fewer tokens are needed to saturate the compute — but real kernels unpack weights in the ALU or use INT8 products (the MMQ path in llama.cpp), so the actual point is higher; these are lower bounds.

**Conclusion for a dense model:** as long as B < B\*, the step costs almost the same for 1 and for B sequences, so **batching is almost free throughput**. That is why servers batch, and "single-user" engines look slow: they sit far to the left of the roofline chart.

### 2.5 Example A — dense 13B model at 3 bits

Bytes per token = 13e9 × 3/8 = **4.875 GB**. At 640 GB/s the ceiling is **131 tok/s per card** at 100% bandwidth *(my calculation)*. Real kernels achieve a fraction (usually 60–80% *(unverified)*; measure with `llama-bench -p 0 -n 128`). KV reads add on top (§3).

### 2.6 Example B — your class: DeepSeek-V4-Flash

Data from `config.json` and the model card of `deepseek-ai/DeepSeek-V4-Flash` (verified): 43 layers, hidden dimension 4096, **256 routed experts + 1 shared, 6 per token**, `moe_intermediate_size` 2048, 64 heads, `num_key_value_heads` 1, `head_dim` 512, window 128, context 1,048,576, vocabulary 129,280, experts in FP4, the rest FP8; "284B parameters (13B active)".

**Where do those 13B live?** *(my calculation)* An expert (SwiGLU, 3 matrices): 3 × 4096 × 2048 = 25.17M. Routed experts: 256 × 43 × 25.17M = **277.0B**. The rest (attention, shared, embeddings, `lm_head`, router) = 284 − 277 = **~7.0B**. Active per token: 7.0 + 6/256 × 277.0 = **13.5B** — matches the advertised 13B, which confirms the split. **Roughly half of the weight traffic per token is always-read dense and shared weights, half is the 6 experts per layer.**

At uniform 3 bits (a stand-in; real quantizations are mixed — chapter 03): dense 7.0B × 0.375 = 2.6 GB + active experts 277B × 6/256 × 0.375 = 2.4 GB ≈ **5.1 GB per token**; single-card ceiling: 640 / 5.1 ≈ **126 tok/s** *(I ignore KV and activations)*.

**What four cards give you.** With `--split-mode layer` a token travels through the cards in turn, so at any moment only one card's bandwidth "works": the same ceiling of ~126 tok/s. The cards bought **capacity** (106.5 GB of weights at 3 bpw does not fit in 32 GB). With ideal tensor split the bandwidths add up: 4 × 640 = 2560 GB/s ⇒ ~506 tok/s, minus communication (§8).

**Prefill:** FLOP per token ≈ 2 × 13.5B = **~27 GFLOP**; at 96 TFLOPS × 40% *(both inputs unverified)* ~1,400 tok/s per card, ~5,700 with four busy. Your prefill: ~960 → ~700 tok/s after switching to the deployed configuration ([`../speeding-up-generation/README.md`](../speeding-up-generation/README.md)) — far below that ceiling; I do not know why *(unverified)*.

**KV is the second half of the traffic in decoding:** each step also reads the entire KV cache of all sequences in the batch. Llama-3.1-70B's KV at 128K (40 GiB, §3) is larger than its weights in 4 bits — that is why MQA/GQA/MLA and sparse attention exist.

> **Check it yourself (2)**
> ```bash
> cat /sys/class/drm/card*/device/mem_info_vram_total      # 34 208 743 424 B (notes)
> cat /sys/class/drm/card*/device/pp_dpm_mclk              # highest state: 1258 MHz
> cat /sys/class/drm/card*/device/current_link_speed /sys/class/drm/card*/device/current_link_width
> lspci -vv | grep -E "VGA|Display|LnkSta:"                # (root) compare with "cards 1 and 3 on x4"
> ```
> Arithmetic exercise: tok/s ceiling = `bandwidth [GB/s] / (active parameters [B] × bits / 8)`. Compute it for a dense 70B at 4 bits (35 GB of weights — how many cards, and what does that mean for speed with layer split?). Measurement (not run by me; **the cards are production** — stop `llama-swap` or use a small model): `llama-bench -p 0 -n 128` (pure decoding), `llama-bench -d N` (pre-fills N context tokens).

---
## 3. Attention variants and KV size

Layer building blocks in brief: **RMSNorm** (Zhang and Sennrich, NeurIPS 2019: normalization without mean subtraction; "7%–64%" faster than LayerNorm *(authors' own claim)*), **SwiGLU** FFN: y = W_down(SiLU(W_gate·x) ⊙ (W_up·x)) — three matrices (Shazeer, arXiv 2002.05202), **RoPE** (below). In each layer, every token produces a key K and a value V; the KV cache holds them for all tokens seen so far. For MHA/MQA/GQA:

> **KV bytes per token = 2 (K and V) × n_layers × n_kv_heads × head_dim × bytes_per_element**

(in llama.cpp: `n_embd_k_gqa(il)` / `n_embd_v_gqa(il)`, KV tensors of shape `[n_embd_k_gqa, kv_size, n_stream]` — `src/llama-kv-cache.cpp`).

| variant | idea | source |
|---|---|---|
| **MHA** | as many K/V heads as queries | Vaswani et al. 2017 *(unverified)* |
| **MQA** | **one** K/V head for all queries; Shazeer, arXiv 1911.02150: decoding is slow due to "memory bandwidth cost of repeatedly loading large key and value tensors" | abstract |
| **GQA** | n_kv between 1 and n_heads; Ainslie et al., arXiv 2305.13245; existing MHA can be converted by "uptraining" at 5% of pretraining cost *(authors' own claim)* | abstract |
| **MLA** | cache holds a **low-dimensional latent vector** (`kv_lora_rank`) plus a small separate RoPE key; K and V are reconstructed from the vector or "absorbed" into multiplications *(absorption — unverified)*. DeepSeek-V2, arXiv 2405.04434: **KV 93.3% smaller**, 5.76× higher throughput than DeepSeek 67B *(authors' own claim)* | abstract |
| **DSA** | a "lightning indexer" scores previous tokens; full attention only after top-k; DeepSeek-V3.2, arXiv 2512.02556 | abstract (indexer mechanism — unverified) |
| **CSA / HCA** (V4) | raw 128-token window + KV rows compressed over time: on even layers ≥2 one row per 4 tokens (indexer selects up to 512), on odd layers ≥3 one per 128; layers 0–1 window only | `MODEL_CARD.md` ds4 + `config.json` (`compress_ratios`, `index_topk` 512, `sliding_window` 128) |

llama.cpp has separate cache classes for them in `src/`: `llama-kv-cache.cpp` (for MLA `has_v = !is_mla` — **no V tensor**), `llama-kv-cache-iswa.cpp` (two caches: full and windowed), `llama-kv-cache-dsa*.cpp`, `llama-kv-cache-dsv4.cpp`, `llama-memory-recurrent.cpp` (SSM/RWKV), `llama-memory-hybrid*.cpp`.

### 3.1 KV sizes with numbers (FP16/BF16 cache, 2 B per element)

Configurations from `config.json` on Hugging Face (Llama via the NousResearch mirror — the official repository is closed).

| model | input data | bytes per token | at 128K |
|---|---|---|---|
| Llama-3.1-70B (GQA) | 80 layers, 8 KV heads, head_dim 128 | 2×80×8×128×2 = **327,680 B = 320 KiB** | **40 GiB** |
| same as MHA (64 KV heads) | | 2.5 MiB | 320 GiB (8×) |
| Qwen3-30B-A3B (GQA) | 48 layers, 4 KV heads, head_dim 128 | **96 KiB** | 12 GiB (native max 40,960 ⇒ 3.75 GiB) |
| gpt-oss-120b (GQA + SWA) | 36 layers alternating window(128)/full, 8 KV heads, head_dim 64 | full layers: 18×8×64×2×2 = **36 KiB** (+ fixed 128-token window) | ~4.5 GiB *(my calculation)* |
| DeepSeek-V3 (MLA) | 61 layers, `kv_lora_rank` 512, `qk_rope_head_dim` 64 | 61×(512+64)×2 = **70,272 B = 68.6 KiB** | 8.6 GiB |
| same as MHA | 128 heads × (192+128) × 2 B × 61 | 5.0 MB | 71× MLA *(my calculation)* |
| DeepSeek-V4-Flash (CSA/HCA) | averaged: (21/4 + 20/128) = 5.41 rows × 512 × 2 B + indexer 21/4 × 128 × 2 B (assumes shared K=V row, FP16, no window) | **~6.9 KB** | ~1M tokens ≈ 6.4–6.7 GiB (depending on whether "1M" is 10⁶ or 2²⁰) *(my calculation; assumptions unverified)* |

Sanity check: 6.9 KB is ~10% of MLA from V3, which matches the model card's claim of "10% KV relative to V3.2 at 1M" *(company's own claim)* (V3.2 also holds the indexer cache, so the match is approximate).

**How to use this.** Take the number of layers, KV heads, and `head_dim` from `config.json` (or `kv_lora_rank` + `qk_rope_head_dim` for MLA), compute, divide the free VRAM after weights by the result — you get the upper bound of context tokens across all slots together. For you, the KV of a single 131,072-token sequence is on the order of 0.9 GB *(my calculation, assumptions as in the table)* — a fraction of the weights. Yet the log at 4 slots × 131,072 showed `cudaMalloc failed: out of memory`: the card also holds compute buffers (dependent on `--ubatch-size`) and ~4 GB per card for the draft ([`02-WDROZENIE-DEEPSEEK.md`](../speeding-up-generation/02-WDROZENIE-DEEPSEEK.md)).
### 3.2 RoPE — briefly, because it has consequences for the KV cache

RoPE (Su et al., arXiv 2104.09864) rotates pairs of Q and K coordinates by a position-dependent angle, so the dot product depends only on relative distance. Consequences: RoPE is applied to K **before** it is written to the cache, so the stored keys "remember" the absolute position; shifting the cache (*context shift*) requires re-rotating the keys — `seq_add` (K-shift) gated by `get_can_shift()` in `llama-kv-cache.cpp`, which is why context shift does not work for every architecture or with multimodal prompts. Context extension: linear scaling, **YaRN** (arXiv 2309.00071: "10× fewer tokens and 2.5× fewer steps" *(authors' own claim)*), LongRoPE (`LLAMA_ROPE_SCALING_TYPE_*` in `llama.h`); DeepSeek-V3 uses YaRN with a factor of 40, V4 — 16 (`config.json`). MLA keeps a separate small part of the key with RoPE precisely so that the hidden vector can remain "position-free".

> **Check it yourself (3)**
> ```bash
> grep -n "is_mla\|has_v" ~/llama.cpp-0ce8cd1/src/llama-kv-cache.cpp | head      # MLA => no V tensor
> ls ~/llama.cpp-0ce8cd1/src | grep -E "kv-cache|memory"
> ```
> Arithmetic exercise: download the `config.json` of the model from your `llama-swap`, compute the KV bytes per token from the formula above for two context sizes, and compare with the free VRAM from the measurement loop in `../speeding-up-generation/narzedzia/`.

---

## 4. Experts (MoE): why batching is not free

### 4.1 Routing

In **MoE** (*mixture of experts*) the dense FFN is replaced by many small ones ("experts"). A **router** (one small linear layer: `logits = W_gate·x`) scores the experts, the token goes to top-k, the results are weighted and summed; **shared experts** always run (DeepSeekMoE idea, arXiv 2401.06066: 16B model ~ LLaMA2-7B at ~40% compute *(authors' own claim)*; Mixtral, arXiv 2401.04088: 8 experts, top-2, 47B total / 13B active *(authors' own claim)*).

Code: `llm_graph_context::build_moe_ffn` (`src/llama-graph.cpp`). Steps: (1) gating function — softmax, sigmoid, or **sqrt-softplus** (`scoring_func: sqrtsoftplus` in V4); (2) optional **choice load** `exp_probs_b`, added *only to the choice* (balancing without an auxiliary loss from DeepSeek-V3, arXiv 2412.19437); (3) optionally best groups first (`n_expert_groups`, `n_group_used`); (4) `ggml_argsort_top_k`; (5) unweighted weights, renormalization (`norm_w`) and scale (`w_scale`; `routed_scaling_factor` 1.5 in V4); (6) `ggml_mul_mat_id` — grouped GEMM only for the selected experts. For CUDA/HIP there is fused gating (`ggml-cuda/topk-moe.cu`). llama.cpp also has a **host-side expert cache** (`src/llama-moe-cache.{h,cpp}`: it keeps frequently used experts of layers residing in host RAM in a device-side buffer) — thanks to it, models larger than VRAM are tolerable.

**Consequence:** *total* parameters determine **capacity** (VRAM), *active* ones determine **bytes per token** (speed), and the number of *distinct* experts touched in one step determines how much batching and speculation cost.

### 4.2 Calculation: how many experts a batch touches

With B tokens in a step and **uniform, independent routing** *(simplifying assumption)* the fraction of touched experts in a layer:

> **f(B) = 1 − (1 − 6/256)^B**

Bytes per step = dense (~2.6 GB) + 277B × 0.375 B × f(B). At 640 GB/s for one card and 3 bpw *(everything: my calculation; without KV and activations, 100% bandwidth)*:

| batch B | experts touched | GB / step | step time | aggregate tok/s | bytes per token vs B=1 |
|---|---|---|---|---|---|
| 1 | 2.3% | 5.1 | 7.9 ms | 126 | 1.00× |
| 4 | 9.1% | 12.0 | 18.8 ms | 213 | 0.59× |
| 8 | 17.3% | 20.6 | 32.2 ms | 249 | 0.51× |
| **32** | **53.2%** | 57.9 | 90.4 ms | 354 | 0.36× |
| 128 | 95.2% | 101.5 | 158.6 ms | 807 | 0.16× |
| 512 | 100% | 106.5 | 166.4 ms | 3077 | 0.04× |

Row B = 32 in your head: (1 − 6/256)^32 ≈ 0.468 ⇒ 53.2% of experts touched ⇒ 0.532 × 277B × 0.375 B ≈ 55 GB + 2.6 GB dense = 57.9 GB. A **dense** model with the same 13B active would still read ~5 GB.

1. **For MoE, "batching is free" is false until almost all experts are present in the step.** At B = 32 each expert gets on average 0.75 token (B × 6/256). The inflection point for *expert* GEMMs lies at B ≈ 28 × 256/6 ≈ **1200 tokens**, not 28 *(my calculation)*. Real routing is skewed ("hot" experts), so the real traffic is lower *(unverified)*.
2. **Speculative decoding on MoE is penalized**: verifying n tokens reads 1.47× (n=2), 1.93× (3), 2.38× (4), 2.82× (5), 3.25× (6), 4.07× (8) the bytes of a single token *(my calculation)*. The DFlash PR to llama.cpp says this for gpt-oss: the speedup "is usually smaller than for dense-attention targets, because parallel verification activates more experts than single-token decoding" (ggml-org/llama.cpp#22105). Net-gain table: §9.3.
### 4.3 What this means for you

Two agents instead of one (deployed configuration, 2 slots): 34.5 tok/s each, **63** total, versus 49.7 for one ([`README.md`](../speeding-up-generation/README.md)); with 4 agents (2 slots + queue) 63 total. The second agent added ~27% of aggregate throughput, not +100% — *sublinearly*, as in the table (with uniform routing and no speculation B = 2 gives 1.37×; in your case each slot already verifies 4 tokens per step, so two slots make 8 — an order-of-magnitude comparison, not proof *(unverified)*). And speculative decoding gave you 1.5–1.6× (§8.4) — more than the MoE calculation for uniform routing suggests (§9.3: 1.2–1.45×). Possible explanations: correlated routing of neighboring tokens or high draft accuracy; **I did not check which**.

> **Check it yourself (4)**
> ```bash
> grep -n "build_moe_ffn\|argsort_top_k\|exp_probs_b\|n_group_used" ~/llama.cpp-0ce8cd1/src/llama-graph.cpp | head -20
> head -40 ~/llama.cpp-0ce8cd1/src/llama-moe-cache.h
> ```
> Exercise: in Python compute f(B) = 1 − (1 − k/E)^B for Mixtral (k=2, E=8) and for Qwen3-30B-A3B (**take the k and E numbers from its `config.json` — they are not in my notes**). At what B does Mixtral touch 90% of experts? Why are MoE models with few experts less "punished" by batching than fine-grained ones (DeepSeek)?

---

## 5. KV cache management

KV is the only request state that grows. Problems: fragmentation, sharing, eviction, windows and compression, moving to cheaper memory.

### 5.1 Continuous slice versus paging

Naively: reserve max_len × bytes_per_token of contiguous space per request — fragmentation and over-reservation. **PagedAttention** (Kwon et al., SOSP 2023, arXiv 2309.06180): KV in blocks, mapped by a block table — like virtual memory; "near-zero waste", **2–4×** higher throughput than FasterTransformer and Orca at the same latency *(authors' claim)*. vLLM code: `vllm/v1/core/kv_cache_manager.py`, `block_pool.py`, `kv_cache_utils.py`; `DEFAULT_BLOCK_SIZE = 16` tokens (`vllm/config/cache.py`).

### 5.2 Prefix caching — lever no. 1 for agents

The start of the prompt (system, tool schemas, history) returns in every turn; reusing its KV shortens TTFT.

- **vLLM**: hash chain — every *full* block gets a hash (previous hash, block tokens, extra keys like LoRA); freed blocks stay on an LRU list; enabled by default (`enable_prefix_caching = True`), `sha256` hash; hits with block granularity (16 tokens).
- **SGLang RadixAttention** (arXiv 2312.07104: "up to 6.4×" *(authors' claim)*): a **radix tree** over token sequences (`mem_cache/radix_cache.py`: `RadixKey`, `TreeNode` with `lock_ref`, `last_access_time`, `hit_count`; `match_prefix`, node splitting on partial match, LRU/priority eviction). Many agents sharing a prefix with different suffixes hit the cache; the scheduler is cache-aware (`lpm`, `dfs-weight`, `fcfs`, `lof` policies in `managers/schedule_policy.py`).
- **llama.cpp**: `--slot-prompt-similarity` (selects the free slot with the longest common prefix), `--cache-reuse N` (fragments ≥N tokens matched *anywhere* in the old prompt, moved via `seq_add`), **RAM prompt cache** `--cache-ram MiB` (default 8192; free slots saved when `--cache-idle-slots`, enabled by default), `--ctx-checkpoints N` (default 32; checkpoints required by SWA and recurrent models, because their state cannot be truncated token by token). Values from `common/common.h`, `common/arg.cpp`.
- **MLX-LM**: `PromptTrie` + `LRUPromptCache` (`mlx_lm/models/cache.py`, `--prompt-cache-size`). **ds4**: KV snapshots of the prefix **on disk** (`--kv-disk-dir`, `--kv-disk-space-mb`; "files contain prompt text and model state: treat the directory as sensitive").
### 5.3 Windows, compression, recurrent state

- **SWA**: the layer only looks at the last W tokens, so its cache is a ring buffer (gpt-oss: W = 128 on every other layer). llama.cpp: full cache for global layers and a small one for SWA; `--swa-full` forces full. The cost: the SWA cache cannot be cheaply "rewound" — hence the checkpoints from §5.2. MLX: `RotatingKVCache(max_size, keep=0)` — overwrites the oldest entries, can pin the first `keep` tokens.
- **Compression** (DSA, CSA/HCA): §3. **Recurrent layers** (Mamba, Qwen3-Next "gated delta net", RWKV): fixed state size per sequence instead of KV per token; the state "does not decompose across positions", so rewinding under speculation requires snapshots (PR #22105 text).

### 5.4 What "slot" and "unified KV" really are in llama.cpp (verified)

- The KV store is an array of **cells**; each holds (position, set of sequence ids). `llama_kv_cache::find_slot` selects cells for a micro-batch, `seq_rm/seq_cp/seq_keep/seq_add` edit metadata, and the attention mask is built from positions and membership. **There is no block array**, there is a cell index per token — memory resistant to fragmentation, although kernels see a masked contiguous window.
- **`n_stream`**: with `kv_unified = false` the KV tensor has shape `[n_embd_kv, kv_size, n_stream]` with `n_stream == n_seq_max` — **each sequence has a private stream of `n_ctx / n_seq_max` cells**. With `kv_unified = true` there is one stream and all sequences share the entire `n_ctx` pool.
- In this build `-np` defaults to **auto**: "using n_parallel = 4 and kv_unified = true" (`tools/server/server.cpp`). `--cont-batching` is enabled by default.
- **Context shift** (`--context-shift`, *disabled* by default): once a slot reaches `n_ctx`, keep the first `n_keep` tokens, discard `n_discard` (by default half of the rest), `seq_rm` + `seq_add(−n_discard)` — a lossy sliding window that re-rotates keys. When disabled, the request ends at the limit.

### 5.5 KV in fewer bits and offload

llama.cpp: `-ctk/-ctv` default to `f16`; allowed `f32, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1`; **quantized V requires flash attention**; **tensor split requires unquantized KV** (`docs/multi-gpu.md`) — your constraint, because the deployed configuration uses f16. Research basis: KIVI (arXiv 2402.02750; 2 bits, 2.6× less peak memory *(project's own claim)*). The rest on quantization — chapter 03. Offload: vLLM has KV connectors (LMCache, NIXL, Mooncake and others) and `kv_offload` directories; LMCache (arXiv 2510.09665): "up to 15×" with vLLM *(project's own claim)*; SGLang HiCache — I know the file names, I could not verify the semantics. For a single user, `--cache-ram` and the ds4 disk matter. (Do not confuse with the host *expert* cache from §4.1 — that one holds weights, this one holds KV.)

| mechanism | llama.cpp (`0ce8cd1`) | vLLM | SGLang | mlx-lm | ds4 |
|---|---|---|---|---|---|
| KV layout | cells; streams or unified pool | blocks of 16 | pages + radix tree | per-layer cache, grows in steps of 256 | own (V4: compressor state) |
| prefix | best slot, `--cache-reuse`, RAM cache | hash chain, default | radix tree | `PromptTrie` + LRU | disk snapshots |
| window / compression | iSWA, DSA, DSV4 | per-layer cache types | V4 backends | `RotatingKVCache` | native CSA/HCA |
| KV in fewer bits | `-ctk/-ctv` | FP8, turbo/ultraquant backends (I know the names) | *I could not establish* | `QuantizedKVCache` | *I could not establish* |
| offload | `--cache-ram`; expert cache | connectors, cpu/disk | HiCache | *I could not establish* | disk |

> **Check it yourself (5)**
> ```bash
> grep -n "cache_ram_mib\|cache_idle_slots\|n_ctx_checkpoints\|ctx_shift" ~/llama.cpp-0ce8cd1/common/common.h
> sed -n 160,175p ~/llama.cpp-0ce8cd1/tools/server/server.cpp          # "n_parallel = 4 and kv_unified = true"
> grep -n "DEFAULT_BLOCK_SIZE" ~/runtimes-src/vllm/vllm/config/cache.py
> ```
> Exercise: from the `llama-swap` configuration, read `-np`, `-c`, and any `--no-kv-unified` of your production configuration and calculate how many tokens *each* slot has with unified KV and without it.

---
## 6. Batching generation and what `--parallel` really is

### 6.1 Four generations

1. **Static**: collect B requests, run until the longest one finishes; finished sequences waste space.
2. **Dynamic**: wait a moment to gather a batch, still at the request level.
3. **Continuous / iteration-level** (*continuous batching*). Orca (Yu et al., OSDI '22): "iteration-level scheduling" (the batch composition is determined at each iteration; finished requests leave, new ones enter) + "selective batching" (only operations with compatible shapes are batched, e.g. dense multiplications; attention is handled separately per sequence). **36.9×** higher throughput than FasterTransformer at the same latency on GPT-3 175B *(project's own claim, OSDI '22 page)*. Every engine in this course is iterative: the vLLM scheduler (`v1/core/sched/scheduler.py`, 3527 lines), SGLang (`managers/scheduler.py`, 6278), `update_slots()` in llama-server, `BatchGenerator` in mlx-lm (`--decode-concurrency`, `--prompt-concurrency`).
4. **Chunked prefill** and **disaggregation** — below.

### 6.2 Chunked prefill and a citation correction

A long prompt (e.g. a tool result of 20k tokens) takes up an entire iteration and stalls all generating sequences — the per-token latency jumps. The fix: cut the prompt into chunks and attach them to each decoding of other sequences.

> ⚠️ **Citation correction.** The assignment sheet pointed to arXiv 2308.16369 as "Sarathi-Serve". That is not true: **2308.16369 is the original SARATHI** ("Piggybacking Decodes with Chunked Prefills", August 2023), and **Sarathi-Serve is arXiv 2403.02310** ("Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve", March 2024). I checked both abstract pages. The terms "chunked prefill" and "stall-free scheduling" come from the second paper; cite both.

SARATHI: up to 10× higher decoding throughput (LLaMA-13B/A6000), 1.25× end-to-end *(project's own claim)*. Sarathi-Serve: "2.6×" serving capacity for Mistral-7B, "up to 3.7×" for Yi-34B relative to vLLM *(project's own claim)*. In code: vLLM has `enable_chunked_prefill = True` and the `max_num_batched_tokens` budget (`config/scheduler.py`); llama.cpp does this **implicitly** — a prompt longer than `n_batch` stretches over several `llama_decode` calls interleaved with decoding of other slots. The knob pair: `n_batch` (logical batch) and `n_ubatch` (physical micro-batch fed to the GPU graph): `-b`, `-ub`.

### 6.3 Prefill/decode disaggregation

Prefill on some GPUs, decoding on others, KV transferred between them. DistServe (arXiv 2401.09670): "7.4× more requests or 12.6× stricter SLO", optimizes *goodput* *(project's own claim)*; Splitwise (arXiv 2311.18677): 1.4× at 20% lower cost *(project's own claim)*. Implementations (I know they exist, not how they work): vLLM `disagg_prefill.md`, SGLang `srt/disaggregation/`, llm-d, Dynamo.

**When this matters to you.** With a single user the scheduler has nothing to interleave. But in an **agent application** with parallel sub-agents the interference returns: a 20k-token prefill of a tool result will stall the decoding of the others. The llama.cpp answer: slots + unified KV + tuning `n_batch`/`n_ubatch` (smaller micro-batch = shorter stalls, lower prefill throughput) *(my inference)*.
### 6.4 What a slot is (verified)

**A slot is a server concept, not a KV cache concept.** `server_slot` (`server-context.cpp`) = one sequence ID + a state machine {IDLE, WAIT_OTHER, STARTED, PROCESSING_PROMPT, DONE_PROMPT, GENERATING} + its own sampler chain + its own speculation state + its own list of prompt tokens (for prefix matching). `--parallel N` (`-np`) = number of slots = `n_seq_max`.

**Gotcha** *(my inference from §5.4)*: with `-np 4 -c 32768 --no-kv-unified`, each slot gets 8,192 tokens; with unified KV the pool is shared and a single request can take all 32,768 while the rest wait. In your case it's a **measurement**: 2 slots × 98,304 worked best (49.2 tok/s), 4 × 131,072 did not fit, 4 × 65,536 was slower (44.6) and too tight ([`02-WDROZENIE-DEEPSEEK.md`](../speeding-up-generation/02-WDROZENIE-DEEPSEEK.md)). Slots are **not** free.

> **Check it yourself (6)**
> ```bash
> grep -n "struct server_slot" ~/llama.cpp-0ce8cd1/tools/server/server-context.cpp
> grep -n "n_parallel" ~/llama.cpp-0ce8cd1/tools/server/server.cpp | head
> grep -n "enable_chunked_prefill\|long_prefill_token_threshold" ~/runtimes-src/vllm/vllm/config/scheduler.py
> ```
> Exercise: open `arxiv.org/abs/2308.16369` and `arxiv.org/abs/2403.02310` and check which one uses "stall-free" (expected: 2403.02310). Then count how many iterations a prefill of 20,000 tokens takes with `n_batch` = 2048 and how the count changes with `-ub 512`.

---

## 7. Attention kernels

**The FlashAttention line.** Naive attention materializes an N × N matrix in HBM. **FlashAttention** (Dao et al., arXiv 2205.14135): exact "I/O-aware" attention, tiled, with *online softmax*; 15% faster BERT-large, 3× GPT-2 *(authors' own claim)*. The trick *(from memory, unverified)*: for each row keep the running maximum m and normalizer l; when a tile arrives, rescale: m' = max(m, rowmax(S)), l' = e^(m−m')·l + rowsum(e^(S−m')), O' = e^(m−m')·O + e^(S−m')·V — the result is exact, extra memory O(N). **FlashAttention-2** (arXiv 2307.08691): ~2×, 72% MFU on A100. **FlashAttention-3** (arXiv 2407.08608): Hopper-specific (TMA, asynchronous tensor cores, FP8), up to 740 TFLOPs/s in FP16 *(authors' own claim)* — NVIDIA only, for RDNA4 merely a reference point. **FlashInfer** (arXiv 2501.01005): block-sparse formats, JIT, balanced planning; 29–69% lower inter-token latency *(authors' own claim)*. Decoding has a different profile (one query per sequence, KV-bound work; "split-KV / flash-decoding" — from memory); llama.cpp has separate kernels `fattn-vec` (small batch), `fattn-tile`, `fattn-mma-f16`.

**What llama.cpp runs on your cards** (code). The ROCm backend is ggml CUDA code compiled for HIP, so the names are `ggml-cuda/*`. `ggml_cuda_get_best_fattn_kernel` (`ggml/src/ggml-cuda/fattn.cu`) chooses at every call: on AMD with **WMMA** (RDNA3/4) the MMA_F16 kernel **only if** the GQA optimization applies, head_dim ≤ 256 and `Q->ne[1] * gqa_ratio_eff > 8` (head_dim ≤ 128) or `> 16` (≤ 256); otherwise the generic **TILE**, or **VEC** for quantized KV with ≤ 2 query columns. Conclusion *(my calculation from the thresholds)*: decoding with batch 1 on gfx1201 mostly runs through TILE/VEC, while prefill with a large micro-batch runs through WMMA. `-fa auto` is the default; quantized V and tensor split / tensor parallelism **require** FA. Multiplications: `mmvq` (quantized matrix × vector, the workhorse of decoding), `mmq` (matrix × matrix with INT8 tiles; `mmq-config-rdna4.cuh`), `mmf`, `topk-moe`.

**vLLM and SGLang on ROCm** (selection logic, not operation). vLLM knows the R9700 (`vllm/platforms/rocm.py`: `0x7551: "AMD_Radeon_R9700"`, `_ON_RDNA4`); backend priority (`_get_backend_priorities`): `ROCM_ATTN` → `ROCM_AITER_FA` (if AITER is enabled) → `ROCM_AITER_UNIFIED_ATTN` (on RDNA only with `is_rdna_aiter_enabled()`) → `TRITON_ATTN`…; for sparse MLA (DSA/V4) only `ROCM_AITER_MLA_SPARSE` plus separate V4/V4.1 backends. **Whether AITER is tuned and works on gfx1201, and not just on the MI300 class, does not follow from the code.** SGLang has `aiter_backend.py`, `triton_backend.py`, `flashinfer_backend.py`, `deepseek_v4_backend*.py` (including `_hip_radix`). MLX uses its own Metal kernels *(unverified)*. Details: chapter [`06`](06-SERVING-ENGINES-VLLM-SGLANG.md).

> **Check it yourself (7)**
> ```bash
> grep -n "amd_wmma\|TILE\|VEC\|MMA_F16" ~/llama.cpp-0ce8cd1/ggml/src/ggml-cuda/fattn.cu | head -40
> grep -n "R9700\|_ON_RDNA4" ~/runtimes-src/vllm/vllm/platforms/rocm.py
> ```
> Code-reading exercise: find the `> 8` and `> 16` thresholds; determine the branch for decoding with batch 1 at an effective GQA ratio of 8 (1 × 8 does not exceed `> 8`). Then read `head_dim` from your model's `config.json` and check whether `head_dim <= 256` even permits MMA_F16. The result for your model I do not know *(unverified)*.

---
## 8. Multi-GPU Parallelism and Your Measurement

### 8.1 Five Types of Split

| type | what is split | communication per layer | where |
|---|---|---|---|
| **Tensor (TP)**, Megatron-LM (arXiv 1909.08053: 8.3 billion parameters on 512 GPUs, 76% efficiency *(project's own claim)*) | attention heads and FFN columns/rows; each card holds 1/n of every layer | 2 *all-reduce* per layer *(standard; unverified in the paper's content)* | llama.cpp `--split-mode tensor`, vLLM, SGLang |
| **Pipeline (PP)** | contiguous ranges of layers per card | one activation transfer per stage boundary | llama.cpp `--split-mode layer` (default), vLLM |
| **Expert (EP)** | MoE experts distributed across cards; tokens routed *all-to-all* | 2 all-to-all per MoE layer | vLLM (`fused_moe/all2all*`, `distributed/eplb`), SGLang `eplb/` |
| **Data (DP)** | full replicas | none | vLLM; several llama-server processes under `llama-swap` is "DP for the poor" *(my inference)* |
| **Sequence/context (SP/CP)** | the sequence dimension of attention/KV | KV exchange or partial softmaxes | vLLM `_DCP`, `_PCP` (I know the names) |

### 8.2 What the Interconnect Must Carry *(my calculation; flagged inputs)*

V4-Flash shape: hidden 4096, 43 layers ⇒ 86 *all-reduce* per token in TP, FP16.

- **Decoding, batch 1:** one all-reduce = 4096 × 2 B = **8 KiB**; bandwidth does not matter, **latency dominates**: 86 collectives × (10–40 µs, *unverified range*) = **0.9–3.4 ms per token**, versus an ideal TP step of ~2 ms (5.1 GB / 2560 GB/s). TP with batch 1 over PCIe is therefore latency-bound.
- **Prefill, ubatch 2048:** 2048 × 4096 × 2 B = 16 MiB per all-reduce, ×86, ring traffic ≈ **2.0 GiB per card per ubatch**; at 63 GB/s = 34 ms, at 25 GB/s (through the host) = 87 ms, versus ~345 ms of compute *(unverified compute input)* — overhead of 10–25%, *if* the link delivers; for x4, four times worse.
- NVLink/xGMI are ~10× faster than PCIe and have much lower latency *(unverified)*; the R9700 does not have them — every byte between cards goes through PCIe.

### 8.3 Split Modes in llama.cpp (`docs/multi-gpu.md` and code)

- `none`, **`layer`** (default; "priority is a fast prefill", tolerates a slow interconnect), `row` (deprecated), **`tensor`** (EXPERIMENTAL; "meta device" abstraction in `ggml/src/ggml-backend-meta.cpp`; splits weights *and* KV).
- `tensor` requires `-fa on` and **unquantized KV**, disables `--fit` and backend-side sampling; **not implemented** for, among others, Grok, MPT, OLMoE, **DeepSeek2, DeepSeek32**, GLM-DSA, Nemotron-H, MiniMax, Kimi-Linear, Jamba, Mamba(2), Gemma3n, T5 (full list: `llm_arch_supports_sm_tensor`, `src/llama-arch.cpp`). **DeepSeek4 is not on the exclusion list**; your log adds that an updated llama.cpp has explicit support for V4 compressed attention states in this mode, and on the old version you did not try it.
- Reductions: `ggml_backend_comm_allreduce_tensor` (e.g. NCCL) with a generic fallback variant. For ROCm, **RCCL must be enabled at build time with `-DGGML_HIP_RCCL=ON`; by default it is DISABLED**, because "(unlike NCCL) it was not universally beneficial in tests". A built-in all-reduce exists for **two** GPUs (via pinned host memory, with active spinning in the kernel for low latency — `ggml-cuda/allreduce.cu`), meaning the authors know decoding is latency-bound. `GGML_CUDA_P2P=1` (opt-in) enables direct peer-to-peer access between cards; "may cause crashes or corrupted results on some boards (e.g. with IOMMU)".
- **True pipelining** (micro-batch overlap) is enabled only when: >1 device, all layers on GPU, `split_mode == LAYER`, `offload_kqv`, no tensor overrides, no MoE host cache, async support (`src/llama-context.cpp`; log "pipeline parallelism enabled"). For a **single** stream there is nothing to overlap — hence layer split gives single-card speed (§2.6).
### 8.4 Your measurement against the theory

Data from your journal (DeepSeek-V4-Flash-0731, UD-IQ3_XXS, 4 cards, one agent, average of 4 task types × 2 temperatures; [`README.md`](../speeding-up-generation/README.md), [`02-WDROZENIE-DEEPSEEK.md`](../speeding-up-generation/02-WDROZENIE-DEEPSEEK.md)):

| configuration | tok/s | ms / token *(my calculation)* | fraction of the 126 tok/s ceiling *(my calculation)* |
|---|---|---|---|
| old llama.cpp, layer split, no draft | 23.5 | 42.6 | |
| old, + DSpark (n=3) | 35.2 | 28.4 | |
| **new** (`0ce8cd1`), layer split, no draft | 25.2 | 39.7 | ~20% |
| new, layer split, with draft | 37.9 | 26.4 | |
| new, **tensor split**, no draft | 29.1 | 34.4 | ~23% |
| new, tensor split, with draft (1 slot × 131k) | 46.2 | 21.6 | |
| new, tensor split + draft, **deployed** (2 slots × 98k, `--ubatch-size 512`) | 49.2 (production ≈ 49–50) | 20.3 | |

(46.2 and 49.2 are two *different* configurations from the matrix in the journal, not a contradiction. The 126 ceiling is computed for a substitute 3 bpw and 640 GB/s — it is an order of magnitude, not a precise efficiency; the average number of bits in your file is 2.94 bpw (104,207,848,508 B · 8 / 284 billion, *my calculation*; chapter [03](03-QUANTIZATION-AND-FORMATS.md), §7.4), so "3 bpw" was a good approximation.)

1. **Tensor split gave +15% without draft (25.2 → 29.1), not ×4.** Consistent with the fact that at batch 1 what matters is collective latency, not throughput. In the log you have `internal AllReduce init failed (n_devices != 2?); falling back to meta-backend butterfly` — with four cards the **generic, slower path** is used; RCCL and P2P could help — **you did not test them**. On top of that, two cards on x4 (§2.3).
2. **The calculation from §8.2 does not fully explain your numbers.** The overhead of the collectives alone (0.9–3.4 ms) accounts for at most ~3 of the 34 ms. The difference between the modes is 39.7 − 34.4 = 5.3 ms, and the ideal gain from fourfold throughput is 7.9 − 2.0 = 5.9 ms *(my calculation, substitute 3 bpw)*. It looks as if tensor split recovered almost the entire "throughput" part, and the rest (~30 ms per token) **did not depend on memory throughput** — e.g. per-layer fixed costs: kernel launches, synchronizations, MoE routing, unpacking IQ quantized weights. This is a **hypothesis**; the notes contain no profile that would settle it.
3. **Draft helps more when the step is "expensive and fixed":** ×1.5 in layer split and ×1.6 in tensor split (25.2 → 37.9; 29.1 → 46.2); both mechanisms together ×1.8 relative to 25.2 (journal). When most of the step time is a cost independent of the number of tokens, verifying 4 tokens costs little more than verifying one — exactly the condition on which speculation rests (§9). Your journal: the two mechanisms multiply, because a faster step makes verifying a larger batch relatively cheaper.
4. **The price in prefill:** ~960 → ~700 tok/s (−27%) and 2 slots of 98,304 instead of 4 of 131,072. §8.2 predicted a communication overhead of 10–25% on an x16 link; I did not separate how much of the −27% is communication and how much is the smaller micro-batch *(unverified)*.

**How to measure better:** calibrate kernel efficiency on a small dense model that fits on a single card (`llama-bench -p 0 -n 128`; weight bytes from the file size; 640 GB/s *(third-party source)*) — you will get a correction factor for the ceilings from §2; only then is the difference to DeepSeek interpretable.

> **Check it yourself (8)**
> ```bash
> sed -n 1288,1324p ~/llama.cpp-0ce8cd1/src/llama-arch.cpp     # list of architectures without tensor split mode
> grep -n -i "RCCL\|P2P\|tensor" ~/llama.cpp-0ce8cd1/docs/multi-gpu.md | head -30
> sed -n 517,546p ~/llama.cpp-0ce8cd1/src/llama-context.cpp    # conditions for a true pipeline
> ```
> Exercise: check whether your model is **not** on the exclusion list; then, with the measurements from §8.4 in hand, write down three hypotheses about the source of the ~30 ms of "fixed" time per token and, for each, one read-only inspection/measurement that would confirm or refute it.
## 9. Speculative decoding

### 9.1 Idea and guarantee

A cheap *guesser* (*draft*) proposes k tokens; the target model evaluates k+1 positions in a **single** pass (cost close to one step, as long as it is memory-bound); we accept the longest matching prefix plus one target token. Leviathan et al. (arXiv 2211.17192): 2–3× on T5-XXL "with byte-identical results"; Chen et al. (arXiv 2302.01318): "a modified rejection scheme, preserving the target model's distribution" *(authors' own claim)*. The guarantee concerns the *distribution*; with greedy decoding — token by token. llama.cpp implements the rejection scheme (`common_sampler_sample_and_accept_n_rejection`, `common/sampling.cpp`) and documents synthetic acceptance tests (`--spec-synth-rates`, `--spec-synth-len`; `docs/speculative.md`).

### 9.2 Acceptance arithmetic

Assume each guessed token is accepted independently with probability α (idealization). Expected number of tokens per target-model pass with k guessed tokens:

> **E[tokens] = (1 − α^(k+1)) / (1 − α)** (= 1 + α + … + α^k; formula from the Leviathan paper — unverified from the text, but it is a geometric sum I derived myself)
>
> **speedup = E[tokens] / (1 + c·k)**, c = guesser step time / target-model step time (with verification costing as much as a regular step — dense model, memory-bound)

| α \ k | 1 | 2 | 3 | 4 | 5 | 7 | 15 |
|---|---|---|---|---|---|---|---|
| 0.5 | 1.50 | 1.75 | 1.88 | 1.94 | 1.97 | 1.99 | 2.00 |
| 0.7 | 1.70 | 2.19 | 2.53 | 2.77 | 2.94 | 3.14 | 3.32 |
| 0.8 | 1.80 | 2.44 | 2.95 | 3.36 | 3.69 | 4.16 | 4.86 |
| 0.9 | 1.90 | 2.71 | 3.44 | 4.10 | 4.69 | 5.70 | 8.15 |

*(E[tokens] values: my calculation)*

**Example 1** (cheap guesser): α = 0.8, c = 0.05, k = 4: 3.36 / (1 + 0.2) = **2.80**; for k = 1…7: 1.71 / 2.22 / 2.57 / 2.80 / 2.95 / 3.08 (k = 1, 2, 3, 4, 5, 7). **Example 2** (more expensive): α = 0.8, c = 0.2: 1.50 / 1.74 / 1.85 / 1.87 / 1.84 / 1.73 — maximum at k = 4, then decline. Conclusions: gains **saturate** in k, and the guesser cost c determines the optimal k.

**A note on terminology:** llama.cpp prints "draft acceptance rate = accepted/generated" (per guessed token, conditional on position and truncation) — this is **not** the idealized α. `--spec-synth-len L` defines L = the mean accepted length including the target token and solves p + p² + … + p^K = L − 1 (L = 3, K = 7 gives p = 0.68 *(my calculation)*).

**Example 3: reversing the math on your data.** Measured speedup at k = 3 is ×1.5–1.6. With an *assumed* (not measured) c = 0.05 and verification overhead r = 1.2: E / (r + c·k) = 1.55 ⇒ E ≈ 1.55 × 1.35 ≈ 2.1 ⇒ α ≈ 0.6 (E(0.6; 3) = 2.18; E(0.55; 3) = 2.02) *(example of a method for extracting α from a measurement, not a measurement of your α)*.

### 9.3 MoE penalty

From §4.2: verifying n = k+1 tokens reads 1.47× / 1.93× / 2.38× / 2.82× / 3.25× / 4.07× the bytes of a single token (n = 2, 3, 4, 5, 6, 8). Net gain = E[tokens] / (byte ratio), without draft cost *(my calculation; uniform routing)*:

| α \ k | 1 | 2 | 3 | 4 | 5 | 7 |
|---|---|---|---|---|---|---|
| 0.6 | 1.09 | 1.02 | 0.92 | 0.82 | 0.74 | 0.60 |
| 0.7 | 1.16 | 1.14 | 1.07 | 0.99 | 0.91 | 0.77 |
| 0.8 | 1.22 | 1.27 | 1.24 | 1.19 | 1.14 | 1.02 |
| 0.9 | 1.29 | 1.41 | 1.45 | 1.45 | 1.45 | 1.40 |

With α = 0.8, k = 4 a **dense** model gives ×3.36, while MoE with uniform routing gives ×1.19. Real routing is correlated between adjacent tokens, so reality lies **between** the tables *(unverified)*. This is a likely explanation for the modest gains on large sparse MoEs and the reason DSpark/MTP for the V4 class use **short** drafts (ds4: up to 5 tokens) and confidence truncation (ds4 threshold for a single Spark of 0.4).
### 9.4 Family of methods

| method | where the draft comes from | llama.cpp (this build) | vLLM / SGLang (these trees) |
|---|---|---|---|
| **model-guesser** | small LM of the same family | `--spec-type draft-simple`, `-md` | `draft_model` / `STANDALONE` |
| **Medusa** (arXiv 2401.10774: >2.2× and 2.3–3.6× *(authors' own claim)*) | extra heads on the target model, tree attention | **not found by me** (grep) | **not found by me** |
| **EAGLE-1/2/3** (arXiv 2401.15077, 2406.16858, 2503.01840: up to 6.5× in version 3 *(authors' own claim)*) | autoregression at the *feature* level; version 2 — dynamic tree; version 3 — features of multiple layers | only `draft-eagle3` (checkpoints: Llama 3.x, Qwen3, gpt-oss, Gemma-4) | `eagle`, `eagle3` / `EAGLE`, `EAGLE3` |
| **Lookahead** (arXiv 2402.02057) | Jacobi iteration + n-gram pool | `examples/lookahead` | — |
| **n-gram / prompt lookup** | copies continuations previously seen in the context (code, RAG, summarization) | `ngram-simple`, `-map-k`, `-map-k4v`, `ngram-mod` (pool ~16 MB, shared across slots), `ngram-cache`; `--spec-default` = ngram-mod | `ngram`, `suffix` / `NGRAM` |
| **MTP heads** | the model was trained to predict subsequent tokens (V4: `num_nextn_predict_layers: 1`) | `draft-mtp` | many `*_mtp` types / `FROZEN_KV_MTP` |
| **DFlash** | block diffusion guesser: a whole token block in **one** pass, conditioned on the target's hidden states; "up to 6× lossless on Qwen3-8B" *(project's own claim)* | `draft-dflash` (merged 2026-06-28, PR #22105) | `dflash` / `DFLASH` |
| **DSpark** | DFlash + low-rank "Markov head" (block sampled left-to-right in a single graph) + optional confidence head (`--spec-draft-conf-min`) | `draft-dspark` (merged 2026-07-28, PR #25173) | `dspark` / `DSPARK` |

**Corrections to associations.** **DSpark is not an acronym from someone else's fork**: in llama.cpp it is "DFlash + Markov head"; checkpoints are in the Hugging Face organization `deepseek-ai` (`deepseek-ai/dspark_qwen3_{4b,8b,14b}_block7`, `docs/speculative.md`). The PR text (author `wjinxu`) describes it as "DeepSeek + PKU, 2026, 'Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation'" — that the PR says so is verified, I did not download the paper itself *(unverified bibliographic data)*. **DFlash** = "Block Diffusion for Flash Speculative Decoding" (Chen, Liang, Liu; arXiv 2602.06036, ICML 2026; per the z-lab.ai page). Medusa: "not found by grep" in llama.cpp, vLLM, and SGLang; older versions may have had it. **Discrepancy:** the llama.cpp documentation in this tree talks about DSpark with the bare Qwen3 skeleton, while your log describes a DSpark head from the V4-Flash-0731 checkpoint converted to GGUF — I did not settle who is right in the details *(unverified)*.

### 9.5 Measured gains (the PR authors' — not yours)

PR #25173 authors, one RTX 4090, Qwen3-8B bf16, greedy, `--spec-draft-n-max 7` *(project's own claim)*: DSpark **1.88×** over no speculation (DFlash 1.55×) on the "qualitative" subset of SPEED-Bench; geometric mean 3.35× vs. 2.89× on GSM8K/MATH500/HumanEval/MBPP/MT-Bench; less for quantized targets (Q4_K_M: 1.81× vs. 1.54×). PR #22105: Qwen3.6-27B Q4_K_M on DGX Spark 2.69×, but **gpt-oss-20B 0.61–1.27× (often a slowdown)** *(project's own claim)*. Lesson: the gain depends on task predictability (code/RAG high, open chat low), on target precision, and — for MoE — on verification cost. **These are numbers from different hardware and model; do not mix them with yours** (§14).

Yours: 23.5 → 35.2 (×1.50, old build), 25.2 → 37.9 (×1.50) and 29.1 → 46.2 (×1.59) on the new one — V4-Flash with DSpark of length 3. It fits within the PR's range, although it is an MoE with quantized weights; without measuring α and routing behavior I cannot settle *why*.

> **Check it yourself (9)**
> ```bash
> less ~/llama.cpp-0ce8cd1/docs/speculative.md        # types, statistics, --spec-synth-*
> grep -n "spec-type\|draft-dspark\|draft-dflash\|draft-mtp\|ngram" ~/llama.cpp-0ce8cd1/common/arg.cpp | head -30
> grep -n "sample_and_accept_n_rejection" ~/llama.cpp-0ce8cd1/common/sampling.cpp
> ```
> Arithmetic exercise: for α = 0.75 and c = 0.1, find the k maximizing E/(1+ck) (k = 1…8). Repeat for an MoE with the denominator (byte ratio from §4.2) + c·k and compare the optimal k. What does that say about choosing `--spec-draft-n-max` for V4-Flash?

---
## 10. Sampling

The network returns **logits** (one per vocabulary position). The **sampler chain** transforms the candidate array and selects a token. The default order in llama.cpp (`common_params_sampling::samplers`, `common/common.h`):

> **penalties → DRY → top-n-sigma → top-k → typical-p → top-p → min-p → XTC → temperature → (at the end) random or greedy selection**

Default values (`common/common.h`): temperature 0.8; top-k 40; top-p 0.95; min-p 0.05; XTC, DRY (multiplier 0, base 1.75, allowed length 2) and Mirostat disabled. Since truncation happens *before* temperature, temperature operates on the already narrowed set.

**Temperature example** *(my calculation)*: logits (2, 1, 0). T = 1 → (0.665; 0.245; 0.090). T = 0.5 (logits (4, 2, 0)) → (0.867; 0.117; 0.016) — sharper. T = 2 → (0.506; 0.307; 0.186) — flatter. T → 0 is greedy selection. **Min-p example:** with min-p = 0.2 and a distribution from T = 1, the threshold is 0.2 × 0.665 = 0.133; the first two tokens remain; with min-p = 0.05 (threshold 0.033) all three remain.

One line on each knob:

- **Greedy**: argmax of z. **Temperature**: p_i = softmax(z_i / T).
- **Top-k**: the k highest. **Top-p / nucleus** (Holtzman et al., ICLR 2020, arXiv 1904.09751): the smallest set with cumulative mass ≥ p.
- **Min-p** (Nguyen et al., ICLR 2025, arXiv 2407.01082): tokens with p_i ≥ min_p × p_max — "adapts the threshold to the model's confidence".
- **Typical-p** (Meister et al., TACL 2022, arXiv 2202.00666): tokens whose information content −log p_i is closest to the distribution's entropy *(rule from the text, unverified)*.
- **Mirostat** (Basu et al., arXiv 2007.14966): a regulator that tunes truncation so that output entropy tracks a target τ *(formula unverified)*; in llama.cpp v1 and v2.
- **Top-n-sigma** (Tang et al., arXiv 2411.07641): on raw logits, keep z_i ≥ z_max − n·σ(z) — a stable space regardless of temperature *(formula from memory)*.
- **XTC** (*Exclude Top Choices*; p-e-w, PR #6335 in text-generation-webui): with probability P, when ≥ 2 tokens have p ≥ threshold, remove all except the **least** probable (`llama_sample_xtc_apply`; inactive when threshold > 0.5).
- **DRY** (p-e-w, PR #5677): if a token extends a sequence that has already occurred (length n ≥ allowed), subtract **multiplier × base^(n − allowed_length)** from the logit; separators (newline, quotes…) reset the match.
- **Repetition/frequency/presence penalties** over the last `penalty_last_n` tokens. **Adaptive-P**: a new sampler steering the selected token's probability toward a target value with an EMA history *(algorithm unverified)*.
- **Logit bias, grammar, and the reasoning budget** are also samplers in the chain. The budget (`common/reasoning-budget.{h,cpp}`) is an automaton IDLE → COUNTING → WAITING_UTF8 → FORCING → DONE: once the "thinking" budget is exhausted, it forces the thinking block closed by setting other logits to −∞.
- GGUF can carry **recommended sampling parameters** (`general.sampling.top_k/top_p/min_p/temp/…`; `gguf-py/gguf/constants.py`) — for the format: chapter 03.
- **Backend sampling** (`--backend-sampling`): incompatible with grammars, the reasoning budget, and tensor split.

> **Check it yourself (10)**
> ```bash
> sed -n 225,280p ~/llama.cpp-0ce8cd1/common/common.h          # sampler order and default values
> sed -n 1,60p ~/llama.cpp-0ce8cd1/common/reasoning-budget.h   # reasoning budget automaton
> sed -n 30,48p ~/llama.cpp-0ce8cd1/gguf-py/gguf/constants.py  # GGUF keys for sampling
> ```
> Exercise: for logits (3, 2, 1, 0), compute the distribution at T = 0.7, apply top-p = 0.9 and rescale; how many tokens remain? Repeat in reverse order (top-p first, then T) — the result differs; that is why the order is part of the specification.
## 11. Grammar and tool calling

### 11.1 How the token mask is computed

Goal: guarantee that the output matches a regex / JSON schema / grammar. At each step, compute the set of tokens that keep the output a valid prefix, set the logits of the rest to −∞, and only then sample. The difficulty: tokens are byte strings that cut across terminal boundaries, and the vocabulary has 100–250 thousand entries.

- **GBNF in llama.cpp** (`src/llama-grammar.cpp`, 1530 lines; JSON Schema → GBNF in `common/json-schema-to-grammar.cpp`): rules are compiled into a **pushdown automaton**; the environment keeps a *list of stacks* (all states consistent with the text). `llama_grammar_apply_impl`: for each candidate it decodes the UTF-8 fragment and checks it against every stack — work on the order of the vocabulary size per step, on CPU. Mitigation in `common_sampler_sample`: if `grammar_first` is not set, llama.cpp **first samples without the grammar and checks only the sampled token; only when it is invalid does it apply the full mask** — the typical case costs a single check. There are also **lazy grammars** (trigger tokens/patterns): the grammar sleeps until the model emits e.g. the opening of a tool call, so free text remains unconstrained.
- **llguidance** (optionally `-DLLAMA_LLGUIDANCE=ON`, requires Rust): "token mask for the llama3 tokenizer (128 thousand) takes on average 50 µs on one core, p99 0.5 ms" *(project's own claim)*. Grammars with `%llguidance` go to it.
- **xgrammar** (arXiv 2411.15100): *context-independent* tokens have their mask precomputed per automaton state; only *context-dependent* ones are checked at runtime; "up to 100× speedup" *(authors' own claim)*. Default backend in vLLM and SGLang (`backend: "auto"`; also `outlines`, `lm_format_enforcer`, `llguidance`).
- **Outlines** (arXiv 2307.09702): regex/CFG → finite automaton and a **vocabulary index** (state → allowed tokens), so the mask is a vocabulary lookup. SGLang adds *jump-forward*: when the grammar forces an unambiguous continuation, it emits it without sampling.

### 11.2 Why this matters in agents

Tool arguments must be parseable JSON; a single broken call breaks the loop. vLLM: `tool_choice` with a named function and `required` **always** use structural constraints; `auto` uses a model-specific parser on free text, and the grammar only kicks in for `strict: true` or with `--tool-strict-level`; "with `tool_choice="auto"` the model generates calls without any grammar and a corrupted tag can leak into the response" (`docs/features/tool_calling.md`). The first use of a schema pays the compilation cost ("a few seconds"). In vLLM the mask only takes effect after reasoning has finished. Grammar + speculation is delicate: llama.cpp renormalizes the rest of the distribution after masking.

**Cost** *(my inference)*: grammar can *change quality* — it pushes the model onto paths it would not have chosen; forcing `{` as the first character can suppress reasoning. Leave reasoning outside the constrained part.

### 11.3 End-to-end mechanics

1. The client sends `tools=[{name, description, JSON Schema}]` and messages. 2. The server renders the **chat template** (§12) with the `tools` variable. 3. The model generates text with the call in *its own* wire format (Hermes `<tool_call>{json}</tool_call>`, Mistral `[TOOL_CALLS]`, Harmony in gpt-oss, XML in Qwen3-Coder, DeepSeek's DSML…). 4. The server **parses** it into `tool_calls` (name + JSON string), with streaming support, and separates reasoning. 5. The client executes the tool, sends back `role: tool`, loop.

- **vLLM**: parser per family (`--tool-call-parser` with `--enable-auto-tool-choice`; ~60 files in `vllm/tool_parsers/`) and reasoning parsers (`--reasoning-parser`, ~40). **Wrong parser name = calls come back as plain text.**
- **llama.cpp**: `--jinja` (enabled by default) uses its own Jinja engine in C++ (`common/jinja/`, "input marking" so user text cannot inject special tokens). Then either a **hand-written parser per model** (`common/parsers/*.cpp`: deepseek, gpt-oss, qwen3-coder, kimi, gemma4, minimax…), or the **auto-parser** (`common/chat-diff-analyzer.cpp`): analyzes the template *differentially* ("inspired by git diff": renders with and without tools, with and without reasoning), detects markers and builds a **PEG parser** and optionally a (lazy) GBNF grammar (`docs/autoparser.md`). Unknown template ⇒ generic JSON variant, more expensive in tokens and less reliable.
- **Constraint:** JSON-schema, tool grammars and the reasoning budget are CPU samplers; they work with ROCm, but force a **GPU → CPU sync at every token** (`llama_synchronize` in `common_sampler_sample`).

> **Check it yourself (11)**
> ```bash
> sed -n 606,690p ~/llama.cpp-0ce8cd1/common/sampling.cpp         # sample first, then check
> grep -n "lazy\|awaiting_trigger" ~/llama.cpp-0ce8cd1/src/llama-grammar.cpp | head
> less ~/llama.cpp-0ce8cd1/docs/autoparser.md
> ls ~/runtimes-src/vllm/vllm/tool_parsers | head -80
> ```
> Exercise: in vLLM's `docs/features/tool_calling.md`, list which `tool_choice` values give a syntax guarantee; for an agent working for hours unattended, pick one and name the latency cost.
## 12. Chat templates and reasoning parsers

A chat model was trained on the **textual serialization** of conversations with role markers and special tokens (`<|im_start|>user`, `[INST]`, `<|start|>assistant<|channel|>`…). The template ships with the model as **Jinja2** (`tokenizer_config.json: chat_template`; GGUF: `tokenizer.chat_template`). The runtime must reproduce it **byte for byte**, because the model has not seen any other wrapper.

**Silent failure modes** *(my inference from the code and general knowledge; each degrades quality without an error)*:

1. **Mismatched template** (role markers the model does not know).
2. **Double BOS**: GGUF has `add_bos_token = true`, and the prompt also starts with `<bos>`; llama.cpp logs "…So now the final prompt starts with 2 BOS tokens" (`src/llama-vocab.cpp`).
3. **Missing generation prompt** — the model continues the *user turn*.
4. **System role handling** (templates that drop or lose it).
5. **Tools in a different format** than in training, or a parser mismatched to the model.
6. **Reasoning in history**: templates that cut out ` thinking` blocks versus those that keep them; llama.cpp defaults to `preserve_reasoning` and has the `--reasoning on|off|auto`, `--reasoning-format` flags.
7. **EOS vs EOT**: the end-of-turn token (`<|im_end|>`, `<|eot_id|>`) is not the end of text; a wrong stop token = endless generation.
8. **Injection via tokenization**: user text containing the name of a special token gets replaced with a control token (hence "input marking").

Why "silently": the model still produces fluent text, just in a mode it was not trained on. **Especially dangerous when comparing runtimes**: two programs with a different template for "the same" model measure the template, not the engine.

**Not every model has Jinja.** DeepSeek-V4 "does not include a chat template in Jinja format"; one must "refer to the `encoding_dsv4.py` script" (model card). That is why ds4 has a renderer natively in C; llama.cpp also keeps a hardcoded legacy list of ~56 formats (`src/llama-chat.cpp`) in case Jinja is disabled.

**Reasoning parsers.** "Thinking" models emit a reasoning chain inside delimiters (` thinking… response`, Harmony channels). The server splits it into `reasoning_content` (llama.cpp, `--reasoning-format deepseek`) or `reasoning` (vLLM — the field was **renamed from `reasoning_content`**, the old key is accepted on input as an alias; `--reasoning-parser <name>`) and `content`. Interaction: **the grammar must start after reasoning finishes**. DeepSeek-V4 reasoning modes: Non-think / High / Max (Max requires context ≥ 384K), selected by the prompt renderer; ds4 documents that "changing the level mid-conversation rebuilds its cached prefix" — *a different mode = a different prefix = no cache hit* (§5.2).

> **Check it yourself (12)**
> ```bash
> grep -n "2 BOS tokens" ~/llama.cpp-0ce8cd1/src/llama-vocab.cpp
> grep -n "reasoning_content\|reasoning-format" ~/llama.cpp-0ce8cd1/common/arg.cpp | head
> grep -n "reasoning_content" ~/runtimes-src/vllm/vllm/entrypoints/openai/chat_completion/protocol.py | head
> ```
> Exercise (not run by me): download your model's `tokenizer_config.json`, render `chat_template` by hand (`python3` + `jinja2`) for one user message, and compare the bytes with the prompt in the server log, including the final assistant header.

---
## 13. Determinism and numerics

- **Floating-point addition is not associative**: (a + b) + c ≠ a + (b + c). Any change in the *reduction order* changes the last bits: different kernels (split-K, tiles, WMMA vs scalar), different batch shapes, a different number of cards in all-reduce, a different backend, a different layout of quantization blocks.
- Small logit differences matter: argmax jumps when two tokens are within noise range, and continuations diverge; with sampling, the same seed picks different tokens. llama.cpp documentation: "a fixed seed gives repeatable random draws, but stochastic sampling of CPU and backend may still pick different tokens... Use greedy sampling when exact matching is needed" (`docs/speculative.md`).
- **The real culprit in servers is the lack of batch invariance.** Horace He / Thinking Machines (September 2025): 1000 identical Qwen3-235B responses at T = 0 produced **80 different results** (identical for the first 102 tokens); cause: kernels whose reduction strategy depends on batch size, plus nondeterministic server load; fix: invariant kernels at ~2× slowdown *(authors' own claim, blog post)*. vLLM has `VLLM_BATCH_INVARIANT` (beta; **only** NVIDIA cc ≥ 8.0, AMD Instinct gfx90a/942/950 and Intel XPU — **not** RDNA4; `docs/features/batch_invariance.md`), SGLang `srt/batch_invariant_ops/`.

**Consequences** *(my inference from the mechanism)*: (1) the same prompt with `-np 1` vs `-np 4`, with or without speculation, with or without KV quantization, or after hitting the prefix cache **may give a different result**; (2) llama.cpp, vLLM and MLX differ even at T = 0; (3) speculation is lossless *in distribution*, not bitwise — **your log confirms it**: at T = 0, tensor split gave responses identical to the old ones 0 out of 4 times, layer split with draft 2 out of 4; the responses you read were correct, but you did not measure quality ([`README.md`](../speeding-up-generation/README.md)); (4) the proper cross-runtime test is **statistical**: perplexity / KL divergence on a fixed text or task accuracy with confidence intervals (`tools/perplexity`, `tools/imatrix` exist; the KL-mode flag unverified); (5) quantization differences are much larger than kernel noise *(orders of magnitude unverified)* — "the same model" means "numerically the same" only with the same quantization and a measured quality difference (chapter 03).

> **Check it yourself (13)**
> ```bash
> grep -n -i "seed\|different tokens\|greedy" ~/llama.cpp-0ce8cd1/docs/speculative.md | head
> sed -n 1,40p ~/runtimes-src/vllm/docs/features/batch_invariance.md      # list of supported GPUs
> ```
> Exercise (not run by me; **the cards are production**): send the same short request at T = 0 three times to the server with one client, then three times while a second client works in parallel. If the responses diverge — you have your own proof of batch non-invariance, not a server bug.

---

## 14. How to measure fairly

| name | definition |
|---|---|
| **prefill (pp)** | prompt tokens / prefill time |
| **decoding (tg)** | generated tokens / decoding time (without prefill) |
| **end-to-end** | generated tokens / (TTFT + decoding time) — drops sharply with long prompts |
| **TTFT** | queue time + prefill (+ first step) |
| **ITL** | interval between consecutive streamed tokens |
| **TPOT** | (end-to-end latency − TTFT) / (output length − 1) |
| **goodput** | throughput of requests meeting the TTFT/TPOT SLO (DistServe metric) |

ITL and TPOT are the definitions computed by vLLM's `benchmarks/serve.py` (`mean/median/p* ttft_ms, tpot_ms, itl_ms`, `request_goodput`).

**Per stream vs aggregate.** With B streams, aggregate tok/s is the sum, and per-stream speed usually drops. §4.2: at B = 8 aggregate 249, per stream 31, vs 126 at B = 1 *(my calculation)*. In your case: 1 agent 49.7; 2 agents 34.5 each (63 total). **Always report the concurrency.**

**With and without speculation.** Speculation changes tg; report the draft acceptance rate and task type, compare against a no-speculation baseline **on the same prompts** (`tools/server/bench/speed-bench` in llama.cpp runs both passes with per-category gain). Your deployed per-task results (T = 0): translation 51.9; tool call 62.0; code 58.5; prose 37.8 tok/s — ×1.6 difference *from task type alone*.

**Context depth.** tg drops with KV length; `llama-bench -d N` pre-fills N tokens; report for several depths (0, 8k, 32k).

**Why `llama-bench` ≠ llama-server.** `llama-bench` measures `pp` (`-p`) and `tg` (`-n`) of a single sequence through `llama_decode` with fixed `n_batch/n_ubatch`, `-r 5` repetitions: no HTTP, template, sampler chain, prompt cache or slot scheduling. llama-server adds HTTP/JSON, tokenization, samplers (CPU sync on every token), grammar/tool parsing, prompt cache, slot checkpoints, `--parallel`, and reports its own `timings` (`prompt_per_second`, `predicted_per_second`; `server-common.cpp`). Usually tg from `llama-bench` ≥ server tg by a few percent *(unverified)*.

**Runtime comparison checklist**

1. **Pin** hardware, driver/ROCm, weight *lineage*, context, concurrency, prompt set (same token counts), output length (`ignore_eos`/`min_tokens`), sampling parameters (greedy for speed, §13).
2. **The same quantization across formats is impossible**: GGUF Q4_K_M ≠ AWQ-INT4 ≠ MLX 4-bit g64 ≠ FP8; effective bits per weight differ. Compare **quality-matched** points: measure the quality of each variant (perplexity/KL vs BF16 + 1–2 task tests with large n) and compare speed at equal quality, or draw a speed–quality frontier. Also compare **bytes per weight**, because speed ≈ bandwidth / bytes (§2).
3. **Warm up** (JIT/autotuning, CUDA graphs, page cache, first `mmap` access); ≥ 5 repetitions, mean ± deviation, p50/p95; **disable** prefix caching when measuring prefill, and measure *separately* with it enabled (agents live on cache hits).
4. **Do not mix settings:** a number from a PR on an RTX 4090 in bf16 (§9.5) is not a number for an R9700 at Q3. Every number carries (hardware, runtime + build, model + quantization, concurrency, context, date).
5. **Authors' own benchmarks** *(project's own claim)*: all PR tables in this chapter are their runs.
**Your protocol against this backdrop:** the average of 4 tasks × 2 temperatures, one agent, build pinned to SHA `0ce8cd1`, a 2×2 matrix — solid speed *on that single machine*. What is missing (and you say so yourself) is a **quality measurement** and an α measurement. Before you compare llama.cpp with vLLM on the same DeepSeek, remember point 2.

> **Check it yourself (14)**
> ```bash
> sed -n 630,650p ~/runtimes-src/vllm/vllm/benchmarks/serve.py       # TPOT / ITL / goodput
> sed -n 80,110p ~/llama.cpp-0ce8cd1/tools/llama-bench/README.md      # -p, -n, -d, -r
> sed -n 85,100p ~/llama.cpp-0ce8cd1/tools/server/server-common.cpp   # server timings fields
> ```
> Exercise (not run by me): from the `timings` field of a single `llama-server` response, manually calculate the tok/s for prefill, decoding, and end-to-end. Which one goes up and which one goes down when you lengthen the prompt from 1k to 20k tokens?

---

## 15. What this means for me

1. **Decoding speed ≈ bandwidth / bytes of active weights.** Your ~50 tok/s is well below the ceiling from §2 — I could not establish the cause (§8.4). Calibrate the kernels first on a small dense model.
2. **MoE does not scale linearly with the number of agents** (§4): the second agent gave +27% collectively (63 vs 49.7). Set the number of slots by measurement; in your case 2 × 98,304 worked best.
3. **Speculation on MoE works, but the gain is smaller than on dense models** and depends on the task (§9): in your case ×1.5–1.6, from ~38 (prose) to 62 tok/s (tool call).
4. **Tensor mode** is experimental, requires unquantized KV and `-fa on`, is excluded for many architectures (§8.3), and costs prefill (~960 → ~700 tok/s). For agents reading long tool results, that is a real cost — I did not measure the prefill/decoding ratio in your tasks *(unverified)*.
5. **Prefix caching is lever #1 for agents** (§5.2): check `--cache-ram` (default 8 GiB), `--slot-prompt-similarity`, `--cache-reuse`, `--ctx-checkpoints`. Changing the reasoning mode or template between turns invalidates the prefix (§12).
6. **The template and parser are part of the model configuration** (§12): with every new model, check the template, stop tokens, tool parser, and reasoning field — an error gives no message, only a worse model.
7. **Tool calls:** grammar increases reliability at the cost of CPU and per-token synchronization (§11); lazy grammars save this in free text.
8. **Measure fairly** (§14): concurrency, context depth, baseline without speculation, quality alongside speed. The gap is quality.
9. **Mac:** counterparts of the mechanisms from this chapter in mlx-lm (`PromptTrie`/`LRUPromptCache`, `RotatingKVCache`, `QuantizedKVCache`, `--draft-model`, `BatchGenerator`) — chapter [`07`](07-APPLE-MLX-OMLX-AND-DS4.md). The unified memory bandwidth of the Mac is a different input number for the same calculation from §2 (I do not give its values here).
10. **Next:** files and quantization — [`03`](03-QUANTIZATION-AND-FORMATS.md); the engine you know — [`04`](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md); server alternatives — [`06`](06-SERVING-ENGINES-VLLM-SGLANG.md); choosing — [`09`](09-COMPARISON-AND-CHOICE.md); speculation and tensor split in your setup — [`../speeding-up-generation/01-JAK-TO-DZIALA.md`](../speeding-up-generation/01-JAK-TO-DZIALA.md).

---
## 16. What I could not establish

1. **Official R9700 specs** (bandwidth, TFLOPS): I could not fetch the AMD pages; 640 GB/s comes from third-party data and my calculation, 96 TFLOPS — unverified. All ceilings in §2 depend on them.
2. **PCIe topology:** sysfs reports x16 on four cards, your log — that cards 1 and 3 are at x4; the CPU has ~28 lanes. `lspci -vv` will settle it.
3. **Whether P2P works and whether RCCL would help** — not tested by me; the log does not cover it either.
4. **Where the ~30 ms constant per-token time comes from** (§8.4) — hypotheses without a profile. **True α acceptance rate** and V4-Flash routing skew — not measured.
5. **Whether AITER kernels work and are fast on gfx1201** — the code shows RDNA flags, not results.
6. **DSpark discrepancy:** llama.cpp docs (Qwen3 skeleton) vs. your log (head from V4-Flash-0731).
7. **V4-Flash KV:** ~6.9 KB/token rests on assumptions from §3.1; "6.4" vs. "6.7 GiB" at 1M depends on whether 1M is 10⁶ or 2²⁰.
8. **Formulas from paper bodies** (FlashAttention I/O bound, Leviathan Thm. 3.8, top-n-sigma threshold, typical rule, Mirostat update) — I read only abstracts; **Prompt Lookup Decoding, flash-decoding, Williams (roofline), Vaswani** — from memory. **The DSpark paper** and **the arXiv DFlash page** — not downloaded. **Medusa** — "not found by grep". **ONNX** and MLX quant storage — not investigated (chapter 03).

---

## 17. Glossary

Polish term · English · one line (thematic order).

| Polish term | English | one line |
|---|---|---|
| autoregresywny | autoregressive | each token depends on all previous ones; generation is inherently sequential |
| prefill, czytanie promptu | prefill / prompt processing (pp) | first pass over prompt tokens at once; compute-bound |
| dekodowanie | decode / token generation (tg) | one-token-at-a-time phase; memory-bandwidth-bound |
| pamięć podręczna KV | KV cache | stored attention keys and values of all tokens so far |
| intensywność arytmetyczna | arithmetic intensity | FLOP per byte from memory; decides whether a kernel is memory- or compute-bound |
| roofline / punkt załamania | roofline / ridge point | speed = min(peak FLOPS, AI × bandwidth); ridge point is where they meet |
| MFU | model FLOPs utilisation | achieved FLOPS divided by peak |
| czas do pierwszego tokenu | TTFT | queue time + prefill |
| opóźnienie między tokenami / czas na token | ITL / TPOT | interval between successive tokens in the decode phase |
| goodput | goodput | throughput of only the requests that met latency SLOs |
| MHA / MQA / GQA | multi-head / multi-query / grouped-query attention | attention with many / one / several K-V heads |
| MLA | multi-head latent attention | (DeepSeek) cache holds a low-dimensional latent vector instead of full K/V |
| DSA | DeepSeek Sparse Attention | indexer selects top-k tokens to attend to |
| CSA / HCA | compressed / heavily compressed attention | (DeepSeek-V4) KV compression along the time axis |
| SWA / iSWA | sliding-window / interleaved SWA | attention only to the last W tokens / interleaving of window and global layers |
| RoPE | rotary position embedding | rotates Q/K pairs by a position-dependent angle; dot product depends on relative distance |
| YaRN | YaRN | method for scaling RoPE to extend context |
| RMSNorm | RMSNorm | normalization by root mean square, without subtracting the mean |
| SwiGLU | SwiGLU | gated FFN: W_down(SiLU(W_gate x) ⊙ W_up x) |
| eksperci (MoE) | mixture of experts | router sends a token to top-k of many small FFNs |
| ekspert wspólny | shared expert | expert always active alongside routed ones |
| parametry aktywne a łączne | active vs total parameters | active = bytes/FLOP per token; total = memory footprint |
| logity / softmax | logits / softmax | raw scores for the vocabulary / normalization to probabilities |
| łańcuch samplerów | sampler chain | ordered logit transforms and final selection |
| min-p / top-p / top-k | min-p / top-p / top-k | truncation relative to max / by cumulative mass / by count |
| XTC / DRY / Mirostat | XTC / DRY / Mirostat | drop best choices / penalty for repeated strings / target-entropy regulator |
| dekodowanie z gramatyką | grammar-constrained decoding (GBNF, xgrammar, llguidance, Outlines) | logit masking so the output stays in a formal language |
| maska tokenów | token mask / bitmask | set of allowed token IDs at a given step |
| wywoływanie narzędzi | tool calling | model emits a structured call, server parses it into `tool_calls` |
| szablon czatu | chat template (Jinja) | model-specific serialization of messages and tools, shipped with the model |
| BOS / EOS / EOT | BOS / EOS / EOT | beginning-of-sequence / end-of-sequence / end-of-turn tokens |
| parser rozumowania | reasoning parser | separates thinking text from the answer (`reasoning_content` / `reasoning`) |
| PagedAttention | PagedAttention | KV in blocks with a block table, like memory paging |
| prefix caching / RadixAttention | prefix caching / RadixAttention | reuse of KV for a shared prompt prefix (hash chain / radix tree) |
| przesunięcie kontekstu | context shift | window sliding by dropping the middle and re-rotating keys |
| slot | slot (llama.cpp) | concurrent server sequence with its own state, sampler, and prompt; count = `-np` |
| zunifikowane KV | unified KV | one shared KV-cell pool instead of fixed per-slot streams |
| ciągłe batchowanie | continuous batching | batch composition decided each iteration; sequences join and leave (Orca) |
| chunked prefill | chunked prefill | splitting long prompts into chunks mixed with decoding to avoid stalls |
| dezagregacja prefill/decode | prefill/decode disaggregation | separate GPU pools for the two phases, KV transferred between them |
| FlashAttention | FlashAttention | tiled, I/O-aware, exact attention with online softmax |
| podział tensorowy / warstwowy / ekspertowy / danych | tensor / pipeline / expert / data parallelism | splitting within layers / across layers / across experts / across replicas |
| all-reduce | all-reduce (NCCL / RCCL) | collective that sums tensors across cards; RCCL is AMD's NCCL |
| speculative decoding | speculative decoding | guess k tokens cheaply, verify with one target-model pass |
| trafność zgadywacza (α) | acceptance rate | fraction of accepted guessed tokens; E[tokens] = (1−α^(k+1))/(1−α) |
| EAGLE / Medusa / MTP / DFlash / DSpark | EAGLE / Medusa / MTP / DFlash / DSpark | feature-based head / extra heads / own multi-token head / block diffusion drafter / DFlash + Markov head |
| spekulacja n-gramowa | n-gram / prompt-lookup speculation | guesses by copying continuations previously seen in context |
| GGUF / safetensors | GGUF / safetensors | self-describing quantization-friendly file / safe tensor container (chapter 03) |
| kwantyzacja | quantisation (Q4_K, MXFP4, FP8, AWQ/GPTQ) | storing weights in fewer bits with scales (chapter 03) |
| imatrix | importance matrix | importance matrix for choosing quantization precision where it matters (chapter 03) |
| niezmienniczość względem batcha | batch invariance | a sequence's result does not depend on what else is in the batch |
