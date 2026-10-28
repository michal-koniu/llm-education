# Tools

> **Where the scripts are.** To avoid two diverging copies, the scripts live in one place:
> [`pl/przyspieszanie-generowania/narzedzia/`](../../../pl/przyspieszanie-generowania/narzedzia/). Their flags and commands are in English, but most docstrings, comments and
> console messages are in Polish. The two benchmark scripts (`bench_spec.py`, `bench_conc.py`) are also published, in English, as
> [`server-bench/`](https://github.com/michal-koniu/local-llm-perf-bench/tree/main/server-bench) in `local-llm-perf-bench`. Where the guides say `tools/…`, read that directory.


Scripts I used to deploy what's described in [02-DEEPSEEK-DEPLOYMENT.md](../02-DEEPSEEK-DEPLOYMENT.md). All of them ran on the reference rig (4× Radeon AI PRO R9700,
llama.cpp + `llama-swap`); these are **templates**, not a finished product — adjust the paths before using them.

**Setting paths.** Run the scripts from their real location (from the repository root):

```bash
cd pl/przyspieszanie-generowania/narzedzia
```

Paths in the scripts are relative to your home directory (`~`, `$HOME`). `gguf-inspect.py` finds `gguf-py` in `~/llama.cpp`, or in the
directory given by the `LLAMA_CPP` variable. The model, draft and `llama.cpp` build paths at the top of `gate-test.py`, `try-entries.py`,
`vram-try.py`, `build-llama-cpp.sh` and `convert-draft-from-hf.sh` are the reference rig's — edit them, together with where `llama-swap`/`config.yaml` lives.

The scripts assume: `llama-swap` on `localhost:8080` (the `LLAMA_SWAP_URL` variable for `dschat.py`), `llama.cpp` in `~/llama.cpp`, models in `~/models/`, the Python environment
for the converter in `~/spec-dspark/venv` (see [02, section 2](../02-DEEPSEEK-DEPLOYMENT.md)).

| Script | Purpose | Example |
|---|---|---|
| `gguf-inspect.py` | whether the GGUF has an MTP/NextN head; what the file is (model or draft); reads only headers, so it works in seconds | `~/spec-dspark/venv/bin/python gguf-inspect.py model-00001-of-0000N.gguf` |
| `find-drafts.sh` | searches Hugging Face for ready-made drafts (MTP, EAGLE-3, DFlash, DSpark, "speculator") for a given model | `./find-drafts.sh Qwen3-30B-A3B` |
| `convert-draft-from-hf.sh` | template for converting a draft from an HF checkpoint to GGUF (here: DeepSeek's DSpark, `--remote` downloads only the needed files) | edit the repo name and the flag |
| `bench_spec.py` | **single-stream speed**: 4 task types × temp. 0 and 1.0; tok/s and acceptance from server counters | `BENCH_REPS=2 python3 bench_spec.py NAME result.json` |
| `bench_conc.py` | 1, 2 and 4 agents at once: tok/s per stream and total | `python3 bench_conc.py NAME result.json` |
| `try-entries.py` | appends **temporary** entries to `config.yaml`, loads each one, runs `bench_spec.py`, measures free VRAM, restores the config at the end | edit the `E` dictionary or the `ENTRIES` variable |
| `vram-try.py` | as above, but only loading and measuring free VRAM for many memory variants (ubatch, context, slots) | edit the `V` dictionary |
| `gate-test.py` | **gate before deployment**: prefill, 1/2/4 agents, free VRAM after use, consistency with the model without a draft | edit the constants at the top |
| `build-llama-cpp.sh` | builds llama.cpp in a **separate directory** with a full SHA pin | edit the SHA |
| `dschat.py` | terminal chat with a tok/s counter ([04](../04-USING-UI-CLI-OPENCLAW.md)) | `python3 dschat.py "question"` |
| `translate_doc.py` | translates a Markdown document with a local model, section by section | `python3 translate_doc.py source.md result.md deepseek` |
| `verify_translation.py` | mechanical translation verification: code blocks, URLs, flags, numbers, headings, tables, untranslated sentences | `python3 verify_translation.py en.md pl.md` |

**Notes.** `try-entries.py`, `vram-try.py` and `gate-test.py` **modify `config.yaml`** (they restore it in a `finally` block) — and every config write unloads the loaded model in `llama-swap`.
Don't run them while someone is using the model or during a long test. The `bench_*` scripts only send requests.
