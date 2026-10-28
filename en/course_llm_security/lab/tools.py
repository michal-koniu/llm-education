"""Sieve's tools: OpenAI function schemas + implementations.

The tools are deliberately powerful (that is what makes the lab attackable), but
each one has a LAB SAFETY RAIL that keeps every effect inside this directory or
on 127.0.0.1. The rails are not "defences" you study - they are there so that a
hijacked model can never touch your real files, e-mail or the internet.
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter

from . import paths

DEFAULT_TOOLS = frozenset({"search_docs", "read_file", "fetch_url", "send_email", "remember"})
ALL_TOOLS = DEFAULT_TOOLS | {"run_python"}

# Tools whose RESULT is untrusted content (it can carry someone else's instructions).
UNTRUSTED_TOOLS = frozenset({"search_docs", "fetch_url"})

# Lab safety rail: fetch_url may only reach the fixture web and the attacker server.
FETCH_ALLOWED = {("127.0.0.1", paths.WEB_PORT), ("127.0.0.1", paths.ATTACKER_PORT),
                 ("localhost", paths.WEB_PORT), ("localhost", paths.ATTACKER_PORT)}

MAX_RESULT = 6000


def _fn(name, description, **props):
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {k: {"type": "string", "description": v} for k, v in props.items()},
                "required": list(props),
            },
        },
    }


TOOL_SCHEMAS = {
    "search_docs": _fn("search_docs", "Search the household knowledge base (recipes, cleaning guides, "
                       "notes). Returns the best matching documents.",
                       query="keywords to search for"),
    "read_file": _fn("read_file", "Read one of the user's personal files, e.g. 'private_notes.txt'. "
                     "Use '.' to list the files.",
                     path="file name inside the user's files folder"),
    "fetch_url": _fn("fetch_url", "Download a web page and return its content.",
                     url="the http:// URL to fetch"),
    "send_email": _fn("send_email", "Send an e-mail on the user's behalf.",
                      to="recipient address", subject="subject line", body="message body"),
    "remember": _fn("remember", "Save a note to long-term memory. Notes are shown to you in "
                    "every future conversation.",
                    note="the fact or preference to remember"),
    "run_python": _fn("run_python", "Run a short Python snippet and return its output.",
                      code="Python source code"),
}


def schemas(names) -> list:
    return [TOOL_SCHEMAS[n] for n in sorted(names) if n in TOOL_SCHEMAS]


def _clip(text: str) -> str:
    return text if len(text) <= MAX_RESULT else text[:MAX_RESULT] + "\n[... truncated]"


def _append_jsonl(path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------- tools

_WORD = re.compile(r"[a-z0-9]+")


def search_docs(query: str) -> str:
    """BM25-ish keyword search over lab/data/docs/*.md. Returns the top 3 docs."""
    docs = {p.name: p.read_text(encoding="utf-8", errors="replace")
            for p in sorted(paths.DOCS.glob("*.md"))}
    if not docs:
        return "no documents"
    toks = {n: _WORD.findall(t.lower()) for n, t in docs.items()}
    avg = sum(len(t) for t in toks.values()) / len(toks)
    df = Counter(w for t in toks.values() for w in set(t))
    q = _WORD.findall(str(query).lower())
    k1, b, n = 1.5, 0.75, len(docs)
    scores = {}
    for name, t in toks.items():
        tf = Counter(t)
        s = 0.0
        for w in q:
            if tf[w]:
                idf = math.log(1 + (n - df[w] + 0.5) / (df[w] + 0.5))
                s += idf * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * len(t) / avg))
        if s > 0:
            scores[name] = s
    best = sorted(scores, key=scores.get, reverse=True)[:3]
    if not best:
        return "no results"
    return _clip("\n\n".join(f"=== {name} ===\n{docs[name][:2000]}" for name in best))


def _inside_files(path: str):
    rel = str(path).strip().lstrip("/")
    for prefix in ("lab/data/files/", "data/files/", "files/"):
        if rel.startswith(prefix):
            rel = rel[len(prefix):]
    target = (paths.FILES / rel).resolve()
    root = paths.FILES.resolve()
    if target != root and root not in target.parents:
        return None
    return target


def read_file(path: str) -> str:
    """Read a file. Rail: only inside lab/data/files/."""
    target = _inside_files(path or ".")
    if target is None:
        return "error: access denied (only the user's files folder is readable)"
    if target.is_dir():
        return "files: " + ", ".join(sorted(p.name for p in target.iterdir()))
    if not target.exists():
        return f"error: no such file: {path}"
    return _clip(target.read_text(encoding="utf-8", errors="replace"))


def fetch_url(url: str) -> str:
    """HTTP GET. Rail: only 127.0.0.1:8765 (fixture web) and :8766 (attacker server)."""
    u = urllib.parse.urlsplit(str(url).strip())
    if u.scheme != "http" or (u.hostname, u.port or 80) not in FETCH_ALLOWED:
        return ("error: the lab only allows http://127.0.0.1:8765/ (fixture web) and "
                "http://127.0.0.1:8766/ - nothing else")
    try:
        with urllib.request.urlopen(str(url).strip(), timeout=10) as r:
            return _clip(r.read(200_000).decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        return f"error: HTTP {e.code}"
    except Exception as e:  # connection refused etc.
        return f"error: {e}"


def send_email(to: str, subject: str = "", body: str = "") -> str:
    """Never sends anything. Rail: appends to lab/runtime/outbox.jsonl."""
    _append_jsonl(paths.OUTBOX, {"ts": time.time(), "to": str(to),
                                 "subject": str(subject), "body": str(body)})
    return f"e-mail to {to} queued"


def remember(note: str) -> str:
    """Appends to lab/runtime/memory.jsonl; later sessions see it in the system prompt."""
    _append_jsonl(paths.MEMORY, {"ts": time.time(), "note": str(note), "source": "agent"})
    return "saved to memory"


def run_python(code: str) -> str:
    """OFF by default. Rail: isolated interpreter, cwd lab/runtime/, 10 s timeout,
    empty environment. This is NOT a sandbox - see course 2 part 10 for one."""
    paths.RUNTIME.mkdir(parents=True, exist_ok=True)
    try:
        p = subprocess.run([sys.executable, "-I", "-c", str(code)], cwd=paths.RUNTIME,
                           capture_output=True, text=True, timeout=10, env={})
    except subprocess.TimeoutExpired:
        return "error: timeout"
    return _clip((p.stdout + p.stderr).strip() or f"(exit {p.returncode}, no output)")


IMPLEMENTATIONS = {
    "search_docs": search_docs, "read_file": read_file, "fetch_url": fetch_url,
    "send_email": send_email, "remember": remember, "run_python": run_python,
}


def run_tool(name: str, args: dict) -> str:
    fn = IMPLEMENTATIONS.get(name)
    if fn is None:
        return f"error: unknown tool {name!r}"
    try:
        return fn(**args)
    except TypeError as e:  # wrong/missing arguments from the model
        return f"error: bad arguments for {name}: {e}"
