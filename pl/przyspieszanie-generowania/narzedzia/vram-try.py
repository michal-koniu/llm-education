#!/usr/bin/env python3
"""vram-try.py -- SZABLON. Tymczasowo dopisuje do config.yaml wpisy llama-swap o roznych ustawieniach pamieci,
laduje kazdy jednym zapytaniem, zapisuje WOLNY VRAM na kazdej karcie i przywraca config.
Edytuj: GGUF/DRAFT (sciezki), BASE (stale flagi) i slownik V (nazwa -> (tensor-split, dodatkowe flagi, ctx, parallel)).
Uwaga: zapis config.yaml zwalnia zaladowany model; nie uruchamiaj w trakcie waznej pracy."""
import subprocess, time, json, urllib.request, re, sys, os
p=os.path.expanduser("~/.config/llama-swap/config.yaml")
GGUF=os.path.expanduser("~/models/DeepSeek-V4-Flash-0731-GGUF/UD-IQ3_XXS/DeepSeek-V4-Flash-0731-UD-IQ3_XXS-00001-of-00004.gguf")
DRAFT=os.path.expanduser("~/models/DeepSeek-V4-Flash-0731-GGUF/DSpark/DeepSeek-V4-Flash-0731-DSpark.gguf")
V={
 "tmp-u512":  ("0.97,1,0.92,1.11","--spec-draft-type-k q8_0 --spec-draft-type-v q8_0 --ubatch-size 512",524288,4),
 "tmp-u768":  ("0.97,1,0.92,1.11","--spec-draft-type-k q8_0 --spec-draft-type-v q8_0 --ubatch-size 768",524288,4),
 "tmp-par2":  ("0.97,1,0.92,1.11","--spec-draft-type-k q8_0 --spec-draft-type-v q8_0",262144,2),
 "tmp-par2u512":  ("0.97,1,0.92,1.11","--spec-draft-type-k q8_0 --spec-draft-type-v q8_0 --ubatch-size 512",262144,2),
}
orig=open(p).read(); marker="  # Wariant CPU"
def entry(n,sp,extra,ctx,par):
    return f"""  "{n}":
    cmd: |
      ${{server}}
      -m {GGUF}
      -md {DRAFT}
      --spec-type draft-dspark --spec-draft-n-max 3 --spec-draft-p-min 0 {extra}
      -ngl 999 --split-mode layer --tensor-split {sp} --ctx-size {ctx} --load-mode dio
      --parallel {par} {'' if 'ubatch' in extra else '--ubatch-size 1024'}
      --temp 1.0 --top-p 1.0 --top-k 0 --min-p 0
    env:
      - "HIP_VISIBLE_DEVICES=0,1,2,3"
    ttl: 600

"""
open(p,"w").write(orig.replace(marker,"".join(entry(n,*v) for n,v in V.items())+marker,1)); time.sleep(4)
def vram():
    o=subprocess.run("rocm-smi --showmeminfo vram",shell=True,capture_output=True,text=True).stdout
    used=[int(l.split()[-1]) for l in o.splitlines() if "Total Used" in l][:4]
    tot=[int(l.split()[-1]) for l in o.splitlines() if "Total Memory" in l][:4]
    return [round((t-u)/1e9,2) for u,t in zip(used,tot)]
try:
    for n,v in V.items():
        body=dict(model=n,max_tokens=40,temperature=0,messages=[{"role":"user","content":"Count from 1 to 20."}])
        t=time.time()
        try:
            r=urllib.request.Request("http://localhost:8080/v1/chat/completions",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
            x=json.load(urllib.request.urlopen(r,timeout=600)); ok="OK tps %.1f"%x["timings"]["predicted_per_second"]
        except Exception as e: ok="FAIL "+str(e)[:80]
        print(n, v, ok, "load %.0fs"%(time.time()-t), "FREE GB per card:", vram(), flush=True)
finally:
    open(p,"w").write(orig); print("config restored")
