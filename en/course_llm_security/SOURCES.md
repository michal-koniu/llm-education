# Sources — what this course stands on

**Collected 28 October 2026.** Each entry notes **what from it went into the course and where**.

> ⚠️ **This field moves in months.** New attacks, CVEs and defences appear every few weeks, and tool versions
> change their command lines. When a part quotes a number (an attack success rate, a count of exposed servers),
> it is **someone else's measurement on someone else's setup** — repeat it on yours in the lab. CVEs are cited
> with the version that fixed them: if you run something older, update first.
>
> Security research is cited for defence: to explain how an attack works, so you can recognise it, test for it
> and close it on your own systems.

---

## Part 01 · Threat landscape and modelling

Lesson: [`01-THREAT-LANDSCAPE-AND-MODELLING.md`](01-THREAT-LANDSCAPE-AND-MODELLING.md)

| Source | What went into this part (section) |
| :-- | :-- |
| *The lethal trifecta for AI agents: private data, untrusted content, and external communication*, Simon Willison, 2025, https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | §4 the three legs, "avoid the combination" as the only reliable fix; LAB trifecta calculator |
| *Prompt injection attacks against GPT-3*, Simon Willison, 2022, https://simonwillison.net/2022/Sep/12/prompt-injection/ | §4 and §6 origin of the term (12 Sep 2022), the Twitter bot takeover |
| *Agents Rule of Two: A Practical Approach to AI Agent Security*, Meta AI, 2025, https://ai.meta.com/blog/practical-ai-agent-security/ | §4 Rule of Two (31 Oct 2025), broader third leg "change state" |
| *The Confused Deputy (or why capabilities might have been invented)*, Norm Hardy, ACM SIGOPS Operating Systems Review, 1988, https://dl.acm.org/doi/10.1145/54289.871709 | §2.1 the model as a confused deputy |
| *OWASP Top 10 for LLM Applications 2025*, OWASP GenAI Security Project, 2024, https://genai.owasp.org/llm-top-10/ | §5.1 LLM01–LLM10 table, mapping to course parts |
| *OWASP Reveals Updated 2025 Top 10 Risks for LLMs*, OWASP GenAI Security Project, 2024, https://genai.owasp.org/2024/11/17/owasp-reveals-2025-top-10-risks-for-llms-new-sponsorship-program/ | §5.1 release date (November 2024), LLM07/LLM08 new |
| *OWASP Top 10 for Agentic Applications*, OWASP GenAI Security Project, 2025, https://genai.owasp.org/ — walked through in course 2 part 16 (`../course_agentic_apps/16-SECURITY-OWASP-ASI.md`) | §5.2 ASI01–ASI10 and which parts go deeper |
| *MITRE ATLAS*, MITRE, ongoing, https://atlas.mitre.org/ (AML.T0051 https://atlas.mitre.org/techniques/AML.T0051, AML.T0054 https://atlas.mitre.org/techniques/AML.T0054, AML.CS0035 https://atlas.mitre.org/studies/AML.CS0035) | §5.3 tactics/techniques/case studies, example IDs |
| *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations* (NIST AI 100-2 E2025), Vassilev et al., NIST, March 2025, https://csrc.nist.gov/pubs/ai/100/2/e2025/final | §5.4 predictive vs generative taxonomy, goals, capabilities, knowledge levels |
| *Threat Modeling Manifesto*, Braiterman, Shostack et al., 2020, https://www.threatmodelingmanifesto.org/ | §7 the four questions |
| *Threat Modeling Tool threats (STRIDE)*, Microsoft, https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats | §7.4 STRIDE classes; STRIDE per element (origin: Kohnfelder & Garg, Microsoft, 1999) |
| *AI-powered Bing Chat spills its secrets via prompt injection attack*, Benj Edwards, Ars Technica, 2023, https://arstechnica.com/information-technology/2023/02/ai-powered-bing-chat-spills-its-secrets-via-prompt-injection-attack/ | §6 Bing Chat "Sydney" prompt leak (Feb 2023) |
| *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*, Greshake et al., 2023, https://arxiv.org/abs/2302.12173 | §6 indirect prompt injection |
| *March 20 ChatGPT outage: Here's what happened*, OpenAI, 2023, https://openai.com/index/march-20-chatgpt-outage/ | §6 redis-py bug; ~1.2% of Plus subscribers in a 9-hour window (OpenAI's numbers) |
| *Hacking Google Bard — From Prompt Injection to Data Exfiltration*, Johann Rehberger, 2023, https://embracethered.com/blog/posts/2023/google-bard-data-exfiltration/ | §6 markdown-image exfiltration (Nov 2023) |
| *Moffatt v. Air Canada*, 2024 BCCRT 149, BC Civil Resolution Tribunal, 2024, https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html | §2 and §6 chatbot output as a commitment (LLM09) |
| *Data Scientists Targeted by Malicious Hugging Face ML Models with Silent Backdoor*, JFrog, 2024, https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/ | §6 ~100 malicious models (JFrog's count) |
| *CVE-2024-34359* (llama-cpp-python Jinja2 SSTI, fixed in 0.2.72), NVD, 2024, https://nvd.nist.gov/vuln/detail/CVE-2024-34359 | §6 the chat template is code |
| *Data Exfiltration from Slack AI via indirect prompt injection*, PromptArmor, 2024, https://promptarmor.com/resources/data-exfiltration-from-slack-ai-via-indirect-prompt-injection | §6 Slack AI (Aug 2024) |
| *ChatGPT macOS Flaw Could've Enabled Long-Term Spyware via Memory Function*, The Hacker News, 2024, https://thehackernews.com/2024/09/chatgpt-macos-flaw-couldve-enabled-long.html | §6 SpAIware (Rehberger, Sep 2024), fixed in 1.2024.247 |
| *GitHub MCP Exploited: Accessing private repositories via MCP*, Invariant Labs, 2025, https://invariantlabs.ai/blog/mcp-github-vulnerability | §6 toxic agent flow via a public issue (May 2025) |
| *EchoLeak: The First Real-World Zero-Click Prompt Injection Exploit in a Production LLM System*, 2025, https://arxiv.org/abs/2509.10540 · *CVE-2025-32711*, NVD, https://nvd.nist.gov/vuln/detail/CVE-2025-32711 | §6 EchoLeak (Jun 2025, CVSS 9.3) |
| *Compromised Amazon Q extension told AI to delete everything – and it shipped*, The Register, 2025, https://www.theregister.com/2025/07/24/amazon_q_ai_prompt/ | §6 Amazon Q Developer 1.84.0 / fixed 1.85.0 (Jul 2025) |
| Course 1 part 07 (`../course_local_models/07-SANDBOX-SECURITY-MONITORING.md`) and course 2 part 16 (`../course_agentic_apps/16-SECURITY-OWASP-ASI.md`), llm-education, 2026 | §1 order of defences, §7.5 "what we do not defend against", §8 approval built from facts |

## Part 02 · The lab

Lesson: [`02-THE-LAB.md`](02-THE-LAB.md)

| Source | What went into this part (section) |
| :-- | :-- |
| *The lethal trifecta for AI agents: private data, untrusted content, and external communication* — Simon Willison, 16 June 2025 — https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | The three ingredients Sieve has on purpose; "remove one leg" (§0, §2) |
| *Probable inference, the law of succession, and statistical inference* — Edwin B. Wilson, Journal of the American Statistical Association 22(158):209–212, 1927 — https://doi.org/10.1080/01621459.1927.10502953 | The Wilson score interval used by the harness and the interval table (§5.3, `harness.wilson`) |
| *Interval Estimation for a Binomial Proportion* — L. D. Brown, T. T. Cai, A. DasGupta, Statistical Science 16(2):101–133, 2001 — https://doi.org/10.1214/ss/1009213286 | Why the Wald interval fails for small n and proportions near 0/1; Wilson recommended instead (§5.3) |
| *If nothing goes wrong, is everything all right? Interpreting zero numerators* — J. A. Hanley, A. Lippman-Hand, JAMA 249(13):1743–1745, 1983 — https://jamanetwork.com/journals/jama/article-abstract/389714 | The rule of three for 0 successes in n trials (§5.3) |
| *Best-of-N Jailbreaking* — J. Hughes, S. Price, A. Lynch et al., arXiv:2412.03556, December 2024 (NeurIPS 2025) — https://arxiv.org/abs/2412.03556 | Repeated sampling of perturbed prompts; ASR grows with N following a power law — the attacker's arithmetic (§5.4) |
| *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents* — E. Debenedetti et al. (ETH Zurich, Invariant Labs), NeurIPS 2024 Datasets & Benchmarks — https://arxiv.org/abs/2406.13352 | ASR as the standard metric for agents with tools; reporting utility under attack next to ASR (§5.1, §5.5); general shape of a tool-using target with injected content |
| *InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents* — Q. Zhan, Z. Liang, Z. Ying, D. Kang, 2024 — https://arxiv.org/abs/2403.02691 | ASR for indirect injection against tool-using agents (§5.1) |
| *HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal* — M. Mazeika et al., 2024 — https://arxiv.org/abs/2402.04249 | ASR as the standard jailbreak-evaluation metric (§5.1) |
| *Defeating Nondeterminism in LLM Inference* — Horace He and Thinking Machines Lab, September 2025 — https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ (summary: https://simonwillison.net/2025/Sep/11/defeating-nondeterminism/) | Why temperature 0 is not guaranteed to be deterministic in served inference: batch-size variation (§5.2) |
| *Function Calling* (docs/function-calling.md) — ggml-org / llama.cpp — https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md | llama-server handles OpenAI-style tool calls when started with `--jinja`; template overrides (§7, traps 1–2) |
| *llama.cpp HTTP server README* — ggml-org / llama.cpp — https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | OpenAI-compatible `/v1/chat/completions` and `/v1/models`, `--host`, `--port`, `--api-key`, reasoning output (§7, trap 9) |
| *Chat Completions API reference* — OpenAI — https://platform.openai.com/docs/api-reference/chat | Message and `tool_calls` format that `llm.chat()` speaks (§4.1) |
| *OpenAI rolls out imperfect fix for ChatGPT data leak flaw* — BleepingComputer, December 2023 — https://www.bleepingcomputer.com/news/security/openai-rolls-out-imperfect-fix-for-chatgpt-data-leak-flaw/ | Johann Rehberger's April 2023 report of markdown-image exfiltration in ChatGPT (§4.5) |
| *Posts tagged "exfiltration-attacks"* — Simon Willison, 2023–2025 — https://simonwillison.net/tags/exfiltration-attacks/ | The running list of markdown-image exfiltration reports in real products (§4.5) |

## Part 03 · Why models are attackable

Lesson: [`03-WHY-MODELS-ARE-ATTACKABLE.md`](03-WHY-MODELS-ARE-ATTACKABLE.md)

| Source | What went into this part (section) |
| :-- | :-- |
| Course 1 parts 02 and 03 (`../course_local_models/02-MODEL-INTERNALS.md`, `../course_local_models/03-CONTROL-AND-RELIABILITY.md`), llm-education, 2026 | §1 messages are a fiction, `/apply-template`; LAB L1 GGUF reader structure; trap P25 (no system role) |
| *GGUF file format specification*, ggml-org, https://github.com/ggml-org/ggml/blob/master/docs/gguf.md | §2 and L1 value types, `tokenizer.chat_template`, `tokenizer.ggml.token_type` |
| *tiktoken* README / `encode(disallowed_special=...)`, OpenAI, https://github.com/openai/tiktoken | §2 safe-by-default handling of special tokens in text |
| *Tokenizer* documentation (`split_special_tokens`, default False), Hugging Face Transformers, https://huggingface.co/docs/transformers/main_classes/tokenizer | §2 table of defaults |
| *llama.cpp server README* (`/tokenize` `parse_special`, `with_pieces`; `/apply-template`), ggml-org, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md · PR #14783 "server: add parse_special option to /tokenize endpoint", 2025, https://github.com/ggml-org/llama.cpp/pull/14783 | §2 table; LAB L2 and L3 |
| *llama.cpp Jinja engine README* (input marking against special-token injection, introduced in PR #18462), ggml-org, https://github.com/ggml-org/llama.cpp/blob/master/common/jinja/README.md | §2 "depends on your build"; Experiment 03-A prediction |
| *Token Injection: Crashing LLM Inference With Special Tokens*, Ding, Black Hat Europe 2025, https://i.blackhat.com/BH-EU-25/eu-25-Ding-Token-Injection-Crashing-LLM-Inference-With-Special-Tokens-final.pdf | §2.1 special tokens as an availability problem |
| *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions*, Wallace et al., OpenAI, 2024, https://arxiv.org/abs/2404.13208 | §4 system > user > tool, their reported robustness gains |
| *OpenAI Model Spec*, OpenAI, 2024–, https://model-spec.openai.com/ | §4 "chain of command" |
| *StruQ: Defending Against Prompt Injection with Structured Queries*, Chen, Piet, Sitawarin, Wagner, USENIX Security 2025, https://arxiv.org/abs/2402.06363 | §4 and §8 reserved delimiters + filtering them from data + fine-tuning |
| *SecAlign: Defending Against Prompt Injection with Preference Optimization*, Chen et al., ACM CCS 2025, https://arxiv.org/abs/2410.05451 | §4 preference optimisation variant; limits under optimisation attacks |
| *Control Illusion: The Failure of Instruction Hierarchies in Large Language Models*, Geng et al., 2025 (AAAI 2026), https://arxiv.org/abs/2502.15851 | §4 measured limits; social authority beats role; Experiment 03-B hypothesis |
| *Lost in the Middle: How Language Models Use Long Contexts*, Liu et al., 2023, https://arxiv.org/abs/2307.03172 | §5 position effects |
| *Efficient Streaming Language Models with Attention Sinks*, Xiao et al., 2023, https://arxiv.org/abs/2309.17453 | §5 attention sinks |
| *Many-shot jailbreaking*, Anthropic, April 2024, https://www.anthropic.com/research/many-shot-jailbreaking | §5 volume effect |
| *Training language models to follow instructions with human feedback*, Ouyang et al., 2022, https://arxiv.org/abs/2203.02155 | §6 RLHF |
| *Constitutional AI: Harmlessness from AI Feedback*, Bai et al., Anthropic, 2022, https://arxiv.org/abs/2212.08073 | §6 preference tuning |
| *Direct Preference Optimization*, Rafailov et al., 2023, https://arxiv.org/abs/2305.18290 | §6 DPO |
| *Jailbroken: How Does LLM Safety Training Fail?*, Wei, Haghtalab, Steinhardt, 2023, https://arxiv.org/abs/2307.02483 | §6 competing objectives, mismatched generalisation |
| *Safety Alignment Should Be Made More Than Just a Few Tokens Deep*, Qi et al., 2024, https://arxiv.org/abs/2406.05946 | §6 shallow alignment; `p03-text-prefix` case |
| *Refusal in Language Models Is Mediated by a Single Direction*, Arditi et al., NeurIPS 2024, https://arxiv.org/abs/2406.11717 | §6 refusal direction (conceptual only; 13 open models up to 72B) |
| *Towards Understanding Sycophancy in Language Models*, Sharma et al., Anthropic, 2023, https://arxiv.org/abs/2310.13548 | §7 sycophancy across five assistants |
| *Sycophancy in GPT-4o: what happened and what we're doing about it*, OpenAI, April 2025, https://openai.com/index/sycophancy-in-gpt-4o/ | §7 rollback of a sycophantic update |
| *Prompt injection attacks against GPT-3*, Simon Willison, 2022, https://simonwillison.net/2022/Sep/12/prompt-injection/ · *You can't solve AI security problems with more AI*, Simon Willison, 2022, https://simonwillison.net/2022/Sep/17/prompt-injection-more-ai/ | §8 no parameterised query; 99% is a failing grade |
| *The Dual LLM pattern for building AI assistants that can resist prompt injection*, Simon Willison, 2023, https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ | §8 architecture (built in part 07) |
| *Defeating Prompt Injections by Design* (CaMeL), Debenedetti et al., Google DeepMind, 2025, https://arxiv.org/abs/2503.18813 | §8 architecture |
| *Design Patterns for Securing LLM Agents against Prompt Injections*, Beurer-Kellner et al., 2025, https://arxiv.org/abs/2506.08837 | §8 architecture |

## Part 04 · Jailbreaks and alignment

Lesson: [`04-JAILBREAKS-AND-ALIGNMENT.md`](04-JAILBREAKS-AND-ALIGNMENT.md)

| Source | What went into this part (section) |
| :-- | :-- |
| "Prompt injection and jailbreaking are not the same thing", Simon Willison, 2024, https://simonwillison.net/2024/Mar/5/prompt-injection-jailbreaking/ | §0 the jailbreak vs injection distinction |
| "Jailbroken: How Does LLM Safety Training Fail?", Wei, Haghtalab, Steinhardt, 2023 (NeurIPS 2023), https://arxiv.org/abs/2307.02483 | §1.1 competing objectives and mismatched generalisation; §2.4 base64; case `p04-suppress` |
| "Safety Alignment Should Be Made More Than Just a Few Tokens Deep", Qi et al., 2024 (ICLR 2025), https://arxiv.org/abs/2406.05946 | §1.2 shallow alignment; §2.5 why prefill works; §4 |
| "Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models", Shen et al., 2023 (CCS 2024), https://arxiv.org/abs/2308.03825 | §2.1 role-play/DAN family; §3 timeline |
| "Scalable and Transferable Black-Box Jailbreaks for Language Models via Persona Modulation", Shah et al., 2023, https://arxiv.org/abs/2311.03348 | §2.1 automated persona modulation |
| "Mitigating Skeleton Key, a new type of generative AI jailbreak technique", Microsoft Security blog, 2024, https://www.microsoft.com/en-us/security/blog/2024/06/26/mitigating-skeleton-key-a-new-type-of-generative-ai-jailbreak-technique/ | §2.1 guideline-update family; §3; case `p04-guidelines` (benign shape only) |
| "Many-shot jailbreaking", Anil et al., Anthropic, 2024 (NeurIPS 2024), https://www.anthropic.com/research/many-shot-jailbreaking | §2.2 power law, 5 vs 256 shots, 61% → 2% mitigation figure; §7.2 many-shot generator |
| "Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack", Russinovich, Salem, Eldan (Microsoft), 2024 (USENIX Security 2025), https://arxiv.org/abs/2404.01833 | §2.3 multi-turn escalation; §7.3 `p04_multiturn` crescendo variant |
| "Low-Resource Languages Jailbreak GPT-4", Yong, Menghini, Bach, 2023, https://arxiv.org/abs/2310.02446 | §2.4 language family; cases `p04-lang-*` |
| "Best-of-N Jailbreaking", Hughes et al., 2024 (NeurIPS 2025), https://arxiv.org/abs/2412.03556 | §2.4 random augmentations, 89% / 78% at 10,000 samples; §6 rate limits |
| "Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks", Andriushchenko, Croce, Flammarion, 2024, https://arxiv.org/abs/2404.02151 | §2.5 prefill as an attack route |
| llama.cpp server README (`--prefill-assistant` / `--no-prefill-assistant`, default enabled), ggml-org, 2025–2026, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | §2.5 prefill on your own server; §7.3 |
| "Universal and Transferable Adversarial Attacks on Aligned Language Models" (GCG), Zou, Wang, Carlini, Nasr, Kolter, Fredrikson, 2023, https://arxiv.org/abs/2307.15043 | §2.6 GCG and transferability; §3 |
| "AutoDAN: Generating Stealthy Jailbreak Prompts on Aligned Large Language Models", Liu, Xu, Chen, Xiao, 2023 (ICLR 2024), https://arxiv.org/abs/2310.04451 | §2.6 genetic search over readable prompts |
| "Jailbreaking Black Box Large Language Models in Twenty Queries" (PAIR), Chao et al., 2023, https://arxiv.org/abs/2310.08419 | §2.6 attacker-LLM loop; §7.5 PAIR-lite design |
| "Tree of Attacks: Jailbreaking Black-Box LLMs Automatically" (TAP), Mehrotra et al., 2023 (NeurIPS 2024), https://arxiv.org/abs/2312.02119 | §2.6 tree search with pruning |
| "Baseline Defenses for Adversarial Attacks Against Aligned Language Models", Jain et al., 2023, https://arxiv.org/abs/2309.00614 | §2.6 perplexity filtering and its limits; §6 |
| "Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend To!", Qi et al., 2023 (ICLR 2024), https://arxiv.org/abs/2310.03693 | §4 10 examples, < $0.20; benign fine-tuning also degrades safety |
| "Refusal in Language Models Is Mediated by a Single Direction", Arditi et al., 2024 (NeurIPS 2024), https://arxiv.org/abs/2406.11717 | §4 refusal direction in 13 open models, rank-one edit (described conceptually only); §3 |
| "Constitutional Classifiers: Defending against universal jailbreaks", Anthropic, 2025, https://www.anthropic.com/research/constitutional-classifiers | §6 86% → 4.4%, +0.38 pp refusals, +23.7% compute (Anthropic's figures); §3 |
| "Next-generation Constitutional Classifiers", Anthropic, 9 January 2026, https://www.anthropic.com/research/next-generation-constitutional-classifiers | §6 one universal jailbreak found against the first system; ~1% compute next generation |
| "You can't solve AI security problems with more AI", Simon Willison, 2022, https://simonwillison.net/2022/Sep/17/prompt-injection-more-ai/ | §6 the trap of "more AI as the defence"; §7.4 judge design |
| "A customer managed to get the DPD AI chatbot to swear at them, and it wasn't even that hard", TechRadar, January 2024, https://www.techradar.com/pro/a-customer-managed-to-get-the-dpd-ai-chatbot-to-swear-at-them-and-it-wasnt-even-that-hard | §3 the parcel-company chatbot incident (company statement about a system update) |
| Course 1 part 07 and course 2 part 16 of this repository (`../course_local_models/07-SANDBOX-SECURITY-MONITORING.md`, `../course_agentic_apps/16-SECURITY-OWASP-ASI.md`), 2026 | links in the closing section; ASI01 context |

## Part 05 · Direct prompt injection and prompt leaks

Lesson: [`05-DIRECT-PROMPT-INJECTION-AND-PROMPT-LEAKS.md`](05-DIRECT-PROMPT-INJECTION-AND-PROMPT-LEAKS.md)

| Source | What went into this part (section) |
| :-- | :-- |
| "Prompt injection attacks against GPT-3", Simon Willison, 2022, https://simonwillison.net/2022/Sep/12/prompt-injection/ | §1 history: the term and Riley Goodside's "ignore the above directions" examples; §4 |
| "Ignore Previous Prompt: Attack Techniques For Language Models", Perez, Ribeiro, 2022 (NeurIPS ML Safety Workshop), https://arxiv.org/abs/2211.09527 | §1 the names *goal hijacking* and *prompt leaking*; §4 |
| OWASP Top 10 for LLM Applications 2025 (LLM01 Prompt Injection, LLM06 Excessive Agency), OWASP GenAI Security Project, 2024, https://genai.owasp.org/llm-top-10/ | §1 map table; §4 |
| "LLM07:2025 System Prompt Leakage", OWASP GenAI Security Project, 2024, https://genai.owasp.org/llmrisk/llm072025-system-prompt-leakage/ | §1 "not a secret, not a security control"; §3.4; §4 |
| "The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions", Wallace et al. (OpenAI), 2024, https://arxiv.org/abs/2404.13208 | §2.1 role priority as a learned preference; §5 research defences |
| "GM dealer chat bot agrees to sell 2024 Chevy Tahoe for $1", GM Authority, December 2023, https://gmauthority.com/blog/2023/12/gm-dealer-chat-bot-agrees-to-sell-2024-chevy-tahoe-for-1/ | §2.3 the dealer case: missing capability as the defence; §4 |
| "AI-powered Bing Chat spills its secrets via prompt injection attack", Ars Technica (B. Edwards), 10 February 2023, recorded as AI Incident Database report 2666, https://incidentdatabase.ai/reports/2666 | §3.3 Bing Chat / "Sydney" prompt disclosure; §4 |
| OECD AI Incidents Monitor, "Bing Chatbot Exposes Confidential Instructions After Prompt Injection Attack", 2023, https://oecd.ai/en/incidents/2023-02-10-4440 | §3.3 date and Microsoft's confirmation |
| "Effective Prompt Extraction from Language Models" (v1: "Prompts Should Not Be Seen as Secrets"), Zhang, Carlini, Ippolito, 2023–2024, https://arxiv.org/abs/2307.06865 | §3.1 argument; §3.3 11 models, output filters insufficient, translation-style attacks; §4 |
| "Assessing Prompt Injection Risks in 200+ Custom GPTs", Yu et al., 2023, https://arxiv.org/abs/2311.11538 | §3.3 90/96 and 120/120 system prompts extracted (their table); defensive prompts ineffective |
| Gandalf, Lakera, 2023, https://gandalf.lakera.ai/ | §3.3 game evidence for layered input/output checks being bypassed |
| "Tensor Trust: Interpretable Prompt Injection Attacks from an Online Game", Toyer et al., 2023 (ICLR 2024), https://arxiv.org/abs/2311.01011 | §3.3 crowd-sourced hijacking and extraction attacks |
| System prompts release notes, Anthropic documentation, since August 2024, https://docs.anthropic.com/en/release-notes/system-prompts | §3.3 a vendor publishing its prompts; §4 |
| Rebuff (canary-word leak detection), Protect AI, 2023, https://github.com/protectai/rebuff | §5 D2 canary word; §6.2 |
| "StruQ: Defending Against Prompt Injection with Structured Queries", Chen, Piet, Sitawarin, Wagner, 2024, https://arxiv.org/abs/2402.06363 | §5 research defences |
| "SecAlign: Defending Against Prompt Injection with Preference Optimization", Chen et al., 2024–2025, https://arxiv.org/abs/2410.05451 | §5 research defences |
| "Meta SecAlign: A Secure Foundation LLM Against Prompt Injection Attacks", Chen, Zharmagambetov, Wagner, Guo, 2025, https://arxiv.org/abs/2507.02735 | §5 open models with model-level injection defence |
| "A Critical Evaluation of Defenses against Prompt Injection Attacks", 2025, https://arxiv.org/abs/2505.18333 | §5 fixed attack prompts vs adaptive attacks |
| "Jailbroken" (Wei et al., 2023) and "Safety Alignment Should Be Made More Than Just a Few Tokens Deep" (Qi et al., 2024) — full entries in part 04 sources | §2.2 completion priming; §3.1 "never reveal" as a competing preference |
| Course 2 part 16 of this repository (`../course_agentic_apps/16-SECURITY-OWASP-ASI.md`), 2026 | §1 ASI01 goal hijack; closing links |

## Part 06 · Indirect prompt injection and RAG poisoning

Lesson: [`06-INDIRECT-PROMPT-INJECTION-AND-RAG-POISONING.md`](06-INDIRECT-PROMPT-INJECTION-AND-RAG-POISONING.md)

| Source | What went into this part (section) |
| :-- | :-- |
| Greshake, Abdelnabi, Mishra, Endres, Holz, Fritz, "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection", arXiv 2302.12173, Feb 2023, https://arxiv.org/abs/2302.12173 | the term, delivery taxonomy and goals (§1.2, §4) |
| Hines et al. (Microsoft), "Defending Against Indirect Prompt Injection Attacks With Spotlighting", arXiv 2403.14720, Mar 2024, https://arxiv.org/abs/2403.14720 | delimiting / datamarking / encoding; the reported ASR drop from >50% to <2% on GPT-family models (§5.2, `Spotlight`) |
| Zou, Geng, Wang, Jia, "PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models", USENIX Security 2025, arXiv 2402.07867, https://www.usenix.org/conference/usenixsecurity25/presentation/zou | retrieval and generation conditions; ~90% ASR with 5 texts per target question (§3.1, §4) |
| Nasr et al., "The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections", arXiv 2510.09023, Oct 2025, https://arxiv.org/abs/2510.09023 | detectors and adaptive attackers: 12 defences bypassed (§5.3, §7 warning) |
| Wallace et al. (OpenAI), "The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions", arXiv 2404.13208, Apr 2024, https://arxiv.org/abs/2404.13208 | training-time help (§5.5) |
| PromptArmor, "Data Exfiltration from Slack AI via indirect prompt injection", Aug 2024, https://promptarmor.substack.com/p/data-exfiltration-from-slack-ai-via | real-world table (§4) |
| Simon Willison, "Hacking Google Bard - From Prompt Injection to Data Exfiltration" (summary of J. Rehberger's research), 4 Nov 2023, https://simonwillison.net/2023/Nov/4/hacking-google-bard-from-prompt-injection-to-data-exfiltration/ | real-world table (§4); report/fix dates are from secondary reports |
| The Hacker News, "Microsoft Fixes ASCII Smuggling Flaw", Aug 2024, https://thehackernews.com/2024/08/microsoft-fixes-ascii-smuggling-flaw.html | Unicode tag characters in Copilot (§2, §4) |
| Reddy et al., "EchoLeak: The First Real-World Zero-Click Prompt Injection Exploit in a Production LLM System", arXiv 2509.10540, 2025, https://arxiv.org/abs/2509.10540 (CVE-2025-32711) | real-world table (§4); details in part 07 |

## Part 07 · Agents, tools and exfiltration

Lesson: [`07-AGENTS-TOOLS-AND-EXFILTRATION.md`](07-AGENTS-TOOLS-AND-EXFILTRATION.md)

| Source | What went into this part (section) |
| :-- | :-- |
| OWASP Top 10 for LLM Applications 2025, LLM06 Excessive Agency, https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ | three root causes: functionality, permissions, autonomy (§1.1) |
| Norm Hardy, "The Confused Deputy (or why capabilities might have been invented)", ACM SIGOPS Operating Systems Review 22(4), 1988, https://dl.acm.org/doi/10.1145/54289.871709 | confused deputy and the capability fix (§1.2) |
| Simon Willison, "The lethal trifecta for AI agents", 16 Jun 2025, https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | trifecta (§1.3) |
| Meta AI, "Agents Rule of Two", 31 Oct 2025, as discussed in Simon Willison, "New prompt injection papers: Agents Rule of Two and The Attacker Moves Second", 2 Nov 2025, https://simonwillison.net/2025/nov/2/new-prompt-injection-papers | Rule of Two (§1.3) |
| Simon Willison, "The Dual LLM pattern for building AI assistants that can resist prompt injection", Apr 2023, https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ | dual-LLM idea (§5.2) |
| Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against Prompt Injections", arXiv 2506.08837, Jun 2025, https://arxiv.org/abs/2506.08837 | the six patterns and shared principle (§5.2) |
| Debenedetti et al., "Defeating Prompt Injections by Design" (CaMeL), arXiv 2503.18813, Mar 2025 (v2 Jun 2025), https://arxiv.org/abs/2503.18813 | architecture, 77% vs 84% on AgentDojo (authors' figures), limits (§7); `camel_lite` is our simplification |
| Debenedetti et al., "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents", NeurIPS 2024, arXiv 2406.13352, https://arxiv.org/abs/2406.13352 | benchmark behind the CaMeL numbers (§7.1) |
| Reddy et al., "EchoLeak: The First Real-World Zero-Click Prompt Injection Exploit in a Production LLM System", arXiv 2509.10540, 2025, https://arxiv.org/abs/2509.10540 (CVE-2025-32711, CVSS 9.3 per Microsoft) | EchoLeak chain (§4) |
| Simon Willison, "Hacking Google Bard - From Prompt Injection to Data Exfiltration", 4 Nov 2023, https://simonwillison.net/2023/Nov/4/hacking-google-bard-from-prompt-injection-to-data-exfiltration/ | Bard case, CSP and allowlisted collector (§4) |
| PromptArmor, "Data Exfiltration from Slack AI via indirect prompt injection", Aug 2024, https://promptarmor.substack.com/p/data-exfiltration-from-slack-ai-via | Slack AI link exfiltration (§4) |
| The Hacker News, "Microsoft Fixes ASCII Smuggling Flaw", Aug 2024, https://thehackernews.com/2024/08/microsoft-fixes-ascii-smuggling-flaw.html | ASCII smuggling in Copilot (§4) |
| Nasr et al., "The Attacker Moves Second", arXiv 2510.09023, Oct 2025, https://arxiv.org/abs/2510.09023 | why static zeros are not safety (§6.3 warning) |

## Part 08 · MCP, skills, memory and multi-agent

Lesson: [`08-MCP-SKILLS-MEMORY-AND-MULTI-AGENT.md`](08-MCP-SKILLS-MEMORY-AND-MULTI-AGENT.md)

| Source | What went into this part (section) |
| :-- | :-- |
| Model Context Protocol, *Specification 2026-07-28*, overview "Security and Trust & Safety", 2026, https://modelcontextprotocol.io/specification/2026-07-28 | tool descriptions/annotations untrusted unless from a trusted server; consent; MCP cannot enforce at protocol level (§2.8) |
| Model Context Protocol, *Security Best Practices* (spec 2026-07-28), 2026, https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices | confused deputy, token passthrough, SSRF, state handle hijacking, local server compromise, scope minimisation (§2.6, §2.7) |
| NSA AI Security Center, *Model Context Protocol (MCP): Security Design Considerations for AI-Driven Automation* (CSI), 20 May 2026, https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf | adoption outpacing security model; sandbox, validate, log, inventory (§2.8, §6) |
| Invariant Labs, *MCP Security Notification: Tool Poisoning Attacks*, 1 Apr 2025, https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks | tool poisoning, rug pulls, shadowing (§2.2–2.4, §6) |
| Invariant Labs, *GitHub MCP Exploited: Accessing private repositories via MCP*, 26 May 2025, https://invariantlabs.ai/blog/mcp-github-vulnerability | toxic flow with an honest server (§2.5, §6) |
| Oligo Security / NVD, CVE-2025-49596 (MCP Inspector < 0.14.1), Jun 2025, https://nvd.nist.gov/vuln/detail/CVE-2025-49596 | local developer tool reachable from the browser; fixed version (§2.6) |
| JFrog, CVE-2025-6514 in mcp-remote (fixed 0.1.16), 9 Jul 2025, https://jfrog.com/blog/2025-6514-critical-mcp-remote-rce-vulnerability/ | command injection via authorization URL (§2.6) |
| Koi Security via The Hacker News, *First Malicious MCP Server Found Stealing Emails* (postmark-mcp 1.0.16), Sep 2025, https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html | malicious MCP package in the wild (§2.6, §6) |
| Koi Security via eSecurity Planet, *Hundreds of Malicious Skills Found in OpenClaw's ClawHub* (ClawHavoc), Feb 2026, https://www.esecurityplanet.com/threats/hundreds-of-malicious-skills-found-in-openclaws-clawhub/ | 341 malicious of 2,857 skills (§3, §6) |
| Snyk, *ToxicSkills: malicious AI agent skills on ClawHub*, Feb 2026, https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub | 76 confirmed malicious of 3,984 skills (§3, §6) |
| Johann Rehberger via The Hacker News, *ChatGPT macOS flaw could've enabled long-term spyware via memory* (SpAIware), Sep 2024, https://thehackernews.com/2024/09/chatgpt-macos-flaw-couldve-enabled-long.html | memory persistence, fix in 1.2024.247 (§4.2, §6) |
| Johann Rehberger via InfoQ, *Gemini long-term memory attack* (delayed tool invocation), Feb 2025, https://www.infoq.com/news/2025/02/gemini-long-term-memory-attack/ | delayed tool invocation (§4.2, §6) |
| Z. Chen, Z. Xiang, C. Xiao, D. Song, B. Li, *AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases*, NeurIPS 2024, https://arxiv.org/abs/2407.12784 | trigger-keyed memory poisoning (§4.2) |
| Dong et al., *Memory Injection Attacks on LLM Agents via Query-Only Interaction* (MINJA), 2025, https://arxiv.org/abs/2503.03704 | memory injection through queries only (§4.2) |
| Lee, Tiwari, *Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems*, Oct 2024, https://arxiv.org/abs/2410.07283 | self-replicating injection, LLM tagging (§5, §6) |
| Triedman, Jha, Shmatikov, *Multi-Agent Systems Execute Arbitrary Malicious Code*, Mar 2025 (v2 Sep 2025, COLM 2025), https://arxiv.org/abs/2503.12188 | MAS control-flow hijacking, 58–90% (v2, GPT-4o) (§5, §6) |
| AppOmni, *AI agent-to-agent discovery prompt injection* (ServiceNow Now Assist), Nov 2025, https://appomni.com/ao-labs/ai-agent-to-agent-discovery-prompt-injection/ | second-order injection via agent discovery (§5, §6) |
| OWASP GenAI Security Project, *Top 10 for Agentic Applications* (ASI04, ASI06, ASI07), Dec 2025, https://genai.owasp.org/ | framing; see course 2 part 16 (§0) |
| Simon Willison, *The lethal trifecta for AI agents*, Jun 2025, https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | trifecta reading of the GitHub case (§2.5) |
| llm-education course 2, parts 5, 6, 9, 13, 16 (this repository) | memory quarantine, skills, MCP, fleets, ASI map (links throughout) |

## Part 09 · Output handling, code and resources

Lesson: [`09-OUTPUT-HANDLING-CODE-AND-RESOURCES.md`](09-OUTPUT-HANDLING-CODE-AND-RESOURCES.md)

| Source | What went into this part (section) |
| :-- | :-- |
| OWASP GenAI Security Project, *LLM05:2025 Improper Output Handling*, 2025, https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/ | framing of output handling (§0, §1) |
| OWASP GenAI Security Project, *LLM10:2025 Unbounded Consumption*, 2025, https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/ | framing of consumption risks, denial of wallet (§0, §6) |
| NVD / GitHub advisory, CVE-2025-46719, Open WebUI stored XSS in markdown rendering (fixed 0.6.6), 2025, https://nvd.nist.gov/vuln/detail/CVE-2025-46719 | XSS in a self-hosted chat UI (§2.2, §7) |
| The Hacker News, *Researchers Uncover Prompt Injection Vulnerabilities in DeepSeek and Claude AI* (Rehberger: DeepSeek XSS → account takeover; Terminal DiLLMa), Dec 2024, https://thehackernews.com/2024/12/researchers-uncover-prompt-injection.html | prompt injection to XSS; ANSI escapes in terminals (§2.2, §3.4, §7) |
| Pedro, Castro, Carreira, Santos, *From Prompt Injections to SQL Injection Attacks: How Protected is Your LLM-Integrated Web Application?*, arXiv 2023 / ICSE 2025, https://arxiv.org/abs/2308.01990 | prompt-to-SQL attacks (§3.1, §7) |
| JFrog, *Critical RCE Vulnerability in mcp-remote: CVE-2025-6514*, 9 Jul 2025, https://jfrog.com/blog/2025-6514-critical-mcp-remote-rce-vulnerability/ | URL to shell; fixed 0.1.16 (§3.2, §7) |
| Model Context Protocol, *Security Best Practices* (spec 2026-07-28), "OAuth Authorization URL Validation", 2026, https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices | MUST NOT use a shell to open URLs; scheme allowlist; CSP (§2.3, §3.2) |
| GitLab advisory database, CVE-2023-39662 (llama-index, fixed 0.9.14), https://advisories.gitlab.com/pkg/pypi/llama-index/CVE-2023-39662/ | exec of model output in PandasQueryEngine (§4.2, §7) |
| GitLab advisory database, CVE-2024-3098 (llama-index-core, fixed 0.10.24), https://advisories.gitlab.com/pkg/pypi/llama-index-core/CVE-2024-3098/ | bypass of the previous fix (§4.2, §7) |
| Spracklen, Wijewickrama, Sakib, Maiti, Viswanath, Jadliwala, *We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs*, USENIX Security 2025, https://arxiv.org/abs/2406.10279 | 576,000 samples, 16 models, 5.2% / 21.7%, 205,474 names (§5, §7) |
| Kumar et al., *OverThink: Slowdown Attacks on Reasoning LLMs*, 2025, https://arxiv.org/abs/2502.02542 | reasoning-token slowdown attacks (§6.2, §7) |
| Shumailov, Zhao, Bates, Papernot, Mullins, Anderson, *Sponge Examples: Energy-Latency Attacks on Neural Networks*, IEEE EuroS&P 2021, https://arxiv.org/abs/2006.03463 | inputs crafted for cost (§6.2, §7) |
| ggml-org, *llama.cpp server README* (flags `--api-key`, `-n`, `-c`, `-np`, `-to`, `--metrics`; `n_predict`, `t_max_predict_ms`), checked Oct 2026, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | server knobs and defaults (§6.3) |
| Python documentation, `sqlite3` (`set_authorizer`, `set_progress_handler`, URI `mode=ro`), https://docs.python.org/3/library/sqlite3.html | least-privilege SQL executor (§3.1, §9.3) |
| llm-education course 1 part 07 and course 2 parts 10, 16 (this repository) | sandboxing, egress, ASI05/ASI09 (§4.3, links) |

## Part 10 · Model supply chain

Lesson: [`10-MODEL-SUPPLY-CHAIN.md`](10-MODEL-SUPPLY-CHAIN.md)

| Source | What went into this part (section) |
| :-- | :-- |
| *pickle — Python object serialization* (warning box), Python Software Foundation, current docs, https://docs.python.org/3/library/pickle.html | pickle as a stack machine; "never unpickle untrusted data"; `__reduce__` (§2.1, §10.1) |
| *pickletools — Tools for pickle developers*, Python Software Foundation, current docs, https://docs.python.org/3/library/pickletools.html | `genops` as a non-executing opcode decoder for the scanner (§10.2) |
| *torch.load* documentation (`weights_only`), PyTorch, current docs, https://pytorch.org/docs/stable/generated/torch.load.html | restricted unpickler; default changed in PyTorch 2.6 (§2.2) |
| CVE-2025-32434, *PyTorch: torch.load with weights_only=True leads to remote code execution*, NVD, 2025, https://nvd.nist.gov/vuln/detail/CVE-2025-32434 | affected ≤ 2.5.1, fixed in 2.6.0; bug class (§2.2, §9) |
| *Data Scientists Targeted by Malicious Hugging Face ML Models with Silent Backdoor*, JFrog, Feb 2024, https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/ | ~100 models running code on load (their count) (§2.3, §9) |
| *Malicious ML models discovered on Hugging Face platform* (nullifAI), ReversingLabs, Feb 2025, https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face | 7z-wrapped, broken pickle evading picklescan (§2.3, §9, §10.3) |
| CVE-2025-10155 / CVE-2025-10156 / CVE-2025-10157 (picklescan), OSV, 2025, https://osv.dev/vulnerability/CVE-2025-10155 | extension-mismatch and submodule-import bypasses, fixed in 0.0.31 (§2.3, §9) |
| *4M Models Scanned: Protect AI + Hugging Face 6 Months In*, Hugging Face / Protect AI, 2025, https://huggingface.co/blog/pai-6-month | partnership since Oct 2024; 352,000 issues across 51,700 models (their count) (§2.3) |
| *safetensors*, Hugging Face, repository and format description, https://github.com/huggingface/safetensors | header layout, 100 MB header limit, no code path (§3) |
| *GGUF* specification, ggml-org, https://github.com/ggml-org/ggml/blob/master/docs/gguf.md | header layout, value types, alignment, tensor infos (§4, §10.4) |
| TALOS-2024-1916 / CVE-2024-23605 (and TALOS-2024-1915 / CVE-2024-21836), Cisco Talos, Feb 2024, https://www.talosintelligence.com/vulnerability_reports/TALOS-2024-1916 | GGUF `n_kv` / `n_tensors` heap overflows, patch 29 Jan 2024; "check counts before allocating" (§4, §9) |
| CVE-2024-21836, NVD, 2024, https://nvd.nist.gov/vuln/detail/CVE-2024-21836 | severity, Databricks co-report (§4) |
| *Llama Drama: Critical Vulnerability CVE-2024-34359 Threatening Your Software Supply Chain*, Checkmarx, May 2024, https://checkmarx.com/blog/llama-drama-critical-vulnerability-cve-2024-34359-threatening-your-software-supply-chain/ | Jinja2 SSTI in llama-cpp-python, 0.2.30–0.2.71, fixed in 0.2.72 (§5.1, §9) |
| CVE-2024-34359, NVD, 2024, https://nvd.nist.gov/vuln/detail/CVE-2024-34359 | advisory and fix commit reference (§5.1) |
| *llama-server* README (`--jinja`, `--chat-template-file`), ggml-org/llama.cpp, current, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | using your own pinned template (§5.3, §10.5) |
| *Customizing models* (`trust_remote_code`), Hugging Face Transformers docs, https://huggingface.co/docs/transformers/custom_models | what the flag executes; revision pinning (§6) |
| *PoisonGPT* incident report (Mithril Security, Jul 2023), AI Incident Database, https://incidentdatabase.ai/reports/3206/ | ROME-edited GPT-J under a look-alike org name (§7, §8.1, §9) |
| Hubinger et al., *Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training*, Anthropic, Jan 2024, https://arxiv.org/abs/2401.05566 | backdoors survive SFT/RL/adversarial training (§7, §9) |
| Egashira, Vero, Staab, He, Vechev, *Exploiting LLM Quantization*, NeurIPS 2024, https://arxiv.org/abs/2405.18137 | benign in full precision, malicious after quantisation (§7) |
| Egashira, Staab, Vero, He, Vechev, *Mind the Gap: A Practical Attack on GGUF Quantization*, ICML 2025, https://arxiv.org/abs/2505.23786 | the same on GGUF k-quants (§7, §9) |
| *A small number of samples can poison LLMs of any size*, Anthropic with UK AI Security Institute and Alan Turing Institute, Oct 2025, https://www.anthropic.com/research/small-samples-poison | ~250 documents, absolute count matters (§7, §9) |
| *Model Namespace Reuse: An AI Supply-Chain Attack Exploiting Model Name Trust*, Palo Alto Networks Unit 42, 2025, https://unit42.paloaltonetworks.com/model-namespace-reuse/ | re-registered namespaces; pin revisions (§8.1, §9) |
| *Taming the Wild West of ML: Practical Model Signing with Sigstore* (model-signing v1.0), Sigstore / OpenSSF, Apr 2025, https://blog.sigstore.dev/model-transparency-v1.0 | model signing, transparency log, what a signature proves (§8.3, §9) |
| CycloneDX ML-BOM, OWASP CycloneDX, https://cyclonedx.org/ ; SPDX 3.0 AI and Dataset profiles, Linux Foundation, https://spdx.dev/ | ML-BOM; the lock file as a minimal ML-BOM (§8.3) |
| Course 2, part 16 §5 (ASI04), this repository, `../course_agentic_apps/16-SECURITY-OWASP-ASI.md` | supply registry and checksum-on-load, extended here to models (§0, §10.5) |

## Part 11 · Privacy and data leakage

Lesson: [`11-PRIVACY-AND-DATA-LEAKAGE.md`](11-PRIVACY-AND-DATA-LEAKAGE.md)

| Source | What went into this part (section) |
| :-- | :-- |
| Carlini, Liu, Erlingsson, Kos, Song, *The Secret Sharer: Evaluating and Testing Unintended Memorization in Neural Networks*, USENIX Security 2019, https://arxiv.org/abs/1802.08232 | canaries and the exposure metric; memorisation of rare secrets (§2) |
| Carlini et al., *Extracting Training Data from Large Language Models*, USENIX Security 2021, https://arxiv.org/abs/2012.07805 | verbatim extraction from GPT-2, including personal data (§2) |
| Carlini et al., *Quantifying Memorization Across Neural Language Models*, ICLR 2023, https://arxiv.org/abs/2202.07646 | memorisation grows with size, duplication and context (§2) |
| Nasr et al., *Scalable Extraction of Training Data from (Production) Language Models*, Nov 2023, https://arxiv.org/abs/2311.17035 | divergence attack on an aligned production model (§2) |
| Shokri, Stronati, Song, Shmatikov, *Membership Inference Attacks against Machine Learning Models*, IEEE S&P 2017, https://arxiv.org/abs/1610.05820 | the classic membership inference setting (§3) |
| Duan et al., *Do Membership Inference Attacks Work on Large Language Models?*, COLM 2024, https://arxiv.org/abs/2402.07841 | near-random MIA on LLM pretraining data; why (§3) |
| Morris, Kuleshov, Shmatikov, Rush, *Text Embeddings Reveal (Almost) As Much As Text* (vec2text), EMNLP 2023, https://arxiv.org/abs/2310.06816 | 92% exact recovery of 32-token inputs (their measurement); names from clinical notes (§4) |
| Gu et al., *Auditing Prompt Caching in Language Model APIs*, ICML 2025, https://arxiv.org/abs/2502.07776 | 8 of 17 providers cached, 7 shared globally (Sep–Oct 2024 audits); mitigations (§6.1) |
| Wu et al., *I Know What You Asked: Prompt Leakage via KV-Cache Sharing in Multi-Tenant LLM Serving*, NDSS 2025, https://www.ndss-symposium.org/ndss-paper/i-know-what-you-asked-prompt-leakage-via-kv-cache-sharing-in-multi-tenant-llm-serving/ | prompt reconstruction via shared KV cache on vLLM/SGLang (§6.1) |
| Song et al., *The Early Bird Catches the Leak: Unveiling Timing Side Channels in LLM Serving Systems*, 2024, https://arxiv.org/abs/2409.20002 | timing side channels in serving systems (§6.1) |
| *Automatic Prefix Caching* design doc (`cache_salt`), vLLM, current, https://docs.vllm.ai/design/prefix_caching.html | per-tenant cache isolation by salting (§6.1) |
| *llama-server* README (`/slots`, `--no-slots`, `cache_prompt`), ggml-org/llama.cpp, current, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | per-slot prompt cache; slot state may contain prompts (§6.1, §6.2, §10.5) |
| Weiss et al., *What Was Your Prompt? A Remote Keylogging Attack on AI Assistants*, USENIX Security 2024, https://arxiv.org/abs/2403.09751 | token-length side channel in streamed responses (§6.3) |
| *Whisper Leak: a novel side-channel cyberattack on remote language models*, Microsoft, Nov 2025, https://www.microsoft.com/en-us/security/blog/2025/11/07/whisper-leak-a-novel-side-channel-cyberattack-on-remote-language-models/ | topic inference from packet sizes and timing; partial mitigations (§6.3) |
| Carlini et al., *Stealing Part of a Production Language Model*, ICML 2024, https://arxiv.org/abs/2403.06634 | projection layer recovered via logprobs + logit_bias for under $20 (their figure) (§7) |
| *March 20 ChatGPT outage: Here's what happened*, OpenAI, Mar 2023, https://openai.com/index/march-20-chatgpt-outage/ | other users' chat titles; ~1.2% of Plus subscribers' payment details (§8) |
| *Samsung Bans Staff's AI Use After Spotting ChatGPT Data Leak*, Bloomberg, May 2023, https://www.bloomberg.com/news/articles/2023-05-02/samsung-bans-chatgpt-and-other-generative-ai-use-by-staff-after-leak | employees pasting internal code into a chatbot (§8) |
| *Wiz Research Uncovers Exposed DeepSeek Database Leaking Sensitive Information, Including Chat History*, Wiz, Jan 2025, https://www.wiz.io/blog/wiz-research-uncovers-exposed-deepseek-database-leak | unauthenticated ClickHouse with chat logs and keys (§8) |
| *OpenAI kills "short-lived experiment" where ChatGPT chats could be found on Google*, Malwarebytes, Aug 2025, https://www.malwarebytes.com/blog/news/2025/08/openai-kills-short-lived-experiment-where-chatgpt-chats-could-be-found-on-google | shared chats indexed by search engines; option removed 1 Aug 2025 (§8) |
| Regulation (EU) 2016/679 (GDPR), Art. 5 and Art. 17, EUR-Lex, https://eur-lex.europa.eu/eli/reg/2016/679/oj | minimisation, storage limitation, right to erasure (§9) |
| *Opinion 28/2024 on certain data protection aspects related to the processing of personal data in the context of AI models*, European Data Protection Board, Dec 2024, https://www.edpb.europa.eu/our-work-tools/our-documents/opinion-board-art-64/opinion-282024-certain-data-protection-aspects_en | model anonymity assessed case by case (§9) |
| Part 14 §2–§3 of this course, this repository, `14-DETECTION-MONITORING-AND-INCIDENT-RESPONSE.md` | what to log and how to store it; linked instead of repeated (§8) |

## Part 12 · Local infrastructure

Lesson: [`12-LOCAL-INFRASTRUCTURE.md`](12-LOCAL-INFRASTRUCTURE.md)

| Source | What went into this part (section) |
| :-- | :-- |
| Cisco, scan of exposed Ollama servers (Sep 2025): 1,139 servers. URL not re-verified in this session; search "Cisco exposed Ollama servers 2025" | the exposure count, attributed to Cisco (§2.2) |
| SentinelOne + Censys, research on exposed open-source LLM hosts (Jan 2026): about 175,000 hosts. URL not re-verified in this session | the second exposure count, attributed to them (§2.2) |
| llama.cpp `llama-server` README, ggml-org, https://github.com/ggml-org/llama.cpp/tree/master/tools/server | default bind 127.0.0.1, `--api-key` / `--api-key-file` (§2.2, §5.5) |
| Ollama documentation (FAQ: `OLLAMA_HOST`), https://github.com/ollama/ollama/blob/main/docs/faq.md | Ollama binds 127.0.0.1 by default and exposes through `OLLAMA_HOST` (§2.2) |
| Docker documentation, packet filtering and firewalls, https://docs.docker.com/engine/network/packet-filtering-firewalls/ (URL as recalled; verify) | published ports on 0.0.0.0, interaction with ufw/firewalld, `127.0.0.1:` in `-p` (§2.3) |
| Wiz Research, "Probllama" (Ollama path traversal), 2024; NVD https://nvd.nist.gov/vuln/detail/CVE-2024-37032 | CVE-2024-37032, fixed 0.1.34 (§3) |
| NCC Group, Ollama DNS rebinding, Apr 2024; NVD https://nvd.nist.gov/vuln/detail/CVE-2024-28224 | CVE-2024-28224, fixed 0.1.29 (§3, §4.2) |
| Cyera, "Bleeding Llama", May 2026; NVD https://nvd.nist.gov/vuln/detail/CVE-2026-7482 | CVE-2026-7482 memory disclosure, fixed 0.17.1 (§3) |
| Open WebUI security advisory for Direct Connections, 2025; NVD https://nvd.nist.gov/vuln/detail/CVE-2025-64496 | CVE-2025-64496, fixed 0.6.35 (§3) |
| Oligo Security, MCP Inspector, 2025; NVD https://nvd.nist.gov/vuln/detail/CVE-2025-49596 | CVE-2025-49596, fixed 0.14.1 (§3, §4) |
| NVIDIA security bulletin and Trend Micro, "NVIDIA AI Container Toolkit vulnerability fix", 2024, https://www.trendmicro.com/en/research/24/i/nvidia-ai-container-toolkit-vulnerability-fix.html; GitLab advisory for CVE-2024-0132 | CVE-2024-0132 TOCTOU escape, fixed 1.16.2 (§3) |
| Wiz Research, "NVIDIAScape", Jul 2025; NVD https://nvd.nist.gov/vuln/detail/CVE-2025-23266 | CVE-2025-23266, fixed 1.17.8 (§3) |
| Oligo Security, "ShadowRay" (2024) and "ShadowRay 2.0" (Nov 2025); NVD https://nvd.nist.gov/vuln/detail/CVE-2023-48022 | Ray job API without auth, CVE disputed by the vendor, no patch (§1, §3) |
| Sorensen and Khlaaf, Trail of Bits, "LeftoverLocals: Listening to LLM responses through leaked GPU local memory", Jan 2024, https://arxiv.org/abs/2401.16603; CERT/CC VU#446598, https://kb.cert.org/vuls/id/446598 | CVE-2023-4969, affected vendors, GPU memory isolation lesson (§3, §5.4) |
| Google Chrome team, Local Network Access, blog Jun 2025 (opt-in from Chrome 138), https://developer.chrome.com/blog/local-network-access (URL as recalled; verify) | browser-side prompt for private-network access (§4.3) |
| Caddy documentation, https://caddyserver.com/docs/ | `reverse_proxy`, `tls internal`, `request_body`, header matchers (§5.2); not executed in this session |

## Part 13 · Guardrails, red-teaming and evaluating defences

Lesson: [`13-GUARDRAILS-RED-TEAMING-AND-EVALUATING-DEFENCES.md`](13-GUARDRAILS-RED-TEAMING-AND-EVALUATING-DEFENCES.md)

| Source | What went into this part (section) |
| :-- | :-- |
| OWASP, Top 10 for LLM Applications 2025, LLM01 Prompt Injection, https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | mitigations in layers, no foolproof prevention (§1) |
| NIST, AI 100-2 E2025, Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations, https://csrc.nist.gov/pubs/ai/100/2/e2025/final | evaluation against adaptive adversaries (§1) |
| Meta, Llama Prompt Guard 2 (86M, 22M) model documentation, https://www.llama.com/docs/model-cards-and-prompt-formats/prompt-guard/ | sizes, binary benign/malicious labels, gated licence (§1, §6.3). The context-window size was NOT confirmed from Meta's page; the lesson tells the reader to check the model card |
| Meta, Llama Guard 3 and Llama Guard 4 (content-safety classifiers), https://www.llama.com/docs/model-cards-and-prompt-formats/ | what a content-safety model is for versus an injection detector (§1); no model-specific numbers used |
| Nasr, Carlini, Sitawarin, Schulhoff et al., "The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections", arXiv 2510.09023, Oct 2025, https://arxiv.org/abs/2510.09023 | 12 defences bypassed; gradient, RL, random-search and human-guided methods; humans succeeded where static baseline did not; recommendations (§4). The ">90% for most" figure comes from a secondary summary of the abstract: the lesson tells the reader to read per-defence numbers in the paper |
| Hackett, Birch, Trawicki, Suri, Garraghan, "Bypassing Prompt Injection and Jailbreak Detection in LLM Guardrails", arXiv 2504.11168, Apr 2025, https://arxiv.org/abs/2504.11168 | character injection and adversarial-ML evasion against six detectors (§4.1); exact per-detector numbers not checked |
| Robust Intelligence (now Cisco), bypass of Meta's Prompt-Guard-86M by spacing letters, 2024. URL not re-verified in this session | the character-spacing example (§4.1) |
| Wilson, E. B., "Probable inference, the law of succession, and statistical inference", JASA, 1927 (the score interval); formula implemented in the lab's `harness.wilson` | interval method (§3.2, §5.3); the upper-bound table is computed with it |
| NVIDIA, garak, https://github.com/NVIDIA/garak (pinned 0.17.1) | probes/detectors, `--target_type openai.OpenAICompatible`, `--generator_options`, `OPENAICOMPATIBLE_API_KEY` (§5.1, §6.5). Commands not executed in this session (no package-index access in the sandbox) |
| Microsoft, PyRIT, https://microsoft.github.io/PyRIT/1.1.0/ (pinned 1.1.0) | targets, converters, scorers; imports `PromptSendingAttack`, `OpenAIChatTarget`, `IN_MEMORY`, `initialize_pyrit_async` confirmed on the 1.1.0 landing page; other imports not confirmed (§5.1, §6.6). Script not executed |
| promptfoo, https://www.promptfoo.dev/docs/red-team/ (pinned 0.124.1) | plugins, strategies, custom Python provider, `PROMPTFOO_DISABLE_REDTEAM_REMOTE_GENERATION` (§5.1, §6.7). Config not executed |
| GitHub Docs, security hardening for GitHub Actions (self-hosted runners and forks), https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions (URL as recalled; verify) | self-hosted runners and pull requests from forks, pinning actions to SHAs (§6.9) |
| Part 14 of this course, section 10.6, mock-friendly case format | the `>>> CALL` plus natural-language carrier convention for gate cases (§6.9) |

## Part 14 · Detection, monitoring and incident response

Lesson: [`14-DETECTION-MONITORING-AND-INCIDENT-RESPONSE.md`](14-DETECTION-MONITORING-AND-INCIDENT-RESPONSE.md)

| Source | What went into this part (section) |
| :-- | :-- |
| *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile* (SP 800-61 Rev. 3), NIST, April 2025, https://csrc.nist.gov/pubs/sp/800/61/r3/final | the runbook's framing around the CSF 2.0 functions (§9) |
| *GenAI Incident Response Guide 1.0*, OWASP GenAI Security Project (CTI initiative), July 2025, https://genai.owasp.org/resource/genai-incident-response-guide-1-0/ | GenAI-specific response, blast radius of an AI incident (§9) |
| *Semantic conventions for generative AI systems* (status: Development), OpenTelemetry, 2024–2026, https://opentelemetry.io/docs/specs/semconv/gen-ai/ | trace attribute names; message content as opt-in attributes (§2) |
| *Canarytokens*, Thinkst Applied Research, https://canarytokens.org/ | the canary / honeytoken idea in classic infrastructure (§4) |
| *Rebuff: self-hardening prompt injection detector*, Protect AI, 2023, https://github.com/protectai/rebuff | the canary-word check in an open-source detector (§4.1) |
| Gakh, V., Bahsi, H., *Enhancing Security in LLM Applications: A Performance Evaluation of Early Detection Systems*, Tallinn University of Technology, June 2025, https://arxiv.org/abs/2506.19109 | default canary-word checks in Rebuff and Vigil caught none of the authors' prompt-leak attacks; placement as the cause (§4.1) |
| Abdelnabi, S., Fay, A., et al., *Get my drift? Catching LLM Task Drift with Activation Deltas* (first posted as "Are you still on track!?"), Microsoft and CISPA, arXiv June 2024 / SaTML 2025, https://arxiv.org/abs/2406.00799 ; code: https://github.com/microsoft/TaskTracker | activation-based task-drift detection for open-weight models; its limits under adaptive attack (§5) |
| Nasr, M., Carlini, N., et al., *The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections*, October 2025, https://arxiv.org/abs/2510.09023 | why prevention alone never reaches zero (§0) |
| *ChatGPT macOS Flaw Could've Enabled Long-Term Spyware via Memory Function* (on J. Rehberger's "SpAIware"), The Hacker News, September 2024, https://thehackernews.com/2024/09/chatgpt-macos-flaw-couldve-enabled-long.html | persistent memory injection; fix in ChatGPT macOS 1.2024.247; "purge memory" as an IR step (§9.2) |
| *EchoLeak: The First Real-World Zero-Click Prompt Injection Exploit in a Production LLM System*, 2025, https://arxiv.org/abs/2509.10540 ; *Zero-Click AI Vulnerability Exposes Microsoft 365 Copilot Data Without User Interaction*, The Hacker News, June 2025, https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html ; CVE-2025-32711, Microsoft MSRC, https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711 | zero-click exfiltration, CVSS 9.3, reported January 2025, server-side fix May 2025, disclosed June 2025 (§9.2) |
| Regulation (EU) 2016/679 (GDPR), Articles 33 and 34, European Union, 2016, https://eur-lex.europa.eu/eli/reg/2016/679/oj | breach notification to the authority (72 h) and to data subjects (§9) |
| Course 2, part 15 *Observability*, part 16 *Security (OWASP ASI)*, part 18 *Release and maintenance*, this repository, 2026, `../course_agentic_apps/` | traces, replay, kill switch, "sudden surge" memory signal, runbook format (§0, §6, §9) |

## Part 15 · Capstone: secure the lab end to end

Lesson: [`15-CAPSTONE.md`](15-CAPSTONE.md)

| Source | What went into this part (section) |
| :-- | :-- |
| Willison, S., *The lethal trifecta for AI agents: private data, untrusted content, and external communication*, 16 June 2025, https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | principle 2: break the trifecta per session (§1.1, §7) |
| *Agents Rule of Two: A Practical Approach to AI Agent Security*, Meta AI, 31 October 2025, https://ai.meta.com/blog/practical-ai-agent-security/ | at most two of: untrusted input, sensitive data/systems, state change or external communication (§1.1) |
| Debenedetti, E., et al., *Defeating Prompt Injections by Design* (CaMeL), Google DeepMind and ETH Zurich, March 2025, https://arxiv.org/abs/2503.18813 | principle 3: deterministic control outside the model (§1.1) |
| Beurer-Kellner, L., et al., *Design Patterns for Securing LLM Agents against Prompt Injections*, June 2025, https://arxiv.org/abs/2506.08837 | principle 3; architectural fixes in exercise 4 (§1.1, §9) |
| Nasr, M., Carlini, N., et al., *The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections*, October 2025 (USENIX Security 2026), https://arxiv.org/abs/2510.09023 | principle 4; >90% ASR against most of 12 defences; the adaptive round; human red-teaming (§1.1, §3.1, §9) |
| Wilson, E. B., *Probable Inference, the Law of Succession, and Statistical Inference*, Journal of the American Statistical Association 22(158), 1927, https://doi.org/10.1080/01621459.1927.10502953 | the interval used by the harness and `report.py`; reading the upper bound (§5) |
| CVE-2025-32711 (EchoLeak), Microsoft MSRC, 2025, https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711 | "reach" in the severity rubric: zero-click (§6) |
| Regulation (EU) 2024/1689 (AI Act), Article 50, European Union, 2024, https://eur-lex.europa.eu/eli/reg/2024/1689/oj | informing people that they interact with an AI system, applicable from 2 August 2026 (§7) |
| Regulation (EU) 2016/679 (GDPR), European Union, 2016, https://eur-lex.europa.eu/eli/reg/2016/679/oj | personal data of other users (§7) |
| Course 2, part 16 *Security (OWASP ASI)* §10 (ASI09, approval summaries built by code), this repository, 2026, `../course_agentic_apps/16-SECURITY-OWASP-ASI.md` | confirmations in §4 and review item 6 (§4, §7) |
| Parts 01–14 of this course | every layer of the defence-in-depth map and every configuration in the stack (§1, §2) |
