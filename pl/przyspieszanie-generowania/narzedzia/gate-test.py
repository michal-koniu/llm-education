#!/usr/bin/env python3
"""test_candidate.py -- bramka przed wdrozeniem: prefill 6k, 1/2/4 agentow, identycznosc z modelem bez draftu, wolny VRAM po uzyciu.
Dodaje tymczasowy wpis 'tmp-candidate' (NOWY llama-server, tensor split, 2 sloty x 98k, DSpark n=3) i porownuje do 'deepseek-v4-flash-0731-nospec' (stary uklad)."""
import subprocess, time, json, urllib.request, random, os, threading, statistics
p="/home/USER/.config/llama-swap/config.yaml"
NEW="/home/USER/llama.cpp-0ce8cd1/build/bin/llama-server"
GGUF="/home/USER/models/DeepSeek-V4-Flash-0731-GGUF/UD-IQ3_XXS/DeepSeek-V4-Flash-0731-UD-IQ3_XXS-00001-of-00004.gguf"
DRAFT="/home/USER/models/DeepSeek-V4-Flash-0731-GGUF/DSpark/DeepSeek-V4-Flash-0731-DSpark.gguf"
CAND="tmp-candidate"; BASE="deepseek-v4-flash-0731-nospec"
ARGS=f"-md {DRAFT} --spec-type draft-dspark --spec-draft-n-max 3 --spec-draft-p-min 0 --split-mode tensor -ctk f16 -ctv f16 -ngl 999 --load-mode dio --parallel 2 --ctx-size 196608 --ubatch-size 512 --temp 1.0 --top-p 1.0 --top-k 0 --min-p 0"
orig=open(p).read(); marker="  # Wariant CPU"
add=f'''  "{CAND}":
    cmd: |
      {NEW} --port ${{PORT}} --jinja --agent -fa on
      -m {GGUF}
      {ARGS}
    env:
      - "HIP_VISIBLE_DEVICES=0,1,2,3"
    ttl: 600

'''
open(p,"w").write(orig.replace(marker,add+marker,1)); time.sleep(4)
def call(body,t=900):
    r=urllib.request.Request("http://localhost:8080/v1/chat/completions",data=json.dumps(body).encode(),headers={"Content-Type":"application/json"})
    return json.load(urllib.request.urlopen(r,timeout=t))
def free():
    o=subprocess.run("rocm-smi --showmeminfo vram",shell=True,capture_output=True,text=True).stdout.splitlines()
    u=[int(l.split()[-1]) for l in o if "Total Used" in l][:4]; t=[int(l.split()[-1]) for l in o if "Total Memory" in l][:4]
    return [round((a-b)/1e9,2) for b,a in zip(u,t)]
PROMPTS=["Translate to English, output only the translation: Kwantyzacja zmniejsza liczbę bajtów czytanych w każdym kroku generowania, dlatego model działa szybciej, a jakość spada nieznacznie.",
 "Write a Python function is_prime(n) with a docstring and two doctests. Code only.",
 "List three differences between TCP and UDP as short bullet points.",
 "What is 17 * 23? Show the calculation briefly."]
def outputs(n):
    res=[]
    for pr in PROMPTS:
        x=call(dict(model=n,max_tokens=250,temperature=0,seed=1,messages=[{"role":"user","content":pr}])); m=x["choices"][0]["message"]
        res.append((m.get("reasoning_content") or "")+"||"+(m.get("content") or ""))
    return res
def prefill(n):
    r=random.Random(7); words="alfa beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon".split()
    long=" ".join(r.choice(words)+str(r.randint(0,999)) for _ in range(2600))+"\n\nHow many words were in the text above? One number only."
    out=[]
    for k in range(2):
        x=call(dict(model=n,max_tokens=4,temperature=0,messages=[{"role":"user","content":f"[run {k}-{n}] "+long}])); out.append((x["timings"]["prompt_n"],round(x["timings"]["prompt_per_second"])))
    return out
CP=["Translate to English, output only the translation: Modele typu Mixture-of-Experts aktywują w każdym kroku tylko część ekspertów, więc o szybkości decyduje przepustowość pamięci.",
 "Write a Python function that parses an nginx access log line with a regex and returns a dict. Include type hints. Code only.",
 "You are a coding agent. Explain step by step how you would find and fix a failing unit test, then list the shell commands.",
 "Summarize trade-offs between layer-split and tensor-split multi-GPU inference for a MoE model, as bullets."]
def conc(n):
    rows=[]
    for N in (1,2,4):
        res=[]
        def one(i):
            x=call(dict(model=n,stream=False,temperature=0.2,max_tokens=300,seed=7+i,messages=[{"role":"user","content":CP[i%4]}])); tm=x["timings"]; res.append((tm["predicted_n"],tm["predicted_per_second"]))
        ths=[threading.Thread(target=one,args=(i,)) for i in range(N)]; t0=time.time(); [t.start() for t in ths]; [t.join() for t in ths]; w=time.time()-t0
        rows.append((N,round(statistics.mean(r[1] for r in res),1),round(sum(r[0] for r in res)/w,1)))
    return rows
try:
    call(dict(model=CAND,max_tokens=2,messages=[{"role":"user","content":"hi"}]))
    print("candidate loaded; VRAM free",free(),flush=True)
    pf=prefill(CAND); print("PREFILL candidate (tokens, tok/s):",pf,flush=True)
    cc=conc(CAND); print("CONC candidate (N, per-stream tok/s, aggregate tok/s):",cc,flush=True)
    oc=outputs(CAND); print("VRAM free after use:",free(),flush=True)
    call(dict(model=BASE,max_tokens=2,messages=[{"role":"user","content":"hi"}]))
    ob=outputs(BASE); same=[a==b for a,b in zip(oc,ob)]
    print("IDENTICAL to nospec at temp 0:",same,flush=True)
    for i,(a,b) in enumerate(zip(oc,ob)):
        if a!=b:
            k=next((j for j,(c,d) in enumerate(zip(a,b)) if c!=d),min(len(a),len(b))); print(f"  prompt {i}: first diff at char {k}/{len(a)} | cand: {a[max(0,k-15):k+40]!r} | nospec: {b[max(0,k-15):k+40]!r}",flush=True)
    print("ANSWERS cand (final content):",[o.split('||')[-1][:100] for o in oc],flush=True)
finally:
    open(p,"w").write(orig); print("config restored",flush=True)
