> **Przekład** dokumentu [`docs/speculative.md`](https://github.com/ggml-org/llama.cpp/blob/0ce8cd11416c8840498e6701bcbe39ad4b858c2b/docs/speculative.md) z repozytorium [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)
> (commit `0ce8cd1`, 19 października 2026), licencja MIT, © 2023–2026 The ggml authors — pełna treść licencji na końcu pliku.
> Przekładu dokonał lokalnie **DeepSeek-V4-Flash-0731** (ten sam model, który przyspieszam w tym katalogu), sekcja po sekcji.
> **To surowy wynik modelu, jeszcze niezweryfikowany.** Źródłem prawdy jest oryginał.

# Speculative Decoding

llama.cpp obsługuje speculative decoding, technikę, która może znacząco przyspieszyć generowanie tokenów poprzez przewidywanie wielu tokenów z wyprzedzeniem względem głównego modelu.

[Speculative decoding](https://en.wikipedia.org/wiki/Transformer_(deep_learning)#Speculative_decoding) wykorzystuje fakt, że obliczenie n tokenów w partii (jak w przetwarzaniu promptu) jest bardziej wydajne niż obliczanie n tokenów sekwencyjnie (jak w generowaniu odpowiedzi). Poprzez szybkie generowanie tokenów draftu, a następnie weryfikowanie ich za pomocą modelu docelowego w jednej partii, podejście to może osiągnąć znaczące przyspieszenie, gdy przewidywania draftu są często poprawne.

## Implementacje

Aplikacja `llama-server` obsługuje kilka implementacji speculative decoding. Implementację z modelem draftu można łączyć z implementacją bez modelu draftu.

### Model draftu (`draft`)

Znacznie mniejszy model (zwany _modelem draftu_) generuje wersje robocze tokenów.
Model draftu jest najczęściej stosowanym podejściem w speculative decoding.

### EAGLE-3 (`draft-eagle3`)

EAGLE-3 używa małego modelu draftu, który odczytuje ukryte stany modelu docelowego, aby przewidywać kolejne tokeny, dzięki czemu osiąga wyższy współczynnik akceptacji niż samodzielny model draftu o tej samej wielkości. Draft to jednowarstwowy transformer wytrenowany dla konkretnego modelu docelowego; współdzieli tokenizer modelu docelowego i opcjonalnie używa zredukowanego słownika draftu z własnym `lm_head`, który jest mapowany z powrotem za pomocą tabeli `d2t`.

Skonwertuj punkt kontrolny EAGLE-3 za pomocą `--target-model-dir`, aby odziedziczył tokenizer modelu docelowego oraz indeksy warstw do odczytu. Obsługiwane są zarówno formaty punktów kontrolnych SpecForge `LlamaForCausalLMEagle3`, jak i vLLM/AngelSlim `Eagle3LlamaForCausalLM` (na przykład [`AngelSlim/Qwen3-4B_eagle3`](https://huggingface.co/AngelSlim/Qwen3-4B_eagle3) dla `Qwen/Qwen3-4B`):

```bash
python convert_hf_to_gguf.py AngelSlim/Qwen3-4B_eagle3 \
    --target-model-dir Qwen/Qwen3-4B --outtype bf16 --outfile Qwen3-4B-eagle3.gguf

llama-server -m Qwen3-4B.gguf -md Qwen3-4B-eagle3.gguf --spec-type draft-eagle3
```

Obsługiwane modele draftu EAGLE-3 obejmują:

- [yuhuili/EAGLE3-LLaMA3.1-Instruct-8B](https://huggingface.co/yuhuili/EAGLE3-LLaMA3.1-Instruct-8B)
- [yuhuili/EAGLE3-LLaMA3.3-Instruct-70B](https://huggingface.co/yuhuili/EAGLE3-LLaMA3.3-Instruct-70B)
- [RedHatAI/gemma-4-31B-it-speculator.eagle3](https://huggingface.co/RedHatAI/gemma-4-31B-it-speculator.eagle3)
- [RedHatAI/gemma-4-26B-A4B-it-speculator.eagle3](https://huggingface.co/RedHatAI/gemma-4-26B-A4B-it-speculator.eagle3)
- [Tengyunw/qwen3_8b_eagle3](https://huggingface.co/Tengyunw/qwen3_8b_eagle3)
- [Tengyunw/qwen3_30b_moe_eagle3](https://huggingface.co/Tengyunw/qwen3_30b_moe_eagle3)
- [AngelSlim/Qwen3-1.7B_eagle3](https://huggingface.co/AngelSlim/Qwen3-1.7B_eagle3)
- [AngelSlim/Qwen3-4B_eagle3](https://huggingface.co/AngelSlim/Qwen3-4B_eagle3)
- [AngelSlim/Qwen3-8B_eagle3](https://huggingface.co/AngelSlim/Qwen3-8B_eagle3)
- [AngelSlim/Qwen3-14B_eagle3](https://huggingface.co/AngelSlim/Qwen3-14B_eagle3)
- [AngelSlim/Qwen3-32B_eagle3](https://huggingface.co/AngelSlim/Qwen3-32B_eagle3)
- [AngelSlim/Qwen3-a3B_eagle3](https://huggingface.co/AngelSlim/Qwen3-a3B_eagle3)
- [RedHatAI/gpt-oss-20b-speculator.eagle3](https://huggingface.co/RedHatAI/gpt-oss-20b-speculator.eagle3)
- [lmsys/EAGLE3-gpt-oss-120b-bf16](https://huggingface.co/lmsys/EAGLE3-gpt-oss-120b-bf16)
- [nvidia/gpt-oss-120b-Eagle3-long-context](https://huggingface.co/nvidia/gpt-oss-120b-Eagle3-long-context)

Pełną i aktualną listę obsługiwanych modeli znajdziesz w #18039.
### DFlash (`draft-dflash`)

DFlash generuje cały blok tokenów draftu w jednym przejściu w przód (dyfuzja blokowa) i
wstrzykuje ukryte stany modelu docelowego do uwagi modelu draftu, zamiast generować token po
tokenie. Dzięki temu model draftu pozostaje mały, a samo generowanie draftu jest przyjazne dla GPU.
W przeciwieństwie do EAGLE-3 (jednowarstwowy autoregresyjny draft), draft DFlash wykorzystuje
kilka warstw transformera, ale emituje cały blok w jednym kroku draftu.

Draft to mały model dyfuzji blokowej wytrenowany dla konkretnego modelu docelowego (na przykład
`z-lab/Qwen3-4B-DFlash` dla `Qwen/Qwen3-4B`). Konwertuj go za pomocą `--target-model-dir`, aby
odziedziczył tokenizer i embeddingi tokenów modelu docelowego:

```bash
python convert_hf_to_gguf.py z-lab/Qwen3-4B-DFlash \
    --target-model-dir Qwen/Qwen3-4B --outtype bf16 --outfile Qwen3-4B-DFlash.gguf

llama-server -m Qwen3-4B.gguf -md Qwen3-4B-DFlash.gguf \
    --spec-type draft-dflash --spec-draft-n-max 15 -fa on --jinja
```

`--spec-draft-n-max` jest ograniczany do wytrenowanego rozmiaru bloku modelu draftu.

Zobacz:

- #22105

### DSpark (`draft-dspark`)

DSpark rozszerza DFlash o semi-autoregresyjną _głowę Markowa_: draft nadal emituje cały blok
w jednym przejściu w przód, ale logity każdej pozycji w bloku są modyfikowane przez człon
niskiego rzędu zależny od poprzedniego tokena, połączony w grafie w obrębie bloku. Pozwala to
utrzymać generowanie draftu na poziomie jednego dekodowania na blok, jednocześnie odzyskując
część sygnału od lewej do prawej, który traci czysta dyfuzja blokowa.

Draft to mały checkpoint DeepSpec wytrenowany dla konkretnego modelu docelowego (na przykład
[`deepseek-ai/dspark_qwen3_4b_block7`](https://huggingface.co/deepseek-ai/dspark_qwen3_4b_block7)
dla `Qwen/Qwen3-4B`). Konwertuj go za pomocą `--target-model-dir`, aby odziedziczył tokenizer
i embeddingi tokenów modelu docelowego:

```bash
python convert_hf_to_gguf.py deepseek-ai/dspark_qwen3_4b_block7 \
    --target-model-dir Qwen/Qwen3-4B --outtype bf16 --outfile Qwen3-4B-DSpark.gguf

llama-server -m Qwen3-4B.gguf -md Qwen3-4B-DSpark.gguf \
    --spec-type draft-dspark --spec-draft-n-max 7 -fa on --jinja
```

`--spec-draft-n-max` jest ograniczany do wytrenowanego rozmiaru bloku modelu draftu.

`--spec-draft-conf-min P` obcina każdy wygenerowany blok draftu na pierwszej pozycji, której
przewidywany współczynnik akceptacji (z głowy pewności draftu, jeśli istnieje) spada poniżej
`P` (domyślnie 0 = wyłączone).

Obecnie obsługiwane są tylko drafty z rdzeniem Qwen3; wsparcie dla innych rdzeni
(np. Gemma4) jest planowane.

Drafty DSpark eksportowane w formacie [speculators](https://github.com/vllm-project/speculators)
(na przykład [`RedHatAI/gemma-4-31B-it-speculator.dspark`](https://huggingface.co/RedHatAI/gemma-4-31B-it-speculator.dspark))
konwertują się w ten sam sposób.

Zobacz:

- #25173

### Pamięć podręczna n-gramów (`ngram-cache`)

N-gram to sekwencja n tokenów. Implementacja pamięci podręcznej n-gramów utrzymuje statystyki
dotyczące krótkich sekwencji n-gramów. Draft jest obliczany przy użyciu prawdopodobieństw
wyprowadzonych z tych statystyk. Zewnętrzne statystyki można również wczytywać z plików w celu
zwiększenia dokładności.

Zobacz:

- #5479, #6828, #6848
### Mapa n-gramów (`ngram-simple`, `ngram-map-*`)

Implementacje te przeszukują historię tokenów w poszukiwaniu wzorców i używają pasujących sekwencji jako kandydatów na draft.
Nie wymagają dodatkowego modelu, ale opierają się na wzorcach, które już pojawiły się w wygenerowanym tekście.
Przykładem zastosowania tego podejścia może być przepisywanie kodu źródłowego przez LLM.

#### Mapa n-gramów (`ngram-simple`)

Implementacja ta szuka ostatniego n-gramu w historii, który pasuje do bieżącego n-gramu, i tworzy draft przy użyciu m tokenów następujących po dopasowanym n-gramie. Jest to najprostsze podejście self-speculative przy minimalnym narzucie.

```
llama-server [...] --spec-type ngram-simple --spec-draft-n-max 64
```

#### Mapa n-gramów — klucz (`ngram-map-k`)

Implementacja ta szuka bieżącego n-gramu o rozmiarze n (zwanego _kluczem_) w historii tokenów. Jeśli n-gram klucza jest wielokrotnie następowany przez te same m tokenów (zwane _mgramem_), tworzy draft przy użyciu tych m tokenów. Podejście to wymaga minimalnej liczby wystąpień (argument `--spec-ngram-map-k-min-hits`, domyślnie 1) przed wygenerowaniem draftów.

Liczba zaakceptowanych tokenów jest przechowywana dla każdego użytego n-gramu.

**Przykład:**
```
llama-server [...] --spec-type ngram-map-k --spec-draft-n-max 64
```

#### Mapa n-gramów — klucz-4-wartości (`ngram-map-k4v`)

Ta eksperymentalna implementacja szuka bieżącego n-gramu o rozmiarze n (zwanego _kluczem_) w historii tokenów. Dla każdego klucza śledzone są maksymalnie cztery _wartości_ (n-gramy o rozmiarze m, zwane _mgramami_). Wewnętrzna statystyka zlicza wystąpienia każdego mgramu po n-gramie klucza. Jeśli jeden mgram jest znacząco częstszy niż pozostałe, jest używany jako draft.

Liczba zaakceptowanych tokenów jest przechowywana dla każdego użytego n-gramu.

**Przykład:** Opcje serwera do użycia, gdy występuje wiele dłuższych powtórzeń.
```
llama-server [...] --spec-type ngram-map-k4v --spec-ngram-map-k4v-size-n 8 --spec-ngram-map-k4v-size-m 8 --spec-ngram-map-k4v-min-hits 2 --spec-draft-n-max 64
```

### n-gram Mod (`ngram-mod`)

Dodaje podstawowy hasher ngramów dla speculative decoding:

- Dla każdego ngramu obliczany jest hash przy użyciu LCG
- Dla każdego obliczonego hasha przechowywany jest następny token
- Podczas spekulacji iteracyjnie obliczany jest kroczący hash ostatnich n tokenów, a następny token jest wybierany z magazynu

Niektóre cechy:

- Lekki (~16 MB)
- Stała pamięć i złożoność
- Może generować zmienne długości draftów (tzn. m nie jest stałe)

Obecnie pojedyncza pula hashów jest współdzielona między wszystkimi slotami serwera, więc różne żądania mogą korzystać z siebie nawzajem.

**Przykładowe użycie:**

```
# uwagi:
# - małe `n` nie są zalecane
# - modele MoE wymagają długich draftów
# - modele gęste: można zmniejszyć `--spec-ngram-mod-n-min` i `--spec-ngram-mod-n-max`

llama-server ... --spec-type ngram-mod --spec-ngram-mod-n-match 24 --spec-ngram-mod-n-min 48 --spec-ngram-mod-n-max 64
```

Zastosowania:

- Iterowanie po bloku tekstu/kodu (np. w llama.vim)
- Modele rozumowania (gdy muszą powtórzyć swoje rozumowanie w końcowej odpowiedzi)
- Streszczenia

Przykładowe wideo:

- Zobacz #19164
### Różnice między ngram-simple, ngram-map i ngram-mod

- ngram-simple wyszukuje poprzedni pasujący n-gram i wstawia następujący po nim m-gram.
- ngram-map-k wyszukuje poprzedni pasujący n-gram i wstawia następujący po nim m-gram, ale używa wewnętrznej mapy haszującej n-gramów w bieżącym oknie kontekstu.
- ngram-mod używa puli haszującej współdzielonej między wszystkimi slotami serwera. Pula haszująca to mapa od hasza n-gramu do następnego tokenu (nie następnego m-gramu, jak w ngram-map).

## Opcje linii poleceń

Jeśli model draftu jest połączony z dekodowaniem bez draftu, dekodowanie bez draftu ma wyższy priorytet.

### Próbkowanie backendowe

Użyj `--backend-sampling`, aby uruchomić obsługiwane samplery modelu docelowego na backendzie modelu. Próbkowanie modelu draftu domyślnie używa backendu i może być kontrolowane przez `--spec-draft-backend-sampling` oraz `--no-spec-draft-backend-sampling`.

Nieobsługiwane samplery i układy urządzeń przechodzą na próbkowanie CPU. Tryb podziału tensorów nie obsługuje próbkowania backendowego. Stałe ziarno (seed) daje powtarzalne losowania, ale stochastyczne próbkowanie CPU i backendu może nadal wybierać różne tokeny, ponieważ operacje zmiennoprzecinkowe mogą się różnić między implementacjami i urządzeniami. Użyj próbkowania zachłannego (greedy), gdy wymagane jest dokładne dopasowanie wyników.

### Akceptacja syntetyczna

`llama-server` i `llama-cli` mogą zastąpić normalną weryfikację spekulatywną syntetycznymi decyzjami do celów benchmarkowych. Wygenerowane dane wyjściowe nie są prawidłowym wynikiem modelu, ponieważ zaakceptowane tokeny draftu nie muszą odpowiadać modelowi docelowemu.

Użyj dokładnie jednej z tych opcji:

- `--spec-synth-rates P0,P1,...` ustawia bezwarunkowe prawdopodobieństwa akceptacji dla poszczególnych pozycji. Wpis `i` to prawdopodobieństwo, że pierwsze `i+1` tokenów draftu zostanie zaakceptowanych. Liczba wpisów musi odpowiadać efektywnej maksymalnej długości draftu. Wartości muszą być skończone, w zakresie `[0, 1]` i monotonicznie niemalejące.
- `--spec-synth-len L` ustawia docelową średnią długość akceptacji, włączając token docelowy. Dla `K` maksymalnych tokenów draftu, `L` musi być w zakresie `[1, K+1]`. Serwer znajduje stałe prawdopodobieństwo warunkowe `p` takie, że `p + p^2 + ... + p^K = L - 1`, a następnie używa bezwarunkowych współczynników `[p, p^2, ..., p^K]`.

### Ogólne parametry dekodowania spekulatywnego

```
--spec-type [none|draft-simple|draft-eagle3|draft-dflash|draft-dspark|draft-mtp|ngram-cache|ngram-simple|ngram-map-k|ngram-map-k4v|ngram-mod]
                                        comma-separated list of types of speculative decoding to use
                                        (default: none)
                                        (env: LLAMA_ARG_SPEC_TYPE)
--spec-default                          use default speculative decoding config
                                        (enables ngram-mod)
```

### Parametry modelu draftu

```
--spec-draft-model, -md, --model-draft  FNAME
                                        draft model for speculative decoding (default: unused)
                                        (env: LLAMA_ARG_SPEC_DRAFT_MODEL)
--spec-draft-hf, -hfd, -hfrd, --hf-repo-draft  <user>/<model>[:quant]
                                        HuggingFace repository for the draft model
                                        (env: LLAMA_ARG_SPEC_DRAFT_HF_REPO)
--spec-draft-n-max                      N
                                        number of tokens to draft for speculative decoding (default: 3)
                                        (env: LLAMA_ARG_SPEC_DRAFT_N_MAX)
--spec-draft-n-min                      N
                                        minimum number of draft tokens to use for speculative decoding (default: 0)
                                        (env: LLAMA_ARG_SPEC_DRAFT_N_MIN)
--spec-draft-n-ubatch                   N
                                        physical maximum batch size of the draft context, use a smaller value to spare VRAM (default: 0 - same as --n-ubatch)
                                        (env: LLAMA_ARG_SPEC_DRAFT_N_UBATCH)
--spec-draft-p-split, --draft-p-split   P
                                        speculative decoding split probability (default: 0.10)
                                        (env: LLAMA_ARG_SPEC_DRAFT_P_SPLIT)
--spec-draft-p-min, --draft-p-min       P
                                        minimum speculative decoding probability (greedy) (default: 0.00)
                                        (env: LLAMA_ARG_SPEC_DRAFT_P_MIN)
--spec-draft-ngl, -ngld, --gpu-layers-draft, --n-gpu-layers-draft  N
                                        max. number of draft model layers to store in VRAM, either an exact number, 'auto', or 'all' (default: auto)
                                        (env: LLAMA_ARG_N_GPU_LAYERS_DRAFT)
--spec-draft-device, -devd, --device-draft  <dev1,dev2,..>
                                        comma-separated list of devices to use for offloading the draft model
                                        (use --list-devices to see available devices)
```
### Parametry planowania CPU modelu draftu

```
--spec-draft-threads, -td, --threads-draft  N
                                        liczba wątków CPU używanych podczas generacji
--spec-draft-threads-batch, -tbd, --threads-batch-draft  N
                                        liczba wątków używanych podczas przetwarzania wsadowego i promptu (domyślnie: taka sama jak --threads-draft)
--spec-draft-cpu-mask, -Cd, --cpu-mask-draft  M
                                        Maska powinowactwa CPU modelu draftu. Uzupełnia cpu-range-draft
--spec-draft-cpu-range, -Crd, --cpu-range-draft  lo-hi
                                        Zakresy CPU dla powinowactwa. Uzupełnia --cpu-mask-draft
--spec-draft-cpu-strict, --cpu-strict-draft  <0|1>
                                        Użyj ścisłego rozmieszczenia CPU dla modelu draftu (domyślnie: taka sama jak --cpu-strict)
--spec-draft-prio, --prio-draft  N
                                        ustaw priorytet procesu/wątku draftu : 0-normalny, 1-średni, 2-wysoki, 3-czasu rzeczywistego
--spec-draft-poll, --poll-draft  <0|1>
                                        Użyj pollingu, aby czekać na pracę modelu draftu (domyślnie: taka sama jak --poll)
--spec-draft-cpu-mask-batch, -Cbd, --cpu-mask-batch-draft  M
                                        Maska powinowactwa CPU modelu draftu dla wsadu. Uzupełnia cpu-range-batch-draft
--spec-draft-cpu-range-batch, -Crbd, --cpu-range-batch-draft  lo-hi
                                        Zakresy CPU dla powinowactwa dla wsadu. Uzupełnia --cpu-mask-batch-draft
--spec-draft-cpu-strict-batch, --cpu-strict-batch-draft  <0|1>
                                        Użyj ścisłego rozmieszczenia CPU dla wsadu modelu draftu (domyślnie: --cpu-strict-draft)
--spec-draft-prio-batch, --prio-batch-draft  N
                                        ustaw priorytet procesu/wątku draftu dla wsadu : 0-normalny, 1-średni, 2-wysoki, 3-czasu rzeczywistego
--spec-draft-poll-batch, --poll-batch-draft  <0|1>
                                        Użyj pollingu, aby czekać na pracę modelu draftu dla wsadu (domyślnie: --poll-draft)
```

### Parametry nadpisywania pamięci podręcznej KV i tensorów modelu draftu

```
--spec-draft-type-k, -ctkd, --cache-type-k-draft  TYPE
                                        Typ danych pamięci podręcznej KV dla K w modelu draftu
                                        dozwolone wartości: f32, f16, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1
                                        (env: LLAMA_ARG_SPEC_DRAFT_CACHE_TYPE_K)
--spec-draft-type-v, -ctvd, --cache-type-v-draft  TYPE
                                        Typ danych pamięci podręcznej KV dla V w modelu draftu
                                        dozwolone wartości: f32, f16, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1
                                        (env: LLAMA_ARG_SPEC_DRAFT_CACHE_TYPE_V)
--spec-draft-override-tensor, -otd, --override-tensor-draft  <wzorzec nazwy tensora>=<typ bufora>,...
                                        nadpisz typ bufora tensora dla modelu draftu
--spec-draft-cpu-moe, -cmoed, --cpu-moe-draft
                                        przechowuj wszystkie wagi Mixture of Experts (MoE) w CPU dla modelu draftu
                                        (env: LLAMA_ARG_SPEC_DRAFT_CPU_MOE)
--spec-draft-n-cpu-moe, --spec-draft-ncmoe, -ncmoed, --n-cpu-moe-draft  N
                                        przechowuj wagi MoE pierwszych N warstw w CPU dla modelu draftu
                                        (env: LLAMA_ARG_SPEC_DRAFT_N_CPU_MOE)
```
### Parametry modyfikacji n-gram

```
--spec-ngram-mod-n-match                N
                                        długość wyszukiwania ngram-mod (domyślnie: 24)
--spec-ngram-mod-n-min                  N
                                        minimalna liczba tokenów ngram do użycia w speculative decoding opartym na n-gramach (domyślnie: 48)
--spec-ngram-mod-n-max                  N
                                        maksymalna liczba tokenów ngram do użycia w speculative decoding opartym na n-gramach (domyślnie: 64)
```

### Proste parametry n-gram

```
--spec-ngram-simple-size-n              N
                                        rozmiar n-gramu N dla prostego speculative decoding opartego na n-gramach, długość wyszukiwanego n-gramu (domyślnie: 12)
--spec-ngram-simple-size-m              N
                                        rozmiar n-gramu M dla prostego speculative decoding opartego na n-gramach, długość draftu m-gram (domyślnie: 48)
--spec-ngram-simple-min-hits            N
                                        minimalna liczba trafień dla prostego speculative decoding opartego na n-gramach (domyślnie: 1)
```

### Parametry klucza mapy n-gram

```
--spec-ngram-map-k-size-n               N
                                        rozmiar n-gramu N dla speculative decoding opartego na n-gramach z mapą kluczy, długość wyszukiwanego n-gramu (domyślnie: 12)
--spec-ngram-map-k-size-m               N
                                        rozmiar n-gramu M dla speculative decoding opartego na n-gramach z mapą kluczy, długość draftu m-gram (domyślnie: 48)
--spec-ngram-map-k-min-hits             N
                                        minimalna liczba trafień dla speculative decoding opartego na n-gramach z mapą kluczy (domyślnie: 1)
```

### Parametry klucza mapy n-gram z 4 wartościami

```
--spec-ngram-map-k4v-size-n             N
                                        rozmiar n-gramu N dla speculative decoding opartego na n-gramach z mapą kluczy i 4 wartościami, długość wyszukiwanego n-gramu (domyślnie: 12)
--spec-ngram-map-k4v-size-m             N
                                        rozmiar n-gramu M dla speculative decoding opartego na n-gramach z mapą kluczy i 4 wartościami, długość draftu m-gram (domyślnie: 48)
--spec-ngram-map-k4v-min-hits           N
                                        minimalna liczba trafień dla speculative decoding opartego na n-gramach z mapą kluczy i 4 wartościami (domyślnie: 1)
```

### `--spec-type TYPE`

Określa rozdzielaną przecinkami listę typów speculative decoding do użycia.

| Typ | Opis |
|------|-------------|
| `none` | Brak speculative decoding (domyślnie) |
| `draft-simple` | Użycie prostego modelu draftu do spekulacji |
| `draft-eagle3` | Użycie modelu draftu EAGLE-3, który odczytuje ukryte stany modelu docelowego |
| `draft-dflash` | Użycie modelu draftu DFlash z dyfuzją blokową, emitującego blok na krok |
| `draft-dspark` | Użycie modelu draftu DSpark (rdzeń DFlash + półautoregresyjna głowica Markowa) |
| `draft-mtp` | Użycie głowic Multi Token Prediction (MTP) z głównego modelu |
| `ngram-cache` | Użycie wyszukiwania w pamięci podręcznej n-gramów |
| `ngram-simple` | Użycie prostego dopasowywania wzorców n-gram |
| `ngram-map-k` | Użycie dopasowywania wzorców n-gram z kluczami n-gram |
| `ngram-map-k4v` | Użycie dopasowywania wzorców n-gram z kluczami n-gram i do czterech wartości m-gram (eksperymentalne) |
| `ngram-mod` | Użycie podstawowego hashera n-gram do speculative decoding ze wspólną pulą |

**Przykład:** Instancja serwera używana do refaktoryzacji kodu źródłowego.
```bash
./llama-server [...] --spec-type ngram-simple
```

**Przykład:** Wiele implementacji spekulacyjnych.
```bash
./llama-server [...] --spec-type ngram-mod,ngram-map-k4v
```
### `--spec-ngram-*-size-n N`

Ustawia rozmiar N n-gramu wyszukiwania dla speculative decoding opartego na mapie n-gramów.
Rozmiar n-gramu N określa, ile tokenów pod rząd należy sprawdzić wstecz podczas wyszukiwania pasujących wzorców.

Każda implementacja n-gramu ma swój własny parametr:

- `--spec-ngram-simple-size-n` dla `ngram-simple`
- `--spec-ngram-map-k-size-n` dla `ngram-map-k`
- `--spec-ngram-map-k4v-size-n` dla `ngram-map-k4v`
- `--spec-ngram-mod-n-match` dla `ngram-mod`

### `--spec-ngram-*-size-m M`

Ustawia rozmiar M m-gramu draftu dla speculative decoding opartego na mapie n-gramów.
Rozmiar m-gramu określa, ile tokenów draftu ma zostać wygenerowanych po znalezieniu dopasowania.
Większe wartości mogą zapewnić większe przyspieszenie, ale mogą obniżyć współczynnik akceptacji.

Każda implementacja n-gramu ma swój własny parametr:

- `--spec-ngram-simple-size-m` dla `ngram-simple`
- `--spec-ngram-map-k-size-m` dla `ngram-map-k`
- `--spec-ngram-map-k4v-size-m` dla `ngram-map-k4v`

### `--spec-ngram-*-min-hits H`

Ta opcja określa, jak często klucz musi pojawić się w historii tokenów, aby został użyty jako draft (domyślnie 1).

Każda implementacja n-gramu ma swój własny parametr:

- `--spec-ngram-simple-min-hits` dla `ngram-simple`
- `--spec-ngram-map-k-min-hits` dla `ngram-map-k`
- `--spec-ngram-map-k4v-min-hits` dla `ngram-map-k4v`

## Statystyki
Każda implementacja speculative decoding wypisuje statystyki.

```
draft acceptance rate = 0.57576 (  171 accepted /   297 generated)
statistics ngram_simple: #calls = 15, #gen drafts = 5, #acc drafts = 5, #gen tokens = 187, #acc tokens = 73
statistics draft: #calls = 10, #gen drafts = 10, #acc drafts = 10, #gen tokens = 110, #acc tokens = 98
```

```
draft acceptance rate = 0.70312 (   90 accepted /   128 generated)
statistics ngram_mod: #calls = 810, #gen drafts = 15, #acc drafts = 15, #gen tokens = 960, #acc tokens = 730, dur(b,g,a) = 0.149, 0.347, 0.005 ms
```

```
statistics ngram_map_k: #calls(b,g,a) = 6 1690 26, #gen drafts = 26, #acc drafts = 26, #gen tokens = 1248, #acc tokens = 968, dur(b,g,a) = 2.234, 1.427, 0.016 ms
```


- `#calls(b,g,a)`: liczba wywołań fazy begin (nowy prompt), generowania i akumulacji dla tej implementacji
- `#gen drafts`: liczba draftów wygenerowanych przez tę implementację
- `#acc drafts`: liczba draftów zaakceptowanych (częściowo) przez model główny
- `#gen tokens`: liczba tokenów wygenerowanych przez tę implementację (w tym tokeny odrzucone)
- `#acc tokens`: liczba tokenów zaakceptowanych przez model główny
- `dur(b,g,a)`: czasy trwania fazy begin (nowy prompt), generowania i akumulacji (przetwarzanie akceptacji).

## Benchmarking

Aby zmierzyć efekt end-to-end speculative decoding (przepustowość, opóźnienie i akceptację draftów) dla różnych promptów, zobacz klienta SPEED-Bench w [tools/server/bench/speed-bench](../tools/server/bench/speed-bench/README.md).
Działa on względem uruchomionego `llama-server` i może porównać przebieg bazowy z przebiegiem z speculative decoding.

---

## Licencja oryginału

```
MIT License

Copyright (c) 2023-2026 The ggml authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
