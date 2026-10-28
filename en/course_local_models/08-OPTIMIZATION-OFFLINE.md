# Part 8 — Offline optimization: make it fast on your own hardware

**Level: ⭐⭐⭐⭐⭐** · Requires: parts 2, 6, 7 · Time: ~7 h

> **Why this chapter.** You have a working, safe agent. It is too slow.
> An agent that thinks for 40 seconds per turn and needs 15 turns takes 10 minutes per task —
> unusable.
>
> This chapter is **measurement and levers**. We start by measuring where the time goes, and then
> go through them one by one: prompt cache, **speculative decoding** (you already have a model for it!), model
> routing, your own quantization, LoRA and a plan for four cards.

```bash
cd ~/llm-education   # the repository directory (yours may differ)
source rig-env.sh
```

⚠️ **One rule for the whole chapter: DO NOT OPTIMIZE WITHOUT MEASURING.**
Every section starts with a number before and ends with a number after. Without that it is not engineering,
it is superstition.

---

## Table of contents

| § | Lever | Typical gain |
| :-- | :-- | --: |
| [1](#1-measure-first--where-the-time-goes) | **Baseline measurement** | — |
| [2](#2-prompt-cache-and-kv-reuse) | **Prompt cache** | ⭐ **2–10×** on TTFT |
| [3](#3-speculative-decoding) | **Speculative decoding** | ⭐ **1.5–3×** on tok/s |
| [4](#4-model-routing--small-for-easy) | **Model routing** | 2–5× on a typical turn |
| [5](#5-your-own-quantization) | **Your own quantization** | memory + speed |
| [6](#6-lora--teach-the-model-your-domain) | **LoRA** | quality without a bigger model |
| [7](#7-parallelism-and-batches) | **Parallelism** | throughput |
| [8](#8-plan-for-four-cards) | **Four cards** | capacity, not speed |
| [9](#9-decision-table) | **Summary** | what to do first |

---

## 1. Measure first — where the time goes

### 1.1 `llama-bench` — clean measurement

```bash
export HIP_VISIBLE_DEVICES=0,1
pkill -f llama-server; sleep 2

$LB/llama-bench -m $OSS20 -ngl 999 -p 512 -n 128 -r 3 -o md
```

You will see a table with two key columns:

| Test | What it measures | Limited by |
| :-- | :-- | :-- |
| **`pp512`** | prefill of 512 tokens | compute power |
| **`tg128`** | generation of 128 tokens | memory bandwidth |

⭐ **`tg` (decoding) is the number the user feels.** `pp` (prefill) is almost always
fast. When optimizing, look at `tg` — and at TTFT (§2).

### 1.2 Compare all your models

```bash
cat > $KURS/bench-wszystko.sh <<'EOF'
#!/usr/bin/env bash
source $LLMEDU/rig-env.sh
export HIP_VISIBLE_DEVICES=0,1
OUT=$KURS/bench-$(date +%Y%m%d-%H%M).md
echo "# Baseline measurement $(date)" > $OUT
echo "" >> $OUT
echo "llama.cpp: $(cd ~/llama.cpp && git log -1 --format='%h %ad' --date=short)" >> $OUT
echo "" >> $OUT

for M in "$OSS20" "$QWEN32" "$BIELIK"; do
  echo "## $(basename $M)" | tee -a $OUT
  $LB/llama-bench -m "$M" -ngl 999 -p 512 -n 128 -r 3 -o md 2>/dev/null | tee -a $OUT
  echo "" >> $OUT
  sleep 5
done
echo "Saved: $OUT"
EOF
chmod +x $KURS/bench-wszystko.sh
$KURS/bench-wszystko.sh
```

💡 **Save results with the date and the llama.cpp commit.** You already have a habit for this
(`results/all-benchmark-results.md`) — stick to it. In three months you will want to
know whether the new llama.cpp version improved anything.

### 1.3 Measuring the agent — this is the metric that counts

`llama-bench` measures the model. **You need to measure the agent.**

```bash
cat > $AGENT/pomiar-agenta.py <<'PYEOF'
#!/usr/bin/env python3
"""Measures the agent on a set of tasks. This is the metric that counts."""
import json, os, statistics, subprocess, sys, time

ZADANIA = [
    "List the .py files in the working directory.",
    "Write a hello.py file that prints 'hello' and run it.",
    "Count how many lines each .py file in the working directory has.",
    "In hello.py change the text to 'good morning' and run it again.",
    "Check whether the directory has a vat.py file; if so, give the names of its functions.",
]

def uruchom(zadanie: str) -> dict:
    t0 = time.time()
    r = subprocess.run([sys.executable, os.path.join(os.environ["AGENT"], "agent.py"),
                        zadanie, "--bez-zgod"],
                       capture_output=True, text=True, timeout=1200)
    dt = time.time() - t0
    # Find the log from this run
    kat = os.path.join(os.environ["AGENT"], "dzienniki")
    pliki = sorted(os.listdir(kat)) if os.path.isdir(kat) else []
    tury = bledy = 0
    ms_modelu = []
    if pliki:
        for l in open(os.path.join(kat, pliki[-1]), encoding="utf-8"):
            try: rek = json.loads(l)
            except json.JSONDecodeError: continue
            if rek["typ"] == "krok":
                tury += 1
                if rek.get("ms"): ms_modelu.append(rek["ms"])
                if str(rek["wynik"]).startswith(("BŁĄD", "ODMOWA")): bledy += 1
    return {"sekundy": dt, "tury": tury, "bledy": bledy,
            "ms_modelu_suma": sum(ms_modelu),
            "udane": r.returncode == 0 and "Przerwano" not in r.stdout}

def main():
    wyniki = []
    for i, z in enumerate(ZADANIA, 1):
        print(f"[{i}/{len(ZADANIA)}] {z[:60]}...", flush=True)
        w = uruchom(z); wyniki.append(w)
        udzial = 100 * w["ms_modelu_suma"] / 1000 / w["sekundy"] if w["sekundy"] else 0
        print(f"      {w['sekundy']:6.1f}s  {w['tury']:2d} turns  {w['bledy']} errors  "
              f"model={udzial:.0f}% of time  {'✅' if w['udane'] else '❌'}")

    print(f"\n{'='*56}\nSUMMARY")
    print(f"  successful:       {sum(w['udane'] for w in wyniki)}/{len(wyniki)}")
    print(f"  median time:      {statistics.median(w['sekundy'] for w in wyniki):.1f}s")
    print(f"  median turns:     {statistics.median(w['tury'] for w in wyniki):.0f}")
    print(f"  total errors:     {sum(w['bledy'] for w in wyniki)}")
    calosc = sum(w['sekundy'] for w in wyniki)
    model  = sum(w['ms_modelu_suma'] for w in wyniki) / 1000
    print(f"  time in model:    {model:.0f}s of {calosc:.0f}s = {100*model/calosc:.0f}%")
    print(f"\n  ⭐ This is your baseline number. Write it down.")

if __name__ == "__main__":
    main()
PYEOF

pkill -f llama-server; sleep 2
$LB/llama-server -m $OSS20 -ngl 999 -c 16384 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25
cd $AGENT && python3 pomiar-agenta.py | tee $AGENT/pomiar-bazowy.txt
```

⭐ **Write down "time in model %".** If it is 85% — optimize the model (§2–§5). If it is 30% —
your problem is in the number of turns, that is in the harness and the prompt, **not in the speed of the model**.
That one percentage decides which half of this chapter you should read at all.

---

## 2. Prompt cache and KV reuse

⭐ **The biggest lever for an agent.** And the most underrated.

### 2.1 Why it works so well for an agent

Recall part 2 §5: prefill is expensive, but you do it **once per prompt**. On every turn
the agent sends:

```
[system prompt: 1200 tok]     ← IDENTICAL every time
[history: 3000 tok]           ← ONLY GROWS, the beginning does not change
[new observation: 300 tok]    ← the only new part
```

Without a cache the model recomputes **4500 tokens** every time. With a cache — **300**.

```
turn  1: prefill 1500 tok
turn  2: prefill 1800 tok   ← 1500 from cache, 300 new
turn  3: prefill 2100 tok   ← 1800 from cache, 300 new
...
turn 15: prefill 6000 tok   ← 5700 from cache, 300 new
```

### 2.2 Turn it on

```bash
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1

$LB/llama-server -m $OSS20 \
  -ngl 999 -c 32768 \
  --cache-reuse 256 \
  --slot-save-path $AGENT/kv-cache \
  -np 1 \
  --host 127.0.0.1 --port 8081 --no-warmup &
sleep 25
```

| Flag | What it does |
| :-- | :-- |
| **`--cache-reuse 256`** | ⭐ lets it reuse KV chunks by shifting them; `256` = minimum chunk |
| **`--slot-save-path`** | saves the KV cache to disk — **survives a server restart** |
| `-np 1` | one slot = maximum cache per session (see §7) |
| `--keep N` | how many tokens at the start to always keep |

### 2.3 Measure the gain

```bash
cat > $KURS/zmierz-cache.py <<'PYEOF'
#!/usr/bin/env python3
"""Measures TTFT with a growing history - with and without cache."""
import json, time, urllib.request

SRV = "http://127.0.0.1:8081"
SYSTEM = ("You are an agent. " + "You have tools for working with files and the shell. " * 40)

def tura(hist):
    t0 = time.time()
    req = urllib.request.Request(SRV + "/v1/chat/completions",
        data=json.dumps({"messages": hist, "max_tokens": 20,
                         "temperature": 0, "cache_prompt": True}).encode(),
        headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    dt = time.time() - t0
    u = r.get("usage", {})
    return dt, u.get("prompt_tokens", 0), r["choices"][0]["message"]["content"]

hist = [{"role": "system", "content": SYSTEM}]
print(f"{'turn':>4}  {'prompt tok':>12}  {'time':>8}  {'prefill tok/s':>14}")
for i in range(1, 11):
    hist.append({"role": "user", "content":
                 f"Step {i}: read file number {i} and give its size. " * 6})
    dt, tok, odp = tura(hist)
    hist.append({"role": "assistant", "content": odp})
    print(f"{i:4d}  {tok:12d}  {dt:7.2f}s  {tok/dt:14.0f}")
print("\n⭐ If the cache works: time stays FLAT despite the growing number of tokens.")
print("   If it grows linearly - the cache is not working; check --cache-reuse and cache_prompt.")
PYEOF

python3 $KURS/zmierz-cache.py
```

⭐ **Interpretation:** the `time` column should stay **almost flat**, even though
`prompt tok` grows from 1500 to 6000. If it grows linearly — the cache is not working.

### 2.4 ⚠️ What kills the cache — trap P46 (new)

The cache is **prefix matching**. A single change at the beginning invalidates everything after it.

| Cache killer | Why | Fix |
| :-- | :-- | :-- |
| **timestamp in the system prompt** | the prefix differs every time | put the time **at the end**, in the `user` message |
| **notebook appended to `system`** | it grows → the prefix changes | ⚠️ see below |
| `json.dumps()` without `sort_keys=True` | key order is random | always `sort_keys=True` |
| changing the tool set mid-session | tools sit at the beginning | fix the set at session start |
| history compaction | rewrites the middle | unavoidable — the cache rebuilds after it |

⚠️ **A conflict you created for yourself in part 6.**
In `agent.py` you rebuild the system prompt on every compaction, appending the notebook:

```python
hist[0] = {"role": "system", "content": self._prompt_systemowy()}  # ← kills the cache
```

**Fix:** keep the system prompt **frozen**, and insert the notebook as a **separate
message after the history**:

```bash
cd $AGENT && python3 - <<'PYEOF'
import os
p = os.path.join(os.environ["AGENT"], "agent.py")
s = open(p, encoding="utf-8").read()

# 1. System prompt without the notebook = frozen prefix
s = s.replace(
    '        notatki = self.notes.jako_tekst()\n'
    '        if notatki:\n'
    '            czesci += ["", notatki]\n'
    '        return "\\n".join(czesci)',
    '        return "\\n".join(czesci)   # WITHOUT the notebook — frozen prefix (P46)')

# 2. Notebook as the last message before querying the model
s = s.replace(
    '            try:\n                surowy, ms = self._zapytaj(hist)',
    '            notatki = self.notes.jako_tekst()\n'
    '            do_modelu = hist + ([{"role": "user", "content": notatki}] if notatki else [])\n'
    '            try:\n                surowy, ms = self._zapytaj(do_modelu)')

# 3. Compaction does not rebuild the system prompt
s = s.replace(
    '                hist[0] = {"role": "system", "content": self._prompt_systemowy()}\n', '')

open(p, "w", encoding="utf-8").write(s)
print("fixed: system prompt frozen, notebook at the end")
PYEOF

# Measure again
python3 $AGENT/pomiar-agenta.py | tee $AGENT/pomiar-po-cache.txt
diff <(grep median $AGENT/pomiar-bazowy.txt) <(grep median $AGENT/pomiar-po-cache.txt)
```

---

## 3. Speculative decoding

⭐ **You already have a model for it.** `~/models/gpt-oss-120b/eagle3-gpt-oss-120b-Q8_0.gguf`,
849 MB — this is an **EAGLE3 draft model**.

### 3.1 How it works

```
WITHOUT SPECULATION:
  big model: token → token → token → token       (each = a full pass)

WITH SPECULATION:
  small model: drafts 5 tokens ahead  (cheap, 849 MB)
  big model:   verifies ALL 5 AT ONCE (one pass!)
               ├─ 4 agree → accept 4, reject 1
               └─ 0 agree → accept 1 (its own), minimal loss
```

⭐ **Why this is a free lunch.** Verifying 5 tokens at once costs the same as
generating one — because it is **prefill** (parallel), not decoding (sequential).
This is a direct application of the asymmetry from part 2 §5.

💡 **Key point: the result is IDENTICAL** to the one without speculation (with the same seed).
It is not an approximation — the big model accepts a token only if it would have chosen it itself.
**Zero quality cost.**

### 3.2 Run it

⚠️ **The draft model must have the same tokenizer as the main one.** `eagle3-gpt-oss-120b`
is a draft for **gpt-oss** — use it with `gpt-oss-20b`, **not with Qwen or Bielik**.
⚠️ `gpt-oss-120b` as the target model **does not fit on this machine today** (see
§8.1 below — 59 GiB of weights with 65 GiB of VRAM leaves too little room for the KV cache) — it is an option
for AFTER the upgrade to four cards, not now.

```bash
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1

$LB/llama-server -m $OSS20 \
  -md $DRAFT \
  -ngl 999 -ngld 999 \
  -c 16384 \
  --spec-draft-n-max 5 \
  --spec-draft-n-min 1 \
  --spec-draft-p-min 0.75 \
  --cache-reuse 256 \
  --host 127.0.0.1 --port 8081 --no-warmup &
sleep 30
```

| Flag | Meaning |
| :-- | :-- |
| **`-md`** (`--spec-draft-model`) | path to the draft model |
| `-ngld 999` | draft layers on the GPU (separately from `-ngl`) |
| **`--spec-draft-n-max 5`** | how many tokens to draft ahead |
| `--spec-draft-n-min 1` | minimum |
| **`--spec-draft-p-min 0.75`** | draft only when the draft is confident ≥ 0.75 |

⚠️ **The old flags `--draft-max` / `--draft-min` were REMOVED** in this version.
Use `--spec-draft-n-max` / `--spec-draft-n-min`. If you see a tutorial with the old ones —
it is out of date.

### 3.3 Measure the gain

```bash
cat > $KURS/zmierz-spekulacje.py <<'PYEOF'
#!/usr/bin/env python3
"""Measures tok/s and the draft acceptance rate."""
import json, urllib.request

SRV = "http://127.0.0.1:8081"
PROMPTY = [
    "Write a Python function that computes the gross amount from the net amount and the VAT rate.",
    "Explain in five sentences what straight-line depreciation is.",
    "List in bullet points five mandatory elements of a VAT invoice.",
]

for p in PROMPTY:
    req = urllib.request.Request(SRV + "/v1/completions",
        data=json.dumps({"prompt": p, "max_tokens": 200, "temperature": 0}).encode(),
        headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    t = r.get("timings", {})
    print(f"\n{p[:56]}...")
    print(f"  decoding: {t.get('predicted_per_second',0):7.1f} tok/s "
          f"({t.get('predicted_n',0)} tok in {t.get('predicted_ms',0):.0f} ms)")
    # llama-server reports draft statistics, if available
    for k in ("draft_n", "draft_n_accepted", "n_draft", "n_draft_accepted"):
        if k in t:
            print(f"  {k}: {t[k]}")
    if "draft_n" in t and t["draft_n"]:
        acc = 100 * t.get("draft_n_accepted", 0) / t["draft_n"]
        print(f"  draft acceptance: {acc:.0f}%")
PYEOF

python3 $KURS/zmierz-spekulacje.py
```

Now compare **without** the draft:

```bash
pkill -f llama-server; sleep 3
$LB/llama-server -m $OSS20 -ngl 999 -c 16384 --cache-reuse 256 \
  --host 127.0.0.1 --port 8081 --no-warmup &
sleep 25
python3 $KURS/zmierz-spekulacje.py
```

### 3.4 How to read the acceptance rate

| Acceptance | What to do |
| :-- | :-- |
| **> 70%** | ⭐ great — **raise `--spec-draft-n-max` to 8** |
| 40–70% | good, leave it as it is |
| 20–40% | lower `n-max` to 3; raise `p-min` to 0.85 |
| **< 20%** | the draft does not fit — **check that the tokenizers are the same** |

💡 **Acceptance depends on the content.** Code and formal text have a high rate (predictable),
creative writing a low one. **Measure on your real prompts**, not on examples.

### 3.5 ⚠️ Trap P47 (new): the draft eats VRAM and can slow things down

The draft model keeps **its own weights and its own KV cache**. With tight memory:
1. it takes room from the main model → smaller context,
2. with low acceptance it **slows things down** (you pay for the draft and gain nothing).

**Always measure both configurations.** 849 MB is cheap, but not free.

---

## 4. Model routing — small for easy

The agent in part 6 uses one model for everything. **Most turns are simple decisions.**

### 4.1 Division of labour

| Turn type | Model | Why |
| :-- | :-- | :-- |
| tool choice (grammar enforces the format) | ⭐ **small** | a choice from an enum — a small model is enough |
| summary of an observation | small | mechanical task |
| **multi-step plan** | **large** | reasoning is needed here |
| **error diagnosis** | **large** | reasoning is needed here |
| final answer for a human | large | language quality is visible |

```bash
cat > $AGENT/router.py <<'PYEOF'
#!/usr/bin/env python3
"""Routing between two model servers: small (fast) and large (smart)."""
import json, re, urllib.request

MALY = "http://127.0.0.1:8081"     # gpt-oss-20b
DUZY = "http://127.0.0.1:8082"     # qwen3-32b

# Signals that the large model is needed (the patterns match the Polish-language prompts)
SYGNALY_TRUDNE = [
    r"(?i)\bdlaczego\b", r"(?i)\bzdiagnozuj\b", r"(?i)\bzaprojektuj\b",
    r"(?i)\bporownaj\b", r"(?i)\bzaplanuj\b", r"(?i)\bwyjasnij\b",
    r"(?i)\bBŁĄD\b.*\bBŁĄD\b",          # many errors in the history
]

def wybierz(messages: list[dict], ostatnie_bledy: int = 0,
            tura: int = 1) -> tuple[str, str]:
    """Returns (url, reason)."""
    if ostatnie_bledy >= 2:
        return DUZY, f"{ostatnie_bledy} errors in a row — diagnosis needed"
    if tura == 1:
        return DUZY, "first turn: planning"
    ogon = " ".join(m["content"][:1500] for m in messages[-3:])
    for s in SYGNALY_TRUDNE:
        if re.search(s, ogon):
            return DUZY, f"difficulty signal: {s}"
    dlugosc = sum(len(m["content"]) for m in messages)
    if dlugosc > 40000:
        return DUZY, "long context — the small model loses the thread"
    return MALY, "routine turn"

def zapytaj(url: str, messages: list[dict], schema: dict | None = None,
            max_tokens: int = 900) -> str:
    body = {"messages": messages, "max_tokens": max_tokens,
            "temperature": 0, "repeat_penalty": 1.0, "cache_prompt": True}
    if schema:
        body["response_format"] = {"type": "json_schema", "json_schema": {"schema": schema}}
    req = urllib.request.Request(url + "/v1/chat/completions",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=600))
    return r["choices"][0]["message"]["content"]

def zywy(url: str) -> bool:
    try:
        urllib.request.urlopen(url + "/health", timeout=3); return True
    except Exception:
        return False

if __name__ == "__main__":
    for u, n in ((MALY, "small"), (DUZY, "large")):
        print(f"{n:6s} {u}  {'✅ alive' if zywy(u) else '❌ missing'}")
    print()
    for tura, bledy, tresc in ((1, 0, "Napisz test."),
                               (5, 0, "Przeczytaj plik."),
                               (5, 0, "Dlaczego test nie przechodzi?"),
                               (7, 3, "Spróbuj jeszcze raz.")):
        url, powod = wybierz([{"role": "user", "content": tresc}], bledy, tura)
        print(f"turn={tura} errors={bledy}  → {'LARGE' if url == DUZY else 'small'}  ({powod})")
PYEOF

# Run both servers at once - both fit in 65 GB
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1

$LB/llama-server -m $OSS20 -md $DRAFT -ngl 999 -ngld 999 -c 16384 \
  --spec-draft-n-max 5 --cache-reuse 256 \
  --host 127.0.0.1 --port 8081 --no-warmup &
sleep 28

$LB/llama-server -m $QWEN32 -ngl 999 -c 16384 --cache-reuse 256 \
  --host 127.0.0.1 --port 8082 --no-warmup &
sleep 40

python3 $AGENT/router.py
```

⚠️ **Trap P48 (new): routing invalidates the prompt cache.**
Each server has **its own** KV cache. A jump from small to large = a cold prefill.
**The router must be lazy:** once you jump to the large one, **stay there until the end of the task**.
Do not jump back and forth every turn — you will pay more for prefill than you gain.

---

## 5. Your own quantization

You download a ready-made `Q4_K_M` because someone made it. **You can make a better one** — tailored to
your language and domain.

### 5.1 Why your own quantization is better

The "K" quantization uses an **importance matrix** (*importance matrix*): which weights matter,
and which can be rounded more aggressively. The matrix is computed from **calibration text**.

⭐ **Public quants are calibrated on English.** You read Polish invoices.
**Calibration on Polish accounting text gives a measurably better model at the same
size.**

### 5.2 Build the calibration text

```bash
mkdir -p $KURS/kalibracja

# Gather your real domain text (your own notes and the documents from part 4)
cat ~/path/to/your/notes/*.md \
    $KURS/dokumenty/*.md \
    2>/dev/null > $KURS/kalibracja/domena.txt

# Add Polish accounting text
cat >> $KURS/kalibracja/domena.txt <<'EOF'
Faktura VAT nr FV/2025/09/0143 z dnia 15 września 2025 roku.
Sprzedawca: Biuro Rachunkowe ALFA spółka z ograniczoną odpowiedzialnością.
Numer identyfikacji podatkowej NIP 1234567890.
Wartość netto 1 200,00 zł, podatek VAT 23% w kwocie 276,00 zł, brutto 1 476,00 zł.
Amortyzacja środków trwałych metodą liniową według stawki 20% rocznie.
Księga przychodów i rozchodów prowadzona jest w formie elektronicznej.
Deklaracja JPK_V7M składana jest do 25 dnia miesiąca następującego po okresie rozliczeniowym.
Zobowiązania krótkoterminowe obejmują kwoty wymagalne w okresie do dwunastu miesięcy.
Kapitał własny stanowi różnicę między aktywami a zobowiązaniami jednostki.
Rezerwy tworzy się na pewne lub prawdopodobne przyszłe zobowiązania.
Sprawozdanie finansowe składa się z bilansu, rachunku zysków i strat oraz informacji dodatkowej.
Faktura korygująca zmniejsza lub zwiększa podstawę opodatkowania podatkiem od towarów i usług.
EOF

# Duplicate it to get enough material (imatrix needs hundreds of thousands of tokens)
for i in $(seq 1 12); do cat $KURS/kalibracja/domena.txt; done \
  > $KURS/kalibracja/pelny.txt
wc -c $KURS/kalibracja/pelny.txt
```

💡 **The more the calibration text resembles your real input, the better.**
Ideally: drop in anonymized, real documents the agent will work with.

### 5.3 Compute the importance matrix

⚠️ **`--in-file` is NOT the flag for calibration text** — checked with `--help`. That flag loads a **ready, earlier** `imatrix.gguf` matrix (for combining several runs), not raw text. The flag for text is `-f`/`--file` — the same one `llama-perplexity` uses elsewhere in this chapter.

```bash
export HIP_VISIBLE_DEVICES=0,1
pkill -f llama-server; sleep 2

$LB/llama-imatrix \
  -m $QWEN32 \
  -f $KURS/kalibracja/pelny.txt \
  -o $KURS/kalibracja/qwen32-pl.imatrix.gguf \
  --output-format gguf \
  -ngl 999 -c 2048 \
  --chunks 100

ls -la $KURS/kalibracja/
```

⚠️ **This will take a while.** Ten to a few dozen minutes depending on `--chunks`.
Start with `--chunks 50` to see that the process goes through.

### 5.4 Quantize

```bash
mkdir -p ~/models/wlasne

# NOTE: llama-quantize works on a model of HIGHER precision.
# You already have Qwen32 as Q4_K_M - you cannot make a better Q4 from it.
# For a real experiment you need F16/BF16. Here I show the mechanics
# on the example of Q4_K_M -> Q3_K_M (going down always works):

$LB/llama-quantize \
  --imatrix $KURS/kalibracja/qwen32-pl.imatrix.gguf \
  $QWEN32 \
  ~/models/wlasne/qwen32-Q3_K_M-pl.gguf \
  Q3_K_M

ls -lh ~/models/wlasne/
```

💡 **To make your own `Q4_K_M` better than the public one**, download the `F16`
(or `BF16`) version of the model and quantize from it. These are large files (32B in F16 ≈ 65 GB) — you have 1.5 TB,
so you can.

### 5.5 ⭐ Check that you did not break it — PPL as a quality gate

```bash
# The test text MUST be DIFFERENT from the calibration text!
cat > $KURS/kalibracja/test.txt <<'EOF'
Rozliczenie roczne podatku dochodowego od osób fizycznych składa się
w terminie do trzydziestego kwietnia roku następującego po roku podatkowym.
Koszty uzyskania przychodu obejmują wydatki poniesione w celu osiągnięcia
przychodów lub zachowania albo zabezpieczenia źródła przychodów.
Ewidencja środków trwałych zawiera datę przyjęcia do używania, wartość
początkową oraz stawkę amortyzacyjną.
Spis z natury przeprowadza się na koniec roku obrotowego.
EOF
for i in $(seq 1 30); do cat $KURS/kalibracja/test.txt; done > $KURS/kalibracja/test-duzy.txt

for M in $QWEN32 ~/models/wlasne/qwen32-Q3_K_M-pl.gguf; do
  echo "=== $(basename $M) ($(du -h $M | cut -f1))"
  $LB/llama-perplexity -m $M -f $KURS/kalibracja/test-duzy.txt \
    -ngl 999 -c 2048 2>&1 | grep -E 'Final estimate'
  sleep 3
done
```

⚠️ **Trap P49 (new): do not measure PPL on the calibration text.**
The quantization was **fitted** to that text — the result will be artificially good. **The test text
must be disjoint from the calibration text**, otherwise you are measuring yourself.

### 5.6 And above all: measure with the suite from part 3

```bash
pkill -f llama-server; sleep 2
$LB/llama-server -m ~/models/wlasne/qwen32-Q3_K_M-pl.gguf \
  -ngl 999 -c 4096 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 30
python3 $KURS/eval/uruchom.py
```

⭐ **PPL is a preliminary sieve. Your evaluation suite is the real measure.** A model may have
a better PPL and be worse at extracting amounts — and the latter is what you are selling.

---

## 6. LoRA — teach the model your domain

`llama-finetune` lets you **fine-tune a model** on your data without changing the base weights.

### 6.1 When LoRA makes sense and when it does not

| ✅ LoRA will help | ❌ LoRA will not help |
| :-- | :-- |
| the model does not know the format of your documents | the model does not know facts → **use RAG (part 4)** |
| you want a consistent answer style | you want valid JSON → **use grammars (part 3)** |
| industry terminology is being lost | the model is simply too small → **take a bigger one** |

⚠️ **LoRA is not a way to add knowledge.** RAG is for knowledge. LoRA changes **behaviour
and style**. Mixing these two up is the most common misunderstanding.

### 6.2 Prepare the training data

```bash
mkdir -p $KURS/lora

cat > $KURS/lora/dane.txt <<'EOF'
### Zadanie
Wyciągnij dane z faktury.

### Faktura
FV/2025/01/0001 z dnia 2025-01-10. Netto 1000,00 zł, VAT 23%, brutto 1230,00 zł.

### Odpowiedź
{"numer": "FV/2025/01/0001", "data": "2025-01-10", "netto": 1000.0, "vat_stawka": 23, "brutto": 1230.0}

### Zadanie
Wyciągnij dane z faktury.

### Faktura
Faktura nr 7/2025, data 2025-03-02, książki, netto 200 zł, VAT 5%, brutto 210 zł.

### Odpowiedź
{"numer": "7/2025", "data": "2025-03-02", "netto": 200.0, "vat_stawka": 5, "brutto": 210.0}

### Zadanie
Wyciągnij dane z faktury.

### Faktura
Rachunek A/12/2025 wystawiony 2025-06-30. Usługa zwolniona z VAT. Kwota 500,00 zł.

### Odpowiedź
{"numer": "A/12/2025", "data": "2025-06-30", "netto": 500.0, "vat_stawka": 0, "brutto": 500.0}
EOF

# Duplicate it - LoRA needs repetitions
for i in $(seq 1 40); do cat $KURS/lora/dane.txt; echo; done > $KURS/lora/pelny.txt
wc -l $KURS/lora/pelny.txt
```

### 6.3 Train

```bash
export HIP_VISIBLE_DEVICES=0,1
pkill -f llama-server; sleep 2

$LB/llama-finetune \
  -m $OSS20 \
  -f $KURS/lora/pelny.txt \
  -ngl 999 -c 2048 \
  --epochs 3 \
  -lr 1e-5 \
  -opt adamw \
  -wd 0.01 \
  2>&1 | tail -30

ls -la $KURS/lora/ *.gguf 2>/dev/null
```

⚠️ **`llama-finetune` in llama.cpp is still immature** compared with `peft`/`torch`.
Treat it as an **exercise in understanding the mechanism**, not as a production path.
We will come back to serious fine-tuning in part 9 (`torchtune`, `unsloth`, `axolotl`).

### 6.4 Apply the adapter

```bash
# With the adapter loaded at startup
$LB/llama-server -m $OSS20 \
  --lora $KURS/lora/adapter.gguf \
  -ngl 999 -c 16384 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

# Or merge the adapter into the model permanently
$LB/llama-export-lora \
  -m $OSS20 \
  --lora $KURS/lora/adapter.gguf \
  -o ~/models/wlasne/oss20-faktury.gguf
```

⭐ **Measure with the suite from part 3 before and after.** If LoRA does not improve the metrics — **drop it**.
Extra complexity without a gain is a loss.

---

## 7. Parallelism and batches

### 7.1 Server slots

```bash
$LB/llama-server -m $OSS20 -ngl 999 -c 32768 -np 4 ... &
```

`-np 4` = four parallel sessions. **But the context is shared:** `32768 / 4 = 8192` per slot.

| Configuration | When |
| :-- | :-- |
| **`-np 1`, large `-c`** | ⭐ **one agent** — maximum context and cache |
| `-np 4`, smaller `-c` | several users or subagents in parallel |

⚠️ **Trap P50 (new): `-np` divides the context, it does not multiply performance.**
For a single agent `-np 1` is **always better**: the whole context and the whole cache for it.

### 7.2 MoE on CPU — a trick for `qwen3-next-80b`

Your `qwen3-next-80b` is a MoE model (49.7 GB). The new flags let you **leave the expert
weights on the CPU** and keep only the dense layers on the GPU:

```bash
# All MoE weights on the CPU
$LB/llama-server -m $QWEN80 -ngl 999 -cmoe -c 16384 \
  --host 127.0.0.1 --port 8081 --no-warmup &

# Or only the first N layers
$LB/llama-server -m $QWEN80 -ngl 999 -ncmoe 20 -c 16384 \
  --host 127.0.0.1 --port 8081 --no-warmup &
```

💡 **What it is for:** MoE reads only some of the experts per token. By keeping them on the CPU,
you free VRAM for context — **at the cost of throughput**. Measure whether it pays off on your machine:

```bash
for FLAGI in "" "-cmoe" "-ncmoe 20"; do
  echo "=== flags: ${FLAGI:-none}"
  $LB/llama-bench -m $QWEN80 -ngl 999 $FLAGI -p 512 -n 128 -r 2 -o md 2>/dev/null | tail -4
  sleep 5
done
```

---

## 8. Plan for four cards

Cards 3 and 4 will give you **127.4 GiB of VRAM**. Plan for it now.

### 8.1 ⚠️ Four cards will NOT speed up a single query

⭐ **This is the most important sentence in this section.** Measured on your machine: the second card did not
speed up `gpt-oss-20b` (149.7 → 145.3 tok/s). The reason, from part 2 §5: decoding is
limited by **memory bandwidth and sequentiality**, not by compute.

**Four cards give CAPACITY:**

| Model | Weights | Fill of 4 cards |
| :-- | --: | --: |
| `gpt-oss-120b` MXFP4 | 59.0 GiB | 46% ✅ — **the one that does not work today** |
| Qwen3.5-122B-A10B Q4 | ~65 GiB | 51% ✅ |
| Qwen3-235B-A22B UD-Q3 | ~97 GiB | 76% ⚠️ |
| GLM-4.5-Air Q8 | ~102 GiB | 80% ⚠️ too tight |

⚠️ **A rule from the `gpt-oss-120b` failure: do not plan for VRAM fill above ~80% from the weights
alone.** With 7% headroom the model loads, but **does not compute on the GPU** — the compute buffer
ends up in host memory.

### 8.2 ⛔ P2P must stay disabled

**Trap P4** (a hardware pitfall of the reference rig): on a 4 × R9700 configuration, P2P transfers **hang the whole
host** (ROCm #11348), under both llama.cpp and vLLM.

```bash
# MANDATORY with four cards
export NCCL_P2P_DISABLE=1
export NCCL_PROTO=Simple
# GGML_CUDA_P2P: DO NOT SET

grep NCCL $LLMEDU/rig-env.sh    # both lines are already in rig-env.sh (multi-GPU ROCm only)
```

### 8.3 Two architectures to choose from

**Option A: one large model on four cards**

```bash
export HIP_VISIBLE_DEVICES=0,1,2,3   # AFTER remapping via amd-smi list!
$LB/llama-server -m ~/models/gpt-oss-120b/gpt-oss-120b-MXFP4.gguf \
  -ngl 999 --split-mode layer -ts 1,1,1,1 \
  -c 32768 --cache-reuse 256 \
  --host 127.0.0.1 --port 8081 --no-warmup &
```

🔧 **`-ts 1,1,1,1`** are **proportions**, not gigabytes. `--split-mode row` is deprecated —
use `layer`.

**Option B: ⭐ two models on two cards each — my recommendation for an agent**

```bash
# Small + draft on cards 0,1
HIP_VISIBLE_DEVICES=0,1 $LB/llama-server -m $OSS20 -md $DRAFT \
  -ngl 999 -ngld 999 -c 32768 --spec-draft-n-max 5 --cache-reuse 256 \
  --port 8081 --host 127.0.0.1 --no-warmup &

# Large on cards 2,3
HIP_VISIBLE_DEVICES=2,3 $LB/llama-server -m $QWEN32 \
  -ngl 999 -c 32768 --cache-reuse 256 \
  --port 8082 --host 127.0.0.1 --no-warmup &
```

⭐ **Option B is better for an agent.** The router (§4) gets **two hot servers** —
no cold jumps, both caches kept. Option A only makes sense when you
really need a model that does not fit on two cards.

### 8.4 After adding the cards — a mandatory checklist

```bash
# 1. Are all four cards visible?
lspci -d ::0300 | grep -c R9700          # expect 4 (+ the iGPU separately)

# 2. P13: REMAP THE INDICES - the numbering has changed!
amd-smi list

# 3. P15: link width on the PARENT port, not on the card
for BDF in $(lspci -d ::0300 | cut -d' ' -f1); do
  echo "=== $BDF"; sudo lspci -s $BDF -vv 2>/dev/null | grep -E 'LnkSta:' 
done

# 4. Power limit on ALL four
rocm-smi --showpower

# 5. AER = zero
sudo dmesg | grep -ci aer || echo "0 AER errors ✅"

# 6. Baseline measurement from scratch
$KURS/bench-wszystko.sh
```

---

## 9. Decision table

⭐ **The order in which to apply the levers** — from the best gain-to-effort ratio:

| # | Lever | Gain | Effort | Risk |
| --: | :-- | :-- | :-- | :-- |
| **1** | **`--cache-reuse` + frozen prompt** | ⭐⭐⭐⭐⭐ | low | none |
| **2** | **speculative decoding** (you have a draft!) | ⭐⭐⭐⭐ | low | no quality risk |
| **3** | 210 W power limit (you already have it) | — | — | — |
| 4 | `--cache-type-k/v q8_0` | ⭐⭐⭐ | low | minimal loss |
| 5 | model routing | ⭐⭐⭐ | medium | P48: cold cache |
| 6 | fewer turns (better harness/prompt) | ⭐⭐⭐⭐ | medium | none |
| 7 | your own quantization | ⭐⭐ | high | P49: wrong measurement |
| 8 | LoRA | ⭐⭐ | high | may not help |
| 9 | 4 cards | capacity | high | P4, P13 |
| 10 | a different engine (vLLM) | ⭐⭐⭐ | **high** | part 9 |

### 9.1 Measure everything together

```bash
# Target configuration
pkill -f llama-server; sleep 2
source $LLMEDU/rig-env.sh
export HIP_VISIBLE_DEVICES=0,1

$LB/llama-server -m $OSS20 \
  -md $DRAFT -ngl 999 -ngld 999 \
  -c 32768 -np 1 \
  --spec-draft-n-max 5 --spec-draft-p-min 0.75 \
  --cache-reuse 256 \
  --cache-type-k q8_0 --cache-type-v q8_0 \
  --slot-save-path $AGENT/kv-cache \
  --host 127.0.0.1 --port 8081 --no-warmup &
sleep 30

cd $AGENT && python3 pomiar-agenta.py | tee $AGENT/pomiar-koncowy.txt

echo "=== BEFORE vs AFTER ==="
grep -E 'median|time in model' $AGENT/pomiar-bazowy.txt
echo "---"
grep -E 'median|time in model' $AGENT/pomiar-koncowy.txt
```

---

## Exercises

1. **Find the optimal `--spec-draft-n-max`.** Test 3, 5, 8, 12 on your real
   prompts. Record tok/s and acceptance. **There is an optimum — find it.**
2. **Measure the cost of KV quantization.** `f16` vs `q8_0` vs `q4_0`: measure VRAM, tok/s
   **and accuracy with the suite from part 3**. Where does quality start to drop?
3. **Build a routing decision table for your tasks.** Run 20 real tasks on the
   small and the large model. Which ones needed the large one? **Fix the rule in `router.py`.**
4. **Your own `Q4_K_M` from Polish calibration.** Download the `F16` of Bielik (11B — ~22 GB),
   compute the `imatrix` on Polish accounting text, quantize and compare
   with the public `Q4_K_M`. **Measure PPL and the evaluation suite.**
5. **Endurance test.** Run the agent on 50 tasks in a row. Watch VRAM
   (netdata), whether the cache is bloating and whether there is a leak. **This is the pre-production test.**

---

## Check yourself

- [ ] Which phase — prefill or decoding — is the bottleneck, and why?
- [ ] Why is the prompt cache the biggest lever specifically for an agent?
- [ ] What invalidates the prompt cache — five things?
- [ ] Why does speculative decoding not degrade quality?
- [ ] What draft acceptance rate is good, and what to do when it is low?
- [ ] Why must the draft model have the same tokenizer?
- [ ] Why should the router be "lazy"?
- [ ] Why must PPL be measured on a different text than the calibration one?
- [ ] When will LoRA not help, and what should you use instead?
- [ ] Why is `-np 1` better for a single agent?
- [ ] What will four cards give, and what will they not give?

## New traps

| ID | Trap | § |
| :-- | :-- | :-- |
| **P46** | A changing system prompt kills the prompt cache | §2.4 |
| **P47** | The draft model eats VRAM and with low acceptance slows things down | §3.5 |
| **P48** | Routing between servers invalidates the cache — be lazy | §4.1 |
| **P49** | PPL measured on the calibration text is artificially good | §5.5 |
| **P50** | `-np` divides the context, it does not multiply performance | §7.1 |

---

**Next part: `09-TOOL-LANDSCAPE.md`** — a catalogue of open-source tools: alternative
engines (vLLM, SGLang, ExLlama), interfaces, vector databases, agent frameworks. What is
what, what works on RDNA4 and what not to take.
