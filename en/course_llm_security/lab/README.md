# The LLM security lab

A deliberately vulnerable assistant (**Sieve**) with tools, a fake internet, a fake
attacker server and a naive chat UI — plus a harness that measures how often attacks
succeed. Part 02 of the course explains every file:
[`../02-THE-LAB.md`](../02-THE-LAB.md) (Polish: [`../../../pl/kurs_bezpieczenstwo_llm/02-LABORATORIUM.md`](../../../pl/kurs_bezpieczenstwo_llm/02-LABORATORIUM.md)).

**Safety:** everything binds to `127.0.0.1`; e-mail goes to a file; `fetch_url` can reach only
the two lab servers; success is shown with random canary strings, never real secrets.
Attack only this lab and machines you own.

Python 3.11+, standard library only.

```bash
# copy the lab out of the repo; run every command from the directory that CONTAINS lab/
mkdir -p ~/llm-sec-lab && cp -r lab ~/llm-sec-lab/ && cd ~/llm-sec-lab

LLM_BASE_URL=mock python3 -m unittest discover lab/tests   # self-tests, no GPU needed
python3 -m lab.setup_lab                                   # reset: new canaries, fixtures
python3 -m lab.servers                                     # web :8765, attacker :8766, UI :8760 (own terminal)

# point at your local OpenAI-compatible server (llama-server started with --jinja)
export LLM_BASE_URL=http://127.0.0.1:8080/v1               # default
python3 -m lab.harness --cases lab/cases/part02.jsonl --defenses none --k 5
python3 -m lab.harness --cases lab/cases/part02.jsonl --defenses none --k 10 --temperature 0.7
python3 -m lab.harness --scoreboard
```

| File | What it is |
| :-- | :-- |
| `llm.py` | `chat()` for any OpenAI-compatible endpoint; `LLM_BASE_URL=mock` = gullible mock (`>>> CALL`, `>>> SAY`) |
| `target.py` | `Sieve(defenses, tools, system_prompt, max_steps).ask(text) -> Trace` |
| `tools.py` | `search_docs`, `read_file`, `fetch_url`, `send_email`, `remember`, `run_python` (off) |
| `setup_lab.py` | resets `runtime/`, generates canaries, writes `data/` and `web/` |
| `servers.py`, `ui.py` | fixture web, attacker logger, unsafe chat UI |
| `defenses/` | `Defense`/`Verdict` hooks and the `CONFIGS` registry |
| `goals.py` | success checks (`leak_*`, `exfil_http`, `email_external`, `memory_write`, ...) |
| `harness.py` | k repetitions, ASR with Wilson interval, `runtime/scoreboard.csv` |
| `cases/` | attack cases, one JSON per line |

`runtime/`, `data/` and `web/` are generated — do not edit them by hand; `setup_lab` overwrites
them (it keeps `runtime/scoreboard.csv` and `runtime/runs/`). The self-tests reset the lab too.
If ports 8765/8766/8760 are taken, move the lab with `LAB_WEB_PORT`, `LAB_ATTACKER_PORT`, `LAB_UI_PORT`
(export them in every lab terminal); the harness rewrites the default ports in the cases to match.
