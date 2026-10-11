# Część 10 — Hybryda: lokalny model + Claude API

**Poziom: ⭐⭐⭐** · Wymaga: części 6, 8 · Czas: ~3 h

> **Krótki rozdział — i celowo.** Rdzeniem Twojego systemu jest stos lokalny. Claude to
> **jedna dodatkowa opcja w routerze z części 8 §4**, nie nowa architektura.
>
> Kluczowe pytanie nie brzmi „jak wywołać API" (to pół strony kodu), tylko **„co wolno
> wysłać poza maszynę i kto o tym decyduje"**. Od tego zaczniemy.

---

## 1. ⭐ Granica prywatności — zdecyduj najpierw

Sprzedajesz **suwerenność danych**. Dokumenty klientów nie opuszczają maszyny. To jest
Twoja teza produktowa — i hybryda może ją złamać, jeśli zrobisz to bez namysłu.

### 1.1 Trzy klasy danych

```
┌─────────────────────────────────────────────────────────────┐
│ KLASA A — NIGDY nie opuszcza maszyny                        │
│   treść faktur, umów, danych osobowych, NIP-y, kwoty,       │
│   nazwy klientów, zawartość plików klienta                  │
│                            ↓ TYLKO model lokalny            │
├─────────────────────────────────────────────────────────────┤
│ KLASA B — może wyjść po ANONIMIZACJI                        │
│   struktura problemu, schemat bazy, komunikat błędu bez     │
│   danych, fragment kodu bez sekretów                        │
│                            ↓ Claude, po przepuszczeniu      │
│                              przez filtr z §3               │
├─────────────────────────────────────────────────────────────┤
│ KLASA C — może wyjść swobodnie                              │
│   pytania ogólne, dokumentacja publiczna, projektowanie     │
│   architektury, pytania o prawo podatkowe bez danych        │
│                            ↓ Claude bez ograniczeń          │
└─────────────────────────────────────────────────────────────┘
```

⚠️ **Zasada domyślna: WSZYSTKO jest klasą A, dopóki jawnie nie zaklasyfikujesz inaczej.**
Odwrotna domyślność (wysyłamy, chyba że ktoś zabroni) **prędzej czy później wyśle fakturę
klienta**.

### 1.2 Zapisz to w umowie i w kodzie

💡 **Jeśli mówisz klientowi „dane nie opuszczają Państwa serwera", a router czasem wywołuje
Claude — to musi być w umowie.** Ten rozdział jest bezużyteczny, jeśli ta rozmowa się
nie odbędzie. **Techniczny filtr nie zastąpi zgody.**

---

## 2. Kiedy Claude realnie coś dodaje

| Zadanie | Lokalny 20B | Lokalny 32B | Claude |
| :-- | :-- | :-- | :-- |
| wybór narzędzia (gramatyka) | ✅ | ✅ | przesada |
| ekstrakcja z faktury | ✅ | ✅ | ⛔ **klasa A** |
| streszczenie obserwacji | ✅ | ✅ | przesada |
| **projekt architektury** | ⚠️ | ✅ | ⭐ **wyraźnie lepszy** |
| **diagnoza trudnego błędu** | ❌ | ⚠️ | ⭐ **wyraźnie lepszy** |
| **refaktor wielu plików** | ❌ | ⚠️ | ⭐ **wyraźnie lepszy** |
| **pisanie długiego tekstu PL** | ⚠️ | ✅ | ⭐ lepszy |
| **kontekst > 100k tokenów** | ❌ | ❌ | ⭐ **1M kontekstu** |

⭐ **Wzorzec, który polecam: Claude jako konsultant, nie jako wykonawca.**
Lokalny agent pracuje. Gdy utknie — pyta Claude'a o **radę**, opisując problem
**bez danych klienta**. Rada wraca, lokalny agent ją wykonuje.

```
   lokalny agent ──(problem, klasa B/C)──► Claude
        │                                    │
        │◄──────────(strategia)──────────────┘
        │
        └──► wykonuje na danych klasy A, lokalnie
```

---

## 3. Filtr wyjścia — kod, nie dobre chęci

```bash
cat > $AGENT/granica.py <<'PYEOF'
#!/usr/bin/env python3
"""Filtr danych opuszczajacych maszyne. Domyslnie: BLOKUJ."""
import re

WZORCE_WRAZLIWE = [
    (r"\b\d{10}\b",                          "możliwy NIP"),
    (r"\b\d{11}\b",                          "możliwy PESEL/REGON"),
    (r"\b[A-Z]{2}\d{26}\b",                  "numer IBAN"),
    (r"\b\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b", "numer konta"),
    (r"(?i)\bfaktura\s+(vat\s+)?nr\b",       "numer faktury"),
    (r"(?i)\bFV[/-]\d",                      "numer faktury"),
    (r"\b\d{1,3}(?:[  ]\d{3})*,\d{2}\s*(?:zł|PLN)\b", "kwota w złotych"),
    (r"(?i)\b(sp\.\s*z\s*o\.?o\.?|s\.a\.|spółka)\b", "nazwa podmiotu"),
    (r"(?i)-----BEGIN [A-Z ]*PRIVATE KEY",   "klucz prywatny"),
    (r"(?i)\b(api[_-]?key|token|hasło|password)\s*[:=]\s*\S+", "sekret"),
    (r"\b[\w.+-]+@[\w-]+\.[\w.]+\b",         "adres e-mail"),
]

class Granica:
    def __init__(self, tryb: str = "blokuj"):
        """tryb: 'blokuj' | 'anonimizuj' | 'pytaj'"""
        self.tryb = tryb
        self.zablokowane = 0
        self.wyslane = 0

    def sprawdz(self, tekst: str) -> list[tuple[str, str]]:
        """Zwraca [(dopasowanie, opis), ...]."""
        out = []
        for wz, opis in WZORCE_WRAZLIWE:
            for m in re.finditer(wz, tekst):
                out.append((m.group(0), opis))
        return out

    def przepusc(self, tekst: str, klasa: str = "A") -> tuple[bool, str, list]:
        """Zwraca (czy_wolno, tekst_do_wyslania, znaleziska)."""
        if klasa == "A":
            self.zablokowane += 1
            return False, "", [("klasa A", "dane nie opuszczają maszyny")]

        znal = self.sprawdz(tekst)
        if not znal:
            self.wyslane += 1
            return True, tekst, []

        if self.tryb == "blokuj":
            self.zablokowane += 1
            return False, "", znal

        if self.tryb == "anonimizuj":
            czysty = tekst
            for i, (dop, opis) in enumerate(znal):
                czysty = czysty.replace(dop, f"[{opis.upper().replace(' ','_')}_{i}]")
            self.wyslane += 1
            return True, czysty, znal

        # tryb 'pytaj'
        print(f"\n  ⚠️  WYSYŁKA POZA MASZYNĘ — wykryto {len(znal)} wrażliwych fragmentów:")
        for dop, opis in znal[:8]:
            print(f"      {opis}: {dop[:40]!r}")
        print(f"      tekst: {len(tekst)} znaków")
        if input("      wysłać? [t/N] ").strip().lower() in ("t", "tak", "y"):
            self.wyslane += 1
            return True, tekst, znal
        self.zablokowane += 1
        return False, "", znal

if __name__ == "__main__":
    g = Granica(tryb="anonimizuj")
    PROBKI = [
        ("C", "Jak działa dekodowanie spekulatywne w llama.cpp?"),
        ("B", "Faktura FV/2025/143 od ALFA sp. z o.o., NIP 1234567890, 1 476,50 zł."),
        ("B", "Błąd: KeyError 'brutto' w linii 42 pliku ekstraktor.py"),
        ("A", "Cokolwiek — klasa A nigdy nie wychodzi."),
    ]
    for klasa, t in PROBKI:
        ok, wyslac, znal = g.przepusc(t, klasa)
        print(f"\nklasa {klasa}: {t[:60]}")
        print(f"  → {'WYSYŁAM' if ok else 'BLOKUJĘ'}  ({len(znal)} znalezisk)")
        if ok and wyslac != t:
            print(f"  → po anonimizacji: {wyslac[:80]}")
    print(f"\nwysłane={g.wyslane} zablokowane={g.zablokowane}")
PYEOF

python3 $AGENT/granica.py
```

⚠️ **Pułapka P51 (nowa): filtr regexowy przepuści to, czego nie przewidziałeś.**
Nie ma kompletnego zbioru wzorców dla „danych wrażliwych". **Filtr to druga linia obrony.
Pierwsza to klasyfikacja na wejściu** (klasa A = nie wychodzi, bez wyjątków).

---

## 4. Wywołanie Claude — minimum, które musisz wiedzieć

```bash
python3 -m venv $VENVS/claude
$VENVS/claude/bin/pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

```bash
cat > $AGENT/klient_claude.py <<'PYEOF'
#!/usr/bin/env python3
"""Cienki klient Claude z filtrem granicy i licznikiem kosztow."""
import os, sys
import anthropic

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from granica import Granica

MODEL = "claude-opus-5"

# Ceny za milion tokenow (USD), stan na 2026-06
CENNIK = {
    "claude-opus-5":   {"wej": 5.00, "wyj": 25.00},
    "claude-sonnet-5": {"wej": 3.00, "wyj": 15.00},
    "claude-haiku-4-5":{"wej": 1.00, "wyj":  5.00},
}

class Konsultant:
    def __init__(self, model: str = MODEL, tryb_granicy: str = "pytaj"):
        self.klient = anthropic.Anthropic()      # czyta ANTHROPIC_API_KEY
        self.model = model
        self.granica = Granica(tryb=tryb_granicy)
        self.koszt_usd = 0.0
        self.wywolan = 0

    def zapytaj(self, pytanie: str, kontekst: str = "", klasa: str = "A",
                system: str = "") -> str:
        # ⚠️ Domyslnie "A", NIE "C" - zgodnie z zasada z 1.1 ("wszystko jest
        # klasa A, dopoki jawnie nie zaklasyfikujesz inaczej"). Wczesniejsza
        # wersja tego pliku miala tu domyslnie "C" (najmniej bezpieczna opcja),
        # co przeczylo wlasnej zasadzie sekcji 1.1 - kazde wywolanie zapominajace
        # podac `klasa=` dostawaloby najszersze uprawnienia zamiast najwezszych.
        pelne = (kontekst + "\n\n" + pytanie).strip()
        ok, tekst, znal = self.granica.przepusc(pelne, klasa)
        if not ok:
            return (f"[ZABLOKOWANE PRZEZ GRANICĘ] Nie wysłano. "
                    f"Powód: {', '.join(o for _, o in znal[:3]) or 'klasa A'}. "
                    f"Rozwiąż to lokalnie.")

        kwargs = {
            "model": self.model,
            "max_tokens": 8000,
            "messages": [{"role": "user", "content": tekst}],
            # Mysl adaptacyjna jest domyslna na Opus 5; effort steruje glebokoscia
            "output_config": {"effort": "high"},
        }
        if system:
            # cache_control: prefiks systemowy tanieje ~10x przy powtorzeniach
            kwargs["system"] = [{"type": "text", "text": system,
                                 "cache_control": {"type": "ephemeral"}}]

        try:
            r = self.klient.messages.create(**kwargs)
        except anthropic.RateLimitError as e:
            return f"[LIMIT] {e}"
        except anthropic.APIConnectionError:
            return "[BRAK SIECI] Claude niedostępny — rozwiąż lokalnie."
        except anthropic.APIStatusError as e:
            return f"[BŁĄD API {e.status_code}] {e.message}"

        # Opus 5 moze odmowic - sprawdz PRZED czytaniem content
        if r.stop_reason == "refusal":
            kat = getattr(getattr(r, "stop_details", None), "category", None)
            return f"[ODMOWA MODELU] kategoria={kat}. Rozwiąż lokalnie."

        self._policz(r)
        return next((b.text for b in r.content if b.type == "text"), "(brak tekstu)")

    def _policz(self, r):
        c = CENNIK.get(self.model, CENNIK["claude-opus-5"])
        u = r.usage
        wej_pelne = getattr(u, "input_tokens", 0)
        wej_cache = getattr(u, "cache_read_input_tokens", 0) or 0
        wej_zapis = getattr(u, "cache_creation_input_tokens", 0) or 0
        wyj       = getattr(u, "output_tokens", 0)
        koszt = (wej_pelne * c["wej"]
                 + wej_cache * c["wej"] * 0.1        # odczyt z cache ~10% ceny
                 + wej_zapis * c["wej"] * 1.25       # zapis do cache ~125%
                 + wyj * c["wyj"]) / 1_000_000
        self.koszt_usd += koszt
        self.wywolan += 1
        print(f"      [claude] wej={wej_pelne} cache_r={wej_cache} wyj={wyj} "
              f"koszt={koszt:.4f} USD (łącznie {self.koszt_usd:.4f})", file=sys.stderr)

if __name__ == "__main__":
    k = Konsultant(tryb_granicy="pytaj")
    print(k.zapytaj(
        "Mam agenta z pętlą narzędziową na lokalnym modelu 20B. "
        "Model czasem powtarza to samo narzędzie w kółko. "
        "Jakie trzy mechanizmy wykrywania i przerywania takiej pętli polecasz?",
        klasa="C"))
    print(f"\nwywołań={k.wywolan} koszt={k.koszt_usd:.4f} USD")
PYEOF

$VENVS/claude/bin/python $AGENT/klient_claude.py
```

### 4.1 Pięć rzeczy, które musisz wiedzieć o tym API

| Rzecz | Dlaczego ważna |
| :-- | :-- |
| **brak `temperature`/`top_p`/`top_k`** | na Opus 5 zwracają **błąd 400** — sterujesz przez `effort` i prompt |
| **`thinking` domyślnie włączone** | Opus 5 myśli, jeśli nie wyłączysz; **`max_tokens` obejmuje myślenie + odpowiedź** |
| **`cache_control`** | prefiks systemowy tanieje ~10×; sprawdzaj `usage.cache_read_input_tokens` |
| **`stop_reason: "refusal"`** | ⭐ **sprawdzaj PRZED czytaniem `content`** — inaczej `IndexError` |
| **cache to dopasowanie prefiksu** | ta sama zasada co lokalnie (część 8 §2.4) — znacznik czasu w systemie zabija cache |

💡 **Zauważ, jak wiele z części 8 przenosi się 1:1.** Prompt cache, budżet tokenów,
zamrożony prefiks — te same mechanizmy, inny dostawca. **To nie przypadek: to są własności
transformerów, nie konkretnej implementacji.**

---

## 5. Router hybrydowy

Rozszerz `router.py` z części 8 §4 o trzecią opcję:

```bash
cat > $AGENT/router_hybrydowy.py <<'PYEOF'
#!/usr/bin/env python3
"""Router: lokalny maly -> lokalny duzy -> Claude (tylko klasa B/C)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MALY = "http://127.0.0.1:8081"
DUZY = "http://127.0.0.1:8082"

SYGNALY_CLAUDE = [
    r"(?i)\bzaprojektuj\s+(architektur|system)",
    r"(?i)\bzrefaktoryzuj\b.*\bwiele\b",
    r"(?i)\bdlaczego\b.*\bnie\s+dziala\b",
]

def klasa_danych(tekst: str) -> str:
    """Domyslnie A. Podnies do B/C tylko przy jawnych przeslankach."""
    if re.search(r"(?i)\b(faktur|umow|klient|nip|pesel|kwota|brutto|netto)\b", tekst):
        return "A"
    if re.search(r"(?i)\b(błąd|error|traceback|architektur|zaprojektuj|wyjaśnij)\b", tekst):
        return "B"
    return "A"          # ⭐ domyslnie NIE wychodzi

def wybierz(messages, bledy: int = 0, tura: int = 1, claude_dostepny: bool = False):
    """Zwraca ('lokalny'|'claude', cel, powod)."""
    ogon = " ".join(m["content"][:1500] for m in messages[-3:])
    klasa = klasa_danych(ogon)

    if claude_dostepny and klasa in ("B", "C"):
        if bledy >= 3:
            return "claude", None, f"{bledy} błędy pod rząd, dane klasy {klasa}"
        for s in SYGNALY_CLAUDE:
            if re.search(s, ogon):
                return "claude", None, f"zadanie strategiczne, dane klasy {klasa}"

    if bledy >= 2 or tura == 1:
        return "lokalny", DUZY, "planowanie / diagnoza lokalnie"
    if len(ogon) > 30000:
        return "lokalny", DUZY, "długi kontekst"
    return "lokalny", MALY, "rutyna"

if __name__ == "__main__":
    ma_klucz = bool(os.environ.get("ANTHROPIC_API_KEY"))
    print(f"Claude dostępny: {ma_klucz}\n")
    for tura, bledy, t in (
        (1, 0, "Przeczytaj plik vat.py."),
        (5, 0, "Wyciągnij dane z faktury FV/2025/143 na kwotę 1476,50 zł."),
        (8, 3, "Dlaczego ten import nie działa? Traceback: ModuleNotFoundError."),
        (2, 0, "Zaprojektuj architekturę modułu rozliczeń."),
    ):
        gdzie, cel, powod = wybierz([{"role": "user", "content": t}], bledy, tura, ma_klucz)
        etykieta = "CLAUDE" if gdzie == "claude" else ("lokalny-duży" if cel == DUZY else "lokalny-mały")
        print(f"[{klasa_danych(t)}] tura={tura} błędy={bledy}")
        print(f"     {t[:58]}")
        print(f"     → {etykieta}  ({powod})\n")
PYEOF

python3 $AGENT/router_hybrydowy.py
```

⭐ **Zwróć uwagę na `klasa_danych`: domyślnie zwraca `"A"`.** Treść z fakturą nigdy nie
trafi do Claude'a, nawet jeśli agent ma trzy błędy pod rząd. **To jest zabezpieczenie
domyślnie zamknięte.**

---

## 6. Offline-first — tryb awaryjny jest trybem podstawowym

⭐ **To jest najważniejsza zasada architektury hybrydowej.**

```
System MUSI działać w pełni bez Claude'a.
Claude jest ulepszeniem, nigdy zależnością.
```

**Test, który musisz przejść:**

```bash
# Odetnij Claude i uruchom pelny zestaw
unset ANTHROPIC_API_KEY
cd $AGENT && python3 pomiar-agenta.py

# Wynik MUSI byc porownywalny z czescia 8.
# Jesli agent nie dziala bez Claude'a - zbudowales produkt chmurowy
# i Twoja teza o suwerennosci danych jest nieprawdziwa.
```

⚠️ **Pułapka P52 (nowa): ciche uzależnienie od chmury.**
Dodajesz Claude'a „tylko do trudnych przypadków". Po miesiącu 40 % tur idzie przez API,
a agent bez sieci przestaje być użyteczny. **Mierz udział wywołań chmurowych i ustaw
twardy limit** — np. maks. 3 na zadanie.

```bash
# Dopisz licznik do konsultanta
cat >> $AGENT/klient_claude.py <<'PYEOF'

# ---------- twardy limit wywolan na zadanie ----------------------------
class KonsultantZLimitem(Konsultant):
    def __init__(self, *a, limit_na_zadanie: int = 3, limit_usd: float = 0.50, **kw):
        super().__init__(*a, **kw)
        self.limit = limit_na_zadanie
        self.limit_usd = limit_usd

    def zapytaj(self, *a, **kw) -> str:
        if self.wywolan >= self.limit:
            return (f"[LIMIT] Wykorzystano {self.limit} wywołań Claude na to zadanie. "
                    f"Dokończ lokalnie.")
        if self.koszt_usd >= self.limit_usd:
            return f"[LIMIT KOSZTU] {self.koszt_usd:.2f} USD. Dokończ lokalnie."
        return super().zapytaj(*a, **kw)
PYEOF
```

---

## 7. Ekonomia — policz, zanim zdecydujesz

```bash
python3 - <<'PYEOF'
# Szacunek miesieczny
ZADAN_DZIENNIE   = 50
TUR_NA_ZADANIE   = 12
UDZIAL_CLAUDE    = 0.10          # 10% tur
TOK_WEJ, TOK_WYJ = 8000, 1200
CENA_WEJ, CENA_WYJ = 5.00, 25.00   # Opus 5, USD/MTok
DNI = 22

tur_claude = ZADAN_DZIENNIE * TUR_NA_ZADANIE * UDZIAL_CLAUDE * DNI
koszt = tur_claude * (TOK_WEJ*CENA_WEJ + TOK_WYJ*CENA_WYJ) / 1_000_000
print(f"Wywołań Claude / miesiąc: {tur_claude:.0f}")
print(f"Koszt bez cache:          {koszt:8.2f} USD  (~{koszt*4:.0f} zł)")
print(f"Koszt z cache promptu:    {koszt*0.35:8.2f} USD  (~{koszt*0.35*4:.0f} zł)")
print()
print("Dla porownania — prad lokalny:")
kwh = 1.03 * 8 * DNI          # ~1030 W przez 8 h dziennie
print(f"  {kwh:.0f} kWh x 0,90 zł = {kwh*0.9:.0f} zł/mies.")
PYEOF
```

💡 **Wniosek, który zwykle wychodzi:** przy 10 % tur w chmurze koszt Claude'a jest
**porównywalny z rachunkiem za prąd**. To nie jest argument przeciw — to argument za
**świadomym limitem**. Przy 50 % tur proporcje się odwracają i Twoja przewaga kosztowa znika.

---

## 8. Ćwiczenia

1. **Przetestuj granicę na realnych danych.** Weź 20 prawdziwych fragmentów ze swoich
   dokumentów, przepuść przez `Granica` i policz, ile przeszłoby. **Każde przepuszczenie
   danych klienta to błąd krytyczny — dopisz brakujące wzorce.**
2. **Zmierz, czy Claude realnie pomaga.** Weź 10 zadań, na których lokalny agent zawiódł.
   Uruchom z Claude'em jako konsultantem. **Ile rozwiązał? Jaki był koszt na rozwiązane
   zadanie?**
3. **Test odcięcia.** Uruchom pełny zestaw bez `ANTHROPIC_API_KEY`. Wynik musi być
   porównywalny z częścią 8.
4. **Dodaj logowanie wyjścia.** Każde wywołanie Claude'a zapisuj do dziennika audytu
   z części 7: co wysłano, jakiej klasy, ile kosztowało. **To jest dowód zgodności dla
   klienta.**
5. **Zważ Sonnet 5 zamiast Opus 5.** Przy 3/15 USD zamiast 5/25 — zmierz, czy na Twoich
   zadaniach konsultacyjnych jakość spada. Często nie spada.

---

## Sprawdź się

- [ ] Jaka jest domyślna klasa danych i dlaczego akurat ta?
- [ ] Na czym polega wzorzec „Claude jako konsultant, nie wykonawca"?
- [ ] Dlaczego filtr regexowy jest drugą, a nie pierwszą linią obrony?
- [ ] Co trzeba sprawdzić przed odczytaniem `content` z odpowiedzi Opus 5?
- [ ] Dlaczego `temperature` nie działa na Opus 5?
- [ ] Które mechanizmy z części 8 przenoszą się 1:1 na Claude API?
- [ ] Jaki test musi przejść Twój system, żeby teza o suwerenności była prawdziwa?

## Nowe pułapki

| ID | Pułapka | § |
| :-- | :-- | :-- |
| **P51** | Filtr regexowy przepuści to, czego nie przewidziałeś | §3 |
| **P52** | Ciche uzależnienie od chmury — mierz udział i limituj | §6 |

---

## 🎓 Koniec kursu

Przeszedłeś drogę od „model to plik GGUF" do własnego, bezpiecznego, zoptymalizowanego
agenta działającego offline na Twoim sprzęcie.

**Co masz teraz:**

| | |
| :-- | :-- |
| `$KURS/` | narzędzia pomiarowe, RAG, zestawy ewaluacyjne |
| `$AGENT/` | ⭐ **własna pętla agenta** z piaskownicą, audytem i dziennikiem |
| `$NARZEDZIA/whisper.cpp/`, `$NARZEDZIA/piper/` | mowa wejściowa i wyjściowa |
| pułapki **P20–P52** | 33 udokumentowane pułapki programowe |

**Co dalej — w kolejności:**

1. **Zbuduj prawdziwy zestaw ewaluacyjny** na swoich realnych fakturach (50+ przypadków).
   Wszystko inne bez tego jest zgadywaniem.
2. **Uruchom agenta na prawdziwym zadaniu księgowym** i zapisz, gdzie zawodzi.
3. **Napraw harness, nie prompt** — to jest lekcja części 6.
4. **Dołóż karty 3 i 4** (`KARTY-3-I-4-PLAN-PODLACZENIA.md`) i uruchom `gpt-oss-120b`.
5. **Zmierz wszystko ponownie.**

⭐ **Najważniejsze, co wynosisz z tego kursu, to nie kod.** To jest umiejętność
odpowiedzenia na pytanie *„dlaczego to działa wolno / źle / niestabilnie"* — i wiedza,
której warstwy dotknąć. Reszta to szczegóły, które sprawdzisz w `--help`.
