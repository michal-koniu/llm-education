# Źródła — na czym stoi ten kurs

**Zebrane 23 września 2026.** Każda pozycja ma dopisane, **co z niej weszło do kursu i gdzie**.

> ⚠️ **Wszystko tutaj starzeje się w miesiącach.** Krajobraz agentowy w 2026 zmienia się
> szybciej niż dokumentacja za nim nadąża. Gdy w części kursu widzisz konkretną liczbę
> (np. „85 % oszczędności kontekstu"), traktuj ją jako **pomiar cudzy, do powtórzenia u
> siebie** — nie jako stałą fizyczną. Dlatego każda część ma eksperyment.

---

## 1. OpenClaw — główne studium przypadku

Poprosiłeś wprost, żebym to sprawdził. Sprawdziłem — i to jest najlepiej udokumentowany
działający system agentowy do nauki architektury, bo **cała jego logika leży w czytelnych
plikach, a nie w wagach modelu**.

| Źródło | Co z tego wziąłem |
| :-- | :-- |
| [OpenClaw — Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) | Historia (WhatsApp relay → ClawdBot → Moltbot → OpenClaw, 30 I 2026), model bezpieczeństwa i **lista realnych incydentów** — do części 16 |
| [ppaolo · OpenClaw System Architecture Overview](https://ppaolo.substack.com/p/openclaw-system-architecture-overview) | ⭐ Najgłębszy opis, jaki znalazłem. Brama na `127.0.0.1:18789`, rozwiązywanie sesji, składanie promptu, potok wiadomości w 6 fazach, precedencja polityk, pamięć hybrydowa vector+BM25 w SQLite — **szkielet części 2, 6, 12** |
| [Markaicode · OpenClaw Production Architecture](https://markaicode.com/architecture/openclaw-agent-architecture/) | Podział Gateway / Brain / Hands / Memory — nazewnictwo, którego używam w części 1 |
| [Capodieci · OpenClaw Workspace Files Explained](https://capodieci.medium.com/ai-agents-003-openclaw-workspace-files-explained-soul-md-agents-md-heartbeat-md-and-more-5bdfbee4827a) | `SOUL.md`, `AGENTS.md`, `MEMORY.md`, `HEARTBEAT.md` — **cała część 6** |
| [Blink · HEARTBEAT, SOUL and Memory Configuration Guide](https://blink.new/blog/openclaw-heartbeat-soul-memory-configuration-guide-2026) | Wzorzec `HEARTBEAT_OK` tłumionego przez bramę — **rdzeń części 11** |
| [Bibek Poudel · How OpenClaw Works](https://bibek-poudel.medium.com/how-openclaw-works-understanding-ai-agents-through-a-real-architecture-5d59cc7a4764) | Pętla agentowa wyzwalana cronem jako koncept architektoniczny |
| [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) | Układ katalogów, SDK wtyczek, „wiadomość przychodząca jest niezaufana" |
| [awesome-openclaw](https://github.com/SamurAIGPT/awesome-openclaw) · [awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents) | 162 gotowe konfiguracje `SOUL.md` — materiał porównawczy do części 6 |

**Czego OpenClaw uczy najlepiej:** że agent to **problem infrastrukturalny**, nie promptowy.
Sesje, routing, piaskownice i pamięć to 90 % roboty. Prompt to 10 %.

**Czego OpenClaw uczy przez kontrprzykład:** wartości Secret Store **nie są szyfrowane
spoczynkowo** w wersji 2.0, a piaskownica dla niezaufanego kodu **nie jest włączona
domyślnie**. Cisco znalazło w zewnętrznych umiejętnościach realną eksfiltrację danych.
To nie jest powód, żeby go nie studiować — to jest **materiał do części 16**.

---

## 2. Peter Steinberger — głos przeciwny nurtowi

Autor OpenClaw. Warty czytania nie dlatego, że ma rację we wszystkim, tylko dlatego, że
**jego tezy są testowalne i idą pod prąd** temu, co sprzedaje reszta rynku.

| Źródło | Teza, którą zabieram do kursu |
| :-- | :-- |
| [Just Talk To It — the no-bs Way of Agentic Engineering](https://steipete.me/posts/just-talk-to-it) | ⭐ **„MCP i RAG to trucizna kontekstu".** GitHub MCP ≈ 23 tys. tokenów; CLI kosztuje zero, bo model już go zna i przeczyta `--help`. Prompty 1–2 zdania. 3–8 agentów równolegle w jednym katalogu, atomowe commity. **Promień rażenia** jako jednostka planowania. Odrzucenie trybu planowania i subagentów jako „obchodzenia zepsutego systemu" — **część 9, częściowo 13** |
| [MCP Best Practices](https://steipete.me/posts/2025/mcp-best-practices.md) | Pobłażliwy parser argumentów, brak wyjścia na `stdio`, komunikat błędu umożliwiający odzyskanie, podkomenda `info`, limit 300–500 linii na plik — **część 7** |
| [Loop engineering (post z 8 VI 2026)](https://steipete.me/posts) | „Nie promptuj agentów. **Projektuj pętle, które promptują agentów**" — motto części 3 |
| [OpenClaw, OpenAI and the future](https://steipete.me/posts/2026/openclaw) | Kontekst: odejście do OpenAI, OpenClaw pod fundację. Cel „agent, którego użyje moja mama" |
| [Fast Company · How Peter Steinberger built OpenClaw](https://www.fastcompany.com/91550800/how-peter-steinberger-built-openclaw) | Tło powstania — weekendowy projekt, który urósł |

> **Jak czytam Steinbergera w tym kursie.** Jego stanowisko „bez MCP, bez RAG, bez
> subagentów" jest **prawdziwe dla jego przypadku**: doświadczony inżynier, model klasy
> frontier, zadania programistyczne, pełne zaufanie do maszyny. **Trzy z tych czterech
> warunków u Ciebie nie zachodzą.** Dlatego w części 9 i 13 stawiam jego tezy obok
> pomiaru i każę Ci rozstrzygnąć samemu. To jest ważniejsza umiejętność niż wybór strony.

---

## 3. Anthropic — inżynieria harnessu i kontekstu

| Źródło | Co z tego wziąłem |
| :-- | :-- |
| [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | ⭐ **Cała część 3.** Agent inicjalizujący vs roboczy, `init.sh`, plik postępu, **lista funkcji w JSON** przeciw przedwczesnemu „gotowe", git jako pamięć, sekwencja startowa sesji, zakaz kasowania testów |
| [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | ⭐ **Cała część 4.** Budżet uwagi, context rot i jego źródło w n² transformera, **wysokość promptu systemowego**, kompakcja „najpierw pełnia, potem precyzja", notatki strukturalne, doładowanie w ostatniej chwili, subagenci zwracający 1–2 tys. tokenów |
| [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) | Cztery kryteria „czy w ogóle budować agenta": złożoność, wartość, wykonalność, koszt błędu — **otwarcie części 1** |

---

## 4. Code-mode — największa zmiana tego roku

| Źródło | Co z tego wziąłem |
| :-- | :-- |
| [MCP Code Mode — Context Engineering for Efficient Tool Execution](https://medium.com/@amirkiarafiei/mcp-code-mode-context-engineering-for-efficient-tool-execution-in-llm-agents-c46e1ddf80ac) | Redukcja kontekstu ~94 % przez traktowanie narzędzi jako odkrywalnego kodu zamiast statycznego JSON-a |
| [Microsoft Agent Framework · CodeAct](https://learn.microsoft.com/en-us/agent-framework/agents/code-act) | Formalna definicja: `execute_code` jako miejsce, gdzie agent łączy sterowanie, transformację danych i orkiestrację narzędzi **w jednym kroku** |
| [code-mode (UTCP)](https://github.com/universal-tool-calling-protocol/code-mode) | Działająca biblioteka — porównanie w części 8 |
| [mcp-server-code-execution-mode](https://github.com/elusznik/mcp-server-code-execution-mode) | Wykonanie w kontenerach rootless — łącznik części 8 z 10 |
| [Glama · Code execution with MCP](https://glama.ai/blog/2025-12-14-code-execution-with-mcp-architecting-agentic-efficiency) | Argument o zwijaniu wielu tur modelu w jedną |

**Dlaczego to jest dla Ciebie ważniejsze niż dla kogokolwiek innego:** mały model lokalny
generuje poprawny Python znacznie pewniej niż długi, poprawny JSON z zagnieżdżonymi
argumentami. Code-mode **przenosi ciężar z formatu, w którym model jest słaby, na format,
w którym jest mocny**. To jest część 8 i jeden z dwóch najważniejszych rozdziałów kursu.

---

## 5. Pamięć agentowa

| Źródło | Co z tego wziąłem |
| :-- | :-- |
| [Wasowski · I compared 5 AI agent memory systems](https://medium.com/@wasowski.jarek/i-compared-5-ai-agent-memory-systems-across-6-dimensions-none-wins-6a658335ed0a) | ⭐ Liczba, wokół której zbudowałem część 5: **Zep/Graphiti 71,2 % vs Mem0 49 % na LongMemEval** |
| [Atlan · Best AI Agent Memory Frameworks 2026](https://atlan.com/know/best-ai-agent-memory-frameworks-2026/) | Bi-temporalność jako wyróżnik roku: `valid_at` + `invalid_at` przy każdym fakcie |
| [Graphlit · Survey of AI Agent Memory Frameworks](https://www.graphlit.com/blog/survey-of-ai-agent-memory-frameworks) | Rozróżnienie **pamięć vs kontekst** — kluczowe, żeby część 4 i 5 się nie zlały |
| [Codepointer · Agent Memory Systems and Knowledge Graphs](https://codepointer.substack.com/p/agent-memory-systems-and-knowledge) | Letta/MemGPT: pamięć wirtualna w stylu systemu operacyjnego, bloki samo-edytowalne, sleep-time compute |
| [MemGuard (arXiv 2605.28009)](https://arxiv.org/pdf/2605.28009) | Zatrucie pamięci długoterminowej — wejście do ASI06 w części 16 |

---

## 6. Bezpieczeństwo agentowe

| Źródło | Co z tego wziąłem |
| :-- | :-- |
| [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | ⭐ **Szkielet całej części 16.** ASI01–ASI10, opublikowane 9 XII 2025, ponad 100 recenzentów |
| [Cycode · OWASP Top 10 Agentic — rozpisane kategorie](https://cycode.com/blog/owasp-top-10-agentic-applications/) | Pełne nazwy i opisy ASI01–ASI10 |
| [Teleport · Key Takeaways](https://goteleport.com/blog/owasp-top-10-agentic-applications/) | **72,4 %** — tak często jeden skompromitowany serwer MCP pociągał za sobą kolejne. Liczba napędzająca ćwiczenie z kaskady w części 13 |
| [Northflank · How to sandbox AI agents in 2026](https://northflank.com/blog/how-to-sandbox-ai-agents) | Drabina izolacji: kontener → gVisor → microVM. **VM jako granica zewnętrzna, microVM jako jednostka wykonania** — część 10 |
| [emirb · Your Container Is Not a Sandbox](https://emirb.github.io/blog/microvm-2026/) | Dlaczego zwykły kontener nie wystarcza dla agenta piszącego własny kod |
| [awesome-agent-runtime-security](https://github.com/bureado/awesome-agent-runtime-security) | Prymitywy: bubblewrap, Landlock, seccomp, KVM/libkrun, WASM |

---

## 7. Ewaluacja i obserwowalność

| Źródło | Co z tego wziąłem |
| :-- | :-- |
| [Prefactor · Agent Benchmarks: tau-bench, SWE-bench, GAIA, pass^k](https://prefactor.tech/learn/agent-benchmarks) | ⭐ **„Wynik agenta zmienia się bardziej wraz z harnessem niż z modelem".** Teza otwierająca część 14. Plus `pass^k` jako miara niezawodności, nie zdolności |
| [tau2-bench](https://github.com/sierra-research/tau2-bench) | Dwustronna kontrola: użytkownik też wywołuje narzędzia — wzorzec zbioru testowego w części 14 |
| [Guideline-Grounded Evidence Accumulation (arXiv 2603.02798)](https://arxiv.org/pdf/2603.02798) | ⭐ **Weryfikacja zewnętrzna.** Samo-refleksja ma skrzywienie samo-potwierdzające, bo sędzia siedzi w tym samym stanie trajektorii co autor. Sygnał musi powstać w izolowanym kontekście |
| [Stackviv · Agent Reflection](https://stackviv.ai/blog/reflection-ai-agents-self-improvement) | Pętla trzystopniowa generuj → krytykuj → popraw. Problem „ustalonego nastawienia" i krytycy o różnych osobowościach |
| [OpenTelemetry GenAI Semantic Conventions — omówienie](https://twistag.com/thinking/ai-agent-observability) | Spany agenta, workflow, narzędzia i modelu; metryki opóźnienia i tokenów; ostrzeżenie, że atrybuty `gen_ai.*` mają status Development i mogą się zmienić bez major bumpa — **część 15** |
| [Langfuse vs Arize Phoenix](https://qaskills.sh/blog/langfuse-vs-arize-phoenix) | Wybór narzędzia self-hosted do części 15 |

---

## 8. Protokoły

| Źródło | Co z tego wziąłem |
| :-- | :-- |
| [MCP · Specyfikacja 2026-07-28](https://blog.modelcontextprotocol.io/posts/2026-07-28/) | ⭐ **Bezstanowy rdzeń.** Przejście z dwukierunkowego protokołu stanowego na żądanie/odpowiedź. MRTR zamiast stale otwartych strumieni. Utwardzenie autoryzacji: RFC 9207, odejście od DCR na rzecz CIMD — część 9 |
| [The 2026 MCP Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) | Kierunek: od integracji narzędzi do komunikacji między agentami |
| [Agent2Agent — Wikipedia](https://en.wikipedia.org/wiki/Agent2Agent) | A2A pod Linux Foundation, 100+ firm. Podział ról: **MCP łączy agenta z narzędziami, A2A agentów ze sobą** |
| [Agent Context Protocol in 2026: MCP, ACP, A2A](https://www.puppyone.ai/en/blog/agent-context-protocol) | Porównanie trzech protokołów — tabela w części 9 |

---

## 9. Modele lokalne i silniki

| Źródło | Co z tego wziąłem |
| :-- | :-- |
| [LLM Configurator · Local LLM Tool Calling 2026](https://llmconfigurator.com/en/guides/coding-agents/tool-calling-local-models) | ⭐ Twarda liczba do części 7: **90 %+ poprawnych składniowo wywołań na prostych zadaniach, ale 80–90 % end-to-end na wielokrokowych** — błędy wyboru i argumentów się kumulują |
| [PromptQuorum · Best Local Models for Tool Calling 2026](https://www.promptquorum.com/power-local-llm/best-local-models-tool-calling-2026) | GLM-4.5-Air, Qwen3-Coder-30B-A3B, Qwen3-30B-A3B-Thinking jako czołówka agentowa |
| [InsiderLLM · Function Calling Local LLMs](https://insiderllm.com/guides/function-calling-local-llms/) | Parser `qwen3_coder` w vLLM i SGLang; zużycie VRAM per model |
| [Yotta Labs · vLLM vs SGLang w 2026](https://www.yottalabs.ai/post/vllm-vs-sglang-which-inference-engine-should-you-use-in-2026) | Kiedy przesiąść się z `llama-server` na vLLM — przy równoległych sesjach floty (część 13) |
| [ROCm · vLLM inference and serving](https://rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/inference/benchmark-docker/vllm.html) | Stan wsparcia AMD. ⚠️ **AITER i oficjalne testy celują w MI300X/MI350, nie w RDNA4** — u Ciebie wszystko wymaga pomiaru, nie wiary |

---

## 10. Frameworki — do porównań, nie do naśladowania

| Źródło | Rola w kursie |
| :-- | :-- |
| [LangChain · The best AI agent frameworks in 2026](https://www.langchain.com/resources/ai-agent-frameworks) | Mapa terenu; LangGraph jako graf z typowanym stanem |
| [Morphllm · 8 SDKs Compared + Claude Agent SDK Primitive Reference](https://www.morphllm.com/ai-agent-framework) | Porównanie prymitywów — do tabel „Twoje vs ich" |
| [OpenAgents · Open-source agent frameworks compared](https://openagents.org/blog/posts/2026-02-23-open-source-ai-agent-frameworks-compared) | Podział na SDK producenckie vs niezależne |
| [Langfuse · Comparing Open-Source AI Agent Frameworks](https://langfuse.com/blog/2025-03-19-ai-agent-comparison) | Kryteria oceny frameworka |

**Uwaga o smolagents:** agenci generujący kod zamiast JSON-a **redukują liczbę wywołań
modelu o ~30 %** i mają wbudowane wykonanie w piaskownicy. To najbliższa gotowa
implementacja tego, co budujesz w części 8 — i dlatego jest tam punktem odniesienia.

---

## 11. Czego celowo nie ma na tej liście

- **Kursów wideo i płatnych bootcampów.** Sprawdziłem kilka; wszystkie uczą frameworka,
  żaden mechanizmu. Masz je za darmo w dokumentacji tych frameworków.
- **Benchmarków modeli.** Starzeją się w tygodniach i nie odpowiadają na Twoje pytanie,
  bo Twoim wąskim gardłem jest harness, nie model (patrz §7, pozycja pierwsza).
- **Artykułów „top 10 agent frameworks".** Jest ich tysiąc, mówią to samo i żaden nie
  mierzy. Gdzie potrzebowałem porównania, brałem je z dokumentacji źródłowej.

---

## Jak weryfikować to po mnie

Każde twierdzenie w kursie oznaczone **⚠️ do sprawdzenia** to takie, którego **nie
zmierzyłem na Twoim sprzęcie** — bo nie mam do niego ciągłego dostępu. Wszystkie inne
liczby pochodzą albo z tej listy (wtedy jest link), albo z pomiaru opisanego w tekście.

Gdy liczba z tej listy nie zgadza się z Twoim pomiarem — **Twój pomiar wygrywa i popraw
kurs**. Pliki są Twoje.
