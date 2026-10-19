# 03 · Procedura: przyspieszanie nowego modelu (speculative decoding + podział tensorowy)

Instrukcja dla każdego modelu, który pobiorę w przyszłości. Teoria: [01-JAK-TO-DZIALA.md](01-JAK-TO-DZIALA.md) — **przeczytaj §1–§2 raz**, a procedura stanie się oczywista;
przykład wykonania: [02-WDROZENIE-DEEPSEEK.md](02-WDROZENIE-DEEPSEEK.md). Narzędzia: [narzedzia/](narzedzia/README.md) (sprawdzone na DeepSeek-V4-Flash 19 X 2026).

**Zasada naczelna:** speculative decoding **nie zmienia jakości** (duży model zatwierdza każdy token), więc ryzykiem jest tylko **czas** (prefill, VRAM, złożoność), nie poprawność. Dlatego procedura kończy się *pomiarem i decyzją*, nie wiarą.

---

## Krok 0 · Czy w ogóle warto? (2 minuty)

Spekulacja przyspiesza **generowanie**, nie czytanie promptu (prefill bywa wręcz wolniejszy — u DeepSeeka ~2×). Warto, gdy:

| Twoje zadanie | Decyzja |
|---|---|
| agent: wywołania narzędzi, JSON, kod, krótkie odpowiedzi względem kontekstu | **TAK** — tu zysk największy (DeepSeek: do 2×) |
| tłumaczenie, rozmowa, długie odpowiedzi | **TAK** (DeepSeek: +40–45 %) |
| tekst swobodny/kreatywny | ostrożnie — zysk ~0 do +25 % |
| streszczanie wielkich dokumentów (dużo czytam, mało piszę) | **NIE** — zostaw model bez draftu |
| 4+ równoległych agentów na jednym modelu | **zysk ≈ 0** (GPU już nasycone batchingiem) — sprawdź `bench_conc.py` |

Modele **gęste** (np. 32B) powinny zyskiwać *więcej* niż MoE (weryfikacja kilku tokenów kosztuje tam prawie tyle co jednego); **MoE** — mniej (kilka tokenów aktywuje więcej ekspertów). To wniosek z mechaniki, **nie** z pomiaru: modeli gęstych tą metodą nie mierzyłem.

---

## Krok 0,5 · Czy masz dość nowy llama.cpp?

Speculative decoding i podział tensorowy rozwijają się z tygodnia na tydzień (u mnie: 499 commitów różnicy w 3 tygodnie). **Zanim zaczniesz**, sprawdź:

```bash
cd ~/llama.cpp && git fetch origin && git rev-list --count HEAD..origin/master      # ile commitów za Tobą
./build/bin/llama-server --help | grep -E "spec-type|split-mode"                      # co umie Twoja wersja
```

Nowy llama.cpp buduj **w osobnym katalogu**, nie nadpisując działającego (z pinem pełnego SHA; szczegóły i polecenia: [02, sekcja 4](02-WDROZENIE-DEEPSEEK.md)).
Wpisy `llama-swap` mogą wskazywać dowolny plik binarny, więc stary i nowy działają obok siebie, a wracasz zmieniając jedną ścieżkę.

---

## Krok 1 · Zmierz punkt odniesienia

Dodaj model do `llama-swap` normalnie (jak dotąd), a potem:

```bash
cd narzedzia
python3 bench_spec.py NAZWA_MODELU_Z_CONFIGU results-baseline.json      # ~3 min
```

Zapisz **średnią tok/s** (wiersz `ALL`) — to Twoje 100 %. (U DeepSeeka: 23,5; wynik jest bardzo stabilny, szum <0,3.)
Do pomiarów używaj konfiguracji z `--parallel 1` i tym samym `--ctx-size`, co po zmianie — inaczej porównujesz jabłka z gruszkami.

> 🚦 **Bramka:** masz liczbę „bez draftu” z tej samej konfiguracji, w której będziesz testował draft.

---

## Krok 2 · Ustal, jakie opcje ma ten model

Idź od najtańszej opcji do najdroższej. **Zatrzymaj się na pierwszej, która działa.**

### 2A · Czy sam GGUF ma wbudowaną głowicę MTP/NextN?  (najtańsze: zero pobierania)

```bash
~/spec-dspark/venv/bin/python narzedzia/gguf-inspect.py /sciezka/model-00001-of-0000N.gguf
```

- Widzisz `nextn_predict_layers`/tensory `nextn.*` → **TAK**. Wpis w `llama-swap` dostaje tylko: `--spec-type draft-mtp` (bez `-md`; llama.cpp tworzy kontekst MTP na samym modelu). Idź do Kroku 4.
- Widzisz `>>> BRAK glowicy…` → 2B.

> Uwaga: nie każdy model, którego architektura *w kodzie* wspiera MTP, ma te tensory w Twoim GGUF-ie. Wiele publicznych kwantyzacji **wycina** głowicę (DeepSeek-V4-Flash od Unsloth — wycięta; sprawdzone). Zawsze sprawdź plik, nie architekturę.

### 2B · Czy autor modelu dołączył głowicę w oryginalnym checkpoincie?

```bash
# na HF: config.json modelu bazowego
curl -sL https://huggingface.co/ORG/MODEL/raw/main/config.json | grep -iE "nextn|mtp|dspark|speculat"
# i klucze w indeksie wag
curl -sL https://huggingface.co/ORG/MODEL/raw/main/model.safetensors.index.json | python3 -c "import sys,json; k=json.load(sys.stdin)['weight_map']; print(sorted({x.split('.')[0]+'.'+x.split('.')[1] for x in k if x.startswith('mtp')}))"
```

`num_nextn_predict_layers > 0` albo klucze `mtp.*` ⇒ głowica **jest w checkpoincie**, tylko nie w Twoim GGUF-ie ⇒ **skonwertuj ją** (Krok 3, ścieżka „głowica z checkpointu”).

### 2C · Czy ktoś wytrenował draft pod ten model?

```bash
narzedzia/find-drafts.sh NAZWA-MODELU      # np. Qwen3-30B-A3B, gpt-oss-120b
```

Szuka na HF: `mtp`, `eagle3`, `dflash`, `dspark`, `speculator`, `draft`. To lista **kandydatów** — przed pobraniem sprawdź na karcie: dla jakiej **dokładnie wersji** modelu (np. DeepSeek *0731* ≠ *preview*; acceptance spada, gdy wersja się nie zgadza), ten sam **tokenizer**, czy jest gotowy GGUF.

### 2D · Czy jest mały model z tym samym tokenizerem?

Rodziny modeli mają „młodsze rodzeństwo” (np. Qwen3-0.6B/1.7B dla Qwen3-32B). Zwykły draft (`draft-simple`):

```
-md maly-model-Q8_0.gguf --spec-type draft-simple --spec-draft-n-max 8
```

Wymagania: **identyczny słownik (vocab)** co duży model; najlepiej ta sama generacja/dane treningowe. Mały model jest wolniejszy w zgadywaniu niż wyspecjalizowane głowice, ale działa wszędzie. Dla modeli gęstych bywa to najlepsza opcja.

### 2E · Nic z powyższego → zgadywanie z historii tekstu (zero wag, zero VRAM)

```
--spec-type ngram-mod --spec-ngram-mod-n-match 24 --spec-ngram-mod-n-min 48 --spec-ngram-mod-n-max 64
```

Działa **tylko**, gdy tekst się powtarza: przepisywanie/edycja kodu, streszczanie z cytatami, agent powtarzający zawartość pliku. Dla zwykłego tłumaczenia/rozmowy ≈ 0 (u DeepSeeka dołożenie `ngram-mod` do DSpark nic nie dało). Dokumentacja llama.cpp ostrzega: *„MoE potrzebują długich draftów”*.

> 🚦 **Bramka:** wiesz, którą ścieżką idziesz (MTP w pliku / konwersja głowicy / gotowy draft / mały model / n-gramy).

---

## Krok 3 · Zdobądź plik draftu (jeśli ścieżka tego wymaga)

Środowisko konwertera już jest: `~/spec-dspark/venv` (torch CPU 2.11, numpy, gguf). Jeśli kiedyś znika: `narzedzia/convert-draft-from-hf.sh` zawiera polecenia (jest to **szablon z DSpark-iem DeepSeeka** — podmień nazwę repo i flagę).

| Co konwertujesz | Polecenie (wszystko z `~/llama.cpp`) | Uwagi |
|---|---|---|
| **głowica MTP** z checkpointu | `python convert_hf_to_gguf.py ORG/MODEL --remote --mtp --outtype bf16 --outfile mtp-MODEL.gguf` | `--mtp` = eksport samej głowicy jako osobny draft (`-md`); działa tylko dla architektur z `supports_mtp_export` |
| **EAGLE-3** | `python convert_hf_to_gguf.py ORG/EAGLE3-MODEL --target-model-dir ORG/MODEL --outtype bf16 --outfile eagle3.gguf` | `--target-model-dir` = lokalny katalog z `config.json`+tokenizerem modelu **docelowego** |
| **DFlash / DSpark** | j.w. (dla DeepSeek-V4: dodaj `--dspark`) | DSpark: tylko architektury obsługiwane przez konwerter; sprawdź `grep -n dspark ~/llama.cpp/conversion/*.py` |
| **mały model (`draft-simple`)** | pobierz gotowy GGUF z HF | sprawdź ten sam tokenizer |

Wskazówki z praktyki:

- **`--remote`** pobiera tylko te pliki safetensors, które zawierają potrzebne tensory (DeepSeek: 3 z 48 plików = 11 GB zamiast 167 GB). Ustaw `HF_HOME=~/spec-dspark/hf-cache`, żeby cache nie rozlał się po `~/.cache`.
- Ostrzeżenie *„Transformers does not recognize…”* dla nowych architektur jest nieszkodliwe — konwerter czyta wtedy `config.json`.
- Po konwersji **sprawdź plik**: `gguf-inspect.py plik.gguf` — draft ma architekturę `dflash`/`eagle3`/albo `…` z `nextn`; zapisz `sha256sum` obok pliku.
- Trzymaj draft **obok modelu**: `~/models/<MODEL>-GGUF/<TYP-DRAFTU>/`.
- Draft w bf16/Q8, **nie kwantyzuj go mocniej** (mały, a jakość akceptacji od niego zależy — zalecenie autorów DSpark w llama.cpp).

> 🚦 **Bramka:** plik draftu istnieje, `gguf-inspect.py` go rozpoznaje, masz `sha256`.

---

## Krok 4 · Budżet VRAM — zanim cokolwiek załadujesz

Draft kosztuje **wagi + własny kontekst + bufory**. U DeepSeeka: wagi 10,9 GB (≈2,7 GB/kartę) **plus** ok. 1,3 GB/kartę buforów → razem ~4 GB na każdej z 4 kart ([02, sekcja 3](02-WDROZENIE-DEEPSEEK.md)).

**Reguła:** po załadowaniu **każda karta ma ≥ 1 GB wolnego** (karta z pulpitem — ≥ 0,8 GB). Pamięć rezerwowana jest statycznie przy starcie, więc to, co zmierzysz po starcie, zostaje.

Pomiar bez ryzyka: dodaj *tymczasowy* wpis w `config.yaml` (osobna nazwa), wywołaj go jednym żądaniem, odczytaj:

```bash
rocm-smi --showmeminfo vram | grep -E "Total Used|Total Memory"
```

Gotowa pętla „dodaj wpisy → załaduj → zmierz → przywróć config” to `narzedzia/vram-try.py` (szablon: edytuj ścieżki i słownik `V` na górze).

**Dźwignie, gdy brakuje pamięci** (od najskuteczniejszej, zmierzone na DeepSeeku):

| # | Dźwignia | Efekt (DeepSeek) | Koszt |
|---|---|---|---|
| 1 | `--ubatch-size` 1024 → **512** | **+0,7 GB** na karcie 0, +1,3 GB na pozostałych | prefill −8 % |
| 2 | `--parallel`/`--ctx-size` mniejsze | ~0,1–0,4 GB/kartę na 131k kontekstu (KV DeepSeeka jest tani — u innych modeli KV bywa **dominujący**) | mniej agentów/kontekstu |
| 3 | `--spec-draft-type-k/v q8_0` | ~0 do +0,1 GB | pomijalny |
| 4 | draft na wybranych kartach: `--spec-draft-device`, `-ngld` | zależy | draft może wylądować na wolniejszym łączu |
| 5 | `--tensor-split` | **ostrożnie** — warstwa DeepSeeka ma ~2,4 GB, jedna przesunięta przepełnia sąsiada; `--fit` (domyślnie `on`) może wtedy po cichu zmienić układ | dokładnie mierz tok/s po zmianie |

> 🚦 **Bramka:** model z draftem ładuje się, każda karta ma wolne ≥ 1 GB (0,8 dla karty z pulpitem), tok/s nie spadł względem Kroku 1 na „pustym” zapytaniu.

---

## Krok 5 · Wpis w `llama-swap`

Zawsze **dwa wpisy**: spekulatywny (z aliasami, które już masz) i bliźniak `-nospec` (bez draftu, bez aliasów). Dzięki temu aplikacja wybiera nazwą modelu, a Ty masz awaryjny powrót i punkt odniesienia.

```yaml
  "NAZWA":
    cmd: |
      ${server}
      -m  /ścieżka/model.gguf
      -md /ścieżka/draft.gguf                      # POMIŃ dla draft-mtp na samym modelu i dla ngramów
      --spec-type draft-dspark                      # draft-mtp | draft-eagle3 | draft-dflash | draft-dspark | draft-simple | ngram-mod
      --spec-draft-n-max 3 --spec-draft-p-min 0     # patrz Krok 7
      --spec-draft-type-k q8_0 --spec-draft-type-v q8_0
      -ngl 999 --split-mode layer --tensor-split … --ctx-size … --load-mode dio
      --parallel … --ubatch-size 512
    env: ["HIP_VISIBLE_DEVICES=0,1,2,3"]
    ttl: 600
    aliases: ["…stare aliasy…"]

  "NAZWA-nospec":      # kopia starego wpisu bez --spec-*, bez -md, bez aliasów
    …
```

Przed edycją: `cp ~/.config/llama-swap/config.yaml ~/.config/llama-swap/config.yaml.bak-$(date +%Y%m%d)-przed-spec`.
Pamiętaj: zapis `config.yaml` **przeładowuje llama-swap i zwalnia załadowany model** (wraca na kolejne żądanie, ~40 s) — nie rób tego w trakcie ważnego zadania.

---

## Krok 6 · Pomiar (trzy testy, ~15 min razem)

```bash
cd narzedzia

# (a) jeden strumień, 4 typy zadań × temp. 0 i 1.0, z akceptacją       ~3 min
BENCH_REPS=2 python3 bench_spec.py NAZWA wyniki-spec.json
# (b) 1, 2 i 4 agentów naraz (przepustowość łączna i na strumień)       ~2 min
python3 bench_conc.py NAZWA wyniki-conc-spec.json   &&   python3 bench_conc.py NAZWA-nospec wyniki-conc-nospec.json
# (c) bramka przed wdrożeniem: prefill, 1/2/4 agentów, wolny VRAM po użyciu, zgodność z modelem bez draftu — SZABLON: ścieżki i argumenty na górze pliku
python3 gate-test.py
```

Jak czytać (progi z [01, §2](01-JAK-TO-DZIALA.md)):

- `accept` i `tok/s` per zadanie. **Zadanie, w którym spec < nospec** ⇒ ten typ ruchu kieruj na `-nospec`.
- `bench_conc`: czy zysk przy 1–2 agentach zniknął przy 4? (U DeepSeeka: tak.)
- Szum jednego powtórzenia ≈ ±2 tok/s → decyzje na różnicach < 2 są losowe.
- Pamiętaj, że **tokeny „myślenia” modelu też są liczone** (DeepSeek, Qwen3 w trybie thinking) — to zwykle właściwy obraz Twojego użycia.

> 🚦 **Bramka:** masz 3 zestawy liczb: (a) tok/s na zadaniach, (b) skalowanie z liczbą agentów, (c) prefill i pamięć.

---

## Krok 7 · Strojenie (po jednej zmianie naraz)

Zacznij od wartości startowych, potem szukaj lepszej **jedną zmienną naraz** wg `bench_spec.py`.

| Parametr | Start | Kierunek | Reguła |
|---|---|---|---|
| `--spec-draft-n-max` (ile tokenów proponuje) | MoE: **3** (zmierzone); model gęsty: **5–8** (wartość startowa z dokumentacji llama.cpp — nie mierzyłem modelu gęstego) | w górę, gdy `accept` > 0,85; w dół, gdy proza/tłumaczenie ma niski `mean len` | draft opłaca się, gdy `mean len > (c₀ + c₁·n)/c₀`, gdzie c₀ = koszt zwykłego kroku, c₁ ≈ koszt jednego dodatkowego tokenu w kroku (DeepSeek: 43 ms i 15 ms) |
| `--spec-draft-p-min` (próg pewności; tylko drafty z głowicą pewności, np. DSpark) | 0 | 0,5 jeśli duży `n` i proza traci | za wysoki (≥0,75) odcina za dużo |
| `--spec-type a,b` (kombinacje) | pojedynczy | dodaj `ngram-mod` **tylko** dla zadań z powtórzeniami | dla zwykłego tekstu nic nie daje |
| `--spec-draft-n-min` | 0 | zwykle zostaw | |
| `--ubatch-size` | z Kroku 4 | | zmienia pamięć i prefill |

**Własny wzór kosztu kroku** (zrobisz w 5 minut dla nowego modelu): zmierz tok/s dla `n=3` i `n=5` na zadaniu o wysokiej akceptacji (JSON). Z tych dwóch punktów: `c₁ ≈ (T₅ − T₃)/2`, `c₀ ≈ T₃ − 3·c₁`, gdzie `T = mean_len / tok_per_s` to czas kroku. Potem szukasz `n`, które maksymalizuje `mean_len(n)/(c₀ + c₁·n)` na Twoim ruchu.

---

## Krok 7b · Podział tensorowy (opcjonalny, duży zysk, więcej pułapek)

Przy 2+ kartach spróbuj `--split-mode tensor` — wszystkie karty liczą każdy token naraz ([01, §5](01-JAK-TO-DZIALA.md)). U mnie: 37,9 → 46–50 tok/s z draftem.

**Warunki wstępne** (inaczej błąd przy starcie): `-fa on`, `-ctk f16 -ctv f16` (bez kwantyzacji KV), architektura na liście obsługiwanych (`docs/multi-gpu.md`).
**Brak auto-dopasowania** (`--fit`) — pamięć dobierasz ręcznie.

Kolejność postępowania (każdy krok zmierz `bench_spec.py` i `rocm-smi --showmeminfo vram`):

1. Bez draftu, **równy podział** (nie podawaj `--tensor-split`), `--parallel 1`, kontekst jak w kroku 1. Zapisz tok/s i **czas ładowania** (u mnie 108 s vs 35 s).
2. Dodaj draft. Sprawdź wolny VRAM: cel ≥ 1 GB na kartę (≥ 0,8 GB na karcie z pulpitem).
3. Brakuje pamięci → zmniejsz w tej kolejności: `--ubatch-size` (1024→512), `--ctx-size`, `--parallel`. **Nie** używaj nierównego `--tensor-split` (zawiesza ładowanie) ani kwantyzacji KV (zabronione).
4. Dopiero teraz stroiń `--spec-draft-n-max`: stałe kosztu kroku w trybie tensorowym są inne niż w trybie warstw.
5. Opcjonalnie: RCCL (`-DGGML_HIP_RCCL=ON`) i `GGML_CUDA_P2P=1` — **po każdej zmianie sprawdź poprawność wyjścia**, bo P2P potrafi je psuć na części płyt.

**Jakość w trybie tensorowym:** zmienia się kolejność sum zmiennoprzecinkowych, więc wyniki przy temp. 0 przestają być identyczne z trybem warstw (u mnie 0/4). Porównanie tekstów nic nie dowodzi —
**uruchom benchmark jakości** na tym samym zestawie, którym mierzyłeś model przed zmianą ([README](README.md#jakość-czy-model-nie-zgłupiał)). Zmiana w konfiguracji `llama-swap` **zwalnia załadowany model**, więc nie rób jej w trakcie takiego przebiegu.

---

## Krok 8 · Decyzja (kryteria zapisz PRZED pomiarem)

**Zostaw spec**, gdy wszystkie:

1. średnia z Twoich typowych zadań **≥ +20 %** vs Krok 1;
2. **żadne typowe zadanie** nie jest wolniejsze od bazowego o więcej niż 5 % (inaczej: route na `-nospec`);
3. każda karta ≥ 1 GB wolnego (karta z pulpitem ≥ 0,8 GB) **po realnym użyciu** (u mnie wolny VRAM spadł o ~0,3 GB po testach);
4. strata prefillu akceptowalna dla Twoich aplikacji (policz: `nowe_tokeny_promptu/prefill + odpowiedź/tok_s` dla typowego żądania, z i bez);
5. odpowiedzi poprawne funkcjonalnie (wywołanie narzędzia → poprawny JSON; tłumaczenie sensowne);
6. **benchmark jakości bez regresji** względem pomiaru sprzed zmiany (obowiązkowe przy trybie tensorowym).

W przeciwnym razie: wróć do `config.yaml.bak-…`, a wpis `-nospec` zostaje.

---

## Krok 9 · Udokumentuj (10 minut — przyszły Ty będzie wdzięczny)

Do pliku `SPECULATIVE-DECODING-<model>.md` (wzór: dokument DeepSeeka) wpisz:

1. **Co** (typ spec, skąd draft, rewizja/sha) i **czemu** ta ścieżka;
2. **Polecenia** konwersji i wpisy `config.yaml`;
3. **Tabele**: tok/s per zadanie przed/po, tuning, skalowanie agentów, prefill, VRAM;
4. **Ograniczenia** (kiedy kierować na `-nospec`);
5. **Jak cofnąć**.

I dopisz jedną linię w komentarzu wpisu w `config.yaml` (żeby `config.yaml` sam objaśniał, co robi).

---

## Wskazówki dla aplikacji agentowych (zbiorczo)

- **Temperatura 0–0,3 w kliencie** dla wywołań narzędzi/JSON: wyższa akceptacja i bardziej stabilne wyniki. Serwerowe `--temp 1.0` to tylko wartość domyślna — klient może ją nadpisać w żądaniu.
- **Kieruj ruch nazwą modelu:** agent „interaktywny” → wpis ze spec; zadania wsadowe z ogromnymi promptami → `-nospec`.
- **Liczba równoległych agentów:** spec daje najwięcej przy 1–2. Jeśli aplikacja i tak odpala 4+ agentów naraz, zysk jest zerowy — lepiej oszczędzić VRAM i zostawić `-nospec`.
- **Duże, powtarzane prompty** (system prompt, kontekst repozytorium): llama.cpp trzyma cache promptu w slocie — drugi i kolejne tury czytają tylko nowy fragment, więc strata prefillu spekulacji boli rzadziej, niż sugerują surowe liczby.
- **Limit `max_tokens` a myślenie:** modele „myślące” zużywają limit na `reasoning_content` — przy zbyt małym limicie dostaniesz pustą odpowiedź (to nie błąd spec).
- **Nie mierz tylko `tok/s` serwera** — mierz czas całej tury agenta (prefill + generowanie + narzędzia). Spec skraca tylko generowanie.

---

## Ściąga: narzędzia

| Narzędzie | Do czego | Przykład |
|---|---|---|
| `gguf-inspect.py` | czy GGUF ma głowicę MTP / czym jest plik | `~/spec-dspark/venv/bin/python gguf-inspect.py model-00001-of-0000N.gguf` |
| `find-drafts.sh` | szukanie gotowych draftów na HF | `./find-drafts.sh Qwen3-30B-A3B` |
| `convert-draft-from-hf.sh` | szablon konwersji draftu z checkpointu HF | patrz Krok 3 |
| `bench_spec.py` | tok/s i akceptacja, 1 strumień | `BENCH_REPS=2 python3 bench_spec.py NAZWA out.json` |
| `vram-try.py` | wolny VRAM na kartach dla wielu wariantów ustawień (szablon) | edytuj `V` na górze |
| `bench_conc.py` | 1/2/4 agentów naraz | `python3 bench_conc.py NAZWA out.json` |
| `gate-test.py` | bramka: prefill, agenci, VRAM po użyciu, zgodność z bazą (szablon) | edytuj ścieżki na górze |
| `dschat.py` | czat w terminalu z licznikiem tok/s | `python3 dschat.py "pytanie"` |
| `translate_doc.py`, `verify_translation.py` | lokalne tłumaczenie dokumentu Markdown + mechaniczna weryfikacja | patrz [05](05-ODNIESIENIE-LLAMA-CPP-SPECULATIVE.md) |
| log żywy | akceptacja w czasie rzeczywistym | `curl -sN localhost:8080/logs/stream/upstream \| grep "draft acceptance"` |
