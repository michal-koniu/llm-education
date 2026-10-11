# Część 2 — Wnętrze modelu: poczuj, co się dzieje pod spodem

**Poziom: ⭐⭐** · Wymaga: część 1 (`PODSTAWY-LOKALNYCH-MODELI.md`) · Czas: ~4 h

> **Po co ten rozdział.** Część 1 nauczyła Cię **rozmawiać** z modelem. Ten rozdział uczy
> **czuć** model. Po nim wiesz, czym naprawdę jest „token", dlaczego drugi token generuje się
> 50× szybciej niż pierwszy, dlaczego ten sam prompt daje dwie różne odpowiedzi i jak model
> mierzy, że dwa zdania „znaczą to samo".
>
> **To nie jest teoria dla teorii.** Każde pojęcie tutaj wraca w częściach 3–7 jako konkretna
> decyzja inżynierska: token = budżet, próbkowanie = determinizm narzędzi, KV-cache = jedyna
> największa optymalizacja offline, embedding = fundament pamięci agenta.

```bash
source $LLMEDU/rig-env.sh   # jeśli nie masz — patrz 00-KURS-INDEKS.md, sekcja "Konwencje"
```

---

## Spis treści

| § | Temat | Kluczowa intuicja |
| :-- | :-- | :-- |
| [1](#1-token--zobacz-go-własnymi-oczami) | **Token** | model nie widzi liter; widzi liczby, i po polsku widzi ich więcej |
| [2](#2-co-model-naprawdę-zwraca--logity) | **Logity** | model nie zwraca słowa, zwraca **rozkład prawdopodobieństwa nad całym słownikiem** |
| [3](#3-próbkowanie--od-rozkładu-do-słowa) | **Próbkowanie** | `temperature`, `top-k`, `top-p`, `min-p` — to Ty wybierasz słowo, nie model |
| [4](#4-determinizm--dlaczego-ten-sam-prompt-daje-dwie-odpowiedzi) | **Determinizm** | ziarno, greedy, i dlaczego „temperatura 0" nie wystarcza |
| [5](#5-kv-cache--dlaczego-drugi-token-jest-darmowy) | **KV-cache** | prefill vs dekodowanie; zmierz to sam |
| [6](#6-kontekst--co-się-dzieje-na-granicy) | **Kontekst** | ile pamięci zjada, co się dzieje przy przepełnieniu |
| [7](#7-embeddingi--jak-model-mierzy-znaczenie) | **Embeddingi** | tekst → wektor; policz podobieństwo ręcznie |
| [8](#8-kwantyzacja--zmierz-stratę-nie-zgaduj) | **Kwantyzacja** | perplexity jako miara; Q4 vs Q8 na Twoim żelazie |
| [9](#9-ćwiczenie--własna-pętla-generowania) | **Ćwiczenie** | wygeneruj tekst token po tokenie, ręcznie |

---

## 1. Token — zobacz go własnymi oczami

Model nie widzi liter ani słów. Widzi **liczby całkowite** — indeksy w słowniku
(ang. *vocabulary*). Tokenizer to słownik + reguły dzielenia tekstu.

### 1.1 Pierwszy pomiar

```bash
echo -n "Sprawozdanie finansowe za rok obrotowy 2025" | \
  $LB/llama-tokenize -m $BIELIK --stdin
```

Wyjście to lista par `id → 'fragment'`. Przeczytaj ją uważnie — **zobaczysz, że „Sprawozdanie"
to nie jeden token.** To kilka fragmentów, np. `Spraw` + `ozdanie`, albo jeszcze drobniej.

🔧 **Co dokładnie robisz:** `--stdin` każe czytać tekst ze standardowego wejścia (dzięki temu
nie walczysz z cudzysłowami w shellu), `-m` wskazuje model — **bo tokenizer jest częścią pliku
GGUF**, nie osobnym programem. Dwa różne modele potną ten sam tekst inaczej.

### 1.2 Policz sam: polski jest drogi

```bash
# Ten sam sens, dwa języki
echo -n "The financial statement for fiscal year 2025" | $LB/llama-tokenize -m $BIELIK --stdin | wc -l
echo -n "Sprawozdanie finansowe za rok obrotowy 2025" | $LB/llama-tokenize -m $BIELIK --stdin | wc -l
```

Polski wyjdzie **wyraźnie dłuższy**. Dlaczego: tokenizery są trenowane głównie na angielskim,
więc angielskie słowa mają własne tokeny, a polskie są składane z kawałków.

💡 **Dlaczego to Cię obchodzi — trzy razy w tym kursie:**

| Gdzie | Konsekwencja |
| :-- | :-- |
| **Kontekst** (§6) | polski dokument zajmuje ~1,5–2× więcej kontekstu niż angielski o tej samej treści |
| **Koszt** (część 8) | przy Claude API płacisz **za token, nie za znak** — polski jest dosłownie droższy |
| **Szybkość** (część 7) | dekodowanie liczy się w tokenach/s, więc **ta sama odpowiedź po polsku powstaje dłużej** |

### 1.3 Ten sam tekst, różne modele

```bash
for MODEL in $BIELIK $OSS20 $QWEN32; do
  N=$(echo -n "Faktura korygująca nr 12/2025 na kwotę 4 320,50 zł" | \
      $LB/llama-tokenize -m $MODEL --stdin 2>/dev/null | wc -l)
  echo "$N tokenów  $(basename $MODEL)"
done
```

⚠️ **Pułapka P20 (nowa): nie licz tokenów jednego modelu miarką drugiego.**
Jeśli w agencie budżetujesz kontekst, **musisz liczyć tokenizerem tego modelu, którego
realnie używasz.** Przełączysz model w `llama-swap` i wszystkie Twoje budżety przestają być
prawdziwe. W części 5 zbudujemy licznik, który bierze model z konfiguracji.

### 1.4 Jak wygląda słownik

```bash
$LB/llama-tokenize -m $BIELIK --stdin <<< "test" 2>&1 | head -3
```

⚠️ **Ten build `llama-cli` nie wypisuje już `n_vocab`/`BOS`/`EOS` przy `-n 0`.**
Starsze wersje llama.cpp drukowały pełny zrzut metadanych modelu na starcie; ten build
(commit `987498f`) go nie ma — sprawdzone na żywo, `grep` po tych polach nie znajduje
nic, niezależnie od poziomu `-v`/`-lv`. Metadane są w samym pliku GGUF, więc czytamy je
stamtąd wprost — **bez żadnej zależności** (bez `numpy`, bez pakietu `gguf`):

```bash
cat > $KURS/gguf_meta.py <<'EOF'
#!/usr/bin/env python3
"""Minimalny czytnik metadanych GGUF - bez zaleznosci.
Uzycie: python3 gguf_meta.py <plik.gguf> [klucz1 klucz2 ...]"""
import struct, sys

_SIMPLE = {
    0: ("B", 1), 1: ("b", 1), 2: ("H", 2), 3: ("h", 2),
    4: ("I", 4), 5: ("i", 4), 6: ("f", 4), 7: ("?", 1),
    10: ("Q", 8), 11: ("q", 8), 12: ("d", 8),
}

def _read_str(f):
    (n,) = struct.unpack("<Q", f.read(8))
    return f.read(n).decode("utf-8", "replace")

def _read_value(f, vtype):
    if vtype == 8:                       # string
        return _read_str(f)
    if vtype == 9:                       # array
        (elem_t,) = struct.unpack("<I", f.read(4))
        (n,) = struct.unpack("<Q", f.read(8))
        return [_read_value(f, elem_t) for _ in range(n)]
    fmt, size = _SIMPLE[vtype]
    return struct.unpack("<" + fmt, f.read(size))[0]

def wczytaj_metadane(sciezka: str) -> dict:
    with open(sciezka, "rb") as f:
        magic = f.read(4)
        if magic != b"GGUF":
            sys.exit(f"To nie jest plik GGUF (magic={magic!r})")
        struct.unpack("<I", f.read(4))               # wersja formatu
        (n_tensors,) = struct.unpack("<Q", f.read(8))
        (n_kv,) = struct.unpack("<Q", f.read(8))
        meta = {}
        for _ in range(n_kv):
            klucz = _read_str(f)
            (vtype,) = struct.unpack("<I", f.read(4))
            meta[klucz] = _read_value(f, vtype)
        return meta

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    m = wczytaj_metadane(sys.argv[1])
    if len(sys.argv) > 2:
        for k in sys.argv[2:]:
            print(f"{k} = {m.get(k, '(brak)')}")
    else:
        arch = m.get("general.architecture", "?")
        for pole in ("context_length", "vocab_size", "block_count",
                     "attention.head_count", "attention.head_count_kv",
                     "embedding_length"):
            print(f"{arch}.{pole} = {m.get(f'{arch}.{pole}', '(brak)')}")
        print(f"tokenizer.ggml.bos_token_id = {m.get('tokenizer.ggml.bos_token_id', '(brak)')}")
        print(f"tokenizer.ggml.eos_token_id = {m.get('tokenizer.ggml.eos_token_id', '(brak)')}")
EOF
python3 $KURS/gguf_meta.py $BIELIK
```

Oczekiwane (Bielik-11B, zmierzone na tej maszynie):

```
bielik.context_length = 32768
bielik.vocab_size = 32128
bielik.block_count = 50
bielik.attention.head_count = 32
bielik.attention.head_count_kv = 8
bielik.embedding_length = 4096
tokenizer.ggml.bos_token_id = 1
tokenizer.ggml.eos_token_id = 32001
```

🔧 **Format GGUF w skrócie, żeby ten skrypt nie był magią:** nagłówek (`GGUF` + wersja +
liczba tensorów + liczba par klucz-wartość), potem same pary — klucz jako string,
znacznik typu (uint32), wartość zakodowana wg tego typu. `ARRAY` (typ 9) niesie własny
typ elementu i długość. To wystarcza, żeby przejść przez cały plik bez rozpakowywania
samych wag.

Zapisz sobie `vocab_size` — wraca w §2 jako **długość wektora logitów**.

---

## 2. Co model naprawdę zwraca — logity

To jest najważniejszy akapit w tym rozdziale.

> **Model nie generuje słowa. Model generuje liczbę dla KAŻDEGO tokenu w słowniku.**

Jeden przebieg (*forward pass*) to:

```
   [twoje tokeny]  ──►  [ sieć: mnożenia macierzy ]  ──►  wektor długości n_vocab
    np. 12 liczb                                           np. 128 000 liczb
                                                           ("logity")
```

Każda liczba mówi: *„jak bardzo ten token pasuje jako następny"*. Nieznormalizowane.
Potem funkcja **softmax** zamienia je w prawdopodobieństwa sumujące się do 1.

### 2.1 Zobacz rozkład na własne oczy

`llama-server` potrafi zwrócić logprawdopodobieństwa. Uruchom serwer:

```bash
# Zwolnij karty, jeśli coś na nich wisi
pkill -f llama-server; sleep 2

$LB/llama-server -m $BIELIK \
  --host 127.0.0.1 --port 8081 \
  -ngl 999 -c 4096 --no-warmup &
sleep 25   # model musi się wczytać — 11,9 GB
```

🔧 **Flagi:** `-ngl 999` = wszystkie warstwy na GPU (999 to „tyle, ile jest"),
`-c 4096` = okno kontekstu 4096 tokenów, `--no-warmup` = nie rozgrzewaj (szybszy start).

Teraz zapytaj o rozkład:

```bash
curl -s http://127.0.0.1:8081/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Stolicą Polski jest",
    "max_tokens": 1,
    "temperature": 0,
    "n_probs": 10
  }' | python3 -m json.tool | head -60
```

⚠️ **Pole nazywa się inaczej, niż można by zgadywać.** W tym builcie `/v1/completions`
zwraca rozkład pod `choices[0]["logprobs"]["content"][0]["top_logprobs"]` — **stylem
OpenAI**, nie natywnym `completion_probabilities`/`top_probs` ze starszych wersji
llama.cpp. Sprawdzone na żywo curl-em. Szukaj tej ścieżki w JSON-ie z `python3 -m json.tool`.

⚠️ **I druga pułapka: to są `logprob`, nie `prob`.** Każdy wpis niesie **logarytm
naturalny** prawdopodobieństwa (liczba ujemna, bliższa zeru = pewniejszy token), nie samo
prawdopodobieństwo. Żeby dostać `p` z zakresu 0–1, trzeba policzyć `math.exp(logprob)`.
**To jest surowy rozkład modelu** — dziesięć najbardziej prawdopodobnych następnych
tokenów z ich logprawdopodobieństwami.

### 2.2 Czytaj go jak inżynier

```bash
curl -s http://127.0.0.1:8081/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Stolicą Polski jest","max_tokens":1,"temperature":0,"n_probs":10}' \
| python3 -c '
import json,math,sys
d=json.load(sys.stdin)
logprobs = (d.get("choices") or [{}])[0].get("logprobs") or {}
content = logprobs.get("content") or []
if not content:
    print("brak logprobs.content — sprawdz, czy podales n_probs>0"); sys.exit()
for t in content[0].get("top_logprobs", []):
    p   = math.exp(t.get("logprob", -999))
    tok = t.get("token", "")
    bar = "#" * int(p*50)
    print(f"{p:6.3f}  {bar:<50} {tok!r}")
'
```

Zobaczysz histogram. **To jest „pewność" modelu** — i to jest coś, co możesz czytać
programowo.

💡 **Praktyczne zastosowanie, którego nie ma w tutorialach.** Rozkład = miara niepewności.
Jeśli najwyższe prawdopodobieństwo to 0,98 — model wie. Jeśli 0,21 i cztery podobne obok —
model zgaduje. **W agencie do czytania faktur to jest Twój sygnał „wyślij do człowieka".**
Wracamy do tego w części 3 (§ewaluacja) i części 5 (§eskalacja).

### 2.3 Zadanie: znajdź, gdzie model jest niepewny

```bash
for P in "Stolicą Polski jest" "Stawka VAT na książki w Polsce wynosi" "Prezesem NBP w 2025 roku był"; do
  echo "=== $P"
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d "{\"prompt\":\"$P\",\"max_tokens\":1,\"temperature\":0,\"n_probs\":5}" \
  | python3 -c '
import json,math,sys
d=json.load(sys.stdin)
content=((d.get("choices") or [{}])[0].get("logprobs") or {}).get("content") or [{}]
tp=content[0].get("top_logprobs", [])
if tp:
    p=math.exp(tp[0].get("logprob",-999))
    print(f"  najwyzsze p={p:.3f}  -> {tp[0].get(\"token\",\"\")!r}")
'
done
```

Trzecie pytanie powinno mieć **wyraźnie niższą pewność**. To jest halucynacja w momencie
narodzin — widzisz ją jako liczbę, zanim stanie się zdaniem.

---

## 3. Próbkowanie — od rozkładu do słowa

Masz rozkład. Trzeba wybrać jeden token. **Ta decyzja nie należy do modelu — należy do Ciebie.**

```
      rozkład (n_vocab liczb)
              │
              ├─ temperature   → wypłaszcz / zaostrz rozkład
              ├─ top-k         → zostaw K najlepszych
              ├─ top-p         → zostaw tyle, by suma p ≥ P
              ├─ min-p         → odetnij wszystko poniżej (min_p × p_max)
              ├─ repeat penalty→ obniż tokeny, które już były
              │
              ▼
        losuj jeden  (albo weź najlepszy = greedy)
```

### 3.1 Co robi każdy parametr

| Parametr | Co robi z rozkładem | Kiedy używać |
| :-- | :-- | :-- |
| **`temperature`** | dzieli logity przez T. `T<1` zaostrza (pewniejsze), `T>1` wypłaszcza (kreatywniejsze), **`T=0` = zawsze najlepszy** | `0` do zadań precyzyjnych, `0,7` do pisania |
| **`top_k`** | zostawia tylko K najlepszych tokenów | `40` typowo; `1` = greedy |
| **`top_p`** (nucleus) | zostawia najmniejszy zbiór, którego suma p ≥ P | `0,9`–`0,95` typowo |
| **`min_p`** | odcina tokeny słabsze niż `min_p × p_najlepszego` | **lepszy niż `top_p`** — adaptuje się do pewności modelu; `0,05` |
| **`repeat_penalty`** | karze tokeny z ostatnich N | `1,1` przeciw zapętleniu |

💡 **Najważniejsza intuicja o `min_p`.** `top_p` zawsze zostawia „jakiś" ogon, nawet gdy model
jest bardzo pewny. `min_p` jest **relatywny do szczytu**: gdy model jest pewny (p=0,95),
odcina prawie wszystko; gdy niepewny (p=0,2), zostawia więcej opcji. Dla zadań
precyzyjnych `min_p` ≫ `top_p`.

### 3.2 Poczuj temperaturę

```bash
for T in 0 0.3 0.8 1.5; do
  echo "=== temperature=$T"
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d "{\"prompt\":\"Opisz jednym zdaniem, czym jest faktura VAT:\",\"max_tokens\":40,\"temperature\":$T,\"seed\":42}" \
  | python3 -c 'import json,sys; print("  "+json.load(sys.stdin)["choices"][0]["text"].strip().replace(chr(10)," "))'
done
```

Przy `T=0` dostaniesz odpowiedź poprawną i nudną. Przy `T=1.5` — coraz bardziej dziwną.
**Uruchom to kilka razy** i zobacz, że `T=0` daje zawsze to samo, a `T=1.5` — nigdy.

### 3.3 To samo dla `min_p` — zobacz, dlaczego jest lepszy

```bash
for MP in 0.0 0.05 0.3; do
  echo "=== min_p=$MP (temperature=1.0)"
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d "{\"prompt\":\"Stawki VAT w Polsce to:\",\"max_tokens\":50,\"temperature\":1.0,\"min_p\":$MP,\"seed\":7}" \
  | python3 -c 'import json,sys; print("  "+json.load(sys.stdin)["choices"][0]["text"].strip().replace(chr(10)," "))'
done
```

`min_p=0.3` przy `temperature=1.0` da odpowiedź prawie tak stabilną jak `temperature=0`,
ale bez sztywności. **To jest ustawienie, którego chcesz do ekstrakcji danych.**

### 3.4 ⚠️ Pułapka P21 (nowa): próbkowanie to nie „styl", to niezawodność

Kiedy w części 5 model będzie wywoływał narzędzia, **każdy losowy token to szansa na
zepsuty JSON**. Dla ścieżek narzędziowych:

```
temperature = 0      ← albo top_k = 1
repeat_penalty = 1.0 ← kara za powtórzenia psuje JSON (nawiasy się powtarzają!)
```

⛔ **`repeat_penalty > 1.0` przy generowaniu JSON-a jest błędem.** JSON *musi* powtarzać
`"`, `{`, `,`. Kara za powtórzenia aktywnie psuje strukturę. Zapamiętaj to — to jedna
z najczęstszych, najtrudniejszych do zdiagnozowania awarii lokalnych agentów.

---

## 4. Determinizm — dlaczego ten sam prompt daje dwie odpowiedzi

### 4.1 Ziarno losowości

```bash
# Dwa razy to samo ziarno → identyczny wynik
for i in 1 2; do
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d '{"prompt":"Trzy rodzaje kosztów:","max_tokens":30,"temperature":0.8,"seed":1234}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["choices"][0]["text"].strip()[:70])'
done

echo "--- bez ziarna (seed=-1) ---"
for i in 1 2; do
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d '{"prompt":"Trzy rodzaje kosztów:","max_tokens":30,"temperature":0.8,"seed":-1}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["choices"][0]["text"].strip()[:70])'
done
```

### 4.2 ⚠️ Ale `temperature=0` NIE gwarantuje identycznych wyników

To zaskakuje wszystkich. Przy `temperature=0` wybór tokenu jest deterministyczny — **ale
same logity mogą się minimalnie różnić**, bo:

1. **Kolejność operacji zmiennoprzecinkowych na GPU nie jest gwarantowana.** Sumowanie
   równoległe daje wyniki różniące się na ostatnich bitach.
2. **Rozmiar wsadu (batch) zmienia ścieżkę obliczeń.** Ten sam prompt w innym batchu →
   inne zaokrąglenia.
3. Jeśli dwa tokeny mają prawie identyczne logity, **ta różnica na ostatnim bicie decyduje
   o wyborze** — i odpowiedź rozjeżdża się od tego miejsca.

💡 **Co z tego wynika praktycznie:** nie buduj testów, które porównują odpowiedź modelu
znak w znak. Testuj **właściwości** (czy JSON się parsuje, czy pole `kwota` jest liczbą,
czy wartość mieści się w zakresie). Tym się zajmiemy w części 3.

---

## 5. KV-cache — dlaczego drugi token jest darmowy

To jest **najważniejszy mechanizm wydajnościowy** w całym lokalnym LLM. Bez zrozumienia go
nie da się optymalizować (część 7).

### 5.1 Mechanizm

Generowanie ma **dwie zupełnie różne fazy**:

```
FAZA 1: PREFILL  (czytanie Twojego promptu)
   ┌───────────────────────────────────────────────┐
   │ wszystkie tokeny promptu przetwarzane NARAZ   │
   │ → GPU liczy równolegle, pełne wykorzystanie   │
   │ → ograniczenie: MOC OBLICZENIOWA (FLOPS)      │
   │ → szybko: tysiące tokenów/s                   │
   └───────────────────────────────────────────────┘
                        │ zapisuje K i V każdej warstwy
                        ▼
                  [ KV-CACHE w VRAM ]
                        │ czyta przy każdym kroku
                        ▼
FAZA 2: DEKODOWANIE  (pisanie odpowiedzi)
   ┌───────────────────────────────────────────────┐
   │ JEDEN token na raz, każdy zależy od poprzedn. │
   │ → GPU prawie bezczynne, czeka na pamięć       │
   │ → ograniczenie: PRZEPUSTOWOŚĆ PAMIĘCI         │
   │ → wolno: dziesiątki tokenów/s                 │
   └───────────────────────────────────────────────┘
```

**Co jest w KV-cache:** dla każdego już przetworzonego tokenu, w każdej warstwie, model
zapamiętał jego klucz (K) i wartość (V) z mechanizmu uwagi. Gdyby ich nie trzymał, każdy
nowy token wymagałby przeliczenia całej historii od nowa — generowanie 500 tokenów
kosztowałoby 500 pełnych prefilli.

### 5.2 Zmierz obie fazy

```bash
curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
  -d '{"prompt":"Wyjaśnij w trzech zdaniach, czym jest amortyzacja:","max_tokens":150,"temperature":0}' \
| python3 -c '
import json,sys
d=json.load(sys.stdin)
t=d.get("timings",{})
print(f"PREFILL:     {t.get(\"prompt_n\",0):5d} tok w {t.get(\"prompt_ms\",0):8.1f} ms  = {t.get(\"prompt_per_second\",0):8.1f} tok/s")
print(f"DEKODOWANIE: {t.get(\"predicted_n\",0):5d} tok w {t.get(\"predicted_ms\",0):8.1f} ms  = {t.get(\"predicted_per_second\",0):8.1f} tok/s")
pm=t.get("prompt_per_second",0); dm=t.get("predicted_per_second",1)
if dm: print(f"\nPrefill jest {pm/dm:.0f}x szybszy na token niz dekodowanie.")
print(f"\nTTFT (czas do pierwszego tokenu) ~= {t.get(\"prompt_ms\",0):.0f} ms")
'
```

**Zapisz te dwie liczby.** Różnica będzie 20–100×. To nie jest ciekawostka — to jest powód,
dla którego:

| Obserwacja | Wynika z |
| :-- | :-- |
| długi prompt kosztuje mało czasu | prefill jest równoległy |
| długa odpowiedź kosztuje dużo czasu | dekodowanie jest sekwencyjne |
| **druga karta nie przyspiesza jednego zapytania** | dekodowanie czeka na pamięć, nie na moc |
| **cache promptu daje ogromne oszczędności** | pomijasz prefill w całości (część 7) |

### 5.3 Ile VRAM zjada KV-cache — policz to

Wzór:

```
KV-cache [bajty] ≈ 2 × n_layers × n_kv_heads × head_dim × n_ctx × bajty_na_element
                    ↑                                              ↑
                 K oraz V                                   f16 = 2 bajty
```

Weź parametry z modelu — tym samym czytnikiem GGUF co w §1.4 (`llama-cli -n 0 | grep`
nic tu nie znajdzie, z tego samego powodu co tam):

```bash
python3 $KURS/gguf_meta.py $QWEN32
python3 $KURS/gguf_meta.py $QWEN32 qwen3.attention.key_length qwen3.attention.value_length
```

Oczekiwane (Qwen3-32B, zmierzone na tej maszynie):

```
qwen3.context_length = 32768
qwen3.vocab_size = (brak)
qwen3.block_count = 64
qwen3.attention.head_count = 64
qwen3.attention.head_count_kv = 8
qwen3.embedding_length = 5120
qwen3.attention.key_length = 128
qwen3.attention.value_length = 128
```

⚠️ **`head_dim` NIE zawsze wynosi `n_embd / n_head`.** Tutaj `5120 / 64 = 80`, a
prawdziwy `head_dim` (`attention.key_length`) to **128**. Modele z GQA (*grouped-query
attention*, tu: 64 głowy zapytań na tylko 8 głów KV) często mają wymiar głowy
niezależny od tego prostego dzielenia — dlatego GGUF trzyma go **wprost**, jako osobne
pole, zamiast każdemu kazać go wyliczać. Nie zgaduj — czytaj `key_length`.

I policz:

```bash
python3 - <<'EOF'
# Wartosci ODCZYTANE wyzej z pliku GGUF, nie wyliczone recznie.
n_layers   = 64      # qwen3.block_count
n_kv_heads = 8        # qwen3.attention.head_count_kv
head_dim   = 128     # qwen3.attention.key_length (NIE n_embd/n_head!)
bytes_el   = 2        # f16

for ctx in (4096, 16384, 32768, 131072):
    b = 2 * n_layers * n_kv_heads * head_dim * ctx * bytes_el
    print(f"n_ctx={ctx:7d}  ->  KV-cache = {b/2**30:7.2f} GiB")
EOF
```

⚠️ **Pułapka P22 (nowa): kontekst to pamięć, a pamięci masz skończoną ilość.**
Wagi + KV-cache **muszą się zmieścić razem** w 65 GB (dwie karty). Model 20 GB z kontekstem
128k może potrzebować więcej KV-cache niż samych wag. Dlatego `llama-server` czasem
odmawia startu z dużym `-c` — **to nie błąd, to arytmetyka**.

### 5.4 Jak zmniejszyć KV-cache — trzy dźwignie

```bash
# 1. Kwantyzacja KV-cache: f16 -> q8_0 (polowa pamieci)
$LB/llama-server -m $QWEN32 -ngl 999 -c 32768 \
  --cache-type-k q8_0 --cache-type-v q8_0 \
  --port 8082 --host 127.0.0.1 &
```

| Dźwignia | Efekt | Koszt |
| :-- | :-- | :-- |
| `--cache-type-k/v q8_0` | **½ pamięci KV** | minimalna strata jakości |
| `--cache-type-k/v q4_0` | **¼ pamięci KV** | zauważalna strata — ostrożnie |
| mniejsze `-c` | liniowo mniej | krótsza pamięć rozmowy |

💡 **Kolejność wyboru:** najpierw `q8_0` na KV (prawie darmowe), potem zmniejszaj `-c`.
Nie schodź na `q4_0` dla KV, jeśli czytasz liczby z faktur.

---

## 6. Kontekst — co się dzieje na granicy

### 6.1 Co się dzieje, gdy przepełnisz kontekst

Uruchom serwer z **maleńkim** kontekstem, żeby zobaczyć to od razu:

```bash
pkill -f llama-server; sleep 2
$LB/llama-server -m $BIELIK -ngl 999 -c 512 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

# Prompt dluzszy niz kontekst
python3 - <<'EOF'
import json, urllib.request
long_text = "To jest zdanie wypełniające kontekst. " * 200   # ~1400+ tokenow
req = urllib.request.Request("http://127.0.0.1:8081/v1/completions",
    data=json.dumps({"prompt": long_text + "\nPodsumuj:", "max_tokens": 20, "temperature": 0}).encode(),
    headers={"Content-Type": "application/json"})
try:
    print(json.load(urllib.request.urlopen(req, timeout=120)))
except Exception as e:
    print("BŁĄD:", e)
    if hasattr(e, "read"): print(e.read().decode()[:400])
EOF
```

Dostaniesz albo błąd, albo **cichą utratę początku promptu**. To drugie jest groźniejsze.

⚠️ **Pułapka P23 (nowa): przepełnienie kontekstu bywa CICHE.**
Niektóre konfiguracje przycinają prompt bez ostrzeżenia. Model odpowiada pewnie —
na podstawie tekstu, którego **nie zobaczył w całości**. W agencie czytającym umowy to jest
najgorszy możliwy tryb awarii: nie ma wyjątku, jest błędna odpowiedź.

🔧 **Obrona:** licz tokeny **przed** wysłaniem i twardo odrzucaj to, co się nie mieści.
Zbudujemy to w części 4 (budżet kontekstu) i części 5 (kompakcja).

### 6.2 „Zagubiony w środku" — pozycja ma znaczenie

Modele lepiej pamiętają **początek i koniec** kontekstu niż środek. Sprawdź to:

```bash
pkill -f llama-server; sleep 2
$LB/llama-server -m $QWEN32 -ngl 999 -c 8192 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 30

python3 - <<'EOF'
import json, urllib.request

SECRET = "Kod dostępu do archiwum to ZIELONY-7788."
FILLER = "Dokumentacja księgowa jest przechowywana zgodnie z ustawą o rachunkowości. "

def ask(where):
    n = 60
    if where == "poczatek":  body = SECRET + " " + FILLER * n
    elif where == "srodek":  body = FILLER * (n//2) + SECRET + " " + FILLER * (n//2)
    else:                    body = FILLER * n + " " + SECRET
    prompt = body + "\n\nPytanie: Jaki jest kod dostępu do archiwum? Odpowiedz tylko kodem.\nOdpowiedź:"
    req = urllib.request.Request("http://127.0.0.1:8081/v1/completions",
        data=json.dumps({"prompt": prompt, "max_tokens": 20, "temperature": 0}).encode(),
        headers={"Content-Type": "application/json"})
    out = json.load(urllib.request.urlopen(req, timeout=180))["choices"][0]["text"].strip()
    ok = "ZIELONY-7788" in out or "7788" in out
    print(f"{where:10s} -> {'✅' if ok else '❌'}  {out[:60]!r}")

for w in ("poczatek", "srodek", "koniec"):
    ask(w)
EOF
```

💡 **Wniosek do zapamiętania na część 4:** w RAG-u **nie wrzucaj najważniejszego fragmentu
w środek promptu**. Najtrafniejsze wyniki dawaj na koniec, bliżej pytania.

---

## 7. Embeddingi — jak model mierzy znaczenie

Embedding to zamiana tekstu w **wektor liczb**, taki że teksty o podobnym znaczeniu mają
wektory skierowane w podobną stronę. To fundament pamięci agenta (część 4).

### 7.1 Wyprodukuj pierwszy wektor

```bash
pkill -f llama-server; sleep 2

$LB/llama-embedding -m $BIELIK -p "faktura za usługi księgowe" -ngl 999 --pooling mean 2>/dev/null | head -c 400
echo
```

⚠️ **Dwie pułapki na tej jednej linijce, obie sprawdzone na żywo.**

1. **`--stdin` nie istnieje na `llama-embedding`.** W przeciwieństwie do
   `llama-tokenize` (gdzie ta flaga jest po prostu ignorowana i program mimo to czyta
   `stdin`), tutaj kończy się jawnym błędem: `error: invalid argument: --stdin`, kod
   wyjścia 1. Zawsze **`-p "tekst"`**.
2. **Samo przekierowanie bez żadnej flagi (`echo … | llama-embedding …`, bez `-p`)
   nie daje błędu — daje CICHO wektor złożony z samych zer.** Wygląda jak sukces
   (kod wyjścia 0, poprawny JSON), a wynik jest bezużyteczny. To jest dokładnie ten
   rodzaj awarii, przed którym ostrzega P23 w części 6: **żadnego komunikatu, tylko
   cicho zła odpowiedź.** Sprawdzaj nie tylko kod wyjścia, ale i to, czy wektor nie
   jest zdegenerowany.

🔧 **`--pooling mean`** — model daje jeden wektor **na token**; pooling zbija je w jeden
wektor na cały tekst. `mean` = średnia (bezpieczny domyślny wybór), `last` = tylko ostatni
token, `cls` = specjalny token klasyfikacji.

⚠️ **Pułapka P24 (nowa): model generatywny to kiepski model embeddingowy.**
Bielik jest trenowany do *pisania*, nie do *mierzenia podobieństwa*. Działa, ale słabo.
W części 4 pobierzemy dedykowany model embeddingowy (`bge-m3` albo `multilingual-e5`), który
jest 10× mniejszy i **wyraźnie lepszy w tym jednym zadaniu**. Teraz używamy Bielika tylko
dlatego, że już go masz i chodzi o zrozumienie mechanizmu.

### 7.2 Policz podobieństwo — RĘCZNIE, bez numpy

Tu jest sedno „czucia modelu". Podobieństwo kosinusowe to:

```
              a · b              suma(aᵢ × bᵢ)
cos(a,b) = ───────────  =  ──────────────────────────
           |a| × |b|      √suma(aᵢ²) × √suma(bᵢ²)
```

Napisz to sam:

```bash
mkdir -p $KURS && cat > $KURS/podobienstwo.py <<'EOF'
#!/usr/bin/env python3
"""Podobienstwo kosinusowe dwoch tekstow - czysty Python, bez numpy.

Uzycie:  python3 podobienstwo.py "tekst A" "tekst B"
"""
import math, os, subprocess, sys

LB    = os.path.expanduser("~/llama.cpp/build/bin")
# $BIELIK, jesli sourceowales rig-env.sh w tym samym shellu; zapasowo sciezka wprost.
MODEL = os.environ.get("BIELIK",
    os.path.expanduser("~/models/bielik-11b/Bielik-11B-v3.0-Instruct.Q8_0.gguf"))

def embed(text: str) -> list[float]:
    """Zwraca wektor embeddingu dla tekstu."""
    # UWAGA: "--stdin" na llama-embedding NIE ISTNIEJE (blad "invalid argument"),
    # a samo przekierowanie bez flagi daje CICHO wektor samych zer. Jedyna
    # dzialajaca droga: -p "tekst" (sprawdzone na zywo, patrz P24b w indeksie).
    out = subprocess.run(
        [f"{LB}/llama-embedding", "-m", MODEL, "-p", text,
         "-ngl", "999", "--pooling", "mean", "--embd-output-format", "array"],
        capture_output=True, text=True, timeout=600,
    )
    if out.returncode != 0:
        sys.exit(f"llama-embedding zwrocil {out.returncode}:\n{out.stderr[-500:]}")
    # format "array" => [[x, y, z, ...]]
    import json
    for line in out.stdout.splitlines():
        line = line.strip()
        if line.startswith("[["):
            wektor = json.loads(line)[0]
            if all(abs(x) < 1e-12 for x in wektor):
                sys.exit("wektor zlozony z samych zer - cos poszlo nie tak "
                         "(zla sciezka do modelu? sprawdz stderr powyzej)")
            return wektor
    # zapasowo: liczby oddzielone bialymi znakami
    nums = [float(t) for t in out.stdout.split() if _isnum(t)]
    if not nums:
        sys.exit("nie udalo sie odczytac wektora z wyjscia llama-embedding")
    return nums

def _isnum(t):
    try: float(t); return True
    except ValueError: return False

def cosine(a: list[float], b: list[float]) -> float:
    """Podobienstwo kosinusowe. Recznie, zeby bylo widac wzor."""
    if len(a) != len(b):
        sys.exit(f"rozne dlugosci wektorow: {len(a)} vs {len(b)}")
    dot = 0.0; na = 0.0; nb = 0.0
    for x, y in zip(a, b):
        dot += x * y      # licznik: iloczyn skalarny
        na  += x * x      # kwadrat dlugosci a
        nb  += y * y      # kwadrat dlugosci b
    if na == 0 or nb == 0:
        return 0.0
    return dot / (math.sqrt(na) * math.sqrt(nb))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    a, b = sys.argv[1], sys.argv[2]
    va, vb = embed(a), embed(b)
    print(f"wymiar wektora: {len(va)}")
    print(f"cos({a!r},\n    {b!r}) = {cosine(va, vb):.4f}")
EOF
chmod +x $KURS/podobienstwo.py
```

Uruchom na parach, które **powinny** i **nie powinny** być podobne:

```bash
cd $KURS
python3 podobienstwo.py "faktura za usługi księgowe" "rachunek za prowadzenie księgowości"
python3 podobienstwo.py "faktura za usługi księgowe" "przepis na sernik"
```

Pierwsza para powinna dać wyraźnie wyższą liczbę. **Jeśli różnica jest mała — to jest właśnie
pułapka P24**: model generatywny słabo mierzy znaczenie. W części 4 zobaczysz, jak bardzo
poprawi to dedykowany model.

### 7.3 Co to znaczy „wymiar wektora"

Wektor ma np. 4096 liczb. Każda to jedna „oś znaczenia" — nieinterpretowalna dla człowieka,
ale spójna dla modelu. **Dwa wnioski praktyczne:**

| Fakt | Konsekwencja w części 4 |
| :-- | :-- |
| wektory z różnych modeli są **nieporównywalne** | zmiana modelu embeddingowego = **przebudowa całej bazy** |
| wektor 4096 × 4 bajty = 16 KB na fragment | 100 000 fragmentów = 1,6 GB — planuj pamięć |

---

## 8. Kwantyzacja — zmierz stratę, nie zgaduj

Część 1 powiedziała „Q4 dla dużych, Q8 dla małych". Teraz **zmierzysz**, ile to kosztuje.

### 8.1 Perplexity — miara jakości modelu

Perplexity (PPL) mówi, jak bardzo model „dziwi się" tekstowi. **Niżej = lepiej.**
Formalnie: eksponenta średniej entropii krzyżowej.

Przygotuj tekst testowy (po polsku — Twój język docelowy):

```bash
cat > $KURS/test-ppl.txt <<'EOF'
Ustawa o rachunkowości określa zasady prowadzenia księgi rachunkowej przez jednostki
gospodarcze. Sprawozdanie finansowe składa się z bilansu, rachunku zysków i strat oraz
informacji dodatkowej. Amortyzacja środków trwałych jest dokonywana metodą liniową lub
degresywną. Faktura korygująca zmniejsza lub zwiększa podstawę opodatkowania.
Podatek od towarów i usług rozliczany jest w deklaracji miesięcznej lub kwartalnej.
Zobowiązania krótkoterminowe obejmują kwoty wymagalne w okresie do dwunastu miesięcy.
Kapitał własny to aktywa netto jednostki po odjęciu wszystkich zobowiązań.
Rezerwy tworzy się na pewne lub prawdopodobne przyszłe zobowiązania.
EOF

# Powtorz tekst, zeby bylo co mierzyc (PPL potrzebuje kilkuset tokenow)
for i in $(seq 1 30); do cat $KURS/test-ppl.txt; done > $KURS/ppl-duzy.txt
wc -w $KURS/ppl-duzy.txt
```

### 8.2 Zmierz Bielika (Q8)

```bash
pkill -f llama-server; sleep 2
$LB/llama-perplexity -m $BIELIK -f $KURS/ppl-duzy.txt -ngl 999 -c 2048 2>&1 | tail -5
```

Szukaj linii `Final estimate: PPL = X`. **Zapisz tę liczbę.**

### 8.3 Porównaj modele

```bash
for MODEL in $BIELIK $OSS20 $QWEN32; do
  echo "=== $(basename $MODEL)"
  $LB/llama-perplexity -m $MODEL -f $KURS/ppl-duzy.txt -ngl 999 -c 2048 2>&1 \
    | grep -E 'Final estimate' || echo "  (nie policzono)"
  sleep 3
done
```

💡 **Jak czytać wynik.** PPL jest porównywalna **tylko przy tym samym tekście i tym samym
`-c`**. Nie porównuj swojej liczby z niczym z internetu. Porównuj **swoje pomiary między
sobą** — to jedyny sens tego narzędzia u Ciebie.

⚠️ **PPL mierzy „przewidywalność tekstu", nie „przydatność do zadania".** Model z lepszą PPL
na tekście księgowym nie musi lepiej wyciągać kwot z faktur. **PPL to sito wstępne — prawdziwa
miara to Twój własny zestaw ewaluacyjny z części 3.**

### 8.4 Po co Ci to w części 7

W części 7 **skwantyzujesz model sam** (`llama-quantize`) i będziesz potrzebował miary,
czy nie zepsułeś go za mocno. PPL przed i po to dokładnie ta miara.

---

## 9. Ćwiczenie — własna pętla generowania

To jest zwieńczenie rozdziału. Napiszesz generowanie tekstu **token po tokenie**, sam
wybierając każdy token. Po tym ćwiczeniu „model generuje tekst" przestanie być magią.

```bash
cat > $KURS/moja-petla.py <<'PYEOF'
#!/usr/bin/env python3
"""Generowanie tekstu token po tokenie - wlasna petla probkowania.

Wymaga uruchomionego llama-server:
  $LB/llama-server -m $BIELIK -ngl 999 -c 2048 --port 8081 --host 127.0.0.1

Uzycie:  python3 moja-petla.py "Twoj prompt"
"""
import json, math, random, sys, urllib.request

SERVER = "http://127.0.0.1:8081"

def next_token_distribution(prompt: str, n_probs: int = 40):
    """Jeden forward pass. Zwraca liste (token_str, prawdopodobienstwo)."""
    body = {
        "prompt": prompt,
        "max_tokens": 1,
        "temperature": 1.0,   # NIE probkujemy po stronie serwera...
        "top_k": 0,           # ...chcemy surowy rozklad
        "top_p": 1.0,
        "min_p": 0.0,
        "n_probs": n_probs,
    }
    req = urllib.request.Request(SERVER + "/v1/completions",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=120))
    # Ksztalt tego builda: choices[0].logprobs.content[0].top_logprobs,
    # kazdy wpis niesie logprob (log naturalny), NIE prob wprost - stad math.exp().
    choices = d.get("choices") or [{}]
    content = (choices[0].get("logprobs") or {}).get("content") or []
    if not content:
        return []
    raw = content[0].get("top_logprobs") or []
    return [(t.get("token", ""), math.exp(t.get("logprob", -999.0))) for t in raw]

def apply_temperature(dist, temperature):
    """Przeskaluj rozklad. T<1 zaostrza, T>1 wyplaszcza."""
    if temperature <= 0:                       # greedy
        return [max(dist, key=lambda x: x[1])] if dist else []
    # p -> p^(1/T), potem renormalizacja
    scaled = [(t, p ** (1.0 / temperature)) for t, p in dist if p > 0]
    s = sum(p for _, p in scaled)
    return [(t, p / s) for t, p in scaled] if s > 0 else []

def apply_min_p(dist, min_p):
    """Odetnij tokeny slabsze niz min_p * p_najlepszego."""
    if not dist or min_p <= 0:
        return dist
    top = max(p for _, p in dist)
    kept = [(t, p) for t, p in dist if p >= min_p * top]
    s = sum(p for _, p in kept)
    return [(t, p / s) for t, p in kept] if s > 0 else dist

def apply_top_k(dist, k):
    """Zostaw K najlepszych."""
    if not dist or k <= 0:
        return dist
    kept = sorted(dist, key=lambda x: x[1], reverse=True)[:k]
    s = sum(p for _, p in kept)
    return [(t, p / s) for t, p in kept] if s > 0 else dist

def sample(dist, rng):
    """Losuj token wedlug rozkladu (kolo ruletki)."""
    if not dist:
        return None
    r = rng.random()
    acc = 0.0
    for t, p in dist:
        acc += p
        if r <= acc:
            return t
    return dist[-1][0]

def generate(prompt, n_tokens=40, temperature=0.7, top_k=40, min_p=0.05, seed=42, verbose=True):
    rng = random.Random(seed)
    text = prompt
    for step in range(n_tokens):
        dist = next_token_distribution(text)
        if not dist:
            print("\n[koniec: serwer nie zwrocil rozkladu]"); break

        before_top = max(dist, key=lambda x: x[1])

        d = apply_temperature(dist, temperature)
        d = apply_top_k(d, top_k)
        d = apply_min_p(d, min_p)

        tok = sample(d, rng)
        if tok is None or tok == "":
            print("\n[koniec: pusty token]"); break

        if verbose and step < 8:
            print(f"  krok {step:2d}: kandydatow {len(dist):3d} -> po filtrach {len(d):3d} | "
                  f"najlepszy {before_top[0]!r} p={before_top[1]:.3f} | WYBRANO {tok!r}")

        text += tok
        sys.stdout.write(tok); sys.stdout.flush()
    print()
    return text

if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Amortyzacja środka trwałego to"
    print(f"PROMPT: {prompt!r}\n")
    print("--- pierwsze 8 krokow szczegolowo ---")
    generate(prompt)
PYEOF
chmod +x $KURS/moja-petla.py
```

Uruchom:

```bash
pkill -f llama-server; sleep 2
$LB/llama-server -m $BIELIK -ngl 999 -c 2048 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

cd $KURS && python3 moja-petla.py "Amortyzacja środka trwałego to"
```

**Co zobaczysz:** dla pierwszych ośmiu kroków wypisze, ilu było kandydatów, ile zostało po
Twoich filtrach i który token wybrałeś. Potem po prostu leci tekst.

### 9.1 Zadania do tej pętli

1. Ustaw `temperature=0` — potwierdź, że wynik jest identyczny przy każdym uruchomieniu.
2. Ustaw `min_p=0.5` przy `temperature=1.2` — zobacz, że mimo wysokiej temperatury tekst
   zostaje sensowny. **To jest dowód, dlaczego `min_p` jest lepszy od `top_p`.**
3. Ustaw `top_k=1` — porównaj z `temperature=0`. Czy to to samo? (Tak — i teraz wiesz, czemu.)
4. Zmień `seed` — zobacz, że przy `temperature>0` dostajesz inny tekst, przy `0` ten sam.

⚠️ **Ta pętla jest wolna** — jedno żądanie HTTP na token. To jest **celowe**: widzisz koszt
każdego tokenu osobno. W prawdziwym użyciu serwer robi całą pętlę wewnętrznie, bez narzutu
sieci, z KV-cache utrzymanym między krokami.

---

## Sprawdź się

Zanim pójdziesz do części 3, odpowiedz sobie **bez zaglądania**:

- [ ] Dlaczego polski tekst zjada więcej kontekstu niż angielski o tej samej treści?
- [ ] Co dokładnie zwraca jeden forward pass modelu?
- [ ] Dlaczego `repeat_penalty > 1.0` psuje generowanie JSON-a?
- [ ] Dlaczego `temperature=0` **nie** gwarantuje bitowo identycznych wyników?
- [ ] Która faza — prefill czy dekodowanie — jest ograniczona przepustowością pamięci?
- [ ] Dlaczego druga karta nie przyspiesza jednego zapytania?
- [ ] Co się stanie, jeśli zmienisz model embeddingowy po zbudowaniu bazy wektorowej?
- [ ] Dlaczego PPL nie wystarcza jako miara przydatności modelu do Twojego zadania?

## Nowe pułapki z tego rozdziału

| ID | Pułapka | § |
| :-- | :-- | :-- |
| **P20** | Liczenie tokenów tokenizerem innego modelu niż używany | §1.3 |
| **P21** | `repeat_penalty > 1.0` przy generowaniu JSON — psuje strukturę | §3.4 |
| **P22** | Kontekst to VRAM: wagi + KV-cache muszą się zmieścić razem | §5.3 |
| **P23** | Przepełnienie kontekstu bywa **ciche** — pewna odpowiedź na przyciętych danych | §6.1 |
| **P24** | Model generatywny jako model embeddingowy — działa słabo | §7.1 |

---

**Następna część: `03-KONTROLA-I-NIEZAWODNOSC.md`** — jak zmusić lokalny model, żeby
**zawsze** zwracał poprawny JSON. To jest różnica między demem a produktem.
