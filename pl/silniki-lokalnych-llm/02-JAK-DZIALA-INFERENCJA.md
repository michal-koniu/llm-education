# 02 · Jak działa inferencja: od tokenu do tokenu

**Po co ten rozdział.** To fundament całego kursu. Każdy następny rozdział — o llama.cpp, Ollamie, vLLM, MLX, ds4 — opisuje, *jak dany program rozwiązuje któryś z problemów poznanych tutaj*: jak wyliczyć następny token, nie liczyć dwa razy tego samego, upchnąć wielu użytkowników w jednej karcie, rozdzielić model na cztery karty i zgadywać kilka tokenów naprzód. Po przeczytaniu będziesz umiał: prześledzić jedno żądanie od tekstu do tekstu i wskazać, gdzie ucieka czas i pamięć; policzyć na kartce, ile tokenów na sekundę *może* dać model na danym sprzęcie i dlaczego cztery karty R9700 rigu referencyjnego dają ~50, a nie ~500; policzyć rozmiar pamięci KV dla dowolnej architektury; wyjaśnić, czemu dla MoE „batchowanie jest za darmo" jest nieprawdą; obliczyć zysk z speculative decodingu; uczciwie porównać dwa runtime'y. Zakładam, że programujesz i znasz sprzęt, ale nie znasz „ML-owej" strony — wszystko jest wyjaśnione od zera.

> ⚠️ **Niczego tu nie uruchamiałem.** Cały przegląd to *desk research* i czytanie kodu: strony z abstraktami prac (arXiv), dokumentacja projektów, API GitHuba i kod sklonowany lokalnie (llama.cpp w wersji `0ce8cd1` — produkcyjnej — oraz vLLM, SGLang, mlx-lm, ds4, TensorRT-LLM). Żadnego benchmarku nie wykonałem, żadnego modelu nie załadowałem. Liczby oznaczone *(moje wyliczenie)* to arytmetyka na podanych danych — powtórzysz ją na kalkulatorze. Jedyne **pomiary** w tym rozdziale pochodzą z rigu referencyjnego, z katalogu [`../przyspieszanie-generowania/README.md`](../przyspieszanie-generowania/README.md).

**Znaczniki wiarygodności.** Fakt bez znacznika = sprawdzony w źródle pierwotnym (kod, dokument projektu, abstrakt; podaję ścieżkę lub numer arXiv). *(dane autorów)* / *(dane projektu)* / *(dane firmy)* = twierdzenie samego autora (np. liczba z abstraktu), bez niezależnej weryfikacji. *(źródło zewnętrzne)* = np. Wikipedia. *(niezweryfikowane)* = z pamięci lub wywnioskowane. *(moje wyliczenie)* = arytmetyka na zweryfikowanych lub jawnie wymienionych danych.

**Czego tu nie ma.** Formaty plików (GGUF, safetensors, MLX) i wszystko o kwantyzacji — to rozdział [`03-KWANTYZACJA-I-FORMATY.md`](03-KWANTYZACJA-I-FORMATY.md). Używam tu tylko jednej liczby z tamtego świata: *ile bajtów zajmuje jedna waga* (3 bity = 0,375 bajta), bo bez niej nie policzysz szybkości. Komendy w ramkach „Sprawdź sam" są tylko do odczytu; wzięte z notatek badawczych, nie uruchamiałem ich osobiście.

## Spis treści

1. [Podróż jednego żądania](#1-podróż-jednego-żądania)
2. [Prefill i dekodowanie; roofline na sprzęcie referencyjnym](#2-prefill-i-dekodowanie-roofline-na-sprzęcie-referencyjnym)
3. [Warianty uwagi (MHA, MQA, GQA, MLA…) i rozmiar KV](#3-warianty-uwagi-i-rozmiar-kv)
4. [Eksperci (MoE): dlaczego batchowanie nie jest za darmo](#4-eksperci-moe-dlaczego-batchowanie-nie-jest-za-darmo)
5. [Zarządzanie pamięcią KV](#5-zarządzanie-pamięcią-kv)
6. [Batchowanie generacji i czym naprawdę jest `--parallel`](#6-batchowanie-generacji-i-czym-naprawdę-jest---parallel)
7. [Jądra uwagi](#7-jądra-uwagi)
8. [Równoległość na wielu kartach i pomiar referencyjny](#8-równoległość-na-wielu-kartach-i-pomiar-referencyjny)
9. [Speculative decoding](#9-speculative-decoding)
10. [Próbkowanie](#10-próbkowanie)
11. [Gramatyka i wywoływanie narzędzi](#11-gramatyka-i-wywoływanie-narzędzi)
12. [Szablony czatu i parsery rozumowania](#12-szablony-czatu-i-parsery-rozumowania)
13. [Determinizm i numeryka](#13-determinizm-i-numeryka)
14. [Jak uczciwie mierzyć](#14-jak-uczciwie-mierzyć)
15. [Co z tego dla konfiguracji referencyjnej](#15-co-z-tego-dla-konfiguracji-referencyjnej) · 16. [Czego nie ustaliłem](#16-czego-nie-ustaliłem) · 17. [Słowniczek](#17-słowniczek)

Powiązane: [`01-MAPA-I-WARSTWY.md`](01-MAPA-I-WARSTWY.md) · [`04-LLAMA-CPP-I-RODZINA-GGML.md`](04-LLAMA-CPP-I-RODZINA-GGML.md) · [`06-SILNIKI-SERWEROWE-VLLM-SGLANG.md`](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) · [`07-APPLE-MLX-OMLX-I-DS4.md`](07-APPLE-MLX-OMLX-I-DS4.md) · [`09-POROWNANIE-I-WYBOR.md`](09-POROWNANIE-I-WYBOR.md) · [`ZRODLA.md`](ZRODLA.md).

---

## 1. Podróż jednego żądania

Model *decoder-only* (takie są wszystkie modele w tym kursie) definiuje jedną rzecz: **rozkład prawdopodobieństwa następnego tokenu, mając wszystkie poprzednie**. Generowanie to pętla: uruchom sieć na tokenach, których jeszcze nie przetworzyła, weź wynik z ostatniej pozycji, wybierz token, dołącz, powtórz.

```
 tekst: "Napisz funkcję sortującą"                       (UTF-8)
   │  1. TOKENIZER  (tekst -> identyfikatory; słownik V4-Flash: 129 280 pozycji)
   ▼
 [ t1  t2  t3  t4  t5 ]                                  n tokenów promptu
   │  2. OSADZENIE  (wiersz tablicy tok_embd[id] -> wektor długości d = 4096)
   ▼
 ┌──────────── powtórz × N warstw (V4-Flash: 43) ───────────────────────────┐
 │  RMSNorm                                                                  │
 │  UWAGA: Q,K,V = rzut(x); RoPE(Q,K); K,V -> do PAMIĘCI KV;                 │
 │         wynik = softmax(Q·Kᵀ)·V po wszystkich dotychczasowych pozycjach   │
 │  + resztkowe (x + wynik)                                                  │
 │  RMSNorm                                                                  │
 │  FFN (gęsta) albo MoE (router wybiera 6 z 256 ekspertów + 1 wspólny)      │
 │  + resztkowe                                                              │
 └───────────────────────────────────────────────────────────────────────────┘
   │  3. NORMA KOŃCOWA + lm_head ([d] -> [słownik]) — tylko dla pozycji,
   │     z których potrzeba wyniku (przy czytaniu promptu: tylko ostatniej)
   ▼
 LOGITY: 129 280 liczb („wynik” każdego możliwego następnego tokenu)
   │  4. ŁAŃCUCH SAMPLERÓW (kary, top-k, top-p, min-p, temperatura, losowanie;
   │     opcjonalnie maska gramatyki, budżet rozumowania)
   ▼
 token t6 ──► detokenizacja ──► strumień tekstu do klienta
   │
   └── dołącz t6 i wróć do kroku 2 — już tylko dla JEDNEGO nowego tokenu
```

- **Tokenizer** tnie tekst na kawałki ze stałego słownika. Model widzi identyfikatory, nie litery; „tok/s" to więc jednostka modelu, nie ludzkiego tekstu (ile tokenów na polskie słowo — nie mierzyłem).
- **Warstwa** (*pre-norm*): normalizacja → uwaga → dodanie do wejścia → normalizacja → FFN lub eksperci → dodanie do wejścia. Model = tablica osadzeń + N warstw + norma końcowa + `lm_head`. W llama.cpp każda architektura to osobny graf ggml w `src/models/*.cpp` (165 plików w tym buildzie; m.in. `qwen3moe.cpp`, `deepseek2.cpp`, `deepseek4.cpp`), złożony ze wspólnych klocków w `src/llama-graph.cpp` (`build_attn*`, `build_ffn`, `build_moe_ffn`).
- **Uwaga** to jedyne miejsce, w którym token „patrzy" na inne tokeny. Żeby nie przeliczać cudzych K i V w każdym kroku, zapisuje się je w **pamięci podręcznej KV** (*KV cache*) — jej poświęcona jest większość rozdziału.
- **Sampler** to jedyne miejsce losowości i jedyne, gdzie intensywnie pracuje CPU (§10, §11). Reszta to mnożenie macierzy na GPU.

Trzy wnioski: (1) generowanie jest **sekwencyjne** (*autoregresywne*) — token t+1 zależy od t, więc można go przyspieszyć tylko przez *zgadywanie* i sprawdzanie (§9); (2) **czytanie promptu da się zrównoleglić**, bo wszystkie jego tokeny są znane — stąd różnica prefill/dekodowanie (§2); (3) **jedyny stan rosnący z długością rozmowy to pamięć KV** (§3, §5).

W kodzie oba tryby to jedna funkcja `llama_decode`. Serwer llama.cpp (`tools/server/server-context.cpp`, `update_slots()`) w każdej iteracji buduje **jeden** batch: po jednym tokenie od każdego slotu, który generuje, a resztę `n_batch` wypełnia tokenami promptu slotów, które jeszcze czytają. vLLM mówi to w komentarzu w `vllm/v1/core/sched/scheduler.py`: „There's no 'decoding phase' nor 'prefill phase' in the scheduler. Each request just has the num_computed_tokens and num_tokens_with_spec…".

> **Sprawdź sam (1)**
> ```bash
> grep -n "batch.size() < n_batch" ~/llama.cpp-0ce8cd1/tools/server/server-context.cpp
> sed -n 620,631p ~/runtimes-src/vllm/vllm/v1/core/sched/scheduler.py
> ls ~/llama.cpp-0ce8cd1/src/models | wc -l          # notatki: 165
> ```
> Numery wierszy mogą się lekko różnić — szukaj po frazie.

---

## 2. Prefill i dekodowanie; roofline na sprzęcie referencyjnym

### 2.1 Dwa tryby tej samej sieci

- **Prefill** (*prompt processing*, pp): wszystkie n tokenów promptu naraz. Mnożenia macierz × macierz (GEMM): wagi czytane z pamięci **raz**, użyte n razy. Praca ≈ 2 FLOP × aktywne parametry × n. Przy n rzędu setek tokenów jest **ograniczona mocą obliczeniową** (*compute-bound*).
- **Dekodowanie** (*decode*, *token generation*, tg): jeden nowy token na sekwencję na krok. Mnożenia macierz × wektor (GEMV): każdy bajt wag wczytany z VRAM-u służy do **2 operacji** (jedno mnożenie z dodawaniem) na sekwencję w batchu. Jest **ograniczone przepustowością pamięci** (*memory-bound*).

Analogia: prefill to kucharz, który raz sięga do spiżarni po składniki na sto porcji; dekodowanie to kucharz, który po każdą porcję chodzi do spiżarni od nowa. Precyzyjnie: czas kroku dekodowania to głównie *czas wczytania wag*.

> **Wniosek, na którym stoi cały kurs:** skoro koszt kroku to głównie czytanie wag, to sprawdzenie **kilku tokenów naraz kosztuje niewiele więcej niż jednego**. Na tym stoi i batchowanie użytkowników, i speculative decoding. (Z poprawką dla MoE — §4.)

### 2.2 Roofline

Osiągalna szybkość jądra = min(szczyt FLOPS, intensywność arytmetyczna × przepustowość pamięci); intensywność AI = FLOP / bajty z pamięci. **Punkt załamania** AI\* = szczyt FLOPS / przepustowość: poniżej jądro jest ograniczone pamięcią, powyżej — obliczeniami. (Model: Williams, Waterman, Patterson 2009 *(z pamięci, niezweryfikowane)*. Dla LLM najlepsze źródło to Pope i in., arXiv 2211.05102: PaLM-540B — 29 ms/token przy małym batchu z wagami int8 i 76% MFU przy dużym *(dane autorów)*.)

Dla wag po *b* bajtów (FP16: 2; 8 bitów: ~1; 4 bity: 0,5; 3 bity: 0,375) krok dekodowania z B sekwencjami wykonuje 2B FLOP na wagę i czyta b bajtów, więc **AI = 2B/b**, a batch w punkcie załamania **B\* = AI\* × b / 2** *(moje wyliczenie)*.

### 2.3 Karta referencyjna — co o niej wiemy

| Fakt | Wartość | Stan wiedzy |
|---|---|---|
| GPU | AMD Radeon AI PRO R9700, cel `gfx1201`, RDNA4 | zweryfikowane: `rocminfo`, tabela architektur w dokumentacji ROCm |
| VRAM | 34 208 743 424 B = 31,86 GiB na kartę | zweryfikowane: `/sys/class/drm/card*/device/mem_info_vram_total` (4 karty) |
| Jednostki / cache | 64 CU, 8 MiB L2, 64 MiB Infinity Cache | zweryfikowane: dokumentacja ROCm |
| Zegar pamięci | stany 96…1258 MHz | zweryfikowane: `pp_dpm_mclk` |
| **Przepustowość pamięci** | **~640 GB/s** (256-bit GDDR6, ~20 Gbps) | **źródło zewnętrzne + wyliczenie**: Wikipedia o serii RX 9000 podaje „do 640 GB/s zależnie od modelu"; 1258 MHz × 16 = 20,1 Gbps zgadza się z 20 Gbps GDDR6 *(mnożnik ×16 niezweryfikowany)*. **Strony AMD nie udało się pobrać.** |
| Szczyt FP16 | ~96 TFLOPS gęsto | *(niezweryfikowane)* — z pamięci; traktuj jako parametr |
| Łącze z hostem | sysfs: 32 GT/s (PCIe 5.0), x16 na wszystkich czterech | zweryfikowany odczyt — **ale** patrz niżej |
| Karta–karta | tylko PCIe (brak XGMI na kartach RDNA4) | *(niezweryfikowane)* |

**Uwaga o PCIe.** CPU to Ryzen 7 9700X (z `rocminfo`), ma ok. 28 użytecznych linii PCIe, więc cztery prawdziwe łącza x16 Gen5 są niemożliwe *(niezweryfikowane)*. Dziennik wdrożenia w przyspieszanie-generowania mówi wprost, że **karty 1 i 3 pracują na x4** ([`../przyspieszanie-generowania/01-JAK-TO-DZIALA.md`](../przyspieszanie-generowania/01-JAK-TO-DZIALA.md)). Źródła się nie zgadzają — zaufaj własnej obserwacji i potwierdź przez `lspci -vv` (`LnkSta`). Szczyt PCIe 5.0 x16 ≈ 32 GT/s × 16 × 128/130 / 8 = **63 GB/s na kierunek**; 4.0 x16 = 31,5 GB/s *(moje wyliczenie)*.

### 2.4 Punkt załamania na karcie referencyjnej

Przy 96 TFLOPS i 640 GB/s: **AI\* = 150 FLOP/B** *(wyliczenie z danych niezweryfikowanych)*. Stąd B\*: FP16 → 150; 8 bitów → 75; 4 bity → 38; 3 bity → 28 *(moje wyliczenie)*. Im mniej bitów, tym mniej tokenów trzeba, by nasycić obliczenia — ale prawdziwe jądra rozpakowują wagi w ALU albo używają iloczynów INT8 (ścieżka MMQ w llama.cpp), więc faktyczny punkt jest wyżej; to dolne ograniczenia.

**Wniosek dla modelu gęstego:** dopóki B < B\*, krok kosztuje prawie tyle samo dla 1 i dla B sekwencji, więc **batchowanie to prawie darmowa przepustowość**. Dlatego serwery batchują, a silniki „na jednego użytkownika" wyglądają na wolne: siedzą daleko po lewej stronie wykresu roofline.

### 2.5 Przykład A — model gęsty 13B przy 3 bitach

Bajty na token = 13e9 × 3/8 = **4,875 GB**. Przy 640 GB/s sufit to **131 tok/s na kartę** przy 100% przepustowości *(moje wyliczenie)*. Prawdziwe jądra osiągają ułamek (zwykle 60–80% *(niezweryfikowane)*; zmierz `llama-bench -p 0 -n 128`). Dochodzi czytanie KV (§3).

### 2.6 Przykład B — klasa referencyjna: DeepSeek-V4-Flash

Dane z `config.json` i karty modelu `deepseek-ai/DeepSeek-V4-Flash` (zweryfikowane): 43 warstwy, ukryty wymiar 4096, **256 ekspertów routowanych + 1 wspólny, 6 na token**, `moe_intermediate_size` 2048, 64 głowice, `num_key_value_heads` 1, `head_dim` 512, okno 128, kontekst 1 048 576, słownik 129 280, eksperci w FP4, reszta FP8; „284 mld parametrów (13 mld aktywnych)".

**Gdzie mieszkają te 13 mld?** *(moje wyliczenie)* Ekspert (SwiGLU, 3 macierze): 3 × 4096 × 2048 = 25,17 mln. Eksperci routowani: 256 × 43 × 25,17 mln = **277,0 mld**. Reszta (uwaga, wspólni, osadzenia, `lm_head`, router) = 284 − 277 = **~7,0 mld**. Aktywne na token: 7,0 + 6/256 × 277,0 = **13,5 mld** — zgadza się z reklamowanymi 13 mld, co potwierdza podział. **Mniej więcej połowa ruchu wag na token to zawsze czytane wagi gęste i wspólne, połowa to 6 ekspertów na warstwę.**

Przy jednolitych 3 bitach (zastępnik; prawdziwe kwantyzacje są mieszane — rozdział 03): gęste 7,0 mld × 0,375 = 2,6 GB + aktywni eksperci 277 mld × 6/256 × 0,375 = 2,4 GB ≈ **5,1 GB na token**; sufit jednej karty: 640 / 5,1 ≈ **126 tok/s** *(pomijam KV i aktywacje)*.

**Co dają cztery karty.** Przy `--split-mode layer` token wędruje przez karty po kolei, więc w danej chwili „pracuje" przepustowość jednej karty: ten sam sufit ~126 tok/s. Karty kupiły **pojemność** (106,5 GB wag przy 3 bpw nie mieści się w 32 GB). Przy idealnym podziale tensorowym przepustowości się sumują: 4 × 640 = 2560 GB/s ⇒ ~506 tok/s, minus komunikacja (§8).

**Prefill:** FLOP na token ≈ 2 × 13,5 mld = **~27 GFLOP**; przy 96 TFLOPS × 40% *(oba wejścia niezweryfikowane)* ~1 400 tok/s na kartę, ~5 700 przy czterech zajętych. Prefill referencyjny: ~960 → ~700 tok/s po przejściu na wdrożoną konfigurację ([`../przyspieszanie-generowania/README.md`](../przyspieszanie-generowania/README.md)) — daleko poniżej tego sufitu; nie wiem dlaczego *(niezweryfikowane)*.

**KV to druga połowa ruchu w dekodowaniu:** każdy krok czyta też całą pamięć KV wszystkich sekwencji w batchu. KV Llamy-3.1-70B przy 128K (40 GiB, §3) jest większe niż jej wagi w 4 bitach — dlatego istnieją MQA/GQA/MLA i uwaga rzadka.

> **Sprawdź sam (2)**
> ```bash
> cat /sys/class/drm/card*/device/mem_info_vram_total      # 34 208 743 424 B (notatki)
> cat /sys/class/drm/card*/device/pp_dpm_mclk              # najwyższy stan: 1258 MHz
> cat /sys/class/drm/card*/device/current_link_speed /sys/class/drm/card*/device/current_link_width
> lspci -vv | grep -E "VGA|Display|LnkSta:"                # (root) porównaj z "karty 1 i 3 na x4"
> ```
> Ćwiczenie rachunkowe: sufit tok/s = `przepustowość [GB/s] / (aktywne parametry [mld] × bity / 8)`. Policz go dla gęstego 70B w 4 bitach (35 GB wag — ile kart, i co to znaczy dla szybkości przy podziale warstwami?). Pomiar (nie uruchamiałem; **karty są produkcyjne** — zatrzymaj `llama-swap` albo użyj małego modelu): `llama-bench -p 0 -n 128` (czyste dekodowanie), `llama-bench -d N` (wstępnie wypełnia N tokenów kontekstu).

---

## 3. Warianty uwagi i rozmiar KV

Klocki warstwy w skrócie: **RMSNorm** (Zhang i Sennrich, NeurIPS 2019: normalizacja bez odejmowania średniej; „7%–64%" szybsza od LayerNorm *(dane autorów)*), **SwiGLU** FFN: y = W_down(SiLU(W_gate·x) ⊙ (W_up·x)) — trzy macierze (Shazeer, arXiv 2002.05202), **RoPE** (poniżej). W każdej warstwie każdy token produkuje klucz K i wartość V; pamięć KV trzyma je dla wszystkich dotychczasowych tokenów. Dla MHA/MQA/GQA:

> **bajty KV na token = 2 (K i V) × n_warstw × n_głowic_KV × head_dim × bajty_na_element**

(w llama.cpp: `n_embd_k_gqa(il)` / `n_embd_v_gqa(il)`, tensory KV o kształcie `[n_embd_k_gqa, kv_size, n_stream]` — `src/llama-kv-cache.cpp`).

| wariant | pomysł | źródło |
|---|---|---|
| **MHA** | tyle głowic K/V, ile zapytań | Vaswani i in. 2017 *(niezweryfikowane)* |
| **MQA** | **jedna** głowica K/V dla wszystkich zapytań; Shazeer, arXiv 1911.02150: dekodowanie jest wolne przez „koszt przepustowości pamięci przy wielokrotnym ładowaniu dużych tensorów kluczy i wartości" | abstrakt |
| **GQA** | n_kv między 1 a n_głowic; Ainslie i in., arXiv 2305.13245; istniejące MHA można przerobić „uptrainingiem" za 5% kosztu pretreningu *(dane autorów)* | abstrakt |
| **MLA** | cache trzyma **niskowymiarowy wektor ukryty** (`kv_lora_rank`) + mały osobny klucz RoPE; K i V odtwarzane z wektora lub „wchłaniane" w mnożenia *(wchłanianie — niezweryfikowane)*. DeepSeek-V2, arXiv 2405.04434: **KV mniejsze o 93,3%**, 5,76× większa przepustowość niż DeepSeek 67B *(dane autorów)* | abstrakt |
| **DSA** | „błyskawiczny indekser" ocenia poprzednie tokeny; pełna uwaga tylko po top-k; DeepSeek-V3.2, arXiv 2512.02556 | abstrakt (mechanizm indeksera — niezweryfikowany) |
| **CSA / HCA** (V4) | surowe okno 128 tokenów + wiersze KV skompresowane w czasie: na warstwach parzystych ≥2 jeden wiersz na 4 tokeny (indekser wybiera do 512), na nieparzystych ≥3 jeden na 128; warstwy 0–1 tylko okno | `MODEL_CARD.md` ds4 + `config.json` (`compress_ratios`, `index_topk` 512, `sliding_window` 128) |

llama.cpp ma dla nich osobne klasy pamięci (`src/`): `llama-kv-cache.cpp` (dla MLA `has_v = !is_mla` — **brak tensora V**), `llama-kv-cache-iswa.cpp` (dwa cache'e: pełny i okienkowy), `llama-kv-cache-dsa*.cpp`, `llama-kv-cache-dsv4.cpp`, `llama-memory-recurrent.cpp` (SSM/RWKV), `llama-memory-hybrid*.cpp`.

### 3.1 Rozmiary KV z liczbami (cache FP16/BF16, 2 B na element)

Konfiguracje z `config.json` na Hugging Face (Llama przez lustro NousResearch — oficjalne repozytorium jest zamknięte).

| model | dane wejściowe | bajtów na token | przy 128K |
|---|---|---|---|
| Llama-3.1-70B (GQA) | 80 warstw, 8 głowic KV, head_dim 128 | 2×80×8×128×2 = **327 680 B = 320 KiB** | **40 GiB** |
| ta sama jako MHA (64 głowice KV) | | 2,5 MiB | 320 GiB (8×) |
| Qwen3-30B-A3B (GQA) | 48 warstw, 4 głowice KV, head_dim 128 | **96 KiB** | 12 GiB (natywny max 40 960 ⇒ 3,75 GiB) |
| gpt-oss-120b (GQA + SWA) | 36 warstw naprzemiennie okno(128)/pełne, 8 głowic KV, head_dim 64 | pełne warstwy: 18×8×64×2×2 = **36 KiB** (+ stałe okno 128 tokenów) | ~4,5 GiB *(moje wyliczenie)* |
| DeepSeek-V3 (MLA) | 61 warstw, `kv_lora_rank` 512, `qk_rope_head_dim` 64 | 61×(512+64)×2 = **70 272 B = 68,6 KiB** | 8,6 GiB |
| ta sama jako MHA | 128 głowic × (192+128) × 2 B × 61 | 5,0 MB | 71× MLA *(moje wyliczenie)* |
| DeepSeek-V4-Flash (CSA/HCA) | uśrednione: (21/4 + 20/128) = 5,41 wiersza × 512 × 2 B + indekser 21/4 × 128 × 2 B (zakłada wspólny wiersz K=V, FP16, bez okna) | **~6,9 KB** | ~1M tokenów ≈ 6,4–6,7 GiB (zależnie, czy „1M" to 10⁶, czy 2²⁰) *(moje wyliczenie; założenia niezweryfikowane)* |

Kontrola: 6,9 KB to ~10% MLA z V3, co zgadza się z deklaracją karty modelu „10% KV względem V3.2 przy 1M" *(dane firmy)* (V3.2 trzyma też cache indeksera, więc zgodność przybliżona).

**Jak z tego korzystać.** Weź z `config.json` liczbę warstw, głowic KV i `head_dim` (albo `kv_lora_rank` + `qk_rope_head_dim` dla MLA), policz, podziel wolny VRAM po wagach przez wynik — masz górną granicę tokenów kontekstu na wszystkie sloty razem. Na rigu referencyjnym KV jednej sekwencji 131 072 tokenów to rzędu 0,9 GB *(moje wyliczenie, założenia jak w tabeli)* — ułamek wag. A jednak w dzienniku przy 4 slotach × 131 072 było `cudaMalloc failed: out of memory`: na karcie siedzą jeszcze bufory obliczeniowe (zależne od `--ubatch-size`) i ~4 GB na kartę na draft ([`02-WDROZENIE-DEEPSEEK.md`](../przyspieszanie-generowania/02-WDROZENIE-DEEPSEEK.md)).

### 3.2 RoPE — krótko, bo ma skutki dla KV

RoPE (Su i in., arXiv 2104.09864) obraca pary współrzędnych Q i K o kąt zależny od pozycji, więc iloczyn zależy tylko od odległości względnej. Skutki: RoPE jest stosowane do K **przed** zapisem do cache, więc zapisane klucze „pamiętają" pozycję bezwzględną; przesunięcie cache (*context shift*) wymaga ponownego obrócenia kluczy — `seq_add` (K-shift) bramkowane przez `get_can_shift()` w `llama-kv-cache.cpp`, dlatego context shift nie działa dla każdej architektury ani przy promptach multimodalnych. Rozszerzanie kontekstu: skalowanie liniowe, **YaRN** (arXiv 2309.00071: „10× mniej tokenów i 2,5× mniej kroków" *(dane autorów)*), LongRoPE (`LLAMA_ROPE_SCALING_TYPE_*` w `llama.h`); DeepSeek-V3 używa YaRN z czynnikiem 40, V4 — 16 (`config.json`). MLA trzyma osobną małą część klucza z RoPE właśnie po to, by wektor ukryty mógł pozostać „bez pozycji".

> **Sprawdź sam (3)**
> ```bash
> grep -n "is_mla\|has_v" ~/llama.cpp-0ce8cd1/src/llama-kv-cache.cpp | head      # MLA => brak tensora V
> ls ~/llama.cpp-0ce8cd1/src | grep -E "kv-cache|memory"
> ```
> Ćwiczenie rachunkowe: pobierz `config.json` modelu ze swojego `llama-swap`, policz bajty KV na token ze wzoru wyżej dla dwóch rozmiarów kontekstu i porównaj z wolnym VRAM-em z pętli pomiarowej w `../przyspieszanie-generowania/narzedzia/`.

---

## 4. Eksperci (MoE): dlaczego batchowanie nie jest za darmo

### 4.1 Routing

W **MoE** (*mixture of experts*) gęsty FFN zastąpiono wieloma małymi („ekspertami"). **Router** (jedna mała warstwa liniowa: `logits = W_gate·x`) ocenia ekspertów, token trafia do top-k, wyniki są ważone i sumowane; **eksperci wspólni** działają zawsze (pomysł DeepSeekMoE, arXiv 2401.06066: model 16B ~ LLaMA2-7B przy ~40% obliczeń *(dane autorów)*; Mixtral, arXiv 2401.04088: 8 ekspertów, top-2, 47 mld łącznie / 13 mld aktywnych *(dane autorów)*).

Kod: `llm_graph_context::build_moe_ffn` (`src/llama-graph.cpp`). Kroki: (1) funkcja bramkująca — softmax, sigmoid lub **sqrt-softplus** (`scoring_func: sqrtsoftplus` w V4); (2) opcjonalne **obciążenie wyboru** `exp_probs_b`, dodawane *tylko do wyboru* (równoważenie bez straty pomocniczej z DeepSeek-V3, arXiv 2412.19437); (3) opcjonalnie najpierw najlepsze grupy (`n_expert_groups`, `n_group_used`); (4) `ggml_argsort_top_k`; (5) wagi nieobciążone, renormalizacja (`norm_w`) i skala (`w_scale`; `routed_scaling_factor` 1,5 w V4); (6) `ggml_mul_mat_id` — zgrupowane GEMM tylko dla wybranych ekspertów. Dla CUDA/HIP jest fuzyjne bramkowanie (`ggml-cuda/topk-moe.cu`). llama.cpp ma też **hostowy cache ekspertów** (`src/llama-moe-cache.{h,cpp}`: trzyma często używanych ekspertów warstw rezydujących w RAM-ie hosta w buforze na urządzeniu) — dzięki niemu modele większe niż VRAM są znośne.

**Konsekwencja:** parametry *łączne* decydują o **pojemności** (VRAM), *aktywne* o **bajtach na token** (szybkości), a liczba *różnych* ekspertów dotkniętych w jednym kroku — o tym, ile kosztuje batchowanie i spekulacja.

### 4.2 Obliczenie: ile ekspertów dotyka batch

Przy B tokenach w kroku i **jednostajnym, niezależnym routingu** *(założenie upraszczające)* ułamek dotkniętych ekspertów w warstwie:

> **f(B) = 1 − (1 − 6/256)^B**

Bajty w kroku = gęste (~2,6 GB) + 277 mld × 0,375 B × f(B). Przy 640 GB/s jednej karty i 3 bpw *(wszystko: moje wyliczenie; bez KV i aktywacji, 100% przepustowości)*:

| batch B | eksperci dotknięci | GB / krok | czas kroku | zbiorcze tok/s | bajtów na token vs B=1 |
|---|---|---|---|---|---|
| 1 | 2,3% | 5,1 | 7,9 ms | 126 | 1,00× |
| 4 | 9,1% | 12,0 | 18,8 ms | 213 | 0,59× |
| 8 | 17,3% | 20,6 | 32,2 ms | 249 | 0,51× |
| **32** | **53,2%** | 57,9 | 90,4 ms | 354 | 0,36× |
| 128 | 95,2% | 101,5 | 158,6 ms | 807 | 0,16× |
| 512 | 100% | 106,5 | 166,4 ms | 3077 | 0,04× |

Wiersz B = 32 w głowie: (1 − 6/256)^32 ≈ 0,468 ⇒ dotkniętych 53,2% ekspertów ⇒ 0,532 × 277 mld × 0,375 B ≈ 55 GB + 2,6 GB gęstych = 57,9 GB. Model **gęsty** o tych samych 13 mld aktywnych czytałby wciąż ~5 GB.

1. **Dla MoE „batchowanie jest za darmo" jest fałszem, dopóki prawie wszyscy eksperci nie są obecni w kroku.** Przy B = 32 na eksperta przypada średnio 0,75 tokenu (B × 6/256). Punkt załamania dla *ekspertowych* GEMM leży przy B ≈ 28 × 256/6 ≈ **1200 tokenów**, nie 28 *(moje wyliczenie)*. Realny routing jest skośny („gorący" eksperci), więc prawdziwy ruch jest niższy *(niezweryfikowane)*.
2. **Speculative decoding na MoE jest karane**: weryfikacja n tokenów czyta 1,47× (n=2), 1,93× (3), 2,38× (4), 2,82× (5), 3,25× (6), 4,07× (8) bajtów jednego tokenu *(moje wyliczenie)*. PR DFlash do llama.cpp mówi to dla gpt-oss: przyspieszenie „jest zwykle mniejsze niż dla celów z gęstą uwagą, bo podczas równoległej weryfikacji aktywuje się więcej ekspertów niż przy dekodowaniu jednotokenowym" (ggml-org/llama.cpp#22105). Tabela zysku netto: §9.3.

### 4.3 Co to znaczy na rigu referencyjnym

Dwa agenty zamiast jednego (konfiguracja wdrożona, 2 sloty): po 34,5 tok/s, razem **63**, wobec 49,7 dla jednego ([`README.md`](../przyspieszanie-generowania/README.md)); przy 4 agentach (2 sloty + kolejka) razem 60. Drugi agent dołożył ~27% przepustowości zbiorczej, nie +100% — *sublinearnie*, jak w tabeli (przy jednostajnym routingu i bez spekulacji B = 2 daje 1,37×; na rigu referencyjnym każdy slot już weryfikuje 4 tokeny na krok, więc dwa sloty to 8 — porównanie rzędów wielkości, nie dowód *(niezweryfikowane)*). A speculative decoding dał ci 1,5–1,6× (§8.4) — więcej, niż wynika z rachunku MoE dla jednostajnego routingu (§9.3: 1,2–1,45×). Możliwe wyjaśnienia: skorelowany routing sąsiednich tokenów albo wysoka trafność draftu; **nie sprawdzałem, które**.

> **Sprawdź sam (4)**
> ```bash
> grep -n "build_moe_ffn\|argsort_top_k\|exp_probs_b\|n_group_used" ~/llama.cpp-0ce8cd1/src/llama-graph.cpp | head -20
> head -40 ~/llama.cpp-0ce8cd1/src/llama-moe-cache.h
> ```
> Ćwiczenie: w Pythonie policz f(B) = 1 − (1 − k/E)^B dla Mixtrala (k=2, E=8) i dla Qwen3-30B-A3B (**liczby k i E weź z jego `config.json` — nie ma ich w moich notatkach**). Przy jakim B Mixtral dotyka 90% ekspertów? Dlaczego mało-ekspertowe MoE są mniej „karane" przez batchowanie niż drobnoziarniste (DeepSeek)?

---

## 5. Zarządzanie pamięcią KV

KV to jedyny stan żądania, który rośnie. Problemy: fragmentacja, współdzielenie, usuwanie, okna i kompresja, przenoszenie do tańszych pamięci.

### 5.1 Ciągły plaster kontra stronicowanie

Naiwnie: rezerwuj max_len × bajty_na_token ciągłego miejsca na żądanie — fragmentacja i nadmierna rezerwacja. **PagedAttention** (Kwon i in., SOSP 2023, arXiv 2309.06180): KV w blokach, mapowanych tablicą bloków — jak pamięć wirtualna; „niemal zerowe straty", **2–4×** większa przepustowość niż FasterTransformer i Orca przy tym samym opóźnieniu *(dane autorów)*. Kod vLLM: `vllm/v1/core/kv_cache_manager.py`, `block_pool.py`, `kv_cache_utils.py`; `DEFAULT_BLOCK_SIZE = 16` tokenów (`vllm/config/cache.py`).

### 5.2 Prefix caching — dźwignia nr 1 dla agentów

Początek promptu (system, schematy narzędzi, historia) wraca w każdej turze; ponowne użycie jego KV skraca TTFT.

- **vLLM**: łańcuch haszy — każdy *pełny* blok dostaje hasz (poprzedni hasz, tokeny bloku, klucze dodatkowe jak LoRA); zwolnione bloki zostają na liście LRU; domyślnie włączone (`enable_prefix_caching = True`), hasz `sha256`; trafienia z ziarnistością bloku (16 tokenów).
- **SGLang RadixAttention** (arXiv 2312.07104: „do 6,4×" *(dane autorów)*): **drzewo radix** po sekwencjach tokenów (`mem_cache/radix_cache.py`: `RadixKey`, `TreeNode` z `lock_ref`, `last_access_time`, `hit_count`; `match_prefix`, podział węzła przy częściowym dopasowaniu, wypieranie LRU/priorytetowe). Wielu agentów ze wspólnym prefiksem i różnymi końcówkami trafia w cache; scheduler jest cache-aware (polityki `lpm`, `dfs-weight`, `fcfs`, `lof` w `managers/schedule_policy.py`).
- **llama.cpp**: `--slot-prompt-similarity` (wybór wolnego slotu o najdłuższym wspólnym prefiksie), `--cache-reuse N` (fragmenty ≥N tokenów dopasowane *gdziekolwiek* w starym prompcie, przesuwane przez `seq_add`), **cache promptów w RAM-ie** `--cache-ram MiB` (domyślnie 8192; wolne sloty zapisywane, gdy `--cache-idle-slots`, domyślnie włączone), `--ctx-checkpoints N` (domyślnie 32; punkty kontrolne wymagane przez modele z SWA i rekurencyjne, bo ich stanu nie da się przyciąć token po tokenie). Wartości z `common/common.h`, `common/arg.cpp`.
- **MLX-LM**: `PromptTrie` + `LRUPromptCache` (`mlx_lm/models/cache.py`, `--prompt-cache-size`). **ds4**: migawki KV prefiksu **na dysku** (`--kv-disk-dir`, `--kv-disk-space-mb`; „pliki zawierają tekst promptu i stan modelu: traktuj katalog jako wrażliwy").

### 5.3 Okna, kompresja, stan rekurencyjny

- **SWA**: warstwa patrzy tylko na ostatnie W tokenów, więc jej cache to bufor pierścieniowy (gpt-oss: W = 128 na co drugiej warstwie). llama.cpp: pełny cache dla warstw globalnych i mały dla SWA; `--swa-full` wymusza pełny. Cena: cache SWA nie da się tanio „cofnąć" — stąd checkpointy z §5.2. MLX: `RotatingKVCache(max_size, keep=0)` — nadpisuje najstarsze wpisy, może przypiąć pierwsze `keep` tokenów.
- **Kompresja** (DSA, CSA/HCA): §3. **Warstwy rekurencyjne** (Mamba, Qwen3-Next „gated delta net", RWKV): stały rozmiar stanu na sekwencję zamiast KV na token; stan „nie rozkłada się po pozycjach", więc cofanie przy spekulacji wymaga migawek (tekst PR #22105).

### 5.4 Czym naprawdę są „slot" i „zunifikowane KV" w llama.cpp (zweryfikowane)

- Magazyn KV to tablica **komórek**; każda trzyma (pozycja, zbiór id sekwencji). `llama_kv_cache::find_slot` wybiera komórki dla mikro-batcha, `seq_rm/seq_cp/seq_keep/seq_add` edytują metadane, maska uwagi powstaje z pozycji i przynależności. **Nie ma tablicy bloków**, jest indeks komórki na token — pamięć odporna na fragmentację, choć jądra widzą zamaskowane ciągłe okno.
- **`n_stream`**: przy `kv_unified = false` tensor KV ma kształt `[n_embd_kv, kv_size, n_stream]` z `n_stream == n_seq_max` — **każda sekwencja ma prywatny strumień `n_ctx / n_seq_max` komórek**. Przy `kv_unified = true` jest jeden strumień i wszystkie sekwencje dzielą całą pulę `n_ctx`.
- W tym buildzie `-np` to domyślnie **auto**: „using n_parallel = 4 and kv_unified = true" (`tools/server/server.cpp`). `--cont-batching` domyślnie włączone.
- **Context shift** (`--context-shift`, domyślnie *wyłączone*): po dojściu slotu do `n_ctx` zachowaj `n_keep` pierwszych tokenów, odrzuć `n_discard` (domyślnie połowę reszty), `seq_rm` + `seq_add(−n_discard)` — stratne okno przesuwne, które ponownie obraca klucze. Przy wyłączonym żądanie kończy się na limicie.

### 5.5 KV w mniejszej liczbie bitów i offload

llama.cpp: `-ctk/-ctv` domyślnie `f16`; dozwolone `f32, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1`; **skwantyzowane V wymaga flash attention**; **podział tensorowy wymaga nieskwantyzowanego KV** (`docs/multi-gpu.md`) — twoje ograniczenie, bo w konfiguracji wdrożonej jest f16. Podstawa badawcza: KIVI (arXiv 2402.02750; 2 bity, 2,6× mniej pamięci szczytowej *(dane autorów)*). Reszta o kwantyzacji — rozdział 03. Offload: vLLM ma konektory KV (LMCache, NIXL, Mooncake i in.) oraz katalogi `kv_offload`; LMCache (arXiv 2510.09665): „do 15×" z vLLM *(dane autorów)*; SGLang HiCache — znam nazwy plików, semantyki nie sprawdziłem. Dla jednego użytkownika liczą się `--cache-ram` i dysk ds4. (Nie myl z hostowym cache *ekspertów* z §4.1 — tamten trzyma wagi, ten KV.)

| mechanizm | llama.cpp (`0ce8cd1`) | vLLM | SGLang | mlx-lm | ds4 |
|---|---|---|---|---|---|
| układ KV | komórki; strumienie lub pula zunifikowana | bloki po 16 | strony + drzewo radix | cache per warstwa, wzrost krokami 256 | własny (V4: stan kompresora) |
| prefiks | najlepszy slot, `--cache-reuse`, cache w RAM | łańcuch haszy, domyślnie | drzewo radix | `PromptTrie` + LRU | migawki na dysku |
| okno / kompresja | iSWA, DSA, DSV4 | typy cache per warstwa | backendy V4 | `RotatingKVCache` | natywne CSA/HCA |
| KV w mniej bitach | `-ctk/-ctv` | FP8, backendy turbo/ultraquant (znam nazwy) | *nie ustaliłem* | `QuantizedKVCache` | *nie ustaliłem* |
| offload | `--cache-ram`; cache ekspertów | konektory, cpu/disk | HiCache | *nie ustaliłem* | dysk |

> **Sprawdź sam (5)**
> ```bash
> grep -n "cache_ram_mib\|cache_idle_slots\|n_ctx_checkpoints\|ctx_shift" ~/llama.cpp-0ce8cd1/common/common.h
> sed -n 160,175p ~/llama.cpp-0ce8cd1/tools/server/server.cpp          # "n_parallel = 4 and kv_unified = true"
> grep -n "DEFAULT_BLOCK_SIZE" ~/runtimes-src/vllm/vllm/config/cache.py
> ```
> Ćwiczenie: z konfiguracji `llama-swap` odczytaj `-np`, `-c` i ewentualne `--no-kv-unified` swojej konfiguracji produkcyjnej i policz, ile tokenów ma *każdy* slot z zunifikowanym KV i bez niego.

---

## 6. Batchowanie generacji i czym naprawdę jest `--parallel`

### 6.1 Cztery pokolenia

1. **Statyczne**: zbierz B żądań, uruchom, aż skończy się najdłuższe; skończone sekwencje marnują miejsce.
2. **Dynamiczne**: poczekaj chwilę na zebranie batcha, nadal na poziomie żądania.
3. **Ciągłe / na poziomie iteracji** (*continuous batching*). Orca (Yu i in., OSDI '22): „iteration-level scheduling" (skład batcha ustala się w każdej iteracji; skończone żądania wychodzą, nowe wchodzą) + „selective batching" (batchuje się tylko operacje o zgodnych kształtach, np. gęste mnożenia; uwaga idzie osobno na sekwencję). **36,9×** większa przepustowość niż FasterTransformer przy tym samym opóźnieniu na GPT-3 175B *(dane autorów, strona OSDI '22)*. Każdy silnik w kursie jest iteracyjny: scheduler vLLM (`v1/core/sched/scheduler.py`, 3527 wierszy), SGLang (`managers/scheduler.py`, 6278), `update_slots()` w llama-server, `BatchGenerator` w mlx-lm (`--decode-concurrency`, `--prompt-concurrency`).
4. **Chunked prefill** i **dezagregacja** — niżej.

### 6.2 Chunked prefill i poprawka cytowania

Długi prompt (np. wynik narzędzia na 20 tys. tokenów) zajmuje całą iterację i zatrzymuje wszystkie generujące sekwencje — skacze opóźnienie na token. Rozwiązanie: tnij prompt na kawałki i dokładaj do każdego dekodowania innych sekwencji.

> ⚠️ **Poprawka cytowania.** Arkusz zadania wskazywał arXiv 2308.16369 jako „Sarathi-Serve". To nieprawda: **2308.16369 to oryginalny SARATHI** („Piggybacking Decodes with Chunked Prefills", sierpień 2023), a **Sarathi-Serve to arXiv 2403.02310** („Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve", marzec 2024). Sprawdziłem obie strony abstraktów. Terminy „chunked prefill" i „stall-free scheduling" pochodzą z drugiej pracy; cytuj obie.

SARATHI: do 10× większa przepustowość dekodowania (LLaMA-13B/A6000), 1,25× end-to-end *(dane autorów)*. Sarathi-Serve: „2,6×" zdolności obsługi dla Mistral-7B, „do 3,7×" dla Yi-34B względem vLLM *(dane autorów)*. W kodzie: vLLM ma `enable_chunked_prefill = True` i budżet `max_num_batched_tokens` (`config/scheduler.py`); llama.cpp robi to **niejawnie** — prompt dłuższy niż `n_batch` rozciąga się na kilka wywołań `llama_decode` przeplatanych dekodowaniem innych slotów. Para pokręteł: `n_batch` (batch *logiczny*) i `n_ubatch` (fizyczny mikro-batch podawany grafowi GPU): `-b`, `-ub`.

### 6.3 Dezagregacja prefill/decode

Prefill na jednych GPU, dekodowanie na innych, KV przesyłane między nimi. DistServe (arXiv 2401.09670): „7,4× więcej żądań albo 12,6× ostrzejszy SLO", optymalizuje *goodput* *(dane autorów)*; Splitwise (arXiv 2311.18677): 1,4× przy 20% niższym koszcie *(dane autorów)*. Implementacje (znam istnienie, nie działanie): vLLM `disagg_prefill.md`, SGLang `srt/disaggregation/`, llm-d, Dynamo.

**Kiedy to ci się przyda.** Przy jednym użytkowniku scheduler nie ma czego przeplatać. Ale w **aplikacji agentowej** z równoległymi pod-agentami interferencja wraca: 20-tysięczny prefill wyniku narzędzia zatrzyma dekodowanie pozostałych. Odpowiedź llama.cpp: sloty + zunifikowane KV + strojenie `n_batch`/`n_ubatch` (mniejszy mikro-batch = mniejsze przestoje, niższa przepustowość prefillu) *(moje wnioskowanie)*.

### 6.4 Czym jest slot (zweryfikowane)

**Slot to pojęcie serwera, nie pamięci KV.** `server_slot` (`server-context.cpp`) = jeden identyfikator sekwencji + automat stanów {IDLE, WAIT_OTHER, STARTED, PROCESSING_PROMPT, DONE_PROMPT, GENERATING} + własny łańcuch samplerów + własny stan spekulacji + własna lista tokenów promptu (do dopasowania prefiksu). `--parallel N` (`-np`) = liczba slotów = `n_seq_max`.

**Pułapka** *(moje wnioskowanie z §5.4)*: przy `-np 4 -c 32768 --no-kv-unified` każdy slot dostaje 8192 tokeny; przy zunifikowanym KV pula jest wspólna i jedno żądanie może zająć całe 32768, gdy reszta stoi. Na rigu referencyjnym to **pomiar**: 2 sloty × 98 304 wyszły najlepiej (49,2 tok/s), 4 × 131 072 się nie zmieściły, 4 × 65 536 było wolniejsze (44,6) i zbyt ciasne ([`02-WDROZENIE-DEEPSEEK.md`](../przyspieszanie-generowania/02-WDROZENIE-DEEPSEEK.md)). Sloty **nie są** darmowe.

> **Sprawdź sam (6)**
> ```bash
> grep -n "struct server_slot" ~/llama.cpp-0ce8cd1/tools/server/server-context.cpp
> grep -n "n_parallel" ~/llama.cpp-0ce8cd1/tools/server/server.cpp | head
> grep -n "enable_chunked_prefill\|long_prefill_token_threshold" ~/runtimes-src/vllm/vllm/config/scheduler.py
> ```
> Ćwiczenie: otwórz `arxiv.org/abs/2308.16369` i `arxiv.org/abs/2403.02310` i sprawdź, który używa „stall-free" (oczekiwane: 2403.02310). Potem policz, ile iteracji zajmie prefill 20 000 tokenów przy `n_batch` = 2048 i jak zmienia się liczba przy `-ub 512`.

---

## 7. Jądra uwagi

**Linia FlashAttention.** Naiwna uwaga materializuje macierz N × N w HBM. **FlashAttention** (Dao i in., arXiv 2205.14135): dokładna uwaga „świadoma I/O", kafelkowana, z *online softmax*; 15% szybszy BERT-large, 3× GPT-2 *(dane autorów)*. Sztuczka *(z pamięci, niezweryfikowana)*: dla każdego wiersza trzymaj bieżące maksimum m i normalizator l; gdy dochodzi kafelek, przeskaluj: m' = max(m, rowmax(S)), l' = e^(m−m')·l + rowsum(e^(S−m')), O' = e^(m−m')·O + e^(S−m')·V — wynik dokładny, pamięć dodatkowa O(N). **FlashAttention-2** (arXiv 2307.08691): ~2×, 72% MFU na A100. **FlashAttention-3** (arXiv 2407.08608): specyficzna dla Hopper (TMA, asynchroniczne rdzenie tensorowe, FP8), do 740 TFLOPs/s w FP16 *(dane autorów)* — tylko NVIDIA, dla RDNA4 jedynie punkt odniesienia. **FlashInfer** (arXiv 2501.01005): formaty blokowo-rzadkie, JIT, wyważone planowanie; 29–69% mniejsze opóźnienie między tokenami *(dane autorów)*. Dekodowanie ma inny profil (jedno zapytanie na sekwencję, praca ograniczona KV; „split-KV / flash-decoding" — z pamięci); llama.cpp ma osobne jądra `fattn-vec` (mały batch), `fattn-tile`, `fattn-mma-f16`.

**Co llama.cpp uruchamia na kartach R9700** (kod). Backend ROCm to kod ggml CUDA skompilowany dla HIP, więc nazwy to `ggml-cuda/*`. `ggml_cuda_get_best_fattn_kernel` (`ggml/src/ggml-cuda/fattn.cu`) wybiera przy każdym wywołaniu: na AMD z **WMMA** (RDNA3/4) jądro MMA_F16 **tylko jeśli** działa optymalizacja GQA, head_dim ≤ 256 i `Q->ne[1] * gqa_ratio_eff > 8` (head_dim ≤ 128) lub `> 16` (≤ 256); w przeciwnym razie ogólne **TILE**, albo **VEC** dla skwantyzowanego KV przy ≤ 2 kolumnach zapytań. Wniosek *(moje wyliczenie z progów)*: dekodowanie z batchem 1 na gfx1201 w większości biegnie przez TILE/VEC, a prefill z dużym mikro-batchem przez WMMA. `-fa auto` jest domyślne; skwantyzowane V i podział tensorowy **wymagają** FA. Mnożenia: `mmvq` (skwantyzowane macierz × wektor, koń pociągowy dekodowania), `mmq` (macierz × macierz z kafelkami INT8; `mmq-config-rdna4.cuh`), `mmf`, `topk-moe`.

**vLLM i SGLang na ROCm** (logika wyboru, nie działanie). vLLM zna R9700 (`vllm/platforms/rocm.py`: `0x7551: "AMD_Radeon_R9700"`, `_ON_RDNA4`); priorytet backendów (`_get_backend_priorities`): `ROCM_ATTN` → `ROCM_AITER_FA` (jeśli włączono AITER) → `ROCM_AITER_UNIFIED_ATTN` (na RDNA tylko z `is_rdna_aiter_enabled()`) → `TRITON_ATTN`…; dla rzadkiej MLA (DSA/V4) tylko `ROCM_AITER_MLA_SPARSE` plus osobne backendy V4/V4.1. **Czy AITER jest dostrojony i działa na gfx1201, a nie tylko na klasie MI300, nie wynika z kodu.** SGLang ma `aiter_backend.py`, `triton_backend.py`, `flashinfer_backend.py`, `deepseek_v4_backend*.py` (w tym `_hip_radix`). MLX używa własnych jąder Metal *(niezweryfikowane)*. Szczegóły: rozdział [`06`](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md).

> **Sprawdź sam (7)**
> ```bash
> grep -n "amd_wmma\|TILE\|VEC\|MMA_F16" ~/llama.cpp-0ce8cd1/ggml/src/ggml-cuda/fattn.cu | head -40
> grep -n "R9700\|_ON_RDNA4" ~/runtimes-src/vllm/vllm/platforms/rocm.py
> ```
> Ćwiczenie czytania kodu: znajdź progi `> 8` i `> 16`; ustal gałąź dla dekodowania z batchem 1 przy efektywnym stosunku GQA równym 8 (1 × 8 nie przekracza `> 8`). Potem odczytaj z `config.json` swojego modelu `head_dim` i sprawdź, czy `head_dim <= 256` w ogóle dopuszcza MMA_F16. Wyniku dla modelu referencyjnego nie znam *(niezweryfikowane)*.

---

## 8. Równoległość na wielu kartach i pomiar referencyjny

### 8.1 Pięć rodzajów podziału

| rodzaj | co jest dzielone | komunikacja na warstwę | gdzie |
|---|---|---|---|
| **Tensorowy (TP)**, Megatron-LM (arXiv 1909.08053: 8,3 mld parametrów na 512 GPU, 76% sprawności *(dane autorów)*) | głowice uwagi i kolumny/wiersze FFN; każda karta trzyma 1/n każdej warstwy | 2 *all-reduce* na warstwę *(standard; niezweryfikowane w treści pracy)* | llama.cpp `--split-mode tensor`, vLLM, SGLang |
| **Rurociągowy (PP)** | ciągłe zakresy warstw na kartę | jeden transfer aktywacji na granicę etapu | llama.cpp `--split-mode layer` (domyślny), vLLM |
| **Ekspertowy (EP)** | eksperci MoE rozdzieleni między karty; tokeny routowane *all-to-all* | 2 all-to-all na warstwę MoE | vLLM (`fused_moe/all2all*`, `distributed/eplb`), SGLang `eplb/` |
| **Danych (DP)** | pełne repliki | brak | vLLM; kilka procesów llama-server pod `llama-swap` to „DP dla ubogich" *(moje wnioskowanie)* |
| **Sekwencji/kontekstu (SP/CP)** | wymiar sekwencji uwagi/KV | wymiana KV lub częściowych softmaxów | vLLM `_DCP`, `_PCP` (znam nazwy) |

### 8.2 Co interkonekt musi unieść *(moje wyliczenie; wejścia flagowane)*

Kształt V4-Flash: ukryty 4096, 43 warstwy ⇒ 86 *all-reduce* na token w TP, FP16.

- **Dekodowanie, batch 1:** jeden all-reduce = 4096 × 2 B = **8 KiB**; przepustowość nie ma znaczenia, **dominuje opóźnienie**: 86 kolektywów × (10–40 µs, *zakres niezweryfikowany*) = **0,9–3,4 ms na token**, wobec idealnego kroku TP ~2 ms (5,1 GB / 2560 GB/s). TP z batchem 1 przez PCIe jest więc ograniczone opóźnieniem.
- **Prefill, ubatch 2048:** 2048 × 4096 × 2 B = 16 MiB na all-reduce, ×86, ruch pierścieniowy ≈ **2,0 GiB na kartę na ubatch**; przy 63 GB/s = 34 ms, przy 25 GB/s (przez hosta) = 87 ms, wobec ~345 ms obliczeń *(wejście obliczeniowe niezweryfikowane)* — narzut 10–25%, *jeśli* łącze dostarcza; dla x4 czterokrotnie gorzej.
- NVLink/xGMI są ~10× szybsze od PCIe i mają dużo niższe opóźnienie *(niezweryfikowane)*; R9700 ich nie ma — każdy bajt między kartami przechodzi przez PCIe.

### 8.3 Tryby podziału w llama.cpp (`docs/multi-gpu.md` i kod)

- `none`, **`layer`** (domyślny; „priority is a fast prefill", toleruje wolny interkonekt), `row` (przestarzały), **`tensor`** (EKSPERYMENTALNY; abstrakcja „meta device" w `ggml/src/ggml-backend-meta.cpp`; dzieli wagi *i* KV).
- `tensor` wymaga `-fa on` i **nieskwantyzowanego KV**, wyłącza `--fit` i próbkowanie w backendzie; **nie jest zaimplementowany** m.in. dla Grok, MPT, OLMoE, **DeepSeek2, DeepSeek32**, GLM-DSA, Nemotron-H, MiniMax, Kimi-Linear, Jamba, Mamba(2), Gemma3n, T5 (pełna lista: `llm_arch_supports_sm_tensor`, `src/llama-arch.cpp`). **DeepSeek4 nie jest na liście wykluczeń**; dziennik wdrożenia w przyspieszanie-generowania dodaje, że zaktualizowany llama.cpp ma jawną obsługę stanów skompresowanej uwagi V4 w tym trybie, a na starej wersji nie próbowałeś.
- Redukcje: `ggml_backend_comm_allreduce_tensor` (np. NCCL) z ogólnym wariantem zapasowym. Dla ROCm **RCCL trzeba włączyć przy budowaniu `-DGGML_HIP_RCCL=ON`; domyślnie jest WYŁĄCZONY**, bo „(w przeciwieństwie do NCCL) nie był uniwersalnie korzystny w testach". Wbudowany all-reduce istnieje dla **dwóch** GPU (przez pinned host memory, z oczekiwaniem aktywnym w jądrze dla niskiego opóźnienia — `ggml-cuda/allreduce.cu`), czyli autorzy wiedzą, że dekodowanie jest ograniczone opóźnieniem. `GGML_CUDA_P2P=1` (opt-in) włącza bezpośredni dostęp między kartami; „może powodować awarie lub uszkodzone wyniki na niektórych płytach (np. przy IOMMU)".
- **Prawdziwy rurociąg** (nakładanie mikro-batchów) włącza się tylko gdy: >1 urządzenie, wszystkie warstwy na GPU, `split_mode == LAYER`, `offload_kqv`, brak nadpisań tensorów, brak host-cache MoE, wsparcie async (`src/llama-context.cpp`; log „pipeline parallelism enabled"). Dla **jednego** strumienia nie ma czego nakładać — stąd podział warstwami daje szybkość jednej karty (§2.6).

### 8.4 Pomiar referencyjny na tle teorii

Dane z dziennika wdrożenia w przyspieszanie-generowania (DeepSeek-V4-Flash-0731, UD-IQ3_XXS, 4 karty, jeden agent, średnia z 4 rodzajów zadań × 2 temperatury; [`README.md`](../przyspieszanie-generowania/README.md), [`02-WDROZENIE-DEEPSEEK.md`](../przyspieszanie-generowania/02-WDROZENIE-DEEPSEEK.md)):

| konfiguracja | tok/s | ms / token *(moje wyliczenie)* | ułamek sufitu 126 tok/s *(moje wyliczenie)* |
|---|---|---|---|
| stary llama.cpp, warstwy, bez draftu | 23,5 | 42,6 | |
| stary, + DSpark (n=3) | 35,2 | 28,4 | |
| **nowy** (`0ce8cd1`), warstwy, bez draftu | 25,2 | 39,7 | ~20% |
| nowy, warstwy, z draftem | 37,9 | 26,4 | |
| nowy, **tensor**, bez draftu | 29,1 | 34,4 | ~23% |
| nowy, tensor, z draftem (1 slot × 131k) | 46,2 | 21,6 | |
| nowy, tensor + draft, **wdrożone** (2 sloty × 98k, `--ubatch-size 512`) | 49,2 (produkcja ≈ 49–50) | 20,3 | |

(46,2 i 49,2 to dwie *różne* konfiguracje z macierzy w dzienniku, nie sprzeczność. Sufit 126 liczony dla zastępczych 3 bpw i 640 GB/s — to rząd wielkości, nie precyzyjna sprawność; średnia liczba bitów pliku referencyjnego wynosi 2,94 bpw (104 207 848 508 B · 8 / 284 mld, *moje wyliczenie*; rozdział [03](03-KWANTYZACJA-I-FORMATY.md), §7.4), więc „3 bpw” było dobrym przybliżeniem.)

1. **Tryb tensorowy dał +15% bez draftu (25,2 → 29,1), nie ×4.** Zgodne z tym, że przy batchu 1 liczy się opóźnienie kolektywów, nie przepustowość. W logu masz `internal AllReduce init failed (n_devices != 2?); falling back to meta-backend butterfly` — przy czterech kartach działa **ogólna, wolniejsza ścieżka**; RCCL i P2P mogłyby pomóc — **nie testowałeś**. Do tego dwie karty na x4 (§2.3).
2. **Rachunek z §8.2 nie wyjaśnia liczb referencyjnych w całości.** Narzut samych kolektywów (0,9–3,4 ms) tłumaczy co najwyżej ~3 z 34 ms. Różnica między trybami to 39,7 − 34,4 = 5,3 ms, a idealny zysk z czterokrotnej przepustowości to 7,9 − 2,0 = 5,9 ms *(moje wyliczenie, zastępcze 3 bpw)*. Wygląda to tak, jakby tryb tensorowy odzyskał niemal całą część „przepustowościową", a reszta (~30 ms na token) **nie zależała od przepustowości pamięci** — np. koszty stałe na warstwę: uruchamianie jąder, synchronizacje, routing MoE, rozpakowywanie kwantów IQ. To **hipoteza**; w notatkach nie ma profilu, który by ją rozstrzygał.
3. **Draft pomaga bardziej, gdy krok jest „drogi i stały":** ×1,5 w trybie warstwowym i ×1,6 w tensorowym (25,2 → 37,9; 29,1 → 46,2); oba mechanizmy razem ×1,8 względem 25,2 (dziennik). Gdy większość czasu kroku to koszt niezależny od liczby tokenów, weryfikacja 4 tokenów kosztuje niewiele więcej niż jednego — dokładnie warunek, na którym stoi spekulacja (§9). Dziennik wdrożenia: oba mechanizmy się mnożą, bo szybszy krok sprawia, że weryfikacja większej partii jest relatywnie tańsza.
4. **Cena w prefillu:** ~960 → ~700 tok/s (−27%) i 2 sloty po 98 304 zamiast 4 po 131 072. §8.2 przewidywał narzut komunikacji 10–25% przy łączu x16; nie rozdzielałem, ile z −27% to komunikacja, a ile mniejszy mikro-batch *(niezweryfikowane)*.

**Jak zmierzyć lepiej:** skalibruj sprawność jąder na małym modelu gęstym, który mieści się na jednej karcie (`llama-bench -p 0 -n 128`; bajty wag z rozmiaru pliku; 640 GB/s *(źródło zewnętrzne)*) — dostaniesz współczynnik korygujący sufity z §2; dopiero wtedy różnica do DeepSeeka jest interpretowalna.

> **Sprawdź sam (8)**
> ```bash
> sed -n 1288,1324p ~/llama.cpp-0ce8cd1/src/llama-arch.cpp     # lista architektur bez trybu tensorowego
> grep -n -i "RCCL\|P2P\|tensor" ~/llama.cpp-0ce8cd1/docs/multi-gpu.md | head -30
> sed -n 517,546p ~/llama.cpp-0ce8cd1/src/llama-context.cpp    # warunki prawdziwego rurociągu
> ```
> Ćwiczenie: sprawdź, czy twój model **nie** jest na liście wykluczeń; potem, mając pomiary z §8.4, wypisz trzy hipotezy o źródle ~30 ms „stałego" czasu na token i dla każdej jeden odczyt/pomiar tylko-do-odczytu, który by ją potwierdził lub obalił.

---

## 9. Speculative decoding

### 9.1 Idea i gwarancja

Tani *zgadywacz* (*draft*) proponuje k tokenów; model docelowy ocenia k+1 pozycji w **jednym** przebiegu (koszt zbliżony do jednego kroku, dopóki jest ograniczony pamięcią); przyjmujemy najdłuższy zgodny prefiks plus jeden token docelowy. Leviathan i in. (arXiv 2211.17192): 2–3× na T5-XXL „z identycznymi co do bajta wynikami"; Chen i in. (arXiv 2302.01318): „zmodyfikowany schemat odrzucania, zachowujący rozkład modelu docelowego" *(dane autorów)*. Gwarancja dotyczy *rozkładu*; przy dekodowaniu zachłannym — token po tokenie. llama.cpp implementuje schemat odrzucania (`common_sampler_sample_and_accept_n_rejection`, `common/sampling.cpp`) i dokumentuje syntetyczne testy trafności (`--spec-synth-rates`, `--spec-synth-len`; `docs/speculative.md`).

### 9.2 Arytmetyka trafności

Załóż, że każdy zgadywany token jest przyjmowany niezależnie z prawdopodobieństwem α (idealizacja). Oczekiwana liczba tokenów na przebieg modelu docelowego przy k zgadywanych:

> **E[tokeny] = (1 − α^(k+1)) / (1 − α)** (= 1 + α + … + α^k; wzór z pracy Leviathana — z treści niezweryfikowany, ale to suma geometryczna, którą wyprowadziłem sam)
>
> **przyspieszenie = E[tokeny] / (1 + c·k)**, c = czas kroku zgadywacza / czas kroku modelu docelowego (przy weryfikacji kosztującej tyle co zwykły krok — model gęsty, ograniczony pamięcią)

| α \ k | 1 | 2 | 3 | 4 | 5 | 7 | 15 |
|---|---|---|---|---|---|---|---|
| 0,5 | 1,50 | 1,75 | 1,88 | 1,94 | 1,97 | 1,99 | 2,00 |
| 0,7 | 1,70 | 2,19 | 2,53 | 2,77 | 2,94 | 3,14 | 3,32 |
| 0,8 | 1,80 | 2,44 | 2,95 | 3,36 | 3,69 | 4,16 | 4,86 |
| 0,9 | 1,90 | 2,71 | 3,44 | 4,10 | 4,69 | 5,70 | 8,15 |

*(wartości E[tokeny]: moje wyliczenie)*

**Przykład 1** (tani zgadywacz): α = 0,8, c = 0,05, k = 4: 3,36 / (1 + 0,2) = **2,80**; dla k = 1…7: 1,71 / 2,22 / 2,57 / 2,80 / 2,95 / 3,08 (k = 1, 2, 3, 4, 5, 7). **Przykład 2** (droższy): α = 0,8, c = 0,2: 1,50 / 1,74 / 1,85 / 1,87 / 1,84 / 1,73 — maksimum przy k = 4, potem spadek. Wnioski: zyski **nasycają się** w k, a koszt zgadywacza c wyznacza optymalne k.

**Uwaga o słownictwie:** llama.cpp wypisuje „draft acceptance rate = accepted/generated" (na zgadywany token, warunkowo względem pozycji i obcięcia) — to **nie** jest idealizowane α. `--spec-synth-len L` definiuje L = średnią przyjętą długość łącznie z tokenem docelowym i rozwiązuje p + p² + … + p^K = L − 1 (L = 3, K = 7 daje p = 0,68 *(moje wyliczenie)*).

**Przykład 3: odwrócenie rachunku na danych referencyjnych.** Zmierzone przyspieszenie przy k = 3 to ×1,5–1,6. Przy *założonym* (nie zmierzonym) c = 0,05 i narzucie weryfikacji r = 1,2: E / (r + c·k) = 1,55 ⇒ E ≈ 1,55 × 1,35 ≈ 2,1 ⇒ α ≈ 0,6 (E(0,6; 3) = 2,18; E(0,55; 3) = 2,02) *(przykład metody wyciągania α z pomiaru, nie pomiar twojego α)*.

### 9.3 Kara za MoE

Z §4.2: weryfikacja n = k+1 tokenów czyta 1,47× / 1,93× / 2,38× / 2,82× / 3,25× / 4,07× bajtów jednego tokenu (n = 2, 3, 4, 5, 6, 8). Zysk netto = E[tokeny] / (stosunek bajtów), bez kosztu draftu *(moje wyliczenie; jednostajny routing)*:

| α \ k | 1 | 2 | 3 | 4 | 5 | 7 |
|---|---|---|---|---|---|---|
| 0,6 | 1,09 | 1,02 | 0,92 | 0,82 | 0,74 | 0,60 |
| 0,7 | 1,16 | 1,14 | 1,07 | 0,99 | 0,91 | 0,77 |
| 0,8 | 1,22 | 1,27 | 1,24 | 1,19 | 1,14 | 1,02 |
| 0,9 | 1,29 | 1,41 | 1,45 | 1,45 | 1,45 | 1,40 |

Przy α = 0,8, k = 4 model **gęsty** daje ×3,36, a MoE przy jednostajnym routingu ×1,19. Realny routing jest skorelowany między sąsiednimi tokenami, więc rzeczywistość leży **pomiędzy** tabelami *(niezweryfikowane)*. To prawdopodobne wyjaśnienie skromnych zysków na dużych rzadkich MoE i powód, dla którego DSpark/MTP dla klasy V4 mają **krótkie** drafty (ds4: do 5 tokenów) i obcinanie pewnością (próg ds4 dla pojedynczego Sparka 0,4).

### 9.4 Rodzina metod

| metoda | skąd draft | llama.cpp (ten build) | vLLM / SGLang (te drzewa) |
|---|---|---|---|
| **model-zgadywacz** | mały LM tej samej rodziny | `--spec-type draft-simple`, `-md` | `draft_model` / `STANDALONE` |
| **Medusa** (arXiv 2401.10774: >2,2× i 2,3–3,6× *(dane autorów)*) | dodatkowe głowice na modelu docelowym, uwaga drzewiasta | **nie znalazłem** (grep) | **nie znalazłem** |
| **EAGLE-1/2/3** (arXiv 2401.15077, 2406.16858, 2503.01840: do 6,5× w wersji 3 *(dane autorów)*) | autoregresja na poziomie *cech*; wersja 2 — dynamiczne drzewo; wersja 3 — cechy wielu warstw | tylko `draft-eagle3` (checkpointy: Llama 3.x, Qwen3, gpt-oss, Gemma-4) | `eagle`, `eagle3` / `EAGLE`, `EAGLE3` |
| **Lookahead** (arXiv 2402.02057) | iteracja Jacobiego + pula n-gramów | `examples/lookahead` | — |
| **n-gram / prompt lookup** | kopiuje kontynuacje widziane wcześniej w kontekście (kod, RAG, streszczanie) | `ngram-simple`, `-map-k`, `-map-k4v`, `ngram-mod` (pula ~16 MB, wspólna dla slotów), `ngram-cache`; `--spec-default` = ngram-mod | `ngram`, `suffix` / `NGRAM` |
| **głowice MTP** | model był trenowany do przewidywania kolejnych tokenów (V4: `num_nextn_predict_layers: 1`) | `draft-mtp` | wiele typów `*_mtp` / `FROZEN_KV_MTP` |
| **DFlash** | zgadywacz dyfuzyjny blokowy: cały blok tokenów w **jednym** przebiegu, uwarunkowany ukrytymi stanami celu; „do 6× bezstratnie na Qwen3-8B" *(dane projektu)* | `draft-dflash` (scalony 2026-06-28, PR #22105) | `dflash` / `DFLASH` |
| **DSpark** | DFlash + niskorangowa „głowica Markowa" (blok próbkowany od lewej do prawej w jednym grafie) + opcjonalna głowica pewności (`--spec-draft-conf-min`) | `draft-dspark` (scalony 2026-07-28, PR #25173) | `dspark` / `DSPARK` |

**Poprawki do skojarzeń.** **DSpark nie jest akronimem z cudzego forka**: w llama.cpp to „DFlash + głowica Markowa"; checkpointy są w organizacji Hugging Face `deepseek-ai` (`deepseek-ai/dspark_qwen3_{4b,8b,14b}_block7`, `docs/speculative.md`). Tekst PR (autor `wjinxu`) opisuje go jako „DeepSeek + PKU, 2026, ‘Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation’" — że PR tak pisze, jest zweryfikowane, samej pracy nie pobrałem *(dane bibliograficzne niezweryfikowane)*. **DFlash** = „Block Diffusion for Flash Speculative Decoding" (Chen, Liang, Liu; arXiv 2602.06036, ICML 2026; wg strony z-lab.ai). Medusa: „nie znaleziono grepem" w llama.cpp, vLLM i SGLang; starsze wersje mogły ją mieć. **Rozbieżność:** dokumentacja llama.cpp w tym drzewie mówi o DSpark z samym szkieletem Qwen3, a dziennik wdrożenia w przyspieszanie-generowania opisuje głowicę DSpark z checkpointu V4-Flash-0731 skonwertowaną do GGUF — nie rozstrzygałem, kto ma rację w szczegółach *(niezweryfikowane)*.

### 9.5 Zmierzone zyski (autorów PR — nie twoje)

Autorzy PR #25173, jedna RTX 4090, Qwen3-8B bf16, zachłannie, `--spec-draft-n-max 7` *(dane projektu)*: DSpark **1,88×** wobec braku spekulacji (DFlash 1,55×) na podzbiorze „qualitative" SPEED-Bench; średnia geometryczna 3,35× wobec 2,89× na GSM8K/MATH500/HumanEval/MBPP/MT-Bench; mniej dla skwantyzowanych celów (Q4_K_M: 1,81× wobec 1,54×). PR #22105: Qwen3.6-27B Q4_K_M na DGX Spark 2,69×, ale **gpt-oss-20B 0,61–1,27× (często spowolnienie)** *(dane projektu)*. Lekcja: zysk zależy od przewidywalności zadania (kod/RAG wysoko, otwarty czat nisko), od precyzji celu i — dla MoE — od kosztu weryfikacji. **To liczby z innego sprzętu i modelu; nie mieszaj ich z twoimi** (§14).

Twoje: 23,5 → 35,2 (×1,50, stary build), 25,2 → 37,9 (×1,50) i 29,1 → 46,2 (×1,59) na nowym — V4-Flash z DSpark o długości 3. Mieści się w widełkach z PR, choć to MoE ze skwantyzowanymi wagami; bez pomiaru α i zachowania routingu nie rozstrzygnę, *dlaczego*.

> **Sprawdź sam (9)**
> ```bash
> less ~/llama.cpp-0ce8cd1/docs/speculative.md        # typy, statystyki, --spec-synth-*
> grep -n "spec-type\|draft-dspark\|draft-dflash\|draft-mtp\|ngram" ~/llama.cpp-0ce8cd1/common/arg.cpp | head -30
> grep -n "sample_and_accept_n_rejection" ~/llama.cpp-0ce8cd1/common/sampling.cpp
> ```
> Ćwiczenie rachunkowe: dla α = 0,75 i c = 0,1 znajdź k maksymalizujące E/(1+ck) (k = 1…8). Powtórz dla MoE z mianownikiem (stosunek bajtów z §4.2) + c·k i porównaj optymalne k. Co to mówi o doborze `--spec-draft-n-max` dla V4-Flash?

---

## 10. Próbkowanie

Sieć zwraca **logity** z (po jednym na pozycję słownika). **Łańcuch samplerów** przekształca tablicę kandydatów i wybiera token. Domyślna kolejność w llama.cpp (`common_params_sampling::samplers`, `common/common.h`):

> **kary → DRY → top-n-sigma → top-k → typical-p → top-p → min-p → XTC → temperatura → (na końcu) losowanie albo wybór zachłanny**

Wartości domyślne (`common/common.h`): temperatura 0,8; top-k 40; top-p 0,95; min-p 0,05; XTC, DRY (mnożnik 0, baza 1,75, dozwolona długość 2) i Mirostat wyłączone. Skoro obcinanie następuje *przed* temperaturą, temperatura działa już na zawężonym zbiorze.

**Przykład temperatury** *(moje wyliczenie)*: logity (2, 1, 0). T = 1 → (0,665; 0,245; 0,090). T = 0,5 (logity (4, 2, 0)) → (0,867; 0,117; 0,016) — ostrzej. T = 2 → (0,506; 0,307; 0,186) — płasko. T → 0 to wybór zachłanny. **Przykład min-p:** przy min-p = 0,2 i rozkładzie z T = 1 próg to 0,2 × 0,665 = 0,133; zostają dwa pierwsze tokeny; przy min-p = 0,05 (próg 0,033) wszystkie trzy.

Po jednej linii o każdym pokrętle:

- **Zachłanne**: argmax z. **Temperatura**: p_i = softmax(z_i / T).
- **Top-k**: k najwyższych. **Top-p / nucleus** (Holtzman i in., ICLR 2020, arXiv 1904.09751): najmniejszy zbiór o masie skumulowanej ≥ p.
- **Min-p** (Nguyen i in., ICLR 2025, arXiv 2407.01082): tokeny z p_i ≥ min_p × p_max — „dostosowuje próg do pewności modelu".
- **Typical-p** (Meister i in., TACL 2022, arXiv 2202.00666): tokeny o zawartości informacyjnej −log p_i najbliższej entropii rozkładu *(reguła z treści niezweryfikowana)*.
- **Mirostat** (Basu i in., arXiv 2007.14966): regulator dostrajający obcinanie, by entropia wyjścia trzymała się celu τ *(wzór niezweryfikowany)*; w llama.cpp v1 i v2.
- **Top-n-sigma** (Tang i in., arXiv 2411.07641): na surowych logitach, zostaw z_i ≥ z_max − n·σ(z) — stabilna przestrzeń niezależnie od temperatury *(wzór z pamięci)*.
- **XTC** (*Exclude Top Choices*; p-e-w, PR #6335 w text-generation-webui): z prawdopodobieństwem P, gdy ≥ 2 tokeny mają p ≥ progu, usuń wszystkie oprócz **najmniej** prawdopodobnego (`llama_sample_xtc_apply`; nieaktywny przy progu > 0,5).
- **DRY** (p-e-w, PR #5677): jeśli token przedłuża ciąg, który już wystąpił (długość n ≥ dozwolonej), odejmij od logitu **mnożnik × baza^(n − dozwolona_długość)**; separatory (nowa linia, cudzysłowy…) resetują dopasowanie.
- **Kary** powtórzeń/częstości/obecności po ostatnich `penalty_last_n` tokenach. **Adaptive-P**: nowy sampler kierujący prawdopodobieństwo wybranego tokenu ku wartości docelowej z historią EMA *(algorytm niezweryfikowany)*.
- **Bias logitów, gramatyka i budżet rozumowania** to też samplery w łańcuchu. Budżet (`common/reasoning-budget.{h,cpp}`) to automat IDLE → COUNTING → WAITING_UTF8 → FORCING → DONE: po wyczerpaniu budżetu „myślenia" wymusza zamknięcie myślenia, ustawiając inne logity na −∞.
- GGUF może nieść **zalecane parametry próbkowania** (`general.sampling.top_k/top_p/min_p/temp/…`; `gguf-py/gguf/constants.py`) — o formacie: rozdział 03.
- **Próbkowanie w backendzie** (`--backend-sampling`): niezgodne z gramatykami, budżetem rozumowania i podziałem tensorowym.

> **Sprawdź sam (10)**
> ```bash
> sed -n 225,280p ~/llama.cpp-0ce8cd1/common/common.h          # kolejność samplerów i domyślne wartości
> sed -n 1,60p ~/llama.cpp-0ce8cd1/common/reasoning-budget.h   # automat budżetu rozumowania
> sed -n 30,48p ~/llama.cpp-0ce8cd1/gguf-py/gguf/constants.py  # klucze GGUF z próbkowaniem
> ```
> Ćwiczenie: dla logitów (3, 2, 1, 0) policz rozkład przy T = 0,7, zastosuj top-p = 0,9 i przeskaluj; ile tokenów zostaje? Powtórz w odwrotnej kolejności (najpierw top-p, potem T) — wynik się różni; dlatego kolejność jest częścią specyfikacji.

---

## 11. Gramatyka i wywoływanie narzędzi

### 11.1 Jak liczy się maska tokenów

Cel: zagwarantować, że wynik pasuje do regexu / schematu JSON / gramatyki. W każdym kroku wylicz zbiór tokenów, które utrzymują wynik jako poprawny prefiks, ustaw logity reszty na −∞, dopiero potem losuj. Trudność: tokeny to ciągi bajtów przecinające granice terminali, a słownik ma 100–250 tys. pozycji.

- **GBNF w llama.cpp** (`src/llama-grammar.cpp`, 1530 wierszy; JSON Schema → GBNF w `common/json-schema-to-grammar.cpp`): reguły kompilowane do **automatu ze stosem**; środowisko trzyma *listę stosów* (wszystkie stany zgodne z tekstem). `llama_grammar_apply_impl`: dla każdego kandydata dekoduje fragment UTF-8 i sprawdza go na każdym stosie — praca rzędu wielkości słownika na krok, na CPU. Łagodzenie w `common_sampler_sample`: jeśli nie ustawiono `grammar_first`, llama.cpp **najpierw losuje bez gramatyki i sprawdza tylko wylosowany token; dopiero gdy jest niepoprawny, nakłada pełną maskę** — typowy przypadek kosztuje jedno sprawdzenie. Są też **gramatyki leniwe** (tokeny/wzorce wyzwalające): gramatyka śpi, dopóki model nie wyemituje np. otwarcia wywołania narzędzia, więc wolny tekst zostaje nieograniczony.
- **llguidance** (opcjonalnie `-DLLAMA_LLGUIDANCE=ON`, wymaga Rusta): „maska tokenów dla tokenizera llama3 (128 tys.) zajmuje średnio 50 µs jednego rdzenia, p99 0,5 ms" *(dane projektu)*. Gramatyki z `%llguidance` trafiają do niego.
- **xgrammar** (arXiv 2411.15100): tokeny *niezależne od kontekstu* mają maskę wyliczoną z góry per stan automatu, tylko *zależne od kontekstu* sprawdza się w czasie działania; „do 100× przyspieszenia" *(dane autorów)*. Domyślny backend w vLLM i SGLang (`backend: "auto"`; są też `outlines`, `lm_format_enforcer`, `llguidance`).
- **Outlines** (arXiv 2307.09702): regex/CFG → automat skończony i **indeks słownika** (stan → dozwolone tokeny), więc maska to wyszukanie w słowniku. SGLang dodaje *jump-forward*: gdy gramatyka wymusza jednoznaczną kontynuację, emituje ją bez losowania.

### 11.2 Dlaczego to ważne w agentach

Argumenty narzędzia muszą być parsowalnym JSON-em; jedno zepsute wywołanie przerywa pętlę. vLLM: `tool_choice` z nazwaną funkcją i `required` **zawsze** używają ograniczeń strukturalnych; `auto` używa parsera specyficznego dla modelu na wolnym tekście, a gramatyka dochodzi tylko dla `strict: true` lub z `--tool-strict-level`; „przy `tool_choice="auto"` model generuje wywołania bez żadnej gramatyki i uszkodzony znacznik może wyciec do odpowiedzi" (`docs/features/tool_calling.md`). Pierwsze użycie schematu płaci koszt kompilacji („kilka sekund"). W vLLM maska działa dopiero po zakończeniu rozumowania. Gramatyka + spekulacja jest delikatna: llama.cpp renormalizuje resztę rozkładu po zamaskowaniu.

**Koszt** *(moje wnioskowanie)*: gramatyka może *zmienić jakość* — wpycha model na ścieżki, których by nie wybrał; wymuszenie `{` jako pierwszego znaku może stłumić rozumowanie. Rozumowanie zostaw poza częścią ograniczoną.

### 11.3 Mechanika od początku do końca

1. Klient wysyła `tools=[{name, description, JSON Schema}]` i wiadomości. 2. Serwer renderuje **szablon czatu** (§12) ze zmienną `tools`. 3. Model generuje tekst z wywołaniem w *swoim* formacie przewodowym (Hermes `<tool_call>{json}</tool_call>`, Mistral `[TOOL_CALLS]`, Harmony w gpt-oss, XML w Qwen3-Coder, DSML DeepSeeka…). 4. Serwer **parsuje** go do `tool_calls` (nazwa + ciąg JSON), z obsługą strumieniowania, i oddziela rozumowanie. 5. Klient wykonuje narzędzie, odsyła `role: tool`, pętla.

- **vLLM**: parser per rodzina (`--tool-call-parser` z `--enable-auto-tool-choice`; ~60 plików w `vllm/tool_parsers/`) i parsery rozumowania (`--reasoning-parser`, ~40). **Zła nazwa parsera = wywołania wracają jako zwykły tekst.**
- **llama.cpp**: `--jinja` (domyślnie włączone) używa własnego silnika Jinja w C++ (`common/jinja/`, „znakowanie wejścia", by tekst użytkownika nie wstrzyknął tokenów specjalnych). Potem albo **parser ręczny per model** (`common/parsers/*.cpp`: deepseek, gpt-oss, qwen3-coder, kimi, gemma4, minimax…), albo **auto-parser** (`common/chat-diff-analyzer.cpp`): analizuje szablon *różnicowo* („zainspirowane git diff": renderuje z narzędziami i bez, z rozumowaniem i bez), wykrywa znaczniki i buduje **parser PEG** oraz opcjonalnie (leniwą) gramatykę GBNF (`docs/autoparser.md`). Nieznany szablon ⇒ ogólny wariant JSON, droższy w tokenach i mniej niezawodny.
- **Ograniczenie:** JSON-schema, gramatyki narzędzi i budżet rozumowania to samplery CPU; działają z ROCm, ale wymuszają **synchronizację GPU → CPU przy każdym tokenie** (`llama_synchronize` w `common_sampler_sample`).

> **Sprawdź sam (11)**
> ```bash
> sed -n 606,690p ~/llama.cpp-0ce8cd1/common/sampling.cpp         # najpierw losuj, potem sprawdź
> grep -n "lazy\|awaiting_trigger" ~/llama.cpp-0ce8cd1/src/llama-grammar.cpp | head
> less ~/llama.cpp-0ce8cd1/docs/autoparser.md
> ls ~/runtimes-src/vllm/vllm/tool_parsers | head -80
> ```
> Ćwiczenie: w `docs/features/tool_calling.md` vLLM wypisz, które wartości `tool_choice` dają gwarancję składni; dla agenta pracującego godzinami bez nadzoru wybierz jedną i nazwij koszt opóźnienia.

---

## 12. Szablony czatu i parsery rozumowania

Model czatu był trenowany na **serializacji tekstowej** rozmów ze znacznikami ról i tokenami specjalnymi (`<|im_start|>user`, `[INST]`, `<|start|>assistant<|channel|>`…). Szablon jest dostarczany z modelem jako **Jinja2** (`tokenizer_config.json: chat_template`; GGUF: `tokenizer.chat_template`). Runtime musi go odtworzyć **co do bajta**, bo model nie widział innego opakowania.

**Ciche tryby awarii** *(wniosek z kodu i wiedzy ogólnej; każdy pogarsza jakość bez błędu)*:

1. **Niedopasowany szablon** (znaczniki ról, których model nie zna).
2. **Podwójny BOS**: GGUF ma `add_bos_token = true`, a prompt też zaczyna się od `<bos>`; llama.cpp loguje „…So now the final prompt starts with 2 BOS tokens" (`src/llama-vocab.cpp`).
3. **Brak promptu generowania** — model kontynuuje *turę użytkownika*.
4. **Obsługa roli system** (szablony, które ją odrzucają lub gubią).
5. **Narzędzia w innym formacie** niż w treningu albo parser niedopasowany do modelu.
6. **Rozumowanie w historii**: szablony wycinające bloki `<think>` kontra zachowujące je; llama.cpp ma domyślnie `preserve_reasoning` i flagi `--reasoning on|off|auto`, `--reasoning-format`.
7. **EOS vs EOT**: token końca tury (`<|im_end|>`, `<|eot_id|>`) to nie koniec tekstu; zły token stopu = ciągłe generowanie.
8. **Wstrzyknięcie przez tokenizację**: tekst użytkownika zawierający nazwę tokenu specjalnego zamieniony na token sterujący (stąd „znakowanie wejścia").

Dlaczego „po cichu": model nadal produkuje płynny tekst, tylko w trybie, na którym nie był trenowany. **Szczególnie groźne przy porównywaniu runtime'ów**: dwa programy z innym szablonem dla „tego samego" modelu mierzą szablon, nie silnik.

**Nie każdy model ma Jinja.** DeepSeek-V4 „nie zawiera szablonu czatu w formacie Jinja"; trzeba „odwołać się do skryptu `encoding_dsv4.py`" (karta modelu). Dlatego ds4 ma renderer natywnie w C; llama.cpp trzyma też zakodowaną starszą listę ~56 formatów (`src/llama-chat.cpp`) na wypadek wyłączonej Jinja.

**Parsery rozumowania.** Modele „myślące" emitują łańcuch rozumowania w ogranicznikach (`<think>…</think>`, kanały Harmony). Serwer rozdziela go na `reasoning_content` (llama.cpp, `--reasoning-format deepseek`) albo `reasoning` (vLLM — pole **zmieniono z `reasoning_content`**, stary klucz akceptowany na wejściu jako alias; `--reasoning-parser <nazwa>`) oraz `content`. Interakcja: **gramatyka musi startować po zakończeniu rozumowania**. Tryby rozumowania DeepSeek-V4: Non-think / High / Max (Max wymaga kontekstu ≥ 384K), wybierane przez renderer promptu; ds4 dokumentuje, że „zmiana poziomu w rozmowie przebudowuje jej zbuforowany prefiks" — *inny tryb = inny prefiks = brak trafienia w cache* (§5.2).

> **Sprawdź sam (12)**
> ```bash
> grep -n "2 BOS tokens" ~/llama.cpp-0ce8cd1/src/llama-vocab.cpp
> grep -n "reasoning_content\|reasoning-format" ~/llama.cpp-0ce8cd1/common/arg.cpp | head
> grep -n "reasoning_content" ~/runtimes-src/vllm/vllm/entrypoints/openai/chat_completion/protocol.py | head
> ```
> Ćwiczenie (nie uruchamiałem): pobierz `tokenizer_config.json` swojego modelu, wyrenderuj `chat_template` ręcznie (`python3` + `jinja2`) dla jednej wiadomości użytkownika i porównaj bajty z promptem w logu serwera, łącznie z końcowym nagłówkiem asystenta.

---

## 13. Determinizm i numeryka

- **Dodawanie zmiennoprzecinkowe nie jest łączne**: (a + b) + c ≠ a + (b + c). Każda zmiana *kolejności redukcji* zmienia ostatnie bity: inne jądra (split-K, kafle, WMMA vs skalarne), inne kształty batcha, inna liczba kart w all-reduce, inny backend, inny układ bloków kwantyzacji.
- Drobne różnice logitów mają znaczenie: argmax przeskakuje, gdy dwa tokeny są w granicach szumu, i kontynuacje się rozchodzą; przy próbkowaniu to samo ziarno wybiera inne tokeny. Dokumentacja llama.cpp: „stałe ziarno daje powtarzalne losowania, ale stochastyczne próbkowanie CPU i backendu może wciąż wybierać różne tokeny… Użyj próbkowania zachłannego, gdy potrzebne jest dokładne dopasowanie" (`docs/speculative.md`).
- **Prawdziwy winowajca w serwerach to brak niezmienniczości względem batcha.** Horace He / Thinking Machines (wrzesień 2025): 1000 identycznych odpowiedzi Qwen3-235B przy T = 0 dało **80 różnych wyników** (zgodnych przez pierwsze 102 tokeny); przyczyna: jądra, których strategia redukcji zależy od rozmiaru batcha, plus niedeterministyczne obciążenie serwera; poprawka: jądra niezmiennicze za ~2× spowolnienia *(dane autorów, wpis na blogu)*. vLLM ma `VLLM_BATCH_INVARIANT` (beta; **tylko** NVIDIA cc ≥ 8.0, AMD Instinct gfx90a/942/950 i Intel XPU — **nie** RDNA4; `docs/features/batch_invariance.md`), SGLang `srt/batch_invariant_ops/`.

**Konsekwencje** *(moje wnioskowanie z mechanizmu)*: (1) ten sam prompt z `-np 1` kontra `-np 4`, ze spekulacją lub bez, z kwantyzacją KV lub bez, albo po trafieniu w prefix cache **może dać inny wynik**; (2) llama.cpp, vLLM i MLX różnią się nawet przy T = 0; (3) spekulacja jest bezstratna *w rozkładzie*, nie bitowo — **dziennik wdrożenia w przyspieszanie-generowania to potwierdza**: przy T = 0 podział tensorowy dał odpowiedzi identyczne ze starymi 0 z 4 razy, warstwy z draftem 2 z 4; odpowiedzi, które czytałeś, były poprawne, ale jakości **nie zmierzyłeś** ([`README.md`](../przyspieszanie-generowania/README.md)); (4) właściwy test międzyruntime'owy jest **statystyczny**: perplexity / dywergencja KL na ustalonym tekście albo trafność zadań z przedziałami ufności (`tools/perplexity`, `tools/imatrix` istnieją; flaga trybu KL niezweryfikowana); (5) różnice kwantyzacji są dużo większe niż szum jąder *(rzędy wielkości niezweryfikowane)* — „ten sam model" znaczy „ten sam numerycznie" tylko przy tej samej kwantyzacji i zmierzonej różnicy jakości (rozdział 03).

> **Sprawdź sam (13)**
> ```bash
> grep -n -i "seed\|different tokens\|greedy" ~/llama.cpp-0ce8cd1/docs/speculative.md | head
> sed -n 1,40p ~/runtimes-src/vllm/docs/features/batch_invariance.md      # lista wspieranych GPU
> ```
> Ćwiczenie (nie uruchamiałem; **karty są produkcyjne**): wyślij tę samą krótką prośbę przy T = 0 trzy razy do serwera z jednym klientem, a potem trzy razy, gdy równolegle pracuje drugi. Jeśli odpowiedzi się rozjadą — masz własny dowód niezmienniczości względem batcha, nie błąd serwera.

---

## 14. Jak uczciwie mierzyć

| nazwa | definicja |
|---|---|
| **prefill (pp)** | tokeny promptu / czas prefillu |
| **dekodowanie (tg)** | wygenerowane tokeny / czas dekodowania (bez prefillu) |
| **end-to-end** | wygenerowane tokeny / (TTFT + czas dekodowania) — spada ostro przy długich promptach |
| **TTFT** | czas w kolejce + prefill (+ pierwszy krok) |
| **ITL** | odstęp między kolejnymi strumieniowanymi tokenami |
| **TPOT** | (opóźnienie end-to-end − TTFT) / (długość wyjścia − 1) |
| **goodput** | przepustowość żądań mieszczących się w SLO na TTFT/TPOT (metryka DistServe) |

ITL i TPOT to definicje, które liczy `benchmarks/serve.py` vLLM (`mean/median/p* ttft_ms, tpot_ms, itl_ms`, `request_goodput`).

**Na strumień a zbiorczo.** Przy B strumieniach zbiorcze tok/s = suma, a szybkość na strumień zwykle maleje. §4.2: przy B = 8 zbiorczo 249, na strumień 31, wobec 126 przy B = 1 *(moje wyliczenie)*. Na rigu referencyjnym: 1 agent 49,7; 2 agenty po 34,5 (razem 63). **Zawsze podawaj współbieżność.**

**Ze spekulacją i bez.** Spekulacja zmienia tg; raportuj trafność (`draft acceptance rate`) i rodzaj zadania, porównuj z bazą bez spekulacji **na tych samych promptach** (`tools/server/bench/speed-bench` w llama.cpp robi oba przebiegi z zyskiem per kategoria). Wdrożone wyniki referencyjne per zadanie (T = 0): tłumaczenie 51,9; wywołanie narzędzia 62,0; kod 58,5; proza 37,8 tok/s — ×1,6 różnicy *tylko z typu zadania*.

**Głębokość kontekstu.** tg spada z długością KV; `llama-bench -d N` wstępnie wypełnia N tokenów; raportuj dla kilku głębokości (0, 8k, 32k).

**Dlaczego `llama-bench` ≠ llama-server.** `llama-bench` mierzy `pp` (`-p`) i `tg` (`-n`) jednej sekwencji przez `llama_decode` ze stałymi `n_batch/n_ubatch`, `-r 5` powtórzeń: bez HTTP, szablonu, łańcucha samplerów, cache'u promptów i planowania slotów. llama-server dokłada HTTP/JSON, tokenizację, samplery (synchronizacja CPU w każdym tokenie), parsowanie gramatyk/narzędzi, cache promptów, checkpointy slotów, `--parallel`, i raportuje własne `timings` (`prompt_per_second`, `predicted_per_second`; `server-common.cpp`). Zwykle tg z `llama-bench` ≥ tg serwera o kilka procent *(niezweryfikowane)*.

**Lista kontrolna porównania runtime'ów**

1. **Przypnij** sprzęt, sterownik/ROCm, *rodowód* wag, kontekst, współbieżność, zestaw promptów (te same liczby tokenów), długość wyjścia (`ignore_eos`/`min_tokens`), parametry próbkowania (zachłanne dla szybkości, §13).
2. **Ta sama kwantyzacja między formatami jest niemożliwa**: GGUF Q4_K_M ≠ AWQ-INT4 ≠ MLX 4-bit g64 ≠ FP8; efektywne bity na wagę się różnią. Porównuj punkty **dopasowane jakościowo**: zmierz jakość każdego wariantu (perplexity/KL względem BF16 + 1–2 testy zadań z dużym n) i porównuj szybkość przy równej jakości albo rysuj front szybkość–jakość. Porównuj też **bajty na wagę**, bo szybkość ≈ przepustowość / bajty (§2).
3. **Rozgrzej** (JIT/autotuning, grafy CUDA, page cache, pierwszy dostęp `mmap`); ≥ 5 powtórzeń, średnia ± odchylenie, p50/p95; **wyłącz** prefix caching, gdy mierzysz prefill, i mierz *osobno* z włączonym (agenci żyją z trafień w cache).
4. **Nie mieszaj ustawień:** liczba z PR na RTX 4090 w bf16 (§9.5) nie jest liczbą dla R9700 przy Q3. Każda liczba niesie (sprzęt, runtime + build, model + kwantyzacja, współbieżność, kontekst, data).
5. **Benchmarki własne autorów** *(dane projektu)*: wszystkie tabele PR w tym rozdziale to ich przebiegi.

**Twój protokół na tym tle:** średnia z 4 zadań × 2 temperatury, jeden agent, build przypięty do SHA `0ce8cd1`, macierz 2×2 — solidna szybkość *na tej jednej maszynie*. Brakuje (i sam to piszesz) **pomiaru jakości** oraz pomiaru α. Zanim porównasz llama.cpp z vLLM na tym samym DeepSeeku, pamiętaj o punkcie 2.

> **Sprawdź sam (14)**
> ```bash
> sed -n 630,650p ~/runtimes-src/vllm/vllm/benchmarks/serve.py       # TPOT / ITL / goodput
> sed -n 80,110p ~/llama.cpp-0ce8cd1/tools/llama-bench/README.md      # -p, -n, -d, -r
> sed -n 85,100p ~/llama.cpp-0ce8cd1/tools/server/server-common.cpp   # pola timings serwera
> ```
> Ćwiczenie (nie uruchamiałem): z pola `timings` jednej odpowiedzi `llama-server` wylicz ręcznie tok/s prefillu, dekodowania i end-to-end. Który rośnie, a który spada, gdy prompt wydłużysz z 1 tys. do 20 tys. tokenów?

---

## 15. Co z tego dla konfiguracji referencyjnej

1. **Szybkość dekodowania ≈ przepustowość / bajty aktywnych wag.** Twoje ~50 tok/s to znacznie poniżej sufitu z §2 — przyczyn nie ustaliłem (§8.4). Skalibruj jądra najpierw na małym modelu gęstym.
2. **MoE nie skaluje się liniowo z liczbą agentów** (§4): drugi agent dał +27% zbiorczo (63 vs 49,7). Liczbę slotów ustalaj pomiarem; na rigu referencyjnym 2 × 98 304 wyszły najlepiej.
3. **Spekulacja na MoE działa, ale zysk jest mniejszy niż na gęstych** i zależy od zadania (§9): na rigu referencyjnym ×1,5–1,6, od ~38 (proza) do 62 tok/s (wywołanie narzędzia).
4. **Tryb tensorowy** jest eksperymentalny, wymaga nieskwantyzowanego KV i `-fa on`, jest wykluczony dla wielu architektur (§8.3) i kosztuje prefill (~960 → ~700 tok/s). Dla agentów czytających długie wyniki narzędzi to realny koszt — nie mierzyłem proporcji prefill/dekodowanie w zadaniach referencyjnych *(niezweryfikowane)*.
5. **Prefix caching to dźwignia nr 1 dla agentów** (§5.2): sprawdź `--cache-ram` (domyślnie 8 GiB), `--slot-prompt-similarity`, `--cache-reuse`, `--ctx-checkpoints`. Zmiana trybu rozumowania lub szablonu między turami unieważnia prefiks (§12).
6. **Szablon i parser to część konfiguracji modelu** (§12): przy każdym nowym modelu sprawdź szablon, tokeny stopu, parser narzędzi i pole rozumowania — błąd nie daje komunikatu, tylko gorszy model.
7. **Wywołania narzędzi:** gramatyka zwiększa niezawodność kosztem CPU i synchronizacji w każdym tokenie (§11); gramatyki leniwe oszczędzają to w wolnym tekście.
8. **Mierz uczciwie** (§14): współbieżność, głębokość kontekstu, baza bez spekulacji, jakość obok szybkości. Luką jest jakość.
9. **Mac:** odpowiedniki mechanizmów z tego rozdziału w mlx-lm (`PromptTrie`/`LRUPromptCache`, `RotatingKVCache`, `QuantizedKVCache`, `--draft-model`, `BatchGenerator`) — rozdział [`07`](07-APPLE-MLX-OMLX-I-DS4.md). Przepustowość pamięci zunifikowanej Maca to inna liczba wejściowa tego samego rachunku z §2 (jej wartości tu nie podaję).
10. **Dalej:** pliki i kwantyzacja — [`03`](03-KWANTYZACJA-I-FORMATY.md); silnik, który znasz — [`04`](04-LLAMA-CPP-I-RODZINA-GGML.md); alternatywy serwerowe — [`06`](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md); wybór — [`09`](09-POROWNANIE-I-WYBOR.md); spekulacja i podział tensorowy na rigu referencyjnym — [`../przyspieszanie-generowania/01-JAK-TO-DZIALA.md`](../przyspieszanie-generowania/01-JAK-TO-DZIALA.md).

---

## 16. Czego nie ustaliłem

1. **Oficjalne parametry R9700** (przepustowość, TFLOPS): strony AMD nie udało się pobrać; 640 GB/s to dane zewnętrzne i wyliczenie, 96 TFLOPS — niezweryfikowane. Wszystkie sufity w §2 od nich zależą.
2. **Topologia PCIe:** sysfs mówi x16 na czterech kartach, dziennik wdrożenia w przyspieszanie-generowania — że karty 1 i 3 są na x4; CPU ma ~28 linii. Rozstrzygnie `lspci -vv`.
3. **Czy P2P działa i czy RCCL by pomógł** — nie testowałem; dziennik też nie.
4. **Skąd ~30 ms stałego czasu na token** (§8.4) — hipotezy bez profilu. **Prawdziwa trafność α** i skośność routingu V4-Flash — niezmierzone.
5. **Czy jądra AITER działają i są szybkie na gfx1201** — kod pokazuje flagi RDNA, nie wynik.
6. **Rozbieżność DSpark:** dokumentacja llama.cpp (szkielet Qwen3) kontra dziennik wdrożenia w przyspieszanie-generowania (głowica z V4-Flash-0731).
7. **KV V4-Flash:** ~6,9 KB/token opiera się na założeniach z §3.1; „6,4" czy „6,7 GiB" przy 1M zależy od tego, czy 1M to 10⁶, czy 2²⁰.
8. **Wzory z treści prac** (granica I/O FlashAttention, tw. 3.8 Leviathana, próg top-n-sigma, reguła typical, aktualizacja Mirostat) — czytałem tylko abstrakty; **Prompt Lookup Decoding, flash-decoding, Williams (roofline), Vaswani** — z pamięci. **Praca o DSpark** i **strona arXiv DFlash** — nie pobrane. **Medusa** — „nie znaleziono grepem". **ONNX** i przechowywanie kwantów MLX — nie badane (rozdział 03).

---

## 17. Słowniczek

Termin polski · English · jedna linia (kolejność tematyczna).

| termin polski | English | jedna linia |
|---|---|---|
| autoregresywny | autoregressive | każdy token zależy od wszystkich poprzednich; generowanie jest z natury sekwencyjne |
| prefill, czytanie promptu | prefill / prompt processing (pp) | pierwszy przebieg po tokenach promptu naraz; ograniczony mocą obliczeniową |
| dekodowanie | decode / token generation (tg) | faza po jednym tokenie; ograniczona przepustowością pamięci |
| pamięć podręczna KV | KV cache | zapisane klucze i wartości uwagi wszystkich dotychczasowych tokenów |
| intensywność arytmetyczna | arithmetic intensity | FLOP na bajt z pamięci; decyduje, czy jądro jest ograniczone pamięcią, czy obliczeniami |
| roofline / punkt załamania | roofline / ridge point | szybkość = min(szczyt FLOPS, AI × przepustowość); punkt załamania to miejsce, gdzie się spotykają |
| MFU | model FLOPs utilisation | osiągnięte FLOPS podzielone przez szczytowe |
| czas do pierwszego tokenu | TTFT | czas w kolejce + prefill |
| opóźnienie między tokenami / czas na token | ITL / TPOT | odstęp między kolejnymi tokenami w fazie dekodowania |
| goodput | goodput | przepustowość tylko żądań, które zmieściły się w SLO opóźnień |
| MHA / MQA / GQA | multi-head / multi-query / grouped-query attention | uwaga z wieloma / jedną / kilkoma głowicami K-V |
| MLA | multi-head latent attention | (DeepSeek) cache trzyma niskowymiarowy wektor ukryty zamiast pełnych K/V |
| DSA | DeepSeek Sparse Attention | indekser wybiera top-k tokenów, na które liczy się uwagę |
| CSA / HCA | compressed / heavily compressed attention | (DeepSeek-V4) kompresja KV w osi czasu |
| SWA / iSWA | sliding-window / interleaved SWA | uwaga tylko na ostatnie W tokenów / przeplot warstw okienkowych i globalnych |
| RoPE | rotary position embedding | obraca pary Q/K o kąt zależny od pozycji; iloczyn zależy od odległości względnej |
| YaRN | YaRN | metoda skalowania RoPE do rozszerzania kontekstu |
| RMSNorm | RMSNorm | normalizacja przez pierwiastek ze średniej kwadratów, bez odejmowania średniej |
| SwiGLU | SwiGLU | FFN z bramką: W_down(SiLU(W_gate x) ⊙ W_up x) |
| eksperci (MoE) | mixture of experts | router wysyła token do top-k z wielu małych FFN |
| ekspert wspólny | shared expert | ekspert zawsze aktywny obok routowanych |
| parametry aktywne a łączne | active vs total parameters | aktywne = bajty/FLOP na token; łączne = zajętość pamięci |
| logity / softmax | logits / softmax | surowe wyniki dla słownika / normalizacja do prawdopodobieństw |
| łańcuch samplerów | sampler chain | uporządkowane przekształcenia logitów i końcowy wybór |
| min-p / top-p / top-k | min-p / top-p / top-k | obcinanie względem maksimum / po masie skumulowanej / po liczbie |
| XTC / DRY / Mirostat | XTC / DRY / Mirostat | usuń najlepsze wybory / kara za powtarzanie ciągów / regulator docelowej entropii |
| dekodowanie z gramatyką | grammar-constrained decoding (GBNF, xgrammar, llguidance, Outlines) | maskowanie logitów tak, by wynik pozostał w języku formalnym |
| maska tokenów | token mask / bitmask | zbiór dozwolonych identyfikatorów tokenów w danym kroku |
| wywoływanie narzędzi | tool calling | model emituje ustrukturyzowane wywołanie, serwer parsuje je do `tool_calls` |
| szablon czatu | chat template (Jinja) | serializacja wiadomości i narzędzi specyficzna dla modelu, dostarczana z nim |
| BOS / EOS / EOT | BOS / EOS / EOT | tokeny początku sekwencji / końca sekwencji / końca tury |
| parser rozumowania | reasoning parser | oddziela tekst myślenia od odpowiedzi (`reasoning_content` / `reasoning`) |
| PagedAttention | PagedAttention | KV w blokach z tablicą bloków, jak stronicowanie pamięci |
| prefix caching / RadixAttention | prefix caching / RadixAttention | ponowne użycie KV wspólnego początku promptu (łańcuch haszy / drzewo radix) |
| przesunięcie kontekstu | context shift | przesuwanie okna przez odrzucenie środka i ponowne obrócenie kluczy |
| slot | slot (llama.cpp) | współbieżna sekwencja serwera z własnym stanem, samplerem i promptem; liczba = `-np` |
| zunifikowane KV | unified KV | jedna wspólna pula komórek KV zamiast stałych strumieni na slot |
| ciągłe batchowanie | continuous batching | skład batcha ustalany w każdej iteracji; sekwencje dołączają i odchodzą (Orca) |
| chunked prefill | chunked prefill | cięcie długich promptów na kawałki mieszane z dekodowaniem, by uniknąć przestojów |
| dezagregacja prefill/decode | prefill/decode disaggregation | osobne pule GPU dla obu faz, KV przesyłane między nimi |
| FlashAttention | FlashAttention | kafelkowana, świadoma I/O, dokładna uwaga z online softmax |
| podział tensorowy / warstwowy / ekspertowy / danych | tensor / pipeline / expert / data parallelism | dzielenie wewnątrz warstw / między warstwami / między ekspertami / między replikami |
| all-reduce | all-reduce (NCCL / RCCL) | kolektyw sumujący tensory między kartami; RCCL to NCCL od AMD |
| speculative decoding | speculative decoding | zgadnij k tokenów tanio, zweryfikuj jednym przebiegiem modelu docelowego |
| trafność zgadywacza (α) | acceptance rate | ułamek przyjętych zgadywanych tokenów; E[tokeny] = (1−α^(k+1))/(1−α) |
| EAGLE / Medusa / MTP / DFlash / DSpark | EAGLE / Medusa / MTP / DFlash / DSpark | głowica na cechach / dodatkowe głowice / własna głowica wielotokenowa / zgadywacz dyfuzyjny blokowy / DFlash + głowica Markowa |
| spekulacja n-gramowa | n-gram / prompt-lookup speculation | zgaduje, kopiując kontynuacje widziane wcześniej w kontekście |
| GGUF / safetensors | GGUF / safetensors | samoopisujący się plik przyjazny kwantyzacji / bezpieczny kontener tensorów (rozdział 03) |
| kwantyzacja | quantisation (Q4_K, MXFP4, FP8, AWQ/GPTQ) | zapis wag w mniejszej liczbie bitów ze skalami (rozdział 03) |
| imatrix | importance matrix | macierz ważności do wyboru precyzji kwantyzacji tam, gdzie ma znaczenie (rozdział 03) |
| niezmienniczość względem batcha | batch invariance | wynik sekwencji nie zależy od tego, co jeszcze jest w batchu |
