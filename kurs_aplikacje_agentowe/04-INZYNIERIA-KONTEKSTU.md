# Część 4 · Inżynieria kontekstu — budżet uwagi

**Poziom:** ⭐⭐⭐⭐ · **Czas:** ~5 h · **Wymaga:** części 2 i 3
**Produkuje:** menedżer kontekstu, zmierzoną krzywą degradacji Twoich modeli, kompakcję, która nie gubi liczb

---

## 0. Kontekst to nie pojemnik. To budżet uwagi.

Najkosztowniejsze nieporozumienie w pracy z modelami lokalnymi brzmi tak: *„mam okno
32 tys. tokenów, więc mogę wrzucić 32 tys. tokenów"*.

Nie możesz. A dokładniej: możesz, ale **jakość spadnie na długo przed granicą okna**.

Anthropic nazywa to **budżetem uwagi** i podaje mechanizm:

> Modele mają skończony „budżet uwagi" z malejącymi przychodami krańcowymi. Wynika to
> z architektury transformera — **n² relacji parami między tokenami** — oraz z rozkładu
> danych treningowych, w których krótsze sekwencje dominują.
> — [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Praktyczna konsekwencja: **dobry kontekst to najmniejszy zbiór tokenów o najwyższym
sygnale**, a nie największy, jaki się zmieści.

```
       JAKOŚĆ ODPOWIEDZI w funkcji zapełnienia okna
  100% ┤●●●●●●●●●
       │         ●●●●●●
   75% ┤               ●●●●
       │                   ●●●
   50% ┤                      ●●●
       │                         ●●●●
   25% ┤                             ●●●●●●
       └──┬────┬────┬────┬────┬────┬────┬────
         10%  25%  40%  55%  70%  85% 100%
                            ▲
                    tu przestajesz (§4)
```

⚠️ **Kształt tej krzywej jest inny dla każdego modelu i Ty swojej nie znasz.** Dlatego
eksperyment w §8 jest najważniejszym ćwiczeniem tej części — bez niego wszystkie progi
w Twoim systemie będą zgadywane.

### 0.1 · Kontekst a pamięć — rozróżnienie, bez którego zlejesz część 4 z 5

| | Kontekst (ta część) | Pamięć (część 5) |
| :-- | :-- | :-- |
| Gdzie żyje | w oknie modelu, tu i teraz | na dysku, między sesjami |
| Czas życia | jedna tura | miesiące |
| Koszt | tokeny w każdej turze | miejsce na dysku |
| Problem | **za mało miejsca** | **za dużo rzeczy do znalezienia** |
| Operacja | wybieranie, przycinanie, streszczanie | zapisywanie, indeksowanie, wyszukiwanie |

**Kontekst to pamięć robocza. Pamięć to dysk.** Mylenie ich prowadzi do dwóch typowych
błędów: ładowania całej pamięci do kontekstu (drogo i szkodliwie) albo trzymania stanu
tylko w kontekście (ginie przy restarcie).

---

## 1. Z czego składa się kontekst agenta

Rozbij budżet na pozycje — inaczej nie da się nim zarządzać.

```
┌─ prompt systemowy ────────── 400–2000 tok.   stały, cache'owalny
├─ definicje narzędzi ──────── 200–8000 tok.   ⚠️ rośnie z liczbą narzędzi
├─ pliki robocze (SOUL itd.) ─ 300–1500 tok.   stały, cache'owalny
├─ pamięć doładowana ───────── 0–3000 tok.     zmienny
├─ historia rozmowy ────────── 0–∞             ⚠️ rośnie bez granicy
├─ wyniki narzędzi ─────────── 0–∞             ⚠️⚠️ rośnie NAJSZYBCIEJ
└─ pytanie użytkownika ─────── 10–500 tok.
```

⭐ **Dwie pozycje z podwójnym ostrzeżeniem odpowiadają za ~80 % problemów.** Jedno
`ls -R` w dużym katalogu potrafi wrzucić 15 tys. tokenów i **jednym ruchem zjeść pół
okna**. Dlatego „przycinanie obserwacji" wraca w częściach 7 i 8.

### 1.1 · Kolejność składania ma znaczenie finansowe

Prompt cache działa na **prefiksie**. Wszystko, co stałe, musi być **na początku**
i w niezmiennej kolejności:

```
✓ [systemowy][narzędzia][pliki robocze] │ [pamięć][historia][pytanie]
  └──── stałe, trafia w cache ─────────┘   └── zmienne ──┘

✗ [systemowy][data i godzina][narzędzia][…]
                 ▲ jedna zmienna wartość UNIEWAŻNIA CAŁY prefiks
```

To jest pułapka P46 z kursu 1 i wraca tu, bo w systemie wieloagentowym **łatwiej ją
popełnić**: wystarczy, że wstrzykniesz nazwę agenta albo znacznik czasu przed
definicjami narzędzi.

---

## 2. Wysokość promptu systemowego

Anthropic używa terminu **„altitude"** — wysokość, z której prompt opisuje zadanie.
Dwa skrajne błędy:

**Za nisko — twarda logika w prompcie:**

```
Jeśli plik ma rozszerzenie .pdf, użyj narzędzia czytaj_pdf. Jeśli .txt, użyj
czytaj_plik. Jeśli .docx, najpierw konwertuj przez libreoffice, potem czytaj_plik.
Jeśli plik jest większy niż 1 MB, przeczytaj tylko pierwsze 100 linii, chyba że
użytkownik prosił o całość, wtedy…
```

**Kruche i nie skaluje się.** Każdy nowy przypadek to nowa gałąź; model i tak trafi na
sytuację, której nie przewidziałeś, a Ty nauczyłeś go, że ma czekać na instrukcję.

**Za wysoko — mgła:**

```
Jesteś pomocnym asystentem. Rób rzeczy dobrze i myśl o użytkowniku.
```

**Zakłada wspólny kontekst, którego nie ma.** Model nie wie, co u Ciebie znaczy „dobrze".

**Właściwa wysokość — heurystyki plus granice:**

```
Czytasz dokumenty użytkownika i odpowiadasz na pytania o nie.

Zasady:
- Zawsze cytuj plik i fragment, na którym opierasz twierdzenie.
- Gdy nie znajdujesz odpowiedzi w dokumentach — powiedz to wprost.
  „Nie ma tego w przeszukanych plikach" jest poprawną, pełną odpowiedzią.
- Czytaj wybiórczo. Zacznij od nagłówków i spisu treści, całość tylko gdy trzeba.
- Nie zgaduj dat, kwot ani nazwisk. Albo cytat, albo „nie znalazłem".

Masz do dyspozycji narzędzia — ich opisy mówią, kiedy ich użyć.
```

> 💡 **Test wysokości.** Przeczytaj prompt i zapytaj: *czy dałbym to nowemu
> współpracownikowi pierwszego dnia?* Jeśli brzmi jak instrukcja obsługi tostera —
> za nisko. Jeśli jak hasło z plakatu motywacyjnego — za wysoko.

### 2.1 · Jak pisać prompt systemowy, żeby nie zgnił

Metoda, która działa i jest nudna:

1. **Zacznij od minimum** na najlepszym modelu, jaki masz.
2. **Uruchom zbiór testowy** (część 14). Zapisz tryby awarii.
3. **Dodaj jedno zdanie** adresujące **jeden** zaobserwowany tryb.
4. **Zmierz ponownie.** Jeśli nie pomogło — **usuń to zdanie**.

⚠️ **Krok 4 jest tym, którego nikt nie robi.** Prompty rosną, bo zdania się dokłada
i nigdy nie odejmuje. Po pół roku masz 3000 tokenów, z czego połowa nie robi nic albo
szkodzi — a nie wiesz która połowa, bo nigdy nie mierzyłeś.

---

## 3. Doładowanie w ostatniej chwili

Dwie filozofie dostarczania danych:

| | Wstępne ładowanie | **Doładowanie w ostatniej chwili** |
| :-- | :-- | :-- |
| Kiedy | wszystko przed pierwszą turą | gdy agent poprosi |
| Agent dostaje | treść | **lekkie identyfikatory** (ścieżki, nazwy) |
| Koszt przy 100 plikach | 200 tys. tokenów | ~1 tys. tokenów |
| Ryzyko | context rot, koszt | dodatkowa tura na pobranie |

Anthropic zwraca uwagę, że to odpowiada ludzkiemu poznaniu: nie pamiętasz treści
wszystkich swoich plików, pamiętasz **strukturę katalogów** i wiesz, gdzie zajrzeć.

**Metadane są sygnałem.** `~/dokumenty/2026/03/faktura-orange.pdf` niesie datę,
kategorię i wystawcę **za 12 tokenów**. Treść tego pliku to 800 tokenów. Agent, który
dostanie 200 takich ścieżek, wie o Twoim archiwum zaskakująco dużo za 2400 tokenów.

```python
# Zamiast: wrzuć 100 dokumentów (200 000 tok.)
# Zrób:    wrzuć mapę (1 200 tok.) + narzędzie czytaj(sciezka)

def mapa_korpusu(katalog, max_pozycji=200) -> str:
    """Lekki identyfikator zamiast treści."""
    import pathlib
    p = pathlib.Path(katalog)
    linie = []
    for f in sorted(p.rglob("*"))[:max_pozycji]:
        if f.is_file():
            linie.append(f"{f.relative_to(p)}  ({f.stat().st_size // 1024} KB)")
    return "\n".join(linie)
```

> ⚠️ **Kiedy wstępne ładowanie jednak wygrywa.** Gdy korpus jest mały (<20 tys. tokenów)
> **i stały**. Wtedy trafia w prompt cache i kosztuje raz, a doładowanie kosztowałoby
> dodatkową turę za każdym razem. Granica przebiega tam, gdzie koszt tury przewyższa
> koszt trzymania — policz ją dla siebie, nie zgaduj.

---

## 4. Kompakcja — najpierw pełnia, potem precyzja

Gdy historia rosła i zbliżasz się do progu, masz cztery ruchy, od najtańszego:

### Ruch 1 · Czyszczenie wyników narzędzi (najlżejszy dotyk)

Wynik `ls -R` z tury 3 nie jest już potrzebny w turze 20 — agent dawno z niego
skorzystał. Zastąp go zaślepką:

```python
def wyczysc_stare_wyniki(historia, zachowaj_ostatnie=3):
    """Najtańsza kompakcja: wyniki narzędzi starsze niż N tracą treść."""
    indeksy = [i for i, w in enumerate(historia) if w.get("rola") == "tool"]
    for i in indeksy[:-zachowaj_ostatnie] if zachowaj_ostatnie else indeksy:
        oryg = len(historia[i]["tresc"])
        historia[i]["tresc"] = f"[wynik usunięty z kontekstu — {oryg} znaków, seq w dzienniku]"
    return historia
```

⭐ **Zaczynaj zawsze od tego.** W typowej sesji agentowej wyniki narzędzi to **50–70 %
historii**, a ich wartość informacyjna spada praktycznie do zera po 2–3 turach. To jest
najlepszy stosunek oszczędności do ryzyka w całym rozdziale.

### Ruch 2 · Deduplikacja

Agent przeczytał ten sam plik trzy razy? Zostaw ostatnie odczytanie.

### Ruch 3 · Streszczenie historii

Dopiero gdy 1 i 2 nie wystarczą. **Kolejność jest kluczowa:**

> Zacznij od maksymalizacji **pełni** (recall), potem iteruj w stronę **precyzji**.
> — Anthropic

Znaczy to: pierwsza wersja promptu streszczającego ma **zachowywać za dużo**. Dopiero
gdy widzisz, że nic ważnego nie ginie, zaczynaj przycinać. Odwrotna kolejność — od
zwięzłości ku pełni — gwarantuje, że przez pierwsze tygodnie będziesz gubił rzeczy
i nie będziesz wiedział jakie.

```python
PROMPT_KOMPAKCJI = """Streść poniższą historię pracy agenta.

ZACHOWAJ DOSŁOWNIE, bez parafrazy:
- wszystkie liczby, kwoty, daty, identyfikatory, ścieżki plików
- decyzje, które zapadły, wraz z uzasadnieniem
- błędy, które wystąpiły, i co je naprawiło
- to, czego jeszcze NIE zrobiono

MOŻESZ POMINĄĆ:
- powtórzenia i nieudane próby, które nic nie wniosły
- pełne treści plików (zostaw ścieżkę i jednozdaniowy opis)
- uprzejmości

Format: punkty. Bez wstępu i bez podsumowania.

HISTORIA:
{historia}"""
```

⚠️ **„ZACHOWAJ DOSŁOWNIE ... liczby" jest tam z konkretnego powodu** — to pułapka P31
z kursu 1. Model streszczający **zaokrągla**. „Przetworzył 3847 plików" staje się
„przetworzył prawie cztery tysiące plików", a agent w następnej turze nie wie, czy
skończył. W §8 zmierzysz, jak często to się dzieje.

### Ruch 4 · Zamknięcie sesji i przekazanie

Gdy streszczenie też nie wystarcza — **to nie jest problem kompakcji, tylko sygnał, że
zadanie jest za duże na sesję**. Użyj harnessu z części 3: zapisz postęp, commit, nowa
sesja. To jest tańsze i bezpieczniejsze niż trzecia kompakcja z rzędu.

---

## 5. Notatki strukturalne — pamięć poza kontekstem

Zamiast trzymać wszystko w oknie, agent **pisze notatki do pliku i czyta je, gdy trzeba**.
Anthropic pokazuje to na przykładzie Claude'a grającego w Pokémona przez tysiące kroków.

U Ciebie to jest `POSTEP.md` z części 3 — ale można to sformalizować jako narzędzie:

```python
def narzedzie_notatka(akcja: str, klucz: str, tresc: str = "") -> str:
    """Notatnik agenta. Poza kontekstem, trwały między turami."""
    import os, pathlib, json
    p = pathlib.Path(os.environ["OSA"], "notatnik.json")
    d = json.loads(p.read_text()) if p.exists() else {}
    if akcja == "zapisz":
        d[klucz] = tresc
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2))
        return f"zapisano '{klucz}' ({len(tresc)} znaków)"
    if akcja == "czytaj":
        return d.get(klucz, f"brak notatki '{klucz}'")
    if akcja == "lista":
        return "\n".join(f"{k} ({len(v)} zn.)" for k, v in d.items()) or "notatnik pusty"
    return "akcja: zapisz | czytaj | lista"
```

⭐ **Kluczowa różnica wobec pamięci z części 5:** notatnik jest **jawnie sterowany przez
agenta** i zakresowany do zadania. Pamięć z części 5 jest automatyczna i trwała.
Notatnik to brudnopis; pamięć to archiwum.

---

## 6. OD ZERA — menedżer kontekstu

```python
# $OSA/kontekst.py
"""Budżetowanie kontekstu: licz, przycinaj, kompaktuj — w tej kolejności."""
import json

class Budzet:
    def __init__(self, okno: int, licz_tokeny, prog_kompakcji=0.70, prog_twardy=0.85):
        self.okno, self.licz = okno, licz_tokeny
        self.prog_k, self.prog_t = prog_kompakcji, prog_twardy

    def rozbicie(self, czesci: dict) -> dict:
        """Ile zjada każda pozycja budżetu. Bez tego nie da się optymalizować."""
        r = {k: self.licz(v) for k, v in czesci.items()}
        r["_razem"] = sum(r.values())
        r["_zapelnienie"] = round(r["_razem"] / self.okno, 3)
        return r

    def stan(self, razem: int) -> str:
        z = razem / self.okno
        if z >= self.prog_t: return "twardy"      # kompaktuj TERAZ
        if z >= self.prog_k: return "ostrzezenie" # zaplanuj kompakcję
        return "ok"

def przytnij_obserwacje(tresc: str, limit_znakow=2000) -> str:
    """P40 z kursu 1: jedna obserwacja nie może zjeść okna.
    Zachowuje POCZĄTEK i KONIEC — środek jest zwykle najmniej istotny."""
    if len(tresc) <= limit_znakow:
        return tresc
    pol = limit_znakow // 2
    ucieto = len(tresc) - limit_znakow
    return (tresc[:pol] + f"\n\n[… wycięto {ucieto} znaków — "
            f"użyj narzędzia z węższym zapytaniem, jeśli potrzebujesz środka …]\n\n"
            + tresc[-pol:])

def kompaktuj(historia: list, wywolaj_model, zachowaj_ostatnie=4) -> tuple[list, dict]:
    """Ruch 1 → 2 → 3. Zwraca nową historię i raport oszczędności."""
    przed = sum(len(json.dumps(w, ensure_ascii=False)) for w in historia)

    # Ruch 1 — czyszczenie starych wyników narzędzi
    idx = [i for i, w in enumerate(historia) if w.get("rola") == "tool"]
    for i in idx[:-2] if len(idx) > 2 else []:
        historia[i]["tresc"] = f"[wynik usunięty — {len(historia[i]['tresc'])} znaków]"

    po_r1 = sum(len(json.dumps(w, ensure_ascii=False)) for w in historia)
    if po_r1 < przed * 0.6:                        # wystarczyło
        return historia, {"ruch": 1, "przed": przed, "po": po_r1}

    # Ruch 3 — streszczenie wszystkiego poza ogonem
    glowa, ogon = historia[:-zachowaj_ostatnie], historia[-zachowaj_ostatnie:]
    streszczenie = wywolaj_model([{"rola": "user", "tresc": PROMPT_KOMPAKCJI.format(
        historia=json.dumps(glowa, ensure_ascii=False, indent=1))}])["tresc"]

    nowa = [{"rola": "system", "tresc": "PODSUMOWANIE WCZEŚNIEJSZEJ PRACY:\n" + streszczenie}] + ogon
    po = sum(len(json.dumps(w, ensure_ascii=False)) for w in nowa)
    return nowa, {"ruch": 3, "przed": przed, "po": po, "streszczenie": streszczenie}
```

**Wepnij to w dziennik z części 2** — kompakcja musi zostawić ślad:

```python
d.dopisz("kompakcja", od_seq=pierwszy, do_seq=ostatni,
         streszczenie=raport["streszczenie"], zachowaj_ostatnie=4,
         znakow_przed=raport["przed"], znakow_po=raport["po"])
```

⭐ **Dzięki temu w części 15 odpowiesz na pytanie „co agent widział w turze 40",
nawet jeśli w turze 60 to skompaktował.** Oryginał nigdy nie znika z pliku.

---

## 7. PRODUKCYJNIE — co robią inni

| Mechanizm | Claude Agent SDK | LangGraph | **Twój** |
| :-- | :-- | :-- | :-- |
| Automatyczna kompakcja | ⭐ wbudowana, przy progu | ✗ | próg + 3 ruchy |
| Czyszczenie wyników narzędzi | ⭐ `context editing` | ✗ | ruch 1 |
| Świadomość pozostałego budżetu | ⭐ model ją widzi | ✗ | `Budzet.stan()` |
| Notatki poza kontekstem | ⭐ narzędzie `memory` | store | notatnik |
| **Rozbicie budżetu na pozycje** | ✗ | ✗ | ⭐ `rozbicie()` |
| **Ślad kompakcji w dzienniku** | częściowo | ✗ | ⭐ zdarzenie |

> 💡 **Jedna rzecz warta skopiowania od Anthropica: powiedz modelowi, ile mu zostało.**
> Model, który wie, że ma 20 % okna, zachowuje się inaczej — zaczyna podsumowywać
> i domykać, zamiast otwierać nowe wątki. Kosztuje to 15 tokenów w prompcie:
>
> ```
> Pozostały budżet kontekstu: ~22 %. Zmierzaj do domknięcia bieżącej pozycji.
> ```

---

## 8. EKSPERYMENT 4 — zmierz krzywą degradacji swoich modeli

⭐ **To jest najważniejszy pomiar w całym kursie.** Wszystkie progi w Twoim systemie
(kiedy kompaktować, kiedy zamykać sesję, ile narzędzi pokazać) opierają się na tej
jednej krzywej — a jest inna dla każdego modelu.

**Hipoteza:** trafność spada nieliniowo wraz z zapełnieniem okna, a punkt załamania
leży **istotnie poniżej** deklarowanej długości kontekstu.

### 8.1 · Zadanie testowe — dwa typy, bo mierzą co innego

```bash
mkdir -p $OSA/pomiary/kontekst && cd $OSA/pomiary/kontekst
cd ~/Desktop/github_repos/llm-education   # katalog repozytorium (u Ciebie może być inny)
source rig-env.sh
```

```python
# generuj.py — buduje zestawy o rosnącym zapełnieniu
import random, json, pathlib
random.seed(7)

WYPELNIACZ = ("Protokół z zebrania wspólnoty. Omówiono stan techniczny budynku "
              "oraz plan remontów. Zatwierdzono sprawozdanie. ")

def zestaw(zapelnienie_tok: int, typ: str) -> dict:
    """typ='igla' — wyszukanie faktu. typ='synteza' — połączenie 3 faktów."""
    fakty = {
        "igla":    [("Kod dostępu do kotłowni to 7741.", "Jaki jest kod do kotłowni?", "7741")],
        "synteza": [("Zaliczka w styczniu: 420 zł.", None, None),
                    ("W marcu zaliczkę podniesiono o 85 zł.", None, None),
                    ("Od lipca obowiązuje zniżka 30 zł.", 
                     "Ile wynosi zaliczka od lipca?", "475")],
    }[typ]
    wypelniacz_n = max(1, zapelnienie_tok * 4 // len(WYPELNIACZ))
    bloki = [WYPELNIACZ] * wypelniacz_n
    # rozrzuć fakty równomiernie — NIE wszystkie na początku
    for i, (f, _, _) in enumerate(fakty):
        bloki.insert(len(bloki) * (i + 1) // (len(fakty) + 1), f + " ")
    pytanie = [p for _, p, _ in fakty if p][0]
    odp     = [o for _, _, o in fakty if o][0]
    return {"kontekst": "".join(bloki), "pytanie": pytanie, "oczekiwane": odp}

if __name__ == "__main__":
    out = []
    for zap in (1000, 2000, 4000, 8000, 12000, 16000, 24000, 32000):
        for typ in ("igla", "synteza"):
            for powt in range(5):                    # 5 powtórzeń — P61
                z = zestaw(zap, typ)
                z.update(zapelnienie=zap, typ=typ, powt=powt)
                out.append(z)
    pathlib.Path("zestawy.jsonl").write_text(
        "\n".join(json.dumps(z, ensure_ascii=False) for z in out), encoding="utf-8")
    print(f"{len(out)} zestawów")
```

### 8.2 · Uruchomienie

```bash
python3 generuj.py
$LB/llama-server -m $OSS20 -c 32768 -ngl 99 --port 8080 --host 127.0.0.1 &
sleep 20
python3 zmierz.py --model gpt-oss-20b > wyniki-oss20.csv
# powtórz dla $QWEN32 i $BIELIK
```

```python
# zmierz.py
import json, sys, time, urllib.request

def pytaj(kontekst, pytanie):
    ciało = json.dumps({
        "messages": [{"role": "user",
                      "content": f"{kontekst}\n\nPytanie: {pytanie}\nOdpowiedz samą liczbą."}],
        "temperature": 0, "max_tokens": 32,
    }).encode()
    r = urllib.request.Request("http://127.0.0.1:8080/v1/chat/completions", ciało,
                               {"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(r, timeout=300) as o:
        d = json.load(o)
    return (d["choices"][0]["message"]["content"].strip(),
            d["usage"]["prompt_tokens"], round(time.time() - t0, 2))

print("model,zapelnienie,typ,powt,tokeny,ms,trafne,odpowiedz")
model = sys.argv[2]
for linia in open("zestawy.jsonl", encoding="utf-8"):
    z = json.loads(linia)
    odp, tok, sek = pytaj(z["kontekst"], z["pytanie"])
    trafne = int(z["oczekiwane"] in odp)
    print(f'{model},{z["zapelnienie"]},{z["typ"]},{z["powt"]},{tok},{sek},{trafne},"{odp[:40]}"')
```

### 8.3 · Tabela do wypełnienia

| Zapełnienie | `gpt-oss-20b` igła | `gpt-oss-20b` synteza | `qwen3-32b` igła | `qwen3-32b` synteza |
| --: | --: | --: | --: | --: |
| 1 000 | /5 | /5 | /5 | /5 |
| 2 000 | | | | |
| 4 000 | | | | |
| 8 000 | | | | |
| 12 000 | | | | |
| 16 000 | | | | |
| 24 000 | | | | |
| 32 000 | | | | |

### 8.4 · Co z tego wyczytać

**Trzy liczby, które wyciągniesz i wpiszesz do konfiguracji:**

1. **Punkt załamania igły** — gdzie trafność wyszukiwania spada poniżej 90 %.
2. **Punkt załamania syntezy** — to samo dla łączenia faktów. ⚠️ **Będzie znacznie
   wcześniej** — zwykle 2–3× — bo synteza wymaga jednoczesnej uwagi na wielu miejscach.
3. **Próg kompakcji** = 80 % punktu załamania **syntezy**, nie igły.

```bash
# wpisz wynik do konfiguracji
python3 - <<'EOF'
import json, pathlib
p = pathlib.Path.home() / "os-agenta/konfiguracja/system.json"
k = json.loads(p.read_text())
k["kontekst"] = {
    "gpt-oss-20b": {"okno": 32768, "zalamanie_igla": 0, "zalamanie_synteza": 0, "prog_kompakcji": 0},
    "qwen3-32b":   {"okno": 32768, "zalamanie_igla": 0, "zalamanie_synteza": 0, "prog_kompakcji": 0},
}
p.write_text(json.dumps(k, indent=2, ensure_ascii=False))
print("uzupełnij zerami zmierzonymi wartościami")
EOF
```

⚠️ **Predykcja do sprawdzenia:** igła utrzyma się długo — modele są trenowane pod
wyszukiwanie i „needle in a haystack" jest łatwy. **Synteza załamie się dużo wcześniej**,
prawdopodobnie w okolicach 40–60 % okna. Ponieważ Twój agent robi syntezę (czyta wynik
narzędzia, łączy z celem, decyduje), **to ta druga krzywa jest Twoim realnym limitem** —
i dlatego nie wolno ufać deklarowanej długości kontekstu.

### 8.5 · Eksperyment dodatkowy — czy kompakcja gubi liczby

```bash
# Weź 20 prawdziwych sesji z dziennika, skompaktuj, sprawdź zachowanie liczb
python3 - <<'EOF'
import re, json, pathlib
def liczby(t): return set(re.findall(r'\b\d[\d\s.,]{2,}\b', t))
# dla każdej sesji: liczby(oryginał) - liczby(streszczenie) = liczby UTRACONE
EOF
```

Zanotuj **odsetek liczb utraconych w kompakcji**. Jeśli przekracza 5 % — wzmocnij
sekcję „ZACHOWAJ DOSŁOWNIE" w prompcie i zmierz ponownie. To jest pułapka P31 z kursu 1
i jedyny sposób, żeby wiedzieć, czy Cię dotyczy.

---

## 9. ĆWICZENIE — wepnij budżet w bramę

Rozszerz bramę z części 2, żeby przy każdej turze:

1. Liczyła **rozbicie budżetu** na pozycje i dopisywała je jako zdarzenie `budzet`.
2. Wstrzykiwała do promptu linię o pozostałym budżecie, gdy zejdzie poniżej 40 %.
3. Uruchamiała kompakcję automatycznie przy progu **zmierzonym w §8**.
4. Odmawiała startu tury, gdy sam prompt systemowy + narzędzia przekraczają 50 % okna
   (to znaczy, że masz za dużo narzędzi — patrz część 7).

```bash
python3 sesja-cli.py budzet main
# oczekuj:
#   systemowy       412  ( 1.3%)
#   narzedzia      3180  ( 9.7%)
#   pliki_robocze   890  ( 2.7%)
#   historia      11240  (34.3%)
#   wyniki         8100  (24.7%)
#   ─────────────────────────────
#   razem         23822  (72.7%)  ← stan: ostrzezenie
```

> 💡 **To rozbicie jest diagnostyką, do której będziesz wracał najczęściej.** Gdy agent
> zacznie się zachowywać dziwnie, pierwsze pytanie brzmi „co zjadło kontekst" — i tu
> masz odpowiedź w jednej komendzie.

---

## 10. Pułapki tej części

| ID | Pułapka | Objaw | Jak uniknąć |
| :-- | :-- | :-- | :-- |
| **P72** | **Ufanie deklarowanej długości kontekstu** | Model „obsługuje 128 k", a myli się od 30 k | Zmierz **własną** krzywą (§8). Limit to synteza, nie igła |
| **P73** | **Zmienna wartość przed stałym prefiksem** | Prompt cache nigdy nie trafia, TTFT stale wysoki | Data, nazwa agenta, licznik — **zawsze po** narzędziach i plikach roboczych |
| **P74** | **Kompakcja od razu, bez ruchu 1 i 2** | Tracisz szczegóły, choć wystarczyło wyczyścić stare wyniki narzędzi | Kolejność 1 → 2 → 3 → zamknięcie sesji |
| **P75** | **Streszczenie zaokrągla liczby** | „prawie cztery tysiące plików" zamiast 3847; agent nie wie, czy skończył | „ZACHOWAJ DOSŁOWNIE" + pomiar z §8.5 |
| **P76** | **Prompt systemowy rośnie i nigdy nie maleje** | Po pół roku 3000 tokenów, połowa nic nie robi | Każde dodane zdanie mierzysz; nie pomogło → **usuwasz** |

---

## 11. Checkpoint

```bash
cd $OSA
python3 -c "from kontekst import Budzet, przytnij_obserwacje, kompaktuj; print('✓ import')"
test -s pomiary/kontekst/wyniki-oss20.csv && echo "✓ krzywa zmierzona"
python3 -c "
import json,pathlib
k=json.loads((pathlib.Path.home()/'os-agenta/konfiguracja/system.json').read_text())
assert k['kontekst']['gpt-oss-20b']['prog_kompakcji']>0, 'próg nieustawiony'
print('✓ próg z pomiaru w konfiguracji')"
git add -A && git commit -m "część 4: budżet kontekstu, kompakcja, krzywa degradacji"
```

- [ ] Rozumiesz różnicę: kontekst = pamięć robocza, pamięć = dysk
- [ ] Umiesz rozbić budżet na pozycje i wiesz, która rośnie najszybciej
- [ ] Prompt systemowy ma właściwą wysokość i **mierzysz każde dodane zdanie**
- [ ] Stosujesz doładowanie w ostatniej chwili zamiast wstępnego ładowania
- [ ] Kompaktujesz w kolejności 1 → 2 → 3, a nie od razu streszczeniem
- [ ] Kompakcja zostawia ślad w dzienniku; oryginał nigdy nie znika
- [ ] ⭐ **Masz zmierzoną krzywą degradacji obu modeli i próg wpisany do konfiguracji**

---

**Dalej: `05-PAMIEC-DLUGOTERMINOWA.md`** — trzy szkoły pamięci agentowej i graf
bi-temporalny, który wie, **kiedy** coś było prawdą.
