# How to use cheap and free online models in agentic apps (October 2026)

This file is the practical half of the survey. [01-PROFILES.md](01-PROFILES.md) says what each route offers and
[02-MODELS.md](02-MODELS.md) says which models are smart enough. Here I describe how I wire them into my agents: which
work goes where, a router config, the cost math, the traps, a short acceptance test, the terms, and how I monitor it all.

**AA** in this file means the **Artificial Analysis Intelligence Index v4.3.2, as of 13 Oct 2026** (a third-party
measurement). My local model, DeepSeek-V4-Flash-0731, scores **AA 34**, and that is the bar. Prices are USD per 1M
tokens (input / output) as seen on 13 Oct 2026. Cached-input prices are given separately.

## 1. The shortest answer

- **One router, four legs.** My agents talk to one OpenAI-compatible endpoint (a LiteLLM proxy). Behind it are the
  local rig, free tiers, cheap pay-as-you-go hosts and Claude Opus as the planner. Agents ask for a group name, not a
  provider.
- **Client data never goes through the router.** Private jobs call llama-swap on the rig directly. A fallback is
  exactly how private data would leak by accident.
- **Free tiers are for experiments and small batches, not for production loops.** They count requests (Gemini about
  20 a day, Requesty 200 a day) or tokens (Groq 200K a day, about 3 agent steps). Every one of them changed in 2026.
- **The cheap default is GLM-5.3-Flash (AA 42) at USD 0.15 / 0.50** on a measured host, with DeepSeek V4.1-Flash
  (AA 39) as the fallback. 1,000 ten-step agent tasks cost about USD 20 to 40 with caching.
- **Caching and reasoning effort matter more than the list price.** A broken cache makes the same run 3 to 7 times
  more expensive. Max effort costs 1.7 to 2.4 times as much as low effort in my examples.
- **The same model on another host is not the same model.** Tool-call success for GLM-5.3-Flash ranged from 99.5%
  (Fireworks) to 84.8% (Nebius) in one test *(third-party measurement)*. Pin hosts you have measured.
- **Run a 15-minute acceptance test before trusting a route,** and run it again every month. Models, prices, limits
  and terms all moved within the last 90 days.
- **Flat coding plans are not agent backends.** GLM Coding Plan, Kimi Code, Alibaba Coding Plan and MiMo Token Plan
  forbid use from your own scripts or backends. Ollama Cloud does not restrict it.

## 2. Four legs, one router

The idea follows [../course_agentic_apps/17-HYBRID-AND-ROUTER.md](../course_agentic_apps/17-HYBRID-AND-ROUTER.md) and
[../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md](../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md). This
survey adds two online legs between the rig and Claude.

| Leg | What it is | Strength | Weakness |
|---|---|---|---|
| Local | DeepSeek-V4-Flash-0731 (AA 34) via llama-swap, OpenAI-compatible at `http://localhost:8080/v1` | private, no per-token cost, 131K context per slot | 4 slots at about 13.6 tok/s each |
| Free | NVIDIA build (GLM-5.3, AA 45), Kilo (Step 5 Preview, AA 44), Requesty (Ling 3.1 Flash, AA 41), Gemini API (Gemini 3.8 Flash, AA 41) | zero cost, often stronger than local | tiny or unpublished quotas, queueing, churn, some train on prompts |
| Cheap PAYG | GLM-5.3-Flash, DeepSeek V4.1-Flash, V4-Flash-0731 on DeepInfra, MiMo-V2.6-Pro | fast, high concurrency, USD 0.18 to 0.87 output | quality varies by host |
| Frontier | Claude Opus as the planner | best plans and judgement | price, so few calls |

Local throughput, worked out: 4 slots × 13.6 tok/s × 86,400 s is about **4.7M output tokens a day** at best. A step
that writes 1,500 tokens takes about 110 s on one slot. That is fine overnight and slow for anything interactive.

### Decision table by task type

| Task | First choice | Then | Why |
|---|---|---|---|
| Anything with client or professional data | **local only** | nothing: wait or fail | data rule; no fallback exists for this class |
| Bulk extraction and classification (non-sensitive) | GLM-5.3-Flash at low effort on Z.ai or Fireworks | V4-Flash-0731 on DeepInfra (same weights as local) | cheap, ExtractBench 80.75 *(vendor claim)*; 0731 needs no prompt retuning |
| Small one-off batch (under about 200 requests) | Requesty free (Ling 3.1 Flash) or NVIDIA free | cheap GLM-5.3-Flash | fits a daily free quota |
| Coding sub-agent | GLM-5.3-Flash (Vals TB4.0 37.4) | GLM-5.3 on a faithful host; NVIDIA free GLM-5.3 for experiments | best hard-terminal score per dollar |
| Tool-heavy loop (many short steps) | DeepSeek V4.1-Flash first-party (190 tok/s, TTFT 0.96 s) | GLM-5.3-Flash | speed and cache hits at USD 0.003 off-peak; free tiers die on request counts |
| Long-context reading (200K to 1M) | DeepSeek V4.1-Flash, 1M context, stable prefix | Gemini 3.8 Flash free tier for knowledge-heavy reading | avoid capped hosts (section 6); local stops at 131K |
| Eval and judging | a different model family than the one judged, e.g. MiMo-V2.6-Pro (AA 46) | Claude Opus for disputed cases | a judge from the same family flatters itself |
| Planning and decomposition | Claude Opus | MiMo-V2.6-Pro as a cheap second opinion | few calls, high stakes |
| Overflow when the local queue is full (non-sensitive only) | V4-Flash-0731 on DeepInfra (USD 0.06 / 0.18) | V4.1-Flash | same weights, so the same prompts and parsers work |

**My rule:** fallbacks go from free to cheap, and from cheap to cheap. Nothing falls back into the local leg
automatically, because its 4 slots belong to private work. Nothing ever falls back out of the local leg.

## 3. A concrete LiteLLM router config

LiteLLM runs as a proxy (default port 4000) in front of everything. Each `model_name` is a group, and deployments
sharing a name are load-balanced. I keep **one model per group**, so a fallback never silently swaps GLM for
DeepSeek in the middle of a task. The fallbacks between groups do that, and they do it visibly.

**All model IDs and OpenRouter provider slugs below are as of 13 Oct 2026. Check current IDs before use.**
The `rpm` values are my own throttles set under the published or measured limits.

```yaml
# litellm-config.yaml: four legs, one router. Keys only from environment variables.
model_list:
  # ---- leg 1: local rig. Private jobs call llama-swap directly; this entry is for non-sensitive use only.
  - model_name: local
    litellm_params:
      model: openai/DeepSeek-V4-Flash-0731          # name as defined in llama-swap
      api_base: http://localhost:8080/v1
      api_key: os.environ/LOCAL_API_KEY             # llama-swap ignores it; any string
      max_parallel_requests: 4                      # 4 slots
      timeout: 1800                                 # ~13.6 tok/s per slot: long answers take minutes
    model_info: {max_input_tokens: 131072}

  # ---- leg 2: free tiers (non-sensitive only)
  - model_name: free-glm                            # GLM-5.3, AA 45
    litellm_params:
      model: openai/z-ai/glm-5.3                    # check current IDs
      api_base: https://integrate.api.nvidia.com/v1
      api_key: os.environ/NVIDIA_API_KEY
      rpm: 30                                       # ~40 RPM per ACCOUNT (community-measured), shared by all NVIDIA models
      timeout: 900                                  # queueing on popular models
      cooldown_time: 300
  - model_name: free-step                           # Step 5 Preview, AA 44; promo; Kilo flags "may train"
    litellm_params:
      model: openai/stepfun/step-5-preview-free
      api_base: https://api.kilo.ai/api/gateway
      api_key: os.environ/KILO_API_KEY              # free models answer without a key
      rpm: 3                                        # 200 requests per hour per IP
      timeout: 300
  - model_name: free-ling                           # Ling 3.1 Flash, AA 41; EU endpoint
    litellm_params:
      model: openai/novita/ling-3.1-flash
      api_base: https://router.eu.requesty.ai/v1
      api_key: os.environ/REQUESTY_API_KEY
      rpm: 5                                        # 200 requests per DAY across all Requesty free models
      timeout: 300
      cooldown_time: 3600
    model_info: {max_input_tokens: 262144, max_output_tokens: 32768}
  - model_name: free-gemini                         # Gemini 3.8 Flash, AA 41 (high)
    litellm_params:
      model: gemini/gemini-3.8-flash
      api_key: os.environ/GEMINI_API_KEY
      rpm: 5                                        # ~5 RPM / ~20 RPD measured; resets midnight Pacific
      timeout: 600                                  # free-tier latency measured at 27-354 s
      cooldown_time: 3600                           # a daily-quota 429 does not clear in two minutes
    model_info: {max_input_tokens: 1048576, max_output_tokens: 65536}

  # ---- leg 3: cheap pay-as-you-go
  - model_name: cheap-glm                           # GLM-5.3-Flash, AA 42: three hosts, same model
    litellm_params:
      model: openrouter/z-ai/glm-5.3-flash
      api_key: os.environ/OPENROUTER_API_KEY
      rpm: 60
      timeout: 300
      extra_body:
        provider:
          order: ["fireworks", "together", "parasail"]  # best measured tool success; check slugs on /endpoints
          allow_fallbacks: false                    # do not drift to an unmeasured host
          require_parameters: true                  # never land on a host that drops tools or response_format
          quantizations: ["fp8", "bf16"]
          data_collection: "deny"                   # skip endpoints that may store or train
  - model_name: cheap-glm
    litellm_params:
      model: openai/glm-5.3-flash
      api_base: https://api.z.ai/api/paas/v4        # PAYG endpoint, NOT the coding-plan endpoint
      api_key: os.environ/ZAI_API_KEY
      rpm: 60
      timeout: 300
  - model_name: cheap-glm
    litellm_params:
      model: fireworks_ai/accounts/fireworks/models/glm-5p3-flash   # check current IDs
      api_key: os.environ/FIREWORKS_API_KEY
      rpm: 60
      timeout: 300

  - model_name: cheap-ds                            # DeepSeek V4.1-Flash, AA 39
    litellm_params:
      model: deepseek/deepseek-flash                # first-party ID, currently V4.1-Flash
      api_key: os.environ/DEEPSEEK_API_KEY
      max_parallel_requests: 100                    # DeepSeek allows 2,500 concurrent
      timeout: 900                                  # server holds queued requests up to 10 minutes
  - model_name: cheap-ds
    litellm_params:
      model: openrouter/deepseek/deepseek-v4.1-flash
      api_key: os.environ/OPENROUTER_API_KEY
      rpm: 60
      timeout: 300
      extra_body:
        provider:
          order: ["deepinfra"]
          allow_fallbacks: false
          require_parameters: true
          quantizations: ["fp8"]
          data_collection: "deny"

  - model_name: cheap-0731                          # the rig's own weights, for non-sensitive overflow
    litellm_params:
      model: openai/deepseek-ai/DeepSeek-V4-Flash-0731
      api_base: https://api.deepinfra.com/v1/openai
      api_key: os.environ/DEEPINFRA_TOKEN
      max_parallel_requests: 50                     # DeepInfra allows 200 concurrent per model
      timeout: 600

  # ---- leg 4: frontier planner
  - model_name: frontier
    litellm_params:
      model: anthropic/claude-opus-5-5              # check current IDs
      api_key: os.environ/ANTHROPIC_API_KEY
      timeout: 600

router_settings:
  routing_strategy: simple-shuffle
  enable_pre_call_checks: true                      # skip deployments whose context window is too small
  num_retries: 2
  retry_policy:
    RateLimitErrorRetries: 1                        # one retry on another deployment, then fall back
    TimeoutErrorRetries: 1
    InternalServerErrorRetries: 2
    BadRequestErrorRetries: 0                       # a 400 is a bug or a missing reasoning echo; retrying will not help
  allowed_fails_policy:
    RateLimitErrorAllowedFails: 1                   # one 429 puts the deployment in cooldown
    InternalServerErrorAllowedFails: 3
  cooldown_time: 120
  fallbacks:
    - {"free-glm": ["cheap-glm"]}
    - {"free-step": ["cheap-glm"]}
    - {"free-ling": ["cheap-glm"]}
    - {"free-gemini": ["cheap-glm"]}
    - {"cheap-glm": ["cheap-ds"]}
    - {"cheap-ds": ["cheap-0731"]}
    # deliberately absent: anything -> local, and local -> anything
  context_window_fallbacks:
    - {"free-ling": ["cheap-glm"]}                  # 262K on Requesty -> 1M

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

Notes on the config:

- **The OpenRouter `provider` block** is passed through `extra_body`. `order` plus `allow_fallbacks: false` pins the
  hosts. `require_parameters: true` drops hosts that do not support every parameter in the request, such as `tools`
  or `response_format`. `quantizations` filters by precision. `data_collection: "deny"` skips endpoints that may store
  or train. If I have no measurement for a model, I leave out `order` and let **Auto Exacto** choose: since
  12 Mar 2026 it re-ranks providers for every request with `tools` on tool-call telemetry. Never use `:floor` for
  agents, because it picks the cheapest host regardless of quality.
- **A quantization filter may also remove endpoints whose quantization is "unknown"** (DeepSeek's own, Fireworks and
  Together show it that way on OpenRouter). The acceptance test in section 7 tells me which host actually answered.
- **Timeouts are long on purpose.** NVIDIA queues popular models, DeepSeek holds queued requests up to 10 minutes,
  and Gemini free answers took 27 to 354 s in a September measurement. A short client timeout plus a retry just
  doubles the load and the bill.
- **Cooldowns on 429.** One 429 puts the deployment in cooldown and the next one in the group is used. For free tiers
  with a *daily* quota I set a long per-deployment `cooldown_time`. As far as I know, LiteLLM has no
  requests-per-day limit per deployment, so after the daily quota is gone the router will keep trying once per
  cooldown. On OpenRouter free models, even failed requests can count against the daily quota *(third-party
  measurement)*.
- **Reasoning effort is set per call in the app**, not in the router (section 5). Bulk steps use low effort and hard
  steps use high.
- **Prompt caches live at one provider.** When the router spreads one task over several hosts, each switch pays
  full price for the prefix again. For long tasks I prefer a group with a single deployment and a fallback group,
  rather than a group that shuffles between three hosts.

## 4. Juggling free tiers honestly

**One account per service, used as the service intends.** I do not pool accounts. GLM Coding Plan bans account
sharing (more than 3 violations means a ban). Google has suspended Antigravity accounts that used the quota through
other tools. Puter-pool repos break the spirit of Puter's terms. NVIDIA needs SMS verification per account. A ban
usually lands on the identity, and with it on the paid account I depend on. Free tiers are samplers; when one
becomes load-bearing, I pay for it.

### Request-counted versus token-counted quotas

An agent step re-sends the whole history, so the unit of the quota decides everything. My standard step has
**60K tokens of context, of which 54K hit the cache, 6K are new, and 1.5K are output** (reasoning included).

| Route | Quota counts | Free volume (13 Oct 2026) | Resets | Scope | 60K-context steps per day |
|---|---|---|---|---|---|
| Gemini API, Gemini 3.8 Flash | requests | ~5 RPM, ~20 RPD *(third-party measurement)* | midnight Pacific | per project (extra keys add nothing) | ~20 |
| NVIDIA build | requests | ~40 RPM *(community-measured)*, daily cap unknown | not documented | per account, all models share it | limited by queueing, not by quota |
| Requesty free | requests | 200 RPD, no card | daily, time not documented | per account, all free models share it | 200 |
| Kilo free | requests | 200 per hour per IP, no account | hourly | per IP (NAT shares it) | up to 200 an hour |
| OpenRouter free | requests | 20 RPM; 50 RPD, or 1,000 RPD after USD 10 lifetime purchases | daily, time not documented | per account | 1,000, but the free models there are below the bar |
| Groq free | tokens and requests | 30 RPM, 1K RPD, 8K TPM, 200K TPD | daily | per org, per model | ~3 (8K TPM blocks even one step) |
| Cerebras free trial | tokens | 5 RPM, 30K uncached TPM, 1M TPD, 64K context | daily | per model; card required | ~16, but the 60K step barely fits in 64K |
| Cloudflare Workers AI | neurons | 10,000 neurons a day (about 147K gpt-oss-120b output tokens) | 00:00 UTC | per account | gpt-oss-120b only (AA 12) |
| Alibaba Model Studio intl | tokens | 1M per model, one-time, 90 days | never | per model | ~16 in total, per model |

What this means in practice:

- **Request-counted tiers favour long-context steps.** A 60K-token step costs Requesty one request out of 200. The
  same step costs Groq 30% of its daily tokens.
- **A ten-step task costs 10 requests plus retries.** Requesty gives me about 20 such tasks a day, Gemini about two.
- **Reset times in Polish time:** midnight Pacific is 09:00 most of the year, but 08:00 between 25 Oct and
  1 Nov 2026, when Europe has left summer time and the US has not. Cloudflare documents 00:00 UTC. Most others
  do not say, so I read the `x-ratelimit-*` headers and the 429 body (Gemini names the quota, for example
  `GenerateRequestsPerDayPerProjectPerModel-FreeTier`).
- **Other windows:** Ollama Free resets monthly from signup. Z.ai's off-peak window halves Coding Plan credits.
  DeepSeek's peak window (01:00 to 04:00 and 06:00 to 10:00 UTC on weekdays) doubles the price.
- **Traps on the way to paying:** on Vercel AI Gateway, buying any credits permanently ends the USD 5 per 30 days free
  credit. On OpenRouter, a negative balance returns 402 even on free models.

## 5. Cost math

The prices used here (13 Oct 2026, input / cached / output):

- **DeepSeek V4.1-Flash, first-party:** 0.15 / 0.003 / 0.60 off-peak. Peak is double.
- **GLM-5.3-Flash on Z.ai:** 0.15 / 0.03 / 0.50.
- **MiMo-V2.6-Pro on Xiaomi:** 0.435 / 0.0036 / 0.87.
- **OpenRouter V4.1-Flash, fp4 host (Decart):** 0.09 / 0.018 / 0.18.
- **OpenRouter V4.1-Flash, fp8 host (DeepInfra):** 0.14 / 0.004 / 0.42. This is a promo price (−30%).

OpenRouter rows include its 5.5% fee on credit purchases. For Ollama Pro (USD 20 a month with USD 60 of credits),
V4.1-Flash costs 0.15 / 0.60 off-peak. My sources do not give an Ollama cached-input price, so I assume no cache
discount. That is the worst case, and you should check it.

### Example 1: bulk extraction, 1,000 tasks × 3 steps

Each step has 6K input (a 3K cached prefix plus 3K of new text) and 1K output. In total that is 9M cached, 9M
uncached and 3M output tokens.

| Route | Model (AA) | Cost for 1,000 tasks |
|---|---|---|
| DeepSeek off-peak | V4.1-Flash (39) | USD 3.18 (peak 6.35) |
| Z.ai | GLM-5.3-Flash (42) | USD 3.12 |
| Xiaomi | MiMo-V2.6-Pro (46) | USD 6.56 |
| OpenRouter fp4 (Decart) | V4.1-Flash (39) | USD 1.60 |
| OpenRouter fp8 (DeepInfra) | V4.1-Flash (39) | USD 2.70 |
| Ollama Pro, off-peak | V4.1-Flash (39) | USD 4.50 of credits (7.5% of the month) |
| Local rig | V4-Flash-0731 (34) | USD 0, about 15 hours on 4 slots |
| Requesty free | Ling 3.1 Flash (41) | USD 0, 15 days at 200 RPD |

**At this size, money does not decide anything. Quality, latency and data terms do.** Saving USD 1.10 by going to an
fp4 micro-host with no accuracy data is not worth it.

### Example 2: tool loop, 1,000 tasks × 10 steps, 60K context

This is my standard step: 54K cached, 6K new and 1.5K output. 10,000 steps give 540M cached, 60M uncached and 15M
output tokens. The second column breaks the cache (all 600M input tokens uncached). The third is Example 3: the same
loop at max effort, which I model as 6K output per step instead of 1.5K (60M output in total).

| Route | Ex. 2, cache works | Ex. 2, cache broken | Ex. 3, max effort | Generation time per step (1.5K / 6K out) |
|---|---|---|---|---|
| DeepSeek V4.1-Flash, off-peak | **USD 19.62** | USD 99.00 (5.0×) | USD 46.62 (2.4×) | 8 s / 32 s at 190 tok/s |
| DeepSeek V4.1-Flash, peak | USD 39.24 | USD 198.00 | USD 93.24 | same |
| GLM-5.3-Flash, Z.ai | **USD 32.70** | USD 97.50 (3.0×) | USD 55.20 (1.7×) | 23 s / 90 s at 66.5 tok/s |
| MiMo-V2.6-Pro, Xiaomi | USD 41.09 | USD 274.05 (6.7×) | USD 80.24 (2.0×) | 32 s / 128 s at 46.8 tok/s |
| OpenRouter V4.1-Flash fp4 (Decart) | USD 18.80 | USD 59.82 | USD 27.35 | host-dependent |
| OpenRouter V4.1-Flash fp8 (DeepInfra) | **USD 17.79** | USD 95.27 | USD 37.73 | host-dependent |
| Ollama Pro, V4.1-Flash off-peak (no cache discount assumed) | USD 99 of credits | USD 99 of credits | USD 126 of credits | host-dependent |
| Local rig, V4-Flash-0731 | USD 0 | USD 0 | USD 0 | 110 s / 441 s at 13.6 tok/s |

How the main row adds up, for DeepSeek off-peak: 540M × 0.003 = 1.62, plus 60M × 0.15 = 9.00, plus 15M × 0.60 = 9.00.

What the numbers show:

- **A cheap cached-input price beats a cheap headline price.** Once caching works, the fp8 DeepInfra endpoint is
  cheaper than the fp4 one, because its cache price is 0.004 against 0.018. The fp4 route only wins when the cache is
  broken.
- **GLM-5.3-Flash caches at 20% of its input price**, against about 2% for DeepSeek and under 1% for MiMo. That is
  why GLM is the cheapest per token in Example 1 but not in Example 2.
- **MiMo-V2.6-Pro is cheap as a planner and expensive as a worker.** Its 0.435 uncached input hurts every time the
  cache misses.
- **Ollama Pro's USD 60 of credits cover about 600 such tasks a month** if cached tokens are billed in full. The plan
  shines for GLM-5.3 (AA 45) on short contexts. At about USD 0.47 / 1.47 effective, GLM-5.3 there is in band.
- **The local rig is free, but 10,000 steps at 110 s each on 4 slots take about 76 hours** of generation. That is
  fine for an overnight queue of private work and wrong for anything else.
- **What breaks a cache:** a timestamp or a request ID at the top of the system prompt, tool lists in a changing
  order, the router switching hosts, and history rewriting (summaries that change earlier messages). I keep the
  prefix byte-stable and append only.

### Reasoning effort knobs

Max effort often buys little. DeepSeek reports that effort 60 to 80 gives most of the max accuracy at less than half
the tokens *(vendor claim)*. AA counts DeepSeek V4.1-Flash as the most verbose model it measured: 250M output tokens
on the index, against a 140M median *(third-party measurement)*. Low effort can also drop a model to the bar or
below it.

| Model | Knob | Values | Default | My setting |
|---|---|---|---|---|
| DeepSeek V4.1-Flash (first-party) | `reasoning_effort` | low / high / max (NVIDIA build: 1 to 100) | thinking on | low for routine steps, high for hard ones |
| GLM-5.3 (Z.ai) | `reasoning_effort` | low / high / max; thinking cannot be turned off | **max** | low in loops; AA is 34 at low, 45 at max |
| GLM-5.3-Flash | `reasoning_effort` | low and up | reasoning on | low; tbench.ai TB4.0 is 35.8 even at effort `none` *(third-party measurement)* |
| Step 5 Preview | `reasoning_effort` | low / medium / high | not documented in my sources | medium |
| Gemini 3.8 Flash | thinking level | low / medium / high ("minimal" errors) | not documented in my sources | medium; AA 33 at low (below the bar), 41 at high |
| Kimi K3 | none | thinking always on | on | not in band anyway; AA 30 at low |
| Qwen3.8-27B (Groq, Cerebras) | `reasoning_effort` | none / low / medium / high | high on Cerebras | AA 34 only at xhigh |
| MiMo-V2.6-Pro | not found in my sources | reasoning on | on | leave it, use for few calls |

## 6. Quality traps

**Same model, different host.** These are the strongest measured gaps *(third-party measurements)*:

| Model | Good hosts | Bad hosts | Source and date |
|---|---|---|---|
| GLM-5.3-Flash, 600 tool tasks | Fireworks 99.5%, Telnyx 99.5%, Modal 99.3%, Together 98.5%, Parasail 98.3%, Z.AI 97.5% | DeepInfra 95.5%, Novita 94.2%, **Nebius 84.8% (14.8% failures)** | openbenchmarks, 3 Sep 2026 |
| GLM-5.2, AA Endpoint Accuracy | FriendliAI, Nebius, Fireworks 100 | **Scaleway 75, DeepInfra 73 (FP4)** | AA, 26 Sep 2026 |
| gpt-oss-120b, AA Endpoint Accuracy | Bedrock 104, Nebius 102, DeepInfra Turbo 98 | **DeepInfra default 85, Together 81, Vertex 72** | AA, 26 Sep 2026 |
| GLM-5.3, AA Endpoint Accuracy | 15 hosts between 95 and 99 | none | AA, 26 Sep 2026 |
| DeepSeek V4 Pro, AA Endpoint Accuracy | 97 to 107 everywhere | none | AA snapshot, Aug 2026 |
| Kimi K2-0905, Moonshot K2VV | DeepInfra, Fireworks 100% schema | Groq: 100% schema but tool-call F1 69.52% | K2VV, 15 Nov 2025 |

- **Damage concentrates in tool calling.** In the GLM-5.2 data, BFCL tool calling fell from 37% to 22% on the worst
  endpoint while GPQA moved only about 8 points. A chat benchmark will not show you the problem.
- **Quantization is not automatically bad.** Nebius FP4 GLM-5.3 scores 99. DeepInfra FP4 GLM-5.2 scores 73. Measure
  the endpoint, not the label.
- **OpenRouter's re-ranking shows how common bad hosts are.** Auto Exacto cut GLM-5 tool errors from 8% to about 1%
  and gpt-oss-120b errors from 5.6% to 3.5% *(vendor claim)*. Before it, a 5 to 8% tool failure rate per provider was
  normal for popular models.
- **V4-Flash has no Jinja chat template**, so every host writes its own tool parser. That is one known source of the
  differences, and it applies to my local model's online copies too.

**Silent model swaps and alias IDs.**

- SiliconFlow routed `GLM-5` to GLM-5.1 and `Kimi-K2.5` to K2.6 on 11 Jun 2026. Together redirected GLM-4.6 to 4.7.
- DeepSeek's legacy `deepseek-v4-flash` names now go to V4.1-Flash (different weights, 552B). The GLM Coding Plan
  routes requests for 5.2, 5.1 and 4.7 to the newer models.
- OpenRouter aliases such as `~deepseek/deepseek-flash-latest` move to newer versions. Pin dated IDs.
- Nebius does the opposite: old IDs simply fail (deprecations on 22 Jun and 31 Aug 2026).

**Output caps** cut long reasoning or long patches, usually with `finish_reason: "length"`:

- 8K: SiliconFlow gpt-oss-120b.
- 16K: DeepInfra V4-Pro and Kimi K2.6; Groq Qwen3.8-27B.
- 32K: Vercel V4.1-Flash (32,768); Requesty Ling 3.1 Flash; Cerebras free tier.
- 64K to 65K: Step 5 Preview, Gemini 3.8 Flash, DeepInfra V4-Flash.
- 384K: DeepSeek first-party, for comparison.

**Context truncation** below the native window:

- Cerebras free tier: 64K to 65K.
- SambaNova DeepSeek-V3.2: 32K.
- Groq Qwen3.8-27B: 131K (native 256K).
- Scaleway: 256K for models that have 1M natively.
- OpenRouter Ling 3.1 Flash: 262K.
- Mistral Large 4: 524K measured against 1M claimed.

**Reasoning echo.** Kimi K3 on NVIDIA build needs `reasoning_content` and `tool_calls` sent back each turn.
Xiaomi's Anthropic-compatible endpoint returns 400 in multi-turn tool calls if the reasoning content is not passed
back. Gemini 3.x needs thought signatures returned (not re-verified). My agent loop keeps the full assistant message,
unmodified, in history.

**Tools and structured output that are ignored or rejected:**

- Inkling free on OpenRouter does not support `tool_choice`.
- Groq forum threads report gpt-oss-120b ignoring tools or inventing tool names.
- Cerebras gpt-oss-120b rejects `tools` and `response_format` in the same request.
- GPT-6 Luna on Chat Completions reportedly calls tools only at effort `none`.
- OpenRouter flags structured outputs as unsupported on several Novita and SiliconFlow endpoints. Chutes Kimi K3
  has no tools at all.

`require_parameters: true` catches some of this. The acceptance test catches the rest.

**Preview models and catalog churn.**

- Groq has removed seven models since March 2026, and its Qwen3.6-27B lasted about three months.
- Cerebras went from about 12 public models to 2.
- NVIDIA's live model list lacks IDs that its own docs still list.
- Fireworks removed V4-Flash-0731 and Kimi K2.6 from serverless on 26 Sep 2026, and Hyperbolic retired its
  serverless API on 24 Sep 2026.
- **OpenRouter free models have a median listing life of about 75 days** *(third-party measurement)*. The free list
  shrank from 24 to 16 between 21 Sep and 13 Oct 2026, and `glm-5.2:free` and `deepseek-v4-flash-0731:free` were
  among the models removed.

## 7. A 15-minute acceptance test before trusting a route

**I run it against the provider directly, not through the router, or the fallbacks will hide the failures.**

| Test | What I check | Fail means |
|---|---|---|
| Tool call | forced `tool_choice: "required"`, right name, arguments parse as JSON | the host drops or mangles tools |
| Second tool turn | full assistant message echoed, tool result in, sensible answer | reasoning-echo rules (Kimi K3, MiMo) or a broken parser |
| JSON schema | strict `json_schema`, output parses and matches the enum | no structured output: validate and retry in code, or drop the route |
| Long-context needle | a fact at 70% depth in about 100K tokens; `prompt_tokens` close to expected | silent truncation or a context cap |
| Burst | 20 parallel requests: count of 200 / 429 / 5xx codes, p50 and p95 latency | RPM or concurrency much lower than documented |
| Identity | the returned `model` field and, on OpenRouter, the `provider` field | a silent swap, or a host you did not pin |
| My own tasks | 10 to 20 tasks from my eval set, compared with local 0731 | the route is not better than what I already own |

```python
#!/usr/bin/env python3
# accept.py: acceptance test for ONE route. Call the provider directly, not the router.
# BASE_URL=https://api.z.ai/api/paas/v4 API_KEY=$ZAI_API_KEY MODEL=glm-5.3-flash python3 accept.py
# OpenRouter pinning: EXTRA='{"provider":{"order":["fireworks"],"allow_fallbacks":false}}'
import asyncio, json, os, statistics, time
from collections import Counter
from openai import AsyncOpenAI, APIStatusError

c = AsyncOpenAI(base_url=os.environ["BASE_URL"], api_key=os.environ["API_KEY"], timeout=900, max_retries=0)
M, EXTRA = os.environ["MODEL"], json.loads(os.environ.get("EXTRA", "{}"))
TOOLS = [{"type": "function", "function": {"name": "get_weather", "parameters": {
    "type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}]

async def chat(**kw):
    return await c.chat.completions.create(model=M, extra_body=EXTRA, **kw)

async def tools():
    msgs = [{"role": "user", "content": "What is the weather in Krakow? Use the tool."}]
    r = await chat(messages=msgs, tools=TOOLS, tool_choice="required")
    m = r.choices[0].message
    tc = m.tool_calls[0]
    assert tc.function.name == "get_weather" and json.loads(tc.function.arguments)["city"]
    msgs += [m.model_dump(exclude_none=True),  # keeps reasoning_content if the host sent it
             {"role": "tool", "tool_call_id": tc.id, "content": '{"temp_c": 11, "sky": "rain"}'}]
    r2 = await chat(messages=msgs, tools=TOOLS)
    assert "11" in (r2.choices[0].message.content or "")
    return f"model={r.model} provider={getattr(r, 'provider', '-')}"

async def schema():
    fmt = {"type": "json_schema", "json_schema": {"name": "triage", "strict": True, "schema": {
        "type": "object", "additionalProperties": False, "required": ["severity", "service"],
        "properties": {"severity": {"type": "string", "enum": ["low", "high"]},
                       "service": {"type": "string"}}}}}
    r = await chat(response_format=fmt, messages=[{"role": "user",
        "content": "Triage: postgres disk 100% full, writes failing."}])
    d = json.loads(r.choices[0].message.content)
    assert d["severity"] in ("low", "high")
    return str(d)

async def needle(tokens=int(os.environ.get("NEEDLE_TOKENS", "100000"))):
    lines = [f"Log line {i}: service healthy." for i in range(tokens // 9)]
    lines.insert(int(len(lines) * 0.7), "NOTE: the rollback password is plum-4417.")
    r = await chat(max_tokens=4096, messages=[{"role": "user",
        "content": "\n".join(lines) + "\n\nWhat is the rollback password? Answer with it only."}])
    assert "plum-4417" in (r.choices[0].message.content or "")
    return f"prompt_tokens={r.usage.prompt_tokens}"  # far below the expected size = truncation

async def burst(n=20):
    async def one():
        t = time.monotonic()
        try:
            await chat(max_tokens=64, messages=[{"role": "user", "content": "Say OK."}])
            return "200", time.monotonic() - t
        except APIStatusError as e:
            return str(e.status_code), time.monotonic() - t
    res = await asyncio.gather(*[one() for _ in range(n)])
    lat = sorted(t for code, t in res if code == "200")
    p = f" p50={statistics.median(lat):.1f}s p95={lat[int(len(lat) * 0.95) - 1]:.1f}s" if lat else ""
    return f"codes={dict(Counter(code for code, _ in res))}{p}"

async def main():
    for name, test in [("tools", tools), ("schema", schema), ("needle", needle), ("burst", burst)]:
        try:
            print(f"PASS {name}: {await test()}")
        except Exception as e:
            print(f"FAIL {name}: {type(e).__name__}: {str(e)[:200]}")

asyncio.run(main())
```

Before the test I look at what OpenRouter itself reports for the hosts:

```bash
curl -s https://openrouter.ai/api/v1/models/z-ai/glm-5.3-flash/endpoints \
  | jq '.data.endpoints[]|{provider_name,quantization,pricing,uptime_last_1d}'
```

**My acceptance rule:** all four tests pass, the burst shows no 5xx, and on my own tasks the route is at least as
good as local 0731 on pass rate. For the eval half see
[../course_agentic_apps/14-EVALUATION.md](../course_agentic_apps/14-EVALUATION.md). In production I want the
tool-parse failure rate under about 2%. The best hosts above failed 0.5 to 2.5% of the GLM-5.3-Flash tasks, and
Nebius failed 14.8%.

## 8. Terms and data

### Flat plans: own agent allowed or not

| Plan | Price (13 Oct 2026) | Own agent or backend? | What the terms say |
|---|---|---|---|
| GLM Coding Plan | USD 18 / 80 / 168 a month (third-party; official "from USD 18") | **No** | "may only be used within officially supported tools and products"; more than 3 violations means a ban; no refunds |
| Kimi Code | USD 19 / 39 / 99 / 199 a month | **No** in a product, grey in your own agent | changing the User-Agent "is considered a violation"; for your own product "visit the Kimi Platform" |
| Alibaba Coding Plan Pro | USD 50 a month | **No** | "Do not use the plan's API key for automated scripts, application backends, or other non-interactive scenarios" |
| MiMo Token Plan | USD 6 to 100 a month | **No** | "only available for use in programming tools" and "prohibited" for "automated scripts and custom application backends" |
| MiniMax M Plan | USD 22 / 55 / 132 a month | interactive only | "designed for individual, interactive developer use"; PAYG recommended for production |
| Fireworks Fire Pass | closed to new subscribers | **No** | personal and coding-harness use only |
| Ollama Cloud Pro | USD 20 a month, includes USD 60 of credits | **Yes** | no restriction to coding tools in the docs |
| StepFun Step Plan | USD 6.99 to 99 a month (third-party) | claimed yes | launch post: "works with Cursor, Windsurf, Cline, and your own stack"; check the ToS, credit conversion unknown |

The math on a restricted plan can look great. The GLM Coding Plan Lite works out to about 590 of my standard steps a
week. That does not matter, because the plan forbids the use. **For my own agents I use PAYG keys or Ollama Cloud.**
The restricted plans are fine inside the tools they name, such as Claude Code or OpenCode on GLM.

### Training and hosting flags (a flag, not a judgement)

| Route | Trains on prompts | Hosted |
|---|---|---|
| DeepSeek API | opt-out (on by default, third-party reading of the policy) | PRC |
| Z.ai API (PAYG) | no (opt-in only, per its DPA) | Singapore entity |
| Xiaomi MiMo PAYG | no by default (third-party summaries) | Netherlands and Singapore entities |
| Kimi platform | yes, no product-level opt-out | Singapore (third-party reading) |
| NVIDIA build trial | may be used to improve NVIDIA products | US (assumed) |
| Kilo free models | may train (Kilo flags every free model) | unknown |
| OpenCode Zen free | Step 5: no (zero retention); Ling and MiMo-Flash: yes | US and EU |
| Requesty free Ling 3.1 Flash | no (catalog metadata) | EU endpoint, upstream Novita |
| OpenRouter | per endpoint; `data_collection: "deny"` filters | host-dependent |
| Gemini API free tier, from Poland | no (EEA gets the paid-service terms) | Google |
| Mistral Free | yes unless opted out | EU |
| Ollama Cloud | no ("never logged or trained on", vendor claim) | mostly US |
| DeepInfra | no | US |
| Together | stored by default, training opt-in | US |
| Fireworks | not stored for open models by default | global unless the US endpoint is used |
| Meta Muse Spark Contributor, OpenAI data-sharing tokens | **yes, that is the deal** | US |

**EEA notes.**

- **Gemini:** in the EEA, Switzerland and the UK, the paid-service data terms apply to the free tier too, so my free
  prompts are not used for training. But the same terms say "You may use only Paid Services when making API Clients
  available to users in the European Economic Area". So the free tier is for my own development and testing, and an
  app with EU users must be on the paid tier.
- **Mistral:** since 5 Aug 2026 (7 Aug in the EU) the API is limited to business customers. Individuals may no longer
  use it for personal projects.
- **Nebius:** public serverless runs in region "Global", with the processing location able to change without
  notice. EU residency comes only with dedicated endpoints.
- **OpenRouter:** EU in-region routing is only on Business and Enterprise plans.
- **EU-hosted options:** Requesty's EU endpoint, Scaleway (Paris), OVHcloud (Gravelines) and Mistral-hosted GLM-5.3
  on `api.eu.mistral.ai` (+10%).

**Client data stays local.** It does not matter that a route says "no training". Client and professional data does
not leave the rig, and the private pipeline does not even know the router exists. The wider rules are in
[../ai-assistants/README.md](../ai-assistants/README.md). Prompt injection through tool output is a separate risk on
every leg: see [../course_agentic_apps/16-SECURITY-OWASP-ASI.md](../course_agentic_apps/16-SECURITY-OWASP-ASI.md).

## 9. Monitoring and kill switches

**Budgets, in three layers:**

1. **Prepaid balances are the hard stop.** I top up DeepSeek, Z.ai, Xiaomi, DeepInfra and OpenRouter with small
   amounts and keep auto-recharge off. Together, Kimi and StepFun are prepaid anyway. Vercel budgets return 402
   `quota_for_entity_exceeded`. `curl -s https://openrouter.ai/api/v1/key -H "Authorization: Bearer $OPENROUTER_API_KEY"`
   shows the key's limits.
2. **Router budgets.** Each app gets its own LiteLLM virtual key with a `max_budget` and a `budget_duration`, so one
   runaway agent cannot spend the month.
3. **Per-task caps in the app.** I set a maximum number of steps, `max_tokens` per call and a wall-clock limit per
   task. A loop that does not converge costs money on every leg except local.

**What I track per route (per deployment, not per group):**

- HTTP success rate and the mix of error codes.
- Tool-call parse failure rate and schema-valid rate.
- Task pass rate from the eval.
- p50 and p95 latency, and time to first token.
- Output tokens per task, which catches verbosity drift after a silent model upgrade.
- Cache-hit ratio from `usage`. If it drops, the bill grows by 3 to 7 times.
- Cost per task.
- The returned `model` field (and `provider` on OpenRouter) compared with what I pinned.

**My alert thresholds:**

| Signal | Alert when | Usual cause |
|---|---|---|
| 429 rate | above 10% over 15 minutes | quota gone, or another tenant on a shared free pool |
| 5xx or timeouts | above 2% | host trouble, NVIDIA queueing, Chutes "maximum capacity" |
| 400 | any rise after a change | missing reasoning echo, parameter not supported |
| 402 | any | budget reached or negative balance (OpenRouter returns 402 even on free models) |
| 403 | any | Kimi Code quota or concurrency, Vercel card verification |
| Provider-specific | any | Groq 498 `capacity_exceeded` (Flex); Z.ai 1113 "Insufficient balance" (wrong endpoint) |
| Tool-parse failures | above 2% over 100 calls | host change or a quantized endpoint |
| Output tokens per task | +50% week over week | model swapped behind an alias |

**Kill switches.** Each group can be switched off without a deploy. I remove the deployment through the LiteLLM admin
API or comment it out and reload. A fallback I no longer trust gets deleted, not just ignored. Every provider key is
revocable on its own, so one leak does not take down the rest.

**Re-check cadence:**

- **Monthly**, for every route I use: the acceptance test and my eval set, the OpenRouter `/endpoints` data
  (quantization, uptime, price), the deprecation pages (Groq, Cerebras, Nebius, Fireworks changelog) and the data
  terms.
- **Weekly**, for free promos: Step 5 Preview free, the OpenRouter free list, OpenCode Zen.
- **Dates already on my calendar:**
  - Step 5 Preview open weights: due 15 Oct 2026.
  - Poolside Laguna S 2.1 free on Vercel: deprecated 31 Oct 2026.
  - GLM-5.2 on Mistral: retires 31 Oct 2026.
  - Gemini 3.8 Flash price: doubles to USD 1.50 / 7.50 on 1 Jan 2027.
  - Mistral Large 4: its launch discount (about two weeks from 6 Oct 2026) ends soon.
- **Recent reminders of why this matters:** Fireworks raised the V4.1-Flash price on 1 Oct 2026, and LLM7 cut its
  free quota on 7 Oct 2026. Hugging Face removed its free credits on 7 Oct 2026, and Mistral dropped the stated free
  credit the same day.

**Everything in this file changes. I rerun the numbers and the tests before I trust them again.**

**Sources:** [OpenRouter limits](https://openrouter.ai/docs/api/reference/limits) · [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection) ·
[OpenRouter pricing](https://openrouter.ai/pricing) · [OpenRouter models API](https://openrouter.ai/api/v1/models) · [OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection) ·
[OpenRouter Auto Exacto](https://openrouter.ai/blog/announcements/auto-exacto/) · [TrueFoundry on OR free models](https://www.truefoundry.com/blog/openrouter-free-models-whats-actually-free-and-what-it-costs-you) ·
[OR free-model tracker](https://github.com/cyclez2000/openrouter-free-models/issues/82) · [Vercel AI Gateway pricing](https://vercel.com/docs/ai-gateway/pricing) ·
[Requesty pricing](https://www.requesty.ai/pricing) · [Requesty quickstart](https://docs.requesty.ai/quickstart) · [Kilo Gateway docs](https://kilo.ai/docs/gateway) ·
[Kilo Gateway models](https://api.kilo.ai/api/gateway/models) · [OpenCode Zen docs](https://opencode.ai/docs/zen/) · [Puter rate limits](https://docs.puter.com/rate-limits-and-quotas/) ·
[LLM7 limits](https://docs.llm7.io/limits.md) · [Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) ·
[Gemini API terms](https://ai.google.dev/gemini-api/terms) · [Gemini free tier measured](https://dev.to/romeroyang/geminis-free-tier-measured-20-requests-a-day-and-google-no-longer-publishes-the-number-4gf2) ·
[Antigravity suspensions](https://preuve.ai/blog/antigravity-review) · [NVIDIA free API test](https://dev.to/klukyanov/kimi-k3-deepseek-and-glm-free-from-nvidia-i-tested-the-claim-and-here-is-the-catch-2m9b) ·
[NVIDIA forum timeouts](https://forums.developer.nvidia.com/t/all-new-model-are-timeout/368931) · [NVIDIA trial terms summary](https://standardcompute.com/providers/nvidia) ·
[Cloudflare Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/) · [Alibaba free quota](https://www.alibabacloud.com/help/en/model-studio/new-free-quota) ·
[Groq rate limits](https://console.groq.com/docs/rate-limits) · [Groq deprecations](https://console.groq.com/docs/deprecations) · [Groq gpt-oss tools thread](https://community.groq.com/t/gpt-oss-120b-ignoring-tools/385) ·
[Cerebras rate limits](https://inference-docs.cerebras.ai/support/rate-limits) · [Cerebras gpt-oss limitations](https://inference-docs.cerebras.ai/models/openai-oss) ·
[SambaNova models](https://docs.sambanova.ai/cloud/docs/get-started/supported-models) · [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) ·
[DeepSeek rate limit](https://api-docs.deepseek.com/quick_start/rate_limit) · [DeepSeek data policy reading](https://meetily.ai/llm-privacy/deepseek) · [Z.ai pricing](https://docs.z.ai/guides/overview/pricing) ·
[GLM Coding Plan overview](https://docs.z.ai/devpack/overview.md) · [GLM Coding Plan usage policy](https://docs.z.ai/devpack/usage-policy) · [Z.ai DPA summary](https://standardcompute.com/providers/z-ai) ·
[Kimi Code docs](https://www.kimi.com/code/docs/en/) · [Kimi Code errors](https://www.kimi.com/code/docs/en/kimi-code/error-reference.html) · [Kimi data policy](https://www.cometapi.com/is-kimi-safe-to-use/) ·
[Alibaba Coding Plan](https://www.alibabacloud.com/help/en/model-studio/coding-plan) · [MiMo Token Plan](https://mimo.mi.com/docs/en-US/tokenplan/Token%20Plan/subscription) ·
[MiMo reasoning echo](https://kingy.ai/blog/mimo-v2-6-pro-free-access-pricing-setup/) · [MiMo pricing](https://www.eesel.ai/blog/xiaomi-mimo-v2-6-pricing) · [MiniMax M Plan FAQ](https://platform.minimax.io/docs/m-plan/faq.md) ·
[StepFun pricing](https://platform.stepfun.ai/docs/en/guides/pricing/details) · [StepFun Step Plan post](https://x.com/StepFun_ai/status/2035815197584023835) · [Ollama pricing](https://ollama.com/pricing) ·
[Mistral business-only API](https://agentdeals.dev/vendor/mistral-ai) · [Fireworks Fire Pass](https://docs.fireworks.ai/firepass) · [Fireworks changelog](https://docs.fireworks.ai/updates/changelog) ·
[DeepInfra rate limits](https://docs.deepinfra.com/account/rate-limits) · [DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy) · [Together ZDR](https://docs.together.ai/docs/zero-data-retention) ·
[Together changelog](https://docs.together.ai/docs/changelog) · [Nebius public serverless](https://docs.tokenfactory.nebius.com/public-serverless.md) ·
[Scaleway supported models](https://raw.githubusercontent.com/scaleway/docs-content/main/pages/generative-apis/reference-content/supported-models.mdx) ·
[SiliconFlow review](https://dev.to/gretavolkov/siliconflow-api-review-2026-setup-models-and-real-pricing-1gdo) · [AA Endpoint Accuracy Index](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) ·
[AA GLM-5.2 providers](https://artificialanalysis.ai/models/glm-5-2/providers) · [AA gpt-oss-120b providers](https://artificialanalysis.ai/models/gpt-oss-120b/providers) ·
[openbenchmarks same-model accuracy](https://openbenchmarks.com/inference/same-model-different-accuracy) · [K2 Vendor Verifier](https://github.com/MoonshotAI/K2-Vendor-Verifier) ·
[AA leaderboard v4.3.2](https://artificialanalysis.ai/leaderboards/models) · [AA V4.1-Flash](https://artificialanalysis.ai/models/deepseek-v4-1-flash) · [AA GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash) ·
[AA MiMo-V2.6-Pro](https://artificialanalysis.ai/models/mimo-v2-6-pro) · [DeepSeek-V4.1-Flash paper](https://arxiv.org/pdf/2609.19969) · [HF V4-Flash-0731 card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) ·
[HF GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash) · [tbench.ai leaderboard](https://www.tbench.ai/leaderboard) · [computingforgeeks GPT-6 Luna](https://computingforgeeks.com/gpt-6-sol-luna-released-features-benchmarks/)
