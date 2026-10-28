# 01 · Mapa i warstwy — czym jest „runtime” i kto jest kim

Rozdział otwierający. Po jego przeczytaniu będziesz umieć odpowiedzieć na pytanie, **o którym programie w ogóle mówimy**, gdy ktoś pisze „uruchamiam model lokalnie”:
o pliku z wagami, o bibliotece liczącej macierze, o silniku wnioskowania, o serwerze HTTP, o aplikacji z oknem, czy o bramce przed nimi.
Z tej mapy korzystają wszystkie następne rozdziały.

> ⚠️ **Czego tu nie ma.** Cały kurs to **research biurkowy i czytanie kodu źródłowego**: dokumentacja, API GitHuba, artykuły naukowe i repozytoria sklonowane na rigu
> (tylko do odczytu). **Niczego nie uruchamiałem ani nie mierzyłem** — GPU rigu pracują produkcyjnie. Liczby mają datę i źródło; dane podane przez same projekty
> oznaczam *(dane projektu)*, doniesienia prasowe *(prasa)*, własne wyliczenia *(moje wyliczenie)*. Stan na **19 października 2026**; ten przegląd starzeje się w tygodniach.
> Gwiazdki, licencje i daty założenia pochodzą z API GitHuba z tego dnia.

## Spis treści

1. [Siedem warstw: od pliku z wagami do okna czatu](#1-siedem-warstw-od-pliku-z-wagami-do-okna-czatu)
2. [Mapa projektów: kto leży w której warstwie](#2-mapa-projektów-kto-leży-w-której-warstwie)
3. [Sieć zależności: kto uruchamia czyj kod](#3-sieć-zależności-kto-uruchamia-czyj-kod)
4. [Pięć filozofii: po co powstają kolejne silniki](#4-pięć-filozofii-po-co-powstają-kolejne-silniki)
5. [Podróż jednego żądania przez wszystkie warstwy](#5-podróż-jednego-żądania-przez-wszystkie-warstwy)
6. [Jak to powstało: oś czasu](#6-jak-to-powstało-oś-czasu)
7. [Jak czytać resztę kursu](#7-jak-czytać-resztę-kursu)

---

## 1. Siedem warstw: od pliku z wagami do okna czatu

Słowo „runtime” (albo „silnik”, „inference engine”) bywa używane na wszystko od biblioteki z kernelami po aplikację z ikoną w pasku.
Żeby się nie pomylić, trzeba rozdzielić **warstwy**. Jedna ciężarówka, kilka różnych rzeczy: pole z surowcem, fabryka, magazyn, sklep.

```
 ┌───────────────────────────────────────────────────────────────────────────────┐
 │ 7  Orkiestracja i bramki   llama-swap, LiteLLM, llm-d, Dynamo, LMCache         │ wiele serwerów, routing,
 │                            (kilka procesów / maszyn jako jedno API)            │ wymiana modeli, cache KV
 ├───────────────────────────────────────────────────────────────────────────────┤
 │ 6  Aplikacje i frontendy   Open WebUI, AnythingLLM, UI LM Studio, Jan          │ okno czatu, agenci,
 │                            (rozmawiają z API, same nie liczą)                  │ historia rozmów
 ├───────────────────────────────────────────────────────────────────────────────┤
 │ 5  Opakowania              Ollama, LM Studio, Jan, LocalAI, Lemonade,          │ rejestr modeli, cykl życia,
 │                            Docker Model Runner, RamaLama, llmman               │ wartości domyślne, GUI
 ├───────────────────────────────────────────────────────────────────────────────┤
 │ 4  Serwer                  llama-server, vLLM API server, SGLang, ds4-server   │ HTTP: /v1/chat/completions,
 │                            (kolejka żądań, sloty, strumieniowanie SSE)         │ szablony czatu, wywołania narzędzi
 ├───────────────────────────────────────────────────────────────────────────────┤
 │ 3  Silnik wnioskowania     libllama, vLLM EngineCore, SGLang scheduler,        │ scheduler, pamięć podręczna KV,
 │                            mlx-lm, ds4, mistral.rs, TensorRT-LLM               │ próbkowanie, wsadowanie, równoległość
 ├───────────────────────────────────────────────────────────────────────────────┤
 │ 2  Biblioteka tensorowa    ggml, MLX, PyTorch, Candle, + kernele:              │ mnożenie macierzy, uwaga,
 │    i kernele               FlashAttention, FlashInfer, hipBLAS/cuBLAS          │ kwantyzowane jądra na GPU
 ├───────────────────────────────────────────────────────────────────────────────┤
 │ 1  Model i format          checkpoint HF (safetensors), GGUF, MLX, AWQ/GPTQ    │ wagi + tokenizer + szablon;
 │                            (+ kwantyzacja: Unsloth UD, imatrix, oQ…)           │ „co jest w pliku”
 └───────────────────────────────────────────────────────────────────────────────┘
        sprzęt: CUDA · ROCm/HIP · Metal · Vulkan · SYCL · CPU · NPU
```

Dwie uwagi, bez których reszta kursu będzie mylić:

1. **Granice warstw są rozmyte, bo projekty chętnie je przekraczają.** llama.cpp to naraz warstwa 2 (ggml), 3 (libllama), 4 (`llama-server`) i — od 2026 — kawałek 5 i 7
   (wbudowany tryb routera z wymianą modeli LRU, wbudowane narzędzia i klient MCP; zob. [`04-LLAMA-CPP-I-RODZINA-GGML.md`](04-LLAMA-CPP-I-RODZINA-GGML.md)).
   vLLM i SGLang to 3 + 4. LM Studio to 5 + 6, z zamkniętym kodem. Rozdział „co jest w której warstwie” jest więc raczej odpowiedzią na pytanie „czyj kod odpowiada za co”.
2. **Szybkość generowania (tok/s) rozstrzyga się w warstwach 1–3.** Warstwy 4–7 mogą ją psuć (złe wartości domyślne, kopiowanie, pamięć podręczna, która nie trafia),
   ale poprawić mogą tylko pośrednio (np. przez trafienia w cache promptu). Dlatego w kursie techniczne rozdziały dotyczą głównie warstw 1–4, a „opakowania” opisuję oddzielnie
   (rozdział [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md)).

---

## 2. Mapa projektów: kto leży w której warstwie

Poniższa tabela obejmuje projekty, którym kurs poświęca coś więcej niż zdanie. **Warstwa** odnosi się do diagramu z §1 (najważniejsza z kilku). Gwiazdki: API GitHuba, 2026-10-19.
Znak „archiwum” = repozytorium zarchiwizowane.

### 2.1 Silniki i biblioteki (warstwy 2–4)

| Projekt | Warstwa | Licencja | Gwiazdki | Założony | Język | Gdzie omówiony |
|---|---|---|---|---|---|---|
| **llama.cpp** (+ **ggml**) | 2–4 | MIT | 131 716 (ggml: 15 508) | 2023-03-10 | C/C++ | [04](04-LLAMA-CPP-I-RODZINA-GGML.md) |
| **ik_llama.cpp** (fork) | 2–4 | MIT | 3 311 | 2024-06-27 | C++ | [04](04-LLAMA-CPP-I-RODZINA-GGML.md) |
| **llamafile** | 5 na llama.cpp | NOASSERTION (zob. [04](04-LLAMA-CPP-I-RODZINA-GGML.md)) | 26 441 | 2023-09-10 | C++ | [04](04-LLAMA-CPP-I-RODZINA-GGML.md) |
| **KoboldCpp** | 5 na llama.cpp | AGPL-3.0 | 12 032 | 2023-03-16 | C++ | [04](04-LLAMA-CPP-I-RODZINA-GGML.md) |
| **vLLM** | 3–4 | Apache-2.0 | 94 152 | 2023-02-09 | Python | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| **SGLang** | 3–4 | Apache-2.0 | 37 444 | 2024-01-08 | Python | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| **TensorRT-LLM** | 3–4 (tylko NVIDIA) | Apache-2.0 + noty obcego kodu (GitHub: NOASSERTION) | 14 859 | 2023-08-16 | Python/C++ | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| **TGI** (Hugging Face) | 3–4 | Apache-2.0 | 10 879 (**archiwum**) | 2022-10-08 | Python/Rust | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| **MLX** | 2 | MIT | 28 845 | 2023-11-28 | C++/Python | [07](07-APPLE-MLX-OMLX-I-DS4.md) |
| **mlx-lm** | 3–4 | MIT | 7 405 | 2025-03-11 | Python | [07](07-APPLE-MLX-OMLX-I-DS4.md) |
| **oMLX** | 3–5 (Mac) | Apache-2.0 | 22 936 | 2026-02-13 | Python | [07](07-APPLE-MLX-OMLX-I-DS4.md) |
| **ds4 / DwarfStar** | 2–4 (wąski) | MIT | 23 955 | 2026-05-06 | C | [07](07-APPLE-MLX-OMLX-I-DS4.md) |
| **exo** | 7 (klaster Maców) | Apache-2.0 | 47 965 | 2024-06-24 | Python | [07](07-APPLE-MLX-OMLX-I-DS4.md) |
| **KTransformers** | 3 (hybrydowe MoE) | Apache-2.0 | 19 619 | 2024-07-26 | Python/C++ | [08](08-SPECJALISCI-KTRANSFORMERS-I-INNE.md) |
| **mistral.rs** | 3–4 | MIT | 7 759 | 2024-02-26 | Rust | [08](08-SPECJALISCI-KTRANSFORMERS-I-INNE.md) |
| **MLC LLM** | 2–3 | Apache-2.0 | 23 258 | 2023-04-29 | Python/C++ | [08](08-SPECJALISCI-KTRANSFORMERS-I-INNE.md) |
| **LMDeploy** | 3–4 | Apache-2.0 | 8 108 | 2023-06-15 | Python | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |

### 2.2 Opakowania i frontendy (warstwy 5–6)

| Projekt | Silnik pod spodem | Licencja | Gwiazdki | Założony | Gdzie omówiony |
|---|---|---|---|---|---|
| **Ollama** | upstream `llama-server` (GGUF) + własny runner MLX (Apple) | MIT | 183 857 | 2023-06-26 | [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |
| **LM Studio** | zamknięte runtime’y llama.cpp + MLX | aplikacja zamknięta; `lms` (CLI) MIT | `lms`: 5 360 | — | [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |
| **Jan** | llama.cpp (+ MLX na Macu) | Apache-2.0 w README, GitHub: NOASSERTION | 45 017 | 2023-08-17 | [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |
| **GPT4All** | własny fork llama.cpp; **projekt uśpiony** (ostatni commit 2025-05-27) | MIT | 77 350 | 2023-03-27 | [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |
| **LocalAI** | 60+ backendów w obrazach OCI | MIT | 49 695 | 2023-03-18 | [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |
| **Lemonade** | llama.cpp (ROCm/Vulkan), NPU AMD | Apache-2.0 | 5 936 | 2025-05-15 | [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |
| **Docker Model Runner** | llama.cpp / vLLM / SGLang / MLX | Apache-2.0 | 658 | 2025-03-28 | [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |
| **RamaLama** | llama.cpp / vLLM w obrazach per GPU | MIT | 3 086 | 2024-07-24 | [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |
| **llmman** | upstream llama.cpp / vLLM / SGLang / mlx-lm / ds4 | Apache-2.0 | 563 | 2026-03-22 | [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |
| **Open WebUI** (frontend) | — | BSD-3 + klauzula o brandingu | 156 189 | 2023-10-06 | [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |
| **AnythingLLM** (frontend) | — | MIT | 67 323 | 2023-06-04 | [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |

### 2.3 Orkiestracja i narzędzia dookoła (warstwa 7 i boki)

| Projekt | Rola | Licencja | Gwiazdki | Gdzie |
|---|---|---|---|---|
| **llama-swap** | proxy + menedżer procesów: wymiana modeli, grupy, TTL (używasz go w produkcji) | MIT | 6 015 | [04](04-LLAMA-CPP-I-RODZINA-GGML.md) |
| **NVIDIA Dynamo** | routing i rozdział prefill/decode w klastrze | NOASSERTION | 8 332 | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| **llm-d** | inferencja na Kubernetesie | Apache-2.0 | 4 866 | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| **LMCache** | warstwa pamięci podręcznej KV (offload) | Apache-2.0 | 12 116 | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| **FlashInfer**, **FlashAttention** | biblioteki jąder uwagi | Apache-2.0 / BSD-3 | 6 708 / 25 161 | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| **Unsloth** | trening + kwantyzacje GGUF „Dynamic” (UD), lokalny UI | Apache-2.0 | 78 273 | [03](03-KWANTYZACJA-I-FORMATY.md) |

**Sprawdź sam — policz gwiazdki i licencje samodzielnie** (nie uruchamiałem dokładnie tej pętli; pojedyncze wywołania tego rodzaju użyłem do zebrania powyższych danych):

```bash
for r in ggml-org/llama.cpp vllm-project/vllm sgl-project/sglang ollama/ollama antirez/ds4 jundot/omlx llmmanorg/llmman; do
  gh api repos/$r --jq '"\(.stargazers_count)\t\(.full_name)\t\(.license.spdx_id)\t\(.created_at[:10])\t\(.pushed_at[:10])\t\(.archived)"'
done
```

---

## 3. Sieć zależności: kto uruchamia czyj kod

Najważniejszy fakt rynkowy tej mapy: **większość „różnych” programów do lokalnych modeli uruchamia ten sam silnik — llama.cpp.**
Poniższy diagram pokazuje ścieżki wg notatek z 19 października 2026 (szczegóły i dowody w rozdziałach 04–05).

```
                        ┌────────────────────────── warstwa 5/6: produkty ──────────────────────────┐
                        │                                                                           │
   Ollama ──(GGUF)──────┤                                                                           │
   LM Studio ───────────┤                                                                           │
   Jan ─────────────────┤──────────►  llama.cpp  (libllama + llama-server; ggml; backendy:         │
   LocalAI (1 z 60+) ───┤                          CUDA · HIP · Metal · Vulkan · SYCL · CPU …)      │
   Lemonade ────────────┤                          ▲                    ▲                           │
   Docker Model Runner ─┤                          │ fork                │ fork / wbudowany            │
   RamaLama ────────────┤                   ik_llama.cpp          GPT4All (zamrożony), llamafile,    │
   llmman ──────────────┘                                          KoboldCpp                        │
                                                                                                    │
   Ollama (Apple Silicon, safetensors) ─┐                                                           │
   LM Studio (mlx-engine) ──────────────┼──────►  MLX / mlx-lm  ◄── oMLX (serwer z cache SSD)      │
   Jan (własny mlx-server) ─────────────┘                                                           │
                                                                                                    │
   Docker Model Runner, LocalAI, RamaLama, llmman, Lemonade ──►  vLLM  /  SGLang  (opcjonalnie)     │
                                                                                                    │
   ds4 / DwarfStar — samodzielny silnik jednego modelu (+ forki: GB10, CPU/NVMe, aplikacja menu bar)│
   TensorRT-LLM — samodzielny silnik NVIDIA; KTransformers — wtyczka do SGLang + własne jądra CPU    │
```

Trzy wnioski:

1. **„Ollama kontra llama.cpp” przestało być porównaniem dwóch silników.** Według notatek Ollama usunęła własny silnik GGUF w maju 2026 (PR #16031 zmergowany 2026-05-29, około −430 tys. linii)
   i uruchamia teraz upstreamowy `llama-server` w przypiętej wersji (w sprawdzanym klonie: `LLAMA_CPP_VERSION` b11669, podczas gdy upstream w tym dniu był na b11741) z własną warstwą łatek;
   własny runner ma tylko dla MLX na Apple Silicon. README projektu llmman opisuje jeszcze starszy stan i jest w tym punkcie nieaktualne (rozdział [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md)).
2. **Dwa światy formatów.** GGUF (świat llama.cpp, jeden plik, wiele kwantyzacji) i checkpointy HF/safetensors z kwantyzacjami kalibrowanymi (świat vLLM/SGLang/TensorRT-LLM/MLX).
   Przejście między nimi wymaga konwersji i często zmiany kwantyzacji — rozdział [03](03-KWANTYZACJA-I-FORMATY.md).
3. **Koncentracja opiekunów.** Około siedmiu z dwunastu największych kontrybutorów llama.cpp deklaruje w profilach pracę w Hugging Face (*dane z profili GitHub, samodeklarowane*); ggml.ai dołączyło do HF 2026-02-20.
   To nie zmienia licencji (MIT), ale zmienia to, kto płaci za rozwój — rozdział [10](10-PIENIADZE-I-LUDZIE.md).

---

## 4. Pięć filozofii: po co powstają kolejne silniki

Gdyby jeden silnik był najlepszy na wszystkim, nie byłoby ich kilkunastu. Różnią się tym, **co optymalizują i czego świadomie się wyrzekają**:

| # | Filozofia | Co optymalizuje | Czego się wyrzeka | Przykłady |
|---|---|---|---|---|
| **A** | **Jeden użytkownik, dowolny sprzęt** | opóźnienie jednego strumienia; szerokość sprzętu (CPU, AMD, Apple, Vulkan, telefony); 1–16-bitowe kwantyzacje; jeden plik | maksymalna przepustowość przy setkach użytkowników; stronicowany KV; dojrzały równoległy tensor | llama.cpp, ik_llama.cpp, KoboldCpp, llamafile |
| **B** | **Wielu użytkowników, GPU serwerowe** | przepustowość (tokeny na sekundę łącznie), wykorzystanie pamięci przez stronicowany KV, wspólne prefiksy, równoległość między wieloma GPU i węzłami | prostota, małe zużycie pamięci, niszowy sprzęt, bogate kwantyzacje | vLLM, SGLang, TensorRT-LLM, LMDeploy, (TGI — archiwum) |
| **C** | **Jedna platforma, natywnie** | pełne wykorzystanie sprzętu jednego producenta (pamięć zunifikowana Apple) | przenośność | MLX, mlx-lm, oMLX |
| **D** | **Jeden model, na sztywno** | szybkość i pamięć dla *jednej* rodziny modeli (graf, kwantyzacja i cache wpisane w kod) | ogólność: każdy nowy model to nowa praca | ds4 / DwarfStar |
| **E** | **Wąska nisza** | nietypowy problem (ogromne MoE w RAM-ie, przeglądarka, NPU, osadzanie w Ruście, klaster z kilku Maców) | wszystko poza niszą | KTransformers, MLC/WebLLM, mistral.rs, exo, stosy NPU |

Do tego dochodzi **filozofia opakowania** (warstwa 5): nie optymalizuj liczenia, zoptymalizuj *dotarcie od pytania do odpowiedzi* — rejestr modeli, domyślne ustawienia, okno z czatem.

Tabela wymiarów, które rzeczywiście się liczą przy wyborze (kierunek „+” = lepiej; to **moja synteza z rozdziałów 04–08**, nie pomiar):

| | A (llama.cpp) | B (vLLM/SGLang) | C (MLX) | D (ds4) | Opakowania |
|---|---|---|---|---|---|
| szybkość jednego strumienia (batch 1) | + | ± | + (Mac) | + (jeden model) | zależy od silnika pod spodem |
| łączna przepustowość przy wielu żądaniach | ± | **+** | ± (oMLX) | − | zależy |
| szerokość sprzętu | **+** | − (NVIDIA > AMD Instinct > reszta) | − (tylko Apple, backend CUDA w MLX) | − | zależy |
| bogactwo kwantyzacji (1–8 bit, imatrix) | **+** | ± (FP8/INT4/AWQ) | ± | własny układ | zależy |
| świeże modele „od razu” | + (165 plików architektur) | + (zwykle pierwsze) | ± | wybrane | opóźnienie (przypięte wersje) |
| sterowanie flagami i buildem | **+** | + | ± | ± | − (ukryte) |
| czas do pierwszej odpowiedzi dla nowicjusza | − | − | ± | − | **+** |

---

## 5. Podróż jednego żądania przez wszystkie warstwy

Tak wygląda jedna prośba agenta na rigu referencyjnym (nazwy ze stosu referencyjnego; każdy krok ma rozdział, w którym jest opisany dokładniej):

```
 agent (Python/TS)                                                       warstwa 6
   │  POST /v1/chat/completions  {"model":"deepseek", "messages":[…], "tools":[…]}
   ▼
 llama-swap :8080   — czyta pole "model", znajduje wpis w config.yaml,    warstwa 7
   │                  w razie potrzeby wyładowuje inny model i startuje ten (ładowanie ~110 s)
   ▼
 llama-server       — szablon czatu (Jinja) → prompt; wybór slotu          warstwa 4   (rozdz. 04 §6)
   │                  po najdłuższym wspólnym prefiksie; kolejka zadań
   ▼
 libllama           — tokenizacja → ubatch → budowa grafu ggml             warstwa 3   (rozdz. 04 §4)
   │                  zapis K/V do pamięci podręcznej, kontekst/sloty
   ▼
 ggml + backend HIP — graf rozdzielony na 4 karty (tryb tensorowy),        warstwa 2   (rozdz. 04 §2, §8)
   │                  jądra CUDA skompilowane jako HIP dla gfx1201
   ▼
 próbkowanie        — kolejka próbników (top-k/top-p/min-p/gramatyka);     warstwa 3   (rozdz. 04 §5)
   │                  weryfikacja szkicu DSpark (dekodowanie spekulacyjne)
   ▼
 SSE ──► llama-swap ──► agent        parser wywołań narzędzi odtwarza `tool_calls`
```

Dla porównania — ta sama prośba w **Ollamie** przechodzi przez serwer Ollamy (szablon, harmonogram, parsery) i dopiero potem przez proces potomny `llama-server`;
w **vLLM** przez serwer API → `EngineCore` → scheduler → menedżer bloków KV → wykonawcę → jądra (rozdział [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md)).

---

## 6. Jak to powstało: oś czasu

Daty założenia repozytoriów pochodzą z API GitHuba (zweryfikowane 2026-10-19); pozostałe wydarzenia — z notatek, ze źródłami w [`ZRODLA.md`](ZRODLA.md).

| Data | Zdarzenie |
|---|---|
| 2022-10-08 | założone repozytorium Text Generation Inference (HF) — później zarchiwizowane |
| 2023-02-09 | założone repozytorium vLLM (artykuł o PagedAttention — SOSP 2023) |
| 2023-03-10 | pierwszy commit llama.cpp |
| 2023-06-26 | założona Ollama |
| 2023-11-28 | założone repozytorium MLX (zespół Apple) |
| 2024-01-08 | założony SGLang (RadixAttention) |
| 2024-06-27 | fork ik_llama.cpp |
| 2025-03 | Docker Model Runner, `mlx-lm` jako osobne repozytorium |
| 2025-05-06 | vLLM trafia pod PyTorch Foundation |
| 2026-02-13 | założony oMLX |
| 2026-02-20 | ggml.ai (twórcy llama.cpp) dołącza do Hugging Face |
| 2026-03-22 | założony llmman |
| 2026-05-06 | założony ds4 (po 5 miesiącach ~24 tys. gwiazdek) |
| 2026-05-29 | Ollama usuwa własny silnik GGUF (PR #16031) |
| 2026-06-24 / 07-29 | Qualcomm ogłasza / kończy przejęcie Modular *(dane firmy; cena nieujawniona)* |
| 2026-08-26 / 09-03 | doniesienia prasowe o przejęciu Hugging Face przez NVIDIA (zob. [10](10-PIENIADZE-I-LUDZIE.md); *nie znalazłem komunikatu którejkolwiek ze stron*) |

Wzór, który widać: **2023 = narodziny silników, 2024–25 = opakowania i specjalizacja, 2026 = konsolidacja i silniki jednego modelu.**

---

## 7. Jak czytać resztę kursu

| Jeśli chcesz… | Czytaj |
|---|---|
| szybko wiedzieć, co wybrać do swoich zastosowań | [09](09-POROWNANIE-I-WYBOR.md) (pomijając resztę) |
| zrozumieć, *dlaczego* generowanie ma taką szybkość (roofline, KV cache, batching, spekulacja) | [02](02-JAK-DZIALA-INFERENCJA.md), potem [03](03-KWANTYZACJA-I-FORMATY.md) |
| wejść głęboko w silnik, na którym w produkcji stoi konfiguracja referencyjna | [04](04-LLAMA-CPP-I-RODZINA-GGML.md) |
| porównać „gotowce” z oknem czatu | [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |
| zrozumieć silniki serwerowe i to, co działa na AMD gfx1201 | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| mieć plan dla Maców | [07](07-APPLE-MLX-OMLX-I-DS4.md) |
| ogromne MoE w RAM-ie, Rust, przeglądarka, NPU | [08](08-SPECJALISCI-KTRANSFORMERS-I-INNE.md) |
| zrozumieć rynek: kto płaci, kto za tym stoi, ryzyka | [10](10-PIENIADZE-I-LUDZIE.md) |
| sprawdzić źródła | [`ZRODLA.md`](ZRODLA.md) |

Pomiary własne na rigu (jak z 23,5 doszedłem do ok. 50 tok/s w llama.cpp) są poza tym kursem: [`../przyspieszanie-generowania/README.md`](../przyspieszanie-generowania/README.md).
Ten kurs **nie zawiera żadnych nowych pomiarów** — jest mapą i lekturą kodu.

**Jak czytać oznaczenia pewności:** brak oznaczenia = sprawdzone w kodzie lub w pierwotnym źródle; *(dane projektu / firmy)* = deklaracja strony zainteresowanej;
*(prasa)* = doniesienie, którego nie potwierdziłem u źródła; *(moje wyliczenie)* = arytmetyka na liczbach ze źródeł; *(niezweryfikowane)* = przypuszczenie.
