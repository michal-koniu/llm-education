# Część 8 — Optymalizacja offline: zrób to szybko na własnym żelazie

**Poziom: ⭐⭐⭐⭐⭐** · Wymaga: części 2, 6, 7 · Czas: ~7 h

> **Po co ten rozdział.** Masz działającego, bezpiecznego agenta. Jest za wolny.
> Agent, który myśli 40 sekund na turę i potrzebuje 15 tur, to 10 minut na zadanie —
> nieużywalne.
>
> Ten rozdział to **pomiar i dźwignie**. Zaczynamy od zmierzenia, gdzie idzie czas, a potem
> po kolei: prompt cache, **dekodowanie spekulatywne** (masz już do tego model!), routing
> modeli, własna kwantyzacja, LoRA i plan na cztery karty.

```bash
cd ~/Desktop/github_repos/llm-education   # katalog repozytorium (u Ciebie może być inny)
source rig-env.sh
```

⚠️ **Jedna zasada na cały rozdział: NIE OPTYMALIZUJ BEZ POMIARU.**
Każda sekcja zaczyna się od liczby przed i kończy liczbą po. Bez tego to nie inżynieria,
a przesądy.

---

## Spis treści

| § | Dźwignia | Typowy zysk |
| :-- | :-- | --: |
| [1](#1-zmierz-najpierw--gdzie-idzie-czas) | **Pomiar bazowy** | — |
| [2](#2-prompt-cache-i-ponowne-użycie-kv) | **Prompt cache** | ⭐ **2–10×** na TTFT |
| [3](#3-dekodowanie-spekulatywne) | **Dekodowanie spekulatywne** | ⭐ **1,5–3×** na tok/s |
| [4](#4-routing-modeli--mały-do-łatwego) | **Routing modeli** | 2–5× na typowej turze |
| [5](#5-własna-kwantyzacja) | **Własna kwantyzacja** | pamięć + szybkość |
| [6](#6-lora--naucz-model-swojej-domeny) | **LoRA** | jakość bez większego modelu |
| [7](#7-równoległość-i-wsady) | **Równoległość** | przepustowość |
| [8](#8-plan-na-cztery-karty) | **Cztery karty** | pojemność, nie szybkość |
| [9](#9-tabela-decyzyjna) | **Podsumowanie** | co robić najpierw |

---

## 1. Zmierz najpierw — gdzie idzie czas

### 1.1 `llama-bench` — pomiar czysty

```bash
export HIP_VISIBLE_DEVICES=0,1
pkill -f llama-server; sleep 2

$LB/llama-bench -m $OSS20 -ngl 999 -p 512 -n 128 -r 3 -o md
```

Zobaczysz tabelę z dwiema kluczowymi kolumnami:

| Test | Co mierzy | Czym ograniczony |
| :-- | :-- | :-- |
| **`pp512`** | prefill 512 tokenów | moc obliczeniowa |
| **`tg128`** | generowanie 128 tokenów | przepustowość pamięci |

⭐ **`tg` (dekodowanie) to liczba, którą czuje użytkownik.** `pp` (prefill) prawie zawsze
jest szybki. Optymalizując, patrz na `tg` — i na TTFT (§2).

### 1.2 Porównaj wszystkie swoje modele

```bash
cat > $KURS/bench-wszystko.sh <<'EOF'
#!/usr/bin/env bash
source $LLMEDU/rig-env.sh
export HIP_VISIBLE_DEVICES=0,1
OUT=$KURS/bench-$(date +%Y%m%d-%H%M).md
echo "# Pomiar bazowy $(date)" > $OUT
echo "" >> $OUT
echo "llama.cpp: $(cd ~/llama.cpp && git log -1 --format='%h %ad' --date=short)" >> $OUT
echo "" >> $OUT

for M in "$OSS20" "$QWEN32" "$BIELIK"; do
  echo "## $(basename $M)" | tee -a $OUT
  $LB/llama-bench -m "$M" -ngl 999 -p 512 -n 128 -r 3 -o md 2>/dev/null | tee -a $OUT
  echo "" >> $OUT
  sleep 5
done
echo "Zapisano: $OUT"
EOF
chmod +x $KURS/bench-wszystko.sh
$KURS/bench-wszystko.sh
```

💡 **Zapisuj wyniki z datą i commitem llama.cpp.** Masz już do tego nawyk
(`results/all-benchmark-results.md`) — trzymaj się go. Za trzy miesiące będziesz chciał
wiedzieć, czy nowa wersja llama.cpp coś poprawiła.

### 1.3 Pomiar agenta — to jest metryka, która się liczy

`llama-bench` mierzy model. **Ty potrzebujesz zmierzyć agenta.**

```bash
cat > $AGENT/pomiar-agenta.py <<'PYEOF'
#!/usr/bin/env python3
"""Mierzy agenta na zestawie zadan. To jest metryka, ktora sie liczy."""
import json, os, statistics, subprocess, sys, time

ZADANIA = [
    "Wypisz pliki .py w katalogu roboczym.",
    "Napisz plik hello.py wypisujący 'czesc' i uruchom go.",
    "Policz, ile linii ma każdy plik .py w katalogu roboczym.",
    "W pliku hello.py zmień tekst na 'dzien dobry' i uruchom ponownie.",
    "Sprawdź, czy w katalogu jest plik vat.py; jeśli tak — podaj nazwy jego funkcji.",
]

def uruchom(zadanie: str) -> dict:
    t0 = time.time()
    r = subprocess.run([sys.executable, os.path.join(os.environ["AGENT"], "agent.py"),
                        zadanie, "--bez-zgod"],
                       capture_output=True, text=True, timeout=1200)
    dt = time.time() - t0
    # Znajdz dziennik z tego uruchomienia
    kat = os.path.join(os.environ["AGENT"], "dzienniki")
    pliki = sorted(os.listdir(kat)) if os.path.isdir(kat) else []
    tury = bledy = 0
    ms_modelu = []
    if pliki:
        for l in open(os.path.join(kat, pliki[-1]), encoding="utf-8"):
            try: rek = json.loads(l)
            except json.JSONDecodeError: continue
            if rek["typ"] == "krok":
                tury += 1
                if rek.get("ms"): ms_modelu.append(rek["ms"])
                if str(rek["wynik"]).startswith(("BŁĄD", "ODMOWA")): bledy += 1
    return {"sekundy": dt, "tury": tury, "bledy": bledy,
            "ms_modelu_suma": sum(ms_modelu),
            "udane": r.returncode == 0 and "Przerwano" not in r.stdout}

def main():
    wyniki = []
    for i, z in enumerate(ZADANIA, 1):
        print(f"[{i}/{len(ZADANIA)}] {z[:60]}...", flush=True)
        w = uruchom(z); wyniki.append(w)
        udzial = 100 * w["ms_modelu_suma"] / 1000 / w["sekundy"] if w["sekundy"] else 0
        print(f"      {w['sekundy']:6.1f}s  {w['tury']:2d} tur  {w['bledy']} błędów  "
              f"model={udzial:.0f}% czasu  {'✅' if w['udane'] else '❌'}")

    print(f"\n{'='*56}\nPODSUMOWANIE")
    print(f"  udanych:          {sum(w['udane'] for w in wyniki)}/{len(wyniki)}")
    print(f"  mediana czasu:    {statistics.median(w['sekundy'] for w in wyniki):.1f}s")
    print(f"  mediana tur:      {statistics.median(w['tury'] for w in wyniki):.0f}")
    print(f"  błędów łącznie:   {sum(w['bledy'] for w in wyniki)}")
    calosc = sum(w['sekundy'] for w in wyniki)
    model  = sum(w['ms_modelu_suma'] for w in wyniki) / 1000
    print(f"  czas w modelu:    {model:.0f}s z {calosc:.0f}s = {100*model/calosc:.0f}%")
    print(f"\n  ⭐ To jest Twoja liczba bazowa. Zapisz ją.")

if __name__ == "__main__":
    main()
PYEOF

pkill -f llama-server; sleep 2
$LB/llama-server -m $OSS20 -ngl 999 -c 16384 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25
cd $AGENT && python3 pomiar-agenta.py | tee $AGENT/pomiar-bazowy.txt
```

⭐ **Zapisz „czas w modelu %".** Jeśli to 85 % — optymalizuj model (§2–§5). Jeśli 30 % —
Twój problem jest w liczbie tur, czyli w harnessie i prompcie, **nie w szybkości modelu**.
Ten jeden procent decyduje, którą połowę tego rozdziału w ogóle czytać.

---

## 2. Prompt cache i ponowne użycie KV

⭐ **Największa dźwignia dla agenta.** I najbardziej niedoceniana.

### 2.1 Dlaczego to działa tak dobrze u agenta

Przypomnij część 2 §5: prefill jest kosztowny, ale robisz go **raz na prompt**. Agent
w każdej turze wysyła:

```
[prompt systemowy: 1200 tok]  ← IDENTYCZNY za każdym razem
[historia: 3000 tok]          ← TYLKO ROŚNIE, początek się nie zmienia
[nowa obserwacja: 300 tok]    ← jedyne nowe
```

Bez cache'u model przelicza **4500 tokenów** za każdym razem. Z cache'em — **300**.

```
tura  1: prefill 1500 tok
tura  2: prefill 1800 tok   ← 1500 z cache, 300 nowych
tura  3: prefill 2100 tok   ← 1800 z cache, 300 nowych
...
tura 15: prefill 6000 tok   ← 5700 z cache, 300 nowych
```

### 2.2 Włącz to

```bash
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1

$LB/llama-server -m $OSS20 \
  -ngl 999 -c 32768 \
  --cache-reuse 256 \
  --slot-save-path $AGENT/kv-cache \
  -np 1 \
  --host 127.0.0.1 --port 8081 --no-warmup &
sleep 25
```

| Flaga | Co robi |
| :-- | :-- |
| **`--cache-reuse 256`** | ⭐ pozwala ponownie użyć fragmentów KV przez przesuwanie; `256` = minimalny blok |
| **`--slot-save-path`** | zapisuje KV-cache na dysk — **przeżywa restart serwera** |
| `-np 1` | jeden slot = maksymalny cache na sesję (patrz §7) |
| `--keep N` | ile tokenów początku zawsze zachować |

### 2.3 Zmierz zysk

```bash
cat > $KURS/zmierz-cache.py <<'PYEOF'
#!/usr/bin/env python3
"""Mierzy TTFT przy rosnacej historii - z cache i bez."""
import json, time, urllib.request

SRV = "http://127.0.0.1:8081"
SYSTEM = ("Jesteś agentem. " + "Masz narzędzia do pracy z plikami i powłoką. " * 40)

def tura(hist):
    t0 = time.time()
    req = urllib.request.Request(SRV + "/v1/chat/completions",
        data=json.dumps({"messages": hist, "max_tokens": 20,
                         "temperature": 0, "cache_prompt": True}).encode(),
        headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    dt = time.time() - t0
    u = r.get("usage", {})
    return dt, u.get("prompt_tokens", 0), r["choices"][0]["message"]["content"]

hist = [{"role": "system", "content": SYSTEM}]
print(f"{'tura':>4}  {'tok promptu':>12}  {'czas':>8}  {'tok/s prefill':>14}")
for i in range(1, 11):
    hist.append({"role": "user", "content":
                 f"Krok {i}: przeczytaj plik nr {i} i podaj jego rozmiar. " * 6})
    dt, tok, odp = tura(hist)
    hist.append({"role": "assistant", "content": odp})
    print(f"{i:4d}  {tok:12d}  {dt:7.2f}s  {tok/dt:14.0f}")
print("\n⭐ Jesli cache dziala: czas zostaje PLASKI mimo rosnacej liczby tokenow.")
print("   Jesli rosnie liniowo - cache nie dziala; sprawdz --cache-reuse i cache_prompt.")
PYEOF

python3 $KURS/zmierz-cache.py
```

⭐ **Interpretacja:** kolumna `czas` powinna zostać **prawie płaska**, mimo że
`tok promptu` rośnie z 1500 do 6000. Jeśli rośnie liniowo — cache nie działa.

### 2.4 ⚠️ Co zabija cache — pułapka P46 (nowa)

Cache to **dopasowanie prefiksu**. Jedna zmiana na początku unieważnia wszystko dalej.

| Zabójca cache'u | Dlaczego | Naprawa |
| :-- | :-- | :-- |
| **znacznik czasu w prompcie systemowym** | prefiks inny za każdym razem | wstaw czas **na końcu**, w wiadomości `user` |
| **notatnik doklejany do `system`** | rośnie → prefiks się zmienia | ⚠️ patrz niżej |
| `json.dumps()` bez `sort_keys=True` | kolejność kluczy losowa | zawsze `sort_keys=True` |
| zmiana zestawu narzędzi w trakcie | narzędzia są na początku | ustal zestaw na start sesji |
| kompakcja historii | przepisuje środek | nieunikniona — cache odbuduje się po niej |

⚠️ **Konflikt, który sam sobie zrobiłeś w części 6.**
W `agent.py` przebudowujesz prompt systemowy przy każdej kompakcji, doklejając notatnik:

```python
hist[0] = {"role": "system", "content": self._prompt_systemowy()}  # ← zabija cache
```

**Naprawa:** trzymaj prompt systemowy **zamrożony**, a notatnik wstawiaj jako **osobną
wiadomość po historii**:

```bash
cd $AGENT && python3 - <<'PYEOF'
import os
p = os.path.join(os.environ["AGENT"], "agent.py")
s = open(p, encoding="utf-8").read()

# 1. Prompt systemowy bez notatnika = zamrozony prefiks
s = s.replace(
    '        notatki = self.notes.jako_tekst()\n'
    '        if notatki:\n'
    '            czesci += ["", notatki]\n'
    '        return "\\n".join(czesci)',
    '        return "\\n".join(czesci)   # BEZ notatnika — zamrozony prefiks (P46)')

# 2. Notatnik jako ostatnia wiadomosc przed pytaniem modelu
s = s.replace(
    '            try:\n                surowy, ms = self._zapytaj(hist)',
    '            notatki = self.notes.jako_tekst()\n'
    '            do_modelu = hist + ([{"role": "user", "content": notatki}] if notatki else [])\n'
    '            try:\n                surowy, ms = self._zapytaj(do_modelu)')

# 3. Kompakcja nie przebudowuje systemu
s = s.replace(
    '                hist[0] = {"role": "system", "content": self._prompt_systemowy()}\n', '')

open(p, "w", encoding="utf-8").write(s)
print("naprawiono: prompt systemowy zamrozony, notatnik na koncu")
PYEOF

# Zmierz ponownie
python3 $AGENT/pomiar-agenta.py | tee $AGENT/pomiar-po-cache.txt
diff <(grep mediana $AGENT/pomiar-bazowy.txt) <(grep mediana $AGENT/pomiar-po-cache.txt)
```

---

## 3. Dekodowanie spekulatywne

⭐ **Masz już do tego model.** `~/models/gpt-oss-120b/eagle3-gpt-oss-120b-Q8_0.gguf`,
849 MB — to jest **model szkicowy EAGLE3**.

### 3.1 Jak to działa

```
BEZ SPEKULACJI:
  duży model: token → token → token → token      (każdy = pełny przebieg)

ZE SPEKULACJĄ:
  mały model:  szkicuje 5 tokenów naprzód  (tanio, 849 MB)
  duży model:  sprawdza WSZYSTKIE 5 NARAZ  (jeden przebieg!)
               ├─ zgadzają się 4 → przyjmij 4, odrzuć 1
               └─ zgadza się 0   → przyjmij 1 (własny), strata minimalna
```

⭐ **Dlaczego to jest darmowy obiad.** Weryfikacja 5 tokenów naraz kosztuje tyle samo co
wygenerowanie jednego — bo to **prefill** (równoległy), a nie dekodowanie (sekwencyjne).
To jest bezpośrednie zastosowanie asymetrii z części 2 §5.

💡 **Kluczowe: wynik jest IDENTYCZNY** jak bez spekulacji (przy tym samym ziarnie).
To nie jest przybliżenie — model duży akceptuje token tylko wtedy, gdy sam by go wybrał.
**Zero kosztu jakościowego.**

### 3.2 Uruchom

⚠️ **Model szkicowy musi mieć ten sam tokenizer co główny.** `eagle3-gpt-oss-120b`
jest szkicem dla **gpt-oss** — użyj go z `gpt-oss-20b`, **nie z Qwenem ani Bielikiem**.
⚠️ `gpt-oss-120b` jako model docelowy **dziś się na tej maszynie nie mieści** (patrz
§8.1 niżej — 59 GiB wag przy 65 GiB VRAM to za mało miejsca na KV-cache) — to opcja
na PO rozbudowie do czterech kart, nie teraz.

```bash
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1

$LB/llama-server -m $OSS20 \
  -md $DRAFT \
  -ngl 999 -ngld 999 \
  -c 16384 \
  --spec-draft-n-max 5 \
  --spec-draft-n-min 1 \
  --spec-draft-p-min 0.75 \
  --cache-reuse 256 \
  --host 127.0.0.1 --port 8081 --no-warmup &
sleep 30
```

| Flaga | Znaczenie |
| :-- | :-- |
| **`-md`** (`--spec-draft-model`) | ścieżka do modelu szkicowego |
| `-ngld 999` | warstwy szkicu na GPU (osobno od `-ngl`) |
| **`--spec-draft-n-max 5`** | ile tokenów szkicować naprzód |
| `--spec-draft-n-min 1` | minimum |
| **`--spec-draft-p-min 0.75`** | szkicuj tylko, gdy szkic jest pewny ≥ 0,75 |

⚠️ **Stare flagi `--draft-max` / `--draft-min` zostały USUNIĘTE** w tej wersji.
Używaj `--spec-draft-n-max` / `--spec-draft-n-min`. Jeśli widzisz tutorial ze starymi —
jest nieaktualny.

### 3.3 Zmierz zysk

```bash
cat > $KURS/zmierz-spekulacje.py <<'PYEOF'
#!/usr/bin/env python3
"""Mierzy tok/s i wspolczynnik akceptacji szkicu."""
import json, urllib.request

SRV = "http://127.0.0.1:8081"
PROMPTY = [
    "Napisz funkcję w Pythonie liczącą kwotę brutto z netto i stawki VAT.",
    "Wyjaśnij w pięciu zdaniach, czym jest amortyzacja liniowa.",
    "Wypisz w punktach pięć elementów obowiązkowych faktury VAT.",
]

for p in PROMPTY:
    req = urllib.request.Request(SRV + "/v1/completions",
        data=json.dumps({"prompt": p, "max_tokens": 200, "temperature": 0}).encode(),
        headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    t = r.get("timings", {})
    print(f"\n{p[:56]}...")
    print(f"  dekodowanie: {t.get('predicted_per_second',0):7.1f} tok/s "
          f"({t.get('predicted_n',0)} tok w {t.get('predicted_ms',0):.0f} ms)")
    # llama-server raportuje statystyki szkicu, jesli sa dostepne
    for k in ("draft_n", "draft_n_accepted", "n_draft", "n_draft_accepted"):
        if k in t:
            print(f"  {k}: {t[k]}")
    if "draft_n" in t and t["draft_n"]:
        acc = 100 * t.get("draft_n_accepted", 0) / t["draft_n"]
        print(f"  akceptacja szkicu: {acc:.0f}%")
PYEOF

python3 $KURS/zmierz-spekulacje.py
```

Teraz porównaj **bez** szkicu:

```bash
pkill -f llama-server; sleep 3
$LB/llama-server -m $OSS20 -ngl 999 -c 16384 --cache-reuse 256 \
  --host 127.0.0.1 --port 8081 --no-warmup &
sleep 25
python3 $KURS/zmierz-spekulacje.py
```

### 3.4 Jak czytać współczynnik akceptacji

| Akceptacja | Co robić |
| :-- | :-- |
| **> 70 %** | ⭐ świetnie — **zwiększ `--spec-draft-n-max` do 8** |
| 40–70 % | dobrze, zostaw jak jest |
| 20–40 % | zmniejsz `n-max` do 3; podnieś `p-min` do 0,85 |
| **< 20 %** | szkic nie pasuje — **sprawdź, czy tokenizery są te same** |

💡 **Akceptacja zależy od treści.** Kod i tekst formalny mają wysoką (przewidywalne),
kreatywne pisanie niską. **Zmierz na swoich realnych promptach**, nie na przykładach.

### 3.5 ⚠️ Pułapka P47 (nowa): szkic zjada VRAM i może zwolnić

Model szkicowy trzyma **własne wagi i własny KV-cache**. Przy ciasnej pamięci:
1. zabiera miejsce głównemu modelowi → mniejszy kontekst,
2. przy niskiej akceptacji **spowalnia** (płacisz za szkic, nic nie zyskujesz).

**Zawsze zmierz obie konfiguracje.** 849 MB jest tanie, ale nie darmowe.

---

## 4. Routing modeli — mały do łatwego

Agent w części 6 używa jednego modelu do wszystkiego. **Większość tur to proste decyzje.**

### 4.1 Podział pracy

| Typ tury | Model | Dlaczego |
| :-- | :-- | :-- |
| wybór narzędzia (gramatyka wymusza format) | ⭐ **mały** | wybór z enuma — mały model wystarcza |
| streszczenie obserwacji | mały | zadanie mechaniczne |
| **plan wieloetapowy** | **duży** | tu potrzeba rozumowania |
| **diagnoza błędu** | **duży** | tu potrzeba rozumowania |
| finalna odpowiedź dla człowieka | duży | jakość języka widoczna |

```bash
cat > $AGENT/router.py <<'PYEOF'
#!/usr/bin/env python3
"""Routing miedzy dwoma serwerami modeli: maly (szybki) i duzy (madry)."""
import json, re, urllib.request

MALY = "http://127.0.0.1:8081"     # gpt-oss-20b
DUZY = "http://127.0.0.1:8082"     # qwen3-32b

# Sygnaly, ze potrzebny jest duzy model
SYGNALY_TRUDNE = [
    r"(?i)\bdlaczego\b", r"(?i)\bzdiagnozuj\b", r"(?i)\bzaprojektuj\b",
    r"(?i)\bporownaj\b", r"(?i)\bzaplanuj\b", r"(?i)\bwyjasnij\b",
    r"(?i)\bBŁĄD\b.*\bBŁĄD\b",          # wiele bledow w historii
]

def wybierz(messages: list[dict], ostatnie_bledy: int = 0,
            tura: int = 1) -> tuple[str, str]:
    """Zwraca (url, powod)."""
    if ostatnie_bledy >= 2:
        return DUZY, f"{ostatnie_bledy} błędy pod rząd — potrzebna diagnoza"
    if tura == 1:
        return DUZY, "pierwsza tura: planowanie"
    ogon = " ".join(m["content"][:1500] for m in messages[-3:])
    for s in SYGNALY_TRUDNE:
        if re.search(s, ogon):
            return DUZY, f"sygnał trudności: {s}"
    dlugosc = sum(len(m["content"]) for m in messages)
    if dlugosc > 40000:
        return DUZY, "długi kontekst — mały model gubi wątek"
    return MALY, "rutynowa tura"

def zapytaj(url: str, messages: list[dict], schema: dict | None = None,
            max_tokens: int = 900) -> str:
    body = {"messages": messages, "max_tokens": max_tokens,
            "temperature": 0, "repeat_penalty": 1.0, "cache_prompt": True}
    if schema:
        body["response_format"] = {"type": "json_schema", "json_schema": {"schema": schema}}
    req = urllib.request.Request(url + "/v1/chat/completions",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=600))
    return r["choices"][0]["message"]["content"]

def zywy(url: str) -> bool:
    try:
        urllib.request.urlopen(url + "/health", timeout=3); return True
    except Exception:
        return False

if __name__ == "__main__":
    for u, n in ((MALY, "mały"), (DUZY, "duży")):
        print(f"{n:6s} {u}  {'✅ żyje' if zywy(u) else '❌ brak'}")
    print()
    for tura, bledy, tresc in ((1, 0, "Napisz test."),
                               (5, 0, "Przeczytaj plik."),
                               (5, 0, "Dlaczego test nie przechodzi?"),
                               (7, 3, "Spróbuj jeszcze raz.")):
        url, powod = wybierz([{"role": "user", "content": tresc}], bledy, tura)
        print(f"tura={tura} błędy={bledy}  → {'DUŻY' if url == DUZY else 'mały'}  ({powod})")
PYEOF

# Uruchom dwa serwery jednoczesnie - oba zmieszcza sie w 65 GB
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1

$LB/llama-server -m $OSS20 -md $DRAFT -ngl 999 -ngld 999 -c 16384 \
  --spec-draft-n-max 5 --cache-reuse 256 \
  --host 127.0.0.1 --port 8081 --no-warmup &
sleep 28

$LB/llama-server -m $QWEN32 -ngl 999 -c 16384 --cache-reuse 256 \
  --host 127.0.0.1 --port 8082 --no-warmup &
sleep 40

python3 $AGENT/router.py
```

⚠️ **Pułapka P48 (nowa): routing unieważnia prompt cache.**
Każdy serwer ma **własny** KV-cache. Przeskok mały→duży = zimny prefill.
**Router musi być leniwy:** raz przeskoczysz na duży, **zostań tam do końca zadania**.
Nie przeskakuj tam i z powrotem co turę — zapłacisz za prefill więcej, niż zyskasz.

---

## 5. Własna kwantyzacja

Pobierasz gotowe `Q4_K_M`, bo ktoś je zrobił. **Możesz zrobić lepsze** — dopasowane do
Twojego języka i domeny.

### 5.1 Dlaczego własna kwantyzacja jest lepsza

Kwantyzacja „K" używa **macierzy istotności** (*importance matrix*): które wagi są ważne,
a które można zaokrąglić agresywniej. Macierz liczy się z **tekstu kalibracyjnego**.

⭐ **Publiczne kwanty są kalibrowane na angielskim.** Ty czytasz polskie faktury.
**Kalibracja na polskim tekście księgowym daje mierzalnie lepszy model przy tym samym
rozmiarze.**

### 5.2 Zbuduj tekst kalibracyjny

```bash
mkdir -p $KURS/kalibracja

# Zbierz swoj realny tekst domenowy
cat ~/Desktop/local_agents_project/lokalne/TECHNIKA.md \
    ~/Desktop/local_agents_project/lokalne/HANDOFF.md \
    $KURS/dokumenty/*.md \
    2>/dev/null > $KURS/kalibracja/domena.txt

# Dodaj polski tekst ksiegowy
cat >> $KURS/kalibracja/domena.txt <<'EOF'
Faktura VAT nr FV/2025/09/0143 z dnia 15 września 2025 roku.
Sprzedawca: Biuro Rachunkowe ALFA spółka z ograniczoną odpowiedzialnością.
Numer identyfikacji podatkowej NIP 1234567890.
Wartość netto 1 200,00 zł, podatek VAT 23% w kwocie 276,00 zł, brutto 1 476,00 zł.
Amortyzacja środków trwałych metodą liniową według stawki 20% rocznie.
Księga przychodów i rozchodów prowadzona jest w formie elektronicznej.
Deklaracja JPK_V7M składana jest do 25 dnia miesiąca następującego po okresie rozliczeniowym.
Zobowiązania krótkoterminowe obejmują kwoty wymagalne w okresie do dwunastu miesięcy.
Kapitał własny stanowi różnicę między aktywami a zobowiązaniami jednostki.
Rezerwy tworzy się na pewne lub prawdopodobne przyszłe zobowiązania.
Sprawozdanie finansowe składa się z bilansu, rachunku zysków i strat oraz informacji dodatkowej.
Faktura korygująca zmniejsza lub zwiększa podstawę opodatkowania podatkiem od towarów i usług.
EOF

# Powiel, zeby bylo dosc materialu (imatrix potrzebuje setek tysiecy tokenow)
for i in $(seq 1 12); do cat $KURS/kalibracja/domena.txt; done \
  > $KURS/kalibracja/pelny.txt
wc -c $KURS/kalibracja/pelny.txt
```

💡 **Im bardziej tekst kalibracyjny przypomina Twoje realne wejście, tym lepiej.**
Idealnie: wrzuć tu anonimizowane, prawdziwe dokumenty, z którymi agent będzie pracował.

### 5.3 Policz macierz istotności

⚠️ **`--in-file` to NIE jest flaga na tekst kalibracyjny** — sprawdzone przez `--help`. Ta flaga wczytuje **gotową, wcześniejszą** macierz `imatrix.gguf` (do łączenia kilku przebiegów), nie surowy tekst. Flaga na tekst to `-f`/`--file` — ta sama, której `llama-perplexity` używa gdzie indziej w tym rozdziale.

```bash
export HIP_VISIBLE_DEVICES=0,1
pkill -f llama-server; sleep 2

$LB/llama-imatrix \
  -m $QWEN32 \
  -f $KURS/kalibracja/pelny.txt \
  -o $KURS/kalibracja/qwen32-pl.imatrix.gguf \
  --output-format gguf \
  -ngl 999 -c 2048 \
  --chunks 100

ls -la $KURS/kalibracja/
```

⚠️ **To potrwa.** Kilkanaście–kilkadziesiąt minut zależnie od `--chunks`.
Zacznij od `--chunks 50`, żeby zobaczyć, że proces przechodzi.

### 5.4 Skwantyzuj

```bash
mkdir -p ~/models/wlasne

# UWAGA: llama-quantize dziala na modelu o WYZSZEJ precyzji.
# Qwen32 masz juz jako Q4_K_M - nie da sie z niego zrobic lepszego Q4.
# Do prawdziwego eksperymentu potrzebujesz F16/BF16. Tu pokazuje mechanike
# na przykladzie Q4_K_M -> Q3_K_M (schodzenie w dol dziala zawsze):

$LB/llama-quantize \
  --imatrix $KURS/kalibracja/qwen32-pl.imatrix.gguf \
  $QWEN32 \
  ~/models/wlasne/qwen32-Q3_K_M-pl.gguf \
  Q3_K_M

ls -lh ~/models/wlasne/
```

💡 **Żeby zrobić własne `Q4_K_M` lepsze od publicznego**, pobierz wersję `F16`
(lub `BF16`) modelu i kwantyzuj z niej. To duże pliki (32B w F16 ≈ 65 GB) — masz 1,5 TB,
więc możesz.

### 5.5 ⭐ Sprawdź, czy nie zepsułeś — PPL jako bramka jakości

```bash
# Tekst testowy MUSI byc INNY niz kalibracyjny!
cat > $KURS/kalibracja/test.txt <<'EOF'
Rozliczenie roczne podatku dochodowego od osób fizycznych składa się
w terminie do trzydziestego kwietnia roku następującego po roku podatkowym.
Koszty uzyskania przychodu obejmują wydatki poniesione w celu osiągnięcia
przychodów lub zachowania albo zabezpieczenia źródła przychodów.
Ewidencja środków trwałych zawiera datę przyjęcia do używania, wartość
początkową oraz stawkę amortyzacyjną.
Spis z natury przeprowadza się na koniec roku obrotowego.
EOF
for i in $(seq 1 30); do cat $KURS/kalibracja/test.txt; done > $KURS/kalibracja/test-duzy.txt

for M in $QWEN32 ~/models/wlasne/qwen32-Q3_K_M-pl.gguf; do
  echo "=== $(basename $M) ($(du -h $M | cut -f1))"
  $LB/llama-perplexity -m $M -f $KURS/kalibracja/test-duzy.txt \
    -ngl 999 -c 2048 2>&1 | grep -E 'Final estimate'
  sleep 3
done
```

⚠️ **Pułapka P49 (nowa): nie mierz PPL na tekście kalibracyjnym.**
Kwantyzacja była **dopasowana** do tego tekstu — wyjdzie sztucznie dobra. **Tekst testowy
musi być rozłączny z kalibracyjnym**, inaczej mierzysz sam siebie.

### 5.6 I przede wszystkim: zmierz zestawem z części 3

```bash
pkill -f llama-server; sleep 2
$LB/llama-server -m ~/models/wlasne/qwen32-Q3_K_M-pl.gguf \
  -ngl 999 -c 4096 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 30
python3 $KURS/eval/uruchom.py
```

⭐ **PPL to sito wstępne. Twój zestaw ewaluacyjny to prawdziwa miara.** Model może mieć
lepszą PPL i gorzej wyciągać kwoty — a to drugie jest tym, co sprzedajesz.

---

## 6. LoRA — naucz model swojej domeny

`llama-finetune` pozwala **dostroić model** na Twoich danych bez zmiany wag bazowych.

### 6.1 Kiedy LoRA ma sens, a kiedy nie

| ✅ LoRA pomoże | ❌ LoRA nie pomoże |
| :-- | :-- |
| model nie zna formatu Twoich dokumentów | model nie zna faktów → **użyj RAG (część 4)** |
| chcesz stały styl odpowiedzi | chcesz poprawnego JSON-a → **użyj gramatyk (część 3)** |
| terminologia branżowa jest gubiona | model jest po prostu za mały → **weź większy** |

⚠️ **LoRA to nie sposób dodawania wiedzy.** Do wiedzy jest RAG. LoRA zmienia **zachowanie
i styl**. Mieszanie tych dwóch to najczęstsze nieporozumienie.

### 6.2 Przygotuj dane treningowe

```bash
mkdir -p $KURS/lora

cat > $KURS/lora/dane.txt <<'EOF'
### Zadanie
Wyciągnij dane z faktury.

### Faktura
FV/2025/01/0001 z dnia 2025-01-10. Netto 1000,00 zł, VAT 23%, brutto 1230,00 zł.

### Odpowiedź
{"numer": "FV/2025/01/0001", "data": "2025-01-10", "netto": 1000.0, "vat_stawka": 23, "brutto": 1230.0}

### Zadanie
Wyciągnij dane z faktury.

### Faktura
Faktura nr 7/2025, data 2025-03-02, książki, netto 200 zł, VAT 5%, brutto 210 zł.

### Odpowiedź
{"numer": "7/2025", "data": "2025-03-02", "netto": 200.0, "vat_stawka": 5, "brutto": 210.0}

### Zadanie
Wyciągnij dane z faktury.

### Faktura
Rachunek A/12/2025 wystawiony 2025-06-30. Usługa zwolniona z VAT. Kwota 500,00 zł.

### Odpowiedź
{"numer": "A/12/2025", "data": "2025-06-30", "netto": 500.0, "vat_stawka": 0, "brutto": 500.0}
EOF

# Powiel - LoRA potrzebuje powtorzen
for i in $(seq 1 40); do cat $KURS/lora/dane.txt; echo; done > $KURS/lora/pelny.txt
wc -l $KURS/lora/pelny.txt
```

### 6.3 Trenuj

```bash
export HIP_VISIBLE_DEVICES=0,1
pkill -f llama-server; sleep 2

$LB/llama-finetune \
  -m $OSS20 \
  -f $KURS/lora/pelny.txt \
  -ngl 999 -c 2048 \
  --epochs 3 \
  -lr 1e-5 \
  -opt adamw \
  -wd 0.01 \
  2>&1 | tail -30

ls -la $KURS/lora/ *.gguf 2>/dev/null
```

⚠️ **`llama-finetune` w llama.cpp jest wciąż niedojrzałe** w porównaniu z `peft`/`torch`.
Traktuj to jako **ćwiczenie zrozumienia mechanizmu**, nie jako drogę produkcyjną.
Do poważnego dostrajania wrócimy w części 9 (`torchtune`, `unsloth`, `axolotl`).

### 6.4 Zastosuj adapter

```bash
# Z adapterem wczytywanym w czasie startu
$LB/llama-server -m $OSS20 \
  --lora $KURS/lora/adapter.gguf \
  -ngl 999 -c 16384 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

# Albo wtop adapter w model na stale
$LB/llama-export-lora \
  -m $OSS20 \
  --lora $KURS/lora/adapter.gguf \
  -o ~/models/wlasne/oss20-faktury.gguf
```

⭐ **Zmierz zestawem z części 3 przed i po.** Jeśli LoRA nie poprawia metryk — **odrzuć ją**.
Dodatkowa złożoność bez zysku to strata.

---

## 7. Równoległość i wsady

### 7.1 Sloty serwera

```bash
$LB/llama-server -m $OSS20 -ngl 999 -c 32768 -np 4 ... &
```

`-np 4` = cztery równoległe sesje. **Ale kontekst się dzieli:** `32768 / 4 = 8192` na slot.

| Konfiguracja | Kiedy |
| :-- | :-- |
| **`-np 1`, duże `-c`** | ⭐ **jeden agent** — maksymalny kontekst i cache |
| `-np 4`, mniejsze `-c` | kilku użytkowników albo subagenci równolegle |

⚠️ **Pułapka P50 (nowa): `-np` dzieli kontekst, nie mnoży wydajności.**
Dla jednego agenta `-np 1` jest **zawsze lepsze**: cały kontekst i cały cache dla niego.

### 7.2 MoE na CPU — sztuczka dla `qwen3-next-80b`

Twój `qwen3-next-80b` to model MoE (49,7 GB). Nowe flagi pozwalają **zostawić wagi
ekspertów na CPU**, a na GPU trzymać tylko warstwy gęste:

```bash
# Wszystkie wagi MoE na CPU
$LB/llama-server -m $QWEN80 -ngl 999 -cmoe -c 16384 \
  --host 127.0.0.1 --port 8081 --no-warmup &

# Albo tylko pierwszych N warstw
$LB/llama-server -m $QWEN80 -ngl 999 -ncmoe 20 -c 16384 \
  --host 127.0.0.1 --port 8081 --no-warmup &
```

💡 **Do czego to służy:** MoE czyta tylko część ekspertów na token. Trzymając ich na CPU,
zwalniasz VRAM na kontekst — **kosztem przepustowości**. Zmierz, czy się opłaca u Ciebie:

```bash
for FLAGI in "" "-cmoe" "-ncmoe 20"; do
  echo "=== flagi: ${FLAGI:-brak}"
  $LB/llama-bench -m $QWEN80 -ngl 999 $FLAGI -p 512 -n 128 -r 2 -o md 2>/dev/null | tail -4
  sleep 5
done
```

---

## 8. Plan na cztery karty

Karty 3 i 4 dadzą **127,4 GiB VRAM**. Zaplanuj to teraz.

### 8.1 ⚠️ Cztery karty NIE przyspieszą jednego zapytania

⭐ **To jest najważniejsze zdanie w tej sekcji.** Zmierzone u Ciebie: druga karta nie
przyspieszyła `gpt-oss-20b` (149,7 → 145,3 tok/s). Powód z części 2 §5: dekodowanie jest
ograniczone **przepustowością pamięci i sekwencyjnością**, nie mocą.

**Cztery karty dają POJEMNOŚĆ:**

| Model | Wagi | Zapełnienie 4 kart |
| :-- | --: | --: |
| `gpt-oss-120b` MXFP4 | 59,0 GiB | 46 % ✅ — **ten, który dziś nie działa** |
| Qwen3.5-122B-A10B Q4 | ~65 GiB | 51 % ✅ |
| Qwen3-235B-A22B UD-Q3 | ~97 GiB | 76 % ⚠️ |
| GLM-4.5-Air Q8 | ~102 GiB | 80 % ⚠️ za ciasno |

⚠️ **Reguła z porażki `gpt-oss-120b`: nie planuj zapełnienia VRAM powyżej ~80 % samymi
wagami.** Przy 7 % zapasu model wczytuje się, ale **nie liczy na GPU** — bufor obliczeniowy
ląduje w pamięci hosta.

### 8.2 ⛔ P2P musi zostać wyłączone

**Pułapka P4** z `TECHNIKA.md`: na konfiguracji 4 × R9700 transfery P2P **zawieszają cały
host** (ROCm #11348), i pod llama.cpp, i pod vLLM.

```bash
# OBOWIAZKOWE przy czterech kartach
export NCCL_P2P_DISABLE=1
export NCCL_PROTO=Simple
# GGML_CUDA_P2P: NIE USTAWIAJ

cat >> $LLMEDU/rig-env.sh <<'EOF'
# P4: P2P zawiesza host na 4x R9700
export NCCL_P2P_DISABLE=1
export NCCL_PROTO=Simple
EOF
```

### 8.3 Dwie architektury do wyboru

**Wariant A: jeden duży model na czterech kartach**

```bash
export HIP_VISIBLE_DEVICES=0,1,2,3   # PO przemapowaniu przez amd-smi list!
$LB/llama-server -m ~/models/gpt-oss-120b/gpt-oss-120b-MXFP4.gguf \
  -ngl 999 --split-mode layer -ts 1,1,1,1 \
  -c 32768 --cache-reuse 256 \
  --host 127.0.0.1 --port 8081 --no-warmup &
```

🔧 **`-ts 1,1,1,1`** to **proporcje**, nie gigabajty. `--split-mode row` jest wycofany —
używaj `layer`.

**Wariant B: ⭐ dwa modele po dwie karty — polecam dla agenta**

```bash
# Maly + szkic na kartach 0,1
HIP_VISIBLE_DEVICES=0,1 $LB/llama-server -m $OSS20 -md $DRAFT \
  -ngl 999 -ngld 999 -c 32768 --spec-draft-n-max 5 --cache-reuse 256 \
  --port 8081 --host 127.0.0.1 --no-warmup &

# Duzy na kartach 2,3
HIP_VISIBLE_DEVICES=2,3 $LB/llama-server -m $QWEN32 \
  -ngl 999 -c 32768 --cache-reuse 256 \
  --port 8082 --host 127.0.0.1 --no-warmup &
```

⭐ **Wariant B jest lepszy dla agenta.** Router (§4) dostaje **dwa gorące serwery** —
zero przeskoków na zimno, oba cache'e utrzymane. Wariant A ma sens tylko wtedy, gdy
naprawdę potrzebujesz modelu, który nie mieści się na dwóch kartach.

### 8.4 Po dołożeniu kart — obowiązkowa lista

```bash
# 1. Cztery karty widoczne?
lspci -d ::0300 | grep -c R9700          # oczekuj 4 (+ iGPU osobno)

# 2. P13: PRZEMAPUJ INDEKSY - numeracja sie zmienila!
amd-smi list

# 3. P15: szerokosc lacza na porcie NADRZEDNYM, nie na karcie
for BDF in $(lspci -d ::0300 | cut -d' ' -f1); do
  echo "=== $BDF"; sudo lspci -s $BDF -vv 2>/dev/null | grep -E 'LnkSta:' 
done

# 4. Limit mocy na WSZYSTKICH czterech
rocm-smi --showpower

# 5. AER = zero
sudo dmesg | grep -ci aer || echo "0 bledow AER ✅"

# 6. Pomiar bazowy od nowa
$KURS/bench-wszystko.sh
```

---

## 9. Tabela decyzyjna

⭐ **Kolejność, w jakiej stosować dźwignie** — od najlepszego stosunku zysku do wysiłku:

| # | Dźwignia | Zysk | Wysiłek | Ryzyko |
| --: | :-- | :-- | :-- | :-- |
| **1** | **`--cache-reuse` + zamrożony prompt** | ⭐⭐⭐⭐⭐ | niski | brak |
| **2** | **dekodowanie spekulatywne** (masz szkic!) | ⭐⭐⭐⭐ | niski | brak jakościowego |
| **3** | limit mocy 210 W (już masz) | — | — | — |
| 4 | `--cache-type-k/v q8_0` | ⭐⭐⭐ | niski | minimalna strata |
| 5 | routing modeli | ⭐⭐⭐ | średni | P48: zimny cache |
| 6 | mniej tur (lepszy harness/prompt) | ⭐⭐⭐⭐ | średni | brak |
| 7 | własna kwantyzacja | ⭐⭐ | wysoki | P49: zły pomiar |
| 8 | LoRA | ⭐⭐ | wysoki | może nie pomóc |
| 9 | 4 karty | pojemność | wysoki | P4, P13 |
| 10 | inny silnik (vLLM) | ⭐⭐⭐ | **wysoki** | część 9 |

### 9.1 Zmierz wszystko razem

```bash
# Konfiguracja docelowa
pkill -f llama-server; sleep 2
source $LLMEDU/rig-env.sh
export HIP_VISIBLE_DEVICES=0,1

$LB/llama-server -m $OSS20 \
  -md $DRAFT -ngl 999 -ngld 999 \
  -c 32768 -np 1 \
  --spec-draft-n-max 5 --spec-draft-p-min 0.75 \
  --cache-reuse 256 \
  --cache-type-k q8_0 --cache-type-v q8_0 \
  --slot-save-path $AGENT/kv-cache \
  --host 127.0.0.1 --port 8081 --no-warmup &
sleep 30

cd $AGENT && python3 pomiar-agenta.py | tee $AGENT/pomiar-koncowy.txt

echo "=== PRZED vs PO ==="
grep -E 'mediana|czas w modelu' $AGENT/pomiar-bazowy.txt
echo "---"
grep -E 'mediana|czas w modelu' $AGENT/pomiar-koncowy.txt
```

---

## Ćwiczenia

1. **Znajdź optymalne `--spec-draft-n-max`.** Przetestuj 3, 5, 8, 12 na swoich realnych
   promptach. Zapisz tok/s i akceptację. **Jest optimum — znajdź je.**
2. **Zmierz koszt kwantyzacji KV.** `f16` vs `q8_0` vs `q4_0`: zmierz VRAM, tok/s
   **i trafność zestawem z części 3**. Gdzie jakość zaczyna spadać?
3. **Zbuduj tabelę decyzyjną routingu dla swoich zadań.** Uruchom 20 realnych zadań na
   małym i dużym modelu. Które wymagały dużego? **Popraw regułę w `router.py`.**
4. **Własne `Q4_K_M` z polskiej kalibracji.** Pobierz `F16` Bielika (11B — ~22 GB),
   policz `imatrix` na polskim tekście księgowym, skwantyzuj i porównaj
   z publicznym `Q4_K_M`. **Zmierz PPL i zestaw ewaluacyjny.**
5. **Test wytrzymałości.** Uruchom agenta na 50 zadaniach pod rząd. Obserwuj VRAM
   (netdata), czy cache nie puchnie i czy nie ma wycieku. **To jest test przed produkcją.**

---

## Sprawdź się

- [ ] Która faza — prefill czy dekodowanie — jest wąskim gardłem i dlaczego?
- [ ] Dlaczego prompt cache jest największą dźwignią właśnie dla agenta?
- [ ] Co unieważnia prompt cache — pięć rzeczy?
- [ ] Dlaczego dekodowanie spekulatywne nie pogarsza jakości?
- [ ] Jaki współczynnik akceptacji szkicu jest dobry i co robić przy niskim?
- [ ] Dlaczego model szkicowy musi mieć ten sam tokenizer?
- [ ] Dlaczego router powinien być „leniwy"?
- [ ] Dlaczego PPL trzeba mierzyć na innym tekście niż kalibracyjny?
- [ ] Kiedy LoRA nie pomoże i czego wtedy użyć?
- [ ] Dlaczego `-np 1` jest lepsze dla jednego agenta?
- [ ] Co dadzą cztery karty, a czego nie dadzą?

## Nowe pułapki

| ID | Pułapka | § |
| :-- | :-- | :-- |
| **P46** | Zmienny prompt systemowy zabija prompt cache | §2.4 |
| **P47** | Model szkicowy zjada VRAM i przy niskiej akceptacji zwalnia | §3.5 |
| **P48** | Routing między serwerami unieważnia cache — bądź leniwy | §4.1 |
| **P49** | PPL mierzone na tekście kalibracyjnym jest sztucznie dobre | §5.5 |
| **P50** | `-np` dzieli kontekst, nie mnoży wydajności | §7.1 |

---

**Następna część: `09-KRAJOBRAZ-NARZEDZI.md`** — katalog narzędzi open source: alternatywne
silniki (vLLM, SGLang, ExLlama), interfejsy, bazy wektorowe, frameworki agentowe. Co jest
czym, co działa na RDNA4 i czego nie brać.
