# 04 · How to talk to the fast model — browser, terminal, agent applications

After deployment ([02](02-DEEPSEEK-DEPLOYMENT.md)) the model is available under the same name as before (`deepseek`, `deepseek-v4`, `deepseek-v4-flash-0731`…),
so **no client requires changes** — it just works faster. Everything goes through `llama-swap` (port 8080), which exposes an OpenAI-compatible API.

> **Verified vs. unverified.** I checked: availability of the interfaces below, streaming, tool invocation via `/v1/chat/completions`,
> operation of the `dschat.py` client. I did **not** run OpenClaw or any other agent on this model — the section about it is conclusions from my measurements and a review of
> [assistants](../ai-assistants/01-PROFILES.md#1-openclaw), not a usage report.

## 1. Browser

| Address | What it is |
|---|---|
| `http://<machine-address>:8080/ui/` | `llama-swap` interface: model list, logs, **Playground** tab (chat with the selected model) |
| `http://<machine-address>:8080/upstream/deepseek-v4-flash-0731/` | built-in `llama-server` interface (chat, sampling settings) |

In Playground select the model `deepseek-v4-flash-0731` (or the alias `deepseek`). What's worth knowing:

- **The first request after idle takes ~2 minutes** — `llama-swap` releases the model after 10 min (`ttl: 600`), and tensor mode loads in ~108 s. Subsequent ones are immediate.
  Want it "always hot"? Raise `ttl` in `config.yaml` (e.g., 3600) — at the cost of VRAM occupied by the model when you're not using it.
- The model **"thinks" first** — in the chat you'll see the reasoning phase, then the answer. That's normal, and those tokens also count toward tok/s.
- **The speed you see depends on load**: 1 agent ≈ 50 tok/s, 2 in parallel ≈ 35 each. There are only **2 slots** — a third request waits in the queue.
  If a long test (e.g., a quality benchmark) is running in parallel, interactive conversation will be slower.
- I verified streaming from a client (as in chat): first token after ~1–6 s, then smooth; on an idle machine, without contention, expect ~50 tok/s.

## 2. Terminal — `dschat.py`

No dependencies (pure Python standard library), in the [tools/](tools/README.md) directory:

```bash
export LLAMA_SWAP_URL=http://<machine-address>:8080       # from another computer; locally defaults to localhost:8080
python3 dschat.py                                        # interactively (/reset, /think, /exit)
python3 dschat.py "Explain what MoE is in 3 sentences"
echo "Summarize this text: ..." | python3 dschat.py -       # prompt from a pipe
python3 dschat.py --no-think "Translate: ..."          # without "thinking" (faster, shorter — for simple tasks)
python3 dschat.py --show-thinking "..."                  # also show the model's reasoning
```

After each response you see server counters, e.g., `[91 tokens, 29.2 tok/s, draft 59/96, 1.0 s to 1st token]` — generation tok/s, how many draft tokens were accepted,
time to first token. (The value 29 comes from a moment when the GPU was simultaneously handling two other tasks.)

Without tools, with plain `curl` (streaming):

```bash
curl -N http://<machine-address>:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{
  "model": "deepseek", "stream": true, "temperature": 0.3,
  "messages": [{"role": "user", "content": "Write a haiku about GPU memory."}]}'
```

**Do not run `llama-cli` directly on the same GPUs** while `llama-swap` holds the model — VRAM is full. If you need `llama-cli`, first release the model
in `llama-swap` (it has an endpoint for releasing models — check its documentation; I didn't test this) or use a different model via `llama-swap`.

## 3. Agent applications (e.g., OpenClaw)

Any OpenAI-compatible client is configured the same way:

| Setting | Value |
|---|---|
| base URL | `http://<machine-address>:8080/v1` |
| model | `deepseek` (alias) |
| API key | any non-empty string (the server does not check it) |
| temperature | **0–0.3** for tool calls and JSON (higher draft acceptance and more stable results; the server-side 1.0 is only the default) |
| context window | **≤ ~90,000 tokens** (the slot has 98,304) |
| `max_tokens` | large (≥ 2000) — the model "thinks" and that consumes the limit; with a small value you get an empty response |

What this means for the agent (conclusions from my measurements, not tested on OpenClaw):

1. **Tool calls are exactly what this setup does best**: 54–62 tok/s with draft acceptance of 0.8–0.95. I verified that `llama-server` with `--jinja` returns
   correct `tool_calls` (e.g., `read_file` with JSON arguments) — in my review of assistants, OpenClaw warns that the `/v1` endpoint of *Ollama* breaks tool calls, but that is a different server.
   **Test your harness on a few calls** before trusting it — this warning also applies to "silently dropping tool calls" from the harness review.
2. **Stable prompt start.** The harness review describes a pitfall: a variable prompt start (e.g., a timestamp at the top) destroys the prompt cache. With a prefill of ~700 tok/s, a cache miss
   on a 10,000-token prompt costs ~14 s every time. Keep the system prompt and tool definitions at the beginning and unchanged.
3. **Two parallel agents is the optimum.** 2 slots × ~35 tok/s = 63 tok/s combined. A third agent waits. For several subagents, it is better to queue them than to launch them all at once.
4. **Long contexts cost prefill, not generation**: this setup is fast at writing and ~25% slower at reading than without a draft. For "read thousands of tokens and answer in one sentence" tasks,
   use the `deepseek-v4-flash-0731-nospec` model (the same model without a draft).
5. **Too small `max_tokens`** with a "thinking" model yields an empty response — the agent may interpret that as a failure.

## 4. Security — read this before connecting an agent

My `llama-swap` listens on **all interfaces and has no password**, and the models start with `--agent`, which enables the built-in `llama-server` tools — including **shell command
execution** (`exec_shell_command`) with the privileges of the user who started the server. That is how the note in my configuration describes it. **I have not checked** whether this can be abused
from the network (the tools are intended for the built-in web interface), but I assume the worst: anyone who can reach port 8080 can try.
Before connecting an agent that reads untrusted content (email, web pages), decide: a firewall restricting the port to a single address, a reverse proxy with authentication,
or disabling `--agent` in entries that do not need it. Sandbox rules: [course 1, part 7](../course_local_models/07-SANDBOX-SECURITY-MONITORING.md).
