# 03 · Quantization and model formats: what is actually in the file

**Why this chapter.** The reference model, `DeepSeek-V4-Flash-0731-UD-IQ3_XXS`, has 284 billion parameters in a file of about 104 GB.
If every parameter took 16 bits, the file would be about 568 GB. The difference is **quantization** — and it decides whether the model fits
on four 32 GB cards at all, and how many bytes a card has to read for each token (that is, how fast the model talks).
After reading this chapter you will be able to: (1) work out by hand how many bits per weight any llama.cpp quantization type takes, (2) explain
how Q4_K_M differs from IQ3_XXS, from MXFP4, from AWQ and from Unsloth's `UD-`, (3) read from the GGUF header what is actually in the file, (4) know
which format is loaded by which engine and on what hardware, (5) plan a quality measurement for the reference model, which — as the speed-up directory admits —
you have not measured yet.

> ⚠️ **I did not run anything here.** This chapter was written from reading code (the llama.cpp tree at version `0ce8cd1`, which you have in production; the clones of `vllm`, `sglang`,
> `mlx`, `mlx-lm`, `ds4`), project documentation, research papers and pull requests (PRs) on GitHub, and notes from this survey. The only "measurement" of my own is **reading the header
> of an Unsloth GGUF file** (Qwen3-Coder-30B-A3B in the UD-IQ3_XXS version) — described in section 7. All quality numbers come from tables in the projects'
> repositories, with the configuration stated; I never mix them across configurations. Commands marked *(not run by me)* come from documentation or code, not from my terminal.
> Things I do not know, I call "I could not establish".

Evidence tags in the text: no tag = I checked it in the code or in the primary source; *(project's own claim)* = the authors' assertion;
*(press report)* / *(third-party source)* = a third party's account; *(my calculation)* = arithmetic from the data given; *(unverified)* = a guess.

## Table of contents

1. [Why quantize: bandwidth and capacity](#1-why-quantize-bandwidth-and-capacity)
2. [Block quantization from scratch: 8 weights on a sheet of paper](#2-block-quantization-from-scratch-8-weights-on-a-sheet-of-paper)
3. [Type families in llama.cpp, with exact bpw](#3-type-families-in-llamacpp-with-exact-bpw)
4. [imatrix: weighting the error by what the model actually uses](#4-imatrix-weighting-the-error-by-what-the-model-actually-uses)
5. [Quality: what the tables in the llama.cpp repository measure](#5-quality-what-the-tables-in-the-llamacpp-repository-measure)
6. [Families outside GGUF: GPTQ, AWQ, SmoothQuant, FP8, NF4, HQQ, EXL, MLX, oQ, ds4](#6-families-outside-gguf)
7. [Unsloth Dynamic (`UD-`) and the reference file](#7-unsloth-dynamic-ud--and-the-reference-file)
8. [Summary table: format × engine × hardware × use case](#8-summary-table-format--engine--hardware--use-case)
9. [The quality of the reference model: what we do not know and how to measure it](#9-the-quality-of-the-reference-model-what-we-do-not-know-and-how-to-measure-it)
10. [File formats: safetensors, GGUF, MLX, ONNX, TensorRT](#10-file-formats)
11. [Conversions and tools: where a GGUF file comes from](#11-conversions-and-tools)
12. [Who is behind it (Unsloth)](#12-who-is-behind-it-unsloth)
13. [What this means for the reference setup](#13-what-this-means-for-the-reference-setup)
14. [What I could not establish](#14-what-i-could-not-establish)

---

## 1. Why quantize: bandwidth and capacity

There are two reasons, and it is worth separating them, because they lead to different decisions.

### 1.1 Capacity: do the weights fit in memory

This is the obvious reason. A parameter in BF16/FP16 takes 2 bytes; in 3 bits — 0.375 bytes.

| Variant of the 284B model | bits per weight | size | fits in 4 × 32 GB? |
|---|---|---|---|
| BF16/FP16 | 16 | 568 GB | no (*my calculation*: 284·10⁹ · 16 / 8) |
| original DeepSeek checkpoint (FP4 experts, the rest FP8) | ≈ 4.4–4.7 | 167 GB (including about 11 GB of the DSpark head) | no (size from the deployment log in `../speeding-up-generation/`; bpw: *my calculation*) |
| Q4_K_M "as if" (4.89 bpw from the README table for Llama-3.1-8B) | 4.89 | about 174 GB | no (*my calculation*; this is only a scale, not an existing file) |
| your UD-IQ3_XXS | ≈ 2.9–3.2 (section 7.4) | about 104 GB | yes, but with almost no headroom |

Consistency check: experts in MXFP4 (4.25 bpw) come to 277·10⁹ · 4.25 / 8 ≈ 147 GB, the rest (about 7 billion parameters, ~8 bits) about 7 GB — about 154 GB together, and from the 167 GB size minus about 11 GB of head you get about 156 GB *(my calculation)*. So the split of 277 + 7 billion parameters and the "FP4 + FP8" description hold together.

Each card has **34,208,743,424 bytes** of memory (31.86 GiB; read from `/sys/class/drm/card*/device/mem_info_vram_total` on the machine in the notes), so about **136.8 GB** in total
(127.4 GiB). The nominal "4 × 32 = 128" is in fact 127.4 GiB; in decimal GB it is 136.8. Remember this in every
"file X GB versus memory" comparison: **GB (10⁹) and GiB (2³⁰) differ by 7.4%**, and that difference is what we will stumble over in section 7.4.

### 1.2 Bandwidth: how many bytes have to be read per token

This is the subtler reason and the more important one for speed. From chapter [02](02-HOW-INFERENCE-WORKS.md) you know that decoding (generating token by token) is
**memory-bandwidth-bound**: for every token the card reads all the active weights from memory, and does only two floating-point operations per weight (a multiply and an add).
Step time ≈ (bytes of active weights) / (memory bandwidth). Quantization shrinks the numerator.

For the reference model (*my calculation*, based on the parameters from the model card: 13.5 billion active parameters after splitting 277 billion experts + about 7 billion for the rest, see below):

```
bytes per token ≈ 13.5·10⁹ · (bpw / 8)

bpw = 16     → 27.0 GB per token   (ceiling at 640 GB/s: ~24 tok/s)
bpw = 4.5    →  7.6 GB            (~84 tok/s)
bpw = 2.94   →  4.96 GB           (~129 tok/s)
```

This agrees with the calculation from the speed-up directory ("~5 GB to read per token"). This is a **ceiling for a single card at 100% memory utilization**; the measured 23.5 → 49 tok/s
is another story (hand-offs between cards, irregular reading of experts) — described there, not here.
The 640 GB/s bandwidth is a second-hand figure (*third-party source*, Wikipedia on the RX 9000 family; I could not fetch the AMD page) — treat it as a parameter, not a fact.

Two things this calculation hides:

1. **Not all weights are quantized equally.** In the real file, attention, embeddings and output have 4–8 bits, and the experts 2–3 (section 7). The effective number of bytes per token is therefore higher than
   "average × active". A measurement from the notes: ds4 on a Mac M5 Max (Q2, 2.45 bpw on average) reaches 39.35 tok/s, whereas the formula predicted about 154 — that is 26% of the ceiling *(project's own claim + my calculation)*. The formula is an **upper bound**.
2. **Quantization moves the roofline "inflection point" (ridge) to the left**: the fewer bytes per weight, the fewer tokens in a batch are enough for the card to become compute-bound rather than memory-bound
   (at 150 FLOP/B: batch 150 for FP16, 75 for 8 bits, 38 for 4 bits, 28 for 3 bits *(my calculation from the fundamentals note; 96 TFLOPS and 640 GB/s are unverified)*).
   In practice the kernels dequantize in the ALU anyway, or compute on INT8 integer dot products (the `mmq` path in llama.cpp, with activations in Q8_1), so the effective point is higher.

### 1.3 Quantization is not free

Fewer bits means a larger error. The rest of the chapter answers the question: **how to spend the bit budget wisely** (where to give more bits, how to store the scales, how to choose the representative values) and **how to measure how much quality
it cost**. A separate matter — quantization of the *KV cache* (`-ctk`/`-ctv`) — is outside this chapter (chapter 02); I only mention that in llama.cpp tensor mode requires an **unquantized** KV
(a note from `docs/multi-gpu.md`), so in the reference deployment `-ctk f16 -ctv f16` is a requirement, not a choice.

---

## 2. Block quantization from scratch: 8 weights on a sheet of paper

### 2.1 The idea

Weights are floating-point numbers, say in the range −1…1. We want to store them in 4 bits, that is as integers 0…15. This cannot be done directly — we need a **scale**:
`w ≈ d · (q − 8)`, where `q` is a 4-bit integer (0…15), and `d` is a single floating-point number (the scale) shared by a group of weights. We remember `q` for every weight and `d` once per group.
On readout we multiply. This is exactly the construction that llama.cpp implements in the Q4_0 type: `block_q4_0` = an fp16 scale + 16 bytes of nibbles for 32 weights, and the value is `d · (q − 8)`.

**Analogy:** it is a ruler with markings. Instead of measuring every weight in millimetres (16 bits), you measure it in the ruler's "ticks" (4 bits), and you write down the size of a tick — `d` — once per few dozen measurements.
The larger the spread of values in the group, the coarser the tick and the larger the error.

### 2.2 A worked example

Take 8 weights (eight, so that they fit on a sheet of paper; a real block has 32 or 256):

```
w = [ 0.12  −0.31  0.05  0.47  −0.08  0.22  −0.55  0.03 ]
```

**Simplified scale rule** (my didactic version; I did not read the exact `quantize_row_q4_0` function, so the details of scale selection in llama.cpp may differ):
let the weight with the largest magnitude land at the edge of the range. Here that is −0.55, and the range is 16 levels, so `d = 0.55 / 8 = 0.06875`.
Then `q = round(w / d + 8)`, clipped to 0…15.

| weight w | w / d + 8 | q (stored in 4 bits) | reconstructed d·(q−8) | absolute error |
|---:|---:|---:|---:|---:|
| 0.12 | 9.75 | 10 | 0.1375 | 0.0175 |
| −0.31 | 3.49 | 3 | −0.3438 | 0.0338 |
| 0.05 | 8.73 | 9 | 0.0688 | 0.0188 |
| 0.47 | 14.84 | 15 | 0.4813 | 0.0113 |
| −0.08 | 6.84 | 7 | −0.0688 | 0.0112 |
| 0.22 | 11.20 | 11 | 0.2063 | 0.0137 |
| −0.55 | 0.00 | 0 | −0.5500 | 0.0000 |
| 0.03 | 8.44 | 8 | 0.0000 | 0.0300 |

*(my calculation; halves rounded up)*. The largest error is 0.0338, that is about **half a "tick" `d`** (0.034) — the theoretical worst case of rounding, no surprises.
Note the last weight: 0.03 landed on `q = 8`, that is **exactly zero**. Small weights merge into zero; that is the price.

**The same group in 8 bits** (range −127…127, `d = 0.55/127 = 0.00433`): the reconstructed values are 0.1213; −0.3118; 0.0520; 0.4720; −0.0780; 0.2209; −0.5500; 0.0303, the largest error **0.0020** — about 16× smaller,
because the tick is 16× finer. That is how Q8_0 compares to Q4_0.

**Memory cost of this toy.** 8 weights × 4 bits = 32 bits, plus an fp16 scale = 16 bits → 48 bits for 8 weights = **6 bits per weight**. A real Q4_0 block has 32 weights:
(32 · 4 + 16) / 32 = **4.5 bpw** (bits per weight). The scale "taxes" every weight: the smaller the block, the more finely the scale is fitted, but the larger the tax.

### 2.3 Why blocks, and not one scale per tensor

Add one outlier weight to the group: instead of 0.03 let the last one be **−2.2**.

* **One scale for all 8:** `d = 2.2 / 8 = 0.275`. The weights 0.12; 0.05; −0.08 are reconstructed as **0.000** (an error of up to 0.12 — as much as the weight itself); 0.22 → 0.275; −0.31 → −0.275. RMS error (root of the mean square): **0.065**.
* **Two blocks of 4:** the first (0.12; −0.31; 0.05; 0.47) has its own scale ≈ 0.059; the largest error in it is **0.016**. The second block (containing the outlier) suffers as above (an error of up to 0.08), but **the damage stays within its bounds**.

*(my calculation, using the same simplified rule.)* Conclusion: a single outlier "ruins" the scale of all the weights it shares a block with. Blocks limit the reach of the damage — and that is why all
the formats in this chapter, from Q4_0 to MXFP4, are **block-based**. The kernel multiplies on the fly: for each block it performs an integer dot product of the weights with the activations (these are also quantized to Q8) and multiplies the result by two scales
(`mmq`, `mmvq`, on CPU `vec_dot` — notes on llama.cpp).

### 2.4 Two-level scales: the idea behind K-quants

If a small block (32 weights) is good for accuracy, and an fp16 scale costs 0.5 bpw, then you can… **quantize the scales themselves**. K-quants (Iwan Kawrakow, PR #1684, merged 2023-06-05) do exactly that:

* a **super-block** of 256 weights = 8 sub-blocks of 32 (types Q4_K, Q5_K) or 16 of 16 (Q2_K, Q3_K, Q6_K);
* each sub-block has its own scale (and, in the "type-1" types, its own minimum) stored in **6 bits** (Q3_K/Q4_K/Q5_K), 4 bits (Q2_K) or 8 bits (Q6_K);
* only these scales have one fp16 "super-scale" (`d`) and a super-minimum (`dmin`) for the whole super-block.

The calculation for Q4_K, from the `block_q4_K` structure in `ggml/src/ggml-common.h` (line 338, `static_assert`):

```
2 · fp16 (d, dmin)                         =   4 B
12 B of packed 6-bit scales and minimums   =  12 B   (8 sub-blocks × (6+6) bits = 96 bits)
256 weights × 4 bits                       = 128 B
                                           ─────────
                                             144 B per 256 weights  → 144·8/256 = 4.5 bpw
```

The scale overhead is 16 B / 256 weights = **0.5 bpw**. If every sub-block of 32 weights had a scale **and** a minimum in fp16 (as in the older Q4_1), the overhead would be 4 B / 32 weights = **1.0 bpw** — Q4_1 has 5.0 bpw, Q4_K 4.5 with the same sub-block size.
Two-level scales thus bought half a bit per weight, without coarser ticks.

> **Check it yourself 1 — work out bpw from the code.** Open `ggml/src/ggml-common.h` in the llama.cpp tree and find the `static_assert(sizeof(block_…) == …)` lines
> (for Q4_K line 338, for Q6_K 368, for IQ3_XXS 411). Each of them is a computation of the block size in bytes; divide by the number of weights in the block (32 or `QK_K` = 256, line 89) and multiply by 8.
> For example: `grep -n "static_assert(sizeof(block_" ~/llama.cpp-0ce8cd1/ggml/src/ggml-common.h` (just reading a file, GPU untouched).

---

## 3. Type families in llama.cpp, with exact bpw

Below I count bits per weight from the `block_*` structures (sizes from `static_assert` in `ggml/src/ggml-common.h`, tree `0ce8cd1`). This is the **block bpw** — "(bits of the block) / (number of weights in the block)", with the scales included.
Note: the llama.cpp README gives different numbers (e.g. IQ3_XXS 3.2548 bpw for Llama-3.1-8B), because that is the **average over the whole file**, in which some tensors (embeddings, output, norms) are in other types.

### 3.1 Legacy types: Q4_0, Q4_1, Q5_0, Q5_1, Q8_0

One level of scales: a block of 32 weights, an fp16 scale (+ an fp16 minimum in the "_1" types), + possibly a fifth bit.

| type | block structure (32 weights) | bytes | bpw |
|---|---|---:|---:|
| Q4_0 | fp16 `d` + 16 B of nibbles | 18 | **4.5** |
| Q4_1 | fp16 `d`, fp16 `m` + 16 B | 20 | **5.0** |
| Q5_0 | fp16 `d` + 4 B (fifth bits) + 16 B | 22 | **5.5** |
| Q5_1 | fp16 `d`, fp16 `m` + 4 B + 16 B | 24 | **6.0** *(my calculation from `static_assert`)* |
| Q8_0 | fp16 `d` + 32 × int8 | 34 | **8.5** |

Q8_0 is today mainly the "nearly lossless" variant for reference and the format of **activations** in kernels (Q8_1 with an extra sum; 36 B / 32 weights = 9.0 bpw, but that is not a format for storing weights). Q4_0 and Q4_1 are clearly worse than K-quants in the quality tables
at a similar size (section 5).

### 3.2 K-quants: Q2_K … Q6_K

Super-blocks of 256, two levels of scales (section 2.4). Sizes from `static_assert`:

| type | byte layout in a super-block (256 weights) | bytes | bpw |
|---|---|---:|---:|
| Q2_K | 16 B of scales+minimums (4+4 bits × 16 sub-blocks) + 64 B of 2-bit weights + 2 × fp16 | 84 | **2.625** |
| Q3_K | 32 B (high bit) + 64 B (2 low bits) + 12 B of scales + fp16 `d` | 110 | **3.4375** |
| Q4_K | 2 × fp16 + 12 B of scales/minimums + 128 B | 144 | **4.5** |
| Q5_K | 2 × fp16 + 12 B + 128 B + 32 B (fifth bit) | 176 | **5.5** |
| Q6_K | 128 B (low nibbles) + 64 B (2 high bits) + 16 × int8 scales + fp16 `d` | 210 | **6.5625** |
| Q8_K | fp32 `d` + 256 × int8 + 16 × int16 sums | 292 | 9.125 (internal only, activations) |

Q2_K, Q4_K, Q5_K are "type-1" types (`w = d·q + m`, with a scale and a minimum), while Q3_K and Q6_K are "type-0" (`w = d·q`, scale only) *(project's own claim: the text of PR #1684)*.

**The suffixes `_S`, `_M`, `_L` are not block types, but *recipes* (mixtures).** `Q4_K_M` is not a "Q4_K_M block": it is a file in which most tensors are in Q4_K, but e.g. half of `attn_v` and `ffn_down` are in Q6_K,
and `output.weight` is always in 6 bits *(project's own claim: PR #1684)*. Today's mixture rules live in `src/llama-quant.cpp` (lines about 465–735 in tree `0ce8cd1`) and are heavily elaborated (separate paths for GQA and MoE).
The prototype of this way of thinking — "give more bits to the layers where it matters" — is exactly what Unsloth Dynamic, oQ in oMLX and the ds4 recipe do later (sections 6–7).

### 3.3 i-quants: IQ1…IQ4 (coding through a codebook)

So far every weight had its own `q`. i-quants (IQ) do something different for low bits: a group of several weights (e.g. 8) is replaced by an **index into a table of patterns** (a *codebook*), chosen so as to cover
the distribution of weights well. Inspiration: the QuIP# paper *(project's own claim: the text of PR #4773)*. Provenance from the notes, all from the PR texts:

* **#4773** (merged 2024-01-08): "true" 2 bits, **2.0625 bpw**; borrows from QuIP# the sign-parity trick (7 bits encode 8 signs) and a codebook from points of the **E8** lattice (256 points); instead of QuIP#'s Hadamard rotations
  it uses ordinary ggml block scaling.
* **#4897**: quantization code and a **ban on IQ2_XXS/IQ2_XS without imatrix** (in the PR: without it the result is "garbage").
* **#5196** (2024-01-30): **IQ3_XXS 3.0625 bpw**, the **D4** lattice (256 points), 92 bits per 32 weights + a 4-bit scale.

Sizes from `static_assert`:

| type | bytes / 256 weights | bpw | notes |
|---|---:|---:|---|
| IQ1_S | 50 | **1.5625** | |
| IQ1_M | 56 | **1.75** | |
| IQ2_XXS | 66 (fp16 + 64 × uint16) | **2.0625** | requires imatrix |
| IQ2_XS | 74 | **2.3125** | requires imatrix |
| IQ2_S | 82 | **2.5625** | |
| IQ3_XXS | 98 (fp16 + 96 B) | **3.0625** | the type from your file's name |
| IQ3_S | 110 | **3.4375** | |
| IQ4_NL | 18 / 32 weights | **4.5** | 16-element nonlinear value table |
| IQ4_XS | 136 | **4.25** | block of 256, 6-bit sub-scales |

The price: decoding through a table is more expensive than multiplication — in the llama.cpp README (Llama-3.1-8B, hardware not stated) K and IQ quants generate tokens at a similar speed, IQ "with a low computational overhead".
The name "IQ" **does not mean "requires imatrix"** (that is true only for IQ2_XXS/XS) — the fundamentals note was too simplified at this point.

### 3.4 MXFP4 and NVFP4: 4-bit floating-point formats

Instead of integers — **E2M1** floating-point micro-numbers (1 sign bit, 2 exponent bits, 1 mantissa bit; 16 possible values), with a block scale.

| format | block | scale | bytes | bpw |
|---|---|---|---:|---:|
| **MXFP4** (OCP Microscaling, arXiv 2310.10537) | 32 weights | 1 byte **E8M0** (a power of two) | 17 | **4.25** |
| **NVFP4** (NVIDIA) | 64 weights = 4 sub-blocks of 16 | 1 byte **UE4M3 (FP8)** per sub-block; **plus** one fp32 for the whole tensor, stored separately | 36 | **4.5** |

In ggml: `block_mxfp4` = a byte `e` + 16 bytes of `qs`; types `GGML_TYPE_MXFP4 = 39`, `NVFP4 = 40`. The llama.cpp converter has "lossless" repackings of MXFP4 and NVFP4 experts (from `compressed-tensors`, ModelOpt) — "only moves bits", file `conversion/base.py`.
This matters for you, because **DeepSeek-V4 experts are natively in FP4** (`expert_dtype: fp4` in the checkpoint configuration), and gpt-oss ships in MXFP4.
NVIDIA claims NVFP4 gives "1% or less" degradation relative to FP8 on DeepSeek-R1-0528 *(company's own claim)*. Fast multiplication in FP4 requires Blackwell tensor cores (5th generation) — on gfx1201 FP4 is only a **storage** format
with software decoding; kernel support for MX types on gfx1201 *(unverified)*.

### 3.5 Ternary and extreme types: TQ1_0, TQ2_0, Q1_0, Q2_0

* **TQ1_0**: 54 B / 256 weights (fp16 + 4 B + 48 B, "trits" encoded 5 per byte) → **1.6875 bpw**; **TQ2_0**: 66 B / 256 → **2.0625 bpw**. Intended for models trained as ternary (BitNet), not for quantizing ordinary models.
  Interestingly, the converter `convert_hf_to_gguf.py` has `--outtype` with the values `f32, f16, bf16, q8_0, tq1_0, tq2_0, auto` (line 60) — these are the only types it can write directly.
* **Q1_0** (128 weights: 18 B → **1.125 bpw**) and **Q2_0** (64 weights: 18 B → **2.25 bpw**): new in this tree (types 41 and 42), `GGML_TYPE_COUNT = 43`. Kernels *(unverified)*.

### 3.6 What else is "in the family", though not in this tree

`ik_llama.cpp` (Iwan Kawrakow's fork, chapter [04](04-LLAMA-CPP-AND-THE-GGML-FAMILY.md)) has its own types: IQ2_K…IQ6_K, "trellis" quants IQ1_KT…IQ4_KT, variants with row interleaving (`_R4`) for CPU.
**Files with these types load only in ik_llama.cpp** — this is a real dependency on the fork; plain llama.cpp will not load them. For your AMD machine this is something to know about, not to use
(HIP/ROCm for gfx1201 in ik_llama.cpp is not a documented target, *unverified*).

Read the mixture recipes (the `use_more_bits(i_layer, n_layers)` rule and the branches for `attn_v`, `ffn_down`, GQA, MoE) in `src/llama-quant.cpp`, lines about 465–735 — this will be useful in section 7.3, where I compare them with the Unsloth file.

---

## 4. imatrix: weighting the error by what the model actually uses

A standard quantizer minimizes the reconstruction error of every weight equally. But not every weight is equally important: an error in a matrix column through which large activations pass damages the result more
than an error in a column that the activations barely brush.

The **importance matrix (imatrix)** is, for each tensor, a vector: for each column — the **sum of squared activations** (over the tokens of the calibration text). The quantizer uses it as weights in a weighted least-squares method:
it chooses the representative values so that the error is small **where the importance vector is large**. This is a *diagonal* approximation ("ignoring non-diagonal elements" in the text of PR **#4861**, merged 2024-01-12):
a full second-order matrix (as in GPTQ) would be huge.

What follows from this:

* It is **not training** — the weights are not updated "down the gradient", they are only rounded differently.
* The result **depends on the calibration text** (language, domain) and may overfit to it. Unsloth publishes its own imatrix files (for Qwen3-Coder-30B: `imatrix_unsloth.gguf_file`, 122 MB).
  The llama.cpp README also has an experiment (a table in section 5): for IQ1_S or Q2_K, **more wikitext tokens in the imatrix did not give a consistent improvement** (10k vs 10m tokens).
* For low bits it is a **necessary condition** (IQ2_XXS/XS). For Q4_K_M — the improvement is small but measurable: in the Llama-3-8B table (section 5) KLD drops from 0.0313 to 0.0282 (≈ −10%).
* By default imatrix is **not** used for `output.weight` and embeddings (`--process-output` disabled) — "it is usually better not to use it for these tensors" (the tool's README).

Commands (from `tools/imatrix/README.md` and `tools/quantize/README.md` in tree `0ce8cd1`, *not run by me*):

```bash
# 1) compute the imatrix on calibration text, from an F16/BF16 model
llama-imatrix -m model-f16.gguf -f kalibracja.txt -ngl 99 -o imatrix.gguf

# 2) quantize with the imatrix (last argument: number of threads)
llama-quantize --imatrix imatrix.gguf model-f16.gguf model-Q4_K_M.gguf Q4_K_M 8
```

---

## 5. Quality: what the tables in the llama.cpp repository measure

There are two measures, and you need to know what each means.

* **Perplexity (PPL)** — how well the model predicts the next token on a given text (lower = better). It is *not comparable between models* with different tokenizers, and for fine-tuned models it can be higher despite better answers
  (the tool's README). llama.cpp numbers are not comparable with the numbers of other projects.
* **Kullback–Leibler divergence (KLD)** — the distance between the next-token probability distribution of the reference model (FP16) and of the quantized one, averaged over tokens. 0 = identical distributions.
  **KLD is a more sensitive measure of damage than PPL**, because PPL can "hide" damage (changes up and down cancel out), whereas KLD cannot. Besides KLD the tool computes, among other things, "same top p" — how often both models assign the highest probability to the same token.

### 5.1 Reference table: Llama-3-8B, KLD relative to FP16

Source: `tools/perplexity/README.md` in tree `0ce8cd1` (added by Johannes Gäßler, PR #6936, 2024-04-30). **Configuration:** llama.cpp revision `f364eb6f`, CUDA backend, CPU AMD EPYC 7742, GPU 1 × RTX 4090,
Wikitext-2 corpus (test), model Llama-3-8B; the reference is FP16 logits saved to a file. "imatrix WT 10m" = an imatrix from 10 million wikitext tokens. I picked the rows; the full table is in the README.

| type | imatrix | size [GiB] | PPL | ΔPPL | KLD | RMS Δp |
|---|---|---:|---:|---:|---:|---:|
| f16 | – | 14.97 | 6.2332 | 0.0015 | 0.00055 | 0.79% |
| q8_0 | – | 7.96 | 6.2343 | 0.0027 | 0.00136 | 1.20% |
| q6_K | – | 6.14 | 6.2534 | 0.0217 | 0.00545 | 2.30% |
| q5_K_M | – | 5.33 | 6.2886 | 0.0570 | 0.01076 | 3.16% |
| q4_K_M | WT 10m | 4.58 | 6.3829 | 0.1513 | 0.02815 | 5.25% |
| q4_K_M | – | 4.58 | 6.4071 | 0.1755 | 0.03127 | 5.52% |
| iq4_XS | WT 10m | 4.14 | 6.4597 | 0.2281 | 0.03633 | 6.04% |
| q4_0 | – | 4.34 | 6.7001 | 0.4685 | 0.07194 | 8.43% |
| q3_K_M | WT 10m | 3.74 | 6.7343 | 0.5026 | 0.08436 | 9.29% |
| iq3_S | WT 10m | 3.42 | 6.9655 | 0.7339 | 0.11128 | 10.85% |
| **iq3_XXS** | WT 10m | **3.05** | 7.4584 | 1.2268 | **0.18363** | 13.84% |
| q3_K_S | WT 10m | 3.41 | 7.6029 | 1.3712 | 0.19982 | 14.98% |
| q2_K | WT 10m | 2.96 | 8.6478 | 2.4162 | 0.33222 | 18.88% |
| iq2_XS | WT 10m | 2.43 | 10.7614 | 4.5298 | 0.54629 | 23.87% |
| iq2_XXS | WT 10m | 2.24 | 14.0918 | 7.8601 | 0.81202 | 28.58% |
| iq1_S | WT 1m | 1.88 | 58.0978 | 51.8661 | 2.21128 | 46.42% |

*(size in GiB for the 8B model; "f16" in this table is a difference caused solely by casting the logits to 16 bits).*

Three things to remember from this table:

1. **Stairs, not a ramp.** From Q8_0 to Q5_K_M KLD grows about 8×, from Q5_K_M to Q4_K_M 3×, and from Q4_K_M to IQ3_XXS 6.5× (0.028 → 0.184). Below 3 bits quality drops sharply (IQ2_XXS: PPL more than 2× higher than FP16; IQ1_S: unusable).
2. **Imatrix always helps, more so at low bits.** Q3_K_M: 0.1019 without, 0.0844 with imatrix; Q3_K_S: 0.2282 vs 0.1998.
3. **At the same size, IQ types beat K-quants.** IQ3_S (3.42 GiB, KLD 0.111) vs Q3_K_S (3.41 GiB, KLD 0.200) — almost the same size, KLD 44% lower.

### 5.2 The same type hurts newer models more

From the same README: LLaMA-2-7B vs LLaMA-3-8B (same configuration, KLD relative to FP16):

| type | KLD LLaMA-2-7B | KLD LLaMA-3-8B | PPL ratio (quant / FP16): 2-7B → 3-8B |
|---|---:|---:|---|
| Q2_K | 0.1089 | 0.4451 | 1.108 → 1.565 |
| Q4_K_M | 0.01269 | 0.03127 | 1.0142 → 1.0282 |
| Q6_K | 0.00210 | 0.00545 | – |
| Q8_0 | 0.00037 | 0.00136 | – |

The authors point out: LLaMA-3 after Q2_K has a PPL that is 56% higher. **More heavily trained models are harder to compress.** For you the conclusion is inconvenient: tables from years ago about older models
**understate** the losses on modern models, and there is no in-tree table for a modern MoE (see section 9).

### 5.3 Older data on model size

* **LLaMA-2-70B, Wikitext-2** (same README): FP16 PPL 3.4313 (128.5 GiB); Q6_K +0.16% (52.70 GiB); Q5_K_M +0.40% (45.41); Q4_K_M +1.20% (38.54); Q3_K_M +4.72% (30.83); Q2_K +8.82% (27.27).
  So on a **70B** model the same quantization hurts relatively less than on 7–8B (Q2_K: +8.8% for 70B versus +56% for LLaMA-3-8B — but these are different families, so do not draw a "law of nature" from it).
* **PR #1684 (June 2023, LLaMA-1, wikitext, context 512):** FP16 PPL 5.9066 (7B) → Q2_K 6.7764, Q3_K_M 6.1503, Q4_K_S 6.0215, Q4_K_M 5.9601, Q5_K_S 5.9419, Q6_K 5.9110. The author: 6 bits fit within 0.1% of FP16 and the relative error **does not decrease** with model size above 13B *(project's own claim)*.
* **PR #5196 (January 2024, imatrix from wiki.train.raw):** IQ3_XXS beats Q3_K_XS at a smaller size, e.g. Mistral-7B 2.705 GiB / PPL 6.0578 vs 2.786 GiB / 6.1632; Mixtral-8x7B 17.05 GiB / 4.4570 vs 17.75 / 4.5174.
  At context 4096: IQ3_XXS Mixtral 3.7689, LLaMA-2-70B 3.2757 *(project's own claim)*.

### 5.4 File size versus speed

In the README `tools/quantize/README.md` (Llama-3.1-8B; **hardware not stated in the file**) there are average bpw of whole files and generation speed: Q4_K_M 4.8944 bpw — 71.93 tok/s, Q8_0 8.5008 — 50.93, F16 16.0005 — 29.17 (tg128).
Decoding speed **follows the number of bytes** — it is the same regularity as in section 1.2, just seen from the other side. IQ recipes have an additional computational cost, small on this machine.

Average bpw of whole files (Llama-3.1-8B, same README): IQ1_S 2.0042; IQ2_XXS 2.3824; IQ3_XXS 3.2548; IQ4_XS 4.4597; Q2_K 3.1593; Q3_K_M 3.9960; Q4_K_M 4.8944; Q5_K_M 5.7036; Q6_K 6.5633; Q8_0 8.5008.
Note: "Q2_K" has 3.16 bpw in the file, not 2.625 — because `output.weight`, embeddings, parts of `attn_v`/`ffn_down` are in higher types. **It is the same lesson that in section 7 will explain why "IQ3_XXS" from your model's name has on average a different number of bits than 3.0625.**

> **Check it yourself 2 — the KLD table at the source.** `tools/perplexity/README.md` in the llama.cpp tree: the section "LLaMA 3 8b Scoreboard" (configuration at the top: revision, backend, CPU, GPU) and the description of the statistics under `--kl-divergence`.
> Read the paragraph saying that the reference logits file is large (README: 11 GiB for LLaMA 2, 37 GiB for LLaMA 3 on the Wikitext-2 test set) — this matters when in section 9 you plan a measurement on a model with a vocabulary of 129,280 tokens.

---

## 6. Families outside GGUF

Everything below lives mainly in the world of **safetensors + servers** (vLLM, SGLang, TensorRT-LLM) or in the Apple world (MLX). What matters to you above all is **whether a given format has
a kernel on gfx1201 at all** (section 8) and **whether it can be converted to GGUF**.

### 6.1 GPTQ (Frantar, Ashkboos, Hoefler, Alistarh; arXiv 2210.17323, 2022)

One-shot quantization of **weights only**, to 3–4 bits, using approximate second-order information (the Hessian): the weights are quantized one after another, and the rounding error of each of them
**is compensated by adjusting the not-yet-quantized weights**, so that the layer's output changes as little as possible on a calibration sample. The authors report about 4 GPU-hours for a 175B model and generation speed-ups of 3.25× (A100) / 4.5× (A6000)
thanks to custom kernels *(project's own claim / abstract)*. Typical layout: 4 bits, group 128, fp16 scale and a 4-bit zero → 4 + (16 + 4)/128 ≈ **4.16 bpw** *(my calculation for a common configuration)*.
The checkpoint is safetensors with tensors `qweight/qzeros/scales/g_idx`. llama.cpp **reads** such a checkpoint, but only **dequantizes it to floating point and quantizes again from scratch** (`conversion/base.py` line about 495).

### 6.2 AWQ (Lin, Tang, Tang et al.; arXiv 2306.00978; MLSys 2024 — best paper award)

The opposite idea to GPTQ: it does not reconstruct the error, but **protects about 1% of "salient" channels**, chosen by the magnitude of the **activations** (not the weights), by rescaling them before quantization. No backpropagation and no reconstruction.
The authors claim it is more robust to a change of calibration set than GPTQ *(project's own claim)*. Memory as in GPTQ g128: ≈ 4.16 bpw *(my calculation)*.
**llama.cpp does not load AWQ**: the converter raises `NotImplementedError: Quant method is not yet supported` (`conversion/base.py` line about 573).
State of the tools (GitHub API, 2026-10-19): **AutoAWQ archived** (2025-05-11), **AutoGPTQ archived** (2025-04-11); the live paths are `vllm-project/llm-compressor` (3.9k stars, active),
GPTQModel (1.3k) and `NVIDIA/Model-Optimizer` (5.4k, Apache-2.0). If you see "pip install autoawq" in a tutorial, know that it is a dead project.

### 6.3 SmoothQuant (Xiao, Lin et al.; arXiv 2211.10438; ICML 2023)

The only one in this set that also quantizes **activations to INT8** (W8A8). The problem: activations have outlier channels, which ruin INT8. The solution: a mathematically equivalent transfer of the "difficulty" from activations to weights by scaling
the channels. The gain (authors' data): up to 1.56× faster and 2× less memory. Requires **INT8 GEMM units** — it is a server-throughput technique, not a way to "fit a big model in VRAM". In vLLM as `w8a8_int8` / compressed-tensors.

### 6.4 FP8 (Micikevicius et al.; arXiv 2209.05433)

Two forms: **E4M3** (4 exponent bits, 3 mantissa bits; no infinities, a single NaN pattern) and **E5M2** (close to IEEE). Convention: E4M3 for weights and activations. Real checkpoints add scales:
per tensor, per channel or per block (e.g. 128×128: 8 + 32/16384 ≈ 8.002 bpw *(my calculation)*). This is exactly how the "rest" (non-experts) is stored in the original DeepSeek-V4 checkpoint: FP8 outside the FP4 experts.
In vLLM on ROCm the kernel `ROCmFP8ScaledMMLinearKernel` declares support for "CDNA3+ (gfx942/gfx950) or RDNA4 (gfx12x)" — so **FP8 is permitted in the code on gfx1201**, but performance was not measured (*unverified*).

### 6.5 bitsandbytes NF4 and double quantization (QLoRA; Dettmers et al.; arXiv 2305.14314, 2023)

**NF4** ("NormalFloat", 4 bits) is a set of 16 values placed so as to be optimal for weights with a normal distribution with zero mean; a block of 64 weights with an fp32 scale (absmax) = 4 + 32/64 = **4.5 bpw**.
**Double quantization** also quantizes the scales themselves (8 bits per 64, plus an fp32 per 256 scales): 4 + 8/64 + 32/(64·256) = **4.127 bpw** (as in the paper: a saving of 0.37 bit per parameter, about 3 GB for a 65B model).
It is a format **for training** (QLoRA: a frozen model in NF4 + LoRA adapters); at inference the weights are dequantized to bf16 before multiplication — hence the slow decoding. Supported in transformers, PEFT, Unsloth (for training), vLLM, SGLang;
**not** in llama.cpp or MLX.

### 6.6 HQQ, EXL2, EXL3

* **HQQ** (Half-Quadratic Quantization): **no calibration**, quantizes the largest models "in a few minutes" *(project's own claim)*; base configuration `nbits=4, group_size=64` (≈ 4.5 bpw with an fp16 scale and zero *(my calculation)*).
  The repository moved to `dropbox/hqq` (960 stars, last change 2026-02-26). In mistral.rs as `HQQ4/HQQ8`.
* **EXL2** (turboderp; a GPTQ derivative, mixed per-layer bitrates of 2–8 bpw) and **EXL3** (ExLlamaV3: "a simplified variant of QTIP", lattice/trellis quantization, arXiv 2406.11235, NeurIPS 2024): fractional bpw 2–8, TP/EP, continuous batching, **CUDA only** (the README does not mention ROCm).
  The ExLlamaV2 README says development moved to V3, although the GitHub API does not show archiving (last change 2026-03-04) — a contradiction; treat V2 as legacy. I **did not collect** quality comparisons of EXL3 against GGUF/AWQ at the same bpw.

### 6.7 MLX: affine group quantization and its variants

The MLX core (`mlx/ops.cpp`, lines about 4827–4852): `quantize(w, group_size=None, bits=None, mode='affine')` with modes `affine`, `mxfp4`, `mxfp8`, `nvfp4` and default group sizes **64 / 32 / 32 / 16**.
The affine mode keeps a **scale and a bias** per group, so 4 bits, group 64, fp16 scale and bias → 4 + 32/64 = **4.5 bpw** *(my calculation; assumes 16-bit scales)*.

`mlx_lm.convert` (file `mlx_lm/convert.py`) accepts: `--hf-path`, `--mlx-path`, `-q/--quantize`, `--q-group-size`, `--q-bits`, `--q-mode`, `--quant-predicate`, `--dtype`, `--upload-repo`, `-d/--dequantize`.
The recipes `mixed_2_6`, `mixed_3_4`, `mixed_3_6`, `mixed_4_6` assign layers `low_bits` or 6 bits, "with similar choices as e.g. Q4_K_M in llama.cpp" (a comment in the code) — it is the same thought as section 3.2.
Besides that, `mlx_lm/quant/` contains learned methods: **DWQ** (distillation: tunes scales and biases against an unquantized teacher), **AWQ**, **GPTQ** and **dynamic quantization** (per-layer sensitivity → mixed bits; the document `LEARNED_QUANTS.md`).
A quantized **KV** (`--kv-bits`, `QuantizedKVCache`) disables batching in `mlx_lm.server` (the SERVER.md document). Chapter [07](07-APPLE-MLX-OMLX-AND-DS4.md) describes the rest.

### 6.8 oQ from oMLX

oMLX (`omlx/oq.py`, 11,295 lines) has its own mixed-precision quantizer which — as the document `oQ_Quantization.md` itself says — combines "the layer-position strategy of GGUF K-quants, the selective non-quantization of Unsloth Dynamic 2.0, and the MSE-optimal clipping of BnB".
Levels oQ2, 2.5, 2.7, 3, 3.5, 4, 5, 6, 8; approximate bpw including scales for group 64: oQ4 ≈ 4.6–4.7, oQ3 ≈ 3.5–3.7, oQ2 ≈ 2.8–3.0, oQ8 ≈ 8.5.
The procedure: it streams the tensors → **measures the sensitivity of each layer** on built-in calibration (600 multilingual/code/tool samples) → allocates extra bits to sensitive tensors within a size budget →
in the "e" variant (*enhanced*, e.g. `oQ4e`) it collects an imatrix (about 2700 samples; for MoE it samples until every expert has enough tokens) and rounds the groups, searching for a scale/offset with the minimum **importance-weighted** error. The result: standard MLX safetensors.
Safeguards: 8-bit embeddings and head, MoE routers in full precision, norms unquantized. Quality from the project's documentation *(project's own claim, a set of 1900 MMLU/Winogrande/MBPP/GSM8K questions)*:
Qwen3.5-9B original 76.53, oQ4e 77.05 (5.6 GB), oQ3e 73.79 (4.6 GB); Qwen3.6-35B-A3B original 82.68, oQ4e 83.05 (20 GB), oQ3e 82.68 (16 GB). Note: **these are the author's results**, on their own set, with no independent replication.
The very idea — "measure sensitivity, then spend the bit budget" — is exactly what you do in the llama.cpp world through imatrix + `--tensor-type`.

### 6.9 The quantization layout in ds4 (DwarfStar)

ds4 **does not introduce a new format** — it uses GGML types, but in an **asymmetric layout** (`docs/MODELS.md`): routed experts are the compression target — `IQ2_XXS` for gate/up and `Q2_K` for down (with imatrix) — while "Q8 projections, shared experts and the output, plus F16/F32 tensors" stay in high precision.
There are also Q4_K variants and **native MXFP4** for DeepSeek experts (they preserve DeepSeek's original FP4 without re-quantization).

**I checked whether this description agrees with the file size** *(my calculation)*: experts 277.0 billion parameters, of which 2/3 (gate, up) at 2.0625 bpw and 1/3 (down) at 2.625 bpw → 2.25 bpw on average → 277.0·10⁹ · 2.25 / 8 = **77.9 GB**.
The rest, about 7.0 billion parameters in Q8_0 (8.5 bpw) → **7.4 GB**. Together **85.3 GB = 79.5 GiB**. The notes give "about 81 GiB" for the file *(project's own claim)* — a 2% discrepancy, so the layout is as described (the remainder: F16/F32 tensors, overhead). This is also
a test of the "277 + 7 billion" split used in this chapter. On average it comes to 2.45 bpw (81 GiB · 8 / 284 billion).

A digression that will be useful in section 13: ds4 on the M5 Max reaches 39.35 tok/s at an average of 2.45 bpw, whereas the pure formula "bandwidth / (active · bpw/8)" would give about 154 — because **dense tensors (attention, shared experts, output) are in Q8/F16 and are read for every token**.

---

## 7. Unsloth Dynamic (`UD-`) and the reference file

### 7.1 What Unsloth is, and what it is not

`unslothai/unsloth` is above all a **fine-tuning library** (its own Triton kernels) plus, since 2026, the "Studio" app, which **wraps llama.cpp** (optionally vLLM/SGLang) — and, most importantly for you, a **model publisher**:
the "Dynamic GGUF" quants are the artifacts that most users of local models actually download. When Studio runs a GGUF, **that is llama.cpp** — there is no point comparing "Unsloth versus llama.cpp" as engines.
(More on this in chapter [05](05-PACKAGED-RUNTIMES-OLLAMA-LM-STUDIO-AND-OTHERS.md).) As of 2026-10-19 (GitHub API): 78,273 stars, release `v0.1.909-beta` every 2–4 days; dual licence (core Apache-2.0, the optional Studio UI part — AGPL-3.0).

### 7.2 What `UD-` means

**`UD-` = Unsloth Dynamic** (documentation: `unsloth.ai/docs/basics/unsloth-dynamic-2.0-ggufs`). Names like `UD-IQ3_XXS`, `UD-Q4_K_XL`, `UD-Q2_K_XL` are Unsloth's labels. The `_XL` suffixes are **theirs** — llama.cpp has no `Q4_K_XL` type
(`include/llama.h` has `IQ3_XS=22`, `IQ3_XXS=23`, no XL). The GGUF header does, however, keep the closest standard ftype in `general.file_type` (23 = `MOSTLY_IQ3_XXS`, `llama.h:142`), though the tensor mixture is custom.

The method according to the documentation *(company's own claim)*: Dynamic 2.0 "selectively and far more cleverly quantizes layers… instead of modifying only selected layers, we dynamically adjust the quantization type of **every possible layer**"; the schemes are model-specific
(MoE and dense); calibration of >1.5 million tokens "hand-curated and cleaned", not an evaluation set; it is **post-training quantization with imatrix** — "we do NOT use QAT or QAD"; the recommended measure is KL divergence.
Version v3.0 (models up to Qwen3.8): "a much better calibration set… agentic coding, chat, multilinguality", a published imatrix file, the claim ">10% better top-1 accuracy at the same size than any other provider" for Qwen3.8-27B *(company's own claim)*.
Numbers from the documentation that the author of the notes saw only in a tool's summary (Gemma 3 27B: MMLU 71.47% for Dynamic 4-bit versus 70.64% for Google's QAT at 17.2 GB; about 7.5% lower KLD for Q2_K_XL), **check on the page before quoting**.

**What is not known:** *how* the choice of type for each layer is computed (sensitivity analysis? a heuristic?) — I did not find a description on the accessible pages, and the recipe tool **is not in the public `unsloth` repository**. Whether the recipes are produced by plain
`llama-quantize --tensor-type …` or by a private version of the tool — *I could not establish*. The sentence "layer selection by sensitivity analysis" is therefore *unverified*.

### 7.3 What is actually in UD-IQ3_XXS: reading the header

I read the GGUF v3 header of the file `unsloth/Qwen3-Coder-30B-A3B-Instruct-UD-IQ3_XXS.gguf` (size 12,848,766,112 B; I downloaded the first 40 MB by range request; the repository also contains `imatrix_unsloth.gguf_file`, 122 MB).
The model: architecture `qwen3moe`, 48 blocks, 128 experts (8 active), `general.quantized_by = Unsloth`, `file_type = 23`, **30,532,122,624 parameters**. The distribution of tensor types:

| type | block bpw | parameters | share of parameters | share of bytes |
|---|---:|---:|---:|---:|
| IQ3_XXS | 3.0625 | 18.32 billion | 60.0% | 54.6% |
| IQ3_S | 3.4375 | 8.25 billion | 27.0% | 27.6% |
| IQ4_XS | 4.25 | 3.16 billion | 10.4% | 13.1% |
| Q6_K | 6.5625 | 0.395 billion | 1.3% | 2.5% |
| Q4_K (`token_embd`) | 4.5 | 0.311 billion | 1.0% | 1.4% |
| Q5_K | 5.5 | 0.078 billion | 0.25% | 0.4% |
| F32 (norms, router `ffn_gate_inp`, q/k norms) | 32 | 0.013 billion | 0.04% | 0.4% |

**Seven different types in a file named "IQ3_XXS".** The average bpw — I computed it two ways:

```
from type bits:  (18.32·3.0625 + 8.25·3.4375 + 3.16·4.25 + 0.395·6.5625
                  + 0.311·4.5 + 0.078·5.5 + 0.013·32) / 30.527
               = 102.73 Gbit / 30.527 bn  = 3.365 bpw        (my calculation)
from file size: 12,848,766,112 · 8 / 30,532,122,624          = 3.367 bpw
```

Agreement to 0.05%, so the distribution from the header is complete. Note: **the name "IQ3_XXS" means 3.06 bpw, but the whole file has 3.37** — exactly the lesson that Q2_K from section 5.4 gave you.

The allocation to tensors (from the header; "layer" = block number 0–47):

* `ffn_gate_exps` / `ffn_up_exps`: **IQ3_XXS** in layers 0, 3–31, 34–35; **IQ3_S** in 1–2, 32–33, 36–47;
* `ffn_down_exps`: IQ3_XXS in most of the middle ones; **IQ4_XS** in layers 1–3, 21, 28, 41–47; IQ3_S in 26, 32–33, 35–40;
* `attn_q/k/v`: IQ4_XS, except layers 1–2 and 45–47 (Q5_K);
* `attn_output`: IQ4_XS, with Q6_K in layers 0, 5, 7, 33, 37–38, 40, 44, 46–47 and Q5_K in 1–2, 45;
* `output.weight`: Q6_K; `token_embd`: Q4_K.

The standard llama.cpp rule for IQ3_XXS (`src/llama-quant.cpp`, lines about 465–735) would give Q4_K for this model's `attn_v` (GQA-8) (line 601) — the file has something else (IQ4_XS/Q5_K), and the irregular layers (21, 28, 4–5 vs 1–3)
do not fit the standard pattern. I did not run plain `llama-quantize` on this model to compare, so "deviates from the standard recipe" I read from the code and the dump (*causality: unverified*).

**Conclusion about your file type:** it is a **~3.4 bpw mixed-precision** file in which attention, embeddings, output, the experts of the first and last layers and some middle layers get 4–6 bits,
and about 87% of the parameters (the experts) sit at about 3.1–3.4 bits. An imatrix was used (the file is published). This is for the **Qwen3-Coder-30B model**; for DeepSeek I do not know the layout (section 7.4).

> **Check it yourself 3 — the type distribution in your file.** In an environment where you have `gguf-py` (the script `../../pl/przyspieszanie-generowania/narzedzia/gguf-inspect.py` uses `GGUFReader`), count the tensor types
> *(not run by me; the fields `tensor_type`, `n_elements`, `n_bytes` exist in `ReaderTensor` in `gguf-py/gguf/gguf_reader.py`)*:
>
> ```python
> from collections import Counter
> from gguf import GGUFReader
> import glob
> files = sorted(glob.glob("…/DeepSeek-V4-Flash-0731-UD-IQ3_XXS-0000*-of-00004.gguf"))
> par, byt = Counter(), Counter()
> for f in files:
>     for t in GGUFReader(f).tensors:
>         par[t.tensor_type.name] += t.n_elements
>         byt[t.tensor_type.name] += t.n_bytes
> for k in par: print(k, par[k]/1e9, "bn params", byt[k]/1e9, "GB")
> print("total", sum(byt.values())*8/sum(par.values()), "bpw")
> ```
>
> It reads only the headers (like `gguf-inspect.py`), so it runs in seconds and does not touch the GPU. It will settle the doubt from section 7.4 (GB or GiB) and show the real mixture.

### 7.4 The reference model: DeepSeek-V4-Flash UD-IQ3_XXS — the arithmetic *(my calculation)*

Input data: the four parts of the file total **104,207,848,508 bytes** *(measured: `du -sb` on the directory with the files `…-0000N-of-00004.gguf`)* — that is **104.2 decimal GB** (≈ 97.05 GiB) — for **284 billion** parameters (model card; a rounded number).

**(a) The average from file size**

```
104.2·10⁹ B · 8 / 284·10⁹ = 833.6 / 284 = 2.935 bpw
```

A note on units, because it is easy to be off by 0.22 bpw: the Hugging Face page and `du -sb` show bytes/decimal GB, `ls -lh` and `du -h` — GiB (97.05 GiB). The numbers in this handbook are decimal GB.

**(b) Comparison with the structural model.** From the DeepSeek-V4-Flash configuration (43 layers, 256 routed experts + 1 shared, 6 routed per token, `moe_intermediate_size` 2048, hidden 4096) it follows that:
experts = 256 · 43 · (3 · 4096 · 2048) = **277.0 billion** parameters, the rest (attention, shared experts, embeddings, output, routers) ≈ **7.0 billion**; active per token 7.0 + 6/256 · 277.0 = **13.5 billion**, which agrees with the declared 13B.

| scenario | calculation | size |
|---|---|---:|
| all experts in pure IQ3_XXS (3.0625 bpw) | 277.0·10⁹ · 3.0625 / 8 | 106.0 GB |
| + the rest in Q8_0 | 7.0·10⁹ · 8.5 / 8 | + 7.4 GB → **113.5 GB = 105.7 GiB** |
| + the rest at about 5 bpw (like attention in the Qwen3-Coder file: IQ4_XS–Q6_K) | 7.0·10⁹ · 5 / 8 | + 4.4 GB → **110.4 GB = 102.8 GiB** |

The result: the file (104.2 GB) is about 2–9 GB (2–8%) **smaller** than each of the variants above, and even than "pure IQ3_XXS" for the experts alone (106.0 GB). Assuming the structure from (b) is correct,
this means that **some of the experts lie in 2-bit types** (e.g. IQ2_XS/IQ2_S), and the dense part is not entirely in 8 bits. This is consistent with the idea of Dynamic quants (a variable number of bits per tensor), but **the specific composition of types in this file is not verified here** — reading the header will settle it (the *Check it yourself 3* box above; the Qwen file from the notes has a different mixture and cannot be transferred 1:1).

**(c) How many bytes per token** — here something shows up that the simple formula from section 1.2 does not see. For each token the card reads **whole dense tensors** (about 7.0 billion parameters, always) and **6 of 256 experts in every layer** (6/256 · 277.0 = 6.49 billion):

```
bytes/token = 7.0·10⁹ · b_dense/8  +  6.49·10⁹ · b_experts/8

b_dense = 5,   b_experts = 3.06 :   4.38 + 2.48 =  6.9 GB
b_dense = 8.5, b_experts = 3.06 :   7.44 + 2.48 =  9.9 GB
(the simple formula "13.5 bn · 2.94 / 8"        =  4.96 GB)
```

So **most of the memory traffic per token is the dense part**, not the experts. This explains why the measured 49 tok/s lies far below the ceiling from section 1.2, and — more importantly — **what follows for choosing a larger quant** (section 13):
the experts' bits cost a lot of capacity but little bandwidth.

### 7.5 Cost-quality position

The llama.cpp data (section 5): IQ3_XXS lies between Q2_K and Q4_K in size; PR #5196 shows that it beats Q3_K_XS at a smaller size on the same models, and in the Llama-3-8B table it has a KLD of 0.184 — 6.5× more than Q4_K_M.
**No in-tree table measures IQ3_XXS against FP16 on a modern MoE.** Whether 3.4 bpw is "good enough" for a production agentic model has to be measured on your own tasks — and I will get to that in section 9.

---

## 8. Summary table: format × engine × hardware × use case

Legend for the "hardware" columns: ✔ = the kernel exists (visible in the code or documented by the project); ~ = exists, but coverage not audited; ✘ = absent (verified); ? = *I could not establish*.
The "gfx1201" column concerns **the reference cards (R9700, ROCm)**.

### 8.1 GGUF families (kernels in llama.cpp and derivatives)

| format | block bpw | loaded by | CPU | CUDA | gfx1201 / ROCm | Metal | typical use |
|---|---|---|---|---|---|---|---|
| Q4_0/Q4_1/Q5_x/Q8_0 | 4.5 / 5.0 / 5.5–6.0 / 8.5 | llama.cpp, ik_llama.cpp, Ollama, LM Studio, llamafile, KoboldCpp, mistral.rs (also ISQ), KTransformers (LLAMAFILE backend) | ~ | ~ | ~ (the `hip` backend is in the tree) | ~ | backward compatibility; Q8_0 as "nearly lossless" |
| K-quants Q2_K…Q6_K | 2.625…6.5625 | as above | ~ | ~ | ~ (types Q4_K/Q5_K/Q6_K appear in Qwen's UD file; in your DeepSeek — section 7.4) | ~ | **the default choice** at 4–6 bits (Q4_K_M, Q5_K_M) |
| i-quants IQ1…IQ4 | 1.56…4.5 | llama.cpp + forks; mistral.rs only via the GGUF path | ~ (slower decoding) | ~ | ~ (IQ3_XXS is in the name of your file, which runs in production) | ~ | low bits (2–3.5); IQ2_XXS/XS only with imatrix |
| TQ1_0/TQ2_0, Q1_0, Q2_0 | 1.69 / 2.06 / 1.125 / 2.25 | llama.cpp | ? | ? | ? | ? | ternary/BitNet; new types, *not audited* |
| MXFP4 / NVFP4 (in GGUF) | 4.25 / 4.5 | llama.cpp (CPU + CUDA; PR #23572 for NVFP4 quantization on CUDA still open), KTransformers (CPU) | ~ (per the notes) | ~ (per the notes) | ? (FP4 as a format; **do not expect FP4 speed** *(unverified)*) | ? | "natively FP4" models (gpt-oss, DeepSeek experts) |
| **UD-** (Unsloth mixtures) | per file: e.g. 3.37 | everything that reads GGUF | = kernels of the types used | = | = (types as above) | = | ready-made "best" recipes + imatrix; the production file of the reference setup |
| IQK/trellis from ik_llama | various | **ik_llama.cpp only** | ✔ | ✔ | ? (not a documented target) | ~ | CPU/hybrid for MoE; dependence on the fork |
| ds4 (GGML types in an asymmetric layout) | about 2.45 on average | ds4 only | ~ | ✔ | in `main` the target is gfx1151, **not gfx1201** (3 open PRs from third parties) | ✔ | DeepSeek V4/GLM/Qwen3.8 on Macs with 96–128 GB |

### 8.2 "Server" families and Apple

| format | bpw (usually) | loaded by | calibration | CUDA | gfx1201 / ROCm | Metal | typical use |
|---|---|---|---|---|---|---|---|
| **GPTQ** (safetensors) | ≈ 4.16 (g128) | vLLM (`gptq`, `gptq_marlin`), SGLang, TRT-LLM, ExLlama, mistral.rs; llama.cpp only dequantizes | yes (Hessian) | ✔ (Marlin, Ampere+) | vLLM: **the code has an `RDNAHybridW4A16` kernel for gfx11/12**, while the table in the documentation says ❌ — *a contradiction, test it* | ✘ | servers, 4-bit weights |
| **AWQ** | ≈ 4.16 (g128) | vLLM (`awq`, `awq_marlin`), SGLang, TRT-LLM, MLC; **not llama.cpp** | yes (activation statistics) | ✔ | as GPTQ (the same W4A16 kernel) | ✘ | as above; dead AutoAWQ → use llm-compressor |
| **SmoothQuant W8A8** | 8 | TRT-LLM, vLLM (`w8a8_int8`), SGLang | yes | ~ (INT8 TC) | ? | ✘ | server throughput in data centers |
| **FP8** E4M3/E5M2 | ≈ 8 | vLLM, SGLang, TRT-LLM, KTransformers, mistral.rs, MLC; llama.cpp only reads and converts | none/light | ✔ (Hopper/Ada/Blackwell) | vLLM: **permitted in the code on gfx12x**, performance not measured | ✘ | weights + KV in servers; DeepSeek's native "rest" |
| **MXFP4 / NVFP4** (safetensors) | 4.25 / 4.5 | vLLM (`mxfp4`, `modelopt_fp4`), SGLang, TRT-LLM, MLX, KT | none (native checkpoint) / ModelOpt PTQ | ~ (natively only Blackwell) | vLLM: `mxfp4` is on the ROCm list; *kernels on gfx1201: I could not establish* | ✔ (MLX) | models released in FP4 |
| **bitsandbytes NF4** | 4.5 / 4.127 | transformers, PEFT, Unsloth, vLLM, SGLang, mistral.rs; not llama.cpp/MLX | none | ✔ | `bitsandbytes` **is not** on the ROCm quantization list in vLLM (`rocm.py`) | ✘ | **training** (QLoRA), not fast inference |
| **HQQ** | ≈ 4.5 (g64) | transformers, mistral.rs, torchao | **none** (minutes) | ✔ | ? | ✘ | fast quantization without calibration |
| **EXL2 / EXL3** | 2–8 fractional | ExLlamaV2/V3, TabbyAPI | yes (Hessian / QTIP) | ✔ | ✘ (the README does not mention ROCm) | ✘ | maximum quality per bit on NVIDIA |
| **MLX affine / mxfp4 / nvfp4** | 4.5 (4-bit g64) | MLX, mlx-lm, oMLX, LM Studio (MLX), mistral.rs (AFQ) | none (+ DWQ/AWQ/GPTQ optionally) | ✔ (a CUDA backend for MLX exists) | ✘ (MLX: Metal, CUDA, CPU) | ✔ | **Mac** |
| **oQ** (oMLX) | oQ4 ≈ 4.6 | only as plain MLX safetensors (any MLX engine) | yes (sensitivity + imatrix) | – | ✘ | ✔ | Mac, mixed precision to a budget |
| **MLC group quant** `q4f16_1` | ≈ 4 + scales | MLC/WebLLM only | none | TVM compilation | ? | ✔ | browser/phone |

**What the table does not say (honestly):**

* For llama.cpp I verified the **existence of the backend directories** (`cuda`, `hip`, `metal`, `vulkan`, `sycl`, `opencl`, `cann`, `hexagon`, `openvino`, `webgpu`), not the coverage of every type on each of them. The only evidence "in practice" is that **your UD-IQ3_XXS file runs on gfx1201 in production** (which exact types it contains — section 7.4).
* For vLLM on gfx1201 the code and the documentation disagree (AWQ/GPTQ: documentation ❌, the code has RDNA kernels); in the notes I advised "test before you trust". SGLang: gfx1201 **is not a target** (the `setup_rocm.py` script accepts only `gfx942`, `gfx950`, `gfx1250`;
  note: gfx1250 is not RDNA4). TensorRT-LLM: NVIDIA only. mistral.rs: **no ROCm or Vulkan backend** (CUDA, Metal, CPU). Details in chapter [06](06-SERVING-ENGINES-VLLM-SGLANG.md).
* **GGUF itself** in vLLM/SGLang: loaders exist, but vLLM does not have `gguf` on its ROCm quantization list, and SGLang lists GGUF with kernels for **CUDA only** (Ascend via dequantization on CPU). The documentation of the GGUF plugin for vLLM speaks of a "highly experimental and under-optimized" path.

> **Check it yourself 4 — the vLLM quantization list on ROCm.** In the vLLM clone: `vllm/platforms/rocm.py`, the field `supported_quantization` (lines about 625–649): you will find `awq`, `gptq`, `fp8`, `compressed-tensors`, `quark`, `mxfp4`… and **no `gguf` or `bitsandbytes`**.
> Next to it check `vllm/model_executor/kernels/linear/mixed_precision/rdna_hybrid_w4a16.py` (651 lines) — this is the W4A16 kernel for gfx11/gfx12 that conflicts with the "AWQ ❌" table in `docs/features/quantization/README.md`.

---

## 9. The quality of the reference model: what we do not know and how to measure it

### 9.1 What you changed and what is known about it

In the speed-up directory ([`../speeding-up-generation/README.md`](../speeding-up-generation/README.md)) you went from 23.5 to about 50 tok/s with two changes: **speculative decoding** (DSpark draft, 3 tokens) and **tensor split** (`--split-mode tensor`) on a newer llama.cpp.
The weights and their quantization **did not change** — it is the same UD-IQ3_XXS file. So this decision raises two separate questions about quality, and it is worth not mixing them:

1. **Did the speed-up change quality?** Speculative decoding by design does not change the distribution of the answers (the big model approves every token). Tensor split changes the **order of floating-point summation** — at temperature 0 the answers are not identical character for character (0 of 4 identical; with layer split and the draft 2 of 4).
   This is numerical noise, but *whether* it is harmless — in the words of the deployment log: "I don't know".
2. **How good is the quant itself**, UD-IQ3_XXS on DeepSeek-V4-Flash, relative to a better quant of the same model? **Nobody has measured this**, certainly not me.

### 9.2 What we do not know (honestly)

* **You did not measure quality after the speed-up.** You started the quality benchmark (the "hard" set, 20 PL/EN tasks, k = 3, 120 samples; this model scored **PL 92 / EN 93** on 10 October) and **aborted it after 11 samples**, so there is no publishable data.
  11 samples are too few for any conclusion: at about 92% accuracy the standard error is sqrt(0.92 · 0.08 / 11) ≈ **8 percentage points**; even the full 120 samples give ≈ **2.5 pp** (*my calculation*, assuming independence — but the samples are correlated, because there are only 20 different tasks repeated 3 times,
  so the real error is larger). You will not detect differences of a few points with such a set.
* **We have no public quality figure for UD-IQ3_XXS on DeepSeek-V4.** Unsloth's documentation (company's own claim) gives results for Gemma 3 27B and Qwen3.8-27B, not for this model; the llama.cpp tables measure older dense models (Llama).
  From section 5.2 you know that the same type hurts newer models more, so the Llama tables may **understate** the loss.
* **We do not know what the mixture of types in your file looks like** (section 7.4) — so we cannot even estimate the losses from the per-type table.
* **Perplexity and KLD will not show degradation over a long tool-use horizon** (multi-step calls, long context), and that is your actual use *(unverified — a conclusion from Unsloth's documentation and from the fundamentals)*.
  A model can have an excellent KLD on wikitext and get lost on the third tool call.
* **The model was natively FP4 (the experts).** The path "FP4 → (BF16?) → IQ3_XXS" is a re-quantization from an already 4-bit source; how Unsloth carried it out, *I could not establish*.

### 9.3 Method: three questions, three measurements

Below are commands **from the documentation and code in tree `0ce8cd1`**; *I ran none of them*. Remember that the GPUs are production ones — you take measurements where you can, when you can.

**Measurement A — did the speed-up change anything? (same file, two configurations)**
Cheap, and it answers question 1 directly. Record the logits in the old configuration (layer split; you do not enable the draft in this measurement — it is lossless in the distribution), then compare against the tensor configuration:

```bash
# Wikitext-2 test set (a script in the llama.cpp tree, per the perplexity tool's README;
# the output file name `wiki.test.raw` below is my assumption)
scripts/get-wikitext-2.sh

# 1) reference: layer split, save the logits
llama-perplexity -m MODEL.gguf -f wiki.test.raw -fa on -ngl 999 --split-mode layer \
    --kl-divergence-base logits-layer.kld

# 2) comparison: tensor split against that file
llama-perplexity -m MODEL.gguf -f wiki.test.raw -fa on -ngl 999 --split-mode tensor \
    --kl-divergence-base logits-layer.kld --kl-divergence
```

(The syntax `--kl-divergence-base` / `--kl-divergence` is from the tool's README. That tensor mode works with `llama-perplexity` and requires `-fa on` and an unquantized KV is from `docs/multi-gpu.md`; **that it works specifically with this model and this version is not verified**.)
*How to read the result:* the reference scale is the table from section 5.1 — the noise of merely saving logits in 16 bits is KLD ≈ 0.0006, and Q8_0 ≈ 0.0014. If the KLD between the configurations is on the order of 10⁻⁴–10⁻³, it is numerical noise; if it approaches 10⁻², something more is going on.
*(This is my proposed threshold, not a value from the documentation.)* **Watch the disk space:** the logits file is large (README: 37 GiB for LLaMA 3 on Wikitext-2; DeepSeek's vocabulary has 129,280 tokens, so expect tens of GiB — *unverified*).
You can shorten the test text.

**Measurement B — how much does the quant fall short of a better one? (the same question as the tables in section 5, but on the reference model)**
You need a *reference*. BF16 is out of the question (568 GB). Three realistic options:

1. **A higher quant of the same model** (from the UD family, if it exists and can be run — even slowly, with offloading to RAM: KLD on a few tens of thousands of tokens does not require speed). Then the same two commands as above: reference logits → `--kl-divergence` for UD-IQ3_XXS.
   The result says how much is lost relative to *that* quant, not relative to FP16 — so it is a lower bound on the loss.
2. **A proxy model of the same quantization family**: e.g. Qwen3-Coder-30B-A3B, for which you know the UD-IQ3_XXS mixture (section 7.3) and whose BF16 (≈ 61 GB *(my calculation: 30.5 billion · 2 B)*) fits in the 128 GB of the cards' memory — you compare UD-IQ3_XXS with Q8_0/BF16 in KLD.
   This will tell you what **this class of recipe costs on MoE**, not what it costs on DeepSeek.
3. **ds4 with native MXFP4** (experts without re-quantization; the "Vision Exp MXFP4" version is 145 GiB, so it **does not fit** in the 136.8 GB of the cards without an SSD) — only as reading material for the idea.

**Measurement C — do the tasks work? (the most important for agents)**
KLD and PPL will not replace it. You already have the tool: `python3 -m qbench run --model deepseek-v4-flash-0731 --suite hard --k 3` (a few hours; do not change the `llama-swap` configuration during the run — it will unload the model). Compare with the report from 10 October.
Two pieces of advice (*mine*, from the error calculation above): increase the number of **different** tasks (not just k), because repetitions of the same task say little; and add a separate measure: the **share of correct tool calls (valid JSON + the right function)** on a large sample — this is the most sensitive to degradation
from quantization and the closest to your use. If the result gets worse relative to 10 October, the speed-up directory advises routing clients to the `-nospec` twin entry or going back to layer split.

**Why PPL alone is not enough:** according to the llama.cpp documentation PPL is not comparable between models and can be higher for fine-tuned models despite better answers; KLD against a reference is more sensitive, but it still measures the next-token distribution on ordinary text, not an agentic task.
That is why three measurements, not one.

---

## 10. File formats

So far I have talked about the *content* (how the weights are stored). Now about the *packaging*: what is in the file besides the weights and why it matters for tools.

### 10.1 safetensors (Hugging Face)

A "tensor container" format: the file begins with an 8-byte number (little-endian) with the header length, then a JSON header (tensor name → type, shape, byte offsets), then the raw bytes of the tensors.
The HF documentation speaks of the goals: **safety** (unlike pickle it does not execute code), speed (**zero-copy**) and **partial loading** (`get_slice`). The byte layout above is for me *unverified details from memory* — I read the HF documentation only as far as the goals.

```
[ 8 B: header length N ][ N B: JSON {"tensor.name": {"dtype":..., "shape":[...], "data_offsets":[from,to]}, ...} ][ raw tensor bytes ]
```

Large models are split: `model-00001-of-000NN.safetensors` + `model.safetensors.index.json` (a name → file map; `mlx_lm/utils.py`). It is used by transformers, vLLM, SGLang and MLX.
**Quantized checkpoints (GPTQ/AWQ/FP8/NVFP4) are still safetensors** — with additional tensors (scales, zeros) and a `quantization_config` field in `config.json`; in DeepSeek-V4, e.g., `expert_dtype: fp4` and dynamic FP8.
So for safetensors quantization is a **convention bolted on from the side**, not part of the format.

### 10.2 GGUF — the layout, annotated

GGUF is **one file that knows everything about the model**. The layout (`ggml/include/gguf.h`: `GGUF_MAGIC "GGUF"`, `GGUF_VERSION 3`, `GGUF_DEFAULT_ALIGNMENT 32`; `ggml/src/gguf.cpp`), little-endian:

```
┌─ HEADER ────────────────────────────────────────────────────────────────┐
│ "GGUF"                   4 B   magic                                   │
│ version                  u32   = 3                                     │
│ n_tensors                i64   how many tensors in the file (yours: this part)
│ n_kv                     i64   how many metadata key-value pairs       │
├─ METADATA (n_kv times) ─────────────────────────────────────────────────┤
│ key: string (u64 length + bytes, no NUL)                               │
│ value type: u8,i8,u16,i16,u32,i32,f32,bool,string,array,u64,i64,f64    │
│ value (arrays carry the element type and a u64 count)                  │
│   e.g. general.architecture, general.file_type (23 = MOSTLY_IQ3_XXS),  │
│       general.quantized_by, general.alignment (default 32),            │
│       <arch>.block_count, <arch>.attention.head_count_kv, <arch>.rope.*│
│       tokenizer.ggml.tokens, ….merges, tokenizer.chat_template        │
├─ TENSOR TABLE (n_tensors times) ────────────────────────────────────────┤
│ name (e.g. blk.12.ffn_down_exps.weight, output.weight, token_embd…)    │
│ n_dims u32 │ ne[] (i64 per dimension) │ ggml type (Q4_K, IQ3_XXS, F32…) │ offset u64
├─ padding to general.alignment ──────────────────────────────────────────┤
├─ DATA BLOB ──────────────────────────────────────────────────────────────┤
│ tensors one after another, each aligned; offset counted from the start of the blob
└──────────────────────────────────────────────────────────────────────────┘
```

What this gives and why **the type is per tensor**: the tensor table is where what your readout from section 7.3 shows sits — *every tensor has its own type*. Unsloth's mixture is simply "a different type in a row of the table".
The `<arch>.*` metadata carries the architecture hyperparameters, and `tokenizer.*` — the full tokenizer and the chat template. That is why `llama-server -m file.gguf` needs nothing else.

**Alignment and `mmap`.** Because the data is aligned and contiguous, the loader can map the file into memory (`mmap`) and hand pointers straight to the backends (`src/llama-model-loader.cpp`, lines about 560–691, the alignment check at line 691).
The effects: nearly instant loading, sharing of the page cache between processes, working with models larger than RAM. In `include/llama.h` (line about 207) there are the loading modes AUTO, NONE, MMAP, MLOCK, MMAP_MLOCK and **DIRECT_IO** — your configuration uses `--load-mode dio`;
there is also a "lazy mode" (read only those rows of large tensors that the architecture marks, e.g. MoE experts; "lazy only for marked tensors larger than 4 GiB").

**Splitting.** Files >50 GB are split with the `gguf-split` tool into `…-00001-of-0000N.gguf` (the reference model: 4 parts; the converter also has `--split-max-size` and `--split-max-tensors`). The DSpark draft is a **separate** GGUF file (10.9 GB, 81 tensors, architecture `dflash`),
because DeepSeek's public GGUFs "cut out" the MTP/NextN tensors (you checked: 43 blocks, zero `nextn` tensors).

**Why GGUF won locally** *(reasoning from verified properties)*: (1) one self-describing file: weights + architecture + tokenizer + chat template + default sampling; (2) `mmap`-friendly alignment; (3) quantization is **part of the format** (dozens of block types), whereas
in safetensors it is a sidecar; (4) extensible metadata — new architectures do not break old readers; (5) the whole ecosystem (Ollama, LM Studio, llama-swap, koboldcpp, llamafile, ds4) standardized on it; (6) every ggml backend (CPU/CUDA/HIP/Metal/Vulkan/SYCL) consumes the same blocks.
**Drawbacks:** attachment to the ggml "zoo" of quants; the conversion step from HF; the metadata and tensor names for each architecture are maintained by the llama.cpp developers (a new architecture = a new file in `src/models/` + code in `convert_hf_to_gguf.py`).

### 10.3 MLX

MLX saves arrays through `mx.save_safetensors` — and mlx-lm models are **directories**: `config.json`, tokenizer files and `model*.safetensors`; quantized weights are packed integers + scales and biases per group (default group 64 — section 6.7).
`mlx_lm/gguf.py` can read/write GGUF (a limited reader — *details unverified*). So the "MLX format" is essentially **safetensors with the MLX quantization convention**; it is not an interchangeable format between engines.

### 10.4 ONNX

A computation graph + weights in one protobuf container; used by ONNX Runtime, DirectML and OpenVINO paths (Copilot+ NPU, Lemonade). I **did not study** the details of quantization in ONNX; no engine in the reference stack uses this format.

### 10.5 TensorRT (and the "engine file")

A TensorRT "plan" file is compiled for **one GPU architecture**, a TensorRT version and a shape profile. **TensorRT-LLM no longer uses it**: `trtllm-build`, `LLM(backend="tensorrt")` and the `convert_checkpoint.py` scripts have been removed;
the only backend is PyTorch, and HF checkpoints load directly (`~/runtimes-src/TensorRT-LLM/docs/source/legacy/tensorrt-backend-removal.md`). If in some tutorial you read "TensorRT-LLM compiles an engine file" — it is outdated.
For you this is purely background knowledge (TRT-LLM = NVIDIA only).

### 10.6 Summary

| format | what it is | self-describing? | quantization as part of the format? | who reads it |
|---|---|---|---|---|
| **safetensors** | tensor container (JSON + bytes) | partly (`config.json` alongside) | no, conventions from the side | transformers, vLLM, SGLang, MLX, mistral.rs, TRT-LLM |
| **GGUF** | container + metadata + tokenizer | **yes** | **yes**, type per tensor | llama.cpp and derivatives, ds4 (its own GGUF), mistral.rs, KT (CPU), vLLM/SGLang (experimental) |
| **MLX directory** | safetensors + scale/bias convention | partly | yes (the MLX convention) | MLX, mlx-lm, oMLX, LM Studio (MLX) |
| **ONNX** | graph + weights | yes (the graph) | I did not study it | ONNX Runtime, OpenVINO |
| **TensorRT plan** | compiled engine | no | n/a | (TRT-LLM no longer) |
| `pytorch_model.bin` | pickle | no | no | **avoid** (executes code) |

---

## 11. Conversions and tools

### 11.1 Data flow

```
                  ┌────────────────────────────────────────────────────────────────┐
 HF checkpoint    │  convert_hf_to_gguf.py   --outtype bf16|f16|f32|q8_0|tq1_0|…   │
 (safetensors:    ├─────────────►  GGUF F16/BF16 (full precision, ~2 B/parameter)  │
  BF16/FP8/FP4)   │                         │                                      │
                  │                         ├──► llama-imatrix -m … -f tekst.txt   │
                  │                         │        └─► imatrix.gguf               │
                  │                         ▼                                      │
                  │        llama-quantize [--imatrix …] [--tensor-type …] in out TYPE │
                  │                         │                                      │
                  │                         ▼                                      │
                  │             quantized GGUF (Q4_K_M, IQ3_XXS, …)                │
                  │                         │ (optionally) llama-gguf-split        │
                  │                         ▼                                      │
                  │                    llama-server -m …-00001-of-0000N.gguf       │
                  └────────────────────────────────────────────────────────────────┘

 Same HF ──► mlx_lm.convert --hf-path … -q [--q-bits --q-group-size --q-mode --quant-predicate]
               └─► MLX directory (quantized safetensors) ──► mlx_lm.server / oMLX / LM Studio (MLX)

 Same HF ──► llm-compressor / GPTQModel / Model-Optimizer ──► safetensors AWQ/GPTQ/FP8/NVFP4 ──► vLLM / SGLang / TRT-LLM
                                     (GPTQ: llama.cpp can only dequantize and start over; AWQ: it will not accept it)
```

The principle visible in the diagram: **quantize from high precision, not from a quant**. `llama-quantize` has an `--allow-requantize` flag with a warning in the README: "can severely reduce quality compared to quantizing from 16 or 32 bits".

### 11.2 Commands (from the documentation and the deployment log; *not run by me*)

**HF → GGUF.** A fragment from the DSpark deployment log in `../speeding-up-generation/02-DEEPSEEK-DEPLOYMENT.md` (your own, actually run) shows the converter's syntax:

```bash
python ~/llama.cpp/convert_hf_to_gguf.py deepseek-ai/DeepSeek-V4-Flash-0731 --remote --dspark \
   --target-model-dir ~/spec-dspark/target-hf --outtype bf16 --outfile ~/spec-dspark/DeepSeek-V4-Flash-0731-DSpark.gguf
```

What follows from it: `torch ≥ 2.7` is needed (the type `float8_e8m0fnu`); `--remote` downloads only those safetensors files that contain the needed tensors (3 of 48 files = 11 GB instead of 167 GB); `--outtype` allows `f32, f16, bf16, q8_0, tq1_0, tq2_0, auto`
(converter code, line 60). **Scale:** a full conversion of the 284B model to BF16 would mean about **568 GB** of intermediate file *(my calculation)* — which is why most people download ready-made quants instead of making them.

**Imatrix and quantization** (`tools/imatrix/README.md`, `tools/quantize/README.md` in tree `0ce8cd1`):

```bash
llama-imatrix -m model-f16.gguf -f kalibracja.txt -ngl 99 -o imatrix.gguf

# simple quantization, 8 threads; the output file is "ggml-model-Q4_K_M.gguf"
./llama-quantize input-model-f32.gguf q4_k_m 8

# with imatrix and overriding the types of selected tensors (regex) — a stand-in for a UD-style recipe
./llama-quantize --imatrix imatrix.gguf --output-tensor-type q5_k --token-embedding-type q3_k \
    --keep-split input-model-f32.gguf q4_k_m 8
./llama-quantize --imatrix imatrix.gguf --tensor-type "\.(\d*[13579])\.attn_k=q5_k" \
    --tensor-type "\.(\d*[02468])\.attn_q=q3_k" input-model-f32.gguf q4_k_m 8
```

Useful flags from the tool's README: `--tensor-type` (many times, regex), `--output-tensor-type`, `--token-embedding-type`, `--include-weights`, `--prune-layers`, `--allow-requantize`, `--leave-output-tensor`, `--override-kv`.
Note: these are **the same knobs** with which — according to the assessment in the notes — one can reproduce *in spirit* the UD mixtures and the ds4 recipe (2-bit experts + Q8 for the rest). Whether Unsloth uses exactly these tools is not known (section 7.2); I do not promise that the same file will come out.

**HF → MLX** *(flag syntax from `mlx_lm/convert.py`)*: `mlx_lm.convert --hf-path MODEL_ID -q` with the optional `--q-bits`, `--q-group-size`, `--q-mode {affine,mxfp4,nvfp4,mxfp8}` and `--quant-predicate mixed_4_6` (one of the `mixed_*` recipes). Default: 4 bits, group 64.

What the converter can do, you can check like this: `grep -n "outtype\|--remote\|--dspark\|--split-max" ~/llama.cpp-0ce8cd1/convert_hf_to_gguf.py` will show the `--outtype` list (line 60) and the splitting options; the `conversion/` directory has one file per architecture family
> (e.g. `deepseek.py`) and `base.py` with the logic for reading quantized checkpoints (FP8, GPTQ, compressed-tensors, NVFP4/MXFP4).

---

## 12. Who is behind it (Unsloth)

Unsloth is a company from **Y Combinator (summer 2024)**, founded by **Daniel Han** (formerly NVIDIA; known for bug fixes in Gemma/Llama/Mistral/Phi) and **Michael Han**; the YC page lists a team of 12 (date of the entry unknown). The repository: dual licence — core Apache-2.0,
the optional part (Studio UI) AGPL-3.0, which the README explains as a way to sustain development. Its position in the ecosystem comes from **fast quants and fixes for new models on launch day** (in the documentation: fixes to RoPE scaling, the QK Norm epsilon in llama.cpp *(company's own claim)*).
Daniel Han has about 56% of the repository's commits (6,391 of about 11.4k) — a high "bus factor". **I could not establish price lists, funding rounds or investors** (the `pricing` and `about` pages returned 403); do not rely on anything you "remember" about rounds. More on money and people in chapter [10](10-MONEY-AND-PEOPLE.md).

---

## 13. What this means for the reference setup

### 13.1 Stay with GGUF

On four R9700s (gfx1201, ROCm), GGUF is the only family with first-class support in all the engines that have a chance of working for you (llama.cpp with the HIP backend). vLLM has gfx1201 "on paper" and dedicated RDNA kernels (INT4 W4A16, FP8),
but ROCm is secondary there relative to MI300/MI350, and the ROCm quantization list in the code **does not include `gguf` or `bitsandbytes`**; SGLang does not have gfx1201 as a target; EXL3 and TensorRT-LLM are CUDA. So for this hardware you quantize **to GGUF** and choose the type according to
**bytes per token** (section 7.4c) and **quality measured by KLD on your own prompts** (section 9).

### 13.2 The memory budget today

From the deployment log (measured) and section 1.1:

| item | value |
|---|---|
| memory of the 4 cards together | 136.8 GB (127.4 GiB) |
| UD-IQ3_XXS weights | 104.2 GB (104,207,848,508 B; section 7.4) |
| DSpark draft | file 10.9 GB + buffers; about 4 GB on each of the 4 cards in total (about 16 GB) |
| free VRAM after loading → after real use | card 0: 1.08 → **0.82 GB**; the others: 1.7 → 1.43 GB (≈ 5.1 GB in total) |
| rule from the procedure | ≥ 1 GB free per card (the card with the desktop ≥ 0.8 GB) |

Conclusion *(my calculation)*: **the deployed configuration is at the edge of capacity.** DeepSeek's KV is cheap (0.1–0.4 GB per card for 131k context — the log; about 6.9 KB per token *(my calculation from the notes, assumptions uncertain)*), so it is not the context that eats memory, but weights + draft + compute buffers.

### 13.3 When a larger quant would fit and what it would cost in speed *(reasoning from bandwidth; I measured nothing)*

Two MoE asymmetries from section 7.4(c): the bits of the **experts** cost a lot of capacity (277 billion parameters) and little bandwidth (6.49 billion read per token); the bits of the **dense part** — the opposite (7 billion, read in full, but little capacity).

| change | capacity | bytes/token | effect on the speed ceiling |
|---|---:|---:|---|
| experts +0.25 bpw (e.g. some layers from IQ3_XXS → IQ3_S/IQ4_XS) | **+8.7 GB** (277·10⁹·0.25/8) | + 0.20 GB (+2…3% of 6.9–9.9 GB) | about −2…3% |
| experts +0.5 bpw | **+17.3 GB** | + 0.41 GB (+4…6%) | about −4…6% |
| dense part from about 5 to 8.5 bpw | + 3.1 GB | + 3.1 GB (+44% on a base of 6.9 GB) | about −30% |

So **in bytes (and therefore in speed) raising the dense part is the most expensive, not the experts** — and that part is already high in UD mixtures anyway (IQ4_XS–Q6_K in the Qwen file).
The problem is that there is no memory: you have about 5 GB free in total, and even +0.25 bpw on the experts is +8.7 GB. To make room:

* **Give up the draft** (frees about 16 GB). But the draft gave +50% (23.5 → 35.2 tok/s with layer split, the log) — a cost of about **−33%** in speed (1/1.5), plus a few percent for the more expensive weights. Roughly from 49 to about **30 tok/s** *(my calculation; assumes that the contributions of the draft and of tensor split multiply, which I did not check)*.
  You would then buy about +0.45 bpw (16 GB · 8 / 284 billion, if all of it goes into weights) — little quality for a lot of speed.
* **Offload the experts to host RAM** (`--cpu-moe`, `-ot` in llama.cpp, according to the notes on KTransformers): I could not establish the machine's RAM size and bandwidth, so I will not give a cost. Host memory bandwidth is usually many times lower than 640 GB/s of GDDR6 *(unverified)*, so every expert "in RAM" slows things down considerably.
* **A smaller `--ubatch-size`** (already 512; earlier a gain of 0.7–2.0 GB per card cost 8% of prefill) — the next step is only a few GB and slower prefill *(unverified)*.

**Conclusion:** UD-IQ3_XXS is today **the largest quant that fits together with the draft**. A higher one requires giving up the draft (−33%) or offloading to RAM. Downward (e.g. IQ2_XXS) quality drops steeply — in the Llama-3-8B table KLD rises from 0.18 (IQ3_XXS) to 0.81 (IQ2_XXS) — so do not look for room that way.
Before you change anything, do **measurements B and C** from section 9: perhaps IQ3_XXS is "good enough", perhaps not — and only then does this table make sense.

### 13.4 Before you download the next model — arithmetic on a sheet of paper

```
weights_size ≈ number_of_parameters · bpw / 8
it fits if:  weights_size + draft (if any) + buffers + headroom ≥1 GB/card  ≤  136.8 GB
speed (ceiling) ≈ bandwidth / (dense·b_dense/8 + active_experts·b_experts/8)
```

For dense models the second formula simplifies to "bandwidth / weights size". For MoE **separate** the dense part and the experts, as in 7.4(c) — take the parameter counts from the model's `config.json`.

### 13.5 Macs

* **MLX 4-bit, group 64 = 4.5 bpw**; the same family as Q4_K (4.5 bpw). For a Mac, the speed ceiling from the notes: M5 Max (614 GB/s) — a 4-bit dense 30B about 36 tok/s (25 after a 70% correction), MoE with 13B active about 84 (59) *(formula unverified; a "ceiling", not a promise)*.
  A control measurement: ds4 DeepSeek V4 Flash Q2 on an M5 Max gives 39.35 tok/s, that is about 26% of the formula's ceiling — because of the dense tensors in Q8/F16 (section 6.9).
* **oQ4e** (oMLX) for medium-sized models: e.g. Qwen3.6-35B-A3B oQ4e = 20 GB, according to the author on their set with no loss (83.05 versus 82.68) *(project's own claim)*. Do not believe it until you measure on your own tasks — the same rule as above.
* GGUF files work on a Mac in llama.cpp (Metal); the quality of the quant is the same, only the kernel changes.

### 13.6 Checklist

1. Count the tensor types and the average bpw of your file (*Check it yourself 3*) — two numbers that will settle the doubts from section 7.4.
2. Do **measurement A** (KLD between configurations; cheap) and **measurement C** (tasks + the share of correct tool calls; on a larger number of different tasks) before you build agents on the fast configuration.
3. Keep the imatrix file published by Unsloth next to the model, in case you ever quantize your own fine-tuned models — it is the cheapest quality improvement at low bits.
4. Do not trust numbers from other people's tables: quality depends on the model (section 5.2), and every number should come with hardware, version, model + quant, context and date.

---

## 14. What I could not establish

1. **The composition of the file `DeepSeek-V4-Flash-0731-UD-IQ3_XXS`**: which tensor types it contains and in what proportions (the size is measured: 104.2 decimal GB). To be checked locally (*Check it yourself 3*).
2. **The quality of UD-IQ3_XXS on DeepSeek-V4-Flash** — relative to any higher quant. I have no data at all.
3. **How Unsloth computes the choice of types per layer** and whether it uses the standard `llama-quantize --tensor-type`; the recipe is not in the public repository. The original entry on Dynamic v1 returned 403.
4. **Numbers from Unsloth's documentation** (Gemma 3 27B MMLU 71.47% / 70.64%; about 7.5% lower KLD) — I know them only from the summary of a fetching tool; check on the page.
5. **Coverage of quantization types on the HIP/Vulkan backends** — I verified the existence of the backend directories, not of every type. Support for MX/NVFP4 types on gfx1201 — no data.
6. **vLLM on gfx1201**: the documentation and the code disagree (AWQ/GPTQ); FP8 and INT4 performance on RDNA4 was not measured. SGLang: whether it works on gfx1201 at all — it needs a trial that was not allowed to be done.
7. **EXL3 vs GGUF/AWQ at the same bpw** — I did not collect the primary tables (`doc/exl3.md` returned 404). The state of ExLlamaV2: the README says "superseded", the GitHub API does not show archiving — a contradiction.
8. **Stored bpw of GPTQ/AWQ/HQQ** — computed for typical configurations (g128, g64), not measured.
9. **ONNX details and the safetensors byte layout** beyond the goals from the HF documentation; **some arXiv numbers** I give from the notes (QLoRA 2305.14314).
10. **The machine's capacity outside the cards** (amount of host RAM, its bandwidth) — needed to assess offloading experts to RAM; it is not in the notes.
