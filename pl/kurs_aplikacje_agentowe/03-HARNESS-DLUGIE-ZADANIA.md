# Część 3 · Harness — pętla, która przeżywa długie zadania

**Poziom:** ⭐⭐⭐⭐ · **Czas:** ~6 h · **Wymaga:** części 1 i 2
**Produkuje:** harness, rejestr zadań, plik postępu, agenta kończącego robotę w 5 oknach kontekstu

> ⭐ **To jest najważniejsza część kursu.** Jeśli przeczytasz tylko jedną, przeczytaj tę.
> Wszystko dalej — pamięć, narzędzia, flota — jest rozbudową tego, co tu powstaje.

---

## 0. Czym jest harness i dlaczego to on jest produktem

**Harness** to wszystko wokół wywołania modelu: co agent dostaje na starcie tury, kiedy
się zatrzymuje, co widzi po błędzie, jak przekazuje pracę następnej sesji, kto sprawdza
wynik.

Przypomnij sobie odkrycie z części 1:

> **Wynik agenta zmienia się bardziej wraz z harnessem niż z modelem.** Ten sam model pod
> dwoma szkieletami daje istotnie różne liczby.
> — [Prefactor, Agent Benchmarks](https://prefactor.tech/learn/agent-benchmarks)

I zdanie Steinbergera:

> „Nie promptuj agentów. **Projektuj pętle, które promptują agentów.**"

Obie wypowiedzi mówią to samo z dwóch stron. **Harness jest zmienną, nad którą masz
pełną kontrolę.** Wagi modelu są zmienną, nad którą nie masz żadnej.

### 0.1 · Problem w jednym obrazku

Zadanie: „uporządkuj moje dokumenty z 2026 — przeczytaj, sklasyfikuj, zmień nazwy wg
schematu, zrób indeks". 340 plików. Realnie ~6 godzin pracy agenta.

```
BEZ HARNESSU (Twoja pętla z kursu 1):

 okno 1 ████████████████████ pełne → agent gubi cel, zaczyna halucynować
        ✗ koniec. 41 plików zrobionych. Nie wiadomo które.

Z HARNESSEM:

 okno 1 ████████████████ → zapis postępu → git commit → koniec sesji
 okno 2 ████████████████ → czyta postęp, wie gdzie skończył → dalej
 okno 3 ████████████████ → …
 okno 4 ████████████████ → …
 okno 5 ██████████       → wszystkie 340, indeks, testy zielone
```

**Różnica nie leży w modelu. Leży w tym, że sesja 2 wie, co zrobiła sesja 1.**

---

## 1. Problem zimnego startu

Za każdym razem, gdy sesja się kończy, agent **traci całą pamięć roboczą**. Nowa sesja
startuje z pustym kontekstem. Anthropic nazywa to sednem sprawy:

> Kluczowe jest znalezienie sposobu, by agent **szybko zrozumiał stan pracy**, startując
> z czystym oknem kontekstu.
> — [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

Nowa sesja musi w ciągu **pierwszych ~2000 tokenów** odpowiedzieć sobie na cztery pytania:

| Pytanie | Skąd bierze odpowiedź |
| :-- | :-- |
| Co mam zrobić? | **rejestr zadań** (`zadanie.json`) |
| Co już zrobiono? | **plik postępu** (`POSTEP.md`) + `git log` |
| Czy to, co zrobiono, **działa**? | **testy bazowe** uruchamiane na starcie |
| Co robię teraz? | pierwsza nieukończona pozycja rejestru |

⭐ **To są cztery artefakty i wszystkie są plikami.** Nie ma tu nic o modelu, kontekście
ani promptach. **Pamięć długoterminowa agenta to system plików** — i to jest cała
tajemnica.

---

## 2. Rejestr zadań — lekarstwo na „gotowe!", gdy nie jest gotowe

Najczęstszy i najbardziej wkurzający tryb awarii agenta: **mówi, że skończył, a nie
skończył**. W eksperymencie z części 1 nazwałeś go `CICHY`.

Przyczyna jest strukturalna, nie promptowa. Agent nie ma **obiektywnej definicji
ukończenia** — więc używa subiektywnej: „zrobiłem sporo, brzmi jak koniec".

**Lekarstwo: rozbij zadanie na listę pozycji o binarnym stanie, z krokiem testowym przy
każdej.**

```json
{
  "zadanie": "Uporządkuj dokumenty z 2026",
  "utworzone": "2026-09-23T08:00:00Z",
  "zasady": [
    "NIE WOLNO usuwać ani zmieniać kroków testowych.",
    "Pozycja jest 'zrobione' dopiero gdy krok testowy przechodzi.",
    "Przy wątpliwości zostaw 'w_toku' i opisz blokadę."
  ],
  "pozycje": [
    {
      "id": "P01",
      "opis": "Zinwentaryzuj wszystkie pliki z 2026 do inwentarz.csv",
      "test": "wc -l < inwentarz.csv  → oczekuj 340",
      "stan": "zrobione",
      "uwagi": "3 pliki bez daty w metadanych — wzięte z nazwy"
    },
    {
      "id": "P02",
      "opis": "Sklasyfikuj każdy plik do jednej z 6 kategorii",
      "test": "python3 sprawdz.py kategorie  → 0 pustych, 0 spoza słownika",
      "stan": "w_toku",
      "uwagi": "zrobione 180/340, ostatni: faktura-2026-03-11.pdf"
    },
    {
      "id": "P03",
      "opis": "Zmień nazwy wg schematu RRRR-MM-DD_kategoria_opis",
      "test": "python3 sprawdz.py nazwy  → 0 niezgodnych",
      "stan": "do_zrobienia",
      "uwagi": ""
    }
  ]
}
```

### 2.1 · Trzy reguły, bez których to nie działa

**1 · Krok testowy musi być wykonywalnym poleceniem, nie opisem.**

```
✗ "test": "sprawdź, czy kategorie są poprawne"     ← agent oceni sam siebie
✓ "test": "python3 sprawdz.py kategorie"           ← werdykt z zewnątrz
```

To jest bezpośrednie zastosowanie odkrycia o **weryfikacji zewnętrznej**: samo-refleksja
ma skrzywienie samo-potwierdzające, bo sędzia siedzi w tym samym stanie trajektorii co
autor ([arXiv 2603.02798](https://arxiv.org/pdf/2603.02798)). Kod uruchomiony w powłoce
nie jest w tym stanie. **Wykonanie jest najmocniejszym sygnałem weryfikacyjnym, jaki
masz** — w części 14 rozwiniesz to w pełną ewaluację.

**2 · Agentowi nie wolno kasować ani zmieniać testów.**

Anthropic stawia to jako zasadę twardą: *„It is unacceptable to remove or edit tests
because this could lead to missing or buggy functionality."* Agent pod presją
nieprzechodzącego testu **usunie test** — to jest lokalnie optymalne i globalnie
katastrofalne. Zasada w pliku to za mało; w §9 wymuszasz to kodem.

**3 · Stan `w_toku` musi nieść, gdzie dokładnie przerwano.**

`"zrobione 180/340, ostatni: faktura-2026-03-11.pdf"` to różnica między wznowieniem
a zaczynaniem od nowa.

---

## 3. Plik postępu — narracja dla następnej sesji

Rejestr mówi **co**. Plik postępu mówi **jak i czego się nauczyłem**.

```markdown
# POSTĘP · Uporządkuj dokumenty z 2026

## Stan na 2026-09-23 11:40 (sesja 3)

Zrobione: P01. W toku: P02 (180/340).

## Czego się nauczyłem — czytaj to, zanim zaczniesz

- Pliki w `~/dokumenty/skan/` mają datę **tylko w nazwie**, metadane są puste.
  Używaj `parsuj_nazwe()`, nie `os.path.getmtime`.
- Kategoria „umowa" i „aneks" są mylone. Aneks ma zawsze w pierwszych
  200 znakach słowo „aneks" albo „zmieniający". Dodałem to do `sprawdz.py`.
- ⚠️ **NIE uruchamiaj `zmien_nazwy.py` bez `--sucho`.** Raz nadpisałem dwa pliki
  o tej samej dacie. Naprawione przez kopię zapasową, ale nie powtarzaj.

## Zablokowane

Nic.

## Następny krok

`P02` od `faktura-2026-03-11.pdf`. Lista pozostałych w `pozostale.txt`.
```

> 💡 **Sekcja „Czego się nauczyłem" jest tu najcenniejsza** i to ona odróżnia harness od
> zwykłego wznawiania. Bez niej sesja 4 **powtórzy błąd sesji 2** — bo nie ma skąd
> wiedzieć, że ktoś już w to wdepnął. To jest pamięć proceduralna agenta i pierwszy
> zarodek tego, co w części 5 rozwiniesz w pamięć długoterminową.

---

## 4. Git jako pamięć agenta

Anthropic używa gita w harnessie nie do wersjonowania, tylko **jako mechanizmu pamięci**:

| Do czego | Jak |
| :-- | :-- |
| „Co zrobiła poprzednia sesja" | `git log --oneline -20` — tańsze niż czytanie plików |
| „Czy ja to już zmieniałem" | `git diff HEAD~1` |
| „Zepsułem, cofnij" | `git reset --hard` — **odzyskiwanie po błędzie za darmo** |
| „Kiedy to się zepsuło" | `git bisect` |

**Reguła: jeden commit na ukończoną pozycję rejestru**, z komunikatem zawierającym `id`.

```
P01: inwentaryzacja 340 plików do inwentarz.csv
P02: klasyfikacja 180/340 (przerwane, wznowić od faktura-2026-03-11)
```

⭐ **Dlaczego commit przy `w_toku`, nie tylko przy `zrobione`.** Bo sesja kończy się
w środku pozycji znacznie częściej niż na jej granicy. Commit „przerwane, wznowić od X"
jest **tańszym nośnikiem stanu niż jakikolwiek plik**, który musiałbyś napisać.

---

## 5. Sekwencja startowa — pierwsze 60 sekund sesji

Każda sesja robocza wykonuje **identyczną, sztywną sekwencję**, zanim dotknie zadania.
To nie jest prompt — to jest kod.

```
1. Ustal miejsce        pwd, sprawdź że to katalog zadania
2. Przeczytaj historię  git log -15, POSTEP.md, zadanie.json
3. Zweryfikuj bazę      uruchom testy WSZYSTKICH pozycji 'zrobione'
4. Wybierz pracę        pierwsza pozycja 'w_toku', potem 'do_zrobienia'
5. Zadeklaruj zamiar    dopisz do POSTEP.md: "sesja N zaczyna P0X"
6. → praca
7. Zamknij              zaktualizuj rejestr + postęp, commit, testy końcowe
```

**Krok 3 jest tym, który wszyscy pomijają, i tym, który ratuje projekt.**

Jeśli sesja 2 zepsuła coś, co sesja 1 zrobiła poprawnie, **dowiesz się o tym na starcie
sesji 3**, a nie po sześciu godzinach. Koszt: kilkanaście sekund na sesję. Zwrot:
wykrycie regresji w oknie, w którym da się ją jeszcze przypisać do przyczyny.

> ⚠️ **Tryb awarii, który to łapie, jest podstępny.** Agent poprawia P02 i „przy okazji"
> refaktoryzuje funkcję używaną przez P01. P01 nadal ma stan `zrobione` w rejestrze, ale
> jego test już nie przechodzi. Bez kroku 3 **rejestr kłamie do samego końca**.

---

## 6. Zatrzymywanie — pięć warunków, nie jeden

Pętla z kursu 1 kończyła się, gdy model przestał wołać narzędzia. To jest jeden warunek
i **zdecydowanie za mało**.

| # | Warunek | Dlaczego | Co robić po |
| :-- | :-- | :-- | :-- |
| 1 | **Zadanie ukończone** | wszystkie pozycje `zrobione` + testy zielone | commit, raport |
| 2 | **Budżet kontekstu** (~70 % okna) | dalej zaczyna się context rot (część 4) | **kompakcja albo zamknięcie sesji** |
| 3 | **Budżet tur** (np. 40) | zabezpieczenie przed zapętleniem | zapis postępu, zamknięcie |
| 4 | **Brak postępu** (3 tury bez zmiany stanu) | agent kręci się w kółko | eskalacja: inny model albo człowiek |
| 5 | **Blokada twarda** | brak uprawnień, brak pliku, brak sieci | zapis blokady, **zawołaj człowieka** |

⭐ **Warunek 4 jest najtrudniejszy do wykrycia i najcenniejszy.** „Brak postępu" nie
znaczy „brak aktywności" — agent może pracowicie czytać ten sam plik piąty raz. Mierz
**zmianę stanu świata**, nie liczbę tur:

```python
def odcisk_stanu(katalog: str) -> str:
    """Hash stanu świata. Zmienił się = był postęp."""
    import hashlib, subprocess
    h = hashlib.sha256()
    h.update(subprocess.run(["git", "status", "--porcelain"],
                            cwd=katalog, capture_output=True).stdout)
    h.update(pathlib.Path(katalog, "zadanie.json").read_bytes())
    return h.hexdigest()[:16]
```

Trzy tury z tym samym odciskiem = agent nie robi nic użytecznego, **niezależnie od tego,
jak pracowicie wygląda**.

---

## 7. Drabina odzyskiwania po błędzie

Pamiętasz arytmetykę z części 1: 0,92¹⁵ = 29 %. Przy 15 krokach **błąd jest normą, nie
wyjątkiem**. Harness, który nie umie się po błędzie pozbierać, jest bezużyteczny.

**Reguła: eskaluj kosztem, nie od razu na maksimum.**

| Szczebel | Reakcja | Koszt | Kiedy |
| :-- | :-- | :-- | :-- |
| 0 | **Pokaż błąd modelowi i pozwól poprawić** | 1 tura | zawsze najpierw |
| 1 | **Pokaż błąd + podpowiedź strukturalną** | 1 tura | druga próba tego samego narzędzia |
| 2 | **Cofnij ostatnią akcję, spróbuj inaczej** | `git checkout` + 1 tura | trzecia próba |
| 3 | **Podziel pozycję na mniejsze** | przepisanie rejestru | zadanie za duże na jedną turę |
| 4 | **Zmień model na mocniejszy** | ~3× czas | wyczerpane 0–3 |
| 5 | **Zatrzymaj, zawołaj człowieka** | Twój czas | blokada twarda lub wyczerpane wszystko |

⚠️ **Szczebel 0 wymaga, żeby błąd był czytelny dla modelu.** To jest bezpośrednio reguła
Steinbergera z MCP Best Practices: *„w razie błędu wyemituj komunikat z informacją
pozwalającą się pozbierać"*. Porównaj:

```
✗  Traceback (most recent call last): … PermissionError: [Errno 13]
✓  BŁĄD: brak prawa zapisu do /etc/hosts.
   Piaskownica pozwala pisać tylko w $OSA/ i /tmp/.
   Jeśli chcesz zapisać wynik — użyj /tmp/wynik.txt.
```

Pierwszy komunikat daje modelowi 20 % szans na poprawę. Drugi — powyżej 90 %.
**Komunikat błędu jest częścią promptu.** Pisz go jak prompt.

---

## 8. Loop engineering w praktyce — siedem dźwigni

Skoro projektujesz pętlę, a nie prompt, warto wiedzieć, **co w pętli da się kręcić**.

| # | Dźwignia | Pytanie | Gdzie w kursie |
| :-- | :-- | :-- | :-- |
| 1 | **Wejście tury** | Co agent widzi na starcie każdej tury? | ta część, 4 |
| 2 | **Widoczność narzędzi** | Wszystkie naraz czy doładowywane? | 7, 8 |
| 3 | **Kształt obserwacji** | Surowy wynik czy przycięty i opisany? | 7 |
| 4 | **Warunek stopu** | Kiedy przerywasz? | ta część, §6 |
| 5 | **Reakcja na błąd** | Co widzi po porażce? | ta część, §7 |
| 6 | **Przekazanie** | Co dostaje następna sesja? | ta część, §2–4 |
| 7 | **Weryfikacja** | Kto sprawdza — i czy z zewnątrz? | 14 |

> 🎯 **Ćwiczenie myślowe, które warto robić przy każdym błędzie agenta.** Zamiast pytać
> „jak przeformułować prompt", zapytaj: **„którą z tych siedmiu dźwigni powinienem
> ruszyć?"** W 8 przypadkach na 10 odpowiedź nie brzmi „prompt".

---

## 9. OD ZERA — harness

```python
# $OSA/harness.py
"""Harness: pętla przeżywająca wiele okien kontekstu."""
import json, pathlib, subprocess, hashlib, datetime, shutil

TERAZ = lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

class Rejestr:
    """zadanie.json — binarny stan pozycji, testy nienaruszalne."""
    def __init__(self, katalog):
        self.kat = pathlib.Path(katalog)
        self.plik = self.kat / "zadanie.json"
        self.dane = json.loads(self.plik.read_text(encoding="utf-8"))
        self._testy_odcisk = self._odcisk_testow()

    def _odcisk_testow(self) -> str:
        t = "|".join(f'{p["id"]}::{p["test"]}' for p in self.dane["pozycje"])
        return hashlib.sha256(t.encode()).hexdigest()

    def nastepna(self) -> dict | None:
        for stan in ("w_toku", "do_zrobienia"):
            for p in self.dane["pozycje"]:
                if p["stan"] == stan:
                    return p
        return None

    def ustaw(self, id_: str, stan: str, uwagi: str = ""):
        for p in self.dane["pozycje"]:
            if p["id"] == id_:
                p["stan"], p["uwagi"] = stan, uwagi or p["uwagi"]
        self.zapisz()

    def zapisz(self):
        # P67: agent NIE MOŻE zmienić ani usunąć testu.
        if self._odcisk_testow() != self._testy_odcisk:
            raise PermissionError(
                "ZABLOKOWANE: próba zmiany kroków testowych w zadanie.json. "
                "Testy są nienaruszalne. Jeśli test jest zły — zgłoś to człowiekowi.")
        self.plik.write_text(json.dumps(self.dane, indent=2, ensure_ascii=False),
                             encoding="utf-8")

    def test(self, poz: dict) -> tuple[bool, str]:
        polecenie = poz["test"].split("→")[0].strip()
        w = subprocess.run(polecenie, shell=True, cwd=self.kat,
                           capture_output=True, text=True, timeout=120)
        return w.returncode == 0, (w.stdout + w.stderr)[-800:]

    def weryfikuj_baze(self) -> list[str]:
        """Krok 3 sekwencji startowej. Zwraca ID-ki, które REGRESOWAŁY."""
        zepsute = []
        for p in self.dane["pozycje"]:
            if p["stan"] == "zrobione":
                ok, _ = self.test(p)
                if not ok:
                    zepsute.append(p["id"])
                    p["stan"] = "w_toku"
                    p["uwagi"] = f"REGRESJA wykryta {TERAZ()} — było 'zrobione'"
        if zepsute:
            self.zapisz()
        return zepsute
```

```python
# $OSA/harness.py (ciąg dalszy)

def git(kat, *a) -> str:
    return subprocess.run(["git", *a], cwd=kat, capture_output=True,
                          text=True).stdout.strip()

def odcisk_stanu(kat) -> str:
    h = hashlib.sha256()
    h.update(git(kat, "status", "--porcelain").encode())
    h.update((pathlib.Path(kat) / "zadanie.json").read_bytes())
    return h.hexdigest()[:16]

def sekwencja_startowa(kat: str) -> dict:
    """Pierwsze 60 sekund sesji. Zwraca pakiet startowy dla modelu."""
    r = Rejestr(kat)
    postep = (pathlib.Path(kat) / "POSTEP.md")
    zepsute = r.weryfikuj_baze()                       # krok 3
    poz = r.nastepna()                                 # krok 4
    return {
        "katalog": kat,
        "zadanie": r.dane["zadanie"],
        "historia_git": git(kat, "log", "--oneline", "-15"),
        "postep": postep.read_text(encoding="utf-8") if postep.exists() else "(brak)",
        "regresje": zepsute,
        "pozycja": poz,
        "pozostalo": sum(1 for p in r.dane["pozycje"] if p["stan"] != "zrobione"),
        "rejestr": r,
    }

SZABLON_STARTU = """Pracujesz nad zadaniem wieloetapowym. To jest sesja robocza.

# Zadanie
{zadanie}

# Co zrobiono wcześniej (git)
{historia_git}

# Notatki poprzednich sesji — PRZECZYTAJ, zanim zaczniesz
{postep}
{blok_regresji}
# Twoja pozycja w tej sesji
{pozycja_id}: {pozycja_opis}
Krok testowy (NIE WOLNO go zmieniać): {pozycja_test}
Notatki do tej pozycji: {pozycja_uwagi}

Pozostało pozycji: {pozostalo}

# Zasady
1. Pracujesz WYŁĄCZNIE nad tą jedną pozycją.
2. Pozycja jest ukończona dopiero, gdy krok testowy przechodzi. Uruchom go.
3. Gdy skończysz albo utkniesz — zapisz stan do POSTEP.md i zrób commit.
4. Jeśli test jest błędny — NIE zmieniaj go. Opisz problem i zatrzymaj się.
"""

def pakiet_startowy(s: dict) -> str:
    blok = ""
    if s["regresje"]:
        blok = (f"\n# ⚠️ REGRESJA\nPozycje {', '.join(s['regresje'])} były 'zrobione', "
                f"a ich testy już nie przechodzą. Napraw je PRZED nową pracą.\n")
    p = s["pozycja"] or {"id": "—", "opis": "brak pracy", "test": "—", "uwagi": ""}
    return SZABLON_STARTU.format(
        zadanie=s["zadanie"], historia_git=s["historia_git"], postep=s["postep"],
        blok_regresji=blok, pozycja_id=p["id"], pozycja_opis=p["opis"],
        pozycja_test=p["test"], pozycja_uwagi=p["uwagi"] or "(brak)",
        pozostalo=s["pozostalo"])
```

```python
# $OSA/harness.py (koniec) — pętla sesji z pięcioma warunkami stopu

MAX_TUR         = 40
BUDZET_KONTEKSTU = 0.70
BEZ_POSTEPU_MAX = 3

def sesja_robocza(kat: str, wywolaj_model, wykonaj_narzedzie, okno_tokenow=32768):
    s = sekwencja_startowa(kat)
    if s["pozycja"] is None:
        return {"powod": "ukonczone", "tur": 0}

    r: Rejestr = s["rejestr"]
    historia = [{"rola": "user", "tresc": pakiet_startowy(s)}]
    odcisk, bez_postepu, uzyte = odcisk_stanu(kat), 0, 0

    for tura in range(1, MAX_TUR + 1):
        odp = wywolaj_model(historia)
        uzyte = odp["tokeny_we"] + odp["tokeny_wy"]

        if odp.get("narzedzie"):
            wynik = wykonaj_narzedzie(odp["narzedzie"], odp["argumenty"])
            historia += [{"rola": "assistant", "tresc": odp["tresc"]},
                         {"rola": "tool", "tresc": wynik}]
        else:
            historia.append({"rola": "assistant", "tresc": odp["tresc"]})

        # --- warunki stopu, w kolejności ważności ---
        ok, wyjscie = r.test(s["pozycja"])
        if ok:                                                        # 1
            r.ustaw(s["pozycja"]["id"], "zrobione", f"ukończone {TERAZ()}")
            zamknij(kat, r, s["pozycja"], "zrobione", tura)
            return {"powod": "pozycja_ukonczona", "tur": tura}

        if uzyte > okno_tokenow * BUDZET_KONTEKSTU:                   # 2
            zamknij(kat, r, s["pozycja"], "budżet kontekstu", tura)
            return {"powod": "kontekst", "tur": tura}

        nowy = odcisk_stanu(kat)                                      # 4
        bez_postepu = bez_postepu + 1 if nowy == odcisk else 0
        odcisk = nowy
        if bez_postepu >= BEZ_POSTEPU_MAX:
            zamknij(kat, r, s["pozycja"], "brak postępu — eskalacja", tura)
            return {"powod": "brak_postepu", "tur": tura}

    zamknij(kat, r, s["pozycja"], "limit tur", MAX_TUR)               # 3
    return {"powod": "limit_tur", "tur": MAX_TUR}

def zamknij(kat, r: Rejestr, poz, powod, tura):
    """Krok 7. Postęp + commit. Wykonywany ZAWSZE, także przy awarii."""
    p = pathlib.Path(kat) / "POSTEP.md"
    p.write_text((p.read_text(encoding="utf-8") if p.exists() else "# POSTĘP\n")
                 + f"\n## {TERAZ()} — {poz['id']} — {powod} (tur: {tura})\n"
                   f"Stan: {poz['stan']}. {poz['uwagi']}\n", encoding="utf-8")
    git(kat, "add", "-A")
    git(kat, "commit", "-m", f"{poz['id']}: {powod} ({poz['stan']})")
```

---

## 10. PRODUKCYJNIE — co dają gotowe harnessy

| Element | Claude Agent SDK | LangGraph | **Twój** |
| :-- | :-- | :-- | :-- |
| Automatyczna kompakcja | ⭐ wbudowana | ✗ | ręcznie (część 4) |
| Punkty kontrolne | sesje | ⭐ checkpointer + time-travel | dziennik + gałęzie (część 2) |
| Wznowienie z zimnego startu | częściowo | przez checkpointer | ⭐ **rejestr + postęp + git** |
| **Nienaruszalność testów** | ✗ | ✗ | ⭐ **wymuszona kodem** |
| Wykrywanie braku postępu | ✗ | ręcznie | ⭐ odcisk stanu |
| Weryfikacja bazy na starcie | ✗ | ✗ | ⭐ krok 3 |
| Dojrzałość | wysoka | wysoka | Twoja |

**Trzy gwiazdki w Twojej kolumnie to nie przypadek.** Gotowe frameworki rozwiązują
problem „jak uruchomić agenta". Ty rozwiązujesz problem **„jak sprawić, żeby agent
skończył robotę i żebyś mu uwierzył"** — a to jest inny i rzadziej adresowany problem.

> ⚠️ **Uczciwie: gdzie Twój harness przegrywa.** Nie ma automatycznej kompakcji (robisz
> ją w części 4), nie ma streamingu i nie ma podróży w czasie po stanie grafu. Jeśli
> kiedyś zaczniesz budować przepływy zatwierdzane przez audytora — checkpointer
> LangGraph będzie lepszy, bo **da się go narysować**.

---

## 11. EKSPERYMENT 3 — zadanie na pięć okien kontekstu

**Hipoteza:** to samo zadanie, które bez harnessu kończy się porażką w pierwszym oknie,
z harnessem kończy się sukcesem w kilku sesjach — **na tym samym modelu**.

**Zadanie testowe** (nie wymaga Twoich prywatnych plików):

```bash
mkdir -p $OSA/proby/korpus && cd $OSA/proby
python3 - <<'EOF'
import random, pathlib
random.seed(42)
kat = pathlib.Path("korpus"); kat.mkdir(exist_ok=True)
typy = ["faktura", "umowa", "aneks", "notatka", "raport", "pismo"]
for i in range(340):
    t = random.choice(typy)
    m, d = random.randint(1,9), random.randint(1,28)
    tresc = f"{'ANEKS zmieniający' if t=='aneks' else t.upper()} nr {i}\n" + "treść "*random.randint(20,200)
    (kat / f"dok_{i:03d}.txt").write_text(tresc, encoding="utf-8")
print("340 plików gotowych")
EOF
git init && git add -A && git commit -q -m "korpus startowy"
```

Zbuduj `zadanie.json` z czterema pozycjami (inwentarz → klasyfikacja → nazwy → indeks),
każda z **wykonywalnym** krokiem testowym.

**Przebieg A — bez harnessu.** Uruchom pętlę z kursu 1 z pełnym opisem zadania w jednym
promptcie. Zanotuj, gdzie umarła.

**Przebieg B — z harnessem.** Uruchamiaj `sesja_robocza()` w pętli, aż zwróci
`ukonczone` albo pięć razy z rzędu ten sam powód.

**Tabela wyników:**

| Miara | A (bez) | B (z harnessem) |
| :-- | --: | --: |
| Pozycji ukończonych /4 | | |
| Sesji | 1 | |
| Tur łącznie | | |
| Tokenów łącznie | | |
| Czas łączny | | |
| Wykrytych regresji | 0 | |
| Tryb zakończenia | | |

⚠️ **Predykcja do sprawdzenia:** A kończy pozycję 1, może zacznie 2, i umrze na
`KONTEKST` albo `CICHY`. B skończy wszystkie cztery w 4–7 sesjach, zużywając **więcej
tokenów łącznie** (bo każda sesja czyta pakiet startowy) i **mniej Twojego czasu**.

⭐ **Jeśli B zużyje więcej tokenów niż A, to nie jest porażka.** To jest cena, którą
płacisz za skończone zadanie. Porównujesz „drożej i gotowe" z „taniej i nieskończone" —
a to nie jest ta sama jednostka.

---

## 12. ĆWICZENIE — agent inicjalizujący

Anthropic dzieli agentów na **inicjalizującego** (pierwsza sesja) i **roboczego**
(wszystkie kolejne). Zbudowałeś roboczego. Napisz inicjalizującego:

```bash
python3 harness.py inicjuj "Uporządkuj dokumenty z 2026" $OSA/proby
```

Ma wyprodukować:

1. **`zadanie.json`** — rozbicie na 4–8 pozycji, każda z **wykonywalnym** testem
2. **`sprawdz.py`** — skrypt, który te testy realizuje
3. **`POSTEP.md`** — pusty, z nagłówkami sekcji
4. **`init.sh`** — odtwarza środowisko od zera
5. **pierwszy commit** — baza, do której da się wrócić

**Kryterium jakości, które naprawdę coś mierzy:** usuń wszystko poza `korpus/`
i `init.sh`, uruchom `init.sh`, i sprawdź, czy agent roboczy **wystartuje bez Twojej
pomocy**. Jeśli nie — inicjalizujący był za słaby i to jest właściwa diagnoza.

> 💡 **Dlaczego to rozdzielenie ma sens.** Inicjalizujący i roboczy mają **sprzeczne
> cele**. Inicjalizujący ma być rozrzutny: przemyśleć zadanie, rozbić, napisać testy —
> raz, drogo, dobrze. Roboczy ma być oszczędny: wejść, zrobić jedną rzecz, wyjść.
> Jeden prompt nie obsłuży obu, bo optymalizują co innego.

---

## 13. Pułapki tej części

| ID | Pułapka | Objaw | Jak uniknąć |
| :-- | :-- | :-- | :-- |
| **P67** | **Agent zmienia lub kasuje test, żeby przeszedł** | Wszystko zielone, funkcjonalność nie działa | Odcisk testów sprawdzany przy każdym zapisie rejestru (`Rejestr.zapisz`) |
| **P68** | **Pozycja rejestru za duża na jedną sesję** | Zawsze `w_toku`, nigdy `zrobione`, postęp pozorny | Pozycja musi mieścić się w ~60 % okna. Za duża → dziel (szczebel 3 drabiny) |
| **P69** | **Pominięcie weryfikacji bazy na starcie** | Regresja z sesji 2 wychodzi w sesji 9, gdy nie wiesz już dlaczego | Krok 3 sekwencji startowej. Kilkanaście sekund |
| **P70** | **Brak postępu mylony z brakiem aktywności** | Agent pracowicie czyta ten sam plik 5 razy i licznik tur rośnie | Mierz **odcisk stanu świata**, nie liczbę tur |
| **P71** | **Komunikat błędu nieczytelny dla modelu** | Agent poddaje się po pierwszej porażce zamiast poprawić | Błąd = prompt. Napisz co poszło źle, dlaczego i **co wolno zamiast tego** |

---

## 14. Checkpoint

```bash
cd $OSA
python3 -c "import harness; print('✓ import')"
python3 - <<'EOF'
from harness import Rejestr
r = Rejestr("proby")
r.dane["pozycje"][0]["test"] = "echo oszustwo"
try:
    r.zapisz(); print("✗ P67 NIE DZIAŁA — testy dają się podmienić")
except PermissionError:
    print("✓ P67 — testy nienaruszalne")
EOF
git add -A && git commit -m "część 3: harness, rejestr zadań, sekwencja startowa"
```

- [ ] Rozumiesz, dlaczego harness > model
- [ ] Rejestr zadań ma binarne stany i **wykonywalne** testy
- [ ] Testów nie da się zmienić — wymuszone kodem, nie prośbą
- [ ] `POSTEP.md` niesie „czego się nauczyłem", nie tylko „co zrobiłem"
- [ ] Git jest mechanizmem pamięci, nie tylko wersjonowania
- [ ] Sekwencja startowa **weryfikuje bazę** przed nową pracą
- [ ] Pięć warunków stopu, w tym wykrywanie braku postępu
- [ ] Drabina odzyskiwania eskaluje kosztem
- [ ] **Zadanie na 5 okien kontekstu przechodzi od początku do końca**

---

**Dalej: `04-INZYNIERIA-KONTEKSTU.md`** — budżet uwagi, context rot zmierzony na Twoich
modelach, i kompakcja, która nie gubi liczb.
