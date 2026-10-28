#!/usr/bin/env python3
"""try_entries.py -- dopisuje tymczasowe wpisy do config.yaml, dla kazdego: laduje, uruchamia bench_spec.py, zbiera VRAM i bledy z logu, na koncu przywraca config.
Uzycie: edytuj slownik E (nazwa -> argumenty serwera). Wynik: ~/spec-dspark/results/<nazwa>.log"""
import subprocess, time, json, urllib.request, sys, os
p=os.path.expanduser("~/.config/llama-swap/config.yaml")
NEW=os.path.expanduser("~/llama.cpp-0ce8cd1/build/bin/llama-server")
GGUF=os.path.expanduser("~/models/DeepSeek-V4-Flash-0731-GGUF/UD-IQ3_XXS/DeepSeek-V4-Flash-0731-UD-IQ3_XXS-00001-of-00004.gguf")
DRAFT=os.path.expanduser("~/models/DeepSeek-V4-Flash-0731-GGUF/DSpark/DeepSeek-V4-Flash-0731-DSpark.gguf")
SPEC=f"-md {DRAFT} --spec-type draft-dspark --spec-draft-n-max 3 --spec-draft-p-min 0"
LAYER="--split-mode layer --tensor-split 0.97,1,0.92,1.11"
TENSOR="--split-mode tensor -ctk f16 -ctv f16"
COMMON="-ngl 999 --load-mode dio --parallel 1 --ctx-size 131072 --ubatch-size 1024 --temp 1.0 --top-p 1.0 --top-k 0 --min-p 0"
def spec(n,pmin=0): return f"-md {DRAFT} --spec-type draft-dspark --spec-draft-n-max {n} --spec-draft-p-min {pmin}"
TT="--split-mode tensor -ctk f16 -ctv f16"
C4=COMMON.replace("--ubatch-size 1024","--ubatch-size 512").replace("--parallel 1 --ctx-size 131072","--parallel 4 --ctx-size 524288")
def C(par,ctx): return COMMON.replace("--ubatch-size 1024","--ubatch-size 512").replace("--parallel 1 --ctx-size 131072",f"--parallel {par} --ctx-size {ctx}")
E={
 "tmp-p2-131k": f"{spec(3)} {TT} {C(2,262144)}",
 "tmp-p2-98k":  f"{spec(3)} {TT} {C(2,196608)}",
 "tmp-p4-65k":  f"{spec(3)} {TT} {C(4,262144)}",
}
EXTRA_ENV=json.loads(os.environ.get("EXTRA_ENV","[]"))
orig=open(p).read(); marker="  # Wariant CPU"
add="".join(f"""  "{n}":
    cmd: |
      {NEW} --port ${{PORT}} --jinja --agent -fa on
      -m {GGUF}
      {a}
    env:
      - "HIP_VISIBLE_DEVICES=0,1,2,3"
""" + "".join(f'      - "{e}"\n' for e in EXTRA_ENV) + "    ttl: 600\n\n" for n,a in E.items())
open(p,"w").write(orig.replace(marker,add+marker,1)); time.sleep(4)
def vramfree():
    o=subprocess.run("rocm-smi --showmeminfo vram",shell=True,capture_output=True,text=True).stdout.splitlines()
    u=[int(l.split()[-1]) for l in o if "Total Used" in l][:4]; t=[int(l.split()[-1]) for l in o if "Total Memory" in l][:4]
    return [round((a-b)/1e9,2) for b,a in zip(u,t)]
R=os.path.expanduser("~/spec-dspark/results/")
try:
    for n in E:
        t=time.time()
        body=dict(model=n,max_tokens=8,temperature=0,messages=[{"role":"user","content":"hi"}])
        try:
            r=urllib.request.Request("http://localhost:8080/v1/chat/completions",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
            urllib.request.urlopen(r,timeout=700).read(); ok=True
        except Exception as e:
            ok=False; print(f"### {n}: LOAD/CALL FAILED after {time.time()-t:.0f}s: {str(e)[:100]}",flush=True)
            log=subprocess.run("timeout 4 curl -s -N localhost:8080/logs/stream/upstream | grep -iE 'error|fail|not impl|abort|assert|unsupported|out of memory|invalid' | tail -12",shell=True,capture_output=True,text=True).stdout
            print(log[-1800:],flush=True)
        if ok:
            print(f"### {n}: loaded in {time.time()-t:.0f}s, VRAM free per card {vramfree()}",flush=True)
            env=dict(os.environ,BENCH_REPS=os.environ.get("BENCH_REPS","1"))
            out=subprocess.run(["python3",os.path.join(os.path.dirname(os.path.abspath(__file__)),"bench_spec.py"),n,R+n+".json"],capture_output=True,text=True,env=env).stdout
            open(R+n+".log","w").write(out)
            print(out[out.find("=== SUMMARY"):],flush=True)
finally:
    open(p,"w").write(orig); print("config restored",flush=True)
