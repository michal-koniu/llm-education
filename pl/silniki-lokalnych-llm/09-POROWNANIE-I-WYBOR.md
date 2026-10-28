# 09 · Porównanie i wybór — co do czego, i co zrobić na twoim sprzęcie

Rozdział praktyczny: zbiera wnioski z rozdziałów 04–08 w tabele i scenariusze. Po jego przeczytaniu będziesz umieć wskazać silnik do każdego ze swoich zastosowań,
wiedzieć, **co z tego uruchomi się na referencyjnym rigu AMD (4× R9700, gfx1201)**, a co tylko na Macu, i mieć listę eksperymentów, które warto wykonać (żadnego z nich nie wykonałem).

> ⚠️ **Czego tu nie ma.** Nie mam ani jednego pomiaru, który porównywałby silniki na jednym sprzęcie, jednym modelu i jednym obciążeniu — a bez takiego pomiaru nie wolno
> porównywać liczb tok/s z różnych źródeł (zob. rozdział [02](02-JAK-DZIALA-INFERENCJA.md), sekcja o metodologii). Dlatego **nie ma tu kolumny „szybkość”**. Są cechy ustalone w kodzie i dokumentacji,
> wnioski z nich i ocena ryzyka. Moje własne pomiary dotyczą wyłącznie llama.cpp na rigu referencyjnym: [`../przyspieszanie-generowania/README.md`](../przyspieszanie-generowania/README.md).
> Stan na **19 października 2026**.

## Spis treści

1. [Macierz główna](#1-macierz-główna)
2. [Co z tego uruchomi się na gfx1201 (R9700)](#2-co-z-tego-uruchomi-się-na-gfx1201-r9700)
3. [API, tryb offline, telemetria i bezpieczeństwo](#3-api-tryb-offline-telemetria-i-bezpieczeństwo)
4. [Wybór według scenariusza](#4-wybór-według-scenariusza)
5. [Co pożyczyć z całego przeglądu](#5-co-pożyczyć-z-całego-przeglądu)
6. [Eksperymenty do wykonania (nie wykonane)](#6-eksperymenty-do-wykonania-nie-wykonane)
7. [Rekomendacja dla dwóch środowisk referencyjnych](#7-rekomendacja-dla-dwóch-środowisk-referencyjnych)

---

## 1. Macierz główna

Jedna tabela, wszystkie główne silniki. Szczegóły i dowody: rozdziały w ostatniej kolumnie. „Zarządza KV” = jak pamięć podręczna KV jest podzielona między żądania.

| Silnik | Do czego służy | Sprzęt | Format modeli | Wielu użytkowników | Zarządzanie KV | Licencja | Rozdz. |
|---|---|---|---|---|---|---|---|
| **llama.cpp** | jeden użytkownik / mały zespół, każdy sprzęt | CPU + ok. 15 backendów (CUDA, **HIP**, Metal, Vulkan, SYCL, …) | **GGUF** | sloty `-np`, prosty scheduler | ciągły KV na slot, cache promptu w RAM-ie, punkty kontrolne; **bez PagedAttention** | MIT | [04](04-LLAMA-CPP-I-RODZINA-GGML.md) |
| **ik_llama.cpp** | fork: więcej kwantyzacji i jąder, CPU/hybryda | jak llama.cpp (zakres węższy) | GGUF (+ własne typy IQ_K — tylko w forku) | jak llama.cpp | jak llama.cpp | MIT | [04](04-LLAMA-CPP-I-RODZINA-GGML.md) |
| **vLLM** | przepustowość, wielu użytkowników, GPU serwerowe | NVIDIA, ROCm, Intel XPU, CPU, TPU + wtyczki | HF/safetensors (+ AWQ, GPTQ, FP8…); GGUF = eksperymentalna wtyczka | **tak**, ciągłe batchowanie z budżetem tokenów | bloki + hash prefiksów | Apache-2.0 | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| **SGLang** | agenci, wspólne prefiksy, MoE | NVIDIA, AMD Instinct, TPU, Intel, Ascend | HF/safetensors | **tak** | drzewo radix | Apache-2.0 | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| **TensorRT-LLM** | maksimum na NVIDIA | **tylko NVIDIA** | HF + FP8/NVFP4 | **tak** | paged KV | Apache-2.0 + noty | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| **MLX / mlx-lm** | Apple Silicon (natywnie) | Metal; backend CUDA; **bez HIP** | MLX (safetensors) | serwer z batchowaniem w mlx-lm | klasy cache (rotujący, kwantyzowany) | MIT | [07](07-APPLE-MLX-OMLX-I-DS4.md) |
| **oMLX** | Mac + agenci kodujący, trwały cache | Apple Silicon | MLX, formaty oQ | **tak**, ciągłe batchowanie | stronicowany, warstwa RAM + **SSD** | Apache-2.0 | [07](07-APPLE-MLX-OMLX-I-DS4.md) |
| **ds4 / DwarfStar** | wąski silnik: rodzina DeepSeek V4 (+ kilka modeli) | Metal, CUDA, ROCm (**gfx1151**) | własny układ GGUF | słabo (jeden model na proces) | **dysk**: KV na SSD, strumieniowanie ekspertów | MIT | [07](07-APPLE-MLX-OMLX-I-DS4.md) |
| **KTransformers** | ogromne MoE: eksperci w RAM, uwaga na GPU | NVIDIA (koło), ROCm ze źródeł | HF | tak (przez SGLang) | jak SGLang | Apache-2.0 | [08](08-SPECJALISCI-KTRANSFORMERS-I-INNE.md) |
| **mistral.rs** | silnik w Ruście do osadzania | CUDA, Metal, CPU; **bez ROCm i Vulkan** | HF, GGUF, ISQ | tak | PagedAttention | MIT | [08](08-SPECJALISCI-KTRANSFORMERS-I-INNE.md) |
| **MLC LLM / WebLLM** | kompilacja na każde urządzenie, przeglądarka | wiele (przez TVM) | skompilowane artefakty MLC | ograniczone | własny | Apache-2.0 | [08](08-SPECJALISCI-KTRANSFORMERS-I-INNE.md) |
| **Ollama / LM Studio / Jan / Lemonade / …** | opakowania z rejestrem i GUI | zależy od silnika pod spodem | GGUF (i MLX na Macu) | zależy | zależy | różne | [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |

Zasada czytania: **jeśli w „Wielu użytkownikach” nie ma „tak”, silnik jest zbudowany dla jednej rozmowy naraz** — co dla agenta o kilku równoległych wywołaniach bywa wystarczające (na rigu referencyjnym: 2 sloty × 98 304 tokenów, 63 tok/s łącznie przy dwóch agentach — mój pomiar).

---

## 2. Co z tego uruchomi się na gfx1201 (R9700)

Najważniejsza tabela dla rigu referencyjnego. Źródła: kod i dokumentacja z rozdziałów 04–08. ⚠️ **Nie uruchamiałem żadnego z tych programów na R9700 poza llama.cpp, który działa produkcyjnie.**

| Silnik | Stan na gfx1201 według notatek | Co to znaczy dla rigu referencyjnego |
|---|---|---|
| **llama.cpp** | **działa** (produkcja referencyjna: build HIP na dokładne `gfx1201`; kod ma dedykowany plik strojenia `mmq-config-rdna4.cuh` i ścieżki WMMA dla RDNA4) | punkt odniesienia |
| **vLLM** | *deklarowane*: R9700 rozpoznawany po PCI id, gfx1201 w domyślnych architekturach budowania, jądra INT4 dla RDNA; **brak jakiegokolwiek pomiaru** w notatkach; dokumentacja twierdzi, że AWQ/GPTQ nie działają na AMD, kod mówi co innego | jedyny silnik serwerowy z udokumentowanym wsparciem RDNA4 — ale najpierw test, zob. §6 |
| **SGLang** | **nieobsługiwane**: build ROCm akceptuje tylko gfx942, gfx950, gfx1250 (a gfx1250 to nie RDNA4) | wróć, gdy `setup_rocm.py` wymieni gfx12xx |
| **TensorRT-LLM** | nie dotyczy (tylko NVIDIA) | pomiń |
| **ds4** | ROCm tylko **gfx1151** (Strix Halo); trzy PR-y i jedno zgłoszenie dla gfx1201 otwarte, niezmergowane; jedyny punkt danych: jedna R9700 ze strumieniowaniem SSD, **2,3–4,7 tok/s**; ścieżka ROCm w kodzie wygląda na jednokartową | nie zamiennik llama.cpp na rigu; porównanie z ~50 tok/s rigu referencyjnego **nie jest like-for-like** (na rigu referencyjnym wagi siedzą w VRAM czterech kart) |
| **MLX, mlx-lm, oMLX, exo** | brak backendu HIP w MLX; exo na Linuksie tylko CPU | tylko Mac |
| **KTransformers** | gotowe koło tylko NVIDIA (SM 80–90, serwerowy RAM ≥ 256 GB); ROCm = budowa ze źródeł bez deklaracji wsparcia | pomiń |
| **mistral.rs** | brak backendów ROCm i Vulkan | pomiń na rigu; opcja na Macu |
| **MLC / WebLLM** | jakość i wydajność na konsumenckich kartach ROCm nieudokumentowana w moich źródłach; niski i spadający rytm commitów | *(nie ustaliłem)* |
| **Ollama** | `docs/gpu.mdx` wymienia **Radeon AI PRO R9700** w sekcji ROCm (ROCm v7); Vulkan domyślnie włączony | możliwe, **niesprawdzone** dla modelu referencyjnego 284B |
| **Lemonade** | tabela backendów wymienia rodzinę `gfx120X` (llama.cpp-ROCm, vLLM-ROCm eksperymentalnie) | najbliższe potwierdzenie wśród opakowań, jako rodzina |
| **LM Studio** | niezweryfikowane (strona runtime’ów zwróciła 404) | *(nie ustaliłem)* |
| **Docker Model Runner, RamaLama, Jan, llmman** | ROCm istnieje jako ścieżka; gfx1201 nie jest wymieniony | *(niesprawdzone)* |

Wniosek: **na rigu AMD realna alternatywa dla llama.cpp to dziś (potencjalnie) jedynie vLLM**, i to dla modeli w formacie HF, które mieszczą się w 128 GB razem z pulą KV.
Model referencyjny (284B, GGUF UD-IQ3_XXS, 104,2 GB) tej drogi nie ma: w INT4 miałby ≈ 142 GB samych wag *(moje wyliczenie: 284 mld × 0,5 B)*, więcej niż 4 × 32 GB.

---

## 3. API, tryb offline, telemetria i bezpieczeństwo

### 3.1 Protokoły, które mówią serwery

| | OpenAI Chat | OpenAI Responses | Anthropic `/v1/messages` | API Ollamy | Uwagi |
|---|---|---|---|---|---|
| **llama-server** | ✔ | ✔ | ✔ (+ `count_tokens`) | — | + `/v1/rerank`, `/v1/embeddings`, `/slots`, `/metrics` |
| **vLLM** | ✔ | — (nie ustaliłem) | ✔ | **nie** | + Cohere, gRPC |
| **SGLang** | ✔ | — (nie ustaliłem) | ✔ | ✔ | + gRPC |
| **TensorRT-LLM** | ✔ | ✔ | adapter | — | |
| **Ollama** | ✔ (w tym `/v1/responses`) | ✔ | ✔ | natywne `/api/*` | |
| **LM Studio** | ✔ | — | ✔ | — | + natywne REST, stanowe `/v1/chat` (`response_id`) |
| **llmman** | ✔ | — | ✔ | ✔ | + Gemini |
| **Lemonade** | ✔ | — | ✔ | ✔ | |

(„—” = nie wymienione w notatkach, nie „nie istnieje”.) Praktyka: jeśli twój agent (np. Claude Code-podobny) mówi po Anthropic, a nie chcesz proxy, `llama-server` obsłuży go bezpośrednio.

### 3.2 Offline i telemetria

| Silnik | Pełny offline po pobraniu modelu? | Telemetria / połączenia „do domu” |
|---|---|---|
| **llama.cpp** | tak; flaga `--offline` | w kodzie `common`, `tools`, `src`, `ggml/src` **nie znalazłem** telemetrii ani sprawdzania aktualizacji (przeszukanie grep, nie dowód negatywny) |
| **vLLM** | tak | statystyki użycia **domyślnie włączone**, wyłączane opt-outem |
| **TensorRT-LLM** | tak | statystyki użycia **domyślnie włączone**, opt-out |
| **SGLang** | tak | nie znaleziono |
| **Ollama** | inferencja tak (`--offline`) | aplikacja sprawdza aktualizacje; modele z rejestru; chmura opcjonalna (`OLLAMA_NO_CLOUD=1` ją wyłącza) |
| **LM Studio** | tak | aktualizacje, wyszukiwanie modeli, funkcje chmurowe; deklaracja prywatności *(dane firmy)* |
| **Jan** | tak | analityka opt-in (PostHog EU) *(dane projektu)* |
| **Lemonade** | tak (backendy i modele pobierane przy pierwszym użyciu) | „zero telemetrii” *(dane projektu)* |
| **ONNX Runtime GenAI** | tak | telemetria **domyślnie włączona** w oficjalnych pakietach |

### 3.3 Powierzchnie ataku, które warto znać

- **`llama-server --agent` / `--tools` / `--mcp-servers-config`** (rozdział [04](04-LLAMA-CPP-I-RODZINA-GGML.md) §6): nieuwierzytelnione wykonywanie poleceń powłoki z uprawnieniami użytkownika serwera, jeśli port jest osiągalny. Jeśli `llama-swap` nasłuchuje na wszystkich interfejsach bez hasła, a modele startują z `--agent`, każdy w sieci LAN może uruchamiać polecenia powłoki na hoście — **to najważniejsze ryzyko takiego stosu** (zob. też [`../przyspieszanie-generowania/04-UZYTKOWANIE-UI-CLI-OPENCLAW.md`](../przyspieszanie-generowania/04-UZYTKOWANIE-UI-CLI-OPENCLAW.md)). Nie sprawdzałem, czy da się to wykorzystać z sieci.
- **ds4:** serwer bez uwierzytelniania; protokół równoległości tensorowej bez szyfrowania.
- **`ggml-rpc-server`:** README ostrzega, że to „proof-of-concept, fragile and insecure”; nie uruchamiaj w otwartej sieci.
- **Łańcuch dostaw modeli:** pobierasz wagi i szablony czatu z cudzych repozytoriów. Szablon Jinja jest kodem wykonywanym przy każdym żądaniu; GGUF od obcych wymaga takiej samej ostrożności jak każdy plik wykonywalny *(wniosek ogólny, nie z notatek)*.

---

## 4. Wybór według scenariusza

| Scenariusz | Wybór | Dlaczego | Czego unikać |
|---|---|---|---|
| **Rig AMD 4×R9700, jeden duży MoE do agentów** (konfiguracja referencyjna) | **llama.cpp + llama-swap**, tryb tensorowy + draft; `layer` + 4 sloty jako zapasowy | jedyny silnik z potwierdzonym działaniem na gfx1201 i z GGUF IQ3 dla 284B; pokrętła, których potrzebujesz | wymiana na opakowanie, które chowa flagi |
| **Wielu agentów równolegle ze wspólnym długim prefiksem** (na tym samym rigu) | najpierw **`--parallel` / `--cache-ram` / `--ctx-checkpoints` w llama.cpp**; dopiero potem jednodniowy test vLLM na mniejszym modelu HF | prefiksy i sloty w llama.cpp pokrywają dużą część potrzeb; vLLM bez pomiaru na RDNA4 | przeprowadzka w ciemno |
| **Mac (≥ 64 GB) — codzienna praca i agenci kodujący** | **oMLX** (trwały cache KV na SSD, API Anthropic) lub **mlx-lm** | cache prefiksu przeżywa restart; MLX natywny dla Apple | llama.cpp na Macu tylko, gdy potrzebujesz GGUF |
| **Mac z ≥ 96 GB i chęć na DeepSeek V4 lokalnie z dyskowym KV** | **ds4** (beta) | silnik zbudowany pod tę klasę modeli *(dane projektu)* | wystawianie na sieć (brak uwierzytelniania) |
| **Szybki start, okno czatu, pierwsze modele** | **LM Studio** lub **Ollama** | rejestr, GUI, minimum konfiguracji | oczekiwanie, że wyciśniesz z nich wszystko, co z `llama-server` |
| **Zespół, serwer na NVIDIA, dziesiątki użytkowników** | **vLLM** (lub SGLang przy wspólnych prefiksach i MoE) | przepustowość, stronicowany KV, ekosystem | llama.cpp jako serwer wielu użytkowników |
| **Maksimum na GPU NVIDIA, stała konfiguracja** | **TensorRT-LLM** (lub vLLM) | jądra FP8/NVFP4 | AMD |
| **Ogromne MoE w RAM-ie, mało VRAM** | **llama.cpp z `-ot`/`--n-cpu-moe`**, ik_llama.cpp, KTransformers (NVIDIA) | eksperci w RAM, uwaga na GPU | KTransformers na AMD |
| **Modele w przeglądarce / telefonie / NPU** | **WebLLM**, **Qualcomm GenieX**, ONNX Runtime GenAI, Lemonade (NPU Ryzen AI) | nisze | pomijanie sprawdzenia telemetrii |
| **Środowisko odcięte od sieci (air-gap)** | llama.cpp (`--offline`) lub **llmman/OCI** (transfer obrazów modeli) | brak telemetrii; modele jako artefakty OCI | produkty z aktualizatorem w tle |
| **Jedno API dla wielu różnych silników** | **llama-swap**, LiteLLM, LocalAI (60+ backendów) | jedna warstwa routingu | — |

---

## 5. Co pożyczyć z całego przeglądu

Najcenniejsze idee, w kolejności przydatności dla stosu referencyjnego (każda ma źródło w rozdziale podanym w nawiasie):

1. **Stabilny prefiks i bajt-w-bajt identyczna historia** w aplikacjach agentowych — każda zmiana serializacji unieważnia cache (ds4, oMLX, vLLM; [07](07-APPLE-MLX-OMLX-I-DS4.md), [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md)).
2. **Ustawienia llama.cpp realizujące te same idee co silniki serwerowe:** `--parallel` + stały `id_slot`, `--cache-ram` (domyślnie 8192 MiB), `--cache-idle-slots`, `--ctx-checkpoints` ([04](04-LLAMA-CPP-I-RODZINA-GGML.md)).
3. **Trwały cache prefiksu na dysku** (oMLX, ds4): dziś w llama.cpp tylko ręcznie przez `/slots` (zapis/odtworzenie stanu slotu) — warto przetestować przed zbudowaniem własnego mechanizmu ([07](07-APPLE-MLX-OMLX-I-DS4.md)).
4. **Dekodowanie spekulacyjne natywne dla modelu** (DSpark/MTP — już je masz) i warianty n-gramowe bez draftu — tanie przy kodzie i powtarzalnych wywołaniach narzędzi ([04](04-LLAMA-CPP-I-RODZINA-GGML.md), [02](02-JAK-DZIALA-INFERENCJA.md)).
5. **Routing zapytań ze wspólnym prefiksem do tego samego backendu** (polityka `cache_aware` w bramce SGLang) — do własnego orkiestratora ([06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md)).
6. **Dystrybucja modeli jako artefakty OCI** (llmman, Docker Model Runner, RamaLama, Ollama): rejestr Harbor/Artifactory/ghcr jako magazyn modeli w twojej infrastrukturze, podpisy cosign ([05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md)).
7. **Heurystyka rozmieszczenia:** najpierw spróbuj zmieścić model na jednej karcie, dopiero potem dziel ([05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md)); w llama-swap wyrazisz to osobnym wpisem per model.
8. **Izolacja narzędzi agenta:** `--tools-runtime docker:<obraz>` w llama-server, `--network none` w kontenerze rootless (RamaLama), flaga `--sandbox` w llmman ([04](04-LLAMA-CPP-I-RODZINA-GGML.md), [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md)).
9. **Rejestr parserów narzędzi i rozumowania per rodzina modeli**, oddzielony od silnika (vLLM) — własny kod kleju w aplikacjach agentowych ([06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md)).
10. **Zawsze mierz własną kwantyzację własną metryką** — dane o jakości, które dziś masz dla UD-IQ3_XXS po przyspieszeniu, to 11 z 120 próbek ([03](03-KWANTYZACJA-I-FORMATY.md)).

---

## 6. Eksperymenty do wykonania (nie wykonane)

Każdy z nich jest zaprojektowany tak, żeby dać liczbę lub jednoznaczne „nie działa”. Żadnego nie uruchamiałem — wymagają odizolowania kart od produkcji.

| # | Pytanie | Metoda | Orientacyjny koszt | Rozdz. |
|---|---|---|---|---|
| 1 | Ile kosztuje ciebie spadek jakości po przejściu na tryb tensorowy + DSpark? | dokończ benchmark jakości (był przerwany po 11 z 120 próbek) albo porównaj dywergencję KL względem wyższej kwantyzacji na tych samych promptach | kilka godzin GPU | [03](03-KWANTYZACJA-I-FORMATY.md) |
| 2 | Czy RCCL poprawia tryb tensorowy na 4×R9700? | zbuduj z `-DGGML_HIP_RCCL=ON`, porównaj tok/s | ~2 min buildu + pomiary | [04](04-LLAMA-CPP-I-RODZINA-GGML.md) |
| 3 | Czy P2P między kartami (`GGML_CUDA_P2P=1`) pomaga bez psucia wyników? | test z porównaniem tekstu; ryzyko: uszkodzone wyjście przy włączonym IOMMU | godzina | [04](04-LLAMA-CPP-I-RODZINA-GGML.md) |
| 4 | Czy vLLM w ogóle startuje na gfx1201 i jak wypada przy wielu agentach? | mały model HF (FP8/INT4) w 128 GB; `vllm bench` przy *twojej* liczbie równoległych żądań; odizolowane karty | dzień | [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| 5 | Czy warianty n-gramowe (`--spec-type ngram-*`) dodają coś do DSpark przy kodzie agenta? | te same prompty, osobne przebiegi | godzina | [04](04-LLAMA-CPP-I-RODZINA-GGML.md) |
| 6 | Czy zapis/odtworzenie slotu przez `/slots` skraca start długiej sesji agenta? | pomiar czasu prefillu z odtworzeniem i bez | godzina | [07](07-APPLE-MLX-OMLX-I-DS4.md) |
| 7 | Czy `--cache-ram` i `--ctx-checkpoints` poprawiają trafienia w cache w twoich pętlach agentowych? | metryki `/metrics` przed i po | godzina | [04](04-LLAMA-CPP-I-RODZINA-GGML.md) |
| 8 | Ile daje wymiana kwantyzacji na większą (np. okolice Q4), jeśli się zmieści? | tok/s i jakość; pamiętaj o 128 GB VRAM i puli KV | wymaga pobrania modelu | [03](03-KWANTYZACJA-I-FORMATY.md) |

---

## 7. Rekomendacja dla dwóch środowisk referencyjnych

**Rig AMD (4× R9700):** zostań przy **llama.cpp + llama-swap**. To jedyny silnik z potwierdzonym działaniem, dla którego jest zmierzony wynik (z 23,5 do ok. 50 tok/s dla jednego agenta, 63 tok/s łącznie przy dwóch).
Ulepszaj go tym, co jest już w nim: eksperymenty 1–3 i 5–7 z §6. Przejście na vLLM rozważ wyłącznie dla *innego, mniejszego* modelu w formacie HF i wyłącznie po teście z §6 (nr 4).
Najpilniejsza sprawa to nie szybkość, tylko **bezpieczeństwo ekspozycji** (`--agent` na porcie dostępnym w sieci, §3.3) i **jakość po zmianie** (nr 1).

**Mac:** do codziennej pracy i agentów kodujących zacznij od **oMLX** (lub **mlx-lm**, jeśli wolisz mniej magii); do prostych rozmów **LM Studio** lub **Ollama** (obie mają ścieżki MLX). **ds4** traktuj jako ciekawy, szybki, ale młody silnik jednego rodzaju modeli — dobry do wypróbowania na Macu z dużą pamięcią,
nie jako fundament. Przy wyborze Maca kieruj się **GB/s i GB RAM**, nie liczbą rdzeni (rozdział [07](07-APPLE-MLX-OMLX-I-DS4.md), §1).

**Ogólnie:** silnik to wymienny element; trwałe są **format modelu, protokół API i twoje pętle agentowe**. Trzymaj się standardowych API (OpenAI/Anthropic), plików GGUF i konfiguracji w repozytorium —
wtedy zmiana silnika za rok (albo zmiana właściciela projektu, rozdział [10](10-PIENIADZE-I-LUDZIE.md)) kosztuje godzinę, nie tydzień.
