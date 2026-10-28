#!/usr/bin/env python3
"""verify_translation.py EN.md PL.md -- mechaniczna weryfikacja tlumaczenia dokumentu Markdown."""
import re, sys, collections
en = open(sys.argv[1], encoding="utf-8").read(); pl = open(sys.argv[2], encoding="utf-8").read()
def blocks(t): return re.findall(r"^```[^\n]*\n.*?^```[ \t]*$", t, flags=re.S | re.M)
def strip_blocks(t): return re.sub(r"^```[^\n]*\n.*?^```[ \t]*$", "", t, flags=re.S | re.M)
ok = True
def rep(name, good, detail=""):
    global ok; ok &= good; print(("PASS " if good else "FAIL ") + name + (f" -- {detail}" if detail else ""))
be, bp = blocks(en), blocks(pl)
rep("liczba blokow kodu", len(be) == len(bp), f"{len(be)} vs {len(bp)}")
diff = [i for i, (a, b) in enumerate(zip(be, bp)) if a != b]
rep("bloki kodu identyczne znak w znak", not diff and len(be) == len(bp), f"{len(be)-len(diff)}/{len(be)} identycznych")
for i in diff[:6]:
    a, b = be[i].split("\n"), bp[i].split("\n")
    d = [(x, y) for x, y in zip(a, b) if x != y][:2]
    print(f"   blok {i}: EN={d[0][0]!r}\n           PL={d[0][1]!r}" if d else f"   blok {i}: rozna liczba linii {len(a)} vs {len(b)}")
pe, pp = strip_blocks(en), strip_blocks(pl)
def ms(rx, t): return collections.Counter(re.findall(rx, t))
for name, rx in [("adresy URL", r"https?://[^\s)>\]]+"), ("kod inline w `backtickach`", r"`[^`\n]+`"), ("flagi --xxx", r"--[a-z][a-z0-9-]*"), ("numery PR (#123)", r"#\d{3,}")]:
    a, b = ms(rx, pe), ms(rx, pp); miss, extra = a - b, b - a
    rep(name, not miss and not extra, f"EN {sum(a.values())} vs PL {sum(b.values())}" + (f"; brak w PL: {list(miss)[:6]}" if miss else "") + (f"; nadmiarowe w PL: {list(extra)[:6]}" if extra else ""))
he = re.findall(r"^(#{1,6}) ", pe, flags=re.M); hp = re.findall(r"^(#{1,6}) ", pp, flags=re.M)
rep("naglowki: liczba i poziomy", he == hp, f"EN {len(he)} vs PL {len(hp)}")
def tables(t): 
    out = []; cur = 0
    for ln in t.split("\n"):
        if ln.strip().startswith("|"): cur += 1
        elif cur: out.append(cur); cur = 0
    return out + ([cur] if cur else [])
rep("tabele: liczba wierszy", tables(pe) == tables(pp), f"EN {tables(pe)} vs PL {tables(pp)}")
ne = ms(r"(?<![\w.-])\d+(?:[.,]\d+)?(?![\w-])", re.sub(r"`[^`\n]*`|https?://\S+", "", pe)); np_ = ms(r"(?<![\w.-])\d+(?:[.,]\d+)?(?![\w-])", re.sub(r"`[^`\n]*`|https?://\S+", "", pp))
miss = {k: v for k, v in (ne - np_).items()}; extra = {k: v for k, v in (np_ - ne).items()}
rep("liczby w tekscie (poza kodem/URL)", not miss and not extra, f"brak w PL: {miss}; nadmiar w PL: {extra}" if (miss or extra) else f"{sum(ne.values())} liczb zgodnych")
lines_e, lines_p = [l for l in en.split("\n")], [l for l in pl.split("\n")]
print(f"INFO dlugosc: EN {len(en)} znakow / {len(lines_e)} linii; PL {len(pl)} znakow / {len(lines_p)} linii; stosunek {len(pl)/len(en):.2f}")
stop = re.compile(r"\b(the|and|is|are|of|to|for|with|this|that|which|when|can|from|by|it)\b", re.I)
left = [l for l in strip_blocks(pl).split("\n") if len(stop.findall(l)) >= 3 and not re.search(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]", l) and not l.strip().startswith(("|", "-->"))]
rep("brak nieprzetlumaczonych zdan (heurystyka)", not left, f"{len(left)} podejrzanych linii" if left else "")
for l in left[:6]: print("   ?", l[:140])
print("\nWYNIK MECHANICZNY:", "WSZYSTKO OK" if ok else "SA ROZBIEZNOSCI")
