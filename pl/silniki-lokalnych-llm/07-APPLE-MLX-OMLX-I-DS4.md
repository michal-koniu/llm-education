# 07 · Apple Silicon i silniki jednego modelu: MLX, mlx-lm, oMLX, ds4, exo

## Po co ten rozdział

Do tej pory (rozdziały 04–06) mówiliśmy o silnikach, które próbują obsłużyć **każdy** model na **każdym** sprzęcie: llama.cpp, Ollama, vLLM, SGLang. Ten rozdział jest o drugim biegunie: o silnikach, które świadomie rezygnują z uniwersalności — albo na rzecz **jednej platformy** (Apple Silicon), albo nawet **jednej rodziny modeli** (ds4/DwarfStar).

Po przeczytaniu będziesz umiał:

- wyjaśnić, dlaczego na Macu o szybkości generowania decyduje **przepustowość pamięci**, a nie „moc GPU", i policzyć sufit tok/s dla dowolnego układu M-serii;
- rozróżnić cztery warstwy: **MLX** (framework tablicowy), **mlx-lm** (biblioteka LLM na MLX), **oMLX** (serwer na mlx-lm) i **exo** (warstwa klastrowa nad MLX);
- powiedzieć, co znaczy „oQ4e", jak działa dwupoziomowy (RAM + SSD) cache KV w oMLX i dlaczego agenci kodujący go potrzebują;
- zrozumieć **argument inżynierski za silnikiem dla jednego modelu** (ds4) i ocenić, co z niego da się przenieść do llama.cpp;
- uczciwie ocenić, co z tego wszystkiego działa na twoim rigu 4× R9700 (gfx1201) — **spoiler: prawie nic, poza pomysłami**.

> ⚠️ **Niczego tu nie uruchamiałem.** Cały rozdział to *desk research* oraz czytanie kodu źródłowego (klony repozytoriów z 19.10.2026) i API GitHuba. Żadnego z opisywanych silników nie testowałem ani nie mierzyłem. Wszystkie liczby wydajnościowe pochodzą od projektów lub osób trzecich i są oznaczone; liczby „moje wyliczenie" to arytmetyka na zweryfikowanych danych wejściowych, a nie pomiar. Stan na **19 października 2026** — ds4 i oMLX zmieniają się codziennie.

> ⚠️ **Twój rig (4× Radeon AI PRO R9700, gfx1201, ROCm):** MLX nie ma backendu HIP/ROCm, oMLX działa tylko na Apple Silicon, exo na Linuksie działa wyłącznie na CPU, a ds4 ma ROCm tylko dla gfx1151 (Strix Halo). **Nic z tego rozdziału nie uruchomisz na rigu.** Rozdział jest dla twoich Maców i dla pomysłów, które przenosisz do llama.cpp.

## Spis treści

1. [Dlaczego Apple Silicon jest inny](#1-dlaczego-apple-silicon-jest-inny) — pamięć współdzielona, przepustowość, tabela sufitów
2. [MLX — framework tablicowy](#2-mlx--framework-tablicowy)
3. [mlx-lm — warstwa LLM](#3-mlx-lm--warstwa-llm)
4. [oMLX w głąb](#4-omlx-w-głąb) — ciągłe batchowanie, cache stronicowany z warstwą SSD, oQ, MTP
5. [ds4 / DwarfStar w głąb](#5-ds4--dwarfstar-w-głąb) — silnik jednego modelu
6. [Własny stos Apple](#6-własny-stos-apple-foundation-models-core-ml-core-ai-ane)
7. [exo — klaster Maców](#7-exo--klaster-maców)
8. [Co z tego dla mnie](#8-co-z-tego-dla-mnie)

Słowniczek tego rozdziału (patrz też `02-JAK-DZIALA-INFERENCJA.md`): *szybkość generowania (tok/s)*, *prefill* (czytanie promptu), *dekodowanie*, *pamięć podręczna KV (KV cache)*, *kwantyzacja*, *eksperci (MoE)*, *ciągłe batchowanie (continuous batching)*, *podział tensorowy (tensor parallel)*, *rurociąg (pipeline parallel)*.

---

## 1. Dlaczego Apple Silicon jest inny

### 1.1 Jedna pamięć dla CPU i GPU

W twoim rigu są dwa światy pamięci: RAM systemowy (DDR5, szeroki, ale wolny) i VRAM kart (GDDR6, 32 GB na kartę, szybki). Wagi, które się nie mieszczą w VRAM, trzeba „wylewać" do RAM-u i przesyłać przez PCIe — i tu właśnie zwykle kończy się szybkość.

W układach Apple Silicon (M1…M5) CPU, GPU i Neural Engine współdzielą **jedną pulę pamięci zunifikowanej**. Nie ma kopiowania „z hosta na kartę": ten sam bufor widzą oba procesory. Z punktu widzenia LLM-a to znaczy, że **cała pamięć maszyny jest „VRAM-em"** (z zastrzeżeniem limitu pamięci „wired" dla GPU — ds4 zaleca przy 128 GB `sudo sysctl iogpu.wired_limit_mb=120000`, patrz §5.9).

Analogia: rig to dwa magazyny połączone wąskim mostem; Mac to jeden magazyn z szerokimi drzwiami. Precyzyjniej: Mac nie jest szybszy w arytmetyce niż R9700, tylko **nie ma mostu**, a pamięć jest duża (64–512 GB w konfiguracjach, które wymieniają notatki).

### 1.2 Przepustowość = szybkość generowania

Z rozdziału 02 pamiętasz: dekodowanie to czytanie wszystkich *aktywnych* wag raz na token. Zatem

```
tok/s (sufit) ≈ przepustowość pamięci / (aktywne parametry × bity na wagę / 8)
```

To jest **górna granica**. Realne silniki osiągają zwykle 60–80% tego *(niezweryfikowane — reguła inżynierska, nie pomiar z tej ankiety)*. Dlatego **liczba GB/s układu jest prawdziwą specyfikacją Maca do LLM-ów**, a nie liczba rdzeni GPU.

### 1.3 Przepustowość układów — co jest sprawdzone

| Układ | GB/s | Źródło |
|---|---:|---|
| M4 Pro | 273 | Wikipedia *(źródło zewnętrzne)* |
| M4 Max (wersja 32-rdz. GPU / pełna 40-rdz.) | 410 / **546** | Wikipedia *(źródło zewnętrzne)* |
| M3 Max (14 / 16 rdz.) | 300 / 400 | Wikipedia *(źródło zewnętrzne)* |
| M3 Ultra | **819,3** | Wikipedia *(źródło zewnętrzne)*; wpis Apple ML „819 GB/s" *(dane firmy)* |
| M5 (bazowy) | 153 (153,6) | apple.com, specyfikacja MacBook Pro *(dane firmy)*; Wikipedia *(źródło zewnętrzne)* |
| M5 Pro | 307 | apple.com *(dane firmy)* |
| M5 Max (32 / 40-rdz. GPU) | 460 / **614** | apple.com, MacBook Pro i Mac Studio *(dane firmy)* |
| **M5 Ultra** (Mac Studio, sierpień 2026; 256/512 GB) | **~1,2 TB/s** (1 228,8) | apple.com, Mac Studio *(dane firmy)*; Wikipedia *(źródło zewnętrzne)* |

Wartość dla M5 Ultra podaję tak, jak ją notują źródła: to liczba ze strony specyfikacji Apple, potwierdzona przez Wikipedię; nie mam pomiaru, który by ją sprawdzał.

### 1.4 Tabela sufitów (moje wyliczenie)

Założenia *(moje wyliczenie)*: wagi 4-bitowe liczone jako **4,5 bita na wagę łącznie ze skalami grup** (afiniczna kwantyzacja grupowa 64 lub coś w rodzaju Q4_K); model gęsty 30B ⇒ 16,9 GB na token; MoE z 13B aktywnych ⇒ 7,3 GB na token (pozostali eksperci stoją, kontekst krótki, batch 1). Kolumna „@70%" to sufit × 0,7 — typowa sprawność dobrze dostrojonego kodu *(niezweryfikowane)*.

| Układ | GB/s | Gęsty 30B 4-bit: sufit / @70% | MoE 13B aktywnych 4-bit: sufit / @70% |
|---|---:|---:|---:|
| M5 | 153,6 | 9,1 / 6,4 | 21,0 / 14,7 |
| M4 Pro | 273 | 16,2 / 11,3 | 37,3 / 26,1 |
| M5 Pro | 307 | 18,2 / 12,7 | 42,0 / 29,4 |
| M4 Max (32 rdz.) | 410 | 24,3 / 17,0 | 56,1 / 39,2 |
| M5 Max (32 rdz. GPU) | 460 | 27,3 / 19,1 | 62,9 / 44,0 |
| M4 Max (pełny) | 546 | 32,4 / 22,6 | 74,7 / 52,3 |
| M5 Max (40 rdz. GPU) | 614 | 36,4 / 25,5 | 84,0 / 58,8 |
| M3 Ultra | 819,3 | 48,6 / 34,0 | 112 / 78,4 |
| M5 Ultra | 1 228,8 | 72,8 / 51,0 | 168 / 117,6 |

**Test zdrowego rozsądku na pomiarze** *(dane projektu + moje wyliczenie)*: ds4 na M5 Max 128 GB z DeepSeek V4 Flash w kwantyzacji Q2 (13B aktywnych) mierzy **39,35 tok/s** przy kontekście 2K. Przy *średnich* 2,45 bita na wagę (patrz §5.4) wzór daje ~154 tok/s przy 614 GB/s — pomiar to ok. 26% sufitu. Wyjaśnienie (moje, niezweryfikowane): tensory uwagi, ekspertów współdzielonych i wyjścia są w Q8/F16, nie w 2 bitach, więc realnie na token czytasz ekwiwalent ok. 15,6 GB (614 / 39,35), a nie ~4 GB. Notatki nie podają też, czy plik CSV pochodzi z M5 Max o 40 czy 32 rdzeniach GPU; przy 460 GB/s proporcja wyszłaby ~34%.

**Wniosek:** wzór to *górna granica*; kwantyzacja niejednorodna i nieuwzględniony ruch pamięci spychają MoE znacznie niżej, modele gęste — bliżej sufitu. Drugi test: ta sama proporcja Spark/M5 Max. DGX Spark ma 273 GB/s *(niezweryfikowane — z pamięci autora notatek)*, a ds4 mierzy tam 18,05 tok/s wobec 39,35 na M5 Max; stosunek 0,46 vs. stosunek przepustowości 0,44 *(moje wyliczenie)*. Dekodowanie rzeczywiście skaluje się z GB/s.

Dla porównania z twoim rigiem: jedna R9700 ma ok. 640 GB/s *(niezweryfikowane — z pamięci, sprawdź w specyfikacji AMD)*. To klasa przepustowości M5 Max, tyle że razy cztery karty — i z tą różnicą, że karty mają osobne pule pamięci.

### 1.5 Prefill jest inny niż dekodowanie

Dekodowanie jest ograniczone pamięcią; **prefill** (czytanie promptu) jest ograniczony obliczeniami. Na M5 Apple dołożył „Neural Accelerator" w każdym rdzeniu GPU (wg Apple ok. 4× większa szczytowa moc obliczeniowa AI niż M4) *(dane firmy / źródło zewnętrzne)* — to pomaga prefillowi i czasowi do pierwszego tokenu, **nie** dekodowaniu, bo przepustowość rośnie osobno. MLX ma pod to osobną ścieżkę (§2.4).

---

## 2. MLX — framework tablicowy

**Warstwa:** biblioteka obliczeń numerycznych (jak NumPy + PyTorch w jednym), nie silnik LLM. To na niej stoją mlx-lm, oMLX, exo, vllm-metal, silnik MLX w LM Studio i runner MLX w Ollamie.

> ⚠️ **MLX nie ma backendu HIP/ROCm.** Sprawdziłem listę katalogów `mlx/backend/`: są `metal`, `cuda`, `cpu`, `common` — brak `hip`. MLX **nie uruchomi się na twoich R9700**. Na Linuksie możesz mieć MLX na CPU lub na CUDA (`pip install mlx[cuda]`), ale to nie jest twoja platforma.

### 2.1 Tożsamość

- Repozytorium `ml-explore/mlx`, licencja **MIT**, C++ z wiązaniami Pythona, Swifta i C; utworzone 2023-11-28; **28 845 gwiazdek**, 2 353 forków; ostatnie wydanie **v0.32.4 (2026-10-14)**. Pokrewne repozytoria: `mlx-swift`, `mlx-swift-lm`, `mlx-c`, `mlx-lm`.
- Opiekun: „Apple machine learning research". Cytowanie w README wymienia czterech twórców: Awni Hannun, Jagrit Digani, Angelos Katharopoulos, Ronan Collobert.

### 2.2 Idee

- **Leniwe tablice (*lazy evaluation*).** Operacja na tablicy nie liczy wyniku — buduje węzeł grafu. Obliczenie następuje dopiero przy `mx.eval` (albo gdy czegoś potrzebujesz, np. wydruku). Dzięki temu framework widzi większy fragment grafu i może go zoptymalizować.
- **Pamięć zunifikowana.** Tablice żyją w pamięci współdzielonej, więc ta sama tablica może być argumentem operacji na CPU i na GPU **bez kopiowania**.
- **Dynamiczna konstrukcja grafu.** Zmiana kształtów nie wywołuje wolnej rekompilacji (README).
- **Transformacje funkcji:** `grad`, `vmap`, `compile` (plik `compile.cpp` — fuzja grafu, opcja „shapeless compile"), eksport grafu funkcji do pliku dla konsumenta w C++ (`export.cpp`).
- **Strumienie** (`scheduler.cpp`) i szybkie operacje `mx.fast`: `rms_norm`, `layer_norm`, `rope`, `scaled_dot_product_attention` oraz **własne kernele użytkownika**: `metal_kernel`, `cuda_kernel`, `precompiled_cuda_kernel`. Kod modeli w mlx-lm wywołuje właśnie te operacje.

### 2.3 Rozmiar i układ kodu (klon z 19.10.2026)

| Katalog | Linie | Co tam jest |
|---|---:|---|
| `mlx/` łącznie | 155 825 (633 plików) | rdzeń |
| `mlx/backend/metal` | 61 486 | kernele `.metal` (uwaga „steel", GEMM „steel", skwantyzowane, `gather_mm`, Hadamard, `gated_delta_update` dla liniowej uwagi w stylu Qwen3.5, FFT) |
| `mlx/backend/cuda` | 30 830 | cuBLAS/cuDNN/CUTLASS, kernele `.cu`; `MLX_CUDA_ARCHITECTURES` domyślnie natywna |
| `mlx/backend/cpu` | 13 410 | |
| `mlx/distributed` | 8 091 | `jaccl` 4 958, `ring` 879, `mpi` 579, `nccl` 506 |
| `python/src` | 17 432 | wiązania |

Kwantyzacja w rdzeniu: afiniczna grupowa (2–8 bitów, grupy 32/64/128) oraz tryby MXFP4 / NVFP4 / MXFP8 (`mx.quantize(..., mode=...)`).

### 2.4 Ścieżka „NAX" (M5)

`is_nax_available()` w `mlx/backend/metal/device.cpp:978` wymaga macOS ≥ 26.2 i odpowiednio nowej generacji GPU. Są dla niej osobne kernele: `steel_gemm_fused_nax`, `fp_quantized_nax`, `gated_delta_update_nax`. To jest ta część MLX, która korzysta z Neural Accelerator z §1.5.

### 2.5 Backendy rozproszone

Z `docs/src/usage/distributed.rst`:

| Backend | Opis z dokumentacji | Uwagi |
|---|---|---|
| `mpi` | „full featured and mature" | |
| `ring` | all-reduce i all-gather przez TCP; „zwykle szybszy niż MPI" | |
| **`jaccl`** | „Low latency communication with RDMA over thunderbolt. Necessary for things like tensor parallelism" | nazwa = „Jack and Angelos' Collective Communication Library"; **tylko topologia pełnej siatki (*fully-connected mesh*)**; RDMA włącza się z trybu Recovery komendą `rdma_ctl enable`; wymaga macOS ≥ 26.2 i Thunderbolt 5 |
| `nccl` | dla backendu CUDA | |

API: `mx.distributed.init()`, `all_sum`, `all_gather`, `send`/`recv`; przy grupie o rozmiarze 1 operacje są pustymi wywołaniami; pomocnik `mlx.launch`. Dokumentacja JACCL dziękuje Jackowi Beasleyowi, który „led the development of RDMA over Thunderbolt at Apple".

**Konsekwencja praktyczna:** pełna siatka oznacza, że 4 maszyny wymagają **6 kabli** (n(n−1)/2), a każda dodatkowa maszyna dokłada kabel do każdej poprzedniej. To realne ograniczenie projektowania klastra Maców (wróć do tego w §7).

### 2.6 Liczby od Apple (z zastrzeżeniem)

Wpis Apple ML Research z 2026-10-15 „Local and Distributed Large LLM Inference with MLX and RDMA on Mac Studio" podaje według mojego źródła m.in.: 4× M5 Ultra po Thunderbolt 5/JACCL, podział tensorowy, model „Muse Spark Open" (816B łącznie / 42B aktywnych, NVFP4) — **36,73 tok/s** przy kontekście 65 536, TTFT 4,8 s; dwa kable na łącze zmniejszają TTFT z ok. 50,5 s do 40,6 s; szczytowy pobór ok. 300 W (M5 Ultra) wobec ok. 200 W (M3 Ultra); gęste modele skalują się między maszynami lepiej niż MoE *(dane firmy)*.

⚠️ **Zastrzeżenie:** notatki zawierają tylko streszczenie tej strony wykonane przez mniejszy model; nie czytałem surowego tekstu wpisu. Nazwy modeli i parametry są wiarygodne, ale **zweryfikuj je u źródła, zanim je zacytujesz**.

### 2.7 Kto za tym stoi

MLX jest projektem pierwszej strony Apple: płacą zatrudnieni inżynierowie, licencja MIT, brak fundacji. Awni Hannun (najwięcej commitów: 718) według własnego profilu GitHub pracuje teraz w Anthropic i „co-created MLX at Apple"; jego ostatnie commity do mlx i mlx-lm pochodzą z lutego 2026. Projekt przeżył odejście założyciela: aktywni są inżynierowie z firmą „Apple" w profilu (zcbenz — 304 commity, angeloskath — 235, jagrit06 — 58). Apple nie wypuściło — o ile zweryfikowałem — własnego *produktu* zbudowanego na MLX *(niezweryfikowane)*. Pełny obraz: [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

> **Sprawdź sam #1 — czy MLX ma backend AMD?**
> ```bash
> gh api repos/ml-explore/mlx/contents/mlx/backend --jq '.[].name'
> ```
> Powinieneś zobaczyć `common`, `cpu`, `cuda`, `metal` (i ewentualnie katalogi pomocnicze) — **bez** `hip`/`rocm`. *(Dokładnej postaci tego polecenia nie uruchamiałem; listę katalogów odczytałem z klonu.)*

---

## 3. mlx-lm — warstwa LLM

**Warstwa:** biblioteka i narzędzia wiersza poleceń dla modeli językowych na MLX: zoo modeli, konwerter i kwantyzatory, generowanie, LoRA, prosty serwer HTTP.

### 3.1 Tożsamość

Repozytorium `ml-explore/mlx-lm`, MIT, Python; powstało 2025-03-11 (wydzielone z `mlx-examples`); **7 405 gwiazdek**, 1 136 forków; najnowsze **v0.32.2 (2026-10-16)** — trzy wydania w dwa dni. Największe wkłady: awni 291 commitów, angeloskath 63, Goekdeniz-Guelmez 56, mzbac 38, kernelpool 33, ivanfioravanti 26… Repozytorium ma pliki `CLAUDE.md` i `AGENTS.md`.

Rozmiar (klon): `mlx_lm/` ok. 59,6 tys. linii Pythona; `models/` — 43,2 tys. linii w **137 plikach**. Największe pliki: `generate.py` 2 184, `server.py` 2 094, `models/cache.py` 1 741.

### 3.2 Zoo modeli

137 plików architektur: rodziny llama, qwen3 / 3.5 / 3.8 (w tym `qwen3_next`, `gated_delta`), deepseek v2 / v3 / v3.2 / **v4.1**, glm4 i `glm_moe_dsa`, kimi (k25, k3, liniowe), gpt_oss, gemma 3 / 3n / 4, mistral3/4, minimax, nemotron_h, mamba / mamba2 / rwkv7 / jamba (SSM i hybrydy), bitnet i wiele innych. To daje mlx-lm **najszerszą pokrywę modeli „od dnia zero" na Macu**.

### 3.3 Klasy cache KV (`models/cache.py`)

| Klasa | Do czego |
|---|---|
| `KVCache`, `ConcatenateKVCache` | zwykły cache |
| `RotatingKVCache` | okno przesuwne (sliding window) |
| `QuantizedKVCache` | `--kv-bits`, `--kv-group-size`, `--quantized-kv-start` (domyślnie 5000) |
| `ArraysCache` | stan SSM / uwagi liniowej |
| `ChunkedKVCache`, `CacheList` | kawałkowanie, listy cache |
| `BatchKVCache`, `BatchRotatingKVCache` | batchowanie |
| `PromptTrie`, **`LRUPromptCache`** | ponowne użycie prefiksu promptu w serwerze |

Cache promptu można zapisać na dysk i wczytać (`save_prompt_cache` / `load_prompt_cache`, safetensors; używa tego `mlx_lm.cache_prompt`). **Serwer natomiast ma tylko LRU w RAM-ie** — poziomu SSD nie ma; dopiero oMLX go dokłada (§4).

### 3.4 Generowanie

`generate.py`: `generate_step`, `speculative_generate_step` (dekodowanie spekulatywne z modelem pomocniczym — flagi serwera `--draft-model`, `--num-draft-tokens`, domyślnie 3), `stream_generate`, **`BatchGenerator`** z `PromptProcessingBatch` / `GenerationBatch` (ciągłe batchowanie, automaty zatrzymania), `batch_generate`. MTP w `generate.py` **nie ma**; głowice MTP występują tylko wewnątrz niektórych plików modeli (np. `deepseek_v41`, `kimi_k3`, `mimo`).

### 3.5 Serwer `mlx_lm.server`

- Endpointy: `/v1/completions`, `/v1/chat/completions`, `/v1/models`, `/health`. **Brak endpointu Anthropic, brak embeddingów.**
- Flagi: `--decode-concurrency`, `--prompt-concurrency`, `--prefill-step-size`, `--prompt-cache-size`, `--prompt-cache-bytes`, `--kv-bits`, `--draft-model`, `--pipeline` (rurociąg między maszynami), `--chat-template-args`.
- Dokumentacja (`SERVER.md`): „nie zalecany do produkcji, bo ma tylko podstawowe kontrole bezpieczeństwa"; **skwantyzowany cache KV wyłącza batchowanie** (żądania obsługiwane po jednym, gdy ustawisz `--kv-bits`).
- Parsery wywołań narzędzi w `tool_parsers/` (qwen3_coder, glm47, kimi_k2/k3, mistral, minimax_m2, gemma4, pythonic…).

### 3.6 Kwantyzacja

`mlx_lm.convert -q`: kwantyzacja afiniczna (domyślnie 4 bity, grupa 64), `--q-mode {affine, mxfp4, nvfp4, mxfp8}`; metody uczone w `quant/`: **DWQ** (destylacja — dostraja skale i biasy względem nieskwantyzowanego nauczyciela), **AWQ**, **GPTQ**, **kwantyzacja dynamiczna** (wrażliwość per warstwa → mieszane bity). Dokumentuje je `LEARNED_QUANTS.md`. Do tego `mlx_lm.lora`/`fuse`, eksport `gguf.py`, `evaluate`, `perplexity`, `benchmark`.

Porównaj z rozdziałem 03: DWQ/AWQ/GPTQ to „kwantyzacja z nauką", imatrix w llama.cpp to „kwantyzacja z ważeniem błędu" — idee pokrewne, formaty niezgodne.

### 3.7 mlx-community

De facto centrum skonwertowanych modeli na Hugging Face: wg API z 19.10.2026 **5 753 modele, 5 963 członków, 17 847 obserwujących**, `isVerified: false`. To otwarta organizacja społecznościowa, **nie** organizacja Apple. Kto ją administruje — nie ustaliłem *(niezweryfikowane)*.

### 3.8 Ocena

Plusy: najszersza pokrywa modeli, referencja dla formatów kwantyzacji na Macu. Minusy: serwer podstawowy (bez Anthropic, uwierzytelniania, menedżera wielu modeli); skwantyzowany KV nie współgra z batchowaniem; brak stronicowania KV i poziomu SSD.

---

## 4. oMLX w głąb

**Warstwa:** serwer inferencji w Pythonie/FastAPI nad mlx-lm i mlx-vlm, tylko dla Apple Silicon: ciągłe batchowanie, **stronicowany cache KV z warstwą gorącą (RAM) i zimną (SSD)**, zarządzanie wieloma modelami, panel administracyjny, natywna aplikacja SwiftUI w pasku menu, własny kwantyzator (oQ), dekodowanie spekulatywne.

### 4.1 Tożsamość

- `jundot/omlx`, **Apache-2.0**; Python 3.11–3.13 plus aplikacja Swift, panel w JS i kernele Metal/C++. Utworzone **2026-02-13**; najnowsze **v0.7.1rc1 (2026-10-15)**, wydania co tydzień (ponad 100 wydań w 8 miesięcy); **3 353 commity**; **22 936 gwiazdek**, 2 171 forków; ok. 594 otwarte zgłoszenia i PR-y.
- macOS ≥ 15 (Sequoia), tylko Apple Silicon. Dystrybucja: `.dmg` (wersje dla macOS 15 i dla 26/27), tap Homebrew `jundot/omlx`, koła pip (universal2), źródła.
- Pochodzenie: „oMLX started from vllm-mlx v0.1.0 and evolved significantly" (README; vllm-mlx = `waybarrios/vllm-mlx`, 1 626 gwiazdek).

### 4.2 Po co powstał

Cytat z README: autor nie chciał wybierać między wygodą a kontrolą — chciał przypinać na stałe w pamięci codzienne modele, automatycznie podmieniać cięższe na żądanie, ustawiać limity kontekstu, wszystko z paska menu, i trzymać cache KV „w gorącej warstwie w pamięci i zimnej na SSD", żeby lokalne LLM-y były praktyczne do pracy z narzędziami takimi jak Claude Code. Czyli: **Mac power-usera, który uruchamia agentów kodujących**. Nie: Linux, CUDA, AMD.

### 4.3 Funkcje

- **Modele:** LLM (to, co załaduje mlx-lm), VLM (mlx-vlm: Qwen3.5/3.6/3.8, GLM-4V, Pixtral…), OCR (DeepSeek-OCR, DOTS-OCR, GLM-OCR), embeddingi (BERT, BGE-M3, ModernBERT, EmbeddingGemma), rerankery, modele „decyzyjne", silniki STT/TTS/STS.
- **API:** `/v1/chat/completions`, `/v1/completions`, **`/v1/messages` (Anthropic)**, `/v1/embeddings`, `/v1/rerank`, `/v1/systemone`, `/v1/models`, `/tokenize`, `/detokenize` w stylu vLLM; postęp prefillu w stylu llama.cpp (`return_progress`); wywołania narzędzi rozpoznawane automatycznie (Qwen/Llama JSON, XML Qwen3.5, Gemma, GLM, MiniMax, Mistral, Kimi, Longcat); klient MCP (`mcp.json`); wyjście ograniczone gramatyką (`omlx[grammar]`); wbudowane wyszukiwanie w sieci (opcjonalne). Strojenie pod Claude Code: serwer zgłasza realne okno kontekstu (żeby auto-compact działał) i wysyła SSE keep-alive podczas długiego prefillu.
- **Zarządzanie:** wyrzucanie modeli według LRU, ręczne ładowanie/zwalnianie, **przypinanie (*pinning*)**, **TTL per model**, `ProcessMemoryEnforcer` (domyślny limit = RAM systemu − 8 GB), ustawienia i „profile" per model wystawiane jako identyfikatory `model:profile`, pobieranie z HF, jednoklikowe integracje (OpenClaw, OpenCode, Codex, Hermes Agent, Copilot, Pi, Mistral Vibe), narzędzie benchmarkowe. **Klucz API jest wymagany przy każdym wiązaniu poza loopbackiem.**
- **Zewnętrzny silnik:** niektóre checkpointy Qwen obsługuje przez **Splash** (`incoai/splash`, osobny silnik Metal na Apache-2.0, 1 557 gwiazdek) w osobnym procesie.

### 4.4 Architektura (zweryfikowana w kodzie)

```
 żądanie HTTP (OpenAI / Anthropic / embeddings / rerank)
        │
        ▼
  FastAPI server ──► EnginePool
                       ├─ BatchedEngine   (LLM)
                       ├─ VLMEngine
                       ├─ EmbeddingEngine / RerankerEngine / DecisionEngine
                       ▼
              ProcessMemoryEnforcer  (limit RAM; LRU / TTL / pin)
                       ▼
                  Scheduler  (FCFS, konfigurowalna współbieżność)
                       ▼
        mlx-lm BatchGenerator  ◄──── tokeny: ciągłe batchowanie
                       ▼
        ┌─────────────── stos cache ───────────────┐
        │ PagedCacheManager  (bloki, copy-on-write,│
        │                     współdzielenie prefiksów)
        │ hot cache  (RAM, write-back)             │
        │ PagedSSDCacheManager (SSD, bloki safetensors)
        └───────────────────────────────────────────┘
```

**Scheduler** (`omlx/scheduler.py`, 16 621 linii; klasa `Scheduler` od linii 2105; `add_request` ~10667, `_schedule_waiting` ~12592, `_process_batch_responses` ~13439, `step()` ~15061): kopiuje projekt „waiting/running" z vLLM, ale **delegację batchowania na poziomie tokenów zostawia `BatchGenerator` z mlx-lm** („the key insight is that mlx-lm's BatchGenerator already implements…"). Dokłada: szacunki przyjęcia żądania, plany prefillu w kawałkach (*chunked prefill*), obsługę przerwań, dopasowanie sekwencji stopu świadome rozumowania (*reasoning*), migawki na granicach dla hybrydowych cache (SSM/GDN) oraz dekodowanie MTP dla VLM, które **omija** `BatchGenerator` dla kwalifikujących się żądań.

**Cache** (`omlx/cache/` ≈ 20 tys. linii): `prefix_cache.py` 5 783; `paged_ssd_cache.py` 5 639 (asynchroniczny zapis z kolejką oczekujących zapisów w RAM-ie ograniczoną do 10%/30% RAM-u hosta; podkatalogi z shardowaniem po hashu; zarządzanie rozmiarem LRU; **skan przy starcie, który ponownie wykorzystuje istniejące pliki — cache przeżywa restart**); `boundary_snapshot_store.py`, `type_handlers.py`, `vision_feature_cache.py`. Domyślny limit cache SSD `auto` = 50% (wolne miejsce + istniejące pliki cache).

### 4.5 Diagram: trzy poziomy cache

Idea „stronicowania" — pożyczona z vLLM: KV nie leży w jednym ciągłym buforze na sekwencję, tylko w **blokach**, które można współdzielić między żądaniami o wspólnym prefiksie i kopiować dopiero przy zapisie (*copy-on-write*). oMLX dokłada do tego **hierarchię nośników**:

```
  nowe żądanie (prompt = [system][historia agenta][nowa wiadomość])
        │  hash bloków prefiksu
        ▼
 ┌──────────────────────────────────────────────────────────────┐
 │ Poziom 1: bloki w pamięci GPU/zunifikowanej (PagedCacheManager)
 │   - najszybszy dostęp, współdzielenie prefiksów, COW         │
 └──────────────┬───────────────────────────────▲───────────────┘
        trafienie│                         wyparcie│ (LRU, presja RAM)
        ▼        │                               │ write-back
 ┌──────────────────────────────────────────────────────────────┐
 │ Poziom 2: „gorący" cache w RAM (write-back)                  │
 │   - kolejka zapisów oczekujących: ≤ 10% / 30% RAM hosta      │
 └──────────────┬───────────────────────────────▲───────────────┘
        trafienie│                    asynchroniczny zapis
        ▼        │                               │
 ┌──────────────────────────────────────────────────────────────┐
 │ Poziom 3: „zimny" cache na SSD (PagedSSDCacheManager)        │
 │   - bloki w formacie safetensors, zgodne z mlx-lm            │
 │   - podkatalogi shardowane hashem, wyrzucanie LRU            │
 │   - limit domyślny „auto" = 50% (wolny dysk + stary cache)   │
 │   - skan przy starcie ⇒ prefiksy ŻYJĄ po restarcie serwera   │
 └──────────────────────────────────────────────────────────────┘
        │  brak trafienia na żadnym poziomie
        ▼
   prefill tylko dla brakującego sufiksu → nowe bloki w dół hierarchii
```

*Diagram jest moją syntezą opisu README i kodu `omlx/cache/`; nazwy klas i liczby (10%/30%, 50%) pochodzą z notatek, układ strzałek upraszcza kod.*

**Dlaczego to ważne dla agenta?** Agent kodujący wysyła przy każdym kroku całą rosnącą historię. Bez ponownego użycia prefiksu każdy krok oznacza prefill od zera — a prefill długiej historii kosztuje na Macu sporo czasu (przy 65 tys. tokenów kontekstu Apple podaje TTFT rzędu kilku sekund na klastrze 4× M5 Ultra, §2.6). Z cache SSD prefill dotyczy tylko nowego ogona, nawet po wyłączeniu serwera lub po wyparciu modelu z pamięci.

### 4.6 Kompresja KV, kernele i łatki

- **Opcjonalna kompresja KV:** Affine4 / Affine8 (`docs/affine4.md`) z dekodowaniem uwagi na Metal TensorOps; w repozytorium jest też `turboquant_kv.py`.
- **Własne kernele natywne** (`omlx/custom_kernels/{attention, quant_matmul(+ane), lowbit, sparse_index, moe_staging}`, budowane toolchainem Metal z Xcode; DMG zawiera je prekompilowane). README: GLM-5.2, MiniMax M3 i Qwen3.5 *wymagają* tych kerneli; „fused DSA prefill is roughly 30x faster with the kernels (measured 845 vs ~29 tok/s on an M3 Ultra)" *(dane projektu)*.
- **Ok. 90 łatek** w `omlx/patches/` — monkey-patche warstw nad mlx-lm/mlx-vlm (Qwen3.5 GDN/MoE, DeepSeek V4/V4.1, GLM-DSA, MiniMax M3, Muse Spark, MiMo V2, „ragged decode", kernele weryfikacji…). To strategia wsparcia „od dnia zero" przez wendoryzację i łatanie — **w duchu zbliżona do ds4, ale na wierzchu uniwersalnej biblioteki**.
- **Odciążanie ekspertów MoE** (`docs/experimental/MoE_Expert_Offload.md`): trzymasz ułamek (5–95%) ekspertów każdej warstwy w gnieździe cache, resztę strumieniujesz z oryginalnych safetensors przez `pread` (12 wątków, ≤ 48 odczytów w locie). Wyniki „bit-identyczne"; przy gemma-4-26b-a4b 4-bit szczyt pamięci przy ładowaniu spada z 14,28 GB do 4,69 GB przy 25% rezydentnych *(dane projektu)*. To ten sam pomysł co strumieniowanie SSD w ds4 (§5.6), ale na ścieżce mlx-lm.

### 4.7 Dekodowanie spekulatywne (MTP, DFlash)

- **„Lightning MTP"** — natywne głowice MTP (*multi-token prediction*), z kernelami weryfikacji pożyczonymi z MTPLX.
- **DFlash** — szkicowanie blokowe typu *block-diffusion* (arXiv:2602.06036): model-szkic proponuje cały **blok** tokenów na podstawie stanów ukrytych zebranych z kilku warstw modelu docelowego; adaptacyjna głębokość weryfikacji; wzajemnie wykluczające się z MTP i z odciążaniem ekspertów; dla większości rodzin jeden wiersz, dla Qwen3.5–3.8 i GLM-5.3 — wiele wierszy równolegle.
- **SpecPrefill** (`omlx/specprefill`).

To ten sam kierunek, który znasz z `../przyspieszanie-generowania/README.md`: sprawdzić kilka tokenów naraz, bo koszt kroku to czytanie wag.

### 4.8 Eksperymenty

- **Prefill na dwóch ANE + GPU** dla Qwen3.5/3.6/3.8 na M3 Ultra przez **prywatne API AppleNeuralEngine**: dwie instancje ANE liczą kawałki INT8 bramek MLP, GPU resztę; stan rekurencyjny zostaje na GPU dla precyzji; domyślnie wyłączone (`docs/experimental/qwen35_ane_prefill.md`).
- **Klaster wielu Maców** — rurociąg po rangach przez Ring lub JACCL/RDMA z panelem (`omlx/cluster`).

### 4.9 oQ — własny kwantyzator i co znaczy „oQ4e"

`omlx/oq.py` (11 295 linii), `docs/oQ_Quantization.md`. Opis autora: „mixed-precision quantization combining GGUF K-quant layer-position strategy, unsloth Dynamic 2.0 selective non-quantization, and BnB MSE-optimal clipping". Poziomy: **oQ2, 2.5, 2.7, 3, 3.5, 4, 5, 6, 8**; przybliżone bity na wagę łącznie ze skalami (grupa 64): oQ4 ≈ 4,6–4,7; oQ3 ≈ 3,5–3,7; oQ2 ≈ 2,8–3,0; oQ8 ≈ 8,5.

Procedura:

1. Strumieniuj tensory z dysku.
2. **Zmierz wrażliwość każdej warstwy** na wbudowanej kalibracji (600 próbek wielojęzycznych / kodu / wywołań narzędzi; 128 × 256 tokenów).
3. Zaplanuj dodatkowe bity dla wrażliwych tensorów w ramach budżetu rozmiaru.
4. **Wariant „e" (*enhanced*, np. „oQ4e")**: dodatkowo zbierz **imatrix** (ok. 2 700 próbek; 128 × 512 tokenów; dla MoE próbkuj do 1 024 sekwencji, aż każdy ekspert dostanie dość tokenów) i zaokrąglaj każdą grupę, szukając skali/przesunięcia dających minimalny błąd *ważony ważnością* oraz dopasowanie ważonymi najmniejszymi kwadratami.
5. Zapisz **standardowe safetensors MLX** — wynik wczytuje zwykły mlx-lm/mlx-vlm.

**Zatem „oQ4e" = poziom oQ 4 (baza 4-bitowa) z ulepszonym zaokrąglaniem sterowanym imatrix**, np. `Qwen3.5-122B-A10B-oQ4e`. Przyrostek `-mtp` = zachowane głowice MTP; `-fp16` = skale w float16. Ochrona: osadzenia i głowica wyjściowa w 8 bitach, routery MoE w pełnej precyzji, bramki ekspertów współdzielonych w 8 bitach, enkodery wizji/audio, normy i parametry SSM nieskwantyzowane. Modele już skwantyzowane w MLX **nie mogą** być źródłem. DeepSeek V4.1 jest obsługiwany na poziomach oQ3/oQ4(e), w tym z 4-bitowym Engramem.

Jakość (pomiary projektu, *dane projektu*): Qwen3.5-9B (1 900 pytań MMLU/Winogrande/MBPP/GSM8K) — oryginał 76,53, oQ4e 77,05 (5,6 GB), oQ3e 73,79 (4,6 GB); Qwen3.6-35B-A3B — oryginał 82,68, oQ4e 83,05 (20 GB), oQ3e 82,68 (16 GB). Wcześniejsza tabela (1 600 pytań): jednolity 4-bit z mlx-lm 70,12 vs oQ4e 72,38 na Qwen3.5-9B. To pomiary autora, bez niezależnej replikacji; pamiętaj, że przy 1,9 tys. pytań różnice rzędu 0,5 pkt mieszczą się w szumie.

Pokrewieństwo z llama.cpp: „zmierz wrażliwość, potem rozdziel budżet bitów" to ta sama idea co imatrix + `--tensor-type` w llama.cpp — możesz ją odtworzyć na rigu (rozdział 03).

### 4.10 Porównanie z sąsiadami

| | oMLX | `mlx_lm.server` | silnik MLX w LM Studio | Ollama (Mac) | llama.cpp (Metal) | vllm-metal |
|---|---|---|---|---|---|---|
| Podstawa | BatchGenerator mlx-lm + własny cache stronicowany/SSD | własna | `lmstudio-ai/mlx-engine` (MIT, 1 189 gwiazdek) opakowujący mlx-lm/mlx-vlm | Go `mlxrunner/` (ok. 55 tys. linii) na mlx-c | ggml Metal | scheduler vLLM + menedżer bloków; warstwy mlx_lm |
| Ciągłe batchowanie | tak | tak (podstawowe) | zależne od aplikacji | przez `batch/` w mlxrunner *(niezweryfikowane głębokość)* | tak (sloty) | tak |
| Warstwa SSD dla KV | **tak** | nie (LRU w RAM) | nie | nie *(niezweryfikowane)* | zapis slotu na dysk (`/slots`) | nie *(niezweryfikowane)* |
| API Anthropic | tak | nie | nie *(niezweryfikowane)* | tak (katalog `anthropic/`) | tak | nie *(niezweryfikowane)* |
| UI | panel www + menu bar | brak | pełna aplikacja | ikona w tacce | web UI | brak |

Inni budujący na MLX: `vllm-project/vllm-metal` (Apache-2.0, 1 890 gwiazdek, utworzone 2025-12-12), `waybarrios/vllm-mlx` (przodek oMLX), `ddalcu/mlx-serve` (1 990; Zig + aplikacja Swift), `youssofal/mtplx` (2 605; natywne MTP na Macu — „125 tok/s in OpenCode on an M5 Max" *(dane projektu)*), `bstnxbt/dflash-mlx`, `Blaizzy/mlx-vlm` (5 639), `incoai/splash`.

### 4.11 Offline

Panel administracyjny ma zwendorowane wszystkie zależności CDN („fully offline"). Pobieranie z HF i aktualizacje są opcjonalne (`--hf-endpoint` pozwala użyć lustra); DMG ma auto-aktualizację w aplikacji, którą — jak zakładam — da się wyłączyć *(niezweryfikowane)*.

### 4.12 Kto za tym stoi

**Jun Kim (jundot)**, Seul. Według profilu GitHub: „Open-Source ML Engineer at Hugging Face | Creator of oMLX"; jest też publicznym członkiem organizacji `huggingface`. Z 3 353 commitów 2 110 to jego (ok. 63%). Na stronie omlx.ai i w repozytorium **nie ma informacji o sponsorach, cenniku ani donacjach** (brak `FUNDING.yml`); licencja Apache-2.0, bez płatnej wersji. **Czy Hugging Face finansuje lub sponsoruje oMLX — nie ustaliłem** *(niezweryfikowane)*; fakt zatrudnienia autora w HF to jedyne, co jest sprawdzone. Szczegóły: [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

### 4.13 Ocena

+ Jedyny sprawdzony serwer na Maca łączący: trwały cache KV na SSD, przypinanie i TTL wielu modeli, API OpenAI i Anthropic, kwantyzator i GUI. Rusza szybko.
− Jeden opiekun (63% commitów), duża powierzchnia łatek nad dwoma upstreamami, `scheduler.py` na 16,6 tys. linii; poleganie na prywatnych i eksperymentalnych ścieżkach (prywatne API ANE; własne kernele wymagające pełnego Xcode); tylko macOS; brak deklarowanego modelu finansowania.

> **Sprawdź sam #2 — scheduler oMLX.** W klonie `omlx`:
> ```bash
> wc -l omlx/scheduler.py omlx/oq.py omlx/cache/paged_ssd_cache.py
> grep -n "BatchGenerator" omlx/scheduler.py | head
> grep -n "def step" omlx/scheduler.py
> ```
> Powinieneś zobaczyć 16 621 / 11 295 / 5 639 linii i to, że scheduler wywołuje `BatchGenerator` z mlx-lm, zamiast sam składać batch tokenów. *(Polecenia odtworzone z nazw w notatkach.)*

---

## 5. ds4 / DwarfStar w głąb

**Warstwa:** mały, natywny silnik inferencji w C (Metal jako główny, plus CUDA i ROCm), który uruchamia **garstkę** bardzo dużych modeli MoE z **własnych** plików GGUF, z własnym serwerem HTTP (OpenAI, Responses, Anthropic), własnym agentem kodującym, trwałym cache KV na dysku, strumieniowaniem ekspertów z SSD, dekodowaniem spekulatywnym i tensorowym podziałem na dwie maszyny.

### 5.0 Poprawka do nazwy

Nazwa „ds4" jest już historyczna. README mówi dziś: „**DwarfStar** aims to be the best way to run a few excellent large language models on consumer hardware", a pliki binarne nadal nazywają się `ds4`, `ds4-server`, `ds4-agent`, `ds4-bench`, `ds4-eval`. Obsługiwane modele: DeepSeek V4 Flash (w tym „experimental vision"), DeepSeek V4.1 Flash, DeepSeek V4 PRO, **GLM 5.2 / 5.3 / 5.3 Flash**, **Qwen3.8 Flash Next**. Silnik jest więc nadal „celowo wąski, nie jest ogólnym ładowarką GGUF", ale to już „kilka modeli", nie jeden.

⚠️ **Sprzeczność w repozytorium:** plik `AGENT.md` wciąż twierdzi, że „ds4.c is a DeepSeek V4 Flash specific inference engine", co jest nieaktualne względem README i `docs/MODELS.md`. W razie rozbieżności ufaj README.

### 5.1 Tożsamość

- `antirez/ds4`, licencja **MIT**. Plik `LICENSE` ma trzy linie praw autorskich: „The ds4.c authors", „The ggml authors" (2023–2026) i „DeepSeek" (2023). Część tabel kwantyzacji GGUF, logiki CPU i kerneli jest zaadaptowana z llama.cpp/GGML (MIT) — README, sekcja „Acknowledgements". W repo jest też `licenses/Apache-2.0.txt` (fragment zewnętrzny, nie ustaliłem który).
- Utworzone **2026-05-06**; ostatni commit **2026-10-19**; **827 commitów** w ok. 5,4 miesiąca. **Brak wydań i tagów** (README: „very fast changing… beta quality").
- **23 955 gwiazdek**, 2 314 forków, 793 otwarte zgłoszenia i PR-y. Rozkład bajtów: C 9,07 MB, CUDA 4,89 MB, Objective-C 2,34 MB, Metal 1,37 MB, Python 1,0 MB, C++ 0,5 MB.
- Commity: antirez 523, kyuz0 33, ivanfioravanti 28, polymorf 23, Entrpi 15, jyatesdotdev 11, mitsuhiko 7. Czyli ok. 63% to autor; reszta to realny, ale mały ogon.
- Dokumentacja w repo: `README.md` i `docs/*.md` (MODELS, SERVER, CLIENTS, SSD_STREAMING, DISTRIBUTED, SPECULATIVE_DECODING, PERFORMANCE, TESTING, METAL, DGX_SPARK, STRIX_HALO, CUDA_MULTI_GPU, QWEN38_FLASH_NEXT) oraz 147-kilobajtowy `QA_BEFORE_RELEASES.md` — runbook QA z pomiarami.
- Niezwykła deklaracja z README: projekt powstaje „with **strong assistance from AI coding agents** and with humans leading the ideas, testing, and debugging", a filozofia mówi, że oprogramowanie powinno być dostarczane jako „working template", który użytkownik adaptuje własnymi agentami kodującymi.

### 5.2 Argument inżynierski: po co silnik tylko dla jednego modelu

llama.cpp jest uniwersalny: ładuje wiele architektur z jednego formatu, buduje graf obliczeń z opisu architektury w `src/llama-model.cpp`, planuje go przez `ggml_backend_sched` i wysyła do kerneli generycznych. Za tę uniwersalność płacisz warstwami abstrakcji: ogólny graf, ogólny alokator, kernele pisane „pod każdy kształt", szablony czatu składane z Jinja itd.

ds4 idzie w drugą stronę. **Graf jest wpisany na sztywno dla rodziny architektury** (`DS4_N_LAYER`, `DS4_N_HC`, top-k indeksera, uwaga liniowa KDA dla GLM 5.3, tabele n-gramowe/PLE dla Qwen…), a walidacja „akceptuje znane układy Flash i Pro i kończy się wcześnie błędem dla czegokolwiek innego" (komentarz nagłówkowy w `ds4.c`). Z tego wynikają konsekwencje:

1. **Plan całego modelu na Metal.** Zamiast wysyłać pojedyncze operacje z generycznej reprezentacji pośredniej, silnik planuje cały przebieg modelu na poziomie bufora poleceń.
2. **Fuzje pod egzotyczne elementy DeepSeeka** (kompresowany KV z indekserem, hiperpołączenia z więzami, itd.) — kernele mogą zakładać stałe kształty.
3. **Dokładny tokenizer, szablony czatu i narzędzi** — „bloki DSML" dla DeepSeeka, własne szablony dla GLM — zamiast ogólnego silnika szablonów.
4. **Testy względem oficjalnych wektorów logprobów DeepSeeka** (`ds4_test --logprob-vectors`, `CONTRIBUTING.md`): jakość mierzona wobec referencji producenta modelu, a nie wobec innych silników.

Cena: **każda nowa architektura to port na tysiące linii** (np. `metal/qwen4.metal` ma 4 733 linie), a model „może zostać usunięty, gdy pojawi się lepszy zamiennik" (README: wsparcie „intentionally opportunistic"). To nie jest długowieczna platforma; to szybko zmieniające się laboratorium jednego autora, które śledzi aktualnie najlepszy duży MoE.

Analogia: llama.cpp to uniwersalny warsztat z kompletem kluczy; ds4 to oprzyrządowanie pod jeden silnik w fabryce — szybsze przy tym jednym silniku, bezużyteczne przy innym. Precyzyjnie: **projekt nie dokumentuje, że jest szybszy od silników ogólnych** (patrz §5.12) — to argument konstrukcyjny, nie wynik pomiaru.

### 5.3 Układ plików i rozmiary (klon z 19.10.2026)

| Plik / katalog | Linie | Rola |
|---|---:|---|
| `ds4.c` | 87 535 | „pionowy" plik: ładowanie GGUF, stałe układy tensorów, tokenizer, referencyjne kernele CPU, **sterowniki grafu całego modelu**, sesje, ładunki cache dyskowego |
| `ds4_metal.m` + `metal/*.metal` | 50 537 + 32 833 | backend Metal; największe: `moe.metal` 9 591, `dsv4_misc.metal` 7 110, `qwen4.metal` 4 733, `dense.metal` 2 933, `flash_attn.metal` 1 692 |
| `ds4_cuda.cu` + `cuda/mmq/*` | 36 309 + 37 498 | backend CUDA; kernele MMQ/MMVQ zaadaptowane z ggml-cuda |
| `rocm/*.cuh` + `ds4_rocm*.cu` | 32 248 | backend ROCm |
| `ds4_server.c` | 23 115 | serwer HTTP |
| `ds4_agent.c` | 13 635 | agent kodujący |
| `ds4_distributed.c`, `ds4_tp.c` | 8 437, 3 944 | podział na maszyny |
| `ds4_kvstore.c` | 1 352 | dyskowy magazyn KV |
| `ds4_engram.c` | 473 | tabele Engram (V4.1) |
| `tests/`, `gguf-tools/` | 76 802, ok. 20 tys. | testy; konwertery/kwantyzatory (`deepseek4-quantize.c`, `deepseek41_quantize.py`, `glm53_quantize.py`) |

Łącznie pliki C/H/M/CU/CUH na najwyższym poziomie dają ok. **249 625 linii**. To jest **ogromny „mały" silnik**: estetyka „jednego prostego pliku C" nie przetrwała wzrostu do wielu modeli i backendów, choć `AGENT.md` nadal wymaga „small, readable… Do not introduce C++" (C++ pojawia się tylko w plikach kerneli CUDA/ROCm).

**Ładowanie:** oparte na `mmap`; loader parsuje tylko nagłówek GGUF, metadane i katalog tensorów; na Metal wycinki mapowania są opakowywane jako bufory `MTLBuffer` bez kopiowania. Blokada na poziomie procesu uniemożliwia uruchomienie dwóch ogromnych modeli naraz.

### 5.4 Układ kwantyzacji

Ds4 **nie wymyśla nowego formatu** — używa typów llama.cpp/GGML, ale w układzie **asymetrycznym**: celem kompresji są **eksperci kierowani (*routed*)**, a reszta zostaje w wysokiej precyzji.

- Eksperci kierowani: `IQ2_XXS` dla gate/up + `Q2_K` dla down (kalibrowane imatrix).
- „Q8 projections, shared experts and output, plus F16/F32 tensors" pozostają wysokiej precyzji.
- Inne warianty: `Q4_K` oraz **natywne MXFP4** dla ekspertów DeepSeeka (zachowuje oryginalne eksperty FP4 DeepSeeka bez ponownej kwantyzacji; Blackwell używa natywnych instrukcji macierzowych FP4).
- DeepSeek V4 Flash w Q2 to plik ok. **81 GiB** przy 284 mld parametrów ⇒ średnio ok. 2,45 bita na wagę *(moje wyliczenie: 81 GiB × 8 / 284·10⁹)*.
- Modele DeepSeek V4 obsługują kontekst 1M tokenów (Flash 284B łącznie / 13B aktywnych; PRO 1,6T / 49B aktywnych) — `MODEL_CARD.md`. Praktyczny kontekst ogranicza alokacja KV (`--ctx`).
- Pliki publikowane na Hugging Face w `antirez/*` (`deepseek-v4-gguf`, `deepseek-v4.1-flash-gguf`, `glm-5.3-flash-gguf`, `glm-5.3-gguf`, `GLM-5.2-GGUF`, `qwen3.8-flash-next-gguf`) oraz `unsloth/GLM-5.2-GGUF` i `ggml-org/Qwen3.8-Flash-Next-GGUF` (mmproj) — `download_model.sh`, linie 4–11.

**Zadanie dla ciebie:** przepis „2-bitowi eksperci kierowani, Q8 reszta, imatrix tylko na ekspertach" jest odtwarzalny w llama.cpp przez nadpisania typów tensorów (`--tensor-type`/własny GGUF) dla dowolnego dużego MoE (rozdział 03). Twój plik UD-IQ3_XXS od Unsloth to ta sama filozofia (dynamiczna, niejednorodna kwantyzacja), tylko z innymi poziomami.

### 5.5 Dlaczego KV w DeepSeek V4 jest taki mały

Fakty, które silnik koduje (`MODEL_CARD.md`; spójne z rozmiarami z kvstore): 43 warstwy; w każdej warstwie surowe okno przesuwne 128 tokenów; warstwy 0–1 tylko surowe; parzyste ≥ 2 używają **skompresowanego KV w stosunku 4** plus **indeksera** (64 głowice × 128 wymiarów, **top-k 512** skompresowanych wierszy); nieparzyste ≥ 3 używają stosunku 128; do tego hiperpołączenia z więzami rozmaitościowymi (mHC) i MoE ze współdzielonymi + kierowanymi ekspertami.

Skutek: plik pomiarowy `speed-bench/m5_max.csv` (kolumna `kvcache_bytes`) notuje **migawkę KV 52,2 MB przy 2 048 tokenach i 475 MB przy 32 768 tokenach, czyli ok. 14,5 KB na token**. To powód, dla którego kontekst 1M jest w ogóle wyobrażalny i dlaczego **zapisywanie KV na dysk** (§5.7) się opłaca: migawka jest mała.

DeepSeek V4.1 dodaje tabele **Engram** (osadzenia wierszy hashowane n-gramami; 189 GiB wierszy FP8 ze skalami w pliku Q2), które **nigdy nie są ładowane do RAM-u** — czytane przez `pread` na żądanie osobnym, niecache'owanym deskryptorem z ograniczonymi buforami tymczasowymi (384 KiB) (`ds4_engram.h`, `docs/MODELS.md`).

### 5.6 Strumieniowanie ekspertów z SSD

Gdy model jest większy niż RAM (`ds4_ssd.c`, `docs/SSD_STREAMING.md`):

```
 RAM / pamięć GPU                       SSD (plik GGUF)
 ┌──────────────────────────┐            ┌─────────────────────────┐
 │ tensory nie-kierowane    │            │ wszyscy eksperci        │
 │ (uwaga, współdzieleni,   │            │ kierowani (routed)      │
 │  wyjście) — rezydentne   │            └────────────▲────────────┘
 │                          │                         │ pread przy pudle
 │ ograniczony cache        │◄────────────────────────┘
 │ ekspertów kierowanych    │   (odczyt ukryty za obliczeniami
 │  - start: „hotlist"      │    ekspertów współdzielonych /
 │    z binarki             │    poprzedniej warstwy)
 └──────────────────────────┘
```

- Nie-kierowane wagi zostają rezydentne (Metal próbuje je „przypiąć" w pamięci).
- **Eksperci kierowani żyją w ograniczonym cache; chybienia czyta się z GGUF**, a opóźnienie chowa się za obliczeniami ekspertów współdzielonych/poprzedniej warstwy. `AGENT.md`: „always try to hide loading of missing routed experts by loading them while performing the inference of the shared expert".
- Budżet cache jest domyślnie automatyczny (`ds4_ssd_auto_cache_plan`); ręcznie `--ssd-streaming-cache-experts 32GB` (bajty) lub sama liczba (sloty ekspertów).
- **Hotlista precomputed**: `ds4_streaming_hotlist.inc` (192 KB; `…_glm52.inc`) jest wkompilowana w binarkę (wygenerowana z profilowania), dzięki czemu cache startuje od ekspertów prawdopodobnie „gorących"; jest też profiler (`ds4_expert_profile_*`).
- Pomiary (M5 Max 128 GB, 2026-09-06, cache automatyczny; *dane projektu*): GLM 5.3 Flash Q4_K (177,77 GiB) — prefill początkowy 121 tok/s, dekodowanie 11,9 → 14,9 tok/s; DeepSeek Flash Vision Exp MXFP4 (145 GiB) — prefill 300 tok/s, dekodowanie 11,9 → 19,3 tok/s (pojedynczy przebieg; `docs/SSD_STREAMING.md`).

Intuicja: MoE aktywuje w każdym kroku tylko garstkę ekspertów, a rozkład użycia jest nierówny, więc **mały cache gorących ekspertów trafia często**. SSD dostarcza resztę. Tak model 178 GiB działa na maszynie ze 128 GB RAM-u z szybkością „interaktywną", choć wolniejszą niż model rezydentny.

### 5.7 Dyskowy magazyn KV (`ds4_kvstore.c/.h`)

To jest najbardziej „agentowa" część ds4.

- **Klucz = SHA-1 renderowanego prefiksu tekstowego** (nazwa pliku = hash prefiksu bajtów). Ładunek zawiera dokładne tokeny i stan grafu; nagłówek 48 bajtów z `model_id`, `quant_bits`, `ctx_size` i kodem powodu zapisu (COLD / CONTINUED / EVICT / SHUTDOWN / AGENT_SYSTEM / AGENT_SESSION). Eksmisja używa licznika trafień z **półokresem 6 godzin**.
- Flagi serwera: `--kv-disk-dir`, `--kv-disk-space-mb` (domyślnie 4096 MB), `--kv-cache-min-tokens`, `--kv-cache-cold-max-tokens`, `--kv-cache-continued-interval-tokens`, przycinanie i wyrównywanie granic, `--kv-cache-reject-different-quant`.
- **Kolejność wyszukiwania:** żywy slot z prefiksem tokenów → zgodne prefiksy tekstowe na dysku → prefill tylko sufiksu.
- **Mapa powtórek ID wywołań narzędzi (*tool-call ID replay*)**: serwer pamięta dokładnie wylosowany blok DSML wywołania narzędzia i używa go ponownie, zamiast ponownie tokenizować JSON przeformatowany przez klienta (`--tool-memory-max-ids`). Ma to znaczenie, bo klienci agentowi odsyłają historię w nieco innej postaci — a gdyby tokeny się różniły, prefiks przestałby pasować i cache by nie trafił.
- Przy podziale tensorowym (TP) odtworzenie prefiksu musi odbudować go na obu rangach — nie ma natychmiastowego odtworzenia.

**Dlaczego klucz tekstowy, a nie tokenowy?** Bo klient widzi tekst; hash renderowanego prefiksu to niezależność od drobnych różnic tokenizacji na granicach wiadomości. Nie wiem, czy autor tak to uzasadniał — to moja interpretacja wzoru w kodzie *(niezweryfikowane)*.

### 5.8 Dekodowanie spekulatywne: DSpark i MTP

(`docs/SPECULATIVE_DECODING.md`, `ds4_deepseek41_dspark.h`, `metal_graph_dspark_*` w `ds4.c`)

- **DSpark** (tylko DeepSeek): osobny **GGUF „support"** (5,6 GiB dla V4 Flash 0731; 8,04 GiB dla V4.1) z małym drafterem, który zużywa stany ukryte **zebrane z 3 warstw modelu docelowego** (`target[3]`, `window[3]`, okno szkicu 128 pozycji, `DS41_DRAFT_ROWS 5`, `DS41_VERIFY_ROWS 6`) i proponuje do 5 tokenów plus **głowicę pewności** (`--dspark-confidence`; domyślne przycinanie 0,4 na jednym Sparku, 0,8 dla dokładnego próbkowania). Model docelowy weryfikuje w jednym przebiegu batchowym i zachowuje najdłuższy zaakceptowany prefiks. Dla V4 wymaga rezydentnych wag (nie działa ze strumieniowaniem SSD); dla V4.1 DSpark działa ze strumieniowaniem (drafter zostaje w pamięci, +8 GiB). Nie dla PRO. Dwa hosty TP mogą podzielić drafter przez RDMA.
- **MTP** (GLM 5.3, Qwen3.8): wbudowane w główny GGUF; GLM zatwierdza do 2 tokenów na cykl; Qwen szkicuje 1 do przodu z adaptacyjnym drugim łańcuchowym. Flaga `--mtp`.
- **Semantyka próbkowania jest jawna:** domyślny tryb „opportunistic" akceptuje zachłanny szkic tylko, gdy zgadza się z zachłannym tokenem celu (bardziej deterministyczny niż prawdziwe próbkowanie); `--mtp-exact-sampling` implementuje pełną regułę akceptuj/popraw zachowującą rozkład modelu docelowego.
- Dokumentacja ostrzega: „V4.1 DSpark can still be slower than ordinary decoding"; batchowanie sesji wyłącza MTP/DSpark (poza Qwen na Metal).

Pomiary (*dane projektu*, `docs/DGX_SPARK.md`; mediany z 2 przebiegów; temp. 0, kontekst 64K): dwa DGX Spark po RoCE, V4 Flash 0731 Q2: **44,0 tok/s** (proza angielska) i **83,3 tok/s** (kod C — tablica haszująca) z DSpark, wobec **26,0 tok/s** bez; jeden Spark z DSpark: 23,4 i 44,0 tok/s.

**Lekcja:** zysk ze spekulacji zależy od **treści**. Kod (przewidywalny) przyspiesza ponad trzykrotnie, proza o ok. 1,7×. Gdy mierzysz własną instalację, mierz na promptach, jakie naprawdę dajesz agentom.

### 5.9 Równoległość

Z `docs/DISTRIBUTED.md` i `CUDA_MULTI_GPU.md`:

- **Tensorowy podział na dwie maszyny** (50/50 ekspertów kierowanych, dokładnie jeden worker): koordynator/worker po **Thunderbolt RDMA na Macach** (potrzebny `rdma_ctl`; na maszynach 128 GB `sudo sysctl iogpu.wired_limit_mb=120000`) albo RoCEv2 na dwóch DGX Spark, z awaryjnym TCP. „No authentication or encryption"; wszystkie węzły muszą mieć ten sam commit.
- **Podział rurociągowy**: całe zakresy warstw na kilku maszynach (nie zaimplementowany dla V4.1).
- **Wiele GPU CUDA na jednym hoście**: całe warstwy na GPU (`--gpu-devices`, `--gpu-vram auto`) albo `--cuda-tensor-parallel`, który paruje GPU i dzieli ekspertów wewnątrz pary; testowane: 4×48 GB Q2 i 8×L40S Q4. **126 tok/s zbiorczo przy 16 sesjach na 8×L40S** (Flash Q4; *dane projektu*; plik QA notuje na tym sprzęcie także prefill 1 524,84 tok/s i 46,93 tok/s dla pojedynczego strumienia).

Dla porównania z twoim rigiem — to jest **dokładnie ta klasa konfiguracji** (kilka kart, układ warstw), tyle że w backendzie CUDA, nie ROCm.

### 5.10 Sterowanie kierunkowe (*steering*)

Katalog `dir-steering/`: płaska macierz f32 z jednym znormalizowanym kierunkiem o szerokości ukrytej na warstwę. W czasie działania, po wyjściu uwagi i/lub FFN:

```
y = y - scale * direction[layer] * dot(direction[layer], y)
```

(ujemna skala wzmacnia kierunek). Kształty plików: DeepSeek V4 Flash `43 × 4096`, GLM 5.3 Flash `45 × 4096`, Qwen3.8 Flash Next `48 × 2560`. `build_direction.py` buduje wektor z list par promptów „dobry/zły" (przykład w repo: zwięzły vs rozwlekły, 100 par); `/steer F` zmienia skalę na żywo **bez przebudowy cache KV**. Działa z MTP, serwerem, batchowaniem sesji i TP na 2 Macach dla GLM 5.3; nie dla GLM 5.2. To tania demonstracja edycji aktywacji w stylu interpretowalności — dobre ćwiczenie edukacyjne.

Osobna gałka: `--power N` (tylko DeepSeek V4) wymienia przepustowość na niższe stałe obciążenie GPU.

### 5.11 API, narzędzia i klienci

- **Binarki:** `ds4` (CLI/REPL z linenoise), `ds4-server`, `ds4-agent` (natywny agent kodujący bez przeskoku HTTP, `/save`, `/switch`, sesje w `~/.ds4/kvcache`, narzędzie `view_image`, `/hints`), `ds4-bench` (sweep długości kontekstu), `ds4-eval` (osadzone zestawy regresji `core`/`hard`).
- **HTTP** (`docs/SERVER.md`): `GET /v1/models`, `POST /v1/chat/completions`, `POST /v1/responses`, `POST /v1/completions`, `POST /v1/messages` (Anthropic). Narzędzia i SSE w chat/Responses/Anthropic; rozumowanie zwracane osobno w natywnej formie każdego API; `reasoning_effort=max` włącza Think Max tylko przy dość dużym kontekście. Nazwy typu `deepseek-v4-flash` to „aliasy zgodności, nie osobne załadowane modele" — **jeden model na proces serwera**. Obrazy (PNG/JPEG jako data URI; ≤ 16 obrazów, 64 MiB) z odpowiednim enkoderem `--vision`.
- **Przepisy dla klientów** (`docs/CLIENTS.md`): Pi, OpenCode, Codex CLI (Responses API) i **Claude Code** (endpoint Anthropic przez `ANTHROPIC_BASE_URL`; przepis ustawia `ANTHROPIC_DEFAULT_*_MODEL` i `CLAUDE_CODE_SUBAGENT_MODEL` na model lokalny).
- **Myślenie:** domyślnie włączone; `--nothink`; dla V4.1 `--think-level 1..100` (0 = wyłączone); domyślne próbkowanie temp 1, top-p 1, min-p 0,05.
- **Sesje wielokrotne:** `--batched-session N` prealokuje N stanów KV; natywne batchowane dekodowanie tam, gdzie wspierane (Metal rezydentny V4.1: 2–8 sesji; układ TP CUDA); **pojedyncze GPU CUDA, w tym Spark = uporządkowany fallback, czyli współbieżność bez przyspieszenia**.
- **Bezpieczeństwo:** serwer wiąże się domyślnie z 127.0.0.1:8000; brak uwierzytelniania („put authentication and TLS in front"). Zewnętrzne wywołanie sieciowe robi tylko `download_model.sh` (opcjonalny token HF). Nie znalazłem telemetrii ani sprawdzania aktualizacji w liście plików, ale **nie przeszukałem każdego źródła pod kątem gniazd** *(niezweryfikowane dla twierdzenia „wyczerpująco")*.

### 5.12 Wydajność (wszystkie liczby: *dane projektu*)

Konfiguracja: DeepSeek V4 Flash Q2 (`IQ2_XXS` gate/up + `Q2_K` down), zachłannie, 128 tokenów na front, `ds4-bench`, tekst `speed-bench/promessi_sposi.txt`. Wartości: prefill / generowanie, tok/s.

| Maszyna | Kontekst 2 048 | Kontekst 32 768 | Plik |
|---|---|---|---|
| M5 Max 128 GB | 790,2 / 39,35 | 557,0 / 34,36 | `speed-bench/m5_max.csv` |
| M4 Max (RAM nie podany w nazwie CSV) | 343,8 / 26,76 | 247,9 / 24,52 | `m4_max.csv` |
| M2 Ultra | 410,6 / 23,22 | 325,8 / 21,92 | `m2_ultra.csv` |
| DGX Spark 128 GB (GB10) | 825,8 / 18,05 | 855,9 / 14,43 | `gb10.csv` |
| Strix Halo gfx1151 128 GB (ROCm 7.14) | prefill 231,9 przy 2K („tuned"), 292,9 przy 4K (ciepły) | – | `speed-bench/gfx1151-prefill-results.md` |
| M3 Ultra, **PRO** Q2 (1,6T) | 183,1 / 12,42 | 138,8 / 9,56 | `pro_model_m3_ultra.csv` |

Dodatkowo w `QA_BEFORE_RELEASES.md` (linia 1491; moja interpretacja etykiet komórek, zweryfikuj) dla Strix Halo, kod w 128 tokenach, temp 1: dekodowanie zwykłe 16,26 tok/s, „opportunistic" 12,28, „exact" 13,52 — czyli na tym prompcie spekulacja była **wolniejsza** od zwykłego dekodowania.

**Czego nie ma:** w repozytorium nie ma porównania z llama.cpp ani MLX (grep po dokumentacji znajduje „llama.cpp" tylko w podziękowaniach). Nie znalazłem też porównania zewnętrznego *(niezweryfikowane)*. Zatem „szybszy niż silniki ogólne" **nie jest udokumentowane przez projekt**. Co jest sprawdzone: jakość porównywana jest z oficjalnymi wektorami logprobów DeepSeeka, nie z innymi silnikami.

**Co ds4 optymalizuje:** opóźnienie pojedynczego strumienia dla agentowego kodowania na jednym dużym pudle plus ponowne użycie prefiksów z dysku. Batchowaną przepustowość dostajesz tylko w układzie TP wielu GPU CUDA i na ścieżkach rezydentnych Metal.

### 5.13 Twój wynik z llama.cpp vs dane ds4 — i dlaczego to nie jest porównanie „jabłko do jabłka"

Twój zmierzony wynik (z `../przyspieszanie-generowania/README.md`): **23,5 → ok. 50 tok/s** dla jednego agenta, llama.cpp, DeepSeek-V4-Flash w UD-IQ3_XXS, 4× R9700, podział tensorowy + DSpark. Jedyny punkt danych ds4 dla R9700 (PR #558, §5.14): **jedna** karta R9700 32 GB, V4 Flash Q2 (~81 GB) **ze strumieniowaniem SSD**, generowanie **2,30 → 4,70 tok/s**, prefill 3,67 → 6,33 tok/s.

> ⚠️ **To nie jest porównanie like-for-like.** Różnice, każda z osobna wystarczy do unieważnienia wniosku „silnik X jest N razy szybszy":

| Wymiar | Twój wynik | Punkt danych z PR #558 |
|---|---|---|
| Silnik | llama.cpp (build 0ce8cd1) | ds4 + niezmergowana łatka |
| Kwantyzacja | UD-IQ3_XXS (Unsloth, niejednorodna) | Q2 ds4 (`IQ2_XXS` + `Q2_K`, ok. 2,45 b/w) |
| Karty | 4 × R9700, łącznie 128 GB VRAM | 1 × R9700 32 GB |
| Gdzie są wagi | **w całości w VRAM** | większość na SSD, strumieniowana przez cache |
| Dekodowanie spekulatywne | DSpark włączony | brak informacji w PR |
| Reszta platformy | twój host | Ryzen 9 9950X3D, 128 GB DDR5, ROCm 7.2.2, Ubuntu 26.04 |
| Źródło | twój pomiar | liczby autora PR *(dane autora PR)* |

**Co z tego wolno wywnioskować** *(moje wnioskowanie)*: różnicę rzędu 10× między 4,7 a ~50 tok/s najprawdopodobniej tłumaczy przede wszystkim to, **gdzie leżą wagi** — rezydentne w 4 × 32 GB kontra strumieniowane z SSD przez jedną kartę — a nie wyższość jednego kodu nad drugim. Dokładnie tak działa twierdzenie z §1: gdy wagi muszą przechodzić przez wolniejszy nośnik, ten nośnik staje się sufitem. Gdyby ds4 miało na ROCm układ warstw jak w CUDA, mogłoby w zasadzie trzymać 81 GiB w twoich 128 GB VRAM (to hipoteza *(niezweryfikowane)*) — i dopiero wtedy porównanie miałoby sens.

Zysk ze spekulacji wygląda podobnie w obu światach: u ciebie ok. 2,1× (23,5 → ~50), u projektu ds4 na dwóch Sparkach 1,7× dla prozy i 3,2× dla kodu (26,0 → 44,0 / 83,3). To **nie** są porównywalne pomiary (inny sprzęt, inny model w innej kwantyzacji, inne prompty), ale pokazują ten sam efekt: zysk zależy od treści i mieści się w przedziale „około dwukrotności".

**Wniosek praktyczny:** dla twojego rigu llama.cpp jest dziś jedynym realnym wyborem, bo ds4 nie buduje się na gfx1201 bez łatek.

### 5.14 ROCm i gfx1201 — stan na 19.10.2026

- Gałąź główna ma `ROCM_ARCH ?= gfx1151` (Strix Halo). **Dostrojone ścieżki są bramkowane przez `ds4_rocm_is_gfx1151()`** (np. `rocm/ds4_rocm_common.cuh:6-22`, `ds4_rocm_hipblaslt.cuh`, wiele przełączników środowiskowych `*_gfx1151_flag(...)`). Referencyjna maszyna dev to Strix Halo (APU z pamięcią zunifikowaną) — `QA_BEFORE_RELEASES.md`, §9.
- Backend ROCm jest w kodzie **jednourządzeniowy**: `ds4_rocm_compat.cu` wybiera jedno urządzenie HIP (`hipSetDevice(g_gpu[0].device_id)`), podczas gdy backend CUDA ma mechanizm rozmieszczania warstw na wielu GPU (`ds4_gpu_mgpu.h`, `DS4_MAX_GPUS 16`, 62 miejsca wywołania `SetDevice` w `ds4_cuda.cu`). *Wniosek o jednourządzeniowości to moja interpretacja grepa, pewność umiarkowana.*
- **Otwarta praca zewnętrzna — wszystko niezmergowane na 19.10.2026** (API GitHuba):
  - zgłoszenie **#521** (2026-07-08, cm999club): „gfx1201 (RDNA4, R9700) build fails: `__builtin_amdgcn_wmma_f32_16x16x16_f16_w32` not supported" — ręcznie pisany kernel GEMM Q8 używa wbudowanej funkcji WMMA w stylu gfx11, a RDNA4 zmieniło sygnatury;
  - PR **#558** (2026-07-13): „run on discrete RDNA4 (gfx1201) — opt-in WMMA fallback + configurable VRAM reserve". Test autora na **jednej R9700 32 GB**, V4 Flash Q2 (~81 GB) **ze strumieniowaniem SSD**: prefill 3,67 → 6,33 tok/s, generowanie 2,30 → 4,70 tok/s po nadpisaniu sztywno zakodowanej rezerwy 16 GiB wolnego VRAM (`DS4_ROCM_FREE_RESERVE_MB=2048`, cache 26 GB) *(dane autora PR)*; endpointy serwera działały;
  - PR **#599** (2026-07-24) „gate the WMMA v1 kernel" i PR **#744** (2026-08-08, bestbug456) „rdna4 gfx1201 rocwmma v2";
  - PR **#602** (ewindisch, 2026-07-24): „AMD Instinct (CDNA/gfx90a) support with multi-GPU device placement"; PR #1233 „CUDA: resident V4.1 multi-GPU layer placement, validated on Turing";
  - zbiorcze zgłoszenie **#16** „AMD GPU (ROCm/HIP) and especially Strix Halo".

**Stan:** (a) bez łatek nie zbuduje się na gfx1201, (b) z łatką działa na jednej karcie przez strumieniowanie SSD z szybkością 2–5 tok/s, (c) wielokartowe rezydentne ułożenie warstw istnieje tylko w CUDA. Warto obserwować PR-y #558, #744 i #602.

### 5.15 Forki i rozpęd społeczności

Z API GitHuba, 19.10.2026:

| Projekt | Gwiazdki | Co to |
|---|---:|---|
| `notatestuser/ds4-control` | 915 | aplikacja menu-bar w Swifcie (MIT) „for fast local DeepSeek V4.1, with 1M context"; pojedyncza binarka Swift; ds4 jako submoduł git z łatkami; „no embedded inference" |
| `ivanfioravanti/ds4-metal` | 87 | fork Metal (push dziś); Ivan Fioravanti, założyciel CoreView, współtwórca mlx-lm |
| `Entrpi/ds4` | 77 | CUDA Blackwell: „~4x prefill, ~1.5x decode, continuous batching, weight server, DSpark" *(deklaracja forka)* |
| `hebrus-labs/hebrus` | 66 | Metal-first MoE ze strumieniowaniem ekspertów z SSD |
| `giannisanni/neutronstar` | 40 | CUDA, io_uring, cache hosta LFU, „first MTP for GLM-5.2" |
| `audreyt/ds4` | 36 | wariant z checkpointem „abliterated" |
| `paperniuk/ds4` | 24 | strojenie M1/M2; Qwen3.8 Flash Next 262K na 64 GB, „35 tok/s on an M1 Max" |
| `kernelpool/ds4` | 15 | też współtwórca mlx-lm |
| `kyuz0/strix-halo-ds4-toolbox` | 94 | kontenery toolbox dla Strix Halo |

Niezależne, nie-forkowe projekty, które w opisie powołują się na ds4: `mw00/project-maya` (1 080 gwiazdek, C++, „run GLM-5.3-Flash and DeepSeek-V4.1-Flash privately on your own GPU(s), from one card to 16, NVIDIA or AMD") i `gufo-org/gufo` (816, „Open Source Strix Halo AI engine"); związek z ds4 nie jest zweryfikowany *(niezweryfikowane)*. Pomysł „silnika zbudowanego wokół konkretnych modeli" kopiują też inni (hebrus, mlx-serve, Splash, gufo).

**Odczyt rozpędu** *(moje wnioskowanie z liczb)*: ok. 24 tys. gwiazdek w 5,4 miesiąca, 827 commitów, codzienne pushe i widoczny ekosystem (aplikacja menu-bar, forki dla Blackwell, Strix i M1). Bus factor architektury ≈ 1, ale licencja MIT i 2 314 forków łagodzą ryzyko.

### 5.16 Mocne i słabe strony, pułapki

+ Uruchamia **najnowsze gigantyczne MoE** (284B–1,6T) na maszynach 96–128 GB z interaktywną szybkością dzięki 2-bitowym ekspertom + architekturze z kompresowanym KV + strumieniowaniu SSD. Presety kwantyzacji mlx-lm nie oferują domyślnie tej asymetrycznej receptury; najbliższe jest oQ2.
+ Dyskowy KV + powtórka ID narzędzi są zbudowane pod agentów kodujących.
+ Zależności: C + Metal/CUDA/HIP, bez Pythona w czasie działania.
− Jeden model na proces, brak menedżera modeli, uwierzytelniania i hot reloadu; modele bywają „oportunistycznie" usuwane.
− Szybkie zmiany, brak wydań/tagów, „instabilities and regressions are definitely possible"; ok. 793 otwarte pozycje na jednego opiekuna.
− **Numeryczna nieidentyczność** ścieżek skalarnych, batchowanych, TP i spekulatywnych (udokumentowana).
− Pojedyncze GPU CUDA/ROCm serwuje sesje po kolei (bez przyspieszenia); ROCm tylko gfx1151.
− Kod w dużej mierze pisany z asystą AI (deklaracja projektu) — powierzchnia przeglądu to ok. 250 tys. linii.

### 5.17 Kto za tym stoi

**Salvatore Sanfilippo (antirez)** — BDFL. Zweryfikowane: profil GitHub („Computer programmer based in Sicily, Italy… Born 1977", pole firmy „Redis Labs" — nieaktualne, 32,3 tys. obserwujących); Wikipedia: autor Redisa (2009), zrezygnował z roli opiekuna 2020-06-30, **wrócił do firmy Redis w grudniu 2024 jako „evangelist"**, potem zbudował Vector Sets. Jego blog wg streszczenia mówi, że „niedawno wrócił do Redis" i pracuje nad DwarfStar *(wording przybliżony — strona pobrana przez streszczacz)*. Dla ds4 nie ma firmy, finansowania ani płatnej wersji, MIT. Czy Redis płaci za czas pracy nad ds4 — nie ustaliłem *(niezweryfikowane)*. Pełniej: [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

> **Sprawdź sam #3 — czy ds4 ma ROCm dla gfx1201?**
> ```bash
> grep -n "ROCM_ARCH" Makefile
> grep -rn "ds4_rocm_is_gfx1151" rocm/ | head
> gh api repos/antirez/ds4/pulls/558 --jq '.state, .merged'
> ```
> Zobaczysz domyślne `gfx1151`, bramki `ds4_rocm_is_gfx1151()` i stan PR #558 (na 19.10.2026: otwarty, niezmergowany). *(Odtworzone z nazw w notatkach; nie uruchamiałem ich w tej postaci. Polecenie `gh` zwraca stan z chwili wywołania — może być nowszy niż w tym rozdziale.)*

> **Sprawdź sam #4 — rozmiar „małego" silnika.**
> ```bash
> wc -l ds4.c ds4_metal.m ds4_cuda.cu ds4_server.c ds4_kvstore.c
> ls docs/ && ls ~/.ds4/kvcache 2>/dev/null
> ```
> Ma wyjść 87 535 / 50 537 / 36 309 / 23 115 / 1 352 linii (stan klonu z 19.10.2026; liczby szybko się zmieniają).

---

## 6. Własny stos Apple: Foundation Models, Core ML, Core AI, ANE

Krótko, bo to nie jest ścieżka do uruchamiania dużych modeli otwartych.

- **Foundation Models** (framework Swift): `LanguageModelSession`, generowanie z gwarancją typu `@Generable`, wywołania narzędzi (`Tool`), transkrypty, strumieniowanie, obrazy. Wymaga urządzenia z Apple Intelligence. Domyślny model na urządzeniu ma okno **4 096 tokenów na sesję** (dokumentacja „managing the context window" i TN3193). Wpis z 2025 mówił o 65K tokenów — **liczby się rozjeżdżają**; to, co egzekwuje API, to wartość z dokumentacji dla deweloperów (4 096), rozbieżność pozostaje niewyjaśniona.
- **Modele trzeciej generacji** (zapowiedź 2026-06-08, *dane firmy*, przez streszczacz): **AFM 3 Core** (3B gęsty) i **AFM 3 Core Advanced** (20B rzadki, 1–4B aktywnych; pełne wagi we flashu, eksperci współdzieleni zawsze aktywni, kierowani zamieniani do DRAM-u; „Instruction-Following Pruning" = routing per prompt, nie per token). Model 2025: ok. 3B, 2-bitowe wagi QAT, współdzielenie KV w podziale bloków 5:3 (−37,5% cache), 15 języków *(dane firmy)*.
- **Private Cloud Compute z tego samego API** (iOS/macOS 27): `PrivateCloudComputeLanguageModel` — kontekst 32K, „wiele poziomów" rozumowania, dzienny limit żądań, wymaga sieci i uprawnienia; `SystemLanguageModel` — offline, bez limitu, 4K, bez rozumowania.
- **Modele zewnętrzne:** framework „provides a consistent API experience for using any language model, including those you bring from other model providers"; otwarty model wyeksportowany przez **Core AI** (`apple/coreai-models`, BSD-3-Clause, 2 198 gwiazdek, utworzone 2026-06-08; „wybierz model ok. 0,6B parametrów na początek") ładujesz do `LanguageModelSession` przez `CoreAILanguageModel` (macOS/iOS 27, Xcode 27).
- **Core AI** (macOS/iOS 27): modele w aplikacji na CPU, GPU i Neural Engine; format `.aimodel`, kompilator AOT `coreai-build`, `AIModelCache`. Stoi obok Core ML; czy Core ML jest wycofywany — nie ustaliłem *(niezweryfikowane)*.
- **Data point z ery Core ML** (wpis Apple 2024): Llama-3.1-8B-Instruct, M1 Max, macOS 15.2 beta, Int4 blokowo (blok 32) → **ok. 33 tok/s**, 16 GB → 4,2 GB, TTFT 51,9 ms; Apple celowało w **GPU**, bo LLM-y „are usually constrained by memory bandwidth" *(dane firmy)*.

**Czego tym kanałem nie zrobisz:** brak serwera w stylu OpenAI, brak dowolnego GGUF/safetensors bez eksportu Core AI, mały kontekst na urządzeniu, wymóg urządzenia z Apple Intelligence; modele 30B+ nie są celem frameworka.

### Neural Engine a GPU

Apple samo uruchamia dekodowanie LLM na **GPU**; tak samo robią MLX, llama.cpp, ds4 i oMLX. ANE to blok stałych kształtów, niskiego poboru mocy, dobry do mnożeń macierzy o dużej gęstości obliczeń. Eksperymentalne dwu-ANE + GPU w oMLX pomaga tylko **prefillowi** (ograniczonemu obliczeniami), wymaga *prywatnych* API, stałych kształtów i INT8, a części rekurencyjne i wrażliwe na precyzję zostawia na GPU. Reguła kciuka: **ANE = obliczenia gęste i małe modele „zawsze włączone"; GPU = dekodowanie dużych modeli ograniczone przepustowością**. Neural Accelerator z M5 w rdzeniach GPU celuje w prefill i TTFT, nie w przepustowość dekodowania *(dane firmy / źródło zewnętrzne)*.

---

## 7. exo — klaster Maców

**Warstwa:** warstwa klastrowa, która odkrywa maszyny w sieci, decyduje, jak podzielić model (rurociąg czy podział tensorowy), uruchamia MLX na każdym węźle z kolektywami MLX distributed i wystawia API zgodne z OpenAI, Claude, Responses i Ollama oraz panel.

### 7.1 Tożsamość

Repozytorium `exo-explore/exo`, Apache-2.0; Python (2,87 MB) + panel Svelte + aplikacja macOS w Swifcie + sieć w Rust (`rust/networking`, `rust/exo_rs`). Utworzone 2024-06-24; **47 965 gwiazdek**, 3 567 forków, 378 otwartych pozycji; ostatnie wydanie **v1.0.71 (2026-04-23)**, ale commity do 2026-10-13 (projekt wydaje z `main` i przez DMG). Najwięcej commitów: AlexCheema 1 424, Evanev7 147, rltakashige 141, JakeHillion 74, cadenmackenzie 64. Opiekun: **exo labs** („Run frontier AI locally"). Strona firmy: misja „building the future of democratized, sovereign machine intelligence"; wzmianka o przychodach: „open-source software and enterprise consulting"; **finansowanie, inwestorzy i założyciele nie są ujawnione na stronie** — rundy finansowania nie znalazłem. Więcej: [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

Poziomy platform (`PLATFORMS.md`): Tier 1 = Apple Silicon macOS (Mac Studio M3 Ultra, Mac mini M4 Pro, MacBook Pro M5/M4 Max); planowane: Linux CUDA (DGX Spark), Linux CPU; Tier 2 planowany: Vulkan/CUDA na Framework Desktop; Windows później.

> ⚠️ **Linux = tylko CPU.** README: „Currently, exo runs on CPU on Linux. GPU support for Linux platforms is under development." Istnieje `uv sync --extra mlx-cuda12|mlx-cuda13|mlx-cpu` (backend CUDA MLX), ale **exo nie jest sposobem na użycie twojego rigu AMD** — nie ma ścieżki AMD.

### 7.2 Jak to działa

**Odkrywanie i sieć:** crate Rust `rust/networking` (`discovery.rs`, `swarm.rs`) z pub/sub opartym na **Zenoh** (`EXO_ZENOH_NAMESPACE` izoluje klastry; `routing/router.py`, `event_router.py`, `topics.py`). Węzły odnajdują się w LAN automatycznie, bez konfiguracji.

**Wybór mastera i event sourcing:** `shared/election.py` — wybory (limit 3 s, heartbeat mastera co 5 s, 30 s ciszy mastera, ponowienia 15–300 s); komentarze zauważają, że węzeł, który padł w klastrze ≥ 3, może pozostać „widoczny" przez liveliness Zenoh. `shared/apply.py` stosuje zdarzenia do stanu współdzielonego; `master/main.py` (35 KB) umieszcza i zarządza instancjami; workery uruchamiają runnery (`worker/runner/llm_inference`, `image_models`).

**Rozmieszczanie świadome topologii** (`master/placement.py::place_instance`):

1. wylicza **cykle** połączonych węzłów (`topology.get_cycles()`);
2. filtruje po wymaganej pamięci (rozmiar modelu vs pamięć węzła po uwzględnieniu ładowanych instancji), po wsparciu backendu i po podzielności dla podziału tensorowego (`hidden_size % n == 0` i głowice KV podzielne; wyjątek: DeepSeek V4);
3. preferuje **najmniejszy wystarczający cykl**, cykle RDMA dla `MlxJaccl`, heurystyki postępu pobierania i liści.

Tryby: `Sharding.Pipeline` lub `Sharding.Tensor`; parametr `min_nodes`.

```
 4 Mac Studio, pełna siatka Thunderbolt 5 (JACCL):

      A ───────── B          6 kabli = 4·3/2
      │ ╲       ╱ │          każda para ma własne łącze
      │   ╲   ╱   │          (wymóg „fully connected")
      │     ╳     │
      │   ╱   ╲   │          podział tensorowy: każda warstwa
      │ ╱       ╲ │          rozcięta na 4, all_sum po każdym
      C ───────── D          bloku → wymaga niskiej latencji RDMA
```

**Wykonanie równoległe** (`worker/engines/mlx/auto_parallel.py`, 64 KB):

- `pipeline_auto_parallel` owija warstwy w `PipelineFirstLayer/LastLayer` (send/recv aktywacji; potokowa kolejka prefillu);
- `tensor_auto_parallel` z klasami `TensorParallelShardingStrategy` per architektura (Llama, DeepSeek V3, **DeepSeek V4**, GLM4 MoE (Lite), MiniMax, Qwen, GPT-OSS, Step 3.5, NemotronH, Gemma 4) dzielącymi warstwy liniowe, głowice uwagi i ekspertów MoE oraz wstawiającymi kolektywy `all_sum` (`_AllSumLinear`, `ShardedMoE`);
- backendy: MLX **ring (TCP)** lub **MLX JACCL (RDMA po Thunderbolt 5)**; aplikacja macOS instaluje profil sieciowy i oczekuje `rdma_ctl enable` z Recovery (macOS ≥ 26.2).
- Istnieją katalogi „disaggregated inference" (`worker/disaggregated`, `engines/mlx/disaggregated`) — podział prefill/decode; dojrzałość nieznana *(niezweryfikowane)*.
- API: OpenAI Chat Completions, Claude Messages, OpenAI Responses, Ollama; modele HF; modele obrazowe (flux, qwen) za `EXO_ENABLE_IMAGE_MODELS`; zmienna `EXO_OFFLINE` dla pracy offline.

### 7.3 Co ogranicza exo

README twierdzi „up to 1.8x speedup on 2 devices and 3.2x speedup on 4 devices" dla podziału tensorowego i „99% reduction in latency between devices" z RDMA *(dane projektu)*; obrazy benchmarkowe powołują się na klaster Jeffa Geerlinga z 4 × M3 Ultra (Qwen3-235B 8-bit, DeepSeek V3.1 671B 8-bit, Kimi K2 Thinking 4-bit) *(dane projektu / źródło zewnętrzne — czytałem deklaracje, nie same wykresy)*. Ograniczenia z kodu i dokumentów:

- **JACCL wymaga pełnej siatki** Thunderbolt z kablami TB5, jednakowych wersji macOS na wszystkich węzłach (nawet wersji beta) i nie wszystkie porty Mac Studio się nadają;
- **rurociąg daje pojemność, nie szybkość** pojedynczego strumienia dekodowania — każdy token przechodzi przez wszystkie etapy;
- podział tensorowy potrzebuje podzielnych głowic/wymiarów i kodu per architektura;
- wybór mastera na chwilę wstrzymuje klaster;
- Linux tylko CPU; brak ścieżki AMD.

Wpis Apple z października 2026 pokazuje ten sam mechanizm MLX + JACCL na 4 × M5 Ultra (§2.6) — **centralny trik exo został więc potwierdzony przez producenta**.

> **Sprawdź sam #5 — jak exo wybiera układ.** Przeczytaj `src/exo/master/placement.py`, funkcja `place_instance`:
> ```bash
> gh api repos/exo-explore/exo/contents/src/exo/master/placement.py --jq .content | base64 -d | sed -n '1,120p'
> ```
> Szukaj `get_cycles`, filtrów pamięci i podzielności (`hidden_size % n`). *(Polecenie złożone z ścieżki w notatkach; nie uruchamiałem go.)*

---

## 8. Co z tego dla mnie

### 8.1 Na twoich Macach — co możesz wdrożyć dziś

Nie znam konfiguracji pamięci twoich Maców — to ona decyduje o wyborze. Reguła z §1: patrz na **GB/s i GB RAM**, nie na rdzenie.

| Jeśli… | to rozważ | Dlaczego / uwaga |
|---|---|---|
| chcesz po prostu uruchomić model na Macu i mieć szeroki wybór | **mlx-lm** (`mlx_lm.convert`, `mlx_lm.server`) | najszersza pokrywa modeli (137 architektur); modele w `mlx-community` |
| używasz agentów kodujących (Claude Code, OpenCode, Codex) i masz długie historie | **oMLX** | cache KV na SSD przeżywa restart, API Anthropic, przypinanie i TTL modeli, menu bar; pamiętaj o jednym opiekunie i łatkach |
| masz Maca z ≥ 96 GB (README ds4: „64 GB dla Qwen i 96 GB lub więcej") i chcesz DeepSeek V4 Flash lokalnie z dyskowym KV | **ds4** | silnik zbudowany pod tę klasę modeli (projekt nie publikuje porównań z innymi silnikami), ale beta, jeden model na proces, bez uwierzytelniania |
| masz dwa–cztery duże Maki połączone TB5 i chcesz większy model | **exo** (lub `mlx_lm.server --pipeline`) | pamiętaj: rurociąg = pojemność, nie szybkość; pełna siatka = 6 kabli dla 4 maszyn |
| potrzebujesz aplikacji z GUI i API | LM Studio, Ollama | patrz [`05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md`](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) — oba mają ścieżki MLX |

Praktyczne zasady, które wynikają z rozdziału:

1. **Zanim kupisz/wybierzesz Maca, policz sufit** z §1.4 dla modelu, którego chcesz używać; weź ~50–70% jako realistyczną szybkość.
2. **MoE z małą liczbą aktywnych parametrów** (jak DeepSeek V4 Flash: 13B z 284B) jest najlepszym dopasowaniem dla dużej pamięci i średniej przepustowości — liczy się RAM na całość, a przepustowość na aktywną część.
3. Przy agentach **zawsze włącz trwały cache prefiksu** (oMLX albo dyskowy KV w ds4) — to różnica między „agent czeka kilkadziesiąt sekund na każdy krok" a „czeka sekundy".
4. Przy dekodowaniu spekulatywnym **mierz na własnych promptach**: zysk zależy od treści (§5.8), a oba projekty (ds4, oMLX) przyznają, że bywa wolniej niż zwykłe dekodowanie.

### 8.2 Na twoim rigu AMD — uczciwie

Nic z tego rozdziału nie uruchomisz (ramka na początku). **Dlatego najcenniejsze są pomysły**, które możesz przenieść do **llama.cpp + llama-swap**. Mapowanie na to, co llama.cpp ma dzisiaj (rozdział 04; build 0ce8cd1 i stan z notatek):

| Pomysł z tego rozdziału | Gdzie jest w tym rozdziale | Odpowiednik w llama.cpp (z notatek) | Co możesz zrobić |
|---|---|---|---|
| **Warstwa SSD dla KV / trwałość cache** | oMLX §4.5, ds4 §5.7 | RAM-owy cache promptu `--cache-ram` (domyślnie 8192 MiB), `--cache-idle-slots`, punkty kontrolne kontekstu (`--ctx-checkpoints`, domyślnie 32), endpoint `/slots` do zapisu/odtworzenia stanu slotu | Zwiększ `--cache-ram`; rozważ zapis stanu slotu przez `/slots` do trwałej pamięci między restartami. Flagi `--slot-save-path` w notatkach nie potwierdzono — sprawdź w swoim buildzie. Nie ma wbudowanego poziomu SSD jak w oMLX. |
| **Stabilny format wywołań narzędzi, żeby prefiks pasował** | ds4 „powtórka ID narzędzi" §5.7 | dopasowanie najdłuższego wspólnego prefiksu przy wyborze slotu | Dopilnuj, żeby klient agentowy odsyłał historię **bajt w bajt** tak samo — każda zmiana serializacji JSON unieważnia prefiks. |
| **Ścieżki szybkie dla jednego modelu** | ds4 §5.2 | brak; llama.cpp jest generyczny | Możesz zbudować specyficzne ustawienia dla jednego modelu: tensor split, `-ot` (override tensor) dla ekspertów, pinowanie rozmiaru kontekstu (`-c` jawnie, bo `--fit` zmienia kontekst). |
| **Cache gorących ekspertów** | ds4 §5.6, oMLX §4.6 | nowy `src/llama-moe-cache.{h,cpp}` — „recently used experts of host-resident MoE layers in a device buffer" | Warto przejrzeć, kiedy będziesz trzymać MoE częściowo w RAM-ie. Przy 4 × 32 GB rezydentnie ci niepotrzebny. |
| **Dekodowanie spekulatywne natywne dla modelu** | ds4 DSpark/MTP §5.8, oMLX MTP/DFlash §4.7 | `common_speculative_type`: `DRAFT_MTP`, `DRAFT_DFLASH`, `DRAFT_DSPARK`, `DRAFT_EAGLE3` oraz warianty n-gram bez modelu (`NGRAM_*`, `examples/lookup`) | **To już robisz** (DSpark na rigu). Warianty n-gram „z promptu" nie wymagają osobnego modelu i mogą dawać zysk tam, gdzie agent cytuje własny kod — *moje przypuszczenie, zmierz*. Nie sprawdzałem, które z tych wariantów masz już włączone w przewodniku o przyspieszaniu. |
| **Asymetryczna kwantyzacja i imatrix na ekspertach** | ds4 §5.4, oQ §4.9 | `--tensor-type`/`-ot`, imatrix, kwantyzacje Unsloth Dynamic | Masz już UD-IQ3_XXS; możesz porównać z własnym przepisem „2-bit eksperci, Q8 reszta". |
| **Profile modelu (`model:profile`)** | oMLX §4.3 | `llama-swap` | Aliasuj ten sam model z różnymi presetami próbkowania per agent. |

Dodatkowa uwaga o architekturze, nie o silniku: **kompresowany KV z indekserem (§5.5)** to cecha *modelu* (DeepSeek V4), nie ds4 — korzystasz z niej także w llama.cpp, o ile ten implementuje ten typ uwagi. Dlatego przy doborze modeli do długich kontekstów agentowych liczy się architektura uwagi, a nie tylko liczba parametrów.

### 8.3 Czego nie robić

- Nie traktuj ds4 jako zamiennika llama.cpp na rigu: nie zbuduje się na gfx1201 bez łatek, a jedyny punkt danych to 2–5 tok/s na jednej karcie.
- Nie wystawiaj ds4 na sieć: brak uwierzytelniania; protokół TP nie ma szyfrowania.
- Nie przeceniaj liczb „projektu" (ds4, oMLX): to pomiary własne, na wybranych maszynach i promptach.

### 8.4 Podsumowanie rozdziału w pięciu zdaniach

1. Na Macu **GB/s decydują o tok/s**; M5 Ultra ma ok. 1,2 TB/s, ale M5 Ultra i tak daje sufit „tylko" ok. 117 tok/s dla MoE 13B aktywnych w 4 bitach (moje wyliczenie, @70%).
2. MLX to framework (jest backend Metal i CUDA, **nie ma HIP**), mlx-lm to LLM-y na nim, oMLX to serwer z cache KV na SSD, exo to klaster.
3. ds4/DwarfStar to świadomie wąski silnik w C: graf wpisany na sztywno per model, strumieniowanie ekspertów z SSD, dyskowy KV, DSpark/MTP.
4. Na twoim rigu (gfx1201) ds4 działa dziś tylko z niezmergowanymi łatkami i ze strumieniowaniem SSD (2–5 tok/s na jednej karcie); twoje ok. 50 tok/s w llama.cpp to **inny** układ (wagi rezydentne w 4 kartach), więc porównanie nie jest like-for-like.
5. Przenieś pomysły, nie kod: trwały cache prefiksu, stabilne wywołania narzędzi, spekulacja natywna dla modelu i asymetryczna kwantyzacja.

---

*Źródła tego rozdziału: patrz `07-APPLE-MLX-OMLX-I-DS4.md.sources.txt`. Pełna lista wszystkich źródeł kursu: [`ZRODLA.md`](ZRODLA.md). Dla kontekstu: [`01-MAPA-I-WARSTWY.md`](01-MAPA-I-WARSTWY.md), [`02-JAK-DZIALA-INFERENCJA.md`](02-JAK-DZIALA-INFERENCJA.md), [`03-KWANTYZACJA-I-FORMATY.md`](03-KWANTYZACJA-I-FORMATY.md), [`04-LLAMA-CPP-I-RODZINA-GGML.md`](04-LLAMA-CPP-I-RODZINA-GGML.md), [`09-POROWNANIE-I-WYBOR.md`](09-POROWNANIE-I-WYBOR.md), przewodnik [`../przyspieszanie-generowania/README.md`](../przyspieszanie-generowania/README.md).*
