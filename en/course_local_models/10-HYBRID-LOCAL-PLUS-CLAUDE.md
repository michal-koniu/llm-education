# Part 10 — Hybrid: local model + Claude API

**Level: ⭐⭐⭐** · Requires: parts 6, 8 · Time: ~3 h

> **A short chapter — deliberately.** The core of your system is the local stack. Claude is
> **one additional option in the router from part 8 §4**, not a new architecture.
>
> The key question is not "how do I call the API" (that is half a page of code), but **"what may
> be sent off the machine and who decides that"**. We start there.

---

## 1. ⭐ The privacy boundary — decide first

You sell **data sovereignty**. Client documents do not leave the machine. This is
your product thesis — and a hybrid can break it if you do it without thought.

### 1.1 Three classes of data

```
┌─────────────────────────────────────────────────────────────┐
│ CLASS A — NEVER leaves the machine                          │
│   contents of invoices, contracts, personal data, tax IDs,  │
│   amounts, client names, contents of client files           │
│                            ↓ ONLY the local model           │
├─────────────────────────────────────────────────────────────┤
│ CLASS B — may leave after ANONYMIZATION                     │
│   structure of a problem, database schema, an error message │
│   without data, a code fragment without secrets             │
│                            ↓ Claude, after passing through  │
│                              the filter from §3             │
├─────────────────────────────────────────────────────────────┤
│ CLASS C — may leave freely                                  │
│   general questions, public documentation, architecture     │
│   design, tax-law questions without data                    │
│                            ↓ Claude without restrictions    │
└─────────────────────────────────────────────────────────────┘
```

⚠️ **The default rule: EVERYTHING is class A until you explicitly classify it otherwise.**
The opposite default (we send unless someone forbids it) **will sooner or later send a client's
invoice**.

### 1.2 Write it into the contract and into the code

💡 **If you tell the client "the data does not leave your server", and the router sometimes calls
Claude — that must be in the contract.** This chapter is useless if that conversation does not
happen. **A technical filter does not replace consent.**

---

## 2. When Claude really adds something

| Task | Local 20B | Local 32B | Claude |
| :-- | :-- | :-- | :-- |
| tool choice (grammar) | ✅ | ✅ | overkill |
| extraction from an invoice | ✅ | ✅ | ⛔ **class A** |
| summary of an observation | ✅ | ✅ | overkill |
| **architecture design** | ⚠️ | ✅ | ⭐ **clearly better** |
| **diagnosis of a hard bug** | ❌ | ⚠️ | ⭐ **clearly better** |
| **multi-file refactor** | ❌ | ⚠️ | ⭐ **clearly better** |
| **writing a long text in Polish** | ⚠️ | ✅ | ⭐ better |
| **context > 100k tokens** | ❌ | ❌ | ⭐ **1M context** |

⭐ **The pattern I recommend: Claude as a consultant, not as an executor.**
The local agent does the work. When it gets stuck — it asks Claude for **advice**, describing the problem
**without client data**. The advice comes back, the local agent carries it out.

```
   local agent ──(problem, class B/C)──► Claude
        │                                    │
        │◄──────────(strategy)───────────────┘
        │
        └──► executes on class A data, locally
```

---

## 3. The output filter — code, not good intentions

```bash
cat > $AGENT/granica.py <<'PYEOF'
#!/usr/bin/env python3
"""Filter for data leaving the machine. Default: BLOCK."""
import re

# The patterns match Polish-language data (NIP, PESEL, REGON, zł, sp. z o.o.)
WZORCE_WRAZLIWE = [
    (r"\b\d{10}\b",                          "possible NIP"),
    (r"\b\d{11}\b",                          "possible PESEL/REGON"),
    (r"\b[A-Z]{2}\d{26}\b",                  "IBAN number"),
    (r"\b\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b", "account number"),
    (r"(?i)\bfaktura\s+(vat\s+)?nr\b",       "invoice number"),
    (r"(?i)\bFV[/-]\d",                      "invoice number"),
    (r"\b\d{1,3}(?:[  ]\d{3})*,\d{2}\s*(?:zł|PLN)\b", "amount in PLN"),
    (r"(?i)\b(sp\.\s*z\s*o\.?o\.?|s\.a\.|spółka)\b", "entity name"),
    (r"(?i)-----BEGIN [A-Z ]*PRIVATE KEY",   "private key"),
    (r"(?i)\b(api[_-]?key|token|hasło|password)\s*[:=]\s*\S+", "secret"),
    (r"\b[\w.+-]+@[\w-]+\.[\w.]+\b",         "e-mail address"),
]

class Granica:
    def __init__(self, tryb: str = "blokuj"):
        """tryb: 'blokuj' | 'anonimizuj' | 'pytaj'"""
        self.tryb = tryb
        self.zablokowane = 0
        self.wyslane = 0

    def sprawdz(self, tekst: str) -> list[tuple[str, str]]:
        """Returns [(match, description), ...]."""
        out = []
        for wz, opis in WZORCE_WRAZLIWE:
            for m in re.finditer(wz, tekst):
                out.append((m.group(0), opis))
        return out

    def przepusc(self, tekst: str, klasa: str = "A") -> tuple[bool, str, list]:
        """Returns (allowed, text_to_send, findings)."""
        if klasa == "A":
            self.zablokowane += 1
            return False, "", [("class A", "data does not leave the machine")]

        znal = self.sprawdz(tekst)
        if not znal:
            self.wyslane += 1
            return True, tekst, []

        if self.tryb == "blokuj":
            self.zablokowane += 1
            return False, "", znal

        if self.tryb == "anonimizuj":
            czysty = tekst
            for i, (dop, opis) in enumerate(znal):
                czysty = czysty.replace(dop, f"[{opis.upper().replace(' ','_')}_{i}]")
            self.wyslane += 1
            return True, czysty, znal

        # 'pytaj' (ask) mode
        print(f"\n  ⚠️  SENDING OFF THE MACHINE — detected {len(znal)} sensitive fragments:")
        for dop, opis in znal[:8]:
            print(f"      {opis}: {dop[:40]!r}")
        print(f"      text: {len(tekst)} characters")
        if input("      send? [y/N] ").strip().lower() in ("t", "tak", "y"):
            self.wyslane += 1
            return True, tekst, znal
        self.zablokowane += 1
        return False, "", znal

if __name__ == "__main__":
    g = Granica(tryb="anonimizuj")
    PROBKI = [
        ("C", "Jak działa dekodowanie spekulatywne w llama.cpp?"),
        ("B", "Faktura FV/2025/143 od ALFA sp. z o.o., NIP 1234567890, 1 476,50 zł."),
        ("B", "Błąd: KeyError 'brutto' w linii 42 pliku ekstraktor.py"),
        ("A", "Cokolwiek — klasa A nigdy nie wychodzi."),
    ]
    for klasa, t in PROBKI:
        ok, wyslac, znal = g.przepusc(t, klasa)
        print(f"\nclass {klasa}: {t[:60]}")
        print(f"  → {'SENDING' if ok else 'BLOCKING'}  ({len(znal)} findings)")
        if ok and wyslac != t:
            print(f"  → after anonymization: {wyslac[:80]}")
    print(f"\nsent={g.wyslane} blocked={g.zablokowane}")
PYEOF

python3 $AGENT/granica.py
```

⚠️ **Trap P51 (new): a regex filter will let through what you did not anticipate.**
There is no complete set of patterns for "sensitive data". **The filter is the second line of defence.
The first is classification at the input** (class A = does not leave, no exceptions).

---

## 4. Calling Claude — the minimum you must know

```bash
python3 -m venv $VENVS/claude
$VENVS/claude/bin/pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

```bash
cat > $AGENT/klient_claude.py <<'PYEOF'
#!/usr/bin/env python3
"""A thin Claude client with the boundary filter and a cost counter."""
import os, sys
import anthropic

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from granica import Granica

MODEL = "claude-opus-5"

# Prices per million tokens (USD), as of June 2026
CENNIK = {
    "claude-opus-5":   {"wej": 5.00, "wyj": 25.00},
    "claude-sonnet-5": {"wej": 3.00, "wyj": 15.00},
    "claude-haiku-4-5":{"wej": 1.00, "wyj":  5.00},
}

class Konsultant:
    def __init__(self, model: str = MODEL, tryb_granicy: str = "pytaj"):
        self.klient = anthropic.Anthropic()      # reads ANTHROPIC_API_KEY
        self.model = model
        self.granica = Granica(tryb=tryb_granicy)
        self.koszt_usd = 0.0
        self.wywolan = 0

    def zapytaj(self, pytanie: str, kontekst: str = "", klasa: str = "A",
                system: str = "") -> str:
        # ⚠️ The default is "A", NOT "C" - in line with the rule from 1.1 ("everything is
        # class A until you explicitly classify it otherwise"). An earlier
        # version of this file defaulted to "C" (the least safe option),
        # which contradicted the rule of section 1.1 - every call that forgot to
        # pass `klasa=` would get the broadest permissions instead of the narrowest.
        pelne = (kontekst + "\n\n" + pytanie).strip()
        ok, tekst, znal = self.granica.przepusc(pelne, klasa)
        if not ok:
            return (f"[BLOCKED BY THE BOUNDARY] Not sent. "
                    f"Reason: {', '.join(o for _, o in znal[:3]) or 'class A'}. "
                    f"Solve it locally.")

        kwargs = {
            "model": self.model,
            "max_tokens": 8000,
            "messages": [{"role": "user", "content": tekst}],
            # Adaptive thinking is the default on Opus 5; effort controls the depth
            "output_config": {"effort": "high"},
        }
        if system:
            # cache_control: the system prefix gets ~10x cheaper on repeats
            kwargs["system"] = [{"type": "text", "text": system,
                                 "cache_control": {"type": "ephemeral"}}]

        try:
            r = self.klient.messages.create(**kwargs)
        except anthropic.RateLimitError as e:
            return f"[LIMIT] {e}"
        except anthropic.APIConnectionError:
            return "[NO NETWORK] Claude unavailable — solve it locally."
        except anthropic.APIStatusError as e:
            return f"[API ERROR {e.status_code}] {e.message}"

        # Opus 5 may refuse - check BEFORE reading content
        if r.stop_reason == "refusal":
            kat = getattr(getattr(r, "stop_details", None), "category", None)
            return f"[MODEL REFUSAL] category={kat}. Solve it locally."

        self._policz(r)
        return next((b.text for b in r.content if b.type == "text"), "(no text)")

    def _policz(self, r):
        c = CENNIK.get(self.model, CENNIK["claude-opus-5"])
        u = r.usage
        wej_pelne = getattr(u, "input_tokens", 0)
        wej_cache = getattr(u, "cache_read_input_tokens", 0) or 0
        wej_zapis = getattr(u, "cache_creation_input_tokens", 0) or 0
        wyj       = getattr(u, "output_tokens", 0)
        koszt = (wej_pelne * c["wej"]
                 + wej_cache * c["wej"] * 0.1        # cache read ~10% of the price
                 + wej_zapis * c["wej"] * 1.25       # cache write ~125%
                 + wyj * c["wyj"]) / 1_000_000
        self.koszt_usd += koszt
        self.wywolan += 1
        print(f"      [claude] in={wej_pelne} cache_r={wej_cache} out={wyj} "
              f"cost={koszt:.4f} USD (total {self.koszt_usd:.4f})", file=sys.stderr)

if __name__ == "__main__":
    k = Konsultant(tryb_granicy="pytaj")
    print(k.zapytaj(
        "I have an agent with a tool loop on a local 20B model. "
        "The model sometimes repeats the same tool over and over. "
        "Which three mechanisms for detecting and breaking such a loop do you recommend?",
        klasa="C"))
    print(f"\ncalls={k.wywolan} cost={k.koszt_usd:.4f} USD")
PYEOF

$VENVS/claude/bin/python $AGENT/klient_claude.py
```

### 4.1 Five things you must know about this API

| Thing | Why it matters |
| :-- | :-- |
| **no `temperature`/`top_p`/`top_k`** | on Opus 5 they return a **400 error** — you steer through `effort` and the prompt |
| **`thinking` on by default** | Opus 5 thinks unless you turn it off; **`max_tokens` covers thinking + the answer** |
| **`cache_control`** | the system prefix gets ~10× cheaper; check `usage.cache_read_input_tokens` |
| **`stop_reason: "refusal"`** | ⭐ **check BEFORE reading `content`** — otherwise `IndexError` |
| **the cache is prefix matching** | the same rule as locally (part 8 §2.4) — a timestamp in the system prompt kills the cache |

💡 **Notice how much of part 8 carries over 1:1.** Prompt cache, token budget,
frozen prefix — the same mechanisms, a different provider. **This is no accident: these are properties
of transformers, not of a particular implementation.**

---

## 5. The hybrid router

Extend `router.py` from part 8 §4 with a third option:

```bash
cat > $AGENT/router_hybrydowy.py <<'PYEOF'
#!/usr/bin/env python3
"""Router: local small -> local large -> Claude (class B/C only)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MALY = "http://127.0.0.1:8081"
DUZY = "http://127.0.0.1:8082"

# The patterns match the Polish-language prompts
SYGNALY_CLAUDE = [
    r"(?i)\bzaprojektuj\s+(architektur|system)",
    r"(?i)\bzrefaktoryzuj\b.*\bwiele\b",
    r"(?i)\bdlaczego\b.*\bnie\s+dziala\b",
]

def klasa_danych(tekst: str) -> str:
    """Default A. Raise to B/C only on explicit grounds."""
    if re.search(r"(?i)\b(faktur|umow|klient|nip|pesel|kwota|brutto|netto)\b", tekst):
        return "A"
    if re.search(r"(?i)\b(błąd|error|traceback|architektur|zaprojektuj|wyjaśnij)\b", tekst):
        return "B"
    return "A"          # ⭐ by default it does NOT leave

def wybierz(messages, bledy: int = 0, tura: int = 1, claude_dostepny: bool = False):
    """Returns ('lokalny'|'claude', target, reason)."""
    ogon = " ".join(m["content"][:1500] for m in messages[-3:])
    klasa = klasa_danych(ogon)

    if claude_dostepny and klasa in ("B", "C"):
        if bledy >= 3:
            return "claude", None, f"{bledy} errors in a row, class {klasa} data"
        for s in SYGNALY_CLAUDE:
            if re.search(s, ogon):
                return "claude", None, f"strategic task, class {klasa} data"

    if bledy >= 2 or tura == 1:
        return "lokalny", DUZY, "planning / diagnosis locally"
    if len(ogon) > 30000:
        return "lokalny", DUZY, "long context"
    return "lokalny", MALY, "routine"

if __name__ == "__main__":
    ma_klucz = bool(os.environ.get("ANTHROPIC_API_KEY"))
    print(f"Claude available: {ma_klucz}\n")
    for tura, bledy, t in (
        (1, 0, "Przeczytaj plik vat.py."),
        (5, 0, "Wyciągnij dane z faktury FV/2025/143 na kwotę 1476,50 zł."),
        (8, 3, "Dlaczego ten import nie działa? Traceback: ModuleNotFoundError."),
        (2, 0, "Zaprojektuj architekturę modułu rozliczeń."),
    ):
        gdzie, cel, powod = wybierz([{"role": "user", "content": t}], bledy, tura, ma_klucz)
        etykieta = "CLAUDE" if gdzie == "claude" else ("local-large" if cel == DUZY else "local-small")
        print(f"[{klasa_danych(t)}] turn={tura} errors={bledy}")
        print(f"     {t[:58]}")
        print(f"     → {etykieta}  ({powod})\n")
PYEOF

python3 $AGENT/router_hybrydowy.py
```

⭐ **Note `klasa_danych`: by default it returns `"A"`.** Content containing an invoice will never
reach Claude, even if the agent has three errors in a row. **This is a safeguard that is
closed by default.**

---

## 6. Offline-first — the fallback mode is the primary mode

⭐ **This is the most important rule of hybrid architecture.**

```
The system MUST work fully without Claude.
Claude is an enhancement, never a dependency.
```

**A test you must pass:**

```bash
# Cut off Claude and run the full suite
unset ANTHROPIC_API_KEY
cd $AGENT && python3 pomiar-agenta.py

# The result MUST be comparable with part 8.
# If the agent does not work without Claude - you have built a cloud product
# and your thesis about data sovereignty is untrue.
```

⚠️ **Trap P52 (new): silent cloud dependency.**
You add Claude "only for hard cases". After a month 40% of turns go through the API,
and the agent without a network stops being useful. **Measure the share of cloud calls and set
a hard limit** — e.g. at most 3 per task.

```bash
# Add a counter to the consultant
cat >> $AGENT/klient_claude.py <<'PYEOF'

# ---------- hard limit on calls per task ----------------------------
class KonsultantZLimitem(Konsultant):
    def __init__(self, *a, limit_na_zadanie: int = 3, limit_usd: float = 0.50, **kw):
        super().__init__(*a, **kw)
        self.limit = limit_na_zadanie
        self.limit_usd = limit_usd

    def zapytaj(self, *a, **kw) -> str:
        if self.wywolan >= self.limit:
            return (f"[LIMIT] Used {self.limit} Claude calls on this task. "
                    f"Finish locally.")
        if self.koszt_usd >= self.limit_usd:
            return f"[COST LIMIT] {self.koszt_usd:.2f} USD. Finish locally."
        return super().zapytaj(*a, **kw)
PYEOF
```

---

## 7. Economics — calculate before you decide

```bash
python3 - <<'PYEOF'
# Monthly estimate
ZADAN_DZIENNIE   = 50
TUR_NA_ZADANIE   = 12
UDZIAL_CLAUDE    = 0.10          # 10% of turns
TOK_WEJ, TOK_WYJ = 8000, 1200
CENA_WEJ, CENA_WYJ = 5.00, 25.00   # Opus 5, USD/MTok
DNI = 22

tur_claude = ZADAN_DZIENNIE * TUR_NA_ZADANIE * UDZIAL_CLAUDE * DNI
koszt = tur_claude * (TOK_WEJ*CENA_WEJ + TOK_WYJ*CENA_WYJ) / 1_000_000
print(f"Claude calls / month:     {tur_claude:.0f}")
print(f"Cost without cache:       {koszt:8.2f} USD  (~PLN {koszt*4:.0f})")
print(f"Cost with prompt cache:   {koszt*0.35:8.2f} USD  (~PLN {koszt*0.35*4:.0f})")
print()
print("For comparison — local electricity:")
kwh = 1.03 * 8 * DNI          # ~1030 W for 8 h a day
print(f"  {kwh:.0f} kWh x PLN 0.90 = PLN {kwh*0.9:.0f}/month")
PYEOF
```

💡 **The conclusion that usually comes out:** with 10% of turns in the cloud, the cost of Claude is
**comparable to the electricity bill**. That is not an argument against — it is an argument for
a **conscious limit**. At 50% of turns the proportions flip and your cost advantage disappears.

---

## 8. Exercises

1. **Test the boundary on real data.** Take 20 real fragments from your
   documents, run them through `Granica` and count how many would pass. **Every pass of
   client data is a critical bug — add the missing patterns.**
2. **Measure whether Claude really helps.** Take 10 tasks on which the local agent failed.
   Run them with Claude as a consultant. **How many did it solve? What was the cost per solved
   task?**
3. **Cut-off test.** Run the full suite without `ANTHROPIC_API_KEY`. The result must be
   comparable with part 8.
4. **Add output logging.** Write every Claude call to the audit log
   from part 7: what was sent, of what class, what it cost. **This is proof of compliance for
   the client.**
5. **Weigh Sonnet 5 instead of Opus 5.** At 3/15 USD instead of 5/25 — measure whether quality drops
   on your consulting tasks. Often it does not.

---

## Check yourself

- [ ] What is the default data class and why that one?
- [ ] What is the "Claude as a consultant, not an executor" pattern?
- [ ] Why is the regex filter the second, not the first, line of defence?
- [ ] What must be checked before reading `content` from an Opus 5 response?
- [ ] Why does `temperature` not work on Opus 5?
- [ ] Which mechanisms from part 8 carry over 1:1 to the Claude API?
- [ ] What test must your system pass for the sovereignty thesis to be true?

## New traps

| ID | Trap | § |
| :-- | :-- | :-- |
| **P51** | A regex filter will let through what you did not anticipate | §3 |
| **P52** | Silent cloud dependency — measure the share and limit it | §6 |

---

## 🎓 End of the course

You have come all the way from "a model is a GGUF file" to your own safe, optimized
agent running offline on your hardware.

**What you have now:**

| | |
| :-- | :-- |
| `$KURS/` | measurement tools, RAG, evaluation suites |
| `$AGENT/` | ⭐ **your own agent loop** with a sandbox, audit and log |
| `$NARZEDZIA/whisper.cpp/`, `$NARZEDZIA/piper/` | speech input and output |
| traps **P20–P52** | 33 documented software traps |

**What next — in order:**

1. **Build a real evaluation suite** on your real invoices (50+ cases).
   Everything else without it is guessing.
2. **Run the agent on a real accounting task** and write down where it fails.
3. **Fix the harness, not the prompt** — that is the lesson of part 6.
4. **If you add more GPUs**, remap them in `rig-env.sh` (see the course index) and run a larger model such as `gpt-oss-120b`.
5. **Measure everything again.**

⭐ **The most important thing you take away from this course is not code.** It is the ability to
answer the question *"why is this slow / wrong / unstable"* — and to know
which layer to touch. The rest is details you will look up in `--help`.
