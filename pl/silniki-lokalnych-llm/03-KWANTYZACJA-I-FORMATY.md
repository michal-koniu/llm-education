# 03 · Kwantyzacja i formaty modeli: co właściwie jest w pliku

**Po co ten rozdział.** Model referencyjny, `DeepSeek-V4-Flash-0731-UD-IQ3_XXS`, to 284 mld parametrów w pliku o rozmiarze ok. 104 GB.
Gdyby każdy parametr zajmował 16 bitów, plik miałby ok. 568 GB. Różnica to **kwantyzacja** — i to ona decyduje o tym, czy model w ogóle
mieści się na czterech kartach po 32 GB, oraz o tym, ile bajtów karta musi przeczytać na każdy token (czyli jak szybko model mówi).
Po przeczytaniu tego rozdziału będziesz umieć: (1) policzyć ręcznie, ile bitów na wagę zajmuje dowolny typ kwantyzacji z llama.cpp, (2) wyjaśnić,
czym różni się Q4_K_M od IQ3_XXS, od MXFP4, od AWQ i od `UD-` Unsloth, (3) odczytać z nagłówka GGUF, co faktycznie jest w pliku, (4) wiedzieć,
który format ładuje który silnik i na jakim sprzęcie, (5) zaplanować pomiar jakości swojego modelu, którego — jak przyznajesz w katalogu o przyspieszaniu —
jeszcze nie zmierzyłeś.

> ⚠️ **Niczego tu nie uruchamiałem.** Rozdział powstał z lektury kodu (drzewo llama.cpp w wersji `0ce8cd1`, którą masz w produkcji; klony `vllm`, `sglang`,
> `mlx`, `mlx-lm`, `ds4`), dokumentacji projektów, prac naukowych i zgłoszeń zmian (PR) na GitHubie oraz notatek z tej ankiety. Jedyny „pomiar" własny to **odczyt nagłówka
> pliku GGUF** Unsloth (Qwen3-Coder-30B-A3B w wersji UD-IQ3_XXS) — opisany w sekcji 7. Wszystkie liczby jakości pochodzą z tabel w repozytoriach
> projektów, z podaną konfiguracją; nigdy ich nie mieszam między konfiguracjami. Polecenia oznaczone *(nie uruchamiałem)* pochodzą z dokumentacji lub kodu, nie z mojego terminala.
> Rzeczy, których nie wiem, nazywam „nie ustaliłem".

Znaczniki wiarygodności w tekście: bez znacznika = sprawdziłem w kodzie lub w pierwotnym źródle; *(dane projektu)* = twierdzenie autorów;
*(prasa)* / *(źródło zewnętrzne)* = relacja osoby trzeciej; *(moje wyliczenie)* = arytmetyka z podanych danych; *(niezweryfikowane)* = przypuszczenie.

## Spis treści

1. [Po co kwantyzować: przepustowość i pojemność](#1-po-co-kwantyzować-przepustowość-i-pojemność)
2. [Kwantyzacja blokowa od zera: 8 wag na kartce](#2-kwantyzacja-blokowa-od-zera-8-wag-na-kartce)
3. [Rodziny typów w llama.cpp, z dokładnym bpw](#3-rodziny-typów-w-llamacpp-z-dokładnym-bpw)
4. [imatrix: ważenie błędu tym, co model naprawdę używa](#4-imatrix-ważenie-błędu-tym-co-model-naprawdę-używa)
5. [Jakość: co mierzą tabele w repozytorium llama.cpp](#5-jakość-co-mierzą-tabele-w-repozytorium-llamacpp)
6. [Rodziny spoza GGUF: GPTQ, AWQ, SmoothQuant, FP8, NF4, HQQ, EXL, MLX, oQ, ds4](#6-rodziny-spoza-gguf)
7. [Unsloth Dynamic (`UD-`) i plik referencyjny](#7-unsloth-dynamic-ud--i-plik-referencyjny)
8. [Tabela zbiorcza: format × silnik × sprzęt × zastosowanie](#8-tabela-zbiorcza-format--silnik--sprzęt--zastosowanie)
9. [Jakość modelu referencyjnego: czego nie wiemy i jak to zmierzyć](#9-jakość-modelu-referencyjnego-czego-nie-wiemy-i-jak-to-zmierzyć)
10. [Formaty plików: safetensors, GGUF, MLX, ONNX, TensorRT](#10-formaty-plików)
11. [Konwersje i narzędzia: skąd się bierze plik GGUF](#11-konwersje-i-narzędzia)
12. [Kto za tym stoi (Unsloth)](#12-kto-za-tym-stoi-unsloth)
13. [Co z tego dla konfiguracji referencyjnej](#13-co-z-tego-dla-konfiguracji-referencyjnej)
14. [Czego nie ustaliłem](#14-czego-nie-ustaliłem)

---

## 1. Po co kwantyzować: przepustowość i pojemność

Dwa powody, i warto je rozdzielić, bo prowadzą do różnych decyzji.

### 1.1 Pojemność: czy wagi mieszczą się w pamięci

To powód oczywisty. Parametr w BF16/FP16 zajmuje 2 bajty; w 3 bitach — 0,375 bajta.

| Wariant modelu 284B | bity na wagę | rozmiar | mieści się w 4 × 32 GB? |
|---|---|---|---|
| BF16/FP16 | 16 | 568 GB | nie (*moje wyliczenie*: 284·10⁹ · 16 / 8) |
| oryginalny checkpoint DeepSeeka (eksperci FP4, reszta FP8) | ≈ 4,4–4,7 | 167 GB (w tym ok. 11 GB głowicy DSpark) | nie (rozmiar z dziennika wdrożenia w `../przyspieszanie-generowania/`; bpw: *moje wyliczenie*) |
| Q4_K_M „jakby" (4,89 bpw z tabeli README dla Llama-3.1-8B) | 4,89 | ok. 174 GB | nie (*moje wyliczenie*; to tylko skala, nie istniejący plik) |
| referencyjny UD-IQ3_XXS | ≈ 2,9–3,2 (sekcja 7.4) | ok. 104 GB | tak, ale prawie bez zapasu |

Kontrola spójności: eksperci w MXFP4 (4,25 bpw) to 277·10⁹ · 4,25 / 8 ≈ 147 GB, reszta (ok. 7 mld parametrów, ~8 bitów) ok. 7 GB — razem ok. 154 GB, a z rozmiaru 167 GB minus ok. 11 GB głowicy wychodzi ok. 156 GB *(moje wyliczenie)*. Czyli rozbicie 277 + 7 mld parametrów i opis „FP4 + FP8" trzymają się kupy.

Karty mają **34 208 743 424 bajtów** pamięci każda (31,86 GiB; odczyt z `/sys/class/drm/card*/device/mem_info_vram_total` na maszynie w notatkach), czyli razem ok. **136,8 GB**
(127,4 GiB). Nominalne „4 × 32 = 128" to w istocie 127,4 GiB; w GB dziesiętnych jest to 136,8. Pamiętaj o tym przy każdym
porównaniu „plik X GB kontra pamięć": **GB (10⁹) i GiB (2³⁰) różnią się o 7,4 %**, a o tę różnicę w sekcji 7.4 się potkniemy.

### 1.2 Przepustowość: ile bajtów trzeba przeczytać na token

To powód subtelniejszy i ważniejszy dla szybkości. Z rozdziału [02](02-JAK-DZIALA-INFERENCJA.md) wiesz, że dekodowanie (generowanie token po tokenie) jest
**ograniczone przepustowością pamięci**: na każdy token karta czyta z pamięci wszystkie aktywne wagi, a robi z nimi tylko dwa działania zmiennoprzecinkowe na wagę (mnożenie i dodawanie).
Czas kroku ≈ (bajty aktywnych wag) / (przepustowość pamięci). Kwantyzacja zmniejsza licznik.

Dla modelu referencyjnego (*moje wyliczenie*, na bazie parametrów z karty modelu: 13,5 mld aktywnych parametrów po rozbiciu 277 mld ekspertów + ok. 7 mld reszty, patrz niżej):

```
bajty na token ≈ 13,5·10⁹ · (bpw / 8)

bpw = 16     → 27,0 GB na token   (sufit przy 640 GB/s: ~24 tok/s)
bpw = 4,5    →  7,6 GB            (~84 tok/s)
bpw = 2,94   →  4,96 GB           (~129 tok/s)
```

Zgadza się to z rachunkiem z katalogu o przyspieszaniu („~5 GB do przeczytania na token"). To jest **sufit dla jednej karty przy 100 % wykorzystania pamięci**; zmierzone 23,5 → 49 tok/s
to już inna historia (przekazania między kartami, nieregularny odczyt ekspertów) — opisana tam, nie tu.
Przepustowość 640 GB/s to liczba z drugiej ręki (*źródło zewnętrzne*, Wikipedia o rodzinie RX 9000; strony AMD nie udało się pobrać) — traktuj jako parametr, nie fakt.

Dwie rzeczy, które ten rachunek ukrywa:

1. **Nie wszystkie wagi są jednakowo skwantyzowane.** W rzeczywistym pliku uwaga, osadzenia i wyjście mają 4–8 bitów, a eksperci 2–3 (sekcja 7). Efektywna liczba bajtów na token jest więc wyższa niż
   „średnia × aktywne". Pomiar z notatek: ds4 na Macu M5 Max (Q2, średnio 2,45 bpw) osiąga 39,35 tok/s, podczas gdy wzór wróżył ok. 154 — czyli 26 % sufitu *(dane projektu + moje wyliczenie)*. Wzór to **górne ograniczenie**.
2. **Kwantyzacja przesuwa „punkt przegięcia" (ridge) roofline'u w lewo**: im mniej bajtów na wagę, tym mniej tokenów w partii wystarczy, żeby karta zaczęła być ograniczona obliczeniami, a nie pamięcią
   (przy 150 FLOP/B: partia 150 dla FP16, 75 dla 8 bitów, 38 dla 4 bitów, 28 dla 3 bitów *(moje wyliczenie z notatki o podstawach; 96 TFLOPS i 640 GB/s są niezweryfikowane)*).
   W praktyce jądra i tak odkwantyzowują w ALU lub liczą na całkowitoliczbowych iloczynach skalarnych INT8 (ścieżka `mmq` w llama.cpp, z aktywacjami w Q8_1), więc efektywny punkt jest wyżej.

### 1.3 Kwantyzacja nie jest darmowa

Mniej bitów to większy błąd. Cała reszta rozdziału odpowiada na pytanie: **jak wydać budżet bitów mądrze** (gdzie dać ich więcej, jak zapisać skale, jak wybrać wartości reprezentacyjne) i **jak zmierzyć, ile jakości
to kosztowało**. Osobna sprawa — kwantyzacja *pamięci podręcznej KV* (`-ctk`/`-ctv`) — jest poza tym rozdziałem (rozdział 02); wspominam tylko, że w llama.cpp tryb tensorowy wymaga **niekwantyzowanego** KV
(notatka z `docs/multi-gpu.md`), więc przy wdrożeniu referencyjnym `-ctk f16 -ctv f16` jest wymogiem, nie wyborem.

---

## 2. Kwantyzacja blokowa od zera: 8 wag na kartce

### 2.1 Pomysł

Wagi to liczby zmiennoprzecinkowe, powiedzmy z zakresu −1…1. Chcemy je zapisać na 4 bitach, czyli jako liczby całkowite 0…15. Nie da się tego zrobić wprost — trzeba **skali**:
`w ≈ d · (q − 8)`, gdzie `q` to 4-bitowa liczba całkowita (0…15), a `d` — jedna liczba zmiennoprzecinkowa (skala) dzielona przez grupę wag. Zapamiętujemy `q` dla każdej wagi i `d` raz na grupę.
Przy odczycie mnożymy. To dokładnie ta konstrukcja, którą w llama.cpp realizuje typ Q4_0: `block_q4_0` = skala fp16 + 16 bajtów nibble'i na 32 wagi, a wartość to `d · (q − 8)`.

**Analogia:** to linijka z podziałką. Zamiast mierzyć każdą wagę w milimetrach (16 bitów), mierzysz ją w „ząbkach" linijki (4 bity), a rozmiar ząbka — `d` — zapisujesz raz na kilkadziesiąt pomiarów.
Im większy rozrzut wartości w grupie, tym grubszy ząbek i tym większy błąd.

### 2.2 Przykład policzony ręcznie

Weź 8 wag (osiem, żeby zmieściły się na kartce; prawdziwy blok ma 32 lub 256):

```
w = [ 0,12  −0,31  0,05  0,47  −0,08  0,22  −0,55  0,03 ]
```

**Uproszczona reguła skali** (moja dydaktyczna wersja; dokładnej funkcji `quantize_row_q4_0` nie czytałem, więc szczegóły doboru skali w llama.cpp mogą się różnić):
niech waga o największym module trafi na skraj zakresu. Tu to −0,55, a zakres to 16 poziomów, więc `d = 0,55 / 8 = 0,06875`.
Następnie `q = zaokrąglenie(w / d + 8)`, obcięte do 0…15.

| waga w | w / d + 8 | q (zapisane na 4 bitach) | odtworzone d·(q−8) | błąd bezwzględny |
|---:|---:|---:|---:|---:|
| 0,12 | 9,75 | 10 | 0,1375 | 0,0175 |
| −0,31 | 3,49 | 3 | −0,3438 | 0,0338 |
| 0,05 | 8,73 | 9 | 0,0688 | 0,0188 |
| 0,47 | 14,84 | 15 | 0,4813 | 0,0113 |
| −0,08 | 6,84 | 7 | −0,0688 | 0,0112 |
| 0,22 | 11,20 | 11 | 0,2063 | 0,0137 |
| −0,55 | 0,00 | 0 | −0,5500 | 0,0000 |
| 0,03 | 8,44 | 8 | 0,0000 | 0,0300 |

*(moje wyliczenie; zaokrąglenie połówek w górę)*. Największy błąd to 0,0338, czyli ok. **połowa „ząbka" `d`** (0,034) — to teoretyczny najgorszy przypadek zaokrąglenia, bez niespodzianek.
Zwróć uwagę na ostatnią wagę: 0,03 trafiła na `q = 8`, czyli **dokładnie zero**. Małe wagi zlewają się w zero; to cena.

**Ta sama grupa na 8 bitach** (zakres −127…127, `d = 0,55/127 = 0,00433`): odtworzone wartości to 0,1213; −0,3118; 0,0520; 0,4720; −0,0780; 0,2209; −0,5500; 0,0303, największy błąd **0,0020** — ok. 16× mniejszy,
bo ząbek jest 16× drobniejszy. Tak wygląda Q8_0 wobec Q4_0.

**Koszt pamięci tej zabawki.** 8 wag × 4 bity = 32 bity, plus skala fp16 = 16 bitów → 48 bitów na 8 wag = **6 bitów na wagę**. Prawdziwy blok Q4_0 ma 32 wagi:
(32 · 4 + 16) / 32 = **4,5 bpw** (bits per weight, bity na wagę). Skala „podatkuje" każdą wagę: im mniejszy blok, tym drobniej dopasowana skala, ale tym większy podatek.

### 2.3 Dlaczego bloki, a nie jedna skala na tensor

Dodaj do grupy jedną wagę-odstającą (outlier): zamiast 0,03 niech ostatnia będzie **−2,2**.

* **Jedna skala na wszystkie 8:** `d = 2,2 / 8 = 0,275`. Wagi 0,12; 0,05; −0,08 odtwarzają się jako **0,000** (błąd do 0,12 — tyle, ile sama waga); 0,22 → 0,275; −0,31 → −0,275. RMS błędu (pierwiastek ze średniego kwadratu): **0,065**.
* **Dwa bloki po 4:** pierwszy (0,12; −0,31; 0,05; 0,47) ma własną skalę ≈ 0,059; największy błąd w nim to **0,016**. Drugi blok (zawierający outliera) cierpi jak wyżej (błąd do 0,08), ale **szkoda zostaje w jego granicach**.

*(moje wyliczenie, tą samą uproszczoną regułą.)* Wniosek: jeden outlier „psuje" skalę wszystkich wag, z którymi dzieli blok. Bloki ograniczają zasięg szkody — i dlatego wszystkie
formaty z tego rozdziału, od Q4_0 po MXFP4, są **blokowe**. Kernel mnoży w locie: dla każdego bloku wykonuje całkowitoliczbowy iloczyn skalarny wag z aktywacjami (te też kwantyzowane do Q8) i mnoży wynik przez dwie skale
(`mmq`, `mmvq`, na CPU `vec_dot` — notatki do llama.cpp).

### 2.4 Dwupoziomowe skale: pomysł K-quantów

Jeśli mały blok (32 wagi) jest dobry dla dokładności, a skala fp16 kosztuje 0,5 bpw, to można… **skwantyzować same skale**. K-quanty (Iwan Kawrakow, PR #1684, zmergowany 2023-06-05) robią tak:

* **super-blok** 256 wag = 8 pod-bloków po 32 (typy Q4_K, Q5_K) albo 16 po 16 (Q2_K, Q3_K, Q6_K);
* każdy pod-blok ma własną skalę (i, w typach „type-1", własne minimum) zapisaną na **6 bitach** (Q3_K/Q4_K/Q5_K), 4 bitach (Q2_K) lub 8 bitach (Q6_K);
* dopiero te skale mają jedną „nadskalę" fp16 (`d`) i nadminimum (`dmin`) na cały super-blok.

Rachunek dla Q4_K, ze struktury `block_q4_K` w `ggml/src/ggml-common.h` (linia 338, `static_assert`):

```
2 · fp16 (d, dmin)                         =   4 B
12 B spakowanych skal i minimów 6-bitowych =  12 B   (8 pod-bloków × (6+6) bitów = 96 bitów)
256 wag × 4 bity                           = 128 B
                                           ─────────
                                             144 B na 256 wag  → 144·8/256 = 4,5 bpw
```

Narzut skal to 16 B / 256 wag = **0,5 bpw**. Gdyby każdy pod-blok po 32 wagi miał skalę **i** minimum w fp16 (jak w starszym Q4_1), narzut wyniósłby 4 B / 32 wagi = **1,0 bpw** — Q4_1 ma 5,0 bpw, Q4_K 4,5 przy tej samej wielkości pod-bloku.
Dwupoziomowe skale kupiły więc pół bita na wagę, bez grubszych ząbków.

> **Sprawdź sam 1 — policz bpw z kodu.** Otwórz `ggml/src/ggml-common.h` w drzewie llama.cpp i znajdź wiersze `static_assert(sizeof(block_…) == …)`
> (dla Q4_K linia 338, dla Q6_K 368, dla IQ3_XXS 411). Każdy z nich to rachunek rozmiaru bloku w bajtach; podziel przez liczbę wag w bloku (32 albo `QK_K` = 256, linia 89) i pomnóż przez 8.
> Na przykład: `grep -n "static_assert(sizeof(block_" ~/llama.cpp-0ce8cd1/ggml/src/ggml-common.h` (samo czytanie pliku, GPU nietknięte).

---

## 3. Rodziny typów w llama.cpp, z dokładnym bpw

Poniżej liczę bity na wagę ze struktur `block_*` (rozmiary z `static_assert` w `ggml/src/ggml-common.h`, drzewo `0ce8cd1`). To jest **bpw bloku** — „(bity bloku) / (liczba wag w bloku)", ze skalami wliczonymi.
Uwaga: README llama.cpp podaje inne liczby (np. IQ3_XXS 3,2548 bpw dla Llama-3.1-8B), bo to **średnia z całego pliku**, w którym część tensorów (osadzenia, wyjście, normy) jest w innych typach.

### 3.1 Typy dawne („legacy"): Q4_0, Q4_1, Q5_0, Q5_1, Q8_0

Jeden poziom skal: blok 32 wag, skala fp16 (+ minimum fp16 w typach „_1"), + ewentualny piąty bit.

| typ | struktura bloku (32 wag) | bajty | bpw |
|---|---|---:|---:|
| Q4_0 | fp16 `d` + 16 B nibble'i | 18 | **4,5** |
| Q4_1 | fp16 `d`, fp16 `m` + 16 B | 20 | **5,0** |
| Q5_0 | fp16 `d` + 4 B (piąte bity) + 16 B | 22 | **5,5** |
| Q5_1 | fp16 `d`, fp16 `m` + 4 B + 16 B | 24 | **6,0** *(moje wyliczenie z `static_assert`)* |
| Q8_0 | fp16 `d` + 32 × int8 | 34 | **8,5** |

Q8_0 jest dziś głównie „prawie bezstratnym" wariantem do referencji i formatem **aktywacji** w kernelach (Q8_1 z dodatkową sumą; 36 B / 32 wag = 9,0 bpw, ale to nie format zapisu wag). Q4_0 i Q4_1 są w tabelach jakości wyraźnie gorsze od K-quantów
przy podobnym rozmiarze (sekcja 5).

### 3.2 K-quanty: Q2_K … Q6_K

Super-bloki po 256, dwa poziomy skal (sekcja 2.4). Rozmiary z `static_assert`:

| typ | rozkład bajtów w super-bloku (256 wag) | bajty | bpw |
|---|---|---:|---:|
| Q2_K | 16 B skal+minimów (4+4 bity × 16 pod-bloków) + 64 B wag 2-bitowych + 2 × fp16 | 84 | **2,625** |
| Q3_K | 32 B (bit wysoki) + 64 B (2 bity niskie) + 12 B skal + fp16 `d` | 110 | **3,4375** |
| Q4_K | 2 × fp16 + 12 B skal/minimów + 128 B | 144 | **4,5** |
| Q5_K | 2 × fp16 + 12 B + 128 B + 32 B (piąty bit) | 176 | **5,5** |
| Q6_K | 128 B (niskie nibble'e) + 64 B (2 bity wysokie) + 16 × int8 skal + fp16 `d` | 210 | **6,5625** |
| Q8_K | fp32 `d` + 256 × int8 + 16 × int16 sum | 292 | 9,125 (tylko wewnętrznie, aktywacje) |

Q2_K, Q4_K, Q5_K to typy „type-1" (`w = d·q + m`, ze skalą i minimum), a Q3_K i Q6_K — „type-0" (`w = d·q`, samą skalą) *(dane projektu: treść PR #1684)*.

**Przyrostki `_S`, `_M`, `_L` to nie są typy bloków, tylko *przepisy* (mieszanki).** `Q4_K_M` nie jest „blokiem Q4_K_M": to plik, w którym większość tensorów jest w Q4_K, ale np. połowa `attn_v` i `ffn_down` w Q6_K,
a `output.weight` zawsze w 6 bitach *(dane projektu: PR #1684)*. Dzisiejsze reguły mieszanek siedzą w `src/llama-quant.cpp` (linie ok. 465–735 w drzewie `0ce8cd1`) i są mocno rozbudowane (osobne ścieżki dla GQA i MoE).
Pierwowzór tego myślenia — „daj więcej bitów tym warstwom, na których to ma znaczenie" — jest dokładnie tym, co robią potem Unsloth Dynamic, oQ w oMLX i recepta ds4 (sekcje 6–7).

### 3.3 i-quanty: IQ1…IQ4 (kodowanie przez książkę kodową)

Dotąd każda waga miała własny `q`. i-quanty (IQ) robią coś innego dla niskich bitów: grupę kilku wag (np. 8) zastępują **indeksem w tablicy wzorców** (książka kodowa, *codebook*), wybranej tak, by dobrze pokrywać
rozkład wag. Inspiracja: praca QuIP# *(dane projektu: treść PR #4773)*. Prowenans z notatek, wszystko z treści PR:

* **#4773** (zmergowany 2024-01-08): „prawdziwe" 2 bity, **2,0625 bpw**; pożycza z QuIP# trik z parzystością znaków (7 bitów koduje 8 znaków) i książkę kodową z punktów siatki **E8** (256 punktów); zamiast hadamardowych rotacji z QuIP#
  używa zwykłego skalowania blokowego ggml.
* **#4897**: kod kwantyzacji i **zakaz IQ2_XXS/IQ2_XS bez imatrix** (w zgłoszeniu: bez niego wynik jest „śmieciowy").
* **#5196** (2024-01-30): **IQ3_XXS 3,0625 bpw**, siatka **D4** (256 punktów), 92 bity na 32 wagi + 4-bitowa skala.

Rozmiary z `static_assert`:

| typ | bajty / 256 wag | bpw | uwagi |
|---|---:|---:|---|
| IQ1_S | 50 | **1,5625** | |
| IQ1_M | 56 | **1,75** | |
| IQ2_XXS | 66 (fp16 + 64 × uint16) | **2,0625** | wymaga imatrix |
| IQ2_XS | 74 | **2,3125** | wymaga imatrix |
| IQ2_S | 82 | **2,5625** | |
| IQ3_XXS | 98 (fp16 + 96 B) | **3,0625** | typ z nazwy pliku referencyjnego |
| IQ3_S | 110 | **3,4375** | |
| IQ4_NL | 18 / 32 wag | **4,5** | 16-elementowa nieliniowa tabela wartości |
| IQ4_XS | 136 | **4,25** | blok 256, 6-bitowe pod-skale |

Cena: odkodowanie przez tabelę jest kosztowniejsze niż mnożenie — w README llama.cpp (Llama-3.1-8B, sprzęt niepodany) kwanty K i IQ generują tokeny w podobnym tempie, IQ „ze słabym narzutem obliczeń".
Nazwa „IQ" **nie znaczy „wymaga imatrix"** (to prawda tylko dla IQ2_XXS/XS) — notatka o podstawach w tym miejscu była za uproszczona.

### 3.4 MXFP4 i NVFP4: formaty zmiennoprzecinkowe 4-bitowe

Zamiast liczb całkowitych — mikro-liczby zmiennoprzecinkowe **E2M1** (1 bit znaku, 2 wykładnika, 1 mantysy; 16 możliwych wartości), z blokową skalą.

| format | blok | skala | bajty | bpw |
|---|---|---|---:|---:|
| **MXFP4** (OCP Microscaling, arXiv 2310.10537) | 32 wagi | 1 bajt **E8M0** (potęga dwójki) | 17 | **4,25** |
| **NVFP4** (NVIDIA) | 64 wagi = 4 pod-bloki po 16 | po 1 bajcie **UE4M3 (FP8)** na pod-blok; **plus** jeden fp32 na cały tensor, zapisany osobno | 36 | **4,5** |

W ggml: `block_mxfp4` = bajt `e` + 16 bajtów `qs`; typy `GGML_TYPE_MXFP4 = 39`, `NVFP4 = 40`. Konwerter llama.cpp ma „bezstratne" przepakowania ekspertów MXFP4 i NVFP4 (z `compressed-tensors`, ModelOpt) — „only moves bits", plik `conversion/base.py`.
To ważne dla ciebie, bo **eksperci DeepSeek-V4 są natywnie w FP4** (`expert_dtype: fp4` w konfiguracji checkpointu), a gpt-oss wychodzi w MXFP4.
NVIDIA twierdzi, że NVFP4 daje „1 % lub mniej" degradacji względem FP8 na DeepSeek-R1-0528 *(dane firmy)*. Szybkie mnożenie w FP4 wymaga rdzeni tensorowych Blackwell (5. generacji) — na gfx1201 FP4 to tylko format **przechowywania**
z programowym odkodowaniem; wsparcie jąder dla typów MX na gfx1201 *(niezweryfikowane)*.

### 3.5 Typy trójkowe i ekstremalne: TQ1_0, TQ2_0, Q1_0, Q2_0

* **TQ1_0**: 54 B / 256 wag (fp16 + 4 B + 48 B, „trójki" kodowane po 5 w bajcie) → **1,6875 bpw**; **TQ2_0**: 66 B / 256 → **2,0625 bpw**. Przeznaczone dla modeli trenowanych jako trójkowe (BitNet), nie do kwantyzowania zwykłych modeli.
  Co ciekawe, konwerter `convert_hf_to_gguf.py` ma `--outtype` z wartościami `f32, f16, bf16, q8_0, tq1_0, tq2_0, auto` (linia 60) — to jedyne typy, które potrafi zapisać bezpośrednio.
* **Q1_0** (128 wag: 18 B → **1,125 bpw**) i **Q2_0** (64 wagi: 18 B → **2,25 bpw**): nowe w tym drzewie (typy 41 i 42), `GGML_TYPE_COUNT = 43`. Kernele *(niezweryfikowane)*.

### 3.6 Co jeszcze jest „w rodzinie", choć nie w tym drzewie

`ik_llama.cpp` (fork Iwana Kawrakowa, rozdział [04](04-LLAMA-CPP-I-RODZINA-GGML.md)) ma własne typy: IQ2_K…IQ6_K, kwanty „trellis" IQ1_KT…IQ4_KT, warianty z przeplotem wierszy (`_R4`) dla CPU.
**Pliki z tymi typami ładują się tylko w ik_llama.cpp** — to realne uzależnienie od forka; zwykły llama.cpp ich nie wczyta. Dla referencyjnej maszyny AMD to rzecz do wiedzenia, nie do używania
(HIP/ROCm dla gfx1201 w ik_llama.cpp nie jest udokumentowanym celem, *niezweryfikowane*).

Przepisy mieszanek (reguła `use_more_bits(i_layer, n_layers)` i gałęzie dla `attn_v`, `ffn_down`, GQA, MoE) czytaj w `src/llama-quant.cpp`, linie ok. 465–735 — przyda się to w sekcji 7.3, gdzie porównam je z plikiem Unsloth.

---

## 4. imatrix: ważenie błędu tym, co model naprawdę używa

Standardowy kwantyzator minimalizuje błąd odtworzenia każdej wagi jednakowo. Ale nie każda waga jest jednakowo ważna: błąd w kolumnie macierzy, przez którą przechodzą duże aktywacje, psuje wynik bardziej
niż błąd w kolumnie, którą aktywacje ledwo muskają.

**Macierz ważności (imatrix)** to dla każdego tensora wektor: dla każdej kolumny — **suma kwadratów aktywacji** (po tokenach tekstu kalibracyjnego). Kwantyzator używa go jako wag w ważonej metodzie najmniejszych kwadratów:
wartości reprezentacyjne dobiera tak, by błąd był mały **tam, gdzie wektor ważności jest duży**. To przybliżenie *diagonalne* („ignoring non-diagonal elements" w treści PR **#4861**, zmergowany 2024-01-12):
pełna macierz drugiego rzędu (jak w GPTQ) byłaby ogromna.

Co z tego wynika:

* To **nie jest trening** — wagi nie są aktualizowane „w dół gradientu", jedynie inaczej zaokrąglane.
* Wynik **zależy od tekstu kalibracyjnego** (język, dziedzina) i może się do niego przeuczyć. Unsloth publikuje własne pliki imatrix (dla Qwen3-Coder-30B: `imatrix_unsloth.gguf_file`, 122 MB).
  W README llama.cpp jest też eksperyment (tabela w sekcji 5): dla IQ1_S czy Q2_K **więcej tokenów wikitext do imatrix nie dało spójnej poprawy** (10k vs 10m tokenów).
* Dla niskich bitów to **warunek konieczny** (IQ2_XXS/XS). Dla Q4_K_M — poprawa mała, lecz mierzalna: w tabeli Llama-3-8B (sekcja 5) KLD spada z 0,0313 do 0,0282 (≈ −10 %).
* Domyślnie imatrix **nie jest** używany dla `output.weight` i osadzeń (`--process-output` wyłączone) — „zwykle lepiej nie używać go dla tych tensorów" (README narzędzia).

Polecenia (z `tools/imatrix/README.md` i `tools/quantize/README.md` w drzewie `0ce8cd1`, *nie uruchamiałem*):

```bash
# 1) obliczenie imatrix na tekście kalibracyjnym, z modelu F16/BF16
llama-imatrix -m model-f16.gguf -f kalibracja.txt -ngl 99 -o imatrix.gguf

# 2) kwantyzacja z imatrix (ostatni argument: liczba wątków)
llama-quantize --imatrix imatrix.gguf model-f16.gguf model-Q4_K_M.gguf Q4_K_M 8
```

---

## 5. Jakość: co mierzą tabele w repozytorium llama.cpp

Są dwie miary, i trzeba wiedzieć, co każda znaczy.

* **Perplexity (PPL)** — jak dobrze model przewiduje następny token na zadanym tekście (niżej = lepiej). *Nie jest porównywalna między modelami* z różnymi tokenizatorami, a dla modeli po dostrojeniu bywa wyższa mimo lepszych odpowiedzi
  (README narzędzia). Liczby llama.cpp nie są porównywalne z liczbami innych projektów.
* **Dywergencja Kullbacka–Leiblera (KLD)** — odległość między rozkładem prawdopodobieństwa następnego tokenu modelu referencyjnego (FP16) a skwantyzowanego, uśredniona po tokenach. 0 = identyczne rozkłady.
  **KLD jest czulszą miarą szkody od PPL**, bo PPL może „ukryć" szkodę (zmiany w górę i w dół się kasują), a KLD nie. Obok KLD narzędzie liczy m.in. „same top p" — jak często oba modele przypisują najwyższe prawdopodobieństwo temu samemu tokenowi.

### 5.1 Tabela referencyjna: Llama-3-8B, KLD względem FP16

Źródło: `tools/perplexity/README.md` w drzewie `0ce8cd1` (dodane przez Johannesa Gäßlera, PR #6936, 2024-04-30). **Konfiguracja:** rewizja llama.cpp `f364eb6f`, backend CUDA, CPU AMD EPYC 7742, GPU 1 × RTX 4090,
korpus Wikitext-2 (test), model Llama-3-8B; referencja to logity FP16 zapisane do pliku. „imatrix WT 10m" = imatrix z 10 mln tokenów wikitext. Wybrałem wiersze; pełna tabela jest w README.

| typ | imatrix | rozmiar [GiB] | PPL | ΔPPL | KLD | RMS Δp |
|---|---|---:|---:|---:|---:|---:|
| f16 | – | 14,97 | 6,2332 | 0,0015 | 0,00055 | 0,79 % |
| q8_0 | – | 7,96 | 6,2343 | 0,0027 | 0,00136 | 1,20 % |
| q6_K | – | 6,14 | 6,2534 | 0,0217 | 0,00545 | 2,30 % |
| q5_K_M | – | 5,33 | 6,2886 | 0,0570 | 0,01076 | 3,16 % |
| q4_K_M | WT 10m | 4,58 | 6,3829 | 0,1513 | 0,02815 | 5,25 % |
| q4_K_M | – | 4,58 | 6,4071 | 0,1755 | 0,03127 | 5,52 % |
| iq4_XS | WT 10m | 4,14 | 6,4597 | 0,2281 | 0,03633 | 6,04 % |
| q4_0 | – | 4,34 | 6,7001 | 0,4685 | 0,07194 | 8,43 % |
| q3_K_M | WT 10m | 3,74 | 6,7343 | 0,5026 | 0,08436 | 9,29 % |
| iq3_S | WT 10m | 3,42 | 6,9655 | 0,7339 | 0,11128 | 10,85 % |
| **iq3_XXS** | WT 10m | **3,05** | 7,4584 | 1,2268 | **0,18363** | 13,84 % |
| q3_K_S | WT 10m | 3,41 | 7,6029 | 1,3712 | 0,19982 | 14,98 % |
| q2_K | WT 10m | 2,96 | 8,6478 | 2,4162 | 0,33222 | 18,88 % |
| iq2_XS | WT 10m | 2,43 | 10,7614 | 4,5298 | 0,54629 | 23,87 % |
| iq2_XXS | WT 10m | 2,24 | 14,0918 | 7,8601 | 0,81202 | 28,58 % |
| iq1_S | WT 1m | 1,88 | 58,0978 | 51,8661 | 2,21128 | 46,42 % |

*(rozmiar w GiB dla modelu 8B; „f16" w tej tabeli to różnica spowodowana wyłącznie rzutowaniem logitów na 16 bitów).*

Trzy rzeczy do zapamiętania z tej tabeli:

1. **Schody, nie rampa.** Od Q8_0 do Q5_K_M KLD rośnie ok. 8×, od Q5_K_M do Q4_K_M 3×, a od Q4_K_M do IQ3_XXS 6,5× (0,028 → 0,184). Poniżej 3 bitów jakość zjeżdża gwałtownie (IQ2_XXS: PPL ponad 2× wyższa niż FP16; IQ1_S: nie do użytku).
2. **Imatrix pomaga zawsze, bardziej przy niskich bitach.** Q3_K_M: 0,1019 bez, 0,0844 z imatrix; Q3_K_S: 0,2282 vs 0,1998.
3. **Przy tym samym rozmiarze typy IQ biją K-quanty.** IQ3_S (3,42 GiB, KLD 0,111) vs Q3_K_S (3,41 GiB, KLD 0,200) — prawie ten sam rozmiar, KLD o 44 % niższy.

### 5.2 Ten sam typ szkodzi nowszym modelom bardziej

Z tego samego README: LLaMA-2-7B vs LLaMA-3-8B (ta sama konfiguracja, KLD względem FP16):

| typ | KLD LLaMA-2-7B | KLD LLaMA-3-8B | stosunek PPL (kwant / FP16): 2-7B → 3-8B |
|---|---:|---:|---|
| Q2_K | 0,1089 | 0,4451 | 1,108 → 1,565 |
| Q4_K_M | 0,01269 | 0,03127 | 1,0142 → 1,0282 |
| Q6_K | 0,00210 | 0,00545 | – |
| Q8_0 | 0,00037 | 0,00136 | – |

Autorzy zwracają uwagę: LLaMA-3 po Q2_K ma PPL wyższą o 56 %. **Mocniej wytrenowane modele są trudniej kompresowalne.** Dla ciebie wniosek jest niewygodny: tabele sprzed lat o starszych modelach
**zaniżają** straty na nowoczesnych modelach, a żadnej tabeli in-tree dla nowoczesnego MoE nie ma (patrz sekcja 9).

### 5.3 Starsze dane o rozmiarze modelu

* **LLaMA-2-70B, Wikitext-2** (to samo README): FP16 PPL 3,4313 (128,5 GiB); Q6_K +0,16 % (52,70 GiB); Q5_K_M +0,40 % (45,41); Q4_K_M +1,20 % (38,54); Q3_K_M +4,72 % (30,83); Q2_K +8,82 % (27,27).
  Czyli na modelu **70B** ta sama kwantyzacja szkodzi względnie mniej niż na 7–8B (Q2_K: +8,8 % dla 70B kontra +56 % dla LLaMA-3-8B — ale to różne rodziny, więc nie wyciągaj stąd „prawa przyrody").
* **PR #1684 (czerwiec 2023, LLaMA-1, wikitext, kontekst 512):** PPL FP16 5,9066 (7B) → Q2_K 6,7764, Q3_K_M 6,1503, Q4_K_S 6,0215, Q4_K_M 5,9601, Q5_K_S 5,9419, Q6_K 5,9110. Autor: 6 bitów mieści się w 0,1 % FP16 i błąd względny **nie maleje** wraz z rozmiarem modelu powyżej 13B *(dane projektu)*.
* **PR #5196 (styczeń 2024, imatrix z wiki.train.raw):** IQ3_XXS bije Q3_K_XS przy mniejszym rozmiarze, np. Mistral-7B 2,705 GiB / PPL 6,0578 vs 2,786 GiB / 6,1632; Mixtral-8x7B 17,05 GiB / 4,4570 vs 17,75 / 4,5174.
  Przy kontekście 4096: IQ3_XXS Mixtral 3,7689, LLaMA-2-70B 3,2757 *(dane projektu)*.

### 5.4 Rozmiar pliku a prędkość

W README `tools/quantize/README.md` (Llama-3.1-8B; **sprzęt w pliku niepodany**) są średnie bpw całych plików i prędkość generowania: Q4_K_M 4,8944 bpw — 71,93 tok/s, Q8_0 8,5008 — 50,93, F16 16,0005 — 29,17 (tg128).
Prędkość dekodowania **idzie za liczbą bajtów** — to ta sama prawidłowość co w sekcji 1.2, tylko widziana z drugiej strony. Przepisy IQ mają dodatkowy koszt obliczeniowy, niewielki na tej maszynie.

Średnie bpw całych plików (Llama-3.1-8B, to samo README): IQ1_S 2,0042; IQ2_XXS 2,3824; IQ3_XXS 3,2548; IQ4_XS 4,4597; Q2_K 3,1593; Q3_K_M 3,9960; Q4_K_M 4,8944; Q5_K_M 5,7036; Q6_K 6,5633; Q8_0 8,5008.
Zauważ: „Q2_K" ma w pliku 3,16 bpw, nie 2,625 — bo `output.weight`, osadzenia, części `attn_v`/`ffn_down` są w wyższych typach. **To ta sama lekcja, która w sekcji 7 wyjaśni, dlaczego „IQ3_XXS" z nazwy modelu referencyjnego ma średnio inną liczbę bitów niż 3,0625.**

> **Sprawdź sam 2 — tabela KLD u źródła.** `tools/perplexity/README.md` w drzewie llama.cpp: sekcja „LLaMA 3 8b Scoreboard" (konfiguracja na górze: rewizja, backend, CPU, GPU) i opis statystyk pod `--kl-divergence`.
> Przeczytaj akapit o tym, że plik logitów referencyjnych jest duży (README: 11 GiB dla LLaMA 2, 37 GiB dla LLaMA 3 na zbiorze testowym Wikitext-2) — to ważne, gdy w sekcji 9 zaplanujesz pomiar na modelu o słowniku 129 280 tokenów.

---

## 6. Rodziny spoza GGUF

Wszystko, co niżej, żyje głównie w świecie **safetensors + serwery** (vLLM, SGLang, TensorRT-LLM) albo w świecie Apple (MLX). Dla ciebie ważne jest przede wszystkim to, **czy dany format ma
w ogóle jądro na gfx1201** (sekcja 8) i **czy da się go zamienić na GGUF**.

### 6.1 GPTQ (Frantar, Ashkboos, Hoefler, Alistarh; arXiv 2210.17323, 2022)

Jednorazowa (*one-shot*) kwantyzacja **tylko wag**, na 3–4 bity, z użyciem przybliżonej informacji drugiego rzędu (Hesjan): wagi kwantyzuje się kolejno, a błąd zaokrąglenia każdej z nich
**kompensuje się korektą jeszcze niezkwantyzowanych wag** tak, by wyjście warstwy zmieniło się jak najmniej na próbce kalibracyjnej. Autorzy podają ok. 4 godzin GPU dla modelu 175B i przyspieszenia generowania 3,25× (A100) / 4,5× (A6000)
dzięki własnym jądrom *(dane projektu / abstrakt)*. Typowy układ: 4 bity, grupa 128, skala fp16 i zero 4-bitowe → 4 + (16 + 4)/128 ≈ **4,16 bpw** *(moje wyliczenie dla częstej konfiguracji)*.
Checkpoint to safetensors z tensorami `qweight/qzeros/scales/g_idx`. llama.cpp **czyta** taki checkpoint, ale tylko go **odkwantyzowuje do liczb zmiennoprzecinkowych i kwantyzuje od nowa** (`conversion/base.py` linia ok. 495).

### 6.2 AWQ (Lin, Tang, Tang i in.; arXiv 2306.00978; MLSys 2024 — nagroda za najlepszą pracę)

Pomysł przeciwny do GPTQ: nie rekonstruuje się błędu, tylko **chroni się ok. 1 % „istotnych" kanałów**, wybranych według wielkości **aktywacji** (nie wag), przez przeskalowanie ich przed kwantyzacją. Bez propagacji wstecznej i bez rekonstrukcji.
Autorzy twierdzą, że jest odporniejszy na zmianę zbioru kalibracyjnego niż GPTQ *(dane projektu)*. Pamięć jak w GPTQ g128: ≈ 4,16 bpw *(moje wyliczenie)*.
**llama.cpp nie ładuje AWQ**: konwerter zgłasza `NotImplementedError: Quant method is not yet supported` (`conversion/base.py` linia ok. 573).
Stan narzędzi (GitHub API, 2026-10-19): **AutoAWQ zarchiwizowany** (2025-05-11), **AutoGPTQ zarchiwizowany** (2025-04-11); żywe ścieżki to `vllm-project/llm-compressor` (3,9 tys. gwiazdek, aktywny),
GPTQModel (1,3 tys.) i `NVIDIA/Model-Optimizer` (5,4 tys., Apache-2.0). Jeśli w poradniku zobaczysz „pip install autoawq", wiedz, że to martwy projekt.

### 6.3 SmoothQuant (Xiao, Lin i in.; arXiv 2211.10438; ICML 2023)

Jedyny w tym zestawie, który kwantyzuje także **aktywacje do INT8** (W8A8). Problem: aktywacje mają kanały-outliery, które psują INT8. Rozwiązanie: matematycznie równoważne przeniesienie „trudności" z aktywacji do wag przez skalowanie
kanałów. Zysk (dane autorów): do 1,56× szybciej i 2× mniej pamięci. Wymaga **jednostek INT8 GEMM** — to technika przepustowości serwera, nie sposób na „zmieścić duży model w VRAM". W vLLM jako `w8a8_int8` / compressed-tensors.

### 6.4 FP8 (Micikevicius i in.; arXiv 2209.05433)

Dwie postaci: **E4M3** (4 bity wykładnika, 3 mantysy; bez nieskończoności, jeden wzorzec NaN) i **E5M2** (zbliżony do IEEE). Konwencja: E4M3 dla wag i aktywacji. Rzeczywiste checkpointy dodają skale:
na tensor, na kanał albo na blok (np. 128×128: 8 + 32/16384 ≈ 8,002 bpw *(moje wyliczenie)*). Właśnie tak jest zapisana „reszta" (nie-eksperci) w oryginalnym checkpoincie DeepSeek-V4: FP8 poza ekspertami w FP4.
W vLLM na ROCm kernel `ROCmFP8ScaledMMLinearKernel` deklaruje obsługę „CDNA3+ (gfx942/gfx950) lub RDNA4 (gfx12x)" — czyli **FP8 jest dopuszczone w kodzie na gfx1201**, ale wydajności nie zmierzono (*niezweryfikowane*).

### 6.5 bitsandbytes NF4 i podwójna kwantyzacja (QLoRA; Dettmers i in.; arXiv 2305.14314, 2023)

**NF4** („NormalFloat", 4 bity) to zestaw 16 wartości rozmieszczonych tak, by były optymalne dla wag o rozkładzie normalnym z zerową średnią; blok 64 wagi ze skalą fp32 (absmax) = 4 + 32/64 = **4,5 bpw**.
**Podwójna kwantyzacja** kwantyzuje jeszcze same skale (8 bitów na 64, plus fp32 na 256 skal): 4 + 8/64 + 32/(64·256) = **4,127 bpw** (jak w artykule: oszczędność 0,37 bita na parametr, ok. 3 GB dla modelu 65B).
To format **do treningu** (QLoRA: zamrożony model w NF4 + adaptery LoRA); przy wnioskowaniu wagi są odkwantyzowywane do bf16 przed mnożeniem — stąd wolne dekodowanie. Wspierany w transformers, PEFT, Unsloth (do treningu), vLLM, SGLang;
**nie** w llama.cpp ani MLX.

### 6.6 HQQ, EXL2, EXL3

* **HQQ** (Half-Quadratic Quantization): **bez kalibracji**, kwantyzuje największe modele „w kilka minut" *(dane projektu)*; konfiguracja bazowa `nbits=4, group_size=64` (≈ 4,5 bpw przy skali i zerze fp16 *(moje wyliczenie)*).
  Repozytorium przeniosło się do `dropbox/hqq` (960 gwiazdek, ostatnia zmiana 2026-02-26). W mistral.rs jako `HQQ4/HQQ8`.
* **EXL2** (turboderp; pochodna GPTQ, mieszane bitrate'y na warstwę 2–8 bpw) i **EXL3** (ExLlamaV3: „uproszczony wariant QTIP", kwantyzacja kratowa/trellis, arXiv 2406.11235, NeurIPS 2024): ułamkowe bpw 2–8, TP/EP, ciągłe batchowanie, **tylko CUDA** (README nie wspomina ROCm).
  README ExLlamaV2 mówi, że rozwój przeniesiono do V3, choć API GitHuba nie pokazuje archiwizacji (ostatnia zmiana 2026-03-04) — sprzeczność, traktuj V2 jako dziedzictwo. Porównań jakości EXL3 z GGUF/AWQ przy tym samym bpw **nie zebrałem**.

### 6.7 MLX: afiniczna kwantyzacja grupowa i jej odmiany

Rdzeń MLX (`mlx/ops.cpp`, linie ok. 4827–4852): `quantize(w, group_size=None, bits=None, mode='affine')` z trybami `affine`, `mxfp4`, `mxfp8`, `nvfp4` i domyślnymi rozmiarami grup **64 / 32 / 32 / 16**.
Tryb afiniczny trzyma **skalę i bias** na grupę, więc 4 bity, grupa 64, skala i bias fp16 → 4 + 32/64 = **4,5 bpw** *(moje wyliczenie; zakłada 16-bitowe skale)*.

`mlx_lm.convert` (plik `mlx_lm/convert.py`) przyjmuje: `--hf-path`, `--mlx-path`, `-q/--quantize`, `--q-group-size`, `--q-bits`, `--q-mode`, `--quant-predicate`, `--dtype`, `--upload-repo`, `-d/--dequantize`.
Przepisy `mixed_2_6`, `mixed_3_4`, `mixed_3_6`, `mixed_4_6` przypisują warstwom `low_bits` lub 6 bitów, „z podobnymi wyborami jak np. Q4_K_M w llama.cpp" (komentarz w kodzie) — to ta sama myśl co sekcja 3.2.
Poza tym w `mlx_lm/quant/` są metody uczone: **DWQ** (destylacja: dostraja skale i biasy względem niekwantyzowanego nauczyciela), **AWQ**, **GPTQ** i **kwantyzacja dynamiczna** (czułość per warstwa → mieszane bity; dokument `LEARNED_QUANTS.md`).
Kwantyzowany **KV** (`--kv-bits`, `QuantizedKVCache`) wyłącza w `mlx_lm.server` batchowanie (dokument SERVER.md). Rozdział [07](07-APPLE-MLX-OMLX-I-DS4.md) opisuje resztę.

### 6.8 oQ z oMLX

oMLX (`omlx/oq.py`, 11 295 linii) ma własny kwantyzator mieszanej precyzji, który — jak sam mówi dokument `oQ_Quantization.md` — łączy „strategię pozycji warstw z K-quantów GGUF, selektywne niekwantyzowanie z Unsloth Dynamic 2.0 i optymalne w sensie MSE obcinanie z BnB".
Poziomy oQ2, 2.5, 2.7, 3, 3.5, 4, 5, 6, 8; w przybliżeniu bpw wraz ze skalami dla grupy 64: oQ4 ≈ 4,6–4,7, oQ3 ≈ 3,5–3,7, oQ2 ≈ 2,8–3,0, oQ8 ≈ 8,5.
Procedura: strumieniowo czyta tensory → **mierzy czułość każdej warstwy** na wbudowanej kalibracji (600 próbek wielojęzycznych/kod/narzędzia) → przydziela dodatkowe bity tensorom wrażliwym w ramach budżetu rozmiaru →
w wariancie „e" (*enhanced*, np. `oQ4e`) zbiera imatrix (ok. 2700 próbek; dla MoE próbkuje, dopóki każdy ekspert nie ma dość tokenów) i zaokrągla grupy, szukając skali/przesunięcia o minimalnym błędzie **ważonym ważnością**. Wynik: standardowy safetensors MLX.
Zabezpieczenia: osadzenia i głowica 8-bitowe, routery MoE w pełnej precyzji, normy niekwantyzowane. Jakość z dokumentacji projektu *(dane projektu, zestaw 1900 pytań MMLU/Winogrande/MBPP/GSM8K)*:
Qwen3.5-9B oryginał 76,53, oQ4e 77,05 (5,6 GB), oQ3e 73,79 (4,6 GB); Qwen3.6-35B-A3B oryginał 82,68, oQ4e 83,05 (20 GB), oQ3e 82,68 (16 GB). Zwróć uwagę: **to wyniki autora**, na jego zestawie, bez niezależnego powtórzenia.
Sam pomysł — „zmierz czułość, potem wydaj budżet bitów" — to dokładnie to, co w świecie llama.cpp robisz przez imatrix + `--tensor-type`.

### 6.9 Układ kwantyzacji w ds4 (DwarfStar)

ds4 **nie wprowadza nowego formatu** — używa typów GGML, ale w **asymetrycznym układzie** (`docs/MODELS.md`): eksperci routowani są celem kompresji — `IQ2_XXS` dla gate/up i `Q2_K` dla down (z imatrix) — a „projekcje Q8, eksperci dzieleni i wyjście, plus tensory F16/F32" zostają w wysokiej precyzji.
Są też warianty Q4_K i **natywne MXFP4** dla ekspertów DeepSeek (zachowują oryginalne FP4 DeepSeeka bez ponownej kwantyzacji).

**Sprawdziłem, czy ten opis zgadza się z rozmiarem pliku** *(moje wyliczenie)*: eksperci 277,0 mld parametrów, z czego 2/3 (gate, up) po 2,0625 bpw i 1/3 (down) po 2,625 bpw → średnio 2,25 bpw → 277,0·10⁹ · 2,25 / 8 = **77,9 GB**.
Reszta, ok. 7,0 mld parametrów w Q8_0 (8,5 bpw) → **7,4 GB**. Razem **85,3 GB = 79,5 GiB**. Notatki podają dla pliku „ok. 81 GiB" *(dane projektu)* — rozbieżność 2 %, więc układ jest taki, jak opisano (reszta: tensory F16/F32, narzut). To jednocześnie
sprawdzian podziału „277 + 7 mld" użytego w tym rozdziale. Średnio wychodzi 2,45 bpw (81 GiB · 8 / 284 mld).

Dygresja, która przyda się w sekcji 13: ds4 na M5 Max osiąga 39,35 tok/s przy średnich 2,45 bpw, podczas gdy czysty wzór „przepustowość / (aktywne · bpw/8)" dałby ok. 154 — bo **tensory gęste (uwaga, eksperci dzieleni, wyjście) są w Q8/F16 i czytane przy każdym tokenie**.

---

## 7. Unsloth Dynamic (`UD-`) i plik referencyjny

### 7.1 Czym jest, a czym nie jest, Unsloth

`unslothai/unsloth` to przede wszystkim **biblioteka do dostrajania** (własne jądra Triton) plus od 2026 aplikacja „Studio", która **opakowuje llama.cpp** (opcjonalnie vLLM/SGLang) — i, co najważniejsze dla ciebie, **wydawca modeli**:
kwanty „Dynamic GGUF" to artefakty, które większość użytkowników lokalnych modeli faktycznie pobiera. Gdy Studio uruchamia GGUF, **to jest llama.cpp** — nie ma sensu porównywać „Unsloth kontra llama.cpp" jako silników.
(Pełniej o tym w rozdziale [05](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md).) Stan na 2026-10-19 (GitHub API): 78 273 gwiazdek, wydanie `v0.1.909-beta` co 2–4 dni; licencja dwoista (rdzeń Apache-2.0, część opcjonalna z UI Studio — AGPL-3.0).

### 7.2 Co znaczy `UD-`

**`UD-` = Unsloth Dynamic** (dokumentacja: `unsloth.ai/docs/basics/unsloth-dynamic-2.0-ggufs`). Nazwy typu `UD-IQ3_XXS`, `UD-Q4_K_XL`, `UD-Q2_K_XL` to etykiety Unslotha. Przyrostki `_XL` są **jego** — llama.cpp nie ma typu `Q4_K_XL`
(w `include/llama.h` są `IQ3_XS=22`, `IQ3_XXS=23`, bez XL). Nagłówek GGUF zachowuje jednak najbliższy standardowy ftyp w `general.file_type` (23 = `MOSTLY_IQ3_XXS`, `llama.h:142`), choć mieszanka tensorów jest własna.

Metoda według dokumentacji *(dane firmy)*: Dynamic 2.0 „wybiórczo i znacznie mądrzej kwantyzuje warstwy… zamiast modyfikować tylko wybrane warstwy, dynamicznie dostosowujemy typ kwantyzacji **każdej możliwej warstwy**"; schematy są specyficzne dla modelu
(MoE i gęste); kalibracja >1,5 mln tokenów „ręcznie dobranych i oczyszczonych", a nie zbiór ewaluacyjny; to **kwantyzacja po treningu z imatrix** — „NIE używamy QAT ani QAD"; zalecaną miarą jest KL divergence.
Wersja v3.0 (modele do Qwen3.8): „znacznie lepszy zbiór kalibracyjny… agentowe kodowanie, czat, wielojęzyczność", opublikowany plik imatrix, twierdzenie „>10 % lepsza trafność top-1 przy tym samym rozmiarze niż każdy inny dostawca" dla Qwen3.8-27B *(dane firmy)*.
Liczby z dokumentacji, które autor notatek zobaczył tylko w streszczeniu narzędzia (Gemma 3 27B: MMLU 71,47 % dla Dynamic 4-bit kontra 70,64 % dla QAT Google przy 17,2 GB; ok. 7,5 % mniej KLD dla Q2_K_XL), **przed zacytowaniem sprawdź na stronie**.

**Czego nie wiadomo:** *jak* obliczany jest wybór typu dla każdej warstwy (analiza czułości? heurystyka?) — opisu nie znalazłem na dostępnych stronach, a narzędzie receptur **nie jest w publicznym repozytorium `unsloth`**. Czy receptury powstają zwykłym
`llama-quantize --tensor-type …`, czy prywatną wersją narzędzia — *nie ustaliłem*. Zdanie „dobór warstw przez analizę czułości" jest zatem *niezweryfikowane*.

### 7.3 Co faktycznie jest w UD-IQ3_XXS: odczyt nagłówka

Przeczytałem nagłówek GGUF v3 pliku `unsloth/Qwen3-Coder-30B-A3B-Instruct-UD-IQ3_XXS.gguf` (rozmiar 12 848 766 112 B, pobrałem pierwsze 40 MB zakresowo; w repozytorium leży też `imatrix_unsloth.gguf_file`, 122 MB).
Model: architektura `qwen3moe`, 48 bloków, 128 ekspertów (8 aktywnych), `general.quantized_by = Unsloth`, `file_type = 23`, **30 532 122 624 parametrów**. Rozkład typów tensorów:

| typ | bpw bloku | parametry | udział w parametrach | udział w bajtach |
|---|---:|---:|---:|---:|
| IQ3_XXS | 3,0625 | 18,32 mld | 60,0 % | 54,6 % |
| IQ3_S | 3,4375 | 8,25 mld | 27,0 % | 27,6 % |
| IQ4_XS | 4,25 | 3,16 mld | 10,4 % | 13,1 % |
| Q6_K | 6,5625 | 0,395 mld | 1,3 % | 2,5 % |
| Q4_K (`token_embd`) | 4,5 | 0,311 mld | 1,0 % | 1,4 % |
| Q5_K | 5,5 | 0,078 mld | 0,25 % | 0,4 % |
| F32 (normy, router `ffn_gate_inp`, normy q/k) | 32 | 0,013 mld | 0,04 % | 0,4 % |

**Siedem różnych typów w pliku o nazwie „IQ3_XXS".** Średnie bpw — policzyłem na dwa sposoby:

```
z bitów typów:   (18,32·3,0625 + 8,25·3,4375 + 3,16·4,25 + 0,395·6,5625
                  + 0,311·4,5 + 0,078·5,5 + 0,013·32) / 30,527
               = 102,73 Gbit / 30,527 mld  = 3,365 bpw        (moje wyliczenie)
z rozmiaru pliku: 12 848 766 112 · 8 / 30 532 122 624        = 3,367 bpw
```

Zgodność do 0,05 %, więc rozkład z nagłówka jest kompletny. Zauważ: **nazwa „IQ3_XXS" to 3,06 bpw, a cały plik ma 3,37** — dokładnie ta lekcja, którą dał ci Q2_K z sekcji 5.4.

Przydział na tensory (z nagłówka; „warstwa" = numer bloku 0–47):

* `ffn_gate_exps` / `ffn_up_exps`: **IQ3_XXS** w warstwach 0, 3–31, 34–35; **IQ3_S** w 1–2, 32–33, 36–47;
* `ffn_down_exps`: IQ3_XXS w większości środkowych; **IQ4_XS** w warstwach 1–3, 21, 28, 41–47; IQ3_S w 26, 32–33, 35–40;
* `attn_q/k/v`: IQ4_XS, poza warstwami 1–2 i 45–47 (Q5_K);
* `attn_output`: IQ4_XS, z Q6_K w warstwach 0, 5, 7, 33, 37–38, 40, 44, 46–47 i Q5_K w 1–2, 45;
* `output.weight`: Q6_K; `token_embd`: Q4_K.

Standardowa reguła llama.cpp dla IQ3_XXS (`src/llama-quant.cpp`, linie ok. 465–735) dałaby dla `attn_v` tego modelu (GQA-8) Q4_K (linia 601) — w pliku jest co innego (IQ4_XS/Q5_K), a nieregularne warstwy (21, 28, 4–5 vs 1–3)
nie pasują do standardowego wzorca. Nie uruchamiałem zwykłego `llama-quantize` na tym modelu, żeby porównać, więc „odbiega od standardowej receptury" czytam z kodu i zrzutu (*przyczynowość: niezweryfikowane*).

**Wniosek o typie pliku referencyjnego:** to plik **~3,4 bpw o mieszanej precyzji**, w którym uwaga, osadzenia, wyjście, eksperci pierwszych i ostatnich warstw oraz niektóre warstwy środkowe dostają 4–6 bitów,
a ok. 87 % parametrów (eksperci) siedzi na ok. 3,1–3,4 bita. Imatrix był użyty (plik opublikowany). To dla **modelu Qwen3-Coder-30B**; dla DeepSeeka układ nie jest mi znany (sekcja 7.4).

> **Sprawdź sam 3 — rozkład typów w pliku referencyjnym.** W środowisku, gdzie masz `gguf-py` (katalog narzędzi z `../przyspieszanie-generowania/narzedzia/gguf-inspect.py` używa `GGUFReader`), policz typy tensorów
> *(nie uruchamiałem; pola `tensor_type`, `n_elements`, `n_bytes` istnieją w `ReaderTensor` w `gguf-py/gguf/gguf_reader.py`)*:
>
> ```python
> from collections import Counter
> from gguf import GGUFReader
> import glob
> files = sorted(glob.glob("…/DeepSeek-V4-Flash-0731-UD-IQ3_XXS-0000*-of-00004.gguf"))
> par, byt = Counter(), Counter()
> for f in files:
>     for t in GGUFReader(f).tensors:
>         par[t.tensor_type.name] += t.n_elements
>         byt[t.tensor_type.name] += t.n_bytes
> for k in par: print(k, par[k]/1e9, "mld par.", byt[k]/1e9, "GB")
> print("razem", sum(byt.values())*8/sum(par.values()), "bpw")
> ```
>
> Czyta same nagłówki (jak `gguf-inspect.py`), więc działa w sekundy i nie dotyka GPU. To rozstrzygnie wątpliwość z sekcji 7.4 (GB czy GiB) i pokaże prawdziwą mieszankę.

### 7.4 Model referencyjny: DeepSeek-V4-Flash UD-IQ3_XXS — arytmetyka *(moje wyliczenie)*

Dane wejściowe: cztery części pliku mają razem **104 207 848 508 bajtów** *(zmierzone: `du -sb` na katalogu z plikami `…-0000N-of-00004.gguf`)* — to **104,2 GB dziesiętnych** (≈ 97,05 GiB) — dla **284 mld** parametrów (karta modelu; liczba zaokrąglona).

**(a) Średnia z rozmiaru pliku**

```
104,2·10⁹ B · 8 / 284·10⁹ = 833,6 / 284 = 2,935 bpw
```

Uwaga o jednostkach, bo łatwo się pomylić o 0,22 bpw: strona Hugging Face i `du -sb` pokazują bajty/GB dziesiętne, `ls -lh` i `du -h` — GiB (97,05 GiB). Liczby w tym podręczniku to GB dziesiętne.

**(b) Porównanie z modelem strukturalnym.** Z konfiguracji DeepSeek-V4-Flash (43 warstwy, 256 ekspertów routowanych + 1 dzielony, 6 routowanych na token, `moe_intermediate_size` 2048, hidden 4096) wychodzi:
eksperci = 256 · 43 · (3 · 4096 · 2048) = **277,0 mld** parametrów, reszta (uwaga, eksperci dzieleni, osadzenia, wyjście, routery) ≈ **7,0 mld**; aktywnych na token 7,0 + 6/256 · 277,0 = **13,5 mld**, co zgadza się z deklarowanymi 13B.

| scenariusz | liczenie | rozmiar |
|---|---|---:|
| wszyscy eksperci w czystym IQ3_XXS (3,0625 bpw) | 277,0·10⁹ · 3,0625 / 8 | 106,0 GB |
| + reszta w Q8_0 | 7,0·10⁹ · 8,5 / 8 | + 7,4 GB → **113,5 GB = 105,7 GiB** |
| + reszta w ok. 5 bpw (jak uwaga w pliku Qwen3-Coder: IQ4_XS–Q6_K) | 7,0·10⁹ · 5 / 8 | + 4,4 GB → **110,4 GB = 102,8 GiB** |

Wynik: plik (104,2 GB) jest o ok. 2–9 GB (2–8 %) **mniejszy** niż każdy z powyższych wariantów, a nawet niż „czysty IQ3_XXS" dla samych ekspertów (106,0 GB). Przy założeniu, że struktura z (b) jest poprawna,
oznacza to, że **część ekspertów leży w typach 2-bitowych** (np. IQ2_XS/IQ2_S), a część gęsta nie jest cała w 8 bitach. To zgodne z ideą Dynamic quants (zmienna liczba bitów na tensor), ale **konkretny skład typów w tym pliku nie jest tu zweryfikowany** — rozstrzygnie to odczyt nagłówka (ramka *Sprawdź sam 3* wyżej; plik Qwena z notatek ma inną mieszankę i nie można jej przenosić 1:1).

**(c) Ile bajtów na token** — tu ujawnia się coś, czego prosty wzór z sekcji 1.2 nie widzi. Na token karta czyta **całe tensory gęste** (ok. 7,0 mld parametrów, zawsze) i **6 z 256 ekspertów w każdej warstwie** (6/256 · 277,0 = 6,49 mld):

```
bajty/token = 7,0·10⁹ · b_gęste/8  +  6,49·10⁹ · b_eksperci/8

b_gęste = 5,   b_eksperci = 3,06 :   4,38 + 2,48 =  6,9 GB
b_gęste = 8,5, b_eksperci = 3,06 :   7,44 + 2,48 =  9,9 GB
(prosty wzór „13,5 mld · 2,94 / 8"                 =  4,96 GB)
```

Czyli **większość ruchu pamięci na token to część gęsta**, nie eksperci. To tłumaczy, dlaczego zmierzone 49 tok/s leży daleko poniżej sufitu z sekcji 1.2, i — co ważniejsze — **co wynika dla wyboru większego kwantu** (sekcja 13):
bity ekspertów kosztują dużo pojemności, ale mało przepustowości.

### 7.5 Pozycja kosztowo-jakościowa

Dane llama.cpp (sekcja 5): IQ3_XXS leży między Q2_K a Q4_K rozmiarem; PR #5196 pokazuje, że bije Q3_K_XS przy mniejszym rozmiarze na tych samych modelach, a w tabeli Llama-3-8B ma KLD 0,184 — 6,5× więcej niż Q4_K_M.
**Żadna tabela in-tree nie mierzy IQ3_XXS względem FP16 na nowoczesnym MoE.** Czy 3,4 bpw to „dość dobrze" dla produkcyjnego modelu agentowego, trzeba zmierzyć na swoich zadaniach — i do tego zmierzę w sekcji 9.

---

## 8. Tabela zbiorcza: format × silnik × sprzęt × zastosowanie

Legenda kolumn „sprzęt": ✔ = jądro istnieje (widoczne w kodzie lub udokumentowane przez projekt); ~ = istnieje, ale pokrycie nieaudytowane; ✘ = brak (zweryfikowane); ? = *nie ustaliłem*.
Kolumna „gfx1201" dotyczy **kart referencyjnych (R9700, ROCm)**.

### 8.1 Rodziny GGUF (jądra w llama.cpp i pochodnych)

| format | bpw bloku | kto ładuje | CPU | CUDA | gfx1201 / ROCm | Metal | typowe użycie |
|---|---|---|---|---|---|---|---|
| Q4_0/Q4_1/Q5_x/Q8_0 | 4,5 / 5,0 / 5,5–6,0 / 8,5 | llama.cpp, ik_llama.cpp, Ollama, LM Studio, llamafile, KoboldCpp, mistral.rs (też ISQ), KTransformers (backend LLAMAFILE) | ~ | ~ | ~ (backend `hip` jest w drzewie) | ~ | zgodność wsteczna; Q8_0 jako „prawie bezstratne" |
| K-quanty Q2_K…Q6_K | 2,625…6,5625 | j.w. | ~ | ~ | ~ (typy Q4_K/Q5_K/Q6_K występują w pliku UD Qwena; w referencyjnym DeepSeeku — sekcja 7.4) | ~ | **domyślny wybór** przy 4–6 bitach (Q4_K_M, Q5_K_M) |
| i-quanty IQ1…IQ4 | 1,56…4,5 | llama.cpp + forki; mistral.rs tylko przez ścieżkę GGUF | ~ (wolniejsze odkodowanie) | ~ | ~ (IQ3_XXS jest w nazwie pliku referencyjnego, który działa w produkcji) | ~ | niskie bity (2–3,5); IQ2_XXS/XS tylko z imatrix |
| TQ1_0/TQ2_0, Q1_0, Q2_0 | 1,69 / 2,06 / 1,125 / 2,25 | llama.cpp | ? | ? | ? | ? | trójkowe/BitNet; nowe typy, *nie audytowane* |
| MXFP4 / NVFP4 (w GGUF) | 4,25 / 4,5 | llama.cpp (CPU + CUDA; PR #23572 do kwantyzacji NVFP4 na CUDA nadal otwarty), KTransformers (CPU) | ~ (wg notatek) | ~ (wg notatek) | ? (FP4 jako format; **szybkości FP4 nie oczekuj** *(niezweryfikowane)*) | ? | modele „natywnie FP4" (gpt-oss, eksperci DeepSeek) |
| **UD-** (mieszanki Unsloth) | per plik: np. 3,37 | wszystko, co czyta GGUF | = jądra użytych typów | = | = (typy jak wyżej) | = | gotowe „najlepsze" przepisy + imatrix; produkcyjny plik konfiguracji referencyjnej |
| IQK/trellis z ik_llama | różne | **tylko ik_llama.cpp** | ✔ | ✔ | ? (nie udokumentowany cel) | ~ | CPU/hybryda dla MoE; uzależnienie od forka |
| ds4 (typy GGML w asymetrycznym układzie) | ok. 2,45 średnio | tylko ds4 | ~ | ✔ | w `main` cel to gfx1151, **nie gfx1201** (3 otwarte PR od osób trzecich) | ✔ | DeepSeek V4/GLM/Qwen3.8 na Macach 96–128 GB |

### 8.2 Rodziny „serwerowe" i Apple

| format | bpw (zwykle) | kto ładuje | kalibracja | CUDA | gfx1201 / ROCm | Metal | typowe użycie |
|---|---|---|---|---|---|---|---|
| **GPTQ** (safetensors) | ≈ 4,16 (g128) | vLLM (`gptq`, `gptq_marlin`), SGLang, TRT-LLM, ExLlama, mistral.rs; llama.cpp tylko odkwantyzuje | tak (Hesjan) | ✔ (Marlin, Ampere+) | vLLM: **kod ma jądro `RDNAHybridW4A16` dla gfx11/12**, a tabela w dokumentacji mówi ❌ — *sprzeczność, testuj* | ✘ | serwery, 4-bitowe wagi |
| **AWQ** | ≈ 4,16 (g128) | vLLM (`awq`, `awq_marlin`), SGLang, TRT-LLM, MLC; **nie llama.cpp** | tak (statystyki aktywacji) | ✔ | jak GPTQ (to samo jądro W4A16) | ✘ | j.w.; martwe AutoAWQ → używaj llm-compressor |
| **SmoothQuant W8A8** | 8 | TRT-LLM, vLLM (`w8a8_int8`), SGLang | tak | ~ (INT8 TC) | ? | ✘ | przepustowość serwera w centrach danych |
| **FP8** E4M3/E5M2 | ≈ 8 | vLLM, SGLang, TRT-LLM, KTransformers, mistral.rs, MLC; llama.cpp tylko czyta i konwertuje | brak/lekka | ✔ (Hopper/Ada/Blackwell) | vLLM: **dopuszczony w kodzie na gfx12x**, wydajność niezmierzona | ✘ | wagi + KV w serwerach; natywna „reszta" DeepSeek |
| **MXFP4 / NVFP4** (safetensors) | 4,25 / 4,5 | vLLM (`mxfp4`, `modelopt_fp4`), SGLang, TRT-LLM, MLX, KT | brak (checkpoint natywny) / PTQ ModelOpt | ~ (natywnie dopiero Blackwell) | vLLM: `mxfp4` na liście ROCm; *jądra na gfx1201: nie ustaliłem* | ✔ (MLX) | modele wydawane w FP4 |
| **bitsandbytes NF4** | 4,5 / 4,127 | transformers, PEFT, Unsloth, vLLM, SGLang, mistral.rs; nie llama.cpp/MLX | brak | ✔ | `bitsandbytes` **nie ma** na liście kwantyzacji ROCm w vLLM (`rocm.py`) | ✘ | **trening** (QLoRA), nie szybkie wnioskowanie |
| **HQQ** | ≈ 4,5 (g64) | transformers, mistral.rs, torchao | **brak** (minuty) | ✔ | ? | ✘ | szybka kwantyzacja bez kalibracji |
| **EXL2 / EXL3** | 2–8 ułamkowe | ExLlamaV2/V3, TabbyAPI | tak (Hesjan / QTIP) | ✔ | ✘ (README nie wspomina ROCm) | ✘ | maksymalna jakość/bit na NVIDIA |
| **MLX afiniczny / mxfp4 / nvfp4** | 4,5 (4-bit g64) | MLX, mlx-lm, oMLX, LM Studio (MLX), mistral.rs (AFQ) | brak (+ DWQ/AWQ/GPTQ opcjonalnie) | ✔ (backend CUDA MLX istnieje) | ✘ (MLX: Metal, CUDA, CPU) | ✔ | **Mac** |
| **oQ** (oMLX) | oQ4 ≈ 4,6 | tylko jako zwykły MLX safetensors (każdy silnik MLX) | tak (czułość + imatrix) | – | ✘ | ✔ | Mac, mieszana precyzja na budżet |
| **MLC group quant** `q4f16_1` | ≈ 4 + skale | tylko MLC/WebLLM | brak | kompilacja TVM | ? | ✔ | przeglądarka/telefon |

**Czego tabela nie mówi (uczciwie):**

* Dla llama.cpp zweryfikowałem **istnienie katalogów backendów** (`cuda`, `hip`, `metal`, `vulkan`, `sycl`, `opencl`, `cann`, `hexagon`, `openvino`, `webgpu`), a nie pokrycie każdego typu na każdym z nich. Jedyny dowód „w praktyce" to to, że **plik referencyjny UD-IQ3_XXS działa na gfx1201 w produkcji** (jakie dokładnie typy zawiera — sekcja 7.4).
* Dla vLLM na gfx1201 kod i dokumentacja się nie zgadzają (AWQ/GPTQ: dokumentacja ❌, kod ma jądra RDNA); zaleciłem w notatkach „przetestuj, zanim zaufasz". SGLang: gfx1201 **nie jest celem** (skrypt `setup_rocm.py` akceptuje tylko `gfx942`, `gfx950`, `gfx1250`;
  uwaga: gfx1250 to nie RDNA4). TensorRT-LLM: tylko NVIDIA. mistral.rs: **brak backendu ROCm i Vulkan** (CUDA, Metal, CPU). Szczegóły w rozdziale [06](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md).
* **Same GGUF** w vLLM/SGLang: istnieją ładowarki, ale vLLM na liście kwantyzacji ROCm nie ma `gguf`, a SGLang wymienia GGUF z jądrami **tylko CUDA** (Ascend przez odkwantyzację na CPU). Dokumentacja wtyczki GGUF dla vLLM mówi o „wysoce eksperymentalnej i niedopracowanej" ścieżce.

> **Sprawdź sam 4 — lista kwantyzacji vLLM na ROCm.** W klonie vLLM: `vllm/platforms/rocm.py`, pole `supported_quantization` (linie ok. 625–649): znajdziesz `awq`, `gptq`, `fp8`, `compressed-tensors`, `quark`, `mxfp4`… i **brak `gguf` oraz `bitsandbytes`**.
> Obok sprawdź `vllm/model_executor/kernels/linear/mixed_precision/rdna_hybrid_w4a16.py` (651 linii) — to jądro W4A16 dla gfx11/gfx12, które kłóci się z tabelą „AWQ ❌" w `docs/features/quantization/README.md`.

---

## 9. Jakość modelu referencyjnego: czego nie wiemy i jak to zmierzyć

### 9.1 Co zmieniłeś i co o tym wiadomo

W katalogu o przyspieszaniu ([`../przyspieszanie-generowania/README.md`](../przyspieszanie-generowania/README.md)) przeszedłeś z 23,5 do ok. 50 tok/s dwiema zmianami: **speculative decoding** (draft DSpark, 3 tokeny) i **podział tensorowy** (`--split-mode tensor`) na nowszym llama.cpp.
Wagi i ich kwantyzacja się **nie zmieniły** — to ten sam plik UD-IQ3_XXS. Ta decyzja ma więc dwa osobne pytania o jakość, i warto ich nie mieszać:

1. **Czy przyspieszenie zmieniło jakość?** Speculative decoding z założenia nie zmienia rozkładu odpowiedzi (duży model zatwierdza każdy token). Podział tensorowy zmienia **kolejność sumowania zmiennoprzecinkowego** — przy temperaturze 0 odpowiedzi nie są identyczne znak w znak (0 z 4 identycznych; z podziałem warstwami i draftem 2 z 4).
   To szum numeryczny, ale *czy* jest nieszkodliwy — słowami dziennika wdrożenia: „nie wiem".
2. **Jak dobry jest sam kwant** UD-IQ3_XXS na DeepSeek-V4-Flash względem lepszego kwantu tego samego modelu? Tego **nie mierzył nikt**, na pewno nie ja.

### 9.2 Czego nie wiemy (uczciwie)

* **Jakości po przyspieszeniu nie zmierzyłeś.** Benchmark jakości (zestaw „hard", 20 zadań PL/EN, k = 3, 120 próbek; ten model miał 10 października wynik **PL 92 / EN 93**) uruchomiłeś i **przerwałeś po 11 próbkach**, więc nie ma żadnych publikowalnych danych.
  11 próbek to za mało na jakikolwiek wniosek: przy trafności ok. 92 % błąd standardowy wynosi sqrt(0,92 · 0,08 / 11) ≈ **8 punktów procentowych**; nawet pełne 120 próbek daje ≈ **2,5 pp** (*moje wyliczenie*, zakładając niezależność — a próbki są skorelowane, bo to tylko 20 różnych zadań powtórzonych po 3 razy,
  więc realny błąd jest większy). Różnic rzędu kilku punktów takim zestawem nie wykryjesz.
* **Nie mamy żadnej publicznej liczby jakości UD-IQ3_XXS na DeepSeek-V4.** Dokumentacja Unslotha (dane firmy) podaje wyniki dla Gemma 3 27B i Qwen3.8-27B, nie dla tego modelu; tabele llama.cpp mierzą starsze modele gęste (Llama).
  Z sekcji 5.2 wiesz, że ten sam typ szkodzi nowszym modelom bardziej, więc tabele z Llamy mogą **zaniżać** stratę.
* **Nie wiemy, jak wygląda mieszanka typów w pliku referencyjnym** (sekcja 7.4) — więc nie możemy nawet szacować strat z tabeli per typ.
* **Perplexity i KLD nie pokażą degradacji długiego horyzontu narzędzi** (wieloetapowe wywołania, długi kontekst), a to jest faktyczny użytek w konfiguracji referencyjnej *(niezweryfikowane — wniosek z dokumentacji Unslotha i podstaw)*.
  Model może mieć świetne KLD na wikitext i gubić się w trzecim wywołaniu narzędzia.
* **Model był natywnie FP4 (eksperci).** Droga „FP4 → (BF16?) → IQ3_XXS" to ponowna kwantyzacja z już 4-bitowego źródła; jak Unsloth ją przeprowadził, *nie ustaliłem*.

### 9.3 Metoda: trzy pytania, trzy pomiary

Poniżej polecenia **z dokumentacji i kodu w drzewie `0ce8cd1`**; *żadnego nie uruchamiałem*. Pamiętaj, że GPU są produkcyjne — pomiary robisz tam, gdzie możesz, kiedy możesz.

**Pomiar A — czy przyspieszenie coś zmieniło? (ten sam plik, dwie konfiguracje)**
Tanie i bezpośrednio odpowiada na pytanie 1. Nagraj logity w starej konfiguracji (podział warstwami; draftu w tym pomiarze nie włączasz — jest bezstratny w rozkładzie), potem porównaj z konfiguracją tensorową:

```bash
# zbiór testowy Wikitext-2 (skrypt w drzewie llama.cpp, wg README narzędzia perplexity;
# nazwa pliku wynikowego `wiki.test.raw` poniżej jest moim założeniem)
scripts/get-wikitext-2.sh

# 1) odniesienie: podział warstwami, zapis logitów
llama-perplexity -m MODEL.gguf -f wiki.test.raw -fa on -ngl 999 --split-mode layer \
    --kl-divergence-base logits-layer.kld

# 2) porównanie: podział tensorowy względem tego pliku
llama-perplexity -m MODEL.gguf -f wiki.test.raw -fa on -ngl 999 --split-mode tensor \
    --kl-divergence-base logits-layer.kld --kl-divergence
```

(Składnia `--kl-divergence-base` / `--kl-divergence` — z README narzędzia. Że tryb tensorowy działa z `llama-perplexity` i że wymaga `-fa on` oraz niekwantyzowanego KV — z `docs/multi-gpu.md`; **to, że to konkretnie działa z tym modelem i tą wersją, nie jest sprawdzone**.)
*Jak czytać wynik:* skalą odniesienia jest tabela z sekcji 5.1 — szum samego zapisu logitów w 16 bitach to KLD ≈ 0,0006, a Q8_0 ≈ 0,0014. Jeśli KLD między konfiguracjami jest rzędu 10⁻⁴–10⁻³, to szum numeryczny; jeśli zbliża się do 10⁻², dzieje się coś więcej.
*(To moja propozycja progu, nie wartość z dokumentacji.)* **Uwaga na miejsce:** plik logitów jest duży (README: 37 GiB dla LLaMA 3 na Wikitext-2; słownik DeepSeeka ma 129 280 tokenów, więc spodziewaj się rzędu dziesiątek GiB — *niezweryfikowane*).
Można skrócić tekst testowy.

**Pomiar B — jak bardzo kwant ustępuje lepszemu? (to samo pytanie, co tabele w sekcji 5, ale na modelu referencyjnym)**
Potrzebujesz *referencji*. BF16 nie wchodzi w grę (568 GB). Trzy realne opcje:

1. **Wyższy kwant tego samego modelu** (z rodziny UD, jeśli istnieje i da się uruchomić — choćby wolno, z odciążeniem do RAM: KLD na kilkudziesięciu tysiącach tokenów nie wymaga szybkości). Wtedy te same dwa polecenia co wyżej: logity referencji → `--kl-divergence` dla UD-IQ3_XXS.
   Wynik mówi, ile traci się względem *tego* kwantu, nie względem FP16 — czyli to jest dolne ograniczenie straty.
2. **Model zastępczy (proxy) o tej samej rodzinie kwantyzacji**: np. Qwen3-Coder-30B-A3B, dla którego znasz mieszankę UD-IQ3_XXS (sekcja 7.3) i którego BF16 (≈ 61 GB *(moje wyliczenie: 30,5 mld · 2 B)*) zmieści się w 128 GB pamięci kart — porównujesz UD-IQ3_XXS z Q8_0/BF16 w KLD.
   To powie, ile **kosztuje ta klasa receptury na MoE**, nie ile kosztuje na DeepSeeku.
3. **ds4 z natywnym MXFP4** (eksperci bez ponownej kwantyzacji; wersja „Vision Exp MXFP4" to 145 GiB, więc **nie mieści się** w 136,8 GB kart bez SSD) — tylko jako lektura pomysłu.

**Pomiar C — czy zadania działają? (najważniejszy dla agentów)**
Nie zastąpią go KLD ani PPL. Masz już narzędzie: `python3 -m qbench run --model deepseek-v4-flash-0731 --suite hard --k 3` (kilka godzin; nie zmieniaj konfiguracji `llama-swap` w trakcie — zwolni model). Porównaj z raportem z 10 października.
Dwie rady (*moje*, z rachunku błędu powyżej): zwiększ liczbę **różnych** zadań (nie tylko k), bo powtórzenia tego samego zadania niewiele mówią; i dołóż osobną miarę: **odsetek poprawnych wywołań narzędzi (poprawny JSON + właściwa funkcja)** na dużej próbce — to najczulsze na degradację
kwantyzacją i najbliższe twojemu zastosowaniu. Jeśli wynik pogorszy się względem 10 października, katalog o przyspieszaniu radzi przełączyć klientów na bliźniaczy wpis `-nospec` albo wrócić do podziału warstwami.

**Dlaczego nie wystarczy samo PPL:** według dokumentacji llama.cpp PPL nie jest porównywalna między modelami i bywa wyższa dla modeli dostrojonych mimo lepszych odpowiedzi; KLD względem referencji jest czulsze, ale nadal mierzy rozkład następnego tokenu na zwykłym tekście, a nie zadanie agentowe.
Dlatego trzy pomiary, a nie jeden.

---

## 10. Formaty plików

Do tej pory mówiłem o *zawartości* (jak zapisane są wagi). Teraz o *opakowaniu*: co jest w pliku obok wag i dlaczego to ważne dla narzędzi.

### 10.1 safetensors (Hugging Face)

Format „kontenera tensorów": plik zaczyna się od 8-bajtowej liczby (little-endian) z długością nagłówka, potem nagłówek JSON (nazwa tensora → typ, kształt, przesunięcia bajtowe), potem surowe bajty tensorów.
Dokumentacja HF mówi o celach: **bezpieczeństwo** (w przeciwieństwie do pickle nie wykonuje kodu), szybkość (**zero-copy**) i **częściowe ładowanie** (`get_slice`). Układ bajtów powyżej to dla mnie *niezweryfikowane szczegóły z pamięci* — dokumentację HF czytałem tylko w zakresie celów.

```
[ 8 B: długość nagłówka N ][ N B: JSON {"nazwa.tensora": {"dtype":..., "shape":[...], "data_offsets":[od,do]}, ...} ][ surowe bajty tensorów ]
```

Duże modele są dzielone: `model-00001-of-000NN.safetensors` + `model.safetensors.index.json` (mapa nazwa → plik; `mlx_lm/utils.py`). Używają go transformers, vLLM, SGLang i MLX.
**Kwantyzowane checkpointy (GPTQ/AWQ/FP8/NVFP4) to nadal safetensors** — z dodatkowymi tensorami (skale, zera) i polem `quantization_config` w `config.json`; w DeepSeek-V4 np. `expert_dtype: fp4` i dynamiczne FP8.
Czyli dla safetensors kwantyzacja jest **konwencją doklejoną z boku**, a nie częścią formatu.

### 10.2 GGUF — układ z adnotacjami

GGUF to **jeden plik, który wie wszystko o modelu**. Układ (`ggml/include/gguf.h`: `GGUF_MAGIC "GGUF"`, `GGUF_VERSION 3`, `GGUF_DEFAULT_ALIGNMENT 32`; `ggml/src/gguf.cpp`), little-endian:

```
┌─ NAGŁÓWEK ──────────────────────────────────────────────────────────────┐
│ "GGUF"                   4 B   magia                                   │
│ version                  u32   = 3                                     │
│ n_tensors                i64   ile tensorów w pliku (tu: tej części)
│ n_kv                     i64   ile par klucz-wartość metadanych        │
├─ METADANE (n_kv razy) ──────────────────────────────────────────────────┤
│ klucz: string (u64 długość + bajty, bez NUL)                           │
│ typ wartości: u8,i8,u16,i16,u32,i32,f32,bool,string,array,u64,i64,f64  │
│ wartość (tablice niosą typ elementu i liczbę u64)                      │
│   np. general.architecture, general.file_type (23 = MOSTLY_IQ3_XXS),   │
│       general.quantized_by, general.alignment (domyślnie 32),          │
│       <arch>.block_count, <arch>.attention.head_count_kv, <arch>.rope.*│
│       tokenizer.ggml.tokens, ….merges, tokenizer.chat_template        │
├─ TABLICA TENSORÓW (n_tensors razy) ─────────────────────────────────────┤
│ nazwa (np. blk.12.ffn_down_exps.weight, output.weight, token_embd…)    │
│ n_dims u32 │ ne[] (i64 na wymiar) │ typ ggml (Q4_K, IQ3_XXS, F32…) │ offset u64
├─ wypełnienie do general.alignment ──────────────────────────────────────┤
├─ BLOB DANYCH ────────────────────────────────────────────────────────────┤
│ tensory jeden za drugim, każdy wyrównany; offset liczony od początku bloku
└──────────────────────────────────────────────────────────────────────────┘
```

Co to daje i dlaczego **typ jest per tensor**: to w tablicy tensorów siedzi to, co pokazuje odczyt z sekcji 7.3 — *każdy tensor ma własny typ*. Mieszanka Unslotha to po prostu „inny typ w wierszu tablicy".
Metadane `<arch>.*` niosą hiperparametry architektury, a `tokenizer.*` — pełny tokenizator i szablon czatu. Dlatego `llama-server -m plik.gguf` nie potrzebuje niczego więcej.

**Wyrównanie i `mmap`.** Ponieważ dane są wyrównane i ciągłe, loader może zmapować plik w pamięci (`mmap`) i oddać wskaźniki prosto do backendów (`src/llama-model-loader.cpp`, linie ok. 560–691, sprawdzenie wyrównania w linii 691).
Efekty: niemal natychmiastowe ładowanie, współdzielenie cache stron między procesami, praca z modelami większymi niż RAM. W `include/llama.h` (linia ok. 207) są tryby ładowania AUTO, NONE, MMAP, MLOCK, MMAP_MLOCK i **DIRECT_IO** — konfiguracja referencyjna używa `--load-mode dio`;
jest też „tryb leniwy" (czytaj tylko te wiersze dużych tensorów, które architektura oznaczy, np. eksperci MoE; „lazy only for marked tensors larger than 4 GiB").

**Dzielenie.** Pliki >50 GB dzieli się narzędziem `gguf-split` na `…-00001-of-0000N.gguf` (model referencyjny: 4 części; konwerter ma też `--split-max-size` i `--split-max-tensors`). Draft DSpark to **osobny** plik GGUF (10,9 GB, 81 tensorów, architektura `dflash`),
bo publiczne GGUF-y DeepSeeka „wycinają" tensory MTP/NextN (sprawdziłeś: 43 bloki, zero tensorów `nextn`).

**Dlaczego GGUF wygrał lokalnie** *(rozumowanie z zweryfikowanych właściwości)*: (1) jeden samoopisujący się plik: wagi + architektura + tokenizator + szablon czatu + domyślne próbkowanie; (2) wyrównanie przyjazne `mmap`; (3) kwantyzacja jest **częścią formatu** (dziesiątki typów bloków), podczas gdy
w safetensors jest sidecarem; (4) rozszerzalne metadane — nowe architektury nie psują starych czytników; (5) cały ekosystem (Ollama, LM Studio, llama-swap, koboldcpp, llamafile, ds4) się na nim ustandaryzował; (6) każdy backend ggml (CPU/CUDA/HIP/Metal/Vulkan/SYCL) konsumuje te same bloki.
**Wady:** przywiązanie do „zoo" kwantów ggml; krok konwersji z HF; metadane i nazwy tensorów dla każdej architektury utrzymują programiści llama.cpp (nowa architektura = nowy plik w `src/models/` + kod w `convert_hf_to_gguf.py`).

### 10.3 MLX

MLX zapisuje tablice przez `mx.save_safetensors` — a modele mlx-lm to **katalogi**: `config.json`, pliki tokenizera i `model*.safetensors`; wagi kwantyzowane to spakowane liczby całkowite + skale i biasy per grupa (domyślnie grupa 64 — sekcja 6.7).
`mlx_lm/gguf.py` potrafi czytać/pisać GGUF (ograniczony czytnik — *szczegóły niezweryfikowane*). Czyli „format MLX" to w gruncie rzeczy **safetensors z konwencją kwantyzacji MLX**; nie jest to wymienny format między silnikami.

### 10.4 ONNX

Graf obliczeń + wagi w jednym kontenerze protobuf; używany przez ONNX Runtime, DirectML i ścieżki OpenVINO (Copilot+ NPU, Lemonade). **Nie badałem** szczegółów kwantyzacji w ONNX; tego formatu nie używa żaden silnik ze stosu referencyjnego.

### 10.5 TensorRT (i „plik silnika")

Plik „plan" TensorRT jest kompilowany dla **jednej architektury GPU**, wersji TensorRT i profilu kształtów. **TensorRT-LLM już go nie używa**: `trtllm-build`, `LLM(backend="tensorrt")` i skrypty `convert_checkpoint.py` zostały usunięte;
jedynym backendem jest PyTorch, a checkpointy HF ładują się wprost (`~/runtimes-src/TensorRT-LLM/docs/source/legacy/tensorrt-backend-removal.md`). Jeśli w jakimś tutorialu czytasz „TensorRT-LLM kompiluje plik silnika" — jest przestarzały.
Dla ciebie to wyłącznie wiedza poglądowa (TRT-LLM = tylko NVIDIA).

### 10.6 Zestawienie

| format | co to jest | samoopisujący się? | kwantyzacja jako część formatu? | kto czyta |
|---|---|---|---|---|
| **safetensors** | kontener tensorów (JSON + bajty) | częściowo (`config.json` obok) | nie, konwencje z boku | transformers, vLLM, SGLang, MLX, mistral.rs, TRT-LLM |
| **GGUF** | kontener + metadane + tokenizer | **tak** | **tak**, typ per tensor | llama.cpp i pochodne, ds4 (własne GGUF), mistral.rs, KT (CPU), vLLM/SGLang (eksperymentalnie) |
| **katalog MLX** | safetensors + konwencja skal/biasów | częściowo | tak (konwencja MLX) | MLX, mlx-lm, oMLX, LM Studio (MLX) |
| **ONNX** | graf + wagi | tak (graf) | nie badałem | ONNX Runtime, OpenVINO |
| **plan TensorRT** | skompilowany silnik | nie | n/d | (TRT-LLM już nie) |
| `pytorch_model.bin` | pickle | nie | nie | **unikaj** (wykonuje kod) |

---

## 11. Konwersje i narzędzia

### 11.1 Przepływ danych

```
                  ┌────────────────────────────────────────────────────────────────┐
 Checkpoint HF    │  convert_hf_to_gguf.py   --outtype bf16|f16|f32|q8_0|tq1_0|…   │
 (safetensors:    ├─────────────►  GGUF F16/BF16 (pełna precyzja, ok. 2 B/parametr)│
  BF16/FP8/FP4)   │                         │                                      │
                  │                         ├──► llama-imatrix -m … -f tekst.txt   │
                  │                         │        └─► imatrix.gguf               │
                  │                         ▼                                      │
                  │        llama-quantize [--imatrix …] [--tensor-type …] in out TYP  │
                  │                         │                                      │
                  │                         ▼                                      │
                  │             GGUF skwantyzowany (Q4_K_M, IQ3_XXS, …)            │
                  │                         │ (opcjonalnie) llama-gguf-split       │
                  │                         ▼                                      │
                  │                    llama-server -m …-00001-of-0000N.gguf       │
                  └────────────────────────────────────────────────────────────────┘

 Ten sam HF ──► mlx_lm.convert --hf-path … -q [--q-bits --q-group-size --q-mode --quant-predicate]
               └─► katalog MLX (safetensors skwantyzowane) ──► mlx_lm.server / oMLX / LM Studio (MLX)

 Ten sam HF ──► llm-compressor / GPTQModel / Model-Optimizer ──► safetensors AWQ/GPTQ/FP8/NVFP4 ──► vLLM / SGLang / TRT-LLM
                                     (GPTQ: llama.cpp potrafi tylko odkwantyzować i zacząć od nowa; AWQ: nie przyjmie)
```

Zasada, którą widać na schemacie: **kwantyzuj z wysokiej precyzji, nie z kwantu**. `llama-quantize` ma flagę `--allow-requantize` z ostrzeżeniem w README: „może poważnie obniżyć jakość w porównaniu z kwantyzacją z 16 lub 32 bitów".

### 11.2 Polecenia (z dokumentacji i dziennika wdrożenia; *nie uruchamiałem*)

**HF → GGUF.** Fragment z dziennika wdrożenia DSpark w `../przyspieszanie-generowania/02-WDROZENIE-DEEPSEEK.md` (własny, uruchomiony) pokazuje składnię konwertera:

```bash
python ~/llama.cpp/convert_hf_to_gguf.py deepseek-ai/DeepSeek-V4-Flash-0731 --remote --dspark \
   --target-model-dir ~/spec-dspark/target-hf --outtype bf16 --outfile ~/spec-dspark/DeepSeek-V4-Flash-0731-DSpark.gguf
```

Z tego, co w nim wynika: potrzebny jest `torch ≥ 2.7` (typ `float8_e8m0fnu`); `--remote` pobiera tylko te pliki safetensors, które zawierają potrzebne tensory (3 z 48 plików = 11 GB zamiast 167 GB); `--outtype` dopuszcza `f32, f16, bf16, q8_0, tq1_0, tq2_0, auto`
(kod konwertera, linia 60). **Skala:** pełna konwersja modelu 284B do BF16 oznaczałaby ok. **568 GB** pośredniego pliku *(moje wyliczenie)* — to dlatego większość ludzi pobiera gotowe kwanty zamiast je robić.

**Imatrix i kwantyzacja** (`tools/imatrix/README.md`, `tools/quantize/README.md` w drzewie `0ce8cd1`):

```bash
llama-imatrix -m model-f16.gguf -f kalibracja.txt -ngl 99 -o imatrix.gguf

# prosta kwantyzacja, 8 wątków; plik wynikowy "ggml-model-Q4_K_M.gguf"
./llama-quantize input-model-f32.gguf q4_k_m 8

# z imatrix i nadpisaniem typów wybranych tensorów (regex) — namiastka receptury w stylu UD
./llama-quantize --imatrix imatrix.gguf --output-tensor-type q5_k --token-embedding-type q3_k \
    --keep-split input-model-f32.gguf q4_k_m 8
./llama-quantize --imatrix imatrix.gguf --tensor-type "\.(\d*[13579])\.attn_k=q5_k" \
    --tensor-type "\.(\d*[02468])\.attn_q=q3_k" input-model-f32.gguf q4_k_m 8
```

Przydatne flagi z README narzędzia: `--tensor-type` (wiele razy, regex), `--output-tensor-type`, `--token-embedding-type`, `--include-weights`, `--prune-layers`, `--allow-requantize`, `--leave-output-tensor`, `--override-kv`.
Zauważ: to **te same pokrętła**, którymi — według oceny w notatkach — można odtworzyć *w duchu* mieszanki UD i receptę ds4 (2-bitowi eksperci + Q8 reszta). Czy Unsloth używa dokładnie tych narzędzi, nie wiadomo (sekcja 7.2); nie obiecuję, że wyjdzie ten sam plik.

**HF → MLX** *(składnia flag z `mlx_lm/convert.py`)*: `mlx_lm.convert --hf-path ID_MODELU -q` z opcjonalnymi `--q-bits`, `--q-group-size`, `--q-mode {affine,mxfp4,nvfp4,mxfp8}` i `--quant-predicate mixed_4_6` (jeden z przepisów `mixed_*`). Domyślnie: 4 bity, grupa 64.

Co umie konwerter, sprawdzisz tak: `grep -n "outtype\|--remote\|--dspark\|--split-max" ~/llama.cpp-0ce8cd1/convert_hf_to_gguf.py` pokaże listę `--outtype` (linia 60) i opcje dzielenia; katalog `conversion/` ma po jednym pliku na rodzinę architektur
> (np. `deepseek.py`) i `base.py` z logiką czytania skwantyzowanych checkpointów (FP8, GPTQ, compressed-tensors, NVFP4/MXFP4).

---

## 12. Kto za tym stoi (Unsloth)

Unsloth to firma z **Y Combinator (lato 2024)**, założona przez **Daniela Hana** (wcześniej NVIDIA; znany z poprawek błędów w Gemma/Llama/Mistral/Phi) i **Michaela Hana**; strona YC wymienia zespół 12 osób (data wpisu nieznana). Repozytorium: licencja dwoista — rdzeń Apache-2.0,
część opcjonalna (UI Studio) AGPL-3.0, co README tłumaczy jako sposób na utrzymanie rozwoju. Pozycja w ekosystemie wynika z **szybkich kwantów i poprawek dla nowych modeli w dniu premiery** (w dokumentacji: poprawki RoPE scaling, epsilon QK Norm w llama.cpp *(dane firmy)*).
Daniel Han ma ok. 56 % commitów repozytorium (6391 z ok. 11,4 tys.) — wysoki „bus factor". **Cenników, rund finansowania i inwestorów nie ustaliłem** (strony `pricing` i `about` zwracały 403); nie opieraj się na niczym, co „pamiętasz" o rundach. Pełniej o pieniądzach i ludziach — w rozdziale [10](10-PIENIADZE-I-LUDZIE.md).

---

## 13. Co z tego dla konfiguracji referencyjnej

### 13.1 Zostań przy GGUF

Na czterech R9700 (gfx1201, ROCm) GGUF to jedyna rodzina z pierwszoklasowym wsparciem we wszystkich silnikach, które na rigu referencyjnym mają szansę działać (llama.cpp z backendem HIP). vLLM ma gfx1201 „na papierze" i dedykowane jądra RDNA (INT4 W4A16, FP8),
ale ROCm jest tam drugoplanowy względem MI300/MI350, a lista kwantyzacji ROCm w kodzie **nie zawiera `gguf` ani `bitsandbytes`**; SGLang nie ma gfx1201 jako celu; EXL3 i TensorRT-LLM to CUDA. Dlatego dla tego sprzętu kwantyzujesz **do GGUF** i wybierasz typ według
**bajtów na token** (sekcja 7.4c) oraz **jakości zmierzonej KLD na własnych promptach** (sekcja 9).

### 13.2 Budżet pamięci dziś

Z dziennika wdrożenia (zmierzone) i sekcji 1.1:

| pozycja | wartość |
|---|---|
| pamięć 4 kart razem | 136,8 GB (127,4 GiB) |
| wagi UD-IQ3_XXS | 104,2 GB (104 207 848 508 B; sekcja 7.4) |
| draft DSpark | plik 10,9 GB + bufory; razem ok. 4 GB na każdej z 4 kart (ok. 16 GB) |
| wolny VRAM po załadowaniu → po realnym użyciu | karta 0: 1,08 → **0,82 GB**; pozostałe: 1,7 → 1,43 GB (razem ≈ 5,1 GB) |
| reguła z procedury | ≥ 1 GB wolnego na kartę (karta z pulpitem ≥ 0,8 GB) |

Wniosek *(moje wyliczenie)*: **wdrożona konfiguracja jest na granicy pojemności.** KV DeepSeeka jest tani (0,1–0,4 GB na kartę dla 131 tys. kontekstu — dziennik; ok. 6,9 KB na token *(moje wyliczenie z notatek, założenia niepewne)*), więc to nie kontekst zjada pamięć, tylko wagi + draft + bufory obliczeń.

### 13.3 Kiedy większy kwant by się zmieścił i co by kosztował w szybkości *(rozumowanie z przepustowości; niczego nie mierzyłem)*

Dwie asymetrie MoE z sekcji 7.4(c): bity **ekspertów** kosztują dużo pojemności (277 mld parametrów) i mało przepustowości (6,49 mld czytanych na token); bity **części gęstej** — odwrotnie (7 mld, czytane w całości, ale mała pojemność).

| zmiana | pojemność | bajty/token | wpływ na sufit prędkości |
|---|---:|---:|---|
| eksperci +0,25 bpw (np. część warstw z IQ3_XXS → IQ3_S/IQ4_XS) | **+8,7 GB** (277·10⁹·0,25/8) | + 0,20 GB (+2…3 % z 6,9–9,9 GB) | ok. −2…3 % |
| eksperci +0,5 bpw | **+17,3 GB** | + 0,41 GB (+4…6 %) | ok. −4…6 % |
| część gęsta z ok. 5 do 8,5 bpw | + 3,1 GB | + 3,1 GB (+44 % przy bazie 6,9 GB) | ok. −30 % |

Czyli **w bajtach (a więc w prędkości) najdrożej wychodzi podnoszenie części gęstej, nie ekspertów** — a ta i tak jest w mieszankach UD wysoko (IQ4_XS–Q6_K w pliku Qwena).
Problem w tym, że pamięci nie ma: wolnych masz ok. 5 GB łącznie, a nawet +0,25 bpw na ekspertach to +8,7 GB. Żeby zrobić miejsce:

* **Zrezygnować z draftu** (zwolni ok. 16 GB). Ale draft dał +50 % (23,5 → 35,2 tok/s przy podziale warstwami, dziennik) — koszt ok. **−33 %** prędkości (1/1,5), plus kilka procent za droższe wagi. Zgrubnie z 49 do ok. **30 tok/s** *(moje wyliczenie; zakłada, że wkłady draftu i podziału tensorowego się mnożą, czego nie sprawdziłem)*.
  Kupujesz wtedy ok. +0,45 bpw (16 GB · 8 / 284 mld, jeśli całość pójdzie w wagi) — niewiele jakości za dużo prędkości.
* **Odciążyć eksperci do RAM-u hosta** (`--cpu-moe`, `-ot` w llama.cpp, według notatek o KTransformers): rozmiaru RAM-u i przepustowości maszyny nie ustaliłem, więc nie podam kosztu. Przepustowość pamięci hosta jest zwykle wielokrotnie niższa niż 640 GB/s GDDR6 *(niezweryfikowane)*, więc każdy ekspert „w RAM-ie" mocno spowalnia.
* **Mniejszy `--ubatch-size`** (już 512; wcześniej zysk 0,7–2,0 GB na kartę kosztował 8 % prefillu) — kolejny krok to już tylko kilka GB i wolniejszy prefill *(niezweryfikowane)*.

**Wniosek:** UD-IQ3_XXS jest dziś **największym kwantem, który mieści się razem z draftem**. Wyższy wymaga rezygnacji z draftu (−33 %) albo odciążania do RAM-u. W dół (np. IQ2_XXS) jakość zjeżdża stromo — w tabeli Llama-3-8B KLD rośnie z 0,18 (IQ3_XXS) do 0,81 (IQ2_XXS) — więc nie szukaj miejsca tą drogą.
Zanim cokolwiek zmienisz, wykonaj **pomiar B i C** z sekcji 9: być może IQ3_XXS jest „dość dobry", a być może nie — i dopiero wtedy ta tabela ma sens.

### 13.4 Zanim pobierzesz następny model — arytmetyka na kartce

```
rozmiar_wag ≈ liczba_parametrów · bpw / 8
mieści się, jeśli:  rozmiar_wag + draft (jeśli jest) + bufory + zapas ≥1 GB/kartę  ≤  136,8 GB
prędkość (sufit) ≈ przepustowość / (gęste·b_gęste/8 + aktywne_eksperci·b_eksperci/8)
```

Dla gęstych modeli drugi wzór upraszcza się do „przepustowość / rozmiar wag". Dla MoE **rozdziel** część gęstą i ekspertów, jak w 7.4(c) — dane o liczbie parametrów weź z `config.json` modelu.

### 13.5 Maki

* **MLX 4-bit, grupa 64 = 4,5 bpw**; to ta sama rodzina co Q4_K (4,5 bpw). Dla Maca sufit prędkości z notatek: M5 Max (614 GB/s) — 4-bit gęsty 30B ok. 36 tok/s (25 po korekcie 70 %), MoE 13B aktywnych ok. 84 (59) *(wzór niezweryfikowany; „sufit", nie obietnica)*.
  Pomiar kontrolny: ds4 DeepSeek V4 Flash Q2 na M5 Max daje 39,35 tok/s, czyli ok. 26 % ceilingu wzoru — z powodu gęstych tensorów w Q8/F16 (sekcja 6.9).
* **oQ4e** (oMLX) dla modeli średnich: np. Qwen3.6-35B-A3B oQ4e = 20 GB, wg autora na jego zestawie bez straty (83,05 wobec 82,68) *(dane projektu)*. Nie wierz, dopóki nie zmierzysz na swoich zadaniach — zasada ta sama co wyżej.
* Pliki GGUF działają na Macu w llama.cpp (Metal); jakość kwantu jest ta sama, zmienia się tylko jądro.

### 13.6 Lista kontrolna

1. Policz typy tensorów i średnie bpw swojego pliku (*Sprawdź sam 3*) — dwie liczby, które rozstrzygną wątpliwości z sekcji 7.4.
2. Wykonaj **pomiar A** (KLD między konfiguracjami; tani) i **pomiar C** (zadania + odsetek poprawnych wywołań narzędzi; na większej liczbie różnych zadań), zanim zbudujesz agentów na szybkiej konfiguracji.
3. Zachowaj plik imatrix publikowany przez Unslotha obok modelu, jeśli kiedyś będziesz kwantyzować własne dostrojone modele — to najtańsza poprawa jakości na niskich bitach.
4. Nie ufaj numerom z cudzych tabel: jakość zależy od modelu (sekcja 5.2), a każda liczba powinna mieć sprzęt, wersję, model + kwant, kontekst i datę.

---

## 14. Czego nie ustaliłem

1. **Składu pliku `DeepSeek-V4-Flash-0731-UD-IQ3_XXS`**: jakie typy tensorów zawiera i w jakich proporcjach (rozmiar jest zmierzony: 104,2 GB dziesiętnych). Do sprawdzenia lokalnie (*Sprawdź sam 3*).
2. **Jakości UD-IQ3_XXS na DeepSeek-V4-Flash** — względem jakiegokolwiek wyższego kwantu. Żadnych danych nie mam.
3. **Jak Unsloth wylicza wybór typów per warstwa** i czy używa standardowego `llama-quantize --tensor-type`; recepta nie jest w publicznym repozytorium. Pierwotny wpis o Dynamic v1 zwracał 403.
4. **Liczby z dokumentacji Unslotha** (Gemma 3 27B MMLU 71,47 % / 70,64 %; ok. 7,5 % mniej KLD) — znam je tylko ze streszczenia narzędzia pobierającego; sprawdź na stronie.
5. **Pokrycia typów kwantyzacji na backendach HIP/Vulkan** — zweryfikowałem istnienie katalogów backendów, nie każdego typu. Wsparcia typów MX/NVFP4 na gfx1201 — brak danych.
6. **vLLM na gfx1201**: dokumentacja i kod się nie zgadzają (AWQ/GPTQ); wydajności FP8 i INT4 na RDNA4 nie zmierzono. SGLang: czy w ogóle działa na gfx1201 — wymaga próby, której nie wolno było robić.
7. **EXL3 vs GGUF/AWQ przy tym samym bpw** — nie zebrałem pierwotnych tabel (`doc/exl3.md` zwracał 404). Stan ExLlamaV2: README mówi „zastąpiony", API GitHuba nie pokazuje archiwizacji — sprzeczność.
8. **Stored bpw GPTQ/AWQ/HQQ** — wyliczone dla typowych konfiguracji (g128, g64), nie zmierzone.
9. **Szczegóły ONNX i układ bajtów safetensors** poza celami z dokumentacji HF; **niektóre numery arXiv** podaję za notatkami (QLoRA 2305.14314).
10. **Moce przerobowe maszyny poza kartami** (ilość RAM hosta, jego przepustowość) — potrzebne do oceny odciążania ekspertów do RAM-u; nie ma ich w notatkach.
