# Part 12 · Local infrastructure

**Level:** ⭐⭐⭐ · **Time:** ~4 h · **Requires:** parts 01, 02 (+ course 1 part 07, course 2 part 10) · **Produces:** an inventory of every listener on your machine/LAN, a loopback + reverse-proxy + auth layout, scan scripts, a verified before/after scan

---

## 0. The problem

Parts 03–11 attacked what the model reads and does. This part attacks the thing the model runs *on*: the
inference server, the chat UI, the vector database, the MCP servers, the GPU, the machine and the network
around them.

Almost every tool in a local LLM stack was built to work on a laptop in five minutes. That means: **no login,
plain HTTP, one process that is allowed to do everything, and a port number.** None of that is a bug on
`127.0.0.1`. All of it becomes a bug the moment the port is reachable by someone you did not mean to let in:
the rest of your LAN, a guest on your Wi-Fi, a container on the same Docker network, or **a web page open in
your own browser**.

Two facts frame the part:

1. An unauthenticated inference server gives a stranger **your GPU, your model and your electricity bill**, and
   often a read on what other people are asking. Nothing in the prompt-injection toolbox is needed.
2. The most exploited bugs in this ecosystem are not clever model attacks. They are **missing authentication,
   a service bound to every interface, and a parser that trusts what it downloads** — the same three bugs the
   web had in 2005.

⭐ **The thesis of this part: reachability is the first security control.** Decide who can send a packet to every
port before you decide anything else, then add authentication, then keep the software patched. You will write
three small scripts, take an inventory of **your own** machine, close what should not be open, and prove it
with a before/after scan.

**Scope and safety.** Every command in this part touches only `127.0.0.1` and machines **you own on your own
LAN**. The scripts refuse public addresses (they check, and they exit). Do not point a scanner at anything you
do not own: it is rude at best and illegal at worst, and nothing here needs it. Addresses in examples use the
documentation range `192.0.2.0/24`; substitute your own.

---

## 1. Words and maps

**Listener.** A process that has called `listen()` on an address and port. The *address* decides who can
connect:

| Bound to | Who can connect | Typical meaning |
| :-- | :-- | :-- |
| `127.0.0.1` / `::1` (loopback) | processes on this machine only (and **web pages in this machine's browser**, see §4) | the safe default |
| a LAN address (e.g. `192.0.2.10`) | everyone who can route to that address | "I want my phone to use it" |
| `0.0.0.0` / `::` (all interfaces) | every interface at once: LAN, Wi-Fi, VPN, Docker bridges, and the internet if the router or cloud firewall allows | "it just works" — and the usual cause of exposure |

**The stack, as a surface.** Each row is something you may be running. The "default posture" column is what the
project ships; check your version, defaults change.

| Component | Typical port | Default posture (verify!) | What an unauthenticated caller gets |
| :-- | :-- | :-- | :-- |
| llama-server (llama.cpp) | 8080 | binds `127.0.0.1`; auth only if you pass `--api-key` / `--api-key-file` | free inference, model info, in some versions/flags also `/props`, `/slots`, `/metrics` |
| Ollama | 11434 | binds `127.0.0.1`; **no authentication feature at all** | inference, list/pull/delete models, running-model info |
| vLLM, TGI, other OpenAI-compatible servers | 8000, … | varies; usually optional key | the same as llama-server |
| Open WebUI and similar chat UIs | 3000 / 8080 | has user accounts; first-registered account becomes admin | the UI, its stored chats, its connections to your model servers |
| Vector stores (Qdrant, Chroma, …) | 6333, 8000 | often no auth on a default install | **your RAG corpus** (part 11): read, poison (part 06), delete |
| MCP servers and inspectors | varies | local stdio, or a local HTTP port | whatever tools they expose (part 08) |
| Ray / compute clusters | 8265, 6379 | dashboard and job API with no auth by design | arbitrary code on every worker (§3, ShadowRay) |
| llama.cpp `rpc-server` | 50052 | no auth, trusts the caller completely | use of the GPU and memory of the host |
| Jupyter, Gradio, ad-hoc dashboards | 8888, 7860 | token or none | code execution (Jupyter) or the demo app |

The map of this part is therefore **a table you fill in for your own machine** (§6.1). The OWASP LLM Top 10 does
not cover it, because it is classic infrastructure security; the nearest entries are supply-chain items
(LLM03, part 10) and the whole deployment-side of NIST's and MITRE ATLAS's "execution environment" thinking.
What matters here is older and simpler: **least exposure, authenticate everything that is reachable, patch.**

```
                        internet
                           │   (router / cloud firewall: who is allowed in?)
        ┌──────────────────┴───────────────────────────────────────┐
        │  LAN / Wi-Fi  ── other people's devices, guests, IoT      │
        │        │                                                  │
        │  ┌─────┴───────── your machine ─────────────────────┐    │
        │  │  reverse proxy :443  (TLS + auth + limits + log)  │◄───┼── the ONLY thing on a non-loopback address
        │  │        │                                          │    │
        │  │  ┌─────┴─ loopback 127.0.0.1 ───────────────┐     │    │
        │  │  │ llama-server  chat UI  vector DB  MCP  … │◄────┼────┼── your browser: a web page can reach this too (§4)
        │  │  └──────────────────────────────────────────┘     │    │
        │  └───────────────────────────────────────────────────┘    │
        └───────────────────────────────────────────────────────────┘
```

---

## 2. Exposed inference servers

### 2.1 · What "exposed" costs

An inference server with no authentication is an open GPU. What a stranger can do with it, in order of
likelihood: run their own workloads on your hardware (free compute, and your electricity); read your system
prompt and configuration through whatever status endpoints the server has; flood it so your own use stops
(part 09, unbounded consumption); and, on servers with management APIs, load or delete models. If your app
also serves other people (part 11), they can also **see what others are asking**, because most of these
servers have no notion of "user".

### 2.2 · In the real world

- **Cisco**, scanning the internet in **September 2025**, found **1,139 exposed Ollama servers** (Cisco's
  measurement).
- **SentinelOne and Censys**, **January 2026**, reported about **175,000 hosts** exposing Ollama (their
  measurement).

The two numbers differ by more than two orders of magnitude. I have not checked how each team defined "exposed"
or how they probed, so **do not compare them as a trend**; take the point both make: this is not rare, and
internet-wide scanners find these services in hours. (Sources in [`SOURCES.md`](SOURCES.md).)

Two defaults make it worse:

- **Ollama has no authentication feature.** It binds `127.0.0.1` by default, and the documented way to reach it
  from elsewhere is to set `OLLAMA_HOST=0.0.0.0`, which publishes an API that cannot ask for a password. If
  you need remote access, the *only* design is a reverse proxy (§5.2) in front of a loopback-bound server.
- **llama-server binds `127.0.0.1` by default and supports `--api-key` / `--api-key-file`.** That is the right
  default and a useful lock. Two traps remain: someone adds `--host 0.0.0.0` for "just one test" and forgets,
  and `--api-key KEY` puts the key in the process list, where every local user can read it (use `--api-key-file`
  and `chmod 600`, §5.5).

### 2.3 · Docker publishes ports on every interface

⚠️ `docker run -p 8080:8080 …` binds **`0.0.0.0:8080`** on the host. Docker also writes its own packet-filter
rules *ahead of* the ones your host firewall front-end (`ufw`, `firewalld`) manages, so a port you "closed" in
`ufw` can still be reachable. The fix is one word in the publish flag:

```bash
docker run -p 127.0.0.1:8080:8080 …       # loopback only; the proxy on the host is the front door
```

In Compose: `ports: ["127.0.0.1:8080:8080"]`. Check the result with the inventory script in §6.1, not by
reading the file. Same for the chat UI container, the vector DB and anything else with a `ports:` line.

---

## 3. Bugs in the stack (public, patched)

Only public, **patched** issues, with the fixed version and the lesson; no exploit steps. Each is an example of
a bug *class* you should expect to see again. Update to at least the version shown, and read the vendor advisory
for details.

| CVE | Product | What kind of bug | Fixed in | The lesson |
| :-- | :-- | :-- | :-- | :-- |
| **CVE-2024-37032** ("Probllama", Wiz, 2024) | Ollama | path traversal in a model-pull code path (data from a registry used to build file paths), exploitable through the unauthenticated API | 0.1.34 | pulling a model is **parsing untrusted input**, and a management API with no auth lets anyone start it |
| **CVE-2024-28224** (NCC Group, Apr 2024) | Ollama | DNS rebinding: a web page could make the browser talk to the local API as if it were same-origin | 0.1.29 | "listens on localhost" does not mean "unreachable from the web" (§4) |
| **CVE-2026-7482** ("Bleeding Llama", Cyera, May 2026) | Ollama | memory disclosure (server memory leaks to a remote caller) | 0.17.1 | a server that holds other users' prompts in memory turns every memory bug into a privacy incident (part 11) |
| **CVE-2025-64496** (Open WebUI "Direct Connections") | Open WebUI | the UI trusted a model server you connect it to, so a hostile *model endpoint* could attack the UI | 0.6.35 | the model endpoint is an **input**, not a trusted back end: only connect to servers you control |
| **CVE-2025-49596** (Oligo, 2025) | MCP Inspector | a developer tool with a local proxy and no auth; a web page in the browser could drive it | 0.14.1 | local dev tools are services too; browser + localhost + no auth is a complete attack path (§4) |
| **CVE-2024-0132** | NVIDIA Container Toolkit | time-of-check/time-of-use container escape | 1.16.2 | the GPU toolchain runs with host privileges: **a container with GPU access is not a sandbox unless you keep the toolkit patched** |
| **CVE-2025-23266** ("NVIDIAScape", Wiz, Jul 2025) | NVIDIA Container Toolkit | another container-escape bug in the same layer | 1.17.8 | same: the escape is in the glue, not in your code |
| **CVE-2023-48022** (Ray; "ShadowRay", 2024) | Ray | the job API runs code for any caller; the vendor disputes it as a vulnerability (by design, no patch) | none (disputed) | a feature that is "by design" is still your exposure: put the cluster on a private network and in front of auth |
| **CVE-2023-4969** ("LeftoverLocals", Trail of Bits, Jan 2024) | GPU drivers (Apple, AMD, Qualcomm, Imagination reported) | GPU local memory not cleared between kernels | vendor driver updates | **GPUs shared between users can leak data between them**; on a multi-user box, process isolation does not cover the GPU |

ShadowRay was followed by **ShadowRay 2.0** (Oligo, Nov 2025), the same class again: exposed clusters, abused.
A single sentence covers the whole table: *the dangerous bugs live in the layers around the model, and they are
found by people who scan the internet, not by people who study prompts.*

⚠️ I give no version for LeftoverLocals because the fix is in each vendor's driver; check your own GPU vendor's
advisory for your hardware.

---

## 4. The browser is a bridge to your loopback

"Bound to `127.0.0.1`" protects you from other machines. It does **not** protect you from the page you opened
in your own browser, because the browser runs on your machine and can send requests to `127.0.0.1`.

### 4.1 · What CORS does and does not do

The browser's same-origin policy decides what a page can **read**. CORS is the server's way to relax it. The
rules that matter:

- A page on `https://evil.example` can **send** a "simple" request (e.g. a `POST` with `Content-Type:
  text/plain`) to `http://127.0.0.1:8080/...` with **no preflight**. The server processes it. The page just
  cannot read the answer.
- For a JSON `POST` the browser sends a preflight (`OPTIONS`) first. A server that answers it with permissive CORS
  headers hands the page the response too.

So "the answer was blocked by CORS" means *the server still did the work.* For an unauthenticated API that
mutates state (load a model, send a prompt that calls a tool) the **side effect** is the attack, and CORS never
sees it.

### 4.2 · DNS rebinding

The attacker's page loads from `rebind.example`. After the page is loaded, the attacker's DNS server changes the
answer for `rebind.example` to `127.0.0.1`. The browser's next request to `rebind.example` goes to **your**
local server, and because the origin is still `rebind.example`, the same-origin policy now **allows the page to
read the responses.** The server sees a request with `Host: rebind.example`.

⭐ **The defence is on the server: check the `Host` header against an allow-list** (`127.0.0.1:PORT`,
`localhost:PORT`, your real host name) and refuse the rest with `421`. A key in an `Authorization` header also
stops it, because the foreign page does not have the key. Do both. This is exactly what CVE-2024-28224 (Ollama)
was about.

### 4.3 · The browser is starting to help

Chrome's **Local Network Access** work (announced June 2025; opt-in from Chrome 138) makes the browser ask the
user before a public web page may reach private addresses. Good, but it is a **seatbelt, not a lock**: it depends
on browser and version, on the user clicking the right button, and it does not protect you from your own
other processes or from other browsers. Treat it as defence in depth, never as the control.

### 4.4 · Why a page can find your port

Scanning `127.0.0.1:1…65535` from a web page is slow but possible; pages try the well-known ports first (11434,
8080, 3000, 6333, 8000, 8265). **Default ports are public knowledge**, so moving to a "secret" port is not a
control; it only shortens the list of log lines.

---

## 5. The layout to aim for

```
 client ──TLS──▶ reverse proxy ──plain HTTP──▶ llama-server (127.0.0.1)
                 · TLS            · bearer key            · only reachable from the proxy
                 · key per client · body size cap         · no key needed (or one the proxy adds)
                 · rate limit     · request log
```

### 5.1 · Bind to loopback, always

Every backend gets a loopback address (`--host 127.0.0.1`, `OLLAMA_HOST=127.0.0.1`, `-p 127.0.0.1:…`). Exactly
one thing may listen on a non-loopback address: the reverse proxy. If a backend must be on a different machine
from its proxy, use a private network or an SSH/WireGuard tunnel and still bind it to the **tunnel** address only.

### 5.2 · A reverse proxy in front

A proxy adds what the backends lack, in one place: TLS, authentication, request size limits, rate limits and an
access log. With Caddy it is a dozen lines (`deploy/Caddyfile`):

```
# Caddy 2: TLS + bearer key + body cap in front of llama-server on 127.0.0.1:8080.
# Start:  LLM_PROXY_KEY=$(cat ~/llm.key) caddy run --config deploy/Caddyfile
llm.example.test {
	tls internal                      # Caddy's own local CA; use a real certificate in production
	@denied not header Authorization "Bearer {$LLM_PROXY_KEY}"
	respond @denied 401
	request_body {
		max_size 1MB
	}
	reverse_proxy 127.0.0.1:8080
}
```

`tls internal` uses Caddy's own local certificate authority (good for a home or lab network: you install that
root on your devices once). The `@denied` matcher refuses any request without the right bearer key with `401`,
`request_body` caps the body, and `reverse_proxy` forwards the rest. Behind it, llama-server needs no key of its
own, but adding `--api-key-file` is free defence in depth. nginx and Traefik do the same job; the choice does not
matter, the **topology** does.

⚠️ One shared key for everyone is better than no key and worse than a key per client: you cannot revoke one
person, and the log cannot say who did what. §5.6 covers per-user keys. I validated this Caddyfile with `caddy validate`
and ran it in a throwaway container in front of a stub upstream: no key gave `401`, a wrong key `401`, the right key
`200`, a 1.2 MB body `413`. Do the same on your own setup, starting with `caddy validate`.

### 5.3 · Segmentation and egress

- **Put the inference host on a network segment** (VLAN or at least a firewall rule set) that your phones, TVs
  and guests cannot reach, and that can reach out only where it must.
- **Control egress.** A model host that can reach the whole internet is an exfiltration path (part 07) and a
  command-and-control path if anything on it is ever compromised. If the host only needs to pull models from one
  place, allow that and nothing else, and do model downloads deliberately (part 10), not from the serving process.
- Name the three flows explicitly: *who may call the proxy*, *what the proxy may call*, *what the backends may
  call*. Anything not on the list is denied. The last item is the one people forget.

### 5.4 · Containers and GPU access

A container is a convenience boundary, not a sandbox, unless you configure it as one. For a serving container:

```bash
MODELS=~/models                    # a folder with your .gguf files
IMAGE=your-llama-server-image      # a llama.cpp server image you chose; pin it by digest
# AMD ROCm devices below; for NVIDIA drop both --device flags and add --gpus device=0
docker run --rm \
  -p 127.0.0.1:8080:8080 \
  --cap-drop ALL --security-opt no-new-privileges \
  --read-only --tmpfs /tmp \
  -v "$MODELS":/models:ro \
  --device /dev/kfd --device /dev/dri \
  "$IMAGE" -m /models/your-model.gguf --host 0.0.0.0 --port 8080
```

(`--host 0.0.0.0` is the address **inside** the container, the only one Docker can forward to; what keeps the
server off your LAN is the `127.0.0.1:` in the publish flag.)

What each choice buys: `127.0.0.1` in the publish flag (§2.3); no capabilities and no privilege escalation;
a read-only root and a read-only model volume (a compromised server cannot rewrite the model, part 10); and
**only the GPU device nodes it needs.** Never use `--privileged`, never mount the Docker socket (`/var/run/docker.sock`)
into a container, and never mount your home directory. Remember §3: the GPU path itself is attack surface
(NVIDIA toolkit CVEs, LeftoverLocals), so keep drivers and toolkit patched, and do not share one GPU between
*mutually untrusting* users. For the sandbox for the code a model writes, go to course 1 part 07 and course 2
part 10: that is a different, stricter container.

### 5.5 · Secrets

- Keys in a **file** with mode `600` (`--api-key-file`, a Docker/Compose secret, a systemd credential), not in
  command lines (visible to every local user in the process list) and not in environment variables of a
  long-lived shell.
- Never in the image, never in git, never in the chat history the model can see (part 05: whatever is in a prompt,
  the user can read).
- One key per client and per purpose; rotate on a schedule and immediately after any doubt. Part 14 has the
  rotation steps for an incident.
- The upstream model key the proxy holds is **not** forwarded to clients: see the comment in
  `infra/auth_proxy.py`.

### 5.6 · More than one user

Once other people use your app: authenticate **each user** (a key or login per person), log who called what
(part 14, redacted), rate-limit per key (part 09), and re-read part 11 for cache and memory sharing. The chat
UI's own accounts are not the proxy's accounts: decide which one is the real boundary and make the other
redundant, not contradictory. Open WebUI-style UIs often make the *first registered account the administrator*:
register yours before anyone else can, and turn open sign-up off.

### 5.7 · Updates

A local stack has no vendor pushing patches. Every row of §3 was fixed by a release somebody had to install.

- **Pin** versions (container tags by digest, `pip`/`npm` lock files) so you know what you run.
- **Subscribe** to the advisories of every component in the §1 table (GitHub "Watch → Security advisories" is
  enough).
- **Schedule** a monthly "update and re-run the scan" slot; add an out-of-band update when a CVE hits something
  you run.
- Do not auto-update the serving path blindly either: a bad release is also a supply-chain event (part 10). Update
  in a copy, run the part 13 gate, then switch.

---

## 6. LAB · inventory, probe, scan, close, verify

Everything runs from `$SEC` (the folder that contains `lab/`). The scripts live in `$SEC/infra/` and are standalone
stdlib Python. They are read-only except `auth_proxy.py` and `cors_lab.py`, which start servers on loopback.

```bash
mkdir -p "$SEC/infra" && cd "$SEC"
```

### 6.1 · Inventory: every listener on this machine

```bash
cat > infra/inventory.py <<'EOF'
"""List every TCP listener on THIS machine and say how exposed it is.

Linux: uses `ss`; macOS: uses `lsof`. Read-only, touches nothing.
Usage: python3 infra/inventory.py [--json out.jsonl]
"""
import json, platform, re, subprocess, sys

KNOWN = {  # default ports of common LLM-stack components (a hint, not proof)
    8080: "llama-server / Open WebUI (container)", 11434: "Ollama",
    8000: "vLLM / Chroma", 3000: "Open WebUI (published)", 8265: "Ray dashboard",
    6333: "Qdrant", 50052: "llama.cpp rpc-server", 7860: "Gradio",
    8888: "Jupyter", 8760: "lab UI", 8765: "lab web", 8766: "lab attacker",
}

def listeners():
    if platform.system() == "Linux":
        out = subprocess.run(["ss", "-ltnpH"], capture_output=True, text=True).stdout
        for line in out.splitlines():
            cols = line.split()
            if len(cols) < 4:
                continue
            local = cols[3]
            proc = re.search(r'users:\(\("([^"]+)"', line)
            yield local, proc.group(1) if proc else "?"
    else:  # macOS / BSD
        out = subprocess.run(["lsof", "-nP", "-iTCP", "-sTCP:LISTEN"],
                             capture_output=True, text=True).stdout
        for line in out.splitlines()[1:]:
            cols = line.split()
            if len(cols) >= 9:
                yield cols[8], cols[0]

def classify(addr: str) -> str:
    host = addr.rsplit(":", 1)[0].strip("[]")
    if host in ("127.0.0.1", "::1", "localhost") or host.startswith("127."):
        return "loopback"
    if host in ("*", "0.0.0.0", "::", ""):
        return "ALL-INTERFACES"
    return f"interface {host}"

def main():
    rows = []
    for local, proc in listeners():
        port = int(local.rsplit(":", 1)[1])
        rows.append({"addr": local, "port": port, "process": proc,
                     "exposure": classify(local), "hint": KNOWN.get(port, "")})
    rows.sort(key=lambda r: (r["exposure"] == "loopback", r["port"]))
    for r in rows:
        flag = "⚠️ " if r["exposure"] != "loopback" else "   "
        print(f"{flag}{r['addr']:<28} {r['process']:<18} {r['exposure']:<20} {r['hint']}")
    if "--json" in sys.argv:
        path = sys.argv[sys.argv.index("--json") + 1]
        with open(path, "w") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        print(f"\nsaved {len(rows)} rows to {path}")

if __name__ == "__main__":
    main()
EOF
python3 infra/inventory.py --json before.jsonl
```

The first column is the bound address: anything flagged `ALL-INTERFACES` or `interface …` is reachable from
other machines (subject to your firewall). The "hint" column is a guess from the port number, nothing more.
`process` is the program name; on Linux you may need `sudo` to see processes of other users (`ss -p`). On macOS
this uses `lsof`.

### 6.2 · Probe: what would a stranger get?

```bash
cat > infra/probe_llm.py <<'EOF'
"""Ask YOUR OWN hosts what an unauthenticated stranger would get.

Refuses anything that is not loopback or a private / documentation address.
Usage: python3 infra/probe_llm.py 127.0.0.1 8080 11434 [--key KEY]
"""
import ipaddress, json, sys, urllib.error, urllib.request

PATHS = [  # read-only fingerprints; nothing here changes server state
    "/v1/models", "/health", "/props", "/slots", "/metrics",   # llama-server
    "/api/version", "/api/tags", "/api/ps",                     # Ollama
    "/api/jobs/",                                              # Ray job API
]

def own_address(host: str) -> bool:
    ip = ipaddress.ip_address(host)
    return ip.is_loopback or ip.is_private

def get(url, headers):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=3) as r:
            return r.status, dict(r.headers), r.read(300)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), b""
    except Exception as e:  # closed port, timeout, TLS
        return None, {}, str(e).encode()

def probe(host, port, key=None):
    base = f"http://{host}:{port}"
    auth = {"Authorization": f"Bearer {key}"} if key else {}
    found = []
    for p in PATHS:
        status, hdrs, body = get(base + p, auth)
        if status is None:
            return [("port", "closed or not HTTP")]
        if status == 200:
            found.append((p, body[:80].decode(errors="replace").replace("\n", " ")))
    # CORS: does the server hand its responses to any web page?
    _, hdrs, _ = get(base + "/v1/models", {"Origin": "http://evil.example", **auth})
    acao = {k.lower(): v for k, v in hdrs.items()}.get("access-control-allow-origin")
    if acao:
        found.append(("CORS", f"Access-Control-Allow-Origin: {acao}"))
    # DNS rebinding: is a foreign Host header accepted?
    status, _, _ = get(base + "/v1/models", {"Host": "rebind.example", **auth})
    found.append(("Host check", "foreign Host ACCEPTED" if status == 200
                  else f"foreign Host refused ({status})"))
    return found

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    key = sys.argv[sys.argv.index("--key") + 1] if "--key" in sys.argv else None
    if key in args:
        args.remove(key)
    host, ports = args[0], [int(p) for p in args[1:]]
    if not own_address(host):
        sys.exit(f"refusing {host}: only loopback / private addresses (your own LAN)")
    for port in ports:
        print(f"== {host}:{port}")
        for what, detail in probe(host, port, key):
            print(f"   {what:<14} {detail}")

if __name__ == "__main__":
    main()
EOF
python3 infra/probe_llm.py 127.0.0.1 8080 11434          # from the machine itself
python3 infra/probe_llm.py 192.0.2.10 8080 11434         # use YOUR machine's LAN address
```

The second form is a nice trick: connecting to your **own LAN address** from the same machine tests the
*binding*. A service bound only to `127.0.0.1` refuses that connection; one bound to `0.0.0.0` answers. It lists
which read-only paths answer without a key, whether the server returns an `Access-Control-Allow-Origin` header to
a foreign `Origin`, and whether it accepts a foreign `Host` header (the DNS-rebinding precondition, §4.2). Add
`--key KEY` to see the difference a key makes.

### 6.3 · Scan your own LAN (from a second machine of yours)

```bash
cat > infra/lan_scan.py <<'EOF'
"""TCP connect scan of YOUR OWN LAN for LLM-stack ports. Stdlib, slow, polite.

Refuses non-private networks and anything bigger than a /24.
Usage: python3 infra/lan_scan.py 192.0.2.0/24 [--out scan.jsonl]
"""
import concurrent.futures as cf, ipaddress, json, socket, sys

PORTS = [22, 3000, 6333, 7860, 8000, 8080, 8265, 8888, 11434, 50052]

def is_open(host, port):
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0

def main():
    net = ipaddress.ip_network(sys.argv[1], strict=False)
    if not net.is_private or net.num_addresses > 256:
        sys.exit("refusing: only your own private network, at most a /24")
    jobs = [(str(h), p) for h in net.hosts() for p in PORTS]
    with cf.ThreadPoolExecutor(max_workers=32) as ex:
        hits = [j for j, ok in zip(jobs, ex.map(lambda j: is_open(*j), jobs)) if ok]
    for host, port in hits:
        print(f"{host:<16} {port}")
    if "--out" in sys.argv:
        with open(sys.argv[sys.argv.index("--out") + 1], "w") as f:
            for host, port in hits:
                f.write(json.dumps({"host": host, "port": port}) + "\n")

if __name__ == "__main__":
    main()
EOF
python3 infra/lan_scan.py 192.0.2.0/24 --out lan-before.jsonl      # YOUR network, not mine
```

It is a plain TCP connect on ten well-known ports. It refuses non-private ranges and anything larger than a
/24, and it is slow on purpose. Run it **from a different machine than the one you are checking** (a laptop
against the server), because a machine scanning itself tells you about its own firewall, not about what the LAN
sees. If you do not own a second machine, skip this step and rely on the own-LAN-address trick of §6.2. **Do not scan a network you do not run.**

### 6.4 · The browser path: CORS and the Host check

```bash
cat > infra/cors_lab.py <<'EOF'
"""Two loopback servers to watch what a *foreign web page* can do to a localhost API.

  127.0.0.1:8798  "foreign" page (different origin = different port)
  127.0.0.1:8799  target API: logs every request (method, Origin, Host, body)
Usage: python3 infra/cors_lab.py [--strict]   then open http://127.0.0.1:8798/
(ports busy? CORS_PAGE_PORT=... CORS_API_PORT=... python3 infra/cors_lab.py)
--strict turns on the two defences: Host allow-list + bearer token.
"""
import http.server, json, os, sys, threading

STRICT = "--strict" in sys.argv
PAGE_PORT = int(os.environ.get("CORS_PAGE_PORT", "8798"))
API_PORT = int(os.environ.get("CORS_API_PORT", "8799"))
TOKEN = "lab-token-not-a-secret"
ALLOWED_HOSTS = {f"127.0.0.1:{API_PORT}", f"localhost:{API_PORT}"}

PAGE = """<!doctype html><meta charset=utf-8><title>foreign page</title>
<pre id=log></pre><script>
const T = new URLSearchParams(location.search).get("target") || "http://127.0.0.1:__API__";
const log = m => document.getElementById("log").textContent += m + "\\n";
async function tryIt(name, opts) {
  try { const r = await fetch(T + "/v1/chat/completions", opts);
        log(name + ": response READABLE, status " + r.status); }
  catch (e) { log(name + ": response blocked by the browser (" + e + ")"); }
}
tryIt("A simple POST text/plain", {method: "POST", body: '{"messages":[{"role":"user","content":"say MARKER-A"}]}'});
tryIt("B JSON POST (preflight)", {method: "POST", headers: {"Content-Type": "application/json"},
      body: '{"messages":[{"role":"user","content":"say MARKER-B"}]}'});
new Image().src = T + "/v1/models?marker=C";  log("C image GET sent");
</script>"""

class Page(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(PAGE.replace("__API__", str(API_PORT)).encode())
    def log_message(self, *a):
        pass

class Target(http.server.BaseHTTPRequestHandler):
    def _guard(self) -> bool:
        if not STRICT:
            return True
        if self.headers.get("Host") not in ALLOWED_HOSTS:
            self._reply(421, {"error": "unknown Host (DNS rebinding?)"}); return False
        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            self._reply(401, {"error": "missing token"}); return False
        return True
    def _reply(self, code, obj):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode())
    def _record(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n).decode(errors="replace") if n else ""
        print(f"[target] {self.command:<7} {self.path:<28} Origin={self.headers.get('Origin')} "
              f"Host={self.headers.get('Host')} body={body[:60]!r}", flush=True)
    def do_OPTIONS(self):          # preflight: we do NOT allow foreign origins
        self._record(); self.send_response(204); self.end_headers()
    def do_GET(self):
        self._record()
        if self._guard(): self._reply(200, {"data": [{"id": "local"}]})
    def do_POST(self):
        self._record()
        if self._guard(): self._reply(200, {"choices": [{"message": {"content": "ok"}}]})
    def log_message(self, *a):
        pass

def serve(port, handler):
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()

if __name__ == "__main__":
    threading.Thread(target=serve, args=(PAGE_PORT, Page), daemon=True).start()
    print(f"strict={STRICT}. Open http://127.0.0.1:{PAGE_PORT}/ in your browser. Ctrl-C to stop.")
    serve(API_PORT, Target)
EOF
python3 infra/cors_lab.py            # terminal A: open http://127.0.0.1:8798/ in your browser
```

The page on port 8798 is a *foreign origin* relative to the API on 8799. It fires three requests: a simple
`text/plain` POST, a JSON POST (needs a preflight) and an `<img>` GET. Read what the **terminal** shows (the
server logged all of them, with `Origin` and `Host`) against what the **page** shows (which answers it could
read). Prediction, mine and unmeasured: the simple POST and the image GET reach the server and the page can read
neither answer; the JSON POST sends only an `OPTIONS`, which the server answers with no CORS headers, so the
browser never sends the real request. Then stop it and run `python3 infra/cors_lab.py --strict`: the Host
allow-list and the bearer key are on: the same three requests still arrive (the terminal logs them), but the server
now refuses them with `401` instead of doing the work, and the page still reads nothing. Prove the rebinding defence without DNS
tricks by changing the header yourself:

```bash
curl -s -i -H "Host: rebind.example:8799" http://127.0.0.1:8799/v1/models           # 421 in --strict mode
curl -s -i -H "Authorization: Bearer lab-token-not-a-secret" http://127.0.0.1:8799/v1/models   # 200
```

(Ports busy? Set `CORS_PAGE_PORT` and `CORS_API_PORT`.)

### 6.5 · A tiny auth proxy to practise on (not for production)

```bash
cat > infra/auth_proxy.py <<'EOF'
"""A minimal auth + Host-check reverse proxy. A TEACHING tool: no streaming (it buffers the
whole answer), no HTTP/2. For real use put Caddy or nginx in front (section 5.2).

    python3 infra/auth_proxy.py --listen 8081 --upstream http://127.0.0.1:8080
        --key-file proxy.key --host llm.example.test [--bind 127.0.0.1] [--cert c.pem --key k.pem]

What it enforces: Host header on an allow-list (stops DNS rebinding), bearer key compared
in constant time, request body capped, every request logged with a short key fingerprint.
"""
import argparse
import hashlib
import hmac
import http.server
import pathlib
import ssl
import sys
import urllib.error
import urllib.request

MAX_BODY = 1_000_000


def make_handler(upstream, key, hosts):
    class H(http.server.BaseHTTPRequestHandler):
        def _reply(self, code, body=b"", ctype="application/json"):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _handle(self):
            fp = "-"
            if self.headers.get("Host", "") not in hosts:
                code = 421                                   # misdirected request: wrong Host
            else:
                got = self.headers.get("Authorization", "")
                if not hmac.compare_digest(got.encode(), f"Bearer {key}".encode()):
                    code = 401
                else:
                    fp = hashlib.sha256(key.encode()).hexdigest()[:6]
                    n = int(self.headers.get("Content-Length") or 0)
                    code = 413 if n > MAX_BODY else 0
            if code:
                print(f"{self.command} {self.path} -> {code} key={fp}", file=sys.stderr, flush=True)
                return self._reply(code, b'{"error": "refused by proxy"}')
            body = self.rfile.read(n) if n else None
            req = urllib.request.Request(upstream + self.path, data=body, method=self.command)
            req.add_header("Content-Type", self.headers.get("Content-Type", "application/json"))
            try:                                             # the upstream key, if any, is not ours to forward
                with urllib.request.urlopen(req, timeout=300) as r:
                    code, data, ctype = r.status, r.read(), r.headers.get("Content-Type", "application/json")
            except urllib.error.HTTPError as e:
                code, data, ctype = e.code, e.read(), "application/json"
            except OSError:
                code, data, ctype = 502, b'{"error": "upstream unreachable"}', "application/json"
            print(f"{self.command} {self.path} -> {code} key={fp}", file=sys.stderr, flush=True)
            self._reply(code, data, ctype)

        do_GET = do_POST = _handle

        def log_message(self, *a):
            pass
    return H


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--listen", type=int, required=True)
    ap.add_argument("--bind", default="127.0.0.1")
    ap.add_argument("--upstream", required=True)
    ap.add_argument("--key-file", required=True)
    ap.add_argument("--host", action="append", default=[], help="allowed Host name (repeatable)")
    ap.add_argument("--cert")
    ap.add_argument("--key")
    a = ap.parse_args()
    key = pathlib.Path(a.key_file).read_text().strip()
    hosts = set()
    for h in a.host + ["127.0.0.1", "localhost"]:
        hosts.update({h, f"{h}:{a.listen}"})
    srv = http.server.ThreadingHTTPServer((a.bind, a.listen),
                                          make_handler(a.upstream.rstrip("/"), key, hosts))
    if a.cert:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(a.cert, a.key)
        srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    print(f"proxy {a.bind}:{a.listen} -> {a.upstream}  hosts={sorted(hosts)}", file=sys.stderr)
    srv.serve_forever()


if __name__ == "__main__":
    main()
EOF
python3 -c "import secrets; print(secrets.token_urlsafe(32))" > proxy.key && chmod 600 proxy.key
python3 infra/auth_proxy.py --listen 8081 --upstream http://127.0.0.1:8080 --key-file proxy.key --host llm.example.test
```

In another terminal:

```bash
python3 infra/probe_llm.py 127.0.0.1 8081                              # no key: nothing answers
python3 infra/probe_llm.py 127.0.0.1 8081 --key "$(cat proxy.key)"     # with the key: the upstream answers
```

It buffers the whole reply, so streaming chat will not stream through it; that is the price of 90 lines of
stdlib. Real deployments use the Caddyfile of §5.2. What this proxy teaches is the three decisions: Host
allow-list, constant-time key comparison (`hmac.compare_digest`) and a body cap. Also note what is *not* in it:
TLS (give it `--cert`/`--key` if it ever leaves loopback: a bearer key over plain HTTP on a LAN is readable by
anyone on it), per-user keys and rate limits.

---

## 7. ⭐ EXPERIMENT 12 — before and after on your own machine

**Hypothesis.** Your machine has at least one listener that is more exposed than it needs to be (a container
publishing on all interfaces, a dev server bound to `0.0.0.0`, a UI someone started "just to test"), and after you
move every backend to loopback and put one authenticated proxy in front, a probe from the LAN side finds nothing
open except the proxy, and nothing answers it without a key.

**Procedure.**

1. `python3 infra/inventory.py --json before.jsonl`. Mark each row **needed / not needed** and **who must reach it**
   (nobody, this machine, a device on my LAN).
2. For every row that is not loopback, write the reason it is not loopback. If you cannot, it is a finding.
3. `python3 infra/probe_llm.py <your-LAN-address> <port>…` for each such port; save the output.
4. From a second machine of yours: `python3 infra/lan_scan.py <your-subnet> --out lan-before.jsonl`.
5. Fix: bind backends to loopback; change `-p` flags to `127.0.0.1:`; set `--api-key-file` where there is one;
   front what must be reachable with the proxy; turn off open sign-up on the UI.
6. Re-run steps 1, 3 and 4 as `after`.
7. `diff before.jsonl after.jsonl` and `diff lan-before.jsonl lan-after.jsonl`.

**Prediction** (mine, unmeasured, for a typical home-lab with a UI container and one or two inference servers):
step 1 shows between one and four non-loopback listeners; at least one is a Docker-published port you did not
remember publishing; step 3 shows that at least one answers `/v1/models` without a key and accepts a foreign
`Host`; after the fixes the LAN scan shows only the proxy port.

| What | Before | After |
| :-- | :-- | :-- |
| Listeners not on loopback (count) | | |
| Which ones, and why | | |
| Ports answering without a key (LAN address) | | |
| Foreign `Host` accepted (count) | | |
| Ports seen by the LAN scan | | |
| Anything you could not close, and the compensating control | | |

---

## 8. EXERCISES

1. **Inventory your other machines.** Repeat §6.1 on every machine that runs any part of your stack (server, laptop,
   the box with the GPU). Which ones had a listener you did not know about?
2. **Rebinding in the lab.** Run the lab's chat UI (`python3 -m lab.servers`, port 8760). Which of its three
   servers check the `Host` header? Add a 421 check to the one you think matters most, and prove it with `curl -H`.
3. **A proxy for the Sieve endpoint.** Part 13 §6.4 builds an OpenAI-compatible endpoint for Sieve. Put
   `auth_proxy.py` in front of it and make the red-team tools talk to the proxy with a key. What changes in the
   tool configs?
4. **Threat-model the network.** Draw your real network like the diagram in §1 (names, not addresses) and mark every
   trust boundary a request crosses from "guest Wi-Fi" to "model". Which crossing has no control at all?
5. **Update drill.** List every component of your stack, the version you run and the newest one. Which are more than
   two minor versions behind, and does any advisory apply?
6. **Egress.** From inside your serving container run `curl -sI https://example.com`. If it works, write down
   what the container actually needs to reach and the rule that would allow only that.

---

## 9. Traps of this part

| ID | Trap | Symptom | Remedy |
| :-- | :-- | :-- | :-- |
| **T12.1** | `0.0.0.0` "to test from my phone", never reverted | Inventory shows `ALL-INTERFACES` weeks later | Proxy plus loopback; never test with the exposed backend |
| **T12.2** | `-p 8080:8080` and a host firewall that "blocks 8080" | Port still answers from the LAN | `-p 127.0.0.1:8080:8080`; verify with the inventory, not the firewall config |
| **T12.3** | Security by obscure port | "Nobody knows it's on 18434" | Scanners and web pages try the defaults first, then everything; authenticate |
| **T12.4** | "It's only on localhost" | A page in your own browser reaches it | Host allow-list plus a key (§4) |
| **T12.5** | `--api-key KEY` on the command line | The key is visible in `ps` to every local user | `--api-key-file`, mode 600 |
| **T12.6** | One shared key | Cannot revoke one person; log cannot say who | Key per client at the proxy |
| **T12.7** | Bearer key over plain HTTP on the LAN | Anyone on the LAN reads it | TLS at the proxy, always, once it leaves loopback |
| **T12.8** | Scanning yourself from yourself | "Nothing open" but a laptop can connect | Scan from a second machine; use your own LAN address (§6.2) |
| **T12.9** | `--privileged`, the Docker socket or `$HOME` mounted into a serving container | A compromised server owns the host | Drop caps, mount read-only, pass only the GPU device nodes (§5.4) |
| **T12.10** | Patching once | A CVE from this table hits a stale version | Pin, subscribe, monthly update slot (§5.7) |
| **T12.11** | Trusting the model endpoint the UI connects to | A hostile endpoint (CVE-2025-64496 class) attacks the UI | Connect only to servers you control; update the UI |
| **T12.12** | One shared GPU for untrusting users | LeftoverLocals-style leakage between processes | Do not share one GPU across mutually untrusting users |

---

## 10. Checkpoint

```bash
cd "$SEC"
python3 infra/inventory.py | grep -v "loopback"        # ideally only the proxy
python3 infra/probe_llm.py <your-LAN-address> 8080 11434   # connection refused for the backends
python3 infra/probe_llm.py <proxy-host-or-address> <proxy-port>   # nothing without a key
```

- [ ] You can explain the difference between loopback, a LAN address and `0.0.0.0`, and why a page in your own
      browser can reach loopback
- [ ] Every backend you run is bound to loopback; exactly one thing (the proxy) is not
- [ ] The proxy has TLS and a key; your key lives in a mode-600 file, not on a command line
- [ ] `inventory.py` and a second-machine scan agree with your own list in the §7 table
- [ ] Your before/after table is filled in, with what you could not close and the compensating control
- [ ] You have written down your update routine and the advisories you follow
- [ ] You can name, for each of the §3 bug classes, the one control in §5 that would have stopped it

---

**Next: [`13-GUARDRAILS-RED-TEAMING-AND-EVALUATING-DEFENCES.md`](13-GUARDRAILS-RED-TEAMING-AND-EVALUATING-DEFENCES.md)** —
guardrail models, how to measure them honestly, red-team tools pointed at the lab, and a regression gate for CI.

Related: course 1, [part 07 — sandbox, security, monitoring](../course_local_models/07-SANDBOX-SECURITY-MONITORING.md);
course 2, [part 10 — production sandbox](../course_agentic_apps/10-PRODUCTION-SANDBOX.md). Sources:
[`SOURCES.md`](SOURCES.md).
