# Źródła — na czym stoi ten kurs

**Zebrane 28 października 2026.** Przy każdej pozycji jest napisane, **co z niej weszło do kursu i gdzie**.

> ⚠️ **Ta dziedzina zmienia się w miesiącach.** Nowe ataki, CVE i obrony pojawiają się co kilka tygodni,
> a narzędzia zmieniają składnię poleceń. Gdy część podaje liczbę (skuteczność ataku, liczbę wystawionych
> serwerów), to jest **czyjś pomiar na czyjejś konfiguracji** — powtórz go u siebie w laboratorium. CVE są
> podane z wersją, która je naprawiła: jeśli używasz starszej, najpierw zaktualizuj.
>
> Badania bezpieczeństwa są cytowane w celach obronnych: żeby wyjaśnić, jak działa atak, abyś umiał go
> rozpoznać, przetestować i zamknąć we własnych systemach.

---

## Część 01 · Krajobraz zagrożeń i modelowanie

Lesson: [`01-KRAJOBRAZ-ZAGROZEN-I-MODELOWANIE.md`](01-KRAJOBRAZ-ZAGROZEN-I-MODELOWANIE.md)

| Źródło | Co trafiło do tej części (sekcja) |
| :-- | :-- |
| *The lethal trifecta for AI agents: private data, untrusted content, and external communication*, Simon Willison, 2025, https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | §4 trzy nogi, „unikaj połączenia” jako jedyna niezawodna naprawa; kalkulator trójcy w LABORATORIUM |
| *Prompt injection attacks against GPT-3*, Simon Willison, 2022, https://simonwillison.net/2022/Sep/12/prompt-injection/ | §4 i §6 pochodzenie terminu (12 IX 2022), przejęcie bota na Twitterze |
| *Agents Rule of Two: A Practical Approach to AI Agent Security*, Meta AI, 2025, https://ai.meta.com/blog/practical-ai-agent-security/ | §4 Rule of Two (31 X 2025), szersza trzecia noga „zmiana stanu” |
| *The Confused Deputy (or why capabilities might have been invented)*, Norm Hardy, ACM SIGOPS Operating Systems Review, 1988, https://dl.acm.org/doi/10.1145/54289.871709 | §2.1 model jako zdezorientowany zastępca |
| *OWASP Top 10 for LLM Applications 2025*, OWASP GenAI Security Project, 2024, https://genai.owasp.org/llm-top-10/ | §5.1 tabela LLM01–LLM10, przypisanie do części kursu |
| *OWASP Reveals Updated 2025 Top 10 Risks for LLMs*, OWASP GenAI Security Project, 2024, https://genai.owasp.org/2024/11/17/owasp-reveals-2025-top-10-risks-for-llms-new-sponsorship-program/ | §5.1 data wydania (listopad 2024), nowe LLM07/LLM08 |
| *OWASP Top 10 for Agentic Applications*, OWASP GenAI Security Project, 2025, https://genai.owasp.org/ — omówione w kursie 2, część 16 (`../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md`) | §5.2 ASI01–ASI10 i które części idą głębiej |
| *MITRE ATLAS*, MITRE, na bieżąco, https://atlas.mitre.org/ (AML.T0051 https://atlas.mitre.org/techniques/AML.T0051, AML.T0054 https://atlas.mitre.org/techniques/AML.T0054, AML.CS0035 https://atlas.mitre.org/studies/AML.CS0035) | §5.3 taktyki/techniki/studia przypadków, przykładowe ID |
| *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations* (NIST AI 100-2 E2025), Vassilev i in., NIST, marzec 2025, https://csrc.nist.gov/pubs/ai/100/2/e2025/final | §5.4 taksonomia predykcyjne vs generatywne, cele, możliwości, poziomy wiedzy |
| *Threat Modeling Manifesto*, Braiterman, Shostack i in., 2020, https://www.threatmodelingmanifesto.org/ | §7 cztery pytania |
| *Threat Modeling Tool threats (STRIDE)*, Microsoft, https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats | §7.4 klasy STRIDE; STRIDE dla każdego elementu (pochodzenie: Kohnfelder i Garg, Microsoft, 1999) |
| *AI-powered Bing Chat spills its secrets via prompt injection attack*, Benj Edwards, Ars Technica, 2023, https://arstechnica.com/information-technology/2023/02/ai-powered-bing-chat-spills-its-secrets-via-prompt-injection-attack/ | §6 wyciek promptu Bing Chat „Sydney” (luty 2023) |
| *Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*, Greshake i in., 2023, https://arxiv.org/abs/2302.12173 | §6 pośredni prompt injection |
| *March 20 ChatGPT outage: Here's what happened*, OpenAI, 2023, https://openai.com/index/march-20-chatgpt-outage/ | §6 błąd redis-py; ok. 1,2% subskrybentów Plus w 9-godzinnym oknie (liczby OpenAI) |
| *Hacking Google Bard — From Prompt Injection to Data Exfiltration*, Johann Rehberger, 2023, https://embracethered.com/blog/posts/2023/google-bard-data-exfiltration/ | §6 eksfiltracja przez obrazki markdown (listopad 2023) |
| *Moffatt v. Air Canada*, 2024 BCCRT 149, BC Civil Resolution Tribunal, 2024, https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html | §2 i §6 wyjście chatbota jako zobowiązanie (LLM09) |
| *Data Scientists Targeted by Malicious Hugging Face ML Models with Silent Backdoor*, JFrog, 2024, https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/ | §6 ok. 100 złośliwych modeli (liczba JFrog) |
| *CVE-2024-34359* (SSTI Jinja2 w llama-cpp-python, naprawione w 0.2.72), NVD, 2024, https://nvd.nist.gov/vuln/detail/CVE-2024-34359 | §6 szablon czatu to kod |
| *Data Exfiltration from Slack AI via indirect prompt injection*, PromptArmor, 2024, https://promptarmor.com/resources/data-exfiltration-from-slack-ai-via-indirect-prompt-injection | §6 Slack AI (sierpień 2024) |
| *ChatGPT macOS Flaw Could've Enabled Long-Term Spyware via Memory Function*, The Hacker News, 2024, https://thehackernews.com/2024/09/chatgpt-macos-flaw-couldve-enabled-long.html | §6 SpAIware (Rehberger, wrzesień 2024), naprawione w 1.2024.247 |
| *GitHub MCP Exploited: Accessing private repositories via MCP*, Invariant Labs, 2025, https://invariantlabs.ai/blog/mcp-github-vulnerability | §6 „toxic agent flow” przez publiczne issue (maj 2025) |
| *EchoLeak: The First Real-World Zero-Click Prompt Injection Exploit in a Production LLM System*, 2025, https://arxiv.org/abs/2509.10540 · *CVE-2025-32711*, NVD, https://nvd.nist.gov/vuln/detail/CVE-2025-32711 | §6 EchoLeak (czerwiec 2025, CVSS 9,3) |
| *Compromised Amazon Q extension told AI to delete everything – and it shipped*, The Register, 2025, https://www.theregister.com/2025/07/24/amazon_q_ai_prompt/ | §6 Amazon Q Developer 1.84.0 / naprawa 1.85.0 (lipiec 2025) |
| Kurs 1, część 07 (`../kurs_lokalne_modele/07-SANDBOX-BEZPIECZENSTWO-MONITORING.md`) i kurs 2, część 16 (`../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md`), llm-education, 2026 | §1 kolejność obron, §7.5 „przed czym się nie bronimy”, §8 zgoda budowana z faktów |

## Część 02 · Laboratorium

Lesson: [`02-LABORATORIUM.md`](02-LABORATORIUM.md)

| Źródło | Co trafiło do tej części (sekcja) |
| :-- | :-- |
| *The lethal trifecta for AI agents: private data, untrusted content, and external communication* — Simon Willison, 16 VI 2025 — https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | Trzy składniki, które Sieve ma celowo; „usuń jedną nogę” (§0, §2) |
| *Probable inference, the law of succession, and statistical inference* — Edwin B. Wilson, Journal of the American Statistical Association 22(158):209–212, 1927 — https://doi.org/10.1080/01621459.1927.10502953 | Przedział Wilsona używany przez harness i tabela przedziałów (§5.3, `harness.wilson`) |
| *Interval Estimation for a Binomial Proportion* — L. D. Brown, T. T. Cai, A. DasGupta, Statistical Science 16(2):101–133, 2001 — https://doi.org/10.1214/ss/1009213286 | Dlaczego przedział Walda zawodzi przy małym n i proporcjach bliskich 0/1; zalecenie Wilsona (§5.3) |
| *If nothing goes wrong, is everything all right? Interpreting zero numerators* — J. A. Hanley, A. Lippman-Hand, JAMA 249(13):1743–1745, 1983 — https://jamanetwork.com/journals/jama/article-abstract/389714 | Reguła trzech dla 0 sukcesów w n próbach (§5.3) |
| *Best-of-N Jailbreaking* — J. Hughes, S. Price, A. Lynch i in., arXiv:2412.03556, grudzień 2024 (NeurIPS 2025) — https://arxiv.org/abs/2412.03556 | Wielokrotne losowanie zaburzonych promptów; ASR rośnie z N zgodnie z prawem potęgowym — arytmetyka atakującego (§5.4) |
| *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents* — E. Debenedetti i in. (ETH Zurich, Invariant Labs), NeurIPS 2024 Datasets & Benchmarks — https://arxiv.org/abs/2406.13352 | ASR jako standardowa miara dla agentów z narzędziami; użyteczność pod atakiem obok ASR (§5.1, §5.5); ogólny kształt celu z narzędziami i wstrzykniętą treścią |
| *InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents* — Q. Zhan, Z. Liang, Z. Ying, D. Kang, 2024 — https://arxiv.org/abs/2403.02691 | ASR dla pośrednich wstrzyknięć w agentach z narzędziami (§5.1) |
| *HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal* — M. Mazeika i in., 2024 — https://arxiv.org/abs/2402.04249 | ASR jako standardowa miara oceny jailbreaków (§5.1) |
| *Defeating Nondeterminism in LLM Inference* — Horace He i Thinking Machines Lab, wrzesień 2025 — https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ (streszczenie: https://simonwillison.net/2025/Sep/11/defeating-nondeterminism/) | Dlaczego temperatura 0 nie gwarantuje determinizmu w serwowanym wnioskowaniu: zmienny rozmiar wsadu (§5.2) |
| *Function Calling* (docs/function-calling.md) — ggml-org / llama.cpp — https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md | llama-server obsługuje wywołania narzędzi w stylu OpenAI po uruchomieniu z `--jinja`; nadpisywanie szablonu (§7, pułapki 1–2) |
| *llama.cpp HTTP server README* — ggml-org / llama.cpp — https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | Zgodne z OpenAI `/v1/chat/completions` i `/v1/models`, `--host`, `--port`, `--api-key`, wyjście rozumowania (§7, pułapka 9) |
| *Chat Completions API reference* — OpenAI — https://platform.openai.com/docs/api-reference/chat | Format wiadomości i `tool_calls`, którym mówi `llm.chat()` (§4.1) |
| *OpenAI rolls out imperfect fix for ChatGPT data leak flaw* — BleepingComputer, grudzień 2023 — https://www.bleepingcomputer.com/news/security/openai-rolls-out-imperfect-fix-for-chatgpt-data-leak-flaw/ | Zgłoszenie Johanna Rehbergera z kwietnia 2023 o eksfiltracji przez obrazki markdown w ChatGPT (§4.5) |
| *Posts tagged "exfiltration-attacks"* — Simon Willison, 2023–2025 — https://simonwillison.net/tags/exfiltration-attacks/ | Bieżąca lista zgłoszeń eksfiltracji przez obrazki markdown w prawdziwych produktach (§4.5) |

## Część 03 · Dlaczego modele da się atakować

Lesson: [`03-DLACZEGO-MODELE-DA-SIE-ATAKOWAC.md`](03-DLACZEGO-MODELE-DA-SIE-ATAKOWAC.md)

| Źródło | Co trafiło do tej części (sekcja) |
| :-- | :-- |
| Kurs 1, części 02 i 03 (`../kurs_lokalne_modele/02-WNETRZE-MODELU.md`, `../kurs_lokalne_modele/03-KONTROLA-I-NIEZAWODNOSC.md`), llm-education, 2026 | §1 wiadomości jako fikcja, `/apply-template`; struktura czytnika GGUF w L1; pułapka P25 (brak roli system) |
| *GGUF file format specification*, ggml-org, https://github.com/ggml-org/ggml/blob/master/docs/gguf.md | §2 i L1 typy wartości, `tokenizer.chat_template`, `tokenizer.ggml.token_type` |
| *tiktoken* README / `encode(disallowed_special=...)`, OpenAI, https://github.com/openai/tiktoken | §2 domyślnie bezpieczna obsługa tokenów specjalnych w tekście |
| Dokumentacja *Tokenizer* (`split_special_tokens`, domyślnie False), Hugging Face Transformers, https://huggingface.co/docs/transformers/main_classes/tokenizer | §2 tabela wartości domyślnych |
| *llama.cpp server README* (`/tokenize` `parse_special`, `with_pieces`; `/apply-template`), ggml-org, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md · PR #14783 „server: add parse_special option to /tokenize endpoint”, 2025, https://github.com/ggml-org/llama.cpp/pull/14783 | §2 tabela; LABORATORIUM L2 i L3 |
| *llama.cpp Jinja engine README* (oznaczanie wejścia przeciw wstrzykiwaniu tokenów specjalnych, wprowadzone w PR #18462), ggml-org, https://github.com/ggml-org/llama.cpp/blob/master/common/jinja/README.md | §2 „zależy od Twojej wersji”; przewidywanie w Eksperymencie 03-A |
| *Token Injection: Crashing LLM Inference With Special Tokens*, Ding, Black Hat Europe 2025, https://i.blackhat.com/BH-EU-25/eu-25-Ding-Token-Injection-Crashing-LLM-Inference-With-Special-Tokens-final.pdf | §2.1 tokeny specjalne jako problem dostępności |
| *The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions*, Wallace i in., OpenAI, 2024, https://arxiv.org/abs/2404.13208 | §4 system > user > narzędzie, raportowany przez nich wzrost odporności |
| *OpenAI Model Spec*, OpenAI, od 2024, https://model-spec.openai.com/ | §4 „chain of command” |
| *StruQ: Defending Against Prompt Injection with Structured Queries*, Chen, Piet, Sitawarin, Wagner, USENIX Security 2025, https://arxiv.org/abs/2402.06363 | §4 i §8 zarezerwowane ograniczniki + ich usuwanie z danych + dostrajanie |
| *SecAlign: Defending Against Prompt Injection with Preference Optimization*, Chen i in., ACM CCS 2025, https://arxiv.org/abs/2410.05451 | §4 wariant z optymalizacją preferencji; granice przy atakach optymalizacyjnych |
| *Control Illusion: The Failure of Instruction Hierarchies in Large Language Models*, Geng i in., 2025 (AAAI 2026), https://arxiv.org/abs/2502.15851 | §4 zmierzone granice; autorytet społeczny wygrywa z rolą; hipoteza Eksperymentu 03-B |
| *Lost in the Middle: How Language Models Use Long Contexts*, Liu i in., 2023, https://arxiv.org/abs/2307.03172 | §5 efekty pozycji |
| *Efficient Streaming Language Models with Attention Sinks*, Xiao i in., 2023, https://arxiv.org/abs/2309.17453 | §5 attention sinks |
| *Many-shot jailbreaking*, Anthropic, kwiecień 2024, https://www.anthropic.com/research/many-shot-jailbreaking | §5 efekt ilości |
| *Training language models to follow instructions with human feedback*, Ouyang i in., 2022, https://arxiv.org/abs/2203.02155 | §6 RLHF |
| *Constitutional AI: Harmlessness from AI Feedback*, Bai i in., Anthropic, 2022, https://arxiv.org/abs/2212.08073 | §6 dostrajanie preferencji |
| *Direct Preference Optimization*, Rafailov i in., 2023, https://arxiv.org/abs/2305.18290 | §6 DPO |
| *Jailbroken: How Does LLM Safety Training Fail?*, Wei, Haghtalab, Steinhardt, 2023, https://arxiv.org/abs/2307.02483 | §6 sprzeczne cele, niedopasowana generalizacja |
| *Safety Alignment Should Be Made More Than Just a Few Tokens Deep*, Qi i in., 2024, https://arxiv.org/abs/2406.05946 | §6 płytkie dopasowanie; przypadek `p03-text-prefix` |
| *Refusal in Language Models Is Mediated by a Single Direction*, Arditi i in., NeurIPS 2024, https://arxiv.org/abs/2406.11717 | §6 kierunek odmowy (tylko koncepcyjnie; 13 otwartych modeli do 72B) |
| *Towards Understanding Sycophancy in Language Models*, Sharma i in., Anthropic, 2023, https://arxiv.org/abs/2310.13548 | §7 służalczość w pięciu asystentach |
| *Sycophancy in GPT-4o: what happened and what we're doing about it*, OpenAI, kwiecień 2025, https://openai.com/index/sycophancy-in-gpt-4o/ | §7 wycofanie służalczej aktualizacji |
| *Prompt injection attacks against GPT-3*, Simon Willison, 2022, https://simonwillison.net/2022/Sep/12/prompt-injection/ · *You can't solve AI security problems with more AI*, Simon Willison, 2022, https://simonwillison.net/2022/Sep/17/prompt-injection-more-ai/ | §8 brak zapytania parametryzowanego; 99% to ocena niedostateczna |
| *The Dual LLM pattern for building AI assistants that can resist prompt injection*, Simon Willison, 2023, https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ | §8 architektura (budowana w części 07) |
| *Defeating Prompt Injections by Design* (CaMeL), Debenedetti i in., Google DeepMind, 2025, https://arxiv.org/abs/2503.18813 | §8 architektura |
| *Design Patterns for Securing LLM Agents against Prompt Injections*, Beurer-Kellner i in., 2025, https://arxiv.org/abs/2506.08837 | §8 architektura |

## Część 04 · Jailbreaki i alignment

Lesson: [`04-JAILBREAKI-I-ALIGNMENT.md`](04-JAILBREAKI-I-ALIGNMENT.md)

| Źródło | Co trafiło do tej części (sekcja) |
| :-- | :-- |
| „Prompt injection and jailbreaking are not the same thing”, Simon Willison, 2024, https://simonwillison.net/2024/Mar/5/prompt-injection-jailbreaking/ | §0 rozróżnienie jailbreak / injection |
| „Jailbroken: How Does LLM Safety Training Fail?”, Wei, Haghtalab, Steinhardt, 2023 (NeurIPS 2023), https://arxiv.org/abs/2307.02483 | §1.1 konkurujące cele i niedopasowana generalizacja; §2.4 base64; przypadek `p04-suppress` |
| „Safety Alignment Should Be Made More Than Just a Few Tokens Deep”, Qi i in., 2024 (ICLR 2025), https://arxiv.org/abs/2406.05946 | §1.2 płytki alignment; §2.5 dlaczego prefill działa; §4 |
| „Do Anything Now: Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models”, Shen i in., 2023 (CCS 2024), https://arxiv.org/abs/2308.03825 | §2.1 rodzina odgrywania ról / DAN; §3 oś czasu |
| „Scalable and Transferable Black-Box Jailbreaks for Language Models via Persona Modulation”, Shah i in., 2023, https://arxiv.org/abs/2311.03348 | §2.1 zautomatyzowana modulacja persony |
| „Mitigating Skeleton Key, a new type of generative AI jailbreak technique”, blog Microsoft Security, 2024, https://www.microsoft.com/en-us/security/blog/2024/06/26/mitigating-skeleton-key-a-new-type-of-generative-ai-jailbreak-technique/ | §2.1 rodzina „aktualizacji wytycznych”; §3; przypadek `p04-guidelines` (tylko niegroźny kształt) |
| „Many-shot jailbreaking”, Anil i in., Anthropic, 2024 (NeurIPS 2024), https://www.anthropic.com/research/many-shot-jailbreaking | §2.2 prawo potęgowe, 5 vs 256 przykładów, liczba 61% → 2% dla łagodzenia; §7.2 generator many-shot |
| „Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack”, Russinovich, Salem, Eldan (Microsoft), 2024 (USENIX Security 2025), https://arxiv.org/abs/2404.01833 | §2.3 eskalacja wieloturowa; §7.3 wariant crescendo w `p04_multiturn` |
| „Low-Resource Languages Jailbreak GPT-4”, Yong, Menghini, Bach, 2023, https://arxiv.org/abs/2310.02446 | §2.4 rodzina językowa; przypadki `p04-lang-*` |
| „Best-of-N Jailbreaking”, Hughes i in., 2024 (NeurIPS 2025), https://arxiv.org/abs/2412.03556 | §2.4 losowe zaburzenia, 89% / 78% przy 10 000 próbek; §6 limity zapytań |
| „Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks”, Andriushchenko, Croce, Flammarion, 2024, https://arxiv.org/abs/2404.02151 | §2.5 prefill jako droga ataku |
| README serwera llama.cpp (`--prefill-assistant` / `--no-prefill-assistant`, domyślnie włączone), ggml-org, 2025–2026, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | §2.5 prefill na własnym serwerze; §7.3 |
| „Universal and Transferable Adversarial Attacks on Aligned Language Models” (GCG), Zou, Wang, Carlini, Nasr, Kolter, Fredrikson, 2023, https://arxiv.org/abs/2307.15043 | §2.6 GCG i przenoszalność; §3 |
| „AutoDAN: Generating Stealthy Jailbreak Prompts on Aligned Large Language Models”, Liu, Xu, Chen, Xiao, 2023 (ICLR 2024), https://arxiv.org/abs/2310.04451 | §2.6 przeszukiwanie genetyczne czytelnych promptów |
| „Jailbreaking Black Box Large Language Models in Twenty Queries” (PAIR), Chao i in., 2023, https://arxiv.org/abs/2310.08419 | §2.6 pętla z LLM-atakującym; §7.5 projekt PAIR-lite |
| „Tree of Attacks: Jailbreaking Black-Box LLMs Automatically” (TAP), Mehrotra i in., 2023 (NeurIPS 2024), https://arxiv.org/abs/2312.02119 | §2.6 przeszukiwanie drzewa z przycinaniem |
| „Baseline Defenses for Adversarial Attacks Against Aligned Language Models”, Jain i in., 2023, https://arxiv.org/abs/2309.00614 | §2.6 filtr perpleksji i jego granice; §6 |
| „Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend To!”, Qi i in., 2023 (ICLR 2024), https://arxiv.org/abs/2310.03693 | §4 10 przykładów, < 0,20 USD; niewinny fine-tuning też osłabia bezpieczeństwo |
| „Refusal in Language Models Is Mediated by a Single Direction”, Arditi i in., 2024 (NeurIPS 2024), https://arxiv.org/abs/2406.11717 | §4 kierunek odmowy w 13 otwartych modelach, edycja rzędu jeden (opisana wyłącznie koncepcyjnie); §3 |
| „Constitutional Classifiers: Defending against universal jailbreaks”, Anthropic, 2025, https://www.anthropic.com/research/constitutional-classifiers | §6 86% → 4,4%, +0,38 pp odmów, +23,7% obliczeń (liczby Anthropic); §3 |
| „Next-generation Constitutional Classifiers”, Anthropic, 9 stycznia 2026, https://www.anthropic.com/research/next-generation-constitutional-classifiers | §6 jeden uniwersalny jailbreak znaleziony na pierwszym systemie; następna generacja ~1% obliczeń |
| „You can't solve AI security problems with more AI”, Simon Willison, 2022, https://simonwillison.net/2022/Sep/17/prompt-injection-more-ai/ | §6 pułapka „więcej AI jako obrona”; §7.4 projekt sędziego |
| „A customer managed to get the DPD AI chatbot to swear at them, and it wasn't even that hard”, TechRadar, styczeń 2024, https://www.techradar.com/pro/a-customer-managed-to-get-the-dpd-ai-chatbot-to-swear-at-them-and-it-wasnt-even-that-hard | §3 incydent z chatbotem firmy kurierskiej (oświadczenie firmy o aktualizacji systemu) |
| Kurs 1 część 07 i kurs 2 część 16 z tego repozytorium (`../kurs_lokalne_modele/07-SANDBOX-BEZPIECZENSTWO-MONITORING.md`, `../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md`), 2026 | linki w sekcji końcowej; kontekst ASI01 |

## Część 05 · Bezpośredni prompt injection i wycieki promptu

Lesson: [`05-BEZPOSREDNI-PROMPT-INJECTION-I-WYCIEKI-PROMPTU.md`](05-BEZPOSREDNI-PROMPT-INJECTION-I-WYCIEKI-PROMPTU.md)

| Źródło | Co trafiło do tej części (sekcja) |
| :-- | :-- |
| „Prompt injection attacks against GPT-3”, Simon Willison, 2022, https://simonwillison.net/2022/Sep/12/prompt-injection/ | §1 historia: termin i przykłady „ignore the above directions” Rileya Goodside'a; §4 |
| „Ignore Previous Prompt: Attack Techniques For Language Models”, Perez, Ribeiro, 2022 (NeurIPS ML Safety Workshop), https://arxiv.org/abs/2211.09527 | §1 nazwy *goal hijacking* i *prompt leaking*; §4 |
| OWASP Top 10 for LLM Applications 2025 (LLM01 Prompt Injection, LLM06 Excessive Agency), OWASP GenAI Security Project, 2024, https://genai.owasp.org/llm-top-10/ | §1 tabela mapy; §4 |
| „LLM07:2025 System Prompt Leakage”, OWASP GenAI Security Project, 2024, https://genai.owasp.org/llmrisk/llm072025-system-prompt-leakage/ | §1 „nie sekret, nie mechanizm bezpieczeństwa”; §3.4; §4 |
| „The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions”, Wallace i in. (OpenAI), 2024, https://arxiv.org/abs/2404.13208 | §2.1 priorytet ról jako wyuczona preferencja; §5 obrony badawcze |
| „GM dealer chat bot agrees to sell 2024 Chevy Tahoe for $1”, GM Authority, grudzień 2023, https://gmauthority.com/blog/2023/12/gm-dealer-chat-bot-agrees-to-sell-2024-chevy-tahoe-for-1/ | §2.3 przypadek dealera: brakująca możliwość jako obrona; §4 |
| „AI-powered Bing Chat spills its secrets via prompt injection attack”, Ars Technica (B. Edwards), 10 lutego 2023, zarejestrowane jako raport 2666 w AI Incident Database, https://incidentdatabase.ai/reports/2666 | §3.3 ujawnienie promptu Bing Chat / „Sydney”; §4 |
| OECD AI Incidents Monitor, „Bing Chatbot Exposes Confidential Instructions After Prompt Injection Attack”, 2023, https://oecd.ai/en/incidents/2023-02-10-4440 | §3.3 data i potwierdzenie Microsoftu |
| „Effective Prompt Extraction from Language Models” (v1: „Prompts Should Not Be Seen as Secrets”), Zhang, Carlini, Ippolito, 2023–2024, https://arxiv.org/abs/2307.06865 | §3.1 argument; §3.3 11 modeli, filtry wyjścia niewystarczające, ataki w stylu tłumaczenia; §4 |
| „Assessing Prompt Injection Risks in 200+ Custom GPTs”, Yu i in., 2023, https://arxiv.org/abs/2311.11538 | §3.3 90/96 i 120/120 wydobytych promptów systemowych (ich tabela); prompty obronne nieskuteczne |
| Gandalf, Lakera, 2023, https://gandalf.lakera.ai/ | §3.3 dowód z gry, że warstwowe sprawdzenia wejścia/wyjścia są omijane |
| „Tensor Trust: Interpretable Prompt Injection Attacks from an Online Game”, Toyer i in., 2023 (ICLR 2024), https://arxiv.org/abs/2311.01011 | §3.3 ataki porywania i wydobywania zebrane od tłumu |
| Noty wydań „System prompts”, dokumentacja Anthropic, od sierpnia 2024, https://docs.anthropic.com/en/release-notes/system-prompts | §3.3 dostawca publikujący swoje prompty; §4 |
| Rebuff (wykrywanie wycieku przez słowo-kanarek), Protect AI, 2023, https://github.com/protectai/rebuff | §5 D2 słowo-kanarek; §6.2 |
| „StruQ: Defending Against Prompt Injection with Structured Queries”, Chen, Piet, Sitawarin, Wagner, 2024, https://arxiv.org/abs/2402.06363 | §5 obrony badawcze |
| „SecAlign: Defending Against Prompt Injection with Preference Optimization”, Chen i in., 2024–2025, https://arxiv.org/abs/2410.05451 | §5 obrony badawcze |
| „Meta SecAlign: A Secure Foundation LLM Against Prompt Injection Attacks”, Chen, Zharmagambetov, Wagner, Guo, 2025, https://arxiv.org/abs/2507.02735 | §5 otwarte modele z obroną przed injection na poziomie modelu |
| „A Critical Evaluation of Defenses against Prompt Injection Attacks”, 2025, https://arxiv.org/abs/2505.18333 | §5 stałe prompty atakujące vs ataki adaptacyjne |
| „Jailbroken” (Wei i in., 2023) i „Safety Alignment Should Be Made More Than Just a Few Tokens Deep” (Qi i in., 2024) — pełne wpisy w źródłach części 04 | §2.2 torowanie dopełnienia; §3.1 „nigdy nie ujawniaj” jako konkurująca preferencja |
| Kurs 2 część 16 z tego repozytorium (`../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md`), 2026 | §1 ASI01 porwanie celu; linki końcowe |

## Część 06 · Pośredni prompt injection i zatruwanie RAG

Lesson: [`06-POSREDNI-PROMPT-INJECTION-I-ZATRUWANIE-RAG.md`](06-POSREDNI-PROMPT-INJECTION-I-ZATRUWANIE-RAG.md)

| Źródło | Co weszło do tej części (rozdział) |
| :-- | :-- |
| Greshake, Abdelnabi, Mishra, Endres, Holz, Fritz, „Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection”, arXiv 2302.12173, lut 2023, https://arxiv.org/abs/2302.12173 | termin, taksonomia dostarczania i cele (§1.2, §4) |
| Hines i in. (Microsoft), „Defending Against Indirect Prompt Injection Attacks With Spotlighting”, arXiv 2403.14720, mar 2024, https://arxiv.org/abs/2403.14720 | delimiting / datamarking / encoding; raportowany spadek ASR z >50% do <2% na modelach rodziny GPT (§5.2, `Spotlight`) |
| Zou, Geng, Wang, Jia, „PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models”, USENIX Security 2025, arXiv 2402.07867, https://www.usenix.org/conference/usenixsecurity25/presentation/zou | warunki wyszukania i generowania; ~90% ASR przy 5 tekstach na pytanie docelowe (§3.1, §4) |
| Nasr i in., „The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections”, arXiv 2510.09023, paź 2025, https://arxiv.org/abs/2510.09023 | detektory i napastnicy adaptacyjni: obejście 12 obron (§5.3, ostrzeżenie w §7) |
| Wallace i in. (OpenAI), „The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions”, arXiv 2404.13208, kwi 2024, https://arxiv.org/abs/2404.13208 | pomoc z treningu (§5.5) |
| PromptArmor, „Data Exfiltration from Slack AI via indirect prompt injection”, sie 2024, https://promptarmor.substack.com/p/data-exfiltration-from-slack-ai-via | tabela przypadków z praktyki (§4) |
| Simon Willison, „Hacking Google Bard - From Prompt Injection to Data Exfiltration” (omówienie badań J. Rehbergera), 4 lis 2023, https://simonwillison.net/2023/Nov/4/hacking-google-bard-from-prompt-injection-to-data-exfiltration/ | tabela przypadków (§4); daty zgłoszenia/naprawy z relacji wtórnych |
| The Hacker News, „Microsoft Fixes ASCII Smuggling Flaw”, sie 2024, https://thehackernews.com/2024/08/microsoft-fixes-ascii-smuggling-flaw.html | znaki tag Unicode w Copilot (§2, §4) |
| Reddy i in., „EchoLeak: The First Real-World Zero-Click Prompt Injection Exploit in a Production LLM System”, arXiv 2509.10540, 2025, https://arxiv.org/abs/2509.10540 (CVE-2025-32711) | tabela przypadków (§4); szczegóły w części 07 |

## Część 07 · Agenci, narzędzia i eksfiltracja

Lesson: [`07-AGENCI-NARZEDZIA-I-EKSFILTRACJA.md`](07-AGENCI-NARZEDZIA-I-EKSFILTRACJA.md)

| Źródło | Co weszło do tej części (rozdział) |
| :-- | :-- |
| OWASP Top 10 for LLM Applications 2025, LLM06 Excessive Agency, https://genai.owasp.org/llmrisk/llm062025-excessive-agency/ | trzy przyczyny źródłowe: funkcje, uprawnienia, autonomia (§1.1) |
| Norm Hardy, „The Confused Deputy (or why capabilities might have been invented)”, ACM SIGOPS Operating Systems Review 22(4), 1988, https://dl.acm.org/doi/10.1145/54289.871709 | confused deputy i lekarstwo przez zdolności (§1.2) |
| Simon Willison, „The lethal trifecta for AI agents”, 16 cze 2025, https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | śmiertelna trójka (§1.3) |
| Meta AI, „Agents Rule of Two”, 31 paź 2025, as discussed in Simon Willison, „New prompt injection papers: Agents Rule of Two and The Attacker Moves Second”, 2 lis 2025, https://simonwillison.net/2025/nov/2/new-prompt-injection-papers | reguła dwóch (§1.3) |
| Simon Willison, „The Dual LLM pattern for building AI assistants that can resist prompt injection”, kwi 2023, https://simonwillison.net/2023/Apr/25/dual-llm-pattern/ | idea dual-LLM (§5.2) |
| Beurer-Kellner et al., „Design Patterns for Securing LLM Agents against Prompt Injections”, arXiv 2506.08837, cze 2025, https://arxiv.org/abs/2506.08837 | sześć wzorców i wspólna zasada (§5.2) |
| Debenedetti et al., „Defeating Prompt Injections by Design” (CaMeL), arXiv 2503.18813, mar 2025 (v2 cze 2025), https://arxiv.org/abs/2503.18813 | architektura, 77% vs 84% w AgentDojo (liczby autorów), ograniczenia (§7); `camel_lite` to nasze uproszczenie |
| Debenedetti et al., „AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents”, NeurIPS 2024, arXiv 2406.13352, https://arxiv.org/abs/2406.13352 | benchmark stojący za liczbami CaMeL (§7.1) |
| Reddy et al., „EchoLeak: The First Real-World Zero-Click Prompt Injection Exploit in a Production LLM System”, arXiv 2509.10540, 2025, https://arxiv.org/abs/2509.10540 (CVE-2025-32711, CVSS 9,3 wg Microsoft) | łańcuch EchoLeak (§4) |
| Simon Willison, „Hacking Google Bard - From Prompt Injection to Data Exfiltration”, 4 lis 2023, https://simonwillison.net/2023/Nov/4/hacking-google-bard-from-prompt-injection-to-data-exfiltration/ | przypadek Barda, CSP i kolektor na allowliście (§4) |
| PromptArmor, „Data Exfiltration from Slack AI via indirect prompt injection”, sie 2024, https://promptarmor.substack.com/p/data-exfiltration-from-slack-ai-via | eksfiltracja linkiem w Slack AI (§4) |
| The Hacker News, „Microsoft Fixes ASCII Smuggling Flaw”, sie 2024, https://thehackernews.com/2024/08/microsoft-fixes-ascii-smuggling-flaw.html | ASCII smuggling w Copilot (§4) |
| Nasr et al., „The Attacker Moves Second”, arXiv 2510.09023, paź 2025, https://arxiv.org/abs/2510.09023 | dlaczego statyczne zera to nie bezpieczeństwo (ostrzeżenie §6.3) |

## Część 08 · MCP, skille, pamięć i wiele agentów

Lesson: [`08-MCP-SKILLE-PAMIEC-I-WIELE-AGENTOW.md`](08-MCP-SKILLE-PAMIEC-I-WIELE-AGENTOW.md)

| Źródło | Co weszło do tej części (sekcja) |
| :-- | :-- |
| Model Context Protocol, *Specification 2026-07-28*, przegląd „Security and Trust & Safety”, 2026, https://modelcontextprotocol.io/specification/2026-07-28 | opisy/adnotacje narzędzi niezaufane, chyba że z zaufanego serwera; zgoda; MCP nie egzekwuje tego na poziomie protokołu (§2.8) |
| Model Context Protocol, *Security Best Practices* (spec. 2026-07-28), 2026, https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices | confused deputy, token passthrough, SSRF, przejęcie uchwytu stanu, kompromitacja lokalnego serwera, minimalizacja zakresów (§2.6, §2.7) |
| NSA AI Security Center, *Model Context Protocol (MCP): Security Design Considerations for AI-Driven Automation* (CSI), 20 V 2026, https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf | adopcja wyprzedza model bezpieczeństwa; piaskownica, walidacja, logi, inwentaryzacja (§2.8, §6) |
| Invariant Labs, *MCP Security Notification: Tool Poisoning Attacks*, 1 IV 2025, https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks | zatruwanie narzędzi, rug pull, shadowing (§2.2–2.4, §6) |
| Invariant Labs, *GitHub MCP Exploited: Accessing private repositories via MCP*, 26 V 2025, https://invariantlabs.ai/blog/mcp-github-vulnerability | toksyczny przepływ z uczciwym serwerem (§2.5, §6) |
| Oligo Security / NVD, CVE-2025-49596 (MCP Inspector < 0.14.1), VI 2025, https://nvd.nist.gov/vuln/detail/CVE-2025-49596 | lokalne narzędzie deweloperskie osiągalne z przeglądarki; wersja z poprawką (§2.6) |
| JFrog, CVE-2025-6514 w mcp-remote (poprawione 0.1.16), 9 VII 2025, https://jfrog.com/blog/2025-6514-critical-mcp-remote-rce-vulnerability/ | wstrzyknięcie poleceń przez URL autoryzacji (§2.6) |
| Koi Security przez The Hacker News, *First Malicious MCP Server Found Stealing Emails* (postmark-mcp 1.0.16), IX 2025, https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html | złośliwy pakiet MCP w realu (§2.6, §6) |
| Koi Security przez eSecurity Planet, *Hundreds of Malicious Skills Found in OpenClaw's ClawHub* (ClawHavoc), II 2026, https://www.esecurityplanet.com/threats/hundreds-of-malicious-skills-found-in-openclaws-clawhub/ | 341 złośliwych z 2857 skilli (§3, §6) |
| Snyk, *ToxicSkills: malicious AI agent skills on ClawHub*, II 2026, https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub | 76 potwierdzonych złośliwych z 3984 skilli (§3, §6) |
| Johann Rehberger przez The Hacker News, *ChatGPT macOS flaw could've enabled long-term spyware via memory* (SpAIware), IX 2024, https://thehackernews.com/2024/09/chatgpt-macos-flaw-couldve-enabled-long.html | trwałość w pamięci, poprawka w 1.2024.247 (§4.2, §6) |
| Johann Rehberger przez InfoQ, *Gemini long-term memory attack* (opóźnione wywołanie narzędzia), II 2025, https://www.infoq.com/news/2025/02/gemini-long-term-memory-attack/ | opóźnione wywołanie narzędzia (§4.2, §6) |
| Z. Chen, Z. Xiang, C. Xiao, D. Song, B. Li, *AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases*, NeurIPS 2024, https://arxiv.org/abs/2407.12784 | zatruwanie pamięci kluczowane wyzwalaczem (§4.2) |
| Dong i in., *Memory Injection Attacks on LLM Agents via Query-Only Interaction* (MINJA), 2025, https://arxiv.org/abs/2503.03704 | wstrzyknięcie do pamięci samymi zapytaniami (§4.2) |
| Lee, Tiwari, *Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems*, X 2024, https://arxiv.org/abs/2410.07283 | samopowielające się wstrzyknięcie, LLM tagging (§5, §6) |
| Triedman, Jha, Shmatikov, *Multi-Agent Systems Execute Arbitrary Malicious Code*, III 2025 (v2 IX 2025, COLM 2025), https://arxiv.org/abs/2503.12188 | przejęcie przepływu sterowania MAS, 58–90% (v2, GPT-4o) (§5, §6) |
| AppOmni, *AI agent-to-agent discovery prompt injection* (ServiceNow Now Assist), XI 2025, https://appomni.com/ao-labs/ai-agent-to-agent-discovery-prompt-injection/ | wstrzyknięcie drugiego rzędu przez odkrywanie agentów (§5, §6) |
| OWASP GenAI Security Project, *Top 10 for Agentic Applications* (ASI04, ASI06, ASI07), XII 2025, https://genai.owasp.org/ | ramy; zob. kurs 2 część 16 (§0) |
| Simon Willison, *The lethal trifecta for AI agents*, VI 2025, https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | triada w przypadku GitHuba (§2.5) |
| llm-education kurs 2, części 5, 6, 9, 13, 16 (to repozytorium) | kwarantanna pamięci, skille, MCP, floty, mapa ASI (linki w całej części) |

## Część 09 · Obsługa wyjścia, kod i zasoby

Lesson: [`09-OBSLUGA-WYJSCIA-KOD-I-ZASOBY.md`](09-OBSLUGA-WYJSCIA-KOD-I-ZASOBY.md)

| Źródło | Co weszło do tej części (sekcja) |
| :-- | :-- |
| OWASP GenAI Security Project, *LLM05:2025 Improper Output Handling*, 2025, https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/ | ramy obsługi wyjścia (§0, §1) |
| OWASP GenAI Security Project, *LLM10:2025 Unbounded Consumption*, 2025, https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/ | ramy ryzyk zużycia, denial of wallet (§0, §6) |
| NVD / komunikat GitHub, CVE-2025-46719, stored XSS w renderowaniu markdownu Open WebUI (poprawione 0.6.6), 2025, https://nvd.nist.gov/vuln/detail/CVE-2025-46719 | XSS w samodzielnie hostowanym UI czatu (§2.2, §7) |
| The Hacker News, *Researchers Uncover Prompt Injection Vulnerabilities in DeepSeek and Claude AI* (Rehberger: XSS w DeepSeek → przejęcie konta; Terminal DiLLMa), XII 2024, https://thehackernews.com/2024/12/researchers-uncover-prompt-injection.html | wstrzyknięcie promptu do XSS; sekwencje ANSI w terminalach (§2.2, §3.4, §7) |
| Pedro, Castro, Carreira, Santos, *From Prompt Injections to SQL Injection Attacks: How Protected is Your LLM-Integrated Web Application?*, arXiv 2023 / ICSE 2025, https://arxiv.org/abs/2308.01990 | ataki prompt-to-SQL (§3.1, §7) |
| JFrog, *Critical RCE Vulnerability in mcp-remote: CVE-2025-6514*, 9 VII 2025, https://jfrog.com/blog/2025-6514-critical-mcp-remote-rce-vulnerability/ | URL do powłoki; poprawione 0.1.16 (§3.2, §7) |
| Model Context Protocol, *Security Best Practices* (spec. 2026-07-28), „OAuth Authorization URL Validation”, 2026, https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices | NIE WOLNO otwierać URL-i przez powłokę; lista dozwolonych schematów; CSP (§2.3, §3.2) |
| Baza komunikatów GitLab, CVE-2023-39662 (llama-index, poprawione 0.9.14), https://advisories.gitlab.com/pkg/pypi/llama-index/CVE-2023-39662/ | exec wyjścia modelu w PandasQueryEngine (§4.2, §7) |
| Baza komunikatów GitLab, CVE-2024-3098 (llama-index-core, poprawione 0.10.24), https://advisories.gitlab.com/pkg/pypi/llama-index-core/CVE-2024-3098/ | obejście poprzedniej poprawki (§4.2, §7) |
| Spracklen, Wijewickrama, Sakib, Maiti, Viswanath, Jadliwala, *We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs*, USENIX Security 2025, https://arxiv.org/abs/2406.10279 | 576 000 próbek, 16 modeli, 5,2% / 21,7%, 205 474 nazwy (§5, §7) |
| Kumar i in., *OverThink: Slowdown Attacks on Reasoning LLMs*, 2025, https://arxiv.org/abs/2502.02542 | ataki spowalniające przez tokeny rozumowania (§6.2, §7) |
| Shumailov, Zhao, Bates, Papernot, Mullins, Anderson, *Sponge Examples: Energy-Latency Attacks on Neural Networks*, IEEE EuroS&P 2021, https://arxiv.org/abs/2006.03463 | wejścia skrojone pod koszt (§6.2, §7) |
| ggml-org, *README serwera llama.cpp* (flagi `--api-key`, `-n`, `-c`, `-np`, `-to`, `--metrics`; `n_predict`, `t_max_predict_ms`), sprawdzone X 2026, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | pokrętła serwera i wartości domyślne (§6.3) |
| Dokumentacja Pythona, `sqlite3` (`set_authorizer`, `set_progress_handler`, URI `mode=ro`), https://docs.python.org/3/library/sqlite3.html | wykonawca SQL z minimalnymi uprawnieniami (§3.1, §9.3) |
| llm-education kurs 1 część 07 i kurs 2 części 10, 16 (to repozytorium) | piaskownica, ruch wychodzący, ASI05/ASI09 (§4.3, linki) |

## Część 10 · Łańcuch dostaw modeli

Lesson: [`10-LANCUCH-DOSTAW-MODELI.md`](10-LANCUCH-DOSTAW-MODELI.md)

| Źródło | Co z niego weszło do tej części (sekcja) |
| :-- | :-- |
| *pickle — Python object serialization* (ramka ostrzeżenia), Python Software Foundation, aktualna dokumentacja, https://docs.python.org/3/library/pickle.html | pickle jako maszyna stosowa; „nigdy nie odczytuj niezaufanego pickle”; `__reduce__` (§2.1, §10.1) |
| *pickletools — Tools for pickle developers*, Python Software Foundation, aktualna dokumentacja, https://docs.python.org/3/library/pickletools.html | `genops` jako dekoder opkodów bez wykonywania, podstawa skanera (§10.2) |
| Dokumentacja *torch.load* (`weights_only`), PyTorch, aktualna, https://pytorch.org/docs/stable/generated/torch.load.html | ograniczony unpickler; zmiana domyślnej wartości w PyTorch 2.6 (§2.2) |
| CVE-2025-32434, *PyTorch: torch.load with weights_only=True leads to remote code execution*, NVD, 2025, https://nvd.nist.gov/vuln/detail/CVE-2025-32434 | podatne ≤ 2.5.1, poprawione w 2.6.0; klasa błędu (§2.2, §9) |
| *Data Scientists Targeted by Malicious Hugging Face ML Models with Silent Backdoor*, JFrog, lut 2024, https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/ | ~100 modeli uruchamiających kod przy wczytaniu (ich liczenie) (§2.3, §9) |
| *Malicious ML models discovered on Hugging Face platform* (nullifAI), ReversingLabs, lut 2025, https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face | uszkodzony pickle w 7z omijający picklescan (§2.3, §9, §10.3) |
| CVE-2025-10155 / CVE-2025-10156 / CVE-2025-10157 (picklescan), OSV, 2025, https://osv.dev/vulnerability/CVE-2025-10155 | obejścia przez rozszerzenie i import przez podmoduł, poprawione w 0.0.31 (§2.3, §9) |
| *4M Models Scanned: Protect AI + Hugging Face 6 Months In*, Hugging Face / Protect AI, 2025, https://huggingface.co/blog/pai-6-month | partnerstwo od paź 2024; 352 000 zgłoszeń w 51 700 modelach (ich liczenie) (§2.3) |
| *safetensors*, Hugging Face, repozytorium i opis formatu, https://github.com/huggingface/safetensors | układ nagłówka, limit 100 MB, brak ścieżki do kodu (§3) |
| Specyfikacja *GGUF*, ggml-org, https://github.com/ggml-org/ggml/blob/master/docs/gguf.md | układ nagłówka, typy wartości, wyrównanie, opisy tensorów (§4, §10.4) |
| TALOS-2024-1916 / CVE-2024-23605 (oraz TALOS-2024-1915 / CVE-2024-21836), Cisco Talos, lut 2024, https://www.talosintelligence.com/vulnerability_reports/TALOS-2024-1916 | przepełnienia sterty `n_kv` / `n_tensors` w GGUF, poprawka 29 I 2024; „sprawdzaj liczniki przed alokacją” (§4, §9) |
| CVE-2024-21836, NVD, 2024, https://nvd.nist.gov/vuln/detail/CVE-2024-21836 | ocena, współzgłoszenie Databricks (§4) |
| *Llama Drama: Critical Vulnerability CVE-2024-34359 Threatening Your Software Supply Chain*, Checkmarx, maj 2024, https://checkmarx.com/blog/llama-drama-critical-vulnerability-cve-2024-34359-threatening-your-software-supply-chain/ | SSTI w Jinja2 w llama-cpp-python, 0.2.30–0.2.71, poprawione w 0.2.72 (§5.1, §9) |
| CVE-2024-34359, NVD, 2024, https://nvd.nist.gov/vuln/detail/CVE-2024-34359 | biuletyn i odnośnik do poprawki (§5.1) |
| README *llama-server* (`--jinja`, `--chat-template-file`), ggml-org/llama.cpp, aktualne, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | używanie własnego przypiętego szablonu (§5.3, §10.5) |
| *Customizing models* (`trust_remote_code`), dokumentacja Hugging Face Transformers, https://huggingface.co/docs/transformers/custom_models | co wykonuje flaga; przypinanie rewizji (§6) |
| Raport o incydencie *PoisonGPT* (Mithril Security, lip 2023), AI Incident Database, https://incidentdatabase.ai/reports/3206/ | GPT-J edytowany ROME pod podobną nazwą organizacji (§7, §8.1, §9) |
| Hubinger i in., *Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training*, Anthropic, sty 2024, https://arxiv.org/abs/2401.05566 | backdoory przetrwają SFT/RL/trening adwersarialny (§7, §9) |
| Egashira, Vero, Staab, He, Vechev, *Exploiting LLM Quantization*, NeurIPS 2024, https://arxiv.org/abs/2405.18137 | niewinny w pełnej precyzji, złośliwy po kwantyzacji (§7) |
| Egashira, Staab, Vero, He, Vechev, *Mind the Gap: A Practical Attack on GGUF Quantization*, ICML 2025, https://arxiv.org/abs/2505.23786 | to samo dla k-kwantów GGUF (§7, §9) |
| *A small number of samples can poison LLMs of any size*, Anthropic z UK AI Security Institute i Alan Turing Institute, paź 2025, https://www.anthropic.com/research/small-samples-poison | ~250 dokumentów, liczy się liczba bezwzględna (§7, §9) |
| *Model Namespace Reuse: An AI Supply-Chain Attack Exploiting Model Name Trust*, Palo Alto Networks Unit 42, 2025, https://unit42.paloaltonetworks.com/model-namespace-reuse/ | ponownie zarejestrowane przestrzenie nazw; przypinanie rewizji (§8.1, §9) |
| *Taming the Wild West of ML: Practical Model Signing with Sigstore* (model-signing v1.0), Sigstore / OpenSSF, kwi 2025, https://blog.sigstore.dev/model-transparency-v1.0 | podpisywanie modeli, rejestr przejrzystości, czego dowodzi podpis (§8.3, §9) |
| CycloneDX ML-BOM, OWASP CycloneDX, https://cyclonedx.org/ ; profile AI i Dataset w SPDX 3.0, Linux Foundation, https://spdx.dev/ | ML-BOM; plik lock jako minimalny ML-BOM (§8.3) |
| Kurs 2, część 16 §5 (ASI04), to repozytorium, `../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md` | rejestr dostaw i suma kontrolna przy wczytaniu, tu rozszerzone na modele (§0, §10.5) |

## Część 11 · Prywatność i wycieki danych

Lesson: [`11-PRYWATNOSC-I-WYCIEKI-DANYCH.md`](11-PRYWATNOSC-I-WYCIEKI-DANYCH.md)

| Źródło | Co z niego weszło do tej części (sekcja) |
| :-- | :-- |
| Carlini, Liu, Erlingsson, Kos, Song, *The Secret Sharer: Evaluating and Testing Unintended Memorization in Neural Networks*, USENIX Security 2019, https://arxiv.org/abs/1802.08232 | kanarki i miara exposure; zapamiętywanie rzadkich sekretów (§2) |
| Carlini i in., *Extracting Training Data from Large Language Models*, USENIX Security 2021, https://arxiv.org/abs/2012.07805 | dosłowne wydobycie z GPT-2, w tym danych osobowych (§2) |
| Carlini i in., *Quantifying Memorization Across Neural Language Models*, ICLR 2023, https://arxiv.org/abs/2202.07646 | zapamiętywanie rośnie z rozmiarem, duplikacją i kontekstem (§2) |
| Nasr i in., *Scalable Extraction of Training Data from (Production) Language Models*, lis 2023, https://arxiv.org/abs/2311.17035 | atak dywergencyjny na produkcyjny model po alignmencie (§2) |
| Shokri, Stronati, Song, Shmatikov, *Membership Inference Attacks against Machine Learning Models*, IEEE S&P 2017, https://arxiv.org/abs/1610.05820 | klasyczne ujęcie membership inference (§3) |
| Duan i in., *Do Membership Inference Attacks Work on Large Language Models?*, COLM 2024, https://arxiv.org/abs/2402.07841 | MIA bliskie losowemu na danych z pretreningu LLM; przyczyny (§3) |
| Morris, Kuleshov, Shmatikov, Rush, *Text Embeddings Reveal (Almost) As Much As Text* (vec2text), EMNLP 2023, https://arxiv.org/abs/2310.06816 | 92% dokładnego odtworzenia wejść 32-tokenowych (ich pomiar); nazwiska z notatek klinicznych (§4) |
| Gu i in., *Auditing Prompt Caching in Language Model APIs*, ICML 2025, https://arxiv.org/abs/2502.07776 | 8 z 17 dostawców z cache'em, 7 współdzielących globalnie (audyty IX–X 2024); łagodzenia (§6.1) |
| Wu i in., *I Know What You Asked: Prompt Leakage via KV-Cache Sharing in Multi-Tenant LLM Serving*, NDSS 2025, https://www.ndss-symposium.org/ndss-paper/i-know-what-you-asked-prompt-leakage-via-kv-cache-sharing-in-multi-tenant-llm-serving/ | odtwarzanie promptów przez współdzielony cache KV w vLLM/SGLang (§6.1) |
| Song i in., *The Early Bird Catches the Leak: Unveiling Timing Side Channels in LLM Serving Systems*, 2024, https://arxiv.org/abs/2409.20002 | kanały czasowe w systemach serwujących (§6.1) |
| Dokument projektowy *Automatic Prefix Caching* (`cache_salt`), vLLM, aktualny, https://docs.vllm.ai/design/prefix_caching.html | izolacja cache'u per najemca przez solenie (§6.1) |
| README *llama-server* (`/slots`, `--no-slots`, `cache_prompt`), ggml-org/llama.cpp, aktualne, https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md | cache promptu per slot; stan slotów może zawierać prompty (§6.1, §6.2, §10.5) |
| Weiss i in., *What Was Your Prompt? A Remote Keylogging Attack on AI Assistants*, USENIX Security 2024, https://arxiv.org/abs/2403.09751 | kanał boczny długości tokenów w strumieniowanych odpowiedziach (§6.3) |
| *Whisper Leak: a novel side-channel cyberattack on remote language models*, Microsoft, lis 2025, https://www.microsoft.com/en-us/security/blog/2025/11/07/whisper-leak-a-novel-side-channel-cyberattack-on-remote-language-models/ | wnioskowanie o temacie z rozmiarów i czasów pakietów; częściowe łagodzenia (§6.3) |
| Carlini i in., *Stealing Part of a Production Language Model*, ICML 2024, https://arxiv.org/abs/2403.06634 | warstwa projekcji odtworzona przez logprobs + logit_bias za mniej niż 20 USD (ich wyliczenie) (§7) |
| *March 20 ChatGPT outage: Here's what happened*, OpenAI, mar 2023, https://openai.com/index/march-20-chatgpt-outage/ | tytuły rozmów innych użytkowników; dane płatnicze ~1,2% subskrybentów Plus (§8) |
| *Samsung Bans Staff's AI Use After Spotting ChatGPT Data Leak*, Bloomberg, maj 2023, https://www.bloomberg.com/news/articles/2023-05-02/samsung-bans-chatgpt-and-other-generative-ai-use-by-staff-after-leak | pracownicy wklejający wewnętrzny kod do chatbota (§8) |
| *Wiz Research Uncovers Exposed DeepSeek Database Leaking Sensitive Information, Including Chat History*, Wiz, sty 2025, https://www.wiz.io/blog/wiz-research-uncovers-exposed-deepseek-database-leak | ClickHouse bez uwierzytelnienia z logami czatów i kluczami (§8) |
| *OpenAI kills "short-lived experiment" where ChatGPT chats could be found on Google*, Malwarebytes, sie 2025, https://www.malwarebytes.com/blog/news/2025/08/openai-kills-short-lived-experiment-where-chatgpt-chats-could-be-found-on-google | udostępnione rozmowy w wyszukiwarkach; opcja usunięta 1 VIII 2025 (§8) |
| Rozporządzenie (UE) 2016/679 (RODO), art. 5 i art. 17, EUR-Lex, https://eur-lex.europa.eu/eli/reg/2016/679/oj | minimalizacja, ograniczenie przechowywania, prawo do usunięcia (§9) |
| *Opinion 28/2024 on certain data protection aspects related to the processing of personal data in the context of AI models*, Europejska Rada Ochrony Danych, gru 2024, https://www.edpb.europa.eu/our-work-tools/our-documents/opinion-board-art-64/opinion-282024-certain-data-protection-aspects_en | anonimowość modelu oceniana indywidualnie (§9) |
| Część 14 §2–§3 tego kursu, to repozytorium, `14-WYKRYWANIE-MONITORING-I-REAGOWANIE.md` | co logować i jak przechowywać; odnośnik zamiast powtórzenia (§8) |

## Część 12 · Infrastruktura lokalna

Lesson: [`12-INFRASTRUKTURA-LOKALNA.md`](12-INFRASTRUKTURA-LOKALNA.md)

| Źródło | Co weszło do tej części (sekcja) |
| :-- | :-- |
| Cisco, skan wystawionych serwerów Ollama (wrzesień 2025): 1139 serwerów. URL nie został ponownie zweryfikowany w tej sesji; szukaj „Cisco exposed Ollama servers 2025” | liczba wystawionych serwerów, przypisana Cisco (§2.2) |
| SentinelOne + Censys, badanie wystawionych hostów z otwartymi LLM (styczeń 2026): ok. 175 000 hostów. URL nie został ponownie zweryfikowany | druga liczba, przypisana im (§2.2) |
| llama.cpp, README `llama-server`, ggml-org, https://github.com/ggml-org/llama.cpp/tree/master/tools/server | domyślne przypięcie do 127.0.0.1, `--api-key` / `--api-key-file` (§2.2, §5.5) |
| Dokumentacja Ollama (FAQ: `OLLAMA_HOST`), https://github.com/ollama/ollama/blob/main/docs/faq.md | Ollama domyślnie na 127.0.0.1, wystawiana przez `OLLAMA_HOST` (§2.2) |
| Dokumentacja Dockera, packet filtering and firewalls, https://docs.docker.com/engine/network/packet-filtering-firewalls/ (URL z pamięci; sprawdź) | porty publikowane na 0.0.0.0, współgra z ufw/firewalld, `127.0.0.1:` w `-p` (§2.3) |
| Wiz Research, „Probllama” (path traversal w Ollama), 2024; NVD https://nvd.nist.gov/vuln/detail/CVE-2024-37032 | CVE-2024-37032, naprawiony w 0.1.34 (§3) |
| NCC Group, DNS rebinding w Ollama, kwiecień 2024; NVD https://nvd.nist.gov/vuln/detail/CVE-2024-28224 | CVE-2024-28224, naprawiony w 0.1.29 (§3, §4.2) |
| Cyera, „Bleeding Llama”, maj 2026; NVD https://nvd.nist.gov/vuln/detail/CVE-2026-7482 | CVE-2026-7482, ujawnienie pamięci, naprawiony w 0.17.1 (§3) |
| Poradnik bezpieczeństwa Open WebUI dla Direct Connections, 2025; NVD https://nvd.nist.gov/vuln/detail/CVE-2025-64496 | CVE-2025-64496, naprawiony w 0.6.35 (§3) |
| Oligo Security, MCP Inspector, 2025; NVD https://nvd.nist.gov/vuln/detail/CVE-2025-49596 | CVE-2025-49596, naprawiony w 0.14.1 (§3, §4) |
| Biuletyn bezpieczeństwa NVIDIA i Trend Micro, „NVIDIA AI Container Toolkit vulnerability fix”, 2024, https://www.trendmicro.com/en/research/24/i/nvidia-ai-container-toolkit-vulnerability-fix.html; poradnik GitLab dla CVE-2024-0132 | CVE-2024-0132, ucieczka TOCTOU, naprawiony w 1.16.2 (§3) |
| Wiz Research, „NVIDIAScape”, lipiec 2025; NVD https://nvd.nist.gov/vuln/detail/CVE-2025-23266 | CVE-2025-23266, naprawiony w 1.17.8 (§3) |
| Oligo Security, „ShadowRay” (2024) i „ShadowRay 2.0” (listopad 2025); NVD https://nvd.nist.gov/vuln/detail/CVE-2023-48022 | API zadań Ray bez uwierzytelniania, CVE kwestionowane przez producenta, bez łatki (§1, §3) |
| Sorensen i Khlaaf, Trail of Bits, „LeftoverLocals: Listening to LLM responses through leaked GPU local memory”, styczeń 2024, https://arxiv.org/abs/2401.16603; CERT/CC VU#446598, https://kb.cert.org/vuls/id/446598 | CVE-2023-4969, dotknięci producenci, lekcja o izolacji pamięci GPU (§3, §5.4) |
| Zespół Google Chrome, Local Network Access, blog czerwiec 2025 (opt-in od Chrome 138), https://developer.chrome.com/blog/local-network-access (URL z pamięci; sprawdź) | pytanie przeglądarki o dostęp do sieci prywatnej (§4.3) |
| Dokumentacja Caddy, https://caddyserver.com/docs/ | `reverse_proxy`, `tls internal`, `request_body`, matchery nagłówków (§5.2); nie uruchamiane w tej sesji |

## Część 13 · Guardrails, red teaming i ocena obron

Lesson: [`13-GUARDRAILE-RED-TEAMING-I-OCENA-OBRON.md`](13-GUARDRAILE-RED-TEAMING-I-OCENA-OBRON.md)

| Źródło | Co weszło do tej części (sekcja) |
| :-- | :-- |
| OWASP, Top 10 for LLM Applications 2025, LLM01 Prompt Injection, https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | środki zaradcze warstwowo, brak niezawodnego zapobiegania (§1) |
| NIST, AI 100-2 E2025, Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations, https://csrc.nist.gov/pubs/ai/100/2/e2025/final | ocena wobec przeciwników adaptacyjnych (§1) |
| Meta, dokumentacja modeli Llama Prompt Guard 2 (86M, 22M), https://www.llama.com/docs/model-cards-and-prompt-formats/prompt-guard/ | rozmiary, binarne etykiety benign/malicious, licencja za bramką (§1, §6.3). Rozmiaru okna kontekstu NIE potwierdzono ze strony Mety; lekcja każe czytelnikowi sprawdzić kartę modelu |
| Meta, Llama Guard 3 i Llama Guard 4 (klasyfikatory bezpieczeństwa treści), https://www.llama.com/docs/model-cards-and-prompt-formats/ | do czego służy model bezpieczeństwa treści w odróżnieniu od detektora injection (§1); bez liczb specyficznych dla modelu |
| Nasr, Carlini, Sitawarin, Schulhoff i in., „The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections”, arXiv 2510.09023, październik 2025, https://arxiv.org/abs/2510.09023 | 12 obejść obron; metody gradientowe, RL, przeszukiwanie losowe i kierowane przez człowieka; ludzie odnieśli sukces tam, gdzie statyczny atak bazowy nie; zalecenia (§4). Liczba „>90% dla większości” pochodzi z wtórnego streszczenia abstraktu: lekcja każe czytelnikowi sprawdzić liczby per obrona w artykule |
| Hackett, Birch, Trawicki, Suri, Garraghan, „Bypassing Prompt Injection and Jailbreak Detection in LLM Guardrails”, arXiv 2504.11168, kwiecień 2025, https://arxiv.org/abs/2504.11168 | wstrzykiwanie znaków i unikanie ML przeciwnika wobec sześciu detektorów (§4.1); dokładnych liczb per detektor nie sprawdzono |
| Robust Intelligence (obecnie Cisco), obejście Prompt-Guard-86M Mety przez rozstrzelenie liter, 2024. URL nie został ponownie zweryfikowany | przykład z rozstrzeleniem znaków (§4.1) |
| Wilson, E. B., „Probable inference, the law of succession, and statistical inference”, JASA, 1927 (przedział score); wzór zaimplementowany w `harness.wilson` w laboratorium | metoda przedziału (§3.2, §5.3); tabela górnych granic jest nią policzona |
| NVIDIA, garak, https://github.com/NVIDIA/garak (przypięty 0.17.1) | probes/detectors, `--target_type openai.OpenAICompatible`, `--generator_options`, `OPENAICOMPATIBLE_API_KEY` (§5.1, §6.5). Polecenia nie uruchamiane w tej sesji (brak dostępu do indeksu pakietów w piaskownicy) |
| Microsoft, PyRIT, https://microsoft.github.io/PyRIT/1.1.0/ (przypięty 1.1.0) | cele, konwertery, scorery; importy `PromptSendingAttack`, `OpenAIChatTarget`, `IN_MEMORY`, `initialize_pyrit_async` potwierdzone na stronie głównej 1.1.0; pozostałych importów nie potwierdzono (§5.1, §6.6). Skrypt nie uruchamiany |
| promptfoo, https://www.promptfoo.dev/docs/red-team/ (przypięty 0.124.1) | plugins, strategies, własny provider w Pythonie, `PROMPTFOO_DISABLE_REDTEAM_REMOTE_GENERATION` (§5.1, §6.7). Konfiguracja nie uruchamiana |
| GitHub Docs, security hardening for GitHub Actions (runnery self-hosted i forki), https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions (URL z pamięci; sprawdź) | runnery self-hosted i pull requesty z forków, przypinanie akcji do SHA (§6.9) |
| Część 14 tego kursu, sekcja 10.6, format przypadków przyjaznych mockowi | konwencja `>>> CALL` plus nośnik w języku naturalnym dla przypadków bramki (§6.9) |

## Część 14 · Wykrywanie, monitoring i reagowanie na incydenty

Lesson: [`14-WYKRYWANIE-MONITORING-I-REAGOWANIE.md`](14-WYKRYWANIE-MONITORING-I-REAGOWANIE.md)

| Źródło | Co weszło do tej części (sekcja) |
| :-- | :-- |
| *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile* (SP 800-61 Rev. 3), NIST, kwiecień 2025, https://csrc.nist.gov/pubs/sp/800/61/r3/final | ujęcie runbooka wokół funkcji CSF 2.0 (§9) |
| *GenAI Incident Response Guide 1.0*, OWASP GenAI Security Project (inicjatywa CTI), lipiec 2025, https://genai.owasp.org/resource/genai-incident-response-guide-1-0/ | reagowanie specyficzne dla GenAI, promień rażenia incydentu AI (§9) |
| *Semantic conventions for generative AI systems* (status: Development), OpenTelemetry, 2024–2026, https://opentelemetry.io/docs/specs/semconv/gen-ai/ | nazwy atrybutów śladów; treść wiadomości jako atrybuty opt-in (§2) |
| *Canarytokens*, Thinkst Applied Research, https://canarytokens.org/ | idea kanarków / honeytokenów w klasycznej infrastrukturze (§4) |
| *Rebuff: self-hardening prompt injection detector*, Protect AI, 2023, https://github.com/protectai/rebuff | sprawdzanie „słowa-kanarka” w otwartym detektorze (§4.1) |
| Gakh, V., Bahsi, H., *Enhancing Security in LLM Applications: A Performance Evaluation of Early Detection Systems*, Politechnika Tallińska, czerwiec 2025, https://arxiv.org/abs/2506.19109 | domyślne kanarki w Rebuff i Vigil nie wykryły żadnego z ataków autorów na wyciek promptu; przyczyną było umiejscowienie (§4.1) |
| Abdelnabi, S., Fay, A. i in., *Get my drift? Catching LLM Task Drift with Activation Deltas* (pierwotnie „Are you still on track!?”), Microsoft i CISPA, arXiv czerwiec 2024 / SaTML 2025, https://arxiv.org/abs/2406.00799 ; kod: https://github.com/microsoft/TaskTracker | wykrywanie dryfu zadania na podstawie aktywacji w modelach otwartych; granice tej metody wobec ataku adaptacyjnego (§5) |
| Nasr, M., Carlini, N. i in., *The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections*, październik 2025, https://arxiv.org/abs/2510.09023 | dlaczego sama prewencja nigdy nie schodzi do zera (§0) |
| *ChatGPT macOS Flaw Could've Enabled Long-Term Spyware via Memory Function* (o „SpAIware” J. Rehbergera), The Hacker News, wrzesień 2024, https://thehackernews.com/2024/09/chatgpt-macos-flaw-couldve-enabled-long.html | trwałe wstrzyknięcie do pamięci; poprawka w ChatGPT macOS 1.2024.247; „czyszczenie pamięci” jako krok reagowania (§9.2) |
| *EchoLeak: The First Real-World Zero-Click Prompt Injection Exploit in a Production LLM System*, 2025, https://arxiv.org/abs/2509.10540 ; *Zero-Click AI Vulnerability Exposes Microsoft 365 Copilot Data Without User Interaction*, The Hacker News, czerwiec 2025, https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html ; CVE-2025-32711, Microsoft MSRC, https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711 | eksfiltracja bez kliknięcia, CVSS 9.3, zgłoszona w styczniu 2025, poprawka po stronie serwera w maju 2025, ujawniona w czerwcu 2025 (§9.2) |
| Rozporządzenie (UE) 2016/679 (RODO), art. 33 i 34, Unia Europejska, 2016, https://eur-lex.europa.eu/eli/reg/2016/679/oj | zgłoszenie naruszenia organowi nadzorczemu (72 h) i osobom, których dane dotyczą (§9) |
| Kurs 2, część 15 *Obserwowalność*, część 16 *Bezpieczeństwo (OWASP ASI)*, część 18 *Wydanie i utrzymanie*, to repozytorium, 2026, `../kurs_aplikacje_agentowe/` | ślady, odtwarzanie, wyłącznik awaryjny, sygnał „nagłego przyrostu” w pamięci, format runbooka (§0, §6, §9) |

## Część 15 · Capstone: zabezpiecz laboratorium od początku do końca

Lesson: [`15-CAPSTONE.md`](15-CAPSTONE.md)

| Źródło | Co weszło do tej części (sekcja) |
| :-- | :-- |
| Willison, S., *The lethal trifecta for AI agents: private data, untrusted content, and external communication*, 16 czerwca 2025, https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | zasada 2: przerwij śmiertelną triadę w każdej sesji (§1.1, §7) |
| *Agents Rule of Two: A Practical Approach to AI Agent Security*, Meta AI, 31 października 2025, https://ai.meta.com/blog/practical-ai-agent-security/ | najwyżej dwa z trzech: niezaufane wejście, wrażliwe dane/systemy, zmiana stanu lub komunikacja na zewnątrz (§1.1) |
| Debenedetti, E. i in., *Defeating Prompt Injections by Design* (CaMeL), Google DeepMind i ETH Zurich, marzec 2025, https://arxiv.org/abs/2503.18813 | zasada 3: deterministyczna kontrola poza modelem (§1.1) |
| Beurer-Kellner, L. i in., *Design Patterns for Securing LLM Agents against Prompt Injections*, czerwiec 2025, https://arxiv.org/abs/2506.08837 | zasada 3; poprawki architektoniczne w ćwiczeniu 4 (§1.1, §9) |
| Nasr, M., Carlini, N. i in., *The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections*, październik 2025 (USENIX Security 2026), https://arxiv.org/abs/2510.09023 | zasada 4; ASR >90% przeciw większości z 12 obron; runda adaptacyjna; red-teaming z udziałem ludzi (§1.1, §3.1, §9) |
| Wilson, E. B., *Probable Inference, the Law of Succession, and Statistical Inference*, Journal of the American Statistical Association 22(158), 1927, https://doi.org/10.1080/01621459.1927.10502953 | przedział używany przez harness i `report.py`; czytanie górnej granicy (§5) |
| CVE-2025-32711 (EchoLeak), Microsoft MSRC, 2025, https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-32711 | „zasięg” w skali ważności: bez kliknięcia (§6) |
| Rozporządzenie (UE) 2024/1689 (AI Act), art. 50, Unia Europejska, 2024, https://eur-lex.europa.eu/eli/reg/2024/1689/oj | informowanie ludzi, że rozmawiają z systemem AI, stosowane od 2 sierpnia 2026 (§7) |
| Rozporządzenie (UE) 2016/679 (RODO), Unia Europejska, 2016, https://eur-lex.europa.eu/eli/reg/2016/679/oj | dane osobowe innych użytkowników (§7) |
| Kurs 2, część 16 *Bezpieczeństwo (OWASP ASI)* §10 (ASI09, podsumowania do zatwierdzenia budowane przez kod), to repozytorium, 2026, `../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md` | potwierdzenia w §4 i pytanie 6 przeglądu (§4, §7) |
| Części 01–14 tego kursu | każda warstwa mapy obrony w głąb i każda konfiguracja w stosie (§1, §2) |
