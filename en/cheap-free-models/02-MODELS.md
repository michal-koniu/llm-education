# Which models are really at least as smart as DeepSeek-V4-Flash (October 2026)

This file is about **models, not providers**. The question is simple: my local rig runs DeepSeek-V4-Flash-0731. Which
models that I can reach cheaply or for free online are at least that smart, and which "free" offers only look like an
upgrade? Provider details (signup, limits, data terms) live in [01-PROFILES.md](01-PROFILES.md). How to wire the models
into an agent is in [03-AGENTIC-USE.md](03-AGENTIC-USE.md).

**AA** in this file means the **Artificial Analysis Intelligence Index v4.3.2, as of 13 Oct 2026** (a third-party
measurement). **Vals** means the independent Vals.ai harness, which runs every model through the same setup. Numbers
from model makers are marked *(vendor claim)*. Prices are USD per 1M tokens (input / output) as seen on 13 Oct 2026.

## 1. The shortest answer

- **The bar is AA 34**, the score of DeepSeek-V4-Flash-0731 at max effort. The bar on hard terminal agents is
  **Vals Terminal-Bench 4.0 = 18.7**.
- **Clearly above the bar and cheap (open weights):** MiMo-V2.6-Pro (AA 46, USD 0.87 output), GLM-5.3 via third-party
  hosts (AA 45, from USD 1.88), Step 5 Preview (AA 44, USD 2.70, free promos), GLM-5.3-Flash (AA 42, from USD 0.15),
  DeepSeek V4.1-Flash (AA 39, from USD 0.18) and MiMo-V2.6-Flash (AA 38, USD 0.28).
- **Above the bar but closed:** Claude Haiku 5.5 (AA 43 at max), GPT-6 Luna (AA 38 at max) and Muse Spark 1.3
  Contributor (AA 45 at its highest allowed effort, but **Meta trains on your prompts**). These are proprietary APIs, so no local fallback exists.
- **The best agent model per dollar is GLM-5.3-Flash.** It scores Vals TB4.0 37.4, twice the bar, at USD 0.50 output
  on Z.ai.
- **AA alone misleads for agents.** GPT-6 Luna (AA 38) and DeepSeek V4-Pro-0813 (AA 36) both fall **below** the bar on
  Vals TB4.0 (13.6 and 14.1).
- **The well-known free models are below the bar.** Inkling, Inkling Small, Nemotron 3 Ultra, gpt-oss-120b,
  MiniMax-M3 and Kimi K2.6 all score AA 12 to 29.
- **Kimi K3 (AA 44) is the strongest open tool-use model, but it is not cheap.** Output costs USD 9.50 to 15
  everywhere, so it only makes sense through a flat plan.
- **Do not compare AA numbers across index versions.** The same 0731 model scored 50 in July and scores 34 today.

## 2. The bar: three "V4-Flash" checkpoints

"DeepSeek-V4-Flash" is three different things, and the bar moves a lot depending on which one you mean:

| Checkpoint | Released | Size | AA v4.3.2 (max) | Status |
|---|---|---|---|---|
| V4-Flash 0420 (preview) | 24 Apr 2026 | 284B total / 13B active | 24 | deprecated on AA |
| **V4-Flash 0731 (GA), my local model** | 31 Jul 2026 | 284B / 13B | **34** | deprecated on AA in favour of V4.1 |
| V4.1-Flash (new weights) | 10 Sep 2026 | 552B / 16B | 39 (25 without reasoning) | current |

All three are MIT-licensed with 1M native context. Two traps follow from this:

- **The online `deepseek-v4-flash` ID is no longer V4-Flash.** Since 10 Sep 2026, DeepSeek's own API routes the legacy
  names to `deepseek-flash`, which is V4.1-Flash. If I want the exact weights my rig runs, I have to use a third-party
  host. OpenRouter lists `deepseek/deepseek-v4-flash-0731` with 27 endpoints.
- **Older blog posts use the 0420 preview numbers.** The famous "SWE-bench Verified 79.0" and "SWE-bench Pro 52.6"
  belong to the preview *(vendor claim)*. For 0731, Vals measured SWE-bench Verified 88.8 *(third-party measurement)*.

**Why the AA index version matters.** AA has rescaled the index several times, so the same model gets very different
numbers depending on the version:

| Model | AA v4.0 (Apr 2026) | AA v4.1 (Jul 2026) | AA v4.3.2 (since 19 Sep 2026) |
|---|---|---|---|
| V4-Flash 0420 | 47 | 40 | 24 |
| V4-Flash 0731 | – | 50 | 34 |

The v4.3 rescale (7 Sep 2026) added Terminal-Bench 4.0 and replaced tau3-Banking with AutomationBench. The current
weights are Agents 30 %, Coding 20 %, Science 20 % and General 30 %. Any blog post that says "Inkling 41 vs V4 Flash 40"
uses an older version. **I only compare v4.3.2 numbers in this file.** If my rig ran the 0420 preview, the bar would be
24, and MiniMax-M3, Kimi K2.6, GLM-5.1 and both Inklings would clear it. It runs 0731, so they do not (section 7).

Other baseline numbers for 0731: Vals TB2.1 **67.0**, Vals TB4.0 **18.7**, Vals SWE-bench Verified 88.8, Vals
LiveCodeBench 87.3, Vals GPQA 89.9 *(third-party measurements)*. DeepSeek's own card claims TB2.1 82.7, DeepSWE 54.4
and Toolathlon-Verified 70.3 *(vendor claim)*. Non-thinking mode is much weaker: on the preview, HLE dropped from 35 to
8 and LiveCodeBench from 92 to 55 *(vendor claim)*. Run it with reasoning on.

## 3. Benchmarks: what is still alive in H2 2026

Most benchmarks that agent guides quote are **frozen**: no new models have been added for months.

| Benchmark | State on 13 Oct 2026 | Use it? |
|---|---|---|
| AA Intelligence Index v4.3.2 | live, covers almost every model | yes, as the main ranking |
| Vals Terminal-Bench 4.0 | live, 48 models | **yes, for hard agents** |
| Vals Terminal-Bench 2.1 | archived 28 Sep 2026, 76 models | yes, for models released before then |
| tbench.ai TB4.0 board | live, fewer models | as a cross-check |
| SWE-bench Verified (official) | last entries Feb 2026. Vals archived it 1 Sep 2026 as saturated | only for models already on it |
| BFCL V4 | last update 12 Apr 2026 | no, too old |
| tau2-bench | about Mar 2026 | no |
| SWE-Bench Pro public (Scale) | stale | no |
| LiveCodeBench, GPQA, MMLU-Pro (Vals) | archived 1 Sep 2026 | only as background |
| Terminal-Bench 2.0 (Vals) | archived 4 Jun 2026 | no, it is not comparable with 2.1 |

In H2 2026, vendors report Terminal-Bench 2.1/3.0/4.0, DeepSWE v1.1, Toolathlon-Verified, AutomationBench, MCP-Atlas
and Agents' Last Exam. Those vendor numbers are rarely run on the same harness.

**The gap between vendor and independent numbers is large.** On Terminal-Bench 2.1, vendors report about 10 to 20
points more than Vals measures:

| Model | TB2.1 *(vendor claim)* | TB2.1 Vals *(third-party measurement)* | Gap |
|---|---|---|---|
| DeepSeek V4-Flash 0731 | 82.7 | 67.0 | 15.7 |
| DeepSeek V4.1-Flash | 90.6 | 74.5 | 16.1 |
| GLM-5.3 | 88.2 | 71.5 | 16.7 |
| MiMo-V2.6-Pro | 89.9 | 67.8 | 22.1 |

The gap also runs the other way: DeepSeek reports TB4.0 7.0 for 0731, while Vals measures 18.7. **The rule is that I rank
models on AA plus the Vals columns only.** I use vendor numbers to describe a model's shape, not to rank it.

## 4. Main table: at or above the bar, and cheap

"Cheap" means at least one public route at or under about USD 3 output per 1M tokens, or free. The price is the
cheapest output price I saw on 13 Oct 2026. "OR" means an OpenRouter endpoint, and "–" means no score was published.
The bar model is in the first row.

| Model | AA | Vals TB4.0 | Vals TB2.1 | Native ctx | Licence / open | Released | Cheapest output (route) |
|---|---|---|---|---|---|---|---|
| DeepSeek V4-Flash 0731 (bar) | 34 | 18.7 | 67.0 | 1M | MIT, open | 31 Jul 2026 | 0.18 (DeepInfra FP8, OR) |
| Muse Spark 1.3 Contributor | 45 (xhigh; max not allowed) | 10.6 std / 24.8 Max | 72.3 std / 79.0 Max | 1M | proprietary, trains on prompts | 2 Sep 2026 | 0.20 (Meta Contributor); free on OpenCode Zen |
| MiMo-V2.6-Pro | 46 | 31.3 | 67.8 | 1M | MIT, open | 21 Sep 2026 | 0.87 (Xiaomi, DeepInfra FP8) |
| GLM-5.3 (max) | 45 | 38.9 | 71.5 | 1M | GLM-5.3 licence (restrictions), open | 18 Aug 2026 | 1.88 (Baidu FP8 / Inceptron FP4, OR); Z.ai 4.40 |
| Step 5 Preview | 44 | 31.8 | – | 1M | API only, weights promised 15 Oct 2026 | 20 Sep 2026 | 2.70 (StepFun); free on Kilo and OpenCode Zen |
| Claude Haiku 5.5 (max) | 43 | 36.4 | – | 1M | proprietary | 7 Oct 2026 | 0.50 (prompt up to 100K; 2.50 above) |
| GLM-5.3-Flash | 42 | 37.4 | 62.9 | 1M | MIT, open | 26 Aug 2026 | 0.15 (StreamLake FP8, OR); Z.ai 0.50 |
| Ling 3.1 Flash | 41 | – | – | 1M on AA, 262K on OR | proprietary for now, "weights soon" | 1 Oct 2026 | 0.225 (Novita, OR); free on Requesty, Kilo, OpenCode Zen |
| Gemini 3.8 Flash (high) | 41 | 19.7 | 81.3 | 1M | proprietary | 2 Sep 2026 | 1.875 batch; 3.75 standard; free tier about 20 RPD |
| Qwen3.8-Flash-Next | 40 | – | – | 262K | Qwen Community Licence 1.0, open | 26 Aug 2026 | 0.47 (Alibaba, only host) |
| DeepSeek V4.1-Flash | 39 | 19.7 | 74.5 | 1M | MIT, open | 10 Sep 2026 | 0.18 (Decart FP4, OR); DeepSeek 0.60 off-peak |
| MiMo-V2.6-Flash | 38 | 24.2 | 76.4 | 1M | MIT, open | 21 Sep 2026 | 0.28 (Xiaomi); free on OpenCode Zen |
| GPT-6 Luna (max) | 38 | 13.6 | 73.0 | 1.05M | proprietary | 22 Sep 2026 | 0.50 (prompt from 272K: 0.75) |
| Mistral Large 4 Preview | 38 | 23.2 | – | 1M claimed, 524K measured | "open", licence and weights due late Oct 2026 | 6 Oct 2026 | 2.09 launch sale (list 4.18) |
| DeepSeek V4-Pro 0813 | 36 | 14.1 | 54.7 | 1M | MIT, open | Aug 2026 | 0.75 (Baidu FP8, OR, promo); DeepSeek 1.98 off-peak |
| Qwen3.8 27B (xhigh) | 34 | – | 58.4 | 256K | Apache 2.0, open, dense | 14 Aug 2026 | 1.25 (Chutes); Cerebras 1.49 |

How to read it:

- **AA and TB4.0 often disagree.** Muse Spark, GPT-6 Luna and V4-Pro look strong on AA and weak on TB4.0. Haiku 5.5 and
  GLM-5.3-Flash are the opposite case. Section 8 covers this.
- **Effort level is part of the score.** GLM-5.3 at low effort is AA 34, Haiku 5.5 at medium is 34, GPT-6 Luna at high
  is 33 and Gemini 3.8 Flash at low is 33. A cheap call at a low effort can land at or under the bar.
- **The cheapest route is often FP4 or a promo.** FP4 is not automatically bad (Nebius FP4 GLM-5.3 reached 99 % on AA's
  Endpoint Accuracy Index), but specific endpoints lost 15 to 27 % *(third-party measurement)*. Pin the quantization
  or the provider. The host comparison is in [01-PROFILES.md](01-PROFILES.md).

## 5. Per-model notes for agents

**MiMo-V2.6-Pro (Xiaomi, AA 46).** It is the highest-scoring open model on AA: 1.02T total / 42B active, 1M context,
with text, image, audio and video input. Xiaomi sells it at USD 0.435 / 0.87 with a cache read of 0.0036.
- Strengths: Vals TB4.0 31.3 is well above the bar. The vendor claims DeepSWE 71.9 and AutomationBench 53.1 *(vendor
  claim, harness not disclosed)*.
- Weaknesses: it is slow (about 42 to 47 tok/s, TTFT about 4 s) and has few hosts (4 on OR, some degraded). Vals TB2.1
  67.8 is only at the bar. In a hands-on DevOps test, Terraform and bash were fine, but only 1 of 3 Kubernetes manifests
  ran; the others crash-looped *(third-party measurement)*.
- Gotchas: reasoning is on by default. On the Anthropic-compatible endpoint, **multi-turn tool calls return 400 if
  `reasoning_content` is not passed back**, so echo it in the history. Max output is 128K first-party.

**MiMo-V2.6-Flash (Xiaomi, AA 38).** It has 309B / 15B parameters, an MIT licence and 1M context, at USD 0.14 / 0.28.
- Strengths: **Vals TB2.1 76.4 beats V4.1-Flash**, and TB4.0 24.2 is above the bar. Together with V4.1-Flash, it is the
  best price per intelligence point in the set.
- Weaknesses: very verbose (240M output tokens on the AA run, against a 140M median). It did worse than Pro in the same
  DevOps test (0 of 3 Kubernetes manifests ran).
- Gotchas: the reasoning-echo rule from Pro applies. The free OpenCode Zen variant uses your data.

**GLM-5.3 (Z.ai, AA 45 at max).** It has 753B / 40B parameters and 1M context, with effort low/high/max and a
`clear_thinking` flag.
- Strengths: **the strongest independent agent scores of any cheaply routable open model.** It scores Vals TB4.0 38.9,
  tbench.ai TB4.0 41.8 (Claude Code harness) and Vals SWE-bench Verified 95.4.
- Weaknesses: verbose (210M) and slow (64 tok/s). The licence has restrictions, so read it.
- Gotchas: Z.ai's first-party price (USD 1.40 / 4.40) is over the cap. Third-party hosts sell it for USD 1.88 to 2.90,
  and the endpoints cluster tightly on accuracy (95 to 99 % on AA's Endpoint Accuracy Index). **Thinking is always on, and
  the default effort is max**, so set `reasoning_effort` to low in tool loops. At low effort it is AA 34, exactly the bar.

**GLM-5.3-Flash (Z.ai, AA 42).** It has 320B / 18B parameters, an MIT licence, 1M context and hybrid sparse plus linear
attention, at USD 0.15 / 0.50 on Z.ai.
- Strengths: **the best hard-terminal score per dollar here.** It scores Vals TB4.0 37.4, and tbench.ai TB4.0 35.8 even
  with effort `none`. It also scores ExtractBench 80.75 for structured output *(vendor claim)* and Vals SWE-bench
  Verified 92.0. It supports `parallel_tool_calls` on OR and has 32 OR endpoints.
- Weaknesses: very verbose (180M) and below-average speed. Its LiveCodeBench score (80.5) is weaker than DeepSeek's.
- Gotchas: host quality varies. In a 600-task tool test, Fireworks scored 99.5 % and Nebius 84.8 % *(third-party
  measurement)*.

**DeepSeek V4.1-Flash (AA 39, 25 without reasoning).** This is the natural online upgrade within the same family. It
has 552B / 16B parameters, FP4 KV cache, 1M context, up to 384K output and a continuous effort setting from 1 to 100.
- Strengths: Vals TB2.1 74.5 against 67.0 for 0731. First-party it runs at 190 tok/s with TTFT 0.96 s, and supports up
  to 2,500 concurrent requests. It accepts JSON output and tool calls, and supports the Responses API and the
  Anthropic-compatible API first-party.
- Weaknesses: **on hard tasks, TB4.0 only moves from 18.7 to 19.7.** It is the most verbose model AA measured (250M).
- Gotchas: there is no Jinja chat template, so each host implements its own tool parsing, and tool calls can differ by
  host. Many of its 32 OR endpoints are FP4. Vercel caps output at 32K. The vendor says effort 60 to 80 gives most of
  max accuracy at under half the tokens *(vendor claim)*. DeepSeek trains on API inputs by default (opt-out).

**DeepSeek V4-Flash-0731 (AA 34, the bar).** These are the exact weights my rig runs. Online it costs USD 0.06 / 0.18
at DeepInfra (FP8).
- Strengths: it is a perfect overflow target. My prompts behave the same online as locally, at about the price of the
  electricity.
- Weaknesses: it is weak on knowledge, and AA measured a very high hallucination rate when the model is unsure (96 % for
  the preview). It is verbose (about 206M on the v4.1 run).
- Gotchas: there is no Jinja template (same caveat as V4.1). The `:free` variant on OR was removed on 21 Sep 2026.
  Hosts are retiring the older 0420 ID.

**DeepSeek V4-Pro-0813 (AA 36).** It has 1.6T / 49B parameters and an MIT licence.
- Strengths: **Vals SWE-bench Verified 96.4, the best patch-writing score in the cheap set.** It also scores GPQA 92.4.
- Weaknesses: on terminal agents it is weaker than the bar: Vals TB2.1 54.7 and TB4.0 14.1.
- Gotchas: the cheap Baidu route (USD 0.75) is an 81 % promo. DeepInfra caps output at 16K. DeepSeek's first-party
  price at peak (USD 3.96) is over the cap, and USD 1.98 off-peak.

**Step 5 Preview (StepFun, AA 44).** It has 600B / 27B parameters, 1M context and image and video input.
- Strengths: Vals TB4.0 31.8. The vendor claims TB2.1 85.0, GPQA 93.5 and BrowseComp 88.7 *(vendor claim)*. It is free
  on Kilo (no account, 200 req/h per IP, may train) and on OpenCode Zen (zero retention, no training).
- Weaknesses: one paid host (StepFun FP8), and its data terms are unknown.
- Gotchas: **it is a preview**, so expect churn. Weights are promised for 15 Oct 2026. Max output is 64K. The free
  routes are time-limited promos.

**Ling 3.1 Flash (InclusionAI, AA 41).** It is a 560B / 25B hybrid reasoning MoE released on 1 Oct 2026.
- Strengths: very cheap (Novita USD 0.075 / 0.225) and free on Requesty (no retention and no training per Requesty's
  metadata, EU endpoint, 200 RPD).
- Weaknesses: there are no independent agent benchmarks yet and no weights. It is very verbose (220M).
- Gotchas: **OR and Requesty serve only 262K context and 32K max output**, and Requesty flags no JSON-schema support.
  Its free listings churn by the day; OR's free variant disappeared between 12 and 13 Oct 2026. It is promising but
  unproven.

**Qwen3.8-Flash-Next (Alibaba, AA 40).** It has 180B / 6B parameters, is a preview of the Qwen4 architecture, and
has 262K context.
- Strengths: the vendor claims TB2.1 86.1, DeepSWE 58.7 and SWE-Pro 62.5 *(vendor claim)*. Its price is low at USD
  0.15 / 0.47.
- Weaknesses: there are no Vals numbers and Alibaba is the only host. It is very verbose (240M).
- Gotchas: **the model ID is ambiguous.** The Qwen Cloud ID "Qwen3.8-Flash" is reported not to be the same model, and
  OR's `qwen/qwen3.8-flash` (1M context) may be the cloud model. Check which one you get.

**Qwen3.8 27B (AA 34 at xhigh, 28 at medium).** It is a dense 27B model with an Apache 2.0 licence, 256K context and
multimodal input.
- Strengths: it is the only model at the bar that is small enough to run on modest local hardware. Cerebras serves it
  fast.
- Weaknesses: it reaches the bar only at xhigh effort (200M tokens, 45 tok/s). Vals TB2.1 58.4 is below the bar.
- Gotchas: Cerebras limits context to 65K. OR's free variant was removed on 6 Oct 2026.

**Gemini 3.8 Flash (Google, AA 41 at high).** It is proprietary, with 1M context.
- Strengths: the best knowledge scores in the set: Vals GPQA 94.4, MMLU-Pro 90.2, LiveCodeBench 89.5 and TB2.1 81.3. A
  free tier exists, with no-training terms in the EEA.
- Weaknesses: **Vals TB4.0 19.7 is only at the bar** for hard agents. AA's TTFT at high effort is about 25 s.
- Gotchas: max output is 65K. The intro price (USD 0.75 / 3.75) rises to **USD 1.50 / 7.50 on 1 Jan 2027**, which only
  batch processing (half price) keeps under the cap. The free tier gives about 20 requests per day according to forum
  reports.

**Mistral Large 4 Preview (AA 38).** It has 1.05T / 52B parameters, image input, and is EU-trained and EU-hosted.
- Strengths: Vals TB4.0 23.2 is above the bar. The vendor claims AutomationBench 59.9 and DeepSWE 61.7 *(vendor claim)*.
  It is relevant if I need EU residency.
- Weaknesses: the context measured 524K, against 1M claimed.
- Gotchas: **it is a preview, and it is cheap only during the launch sale** (USD 0.68 / 2.09; list output 4.18). The
  weights and licence are due in late Oct 2026.

**Cheap closed models.** These are proprietary APIs. There are no weights, no local fallback, and the provider can
change behaviour behind the same ID.

- **Claude Haiku 5.5 (AA 43 max, 38 high, 34 medium).** It costs USD 0.10 / 0.50 up to a 100K prompt, then **0.50 /
  2.50 above 100K**, so agent loops with long context hit the 5x tier quickly. Its agent scores are strong: Vals TB4.0
  36.4, the third best in this file, and OSWorld 2.1 72.4 *(vendor claim)*. At max effort it is extremely verbose (440M
  tokens) and AA measured a **TTFT of about 303 s**. Medium effort is only at the bar. The API is Anthropic-native, and
  OpenAI-compatible access goes through gateways.
- **GPT-6 Luna (AA 38 max, 35 xhigh, 33 high).** It costs USD 0.10 / 0.50 (0.75 output from a 272K prompt), with 1.05M
  context and 128K output. It scores Vals TB2.1 73.0 but **TB4.0 13.6, below the bar**. One report says **tool calling
  works only at reasoning effort `none` on Chat Completions**, so the Responses API is needed for reasoning plus tools
  (verify this yourself). The same source reports a 93 % hallucination rate at max effort. AA's TTFT at max is about
  89 s.
- **Muse Spark 1.3 Contributor (Meta, AA 45 at xhigh).** It costs USD 0.10 / 0.20 because **Meta trains on your
  prompts and outputs**. Meta's docs say the Contributor ID cannot run at "max", so its ceiling is xhigh = AA 45
  (Muse Spark 1.3 standard at max = 48). The official limit on 13 Oct 2026 is 150 RPM / 3M TPM per team (older
  blogs say 60 or 100 RPM). EU access is unconfirmed: it works only "where Meta has enabled access", with no DPA. Vals lists "Muse Spark 1.3" (TB4.0 10.6) and "Muse Spark 1.3 Max" (TB4.0 24.8)
  separately. I would send it only non-sensitive bulk text, never anything with client context.

## 6. Above the bar, but not cheap

| Model | AA | Independent agent numbers | Cheapest output | Why it is here |
|---|---|---|---|---|
| Kimi K3 (max) | 44 (30 at low) | Vals TB2.1 80.9, TB4.0 17.2, SWE-V 93.4 | 9.50 (Chutes, no tools); Moonshot 15.00 | best open tool-use model, expensive per token |
| Grok 4.7 | 46 | Vals TB4.0 28.8 | 6.00 | 500K context, TTFT about 101 s |
| Qwen3.8 Max | 45 | Vals TB4.0 34.3 | 6.00 | proprietary |
| GPT-6.1 Sol (low) | 42 | – | 10.00 | concise: AA cost per task USD 0.13 |
| GPT-5.6 Terra | 42 | Vals TB2.1 77.5, SWE-V 95.4 | 12.00 | |
| Muse Spark 1.3 standard | 48 | see section 5 | 4.25 | the Contributor tier is the cheap route |
| Gemini 3.8 Flash from 2027 | 41 | see section 5 | 7.50 list | stays cheap only via batch or the free tier |

**Kimi K3** is the interesting one. It has the best tool-use numbers of any open model: MCP-Atlas 84.2, MCPMark-V 94.5,
Toolathlon-Verified 76.5 and BrowseComp 91.2 *(vendor claim)*. Note, though, that its Vals TB4.0 (17.2) is just below
the bar. Thinking is always on, and **every turn must echo the full assistant message, including `reasoning_content`
and `tool_calls`**. Moonshot's privacy policy allows training on user content.

**Flat plans change the price, but they come with scope rules:**

- **Kimi Code** (Plus USD 19, Pro 39, Max 99, Ultra 199 a month) includes K3. `k3-256k` is on Plus, and the 1M-context
  `k3` is on Pro and above. It is limited to supported coding clients such as Claude Code, OpenCode and Codex.
  Tampering with the User-Agent can get the account suspended. **My own agent is a grey area here, and a product
  backend is not allowed.**
- **GLM Coding Plan** (Lite USD 18 a month, third-party price) gives GLM-5.3 at roughly USD 65 to 175 a month of
  PAYG value, according to my calculation from the published credit multipliers. It may be used **only inside officially
  supported tools**, so raw API calls from my own agent are out. For GLM-5.3-Flash the plan is poor value; PAYG is
  better.
- **Ollama Cloud Pro** (USD 20 a month with USD 60 of credits) serves `kimi-k3` and `glm-5.3` at list prices, with no
  restriction on API use. That cuts K3's effective output price to about USD 5, which is still over the cap.
- **Step Plan** (Mini USD 6.99 to Max USD 99, third-party prices) includes Step 5 Preview and appears to allow your own
  stack. Verify this in the terms of service.
- Fireworks Fire Pass (Kimi K3 Fast) was closed to new subscribers in Oct 2026.

## 7. Below the bar, including the free models

"Free" usually means a model that is weaker than what my rig already runs. These are the ones still offered, with
their AA v4.3.2 scores against the bar of 34:

| Model | AA | Independent agent numbers | Where it is free or cheap | Verdict |
|---|---|---|---|---|
| MiniMax-M3 | 29 | Vals TB2.1 53.6, **TB4.0 1.0**, SWE-V 75.0 | USD 0.96 to 1.20 output; Vercel free-tier eligible | below, cheap and open, 1M context |
| Kimi K2.6 | 27 | Vals TB2.1 53.6, SWE-V 76.2 | USD 1.82 to 1.95 (Baidu, Chutes) | below, deprecated on AA |
| Kimi K2.7 Code | 26 | Vals TB2.1 67.0, SWE-V 78.2 | Vercel free-tier eligible; USD 4.00 list | coding-tuned, below on AA |
| Inkling Small | 26 | Vals TB2.1 55.1 | `:free` on OR, Kilo | below |
| Inkling | 25 | Vals TB2.1 47.6 | `:free` on OR (1M context, 262K out) | below, ignores `tool_choice` |
| Nemotron 3 Ultra 550B | 23 | Vals TB2.1 50.9, SWE-V 69.0; AutomationBench 3 % (AA) | free on OR, Kilo, Requesty | below, NVIDIA trial terms say do not send personal data |
| gpt-oss-120b (high) | 12 | Vals TB2.0 19.1, SWE-V 33.6 | from USD 0.15 output; OVH anonymous 2 RPM | far below for agents |

Others below the bar include Gemini 3.1 Pro Preview (30, TB4.0 2.5), GLM-5.1 (26), Gemini 3 Flash (26), Qwen3.7 Plus
(25), the V4-Flash 0420 preview (24), Kimi K2.5 and MiniMax-M2.7 (23), GLM-4.7 (22), Gemini 3.5 Flash-Lite (22),
Qwen3.5 and Qwen3.6 (18), Mistral Medium 3.5 (14) and Llama 4 Maverick and Scout (10 and 8). **Everything on the usual
"free and cheap" lists from early 2026 is below V4-Flash-0731 today:** GLM-4.6/4.7, Kimi K2.x, Qwen3.5/3.6, MiniMax
M2.x, gpt-oss-120b, Gemini 2.5/3 Flash, Mistral Medium 3.x, Grok fast, GPT-5.x mini and Llama 4.

**The genuinely free models that are above the bar are all time-limited promos:** Step 5 Preview (Kilo, OpenCode Zen),
Ling 3.1 Flash (Requesty, Kilo, OpenCode Zen), MiMo-V2.6-Flash (OpenCode Zen) and Muse Spark 1.3 Contributor (OpenCode
Zen, trains). The median free model on OR stays listed about 75 days, and the OR free list shrank from 24 to 16 entries
between 21 Sep and 13 Oct 2026. GLM-5.3-Flash is not free, but Vercel's USD 5 monthly credit buys about 10M of its
output tokens.

## 8. Hard-agent ranking: Vals Terminal-Bench 4.0

TB4.0 is the hardest live agent benchmark with an independent harness. The bar (0731) is **18.7**. The table covers
every model from this file that Vals has run.

| Rank | Model | Vals TB4.0 | AA | Cheap? |
|---|---|---|---|---|
| 1 | GLM-5.3 | 38.9 | 45 | yes (third-party hosts) |
| 2 | GLM-5.3-Flash | 37.4 | 42 | **yes, USD 0.15 to 0.50** |
| 3 | Claude Haiku 5.5 | 36.4 | 43 | yes, closed |
| 4 | Qwen3.8 Max | 34.3 | 45 | no |
| 5 | Step 5 Preview | 31.8 | 44 | yes, preview |
| 6 | MiMo-V2.6-Pro | 31.3 | 46 | yes |
| 7 | Grok 4.7 | 28.8 | 46 | no |
| 8 | Muse Spark 1.3 Max | 24.8 | 48 | standard price only |
| 9 | MiMo-V2.6-Flash | 24.2 | 38 | yes |
| 10 | Mistral Large 4 Preview | 23.2 | 38 | sale only |
| 11 | DeepSeek V4.1-Flash | 19.7 | 39 | yes |
| 11 | Gemini 3.8 Flash | 19.7 | 41 | batch or free tier |
| – | **DeepSeek V4-Flash 0731 (bar)** | **18.7** | **34** | local |
| 13 | Kimi K3 | 17.2 | 44 | no |
| 14 | DeepSeek V4-Pro 0813 | 14.1 | 36 | yes |
| 15 | GPT-6 Luna | 13.6 | 38 | yes, closed |
| 16 | Muse Spark 1.3 (standard) | 10.6 | 48 | Contributor tier |
| 17 | MiniMax-M3 | 1.0 | 29 | yes |

What this shows:

- **AA alone misleads for agents.** GPT-6 Luna and V4-Pro-0813 clear the AA bar but fall below 0731 on hard terminal
  tasks. Muse Spark 1.3 has the highest AA in the file (48), yet its standard SKU scores 10.6.
- **The reverse also happens.** GLM-5.3-Flash and Haiku 5.5 rank higher on TB4.0 than their AA position suggests.
- **V4.1-Flash is not a big step up for hard agents.** It barely beats the bar (19.7 against 18.7), so the reason to use
  it is speed and price, not capability.
- The official tbench.ai board agrees on the order: GLM-5.3 41.8, GLM-5.3-Flash 35.8, Gemini 3.8 Flash 19.1, GPT-6 Luna
  16.4.
- Ling 3.1 Flash, Qwen3.8-Flash-Next and Qwen3.8 27B have no TB4.0 run yet, so I treat them as unproven for hard agents.

To check a model on my own tasks rather than on a leaderboard, see
[../course_agentic_apps/14-EVALUATION.md](../course_agentic_apps/14-EVALUATION.md).

## 9. My picks per role

These picks are for non-sensitive data only. Client and professional data stays on the local rig.

- **Bulk worker** (summaries, extraction, classification at volume): **GLM-5.3-Flash** at USD 0.15 / 0.50 on Z.ai,
  Fireworks, Together or Parasail, with `reasoning_effort` set low. Z.ai does not train on API data. My second choice
  is **V4-Flash-0731 at DeepInfra** (USD 0.06 / 0.18). It is my local model, so the same prompts work for overflow
  without any retuning. **MiMo-V2.6-Flash** (USD 0.28) is the alternative when I need TB2.1-style shell work.
- **Coding sub-agent:** **GLM-5.3** through a faithful third-party host (USD 1.88 to 2.20 output), or through the GLM
  Coding Plan when it runs inside Claude Code or OpenCode. GLM-5.3-Flash is nearly as strong on TB4.0 for a quarter of
  the price. For patch-only tasks (fix this failing test), **V4-Pro-0813** has the best SWE-bench Verified score (96.4),
  but I would not let it drive a terminal. If closed is fine: **Haiku 5.5** at high effort, with the prompt kept under
  100K.
- **Tool router** (picks a tool or emits JSON, latency matters): **GLM-5.3-Flash** at effort `none` or low. It still
  scores 35.8 on tbench.ai TB4.0 at `none`, supports `parallel_tool_calls` and scores 80.75 on ExtractBench *(vendor
  claim)*. Otherwise **V4.1-Flash first-party** at low effort (190 tok/s, TTFT under 1 s). I would avoid GPT-6 Luna on
  Chat Completions (tools only at effort `none`), Inkling free (no `tool_choice`) and the random `openrouter/free` or
  `kilo-auto/free` routers.
- **Long-context reader** (whole repos, long logs, 200K to 1M tokens): **V4.1-Flash on DeepSeek** has 1M context and
  cache hits at USD 0.003 off-peak, so I keep the prefix stable. **Gemini 3.8 Flash** (free tier or batch) is good
  for knowledge-heavy reading, but output is capped at 65K. I would avoid Ling on OR (262K), Mistral Large 4 (524K
  measured) and Scaleway's capped 256K endpoints. Haiku 5.5 and GPT-6 Luna do have 1M context, but their price
  jumps above 100K and 272K.
- **Planner-lite** (a cheap second opinion below Claude Opus): **MiMo-V2.6-Pro** (AA 46, USD 0.87 output). It is slow,
  but a planner does not need many calls. For free experiments, **Step 5 Preview on OpenCode Zen** (zero retention).
  **Muse Spark 1.3 Contributor** only for throwaway prompts, because Meta trains on them. For real planning, Opus stays
  the planner (see [../course_agentic_apps/17-HYBRID-AND-ROUTER.md](../course_agentic_apps/17-HYBRID-AND-ROUTER.md)).

**Sources:** [AA leaderboard v4.3.2](https://artificialanalysis.ai/leaderboards/models) · [AA methodology](https://artificialanalysis.ai/methodology/intelligence-benchmarking) ·
[AA changelog](https://artificialanalysis.ai/changelog) · [AA V4-Flash 0731](https://artificialanalysis.ai/models/deepseek-v4-flash) · [AA V4-Flash 0420](https://artificialanalysis.ai/models/deepseek-v4-flash-0420) ·
[AA 0731 at v4.1](https://artificialanalysis.ai/articles/deepseek-v4-flash-0731-scores-50-on-the-artificial-analysis-intelligence-index-10-points-above-previous-deepseek-v4-flash) ·
[AA V4 launch at v4.0](https://artificialanalysis.ai/articles/deepseek-is-back-among-the-leading-open-weights-models-with-v4-pro-and-v4-flash) · [AA V4.1-Flash](https://artificialanalysis.ai/models/deepseek-v4-1-flash) ·
[AA MiMo-V2.6-Pro](https://artificialanalysis.ai/models/mimo-v2-6-pro) · [AA GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash) · [AA Kimi K3](https://artificialanalysis.ai/models/kimi-k3) ·
[AA Claude Haiku 5.5](https://artificialanalysis.ai/models/claude-haiku-5-5) · [AA Endpoint Accuracy Index](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) ·
[Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [Vals TB2.1](https://www.vals.ai/benchmarks/terminal-bench-2-1) · [Vals SWE-bench](https://www.vals.ai/benchmarks/swebench) ·
[tbench.ai leaderboard](https://www.tbench.ai/leaderboard) · [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) · [DeepSeek-V4 paper](https://arxiv.org/pdf/2606.19348) ·
[DeepSeek-V4.1-Flash paper](https://arxiv.org/pdf/2609.19969) · [HF V4-Flash-0731 card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) · [HF GLM-5.3](https://huggingface.co/zai-org/GLM-5.3) ·
[HF Kimi K3](https://huggingface.co/moonshotai/Kimi-K3) · [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) · [Z.ai pricing](https://docs.z.ai/guides/overview/pricing) ·
[GLM Coding Plan usage policy](https://docs.z.ai/devpack/usage-policy) · [Kimi Code docs](https://www.kimi.com/code/docs/en/) · [Kimi platform pricing](https://platform.kimi.ai/docs/pricing/chat) ·
[MiMo Token Plan](https://mimo.mi.com/docs/en-US/tokenplan/Token%20Plan/subscription) · [StepFun pricing](https://platform.stepfun.ai/docs/en/guides/pricing/details) · [OpenRouter models API](https://openrouter.ai/api/v1/models) ·
[TrueFoundry on OR free models](https://www.truefoundry.com/blog/openrouter-free-models-whats-actually-free-and-what-it-costs-you) · [Kilo Gateway models](https://api.kilo.ai/api/gateway/models) ·
[OpenCode Zen docs](https://opencode.ai/docs/zen/) · [Requesty free models](https://www.requesty.ai/models/free) · [Vercel AI Gateway pricing](https://vercel.com/docs/ai-gateway/pricing) ·
[openbenchmarks same-model accuracy](https://openbenchmarks.com/inference/same-model-different-accuracy) · [computingforgeeks MiMo test](https://computingforgeeks.com/xiaomi-mimo-v2-6-pro-flash/) ·
[computingforgeeks GPT-6 Luna](https://computingforgeeks.com/gpt-6-sol-luna-released-features-benchmarks/) · [Claude pricing](https://claude.com/pricing) · [Gemini API terms](https://ai.google.dev/gemini-api/terms) ·
[Vellum on Gemini 3.8 Flash](https://www.vellum.ai/md/blog/gemini-3-8-flash-benchmarks-explained) · [Mistral Large 4 pricing](https://capitalandcompute.net/md/mistral-large-4-pricing-benchmarks.md) ·
[Step 5 Preview](https://www.orcarouter.ai/blog/step-5-preview-open-weights) · [Qwen3.8-Flash-Next](https://llm-stats.com/blog/research/qwen3.8-flash-next-launch) ·
[Muse Spark Contributor tier](https://cryptobriefing.com/meta-muse-spark-discounted-data-sharing/) · [Ollama Cloud pricing](https://ollama.com/pricing)
