# Część 17 · Hybryda i router — lokalny domyślnie, chmura świadomie

**Poziom:** ⭐⭐⭐ · **Czas:** ~4 h · **Wymaga:** części 14 (ewaluacja), 15 (metryki), 16 (bezpieczeństwo)
**Produkuje:** router, granicę prywatności wyrażoną kodem, audyt wyjścia, tryb pełnego offline

---

## 0. Ustalenie na początek

**Lokalny jest domyślny. Chmura jest wyjątkiem, który musi się uzasadnić.** Nie
odwrotnie.

To nie jest ideologia, tylko trzy policzalne powody:

| Powód | Liczba |
| :-- | :-- |
| **Koszt krańcowy** | lokalnie ≈ prąd. Agent mielący 40 min w nocy kosztuje grosze |
| **Prywatność** | treść, która nie wyszła, nie wycieknie — **wymuszalne technicznie** |
| **Dostępność** | brak sieci, brak limitów, brak zmiany cennika w cudzym kwartale |

⭐ **A jednocześnie: odmowa użycia chmury tam, gdzie realnie wygrywa, jest kosztem,
nie cnotą.** Ta część uczy Cię **rozstrzygać to pomiarem** i wpisywać rozstrzygnięcie
w kod, a nie w dobre chęci.

---

## 1. Trzy pytania routera — w tej kolejności

```
1. PRYWATNOŚĆ  →  czy tę treść WOLNO wysłać?        ← twarda bramka
2. ZDOLNOŚĆ    →  czy lokalny to zrobi?              ← z pomiaru, nie z przeczucia
3. KOSZT       →  czy warto zapłacić za różnicę?     ← liczba
```

⚠️ **Kolejność jest nienegocjowalna.** Router pytający najpierw o zdolność, a potem
o prywatność, **kiedyś wyśle coś, czego nie powinien** — bo ścieżka „model lokalny
zawiódł, spróbuj chmury" ominie bramkę. Prywatność jest **pierwsza i jest bramką,
nie wagą w funkcji oceniającej**.

---

## 2. Granica prywatności jako kod

Deklaracja w regulaminie jest warta tyle, ile wynosi dyscyplina osoby, która pisze
kod o 23:00. **Granica musi być egzekwowana, nie deklarowana.**

```python
# $OSA/router/granica.py
"""Jedyna droga treści na zewnątrz. Wszystko inne jest błędem architektury."""
import re, hashlib, os, pathlib, json

class Odmowa(Exception): pass

KATALOGI_ZAKAZANE = ["~/dokumenty", "~/.ssh", "~/.config", "$OSA/pamiec"]

WZORCE_ZAKAZANE = [
    (r"\b\d{10}\b",                          "NIP"),
    (r"\b\d{11}\b",                          "PESEL"),
    (r"\bPL\d{26}\b",                        "IBAN"),
    (r"[\w.+-]+@[\w-]+\.[\w.]+",             "e-mail"),
    (r"\b(?:\+48\s?)?\d{3}[\s-]?\d{3}[\s-]?\d{3}\b", "telefon"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----",  "klucz prywatny"),
    (r"\b(sk-|ghp_|xoxb-)[A-Za-z0-9_-]{16,}", "token API"),
]

def sprawdz(tresc: str, zrodlo: str, zgoda_jawna=False) -> None:
    """Rzuca Odmowa, jeśli treść nie może opuścić maszyny."""
    for k in KATALOGI_ZAKAZANE:
        if str(pathlib.Path(os.path.expandvars(k)).expanduser()) in zrodlo:
            raise Odmowa(f"Źródło '{zrodlo}' jest w katalogu zakazanym ({k}).")
    znalezione = [n for w, n in WZORCE_ZAKAZANE if re.search(w, tresc)]
    if znalezione and not zgoda_jawna:
        raise Odmowa(f"Treść zawiera: {', '.join(set(znalezione))}. "
                     f"Wysyłka wymaga jawnej zgody albo anonimizacji.")

def anonimizuj(tresc: str) -> tuple[str, dict]:
    """Zamiana na zastępniki. Odwracalna po powrocie odpowiedzi."""
    mapa = {}
    for wzor, nazwa in WZORCE_ZAKAZANE:
        for m in re.finditer(wzor, tresc):
            if m.group() not in mapa:
                mapa[m.group()] = f"[{nazwa}_{len(mapa)+1}]"
    for orig, zast in mapa.items():
        tresc = tresc.replace(orig, zast)
    return tresc, mapa

def przywroc(tresc: str, mapa: dict) -> str:
    for orig, zast in mapa.items():
        tresc = tresc.replace(zast, orig)
    return tresc
```

⚠️ **P51 z kursu 1 obowiązuje w pełni: filtr regexowy przepuści to, czego nie
przewidziałeś.** Nazwisko w treści umowy nie pasuje do żadnego wzorca. Dlatego:

⭐ **Prawdziwą granicą jest `KATALOGI_ZAKAZANE`, nie `WZORCE_ZAKAZANE`.** Reguła
„treść z `~/dokumenty` **nigdy** nie wychodzi" jest jednoznaczna i nie zależy od
pomysłowości wzorców. Wzorce to druga warstwa — łapią przypadkowe wklejenie, nie
systematyczny wyciek.

### 2.1 · Jedno wyjście, twardo

```python
# $OSA/router/wyjscie.py
import os, pathlib
"""JEDYNA funkcja w systemie wykonująca żądanie do chmury."""
def wyslij_na_zewnatrz(tresc, zrodlo, powod, zgoda=False, anonimizuj_auto=True):
    sprawdz(tresc, zrodlo, zgoda_jawna=zgoda)          # 1. bramka
    mapa = {}
    if anonimizuj_auto:
        tresc, mapa = anonimizuj(tresc)                 # 2. zastępniki
    _audyt(tresc, zrodlo, powod, mapa)                  # 3. ⭐ ślad ZAWSZE
    odp = _wywolaj_claude(tresc)                        # 4. dopiero teraz
    return przywroc(odp, mapa)

def _audyt(tresc, zrodlo, powod, mapa):
    """Pełny zapis. Dzięki temu §6 jest możliwe."""
    with open(pathlib.Path(os.environ["OSA"], "dziennik/wyjscie.jsonl"),
              "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "ts": TERAZ(), "zrodlo": zrodlo, "powod": powod,
            "znakow": len(tresc),
            "sha256": hashlib.sha256(tresc.encode()).hexdigest(),
            "anonimizowano": list(mapa.values()),
            "pierwsze_200": tresc[:200],
        }, ensure_ascii=False) + "\n")
```

⭐ **`sha256` pełnej treści bez samej treści** to dobry kompromis: możesz udowodnić,
**co** wysłałeś (porównując skrót), nie tworząc drugiej kopii swoich danych
w dzienniku. Ta sama zasada co przy sanityzacji śladów w części 15.

---

## 3. Gdzie chmura realnie wygrywa

Nie zgaduj — **zmierz na swoim zbiorze złotym**. Ale oto, gdzie spodziewać się
różnicy i gdzie jej nie ma:

| Zadanie | Lokalny | Chmura | Werdykt |
| :-- | :-- | :-- | :-- |
| Klasyfikacja, ekstrakcja z gramatyką | ⭐ | ⭐ | **lokalny** — remis, więc taniej |
| Wyszukanie z cytatem | ⭐ | ⭐ | **lokalny** |
| Polski język potoczny | ⭐ Bielik | ⭐ | **lokalny** |
| Rozumowanie 10+ kroków | ⚠️ | ⭐⭐ | **chmura**, jeśli wolno |
| Kod w mniej typowym języku | ⚠️ | ⭐⭐ | chmura |
| Bardzo długi kontekst (>100 k) | ✗ | ⭐⭐ | chmura |
| Synteza z 20 źródeł | ⚠️ | ⭐⭐ | zależy — **zmierz** |
| Praca masowa, nocna | ⭐⭐ | 💸 | ⭐ **lokalny, bezdyskusyjnie** |
| Cokolwiek z Twoimi dokumentami | ⭐ | ✗ | **lokalny — bramka** |

⭐ **Ostatni wiersz wyklucza większość tego, co robi Twój system.** Archiwista nigdy
nie pójdzie do chmury. Gospodarz prawie nigdy. Realnym kandydatem jest **Badacz** —
bo pracuje na treści publicznej, którą i tak przed chwilą pobrał z internetu.

> 💡 **To jest ciekawa konsekwencja Twojej architektury: jedyny agent, którego wolno
> wysłać do chmury, to ten, który przetwarza dane najmniej wrażliwe.** Granica
> prywatności i granica zaufania pokrywają się prawie idealnie — tylko odwrotnie.

---

## 4. Klient Claude — minimum, które działa

Utrzymuję to krótko, bo chmura jest u Ciebie wyjątkiem. Ale ma działać poprawnie.

```python
# $OSA/router/klient_claude.py
"""Wywoływany WYŁĄCZNIE przez wyjscie.py. Nigdy bezpośrednio."""
import anthropic, os

KLIENT = anthropic.Anthropic()       # ANTHROPIC_API_KEY ze środowiska BRAMY (nie piaskownicy!)
MODEL  = "claude-opus-5"

def _wywolaj_claude(tresc: str, system: str = "", max_tokens=4096) -> str:
    with KLIENT.messages.stream(                 # ⭐ strumień: brak timeoutu przy długim wyjściu
        model=MODEL,
        max_tokens=max_tokens,
        thinking={"type": "adaptive"},           # ⭐ myślenie adaptacyjne
        system=[{"type": "text", "text": system,
                 "cache_control": {"type": "ephemeral"}}] if system else [],
        messages=[{"role": "user", "content": tresc}],
    ) as s:
        wiadomosc = s.get_final_message()

    if wiadomosc.stop_reason == "refusal":       # ⚠️ P134 — sprawdź PRZED czytaniem treści
        raise Odmowa("Model odmówił odpowiedzi (stop_reason=refusal).")

    return "".join(b.text for b in wiadomosc.content if b.type == "text")
```

**Cztery rzeczy, które łatwo zrobić źle:**

| Rzecz | Poprawnie |
| :-- | :-- |
| Myślenie | `thinking={"type": "adaptive"}`. ⚠️ `budget_tokens` jest **odrzucane błędem 400** na Opus 5 |
| Próbkowanie | ⚠️ **`temperature`, `top_p`, `top_k` → 400.** Przyzwyczajenie z modeli lokalnych |
| Strumieniowanie | domyślnie przy długim wyjściu — inaczej timeout żądania |
| Odmowa | `stop_reason == "refusal"` sprawdzany **przed** czytaniem `content` |

⚠️ **Klucz API żyje w środowisku bramy i nigdy nie trafia do piaskownicy** (część 10,
P101). Agent nie ma klucza — ma **zdolność** wywołania przez bramę, którą brama widzi
i może odrzucić.

---

## 5. Router

```python
# $OSA/router/router.py
"""Trzy pytania w kolejności. Prywatność jest BRAMKĄ, nie wagą."""

SILNIKI = {
    "lokalny_szybki": {"url": "http://127.0.0.1:8080/v1", "model": "gpt-oss-20b",
                       "okno": 32768, "s_na_1k": 1.2, "poziom": 1},
    "lokalny_mocny":  {"url": "http://127.0.0.1:8080/v1", "model": "qwen3-32b",
                       "okno": 32768, "s_na_1k": 3.4, "poziom": 2},
    "chmura":         {"model": "claude-opus-5", "okno": 1_000_000,
                       "usd_we": 5.0, "usd_wy": 25.0, "poziom": 3},
}

def wybierz(zadanie: dict) -> tuple[str, str]:
    # 1 · PRYWATNOŚĆ — bramka
    try:
        sprawdz(zadanie["tresc"], zadanie["zrodlo"])
        wolno_na_zewnatrz = True
    except Odmowa as e:
        wolno_na_zewnatrz, powod_blokady = False, str(e)

    # 2 · TWARDE OGRANICZENIA
    if zadanie["tokenow"] > 30_000:
        if not wolno_na_zewnatrz:
            return "lokalny_mocny", f"za długie, ale {powod_blokady} → dzielę na etapy"
        return "chmura", "kontekst przekracza okno lokalne"

    # 3 · ZDOLNOŚĆ — z pomiaru, nie z przeczucia
    poziom = _wymagany_poziom(zadanie["kategoria"])     # z tabeli §5.1
    if poziom <= 1: return "lokalny_szybki", "kategoria w zasięgu małego modelu"
    if poziom <= 2: return "lokalny_mocny",  "wymaga mocniejszego lokalnego"
    if not wolno_na_zewnatrz:
        return "lokalny_mocny", f"wymagałoby chmury, ale {powod_blokady} → próbuję lokalnie"
    return "chmura", "zmierzona przewaga chmury w tej kategorii"
```

### 5.1 · Tabela poziomów — wypełniasz pomiarem, nie intuicją

```bash
# Uruchom zbiór złoty (część 14) na wszystkich trzech silnikach
for s in lokalny_szybki lokalny_mocny chmura; do
  python3 ewaluacja/uruchom.py --silnik $s --przebiegow 3 > pomiary/router/$s.json
done
python3 router/zbuduj_tabele.py > router/poziomy.json
```

| Kategoria | szybki | mocny | chmura | **wymagany poziom** |
| :-- | --: | --: | --: | --: |
| wyszukanie_z_cytatem | | | | |
| synteza | | | | |
| poprawna_odmowa | | | | |
| wieloetapowe | | | | |
| odpornosc | | | | |

⭐ **Reguła wypełniania: wymagany poziom to NAJNIŻSZY, który osiąga co najmniej 90 %
wyniku najlepszego.** Nie najwyższy dostępny. Jeśli mały model daje 88 % tego, co
chmura — wybierasz mały, bo różnica nie jest warta wyjścia z maszyny.

### 5.2 · Eskalacja, która nie łamie bramki

```python
def wykonaj_z_eskalacja(zadanie, prog_pewnosci=0.6):
    silnik, powod = wybierz(zadanie)
    wynik = _uruchom(silnik, zadanie)
    if wynik["pewnosc"] >= prog_pewnosci or SILNIKI[silnik]["poziom"] == 3:
        return wynik
    wyzsze = [n for n, s in SILNIKI.items() if s["poziom"] > SILNIKI[silnik]["poziom"]]
    for n in sorted(wyzsze, key=lambda x: SILNIKI[x]["poziom"]):
        if n == "chmura":
            try: sprawdz(zadanie["tresc"], zadanie["zrodlo"])   # ⭐ BRAMKA PONOWNIE
            except Odmowa: continue                              # ⚠️ P132
        w = _uruchom(n, zadanie)
        if w["pewnosc"] >= prog_pewnosci:
            return w
    return wynik
```

⚠️ **Linia `sprawdz()` wewnątrz pętli eskalacji jest tą, o której się zapomina** —
i to jest **najczęstsza droga, jaką dane wyciekają z systemów hybrydowych**. Ścieżka
główna sprawdza prywatność, ścieżka awaryjna nie. Sprawdzaj na **każdym** przejściu
granicy.

---

## 6. EKSPERYMENT 17 — audyt wyjścia

⭐ **Pytanie: co naprawdę opuściło Twoją maszynę w ostatnim tygodniu?**

```bash
python3 router/audyt.py --okres 7d
```

```
═══ AUDYT WYJŚCIA · 7 dni ═══
  żądań do chmury:        23
  znaków wysłanych:   184 200
  tokenów we/wy:    46 100 / 12 400
  koszt:                $0,54

  wg agenta:        badacz 21 · nadzorca 2 · archiwista 0 ✓ · gospodarz 0 ✓
  wg powodu:        kontekst za długi 11 · zmierzona przewaga 9 · eskalacja 3
  anonimizowano:    e-mail 14× · telefon 3× · NIP 1×
  ⚠️ odrzucone przez bramkę: 7   (4× katalog zakazany, 3× wzorzec)

  ⚠️ DO PRZEJRZENIA: 2 żądania z >20 000 znaków
     2026-09-21 14:02  badacz  sha 8f3a…  „Przeanalizuj poniższe 14 artykułów…"
     2026-09-23 09:41  badacz  sha c21e…  „Porównaj stanowiska w tych dokumentach…"
```

**Cztery pytania do tego raportu:**

1. **Czy Archiwista i Gospodarz mają zero?** Jeśli nie — masz błąd architektury,
   nie konfiguracji.
2. **Czy 7 odrzuceń to były pomyłki, czy realne próby?** Przejrzyj każde.
3. **Czy dwa duże żądania musiały być tak duże?** Zwykle dało się streścić lokalnie
   i wysłać streszczenie.
4. **Czy powód „eskalacja" × 3 oznacza, że próg pewności jest za wysoki?**

### 6.1 · Test pełnego offline

```bash
sudo nft add rule inet filter output ip daddr != 127.0.0.1 drop   # odetnij
python3 ewaluacja/uruchom.py --przebiegow 3 --oczekuj-offline
sudo nft flush chain inet filter output                            # przywróć
```

| Miara | Online | Offline | Δ |
| :-- | --: | --: | --: |
| Wynik zbioru złotego | | | |
| Zadań zakończonych | | | |
| Zadań zdegradowanych | 0 | | |
| **Zadań nieudanych** | | | ⭐ **cel: 0** |

⭐ **Kryterium zaliczenia: zero zadań NIEUDANYCH.** Zdegradowane (gorszy wynik,
wyraźnie oznaczony) są w porządku. Nieudane oznaczają **ciche uzależnienie od chmury**
— coś w systemie zakłada sieć i nie ma ścieżki zapasowej. To jest P52 z kursu 1
i najlepszy sposób, żeby go u siebie znaleźć.

---

## 7. ĆWICZENIE

1. Zaimplementuj `granica.py` z **jedną** funkcją wyjścia. Zaudytuj kod: żadne inne
   miejsce nie wykonuje żądania na zewnątrz.

```bash
grep -rn "anthropic\|api.anthropic\|requests.post\|urlopen" $OSA --include=*.py \
  | grep -v "router/klient_claude.py\|piaskownica/proxy.py"
# oczekuj: pusto
```

2. Zbuduj tabelę poziomów **pomiarem** na zbiorze złotym.
3. Router z trzema pytaniami i bramką **także w eskalacji**.
4. Audyt wyjścia + cotygodniowy raport w zadaniu nocnym (część 11).
5. Test offline. Napraw każde nieudane zadanie.
6. Napisz `decyzje/0005-granica-prywatnosci.md`: co **nigdy** nie wychodzi, co za
   zgodą, co swobodnie — i jak to jest **wymuszone**.

---

## 8. Pułapki tej części

| ID | Pułapka | Objaw | Jak uniknąć |
| :-- | :-- | :-- | :-- |
| **P132** | **Bramka prywatności omijana w eskalacji** | Ścieżka główna sprawdza, awaryjna nie — i tędy wycieka | `sprawdz()` przy **każdym** przejściu granicy, nie raz na zadanie |
| **P133** | **Granica oparta na wzorcach zamiast na źródle** | Nazwisko w umowie nie pasuje do regexa i wychodzi | Katalogi zakazane są granicą; wzorce to druga warstwa |
| **P134** | **Nieprzeczytany `stop_reason`** | Odmowa modelu czytana jak pusta odpowiedź; agent idzie dalej z niczym | `stop_reason == "refusal"` sprawdzany **przed** `content` |
| **P135** | **Ciche uzależnienie od chmury** | Brak sieci → system nie działa, choć „lokalny jest domyślny" | Test offline, kryterium: zero zadań **nieudanych** |

---

## 9. Checkpoint

```bash
cd $OSA
python3 - <<'EOF'
from router.granica import sprawdz, Odmowa, anonimizuj, przywroc
try: sprawdz("cokolwiek", "/home/u/dokumenty/umowa.txt"); print("✗ P133")
except Odmowa: print("✓ katalog zakazany")
try: sprawdz("NIP 1234567890", "/tmp/x"); print("✗ wzorzec")
except Odmowa: print("✓ wzorzec")
t, m = anonimizuj("kontakt: jan@example.com, tel 501234567")
assert "@" not in t and przywroc(t, m).count("jan@") == 1
print("✓ anonimizacja odwracalna")
EOF
python3 router/audyt.py --okres 7d
python3 ewaluacja/uruchom.py --offline --wymagaj-zero-nieudanych \
  && echo "✓ pełny offline bez zadań nieudanych"
git add -A && git commit -m "część 17: router, granica prywatności, audyt wyjścia, offline"
```

- [ ] Kolejność pytań: **prywatność → zdolność → koszt**, i prywatność jest bramką
- [ ] Granica oparta na **źródle**, wzorce jako druga warstwa
- [ ] **Jedna** funkcja wyjścia w całym systemie — zweryfikowane `grep`-em
- [ ] Każde wyjście zostawia ślad ze skrótem treści
- [ ] Anonimizacja odwracalna
- [ ] Tabela poziomów wypełniona **pomiarem**; reguła 90 %
- [ ] Bramka sprawdzana **także w eskalacji**
- [ ] Klucz API w środowisku bramy, **nigdy** w piaskownicy
- [ ] ⭐ **Audyt pokazuje: Archiwista i Gospodarz — zero wyjść**
- [ ] ⭐ **Pełny offline: zero zadań nieudanych**

---

**Dalej: `18-WYDANIE-I-UTRZYMANIE.md`** — wersjonowanie, wycofanie i runbook na
trzecią w nocy.
