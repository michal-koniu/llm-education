#!/usr/bin/env python3
"""translate_doc.py SRC.md OUT.md  -- tlumaczy dokument Markdown EN->PL lokalnym modelem (llama-swap :8080, alias 'deepseek'), sekcja po sekcji.
Nie dotyka bloków kodu w sposób programowy -- model dostaje je w tekście i ma je zostawić bez zmian (weryfikacja osobno)."""
import sys, json, re, time, urllib.request
SRC, OUT = sys.argv[1], sys.argv[2]
MODEL = sys.argv[3] if len(sys.argv) > 3 else "deepseek"
src = open(SRC, encoding="utf-8").read()
# ---- chunking: split on headings (level 1-3) outside code fences, merge up to ~5500 chars
lines = src.split("\n"); chunks = []; cur = []; fence = False
for ln in lines:
    if ln.startswith("```"): fence = not fence
    if not fence and re.match(r"^#{1,3} ", ln) and cur and sum(len(x)+1 for x in cur) > 3000:
        chunks.append("\n".join(cur)); cur = []
    cur.append(ln)
if cur: chunks.append("\n".join(cur))
print(f"{len(src)} chars -> {len(chunks)} chunks: {[len(c) for c in chunks]}", flush=True)
SYSTEM = """Jesteś profesjonalnym tłumaczem technicznym EN→PL. Tłumaczysz fragment dokumentacji o LLM (llama.cpp) na naturalny, poprawny język polski dla inżynierów.
Zasady (bezwzględne):
1. Zachowaj dokładnie strukturę Markdown: te same nagłówki (# ## ###), listy, tabele, linki, pogrubienia. Tłumacz TEKST nagłówków, nie ich poziomy.
2. BLOKI KODU (``` ... ```) przepisz BEZ ŻADNEJ ZMIANY, znak w znak — łącznie z komentarzami i flagami. Nie tłumacz niczego wewnątrz bloków kodu.
3. Nie tłumacz i nie zmieniaj: nazw flag (--spec-type …), nazw parametrów, nazw plików, nazw modeli, URL-i, numerów PR (#12345), nazw własnych, nazw technologii w `backtickach`.
4. Terminy techniczne: „speculative decoding” → „speculative decoding” (przy pierwszym użyciu możesz dodać polski opis w nawiasie), „draft model” → „model draftu”, „target model” → „model docelowy”, „acceptance rate” → „współczynnik akceptacji”, „tokens” → „tokeny”.
5. Nie dodawaj komentarzy, wyjaśnień ani wstępu. Nie pomijaj niczego. Zwróć WYŁĄCZNIE przetłumaczony fragment w Markdown."""
def call(text):
    body = dict(model=MODEL, temperature=0.2, max_tokens=8192, stream=False,
                chat_template_kwargs={"enable_thinking": False},
                messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}])
    r = urllib.request.Request("http://localhost:8080/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    x = json.load(urllib.request.urlopen(r, timeout=1800)); m = x["choices"][0]["message"]
    return (m.get("content") or "").strip("\n"), x["timings"], x["choices"][0]["finish_reason"], bool(m.get("reasoning_content"))
out = []; t0 = time.time(); tot = 0
for i, c in enumerate(chunks, 1):
    for attempt in range(3):
        txt, tm, fin, had_reasoning = call(c)
        if fin == "stop" and txt: break
        print(f"  chunk {i}: retry (finish={fin})", flush=True)
    tot += tm["predicted_n"]
    print(f"chunk {i}/{len(chunks)}: {len(c)} -> {len(txt)} chars, {tm['predicted_n']} tok @ {tm['predicted_per_second']:.1f} tok/s, draft {tm.get('draft_n_accepted')}/{tm.get('draft_n')}, finish={fin}, reasoning_used={had_reasoning}", flush=True)
    out.append(txt)
open(OUT, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"DONE {len(chunks)} chunks, {tot} tokens in {time.time()-t0:.0f}s ({tot/(time.time()-t0):.1f} tok/s overall)", flush=True)
