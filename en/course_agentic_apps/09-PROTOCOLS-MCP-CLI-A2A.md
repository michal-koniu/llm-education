# Part 9 · Protocols and integrations — MCP, CLI, A2A

**Level:** ⭐⭐⭐ · **Time:** ~4 h · **Requires:** parts 7 and 8
**Produces:** the same capability as an MCP server and as a CLI, a measured comparison, a written decision

---

## 0. A dispute you settle by measurement

Peter Steinberger, the author of OpenClaw:

> MCP and RAG are **context poison**. The GitHub MCP server is about **23k tokens**.
> And I can simply call the CLI by name: the CLI shows `--help`, and the context has
> the full information on how it works. **For zero.**

The MCP market at the same time: hundreds of servers, support in all the major tools,
the specification rewritten in July 2026.

**Both sides are right in their own context.** This part is not meant to convince you of
one of them. It is meant to give you **a number from your own machine**, so that you
settle it yourself.

---

## 1. What a protocol costs

Break the cost of an integration into three items. Almost nobody does this, and that is
where inconclusive disputes come from.

| Item | MCP | CLI | Function in code (part 8) |
| :-- | :-- | :-- | :-- |
| **Fixed context cost** (every turn) | ⚠️ schemas of all tools | ⭐ ~1 line | ⭐ ~1 line in `pomoc()` |
| **Discovery cost** (once) | zero: the schemas are already there | `--help`, ~300–1500 tok. | `pomoc()`, ~400 tok. |
| **Call cost** | JSON conforming to the schema | a command line | a function call |
| Interoperability | ⭐⭐ with every MCP client | ⭐ with every shell | only your system |
| Authentication | ⭐ built in (OAuth, CIMD) | yours | yours |
| Runtime discovery | ⭐ yes | ✗ | ✗ |

⭐ **The key distinction: fixed cost vs discovery cost.** MCP pays **in every turn** for
tools the agent will not use in that turn. A CLI pays **once**, when the agent actually
wants to learn about it. With 40 turns and 20 tools the difference is enormous, and this
is exactly Steinberger's argument, expressed in units.

⚠️ **But that is not the whole truth.** Since the **2026-07-28** specification, MCP has
on-demand tool search, which flattens the fixed cost (a reported ~85% reduction on MCP
evaluations). The "23k tokens" claim describes a server configured the old way, with the
full catalogue in the prompt. **Measure your configuration, not someone else's.**

---

## 2. MCP in 2026: what changed

The **2026-07-28** specification is a major rework, and four changes are worth knowing:

| Change | What it means in practice |
| :-- | :-- |
| ⭐ **Stateless core** | From a stateful bidirectional protocol → request/response. **An MCP server becomes plain HTTP**: easier to write, test and expose |
| **MRTR** (Multi Round-Trip Requests) | Sampling and elicitation without a permanently open stream. No more long-lived SSE where it is not needed |
| **Authorization hardening** | RFC 9207 (issuer validation), moving away from DCR in favour of CIMD |
| **Tasks, MCP Apps, EMA** | Extensions: long operations, UI, organization-level management |

**What follows for you.** The stateless core is good news: an MCP server in plain Python
with no dependencies is now a few dozen lines. Everything else (authorization, EMA)
solves problems that you **do not have in a loopback system**.

---

## 3. FROM SCRATCH: the same capability, three interfaces

The test capability: **search in a document archive**. You will write it once as logic,
and then expose it three ways.

### 3.1 · The logic (shared)

```python
# $OSA/zdolnosci/archiwum.py
"""The logic. It knows nothing about protocols, and that is the point."""
import pathlib, re

def szukaj(korzen: str, fraza: str, limit: int = 20) -> list[dict]:
    """Searches for a phrase in text documents. Returns hits with context."""
    out = []
    for p in sorted(pathlib.Path(korzen).rglob("*.txt")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(re.escape(fraza), t, re.I):
            a, b = max(0, m.start() - 60), min(len(t), m.end() + 60)
            out.append({"plik": str(p.relative_to(korzen)),
                        "pozycja": m.start(),
                        "kontekst": t[a:b].replace("\n", " ")})
            if len(out) >= limit:
                return out
    return out
```

### 3.2 · Variant A: CLI

```python
#!/usr/bin/env python3
# $OSA/zdolnosci/archiwum-cli.py
"""Searches for a phrase in the document archive.

USAGE:
  archiwum-cli.py szukaj PHRASE [--limit N] [--json]
  archiwum-cli.py info

EXAMPLES:
  archiwum-cli.py szukaj "termin płatności" --limit 5
  archiwum-cli.py szukaj Orange --json

OUTPUT:
  Default:   file:position  context
  With --json:  a list of objects {plik, pozycja, kontekst}

Exit code 0 = found, 1 = no hits, 2 = usage error.
"""
import sys, json, os
from archiwum import szukaj

def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return 2
    if a[0] == "info":                                  # ← Steinberger's rule
        print(json.dumps({"wersja": "1.2.0",
                          "korzen": os.environ.get("ARCHIWUM", "~/dokumenty"),
                          "gotowe": os.path.isdir(os.path.expanduser(
                              os.environ.get("ARCHIWUM", "~/dokumenty")))}))
        return 0
    if a[0] != "szukaj" or len(a) < 2:
        print(__doc__, file=sys.stderr); return 2

    fraza = a[1]
    limit = int(a[a.index("--limit") + 1]) if "--limit" in a else 20
    w = szukaj(os.path.expanduser(os.environ.get("ARCHIWUM", "~/dokumenty")), fraza, limit)
    if "--json" in a:
        print(json.dumps(w, ensure_ascii=False, indent=1))
    else:
        for t in w:
            print(f'{t["plik"]}:{t["pozycja"]}  …{t["kontekst"]}…')
    if not w:
        print(f"No hits for '{fraza}'.", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

⭐ **The docstring *is* the documentation for the model.** The agent runs
`archiwum-cli.py --help`, gets 25 lines and **knows everything**: the syntax, examples,
output format, exit codes. This is the whole mechanism Steinberger talks about, and it
is surprisingly cheap.

The `info` subcommand is his rule from the MCP Best Practices: the agent must be able to
**diagnose the tool itself**, without asking you.

### 3.3 · Variant B: an MCP server (stateless)

```python
# $OSA/zdolnosci/archiwum-mcp.py
"""An MCP server, stateless core (2026-07-28). Plain HTTP, zero dependencies."""
import json, os, http.server, socketserver
from archiwum import szukaj

NARZEDZIA = [{
    "name": "archiwum_szukaj",
    "description": ("Searches for a phrase in the archive of text documents. "
                    "Returns a list of hits with 60 characters of context on each side. "
                    "When there are no hits, it returns an empty list, not an error."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "fraza": {"type": "string", "description": "The text to search for, no regular expressions."},
            "limit": {"type": "integer", "description": "Max hits. Defaults to 20.", "default": 20},
        },
        "required": ["fraza"],
    },
}]

class MCP(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        z = json.loads(self.rfile.read(n) or b"{}")
        m, ident = z.get("method"), z.get("id")

        if m == "initialize":
            w = {"protocolVersion": "2026-07-28",
                 "capabilities": {"tools": {}},
                 "serverInfo": {"name": "archiwum", "version": "1.2.0"}}
        elif m == "tools/list":
            w = {"tools": NARZEDZIA}
        elif m == "tools/call":
            p = z["params"]["arguments"]
            wynik = szukaj(os.path.expanduser(os.environ.get("ARCHIWUM", "~/dokumenty")),
                           p["fraza"], p.get("limit", 20))
            w = {"content": [{"type": "text",
                              "text": json.dumps(wynik, ensure_ascii=False)}],
                 "isError": False}
        else:
            return self._wyslij({"jsonrpc": "2.0", "id": ident,
                                 "error": {"code": -32601, "message": f"unknown method {m}"}})
        self._wyslij({"jsonrpc": "2.0", "id": ident, "result": w})

    def _wyslij(self, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers(); self.wfile.write(b)

    def log_message(self, *a): pass          # P63: silence on stdout

if __name__ == "__main__":
    with socketserver.TCPServer(("127.0.0.1", 18790), MCP) as s:
        s.serve_forever()
```

> 💡 **Notice how little code there is here.** The stateless core of 2026-07-28 reduces
> an MCP server to an ordinary JSON-RPC endpoint. The earlier version required SSE and
> connection management. **This is a real change for the better**, worth appreciating
> regardless of whether you end up using MCP.

### 3.4 · Variant C: a function in the API (part 8)

```python
def szukaj_w_archiwum(fraza: str, limit: int = 20) -> list[dict]:
    """Searches for a phrase in the archive. Returns [{plik, pozycja, kontekst}].
    Empty list = no hits (not an error). The phrase is literal, no regex."""
    return szukaj(KORZEN, fraza, limit)
```

---

## 4. EXPERIMENT 9: measure the three variants

**Hypothesis:** with a small number of capabilities, the CLI and the function win on
fixed cost, and MCP starts to pay off only when you need interoperability or
authentication.

### 4.1 · Measurement 1: fixed context cost

```bash
mkdir -p $OSA/pomiary/protokoly && cd $OSA/pomiary/protokoly

# How many tokens does merely making the capability available to the model take?
python3 policz_tokeny.py --wariant cli    # a line: "you have archiwum-cli.py, use --help"
python3 policz_tokeny.py --wariant mcp    # the full inputSchema in the prompt
python3 policz_tokeny.py --wariant api    # a line in pomoc()
```

| Capabilities | CLI | MCP (schemas) | API (code-mode) |
| --: | --: | --: | --: |
| 1 | | | |
| 5 | | | |
| 20 | | | |

⚠️ **Prediction:** the CLI and the API grow ~linearly at ~15 tokens per capability. MCP
grows at ~150–250 tokens per tool. At 20 capabilities I expect **~300 vs ~4000 tokens**.
This is Steinberger's thesis in miniature, and if it comes out that way, you have it
confirmed on your own hardware.

### 4.2 · Measurement 2: usage success

20 tasks requiring a search, 3 runs each:

| Variant | Correct /20 | Avg turns | Avg tokens | Time |
| :-- | --: | --: | --: | --: |
| CLI (via `powloka`) | | | | |
| MCP | | | | |
| API (code-mode) | | | | |

⚠️ **Prediction:** MCP will have the **highest first-use accuracy** (the schema is in
the prompt, the model does not have to guess), but the highest cost. The CLI needs one
turn for `--help` **on first use in a session**, after which it is equally effective and
cheaper.

⭐ **This is the core of the trade-off and worth remembering: MCP buys first-shot
accuracy for a fixed cost paid in every turn.** With short sessions that pays off. With
long ones it does not.

### 4.3 · Measurement 3: can the model handle `--help`

This is the **hidden assumption of Steinberger's thesis**, and with local models it need
not hold at all:

```bash
python3 test_help.py --model gpt-oss-20b --narzedzi 8
# For 8 unfamiliar CLIs: after --help, does the model use them correctly on the first try?
```

| Model | Correct use after `--help` /8 |
| :-- | --: |
| `gpt-oss-20b` | |
| `qwen3-32b` | |

⚠️ **This is the most interesting measurement in this part.** Steinberger uses frontier
models, which read `--help` flawlessly. If `gpt-oss-20b` scores below ~6/8, his thesis
**does not hold for you in this form**, and the right conclusion is either a schema in
the prompt (MCP) or an API with docstrings (part 8), which is cheaper than both.

---

## 5. When a protocol earns its keep

| Situation | Choice | Why |
| :-- | :-- | :-- |
| A capability only for your agent | ⭐ **a function in the API** | zero overhead, a docstring is enough |
| A capability you also use from the terminal | ⭐ **CLI** | one source of truth, you and the agent alike |
| A capability for **other clients** (an IDE, someone else's agent) | ⭐ **MCP** | interoperability is its only real argument |
| An external service with OAuth | ⭐ **MCP** | you get authentication for free |
| Over 25 capabilities | ⭐ **code-mode** (part 8) | see measurement 4.1 |
| A capability discovered at runtime | **MCP** | the only one that has it |

⭐ **The default rule for your system:** **a function in the API → a CLI when useful to a
human → MCP only when someone from outside is to use it.** The reverse order ("let's
start with MCP, because it's the standard") costs you tokens in every turn for an
interoperability you do not use.

> ⚠️ **And a security argument that outweighs performance.** Every MCP server is a
> **supply chain element** (ASI04): code that you read through someone else's eyes, with
> access to your tools. A statistic from OWASP: one compromised server affected the
> operation of subsequent ones in **72.4%** of cases. A function you wrote yourself does
> not have this property. **With equal results, choose what you do not have to trust.**

---

## 6. A2A: a protocol between agents

MCP connects an agent to tools. **A2A** (Agent2Agent, under the Linux Foundation, 100+
companies) connects agents to each other.

| | MCP | A2A |
| :-- | :-- | :-- |
| Connects | agent ↔ tool | agent ↔ agent |
| Model | function call | task delegation |
| State | stateless (since 2026-07) | long-running tasks |
| Discovery | list of tools | an "Agent Card" with skills |

**Do you need A2A?** In your system, **no, and for a long time**. Three agents in one
process communicate by a function call, which is orders of magnitude cheaper and **has
no attack surface**.

A2A starts to make sense exactly when:

- the agents run in **separate processes or machines**, **and**
- they belong to **different owners** (otherwise your own RPC is enough), **and**
- they must **discover each other dynamically**.

⚠️ **Before you touch A2A, read ASI07 (insecure inter-agent communication) from part
16.** A protocol between agents is a **new trust boundary**, and most of the
implementations I have seen treat a message from "another agent" as trusted. This is
the same mistake as treating content from a web page as a command.

In part 13 you will build communication between your agents. You will do it through a
function call with an explicit trust boundary, **and that is the right choice** as long
as all the agents are yours.

---

## 7. EXERCISE: a decision in writing

1. Implement all three variants of the "search the archive" capability.
2. Run the three measurements from §4 on both models.
3. Write `decyzje/0003-protokoly.md` in the ADR format from part 1, with **numbers from
   your measurement**, not from this course.
4. Carry out the decision: delete the variants you did not choose. **Maintaining three
   interfaces to one capability is a guaranteed divergence.**

```markdown
# ADR 0003 · Integration protocols

## Decision
By default: a function in the API (code-mode). A CLI for capabilities also used from the terminal.
MCP: <your decision here>.

## The measurement I rely on
| Capabilities | CLI | MCP | API |
|---|---|---|---|
| 20 | ___ tok. | ___ tok. | ___ tok. |

Accuracy after --help, gpt-oss-20b: ___/8.

## How I will know it was a bad decision
When I want to use my capabilities from someone else's client: then MCP stops being
a cost and becomes the only way.
```

---

## 8. Pitfalls of this part

| ID | Pitfall | Symptom | How to avoid |
| :-- | :-- | :-- | :-- |
| **P95** | **Accepting the "23k tokens" figure without checking your own configuration** | You reject MCP on the basis of someone else's measurement from before the specification change | Measure your own (§4.1). Since 2026-07 MCP has on-demand tool search |
| **P96** | **Assuming the model will handle `--help`** | The CLI thesis assumes a frontier model; a small one loses the syntax | Measurement 4.3. Below ~6/8, the CLI loses for you |
| **P97** | **An MCP server as a trusted element of the system** | Someone else's code with access to your tools; a cascade in 72.4% of cases | An MCP server = supply chain (ASI04). You read it or you don't install it |
| **P98** | **Three interfaces to one capability maintained in parallel** | A fix in the CLI, MCP keeps the old logic, the agent gets different results | One logic, **one** exposure. The rest deleted after measurement |

---

## 9. Checkpoint

```bash
cd $OSA/zdolnosci
./archiwum-cli.py --help | head -3            && echo "✓ the CLI documents itself"
./archiwum-cli.py info                        && echo "✓ info subcommand"
python3 archiwum-mcp.py & sleep 1
curl -s -X POST localhost:18790 -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  | python3 -c "import json,sys; print('✓ MCP:', json.load(sys.stdin)['result']['tools'][0]['name'])"
test -s $OSA/decyzje/0003-protokoly.md && echo "✓ ADR with your own numbers"
git -C $OSA add -A && git -C $OSA commit -m "part 9: protocols, measurement, ADR"
```

- [ ] You understand the cost split: fixed (every turn) vs discovery (once)
- [ ] You know what the MCP 2026-07-28 specification changed
- [ ] You wrote the same capability as a CLI, MCP and a function
- [ ] The CLI documents itself via `--help` and has an `info` subcommand
- [ ] ⭐ **You measured the fixed cost of all three at 1, 5 and 20 capabilities**
- [ ] ⭐ **You checked whether your model can handle `--help`**: a precondition of the CLI thesis
- [ ] You know when A2A makes sense, and that for you it does not yet
- [ ] You have ADR 0003 with your own numbers and a falsification condition

---

**Next: `10-PRODUCTION-SANDBOX.md`**: the isolation ladder from `bwrap` to microVM, and
what each rung really stops.
