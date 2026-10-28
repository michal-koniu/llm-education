# Część 7 · Narzędzia — projekt i ergonomia

**Poziom:** ⭐⭐⭐⭐ · **Czas:** ~5 h · **Wymaga:** części 4 (budżet) i 6 (składanie promptu)
**Produkuje:** rejestr narzędzi, przycinanie obserwacji, klucze idempotencji, ablację liczby narzędzi

---

## 0. Narzędzie to interfejs użytkownika, którego użytkownikiem jest model

Piszesz narzędzie tak, jakbyś pisał je dla juniora, który:

- przeczyta **tylko opis**, nigdy kod,
- nie zapamięta niczego między turami,
- pod presją **zgadnie** zamiast zapytać,
- i przy błędzie albo się podda, albo powtórzy to samo.

Każda z tych czterech cech ma odpowiadającą jej regułę projektową. Cała ta część to
ich rozwinięcie.

> ⭐ **Arytmetyka z części 1 wraca tutaj i jest sednem sprawy.** Przy 92 % skuteczności
> na krok 15 kroków daje 29 %. **Projektowanie narzędzi to główna dźwignia podnoszenia
> tych 92 %** — i jednocześnie dźwignia skracania łańcucha, bo lepsze narzędzie robi
> w jednym kroku to, co gorsze w trzech.

---

## 1. Anatomia narzędzia

```python
{
  "nazwa": "czytaj_dokument",
  "opis": ("Czyta dokument tekstowy lub PDF z archiwum. Zwraca treść. "
           "Przy dokumentach > 500 linii zwraca początek i koniec — "
           "wtedy użyj `szukaj_w_dokumencie`, żeby dostać środek."),
  "parametry": {
    "sciezka": {
      "typ": "string",
      "opis": "Ścieżka względem ~/dokumenty, np. 'faktury/2026/03/orange.pdf'. "
              "Ścieżki bezwzględne są odrzucane.",
      "wymagany": True
    },
    "od_linii": {
      "typ": "integer",
      "opis": "Numer pierwszej linii (od 1). Domyślnie 1.",
      "wymagany": False, "domyslnie": 1
    }
  }
}
```

**Pięć rzeczy, które ten opis robi dobrze:**

1. **Mówi, co zwraca** — nie tylko co robi.
2. **Ostrzega o zachowaniu brzegowym** — obcięcie przy >500 linii.
3. **Kieruje do narzędzia następnego** — „wtedy użyj `szukaj_w_dokumencie`". To jest
   najtańszy sposób nauczenia modelu sekwencji.
4. **Podaje przykład formatu** — `'faktury/2026/03/orange.pdf'` mówi więcej niż zdanie.
5. **Mówi, co jest odrzucane** — model nie traci tury na próbę.

### 1.1 · Nazewnictwo

| Zasada | ✗ | ✓ |
| :-- | :-- | :-- |
| Czasownik + rzeczownik | `dokument`, `pdf_handler` | `czytaj_dokument` |
| Bez skrótów | `rd_doc`, `get_fl` | `czytaj_dokument` |
| Jednoznaczne wobec reszty | `szukaj` i `znajdz` obok siebie | `szukaj_w_dokumencie`, `znajdz_dokumenty` |
| Konsekwentny język | `read_file` obok `zapisz_plik` | jeden język w całym zestawie |

⚠️ **Trzeci wiersz jest tym, który boli najbardziej.** Dwa narzędzia o podobnych
nazwach i nakładających się opisach to **gwarantowany błąd wyboru**, i to taki, którego
nie naprawisz lepszym promptem. Anthropic mówi o tym wprost: narzędzia mają
**minimalizować nakładanie się funkcji**. Jeśli nie umiesz w jednym zdaniu powiedzieć,
kiedy użyć A, a kiedy B — **scal je albo usuń jedno**.

---

## 2. Pobłażliwe wejście, surowe wyjście

Reguła Steinbergera z MCP Best Practices, przepisana:

> Parsowanie parametrów powinno być pobłażliwe (np. przyjmij `path`, gdy formalnie
> zdefiniowano `project_path`).

```python
ALIASY = {
    "sciezka": ["path", "plik", "file", "sciezka_pliku", "filepath"],
    "od_linii": ["from_line", "start", "od"],
}

def normalizuj(argumenty: dict, schemat: dict) -> dict:
    """Model pomyli nazwę parametru. Nie karz go za to turą."""
    wynik = {}
    for kanon, spec in schemat.items():
        if kanon in argumenty:
            wynik[kanon] = argumenty[kanon]
            continue
        for alias in ALIASY.get(kanon, []):
            if alias in argumenty:
                wynik[kanon] = argumenty[alias]
                break
        else:
            if spec.get("wymagany"):
                raise BladNarzedzia(
                    f"Brak wymaganego parametru '{kanon}'. "
                    f"Podałeś: {list(argumenty)}. "
                    f"Oczekiwane: {list(schemat)}.")
            if "domyslnie" in spec:
                wynik[kanon] = spec["domyslnie"]
    return wynik
```

⭐ **Jedna tura zmarnowana na literówkę w nazwie parametru kosztuje Cię ~2 sekundy
i ~400 tokenów.** Trzydzieści linii aliasów zwraca się pierwszego dnia.

**Ale wyjście musi być surowe i przewidywalne.** Pobłażliwość na wejściu, rygor na
wyjściu — bo wyjście czyta model i każda niespójność go myli.

---

## 3. Kształtowanie obserwacji — gdzie umiera kontekst

To jest miejsce, w którym agenci przegrywają najczęściej, i jednocześnie najłatwiejsze
do naprawienia.

```
ls -R ~/dokumenty        → 14 200 tokenów      ← pół okna, jednym wywołaniem
cat duza-umowa.pdf       →  8 900 tokenów
git log                  →  6 100 tokenów
```

### 3.1 · Cztery techniki, w kolejności użycia

**1 · Przycinanie z zachowaniem obu końców**

```python
def przytnij(tresc: str, limit=2000) -> str:
    if len(tresc) <= limit:
        return tresc
    p = limit // 2
    return (tresc[:p] +
            f"\n\n[… wycięto {len(tresc)-limit} znaków. "
            f"Użyj węższego zapytania, jeśli potrzebujesz środka …]\n\n" +
            tresc[-p:])
```

⭐ **Środek jest wycinany celowo.** W wynikach poleceń informacja koncentruje się na
brzegach: początek to nagłówek i struktura, koniec to podsumowanie, błędy i status.
Środek to zwykle powtarzalna lista.

**2 · Podsumowanie strukturalne zamiast surowego wyniku**

```python
def podsumuj_liste_plikow(sciezki: list) -> str:
    """Zamiast 14 tys. tokenów listy — 200 tokenów struktury."""
    from collections import Counter
    katalogi = Counter(str(pathlib.Path(s).parent) for s in sciezki)
    rozszerz = Counter(pathlib.Path(s).suffix for s in sciezki)
    return (f"{len(sciezki)} plików w {len(katalogi)} katalogach.\n"
            f"Największe katalogi: " +
            ", ".join(f"{k} ({n})" for k, n in katalogi.most_common(8)) + "\n"
            f"Typy: " + ", ".join(f"{e or '(brak)'} ({n})" for e, n in rozszerz.most_common()) +
            "\n\nUżyj `znajdz_dokumenty(wzorzec)`, żeby zawęzić.")
```

**3 · Stronicowanie z jawnym wskaźnikiem**

```
Wyniki 1–20 z 340. Aby zobaczyć kolejne: znajdz_dokumenty(..., od=21).
```

**4 · Odesłanie zamiast treści** — wynik ląduje w pliku, model dostaje ścieżkę i nagłówek.
To jest doładowanie w ostatniej chwili z części 4, zastosowane do wyjścia narzędzia.

### 3.2 · Budżet per narzędzie

```python
LIMITY = {
    "czytaj_dokument":   4000,   # czasem naprawdę trzeba dużo
    "znajdz_dokumenty":   800,   # lista — wystarczy podsumowanie
    "powloka":           2000,
    "szukaj_w_sieci":    1500,   # ⚠️ najbardziej niezaufane, najkrócej
}
```

⚠️ **`szukaj_w_sieci` ma najniższy limit nieprzypadkowo.** Im mniej obcego tekstu
wpuszczasz do kontekstu, tym mniejsza powierzchnia wstrzyknięcia. **Limit tokenów jest
tu środkiem bezpieczeństwa, nie tylko oszczędnością.** Wraca w częściach 10 i 16.

---

## 4. Błąd jest promptem

Rozwinięcie drabiny z części 3. Dobry komunikat błędu ma **trzy części**:

```
CO poszło źle    +    DLACZEGO    +    CO WOLNO ZAMIAST TEGO
```

| ✗ Zły | ✓ Dobry |
| :-- | :-- |
| `FileNotFoundError: faktury/orange.pdf` | `Nie ma pliku 'faktury/orange.pdf'. W katalogu 'faktury/' są podkatalogi: 2025/, 2026/. Spróbuj 'faktury/2026/orange.pdf' albo użyj znajdz_dokumenty("orange").` |
| `PermissionError: [Errno 13]` | `Brak prawa zapisu do /etc/hosts. Wolno pisać tylko w ~/dokumenty i /tmp. Jeśli to wynik pośredni — użyj /tmp/wynik.txt.` |
| `TimeoutError` | `Polecenie przekroczyło 30 s i zostało przerwane. Jeśli przetwarzasz wiele plików — podziel na partie po 50 i wywołaj kilka razy.` |
| `JSONDecodeError: line 1 col 1` | `Zwróciłeś tekst, a oczekiwano JSON. Twoja odpowiedź zaczynała się od 'Oczywiście, oto...'. Zwróć SAM obiekt JSON, bez wstępu.` |

```python
class BladNarzedzia(Exception):
    def __init__(self, co, dlaczego="", zamiast=""):
        self.tresc = co + (f" {dlaczego}" if dlaczego else "") + \
                     (f"\nSpróbuj: {zamiast}" if zamiast else "")
        super().__init__(self.tresc)

# Użycie — zauważ, że podpowiedź jest WYLICZANA, nie stała:
raise BladNarzedzia(
    co=f"Nie ma pliku '{s}'.",
    dlaczego=f"W '{rodzic}' są: {', '.join(sasiedzi[:6])}.",
    zamiast=f"znajdz_dokumenty('{pathlib.Path(s).stem}')")
```

⭐ **„Wyliczana, nie stała" jest tu istotne.** Podpowiedź zawierająca **rzeczywistą
zawartość katalogu** podnosi szansę poprawy z ~20 % do ponad 90 %. Stała podpowiedź
(„sprawdź ścieżkę") nie daje prawie nic.

---

## 5. Idempotencja — narzędzie, które wolno powtórzyć

Agent powtarza wywołania: po timeoucie, po niejasnym wyniku, po restarcie sesji. Jeśli
narzędzie ma skutek uboczny, powtórzenie **robi ten skutek dwa razy**.

```python
import hashlib, json, os, pathlib

def klucz_idempotencji(narzedzie: str, argumenty: dict) -> str:
    return hashlib.sha256(
        (narzedzie + json.dumps(argumenty, sort_keys=True)).encode()).hexdigest()[:16]

class RejestrSkutkow:
    """Wykonane operacje ze skutkiem ubocznym. Powtórzenie zwraca poprzedni wynik."""
    def __init__(self, plik="$OSA/skutki.json"):
        self.p = pathlib.Path(os.path.expandvars(plik)).expanduser()
        self.d = json.loads(self.p.read_text()) if self.p.exists() else {}

    def wykonaj_raz(self, narzedzie, argumenty, funkcja):
        k = klucz_idempotencji(narzedzie, argumenty)
        if k in self.d:
            return (f"[już wykonane {self.d[k]['kiedy']}] {self.d[k]['wynik']}")
        wynik = funkcja(**argumenty)
        self.d[k] = {"kiedy": TERAZ(), "wynik": str(wynik)[:500]}
        self.p.write_text(json.dumps(self.d, ensure_ascii=False, indent=1))
        return wynik
```

| Narzędzie | Idempotentne? | Uwaga |
| :-- | :-- | :-- |
| `czytaj_dokument` | ⭐ tak | odczyt — powtarzaj dowolnie |
| `znajdz_dokumenty` | ⭐ tak | — |
| `zmien_nazwe` | ✗ **nie** | ⚠️ drugie wywołanie zmienia nazwę już zmienionej |
| `wyslij_wiadomosc` | ✗ **nie** | ⚠️⚠️ podwójna wysyłka jest widoczna dla ludzi |
| `dopisz_do_pliku` | ✗ **nie** | wpis dwa razy |

⚠️ **Zapisz w rejestrze narzędzi, które są idempotentne, i traktuj to jako pole
obowiązkowe.** Narzędzie bez zadeklarowanej idempotencji domyślnie uznajesz za
nieidempotentne i przepuszczasz przez `wykonaj_raz`.

---

## 6. Ile narzędzi to za dużo

Tu jest twardy kompromis i mało kto go mierzy.

```
     TRAFNOŚĆ WYBORU NARZĘDZIA vs LICZBA NARZĘDZI  (kształt spodziewany)

  95% ┤●●●●●●
      │      ●●●●●
  85% ┤           ●●●●
      │               ●●●●
  70% ┤                   ●●●●●
      │                        ●●●●●●●
  50% ┤                               ●●●●
      └──┬─────┬─────┬─────┬─────┬─────┬───
         3     8    15    25    40    60
```

Dwa mechanizmy działają jednocześnie i oba pogarszają sprawę:

1. **Koszt kontekstu** — 40 narzędzi × ~200 tokenów = 8 tys. tokenów **w każdej turze**.
2. **Niejednoznaczność wyboru** — im więcej narzędzi, tym więcej par o nakładających
   się opisach.

### 6.1 · Trzy strategie

| Strategia | Jak | Koszt | Kiedy |
| :-- | :-- | :-- | :-- |
| **A · mniej narzędzi** | scal podobne, usuń nieużywane | zero | ⭐ zawsze najpierw |
| **B · doładowanie** | pokaż 5 podstawowych + `znajdz_narzedzie(opis)` | 1 tura przy rzadkich | >15 narzędzi |
| **C · code-mode** | narzędzia jako funkcje w kodzie, nie w prompcie | patrz część 8 | ⭐⭐ >25 narzędzi |

**Strategia A jest niedoceniana.** Zanim dołożysz mechanizm, sprawdź dziennik: ilu
narzędzi agent użył **choć raz** w ostatnich 100 sesjach?

```bash
python3 sesja-cli.py statystyki-narzedzi --ostatnie 100
# nazwa              użyć   % sesji   błędów
# czytaj_dokument     412      94%       3%
# znajdz_dokumenty    388      91%       1%
# powloka             201      44%      12%   ← wysoki błąd, zobacz §4
# konwertuj_docx        4       2%      50%   ← ⚠️ kandydat do usunięcia
# ocr_skan              0       0%        —   ← ⚠️⚠️ usuń
```

⭐ **Narzędzie użyte w 2 % sesji kosztuje kontekst w 100 % sesji.** To jest zły
interes i najprostsza optymalizacja w całym kursie.

### 6.2 · Promień rażenia jako kryterium projektowe

Steinberger planuje zmiany według **promienia rażenia** — ile plików ruszy. Ta sama
jednostka świetnie działa przy projektowaniu narzędzi:

| Promień | Przykład | Wymagania |
| :-- | :-- | :-- |
| **Zerowy** (odczyt) | `czytaj_dokument` | brak; idempotentne z definicji |
| **Punktowy** (1 obiekt) | `zmien_nazwe(plik)` | dziennik, idempotencja |
| **Lokalny** (do 10) | `zmien_nazwy(wzorzec)` | ⭐ **tryb `--sucho` obowiązkowy** |
| **Szeroki** (>10) | `przenies_katalog` | ⭐⭐ potwierdzenie człowieka + kopia |
| **Nieodwracalny** | `wyslij_mail`, `usun` | ⭐⭐⭐ potwierdzenie + **nie dawaj agentowi** |

```python
def wymaga_zgody(narzedzie: dict, argumenty: dict, granice: dict) -> bool:
    promien = narzedzie["promien"](argumenty)       # wyliczany, nie stały
    return promien >= granice.get("prog_zgody", 10)
```

⚠️ **Promień musi być wyliczany z argumentów, nie z nazwy narzędzia.**
`zmien_nazwy("*.txt")` ma promień 3 albo 3000 zależnie od katalogu — i to jest
właśnie ta różnica, która decyduje, czy pytać.

---

## 7. OD ZERA — rejestr narzędzi

```python
# $OSA/narzedzia/rejestr.py
"""Rejestr: jedno miejsce na schemat, limity, promień i idempotencję."""
import json, time, inspect

class Rejestr:
    def __init__(self, budzet_obserwacji=2000):
        self.n, self.budzet = {}, budzet_obserwacji

    def dodaj(self, nazwa, opis, parametry, funkcja, *,
              limit=None, idempotentne=False, promien=lambda a: 0, zaufanie="host"):
        self.n[nazwa] = dict(nazwa=nazwa, opis=opis, parametry=parametry,
                             funkcja=funkcja, limit=limit or self.budzet,
                             idempotentne=idempotentne, promien=promien,
                             zaufanie=zaufanie)

    def schemat(self, poziom_zaufania="host", tylko=None) -> list:
        """To, co trafia do promptu. Filtrowane po zaufaniu sesji — P88."""
        rzad = {"piaskownica": 0, "host": 1}
        out = []
        for n in self.n.values():
            if rzad[poziom_zaufania] < rzad[n["zaufanie"]]:
                continue                       # sesja niezaufana NIE WIDZI narzędzia
            if tylko and n["nazwa"] not in tylko:
                continue
            out.append({k: n[k] for k in ("nazwa", "opis", "parametry")})
        return out

    def wywolaj(self, nazwa, argumenty, kontekst) -> dict:
        if nazwa not in self.n:
            bliskie = [k for k in self.n if nazwa[:4] in k]
            raise BladNarzedzia(f"Nie ma narzędzia '{nazwa}'.",
                                f"Dostępne: {', '.join(self.schemat_nazw(kontekst))}.",
                                bliskie[0] if bliskie else "")
        n = self.n[nazwa]
        if kontekst["zaufanie"] == "piaskownica" and n["zaufanie"] == "host":
            raise BladNarzedzia(f"'{nazwa}' niedostępne w tej sesji.",
                                "Sesja ma poziom 'piaskownica'.", "")
        arg = normalizuj(argumenty, n["parametry"])
        if n["promien"](arg) >= kontekst.get("prog_zgody", 10) and not kontekst.get("zgoda"):
            return {"status": "wymaga_zgody",
                    "tresc": f"Operacja dotknie ~{n['promien'](arg)} obiektów. "
                             f"Potwierdź, żeby wykonać."}
        t0 = time.time()
        try:
            wynik = (kontekst["skutki"].wykonaj_raz(nazwa, arg, n["funkcja"])
                     if not n["idempotentne"] else n["funkcja"](**arg))
            status = "ok"
        except BladNarzedzia as e:
            wynik, status = e.tresc, "blad"
        except Exception as e:
            wynik, status = f"Nieoczekiwany błąd: {type(e).__name__}: {e}", "blad"
        return {"status": status, "tresc": przytnij(str(wynik), n["limit"]),
                "ms": int((time.time() - t0) * 1000)}
```

**Trzy rzeczy, które ten rejestr robi, a większość implementacji nie:**

1. **Filtruje narzędzia po poziomie zaufania sesji** — sesja z piaskownicy nawet **nie
   widzi** narzędzi hosta. Niewidoczne narzędzie nie zostanie wywołane ani opisane
   atakującemu.
2. **Wylicza promień z argumentów** i pyta o zgodę.
3. **Nigdy nie wypuszcza surowego traceback** — każdy wyjątek wraca jako czytelny tekst.

---

## 8. PRODUKCYJNIE

| | Anthropic tool use | MCP | LangChain | **Twój rejestr** |
| :-- | :-- | :-- | :-- | :-- |
| Schemat | JSON Schema | JSON Schema | Pydantic | dict |
| Walidacja `strict` | ⭐ tak | częściowo | ⭐ tak | ręcznie |
| **Pobłażliwe aliasy** | ✗ | ✗ | ✗ | ⭐ tak |
| **Filtr po zaufaniu** | ✗ | ✗ | ✗ | ⭐ tak |
| **Promień rażenia** | ✗ | ✗ | ✗ | ⭐ tak |
| **Idempotencja** | ręcznie | ⭐ konwencja | ✗ | ⭐ wymuszona |
| Doładowanie narzędzi | ⭐ tool search | ⭐ od 2026-07 | ✗ | ręcznie |

> 💡 **Jedna rzecz warta wzięcia z zewnątrz: JSON Schema zamiast własnego dict.**
> Nie dlatego, że ładniejsze — dlatego, że **`llama-server` potrafi wymusić JSON Schema
> na poziomie próbkowania** (gramatyki z kursu 1, część 3). Wymuszenie strukturalne to
> nie jest prośba do modelu, to jest gwarancja. Przy modelach lokalnych ta różnica jest
> znacznie większa niż przy frontier.

---

## 9. EKSPERYMENT 7 — ablacja liczby narzędzi

⭐ **Ten eksperyment da Ci liczbę, której nie znajdziesz w żadnej dokumentacji: ile
narzędzi wytrzymują Twoje modele.**

**Hipoteza:** trafność wyboru narzędzia spada nieliniowo z ich liczbą, a próg jest
**znacznie niższy** dla modeli lokalnych niż dla frontier.

### 9.1 · Przygotowanie

```bash
mkdir -p $OSA/pomiary/narzedzia && cd $OSA/pomiary/narzedzia
```

- **5 narzędzi realnych** — tych, których agent faktycznie używa.
- **35 atrap** — działających, ale nieistotnych (`sprawdz_pogode`, `konwertuj_waluty`,
  `generuj_qr`…). ⚠️ **Opisy muszą być wiarygodne**, nie „atrapa 7" — inaczej mierzysz
  coś innego.
- **40 zadań** z jednoznacznie poprawnym narzędziem.

```python
# zadania.py
ZADANIA = [
  ("Ile linii ma umowa-najem.txt?",          "czytaj_dokument"),
  ("Znajdź wszystkie faktury z marca",       "znajdz_dokumenty"),
  ("Zmień nazwę skan001.pdf na faktura.pdf", "zmien_nazwe"),
  ("Ile plików jest w ~/dokumenty?",         "powloka"),
  ("Co pamiętasz o moim rachunku za prąd?",  "przypomnij"),
  # … do 40, po 8 na każde narzędzie realne
]
```

### 9.2 · Przebieg

```bash
for n in 5 10 15 25 40; do
  python3 ablacja.py --narzedzi $n --model gpt-oss-20b --powtorzen 3
done
```

| Narzędzi w prompcie | Trafność wyboru | Tokeny (schematy) | Czas do 1. tokena | Błędne argumenty |
| --: | --: | --: | --: | --: |
| 5 | /40 | | | |
| 10 | /40 | | | |
| 15 | /40 | | | |
| 25 | /40 | | | |
| 40 | /40 | | | |

**Powtórz dla `qwen3-32b`.** Spodziewaj się, że model gęstszy wytrzyma więcej — i to
jest konkretny argument za routingiem z części 17.

### 9.3 · Eksperyment dodatkowy — które pary się mylą

```bash
python3 ablacja.py --narzedzi 40 --macierz-pomylek
# wypisz 10 najczęstszych par (oczekiwane → wybrane)
```

⭐ **To jest najbardziej praktyczny wynik z całej tej części.** Dostajesz konkretną
listę par narzędzi o nakładających się opisach. Dla każdej pary zrób jedno z trzech:
**scal**, **usuń jedno**, albo **przepisz oba opisy tak, żeby różnica była w pierwszym
zdaniu**. Potem zmierz ponownie.

⚠️ **Predykcja do sprawdzenia:** przy `gpt-oss-20b` spodziewam się wyraźnego spadku
już między 15 a 25 narzędziami i większości pomyłek **skoncentrowanych w 3–4 parach**,
nie rozłożonych równomiernie. Jeśli tak jest — naprawa czterech opisów kupi Ci
większość utraconej trafności bez żadnego mechanizmu.

---

## 10. ĆWICZENIE — przepisz zestaw narzędzi Archiwisty

1. Wypisz wszystkie narzędzia, jakie ma dziś, ze statystyką użycia.
2. **Usuń każde użyte w mniej niż 5 % sesji.** Bez sentymentów.
3. Dla każdego pozostałego uzupełnij: `limit`, `idempotentne`, `promien`, `zaufanie`.
4. Przepisz opisy według pięciu zasad z §1: co zwraca, zachowanie brzegowe, odesłanie
   do narzędzia następnego, przykład formatu, co jest odrzucane.
5. Napisz **trzy komunikaty błędu** w formacie CO + DLACZEGO + CO ZAMIAST, z podpowiedzią
   **wyliczaną** z rzeczywistego stanu.
6. Zmierz ponownie zadania z §9 na nowym zestawie.

```bash
python3 sesja-cli.py narzedzia archiwista --sprawdz
# oczekuj wykrycia:
#   ⚠️ 'szukaj' i 'znajdz' — opisy nakładają się w 71%
#   ⚠️ 'zmien_nazwe' — brak zadeklarowanej idempotencji
#   ⚠️ 'powloka' — promień stały, powinien być wyliczany z argumentów
#   ⚠️ 'ocr_skan' — 0 użyć w 100 sesjach
```

---

## 11. Pułapki tej części

| ID | Pułapka | Objaw | Jak uniknąć |
| :-- | :-- | :-- | :-- |
| **P86** | **Dwa narzędzia o nakładających się opisach** | Model losowo wybiera złe; prompt nie pomaga | Macierz pomyłek (§9.3). Nie umiesz w zdaniu powiedzieć, kiedy A a kiedy B → scal |
| **P87** | **Surowy traceback jako wynik narzędzia** | Agent widzi `Errno 13`, poddaje się albo powtarza to samo | Każdy wyjątek → CO + DLACZEGO + CO ZAMIAST, z podpowiedzią wyliczaną |
| **P88** | **Narzędzia niefiltrowane po zaufaniu sesji** | Sesja z kanału widzi `powloka`; wstrzyknięcie dostaje shell | Filtr w `schemat()` — niezaufana sesja **nie widzi** narzędzi hosta |
| **P89** | **Brak idempotencji przy skutku ubocznym** | Po timeoucie agent wysyła wiadomość drugi raz | Pole `idempotentne` obowiązkowe; brak = przepuszczasz przez `wykonaj_raz` |
| **P90** | **Promień rażenia stały zamiast wyliczanego** | `zmien_nazwy("*")` przechodzi bez pytania, bo „to tylko zmiana nazwy" | `promien` to funkcja argumentów, zawsze |

---

## 12. Checkpoint

```bash
cd $OSA
python3 - <<'EOF'
from narzedzia.rejestr import Rejestr
r = Rejestr()
r.dodaj("powloka", "…", {}, lambda: None, zaufanie="host")
r.dodaj("czytaj",  "…", {}, lambda: None, zaufanie="piaskownica")
assert len(r.schemat("piaskownica")) == 1, "P88: filtr zaufania nie działa"
assert len(r.schemat("host")) == 2
print("✓ filtr zaufania")
EOF
python3 sesja-cli.py narzedzia archiwista --sprawdz
test -s pomiary/narzedzia/ablacja.csv && echo "✓ ablacja przeprowadzona"
git add -A && git commit -m "część 7: rejestr narzędzi, obserwacje, promień, idempotencja"
```

- [ ] Opis narzędzia mówi, co zwraca, i kieruje do narzędzia następnego
- [ ] Wejście pobłażliwe (aliasy), wyjście surowe
- [ ] Obserwacje przycinane z zachowaniem obu końców, budżet per narzędzie
- [ ] Błąd ma trzy części, a podpowiedź jest **wyliczana** ze stanu
- [ ] Narzędzia nieidempotentne przechodzą przez rejestr skutków
- [ ] Promień rażenia wyliczany z argumentów, próg zgody działa
- [ ] Narzędzia filtrowane po poziomie zaufania sesji — **sprawdzone testem**
- [ ] ⭐ **Znasz swój próg liczby narzędzi i masz macierz pomyłek**

---

**Dalej: `08-CODE-MODE.md`** — największa zmiana 2026. Agent pisze program zamiast
wywoływać narzędzia, a Twój mały model nagle staje się dużo lepszy.
