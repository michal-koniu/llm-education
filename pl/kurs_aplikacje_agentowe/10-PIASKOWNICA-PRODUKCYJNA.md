# Część 10 · Piaskownica produkcyjna

**Poziom:** ⭐⭐⭐⭐ · **Czas:** ~5 h · **Wymaga:** kursu 1 cz. 7 (`bwrap`), części 2 (zaufanie sesji), 8 (code-mode)
**Produkuje:** trzy poziomy izolacji wpięte w bramę, kontrolę wyjścia sieciowego, warstwę sekretów, zestaw prób ucieczki

---

## 0. Pytanie, na które ta część odpowiada

**Nie** „jak uruchomić kod w izolacji" — to umiesz z kursu 1.

Tylko: **„przed czym dokładnie chroni każdy szczebel izolacji i ile kosztuje?"** Bo
odpowiedź „użyj kontenera" jest w 2026 niewystarczająca, a przy agencie piszącym własny
kod — po prostu nieprawdziwa.

> **Twój kontener nie jest piaskownicą.** Standardowe kontenery wielodzierżawne nie
> utrzymają agenta wykonującego dowolny kod. Gdy agent może pisać własne skrypty,
> instalować pakiety i manipulować deskryptorami plików, **współdzielone jądro staje
> się zobowiązaniem**.
> — [emirb, *Your Container Is Not a Sandbox*](https://emirb.github.io/blog/microvm-2026/)

---

## 1. Drabina izolacji

```
  KOSZT                                          CO ZATRZYMUJE
    │
    │  ┌─ 5 · maszyna wirtualna ───────────┐    wszystko poza błędem hiperwizora
    │  │    pełna VM, osobne jądro         │    start: 10–30 s   RAM: 1 GB+
    │  ├─ 4 · microVM (Firecracker/libkrun)┤    ⭐ osobne jądro, mała powierzchnia
    │  │                                    │    start: <1 s      RAM: 128 MB+
    │  ├─ 3 · gVisor ─────────────────────┤    jądro w przestrzeni użytkownika
    │  │                                    │    start: ~ms       narzut I/O 10–40 %
    │  ├─ 2 · kontener rootless (podman) ──┤    namespace + seccomp, JĄDRO WSPÓLNE
    │  │                                    │    start: ~200 ms
    │  ├─ 1 · bwrap + seccomp + cgroups ───┤    namespace, JĄDRO WSPÓLNE
    │  │                                    │    start: ~10 ms    ⭐ masz to
    │  └─ 0 · brak ─────────────────────────┘    nic
    ▼
```

### 1.1 · Co naprawdę zatrzymuje każdy szczebel

| Zagrożenie | 1 `bwrap` | 2 rootless | 3 gVisor | 4 microVM |
| :-- | :-: | :-: | :-: | :-: |
| Odczyt Twoich plików | ⭐ tak | ⭐ tak | ⭐ tak | ⭐ tak |
| Zapis poza obszarem roboczym | ⭐ tak | ⭐ tak | ⭐ tak | ⭐ tak |
| Wyjście do sieci | ⭐ tak (`--unshare-net`) | ⭐ tak | ⭐ tak | ⭐ tak |
| Wyczerpanie CPU/RAM | z cgroups | ⭐ tak | ⭐ tak | ⭐ tak |
| Podglądanie innych procesów | ⭐ tak | ⭐ tak | ⭐ tak | ⭐ tak |
| **Exploit jądra Linuksa** | ✗ **nie** | ✗ **nie** | ⭐ tak | ⭐ tak |
| Ucieczka przez `/proc`, `/sys` | częściowo | częściowo | ⭐ tak | ⭐ tak |
| Kanały boczne (czas, cache) | ✗ | ✗ | częściowo | częściowo |

⭐ **Cały wiersz „exploit jądra" jest powodem istnienia szczebli 3 i 4.** Przy szczeblach
1 i 2 kod agenta rozmawia z **tym samym jądrem**, co reszta Twojego systemu. Jedna luka
w wywołaniu systemowym = ucieczka. gVisor to eliminuje, bo proces w piaskownicy
**nigdy nie rozmawia z prawdziwym jądrem** — rozmawia z jego reimplementacją
w przestrzeni użytkownika.

### 1.2 · Który szczebel dla którego agenta

| Agent | Co przetwarza | Szczebel | Uzasadnienie |
| :-- | :-- | :-: | :-- |
| **Archiwista** | Twoje pliki | **1** `bwrap` | wejście zaufane; chronisz przed pomyłką, nie przed atakiem |
| **Gospodarz** | kalendarz, lokalna sieć | **1–2** | wejście półzaufane |
| **Badacz** | ⚠️ **treść z internetu** | **3–4** | wejście wrogie z definicji |
| **code-mode** (część 8) | kod pisany przez model | **2–4** | ⭐ zależy, skąd przyszło zadanie |

⭐ **Reguła: poziom izolacji wynika ze źródła WEJŚCIA, nie z nazwy agenta.** Archiwista
proszony o przetworzenie pliku, który przyszedł mailem, jest w tej turze tak samo
niezaufany jak Badacz. To jest dokładnie ta rzecz, którą zaimplementowałeś w części 2
jako poziom zaufania sesji — teraz ją wyegzekwujesz.

---

## 2. Szczebel 1 — `bwrap` porządnie

Kurs 1 dał podstawy. Tu jest wersja produkcyjna z limitami zasobów.

```bash
# $OSA/piaskownica/szczebel1.sh
#!/usr/bin/env bash
set -euo pipefail

OBSZAR="${1:?katalog roboczy}"; shift
ARCHIWUM="${ARCHIWUM:-}"

ARGS=(
  --unshare-all                      # ⭐ wszystkie namespace: net, pid, ipc, uts, cgroup
  --die-with-parent                  # zabity razem z bramą
  --new-session                      # P44: bez wstrzykiwania do terminala przez TIOCSTI
  --clearenv                         # ⭐ P101: żadnych sekretów przez środowisko
  --setenv PATH /usr/bin:/bin
  --setenv HOME "$OBSZAR"
  --setenv LANG pl_PL.UTF-8
  --ro-bind /usr /usr
  --ro-bind /bin /bin
  --ro-bind /lib /lib
  --symlink usr/lib64 /lib64
  --ro-bind /etc/ssl /etc/ssl
  --proc /proc
  --dev /dev
  --tmpfs /tmp
  --bind "$OBSZAR" "$OBSZAR"         # jedyny zapis
  --chdir "$OBSZAR"
)
[ -n "$ARCHIWUM" ] && ARGS+=(--ro-bind "$ARCHIWUM" /archiwum)

# Limity zasobów — bwrap ich NIE MA, dokłada je systemd
exec systemd-run --user --scope --quiet \
  -p MemoryMax=1G -p CPUQuota=200% -p TasksMax=64 \
  -- sudo bwrap "${ARGS[@]}" -- "$@"
```

⚠️ **`sudo` przed `bwrap` jest tu konieczny na tej maszynie, nie ozdobny.** Ubuntu
24.04 ogranicza tworzenie namespace'ów użytkownika przez procesy nieuprzywilejowane
(`kernel.apparmor_restrict_unprivileged_userns=1`), a pakiet `bubblewrap` w tym
wydaniu **nie ma własnego profilu AppArmor**, który normalnie by to omijał —
sprawdzone na żywo (pełna diagnoza i dowód z dziennika jądra: kurs 1,
`07-SANDBOX-BEZPIECZENSTWO-MONITORING.md`, §2). Bez `sudo`, każde wywołanie z
`--unshare-net` lub `--unshare-all` kończy się:

```
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
```

`sudo` w środku `systemd-run --user --scope` **działa** — sprawdzone na żywo — i **nie
wyłącza** żadnej ochrony systemową: `bwrap` tworzy namespace z realnych uprawnień
roota, więc restrykcja dotycząca *nie*uprzywilejowanych namespace'ów po prostu go
nie dotyczy. Izolacja wewnątrz piaskownicy jest identyczna.

**Cztery flagi warte uzasadnienia:**

| Flaga | Bez niej |
| :-- | :-- |
| `--unshare-all` | kod widzi Twoje procesy i ma sieć |
| `--clearenv` | ⚠️ **`ANTHROPIC_API_KEY` ląduje w piaskownicy**. To najczęstszy wyciek |
| `--new-session` | atak `TIOCSTI` — wstrzyknięcie znaków do Twojego terminala |
| `systemd-run` z limitami | `bwrap` **nie limituje zasobów**; pętla nieskończona zjada maszynę |

> ⚠️ **`bwrap` nie ma limitów zasobów i to jest jego najczęściej przeoczana luka.**
> Namespace izolują *widoczność*, nie *zużycie*. Bez `systemd-run` jedna pętla
> `while True: []` zabiera CPU, a `[0]*10**10` zabiera RAM — i Twoja brama umiera razem
> z całą flotą.

---

## 3. Szczebel 2 — kontener rootless

```bash
# podman: bez demona, bez roota — właściwy wybór, gdy potrzebujesz obrazu
podman run --rm \
  --network none \
  --read-only \
  --tmpfs /tmp:rw,size=256m,noexec \
  --memory 1g --cpus 2 --pids-limit 64 \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --security-opt seccomp=/etc/osa/seccomp.json \
  --user 65534:65534 \
  -v "$ARCHIWUM:/archiwum:ro,Z" \
  -v "$OBSZAR:/praca:rw,Z" \
  osa-runtime:1.0 python3 /praca/_program.py
```

| Kiedy warto zejść z `bwrap` na kontener | Kiedy nie |
| :-- | :-- |
| Potrzebujesz konkretnych zależności (OCR, pandoc) | Wystarczy Python ze stdlib |
| Chcesz odtwarzalny obraz z SBOM | Iterujesz szybko |
| Uruchamiasz cudzy kod z obrazu | `bwrap` startuje 20× szybciej |

⚠️ **`--cap-drop ALL` i `--security-opt no-new-privileges` nie są opcjonalne.** Kontener
bez nich ma domyślny zestaw capabilities, który przy kilku znanych lukach wystarcza do
ucieczki. A i tak **jądro jest wspólne** — to nadal szczebel 2, nie 3.

---

## 4. Szczebel 3–4 — gVisor i microVM

**gVisor** (`runsc`) — jądro Linuksa zaimplementowane w przestrzeni użytkownika.
Proces w piaskownicy wykonuje `syscall`, który przechwytuje `runsc`, a nie jądro hosta.

```bash
# instalacja i uruchomienie przez podman
podman run --rm --runtime=/usr/local/bin/runsc --network none … osa-runtime:1.0
```

| Zalety | Koszty |
| :-- | :-- |
| ⭐ Luka w jądrze Linuksa **nie jest wykorzystywalna** ze środka | narzut I/O 10–40 % |
| Start w milisekundach | część `syscall` niezaimplementowana |
| Działa z podmanem/dockerem | ⚠️ luka w samym gVisor pozostaje możliwa |

**microVM** (Firecracker, libkrun) — prawdziwa wirtualizacja z osobnym jądrem, start
poniżej sekundy. To jest architektura, której używają Vercel, AWS Lambda i E2B:
**pełna VM jako granica zewnętrzna, microVM jako jednostka wykonania na żądanie**.

### 4.1 · Rekomendacja dla Twojej maszyny

```
Archiwista, Gospodarz        → szczebel 1 (bwrap + systemd-run)
code-mode z zadania własnego → szczebel 1
Badacz i wszystko z sieci    → szczebel 2 dziś, ⭐ szczebel 3 gdy Badacz ruszy na serio
```

⚠️ **Nie buduj microVM teraz.** Twoje realne zagrożenie to **wstrzyknięcie przez treść**
(ASI01/ASI06), a nie exploit jądra. Wstrzyknięcie przechodzi przez każdy szczebel
izolacji jednakowo, bo **nie łamie piaskownicy — używa uprawnień, które sam dałeś**.
Szczebel 3 dokładasz, gdy Badacz zacznie wykonywać kod pobrany z sieci; wtedy to jest
konieczne, nie wcześniej.

⭐ **To jest najważniejsze zdanie tej części. Izolacja nie rozwiązuje wstrzyknięcia.**
Rozwiązaniem wstrzyknięcia jest ograniczenie uprawnień (§5) i granica zaufania
(część 16), a nie mocniejsza piaskownica.

---

## 5. Kontrola wyjścia sieciowego

Badacz potrzebuje sieci. Dawanie mu „sieci" to dawanie mu **całego internetu plus
Twojej sieci lokalnej plus metadanych chmury**.

### 5.1 · Właściwy wzorzec: brak sieci + proxy jako jedyne wyjście

```
┌─ piaskownica Badacza ──┐
│  --unshare-net         │   ⭐ zero sieci w środku
│  gniazdo uniksowe ─────┼──►  proxy poza piaskownicą
└────────────────────────┘        │  lista dozwolonych domen
                                  │  limit żądań i bajtów
                                  │  dziennik każdego żądania
                                  ▼  internet
```

```python
# $OSA/piaskownica/proxy.py
"""Jedyne wyjście Badacza. Lista dozwolonych, limity, dziennik."""
DOZWOLONE = {"pl.wikipedia.org", "arxiv.org", "isap.sejm.gov.pl", "docs.python.org"}
LIMIT_ZADAN, LIMIT_BAJTOW = 60, 20 * 1024 * 1024

def wolno(url: str, licznik: dict) -> tuple[bool, str]:
    from urllib.parse import urlparse
    u = urlparse(url)
    if u.scheme != "https":
        return False, "Tylko HTTPS."
    if u.hostname not in DOZWOLONE:
        return False, (f"Domena '{u.hostname}' nie jest na liście dozwolonych. "
                       f"Dozwolone: {', '.join(sorted(DOZWOLONE))}. "
                       f"Jeśli potrzebujesz innej — poproś człowieka o dopisanie.")
    if licznik["zadan"] >= LIMIT_ZADAN:
        return False, f"Limit {LIMIT_ZADAN} żądań na sesję wyczerpany."
    if licznik["bajtow"] >= LIMIT_BAJTOW:
        return False, "Limit pobranych danych wyczerpany."
    return True, ""
```

⚠️ **Pułapka P45 z kursu 1 wraca i jest kluczowa: `HTTP_PROXY` to konwencja, nie
wymuszenie.** Zmienna środowiskowa jest **sugestią dla grzecznych bibliotek**. Kod,
który otworzy surowe gniazdo, ją zignoruje. **Jedynym wymuszeniem jest `--unshare-net`**
— skoro w namespace nie ma interfejsu sieciowego, nie ma czego otworzyć.

### 5.2 · Zablokuj adres metadanych — nawet lokalnie

```bash
# 169.254.169.254 to metadane chmury. Na laptopie "niepotrzebne" —
# aż przeniesiesz agenta na VPS i zapomnisz. Blokuj od początku.
sudo nft add rule inet filter output ip daddr 169.254.169.254 drop
```

---

## 6. Sekrety — warstwa poza piaskownicą

OpenClaw miał tu udokumentowany problem: **wartości Secret Store nie były szyfrowane
spoczynkowo w wersji 2.0.** Ucz się na cudzym.

**Trzy zasady:**

1. **Sekret nigdy nie wchodzi do piaskownicy.** Ani w środowisku, ani w pliku, ani
   w argumencie (`ps` je widzi).
2. **Agent nie dostaje sekretu — dostaje zdolność.** Nie „masz klucz do API" tylko
   „masz funkcję `wyslij_zapytanie()`", która działa **poza** piaskownicą.
3. **Plik sekretów ma osobne uprawnienia i innego właściciela** niż proces agenta.

```python
# $OSA/sekrety.py — działa TYLKO w procesie bramy, nigdy w piaskownicy
import pathlib, json, os, stat

def wczytaj() -> dict:
    p = pathlib.Path("~/.config/osa/sekrety.json").expanduser()
    m = p.stat().st_mode
    if m & (stat.S_IRWXG | stat.S_IRWXO):
        raise PermissionError(f"{p} ma prawa {oct(m & 0o777)}. Wymagane 0600: chmod 600 {p}")
    return json.loads(p.read_text())

def granica_zdolnosci(nazwa: str):
    """Agent woła to przez bramę. Sekret NIE przekracza granicy piaskownicy."""
    ...
```

⭐ **Zasada 2 jest tą, która realnie ratuje.** Gdy agent zostanie przejęty przez
wstrzyknięcie, **nie ma czego wyeksfiltrować** — nie posiada klucza, tylko możliwość
wywołania jednej funkcji przez bramę. Brama widzi każde wywołanie i może je odrzucić.
To jest ta sama idea, co vault po stronie dostawcy: **sekret podstawiany na wyjściu,
nigdy widoczny wewnątrz**.

---

## 7. OD ZERA — trzy poziomy wpięte w bramę

```python
# $OSA/piaskownica/poziomy.py
"""Poziom izolacji wynika z zaufania sesji (część 2), nie z nazwy agenta."""
import subprocess, pathlib, os, shlex

POZIOMY = {
    "host":        {"szczebel": 0, "siec": True,  "zapis": ["~/dokumenty", "/tmp"]},
    "lekki":       {"szczebel": 1, "siec": False, "zapis": ["/tmp/praca"]},
    "piaskownica": {"szczebel": 1, "siec": False, "zapis": ["/tmp/praca"], "clearenv": True},
    "scisly":      {"szczebel": 2, "siec": False, "zapis": ["/tmp/praca"], "clearenv": True},
}

MAPA_ZAUFANIA = {          # ⭐ jedno miejsce, w którym to się rozstrzyga
    ("archiwista", "host"):        "lekki",
    ("archiwista", "piaskownica"): "piaskownica",
    ("gospodarz",  "host"):        "lekki",
    ("badacz",     "host"):        "scisly",     # ⚠️ Badacz NIGDY nie dostaje 'lekki'
    ("badacz",     "piaskownica"): "scisly",
}

def poziom_dla(agent: str, zaufanie_sesji: str) -> str:
    return MAPA_ZAUFANIA.get((agent, zaufanie_sesji), "scisly")   # P66: domyślnie NAJWĘŻEJ

def uruchom(agent, zaufanie_sesji, polecenie, obszar="/tmp/praca", archiwum=None):
    p = POZIOMY[poziom_dla(agent, zaufanie_sesji)]
    if p["szczebel"] == 0:
        return subprocess.run(polecenie, shell=True, capture_output=True,
                              text=True, timeout=60)
    if p["szczebel"] == 1:
        env = dict(os.environ)
        if archiwum: env["ARCHIWUM"] = archiwum
        return subprocess.run(
            [str(pathlib.Path(os.environ["OSA"], "piaskownica/szczebel1.sh")),
             obszar, "bash", "-c", polecenie],
            capture_output=True, text=True, timeout=60, env=env)
    return _kontener(polecenie, obszar, archiwum)
```

⭐ **`MAPA_ZAUFANIA` jest jedynym miejscem w całym systemie, gdzie rozstrzyga się, ile
komu wolno.** Gdy za pół roku będziesz się zastanawiał „czy Badacz może czytać
`~/dokumenty`" — patrzysz w jeden słownik, a nie przeszukujesz kodu. To jest warte
więcej niż elegancja.

---

## 8. EKSPERYMENT 10 — próby ucieczki

⭐ **Nie ufaj piaskownicy, której nie próbowałeś złamać.**

```bash
mkdir -p $OSA/testy/ucieczka && cd $OSA/testy/ucieczka
```

```python
# proby.py — każda próba MUSI się nie udać
PROBY = [
 ("odczyt /etc/shadow",     "open('/etc/shadow').read()"),
 ("odczyt kluczy SSH",      "open('/root/.ssh/id_rsa').read()"),
 ("odczyt dokumentów",      "open('/home/USER/dokumenty/umowa.txt').read()"),
 ("zapis poza obszarem",    "open('/home/USER/wlam.txt','w').write('x')"),
 ("zapis do /usr",          "open('/usr/bin/zle','w').write('x')"),
 ("gniazdo TCP",            "import socket; socket.create_connection(('1.1.1.1',80),2)"),
 ("DNS",                    "import socket; socket.gethostbyname('example.com')"),
 ("metadane chmury",        "import urllib.request; urllib.request.urlopen('http://169.254.169.254/',timeout=2)"),
 ("lista procesów hosta",   "import os; print([p for p in os.listdir('/proc') if p.isdigit()][:20])"),
 ("sekret ze środowiska",   "import os; print([k for k in os.environ if 'KEY' in k or 'TOKEN' in k])"),
 ("fork bomb",              "import os\nwhile True: os.fork()"),
 ("wyczerpanie RAM",        "x=[0]*10**10"),
 ("pętla CPU",              "while True: pass"),
 ("zapis przez /proc/self", "open('/proc/self/root/etc/passwd','w')"),
 ("podniesienie uprawnień", "import subprocess; subprocess.run(['sudo','id'])"),
 ("ucieczka ../",           "open('../../../../etc/passwd').read()"),
]
```

```bash
for poziom in lekki piaskownica scisly; do
  python3 proby.py --poziom $poziom
done
```

| # | Próba | `lekki` | `piaskownica` | `scisly` | Oczekiwane |
| --: | :-- | :-: | :-: | :-: | :-- |
| 1 | `/etc/shadow` | | | | ✗ wszędzie |
| 3 | dokumenty | | | | ✗ (⚠️ poza Archiwistą przez `/archiwum` ro) |
| 6 | gniazdo TCP | | | | ✗ wszędzie |
| 10 | sekret ze środowiska | | | | ✗ przy `clearenv` |
| 11 | fork bomb | | | | ✗ przy `TasksMax` |
| 12 | wyczerpanie RAM | | | | ✗ przy `MemoryMax` |
| 13 | pętla CPU | | | | ⚠️ **nie zostanie zablokowana** — tylko ograniczona przez `CPUQuota` |

⚠️ **Wiersz 13 jest nauką samą w sobie.** `CPUQuota=200%` nie zatrzymuje pętli
nieskończonej — **ogranicza ją do dwóch rdzeni**. Zatrzymuje ją dopiero timeout
w `uruchom()`. Limity zasobów i limity czasu to dwie różne rzeczy i **potrzebujesz obu**.

### 8.1 · Pomiar drugi — koszt izolacji

| Operacja | bez izolacji | `bwrap` | kontener | gVisor |
| :-- | --: | --: | --: | --: |
| Start procesu | ms | ms | ms | ms |
| Odczyt 100 plików | ms | ms | ms | ms |
| Program 5 s CPU | s | s | s | s |

⚠️ **Predykcja:** `bwrap` dokłada ~10–20 ms na start i **prawie nic** na I/O.
Kontener ~200 ms. gVisor startuje szybko, ale **I/O bywa wolniejsze o 10–40 %** —
i dla agenta czytającego setki plików to jest odczuwalne. Zmierz, zanim zdecydujesz.

---

## 9. ĆWICZENIE

1. Zaimplementuj `szczebel1.sh`, `poziomy.py` i proxy z listą dozwolonych.
2. Wepnij `poziom_dla()` w bramę — **każde** wykonanie narzędzia przechodzi przez tę mapę.
3. Uruchom wszystkie 16 prób na trzech poziomach. **Każda ma zawieść.** Każda, która
   przejdzie, to zadanie do naprawy przed częścią 13.
4. Wystaw Badaczowi narzędzie `pobierz(url)` działające **wyłącznie** przez proxy
   i sprawdź, że w piaskownicy nie ma interfejsu sieciowego:

```bash
python3 sesja-cli.py piaskownica badacz --diagnostyka
# oczekuj:
#   poziom:          scisly (szczebel 2)
#   sieć w środku:   BRAK (--unshare-net)   ✓
#   wyjście:         proxy, 4 domeny, 60 żądań/sesję
#   zapis:           /tmp/praca (256 MB)
#   środowisko:      wyczyszczone, 0 sekretów   ✓
#   limity:          1 GB RAM, 200% CPU, 64 zadania, 60 s
```

5. **Zadanie dodatkowe:** dopisz do `proby.py` trzy własne próby ucieczki. Jeśli
   którakolwiek przejdzie — masz realne znalezisko i wiesz o swoim systemie coś, czego
   nie wiedziałeś.

---

## 10. Pułapki tej części

| ID | Pułapka | Objaw | Jak uniknąć |
| :-- | :-- | :-- | :-- |
| **P99** | **Mylenie kontenera z piaskownicą** | „Jest w Dockerze, więc bezpieczne" — a jądro wspólne | Kontener to szczebel 2. Exploit jądra przechodzi. Przy kodzie z sieci → gVisor lub microVM |
| **P100** | **Brak limitów zasobów przy `bwrap`** | Jedna pętla zjada maszynę; brama i cała flota padają | `bwrap` nie limituje. `systemd-run` z `MemoryMax`, `CPUQuota`, `TasksMax` **i** timeout |
| **P101** | **Środowisko dziedziczone do piaskownicy** | `ANTHROPIC_API_KEY` widoczny dla kodu agenta; wstrzyknięcie go wynosi | `--clearenv` + jawne `--setenv`. Sekrety przez granicę zdolności, nigdy w środku |
| **P102** | **`HTTP_PROXY` jako kontrola sieci** | Kod z surowym gniazdem ignoruje proxy i wychodzi, gdzie chce | Jedynym wymuszeniem jest `--unshare-net`. Proxy dopiero **poza** piaskownicą |
| **P103** | **Przekonanie, że piaskownica chroni przed wstrzyknięciem** | Agent w idealnej izolacji wykonuje polecenie atakującego **swoimi uprawnieniami** | Izolacja ogranicza **promień rażenia**, nie zapobiega atakowi. Obrona: uprawnienia + granica zaufania (część 16) |

---

## 11. Checkpoint

```bash
cd $OSA
python3 testy/ucieczka/proby.py --poziom scisly --wymagaj-porazki-wszystkich \
  && echo "✓ wszystkie 16 prób zablokowane na poziomie ścisłym"
python3 -c "
from piaskownica.poziomy import poziom_dla
assert poziom_dla('badacz','host') == 'scisly',  'Badacz NIGDY nie dostaje lekkiego'
assert poziom_dla('nieznany','host') == 'scisly','domyślnie najwęziej (P66)'
print('✓ mapa zaufania')"
ls -l ~/.config/osa/sekrety.json | grep -q '^-rw-------' && echo "✓ sekrety 0600"
git add -A && git commit -m "część 10: drabina izolacji, proxy, sekrety, próby ucieczki"
```

- [ ] Znasz pięć szczebli i wiesz, **co każdy zatrzymuje** — zwłaszcza wiersz „exploit jądra"
- [ ] Poziom izolacji wynika ze **źródła wejścia**, nie z nazwy agenta
- [ ] `bwrap` ma `--clearenv`, `--new-session` i limity przez `systemd-run`
- [ ] Sieć: `--unshare-net` w środku, proxy z listą dozwolonych na zewnątrz
- [ ] Sekrety nigdy nie przekraczają granicy — agent dostaje zdolność, nie klucz
- [ ] `MAPA_ZAUFANIA` jest jedynym miejscem decyzji o uprawnieniach
- [ ] ⭐ **16 prób ucieczki, wszystkie zablokowane, koszt izolacji zmierzony**
- [ ] ⭐ Rozumiesz, że **izolacja nie rozwiązuje wstrzyknięcia** — ogranicza skutki

---

**Dalej: `11-HARMONOGRAM-PROAKTYWNOSC.md`** — agent, który budzi się sam, robi coś
sensownego i **nie zawraca Ci głowy, gdy nie ma po co**.
