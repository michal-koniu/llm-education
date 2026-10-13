# Sources — what this course stands on

**Collected 23 September 2026.** Each entry notes **what from it went into the course and where**.

> ⚠️ **Everything here ages in months.** The agentic landscape in 2026 changes faster
> than the documentation can keep up. When you see a specific number in a part of the
> course (e.g. "85% context savings"), treat it as **someone else's measurement, to be
> repeated on your own setup** — not as a physical constant. That is why every part
> has an experiment.

---

## 1. OpenClaw — the main case study

You asked me directly to check this. I did — and it is the best-documented working
agentic system for learning architecture, because **all of its logic lives in readable
files, not in the model weights**.

| Source | What I took from it |
| :-- | :-- |
| [OpenClaw — Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) | History (WhatsApp relay → ClawdBot → Moltbot → OpenClaw, 30 January 2026), the security model and a **list of real incidents** — for part 16 |
| [ppaolo · OpenClaw System Architecture Overview](https://ppaolo.substack.com/p/openclaw-system-architecture-overview) | ⭐ The deepest description I found. Gateway on `127.0.0.1:18789`, session resolution, prompt assembly, a 6-phase message pipeline, policy precedence, hybrid vector+BM25 memory in SQLite — **the backbone of parts 2, 6, 12** |
| [Markaicode · OpenClaw Production Architecture](https://markaicode.com/architecture/openclaw-agent-architecture/) | The Gateway / Brain / Hands / Memory split — the naming I use in part 1 |
| [Capodieci · OpenClaw Workspace Files Explained](https://capodieci.medium.com/ai-agents-003-openclaw-workspace-files-explained-soul-md-agents-md-heartbeat-md-and-more-5bdfbee4827a) | `SOUL.md`, `AGENTS.md`, `MEMORY.md`, `HEARTBEAT.md` — **all of part 6** |
| [Blink · HEARTBEAT, SOUL and Memory Configuration Guide](https://blink.new/blog/openclaw-heartbeat-soul-memory-configuration-guide-2026) | The `HEARTBEAT_OK` pattern suppressed by the gateway — **the core of part 11** |
| [Bibek Poudel · How OpenClaw Works](https://bibek-poudel.medium.com/how-openclaw-works-understanding-ai-agents-through-a-real-architecture-5d59cc7a4764) | The cron-triggered agent loop as an architectural concept |
| [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) | Directory layout, plugin SDK, "an incoming message is untrusted" |
| [awesome-openclaw](https://github.com/SamurAIGPT/awesome-openclaw) · [awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents) | 162 ready-made `SOUL.md` configurations — comparison material for part 6 |

**What OpenClaw teaches best:** that an agent is an **infrastructure problem**, not a
prompt problem. Sessions, routing, sandboxes and memory are 90% of the work. The prompt
is 10%.

**What OpenClaw teaches by counter-example:** Secret Store values are **not encrypted
at rest** in version 2.0, and the sandbox for untrusted code is **not enabled by
default**. Cisco found real data exfiltration in third-party skills. That is not a
reason not to study it — it is **material for part 16**.

---

## 2. Peter Steinberger — a voice against the current

The author of OpenClaw. Worth reading not because they are right about everything, but
because **their theses are testable and run against the grain** of what the rest of the
market sells.

| Source | The thesis I take into the course |
| :-- | :-- |
| [Just Talk To It — the no-bs Way of Agentic Engineering](https://steipete.me/posts/just-talk-to-it) | ⭐ **"MCP and RAG are context poison."** GitHub MCP ≈ 23k tokens; a CLI costs zero, because the model already knows it and will read `--help`. Prompts of 1–2 sentences. 3–8 agents in parallel in one directory, atomic commits. **Blast radius** as a planning unit. Rejection of plan mode and subagents as "working around a broken system" — **part 9, partly 13** |
| [MCP Best Practices](https://steipete.me/posts/2025/mcp-best-practices.md) | A forgiving argument parser, no output on `stdio`, an error message that enables recovery, an `info` subcommand, a 300–500 line limit per file — **part 7** |
| [Loop engineering (post of 8 June 2026)](https://steipete.me/posts) | "Don't prompt agents. **Design loops that prompt agents**" — the motto of part 3 |
| [OpenClaw, OpenAI and the future](https://steipete.me/posts/2026/openclaw) | Context: the move to OpenAI, OpenClaw going to a foundation. The goal of "an agent my mom will use" |
| [Fast Company · How Peter Steinberger built OpenClaw](https://www.fastcompany.com/91550800/how-peter-steinberger-built-openclaw) | Background of its origin — a weekend project that grew |

> **How I read Steinberger in this course.** His "no MCP, no RAG, no subagents"
> position is **true for his case**: an experienced engineer, a frontier-class model,
> programming tasks, full trust in the machine. **Three of those four conditions do not
> hold for you.** That is why in parts 9 and 13 I put his theses next to a measurement
> and make you decide for yourself. That is a more important skill than choosing a side.

---

## 3. Anthropic — harness and context engineering

| Source | What I took from it |
| :-- | :-- |
| [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | ⭐ **All of part 3.** Initializer vs worker agent, `init.sh`, the progress file, a **feature list in JSON** against premature "done", git as memory, the session start sequence, the ban on deleting tests |
| [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | ⭐ **All of part 4.** The attention budget, context rot and its source in the transformer's n², the **altitude of the system prompt**, compaction "recall first, then precision", structured notes, just-in-time loading, subagents returning 1–2k tokens |
| [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) | Four criteria for "should you build an agent at all": complexity, value, feasibility, cost of error — **the opening of part 1** |

---

## 4. Code-mode — the biggest change of this year

| Source | What I took from it |
| :-- | :-- |
| [MCP Code Mode — Context Engineering for Efficient Tool Execution](https://medium.com/@amirkiarafiei/mcp-code-mode-context-engineering-for-efficient-tool-execution-in-llm-agents-c46e1ddf80ac) | A context reduction of ~94% by treating tools as discoverable code instead of static JSON |
| [Microsoft Agent Framework · CodeAct](https://learn.microsoft.com/en-us/agent-framework/agents/code-act) | The formal definition: `execute_code` as the place where the agent combines control flow, data transformation and tool orchestration **in a single step** |
| [code-mode (UTCP)](https://github.com/universal-tool-calling-protocol/code-mode) | A working library — the comparison in part 8 |
| [mcp-server-code-execution-mode](https://github.com/elusznik/mcp-server-code-execution-mode) | Execution in rootless containers — the link between parts 8 and 10 |
| [Glama · Code execution with MCP](https://glama.ai/blog/2025-12-14-code-execution-with-mcp-architecting-agentic-efficiency) | The argument for collapsing many model turns into one |

**Why this matters more to you than to anyone else:** a small local model generates
correct Python far more reliably than long, correct JSON with nested arguments.
Code-mode **shifts the burden from a format in which the model is weak to one in which
it is strong**. That is part 8 and one of the two most important chapters of the course.

---

## 5. Agent memory

| Source | What I took from it |
| :-- | :-- |
| [Wasowski · I compared 5 AI agent memory systems](https://medium.com/@wasowski.jarek/i-compared-5-ai-agent-memory-systems-across-6-dimensions-none-wins-6a658335ed0a) | ⭐ The number around which I built part 5: **Zep/Graphiti 71.2% vs Mem0 49% on LongMemEval** |
| [Atlan · Best AI Agent Memory Frameworks 2026](https://atlan.com/know/best-ai-agent-memory-frameworks-2026/) | Bi-temporality as the differentiator of the year: `valid_at` + `invalid_at` on every fact |
| [Graphlit · Survey of AI Agent Memory Frameworks](https://www.graphlit.com/blog/survey-of-ai-agent-memory-frameworks) | The distinction **memory vs context** — key to keeping parts 4 and 5 from merging |
| [Codepointer · Agent Memory Systems and Knowledge Graphs](https://codepointer.substack.com/p/agent-memory-systems-and-knowledge) | Letta/MemGPT: operating-system-style virtual memory, self-editable blocks, sleep-time compute |
| [MemGuard (arXiv 2605.28009)](https://arxiv.org/pdf/2605.28009) | Long-term memory poisoning — the entry to ASI06 in part 16 |

---

## 6. Agentic security

| Source | What I took from it |
| :-- | :-- |
| [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | ⭐ **The backbone of all of part 16.** ASI01–ASI10, published 9 December 2025, over 100 reviewers |
| [Cycode · OWASP Top 10 Agentic — categories broken out](https://cycode.com/blog/owasp-top-10-agentic-applications/) | Full names and descriptions of ASI01–ASI10 |
| [Teleport · Key Takeaways](https://goteleport.com/blog/owasp-top-10-agentic-applications/) | **72.4%** — how often one compromised MCP server dragged others down with it. The number driving the cascade exercise in part 13 |
| [Northflank · How to sandbox AI agents in 2026](https://northflank.com/blog/how-to-sandbox-ai-agents) | The isolation ladder: container → gVisor → microVM. **The VM as the outer boundary, the microVM as the unit of execution** — part 10 |
| [emirb · Your Container Is Not a Sandbox](https://emirb.github.io/blog/microvm-2026/) | Why a plain container is not enough for an agent writing its own code |
| [awesome-agent-runtime-security](https://github.com/bureado/awesome-agent-runtime-security) | Primitives: bubblewrap, Landlock, seccomp, KVM/libkrun, WASM |

---

## 7. Evaluation and observability

| Source | What I took from it |
| :-- | :-- |
| [Prefactor · Agent Benchmarks: tau-bench, SWE-bench, GAIA, pass^k](https://prefactor.tech/learn/agent-benchmarks) | ⭐ **"An agent's score changes more with the harness than with the model."** The opening thesis of part 14. Plus `pass^k` as a measure of reliability, not capability |
| [tau2-bench](https://github.com/sierra-research/tau2-bench) | Two-sided control: the user also invokes tools — the test-set pattern in part 14 |
| [Guideline-Grounded Evidence Accumulation (arXiv 2603.02798)](https://arxiv.org/pdf/2603.02798) | ⭐ **External verification.** Self-reflection has a self-confirming bias, because the judge sits in the same trajectory state as the author. The signal has to arise in an isolated context |
| [Stackviv · Agent Reflection](https://stackviv.ai/blog/reflection-ai-agents-self-improvement) | The three-step loop generate → critique → fix. The "fixed mindset" problem and critics with different personalities |
| [OpenTelemetry GenAI Semantic Conventions — overview](https://twistag.com/thinking/ai-agent-observability) | Agent, workflow, tool and model spans; latency and token metrics; the warning that `gen_ai.*` attributes have Development status and may change without a major bump — **part 15** |
| [Langfuse vs Arize Phoenix](https://qaskills.sh/blog/langfuse-vs-arize-phoenix) | Choosing a self-hosted tool for part 15 |

---

## 8. Protocols

| Source | What I took from it |
| :-- | :-- |
| [MCP · Specification 2026-07-28](https://blog.modelcontextprotocol.io/posts/2026-07-28/) | ⭐ **A stateless core.** The shift from a bidirectional stateful protocol to request/response. MRTR instead of permanently open streams. Authorization hardening: RFC 9207, moving away from DCR towards CIMD — part 9 |
| [The 2026 MCP Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) | The direction: from tool integrations to communication between agents |
| [Agent2Agent — Wikipedia](https://en.wikipedia.org/wiki/Agent2Agent) | A2A under the Linux Foundation, 100+ companies. The split of roles: **MCP connects an agent to tools, A2A connects agents to each other** |
| [Agent Context Protocol in 2026: MCP, ACP, A2A](https://www.puppyone.ai/en/blog/agent-context-protocol) | A comparison of three protocols — the table in part 9 |

---

## 9. Local models and engines

| Source | What I took from it |
| :-- | :-- |
| [LLM Configurator · Local LLM Tool Calling 2026](https://llmconfigurator.com/en/guides/coding-agents/tool-calling-local-models) | ⭐ A hard number for part 7: **90%+ syntactically correct calls on simple tasks, but 80–90% end-to-end on multi-step ones** — selection and argument errors accumulate |
| [PromptQuorum · Best Local Models for Tool Calling 2026](https://www.promptquorum.com/power-local-llm/best-local-models-tool-calling-2026) | GLM-4.5-Air, Qwen3-Coder-30B-A3B, Qwen3-30B-A3B-Thinking as the agentic front-runners |
| [InsiderLLM · Function Calling Local LLMs](https://insiderllm.com/guides/function-calling-local-llms/) | The `qwen3_coder` parser in vLLM and SGLang; VRAM usage per model |
| [Yotta Labs · vLLM vs SGLang in 2026](https://www.yottalabs.ai/post/vllm-vs-sglang-which-inference-engine-should-you-use-in-2026) | When to move from `llama-server` to vLLM — with parallel fleet sessions (part 13) |
| [ROCm · vLLM inference and serving](https://rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/inference/benchmark-docker/vllm.html) | The state of AMD support. ⚠️ **AITER and the official tests target MI300X/MI350, not RDNA4** — in your setup everything needs measuring, not believing |

---

## 10. Frameworks — for comparison, not for imitation

| Source | Role in the course |
| :-- | :-- |
| [LangChain · The best AI agent frameworks in 2026](https://www.langchain.com/resources/ai-agent-frameworks) | A map of the terrain; LangGraph as a graph with typed state |
| [Morphllm · 8 SDKs Compared + Claude Agent SDK Primitive Reference](https://www.morphllm.com/ai-agent-framework) | A comparison of primitives — for the "Yours vs theirs" tables |
| [OpenAgents · Open-source agent frameworks compared](https://openagents.org/blog/posts/2026-02-23-open-source-ai-agent-frameworks-compared) | The split into vendor SDKs vs independent ones |
| [Langfuse · Comparing Open-Source AI Agent Frameworks](https://langfuse.com/blog/2025-03-19-ai-agent-comparison) | Criteria for evaluating a framework |

**A note on smolagents:** agents that generate code instead of JSON **reduce the number
of model calls by ~30%** and have sandboxed execution built in. It is the closest
ready-made implementation of what you build in part 8 — and that is why it is the
reference point there.

---

## 11. What is deliberately not on this list

- **Video courses and paid bootcamps.** I checked several; they all teach a framework,
  none a mechanism. You have them for free in those frameworks' documentation.
- **Model benchmarks.** They age in weeks and do not answer your question, because your
  bottleneck is the harness, not the model (see §7, the first entry).
- **"Top 10 agent frameworks" articles.** There are a thousand of them, they say the
  same thing and none of them measures. Where I needed a comparison, I took it from the
  primary documentation.

---

## How to verify this after me

Every claim in the course marked **⚠️ to be checked** is one that I **did not measure
on your hardware** — because I do not have continuous access to it. All other numbers
come either from this list (in which case there is a link) or from a measurement
described in the text.

When a number from this list does not match your measurement — **your measurement wins,
and you correct the course**. The files are yours.
