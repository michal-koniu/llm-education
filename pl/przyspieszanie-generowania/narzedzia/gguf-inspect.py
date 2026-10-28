#!/usr/bin/env python3
"""gguf-inspect.py MODEL.gguf [more.gguf ...]

Odpowiada na pytanie: "czy ten model ma wbudowana glowice do speculative decodingu (MTP/NextN)
i czym jest ten plik?"  Czyta TYLKO naglowki (nie ladujac wag), wiec dziala w sekundy.
Dla modelu dzielonego na czesci podaj pierwszy plik -- reszta zostanie dolaczona automatycznie.

Uruchamianie (venv z biblioteka gguf):
  ~/spec-dspark/venv/bin/python narzedzia/gguf-inspect.py PLIK.gguf
"""
import os, sys, re, glob
# gguf-py from your llama.cpp checkout; override with LLAMA_CPP=/path/to/llama.cpp
sys.path.insert(0, os.path.join(os.path.expanduser(os.environ.get("LLAMA_CPP", "~/llama.cpp")), "gguf-py"))
from gguf import GGUFReader

def shards(path):
    m = re.match(r"(.*)-(\d{5})-of-(\d{5})\.gguf$", path)
    return sorted(glob.glob(f"{m.group(1)}-*-of-{m.group(3)}.gguf")) if m else [path]

def val(f):
    try: return f.contents()
    except Exception:
        try: return f.parts[-1].tolist()
        except Exception: return "?"

for path in sys.argv[1:]:
    files = shards(path)
    r0 = GGUFReader(files[0])
    F = r0.fields
    arch = val(F["general.architecture"]); arch = arch if isinstance(arch, str) else bytes(arch).decode()
    print(f"=== {path}\n  czesci: {len(files)}   architektura: {arch}")
    for k in sorted(F):
        if any(s in k for s in ("block_count", "nextn", "mtp", "block_size", "target_layers", "mask_token", "expert_count", "expert_used")):
            v = val(F[k]); print(f"  {k} = {v if not isinstance(v, list) or len(v) < 12 else str(v[:12]) + '...'}")
    names = []
    for f in files: names += [t.name for t in GGUFReader(f).tensors]
    blk = sorted({int(n.split('.')[1]) for n in names if n.startswith('blk.') and n.split('.')[1].isdigit()})
    spec = [n for n in names if any(s in n for s in ("nextn", "mtp", "eh_proj", "markov", "conf_proj", "enc_output_norm", ".fc."))]
    print(f"  tensorow: {len(names)}   bloki: {blk[0] if blk else '-'}..{blk[-1] if blk else '-'} ({len(blk)})")
    if spec:
        print(f"  >>> tensory pomocnicze do speculative decodingu: {len(spec)}  np. {spec[:4]}")
    else:
        print("  >>> BRAK glowicy MTP/NextN/draftu w tym pliku (speculative decoding wymaga osobnego draftu lub n-gramow)")
    if arch in ("dflash", "eagle3"): print("  >>> To jest DRAFT (uzywasz go jako -md, nie jako -m).")
