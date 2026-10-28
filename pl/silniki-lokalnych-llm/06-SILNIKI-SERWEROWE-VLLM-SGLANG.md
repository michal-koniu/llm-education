# 06 · Silniki serwerowe: vLLM, SGLang i spółka

**Po co ten rozdział.** Do tej pory siedziałeś w świecie jednego użytkownika i jednego strumienia tokenów: llama.cpp, llama-swap, jeden model na czterech kartach. Ten rozdział pokazuje drugi świat — silniki, które powstały po to, by **jedna maszyna obsłużyła setki równoległych zapytań** i zrobiła to możliwie tanio na token. Po lekturze będziesz umieć: wyjaśnić, dlaczego pamięć KV (*KV cache*) jest głównym problemem serwera i jak go rozwiązuje stronicowanie (*PagedAttention*); prześledzić drogę zapytania przez vLLM od serwera HTTP do jądra GPU; powiedzieć, czym różni się hashowany łańcuch bloków vLLM od drzewa radix w SGLang; ocenić, co z tego stosu da się uruchomić na czterech Radeonach R9700 rigu referencyjnego (gfx1201), a co nie; i zdecydować, kiedy w ogóle warto opuścić llama.cpp.

> ⚠️ **Niczego tu nie uruchamiałem ani nie mierzyłem.** Cały rozdział to desk research i czytanie kodu: vLLM w commicie `b7701fc` (2026-10-19), SGLang `aaa9388`, TensorRT-LLM `7695494`, plus API GitHuba i strony projektów. Stan na **19 października 2026**. Wszystko, co dotyczy działania na gfx1201, jest wnioskiem z kodu i dokumentacji, nie wynikiem testu. Liczby wydajności pochodzą od projektów i firm (oznaczone *dane projektu* / *dane firmy*) — nie są niezależne i nie wolno ich mieszać między różnymi sprzętami.

**Spis treści**

1. [Dlaczego silnik serwerowy to inna bestia niż desktopowy](#1-dlaczego-silnik-serwerowy-to-inna-bestia-niż-desktopowy)
2. [vLLM od środka](#2-vllm-od-środka)
3. [vLLM na R9700 (gfx1201)](#3-vllm-na-r9700-gfx1201)
4. [SGLang od środka](#4-sglang-od-środka)
5. [TensorRT-LLM, TGI (archiwum i lekcja), LMDeploy](#5-tensorrt-llm-tgi-archiwum-i-lekcja-lmdeploy)
6. [Warstwy klastrowe: Dynamo, llm-d, LMCache, FlashInfer, FlashAttention, Modular MAX](#6-warstwy-klastrowe-dynamo-llm-d-lmcache-flashinfer-flashattention-modular-max)
7. [Tabela porównawcza: vLLM, SGLang, TensorRT-LLM, llama.cpp](#7-tabela-porównawcza-vllm-sglang-tensorrt-llm-llamacpp)
8. [Co z tego dla konfiguracji referencyjnej](#8-co-z-tego-dla-konfiguracji-referencyjnej)

Konwencja tagów w tekście: bez znacznika = zweryfikowane w kodzie lub w źródle pierwotnym; *(dane projektu)* / *(dane firmy)* = własne twierdzenie; *(prasa)* / *(źródło zewnętrzne)* = relacja trzecia; *(niezweryfikowane)* i *(moje wyliczenie)* = wnioski. Jeśli chcesz zobaczyć, czym są warstwy stosu, wróć do [`01-MAPA-I-WARSTWY.md`](01-MAPA-I-WARSTWY.md); o tym, dlaczego dekodowanie jest ograniczone przepustowością pamięci, jest [`02-JAK-DZIALA-INFERENCJA.md`](02-JAK-DZIALA-INFERENCJA.md); llama.cpp opisuje [`04-LLAMA-CPP-I-RODZINA-GGML.md`](04-LLAMA-CPP-I-RODZINA-GGML.md).

---

## 1. Dlaczego silnik serwerowy to inna bestia niż desktopowy

### 1.1 Inny cel: agregat zamiast jednego strumienia

Silnik desktopowy (llama.cpp, Ollama, LM Studio) optymalizuje **czas do pierwszego tokenu** i **szybkość generowania (tok/s) jednego strumienia**, a do tego musi grzecznie dzielić maszynę z innymi programami. Silnik serwerowy optymalizuje coś innego: **łączną liczbę tokenów na sekundę przy zadanym limicie opóźnienia**, rozłożoną na dziesiątki lub setki jednoczesnych zapytań.

To nie jest różnica kosmetyczna. Zmienia ona, co jest wąskim gardłem, a więc i cały projekt programu.

Przypomnienie z rozdziału 02: dekodowanie jednego tokenu wymaga przeczytania z pamięci karty wszystkich aktywnych wag, a praca arytmetyczna na token jest mała, więc karta czeka na pamięć. **Jeśli jednak w jednym kroku obsłużysz 64 sekwencje naraz, te same wagi przeczytasz raz, a dostaniesz 64 tokeny.** Na przykładzie z artykułu o vLLM (model 13B, wagi 26 GB): przy batchu 1 jeden token „kosztuje” odczyt 26 GB, przy batchu 64 — 64 tokeny na ten sam odczyt (*moje wyliczenie*, pomijam odczyt KV i narzut). Stąd cała ekonomia serwera: **im więcej sekwencji wrzucisz do jednego kroku, tym tańszy token**. Przy batchu 1 nie ma czego amortyzować.

Ale żeby wrzucić dużo sekwencji do jednego kroku, każda z nich musi mieć w pamięci karty swój KV cache. I tu zaczyna się problem, który rozwiązuje stronicowanie.

### 1.2 Problem pamięci KV: arytmetyka z artykułu o PagedAttention

Źródło: Kwon i in., *Efficient Memory Management for Large Language Model Serving with PagedAttention*, arXiv 2309.06180, SOSP 2023 (Koblenz, 23–26 października 2023). Autorzy w kolejności: Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, Ion Stoica (UC Berkeley, Stanford, UC San Diego, niezależny badacz). Strony 1–2 i 8–9 PDF-a przeczytałem sam; liczby poniżej to liczby, które tam widziałem.

**Krok 1 — co zajmuje pamięć karty.** Rys. 1 artykułu: model 13B na A100 40 GB. Parametry zajmują 26 GB, czyli 65% pamięci (26/40 = 0,65). KV cache zajmuje **ponad 30%**, czyli ponad 12 GB. Reszta (aktywacje itp.) to mniej niż ~5% (*moje wyliczenie* z reszty do 100%).

**Krok 2 — ile to tokenów.** Tabela 1: dla OPT-13B na 1×A100-40GB pula KV mieściła **15,7 tys. tokenów**. Z 12 GB i 15,7 tys. tokenów wychodzi rząd wielkości **~0,8 MB KV na jeden token** (*moje wyliczenie*, z dwóch liczb artykułu; to rząd wielkości, nie dokładna wartość). Dla większych modeli w tabeli: OPT-66B na 4×A100 → 9,7 tys. tokenów; OPT-175B na 8×A100-80GB → 60,1 tys. tokenów.

**Krok 3 — ile z tej puli idzie na marne.** Rys. 2 artykułu mierzy, jaka część zarezerwowanej pamięci KV przechowuje *faktyczne stany tokenów*. W trzech wariantach systemu Orca użytych w artykule (Orca-Max, Orca-Pow2, Orca-Oracle) było to odpowiednio **20,4% / 26,8% / 38,2%**, w vLLM — **96,3%**. Zdanie z tekstu: „only 20.4% – 38.2% of the KV cache memory is used to store the actual token states in the existing systems”. „Prawie zerowe marnotrawstwo”, które projekt ma w opisie, to właśnie te 96,3%.

Przyłóżmy te odsetki do puli 15,7 tys. tokenów (*ilustracja, moje wyliczenie* — artykuł podaje średnie z eksperymentu, nie rozkład na tę konkretną pulę):

| System | Odsetek pamięci KV z realnymi tokenami | Realne tokeny z puli 15,7 tys. |
|---|---|---|
| Orca (najgorszy wariant) | 20,4% | ≈ 3,2 tys. |
| Orca (najlepszy wariant) | 38,2% | ≈ 6,0 tys. |
| vLLM | 96,3% | ≈ 15,1 tys. |

Stosunek 96,3/38,2 ≈ 2,5, a 96,3/20,4 ≈ 4,7. To zgadza się z rzędem wielkości nagłówkowego wyniku z abstraktu: „vLLM improves the throughput of popular LLMs by 2-4x with the same level of latency compared to the state-of-the-art systems, such as FasterTransformer and Orca”. Uwaga na cytowanie: **to 2–4× względem FasterTransformer i Orca, na setupach z 2023 roku (ślady ShareGPT/Alpaca)**. Nigdy nie cytuj tego jako „vLLM jest 4× szybszy od …” bez tego zastrzeżenia.

**Skąd bierze się marnotrawstwo — wyobraź to sobie tak.** Stary sposób to jak hotel, w którym każdy gość rezerwuje z góry cały ciągły rząd pokoi „na wypadek, gdyby został rok”, choć większość zostaje na dwie noce. Rząd stoi pusty i nikt inny go nie dostanie. Stronicowanie to hotel, w którym gość dostaje pokoje pojedynczo, **w dowolnych miejscach budynku**, a recepcja trzyma tabelkę „twój pokój nr 1 to fizyczny pokój 7, nr 2 to fizyczny 1”.

Teraz ściśle. Gdy silnik nie wie, ile tokenów wygeneruje zapytanie, a KV musi leżeć w jednym ciągłym kawałku, musi zarezerwować miejsce na najgorszy przypadek. Ilustracja z **hipotetycznymi liczbami** (nie z artykułu): jeśli rezerwujesz po 2048 tokenów na zapytanie, pula 15,7 tys. mieści ok. 7 równoległych zapytań (15 700 / 2048 ≈ 7,7), choćby wszystkie miały po 300 tokenów. Gdy pamięć przydzielasz w miarę potrzeby, to samo zapytanie zajmuje ~300 tokenów i w puli mieści się ich ok. 52 (15 700 / 300). **Siedem sekwencji w batchu kontra pięćdziesiąt** — a z punktu 1.1 wiesz, że wielkość batcha to bezpośrednio koszt tokenu.

**Mechanizm stronicowania** (artykuł §4, opis ogólny):

- KV cache dzieli się na **bloki stałego rozmiaru**.
- **Tablica bloków** (*block table*) mapuje bloki logiczne zapytania na bloki fizyczne w pamięci karty.
- Bloki fizyczne mogą leżeć w dowolnej kolejności; marnuje się co najwyżej kawałek **ostatniego** bloku każdej sekwencji.
- **Copy-on-write** pozwala dzielić bloki między sekwencjami (równoległe próbkowanie, *beam search*).
- Gdy bloków zabraknie, system **wywłaszcza** (*preemption*) — wypycha bloki na CPU albo odrzuca i liczy od nowa; kolejka FCFS; eksmisja „wszystko albo nic” na grupę sekwencji.

Ilustracja z blokiem **4-tokenowym** (rozmiar dobrany dla czytelności; domyślny rozmiar bloku na ROCm nie został ustalony — `block_size` jest `None`/zależny od platformy w `vllm/config/cache.py:74`):

```
Zapytanie A: 7 tokenów promptu            Pamięć fizyczna (bloki w dowolnej kolejności)
 blok logiczny 0: [t0 t1 t2 t3]  ──────►  blok fizyczny 7
 blok logiczny 1: [t4 t5 t6 __]  ──────►  blok fizyczny 1   (1 wolny slot = jedyne marnotrawstwo)
 (kolejny token trafi w wolne miejsce bloku 1; dopiero ósmy dostanie nowy blok)

Zapytanie B: 5 tokenów
 blok logiczny 0: [u0 u1 u2 u3]  ──────►  blok fizyczny 3
 blok logiczny 1: [u4 __ __ __]  ──────►  blok fizyczny 4
```

Ciekawostka skali: oryginalna implementacja z artykułu to „8.5K lines of Python and 2K lines of C++/CUDA code”. W dzisiejszym drzewie `vllm/` ma ok. 1,1 mln linii Pythona. O tym, skąd taki wzrost, za chwilę.

### 1.3 Reszta kompromisów — tabela

| Kwestia | Silnik desktopowy (llama.cpp) | Silnik serwerowy (vLLM, SGLang) |
|---|---|---|
| Cel | czas do pierwszego tokenu i tok/s jednego strumienia | łączna przepustowość przy limicie opóźnienia |
| KV cache | ciągły kawałek na slot; fragmentacja objawia się jako „slot za mały” | bloki + tablica bloków (vLLM), drzewo radix (SGLang) |
| Pamięć karty | współdzielona z innymi programami; możliwy swap modeli | **pre-alokacja**: vLLM bierze domyślnie `gpu_memory_utilization = 0.92` (`vllm/config/cache.py:102`) i z góry rozmiaruje pulę KV |
| Uruchomienie | bez kompilacji modelu (czasu nie mierzyłem) | kompilacja `torch.compile` + przechwycenie grafów — koszt startowy za stabilną szybkość |
| Procesor (CPU) | jeden wątek, nie ma co ukrywać | scheduler w Pythonie na ścieżce krytycznej → async scheduling, podział na procesy, front-end w Ruście |
| Kwantyzacje | zoo GGUF (k-quanty, i-quanty) | kilka formatów kalibrowanych pod konkretną kartę (AWQ/GPTQ, FP8, FP4, compressed-tensors) |
| Wiele kart | wtórne; tensor parallel *eksperymentalny* | pierwszorzędne; zakłada szybkie łącza |
| Telemetria | „jeden plik, działa offline” | metryki Prometheus/OTel, sondy zdrowia, raport użycia (włączony domyślnie w vLLM i TRT-LLM) |
| Utrzymanie | małe jądro, jeden format | 2-tygodniowe wydania, ~1,1 mln linii Pythona w vLLM, 286 plików modeli |

Parę wierszy z tej tabeli wymaga komentarza.

**Pre-alokacja kontra współdzielenie maszyny.** vLLM startuje, profiluje pamięć, rezerwuje ~92% każdej karty i dopiero z reszty tworzy pulę KV (`core.py::_initialize_kv_caches`). To słuszne, gdy maszyna istnieje po to, by serwować jeden model; to fatalne, gdy llama-swap ma ładować i zwalniać różne modele na tych samych kartach. vLLM ma endpointy `/sleep`, `/pause`, `/resume` (`EngineCore.sleep/wake_up`), które łagodzą problem, ale nie są pomyślane jako mechanizm częstej wymiany modeli.

**Grafy i kompilacja.** Za chwilę zobaczysz, że vLLM domyślnie przechwytuje grafy dla wielu rozmiarów batcha; dokumentacja sama mówi, że ten tryb jest „najbardziej wydajny, ale wymaga najwięcej pamięci i najdłużej się przechwytuje”. Dla jednego użytkownika narzut uruchamiania jąder jest drobnym składnikiem, a koszt startu i rezerwacji pamięci płacisz za każdym załadowaniem modelu (czas „dziesiątek sekund do minut” to *niezweryfikowane* — nie mierzyłem).

**Kwantyzacja jako koszt utrzymania.** Operator centrum danych kwantyzuje raz, z kalibracją, pod kartę, którą kupił. Użytkownik lokalny ściąga plik, który mu się mieści. Macierz „format × architektura GPU” to koszt utrzymania, którego serwery unikają, wspierając mniej formatów. Dlatego GGUF wyleciał z rdzenia vLLM (patrz §3).

**Co mówi o tym sam kod: jądra „na mały batch” na RDNA.** Nawet vLLM, silnik z założenia batchowy, ma w ścieżce RDNA dedykowane jądra „skinny GEMM” dla batcha ≤ 5 (`MAX_SKINNY_BATCH_SIZE = 5` w `rdna_hybrid_w4a16.py`; FP8 `wvSplitKQ` gdy `A.shape[0] <= 4`, `scaled_mm/rocm.py`), bo ogólny GEMM zestrojony pod duże batche marnuje się przy kilku wierszach. Lokalne runtime’y żyją w tym reżimie cały czas.

### 1.4 Kiedy stronicowanie pomaga mniej

*(Niezweryfikowane — rozumowanie, nie pomiar.)* Pojedynczy użytkownik z jedną–dwiema długimi rozmowami nie ma dużo fragmentacji do odzyskania. U niego liczy się to, **ile tokenów kontekstu zmieści się w VRAM po odjęciu wag**, i czy prefiks przetrwa między turami. Wyższe poziomy (reuse prefiksu: łańcuch bloków vLLM, drzewo radix SGLang) dają zysk w przypadku wspólnego system promptu wielu zapytań; w desktopie podobną rolę pełni utrzymywanie jednego slotu „ciepłym”.

---

## 2. vLLM od środka

**Jedna linia:** de facto standardowy otwartoźródłowy silnik serwerowy: scheduler w Pythonie/PyTorchu + stronicowany menedżer KV + jądra CUDA/ROCm/Triton za serwerem HTTP zgodnym z OpenAI (i Anthropic).

### 2.1 Tożsamość i skala

| | |
|---|---|
| Licencja | Apache-2.0 (API GitHuba, plik `LICENSE`) |
| Repozytorium | github.com/vllm-project/vllm; utworzone 2023-02-09; pierwsze wydanie v0.1.0 2023-06-20 |
| Aktualna wersja | **v0.32.0, 2026-10-18**; wydania co ok. 2 tygodnie (v0.29.0 09-09, v0.30.0 09-22, v0.31.0 10-05) |
| Gwiazdki / forki | 94 152 / 23 600 (API, 2026-10-19) |
| Języki (bajty) | Python 69,0 MB, Rust 5,2 MB, CUDA 3,2 MB, C++ 2,4 MB |
| Linie w migawce | `vllm/` Python 1 095 116; `csrc/` CUDA 76 562 + C++ 40 310 (plus ~46 tys. jąder CPU); `rust/` 145 149 linii Rusta |
| Pochodzenie | UC Berkeley, Sky Computing Lab (README); „v” miało pierwotnie oznaczać „virtual” — analogia do pamięci wirtualnej *(źródło zewnętrzne: Wikipedia)* |
| Dokumentacja | docs.vllm.ai; blog vllm.ai/blog |

Liczba współautorów z API (454) jest zaniżona, bo API ogranicza paginację; README mówi o ponad 2000 deweloperów *(dane projektu)*.

**Do kogo to jest.** Zespół platformowy z kartami centrum danych (albo ROCm Instinct, TPU, Gaudi…), który utrzymuje wspólny endpoint dla aplikacji, agentów i rolloutów RL. vLLM zakłada, że **maszyna jest jego**: rezerwuje pulę KV, kompiluje i przechwytuje grafy przy starcie, oczekuje checkpointów w formacie Hugging Face. Własne wartości projektu (`docs/governance/process.md`): wydajność, łatwość użycia, szerokie pokrycie, gotowość produkcyjna, rozszerzalność.

### 2.2 Model procesów (silnik V1) i droga zapytania

Źródło: `docs/design/arch_overview.md` (sekcja *V1 Process Architecture*) i kod w `vllm/v1/`.

```
                       HTTP / gRPC (klient: aplikacja, agent)
                                   │
        ┌──────────────────────────▼──────────────────────────┐
        │ Serwer API  (1 proces domyślnie; --api-server-count)  │
        │  vllm/entrypoints/openai/api_server.py                │
        │  tokenizacja, ładowanie multimodalne, SSE, detokenizacja│
        │  (async_llm.py, output_processor.py, detokenizer.py)  │
        └──────────────────────────┬──────────────────────────┘
                                   │  ZMQ + MessagePack
        ┌──────────────────────────▼──────────────────────────┐
        │ EngineCore  (1 proces na rangę DP; busy loop)         │
        │  vllm/v1/engine/core.py                               │
        │  ┌───────────────┐   ┌──────────────────────────────┐ │
        │  │  Scheduler    │◄─►│ KVCacheManager               │ │
        │  │ (v1/core/sched│   │  └─ BlockPool (bloki, hashe, │ │
        │  │  /scheduler.py)│  │     kolejka wolnych, LRU)     │ │
        │  └───────┬───────┘   └──────────────────────────────┘ │
        │          │ SchedulerOutput                            │
        │  ┌───────▼───────┐                                    │
        │  │ Executor      │  uniproc / multiproc / Ray         │
        │  └───────┬───────┘                                    │
        └──────────┼────────────────────────────────────────────┘
                   │  RPC do workerów
     ┌─────────────┼─────────────┬─────────────┬────────────┐
     ▼             ▼             ▼             ▼
 Worker GPU0   Worker GPU1   Worker GPU2   Worker GPU3     (po jednym na kartę:
 ┌─────────┐                                                 TP × PP na rangę DP)
 │ModelRunner│  stan trwały batcha, przygotowanie wejść,
 │ (V1/V2)  │  grafy CUDA/HIP, próbkowanie
 └────┬────┘
      ▼
 Backend uwagi (attention) + jądra: FlashAttention-fork / FlashInfer / Triton /
 rocm_attn / AITER … + csrc/ (Marlin, paged attention, MoE, skinny GEMM …)
```

Przykład z dokumentacji, który jest dokładnie kształtem maszyny referencyjnej: `vllm serve -tp=4` to **1 serwer API + 1 EngineCore + 4 workery GPU = 6 procesów** (plus proces koordynatora DP, jeśli DP > 1). Oddzielenie serwera API od rdzenia ma jeden cel: tokenizacja, detokenizacja i HTTP nie mogą konkurować o GIL z schedulerem (ogłoszenie V1). Płacisz za to IPC i większą liczbą procesów, pod które musisz mieć rdzenie CPU.

Pliki do zapamiętania: `vllm/v1/engine/core.py` (2806 linii: `EngineCore`, `EngineCoreProc`, `DPEngineCoreProc`), `core_client.py` (2162), `async_llm.py` (1445), `output_processor.py` (1047); wykonawcy w `vllm/v1/executor/` (`uniproc_executor.py`, `multiproc_executor.py` 1134 linii, `ray_executor_v2.py`).

**Jeden krok silnika** (`EngineCoreProc.run_busy_loop`, `core.py:1589`; `EngineCore.step()`, `core.py:640`):

```
while not shutdown:
    _process_input_queue()          # nowe zapytania z ZMQ
    step():
        scheduler.schedule()                      # kto dostaje ile tokenów w tym kroku
        model_executor.execute_model(..., non_block=True)   # GPU zaczyna forward pass
        (CPU liczy w tym czasie maskę gramatyki dla structured output)
        sample_tokens(grammar_output)             # próbkowanie
        scheduler.update_from_output(...)         # zapis wyników, zwolnienia, zakończenia
```

Wskazówka konstrukcyjna: maska gramatyki jest liczona na CPU **w trakcie** przebiegu w przód na GPU — standardowy trik, by ukryć koszt wymuszania gramatyki.

V1 ogłoszono 2025-01-27 (blog „vLLM V1 alpha”): jednolity scheduler, trwały batch, izolowana pętla EngineCore w osobnym procesie, prefix caching domyślnie włączony („<1% spadku przepustowości przy 0% trafień”), „do 1,7× większa przepustowość niż V0” *(dane projektu)*.

### 2.3 Scheduler: ciągłe batchowanie jako przydział budżetu tokenów

`vllm/v1/core/sched/scheduler.py` (3527 linii), plus `async_scheduler.py` i `request_queue.py` (kolejki FCFS i priorytetowa).

Najważniejsza rzecz w całym pliku to komentarz przy `scheduler.py:623–632`:

> „There's no 'decoding phase' nor 'prefill phase' in the scheduler. Each request just has the num_computed_tokens and num_tokens_with_spec … At each step, the scheduler tries to assign tokens to the requests so that each request's num_computed_tokens can catch up its num_tokens_with_spec. This is general enough to cover chunked prefills, prefix caching, speculative decoding, and the 'jump decoding' optimization.”

Po polsku: **scheduler nie zna faz „prefill” i „dekodowanie”**. Każde zapytanie ma licznik `num_computed_tokens` (ile tokenów ma już policzone) i cel `num_tokens_with_spec`. W każdym kroku scheduler rozdziela **budżet tokenów** `max_num_batched_tokens` tak, by liczniki „doganiały” cele, a potem wpuszcza zapytania oczekujące. Ten jeden mechanizm obejmuje:

- **ciągłe batchowanie** (*continuous batching*): zapytania wchodzą i wychodzą z batcha w każdym kroku, a nie czekają na koniec całej partii;
- **chunked prefill**: długi prompt jest cięty na kawałki i liczony w kilku krokach razem z dekodowaniem innych;
- **prefix caching**: tokeny trafione w cache są po prostu „już policzone” (`num_computed_tokens` startuje wyżej);
- **spekulatywne dekodowanie**: zapytanie ma więcej tokenów do sprawdzenia w jednym kroku.

Domyślne wartości w `vllm/config/scheduler.py`:

| Parametr | Domyślnie | Znaczenie |
|---|---|---|
| `max_num_batched_tokens` | 2048 (256 dla batched-DP) | budżet tokenów na krok |
| `max_num_seqs` | 128 (`DEFAULT_MAX_NUM_SEQS=128`, linia 43) | maks. zapytań w locie |
| `enable_chunked_prefill` | `True` | cięcie długich promptów |
| `long_prefill_token_threshold` | konfigurowalne (jest wariant adaptacyjny) | nie pozwala długiemu promptowi zagłodzić innych |
| „prefill cadence” | konfigurowalne | odkłada prefill, by dekodowanie miało dłuższe nieprzerwane serie |
| `stream_interval` | konfigurowalne | ile tokenów buforować przed wysłaniem SSE |

⚠️ **Rozbieżność w źródłach:** dokument projektowy Model Runner V2 mówi o „`max_num_reqs` (1024 by default on most platforms)”, a klasa konfiguracji ma 128. Zweryfikowałem obie wartości w plikach; nie ustaliłem, która wygrywa na danej platformie (są nadpisania zależne od kontekstu użycia).

**Przykład chunked prefill z budżetem 2048** (*ilustracja, moje wyliczenie*): w locie jest 10 sekwencji dekodujących, nadchodzi prompt 6000 tokenów. Krok 1: 10 tokenów dekodowania + 2038 tokenów promptu (2048 − 10). Krok 2: znów 10 + 2038. Krok 3: 10 + 1924 (reszta). Przez te 3 kroki dziesięć sekwencji **nie przestało generować** — gdyby prompt poszedł jednym kawałkiem, każdy z nich czekałby na cały prefill. Ceną jest dłuższy czas do pierwszego tokenu dla samego długiego promptu.

**Wywłaszczanie.** Gdy bloków KV zabraknie, scheduler wywłaszcza zapytania z biegu i liczy je później od nowa. V1 wybrał **przeliczenie zamiast swapu** (artykuł z 2023 miał oba warianty; w `schedule()` jest `preempted_reqs`, a dokument MRV2 mówi „Treat preemption as completion. On resume, re-add request data as fresh state”).

**Async scheduling** (`AsyncScheduler`, `async_scheduler.py:14–80`): scheduler planuje krok N+1, gdy GPU wykonuje krok N. Ponieważ wylosowane tokeny kroku N nie są jeszcze znane, scheduler zapisuje `num_output_placeholders` i tokeny-zastępniki `-1`, a poprawia je, gdy wynik nadejdzie. Zapytania ze structured output są oznaczane `pending_structured_output_tokens`, bo gramatyka potrzebuje prawdziwego tokenu. `SchedulerConfig.async_scheduling` domyślnie `None` (tryb automatyczny). To odpowiednik „scheduler zero-overhead” w SGLang (§4).

### 2.4 Menedżer KV i prefix caching

Pliki w `vllm/v1/core/`: `kv_cache_manager.py` (922), `block_pool.py` (905), `kv_cache_utils.py` (1217), `kv_cache_coordinator.py` (1038), `single_type_kv_cache_manager.py` (2719), `kv_cache_planning.py` (1704).

**`BlockPool`** jest właścicielem wszystkich bloków GPU jako obiektów `KVCacheBlock` (licznik referencji, opcjonalny hash). Wolne bloki leżą w `FreeKVCacheBlockQueue` — **intruzyjnej liście dwukierunkowej**, napisanej tak, by usunięcie elementu ze środka było O(1) (dotknięcie bloku z cache zdejmuje go z listy wolnych) bez alokowania obiektów Pythona. Kolejność eksmisji to LRU, z remisami rozstrzyganymi tak, że **ogon łańcucha bloków wylatuje pierwszy** (`kv_cache_utils.py:258–285`).

`BlockPool.free_blocks` (`block_pool.py:776`): bloki z `ref_cnt==0` **bez hasha** trafiają na **początek** kolejki (ponowne użycie LIFO „dla lepszej lokalności GPU”); bloki z hashem (nadające się do prefix cache) — na **koniec** (FIFO = eksmisja LRU).

**Jak działa hashowanie prefiksu.** Cache to tablica haszująca `BlockHashToBlockMap`: `{(block_hash, group_id) → blok}`. Zasady:

1. Cache’owane są **tylko pełne bloki**.
2. Hash bloku zależy od hasha **poprzedniego** bloku (łańcuch): `hash_block_tokens(hash_fn, parent_block_hash, curr_block_token_ids, extra_keys)` = `hash((parent_hash, tuple(token_ids), extra_keys))`; pierwszy blok dostaje początkową wartość `NONE_HASH` (`kv_cache_utils.py:707–737`).
3. `extra_keys` niosą identyfikator LoRA, hashe wejść multimodalnych, hash osadzeń promptu i — ważne w wielodzierżawczości — **`cache_salt`** per zapytanie.

```
tokeny:  [ A A A A | B B B B | C C C C | D D ]      (blok = 4 tokeny, ilustracja)
          └─blok 0─┘ └─blok 1─┘ └─blok 2─┘ └ niepełny: nie jest w cache
h0 = H( NONE_HASH, (A A A A), extra )
h1 = H( h0,        (B B B B), extra )
h2 = H( h1,        (C C C C), extra )
```

**Dlaczego łańcuch, a nie sam hash tokenów bloku?** Bo stan KV tokenu zależy od *wszystkich* tokenów przed nim. Taki sam blok `(B B B B)` po innym prefiksie to inne KV, więc musi mieć inny hash. Łańcuch zapewnia to za darmo: nowe zapytanie liczy hashe blok po bloku od początku i szuka każdego w tablicy; pierwsze nietrafienie kończy dopasowanie.

Funkcja haszująca: od v0.11 domyślnie **sha256** (przez pickle; wynik może różnić się między wersjami Pythona/vLLM), `sha256_cbor` dla powtarzalnych hashy między procesami i językami, `xxhash`/`xxhash_cbor` szybsze, ale niekryptograficzne, z udokumentowanym zastrzeżeniem o kolizjach i prywatności w środowiskach wielodzierżawczych (opcja `--prefix-caching-hash-algo`; `docs/design/prefix_caching.md`).

Uwaga projektowa z kodu (`block_pool.py:44–49`): „we don't de-duplicate the blocks in the cache … block tables are append-only”.

Konsekwencje: wyszukiwanie O(1), trywialna dystrybucja (zdarzenia KV, offload, P2P), ale dopasowanie **tylko co cały blok**. Krótkich wspólnych prefiksów (mniej niż blok) nie współdzielisz. Porównaj z drzewem SGLang w §4.

**Modele hybrydowe.** `kv_cache_coordinator.py` i `single_type_kv_cache_manager.py` zarządzają kilkoma „grupami KV” o różnych typach warstw (pełna uwaga, okno przesuwne, stan Mamba/liniowej uwagi) — `docs/design/hybrid_kv_cache_manager.md`. Przejrzałem nazwy plików, nie wnętrze.

**Zdarzenia KV** (`vllm/distributed/kv_events.py`: `BlockStored`/`BlockRemoved`/`AllBlocksCleared`) są publikowane, by zewnętrzne routery (llm-d, Dynamo) widziały zawartość cache. **Offload KV** — `vllm/v1/kv_offload/` (15 195 linii; CPU/warstwy/plik), `vllm/v1/simple_kv_offload/` (2940) i offload przez konektory.

### 2.5 Worker i Model Runner: V1 i V2

Katalog `vllm/v1/worker/` ma 45 135 linii.

**Model Runner V1:** `gpu_model_runner.py` — 7221 linii, największy plik w `v1`. Trwały batch: stan zapytań trzymany w trwałych tensorach (`gpu_input_batch.py`) i aktualizowany różnicowo w każdym kroku, żeby nie przebudowywać tablic bloków w Pythonie.

**Model Runner V2 (MRV2):** `vllm/v1/worker/gpu/` (`model_runner.py` 2473 linii, `input_batch.py`, `cudagraph_utils.py` 1098, `spec_decode/`, `sample/`, `pcp_manager.py`). Dokument projektowy (`docs/design/model_runner_v2.md`) mówi słowami autorów, że w V1 „we discovered several fundamental design mistakes and accumulated significant technical debt”, więc runner napisano od nowa: stan trwały oddzielony od tensorów wejściowych per krok (składanych na GPU przez Triton/UVA), podejście „async-first” — „the core model execution loop is a CUDA stream with no CPU synchronization points”, próbkowanie Gumbel-max po stronie GPU.

Status w tej migawce: `VllmConfig.use_v2_model_runner` (`vllm/config/vllm.py:707–740`) zwraca **`True` domyślnie**, chyba że ustawisz `VLLM_USE_V2_MODEL_RUNNER=0`, brakuje Tritona albo zażądasz nieobsługiwanej funkcji (wtedy ostrzeżenie i powrót do V1). ⚠️ Dokumentacja jest w tyle za kodem: `worker/gpu/README.md` nadal pisze „[Experimental]”, a dokument projektowy „not yet feature-complete”. Czy ten sam domyślny wybór obowiązuje na ROCm — **nie sprawdziłem**.

`gpu_worker.py` (1708 linii): profiluje pamięć, rozmiaruje pulę KV, ładuje wagi, przechwytuje grafy. Planowanie KV: `core.py::_initialize_kv_caches` (`core.py:244`) i `kv_cache_planning.py`.

### 2.6 `torch.compile` i grafy CUDA/HIP

`vllm/compilation/` (15 974 linii), `docs/design/torch_compile.md`, `cuda_graphs.md`, `vllm/v1/cudagraph_dispatcher.py`.

- vLLM kompiluje model `torch.compile` **kawałkami** (*piecewise*): graf jest cięty na uwadze (która nie we wszystkich backendach da się przechwycić do grafu CUDA), kawałki kompiluje Inductor, a grafy są przechwytywane dla zaokrąglonych rozmiarów batcha.
- Warstwa operacji własnych (`docs/design/custom_op.md`) pozwala podmieniać jądra (RMSNorm, operacje fuzowane, kwantyzacja) i przepuszczać przejścia fuzji (`vllm/compilation/passes/fusion/`, w tym `rocm_aiter_fusion.py`).
- Tryby `CUDAGraphMode`: `NONE`, `PIECEWISE`, `FULL`, `FULL_DECODE_ONLY`, **`FULL_AND_PIECEWISE` (domyślny)** — pełny graf dla jednolitych batchy dekodowania, kawałkowy dla prefillu i batchy mieszanych. Dokumentacja: „generally the most performant … but also requires the most memory and takes the longest to capture”. `CudagraphDispatcher` wybiera graf z `BatchDescriptor`.
- Na ROCm to samo robią grafy HIP przez ten sam kod; „CUDA graphs” to nazwa API (`cuda_alike`).

Skutek dla pojedynczej maszyny: start to kompilacja i przechwytywanie, a grafy rezerwują pamięć. Zysk: mniejszy narzut CPU na krok przy średnich i dużych batchach.

### 2.7 Backendy uwagi i jądra

`vllm/v1/attention/` (68 079 linii wraz z operacjami). W `backends/`: `flash_attn.py` (własny fork FlashAttention `vllm_flash_attn` dla CUDA), `flashinfer.py`, `triton_attn.py`, `flex_attention.py`, MLA (`mla/`), warianty Mamba/GDN/liniowe, `cpu_attn.py`; dla ROCm: `rocm_attn.py`, `rocm_aiter_fa.py`, `rocm_aiter_unified_attn.py`, `rocm_segmented_attn.py`, `triton_flash_attn.py`; dalej `hpc_attn.py`, `turboquant_attn.py`, `ultraquant_attn.py`. Wybór według listy priorytetów dla platformy (`vllm/v1/attention/selector.py`, `platforms/*.py::_get_backend_priorities`). FlashInfer to przypięta zależność (`requirements/cuda.txt: flashinfer-python==0.7.2`).

Jądra (`csrc/`, ~118 tys. linii bez CPU): `attention/` (4315: paged attention v1/v2, MLA), `quantization/` (27 232: Marlin, AWQ, GPTQ/Exllama, CUTLASS scaled-mm, FP8/FP4, machete), `moe/` (9704), `rocm/` (13 701), `mamba/`, `kimi_k3/`, własny all-reduce (`custom_all_reduce.cu*`), jądra cache (`cache_kernels.cu`), jądra próbkowania. Powtarzające się jądra „fused_*_qknorm_rope_kv_insert” per rodzina modeli pokazują, ile pracy per model projekt na siebie bierze — to wyjaśnia, dlaczego z 2K linii C++/CUDA zrobiło się ~118 tys.

### 2.8 Funkcje: spekulatywne dekodowanie, structured output, narzędzia, LoRA, multimodal

- **Spekulatywne dekodowanie** (`vllm/v1/spec_decode/`, 6373 linii): n-gram (CPU i GPU), EAGLE, model szkicujący (*draft*), MTP, dekodowanie sufiksowe, „dflash”, „fly”, wyciąganie stanów ukrytych, głowice specyficzne dla modeli; sampler odrzucający `vllm/v1/sample/rejection_sampler.py` (1197 linii). Ogólna zasada „sprawdź kilka tokenów naraz za cenę jednego” jest opisana w katalogu o przyspieszaniu: [`../przyspieszanie-generowania/README.md`](../przyspieszanie-generowania/README.md).
- **Structured output** (`vllm/v1/structured_output/`): backendy xgrammar, guidance, outlines, lm-format-enforcer; domyślnie `backend="auto"` wybiera według treści zapytania (`vllm/config/structured_outputs.py:20`).
- **Wywoływanie narzędzi:** `vllm/tool_parsers/` ma ok. 60 plików (≈55 parserów: hermes, llama, mistral, pythonic, qwen3, deepseek v3/v3.1/v3.2/v4, kimi k2/k3, glm, gpt-oss/harmony, granite, …). **Parsery rozumowania:** `vllm/reasoning/` ~42 pliki (deepseek r1/v3, qwen3, gpt-oss, kimi, glm, …). To liczby plików, nie parserów. Sens: każda nowa rodzina otwartych modeli wymaga własnego parsera i vLLM dostarcza je szybko („Day-0” to *niezweryfikowane* w sensie „w ciągu dni”).
- **LoRA:** wiele adapterów naraz (`vllm/lora/`, 14 653 linii; `/v1/load_lora_adapter`). **Multimodal:** `vllm/multimodal/` (13 441 linii; obrazy/wideo/audio; cache enkodera `v1/core/encoder_cache_manager.py`). **Embeddingi/rerank/pooling.** **Tryb uśpienia** (`EngineCore.sleep/wake_up`).
- **Dezagregacja prefill/decode** — „eksperymentalna”: konektory NixlConnector, MooncakeConnector, MoRIIOConnector (tylko ROCm), LMCacheConnectorV1/LMCacheMPConnector, OffloadingConnector (offload KV do CPU), MultiConnector, ExampleConnector (`docs/features/disagg_prefill.md`). Dokument jest szczery: „Disaggregated prefill DOES NOT improve throughput” — służy do osobnego strojenia TTFT i opóźnienia międzytokenowego i do kontroli ogona ITL.

### 2.9 Równoległość

Tensor parallel, pipeline parallel, data parallel, expert parallel, context parallel (DCP/PCP), elastyczny EP, „dual-batch overlap” (`design/dbo.md`); `vllm/distributed` ma 85 642 linii. W słowniku kursu: *podział tensorowy (tensor parallel)* tnie każdą warstwę między karty (karty muszą często wymieniać wyniki — stąd znaczenie łącza), a *rurociąg (pipeline)* przydziela kartom kolejne grupy warstw. Gdzie to boli na sprzęcie referencyjnym, zobaczysz w §3.

### 2.10 Projekt „platform” i wtyczki sprzętowe

vLLM nie jest jedynie „silnikiem CUDA”. W `vllm/platforms/` leżą platformy w drzewie: `cuda.py`, `rocm.py` (1408 linii), `xpu.py`, `cpu.py`, `zen_cpu.py`, `tpu.py`. Inny sprzęt dołącza **spoza drzewa** przez punkty wejścia Pythona (`vllm.platform_plugins`, `docs/design/plugin_system.md`):

| Wtyczka | Sprzęt | Gwiazdki (API) |
|---|---|---|
| vllm-ascend | Huawei Ascend | 3000 |
| vllm-gaudi | Intel Gaudi | 63 |
| tpu-inference | Google TPU (JAX + PyTorch) | 464 |
| vllm-metal | Apple Silicon (link w dokumentacji instalacji) | — |

Wpis w blogu PyTorch Foundation (2025-05-06) wymienia też AWS Neuron i IBM Spyre jako cele wtyczkowe lub oficjalne. Idea projektowa: **PyTorch + operacje własne jako warstwa przenośności** — producent sprzętu dostarcza wtyczkę i implementacje operacji, a rdzeń (scheduler, KV) zostaje wspólny. Cena: narzut Pythona, łagodzony kompilacją i grafami.

Sam front-end też się zmienia: **Rust front-end** (`rust/`, „vllm-frontend-rs”, serwer HTTP+gRPC na axum, rozmawia z rdzeniem Pythona przez ZMQ+MessagePack; włączany `VLLM_USE_RUST_FRONTEND=1`; README: „experimental, not feature-complete”). Powstał najpierw w `github.com/Inferact/vllm-frontend-rs` (zarchiwizowane), potem został przeniesiony do głównego repo.

### 2.11 API i modele

Serwer (`vllm/entrypoints/openai/api_server.py`, komenda `vllm serve`) wystawia m.in. `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/responses`, `/v1/audio/transcriptions`, `/v1/realtime`, `/v1/score`, `/v1/rerank`, `/tokenize`, `/detokenize`, `/v1/load_lora_adapter`, `/sleep`, `/pause`, `/resume`, `/metrics`, `/health`, `/v1/models`. **API zgodne z Anthropic**: `/v1/messages` i `/v1/messages/count_tokens` (`vllm/entrypoints/anthropic/`). Jest też router `cohere`, serwer gRPC (`grpc_server.py`), klasa `LLM` do pracy offline i `vllm bench`. **Nie ma API zgodnego z Ollamą** (SGLang je ma).

Modele: README podaje 200+ architektur *(dane projektu)*; w drzewie `vllm/model_executor/models/` jest 286 plików, a sam rejestr ma 1607 linii.

### 2.12 Mocne i słabe strony, offline, kto za tym stoi

**Mocne strony:** najszersze pokrycie modeli i największy ekosystem (llm-compressor, production-stack, aibrix, semantic-router, guidellm, vllm-omni — wszystko `vllm-project/*`, Apache-2.0); realna szerokość sprzętowa przez wtyczki; API OpenAI + Anthropic + gRPC; dobry tensor parallel na jednakowych kartach. „Najszybsze wsparcie dnia zerowego” — *niezweryfikowane*.

**Słabe strony dla ciebie:** (a) brak GGUF w rdzeniu (§3); (b) ROCm pierwszej klasy dotyczy Instinct (MI300/MI350), RDNA4 jest celem drugorzędnym; (c) 0,92 pamięci karty — nie współistnieje z procesami llama.cpp zarządzanymi przez llama-swap na tych samych kartach; (d) jeden model na proces serwera, brak wbudowanej wymiany modeli (nie znalazłem w drzewie; tryb uśpienia pomaga częściowo — *niezweryfikowane*).

**Offline.** Działa offline po lokalnym załadowaniu wag (wskaż lokalną ścieżkę; `HF_HUB_OFFLINE=1` to standardowe zachowanie Hugging Face — *niezweryfikowane* tu). **Telemetria jest domyślnie włączona**: reporter statystyk użycia wysyła na `https://stats.vllm.ai`; docstring `is_usage_stats_enabled()`: „By default, it should be enabled”. Wyłączasz zmienną `VLLM_DO_NOT_TRACK=1`, `DO_NOT_TRACK=1`, `VLLM_NO_USAGE_STATS=1` albo plikiem `$HOME/.config/vllm/do_not_track` (`vllm/usage/usage_lib.py:50–68`, `vllm/envs.py:36–38, 828–835`). Kolektor zagląda też do plików dostawców chmury w `/sys/class/dmi` (`_detect_cloud_provider`). Co dokładnie jest wysyłane — nie przeczytałem całości.

**Kto za tym stoi.** Projekt wyszedł z UC Berkeley (Sky Computing Lab); od 2025-05-06 jest hostowany przez PyTorch Foundation, a wcześniej (lipiec 2024) wszedł pod parasol Linux Foundation *(źródło zewnętrzne)*. Licencja Apache-2.0; dokument zarządzania mówi wprost: „No one buys their way into governance. Committer status belongs to individuals, not companies.” Rdzeń „Project Leads” (odpowiednik Technical Steering Committee) to m.in. Woosuk Kwon, Zhuohan Li, Simon Mo, Kaichao You, Robert Shaw, Tyler Michael Smith, Michael Goin, Nick Hill; lead maintainerami są Woosuk Kwon i Zhuohan Li. Wielu z nich pracuje dziś w startupie **Inferact** (utworzona 2025-10-20 organizacja GitHub; w styczniu 2026 firma ogłosiła zebranie 150 mln USD — *dane firmy*, powtórzone przez Wikipedię za TechCrunch *(prasa)*; inwestorów i wyceny nie ustaliłem) lub w Red Hat. Pełne pieniądze i ludzie: [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

> **Sprawdź sam (1) — scheduler bez faz i łańcuch hashy prefiksu.** W klonie vLLM (commit `b7701fc`):
> ```bash
> sed -n '620,635p' vllm/v1/core/sched/scheduler.py
> grep -n "max_num_batched_tokens\|DEFAULT_MAX_NUM_SEQS" vllm/config/scheduler.py | head
> sed -n '700,740p' vllm/v1/core/kv_cache_utils.py     # hash_block_tokens, NONE_HASH
> sed -n '770,800p' vllm/v1/core/block_pool.py          # free_blocks: bloki bez hasha na początek, z hashem na koniec
> ```
> Powinieneś zobaczyć zdanie „There's no 'decoding phase' nor 'prefill phase' in the scheduler”, domyślne 2048 / 128 oraz wzór `hash((parent_hash, tuple(token_ids), extra_keys))`. *(Nie uruchamiałem tych poleceń; ścieżki i zakresy linii pochodzą z notatek.)*

---

## 3. vLLM na R9700 (gfx1201)

Wszystko poniżej pochodzi z kodu i dokumentacji migawki `b7701fc`. **Niczego nie uruchomiłem na tej maszynie** — karty są w produkcji.

### 3.1 Co zweryfikowałem w kodzie i dokumentach

1. **Oficjalna deklaracja.** `docs/getting_started/installation/gpu.rocm.inc.md` wymienia: MI200 (gfx90a), MI300 (gfx942), MI350 (gfx950), Radeon RX 7900 (gfx1100/1101), **Radeon RX 9000 (gfx1200/1201)**, Ryzen AI MAX / AI 300 (gfx1151/1150); ROCm 6.3 lub nowszy. Nazwa „R9700” w dokumentacji nie pada.
2. **Karta jest rozpoznawana po nazwie.** `vllm/platforms/rocm.py:92` mapuje identyfikator PCI **`0x7551` na `"AMD_Radeon_R9700"  # gfx1201`**, a `0x7550` na RX 9070 XT (gfx1201).
3. **Domyślna lista architektur.** `CMakeLists.txt:52` — `HIP_SUPPORTED_ARCHS` zawiera `gfx1200;gfx1201`; bazowy obraz Dockera dla ROCm buduje `gfx90a;gfx942;gfx950;gfx1100;gfx1101;gfx1200;gfx1201;gfx1150;gfx1151` (komentarz: „gfx1200 (9070XT), gfx1201 (9070)”).
4. **Predykaty architektury.** `rocm.py` definiuje `_ON_RDNA4 = gfx1200 or gfx1201`, `_ON_GFX12X`, `_ON_GFX1X` (cała RDNA3/4).
5. **Instalacja.** Gotowe koła wymagają **Pythona 3.12**; na innych wersjach pip „will silently fall back to the CUDA wheel from PyPI, which will fail” (ostrzeżenie z dokumentacji). Warianty: `rocm100` (ROCm 10.0 z pip przez TheRock, „includes the GPU kernels for every supported architecture”; domyślny nightly), `rocm721`, `rocm72`, `rocm700` (0.14.0–0.18.0). Polecenie: `uv pip install vllm --extra-index-url https://wheels.vllm.ai/rocm/ --upgrade` *(nie uruchamiałem)*.

⚠️ **gfx1250 to nie RDNA4.** Zarówno vLLM, jak i SGLang mają w listach budowania `gfx1250`; kod vLLM traktuje go jako klasę CDNA (typ MI4xx), a komentarz w Dockerfile SGLang nazywa go „mi45x”. Docstring pomocnika w SGLang, który nazywa gfx1250 „RDNA4”, jest błędny lub nieprecyzyjny. R9700 to **gfx1201**.

### 3.2 Backendy uwagi, które zadziałają

Lista priorytetów dla modeli bez MLA (`_get_backend_priorities`, `rocm.py` ok. 505–530): `ROCM_ATTN` (o ile nie ma konektora KV), `ROCM_AITER_FA` (jeśli włączone AITER MHA), `ROCM_AITER_UNIFIED_ATTN` (jeśli znaleziono AITER; wstawiany **na początek**, gdy `is_rdna_aiter_enabled()` = RDNA4 + zainstalowany `aiter` + włączone przez użytkownika), potem `TRITON_ATTN`, `TURBOQUANT`, `ULTRAQUANT`. `VLLM_ROCM_USE_AITER` ma domyślnie **False** (`envs.py:136, 1250`).

Własne jądro HIP paged attention (`csrc/rocm/attention.cu`) jest na gfx1x dopuszczone tylko dla: fp16/bf16 q, **head_size == 128, block_size == 16, stosunek GQA 3..16, max_seq_len ≤ 128K, bez okna przesuwnego, bez ALiBi, bez „sinks”, `kv_cache_dtype` „auto”** (`rocm.py` ok. 896–908). Wszystko inne trafia do Tritona. Na R9700 spodziewaj się więc `ROCM_ATTN` (dla „zwykłych” kształtów) albo `TRITON_ATTN`.

AITER na gfx12 udostępnia **wyłącznie jądra Triton**: „Only aiter's Triton kernels exist on gfx12 (no CK build)” (`_aiter_ops.py:2276–2290`). Dla enkoderów wizyjnych platforma woli „Flash Attention (Triton backend)” tylko przy `FLASH_ATTENTION_TRITON_AMD_ENABLE=TRUE` i obecnym module; w przeciwnym razie Torch SDPA.

### 3.3 Kwantyzacja na RDNA4: kod kontra dokumentacja

**Kod.** `ROCmPlatform.supported_quantization` (`rocm.py:625–649`) zawiera: awq, auto_awq, awq_marlin (→awq), gptq, auto_gptq, fp8, compressed-tensors, fbgemm_fp8, inc, quark, mxfp4, mxfp8, torchao, modelopt*, warianty fp8 per-tensor/block/channel, online, gpt_oss_mxfp4, deepseek_v4_fp8. **Brak `gguf`, brak `bitsandbytes`, brak `gptq_marlin`.**

**Jądra INT4 (W4A16).** Kolejność priorytetów w `vllm/model_executor/kernels/linear/__init__.py:541–547`:

1. `RDNA3W4A16LinearKernel` — wymaga **tylko gfx1100**;
2. **`RDNAHybridW4A16LinearKernel`** — dowolne gfx11/gfx12: fuzowany GEMM z dekwantyzacją w Triton dla prefillu + „skinny” GEMM w HIP `wvSplitK_int4_g` dla dekodowania (wiersze M ≤ 5); grupy 32/64/128; aktywacje fp16/bf16; K%16==0; wagi przechowywane raz jako int8 w układzie ExLlama (`mixed_precision/rdna_hybrid_w4a16.py`, 651 linii);
3. `TritonW4A16LinearKernel`, 4. `ConchLinearKernel`, 5. `ExllamaLinearKernel`.

Wniosek z kodu: **INT4 GPTQ/AWQ jest na gfx1201 obsługiwane przez jądro hybrydowe**.

**FP8.** `supports_fp8()` to `on_cdna() or on_rdna()`; `ROCmFP8ScaledMMLinearKernel` ma komentarz „Restore RDNA4 (gfx12x) dropped by the get_cdna_version()>2 refactor” i raportuje „requires CDNA3+ (gfx942/gfx950) or RDNA4 (gfx12x)” (`scaled_mm/rocm.py:88–90`); ścieżka małego batcha używa `wvSplitKQ`, inaczej `torch._scaled_mm`. Typ fp8 poza gfx94 to `float8_e4m3fn`. Czy wydajność FP8 na gfx1201 jest dobra — **nie mierzono**.

⚠️ **Rozbieżność dokumentacja–kod (AWQ/GPTQ).** Tabela w `docs/features/quantization/README.md` pokazuje dla „AMD GPU”: AWQ: nie, GPTQ: nie, FP8 (llm-compressor W8A8): tak, GGUF: tak. To przeczy kodowi opisanemu wyżej (jądra RDNA, awq/gptq na liście dopuszczonych). Podejrzewam, że tabela jest zgrubna i nieaktualna, ale **nie umiem tego udowodnić**. Reguła praktyczna: *dokumentacja mówi „nie”, kod ma jądra dla RDNA — przetestuj, zanim na tym oprzesz plan.* Co ciekawe, ta sama tabela uznaje GGUF za obsługiwany dla AMD, a drugi dokument (poniżej) mówi, że GGUF jest poza rdzeniem — czyli tabela jest wewnętrznie niespójna z resztą dokumentacji.

### 3.4 GGUF w vLLM

Z `docs/features/quantization/gguf.md`:

- obsługa „has migrated to OOT vllm-gguf-plugin” (repo `vllm-project/vllm-gguf-plugin`, 54 gwiazdki, ostatni push 2026-09-24) — trzeba `pip install vllm-gguf-plugin`;
- baner: „GGUF support in vLLM is highly experimental and under-optimized … might be incompatible with other features. Currently, you can use GGUF as a way to reduce memory footprint”;
- składnia: `vllm serve unsloth/Qwen3-0.6B-GGUF:Q4_K_M --tokenizer Qwen/Qwen3-0.6B`; tokenizer ma pochodzić z modelu bazowego („conversion from GGUF is time-consuming and unstable”); konfiguracja musi być konwertowalna przez HF (`--hf-config-path`); TP działa (przykład `--tensor-parallel-size 2`);
- plików `gguf.py`/`gguf_loader.py` w rdzeniu migawki już nie ma.

Czego **nie** wiem: jakie typy kwantów obsługuje wtyczka i czy jakiekolwiek jądra ROCm je uruchamiają. Traktuj to jako „wczytaj wagi, żeby zaoszczędzić VRAM, nie oczekuj prędkości klasy llama.cpp”. Dla ciebie to kluczowe: twoja kolekcja kwantów (UD-IQ3_XXS itd.) nie jest paliwem dla vLLM.

### 3.5 Wiele kart

Własny all-reduce jest włączony tylko na `gfx94`/`gfx95` (`rocm.py:1216–1218`). Na czterech R9700 przez PCIe all-reduce w tensor parallel idzie więc przez **RCCL** (`CudaCommunicator`). Te karty nie mają łącza klasy NVLink, więc skalowanie TP będzie ograniczone przepustowością *(niezweryfikowane — wniosek ze sprzętu, nie pomiar)*. To pokrywa się z tym, co o `-sm tensor` w llama.cpp mówi rozdział 04.

### 3.6 Uczciwe podsumowanie dla gfx1201

**Na papierze obsługiwane** (w dokumentacji, w domyślnych architekturach, rozpoznawane po nazwie, dedykowane jądra RDNA istnieją). W praktyce RDNA4 to **konsumencki ogon stosu projektowanego pod MI300/MI350**: szybkie ścieżki AITER oparte o CK nie istnieją na gfx12 (tylko Triton), własny all-reduce jest tylko dla MI300, a tabela kwantyzacji jest zorientowana na Instinct. Nie znalazłem nazw zadań CI dla gfx1201 poza konfiguracją Buildkite dla ROCm (nie sprawdzałem jej wnętrza). Oczekuj, że zadziała dla modeli BF16/FP16 oraz FP8 i INT4-GPTQ w wagach w formacie HF — **i że będziesz musiał stroić i debugować**. Nie znalazłem żadnego niezależnego benchmarku na RDNA4.

### 3.7 Nieprzetestowane — co spróbowałbym najpierw

⚠️ **Poniższa lista jest czystą hipotezą. Nic z tego nie zostało uruchomione.** Zakładam, że karty na czas testu zwolniłeś z llama-swap.

1. **Python 3.12** w świeżym venv (inaczej cichy powrót do koła CUDA z PyPI, które nie zadziała), potem polecenie instalacyjne z §3.1. Upewnij się, że zainstalował się build ROCm.
2. **Zacznij od jednej karty i małego modelu HF w BF16.** Dopiero potem `-tp=4` (`vllm serve <model> --tensor-parallel-size 4`). Nie zaczynaj od modelu, który ledwie mieści się w 4×32 GB.
3. **Zmniejsz `gpu_memory_utilization`** (domyślnie 0,92; nazwa flagi CLI: sprawdź w `vllm serve --help`) i wyłącz inne procesy na kartach — vLLM zarezerwuje resztę.
4. **Przeczytaj log startowy:** który backend uwagi wybrano (`ROCM_ATTN` czy `TRITON_ATTN`), którego jądra W4A16 użyto, czy MRV2 jest włączony na ROCm (nie wiem), jakie tryby grafów przechwycono i ile to trwało.
5. **Checkpoint GPTQ/AWQ INT4**, by sprawdzić, że wybierane jest `RDNAHybridW4A16LinearKernel` — rozstrzygnie to spór „dokumentacja kontra kod”. Potem checkpoint **FP8** (`compressed-tensors`).
6. **Ustaw `VLLM_NO_USAGE_STATS=1` (lub `DO_NOT_TRACK=1`)** na początku.
7. **Nie włączaj AITER na początku** (`VLLM_ROCM_USE_AITER` domyślnie False; na gfx12 i tak są tylko jądra Triton). Dopiero po uzyskaniu stabilnego wyniku bazowego sprawdź, czy zmienia cokolwiek.
8. **Pomiar uczciwy:** `vllm bench` (jest w `entrypoints/cli/benchmark`) przy **tej samej** liczbie równoległych zapytań, na którą liczysz w aplikacjach agentowych; porównaj z llama.cpp na tym samym modelu tylko, jeśli kwantyzacje są porównywalne. Pamiętaj, że wynik przy batchu 1 jest *nie* tym, do czego vLLM został zaprojektowany.
9. **Na końcu, jeśli w ogóle:** `vllm-gguf-plugin` z przykładową składnią z §3.4 na małym modelu — wyłącznie z ciekawości, bez nadziei na prędkość.

> **Sprawdź sam (2) — czy karta (np. R9700) jest znana i co ma w kwantyzacji.**
> ```bash
> grep -n "0x7551\|0x7550" vllm/platforms/rocm.py
> sed -n '541,547p' vllm/model_executor/kernels/linear/__init__.py
> grep -n "AWQ\|GPTQ\|GGUF" docs/features/quantization/README.md | head
> ```
> Porównaj ostatnie dwa wyniki: to jest rozbieżność dokumentacja–kod z §3.3. *(Nie uruchamiałem; ścieżki z notatek.)*

---

## 4. SGLang od środka

**Jedna linia:** wysokoprzepustowy silnik LLM/VLM (Python + PyTorch + jądra Triton/CUDA/HIP, bramka w Ruście), zbudowany wokół ponownego użycia prefiksu (RadixAttention) i języka frontowego do „programów LLM”; dziś silnik klasy vLLM z największym naciskiem na agentów, RL i modele MoE w stylu DeepSeek.

> ⚠️ **R9700 (gfx1201) nie jest obsługiwanym celem SGLang.** Skrypt budujący jądra dla ROCm przyjmuje tylko `gfx942`, `gfx950` i `gfx1250` (`python/sglang/kernels/aot/setup_rocm.py:66–79`: „Unsupported GPU architecture … Expected gfx942, gfx950, or gfx1250”). W repo nie ma Dockerfile dla gfx1200/1201. Szczegóły w §4.5.

### 4.1 Tożsamość

| | |
|---|---|
| Licencja | Apache-2.0 |
| Repozytorium | github.com/sgl-project/sglang; utworzone 2024-01-08 (artykuł z 2023-12); organizacja `sgl-project` od 2023-10-13 |
| Aktualna wersja | **v0.5.22, 2026-10-19**; v0.5.21 2026-10-02; v0.5.20 2026-09-18 (rytm ~2 tygodnie) |
| Gwiazdki / forki | 37 445 / 9 697 (API, 2026-10-19) |
| Języki (bajty) | Python 95,8 MB, Rust 11,0 MB, CUDA 4,8 MB, C++ 1,9 MB, Go 0,1 MB, HIP 65 KB, Metal 11 KB |
| Linie w migawce | `srt/` (runtime) 905 669; `srt/layers` 206 385; `srt/models` 191 806; `srt/mem_cache` 91 816; `srt/managers` 44 415; `srt/disaggregation` 35 154; `srt/speculative` 31 492; jądra `python/sglang/kernels/` 450 109; bramka `sgl-model-gateway/` 112 513 |
| Dokumentacja | docs.sglang.io, cookbook.sglang.io |

**Artykuł:** „SGLang: Efficient Execution of Structured Language Model Programs”, arXiv 2312.07104 (2023-12-12, rev. 2024-06-06). Autorzy: Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao, Christos Kozyrakis, Ion Stoica, Joseph E. Gonzalez, Clark Barrett, Ying Sheng. Abstrakt: „RadixAttention for KV cache reuse and compressed finite state machines for faster structured output decoding”; „up to 6.4x higher throughput compared to state-of-the-art inference systems” — to **własny benchmark autorów, z bazami z 2023 roku** *(dane projektu)*. Według Wikipedii *(źródło zewnętrzne)* projekt przedstawiono publicznie w styczniu 2024 (badacze ze Stanfordu, UC Berkeley, Texas A&M i SJTU), a artykuł pojawił się na NeurIPS 2024.

**Do kogo.** Do programów LLM, nie pojedynczych promptów: pętli agentowych z wieloma wywołaniami, rozgałęzień, structured output, rozmów wieloturowych i rolloutów RL, gdzie zapytania mają wspólne długie prefiksy. README opisuje dziś projekt jako „optimized for agentic workloads, large-scale serving, and RL rollouts” i dodaje silnik generowania obrazów/wideo („SGLang Diffusion”). To nie aplikacja desktopowa.

**Dwie połówki:** „Fast Backend Runtime” (`srt` — SGLang Runtime) i „Flexible Frontend Language” (`python/sglang/lang`: `api.py`, `interpreter.py`, `ir.py`, `tracer.py`…; DSL osadzony w Pythonie z operacjami gen/select/fork/join). W praktyce większość użytkowników woła dziś OpenAI API runtime i ignoruje DSL — *niezweryfikowane*, nie mam danych o adopcji.

### 4.2 Proces i scheduler

**Trzy etapy** (docstring `srt/entrypoints/engine.py:247–253`):

```
 HTTP / Engine  ┌──────────────────┐  ZMQ  ┌─────────────────────┐  ZMQ  ┌───────────────────────┐
 ─────────────► │ TokenizerManager │ ────► │ Scheduler           │ ────► │ DetokenizerManager    │
                │ (proces główny)  │       │ (podproces)         │       │ (podproces)           │
                │ tokenizacja      │       │ planuje + uruchamia │       │ detokenizacja, tekst  │
                └──────────────────┘       │ GPU (TpModelWorker/ │       │ wraca do klienta      │
                                           │ ModelRunner)        │       └───────────────────────┘
                                           └─────────────────────┘
```

Różnica wobec vLLM: scheduler i worker GPU żyją **w tym samym procesie** na kartę (brak osobnego skoku IPC EngineCore→worker): `managers/scheduler.py` woła `run_batch` → `tp_worker`. Liczby procesów przy DP nie prześledziłem (istnieje `data_parallel_controller.py`).

**Główna pętla** (`srt/managers/scheduler.py`, 6278 linii — plik jest węzłem mixinów z `scheduler_components/`, `scheduler_pp_mixin.py`, `schedule_batch.py` 4059 linii z `Req` i `ScheduleBatch`, `schedule_policy.py` 1713 linii i `tp_worker.py`):

- `event_loop_normal` (`scheduler.py:1976`): `ingest_requests()` → `get_next_batch_to_run()` → `run_batch()` → `process_batch_result()` → od nowa.
- `event_loop_overlap` (`scheduler.py:2011`): to samo, ale trzyma `result_queue` z wynikiem **poprzedniego** batcha i przetwarza go dopiero po wystartowaniu następnego. Praca CPU dla batcha N−1 (księgowanie detokenizacji, wstawienie do radix cache, sprawdzenie zakończeń, budowa batcha N+1) nakłada się na GPU liczące batch N. `is_disable_overlap_for_batch` wraca do trybu synchronicznego tam, gdzie trzeba (np. zależny prefill po prefillu).

```
 bez nakładania:  CPU: [przygotuj N]            [przetwórz N]  [przygotuj N+1]  ...
                  GPU:             [liczy N]                                  [liczy N+1]
                                   (GPU czeka na CPU po obu stronach)

 z nakładaniem:   CPU: [przygotuj N][przygotuj N+1 + przetwórz N-1 ][przygotuj N+2 + przetwórz N]
                  GPU:             [liczy N        ][liczy N+1        ][liczy N+2 ]
```

To „**zero-overhead batch scheduler**” z wydania v0.4: „The scheduler runs one batch ahead and prepares all the metadata required for the next batch”; deklarowane „1.1x speedup against its previous version and 1.3x against other state-of-the-art baselines”, największe dla małych modeli z dużym TP *(dane projektu, blog lmsys.org 2024-12-04)*.

**`get_next_batch_to_run`** (linia 3829): obsługuje przerwanie oczekującego chunked prefill, zdarzenia HiCache, łączy ostatni batch prefillu z biegnącym batchem dekodowania, wybiera nowy batch prefillu przez `SchedulePolicy` + `PrefillAdder` (budżet tokenów, `chunked_prefill_size`, świadomość radix cache), a w przeciwnym razie krok dekodowania.

**Polityki** (`schedule_policy.py:169–185`): świadome cache’u `lpm` (*longest prefix match*), `dfs-weight`, `hrrn` (*highest response ratio next*), `shortest-prefill-first`; niezależne od cache’u `fcfs`, `lof` (*longest output first*), `random`, `routing-key`. Domyślnej wartości nie czytałem, więc o niej nie piszę. Idea: **ustaw kolejkę oczekujących tak, by zapytania ze wspólnym prefiksem szły razem, zanim eksmisja go zniszczy** — to połówka RadixAttention odpowiedzialna za planowanie. Są też `prefill_delayer.py`, `min_free_slots_delayer.py` (przepustnice przyjęć).

### 4.3 RadixAttention: drzewo radix nad tokenami

`srt/mem_cache/radix_cache.py` (832 linii), `base_prefix_cache.py`, nowy `unified_radix_cache.py` (3911 linii) i `unified_cache/` — zbieżność wariantów Full/SWA/Mamba w jednym (`mem_cache/README.md`, issue #20415).

**Struktura.** Drzewo radix po identyfikatorach tokenów. Klucz: `RadixKey(token_ids, extra_key)`; `extra_key` tworzy przestrzeń nazw drzewa (różne adaptery LoRA albo sole cache nigdy nie dzielą węzłów); klucze są przed dopasowaniem wyrównywane do strony (`page_size`).

**Analogia:** to jak system plików, w którym „ścieżką” jest sekwencja tokenów, a katalog dzieli się dokładnie tam, gdzie dwie ścieżki przestają być wspólne. **Ściśle:** `match_prefix` zwraca najdłuższy prefiks z cache i **rozszczepia węzeł w miejscu**, gdy dopasowanie kończy się w środku segmentu („the node is split once to expose a precise boundary”); `insert` zapisuje indeksy slotów KV dla tokenów zapytania po jego wykonaniu.

Przykład: dwa zapytania agenta ze wspólnym system promptem (litery to tokeny, ilustracja):

```
Zapytanie 1:  S S S S S S | a b c            (S = system prompt + schematy narzędzi)
Zapytanie 2:  S S S S S S | x y z w

Po zapytaniu 1 drzewo ma jeden węzeł-liść:

   root ──► [ S S S S S S a b c ]                       (jeden segment)

Zapytanie 2 przychodzi. match_prefix dopasowuje 6 tokenów S i kończy się
w ŚRODKU segmentu → węzeł zostaje rozszczepiony:

   root ──► [ S S S S S S ] ──┬──► [ a b c ]            (zapytanie 1)
              (wspólny)       └──► [ x y z w ]          (zapytanie 2: tylko to się liczy od nowa)

Prefill zapytania 2 dotyczy 4 tokenów (x y z w), nie 10.
```

**Przypięcie:** `inc_lock_ref(node)` / `dec_lock_ref` — węzły używane przez zapytania w locie mają `lock_ref > 0` i nie mogą zostać wyeksmitowane.

**Eksmisja** (`radix_cache.py:552–580`): zbierane są `evictable_leaves`, budowany kopiec po `eviction_strategy.get_priority(node)`, zdejmowane są najniższe, aż zwolni się `num_tokens`; zwolnienie liścia może uczynić rodzica liściem i wrzucić go na kopiec — eksmisja idzie więc gałęzią od czubka do korzenia. Polityki (`radix_eviction_policy.mdx`): `lru` (domyślna), `lfu`, `slru`, `priority`, `tlru` (świadoma TTFT, dla ogonów agentowych).

**Pamięć pod drzewem** (`mem_cache/README.md`): `allocation.py` → `hybrid_cache/` (router warstwa→pula) → `allocator/` („daj mi N slotów”) → `pool/` (KV na urządzeniu, L1) → `pool_host/` (L2) → `storage/` (L3). W oryginalnym projekcie sloty są **tokenowe** (strona = 1, „token attention”), nie bloki po 16 tokenów jak w vLLM; stronicowanie włącza się `page_size>1` (wymagane przez niektóre jądra) — domyślnej wartości nie zweryfikowałem.

**HiCache:** hierarchiczny cache KV L1 GPU → L2 pamięć hosta → L3 magazyny (plik, NIXL, HF3FS, Mooncake…).

**Kontrast z vLLM:**

| | vLLM | SGLang |
|---|---|---|
| Struktura | łańcuch hashy pełnych bloków | jawne drzewo radix z rozszczepianiem węzłów |
| Ziarnistość dopasowania | cały blok | token (przy page_size=1) |
| Planowanie | FCFS/priorytet; prefiks pomaga „przy okazji” | polityki świadome prefiksu (`lpm`, `dfs-weight`) |
| Routing | zdarzenia KV dla zewnętrznych routerów | wbudowana bramka `cache_aware` |

### 4.4 Wykonanie modelu, jądra, bramka

**Executor** (`srt/model_executor/`, 24 057 linii): `model_runner.py` (2593), `forward_batch_info.py` (2338; `ForwardBatch`), runnery grafów CUDA rozdzielone na `runner/decode_cuda_graph_runner.py` (1747) i `runner/prefill_cuda_graph_runner.py` (2353) — **SGLang przechwytuje także grafy prefillu**; `cpu_graph_runner.py`, `pool_configurator.py`.

**Backendy uwagi.** `srt/layers/attention/` zawiera FlashInfer, FlashAttention (FA3/FA4), Triton, TRT-LLM MHA/MLA, FlashMLA, CuTe-DSL MLA, Torch-native/Flex, a dla AMD `aiter_backend.py`, `wave_backend.py`, `hip_flash_mla.py`. Dokumentacja wyboru: dla Blackwell SM120 (RTX PRO 6000) `triton` lub `flashinfer`; dla ROCm „`triton` recommended” (linia 403).

**Jądra** (`python/sglang/kernels/`, 450 tys. linii): `aot/` (dawny `sgl-kernel`, jądra kompilowane z wyprzedzeniem CUDA/HIP/CPU/MUSA — historia *niezweryfikowana*), `jit/` (szablony kompilowane w locie), `ops/`. SGLang opiera się na **FlashInfer** (przypięte `flashinfer_python==0.7.2`, `python/pyproject.toml`) oraz DeepGEMM/DeepEP/FlashMLA z DeepSeek dla MoE.

**Bramka** (`sgl-model-gateway/`, Rust): płaszczyzna sterowania (rejestr workerów, zdrowie, odkrywanie w K8s) i płaszczyzna danych (routery HTTP i gRPC, routing PD, router OpenAI proxy do zdalnych dostawców) z politykami `random`, `round_robin`, `cache_aware`, `power_of_two`, `bucket`, ponowieniami, wyłącznikami awaryjnymi, limitami, OTel/Prometheus. Deklaracja z bloga v0.4: router świadomy cache’u podnosi przepustowość z 82 665 do 158 596 tok/s (1,9×), a trafienia cache z 20% do 75%, na 8×A100-80GB, Llama-3.1-8B-Instruct, obciążenie z wieloma grupami prefiksów *(dane projektu; podany setup)*.

### 4.5 Dezagregacja, ekspertów, spekulacja, API

- **Dezagregacja** (`srt/disaggregation/`, 35 154 linii): prefill/decode z backendami transferu Mooncake, NIXL, MoRI (ROCm), Ascend; plus enkoder/prefill/decode („EPD”) dla multimodalności.
- **Równoległość:** TP, PP (`scheduler_pp_mixin.py`), DP i „DP attention” (dla MLA/MoE), **expert parallel** z DeepEP i równoważeniem obciążenia EPLB (`srt/eplb`, `srt/elastic_ep`), context parallel dla długiego prefillu.
- **Spekulatywne dekodowanie** (`srt/speculative/`, 31 492 linii): EAGLE/EAGLE3 (workery v2 z runnerami grafów dla szkicu), multi-layer EAGLE, MTP („frozen_kv_mtp”), n-gram (`cpp_ngram`), warianty DFlash/dspark, parametry adaptacyjne. Zasada ogólna — w katalogu [`../przyspieszanie-generowania/README.md`](../przyspieszanie-generowania/README.md).
- **Structured output** (`srt/constrained/`): xgrammar, llguidance, outlines (z *jump-forward decoding*), backend świadomy rozumowania; z bloga v0.4: xgrammar „up to 10x faster” dla JSON niż inne rozwiązania open source *(dane projektu)*.
- **API** (`srt/entrypoints/`): OpenAI (chat, completions, embeddings, rerank, score, classify, tokenize, responses, audio), **Anthropic**, **Ollama**, gRPC, `Engine` offline. W przeciwieństwie do vLLM SGLang wysyła w drzewie fasadę zgodną z Ollamą.
- **Parsery** narzędzi i rozumowania: `srt/function_call/` (15 162 linii), `srt/parser/` (7640).
- **Inne:** LoRA, multimodal, wnioskowanie deterministyczne (`batch_invariant_ops`), synchronizacja wag dla RL (`weight_sync`, `checkpoint_engine`), beam search, scheduler „dLLM” dla modeli dyfuzyjnych.

### 4.6 SGLang na ROCm: lista obsługiwanych celów

Jak najprościej: **R9700 nie jest obsługiwanym celem.** Dowody z kodu i dokumentów:

1. Dokument AMD (`docs/docs/hardware-platforms/amd_gpu.mdx`) jest w całości pod MI300X (GRUB `iommu=pt`, balansowanie NUMA) i instaluje `sgl-kernel` przez `setup_rocm.py`.
2. `setup_rocm.py` akceptuje cele **`["gfx942", "gfx950", "gfx1250"]`**; dla reszty ostrzega „Unsupported GPU architecture”.
3. Obrazy Dockera: `docker/rocm.Dockerfile` z `GPU_ARCH=gfx942|gfx950|gfx1250` oraz **osobny** `docker/rocm-gfx1151.Dockerfile` dla Strix Halo (komentarz: „This is NOT a variant of docker/rocm.Dockerfile … includes components which do not support gfx1151”, uruchamiany z `--attention-backend triton`). Nie ma Dockerfile dla gfx1200/1201.
4. Dokumentacja uwagi: „AMD (ROCm): triton recommended”; backendy `aiter` i `wave` istnieją.
5. Przeszukanie drzewa pod kątem `gfx1201`/`gfx1200` nie dało nic istotnego.
6. README deklaruje AMD Instinct MI300X/MI325X/MI350X/MI355X *(dane projektu)*.

Możliwe, ale **niezweryfikowane**: SGLang może działać na gfx1201 na gołym PyTorchu i uwadze Triton, bez `sgl-kernel`. Nikt tego nie deklaruje i dokumentacja tego nie wspomina, więc nie budowałbym na tym planu. GGUF w SGLang (`quantization.mdx`): „CUDA kernels in sgl-kernel; Ascend uses CPU pre-dequantization at load time” — **żadnych jąder ROCm**. Zwykły `gptq` jest „Removed on NVIDIA and AMD GPUs — use gptq_marlin instead”.

### 4.7 Mocne i słabe strony, offline, kto za tym stoi

**Mocne:** najlepsze w klasie ponowne użycie prefiksu i routing świadomy cache’u dla pętli agentowych; mocna praca nad DeepSeek/MoE (EP, EPLB, PD); API OpenAI + Anthropic + Ollama w jednym serwerze. **Słabe dla ciebie:** RDNA4 nie jest celem; silniejsze niż w vLLM sprzężenie z NVIDIA/FlashInfer; szybkie zmiany wewnętrzne (w migawce są w toku duże refaktory: unified cache, `arg_groups` — flagi i API zmieniają się między wydaniami 0.5.x, to *wniosek z układu plików*); dokumentacja AMD pisana pod MI300X.

**Offline.** Działa z lokalnymi wagami. Grep po `python/sglang` na `telemetry|usage_stats|posthog|DO_NOT_TRACK` znalazł tylko *tracing* OpenTelemetry (domyślnie wyłączony: `enable_trace`, `arg_groups/fields/observability.py:164`) i narzędzia testowe — **reportera użycia nie znalazłem** (dowód z braku wyniku grepa).

**Kto za tym stoi.** Projekt hostuje **LMSYS** (Large Model Systems Organization), według lmsys.org/about organizacja non-profit 501(c)(3) ustanowiona we wrześniu 2024, z pierwotnej współpracy Berkeley/Stanford/UCSD/CMU/MBZUAI *(dane organizacji)*; wspierana przez NVIDIA, Google Cloud, a16z, AMD, Hugging Face, Together i innych w gotówce, GPU i kredytach. SGLang dołączył do **ekosystemu PyTorch** (nie jest hostowany przez fundację). Autorzy z artykułu pracują dziś w różnych miejscach (profile GitHub: Lianmin Zheng — „Meta”; Liangsheng Yin i Ying Sheng — „RadixArk”). **RadixArk** to firma utworzona wokół SGLang; Wikipedia, powołując się na TechCrunch z 2026-01-21, podaje wycenę 400 mln USD *(prasa, jedno źródło)*; kwoty rundy, inwestorów i założycieli nie ustaliłem. Po szczegóły — [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

> **Sprawdź sam (3) — jakie architektury ROCm zna SGLang.**
> ```bash
> sed -n '60,80p' python/sglang/kernels/aot/setup_rocm.py
> ls docker/ | grep -i rocm
> grep -rn "gfx1201\|gfx1200" python/sglang docker | head
> ```
> Pierwsze polecenie pokaże `["gfx942", "gfx950", "gfx1250"]`; trzecie, wg notatek, nie znajduje nic istotnego. *(Nie uruchamiałem; ścieżki z notatek.)*

---

## 5. TensorRT-LLM, TGI (archiwum i lekcja), LMDeploy

### 5.1 TensorRT-LLM (NVIDIA)

**Jedna linia:** własny stos NVIDIA dla kart NVIDIA — wykonawca w PyTorchu wokół ręcznie strojonych jąder CUDA/CUTLASS i menedżera batchy/KV w C++, który istnieje po to, by wycisnąć ostatni czynnik z krzemu NVIDIA (FP8/NVFP4, NVLink, Blackwell).

- **Licencja:** GitHub pokazuje `NOASSERTION` („Other”). Powód z pliku `LICENSE`: „This project is licensed under the Apache 2.0 license … contains portions of code that are based on or derived from other open source projects, which may have different licenses”, a dalej lista atrybucji (Bitcoin Core MIT, causal-conv1d BSD-3, CUTLASS BSD-3 …). Czyli: **kod NVIDIA na Apache-2.0 plus noty o cudzym kodzie; detektor GitHuba nie umie wybrać jednego identyfikatora SPDX.**
- Repo `NVIDIA/TensorRT-LLM`, utworzone 2023-08-16, 14 859 gwiazdek, 2838 forków; wersja w README **1.4.0rc1**, wydania co tydzień (v1.4.0rc0 2026-10-14, v1.3.0rc29 2026-09-29). Języki: Python 78,3 MB, C++ 29,3 MB, CUDA 6,9 MB.
- **Sprzęt:** wyłącznie NVIDIA: Blackwell B200/GB200/B300/GB300/DGX Spark; Hopper H100/H200/GH200; Ada L20/L40/L40S; Ampere A100 (`docs/source/supported-hardware.md`). Nie AMD, nie Apple, nie CPU.
- **Zmiana architektury (zweryfikowana):** `docs/source/legacy/tensorrt-backend-removal.md`: „**Breaking change. The TensorRT engine backend has been removed. PyTorch is now the sole execution backend**”. Zniknęły `trtllm-build`, `trtllm-refit`, `trtllm-prune`, per-modelowe `convert_checkpoint.py` i zależność `tensorrt`; „no engine-build step — HuggingFace checkpoints load directly”. Zostały `trtllm-serve <hf_model>`, `trtllm-bench`, `trtllm-eval`. Stary projekt (kompilacja silnika zależnego od modelu, GPU i kształtów z wyprzedzeniem) jest powodem, dla którego TRT-LLM pamięta się jako bolesny — i dlaczego **wszystkie artykuły o `trtllm-build` są nieaktualne**.
- **Dziś:** `tensorrt_llm/_torch/pyexecutor/py_executor.py` (9532 linie) to pętla wykonawcza w Pythonie; część C++ (`cpp/tensorrt_llm/batch_manager/`: `capacityScheduler.cpp`, `microBatchScheduler.cpp`, `kvCacheManager.cpp`, `evictionPolicy.cpp`, `cacheTransceiver.cpp`) jest wystawiona do Pythona przez nanobind, a ok. 531 tys. linii jąder (uwaga, MoE, GEMM, all-reduce, kwantyzacja) jest podpiętych jako operacje torch przez `thop/`. Dokumentacja: „In-flight batching (also known as continuous batching or iteration-level batching)”; domyślne `max_num_tokens` 8192; jest *overlap scheduler* i piecewise CUDA graph + `torch.compile`.
- **Funkcje:** `trtllm-serve` zgodny z OpenAI z **adapterem Anthropic**, Responses API, adapter Harmony (gpt-oss), serwer zdezagregowany; paged KV z ponownym użyciem bloków; chunked prefill; spekulacja (EAGLE, MTP, n-gram); LoRA; guided decoding; multimodal.
- **Wydajność:** nagłówkowe liczby są NVIDIA-owe *(dane firmy)* (np. DeepSeek-R1 „world-record” na Blackwell; Llama 4 Maverick „breaks the 1,000 TPS/user barrier on B200”) — nie otwierałem postów źródłowych.
- **Telemetria — domyślnie włączona:** `tensorrt_llm/usage/__init__.py`: anonimowe statystyki idą do usługi telemetrycznej NVIDIA (NvTelemetry/GXT), domyślnie `https://events.gfe.nvidia.com/v1.1/events/json` (`usage_lib.py:79`); wyłączenie: `TRTLLM_NO_USAGE_STATS=1`, `TELEMETRY_DISABLED=true|1`, `DO_NOT_TRACK=1`, plik `~/.config/trtllm/do_not_track`, `TelemetryConfig(disabled=True)` lub `--no-telemetry`.
- **Kto za tym stoi:** pracownicy NVIDIA (w rankingu committerów boty `tensorrt-cicd`, `trtllm-agent`, potem etatowcy); produkt strategiczny, który sprzedaje GPU. Zarządzanie firmowe. Ryzyko licencyjne niskie, noty cudzego kodu trzeba respektować.
- **Dla ciebie:** wyłącznie edukacyjnie — pokazuje, skąd bierze się wydajność specyficzna dla NVIDIA.

### 5.2 TGI (Hugging Face) — archiwum i lekcja

**Jedna linia:** serwer LLM Hugging Face z routerem w Ruście i shardami Pythona po gRPC, silnik Inference Endpoints/HuggingChat; dziś w trybie utrzymania, a repozytorium jest zarchiwizowane.

- Repo `huggingface/text-generation-inference`, utworzone 2022-10-08; 10 879 gwiazdek; **`archived = true`**; ostatni push 2026-03-21 (commit dokumentacyjny); ostatnie wydanie **v3.3.7, 2025-12-19**.
- **Komunikat w README** (commit „Maintenance mode (#3344)”, **2025-12-11**): „text-generation-inference is now in maintenance mode. Going forward, we will accept pull requests for minor bug fixes, documentation improvements and lightweight maintenance tasks. TGI has initiated the movement for optimized inference engines to rely on a `transformers` model architectures. This approach is now adopted by downstream inference engines, which we contribute to and recommend using going forward: **vllm, SGLang, as well as local engines with inter-compatibility such as llama.cpp or MLX.**” Nie znalazłem datowanego ogłoszenia „zarchiwizowano”; decyzja o trybie utrzymania to 2025-12-11, a flaga archiwum i ostatni push wskazują na marzec 2026.
- **Historia licencji** (z commitów dotykających `LICENSE`): Apache-2.0 (2022) → **2023-07-28 zmiana na HFOIL** (restrykcyjna licencja HF; „chore: update license to HFOIL (#725)”) → **2024-04-08 powrót do Apache-2.0** („Revert license to Apache 2.0 (#1714)”). Powodów żadnej ze zmian w repo nie znalazłem — nie podaję ich.
- **Funkcje:** router z ciągłym batchowaniem, strumieniowanie SSE, tensor parallel, API Messages zgodne z OpenAI, Flash/Paged attention (README wprost wskazuje PagedAttention z vLLM), kwantyzacje bitsandbytes/GPTQ/EETQ/AWQ/Marlin/fp8, prowadzone gramatyką narzędzia. Backendy: CUDA własne (`v2`, `v3`), TRTLLM, Llamacpp, Neuron (AWS), Gaudi; obrazy dla ROCm obejmują „AMD Instinct MI210, MI250 and MI300” — **żadnych Radeonów**.
- **Telemetria:** statystyki użycia tylko „when TGI is running in a Docker container” (start/stop plus heartbeat co 15 minut; `router/src/usage_stats.rs`).
- **Kto za tym stoi:** Hugging Face jako firma (produkty Inference Endpoints, HuggingChat); autorzy: Olivier Dehaene (oryginalny autor), Nicolas Patry, Daniël de Kok.

**Lekcja (ugruntowana):**

1. HF przestał utrzymywać własne zoo implementacji modeli. TGI miało ręcznie napisany, zoptymalizowany kod per architektura; nowy kierunek to „silniki polegają na definicjach modeli z `transformers`”. Utrzymywanie jąder per architektura nie skalowało się przeciw społeczności vLLM/SGLang (to *interpretacja*; sam komunikat jest zweryfikowany).
2. Zawirowanie licencyjne (Apache → HFOIL → Apache) kosztowało zaufanie i mogło pomóc adopcji vLLM/SGLang — *niezweryfikowane*.
3. Router w Ruście + shardy Pythona po gRPC to dobry podział; nowy front-end Rust w vLLM i bramka Rust w SGLang odtwarzają go.
4. **Dla ciebie:** wybieraj silniki z fundacją lub wieloma sponsorami. Jeden właściciel to jeden pojedynczy punkt decyzji o porzuceniu projektu.

### 5.3 LMDeploy (TurboMind)

**Jedna linia:** zestaw do kompresji, wdrażania i serwowania LLM/VLM z dwoma silnikami — TurboMind (C++/CUDA; README dziękuje NVIDIA FasterTransformer) i czysto pythonowym silnikiem PyTorch — zbudowany przez zespoły MMRazor/MMDeploy wokół modeli InternLM.

- Apache-2.0; repo `InternLM/lmdeploy`, utworzone 2023-06-15; 8108 gwiazdek; **v0.18.0, 2026-09-28**; Python 10,2 MB, C++ 2,9 MB, CUDA 1,4 MB.
- **Funkcje** *(dane projektu, README)*: kwantyzacja wag 4-bitowa (AWQ-podobna W4A16) i KV int4/int8 z jąder TurboMind, trwały batch (ciągłe batchowanie), blokowy KV, dynamiczny split&fuse, TP, prefix caching, serwer proxy dla wielu maszyn i modeli, dezagregacja PD przez DLSlime/Mooncake (2025/06), MXFP4 na NVIDIA od V100 w górę.
- **Wydajność:** własne deklaracje: „do 1,8× wyższa przepustowość zapytań niż vLLM” (InternLM2-20B, 2024); artykuł „LMDeploy Accelerates Mixed-Precision LLM Inference with TurboMind”, arXiv 2508.15601: „up to 61% lower serving latency (30% on average) and up to 156% higher throughput (58% on average)” względem konkurencyjnych frameworków mieszanej precyzji, 16 LLM i 4 architektury GPU — **benchmark autorów**.
- **Sprzęt:** NVIDIA Volta..Ada; silnik PyTorch dodaje Ascend, Cambricon, MetaX. **ROCm:** instalacja możliwa przez `LMDEPLOY_TARGET_DEVICE=rocm pip install git+...` w kontenerze `rocm/pytorch`, bez listy obsługiwanych GPU; szybki silnik TurboMind jest tylko dla CUDA. **Brak dowodów dla RDNA4.**
- **Architektura** (tylko drzewo z API; kodu nie klonowałem): `lmdeploy/turbomind/` + `src/turbomind/` (C++/CUDA), `lmdeploy/pytorch/` (silnik w Pythonie, łatwiejszy do rozszerzania na nowy sprzęt), `lmdeploy/serve/`, `lmdeploy/vl/`, `lmdeploy/lite/` (kwantyzacja). Zakład projektowy: wydajny silnik w C++ plus hakowalny silnik w Pythonie.
- **Kto za tym stoi:** projekt laboratoryjno-przemysłowy (zespoły MMRazor/MMDeploy, rodzina InternLM — związek ze Shanghai AI Laboratory to *wniosek*, nie ustalony fakt); brak znalezionej firmy ani finansowania; społeczność chińskojęzyczna. Ciekawostka operacyjna: README z kwietnia 2026 wspomina o rozszerzeniu limitu PyPI, co wskazuje, że wielkie koła CUDA przekraczały limity.

---

## 6. Warstwy klastrowe: Dynamo, llm-d, LMCache, FlashInfer, FlashAttention, Modular MAX

Te elementy stoją **nad** silnikiem, **obok** niego albo **pod** nim. Powstały dlatego, że gdy masz wiele GPU, wiele węzłów i tysiące użytkowników, jednostką optymalizacji przestaje być „jeden silnik”, a staje się „flota”. Przy każdej karcie odpowiedź na pytanie: **czy czterokartowe pudło tego potrzebuje?**

### NVIDIA Dynamo

- **Warstwa:** orkiestracja *nad* silnikami. README: „the orchestration layer above inference engines — it doesn't replace SGLang, TensorRT-LLM, or vLLM, it turns them into a coordinated multi-node inference system”. Rdzeń w Ruście, Python do rozszerzeń.
- **Tożsamość:** `ai-dynamo/dynamo`, utworzone 2025-03-03, 8332 gwiazdki. GitHub pokazuje `NOASSERTION`, bo `LICENSE` zaczyna się od noty o danych testowych na MIT; „The rest of this codebase is licensed under the Apache License 2.0”.
- **Co robi:** dezagregacja prefill/decode z niezależnymi pulami GPU; **routing świadomy KV** (do workera z największym nakładaniem cache i najmniejszym obciążeniem); **KVBM** (przerzucanie bloków GPU→CPU→SSD→zdalny magazyn); **ModelExpress** (strumieniowanie wag GPU→GPU przez NIXL/NVLink); **Planner** (autoskalowanie wg SLA); **Grove** (operator K8s z gang schedulingiem uwzględniającym topologię, NVL72). Obsługuje SGLang, TensorRT-LLM i vLLM; w tym, co czytałem, walidowany na sprzęcie NVIDIA, o ROCm nie znalazłem wzmianki w README.
- **Liczby** *(dane firmy, partnerów; różne sprzęty — nie porównuj)*: „7x wyższa przepustowość na GPU, DeepSeek R1 na GB200 NVL72 vs B200 bez tego”, „750x … na GB300 NVL72”, „80% mniej naruszeń SLA przy 5% niższym TCO (Alibaba)”.
- **Czy potrzebujesz?** **Nie.** Sam README mówi: „If you're running a single model on a single GPU, your inference engine alone is probably sufficient”. Wartość edukacyjna: najczystszy obraz tego, co dzieje się *po* jednym pudle.

### llm-d

- **Warstwa:** natywna dla Kubernetesa warstwa serwowania rozproszonego *nad* serwerami modeli (vLLM, SGLang): routing świadomy prefiksu i obciążenia, wielopoziomowy offload KV z indeksem globalnym, dezagregacja PD, szeroki expert parallel, kontrola przepływu, autoskalowanie świadome SLO, batch API.
- **Tożsamość:** `llm-d/llm-d`, Apache-2.0, utworzone 2025-04-29, 4866 gwiazdek; v0.10.0 (2026-09-29). „a Cloud Native Computing Foundation (CNCF) sandbox project, founded by Red Hat, Google Cloud, IBM Research, CoreWeave, and NVIDIA”; do CNCF dołączył w 2026-03.
- **Ludzie:** czołowi committerzy z Red Hat/@llm-d, Google (Abdullah Gharaibeh) i Robert Shaw (Red Hat, również rdzeń vLLM) — oś vLLM–Red Hat jest w nim centralna.
- **Liczby** *(dane partnerów)*: „3× wyższa przepustowość wyjściowa i 2× szybszy TTFT z routingiem świadomym prefiksu vs round-robin, Llama 3.1 70B na 4× AMD MI300X (Red Hat)”; „13,9× przepustowość z hierarchicznym offloadem KV przy 250 użytkownikach, 4× H100”. Część wyników jest na **AMD MI300X**, więc llm-d nie jest zamknięty na NVIDIA — ale to Instinct, nie RDNA.
- **Czy potrzebujesz?** **Nie** — wymaga Kubernetesa. Z całego narzędzia przydaje ci się *idea*: kieruj zapytania z tym samym prefiksem do tego samego backendu.

### LMCache

- **Warstwa:** warstwa zarządzania KV cache poza pamięcią GPU: przechowuje KV w RAM-ie CPU, na SSD, w Redis/Valkey, Mooncake, S3, NIXL, GDS; używa go ponownie między zapytaniami, sesjami i instancjami silnika; przenosi między workerami prefill i decode. Obsługuje **ponowne użycie nie-prefiksowe** (CacheBlend: kawałki z dowolnej pozycji z selektywnym przeliczeniem); tryb wieloprocesowy `lmcache server` przeżywa awarię silnika.
- **Tożsamość:** `LMCache/LMCache`, Apache-2.0, utworzone 2024-05-28, 12 116 gwiazdek; nocne buildy dla **ROCm i XPU**; vLLM ma konektory pierwszej klasy (`lmcache_connector.py`, `lmcache_mp_connector.py`), ale jego Dockerfile ROCm buduje LMCache tylko dla gfx942/gfx950; integruje się też z Dynamo.
- **Kto:** w LMCache blog dołączenie do PyTorch Foundation jako projekt ekosystemu (2025-10-31) oraz firma **Tensormesh** (zespół LMCache i vLLM production stack). Deklarowanych przez stronę Tensormesh kwot finansowania nie potwierdziłem — nie podaję ich. Rodowód uniwersytecki — *niezweryfikowany*.
- **Czy potrzebujesz?** **Raczej nie.** vLLM ma własny offload KV na CPU (`kv_offload/`), więc ok. 80% idei dostajesz bez LMCache (*niezweryfikowane*, wniosek). Analogia desktopowa: zapis/odtwarzanie slotu w llama.cpp.

### FlashInfer

- **Warstwa:** biblioteka jąder serwowania: uwaga (paged/ragged KV, decode/prefill/append, MLA, cascade, sparse), GEMM (FP8, NVFP4/MXFP4 na Blackwell), fuzowany MoE, próbkowanie top-k/top-p, komunikacja. **Tylko NVIDIA, SM75 i nowsze.**
- **Tożsamość:** `flashinfer-ai/flashinfer`, Apache-2.0, utworzone 2023-07-22, 6708 gwiazdek, v0.7.2 (2026-10-15). Artykuł arXiv 2501.01005, MLSys 2025, autorzy m.in. Zihao Ye, Tianqi Chen, Luis Ceze; deklarowane 29–69% redukcji opóźnienia międzytokenowego względem backendów kompilatorowych *(dane autorów)*. Pod SGLang (twarda zależność) i vLLM; opcjonalnie w TRT-LLM.
- **Czy potrzebujesz?** **Nie, nie masz do tego ścieżki.** Wiedz, że każdy benchmark vLLM/SGLang na NVIDIA to po części benchmark FlashInfer.

### FlashAttention (Tri Dao)

- **Warstwa:** dokładne, zorientowane na IO fuzowane jądra uwagi, które nie materializują macierzy wyników N×N — korzeń całej rodziny (FlashInfer, fork `vllm_flash_attn` w vLLM, backendy FA3/FA4 w SGLang). Repo `Dao-AILab/flash-attention`, **BSD-3-Clause**, 25 161 gwiazdek. Wersje: FlashAttention (arXiv 2205.14135, NeurIPS 2022), FlashAttention-2, FlashAttention-3 (Hopper, FP8), **FlashAttention-4** w CuTeDSL dla Hopper i Blackwell.
- **Ludzie:** Tri Dao — profesor na Princeton, współzałożyciel i główny naukowiec Together AI (tridao.me).
- **Wątek AMD, bezpośrednio dla R9700** (README, „AMD ROCm Support”): dwa backendy. (1) **Composable Kernel (CK)** — FlashAttention-2, „MI200x, MI250x, MI300x, MI355x, and RDNA 3/4 GPUs”; (2) **backend Triton** (`FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"`) dla CDNA i RDNA w fp16/bf16/fp32, z maskami przyczynowymi, długościami zmiennymi, MQA/GQA, ALiBi, paged attention i FP8 przez interfejs FA3; jądra z pakietu ROCm `aiter` dołączonego jako submoduł. vLLM wykorzystuje to tylko dla enkoderów wizyjnych na RDNA przy ustawionej zmiennej środowiskowej (§3.2).
- **Czy potrzebujesz?** Algorytm już masz — przez własne jądra flash attention w llama.cpp. Deklaracja „FA2-CK dla RDNA 3/4” jest warta testu, gdybyś kiedyś uruchamiał stosy oparte o PyTorch.

### Modular MAX / Mojo

- **Warstwa:** pionowo zintegrowany stos: język Mojo (składnia Pythona na MLIR), framework i jądra MAX, serwer zgodny z OpenAI; hasło „one code base for any accelerator”.
- **Tożsamość:** `modular/modular`, 29 977 gwiazdek; wersja `max/v26.6.0` (2026-09-17). **Dwie licencje**: repozytorium na „Apache License v2.0 with LLVM Exceptions”, a użycie MAX na „Modular Community License” (warunków nie czytałem). Kompilator Mojo otwarty w sierpniu 2026.
- **Firma:** założona przez Chrisa Lattnera (LLVM, Clang, Swift) i Tima Davisa *(dane firmy)*. **Qualcomm ogłosił przejęcie 2026-06-24 i sfinalizował 2026-07-29** (cena nieujawniona) *(dane firmy; nie otwarłem komunikatu Qualcomma)*. Wcześniejszych rund finansowania nie zweryfikowałem — nie podaję.
- **Sprzęt** *(dane firmy, strona pakietów)*: NVIDIA B200 „tested for serving”; AMD MI355X tested for serving; **„Radeon RX 7900/7800/7600 (RDNA3) and newer RDNA4 variants are compatible”** (sterownik AMD 6.3.3+); Apple M1–M5 „actively developing”. „Compatible” jest słabsze niż „tested”; liczby dla gfx1201 nie znalazłem. To **jedyny silnik poza vLLM w tym rozdziale z deklaracją zgodności z RDNA4**.
- **Czy potrzebujesz?** Nie jako produkcyjnego zamiennika vLLM/SGLang — pokrycie modeli jest mniejsze (*niezweryfikowane*), a właściciel nowy. Warto na weekendowy test, jeśli interesuje cię przenośność Mac + AMD.

> **Sprawdź sam (4) — status TGI i zachowanie wydań.**
> ```bash
> gh api repos/huggingface/text-generation-inference --jq '.archived, .pushed_at'
> gh api "repos/vllm-project/vllm/releases?per_page=5" --jq '.[].tag_name, .[].published_at'
> ```
> Pierwsze powinno dać `true` i datę marca 2026; drugie pokaże rytm wydań vLLM. *(Nie uruchamiałem tych poleceń; zgodnie z konfiguracją `gh` wymaga uruchomienia poza piaskownicą.)*

---

## 7. Tabela porównawcza: vLLM, SGLang, TensorRT-LLM, llama.cpp

Wyłącznie z notatek; stan 2026-10-19; stars z API GitHuba.

| | **vLLM** | **SGLang** | **TensorRT-LLM** | **llama.cpp** |
|---|---|---|---|---|
| Licencja | Apache-2.0 | Apache-2.0 | Apache-2.0 + noty cudzego kodu (GitHub: NOASSERTION) | MIT |
| Gwiazdki | 94 152 | 37 445 | 14 859 | 131 716 |
| Wersja | v0.32.0 (2026-10-18) | v0.5.22 (2026-10-19) | 1.4.0rc1 (RC co tydzień) | b11741 (numery buildów, bez semver) |
| Główne języki | Python (+Rust, CUDA, C++) | Python (+Rust bramka, CUDA) | Python + C++ + CUDA | C/C++ |
| Cel | przepustowość wielu użytkowników | agenci, RL, prefiksy, MoE | maksimum na NVIDIA | jeden użytkownik, lokalnie |
| Zarządzanie KV | bloki + tablica bloków, hash-łańcuch prefiksów | drzewo radix, sloty tokenowe, HiCache | paged KV z ponownym użyciem bloków (C++) | ciągły KV na slot; dopasowanie LCP, cache RAM `--cache-ram 8192` MiB, punkty kontrolne kontekstu; **brak** PagedAttention |
| Ciągłe batchowanie | tak, scheduler budżetu tokenów | tak, polityki świadome prefiksu | tak (*in-flight batching*) | tak, ale prostszy scheduler; `-np` = liczba slotów, domyślnie 1 |
| Podział tensorowy | TP/PP/DP/EP/CP; „strong multi-GPU TP on identical cards” (ocena z notatek) | TP/PP/DP/EP (+ DP attention, context parallel) | obsługiwany; zorientowany na NVLink/NVL72 | `-sm tensor` **eksperymentalny**, wymaga flash attention i nieskwantowanego KV |
| Formaty | HF/safetensors; AWQ, GPTQ, FP8, FP4, compressed-tensors…; GGUF poza rdzeniem (wtyczka, „experimental”) | HF; FP8, FP4, AWQ, gptq_marlin…; GGUF tylko CUDA/Ascend | HF; FP8, NVFP4; INT4/INT8 | **GGUF** (HF przez konwersję) |
| API | OpenAI + Anthropic + Cohere + gRPC; **brak Ollama** | OpenAI + Anthropic + **Ollama** + gRPC | OpenAI + adapter Anthropic + Responses | OpenAI + Anthropic `/v1/messages` + Responses |
| Sprzęt | NVIDIA, ROCm, Intel XPU, CPU, TPU; wtyczki (Ascend, Gaudi, Metal…) | NVIDIA, AMD Instinct, TPU, Intel, Apple (README), Ascend | **tylko NVIDIA** | CPU + ok. 15 backendów (CUDA, HIP, Metal, Vulkan…) |
| **gfx1201 (R9700)** | **deklarowane**: dokumentacja, domyślne arch, PCI id, jądra RDNA; niezweryfikowane testem | **nieobsługiwane** (cele: gfx942/950/1250) | nie dotyczy | **działa** (build HIP na dokładne `gfx1201`) |
| Wymiana modeli | jeden model na proces; `/sleep` | nie ustalałem | nie ustalałem | tryb routera, `--models-max` domyślnie 4; llama-swap |
| Grafy / kompilacja | `torch.compile` kawałkami + grafy (domyślnie `FULL_AND_PIECEWISE`) | grafy decode **i** prefill | piecewise CUDA graph + `torch.compile` | brak odpowiednika w tych notatkach |
| Pre-alokacja pamięci karty | `gpu_memory_utilization` 0,92 | nie ustalałem | nie ustalałem | wg `-c` i `-ngl` |
| Telemetria | **włączona domyślnie**, opt-out | nie znaleziono | **włączona domyślnie**, opt-out | nie sprawdzałem w tych notatkach |
| Fundament | PyTorch Foundation (2025-05) | LMSYS (501(c)(3)) + ekosystem PyTorch | NVIDIA | firma/maintainerzy; zob. [rozdz. 04](04-LLAMA-CPP-I-RODZINA-GGML.md) |

Uwaga do wiersza „gfx1201 / llama.cpp”: to jest stan *twojej* produkcyjnej konfiguracji (llama.cpp + llama-swap na R9700), nie wynik z notatek serwerowych. Szczegółowe dane o HIP i `-sm tensor` w llama.cpp: [rozdz. 04](04-LLAMA-CPP-I-RODZINA-GGML.md).

⚠️ Nie porównuj wierszy „wydajność” — celowo ich nie ma. Notatki nie zawierają żadnego pomiaru na jednym sprzęcie dla wszystkich czterech silników, a liczby projektów pochodzą z różnych kart, modeli i obciążeń.

---

## 8. Co z tego dla konfiguracji referencyjnej

### 8.1 Kiedy przesiąść się z llama.cpp na vLLM/SGLang

Regułą kciuka z notatek (*opinia, niezweryfikowana*): **silniki serwerowe, gdy obciążenie to wiele równoczesnych zapytań ze wspólnymi prefiksami, a modele są w formacie HF (BF16/FP8/GPTQ-INT4); llama.cpp + llama-swap dla interaktywnej pracy w jednym strumieniu, różnorodności kwantów i częstej wymiany modeli.**

Rozbite na twoje powody:

| Sytuacja | Dlaczego silnik serwerowy | Uwaga dla maszyny referencyjnej |
|---|---|---|
| **Wielu agentów równolegle** (fan-out, wiele równoległych wywołań narzędzi) | batch amortyzuje czytanie wag (§1.1), ciągłe batchowanie utrzymuje GPU zajęte | llama.cpp też ma sloty (`-np`), ale prostszy scheduler i brak stronicowanego KV |
| **Długie wspólne prefiksy** (system prompt + schematy narzędzi) | globalny prefix cache (vLLM) lub drzewo radix (SGLang) działa między zapytaniami; w llama.cpp reuse jest per slot | `--cache-ram`, `--cache-idle-slots`, `--ctx-checkpoints` w llama.cpp pokrywają część potrzeb — sprawdź to najpierw |
| **Sprzęt z FP8** | jądra FP8 i FP4 są w centrum uwagi tych silników | vLLM dopuszcza FP8 na RDNA4 w kodzie; wydajności nie mierzono |
| **Checkpointy nie-GGUF** (HF, safetensors, kwanty z kalibracją) | to natywny format; nowe modele pojawiają się tu najszybciej *(niezweryfikowane)* | to jedyny scenariusz, w którym kwantyzacje GGUF przestają być dla ciebie paliwem |
| Embeddingi/rerank jako usługi obok czatu | endpointy w jednym serwerze (vLLM) | |

Zobacz też gotowe pomysły do skopiowania do własnego orkiestratora: kieruj zapytania z tym samym prefiksem do tego samego backendu (wzorzec z polityki `cache_aware` w bramce SGLang); `cache_salt` w vLLM jako sposób izolacji między dzierżawcami/agentami; wzorzec „scheduler o jeden batch do przodu”; rejestr parserów narzędzi/rozumowania per rodzina modeli oddzielony od silnika; endpointy `sleep`/`pause`/`resume` i hot-swap LoRA jako prymitywy współdzielenia GPU.

### 8.2 Dlaczego eksperyment nie jest dziś wart zachodu na gfx1201 — chyba że …

Powody, które wynikają z samych notatek:

1. **Model referencyjny.** Konfiguracja referencyjna używa 284B MoE w UD-IQ3_XXS. Aby uruchomić go w vLLM, potrzebowałbyś checkpointu w formacie HF. Sama arytmetyka wag: 284 mld parametrów po 0,5 B w INT4 to ≈142 GB, a w FP8 ≈284 GB (*moje wyliczenie*, bez KV i narzutów); cztery karty to 4 × 32 = 128 GB. **Ten model w HF-INT4 nie zmieściłby się w VRAM** nawet bez KV. (vLLM ma wprawdzie kwantyzację `deepseek_v4_fp8` w rejestrze i parsery DeepSeek V4, ale rozmiar wag przesądza sprawę.) Twoja kwantyzacja IQ3 to właśnie to, czego silniki serwerowe nie robią dobrze (§3.4).
2. **GGUF w vLLM** jest wtyczką, „highly experimental and under-optimized”; na liście kwantyzacji ROCm go nie ma.
3. **SGLang** nie ma gfx1201 wśród celów (§4.6). Wróć, gdy `setup_rocm.py` wymieni gfx12xx.
4. **Pre-alokacja vLLM** (0,92) koliduje z llama-swap na tych samych kartach.
5. **TP na PCIe:** brak własnego all-reduce poza MI300/MI350, RCCL po PCIe; skalowanie ograniczone przepustowością *(niezweryfikowane)*.
6. **Brak niezależnych pomiarów** vLLM na RDNA4 — w notatkach nie ma ani jednego.

**Kiedy warto (X):** gdy spełnione są **jednocześnie** trzy warunki:

- obciążenie to **wielu równoległych agentów lub zapytań ze wspólnymi długimi prefiksami**, a nie jedna interaktywna rozmowa;
- docelowy **model istnieje w formacie HF (FP8 lub INT4 GPTQ/AWQ) i mieści się w 128 GB z zapasem na pulę KV** — czyli jest znacznie mniejszy niż twoje 284B;
- **jednodniowy test na odizolowanych kartach** (lista z §3.7) potwierdzi, że backend uwagi, jądro W4A16/FP8 i `-tp=4` startują stabilnie na gfx1201 i że wynik zmierzony `vllm bench` przy *twojej* liczbie zapytań bije konfigurację llama.cpp.

Jeśli którykolwiek z trzech warunków nie jest spełniony, llama.cpp + llama-swap pozostaje właściwym wyborem dla tej maszyny. Ostatnie zdanie notatek brzmi: *„On R9700s, vLLM is the only engine here with documented RDNA4 support; test it before betting on it.”*

### 8.3 Co zabrać ze sobą, nawet nie uruchamiając vLLM

- **Zrozumienie kosztu** — dlaczego aplikacje agentowe z wieloma równoległymi wywołaniami zachowują się inaczej niż rozmowa: wszystko sprowadza się do tego, ile sekwencji mieści się w jednym kroku i czy prefiks przeżyje.
- **Ustawienia llama.cpp, które realizują te same idee** (rozdz. 04): `--parallel` i stabilny `id_slot`, `--cache-ram`, `--ctx-checkpoints`.
- **Ostrożność z telemetrią**: przy każdym narzędziu serwerowym ustaw opt-out na wejściu (vLLM i TRT-LLM wysyłają domyślnie).
- **Rozeznanie rynku:** trzy zespoły open source (vLLM, SGLang, LMCache) wypuściły w ciągu ok. roku firmy (Inferact, RadixArk, Tensormesh), a Modular został przejęty przez Qualcomm — to nie wpływa na twoją decyzję techniczną, ale zmienia, kto określa kierunek tych projektów. Kwoty finansowania są w notatkach jednoźródłowe (Inferact: 150 mln USD z nagłówka firmy i Wikipedii; RadixArk: wycena 400 mln USD tylko z prasy), więc szczegóły i tagi są w [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

Dalsze rozdziały: porównanie wszystkich runtime’ów i wybór — [`09-POROWNANIE-I-WYBOR.md`](09-POROWNANIE-I-WYBOR.md); Apple i MLX — [`07-APPLE-MLX-OMLX-I-DS4.md`](07-APPLE-MLX-OMLX-I-DS4.md); specjaliści (m.in. KTransformers, ścieżki hybrydowe CPU+GPU dla dużych MoE) — [`08-SPECJALISCI-KTRANSFORMERS-I-INNE.md`](08-SPECJALISCI-KTRANSFORMERS-I-INNE.md).
