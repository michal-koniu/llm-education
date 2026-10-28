"""The lab's three local servers, all on 127.0.0.1 only.

    python3 -m lab.servers

  :8765  fixture web     serves lab/web/  (the "internet" Sieve can fetch; untrusted)
  :8766  attacker        logs every request line to lab/runtime/attacker.log, answers 1x1 GIF
  :8760  chat UI         lab/ui.py - naive markdown rendering (the exfil channel)

The harness and the tests call ensure_running(), which starts the web and attacker
servers in background threads if nothing is listening yet.
"""
from __future__ import annotations

import base64
import functools
import json
import socket
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, ThreadingHTTPServer

from . import paths

GIF = base64.b64decode("R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")
_LOG_LOCK = threading.Lock()


def _lab_info() -> bytes:
    return json.dumps({"lab": str(paths.LAB_DIR)}).encode()


class WebHandler(SimpleHTTPRequestHandler):
    """Static files from lab/web/ (read at request time, so plants are live)."""

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(paths.WEB), **kw)

    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path == "/__lab":
            body = _lab_info()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


class AttackerHandler(BaseHTTPRequestHandler):
    """Pretends to be the attacker's server: records everything it receives."""
    server_version = "LabAttacker/1.0"

    def log_message(self, *args):
        pass

    def _record(self, body: str = "") -> None:
        line = f"{time.strftime('%Y-%m-%dT%H:%M:%S')}\t{self.requestline}"
        if body:
            line += "\tbody=" + body.replace("\n", "\\n")[:4000]
        paths.RUNTIME.mkdir(parents=True, exist_ok=True)
        with _LOG_LOCK, paths.ATTACKER_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

    def _reply(self, data: bytes, ctype: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/__lab":
            return self._reply(_lab_info(), "application/json")
        self._record()
        self._reply(GIF, "image/gif")

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        self._record(self.rfile.read(min(n, 100_000)).decode(errors="replace"))
        self._reply(b"ok", "text/plain")


def _ui_handler():
    from .ui import UIHandler
    return UIHandler


SERVERS = {
    "web": (paths.WEB_PORT, lambda: WebHandler),
    "attacker": (paths.ATTACKER_PORT, lambda: AttackerHandler),
    "ui": (paths.UI_PORT, _ui_handler),
}

_started: dict = {}


def _listening(port: int) -> bool:
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex((paths.HOST, port)) == 0


def _same_lab(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://{paths.HOST}:{port}/__lab", timeout=2) as r:
            return json.load(r).get("lab") == str(paths.LAB_DIR)
    except Exception:
        return False


def start(name: str) -> ThreadingHTTPServer:
    port, handler = SERVERS[name]
    srv = ThreadingHTTPServer((paths.HOST, port), handler())   # 127.0.0.1 only
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, name=f"lab-{name}", daemon=True).start()
    _started[name] = srv
    return srv


def ensure_running(names=("web", "attacker")) -> None:
    """Start the named servers in this process unless the lab's own copy is already up."""
    for name in names:
        if name in _started:
            continue
        port = SERVERS[name][0]
        if _listening(port):
            if not _same_lab(port):
                raise RuntimeError(
                    f"port {port} is taken by something that is not this lab "
                    f"({paths.LAB_DIR}). Stop it, or stop the other lab copy's servers.")
            continue
        start(name)


def main() -> None:
    from .setup_lab import load_secrets
    load_secrets()  # make sure the lab has been set up at least once
    for name in SERVERS:
        port = SERVERS[name][0]
        if _listening(port):
            raise SystemExit(f"port {port} already in use - is `python3 -m lab.servers` running?")
        start(name)
    print(f"fixture web   http://{paths.HOST}:{paths.WEB_PORT}/   (serves lab/web/)")
    print(f"attacker      http://{paths.HOST}:{paths.ATTACKER_PORT}/   (logs to lab/runtime/attacker.log)")
    print(f"chat UI       http://{paths.HOST}:{paths.UI_PORT}/   (deliberately unsafe rendering)")
    print("Ctrl-C to stop.")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
