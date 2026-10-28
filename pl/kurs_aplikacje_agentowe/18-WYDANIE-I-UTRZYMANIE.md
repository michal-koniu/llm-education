# Część 18 · Wydanie i utrzymanie

**Poziom:** ⭐⭐⭐⭐ · **Czas:** ~4 h · **Wymaga:** części 14 (bramka), 15 (metryki), 16 (bezpieczeństwo)
**Produkuje:** wersjonowanie systemu, wycofanie, migrację pamięci, kopie zapasowe, runbook

---

## 0. Co to znaczy „wydać" system agentowy

W zwykłym oprogramowaniu wydanie to kod. Tutaj zachowanie zależy od **siedmiu rzeczy**,
i zmiana **każdej** z nich zmienia wynik:

```
   kod        ██████░░░░░░░░░░░░░░   ~30 % wpływu na zachowanie
   prompty    ████████░░░░░░░░░░░░   ~25 %
   narzędzia  █████░░░░░░░░░░░░░░░   ~15 %
   model      █████░░░░░░░░░░░░░░░   ~15 %
   konfig.    ███░░░░░░░░░░░░░░░░░   ~8 %
   umiejętn.  ██░░░░░░░░░░░░░░░░░░   ~5 %
   pamięć     █░░░░░░░░░░░░░░░░░░░   ~2 %  ⚠️ ale rośnie w czasie
```

⚠️ **Zmiana promptu bez zmiany kodu jest pełnoprawnym wydaniem.** Ma taki sam wpływ
jak zmiana kodu, a prawie nikt jej tak nie traktuje. To jest **główna przyczyna
sytuacji „działało w zeszłym tygodniu"**.

⭐ **Reguła: wydanie to zamrożony stan WSZYSTKICH siedmiu, z zapisanym wynikiem
zbioru złotego.** Bez wyniku nie jest to wydanie, tylko zbieg okoliczności.

---

## 1. Manifest wydania

```python
# $OSA/wydanie/manifest.py
def zbuduj(wersja: str) -> dict:
    return {
        "wersja": wersja,
        "data": TERAZ(),
        "git": _git("rev-parse", "HEAD"),
        "czyste_repo": _git("status", "--porcelain") == "",   # ⚠️ P136
        "skladniki": {
            "prompty":     _sha_katalogu("agenci", "*.md"),
            "narzedzia":   _sha_katalogu("narzedzia", "*.py"),
            "umiejetnosci":_sha_katalogu("agenci/*/umiejetnosci", "SKILL.md"),
            "konfiguracja":_sha_pliku("konfiguracja/system.json"),
            "modele": {n: {"plik": s["model"], "sha256": _sha_modelu(s["model"])}
                       for n, s in SILNIKI.items() if "url" in s},
            "silnik": _wersja_llama_cpp(),
        },
        "ewaluacja": json.loads(pathlib.Path("pomiary/ewaluacja/biezacy.json").read_text()),
        "schemat_pamieci": _wersja_schematu_pamieci(),
    }
```

⭐ **`sha256` pliku GGUF jest tu nieoczywisty, ale konieczny.** Ponowne pobranie
modelu „tej samej" wersji potrafi dać inny plik — inna kwantyzacja, poprawka
w konwersji, inny build. Bez sumy kontrolnej **wycofanie nie odtworzy zachowania**
i będziesz szukał przyczyny w kodzie, którego nikt nie ruszał.

---

## 2. Potok wydania

```bash
#!/usr/bin/env bash
# $OSA/wydanie/wydaj.sh
set -euo pipefail
WERSJA="${1:?wersja, np. 1.4.0}"

echo "1/7 · czystość repozytorium"
[ -z "$(git status --porcelain)" ] || { echo "✗ niezacommitowane zmiany"; exit 1; }

echo "2/7 · testy jednostkowe"
python3 -m pytest testy/ -q

echo "3/7 · próby ucieczki (część 10)"
python3 testy/ucieczka/proby.py --poziom scisly --wymagaj-porazki-wszystkich

echo "4/7 · ataki ASI (część 16)"
python3 testy/ataki/ataki.py --wszystkie --min-zdanych 18

echo "5/7 · zbiór złoty — 3 przebiegi"
python3 ewaluacja/uruchom.py --przebiegow 3 --zapisz pomiary/ewaluacja/biezacy.json

echo "6/7 · bramka regresji (część 14)"
python3 ewaluacja/bramka.py --wzgledem pomiary/ewaluacja/baza.json || {
  echo "✗ REGRESJA. Wydanie wstrzymane."; exit 1; }

echo "7/7 · manifest i znacznik"
python3 wydanie/manifest.py "$WERSJA" > "wydania/$WERSJA.json"
git add wydania/ && git commit -q -m "wydanie $WERSJA"
git tag -a "v$WERSJA" -m "$(python3 wydanie/podsumuj.py "$WERSJA")"
echo "✓ wydanie $WERSJA gotowe.  Wycofanie: wydanie/wycofaj.sh <poprzednia>"
```

⭐ **Krok 6 jest sercem tego potoku.** Wszystko inne to higiena; bramka regresji to
jedyny mechanizm, który **zatrzyma Cię przed pogorszeniem systemu w dobrej wierze**.

---

## 3. Wycofanie

```bash
#!/usr/bin/env bash
# $OSA/wydanie/wycofaj.sh — cel: poniżej 5 minut
set -euo pipefail
WERSJA="${1:?wersja docelowa}"
M="wydania/$WERSJA.json"
[ -f "$M" ] || { echo "✗ brak manifestu $M"; exit 1; }

echo "→ zatrzymywanie"
systemctl --user stop osa-brama osa-planista

echo "→ kopia stanu bieżącego (na wypadek, gdyby wycofanie było pomyłką)"
tar czf "/tmp/osa-przed-wycofaniem-$(date +%s).tgz" pamiec/ dziennik/ konfiguracja/

echo "→ kod, prompty, konfiguracja"
git checkout "v$WERSJA" -- agenci/ narzedzia/ konfiguracja/ *.py

echo "→ weryfikacja modeli"
python3 wydanie/sprawdz_modele.py "$M" || {
  echo "⚠️ MODEL SIĘ NIE ZGADZA. Zachowanie może odbiegać od wydania $WERSJA."; }

echo "→ migracja pamięci wstecz"
python3 pamiec/migruj.py --do-wersji "$(jq -r .schemat_pamieci "$M")"

echo "→ start i kontrola"
systemctl --user start osa-brama osa-planista
sleep 5 && python3 wydanie/kontrola.py --szybka
echo "✓ wycofano do $WERSJA"
```

⚠️ **Kopia stanu przed wycofaniem** — bo wycofanie bywa błędną diagnozą, a wtedy
chcesz wrócić do tego, co właśnie nadpisałeś.

### 3.1 · Pamięć nie wraca

⭐ **To jest najważniejsza rzecz w tej części i najłatwiejsza do przeoczenia.**

Kod wraca. Prompty wracają. **Pamięć zgromadzona między wydaniami — nie**, i nie
powinna: to są prawdziwe fakty o Tobie zebrane przez tydzień.

```python
# $OSA/pamiec/migruj.py
MIGRACJE = {
    (1, 2): lambda db: db.executescript("""
        ALTER TABLE fakty ADD COLUMN pewnosc REAL DEFAULT 1.0;
        UPDATE fakty SET pewnosc = 1.0 WHERE pewnosc IS NULL;"""),
    (2, 3): lambda db: db.executescript("""
        ALTER TABLE fakty ADD COLUMN cytat TEXT;"""),
}
WSTECZ = {
    (2, 1): lambda db: None,      # ⭐ kolumna zostaje — stary kod jej nie czyta
    (3, 2): lambda db: None,
}
```

⭐ **Wzorzec „migracja wstecz nic nie robi" jest poprawny i celowy.** Nie usuwasz
kolumny — stary kod po prostu jej nie czyta, a dane przetrwają powrót do nowszej
wersji. **Usunięcie kolumny przy wycofaniu to nieodwracalna utrata danych z powodu,
który miał być odwracalny.**

**Zasada: schemat pamięci zmienia się tylko przez dopisanie.** Żadnych `DROP COLUMN`,
żadnych zmian typu, żadnych zmian znaczenia istniejącego pola.

---

## 4. Kopie zapasowe

| Co | Częstość | Gdzie | Dlaczego |
| :-- | :-- | :-- | :-- |
| `pamiec/pamiec.db` | ⭐ codziennie | lokalnie + dysk zewnętrzny | **niezastępowalne** |
| `agenci/**/*.md` | przy zmianie | git | zachowanie systemu |
| `dziennik/*.jsonl` | tygodniowo | lokalnie | źródło ewaluacji i śledztw |
| `pomiary/` | przy zmianie | git | bez baz nie ma bramki |
| Modele GGUF | ✗ nie | — | do pobrania; trzymaj tylko sumy |
| `sekrety.json` | ⭐ ręcznie | ⚠️ **poza maszyną, zaszyfrowane** | jedyna rzecz, której nie odtworzysz |

```bash
#!/usr/bin/env bash
# $OSA/kopia.sh — w zadaniu nocnym (część 11)
set -euo pipefail
CEL="${KOPIA_CEL:-$HOME/kopie/osa}"; mkdir -p "$CEL"
D=$(date +%Y%m%d)

sqlite3 $OSA/pamiec/pamiec.db ".backup '$CEL/pamiec-$D.db'"   # ⭐ nie cp!
tar czf "$CEL/dziennik-$D.tgz" -C $OSA dziennik/
tar czf "$CEL/konfig-$D.tgz"  -C $OSA konfiguracja/ agenci/ wydania/

# ⭐ test odtworzenia — kopia niesprawdzona to nie kopia
sqlite3 "$CEL/pamiec-$D.db" "SELECT count(*) FROM fakty" > /dev/null \
  || { echo "✗ KOPIA USZKODZONA"; exit 1; }

find "$CEL" -name 'pamiec-*.db' -mtime +30 -delete
echo "✓ kopia $D ($(du -sh "$CEL" | cut -f1))"
```

⚠️ **`sqlite3 .backup`, nie `cp`.** Kopiowanie pliku SQLite podczas zapisu daje plik
**uszkodzony w sposób, który ujawni się dopiero przy odtwarzaniu** — czyli w najgorszym
możliwym momencie.

---

## 5. Kontrola stanu

```python
# $OSA/wydanie/kontrola.py
KONTROLE = [
    ("brama odpowiada",     lambda: _http("GET", "/zdrowie")["ok"]),
    ("planista żyje",       lambda: _systemd("osa-planista") == "active"),
    ("model odpowiada",     lambda: _model_echo() is not None),
    ("pamięć zapisywalna",  lambda: _test_zapisu_pamieci()),
    ("dziennik zapisywalny",lambda: _test_zapisu_dziennika()),
    ("miejsce na dysku",    lambda: _wolne_gb() > 20),
    ("VRAM dostępny",       lambda: _wolne_vram_gb() > 4),
    ("GRANICE.md 444",      lambda: _prawa_granic() == "444"),        # cz. 6
    ("sekrety 600",         lambda: _prawa_sekretow() == "600"),      # cz. 10
    ("brak sieci w piaskownicy", lambda: not _piaskownica_ma_siec()), # cz. 10
    ("kopia < 48 h",        lambda: _wiek_kopii_h() < 48),
    ("zbiór złoty < 7 dni", lambda: _wiek_ewaluacji_dni() < 7),
]
```

```bash
python3 wydanie/kontrola.py
# ✓ brama odpowiada          ✓ GRANICE.md 444
# ✓ planista żyje            ✓ sekrety 600
# ✓ model odpowiada          ✓ brak sieci w piaskownicy
# ✓ pamięć zapisywalna       ⚠️ kopia sprzed 61 h
# ✓ dziennik zapisywalny     ✓ zbiór złoty sprzed 2 dni
# ✓ miejsce: 412 GB          ✓ VRAM: 58,1 GB
# 11/12 — 1 ostrzeżenie
```

---

## 6. Runbook na trzecią w nocy

⭐ **Pisz go, gdy jesteś wypoczęty i nic się nie pali.** Wtedy, gdy się pali, nie
napiszesz go dobrze.

```markdown
# RUNBOOK · System agentów

## Najpierw, zawsze
    python3 $OSA/wydanie/kontrola.py
Jeśli nie wiesz, co robić — `bash $OSA/STOP.sh`. Nic nie tracisz.

## Agent nie odpowiada
1. `systemctl --user status osa-brama`
2. `tail -50 $OSA/dziennik/brama.log`
3. Model żyje? `curl -s localhost:8080/health`
4. Blokada po martwym procesie? `cat $OSA/brama.lock` → `kill -0 <PID>`
5. `systemctl --user restart osa-brama`

## Agent odpowiada, ale głupio
1. `python3 ewaluacja/uruchom.py --szybki` — jak bardzo źle?
2. `python3 sesja-cli.py metryki --okres 7d` — od kiedy?
3. `git log --oneline -20 -- agenci/ narzedzia/ konfiguracja/` — co się zmieniło?
4. `python3 wydanie/wycofaj.sh <ostatnia dobra>`
5. Dopiero potem szukaj przyczyny. **Najpierw przywróć, potem diagnozuj.**

## Agent robi coś, czego nie powinien
1. ⭐ `bash $OSA/STOP.sh` — NATYCHMIAST
2. `python3 sesja-cli.py sledztwo --ostatnie 10` (część 15)
3. `python3 bezpieczenstwo/dryf.py --agent <x>` (część 16)
4. `python3 testy/ataki/ataki.py --wszystkie`
5. Dopiero po zrozumieniu — wznów

## Maszyna pada / karty w ogniu
1. `rocm-smi` — temperatury, moc
2. `python3 sesja-cli.py flota --aktywne` — ile równoległych sesji
3. Limit: `limit_rownoczesnych` w konfiguracji (część 13 §5.3)
4. Awaryjnie: `systemctl --user stop osa-planista` (zostawia bramę reaktywną)

## Dysk pełny
1. `du -sh $OSA/*` — zwykle `dziennik/`
2. `python3 dziennik/kompaktuj.py --starsze-niz 30d`
3. `find /tmp/praca -mtime +1 -delete`

## Odtworzenie od zera
1. `git clone` + `git checkout v<wersja>`
2. `bash init.sh`
3. `sqlite3 pamiec/pamiec.db ".restore '<kopia>'"`
4. `python3 pamiec/migruj.py --do-biezacej`
5. `python3 wydanie/kontrola.py`
6. `python3 ewaluacja/uruchom.py --wzgledem-manifestu v<wersja>`
```

⚠️ **„Najpierw przywróć, potem diagnozuj" jest kontrintuicyjne dla inżynierów** —
naturalny odruch to zrozumieć przyczynę. O 3:00 to jest zły odruch. Wycofanie zajmuje
5 minut, diagnoza dwie godziny, a dowody zostają w dzienniku i nigdzie nie uciekną.

---

## 7. EKSPERYMENT 18 — zepsuj i wycofaj

⭐ **Ćwiczenie, którego nikt nie robi, dopóki nie musi — i wtedy jest za późno.**

```bash
python3 ewaluacja/uruchom.py --przebiegow 3 --zapisz /tmp/przed.json
bash wydanie/wydaj.sh 1.0.0-test
```

**Wprowadź awarię (wybierz losowo, nie patrząc):**

```
A. usuń jedno narzędzie z rejestru
B. zmień prompt Archiwisty na wersję sprzed trzech miesięcy
C. podmień model na inną kwantyzację
D. zepsuj schemat pamięci (dodaj NOT NULL bez wartości domyślnej)
E. zmień próg kompakcji na 20 %
F. usuń GRANICE.md Badacza
```

| Miara | Twój wynik |
| :-- | --: |
| Czas do **zauważenia** (kontrola/ewaluacja/metryki) | ___ min |
| Czas do **zdiagnozowania** (która zmiana) | ___ min |
| Czas do **wycofania** | ___ min |
| Czy pamięć przetrwała? | tak / nie |
| Czy wynik wrócił do `/tmp/przed.json`? | tak / nie |
| Czy runbook wystarczył, czy improwizowałeś? | |

⚠️ **Predykcja:** A i C zauważysz szybko (kontrola, ewaluacja). B i E są podstępne —
system działa, tylko gorzej. **D jest najgorsze**, bo psuje zapis, a wycofanie kodu
tego nie naprawi bez migracji. **F nie zostanie zauważone przez ewaluację w ogóle** —
złapie je wyłącznie `kontrola.py` i ataki ASI z części 16.

⭐ **Awaria F jest najważniejszą nauką: ewaluacja mierzy jakość, nie bezpieczeństwo.**
Usunięcie granic **poprawi** wynik zbioru złotego, bo agent będzie mógł więcej.
Dlatego `kontrola.py` sprawdza uprawnienia plików, a potok wydania uruchamia ataki
ASI **obok** bramki regresji, nie zamiast niej.

**Po eksperymencie: dopisz do runbooka to, czego w nim zabrakło.** To jest jego jedyny
sposób dojrzewania.

---

## 8. Higiena bieżąca

| Rytm | Co |
| :-- | :-- |
| **Co noc** (część 11) | ewaluacja, audyt pamięci, wykrywanie dryfu, kopia, kompakcja dzienników |
| **Co tydzień** | przegląd metryk (⭐ `sr_krokow`), audyt wyjścia, kolejka niepilnych |
| **Co miesiąc** | 3 nowe pytania do zbioru złotego z realnych awarii; przegląd `SOUL.md` |
| **Co kwartał** | próby ucieczki, rejestr dostaw, audyt `eval`/`exec`, aktualizacja modeli |
| **Co pół roku** | przegląd ADR: które decyzje się nie sprawdziły i **dlaczego** |

⭐ **Wiersz miesięczny jest tym, który utrzymuje system przy życiu.** Trzy pytania
miesięcznie to 36 rocznie — zbiór złoty rośnie razem z Twoim doświadczeniem i
**przestaje mierzyć rzeczy, które dawno umiesz**, a zaczyna mierzyć te, które Cię
boleśnie zaskoczyły.

---

## 9. Pułapki tej części

| ID | Pułapka | Objaw | Jak uniknąć |
| :-- | :-- | :-- | :-- |
| **P136** | **Wydanie z niezacommitowanymi zmianami** | Manifest nie opisuje tego, co działa; wycofanie nie odtwarza zachowania | Krok 1 potoku: `git status --porcelain` musi być pusty |
| **P137** | **Wycofanie kodu bez migracji pamięci wstecz** | Stary kod + nowy schemat = błędy zapisu; dane w niespójnym stanie | Wersja schematu w manifeście; migracje wstecz **dopisujące, nie usuwające** |
| **P138** | **`cp` zamiast `sqlite3 .backup`** | Kopia uszkodzona; dowiadujesz się przy odtwarzaniu | `.backup` + test odczytu **w tym samym skrypcie** |
| **P139** | **Model niewersjonowany sumą kontrolną** | „Ten sam" GGUF po pobraniu zachowuje się inaczej; szukasz błędu w kodzie | `sha256` pliku modelu w manifeście; `sprawdz_modele.py` przy wycofaniu |

---

## 10. Checkpoint

```bash
cd $OSA
bash wydanie/wydaj.sh 1.0.0-test
python3 wydanie/kontrola.py
bash wydanie/wycofaj.sh <poprzednia> && python3 wydanie/kontrola.py --szybka
python3 - <<'EOF'
import json, pathlib
m = json.loads(sorted(pathlib.Path("wydania").glob("*.json"))[-1].read_text())
assert m["czyste_repo"],                              "P136"
assert all("sha256" in v for v in m["skladniki"]["modele"].values()), "P139"
assert "ewaluacja" in m and m["ewaluacja"]["ogolem"] > 0, "brak wyniku ewaluacji"
print("✓ manifest kompletny")
EOF
bash kopia.sh && echo "✓ kopia z testem odtworzenia"
test -s RUNBOOK.md && echo "✓ runbook"
git add -A && git commit -m "część 18: wydanie, wycofanie, kopie, runbook"
```

- [ ] Wydanie obejmuje **siedem** składników, nie tylko kod
- [ ] Prompt to pełnoprawne wydanie
- [ ] Manifest zawiera `sha256` **modeli**
- [ ] Potok wydania ma bramkę regresji **i** ataki ASI
- [ ] Wycofanie poniżej 5 minut, z kopią stanu przed
- [ ] Schemat pamięci zmienia się **tylko przez dopisanie**
- [ ] Kopie przez `.backup`, z testem odczytu
- [ ] `kontrola.py` sprawdza też **uprawnienia plików**
- [ ] Runbook napisany **przed** awarią, poprawiony **po** eksperymencie
- [ ] ⭐ **Zepsułeś system celowo i wycofałeś — znasz swoje czasy**

---

**Dalej: `19-CAPSTONE.md`** — składasz wszystko w jednego osobistego asystenta
i mierzysz, jak daleko zaszedłeś od części 1.
