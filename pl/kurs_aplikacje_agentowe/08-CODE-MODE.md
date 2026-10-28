# Część 8 · Code-mode — agent pisze program zamiast wywoływać narzędzia

**Poziom:** ⭐⭐⭐⭐⭐ · **Czas:** ~6 h · **Wymaga:** części 7 (narzędzia), kursu 1 cz. 7 (`bwrap`)
**Produkuje:** środowisko wykonania kodu, API narzędzi, porównanie obu trybów na liczbach

> ⭐ **To jest, obok części 3, najważniejsza część kursu — i najbardziej korzystna
> akurat dla Ciebie.** Powód wyjaśniam w §2 i jest zaskakująco prosty.

---

## 1. Problem, którego nie widać, dopóki się go nie zmierzy

Zadanie: *„Dla każdej faktury z marca sprawdź, czy jest opłacona, i wypisz nieopłacone
z sumą."*

**Tryb klasyczny — jedno wywołanie narzędzia na turę:**

```
tura  1  znajdz_dokumenty("faktury/2026/03")   → lista 23 plików     [1 200 tok.]
tura  2  czytaj_dokument("…/f001.pdf")          → treść              [  800 tok.]
tura  3  czytaj_dokument("…/f002.pdf")          → treść              [  800 tok.]
   …
tura 24  czytaj_dokument("…/f023.pdf")          → treść              [  800 tok.]
tura 25  model sumuje w głowie                                       [   -- ]

RAZEM:  25 tur · ~24 000 tokenów · ~90 s
RYZYKO: 0,92²⁴ = 13 % szans, że cały łańcuch przejdzie bez błędu
```

**Tryb code-mode — jeden program:**

```
tura 1   model pisze:

         faktury = znajdz("faktury/2026/03")
         nieoplacone = []
         for f in faktury:
             t = czytaj(f)
             if "opłacono" not in t.lower():
                 nieoplacone.append((f, kwota(t)))
         print(f"{len(nieoplacone)} nieopłaconych, suma {sum(k for _, k in nieoplacone)} zł")
         for f, k in nieoplacone: print(f"  {f}: {k} zł")

tura 2   wynik: "3 nieopłacone, suma 4 820 zł / f007.pdf: 1200 zł / …"   [120 tok.]

RAZEM:  2 tury · ~1 400 tokenów · ~12 s
RYZYKO: 0,92² = 85 %
```

**Siedemnastokrotnie mniej tokenów. Sześciokrotnie szybciej. Sześciokrotnie wyższa
szansa powodzenia.**

Publikowane redukcje kontekstu dla code-mode mieszczą się w przedziale **85–94 %**
([MCP Code Mode](https://medium.com/@amirkiarafiei/mcp-code-mode-context-engineering-for-efficient-tool-execution-in-llm-agents-c46e1ddf80ac)),
a smolagents raportuje **~30 % mniej wywołań modelu**. ⚠️ **Zmierzysz to u siebie w §8** —
i tam ta liczba będzie znaczyła coś realnego.

### 1.1 · Skąd bierze się oszczędność

Trzy niezależne mechanizmy, i warto je rozróżniać:

| Mechanizm | Co oszczędza |
| :-- | :-- |
| **Pętla wykonuje się w kodzie, nie w modelu** | 23 tury × pełna historia = główna pozycja |
| **Dane pośrednie nie wchodzą do kontekstu** | 23 × 800 tokenów treści faktur — model widzi tylko wynik |
| **Schematy narzędzi zastąpione API** | model zna Pythona; nie trzeba opisywać każdego narzędzia w prompcie |

⭐ **Drugi mechanizm jest najmocniejszy i najczęściej pomijany.** W trybie klasycznym
**każdy bajt przeczytany przez narzędzie przechodzi przez okno kontekstu**. W code-mode
dane zostają w procesie, a model dostaje wynik. To jest jakościowa różnica, nie
ilościowa: pozwala przetworzyć 500 plików, czego w trybie klasycznym **nie da się
w ogóle**, niezależnie od cierpliwości.

---

## 2. Dlaczego to jest dla Ciebie ważniejsze niż dla innych

Oto obserwacja, którą warto zapamiętać:

> **Mały model lokalny pisze poprawnego Pythona znacznie pewniej, niż emituje długi,
> poprawny JSON z zagnieżdżonymi argumentami.**

Powód jest w danych treningowych. Kodu w Pythonie w korpusie jest **o rzędy wielkości
więcej** niż wywołań funkcji w formacie JSON danego dostawcy. Model widział miliony
pętli `for` i kilkadziesiąt tysięcy schematów tool-calling — jeśli w ogóle.

Konsekwencje są konkretne:

| | Tryb JSON | Code-mode |
| :-- | :-- | :-- |
| Format, w którym model jest słaby | ⚠️ długi JSON z zagnieżdżeniem | — |
| Format, w którym model jest mocny | — | ⭐ Python |
| Błąd składni | psuje całe wywołanie | ⭐ **widoczny w traceback, do poprawienia** |
| Wymuszenie struktury | gramatyka GBNF (10–30 % wolniej) | ⭐ **niepotrzebne** |
| Pętla po 20 elementach | 20 tur | ⭐ 3 linie |
| Warunek „jeśli X to Y" | 2 tury | ⭐ 1 linia |

⭐ **Code-mode przenosi ciężar z formatu, w którym Twój model jest słaby, na format,
w którym jest mocny.** Dla `gpt-oss-20b` to nie jest optymalizacja — to jest zmiana
klasy zadań, które w ogóle da się wykonać.

> ⚠️ **Cena, którą płacisz, jest realna i nieusuwalna: potrzebujesz piaskownicy.**
> Model, który pisze i uruchamia dowolny kod, **jest dokładnie tym, przed czym ostrzega
> ASI05** (Unexpected Code Execution). Bez części 10 code-mode jest zdalnym wykonaniem
> kodu z uprzejmym interfejsem. Ta część zakłada `bwrap` z kursu 1 jako minimum
> i **wymaga** części 10 zanim wpuścisz tu cokolwiek z sieci.

---

## 3. Architektura

```
┌─ MODEL ─────────────────────────────────────────┐
│  dostaje: prompt + API narzędzi (skrót)         │
│  zwraca:  blok kodu Pythona                     │
└──────────────────┬──────────────────────────────┘
                   │  kod
┌──────────────────▼──────────────────────────────┐
│  PIASKOWNICA (bwrap / kontener)                 │
│  ┌────────────────────────────────────────────┐ │
│  │ narzedzia.py  ← te same funkcje co w cz. 7 │ │
│  │ kod agenta    ← wykonywany tutaj           │ │
│  └────────────────────────────────────────────┘ │
│  bez sieci · tylko /tmp/praca zapisywalne       │
│  limit: 30 s CPU, 512 MB RAM, 200 MB dysku      │
└──────────────────┬──────────────────────────────┘
                   │  stdout + stderr (PRZYCIĘTE)
┌──────────────────▼──────────────────────────────┐
│  MODEL widzi wynik                              │
└─────────────────────────────────────────────────┘
```

**Kluczowa decyzja: narzędzia są tymi samymi funkcjami co w części 7.** Nie budujesz
drugiego zestawu. Rejestr eksponuje je dwojako — jako schematy JSON (tryb klasyczny)
i jako moduł Pythona (code-mode) — a logika, limity i promień rażenia są wspólne.

---

## 4. OD ZERA — API narzędzi wewnątrz piaskownicy

```python
# $OSA/kod/narzedzia_api.py
"""API widziane przez kod agenta. Cienka warstwa nad rejestrem z części 7.

Każda funkcja ma docstring — to jest CAŁA dokumentacja, jaką dostanie model.
Pisz je jak opisy narzędzi: co zwraca, zachowanie brzegowe, przykład."""
import os, json, pathlib

KORZEN = pathlib.Path(os.environ["OSA_KORZEN"])     # ustawiane przez piaskownicę
_LICZNIK = {"wywolan": 0, "bajtow": 0}
_LIMIT_WYWOLAN = 500                                 # P93

def _licz(bajtow=0):
    _LICZNIK["wywolan"] += 1
    _LICZNIK["bajtow"] += bajtow
    if _LICZNIK["wywolan"] > _LIMIT_WYWOLAN:
        raise RuntimeError(
            f"Przekroczono limit {_LIMIT_WYWOLAN} wywołań narzędzi w jednym programie. "
            f"Zawęź zakres albo podziel na etapy.")

def znajdz(wzorzec: str, limit: int = 200) -> list[str]:
    """Znajduje dokumenty pasujące do wzorca (glob) względem archiwum.

    Zwraca listę ścieżek względnych, posortowaną. Maksymalnie `limit` pozycji.
    Przykład: znajdz("faktury/2026/03/*.pdf") -> ["faktury/2026/03/f001.pdf", ...]
    Gdy nic nie pasuje — zwraca pustą listę (nie błąd)."""
    _licz()
    return sorted(str(p.relative_to(KORZEN)) for p in KORZEN.glob(wzorzec))[:limit]

def czytaj(sciezka: str, max_znakow: int = 200_000) -> str:
    """Czyta dokument (txt/md/pdf) i zwraca treść jako tekst.

    PDF jest konwertowany automatycznie. Przy dokumencie dłuższym niż `max_znakow`
    zwraca początek — reszta jest obcięta z adnotacją.
    Rzuca FileNotFoundError z listą sąsiadów, gdy pliku nie ma."""
    p = (KORZEN / sciezka).resolve()
    if not str(p).startswith(str(KORZEN)):            # P92
        raise PermissionError(f"Ścieżka poza archiwum: {sciezka}")
    if not p.exists():
        sasiedzi = [x.name for x in p.parent.glob("*")][:8] if p.parent.exists() else []
        raise FileNotFoundError(f"Nie ma '{sciezka}'. W katalogu: {sasiedzi}")
    t = _do_tekstu(p)
    _licz(len(t))
    return t[:max_znakow]

def kwota(tekst: str) -> float | None:
    """Wyciąga kwotę 'do zapłaty' / 'razem' z tekstu faktury.

    Zwraca liczbę w złotych albo None, gdy nie znaleziono.
    NIE zgaduje — brak dopasowania to None, nie 0."""
    import re
    m = re.search(r"(?:do zapłaty|razem|suma)[^\d]{0,20}([\d\s]+[,.]\d{2})",
                  tekst, re.I)
    return float(m.group(1).replace(" ", "").replace(",", ".")) if m else None

def zapisz_wynik(nazwa: str, tresc: str) -> str:
    """Zapisuje wynik pracy do /tmp/praca/<nazwa>. Jedyne miejsce zapisu.

    Zwraca ścieżkę. Użyj tego zamiast open() — inaczej zapis będzie zablokowany."""
    p = pathlib.Path("/tmp/praca") / nazwa
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(tresc, encoding="utf-8")
    _licz(len(tresc))
    return str(p)

def pomoc() -> str:
    """Wypisuje wszystkie dostępne funkcje z opisami."""
    import inspect, sys
    m = sys.modules[__name__]
    return "\n\n".join(
        f"{n}{inspect.signature(f)}\n    {inspect.getdoc(f)}"
        for n, f in vars(m).items()
        if callable(f) and not n.startswith("_") and inspect.getdoc(f))
```

⭐ **`pomoc()` realizuje tezę Steinbergera z części 1 w miniaturze.** Zamiast wrzucać
schematy wszystkich narzędzi do promptu (8 tys. tokenów w każdej turze), dajesz modelowi
**jedną linię**: *„masz moduł `narzedzia`; wywołaj `pomoc()`, jeśli czegoś nie znasz"*.
Model płaci za dokumentację **tylko wtedy, gdy jej potrzebuje** — i to jest dokładnie
to, co on opisuje jako „CLI kosztuje zero, bo model przeczyta `--help`".

---

## 5. Uruchamianie kodu

```python
# $OSA/kod/wykonanie.py
"""Uruchomienie kodu agenta w piaskownicy. Pełna izolacja — część 10."""
import subprocess, pathlib, textwrap, os, shutil

SZABLON = '''
import sys, traceback
sys.path.insert(0, "/opt/osa")
from narzedzia_api import *          # noqa

try:
{kod}
except Exception:
    print("\\n--- BŁĄD WYKONANIA ---", file=sys.stderr)
    traceback.print_exc(limit=3)     # P91: model MUSI zobaczyć traceback
    sys.exit(1)
'''

def uruchom(kod: str, korzen_archiwum: str, limit_s=30, limit_wyjscia=4000) -> dict:
    praca = pathlib.Path("/tmp/praca"); shutil.rmtree(praca, ignore_errors=True)
    praca.mkdir(parents=True)
    skrypt = praca / "_program.py"
    skrypt.write_text(SZABLON.format(kod=textwrap.indent(kod, "    ")), encoding="utf-8")

    cmd = [
        "sudo", "bwrap",                              # patrz uwaga o AppArmor pod kodem
        "--unshare-all",                              # bez sieci, bez PID hosta
        "--die-with-parent", "--new-session",         # P44 z kursu 1
        "--ro-bind", "/usr", "/usr", "--ro-bind", "/lib", "/lib",
        "--ro-bind", "/lib64", "/lib64", "--ro-bind", "/bin", "/bin",
        "--ro-bind", str(pathlib.Path.home() / "os-agenta/kod"), "/opt/osa",
        "--ro-bind", korzen_archiwum, "/archiwum",    # ⭐ archiwum TYLKO DO ODCZYTU
        "--bind", str(praca), "/tmp/praca",           # jedyne miejsce zapisu
        "--proc", "/proc", "--dev", "/dev",
        "--setenv", "OSA_KORZEN", "/archiwum",
        "--setenv", "HOME", "/tmp/praca",
        "--chdir", "/tmp/praca",
        "python3", "/tmp/praca/_program.py",
    ]
    try:
        w = subprocess.run(cmd, capture_output=True, text=True, timeout=limit_s)
        kod_wy, out, err = w.returncode, w.stdout, w.stderr
    except subprocess.TimeoutExpired:
        kod_wy, out, err = 124, "", (
            f"PRZEKROCZONY CZAS ({limit_s} s). Program został przerwany.\n"
            f"Podziel pracę na mniejsze partie albo zawęź zakres.")

    return {
        "kod_wyjscia": kod_wy,
        "wyjscie": _przytnij(out, limit_wyjscia),
        "blad":    _przytnij(err, 1500),
        "pliki":   [p.name for p in praca.glob("*") if p.name != "_program.py"],
    }

def _przytnij(t, limit):
    if len(t) <= limit: return t
    p = limit // 2
    return t[:p] + f"\n[… {len(t)-limit} znaków wycięte …]\n" + t[-p:]
```

**Cztery decyzje warte uzasadnienia:**

1. **`--unshare-all`** — kod agenta **nie ma sieci**. Nawet Badacz nie dostaje sieci
   wewnątrz `exec`; pobieranie robi osobne, kontrolowane narzędzie (część 10).
2. **Archiwum montowane `--ro-bind`** — nawet kod z błędem nie zniszczy dokumentów.
   Zapis wyłącznie do `/tmp/praca`.
3. **Traceback wraca do modelu** — przycięty do 3 ramek. To jest jego główny kanał
   informacji zwrotnej i **nie wolno go połykać**.
4. **Lista plików w wyniku** — model wie, co wyprodukował, bez czytania katalogu.

⚠️ **`sudo` w `cmd` jest tu konieczny na tej maszynie — ale inaczej niż w skrypcie
powłoki, to jest wywołanie AUTOMATYCZNE, bez człowieka przy klawiaturze.** Ubuntu
24.04 blokuje `--unshare-all`/`--unshare-net` dla procesów nieuprzywilejowanych
(brak profilu AppArmor dla `bubblewrap` w tym wydaniu — pełna diagnoza: kurs 1,
`07-SANDBOX-BEZPIECZENSTWO-MONITORING.md`, §2). Interaktywne `sudo bwrap` wpisane
ręcznie w terminalu po prostu prosi o hasło. **Ten kod tak nie może** — jest wołany
wielokrotnie, w pętli, bez nikogo, kto wpisze hasło.

Zanim uruchomisz to w pętli agenta, zrób jedno z dwóch:

```bash
# Wariant A (szybszy, węższy) — bezhasłowe sudo TYLKO dla bwrap, dla Twojego użytkownika
echo "$(whoami) ALL=(root) NOPASSWD: /usr/bin/bwrap" | sudo tee /etc/sudoers.d/bwrap-osa
sudo chmod 440 /etc/sudoers.d/bwrap-osa
sudo visudo -c        # ⭐ zawsze sprawdź składnię PRZED wylogowaniem się
```

```bash
# Wariant B (czystszy, ale poza zakresem tego kursu) — zainstaluj wlasciwy profil
# AppArmor dla /usr/bin/bwrap, zamiast omijac restrykcje przez sudo. Szukaj:
# "apparmor bubblewrap unprivileged_userns ubuntu 24.04".
```

**Wariant A jest węższy, niż wygląda.** `NOPASSWD` dotyczy wyłącznie uruchomienia
samego `/usr/bin/bwrap` — nie daje ogólnego bezhasłowego roota. To, co `bwrap` może
zrobić WEWNĄTRZ piaskownicy, nadal ogranicza cała reszta tej części (`--ro-bind`,
`--unshare-all`, brak sieci). Bez jednego z tych dwóch wariantów `subprocess.run()`
z `sudo` w pętli agenta **zawiesi się na monicie o hasło**, którego nikt nie wpisze,
aż do `timeout`.

---

## 6. Prompt dla trybu code-mode

```python
PROMPT_CODE_MODE = """Masz do dyspozycji Pythona i moduł narzędzi.
Zamiast wywoływać narzędzia pojedynczo — NAPISZ PROGRAM, który zrobi całość.

Dostępne funkcje (pełne opisy: wywołaj `print(pomoc())`):
{skrot_api}

Zasady:
1. Zwróć WYŁĄCZNIE blok kodu Pythona w ```python … ```. Bez komentarza przed i po.
2. Wypisuj wynik przez `print()`. To jedyne, co zobaczysz.
3. Drukuj ZWIĘŹLE — podsumowania i liczby, nie surowe treści dokumentów.
   Twoje `print` trafia do kontekstu i kosztuje.
4. Przy dużych zbiorach drukuj postęp co N elementów, żeby dało się zdiagnozować
   przerwanie.
5. Masz 30 s i 500 wywołań narzędzi. Przy większej pracy — podziel na etapy
   i zapisuj stan pośredni przez `zapisz_wynik()`.
6. Gdy czegoś nie wiesz o API — `print(pomoc())` w osobnym, krótkim programie.

Zadanie: {zadanie}"""

SKROT_API = """znajdz(wzorzec, limit=200) -> list[str]
czytaj(sciezka, max_znakow=200000) -> str
kwota(tekst) -> float | None
zapisz_wynik(nazwa, tresc) -> str
pomoc() -> str"""
```

⭐ **Zasada 3 jest tą, którą modele łamią najczęściej.** Model napisze
`for f in faktury: print(czytaj(f))` i **wrzuci do kontekstu 24 tys. tokenów**, czyli
dokładnie to, przed czym code-mode miał chronić. Pilnujesz tego dwojako: zasadą
w prompcie **i** twardym limitem `limit_wyjscia` w `uruchom()`. Sama zasada nie
wystarcza.

---

## 7. Kiedy code-mode przegrywa

Uczciwa lista — bo to nie jest rozwiązanie wszystkiego.

| Sytuacja | Dlaczego przegrywa | Co robić |
| :-- | :-- | :-- |
| **Jedno proste wywołanie** | narzut pisania programu > oszczędność | tryb klasyczny |
| **Operacja nieodwracalna** | kod jest trudniejszy do przejrzenia niż jedno wywołanie | ⭐ klasyczny + potwierdzenie |
| **Brak piaskownicy** | ASI05 — wykonanie dowolnego kodu | ⭐⭐ **nie używaj w ogóle** |
| **Model słabo pisze kod** | ⚠️ zmierz; poniżej ~7B bywa źle | klasyczny albo większy model |
| **Zadanie interaktywne** | program nie zapyta użytkownika w połowie | klasyczny |
| **Debugowanie zachowania agenta** | trudniej prześledzić rozumowanie | klasyczny do diagnozy |

### 7.1 · Tryb hybrydowy — rekomendowany

**Nie wybieraj jednego. Wystaw oba i pozwól modelowi decydować** — albo zdecyduj sam
regułą:

```python
def wybierz_tryb(zadanie: str, narzedzia_dostepne: int) -> str:
    sygnaly_petli = ("każd", "wszystk", "dla listy", "porówn", "zsumuj",
                     "ile łącznie", "przejdź przez", "dla wszystkich")
    if any(s in zadanie.lower() for s in sygnaly_petli):
        return "code"
    if narzedzia_dostepne > 25:              # część 7, strategia C
        return "code"
    return "klasyczny"
```

⭐ **Reguła oparta na sygnałach pętli łapie większość przypadków i kosztuje zero.**
Zanim zbudujesz router uczony na danych — zmierz, jak daleko zajedziesz na ośmiu
słowach kluczowych.

---

## 8. EKSPERYMENT 8 — to samo zadanie dwoma drogami

⭐ **Najważniejszy pomiar tej części. Nie przyjmuj cudzych 85–94 % na wiarę.**

### 8.1 · Przygotowanie

```bash
mkdir -p $OSA/pomiary/codemode && cd $OSA/pomiary/codemode
python3 - <<'EOF'
import random, pathlib
random.seed(11)
kat = pathlib.Path("archiwum/faktury/2026/03"); kat.mkdir(parents=True, exist_ok=True)
for i in range(1, 41):
    oplacona = random.random() < 0.7
    kwota = round(random.uniform(80, 3200), 2)
    tresc = (f"FAKTURA VAT nr FV/{i:03d}/03/2026\n"
             f"Data wystawienia: 2026-03-{random.randint(1,28):02d}\n"
             f"Kontrahent: Firma {random.choice('ABCDEFGH')}\n"
             + "pozycja rozliczeniowa\n" * random.randint(15, 60) +
             f"\nRazem do zapłaty: {kwota:.2f} zł\n"
             + ("Opłacono przelewem\n" if oplacona else ""))
    (kat / f"f{i:03d}.txt").write_text(tresc, encoding="utf-8")
print("40 faktur gotowych")
EOF
```

### 8.2 · Pięć zadań o rosnącej złożoności

| # | Zadanie | Spodziewany zwycięzca |
| :-- | :-- | :-- |
| Z1 | „Ile jest faktur w marcu?" | klasyczny (1 wywołanie) |
| Z2 | „Ile wynosi faktura FV/007/03/2026?" | remis |
| Z3 | „Które faktury są nieopłacone?" | code-mode |
| Z4 | „Suma nieopłaconych + lista malejąco" | ⭐ code-mode |
| Z5 | „Dla każdego kontrahenta: liczba, suma, % opłaconych, posortuj" | ⭐⭐ code-mode |

### 8.3 · Tabela wyników — po 3 przebiegi każdy

| Zadanie | Tryb | Tur | Tokeny we | Tokeny wy | Czas | Poprawne /3 |
| :-- | :-- | --: | --: | --: | --: | --: |
| Z1 | klasyczny | | | | | |
| Z1 | code | | | | | |
| Z2 | klasyczny | | | | | |
| … | | | | | | |
| Z5 | klasyczny | | | | | |
| Z5 | code | | | | | |

### 8.4 · Powtórz na obu modelach

To jest część, która da Ci decyzję do routera z części 17:

| Model | Z5 klasyczny | Z5 code | Kod poprawny składniowo za 1. razem |
| :-- | --: | --: | --: |
| `gpt-oss-20b` | /3 | /3 | /3 |
| `qwen3-32b` | /3 | /3 | /3 |

⚠️ **Predykcja do sprawdzenia:**

- Z1–Z2: klasyczny wygrywa albo remis. **Code-mode nie jest darmowy** — pisanie
  programu kosztuje tokeny wyjściowe.
- Z3–Z5: code-mode wygrywa coraz wyraźniej; przy Z5 spodziewam się, że **klasyczny
  w ogóle nie skończy** w limicie tur.
- Największa niewiadoma to ostatnia kolumna. Jeśli `gpt-oss-20b` pisze poprawny
  składniowo kod w mniej niż 2/3 przypadków — potrzebujesz pętli naprawczej z §9.

### 8.5 · Pomiar dodatkowy — czy kod jest bezpieczny

```bash
python3 audyt_kodu.py --z-dziennika 100
# zlicz, ile wygenerowanych programów próbowało:
#   - open() poza /tmp/praca
#   - import socket / urllib / requests
#   - subprocess / os.system
#   - odczyt spoza /archiwum
```

⭐ **Ten pomiar jest ważniejszy, niż się wydaje.** Nie dlatego, że model jest złośliwy
— tylko dlatego, że **liczba prób pokazuje, jak bardzo polegasz na piaskownicy**.
Jeśli 12 % programów próbuje pisać poza `/tmp/praca`, to znaczy, że bez `bwrap`
miałbyś 12 % programów robiących coś, na co nie wyraziłeś zgody.

---

## 9. Pętla naprawcza — kod, który się nie kompiluje

```python
def uruchom_z_naprawa(kod, korzen, wywolaj_model, max_prob=3) -> dict:
    """Błąd składni albo wykonania → model dostaje traceback i poprawia."""
    historia = []
    for proba in range(1, max_prob + 1):
        w = uruchom(kod, korzen)
        if w["kod_wyjscia"] == 0:
            return {**w, "prob": proba}
        historia.append({"kod": kod, "blad": w["blad"]})
        if proba == max_prob:
            return {**w, "prob": proba, "poddano_sie": True}
        kod = _wyciagnij_kod(wywolaj_model([{"rola": "user", "tresc":
            f"Ten program się nie wykonał.\n\nKOD:\n```python\n{kod}\n```\n\n"
            f"BŁĄD:\n{w['blad']}\n\n"
            f"Popraw go. Zwróć TYLKO poprawiony kod w bloku ```python.\n"
            f"Jeśli błąd wynika z braku uprawnień — nie obchodź go, "
            f"tylko zrób to inaczej w dozwolony sposób."}])["tresc"])
    return w
```

⚠️ **Zdanie „nie obchodź go, tylko zrób to inaczej" jest konieczne.** Model, który
dostanie `PermissionError`, domyślnie próbuje **obejścia** — inną ścieżką, przez
`subprocess`, przez `/proc`. Piaskownica go zatrzyma, ale zmarnujesz trzy próby.
Powiedz mu wprost, jaka reakcja jest oczekiwana.

> 💡 **Ile prób.** Trzy. Jeśli model nie poprawi kodu w trzech podejściach, czwarte też
> nie pomoże — to jest sygnał do eskalacji na mocniejszy model (drabina z części 3,
> szczebel 4), nie do kolejnej próby.

---

## 10. PRODUKCYJNIE

| | smolagents | MS Agent Framework CodeAct | `code-mode` (UTCP) | **Twój** |
| :-- | :-- | :-- | :-- | :-- |
| Język | Python | C#/Python | TS/Python | Python |
| Piaskownica | ⭐ wbudowana (E2B/lokalna) | kontenery | konfigurowalna | ⭐ `bwrap` lokalnie |
| Narzędzia jako API | ⭐ tak | ⭐ tak | ⭐ tak | ⭐ tak |
| Offline | ⚠️ zależy od piaskownicy | ✗ chmura | częściowo | ⭐ **pełne** |
| Pętla naprawcza | ⭐ tak | tak | tak | ⭐ tak |
| Limit wywołań narzędzi | ✗ | ✗ | ✗ | ⭐ tak |
| Audyt wygenerowanego kodu | ✗ | częściowo | ✗ | ⭐ §8.5 |

**smolagents to najbliższa gotowa implementacja tego, co zbudowałeś** — warto
przeczytać jej kod po tej części, bo rozpoznasz każdą decyzję. Główny powód, żeby
zostać przy swoim: **piaskownica jest Twoja i offline**, a w smolagents jest
konfigurowalna i domyślnie celuje w usługę zewnętrzną.

---

## 11. ĆWICZENIE — przełącz Archiwistę na tryb hybrydowy

1. Wystaw narzędzia Archiwisty jako moduł `narzedzia_api.py` z **docstringami
   napisanymi wg zasad z części 7** (co zwraca, brzegi, przykład).
2. Zaimplementuj `wybierz_tryb()` i wepnij w pętlę.
3. Dodaj zdarzenie `kod.wykonanie` do dziennika: kod, wynik, liczba prób, czas.
4. Uruchom 20 realnych zadań i sprawdź w `sesja-cli.py`, jak rozłożył się wybór trybu.

```bash
python3 sesja-cli.py tryby archiwista --ostatnie 20
# klasyczny: 12 (60%)  śr. 3,2 tury   śr. 2 100 tok.
# code:       8 (40%)  śr. 2,1 tury   śr. 1 400 tok.   napraw: 1,3 próby
```

5. **Zadanie trudniejsze:** znajdź zadanie, na którym `wybierz_tryb()` decyduje źle,
   i dopisz sygnał, który to naprawia. Potem sprawdź, czy nie zepsułeś pozostałych 19.

---

## 12. Pułapki tej części

| ID | Pułapka | Objaw | Jak uniknąć |
| :-- | :-- | :-- | :-- |
| **P91** | **Połknięty traceback** | Model dostaje „błąd wykonania" bez szczegółów i zgaduje po omacku | Traceback (3 ramki) wraca do modelu. To jego główny kanał zwrotny |
| **P92** | **Ścieżki niesprawdzane wewnątrz API** | `czytaj("../../.ssh/id_rsa")` wychodzi poza archiwum | `resolve()` + sprawdzenie prefiksu w **każdej** funkcji. Piaskownica to druga warstwa, nie pierwsza |
| **P93** | **Brak limitu wywołań w programie** | `for f in znajdz("**/*")` na 40 tys. plików — 30 s timeoutu bez wyniku | Licznik wywołań + limit + czytelny komunikat, co zrobić zamiast |
| **P94** | **Model drukuje surowe treści** | `print(czytaj(f))` w pętli — 24 tys. tokenów, czyli dokładnie to, co miało zniknąć | Zasada 3 w prompcie **i** twardy `limit_wyjscia`. Sama zasada nie wystarcza |

---

## 13. Checkpoint

```bash
cd $OSA
python3 - <<'EOF'
from kod.wykonanie import uruchom
w = uruchom('print(len(znajdz("faktury/**/*.txt")))',
            korzen_archiwum="/home/USER/os-agenta/pomiary/codemode/archiwum")
print("✓ wykonanie:", w["wyjscie"].strip())

z = uruchom('open("/etc/passwd").read()', korzen_archiwum="/tmp")
assert z["kod_wyjscia"] != 0, "✗ P92/piaskownica: odczyt /etc/passwd przeszedł!"
print("✓ piaskownica blokuje odczyt spoza archiwum")

s = uruchom('import socket; socket.create_connection(("1.1.1.1",80),2)',
            korzen_archiwum="/tmp")
assert s["kod_wyjscia"] != 0, "✗ sieć dostępna w piaskownicy!"
print("✓ brak sieci w piaskownicy")
EOF
test -s pomiary/codemode/wyniki.csv && echo "✓ porównanie trybów zmierzone"
git add -A && git commit -m "część 8: code-mode, API narzędzi, wykonanie w piaskownicy"
```

- [ ] Rozumiesz **trzy** mechanizmy oszczędności, nie tylko „mniej tur"
- [ ] Wiesz, dlaczego code-mode szczególnie pomaga **małym modelom lokalnym**
- [ ] Narzędzia mają jedno źródło prawdy, dwie ekspozycje
- [ ] `pomoc()` zastępuje schematy w prompcie — dokumentacja na żądanie
- [ ] Piaskownica: bez sieci, archiwum tylko do odczytu, zapis w `/tmp/praca`
- [ ] Traceback wraca do modelu; pętla naprawcza ma 3 próby i eskaluje
- [ ] Znasz sytuacje, w których code-mode **przegrywa**, i masz tryb hybrydowy
- [ ] ⭐ **Zmierzyłeś oba tryby na 5 zadaniach × 2 modele — masz własne liczby**
- [ ] ⭐ Wiesz, ile wygenerowanych programów próbowało wyjść poza piaskownicę

---

**Dalej: `09-PROTOKOLY-MCP-CLI-A2A.md`** — czy MCP jest wart swoich tokenów. Mierzymy
tezę Steinbergera zamiast się o nią spierać.
