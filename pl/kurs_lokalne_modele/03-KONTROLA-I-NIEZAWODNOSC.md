# Część 3 — Kontrola: jak zmusić lokalny model do posłuszeństwa

**Poziom: ⭐⭐⭐** · Wymaga: część 2 · Czas: ~5 h

> **Po co ten rozdział.** Lokalny model 20B jest głupszy od Claude'a i **będzie** psuł JSON,
> gubił nawiasy i dopisywał „Oto Twoja odpowiedź:" przed danymi. To nie jest problem do
> rozwiązania lepszym promptem. To jest problem do rozwiązania **na poziomie próbkowania**.
>
> Po tym rozdziale Twój model **nie może** zwrócić niepoprawnego JSON-a — nie „zwykle nie
> zwraca", ale **fizycznie nie jest w stanie**. To jest fundament, na którym w części 6 stoi
> cała pętla agenta.

```bash
cd ~/llm-education   # katalog repozytorium (u Ciebie może być inny)
source rig-env.sh
```

---

## Spis treści

| § | Temat | Kluczowa myśl |
| :-- | :-- | :-- |
| [1](#1-szablon-czatu--co-model-naprawdę-widzi) | **Szablon czatu** | „wiadomości" to iluzja; model widzi jeden ciąg znaków |
| [2](#2-gramatyki-gbnf--najważniejsze-narzędzie-w-tym-kursie) | **Gramatyki GBNF** | ⭐ ograniczasz próbkowanie, nie prosisz modelu |
| [3](#3-json-schema--gramatyka-bez-pisania-gramatyki) | **JSON Schema** | 90 % przypadków bez nauki GBNF |
| [4](#4-wywoływanie-narzędzi-niezawodnie) | **Narzędzia** | wymuszone gramatyką = zero zepsutych wywołań |
| [5](#5-determinizm-w-praktyce) | **Determinizm** | ustawienia dla ścieżek maszynowych |
| [6](#6-harness-ewaluacyjny--przestań-oceniać-na-czuja) | **Ewaluacja** | ⭐ bez tego nie wiesz, czy zmiana pomogła |
| [7](#7-ćwiczenie--ekstraktor-faktur-który-nie-może-się-zepsuć) | **Ćwiczenie** | ekstraktor + zestaw testowy + pomiar |

---

## 1. Szablon czatu — co model naprawdę widzi

W części 1 wysyłałeś `messages: [{role, content}]`. To jest **wygodna fikcja**. Model
dostaje **jeden płaski ciąg znaków**, a serwer buduje go z Twoich wiadomości według
**szablonu czatu zapisanego w pliku GGUF**.

### 1.1 Wyciągnij szablon z modelu

⚠️ **`llama-cli -n 0 | grep 'chat template'` nic nie znajdzie w tym builcie** — dokładnie
z tego samego powodu co w części 2, §1.4: ten build nie drukuje już zrzutu metadanych
przy starcie. Szablonu szukaj przez serwer (§1.2 niżej, endpoint `/apply-template`) —
to jest jedyna metoda, która realnie działa na tej maszynie.

### 1.2 Zobacz złożony prompt

Najprościej — poproś serwer, żeby pokazał, co wysyła:

Użyj endpointu `/apply-template` — jest w tym builcie i pokazuje wprost, co model
naprawdę dostaje, bez grzebania w logach:

```bash
pkill -f llama-server; sleep 2
$LB/llama-server -m $BIELIK -ngl 999 -c 4096 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

curl -s http://127.0.0.1:8081/apply-template -H "Content-Type: application/json" \
  -d '{"messages":[
        {"role":"system","content":"Jesteś księgowym."},
        {"role":"user","content":"Co to jest KPiR?"}]}' \
| python3 -c 'import json,sys; d=json.load(sys.stdin); print(repr(d.get("prompt", d)))'
```

Zobaczysz (sprawdzone na żywo — Bielik v3 używa **ChatML**, nie formatu Mistral `[INST]`,
jak można by się spodziewać po jego rodowodzie):

```
'<s><|im_start|>system\nJesteś księgowym.<|im_end|>\n<|im_start|>user\nCo to jest KPiR?<|im_end|>\n<|im_start|>assistant\n'
```

💡 **Ta rozbieżność jest pouczająca sama w sobie.** Model bazowy (Mistral) i model
dostrojony (Bielik) mogą używać **zupełnie innych szablonów rozmowy** — dziedziczenie
architektury nie znaczy dziedziczenia formatu czatu. Nie zgaduj formatu na podstawie
tego, „na czym model jest oparty" — sprawdzaj `/apply-template` za każdym razem, gdy
zmieniasz model.

albo z tokenami specjalnymi typu `<|im_start|>system`. **Każdy model ma inny szablon.**

### 1.3 Dlaczego to ma znaczenie — trzy realne awarie

| Awaria | Przyczyna |
| :-- | :-- |
| model odpowiada bez sensu, jakby nie rozumiał roli | zły szablon (np. wymuszony `--chat-template` niezgodny z modelem) |
| model dopisuje `<\|im_end\|>` do widocznej odpowiedzi | tokeny specjalne nie są poprawnie obsługiwane jako stop |
| model ignoruje `system` | niektóre modele **nie mają roli `system`** w szablonie — serwer wkleja ją do `user` |

⚠️ **Pułapka P25 (nowa): nie każdy model ma rolę `system`.**
Jeśli Twoje instrukcje systemowe są ignorowane — sprawdź szablon. W takim modelu instrukcję
trzeba wkleić na początek pierwszej wiadomości `user`.

### 1.4 Endpoint surowy vs czatowy — kiedy którego

| Endpoint | Co robi z szablonem | Kiedy używać |
| :-- | :-- | :-- |
| `/v1/chat/completions` | **stosuje** szablon modelu | normalna rozmowa, agent |
| `/v1/completions` | **nie stosuje** — wysyła Twój tekst dosłownie | gdy chcesz pełnej kontroli, jak w części 2 |

💡 **W części 6 (pętla agenta) użyjemy `/v1/chat/completions`**, bo szablon poprawnie
oddziela role i to poprawia jakość. Ale będziesz **wiedział**, że pod spodem jest jeden ciąg.

---

## 2. Gramatyki GBNF — najważniejsze narzędzie w tym kursie

### 2.1 Idea — i dlaczego jest genialna

Przypomnij sobie część 2 §3: przy każdym tokenie model daje rozkład nad całym słownikiem,
a Ty wybierasz jeden token.

**Gramatyka to filtr nałożony na ten rozkład.** Przed wyborem tokenu silnik pyta:
*„które z tych 128 000 tokenów są w tym miejscu gramatycznie dozwolone?"* — i **zeruje
prawdopodobieństwo wszystkich pozostałych.**

```
      rozkład (128 000 tokenów)
              │
              ▼
      ┌───────────────────────┐
      │   FILTR GRAMATYKI     │   ← tu odpada 127 990 tokenów
      │ "po { musi być \" "   │
      └───────────────────────┘
              │
              ▼
      wybierasz z 10 dozwolonych
```

💡 **To jest gwarancja twarda, nie prośba.** Model **nie może** wygenerować `{"kwota": abc}`,
jeśli gramatyka mówi, że po `"kwota":` musi być cyfra. Nie „prawdopodobnie nie wygeneruje" —
**nie ma takiej możliwości w przestrzeni wyboru.**

⭐ **To jest jedyny powód, dla którego lokalny model 20B może być fundamentem produktu.**
Bez gramatyk musiałbyś parsować, retryować i modlić się. Z gramatyką masz kontrakt.

### 2.2 Pierwsza gramatyka — tak/nie

```bash
mkdir -p $KURS/gramatyki

cat > $KURS/gramatyki/takNie.gbnf <<'EOF'
root ::= "tak" | "nie"
EOF

curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
  -d "$(python3 -c '
import json
g = open("'"$HOME"'/kurs/gramatyki/takNie.gbnf").read()
print(json.dumps({
  "prompt": "Czy faktura VAT musi zawierać NIP nabywcy? Odpowiedz jednym słowem.\nOdpowiedź:",
  "max_tokens": 5, "temperature": 0, "grammar": g
}))')" | python3 -c 'import json,sys; print(repr(json.load(sys.stdin)["choices"][0]["text"]))'
```

Wynik to **dokładnie** `tak` albo `nie`. Nic więcej. Żadnego „Tak, oczywiście — faktura…".

### 2.3 Składnia GBNF — wszystko, co potrzebujesz

```gbnf
# Komentarz

root      ::= regula                 # "root" to punkt wejscia (obowiazkowy)

literal   ::= "dokladny tekst"        # doslowny ciag
alternat  ::= "a" | "b" | "c"         # alternatywa (lub)
sekwencja ::= "a" "b" "c"             # po kolei
grupa     ::= ("a" | "b") "c"         # nawiasy grupuja

opcjonal  ::= "a"?                    # 0 lub 1
wiele     ::= "a"*                    # 0 lub wiecej
conajmn1  ::= "a"+                    # 1 lub wiecej

zakres    ::= [0-9]                   # klasa znakow
niezakres ::= [^"\\]                  # negacja klasy
```

⚠️ **Sprawdzone na żywo: reguła musi zmieścić się w jednej fizycznej linii.** Ten
parser (w tym builcie) odrzuca definicję rozbitą na wiele linii — nawet z ładnym
wcięciem, nawet z `\` na końcu jako kontynuacją. Serwer odpowiada wtedy
`400 "failed to parse grammar"`, bez wskazania która linia. Dla czytelności możesz
łamać **komentarze** i całe **osobne reguły** na różne linie — ale prawa strona
pojedynczej `nazwa ::= ...` musi być jednym ciągiem.

### 2.4 Gramatyka dla liczby — i dlaczego to takie ważne

```bash
cat > $KURS/gramatyki/kwota.gbnf <<'EOF'
# Kwota w zlotych: cyfry, opcjonalnie dwa miejsca po kropce
root   ::= liczba
liczba ::= [0-9]+ ("." [0-9] [0-9])?
EOF

for PYT in "Ile wynosi 1200 zł netto plus 23% VAT? Podaj tylko kwotę brutto." \
           "Jaka jest stawka VAT na książki w Polsce? Podaj tylko liczbę procent."; do
  echo "--- $PYT"
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d "$(python3 -c '
import json,sys
g=open("'"$HOME"'/kurs/gramatyki/kwota.gbnf").read()
print(json.dumps({"prompt": sys.argv[1] + "\nOdpowiedź:", "max_tokens": 15,
                  "temperature": 0, "grammar": g}))' "$PYT")" \
  | python3 -c 'import json,sys; print("    ->", repr(json.load(sys.stdin)["choices"][0]["text"]))'
done
```

⚠️ **Gramatyka gwarantuje FORMAT, nie PRAWDĘ.** Dostaniesz liczbę. Czy poprawną — to inna
sprawa (i do tego służy §6, ewaluacja). **Nie pomyl tych dwóch rzeczy** — to najczęstsze
nieporozumienie wokół structured output.

### 2.5 Gramatyka JSON — pełny przykład dla faktury

```bash
cat > $KURS/gramatyki/faktura.gbnf <<'EOF'
# Ekstrakcja danych faktury. Kolejnosc pol jest WYMUSZONA - to dobrze,
# bo model nie moze pominac pola ani zmienic kolejnosci.

root ::= "{" ws "\"numer\":" ws string ws "," ws "\"data\":" ws data ws "," ws "\"nip\":" ws nip ws "," ws "\"netto\":" ws kwota ws "," ws "\"vat_stawka\":" ws stawka ws "," ws "\"brutto\":" ws kwota ws "}"
# ⚠️ Cala prawa strona MUSI byc w jednej fizycznej linii - sprawdzone na zywo.
# Ten parser GBNF (w przeciwienstwie do niektorych innych wersji llama.cpp)
# NIE akceptuje reguly rozbitej na wiele linii, nawet z kontynuacja przez "\".
# Blad jest niemy dla czlowieka: serwer odpowiada 400 "failed to parse grammar"
# bez wskazania, ktora linia zawinila. Jesli Twoja gramatyka nagle przestaje
# dzialac po "kosmetycznym" zlamaniu dlugiej linii - to jest dokladnie ten trop.

string ::= "\"" znak* "\""
znak   ::= [^"\\] | "\\" ["\\/bfnrt]

# ISO: RRRR-MM-DD
data   ::= "\"" [0-9][0-9][0-9][0-9] "-" [0-9][0-9] "-" [0-9][0-9] "\""

# NIP: 10 cyfr
nip    ::= "\"" [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9] "\""

kwota  ::= [0-9]+ ("." [0-9][0-9])?

# Tylko realne polskie stawki
stawka ::= "0" | "5" | "8" | "23"

ws     ::= [ \t\n]*
EOF
```

Przetestuj:

```bash
python3 - <<'PYEOF'
import json, urllib.request, os

g = open(os.path.join(os.environ["KURS"], "gramatyki/faktura.gbnf")).read()

TEKST = """
FAKTURA VAT nr FV/2025/09/0143
Data wystawienia: 15 września 2025
Sprzedawca: Biuro Rachunkowe ALFA, NIP 1234567890
Usługa: prowadzenie księgowości za sierpień 2025
Wartość netto: 1 200,00 zł
VAT 23%: 276,00 zł
Do zapłaty: 1 476,00 zł
"""

prompt = f"Wyciągnij dane z faktury jako JSON.\n\n{TEKST}\n\nJSON:"
req = urllib.request.Request("http://127.0.0.1:8081/v1/completions",
    data=json.dumps({"prompt": prompt, "max_tokens": 300,
                     "temperature": 0, "grammar": g}).encode(),
    headers={"Content-Type": "application/json"})
out = json.load(urllib.request.urlopen(req, timeout=300))["choices"][0]["text"]

print("SUROWE:", out)
print()
d = json.loads(out)          # to sie NIE MOZE wywalic - gramatyka gwarantuje
print("SPARSOWANE:")
for k, v in d.items():
    print(f"  {k:12s} = {v!r}")

# Kontrola arytmetyki - gramatyka tego NIE sprawdza
netto  = float(d["netto"]); brutto = float(d["brutto"]); st = int(d["vat_stawka"])
oczek  = round(netto * (1 + st/100), 2)
print(f"\nnetto*{1+st/100} = {oczek}  vs brutto z modelu = {brutto}  "
      f"{'✅ zgodne' if abs(oczek-brutto) < 0.02 else '❌ NIEZGODNE'}")
PYEOF
```

💡 **Zwróć uwagę na ostatnie trzy linie.** Gramatyka dała Ci poprawny JSON z sensownymi
typami. **Poprawność arytmetyczną musisz sprawdzić sam, w kodzie.** To jest podział pracy,
który powtórzymy w całym kursie:

```
gramatyka  → gwarantuje STRUKTURĘ
kod        → sprawdza SPÓJNOŚĆ (arytmetyka, zakresy, słowniki)
ewaluacja  → mierzy TRAFNOŚĆ (§6)
```

### 2.6 Pułapki gramatyk

⚠️ **P26 (nowa): gramatyka może zapętlić model w nieskończoność.**
Jeśli gramatyka pozwala na `"a"*` bez warunku wyjścia, a model „chce" pisać dalej —
poleci do `max_tokens`. **Zawsze ustawiaj `max_tokens`** i zawsze testuj gramatykę na
wejściu, które jej nie pasuje.

⚠️ **P27 (nowa): gramatyka spowalnia generowanie.**
Filtrowanie 128 000 tokenów przy każdym kroku kosztuje. Spodziewaj się **10–30 % spadku
tok/s**. To najlepiej wydane 20 % w całym systemie — ale wiedz o tym, mierząc wydajność.

```bash
# Zmierz koszt gramatyki
for MODE in bez z; do
  if [ "$MODE" = "z" ]; then
    G=$(python3 -c 'import json,os;print(json.dumps(open(os.path.join(os.environ["KURS"], "gramatyki/kwota.gbnf")).read()))')
    EXTRA=",\"grammar\":$G"
  else
    EXTRA=""
  fi
  echo -n "$MODE gramatyki: "
  curl -s http://127.0.0.1:8081/v1/completions -H "Content-Type: application/json" \
    -d "{\"prompt\":\"Podaj liczbe: \",\"max_tokens\":60,\"temperature\":0$EXTRA}" \
  | python3 -c 'import json,sys; t=json.load(sys.stdin)["timings"]; print(f"{t.get(\"predicted_per_second\",0):.1f} tok/s")'
done
```

---

## 3. JSON Schema — gramatyka bez pisania gramatyki

Pisanie GBNF ręcznie jest pouczające, ale na co dzień niepraktyczne. `llama-server`
**sam konwertuje JSON Schema na gramatykę.**

```bash
python3 - <<'PYEOF'
import json, urllib.request

SCHEMA = {
  "type": "object",
  "properties": {
    "numer":      {"type": "string"},
    "data":       {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"},
    "netto":      {"type": "number"},
    "vat_stawka": {"type": "integer", "enum": [0, 5, 8, 23]},
    "brutto":     {"type": "number"},
    "pewnosc":    {"type": "string", "enum": ["wysoka", "srednia", "niska"]},
  },
  "required": ["numer", "data", "netto", "vat_stawka", "brutto", "pewnosc"],
}

TEKST = "Faktura FV/9/2025 z 2025-09-15, netto 1200 zl, VAT 23%, brutto 1476 zl"

req = urllib.request.Request("http://127.0.0.1:8081/v1/chat/completions",
    data=json.dumps({
        "messages": [
            {"role": "system", "content": "Wyciągasz dane z faktur. Jeśli czegoś nie ma w tekście — ustaw pewnosc na niska."},
            {"role": "user", "content": TEKST},
        ],
        "max_tokens": 300,
        "temperature": 0,
        "response_format": {"type": "json_schema", "json_schema": {"schema": SCHEMA}},
    }).encode(),
    headers={"Content-Type": "application/json"})

txt = json.load(urllib.request.urlopen(req, timeout=300))["choices"][0]["message"]["content"]
print(json.dumps(json.loads(txt), indent=2, ensure_ascii=False))
PYEOF
```

💡 **Pole `pewnosc` to wzorzec, który warto zapamiętać.** Wymuszasz na modelu, żeby
**zadeklarował własną niepewność jako pole danych**. Potem w kodzie: `if pewnosc == "niska":
do_weryfikacji_przez_czlowieka`. To jest tanie i skuteczne — i łączy się z odczytem logitów
z części 2 §2.2.

### 3.1 Czego JSON Schema w llama.cpp NIE wspiera

| Nieobsługiwane | Obejście |
| :-- | :-- |
| schematy rekurencyjne | spłaszcz strukturę |
| `minimum` / `maximum` | sprawdź w kodzie po sparsowaniu |
| `minLength` / `maxLength` | j.w. |
| złożone `oneOf` z dyskryminatorem | rozbij na dwa wywołania |

⚠️ **Nie zakładaj, że ograniczenie ze schematu zadziałało.** Jeśli nie jesteś pewien —
**sprawdź w kodzie**. Schemat to wygoda, kod to gwarancja.

---

## 4. Wywoływanie narzędzi niezawodnie

Część 1 §8 pokazała naiwne wywoływanie narzędzi. Teraz zrobimy to **tak, żeby nie mogło się
zepsuć** — i to jest bezpośredni fundament części 6.

```bash
cat > $KURS/narzedzia-schema.py <<'PYEOF'
#!/usr/bin/env python3
"""Wywolywanie narzedzi wymuszone schematem - zero zepsutych wywolan.

Model NIE MOZE zwrocic nieprawidlowej nazwy narzedzia ani zlego typu argumentu.
"""
import json, urllib.request

SERVER = "http://127.0.0.1:8081"

# --- Definicje narzedzi: nazwa -> (opis, schemat_argumentow, funkcja) -------
def _czytaj_plik(sciezka: str) -> str:
    import os
    p = os.path.realpath(os.path.expanduser(os.path.expandvars(sciezka)))
    root = os.path.realpath(os.environ["KURS"])
    if not p.startswith(root + os.sep) and p != root:
        return f"ODMOWA: sciezka poza {root}"
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read()[:2000]
    except OSError as e:
        return f"BLAD: {e}"

def _policz(wyrazenie: str) -> str:
    # Tylko arytmetyka - zadnego eval() na surowym wejsciu modelu
    import re
    if not re.fullmatch(r"[0-9\.\+\-\*/\(\) ]+", wyrazenie):
        return "ODMOWA: dozwolone tylko cyfry i + - * / ( )"
    try:
        return str(eval(wyrazenie, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"BLAD: {e}"

NARZEDZIA = {
    "czytaj_plik": {
        "opis": "Czyta plik tekstowy z katalogu $KURS. Zwraca do 2000 znakow.",
        "args": {"sciezka": {"type": "string"}},
        "fn": _czytaj_plik,
    },
    "policz": {
        "opis": "Liczy wyrazenie arytmetyczne. Tylko cyfry i operatory + - * / ( ).",
        "args": {"wyrazenie": {"type": "string"}},
        "fn": _policz,
    },
    "odpowiedz": {
        "opis": "Konczy prace i podaje ostateczna odpowiedz uzytkownikowi.",
        "args": {"tresc": {"type": "string"}},
        "fn": None,   # obslugiwane w petli
    },
}

def schemat_wywolania() -> dict:
    """Buduje JSON Schema wymuszajacy poprawne wywolanie narzedzia.

    Klucz: "enum" na nazwie narzedzia. Model NIE MOZE wymyslic nazwy.
    """
    return {
        "type": "object",
        "properties": {
            "mysl":      {"type": "string"},
            "narzedzie": {"type": "string", "enum": list(NARZEDZIA)},
            "argumenty": {"type": "object"},
        },
        "required": ["mysl", "narzedzie", "argumenty"],
    }

def opis_narzedzi() -> str:
    linie = []
    for nazwa, meta in NARZEDZIA.items():
        args = ", ".join(f"{k}: {v['type']}" for k, v in meta["args"].items())
        linie.append(f"- {nazwa}({args}) — {meta['opis']}")
    return "\n".join(linie)

def zapytaj(messages, schema):
    req = urllib.request.Request(SERVER + "/v1/chat/completions",
        data=json.dumps({
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0,            # <-- determinizm dla sciezki maszynowej
            "repeat_penalty": 1.0,       # <-- P21: kara psuje JSON
            "response_format": {"type": "json_schema", "json_schema": {"schema": schema}},
        }).encode(), headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    return r["choices"][0]["message"]["content"]

if __name__ == "__main__":
    import sys
    zadanie = sys.argv[1] if len(sys.argv) > 1 else \
        "Policz, ile wynosi 1200 zlotych netto po dodaniu 23 procent VAT."

    SYSTEM = (
        "Jesteś agentem. W każdej turze wybierasz DOKŁADNIE JEDNO narzędzie.\n"
        "Dostępne narzędzia:\n" + opis_narzedzi() + "\n\n"
        "Pole 'mysl' to jedno zdanie uzasadnienia. Gdy masz odpowiedź — użyj 'odpowiedz'."
    )
    msgs = [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": zadanie}]

    for tura in range(1, 7):
        raw = zapytaj(msgs, schemat_wywolania())
        krok = json.loads(raw)          # gwarantowane przez schemat
        nazwa = krok["narzedzie"]
        args  = krok["argumenty"]
        print(f"\n[tura {tura}] mysl: {krok['mysl']}")
        print(f"          -> {nazwa}({args})")

        if nazwa == "odpowiedz":
            print(f"\n=== ODPOWIEDZ ===\n{args.get('tresc','(brak)')}")
            break

        meta = NARZEDZIA[nazwa]          # bezpieczne: enum gwarantuje istnienie
        brakuje = [k for k in meta["args"] if k not in args]
        wynik = (f"BLAD: brakuje argumentow {brakuje}" if brakuje
                 else meta["fn"](**{k: args[k] for k in meta["args"]}))
        print(f"          <- {str(wynik)[:200]}")

        msgs.append({"role": "assistant", "content": raw})
        msgs.append({"role": "user", "content": f"Wynik narzędzia {nazwa}: {wynik}"})
    else:
        print("\n[przerwano: limit tur]")
PYEOF
chmod +x $KURS/narzedzia-schema.py

cd $KURS && python3 narzedzia-schema.py
```

### 4.1 Co dokładnie zabezpieczyliśmy

| Zagrożenie | Obrona |
| :-- | :-- |
| model wymyśla nieistniejące narzędzie | `"enum": list(NARZEDZIA)` — **niemożliwe** |
| model zwraca zepsuty JSON | `response_format` — **niemożliwe** |
| model gubi wymagany klucz | `"required"` + kontrola `brakuje` w kodzie |
| `repeat_penalty` psuje nawiasy | ustawione na `1.0` (**P21**) |
| model czyta `/etc/passwd` | kontrola `realpath` wewnątrz `czytaj_plik` |
| model wykonuje `eval("os.system(...)")` | biała lista znaków w `policz` |
| nieskończona pętla | twardy limit `range(1, 7)` |

⚠️ **To NIE jest jeszcze bezpieczne.** Kontrole są w funkcjach narzędzi — czyli
w tym samym procesie co pętla. W **części 7** wsadzimy narzędzia w `bwrap` i dopiero wtedy
będzie to obronne. Na razie to jest *poprawne*, nie *bezpieczne*.

---

## 5. Determinizm w praktyce

Dwa profile ustawień. Naucz się ich na pamięć.

### 5.1 Profil MASZYNOWY — narzędzia, ekstrakcja, klasyfikacja

```json
{
  "temperature": 0,
  "top_k": 1,
  "repeat_penalty": 1.0,
  "seed": 42,
  "response_format": { "type": "json_schema", "json_schema": { "schema": "..." } }
}
```

### 5.2 Profil ROZMOWNY — pisanie, wyjaśnianie, streszczenia

```json
{
  "temperature": 0.7,
  "min_p": 0.05,
  "repeat_penalty": 1.1,
  "seed": -1
}
```

⚠️ **Pułapka P28 (nowa): jeden profil dla całego agenta to błąd.**
Agent w jednej turze wywołuje narzędzie (potrzebuje profilu maszynowego), a w następnej pisze
podsumowanie dla człowieka (potrzebuje rozmownego). **Przełączaj profil per wywołanie**,
nie per serwer. W części 6 zbudujemy to jako dwie funkcje: `zapytaj_maszynowo()`
i `zapytaj_rozmownie()`.

---

## 6. Harness ewaluacyjny — przestań oceniać „na czuja"

⭐ **To jest drugi najważniejszy fragment tego rozdziału, obok gramatyk.**

Bez zestawu ewaluacyjnego każda Twoja zmiana (inny model, inny prompt, inna kwantyzacja)
jest zgadywaniem. Z zestawem — jest pomiarem.

### 6.1 Zbuduj zestaw testowy

```bash
mkdir -p $KURS/eval
cat > $KURS/eval/faktury.jsonl <<'EOF'
{"id":"f1","tekst":"FV/2025/01/0001 z dnia 2025-01-10. Netto 1000,00 zł, VAT 23%, brutto 1230,00 zł.","oczek":{"numer":"FV/2025/01/0001","data":"2025-01-10","netto":1000.0,"vat_stawka":23,"brutto":1230.0}}
{"id":"f2","tekst":"Faktura nr 7/2025, data 2025-03-02, książki, netto 200 zł, VAT 5%, brutto 210 zł.","oczek":{"numer":"7/2025","data":"2025-03-02","netto":200.0,"vat_stawka":5,"brutto":210.0}}
{"id":"f3","tekst":"Rachunek A/12/2025 wystawiony 2025-06-30. Usługa zwolniona z VAT. Kwota 500,00 zł.","oczek":{"numer":"A/12/2025","data":"2025-06-30","netto":500.0,"vat_stawka":0,"brutto":500.0}}
{"id":"f4","tekst":"FV 99/2025 z 2025-12-01, usługi budowlane, netto 10 000,00 zł, VAT 8%, brutto 10 800,00 zł.","oczek":{"numer":"99/2025","data":"2025-12-01","netto":10000.0,"vat_stawka":8,"brutto":10800.0}}
{"id":"f5","tekst":"Faktura FV/2025/44 z 2025-08-15. Netto 3 333,33 zł, VAT 23%, brutto 4 100,00 zł.","oczek":{"numer":"FV/2025/44","data":"2025-08-15","netto":3333.33,"vat_stawka":23,"brutto":4100.00}}
EOF
wc -l $KURS/eval/faktury.jsonl
```

💡 **Pięć przypadków to za mało na produkcję, ale wystarczy, by zacząć mierzyć.**
Rozbudowuj zestaw **za każdym razem, gdy zobaczysz nowy błąd** — to jest najlepiej wydany
czas w całym projekcie. Dodawaj przypadki trudne: stawka 0, kwoty z groszami, spacje
w liczbach, daty słowne.

### 6.2 Harness

```bash
cat > $KURS/eval/uruchom.py <<'PYEOF'
#!/usr/bin/env python3
"""Harness ewaluacyjny: mierzy trafnosc ekstrakcji pole po polu.

Uzycie:
  python3 uruchom.py                      # domyslny serwer 8081
  python3 uruchom.py http://127.0.0.1:8082
"""
import json, os, sys, time, urllib.request

SERVER = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8081"
ZBIOR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "faktury.jsonl")

SCHEMA = {
    "type": "object",
    "properties": {
        "numer":      {"type": "string"},
        "data":       {"type": "string"},
        "netto":      {"type": "number"},
        "vat_stawka": {"type": "integer", "enum": [0, 5, 8, 23]},
        "brutto":     {"type": "number"},
    },
    "required": ["numer", "data", "netto", "vat_stawka", "brutto"],
}

SYSTEM = ("Wyciągasz dane z polskich faktur. Kwoty jako liczby bez spacji i bez waluty. "
          "Daty w formacie RRRR-MM-DD. Stawka VAT jako liczba całkowita. "
          "Usługa zwolniona z VAT = stawka 0.")

def wyciagnij(tekst: str) -> tuple[dict | None, float]:
    body = {
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user",   "content": tekst}],
        "max_tokens": 300, "temperature": 0, "repeat_penalty": 1.0, "seed": 42,
        "response_format": {"type": "json_schema", "json_schema": {"schema": SCHEMA}},
    }
    req = urllib.request.Request(SERVER + "/v1/chat/completions",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        r = json.load(urllib.request.urlopen(req, timeout=300))
        dt = time.time() - t0
        return json.loads(r["choices"][0]["message"]["content"]), dt
    except Exception as e:
        print(f"    BLAD: {e}")
        return None, time.time() - t0

def rowne(pole, a, b) -> bool:
    """Porownanie tolerancyjne: liczby z groszem, tekst po normalizacji bialych znakow."""
    if a is None or b is None:
        return False
    if isinstance(b, float):
        try: return abs(float(a) - b) < 0.02
        except (TypeError, ValueError): return False
    if isinstance(b, int):
        try: return int(a) == b
        except (TypeError, ValueError): return False
    return str(a).strip().replace(" ", "") == str(b).strip().replace(" ", "")

def main():
    przypadki = [json.loads(l) for l in open(ZBIOR, encoding="utf-8") if l.strip()]
    pola = ["numer", "data", "netto", "vat_stawka", "brutto"]
    trafne = {p: 0 for p in pola}
    pelne, czasy, bledy = 0, [], []

    print(f"Serwer: {SERVER}")
    print(f"Przypadkow: {len(przypadki)}\n")

    for p in przypadki:
        got, dt = wyciagnij(p["tekst"])
        czasy.append(dt)
        if got is None:
            bledy.append((p["id"], "brak odpowiedzi")); print(f"  {p['id']}: ❌ brak"); continue

        ok_pola = [pole for pole in pola if rowne(pole, got.get(pole), p["oczek"][pole])]
        for pole in ok_pola:
            trafne[pole] += 1
        if len(ok_pola) == len(pola):
            pelne += 1
            print(f"  {p['id']}: ✅ wszystkie pola  ({dt:.1f}s)")
        else:
            zle = [pole for pole in pola if pole not in ok_pola]
            print(f"  {p['id']}: ⚠️  zle pola {zle}  ({dt:.1f}s)")
            for pole in zle:
                print(f"        {pole}: oczek={p['oczek'][pole]!r}  got={got.get(pole)!r}")
                bledy.append((p["id"], pole))

    n = len(przypadki)
    print(f"\n{'='*58}\nWYNIK")
    print(f"  pelna zgodnosc:  {pelne}/{n}  = {100*pelne/n:.0f}%")
    for pole in pola:
        print(f"  {pole:12s}   {trafne[pole]}/{n}  = {100*trafne[pole]/n:.0f}%")
    print(f"  sredni czas:     {sum(czasy)/len(czasy):.1f}s")
    if bledy:
        print(f"\n  do poprawy: {bledy}")

if __name__ == "__main__":
    main()
PYEOF
chmod +x $KURS/eval/uruchom.py
```

### 6.3 Uruchom i porównaj modele

```bash
# Bielik (Q8, polski)
pkill -f llama-server; sleep 2
$LB/llama-server -m $BIELIK -ngl 999 -c 4096 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25
python3 $KURS/eval/uruchom.py http://127.0.0.1:8081

# Qwen3-32B (Q4, wiekszy)
pkill -f llama-server; sleep 3
$LB/llama-server -m $QWEN32 -ngl 999 -c 4096 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 40
python3 $KURS/eval/uruchom.py http://127.0.0.1:8081

# gpt-oss-20b (szybki)
pkill -f llama-server; sleep 3
$LB/llama-server -m $OSS20 -ngl 999 -c 4096 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25
python3 $KURS/eval/uruchom.py http://127.0.0.1:8081
```

⭐ **Teraz masz liczby.** „Qwen jest lepszy" przestaje być opinią i staje się
`brutto: 5/5 vs 3/5`. **To jest moment, w którym przestajesz zgadywać, a zaczynasz
inżynierować.**

### 6.4 Zapisuj wyniki — historia pomiarów

```bash
mkdir -p $KURS/eval/wyniki
MODEL_NAZWA=bielik   # ⚠️ zmien na model, ktory WLASNIE testujesz (patrz 6.3) — bez tego
                     # kazdy zapis nadpisze poprzedni tą samą etykietą i pomiary sie zleją
python3 $KURS/eval/uruchom.py 2>&1 | tee $KURS/eval/wyniki/$(date +%Y%m%d-%H%M)-$MODEL_NAZWA.txt
```

💡 **Rób to za każdą zmianą.** Model, prompt, kwantyzacja, gramatyka — każda zmiana dostaje
plik z datą. Za miesiąc będziesz dokładnie wiedział, co pomogło. To jest dokładnie ta sama
dyscyplina, którą już masz w `results/all-benchmark-results.md` dla wydajności — tylko dla
jakości.

---

## 7. Ćwiczenie — ekstraktor faktur, który nie może się zepsuć

Złóż wszystko z tego rozdziału:

1. **Rozbuduj zestaw** `$KURS/eval/faktury.jsonl` do **15 przypadków**. Dodaj:
   - kwotę ze spacją jako separatorem tysięcy (`10 000,00`)
   - datę zapisaną słownie (`15 września 2025`)
   - fakturę bez numeru (co ma zrobić model? zdecyduj i zapisz w `oczek`)
   - dwie stawki VAT na jednej fakturze (to złamie Twój schemat — **to jest cel**)
2. **Uruchom harness** na trzech modelach. Zapisz wyniki.
3. **Wybierz najlepszy** i popraw prompt systemowy pod jego konkretne błędy.
4. **Zmierz ponownie.** Zapisz, o ile się poprawiło.
5. **Dodaj do schematu pole `pewnosc`** (§3) i sprawdź: czy model oznacza niską pewność
   tam, gdzie faktycznie się myli? Jeśli tak — masz gotowy mechanizm eskalacji do człowieka.

### 7.1 Kryterium sukcesu

```
pelna zgodnosc ≥ 80 %   na 15 przypadkach
pole "brutto"  = 100 %  (to pole, na którym nie wolno się mylić)
```

Jeśli nie osiągasz — **nie przechodź do części 4**. Wróć do promptu i schematu.
Agent zbudowany na niewiarygodnej ekstrakcji będzie niewiarygodny na każdym poziomie wyżej.

---

## Sprawdź się

- [ ] Co dokładnie widzi model, gdy wysyłasz `messages: [{role, content}]`?
- [ ] Jak gramatyka GBNF wpływa na rozkład prawdopodobieństwa z części 2?
- [ ] Dlaczego gramatyka gwarantuje format, ale nie prawdę?
- [ ] Dlaczego `repeat_penalty=1.1` psuje generowanie JSON-a?
- [ ] Jak uniemożliwić modelowi wymyślenie nieistniejącej nazwy narzędzia?
- [ ] Dlaczego jeden profil próbkowania dla całego agenta to błąd?
- [ ] Dlaczego bez zestawu ewaluacyjnego nie wiesz, czy zmiana promptu pomogła?

## Nowe pułapki

| ID | Pułapka | § |
| :-- | :-- | :-- |
| **P25** | Nie każdy model ma rolę `system` — instrukcje są cicho ignorowane | §1.3 |
| **P26** | Gramatyka bez warunku wyjścia zapętla generowanie do `max_tokens` | §2.6 |
| **P27** | Gramatyka kosztuje 10–30 % tok/s — uwzględnij w pomiarach | §2.6 |
| **P28** | Jeden profil próbkowania dla całego agenta — przełączaj per wywołanie | §5.2 |

---

**Następna część: `04-PAMIEC-RAG-I-KONTEKST.md`** — dajesz modelowi dostęp do dokumentów,
których nie widział w treningu. Baza wektorowa napisana od zera, w czystym Pythonie.
