# 04 · llama.cpp i rodzina ggml

**Po co ten rozdział.** To najgłębszy rozdział kursu, bo na llama.cpp stoi referencyjny system produkcyjny (cztery karty R9700, `llama-swap`, DeepSeek-V4-Flash w UD-IQ3_XXS). Po przeczytaniu będziesz umieć: (1) narysować z pamięci drogę jednego żądania HTTP aż do tokenu w strumieniu SSE; (2) wyjaśnić, czym jest tensor, graf, alokator i *scheduler* w bibliotece ggml oraz dlaczego mnożenie macierzy na wagach leżących w RAM-ie potrafi wylądować na GPU; (3) przeczytać nagłówek pliku GGUF bajt po bajcie; (4) rozumieć, dlaczego `-c 65536 -np 4` daje cztery sloty po 16384 tokeny; (5) wybrać tryb podziału na wiele GPU ze świadomością, co w nim jest eksperymentalne; (6) ocenić, kiedy zamiast „czystego" llama.cpp sięgnąć po ik_llama.cpp, llamafile, KoboldCpp, textgen albo llama-swap.

> ⚠️ **Niczego tu nie uruchamiałem.** Całość to desk research i czytanie kodu: drzewo źródeł `0ce8cd1` (build produkcyjny, commit z 2026-10-19) oraz API GitHuba z tego samego dnia. Nie mam własnych pomiarów szybkości, a komendy z ramek „Sprawdź sam" są wzięte z notatek badawczych, nie z mojej konsoli. Numery linii dotyczą tego drzewa i będą się przesuwać — upstream wydaje po kilka buildów dziennie.

**Spis treści**
1. Czym jest llama.cpp i gdzie leży w stosie (sieć zależności)
2. Biblioteka ggml: tensor, graf, alokator, backend i *scheduler* — z przykładem offloadu jednego matmula
3. GGUF: układ bajtów z adnotacjami
4. libllama: budowniczowie grafów per architektura, batch/ubatch, rozmiar kontekstu, klasy KV cache
5. Próbkowanie i gramatyki
6. llama-server od środka: pętla slotów, cache promptu, checkpointy, tryb routera, wbudowane narzędzia/MCP
7. Dekodowanie spekulacyjne: typy
8. Wiele GPU: trzy tryby podziału i co to znaczy dla 4×R9700
9. HIP: jak ROCm ponownie używa kodu CUDA i co jest specyficzne dla RDNA4
10. Narzędzia: bench, quantize, imatrix, fit
11. Rodzina: ik_llama.cpp, llamafile, KoboldCpp, textgen, whisper.cpp i ggml jako biblioteka, llama-swap
12. Kto za tym stoi
13. Pułapki
14. Co z tego dla konfiguracji referencyjnej

---

## 1. Czym jest llama.cpp i gdzie leży w stosie

**llama.cpp** to silnik wnioskowania napisany w C/C++: biblioteka (`libllama`), kilka narzędzi wiersza poleceń i serwer HTTP (`llama-server`). Wczytuje model z pliku GGUF i liczy go na CPU oraz na około piętnastu rodzajach akceleratorów. Zbudowany jest na bibliotece tensorowej **ggml** (organizacja `ggml-org` utrzymuje ją osobno, a jej kopia siedzi w `ggml/` wewnątrz llama.cpp). Repozytorium: `github.com/ggml-org/llama.cpp` (dawniej `ggerganov/llama.cpp`), licencja MIT, założone 2023-03-10. Stan na 2026-10-19 z API GitHuba: **131 716 gwiazdek, 24 555 forków, około 11 741 commitów i około 2 138 kontrybutorów** (z anonimowymi). Wersji semantycznych nie ma — „wersja" to numer buildu `bNNNNN`; najnowszy tag w dniu przeglądu to `b11741` (trzy wydania w ciągu poprzednich sześciu godzin). Twoje drzewo produkcyjne to commit `0ce8cd1` z tego samego dnia, czyli praktycznie bieżący HEAD.

### Trzy warstwy w jednym repozytorium

Pomaga rozdzielić trzy rzeczy, które w rozmowie zlewają się w „llama.cpp":

| Warstwa | Katalog | Rozmiar (linie, moje zliczenie z rigu) | Co robi |
|---|---|---|---|
| **ggml** — tensory, graf obliczeń, backendy | `ggml/` (`ggml/src` ≈ 514 tys. linii razem z backendami i shaderami) | ~514k | zna `ggml_tensor`, operacje, alokator, scheduler i wszystkie backendy (CUDA, HIP, Metal, Vulkan, …) |
| **libllama** — model, kontekst, KV cache, tokenizer, próbkowanie | `src/`, `include/llama.h` | ~112k (z tego `src/models/` ≈ 43k w 165 plikach) | wczytuje GGUF, buduje graf dla danej architektury, zarządza pamięcią KV, zamienia logity na tokeny |
| **aplikacje** — `common/`, `tools/` | `common/` ~44k, `tools/server` ~36k, `tools/mtmd` ~31k, … | | parsowanie flag, szablony czatu, gramatyki z JSON-schema, serwer, bench, quantize |

Granica ma znaczenie praktyczne: **ggml nie ma pojęcia KV cache, tokenizera ani próbkowania**. Dlatego gdy ktoś osadza ggml (whisper.cpp, stable-diffusion.cpp), pisze te elementy sam; a gdy ktoś chce LLM-a dekoderowego, bierze libllama.

### Mapa zależności

```
                    Hugging Face  (od 2026-02-20 zatrudnia rdzeń zespołu ggml.ai)
                          |
 ggml-org/ggml  <--sync--> ggml-org/llama.cpp (ggml/ + src/ + common/ + tools/) <--sync--> whisper.cpp
      |                         |
      |       +-----------------+--------------+-------------------+----------------+
      |       |                 |              |                   |                |
 stable-diffusion.cpp   Ollama (pin b11669)  LM Studio, Jan   llamafile (kopia,   KoboldCpp
 bark.cpp (uśpiony)     = proces llama-server  (używają       opóźniona o tygodnie) = wbudowany fork
                         + patche `llama/compat` llama.cpp)                          + launcher Python
      |
 ik_llama.cpp = fork z 2024, rozwijany osobno (kwanty IQ*_K, trellis)
 textgen (oobabooga) = uruchamia llama-server jako proces potomny
 llama-swap = proxy + menedżer procesów przed dowolnym serwerem zgodnym z OpenAI
```

Co z tej mapy jest zweryfikowane w kodzie lub w źródle pierwotnym:
- **Ollama** — w sklonowanym drzewie jest plik z przypiętą wersją `LLAMA_CPP_VERSION = b11669`, a `llama/README.md` mówi, że pobiera przypięte źródło, nakłada patche z `llama/compat/` i buduje `llama-server`. Nie znalazłem katalogu `ml/backend`, czyli dawnego silnika w Go na ggml już tam nie ma. Według tego drzewa Ollama jest w październiku 2026 orkiestratorem w Go wokół podprocesu llama.cpp (plus ścieżka MLX na Macu). To zmiana względem 2025 — szczegóły w `05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md`; tu tylko odnotowuję, że autor notatek prosi o potwierdzenie tego u badacza Ollamy.
- **LM Studio** — dokumentacja: działa na llama.cpp, a na Apple Silicon także na MLX (`lmstudio.ai/docs/app`). Aplikacja zamknięta.
- **Jan** — README wymienia llama.cpp jako fundament; licencja według API to NOASSERTION, a README mówi Apache-2.0.
- **ramalama, LocalAI, lemonade, Docker Model Runner** — nie sprawdzałem ich zależności od llama.cpp w tym rozdziale *(niezweryfikowane)*; zob. rozdział 05.

### Na co llama.cpp się *nie* porywa

Projekt deklaruje „plain C/C++ bez zależności" i „zero alokacji pamięci w trakcie działania" *(dane projektu, README ggml)*, a polityka współtworzenia mówi, że ma być „możliwie prosty" i prowadzony przez „mały zespół" (`AGENTS.md`). Nie jest serwerem klasy datacenter: nie ma PagedAttention, drzewa prefiksów, dojrzałego równoległego podziału tensorowego ani priorytetów i wywłaszczania żądań jak vLLM/SGLang (rozdział 06). Ma ciągłe batchowanie i sloty, ale znacznie prostszy *scheduler*. To wybór: najszersze wsparcie sprzętu i formatów kosztem wyrafinowania serwera.

---

## 2. Biblioteka ggml

### 2.1 Tensor to węzeł grafu

W ggml `struct ggml_tensor` (`ggml/include/ggml.h:685`) jest jednocześnie danymi i węzłem grafu. Pola, które trzeba znać:

| Pole | Znaczenie |
|---|---|
| `type` | typ elementu (`ggml_type`: F32, F16, Q4_K, …) |
| `ne[4]` | liczba elementów w każdym wymiarze (`GGML_MAX_DIMS 4`) |
| `nb[4]` | **kroki w bajtach** (strides) — dlatego widoki i transpozycje są darmowe, a typy kwantyzowane adresuje się per blok |
| `op`, `op_params[]` | jaka operacja (`enum ggml_op`) wytworzyła ten tensor |
| `src[10]` | do 10 wejść (`GGML_MAX_SRC 10`) |
| `view_src`, `view_offs` | jeśli to widok: czyj i z jakim przesunięciem |
| `buffer`, `data` | gdzie fizycznie leżą dane |
| `name[64]`, `extra` | nazwa debugowa; dane prywatne backendu |

**Analogia.** Zapis `c = ggml_mul_mat(ctx, a, b)` to nie obliczenie, tylko *wpisanie zamówienia*: powstaje tensor `c` z `op=MUL_MAT` i `src={a,b}`. Liczenie następuje dopiero, gdy ktoś wykona cały graf. **Precyzyjnie:** `ggml_context` to arena (bump allocator) trzymająca wyłącznie metadane tensorów (przy `no_alloc` — bez danych); dane żyją w osobnych buforach backendów.

Przykład kroków (moje wyliczenie, przy założeniu, że krok wiersza to liczba bloków razy rozmiar bloku): macierz wag 4096×4096 w Q4_K to 4096/256 = 16 bloków po 144 B na wiersz, czyli `nb[1]` = 2304 B, a całość 16 777 216 / 256 · 144 B ≈ 9,4 MB. Rozmiar bloku 144 B / 256 wag = 4,5 bita na wagę — zgodnie z komentarzem w `ggml-common.h`.

### 2.2 Graf: `ggml_cgraph`

`struct ggml_cgraph` (`ggml/src/ggml-impl.h:341`) trzyma tablicę `nodes` (tensory do obliczenia), `leafs` (stałe i wejścia), opcjonalnie gradienty (trening, `ggml-opt.cpp`), zbiór odwiedzonych tensorów, liczniki użyć i `uid`. Ten `uid` pozwala `llama_context` rozpoznać identyczny graf i go **użyć ponownie** (`can_reuse`, `src/llama-context.cpp:1521`) zamiast budować od zera przy każdym ubatchu. Domyślny rozmiar: `GGML_DEFAULT_GRAPH_SIZE = 2048` węzłów.

### 2.3 Pamięć: bufory, typy buforów, alokator

Dane leżą w **buforach backendów** (`ggml_backend_buffer`), a każdy bufor ma **typ bufora** (`ggml_backend_buffer_type`): CPU, CPU przypięty (host/pinned), urządzenie CUDA, bufor „split" CUDA, współdzielony Metal, urządzenie Vulkan itd. To rozróżnienie jest kluczem do reszty rozdziału: o tym, *gdzie liczyć operację*, decyduje m.in. to, *w jakim buforze leży waga*.

`ggml-alloc.c` (1 173 linie) to alokator grafu: wylicza czasy życia tensorów i odzyskuje pamięć, a gdzie operacja na to pozwala (`ggml_op_can_inplace`), liczy w miejscu. „Zero alokacji w trakcie działania" realizowane jest tak: libllama **rezerwuje najgorszy przypadek grafu raz** (`llama_context::graph_reserve`, `sched_reserve`, `src/llama-context.cpp:715–830, 2621`), a każdy kolejny decode używa już gotowych buforów obliczeniowych.

### 2.4 Backendy

Rejestr backendów (`ggml-backend-reg.cpp`) potrafi ładować backendy jako biblioteki współdzielone (`ggml-backend-dl.cpp`, opcja `GGML_BACKEND_DL`). Każde urządzenie (`ggml_backend_dev_*`) odpowiada na pytania: `supports_op` (czy umiem tę operację na tych tensorach), `supports_buft` (czy znam ten typ bufora), `offload_op` (czy warto mi ją zlecić, nawet jeśli waga leży gdzie indziej). Wykonanie podgrafu to `ggml_backend_*_graph_compute`.

W drzewie są backendy (katalogi pod `ggml/src`): CPU (x86 AVX/AVX2/AVX512/AMX, ARM NEON/SVE/KleidiAI, RISC-V, POWER, s390x, LoongArch, WASM), CUDA, **HIP/ROCm**, MUSA (Moore Threads), Metal, Vulkan, SYCL, OpenCL (Adreno), WebGPU, CANN (Ascend), Hexagon (Qualcomm), OpenVINO, zDNN (IBM Z), ZenDNN (AMD CPU), BLAS/BLIS, RPC, VirtGPU oraz `ggml-et`, którego celu nie sprawdzałem *(niezweryfikowane)*. Największe: `ggml-opencl` ~76 tys. linii, `ggml-sycl` ~51 tys., `ggml-cuda` ~49 tys. (164 pliki plus 121 instancji szablonów), `ggml-vulkan` ~48,6 tys. (w tym 188 plików ~16,4 tys. linii shaderów GLSL), `ggml-metal` ~33 tys. (z czego ~15 tys. to kernele `.metal`), CPU ~95 tys. Katalog `ggml-hip` ma zero linii kodu — to tylko `CMakeLists.txt` (zob. §9).

### 2.5 Scheduler: serce heterogeniczności

`ggml_backend_sched` (`ggml/src/ggml-backend.cpp`, ok. linii 900–2300) bierze jeden graf i **przypisuje każdemu węzłowi backend**, a potem tnie graf na **splity** — ciągłe kawałki wykonywane przez jeden backend — wstawiając kopie tensorów tam, gdzie backend się zmienia. Stałe: `GGML_SCHED_MAX_BACKENDS 16`, `GGML_SCHED_MAX_SPLIT_INPUTS 30`, `GGML_SCHED_MAX_COPIES 4` (więcej niż jedna kopia tylko przy `parallel=true`, co pozwala potokować kopie wejść i używać zdarzeń).

Reguły przypisania (funkcja `ggml_backend_sched_backend_id_from_cur`, linie 1069–1130), w kolejności:

1. **Cel już zaalokowany.** Jeśli bufor docelowy węzła (albo bufor jego `view_src`) jest już przydzielony, węzeł przypina się do backendu tego bufora (komunikaty debugowe „1.dst"/„1.vsrc"). Jeśli ten bufor nie potrafi wykonać operacji, program się przerywa.
2. **Wejścia grafu** (tokeny, pozycje) trafiają do **ostatniego backendu — zakładanego jako CPU** („1.inp").
3. **„Operacje z wagami najchętniej na tym samym backendzie co wagi"** — z wyjątkiem `ROPE` i `FLASH_ATTN_EXT`, których małe tensory boczne nie są wiarygodną wskazówką.
4. **Reguła offloadu operacji (op-offload).** Jeśli waga leży w pamięci **hosta** (typ bufora CPU), a `sched->op_offload` jest włączone, scheduler pyta kolejno backendy o wyższym priorytecie: `supports_op && offload_op`. Pierwszy, który się zgodzi, wykonuje operację („1.off"). Dla CUDA/HIP `offload_op` zwraca `get_op_batch_size(op) >= op_offload_min_batch_size`, gdzie próg domyślnie wynosi **32** i można go zmienić zmienną środowiskową **`GGML_OP_OFFLOAD_MIN_BATCH`** (`ggml-cuda.cu:180–183, 6011–6015`).
5. **Dalsze przebiegi** propagują przypisanie na jeszcze nieprzypisane węzły, sprawdzając `supports_op` i zgodność typów buforów (sprawdzenia widać w okolicach linii ~1370 i ~1391; dokładnej liczby przebiegów nie wyliczałem).

### 2.6 Przykład: jak jedno mnożenie macierzy na wagach z RAM-u trafia na GPU

Wyobraź sobie model MoE, w którym tensory ekspertów trzymasz w RAM-ie (flaga `-ot` z wyrażeniem regularnym wskazującym tensory i docelowym typem bufora; dokładną składnię sprawdź w `--help`, nie uruchamiałem), a resztę — uwagę, normy — na GPU. Weźmy jedno mnożenie `ffn_up` na wadze leżącej w buforze CPU. Poniższy przebieg **złożyłem z reguł opisanych wyżej i w kodzie `ggml-backend.cpp`; nie śledziłem go w debugerze** *(moje wnioskowanie)*:

```
(1) ŁADOWANIE   llama-model-loader mmapuje GGUF; waga ffn_up trafia do bufora typu CPU
                (bo override-tensor / brak miejsca na GPU).
(2) BUDOWA      build_ffn()/build_lora_mm() -> ggml_mul_mat(ctx, W_ffn_up, cur)
                = węzeł MUL_MAT, src = {W_ffn_up [bufor CPU], cur [aktywacje]}.
(3) REZERWACJA  graph_reserve: najgorszy przypadek (ubatch 512) -> scheduler przypisuje
                backendy i alokuje bufory obliczeniowe raz.
(4) PODZIAŁ     split_graph, dla tego węzła:
                  reguła 1: cel jeszcze nie zaalokowany            -> nie dotyczy
                  reguła 3: waga w buforze CPU                     -> kandydat: CPU
                  reguła 4: waga w pamięci hosta, op_offload włączone
                            -> pytanie do GPU: supports_op && offload_op?
                               offload_op = (rozmiar batcha operacji >= 32)
                  prefill, ubatch 512 :  512 >= 32  -> TAK -> węzeł dla GPU ("1.off")
                  dekodowanie, batch 1:    1 <  32  -> NIE -> węzeł zostaje na CPU
(5) KOPIE       tam, gdzie sąsiednie węzły mają inny backend, scheduler wstawia kopie
                tensorów; przy offloadzie waga leci z RAM-u do GPU (notatki mówią:
                „streamed to the GPU"). Mechanizmu kopii bajt po bajcie nie czytałem.
(6) WYKONANIE   split po splicie: backend_graph_compute() na swoim kawałku.
```

**Konsekwencja, którą da się zmierzyć samemu:** przy częściowo odciążonym modelu **prefill przyspiesza ze wzrostem `-ub`** (więcej wierszy w operacji ⇒ próg 32 przekroczony i opłaca się przesyłać wagi na GPU), a **generowanie tokenów (batch 1) zostaje na CPU**. Dla ciebie to ważne w jednym przypadku: jeśli kiedykolwiek część ekspertów DeepSeeka wyląduje w RAM-ie, prefill i dekodowanie będą się zachowywać zupełnie różnie.

> **Sprawdź sam #1 — reguła offloadu.** Otwórz `ggml/src/ggml-backend.cpp` i przejdź do funkcji `ggml_backend_sched_backend_id_from_cur` (linie ok. 1069–1130); znajdź komentarze „1.dst", „1.inp", „1.off". Potem `grep -n "GGML_OP_OFFLOAD_MIN_BATCH" ggml/src/ggml-cuda/ggml-cuda.cu` — powinieneś trafić na próg 32. *(Komendy z notatek; nie uruchamiałem.)*

### 2.7 Bloki kwantyzacji w jednym akapicie

Szczegóły formatów są w rozdziale 03; tutaj tylko to, co potrzebne do czytania kodu. Waga kwantyzowana to **blok + skala**. `block_q4_0` = fp16 `d` + 16 B półbajtów dla 32 wag = 18 B / 32 = **4,5 bpw**. K-kwanty używają **super-bloków 256 wag** (`QK_K = 256`) z drugim poziomem kwantyzacji: `block_q4_K` = fp16 `d`, fp16 `dmin`, 12 B spakowanych 6-bitowych skal i minimów oraz 128 B półbajtów = 144 B / 256 = **4,5 bpw**; `block_q6_K` = 210 B = 6,5625 bpw. i-kwanty (IQ*) używają tablic kratowych/słownikowych, np. `block_iq2_xxs` = 2,0625 bpw, a `IQ4_XS` = 4,25 bpw. **MXFP4**: 1 B skali E8M0 + 16 B półbajtów E2M1 dla 32 wag = 17 B = 4,25 bpw (format OCP z gpt-oss); **NVFP4**: 64 wagi = 4 skale UE4M3 + 32 B = 36 B = 4,5 bpw. Enum `ggml_type` ma w tym drzewie `GGML_TYPE_COUNT = 43` (nowe: Q1_0 o 1,125 bpw i Q2_0 o 2,25 bpw).

Dlaczego „blok + skala", a nie jedna skala na tensor? Jądra mnożące (`mmq`, `mmvq`, na CPU `vec_dot`) **kwantyzują kolumnę aktywacji w locie** do Q8_0/Q8_1/Q8_K i liczą iloczyny skalarne na int8 per blok, mnożąc potem przez dwie skale. Typ `block_q8_K` istnieje wyłącznie jako format aktywacji dla iloczynów K-kwantów.

---

## 3. GGUF: układ bajtów

GGUF to jedyny format modelu, który llama.cpp wczytuje (zostaje jeszcze skrypt `convert_llama_ggml_to_gguf.py` dla starych `.bin`; checkpointy HF konwertuje `convert_hf_to_gguf.py`). Definicja: `ggml/include/gguf.h` (komentarz nagłówkowy) i `ggml/src/gguf.cpp` (opiekun modułu: Johannes Gäßler). Wszystko little-endian:

```
offset 0
+----------------------------------------------------------------+
| magic  "GGUF"                                  (4 B)           |
| version  uint32  = 3  (GGUF_VERSION)                           |
| n_tensors  int64                                               |
| n_kv       int64                                               |
+----------------------------------------------------------------+
| n_kv razy:                                                     |
|   key        : string  = uint64 długość + bajty (bez NUL)      |
|   value_type : enum gguf_type                                  |
|                u8,i8,u16,i16,u32,i32,f32,bool,string,array,    |
|                u64,i64,f64                                     |
|   value      : wartość; dla array: typ elementu + u64 liczba   |
|                + elementy                                      |
+----------------------------------------------------------------+
| n_tensors razy (opis tensora, BEZ danych):                     |
|   name    : string                                             |
|   n_dims  : uint32                                             |
|   ne[]    : int64 x n_dims                                     |
|   type    : ggml_type                                          |
|   offset  : uint64  (przesunięcie wewnątrz bloku danych)       |
+----------------------------------------------------------------+
| wypełnienie do granicy general.alignment (domyślnie 32)        |
+----------------------------------------------------------------+
| blok danych: tensory jeden za drugim, każdy też wyrównany      |
+----------------------------------------------------------------+
```

Trzy konsekwencje, które warto zapamiętać:

1. **Plik jest samoopisujący się.** Hiperparametry leżą w kluczach `<arch>.context_length`, `<arch>.block_count`, `<arch>.attention.head_count` itd.; tokenizer w `tokenizer.ggml.tokens`, `tokenizer.ggml.merges`, `tokenizer.chat_template`. Nie potrzeba osobnego `config.json`.
2. **Wyrównanie umożliwia `mmap`.** Skoro dane są ciągłe i wyrównane, loader (`llama-model-loader.cpp:560–691`, sprawdzenie wyrównania w linii 691) mapuje plik w pamięć i oddaje backendom wskaźniki wprost do niego. Stąd „model wczytał się w sekundę", a właściwe czytanie z dysku dzieje się leniwie.
3. **Duże modele są cięte:** `llama-gguf-split` tworzy pliki `*-00001-of-0000N.gguf`.

Tryby ładowania (`include/llama.h:207`): AUTO(-1), NONE, MMAP, MLOCK, MMAP_MLOCK i **DIRECT_IO**; dodatkowo tryb *lazy* (OFF/AUTO/ON) czyta z dysku tylko wiersze dużych tensorów oznaczonych przez architekturę (np. ekspertów MoE) i tylko dla tensorów większych niż 4 GiB.

> **Sprawdź sam #2 — nagłówek GGUF.** Przeczytaj komentarz na początku `ggml/include/gguf.h` i porównaj z diagramem wyżej. Dla własnego pliku: pierwsze cztery bajty (`head -c 4 model.gguf`) powinny dać `GGUF`. *(Nie uruchamiałem.)*

---

## 4. libllama

### 4.1 Jedna architektura = jedna klasa C++

Każda architektura to klasa w `src/models/<arch>.cpp` (plik wzorcowy: `src/models/llama.cpp`, 248 linii). Nadpisuje trzy rzeczy:

1. `load_arch_hparams(ml)` — czyta klucze GGUF do `hparams`;
2. `load_arch_tensors(ml)` — deklaruje oczekiwane tensory, np. `create_tensor(tn(LLM_TENSOR_ATTN_NORM,"weight",i), {n_embd}, flags)`; warstwy MoE dostają trójwymiarowe tensory `ffn_{gate,up,down}_exps` o kształcie `{n_embd, n_ff, n_expert}`;
3. `build_arch_graph(params)` — zwraca podklasę `llm_graph_context`, której **konstruktor jest przejściem w przód**: embedding → dla każdej warstwy {`build_norm`, QKV przez `build_lora_mm` (dokłada poprawki LoRA), RoPE, `build_attn` (zapisuje K/V do cache przez `ggml_set_rows`, czyta je z powrotem jako widoki, woła `ggml_flash_attn_ext` albo wersję bez fuzji), `build_ffn` albo `build_moe_ffn`} → norma wyjściowa → `lm_head` tylko dla wierszy z `inp_out_ids`.

Wspólne klocki są w `src/llama-graph.cpp` (4 265 linii); reszta infrastruktury: `llama-model.cpp` (3 985), `llama-model-loader.cpp` (1 876), `llama-arch.{cpp,h}`, `llama-hparams`, `llama-vocab.cpp` (4 696 linii: tokenizery BPE/SPM/WPM/Unigram/RWKV). W `src/llama-arch.h` jest 163 trafień `LLM_ARCH_*` (razem ze strażnikami), a `src/models/` ma 165 plików — czyli około 160 architektur: gęste i MoE, hybrydy uwaga+SSM (Mamba/Mamba2, Jamba, Granite-hybrid, Nemotron-H, Falcon-H1, LFM2, Kimi-Linear, typ Qwen3-Next z delta-net), RWKV, enkodery typu BERT, T5, modele dyfuzyjne i rodziny DeepSeek V2/V3.2/V4 ze specjalnymi cache'ami uwagi.

**Wniosek praktyczny:** dodanie nowej architektury to nowy plik z grafem, a nie zmiana silnika. To tłumaczy, czemu nowe modele pojawiają się w llama.cpp w ciągu dni — i czemu każde wydanie może coś zepsuć w twojej konkretnej architekturze. W drzewie jest nawet `skills/add-new-model` (instrukcje dla agentów-kontrybutorów).

### 4.2 Gdzie lądują warstwy

Przy `LLAMA_SPLIT_MODE_LAYER` (domyślnym) warstwy trafiają na urządzenia proporcjonalnie do wolnej pamięci albo wg `--tensor-split`; **typ bufora wag warstwy i jej KV cache idzie za nią** (`llama_kv_cache` przyjmuje `layer_filter_cb` i alokuje K/V danej warstwy na jej urządzeniu). Wagi można przypiąć wyrażeniem regularnym (`--override-tensor`, `-ot`) — standardowy trik: eksperci FFN w RAM-ie, uwaga na GPU. Nowy plik `src/llama-moe-cache.{h,cpp}` trzyma **ostatnio używanych ekspertów warstw MoE z hosta w buforze urządzenia**, sterowany przez callback kopiowania schedulera (według komentarza w nagłówku). Automat `--fit` (`common/fit.cpp`, `common_fit_params`) dobiera `-ngl`, podział tensorów i nadpisania, by model + kontekst zmieściły się w wolnej pamięci; jest domyślnie włączony i **nie działa z trybem podziału tensorowego**.

### 4.3 Kontekst, batch i ubatch

- **`llama_batch`** (`include/llama.h:264`): `n_tokens`, `token[]` albo `embd[]`, `pos[]`, `n_seq_id[]`, `seq_id[][]` (token może należeć do kilku sekwencji — tak współdzieli się prompt), `logits[]` (dla których pozycji chcemy wyjście).
- **`n_batch`** = batch logiczny (`-b`, domyślnie **2048**), **`n_ubatch`** = batch fizyczny (`-ub`, domyślnie **512**) (`common/common.h:458–459`). `llama_batch_allocr` czyści batch i **tnie go na `llama_ubatch`** (`src/llama-batch.h:17`; pola `n_tokens`, `n_seq_tokens`, `n_seqs`, `n_seqs_unq`, `n_pos` — 4 dla M-RoPE — i flaga `equal_seqs` wymagana przez modele rekurencyjne).
- **`llama_context::decode`** (`src/llama-context.cpp:1821`): `memory->init_batch(balloc, n_ubatch, embd_all)` tworzy *kontekst pamięci*, który już wie, gdzie w KV cache trafi każdy ubatch; potem pętla {`mctx->apply()` (zatwierdza slot, może defragmentować lub przesunąć) → `process_ubatch` (zbuduj lub **użyj ponownie** graf, `ggml_backend_sched_alloc_graph`, ustaw wejścia, `graph_compute`) → odczytaj logity} aż `mctx->next()` zwróci fałsz (linie 1925–2165).

### 4.4 Rozmiar kontekstu: pułapka `-c / -np`

To najczęstsze zaskoczenie przy serwerze, więc rozbieram ją dokładnie.

- W `llama-context.cpp:379–391`: **`n_ctx_seq = n_ctx / n_seq_max`** (zaokrąglone do 256), *chyba że* ustawiono `kv_unified`. W `llama_context_default_params` (linia 4012) `kv_unified` domyślnie **fałsz**; `n_seq_max` domyślnie 1 (linia 3981).
- Serwer przekazuje `--parallel` jako liczbę slotów. Jak dokładnie wartość trafia do `n_seq_max`, nie prześledziłem *(niezweryfikowane)*, ale konsekwencja jest opisana w kodzie flag.
- **Efekt:** przy domyślnym, niejednolitym cache `-c 65536 -np 4` daje **4 sloty × 16 384 tokenów**, każdy z własnym „strumieniem" KV. Pojedyncza rozmowa agenta, która urośnie do 30 tys. tokenów, w takim slocie się nie zmieści (co serwer zrobi wtedy, zależy m.in. od `--context-shift`, §6.4).
- **Wyjście:** `--kv-unified` — „pojedynczy ujednolicony bufor KV współdzielony przez wszystkie sekwencje; domyślnie włączony, jeśli liczba slotów jest automatyczna" (`common/arg.cpp:1728`). Wtedy każdy slot ma dostęp do całej puli `n_ctx`, a sekwencje przeplatają się w jednym strumieniu. `--kv-unified-per-slot` ogranicza kontekst slotu przy puli ujednoliconej (`server-context.cpp:1357–1372`).
- Domyślnie `-np` = 1; tekst pomocy mówi, że `-1` = auto (`common/common.h:462`, `arg.cpp:2548`).

Rachunek płatności: sloty niejednolite rezerwują `n_ctx / N` na stałe, nawet gdy stoją puste; pula ujednolicona jest elastyczna, ale sekwencje konkurują o te same komórki.

> **Sprawdź sam #3 — dzielenie kontekstu.** `grep -n "kv_unified" src/llama-context.cpp` i przeczytaj okolice linii 379–391. Potem `grep -n "kv-unified" common/arg.cpp`. W logu startowym twojego `llama-server` szukaj informacji o kontekście na slot (nie sprawdzałem, jak dokładnie jest sformułowana). *(Nie uruchamiałem.)*

### 4.5 Klasy pamięci KV (`src/llama-kv-cache*.{h,cpp}`, `llama-memory*.{h,cpp}`, ~11 tys. linii)

Interfejs `llama_memory_i` / `llama_memory_context_i` (`llama-memory.h`): `init_batch`, `init_full`, `init_update` (defragmentacja/przesunięcie), `seq_rm/cp/keep/add/div`, `state_read/write` (zapis i odczyt sesji) oraz obiekt *kontekstu* per ubatch, który stosuje zmianę.

| Klasa | Co przechowuje | Po co |
|---|---|---|
| `llama_kv_cache` (`llama-kv-cache.h:20`, `.cpp` 2 962 linie) | pierścień **komórek** (`llama-kv-cells.h`), każda z pozycją i zbiorem id sekwencji; K i V per warstwa (typy `-ctk/-ctv`, domyślnie f16, `q8_0`/`q4_0` możliwe z flash-attn) | standardowa uwaga; `slot_info` mapuje token ubatcha na komórkę (zapis przez `ggml_set_rows`, więc nieciągłe rozmieszczenie jest tanie); *unified* = jeden strumień, nie-unified = strumień na sekwencję |
| `llama_kv_cache_iswa` | **dwa** obiekty `llama_kv_cache`: pełny dla warstw globalnych i mały (≈ okno + ubatch, chyba że `swa_full`) dla warstw z oknem przesuwnym | Gemma-2/3, gpt-oss, styl Llama-4; tokeny starsze niż okno są **utracone**, więc ponowne użycie prefiksu wymaga checkpointów serwera |
| `llama_memory_recurrent` (1 386 linii) | stały stan na sekwencję (Mamba/RWKV: conv+ssm, delta-net) — „jedna komórka na sekwencję" | nie da się cofnąć po pozycji ⇒ checkpoint/restore dla dekodowania spekulacyjnego i cache'u promptu |
| `llama_memory_hybrid` (+ `-idx`, `-iswa`) | `llama_kv_cache` dla warstw uwagi + `llama_memory_recurrent` dla warstw SSM w jednym modelu | Jamba, Granite-hybrid, Nemotron-H, Falcon-H1, LFM2 |
| `llama_kv_cache_dsa`, `_dsv4` (2 257 linii), `_msa` | cache specyficzne dla schematów uwagi DeepSeek (rzadka uwaga z „lightning indexer", skompresowany KV ze stanem kompresji, selekcja bloków) | pokazują, jak szybko lądują nowe mechanizmy uwagi: graf i cache są per architektura; są dedykowane jądra CUDA (`lightning-indexer.cu`, `dsv4-hc.cu`) |

⚠️ Ostatni wiersz dotyczy modelu referencyjnego: w drzewie produkcyjnym istnieje dedykowana klasa cache `llama_kv_cache_dsv4`. Nie sprawdzałem, którą dokładnie klasę i jądra uruchamia DeepSeek-V4-Flash w UD-IQ3_XXS ani czy jądra `dsv4-hc.cu` są kompilowane dla HIP *(niezweryfikowane)*.

**Czego tu nie ma:** w libllama nie ma PagedAttention ani tablic bloków, ani drzewa prefiksów między żądaniami. Ponowne użycie prefiksu robi serwer: (a) trzyma KV slotu na miejscu i dopasowuje najdłuższy wspólny prefiks, (b) ma RAM-owy **cache promptu** zapisanych stanów slotów, (c) tworzy **checkpointy kontekstu** (§6).

---

## 5. Próbkowanie i gramatyki

**Próbnik** (`llama_sampler`, `src/llama-sampler.cpp`, 4 391 linii) to tablica wirtualna (`accept`, `apply` na `llama_token_data_array`, `reset`, `clone`), a **łańcuch** (`llama_sampler_chain`) stosuje je po kolei. Zaimplementowane: greedy, dist (końcowe losowanie), top-k, top-p, min-p, typical, temp/temp_ext (temperatura dynamiczna), XTC, mirostat v1/v2, top-n-sigma, **DRY**, kary (powtórzeń/częstości/obecności), logit-bias, infill, **adaptive-p** oraz **grammar** (zachłanna i leniwa). Domyślna kolejność w `common_params` (`common/common.h:265–271`): kary → DRY → top-n-sigma → top-k → typical → top-p → min-p → … → temperatura; `common/sampling.cpp` buduje łańcuch z `--samplers`. Istnieje też ścieżka próbkowania na GPU (`llama-context.cpp:1398`, z blokadą dla podziału tensorowego); jej zakres nie był sprawdzany.

**Gramatyki GBNF** (`src/llama-grammar.cpp`) to automat ze stosem po punktach kodowych UTF-8. W każdym kroku **maskowane są wszystkie tokeny słownika, które złamałyby gramatykę** — dla dużych słowników i złożonych gramatyk bywa to wolne. `common/json-schema-to-grammar.cpp` kompiluje JSON-schema do GBNF. **Gramatyki leniwe** (`llama_sampler_init_grammar_lazy_patterns`) włączają się dopiero po wyzwalaczu (np. token/regex początku wywołania narzędzia), więc rozumowanie w wolnym tekście zostaje nieograniczone — to mechanizm, na którym stoi wywoływanie narzędzi.

**LLGuidance**: opcjonalna biblioteka w Ruście (`-DLLAMA_LLGUIDANCE=ON`; gramatyki zaczynające się od `%llguidance` idą do niej); `docs/llguidance.md` podaje ~50 µs średnio na maskę dla słownika 128k *(dane projektu)*.

Wywoływanie narzędzi i struktura odpowiedzi zależą jeszcze od: szablonów Jinja (`common/jinja/`), „autoparsera" (`common/chat-auto-parser*.cpp`, `docs/autoparser.md`), parserów PEG (`common/peg-parser.cpp`, `common/parsers/`) i obsługi budżetu rozumowania (`common/reasoning-budget.cpp`).

---

## 6. llama-server od środka

### 6.1 Droga żądania

```
 klient (curl, agent)
    |  POST /v1/chat/completions   (OpenAI)  |  /v1/messages (Anthropic)  |  /v1/responses
    v
 server-http.cpp (cpp-httplib) ---> parsowanie, szablon czatu, gramatyka --> server_task
    |
    v
 KOLEJKA ZADAŃ (server-queue.cpp)
    |
    v                                          +-----------------------------+
 PĘTLA SLOTÓW  update_slots()  (jeden wątek)   |  sloty: server_slot x N     |
    |  pre_decode():                           |  prompt, próbnik, LoRA,     |
    |   - przesunięcie kontekstu (jeśli pełny) |  kontekst draftu,           |
    |   - składa BATCH: 1 token na slot, który |  checkpointy                |
    |     generuje + kawałki promptu slotów    +-----------------------------+
    |     w prefillu, do n_batch
    v
 batch.render() ---> llama_decode(ctx, batch)
    |                   |  tnie na ubatch (n_ubatch), memory->init_batch
    |                   v
    |              graf ggml (build_arch_graph) --> ggml_backend_sched
    |                   |        split po splicie: GPU0, GPU1, ..., CPU
    |                   v
    |              logity (tylko wiersze z inp_out_ids)
    v
 post_decode():  próbnik slotu (łańcuch + gramatyka) -> token
    |             warunki stopu, checkpoint, ewentualna weryfikacja draftu
    v
 kolejka odpowiedzi (server_response) ---> SSE: "data: {...}\n\n" ---> klient
```

Szczegóły, które odpowiadają polom w kodzie (`tools/server/server-context.cpp`, ~6,3 tys. linii; cały katalog `tools/server` ~36 tys., z czego ok. 25 tys. to C++ bez testów):

- `server_context_impl` (linia 941) posiada `n_parallel` obiektów **`server_slot`** (linia 245); każdy ma własne tokeny promptu, łańcuch próbników, opcjonalny kontekst draftu, zestaw LoRA i „context checkpoints".
- **`update_slots`** (linia 3256): jeśli wszystkie sloty są bezczynne — wróć; w przeciwnym razie wyślij zadanie NEXT_RESPONSE; `pre_decode()`; `batch.render(off, n)` i `decode(...)` w pętli po oknach `n_batch`, z automatycznym ponowieniem przy mniejszym batchu, gdy zabraknie miejsca w KV; `post_decode()`.
- **Ciągłe batchowanie** (*continuous batching*) jest domyślnie włączone (`cont_batching = true`, wyłączenie: `-nocb`; `common/common.h:575`). To batchowanie „na poziomie iteracji": nowe żądania dołączają w następnej iteracji; nie ma osobnych faz prefill/decode ani polityki priorytetów poza budżetem batcha *(szczegółów polityki nie czytałem)*.
- **Wybór slotu**: żądanie z `id_slot` trafia do wskazanego slotu; w przeciwnym razie serwer wybiera slot z **najdłuższym zgodnym prefiksem promptu** (LCP), a gdy brak dopasowania — najdawniej używany wolny slot (okolice `server-context.cpp:1780–1815`; ogólny zarys sprawdzony, nie linia po linii).
- **Liczba slotów** (`-np/--parallel`): domyślnie 1; każdy slot dostaje `n_ctx / N` tokenów, o ile nie `--kv-unified` (§4.4).

### 6.2 Cache promptu w RAM

Gdy slot ma zostać użyty do innego promptu, jego tokeny i **zserializowany stan llama** (cel + draft) są zapisywane do RAM-u (`prompt_save`), a `prompt_load` odtwarza najlepsze dopasowanie dla nowego żądania (`server_prompt_cache`, `server-task.h:668`). Domyślnie **`--cache-ram 8192` MiB** (`-1` = bez limitu, `0` = wyłączone), z limitem również w tokenach równym `n_ctx`; `--cache-idle-slots` (domyślnie włączone, wymaga `--cache-ram`) zapisuje bezczynne sloty do cache'u, gdy przychodzi nowe zadanie (`common/common.h:642`, `arg.cpp:1719–1745`, `server-context.cpp:1494–1520`).

Dlaczego to ważne dla agentów: pętla agenta wysyła za każdym razem **rosnący prefiks** (system prompt + historia + narzędzia). Bez cache'u każde żądanie liczyłoby go od zera; z cache'em liczysz tylko nowy ogon.

### 6.3 Checkpointy kontekstu

`-ctxcp/--ctx-checkpoints N` (domyślnie **32** na slot), odstęp `-cms/--checkpoint-min-step` (domyślnie **8192** tokenów). Po co: modele z oknem przesuwnym (SWA) i rekurencyjne/hybrydowe **nie potrafią „zapomnieć" ogona** — stanu nie da się obciąć do wcześniejszej pozycji (§4.5). Serwer więc **robi migawki stanu pamięci w trakcie prefillu**, żeby późniejsze żądanie ze wspólnym prefiksem mogło odtworzyć najbliższą wcześniejszą migawkę zamiast liczyć wszystko od nowa. Checkpointy trafiają też do plików zapisu `/slots` i służą do cofania odrzuconych tokenów w dekodowaniu spekulacyjnym (`server-context.cpp:2544–2700`, `arg.cpp:1701`). **Koszt:** pamięć RAM.

### 6.4 Przesunięcie kontekstu

`--context-shift`: gdy slot zapełni `n_ctx`, odrzuca starszą połowę niechronionych tokenów i przesuwa pozycje (`llama_memory_seq_rm/add`). Nie wszystkie typy pamięci to wspierają. Dla agentów to groźne cicho: model „zapomina" początek rozmowy bez komunikatu.

### 6.5 Tryb routera (wielu modeli)

Uruchomiony **bez `-m`**, ale z `--models-dir PATH` (skan katalogu GGUF), `--models-preset FILE` (presety w stylu INI, `common/preset.cpp`, `docs/preset.md`) albo z cache HF. `--models-max N` (domyślnie **4**) ogranicza jednocześnie załadowane modele (`server-models.{h,cpp}`, ok. 3 000 + 486 linii; `common/common.h:695–699`; `arg.cpp:3663–3680`).

Router to cienki proces, który **uruchamia osobny potomny `llama-server` na model** (`common/subproc.cpp`; komendy `cmd_router_to_child:exit`, `cmd_child_to_router:state:` przez stdout), kieruje żądania wg pola `"model"`, śledzi stany `DOWNLOADING/DOWNLOADED/UNLOADED/LOADING/LOADED/SLEEPING`, **wywłaszcza najdawniej używany bezczynny model**, gdy kolejka potrzebuje miejsca (`server_lru_sched`, `server-models.cpp:270–400`), i obsługuje `--sleep-idle-seconds` (potomek zwalnia wagi po bezczynności i później się budzi). To wbudowany „mini llama-swap" z LRU zamiast grup/macierzy (porównanie w §11.6). Dodatkowe punkty końcowe: `POST /models`, `/models/load`, `/models/unload`, `GET /models/sse`, `DELETE /models`.

### 6.6 Powierzchnia API

Zarejestrowana w `tools/server/server.cpp` (linie ~256–386): zgodne z OpenAI `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/models`, **`/v1/responses`** (Responses API), `/v1/audio/transcriptions`, `/v1/rerank`; **Anthropic `/v1/messages` i `/v1/messages/count_tokens`**; zliczanie tokenów (`/v1/chat/completions/input_tokens`, `/v1/responses/input_tokens`); stare `/completion`, `/infill`, `/embedding`, `/tokenize`, `/detokenize`, `/apply-template`; `/props`, `/slots` (GET oraz POST `/slots/:id_slot` do zapisu/odczytu), `/lora-adapters`, `/metrics` (Prometheus), `/health`; wznawialne strumienie `/v1/stream`, `/v1/streams/lookup`; oraz `/v1/systemone` — typowane „modele decyzyjne", które odpowiadają na pytania wyboru/oceny jednym przejściem bez generowania tokenu (`server-decision.h`). Wbudowany interfejs WWW (Svelte, `tools/ui`) jest osadzony w serwerze (`--ui/--no-ui`). Brak telemetrii: przeszukano `common`, `tools`, `src`, `ggml/src` pod kątem telemetry/analytics/posthog/sentry — bez trafień; sprawdzenia aktualizacji nie znaleziono *(nie przeszukiwałem wyczerpująco)*. Tryb `--offline` / `LLAMA_ARG_OFFLINE` (`common/arg.cpp:3953`) blokuje sieć.

### 6.7 Wbudowane narzędzia i MCP — oraz ostrzeżenie

Nowość: `llama-server --tools read_file,file_glob_search,grep_search,exec_shell_command,write_file,edit_file,get_info` (lub `all`), `--tools-runtime docker:<obraz>|podman:<obraz>|docker-container:<id>|ssh:<cel>` do izolowania wykonania narzędzi, `--mcp-servers-config PATH` / `--mcp-servers-json` (format `mcpServers` zgodny z Cursorem; klient MCP po stronie serwera w `server-mcp.cpp`), oraz `--agent` = wszystkie narzędzia + CORS/proxy MCP. Wszystko oznaczone w kodzie jako eksperymentalne, z komunikatem „nie włączaj w niezaufanych środowiskach", z ograniczeniem `--cors-origins` do localhost (`common/arg.cpp:3437–3490`; `tools/server/server-tools.{h,cpp}`, `server-mcp.{h,cpp}`).

> ⚠️ **Uwaga bezpieczeństwa.** `--tools` z `exec_shell_command`, `write_file` i `edit_file` to **wykonywanie kodu na hoście dla każdego, kto dotrze do portu serwera**. Nie włączaj tego na instancji osiągalnej z sieci, a jeśli musisz eksperymentować — używaj `--tools-runtime docker:…` i adresu `127.0.0.1`. Podobnie `ggml-rpc-server` (`tools/rpc`): README nazywa go „proof-of-concept … kruchy i niebezpieczny; nigdy w otwartej sieci".

---

## 7. Dekodowanie spekulacyjne

Idea (z katalogu o przyspieszaniu): dekodowanie jest ograniczone przepustowością pamięci, więc **sprawdzenie kilku tokenów zaproponowanych przez tani „draft" kosztuje niewiele więcej niż jednego**. Serwer weryfikuje draft w jednym batchowanym decode; dla celów hybrydowych/rekurencyjnych używa **checkpointów** do cofania odrzuconych tokenów (`spec_ckpt`, `server-context.cpp:266, 1388`). Implementacja: `common/speculative*.{h,cpp}` (`speculative.cpp` 3,1 tys. linii + `ngram-*`), dokument `docs/speculative.md`. Typy (`common_speculative_type`, `common/common.h:175–186`), wybierane `--spec-type` i `--spec-draft-n-max`:

| Typ | Skąd bierze propozycje | Uwagi |
|---|---|---|
| `DRAFT_SIMPLE` | osobny mały model (`-md`) | klasyczny wariant; potrzebny ten sam tokenizer |
| `DRAFT_EAGLE3` | lekka głowica EAGLE-3 | `docs/speculative.md` wymienia drafty dla Llama-3.x, Qwen3, gpt-oss, Gemma-4; konwersja `convert_hf_to_gguf.py --target-model-dir` |
| `DRAFT_MTP` | głowice przewidywania wielu tokenów **wewnątrz modelu** (np. warstwy NextN) | `llama-imatrix` ma flagi `--nextn`/`--model-draft` do zbierania statystyk dla tych warstw |
| `DRAFT_DFLASH` | draft dyfuzyjny blokowy, emituje cały blok na przebieg | |
| `DRAFT_DSPARK` | DFlash + głowica Markowa | |
| `NGRAM_SIMPLE`, `NGRAM_MAP_K`, `NGRAM_MAP_K4V`, `NGRAM_MOD`, `NGRAM_CACHE` | **bez modelu draftu**: propozycje z n-gramów już widzianego tekstu (`ngram-*.cpp`) | darmowe; dobre przy kodzie i powtarzaniu fragmentów (np. echo wywołań narzędzi) |

Warianty można mieszać („implementacja z modelem draftu może być mieszana z implementacją bez modelu"). Starsze `examples/{speculative,lookahead,lookup}` nadal są w drzewie. Czy twój model ma głowice MTP lub dostępny jest dla niego draft EAGLE-3/DFlash, **nie sprawdzałem** *(niezweryfikowane)*; wyniki dla sprzętu i modelu referencyjnego są w `../przyspieszanie-generowania/README.md`.

---

## 8. Wiele GPU: trzy tryby i 4×R9700

Flaga `-sm/--split-mode` (`include/llama.h:200`, `docs/multi-gpu.md`, `ggml/src/ggml-backend-meta.cpp`). Obrazek, co robi każdy tryb (cztery GPU, jedna warstwa = jeden prostokąt):

```
LAYER (domyślny) — rurociąg (pipeline)       TENSOR (eksperymentalny) — meta backend
 token -> GPU0 -> GPU1 -> GPU2 -> GPU3          każda warstwa rozcięta na 4 kawałki naraz
                                                                          
 GPU0: warstwy  0..15   [########]              GPU0: [shard 0 każdej warstwy]
 GPU1: warstwy 16..31   [########]              GPU1: [shard 1 każdej warstwy]
 GPU2: warstwy 32..47   [########]              GPU2: [shard 2 każdej warstwy]
 GPU3: warstwy 48..63   [########]              GPU3: [shard 3 każdej warstwy]
                                                          \  |  |  /
 między GPU: 1 tensor aktywacji na granicę          ALLREDUCE po sumach częściowych
 w danej chwili liczy JEDEN GPU (dla 1 tokenu)      (NCCL / RCCL / wersja zastępcza)
                                                    kilka redukcji na warstwę

ROW (przestarzały): wiersze wag gęstych dzielone między GPU; unikaj, `--fit` go odrzuca
NONE: cały model na `--main-gpu`
```

(Liczby warstw w obrazku są ilustracją, nie parametrami modelu referencyjnego.)

| Tryb | Co faktycznie robi kod | Konsekwencje dla 4×R9700 |
|---|---|---|
| `none` | cały model na `--main-gpu` | |
| **`layer`** (domyślny) | **równoległość potokowa**: ciągłe wycinki warstw na GPU, KV warstwy *l* na GPU, który ją posiada; ruch między kartami = jeden tensor aktywacji na granicę; proporcjonalnie do pamięci lub `-ts` | najlepsza przepustowość promptu, odporny na wolne PCIe; **generowanie tokenów nie przyspiesza od liczby GPU** — dla jednego tokenu pracuje jeden GPU naraz; dokumentacja: skaluje się dobrze dopiero przy wielu tokenach |
| `row` | **przestarzały** starszy podział wierszy dla wag gęstych (`llama-model.cpp:1198–1203`) | unikaj; `--fit` go odmawia |
| **`tensor`** | **równoległość tensorowa przez „meta backend"** (`ggml-backend-meta.cpp`, 2 546 linii): *meta urządzenie* opakowuje N prawdziwych; każdy tensor dostaje stan podziału (`SPLIT_AXIS_0..3`, `MIRRORED`, `PARTIAL` = każdy GPU ma sumę częściową, `NONE`) z callbacku per architektura; operacje liczą się na każdym GPU na jego kawałku, a wyniki `PARTIAL` łączy **allreduce** — przez NCCL (CUDA) lub RCCL (HIP, `-DGGML_HIP_RCCL=ON`, **domyślnie wyłączone**, bo „nie było uniwersalnie korzystne") z uniwersalnym zapasem (`ggml_backend_comm_allreduce_tensor`, `allreduce_fallback`) | **EKSPERYMENTALNY**; wymaga włączonego flash-attn i **niekwantyzowanego KV (f32/f16/bf16)**; `--fit` nieobsługiwany (ustaw `-c` ręcznie); dokumentacja *wprost* wymienia architektury bez implementacji, m.in. DeepSeek2, GLM-DSA, Nemotron-H, Granite-hybrid, LFM2-MoE, Minimax-M2, Mistral4, Kimi-Linear, Jamba, Falcon-H1, Mamba/Mamba2, Gemma-3n, OLMoE; „wydajność powinna być dobra dla wielu GPU NVIDIA z backendem CUDA, **bez gwarancji poza tym**" (`docs/multi-gpu.md`). Zmienna `GGML_CUDA_P2P=1` włącza kopie peer-to-peer (opt-in; przy włączonym IOMMU może psuć wynik) |

Dokumentacja: tryb `tensor` jest „znacznie bardziej ograniczony szybkością interkonektu" i robi wiele redukcji na warstwę; tryb `layer` „minimalizuje transfery … ale potrzebuje wielu tokenów, żeby dobrze się skalować".

### Co to znaczy dla sprzętu referencyjnego

1. Cztery R9700 to AMD z backendem HIP — dokładnie przypadek „bez gwarancji". Tryb `tensor` **nie ma tu żadnej obietnicy** od projektu (dane projektu). Czy działa i czy przyspiesza dekodowanie na gfx1201, zależy od twoich własnych pomiarów, nie od tego rozdziału.
2. Lista architektur bez implementacji `tensor` zawiera `DeepSeek2` i `GLM-DSA`. **DeepSeek-V4 nie występuje w niej z nazwy**, ale w kodzie nie ma też jawnego potwierdzenia, że jest wspierany (w praktyce na maszynie referencyjnej tryb tensorowy z DeepSeek-V4-Flash uruchomił się i dał zmierzony wzrost szybkości; jakości po zmianie nie mierzyłem — zob. §14 i `../przyspieszanie-generowania/`) — sprawdź aktualną listę w `docs/multi-gpu.md` swojego drzewa *(niezweryfikowane)*.
3. W trybie `layer` dodawanie kart zwiększa pojemność (128 GB łącznej VRAM, 4×32), nie szybkość pojedynczego strumienia. Ruch między kartami to tylko aktywacje na 3 granicach.
4. `tensor` wymaga **niekwantyzowanego KV** — to więcej pamięci na kontekst niż `q8_0`. Dla modelu, który i tak ledwo mieści się w pamięci, to realny koszt.
5. Praktyczna wiedza z tuningu tego sprzętu (spekulacja, podział tensorowy) leży w katalogu `../przyspieszanie-generowania/README.md`.

> **Sprawdź sam #4 — status trybu tensor.** Przeczytaj `docs/multi-gpu.md` w swoim drzewie: sekcję o `-sm tensor`, listę nieobsługiwanych architektur i zdanie o „no guarantees". Sprawdź też `grep -n "GGML_HIP_RCCL" ggml/src/ggml-hip/CMakeLists.txt`. *(Nie uruchamiałem.)*

---

## 9. HIP: jak ROCm ponownie używa kodu CUDA

**Nie ma osobnego drzewa jąder ROCm.** `ggml/src/ggml-hip/CMakeLists.txt` zbiera glob `../ggml-cuda/*.cu` (oraz `template-instances/fattn-tile*, fattn-mma*, mmq*, mmf*` i generowane instancje `fattn-vec`) i **kompiluje te same źródła jako HIP** (`LANGUAGE HIP` lub `hipcc` jako C++), definiuje `GGML_USE_HIP` i linkuje `hip`, `hipblas`, `rocblas` (wymagany HIP ≥ 6.1). Warstwą tłumaczącą jest `ggml/src/ggml-cuda/vendors/hip.h` (313 linii; rodzeństwo: `cuda.h` 28, `musa.h` 161) — około 300 makr `#define` mapujących nazwy CUDA na HIP: `cudaMalloc→hipMalloc`, `cudaStream_t→hipStream_t`, `cublasGemmEx→hipblasGemmEx`, `CUBLAS_COMPUTE_32F→HIPBLAS_COMPUTE_32F`, `__shfl_sync(mask,…)→__shfl(…)` (bez maski).

**Analogia:** to jak kompilowanie tego samego programu pod inny system operacyjny przez warstwę zgodności, zamiast pisania go na nowo. **Precyzyjnie:** każdy kernel CUDA w drzewie jest jednocześnie kernelem AMD; ścieżki specyficzne dla AMD to bloki `#if defined(GGML_USE_HIP) && defined(RDNA4)…` w `common.cuh`.

### RDNA4 / gfx1201

- `common.cuh` (linie 83–94, 280–282): stała `GGML_CUDA_CC_RDNA4` = offset AMD + 0x1200 („RX 9000"); `AMD_WMMA_AVAILABLE` włączone dla RDNA3/RDNA4 (mnożenie macierzy na jednostkach WMMA).
- Dedykowany nagłówek strojenia **`mmq-config-rdna4.cuh`** — obok `-rdna3`, `-rdna3-5`, `-rdna2`, `-cdna`, `-gcn`, `-ampere`, `-blackwell`, `-pascal-*`. Czyli kwantyzowane mnożenie macierzy (`mmq`) ma osobne parametry kafelków dla kart R9700.
- Opcje CMake: `GGML_HIP_GRAPHS`, `GGML_HIP_NO_VMM`, `GGML_HIP_MMQ_MFMA` (CDNA/seria MI, nie R9700), `GGML_HIP_RCCL`, `GGML_HIP_EXPORT_METRICS`, `GGML_CUDA_FORCE_MMQ/CUBLAS`, `GGML_CUDA_FA`. Dawna opcja `GGML_HIP_ROCWMMA_FATTN` **nie występuje** w CMake HIP tego drzewa (sprawdzone przez brak) — jeśli widzisz ją w starych poradnikach, jest nieaktualna.
- Budowanie (`docs/build.md:387–427`, w dokumentacji przykłady dla gfx1030/gfx1100):

```bash
HIPCXX="$(hipconfig -l)/clang" HIP_PATH="$(hipconfig -R)" \
  cmake -S . -B build -DGGML_HIP=ON -DGPU_TARGETS=gfx1201 -DCMAKE_BUILD_TYPE=Release
```

  `HIP_VISIBLE_DEVICES` wybiera karty. Cel `GPU_TARGETS` ma być dokładnie twoim `gfx` (zob. pułapki).
- **Alternatywa dla AMD: Vulkan** (utrzymują 0cc4m i Jeff Bolz z NVIDIA według `CODEOWNERS`). Nie mam danych porównawczych HIP vs Vulkan na gfx1201.

---

## 10. Narzędzia

- **`llama-bench`** (`tools/llama-bench/llama-bench.cpp`, 2,5 tys. linii): przemiata `-p` (długości promptu), `-n` (długości generowania), `-pg`, `-b/-ub`, `-t`, `-ngl`, `-sm`, `-ts`, `-fa`, `-ctk/-ctv`, `-r` (powtórzenia, domyślnie 5); wypisuje md/csv/json/jsonl/sql; obsługuje `--rpc` i `--fit-target`. Raportuje **pp** (prefill) i **tg** (generowanie) w tok/s. To kanoniczny benchmark; wyniki z `README` bez linii „sprzęt/model/precyzja" nie są porównywalne.
- **`llama-quantize`**: tablica `QUANT_OPTIONS` ma ~40 receptur (Q1_0, Q2_0, MXFP4_MOE, TQ1_0/TQ2_0, IQ1…IQ4, Q2_K…Q8_0, F16/BF16). Adnotacje perplexity w źródle (np. Q4_K_M „4,58G, +0,1754 ppl @ Llama-3-8B", Q8_0 „7,96G, +0,0026") to liczby projektu *(dane projektu; `tools/quantize/quantize.cpp:34–71`)*.
- **`llama-imatrix`**: `llama-imatrix -m f16.gguf -f calib.txt -ngl 99 -o imatrix.gguf`, potem `llama-quantize --imatrix imatrix.gguf in.gguf out.gguf Q4_K_M`. Pliki imatrix są dziś domyślnie GGUF (stare `.dat`, gdy rozszerzenie na to wskazuje); `--process-output` domyślnie wyłączone; `--nextn`/`--model-draft` zbierają statystyki dla warstw MTP/NextN (`tools/imatrix/README.md`). Macierz ważności mówi kwantyzatorowi, które wagi bardziej bolą przy zaokrągleniu — kluczowe dla niskobitowych kwantów typu IQ3_XXS (rozdział 03).
- **`llama-fit-params`** i `common/fit.cpp`: wyznacza `-ngl`, podział i nadpisania tak, by zmieściło się w pamięci (§4.2).
- Pozostałe: `llama-cli` (1,3 tys. linii), `llama-perplexity` (2,1 tys.), `llama-batched-bench`, `llama-gguf-split`, `llama-export-lora`, `llama-cvector-generator`, `llama-tokenize`, `llama-tts`, `ggml-rpc-server`.

---

## 11. Rodzina

### 11.1 ik_llama.cpp — fork nastawiony na szybkość i kwanty

**Co to:** fork Iwana Kawrakowa (autora k-kwantów i i-kwantów), powstały 2024-06-27; `github.com/ikawrakow/ik_llama.cpp`, MIT, **3 311 gwiazdek, 494 forki** (2026-10-19), ok. 5 080 commitów (z odziedziczoną historią llama.cpp), jedyny tag `t0002` z 2025-07-22 — pracuje się z `main`. Według README (*dane projektu*) ostatnia synchronizacja z upstreamem była w sierpniu 2024, a późniejsze modele (DeepSeek-V4, GLM-5, Qwen3.x, Gemma4, Mistral 4) przenoszono ręcznie (ponad 70 modeli).

**Czym różni się od upstreamu** *(dane projektu, README i `docs/parameters.md`)*:
- kwanty, których upstream nie ma: rodzina `IQ2_K…IQ6_K`, `IQ2_KS…IQ5_KS`, `IQ4_KSS`; warianty przeplatane wierszami dla CPU (`_R4/_R8/_R16`); **kwanty trellis** `IQ1_KT…IQ4_KT`; `IQ1_BN/IQ2_BN` (BitNet); `Q8_KV` (8-bitowy KV cache);
- flagi: `-fmoe` (fuzja MoE), `-muge`, `-mqkv`, `-ger`, `-ser` (mniej aktywnych ekspertów), `-rtr` (przepakowanie w czasie ładowania), `-mla`/`-amb` (warianty MLA dla DeepSeek), `-khad/-vhad` (transformata Hadamarda K/V), `-ot`, oraz **`-sm graph`** — „split mode graph" dla wielu GPU (dzieli tensory *i* graf obliczeń; README: „bardzo skuteczny dla modeli gęstych i MoE");
- MTP dla GLM-4.x MoE, fuzja delta-net dla Qwen3-Next/Qwen3.5-MoE, cache ekspertów MoE (`Implement moe cache #2644`, 2026-10-12).

**Kiedy go wybrać:** CPU lub hybryda CPU+GPU z dużym MoE na „128 GB RAM + jedna karta". **Dla rigu referencyjnego:** README podkreśla CPU (AVX2+/NEON) i CUDA (Turing+); Metal i HIP istnieją, ale jako druga kategoria; HIP dla gfx1201 nie jest udokumentowanym celem *(niezweryfikowane)*. Pliki z kwantami IQ_K/KT ładują się **tylko** w ik_llama.cpp — blokada formatu; czy numery typów nie kolidują z nowymi typami mainline (Q1_0, Q2_0, NVFP4, MXFP4), nie sprawdzałem. Serwer jest rozwidlony ze starszej wersji; trybu routera nie znalazłem. **Nie zakładaj, że bije mainline na AMD** — wszystkie dowody szybkości są autorskie lub z postów użytkowników (setupy różne), więc nie cytuję liczb.

**Kto za tym stoi.** Osoba prywatna, bez firmy i finansowania; Kawrakow opuścił llama.cpp w marcu 2024. Napięcie z upstreamem jest udokumentowane jego własnymi słowami (dyskusje #316 „Mainline is now copying stuff from ik_llama.cpp" z 2025-04-06 oraz #319): spór dotyczy atrybucji i interpretacji licencji MIT; jednocześnie praca przepływa w obie strony (np. dyskusja #2417 z 2026-09 o przeniesieniu nowych kwantów do mainline). Szczegóły w `10-PIENIADZE-I-LUDZIE.md`.

### 11.2 llamafile — jeden plik, który działa wszędzie

**Co to:** pakiet Mozilla.ai wiążący build llama.cpp (oraz whisper.cpp, stable-diffusion.cpp i transcribe.cpp) w jeden **„Actually Portable Executable"** zbudowany na Cosmopolitan Libc, który działa na sześciu systemach i dwóch architekturach CPU, opcjonalnie z wagami w środku. `mozilla-ai/llamafile` (dawniej `Mozilla-Ocho/llamafile`), założone 2023-09-10, **26 441 gwiazdek**, najnowsze wydanie **0.10.6 z 2026-09-15**.

**Czym różni się od upstreamu:**
- **Wagi w pliku wykonywalnym** przez wyrównane archiwum ZIP — po `mmap` wskaźniki idą wprost do GPU; dlatego autor napisał własny `zipalign` (`docs/technical_details.md`). Windows ma limit 4 GB na plik wykonywalny, więc tam wagi muszą być zewnętrzne.
- **Piaskownica domyślnie:** `pledge()` (SECCOMP-BPF na Linuksie, natywnie na OpenBSD) z obietnicami `stdio anet rpath` — proces może `accept()`, ale nie `connect()`, nie może zapisywać ani uruchamiać nowych procesów; opcjonalnie `unveil()` (Landlock) przez `--confine-reads`; pomijana w trybie GPU (`docs/security.md`).
- **0.10.0** przepisał system budowania (BUILD.mk, bez cmake); llama.cpp i whisper.cpp jako podmoduły z łatami `llama.cpp.patches/`. Upstream jest śledzony ręcznie: „Update llama.cpp to b10441" (2026-08-21), „b11100" (szkic z 2026-09-30) wobec b11741 upstreamu — **opóźnienie rzędu 600 buildów (tygodnie)**.
- Jądra CPU (tinyBLAS, `sgemm`, `iqk_mul_mat*`) trafiły z czasem do upstreamu (`ggml-cpu/llamafile/`), więc przewaga szybkości CPU z 2024 w większości zniknęła. Jest też nowy `agentfile`.

**Kiedy:** wysłać model koledze na laptop bez instalowania czegokolwiek. **Dla rigu:** nieprzydatny do serwowania (ROCm wymaga ręcznego budowania). Wzorzec do skopiowania: odmowa `connect()` dla serwera wnioskowania — możesz odtworzyć ją w systemd (`RestrictAddressFamilies`, seccomp) wokół `llama-server` *(mój pomysł, nie sprawdzany)*. Licencja: GitHub pokazuje NOASSERTION, bo plik `LICENSE` zawiera tylko krótką notkę Apache-2.0, a nie pełny tekst; README mówi: projekt Apache-2.0, zmiany w llama.cpp i whisper.cpp MIT.

**Kto za tym stoi.** Mozilla.ai; projekt wystartował jako Mozilla Builders z Justine Tunney jako główną autorką (600 commitów), a w 2026 prawie wszystkie commity robi `aittalam` (Davide Eynard, Mozilla.ai). Kwoty finansowania Mozilla.ai nie ustaliłem. Zob. `10-PIENIADZE-I-LUDZIE.md`.

### 11.3 KoboldCpp — wszystko w jednym dla opowieści i roleplayu

**Co to:** `LostRuins/koboldcpp`, AGPL-3.0, **12 032 gwiazdki**, założone 2023-03-16, wydanie **v1.123.1 z 2026-10-13** (dwa wydania miesięcznie). „One File. Zero Install." Rdzeń: jeden **plik `koboldcpp.py` o rozmiarze ok. 786 KB** (serwer HTTP, launcher w Tk, kolejka wielu użytkowników, tryb admina, wiązania `ctypes`) + natywna biblioteka z `kcpp_src/` (`gpttype_adapter.cpp` 351 KB) zlinkowana z **wbudowanym forkiem ggml/llama.cpp**; gałąź `upstream` jest scalana do `concedo`. Dochodzą: stable-diffusion.cpp, whisper, TTS, generowanie obrazu/wideo/muzyki, interfejs **KoboldAI Lite**, MCP i agent.

**Czym różni się od upstreamu:** funkcje UX nad tym samym ggml — **Context Shifting** (domyślnie włączony dla GGUF, `--noshift`), `--smartcontext`, **SmartCache** (`--smartcache X`, migawki KV w RAM-ie per rozmowa), `--multiuser`, `--admin/--admindir` z plikami `.kcpps`, `--routermode` (wymiana modeli wg pola `model`) *(dane projektu, wiki)*. Zachowuje starsze ładowarki ggml v1/v2/v3 (`otherarch/`: GPT-2, GPT-J, GPT-NeoX, MPT, RWKV) dla bardzo starych modeli.

**Sprzęt:** CUDA, **Vulkan (zalecana ścieżka dla AMD)**, Metal, CPU; **ROCm tylko przez fork firm trzecich** `YellowRoseCx/koboldcpp-rocm` („sprawdź stan utrzymania"). **Dla rigu referencyjnego:** gfx1201 oznaczałby Vulkan, a serwerowo nie ma powodu porzucać mainline. Warto podejrzeć: pomysły SmartCache, pliki `.kcpps` jako profile i zestaw `kcpp_adapters/*.json` do wykrywania szablonów czatu. **Uwaga licencyjna:** AGPL — wystawienie zmodyfikowanej wersji przez sieć zobowiązuje do udostępnienia źródeł; dla własnego, niezmodyfikowanego użytku wewnętrznego zwykle bez problemu, w produkcie sprawa do przeglądu prawnego.

**Kto za tym stoi.** Jeden twórca (LostRuins, 4 374 własnych commitów), bez firmy, bez zaobserwowanego finansowania (README i FUNDING.yml bez trafień; brak listingu GitHub Sponsors).

### 11.4 text-generation-webui, dziś „textgen" (oobabooga)

**Co to:** interfejs WWW (Gradio) do lokalnych LLM-ów, przemianowany na aplikację desktopową; repozytorium `oobabooga/textgen` (stara nazwa `text-generation-webui` nadal się rozwiązuje), AGPL-3.0, **47 738 gwiazdek**, założone 2022-12-21, wydanie **v4.9 z 2026-05-20**, ostatni push 2026-08-17. To **nie jest silnik**: *steruje* silnikami — llama.cpp przez `llama-server`, ExLlamaV3, TensorRT-LLM i Transformers; przełączanie bez restartu. Ścieżka llama.cpp uruchamia **`llama-server` jako proces potomny** i rozmawia po HTTP (commity: „Update llama.cpp", „Bind llama-server to parent process lifetime"). Kodu integracji nie czytałem w głąb.

**Kiedy:** majsterkowanie, szablony postaci, trening LoRA, szybkie porównania backendów. **Dla rigu:** wartość to wzorzec „silnik jako osobny proces, UI go nie linkuje" — dzięki temu restart silnika nie zabija UI. Cadence wydań zwolnił (ostatnie wydanie 2026-05).

**Kto za tym stoi.** Pseudonimowy pojedynczy twórca (oobabooga, ok. 82% commitów); README podaje grant od Andreessen Horowitz z sierpnia 2023 *(dane projektu)*; istnieje listing GitHub Sponsors.

### 11.5 ggml jako biblioteka do osadzenia, whisper.cpp

`ggml-org/ggml` (MIT, założone 2022-09-18, **15 509 gwiazdek**) ma od niedawna **numerowane wydania** (v0.26.0 z 2026-10-05 i v0.27.0 z 2026-10-15). Ten sam kod żyje w `llama.cpp/ggml/` i `whisper.cpp/ggml/`; zmiany płyną przez PR-y „sync: ggml" i **kopia w llama.cpp jest świeższa** niż samodzielne repozytorium dla dużych backendów. Powierzchnia API: `ggml.h` (operacje), `ggml-backend.h` (urządzenia, typy buforów, scheduler), `ggml-alloc.h`, `ggml-opt.h` (optymalizator), `gguf.h`. Kto osadza: **whisper.cpp** (54 489 gwiazdek, v1.9.5 z 2026-10-06), **stable-diffusion.cpp** (7 731 gwiazdek; dyfuzja: SD, Flux, Wan, Qwen Image…), bark.cpp (869 gwiazdek, uśpiony od 2024-11-16), a pośrednio llamafile, KoboldCpp, ik_llama.cpp.

**Kiedy ggml, a kiedy libllama:** ggml dla modeli nie-LLM (dyfuzja, mowa, embeddingi) i eksperymentów z treningiem; libllama dla dekoderów, bo KV cache, próbkowanie i tokenizery **nie są w ggml**.

**whisper.cpp** (MIT, 2022-09-25, ok. 5 588 commitów; najwięcej: ggerganov 1 444): rozpoznawanie mowy w ggml z CUDA, Metal, Core ML, Vulkan, HIP, OpenVINO, Ascend, Moore Threads, VAD, strumieniowaniem i wiązaniami (Rust, JS, Go, Java, Ruby, Swift, .NET, Python, R, Unity); modele od tiny (75 MB) do large-v3-turbo (2,9 GB) *(dane projektu)*. Dla ciebie: front-end STT dla agentów głosowych na Macach; działa jako biblioteka lub `whisper-server`.

### 11.6 llama-swap — przełącznik procesów przed serwerem

**Co to:** pojedyncza statyczna binarka w Go (`mostlygeek/llama-swap`, MIT, **6 015 gwiazdek**, założone 2024-10-04, wydania numerowane liczbami: **v265 z 2026-10-14**), będąca **odwrotnym proxy i menedżerem procesów**: wystawia jeden punkt końcowy zgodny z OpenAI/Anthropic i według pola `model` każdego żądania uruchamia lub zatrzymuje właściwy serwer (llama-server, vLLM, cokolwiek z HTTP). Nie dotyka tensorów.

**Jak działa** (`internal/router/design.md`):
- Konfiguracja YAML: każdy model ma `cmd` (musi zawierać `${PORT}`, przydzielany od `startPort`, domyślnie 5800), opcjonalnie `cmdStop`, `proxy`, `env`, `ttl` (sekundy *bezczynności*; 0 wyłącza), `unloadTimeout`, `checkEndpoint` (domyślnie `/health`, odpytywany do HTTP 200; serwer może zwracać JSON z `progress` 0–1, co resetuje `healthCheckTimeout`), `aliases`, `filters` (`stripParams`, `setParams`), `concurrencyLimit`.
- Trzy wymienne części: `baseRouter` (cykl życia procesów), `Scheduler` (obecnie **FIFO**, czysty automat stanów w **jednej goroutine**), `Swapper` (decyduje, *co wywłaszczyć*: `groupSwapper` statyczny lub `matrixSwapper` kosztowy). Stany procesu: stopped → starting → ready → stopping. Żądania przychodzące w trakcie zamiany **czekają w kolejce, aż wybrany model będzie gotowy**; po przekroczeniu limitów dostajesz HTTP 429.
- **Grupy:** flagi `swap` (członkowie wzajemnie się wykluczają), `exclusive` (załadowanie członka wyładowuje wszystko spoza grupy), `persistent` (nie można wywłaszczyć).
- **Macierz:** DSL z `&`, `|`, nawiasami, np. `"(g | q) & v"` ⇒ dozwolone zbiory `[gemma, voxtral]`, `[qwen, voxtral]`; `evict_costs` to kary za ponowne załadowanie; solver sumuje koszty wywłaszczenia modeli spoza każdego zbioru i wybiera najtańszy. Wskazówka z dokumentacji: grupy, gdy „te działają razem, tamte się wymieniają"; macierz, gdy „70B potrzebuje wszystkich GPU samo, albo kilka małych mieści się razem, albo średni LLM plus TTS".
- Dodatki: UI z playgroundem i logami na żywo, metryki Prometheus, MCP endpoint, peers, `cmd/kubeswap`, `cmd/wol-proxy`.

**Porównanie z wbudowanym routerem llama.cpp (§6.5):**

| | router llama-server | llama-swap |
|---|---|---|
| Co uruchamia | tylko `llama-server` | dowolny serwer HTTP (vLLM, ComfyUI, audio) |
| Wywłaszczanie | LRU wśród bezczynnych, `--models-max` (domyślnie 4) | grupy (`swap/exclusive/persistent`) lub macierz kosztów |
| Przypięcie do GPU | notatki nie opisują takiego mechanizmu *(niezweryfikowane)* | przez `env` na model, np. `HIP_VISIBLE_DEVICES` w `cmd` |
| Obserwowalność | `/metrics`, `/models/sse` | UI, logi, inspektor żądań, Prometheus (też GPU) |
| Zależność | brak, wbudowany | osobna binarka, jedna osoba utrzymuje |

Słabości llama-swap: stanowy menedżer procesów to pojedynczy punkt awarii; zamiana modelu = pełne przeładowanie bez przeniesienia KV (chyba że serwer ma własny cache promptu); najczęstszy błąd konfiguracji to rozjazd portu między `cmd` a `proxy`; macierz bez potrzebnej kombinacji powoduje nieoczekiwane wywłaszczenia („przetestuj każdą żądaną kombinację").

**Kto za tym stoi.** Benson Wong (`mostlygeek`, według GitHuba Vancouver, w polu firmy „Tailscale and Elethink"), jedna osoba utrzymuje projekt (ok. 82% commitów), istnieje listing GitHub Sponsors; bez firmy i znanego finansowania. Zob. `10-PIENIADZE-I-LUDZIE.md`.

### Tabela: kiedy co

| Potrzeba | Wybór | Uwaga |
|---|---|---|
| Serwer produkcyjny na 4×R9700 | **upstream llama.cpp** (+ llama-swap) | HIP jest celem utrzymywanym w tym samym drzewie co CUDA (§9) |
| Duży MoE na CPU+jednej karcie | ik_llama.cpp | kwanty tylko dla tego forka; gfx1201 nieudokumentowany |
| Wysłać model komuś bez instalacji | llamafile | zostaje w tyle za upstreamem o tygodnie |
| Roleplay, obrazy, TTS w jednej paczce | KoboldCpp | AGPL; AMD przez Vulkan |
| Wygodne GUI do porównań backendów | textgen | silnik w procesie potomnym |
| STT/dyfuzja/własny model na ggml | whisper.cpp / stable-diffusion.cpp / ggml | brak KV/tokenizera w ggml |
| Wiele modeli i GPU za jednym adresem | llama-swap albo router llama-server | zob. tabela wyżej |

---

## 12. Kto za tym stoi (llama.cpp)

ggml.ai założył w 2023 Georgi Gerganov; pre-seed dali Nat Friedman i Daniel Gross (`ggml.ai`). **2026-02-20** Hugging Face ogłosił, że ggml i llama.cpp do niego dołączają (wpis „GGML and llama.cpp join Hugging Face": autorzy Georgi Gerganov, Xuan-Son Nguyen, Aleksander Grygier, Lysandre, Victor Mustar, Julien Chaumond). Według wpisu zespół „nadal poświęca 100% czasu" na utrzymanie, ma „pełną autonomię" techniczną, a projekt ma pozostać „w 100% open source i prowadzony przez społeczność" *(dane firmy)*; strona ggml.ai mówi wprost, że firma została przejęta przez Hugging Face w 2026. **Warunków transakcji nie znalazłem** — traktuj jako nieujawnione. Siedmiu z dwunastu największych kontrybutorów deklaruje HF jako pracodawcę (profile GitHub, informacje samodeklarowane); inni pracują dla firm sprzętowych (np. Jeff Bolz, NVIDIA, Vulkan). Zarządzanie to „BDFL plus CODEOWNERS" (opiekunowie per obszar: CUDA, Vulkan, Metal, server itd.), bez fundacji; ok. 17% commitów to sam Gerganov, więc zespół jest szerszy niż w latach 2023–25, ale projekt nadal kręci się wokół kilkunastu osób. Powstaje warstwa konsumencka: `llama.app` oraz aplikacje `Llama-macOS` i `Llama-Windows` (organizacja ggml-org) — czy będą monetyzowane, nie ustaliłem. Polityka dotycząca AI w `AGENTS.md`: kod wygenerowany przez AI tylko wtedy, gdy człowiek go w pełni rozumie; opisy PR-ów i wiadomości commitów pisane przez AI oraz zautomatyzowane PR-y są zakazane. Pełne omówienie: `10-PIENIADZE-I-LUDZIE.md`.

---

## 13. Pułapki

1. **`-c` jest dzielone przez `-np`**, jeśli cache nie jest ujednolicony (`--kv-unified`) — §4.4.
2. **SWA i modele rekurencyjne nie „zapominają"** pozycji; trafienia w cache promptu zależą od checkpointów, które kosztują RAM — §6.3.
3. **Wbudowane `--tools`, MCP i `--agent` to nieuwierzytelnione wykonywanie kodu**, jeśli port jest osiągalny — nie wystawiaj ich — §6.7.
4. **`-ngl auto` / `--fit` potrafi zmienić rozmiar kontekstu**; w produkcji przypnij `-c` jawnie. `--fit` w ogóle nie działa z podziałem tensorowym.
5. **Cel HIP musi być dokładnie twoim `gfx`** (`-DGPU_TARGETS=gfx1201`), inaczej jądra się nie uruchomią lub spadną na ścieżkę zapasową — §9.
6. **`--models-max` w routerze domyślnie 4** — na 4×32 GB to zapewne więcej, niż chcesz trzymać jednocześnie.
7. **`-sm tensor` jest eksperymentalny** i dla AMD „bez gwarancji"; wymaga flash-attn i f16 KV — §8.
8. **Próg offloadu 32** (`GGML_OP_OFFLOAD_MIN_BATCH`): przy częściowo odciążonych modelach prefill zależy od `-ub`, dekodowanie nie — §2.6.
9. **API `llama.h` często się łamie**, a wersje to numery buildów; przypinaj tag `bNNNNN`, bo upstream wydaje po kilka buildów dziennie, a open issues + PR-y to 2 565.
10. **Kwanty i pliki nie są przenośne w obie strony** między mainline a ik_llama.cpp (formaty IQ_K/KT tylko w forku).
11. **Przesunięcie kontekstu** po cichu gubi początek rozmowy — §6.4.
12. **Opóźnienie opakowań:** llamafile jest tygodnie za upstreamem, Ollama przypina konkretny build (b11669 wobec b11741) — nowa architektura może tam jeszcze nie działać, mimo że w upstreamie jest.
13. **Cache promptu w RAM-ie ma domyślnie 8 GiB** — przy kilku modelach w trybie routera pamiętaj, że każdy potomny proces ma własny.

---

## 14. Co z tego dla konfiguracji referencyjnej

**Stos referencyjny:** llama.cpp (HIP, gfx1201) za llama-swap, 4×32 GB, MoE 284B w IQ3_XXS.

1. **Przypinaj i buduj pod konkretny cel.** `-DGGML_HIP=ON -DGPU_TARGETS=gfx1201`; trzymaj w repozytorium wyjście `llama-bench` w JSONL, by wykrywać regresje między tagami `bNNNNN`.
2. **Tryb podziału wybieraj do obciążenia — i mierz.** `layer` dla wielu równoległych agentów i długich promptów (na rigu referencyjnym: 4 sloty × 131 tys., najszybszy prefill ~960 tok/s, ale ~23,5 tok/s generowania). `-sm tensor -fa on -ctk f16 -ctv f16` jest oficjalnie eksperymentalny i dla AMD „bez gwarancji” (§8), a mimo to na referencyjnym rigu 4× R9700 z DeepSeek-V4-Flash **zadziałał i dał mierzalny zysk**: bez draftu 25,2 → 29,1 tok/s, z draftem DSpark 37,9 → 46,2 tok/s, produkcyjnie ~49–50 tok/s dla jednego agenta *(moje pomiary, szczegóły i warunki w [`../przyspieszanie-generowania/README.md`](../przyspieszanie-generowania/README.md))*. Cena: prefill ~700 zamiast ~960 tok/s i 2 sloty × 98 304 zamiast 4 × 131 072. Wnioski ogólne: tryb tensorowy próbuj z własnym pomiarem na swoim modelu (nie wszystkie architektury go wspierają — lista w `docs/multi-gpu.md`), pamiętaj, że jakości po przejściu na tryb tensorowy nie zmierzyłem, i ustawiaj `-c` ręcznie (`--fit` nie działa). RCCL (`-DGGML_HIP_RCCL=ON`) jest domyślnie wyłączony — nie testowałem go.
3. **Cache promptu dla pętli agentów:** trzymaj `--cache-ram` dużo (domyślnie 8 GiB), `--cache-idle-slots` włączone, `--ctx-checkpoints` ≥ 16 dla modeli SWA/hybrydowych; kieruj sesje stałym `id_slot` albo polegaj na wyborze slotu po LCP. Decyzję unified/per-slot podejmij wg tego, czy długości kontekstów są bardzo nierówne (`--kv-unified`).
4. **Ustrukturyzowane wyjście:** używaj gramatyk leniwych / `response_format` z JSON-schema przez serwer; przy dużych schematach rozważ build z LLGuidance.
5. **Dekodowanie spekulacyjne:** warianty n-gramowe (`--spec-type`) nic nie kosztują (brak modelu draftu) i dobrze działają przy kodzie i powtarzaniu wywołań narzędzi; EAGLE-3/MTP/DFlash tylko jeśli istnieje pasujący draft GGUF dla danego modelu.
6. **MoE na mieszanym sprzęcie (np. Mac):** `-ot` z regexem trzyma ekspertów w RAM-ie; nowy `llama_moe_cache` buforuje gorących ekspertów na GPU.
7. **Router llama-server czy llama-swap?** Wbudowany router (`--models-dir --models-max`, LRU) wystarcza przy jednej grupie GPU. Zostań przy llama-swap, gdy potrzebujesz **przypięcia modeli do konkretnych GPU** (`HIP_VISIBLE_DEVICES` w `cmd`/`env`), grup/macierzy, nie-llamowych upstreamów, metryk. Naturalny wybór na sprzęcie referencyjnym: wpis „70B gęsty na wszystkich czterech" (`HIP_VISIBLE_DEVICES=0,1,2,3`, `-sm layer`), obok dwóch modeli 30B MoE na parach kart i stale działający model embeddingów/rerankera na osobnym kawałku; koszty wywłaszczenia ≈ czasy ładowania z dysku. Wspólne `--parallel`, `--cache-ram`, `--ctx-checkpoints` wstaw makrami do `cmd` każdego modelu; `filters.setParams` wymusza ustawienia próbników dla frameworków wysyłających złe domyślne.
8. **Narzędzia agentowe:** przeczytaj `server-tools.cpp` i `--tools-runtime docker:` jako wzorzec izolowanego wykonywania narzędzi, ale nie wystawiaj.
9. **Endpointy Anthropic i Responses** pozwalają podpiąć lokalny model pod narzędzia napisane dla tych API bez proxy tłumaczącego.
10. **Na Macu:** Metal to pełnoprawny backend (~33 tys. linii), a aplikacja `Llama-macOS` (4 MB, `brew install --cask llama-app`, serwer na `localhost:9931/v1`) to najprostsza ścieżka *(dane projektu)*; MLX opisuje rozdział 07.
11. **Czego nie wiem:** wyników wydajności na gfx1201 (nic nie mierzyłem), liczby przebiegów schedulera, polityki priorytetów w ciągłym batchowaniu, celu backendu `ggml-et`, ani tego, czy `--tools`/MCP są wystarczająco stabilne do produkcji. Do porównania z innymi silnikami: `09-POROWNANIE-I-WYBOR.md`; serwery datacenter (vLLM, SGLang) w `06-SILNIKI-SERWEROWE-VLLM-SGLANG.md`; opakowania w `05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md`; kwanty w `03-KWANTYZACJA-I-FORMATY.md`; ludzie i pieniądze w `10-PIENIADZE-I-LUDZIE.md`.
