#!/usr/bin/env python3
"""dschat.py -- terminalowy czat z modelem przez llama-swap (API zgodne z OpenAI). Bez zaleznosci (sama biblioteka standardowa).

  python3 dschat.py                       # interaktywnie, model "deepseek"
  python3 dschat.py "Wyjasnij MoE"        # jedno pytanie i koniec
  echo "Streszcz: ..." | python3 dschat.py -     # prompt z potoku
  python3 dschat.py --show-thinking       # pokaz tez "myslenie" modelu (domyslnie schowane, ale liczone w tok/s)
  python3 dschat.py --no-think "..."      # wylacz myslenie (szybciej, krocej; dla prostych zadan)

Adres serwera: zmienna LLAMA_SWAP_URL (domyslnie http://localhost:8080) -- z innego komputera ustaw adres maszyny z GPU.
Komendy w czacie:  /reset (czysta rozmowa)  /think (przelacz pokazywanie myslenia)  /exit
Po kazdej odpowiedzi: tok/s (z liczników serwera: generowanie), akceptacja draftu, czas do pierwszego tokenu.
"""
import argparse, json, os, sys, time, urllib.request

URL = os.environ.get("LLAMA_SWAP_URL", "http://localhost:8080").rstrip("/") + "/v1/chat/completions"
DIM, RESET = "\033[2m", "\033[0m"

def stream_chat(messages, model, temperature, max_tokens, think, show_thinking):
    body = dict(model=model, messages=messages, stream=True, temperature=temperature, max_tokens=max_tokens,
                stream_options={"include_usage": True})
    if not think:
        body["chat_template_kwargs"] = {"enable_thinking": False}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time(); first = None; answer = []; in_think = False; timings = {}
    with urllib.request.urlopen(req, timeout=3600) as r:
        for raw in r:
            line = raw.decode("utf-8", "ignore").strip()
            if not line.startswith("data:") or line.endswith("[DONE]"):
                continue
            d = json.loads(line[5:])
            if d.get("timings"): timings = d["timings"]
            for ch in d.get("choices", []):
                delta = ch.get("delta", {})
                rc, c = delta.get("reasoning_content"), delta.get("content")
                if rc or c:
                    first = first or time.time()
                if rc and show_thinking:
                    if not in_think: sys.stdout.write(DIM + "[myslenie] "); in_think = True
                    sys.stdout.write(rc); sys.stdout.flush()
                if c:
                    if in_think: sys.stdout.write(RESET + "\n\n"); in_think = False
                    sys.stdout.write(c); sys.stdout.flush(); answer.append(c)
    if in_think: sys.stdout.write(RESET)
    print()
    tps = timings.get("predicted_per_second"); n = timings.get("predicted_n")
    acc = (f", draft {timings.get('draft_n_accepted')}/{timings.get('draft_n')}" if timings.get("draft_n") else "")
    ttft = f"{first - t0:.1f}s do 1. tokenu" if first else "brak tokenow"
    print(f"{DIM}[{n} tokenow, {tps:.1f} tok/s{acc}, {ttft}]{RESET}" if tps else f"{DIM}[{ttft}]{RESET}")
    return "".join(answer)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompt", nargs="?", help="pytanie (albo '-' = czytaj ze stdin); bez tego: tryb interaktywny")
    ap.add_argument("--model", default="deepseek"); ap.add_argument("--temperature", type=float, default=0.3)
    ap.add_argument("--max-tokens", type=int, default=4096); ap.add_argument("--no-think", action="store_true")
    ap.add_argument("--show-thinking", action="store_true"); ap.add_argument("--system", default=None)
    a = ap.parse_args()
    base = [{"role": "system", "content": a.system}] if a.system else []
    show = a.show_thinking
    if a.prompt:
        text = sys.stdin.read() if a.prompt == "-" else a.prompt
        stream_chat(base + [{"role": "user", "content": text}], a.model, a.temperature, a.max_tokens, not a.no_think, show)
        return
    msgs = list(base)
    print(f"{DIM}Czat z '{a.model}' przez {URL}  (/reset /think /exit){RESET}")
    while True:
        try: text = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt): print(); break
        if not text: continue
        if text == "/exit": break
        if text == "/reset": msgs = list(base); print("(rozmowa wyczyszczona)"); continue
        if text == "/think": show = not show; print(f"(pokazywanie myslenia: {'tak' if show else 'nie'})"); continue
        msgs.append({"role": "user", "content": text})
        msgs.append({"role": "assistant", "content": stream_chat(msgs, a.model, a.temperature, a.max_tokens, not a.no_think, show)})

if __name__ == "__main__":
    main()
