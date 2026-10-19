# 01 · Jak to działa — dlaczego generowanie jest wolne i jak je przyspieszyć

Lekcja. Po jej przeczytaniu powinieneś umieć przewidzieć, czy dany model zyska na speculative decodingu, i zrozumieć
każdą flagę z kolejnych plików. Liczby pochodzą z moich pomiarów na 4× Radeon AI PRO R9700.

---

## 1. Generowanie jest ograniczone pamięcią, nie obliczeniami

Model językowy generuje odpowiedź **po jednym tokenie**. Żeby wyliczyć jeden token, trzeba przejść przez wszystkie warstwy,
a to oznacza **przeczytanie z pamięci karty wszystkich wag, które w danym kroku są aktywne**. Przy tak małej pracy
na token (mnożenie wektora przez macierz) procesor graficzny większość czasu **czeka na pamięć**. Mówimy: dekodowanie jest
**ograniczone przepustowością pamięci** (*memory-bound*).

Rachunek dla DeepSeek-V4-Flash:

- 284 mld parametrów, ale to **MoE** (*Mixture of Experts*): 256 ekspertów w warstwie, na token aktywnych jest 6.
  Na token pracuje więc ~**13 mld** parametrów.
- Kwantyzacja UD-IQ3_XXS to ~3 bity na wagę → ~**5 GB do przeczytania na token**.
- Jedna karta R9700 czyta ~640 GB/s → sufit teoretyczny ~100+ tok/s. **Zmierzone: 23,5 tok/s.** Różnicę zjadają przekazania
  między kartami, sterowanie kernelami i nieregularny odczyt ekspertów.

**Wniosek, na którym stoi cały katalog:** skoro koszt kroku to głównie *czytanie wag*, to sprawdzenie **kilku tokenów naraz
kosztuje niewiele więcej niż jednego** — wagi czytamy raz. Prefill (czytanie promptu) działa właśnie tak i jest ~40× szybszy
na token niż generowanie.

### Pułapka: „GPU 100 %” nie znaczy „karta wykorzystana”

Domyślnie llama.cpp dzieli model **warstwami** (`--split-mode layer`): karta 0 ma pierwszą czwartą część warstw, karta 1 następną itd.
Token przechodzi przez karty **po kolei** (potok, *pipeline*), więc w danej chwili pracuje **jedna** karta, a trzy czekają. Wskaźnik
„użycie GPU 100 %” oznacza tylko, że karta jest zajęta w swoim okienku — nie, że wyczerpuje przepustowość pamięci.
To drugi (po pamięci) powód wolnego generowania — i tu wchodzi podział tensorowy (§5).

---

## 2. Speculative decoding

**Analogia.** Asystent pisze szkic odpowiedzi „na czuja”, profesor (duży model) czyta cały szkic naraz i skreśla od pierwszego błędu.
Czytanie szkicu jest tanie, bo profesor i tak musi wczytać swoją wiedzę (wagi) — robi to **raz na cały szkic**, nie raz na słowo.

Jeden krok:

```
1. Draft (zgadywacz) widzi stan dużego modelu i PROPONUJE n tokenów:        [A] [B] [C]
2. Duży model w JEDNYM przebiegu liczy, co sam wybrałby po:                  ostatnim tokenie, A, A+B, A+B+C
3. Porównanie od lewej:   A ✔   B ✔   C ✘   →  zatwierdzamy A, B, a w miejsce C bierzemy token dużego modelu
4. Efekt: w jednym kroku wyszły 3 tokeny (A, B + poprawka) zamiast 1
```

### Dlaczego nie traci się jakości

Zatwierdzany jest wyłącznie token, który **duży model sam by wybrał** w tym miejscu. Draft może się mylić — wtedy tracimy tylko
trochę czasu, nie jakość. (Przy losowaniu z temperaturą stosuje się odpowiednik tej reguły, który zachowuje rozkład prawdopodobieństwa
modelu.) Zastrzeżenie praktyczne: obliczenia zmiennoprzecinkowe zależą od kształtu partii, więc na *remisach* dwóch niemal równie
prawdopodobnych tokenów wynik może się różnić od dawnego — bez wpływu na poprawność, ale „identyczność co do znaku” nie jest gwarantowana.

### Dwie liczby, które musisz umieć czytać

W logu serwera po każdym żądaniu:

```
draft acceptance = 0.75214 (  88 accepted /  117 generated), mean len =  3.26
```

| Wielkość | Znaczenie |
|---|---|
| `acceptance` | jaka część **zaproponowanych** tokenów została przyjęta (88 z 117) |
| **`mean len`** | **ile tokenów wychodzi średnio z jednego kroku** (łącznie z tokenem dużego modelu). To ta liczba decyduje o prędkości. Bez draftu = 1,0 |

### Reguła opłacalności (wyprowadzona z moich pomiarów)

Dla `n = 3` i `n = 5` tokenów draftu koszt jednego kroku dobrze opisuje wzór:

```
czas kroku  ≈  43 ms  +  15 ms × n          (n = ile tokenów draft proponuje)
tok/s       ≈  mean_len / czas_kroku
```

- bez draftu: 43 ms/token = 23,3 tok/s ✔ (zmierzone 23,5)
- `n=3`: krok ≈ 88 ms; `mean len 3,26` → **37 tok/s** (zmierzone ~38 ✔)
- **Próg opłacalności:** draft się opłaca, gdy `mean len > (43 + 15·n) / 43`. Dla `n=3` to **2,05**; dla `n=5` — **2,7**.

To wyjaśnia wszystkie tabele z następnego pliku: tekst swobodny (proza) ma niską akceptację → `mean len` ≈ 2 → draft niczego nie daje;
wywołania narzędzi (JSON) mają akceptację ~0,9 → `mean len` ~3,7 → prawie 2×.
*(To przybliżenie dopasowane do dwóch punktów — reguła kciuka do strojenia, nie prawo fizyki. Zmierzone przed przejściem na podział tensorowy;
tam stałe są inne, ale logika ta sama.)*

### Dlaczego u MoE zysk jest mniejszy niż u modeli gęstych

Sprawdzenie 4 tokenów aktywuje **więcej różnych ekspertów** niż jednego (każdy token wybiera własną szóstkę z 256), więc krok czyta więcej wag.
Dlatego krok z draftem kosztuje u mnie ~2× zwykły krok, a nie ~1,1×. Model gęsty (32B) czyta te same wagi niezależnie od liczby tokenów w partii —
zyskuje więcej.

---

## 3. Odmiany speculative decodingu (llama.cpp, stan z 19 października 2026)

`--spec-type` przyjmuje jeden lub kilka typów po przecinku:

| Typ | Skąd bierze propozycje | Wymaga | Kiedy dobry |
|---|---|---|---|
| `draft-simple` (`-md mały.gguf`) | **mały model** z tym samym tokenizerem (np. 0,6B dla 32B) | osobny mały model | modele gęste, rodziny z „młodszym rodzeństwem” |
| **`draft-mtp`** | **głowica MTP** (*Multi-Token Prediction*) — dodatkowa warstwa wbudowana w model, przewiduje token n+2 | tensory `nextn.*` w GGUF | gdy model je ma **i GGUF ich nie wyciął** |
| `draft-eagle3` | mała jednowarstwowa sieć czytająca stany ukryte modelu | osobny plik EAGLE-3 pod konkretny model | gdy ktoś go wytrenował dla Twojego modelu |
| `draft-dflash` | mała sieć generująca **cały blok tokenów w jednym przebiegu** (dyfuzja blokowa) | osobny plik DFlash | j.w. |
| **`draft-dspark`** (u mnie) | **DFlash + „głowica Markowa”** (zależność od poprzedniego tokenu) **+ głowica pewności** | osobny plik DSpark | j.w.; dla DeepSeek-V4 dostarcza go sam DeepSeek |
| `ngram-*` (`simple`, `map-k`, `map-k4v`, `mod`, `cache`) | **historia tekstu**: jeśli ciąg się powtarza, zgaduje, że będzie dalej tak samo | nic (zero wag, zero VRAM) | przepisywanie kodu, streszczanie z cytatami |

Pełny opis flag w oficjalnej dokumentacji: [05-ODNIESIENIE-LLAMA-CPP-SPECULATIVE.md](05-ODNIESIENIE-LLAMA-CPP-SPECULATIVE.md).

### DSpark — co dokładnie siedzi w DeepSeek-V4-Flash-0731

- Oficjalny checkpoint **0731** nie ma zwykłej głowicy MTP; ma **głowicę DSpark** (w repozytorium HF to tensory `mtp.*` w trzech ostatnich
  plikach safetensors, ~11 GB). README modelu: *„it comes with a speculative decoding module attached”*.
- Parametry z `config.json`: **blok 5 tokenów**, czyta stany ukryte z **warstw 40, 41, 42** (trzy ostatnie z 43), „ranga Markowa” 256,
  jest głowica pewności (przewiduje, czy dana pozycja bloku zostanie przyjęta → flaga `--spec-draft-p-min`).
- Draft **nie jest samodzielnym modelem**: czyta stany ukryte dużego modelu, a embeddingi i głowicę wyjściową pożycza od niego.
- Publiczne GGUF-y (m.in. Unsloth UD-IQ3_XXS, którego używam) **wycinają** te tensory — sprawdziłem nagłówki: 43 bloki, zero tensorów `nextn`/MTP.
  Dlatego `draft-mtp` na tym pliku nic by nie dało, a draft trzeba było skonwertować z oryginalnego checkpointu.

---

## 4. Dlaczego zysk wynosi „tylko” 1,5–2×, a nie 3×

- **MoE** (§2): weryfikacja kilku tokenów czyta więcej ekspertów.
- **Draft nie jest darmowy**: sam jest małym MoE z 3 blokami; jego przebieg wlicza się w te ~15 ms na token.
- **Kwantyzacja celu**: draft trenowano na pełnej precyzji, mój cel to IQ3_XXS. Stany ukryte różnią się nieco → akceptacja niższa niż w publikacjach
  (autorzy DSpark podają +60–85 % dla V4; ja miałem średnio +50 % przy podziale warstwami).
- **Koszt prefillu**: draft musi „przeczytać” cały prompt, bo potrzebuje stanów ukrytych z każdej pozycji — prefill spada o ~25–50 % (patrz plik 02).

---

## 5. Podział tensorowy (`--split-mode tensor`)

Dwa sposoby rozłożenia jednego modelu na wiele kart:

```
PODZIAŁ WARSTWAMI (layer, domyślny)         PODZIAŁ TENSOROWY (tensor, eksperymentalny)
  karta 0: warstwy  0–10*  ─┐                  każda warstwa rozcięta na 4 części
  karta 1: warstwy 11–21    ├─ token idzie     karta 0: ¼ każdej warstwy ┐
  karta 2: warstwy 22–32    │  po kolei        karta 1: ¼ każdej warstwy ├─ wszystkie 4 liczą
  karta 3: warstwy 33–42   ─┘  (potok)          karta 2: ¼ każdej warstwy │  ten sam token naraz,
                                                karta 3: ¼ każdej warstwy ┘  wyniki sumowane (all-reduce)
  w danej chwili pracuje 1 karta               pracują wszystkie 4 — 4× więcej przepustowości pamięci
  (*numery warstw orientacyjne)
  mało komunikacji między kartami              dużo komunikacji: po każdej warstwie karty wymieniają wyniki
```

- **Zysk:** każdy token czyta wagi ze **wszystkich czterech pamięci jednocześnie**. U mnie: bez draftu 25,2 → 29,1 tok/s (+15 %), a **z draftem 37,9 → 46–50 tok/s** —
  oba mechanizmy się mnożą, bo szybszy krok sprawia, że weryfikacja większej partii jest relatywnie tańsza.
- **Koszt:** komunikacja. Po każdej warstwie wyniki trzeba zsumować (*all-reduce*) przez PCIe (u mnie karty 1 i 3 są na x4). W logu widzę
  `internal AllReduce init failed (n_devices != 2?); falling back to meta-backend butterfly` — czyli przy 4 kartach działa ogólna, wolniejsza ścieżka;
  biblioteka RCCL albo bezpośredni dostęp między kartami (P2P) mogłyby to poprawić — **nie testowałem** (patrz plik 02, „Co dalej”).
- **Ograniczenia w llama.cpp (październik 2026)** — każde z nich mnie ugryzło:
  - wymaga `-fa on` i **nieskwantyzowanego KV** (`-ctk f16 -ctv f16`) — więc nie wolno oszczędzać pamięci kwantyzacją KV;
  - **nie działa auto-dopasowanie** (`--fit`): musisz sam dobrać `--ctx-size`, `--parallel`, `--ubatch-size`;
  - **nierówny `--tensor-split` zawiesza ładowanie** (u mnie `0.85,1,1,1` → brak odpowiedzi przez 300 s); równy podział działa;
  - nie każda architektura jest obsługiwana (lista w `docs/multi-gpu.md`); DeepSeek V4 jest na liście, a nowy kod ma osobną obsługę jego stanów
    kompresowanej uwagi. Na starej wersji llama.cpp trybu tensorowego nie testowałem;
  - oznaczony jako **eksperymentalny** — przed wdrożeniem sprawdź jakość (patrz README).

---

## 6. Słowniczek

| Pojęcie | Znaczenie |
|---|---|
| draft | „zgadywacz”: mały model/głowica proponująca tokeny |
| model docelowy | duży model, który zatwierdza tokeny |
| acceptance, `mean len` | jaka część propozycji przeszła; ile tokenów na krok (§2) |
| prefill | przetwarzanie promptu (równolegle, szybkie) — przeciwieństwo generowania |
| MTP / NextN | *Multi-Token Prediction* — wbudowana głowica przewidująca kolejne tokeny |
| layer split / tensor split | podział warstwami (potok) / podział każdej warstwy na karty (§5) |
| all-reduce | zsumowanie wyników częściowych ze wszystkich kart po każdej warstwie |
| slot | równoległa „linia” obsługi jednego żądania w `llama-server` (`--parallel`) |
| ubatch | mikro-wsad przy prefillu; od niego zależą bufory obliczeniowe (pamięć) i szybkość prefillu |
