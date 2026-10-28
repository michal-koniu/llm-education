"""One function between the lab and a model: chat().

Talks to any OpenAI-compatible /v1/chat/completions endpoint (llama-server,
vLLM, Ollama's /v1, ...). With LLM_BASE_URL=mock it uses a deterministic,
gullible mock instead, so every self-test runs without a GPU.

Environment:
    LLM_BASE_URL   default http://127.0.0.1:8080/v1   ("mock" = the mock backend)
    LLM_MODEL      default "local"
    LLM_API_KEY    optional; sent as "Authorization: Bearer ..."
    LLM_TIMEOUT    optional; seconds per request, default 300
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from collections import Counter

DEFAULT_BASE_URL = "http://127.0.0.1:8080/v1"


class LLMError(RuntimeError):
    """The model endpoint could not be reached or returned something unusable."""


def base_url() -> str:
    return os.environ.get("LLM_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def is_mock() -> bool:
    return base_url() == "mock"


def chat(messages, tools=None, temperature=0.0, max_tokens=1024) -> dict:
    """Send a conversation, get back ONE assistant message (OpenAI format).

    Returns {"role": "assistant", "content": str, "tool_calls": [...]}.
    "tool_calls" is present only when the model asked for tools; each entry is
    {"id", "type": "function", "function": {"name", "arguments": <JSON string>}}.
    """
    if is_mock():
        return _mock_chat(messages, tools)
    return _http_chat(messages, tools, temperature, max_tokens)


def model_label() -> str:
    """A name for the scoreboard: the mock, LLM_MODEL, or what the server reports."""
    if is_mock():
        return "mock"
    name = os.environ.get("LLM_MODEL", "local")
    if name != "local":
        return name
    try:  # llama-server answers /v1/models with the loaded GGUF's name
        req = urllib.request.Request(base_url() + "/models", headers=_headers())
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.load(r).get("data") or []
        if data and data[0].get("id"):
            return os.path.basename(str(data[0]["id"]))
    except Exception:
        pass
    return name


# --------------------------------------------------------------------------- HTTP

def _headers() -> dict:
    h = {"Content-Type": "application/json"}
    key = os.environ.get("LLM_API_KEY")
    if key:
        h["Authorization"] = f"Bearer {key}"
    return h


def _http_chat(messages, tools, temperature, max_tokens) -> dict:
    body = {
        "model": os.environ.get("LLM_MODEL", "local"),
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if tools:
        body["tools"] = tools
    req = urllib.request.Request(
        base_url() + "/chat/completions",
        data=json.dumps(body).encode(),
        headers=_headers(),
        method="POST",
    )
    timeout = float(os.environ.get("LLM_TIMEOUT", "300"))
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        raise LLMError(f"HTTP {e.code} from {base_url()}: {detail}") from e
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        raise LLMError(
            f"cannot reach the model at {base_url()} ({e}). Start llama-server "
            f"(see part 02, section 6) or use LLM_BASE_URL=mock") from e
    try:
        choice = data["choices"][0]
        msg = choice["message"]
    except (KeyError, IndexError, TypeError) as e:
        raise LLMError(f"unexpected response: {str(data)[:300]}") from e
    # Reasoning models think before they answer, and the thinking counts against max_tokens.
    # A small budget (a one-word judge, a short rewrite) can be used up before any visible
    # text appears: the reply comes back empty with finish_reason "length". Retry once with
    # room to think, instead of silently treating "" as the model's answer.
    if (choice.get("finish_reason") == "length" and not msg.get("content")
            and not msg.get("tool_calls") and max_tokens < 4096):
        return _http_chat(messages, tools, temperature, max(4096, max_tokens * 8))
    return _normalise(msg)


def _normalise(msg: dict) -> dict:
    out = {"role": "assistant", "content": msg.get("content") or ""}
    calls = []
    for i, tc in enumerate(msg.get("tool_calls") or []):
        fn = tc.get("function") or {}
        args = fn.get("arguments", "{}")
        if not isinstance(args, str):
            args = json.dumps(args)
        calls.append({
            "id": tc.get("id") or f"call_{i}",
            "type": "function",
            "function": {"name": fn.get("name", ""), "arguments": args},
        })
    if calls:
        out["tool_calls"] = calls
    return out


# --------------------------------------------------------------------------- mock

_CALL = re.compile(r"^\s*>>> CALL\s+([A-Za-z_][\w]*)\s*(.*?)\s*$")
_SAY = re.compile(r"^\s*>>> SAY\s?(.*?)\s*$")


def _text_of(message) -> str:
    content = message.get("content")
    if isinstance(content, list):  # OpenAI "content parts"
        return "\n".join(p.get("text", "") for p in content if isinstance(p, dict))
    return content or ""


def _canon(name: str, args) -> tuple:
    return name, json.dumps(args, sort_keys=True)


def _mock_chat(messages, tools) -> dict:
    """The gullible mock. It obeys any '>>> CALL' / '>>> SAY' line, wherever it
    appears: system prompt, user message, memory, tool results. That is exactly
    what a fully injectable model would do, minus the language.

    1. Each '>>> CALL <tool> <json>' line is emitted once, in order of appearance
       (a call already present in the history is not repeated). Ignored if no
       tools were offered.
    2. Then the last '>>> SAY <text>' line found becomes the answer.
    3. Otherwise: a short summary of the last user message.
    """
    directives, says = [], []
    for m in messages:
        for line in _text_of(m).splitlines():
            c = _CALL.match(line)
            if c:
                try:
                    args = json.loads(c.group(2)) if c.group(2) else {}
                except json.JSONDecodeError:
                    args = {}
                if not isinstance(args, dict):
                    args = {}
                directives.append((c.group(1), args))
                continue
            s = _SAY.match(line)
            if s:
                says.append(s.group(1))

    if tools:
        done = Counter()
        n_calls = 0
        for m in messages:
            for tc in m.get("tool_calls") or []:
                n_calls += 1
                fn = tc.get("function") or {}
                try:
                    a = json.loads(fn.get("arguments") or "{}")
                except json.JSONDecodeError:
                    a = {}
                done[_canon(fn.get("name", ""), a)] += 1
        for name, args in directives:
            key = _canon(name, args)
            if done[key] > 0:
                done[key] -= 1
                continue
            return {
                "role": "assistant",
                "content": "",
                "tool_calls": [{
                    "id": f"mock_{n_calls}",
                    "type": "function",
                    "function": {"name": name, "arguments": json.dumps(args)},
                }],
            }

    if says:
        return {"role": "assistant", "content": says[-1]}

    last_user = next((_text_of(m) for m in reversed(messages)
                      if m.get("role") == "user"), "")
    gist = " ".join(last_user.split())[:80]
    return {"role": "assistant", "content": f"(mock) You asked about: {gist}"}
