# 02 · Wdrożenie na DeepSeek-V4-Flash-0731 — dziennik, pomiary, konfiguracja

Zapis tego, co zrobiłem 19 października 2026, **łącznie z drogami, które nie zadziałały**. Teoria: [01-JAK-TO-DZIALA.md](01-JAK-TO-DZIALA.md).
Sprzęt: 4× Radeon AI PRO R9700 (32 GB każda), ROCm 7.2, llama.cpp + `llama-swap` (serwowanie z przełączaniem modeli na żądanie).

> **Metoda pomiaru** (skrypty w [narzedzia/](narzedzia/README.md)): `bench_spec.py` wysyła 4 rodzaje zadań (tłumaczenie PL→EN, wywołanie narzędzia,
> kod, proza swobodna) × temperatura 0 i 1,0, po 300 tokenów, i odczytuje czas **z liczników samego serwera** (`timings.predicted_per_second`).
> Model „myśli” przed odpowiedzią — te tokeny też są liczone, bo to realny obraz użycia. Jedno powtórzenie ⇒ szum ±2 tok/s; różnic mniejszych nie interpretuję.

## 1. Punkt wyjścia i diagnoza (tylko odczyt)

- Stan: llama.cpp `680a036` (28 IX 2026), DeepSeek-V4-Flash-0731 UD-IQ3_XXS (Unsloth), podział warstwami, 4 sloty × 131 072 kontekstu,
  **23,5 tok/s** na jednego agenta (stabilne co do 0,3).
- Szybkie sprawdzenie: czy ten llama.cpp zna speculative decoding? Tak — `--spec-type draft-mtp, draft-eagle3, draft-dflash, draft-dspark, ngram-*`.
- Czy GGUF ma głowicę MTP? Nagłówki: 43 bloki, **zero tensorów `nextn`/MTP** (skrypt `gguf-inspect.py`). Loader po cichu wyłącza MTP, gdy tensorów brak.
- Czy oryginalny checkpoint ma coś do spekulacji? Tak: DSpark (tensory `mtp.*`, pliki 46–48 z 48, ~11 GB), konwerter llama.cpp ma gotową opcję `--dspark`.

## 2. Draft: konwersja DSpark → GGUF (bez zatrzymywania modelu)

```bash
# osobne środowisko Pythona dla konwertera (nie rusza systemowego); torch ≥ 2.7 jest wymagany (typ float8_e8m0fnu)
python3 -m venv ~/spec-dspark/venv && . ~/spec-dspark/venv/bin/activate
pip install -r ~/llama.cpp/requirements/requirements-convert_hf_to_gguf.txt huggingface_hub safetensors
pip install -e ~/llama.cpp/gguf-py

# "model docelowy": sam config + tokenizer (żeby draft miał ten sam słownik)
mkdir -p ~/spec-dspark/target-hf   # config.json, tokenizer.json, tokenizer_config.json, generation_config.json, model.safetensors.index.json

# --remote: pobierz tylko 3 potrzebne pliki (11 GB), nie cały checkpoint (167 GB)
export HF_HOME=~/spec-dspark/hf-cache
python ~/llama.cpp/convert_hf_to_gguf.py deepseek-ai/DeepSeek-V4-Flash-0731 --remote --dspark \
   --target-model-dir ~/spec-dspark/target-hf --outtype bf16 --outfile ~/spec-dspark/DeepSeek-V4-Flash-0731-DSpark.gguf
```

Wynik: **10,9 GB, 81 tensorów**, architektura `dflash`, blok 5, warstwy docelowe 41–43 (numeracja od 1). Ostrzeżenie „Transformers does not recognize deepseek_v4”
jest nieszkodliwe (konwerter czyta wtedy `config.json`). Źródło: `deepseek-ai/DeepSeek-V4-Flash-0731`, rewizja `7872f01b1d1fe23eabc4c98b48bffcef5a386062`.
Plik trzymam obok modelu: `~/models/DeepSeek-V4-Flash-0731-GGUF/DSpark/`, z sumą SHA256.

## 3. Pomiary — runda 1: stary llama.cpp, podział warstwami

Jeden strumień (`--parallel 1`, 131 072), średnia tok/s ze wszystkich zadań:

| Wariant | Średnia | Wniosek |
|---|---|---|
| bez draftu | **23,5** | punkt odniesienia |
| DSpark n=5, p-min 0 | 33,2 | **proza wolniejsza niż bez draftu** (19–22) |
| n=5, p-min 0,5 | 34,8 | próg pewności ratuje prozę |
| n=5, p-min 0,75 | 32,1 | za ostrożnie |
| **n=3, p-min 0** | **36,1** | najlepsza średnia i najlepsze tłumaczenie (34) |
| n=3, p-min 0,5 | 34,3 | bez zysku względem p-min 0 |
| n=4 / n=2 (p-min 0) | 32,4 / 34,7 | n=2 najrówniejszy (żadne zadanie poniżej 28) |
| n=5, p-min 0,5 **+ `ngram-mod`** | 34,4 | n-gramy nic nie dodały (zwykły tekst się nie powtarza) |

`n` = `--spec-draft-n-max` (ile tokenów draft proponuje), `p-min` = `--spec-draft-p-min` (próg głowicy pewności). Wybrałem n=3, p-min 0.

**Wielu agentów naraz** (4 sloty, temp. 0,2; `bench_conc.py`):

| Agentów | bez draftu: każdy / razem | z draftem: każdy / razem |
|---|---|---|
| 1 | 23,1 / 22 | 33,3 / 32 (+44 %) |
| 2 | 19,3 / 38 | 24,6 / 46 (+21 %) |
| 4 | 13,9 / 50,7 | 13,9 / 50,0 (±0) |

Przy 4 agentach GPU jest już nasycone *batchingiem* (4 tokeny na krok z 4 strumieni to w gruncie rzeczy ta sama „spekulacja” zrobiona wsadem) — draft nic nie dodaje i nic nie odbiera.

**Cena draftu:** prefill (6,2 tys. tokenów promptu) spadł z **~960 do ~490 tok/s** — draft też musi przeczytać prompt. Przykład: nowe 10 000 tokenów promptu + 100
tokenów odpowiedzi: bez draftu 10,4 + 4,3 ≈ **14,7 s**, z draftem 20 + 3 ≈ **23 s** (wolniej); 2 000 + 300: 15,0 s vs **12,6 s** (szybciej).
Zasada: **im więcej generujesz względem tego, co czytasz, tym bardziej draft się opłaca.**

**Pamięć:** draft zjada ~4 GB na kartę (wagi 2,7 GB + bufory), a karta 0 obsługuje też pulpit. Zostawało na niej **0,15 GB wolnego** przy `--ubatch-size 1024`.
Dźwignie, od najskuteczniejszej: `--ubatch-size 1024→512` (+0,7 GB na karcie 0, +1,2–2,0 GB na pozostałych; koszt: prefill −8 %), mniej slotów/kontekstu, KV draftu w q8_0 (pomijalne).
Przesunięcie warstw przez `--tensor-split` w trybie warstw nie pomogło: warstwa ma ~2,4 GB, więc jedna przesunięta przepełnia sąsiada.

## 4. Pomiary — runda 2: nowy llama.cpp + podział tensorowy

Zbudowałem **osobno** (stara instalacja nietknięta) llama.cpp `0ce8cd1` z 19 X 2026 z tymi samymi flagami HIP (dzięki `ccache` zajęło to ~2 min):

```bash
git init ~/llama.cpp-0ce8cd1 && cd ~/llama.cpp-0ce8cd1
git remote add origin https://github.com/ggml-org/llama.cpp
git fetch --depth 1 origin 0ce8cd11416c8840498e6701bcbe39ad4b858c2b && git checkout FETCH_HEAD   # GitHub wymaga pełnego SHA
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DGGML_HIP=ON -DGPU_TARGETS=gfx1201 \
      -DGGML_HIP_GRAPHS=ON -DGGML_HIP_NO_VMM=ON -DCMAKE_HIP_COMPILER=/opt/rocm-7.2.4/lib/llvm/bin/clang++ -DGGML_CCACHE=ON
nice cmake --build build -j14 --target llama-server llama-bench llama-cli
```

Macierz 2×2 (1 slot, 131 072, `bench_spec.py`, średnia tok/s):

| | bez draftu | z draftem (n=3) |
|---|---|---|
| podział warstwami | 25,2 | 37,9 |
| **podział tensorowy** | 29,1 | **46,2** |

Względem tego samego trybu bez draftu draft daje 1,5× (warstwy) i 1,6× (tensor); względem punktu wyjścia 25,2 oba mechanizmy razem dają 1,8×. Dalej, przy konfiguracji „na produkcję” (`--ubatch-size 512`, równy podział, n=3):

| Kształt | tok/s | wolny VRAM na kartach 0 / 1–3 | uwagi |
|---|---|---|---|
| 1 slot × 131k (u1024) | 46,2 | 0,35 / 1,5 | punkt wyjścia |
| 2 sloty × 131k | **49,6** | 0,37 / 1,17 | za mało zapasu na karcie 0 |
| **2 sloty × 98k** | **49,2** | **0,73 / 1,68** | **wybrane** |
| 4 sloty × 65k | 44,6 | 0,16 / 1,0 | wolniejsze i za ciasne |
| 4 sloty × 131k | — | — | **brak pamięci** przy ładowaniu (`cudaMalloc failed: out of memory`) |

Wybrana konfiguracja, wyniki per zadanie (temp. 0 / 1,0): tłumaczenie 51,9 / 43,9 · wywołanie narzędzia 62,0 / 54,0 · kod 58,5 / 50,9 · proza 37,8 / 34,6;
akceptacja 0,70/0,59 · 0,95/0,80 · 0,82/0,73 · 0,40/0,36.

### Pułapki trybu tensorowego (każdą zmierzyłem)

1. **Nierówny `--tensor-split` (`0.85,1,1,1`) zawiesza ładowanie** — serwer milczy po komunikacie, że `--fit` nie jest zaimplementowane dla trybu tensorowego; `llama-swap` po 300 s zgłasza błąd 500.
   Zdiagnozowałem to, uruchamiając `llama-server` bezpośrednio z jedną zmianą naraz: równy podział + `ubatch 512` ładuje się w 108 s i działa; nierówny podział + `ubatch 1024` wisi.
2. **4 sloty × 131 072 → brak pamięci** na karcie 0: nie powiódł się przydział ~2,75 GB (KV w trybie tensorowym jest nieskwantyzowane, co zwiększa zapotrzebowanie). Stąd 2 sloty.
3. **Ładowanie trwa ~108 s** (zamiast ~35 s w trybie warstw). Po 10 min bezczynności `llama-swap` zwalnia model (`ttl: 600`), więc pierwsze żądanie czeka ~2 min.
   Jeśli to przeszkadza, podnieś `ttl` w konfiguracji (kosztem VRAM zajętego, gdy model nie jest używany).
4. Log pokazuje `internal AllReduce init failed (n_devices != 2?); falling back to meta-backend butterfly` — przy 4 kartach działa ogólna ścieżka sumowania.

## 5. Bramka przed wdrożeniem

Skrypt `gate-test.py` dodaje tymczasowy wpis do `llama-swap`, mierzy i porównuje z modelem bez draftu:

| Test | Wynik |
|---|---|
| wolny VRAM po załadowaniu / **po użyciu** | 1,08 / 1,7 GB → **0,82** / 1,43 GB (karta 0 / pozostałe; po realnym użyciu spada o ~0,3 GB) |
| prefill (6,2 tys. tokenów) | **694–735 tok/s** (warstwy+draft: 490; bez draftu: ~960) |
| 1 agent | 49,7 tok/s |
| 2 agentów | 34,5 każdy, **63 razem** |
| 4 żądania na 2 slotach | 33 średnio, **60 razem** |
| identyczność z modelem bez draftu (temp. 0) | **0 z 4** identycznych — rozjazd już w pierwszych tokenach „myślenia”; odpowiedzi końcowe poprawne merytorycznie |

Ten ostatni wiersz jest powodem, dla którego pomiar szybkości **nie** jest dowodem jakości — a samej jakości nie zmierzyłem: patrz sekcja „Jakość” w [README](README.md).
W trybie warstw z draftem 2 z 4 odpowiedzi były identyczne co do znaku, a pozostałe rozjeżdżały się na „remisach” tokenów (np. `*three*` vs `three`).
Podział tensorowy zmienia kolejność sumowania zmiennoprzecinkowego, więc rozjazdy są częstsze. Nie wiem, czy to ma jakikolwiek wpływ na jakość — benchmarku jakości po zmianie nie ukończyłem.

## 6. Konfiguracja końcowa

`~/.config/llama-swap/config.yaml`, wpis `deepseek-v4-flash-0731` (aliasy `deepseek`, `deepseek-v4`… bez zmian — klienci nic nie poprawiają):

```yaml
    cmd: |
      ~/llama.cpp-0ce8cd1/build/bin/llama-server --port ${PORT} --jinja --agent -fa on
      -m  ~/models/DeepSeek-V4-Flash-0731-GGUF/UD-IQ3_XXS/DeepSeek-V4-Flash-0731-UD-IQ3_XXS-00001-of-00004.gguf
      -md ~/models/DeepSeek-V4-Flash-0731-GGUF/DSpark/DeepSeek-V4-Flash-0731-DSpark.gguf
      --spec-type draft-dspark --spec-draft-n-max 3 --spec-draft-p-min 0
      --split-mode tensor -ctk f16 -ctv f16
      -ngl 999 --ctx-size 196608 --load-mode dio
      --parallel 2 --ubatch-size 512
      --temp 1.0 --top-p 1.0 --top-k 0 --min-p 0
```

| Flaga | Co robi | Dlaczego taka wartość |
|---|---|---|
| `-md PLIK` | plik draftu | dla `draft-dspark` to GGUF o architekturze `dflash` |
| `--spec-type draft-dspark` | wybiera mechanizm | patrz [01, §3](01-JAK-TO-DZIALA.md); można łączyć typy po przecinku |
| `--spec-draft-n-max 3` | ile tokenów draft proponuje na krok (limit = rozmiar bloku = 5) | najlepsza średnia w rundzie 1; **w trybie tensorowym nie stroiłem n ponownie** |
| `--spec-draft-p-min 0` | próg pewności głowicy; bloki są obcinane, gdy przewidywana akceptacja < p | 0 = wyłączony |
| `--split-mode tensor -ctk f16 -ctv f16` | podział tensorowy; KV musi być nieskwantyzowane | patrz [01, §5](01-JAK-TO-DZIALA.md) |
| `--ctx-size 196608 --parallel 2` | 2 sloty × 98 304 | tyle mieści się z zapasem pamięci |
| `--ubatch-size 512` | mikro-wsad prefillu | **główna dźwignia pamięci**; prefill ~−8 % względem 1024 |
| `--load-mode dio` | omija `mmap` (błąd ROCm przy dużych modelach) | bez zmian względem wcześniej |

Obok zostają: `deepseek-v4-flash-0731-nospec` (stary układ bez draftu, `ubatch 1024`, 4 sloty) — do zadań z ogromnymi promptami i krótką odpowiedzią, oraz
`deepseek-v4-flash-0731-layerspec` (stary llama.cpp, podział warstwami + draft, 4 sloty) — awaryjny powrót. Kopia konfiguracji sprzed zmian: `config.yaml.bak-20261019-przed-tensor`.

## 7. Strojenie ręczne

1. Zmień **jedną** rzecz w `config.yaml` (`llama-swap` przeładuje konfigurację sam i zwolni załadowany model).
2. `python3 bench_spec.py deepseek` (≈3 min; `BENCH_REPS=2` dla mniejszego szumu); porównaj średnią tok/s i `accept`.

| Chcę… | Zmień | Efekt / pułapka |
|---|---|---|
| szybciej na wywołaniach narzędzi i kodzie | `--spec-draft-n-max 4` lub `5` | więcej tokenów na krok przy akceptacji ~0,9; **na prozie traci** |
| nigdy nie być wolniejszym niż bez draftu | `--spec-draft-n-max 2` | najrówniejszy wynik |
| więcej wolnego VRAM | niższy `--ctx-size`, `--ubatch-size 256` | ubatch największy efekt; koszt: prefill |
| szybszy prefill | `--ubatch-size 1024` | karta 0 zostaje z <0,5 GB — ryzyko braku pamięci |
| więcej slotów | **nie przy tym modelu na tych kartach** | 4 sloty nie mieszczą się w trybie tensorowym |
| wyłączyć draft | model `…-nospec` | |

**Żywy podgląd skuteczności draftu:** `curl -sN localhost:8080/logs/stream/upstream | grep "draft acceptance"` — licz średnie `mean len`;
przy `n=3` draft się opłaca, gdy `mean len > 2,05` ([01, §2](01-JAK-TO-DZIALA.md)).
W kliencie ustaw `temperature` 0–0,3 dla wywołań narzędzi/JSON: draft zgaduje zachłannie, więc przy temp. 1,0 akceptacja jest niższa (u mnie 0,95 → 0,80 na wywołaniach narzędzi).

## 8. Ograniczenia

- **Prefill ~25 % wolniejszy** niż bez draftu w trybie tensorowym (700 vs 960) — dla zadań „dużo czytam, mało piszę” użyj `…-nospec`.
- **2 sloty × 98 304** zamiast 4 × 131 072. Trzeci równoległy agent czeka w kolejce.
- **Zapas VRAM na karcie 0: 0,82 GB** po realnym użyciu. Pamięć jest rezerwowana statycznie przy starcie, ale nie dokładaj nic na tę kartę.
- **Odpowiedzi „puste” przy małym `max_tokens`:** model najpierw „myśli” (`reasoning_content`) i to zjada limit — nie jest to błąd draftu.
- **Tryb eksperymentalny:** upstream wprost zaleca walidację jakości przed wdrożeniem.
- Dokumentacja upstream (sekcja DSpark) wciąż pisze „obsługiwane tylko backbone’y Qwen3” — **jest nieaktualna**: konwerter i loader DeepSeek-V4 DSpark działają (to wdrożenie).

## 9. Co dalej (nie przetestowane)

1. **Strojenie `n` w trybie tensorowym** (stałe kosztu kroku są inne niż w trybie warstw).
2. **RCCL** (`-DGGML_HIP_RCCL=ON`) i **P2P** (`GGML_CUDA_P2P=1`) — przyspieszyłyby sumowanie między kartami. Upstream ostrzega, że RCCL nie zawsze pomaga, a P2P potrafi zepsuć wyniki
   na części płyt (IOMMU) — po włączeniu trzeba sprawdzić poprawność wyjścia.
3. **Inne drafty** znalezione przez `find-drafts.sh`: EAGLE-3 dla V4-Flash-0731, DFlash.
4. **Lepsza kwantyzacja modelu docelowego** (wyższa akceptacja), jeśli VRAM pozwoli.

## 10. Jak cofnąć

```bash
# wróć do poprzedniego układu (stary llama.cpp, warstwy + draft): w kliencie użyj modelu deepseek-v4-flash-0731-layerspec
# albo bez draftu: deepseek-v4-flash-0731-nospec
# pełne cofnięcie: cp ~/.config/llama-swap/config.yaml.bak-20261019-przed-tensor ~/.config/llama-swap/config.yaml
```
