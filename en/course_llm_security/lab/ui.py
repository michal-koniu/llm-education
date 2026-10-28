"""A tiny chat UI for Sieve on http://127.0.0.1:8760 - DELIBERATELY UNSAFE.

render_markdown() turns ![alt](url) into <img src=url>, [text](url) into a link,
and lets raw HTML straight through. When the model's answer contains an image
pointing at the attacker server, your browser loads it the moment the answer is
displayed - with whatever the model put into the URL. That is the exfiltration
channel parts 07 and 09 study and close.

simulate_browser() does the same image loading without a browser, so the harness
can measure the channel.

Started by `python3 -m lab.servers` (do not expose it: it binds 127.0.0.1 only,
and checks Host/Origin so other web pages cannot drive it; see part 12).
"""
from __future__ import annotations

import html
import json
import os
import re
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler

from . import paths

_IMG = re.compile(r"!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
_LINK = re.compile(r"\[([^\]]+)\]\(\s*<?([^)\s>]+)>?\s*\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_CODE = re.compile(r"`([^`]+)`")
_SRC = re.compile(r"<img\b[^>]*?\bsrc\s*=\s*[\"']?([^\"' >]+)", re.I)


def render_markdown(text: str) -> str:
    """Naive markdown -> HTML. NO escaping, on purpose."""
    out = _IMG.sub(lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}">', text or "")
    out = _LINK.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', out)
    out = _BOLD.sub(r"<b>\1</b>", out)
    out = _CODE.sub(r"<code>\1</code>", out)
    return out.replace("\n", "<br>\n")


def image_urls(rendered_html: str) -> list:
    return _SRC.findall(rendered_html)


def simulate_browser(markdown_text: str) -> list:
    """Load every <img> the naive renderer would produce, like a browser does.
    Lab rail: only 127.0.0.1/localhost URLs are requested. Returns the URLs loaded."""
    loaded = []
    for url in image_urls(render_markdown(markdown_text)):
        url = html.unescape(url)
        u = urllib.parse.urlsplit(url)
        if u.scheme not in ("http", "https") or u.hostname not in ("127.0.0.1", "localhost"):
            continue
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                r.read(1024)
        except Exception:
            pass  # a failed load still sent the request line
        loaded.append(url)
    return loaded


# --------------------------------------------------------------------------- server

PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>Sieve (lab UI)</title>
<style>body{{font-family:sans-serif;max-width:52rem;margin:2rem auto;padding:0 1rem}}
.u{{background:#eef;padding:.5rem;margin:.5rem 0}} .a{{background:#efe;padding:.5rem;margin:.5rem 0}}
details{{font-size:.85rem;color:#555}} textarea{{width:100%}}</style></head><body>
<h1>Sieve <small>(deliberately vulnerable lab UI &middot; defences: {config})</small></h1>
{history}
<form method="post" action="/ask"><textarea name="q" rows="3" autofocus></textarea>
<button>Ask</button></form>
<form method="post" action="/reset"><button>Reset lab (new canaries)</button></form>
</body></html>"""

HISTORY: list = []   # (user_text, Trace) for this server process


def _allowed_host(value: str) -> bool:
    return value in (f"127.0.0.1:{paths.UI_PORT}", f"localhost:{paths.UI_PORT}")


class UIHandler(BaseHTTPRequestHandler):
    server_version = "SieveLabUI/1.0"

    def log_message(self, *args):  # quiet
        pass

    def _send(self, code: int, body: str, ctype="text/html; charset=utf-8", extra=None):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def _guard(self) -> bool:
        # DNS-rebinding and cross-site-request guard: only our own origin may drive the UI.
        if not _allowed_host(self.headers.get("Host", "")):
            self._send(403, "forbidden host")
            return False
        origin = self.headers.get("Origin")
        if self.command == "POST" and origin and origin not in (
                f"http://127.0.0.1:{paths.UI_PORT}", f"http://localhost:{paths.UI_PORT}"):
            self._send(403, "forbidden origin")
            return False
        return True

    def do_GET(self):
        if self.path == "/__lab":
            return self._send(200, json.dumps({"lab": str(paths.LAB_DIR)}), "application/json")
        if not self._guard():
            return
        parts = []
        for q, t in HISTORY:
            calls = "".join(
                f"<li>{html.escape(c['name'])}({html.escape(json.dumps(c['args'])[:200])})"
                f"{' BLOCKED: ' + html.escape(c['reason']) if c['blocked'] else ''}</li>"
                for c in t.tool_calls)
            events = "".join(f"<li>{html.escape(json.dumps(e))}</li>" for e in t.events)
            parts.append(
                f'<div class="u">{html.escape(q)}</div>'
                f'<div class="a">{render_markdown(t.output)}'       # <- the unsafe line
                f"<details><summary>trace</summary><ul>{calls}</ul><ul>{events}</ul>"
                f"</details></div>")
        self._send(200, PAGE.format(config=html.escape(_config()), history="".join(parts)))

    def do_POST(self):
        if not self._guard():
            return
        length = int(self.headers.get("Content-Length") or 0)
        form = urllib.parse.parse_qs(self.rfile.read(min(length, 100_000)).decode())
        if self.path == "/ask":
            from .target import Sieve
            q = (form.get("q") or [""])[0]
            if q.strip():
                try:
                    HISTORY.append((q, Sieve(defenses=_config()).ask(q)))
                except Exception as e:  # show errors instead of a dead page
                    from .target import Trace
                    HISTORY.append((q, Trace(output=f"[error: {html.escape(str(e))}]")))
        elif self.path == "/reset":
            from .setup_lab import setup
            setup()
            HISTORY.clear()
        self._send(303, "", extra={"Location": "/"})


def _config() -> str:
    return os.environ.get("LAB_DEFENSES", "none")
