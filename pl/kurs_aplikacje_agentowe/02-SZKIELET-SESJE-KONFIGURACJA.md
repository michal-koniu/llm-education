# Część 2 · Szkielet — proces, konfiguracja, sesje

**Poziom:** ⭐⭐⭐ · **Czas:** ~5 h · **Wymaga:** części 1
**Produkuje:** działającą bramę, konfigurację jako dane, dziennik zdarzeń z odtwarzaniem

---

## 0. Po co w ogóle brama

Twoja pętla z kursu 1 to skrypt. Uruchamiasz, rozmawiasz, zamykasz — stan znika.
Trzech agentów działających tygodniami wymaga czegoś innego: **procesu, który żyje
dłużej niż rozmowa**.

Brama daje cztery rzeczy, których skrypt dać nie może:

| Co daje | Dlaczego bez tego nie da się |
| :-- | :-- |
| **Jedno miejsce na stan** | Dwa procesy piszące do tej samej pamięci to wyścig. Jeden proces = brak wyścigu |
| **Jedno miejsce na politykę** | Kontrola dostępu rozsiana po narzędziach **zawsze** ma dziurę. Scentralizowana — nie ma gdzie jej zapomnieć |
| **Jedno miejsce na obserwację** | Ślad rozproszony po skryptach jest bezużyteczny (część 15) |
| **Punkt zaczepienia dla harmonogramu** | Coś musi żyć, żeby obudzić agenta o 7:00 (część 11) |

> ⭐ **Reguła, którą OpenClaw wymusza i którą kradnę: dokładnie jedna brama na hosta.**
> Nie dlatego, że tak ładniej. Dlatego, że przy dwóch instancjach **dwie kopie
> harmonogramu wykonają to samo zadanie dwa razy**, a dwa procesy dopisujące do jednego
> dziennika produkują plik, którego nie da się odtworzyć. Egzekwujesz to plikiem blokady
> — w §4.

---

## 1. Konfiguracja jako dane, nie jako kod

Najczęstszy błąd w projektach, które widziałem: konfiguracja rozsiana po stałych
w Pythonie. Działa do momentu, w którym chcesz **zmienić zachowanie bez restartu**,
**pokazać komuś, co jest ustawione**, albo **cofnąć zmianę**.

### 1.1 · Trzy zasady

1. **Konfiguracja to jeden plik danych**, nie moduł Pythona. Da się go zwalidować,
   zdiffować i wersjonować.
2. **Każda wartość ma sensowny domyślnik.** Pusty plik konfiguracji musi dać działający
   system. (To jest reguła Steinbergera z MCP Best Practices i jest bardzo dobra.)
3. **Sekrety nie są w konfiguracji.** Osobna warstwa, inne uprawnienia pliku (część 10).

### 1.2 · OD ZERA

```bash
cat > $OSA/konfiguracja/system.json <<'EOF'
{
  "brama": {
    "host": "127.0.0.1",
    "port": 18789,
    "plik_blokady": "$OSA/brama.lock"
  },
  "modele": {
    "domyslny":  { "url": "http://127.0.0.1:8080/v1", "nazwa": "gpt-oss-20b" },
    "trudny":    { "url": "http://127.0.0.1:8080/v1", "nazwa": "qwen3-32b" },
    "limit_tokenow_wyjscia": 2048,
    "limit_sekund": 300
  },
  "sesje": {
    "katalog": "$OSA/dziennik",
    "max_zdarzen_na_plik": 50000
  },
  "zaufanie": {
    "konsola":  "host",
    "http":     "piaskownica",
    "kanal_dm": "piaskownica",
    "cron":     "host"
  }
}
EOF
```

⚠️ **Zwróć uwagę na sekcję `zaufanie`.** Wygląda niewinnie, a jest **najważniejszą
częścią pliku**. To jest mapa „skąd przyszło żądanie" → „ile mu wolno". Zaimplementujesz
ją w §5, wyegzekwujesz w części 10.

Teraz wczytywanie — z domyślnikami i rozwijaniem `~`:

```python
# $OSA/konfig.py
"""Konfiguracja jako dane. Pusty plik = działający system."""
import json, os, pathlib

DOMYSLNE = {
    "brama":   {"host": "127.0.0.1", "port": 18789,
                "plik_blokady": "$OSA/brama.lock"},
    "modele":  {"domyslny": {"url": "http://127.0.0.1:8080/v1", "nazwa": "lokalny"},
                "limit_tokenow_wyjscia": 2048, "limit_sekund": 300},
    "sesje":   {"katalog": "$OSA/dziennik", "max_zdarzen_na_plik": 50000},
    "zaufanie": {"konsola": "host"},
}

def _scal(baza: dict, nowe: dict) -> dict:
    """Scalanie głębokie — nowe nadpisuje, ale nie kasuje gałęzi."""
    wynik = dict(baza)
    for k, v in nowe.items():
        if isinstance(v, dict) and isinstance(wynik.get(k), dict):
            wynik[k] = _scal(wynik[k], v)
        else:
            wynik[k] = v
    return wynik

def _rozwin(obiekt):
    """Rozwija ~ w każdym stringu wyglądającym na ścieżkę."""
    if isinstance(obiekt, dict):
        return {k: _rozwin(v) for k, v in obiekt.items()}
    if isinstance(obiekt, list):
        return [_rozwin(v) for v in obiekt]
    if isinstance(obiekt, str) and obiekt.startswith("~"):
        return os.path.expanduser(os.path.expandvars(obiekt))
    return obiekt

def wczytaj(sciezka: str = "$OSA/konfiguracja/system.json") -> dict:
    p = pathlib.Path(os.path.expanduser(os.path.expandvars(sciezka)))
    z_pliku = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return _rozwin(_scal(DOMYSLNE, z_pliku))

if __name__ == "__main__":
    print(json.dumps(wczytaj(), indent=2, ensure_ascii=False))
```

```bash
python3 $OSA/konfig.py          # oczekuj pełnej konfiguracji ze ścieżkami rozwiniętymi
mv $OSA/konfiguracja/system.json /tmp/ && python3 $OSA/konfig.py
# ↑ nadal działa — zasada 2. Przywróć plik.
mv /tmp/system.json $OSA/konfiguracja/
```

---

## 2. Sesja jako dziennik zdarzeń

To jest **najważniejsza decyzja projektowa w tej części** i warto ją zrozumieć zanim
napiszesz kod.

### 2.1 · Dlaczego nie „lista wiadomości"

Naiwne podejście: sesja to lista wiadomości, trzymasz ją w pamięci, zapisujesz JSON na
koniec. Pęka natychmiast:

| Problem | Dlaczego dziennik zdarzeń go nie ma |
| :-- | :-- |
| Proces padł w połowie — tracisz całą sesję | Każde zdarzenie zapisane od razu, tracisz najwyżej ostatnie |
| Nie wiesz, **kiedy** coś się stało | Każde zdarzenie ma znacznik czasu |
| Nie wiesz, **ile** kosztowała tura | Zdarzenie modelu niesie liczbę tokenów |
| Kompakcja bezpowrotnie niszczy historię | Kompakcja to **też zdarzenie** — oryginał zostaje |
| Nie da się „cofnąć o trzy tury i spróbować inaczej" | Gałąź to wskaźnik na zdarzenie |

⭐ **Kluczowa różnica:** lista wiadomości to **stan**. Dziennik zdarzeń to **historia,
z której stan się wylicza**. Stan da się odtworzyć zawsze; historii z samego stanu
odtworzyć się nie da.

### 2.2 · Format

Jedno zdarzenie = jedna linia JSON (JSONL). Plik na sesję.

```json
{"seq":1,"ts":"2026-09-23T07:00:01.220Z","typ":"sesja.start","zaufanie":"host","zrodlo":"konsola"}
{"seq":2,"ts":"2026-09-23T07:00:01.221Z","typ":"wiadomosc","rola":"user","tresc":"ile mam plików w ~/dokumenty"}
{"seq":3,"ts":"2026-09-23T07:00:03.880Z","typ":"model.odpowiedz","tresc":"Sprawdzę.","tokeny_we":412,"tokeny_wy":18,"ms":2659}
{"seq":4,"ts":"2026-09-23T07:00:03.881Z","typ":"narzedzie.wywolanie","narzedzie":"powloka","argumenty":{"cmd":"ls ~/dokumenty | wc -l"},"id":"w1"}
{"seq":5,"ts":"2026-09-23T07:00:04.010Z","typ":"narzedzie.wynik","id":"w1","kod":0,"tresc":"42"}
{"seq":6,"ts":"2026-09-23T07:00:05.900Z","typ":"model.odpowiedz","tresc":"Masz 42 pliki.","tokeny_we":448,"tokeny_wy":9,"ms":1889}
```

**Osiem typów zdarzeń wystarcza na cały kurs:**

| Typ | Kiedy | Niesie |
| :-- | :-- | :-- |
| `sesja.start` | otwarcie sesji | poziom zaufania, źródło |
| `wiadomosc` | wejście od człowieka lub kanału | rola, treść |
| `model.odpowiedz` | model coś powiedział | treść, tokeny, czas |
| `narzedzie.wywolanie` | model chce działać | nazwa, argumenty, `id` |
| `narzedzie.wynik` | narzędzie odpowiedziało | `id`, kod wyjścia, treść |
| `blad` | cokolwiek poszło źle | gdzie, co |
| `kompakcja` | historia została streszczona | zakres `seq`, streszczenie |
| `galaz` | odbicie od wcześniejszego punktu | `seq` rodzica |

> 💡 **Dlaczego `seq` obok `ts`.** Znaczniki czasu potrafią się powtórzyć w tej samej
> milisekundzie i **nie są monotoniczne** przy zmianie czasu systemowego. `seq` jest
> monotoniczny z definicji i to on wyznacza porządek. `ts` jest do czytania przez
> człowieka i do metryk. **Nigdy nie sortuj po `ts`.**

### 2.3 · OD ZERA — magazyn sesji

```python
# $OSA/sesje.py
"""Sesja jako dziennik zdarzeń dopisywany na końcu. Stan = fold(zdarzenia)."""
import json, os, pathlib, datetime, threading

TERAZ = lambda: datetime.datetime.now(datetime.UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")

class Dziennik:
    def __init__(self, katalog: str, sesja: str):
        self.sesja = sesja
        self.plik = pathlib.Path(katalog) / f"{sesja.replace(':', '~')}.jsonl"
        self.plik.parent.mkdir(parents=True, exist_ok=True)
        self._blokada = threading.Lock()
        self._seq = self._ostatni_seq()

    def _ostatni_seq(self) -> int:
        if not self.plik.exists():
            return 0
        ostatnia = 0
        with self.plik.open(encoding="utf-8") as f:
            for linia in f:
                if linia.strip():
                    ostatnia = json.loads(linia)["seq"]
        return ostatnia

    def dopisz(self, typ: str, **pola) -> dict:
        """Jedyny sposób zmiany stanu sesji. Zapis natychmiastowy."""
        with self._blokada:
            self._seq += 1
            z = {"seq": self._seq, "ts": TERAZ(), "typ": typ, **pola}
            with self.plik.open("a", encoding="utf-8") as f:
                f.write(json.dumps(z, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())          # ← P64
            return z

    def zdarzenia(self, do_seq: int | None = None):
        if not self.plik.exists():
            return
        with self.plik.open(encoding="utf-8") as f:
            for linia in f:
                if not linia.strip():
                    continue
                z = json.loads(linia)
                if do_seq is not None and z["seq"] > do_seq:
                    return
                yield z
```

**`os.fsync` w linii zapisu jest celowy** — bez niego zdarzenie siedzi w buforze systemu
i **ginie przy zaniku zasilania**. Kosztuje ~0,1 ms na zdarzenie. Przy agencie robiącym
20 zdarzeń na turę to 2 ms. Płacisz je i nie dyskutujesz (pułapka P64).

### 2.4 · Odtwarzanie — stan wyliczany z historii

```python
# $OSA/sesje.py (ciąg dalszy)

def odtworz(dziennik: Dziennik, do_seq: int | None = None) -> dict:
    """Składa stan sesji ze zdarzeń. To jest JEDYNE miejsce, gdzie powstaje stan."""
    stan = {"sesja": dziennik.sesja, "zaufanie": None, "zrodlo": None,
            "historia": [], "tokeny_we": 0, "tokeny_wy": 0, "bledy": 0,
            "kompakcje": [], "ostatni_seq": 0}

    for z in dziennik.zdarzenia(do_seq):
        stan["ostatni_seq"] = z["seq"]
        t = z["typ"]

        if t == "sesja.start":
            stan["zaufanie"], stan["zrodlo"] = z["zaufanie"], z["zrodlo"]

        elif t == "wiadomosc":
            stan["historia"].append({"rola": z["rola"], "tresc": z["tresc"]})

        elif t == "model.odpowiedz":
            stan["historia"].append({"rola": "assistant", "tresc": z["tresc"]})
            stan["tokeny_we"] += z.get("tokeny_we", 0)
            stan["tokeny_wy"] += z.get("tokeny_wy", 0)

        elif t == "narzedzie.wywolanie":
            stan["historia"].append({"rola": "assistant", "narzedzie": z["narzedzie"],
                                     "argumenty": z["argumenty"], "id": z["id"]})

        elif t == "narzedzie.wynik":
            stan["historia"].append({"rola": "tool", "id": z["id"], "tresc": z["tresc"]})

        elif t == "blad":
            stan["bledy"] += 1

        elif t == "kompakcja":
            # Historia znika z KONTEKSTU, ale ZOSTAJE w pliku.
            ogon = stan["historia"][z["zachowaj_ostatnie"]:] if z.get("zachowaj_ostatnie") else []
            stan["historia"] = [{"rola": "system", "tresc": z["streszczenie"]}] + ogon
            stan["kompakcje"].append({"seq": z["seq"], "od": z["od_seq"], "do": z["do_seq"]})

    return stan
```

⭐ **Przeczytaj gałąź `kompakcja` jeszcze raz.** Kompakcja **nie kasuje niczego z pliku**
— zmienia tylko to, co trafia do kontekstu modelu. Oryginał zostaje na dysku na zawsze.
Dlatego w części 15 będziesz umiał odpowiedzieć na pytanie „co agent widział w turze 40",
nawet jeśli w turze 60 dawno to skompaktował.

### 2.5 · Gałęzie — „cofnij o trzy tury i spróbuj inaczej"

```python
def odgalez(zrodlo: Dziennik, od_seq: int, nowa_nazwa: str) -> Dziennik:
    """Nowa sesja startująca ze stanu sesji źródłowej na zdarzeniu od_seq."""
    nowa = Dziennik(str(zrodlo.plik.parent), nowa_nazwa)
    nowa.dopisz("galaz", rodzic=zrodlo.sesja, rodzic_seq=od_seq)
    for z in zrodlo.zdarzenia(do_seq=od_seq):
        if z["typ"] != "sesja.start":
            nowa.dopisz(z["typ"], **{k: v for k, v in z.items()
                                     if k not in ("seq", "ts", "typ")})
    return nowa
```

**Po co Ci to.** W części 14 budujesz ewaluację. Bez gałęzi jedyny sposób na
porównanie dwóch wariantów to uruchomienie zadania od zera. Z gałęziami **odbijasz się
od tury 12 i sprawdzasz dwa różne prompty na identycznym stanie początkowym.** To jest
różnica między eksperymentem a zgadywaniem.

---

## 3. PRODUKCYJNIE — JSONL czy SQLite

Napisałeś JSONL. Kiedy to przestaje wystarczać?

| Kryterium | JSONL (Twoje) | SQLite WAL |
| :-- | :-- | :-- |
| Dopisanie zdarzenia | ~0,1 ms + fsync | ~0,05 ms |
| Odczyt całej sesji | liniowy, szybki do ~50 tys. | liniowy, szybszy |
| **Zapytanie „wszystkie błędy z ostatniego tygodnia"** | ⚠️ skan wszystkich plików | ⭐ indeks, milisekundy |
| Wielu pisarzy | ⚠️ wymaga blokady zewnętrznej | ⭐ wbudowane |
| Czytelność `cat`-em | ⭐ pełna | ✗ żadna |
| `grep` po dzienniku | ⭐ działa | ✗ nie działa |
| Kopia zapasowa | `cp` | `.backup` |
| Uszkodzenie pliku | tracisz **jedną linię** | ryzyko całego pliku |

**Rekomendacja: zostań przy JSONL do części 15, potem dołóż SQLite jako indeks obok,
nie zamiast.** Dziennik zostaje źródłem prawdy (czytelnym, `grep`-owalnym,
odpornym na uszkodzenia), SQLite jest **pochodną, którą da się odbudować** z dziennika
jednym przebiegiem. To jest ten sam wzorzec co „log + materialized view" w bazach.

> ⚠️ **Pułapka, w którą wpadniesz, jeśli zrobisz odwrotnie.** Gdy SQLite jest źródłem
> prawdy, jedna uszkodzona strona pliku kosztuje Cię całą historię agenta. Gdy jest
> indeksem — kasujesz go i odbudowujesz w 10 sekund.

---

## 4. Brama — jeden proces, pętla zwrotna, blokada

```python
# $OSA/brama.py
"""Brama: jedyne źródło prawdy o sesjach. Jedna na hosta."""
import json, os, sys, pathlib, http.server, socketserver
from konfig import wczytaj
from sesje import Dziennik, odtworz

K = wczytaj()

class JednaInstancja:
    """Plik blokady z PID. Wykrywa też blokadę po martwym procesie."""
    def __init__(self, sciezka): self.p = pathlib.Path(sciezka)
    def __enter__(self):
        if self.p.exists():
            pid = int(self.p.read_text().strip() or 0)
            try:
                os.kill(pid, 0)                       # żyje?
                sys.exit(f"BŁĄD: brama już działa (PID {pid}). Jedna na hosta.")
            except ProcessLookupError:
                print(f"UWAGA: usuwam blokadę po martwym PID {pid}")
        self.p.write_text(str(os.getpid()))
        return self
    def __exit__(self, *a): self.p.unlink(missing_ok=True)

def poziom_zaufania(zrodlo: str) -> str:
    return K["zaufanie"].get(zrodlo, "piaskownica")   # ← P66: domyślnie WĘŻEJ

class Obsluga(http.server.BaseHTTPRequestHandler):
    def _odpowiedz(self, kod, dane):
        tresc = json.dumps(dane, ensure_ascii=False).encode()
        self.send_response(kod)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(tresc)))
        self.end_headers()
        self.wfile.write(tresc)

    def do_POST(self):
        if self.path != "/wiadomosc":
            return self._odpowiedz(404, {"blad": "nieznana ścieżka"})
        n = int(self.headers.get("Content-Length", 0))
        zadanie = json.loads(self.rfile.read(n) or b"{}")

        sesja  = zadanie.get("sesja", "main")
        zrodlo = zadanie.get("zrodlo", "http")
        tresc  = zadanie.get("tresc", "")

        d = Dziennik(K["sesje"]["katalog"], sesja)
        if d._seq == 0:
            d.dopisz("sesja.start", zaufanie=poziom_zaufania(zrodlo), zrodlo=zrodlo)
        z = d.dopisz("wiadomosc", rola="user", tresc=tresc)

        stan = odtworz(d)
        self._odpowiedz(200, {"sesja": sesja, "seq": z["seq"],
                              "zaufanie": stan["zaufanie"],
                              "tur": len(stan["historia"])})

    def do_GET(self):
        if self.path.startswith("/sesja/"):
            d = Dziennik(K["sesje"]["katalog"], self.path.split("/", 2)[2])
            return self._odpowiedz(200, odtworz(d))
        self._odpowiedz(404, {"blad": "nieznana ścieżka"})

    def log_message(self, *a): pass       # ← P63: cisza na stdout

if __name__ == "__main__":
    with JednaInstancja(K["brama"]["plik_blokady"]):
        adres = (K["brama"]["host"], K["brama"]["port"])
        print(f"brama: http://{adres[0]}:{adres[1]}  (tylko pętla zwrotna)")
        socketserver.ThreadingTCPServer.allow_reuse_address = True
        with socketserver.ThreadingTCPServer(adres, Obsluga) as s:
            s.serve_forever()
```

**Uruchom i sprawdź:**

```bash
cd $OSA && python3 brama.py &
sleep 1

curl -s -X POST localhost:18789/wiadomosc \
  -H 'Content-Type: application/json' \
  -d '{"sesja":"test","zrodlo":"konsola","tresc":"cześć"}' | python3 -m json.tool
# oczekuj: {"sesja":"test","seq":2,"zaufanie":"host","tur":1}

curl -s -X POST localhost:18789/wiadomosc \
  -d '{"sesja":"test","zrodlo":"http","tresc":"druga"}' | python3 -m json.tool
# oczekuj: zaufanie NADAL "host" — sesja już istnieje, poziom ustalony przy starcie

cat $OSA/dziennik/test.jsonl
python3 brama.py        # ← oczekuj: BŁĄD: brama już działa
```

⭐ **Zauważ ostatni test.** Poziom zaufania jest **ustalany raz, przy otwarciu sesji**,
i nie zmienia się nawet gdy kolejna wiadomość przyjdzie z bardziej zaufanego źródła.
To nie jest niedoróbka — to jest **zabezpieczenie przed eskalacją przez podmianę
źródła**. Sesja otwarta z sieci zostaje sesją z sieci na zawsze.

---

## 5. EKSPERYMENT 2 — wierność odtwarzania

**Hipoteza:** stan odtworzony z dziennika jest identyczny ze stanem procesu, który
go zapisał — dla dowolnego punktu w historii.

**Procedura:**

```bash
cat > $OSA/testy/test_odtwarzanie.py <<'EOF'
import sys, json, random, hashlib
sys.path.insert(0, "/home/$USER/os-agenta")
from sesje import Dziennik, odtworz, odgalez

KAT = "/tmp/test-dziennik"
import shutil, pathlib; shutil.rmtree(KAT, ignore_errors=True)

d = Dziennik(KAT, "eksperyment")
d.dopisz("sesja.start", zaufanie="host", zrodlo="konsola")

# 200 tur syntetycznych
for i in range(200):
    d.dopisz("wiadomosc", rola="user", tresc=f"pytanie {i}")
    d.dopisz("model.odpowiedz", tresc=f"odpowiedź {i}", tokeny_we=100+i, tokeny_wy=20, ms=900)
    if i % 7 == 0:
        d.dopisz("narzedzie.wywolanie", narzedzie="powloka",
                 argumenty={"cmd": f"echo {i}"}, id=f"w{i}")
        d.dopisz("narzedzie.wynik", id=f"w{i}", kod=0, tresc=str(i))

pelny = odtworz(d)
print(f"zdarzeń: {pelny['ostatni_seq']}  tur: {len(pelny['historia'])}  "
      f"tokeny we: {pelny['tokeny_we']}")

# 1. Odtworzenie dwa razy daje ten sam wynik?
h = lambda s: hashlib.sha256(json.dumps(s, sort_keys=True).encode()).hexdigest()[:16]
assert h(odtworz(d)) == h(odtworz(Dziennik(KAT, "eksperyment"))), "NIEDETERMINISTYCZNE"
print("✓ odtwarzanie deterministyczne")

# 2. Odtworzenie do punktu N == stan po N zdarzeniach?
for punkt in random.sample(range(2, pelny["ostatni_seq"]), 20):
    czesc = odtworz(d, do_seq=punkt)
    assert czesc["ostatni_seq"] == punkt
    assert len(czesc["historia"]) <= len(pelny["historia"])
print("✓ odtwarzanie częściowe zgodne dla 20 losowych punktów")

# 3. Gałąź od tury 50 dzieli prefiks z oryginałem?
g = odgalez(d, 100, "eksperyment-galaz")
assert odtworz(g)["tokeny_we"] == odtworz(d, do_seq=100)["tokeny_we"]
print("✓ gałąź zachowuje stan rodzica")
EOF

sed -i "s|/home/\$USER|$HOME|" $OSA/testy/test_odtwarzanie.py
python3 $OSA/testy/test_odtwarzanie.py
```

**Zmierz też koszt:**

| Pomiar | Polecenie | Twój wynik |
| :-- | :-- | :-- |
| Czas dopisania 1000 zdarzeń | `time python3 -c "..."` | ___ ms |
| To samo **bez** `os.fsync` | zakomentuj linię | ___ ms |
| Rozmiar dziennika po 200 turach | `du -h ~/…/eksperyment.jsonl` | ___ KB |
| Czas odtworzenia 200 tur | `time` w teście | ___ ms |

⚠️ **Predykcja do sprawdzenia:** `fsync` powinien kosztować ~10–30× więcej niż zapis bez
niego, ale w liczbach bezwzględnych **nadal poniżej 1 ms na zdarzenie na NVMe**. Jeśli
u Ciebie wyjdzie więcej niż 5 ms — sprawdź, czy dziennik nie leży przypadkiem na dysku
sieciowym.

---

## 6. ĆWICZENIE — `sesje` jako narzędzie wiersza poleceń

Napisz `$OSA/sesja-cli.py` z czterema poleceniami. Będziesz ich używał **do końca
kursu**, więc zrób to porządnie:

```bash
python3 sesja-cli.py lista                    # sesje, liczba tur, ostatnia aktywność
python3 sesja-cli.py pokaz main               # historia czytelna dla człowieka
python3 sesja-cli.py pokaz main --do-seq 40   # stan w turze 40
python3 sesja-cli.py koszt main               # tokeny we/wy, błędy, kompakcje
python3 sesja-cli.py odgalez main 40 proba-b  # gałąź do eksperymentu
```

**Wymagania, które nie są opcjonalne:**

1. `pokaz` bez `--do-seq` pokazuje stan aktualny; z `--do-seq` stan historyczny.
2. `koszt` liczy tokeny **z dziennika**, nie szacuje.
3. Żadne polecenie nie modyfikuje dziennika poza `odgalez`.
4. Zero wyjścia na `stdout` poza wynikiem — błędy na `stderr` (P63).

> 💡 **Dlaczego każę Ci to napisać teraz, a nie w części 15.** Bo od tej chwili każdy
> błąd, który zobaczysz w kursie, będziesz diagnozował tym narzędziem. Jeśli powstanie
> późno, przez dziesięć części będziesz debugował `cat`-em i `grep`-em.

---

## 7. Pułapki tej części

| ID | Pułapka | Objaw | Jak uniknąć |
| :-- | :-- | :-- | :-- |
| **P63** | **Wypisywanie na `stdout` w procesie bramy** | Kanał się rozjeżdża, klient dostaje śmieci wmieszane w JSON; przy MCP — natychmiastowa awaria | Dziennikowanie **tylko do pliku albo `stderr`**. `log_message` nadpisany pustką |
| **P64** | **Zapis bez `fsync`** | Po zaniku zasilania ostatnie 2–3 tury znikają, a stan sesji jest niespójny z tym, co agent zrobił naprawdę | `f.flush()` + `os.fsync()`. Koszt <1 ms |
| **P65** | **Sortowanie zdarzeń po `ts` zamiast po `seq`** | Zdarzenia z tej samej milisekundy zamieniają się kolejnością; po zmianie czasu systemowego historia się „cofa" | `seq` jest porządkiem. `ts` jest do czytania |
| **P66** | **Domyślny poziom zaufania = szerszy** | Nowy kanał, o którym zapomniałeś w konfiguracji, dostaje uprawnienia hosta | `K["zaufanie"].get(zrodlo, "piaskownica")` — **brak wpisu znaczy najwęziej**, nie najszerzej |

---

## 8. Checkpoint

```bash
cd $OSA
python3 konfig.py > /dev/null            && echo "✓ konfiguracja"
python3 testy/test_odtwarzanie.py        && echo "✓ odtwarzanie"
pgrep -f brama.py > /dev/null            && echo "✓ brama żyje"
python3 sesja-cli.py lista               && echo "✓ cli"
git add -A && git commit -m "część 2: brama, konfiguracja, dziennik zdarzeń"
```

- [ ] Brama działa, tylko na `127.0.0.1`, jedna instancja wymuszona blokadą
- [ ] Konfiguracja jest danymi; pusty plik daje działający system
- [ ] Sesja jest dziennikiem zdarzeń; **stan jest wyliczany, nie przechowywany**
- [ ] Umiesz odtworzyć stan z dowolnej tury
- [ ] Umiesz odgałęzić sesję i porównać dwa warianty
- [ ] Poziom zaufania ustala się **przy otwarciu sesji** i nie eskaluje
- [ ] Masz `sesja-cli.py` i będziesz go używał do końca kursu

---

**Dalej: `03-HARNESS-DLUGIE-ZADANIA.md`** — najważniejsza część kursu. Pętla, która
przeżywa pięć okien kontekstu i wie, co robiła wczoraj.
