# Sources

**Checked on 29 October 2026.** Tags as in the [README](README.md#how-to-read-the-evidence-tags):

- **(V)** the primary page (abstract, HTML, PDF, repository or docs) was read. "(V, abstract)" means only the abstract.
- **(S)** search snippet, secondary coverage or a standard textbook reference; not checked against the original.

Many (V) entries in the "optimisers" and "guidance" groups were read once during the research and not re-read for this
guide. Spot-checks of SkillsBench, SkillBoost, the Hermes Curator, OpenClaw Skill Workshop and autoresearch confirmed
the figures. Every (C) number in the guide comes from [`tools/rare_event_stats.py`](tools/README.md).

> ⚠️ Many of these are 2026 preprints. A preprint is a claim, not a settled result. Where a figure decides a design
> choice, read the paper yourself.

---

## Self-improving systems: classic and evolutionary

- Reflexion: https://arxiv.org/abs/2303.11366 (V)
- Voyager: https://arxiv.org/abs/2305.16291 (V)
- ExpeL: https://arxiv.org/abs/2308.10144 (V)
- Agent Workflow Memory: https://arxiv.org/abs/2409.07429 (V)
- ADAS / Meta Agent Search: https://arxiv.org/abs/2408.08435 (V)
- Gödel Agent: https://arxiv.org/abs/2410.04444 (V)
- Darwin Gödel Machine: https://arxiv.org/abs/2505.22954 and https://sakana.ai/dgm/ (V)
- Huxley-Gödel Machine: https://arxiv.org/abs/2510.21614 (V)
- Hyperagents (DGM-H): https://arxiv.org/abs/2603.19461 (V, abstract)
- SICA: https://arxiv.org/abs/2504.15228 (V)
- AlphaEvolve: https://arxiv.org/abs/2506.13131 (V)
- Georgiev, Gómez-Serrano, Tao, Wagner, AlphaEvolve at scale and the "cheating phenomenon": https://arxiv.org/abs/2511.02864 (V)
- OpenEvolve: https://github.com/algorithmicsuperintelligence/openevolve (V)
- ShinkaEvolve: https://arxiv.org/abs/2509.19349 (V)
- CodeEvolve: https://arxiv.org/abs/2510.14150 (V, abstract)
- Promptbreeder: https://arxiv.org/abs/2309.16797 (V)
- STOP: https://arxiv.org/abs/2310.02304 (V)
- Karpathy, autoresearch: https://github.com/karpathy/autoresearch (V)
- Askarbekuly et al., "Autoresearch with Coding Agents: Generalizers and Metric-Maximizers" (2026): https://arxiv.org/abs/2607.18064 (V)
- RoboPhD, evolving agents under tight evaluation budgets (2026): https://arxiv.org/abs/2604.04347 (V, abstract)

## Prompt, context, skill and memory optimisers

- MIPROv2: https://arxiv.org/abs/2406.11695 and https://dspy.ai/current/api/optimizers/MIPROv2/ (V)
- GEPA: https://arxiv.org/abs/2507.19457 and https://github.com/gepa-ai/gepa (V)
- ESPO (prompt-bloat critique; Qwen2.5-32B reflector swap): https://arxiv.org/abs/2609.04197 (V)
- TextGrad: https://arxiv.org/abs/2406.07496 (V)
- Trace / OptoPrime: https://arxiv.org/abs/2406.16218 (V)
- ACE, Agentic Context Engineering: https://arxiv.org/abs/2510.04618 (V)
- Dynamic Cheatsheet: https://arxiv.org/abs/2504.07952 (V)
- ReasoningBank: https://arxiv.org/abs/2509.25140 (V)
- Memento: https://arxiv.org/abs/2508.16153 (V)
- Agent KB: https://arxiv.org/abs/2507.06229 (V, abstract)
- SkillWeaver: https://arxiv.org/abs/2504.07079 (V, abstract)
- Live-SWE-agent: https://arxiv.org/abs/2511.13646 (V)
- EvoAgentX: https://arxiv.org/abs/2507.03616 (V, abstract)
- Hermes Agent: repository https://github.com/nousresearch/hermes-agent; docs for
  [skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills),
  [memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) and
  [curator](https://hermes-agent.nousresearch.com/docs/user-guide/features/curator) (V)
- Anthropic, Agent Skills: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills (V)
- Anthropic, skill-creator update: https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills (V)
- skill-creator `SKILL.md`: https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md (V)
- OpenAI cookbook, self-evolving agents: https://developers.openai.com/cookbook/examples/partners/self_evolving_agents/autonomous_agent_retraining (V)
- OpenAI Codex, creating skills: https://developers.openai.com/codex/skills/create-skill (S)
- SkillOpt (Microsoft): https://microsoft.github.io/SkillOpt/ (V, project page)
- SkillBoost, "Rethinking Self-Evolution": https://arxiv.org/abs/2607.26643 (V)
- Library Drift: https://arxiv.org/abs/2605.19576 (V, abstract)
- SkillsBench: https://arxiv.org/abs/2602.12670 (V)
- "Do Self-Evolving Agents Forget?": https://arxiv.org/abs/2605.09315 (V)
- SkillLearnBench: https://arxiv.org/abs/2604.20087 (V, abstract)
- PAST-Bench: https://arxiv.org/abs/2608.04003 (V, abstract)
- PILOT: https://arxiv.org/abs/2608.26530 (V, abstract)
- Memory as Infrastructure: https://arxiv.org/abs/2609.05510 (V)
- HarnessBank: https://arxiv.org/abs/2607.13683 (V, abstract)
- SelfOp: https://arxiv.org/abs/2609.22792 (V, abstract)
- Surveys of self-evolving agents: Gao et al. https://arxiv.org/abs/2507.21046 and Fang et al. https://arxiv.org/abs/2508.07407 (V, abstract)
- Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet": https://arxiv.org/abs/2310.01798 (V)
- Kamoi et al., "When Can LLMs Actually Correct Their Own Mistakes?": https://arxiv.org/abs/2406.01297 (V, abstract)
- Fireworks, a self-improving agent with GEPA on open models: https://fireworks.ai/blog/self-improving-agent (V, vendor post)
- An OpenClaw self-improving-agent skill: https://github.com/pskoett/self-improving-agent (V)

## Practitioner guidance, reward hacking, long-running agents

- Anthropic:
  - Demystifying evals for AI agents: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents (V)
  - Effective harnesses for long-running agents: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents (V)
  - Harness design for long-running apps: https://www.anthropic.com/engineering/harness-design-long-running-apps (V)
  - Effective context engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (V)
  - Building effective agents: https://www.anthropic.com/research/building-effective-agents (V)
  - Writing tools for agents: https://www.anthropic.com/engineering/writing-tools-for-agents (V)
  - The advisor strategy: https://claude.com/blog/the-advisor-strategy (V)
  - Project Vend: https://www.anthropic.com/research/project-vend-1 and https://www.anthropic.com/research/project-vend-2 (V)
  - Natural emergent misalignment from reward hacking: https://www.anthropic.com/research/emergent-misalignment-reward-hacking (V)
  - Memory tool docs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool (V)
- OpenAI:
  - A practical guide to building agents: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf (V)
  - Evaluation best practices: https://developers.openai.com/api/docs/guides/evaluation-best-practices (V)
  - Chain-of-thought monitoring: https://arxiv.org/abs/2503.11926 (V)
- Google ADK, evaluation: https://adk.dev/evaluate/ (V)
- METR, "Recent frontier models are reward hacking": https://metr.org/blog/2025-06-05-recent-reward-hacking (V)
- Lilian Weng, reward hacking (including in-context reward hacking): https://lilianweng.github.io/posts/2024-11-28-reward-hacking/ (V)
- DeepMind, specification gaming: https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ (V)
- AI Scientist editing its own code (secondary coverage): https://getcoai.com/news/ai-scientist-research-tool-attempts-to-modify-its-own-source-code/ (S)
- Hamel Husain and Shreya Shankar, evals FAQ: https://hamel.dev/blog/posts/evals-faq/ (V)
- Shankar et al., "Who Validates the Validators?": https://arxiv.org/abs/2404.12272 (V)
- Eugene Yan, product evals: https://eugeneyan.com/writing/product-evals/ (V)
- Chip Huyen, Agents: https://huyenchip.com/2025/01/07/agents.html (V)
- Drew Breunig, [How contexts fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html) and [How to fix your context](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html) (V)
- Chroma, Context Rot: https://www.trychroma.com/research/context-rot (V)
- Manus, context engineering lessons: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus (V)
- Arize, instruction-following benchmark 2026: https://arize.com/blog/llm-instruction-following-benchmark-2026/ (V)
- IFScale: https://arxiv.org/abs/2507.11538 (S)
- Evaluating AGENTS.md: https://arxiv.org/abs/2602.11988 (S)
- Agent memory self-poisoning: https://ai-muninn.com/en/blog/agent-memory-self-poisoning (V)
- Vending-Bench: https://arxiv.org/abs/2502.15840 (V); Vending-Bench 2: https://andonlabs.com/evals/vending-bench-2 (V)
- Simon Willison, [The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) and [Designing agentic loops](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/) (V)

## Local runtime and harness

- llama.cpp: [function calling](https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md),
  [server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md),
  [cache checkpoints discussion](https://github.com/ggml-org/llama.cpp/discussions/22064) (V)
- Qwen3-30B-A3B-Instruct-2507 model card: https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507 (V)
- OpenClaw docs: [workspace](https://docs.openclaw.ai/concepts/agent-workspace/index.html),
  [memory](https://docs.openclaw.ai/concepts/memory), [heartbeat (retired)](https://docs.openclaw.ai/gateway/heartbeat),
  [skills and Skill Workshop](https://docs.openclaw.ai/tools/skills), [local models](https://docs.openclaw.ai/gateway/local-models) (V)
- A community OpenClaw fork for small Qwen models: https://github.com/paulwlisto/openclaw-qwen35 (V)

## Statistics, experimentation, bandits, drift

- Miller, "Adding Error Bars to Evals": https://arxiv.org/abs/2411.00640 and https://www.anthropic.com/research/statistical-approach-to-model-evals (S)
- Bowyer, Aitchison, Ivanova, "Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints": https://arxiv.org/abs/2503.01747 (V, abstract)
- Mandujano Reyes, comparing multiple models on a shared evaluation (2026): https://arxiv.org/abs/2608.22659 (V, abstract)
- Johari, Pekelis, Walsh, "Always Valid Inference" (mixture SPRT): https://arxiv.org/abs/1512.04922 (S)
- Maharaj et al., anytime-valid confidence sequences: https://arxiv.org/abs/2302.10108 (V, abstract)
- Stucchio, Bayesian A/B decision rule (expected loss): https://www.chrisstucchio.com/blog/2014/bayesian_ab_decision_rule.html (S)
- R `poisson.test`, exact conditional test: https://rdrr.io/r/stats/poisson.test.html (S)
- Krishnamoorthy & Thomson (2004), E-test for Poisson means: https://userweb.ucs.louisiana.edu/~kxk4695/JSPI-04.pdf (S)
- Bojinov, Simchi-Levi, Zhao, switchback experiments: https://arxiv.org/abs/2009.00148 (S)
- Lee & Shen, winner's curse in online controlled experiments (KDD 2018): https://dblp.org/rec/conf/kdd/LeeS18.html (S)
- Li, Chu, Langford, Wang, offline replay evaluation: https://arxiv.org/abs/1003.5956 (S)
- Raj & Kalyani, discounted Thompson sampling: https://arxiv.org/abs/1707.09727 (S)
- Fiandri et al., sliding-window Thompson sampling: https://arxiv.org/abs/2409.05181 (S)
- Russo et al., A Tutorial on Thompson Sampling: https://arxiv.org/abs/1707.02038 (S, standard reference)
- Poisson CUSUM (Lucas 1985), via the R `spc` docs: https://search.r-project.org/CRAN/refmans/spc/html/pois.cusum.arl.html (S)
- Page–Hinkley test, scikit-multiflow docs: https://scikit-multiflow.readthedocs.io/en/stable/api/generated/skmultiflow.drift_detection.PageHinkley.html (S); Gama et al. 2014 concept-drift survey (S, standard reference)
- Manheim & Garrabrant, "Categorizing Variants of Goodhart's Law": https://arxiv.org/abs/1803.04585 (V, abstract; variant names S)
- Gao, Schulman, Hilton, "Scaling Laws for Reward Model Overoptimization": https://arxiv.org/abs/2210.10760 (V, abstract)
- Kohavi, Tang, Xu, *Trustworthy Online Controlled Experiments* (Twyman's law, guardrail metrics), Cambridge University Press 2020 (S, standard reference)
