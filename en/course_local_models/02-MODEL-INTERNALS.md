# Part 2 — Model internals: feel what happens underneath

**Level: ⭐⭐** · Requires: part 1 (`LOCAL-MODELS-FUNDAMENTALS.md`) · Time: ~4 h

> **Why this chapter.** Part 1 taught you to **talk** to a model. This chapter teaches you to
> **feel** the model. After it you know what a "token" really is, why the second token is generated
> 50× faster than the first, why the same prompt gives two different answers, and how the model
> measures that two sentences "mean the same thing".
>
> **This is not theory for theory's sake.** Every concept here returns in parts 3–7 as a concrete
> engineering decision: token = budget, sampling = tool determinism, KV-cache = the single
> biggest offline optimization, embedding = the foundation of the agent's memory.

```bash
source $LLMEDU/rig-env.sh   # if you don't have it — see 00-COURSE-INDEX.md, section "Conventions"
```

---

## Table of contents

| § | Topic | Key intuition |
| :-- | :-- | :-- |
| [1](#1-token--see-it-with-your-own-eyes) | **Token** | the model does not see letters; it sees numbers, and in Polish it sees more of them |
| [2](#2-what-the-model-really-returns--logits) | **Logits** | the model does not return a word, it returns a **probability distribution over the whole vocabulary** |
| [3](#3-sampling--from-distribution-to-word) | **Sampling** | `temperature`, `top-k`, `top-p`, `min-p` — you choose the word, not the model |
| [4](#4-determinism--why-the-same-prompt-gives-two-answers) | **Determinism** | seed, greedy, and why "temperature 0" is not enough |
| [5](#5-kv-cache--why-the-second-token-is-free) | **KV-cache** | prefill vs decoding; measure it yourself |
| [6](#6-context--what-happens-at-the-boundary) | **Context** | how much memory it eats, what happens on overflow |
| [7](#7-embeddings--how-a-model-measures-meaning) | **Embeddings** | text → vector; compute similarity by hand |
| [8](#8-quantization--measure-the-loss-dont-guess) | **Quantization** | perplexity as a measure; Q4 vs Q8 on your hardware |
| [9](#9-exercise--your-own-generation-loop) | **Exercise** | generate text token by token, by hand |

---

## 1. Token — see it with your own eyes

The model sees neither letters nor words. It sees **integers** — indices into a vocabulary.
The tokenizer is a vocabulary + rules for splitting text.

### 1.1 First measurement

```bash
echo -n "Sprawozdanie finansowe za rok obrotowy 2025" | \
  $LB/llama-tokenize -m $BIELIK --stdin
```

The output is a list of `id → 'fragment'` pairs. Read it carefully — **you will see that "Sprawozdanie"
is not a single token.** It is several fragments, e.g. `Spraw` + `ozdanie`, or even finer.

🔧 **What exactly you are doing:** `--stdin` tells it to read the text from standard input (so
you don't fight with shell quoting), `-m` points to the model — **because the tokenizer is part of the GGUF
file**, not a separate program. Two different models will cut the same text differently.

### 1.2 Count it yourself: Polish is expensive

```bash
# The same meaning, two languages
echo -n "The financial statement for fiscal year 2025" | $LB/llama-tokenize -m $BIELIK --stdin | wc -l
echo -n "Sprawozdanie finansowe za rok obrotowy 2025" | $LB/llama-tokenize -m $BIELIK --stdin | wc -l
```

The Polish one will come out **noticeably longer**. Why: tokenizers are trained mainly on English,
so English words have their own tokens, while Polish ones are assembled from pieces.

💡 **Why you care — three times in this course:**

| Where | Consequence |
| :-- | :-- |
| **Context** (§6) | a Polish document takes ~1.5–2× more context than an English one with the same content |
| **Cost** (part 8) | with the Claude API you pay **per token, not per character** — Polish is literally more expensive |
| **Speed** (part 7) | decoding is counted in tokens/s, so **the same answer in Polish takes longer to produce** |

### 1.3 The same text, different models

```bash
for MODEL in $BIELIK $OSS20 $QWEN32; do
  N=$(echo -n "Faktura korygująca nr 12/2025 na kwotę 4 320,50 zł" | \
      $LB/llama-tokenize -m $MODEL --stdin 2>/dev/null | wc -l)
  echo "$N tokens  $(basename $MODEL)"
done
```

⚠️ **Pitfall P20 (new): do not measure one model's tokens with another model's ruler.**
If you budget context in an agent, **you must count with the tokenizer of the model you
actually use.** Switch the model in `llama-swap` and all your budgets stop being
true. In part 5 we will build a counter that takes the model from the configuration.

### 1.4 What the vocabulary looks like

```bash
$LB/llama-tokenize -m $BIELIK --stdin <<< "test" 2>&1 | head -3
```

⚠️ **This build of `llama-cli` no longer prints `n_vocab`/`BOS`/`EOS` with `-n 0`.**
Older versions of llama.cpp printed a full dump of the model metadata at startup; this build
(commit `987498f`) does not — checked live, `grep` for those fields finds
nothing, regardless of the `-v`/`-lv` level. The metadata lives in the GGUF file itself, so we read it
from there directly — **with no dependency** (no `numpy`, no `gguf` package):

```bash
cat > $KURS/gguf_meta.py <<'EOF'
#!/usr/bin/env python3
"""Minimal GGUF metadata reader - no dependencies.
Usage: python3 gguf_meta.py <file.gguf> [key1 key2 ...]"""
import struct, sys

_SIMPLE = {
    0: ("B", 1), 1: ("b", 1), 2: ("H", 2), 3: ("h", 2),
    4: ("I", 4), 5: ("i", 4), 6: ("f", 4), 7: ("?", 1),
    10: ("Q", 8), 11: ("q", 8), 12: ("d", 8),
}

def _read_str(f):
    (n,) = struct.unpack("<Q", f.read(8))
    return f.read(n).decode("utf-8", "replace")

def _read_value(f, vtype):
    if vtype == 8:                       # string
        return _read_str(f)
    if vtype == 9:                       # array
        (elem_t,) = struct.unpack("<I", f.read(4))
        (n,) = struct.unpack("<Q", f.read(8))
        return [_read_value(f, elem_t) for _ in range(n)]
    fmt, size = _SIMPLE[vtype]
    return struct.unpack("<" + fmt, f.read(size))[0]

def wczytaj_metadane(sciezka: str) -> dict:
    with open(sciezka, "rb") as f:
        magic = f.read(4)
        if magic != b"GGUF":
            sys.exit(f"This is not a GGUF file (magic={magic!r})")
        struct.unpack("<I", f.read(4))               # format version
        (n_tensors,) = struct.unpack("<Q", f.read(8))
        (n_kv,) = struct.unpack("<Q", f.read(8))
        meta = {}
        for _ in range(n_kv):
            klucz = _read_str(f)
            (vtype,) = struct.unpack("<I", f.read(4))
            meta[klucz] = _read_value(f, vtype)
        return meta

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    m = wczytaj_metadane(sys.argv[1])
    if len(sys.argv) > 2:
        for k in sys.argv[2:]:
            print(f"{k} = {m.get(k, '(missing)')}")
    else:
        arch = m.get("general.architecture", "?")
        for pole in ("context_length", "vocab_size", "block_count",
                     "attention.head_count", "attention.head_count_kv",
                     "embedding_length"):
            print(f"{arch}.{pole} = {m.get(f'{arch}.{pole}', '(missing)')}")
        print(f"tokenizer.ggml.bos_token_id = {m.get('tokenizer.ggml.bos_token_id', '(missing)')}")
        print(f"tokenizer.ggml.eos_token_id = {m.get('tokenizer.ggml.eos_token_id', '(missing)')}")
EOF
python3 $KURS/gguf_meta.py $BIELIK
```

Expected (Bielik-11B, measured on this machine):

```
bielik.context_length = 32768
bielik.vocab_size = 32128
bielik.block_count = 50
bielik.attention.head_count = 32
bielik.attention.head_count_kv = 8
bielik.embedding_length = 4096
tokenizer.ggml.bos_token_id = 1
tokenizer.ggml.eos_token_id = 32001
```

🔧 **The GGUF format in brief, so this script is not magic:** a header (`GGUF` + version +
number of tensors + number of key-value pairs), then the pairs themselves — the key as a string,
a type marker (uint32), the value encoded according to that type. `ARRAY` (type 9) carries its own
element type and length. That is enough to walk through the whole file without unpacking
the weights themselves.

Write down `vocab_size` — it returns in §2 as **the length of the logits vector**.

---

## 2. What the model really returns — logits

This is the most important paragraph in this chapter.

> **The model does not generate a word. The model generates a number for EVERY token in the vocabulary.**

One pass (*forward pass*) is:

```
   [your tokens]  ──►  [ network: matrix multiplications ]  ──►  vector of length n_vocab
    e.g. 12 numbers                                              e.g. 128,000 numbers
                                                                 ("logits")
```

Each number says: *"how well this token fits as the next one"*. Unnormalized.
Then the **softmax** function turns them into probabilities that sum to 1.

### 2.1 See the distribution with your own eyes

`llama-server` can return log-probabilities. Start the server:

```bash
# Free the cards if something is hanging on them
pkill -f llama-server; sleep 2

$LB/llama-server -m $BIELIK \
  --host 127.0.0.1 --port 8081 \
  -ngl 999 -c 4096 --no-warmup &
sleep 25   # the model has to load — 11.9 GB
```

🔧 **Flags:** `-ngl 999` = all layers on the GPU (999 means "as many as there are"),
`-c 4096` = a context window of 4096 tokens, `--no-warmup` = don't warm up (faster start).

Now ask for the distribution:

```bash
curl -s http://127.0.0.1:8081/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Stolicą Polski jest",
    "max_tokens": 1,
    "temperature": 0,
    "n_probs": 10
  }' | python3 -m json.tool | head -60
```

⚠️ **The field is named differently than you might guess.** In this build `/v1/completions`
returns the distribution under `choices[0]["logprobs"]["content"][0]["top_logprobs"]` — **in the
OpenAI style**, not the native `completion_probabilities`/`top_probs` of older versions of
llama.cpp. Checked live with curl. Look for this path in the JSON from `python3 -m json.tool`.

⚠️ **And a second pitfall: these are `logprob`, not `prob`.** Each entry carries the **natural
logarithm** of the probability (a negative number; the closer to zero, the more certain the token), not the probability
itself. To get a `p` in the 0–1 range you have to compute `math.exp(logprob)`.
**This is the model's raw distribution** — the ten most probable next
tokens with their log-probabilities.

### 2.2 Read it like an engineer

```bash
curl -s http://127.0.0.1:8081/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Stolicą Polski jest","max_tokens":1,"temperature":0,"n_probs":10}' \
| python3 -c '
import json,math,sys
d=json.load(sys.stdin)
logprobs = (d.get("choices") or [{}])[0].get("logprobs") or {}
content = logprobs.get("content") or []
if not content:
    print("no logprobs.content — check that you passed n_probs>0"); sys.exit()
for t in content[0].get("top_logprobs", []):
    p   = math.exp(t.get("logprob", -999))
    tok = t.get("token", "")
    bar = "#" * int(p*50)
    print(f"{p:6.3f}  {bar:<50} {tok!r}")
'
```

You will see a histogram. **This is the model's "confidence"** — and it is something you can read
programmatically.

💡 **A practical use you won't find in tutorials.** The distribution = a measure of uncertainty.
If the highest probability is 0.98 — the model knows. If it is 0.21 with four similar ones beside it —
the model is guessing. **In an invoice-reading agent this is your "send to a human" signal.**
We come back to it in part 3 (§evaluation) and part 5 (§escalation).

### 2.3 Task: find where the model is uncertain

```bash
for P in "Stolicą Polski jest" "Stawka VAT na książki w Polsce wynosi" "Prezesem NBP w 2025 roku był"; do
  echo "=== $P"
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d "{\"prompt\":\"$P\",\"max_tokens\":1,\"temperature\":0,\"n_probs\":5}" \
  | python3 -c '
import json,math,sys
d=json.load(sys.stdin)
content=((d.get("choices") or [{}])[0].get("logprobs") or {}).get("content") or [{}]
tp=content[0].get("top_logprobs", [])
if tp:
    p=math.exp(tp[0].get("logprob",-999))
    print(f"  highest p={p:.3f}  -> {tp[0].get(\"token\",\"\")!r}")
'
done
```

The third question should have **noticeably lower confidence**. This is a hallucination at the moment
of its birth — you see it as a number before it becomes a sentence.

---

## 3. Sampling — from distribution to word

You have a distribution. You have to pick one token. **This decision does not belong to the model — it belongs to you.**

```
      distribution (n_vocab numbers)
              │
              ├─ temperature   → flatten / sharpen the distribution
              ├─ top-k         → keep the K best
              ├─ top-p         → keep enough so that the sum of p ≥ P
              ├─ min-p         → cut everything below (min_p × p_max)
              ├─ repeat penalty→ lower tokens that already occurred
              │
              ▼
        draw one  (or take the best = greedy)
```

### 3.1 What each parameter does

| Parameter | What it does to the distribution | When to use |
| :-- | :-- | :-- |
| **`temperature`** | divides the logits by T. `T<1` sharpens (more confident), `T>1` flattens (more creative), **`T=0` = always the best** | `0` for precise tasks, `0.7` for writing |
| **`top_k`** | keeps only the K best tokens | `40` typically; `1` = greedy |
| **`top_p`** (nucleus) | keeps the smallest set whose sum of p ≥ P | `0.9`–`0.95` typically |
| **`min_p`** | cuts tokens weaker than `min_p × p_best` | **better than `top_p`** — adapts to the model's confidence; `0.05` |
| **`repeat_penalty`** | penalizes tokens from the last N | `1.1` against looping |

💡 **The most important intuition about `min_p`.** `top_p` always leaves "some" tail, even when the model
is very sure. `min_p` is **relative to the peak**: when the model is sure (p=0.95),
it cuts off almost everything; when it is unsure (p=0.2), it leaves more options. For precise
tasks `min_p` ≫ `top_p`.

### 3.2 Feel the temperature

```bash
for T in 0 0.3 0.8 1.5; do
  echo "=== temperature=$T"
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d "{\"prompt\":\"Opisz jednym zdaniem, czym jest faktura VAT:\",\"max_tokens\":40,\"temperature\":$T,\"seed\":42}" \
  | python3 -c 'import json,sys; print("  "+json.load(sys.stdin)["choices"][0]["text"].strip().replace(chr(10)," "))'
done
```

At `T=0` you get an answer that is correct and boring. At `T=1.5` — increasingly strange.
**Run it a few times** and see that `T=0` always gives the same thing, while `T=1.5` — never.

### 3.3 The same for `min_p` — see why it is better

```bash
for MP in 0.0 0.05 0.3; do
  echo "=== min_p=$MP (temperature=1.0)"
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d "{\"prompt\":\"Stawki VAT w Polsce to:\",\"max_tokens\":50,\"temperature\":1.0,\"min_p\":$MP,\"seed\":7}" \
  | python3 -c 'import json,sys; print("  "+json.load(sys.stdin)["choices"][0]["text"].strip().replace(chr(10)," "))'
done
```

`min_p=0.3` at `temperature=1.0` gives an answer almost as stable as `temperature=0`,
but without the rigidity. **This is the setting you want for data extraction.**

### 3.4 ⚠️ Pitfall P21 (new): sampling is not "style", it is reliability

When the model calls tools in part 5, **every random token is a chance of
broken JSON**. For tool paths:

```
temperature = 0      ← or top_k = 1
repeat_penalty = 1.0 ← the repetition penalty breaks JSON (brackets repeat!)
```

⛔ **`repeat_penalty > 1.0` when generating JSON is a mistake.** JSON *must* repeat
`"`, `{`, `,`. The repetition penalty actively breaks the structure. Remember this — it is one
of the most common, hardest-to-diagnose failures of local agents.

---

## 4. Determinism — why the same prompt gives two answers

### 4.1 The random seed

```bash
# The same seed twice → an identical result
for i in 1 2; do
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d '{"prompt":"Trzy rodzaje kosztów:","max_tokens":30,"temperature":0.8,"seed":1234}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["choices"][0]["text"].strip()[:70])'
done

echo "--- no seed (seed=-1) ---"
for i in 1 2; do
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d '{"prompt":"Trzy rodzaje kosztów:","max_tokens":30,"temperature":0.8,"seed":-1}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["choices"][0]["text"].strip()[:70])'
done
```

### 4.2 ⚠️ But `temperature=0` does NOT guarantee identical results

This surprises everyone. At `temperature=0` the token choice is deterministic — **but
the logits themselves can differ slightly**, because:

1. **The order of floating-point operations on the GPU is not guaranteed.** Parallel
   summation gives results that differ in the last bits.
2. **Batch size changes the computation path.** The same prompt in a different batch →
   different rounding.
3. If two tokens have almost identical logits, **that last-bit difference decides
   the choice** — and the answer diverges from that point on.

💡 **What follows in practice:** don't build tests that compare the model's answer
character by character. Test **properties** (does the JSON parse, is the `kwota` field a number,
does the value fall within a range). We will do that in part 3.

---

## 5. KV-cache — why the second token is free

This is the **most important performance mechanism** in all of local LLM. Without understanding it
you cannot optimize (part 7).

### 5.1 The mechanism

Generation has **two completely different phases**:

```
PHASE 1: PREFILL  (reading your prompt)
   ┌───────────────────────────────────────────────┐
   │ all prompt tokens processed AT ONCE           │
   │ → the GPU computes in parallel, fully used    │
   │ → limit: COMPUTE POWER (FLOPS)                │
   │ → fast: thousands of tokens/s                 │
   └───────────────────────────────────────────────┘
                        │ stores the K and V of every layer
                        ▼
                  [ KV-CACHE in VRAM ]
                        │ read at every step
                        ▼
PHASE 2: DECODING  (writing the answer)
   ┌───────────────────────────────────────────────┐
   │ ONE token at a time, each depends on the prev.│
   │ → the GPU is almost idle, waiting for memory  │
   │ → limit: MEMORY BANDWIDTH                     │
   │ → slow: tens of tokens/s                      │
   └───────────────────────────────────────────────┘
```

**What is in the KV-cache:** for every token already processed, in every layer, the model has
stored its key (K) and value (V) from the attention mechanism. If it did not keep them, every
new token would require recomputing the whole history from scratch — generating 500 tokens
would cost 500 full prefills.

### 5.2 Measure both phases

```bash
curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
  -d '{"prompt":"Wyjaśnij w trzech zdaniach, czym jest amortyzacja:","max_tokens":150,"temperature":0}' \
| python3 -c '
import json,sys
d=json.load(sys.stdin)
t=d.get("timings",{})
print(f"PREFILL:  {t.get(\"prompt_n\",0):5d} tok in {t.get(\"prompt_ms\",0):8.1f} ms  = {t.get(\"prompt_per_second\",0):8.1f} tok/s")
print(f"DECODING: {t.get(\"predicted_n\",0):5d} tok in {t.get(\"predicted_ms\",0):8.1f} ms  = {t.get(\"predicted_per_second\",0):8.1f} tok/s")
pm=t.get("prompt_per_second",0); dm=t.get("predicted_per_second",1)
if dm: print(f"\nPrefill is {pm/dm:.0f}x faster per token than decoding.")
print(f"\nTTFT (time to first token) ~= {t.get(\"prompt_ms\",0):.0f} ms")
'
```

**Write down these two numbers.** The difference will be 20–100×. This is not a curiosity — it is the reason
why:

| Observation | Follows from |
| :-- | :-- |
| a long prompt costs little time | prefill is parallel |
| a long answer costs a lot of time | decoding is sequential |
| **a second card does not speed up a single request** | decoding waits for memory, not for compute |
| **the prompt cache gives huge savings** | you skip prefill entirely (part 7) |

### 5.3 How much VRAM the KV-cache eats — compute it

The formula:

```
KV-cache [bytes] ≈ 2 × n_layers × n_kv_heads × head_dim × n_ctx × bytes_per_element
                    ↑                                              ↑
                 K and V                                   f16 = 2 bytes
```

Take the parameters from the model — with the same GGUF reader as in §1.4 (`llama-cli -n 0 | grep`
will find nothing here, for the same reason as there):

```bash
python3 $KURS/gguf_meta.py $QWEN32
python3 $KURS/gguf_meta.py $QWEN32 qwen3.attention.key_length qwen3.attention.value_length
```

Expected (Qwen3-32B, measured on this machine):

```
qwen3.context_length = 32768
qwen3.vocab_size = (missing)
qwen3.block_count = 64
qwen3.attention.head_count = 64
qwen3.attention.head_count_kv = 8
qwen3.embedding_length = 5120
qwen3.attention.key_length = 128
qwen3.attention.value_length = 128
```

⚠️ **`head_dim` is NOT always `n_embd / n_head`.** Here `5120 / 64 = 80`, while the
real `head_dim` (`attention.key_length`) is **128**. Models with GQA (*grouped-query
attention*, here: 64 query heads against only 8 KV heads) often have a head dimension
independent of this simple division — which is why GGUF stores it **explicitly**, as a separate
field, instead of making everyone compute it. Don't guess — read `key_length`.

And compute:

```bash
python3 - <<'EOF'
# Values READ above from the GGUF file, not computed by hand.
n_layers   = 64      # qwen3.block_count
n_kv_heads = 8        # qwen3.attention.head_count_kv
head_dim   = 128     # qwen3.attention.key_length (NOT n_embd/n_head!)
bytes_el   = 2        # f16

for ctx in (4096, 16384, 32768, 131072):
    b = 2 * n_layers * n_kv_heads * head_dim * ctx * bytes_el
    print(f"n_ctx={ctx:7d}  ->  KV-cache = {b/2**30:7.2f} GiB")
EOF
```

⚠️ **Pitfall P22 (new): context is memory, and you have a finite amount of memory.**
Weights + KV-cache **have to fit together** in 65 GB (two cards). A 20 GB model with a 128k context
may need more KV-cache than weights. That is why `llama-server` sometimes
refuses to start with a large `-c` — **this is not a bug, it is arithmetic**.

### 5.4 How to shrink the KV-cache — three levers

```bash
# 1. KV-cache quantization: f16 -> q8_0 (half the memory)
$LB/llama-server -m $QWEN32 -ngl 999 -c 32768 \
  --cache-type-k q8_0 --cache-type-v q8_0 \
  --port 8082 --host 127.0.0.1 &
```

| Lever | Effect | Cost |
| :-- | :-- | :-- |
| `--cache-type-k/v q8_0` | **½ of KV memory** | minimal quality loss |
| `--cache-type-k/v q4_0` | **¼ of KV memory** | noticeable loss — careful |
| smaller `-c` | linearly less | shorter conversation memory |

💡 **Order of choice:** first `q8_0` on the KV (almost free), then reduce `-c`.
Don't go down to `q4_0` for the KV if you are reading numbers from invoices.

---

## 6. Context — what happens at the boundary

### 6.1 What happens when you overflow the context

Start the server with a **tiny** context to see it right away:

```bash
pkill -f llama-server; sleep 2
$LB/llama-server -m $BIELIK -ngl 999 -c 512 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

# A prompt longer than the context
python3 - <<'EOF'
import json, urllib.request
long_text = "To jest zdanie wypełniające kontekst. " * 200   # ~1400+ tokens
req = urllib.request.Request("http://127.0.0.1:8081/v1/completions",
    data=json.dumps({"prompt": long_text + "\nPodsumuj:", "max_tokens": 20, "temperature": 0}).encode(),
    headers={"Content-Type": "application/json"})
try:
    print(json.load(urllib.request.urlopen(req, timeout=120)))
except Exception as e:
    print("ERROR:", e)
    if hasattr(e, "read"): print(e.read().decode()[:400])
EOF
```

You will get either an error, or a **silent loss of the beginning of the prompt**. The latter is more dangerous.

⚠️ **Pitfall P23 (new): context overflow can be SILENT.**
Some configurations truncate the prompt without a warning. The model answers confidently —
on the basis of text it **did not see in full**. In an agent reading contracts this is the
worst possible failure mode: there is no exception, there is a wrong answer.

🔧 **Defence:** count tokens **before** sending and hard-reject whatever does not fit.
We will build this in part 4 (context budget) and part 5 (compaction).

### 6.2 "Lost in the middle" — position matters

Models remember the **beginning and the end** of the context better than the middle. Check it:

```bash
pkill -f llama-server; sleep 2
$LB/llama-server -m $QWEN32 -ngl 999 -c 8192 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 30

python3 - <<'EOF'
import json, urllib.request

SECRET = "Kod dostępu do archiwum to ZIELONY-7788."
FILLER = "Dokumentacja księgowa jest przechowywana zgodnie z ustawą o rachunkowości. "

def ask(where):
    n = 60
    if where == "poczatek":  body = SECRET + " " + FILLER * n
    elif where == "srodek":  body = FILLER * (n//2) + SECRET + " " + FILLER * (n//2)
    else:                    body = FILLER * n + " " + SECRET
    prompt = body + "\n\nPytanie: Jaki jest kod dostępu do archiwum? Odpowiedz tylko kodem.\nOdpowiedź:"
    req = urllib.request.Request("http://127.0.0.1:8081/v1/completions",
        data=json.dumps({"prompt": prompt, "max_tokens": 20, "temperature": 0}).encode(),
        headers={"Content-Type": "application/json"})
    out = json.load(urllib.request.urlopen(req, timeout=180))["choices"][0]["text"].strip()
    ok = "ZIELONY-7788" in out or "7788" in out
    print(f"{where:10s} -> {'✅' if ok else '❌'}  {out[:60]!r}")

for w in ("poczatek", "srodek", "koniec"):
    ask(w)
EOF
```

💡 **A conclusion to remember for part 4:** in RAG, **don't put the most important fragment
in the middle of the prompt**. Put the most relevant results at the end, closer to the question.

---

## 7. Embeddings — how a model measures meaning

An embedding is turning text into a **vector of numbers**, such that texts with similar meaning have
vectors pointing in a similar direction. It is the foundation of the agent's memory (part 4).

### 7.1 Produce your first vector

```bash
pkill -f llama-server; sleep 2

$LB/llama-embedding -m $BIELIK -p "faktura za usługi księgowe" -ngl 999 --pooling mean 2>/dev/null | head -c 400
echo
```

⚠️ **Two pitfalls on this one line, both checked live.**

1. **`--stdin` does not exist on `llama-embedding`.** Unlike
   `llama-tokenize` (where this flag is simply ignored and the program reads
   `stdin` anyway), here it ends in an explicit error: `error: invalid argument: --stdin`, exit
   code 1. Always **`-p "text"`**.
2. **Piping alone with no flag (`echo … | llama-embedding …`, without `-p`)
   does not give an error — it SILENTLY gives a vector made of nothing but zeros.** It looks like success
   (exit code 0, valid JSON), and the result is useless. This is exactly the kind
   of failure P23 warns about in part 6: **no message, just a
   silently wrong answer.** Check not only the exit code but also whether the vector
   is degenerate.

🔧 **`--pooling mean`** — the model gives one vector **per token**; pooling collapses them into one
vector for the whole text. `mean` = the average (a safe default), `last` = only the last
token, `cls` = the special classification token.

⚠️ **Pitfall P24 (new): a generative model is a poor embedding model.**
Bielik is trained to *write*, not to *measure similarity*. It works, but poorly.
In part 4 we will download a dedicated embedding model (`bge-m3` or `multilingual-e5`), which
is 10× smaller and **clearly better at this one task**. For now we use Bielik only
because you already have it and the point is to understand the mechanism.

### 7.2 Compute the similarity — BY HAND, without numpy

This is the core of "feeling the model". Cosine similarity is:

```
              a · b              sum(aᵢ × bᵢ)
cos(a,b) = ───────────  =  ──────────────────────────
           |a| × |b|      √sum(aᵢ²) × √sum(bᵢ²)
```

Write it yourself:

```bash
mkdir -p $KURS && cat > $KURS/podobienstwo.py <<'EOF'
#!/usr/bin/env python3
"""Cosine similarity of two texts - pure Python, no numpy.

Usage:  python3 podobienstwo.py "text A" "text B"
"""
import math, os, subprocess, sys

LB    = os.path.expanduser("~/llama.cpp/build/bin")
# $BIELIK, if you sourced rig-env.sh in the same shell; otherwise the direct path.
MODEL = os.environ.get("BIELIK",
    os.path.expanduser("~/models/bielik-11b/Bielik-11B-v3.0-Instruct.Q8_0.gguf"))

def embed(text: str) -> list[float]:
    """Returns the embedding vector for the text."""
    # NOTE: "--stdin" on llama-embedding DOES NOT EXIST ("invalid argument" error),
    # and piping alone with no flag SILENTLY gives an all-zero vector. The only
    # working way: -p "text" (checked live, see P24b in the index).
    out = subprocess.run(
        [f"{LB}/llama-embedding", "-m", MODEL, "-p", text,
         "-ngl", "999", "--pooling", "mean", "--embd-output-format", "array"],
        capture_output=True, text=True, timeout=600,
    )
    if out.returncode != 0:
        sys.exit(f"llama-embedding returned {out.returncode}:\n{out.stderr[-500:]}")
    # "array" format => [[x, y, z, ...]]
    import json
    for line in out.stdout.splitlines():
        line = line.strip()
        if line.startswith("[["):
            wektor = json.loads(line)[0]
            if all(abs(x) < 1e-12 for x in wektor):
                sys.exit("an all-zero vector - something went wrong "
                         "(wrong path to the model? check stderr above)")
            return wektor
    # fallback: numbers separated by whitespace
    nums = [float(t) for t in out.stdout.split() if _isnum(t)]
    if not nums:
        sys.exit("could not read the vector from the llama-embedding output")
    return nums

def _isnum(t):
    try: float(t); return True
    except ValueError: return False

def cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity. By hand, so the formula is visible."""
    if len(a) != len(b):
        sys.exit(f"vectors of different lengths: {len(a)} vs {len(b)}")
    dot = 0.0; na = 0.0; nb = 0.0
    for x, y in zip(a, b):
        dot += x * y      # numerator: the dot product
        na  += x * x      # squared length of a
        nb  += y * y      # squared length of b
    if na == 0 or nb == 0:
        return 0.0
    return dot / (math.sqrt(na) * math.sqrt(nb))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    a, b = sys.argv[1], sys.argv[2]
    va, vb = embed(a), embed(b)
    print(f"vector dimension: {len(va)}")
    print(f"cos({a!r},\n    {b!r}) = {cosine(va, vb):.4f}")
EOF
chmod +x $KURS/podobienstwo.py
```

Run it on pairs that **should** and **should not** be similar:

```bash
cd $KURS
python3 podobienstwo.py "faktura za usługi księgowe" "rachunek za prowadzenie księgowości"
python3 podobienstwo.py "faktura za usługi księgowe" "przepis na sernik"
```

The first pair should give a noticeably higher number. **If the difference is small — that is exactly
pitfall P24**: a generative model measures meaning poorly. In part 4 you will see how much
a dedicated model improves it.

### 7.3 What "vector dimension" means

A vector has, say, 4096 numbers. Each one is a single "axis of meaning" — uninterpretable to a human,
but consistent for the model. **Two practical conclusions:**

| Fact | Consequence in part 4 |
| :-- | :-- |
| vectors from different models are **incomparable** | changing the embedding model = **rebuilding the whole database** |
| a 4096 × 4-byte vector = 16 KB per fragment | 100,000 fragments = 1.6 GB — plan your memory |

---

## 8. Quantization — measure the loss, don't guess

Part 1 said "Q4 for large ones, Q8 for small ones". Now you will **measure** what it costs.

### 8.1 Perplexity — a measure of model quality

Perplexity (PPL) tells you how much the model is "surprised" by a text. **Lower = better.**
Formally: the exponential of the mean cross-entropy.

Prepare a test text (in Polish — your target language):

```bash
cat > $KURS/test-ppl.txt <<'EOF'
Ustawa o rachunkowości określa zasady prowadzenia księgi rachunkowej przez jednostki
gospodarcze. Sprawozdanie finansowe składa się z bilansu, rachunku zysków i strat oraz
informacji dodatkowej. Amortyzacja środków trwałych jest dokonywana metodą liniową lub
degresywną. Faktura korygująca zmniejsza lub zwiększa podstawę opodatkowania.
Podatek od towarów i usług rozliczany jest w deklaracji miesięcznej lub kwartalnej.
Zobowiązania krótkoterminowe obejmują kwoty wymagalne w okresie do dwunastu miesięcy.
Kapitał własny to aktywa netto jednostki po odjęciu wszystkich zobowiązań.
Rezerwy tworzy się na pewne lub prawdopodobne przyszłe zobowiązania.
EOF

# Repeat the text so there is something to measure (PPL needs a few hundred tokens)
for i in $(seq 1 30); do cat $KURS/test-ppl.txt; done > $KURS/ppl-duzy.txt
wc -w $KURS/ppl-duzy.txt
```

### 8.2 Measure Bielik (Q8)

```bash
pkill -f llama-server; sleep 2
$LB/llama-perplexity -m $BIELIK -f $KURS/ppl-duzy.txt -ngl 999 -c 2048 2>&1 | tail -5
```

Look for the line `Final estimate: PPL = X`. **Write this number down.**

### 8.3 Compare models

```bash
for MODEL in $BIELIK $OSS20 $QWEN32; do
  echo "=== $(basename $MODEL)"
  $LB/llama-perplexity -m $MODEL -f $KURS/ppl-duzy.txt -ngl 999 -c 2048 2>&1 \
    | grep -E 'Final estimate' || echo "  (not computed)"
  sleep 3
done
```

💡 **How to read the result.** PPL is comparable **only on the same text and the same
`-c`**. Don't compare your number to anything from the internet. Compare **your own measurements with
each other** — that is the only point of this tool in your setup.

⚠️ **PPL measures "predictability of the text", not "usefulness for the task".** A model with a better PPL
on accounting text need not extract amounts from invoices better. **PPL is a preliminary sieve — the real
measure is your own evaluation set from part 3.**

### 8.4 Why you need this in part 7

In part 7 you will **quantize a model yourself** (`llama-quantize`) and you will need a measure of
whether you broke it too much. PPL before and after is exactly that measure.

---

## 9. Exercise — your own generation loop

This is the capstone of the chapter. You will write text generation **token by token**, choosing
each token yourself. After this exercise "the model generates text" stops being magic.

```bash
cat > $KURS/moja-petla.py <<'PYEOF'
#!/usr/bin/env python3
"""Text generation token by token - your own sampling loop.

Requires a running llama-server:
  $LB/llama-server -m $BIELIK -ngl 999 -c 2048 --port 8081 --host 127.0.0.1

Usage:  python3 moja-petla.py "Your prompt"
"""
import json, math, random, sys, urllib.request

SERVER = "http://127.0.0.1:8081"

def next_token_distribution(prompt: str, n_probs: int = 40):
    """One forward pass. Returns a list of (token_str, probability)."""
    body = {
        "prompt": prompt,
        "max_tokens": 1,
        "temperature": 1.0,   # we do NOT sample on the server side...
        "top_k": 0,           # ...we want the raw distribution
        "top_p": 1.0,
        "min_p": 0.0,
        "n_probs": n_probs,
    }
    req = urllib.request.Request(SERVER + "/v1/completions",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=120))
    # Shape in this build: choices[0].logprobs.content[0].top_logprobs,
    # each entry carries a logprob (natural log), NOT a prob directly - hence math.exp().
    choices = d.get("choices") or [{}]
    content = (choices[0].get("logprobs") or {}).get("content") or []
    if not content:
        return []
    raw = content[0].get("top_logprobs") or []
    return [(t.get("token", ""), math.exp(t.get("logprob", -999.0))) for t in raw]

def apply_temperature(dist, temperature):
    """Rescale the distribution. T<1 sharpens, T>1 flattens."""
    if temperature <= 0:                       # greedy
        return [max(dist, key=lambda x: x[1])] if dist else []
    # p -> p^(1/T), then renormalize
    scaled = [(t, p ** (1.0 / temperature)) for t, p in dist if p > 0]
    s = sum(p for _, p in scaled)
    return [(t, p / s) for t, p in scaled] if s > 0 else []

def apply_min_p(dist, min_p):
    """Cut tokens weaker than min_p * p_best."""
    if not dist or min_p <= 0:
        return dist
    top = max(p for _, p in dist)
    kept = [(t, p) for t, p in dist if p >= min_p * top]
    s = sum(p for _, p in kept)
    return [(t, p / s) for t, p in kept] if s > 0 else dist

def apply_top_k(dist, k):
    """Keep the K best."""
    if not dist or k <= 0:
        return dist
    kept = sorted(dist, key=lambda x: x[1], reverse=True)[:k]
    s = sum(p for _, p in kept)
    return [(t, p / s) for t, p in kept] if s > 0 else dist

def sample(dist, rng):
    """Draw a token according to the distribution (roulette wheel)."""
    if not dist:
        return None
    r = rng.random()
    acc = 0.0
    for t, p in dist:
        acc += p
        if r <= acc:
            return t
    return dist[-1][0]

def generate(prompt, n_tokens=40, temperature=0.7, top_k=40, min_p=0.05, seed=42, verbose=True):
    rng = random.Random(seed)
    text = prompt
    for step in range(n_tokens):
        dist = next_token_distribution(text)
        if not dist:
            print("\n[end: the server returned no distribution]"); break

        before_top = max(dist, key=lambda x: x[1])

        d = apply_temperature(dist, temperature)
        d = apply_top_k(d, top_k)
        d = apply_min_p(d, min_p)

        tok = sample(d, rng)
        if tok is None or tok == "":
            print("\n[end: empty token]"); break

        if verbose and step < 8:
            print(f"  step {step:2d}: candidates {len(dist):3d} -> after filters {len(d):3d} | "
                  f"best {before_top[0]!r} p={before_top[1]:.3f} | CHOSEN {tok!r}")

        text += tok
        sys.stdout.write(tok); sys.stdout.flush()
    print()
    return text

if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Amortyzacja środka trwałego to"
    print(f"PROMPT: {prompt!r}\n")
    print("--- the first 8 steps in detail ---")
    generate(prompt)
PYEOF
chmod +x $KURS/moja-petla.py
```

Run it:

```bash
pkill -f llama-server; sleep 2
$LB/llama-server -m $BIELIK -ngl 999 -c 2048 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

cd $KURS && python3 moja-petla.py "Amortyzacja środka trwałego to"
```

**What you will see:** for the first eight steps it prints how many candidates there were, how many remained after
your filters, and which token you picked. After that the text just flows.

### 9.1 Tasks for this loop

1. Set `temperature=0` — confirm the result is identical on every run.
2. Set `min_p=0.5` at `temperature=1.2` — see that despite the high temperature the text
   stays sensible. **This is the proof of why `min_p` is better than `top_p`.**
3. Set `top_k=1` — compare with `temperature=0`. Is it the same? (Yes — and now you know why.)
4. Change `seed` — see that at `temperature>0` you get a different text, at `0` the same one.

⚠️ **This loop is slow** — one HTTP request per token. That is **deliberate**: you see the cost of
each token separately. In real use the server runs the whole loop internally, without network
overhead, with the KV-cache kept between steps.

---

## Check yourself

Before you move on to part 3, answer **without looking**:

- [ ] Why does Polish text eat more context than English text with the same content?
- [ ] What exactly does a single forward pass of the model return?
- [ ] Why does `repeat_penalty > 1.0` break JSON generation?
- [ ] Why does `temperature=0` **not** guarantee bit-identical results?
- [ ] Which phase — prefill or decoding — is limited by memory bandwidth?
- [ ] Why does a second card not speed up a single request?
- [ ] What happens if you change the embedding model after building the vector database?
- [ ] Why is PPL not enough as a measure of a model's usefulness for your task?

## New pitfalls from this chapter

| ID | Pitfall | § |
| :-- | :-- | :-- |
| **P20** | Counting tokens with a tokenizer other than that of the model in use | §1.3 |
| **P21** | `repeat_penalty > 1.0` when generating JSON — breaks the structure | §3.4 |
| **P22** | Context is VRAM: weights + KV-cache must fit together | §5.3 |
| **P23** | Context overflow can be **silent** — a confident answer on truncated data | §6.1 |
| **P24** | A generative model as an embedding model — works poorly | §7.1 |

---

**Next part: `03-CONTROL-AND-RELIABILITY.md`** — how to force a local model to
**always** return valid JSON. This is the difference between a demo and a product.
