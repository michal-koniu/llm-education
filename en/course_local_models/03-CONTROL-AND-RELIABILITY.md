# Part 3 — Control: how to force a local model to obey

**Level: ⭐⭐⭐** · Requires: part 2 · Time: ~5 h

> **Why this chapter.** A local 20B model is dumber than Claude and **will** break JSON,
> drop brackets and prepend "Here is your answer:" before the data. This is not a problem to be
> solved with a better prompt. It is a problem to be solved **at the sampling level**.
>
> After this chapter your model **cannot** return invalid JSON — not "usually
> doesn't", but is **physically unable to**. This is the foundation on which the whole agent loop
> stands in part 6.

```bash
cd ~/llm-education   # the repository directory (yours may differ)
source rig-env.sh
```

---

## Table of contents

| § | Topic | Key idea |
| :-- | :-- | :-- |
| [1](#1-chat-template--what-the-model-really-sees) | **Chat template** | "messages" are an illusion; the model sees one string |
| [2](#2-gbnf-grammars--the-most-important-tool-in-this-course) | **GBNF grammars** | ⭐ you constrain the sampling, you don't ask the model |
| [3](#3-json-schema--a-grammar-without-writing-a-grammar) | **JSON Schema** | 90% of cases without learning GBNF |
| [4](#4-calling-tools-reliably) | **Tools** | enforced by grammar = zero broken calls |
| [5](#5-determinism-in-practice) | **Determinism** | settings for machine paths |
| [6](#6-evaluation-harness--stop-judging-by-gut-feeling) | **Evaluation** | ⭐ without it you don't know whether a change helped |
| [7](#7-exercise--an-invoice-extractor-that-cannot-break) | **Exercise** | extractor + test set + measurement |

---

## 1. Chat template — what the model really sees

In part 1 you sent `messages: [{role, content}]`. That is a **convenient fiction**. The model
receives **one flat string**, and the server builds it from your messages according to the
**chat template stored in the GGUF file**.

### 1.1 Pull the template out of the model

⚠️ **`llama-cli -n 0 | grep 'chat template'` will find nothing in this build** — for exactly
the same reason as in part 2, §1.4: this build no longer prints the metadata dump
at startup. Look for the template through the server (§1.2 below, the `/apply-template` endpoint) —
it is the only method that actually works on this machine.

### 1.2 See the assembled prompt

The simplest way — ask the server to show what it sends:

Use the `/apply-template` endpoint — it is in this build and shows directly what the model
really receives, without digging through logs:

```bash
pkill -f llama-server; sleep 2
$LB/llama-server -m $BIELIK -ngl 999 -c 4096 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

curl -s http://127.0.0.1:8081/apply-template -H "Content-Type: application/json" \
  -d '{"messages":[
        {"role":"system","content":"Jesteś księgowym."},
        {"role":"user","content":"Co to jest KPiR?"}]}' \
| python3 -c 'import json,sys; d=json.load(sys.stdin); print(repr(d.get("prompt", d)))'
```

You will see (checked live — Bielik v3 uses **ChatML**, not the Mistral `[INST]` format,
as you might expect from its lineage):

```
'<s><|im_start|>system\nJesteś księgowym.<|im_end|>\n<|im_start|>user\nCo to jest KPiR?<|im_end|>\n<|im_start|>assistant\n'
```

💡 **This discrepancy is instructive in itself.** The base model (Mistral) and the
fine-tuned model (Bielik) can use **completely different conversation templates** — inheriting
an architecture does not mean inheriting the chat format. Don't guess the format based on
"what the model is based on" — check `/apply-template` every time you
change the model.

or with special tokens like `<|im_start|>system`. **Every model has a different template.**

### 1.3 Why it matters — three real failures

| Failure | Cause |
| :-- | :-- |
| the model answers nonsensically, as if it did not understand the role | wrong template (e.g. a forced `--chat-template` that does not match the model) |
| the model appends `<\|im_end\|>` to the visible answer | special tokens are not handled correctly as a stop |
| the model ignores `system` | some models **have no `system` role** in the template — the server pastes it into `user` |

⚠️ **Pitfall P25 (new): not every model has a `system` role.**
If your system instructions are ignored — check the template. In such a model the instruction
has to be pasted at the start of the first `user` message.

### 1.4 Raw vs chat endpoint — which one when

| Endpoint | What it does with the template | When to use |
| :-- | :-- | :-- |
| `/v1/chat/completions` | **applies** the model's template | normal conversation, agent |
| `/v1/completions` | **does not apply** — sends your text literally | when you want full control, as in part 2 |

💡 **In part 6 (the agent loop) we will use `/v1/chat/completions`**, because the template correctly
separates the roles and that improves quality. But you will **know** that underneath there is a single string.

---

## 2. GBNF grammars — the most important tool in this course

### 2.1 The idea — and why it is brilliant

Recall part 2 §3: at every token the model gives a distribution over the whole vocabulary,
and you pick one token.

**A grammar is a filter applied to that distribution.** Before a token is chosen the engine asks:
*"which of these 128,000 tokens are grammatically allowed at this point?"* — and **zeroes
the probability of all the others.**

```
      distribution (128,000 tokens)
              │
              ▼
      ┌───────────────────────┐
      │   GRAMMAR FILTER      │   ← 127,990 tokens drop out here
      │ "after { must come \" " │
      └───────────────────────┘
              │
              ▼
      you choose from 10 allowed
```

💡 **This is a hard guarantee, not a request.** The model **cannot** generate `{"kwota": abc}`
if the grammar says that after `"kwota":` there must be a digit. Not "probably won't generate" —
**there is no such possibility in the choice space.**

⭐ **This is the only reason a local 20B model can be the foundation of a product.**
Without grammars you would have to parse, retry and pray. With a grammar you have a contract.

### 2.2 The first grammar — yes/no

```bash
mkdir -p $KURS/gramatyki

cat > $KURS/gramatyki/takNie.gbnf <<'EOF'
root ::= "tak" | "nie"
EOF

curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
  -d "$(python3 -c '
import json
g = open("'"$HOME"'/kurs/gramatyki/takNie.gbnf").read()
print(json.dumps({
  "prompt": "Czy faktura VAT musi zawierać NIP nabywcy? Odpowiedz jednym słowem.\nOdpowiedź:",
  "max_tokens": 5, "temperature": 0, "grammar": g
}))')" | python3 -c 'import json,sys; print(repr(json.load(sys.stdin)["choices"][0]["text"]))'
```

The result is **exactly** `tak` or `nie` (Polish "yes" / "no"). Nothing more. No "Tak, oczywiście — faktura…".

### 2.3 GBNF syntax — everything you need

```gbnf
# Comment

root      ::= rule                   # "root" is the entry point (mandatory)

literal   ::= "exact text"            # a literal string
alternat  ::= "a" | "b" | "c"         # alternation (or)
sequence  ::= "a" "b" "c"             # in order
group     ::= ("a" | "b") "c"         # parentheses group

optional  ::= "a"?                    # 0 or 1
many      ::= "a"*                    # 0 or more
atleast1  ::= "a"+                    # 1 or more

range     ::= [0-9]                   # character class
negrange  ::= [^"\\]                  # negated class
```

⚠️ **Checked live: a rule has to fit on one physical line.** This
parser (in this build) rejects a definition split across multiple lines — even with neat
indentation, even with a `\` at the end as a continuation. The server then answers
`400 "failed to parse grammar"`, without saying which line. For readability you can
break **comments** and whole **separate rules** across lines — but the right-hand side of a
single `name ::= ...` has to be one string.

### 2.4 A grammar for a number — and why it matters so much

```bash
cat > $KURS/gramatyki/kwota.gbnf <<'EOF'
# An amount in zlotys: digits, optionally two places after the dot
root   ::= liczba
liczba ::= [0-9]+ ("." [0-9] [0-9])?
EOF

for PYT in "Ile wynosi 1200 zł netto plus 23% VAT? Podaj tylko kwotę brutto." \
           "Jaka jest stawka VAT na książki w Polsce? Podaj tylko liczbę procent."; do
  echo "--- $PYT"
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d "$(python3 -c '
import json,sys
g=open("'"$HOME"'/kurs/gramatyki/kwota.gbnf").read()
print(json.dumps({"prompt": sys.argv[1] + "\nOdpowiedź:", "max_tokens": 15,
                  "temperature": 0, "grammar": g}))' "$PYT")" \
  | python3 -c 'import json,sys; print("    ->", repr(json.load(sys.stdin)["choices"][0]["text"]))'
done
```

⚠️ **A grammar guarantees FORMAT, not TRUTH.** You will get a number. Whether it is the right one is a different
matter (and that is what §6, evaluation, is for). **Don't confuse these two things** — it is the most common
misunderstanding around structured output.

### 2.5 A JSON grammar — a full example for an invoice

```bash
cat > $KURS/gramatyki/faktura.gbnf <<'EOF'
# Invoice data extraction. The order of fields is ENFORCED - that is good,
# because the model cannot skip a field or change the order.

root ::= "{" ws "\"numer\":" ws string ws "," ws "\"data\":" ws data ws "," ws "\"nip\":" ws nip ws "," ws "\"netto\":" ws kwota ws "," ws "\"vat_stawka\":" ws stawka ws "," ws "\"brutto\":" ws kwota ws "}"
# ⚠️ The whole right-hand side MUST be on one physical line - checked live.
# This GBNF parser (unlike some other versions of llama.cpp)
# does NOT accept a rule split across multiple lines, even with a "\" continuation.
# The error is mute for a human: the server answers 400 "failed to parse grammar"
# without saying which line is at fault. If your grammar suddenly stops
# working after a "cosmetic" break of a long line - this is exactly the clue.

string ::= "\"" znak* "\""
znak   ::= [^"\\] | "\\" ["\\/bfnrt]

# ISO: YYYY-MM-DD
data   ::= "\"" [0-9][0-9][0-9][0-9] "-" [0-9][0-9] "-" [0-9][0-9] "\""

# NIP (Polish tax ID): 10 digits
nip    ::= "\"" [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9] "\""

kwota  ::= [0-9]+ ("." [0-9][0-9])?

# Only real Polish rates
stawka ::= "0" | "5" | "8" | "23"

ws     ::= [ \t\n]*
EOF
```

Test it:

```bash
python3 - <<'PYEOF'
import json, urllib.request, os

g = open(os.path.join(os.environ["KURS"], "gramatyki/faktura.gbnf")).read()

TEKST = """
FAKTURA VAT nr FV/2025/09/0143
Data wystawienia: 15 września 2025
Sprzedawca: Biuro Rachunkowe ALFA, NIP 1234567890
Usługa: prowadzenie księgowości za sierpień 2025
Wartość netto: 1 200,00 zł
VAT 23%: 276,00 zł
Do zapłaty: 1 476,00 zł
"""

prompt = f"Wyciągnij dane z faktury jako JSON.\n\n{TEKST}\n\nJSON:"
req = urllib.request.Request("http://127.0.0.1:8081/v1/completions",
    data=json.dumps({"prompt": prompt, "max_tokens": 300,
                     "temperature": 0, "grammar": g}).encode(),
    headers={"Content-Type": "application/json"})
out = json.load(urllib.request.urlopen(req, timeout=300))["choices"][0]["text"]

print("RAW:", out)
print()
d = json.loads(out)          # this CANNOT blow up - the grammar guarantees it
print("PARSED:")
for k, v in d.items():
    print(f"  {k:12s} = {v!r}")

# Arithmetic check - the grammar does NOT check this
netto  = float(d["netto"]); brutto = float(d["brutto"]); st = int(d["vat_stawka"])
oczek  = round(netto * (1 + st/100), 2)
print(f"\nnetto*{1+st/100} = {oczek}  vs gross from the model = {brutto}  "
      f"{'✅ consistent' if abs(oczek-brutto) < 0.02 else '❌ MISMATCH'}")
PYEOF
```

💡 **Note the last three lines.** The grammar gave you valid JSON with sensible
types. **You have to check arithmetic correctness yourself, in code.** This is the division of labour
we will repeat throughout the course:

```
grammar     → guarantees STRUCTURE
code        → checks CONSISTENCY (arithmetic, ranges, dictionaries)
evaluation  → measures ACCURACY (§6)
```

### 2.6 Grammar pitfalls

⚠️ **P26 (new): a grammar can loop the model forever.**
If a grammar allows `"a"*` without an exit condition, and the model "wants" to keep writing —
it will run up to `max_tokens`. **Always set `max_tokens`** and always test a grammar on
input that does not fit it.

⚠️ **P27 (new): a grammar slows generation down.**
Filtering 128,000 tokens at every step costs something. Expect a **10–30% drop in
tok/s**. It is the best-spent 20% in the whole system — but know about it when measuring performance.

```bash
# Measure the cost of a grammar
for MODE in without with; do
  if [ "$MODE" = "with" ]; then
    G=$(python3 -c 'import json,os;print(json.dumps(open(os.path.join(os.environ["KURS"], "gramatyki/kwota.gbnf")).read()))')
    EXTRA=",\"grammar\":$G"
  else
    EXTRA=""
  fi
  echo -n "$MODE grammar: "
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d "{\"prompt\":\"Podaj liczbe: \",\"max_tokens\":60,\"temperature\":0$EXTRA}" \
  | python3 -c 'import json,sys; t=json.load(sys.stdin)["timings"]; print(f"{t.get(\"predicted_per_second\",0):.1f} tok/s")'
done
```

---

## 3. JSON Schema — a grammar without writing a grammar

Writing GBNF by hand is instructive, but impractical day to day. `llama-server`
**converts JSON Schema into a grammar by itself.**

```bash
python3 - <<'PYEOF'
import json, urllib.request

SCHEMA = {
  "type": "object",
  "properties": {
    "numer":      {"type": "string"},
    "data":       {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"},
    "netto":      {"type": "number"},
    "vat_stawka": {"type": "integer", "enum": [0, 5, 8, 23]},
    "brutto":     {"type": "number"},
    "pewnosc":    {"type": "string", "enum": ["wysoka", "srednia", "niska"]},
  },
  "required": ["numer", "data", "netto", "vat_stawka", "brutto", "pewnosc"],
}

TEKST = "Faktura FV/9/2025 z 2025-09-15, netto 1200 zl, VAT 23%, brutto 1476 zl"

req = urllib.request.Request("http://127.0.0.1:8081/v1/chat/completions",
    data=json.dumps({
        "messages": [
            {"role": "system", "content": "Wyciągasz dane z faktur. Jeśli czegoś nie ma w tekście — ustaw pewnosc na niska."},
            {"role": "user", "content": TEKST},
        ],
        "max_tokens": 300,
        "temperature": 0,
        "response_format": {"type": "json_schema", "json_schema": {"schema": SCHEMA}},
    }).encode(),
    headers={"Content-Type": "application/json"})

txt = json.load(urllib.request.urlopen(req, timeout=300))["choices"][0]["message"]["content"]
print(json.dumps(json.loads(txt), indent=2, ensure_ascii=False))
PYEOF
```

💡 **The `pewnosc` ("confidence") field is a pattern worth remembering.** You force the model to
**declare its own uncertainty as a data field**. Then in code: `if pewnosc == "niska":
do_weryfikacji_przez_czlowieka`. It is cheap and effective — and it ties in with reading logits
from part 2 §2.2.

### 3.1 What JSON Schema in llama.cpp does NOT support

| Unsupported | Workaround |
| :-- | :-- |
| recursive schemas | flatten the structure |
| `minimum` / `maximum` | check in code after parsing |
| `minLength` / `maxLength` | as above |
| complex `oneOf` with a discriminator | split into two calls |

⚠️ **Don't assume that a constraint from the schema worked.** If you are not sure —
**check in code**. The schema is a convenience, the code is a guarantee.

---

## 4. Calling tools reliably

Part 1 §8 showed naive tool calling. Now we will do it **so that it cannot
break** — and this is the direct foundation of part 6.

```bash
cat > $KURS/narzedzia-schema.py <<'PYEOF'
#!/usr/bin/env python3
"""Tool calling enforced by a schema - zero broken calls.

The model CANNOT return an invalid tool name or a wrongly typed argument.
"""
import json, urllib.request

SERVER = "http://127.0.0.1:8081"

# --- Tool definitions: name -> (description, argument_schema, function) -------
def _czytaj_plik(sciezka: str) -> str:
    import os
    p = os.path.realpath(os.path.expanduser(os.path.expandvars(sciezka)))
    root = os.path.realpath(os.environ["KURS"])
    if not p.startswith(root + os.sep) and p != root:
        return f"ODMOWA: sciezka poza {root}"
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read()[:2000]
    except OSError as e:
        return f"BLAD: {e}"

def _policz(wyrazenie: str) -> str:
    # Arithmetic only - no eval() on raw model input
    import re
    if not re.fullmatch(r"[0-9\.\+\-\*/\(\) ]+", wyrazenie):
        return "ODMOWA: dozwolone tylko cyfry i + - * / ( )"
    try:
        return str(eval(wyrazenie, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"BLAD: {e}"

NARZEDZIA = {
    "czytaj_plik": {
        "opis": "Czyta plik tekstowy z katalogu $KURS. Zwraca do 2000 znakow.",
        "args": {"sciezka": {"type": "string"}},
        "fn": _czytaj_plik,
    },
    "policz": {
        "opis": "Liczy wyrazenie arytmetyczne. Tylko cyfry i operatory + - * / ( ).",
        "args": {"wyrazenie": {"type": "string"}},
        "fn": _policz,
    },
    "odpowiedz": {
        "opis": "Konczy prace i podaje ostateczna odpowiedz uzytkownikowi.",
        "args": {"tresc": {"type": "string"}},
        "fn": None,   # handled in the loop
    },
}

def schemat_wywolania() -> dict:
    """Builds a JSON Schema that enforces a valid tool call.

    The key: an "enum" on the tool name. The model CANNOT invent a name.
    """
    return {
        "type": "object",
        "properties": {
            "mysl":      {"type": "string"},
            "narzedzie": {"type": "string", "enum": list(NARZEDZIA)},
            "argumenty": {"type": "object"},
        },
        "required": ["mysl", "narzedzie", "argumenty"],
    }

def opis_narzedzi() -> str:
    linie = []
    for nazwa, meta in NARZEDZIA.items():
        args = ", ".join(f"{k}: {v['type']}" for k, v in meta["args"].items())
        linie.append(f"- {nazwa}({args}) — {meta['opis']}")
    return "\n".join(linie)

def zapytaj(messages, schema):
    req = urllib.request.Request(SERVER + "/v1/chat/completions",
        data=json.dumps({
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0,            # <-- determinism for the machine path
            "repeat_penalty": 1.0,       # <-- P21: the penalty breaks JSON
            "response_format": {"type": "json_schema", "json_schema": {"schema": schema}},
        }).encode(), headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    return r["choices"][0]["message"]["content"]

if __name__ == "__main__":
    import sys
    zadanie = sys.argv[1] if len(sys.argv) > 1 else \
        "Policz, ile wynosi 1200 zlotych netto po dodaniu 23 procent VAT."

    SYSTEM = (
        "Jesteś agentem. W każdej turze wybierasz DOKŁADNIE JEDNO narzędzie.\n"
        "Dostępne narzędzia:\n" + opis_narzedzi() + "\n\n"
        "Pole 'mysl' to jedno zdanie uzasadnienia. Gdy masz odpowiedź — użyj 'odpowiedz'."
    )
    msgs = [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": zadanie}]

    for tura in range(1, 7):
        raw = zapytaj(msgs, schemat_wywolania())
        krok = json.loads(raw)          # guaranteed by the schema
        nazwa = krok["narzedzie"]
        args  = krok["argumenty"]
        print(f"\n[turn {tura}] thought: {krok['mysl']}")
        print(f"          -> {nazwa}({args})")

        if nazwa == "odpowiedz":
            print(f"\n=== ANSWER ===\n{args.get('tresc','(none)')}")
            break

        meta = NARZEDZIA[nazwa]          # safe: the enum guarantees existence
        brakuje = [k for k in meta["args"] if k not in args]
        wynik = (f"BLAD: brakuje argumentow {brakuje}" if brakuje
                 else meta["fn"](**{k: args[k] for k in meta["args"]}))
        print(f"          <- {str(wynik)[:200]}")

        msgs.append({"role": "assistant", "content": raw})
        msgs.append({"role": "user", "content": f"Wynik narzędzia {nazwa}: {wynik}"})
    else:
        print("\n[aborted: turn limit]")
PYEOF
chmod +x $KURS/narzedzia-schema.py

cd $KURS && python3 narzedzia-schema.py
```

### 4.1 What exactly we have secured

| Threat | Defence |
| :-- | :-- |
| the model invents a non-existent tool | `"enum": list(NARZEDZIA)` — **impossible** |
| the model returns broken JSON | `response_format` — **impossible** |
| the model drops a required key | `"required"` + the `brakuje` check in code |
| `repeat_penalty` breaks brackets | set to `1.0` (**P21**) |
| the model reads `/etc/passwd` | the `realpath` check inside `czytaj_plik` |
| the model runs `eval("os.system(...)")` | a character allowlist in `policz` |
| an infinite loop | a hard limit `range(1, 7)` |

⚠️ **This is NOT yet safe.** The checks live in the tool functions — that is,
in the same process as the loop. In **part 7** we will put the tools inside `bwrap`, and only then
will it be defensible. For now it is *correct*, not *safe*.

---

## 5. Determinism in practice

Two settings profiles. Learn them by heart.

### 5.1 MACHINE profile — tools, extraction, classification

```json
{
  "temperature": 0,
  "top_k": 1,
  "repeat_penalty": 1.0,
  "seed": 42,
  "response_format": { "type": "json_schema", "json_schema": { "schema": "..." } }
}
```

### 5.2 CONVERSATIONAL profile — writing, explaining, summaries

```json
{
  "temperature": 0.7,
  "min_p": 0.05,
  "repeat_penalty": 1.1,
  "seed": -1
}
```

⚠️ **Pitfall P28 (new): a single profile for the whole agent is a mistake.**
In one turn the agent calls a tool (it needs the machine profile), and in the next it writes
a summary for a human (it needs the conversational one). **Switch the profile per call**,
not per server. In part 6 we will build this as two functions: `zapytaj_maszynowo()`
and `zapytaj_rozmownie()`.

---

## 6. Evaluation harness — stop judging by gut feeling

⭐ **This is the second most important part of this chapter, alongside grammars.**

Without an evaluation set every change you make (a different model, a different prompt, a different quantization)
is guesswork. With one — it is measurement.

### 6.1 Build a test set

```bash
mkdir -p $KURS/eval
cat > $KURS/eval/faktury.jsonl <<'EOF'
{"id":"f1","tekst":"FV/2025/01/0001 z dnia 2025-01-10. Netto 1000,00 zł, VAT 23%, brutto 1230,00 zł.","oczek":{"numer":"FV/2025/01/0001","data":"2025-01-10","netto":1000.0,"vat_stawka":23,"brutto":1230.0}}
{"id":"f2","tekst":"Faktura nr 7/2025, data 2025-03-02, książki, netto 200 zł, VAT 5%, brutto 210 zł.","oczek":{"numer":"7/2025","data":"2025-03-02","netto":200.0,"vat_stawka":5,"brutto":210.0}}
{"id":"f3","tekst":"Rachunek A/12/2025 wystawiony 2025-06-30. Usługa zwolniona z VAT. Kwota 500,00 zł.","oczek":{"numer":"A/12/2025","data":"2025-06-30","netto":500.0,"vat_stawka":0,"brutto":500.0}}
{"id":"f4","tekst":"FV 99/2025 z 2025-12-01, usługi budowlane, netto 10 000,00 zł, VAT 8%, brutto 10 800,00 zł.","oczek":{"numer":"99/2025","data":"2025-12-01","netto":10000.0,"vat_stawka":8,"brutto":10800.0}}
{"id":"f5","tekst":"Faktura FV/2025/44 z 2025-08-15. Netto 3 333,33 zł, VAT 23%, brutto 4 100,00 zł.","oczek":{"numer":"FV/2025/44","data":"2025-08-15","netto":3333.33,"vat_stawka":23,"brutto":4100.00}}
EOF
wc -l $KURS/eval/faktury.jsonl
```

💡 **Five cases are too few for production, but enough to start measuring.**
Grow the set **every time you see a new error** — it is the best-spent
time in the whole project. Add hard cases: a rate of 0, amounts with grosze (cents), spaces
in numbers, dates written out in words.

### 6.2 The harness

```bash
cat > $KURS/eval/uruchom.py <<'PYEOF'
#!/usr/bin/env python3
"""Evaluation harness: measures extraction accuracy field by field.

Usage:
  python3 uruchom.py                      # default server 8081
  python3 uruchom.py http://127.0.0.1:8082
"""
import json, os, sys, time, urllib.request

SERVER = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8081"
ZBIOR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "faktury.jsonl")

SCHEMA = {
    "type": "object",
    "properties": {
        "numer":      {"type": "string"},
        "data":       {"type": "string"},
        "netto":      {"type": "number"},
        "vat_stawka": {"type": "integer", "enum": [0, 5, 8, 23]},
        "brutto":     {"type": "number"},
    },
    "required": ["numer", "data", "netto", "vat_stawka", "brutto"],
}

SYSTEM = ("Wyciągasz dane z polskich faktur. Kwoty jako liczby bez spacji i bez waluty. "
          "Daty w formacie RRRR-MM-DD. Stawka VAT jako liczba całkowita. "
          "Usługa zwolniona z VAT = stawka 0.")

def wyciagnij(tekst: str) -> tuple[dict | None, float]:
    body = {
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user",   "content": tekst}],
        "max_tokens": 300, "temperature": 0, "repeat_penalty": 1.0, "seed": 42,
        "response_format": {"type": "json_schema", "json_schema": {"schema": SCHEMA}},
    }
    req = urllib.request.Request(SERVER + "/v1/chat/completions",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        r = json.load(urllib.request.urlopen(req, timeout=300))
        dt = time.time() - t0
        return json.loads(r["choices"][0]["message"]["content"]), dt
    except Exception as e:
        print(f"    ERROR: {e}")
        return None, time.time() - t0

def rowne(pole, a, b) -> bool:
    """Tolerant comparison: numbers to the grosz, text after whitespace normalization."""
    if a is None or b is None:
        return False
    if isinstance(b, float):
        try: return abs(float(a) - b) < 0.02
        except (TypeError, ValueError): return False
    if isinstance(b, int):
        try: return int(a) == b
        except (TypeError, ValueError): return False
    return str(a).strip().replace(" ", "") == str(b).strip().replace(" ", "")

def main():
    przypadki = [json.loads(l) for l in open(ZBIOR, encoding="utf-8") if l.strip()]
    pola = ["numer", "data", "netto", "vat_stawka", "brutto"]
    trafne = {p: 0 for p in pola}
    pelne, czasy, bledy = 0, [], []

    print(f"Server: {SERVER}")
    print(f"Cases: {len(przypadki)}\n")

    for p in przypadki:
        got, dt = wyciagnij(p["tekst"])
        czasy.append(dt)
        if got is None:
            bledy.append((p["id"], "no response")); print(f"  {p['id']}: ❌ none"); continue

        ok_pola = [pole for pole in pola if rowne(pole, got.get(pole), p["oczek"][pole])]
        for pole in ok_pola:
            trafne[pole] += 1
        if len(ok_pola) == len(pola):
            pelne += 1
            print(f"  {p['id']}: ✅ all fields  ({dt:.1f}s)")
        else:
            zle = [pole for pole in pola if pole not in ok_pola]
            print(f"  {p['id']}: ⚠️  wrong fields {zle}  ({dt:.1f}s)")
            for pole in zle:
                print(f"        {pole}: expected={p['oczek'][pole]!r}  got={got.get(pole)!r}")
                bledy.append((p["id"], pole))

    n = len(przypadki)
    print(f"\n{'='*58}\nRESULT")
    print(f"  full match:      {pelne}/{n}  = {100*pelne/n:.0f}%")
    for pole in pola:
        print(f"  {pole:12s}   {trafne[pole]}/{n}  = {100*trafne[pole]/n:.0f}%")
    print(f"  average time:    {sum(czasy)/len(czasy):.1f}s")
    if bledy:
        print(f"\n  to fix: {bledy}")

if __name__ == "__main__":
    main()
PYEOF
chmod +x $KURS/eval/uruchom.py
```

### 6.3 Run it and compare models

```bash
# Bielik (Q8, Polish)
pkill -f llama-server; sleep 2
$LB/llama-server -m $BIELIK -ngl 999 -c 4096 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25
python3 $KURS/eval/uruchom.py http://127.0.0.1:8081

# Qwen3-32B (Q4, larger)
pkill -f llama-server; sleep 3
$LB/llama-server -m $QWEN32 -ngl 999 -c 4096 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 40
python3 $KURS/eval/uruchom.py http://127.0.0.1:8081

# gpt-oss-20b (fast)
pkill -f llama-server; sleep 3
$LB/llama-server -m $OSS20 -ngl 999 -c 4096 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25
python3 $KURS/eval/uruchom.py http://127.0.0.1:8081
```

⭐ **Now you have numbers.** "Qwen is better" stops being an opinion and becomes
`brutto: 5/5 vs 3/5`. **This is the moment you stop guessing and start
engineering.**

### 6.4 Save the results — a history of measurements

```bash
mkdir -p $KURS/eval/wyniki
MODEL_NAZWA=bielik   # ⚠️ change to the model you are testing RIGHT NOW (see 6.3) — without this
                     # every save overwrites the previous one under the same label and the measurements get mixed up
python3 $KURS/eval/uruchom.py 2>&1 | tee $KURS/eval/wyniki/$(date +%Y%m%d-%H%M)-$MODEL_NAZWA.txt
```

💡 **Do this after every change.** Model, prompt, quantization, grammar — every change gets
a dated file. In a month you will know exactly what helped. It is exactly the same
discipline you already have in `results/all-benchmark-results.md` for performance — only for
quality.

---

## 7. Exercise — an invoice extractor that cannot break

Put together everything from this chapter:

1. **Extend the set** `$KURS/eval/faktury.jsonl` to **15 cases**. Add:
   - an amount with a space as the thousands separator (`10 000,00`)
   - a date written out in words (`15 września 2025`)
   - an invoice with no number (what should the model do? decide and write it in `oczek`)
   - two VAT rates on one invoice (this will break your schema — **that is the point**)
2. **Run the harness** on three models. Save the results.
3. **Pick the best one** and fix the system prompt for its specific errors.
4. **Measure again.** Record by how much it improved.
5. **Add a `pewnosc` field to the schema** (§3) and check: does the model flag low confidence
   where it is actually wrong? If so — you have a ready mechanism for escalation to a human.

### 7.1 Success criterion

```
full match ≥ 80%        on 15 cases
field "brutto" = 100%   (this is the field you must not get wrong)
```

If you don't reach it — **do not move on to part 4**. Go back to the prompt and the schema.
An agent built on unreliable extraction will be unreliable at every level above.

---

## Check yourself

- [ ] What exactly does the model see when you send `messages: [{role, content}]`?
- [ ] How does a GBNF grammar affect the probability distribution from part 2?
- [ ] Why does a grammar guarantee format, but not truth?
- [ ] Why does `repeat_penalty=1.1` break JSON generation?
- [ ] How do you make it impossible for the model to invent a non-existent tool name?
- [ ] Why is a single sampling profile for the whole agent a mistake?
- [ ] Why, without an evaluation set, don't you know whether a prompt change helped?

## New pitfalls

| ID | Pitfall | § |
| :-- | :-- | :-- |
| **P25** | Not every model has a `system` role — instructions are silently ignored | §1.3 |
| **P26** | A grammar with no exit condition loops the generation up to `max_tokens` | §2.6 |
| **P27** | A grammar costs 10–30% tok/s — account for it in measurements | §2.6 |
| **P28** | A single sampling profile for the whole agent — switch per call | §5.2 |

---

**Next part: `04-MEMORY-RAG-AND-CONTEXT.md`** — you give the model access to documents
it did not see in training. A vector database written from scratch, in pure Python.
