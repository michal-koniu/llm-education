# Cheap and free online models for agents — the top 20 routes (Oct 2026)

My agentic apps stand on three legs: commercial frontier APIs (Claude Opus as the planner), my local rig
(4× AMD Radeon AI PRO R9700 running DeepSeek-V4-Flash-0731), and **cheap or free online models**. This survey is about
the third leg: where to get inference online for little or no money on models **at least as smart as my local
DeepSeek-V4-Flash**, and how far you can trust it in an agent loop.

All facts, prices and limits were checked on **13 Oct 2026**. This market changes every week: re-check before you
build on any number here. Only non-sensitive data goes to these routes. Client and professional data stays on local
models (see [../ai-assistants/README.md](../ai-assistants/README.md)).

## The shortest answer

- **The bar is AA 34.** That is DeepSeek-V4-Flash-0731 on the Artificial Analysis Intelligence Index v4.3.2 ("AA").
  The original April V4-Flash scores 24 and V4.1-Flash 39 on the same index. Always compare numbers from one index
  version only; details in [02-MODELS.md](02-MODELS.md).
- **"Free" mostly means "below the bar" now.** The free models still left on OpenRouter (Inkling, Nemotron 3 Ultra,
  gpt-oss-120b, Gemma 4) score AA 12–26. GitHub Models was retired on 30 Jul 2026, Hugging Face dropped free credits on
  7 Oct 2026, Qwen Code's free tier ended on 15 Apr 2026.
- **"Cheap" is the real third leg.** GLM-5.3-Flash (AA 42) costs USD 0.15 / 0.50 per 1M tokens, DeepSeek V4.1-Flash
  (AA 39) USD 0.15 / 0.60 off-peak, MiMo-V2.6-Pro (AA 46) USD 0.435 / 0.87. A thousand long agent tasks cost single
  dollars to tens of dollars.
- **The strongest free route is NVIDIA build.nvidia.com** (GLM-5.3, Kimi K3, V4.1-Flash for free at about 40 RPM),
  but its terms allow prototyping only and it queues under load.
- **The host matters as much as the model.** The same GLM model scored 73% on one host and 100% on another in
  Artificial Analysis' endpoint accuracy test. Pin providers and quantization, run an acceptance test first
  ([03-AGENTIC-USE.md](03-AGENTIC-USE.md)).
- **Flat coding plans are mostly not for your own agents.** GLM Coding Plan, Kimi Code, Alibaba Coding Plan and the
  MiMo Token Plan restrict use to supported coding tools. Ollama Cloud allows API use.
- **My default:** OpenRouter as the router with pinned providers, GLM-5.3-Flash and DeepSeek V4.1-Flash as cheap
  workers, MiMo-V2.6-Pro or GLM-5.3 for harder steps, free tiers only as overflow and for evaluation.

## Ranking: the top 20

Score out of 100 (method below). Price = USD per 1M tokens, input / output, for the best in-band model. "Data" is a
flag only (does the route train on prompts by default), not part of the score.

| # | Route | Type | Best models in band (AA) | Price or free allowance | Data | Score |
|---|---|---|---|---|---|---|
| 1 | [OpenRouter](01-PROFILES.md#1-openrouter) | aggregator, pay-as-you-go | MiMo-V2.6-Pro (46), GLM-5.3 (45), GLM-5.3-Flash (42) | from 0.045 / 0.15; 1,000 free req/day after a one-time USD 10 | per provider; toggles | 93 |
| 2 | [DeepInfra](01-PROFILES.md#2-deepinfra) | host, pay-as-you-go | MiMo-V2.6-Pro (46), V4.1-Flash (39), V4-Flash-0731 (34) | 0.06 / 0.18 (0731) to 0.435 / 0.87 | no training | 90 |
| 3 | [Fireworks AI](01-PROFILES.md#3-fireworks-ai) | host, pay-as-you-go | GLM-5.3-Flash (42), V4.1-Flash (39) | 0.15 / 0.50 | not stored | 89 |
| 4 | [Z.ai (GLM) API](01-PROFILES.md#4-zai-glm-api) | first-party | GLM-5.3-Flash (42) | 0.15 / 0.50 | no training (API) | 87 |
| 5 | [Parasail](01-PROFILES.md#5-parasail) | host, pay-as-you-go | GLM-5.3-Flash (42), V4-Flash-0731 (34) | 0.14 / 0.28 (0731) | unknown | 87 |
| 6 | [DeepSeek API](01-PROFILES.md#6-deepseek-api) | first-party | V4.1-Flash (39) | 0.15 / 0.60 off-peak, 0.30 / 1.20 peak | trains by default, opt-out; PRC | 85 |
| 7 | [Alibaba Cloud Model Studio](01-PROFILES.md#7-alibaba-cloud-model-studio-international) | first-party + trial | Qwen3.8-Max, GLM-5.3 (45) on trial; Qwen3.8-Flash (40) | 1M free tokens per model for 90 days; 0.15 / 0.47 | no training; Singapore | 85 |
| 8 | [Xiaomi MiMo API](01-PROFILES.md#8-xiaomi-mimo-api) | first-party | MiMo-V2.6-Pro (46) | 0.435 / 0.87 | no training (third-party summary) | 83 |
| 9 | [Together AI](01-PROFILES.md#9-together-ai) | host, pay-as-you-go | GLM-5.3-Flash (42), V4-Flash-0731 (34) | 0.14 / 0.28 (0731) | stored by default, ZDR toggle | 82 |
| 10 | [NVIDIA build.nvidia.com](01-PROFILES.md#10-nvidia-buildnvidiacom-nim-trial-api) | free trial API | GLM-5.3 (45), Kimi K3 (44), V4.1-Flash (39) | free, ~40 RPM, prototyping only | may be used to improve | 79 |
| 11 | [Vercel AI Gateway](01-PROFILES.md#11-vercel-ai-gateway) | aggregator + free credit | GLM-5.3-Flash (42) | USD 5 free every 30 days | assume trains unless ZDR | 77 |
| 12 | [Kilo Gateway](01-PROFILES.md#12-kilo-gateway) | free promo | Step 5 Preview (44), Ling 3.1 Flash (41) | free, 200 req/hour per IP, no key | may train | 75 |
| 13 | [Ollama Cloud](01-PROFILES.md#13-ollama-cloud) | flat plan with credits | GLM-5.3 (45), Kimi K3 (44) | Pro USD 20/month = USD 60 credits | never logged | 74 |
| 14 | [Requesty](01-PROFILES.md#14-requesty) | aggregator, free tier | Ling 3.1 Flash (41) | 200 free req/day, no card; EU endpoint | no retention (metadata) | 72 |
| 15 | [Scaleway Generative APIs (EU)](01-PROFILES.md#15-scaleway-generative-apis-eu) | EU host | V4.1-Flash (39) | EUR 0.60 / 1.80; 1M free tokens once | no retention; Paris | 72 |
| 16 | [StepFun API and Step Plan](01-PROFILES.md#16-stepfun-api-and-step-plan) | first-party + flat | Step 5 Preview (44) | 1.00 / 2.70; plan from USD 6.99 | unknown | 71 |
| 17 | [OpenCode Zen](01-PROFILES.md#17-opencode-zen) | free promo | Muse Spark 1.3 Contributor (45, trains), Step 5 Preview (44) | free, unpublished limits | per model | 70 |
| 18 | [Gemini API free tier](01-PROFILES.md#18-google-gemini-api-free-tier) | free tier | Gemini 3.8 Flash (41) | free, ~20 req/day | no training in the EEA | 68 |
| 19 | [Groq (free tier)](01-PROFILES.md#19-groq-free-tier) | free tier | Qwen3.8-27B (34) | free, 1,000 req/day, 200K tokens/day | no retention by default | 66 |
| 20 | [Cerebras Inference](01-PROFILES.md#20-cerebras-inference) | trial + pay-as-you-go | Qwen3.8-27B (34) at ~1,850 tok/s | 0.99 / 1.49; trial 1M tokens/day | no retention | 66 |

## How I scored

| Criterion | Points | What counts |
|---|---|---|
| Model quality | 30 | AA of the best model you can actually use on this route within budget: AA 34 = 18 points, +1 per AA point, 30 at AA 46 or more |
| Effective cost | 20 | recurring free = 20; promo or one-time free 16–18; pay-as-you-go by output price (≤0.6 → 18–19, ≤1 → 16, ≤2 → 13, ≤3 → 10–11) |
| Limits | 15 | usable volume for agent loops: RPM, requests and tokens per day, concurrency |
| Agent fit | 20 | tool calling, context and max output, OpenAI/Anthropic-compatible endpoints, structured output, measured tool-call accuracy |
| Reliability | 15 | uptime data, catalog churn, preview status, how often limits or terms changed |

"In band" means output at most about USD 3 per 1M tokens, or a free or flat route. Data terms are shown as a flag
because I only send non-sensitive data here.

## Which route for which job

| Job | First choice | Fallback |
|---|---|---|
| Bulk extraction, classification, summaries | GLM-5.3-Flash at Fireworks or Z.ai | V4-Flash-0731 at DeepInfra (0.06 / 0.18) |
| Coding sub-agent, terminal tasks | GLM-5.3 via OpenRouter hosts (best independent Terminal-Bench 4.0) | GLM-5.3-Flash, MiMo-V2.6-Pro |
| Tool-heavy loops | GLM-5.3-Flash on a host with measured tool accuracy (Fireworks, Together, Parasail) | DeepSeek V4.1-Flash first-party |
| Long-context reading (up to 1M) | DeepSeek V4.1-Flash (1M context, 384K output) | Gemini 3.8 Flash free tier for occasional jobs |
| Evaluation and experiments for free | NVIDIA build.nvidia.com, Kilo Gateway, Requesty | Alibaba trial tokens |
| Hard steps without paying Opus prices | MiMo-V2.6-Pro (AA 46) | GLM-5.3 through Ollama Cloud credits |
| Anything with client data | local rig only | — |

## What did not make it

- **Below the bar but free:** OpenRouter's free models (Inkling, Nemotron 3 Ultra, Gemma 4, gpt-oss-120b), Cloudflare
  Workers AI free (gpt-oss-120b only), SambaNova free (20 requests/day; MiniMax-M3 AA 29 is paid), LLM7 (100K tokens/day).
- **Gone in 2026:** GitHub Models (retired 30 Jul), Hyperbolic serverless (24 Sep), Qwen Code free OAuth (15 Apr),
  Hugging Face free credits (7 Oct), Pollinations hourly free credits (10 Jul), Cerebras Code plans (sold out).
- **Above the bar but not cheap:** Kimi K3 (AA 44, USD 9.50+ output), Qwen3.8-Max, Grok 4.7, the large GPT models.
- **Cheap closed models:** Claude Haiku 5.5 (AA 34 at default effort, 43 at max), GPT-6 Luna (AA 38 at max) and Muse Spark 1.3 Contributor (AA 45 at its highest allowed effort, trains
  on prompts) are covered in [02-MODELS.md](02-MODELS.md). They belong to the commercial leg of my stack.
- **Good hosts just outside the top 20:** Novita, SiliconFlow, Nebius Token Factory (poor tool-task score on
  GLM-5.3-Flash), Baseten, GMI Cloud, Chutes, Hugging Face router, Mistral (API for business customers only since Aug 2026).

## Files

| File | Contents |
|---|---|
| [01-PROFILES.md](01-PROFILES.md) | the 20 routes: access, limits, prices, models, agent fit, reliability, catches, verification snippet |
| [02-MODELS.md](02-MODELS.md) | which models really reach DeepSeek-V4-Flash level, benchmarks, picks per role |
| [03-AGENTIC-USE.md](03-AGENTIC-USE.md) | how to combine local, free, cheap and commercial: router config, cost math, traps, acceptance test |
| [SOURCES.md](SOURCES.md) | all sources with what I took from each |

## Related parts of this repo

- [../agent-harnesses/README.md](../agent-harnesses/README.md) — which harness to run these models in.
- [../course_agentic_apps/17-HYBRID-AND-ROUTER.md](../course_agentic_apps/17-HYBRID-AND-ROUTER.md) — building the router.
- [../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md](../course_local_models/10-HYBRID-LOCAL-PLUS-CLAUDE.md) — local plus cloud.

Polish version: [../../pl/tanie-i-darmowe-modele/README.md](../../pl/tanie-i-darmowe-modele/README.md).
