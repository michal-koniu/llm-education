# Część 14 · Ewaluacja — skąd wiesz, że to działa

**Poziom:** ⭐⭐⭐⭐ · **Czas:** ~5 h · **Wymaga:** części 3 (harness), 13 (flota)
**Produkuje:** zbiór złoty, ocenę trajektorii, sędziego z weryfikacją zewnętrzną, bramkę regresji

---

## 0. Liczba, która powinna zmienić Twoje priorytety

> **Wynik agenta zmienia się bardziej wraz z harnessem niż z modelem.** Ten sam model
> pod dwoma szkieletami daje istotnie różne liczby. Harness decyduje, jak udostępnione
> są narzędzia, jak pokazywane są błędy i ile prób dostaje agent. **Prompt i pętla
> planowania potrafią dodać lub odjąć punkty, zanim model w ogóle zacznie pracować.**
> — [Prefactor, Agent Benchmarks](https://prefactor.tech/learn/agent-benchmarks)

Dwie konsekwencje, obie praktyczne:

1. **Cudze benchmarki modeli nic Ci nie mówią** o tym, jak model zachowa się w Twoim
   systemie. Mierzono je pod innym harnessem.
2. **Musisz mierzyć własny system**, bo inaczej nie wiesz, czy zmiana, którą właśnie
   wprowadziłeś, pomogła czy zaszkodziła.

⭐ **To jest część, bez której wszystkie poprzednie są zgadywaniem.** Każdy „próg",
„limit" i „wariant" z części 4–13 opiera się na pomiarze. Tu budujesz maszynę, która
go wykonuje.

---

## 1. Cztery poziomy oceny

Większość ludzi mierzy tylko poziom 1 i dziwi się, że agent jest zawodny.

| Poziom | Co mierzy | Przykład | Trudność |
| :-- | :-- | :-- | :-- |
| **1 · wynik** | czy odpowiedź jest poprawna | „42 faktury" = prawda? | ⭐ łatwe |
| **2 · trajektoria** | czy droga do wyniku była sensowna | 3 kroki czy 19? właściwe narzędzia? | średnie |
| **3 · niezawodność** | czy działa **za każdym razem** | 10 przebiegów, ile sukcesów | średnie |
| **4 · odporność** | czy nie da się go zmylić | wstrzyknięcie, dane brzegowe | trudne |

⭐ **Poziom 3 jest tym, który odróżnia demo od systemu.** Agent zaliczający zadanie
w 7 na 10 przebiegów **nie działa w 70 %** — on **nie działa**, bo nie wiesz, który
przebieg dostaniesz.

### 1.1 · `pass^k` — miara, którą warto znać

```
pass@k  = czy choć raz się udało w k próbach     ← miara ZDOLNOŚCI
pass^k  = czy udało się we WSZYSTKICH k próbach  ← ⭐ miara NIEZAWODNOŚCI
```

Agent ze skutecznością 80 % na krok ma `pass^5` = 0,8⁵ = **33 %**. To znaczy, że
w dwóch trzecich przypadków seria pięciu zadań zawiedzie choć raz.

⭐ **Raportuj `pass^k`, nie `pass@k`.** `pass@k` to liczba do prezentacji. `pass^k`
to liczba, na której podejmujesz decyzje.

---

## 2. Zbiór złoty

### 2.1 · Konstrukcja

**Sto pytań to dobry cel. Pięćdziesiąt wystarcza na start. Dwadzieścia to za mało,
żeby wykryć zmianę o 5 punktów.**

```json
{
  "id": "Z041",
  "kategoria": "wyszukanie_z_cytatem",
  "pytanie": "Jaki jest termin płatności faktury FV/017/03/2026?",
  "oczekiwane": {
    "zawiera": ["2026-04-14"],
    "nie_zawiera": ["nie wiem", "nie znalazłem"],
    "wymaga_cytatu": true,
    "zrodlo": "faktury/2026/03/f017.txt"
  },
  "trajektoria": {
    "max_krokow": 4,
    "wymagane_narzedzia": ["znajdz_dokumenty"],
    "zakazane_narzedzia": ["powloka"]
  },
  "przebiegow": 3
}
```

### 2.2 · Pięć kategorii — i dlaczego akurat te

| Kategoria | Udział | Czego pilnuje |
| :-- | --: | :-- |
| **Wyszukanie z cytatem** | 30 % | podstawowa kompetencja |
| **Synteza z wielu źródeł** | 25 % | ⭐ tu załamuje się kontekst (część 4) |
| **⭐ Poprawna odmowa** | 20 % | pytania, na które **nie ma** odpowiedzi w danych |
| **Wieloetapowe** | 15 % | ⭐ tu widać wartość harnessu (część 3) |
| **⭐ Odporność** | 10 % | wstrzyknięcia, dane sprzeczne, brzegowe |

⭐ **Dwadzieścia procent na poprawną odmowę to nie przesada.** Agent, który zawsze coś
odpowiada, jest **gorszy niż brak agenta**, bo brzmi wiarygodnie. Bez tej kategorii
w zbiorze będziesz optymalizował w stronę pewności siebie, a nie prawdziwości.

### 2.3 · Skąd brać pytania

| Źródło | Jakość | Uwaga |
| :-- | :-- | :-- |
| ⭐ **Twoje realne sesje z dziennika** | najwyższa | są prawdziwe; masz je od części 2 |
| ⭐ **Awarie, które Cię zabolały** | najwyższa | każda awaria → nowe pytanie, na zawsze |
| Wygenerowane modelem z korpusu | średnia | ⚠️ tanie, ale mierzą to, co model uważa za ważne |
| Ręcznie wymyślone | zmienna | zwykle za łatwe |

```bash
# Wyciągnij kandydatów z własnych dzienników — najlepsze źródło, jakie masz
python3 testy/z_dziennika.py --ostatnie 200 --tylko-udane > kandydaci.jsonl
```

⚠️ **Nigdy nie wrzucaj do zbioru złotego odpowiedzi wygenerowanej przez ten sam model,
który testujesz, bez sprawdzenia jej ręcznie.** Zbudujesz benchmark mierzący
powtarzalność, nie poprawność.

---

## 3. Ocena trajektorii

Wynik poprawny, droga absurdalna — to jest realny stan i trzeba go widzieć.

```python
# $OSA/ewaluacja/trajektoria.py
def ocen_trajektorie(zdarzenia: list, oczekiwana: dict) -> dict:
    krokow = sum(1 for z in zdarzenia if z["typ"] == "narzedzie.wywolanie")
    uzyte  = [z["narzedzie"] for z in zdarzenia if z["typ"] == "narzedzie.wywolanie"]
    bledy  = sum(1 for z in zdarzenia if z["typ"] == "narzedzie.wynik" and z.get("kod"))

    # powtórzenia identycznych wywołań = kręcenie się w kółko
    podpisy = [f'{z["narzedzie"]}:{json.dumps(z["argumenty"], sort_keys=True)}'
               for z in zdarzenia if z["typ"] == "narzedzie.wywolanie"]
    powtorzen = len(podpisy) - len(set(podpisy))

    uwagi = []
    if krokow > oczekiwana["max_krokow"]:
        uwagi.append(f"za dużo kroków: {krokow} > {oczekiwana['max_krokow']}")
    if powtorzen:
        uwagi.append(f"{powtorzen} powtórzonych wywołań (kręcenie się)")
    for n in oczekiwana.get("zakazane_narzedzia", []):
        if n in uzyte:
            uwagi.append(f"⚠️ użyto zakazanego '{n}'")
    for n in oczekiwana.get("wymagane_narzedzia", []):
        if n not in uzyte:
            uwagi.append(f"nie użyto wymaganego '{n}'")

    return {"krokow": krokow, "bledow": bledy, "powtorzen": powtorzen,
            "narzedzia": uzyte, "uwagi": uwagi, "czysta": not uwagi}
```

⭐ **`powtorzen` to najtańszy i najskuteczniejszy detektor patologii.** Agent
wywołujący dwa razy to samo z tymi samymi argumentami **na pewno** nie robi postępu.
To ten sam sygnał, co odcisk stanu z części 3, tylko tańszy do policzenia.

---

## 4. Sędzia — i dlaczego nie może być tym samym agentem

### 4.1 · Problem samo-weryfikacji

> Przy próbkowaniu trajektorii samo-refleksja jest podatna na **skrzywienie
> samo-weryfikacji**: agent ocenia własne wyniki pośrednie **z tego samego stanu
> trajektorii, który je wytworzył**. To sprzężenie splata weryfikację
> z samousprawiedliwieniem i prowadzi do akceptowania wadliwych wyników.
> — [arXiv 2603.02798](https://arxiv.org/pdf/2603.02798)

Tłumaczenie na praktykę: **agent, który się pomylił, nie zauważy tego, bo patrzy na
problem tym samym błędnym zestawem założeń.** Badania z ICLR 2024 mówią to samo:
modele nie potrafią niezawodnie poprawiać własnego rozumowania bez sygnału z zewnątrz.

### 4.2 · Cztery źródła weryfikacji, od najmocniejszego

| Źródło | Siła | Koszt | Zastosowanie |
| :-- | :-- | :-- | :-- |
| ⭐⭐⭐ **Wykonanie** | najwyższa | niski | test przechodzi, plik istnieje, suma się zgadza |
| ⭐⭐ **Dopasowanie do wzorca** | wysoka | zerowy | cytat występuje w źródle, format się zgadza |
| ⭐ **Sędzia w izolowanym kontekście** | średnia | średni | „czy odpowiedź jest zgodna z dokumentem" |
| ✗ **Samo-refleksja** | **najniższa** | niski | ⚠️ tylko jako podpowiedź, **nigdy jako bramka** |

⭐ **Kolejność jest tu całą nauką.** Zanim sięgniesz po sędziego-model, sprawdź, czy da
się zweryfikować wykonaniem albo wzorcem. Ponad połowa pytań z dobrze zbudowanego
zbioru złotego da się — i te dwa źródła są **darmowe i niezawodne**.

### 4.3 · Sędzia w izolowanym kontekście

```python
PROMPT_SEDZIEGO = """Oceń, czy ODPOWIEDŹ poprawnie odpowiada na PYTANIE
na podstawie ŹRÓDŁA.

Nie masz dostępu do niczego poza tym, co poniżej. Nie zakładaj kontekstu.

Kryteria (każde osobno):
1. ZGODNOŚĆ — czy twierdzenia odpowiedzi wynikają ze źródła? (tak/nie/częściowo)
2. KOMPLETNOŚĆ — czy odpowiada na całe pytanie? (tak/nie/częściowo)
3. CYTAT — czy podany cytat DOSŁOWNIE występuje w źródle? (tak/nie/brak cytatu)
4. WYMYŚLONE — czy zawiera twierdzenia, których w źródle NIE MA? (tak/nie)

Zwróć JSON: {{"zgodnosc":…,"kompletnosc":…,"cytat":…,"wymyslone":…,"uzasadnienie":"…"}}

PYTANIE: {pytanie}
ŹRÓDŁO: {zrodlo}
ODPOWIEDŹ: {odpowiedz}"""

def sedzia(pytanie, zrodlo, odpowiedz, wywolaj_model_sedziego):
    """⭐ Sędzia NIE WIDZI: trajektorii, promptu agenta, historii. Tylko te trzy rzeczy."""
    return json.loads(wywolaj_model_sedziego(
        [{"rola": "user", "tresc": PROMPT_SEDZIEGO.format(
            pytanie=pytanie, zrodlo=zrodlo, odpowiedz=odpowiedz)}],
        gramatyka=GRAMATYKA_WERDYKTU)["tresc"])
```

**Trzy zasady dla sędziego:**

1. **Izolowany kontekst.** Nie widzi, jak agent doszedł do odpowiedzi — inaczej da się
   przekonać rozumowaniem zamiast wynikiem.
2. **Kryteria osobno.** „Czy to dobra odpowiedź" daje szum. Cztery pytania binarne
   dają sygnał.
3. **Inny model niż oceniany**, jeśli możesz. `qwen3-32b` ocenia `gpt-oss-20b`.

### 4.4 · Kalibracja sędziego

⚠️ **Sędzia to też model i też się myli. Zanim mu zaufasz — zmierz go.**

```bash
# 40 przypadków ocenionych przez Ciebie ręcznie → porównaj z sędzią
python3 ewaluacja/kalibruj_sedziego.py --recznie recznie.jsonl
# zgodność: 34/40 (85%)
# ⚠️ sędzia BARDZIEJ POBŁAŻLIWY w 5 z 6 rozbieżności
#    → przy odmowach: sędzia akceptuje "nie znalazłem", gdy odpowiedź BYŁA w źródle
```

⭐ **Kierunek błędu sędziego jest ważniejszy niż jego wielkość.** Sędzia pobłażliwy
zawyża wynik i **uśpi Cię**. Sędzia surowy zaniża i najwyżej zmarnujesz czas na
nieistniejący problem. Jeśli musisz wybrać — kalibruj w stronę surowości.

---

## 5. Bramka regresji

⭐ **To jest najważniejszy praktyczny produkt tej części.** Żadna zmiana nie wchodzi
bez pomiaru.

```python
# $OSA/ewaluacja/bramka.py
PROGI = {
    "spadek_ogolny_pp":     2.0,    # spadek > 2 pp = odrzucenie
    "spadek_kategorii_pp":  5.0,    # żadna kategoria nie spada > 5 pp
    "min_odmowy":          90.0,    # ⭐ odmowy NIGDY nie mogą spaść poniżej
    "wzrost_krokow":        1.3,    # średnia liczba kroków nie rośnie o >30 %
    "wzrost_tokenow":       1.5,
}

def bramka(nowy: dict, bazowy: dict) -> tuple[bool, list]:
    powody = []
    d = nowy["ogolem"] - bazowy["ogolem"]
    if d < -PROGI["spadek_ogolny_pp"]:
        powody.append(f"wynik ogólny {bazowy['ogolem']:.1f} → {nowy['ogolem']:.1f} ({d:+.1f} pp)")
    for k in bazowy["kategorie"]:
        dk = nowy["kategorie"][k] - bazowy["kategorie"][k]
        if dk < -PROGI["spadek_kategorii_pp"]:
            powody.append(f"kategoria '{k}': {dk:+.1f} pp")
    if nowy["kategorie"].get("poprawna_odmowa", 100) < PROGI["min_odmowy"]:
        powody.append(f"⚠️ odmowy {nowy['kategorie']['poprawna_odmowa']:.1f}% "
                      f"< {PROGI['min_odmowy']}% — agent zaczął zgadywać")
    if nowy["sr_krokow"] > bazowy["sr_krokow"] * PROGI["wzrost_krokow"]:
        powody.append(f"kroki {bazowy['sr_krokow']:.1f} → {nowy['sr_krokow']:.1f}")
    return not powody, powody
```

**Wepnij w trzy miejsca:**

```bash
# 1. przed każdym commitem zmieniającym prompt, narzędzia albo harness
python3 ewaluacja/bramka.py --przed-commitem

# 2. w zadaniu nocnym (część 11) — wykrywa dryf bez Twojego udziału
# 3. przy każdej zmianie modelu albo jego wersji
```

---

## 6. Czego nauczyć się z dużych benchmarków

Nie uruchamiaj ich. **Ukradnij z nich pomysły.**

| Benchmark | Pomysł wart skopiowania |
| :-- | :-- |
| **τ²-bench** | ⭐ **Użytkownik też wywołuje narzędzia.** Twój zbiór powinien mieć przypadki, w których stan świata zmienia się **w trakcie** pracy agenta |
| **SWE-bench** | ⭐ **Weryfikacja przez testy repozytorium** — sygnał z wykonania, nie z opinii |
| **GAIA** | Zadania wymagające **wielu modalności i wielu kroków**; ocena względem prawdy, nie stylu |
| **Terminal-Bench** | Zadania w prawdziwym terminalu — najbliżej tego, co robi Twój agent |

⭐ **τ²-bench jest najciekawszy dla Ciebie.** Klasyczny zbiór złoty zakłada, że świat
stoi. Twój agent pracuje w świecie, w którym **Ty w tym samym czasie dodajesz pliki
i zmieniasz kalendarz**. Dodaj 3–5 takich przypadków — będą najtrudniejsze i najbardziej
pouczające.

---

## 7. EKSPERYMENT 14 — ten sam model, dwa harnessy

⭐ **Ten eksperyment weryfikuje tezę, na której stoi cały kurs.**

**Hipoteza:** różnica między harnessem z części 3 a naiwną pętlą z kursu 1 jest
**większa** niż różnica między `gpt-oss-20b` a `qwen3-32b` pod tym samym harnessem.

### 7.1 · Cztery kombinacje

```bash
mkdir -p $OSA/pomiary/ewaluacja
for h in naiwny pelny; do for m in oss20 qwen32; do
  python3 ewaluacja/uruchom.py --harness $h --model $m --przebiegow 3 \
    > pomiary/ewaluacja/$h-$m.json
done; done
```

| | `gpt-oss-20b` | `qwen3-32b` | **różnica modelu** |
| :-- | --: | --: | --: |
| harness naiwny | | | |
| harness pełny | | | |
| **różnica harnessu** | | | |

⚠️ **Predykcja:** różnica harnessu (pionowo) będzie **większa** niż różnica modelu
(poziomo). Jeśli tak wyjdzie — masz tezę kursu potwierdzoną na własnym sprzęcie
i konkretny argument, żeby **nie kupować większych modeli**, dopóki harness jest słaby.

### 7.2 · Rozbicie na kategorie i `pass^3`

| Kategoria | Naiwny | Pełny | Δ |
| :-- | --: | --: | --: |
| Wyszukanie z cytatem | | | |
| Synteza | | | |
| ⭐ Poprawna odmowa | | | |
| Wieloetapowe | | | |
| Odporność | | | |
| **`pass^3` (wszystkie 3 przebiegi)** | | | |

⭐ **Spodziewam się, że największa różnica będzie w „wieloetapowych" i w `pass^3`** —
bo to są dokładnie te dwie rzeczy, które harness naprawia: dokończenie długiego
zadania i powtarzalność.

### 7.3 · Co zrobić z wynikiem

```bash
python3 ewaluacja/uruchom.py --zapisz-baze    # to jest Twój punkt odniesienia
```

Od tej chwili **każda** zmiana w systemie jest mierzona względem tej bazy. Bez bazy
wszystkie kolejne części to zgadywanie.

---

## 8. PRODUKCYJNIE

| | promptfoo | DeepEval / Ragas | Langfuse / Phoenix | **Twój** |
| :-- | :-- | :-- | :-- | :-- |
| Zbiór złoty | ⭐ YAML | ⭐ | ⭐ | JSON |
| LLM-as-judge | ⭐ | ⭐ | ⭐ | ⭐ |
| **Ocena trajektorii** | ✗ | częściowo | ⭐ ze śladów | ⭐ |
| **`pass^k`** | ✗ | ✗ | ✗ | ⭐ |
| **Bramka regresji** | ⭐ CI | ręcznie | ⭐ | ⭐ |
| **Kalibracja sędziego** | ✗ | częściowo | ✗ | ⭐ |
| Offline | ⭐ | ⭐ | ⭐ self-hosted | ⭐ |

> 💡 **Kiedy warto dołożyć gotowe.** Gdy zechcesz metryk RAG-owych (faithfulness,
> context precision) — Ragas ma je dopracowane i nie ma sensu pisać ich od zera.
> Wynik logujesz na swoje ślady z części 15.

---

## 9. ĆWICZENIE

1. Zbuduj zbiór złoty: **50 pytań**, pięć kategorii w podanych proporcjach.
   Co najmniej 20 wyciągnij z **własnych dzienników** z części 2.
2. Zaimplementuj ocenę trajektorii z detekcją powtórzeń.
3. Zaimplementuj sędziego w izolowanym kontekście na innym modelu.
4. **Skalibruj sędziego** na 40 przypadkach ocenionych ręcznie. Zapisz kierunek błędu.
5. Uruchom eksperyment z §7 i zapisz bazę.
6. Wepnij bramkę w commit i w zadanie nocne.

```bash
python3 ewaluacja/uruchom.py --raport
# ═══ ZBIÓR ZŁOTY · archiwista · gpt-oss-20b · harness pełny ═══
#   wyszukanie_z_cytatem   14/15   93%   (baza 93%)   →
#   synteza                10/13   77%   (baza 69%)   ↑ +8
#   poprawna_odmowa         9/10   90%   (baza 90%)   →
#   wieloetapowe            6/ 8   75%   (baza 50%)   ↑ +25
#   odpornosc               3/ 4   75%   (baza 75%)   →
#   ─────────────────────────────────────────────────
#   OGÓŁEM                 42/50   84%   (baza 78%)   ↑ +6
#   pass^3                 31/50   62%   (baza 48%)   ↑ +14
#   śr. kroków 4,2 (baza 6,8)   śr. tokenów 3 180
#   trajektorie czyste: 38/50 · powtórzenia w 7 · zakazane narzędzia w 0
#   ✓ BRAMKA: przechodzi
```

---

## 10. Pułapki tej części

| ID | Pułapka | Objaw | Jak uniknąć |
| :-- | :-- | :-- | :-- |
| **P118** | **Agent ocenia sam siebie** | Wszystko zielone, użytkownik widzi błędy | Weryfikacja zewnętrzna: wykonanie → wzorzec → sędzia w izolacji. Samo-refleksja **nigdy jako bramka** |
| **P119** | **Brak kategorii „poprawna odmowa"** | Optymalizujesz w stronę pewności siebie; agent zawsze coś odpowiada | 20 % zbioru to pytania bez odpowiedzi w danych; twardy próg 90 % w bramce |
| **P120** | **Jeden przebieg na pytanie** | Wynik skacze o 8 pp między pomiarami, nie wiesz dlaczego | ≥3 przebiegi, raportuj `pass^k` obok średniej |
| **P121** | **Nieskalibrowany sędzia** | Sędzia pobłażliwy zawyża i usypia; myślisz, że jest lepiej | 40 przypadków ręcznie; zapisz **kierunek** błędu, kalibruj w stronę surowości |
| **P122** | **Zbiór złoty wygenerowany testowanym modelem** | Mierzysz powtarzalność, nie poprawność; 95 % i bezużyteczne | Pytania z realnych dzienników i z awarii. Każda wygenerowana odpowiedź sprawdzona ręcznie |

---

## 11. Checkpoint

```bash
cd $OSA
python3 - <<'EOF'
import json, pathlib, collections
z = [json.loads(l) for l in open("testy/zbior-zloty.jsonl", encoding="utf-8")]
assert len(z) >= 50, f"za mało pytań: {len(z)}"
k = collections.Counter(x["kategoria"] for x in z)
assert k["poprawna_odmowa"] / len(z) >= 0.18, "P119: za mało odmów"
assert all(x.get("przebiegow", 1) >= 3 for x in z), "P120: <3 przebiegi"
print(f"✓ zbiór złoty: {len(z)} pytań, {dict(k)}")
EOF
test -s pomiary/ewaluacja/baza.json && echo "✓ baza zapisana"
test -s ewaluacja/kalibracja-sedziego.json && echo "✓ sędzia skalibrowany"
python3 ewaluacja/bramka.py --przed-commitem && echo "✓ bramka przechodzi"
git add -A && git commit -m "część 14: zbiór złoty, trajektoria, sędzia, bramka regresji"
```

- [ ] Mierzysz cztery poziomy, nie tylko wynik
- [ ] Raportujesz `pass^k`, nie `pass@k`
- [ ] Zbiór złoty ≥50 pytań, 20 % to poprawne odmowy
- [ ] Co najmniej 20 pytań pochodzi z **realnych dzienników**
- [ ] Trajektoria oceniana; powtórzenia wykrywane
- [ ] Weryfikacja zewnętrzna: wykonanie → wzorzec → sędzia w izolacji
- [ ] **Sędzia skalibrowany**, znasz kierunek jego błędu
- [ ] Bramka regresji wpięta w commit i w zadanie nocne
- [ ] ⭐ **Zmierzyłeś: harness kontra model. Masz bazę odniesienia**

---

**Dalej: `15-OBSERWOWALNOSC.md`** — widzieć, co agent robi, i umieć odpowiedzieć na
pytanie „dlaczego to zrobił" z samych śladów.
