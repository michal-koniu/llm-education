# 08 · Specjaliści: KTransformers, mistral.rs, MLC i stosy NPU

Ten rozdział opisuje silniki, które nie próbują być "jednym programem do wszystkiego". Każdy z nich istnieje dlatego, że silnik z głównego nurtu (llama.cpp, vLLM, SGLang) zostawia jakąś niszę niezagospodarowaną: model, który nie mieści się w pamięci karty; aplikację w Ruście, która chce mieć silnik w środku; przeglądarkę albo telefon; układ NPU w laptopie. Po przeczytaniu będziesz umieć odpowiedzieć na trzy pytania. Po pierwsze: jak naprawdę działa podział "eksperci w RAM, uwaga na GPU" i czym różni się od `-ot` w llama.cpp. Po drugie: kiedy silnik w Ruście albo silnik "kompilowany" ma sens. Po trzecie: które z tych pomysłów dotykają modelu referencyjnego 284B MoE na 4× R9700, a które możesz spokojnie ominąć.

> ⚠️ **Niczego tu nie uruchamiałem.** Cały rozdział to *desk research* i czytanie kodu źródłowego (klony repozytoriów z 19 października 2026, API GitHuba, dokumentacja projektów). Żadnego z opisanych silników nie zbudowałem ani nie zmierzyłem. Liczby wydajności pochodzą od samych projektów i są oznaczone *(dane projektu)*. Gdzie nie miałem dowodu, piszę "nie ustaliłem".

**Spis treści**

1. [Co mają wspólnego: nisza, którą zostawia główny nurt](#1-co-mają-wspólnego-nisza-którą-zostawia-główny-nurt)
2. [KTransformers w głąb](#2-ktransformers-w-głąb)
3. [Porównanie: hybrydowy offload MoE (KT, llama.cpp, ik_llama.cpp, ds4)](#3-porównanie-hybrydowy-offload-moe)
4. [mistral.rs](#4-mistralrs)
5. [MLC LLM i WebLLM](#5-mlc-llm-i-webllm)
6. [Stosy NPU i stosy producentów](#6-stosy-npu-i-stosy-producentów)
7. [Co z tego dla konfiguracji referencyjnej](#7-co-z-tego-dla-konfiguracji-referencyjnej)

Notka o źródłach: statystyki GitHuba (gwiazdki, commity) pochodzą z API z 19 października 2026. Wszystkie pliki z kodu to ścieżki względem korzenia danego repozytorium. Pełne omówienie pieniędzy i ludzi stojących za projektami jest w [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md); tutaj w każdej sekcji jest tylko krótki akapit "Kto za tym stoi".

Dwie rzeczy, które zostawiam innym rozdziałom: Unsloth i mapę kwantyzacji (w tym, co naprawdę kryje się w pliku `UD-IQ3_XXS`) opisuje [`03-KWANTYZACJA-I-FORMATY.md`](03-KWANTYZACJA-I-FORMATY.md). Rodzinę llama.cpp i ik_llama.cpp (poza porównaniem w sekcji 3) opisuje [`04-LLAMA-CPP-I-RODZINA-GGML.md`](04-LLAMA-CPP-I-RODZINA-GGML.md), a ds4 [`07-APPLE-MLX-OMLX-I-DS4.md`](07-APPLE-MLX-OMLX-I-DS4.md).

---

## 1. Co mają wspólnego: nisza, którą zostawia główny nurt

Silnik z głównego nurtu optymalizuje pod jedno założenie. **llama.cpp** pod "jeden program, każdy sprzęt, każdy plik GGUF". **vLLM i SGLang** pod "wiele równoległych użytkowników na kartach z centrum danych". Każde takie założenie zostawia lukę. Silniki z tego rozdziału wchodzą właśnie w te luki:

| Silnik | Luka, którą zagospodarowuje | Cena, którą za to płaci |
|---|---|---|
| **KTransformers** | Ogromny model MoE (setki miliardów parametrów), mało VRAM, dużo RAM-u serwerowego. | Potrzebny serwerowy procesor z dużą pamięcią, ścieżka GPU gotowa tylko dla NVIDII, słaba skalowalność na wielu użytkowników. |
| **mistral.rs** | Aplikacja w Ruście (albo w Pythonie), która chce silnik *w środku procesu*, z kwantyzacją "w locie" i serwerem agentowym w jednym. | Tylko CUDA, Metal i CPU. Jeden główny autor. |
| **MLC LLM / WebLLM** | "Skompiluj model pod urządzenie": telefon, przeglądarka, karty AMD/Intel/Apple z jednego stosu. | Kompilacja per model per urządzenie, wolne tempo rozwoju, brak GGUF. |
| **Stosy NPU** (ONNX Runtime GenAI, OpenVINO GenAI, Qualcomm GenieX, AMD Ryzen AI) | Układy NPU w laptopach i telefonach, których główne silniki albo nie obsługują, albo obsługują dopiero od niedawna. | Wiązanie z jednym producentem, własne formaty modeli, często Windows. |

**Wspólny motyw wyjaśniający, dlaczego to ważne:** w 2026 roku granice się zacierają. llama.cpp ma już w głównym drzewie backendy `ggml-hexagon` (NPU Qualcomma, 53 tys. linii), `ggml-openvino` (19,6 tys.) i `ggml-webgpu` (21 tys.) *(odczytane z kodu llama.cpp, build `0ce8cd1`)*. Czyli część "nisz" głównego nurtu już się domyka. Specjaliści zostają przy życiu tam, gdzie mają przewagę, której ogólny silnik nie dogoni w rozsądnym czasie: własne jądra obliczeniowe dla ekspertów na CPU (KT), wbudowana kwantyzacja i agent (mistral.rs), kompilator (MLC), wsparcie producenta (NPU).

Dwie obserwacje, które przydadzą się w dalszej części:

1. **KTransformers sam przestał być samodzielnym silnikiem.** Zachował jądra CPU i wpiął je do SGLang. To jest wzorzec: specjalista oddaje serwowanie (API, scheduler, wywoływanie narzędzi) silnikowi z głównego nurtu i zostaje przy tym, co robi najlepiej.
2. **Stosy NPU zbiegają się do "llama.cpp plus runtime producenta".** Qualcomm GenieX to w środku vendorowany llama.cpp (sekcja 6.3). To mówi, że llama.cpp jest dziś wspólnym mianownikiem, nawet dla firm, które mają własny silnik.

---

## 2. KTransformers w głąb

### 2.1 Po co to w ogóle jest

Przypomnienie z [`02-JAK-DZIALA-INFERENCJA.md`](02-JAK-DZIALA-INFERENCJA.md): w modelu MoE (*Mixture of Experts*, **eksperci**) każdy token przechodzi tylko przez kilku wybranych ekspertów w każdej warstwie. Model DeepSeek V4 Flash ma 284 mld parametrów łącznie, ale tylko 13 mld aktywnych na token *(dane projektu ds4, synopsis karty modelu w `MODEL_CARD.md`)*. Dekodowanie jest ograniczone przepustowością pamięci: na token czytasz tylko aktywne 13 mld, ale **wszystkie 284 mld muszą gdzieś leżeć**, bo nie wiesz z góry, którzy eksperci zostaną wybrani.

Analogia: biblioteka z małą czytelnią (VRAM) i dużym magazynem (RAM). Do każdego rozdziału książki potrzebujesz kilku woluminów, ale których, to wiesz dopiero po przeczytaniu spisu treści. Precyzyjniej: wagi ekspertów trzeba mieć tam, skąd da się je szybko odczytać, a szybkość generowania zależy od tego, jaki ułamek odczytów trafia do szybkiej pamięci, a jaki do wolnej.

KTransformers odpowiada na to pytanie w specyficzny sposób: **eksperci zostają w RAM-ie procesora i są tam liczeni** (nie przenoszeni na kartę), a karta robi to, co robi najlepiej: uwagę (*attention*), warstwy gęste, router i wybranych "gorących" ekspertów.

### 2.2 Tożsamość i stan na 19 października 2026

- Repozytorium `kvcache-ai/ktransformers`, licencja **Apache-2.0**, utworzone 2024-07-26. Języki wg GitHuba: Python 7,8 MB, C++ 4,9 MB, CUDA 0,59 MB.
- 19 619 gwiazdek, 1 604 forków, około 1 359 commitów. Najwięcej commitów: Atream (245), KMSorSMS (155), Azure-Tang (116), qiyuxinlin (100), ovowei (95).
- Najnowsze wydanie **v0.7.2 (2026-10-15)**, wcześniej v0.7.1 (2026-09-15) i v0.7.0.post4 (2026-09-13). Ostatni push: 2026-10-19. Projekt jest bardzo aktywny.
- Dokumentacja: README, katalog `doc/`, `kt-kernel/README.md`, książka online https://kvcache-ai.github.io/ktransformers/.

**Kto za tym stoi.** Według README: laboratorium **MADSys na Uniwersytecie Tsinghua**, firma **Approaching.AI**, organizacja **9#AISoft** i społeczność. Lista maintainerów w `MAINTAINERS.md` ma 11 osób: 6 z Tsinghua i 5 z Approaching.AI, czyli zespół, nie jeden człowiek. Organizacja GitHuba `kvcache-ai` opisuje się jako współpraca MADSys z partnerami przemysłowymi; ta sama organizacja trzyma Mooncake, platformę serwującą dla Kimi, rozwijaną z Moonshot AI. Strona Approaching.AI była dla mnie nieosiągalna, więc finansowania i przychodów firmy **nie ustaliłem**. Ryzyka: projekt jest napędzany agendą badawczą (nagłówki wydań to głównie "wsparcie dnia zerowego" dla chińskich modeli frontowych i dostrajanie) oraz zależy od dostępności Intel AMX. Szczegóły i kontekst: [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

### 2.3 Dwie generacje: stary "framework" i nowy `kt-kernel`

To jest najczęstsze źródło nieporozumień, bo w sieci krążą tutoriale do obu.

**Generacja 1 (2024 do połowy 2025): monolityczny framework.** KT podmieniał moduły `nn.Module` z biblioteki HuggingFace własnymi operatorami według reguł YAML (`optimize_rules/*.yaml`, flaga `--optimize_config_path`), a do tego miał własny serwer (`ktransformers/server/main.py --backend_type balance_serve`). Opis jest w `doc/en/AMX.md`.

**Generacja 2 (od późnej jesieni 2025): `kt-kernel` jako wtyczka.** README (wpis z 2025-10-10) mówi o integracji z SGLang; mapa drogowa to issue sgl-project/sglang#11425, a wpis na blogu LMSYS jest z 2025-10-22. Stary kod został przeniesiony do katalogu `archive/` (w klonie z 19 października: `archive/ktransformers/` 50,2 tys. linii, `archive/kt-sft/` 74,1 tys., `archive/csrc/` 28,2 tys. wraz z planistą `balance_serve` w C++). README wprost: "The original integrated KTransformers framework has been archived".

Żywy produkt to dziś:
- **`kt-kernel`**: biblioteka jąder MoE na CPU, w klonie około 73,8 tys. linii w `kt-kernel/operators/` plus warstwa Pythona (35,9 tys.),
- **wtyczka SGLang**: po stronie SGLang plik `python/sglang/srt/layers/moe/kt_ep_wrapper.py` (393 linie, licencja Apache-2.0) mieszka już w *upstreamowym* SGLang,
- **ścieżka SFT**: dostrajanie modeli MoE z ekspertami liczonymi na CPU, zintegrowane z LLaMA-Factory.

Praktyczny wniosek: jeśli czytasz poradnik z `--optimize_config_path` i `balance_serve`, to opisuje on **archiwalną** generację.

### 2.4 Jak płynie żądanie (kt-kernel w SGLang)

Wszystko poniżej zweryfikowałem w kodzie: `kt-kernel/python/experts_base.py` (948 linii), `kt-kernel/python/experts.py` (466 linii) i `kt_ep_wrapper.py` w SGLang.

```
            GPU (NVIDIA)                              CPU + RAM hosta (kilka węzłów NUMA)
  ┌───────────────────────────────┐            ┌──────────────────────────────────────────┐
  │ embedding, norm, attention    │            │  węzeł NUMA 0         węzeł NUMA 1       │
  │ (KV cache zostaje tu)         │            │  ┌──────────────┐     ┌──────────────┐   │
  │ warstwy gęste, router         │            │  │ wycinek       │     │ wycinek       │  │
  │ "gorący" eksperci (maska)     │            │  │ KAŻDEGO       │     │ KAŻDEGO       │  │
  └──────────────┬────────────────┘            │  │ eksperta      │     │ eksperta      │  │
                 │ router wybrał top-k         │  │ (dim. pośredni│     │ (dim. pośredni│  │
                 │ ekspertów                   │  │  podzielony)  │     │  podzielony)  │  │
                 │                             │  └──────┬───────┘     └──────┬───────┘   │
   hidden_states │ topk_ids, topk_weights      │         │ AMX / AVX512       │           │
   (kopia D2H do │ ─────────────────────────►  │         └────────┬───────────┘           │
   pamięci       │                             │      częściowe wyniki ──► redukcja       │
   przypiętej)   │                             │                  │                       │
                 │ ◄─────────────────────────  │                  ▼                       │
                 │   wynik ekspertów CPU       └──────────────────────────────────────────┘
                 ▼
     dodanie do wyniku ekspertów GPU → dalej, następna warstwa

  Odroczenie (deferral): eksperci o najmniejszych wagach routingu NIE są czekani w tej warstwie;
  ich wynik dochodzi dopiero do wejścia NASTĘPNEJ warstwy, gdy GPU już liczy jej attention.
```

Kroki, po kolei:

1. **SGLang liczy po swojemu** attention, normalizacje, router i ekspertów rezydujących na GPU (dowolną metodą kwantyzacji; owijka jest ogólna dla "dowolnej metody kwantyzacji MoE").
2. **Przekazanie do CPU.** Po routingu `kt_ep_wrapper` oddaje `(hidden_states, topk_ids, topk_weights)` do `KTMoEWrapper.submit_forward(...)`. Funkcja `_prepare_forward_cpu_buffers` kopiuje dane z GPU do **przypiętych** (*pinned*), podwójnie buforowanych buforów CPU (`KExpertsCPUBuffer`, `current_slot`/`next_slot`) i maskuje identyfikatory ekspertów rezydujących na GPU (`gpu_experts_mask`), żeby nie liczyć ich dwa razy.
3. **Synchronizacja bez aktywnego czekania.** `CPUInfer.submit_with_cuda_stream(cuda_stream, task)` wstawia zadanie CPU jako *host callback* na strumieniu CUDA. Kolejność względem pracy GPU zapewnia strumień, a nie pętla czekająca na CPU; `sync_forward` robi później odpowiednie `sync_with_cuda_stream`. Na NPU Ascend ten mechanizm bywa zawodny, więc kod ma tam synchroniczną ścieżkę zapasową (długie komentarze na początku `experts_base.py`).
4. **Odroczenie ekspertów** (*expert deferral*; parametr `max_deferred_experts_per_token`, funkcja `select_deferred_experts`). Najmniej ważni (o najniższych wagach routingu) spośród wybranych ekspertów nie są oczekiwani w bieżącej warstwie. Liczą się jako drugie zadanie, a ich wynik jest dodawany do wejścia *następnej* warstwy. Dzięki temu praca CPU nakłada się na attention następnej warstwy na GPU. Według artykułu to podnosi wykorzystanie CPU z "zwykle poniżej 75%" do niemal 100%, daje do 1,45× przepustowości, a dokładność pozostaje w granicach 0,5% *(dane projektu, strona publikacji MADSys)*. Zwróć uwagę: odroczenie *zmienia obliczenia* (wynik słabszych ekspertów trafia nieco później), więc to nie jest czysta optymalizacja bez skutków; stąd deklarowana tolerancja dokładności.
5. **Podział NUMA.** Klasa `TP_MOE_Common<T>` (`kt-kernel/operators/moe-tp.hpp`) dzieli *wymiar pośredni każdego eksperta* na podpule NUMA (`tp_count = pool->config.subpool_count`; kod rzuca wyjątek, jeśli `intermediate_size % tp_count != 0`). Każdy węzeł NUMA trzyma w swojej lokalnej pamięci własny wycinek **każdego** eksperta, liczy swój wynik częściowy, a wyniki są redukowane. Flaga `--kt-threadpool-count` oznacza liczbę węzłów NUMA. To oznacza, że każdy węzeł czyta tylko pamięć lokalną. Przy dekodowaniu MoE, które jest ograniczone przepustowością DRAM, to jest sedno.
6. **Wątki.** `InNumaPool`/`WorkerPool` (`kt-kernel/cpu_backend/worker_pool.{h,cpp}`, 507 linii w `.cpp`) przypinają po jednym wątku na *fizyczny* rdzeń przez `hwloc` (`hwloc_set_membind` ze ścisłym wiązaniem, nazwy wątków `numa_<id>_t_<n>`) i używają pętli *work stealing* z atomowym licznikiem (`do_work_stealing_job`). Dokumentacja wielokrotnie ostrzega: liczyć rdzenie fizyczne, nie wątki sprzętowe (*hyperthreading*).
7. **Jądra AMX.** `kt-kernel/operators/amx/la/amx_kernels.hpp` zawiera ręcznie pisane pętle po kafelkach (`_tile_loadd`, `_tile_dpbssd` dla INT8, `_tile_dpbf16ps` dla BF16) na kafelkach 0–7 (3 kafelki A × 1 kafelek B → 3 kafelki C). Wagi są przepakowywane do układu przyjaznego AMX już przy ładowaniu (`pack.hpp`, `amx_buffers.hpp`). Blog LMSYS podaje "do 21,3 TFLOPS" trwałej wydajności jądra AMX *(dane projektu)*.

**Rozmieszczenie ekspertów** to maska logiczna per warstwa (`generate_gpu_experts_masks`). Strategie: `uniform`, `frequency` (wymaga pliku statystyk `.pt` z flagi `--record-kt-gpu-expert-distribution`), `front-loading`, `random`, oraz *dynamiczna aktualizacja* podczas prefillu (`--kt-gpu-prefill-token-threshold`) *(dokumentacja `doc/en/kt-kernel/experts-sched-Tutorial.md`)*.

**Prefill (czytanie promptu).** Przy długich promptach wąskim gardłem jest CPU, więc projekt pozwala fragmentom prefillu (`chunked_prefill_size`, w komentarzu owijki przykład 25600) używać GPU dla ekspertów, ze strumieniowaniem wag warstwa po warstwie (`fp8_layerwise_transport.cpp`, plik o rozmiarze 31,6 kB). Istnienie pliku sprawdziłem; samego mechanizmu **nie prześledziłem** *(niezweryfikowane)*.

### 2.5 Co KT uruchamia: sprzęt i formaty

Po stronie CPU (źródło: `kt-kernel/README.md` i `doc/en/kt-kernel/kt-kernel_intro.md`; lista metod to dosłownie zbiór `INFERENCE_METHODS` w `kt-kernel/python/experts.py`):

| Metoda (`--kt-method`) | Wymaganie CPU | Format wag |
|---|---|---|
| `AMXINT4`, `AMXINT8` | Intel AMX (od Sapphire Rapids) | przekonwertowane INT4/INT8 (skrypt `convert_cpu_weights.py`) |
| `RAWINT4`, `FP8`, `BF16`, `FP8_PERCHANNEL` ("natywna precyzja") | AVX512 (warianty VNNI/BF16), np. Ice Lake, Zen 4 | własny FP8/BF16/INT4 checkpointu, współdzielony ze ścieżką GPU |
| `LLAMAFILE` | AVX2+ (Haswell 2013 / Zen+) | **GGUF** (Q4_K, Q4_K_M, Q5_K i inne) przez dołączone jądra llamafile |
| `GPTQ_INT4`, `MXFP4`, `NVFP4`, `MXFP8`, `MOE_INT4/8` | AVX2 / AVX512-VNNI | GPTQ, OCP MX, NVFP4 (ModelOpt) |
| procesory AMD | ścieżka BLIS INT8 (`doc/en/kt-kernel/amd_blis.md`) | INT8 |
| ARM | KML (budowa ze źródeł) | nie ustaliłem |

Ważne dla ciebie: **format GGUF działa tylko przez metodę `LLAMAFILE`**, czyli wolniejszą ścieżkę AVX2, nie AMX. Cała reszta (w tym AMX) to formaty safetensors. Z historycznych ciekawostek: wpis z README z 2025-03-05 "Support unsloth 1.58/2.51 bits weights and IQ1_S/FP8 hybrid weights" pokazuje, że dynamiczne GGUF-y Unsloth do DeepSeek-R1 były jednym z wczesnych zastosowań KT.

Po stronie GPU:

- **Gotowe koło (`pip install kt-kernel`) wspiera wyłącznie NVIDIĘ: SM 80/86/89/90** (A100, RTX 30/40, H100). V100/T4/GTX nie są wspierane. Linux x86-64, Python 3.10–3.12, CUDA 12+ *(dokumentacja `kt-kernel_intro.md`)*.
- `kt-kernel/CMakeLists.txt` ma wzajemnie wykluczające się opcje budowania `KTRANSFORMERS_USE_CUDA | MUSA | ROCM | MACA | SYCL | ASCEND_NPU` (linie 16–21 i 54). Czyli ROCm, Moore Threads, MetaX, Intel XPU (jądra SYCL XMX dla GPTQ-INT4, 9 plików w `operators/sycl/`) i Huawei Ascend są celami **budowanymi ze źródeł**. Warstwa abstrakcji to `cpu_backend/vendors/{cuda,hip,musa,maca,ascend_npu}.h`.
- Stara dokumentacja ROCm (`doc/en/ROCm.md`, oznaczona "Beta") dotyczy **starego frameworka**, testowanego na "EPYC 9274F + Radeon 7900 XTX" z PyTorchem dla ROCm 6.2.4. **W repozytorium nie ma ani słowa o gfx1201 ani o R9700** (sprawdziłem grepem po dokumentach; niczego nie budowałem).

⚠️ **Dla maszyny referencyjnej:** ścieżka KT dla kart AMD jest "kompiluj sam i sprawdź", bez deklaracji wsparcia dla RDNA4. Traktuj to jako **architekturę, z której można się uczyć**, a nie narzędzie do wdrożenia na R9700.

### 2.6 Czego KT potrzebuje: sprzęt serwerowy

Dokumentacja podaje minimum **256 GB** pamięci DDR5, testowane na **512 GB** (README i `doc/`). Docelowy użytkownik to stacja robocza lub serwer z dużym RAM-em i jedną lub kilkoma kartami NVIDIA, przy niskiej współbieżności (jeden użytkownik lub mały zespół). Artykuł sam mówi, że projekt "celuje w scenariusze z mniejszą liczbą równoczesnych żądań, gdzie przewagą jest pojemność pamięci CPU" *(dane projektu, strona publikacji MADSys)*.

### 2.7 Wydajność (wszystko to dane projektu; nigdy nie mieszam konfiguracji)

- **Artykuł (SOSP 2025):** 4,62–19,74× szybszy prefill i 1,25–4,09× szybsze dekodowanie wobec "istniejących alternatyw", plus do 1,45× z odroczenia ekspertów. W tym, co udało mi się pobrać, **nie wymieniono** konkurencyjnych baz; podejrzewam llama.cpp i Fiddler, ale to *(niezweryfikowane)*. DOI 10.1145/3731569.3764843 wzięty z BibTeX-a w README (strona ACM zwróciła 403).
- **README:** DeepSeek-R1-0528 (FP8), 8× L20 + Xeon Gold 6454S, współbieżność 8: **227,85 tok/s łącznie, 87,58 tok/s na wyjściu**. Te same liczby w blogu LMSYS (ShareGPT).
- **Blog LMSYS:** dwa gniazda Xeon Platinum 8452Y (72 rdzenie, 2 TB DDR5) + A100 40 GB w wariancie z jedną kartą: "do 20×" prefill i "do 4×" dekodowanie. Przy 8× L20 przewaga nad jedną kartą to 26% przy współbieżności 1 i 264% przy 8.
- **Tabela rozmieszczenia (własna projektu):** Qwen3-Next-80B-A3B-Instruct-FP8, 4× RTX 4090, Xeon Gold 6454S, TP=4, ShareGPT, tok/s:

| Ułamek ekspertów na GPU | Wynik (tok/s) |
|---|---|
| 0% (wszyscy na CPU) | 52,7–54,2 (wszystkie strategie) |
| 50% | losowo 70,4; równomiernie 65,3; przód 73,7; wg częstości 76,2; dynamicznie 81,2 |
| 100% | około 112–114 |

Wniosek, który z tego wynika (z danych projektu): przepustowość rośnie mniej więcej liniowo z ułamkiem ekspertów, które zdołasz trzymać w VRAM, a rozmieszczenie wg *częstości użycia* wygrywa z równomiernym. To jest najcenniejsza lekcja z całego KT i można ją (z grubsza) odtworzyć w llama.cpp, o czym w sekcji 7.

Ograniczenia: GPU tylko NVIDIA w gotowym kole; potrzebny serwerowy RAM; słabe skalowanie ze współbieżnością (obliczenia ekspertów na CPU są współdzielone); każda nowa rodzina modeli wymaga pracy "dnia zerowego", stąd długa lista tutoriali per model.

### 2.8 Dostrajanie (SFT) w skrócie

`kt-kernel/python/sft` (14,4 tys. linii Pythona) pozwala dostrajać modele MoE metodą LoRA oraz (od 2026-07) pełnym dostrajaniem parametrów w BF16, z ekspertami liczonymi na CPU. Jest zintegrowane z LLaMA-Factory (YAML w `examples/ktransformers/...`). README deklaruje 6–12× przyspieszenia wobec ZeRO-Offload "w testowanych zadaniach SFT MoE" i około 3,7 it/s dla DeepSeek-V3/R1 na 4× RTX 4090 *(dane projektu)*. Druga praca, "KTransformers-FineTune (KT-FT)", jest preprintem autorskim z 2026-10-08. Ciekawostka: LLaMA-Factory wymienia KT razem z Unsloth w sekcji "Practical tricks". Ten wątek jest poza naszym głównym tematem (uruchamianie modeli), więc poprzestaję na tym.

### 2.9 Praca offline

W `kt-kernel` (py/cpp/hpp) nie znalazłem żadnych śladów telemetrii (grep zwrócił pusty wynik). Modele trzeba raz pobrać z Hugging Face, koła z PyPI; potem całość działa offline. Samego SGLang tu nie audytowałem.

### Sprawdź sam: KT

> **Sprawdź sam 1: lista metod i opcje budowania** *(nie uruchamiałem tych poleceń; czytałem te pliki w klonie `kvcache-ai/ktransformers@a694e718`)*
> ```bash
> git clone --depth 1 https://github.com/kvcache-ai/ktransformers && cd ktransformers
> grep -n 'INFERENCE_METHODS' -A12 kt-kernel/python/experts.py
> grep -n 'KTRANSFORMERS_USE' kt-kernel/CMakeLists.txt
> ```
> Powinieneś zobaczyć zbiór nazw metod z tabeli wyżej oraz wzajemnie wykluczające się opcje CUDA/MUSA/ROCM/MACA/SYCL/ASCEND_NPU. Upewnij się samodzielnie, że nic w `doc/` nie wspomina gfx1201: `grep -rn -i 'gfx1201\|R9700' doc kt-kernel`.

> **Sprawdź sam 2: odroczenie ekspertów i hak w SGLang** *(nie uruchamiałem)*
> W repozytorium SGLang otwórz `python/sglang/srt/layers/moe/kt_ep_wrapper.py` i znajdź `submit_forward`. Potem w `kt-kernel/python/experts_base.py` poszukaj `select_deferred_experts` i `_layer_has_pending_deferred`. To pokazuje, że wynik ekspertów odroczonych dopisywany jest do wejścia następnej warstwy.

---

## 3. Porównanie: hybrydowy offload MoE

Skoro wiesz już, jak działa KT, zestawmy pięć podejść do tego samego problemu: **model MoE większy niż VRAM; część wag musi leżeć gdzie indziej**. Poniższe podejścia różnią się tym, *gdzie leżą zimne wagi*, *na jakim poziomie ziarnistości decydujesz o ich rozmieszczeniu* oraz *kto je liczy*.

### 3.1 Cztery pytania, według których porównuję

1. **Gdzie leżą "zimne" eksperty?** (RAM hosta czy SSD.)
2. **Jaka jest ziarnistość decyzji?** (Cały tensor warstwy, czy pojedynczy ekspert.)
3. **Kto liczy eksperty, które nie są na GPU?** (CPU czy GPU po doczytaniu.)
4. **Czy opóźnienie jest ukrywane?** (Nakładanie pracy.)

### 3.2 Tabela mechanizmów

| | **llama.cpp `-ot` / `--cpu-moe` / `--n-cpu-moe`** | **llama.cpp `--moe-cache-mib`** | **ik_llama.cpp** | **KTransformers (kt-kernel)** | **ds4, strumieniowanie z SSD** |
|---|---|---|---|---|---|
| Gdzie leżą zimne eksperty | RAM hosta | RAM hosta (+ bufor ekspertów na GPU) | RAM hosta | RAM hosta, podpule NUMA | **plik GGUF na SSD** + ograniczony cache ekspertów w pamięci |
| Ziarnistość | **tensor warstwy**: w GGUF każda warstwa ma jeden tensor 3-D na projekcję (`blk.N.ffn_{gate,up,down}_exps.weight`), więc rozmieszczasz *wszystkich ekspertów warstwy naraz* | **pojedynczy ekspert**: każda warstwa ma mapę slotów w pamięci hosta; brakujących ekspertów doładowuje callback kopiowania schedulera | jak llama.cpp (`-ot`); plus własny cache ekspertów (`Implement moe cache #2644`, 2026-10-12) i `--prefetch-experts` | **pojedynczy ekspert**: maska logiczna per warstwa (`generate_gpu_experts_masks`) | **pojedynczy ekspert** w cache; startowa "hotlista" wkompilowana w plik binarny |
| Kto liczy eksperty poza GPU | `ggml-cpu`, synchronicznie w grafie | eksperty w cache liczy karta; ci spoza cache trafiają przez kopię (patrz niżej) | CPU: własne jądra (`ggml/src/iqk/iqk_mul_mat*.cpp`) | CPU: własne jądra AMX/AVX512 z podziałem NUMA | akcelerator (Metal/CUDA/ROCm) po doczytaniu eksperta (*wynika z opisu w dokumentacji ds4*) |
| Ukrywanie opóźnienia | brak: obliczenie CPU jest krokiem w grafie | kopia ekspertów jest wywoływana z callbacku schedulera; stopnia nakładania z obliczeniami nie ustaliłem | nie czytałem kodu schedulera | host callback na strumieniu CUDA + odroczenie ekspertów | doczytywanie brakujących ekspertów "ukryte za" obliczeniem ekspertów współdzielonych (AGENT.md ds4) |
| NUMA | w notatkach nie ustaliłem | nie ustaliłem | nie ustaliłem | tak, wycinek każdego eksperta w pamięci lokalnej węzła | nie dotyczy |
| Format | GGUF | GGUF | GGUF; pliki z kwantami IQ_K/KT ładują się **tylko** w ik_llama.cpp | safetensors (FP8/BF16/INT4/GPTQ/MXFP4/NVFP4), GGUF tylko przez `LLAMAFILE` | specjalny GGUF z asymetryczną kwantyzacją, wąski zestaw modeli |

Źródła faktów: llama.cpp, flagi z `common/arg.cpp` linie 2758–2793 oraz `src/llama-moe-cache.h` w drzewie `0ce8cd1` (komentarz nagłówka: "keeps recently and repeatedly used experts of host-resident MoE layers in a device buffer"); ik_llama.cpp z README i historii commitów (kodu nie czytałem); KT z sekcji 2; ds4 z `docs/SSD_STREAMING.md` i `ds4_ssd.c`.

Co dzieje się w llama.cpp z ekspertami spoza GPU przy dużej paczce tokenów (**reguła *op-offload***, `ggml-backend.cpp`, `ggml-cuda.cu` linie 180–183 i 6011–6015): jeśli waga leży w pamięci hosta, a scheduler ma włączone `op_offload`, to każdy backend o wyższym priorytecie może przejąć operację, gdy `offload_op` się zgodzi. Dla CUDA/HIP warunek to `get_op_batch_size(op) >= op_offload_min_batch_size`, domyślnie **32** (zmienna środowiskowa `GGML_OP_OFFLOAD_MIN_BATCH`). Skutek: **prefill** na modelu częściowo wyniesionym przyspiesza ze wzrostem `-ub`, bo wagi są "strumieniowane" do GPU, natomiast generowanie (paczka 1) zostaje na CPU. W KT jest odwrotna filozofia prefillu: AMX na CPU ma być wystarczająco szybkie, żeby prefill nie wymagał przenoszenia wag (a przy długich promptach część pracy i tak wraca na GPU, patrz 2.4).

### 3.3 Tabela praktyczna: co to znaczy dla ciebie

| | `-ot` / `--n-cpu-moe` | `--moe-cache-mib` | ik_llama.cpp | KTransformers | ds4 |
|---|---|---|---|---|---|
| GPU AMD (RDNA4, gfx1201) | działa (backend HIP/ROCm, to obecny silnik konfiguracji referencyjnej) | ten sam backend; działanie na kartach R9700 nie było sprawdzone | HIP istnieje, ale jest drugorzędny; dla gfx1201 brak deklaracji | tylko budowa ze źródeł, bez deklaracji dla gfx1201 | ROCm celuje w gfx1151 (Strix Halo); gfx1201 tylko przez PR-y osób trzecich |
| Co potrzebujesz | RAM hosta | RAM hosta + trochę VRAM na cache | RAM hosta | serwerowe CPU z AMX/AVX512, 256+ GB RAM, karta NVIDIA | szybki SSD i pamięć na cache |
| Szybka ocena | najprostsze, dojrzałe | nowe (opis w nagłówku, flaga domyślnie wyłączona) | szybkie jądra CPU wg autora, ryzyko jednego maintainera i rozjazdu z upstreamem | najbardziej wyrafinowane, najcięższe wdrożenie | najbardziej "oszczędne" (wystarczy SSD), ale najwolniejsze i najwęższe |
| Przepustowość (dane projektu) | brak liczb w moich notatkach | brak liczb | brak niezależnych benchmarków; same raporty autora | tabela w 2.7 | M5 Max 128 GB: 11,9–19,3 tok/s dekodowania przy modelach 145–178 GiB; jedna R9700 32 GB z SSD: 4,70 tok/s generowania |

Uwagi do ostatniego wiersza: liczby ds4 pochodzą z jego dokumentacji `docs/SSD_STREAMING.md` (pomiary 2026-09-06 na M5 Max 128 GB, automatyczny cache, jeden przebieg) oraz z PR #558 (2026-07-13), gdzie autor PR-a na **jednej R9700 32 GB** (Ryzen 9 9950X3D, 128 GB DDR5, ROCm 7.2.2) uruchomił V4 Flash Q2 (około 81 GB) ze strumieniowaniem SSD i po obejściu zaszytej rezerwy 16 GiB VRAM uzyskał 6,33 tok/s prefillu i 4,70 tok/s generowania *(dane autora PR-a)*. To są **jedyne** dane z kart gfx1201 w tym zestawieniu, i nie wolno ich porównywać z tabelą KT (inny model, inny sprzęt, inna metryka).

### 3.4 Uczciwe wnioski z porównania

1. **Ziarnistość ma znaczenie.** `-ot` w llama.cpp podejmuje decyzję na poziomie tensora warstwy, więc nie wyrazisz "trzymaj na GPU 20 najczęstszych ekspertów warstwy 7". KT, `--moe-cache-mib` i ds4 pracują na poziomie pojedynczego eksperta. To główna różnica koncepcyjna.
2. **Kto liczy, to osobne pytanie.** KT inwestuje w *liczenie na CPU* (AMX/NUMA). Cache w llama.cpp i ds4 idą inną drogą: *przenieś eksperta tam, gdzie jest szybki akcelerator*. Pierwsza droga wygrywa, gdy CPU ma silne jednostki macierzowe i dużo kanałów pamięci. Druga, gdy łącze (PCIe, SSD) jest relatywnie szybkie, a wzorce użycia ekspertów powtarzalne.
3. **Nic z tego nie jest "darmowe".** Odroczenie ekspertów w KT zmienia obliczenia. Hotlista w ds4 jest wygenerowana z profilowania konkretnych modeli. Cache w llama.cpp i ik_llama.cpp jest świeży (ik_llama.cpp: 2026-10-12), więc nie ma jeszcze historii błędów.
4. **ik_llama.cpp to osobna historia.** Jego README mówi, że repozytorium zaczęło się jako fork llama.cpp w czerwcu 2024 i **ostatnio zsynchronizowano je z upstreamem w sierpniu 2024**. Modele powstałe później są przenoszone ręcznie. Dla hybrydowego MoE README przestrzega przed użyciem `-rtr` (przepakowanie w czasie działania) z ekspertami na CPU. Więcej o forku, tarciach z upstreamem i licencji: [`04-LLAMA-CPP-I-RODZINA-GGML.md`](04-LLAMA-CPP-I-RODZINA-GGML.md).

### Sprawdź sam: porównanie

> **Sprawdź sam 3: flagi offloadu w llama.cpp** *(sed z tych linii uruchomiłem na kopii na maszynie; samego greba nie)*
> W drzewie llama.cpp (build `0ce8cd1`):
> ```bash
> grep -n -E 'override-tensor|cpu-moe|moe-cache-mib|n-cpu-ffn' common/arg.cpp
> sed -n 1,20p src/llama-moe-cache.h
> ```
> W `arg.cpp` zobaczysz `-ot`, `-cmoe/--cpu-moe`, `-ncmoe/--n-cpu-moe`, `--moe-cache-mib` ("default: 0, disabled") i `-ncffn`. Nagłówek `llama-moe-cache.h` opisuje cache jednym zdaniem w komentarzu.
>
> **Sprawdź też u siebie:** `llama-server --help | grep -i -E 'moe|override-tensor'`. Jeśli twój build jest starszy niż `0ce8cd1`, flagi `--moe-cache-mib` może nie być.

---

## 4. mistral.rs

**Jednym zdaniem:** silnik wnioskowania napisany w Ruście (biblioteka + serwer zgodny z OpenAI i Anthropic + SDK Pythona), zbudowany na bibliotece tensorowej Candle od Hugging Face, z własną kwantyzacją (ISQ/UQFF), PagedAttention i wbudowaną pętlą agentową; **tylko CUDA, Metal i CPU**.

⚠️ **Najważniejsze dla rigu referencyjnego, na początku:** mistral.rs **nie ma w ogóle backendu ROCm ani Vulkan**. Grep po wszystkich plikach `.rs`, `.toml`, `.md`, `.mdx` w klonie nie znajduje żadnego wystąpienia "rocm" ani "vulkan". Na kartach R9700 go nie uruchomisz.

### 4.1 Tożsamość

- `EricLBuehler/mistral.rs`, licencja **MIT**, utworzone 2024-02-26, Rust. Wersja workspace **0.9.5 z 2026-10-19**; wcześniej 0.9.4 (2026-09-24) i 0.9.3 (2026-09-07). Minimalna wersja Rusta: 1.94.
- 7 759 gwiazdek, 738 forków, około 3 486 commitów. Najwięcej commitów: EricLBuehler 3 073, lucasavila00 125, LLukas22 54.
- README zaznacza: "mistral.rs is not affiliated with Mistral AI". Dokumentacja: https://docs.mistralrs.dev/.

**Kto za tym stoi.** Utrzymuje je jeden człowiek, **Eric Buehler**. Na jego profilu GitHub jako firma figuruje `@huggingface`, a punkt końcowy `orgs/huggingface/members/EricLBuehler` zwraca 204 (czyli jest publicznym członkiem organizacji). Stanowiska nie sprawdzałem, więc najmocniejsze, co mogę powiedzieć, to "powiązany z Hugging Face". Jest też czwartym autorem Candle (53 commity). **Finansowanie, firma, sponsorzy: nie znalazłem żadnych** (brak `FUNDING.yml`, brak sekcji sponsorów w README). **Czynnik jednego człowieka** (*bus factor*): w 90 dni do 2026-10-19 aż 75 z 82 commitów (bez botów) było jego. Licencja MIT pozwala na fork, ale nie na bezbolesne przejęcie projektu o 550 tys. linii. Więcej w [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

### 4.2 Po co to jest

Jeden silnik dla tekstu, obrazu, wideo, dźwięku na wejściu, mowy na wyjściu, generowania obrazów i embeddingów, z kwantyzacją rozwiązaną *wewnątrz* silnika: ładujesz dowolny checkpoint z Hugging Face i kwantyzujesz w locie. Użytkownik docelowy: budowniczy aplikacji w Ruście (crate `mistralrs`), użytkownik Pythona (`pip install mistralrs`) oraz osoba na **NVIDII albo Apple Silicon**. Czym nie próbuje być: silnikiem zgodnym ze wszystkimi plikami GGUF jak llama.cpp, silnikiem dla AMD/Intela, ani rozproszonym systemem serwującym jak vLLM.

### 4.3 Funkcje

- Modele: "45+ architektur" *(dane projektu)*, automatyczne wykrywanie architektury, formatu wag i szablonu czatu. LoRA i X-LoRA z wyborem adaptera per żądanie, AnyMoE, dekodowanie spekulatywne (`mistralrs-core/src/speculative`, 12,7 tys. linii).
- API: zgodne z OpenAI (`/v1`), **zgodne z Anthropic (`/v1/messages`)**, wbudowany interfejs `/ui`, metryki Prometheus `/metrics`, ładowanie i zwalnianie wielu modeli w czasie działania.
- **Funkcje agentowe:** wywoływanie narzędzi z wymuszaniem gramatyki i ścisłego schematu (llguidance, `pipeline/llg.rs`), **pętla agentowa po stronie serwera** (`engine/agentic_loop.rs`, 1 583 linie, oraz `tool_dispatch.rs`), trwałe sesje Pythona i sandbox shell (`mistralrs-code-exec` 3,2 tys. linii, `mistralrs-sandbox` 1,7 tys.), wyszukiwanie w sieci z rerankingiem, "Skills" w stylu OpenAI i **klient MCP** (`mistralrs-mcp`, 3,2 tys. linii) przez transporty Process / HTTP(+SSE) / WebSocket, z tokenem bearer i prefiksami nazw narzędzi.
- CLI: `mistralrs run | serve | bench | tune | doctor`. Polecenie `tune` "poleca kwantyzację i mapowanie na urządzenia" dla twojego sprzętu.

### 4.4 Sprzęt i formaty

- Funkcje Cargo w `mistralrs-core`: `cuda`, `cudnn`, `cutile`, `flash-attn`, `flash-attn-v3`, `metal`, `accelerate`, `mkl`, `nccl`, `ring`. Brak ROCm/HIP, Vulkan, SYCL i NPU. Dziedziczy to po Candle (CPU, CUDA, Metal, WASM; w README i drzewie Candle nie ma ROCm).
- Formaty: safetensors z HF, **GGUF** (`mistralrs-core/src/gguf`, 14,9 tys. linii; README podaje "2–8 bitów"), starszy GGML, **UQFF** (*Universal Quantized File Format*, oparty na safetensors, metadane `uqff.version.*`, aktualnie 1.2.0), a także wstępnie skwantyzowane GPTQ, AWQ, HQQ, FP8, bitsandbytes i MXFP4.
- **ISQ** (*in-situ quantization*, kwantyzacja na miejscu): wyliczenie `IsqType` w `mistralrs-quant/src/lib.rs` (linia 972) zawiera `Q4_0`…`Q8_1`, `Q2K`…`Q8K`, `HQQ8/4`, `F8E4M3`, `AFQ8/6/4/3/2`, `F8Q8`, `MXFP4`. Funkcja `IsqBits::{Two..Eight}.resolve(device)` zamienia "N-bit" na **AFQ\* na Metal** (kwantyzacja afiniczna grupowa w stylu MLX) oraz **Q\*K (układ k-quantów ggml) na CUDA/CPU**. To ciekawy wzorzec: jedno pokrętło "4 bity", a typ zależy od platformy. W typach ISQ **nie ma kwantów IQ** (i-quants), choć ścieżka GGUF może je czytać (kompletności nie sprawdzałem). Obsługuje też macierz ważności (`imatrix.rs`).

### 4.5 Architektura (klon `EricLBuehler/mistral.rs@465191d0`, 2026-10-19)

**Rozmiar.** Około 550 tys. linii Rusta w workspace, czyli więcej niż sam `src/` llama.cpp, bo każdą architekturę modelu napisano ręcznie w Ruście (w llama.cpp to konstruktory grafów ggml). Największe katalogi: `mistralrs-core` 347,5 tys. (w tym `vision_models` 85,3 tys., `pipeline` 62,8 tys., `models` 25,0 tys., `paged_attention` 22,6 tys., `cuda` 17,6 tys., `gguf` 14,9 tys., `speculative` 12,7 tys., `engine` 8,6 tys., `scheduler` 1,0 tys.), `mistralrs-quant` 109,7 tys. Rusta plus około 63 tys. linii jąder CUDA/Metal/C.

**Zależność od Candle.** `Cargo.toml` przypina `candle-core/-nn/-flash-attn-v3/-metal-kernels` do **rewizji gita z upstreamowego `huggingface/candle`** (`rev = 66a8cf18…`, wersja 0.11.0), a nie do prywatnego forka. Candle 0.11.0 to najnowszy tag; `candle-core` ma 56 tys. linii, `candle-transformers` (referencyjne porty modeli) 83 tys. mistral.rs dokłada: własne mnożenia macierzy dla skwantowanych wag, PagedAttention, integrację FlashInfer, dekodowanie z grafami CUDA, rozproszenie NCCL i "ring" oraz jądra cuTile FP8 (wymagają narzędzia NVIDII `tileiras`).

**Przepływ żądania:** HTTP (axum 0.8, `mistralrs-server-core`) → uchwyt `MistralRs` → zadanie `Engine` (`engine/mod.rs`, 2 525 linii; główna pętla `'lp: loop` w `Engine::run`, okolice linii 1119). Silnik (1) opróżnia kanał żądań (`add_request.rs`, 1 242 linie: tokenizacja, szablon, cechy multimodalne, szukanie w cache prefiksów, kontrola przyjęć w `admission.rs`), (2) wywołuje `scheduler.schedule(...)` (linia ok. 1414), (3) wykonuje **krok potoku** (`Pipeline::step`) dla prefillu lub dekodowania, (4) próbkuje (`sampler.rs`), strumieniuje tokeny i obsługuje narzędzia lub pętlę agentową. Potoki są per modalność: `normal.rs`, `gguf.rs`, `ggml.rs`, `multimodal.rs`, `diffusion.rs`, `speech.rs`, `embedding.rs`, `auto.rs`.

**Scheduler** (`scheduler/mod.rs`): dwie implementacje. `DefaultScheduler` (FCFS ze stałymi koszykami) i `PagedAttentionScheduler` (`paged_attention/scheduler.rs`; ciągłe batchowanie z wywłaszczaniem, `max_num_seqs`, `max_num_batched_tokens` domyślnie **4096**, `max_prefill_chunk_tokens` **512**, `max_decode_steps_before_prefill` **8**). Prefill porcjowany jest przeplatany z dekodowaniem tymi pokrętłami.

**Pamięć podręczna KV:** PagedAttention = pula bloków (`block_pool.rs`), haszowanie bloków dla cache prefiksów także multimodalnych (`block_hash.rs`, `mm_prefix.rs`), osobna pula dla warstw z oknem przesuwnym (`windowed_pool.rs`). Jądra CUDA w `mistralrs-paged-attn/src/cuda` mają w źródłach przestrzeń nazw `vllm::`, czyli zostały przeniesione z vLLM. **PagedAttention działa tylko na CUDA i Metal** (README); ścieżka CPU ma zwykły cache (`kv_cache/`).

**Przepływ ISQ** (`pipeline/isq.rs`, `isq_flow/`): wagi ładowane są warstwa po warstwie w oryginalnym typie, kwantyzowane na urządzeniu docelowym (albo CPU) w miarę napływania. Założenie projektowe: "bez osobnego kroku konwersji". Szczytowe zużycie pamięci ma więc być rzędu jednej warstwy plus suma skwantowanych *(twierdzenie o pamięci niezweryfikowane)*. UQFF zapisuje wynik, żeby koszt kwantyzacji zapłacić raz.

**Pięć decyzji projektowych:**
1. Rust + Candle: bezpieczeństwo pamięci, jeden plik wykonywalny, łatwe osadzenie.
2. Kwantyzacja jako funkcja silnika, a nie ekosystem formatów plików.
3. Własny serwer z narzędziami agentowymi (narzędzia, MCP, sandbox), zamiast zostawiania tego klientom.
4. Typy kwantyzacji zależne od platformy (AFQ na Metal, k-kwanty na CUDA/CPU) za jednym pokrętłem.
5. Głównie jeden proces i jeden węzeł (NCCL/ring dla wielu kart).

### 4.6 Wydajność

Jedyne liczby to własny benchmark z README (wersja 0.8.2): Gemma 4 E4B na **B200**, prefill Q8 27 705,6 tok/s wobec 11 992,4 dla llama.cpp; prefill BF16 43 547,8 wobec 39 431,2 dla vLLM; dekodowanie 202,6 wobec 196,2 tok/s *(dane projektu)*. To jedna klasa GPU z centrum danych i jeden mały model, więc niereprezentatywne dla kart konsumenckich ani AMD. Niezależnych pomiarów nie znalazłem. Rzeczy wpływające na opóźnienie: dekodowanie z grafami CUDA, FlashAttention V2/V3, FlashInfer, cache prefiksów.

### 4.7 Mocne i słabe strony (wobec llama.cpp)

**Mocne:** jeden silnik czyta checkpointy HF *i* GGUF; ISQ oznacza "pobierz dowolny model i uruchom w 4 bitach" bez konwersji; osadzalne SDK w Ruście i Pythonie; API OpenAI i Anthropic oraz wbudowana pętla agentowa i MCP; PagedAttention z ciągłym batchowaniem (serwer llama.cpp ma batchowanie slotowe, ale nie stronicowanie KV w sensie vLLM) w jednym pliku.

**Słabe:** brak AMD/Intel/Vulkan (dyskwalifikuje na kartach R9700); mniej więcej 90% commitów jednej osoby; pokrycie modeli i zgodność numeryczna gonią upstream ręcznym portowaniem; mniej sprawdzone w boju (7,8 tys. gwiazdek wobec ponad 100 tys. dla llama.cpp, *wartość dla llama.cpp niezweryfikowana w moich notatkach*).

**Kiedy silnik w Ruście ma sens?** Gdy dostarczasz produkt napisany w Ruście i chcesz wnioskowania w procesie bez łańcucha budowania C++ i FFI. Gdy ważne jest bezpieczne w pamięci przetwarzanie niezaufanych plików modeli i wykonywania narzędzi. I gdy jesteś na NVIDII albo Apple Silicon. Gdy potrzebujesz Vulkana/ROCm/Intela albo największego ekosystemu GGUF, bierzesz llama.cpp.

### 4.8 Praca offline

Brak kodu telemetrii (grep po `.rs`/`.toml` znajduje tylko trafienia w komentarzach serwera). Respektuje `HF_HUB_OFFLINE` (`pipeline/hf.rs:26`, `lib.rs:170`). `mistralrs doctor` sprawdza CUDA/Metal i łączność z HF. Skrypt instalacyjny pobiera pliki z mistralrs.dev, a wyszukiwanie w sieci i MCP/zdalne pobieranie (`remote_fetch.rs`) wychodzą na zewnątrz, jeśli je włączysz.

### 4.9 Candle w kilku zdaniach

`huggingface/candle`: Apache-2.0 (pliki licencji MIT i Apache), 21,2 tys. gwiazdek, utrzymywane przez Hugging Face. Autor oryginału, **Laurent Mazare** (1 603 commity), podaje teraz w profilu "Co-founder Kyutai & Gradium"; dziś projekt niosą m.in. Nicolas Patry (275 commitów) i **Ivar Flakstad** (126). W 3 miesiące do 2026-10-19 było tam około 40 commitów (dependabot 12, ivarflakstad 10, EricLBuehler 7). Wniosek: Candle żyje, ale z niską intensywnością i zależy od HF. mistral.rs śledzi rewizję gita zamiast wydań z crates.io.

### 4.10 Co z tego wziąć dla swoich aplikacji

- **Wzorzec `IsqBits → typ zależny od platformy`** i polecenie `tune` (sprzęt → kwantyzacja + mapa urządzeń) to dobre pomysły na UX dla własnego launchera lokalnych modeli.
- **Pętla agentowa i klient MCP wewnątrz silnika** to alternatywna architektura wobec "klient prowadzi pętlę". Zastanów się, czy wykonywanie narzędzi należy do silnika (opóźnienia, ponowne użycie cache prefiksów między turami narzędzi) czy do twojego orkiestratora (bezpieczeństwo, obserwowalność).
- **Na Macach:** to wiarygodny drugi silnik Metal obok MLX (kwanty AFQ są w stylu afinicznym MLX). Zmierz na własnym modelu, zanim zaufasz README.

### Sprawdź sam: mistral.rs

> **Sprawdź sam 4: brak ROCm i Vulkan** *(nie uruchamiałem tej linijki; wynik "pusto" ustaliłem tym samym grepem na moim klonie)*
> ```bash
> git clone --depth 1 https://github.com/EricLBuehler/mistral.rs && cd mistral.rs
> grep -rniE 'rocm|vulkan' --include='*.rs' --include='*.toml' --include='*.md' --include='*.mdx' . | head
> grep -n -A12 '^\[features\]' mistralrs-core/Cargo.toml
> ```
> Pierwsze polecenie powinno nic nie zwrócić, drugie pokaże cechy `cuda`, `metal`, `mkl` i resztę z listy w 4.4. Stałe schedulera znajdziesz w `mistralrs-core/src/scheduler/mod.rs` (szukaj `4096`, `512`).

---

## 5. MLC LLM i WebLLM

### 5.1 Idea: kompilacja modelu zamiast "interpretera"

Silnik taki jak llama.cpp to rodzaj *interpretera*: jeden program zna wiele architektur i dla każdego tokenu przechodzi po grafie operacji, wywołując gotowe jądra dla twojego backendu. **MLC LLM** ("Universal LLM Deployment Engine with ML Compilation", tak brzmi opis repozytorium) idzie inną drogą: **kompiluje** model razem z wyborem jąder pod konkretne urządzenie. Wynikiem jest biblioteka (plik `.so`/`.dylib`/`.dll`/`.tar`/`.wasm`) plus wagi. Ten sam model da się w ten sposób uruchomić przez CUDA, ROCm, Vulkan, Metal, OpenCL, WebGPU, na iOS i Androidzie.

Analogia: zamiast tłumacza, który na bieżąco tłumaczy książkę na różne języki, drukujesz osobne wydanie książki dla każdego kraju. Szybsze czytanie, ale osobna praca dla każdego wydania. Precyzyjnie: kompilacja per model *i* per urządzenie jest zarówno źródłem przenośności, jak i głównym tarciem.

### 5.2 Jak wygląda przepływ kompilacji

Trzy kroki (dokumentacja `compilation/compile_models.rst`, https://llm.mlc.ai):

1. **`convert_weight`**: kwantyzacja wag do formatu MLC.
2. **`gen_config`**: zapis `mlc-chat-config.json`.
3. **`compile`**: Apache TVM obniża program (Relax/TIR) do biblioteki modelu dla wybranego celu.

Modele definiuje się **w Pythonie** za pomocą frontendu `nn.Module` z TVM (`python/mlc_llm/model/<arch>/`, około 29 tys. linii; instrukcja `docs/compilation/define_new_models.rst`). W katalogu modeli widać m.in. Qwen3.5, Gemma 4, Ministral3, Llama 4 i DeepSeek-V2, więc projekt nadąża za nowymi architekturami z opóźnieniem.

Rejestr kwantyzacji `QUANTIZATION` w `python/mlc_llm/quantization/quantization.py` zawiera m.in. `q0f16/q0bf16/q0f32` (bez kwantyzacji), `q3f16_0/_1`, `q4f16_0/_1/_2`, `q4bf16_*`, `q4f32_1` (kwantyzacja grupowa), `q4f16_autoawq`, `q4f16_ft` oraz warianty FP8 i skalowane blokowo. Nazwa koduje liczbę bitów, typ aktywacji i wariant. **MLC nie czyta GGUF.** To znaczy, że cały zbiór `UD-*` z Hugging Face jest dla niego bezużyteczny; musisz przekonwertować z oryginalnych wag.

### 5.3 Środowisko uruchomieniowe i zależności

Część serwująca w C++ (`cpp/serve`, 7,3 tys. linii w plikach `.cc`): `engine.cc` (1 102 linie), `model.cc` (1 345), `threaded_engine.cc`, katalog `engine_actions/` (prefill nowych żądań, dekodowanie wsadowe, weryfikacja/szkic dla dekodowania spekulatywnego, EAGLE, dekodowanie "jump-forward" dla gramatyk, **rozdzielony prefill i dekodowanie** w plikach `disagg_*`), `prefix_cache.cc` + `radix_tree.cc` (cache prefiksów w drzewie radix), `sampler/`, `logit_processor.cc`. Stronicowany cache KV mieszka w środowisku TVM. Podmoduły gita: `3rdparty/tvm` wskazuje na **fork `mlc-ai/relax`** (175 gwiazdek, ostatni push 2026-10-04), `tokenizers-cpp`, **`xgrammar`** (generowanie strukturalne) i `argparse`. Warstwa Pythona: `mlc_llm serve` (REST zgodny z OpenAI), `MLCEngine`, `AsyncMLCEngine`, wiele GPU przez "disco".

Macierz sprzętu z README: AMD GPU "Vulkan, ROCm" (Linux/Windows), NVIDIA "Vulkan, CUDA", Apple "Metal", Intel "Vulkan"/Metal iGPU, Web "WebGPU i WASM", iOS Metal, Android OpenCL (Adreno/Mali). **Jakość wsparcia w poszczególnych komórkach tej macierzy jest dla mnie nieznana**; w szczególności wydajność na konsumenckich kartach ROCm nie jest udokumentowana w moich źródłach.

### 5.4 Stan projektu w 2026: żywy, ale wolny

- `mlc-ai/mlc-llm`, **Apache-2.0**, utworzone 2023-04-29, 23 258 gwiazdek, 2 292 forki; Python 62,9 tys. + C++ 22,5 tys. linii (klon `@8978ea9a`, 2026-10-06).
- Ostatni commit 2026-10-06. Commity w oknach czasowych (API): **98 w ostatnich 12 miesiącach, 26 w ostatnich 6 miesiącach wobec 72 w 6 miesiącach wcześniej**. 11 z 26 niedawnych commitów to jeden miesiąc (2026-09), autor `akaashrp`.
- **Wersjonowanie jest niejasne**: w zakładce Releases GitHuba jest tylko `v0.1.dev0` z 2023; tagi z API to `v0.26.dev0`, `v0.20.0` i `v0.20.dev0` (daty commitów tagów 2026-06-28 i 2026-07-07, w niespójnej kolejności). Dystrybucja idzie przez nocne koła `mlc-ai-nightly` (z dokumentacji; nie sprawdzałem).

**Kto za tym stoi.** Bez firmy, bez finansowania, bez przychodów powiązanych z repozytorium *(nie znalazłem)*. Rodowód: Apache TVM (Tianqi Chen, 2016, UW; `apache/tvm` 13,8 tys. gwiazdek, aktywne) i projekt MLC z CMU Catalyst oraz OctoAI. **Tianqi Chen** jest profesorem nadzwyczajnym na CMU i Distinguished Engineer w NVIDII, a w latach 2019–2024 był Chief Technologist w OctoAI, które NVIDIA przejęła *(strona tqchen.com)*. Główni autorzy commitów: MasterJH5574 (Ruihang Lai, CMU), junrushao (Junru Shao), tqchen, CharlieFRuan (Charlie Ruan), vinx13, yzh119. Podmiot z finansowaniem w tym rodowodzie (OctoAI) nie istnieje już samodzielnie. Szczegóły: [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

### 5.5 Mocne i słabe strony

**Mocne:** jedyny stos w tym zestawieniu, który z jednego potoku kompilacji celuje w telefony, przeglądarkę, AMD, Intela, NVIDIĘ i Apple; poważny rodowód badawczy; xgrammar do wyjść strukturalnych; w kodzie są wzorce serwerowe (cache prefiksów w drzewie radix, rozdzielony prefill i dekodowanie).

**Słabe:** kompilacja per urządzenie per model; niski i spadający rytm commitów; brak GGUF; zależność od forka TVM; wydajność na kartach ROCm w moich źródłach nieudokumentowana.

**Praca offline:** po pobraniu modelu całość jest lokalna; w `python/` i `cpp/` nie ma śladów telemetrii (grep zwraca tylko niezwiązane trafienia). W dokumentacji jest plik `privacy.rst`.

### 5.6 WebLLM: ten sam stos w karcie przeglądarki

`mlc-ai/web-llm`, Apache-2.0, TypeScript, 19 284 gwiazdki, pakiet npm `@mlc-ai/web-llm`, wydanie **v0.2.86 (2026-10-11)**; rytm mniej więcej miesięczny (v0.2.85 z 2026-09-08, v0.2.83 z 2026-04-24).

Uruchamia model skompilowany przez MLC jako jądra **WebGPU** plus środowisko WASM, **w całości w karcie przeglądarki**. Ma interfejs JS w kształcie API OpenAI, strumieniowanie, tryb JSON (xgrammar), wstępne wywoływanie funkcji, hostowanie w Web Workerze i Service Workerze oraz przykład rozszerzenia Chrome. Wagi trafiają do Cache API, IndexedDB lub OPFS. Praca naukowa: *WebLLM: A High-Performance In-Browser LLM Inference Engine*, arXiv 2412.15803, Ruan i in. z Tianqi Chenem; deklaruje "do 80% wydajności natywnej na tym samym urządzeniu" *(dane autorów, streszczenie arXiv)*. Autorzy commitów: CharlieFRuan 192, akaashrp 49, Neet-Nestor 46.

Dlaczego to ważne: zero instalacji, brak serwera, dane użytkownika nigdy nie opuszczają urządzenia. Ograniczenia: dostępność WebGPU, limity VRAM per origin, wielogigabajtowe pierwsze pobranie, małe modele. Dla budowniczego aplikacji agentowych to **prywatny fallback po stronie klienta albo cel dla dema**, a nie silnik serwerowy. Pamiętaj też, że llama.cpp ma już backend `ggml-webgpu` (21 tys. linii w drzewie `0ce8cd1`), więc wnioskowanie w przeglądarce nie jest wyłącznością MLC.

### Sprawdź sam: MLC

> **Sprawdź sam 5: rejestr kwantyzacji i brak GGUF** *(nie uruchamiałem)*
> ```bash
> git clone --depth 1 https://github.com/mlc-ai/mlc-llm && cd mlc-llm
> grep -n 'QUANTIZATION' -A40 python/mlc_llm/quantization/quantization.py | head -60
> grep -rli 'gguf' python | head
> ```
> Pierwsze polecenie pokaże rejestr (`q4f16_1` i spółka). Drugie sprawdza, czy w warstwie Pythona jest jakakolwiek obsługa GGUF (moje czytanie: brak; sprawdź samodzielnie i nie traktuj pustego wyniku jako dowodu bez przejrzenia trafień).

---

## 6. Stosy NPU i stosy producentów

NPU (*Neural Processing Unit*) to układ w procesorze laptopa lub telefonu, projektowany do mnożenia macierzy przy małym poborze mocy. Dla ciebie jest to temat poboczny: **żaden z tych stosów nie dotyka kart Radeon ani Linuxa z ROCm**. Poznaj je po to, żeby rozumieć mapę i nie mylić nazw.

### 6.1 Przegląd

| Stos | Producent | Na czym działa | Format modeli | Licencja | Wersja (dane z API) | Dojrzałość |
|---|---|---|---|---|---|---|
| **ONNX Runtime GenAI** | Microsoft | CPU, CUDA, DirectML, NvTensorRtRtx, OpenVINO, **QNN**, WebGPU; AMD GPU "w planach"; w drzewie `src/ep/{amdgpu,ryzenai,vitisai}` | **ONNX** (z wbudowanego *model buildera*) | MIT | v0.17.0 (2026-09-28) | produkcyjny wewnątrz produktów Microsoftu |
| **OpenVINO GenAI** | Intel | CPU, iGPU/Arc, **NPU** (Core Ultra); Linux/Windows/macOS | **OpenVINO IR** (przez `optimum-cli export openvino`) | Apache-2.0 | 2026.4.1.0 (2026-10-01) | solidny projekt korporacyjny |
| **Qualcomm GenieX** (dawniej NexaSDK) | Qualcomm | **Hexagon NPU, Adreno GPU, CPU**; Windows ARM64, Android, Linux ARM64 | GGUF (przez llama.cpp) albo paczki per chipset z Qualcomm AI Hub (QAIRT) | BSD-3-Clause | v0.9.1 (2026-10-17) | bardzo aktywny, przed 1.0 ("developer preview" od 2026-06-30) |
| **AMD Ryzen AI / OGA** | AMD | NPU + iGPU "hybrid" albo samo NPU; procesory Strix i Krackan Point; Windows | ONNX przez ONNX Runtime GenAI z dostawcą VitisAI/Ryzen AI | (z tabeli ONNX Runtime GenAI) | OGA 0.14.0 w momencie tej strony | dokumentacja AMD |

Dodatkowo, **dla porządku**: Apple Foundation Models to interfejs Swift do *systemowego modelu na urządzeniu* z kierowanym generowaniem i wywoływaniem narzędzi. Nie ma wyboru modelu, jest związany z platformą i nie jest ogólnym silnikiem (w odróżnieniu od MLX, rozdział [`07-APPLE-MLX-OMLX-I-DS4.md`](07-APPLE-MLX-OMLX-I-DS4.md)). Opis pochodzi ze strony Apple, którą pobrałem w postaci szczątkowej.

### 6.2 ONNX Runtime GenAI i OpenVINO GenAI

**ONNX Runtime GenAI** (`microsoft/onnxruntime-genai`, MIT, C++ 107,7 tys. linii w `src/`, 1 140 gwiazdek). README opisuje je jako "pętlę generatywnej AI dla modeli ONNX": przetwarzanie wstępne i końcowe, wnioskowanie przez ONNX Runtime, przetwarzanie logitów, przeszukiwanie i próbkowanie oraz zarządzanie cache KV. Zasila Foundry Local, Windows ML i AI Toolkit dla VS Code. Czyli to **biblioteka pętli nad dostawcami wykonania** ONNX Runtime, a nie biblioteka jąder. Wiązania: Python, C#, C/C++, Java. W katalogu `src/engine/` (13 tys. linii: `scheduler.cpp`, `paged_key_value_cache.cpp`, `prefix_cache.cpp`) jest już silnik z ciągłym batchowaniem i stronicowanym KV obok starszego API `Generator` (dojrzałość nieznana). Brak GGUF: modele przechodzą przez `src/python/py/models/builder.py` (1 273 linie), który produkuje zoptymalizowane i skwantowane modele ONNX.

⚠️ **Telemetria w oficjalnych pakietach jest domyślnie włączona** (SDK 1DS, HTTPS do Microsoftu). Wyłączysz ją przez `ORT_DISABLE_TELEMETRY=1`, flagę `--no_telemetry` przy budowie albo przez API (`docs/Privacy.md`, `cmake/options.cmake`).

**OpenVINO GenAI** (`openvinotoolkit/openvino.genai`, Apache-2.0, C++, 602 gwiazdki, 481 forków; numeracja kalendarzowa OpenVINO). Rurociągi: `LLMPipeline`, VLM, generowanie obrazów (Diffusers), Whisper, SpeechT5, embeddingi i reranking. Funkcje: dekodowanie spekulatywne, eksmisja KV, rzadka uwaga, **ciągłe batchowanie**, cache prefiksów, multi-LoRA. API w C++/Pythonie/Node.js. Klon repozytorium miałem niepełny (checkout git-lfs się nie powiódł), więc **nie wypowiadam się o kodzie**. Pamiętaj, że llama.cpp ma teraz `ggml-openvino` (19,6 tys. linii, `docs/backend/OPENVINO.md`), więc sprzęt Intela osiągniesz dwiema drogami. Intel zarchiwizował `intel-extension-for-pytorch` (2026-03-30; optymalizacje przeniesiono do PyTorcha). Telemetrii OpenVINO GenAI nie sprawdzałem.

### 6.3 Qualcomm GenieX: korekta typowego obrazu

`qualcomm/GenieX` **nie jest** nowym silnikiem napisanym w Go od zera. GitHub przekierowuje `NexaAI/nexa-sdk` na `qualcomm/GenieX` (ten sam identyfikator repozytorium 843570824, utworzone 2024-08-16, tagi wydań sięgają `v0.2.16` z 2025-08-07). Najczęstsi autorzy commitów to `mengshengwu`, `RemiliaForever`, `zhycheng614`, `zhiyuan8`, `Davidqian123`, `alexchen4ai`, `alanzhuly` (skojarzenie tych nazw z Nexa AI jest *niezweryfikowane*). README mówi o "środowisku wykonawczym generatywnej AI na urządzeniach Qualcomma" i "wersji społecznościowej Qualcomm GENIE", nie wspominając o Nexa ani o zmianie nazwy. Historia ma commit `init commit` z 2026-04-10 i 2 475 commitów; wydanie **v0.9.1 (2026-10-17)**, 8 448 gwiazdek, licencja **BSD-3-Clause**. **Warunków przejścia z Nexa do Qualcomma (przejęcie? współpraca?) nie ustaliłem w żadnym dostępnym źródle.**

Architektura (`CONTRIBUTING.md`, `.gitmodules`, drzewo): **CLI w Go** (`cli/`, gin + cobra, budowa Bazelem) → **most SDK w C** (`sdk/`, CMake; `llm.cpp`, `vlm.cpp`, `ml.cpp`, `registry.cpp`) → **wtyczki** `sdk/plugins/llama_cpp` (vendorowany podmoduł `third-party/llama.cpp`) i `sdk/plugins/qairt` (vendorowany `qualcomm/geniex-qairt-plugin`, biblioteki **Qualcomm AI Engine Direct / QAIRT**, wybierane flagą `--qairt-lib`), do tego `model-manager` w Ruście, wiązania Python/Kotlin/Java/Docker i serwer zgodny z OpenAI. Formaty: **GGUF** (README poleca **Q4_0**, bo "najlepsze wsparcie Hexagon NPU") albo gotowe paczki per chipset z Qualcomm AI Hub przez QAIRT, tylko NPU. Warunki "Qualcomm Terms of Use" wspomniane w README i ewentualną telemetrię **pozostawiam niezbadane**. Lekcja: stosy NPU producentów zbiegają do "llama.cpp plus runtime producenta"; jednocześnie sam llama.cpp ma backend `ggml-hexagon` (53 tys. linii, `docs/backend/snapdragon`).

### 6.4 AMD Ryzen AI

AMD uruchamia LLM na NPU przez **ONNX Runtime GenAI (OGA) z dostawcą wykonania Ryzen AI / VitisAI**. Według dokumentacji AMD wspierane są wyłącznie procesory **Strix i Krackan Point** (nie Phoenix/Hawk), w trybie **hybrydowym** (NPU + iGPU; "najlepszy TTFT i TPS podczas prefillu i dekodowania") albo samym NPU ("Token Fusion" do 16K tokenów, "Full Fusion" do 4 096), instrukcje tylko dla Windows *(dane firmy: https://ryzenai.docs.amd.com/en/latest/hybrid_oga.html)*. AMD publikuje wstępnie zoptymalizowane modele Llama, Mistral, Qwen, Gemma i Phi. Kod w drzewie ONNX Runtime GenAI (`src/ep/ryzenai`, `src/ep/vitisai`, `src/ep/amdgpu`, "Copyright 2026 Advanced Micro Devices") potwierdza integrację. **Nic z tego nie dotyka dyskretnych kart Radeon ani Linuxa z ROCm.** Lemonade (opisany w [`05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md`](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md)) pakuje ten stos razem z llama.cpp.

### 6.5 Kto za tym stoi (stosy producentów)

Wszystkie cztery to **oprogramowanie sprzedające krzem**: Microsoft (platforma Windows), Intel (CPU/NPU Core Ultra), Qualcomm (Snapdragon), AMD (Ryzen AI). Model biznesowy to "narzędzie za darmo, żeby sprzęt miał oprogramowanie". Skutek praktyczny: priorytety podążają za układami, które producent akurat sprzedaje. Dla kart R9700 najbliższy "sojusznik" AMD to Lemonade, ale celuje w APU i konsumenckie PC, nie w serwery z czterema kartami *(moja ocena z [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md), niezweryfikowana)*.

### Sprawdź sam: NPU

> **Sprawdź sam 6: GenieX to dawny NexaSDK** *(nie uruchamiałem tej linijki; przekierowanie ustaliłem przez API GitHuba)*
> ```bash
> gh api repos/NexaAI/nexa-sdk --jq '{full_name, id, stargazers_count, license: .license.spdx_id}'
> ```
> Powinno wrócić `qualcomm/GenieX` z identyfikatorem 843570824. Do `gh` zwykle potrzebujesz zalogowanej sesji. Potem otwórz `.gitmodules` w repozytorium i sprawdź, że `third-party/llama.cpp` jest podmodułem.

---

## 7. Co z tego dla konfiguracji referencyjnej

### 7.1 Zacznijmy od uczciwego pytania: czy w ogóle masz problem, który to rozwiązuje?

Model referencyjny to DeepSeek-V4-Flash w kwantyzacji `UD-IQ3_XXS`, 284 mld parametrów, uruchamiany w llama.cpp na 4× R9700 (4 × 32 GB nominalnie; w rzeczywistości 4 × 34,2 GB = 136,8 GB) z prędkością około 50 tok/s. Hybrydowy offload MoE ma sens, gdy wagi *nie mieszczą się* w VRAM — na rigu referencyjnym się mieszczą. Plik referencyjny ma 104,2 GB (4 części GGUF; zmierzone), czyli średnio ok. 2,9 bita na wagę (104,2 GB × 8 / 284 mld, *moje wyliczenie*; zob. [`03-KWANTYZACJA-I-FORMATY.md`](03-KWANTYZACJA-I-FORMATY.md) — `UD-IQ3_XXS` to mieszanka typów tensorów, więc średnia zależy od składu). Karty mają razem 136,8 GB (4 × 34,2 GB; zob. [`03`](03-KWANTYZACJA-I-FORMATY.md)), więc plik się mieści i zostaje ok. 32 GB (*moje wyliczenie*) na pamięć podręczną KV i bufory (z czego korzysta kontekst 2 × 98 304 tokenów z produkcji).

Dwa wnioski:

1. **Jeśli model siedzi w VRAM w całości, żaden z mechanizmów z sekcji 3 nie jest ci potrzebny do tego modelu.** To dobra wiadomość: 50 tok/s na takiej konfiguracji to dobry znak, że nic nie wędruje przez wolne łącze.
2. **Mechanizmy offloadu zaczynają mieć znaczenie, gdy:** (a) wybierzesz większą kwantyzację tego samego modelu (np. coś w okolicy Q4, która przekroczy 128 GB), (b) chcesz dłuższego kontekstu kosztem VRAM, (c) pojawi się większy model (rodzina DeepSeek V4 PRO ma 1,6 bln parametrów łącznie, 49 mld aktywnych, według `MODEL_CARD.md` w ds4).

### 7.2 Które pomysły mogą mieć znaczenie

| Pomysł | Skąd | Jak go użyć w llama.cpp na maszynie referencyjnej |
|---|---|---|
| **Rozmieszczenie wg częstości użycia ekspertów** | KT: strategia `frequency`; wg danych projektu wygrywa z równomiernym (tabela w 2.7) | Nie masz tej ziarnistości w `-ot` (tensor warstwy), ale możesz *wybierać warstwy* do `--n-cpu-moe`/`-ot`, kierując się własnymi statystykami (np. które warstwy mają najbardziej "płaski" rozkład użycia). Pomiar jest pracą własną; **nie sprawdzałem**, czy llama.cpp ma gotowe narzędzie do zbierania statystyk użycia ekspertów. |
| **Cache ekspertów na GPU** | llama.cpp `--moe-cache-mib` (domyślnie wyłączone); ds4 (cache + hotlista) | Najbliższy odpowiednik idei KT na stosie referencyjnym. Eksperyment przy większej kwantyzacji: ustaw rozmiar cache i porównaj tok/s. **Nie wiem**, jak działa na gfx1201 (nikt tego w moich źródłach nie mierzył); to jest do własnego pomiaru. |
| **Przypięcie wątków i NUMA** | KT: `hwloc`, wątek na rdzeń fizyczny | Jeśli host ma dwa gniazda, `numactl` lub równoważne przypięcie ma znaczenie przy każdym oparciu o RAM. Konfiguracji CPU maszyny referencyjnej nie znam, więc tylko wskazuję. |
| **Odroczenie ekspertów** | KT | **Nie ma odpowiednika w llama.cpp.** Zapamiętaj jako pomysł; bez zmian w kodzie silnika nie zrobisz. |
| **ISQ i `tune`: "jedno pokrętło bitów" + rekomendacja z sprzętu** | mistral.rs | Wzorzec UX dla własnego launchera przy `llama-swap`. |
| **Pętla agentowa i MCP w silniku** | mistral.rs | Decyzja architektoniczna dla twoich aplikacji: gdzie wykonywać narzędzia (silnik czy orkiestrator). Dla CUDA/Mac; nie na R9700. |
| **WebLLM** | MLC | Prywatny fallback po stronie klienta albo demo w przeglądarce; nie runtime serwerowy. |

### 7.3 Co jest dla ciebie nieistotne (świadomie pomijaj)

- **mistral.rs na R9700**: brak ROCm i Vulkan. Natomiast **na Macach** jest wiarygodnym drugim silnikiem Metal obok MLX, więc ewentualnie do zmierzenia tam.
- **Gotowe koło KTransformers**: tylko NVIDIA SM 80–90 i wymaga serwerowego RAM-u (minimum 256 GB). Na R9700 to budowa ze źródeł bez deklaracji wsparcia.
- **Stosy NPU** (ONNX Runtime GenAI, OpenVINO GenAI, GenieX, Ryzen AI): to Windows, Snapdragon, Core Ultra i APU AMD. Nie ma tam ścieżki dla kart R9700.
- **MLC LLM jako silnik serwerowy**: kompilacja per model per urządzenie, wolne commity i brak GGUF to koszt, którego llama.cpp ci oszczędza.
- **Kwanty IQK z ik_llama.cpp**: pliki z kwantami IQ_K/KT ładują się tylko tam i blokują cię w forku (zob. [`04-LLAMA-CPP-I-RODZINA-GGML.md`](04-LLAMA-CPP-I-RODZINA-GGML.md)).

### 7.4 Lista "obserwuj, nie wdrażaj"

| Co obserwować | Czego szukać | Skąd to wiem |
|---|---|---|
| **KTransformers + ROCm** | Czy `kt-kernel` dostanie udokumentowane wsparcie ROCm/RDNA4 (opcja `KTRANSFORMERS_USE_ROCM` jest w CMake, ale bez wzmianki o gfx1201) i czy wejdzie do głównego SGLang z dokumentacją AMD. | `kt-kernel/CMakeLists.txt`, brak gfx1201 w dokumentach |
| **`--moe-cache-mib` w llama.cpp** | Pomiary na ROCm i opis, kiedy pomaga. Flaga jest świeża i domyślnie wyłączona. | `common/arg.cpp`, `src/llama-moe-cache.h` |
| **Cache ekspertów w ik_llama.cpp** | Czy zaimplementowany 2026-10-12 cache wyrówna się z mainline, czy fork się rozejdzie. | ik_llama.cpp, wpis `Implement moe cache #2644` |
| **ds4 na gfx1201** | Czy PR #558 (i dwa inne PR-y osób trzecich) wejdzie do main. To jedyne źródło danych z R9700 w tej grupie. | notatki o ds4 (PR #558) |
| **llama.cpp: `ggml-hexagon`, `ggml-openvino`, `ggml-webgpu`** | Jak szybko główny nurt pochłania nisze NPU i przeglądarki. | drzewo `0ce8cd1` |
| **mistral.rs: backend Vulkan lub ROCm** | Jeśli się pojawi, silnik z wbudowanym agentem i MCP staje się kandydatem. Dziś: brak. | grep po drzewie |
| **MLC LLM: tempo commitów** | Spadek z 72 do 26 commitów w 6 miesięcy. Dalszy spadek oznacza ryzyko porzucenia. | API GitHuba |
| **Qualcomm GenieX: wyjaśnienie relacji z Nexa AI** | Warunki przejścia i ewentualne warunki użytkowania/telemetria. | README; nie ustaliłem |

### 7.5 Jedno zdanie na koniec

Z tego rozdziału zabierz jedną konkretną lekcję: **rozmieszczenie ekspertów na poziomie pojedynczego eksperta i według rzeczywistej częstości użycia** jest tym, co odróżnia KT (i cache w ds4 oraz w nowym llama.cpp) od `-ot`. Jeśli kiedyś zabraknie ci VRAM, to w llama.cpp sprawdź najpierw `--n-cpu-moe`, potem `--moe-cache-mib`, a dopiero gdy zbudujesz osobną maszynę z serwerowym CPU i kartą NVIDIA, rozważ KT przez SGLang. Dalsze porównanie wszystkich silników i wybór: [`09-POROWNANIE-I-WYBOR.md`](09-POROWNANIE-I-WYBOR.md). O przyspieszaniu generowania na maszynie referencyjnej (dekodowanie spekulatywne, podział tensorowy): [`../przyspieszanie-generowania/README.md`](../przyspieszanie-generowania/README.md).

---

## Otwarte pytania

- KTransformers: nazwy konkurencyjnych baz w artykule SOSP (podejrzewam llama.cpp i Fiddler, niezweryfikowane); mechanizm "layerwise transport" przy prefillu nieprześledzony; finansowanie Approaching.AI nieznane (strona nieosiągalna).
- mistral.rs: stanowisko Erica Buehlera w Hugging Face nie zostało potwierdzone; kompletność odczytu kwantów IQ przez ścieżkę GGUF nie sprawdzona.
- MLC LLM: jakość i wydajność na konsumenckich kartach ROCm w moich źródłach nieudokumentowana; dokładny schemat wydań niejasny.
- Qualcomm GenieX: relacja z Nexa AI i warunki użytkowania.
- ik_llama.cpp: kodu serwera i schedulera nie czytałem (brak klonu); telemetrii nie sprawdzałem.
- llama.cpp `--moe-cache-mib`: stopień nakładania kopii z obliczeniami oraz zachowanie na gfx1201 nieustalone.
- ds4: zestawienie "kto liczy eksperty po doczytaniu" wnioskuję z opisu w dokumentacji, nie z lektury `ds4_ssd.c`.
