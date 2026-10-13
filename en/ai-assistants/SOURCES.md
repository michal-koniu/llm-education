# Sources — what this review stands on

**Checked on 11 October 2026.** For every entry: what I took from it. Primary sources (product pages, price lists,
documentation, company announcements, legal acts) take precedence; figures reported by the companies themselves and
press estimates are flagged in the text. Every profile in [01-PROFILES.md](01-PROFILES.md) also has its own source links.

## GitHub figures

- **GitHub API** — `GET /repos/{owner}/{repo}` and `GET /repos/{…}/releases/latest`, called on 11 October 2026:
  openclaw/openclaw, NousResearch/hermes-agent, browser-use/browser-use, NVIDIA/NemoClaw, nanocoai/nanoclaw,
  bytedance/UI-TARS-desktop, cline/cline, nextcloud/assistant → stars, licences, releases.

## Profiles 1, 2, 5, 6, 13

| Source | What I took |
|---|---|
| [OpenClaw — GitHub](https://github.com/openclaw/openclaw) | MIT licence, stars, releases, 2026 security advisories (GitHub API, 11 October 2026) |
| [OpenClaw — introduction](https://openclaw.ai/blog/introducing-openclaw) | rename to OpenClaw, >100k stars and 2 million visits in a week, funding for the maintainers |
| [OpenClaw Foundation](https://openclaw.ai/blog/introducing-openclaw-foundation) | 501(c)(3) foundation from 8 July 2026, donors and partners, ClawCon, "4.5 million new claws", NemoClaw |
| [OpenClaw Enterprise](https://openclaw.ai/blog/openclaw-enterprise) | enterprise distribution from 29 September 2026, "will always be free", IT bans agents by default |
| [Microsoft Autopilot on OpenClaw](https://openclaw.ai/blog/microsoft-autopilot-openclaw) | Autopilot from 25 September 2026, private preview, upstream fixes (Policy plugin, Teams, Windows) |
| [OpenClaw — security in public](https://openclaw.ai/blog/openclaw-security-in-public) | Steinberger's report statistics, moving channels and providers into plugins |
| [OpenClaw — rough week](https://openclaw.ai/blog/openclaw-rough-week) | broken releases in April 2026, "too founder-driven" |
| [OpenClaw — VirusTotal](https://openclaw.ai/blog/virustotal-partnership) | skill scanning since 7 February 2026 |
| [OpenClaw — NVIDIA SkillSpector](https://openclaw.ai/blog/openclaw-nvidia-skill-security) | SkillSpector and Skill Cards (1 June 2026) |
| [OpenClaw — ClawScan](https://openclaw.ai/blog/tencent-aig-joins-clawscan) | Tencent AI-Infra-Guard, 98.6% of malicious skills detected across 556 cases |
| [OpenClaw docs — heartbeat](https://docs.openclaw.ai/gateway/heartbeat) | 30 min / 1 h interval, wake-up limits |
| [OpenClaw docs — standing orders](https://docs.openclaw.ai/automation/standing-orders) | scope, trigger, gate, escalation; files injected into the session |
| [OpenClaw docs — dreaming](https://docs.openclaw.ai/concepts/dreaming) | memory consolidation phases, DREAMS.md, weights 1–10 |
| [OpenClaw docs — workspace](https://docs.openclaw.ai/concepts/agent-workspace) | the workspace is not a hard sandbox |
| [OpenClaw docs — local models](https://docs.openclaw.ai/gateway/local-models) | llama.cpp, Ollama, vLLM, ds4; ≥8 GiB and 64K; no safety filters locally |
| [OpenClaw docs — Ollama](https://docs.openclaw.ai/providers/ollama) | native /api/chat, /v1 breaks tool calls |
| [OpenClaw docs — security](https://docs.openclaw.ai/gateway/security) | pairing codes, allowlists, security audit |
| [TechCrunch: Steinberger at OpenAI](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/) | move to OpenAI on 14–15 February 2026, foundation announcement |
| [The Register on OpenClaw 2.0](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) | 2.0 news, secrets stored unencrypted, sandbox off by default, the gym incident |
| [Cloudflare — Moltworker](https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/) | hosting on Workers, "flood of people buying Mac minis" |
| [Cisco on OpenClaw](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare) | exfiltration via a skill, 26% of 31k skills vulnerable |
| [InsiderLLM — ClawHub audits](https://insiderllm.com/guides/openclaw-clawhub-security-alert/) | counts of malicious skills (secondary source) |
| [Wiz — Moltbook](https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys) | exposed API tokens and e-mails |
| [Wikipedia — OpenClaw](https://en.wikipedia.org/wiki/OpenClaw) | history of the names, MoltMatch, restrictions in China, Nadella, 247k stars in March 2026 |
| [Wikipedia — Moltbook](https://en.wikipedia.org/wiki/Moltbook) | launch on 28 January 2026, acquisition by Meta |
| [Anthropic — Series G](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation) | USD 30 bn at USD 380 bn, run-rate USD 14 bn, Claude Code >USD 2.5 bn, 4% of commits |
| [Claude — memory](https://claude.com/resources/articles/claudes-memory-works-everywhere-and-you-decide-whats-in-it) | memory in topic files, sensitive topics kept out of memory by default (25 August 2026) |
| [Claude — Cowork to Claude](https://claude.com/resources/articles/cowork-is-now-claude) | merge with chat on 16 September 2026, scheduling, asking before acting |
| [Claude — how people use Cowork](https://claude.com/resources/articles/how-people-are-using-claude-cowork) | 1.2 million sessions, breakdown of task categories |
| [Claude — Dispatch and computer use](https://claude.com/resources/articles/dispatch-and-computer-use) | Dispatch with computer use from 23 March 2026 |
| [Claude — Routines](https://claude.com/resources/articles/introducing-routines-in-claude-code) | Routines in Claude Code (14 April 2026) |
| [Claude — Cowork research preview](https://claude.com/blog/cowork-research-preview) | plan prices, folders, separate browser, approvals |
| [Claude — Cowork help](https://support.claude.com/en/articles/13345190-getting-started-with-cowork) | execution in the Anthropic cloud, scope of outbound-traffic permissions |
| [Simon Willison on Cowork](https://simonwillison.net/2026/Jan/12/claude-cowork/) | local Apple Virtualization VM in January 2026 |
| [Docs — computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) | toolset GA, 17 tools, batch actions, screenshot cost, recommendations |
| [Docs — browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) | 31 tools, accessibility tree, developer-side execution |
| [Computer use demo](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo) | open reference container |
| [Claude for Chrome](https://claude.com/blog/claude-for-chrome) | safeguards, 23.6% → 11.2%, availability schedule |
| [Claude in Chrome](https://claude.com/chrome) | 2026 features, GA on paid plans, discouraged use cases |
| [Anthropic — prompt injection defences](https://www.anthropic.com/research/prompt-injection-defenses) | about 1% for Opus 4.5 against an adaptive attacker |
| [Anthropic — computer use 2024](https://www.anthropic.com/news/3-5-models-and-computer-use) | launch on 22 October 2024, 14.9% OSWorld |
| [Anthropic — Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5) | 61.4% OSWorld |
| [Anthropic — Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6) | prices USD 3 / 15 |
| [Anthropic — Opus 5.5](https://www.anthropic.com/news/claude-opus-5-5) | 81.8% OSWorld 2.1, prices USD 4 / 20 (22 September 2026) |
| [Anthropic — Vercept](https://www.anthropic.com/news/acquires-vercept) | acquisition on 25 February 2026, 72.5% OSWorld |
| [Claude Code — data](https://code.claude.com/docs/en/data-usage) | model providers, retention, non-essential traffic switch, cloud VM |
| [TechCrunch — Claude Code limits](https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/) | weekly limits from 28 August 2025, <5% of subscribers |
| [Stack Overflow 2026](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/) | Claude Code — 66% of coding-agent users |
| [iTiger — SemiAnalysis](https://www.itiger.com/hans/news/1183910360) | estimate of about USD 44 bn run-rate in May 2026 (secondary) |
| [TechCrunch — Claude for Legal](https://techcrunch.com/2026/05/12/the-ai-legal-services-industry-is-heating-up-anthropic-is-getting-in-on-the-action/) | plugins and MCP connectors to Westlaw, Box, Docusign (12 May 2026) |
| [LawNext — CoCounsel on the Agent SDK](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html) | the new CoCounsel built on the Claude Agent SDK |
| [Microsoft — Copilot privacy](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) | Anthropic models outside the EU Data Boundary (as of 8 October 2026) |
| [PromptArmor — Cowork](https://www.promptarmor.com/resources/claude-cowork-exfiltrates-files) | file exfiltration through an allowed API |
| [BleepingComputer — BragJack](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/) | attack via extensions, CVE-2026-0628, including Claude in Chrome |
| [Wikipedia — Claude (language model)](https://en.wikipedia.org/wiki/Claude_(language_model)) | Ars Technica's concerns about Chrome, Cowork in Chrome |
| [Wikipedia — Claude (AI)](https://en.wikipedia.org/wiki/Claude_(AI)) | Claude Code source leak, abuse cases (Wired, BBC), Claude Design |
| [Hermes Agent — GitHub](https://github.com/NousResearch/hermes-agent) | MIT, stars, releases, zero security advisories in 2026 |
| [Hermes Agent — README](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/README.md) | features, backends, FTS5, migration from OpenClaw, trajectories |
| [Hermes Agent — website](https://hermes-agent.nousresearch.com/) | Nous Portal Plus / Super / Ultra prices (11 October 2026) |
| [Hermes docs — memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) | MEMORY.md and USER.md limits, frozen snapshot |
| [Hermes docs — skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) | skills catalogue, hub, ClawHub, scanning |
| [Hermes docs — cron](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron) | jobs in natural language |
| [Hermes docs — delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation) | executors with a separate provider, child limit (after the harness review) |
| [Hermes docs — voice](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode) | faster-whisper locally, Edge TTS by default (after the harness review) |
| [Hermes docs — index](https://hermes-agent.nousresearch.com/llms.txt) | Nous Portal as a model and credits provider |
| [Nous — funding round](https://nousresearch.com/a-note-on-our-fundraise) | USD 90 m, investors, 24 million clones, 2.5% of tokens, MIT since February 2026 |
| [Nous Research](https://nousresearch.com/) | Microsoft Store app from 8 October 2026 |
| [Nous — blog](https://nousresearch.com/blog) | refactoring with 1393 agents |
| [Hermes Business](https://portal.nousresearch.com/business) | shared balance, per-person limits, skills library, Enterprise |
| [NVIDIA NemoClaw](https://github.com/NVIDIA/NemoClaw) | supported agents (OpenClaw, Hermes, Deep Agents), OpenShell sandbox |
| [Manus — context engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) | six principles, KV-cache, 100:1, todo.md, about 50 calls per task |
| [Manus 2.0](https://manus.im/blog/introducing-manus-2-0) | Cascade, Cloud Computer, automations, Cue, claimed savings |
| [Manus Flex](https://manus.im/blog/introducing-manus-flex) | bring your own model key, credits for infrastructure |
| [Manus — Wide Research](https://manus.im/blog/introducing-wide-research) | parallel agents with fresh context |
| [Manus docs — Wide Research](https://manus.im/docs/features/wide-research.md) | up to 250 items |
| [Manus 1.5](https://manus.im/blog/manus-1.5-release) | full-stack apps, task time 15 → <4 min |
| [Manus — Browser Operator](https://manus.im/blog/manus-browser-operator) | extension in the local browser, per-session consent, action log |
| [Manus docs — Cloud Browser](https://manus.im/docs/features/cloud-browser.md) | persistent sessions, Take Over, data-centre IP blocks |
| [Manus — USD 100m ARR](https://manus.im/blog/manus-100m-arr) | ARR, run-rate, 147 trillion tokens, 80 million computers, 105 employees |
| [Manus — letter to users](https://manus.im/blog/a-note-to-our-users) | return to independence, data deletion on 23–24 August 2026, data in the US and Singapore |
| [Manus — independence](https://manus.im/blog/manus-resumes-independent-operations) | formal independence on 1 September 2026, availability in the EU |
| [Manus — credit rules](https://help.manus.im/en/articles/11711097-what-are-the-rules-for-credits-consumption-and-how-can-i-obtain-them) | what consumes credits, daily refresh, no carry-over |
| [E2B — Manus case study](https://e2b.dev/blog/how-manus-uses-e2b-to-provide-agents-with-virtual-computers) | Firecracker micro-VMs, about 150 ms startup, rejection of Docker |
| [The Decoder](https://the-decoder.com/chinese-ai-agent-manus-uses-claude-sonnet-and-open-source-technology/) | models at launch, browser-use, executor–planner setup |
| [TechCrunch — Manus March 2025](https://techcrunch.com/2025/03/09/manus-probably-isnt-chinas-second-deepseek-moment/) | reliability tests, GAIA claim |
| [TechCrunch — China's veto](https://techcrunch.com/2026/04/27/china-vetoes-metas-2b-manus-deal-after-months-long-probe/) | NDRC decision of 27 April 2026, exit ban for the founders |
| [TechCrunch — round October 2026](https://techcrunch.com/2026/10/08/chinas-manus-raises-over-500m-in-first-funding-round-since-split-with-meta/) | >USD 500 m, Boyu and IDG, target of about USD 4 bn |
| [Bloomberg — blocked acquisition](https://www.bloomberg.com/news/articles/2026-04-27/china-blocks-meta-s-2-billion-acquisition-of-ai-startup-manus) | confirmation of the block |
| [Yahoo — Manus valuation](https://finance.yahoo.com/technology/ai/articles/manus-seeks-4b-valuation-beijing-183502124.html) | share buyback, operational separation |
| [Dahui Lawyers](https://www.dahuilawyers.com/en/news-insights/chinas-first-public-foreign-investment-security-review-prohibition-the-metamanus-decision/) | first public prohibition in Chinese investment review |
| [Sacra — Manus](https://sacra.com/c/manus) | March 2025 prices, estimate of USD 450 m in June 2026 |
| [MyClaw — Manus 2.0 review](https://myclaw.ai/blog/manus-2-0) | September 2026 prices, Cloud Computer, Cue wallet limits (third party) |
| [Embrace The Red](https://embracethered.com/blog/posts/2025/manus-ai-kill-chain-expose-port-vs-code-server-on-internet/) | attack exposing a port (25 August 2025) |
| [OpenManus](https://github.com/FoundationAgents/OpenManus) | open MIT clone, stars, Ollama support |
| [Wikipedia — Manus](https://en.wikipedia.org/wiki/Manus_(AI_agent)) | launch, Series B, move to Singapore, resale of invites |
| [browser-use — GitHub](https://github.com/browser-use/browser-use) | MIT, stars, release 0.13.11 |
| [browser-use — GitHub API](https://api.github.com/repos/browser-use/browser-use) | repository creation date, forks |
| [browser-use — pricing](https://browser-use.com/pricing.md) | browser, proxy and token rates, concurrency tiers (3 September 2026) |
| [browser-use — benchmarks](https://browser-use.com/benchmarks) | Browser Use Bench v2.1 with cost per task (7 October 2026) |
| [browser-use — changelog 3 April 2026](https://browser-use.com/changelog/3-4-2026) | free tier, V4 schedule, Agency skill |
| [browser-use — BU-30B-A3B](https://browser-use.com/changelog/16-12-2025) | open weights, 3B active, vLLM |
| [browser-use — move to CDP](https://browser-use.com/changelog/19-8-2025) | "100% CDP-based" |
| [browser-use — BU 2.0](https://browser-use.com/changelog/27-1-2026) | comparison with Opus 4.5 (vendor claim) |
| [browser-use — choosing an agent](https://docs.browser-use.com/cloud/choosing-an-agent) | V2 / V3 / V4: cost, accuracy, time; profiles and secrets |
| [browser-use — BU 2.0 model card](https://docs.browser-use.com/open-source/bu-2-0-model-card) | model available only via API |
| [browser-use — WebVoyager report](https://browser-use.com/posts/sota-technical-report) | 89.1% after removing 55 tasks |
| [Felicis](https://felicis.com/blog/browser-use-the-tool-making-it-easier-for-ai-agents-to-navigate-websites-raises-17m) | USD 17 m seed, investors |
| [ain.ua](https://en.ain.ua/2025/03/25/browser-use-raises-17m) | founders, ETH Zurich, the "text instead of pixels" idea |
| [Princeton HAL — Online-Mind2Web](https://hal.cs.princeton.edu/online_mind2web) | independent score of 40.0% for browser-use + Sonnet 4 |
| [TechCrunch — OpenAI on prompt injection](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/) | "unlikely to ever be fully solved" (22 December 2025) |
| [The Register — Gartner](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/) | recommendation to block AI browsers (8 December 2025) |
| [TechCrunch — end of Atlas](https://techcrunch.com/2026/07/09/openai-is-shutting-down-atlas-but-its-ai-browser-ambitions-are-still-growing/) | Atlas shutdown, "feature, not the destination" |
| [36Kr — AI browser share](https://eu.36kr.com/en/p/3931781634260099) | <1% of the browser market (August 2026) |
| [OpenManus — commits](https://api.github.com/repos/FoundationAgents/OpenManus/commits?per_page=5) | Browser Use CLI 3.0 integration (August 2026) |
| [Harness review — profiles](../agent-harnesses/01-PROFILES.md) | Hermes (81 pts, 4th place), OpenClaw (47th place), the H4 trap, Moltis with Polish Piper |

## Profiles 3, 4, 9–12, 14

| Source | What I took |
|---|---|
| [Fortune, 11 June 2026 — Abridge](https://fortune.com/2026/06/11/abridge-operating-system-medicine-nvidia-eli-lilly-artsight/) | Abridge's shift to a "platform", Lilly, NVIDIA, Artisight, 100m+ conversations a year, valuation of USD 5.3 bn |
| [Sacra: Abridge](https://sacra.com/c/abridge/) | price estimate of about USD 2,500 per physician per year, ARR 2024–2025, Best in KLAS February 2026 |
| [Abridge: ASR benchmark](https://www.abridge.com/blog/becoming-the-benchmark-for-healthcare-ai) | claimed results of its own ASR (6 August 2025) |
| [Abridge: eliminating confabulation](https://www.abridge.com/ai/science-confabulation-hallucination-elimination) | guard model, 97% vs 82% for GPT-4o (company data) |
| [Webb et al., Appl Clin Inform 2026](https://pubmed.ncbi.nlm.nih.gov/41734793/) | independent comparison of Abridge and DAX in the ED |
| [MobiHealthNews: Abridge Series E](https://www.mobihealthnews.com/news/abridge-secures-300m-boosts-valuation-53b) | rounds D and E, 2025 valuations |
| [Menlo Ventures: AI in healthcare 2025](https://menlovc.com/perspective/2025-the-state-of-ai-in-healthcare/) | scribe market shares (Microsoft about 33%, Abridge about 30%) |
| [HLTH: Epic AI Charting](https://hlth.com/insights/news/epic-releases-native-ai-charting-for-integrated-clinical-documentation-2026-02-06) | Epic's native scribe (February 2026) and pressure on vendors |
| [Fierce Healthcare: PHTI on scribes](https://www.fiercehealthcare.com/ai-and-machine-learning/early-evaluation-ai-scribes-finds-decreased-burnout-limited-financial-roi) | less burnout, limited financial return |
| [Lukac et al., NEJM AI (UCLA RCT)](https://pubmed.ncbi.nlm.nih.gov/41497288/) | moderate time savings with scribes |
| [Parakeet-TDT-0.6B-v3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) | local ASR with Polish, about 7.3% WER per the model card |
| [pyannote community-1](https://huggingface.co/pyannote/speaker-diarization-community-1) | offline diarization, CC-BY-4.0 |
| [Noa: pricing](https://noa.ai/pl/cennik) | Noa Notes PLN 199 + VAT per month, price anchor for a scribe |
| [Harvey: multi-model by design](https://www.harvey.ai/en-US/blog/why-harvey-is-multi-model-by-design) | model router, failover, BigLaw Bench |
| [Harvey Tenet](https://www.harvey.ai/blog/post-training-update-harvey-tenet) | Kimi K3 + RL (GSPO), no client data, about 1/10 of the cost |
| [Harvey II](https://www.harvey.ai/blog/introducing-harvey-ii) | Spaces, personal memory, ethical walls |
| [Harvey: MCP Policy Engine](https://www.harvey.ai/blog/building-harveys-mcp-policy-engine) | policies outside the model, lethal trifecta, tool pinning |
| [Harvey: security](https://www.harvey.ai/en-US/security) | processing regions, zero retention, certifications, no on-prem |
| [Harvey: USD 550m round](https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence) | USD 15.5 bn (9 September 2026), 80% of the Am Law 100 |
| [TechCrunch, 9 September 2026 — Harvey](https://techcrunch.com/2026/09/09/harvey-hits-15-5b-valuation-months-after-reaching-11b/) | total capital above USD 1.55 bn |
| [Wikipedia: Harvey](https://en.wikipedia.org/wiki/Harvey_(software)) | valuation history, founders, the A&O test |
| [ITBrief: Harvey's 500 agents](https://itbrief.co.uk/story/harvey-launches-500-legal-ai-agents-builder-tool) | Agent Builder, customer count (May 2026) |
| [raising.fi: Harvey September 2026](https://raising.fi/news/harvey-undisclosed-september-2026) | ARR above USD 400 m (secondary press), acquisition of Guardrails AI |
| [Vaquill: Harvey review](https://www.vaquill.ai/blog/harvey-ai-review-honest-assessment) | seat price estimates (unverified) |
| [LexisNexis + Harvey](https://www.lexisnexis.com/community/pressroom/b/news/posts/lexisnexis-and-harvey-announce-strategic-alliance-to-integrate-trusted-high-quality-ai-technology-and-legal-content-and-develop-advanced-workflows) | content alliance, Shepard's |
| [D. Charlotin's hallucination database](https://www.damiencharlotin.com/hallucinations/) | 2,184 cases, 6 in Poland (10 October 2026) |
| [Cursor: pricing](https://cursor.com/pricing) | plans and prices (October 2026), Bugbot, MCP |
| [Cursor: changelog](https://cursor.com/changelog) | Self-Hosted Machines, Projects, Rollouts, iOS (August–October 2026) |
| [Cursor: Composer 2](https://cursor.com/blog/composer-2) | benchmark results and token prices (company data) |
| [Cursor: June 2025 pricing](https://cursor.com/blog/june-2025-pricing) | Pro plan change, apology and refunds |
| [Cursor: data use](https://cursor.com/data-use) | every request goes through the backend, Privacy Mode |
| [Cursor: security](https://cursor.com/security) | SOC 2 Type II |
| [Cursor: joining SpaceX](https://cursor.com/blog/joining-spacex) | acquisition closed on 14 August 2026, SpaceXAI, Grok |
| [Wikipedia: Cursor](https://en.wikipedia.org/wiki/Cursor_(company)) | rounds, SpaceX deal timeline, acquisitions, the "Sam" bot |
| [Bloomberg: Cursor ARR USD 2 bn](https://www.bloomberg.com/news/articles/2026-03-02/cursor-recurring-revenue-doubles-in-three-months-to-2-billion) | ARR February 2026 |
| [Gigazine: Composer 2 on Kimi](https://gigazine.net/gsc_news/en/20260323-cursor-admits-composer-2-kimi) | undisclosed Kimi K2.5 base |
| [DataCamp: Cursor 3](https://www.datacamp.com/blog/cursor-3) | agents window, cloud VMs, session transfer |
| [Silicon Canals: Cursor](https://siliconcanals.com/t-cursor-100-million-2-billion-annualized-revenue-13-months/) | about 60% of revenue from businesses (March 2026) |
| [Jetadmin: Cursor plans](https://www.jetadmin.io/blog/cursor-pricing-explained-plans-credit-system-and-real-costs-in-2026/) | Pro+ and Ultra (July 2026) |
| [TNW: Granola Series C](https://thenextweb.com/news/granola-series-c-meeting-ai-enterprise-context) | rounds, MCP and API, customers |
| [Granola: pricing](https://www.granola.ai/pricing) | per-seat plans, integrations, Enterprise features |
| [Granola: transcription](https://docs.granola.ai/help-center/taking-notes/transcription) | audio is not stored, Me/Them diarization |
| [YipitData: Granola vs competitors](https://www.yipitdata.com/resources/blog/granola-vs-fathom-otter-fireflies-ai-notetaking) | winning over users, low churn |
| [SoftwareTestingHelp: Granola](https://www.softwaretestinghelp.com/?p=411472) | stated ASR and LLM vendors (unverified) |
| [ARR.club: Granola](https://www.arr.club/granola/granola-arr-grow-at-250-in-q1-2026) | revenue growth in Q1 2026 |
| [Sacra: Granola](https://sacra.com/research/250m-year-granola-for-plumbers) | 250k+ users (unverified) |
| [Substack: dangers of AI note-takers](https://afadeev.substack.com/p/the-hidden-dangers-of-ai-note-taking) | AssemblyAI key hard-coded in the beta |
| [Granola: June 2026 vulnerability](https://docs.granola.ai/help-center/policies/security-contributions/desktop-app-navigation-vulnerability) | course of the patching |
| [Startup Fortune: Granola privacy](https://startupfortune.com/granola-ai-meeting-notes-are-not-as-private-as-you-might-think/) | sharing and training on by default |
| [PPC Land: Chamberlain v. Granola lawsuit](https://ppc.land/granola-sued-for-recording-meetings-without-consent-to-train-ai-models/) | class action of 30 July 2026 |
| [Sierra: blog](https://sierra.ai/blog) | Agent OS 2.0, Voice Personas, Ghostwriter, fleming-1 |
| [Sierra: year two](https://sierra.ai/blog/year-two-in-review) | ARR, customers, Fortune 20, expansion |
| [Sierra: Horizon](https://sierra.ai/blog/horizon) | long-horizon agents, "you pay for outcomes" |
| [Sierra: outcome-based pricing](https://sierra.ai/blog/outcome-based-pricing-for-ai-agents) | billing model (10 December 2024) |
| [Sierra: τ-bench](https://sierra.ai/blog/benchmarking-ai-agents) | pass^k, GPT-4o drop at pass^8 |
| [Sierra: Personal Agent Protocol](https://sierra.ai/blog/introducing-personal-agent-protocol) | protocol with Meta (6 October 2026) |
| [TechCrunch, 4 May 2026 — Sierra](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/) | USD 950 m at over USD 15 bn, 40% of the Fortune 50 |
| [Forbes, November 2025 — Sierra](https://www.forbes.com/sites/richardnieva/2025/11/05/sierra-bret-taylor-clay-bavor/) | valuation of USD 10 bn |
| [Decagon: Series D](https://decagon.ai/blog/series-d-announcement) | Sierra's competitor, USD 4.5 bn |
| [Decagon: blog](https://decagon.ai/blog) | PACT protocol (6 October 2026) |
| [Intercom: pricing](https://www.intercom.com/pricing) | USD 0.99 per outcome |
| [Parloa: pricing](https://www.parloa.com/platform/pricing/) | billing per minute or per interaction |
| [Wikipedia: OpenEvidence](https://en.wikipedia.org/wiki/OpenEvidence) | features, licensed content, lawsuit against Pathway |
| [Sacra: OpenEvidence](https://sacra.com/c/openevidence/) | revenue, CPM, margin, usage, ChatGPT for Clinicians |
| [Rutland Herald: OpenEvidence round](https://www.rutlandherald.com/news/business/openevidence-raises-250-million-to-build-medical-superintelligence-for-doctors/article_0960939c-ca41-5321-8417-54f84800ece6.html) | USD 250 m at USD 12 bn (21 January 2026) |
| [Sacra: OpenEvidence vs Doximity](https://sacra.com/research/openevidence-vs-doximity/) | conflict and convergence of the products |
| [Wikipedia: Doximity](https://en.wikipedia.org/wiki/Doximity) | acquisition of Pathway (August 2025) |
| [ASCO Post: AMA survey](https://ascopost.com/news/march-2026/ama-survey-finds-rapid-growth-in-physician-ai-adoption/) | 81% of US physicians use AI (2026) |
| [Physicians Practice: AMA survey](https://www.physicianspractice.com/view/physician-ai-use-is-surging-is-your-practice-ready-) | 71% with no say in tool choice |
| [Code of Medical Ethics (PDF)](https://nil.org.pl/uploaded_images/1723037323_kel-2305.pdf) | Article 12 — AI in diagnosis and treatment |
| [Noxtua](https://www.noxtua.com/) | features, Athena and Minerva, number of documents |
| [Noxtua: security](https://www.noxtua.com/security) | hosting, self-hosting in a sovereign cloud, § 43e BRAO, § 203 StGB |
| [Noxtua: Series C](https://www.noxtua.com/news/press-releases/series-c) | EUR 100 m+ (23 September 2026), 30,000+ users, certifications |
| [TechCrunch: Noxtua Series B](https://techcrunch.com/2025/04/22/noxtua-raises-92m-for-its-sovereign-ai-tuned-for-the-german-legal-system/) | USD 92.2 m, own model 2025, Xayn history |
| [CMS: C.H.Beck becomes Noxtua investor](https://cms.law/en/deu/news-information/c.h.beck-becomes-leading-investor-in-legal-ai-noxtua) | Series B amount per CMS, working without anonymization |
| [Noxtua: Beck-Noxtua in Poland](https://www.noxtua.com/news/press-releases/beck-noxtua-poland) | announcement of 3 December 2025 |
| [Noxtua: Beck-Noxtua in the Czech Republic](https://www.noxtua.com/news/press-releases/beck-noxtua-for-the-czech-republic) | IONOS and Open Telekom Cloud hosting, BSI C5 |
| [beck-noxtua.pl](https://www.beck-noxtua.pl/) | PLN 590 net/month, Legalis Silver+ requirement, ISO certifications |
| [NRA: § 23e of the Code of Ethics](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/) | rules for advocates' use of AI |
| [Prawo o adwokaturze (Advocacy Act) (PDF)](https://api.sejm.gov.pl/eli/acts/DU/2024/1564/text.pdf) | Article 6 — advocate-client privilege |
| [Ustawa o radcach prawnych (Legal Advisers Act) (PDF)](https://api.sejm.gov.pl/eli/acts/DU/2024/499/text.pdf) | Article 3 — legal adviser privilege |
| [UODO: AI checklists](https://uodo.gov.pl/pl/138/4533) | "initial questions" before deploying AI (6 August 2026) |
| [KIRP: AI recommendations](https://kirp.pl/rekomendacje-dotyczace-korzystania-z-ai/) | recommendations for legal advisers |
| [prawo.pl: LEX Expert AI](https://www.prawo.pl/prawnicy-sady/lex-expert-ai-nowym-narzedziem-dla-prawnikow,535918.html) | competitor in Poland, links to source excerpts |
| [Gaius-Lex](https://gaius-lex.pl/) | Polish player with an on-premise deployment |
| [Mistral: September 2026 round](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/) | capital for sovereign AI in the EU |
| [TechCrunch: Cohere + Aleph Alpha](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/) | merger at USD 20 bn |

## Profiles 7, 8, 15 and "worth knowing"

As of 11 October 2026. The openai.com, chatgpt.com and perplexity.ai sites blocked downloads, so some of the facts about
OpenAI and Perplexity come from the press, the system card (PDF) and Wikipedia; I flagged this in the text.

| Source | What I took |
|---|---|
| [Engadget — DevDay 2026](https://www.engadget.com/2271985/openai-dev-day-live-blog-chatgpt-news/) | 1.2 bn weekly users, dots, Pro 500 (29 September 2026) |
| [Decrypt — DevDay 2026](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced) | 1.2 bn users, opening up the Codex harness |
| [emergent — DevDay 2026](https://emergent.sh/news/openai-devday-2026) | GPT-6 API prices, dots outside the EEA on Pro, OSWorld 2.0 Sol vs Astra |
| [eesel — dots](https://www.eesel.ai/blog/openai-dots) | a VM per dot, Custom Rules, auto-review, dots memory |
| [TechCrunch — dots](https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/) | dots on GPT-6 Astra, 4000+ apps |
| [ChatGPT agent system card](https://cdn.openai.com/pdf/839e66fc-602c-48bf-81d3-b21eacc3459d/chatgpt_agent_system_card.pdf) | agent tools, accuracy of confirmations, watch mode, memory disabled, resistance to injections |
| [digitalapplied — ChatGPT Work](https://www.digitalapplied.com/blog/chatgpt-work-openai-agent-launch-2026) | plan mode, 1400+ plugins, auto-review, usage-based billing |
| [9to5Mac — end of Atlas](https://9to5mac.com/2026/07/09/openai-is-discontinuing-chatgpt-atlas-its-standalone-desktop-browser/) | Atlas deprecation, new desktop app |
| [OpenAI forum — Atlas](https://community.openai.com/t/atlas-is-scheduled-to-stop-working-on-august-9-2026/1389473) | Atlas shutdown date 9 August 2026 |
| [36Kr — Atlas](https://eu.36kr.com/en/p/3931781634260099) | "feature, not a destination", about 10 million Atlas MAU, AI browser share < 1% |
| [9to5Mac — scheduled tasks](https://9to5mac.com/2026/06/17/openai-launches-scheduled-tasks-in-chatgpt-details-here/) | tasks, once-an-hour limit, end of Pulse |
| [Thurrott — memory](https://www.thurrott.com/a-i/337052/openai-is-improving-how-chatgpts-memory-works) | "Dreaming" from 4 June 2026 |
| [9to5Mac — Agent Plugins](https://9to5mac.com/2026/08/06/gpt-5-turning-one-as-openai-shares-new-agent-plugins-standard/) | plugin standard and committee |
| [OpenAI — computer use in the API](https://developers.openai.com/api/docs/guides/tools-computer-use) | "code instead of clicks" recommendation |
| [TechCrunch — prompt injection](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/) | RL-trained attacker, "unlikely to ever be fully solved" |
| [PinMeTo — ads in Europe](https://www.pinmeto.com/news/chatgpt-ads-31-european-markets-2026/) | ads in Poland from 24 August 2026, contextual only |
| [a16z — Top 100](https://a16z.com/100-gen-ai-apps-7/) | ads at USD 1 bn a year, subscribers 3× vs Claude and Gemini |
| [Investing.com — OpenAI ARR](https://www.investing.com/news/stock-market-news/openais-annual-recurring-revenue-nears-70-billion-axios-reports-4923088) | ARR "close to USD 70 bn" (Axios/Reuters) |
| [Bloomberg Law — OpenAI round](https://news.bloomberglaw.com/tech-and-telecom-law/openai-valued-at-852-billion-after-closing-122-billion-round) | USD 122 bn at USD 852 bn |
| [TechCrunch — Sensor Tower](https://techcrunch.com/2026/06/16/chatgpts-market-share-slips-below-50-for-first-time/) | MAU and shares of ChatGPT, Gemini, Perplexity, Grok, DeepSeek (May 2026) |
| [Hugging Face — privacy-filter](https://huggingface.co/openai/privacy-filter) | OpenAI's open PII classifier |
| [Wikipedia — ChatGPT](https://en.wikipedia.org/wiki/ChatGPT) | ChatGPT Health outside the EEA, rename to plugins |
| [Alphabet — Q2 2026 results](https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000066/googexhibit991q22026.htm) | 950 million MAU, subscriptions segment USD 12.9 bn |
| [9to5Google — I/O 2026](https://9to5google.com/2026/05/19/google-io-2026-news/) | Daily Brief, Spark, Live, Ultra prices |
| [TechCrunch — Gemini 3.5 Flash](https://techcrunch.com/2026/05/19/with-gemini-3-5-flash-google-bets-its-next-ai-wave-on-agents-not-chatbots/) | Antigravity, pauses for decisions |
| [Android Headlines — Spark in AI Pro](https://www.androidheadlines.com/2026/07/google-gemini-spark-expands-to-ai-pro-subscribers.html) | Tasks/Schedules/Skills, consent by data scope, country exclusions |
| [Google — Spark help](https://support.google.com/gemini/answer/16596215) | local vs remote Chrome, 15 tasks, outside the EEA, warnings |
| [Google — Spark July 2026](https://blog.google/innovation-and-ai/products/gemini-app/gemini-spark-updates-july-2026/) | Chrome integration, 160+ countries |
| [Efficiently Connected — Spark](https://www.efficientlyconnected.com/google-io-2026-gemini-spark-consumer-ai-agent/) | dedicated cloud VMs |
| [Google — agent security in Chrome](https://blog.google/security/architecting-security-for-agentic/) | planner + User Alignment Critic, Origin Sets, confirmations, VRP |
| [Google — auto browse](https://blog.google/products-and-platforms/products/chrome/gemini-3-auto-browse/) | auto browse features, UCP, US only |
| [Google — auto browse on Android](https://blog.google/products-and-platforms/products/chrome/gemini-in-chrome-android-auto-browse/) | Android from 18 August 2026 |
| [Google — Gemini Agent](https://blog.google/products/gemini/gemini-3-gemini-app/) | Gemini Agent from 18 November 2025 |
| [Gemini API — computer use](https://ai.google.dev/gemini-api/docs/computer-use) | loop, `safety_decision`, 7 policy categories |
| [Google — Computer Use model](https://blog.google/technology/google-deepmind/gemini-computer-use-model/) | launch on 7 October 2025, latency of about 225 s |
| [Google — Mariner](https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/) | Mariner, WebVoyager 83.5% |
| [Wikipedia — Project Mariner](https://en.wikipedia.org/wiki/Project_Mariner) | shutdown on 4 May 2026 |
| [Google — 1 bn users](https://blog.google/innovation-and-ai/products/gemini-app/one-billion-monthly-users/) | over 1 bn monthly (11 August 2026) |
| [Google — Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) | Argon API prices |
| [Gemini — prices PL](https://gemini.google/subscriptions/) · [prices US](https://gemini.google/us/subscriptions/?hl=en) | plans in zloty and dollars |
| [Business Today — Gemini replaces Assistant](https://www.businesstoday.in/amp/technology/news/story/google-assistant-to-be-replaced-by-gemini-starting-september-on-android-and-wearos-547570-2026-08-06) | replacement of Assistant from 4 September 2026 |
| [TNW — Live, Spark and the DMA](https://thenextweb.com/news/gemini-live-spark-voice-agentic-tasks-dma-rival-assistants) | Personal Intelligence, DMA deadline July 2027 |
| [9to5Google — Gems → Skills](https://9to5google.com/2026/09/27/gemini-gems-skills/) | migration on 17 November 2026 |
| [Android Developers — Gemini Nano](https://developer.android.com/ai/gemini-nano) | AICore, offline, Hybrid API |
| [Google DeepMind — Gemma](https://deepmind.google/models/gemma/) | Gemma 4 sizes |
| [TechGenyz — Gemini agent for business](https://techgenyz.com/google-gemini-agent-enterprise-ai/) | collaborator agents, routing to Claude |
| [BleepingComputer — BragJack](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/) | attack on Gemini in Chrome, Comet, Neon; CVE-2026-0628 |
| [Wikipedia — Google Gemini](https://en.wikipedia.org/wiki/Google_Gemini) | lawsuits and the fine in France |
| [VentureBeat — Portable Computer](https://venturebeat.com/infrastructure/perplexity-partners-with-nvidia-to-launch-portable-computer-a-fully-local-ai-agent-with-zero-token-costs) | architecture, models, hardware, Terminal-Bench, escalation with a PII filter |
| [VentureBeat — hybrid at Computex](https://venturebeat.com/technology/perplexity-ai-unveils-hybrid-local-cloud-inference-system-at-computex-2026) | consent before sending to the cloud |
| [TechRepublic — Portable Computer on Windows](https://www.techrepublic.com/article/news-perplexity-portable-computer-windows/) | Windows from September 2026 (teaser) |
| [Computerworld — Perplexity Computer](https://www.computerworld.com/article/4138723/perplexitys-new-computer-agent-will-run-other-agents-for-you.html) | model split, Enterprise Max USD 325 |
| [TechCrunch — Perplexity Computer](https://techcrunch.com/2026/02/27/perplexitys-new-computer-is-another-bet-that-users-need-many-ai-models/) | 19 models, Max USD 200 |
| [TechCrunch — Comet for free](https://techcrunch.com/2025/10/02/perplexitys-comet-ai-browser-now-free-max-users-get-new-background-assistant/) | free Comet, background assistant |
| [Wikipedia — Comet](https://en.wikipedia.org/wiki/Comet_(browser)) · [Perplexity AI](https://en.wikipedia.org/wiki/Perplexity_AI) | platforms, dropping ads, Azure, Personal Computer |
| [The Decoder — BrowseSafe](https://the-decoder.com/perplexitys-browsesafe-tries-to-patch-the-gaping-security-holes-inherent-in-ai-browser-agents/) | open classifier, 91% detection, about 10% leaks through |
| [PYMNTS — Perplexity revenue](https://www.pymnts.com/news/artificial-intelligence/2026/perplexitys-shift-to-ai-agents-boosts-revenue-50/) | ARR about USD 450 m in March 2026, 100 million+ MAU |
| [Yahoo Finance — Nvidia and Perplexity](https://finance.yahoo.com/technology/ai/articles/nvidia-discusses-perplexity-investment-30-031804276.html) | ARR about USD 750 m, valuation > USD 30 bn |
| [TNW — talks with Nvidia](https://thenextweb.com/news/nvidia-perplexity-30bn-valuation-talks) | no published figures |
| [TechCrunch — India](https://techcrunch.com/2026/08/18/perplexitys-free-ai-offer-left-it-with-millions-more-users-in-india/) | Airtel, MAU, app revenue |
| [Vice — Comet Plus](https://www.vice.com/en/article/perplexity-comet-plus-announced/) | Pro/Max prices, Comet Plus |
| [Jones Day — Ninth Circuit](https://www.jonesday.com/en/insights/2026/09/ninth-circuit-vacates-cfaa-injunction-against-perplexitys-comet-ai-agent) | injunction vacated, data flow in Comet |
| [Brave — Comet](https://brave.com/blog/comet-prompt-injection/) | indirect injection, recommendations |
| [LayerX — CometJacking](https://layerxsecurity.com/blog/cometjacking-how-one-click-can-turn-perplexitys-comet-ai-browser-against-you/) | exfiltration via a URL parameter |
| [The Register — PleaseFix](https://www.theregister.com/2026/03/03/perplexity_comet_browser_hole_cal_invite/) | zero-click via the calendar, patches |
| [Help Net Security — MCP API in Comet](https://www.helpnetsecurity.com/2025/11/20/perplexity-comet-browser-security-mcp-api/) | hidden extension, disabling |
| [The Register — Gartner](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/) | advice to block AI browsers |
| [Android Authority — Hey Plex](https://www.androidauthority.com/hey-perplexity-3655439/) | Perplexity in the Galaxy S26 (teaser) |
| [money.pl — Bielik and NVIDIA](https://www.money.pl/gospodarka/wielki-krok-dla-polskiego-ai-bielik-rozpoczyna-wspolprace-z-nvidia-7166523596470944a.html) | announcement of Bielik in Perplexity |
| [AMD — Radeon AI PRO R9700](https://www.amd.com/en/products/graphics/workstations/radeon-ai-pro/ai-9000-series/amd-radeon-ai-pro-r9700.html) | 32 GB per card |
| [Hugging Face — Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | 84.3% OSWorld-Verified (claim), Apache 2.0 |
| [UI-TARS-1.5-7B](https://huggingface.co/ByteDance-Seed/UI-TARS-1.5-7B) · [UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) | OSWorld results, operators, running locally |
| [TNW — Legora](https://thenextweb.com/news/legora-just-hit-100-million-in-revenue-it-took-18-months) | ARR, funding, tabular review |
| [HLTH — Heidi](https://hlth.com/insights/news/heidi-raises-340m-to-expand-clinical-ai-into-supervised-agentic-workflows) | ARR USD 50 m, USD 340 m, agents outside the UK/EU |
| [Microsoft — Copilot privacy](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) · [FY26 Q4 results](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast) | EU Data Boundary, 30 million seats |
| [Yahoo Finance — Genspark](https://finance.yahoo.com/technology/ai/articles/genspark-ai-extends-series-b-131000248.html) | ARR, valuation of USD 2.6 bn |
| [Cognition — Poke](https://cognition.com/blog/interaction) | acquisition, 100 million messages |
| [NVIDIA NemoClaw](https://github.com/NVIDIA/NemoClaw) | OpenShell sandbox, alpha status |
| [TechCrunch — Ghost](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/) | price, hardware, models, firewall |
| [PubMed — UCLA RCT](https://pubmed.ncbi.nlm.nih.gov/41497288/) | Nabla and DAX/Dragon results |
| [Nabla — ASR](https://nabla.com/blog/assessing-the-reliability-of-nablas-speech-to-text-engine) | Whisper + 7000 h of audio |
| [Basis — behavior specs](https://www.getbasis.ai/blogs/behavior-specs-an-open-standard-for-supervising-long-horizon-agents) | standard for evaluating an agent's run |
| [Hebbia — Matrix 2.0](https://www.hebbia.com/blog/introducing-matrix-2-0) | Matrix interface, checkpoints |
| [TechCrunch — Glean](https://techcrunch.com/2026/05/28/gleans-top-line-crosses-300m-as-ai-budget-cutting-becomes-its-major-selling-point/) · [ITBrief — Tau](https://itbrief.asia/story/glean-launches-tau-to-cut-enterprise-ai-token-costs) | ARR USD 300 m, cost per task |
| [Lindy — pricing](https://www.lindy.ai/pricing) · [iMessage](https://www.lindy.ai/blog/imessage-api-three-rewrites-one-apple-ban-and-what-actually-works) | approval rule, Apple ban |
| [gaius-lex.pl](https://gaius-lex.pl/) · [Signalbase](https://www.trysignalbase.com/news/funding/gaius-lex-secures-5) | Gaius Vault on-prem, seed |
| [Meta — Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) · [Muse retention](https://cryptobriefing.com/meta-muse-app-store-retention/) | Sentinel, VM, payments; 5 million downloads vs 700k DAU |
| [VentureBeat — Muse Glimmer](https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now) | model parameters and licence |
| [Amazon — Alexa+](https://www.aboutamazon.com/news/devices/new-alexa-generative-artificial-intelligence) · [countries](https://www.aboutamazon.com/news/devices/alexa-plus-international-launch) | Experts, markets without Poland |
| [TNW — Siri AI](https://thenextweb.com/news/apple-ios-27-siri-ai-release-icloud-plus-child-safety) · [Apple — languages](https://support.apple.com/en-us/121115) | iOS 27, EU, no Polish |
| [TNW — Microsoft Copilot](https://thenextweb.com/news/microsoft-copilot-mico-retired-features-killed-app-merge) · [Windows Agent Workspace](https://support.microsoft.com/en-us/windows/experimental-agentic-features-a25ede8a-e4c2-4841-85a8-44839191dfb3) | removed features, 38.5 million, agent account |
| [Wikipedia — Grok](https://en.wikipedia.org/wiki/Grok_(chatbot)) · [Finbold — Grok Bot](https://finbold.com/spacexais-grok-bot-agent-surpasses-400000-users-after-the-first-month/) | incidents, 418k users |
| [TechNode — Doubao](https://technode.com/2026/09/23/bytedance-doubao-general-session-team-cuts/) | 200 million DAU |
| [TechTimes — Qwen](https://www.techtimes.com/articles/323907/20260811/qwen-sells-paid-office-subscriptions-users-it-bought-with-free-bubble-tea.htm) | RMB 6 bn campaign, session length, MAU |
| [Hugging Face — DeepSeek](https://huggingface.co/api/models?author=deepseek-ai&sort=lastModified) · [netzpolitik](https://netzpolitik.org/2025/datenschutzbehoerde-greift-ein-deepseek-fliegt-aus-den-app-stores/) | MIT weights, demand to remove the app |
| [TechCrunch — Mistral](https://techcrunch.com/2026/09/08/mistral-raises-e3b-as-sovereign-ai-becomes-big-business/) · [pricing](https://mistral.ai/pricing) | EUR 3 bn round, Pro USD 14.99 |
| [Pulse 2.0 — Instinct](https://pulse2.com/instinct-raises-1-billion-series-c-at-10-billion-valuation/) | Series C, sandboxes, credentials |
| [NanoClaw](https://github.com/nanocoai/nanoclaw) | containers, scripted gates, Claude Agent SDK |
| [OpenManus](https://github.com/FoundationAgents/OpenManus) | framework, stars, Ollama |
| [Kortix — README](https://raw.githubusercontent.com/kortix-ai/suna/main/README.md) | sandbox per session, credential broker, licence |
| [Agent S](https://github.com/simular-ai/Agent-S) · [Simular — OSWorld 2.0](https://www.simular.ai/articles/sai-tops-osworld-2-0) | 72.6% OSWorld, 28.25% binary on OSWorld 2.0 |
| [Microsoft Research — Fara-7B](https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/) | 7B model, WebVoyager, number of steps |
| [Open-AutoGLM](https://github.com/zai-org/Open-AutoGLM) | Android control, GPU requirements |
| [Skywork Desktop](https://skywork.ai/desktop/en/index.html) · [36Kr — Kunlun](https://eu.36kr.com/en/p/3878113666724100) | local VM, ARR of the tools division |
| [Opera — free plan for agents](https://blogs.opera.com/news/2026/08/your-ai-agents-can-use-opera-neon-free-of-charge/) · [MCP](https://press.opera.com/2026/03/31/opera-neon-adds-mcp-connector/) | MCP and CLI for external agents |
| [Fellou — pricing](https://fellou.ai/pricing) · [Eko](https://github.com/FellouAI/eko) | cost per task, open framework |
| [AWS — Nova Act](https://aws.amazon.com/nova/pricing/) · [AWS blog](https://aws.amazon.com/blogs/aws/build-reliable-ai-agents-for-ui-workflow-automation-with-amazon-nova-act-now-generally-available/) | price per agent hour, code + `act()` |
| [LawNext — CoCounsel](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html) · [BNN Bloomberg](https://www.bnnbloomberg.ca/business/2026/02/24/thomson-reuters-says-one-million-professionals-using-cocounsel-shares-soar/) | Claude Agent SDK, 1 million users |
| [LexisNexis — growth](https://www.lexisnexis.com/community/pressroom/b/news/posts/legal-ai-propels-lexisnexis-to-fastest-growth-in-history) · [Protégé PL](https://www.lexisnexis.com/de-at/cee/protege-polska) | 90% of new business, offering in Poland |
| [Microsoft — FY26 Q4](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4) | Dragon Copilot, 100 million visits |
| [Wikipedia — Doximity](https://en.wikipedia.org/wiki/Doximity) · [Sacra — OpenEvidence](https://sacra.com/c/openevidence/) | Doximity's reach, ChatGPT for Clinicians |
| [Cognition — USD 1 bn run-rate](https://cognition.com/blog/1b-run-rate) | Devin's run-rate |
| [VKTR — Lovable](https://www.vktr.com/ai-platforms/lovable-raises-400-million-at-133-billion-valuation/) | ARR, valuation |
| [Decagon — Series D](https://decagon.ai/blog/series-d-announcement) | AOP, valuation of USD 4.5 bn |

## Market (02-MARKET.md)

| Source | What I took |
|---|---|
| [menlovc.com](https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/) | Menlo Ventures (analyst), 9 December 2025: USD 37 bn of enterprise spending on genAI, coding 55% of departmental spending |
| [menlovc.com](https://menlovc.com/perspective/2025-the-state-of-ai-in-healthcare/) | Menlo Ventures, 21 October 2025: AI in healthcare USD 1.4 bn, scribes USD 600 m, DAX/Abridge/Ambience shares |
| [emergent.sh](https://emergent.sh/news/openai-devday-2026) | blog: ChatGPT Pro 500 (USD 500), dots without the EEA, DevDay 29 September 2026 |
| [decrypt.co](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced) | press: 1.2 bn weekly ChatGPT users (29 September 2026) |
| [claude.com](https://claude.com/blog/cowork-research-preview) | Anthropic: Pro/Max/Team prices |
| [gemini.google](https://gemini.google/subscriptions/) | Google: AI Plus/Pro/Ultra prices in zloty (October 2026) |
| [vice.com](https://www.vice.com/en/article/perplexity-comet-plus-announced/) | press: Perplexity Pro USD 20, Max USD 200 (August 2025) |
| [poke.com](https://poke.com/pricing) | Poke: Pro USD 19, Ultra USD 199 (11 October 2026) |
| [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/) | Nous: Nous Portal tiers USD 20/100/200 |
| [mistral.ai](https://mistral.ai/fr/pricing) | Mistral: Vibe Pro EUR 14.99, Team EUR 24.99 excl. VAT |
| [pymnts.com](https://www.pymnts.com/news/artificial-intelligence/2026/perplexitys-shift-to-ai-agents-boosts-revenue-50/) | press: Perplexity ARR USD 450 m and 100 million+ MAU (March 2026) |
| [finance.yahoo.com](https://finance.yahoo.com/technology/ai/articles/nvidia-discusses-perplexity-investment-30-031804276.html) | The Information via Yahoo: ARR about USD 750 m, talks with NVIDIA at >USD 30 bn (August 2026) |
| [help.manus.im](https://help.manus.im/en/articles/11711097-what-are-the-rules-for-credits-consumption-and-how-can-i-obtain-them) | Manus: credit rules (tokens + machine + API, order of consumption) |
| [myclaw.ai](https://myclaw.ai/blog/manus-2-0) | review: Manus prices USD 20/40/200 (September 2026), credit price calculation |
| [genspark.ai](https://www.genspark.ai/helpcenter/membership-plans) | Genspark: Plus/Pro/Team tiers, credits |
| [lindy.ai](https://www.lindy.ai/pricing) | Lindy: USD 49.99 per user, 5,000 credits, pause when the pool runs out, consent rule |
| [fellou.ai](https://fellou.ai/pricing) | Fellou: tiers and about 250 Sparks per task |
| [browser-use.com](https://browser-use.com/pricing.md) | browser-use: USD 0.02 per browser hour, cost per task |
| [aws.amazon.com](https://aws.amazon.com/nova/pricing/) | AWS: Nova Act USD 4.75 per agent hour |
| [rabbit.tech](https://www.rabbit.tech/newsroom/rabbit-intern-launch) | Rabbit: intern USD 99.99 for 30 tasks, "per task" price |
| [cursor.com](https://cursor.com/blog/june-2025-pricing) | Cursor: pricing change of 16 June 2025 and apology of 4 July 2025 |
| [techcrunch.com](https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/) | press: weekly Claude Code limits from 28 August 2025 |
| [docs.github.com](https://docs.github.com/en/copilot/concepts/billing/copilot-requests) | GitHub docs: AI credits from 1 June 2026 |
| [github.com](https://github.com/features/copilot/plans) | GitHub: Copilot tiers and credits included in the price |
| [techcrunch.com](https://techcrunch.com/2026/05/28/gleans-top-line-crosses-300m-as-ai-budget-cutting-becomes-its-major-selling-point/) | press: Glean USD 300 m, flat fee + usage model |
| [notion.com](https://www.notion.com/pricing) | Notion: Custom Agents USD 10 per 1,000 credits |
| [gartner.com](https://www.gartner.com/en/newsroom/press-releases/2026-08-17-gartner-predicts-ai-inference-costs-per-agentic-workflow-will-increase-more-than-fivefold-through-2028) | Gartner, 17 August 2026: cost per agentic workflow ×5 by 2028 |
| [sierra.ai](https://sierra.ai/blog/outcome-based-pricing-for-ai-agents) | Sierra: outcome-based payment rules (10 December 2024) |
| [sierra.ai](https://sierra.ai/blog/horizon) | Sierra: "you pay for outcomes, not for tokens" |
| [intercom.com](https://www.intercom.com/pricing) | Intercom: Fin USD 0.99 per outcome |
| [parloa.com](https://www.parloa.com/platform/pricing/) | Parloa: billing per minute or per interaction |
| [ambiencehealthcare.com](https://www.ambiencehealthcare.com/blog) | Ambience: contracts with an outcome bonus (April 2026) |
| [sierra.ai](https://sierra.ai/blog/year-two-in-review) | Sierra: ARR 100 → 150 m+ USD, narrow "jobs to be done" |
| [sacra.com](https://sacra.com/c/openevidence/) | Sacra (analyst): OpenEvidence revenue, CPM, margin |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/OpenEvidence) | encyclopedia: licensed NEJM, JAMA, NCCN content |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Doximity) | encyclopedia: Doximity funded by pharma marketing |
| [openclaw.ai](https://openclaw.ai/blog/introducing-openclaw-foundation) | OpenClaw Foundation: 501(c)(3), donors, "4.5 million claws a week" |
| [openclaw.ai](https://openclaw.ai/blog/openclaw-enterprise) | OpenClaw Enterprise "always free" (29 September 2026) |
| [portal.nousresearch.com](https://portal.nousresearch.com/business) | Nous: Hermes Business and Enterprise |
| [manus.im](https://manus.im/blog/introducing-manus-flex) | Manus Flex: bring your own model key (29 September 2026) |
| [kortix.com](https://www.kortix.com/pricing) | Kortix: credits for the sandbox only, BYOK |
| [openhands.dev](https://openhands.dev/pricing) | OpenHands: models "at cost, no markup" |
| [agent-zero.ai](https://www.agent-zero.ai/p/token/) | Agent Zero: A0T token as financing |
| [github.com](https://github.com/HKUDS/nanobot) | nanobot: affiliate links to model providers |
| [vaquill.ai](https://www.vaquill.ai/blog/harvey-ai-review-honest-assessment) | external estimate: Harvey seat price |
| [layer3labs.io](https://www.layer3labs.io/guides/legora-pricing) | external estimate: Legora seat price |
| [sacra.com](https://sacra.com/c/abridge/) | Sacra: Abridge about USD 2,500 per physician per year, ARR |
| [legal.thomsonreuters.com](https://legal.thomsonreuters.com/en/products/cocounsel-legal/plans) | Thomson Reuters: CoCounsel in bundles with Westlaw |
| [lawnext.com](https://www.lawnext.com/2026/04/clio-work-clios-ai-workspace-is-now-available-to-solo-and-smaller-law-firms-as-a-standalone-product.html) | LawSites: Clio Work USD 199 per user |
| [bluej.com](https://www.bluej.com/pricing) | Blue J: USD 1,498 a year |
| [microsoft.com](https://www.microsoft.com/en-us/microsoft-365-copilot/pricing) | Microsoft: Copilot Business USD 18–21 |
| [github.com](https://github.com/openclaw/openclaw) | GitHub: OpenClaw repository (stars, security reports via the API, 11 October 2026) |
| [anthropic.com](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation) | Anthropic: Series G USD 30 bn at USD 380 bn, run-rate USD 14 bn, Claude Code >USD 2.5 bn (12 February 2026) |
| [itiger.com](https://www.itiger.com/hans/news/1183910360) | secondary press: Anthropic run-rate about USD 44 bn (May 2026, SemiAnalysis) |
| [mobihealthnews.com](https://www.mobihealthnews.com/news/abridge-secures-300m-boosts-valuation-53b) | press: Abridge Series E at USD 5.3 bn |
| [fortune.com](https://fortune.com/2026/06/11/abridge-operating-system-medicine-nvidia-eli-lilly-artsight/) | press: Abridge as a "platform", customer scale (June 2026) |
| [harvey.ai](https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence) | Harvey: USD 550 m at USD 15.5 bn, 80% of the Am Law 100 (9 September 2026) |
| [itbrief.co.uk](https://itbrief.co.uk/story/harvey-launches-500-legal-ai-agents-builder-tool) | press: Harvey 1,500 organizations, 100k+ lawyers (May 2026) |
| [raising.fi](https://raising.fi/news/harvey-undisclosed-september-2026) | secondary press: Harvey ARR >USD 400 m (September 2026) |
| [nousresearch.com](https://nousresearch.com/a-note-on-our-fundraise) | Nous: USD 90 m, "24 million clones", "2.5% of tokens" (October 2026) |
| [github.com](https://github.com/NousResearch/hermes-agent) | GitHub: Hermes Agent repository |
| [manus.im](https://manus.im/blog/manus-100m-arr) | Manus: USD 100 m ARR, 147 trillion tokens, 80 million computers (December 2025) |
| [sacra.com](https://sacra.com/c/manus) | Sacra: Manus about USD 450 m annualized (June 2026), share buyback |
| [techcrunch.com](https://techcrunch.com/2026/10/08/chinas-manus-raises-over-500m-in-first-funding-round-since-split-with-meta/) | press: Manus round >USD 500 m (8 October 2026) |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/ChatGPT) | encyclopedia: 900 million weekly users (February 2026) |
| [blog.google](https://blog.google/innovation-and-ai/products/gemini-app/one-billion-monthly-users/) | Google: Gemini 1 bn+ monthly (11 August 2026) |
| [bloomberg.com](https://www.bloomberg.com/news/articles/2026-03-02/cursor-recurring-revenue-doubles-in-three-months-to-2-billion) | press: Cursor ARR USD 2 bn |
| [cursor.com](https://cursor.com/blog/joining-spacex) | Cursor: joining SpaceX |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Cursor_%28company%29) | encyclopedia: SpaceX deal timeline, ARR USD 3 bn (May 2026) |
| [thenextweb.com](https://thenextweb.com/news/granola-series-c-meeting-ai-enterprise-context) | press: Granola Series C USD 125 m at USD 1.5 bn |
| [arr.club](https://www.arr.club/granola/granola-arr-grow-at-250-in-q1-2026) | aggregator: Granola ARR growth in Q1 2026 |
| [techcrunch.com](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/) | press: Sierra USD 950 m at >USD 15 bn |
| [rutlandherald.com](https://www.rutlandherald.com/news/business/openevidence-raises-250-million-to-build-medical-superintelligence-for-doctors/article_0960939c-ca41-5321-8417-54f84800ece6.html) | press: OpenEvidence USD 250 m at USD 12 bn |
| [felicis.com](https://felicis.com/blog/browser-use-the-tool-making-it-easier-for-ai-agents-to-navigate-websites-raises-17m) | Felicis: browser-use seed USD 17 m |
| [github.com](https://github.com/browser-use/browser-use) | GitHub: browser-use repository |
| [noxtua.com](https://www.noxtua.com/news/press-releases/series-c) | Noxtua: Series C EUR 100 m+, 30,000+ users |
| [techcrunch.com](https://techcrunch.com/2025/04/22/noxtua-raises-92m-for-its-sovereign-ai-tuned-for-the-german-legal-system/) | press: Noxtua Series B USD 92.2 m |
| [beck-noxtua.pl](https://www.beck-noxtua.pl/) | Beck-Noxtua: PLN 590 net, Legalis Silver requirement, certifications |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Perplexity_AI) | encyclopedia: Perplexity valuation about USD 20 bn (September 2025) |
| [thenextweb.com](https://thenextweb.com/news/legora-just-hit-100-million-in-revenue-it-took-18-months) | press: Legora USD 100 m ARR in 18 months, funding |
| [runtimewire.com](https://runtimewire.com/article/legora-funding-talks-8-5-billion-valuation) | secondary press: Legora >USD 200 m ARR, valuation talks |
| [aol.com](https://www.aol.com/articles/genspark-unveils-ai-workspace-6-150700000.html) | press: Genspark about USD 250 m ARR |
| [finance.yahoo.com](https://finance.yahoo.com/technology/ai/articles/genspark-ai-extends-series-b-131000248.html) | press: Genspark USD 485 m at USD 2.6 bn (17 June 2026) |
| [microsoft.com](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast) | Microsoft IR: 30 million+ paid Copilot seats |
| [getpanto.ai](https://www.getpanto.ai/blog/github-statistics) | secondary source: 4.7 million paid GitHub Copilot |
| [cognition.com](https://cognition.com/blog/1b-run-rate) | Cognition: run-rate USD 1 bn (25 September 2026) |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Cognition_AI) | encyclopedia: Cognition valuations, Windsurf history |
| [vktr.com](https://www.vktr.com/ai-platforms/lovable-raises-400-million-at-133-billion-valuation/) | press: Lovable USD 400 m at USD 13.3 bn |
| [hlth.com](https://hlth.com/insights/news/heidi-raises-340m-to-expand-clinical-ai-into-supervised-agentic-workflows) | press: Heidi ARR USD 50 m, USD 340 m round (September 2026) |
| [heidihealth.com](https://www.heidihealth.com/blog/heidi-series-b) | Heidi: Series B (October 2025) |
| [cognition.com](https://cognition.com/blog/interaction) | Cognition: acquisition of Poke, >100 million messages |
| [techcrunch.com](https://techcrunch.com/2026/04/08/poke-makes-ai-agents-as-easy-as-sending-a-text/) | press: Poke USD 300 m after the round, "recipes", creator compensation |
| [mistral.ai](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/) | Mistral: EUR 3 bn at >EUR 21 bn |
| [techcrunch.com](https://techcrunch.com/2026/02/13/coheres-240m-year-sets-stage-for-ipo/) | press: Cohere ARR USD 240 m (2025) |
| [techcrunch.com](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/) | press: Cohere + Aleph Alpha, USD 20 bn, Schwarz USD 600 m |
| [thelogic.co](https://thelogic.co/news/clio-series-g-5-billion-legal-tech) | press: Clio buys vLex for USD 1 bn, Series G |
| [finance.yahoo.com](https://finance.yahoo.com/news/meta-acquire-chinese-startup-manus-233905821.html) | press: Meta acquires Manus (December 2025) |
| [techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/) | press: Steinberger at OpenAI |
| [anthropic.com](https://www.anthropic.com/news/acquires-vercept) | Anthropic: acquisition of Vercept |
| [techcrunch.com](https://techcrunch.com/2026/03/10/meta-acquired-moltbook) | press: Meta buys Moltbook |
| [cohere.com](https://cohere.com/blog/cohere-and-aleph-alpha-sign-agreement) | Cohere: agreement with Aleph Alpha (16 September 2026) |
| [techcrunch.com](https://techcrunch.com/2026/04/27/china-vetoes-metas-2b-manus-deal-after-months-long-probe/) | press: NDRC blocks the Manus acquisition (27 April 2026) |
| [dahuilawyers.com](https://www.dahuilawyers.com/en/news-insights/chinas-first-public-foreign-investment-security-review-prohibition-the-metamanus-decision/) | law firm: first public prohibition in a Chinese security review |
| [manus.im](https://manus.im/blog/a-note-to-our-users) | Manus: independence, data deletion, data in the US and Singapore |
| [manus.im](https://manus.im/blog/manus-resumes-independent-operations) | Manus: formal independence (1 September 2026) |
| [thenextweb.com](https://thenextweb.com/news/tandem-health-100m-series-b-scaleup-europe-fund) | press: Tandem USD 100 m from the Scaleup Europe Fund, MDR IIa |
| [openclaw.ai](https://openclaw.ai/blog/microsoft-autopilot-openclaw) | OpenClaw: Microsoft Autopilot on OpenClaw (25 September 2026) |
| [sierra.ai](https://sierra.ai/blog/introducing-personal-agent-protocol) | Sierra: Personal Agent Protocol with Meta (6 October 2026) |
| [blog.google](https://blog.google/products-and-platforms/products/chrome/gemini-in-chrome-android-auto-browse/) | Google: auto browse in Chrome on Android (18 August 2026) |
| [eu.36kr.com](https://eu.36kr.com/en/p/3931781634260099) | press: AI browsers <1% of the market, Chrome about 2/3 (August 2026) |
| [techcrunch.com](https://techcrunch.com/2026/06/04/apple-approves-poke-as-the-first-ai-agent-on-its-messages-for-business-platform/) | press: Poke the first agent on Apple Messages for Business |
| [docs.openclaw.ai](https://docs.openclaw.ai/llms.txt) | OpenClaw documentation: list of messengers in the gateway |
| [hlth.com](https://hlth.com/insights/news/epic-releases-native-ai-charting-for-integrated-clinical-documentation-2026-02-06) | press: Epic AI Charting (February 2026) |
| [lexisnexis.com](https://www.lexisnexis.com/community/pressroom/b/news/posts/legal-ai-propels-lexisnexis-to-fastest-growth-in-history) | LexisNexis: AI is 90% of new sales |
| [prawo.pl](https://www.prawo.pl/prawnicy-sady/wolters-kluwer-przejmuje-libre-dostawce-rozwiazan-ai-dla-prawnikow,535867.html) | press: Wolters Kluwer and legal content in Poland |
| [harvey.ai](https://www.harvey.ai/blog/post-training-update-harvey-tenet) | Harvey: Tenet on Kimi K3, cost about 1/10 |
| [cursor.com](https://cursor.com/blog/composer-2) | Cursor: Composer 2, prices and results |
| [gigazine.net](https://gigazine.net/gsc_news/en/20260323-cursor-admits-composer-2-kimi) | press: Composer 2 built on Kimi K2.5 |
| [lawnext.com](https://www.lawnext.com/2026/08/thomson-reuters-says-its-homegrown-ai-model-now-rivals-the-frontier-labs-i-take-a-closer-look-at-the-benchmarks.html) | LawSites: "Thomson" model on an open base |
| [noxtua.com](https://www.noxtua.com/) | Noxtua: Athena (open models) and Minerva tiers |
| [bandt.com.au](https://www.bandt.com.au/canva-slashes-revenue-forecast-due-to-ai-spend-being-higher-than-expected/) | press: Canva cuts its forecast over AI costs, own models 17–30× cheaper |
| [harvey.ai](https://www.harvey.ai/blog/building-harveys-mcp-policy-engine) | Harvey: MCP Policy Engine |
| [dgft.nhs.uk](https://www.dgft.nhs.uk/newspost/nhs-launches-largest-ever-procurement-of-ai-clinical-documentation-covering-70000-midlands-clinicians/) | NHS: framework for 70,000 clinicians |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Rabbit_r1) | encyclopedia: Rabbit r1, sales, key leaks |
| [theverge.com](https://www.theverge.com/2024/9/25/24254253/rabbit-r1-5000-daily-users-ai-gadget) | press: about 5,000 active out of ~100,000 r1 owners |
| [techcrunch.com](https://techcrunch.com/2025/05/05/11x-ceo-hasan-sukkar-steps-down/) | press: 11x, fake logos, CEO departure |
| [techcrunch.com](https://techcrunch.com/2026/01/07/yes-linkedin-banned-ai-agent-startup-artisan-but-now-its-back/) | press: Artisan's LinkedIn ban |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Replit) | encyclopedia: Replit's agent deleted a production database (July 2025) |
| [uctoday.com](https://uctoday.com/productivity-automation/otter-ai-fails-to-dismiss-core-privacy-claims-in-u-s-court/) | press: claims against Otter survived (13 August 2026) |
| [ppc.land](https://ppc.land/granola-sued-for-recording-meetings-without-consent-to-train-ai-models/) | press: lawsuit against Granola (30 July 2026) |
| [insiderllm.com](https://insiderllm.com/guides/openclaw-clawhub-security-alert/) | secondary source: audits of malicious skills in ClawHub |
| [theregister.com](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) | press: OpenClaw 2.0, unencrypted secrets, sandbox disabled |
| [lindy.ai](https://www.lindy.ai/blog/imessage-api-three-rewrites-one-apple-ban-and-what-actually-works) | Lindy: Apple ID ban over iMessage |
| [community.openai.com](https://community.openai.com/t/atlas-is-scheduled-to-stop-working-on-august-9-2026/1389473) | OpenAI forum: Atlas stops working on 9 August 2026 |
| [techcrunch.com](https://techcrunch.com/2026/07/09/openai-is-shutting-down-atlas-but-its-ai-browser-ambitions-are-still-growing/) | press: Atlas shutdown announced on 9 July 2026 |
| [en.wikipedia.org](https://en.wikipedia.org/wiki/Project_Mariner) | encyclopedia: end of Project Mariner on 4 May 2026 |
| [trymartin.com](https://www.trymartin.com/blog) | Martin: last post on 23 April 2025 (stagnation) |
| [embracethered.com](https://embracethered.com/blog/posts/2025/manus-ai-kill-chain-expose-port-vs-code-server-on-internet/) | security blog: injection via PDF in Manus |
| [promptarmor.com](https://www.promptarmor.com/resources/claude-cowork-exfiltrates-files) | security blog: file leak in Claude Cowork |
| [damiencharlotin.com](https://www.damiencharlotin.com/hallucinations/) | database of cases with AI hallucinations (10 October 2026) |
| [lindy.ai](https://www.lindy.ai/blog/ai-teammate) | Lindy: shift towards a "teammate in Slack" (31 August 2026) |
| [claude.com](https://claude.com/resources/articles/how-people-are-using-claude-cowork) | Anthropic: what people use Cowork for (July 2026) |
| [techcrunch.com](https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/) | press: ChatGPT dots |
| [manus.im](https://manus.im/blog/introducing-manus-2-0) | Manus 2.0: Cloud Computer, automations (28 September 2026) |
| [support.google.com](https://support.google.com/gemini/answer/16596215) | Google: Gemini Spark, 15 tasks, EEA exclusion |
| [blog.cloudflare.com](https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/) | Cloudflare: "flood of Mac mini purchases" (January 2026) |
| [techcrunch.com](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/) | press: Ghost, an AI computer for USD 3,499 |
| [huggingface.co](https://huggingface.co/Qwen/Qwen3.8-27B) | model card: Qwen3.8-27B 84.3% OSWorld-Verified (company data) |
| [digital-strategy.ec.europa.eu](https://digital-strategy.ec.europa.eu/en/policies/cloud-and-ai-development-act) | European Commission: the CADA proposal and sovereignty levels |
| [learn.microsoft.com](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) | Microsoft docs: EU Data Boundary without Anthropic models |
| [theregister.com](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/) | press: Gartner recommends blocking AI browsers (8 December 2025) |
| [techcrunch.com](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/) | press: OpenAI on the persistence of prompt injection |
| [bankinfosecurity.com](https://www.bankinfosecurity.com/akamai-to-buy-layerx-for-205m-to-expand-ai-browser-security-a-31695) | press: Akamai buys LayerX for about USD 205 m |
| [jonesday.com](https://www.jonesday.com/en/insights/2026/09/ninth-circuit-vacates-cfaa-injunction-against-perplexitys-comet-ai-agent) | law firm: Amazon v. Perplexity, injunction vacated (4 August 2026) |
| [business-standard.com](https://www.business-standard.com/world-news/bytedance-ai-phone-doubao-nubia-zte-app-blocks-user-control-china-125120800459_1.html) | press: blocking of the Doubao agent in Chinese apps |
| [techcrunch.com](https://techcrunch.com/2026/05/12/the-ai-legal-services-industry-is-heating-up-anthropic-is-getting-in-on-the-action/) | press: Claude for Legal (12 May 2026) |
| [lawnext.com](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html) | LawSites: the new CoCounsel on the Claude Agent SDK |
| [noxtua.com](https://www.noxtua.com/news/press-releases/beck-noxtua-for-the-czech-republic) | Noxtua: Beck-Noxtua hosting on IONOS and Open Telekom Cloud |
| [apps.apple.com](https://apps.apple.com/pl/app/lex-ai/id6748342467?l=pl) | App Store: LEX AI prices PLN 49/120/489, servers in Poland |
| [noa.ai](https://www.noa.ai/pl/cennik) | Noa: Noa Notes PLN 199 + VAT |
| [wfirma.pl](https://wfirma.pl/) | wFirma: AI features included in the subscription price |
| [gaius-lex.pl](https://gaius-lex.pl/) | Gaius-Lex: Gaius Vault on-premise, no price list |
| [manus.im](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) | Manus: token ratio 100:1, about 50 calls per task, cache about 10× cheaper |
| [anthropic.com](https://www.anthropic.com/news/claude-opus-5-5) | Anthropic: Opus 5.5 prices USD 4/20 per million tokens |
| [simular.ai](https://www.simular.ai/articles/sai-tops-osworld-2-0) | Simular: cost of long OSWorld 2.0 tasks (company data) |
| [stat.gov.pl](https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultaktualnosci/5497/1/19/1/spoleczenstwo_informacyjne_w_polsce_2025.pdf) | GUS (Statistics Poland): 8.7% of firms use AI, 23.2% in professional services (2025) |
| [ec.europa.eu](https://ec.europa.eu/eurostat/statistics-explained/index.php/Use_of_artificial_intelligence_in_enterprises) | Eurostat: AI in EU firms 19.95%, adoption barriers (2025) |
| [pie.net.pl](https://pie.net.pl/wp-content/uploads/2025/09/2025-09-22_Z-AI-korzysta-mniej-niz-co-szosta-firma-w-Polsce-a-pozostale-nie-planuja-jej-wdrazac-1.pdf) | PIE: 77% of firms without AI will not adopt it "until they have to" |
| [stackoverflow.co](https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/) | Stack Overflow 2025: trust in AI 26% in Poland |
| [ceneo.pl](https://www.ceneo.pl/;szukaj-radeon+ai+pro+r9700) | Radeon AI PRO R9700 prices in Poland, about PLN 8,900 (11 October 2026) |
| [amd.com](https://www.amd.com/en/products/graphics/workstations/radeon-ai-pro/ai-9000-series/amd-radeon-ai-pro-r9700.html) | AMD: R9700, 300 W TBP |
| [ceneo.pl](https://www.ceneo.pl/;szukaj-ascent+gx10) | ASUS Ascent GX10 from PLN 24,499 (11 October 2026) |
| [apple.com](https://www.apple.com/pl/shop/buy-mac/mac-mini) | Mac mini M5 Pro from PLN 8,499 |
| [ceneo.pl](https://www.ceneo.pl/;szukaj-ryzen+ai+max%2B+395+128gb) | Strix Halo mini PC 128 GB, PLN 13,490–19,999 |

## Technical patterns (03-TECHNICAL-PATTERNS.md)

Checked by the research team on 11 October 2026 (files `research/2–6`); company data is flagged in the text *(company data)*.

| Source | What I took |
|---|---|
| [Manus: Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) | six context rules, KV-cache as the main metric, `todo.md`, input-to-output ratio ~100:1 |
| [Manus: Browser Operator](https://manus.im/blog/manus-browser-operator) · [Cloud Browser](https://manus.im/docs/features/cloud-browser.md) | local browser as the actuator, logging every action, "Take Over", banking through the local browser |
| [E2B: how Manus uses E2B](https://e2b.dev/blog/how-manus-uses-e2b-to-provide-agents-with-virtual-computers) | Firecracker micro-VMs ~150 ms, dropping Docker |
| [Harvey: multi-model by design](https://www.harvey.ai/en-US/blog/why-harvey-is-multi-model-by-design) | per-task routing, failover, administrator's model list, BigLaw Bench |
| [Harvey: Tenet](https://www.harvey.ai/blog/post-training-update-harvey-tenet) | Kimi K3 + RL, no client data, cell cost ~1/10, −90% per query |
| [Harvey II](https://www.harvey.ai/blog/introducing-harvey-ii) | matter "Spaces" |
| [Harvey: MCP Policy Engine](https://www.harvey.ai/blog/building-harveys-mcp-policy-engine) | "lethal trifecta", tool pinning, Rego, Unicode sanitizer outside the model |
| [Google: security architecture of the agent in Chrome](https://blog.google/security/architecting-security-for-agentic/) | goal-alignment critic, Agent Origin Sets, deterministic confirmations, work log |
| [Gemini API: computer use](https://ai.google.dev/gemini-api/docs/computer-use) | `safety_decision`, 7 policy categories |
| [Google: Gemini Spark](https://support.google.com/gemini/answer/16596215) | handing over login and payments, unavailable in the EEA |
| [Google: CC](https://blog.google/technology/google-labs/cc-ai-agent/) | a daily e-mail as the interface |
| [OpenClaw: Microsoft Autopilot](https://openclaw.ai/blog/microsoft-autopilot-openclaw) | policy-compliance check, masking secrets in approvals, "unknown outcome — no retry" |
| [OpenClaw docs: heartbeat](https://docs.openclaw.ai/gateway/heartbeat) · [standing orders](https://docs.openclaw.ai/automation/standing-orders) · [dreaming](https://docs.openclaw.ai/concepts/dreaming) · [workspace](https://docs.openclaw.ai/concepts/agent-workspace) · [local models](https://docs.openclaw.ai/gateway/local-models) · [index](https://docs.openclaw.ai/llms.txt) | 30-minute heartbeat and wake-up limits, programme contract, memory in files, no hard sandbox, offline work, channels |
| [OpenClaw: security in public](https://openclaw.ai/blog/openclaw-security-in-public) · [ClawScan](https://openclaw.ai/blog/tencent-aig-joins-clawscan) | report statistics (1,309 / 746 / 87%), skill scanning |
| [The Register: OpenClaw 2.0](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492) | sandbox still not the default |
| [Cisco: OpenClaw security nightmare](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare) | 26% of 31,000 skills vulnerable, exfiltration via `curl` |
| [Hermes docs: memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) · [skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) | limits of 2,200 / 1,375 characters, frozen snapshot, skills scanned at install |
| [OpenHands: condenser](https://openhands.dev/blog/openhands-context-condensensation-for-more-efficient-ai-agents) · [runtime](https://docs.openhands.dev/usage/architecture/runtime) · [security](https://docs.openhands.dev/sdk/guides/security) | context condensation, event stream, `ConfirmRisky` and risk analyzers |
| [digitalapplied: ChatGPT Work](https://www.digitalapplied.com/blog/chatgpt-work-openai-agent-launch-2026) | "Plan mode" as the consent boundary |
| [Decrypt: DevDay 2026](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced) | opening up the Codex harness |
| [TechCrunch: ChatGPT Pulse](https://techcrunch.com/2025/09/25/openai-launches-chatgpt-pulse-to-proactively-write-you-morning-briefs/) | overnight brief |
| [Claude: browser use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) · [computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) | accessibility tree, element references, screenshot cost of 1,000–1,800 tokens |
| [Simon Willison: Claude Cowork](https://simonwillison.net/2026/Jan/12/claude-cowork/) | local VM, mounting selected folders |
| [PromptArmor: Cowork exfiltration](https://www.promptarmor.com/resources/claude-cowork-exfiltrates-files) | exfiltration via an allowed API |
| [Claude for Chrome](https://claude.com/blog/claude-for-chrome) · [Anthropic: prompt injection defenses](https://www.anthropic.com/research/prompt-injection-defenses) | confirmations before publishing and purchasing; 23.6% → 11.2%, ~1% for Opus 4.5 |
| [Claude: memory](https://claude.com/resources/articles/claudes-memory-works-everywhere-and-you-decide-whats-in-it) | memory in topic files, sensitive topics not saved by default |
| [Claude Code: data usage](https://code.claude.com/docs/en/data-usage) | credentials outside the VM, traffic proxy |
| [browser-use: ain.ua](https://en.ain.ua/2025/03/25/browser-use-raises-17m) · [CDP changelog](https://browser-use.com/changelog/19-8-2025) · [Agency changelog](https://browser-use.com/changelog/3-4-2026) · [docs](https://docs.browser-use.com/cloud/choosing-an-agent) · [BU 2.0](https://docs.browser-use.com/open-source/bu-2-0-model-card) · [WebVoyager report](https://browser-use.com/posts/sota-technical-report) | "text first", CDP, approvals only before an external action, secret bindings, cloud-only features, 89.1% after removing 55 tasks |
| [HAL: Online-Mind2Web](https://hal.cs.princeton.edu/online_mind2web) | independent 40.0% for browser-use + Sonnet 4 |
| [UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) · [UI-TARS-1.5-7B](https://huggingface.co/ByteDance-Seed/UI-TARS-1.5-7B) | GUI vision model, GUI + DOM hybrid, event browser, ~27.5% OSWorld for 7B |
| [Agent S](https://github.com/simular-ai/Agent-S) | separate "where to click" model, choosing the best run, 72.6% OSWorld |
| [MSR: Fara-7B](https://www.microsoft.com/en-us/research/blog/fara-7b-an-efficient-agentic-model-for-computer-use/) | training a small model on synthetic trajectories |
| [Microsoft: agent workspace](https://support.microsoft.com/en-us/windows/experimental-agentic-features-a25ede8a-e4c2-4841-85a8-44839191dfb3) | separate Windows account for the agent, six folders |
| [Microsoft 365 Copilot: privacy](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) | Anthropic models outside the EU Data Boundary |
| [Jones Day: Amazon v. Perplexity](https://www.jonesday.com/en/insights/2026/09/ninth-circuit-vacates-cfaa-injunction-against-perplexitys-comet-ai-agent) | local execution, cloud reasoning in Comet |
| [the-decoder: BrowseSafe](https://the-decoder.com/perplexitys-browsesafe-tries-to-patch-the-gaping-security-holes-inherent-in-ai-browser-agents/) | 91% detection, ~10% of attacks get through |
| [TechCrunch: Perplexity Computer](https://techcrunch.com/2026/02/27/perplexitys-new-computer-is-another-bet-that-users-need-many-ai-models/) | 19 models with sub-agents |
| [NVIDIA NemoClaw](https://github.com/NVIDIA/NemoClaw) · [NanoClaw](https://github.com/nanocoai/nanoclaw) | sandbox by default and egress approval; container per agent, scripted gates, credential gate |
| [Kortix README](https://raw.githubusercontent.com/kortix-ai/suna/main/README.md) | credential broker with a single token |
| [Lindy: pricing](https://www.lindy.ai/pricing) · [Lindy: iMessage](https://www.lindy.ai/blog/imessage-api-three-rewrites-one-apple-ban-and-what-actually-works) | approvals by external impact; Apple ID block, ratio ~10:1 |
| [TechCrunch: Poke recipes](https://techcrunch.com/2026/04/08/poke-makes-ai-agents-as-easy-as-sending-a-text/) · [TechCrunch: Poke in Apple Messages](https://techcrunch.com/2026/06/04/apple-approves-poke-as-the-first-ai-agent-on-its-messages-for-business-platform/) · [Cognition](https://cognition.com/blog/interaction) | text recipes, first agent in Messages for Business, >100 million messages |
| [LexisNexis: Protégé](https://www.lexisnexis.com/community/pressroom/b/news/posts/lexis-with-protege-accelerates-frictionless-agentic-productivity-from-first-idea-to-review-ready-legal-work-product) | partner skills, customers "soon" |
| [Spellbook](https://www.spellbook.com/press) · [LawNext: Spellbook](https://www.lawnext.com/2025/08/spellbook-becomes-one-of-the-first-legal-ai-platforms-to-launch-gpt-5.html) | Word plugin; share of accepted suggestions as a metric |
| [Noxtua](https://www.noxtua.com/) · [Noxtua security](https://www.noxtua.com/security) | Athena / Minerva, EU sovereign cloud, Word and Outlook plugins |
| [Nabla: STT reliability](https://nabla.com/blog/assessing-the-reliability-of-nablas-speech-to-text-engine) | Whisper + 7,000 h of medical audio, the raw transcript does not reach the records |
| [Abridge: confabulation elimination](https://www.abridge.com/ai/science-confabulation-hallucination-elimination) | Linked Evidence, guard 97% vs 82% |
| [Wikipedia: OpenEvidence](https://en.wikipedia.org/wiki/OpenEvidence) | RAG over licensed literature with citations |
| [Hebbia: Matrix 2.0](https://www.hebbia.com/blog/introducing-matrix-2-0) | grid interface, human checkpoints, "you can see where every number comes from" |
| [CoCounsel Legal](https://legal.thomsonreuters.com/en/products/cocounsel-legal) | Tabular Analysis 10,000 × 100 |
| [Prawo.pl: LEX Expert AI](https://www.prawo.pl/prawnicy-sady/lex-expert-ai-nowym-narzedziem-dla-prawnikow) | answers with links to LEX excerpts |
| [Decagon: Series D](https://decagon.ai/blog/series-d-announcement) | Agent Operating Procedures |
| [Basis: behavior specs](https://www.getbasis.ai/blogs/behavior-specs-an-open-standard-for-supervising-long-horizon-agents) | trajectory evaluation, specifications hidden from the agent |
| [Sierra: τ-bench](https://sierra.ai/blog/benchmarking-ai-agents) | pass^k, drop to ~25% at pass^8 |
| [Cursor: Composer 2](https://cursor.com/blog/composer-2) · [Gigazine](https://gigazine.net/gsc_news/en/20260323-cursor-admits-composer-2-kimi) · [Cursor: data use](https://cursor.com/data-use) | open Kimi base, not disclosed at launch; requests via the backend |
| [itbrief: Glean Tau](https://itbrief.asia/story/glean-launches-tau-to-cut-enterprise-ai-token-costs) | routing, USD 0.58 vs USD 2.98 per task (vendor benchmark) |
| [Granola: transcription](https://docs.granola.ai/help-center/taking-notes/transcription) · [Startup Fortune](https://startupfortune.com/granola-ai-meeting-notes-are-not-as-private-as-you-might-think/) · [ppc.land](https://ppc.land/granola-sued-for-recording-meetings-without-consent-to-train-ai-models/) | two "Me / Them" channels, no audio recording; sharing and training on by default; the *Chamberlain v. Granola* lawsuit |
| [TechCrunch: Ghost](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/) | egress firewall as a trust feature |
| [Brave: Comet prompt injection](https://brave.com/blog/comet-prompt-injection/) | structural cause, same-origin does not protect |
| [TechCrunch: OpenAI on prompt injection](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/) · [The Register: Gartner](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/) | "unlikely to ever be fully solved"; recommendation to block AI browsers |
| [The Register: Comet calendar](https://www.theregister.com/2026/03/03/perplexity_comet_browser_hole_cal_invite/) · [BleepingComputer: BragJack](https://www.bleepingcomputer.com/news/security/bragjack-attacks-hijack-ai-browser-agents-through-malicious-extensions/) | attack without a click; "prompt forcing" in five products |
| [ComplexDiscovery](https://complexdiscovery.com/ninth-circuit-vacates-amazon-injunction-ai-agent-logs-emerge-as-ediscovery-issue/) | agent logs as evidence (title only) |
| [NRA: § 23e ZZEA](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/) | personal verification, "due protection", naming the tools at the client's request |
| [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Article 28, Chapter V, Article 32, Articles 33–34, recital 26 |
| [EDPB: AI Privacy Risks – LLMs](https://www.edpb.europa.eu/our-work-tools/our-documents/support-pool-experts-projects/ai-privacy-risks-mitigations-large_pt) | re-identification risk |
| [18 U.S.C. § 2713](https://www.law.cornell.edu/uscode/text/18/2713) | CLOUD Act |
| [UODO, 26 June 2026](https://uodo.gov.pl/pl/138/4449) | "regularly measure and test the security measures in place" |
| [PLCC](https://huggingface.co/spaces/sdadas/plcc) · [CPTUB](https://huggingface.co/spaces/speakleash/cptu_bench) | Polish acceptance tests; best open model 89.83 vs 92–97 |
| [arXiv 2609.32042: PolAgentBench](https://arxiv.org/abs/2609.32042) | cliff between 3 and 2 bits in agentic tasks |
| [arXiv 2608.30929](https://arxiv.org/abs/2608.30929) · [arXiv 2511.04205](https://arxiv.org/abs/2511.04205) · [arXiv 2606.12250](https://arxiv.org/abs/2606.12250) · [arXiv 2608.12928](https://arxiv.org/abs/2608.12928) | statute retrieval 72.3% / BM25 61.7%; KIO (National Appeals Chamber) exam; −31 pp on medical exams; weak vision on Polish medical questions |
| [arXiv 2606.29537: OSWorld 2.0](https://arxiv.org/abs/2606.29537) | 20.6% of long tasks completed, causes of failure |
| [Bielik-11B-v3](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [Bielik-Guard](https://huggingface.co/speakleash/Bielik-Guard-0.5B-v1.1) · [gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b) | Apache-2.0 licence, sizes, classifier precision 75.28% |
| [Harness review: 02-BUILDING-BLOCKS](../agent-harnesses/02-BUILDING-BLOCKS.md) · [03-ARCHITECTURE](../agent-harnesses/03-ARCHITECTURE.md) · [01-PROFILES](../agent-harnesses/01-PROFILES.md) | local tools (voice, vision, sandboxes, channels), rig figures (1,186 tok/s, 13.6 tok/s, 104.2 GB, repeatability 83), Moltis, ZeroClaw, OpenCode, Hermes TTS |

## Poland and sovereignty (04-POLAND-AND-SOVEREIGNTY.md)

| Source | What I took |
|---|---|
| [18 U.S.C. § 2713 (Cornell LII)](https://www.law.cornell.edu/uscode/text/18/2713) | Text of the CLOUD Act: "possession, custody, or control" regardless of location |
| [EDPB–EDPS, reply to LIBE (12 July 2019)](https://www.edpb.europa.eu/sites/default/files/files/file2/edpb_edps_joint_response_us_cloudact_annex.pdf) | A CLOUD Act request without an international agreement is not a basis under the GDPR |
| [The Register (25 July 2025)](https://www.theregister.com/2025/07/25/microsoft_admits_it_cannot_guarantee/) | Microsoft France's testimony in the Senate: "Non, je ne peux pas le garantir" |
| [Microsoft — European digital commitments](https://blogs.microsoft.com/on-the-issues/2025/04/30/european-digital-commitments/) | Contractual commitments, not immunity |
| [GDPR (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Articles 9, 10, 28, 32–35, 44–49, 48 |
| [GDPR recital 91](https://gdpr-info.eu/recitals/no-91/) | A single physician or lawyer is not "large scale" — a DPIA is not mandatory |
| [CMS on EDPB Opinion 28/2024](https://cms.law/en/int/legal-updates/edpb-opinion-28-2024-key-takeaways-on-processing-personal-data-in-the-context-of-ai-models) | Model anonymity and legitimate interest |
| [Ustawa o prawach pacjenta (Patient Rights Act) (Dz.U. 2024 poz. 581)](https://api.sejm.gov.pl/eli/acts/DU/2024/581/text.pdf) | Articles 13–14 and 24(2)–(6): IT staff and the processor are bound by confidentiality |
| [European Commission — EU–US transfers](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/eu-us-data-transfers_en) | Date of the DPF decision (10 July 2023) |
| [WilmerHale (blog)](https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20251201-european-court-of-justice-to-review-challenge-to-eu-us-data-privacy-framework) | Judgment T-553/23 Latombe (3 September 2025) |
| [secureprivacy (blog)](https://secureprivacy.ai/blog/is-the-eu-us-data-privacy-framework-at-risk-the-ftc-ruling-explained-2026) | Appeal C-703/25 P pending |
| [Skadden (July 2026)](https://www.skadden.com/insights/publications/2026/07/supreme-court-decision-raises-new-questions) | Trump v. Slaughter and the estimated date of the CJEU judgment |
| [Microsoft EU Data Boundary](https://blogs.microsoft.com/on-the-issues/2025/02/26/microsoft-completes-landmark-eu-data-boundary-offering-enhanced-data-residency-and-transparency/) | Completion on 26 February 2025 and the exceptions |
| [Microsoft Sovereign Cloud](https://blogs.microsoft.com/blog/2025/06/16/announcing-comprehensive-sovereign-solutions-empowering-european-organizations/) | Data Guardian, Azure Local, Bleu, Delos |
| [Copilot — privacy](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy) | Anthropic models outside the EU Data Boundary |
| [Copilot — pricing](https://www.microsoft.com/en-us/microsoft-365-copilot/pricing) | Business USD 18/user/month |
| [Microsoft FY26 Q4](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast) | 30+ million paid Copilot seats |
| [AWS European Sovereign Cloud](https://press.aboutamazon.com/aws/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe) | GA 15 January 2026, Brandenburg, EU staff |
| [S3NS](https://www.s3ns.io/en) and [ANSSI SecNumCloud](https://cyber.gouv.fr/enjeux-technologiques/cloud/) | SecNumCloud 3.2 and protection against extraterritorial law |
| [OVHcloud AI Endpoints](https://www.ovhcloud.com/en/public-cloud/ai-endpoints/), [STACKIT](https://stackit.com/en/), [IONOS AI Model Hub](https://cloud.ionos.com/managed/ai-model-hub) | EU clouds without a US parent company; IONOS token prices |
| [Azure — region list](https://learn.microsoft.com/en-us/azure/reliability/regions-list), [OChK](https://ochk.cloud/pl/) | Poland Central; "100% Polish" when reselling US AI |
| [CADA (European Commission)](https://digital-strategy.ec.europa.eu/en/policies/cloud-and-ai-development-act) | Sovereignty levels L1–L4, status of the proposal |
| [Prawo o adwokaturze (Advocacy Act) (Dz.U. 2024 poz. 1564)](https://api.sejm.gov.pl/eli/acts/DU/2024/1564/text.pdf) | Article 6 |
| [NRA — changes to the ZZEA (Code of Ethics of Advocates)](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/) and [Rzeczpospolita (16 June 2026)](https://www.rp.pl/zawody-prawnicze/art44636171-nra-zmienila-kodeks-etyki-adwokat-moze-korzystac-z-ai-ale-tylko-pomocniczo) | § 23e and § 19(6) |
| [Ustawa o radcach prawnych (Legal Advisers Act) (Dz.U. 2024 poz. 499)](https://api.sejm.gov.pl/eli/acts/DU/2024/499/text.pdf) | Article 3(3)–(6) |
| [KIRP — recommendations](https://kirp.pl/rekomendacje-dotyczace-korzystania-z-ai/) and [prawo.pl](https://www.prawo.pl/prawnicy-sady/rekomendacje-korzystania-z-ai-dla-radcow-prawnych,532905.html) | 22 recommendations, co-authors, scope |
| [Ustawa o zawodach lekarza (Medical Profession Act) (Dz.U. 2026 poz. 37)](https://api.sejm.gov.pl/eli/acts/DU/2026/37/text.pdf) | Article 40 |
| [Kodeks Etyki Lekarskiej (Code of Medical Ethics) (NIL)](https://nil.org.pl/uploaded_images/1723037323_kel-2305.pdf) and [OSOZ blog](https://blog.osoz.pl/nowy-kodeks-etyki-lekarskiej-z-niejasnym-zapisem-o-ai) | Article 12 and criticism |
| [Ustawa o doradztwie podatkowym (Tax Advisory Act) (Dz.U. 2026 poz. 1274)](https://api.sejm.gov.pl/eli/acts/DU/2026/1274/text.pdf) | Article 37 |
| [Rzeczpospolita on KIDP (12 January 2026)](https://www.rp.pl/zawody-prawnicze/art43622191-michna-doradcy-podatkowi-beda-bardziej-widoczni-w-terenie) and [IKiDP (9 August 2026)](https://ikidp.pl/blog/ai-tajemnica-zawodowa-doradcy-podatkowego/) | Verification of AI outputs; risk of pasting documents |
| [Prawo o notariacie (Notaries Act) (Dz.U. 2026 poz. 614)](https://api.sejm.gov.pl/eli/acts/DU/2026/614/text.pdf) | Article 18 |
| [Ustawa o biegłych rewidentach (Statutory Auditors Act) (Dz.U. 2025 poz. 1891)](https://api.sejm.gov.pl/eli/acts/DU/2025/1891/text.pdf) | Article 78 |
| [Kodeks karny (Criminal Code) (ISAP)](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19970880553) | Article 266 § 1 |
| [Charlotin's hallucination database](https://www.damiencharlotin.com/hallucinations/) | 2,184 cases, 6 in Poland (10 October 2026) |
| [AI Act (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj), [Article 50](https://artificialintelligenceact.eu/article/50/), [Article 6](https://artificialintelligenceact.eu/article/6/), [Annex III](https://artificialintelligenceact.eu/annex/3/) | Roles, transparency, the exception in Article 6(3), high-risk categories |
| [AI Omnibus (OJ EU)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601744), [FPF](https://fpf.org/blog/the-ai-act-implementation-timeline-what-changes-under-the-ai-omnibus/), [Lewis Silkin](https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo) | Timeline after the Omnibus, Articles 4 and 4a |
| [GPAI guidelines (Commission)](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers) | "Significant modifications" |
| [MDR (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2017/745/oj) | Rule 11 |
| [Ustawa o systemach SI (AI Systems Act) (Dz.U. 2026 poz. 1003)](https://api.sejm.gov.pl/eli/acts/DU/2026/1003/text.pdf) | Articles 5, 9, 11, 12, 13, 15, 127 (text read) |
| [gdpr.pl](https://gdpr.pl/ustawa-o-systemach-sztucznej-inteligencji-weszla-w-zycie) and [infor.pl](https://www.infor.pl/prawo/nowosci-prawne/7668177,ustawa-o-systemach-sztucznej-inteligencji-od-28-pazdziernika-2026-obowiazki-firm-i-kary-co-to-jest-kribsi.html) | Confirmation of the dates 11 August and 28 October 2026 |
| [PLD (Commission)](https://single-market-economy.ec.europa.eu/single-market/goods/free-movement-sectors/liability-defective-products_en) | Software and AI as a product, from 9 December 2026 |
| [CRA (Commission)](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act) | Reporting from 11 September 2026, obligations from 11 December 2027 |
| [UODO — checklists](https://uodo.gov.pl/pl/138/4533), [UODO — MyDr](https://uodo.gov.pl/pl/138/4540), [UODO — security testing](https://uodo.gov.pl/pl/138/4449) | Initial questions (6 August 2026), the MyDr inspection, testing of measures |
| [Noxtua](https://www.noxtua.com/), [security](https://www.noxtua.com/security), [Series C](https://www.noxtua.com/news/press-releases/series-c), [TechCrunch](https://techcrunch.com/2025/04/22/noxtua-raises-92m-for-its-sovereign-ai-tuned-for-the-german-legal-system/) | Tiers, hosting, users, funding |
| [Beck-Noxtua](https://www.beck-noxtua.pl/), [Noxtua PL](https://www.noxtua.com/news/press-releases/beck-noxtua-poland), [Noxtua CZ](https://www.noxtua.com/news/press-releases/beck-noxtua-for-the-czech-republic) | PLN 590 net, Legalis Silver+, IONOS and Open Telekom Cloud |
| [Mistral pricing](https://mistral.ai/fr/pricing), [heise](https://heise.de/-11311685) | Vibe and prices |
| [Proton Lumo pricing](https://proton.me/lumo/pricing), [privacy](https://proton.me/support/lumo-privacy), [Help Net Security](https://www.helpnetsecurity.com/2026/07/01/proton-lumo-2-0-ai/) | Price, encryption, models, Lumo 2.0 |
| [Nextcloud AI](https://docs.nextcloud.com/server/latest/admin_manual/ai/index.html), [llm2](https://docs.nextcloud.com/server/latest/admin_manual/ai/app_llm2.html) | On-prem AI apps and default models |
| [Cohere North 2](https://cohere.com/blog/introducing-north-2), [TechCrunch (February 2026)](https://techcrunch.com/2026/02/13/coheres-240m-year-sets-stage-for-ipo/), [TechCrunch (April 2026)](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/) | Air-gap, ARR, merger with Aleph Alpha |
| [DeepL Pro](https://www.deepl.com/en/pro), [Langdock](https://www.langdock.com/pricing) | Prices and hosting |
| [Heidi safety](https://heidihealth.com/safety), [Heidi GDPR](https://www.heidihealth.com/au/compliance/gdpr), [Heidi plans](https://support.heidihealth.com/en/articles/8885129-which-heidi-plan-is-right-for-you) | No recordings, EU residency, prices |
| [Nabla (Commure, competitor's review)](https://www.commure.com/blog-scribe/nabla-ai-review), [STAT](https://www.statnews.com/2025/06/17/nabla-raises-70-million-ambient-market-heats-up/) | Audio in the browser, 14-day retention, funding |
| [prawo.pl on LEX Expert AI](https://www.prawo.pl/prawnicy-sady/lex-expert-ai-nowym-narzedziem-dla-prawnikow,535918.html), [Wolters Kluwer](https://www.wolterskluwer.com/pl-pl/news/lex-expert-ai-wspiera-specjalistow-ktorzy-nie-sa-prawnikami) | Launch 19 November 2025, EU servers, expansion 14 July 2026 |
| [Protégé Polska](https://www.lexisnexis.com/de-at/cee/protege-polska) | Offering in Poland, demo only |
| [Gaius-Lex](https://gaius-lex.pl/), [Legal Technology Hub](https://www.legaltechnologyhub.com/vendors/gaius-lex/), [Signalbase](https://www.trysignalbase.com/news/funding/gaius-lex-secures-5) | On-prem, segment of 20–99 lawyers, seed |
| [LEX AI (App Store)](https://apps.apple.com/pl/app/lex-ai/id6748342467?l=pl), [lexai.pl](https://lexai.pl/) | Prices PLN 49/120/489, servers in Poland |
| [Noa pricing](https://www.noa.ai/pl/cennik), [Noa Notes](https://noa.ai/pl/noa-notes) | PLN 199 + VAT, AWS and Azure, 13,000+ professionals |
| [Medidesk](https://www.medidesk.com/), [Comarch ChatERP](https://www.comarch.pl/erp/asystent-ai/), [Comarch AI](https://www.comarch.ai/), [wFirma](https://wfirma.pl/), [inFakt](https://www.infakt.pl/), [SentiOne](https://sentione.com/) | Polish market: hosting and approach to data |
| [KSeF](https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/podstawy-prawne-oraz-kluczowe-terminy/) | Obligation deadlines and legal basis |
| [iMagazine on mObywatel](https://imagazine.pl/2026/01/02/mobywatel-wchodzi-w-2026-rok-z-polskim-ai/) | Assistant on PLLuM without personal data |
| [Eurostat](https://ec.europa.eu/eurostat/statistics-explained/index.php/Use_of_artificial_intelligence_in_enterprises), [GUS](https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultaktualnosci/5497/1/19/1/spoleczenstwo_informacyjne_w_polsce_2025.pdf), [PIE](https://pie.net.pl/wp-content/uploads/2025/09/2025-09-22_Z-AI-korzysta-mniej-niz-co-szosta-firma-w-Polsce-a-pozostale-nie-planuja-jej-wdrazac-1.pdf) | AI adoption in firms, barriers, professional services sector |
| [Future Ready Lawyer 2026 (prawo.pl)](https://www.prawo.pl/prawnicy-sady/prawnicy-na-co-dzien-korzystaja-z-ai-a-ai-zmienia-model-ich-zawodu,1540345.html) | 92% of lawyers use AI daily |
| [NIL — summary (30 June 2026)](https://nil.org.pl/uploaded_files/1783510889_30062026-zestawienie-nr-1.pdf) | Number of physicians and dentists |
| [Bielik-11B-v3.0](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct), [arXiv 2601.11579](https://arxiv.org/abs/2601.11579), [Minitron-7B](https://huggingface.co/speakleash/Bielik-Minitron-7B-v3.0-Instruct), [Bielik-PL-11B](https://huggingface.co/speakleash/Bielik-PL-11B-v3.0-Instruct), [arXiv 2604.10799](https://arxiv.org/abs/2604.10799), [DFlash](https://huggingface.co/speakleash/Bielik-11B-v3.0-DFlash), [Bielik-Guard](https://huggingface.co/speakleash/Bielik-Guard-0.5B-v1.1) | The Bielik v3 family: sizes, licences, APT4 |
| [bielik.ai](https://bielik.ai/), [Ollama SpeakLeash](https://ollama.com/SpeakLeash) | Downloads, partners (Dell) |
| [PLLuM-12B-chat](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-chat), [250715](https://huggingface.co/CYFRAGOVPL/pllum-12b-nc-chat-250715), [12B-2512](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512), [4B-2512](https://huggingface.co/CYFRAGOVPL/PLLuM-4B-instruct-2512) | The patchwork of PLLuM licences |
| [CPTUB](https://huggingface.co/spaces/speakleash/cptu_bench), [PLCC](https://huggingface.co/spaces/sdadas/plcc), [Polish Medical Leaderboard](https://huggingface.co/spaces/speakleash/polish_medical_leaderboard) | Polish benchmark results with data dates |
| [Qwen3.5-27B](https://huggingface.co/Qwen/Qwen3.5-27B), [Gemma 4 31B](https://huggingface.co/google/gemma-4-31B-it), [gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b), [EuroLLM-22B](https://huggingface.co/utter-project/EuroLLM-22B-Instruct-2512) | Licences and context of open models |
| [arXiv 2608.30929](https://arxiv.org/abs/2608.30929), [arXiv 2511.04205](https://arxiv.org/abs/2511.04205), [arXiv 2606.12250](https://arxiv.org/abs/2606.12250) | Statute retrieval, KIO exam, medical exams |
| [arXiv 2603.04162](https://arxiv.org/abs/2603.04162), [PolAgentBench arXiv 2609.32042](https://arxiv.org/abs/2609.32042) | 2-bit quantization: multiple-choice tests vs agents |
| [whisper.cpp](https://github.com/ggml-org/whisper.cpp/issues/89) | Speed of large-v3-turbo |
| [Mac mini](https://www.apple.com/pl/shop/buy-mac/mac-mini), [Mac Studio](https://www.apple.com/pl/shop/buy-mac/mac-studio), [Apple newsroom](https://www.apple.com/newsroom/2026/08/apple-introduces-new-mac-studio-with-m5-max-and-m5-ultra/), [Apple power draw](https://support.apple.com/en-us/102027) | Prices in Poland, memory, power draw |
| [llama.cpp #4167](https://github.com/ggml-org/llama.cpp/discussions/4167), [#15396](https://github.com/ggml-org/llama.cpp/discussions/15396), [#16578](https://github.com/ggml-org/llama.cpp/discussions/16578), [#10879](https://github.com/ggml-org/llama.cpp/discussions/10879), [Ollama MLX](https://ollama.com/blog/mlx), [LMSYS](https://www.lmsys.org/blog/2025-10-13-nvidia-dgx-spark), [Framework forum](https://community.frame.work/t/dgx-spark-vs-strix-halo-initial-impressions/77055) | Decoding and prefill speeds |
| [bestllmfor (estimates)](https://bestllmfor.com/ai-hardware/mac-studio-m5/), [runaihome (blog)](https://runaihome.com/blog/framework-desktop-vs-gmktec-evo-x2-local-ai-2026/) | Estimates for M5 and Strix Halo, noise and power draw |
| [ceneo GX10](https://www.ceneo.pl/;szukaj-ascent+gx10), [ceneo DGX Spark](https://www.ceneo.pl/;szukaj-dgx+spark), [ceneo Strix Halo](https://www.ceneo.pl/;szukaj-ryzen+ai+max%2B+395+128gb), [ceneo RTX PRO 6000](https://www.ceneo.pl/;szukaj-rtx+pro+6000+blackwell), [ceneo R9700](https://www.ceneo.pl/;szukaj-radeon+ai+pro+r9700) | Prices in Poland on 11 October 2026 |
| [NVIDIA forum (price change)](https://forums.developer.nvidia.com/t/2-23-2026-price-change-announcement/361713), [tech-insider](https://tech-insider.org/nvidia-rtx-pro-6000-blackwell-price-2026/) | Rising prices of high-memory hardware |
| [EuroHPC AI Factories](https://www.eurohpc-ju.europa.eu/ai-factories_en), [Beyond.pl](https://beyond.pl/en/) | Where to fine-tune models away from your desk |

## Addendum: the European gap and agent retention (02-MARKET.md)

| Source | What I took |
|---|---|
| [cryptobriefing.com](https://cryptobriefing.com/meta-muse-app-store-retention/) | press: Muse — 5 million downloads in the US in 22 days, about 700k daily users at the end of September 2026 (02-MARKET, 9. The European gap) |
| [about.fb.com](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | Meta (company data): Muse from 8 September 2026, cloud virtual machine, availability in the US and Canada |
| [techcrunch.com](https://techcrunch.com/2026/08/10/metas-new-glimmer-ai-model-offers-a-hint-at-zuckerbergs-personal-intelligence-vision/) | press: Muse Glimmer, 10 August 2026 |
| [venturebeat.com](https://venturebeat.com/technology/meta-returns-to-open-source-with-muse-glimmer-an-apache-2-0-licensed-30b-parameter-ai-model-optimized-for-agents-available-now) | press: Glimmer — Apache 2.0, about 30 bn parameters, 4-bit on a 24 GB GPU |
| [heise.de](https://www.heise.de/en/news/Siri-AI-in-the-EU-iPhone-and-iPad-users-must-continue-to-wait-11476320.html) | press: Siri AI (iOS 27, 14 September 2026) unavailable on iPhones in the EU (DMA) |
| [aboutamazon.com](https://www.aboutamazon.com/news/devices/alexa-plus-international-launch) | Amazon: list of Alexa+ countries — without Poland |
| [androidheadlines.com](https://www.androidheadlines.com/2026/07/google-gemini-spark-expands-to-ai-pro-subscribers.html) | press: Gemini Spark unavailable in the EEA, Switzerland and the United Kingdom |
