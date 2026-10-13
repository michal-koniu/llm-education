# Part 17 · Hybrid and router — local by default, cloud by conscious choice

**Level:** ⭐⭐⭐ · **Time:** ~4 h · **Requires:** parts 14 (evaluation), 15 (metrics), 16 (security)
**Produces:** a router, a privacy boundary expressed in code, an egress audit, a full offline mode

---

## 0. A starting principle

**Local is the default. Cloud is the exception that has to justify itself.** Not the
other way round.

This is not ideology, just three countable reasons:

| Reason | Number |
| :-- | :-- |
| **Marginal cost** | locally ≈ electricity. An agent grinding for 40 min at night costs pennies |
| **Privacy** | content that never left cannot leak — **technically enforceable** |
| **Availability** | no network, no limits, no price change in someone else's quarter |

⭐ **At the same time: refusing to use the cloud where it genuinely wins is a cost,
not a virtue.** This part teaches you to **settle that by measurement** and to write
the verdict into code, not into good intentions.

---

## 1. The router's three questions — in this order

```
1. PRIVACY     →  may this content be sent at all?     ← hard gate
2. CAPABILITY  →  will the local model do it?          ← from measurement, not gut feeling
3. COST        →  is the difference worth paying for?  ← a number
```

⚠️ **The order is non-negotiable.** A router that asks about capability first and
privacy second **will one day send something it should not** — because the "the local
model failed, try the cloud" path bypasses the gate. Privacy comes **first and is a
gate, not a weight in a scoring function**.

---

## 2. The privacy boundary as code

A declaration in a policy document is worth as much as the discipline of the person
writing code at 11 p.m. **The boundary has to be enforced, not declared.**

```python
# $OSA/router/granica.py
"""The only path for content to the outside. Everything else is an architecture bug."""
import re, hashlib, os, pathlib, json

class Odmowa(Exception): pass

KATALOGI_ZAKAZANE = ["~/dokumenty", "~/.ssh", "~/.config", "$OSA/pamiec"]

WZORCE_ZAKAZANE = [
    (r"\b\d{10}\b",                          "NIP"),
    (r"\b\d{11}\b",                          "PESEL"),
    (r"\bPL\d{26}\b",                        "IBAN"),
    (r"[\w.+-]+@[\w-]+\.[\w.]+",             "e-mail"),
    (r"\b(?:\+48\s?)?\d{3}[\s-]?\d{3}[\s-]?\d{3}\b", "telefon"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----",  "klucz prywatny"),
    (r"\b(sk-|ghp_|xoxb-)[A-Za-z0-9_-]{16,}", "token API"),
]

def sprawdz(tresc: str, zrodlo: str, zgoda_jawna=False) -> None:
    """Raises Odmowa if the content may not leave the machine."""
    for k in KATALOGI_ZAKAZANE:
        if str(pathlib.Path(os.path.expandvars(k)).expanduser()) in zrodlo:
            raise Odmowa(f"Source '{zrodlo}' is in a forbidden directory ({k}).")
    znalezione = [n for w, n in WZORCE_ZAKAZANE if re.search(w, tresc)]
    if znalezione and not zgoda_jawna:
        raise Odmowa(f"Content contains: {', '.join(set(znalezione))}. "
                     f"Sending requires explicit consent or anonymization.")

def anonimizuj(tresc: str) -> tuple[str, dict]:
    """Replacement with placeholders. Reversible once the response comes back."""
    mapa = {}
    for wzor, nazwa in WZORCE_ZAKAZANE:
        for m in re.finditer(wzor, tresc):
            if m.group() not in mapa:
                mapa[m.group()] = f"[{nazwa}_{len(mapa)+1}]"
    for orig, zast in mapa.items():
        tresc = tresc.replace(orig, zast)
    return tresc, mapa

def przywroc(tresc: str, mapa: dict) -> str:
    for orig, zast in mapa.items():
        tresc = tresc.replace(zast, orig)
    return tresc
```

⚠️ **P51 from course 1 applies in full: a regex filter lets through what you did not
anticipate.** A surname in the text of a contract matches no pattern. Therefore:

⭐ **The real boundary is `KATALOGI_ZAKAZANE`, not `WZORCE_ZAKAZANE`.** The rule
"content from `~/dokumenty` **never** leaves" is unambiguous and does not depend on the
ingenuity of the patterns. The patterns are the second layer — they catch an accidental
paste, not a systematic leak.

### 2.1 · One exit, hard

```python
# $OSA/router/wyjscie.py
import os, pathlib
"""The ONLY function in the system that makes a request to the cloud."""
def wyslij_na_zewnatrz(tresc, zrodlo, powod, zgoda=False, anonimizuj_auto=True):
    sprawdz(tresc, zrodlo, zgoda_jawna=zgoda)          # 1. gate
    mapa = {}
    if anonimizuj_auto:
        tresc, mapa = anonimizuj(tresc)                 # 2. placeholders
    _audyt(tresc, zrodlo, powod, mapa)                  # 3. ⭐ trace ALWAYS
    odp = _wywolaj_claude(tresc)                        # 4. only now
    return przywroc(odp, mapa)

def _audyt(tresc, zrodlo, powod, mapa):
    """Full record. This is what makes §6 possible."""
    with open(pathlib.Path(os.environ["OSA"], "dziennik/wyjscie.jsonl"),
              "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "ts": TERAZ(), "zrodlo": zrodlo, "powod": powod,
            "znakow": len(tresc),
            "sha256": hashlib.sha256(tresc.encode()).hexdigest(),
            "anonimizowano": list(mapa.values()),
            "pierwsze_200": tresc[:200],
        }, ensure_ascii=False) + "\n")
```

⭐ **The `sha256` of the full content without the content itself** is a good
compromise: you can prove **what** you sent (by comparing the hash) without creating a
second copy of your data in the log. The same principle as sanitizing traces in
part 15.

---

## 3. Where the cloud genuinely wins

Do not guess — **measure on your golden set**. But here is where to expect a
difference and where there is none:

| Task | Local | Cloud | Verdict |
| :-- | :-- | :-- | :-- |
| Classification, grammar-constrained extraction | ⭐ | ⭐ | **local** — a tie, so cheaper |
| Retrieval with a quote | ⭐ | ⭐ | **local** |
| Colloquial Polish | ⭐ Bielik | ⭐ | **local** |
| Reasoning over 10+ steps | ⚠️ | ⭐⭐ | **cloud**, if permitted |
| Code in a less common language | ⚠️ | ⭐⭐ | cloud |
| Very long context (>100k) | ✗ | ⭐⭐ | cloud |
| Synthesis from 20 sources | ⚠️ | ⭐⭐ | depends — **measure** |
| Bulk, overnight work | ⭐⭐ | 💸 | ⭐ **local, no contest** |
| Anything involving your documents | ⭐ | ✗ | **local — gate** |

⭐ **The last row rules out most of what your system does.** The Archivist will never
go to the cloud. The Host almost never. The real candidate is the **Researcher** —
because it works on public content that it has just downloaded from the internet
anyway.

> 💡 **This is an interesting consequence of your architecture: the only agent allowed
> to be sent to the cloud is the one that processes the least sensitive data.** The
> privacy boundary and the trust boundary coincide almost perfectly — only inverted.

---

## 4. The Claude client — the minimum that works

I keep this short because the cloud is the exception in your setup. But it has to work
correctly.

```python
# $OSA/router/klient_claude.py
"""Called ONLY by wyjscie.py. Never directly."""
import anthropic, os

KLIENT = anthropic.Anthropic()       # ANTHROPIC_API_KEY from the GATEWAY's environment (not the sandbox's!)
MODEL  = "claude-opus-5"

def _wywolaj_claude(tresc: str, system: str = "", max_tokens=4096) -> str:
    with KLIENT.messages.stream(                 # ⭐ stream: no timeout on long output
        model=MODEL,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},           # ⭐ adaptive thinking
        system=[{"type": "text", "text": system,
                 "cache_control": {"type": "ephemeral"}}] if system else [],
        messages=[{"role": "user", "content": tresc}],
    ) as s:
        wiadomosc = s.get_final_message()

    if wiadomosc.stop_reason == "refusal":       # ⚠️ P134 — check BEFORE reading the content
        raise Odmowa("The model refused to answer (stop_reason=refusal).")

    return "".join(b.text for b in wiadomosc.content if b.type == "text")
```

**Four things that are easy to get wrong:**

| Thing | Correct |
| :-- | :-- |
| Thinking | `thinking={"type": "adaptive"}`. ⚠️ `budget_tokens` is **rejected with a 400 error** on Opus 5 |
| Sampling | ⚠️ **`temperature`, `top_p`, `top_k` → 400.** A habit carried over from local models |
| Streaming | by default for long output — otherwise the request times out |
| Refusal | `stop_reason == "refusal"` checked **before** reading `content` |

⚠️ **The API key lives in the gateway's environment and never reaches the sandbox**
(part 10, P101). The agent does not have the key — it has the **capability** to call
through the gateway, which the gateway sees and can reject.

---

## 5. The router

```python
# $OSA/router/router.py
"""Three questions in order. Privacy is a GATE, not a weight."""

SILNIKI = {
    "lokalny_szybki": {"url": "http://127.0.0.1:8080/v1", "model": "gpt-oss-20b",
                       "okno": 32768, "s_na_1k": 1.2, "poziom": 1},
    "lokalny_mocny":  {"url": "http://127.0.0.1:8080/v1", "model": "qwen3-32b",
                       "okno": 32768, "s_na_1k": 3.4, "poziom": 2},
    "chmura":         {"model": "claude-opus-5", "okno": 1_000_000,
                       "usd_we": 5.0, "usd_wy": 25.0, "poziom": 3},
}

def wybierz(zadanie: dict) -> tuple[str, str]:
    # 1 · PRIVACY — gate
    try:
        sprawdz(zadanie["tresc"], zadanie["zrodlo"])
        wolno_na_zewnatrz = True
    except Odmowa as e:
        wolno_na_zewnatrz, powod_blokady = False, str(e)

    # 2 · HARD CONSTRAINTS
    if zadanie["tokenow"] > 30_000:
        if not wolno_na_zewnatrz:
            return "lokalny_mocny", f"too long, but {powod_blokady} → splitting into stages"
        return "chmura", "context exceeds the local window"

    # 3 · CAPABILITY — from measurement, not gut feeling
    poziom = _wymagany_poziom(zadanie["kategoria"])     # from the table in §5.1
    if poziom <= 1: return "lokalny_szybki", "category within reach of the small model"
    if poziom <= 2: return "lokalny_mocny",  "needs the stronger local model"
    if not wolno_na_zewnatrz:
        return "lokalny_mocny", f"would need the cloud, but {powod_blokady} → trying locally"
    return "chmura", "measured cloud advantage in this category"
```

### 5.1 · The level table — you fill it in by measurement, not by intuition

```bash
# Run the golden set (part 14) on all three engines
for s in lokalny_szybki lokalny_mocny chmura; do
  python3 ewaluacja/uruchom.py --silnik $s --przebiegow 3 > pomiary/router/$s.json
done
python3 router/zbuduj_tabele.py > router/poziomy.json
```

| Category | fast | strong | cloud | **required level** |
| :-- | --: | --: | --: | --: |
| wyszukanie_z_cytatem | | | | |
| synteza | | | | |
| poprawna_odmowa | | | | |
| wieloetapowe | | | | |
| odpornosc | | | | |

⭐ **Filling-in rule: the required level is the LOWEST one that reaches at least 90%
of the best score.** Not the highest available. If the small model gives 88% of what
the cloud does — you choose the small one, because the difference is not worth leaving
the machine.

### 5.2 · Escalation that does not break the gate

```python
def wykonaj_z_eskalacja(zadanie, prog_pewnosci=0.6):
    silnik, powod = wybierz(zadanie)
    wynik = _uruchom(silnik, zadanie)
    if wynik["pewnosc"] >= prog_pewnosci or SILNIKI[silnik]["poziom"] == 3:
        return wynik
    wyzsze = [n for n, s in SILNIKI.items() if s["poziom"] > SILNIKI[silnik]["poziom"]]
    for n in sorted(wyzsze, key=lambda x: SILNIKI[x]["poziom"]):
        if n == "chmura":
            try: sprawdz(zadanie["tresc"], zadanie["zrodlo"])   # ⭐ GATE AGAIN
            except Odmowa: continue                              # ⚠️ P132
        w = _uruchom(n, zadanie)
        if w["pewnosc"] >= prog_pewnosci:
            return w
    return wynik
```

⚠️ **The `sprawdz()` line inside the escalation loop is the one that gets forgotten** —
and it is **the most common way data leaks from hybrid systems**. The main path checks
privacy, the fallback path does not. Check on **every** crossing of the boundary.

---

## 6. EXPERIMENT 17 — egress audit

⭐ **The question: what has actually left your machine in the last week?**

```bash
python3 router/audyt.py --okres 7d
```

```
═══ EGRESS AUDIT · 7 days ═══
  requests to the cloud:        23
  characters sent:      184,200
  tokens in/out:    46,100 / 12,400
  cost:                $0.54

  by agent:         badacz 21 · nadzorca 2 · archiwista 0 ✓ · gospodarz 0 ✓
  by reason:        context too long 11 · measured advantage 9 · escalation 3
  anonymized:       e-mail 14× · phone 3× · NIP 1×
  ⚠️ rejected by the gate: 7   (4× forbidden directory, 3× pattern)

  ⚠️ TO REVIEW: 2 requests with >20,000 characters
     2026-09-21 14:02  badacz  sha 8f3a…  "Analyze the 14 articles below…"
     2026-09-23 09:41  badacz  sha c21e…  "Compare the positions in these documents…"
```

**Four questions for this report:**

1. **Do the Archivist and the Host have zero?** If not — you have an architecture bug,
   not a configuration one.
2. **Were the 7 rejections mistakes, or real attempts?** Review each one.
3. **Did the two large requests have to be that large?** Usually they could have been
   summarized locally and the summary sent.
4. **Does the reason "escalation" × 3 mean the confidence threshold is too high?**

### 6.1 · Full offline test

```bash
sudo nft add rule inet filter output ip daddr != 127.0.0.1 drop   # cut off
python3 ewaluacja/uruchom.py --przebiegow 3 --oczekuj-offline
sudo nft flush chain inet filter output                            # restore
```

| Measure | Online | Offline | Δ |
| :-- | --: | --: | --: |
| Golden set score | | | |
| Tasks completed | | | |
| Tasks degraded | 0 | | |
| **Tasks failed** | | | ⭐ **target: 0** |

⭐ **Pass criterion: zero FAILED tasks.** Degraded ones (a worse result, clearly
marked) are fine. Failed ones mean a **silent dependency on the cloud** — something in
the system assumes a network and has no fallback path. This is P52 from course 1 and
the best way to find it in your own system.

---

## 7. EXERCISE

1. Implement `granica.py` with **one** exit function. Audit the code: no other place
   makes a request to the outside.

```bash
grep -rn "anthropic\|api.anthropic\|requests.post\|urlopen" $OSA --include=*.py \
  | grep -v "router/klient_claude.py\|piaskownica/proxy.py"
# expect: empty
```

2. Build the level table by **measurement** on the golden set.
3. A router with three questions and the gate **also in escalation**.
4. Egress audit + a weekly report in the nightly job (part 11).
5. The offline test. Fix every failed task.
6. Write `decyzje/0005-granica-prywatnosci.md`: what **never** leaves, what leaves with
   consent, what leaves freely — and how this is **enforced**.

---

## 8. Traps of this part

| ID | Trap | Symptom | How to avoid |
| :-- | :-- | :-- | :-- |
| **P132** | **The privacy gate bypassed in escalation** | The main path checks, the fallback does not — and that is where it leaks | `sprawdz()` on **every** crossing of the boundary, not once per task |
| **P133** | **A boundary based on patterns instead of on the source** | A surname in a contract matches no regex and goes out | Forbidden directories are the boundary; patterns are the second layer |
| **P134** | **An unread `stop_reason`** | A model refusal read as an empty answer; the agent carries on with nothing | `stop_reason == "refusal"` checked **before** `content` |
| **P135** | **A silent dependency on the cloud** | No network → the system does not work, though "local is the default" | The offline test, criterion: zero **failed** tasks |

---

## 9. Checkpoint

```bash
cd $OSA
python3 - <<'EOF'
from router.granica import sprawdz, Odmowa, anonimizuj, przywroc
try: sprawdz("cokolwiek", "/home/u/dokumenty/umowa.txt"); print("✗ P133")
except Odmowa: print("✓ forbidden directory")
try: sprawdz("NIP 1234567890", "/tmp/x"); print("✗ pattern")
except Odmowa: print("✓ pattern")
t, m = anonimizuj("kontakt: jan@example.com, tel 501234567")
assert "@" not in t and przywroc(t, m).count("jan@") == 1
print("✓ reversible anonymization")
EOF
python3 router/audyt.py --okres 7d
python3 ewaluacja/uruchom.py --offline --wymagaj-zero-nieudanych \
  && echo "✓ full offline with no failed tasks"
git add -A && git commit -m "part 17: router, privacy boundary, egress audit, offline"
```

- [ ] Order of questions: **privacy → capability → cost**, and privacy is a gate
- [ ] A boundary based on the **source**, patterns as the second layer
- [ ] **One** exit function in the whole system — verified with `grep`
- [ ] Every exit leaves a trace with a content hash
- [ ] Reversible anonymization
- [ ] Level table filled in by **measurement**; the 90% rule
- [ ] The gate checked **also in escalation**
- [ ] API key in the gateway's environment, **never** in the sandbox
- [ ] ⭐ **The audit shows: Archivist and Host — zero exits**
- [ ] ⭐ **Full offline: zero failed tasks**

---

**Next: `18-RELEASE-AND-MAINTENANCE.md`** — versioning, rollback and a runbook for
three in the morning.
