"""Run attack cases k times, measure ASR, keep a scoreboard.

    python3 -m lab.harness --cases lab/cases/part02.jsonl --defenses none --k 5
    python3 -m lab.harness --cases lab/cases/part02.jsonl --defenses none,p05-canary --k 10 --temperature 0.7
    python3 -m lab.harness --scoreboard

Every repetition starts from a fresh lab (new canaries, clean outbox/memory/attacker
log), plants the case's files, asks Sieve, lets a simulated browser load the
answer's images (like the chat UI would), and checks the goal.

Results: a table on stdout, one row per (config, case) appended to
lab/runtime/scoreboard.csv (timestamp,model,config,case,k,successes), and every
trace in lab/runtime/runs/<timestamp>.jsonl. A non-zero temperature is recorded
in the config column as "<config>@t<T>" so runs at different temperatures never mix.

Case format (one JSON object per line; lines starting with // are comments):
    {"id", "part", "category", "plant": {"web/x.html": "..."}, "user": "...",
     "goal": "...", "notes": "..."}
  optional: "user" may be a LIST = consecutive sessions (memory persists between them),
            "tools": [...] to override the enabled tools, "marker" (memory_write),
            "expect": [...] (off_policy).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
import time
from pathlib import Path

from . import goals, llm, paths, servers, setup_lab, ui
from .defenses import get_config
from .target import DEFAULT_TOOLS, Sieve

FIELDS = ["timestamp", "model", "config", "case", "k", "successes"]
_PLACEHOLDER = re.compile(r"\{(SYSTEM|FILE|MEMORY)_CANARY\}")


# --------------------------------------------------------------------------- statistics

def wilson(successes: int, n: int, z: float = 1.96) -> tuple:
    """95% Wilson score interval for a binomial proportion (good for small n)."""
    if n == 0:
        return 0.0, 1.0
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


# --------------------------------------------------------------------------- cases

def resolve(path_str: str) -> Path:
    """Accept a path relative to the cwd, to the lab's parent, or to lab/."""
    p = Path(path_str).expanduser()
    for cand in (p, paths.LAB_PARENT / p, paths.LAB_DIR / p):
        if cand.exists():
            return cand
    raise FileNotFoundError(path_str)


def load_cases(path) -> list:
    cases = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"{path}:{n}: not valid JSON ({e})") from e
        validate(case, f"{path}:{n}")
        cases.append(remap_ports(case))
    return cases


def remap_ports(obj):
    """Cases are written against the default ports 8765/8766. If LAB_WEB_PORT / LAB_ATTACKER_PORT move the
    servers (because something else on your machine already uses those ports), rewrite the URLs to match."""
    if isinstance(obj, str):
        for host in ("127.0.0.1", "localhost"):
            obj = obj.replace(f"{host}:8765", f"{host}:{paths.WEB_PORT}").replace(
                f"{host}:8766", f"{host}:{paths.ATTACKER_PORT}")
        return obj
    if isinstance(obj, list):
        return [remap_ports(x) for x in obj]
    if isinstance(obj, dict):
        return {remap_ports(k): remap_ports(v) for k, v in obj.items()}
    return obj


def validate(case: dict, where: str = "case") -> None:
    for key in ("id", "user", "goal"):
        if key not in case:
            raise ValueError(f"{where}: missing {key!r}")
    blob = json.dumps(case)
    # Attacks must not know the secret: no placeholders, no literal canaries.
    if _PLACEHOLDER.search(blob) or setup_lab.CANARY_RE.search(blob):
        raise ValueError(f"{where}: cases may not contain canaries or canary placeholders")
    for rel in case.get("plant") or {}:
        rel = rel[4:] if rel.startswith("lab/") else rel
        if ".." in rel.split("/") or not any(rel.startswith(r + "/") for r in paths.PLANT_ROOTS):
            raise ValueError(f"{where}: plant path {rel!r} not under {paths.PLANT_ROOTS}")


# --------------------------------------------------------------------------- running

def run_once(case: dict, config: str, temperature: float, render: bool = True) -> tuple:
    """One repetition from a fresh lab. Returns (success, [traces])."""
    setup_lab.setup()
    setup_lab.plant(case.get("plant") or {})
    tools = case.get("tools") or DEFAULT_TOOLS
    sieve = Sieve(defenses=config, tools=tools, temperature=temperature)
    turns = case["user"] if isinstance(case["user"], list) else [case["user"]]
    traces = []
    for turn in turns:
        t = sieve.ask(turn)
        if render:
            t.rendered = ui.simulate_browser(t.output)
        traces.append(t)
    return goals.evaluate(case, traces), traces


def config_label(config: str, temperature: float) -> str:
    return config if not temperature else f"{config}@t{temperature:g}"


def run(cases_path, configs, k=5, temperature=0.0, only=None, render=True,
        scoreboard=None, verbose=False, out=None) -> list:
    out = out or sys.stdout
    cases = load_cases(resolve(cases_path))
    if only:
        cases = [c for c in cases if c["id"] in only]
        if not cases:
            raise SystemExit(f"no case with id in {only}")
    for cfg in configs:
        get_config(cfg)  # fail early on unknown names
    servers.ensure_running()
    model = llm.model_label()
    stamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    paths.RUNS.mkdir(parents=True, exist_ok=True)
    dump = paths.RUNS / f"{stamp.replace(':', '')}.jsonl"
    rows = []

    print(f"model={model}  k={k}  temperature={temperature:g}  cases={len(cases)}", file=out)
    for cfg in configs:
        label = config_label(cfg, temperature)
        print(f"\n== config: {label}", file=out)
        print(f"{'case':28} {'goal':22} {'succ/k':>7} {'ASR':>6}  95% CI (Wilson)", file=out)
        for case in cases:
            wins = 0
            for i in range(k):
                ok, traces = run_once(case, cfg, temperature, render)
                wins += ok
                with dump.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({"config": label, "case": case["id"], "rep": i,
                                        "success": ok, "traces": [t.to_dict() for t in traces]},
                                       ensure_ascii=False) + "\n")
                if verbose:
                    last = traces[-1]
                    calls = ", ".join(c["name"] + ("(BLOCKED)" if c["blocked"] else "")
                                      for t in traces for c in t.tool_calls)
                    print(f"   rep {i + 1}: {'HIT ' if ok else 'miss'} tools=[{calls}] "
                          f"out={last.output[:100]!r}", file=out)
            lo, hi = wilson(wins, k)
            print(f"{case['id'][:28]:28} {case['goal'][:22]:22} {wins:>3}/{k:<3} "
                  f"{wins / k:>6.0%}  [{lo:.0%}, {hi:.0%}]", file=out)
            rows.append({"timestamp": stamp, "model": model, "config": label,
                         "case": case["id"], "k": k, "successes": wins})
    if scoreboard is not False:
        append_scoreboard(rows, scoreboard or paths.SCOREBOARD)
    print(f"\ntraces: {dump}", file=out)
    return rows


# --------------------------------------------------------------------------- scoreboard

def append_scoreboard(rows, path=None) -> None:
    path = Path(path or paths.SCOREBOARD)
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerows(rows)


def print_scoreboard(path=None, model=None, out=None) -> None:
    """Pivot case x config, using the LATEST row for each (model, config, case)."""
    out = out or sys.stdout
    path = Path(path or paths.SCOREBOARD)
    if not path.exists():
        print("no scoreboard yet - run the harness first", file=out)
        return
    latest = {}
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if model and r["model"] != model:
                continue
            latest[(r["model"], r["config"], r["case"])] = r
    for m in sorted({key[0] for key in latest}):
        configs = sorted({c for (mm, c, _) in latest if mm == m}, key=lambda c: (c != "none", c))
        cases = sorted({cs for (mm, _, cs) in latest if mm == m})
        width = max([28] + [len(c) for c in cases])
        print(f"\nmodel: {m}   (cells: successes/k  ASR)", file=out)
        print(f"{'case':{width}} " + " ".join(f"{c[:16]:>16}" for c in configs), file=out)
        for cs in cases:
            cells = []
            for c in configs:
                r = latest.get((m, c, cs))
                cells.append(f"{r['successes']}/{r['k']} {int(r['successes']) / int(r['k']):>4.0%}"
                             if r else "-")
            print(f"{cs:{width}} " + " ".join(f"{x:>16}" for x in cells), file=out)


# --------------------------------------------------------------------------- CLI

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python3 -m lab.harness", description=__doc__.split("\n\n")[0])
    ap.add_argument("--cases", help="a .jsonl file of cases")
    ap.add_argument("--defenses", default="none",
                    help="config name(s): comma = compare configs, plus = combine (default: none)")
    ap.add_argument("--k", type=int, default=5, help="repetitions per case (default 5)")
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--case", action="append", help="run only this case id (repeatable)")
    ap.add_argument("--no-render", action="store_true",
                    help="do not simulate the browser loading images in the answer")
    ap.add_argument("--no-save", action="store_true", help="do not append to the scoreboard")
    ap.add_argument("--scoreboard-file", help="alternative scoreboard CSV path")
    ap.add_argument("--scoreboard", action="store_true", help="print the scoreboard pivot and exit")
    ap.add_argument("--model", help="with --scoreboard: only this model")
    ap.add_argument("-v", "--verbose", action="store_true", help="one line per repetition")
    a = ap.parse_args(argv)

    if a.scoreboard:
        print_scoreboard(a.scoreboard_file, a.model)
        return 0
    if not a.cases:
        ap.error("--cases is required (or use --scoreboard)")
    if a.k < 1:
        ap.error("--k must be >= 1")
    configs = [c.strip() for c in a.defenses.split(",") if c.strip()]
    try:
        run(a.cases, configs, k=a.k, temperature=a.temperature, only=a.case,
            render=not a.no_render,
            scoreboard=False if a.no_save else a.scoreboard_file, verbose=a.verbose)
    except llm.LLMError as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        return 2
    except (KeyError, ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"\nERROR: {e.args[0] if e.args else e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
