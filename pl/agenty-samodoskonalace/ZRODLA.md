# Źródła

**Sprawdzone 29 października 2026.** Oznaczenia jak w [README](README.md#jak-czytać-oznaczenia):

- **(Z)** przeczytano stronę pierwotną (streszczenie, HTML, PDF, repozytorium albo dokumentację). „(Z, streszczenie)” oznacza, że tylko streszczenie.
- **(D)** z drugiej ręki: wynik wyszukiwania, omówienie albo standardowy podręcznik; bez sprawdzenia oryginału.

Wiele pozycji (Z) w grupach „optymalizatory” i „wskazówki” przeczytano podczas researchu raz i nie czytano ponownie na
potrzeby poradnika. Wyrywkowe sprawdzenie SkillsBench, SkillBoost, Curatora z Hermes Agent, Skill Workshop w OpenClaw
i autoresearch potwierdziło liczby. Każda liczba (O) w poradniku pochodzi z [`narzedzia/rare_event_stats.py`](narzedzia/README.md).

> ⚠️ Wiele z tych prac to preprinty z 2026 roku. Preprint to twierdzenie, a nie ustalony wynik. Jeśli jakaś liczba
> rozstrzyga o decyzji projektowej, przeczytaj artykuł sam.

---

## Systemy samodoskonalące się: klasyka i podejścia ewolucyjne

- Reflexion: https://arxiv.org/abs/2303.11366 (Z)
- Voyager: https://arxiv.org/abs/2305.16291 (Z)
- ExpeL: https://arxiv.org/abs/2308.10144 (Z)
- Agent Workflow Memory: https://arxiv.org/abs/2409.07429 (Z)
- ADAS / Meta Agent Search: https://arxiv.org/abs/2408.08435 (Z)
- Gödel Agent: https://arxiv.org/abs/2410.04444 (Z)
- Darwin Gödel Machine: https://arxiv.org/abs/2505.22954 i https://sakana.ai/dgm/ (Z)
- Huxley-Gödel Machine: https://arxiv.org/abs/2510.21614 (Z)
- Hyperagents (DGM-H): https://arxiv.org/abs/2603.19461 (Z, streszczenie)
- SICA: https://arxiv.org/abs/2504.15228 (Z)
- AlphaEvolve: https://arxiv.org/abs/2506.13131 (Z)
- Georgiev, Gómez-Serrano, Tao, Wagner, AlphaEvolve na dużą skalę i „zjawisko oszukiwania”: https://arxiv.org/abs/2511.02864 (Z)
- OpenEvolve: https://github.com/algorithmicsuperintelligence/openevolve (Z)
- ShinkaEvolve: https://arxiv.org/abs/2509.19349 (Z)
- CodeEvolve: https://arxiv.org/abs/2510.14150 (Z, streszczenie)
- Promptbreeder: https://arxiv.org/abs/2309.16797 (Z)
- STOP: https://arxiv.org/abs/2310.02304 (Z)
- Karpathy, autoresearch: https://github.com/karpathy/autoresearch (Z)
- Askarbekuly i in., „Autoresearch with Coding Agents: Generalizers and Metric-Maximizers” (2026): https://arxiv.org/abs/2607.18064 (Z)
- RoboPhD, ewolucja agentów przy ciasnym budżecie ocen (2026): https://arxiv.org/abs/2604.04347 (Z, streszczenie)

## Optymalizatory promptów, kontekstu, skilli i pamięci

- MIPROv2: https://arxiv.org/abs/2406.11695 i https://dspy.ai/current/api/optimizers/MIPROv2/ (Z)
- GEPA: https://arxiv.org/abs/2507.19457 i https://github.com/gepa-ai/gepa (Z)
- ESPO (krytyka puchnięcia promptów; refleksja na Qwen2.5-32B): https://arxiv.org/abs/2609.04197 (Z)
- TextGrad: https://arxiv.org/abs/2406.07496 (Z)
- Trace / OptoPrime: https://arxiv.org/abs/2406.16218 (Z)
- ACE, Agentic Context Engineering: https://arxiv.org/abs/2510.04618 (Z)
- Dynamic Cheatsheet: https://arxiv.org/abs/2504.07952 (Z)
- ReasoningBank: https://arxiv.org/abs/2509.25140 (Z)
- Memento: https://arxiv.org/abs/2508.16153 (Z)
- Agent KB: https://arxiv.org/abs/2507.06229 (Z, streszczenie)
- SkillWeaver: https://arxiv.org/abs/2504.07079 (Z, streszczenie)
- Live-SWE-agent: https://arxiv.org/abs/2511.13646 (Z)
- EvoAgentX: https://arxiv.org/abs/2507.03616 (Z, streszczenie)
- Hermes Agent: repozytorium https://github.com/nousresearch/hermes-agent; dokumentacja:
  [skille](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills),
  [pamięć](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) and
  [curator](https://hermes-agent.nousresearch.com/docs/user-guide/features/curator) (Z)
- Anthropic, Agent Skills: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills (Z)
- Anthropic, aktualizacja skill-creator: https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills (Z)
- skill-creator `SKILL.md`: https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md (Z)
- Cookbook OpenAI, agenci samoewoluujący: https://developers.openai.com/cookbook/examples/partners/self_evolving_agents/autonomous_agent_retraining (Z)
- OpenAI Codex, tworzenie skilli: https://developers.openai.com/codex/skills/create-skill (D)
- SkillOpt (Microsoft): https://microsoft.github.io/SkillOpt/ (Z, strona projektu)
- SkillBoost, "Rethinking Self-Evolution": https://arxiv.org/abs/2607.26643 (Z)
- Library Drift: https://arxiv.org/abs/2605.19576 (Z, streszczenie)
- SkillsBench: https://arxiv.org/abs/2602.12670 (Z)
- "Do Self-Evolving Agents Forget?": https://arxiv.org/abs/2605.09315 (Z)
- SkillLearnBench: https://arxiv.org/abs/2604.20087 (Z, streszczenie)
- PAST-Bench: https://arxiv.org/abs/2608.04003 (Z, streszczenie)
- PILOT: https://arxiv.org/abs/2608.26530 (Z, streszczenie)
- Memory as Infrastructure: https://arxiv.org/abs/2609.05510 (Z)
- HarnessBank: https://arxiv.org/abs/2607.13683 (Z, streszczenie)
- SelfOp: https://arxiv.org/abs/2609.22792 (Z, streszczenie)
- Przeglądy agentów samoewoluujących: Gao i in. https://arxiv.org/abs/2507.21046 i Fang i in. https://arxiv.org/abs/2508.07407 (Z, streszczenie)
- Huang i in., "Large Language Models Cannot Self-Correct Reasoning Yet": https://arxiv.org/abs/2310.01798 (Z)
- Kamoi i in., "When Can LLMs Actually Correct Their Own Mistakes?": https://arxiv.org/abs/2406.01297 (Z, streszczenie)
- Fireworks, agent samodoskonalący się z GEPA na otwartych modelach: https://fireworks.ai/blog/self-improving-agent (Z, wpis dostawcy)
- Skill self-improving-agent dla OpenClaw: https://github.com/pskoett/self-improving-agent (Z)

## Wskazówki praktyków, oszukiwanie nagrody, długo działające agenty

- Anthropic:
  - Demystifying evals for AI agents: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents (Z)
  - Effective harnesses for long-running agents: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents (Z)
  - Harness design for long-running apps: https://www.anthropic.com/engineering/harness-design-long-running-apps (Z)
  - Effective context engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (Z)
  - Building effective agents: https://www.anthropic.com/research/building-effective-agents (Z)
  - Writing tools for agents: https://www.anthropic.com/engineering/writing-tools-for-agents (Z)
  - The advisor strategy: https://claude.com/blog/the-advisor-strategy (Z)
  - Project Vend: https://www.anthropic.com/research/project-vend-1 i https://www.anthropic.com/research/project-vend-2 (Z)
  - Natural emergent misalignment from reward hacking: https://www.anthropic.com/research/emergent-misalignment-reward-hacking (Z)
  - dokumentacja narzędzia pamięci: https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool (Z)
- OpenAI:
  - A practical guide to building agents: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf (Z)
  - Evaluation best practices: https://developers.openai.com/api/docs/guides/evaluation-best-practices (Z)
  - monitorowanie łańcucha rozumowania: https://arxiv.org/abs/2503.11926 (Z)
- Google ADK, ewaluacja: https://adk.dev/evaluate/ (Z)
- METR, "Recent frontier models are reward hacking": https://metr.org/blog/2025-06-05-recent-reward-hacking (Z)
- Lilian Weng, oszukiwanie nagrody (w tym w kontekście): https://lilianweng.github.io/posts/2024-11-28-reward-hacking/ (Z)
- DeepMind, oszukiwanie specyfikacji: https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ (Z)
- AI Scientist edytujący własny kod (omówienie z drugiej ręki): https://getcoai.com/news/ai-scientist-research-tool-attempts-to-modify-its-own-source-code/ (D)
- Hamel Husain i Shreya Shankar, FAQ o ewaluacjach: https://hamel.dev/blog/posts/evals-faq/ (Z)
- Shankar i in., "Who Validates the Validators?": https://arxiv.org/abs/2404.12272 (Z)
- Eugene Yan, ewaluacje produktowe: https://eugeneyan.com/writing/product-evals/ (Z)
- Chip Huyen, Agents: https://huyenchip.com/2025/01/07/agents.html (Z)
- Drew Breunig, [How contexts fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html) i [How to fix your context](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html) (Z)
- Chroma, Context Rot: https://www.trychroma.com/research/context-rot (Z)
- Manus, lekcje z inżynierii kontekstu: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus (Z)
- Arize, benchmark wykonywania instrukcji 2026: https://arize.com/blog/llm-instruction-following-benchmark-2026/ (Z)
- IFScale: https://arxiv.org/abs/2507.11538 (D)
- Evaluating AGENTS.md: https://arxiv.org/abs/2602.11988 (D)
- Samozatrucie pamięci agenta: https://ai-muninn.com/en/blog/agent-memory-self-poisoning (Z)
- Vending-Bench: https://arxiv.org/abs/2502.15840 (Z); Vending-Bench 2: https://andonlabs.com/evals/vending-bench-2 (Z)
- Simon Willison, [The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) i [Designing agentic loops](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/) (Z)

## Lokalny silnik i harness

- llama.cpp: [wywoływanie funkcji](https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md),
  [README serwera](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md),
  [dyskusja o punktach kontrolnych cache](https://github.com/ggml-org/llama.cpp/discussions/22064) (Z)
- Karta modelu Qwen3-30B-A3B-Instruct-2507: https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507 (Z)
- Dokumentacja OpenClaw: [przestrzeń robocza](https://docs.openclaw.ai/concepts/agent-workspace/index.html),
  [pamięć](https://docs.openclaw.ai/concepts/memory), [heartbeat (wycofany)](https://docs.openclaw.ai/gateway/heartbeat),
  [skille i Skill Workshop](https://docs.openclaw.ai/tools/skills), [modele lokalne](https://docs.openclaw.ai/gateway/local-models) (Z)
- Społecznościowy fork OpenClaw dla małych modeli Qwen: https://github.com/paulwlisto/openclaw-qwen35 (Z)

## Statystyka, eksperymenty, bandyci, dryf

- Miller, "Adding Error Bars to Evals": https://arxiv.org/abs/2411.00640 i https://www.anthropic.com/research/statistical-approach-to-model-evals (D)
- Bowyer, Aitchison, Ivanova, "Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints": https://arxiv.org/abs/2503.01747 (Z, streszczenie)
- Mandujano Reyes, porównanie wielu modeli na wspólnej ewaluacji (2026): https://arxiv.org/abs/2608.22659 (Z, streszczenie)
- Johari, Pekelis, Walsh, "Always Valid Inference" (mieszany SPRT): https://arxiv.org/abs/1512.04922 (D)
- Maharaj i in., ciągi przedziałów ufności ważne w każdej chwili: https://arxiv.org/abs/2302.10108 (Z, streszczenie)
- Stucchio, bayesowska reguła decyzji A/B (oczekiwana strata): https://www.chrisstucchio.com/blog/2014/bayesian_ab_decision_rule.html (D)
- R `poisson.test`, dokładny test warunkowy: https://rdrr.io/r/stats/poisson.test.html (D)
- Krishnamoorthy i Thomson (2004), E-test dla średnich Poissona: https://userweb.ucs.louisiana.edu/~kxk4695/JSPI-04.pdf (D)
- Bojinov, Simchi-Levi, Zhao, eksperymenty z przełączaniem (switchback): https://arxiv.org/abs/2009.00148 (D)
- Lee i Shen, klątwa zwycięzcy w kontrolowanych eksperymentach online (KDD 2018): https://dblp.org/rec/conf/kdd/LeeS18.html (D)
- Li, Chu, Langford, Wang, ocena przez powtórkę offline: https://arxiv.org/abs/1003.5956 (D)
- Raj & Kalyani, dyskontowane próbkowanie Thompsona: https://arxiv.org/abs/1707.09727 (D)
- Fiandri i in., okienkowe próbkowanie Thompsona: https://arxiv.org/abs/2409.05181 (D)
- Russo i in., A Tutorial on Thompson Sampling: https://arxiv.org/abs/1707.02038 (D, standardowe źródło)
- Poisson CUSUM (Lucas 1985), w dokumentacji pakietu R `spc`: https://search.r-project.org/CRAN/refmans/spc/html/pois.cusum.arl.html (D)
- Test Page–Hinkleya, dokumentacja scikit-multiflow: https://scikit-multiflow.readthedocs.io/en/stable/api/generated/skmultiflow.drift_detection.PageHinkley.html (D); przegląd dryfu pojęć Gamy i in. 2014 (D, standardowe źródło)
- Manheim & Garrabrant, "Categorizing Variants of Goodhart's Law": https://arxiv.org/abs/1803.04585 (Z, streszczenie; nazwy odmian D)
- Gao, Schulman, Hilton, "Scaling Laws for Reward Model Overoptimization": https://arxiv.org/abs/2210.10760 (Z, streszczenie)
- Kohavi, Tang, Xu, *Trustworthy Online Controlled Experiments* (prawo Twymana, metryki-barierki), Cambridge University Press 2020 (D, standardowe źródło)
