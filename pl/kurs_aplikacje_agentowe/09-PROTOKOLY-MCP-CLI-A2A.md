# Część 9 · Protokoły i integracje — MCP, CLI, A2A

**Poziom:** ⭐⭐⭐ · **Czas:** ~4 h · **Wymaga:** części 7 i 8
**Produkuje:** tę samą zdolność jako serwer MCP i jako CLI, zmierzone porównanie, decyzję na piśmie

---

## 0. Spór, który rozstrzygasz pomiarem

Peter Steinberger, autor OpenClaw:

> MCP i RAG to **trucizna kontekstu**. Serwer GitHub MCP to około **23 tys. tokenów**.
> A ja mogę po prostu wywołać CLI po nazwie — CLI pokaże `--help`, i kontekst ma
> pełną informację, jak to działa. **Za zero.**

Rynek MCP w tym samym czasie: setki serwerów, wsparcie we wszystkich większych
narzędziach, specyfikacja przepisana w lipcu 2026.

**Obie strony mają rację w swoim kontekście.** Ta część nie ma Cię przekonać do jednej
— ma dać Ci **liczbę z Twojej maszyny**, żebyś rozstrzygał sam.

---

## 1. Co kosztuje protokół

Rozbij koszt integracji na trzy pozycje. Prawie nikt tego nie robi i stąd biorą się
spory bez konkluzji.

| Pozycja | MCP | CLI | Funkcja w kodzie (część 8) |
| :-- | :-- | :-- | :-- |
| **Koszt stały kontekstu** (każda tura) | ⚠️ schematy wszystkich narzędzi | ⭐ ~1 linia | ⭐ ~1 linia w `pomoc()` |
| **Koszt odkrycia** (raz) | zero — schematy już są | `--help`, ~300–1500 tok. | `pomoc()`, ~400 tok. |
| **Koszt wywołania** | JSON zgodny ze schematem | linia poleceń | wywołanie funkcji |
| Interoperacyjność | ⭐⭐ z każdym klientem MCP | ⭐ z każdym shellem | tylko Twój system |
| Uwierzytelnianie | ⭐ wbudowane (OAuth, CIMD) | Twoje | Twoje |
| Odkrywanie w czasie działania | ⭐ tak | ✗ | ✗ |

⭐ **Kluczowe rozróżnienie: koszt stały vs koszt odkrycia.** MCP płaci **w każdej
turze** za narzędzia, których agent w tej turze nie użyje. CLI płaci **raz**, gdy agent
faktycznie chce je poznać. Przy 40 turach i 20 narzędziach różnica jest ogromna — i to
jest dokładnie argument Steinbergera, wyrażony w jednostkach.

⚠️ **Ale to nie jest cała prawda.** MCP od specyfikacji **2026-07-28** ma wyszukiwanie
narzędzi na żądanie, co spłaszcza koszt stały (raportowane ~85 % redukcji na
ewaluacjach MCP). Teza „23 tys. tokenów" opisuje serwer skonfigurowany po staremu,
z pełnym katalogiem w prompcie. **Mierz swoją konfigurację, nie cudzą.**

---

## 2. MCP w 2026 — co się zmieniło

Specyfikacja **2026-07-28** to duża przebudowa i warto znać cztery zmiany:

| Zmiana | Co znaczy w praktyce |
| :-- | :-- |
| ⭐ **Bezstanowy rdzeń** | Z dwukierunkowego protokołu stanowego → żądanie/odpowiedź. **Serwer MCP staje się zwykłym HTTP** — łatwiejszy do napisania, przetestowania i wystawienia |
| **MRTR** (Multi Round-Trip Requests) | Sampling i elicitation bez stale otwartego strumienia. Koniec z długożyjącym SSE tam, gdzie nie jest potrzebny |
| **Utwardzenie autoryzacji** | RFC 9207 (walidacja issuera), odejście od DCR na rzecz CIMD |
| **Zadania, MCP Apps, EMA** | Rozszerzenia: długie operacje, interfejs, zarządzanie w organizacji |

**Co z tego wynika dla Ciebie.** Bezstanowy rdzeń jest dobrą wiadomością: serwer MCP
w czystym Pythonie bez zależności to teraz kilkadziesiąt linii. Cała reszta —
autoryzacja, EMA — rozwiązuje problemy, których **w systemie na pętli zwrotnej nie
masz**.

---

## 3. OD ZERA — ta sama zdolność, trzy interfejsy

Zdolność testowa: **wyszukiwanie w archiwum dokumentów**. Napiszesz ją raz jako logikę,
a potem wystawisz trojako.

### 3.1 · Logika (wspólna)

```python
# $OSA/zdolnosci/archiwum.py
"""Logika. Nie wie nic o protokołach — i to jest sedno."""
import pathlib, re

def szukaj(korzen: str, fraza: str, limit: int = 20) -> list[dict]:
    """Szuka frazy w dokumentach tekstowych. Zwraca trafienia z kontekstem."""
    out = []
    for p in sorted(pathlib.Path(korzen).rglob("*.txt")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(re.escape(fraza), t, re.I):
            a, b = max(0, m.start() - 60), min(len(t), m.end() + 60)
            out.append({"plik": str(p.relative_to(korzen)),
                        "pozycja": m.start(),
                        "kontekst": t[a:b].replace("\n", " ")})
            if len(out) >= limit:
                return out
    return out
```

### 3.2 · Wariant A — CLI

```python
#!/usr/bin/env python3
# $OSA/zdolnosci/archiwum-cli.py
"""Szuka frazy w archiwum dokumentów.

UŻYCIE:
  archiwum-cli.py szukaj FRAZA [--limit N] [--json]
  archiwum-cli.py info

PRZYKŁADY:
  archiwum-cli.py szukaj "termin płatności" --limit 5
  archiwum-cli.py szukaj Orange --json

WYJŚCIE:
  Domyślnie: plik:pozycja  kontekst
  Z --json:  lista obiektów {plik, pozycja, kontekst}

Kod wyjścia 0 = znaleziono, 1 = brak trafień, 2 = błąd użycia.
"""
import sys, json, os
from archiwum import szukaj

def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return 2
    if a[0] == "info":                                  # ← reguła Steinbergera
        print(json.dumps({"wersja": "1.2.0",
                          "korzen": os.environ.get("ARCHIWUM", "~/dokumenty"),
                          "gotowe": os.path.isdir(os.path.expanduser(
                              os.environ.get("ARCHIWUM", "~/dokumenty")))}))
        return 0
    if a[0] != "szukaj" or len(a) < 2:
        print(__doc__, file=sys.stderr); return 2

    fraza = a[1]
    limit = int(a[a.index("--limit") + 1]) if "--limit" in a else 20
    w = szukaj(os.path.expanduser(os.environ.get("ARCHIWUM", "~/dokumenty")), fraza, limit)
    if "--json" in a:
        print(json.dumps(w, ensure_ascii=False, indent=1))
    else:
        for t in w:
            print(f'{t["plik"]}:{t["pozycja"]}  …{t["kontekst"]}…')
    if not w:
        print(f"Brak trafień dla '{fraza}'.", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

⭐ **Docstring **jest** dokumentacją dla modelu.** Agent uruchamia `archiwum-cli.py
--help`, dostaje 25 linii i **wie wszystko**: składnię, przykłady, format wyjścia, kody
wyjścia. To jest cały mechanizm, o którym mówi Steinberger — i jest zaskakująco tani.

Podkomenda `info` to jego reguła z MCP Best Practices: agent musi umieć **zdiagnozować
narzędzie sam**, bez pytania Ciebie.

### 3.3 · Wariant B — serwer MCP (bezstanowy)

```python
# $OSA/zdolnosci/archiwum-mcp.py
"""Serwer MCP, rdzeń bezstanowy (2026-07-28). Czyste HTTP, zero zależności."""
import json, os, http.server, socketserver
from archiwum import szukaj

NARZEDZIA = [{
    "name": "archiwum_szukaj",
    "description": ("Szuka frazy w archiwum dokumentów tekstowych. "
                    "Zwraca listę trafień z 60 znakami kontekstu z każdej strony. "
                    "Gdy brak trafień — zwraca pustą listę, nie błąd."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "fraza": {"type": "string", "description": "Szukany tekst, bez wyrażeń regularnych."},
            "limit": {"type": "integer", "description": "Maks. trafień. Domyślnie 20.", "default": 20},
        },
        "required": ["fraza"],
    },
}]

class MCP(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        z = json.loads(self.rfile.read(n) or b"{}")
        m, ident = z.get("method"), z.get("id")

        if m == "initialize":
            w = {"protocolVersion": "2026-07-28",
                 "capabilities": {"tools": {}},
                 "serverInfo": {"name": "archiwum", "version": "1.2.0"}}
        elif m == "tools/list":
            w = {"tools": NARZEDZIA}
        elif m == "tools/call":
            p = z["params"]["arguments"]
            wynik = szukaj(os.path.expanduser(os.environ.get("ARCHIWUM", "~/dokumenty")),
                           p["fraza"], p.get("limit", 20))
            w = {"content": [{"type": "text",
                              "text": json.dumps(wynik, ensure_ascii=False)}],
                 "isError": False}
        else:
            return self._wyslij({"jsonrpc": "2.0", "id": ident,
                                 "error": {"code": -32601, "message": f"nieznana metoda {m}"}})
        self._wyslij({"jsonrpc": "2.0", "id": ident, "result": w})

    def _wyslij(self, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers(); self.wfile.write(b)

    def log_message(self, *a): pass          # P63 — cisza na stdout

if __name__ == "__main__":
    with socketserver.TCPServer(("127.0.0.1", 18790), MCP) as s:
        s.serve_forever()
```

> 💡 **Zwróć uwagę, jak mało tu kodu.** Bezstanowy rdzeń 2026-07-28 sprowadza serwer MCP
> do zwykłego endpointu JSON-RPC. Wcześniejsza wersja wymagała SSE i zarządzania
> połączeniem — **to jest realna zmiana na lepsze**, którą warto docenić niezależnie od
> tego, czy ostatecznie użyjesz MCP.

### 3.4 · Wariant C — funkcja w API (część 8)

```python
def szukaj_w_archiwum(fraza: str, limit: int = 20) -> list[dict]:
    """Szuka frazy w archiwum. Zwraca [{plik, pozycja, kontekst}].
    Pusta lista = brak trafień (nie błąd). Fraza dosłowna, bez regex."""
    return szukaj(KORZEN, fraza, limit)
```

---

## 4. EKSPERYMENT 9 — zmierz trzy warianty

**Hipoteza:** przy małej liczbie zdolności CLI i funkcja wygrywają kosztem stałym,
a MCP zaczyna się opłacać dopiero, gdy potrzebujesz interoperacyjności albo
uwierzytelniania.

### 4.1 · Pomiar 1 — koszt stały kontekstu

```bash
mkdir -p $OSA/pomiary/protokoly && cd $OSA/pomiary/protokoly

# Ile tokenów zajmuje SAMO udostępnienie zdolności modelowi?
python3 policz_tokeny.py --wariant cli    # linia: "masz archiwum-cli.py, użyj --help"
python3 policz_tokeny.py --wariant mcp    # pełny inputSchema w prompcie
python3 policz_tokeny.py --wariant api    # linia w pomoc()
```

| Zdolności | CLI | MCP (schematy) | API (code-mode) |
| --: | --: | --: | --: |
| 1 | | | |
| 5 | | | |
| 20 | | | |

⚠️ **Predykcja:** CLI i API rosną ~liniowo po ~15 tokenów na zdolność. MCP rośnie
po ~150–250 tokenów na narzędzie. Przy 20 zdolnościach spodziewam się **~300 vs
~4000 tokenów**. To jest teza Steinbergera w miniaturze — i jeśli tak wyjdzie, masz ją
potwierdzoną na własnym sprzęcie.

### 4.2 · Pomiar 2 — skuteczność użycia

20 zadań wymagających wyszukiwania, po 3 przebiegi:

| Wariant | Poprawne /20 | Śr. tur | Śr. tokenów | Czas |
| :-- | --: | --: | --: | --: |
| CLI (przez `powloka`) | | | | |
| MCP | | | | |
| API (code-mode) | | | | |

⚠️ **Predykcja:** MCP będzie miał **najwyższą trafność przy pierwszym użyciu** (schemat
jest w prompcie, model nie musi zgadywać), ale najwyższy koszt. CLI wymaga jednej tury
na `--help` **przy pierwszym użyciu w sesji**, potem jest równie skuteczne i tańsze.

⭐ **To jest sedno kompromisu i warto je zapamiętać: MCP kupuje trafność pierwszego
strzału za koszt stały płacony w każdej turze.** Przy krótkich sesjach to się opłaca.
Przy długich — nie.

### 4.3 · Pomiar 3 — czy model radzi sobie z `--help`

To jest **ukryte założenie tezy Steinbergera** i u modeli lokalnych wcale nie musi
zachodzić:

```bash
python3 test_help.py --model gpt-oss-20b --narzedzi 8
# Dla 8 nieznanych CLI: czy model po --help użyje ich poprawnie za pierwszym razem?
```

| Model | Poprawne użycie po `--help` /8 |
| :-- | --: |
| `gpt-oss-20b` | |
| `qwen3-32b` | |

⚠️ **To jest najciekawszy pomiar w tej części.** Steinberger używa modeli frontier,
które czytają `--help` bezbłędnie. Jeśli `gpt-oss-20b` wypada poniżej ~6/8, jego teza
**u Ciebie nie zachodzi w tej formie** — i właściwym wnioskiem jest albo schemat
w prompcie (MCP), albo API z docstringami (część 8), które jest tańsze od obu.

---

## 5. Kiedy protokół zarabia na siebie

| Sytuacja | Wybór | Dlaczego |
| :-- | :-- | :-- |
| Zdolność tylko dla Twojego agenta | ⭐ **funkcja w API** | zero narzutu, docstring wystarcza |
| Zdolność, której używasz też z terminala | ⭐ **CLI** | jedno źródło prawdy, Ty i agent tak samo |
| Zdolność dla **innych klientów** (IDE, cudzy agent) | ⭐ **MCP** | interoperacyjność jest jego jedynym prawdziwym argumentem |
| Usługa zewnętrzna z OAuth | ⭐ **MCP** | uwierzytelnianie masz za darmo |
| Ponad 25 zdolności | ⭐ **code-mode** (część 8) | patrz pomiar 4.1 |
| Zdolność odkrywana w czasie działania | **MCP** | jedyny, który to ma |

⭐ **Reguła domyślna dla Twojego systemu:** **funkcja w API → CLI, gdy przydatna
człowiekowi → MCP tylko gdy ktoś z zewnątrz ma z tego korzystać.** Odwrotna kolejność
(„zacznijmy od MCP, bo to standard") kosztuje Cię tokeny w każdej turze za
interoperacyjność, z której nie korzystasz.

> ⚠️ **I argument bezpieczeństwa, który przeważa nad wydajnością.** Każdy serwer MCP to
> **element łańcucha dostaw** (ASI04) — kod, który czytasz cudzymi oczami, z dostępem
> do Twoich narzędzi. Statystyka z OWASP: jeden skompromitowany serwer w **72,4 %**
> przypadków wpływał na działanie kolejnych. Funkcja, którą napisałeś sam, nie ma tej
> właściwości. **Przy równym wyniku wybieraj to, czego nie musisz ufać.**

---

## 6. A2A — protokół między agentami

MCP łączy agenta z narzędziami. **A2A** (Agent2Agent, pod Linux Foundation, 100+ firm)
łączy agentów ze sobą.

| | MCP | A2A |
| :-- | :-- | :-- |
| Łączy | agent ↔ narzędzie | agent ↔ agent |
| Model | wywołanie funkcji | delegacja zadania |
| Stan | bezstanowy (od 2026-07) | zadania długotrwałe |
| Odkrywanie | lista narzędzi | „karta agenta" (Agent Card) z umiejętnościami |

**Czy potrzebujesz A2A?** W Twoim systemie — **nie, i to na długo**. Trzej agenci
w jednym procesie komunikują się wywołaniem funkcji, które jest o rzędy wielkości
tańsze i **nie ma powierzchni ataku**.

A2A zaczyna mieć sens dokładnie wtedy, gdy:

- agenci działają w **osobnych procesach lub maszynach**, **i**
- należą do **różnych właścicieli** (inaczej wystarczy Twoje RPC), **i**
- muszą się **odkrywać dynamicznie**.

⚠️ **Zanim dotkniesz A2A, przeczytaj ASI07 (niebezpieczna komunikacja między agentami)
z części 16.** Protokół między agentami to **nowa granica zaufania** — a większość
implementacji, które widziałem, traktuje wiadomość od „innego agenta" jako zaufaną.
To jest ta sama pomyłka co traktowanie treści ze strony WWW jako polecenia.

W części 13 zbudujesz komunikację między swoimi agentami. Zrobisz to przez wywołanie
funkcji z jawną granicą zaufania — **i to jest właściwy wybór**, dopóki wszyscy agenci
są Twoi.

---

## 7. ĆWICZENIE — decyzja na piśmie

1. Zaimplementuj wszystkie trzy warianty zdolności „szukaj w archiwum".
2. Przeprowadź trzy pomiary z §4 na obu modelach.
3. Napisz `decyzje/0003-protokoly.md` w formacie ADR z części 1, z **liczbami
   z Twojego pomiaru**, nie z tego kursu.
4. Wdróż decyzję: usuń warianty, których nie wybrałeś. **Utrzymywanie trzech
   interfejsów do jednej zdolności to gwarantowany rozjazd.**

```markdown
# ADR 0003 · Protokoły integracji

## Decyzja
Domyślnie: funkcja w API (code-mode). CLI dla zdolności używanych też z terminala.
MCP: <tutaj Twoja decyzja>.

## Pomiar, na którym się opieram
| Zdolności | CLI | MCP | API |
|---|---|---|---|
| 20 | ___ tok. | ___ tok. | ___ tok. |

Trafność po --help, gpt-oss-20b: ___/8.

## Jak poznam, że to była zła decyzja
Gdy zechcę użyć swoich zdolności z cudzego klienta — wtedy MCP przestaje być
kosztem, a zaczyna być jedyną drogą.
```

---

## 8. Pułapki tej części

| ID | Pułapka | Objaw | Jak uniknąć |
| :-- | :-- | :-- | :-- |
| **P95** | **Przyjęcie liczby „23 tys. tokenów" bez sprawdzenia własnej konfiguracji** | Odrzucasz MCP na podstawie cudzego pomiaru sprzed zmiany specyfikacji | Zmierz swoje (§4.1). Od 2026-07 MCP ma wyszukiwanie narzędzi na żądanie |
| **P96** | **Założenie, że model poradzi sobie z `--help`** | Teza o CLI zakłada model frontier; mały gubi składnię | Pomiar 4.3. Poniżej ~6/8 — CLI przegrywa u Ciebie |
| **P97** | **Serwer MCP jako zaufany element systemu** | Cudzy kod z dostępem do Twoich narzędzi; kaskada w 72,4 % przypadków | Serwer MCP = łańcuch dostaw (ASI04). Czytasz albo nie instalujesz |
| **P98** | **Trzy interfejsy do jednej zdolności utrzymywane równolegle** | Poprawka w CLI, MCP zostaje ze starą logiką, agent dostaje różne wyniki | Jedna logika, **jedna** ekspozycja. Reszta kasowana po pomiarze |

---

## 9. Checkpoint

```bash
cd $OSA/zdolnosci
./archiwum-cli.py --help | head -3            && echo "✓ CLI dokumentuje się samo"
./archiwum-cli.py info                        && echo "✓ podkomenda info"
python3 archiwum-mcp.py & sleep 1
curl -s -X POST localhost:18790 -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  | python3 -c "import json,sys; print('✓ MCP:', json.load(sys.stdin)['result']['tools'][0]['name'])"
test -s $OSA/decyzje/0003-protokoly.md && echo "✓ ADR z własnymi liczbami"
git -C $OSA add -A && git -C $OSA commit -m "część 9: protokoły, pomiar, ADR"
```

- [ ] Rozumiesz podział kosztu: stały (każda tura) vs odkrycia (raz)
- [ ] Wiesz, co zmieniła specyfikacja MCP 2026-07-28
- [ ] Napisałeś tę samą zdolność jako CLI, MCP i funkcję
- [ ] CLI dokumentuje się przez `--help` i ma podkomendę `info`
- [ ] ⭐ **Zmierzyłeś koszt stały wszystkich trzech przy 1, 5 i 20 zdolnościach**
- [ ] ⭐ **Sprawdziłeś, czy Twój model radzi sobie z `--help`** — to warunek tezy o CLI
- [ ] Wiesz, kiedy A2A ma sens, i że u Ciebie na razie nie ma
- [ ] Masz ADR 0003 z własnymi liczbami i warunkiem falsyfikacji

---

**Dalej: `10-PIASKOWNICA-PRODUKCYJNA.md`** — drabina izolacji od `bwrap` do microVM
i to, co każdy szczebel naprawdę zatrzymuje.
