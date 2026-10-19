#!/bin/bash
# find-drafts.sh NAZWA_MODELU   (np. find-drafts.sh DeepSeek-V4-Flash  /  Qwen3-30B-A3B  /  gpt-oss-120b)
# Szuka na Hugging Face gotowych draftow do speculative decodingu dla danego modelu: MTP, EAGLE-3, DFlash, DSpark, "speculator".
# Wynik to LISTA KANDYDATOW -- zawsze sprawdz kartę modelu: czy zgadza sie model bazowy/wersja/tokenizer.
Q="${1:?podaj nazwe modelu, np. Qwen3-30B-A3B}"
for kw in mtp eagle3 dflash dspark speculator draft; do
  echo "--- $Q + $kw"
  curl -s --max-time 20 "https://huggingface.co/api/models?search=${Q}+${kw}&limit=12&sort=downloads&direction=-1" |
  python3 -c "
import sys,json
try: d=json.load(sys.stdin)
except Exception: d=[]
for m in d: print('  ',m['id'],'|',m.get('downloads'),'pobran')
if not d: print('   (brak)')
"
done
echo; echo "Tez sprawdz: config.json modelu bazowego -> 'num_nextn_predict_layers' > 0 oraz klucze 'mtp.*' w model.safetensors.index.json (oznacza: checkpoint MA glowice MTP)."
