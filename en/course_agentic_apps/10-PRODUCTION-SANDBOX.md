# Part 10 · The production sandbox

**Level:** ⭐⭐⭐⭐ · **Time:** ~5 h · **Requires:** course 1 part 7 (`bwrap`), part 2 (session trust), part 8 (code-mode)
**Produces:** three isolation levels wired into the gateway, network egress control, a secrets layer, a set of escape attempts

---

## 0. The question this part answers

**Not** "how to run code in isolation": you know that from course 1.

Only: **"what exactly does each rung of isolation protect against, and what does it
cost?"** Because the answer "use a container" is insufficient in 2026, and with an agent
that writes its own code it is simply untrue.

> **Your container is not a sandbox.** Standard multi-tenant containers will not hold an
> agent that executes arbitrary code. When an agent can write its own scripts, install
> packages and manipulate file descriptors, **a shared kernel becomes a liability**.
> — [emirb, *Your Container Is Not a Sandbox*](https://emirb.github.io/blog/microvm-2026/)

---

## 1. The isolation ladder

```
  COST                                           WHAT IT STOPS
    │
    │  ┌─ 5 · virtual machine ─────────────┐    everything except a hypervisor bug
    │  │    full VM, separate kernel       │    start: 10–30 s   RAM: 1 GB+
    │  ├─ 4 · microVM (Firecracker/libkrun)┤    ⭐ separate kernel, small surface
    │  │                                    │    start: <1 s      RAM: 128 MB+
    │  ├─ 3 · gVisor ─────────────────────┤    kernel in user space
    │  │                                    │    start: ~ms       I/O overhead 10–40%
    │  ├─ 2 · rootless container (podman) ─┤    namespace + seccomp, SHARED KERNEL
    │  │                                    │    start: ~200 ms
    │  ├─ 1 · bwrap + seccomp + cgroups ───┤    namespace, SHARED KERNEL
    │  │                                    │    start: ~10 ms    ⭐ you have this
    │  └─ 0 · none ─────────────────────────┘    nothing
    ▼
```

### 1.1 · What each rung really stops

| Threat | 1 `bwrap` | 2 rootless | 3 gVisor | 4 microVM |
| :-- | :-: | :-: | :-: | :-: |
| Reading your files | ⭐ yes | ⭐ yes | ⭐ yes | ⭐ yes |
| Writing outside the work area | ⭐ yes | ⭐ yes | ⭐ yes | ⭐ yes |
| Network egress | ⭐ yes (`--unshare-net`) | ⭐ yes | ⭐ yes | ⭐ yes |
| CPU/RAM exhaustion | with cgroups | ⭐ yes | ⭐ yes | ⭐ yes |
| Peeking at other processes | ⭐ yes | ⭐ yes | ⭐ yes | ⭐ yes |
| **A Linux kernel exploit** | ✗ **no** | ✗ **no** | ⭐ yes | ⭐ yes |
| Escape through `/proc`, `/sys` | partially | partially | ⭐ yes | ⭐ yes |
| Side channels (timing, cache) | ✗ | ✗ | partially | partially |

⭐ **The entire "kernel exploit" row is the reason rungs 3 and 4 exist.** At rungs 1 and 2
the agent's code talks to **the same kernel** as the rest of your system. A single hole
in a system call = an escape. gVisor eliminates this, because the sandboxed process
**never talks to the real kernel**: it talks to a reimplementation of it in user space.

### 1.2 · Which rung for which agent

| Agent | What it processes | Rung | Justification |
| :-- | :-- | :-: | :-- |
| **Archivist** | your files | **1** `bwrap` | trusted input; you protect against a mistake, not an attack |
| **Steward** | calendar, local network | **1–2** | semi-trusted input |
| **Researcher** | ⚠️ **content from the internet** | **3–4** | hostile input by definition |
| **code-mode** (part 8) | code written by the model | **2–4** | ⭐ depends on where the task came from |

⭐ **The rule: the isolation level follows from the source of the INPUT, not from the
agent's name.** An Archivist asked to process a file that arrived by email is, in that
turn, as untrusted as the Researcher. This is exactly the thing you implemented in part
2 as the session trust level; now you will enforce it.

---

## 2. Rung 1: `bwrap` done properly

Course 1 gave the basics. Here is the production version with resource limits.

```bash
# $OSA/piaskownica/szczebel1.sh
#!/usr/bin/env bash
set -euo pipefail

OBSZAR="${1:?working directory}"; shift
ARCHIWUM="${ARCHIWUM:-}"

ARGS=(
  --unshare-all                      # ⭐ all namespaces: net, pid, ipc, uts, cgroup
  --die-with-parent                  # killed together with the gateway
  --new-session                      # P44: no injection into the terminal via TIOCSTI
  --clearenv                         # ⭐ P101: no secrets through the environment
  --setenv PATH /usr/bin:/bin
  --setenv HOME "$OBSZAR"
  --setenv LANG pl_PL.UTF-8
  --ro-bind /usr /usr
  --ro-bind /bin /bin
  --ro-bind /lib /lib
  --symlink usr/lib64 /lib64
  --ro-bind /etc/ssl /etc/ssl
  --proc /proc
  --dev /dev
  --tmpfs /tmp
  --bind "$OBSZAR" "$OBSZAR"         # the only write
  --chdir "$OBSZAR"
)
[ -n "$ARCHIWUM" ] && ARGS+=(--ro-bind "$ARCHIWUM" /archiwum)

# Resource limits: bwrap does NOT have them, systemd adds them
exec systemd-run --user --scope --quiet \
  -p MemoryMax=1G -p CPUQuota=200% -p TasksMax=64 \
  -- sudo bwrap "${ARGS[@]}" -- "$@"
```

⚠️ **`sudo` before `bwrap` is necessary on this machine here, not decorative.** Ubuntu
24.04 restricts the creation of user namespaces by unprivileged processes
(`kernel.apparmor_restrict_unprivileged_userns=1`), and the `bubblewrap` package in this
release **has no AppArmor profile of its own**, which would normally get around this.
Checked live (full diagnosis and kernel log evidence: course 1,
`07-SANDBOX-SECURITY-MONITORING.md`, §2). Without `sudo`, every call with
`--unshare-net` or `--unshare-all` ends with:

```
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
```

`sudo` inside `systemd-run --user --scope` **works** (checked live) and **does not
disable** any system protection: `bwrap` creates the namespace with real root
privileges, so the restriction on *un*privileged namespaces simply does not apply to it.
The isolation inside the sandbox is identical.

**Four flags worth justifying:**

| Flag | Without it |
| :-- | :-- |
| `--unshare-all` | the code sees your processes and has a network |
| `--clearenv` | ⚠️ **`ANTHROPIC_API_KEY` lands in the sandbox**. This is the most common leak |
| `--new-session` | the `TIOCSTI` attack: injecting characters into your terminal |
| `systemd-run` with limits | `bwrap` **does not limit resources**; an infinite loop eats the machine |

> ⚠️ **`bwrap` has no resource limits, and this is its most overlooked gap.** Namespaces
> isolate *visibility*, not *consumption*. Without `systemd-run`, a single
> `while True: []` takes the CPU, and `[0]*10**10` takes the RAM, and your gateway dies
> together with the whole fleet.

---

## 3. Rung 2: a rootless container

```bash
# podman: no daemon, no root: the right choice when you need an image
podman run --rm \
  --network none \
  --read-only \
  --tmpfs /tmp:rw,size=256m,noexec \
  --memory 1g --cpus 2 --pids-limit 64 \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --security-opt seccomp=/etc/osa/seccomp.json \
  --user 65534:65534 \
  -v "$ARCHIWUM:/archiwum:ro,Z" \
  -v "$OBSZAR:/praca:rw,Z" \
  osa-runtime:1.0 python3 /praca/_program.py
```

| When it is worth moving from `bwrap` to a container | When it is not |
| :-- | :-- |
| You need specific dependencies (OCR, pandoc) | Python with the stdlib is enough |
| You want a reproducible image with an SBOM | You iterate quickly |
| You run someone else's code from an image | `bwrap` starts 20× faster |

⚠️ **`--cap-drop ALL` and `--security-opt no-new-privileges` are not optional.** A
container without them has the default set of capabilities, which, with a few known
vulnerabilities, is enough to escape. And still **the kernel is shared**: this is still
rung 2, not 3.

---

## 4. Rungs 3–4: gVisor and microVM

**gVisor** (`runsc`) is a Linux kernel implemented in user space. The sandboxed process
makes a `syscall`, which is intercepted by `runsc`, not by the host kernel.

```bash
# installation and running via podman
podman run --rm --runtime=/usr/local/bin/runsc --network none … osa-runtime:1.0
```

| Advantages | Costs |
| :-- | :-- |
| ⭐ A hole in the Linux kernel **cannot be exploited** from inside | I/O overhead 10–40% |
| Starts in milliseconds | some `syscall`s are not implemented |
| Works with podman/docker | ⚠️ a hole in gVisor itself remains possible |

**microVM** (Firecracker, libkrun) is real virtualization with a separate kernel, with a
start in under a second. This is the architecture used by Vercel, AWS Lambda and E2B:
**a full VM as the outer boundary, a microVM as the on-demand unit of execution**.

### 4.1 · Recommendation for your machine

```
Archivist, Steward            → rung 1 (bwrap + systemd-run)
code-mode from your own task  → rung 1
Researcher and anything from the network → rung 2 today, ⭐ rung 3 when the Researcher gets going for real
```

⚠️ **Don't build a microVM now.** Your real threat is **injection through content**
(ASI01/ASI06), not a kernel exploit. Injection passes through every rung of isolation
equally, because **it does not break the sandbox: it uses privileges you gave it
yourself**. You add rung 3 when the Researcher starts executing code downloaded from the
network; then it is necessary, not before.

⭐ **This is the most important sentence of this part. Isolation does not solve
injection.** The solution to injection is limiting privileges (§5) and a trust boundary
(part 16), not a stronger sandbox.

---

## 5. Network egress control

The Researcher needs a network. Giving it "a network" means giving it **the whole
internet plus your local network plus the cloud metadata**.

### 5.1 · The right pattern: no network + a proxy as the only exit

```
┌─ the Researcher's sandbox ─┐
│  --unshare-net             │   ⭐ zero network inside
│  unix socket ──────────────┼──►  proxy outside the sandbox
└────────────────────────────┘        │  allowlist of domains
                                      │  limit on requests and bytes
                                      │  a log of every request
                                      ▼  internet
```

```python
# $OSA/piaskownica/proxy.py
"""The Researcher's only exit. Allowlist, limits, log."""
DOZWOLONE = {"pl.wikipedia.org", "arxiv.org", "isap.sejm.gov.pl", "docs.python.org"}
LIMIT_ZADAN, LIMIT_BAJTOW = 60, 20 * 1024 * 1024

def wolno(url: str, licznik: dict) -> tuple[bool, str]:
    from urllib.parse import urlparse
    u = urlparse(url)
    if u.scheme != "https":
        return False, "HTTPS only."
    if u.hostname not in DOZWOLONE:
        return False, (f"The domain '{u.hostname}' is not on the allowlist. "
                       f"Allowed: {', '.join(sorted(DOZWOLONE))}. "
                       f"If you need another one, ask a human to add it.")
    if licznik["zadan"] >= LIMIT_ZADAN:
        return False, f"The limit of {LIMIT_ZADAN} requests per session is exhausted."
    if licznik["bajtow"] >= LIMIT_BAJTOW:
        return False, "The download data limit is exhausted."
    return True, ""
```

⚠️ **Pitfall P45 from course 1 returns and is crucial: `HTTP_PROXY` is a convention, not
enforcement.** The environment variable is **a suggestion for polite libraries**. Code
that opens a raw socket will ignore it. **The only enforcement is `--unshare-net`**:
since there is no network interface in the namespace, there is nothing to open.

### 5.2 · Block the metadata address, even locally

```bash
# 169.254.169.254 is the cloud metadata. On a laptop it is "unneeded",
# until you move the agent to a VPS and forget. Block it from the start.
sudo nft add rule inet filter output ip daddr 169.254.169.254 drop
```

---

## 6. Secrets: a layer outside the sandbox

OpenClaw had a documented problem here: **Secret Store values were not encrypted at
rest in version 2.0.** Learn from someone else's.

**Three rules:**

1. **A secret never enters the sandbox.** Not in the environment, not in a file, not in
   an argument (`ps` sees those).
2. **The agent does not get a secret; it gets a capability.** Not "you have an API key",
   but "you have a `wyslij_zapytanie()` function", which runs **outside** the sandbox.
3. **The secrets file has separate permissions and a different owner** than the agent
   process.

```python
# $OSA/sekrety.py: works ONLY in the gateway process, never in the sandbox
import pathlib, json, os, stat

def wczytaj() -> dict:
    p = pathlib.Path("~/.config/osa/sekrety.json").expanduser()
    m = p.stat().st_mode
    if m & (stat.S_IRWXG | stat.S_IRWXO):
        raise PermissionError(f"{p} has permissions {oct(m & 0o777)}. Required 0600: chmod 600 {p}")
    return json.loads(p.read_text())

def granica_zdolnosci(nazwa: str):
    """The agent calls this through the gateway. The secret does NOT cross the sandbox boundary."""
    ...
```

⭐ **Rule 2 is the one that really saves you.** When the agent is hijacked by an
injection, **there is nothing to exfiltrate**: it does not own the key, only the ability
to call one function through the gateway. The gateway sees every call and can reject it.
This is the same idea as the vault on the provider side: **a secret substituted on the
way out, never visible inside**.

---

## 7. FROM SCRATCH: three levels wired into the gateway

```python
# $OSA/piaskownica/poziomy.py
"""The isolation level follows from session trust (part 2), not from the agent's name."""
import subprocess, pathlib, os, shlex

POZIOMY = {
    "host":        {"szczebel": 0, "siec": True,  "zapis": ["~/dokumenty", "/tmp"]},
    "lekki":       {"szczebel": 1, "siec": False, "zapis": ["/tmp/praca"]},
    "piaskownica": {"szczebel": 1, "siec": False, "zapis": ["/tmp/praca"], "clearenv": True},
    "scisly":      {"szczebel": 2, "siec": False, "zapis": ["/tmp/praca"], "clearenv": True},
}

MAPA_ZAUFANIA = {          # ⭐ the one place where this is decided
    ("archiwista", "host"):        "lekki",
    ("archiwista", "piaskownica"): "piaskownica",
    ("gospodarz",  "host"):        "lekki",
    ("badacz",     "host"):        "scisly",     # ⚠️ the Researcher NEVER gets 'lekki'
    ("badacz",     "piaskownica"): "scisly",
}

def poziom_dla(agent: str, zaufanie_sesji: str) -> str:
    return MAPA_ZAUFANIA.get((agent, zaufanie_sesji), "scisly")   # P66: default to the NARROWEST

def uruchom(agent, zaufanie_sesji, polecenie, obszar="/tmp/praca", archiwum=None):
    p = POZIOMY[poziom_dla(agent, zaufanie_sesji)]
    if p["szczebel"] == 0:
        return subprocess.run(polecenie, shell=True, capture_output=True,
                              text=True, timeout=60)
    if p["szczebel"] == 1:
        env = dict(os.environ)
        if archiwum: env["ARCHIWUM"] = archiwum
        return subprocess.run(
            [str(pathlib.Path(os.environ["OSA"], "piaskownica/szczebel1.sh")),
             obszar, "bash", "-c", polecenie],
            capture_output=True, text=True, timeout=60, env=env)
    return _kontener(polecenie, obszar, archiwum)
```

⭐ **`MAPA_ZAUFANIA` is the only place in the whole system where it is decided how much
each party is allowed.** When in half a year you wonder "can the Researcher read
`~/dokumenty`", you look at one dictionary instead of searching the code. This is worth
more than elegance.

---

## 8. EXPERIMENT 10: escape attempts

⭐ **Don't trust a sandbox you have not tried to break.**

```bash
mkdir -p $OSA/testy/ucieczka && cd $OSA/testy/ucieczka
```

```python
# proby.py: every attempt MUST fail
PROBY = [
 ("read /etc/shadow",         "open('/etc/shadow').read()"),
 ("read SSH keys",            "open('/root/.ssh/id_rsa').read()"),
 ("read documents",           "open('/home/USER/dokumenty/umowa.txt').read()"),
 ("write outside the area",   "open('/home/USER/wlam.txt','w').write('x')"),
 ("write to /usr",            "open('/usr/bin/zle','w').write('x')"),
 ("TCP socket",               "import socket; socket.create_connection(('1.1.1.1',80),2)"),
 ("DNS",                      "import socket; socket.gethostbyname('example.com')"),
 ("cloud metadata",           "import urllib.request; urllib.request.urlopen('http://169.254.169.254/',timeout=2)"),
 ("host process list",        "import os; print([p for p in os.listdir('/proc') if p.isdigit()][:20])"),
 ("secret from environment",  "import os; print([k for k in os.environ if 'KEY' in k or 'TOKEN' in k])"),
 ("fork bomb",                "import os\nwhile True: os.fork()"),
 ("RAM exhaustion",           "x=[0]*10**10"),
 ("CPU loop",                 "while True: pass"),
 ("write via /proc/self",     "open('/proc/self/root/etc/passwd','w')"),
 ("privilege escalation",     "import subprocess; subprocess.run(['sudo','id'])"),
 ("escape via ../",           "open('../../../../etc/passwd').read()"),
]
```

```bash
for poziom in lekki piaskownica scisly; do
  python3 proby.py --poziom $poziom
done
```

| # | Attempt | `lekki` | `piaskownica` | `scisly` | Expected |
| --: | :-- | :-: | :-: | :-: | :-- |
| 1 | `/etc/shadow` | | | | ✗ everywhere |
| 3 | documents | | | | ✗ (⚠️ except for the Archivist via `/archiwum` ro) |
| 6 | TCP socket | | | | ✗ everywhere |
| 10 | secret from environment | | | | ✗ with `clearenv` |
| 11 | fork bomb | | | | ✗ with `TasksMax` |
| 12 | RAM exhaustion | | | | ✗ with `MemoryMax` |
| 13 | CPU loop | | | | ⚠️ **will not be blocked**, only limited by `CPUQuota` |

⚠️ **Row 13 is a lesson in itself.** `CPUQuota=200%` does not stop an infinite loop: it
**limits it to two cores**. Only the timeout in `uruchom()` stops it. Resource limits and
time limits are two different things, and **you need both**.

### 8.1 · The second measurement: the cost of isolation

| Operation | no isolation | `bwrap` | container | gVisor |
| :-- | --: | --: | --: | --: |
| Process start | ms | ms | ms | ms |
| Reading 100 files | ms | ms | ms | ms |
| A 5 s CPU program | s | s | s | s |

⚠️ **Prediction:** `bwrap` adds ~10–20 ms to the start and **almost nothing** to I/O. A
container ~200 ms. gVisor starts fast, but **I/O can be 10–40% slower**, and for an
agent reading hundreds of files this is noticeable. Measure before you decide.

---

## 9. EXERCISE

1. Implement `szczebel1.sh`, `poziomy.py` and the proxy with an allowlist.
2. Wire `poziom_dla()` into the gateway: **every** tool execution goes through this map.
3. Run all 16 attempts on the three levels. **Each one must fail.** Each one that goes
   through is a task to fix before part 13.
4. Expose to the Researcher a `pobierz(url)` tool that works **only** through the proxy,
   and check that there is no network interface in the sandbox:

```bash
python3 sesja-cli.py piaskownica badacz --diagnostyka
# expect:
#   level:           scisly (rung 2)
#   network inside:  NONE (--unshare-net)   ✓
#   egress:          proxy, 4 domains, 60 requests/session
#   write:           /tmp/praca (256 MB)
#   environment:     cleared, 0 secrets   ✓
#   limits:          1 GB RAM, 200% CPU, 64 tasks, 60 s
```

5. **Bonus task:** add three escape attempts of your own to `proby.py`. If any of them
   goes through, you have a real finding and you know something about your system that
   you did not know.

---

## 10. Pitfalls of this part

| ID | Pitfall | Symptom | How to avoid |
| :-- | :-- | :-- | :-- |
| **P99** | **Confusing a container with a sandbox** | "It's in Docker, so it's safe", and the kernel is shared | A container is rung 2. A kernel exploit goes through. For code from the network → gVisor or microVM |
| **P100** | **No resource limits with `bwrap`** | One loop eats the machine; the gateway and the whole fleet go down | `bwrap` does not limit. `systemd-run` with `MemoryMax`, `CPUQuota`, `TasksMax` **and** a timeout |
| **P101** | **Environment inherited into the sandbox** | `ANTHROPIC_API_KEY` visible to the agent's code; an injection carries it out | `--clearenv` + an explicit `--setenv`. Secrets across the capability boundary, never inside |
| **P102** | **`HTTP_PROXY` as network control** | Code with a raw socket ignores the proxy and goes wherever it wants | The only enforcement is `--unshare-net`. The proxy only **outside** the sandbox |
| **P103** | **Believing the sandbox protects against injection** | An agent in perfect isolation executes the attacker's command **with its own privileges** | Isolation limits the **blast radius**, it does not prevent the attack. Defence: privileges + a trust boundary (part 16) |

---

## 11. Checkpoint

```bash
cd $OSA
python3 testy/ucieczka/proby.py --poziom scisly --wymagaj-porazki-wszystkich \
  && echo "✓ all 16 attempts blocked at the strict level"
python3 -c "
from piaskownica.poziomy import poziom_dla
assert poziom_dla('badacz','host') == 'scisly',  'The Researcher NEVER gets the light level'
assert poziom_dla('nieznany','host') == 'scisly','default to the narrowest (P66)'
print('✓ trust map')"
ls -l ~/.config/osa/sekrety.json | grep -q '^-rw-------' && echo "✓ secrets 0600"
git add -A && git commit -m "part 10: isolation ladder, proxy, secrets, escape attempts"
```

- [ ] You know the five rungs and **what each one stops**, especially the "kernel exploit" row
- [ ] The isolation level follows from the **source of input**, not from the agent's name
- [ ] `bwrap` has `--clearenv`, `--new-session` and limits via `systemd-run`
- [ ] Network: `--unshare-net` inside, a proxy with an allowlist outside
- [ ] Secrets never cross the boundary: the agent gets a capability, not a key
- [ ] `MAPA_ZAUFANIA` is the only place for privilege decisions
- [ ] ⭐ **16 escape attempts, all blocked, isolation cost measured**
- [ ] ⭐ You understand that **isolation does not solve injection**: it limits the consequences

---

**Next: `11-SCHEDULING-PROACTIVITY.md`**: an agent that wakes up on its own, does
something sensible and **doesn't bother you when there is no reason to**.
