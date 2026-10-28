# Profiles: the top 20 cheap and free online routes

Twenty access routes, ranked by score (see [README.md](README.md#how-i-scored)). Every entry has the same sections, so
you can compare them side by side. Facts and prices as of **13 Oct 2026**; "AA" is the Artificial Analysis
Intelligence Index v4.3.2, where my local DeepSeek-V4-Flash-0731 scores **34** (the bar). Model background is in
[02-MODELS.md](02-MODELS.md), how to combine the routes in an agent is in [03-AGENTIC-USE.md](03-AGENTIC-USE.md).

---

## 1. OpenRouter

**Type:** pay-as-you-go (free tier exists, models below the bar) · **Best models:** `xiaomi/mimo-v2.6-pro` AA 46, `z-ai/glm-5.3` AA 45, `z-ai/glm-5.3-flash` AA 42, `deepseek/deepseek-v4.1-flash` AA 39 · **Score: 93** (Q30 C17 L14 A19 R13) · **Data:** trains on prompts: depends on the host you land on (free endpoints: mostly "may train"); OpenRouter itself stores no prompts unless you opt in; hosted wherever the chosen provider runs, EU in-region routing only on Business/Enterprise

> One key, one OpenAI-compatible URL and 30+ hosts per strong open model: the cheapest and most flexible way to reach MiMo-V2.6-Pro, GLM-5.3(-Flash) and V4.1-Flash, with fallbacks and tool-call-aware routing built in.

**What you get.**
- Pay-as-you-go credits. Token prices are the providers' own prices passed through; OpenRouter adds a **5.5% fee on credit purchases** (Standard plan, 13 Oct 2026).
- **The strong models are not free.** On 13 Oct 2026 none of DeepSeek, GLM, Kimi, Qwen, MiniMax or MiMo has a `:free` variant. The best free models (Inkling Small AA 26, Inkling AA 25, Nemotron 3 Ultra AA 23) sit below my bar of AA 34 (my local DeepSeek-V4-Flash-0731).
- The paid routes are near-free: GLM-5.3-Flash from USD 0.045 / 0.15, V4.1-Flash from USD 0.09 / 0.18, MiMo-V2.6-Pro at USD 0.43 / 0.87 per 1M tokens (input / output), 13 Oct 2026.
- **A one-time USD 10 purchase** lifts the free-model quota from 50 to 1,000 requests/day for good.

**Models.** Cheapest live endpoints, 13 Oct 2026, prices USD per 1M (input / output).

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `xiaomi/mimo-v2.6-pro` | 46 | 1M | 943k (DeepInfra) | check `/endpoints` | DeepInfra fp8 0.43 / 0.87, cached 0.004, 1-day uptime 100%; Xiaomi fp8 0.435 / 0.87, uptime 95.9%; only 4 hosts, slow (~42–47 t/s) |
| `z-ai/glm-5.3` | 45 | 1M | 128k (Z.ai) | yes | Baidu fp8 0.599 / 1.883; Inceptron fp4 0.60 / 1.883; SiliconFlow and Novita fp8 0.70 / 2.20; Z.ai 1.40 / 4.40 is over budget; reasoning always on |
| `z-ai/glm-5.3-flash` | 42 | 1M | 128k (StreamLake) | yes, parallel calls | 32 providers; StreamLake fp8 0.045 / 0.15, uptime 99.6%; DeepInfra fp4 0.075 / 0.25; Z.ai 0.15 / 0.50; `:batch` 0.06 / 0.20 |
| `deepseek/deepseek-v4.1-flash` | 39 | 1M | 131k (DeepInfra) | yes | 32 providers; Decart fp4 0.09 / 0.18; DeepInfra fp8 0.14 / 0.42; DeepSeek 0.15 / 0.60, uptime 100%; `:batch` 0.112 / 0.336 |
| `deepseek/deepseek-v4-flash-0731` | 34 | 1M | 384k (DeepInfra) | yes | my local model in the cloud: DeepInfra fp8 0.06 / 0.18, uptime 100%; useful for A/B against the rig |

**Limits and prices.**
- Free models: **20 RPM** always; **50 requests/day** while lifetime credit purchases are below USD 10; **1,000 requests/day** after USD 10 (one-time threshold, not a subscription). A negative balance returns 402 even on free models. Failed free requests can count against the daily quota *(third-party measurement)*.
- Paid models: provider price + 5.5% purchase fee (Business plan 8%). BYOK: the first USD 25,000/month of list-price inference is fee-free, then 5%.

**How to get access.**
1. Sign up at openrouter.ai with email or OAuth. No region block noted for Poland/EU.
2. A card is needed only to buy credits. Buy USD 10 once: it unlocks 1,000 free requests/day and funds months of near-free paid calls.
3. In account privacy settings, decide on the paid and free "may train" toggles separately. Turning off free endpoints that may train makes about 9 free models unreachable (404 "No endpoints found matching your data policy").
4. Create an API key and export it as `OPENROUTER_API_KEY`. `GET /api/v1/key` shows your limits and free-tier status.

**Agent fit.**
- OpenAI-compatible base URL `https://openrouter.ai/api/v1`. Anthropic-compatible `/api/v1/messages` exists (a probe returned an Anthropic-shaped 401), so `ANTHROPIC_BASE_URL=https://openrouter.ai/api` works for Anthropic-SDK harnesses.
- **Provider routing is the killer feature:** `provider.order`, `only`, `ignore`, `allow_fallbacks` (default true), `require_parameters`, `quantizations` (e.g. `["fp8","bf16"]`), `sort`, `max_price`, `preferred_min_throughput`, `preferred_max_latency`, `zdr`, `data_collection`; top-level `models: [...]` fallback list.
- **Auto Exacto** (since 12 Mar 2026, updated 24 Jun 2026) is on by default for every request with `tools`: it re-ranks providers about every 5 min on throughput, tool-call telemetry and internal benchmarks. Reported tool-error cuts: GLM-5 −88% (8% to ~1%), gpt-oss-120b −36%, DeepSeek V3.2 −16% *(vendor claim)*. `:exacto` (Oct 2025) = curated tool-calling providers, +10–20% on Tau2Bench/LiveMCPBench *(vendor claim)*.
- Set **`require_parameters: true`** so a tool call never lands on a host that ignores `tools` or `response_format` (BaseTen V4-Flash endpoints lack structured outputs, Relace lacks tools).

**Reliability.**
- Status page at status.openrouter.ai (JS page). Per-endpoint 1-day uptime is exposed in the `/endpoints` API.
- Cheapest hosts are often the flakiest: Baidu V4-Flash 94.0%, Chutes GLM-5.1 57.5%, GMICloud MiMo-Flash 42.9% (13 Oct 2026).
- **Free-model churn is high:** `z-ai/glm-5.2:free` removed 7 Sep 2026, `deepseek/deepseek-v4-flash-0731:free` removed 21 Sep 2026; free count fell from 24 (21 Sep) to 16 (13 Oct); median listing life of a free model ~75 days *(third-party measurement)*.

**Limitations.**
- Nothing at or above AA 34 is free; the free tier is a fallback for AA 23–26 models at best.
- 50 requests/day without the USD 10 top-up is useless for agent loops.
- With default routing you can land on an fp4 endpoint you never evaluated; you must set `quantizations` / `only` yourself.

**Where it fits in my stack.**
- **Default gateway for the cheap leg:** one key for GLM-5.3-Flash (bulk tool loops), V4.1-Flash (same family as my rig, stronger) and MiMo-V2.6-Pro (hardest sub-tasks), with a `models` fallback list.
- Planner stays on Claude Opus; OpenRouter models are sub-agents and bulk workers (see [17-HYBRID-AND-ROUTER.md](../course_agentic_apps/17-HYBRID-AND-ROUTER.md)).
- Eval runner: the same prompt across hosts and quantizations in one script ([14-EVALUATION.md](../course_agentic_apps/14-EVALUATION.md)).

**Verify yourself.**

```bash
# per-host price, quantization and uptime for one model
curl -s https://openrouter.ai/api/v1/models/deepseek/deepseek-v4.1-flash/endpoints \
  | jq '.data.endpoints[]|{provider_name,quantization,pricing,uptime_last_1d}'
# tool call on GLM-5.3-Flash, fp8+ only, hosts that honour every parameter
curl -s https://openrouter.ai/api/v1/chat/completions -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H 'Content-Type: application/json' -d '{
  "model":"z-ai/glm-5.3-flash",
  "messages":[{"role":"user","content":"Weather in Warsaw?"}],
  "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}],
  "provider":{"require_parameters":true,"quantizations":["fp8","bf16"]}}'
```

**Sources:** [OpenRouter models API](https://openrouter.ai/api/v1/models) · [OpenRouter endpoints API](https://openrouter.ai/api/v1/models/deepseek/deepseek-v4.1-flash/endpoints) · [OpenRouter limits](https://openrouter.ai/docs/api/reference/limits) · [OpenRouter pricing](https://openrouter.ai/pricing) · [OpenRouter BYOK](https://openrouter.ai/docs/guides/overview/auth/byok) · [OpenRouter provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging) · [OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection) · [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection) · [Auto Exacto](https://openrouter.ai/blog/announcements/auto-exacto/) · [Exacto](https://openrouter.ai/blog/announcements/provider-variance-introducing-exacto/) · [TrueFoundry on OR free models](https://www.truefoundry.com/blog/openrouter-free-models-whats-actually-free-and-what-it-costs-you) · [OR free-model tracker](https://github.com/cyclez2000/openrouter-free-models/issues/82) · [AA Endpoint Accuracy Index](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · [Z.ai pricing](https://docs.z.ai/guides/overview/pricing)

---

## 2. DeepInfra

**Type:** pay-as-you-go · **Best models:** `xiaomi/mimo-v2.6-pro` AA 46 (via OpenRouter data), `zai-org/GLM-5.3-Flash` AA 42, `deepseek-ai/DeepSeek-V4.1-Flash` AA 39, `deepseek-ai/DeepSeek-V4-Flash-0731` AA 34 · **Score: 90** (Q30 C19 L14 A15 R12) · **Data:** trains on prompts: no; input not stored to disk, metadata-only logging *(vendor claim)*; US-hosted (location not stated in the privacy doc)

> The price floor of the US open-weight hosts: my own local model V4-Flash-0731 at USD 0.06 / 0.18 and V4.1-Flash at USD 0.20 / 0.60, with OpenAI- and Anthropic-compatible endpoints and no training on prompts.

**What you get.**
- Plain pay-as-you-go serverless inference, billed per token; card or prepay needed for real use.
- **Cheapest strong DeepSeek anywhere I found** (13 Oct 2026): V4-Flash-0731 USD 0.06 / 0.18 per 1M (input / output), cached 0.015; V4.1-Flash USD 0.20 / 0.60, cached 0.006.
- GLM-5.3-Flash at the reference USD 0.15 / 0.50 (cached 0.03), but **FP4**.
- Free credit: third-party pages claim "USD 5 free, 90 days"; not in the official docs, treat as unverified.

**Models.** Direct-API prices, USD per 1M (input / output), 13 Oct 2026.

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `xiaomi/mimo-v2.6-pro` | 46 | 1M | 943k | check endpoint | Seen as DeepInfra fp8 on OpenRouter at 0.43 / 0.87, cached 0.004, uptime 100%; direct price not on the pricing page I read; slow model (~42–47 t/s) |
| `zai-org/GLM-5.3-Flash` | 42 | 1M | unknown | yes + structured | 0.15 / 0.50, cached 0.03; FP4; 95.5% tool-task success *(third-party measurement)*; OR promo 0.075 / 0.25 |
| `deepseek-ai/DeepSeek-V4.1-Flash` | 39 | 1M | 131k (OR) | yes + structured | 0.20 / 0.60, cached 0.006; FP8; OR shows 0.14 / 0.42 with a −30% promo |
| `deepseek-ai/DeepSeek-V4-Flash-0731` | 34 | 1M | 384k | yes + structured | 0.06 / 0.18, cached 0.015; FP8; same checkpoint as my rig |
| `zai-org/GLM-5.3` | 45 | 1M | unknown | yes | 0.90 / 4.00 direct (output over my USD 3 cap); OR promo 0.5625 / 2.50 fp4; endpoint accuracy 96 *(third-party measurement)* |
| `deepseek-ai/DeepSeek-V4-Pro-0813` | 36 | 1M | **16k** | yes | 1.30 / 2.60, cached 0.10; FP8; 16k output kills long reasoning |

**Limits and prices.**
- **200 concurrent requests per model** (about 1,200 RPM at 10 s per request); raise via the dashboard. No TPM limit published.
- Through Requesty a DeepInfra `:flex` tier shows V4.1-Flash at USD 0.16 / 0.48 and V4-Flash-0731 at USD 0.072 / 0.144 (13 Oct 2026, before Requesty's 5% markup).

**How to get access.**
1. Sign up at deepinfra.com with email or GitHub. Available in Poland.
2. Add a card or prepay; the free credit is not documented officially.
3. Create an API token in the dashboard and export it as `DEEPINFRA_TOKEN`.

**Agent fit.**
- OpenAI-compatible base URL `https://api.deepinfra.com/v1/openai`; Anthropic-compatible `ANTHROPIC_BASE_URL=https://api.deepinfra.com/anthropic` for Anthropic-SDK harnesses.
- Tools, `tool_choice` and structured outputs on the DeepSeek, GLM, Kimi, MiniMax and Qwen models above (per OpenRouter endpoint metadata); reasoning toggle, prompt cache, streaming.
- **Accuracy is model-dependent, so check per model** *(third-party measurements)*: V4-Pro 97 and GLM-5.3 96 on the AA Endpoint Accuracy Index (faithful); GLM-5.3-Flash 95.5% task success with 4% failures (openbenchmarks, vs Fireworks 99.5%); **GLM-5.2 FP4 only 73** (bad); gpt-oss-120b default 85 vs `-Turbo` 98. Kimi K2-0905 scored 100% schema accuracy on Moonshot's K2VV (Nov 2025).
- **Slow:** AA measured V4-Flash-0731 at 42 t/s and Kimi K2.6 at 22 t/s (slowest tier). Fine for parallel bulk work, painful for a serial agent loop.

**Reliability.**
- Status page: status.deepinfra.com.
- OpenRouter 1-day uptime (13 Oct 2026): most DeepInfra endpoints at 99.4% or better, but Kimi K2.6 91.98% and GLM-5.3-Flash showed 0% at fetch time.

**Limitations.**
- Slowest tier of the cheap hosts; bad for latency-sensitive single-thread agents.
- **FP4 on all GLM models**; GLM-5.2 FP4 lost a quarter of its accuracy, GLM-5.3-Flash FP4 is decent but not best.
- Small max output on V4-Pro (16k) and Kimi K2.6 (16k).
- US only; no EU processing option.

**Where it fits in my stack.**
- **Bulk worker for DeepSeek:** V4-Flash-0731 at USD 0.18 output is the same model as my rig, so I can burst overflow jobs here with identical prompts when my 4 local slots are full.
- V4.1-Flash at USD 0.60 output as the "same family, stronger" sub-agent for non-sensitive tasks.
- Parallel eval runs and batch extraction, where 200 concurrent requests matters more than tokens per second.
- For tool-heavy GLM-5.3-Flash loops I would prefer Fireworks or Parasail (better measured tool accuracy); for one key across hosts, OpenRouter.

**Verify yourself.**

```bash
# public model list with prices and context (no key)
curl -s https://api.deepinfra.com/v1/openai/models
# tool call on V4.1-Flash
curl -s https://api.deepinfra.com/v1/openai/chat/completions -H "Authorization: Bearer $DEEPINFRA_TOKEN" \
  -H 'Content-Type: application/json' -d '{"model":"deepseek-ai/DeepSeek-V4.1-Flash",
  "messages":[{"role":"user","content":"Weather in Krakow?"}],
  "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
```

**Sources:** [DeepInfra pricing](https://deepinfra.com/pricing) · [DeepInfra models API](https://api.deepinfra.com/v1/openai/models) · [DeepInfra rate limits](https://docs.deepinfra.com/account/rate-limits) · [DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy) · [DeepInfra Anthropic integration](https://docs.deepinfra.com/integrations/anthropic) · [OpenRouter endpoints API](https://openrouter.ai/api/v1/models/xiaomi/mimo-v2.6-pro/endpoints) · [AA Endpoint Accuracy Index](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) · [AA GLM-5.2 providers](https://artificialanalysis.ai/models/glm-5-2/providers) · [AA GLM-5.3 providers](https://artificialanalysis.ai/models/glm-5-3/providers) · [AA gpt-oss-120b providers](https://artificialanalysis.ai/models/gpt-oss-120b/providers) · [openbenchmarks same-model accuracy](https://openbenchmarks.com/inference/same-model-different-accuracy) · [K2 Vendor Verifier](https://github.com/MoonshotAI/K2-Vendor-Verifier) · [Requesty models API](https://router.requesty.ai/v1/models) · [AA MiMo-V2.6-Pro](https://artificialanalysis.ai/models/mimo-v2-6-pro)

---

## 3. Fireworks AI

**Type:** pay-as-you-go (USD 1 one-time credit) · **Best models:** GLM 5.3 Flash AA 42, DeepSeek V4.1 Flash AA 39 · **Score: 89** (Q26 C17 L15 A19 R12) · **Data:** trains on prompts: no (nothing kept by default); open-model inference not persistently stored (ZDR by default) *(vendor claim)*, exceptions for the Responses API and batch; "global" routing, US-only processing on `us.api.fireworks.ai` at +50%

> The most accurate cheap host for tool calling I found (99.5% on GLM-5.3-Flash), fast, with huge rate limits and both OpenAI- and Anthropic-compatible endpoints.

**What you get.**
- Pay-as-you-go serverless; about USD 1 free credit on signup *(secondary source)*.
- **GLM 5.3 Flash at USD 0.15 / 0.50 per 1M tokens (input / output), cached 0.03**, with the best measured tool-task success of any host.
- DeepSeek V4.1 Flash at USD 0.30 / 1.20, cached 0.006 (raised on 1 Oct 2026 from 0.22 / 0.66).
- Batch API at 50% of serverless prices.

**Models.** Standard serverless prices, USD per 1M (input / output), Oct 2026.

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| GLM 5.3 Flash | 42 | 1M (native) | unknown | yes | 0.15 / 0.50, cached 0.03; 99.5% tool-task success, best of 10 hosts *(third-party measurement)* |
| DeepSeek V4.1 Flash | 39 | 1M (native) | unknown | not verified | 0.30 / 1.20, cached 0.006; price raised 1 Oct 2026 |
| GLM 5.3 | 45 | 1M (native) | unknown | not verified | 1.40 / 4.40, cached 0.26: output over my USD 3 cap; "Fast" variant 2.10 / 6.60 |
| Kimi K3 | 44 | 1M (native) | unknown | yes | 3 / 15, far over budget; endpoint accuracy 97 *(third-party measurement)* |

**Limits and prices.**
- About **10 RPM until you add a payment method** *(secondary source)*.
- Adaptive TPM by model-size tier since 1 Sep 2026. "Small" tier = models under 600B parameters (GLM 5.3 Flash at 320B and V4.1 Flash at 552B both qualify): **108M prompt TPM, 27M uncached TPM, 1.08M generated TPM** (2 Oct 2026), **doubled on 7 Oct 2026**. That is far beyond what my agents need.
- Price modifiers: "(US)" variants +50%, Priority +25%, Batch −50%.
- **Fire Pass** (flat plan, Kimi K3 Fast via `kimi-fast-latest`, personal/coding-harness use only) is "not currently open to new subscriptions" (docs, Oct 2026).

**How to get access.**
1. Sign up at fireworks.ai. Available in Poland.
2. Use the ~USD 1 credit for a smoke test; add a card to lift the ~10 RPM ceiling.
3. Create an API key in the dashboard and export it as `FIREWORKS_API_KEY`.

**Agent fit.**
- OpenAI-compatible base URL `https://api.fireworks.ai/inference/v1`; Anthropic-compatible `https://api.fireworks.ai/inference` (`ANTHROPIC_BASE_URL`).
- **Best tool-calling fidelity measured** *(third-party measurements)*: openbenchmarks GLM-5.3-Flash 99.5% on 600 structured tool tasks (3 Sep 2026; Nebius 84.8% on the same test); AA Endpoint Accuracy GLM-5.2 100, Kimi K3 97; Moonshot's K2 Vendor Verifier 100% schema accuracy on K2-Thinking and K2-0905. Moonshot names Fireworks as a faithful vendor.
- Responses API defaults to `store=true` (kept 30 days): pass `store=false` if you use it for anything you would not log.

**Reliability.**
- Status page: status.fireworks.ai. OpenRouter 1-day uptime 99.2–100% (13 Oct 2026).
- **Catalog churn is real:** on 26 Sep 2026 Fireworks removed DeepSeek V4 Pro 0813, V4 Flash 0731, Kimi K2.6, K2.7 Code and GLM 5.2 from public serverless; on 27 Aug it deprecated MiniMax M2.7, V4 Pro and K2.6 Turbo. There is no sub-USD-3-output Kimi left here.

**Limitations.**
- Only two models in my budget and above the bar (GLM 5.3 Flash, V4.1 Flash); no MiMo, and V4-Flash-0731 (my rig's model) was removed.
- V4.1 Flash costs twice DeepInfra's output price (1.20 vs 0.60).
- Quantization undisclosed: you trust the measurements, not the spec sheet.
- No EU processing; "global" routing by default.

**Where it fits in my stack.**
- **Primary host for GLM-5.3-Flash tool loops:** sub-agents that call many tools, where a 4% failure rate (DeepInfra, Novita) would cost more in retries than the price difference.
- Coding sub-agent behind an Anthropic-SDK harness, via the Anthropic-compatible endpoint.
- Batch evals and extraction at half price via the Batch API.
- For DeepSeek volume I would use DeepInfra or Parasail instead; for one key with fallbacks, OpenRouter with Fireworks pinned in `provider.order`.

**Verify yourself.**

```bash
# model list (find the exact GLM / DeepSeek IDs)
curl -s https://api.fireworks.ai/inference/v1/models -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  | jq -r '.data[].id' | grep -iE 'glm|deepseek'
export FW_MODEL="<id from the list above>"
# tool call
curl -s https://api.fireworks.ai/inference/v1/chat/completions -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -H 'Content-Type: application/json' -d "{\"model\":\"$FW_MODEL\",
  \"messages\":[{\"role\":\"user\",\"content\":\"Weather in Gdansk?\"}],
  \"tools\":[{\"type\":\"function\",\"function\":{\"name\":\"get_weather\",\"parameters\":{\"type\":\"object\",\"properties\":{\"city\":{\"type\":\"string\"}},\"required\":[\"city\"]}}}]}"
```

**Sources:** [Fireworks pricing](https://fireworks.ai/pricing) · [Fireworks serverless pricing](https://docs.fireworks.ai/serverless/pricing) · [Fireworks changelog](https://docs.fireworks.ai/updates/changelog) · [Fire Pass docs](https://docs.fireworks.ai/firepass) · [Fireworks data residency](https://docs.fireworks.ai/accounts/data-residency) · [Fireworks ZDR write-up](https://abubakarsiddik.site/blog/fireworks-ai-zero-data-retention) · [Fireworks no-card limits](https://yangmao.ai/en/providers/fireworks/no-credit-card/) · [openbenchmarks same-model accuracy](https://openbenchmarks.com/inference/same-model-different-accuracy) · [AA GLM-5.2 providers](https://artificialanalysis.ai/models/glm-5-2/providers) · [AA Kimi K3 providers](https://artificialanalysis.ai/models/kimi-k3/providers) · [K2 Vendor Verifier](https://github.com/MoonshotAI/K2-Vendor-Verifier) · [Kimi Vendor Verifier](https://github.com/MoonshotAI/Kimi-Vendor-Verifier) · [OpenRouter endpoints API](https://openrouter.ai/api/v1/models/z-ai/glm-5.3-flash/endpoints) · [AA GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash)

---

## 4. Z.ai (GLM) API

**Type:** pay-as-you-go (plus a free small-model tier and a flat coding plan) · **Best models:** `glm-5.3-flash` (AA 42), `glm-5.3` (AA 45, over the price band) ·
**Score: 87** (Q26 C18 L12 A18 R13) · **Data:** trains on prompts: no for the API (opt-in only, per the DPA); entity in Singapore, server location not stated

> The first-party API of the GLM models: GLM-5.3-Flash at USD 0.50 output is the best agent model per dollar in this survey, straight from the maker.

**What you get.** A plain pay-as-you-go API with OpenAI-, Responses- and Anthropic-compatible endpoints. The headline is
**GLM-5.3-Flash at USD 0.15 / 0.50 per 1M tokens (input / output), cached input 0.03** (13 Oct 2026). The big GLM-5.3
costs USD 1.40 / 4.40 here, which is over my USD 3 output band. A free tier exists, but only for small models that are
below the bar.

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `glm-5.3-flash` | 42 | 1M | 128K on OpenRouter hosts | yes | 320B / 18B MoE, MIT, vision, released 26 Aug 2026. Vals TB4.0 37.4 vs the bar 18.7 |
| `glm-5.3` | 45 (max) · 34 (low) | 1M | 128K | yes | 753B / 40B, released 18 Aug 2026. USD 4.40 output here: use third-party hosts |

**Limits and prices.**
- PAYG (Z.ai pricing page, no page date, read 13 Oct 2026), USD per 1M input / cached / output:
  - `glm-5.3-flash` 0.15 / 0.03 / 0.50 · `glm-5.3-flashx` 0.37 / 0.075 / 1.25.
  - `glm-5.3` 1.40 / 0.26 / 4.40 (also GLM-5.2 and 5.1). Cached-input storage is "limited-time free".
- **GLM-5.3 at a sane price lives elsewhere** (OpenRouter, 13 Oct 2026): Baidu fp8 USD 0.599 / 1.883, SiliconFlow and
  Novita fp8 0.70 / 2.20, DeepInfra fp4 0.5625 / 2.50 *(promo)*. Z.ai itself lists 1.40 / 4.40 there too.
- Free GLM-4.7-Flash: **1 concurrent request, about 1 RPS, about 1,000 RPD**, no card *(third-party measurement)*.
- I found no published RPM/TPM numbers for the paid API (13 Oct 2026).

**How to get access.**
1. Create an account on z.ai (entity: JINGSHENG HENGXING TECHNOLOGY PTE. LTD., Singapore); signup works from Poland.
2. Add a balance in the console (payment method details were not in the pages I read).
3. Create an API key and export it as `ZAI_API_KEY`.
4. Use the PAYG base URL, **not** the coding-plan URL: a call on the wrong endpoint fails with error 1113 "Insufficient balance".

**Agent fit.**
- Base URLs: OpenAI-compatible `https://api.z.ai/api/paas/v4`, Responses API `https://api.z.ai/api/v1`,
  Anthropic-compatible `https://api.z.ai/api/anthropic`.
- Streaming, function calling, context caching and JSON structured output are supported.
- **Reasoning is always on** for GLM-5.3 (`thinking.type` accepts only `enabled`), and the Z.ai listing treats Flash
  the same way; tbench.ai did run Flash at effort "none", so test it. `reasoning_effort` is low / high / max with
  **max as the default**, so output bills balloon unless you set `"reasoning_effort":"low"` in tool loops.
- Tool accuracy: on 600 structured tool tasks Z.ai's GLM-5.3-Flash endpoint hit **97.5 %**, against 99.5 % for
  Fireworks and 84.8 % for Nebius *(third-party measurement, 3 Sep 2026)*. On the AA Endpoint Accuracy Index Z.ai's
  GLM-5.3 scores 98 % of the reference *(third-party measurement, 26 Sep 2026)*.

**Reliability.**
- OpenRouter shows the Z.ai GLM-5.3-Flash endpoint at 100 % 1-day uptime (13 Oct 2026). No status-page history was in my sources.
- Fast release cadence: GLM-5.1, 5.2 and 5.3 all shipped in 2026, 5.3 and 5.3-Flash eight days apart in August.

**Limitations.**
- **GLM-5.3 is over the band here** (USD 4.40 output). Z.ai is a Flash route; buy GLM-5.3 from a third-party host.
- The free GLM-4.7-Flash is 30B-A3B class, below my local DeepSeek-V4-Flash-0731 (AA 34). It is not a real free tier.
- **GLM Coding Plan is not usable from my own agent.** It costs from USD 18 / 80 / 168 a month (Lite / Pro / Max; one
  tracker lists 18 / 72 / 160), but the policy says it *"may only be used within officially supported tools and products"*
  (Claude Code, OpenCode, Codex and others), with bans after 3 violations and no refunds. Users also report heavy
  throttling since the 14 Aug 2026 credit change.

**Where it fits in my stack.**
- **Default cheap sub-agent and bulk worker** on GLM-5.3-Flash at low effort: it beats my local model on hard terminal
  tasks (Vals TB4.0 37.4 vs 18.7) at USD 0.50 output.
- Client or professional data stays on the local rig; for GLM-5.3 itself I would use a third-party host, not Z.ai.

**Verify yourself.**
```bash
curl https://api.z.ai/api/paas/v4/chat/completions -H "Authorization: Bearer $ZAI_API_KEY" -H "Content-Type: application/json" \
 -d '{"model":"glm-5.3-flash","reasoning_effort":"low","messages":[{"role":"user","content":"hi"}],
      "tools":[{"type":"function","function":{"name":"ping","parameters":{"type":"object","properties":{}}}}]}'
```

**Sources:** [Z.ai pricing](https://docs.z.ai/guides/overview/pricing) · [Z.ai GLM-5.3 guide](https://docs.z.ai/guides/llm/glm-5.3.md) · [Z.ai release notes](https://docs.z.ai/release-notes/new-released.md) · [GLM Coding Plan overview](https://docs.z.ai/devpack/overview.md) · [GLM Coding Plan usage policy](https://docs.z.ai/devpack/usage-policy) · [GLM Coding Plan FAQ](https://docs.z.ai/devpack/faq.md) · [codingplan.org GLM prices](https://codingplan.org/en/plans/glm) · [usagepricing price change](https://usagepricing.com/blueprint/activity/zhipu-ai-2026-07-22-price-change) · [zentor.ai plan limits](https://zentor.ai/blog/glm-coding-plan-rate-limits) · [Standard Compute on Z.ai data](https://standardcompute.com/providers/z-ai) · [toolnavs on free GLM-4.7-Flash](https://toolnavs.com/en/article/1100-zai-released-glm-47-flash-weights-and-api-free-tier-1-concurrency-and-launched-f) · [AA GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash) · [AA GLM-5.3](https://artificialanalysis.ai/models/glm-5-3) · [AA GLM-5.3 providers](https://artificialanalysis.ai/models/glm-5-3/providers) · [openbenchmarks same-model accuracy](https://openbenchmarks.com/inference/same-model-different-accuracy) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [OpenRouter models API](https://openrouter.ai/api/v1/models)

---

## 5. Parasail

**Type:** pay-as-you-go · **Best models:** GLM-5.3-Flash AA 42, DeepSeek-V4.1-Flash AA 39, DeepSeek-V4-Flash-0731 AA 34 · **Score: 87** (Q26 C18 L14 A17 R12) · **Data:** trains on prompts: unknown (not covered in my sources); US-hosted

> A small US serverless broker that is one of the most consistently faithful cheap hosts in every accuracy test, with quantization disclosed and no published rate limits.

**What you get.**
- Pay-as-you-go serverless with "no minimums or rate limits" *(vendor claim)*.
- **V4-Flash-0731 at USD 0.14 / 0.28 per 1M tokens (input / output), cached 0.05**, FP8: my local model at a faithful host.
- GLM-5.3-Flash at USD 0.15 / 0.50 and V4.1-Flash at USD 0.30 / 1.20 (13 Oct 2026).
- Free credits: unknown (not on the pricing page).

**Models.** Direct prices, USD per 1M (input / output), 13 Oct 2026; quantization as disclosed on OpenRouter.

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| GLM-5.3-Flash | 42 | 1M (native) | unknown | yes | 0.15 / 0.50; FP4; 98.3% tool-task success *(third-party measurement)* |
| DeepSeek-V4.1-Flash | 39 | 1M (native) | unknown | not verified | 0.30 / 1.20 (reference price, same as Together/Fireworks) |
| DeepSeek-V4-Flash-0731 | 34 | 1M (native) | unknown | not verified | 0.14 / 0.28, cached 0.05; FP8; OR 1-day uptime 100% |
| GLM-5.3 | 45 | 1M (native) | unknown | not verified | 1.40 / 4.40, cached 0.26: output over my USD 3 cap; FP8; endpoint accuracy 99 *(third-party measurement)* |
| DeepSeek-V4-Pro-0813 | 36 | 1M (native) | unknown | not verified | 1.32 / 3.96: over cap |

**Limits and prices.**
- No rate limits published ("no minimums or rate limits" *(vendor claim)*); in practice expect host capacity to be the limit.
- Prices match the US "reference" price list (V4.1-Flash 0.30 / 1.20, GLM-5.3-Flash 0.15 / 0.50); for 0731 Parasail ties Together at 0.14 / 0.28, DeepInfra is cheaper at 0.06 / 0.18.

**How to get access.**
1. Sign up at parasail.io. No region restriction for Poland is documented in my sources.
2. Add billing; free credit is not advertised.
3. Create an API key and export it as `PARASAIL_API_KEY`.
4. Or skip the account: Parasail is a provider on OpenRouter, pinnable with `provider.only: ["Parasail"]`.

**Agent fit.**
- OpenAI-compatible base URL `https://api.parasail.io/v1`. No Anthropic-compatible endpoint is mentioned in my sources; use it from OpenAI-SDK harnesses or via OpenRouter.
- **Accuracy is consistently near reference** *(third-party measurements)*: AA Endpoint Accuracy Index GLM-5.3 99, GLM-5.2 98, gpt-oss-120b 97, Kimi K3 102 (26 Sep 2026); openbenchmarks GLM-5.3-Flash 98.3% on 600 structured tool tasks (Fireworks 99.5%, Nebius 84.8%).
- Tool calling on GLM-5.3-Flash is proven by the tool-task test; for the DeepSeek models check `supported_parameters` on the OpenRouter endpoint before relying on `tools` or `response_format`.

**Reliability.**
- Status page: status.parasail.io. OpenRouter 1-day uptime 97.4–100% across its endpoints (13 Oct 2026).
- No catalog churn or deprecation events recorded in my sources (unlike Fireworks or Together).

**Limitations.**
- **Data terms unknown**: I found nothing on retention or training; fine for non-sensitive work only, which is my rule for this leg anyway.
- V4.1-Flash at 1.20 output is twice DeepInfra's direct price.
- No MiMo-V2.6-Pro; the only above-bar models within budget are GLM-5.3-Flash and V4.1-Flash.
- **Near-equivalent alternative: [Together AI](#9-together-ai).** Same reference prices (0731 0.14 / 0.28, GLM-5.3-Flash 0.15 / 0.50 FP8, V4.1-Flash 0.30 / 1.20 FP8), quantization disclosed, GLM-5.3-Flash 98.5% tool-task success, but a USD 5 minimum top-up, prompts stored by default (ZDR toggle), silent redirects on deprecated IDs and gpt-oss-120b accuracy of only 81.

**Where it fits in my stack.**
- **Fallback host for GLM-5.3-Flash tool loops**, second in `provider.order` after Fireworks on OpenRouter.
- Overflow for V4-Flash-0731 when I want a faithful host with published quantization rather than the cheapest one.
- For the lowest DeepSeek price use DeepInfra; for sensitive data, the rig.

**Verify yourself.**

```bash
# Parasail endpoints on OpenRouter: price, quantization, uptime
curl -s https://openrouter.ai/api/v1/models/z-ai/glm-5.3-flash/endpoints \
  | jq '.data.endpoints[]|select(.provider_name|test("Parasail"))|{provider_name,quantization,pricing,uptime_last_1d}'
# direct: list models and pick an ID
curl -s https://api.parasail.io/v1/models -H "Authorization: Bearer $PARASAIL_API_KEY" | jq -r '.data[].id'
export PS_MODEL="<GLM-5.3-Flash id from the list>"
curl -s https://api.parasail.io/v1/chat/completions -H "Authorization: Bearer $PARASAIL_API_KEY" \
  -H 'Content-Type: application/json' -d "{\"model\":\"$PS_MODEL\",
  \"messages\":[{\"role\":\"user\",\"content\":\"Weather in Poznan?\"}],
  \"tools\":[{\"type\":\"function\",\"function\":{\"name\":\"get_weather\",\"parameters\":{\"type\":\"object\",\"properties\":{\"city\":{\"type\":\"string\"}},\"required\":[\"city\"]}}}]}"
```

**Sources:** [Parasail pricing](https://www.parasail.io/pricing) · [OpenRouter endpoints API](https://openrouter.ai/api/v1/models/z-ai/glm-5.3-flash/endpoints) · [AA Endpoint Accuracy Index](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) · [AA GLM-5.3 providers](https://artificialanalysis.ai/models/glm-5-3/providers) · [AA GLM-5.2 providers](https://artificialanalysis.ai/models/glm-5-2/providers) · [AA gpt-oss-120b providers](https://artificialanalysis.ai/models/gpt-oss-120b/providers) · [AA Kimi K3 providers](https://artificialanalysis.ai/models/kimi-k3/providers) · [openbenchmarks same-model accuracy](https://openbenchmarks.com/inference/same-model-different-accuracy) · [Together pricing](https://www.together.ai/pricing) · [Together serverless models](https://docs.together.ai/docs/serverless-models) · [Together ZDR](https://docs.together.ai/docs/zero-data-retention) · [Together changelog](https://docs.together.ai/docs/changelog)

---

## 6. DeepSeek API

**Type:** pay-as-you-go · **Best models:** `deepseek-flash` = DeepSeek-V4.1-Flash (AA 39) ·
**Score: 85** (Q23 C16 L15 A18 R13) · **Data:** trains on prompts: opt-out (on by default); stored in the PRC

> The maker of my local model: the same family one step up (V4.1-Flash), very cheap off-peak and with practically no rate limits.

**What you get.** Pay-as-you-go only, no free tier. **`deepseek-flash` costs USD 0.15 / 0.60 per 1M tokens (input /
output) off-peak and USD 0.30 / 1.20 at peak**; a cache hit is USD 0.003 off-peak (13 Oct 2026). The account gets 2,500
concurrent requests on Flash and no RPM or TPM caps. The catch is the data terms, not the price.

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `deepseek-flash` (V4.1-Flash) | 39 (max) · 25 (non-reasoning) | 1M | 384K | yes | 552B / 16B MoE, MIT, released 10 Sep 2026. Text + image in. Vals TB2.1 74.5 vs 0731's 67.0 |
| `deepseek-v4-pro` (0813) | 36 | 1M | 384K | yes | 1.6T / 49B. Below Flash on AA and on Vals TB4.0 (14.1). Not worth it |

**My local model is not on this API.** The legacy IDs `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` were
retired on 10 Sep 2026 and now route to V4.1-Flash. **The 0731 weights are served only by third-party hosts**
(OpenRouter, 13 Oct 2026): DeepInfra fp8 USD 0.06 / 0.18, Parasail fp8 and Together 0.14 / 0.28, Alibaba 0.176 / 0.528.

**Limits and prices.**

| Model | Cache hit (off-peak / peak) | Cache miss (off-peak / peak) | Output (off-peak / peak) |
|---|---|---|---|
| `deepseek-flash` | 0.003 / 0.006 | 0.15 / 0.30 | 0.60 / 1.20 |

- **Peak = 01:00–04:00 and 06:00–10:00 UTC, Monday to Friday** (Chinese holidays excluded), introduced 16 Aug 2026.
- **In Polish time: 03:00–06:00 and 08:00–12:00 CEST on weekdays; from 25 Oct 2026 02:00–05:00 and 07:00–11:00 CET** (my calculation).
- Concurrency: **2,500 on Flash, 500 on Pro** per account; more is free on request. Over the limit you get HTTP 429.
- No RPM/TPM limits; under load requests are held open (keep-alive) and closed if inference has not started within 10 minutes.

**How to get access.**
1. Sign up for the DeepSeek Open Platform with email or phone. Poland and the EU are served.
2. Top up with a card or PayPal (PayPal not verified).
3. Create a key and export it as `DEEPSEEK_API_KEY`. Use the policy's training opt-out if you want training off.

**Agent fit.**
- OpenAI-compatible `https://api.deepseek.com`, Anthropic-compatible `https://api.deepseek.com/anthropic`, plus the
  Responses API. JSON output, tool calls and chat-prefix completion; FIM and vision only on Flash.
  vision only on Flash.
- Thinking is **on by default** (low / high / max). V4.1-Flash is **the most verbose model AA measured** (250M output
  tokens), so use low or high effort for routine steps. 190 tok/s, TTFT 0.96 s *(third-party measurement)*.
- Accuracy: no Jinja chat template, so hosts write their own tool parsing; on the AA Endpoint Accuracy Index (V4-Pro,
  Aug 2026) DeepSeek scored 107 % and every host 97–107 % *(third-party measurement)*. Keep prompt prefixes stable for cache hits.

**Reliability.**
- status.deepseek.com 90-day uptime (Jul–Oct 2026): **V4.1-Flash API 99.69 %**, V4-Pro API 99.92 %, no open incidents.
- **Heavy churn behind one ID:** 0731 (31 Jul), V4-Pro update (13 Aug), V4.1-Flash (10 Sep, new ID). Pin `deepseek-flash` and expect silent upgrades.

**Limitations.**
- **Trains on prompts by default (opt-out), PRC storage, no DPA or SCCs**; Italy's Garante blocked DeepSeek *(third-party reports)*.
- No free tier, and peak hours double the price during the Polish working morning.
- V4.1-Flash is not my local 0731, so results from the API do not prove what the rig will do.

**Where it fits in my stack.**
- **Burst capacity for the same family:** overflow non-sensitive jobs here when the 4 local slots are full.
- **Off-peak batch worker:** schedule bulk jobs for afternoons, evenings and weekends in Polish time.
- For an exact 0731 match (evals against the rig) use a third-party host, not this API.

**Verify yourself.**
```bash
curl https://api.deepseek.com/models -H "Authorization: Bearer $DEEPSEEK_API_KEY"
curl https://api.deepseek.com/chat/completions -H "Authorization: Bearer $DEEPSEEK_API_KEY" -H "Content-Type: application/json" \
 -d '{"model":"deepseek-flash","messages":[{"role":"user","content":"weather in Warsaw?"}],
      "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
```

**Sources:** [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) · [DeepSeek rate limit](https://api-docs.deepseek.com/quick_start/rate_limit) · [DeepSeek changelog](https://api-docs.deepseek.com/updates) · [DeepSeek status](https://status.deepseek.com/) · [AA V4.1-Flash](https://artificialanalysis.ai/models/deepseek-v4-1-flash) · [AA V4-Pro](https://artificialanalysis.ai/models/deepseek-v4-pro) · [AA V4-Pro providers](https://artificialanalysis.ai/models/deepseek-v4-pro/providers) · [AA Endpoint Accuracy Index](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) · [DeepSeek-V4.1-Flash paper](https://arxiv.org/pdf/2609.19969) · [HF V4-Flash-0731 card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) · [Vals TB2.1](https://www.vals.ai/benchmarks/terminal-bench-2-1) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [OpenRouter models API](https://openrouter.ai/api/v1/models) · [Meetily on DeepSeek data](https://meetily.ai/llm-privacy/deepseek) · [ComplianceHub on the Garante block](https://www.compliancehub.wiki/italys-privacy-watchdog-blocks-deepseek-ai-a-gdpr-battle-begins)

---

## 7. Alibaba Cloud Model Studio (international)

**Type:** one-time credits (1M free tokens per model) then pay-as-you-go · **Best models:** trial: `qwen3.8-max` (AA 45), `glm-5.3` (AA 45), `kimi-k3` (AA 44); PAYG in band: `qwen3.8-flash` (AA 40), `deepseek-v4.1-flash` (AA 39) ·
**Score: 85** (Q29 C17 L11 A17 R11) · **Data:** trains on prompts: no ("will never use your data for model training"); hosted in Singapore

> One account gives a free 90-day taste of nearly every strong model (Qwen3.8-Max, GLM-5.3, Kimi K3, DeepSeek V4.1), then cheap Qwen and DeepSeek on pay-as-you-go.

**What you get.** New users get **1M free tokens per model, valid 90 days from activating Model Studio**, one time,
for every Singapore-region model with "International" deployment scope (doc updated 11 Oct 2026). After that it is
plain pay-as-you-go: the in-band picks are **`qwen3.8-flash` at USD 0.15 / 0.47 per 1M tokens (input / output)** and
`deepseek-v4.1-flash` at USD 0.15 / 0.60 in idle hours (13 Oct 2026).

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `qwen3.8-flash` | 40 (as Qwen3.8-Flash-Next) | 1M on OpenRouter · 262K native for Flash-Next | not stated | not stated | Only host is Alibaba. Check which model the ID really is (see Limitations) |
| `deepseek-v4.1-flash` | 39 | 1M | not stated | yes | Idle USD 0.15 / 0.60, busy 0.30 / 1.20 |
| `qwen3.8-max` | 45 | not stated | not stated | not stated | USD 2 / 6: trial only for me |
| `ZHIPU/GLM-5.3` | 45 | 1M | not stated | yes | USD 1.40 / 4.40: trial only |
| `kimi-k3` | 44 | 1M | not stated | yes | USD 3 / 15: trial only |

**Limits and prices.**
- PAYG, Singapore, USD per 1M input / output (page updated 13 Oct 2026):
  - `qwen3.8-flash` 0.15 / 0.47 (cache 0.016 on OpenRouter) · `qwen3.7-plus` 0.40 / 1.60 up to 256K (AA 25, below the bar).
  - `deepseek-v4.1-flash` idle 0.15 / 0.60, busy 0.30 / 1.20 · `deepseek-v4-pro-0813` idle 0.66 / 1.98, busy 1.32 / 3.96.
- **Batch is −50 %**; context caching is discounted. The idle/busy hours for DeepSeek were not published in my sources.
- OpenRouter also lists Alibaba as a host of my local **DeepSeek-V4-Flash-0731 at USD 0.176 / 0.528** (13 Oct 2026).
- The free quota is small for agents: **1M tokens is a few dozen long agent tasks per model**. The "Free Quota Only"
  switch stops service at zero (error `AllocationQuota.FreeTierOnly`), so there is no surprise bill.

**How to get access.**
1. Create an Alibaba Cloud **international** account (open to EU users; a card is typically required, not re-checked).
2. Activate Model Studio in the **Singapore** region: the 90-day clock starts here, so activate when you are ready to test.
3. Create an API key and export it as `DASHSCOPE_API_KEY`.

**Agent fit.**
- OpenAI-compatible `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`.
- **Anthropic-compatible** `https://dashscope-intl.aliyuncs.com/apps/anthropic`, usable from Claude Code via `ANTHROPIC_BASE_URL`.
- Model IDs are case-sensitive and mixed-style (`ZHIPU/GLM-5.3` next to `kimi-k3`): copy them from `/models`.
- Qwen3.8-Flash-Next: TB2.1 86.1, DeepSWE 58.7, SWE-Pro 62.5 *(vendor claim)*; no independent agent scores yet.

**Reliability.**
- Terms move: the **Qwen Code free OAuth tier was shut down on 15 Apr 2026** (1,000 RPD, then 100, then zero), and the
  Coding Plan Lite closed to new buyers on 20 Mar 2026 and to renewals on 13 Apr 2026.
- No uptime or status data for Model Studio in my sources.

**Limitations.**
- The free tokens are **one-time**, not a recurring free tier.
- **`qwen3.8-flash` may not be the model AA scores 40**: a third-party report says Qwen Cloud "Qwen3.8-Flash" is not
  the same ID as Qwen3.8-Flash-Next. Verify via `/models` and your own eval.
- **Coding Plan** (Pro USD 50 a month only; 6,000 requests per 5 hours, 45,000 a week, 90,000 a month) has an old model
  list (no Qwen3.8, no GLM-5.3) and says *"Do not use the plan's API key for automated scripts, application backends,
  or other non-interactive scenarios"*; third parties report ban risk.
- **Token Plan** (Lite USD 6 for 11.5k credits up to Pro USD 68 for 180k) is sold for listed tools (Claude Code,
  Cursor, Qwen Code, Codex and others), and the credit-to-token conversion is not published. I would not run my own agent on it.

**Where it fits in my stack.**
- **Free eval runner for 90 days:** one key to run my evals against Qwen3.8-Max, GLM-5.3, Kimi K3 and V4.1-Flash.
- **Cheap PAYG worker** on `qwen3.8-flash` once I have confirmed which model it is, with batch at −50 % for offline jobs.
- A second source for DeepSeek V4.1-Flash, and possibly for exact 0731 comparisons against the rig.

**Verify yourself.**
```bash
curl -s https://dashscope-intl.aliyuncs.com/compatible-mode/v1/models -H "Authorization: Bearer $DASHSCOPE_API_KEY"
curl -s https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" -d '{"model":"qwen3.8-flash","messages":[{"role":"user","content":"hi"}]}'
```

**Sources:** [Model Studio free quota](https://www.alibabacloud.com/help/en/model-studio/new-free-quota) · [Model Studio pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing) · [Model Studio models](https://www.alibabacloud.com/help/en/model-studio/models) · [Model Studio privacy notice](https://www.alibabacloud.com/help/en/model-studio/privacy-notice) · [Coding Plan](https://www.alibabacloud.com/help/en/model-studio/coding-plan) · [Token Plan](https://www.alibabacloud.com/help/en/model-studio/token-plan-overview) · [Token Plan landing page](https://www.alibabacloud.com/en/campaign/ai-landing-page-token) · [Kong DashScope Anthropic URL](https://developer.konghq.com/ai-gateway/use-claude-code-with-ai-gateway-dashscope/) · [vibecoding.app plan review](https://vibecoding.app/blog/alibaba-coding-plan-review) · [Qwen Code issue 1742](https://github.com/QwenLM/qwen-code/issues/1742) · [inventivehq on Qwen Code shutdown](https://inventivehq.com/blog/qwen-code-still-free-2026-shutdown) · [AA Qwen3.8-Flash-Next](https://artificialanalysis.ai/models/qwen3-8-flash-next) · [llm-stats Qwen3.8-Flash-Next](https://llm-stats.com/blog/research/qwen3.8-flash-next-launch) · [OpenRouter models API](https://openrouter.ai/api/v1/models)

---

## 8. Xiaomi MiMo API

**Type:** pay-as-you-go (a flat Token Plan exists, but not for own agents) · **Best models:** `mimo-v2.6-pro` (AA 46), `mimo-v2.6-flash` (AA 38) ·
**Score: 83** (Q30 C16 L11 A15 R11) · **Data:** trains on prompts: no by default *(third-party summary)*; contracting entities in the Netherlands and Singapore, server location not stated

> The highest-scoring open model in this survey (MiMo-V2.6-Pro, AA 46) for under USD 1 output, sold directly by its maker.

**What you get.** A pay-as-you-go, OpenAI-compatible API. **MiMo-V2.6-Pro costs USD 0.435 / 0.87 per 1M tokens
(input / output), cache read USD 0.0036**, with cache writes free for a limited time (13 Oct 2026). Xiaomi cut prices
permanently by up to 99 % on 27 May 2026. There is no free tier; a payment method is required before the key works.

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `mimo-v2.6-pro` | 46 (#1 open weights) | 1M | 128K | yes | 1.02T / 42B MoE, MIT, released 21 Sep 2026. Vals TB4.0 31.3, TB2.1 67.8 |
| `mimo-v2.6-flash` | 38 | 1M | not stated | yes | 309B / 15B MoE, MIT. Vals TB2.1 76.4 (beats V4.1-Flash), TB4.0 24.2 |

Both take text, image, audio and video input. Reasoning is on by default.

**Limits and prices.**
- PAYG, USD per 1M input / cache read / output (13 Oct 2026):
  - `mimo-v2.6-pro` 0.435 / 0.0036 / 0.87.
  - `mimo-v2.6-flash` 0.14 / 0.003 (OpenRouter) / 0.28.
- No PAYG RPM/TPM numbers in the pages I read (13 Oct 2026).
- **Token Plan:** Lite USD 6, Standard 16, Pro 50, Max 100 a month for 4.1B / 11B / 38B / 82B credits (annual −12 %).
  Pro costs 300 / 2.5 / 600 credits per token (input miss / cache hit / output); off-peak 0.8× from 16:00–24:00 UTC
  (18:00–02:00 CEST). By my calculation Lite is worth about USD 5.9 of PAYG for USD 6, so the plan saves only
  **0–20 %** (more off-peak).

**How to get access.**
1. Create a Xiaomi account and open the MiMo developer platform. The entities are Xiaomi Technology Netherlands B.V.
   and Xiaomi Singapore, so signup from Poland works.
2. Add a payment method: the key does not work until one is on file.
3. Create a PAYG key and export it as `MIMO_API_KEY`. Do not use a Token Plan key for your own agent.

**Agent fit.**
- PAYG base URL: `https://api.xiaomimimo.com/v1` (OpenAI-compatible). The Token Plan endpoints
  (`token-plan-{cn,sgp,ams}.xiaomimimo.com/v1`, ams = Amsterdam) also have an `/anthropic` variant.
- Tool calling, reasoning and multimodal input are supported; JSON output is **"soft"** (no strict schema mode in my
  sources), so validate and retry.
- **Gotcha:** Xiaomi warns that the Anthropic-compatible endpoint returns **HTTP 400 in multi-turn tool calls if the
  reasoning content is not passed back**. Echo `reasoning_content` in the history.
- **Slow:** 46.8 tok/s, TTFT 4.0 s *(third-party measurement)*. Fine for a planner or reviewer, painful for tight loops.
- Independent agent scores are split: Vals TB2.1 67.8 is about my local model's 67.0, but **TB4.0 31.3 is well above
  the bar of 18.7**. Vendor TB2.1 89.9 *(vendor claim)* is far above the independent number.

**Reliability.**
- OpenRouter shows the Xiaomi Pro endpoint at **95.9 % 1-day uptime** vs 100 % for DeepInfra at the same price (13 Oct 2026).
- Few hosts serve Pro (4 on OpenRouter, some with degraded status), so the first-party API is the main route.

**Limitations.**
- **The Token Plan is not for own agents:** *"only available for use in programming tools… prohibited… automated
  scripts and custom application backends"*. Use PAYG; the plan only saves 0–20 % anyway.
- Data terms rest on third-party summaries (no training by default, ZDR for Enterprise); I did not read the full
  privacy policy.
- Card required: no way to test without paying.

**Where it fits in my stack.**
- **Cheap planner or reviewer** for non-sensitive tasks: AA 46 at USD 0.87 output is the best quality per dollar I found.
- **MiMo-V2.6-Flash as a bulk worker** at USD 0.28 output where TB2.1-style terminal work matters.
- For a second route to the same weights at the same price with better uptime, DeepInfra serves Pro at USD 0.43 / 0.87.

**Verify yourself.**
```bash
curl https://api.xiaomimimo.com/v1/chat/completions -H "Authorization: Bearer $MIMO_API_KEY" -H "Content-Type: application/json" \
 -d '{"model":"mimo-v2.6-pro","messages":[{"role":"user","content":"hi"}],"tools":[{"type":"function","function":{"name":"ping","parameters":{"type":"object","properties":{}}}}]}'
```

**Sources:** [MiMo Token Plan](https://mimo.mi.com/docs/en-US/tokenplan/Token%20Plan/subscription) · [eesel MiMo pricing](https://www.eesel.ai/blog/xiaomi-mimo-v2-6-pricing) · [TypingMind MiMo guide](https://www.typingmind.com/guide/xiaomi/mimo-v2.6-pro) · [kingy.ai MiMo setup](https://kingy.ai/blog/mimo-v2-6-pro-free-access-pricing-setup/) · [36kr price cut](https://eu.36kr.com/en/p/3826964226691972) · [AA MiMo-V2.6-Pro](https://artificialanalysis.ai/models/mimo-v2-6-pro) · [AA MiMo-V2.6-Flash](https://artificialanalysis.ai/models/mimo-v2-6-flash) · [Vals TB2.1](https://www.vals.ai/benchmarks/terminal-bench-2-1) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [computingforgeeks MiMo test](https://computingforgeeks.com/xiaomi-mimo-v2-6-pro-flash/) · [OpenRouter models API](https://openrouter.ai/api/v1/models)

---

## 9. Together AI

**Type:** pay-as-you-go · **Best models:** GLM-5.3 (AA 45), GLM-5.3-Flash (AA 42), DeepSeek-V4.1-Flash (AA 39) ·
**Score: 82** (Q26 C17 L13 A15 R11) · **Data:** trains on prompts: no (opt-in, off by default); prompts and responses
stored by default, ZDR toggle available; hosted in the US

> A US serverless host with list-price access to every strong open-weight family and the best quantization disclosure
> in the group, which is why it ranks high despite having no free tier.

**What you get.** Prepaid credits, **minimum USD 5 top-up, no free trial since July 2025**. OpenAI-compatible API,
1M context on the DeepSeek V4 and GLM-5.x models, a Batch API (discount rate not on the page). AA = Artificial Analysis
Intelligence Index v4.3.2 as of 13 Oct 2026; my local DeepSeek-V4-Flash-0731 scores AA 34.

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `zai-org/GLM-5.3` | 45 | 1M | not captured | yes | FP4 · AA endpoint accuracy 97 |
| `zai-org/GLM-5.3-Flash` | 42 | 1M | not captured | yes | FP8 · 98.5% tool-task success |
| `deepseek-ai/DeepSeek-V4.1-Flash` | 39 | 1M | not captured | yes | FP8 · added 11 Sep 2026 |
| `deepseek-ai/DeepSeek-V4-Pro-0813` | 36 | 1M | not captured | yes | NVFP4 · output over USD 3 |
| `deepseek-ai/DeepSeek-V4-Flash-0731` | 34 | 1M | not captured | yes | same model as my local rig |

**Limits and prices.** USD per 1M tokens (input / cached / output), 13 Oct 2026:
- GLM-5.3-Flash 0.15 / 0.03 / 0.50 · V4-Flash-0731 0.14 / 0.03 / 0.28 · V4.1-Flash 0.30 / 0.006 / 1.20.
- GLM-5.3 and GLM-5.2 1.40 / 0.26 / 4.40 · V4-Pro-0813 1.32 / 0.13 / 3.96 · MiniMax-M3 0.30 / 0.06 / 1.20 (524k).
- gpt-oss-120b 0.15 / 0.60 (MXFP4, 131k) · Kimi-K3 3 / 0.30 / 15.
- **"Dynamic rate limits for serverless retired" on 2 Oct 2026**; no fixed RPM/TPM is published.
- Balance may go negative up to USD -100 on tiers 1–4.

**How to get access.**
1. Sign up at together.ai (available in Poland).
2. Buy at least USD 5 of credits with a card.
3. Org Settings → Privacy → set "Store prompts and model responses" to **No** before sending anything.
4. Create the API key in the dashboard and export it as `TOGETHER_API_KEY`.

**Agent fit.** OpenAI-compatible base URL `https://api.together.xyz/v1`; no Anthropic endpoint in the research. Provider
accuracy is good on the models that matter *(third-party measurement)*: AA Endpoint Accuracy Index GLM-5.2 97, GLM-5.3
97, Kimi K3 100; openbenchmarks GLM-5.3-Flash 98.5% on 600 tool tasks (3 Sep 2026); KVV Kimi K3 within noise of
Moonshot. **Exception: gpt-oss-120b scores only 81** on the AA endpoint index, so do not use it here.

**Reliability.** Status at status.together.ai. OpenRouter 1-day uptime 94–100% (gpt-oss 94.4%, GLM-5.3 97.0%,
V4-Flash-0731 99.8%) on 13 Oct 2026. Frequent serverless deprecations (gpt-oss-20b on 14 Sep 2026) and **silent
redirects** of deprecated IDs (GLM-4.6 → GLM-4.7, DeepSeek-V3-0324 → V3.1).

**Limitations.**
- No free allowance at all; USD 5 to start.
- Prompts are stored by default until you flip the ZDR switch.
- Old model IDs may be silently redirected to a newer model, which breaks eval reproducibility.
- gpt-oss-120b endpoint is degraded (AA 81).
- US-only processing.

**Where it fits in my stack.**
- **Bulk worker on GLM-5.3-Flash** (AA 42 at USD 0.50 output): smarter than my local model, cheap enough for batch.
- Cloud overflow for my local V4-Flash-0731 at USD 0.28 output, same weights, so prompts transfer unchanged.
- GLM-5.3 as a mid-tier planner when Opus is overkill; keep client data local as always.

**Verify yourself.**
```bash
curl -s https://api.together.xyz/v1/models -H "Authorization: Bearer $TOGETHER_API_KEY" | jq '.[].id' | head
```

**Sources:** [Together pricing](https://www.together.ai/pricing) · [Serverless models](https://docs.together.ai/docs/serverless-models) · [Changelog](https://docs.together.ai/docs/changelog) · [Zero data retention](https://docs.together.ai/docs/zero-data-retention) · [Free tier change Jul 2025](https://support.together.ai/articles/1862638756-changes-to-free-tier-and-billing-july-2025) · [AA DeepSeek V4 Flash](https://artificialanalysis.ai/models/deepseek-v4-flash)

---

## 10. NVIDIA build.nvidia.com (NIM trial API)

**Type:** free tier (developer trial, prototyping only) · **Best models:** `z-ai/glm-5.3` (AA 45), `moonshotai/kimi-k3` (AA 44), `z-ai/glm-5.3-flash` (AA 42), `deepseek-ai/deepseek-v4.1-flash` (AA 39) ·
**Score: 79** (Q29 C20 L10 A14 R6) · **Data:** trains on prompts: unknown, NVIDIA "may use" content to improve its products and models; hosted in the US (assumed, not stated)

> NVIDIA's free hosted NIM endpoints are the only place on 13 Oct 2026 where I get GLM-5.3 and Kimi K3 for USD 0 with an
> OpenAI-compatible API, which is why it ranks high on quality and cost even though the terms say "prototyping only".

**What you get.** A free API key for NVIDIA Developer Program members, no card. The live `/v1/models` list had **80 model
ids on 13 Oct 2026**. There is **no published token or daily cap**: the only consistent number is **about 40 requests per
minute per account** *(third-party measurement, community and forum consensus)*. Kimi K3 is the headline: it costs
USD 9.50 to 15 per 1M output tokens everywhere else, here it is free.

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `z-ai/glm-5.3` | 45 | 1M | not stated | yes | ~40B active, reasoning; best independent agent scores of the cheap open models (Vals TB4.0 38.9) |
| `moonshotai/kimi-k3` | 44 | 1,048,576 | not stated | yes | thinking always on; echo `reasoning_content` and `tool_calls` back every turn |
| `z-ai/glm-5.3-flash` | 42 | 1M | not stated | not stated | 18B active, multimodal, structured output |
| `deepseek-ai/deepseek-v4.1-flash` | 39 | 1,048,576 | not stated | yes | on build since 18 Sep 2026; reasoning effort 1 to 100; FP4 KV cache |

**Limits and prices.** As of 13 Oct 2026:
- **~40 RPM per account, shared across all models** *(third-party measurement)*; a moderator (Jul 2026) said it "depends
  on the model, use case and overall traffic" and cannot be raised officially.
- Daily cap: **unknown**; sources say "unlimited but RPM" (May 2026), "1,000 credits" (2 Oct 2026) or "10,000 RPD per model".

**How to get access.**
1. Create an NVIDIA account and join the NVIDIA Developer Program. No card.
2. Pass **SMS phone verification**; the key is not activated before that (reported 1 Oct 2026).
4. Generate the API key on build.nvidia.com and export it as `NVIDIA_API_KEY`.

**Agent fit.**
- **OpenAI-compatible** base URL `https://integrate.api.nvidia.com/v1` (`/chat/completions`, streaming, tools).
  **No Anthropic-compatible endpoint**, so a Claude-style harness needs a translating proxy.
- Kimi K3 needs `reasoning_content` and `tool_calls` echoed back every turn; V4.1-Flash exposes effort 1 to 100.
- **Concurrency is the real limit**: the 40 RPM is account-wide, so four parallel sub-agents share it.
- Long reasoning turns plus queueing cause client timeouts. Set long timeouts and retry 429 and 504 with backoff.

**Reliability.**
- **No SLA and no public status page** for the trial API.
- Forum, May 2026: new models "are always time out"; the web UI shows "hundreds of requests in queue" at peaks.
- The NVIDIA-hosted `nemotron-3-ultra:free` endpoint on OpenRouter showed **77.4 % one-day uptime, degraded**, on
  13 Oct 2026 *(third-party measurement)*.
- **Catalog churn**: docs list `deepseek-v4-pro`, `deepseek-v4-flash(-0731)`, `glm-5.1`/`5.2` and others that were not live on 13 Oct 2026.

**Limitations.**
- No published limits, and models disappear without notice; quantization is not disclosed.
- **Terms say prototyping, research, development and testing only.** Not a production backend.
- Data: content is used to provide the service and not stored after the session by default, **but** NVIDIA may monitor,
  scan and use it to improve products and AI models (third-party summaries of the trial ToS). Non-sensitive data only.

**Where it fits in my stack.**
- **Free evaluation of GLM-5.3 and Kimi K3** before I pay for them elsewhere: run my eval set
  ([../course_agentic_apps/14-EVALUATION.md](../course_agentic_apps/14-EVALUATION.md)) here at ~40 RPM.
- A free "smarter than local" sub-agent for prototypes: GLM-5.3 (AA 45) as reviewer or second planner next to my local
  V4-Flash-0731 (AA 34).
- **Not for anything that must finish on time**: for bulk or scheduled jobs my 4 local slots are more predictable, and
  for production I would pay a host with an SLA.

**Verify yourself.**
```bash
curl -s https://integrate.api.nvidia.com/v1/models | jq -r '.data[].id'   # no key needed
curl -s https://integrate.api.nvidia.com/v1/chat/completions -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" -d '{"model":"deepseek-ai/deepseek-v4.1-flash","messages":[{"role":"user","content":"Weather in Warsaw?"}],
  "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}],"max_tokens":1024}'
```

**Sources:** [NVIDIA live model list](https://integrate.api.nvidia.com/v1/models) · [build.nvidia.com DeepSeek V4.1-Flash](https://build.nvidia.com/deepseek-ai/deepseek-v4.1-flash) · [NIM product docs](https://docs.api.nvidia.com/nim/docs/product) · [NIM LLM API reference](https://docs.api.nvidia.com/nim/reference/llm-apis) · [dev.to test of the NVIDIA free claim](https://dev.to/klukyanov/kimi-k3-deepseek-and-glm-free-from-nvidia-i-tested-the-claim-and-here-is-the-catch-2m9b) · [klymentiev.com credits post](https://klymentiev.com/blog/nvidia-nim-free-credits) · [NVIDIA forum: is NIM free](https://forums.developer.nvidia.com/t/is-nim-free/369368) · [NVIDIA forum: new models time out](https://forums.developer.nvidia.com/t/all-new-model-are-timeout/368931) · [Standard Compute NVIDIA ToS summary](https://standardcompute.com/providers/nvidia) · [OpenRouter endpoints API](https://openrouter.ai/api/v1/models) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4)

---

## 11. Vercel AI Gateway

**Type:** free tier (USD 5 credit every 30 days) and pay-as-you-go · **Best models:** `zai/glm-5.3-flash` (AA 42) on the free credit; paid `xiaomi/mimo-v2.6-pro` (AA 46), `deepseek/deepseek-v4.1-flash` (AA 39) ·
**Score: 77** (Q26 C18 L7 A17 R9) · **Data:** trains on prompts: unknown per provider, Vercel assumes training unless it has an agreement; per-model `no_training` flag in the catalog; regions per model (DeepSeek `us`, Gemini `eu`/`us`)

> Vercel's router passes provider list prices through with no markup and gives every team USD 5 a month, which on
> GLM-5.3-Flash is about 10M output tokens: a small but recurring free pool with both OpenAI and Anthropic APIs.

**What you get.** One key for 463 models (live catalog, 13 Oct 2026). The free tier gives **USD 5 credit every 30 days per
Vercel team**, counted from the first request, usable only on a "free-tier-eligible" subset with lower, unpublished
per-model rate limits. **Buying any credits moves you to the paid tier and the monthly free credit stops for good.** Paid
tier: no markup, no platform fee on tokens, no gateway rate limits.

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `zai/glm-5.3-flash` | 42 | 1M | 131k | yes (model) | free-tier eligible; USD 0.15 / 0.50, cached 0.03 |
| `alibaba/qwen3.8-flash-next` | 40 | 262k (native) | not stated | not stated | free-tier eligible; may not be the same model as `alibaba/qwen3.8-flash` (USD 0.15 / 0.47) |
| `xiaomi/mimo-v2.6-pro` | 46 | 1M (native) | not stated | not stated | paid only; USD 0.435 / 0.87 |
| `deepseek/deepseek-v4.1-flash` | 39 | 1M (native) | **32,768** | yes (model) | paid only; USD 0.30 / 1.20; output capped far below the model's 384k |
| `deepseek/deepseek-v4-flash-0731` | 34 | 1M (native) | not stated | yes (model) | paid only; USD 0.076 / 0.153, cached 0.014; my local model, hosted |

**Limits and prices.** As of 13 Oct 2026:
- Free: **USD 5 per 30 days**. On GLM-5.3-Flash that is **about 10M output tokens** (my arithmetic, ignoring input).
- Free-tier rate limits are **deliberately unpublished**: "Limits can change, so this page describes behavior rather than
  fixed numbers" (docs, 8 Sep 2026).
- Zero-priced routes that do not use the USD 5: `poolside/laguna-s-2.1-free` (256k context, 32k output,
  **deprecated on 31 Oct 2026**), `stealth/glyph-cluster` (Pro/Enterprise plus purchased credits), and
  `inclusionai/ling-3.1-flash-free` (AA 41, listed by a third party on 13 Oct 2026 but absent from the public catalog,
  which shows only the paid `inclusionai/ling-3.1-flash` at USD 0.30 / 0.90).
- Paid list prices: `mimo-v2.6-flash` (AA 38) 0.14 / 0.28, `zai/glm-5.3` (AA 45) 1.40 / 4.40 (out of band).

**How to get access.**
1. Create a Vercel account and a team; the free credit belongs to the team.
2. **Expect to need a card on file.** A community thread (9 Jul 2026) shows `403 customer_verification_required`
   ("AI Gateway requires a valid credit card on file"); some directories (Aug to Sep 2026) say no card. The sources conflict.
3. Create an AI Gateway API key and export it as `AI_GATEWAY_API_KEY`.
4. **Do not buy credits on this team** if you want to keep the monthly USD 5.

**Agent fit.**
- **OpenAI-compatible**: `https://ai-gateway.vercel.sh/v1/chat/completions`. Also OpenResponses.
- **Anthropic Messages**: set `ANTHROPIC_BASE_URL=https://ai-gateway.vercel.sh` and `ANTHROPIC_AUTH_TOKEN`, so a
  Claude-style harness can run GLM-5.3-Flash without a proxy.
- 429 body `{"error":{"message":"Rate limit exceeded","type":"rate_limit_exceeded"}}`; honour `retry-after`. Budget
  exhaustion returns **402** `quota_for_entity_exceeded`.
- BYOK has no fee but is paid-tier only, and **a failed BYOK call falls back to Vercel credentials and is billed**.

**Reliability.**
- No uptime or status numbers in my sources for the gateway itself.

**Limitations.**
- Free-tier rate limits are unpublished; most other free-eligible models are below my bar (MiniMax-M3 AA 29).
- **USD 5 a month is small**: one busy day of a parallel agent loop can burn it.
- **First purchase ends the free tier permanently**; card-on-file is likely required anyway.

**Where it fits in my stack.**
- A **monthly free pool for GLM-5.3-Flash sub-agents** (tool-heavy workers, extraction) when the local slots are busy.
- **Anthropic-compatible test bed**: point a Claude-oriented harness ([../agent-harnesses/README.md](../agent-harnesses/README.md))
  at cheap models without writing a proxy.

**Verify yourself.**
```bash
curl -s https://ai-gateway.vercel.sh/v1/models | jq -r '.data[]|select(.pricing.output=="0")|.id'
curl -s https://ai-gateway.vercel.sh/v1/chat/completions -H "Authorization: Bearer $AI_GATEWAY_API_KEY" -H 'Content-Type: application/json' \
 -d '{"model":"zai/glm-5.3-flash","messages":[{"role":"user","content":"hi"}]}'
```

**Sources:** [Vercel AI Gateway pricing](https://vercel.com/docs/ai-gateway/pricing) · [Vercel AI Gateway rate limits](https://vercel.com/docs/ai-gateway/rate-limits) · [Vercel live model catalog](https://ai-gateway.vercel.sh/v1/models) · [Vercel Anthropic Messages API](https://vercel.com/docs/ai-gateway/sdks-and-apis/anthropic-messages-api) · [Vercel community: card verification](https://community.vercel.com/t/ai-gateway-stuck-on-customer-verification-required-despite-valid-card-on-file/45438) · [itsfree.ai: Vercel AI Gateway](https://itsfree.ai/provider/vercel-ai-gateway/) · [awesome-free-ai-coding: Vercel](https://mvalentsev.github.io/awesome-free-ai-coding/providers/vercel-ai-gateway/) · [agentjournal.dev: Vercel free credits](https://agentjournal.dev/blog/vercel-ai-gateway-free/) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models)

---

## 12. Kilo Gateway

**Type:** free promo (no account needed) and pay-as-you-go · **Best models:** `stepfun/step-5-preview-free` (AA 44), `inclusionai/ling-3.1-flash` (AA 41) ·
**Score: 75** (Q28 C18 L9 A15 R5) · **Data:** trains on prompts: **yes** (Kilo flags every free model `mayTrainOnYourPrompts: true`); hosting location not stated

> The gateway behind Kilo Code serves Step 5 Preview (AA 44, USD 2.70 output elsewhere) for free, with tools and 1M
> context, and answers without a key or account: the fastest way on 13 Oct 2026 to try a model ten points above my bar.

**What you get.** An OpenAI-compatible gateway with an OpenRouter-style catalog of **393 models** (live, 13 Oct 2026) plus
Kilo-only free promos. **Free models answer without a key or account**, limited to **200 requests per hour per IP**
(Kilo docs). Paid models need an account and credits; BYOK is supported. Per the Kilo docs, Kilo was acquired by Anaconda.

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `stepfun/step-5-preview-free` | 44 | 1M | 64k | yes | reasoning low / medium / high; Kilo-exclusive free, OpenRouter charges USD 1.00 / 2.70 |
| `inclusionai/ling-3.1-flash` | 41 | not stated (262k on other routers) | not stated (32k elsewhere) | not stated | free here; released 1 to 2 Oct 2026; no independent agent benchmarks yet |

Step 5 Preview: 600B total / 27B active, image input, served by a single host (StepFun, FP8). Vals Terminal-Bench 4.0
**31.8** *(third-party measurement)* against my bar of 18.7; vendor Terminal-Bench 2.1 85.0 *(vendor claim)*. Open
weights were promised for 15 Oct 2026.

The rest of the free list is below my bar or unscored (Nemotron 3 Ultra AA 23, Inkling Small AA 26, Glyph Cluster, Laguna S 2.1).

**Limits and prices.** As of 13 Oct 2026:
- Free models: USD 0. Anonymous traffic: **200 requests per hour per IP**. No published per-account free limit.
- Paid models: account plus credits; the catalog mirrors OpenRouter's. For Step 5 Preview after the promo, the reference
  price is USD 1.00 / 2.70 per 1M tokens (input / output), cached 0.05, on OpenRouter.
- The Step 5 free route is a **time-limited promo** with no published end date.

**How to get access.**
1. For free models: nothing. Send requests to the gateway without a key.
2. For paid models or BYOK: create a Kilo account, add credits, and use the key from the account.

**Agent fit.**
- **OpenAI-compatible** base URL `https://api.kilo.ai/api/gateway` (chat at `/chat/completions`). No Anthropic-compatible
  endpoint in my sources.
- Step 5 Preview free has **tools, 1M context, 64k output and an effort knob**: it is a real agent model, not a toy.
- **Do not use `kilo-auto/free`** (256k context, 32k output) in agent loops: it rotates among dots-3-note, ling-3.1-flash,
  nemotron-3-ultra, laguna-s-2.1 and glyph-cluster, so tool-call behaviour changes from request to request.
- Many `:free` ids are **proxied OpenRouter free endpoints**, so they inherit OpenRouter's churn and upstream 429s.

**Reliability.**
- Promo churn: free models on OpenRouter, which Kilo proxies, live a **median of about 75 days** *(third-party measurement,
  TrueFoundry, Oct 2026)*; the OpenRouter free list shrank from 24 to 16 models between 21 Sep and 13 Oct 2026.

**Limitations.**
- **Everything free may be used for training**: "Auto Free may route your requests to providers that log prompts and outputs
  and use them to improve their services." NVIDIA endpoints add "Do not submit personal or confidential data".
- The best route is a promo; it can end any week.
- 200 requests per hour per IP is the whole budget, shared by every process behind that IP.
- Ling 3.1 Flash is unproven: one host, no independent agent benchmarks, weights not released.

**Where it fits in my stack.**
- **Zero-friction trials**: point a harness at Step 5 Preview free to see whether an AA 44 model beats my local
  V4-Flash-0731 (AA 34) on my own agent tasks before I pay for it.
- A free **planner or reviewer sub-agent** for open-source or demo work where training on prompts does not matter.
- Not for production or scheduled jobs: when the promo ends, switch to paid Step 5 (USD 2.70 output) or to GLM-5.3-Flash
  (AA 42, USD 0.50 output) on a paid host, and keep the local rig for anything with client data.
- Wire it as a first hop with a paid fallback, as in [../course_agentic_apps/17-HYBRID-AND-ROUTER.md](../course_agentic_apps/17-HYBRID-AND-ROUTER.md).

**Verify yourself.**
```bash
curl -s https://api.kilo.ai/api/gateway/models | jq -r '.data[]|select(.isFree==true)|"\(.id) train=\(.mayTrainOnYourPrompts)"'
curl -s https://api.kilo.ai/api/gateway/chat/completions -H 'Content-Type: application/json' \
 -d '{"model":"stepfun/step-5-preview-free","messages":[{"role":"user","content":"hi"}]}'
```

**Sources:** [Kilo live model catalog](https://api.kilo.ai/api/gateway/models) · [Kilo Gateway docs](https://kilo.ai/docs/gateway) · [Kilo models and providers](https://kilo.ai/docs/gateway/models-and-providers) · [OpenRouter live catalog](https://openrouter.ai/api/v1/models) · [TrueFoundry: OpenRouter free models](https://www.truefoundry.com/blog/openrouter-free-models-whats-actually-free-and-what-it-costs-you) · [openrouter-free-models tracker](https://github.com/cyclez2000/openrouter-free-models/issues/82) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [OrcaRouter: Step 5 open weights](https://www.orcarouter.ai/blog/step-5-preview-open-weights)

---

## 13. Ollama Cloud

**Type:** flat plan (Pro USD 20 a month includes USD 60 of credits) · **Best models:** `glm-5.3` (AA 45), `kimi-k3` (AA 44), `glm-5.3-flash` (AA 42), `deepseek-v4.1-flash` (AA 39) ·
**Score: 74** (Q29 C15 L8 A13 R9) · **Data:** trains on prompts: **no** *(vendor claim: "never logged or trained on")*; hosted mainly in the US on NVIDIA cloud providers under zero data retention, EU routing possible

> Ollama's cloud plan gives three dollars of model credit for every dollar of subscription, which pulls GLM-5.3 (AA 45)
> and Kimi K3 (AA 44) into my price band, with no restriction to coding tools.

**What you get.** A subscription that converts into usage credits billed at per-token rates mirroring first-party list
prices. Pricing changed from usage limits to credits between about 27 Aug and 1 Sep 2026. **Pro: USD 20 a month (or 200 a
year) buys USD 60 of credits a month.** Unlike the GLM Coding Plan or Kimi Code, **API use is not restricted to coding
tools**, so I can call it from my own agents.

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `glm-5.3` | 45 | 1M (native) | not stated | yes (model) | list USD 1.40 / 4.40; effective on Pro about 0.47 / 1.47 |
| `kimi-k3` | 44 | 1M (native) | not stated | yes (model) | list USD 3 / 15; effective on Pro about 1 / 5; strongest open tool-use model |
| `glm-5.3-flash` | 42 | 1M (native) | not stated | yes (model) | list USD 0.15 / 0.50 |
| `deepseek-v4.1-flash` | 39 | 1M (native) | not stated | yes (model) | list USD 0.30 / 1.20, off-peak 0.15 / 0.60 |
| `mistral-large-4` | 38 | 1M vendor, 524k measured | not stated | not stated | list USD 0.68 / 2.09 |

Ollama's context/output limits and **quantization are not disclosed**. Below my bar: `minimax-m3` (AA 29), `kimi-k2.6` (27).

**Limits and prices.** As of 13 Oct 2026:

| Plan | Price | Included credits | Concurrency |
|---|---|---|---|
| Free | USD 0 | starter credits, starter models only, reset monthly, no rollover | 1 (queued, then rejected) |
| Pro | USD 20 a month or 200 a year | USD 60 a month | 3 |
| Max | USD 100 a month | USD 300 a month | 10 |
| Team | USD 500 a month | USD 1,000 shared | 10 |

- **Off-peak** is outside 12:00 to 18:00 UTC on weekdays, plus all weekend; off-peak is cheaper, for DeepSeek half price.
  In Poland that peak window is 14:00 to 20:00 in summer time and 13:00 to 19:00 in winter time.
- Pro's USD 60 buys **about 13.6M GLM-5.3 output tokens** or about 4M Kimi K3 (my arithmetic, output only).

**How to get access.**
1. Create an account on ollama.com.
2. Subscribe to Pro (or Max) for the credits; the free plan only covers starter models.
3. Create an API key in the ollama.com account and export it as `OLLAMA_API_KEY` (see docs.ollama.com/cloud).

**Agent fit.**
- Native API at `https://ollama.com/api`; `curl https://ollama.com/api/tags` lists the cloud models.
- OpenAI and Anthropic clients are supported **as a subset** (docs); `https://ollama.com/v1` is **assumed, not verified**.
- **Concurrency 3 on Pro is the binding limit**: fewer parallel workers than my 4 local slots. Max raises it to 10.

**Reliability.**
- **Terms moved recently** (credits since late Aug 2026); no uptime or status data in my sources.

**Limitations.**
- **You pay USD 20 up front**: it is cheap only if I actually burn most of the USD 60 every month.
- Concurrency 3 on Pro limits fan-out agents.
- The `/v1` path is unverified, and quantization and context limits are undisclosed.

**Where it fits in my stack.**
- **A cheap GLM-5.3 planner or reviewer** (AA 45 at about USD 1.47 effective output) between my local V4-Flash-0731
  (AA 34) and Claude Opus for planning.
- **Kimi K3 for tool-heavy sub-agents** where its tool-use strength matters, at about USD 5 effective output instead of 15.

**Verify yourself.**
```bash
curl -s https://ollama.com/api/tags | jq -r '.models[].name'
# chat call on the native API; check the exact model tag in /api/tags and the auth header in docs.ollama.com/cloud
curl -s https://ollama.com/api/chat -H "Authorization: Bearer $OLLAMA_API_KEY" -H 'Content-Type: application/json' \
 -d '{"model":"glm-5.3","messages":[{"role":"user","content":"hi"}],"stream":false}'
```

**Sources:** [Ollama pricing](https://ollama.com/pricing) · [Ollama Cloud docs](https://docs.ollama.com/cloud) · [agentdeals.dev: Ollama Cloud](https://agentdeals.dev/vendor/ollama-cloud) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · [AA Kimi K3](https://artificialanalysis.ai/models/kimi-k3) · [Kimi K3 model card](https://huggingface.co/moonshotai/Kimi-K3) · [Mistral Large 4 specs](https://capitalandcompute.net/md/mistral-large-4-pricing-benchmarks.md)

---

## 14. Requesty

**Type:** free tier + pay-as-you-go · **Best models:** `novita/ling-3.1-flash` (AA 41, free); paid GLM-5.3-Flash (AA 42), DeepSeek V4.1 Flash (AA 39), MiMo-V2.6-Pro (AA 46) · **Score: 72** (Q25 C18 L6 A15 R8) · **Data:** Trains on prompts: no for the free Ling 3.1 Flash (Requesty metadata: no retention, no training, upstream Novita, geo global); yes for the free NVIDIA-trial models; router has an EU region (Frankfurt) on every plan

> A UK router with a real no-card free tier, an EU endpoint on the free plan, and the only free Ling 3.1 Flash route that is flagged no-training, which puts an above-bar model behind an EU URL for zero cost.

**What you get.** As of 13 Oct 2026: the Free plan is "the full platform, on free models", **200 requests/day, no credit card**. Pay-as-you-go adds every model (784 routes) at a **5% markup** on managed usage, plus BYOK. The router itself runs in Frankfurt if you use the EU base URL, even on Free.

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `novita/ling-3.1-flash` (free) | 41 | 262k | 32k | yes, plus reasoning | no JSON-schema flag; single upstream (Novita) |
| GLM-5.3-Flash (zai / deepinfra / novita / fireworks / runware) | 42 | 1M native | not captured | per upstream | USD 0.15 / 0.50 |
| `melious/glm-5.3-flash` (EU geolocation) | 42 | 1M native | not captured | per upstream | USD 0.12 / 0.46 |
| `deepinfra/deepseek-v4.1-flash` | 39 | 1M native | not captured | per upstream | USD 0.20 / 0.60, cached 0.006; `:flex` 0.16 / 0.48 |
| `melious/deepseek-v4-flash-0731` (EU geolocation) | 34 | 1M native | not captured | per upstream | USD 0.12 / 0.29; same model as my rig |
| MiMo-V2.6-Pro | 46 | 1M native | not captured | per upstream | USD 0.43–0.435 / 0.87 |

"1M native" is the model's own window; I did not capture Requesty's per-route context for paid models. Ling 3.1 Flash has a 1M window on AA but only 262k / 32k on this route.

**Limits and prices.** All as of 13 Oct 2026 (Requesty pricing page and live catalog):
- Free: 200 requests/day, **shared across all free models**; RPM not published; no card.
- PAYG: list price + 5%. Examples before markup: DeepSeek V4.1 Flash USD 0.20 / 0.60 (DeepInfra), 0.15 / 0.60 (Runware), 0.30 / 1.20 (DeepSeek); V4 Flash 0731 USD 0.076 / 0.153 (Runware), 0.072 / 0.144 (DeepInfra `:flex`).
- Other EU-geolocated routes: `lyceum/deepseek-v4-flash-0731` USD 0.25 / 0.30, `scaleway/deepseek-v4-flash-0731` 0.46 / 0.93 (256k ctx), `sference/glm-5.3-flash` 0.20 / 0.60, `melious/deepseek-v4.1-flash` 0.23 / 1.14.
- Other free models are below the bar: Nemotron 3 Ultra (AA 23; NVIDIA trial terms, 30-day retention, trains), Gemma 4 31B (AA 15; 8k output here), Poolside Laguna (32k ctx and no tools on Requesty).

**How to get access.**
1. Sign up at requesty.ai; no card is needed for the Free plan.
2. Create an API key in the dashboard and export it as `REQUESTY_API_KEY`.
3. From Poland, use the EU base URL `https://router.eu.requesty.ai/v1`; no region block applies.
4. Add credit only when you want paid models; the 5% markup applies to managed usage, not to BYOK keys.

**Agent fit.** OpenAI-compatible at `https://router.requesty.ai/v1` (EU: `https://router.eu.requesty.ai/v1`) and Anthropic-compatible at `https://router.requesty.ai/anthropic/v1/messages`. A bare model name gets managed failover; `provider/model` pins a host; `policy/<name>` applies a routing policy. Ling 3.1 Flash free does tool calls and reasoning, but has **no JSON-schema flag and a 32k output cap**, so I would use plain JSON prompts with a validator and keep outputs short. Ling has no independent agentic benchmark yet, it is very verbose (220M tokens on the AA run), and it is served by one upstream. I found no published 429 shape or concurrency limit.

**Reliability.** No public uptime numbers, and the catalog has no health fields: unknown. The free list "changes as providers add and remove them". Ling 3.1 Flash churn is visible elsewhere: OpenRouter listed it at zero price on 3 Oct 2026, made it paid (USD 0.075 / 0.225), and its free variant was gone by 13 Oct 2026 *(third-party measurement)*.

**Limitations.**
- 200 requests/day for everything free: one long agent run can use half of it.
- The EU URL makes the *router* EU; Ling's upstream is Novita with geo "global", so inference is not EU-resident.
- 32k max output and no JSON-schema support on the free Ling route.
- Ling 3.1 Flash is unproven: released 1–2 Oct 2026, weights not out, no Vals or tbench numbers.
- No uptime data, no published RPM.

**Where it fits in my stack.**
- Free EU-endpoint sub-agent for short classify / extract / summarise calls on non-sensitive data, up to ~200 a day.
- A second-opinion model in evals (see `../course_agentic_apps/14-EVALUATION.md`): Ling 41 vs my local 34.
- PAYG as an EU-routed gateway with failover to GLM-5.3-Flash or V4 Flash 0731 at Melious / Lyceum prices.
- For volume I stay local (4 slots, no daily cap); for heavy paid loops OpenRouter or DeepInfra are simpler.

**Verify yourself.**
```bash
curl -s https://router.requesty.ai/v1/models | jq -r '.data[]|select(.input_price==0 and .output_price==0)|.id'
curl -s https://router.eu.requesty.ai/v1/chat/completions -H "Authorization: Bearer $REQUESTY_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"novita/ling-3.1-flash","messages":[{"role":"user","content":"hi"}],
       "tools":[{"type":"function","function":{"name":"f","parameters":{"type":"object","properties":{}}}}]}'
```

**Sources:** [Requesty pricing](https://www.requesty.ai/pricing) · [Requesty free models](https://www.requesty.ai/models/free) · [Requesty models API](https://router.requesty.ai/v1/models) · [Requesty quickstart](https://docs.requesty.ai/quickstart) · [AA Ling 3.1 Flash](https://artificialanalysis.ai/models/ling-3-1-flash) · [OpenRouter models API](https://openrouter.ai/api/v1/models) · [OpenRouter free-model tracker](https://github.com/cyclez2000/openrouter-free-models/issues)

---

## 15. Scaleway Generative APIs (EU)

**Type:** pay-as-you-go (plus 1M free tokens, one-time) · **Best models:** `deepseek-v4.1-flash` (AA 39), `deepseek-v4-flash-0731` (AA 34) · **Score: 72** (Q23 C12 L11 A14 R12) · **Data:** Trains on prompts: no (no data retention claimed, *vendor claim*); hosted in Paris (fr-par), EU

> A French cloud's serverless OpenAI-compatible API: the most established EU-resident route to an above-bar model, with disclosed quantization and a status page, at a clear price premium over US hosts.

**What you get.** As of 13 Oct 2026: the first **1M tokens are free** (plus 60 minutes of audio), one-time. After that it is pay-as-you-go in EUR. The base tier needs a valid payment method; an "Enhanced" tier after ID verification raises the limits. Everything runs in Paris.

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `deepseek-v4.1-flash` | 39 | not captured | not captured | not captured | EUR 0.60 / 1.80, cached 0.12 |
| `deepseek-v4-flash-0731` | 34 | 256k | 32k | not captured | reasoning none to max; listed in docs, price not captured |
| `glm-5.3` | 45 | not captured | not captured | not captured | EUR 1.80 / 5.50: above the 3 USD cap |

**Limits and prices.** Pricing page, Oct 2026 (EUR per 1M tokens, input / output): `deepseek-v4.1-flash` 0.60 / 1.80 (cached 0.12); `glm-5.3` 1.80 / 5.50; `qwen3.5-397b-a17b` 0.60 / 3.60; `mistral-medium-3.5-128b` 1.50 / 7.50; `mistral-small-3.2-24b` 0.15 / 0.35. Batch is 50% off. RPM and TPM are not published; they are shown only in the console under "Organization quotas". For scale: DeepSeek's own API sells the same V4.1 Flash at USD 0.15 / 0.60 off-peak, so the EU residency costs about 3x on output. Context is **capped below native** (256k against a 1M window).

**How to get access.**
1. Create a Scaleway account and add a payment method: the base tier requires one.
2. Optionally pass ID verification for the Enhanced tier and higher quotas.
3. Create an API secret key in the console and export it as `SCW_SECRET_KEY`; no region issue from Poland (fr-par).

**Agent fit.** OpenAI-compatible at `https://api.scaleway.ai/v1` (also `/{project_id}/v1`). Quantization is disclosed per model in the docs (fp8 / fp4 / bf16). The 256k context cap and 32k output on V4 Flash 0731 matter for long agent loops: plan for compaction. The weak spot is **endpoint accuracy**: AA measured Scaleway's GLM-5.2 at **75%** of the reference, with the damage concentrated in BFCL tool calling, while its gpt-oss-120b (FP4, 128k / 32k, AA 12) scored 98% *(third-party measurement, AA Endpoint Accuracy Index, 26 Sep 2026)*. There is no measurement for its DeepSeek endpoints, so run a tool-calling smoke test first. I found no Anthropic-compatible endpoint in my sources.

**Reliability.** Status at status.scaleway.com. Catalog moves: `devstral-2-123b` was deprecated on 1 Jul 2026, and the GitHub model docs lag the pricing page (docs still list GLM-5.2 at 256k / 16k output while pricing shows GLM-5.3).

**Other EU routes compared.** As of 13 Oct 2026:

| Route | Best in-band model (AA) | Price per 1M (input / output) | Notes |
|---|---|---|---|
| Scaleway | V4.1 Flash (39) | EUR 0.60 / 1.80 | Paris; no retention claimed; quant disclosed |
| Lyceum | GLM-5.3-Flash (42) | USD 0.20 / 0.50 | Berlin company, eu-north1 / Paris; zero-retention mode claimed; no accuracy data |
| Mistral EU endpoint | GLM-5.3 (45) | USD 1.54 / 4.84 | `api.eu.mistral.ai` at +10% on 1.40 / 4.40; NVFP4; training off for paid API, ZDR on request |
| Mistral | Mistral Large 4 preview (38) | USD 0.68 / 2.09 promo | about two weeks from 6 Oct 2026, then 1.36 / 4.18; measured ctx 524k vs 1M claimed |
| OVHcloud | Qwen3.8-27B (34 at xhigh) | EUR 0.40 / 2.70 | Gravelines; data not stored; gpt-oss-120b EUR 0.08 / 0.40; no DeepSeek or GLM |
| Requesty EU routes | GLM-5.3-Flash (42) | USD 0.12 / 0.46 + 5% | Melious; also `melious/deepseek-v4-flash-0731` 0.12 / 0.29, `lyceum/` 0.25 / 0.30 |

Mistral's catch is legal, not technical: **since 5 Aug 2026 (7 Aug in the EU) the API is for business customers only**; individuals may not use it for personal projects. The Free plan's credit has been unstated since 7 Oct 2026, and the Free plan may train on inputs unless you opt out. An older third-party summary still describes a free tier of 1B tokens/month per model; the newer sources contradict it. OVHcloud also allows 2 RPM per IP per model without a key and 400 RPM per project per model with one.

**Limitations.**
- About 3x the price of US hosts for the same DeepSeek model; GLM-5.3 is over the cap here.
- Context capped at 256k (32k output on V4 Flash 0731); measured tool-call loss on GLM-5.2 (75%), nothing on DeepSeek.
- Quotas visible only in the console; the free 1M tokens are a sampler, not a tier.

**Where it fits in my stack.**
- The EU-resident paid route when a task must not leave the EU but is not sensitive enough to stay on the rig.
- A failover for my local V4 Flash 0731 (same model, 256k cap) when the rig is busy or down.
- For price and quality in the EU I would try Lyceum GLM-5.3-Flash first and keep Scaleway as the established fallback.
- Truly sensitive client data still stays local (see `../course_agentic_apps/16-SECURITY-OWASP-ASI.md`).

**Verify yourself.**
```bash
curl -s https://api.scaleway.ai/v1/models -H "Authorization: Bearer $SCW_SECRET_KEY" | jq -r '.data[].id'
curl -s https://api.scaleway.ai/v1/chat/completions -H "Authorization: Bearer $SCW_SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"deepseek-v4.1-flash","messages":[{"role":"user","content":"Weather in Warsaw?"}],
       "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
curl -s https://oai.endpoints.kepler.ai.cloud.ovh.net/v1/models | jq -r '.data[].id'
```

**Sources:** [Scaleway pricing](https://www.scaleway.com/en/pricing/model-as-a-service/) · [Scaleway supported models](https://raw.githubusercontent.com/scaleway/docs-content/main/pages/generative-apis/reference-content/supported-models.mdx) · [Scaleway rate limits](https://raw.githubusercontent.com/scaleway/docs-content/main/pages/generative-apis/reference-content/rate-limits.mdx) · [Scaleway signup](https://www.scaleway.com/en/generative-apis-signup/) · [AA GLM-5.2 providers](https://artificialanalysis.ai/models/glm-5-2/providers) · [AA gpt-oss-120b providers](https://artificialanalysis.ai/models/gpt-oss-120b/providers) · [Lyceum roster](https://lyceum.technology/magazine/eu-hosted-llm-api-lyceum-model-roster-prices/) · [Mistral GLM-5.3](https://docs.mistral.ai/models/zai-glm-5-3) · [Mistral regional endpoints](https://www.digitalapplied.com/blog/mistral-hosts-rival-open-models-regional-endpoints-2026) · [Mistral changelog](https://docs.mistral.ai/resources/changelogs) · [agentdeals Mistral](https://agentdeals.dev/mistral-api-pricing-2026) · [Mistral Large 4 specs](https://capitalandcompute.net/md/mistral-large-4-pricing-benchmarks.md) · [OVHcloud catalog](https://www.ovhcloud.com/en/public-cloud/ai-endpoints/catalog/) · [OVHcloud capabilities](https://docs.ovhcloud.com/en/guides/public-cloud/ai-machine-learning/ai-endpoints-capabilities) · [Requesty models API](https://router.requesty.ai/v1/models) · [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing)

---

## 16. StepFun API and Step Plan

**Type:** pay-as-you-go + flat plan · **Best models:** `step-5-preview` (AA 44, leaderboard) · **Score: 71** (Q28 C11 L12 A13 R7) · **Data:** Trains on prompts: unknown on the first-party API; hosting region not documented

> The first-party home of Step 5 Preview, one of the strongest models under the 3 USD output cap, sold per token or as a cheap monthly plan that claims to work with your own stack.

**What you get.** As of 13 Oct 2026: international pay-as-you-go on platform.stepfun.ai, with rate tiers that grow with your total top-up, and the **Step Plan**, a flat monthly subscription paid in credits. Step 5 Preview was released on 20 Sep 2026 as an API-only model; **open weights are scheduled for 15 Oct 2026** *(vendor claim)*.

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `step-5-preview` (StepFun direct) | 44 | 1M | 64k | not captured | 600B / 27B MoE; `reasoning_effort` low / medium / high; image and video in |
| `stepfun/step-5-preview` (OpenRouter) | 44 | 1M | 64k | not captured | single host (StepFun, FP8); USD 1.00 / 2.70, cached 0.05 |
| `stepfun/step-5-preview-free` (Kilo Gateway) | 44 | 1M | 64k | yes | free promo, no account; Kilo flags it "may train" |
| `step-5-preview-free` (OpenCode Zen) | 44 | not captured | not captured | not captured | free promo; provider zero retention, no training |

Step 5's numbers: Vals Terminal-Bench 4.0 **31.82** *(third-party measurement)* against 18.69 for my local V4 Flash 0731; vendor TB2.1 85.0, GPQA 93.5, BrowseComp 88.7 *(vendor claim)*. `step-3.7-flash` and `step-3.5-flash` have no AA score.

**Limits and prices.** First-party pay-as-you-go, USD per 1M tokens (input / cached / output), 13 Oct 2026: `step-5-preview` 1.00 / 0.10 / 2.70 (third-party sources and OpenRouter show cached at 0.05); `step-3.7-flash` 0.20 / 0.04 / 1.15; `step-3.5-flash` 0.10 / 0.02 / 0.30. **Output includes reasoning tokens.** CN prices for Step 5: CNY 7 / 0.70 / 20.

| Tier | Total top-up | Concurrency | RPM | TPM |
|---|---|---|---|---|
| V0 | under USD 15 | 5 | 100 | 500K |
| V1 | USD 15–69 | 20 | 400 | 2M |
| V2 | USD 70–299 | 30 | 600 | 3M |
| V3 | USD 300–1,499 | 40 | 800 | 4M |
| V4 | USD 1,500+ | 130 | 2,600 | 13M |

Step Plan (third-party prices; the official page shows credits only): Mini USD 6.99 (400M credits/month), Plus 9.99 (1,600M), Pro 29 (8,000M), Max 99 (40,000M). Models: Step 5 Preview, 3.7 Flash, 3.5 Flash. **The credit-to-token conversion and any 5-hour windows were not found.**

**How to get access.**
1. Register on platform.stepfun.ai (the international platform; platform.stepfun.com is the CN one).
2. Top up; USD 15 lifts you from V0 (5 concurrent) to V1 (20 concurrent).
3. Create an API key in the console and export it as `STEPFUN_API_KEY`.
4. For the plan, subscribe on the Step Plan page and check which balance your calls draw from. No Poland region note found.

**Agent fit.** Kilo's catalog lists Step 5 with tools and reasoning low / medium / high; 1M context and 64k output are enough for long loops, but run the tool-call check below on the paid route before relying on it. The launch post says the plan *"works with Cursor, Windsurf, Cline, and your own stack. Zero lock-in"*, so it
**appears to allow your own agents** *(vendor claim, check the ToS)*. I did not capture the direct base URL; the simplest documented path is OpenRouter (`stepfun/step-5-preview`, OpenAI-compatible, same StepFun host and price). With V0's 5 concurrent requests, parallelism equals my local rig's 4 slots; V1 gives 20.

**Reliability.** One host serves the model everywhere (StepFun, FP8), so there is no fallback provider. It is a preview: IDs, prices and limits can change at GA. No uptime data and no accuracy cross-check exist yet. The weights release on 15 Oct 2026 could add third-party hosts, but that is not confirmed.

**Limitations.**
- USD 2.70 output is close to the 3 USD cap; verbose reasoning is billed as output.
- Data terms for the first-party API are unknown.
- Plan credits and the pay-as-you-go balance are separate, so a call can be charged to the wrong one.
- Step Plan value is unknowable until the credit conversion is published.
- Preview model, single host.

**Where it fits in my stack.**
- Free experiments first: the OpenCode Zen variant (zero retention) or Kilo (no account) cost nothing.
- Paid Step 5 as a sub-agent for hard terminal tasks, where TB4.0 31.8 beats my local model clearly.
- On price, GLM-5.3-Flash (TB4.0 37.4 at USD 0.50 output) is the better terminal worker; Step 5 is the second opinion.
- The Step Plan becomes interesting if 400M credits turn out to mean a lot of Step 5 tokens.

**Verify yourself.**
```bash
curl -s https://openrouter.ai/api/v1/models/stepfun/step-5-preview/endpoints \
  | jq '.data.endpoints[]|{provider_name,quantization,pricing,context_length}'
curl -s https://api.kilo.ai/api/gateway/chat/completions -H 'Content-Type: application/json' \
  -d '{"model":"stepfun/step-5-preview-free","messages":[{"role":"user","content":"hi"}]}'
curl -s https://openrouter.ai/api/v1/chat/completions -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"stepfun/step-5-preview","messages":[{"role":"user","content":"Weather in Warsaw?"}],
       "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
```

**Sources:** [StepFun pricing (intl)](https://platform.stepfun.ai/docs/en/guides/pricing/details) · [StepFun pricing (CN)](https://platform.stepfun.com/docs/zh/guides/pricing/details) · [Step Plan](https://platform.stepfun.ai/step-plan) · [StepFun launch post](https://x.com/StepFun_ai/status/2035815197584023835) · [eesel Step 5](https://www.eesel.ai/blog/stepfun-step-5) · [Step Plan prices](https://omidsaffari.com/de/blog/step-5-preview-preise) · [Step 5 open weights](https://www.orcarouter.ai/blog/step-5-preview-open-weights) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [OpenRouter models API](https://openrouter.ai/api/v1/models) · [Kilo models API](https://api.kilo.ai/api/gateway/models) · [OpenCode Zen models](https://opencode.ai/zen/v1/models)

---

## 17. OpenCode Zen

**Type:** free promo + pay-as-you-go · **Best models:** `muse-spark-1.3-contributor-free` (AA 45 at xhigh, trains), `step-5-preview-free` (AA 44), `ling-3.1-flash-free` (AA 41), `mimo-v2.6-flash-free` (AA 38) · **Score: 70** (Q30 C18 L6 A12 R4) · **Data:** Trains on prompts: per model, from no (Step 5: zero retention, no training) to yes (Muse Spark Contributor trains Meta models); hosted in the US and EU

> The OpenCode team's curated gateway with the strongest free lineup in this survey, including Step 5 Preview with zero retention, but it is a weekly-changing promo with unpublished limits that favours its own client.

**What you get.** As of 13 Oct 2026: an account and API key from the opencode.ai console. Free models cost USD 0 "for a limited time", with no end dates. Paid models need billing credit and are priced per token. Models are "hosted in the US and EU" *(vendor claim)*; which region serves a request is not stated.

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `muse-spark-1.3-contributor-free` | 45 (xhigh) | 1M | not captured | not captured | Meta trains on prompts and completions; Responses API only |
| `step-5-preview-free` | 44 | 1M native | not captured | not captured | provider zero retention, no training |
| `ling-3.1-flash-free` | 41 | 1M on AA | not captured | not captured | data used to improve the model |
| `mimo-v2.6-flash-free` | 38 | 1M native | not captured | not captured | data used; TB4.0 24.2 (Vals) |
| GLM 5.3 Flash (paid) | 42 | 1M native | not captured | not captured | USD 0.15 / 0.50, cached 0.03 |

**Muse Spark caveats.** AA 48 is Muse Spark 1.3 at max effort; Meta's docs say the **Contributor ID cannot run at max**, so its ceiling is xhigh = AA 45 *(AA, 13 Oct 2026)*. Vals lists "Muse Spark 1.3" at TB2.1 72.3 / TB4.0 **10.6** and "Muse Spark 1.3 Max" at 79.0 / 24.8 *(third-party measurement)*. My local V4 Flash 0731 scores 18.7 on TB4.0, so the standard 1.3 can be weaker than my rig on hard terminal tasks. Meta's own Contributor tier costs USD 0.10 / 0.20, limited to 150 RPM / 3M TPM per team on 13 Oct 2026 (older blogs say 60 RPM).

**Limits and prices.** Free limits are **not published**. Hitting the ceiling returns `429 FreeUsageLimitError` "Rate limit exceeded" *(third-party report, 18 Aug 2026)*; one directory claims 100 requests/day, unverified. Paid list prices (Zen docs, 13 Oct 2026, USD per 1M input / output / cached): DeepSeek V4 Flash 0.14 / 0.28 / 0.028 (checkpoint not stated), GLM 5.3 Flash 0.15 / 0.50 / 0.03, MiniMax M3 0.30 / 1.20 / 0.06, DeepSeek V4 Pro 1.74 / 3.48, Qwen3.8 Max 2 / 6, Kimi K3 3 / 15. The last three are above the 3 USD cap.

**How to get access.**
1. Sign in to the opencode.ai console and create an API key; export it as `OPENCODE_API_KEY`.
2. Free models need no credit; add billing only for paid models.
3. Pull the live list from `https://opencode.ai/zen/v1/models` before each project: IDs change weekly. I found no region note for Poland.

**Agent fit.** OpenAI-compatible. The docs now use `https://opencode.ai/inference/v1/chat/completions`, plus `/messages` for Anthropic models and `/responses` for GPT and Muse; the older `https://opencode.ai/zen/v1/...` still serves `/models`. Muse Spark needs a Responses API client, so a Chat Completions agent cannot call it unchanged. The catch for my own agents: **reports say direct API calls get 429 while the OpenCode CLI succeeds with the same key** *(third-party report)*, so the free tier looks intended for the OpenCode client. Tool support, max output and concurrency per model were not in my sources.

**Reliability.** Promo churn is weekly. `exo-free` was added on 6 Oct 2026 and is already missing from the live list; `nemotron-3-ultra-free`, `mimo-v2.5-free` and `ling-3.0-flash-fin-free` are in the docs but not live (13 Oct 2026). Stealth models (`space-bunny-free`, `big-pickle`, `cat-jam-free`, `jev-1.13-free`) have unknown identities. No uptime data.

**Limitations.**
- No published limits; 429 can arrive any time, and direct API use may be throttled harder than the CLI.
- Every free model can vanish without notice; no end dates are given.
- Data terms differ per model: Muse, Ling, MiMo and Big Pickle use your data; Step 5, LongCat and Space Bunny do not.
- Muse Spark needs the Responses API, and its Contributor SKU may not match the AA-tested config.
- Paid prices are not better than going to the hosts directly.

**Where it fits in my stack.**
- Free planner trials and evals with Step 5 Preview (zero retention) on non-sensitive tasks.
- Inside the OpenCode CLI as a free coding agent; that is where the free tier works best (see `../agent-harnesses/README.md`).
- Not a backend for production loops: no SLA, no limits, weekly churn. For that I would pay a host or use the rig.
- Muse Spark only on public or throwaway data, because Meta trains on it.

**Verify yourself.**
```bash
curl -s https://opencode.ai/zen/v1/models | jq -r '.data[].id' | grep -E 'free|pickle'
curl -s https://opencode.ai/zen/v1/chat/completions -H "Authorization: Bearer $OPENCODE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"step-5-preview-free","messages":[{"role":"user","content":"hi"}]}'
```

**Sources:** [OpenCode Zen models API](https://opencode.ai/zen/v1/models) · [OpenCode Zen docs](https://opencode.ai/docs/zen/) · [manifest.build 429 FreeUsageLimitError](https://manifest.build/errors/opencode-zen/429-freeusagelimiterror-60fcef/) · [Exo Free promo](https://www.aipromonow.com/en/promos/opencode-exo-free-oct2026) · [AA Muse Spark 1.3](https://artificialanalysis.ai/models/muse-spark-1-3) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [Vals TB2.1](https://www.vals.ai/benchmarks/terminal-bench-2-1) · [Muse Spark Contributor tier](https://cryptobriefing.com/meta-muse-spark-discounted-data-sharing/) · [Muse Spark pricing](https://www.eesel.ai/blog/meta-muse-spark-12-pricing)

---

## 18. Google Gemini API free tier

**Type:** free tier (paid Flex / Batch as fallback) · **Best models:** `gemini-3.8-flash` (AA 41 at high) · **Score: 68** (Q25 C20 L2 A15 R6) · **Data:** Trains on prompts: no from Poland (EEA users get the paid-service data terms on the free tier too); elsewhere yes, with human review; hosting region not stated

> A no-card free tier on a strong, well-documented model with real tool calling and 1M context, but the daily volume is tiny and the terms forbid shipping a free-tier app to EEA users.

**What you get.** As of 13 Oct 2026: a Google account and an AI Studio key give free access to `gemini-3.8-flash`, `gemini-3.6-flash`, the Flash-Lite models, `gemini-3-flash-preview` and Gemma 4. **Pro models left the free tier on 1 Apr 2026** *(third-party report)*, and `gemini-4-argon` is paid only. The volume on 3.8 Flash is **about 20 requests per day** *(third-party measurement)*.

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `gemini-3.8-flash` | 41 (high), 40 (medium), 33 (low) | 1,048,576 | 65,536 | yes, plus structured outputs | thinking low / medium / high; "minimal" errors; multimodal in |
| `gemini-3.6-flash` | no AA score | not captured | not captured | not captured | free; same paid price as 3.8 |

3.8 Flash's numbers: Vals TB2.1 81.27, TB4.0 **19.70** (my local bar is 18.69), GPQA 94.44, MMLU-Pro 90.22, LCB 89.48 *(third-party measurement)*. AA measures time to first token at about 25 s at high effort. Flash-Lite (AA 22) and Gemma 4 31B (AA 15) are below the bar.

**Limits and prices.** Google **no longer publishes free limits**; the docs point to AI Studio's rate-limit page and say "Specified rate limits are not guaranteed". Measured from 429 bodies on 2 Sep 2026: 5 RPM / 20 RPD on the 3.7, 3.6, 3.5 and 3-preview Flash models, 15 RPM / 500 RPD on Flash-Lite; about 20 RPD on 3.8 Flash per a Sep 2026 forum report *(third-party measurements)*. Limits are **per project, not per key**, and reset at midnight Pacific. Search grounding: 500 RPD free. Older pages quoting 1,500 RPD / 10 RPM look stale.

Paid fallback (USD per 1M input / output, page dated 13 Oct 2026): `gemini-3.8-flash` 0.75 / 3.75, cached 0.075, **until 31 Dec 2026, then 1.50 / 7.50**. Batch or Flex: **0.375 / 1.875**, which is in band until 31 Dec 2026 for asynchronous jobs.

**How to get access.**
1. Sign in to AI Studio with a Google account (age 18+); no card needed. Poland is a supported region.
2. Create an API key and export it as `GEMINI_API_KEY`.
3. Check your project's real limits at aistudio.google.com/rate-limit.
4. Extra keys in the same project add no quota; enable billing on the project for Flex / Batch.

**Agent fit.** Native API at `https://generativelanguage.googleapis.com/v1beta`, OpenAI-compatible at `https://generativelanguage.googleapis.com/v1beta/openai/` (chat/completions, tools, streaming); no Anthropic-compatible endpoint. Function calling, structured outputs, caching, code execution and search grounding are supported. Gemini 3.x requires **thought signatures passed back** in multi-turn tool use (not re-verified). The 429 body names the quota (`GenerateRequestsPerDayPerProjectPerModel-FreeTier`), so a router can detect a daily cap and fail over at once instead of retrying. Free-tier latency is the real problem: **27–354 s per request** measured on 3.7 Flash.

**Reliability.** Status at aistudio.google.com/status. Free limits were cut repeatedly in 2025–2026 (Pro removed, Flash down to about 20 RPD). Model churn is fast: 3.5, 3.6, 3.7 and 3.8 Flash all shipped in 2026; the 2.0 models are shut down; 2.5 models return 404 for new users even though they are still listed as free.

**Limitations.**
- About 20 RPD: one agent run with 20 tool turns burns the day.
- **EEA rule:** "You may use only Paid Services when making API Clients available to users in the European Economic Area, Switzerland, or the United Kingdom." Personal dev and testing on free is fine; an app with EU users must be paid.
- Minutes of latency on the free tier.
- **Antigravity and Gemini CLI quota is not an API.** Gemini CLI was replaced by Antigravity CLI on 18 Jun 2026; its free plan has about 20 agent requests/day with a weekly refresh, and Google reportedly suspends accounts that use it through other tools *(third-party reports)*. Do not wire it into my agents.
- The paid list price doubles on 1 Jan 2027.

**Where it fits in my stack.**
- Free eval runner: a few dozen checks a day of 3.8 Flash (AA 41) against my local 34 (see `../course_agentic_apps/14-EVALUATION.md`).
- Long-document reader for non-sensitive input: 1M context and strong knowledge scores, a few calls a day.
- Paid Flex (USD 0.375 / 1.875) as a cheap asynchronous batch worker until 31 Dec 2026.
- Not a sub-agent in loops: the RPD and latency rule that out. Volume stays on the rig.

**Verify yourself.**
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/openai/models" -H "Authorization: Bearer $GEMINI_API_KEY"
curl -s https://generativelanguage.googleapis.com/v1beta/openai/chat/completions \
  -H "Authorization: Bearer $GEMINI_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"gemini-3.8-flash","messages":[{"role":"user","content":"Weather in Warsaw?"}],
       "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
```

**Sources:** [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) · [Gemini models](https://ai.google.dev/gemini-api/docs/models) · [Gemini 3.8 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) · [Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) · [Gemini API terms](https://ai.google.dev/gemini-api/terms) · [dev.to measured limits](https://dev.to/romeroyang/geminis-free-tier-measured-20-requests-a-day-and-google-no-longer-publishes-the-number-4gf2) · [Gemini forum 20 RPD](https://discuss.ai.google.dev/t/gemini-3-8-flash-free-tier-20-rpd-is-too-limited-for-practical-evaluation/180609) · [aifreeapi EEA note](https://www.aifreeapi.com/en/posts/google-gemini-api-free-tier) · [apiyi Pro removal](https://help.apiyi.com/en/google-gemini-api-free-tier-changes-april-2026-guide-en.html) · [Gemini CLI quota](https://geminicli.com/docs/resources/quota-and-pricing/) · [Antigravity credits](https://agentpedia.codes/blog/antigravity-credits-pricing-explained) · [Antigravity review](https://preuve.ai/blog/antigravity-review) · [AA Gemini 3.8 Flash](https://artificialanalysis.ai/models/gemini-3-8-flash) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [Vals TB2.1](https://www.vals.ai/benchmarks/terminal-bench-2-1)

---

## 19. Groq (free tier)

**Type:** free tier · **Best models:** `qwen/qwen3.8-27b` (AA 34), `openai/gpt-oss-120b` (AA 12) ·
**Score: 66** (Q18 C20 L6 A13 R9) · **Data:** trains on prompts: unknown (not addressed, nothing suggests it); no
retention by default except up to 30 days for abuse monitoring, ZDR available; stored in the US (GCP)

> LPU-based inference with a permanent no-card free tier and very high speed; it is in the top 20 because Qwen3.8-27B
> matches my local model (AA 34) at about 450 tok/s for free.

**What you get.** A free tier with no card, a pay-as-you-go Developer tier and Enterprise. Free limits are per
organization and per model. AA = Artificial Analysis Intelligence Index v4.3.2 as of 13 Oct 2026 (my local
V4-Flash-0731 = AA 34).

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `qwen/qwen3.8-27b` | 34 | 131,072 | 16,384 | yes | **preview** · vision · native ctx 256K cut to 128K |
| `openai/gpt-oss-120b` | 12 | 131,072 | 65,536 | yes | production · ~475 t/s, TTFT 0.63 s |

**Limits and prices.** Free tier, 13 Oct 2026:
- Both models: **30 RPM, 1K RPD, 8K TPM, 200K TPD**. Flat since at least Sep 2026.
- Developer prices (USD per 1M, input / output): gpt-oss-120b 0.15 / 0.60 (cached 0.075); qwen3.8-27b 0.80 / **4.00**.
- Batch API −50%; Flex tier gives 10× limits at the same price but fails fast with HTTP 498 `capacity_exceeded`.

**How to get access.**
1. Create an account at console.groq.com; no card needed (third-party reports Sep–Oct 2026). Phone check: unknown.
2. Poland and the EU are fine; only China, Russia, Syria, Iran, North Korea and Cuba are blocked.
3. Create a key under API Keys and export it as `GROQ_API_KEY`.
4. Optional: enable ZDR in Data Controls (it disables Batch).

**Agent fit.** OpenAI-compatible `https://api.groq.com/openai/v1` (Chat Completions and Responses). **No Anthropic
endpoint**; a community proxy (`wearedevx/groq-for-claude-code`) fills the gap. JSON object and JSON schema modes;
`reasoning_effort` and `reasoning_format` on Qwen. **The 8K TPM cap is the real bottleneck**: one 8K prompt eats the
minute. Forum threads report gpt-oss-120b ignoring `tool_choice` or inventing tools; AA endpoint accuracy for Groq
gpt-oss-120b is 90 *(third-party measurement)*. 429 with `x-ratelimit-*` headers when quota runs out.

**Reliability.** groqstatus.com Jul–Oct 2026: production 100%, preview 99.98%, no October incidents. **Catalog churn is
the big risk**: seven models removed since March 2026, including Kimi K2 (15 Apr), Llama 3.x (16 Aug, now
enterprise-only) and `qwen3.6-27b` (14 Sep, about three months after launch). Nvidia licensed Groq's tech in Dec 2025;
Groq says GroqCloud continues.

**Limitations.**
- 8K TPM and 200K TPD: no long-context loops on the free tier.
- Qwen3.8-27B is a preview: replacement within months is likely, and output caps at 16K.
- Paid Qwen output (USD 4.00) is over my budget; stay free or go elsewhere for volume.
- gpt-oss-120b is far below my local model on AA.

**Where it fits in my stack.**
- **Fast, free sub-agent** for short tool-routing and classification calls on Qwen3.8-27B.
- Low-latency fallback when all four local slots are busy and the prompt is small.
- Not a bulk worker and not a planner: prefer local for long context and commercial for planning.

**Verify yourself.**
```bash
curl -s https://api.groq.com/openai/v1/models -H "Authorization: Bearer $GROQ_API_KEY" | jq '.data[].id'
curl -s https://api.groq.com/openai/v1/chat/completions -H "Authorization: Bearer $GROQ_API_KEY" -H "Content-Type: application/json" -d '{
 "model":"qwen/qwen3.8-27b","messages":[{"role":"user","content":"Weather in Krakow?"}],
 "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
```

**Sources:** [Rate limits](https://console.groq.com/docs/rate-limits) · [Models](https://console.groq.com/docs/models) · [Qwen3.8 27B](https://console.groq.com/docs/model/qwen/qwen3.8-27b) · [Deprecations](https://console.groq.com/docs/deprecations) · [Flex](https://console.groq.com/docs/flex-processing) · [Your data](https://console.groq.com/docs/your-data) · [Status](https://groqstatus.com/) · [Tool issue thread](https://community.groq.com/t/gpt-oss-120b-ignoring-tools/385) · [AA gpt-oss providers](https://artificialanalysis.ai/models/gpt-oss-120b/providers) · [AA Qwen vs V4 Flash](https://artificialanalysis.ai/models/comparisons/qwen3-8-27b-vs-deepseek-v4-flash)

---

## 20. Cerebras Inference

**Type:** one-time credits · **Best models:** `qwen-3.8-27b` (AA 34), `gpt-oss-120b` (AA 12) ·
**Score: 66** (Q18 C14 L12 A14 R8) · **Data:** trains on prompts: no; inputs and outputs not retained (privacy policy);
processed in the US and other countries, no EU residency

> Wafer-scale inference with the fastest output speed on the market; it is in the top 20 because Qwen3.8-27B (AA 34,
> equal to my local model) runs at about 1,500–1,850 tok/s with 1M free tokens a day.

**What you get.** Free Trial with a **one-time USD 5 credit that expires 30 days after activation**, a pay-as-you-go
Developer tier, Cerebras Code flat plans (sold out) and Enterprise. AA = Artificial Analysis Intelligence Index v4.3.2
as of 13 Oct 2026 (my local V4-Flash-0731 = AA 34).

**Models.**

| Model | AA | Context | Max output | Tools | Notes |
|---|---|---|---|---|---|
| `qwen-3.8-27b` | 34 | 64K free / 128K paid | 32K free / 40K paid | yes | dense · reasoning high by default |
| `gpt-oss-120b` | 12 | 65K free / 131K paid | 32K free / 40K paid | yes | ~1,686 t/s, TTFT 0.44 s (AA) |

**Limits and prices.** 13 Oct 2026:
- Free Trial, per model: **5 RPM, 30K uncached / 90K total TPM, 1M tokens per hour, 1M tokens per day**.
- Developer: gpt-oss-120b 1K RPM, 1M uncached / 3M total TPM; qwen 300 RPM, 150K / 750K TPM; no daily caps.
- Prices (USD per 1M, input / output): qwen-3.8-27b **0.99 / 1.49**; gpt-oss-120b 0.35 / 0.75. Cached price unknown.
- Cerebras Code Pro USD 50/mo (24M tokens/day) and Max USD 200/mo (120M/day): **"sold out"**; the page still names
  the deprecated GLM-4.7.

**How to get access.**
1. Sign up at cloud.cerebras.ai.
2. **Add a verified payment method** (required since 16 Jul 2026); API stays inactive until you do. Posts saying "no
   card" are stale.
3. No region restriction for Poland found (unknown).
4. Create a key and export it as `CEREBRAS_API_KEY`.

**Agent fit.** OpenAI-compatible `https://api.cerebras.ai/v1`; **no Anthropic endpoint**. Parallel tool calls, all
`tool_choice` modes, strict structured outputs (avoid `pattern`, `minLength`, `maxLength`). Gotchas: gpt-oss
**rejects `tools` plus `response_format` in one request**; `tool_stream` unsupported (use `stream: true`); no `n > 1`.
**5 RPM is tight** for multi-step agents and the 64K free context truncates long histories. Set
`reasoning_effort: "none"` on Qwen for quick routing calls. AA endpoint accuracy for gpt-oss-120b here is 92
*(third-party measurement)*.

**Reliability.** status.cerebras.ai shows no incidents 29 Sep – 13 Oct 2026, but the visible history is short.
**Catalog volatility is the main risk**: the public catalog shrank from about 12 models to 2, with GLM-4.7 removed 17 Aug
and Gemma 4 on 3 Sep 2026; a May 2026 blog reports deletions without notice.

**Limitations.**
- Card required, and the USD 5 credit lasts only 30 days.
- 5 RPM and 64K context on the free trial.
- Only two public models; Kimi K2.6 and GLM-5.x are enterprise Dedicated Endpoints only.
- Flat Code plans are sold out, and which model they serve is unknown.

**Where it fits in my stack.**
- **Latency-critical sub-agent**: fast reasoning bursts on Qwen3.8-27B where my local 13.6 tok/s is too slow.
- Eval runner for short-prompt suites, using the 1M TPD within 5 RPM.
- Paid Qwen at USD 1.49 output is reasonable for speed; for long context stay local (131k per slot).

**Verify yourself.**
```bash
curl -s https://api.cerebras.ai/v1/models -H "Authorization: Bearer $CEREBRAS_API_KEY" | jq '.data[].id'
curl -s https://api.cerebras.ai/v1/chat/completions -H "Authorization: Bearer $CEREBRAS_API_KEY" -H "Content-Type: application/json" -d '{
 "model":"qwen-3.8-27b","reasoning_effort":"none","messages":[{"role":"user","content":"Weather in Krakow?"}],
 "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
```

**Sources:** [Rate limits](https://inference-docs.cerebras.ai/support/rate-limits) · [Models overview](https://inference-docs.cerebras.ai/models/overview) · [Qwen 3.8 27B](https://inference-docs.cerebras.ai/models/qwen-3.8-27b) · [gpt-oss](https://inference-docs.cerebras.ai/models/openai-oss) · [Tool use](https://inference-docs.cerebras.ai/capabilities/tool-use) · [OpenAI compat](https://inference-docs.cerebras.ai/resources/openai) · [Deprecations](https://inference-docs.cerebras.ai/support/deprecation) · [Pricing](https://www.cerebras.ai/pricing) · [Code plans](https://www.cerebras.ai/code) · [Privacy](https://www.cerebras.ai/privacy-policy) · [Status](https://status.cerebras.ai/) · [Catalog volatility blog](https://ianlpaterson.com/blog/free-llm-api-2026/)
