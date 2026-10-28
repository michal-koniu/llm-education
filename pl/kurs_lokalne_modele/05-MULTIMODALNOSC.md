# Część 5 — Multimodalność: agent, który widzi, słyszy i mówi

**Poziom: ⭐⭐⭐⭐** · Wymaga: części 2–4 · Czas: ~6 h

> **Po co ten rozdział.** Agent, który tylko czyta tekst, jest kalendarzem. Agent, który
> **widzi skan faktury**, **słucha, jak dyktujesz**, i **odpowiada głosem** — to jest
> narzędzie pracy. Wszystko w tym rozdziale działa **całkowicie offline** na Twoim żelazie.
>
> Zaczynamy nisko: każda modalność to osobny model, osobny plik, osobne polecenie. Najpierw
> zrozumiesz każdy kawałek, potem połączysz je w jedną pętlę.

```bash
cd ~/llm-education   # katalog repozytorium (u Ciebie może być inny)
source rig-env.sh
```

---

## Spis treści

| § | Temat | Narzędzie |
| :-- | :-- | :-- |
| [1](#1-co-masz-a-czego-brakuje) | **Inwentarz** | co jest na maszynie, co dokupić |
| [2](#2-sprzęt--co-kupić-i-dlaczego) | **Sprzęt** | ⭐ lista zakupowa: mikrofon, kamera, głośnik |
| [3](#3-widzenie--model-który-czyta-obrazy) | **Widzenie** | `llama-mtmd-cli` + model VL |
| [4](#4-słuchanie--whispercpp-od-zera) | **Słuchanie** | `whisper.cpp` zbudowany na ROCm |
| [5](#5-mówienie--dwie-drogi) | **Mówienie** | `llama-tts` vs Piper |
| [6](#6-pełna-pętla-głosowa) | **Pętla głosowa** | mów → agent → słyszysz odpowiedź |
| [7](#7-ćwiczenie--asystent-który-czyta-skany-faktur) | **Ćwiczenie** | skan → dane → głos |

---

## 1. Co masz, a czego brakuje

Sprawdzone na Twojej maszynie 22 września 2026:

| Element | Stan | Uwaga |
| :-- | :-- | :-- |
| **`llama-mtmd-cli`** | ✅ **jest** | wizja + audio wejściowe, zbudowany |
| **`llama-tts`** | ✅ **jest** | synteza mowy, zbudowany |
| `libmtmd.so` | ✅ jest | biblioteka multimodalna |
| `arecord` / `aplay` | ✅ jest | ALSA — nagrywanie i odtwarzanie |
| `pw-cat` | ✅ jest | PipeWire — alternatywa dla ALSA |
| **wejście audio** | ✅ **jest** | `card 3: ALC1220 Analog` (wejście liniowe/mikrofonowe płyty) |
| **`whisper.cpp`** | ❌ **brak** | §4 — trzeba sklonować i zbudować |
| **modele VL (`mmproj`)** | ❌ **brak** | §3 — trzeba pobrać |
| kamera | ❌ brak `/dev/video*` | §2 — trzeba kupić |
| `ffmpeg`, `sox` | ❌ brak | §4.1 — `apt install` |
| Piper (TTS) | ❌ brak | §5.2 — opcjonalnie, ale polecam dla polskiego |

⚠️ **Pułapka P32 (nowa): iGPU jest teraz `GPU[2]`.**
`rocm-smi` pokazuje trzy urządzenia: `GPU[0]` i `GPU[1]` to karty R9700 (34,2 GB każda),
`GPU[2]` to **zintegrowana grafika z 2 GB**. Modele multimodalne są małe i **mogą omyłkowo
wylądować na iGPU** — wtedy działają, ale 50× wolniej. To jest pułapka **P12** w nowym
przebraniu. **Zawsze ustawiaj `HIP_VISIBLE_DEVICES=0,1`** dla zadań, które mają iść na karty:

```bash
export HIP_VISIBLE_DEVICES=0,1
echo 'export HIP_VISIBLE_DEVICES=0,1' >> $LLMEDU/rig-env.sh
```

⚠️ **Sprawdź to po dołożeniu kart 3 i 4** — numeracja zmieni się znowu (pułapka **P13**).

---

## 2. Sprzęt — co kupić i dlaczego

Masz wejście audio na płycie (`ALC1220`), ale **nie masz mikrofonu ani kamery**.

### 2.1 Mikrofon — najważniejszy zakup

| Opcja | Cena | Dlaczego |
| :-- | --: | :-- |
| ⭐ **USB mikrofon pojemnościowy** (Fifine K669B, Trust GXT 232) | 120–200 zł | **polecam na start.** USB = własna karta dźwiękowa, omija szum płyty. Wystarczający do dyktowania |
| **Zestaw słuchawkowy USB** (Logitech H390, Jabra Evolve) | 150–350 zł | ⭐ **lepszy do pętli głosowej** — mikrofon przy ustach, brak echa ze głośników |
| Mikrofon XLR + interfejs (Rode PodMic + Focusrite) | 900–1500 zł | jakość studyjna; **przesada** do STT |
| **Macierz mikrofonowa** (ReSpeaker 4-Mic Array, Anker PowerConf) | 350–700 zł | do sterowania głosem **z drugiego końca pokoju**; kupuj, gdy pętla głosowa już działa |

💡 **Kluczowa rada techniczna:** Whisper pracuje na **16 kHz mono**. Nie potrzebujesz
mikrofonu studyjnego — potrzebujesz **czystego sygnału bez szumu tła**. Zestaw słuchawkowy
USB za 200 zł da lepsze wyniki STT niż mikrofon pojemnościowy za 800 zł stojący metr od
wentylatorów czterech kart grafiki. **A maszyna z wieloma kartami jest głośna.**

⚠️ **To jest realny problem, nie teoria.** Cztery karty R9700 pod obciążeniem to solidny
szum. Mikrofon wszechkierunkowy na biurku nagra wentylatory i Whisper będzie halucynował.
**Bierz zestaw słuchawkowy albo mikrofon kierunkowy.**

### 2.2 Kamera

| Opcja | Cena | Do czego |
| :-- | --: | :-- |
| ⭐ **Logitech C920 / C922** | 250–400 zł | **polecam.** 1080p, świetne wsparcie w Linuksie (UVC, zero sterowników) |
| Logitech Brio 4K | 700–900 zł | 4K — przydatne, jeśli kamera ma **czytać dokumenty** |
| **Kamera dokumentowa / wizualizer** (IPEVO, Aver) | 600–1200 zł | ⭐ jeśli celem jest **skanowanie faktur na blacie** — ramię nad biurkiem, ostrość na papier |
| Kamera USB z autofokusem i makro | 200–300 zł | budżetowo do dokumentów |

💡 **Do czytania faktur kamera dokumentowa bije webcam.** Webcam jest zoptymalizowany pod
twarz w odległości 50 cm; dokument na biurku wychodzi krzywo i z odblaskami. Jeśli
multimodalność ma służyć **księgowości**, kamera na ramieniu jest właściwym narzędziem.

⚠️ **Sprawdź obsługę UVC przed zakupem.** Kamera „UVC-compatible" działa w Linuksie bez
sterowników. Wszystko inne to loteria.

### 2.3 Wyjście audio

Masz wyjście na płycie. Wystarczy. Jeśli chcesz dedykowane:

| Opcja | Cena |
| :-- | --: |
| Głośniki USB / aktywne na jack | 100–300 zł |
| DAC USB + słuchawki | 200–500 zł |

### 2.4 Minimalny zestaw startowy

```
Zestaw słuchawkowy USB (Logitech H390)   ~170 zł   ← mikrofon + głośnik w jednym
Kamera Logitech C920                      ~300 zł
─────────────────────────────────────────────────
RAZEM                                     ~470 zł
```

To wystarczy, żeby przejść **cały ten rozdział**. Kamerę dokumentową i macierz mikrofonową
dokupisz, gdy będziesz wiedział, że ich potrzebujesz.

### 2.5 Sprawdź sprzęt po podłączeniu

```bash
# Mikrofon widoczny?
arecord -l

# Nagraj 5 sekund testowo (podstaw wlasciwy numer karty)
arecord -D plughw:3,0 -f S16_LE -r 16000 -c 1 -d 5 $KURS/test-mic.wav
aplay $KURS/test-mic.wav

# Kamera widoczna?
ls -l /dev/video*
v4l2-ctl --list-devices 2>/dev/null || sudo apt install -y v4l-utils
```

🔧 **`-f S16_LE -r 16000 -c 1`** = 16-bit, 16 kHz, mono. **To jest dokładnie format,
którego chce Whisper** — nagrywaj tak od razu i nie będziesz musiał konwertować.

---

## 3. Widzenie — model, który czyta obrazy

### 3.1 Jak to działa pod spodem

Model językowy nie rozumie pikseli. Potrzebuje **tłumacza**:

```
   obraz JPEG
       │
       ▼
  ┌──────────────────────────┐
  │  ENKODER WIZYJNY (ViT)   │  plik mmproj.gguf
  │  obraz → siatka cech     │
  └──────────────────────────┘
       │
       ▼
  ┌──────────────────────────┐
  │  PROJEKTOR               │  też w mmproj.gguf
  │  cechy → "tokeny obrazu" │  ← w przestrzeni embeddingów modelu!
  └──────────────────────────┘
       │
       ▼
  wstawione w ciąg tokenów obok Twojego tekstu
       │
       ▼
  ┌──────────────────────────┐
  │  MODEL JĘZYKOWY          │  plik modelu .gguf
  └──────────────────────────┘
```

⭐ **Kluczowa intuicja:** obraz zostaje **zamieniony w tokeny** i wrzucony do tego samego
kontekstu co tekst. Dlatego:

| Fakt | Konsekwencja |
| :-- | :-- |
| obraz zajmuje **setki–tysiące tokenów** | jedno zdjęcie może zjeść ¼ kontekstu |
| większa rozdzielczość = więcej tokenów | skan A4 w 300 dpi to bardzo drogi obraz |
| **potrzebujesz DWÓCH plików** | model + `mmproj` — sam model nie widzi |

⚠️ **Pułapka P33 (nowa): `mmproj` musi pasować do modelu.**
`mmproj` z Qwen2.5-VL nie zadziała z Gemmą. To nie jest generyczny „dodatek wizyjny" —
to część konkretnego modelu. **Pobieraj oba pliki z tego samego repozytorium.**

### 3.2 Pobierz model wizyjny

Dla polskiego + czytania dokumentów polecam **Qwen2.5-VL-7B**:

```bash
mkdir -p ~/models/vl && cd ~/models/vl

# Model + projektor wizyjny - OBA pliki z tego samego repo
hf download ggml-org/Qwen2.5-VL-7B-Instruct-GGUF \
  Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf --local-dir .
hf download ggml-org/Qwen2.5-VL-7B-Instruct-GGUF \
  mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf --local-dir .

ls -la ~/models/vl/
```

```bash
export VL=~/models/vl/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf
export VLMM=~/models/vl/mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf
cat >> $LLMEDU/rig-env.sh <<'EOF'
export VL=~/models/vl/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf
export VLMM=~/models/vl/mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf
EOF
```

**Alternatywy warte uwagi:**

| Model | Rozmiar | Mocna strona |
| :-- | --: | :-- |
| **Qwen2.5-VL-7B** | ~5 GB | ⭐ najlepszy do **tekstu w obrazie** (OCR faktur), dobry polski |
| Gemma 3 12B (wizja) | ~8 GB | mocne rozumowanie o obrazie, słabszy OCR |
| MiniCPM-V 2.6 | ~5 GB | bardzo dobry stosunek jakość/rozmiar |
| InternVL2.5 | 4–26 GB | najmocniejszy na wykresach i tabelach |

⚠️ **Nie kwantyzuj `mmproj` poniżej `f16`.** Projektor to warstwa numeryczna; `Q4` na nim
psuje rozumienie obrazu drastycznie mocniej niż `Q4` na modelu językowym.

### 3.3 Pierwszy obraz

```bash
# Przygotuj obraz testowy: zrzut ekranu albo zdjecie
mkdir -p $KURS/obrazy
# Jesli masz kamere:
#   sudo apt install -y fswebcam && fswebcam -r 1280x720 $KURS/obrazy/test.jpg
# Albo skorzystaj z pliku, ktory juz masz (np. zdjecie plytki F43SG):
ls $KURS/obrazy/ 2>/dev/null || echo "wrzuc jakis .jpg do $KURS/obrazy/"

export HIP_VISIBLE_DEVICES=0,1

$LB/llama-mtmd-cli \
  -m $VL --mmproj $VLMM \
  -ngl 999 -c 8192 \
  --image $KURS/obrazy/test.jpg \
  -p "Opisz dokładnie, co widzisz na tym obrazie. Odpowiedz po polsku."
```

🔧 **Flagi:** `--mmproj` to projektor wizyjny, `--image` to plik obrazu (można podać
wielokrotnie dla kilku obrazów), `-c 8192` bo **obraz zjada dużo kontekstu**.

### 3.4 Zmierz, ile tokenów zjada obraz

```bash
for ROZM in 320 640 1280; do
  python3 - "$ROZM" <<'PYEOF'
import subprocess, sys, os
r = sys.argv[1]
src = os.path.join(os.environ["KURS"], "obrazy/test.jpg")
dst = os.path.expandvars(f"$KURS/obrazy/skala-{r}.jpg")
# Skalowanie przez Pythona (brak ffmpeg) - wymaga Pillow
try:
    from PIL import Image
    im = Image.open(src); im.thumbnail((int(r), int(r))); im.save(dst, quality=88)
    print(f"{r}px -> {dst} ({os.path.getsize(dst)//1024} KB)")
except ImportError:
    print("brak Pillow: python3 -m venv $VENVS/kurs && $VENVS/kurs/bin/pip install pillow")
PYEOF
done

# Teraz porownaj liczbe tokenow promptu dla kazdej skali
for ROZM in 320 640 1280; do
  IMG=$KURS/obrazy/skala-$ROZM.jpg
  [ -f "$IMG" ] || continue
  echo -n "$ROZM px: "
  $LB/llama-mtmd-cli -m $VL --mmproj $VLMM -ngl 999 -c 8192 \
    --image "$IMG" -p "Co to?" -n 1 2>&1 | grep -oE 'prompt eval.*tokens' | head -1
done
```

⭐ **Zobacz, jak liczba tokenów rośnie z rozdzielczością.** To jest bezpośredni koszt —
kontekstu, czasu i (w części 10, przy Claude) pieniędzy.

💡 **Praktyczna reguła dla faktur:** skaluj długą krawędź do **1024–1280 px**. Poniżej
Whisper... pardon, model VL przestaje czytać drobny druk; powyżej płacisz tokenami bez
zysku w trafności. **Zmierz to na własnych skanach** — to trzy minuty i oszczędza połowę
kontekstu.

### 3.5 Model wizyjny jako serwer

```bash
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1

$LB/llama-server -m $VL --mmproj $VLMM \
  -ngl 999 -c 16384 \
  --host 127.0.0.1 --port 8085 --no-warmup &
sleep 30

# Wyslij obraz przez API (base64, protokol OpenAI)
python3 - <<'PYEOF'
import base64, json, os, urllib.request

img = os.path.join(os.environ["KURS"], "obrazy/test.jpg")
b64 = base64.b64encode(open(img, "rb").read()).decode()

body = {
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "Opisz ten obraz po polsku w dwóch zdaniach."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
        ],
    }],
    "max_tokens": 300, "temperature": 0.2,
}
req = urllib.request.Request("http://127.0.0.1:8085/v1/chat/completions",
    data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
r = json.load(urllib.request.urlopen(req, timeout=300))
print(r["choices"][0]["message"]["content"])
print("\ntokeny promptu:", r.get("usage", {}).get("prompt_tokens"))
PYEOF
```

⭐ **To jest ten sam protokół, którego używa Claude API** (część 10). Ucząc się go tutaj,
uczysz się interfejsu, który zadziała w obie strony.

### 3.6 Ekstrakcja danych ze skanu — połącz z częścią 3

```bash
python3 - <<'PYEOF'
import base64, json, os, urllib.request

SCHEMA = {
  "type": "object",
  "properties": {
    "typ_dokumentu": {"type": "string", "enum": ["faktura", "paragon", "umowa", "inne"]},
    "numer":         {"type": "string"},
    "data":          {"type": "string"},
    "sprzedawca":    {"type": "string"},
    "kwota_brutto":  {"type": "number"},
    "czytelnosc":    {"type": "string", "enum": ["dobra", "srednia", "zla"]},
  },
  "required": ["typ_dokumentu", "numer", "data", "sprzedawca", "kwota_brutto", "czytelnosc"],
}

img = os.path.join(os.environ["KURS"], "obrazy/test.jpg")
b64 = base64.b64encode(open(img, "rb").read()).decode()

body = {
  "messages": [
    {"role": "system", "content":
       "Wyciągasz dane z polskich dokumentów księgowych ze zdjęć. "
       "Jeśli czegoś nie widać wyraźnie — ustaw czytelnosc na 'zla' i wpisz pusty string."},
    {"role": "user", "content": [
        {"type": "text", "text": "Wyciągnij dane z tego dokumentu."},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
    ]},
  ],
  "max_tokens": 400, "temperature": 0, "repeat_penalty": 1.0,
  "response_format": {"type": "json_schema", "json_schema": {"schema": SCHEMA}},
}
req = urllib.request.Request("http://127.0.0.1:8085/v1/chat/completions",
    data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
txt = json.load(urllib.request.urlopen(req, timeout=300))["choices"][0]["message"]["content"]
d = json.loads(txt)
print(json.dumps(d, indent=2, ensure_ascii=False))
if d["czytelnosc"] == "zla":
    print("\n⚠️  Model zglasza zla czytelnosc -> do weryfikacji przez czlowieka")
PYEOF
```

⭐ **To jest gramatyka z części 3 nałożona na wizję z części 5.** Skan wchodzi, gwarantowany
JSON wychodzi, a pole `czytelnosc` jest Twoim mechanizmem eskalacji. **To jest realny
fragment produktu księgowego.**

---

## 4. Słuchanie — `whisper.cpp` od zera

`whisper.cpp` to ten sam autor co llama.cpp, ta sama filozofia: jeden plik modelu,
jedna binarka, zero zależności Pythona.

### 4.1 Doinstaluj narzędzia audio

```bash
sudo apt update
sudo apt install -y ffmpeg sox libsox-fmt-all v4l-utils
```

🔧 `ffmpeg` do konwersji formatów, `sox` do obróbki (normalizacja, wykrywanie ciszy),
`v4l-utils` do kamery.

### 4.2 Sklonuj i zbuduj na ROCm

⚠️ **To te same flagi budowania z HIP, których użyłeś do llama.cpp** (część 1).
**Nie zmieniaj ich**, inaczej wyjdzie budowa na CPU.

```bash
cd ~
git clone https://github.com/ggml-org/whisper.cpp
cd whisper.cpp
git log -1 --format='%h %ad %s' --date=short   # zapisz commit!

# Budowa z HIP dla gfx1201 (RDNA4)
cmake -B build \
  -DGGML_HIP=ON \
  -DGPU_TARGETS=gfx1201 \
  -DCMAKE_BUILD_TYPE=Release

cmake --build build -j $(nproc)

ls -la build/bin/
```

```bash
export WB=$NARZEDZIA/whisper.cpp/build/bin
echo 'export WB=$NARZEDZIA/whisper.cpp/build/bin' >> $LLMEDU/rig-env.sh
$WB/whisper-cli --help | head -20
```

⚠️ **Jeśli budowa padnie na HIP** — sprawdź, czy `ROCM_PATH` jest ustawiony:
```bash
export ROCM_PATH=/opt/rocm
export HIP_PATH=/opt/rocm
```
i powtórz `cmake`. Zapisz, co zadziałało, we własnych notatkach o maszynie — tak jak przy llama.cpp.

### 4.3 Pobierz model Whispera

```bash
cd $NARZEDZIA/whisper.cpp
# large-v3-turbo: najlepszy stosunek jakosc/szybkosc, dobry polski
bash ./models/download-ggml-model.sh large-v3-turbo

ls -la models/*.bin
export WMODEL=$NARZEDZIA/whisper.cpp/models/ggml-large-v3-turbo.bin
echo 'export WMODEL=$NARZEDZIA/whisper.cpp/models/ggml-large-v3-turbo.bin' >> $LLMEDU/rig-env.sh
```

| Model | Rozmiar | Polski | Szybkość |
| :-- | --: | :-- | :-- |
| `tiny` | 75 MB | ❌ słaby | bardzo szybki |
| `base` | 142 MB | ⚠️ przeciętny | szybki |
| `small` | 466 MB | ✅ dobry | dobry |
| **`large-v3-turbo`** | ~1,6 GB | ⭐ **bardzo dobry** | **szybki** — polecam |
| `large-v3` | ~3,1 GB | ⭐ najlepszy | wolniejszy |

💡 **`large-v3-turbo` to właściwy wybór.** Ma jakość niemal `large-v3` przy ~4× większej
szybkości. Przy Twoich kartach i tak zmieści się bez problemu.

### 4.4 Pierwsza transkrypcja

```bash
export HIP_VISIBLE_DEVICES=0,1

# Nagraj 8 sekund (podstaw wlasciwa karte z arecord -l)
arecord -D plughw:3,0 -f S16_LE -r 16000 -c 1 -d 8 $KURS/nagranie.wav
echo "Nagrane. Transkrybuje..."

$WB/whisper-cli -m $WMODEL -f $KURS/nagranie.wav -l pl --output-txt
cat $KURS/nagranie.wav.txt
```

🔧 **`-l pl`** wymusza polski. **Podaj go zawsze** — autodetekcja przy krótkich nagraniach
myli polski z czeskim i słowackim.

### 4.5 Ważne flagi Whispera

```bash
$WB/whisper-cli -m $WMODEL -f $KURS/nagranie.wav \
  -l pl \
  --output-json \
  --max-len 0 \
  --threads $(nproc) \
  --print-progress
```

| Flaga | Do czego |
| :-- | :-- |
| `-l pl` | język (zawsze podawaj) |
| `--output-json` | wyjście ze znacznikami czasu — do synchronizacji |
| `--output-srt` | napisy |
| `--max-len N` | maks. długość segmentu w znakach |
| `-t N` | wątki CPU |
| `--no-timestamps` | czysty tekst bez czasów |
| `--prompt "..."` | ⭐ **podpowiedź kontekstowa** — patrz niżej |

### 4.6 ⭐ `--prompt` — najbardziej niedoceniana flaga

Whisper przyjmuje podpowiedź, która **poprawia rozpoznawanie terminów branżowych**:

```bash
$WB/whisper-cli -m $WMODEL -f $KURS/nagranie.wav -l pl \
  --prompt "Terminologia księgowa: faktura VAT, KPiR, amortyzacja, NIP, ryczałt, JPK_V7M, PKPiR, środek trwały."
```

💡 **Dla Twojego produktu to jest kluczowe.** Bez podpowiedzi Whisper napisze „kapir",
„jotpekawusiedem". Z podpowiedzią — poprawnie. **Zbuduj słownik swojej domeny i podawaj go
zawsze.**

### 4.7 Nagrywanie z detekcją ciszy — praktyczne dyktowanie

```bash
cat > $KURS/sluchaj.sh <<'EOF'
#!/usr/bin/env bash
# Nagrywa, dopoki mowisz. Konczy po 2 s ciszy. Transkrybuje.
set -euo pipefail

KARTA="${KARTA:-plughw:3,0}"
WAV=$(mktemp /tmp/sluchaj-XXXXXX.wav)
SLOWNIK="Terminologia księgowa: faktura VAT, KPiR, amortyzacja, NIP, ryczałt, JPK, środek trwały, przychód, koszt."

echo "🎤 Mów... (kończę po 2 s ciszy)" >&2

# sox: nagrywaj, utnij cisze na koncu
rec -q -c 1 -r 16000 -b 16 "$WAV" \
    silence 1 0.1 2% 1 2.0 2% 2>/dev/null \
  || arecord -D "$KARTA" -f S16_LE -r 16000 -c 1 -d 10 "$WAV" 2>/dev/null

echo "⏳ Transkrybuję..." >&2
"$WB/whisper-cli" -m "$WMODEL" -f "$WAV" -l pl \
  --no-timestamps --output-txt --prompt "$SLOWNIK" >/dev/null 2>&1

cat "${WAV}.txt"
rm -f "$WAV" "${WAV}.txt"
EOF
chmod +x $KURS/sluchaj.sh

# Uzyj
$KURS/sluchaj.sh
```

🔧 **`silence 1 0.1 2% 1 2.0 2%`** — `sox` nagrywa od momentu, gdy poziom przekroczy 2 %,
i kończy po 2 sekundach ciszy. **To jest to, co zamienia „nagraj 10 sekund" w naturalne
dyktowanie.**

---

## 5. Mówienie — dwie drogi

### 5.1 Droga A: `llama-tts` (masz go już)

```bash
$LB/llama-tts --help 2>&1 | head -30
```

Wymaga **dwóch plików**, tak jak wizja: model bazowy (*backbone*) + wokoder (podawany jako
`-mm`).

```bash
mkdir -p ~/models/tts && cd ~/models/tts

# OuteTTS - model TTS dzialajacy w llama.cpp
hf download OuteAI/OuteTTS-0.3-500M-GGUF OuteTTS-0.3-500M-Q8_0.gguf --local-dir . 2>/dev/null
hf download ggml-org/WavTokenizer WavTokenizer-Large-75-F16.gguf --local-dir . 2>/dev/null

ls -la ~/models/tts/
```

```bash
$LB/llama-tts \
  -m ~/models/tts/OuteTTS-0.3-500M-Q8_0.gguf \
  -mm ~/models/tts/WavTokenizer-Large-75-F16.gguf \
  -p "Faktura została zaksięgowana poprawnie." \
  -o $KURS/mowa.wav

aplay $KURS/mowa.wav
```

⚠️ **Pułapka P34 (nowa): OuteTTS słabo mówi po polsku.**
Modele TTS w llama.cpp są trenowane głównie na angielskim. Polski wyjdzie zrozumiały, ale
z obcym akcentem i błędnymi akcentami wyrazowymi. **Do produktu polskojęzycznego to za mało.**

### 5.2 Droga B: Piper — ⭐ polecam dla polskiego

**Piper** to dedykowany silnik TTS (ONNX, CPU, bardzo szybki) z **prawdziwymi polskimi
głosami**.

```bash
mkdir -p $NARZEDZIA/piper && cd $NARZEDZIA/piper

# Binarka (sprawdz najnowsza wersje na github.com/rhasspy/piper/releases)
curl -L -o piper_amd64.tar.gz \
  https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz
tar -xzf piper_amd64.tar.gz
ls -la $NARZEDZIA/piper/piper/

# Polski glos
mkdir -p $NARZEDZIA/piper/glosy && cd $NARZEDZIA/piper/glosy
curl -L -O https://huggingface.co/rhasspy/piper-voices/resolve/main/pl/pl_PL/darkman/medium/pl_PL-darkman-medium.onnx
curl -L -O https://huggingface.co/rhasspy/piper-voices/resolve/main/pl/pl_PL/darkman/medium/pl_PL-darkman-medium.onnx.json
ls -la
```

```bash
echo "Faktura numer FV dwa tysiące dwadzieścia pięć została zaksięgowana poprawnie." | \
  $NARZEDZIA/piper/piper/piper \
    --model $NARZEDZIA/piper/glosy/pl_PL-darkman-medium.onnx \
    --output_file $KURS/mowa-piper.wav

aplay $KURS/mowa-piper.wav
```

**Porównaj obie drogi na tym samym zdaniu.** Usłyszysz różnicę natychmiast.

| | `llama-tts` (OuteTTS) | **Piper** |
| :-- | :-- | :-- |
| polski | ⚠️ obcy akcent | ✅ **naturalny** |
| gdzie liczy | GPU | CPU (~50 MB RAM) |
| szybkość | wolniejszy | ⭐ **szybszy niż czas rzeczywisty** |
| zależności | już masz | osobna binarka |
| głosy PL | — | kilka do wyboru |

⭐ **Rekomendacja: Piper.** Działa na CPU, więc **nie konkuruje z modelem językowym
o VRAM** — a to jest w Twoim systemie cenniejsze niż elegancja jednego stosu.

💡 **Inne polskie głosy Piper do wypróbowania:** `pl_PL-gosia-medium` (żeński),
`pl_PL-mc_speech-medium`. Pobierasz tak samo — zmieniasz tylko ścieżkę w URL.

### 5.3 Normalizacja tekstu przed TTS — konieczna

```bash
cat > $KURS/mow.py <<'PYEOF'
#!/usr/bin/env python3
"""TTS przez Piper z normalizacja polskiego tekstu.

TTS czyta "1476,50 zl" jako "jeden cztery siedem szesc" - trzeba to rozpisac.
"""
import os, re, subprocess, sys

PIPER = os.path.join(os.environ["NARZEDZIA"], "piper/piper/piper")
GLOS  = os.path.join(os.environ["NARZEDZIA"], "piper/glosy/pl_PL-darkman-medium.onnx")

JEDNOSTKI = "zero jeden dwa trzy cztery pięć sześć siedem osiem dziewięć".split()
NASCIE   = ("dziesięć jedenaście dwanaście trzynaście czternaście piętnaście "
            "szesnaście siedemnaście osiemnaście dziewiętnaście").split()
DZIESIATKI = ("", "", "dwadzieścia", "trzydzieści", "czterdzieści", "pięćdziesiąt",
              "sześćdziesiąt", "siedemdziesiąt", "osiemdziesiąt", "dziewięćdziesiąt")
SETKI = ("", "sto", "dwieście", "trzysta", "czterysta", "pięćset",
         "sześćset", "siedemset", "osiemset", "dziewięćset")

def forma(n: int, jeden: str, kilka: str, wiele: str) -> str:
    """Polska odmiana liczebnikowa: 1 zloty / 2-4 zlote / 5+ (i 12-14) zlotych.
    Standardowa regula pluralizacji jezyka polskiego (ta sama, ktorej uzywa
    gettext/ICU dla pl_PL) - NIE wystarczy sprawdzic sam ostatni cyfre,
    trzeba wykluczyc "nascie" (11-14) z formy "kilka"."""
    if n == 1:
        return jeden
    ost2 = n % 100
    if 2 <= n % 10 <= 4 and not (12 <= ost2 <= 14):
        return kilka
    return wiele

def liczba_slownie(n: int) -> str:
    if n == 0:  return "zero"
    if n < 0:   return "minus " + liczba_slownie(-n)
    if n < 10:  return JEDNOSTKI[n]
    if n < 20:  return NASCIE[n - 10]
    if n < 100:
        d, r = divmod(n, 10)
        return DZIESIATKI[d] + ((" " + JEDNOSTKI[r]) if r else "")
    if n < 1000:
        s, r = divmod(n, 100)
        return SETKI[s] + ((" " + liczba_slownie(r)) if r else "")
    if n < 1_000_000:
        t, r = divmod(n, 1000)
        pre = "tysiąc" if t == 1 else liczba_slownie(t) + " " + forma(t, "tysiąc", "tysiące", "tysięcy")
        return pre + ((" " + liczba_slownie(r)) if r else "")
    m, r = divmod(n, 1_000_000)
    pre = "milion" if m == 1 else liczba_slownie(m) + " " + forma(m, "milion", "miliony", "milionów")
    return pre + ((" " + liczba_slownie(r)) if r else "")

def normalizuj(t: str) -> str:
    """Rozpisuje kwoty, liczby i skroty na slowa."""
    # kwoty: 1476,50 zl  /  1 476,50 zł
    def kwota(m):
        cal = int(m.group(1).replace(" ", "").replace(" ", ""))
        gr  = int(m.group(2))
        s = liczba_slownie(cal) + " " + forma(cal, "złoty", "złote", "złotych")
        if gr:
            s += " " + liczba_slownie(gr) + " " + forma(gr, "grosz", "grosze", "groszy")
        return s
    t = re.sub(r"([\d  ]+),(\d{2})\s*(?:zł|zl|PLN)", kwota, t)

    # procenty
    t = re.sub(r"(\d+)\s*%", lambda m: liczba_slownie(int(m.group(1))) + " procent", t)

    # skroty branzowe
    for a, b in (("VAT", "wat"), ("NIP", "en i pe"), ("KPiR", "ka pe i er"),
                 ("JPK", "jot pe ka"), ("ZUS", "zus"), ("PIT", "pit"),
                 ("FV", "ef fau"), ("nr", "numer")):
        t = re.sub(rf"\b{a}\b", b, t)

    # pozostale gole liczby
    t = re.sub(r"\b(\d{1,7})\b", lambda m: liczba_slownie(int(m.group(1))), t)
    return t

def mow(tekst: str, plik: str | None = None, odtworz: bool = True):
    norm = normalizuj(tekst)
    out = plik or "/tmp/mowa.wav"
    subprocess.run([PIPER, "--model", GLOS, "--output_file", out],
                   input=norm, text=True, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if odtworz:
        subprocess.run(["aplay", "-q", out], check=False)
    return out, norm

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else \
        "Faktura FV 143/2025 na kwotę 1476,50 zł z VAT 23% została zaksięgowana."
    _, norm = mow(t)
    print(f"ORYGINAŁ:      {t}")
    print(f"ZNORMALIZOWANY: {norm}")
PYEOF
chmod +x $KURS/mow.py

python3 $KURS/mow.py
```

⚠️ **Pułapka P35 (nowa): TTS bez normalizacji brzmi jak awaria.**
„1476,50 zł" przeczytane dosłownie to „jeden cztery siedem sześć przecinek pięć zero
zet ł". **Normalizacja liczb i skrótów jest obowiązkowa**, nie kosmetyczna — zwłaszcza
w domenie, gdzie kwoty są treścią.

---

## 6. Pełna pętla głosowa

Teraz łączymy: **mikrofon → Whisper → model → Piper → głośnik.** Wszystko offline.

```bash
cat > $KURS/glos.py <<'PYEOF'
#!/usr/bin/env python3
"""Petla glosowa offline: mow -> agent odpowiada glosem.

Wymaga uruchomionego llama-server na 8081.
Uzycie:  python3 glos.py            # petla ciagla
         python3 glos.py --raz      # jedna wymiana
"""
import json, os, subprocess, sys, tempfile, urllib.request

WB      = os.path.join(os.environ["NARZEDZIA"], "whisper.cpp/build/bin")
WMODEL  = os.path.join(os.environ["NARZEDZIA"], "whisper.cpp/models/ggml-large-v3-turbo.bin")
KARTA   = os.environ.get("KARTA", "plughw:3,0")
LLM     = "http://127.0.0.1:8081"

sys.path.insert(0, os.environ["KURS"])
from mow import mow          # nasz TTS z normalizacja

SLOWNIK = ("Terminologia księgowa: faktura VAT, KPiR, amortyzacja, NIP, "
           "ryczałt, JPK, środek trwały, przychód, koszt, bilans.")

SYSTEM = ("Jesteś asystentem księgowym. Odpowiadasz KRÓTKO — maksymalnie trzy zdania, "
          "bo Twoja odpowiedź będzie przeczytana na głos. Bez list, bez punktorów, "
          "bez formatowania markdown. Jeśli nie wiesz — powiedz to wprost.")

# ---------- 1. SLUCHANIE --------------------------------------------------
def sluchaj(max_sek: int = 15) -> str:
    wav = tempfile.mktemp(suffix=".wav")
    print("🎤 Mów... (kończę po 2 s ciszy)", flush=True)
    # sox z detekcja ciszy; zapasowo arecord na staly czas
    r = subprocess.run(["rec", "-q", "-c", "1", "-r", "16000", "-b", "16", wav,
                        "silence", "1", "0.1", "2%", "1", "2.0", "2%"],
                       capture_output=True)
    if r.returncode != 0 or not os.path.exists(wav) or os.path.getsize(wav) < 2000:
        subprocess.run(["arecord", "-q", "-D", KARTA, "-f", "S16_LE",
                        "-r", "16000", "-c", "1", "-d", str(max_sek), wav], check=False)
    if not os.path.exists(wav) or os.path.getsize(wav) < 2000:
        return ""
    print("⏳ Rozpoznaję...", flush=True)
    subprocess.run([f"{WB}/whisper-cli", "-m", WMODEL, "-f", wav, "-l", "pl",
                    "--no-timestamps", "--output-txt", "--prompt", SLOWNIK],
                   capture_output=True, check=False)
    txt = ""
    if os.path.exists(wav + ".txt"):
        txt = open(wav + ".txt", encoding="utf-8").read().strip()
        os.unlink(wav + ".txt")
    os.unlink(wav)
    return txt

# ---------- 2. MYSLENIE --------------------------------------------------
def mysl(historia: list[dict]) -> str:
    req = urllib.request.Request(LLM + "/v1/chat/completions",
        data=json.dumps({"messages": historia, "max_tokens": 200,
                         "temperature": 0.4, "min_p": 0.05}).encode(),
        headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    return r["choices"][0]["message"]["content"].strip()

# ---------- 3. PETLA -----------------------------------------------------
def main():
    raz = "--raz" in sys.argv
    hist = [{"role": "system", "content": SYSTEM}]
    print("=== Asystent głosowy (offline). Powiedz 'koniec', żeby wyjść. ===\n")
    while True:
        uzytkownik = sluchaj()
        if not uzytkownik:
            print("(nic nie usłyszałem)\n"); 
            if raz: break
            continue
        print(f"👤 {uzytkownik}")
        if any(s in uzytkownik.lower() for s in ("koniec", "zakończ", "do widzenia")):
            mow("Do usłyszenia."); break

        hist.append({"role": "user", "content": uzytkownik})
        odp = mysl(hist)
        hist.append({"role": "assistant", "content": odp})
        print(f"🤖 {odp}\n")
        mow(odp)

        if len(hist) > 13:                    # prosta kompakcja (czesc 4 §8.2)
            hist = [hist[0]] + hist[-8:]
        if raz:
            break

if __name__ == "__main__":
    main()
PYEOF
chmod +x $KURS/glos.py
```

Uruchom:

```bash
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1
$LB/llama-server -m $BIELIK -ngl 999 -c 8192 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

cd $KURS && python3 glos.py --raz    # najpierw jedna wymiana
python3 glos.py                        # potem petla
```

### 6.1 Zmierz opóźnienia — gdzie naprawdę idzie czas

```bash
cat > $KURS/pomiar-glos.py <<'PYEOF'
#!/usr/bin/env python3
"""Mierzy, ile czasu zjada kazdy etap petli glosowej."""
import os, sys, time
sys.path.insert(0, os.environ["KURS"])
import glos
from mow import mow

t = {}
t0 = time.time();  txt = glos.sluchaj();          t["1. nagranie+STT"] = time.time()-t0
if not txt:
    sys.exit("nic nie nagrano")
t0 = time.time()
odp = glos.mysl([{"role":"system","content":glos.SYSTEM},{"role":"user","content":txt}])
t["2. model (LLM)"] = time.time()-t0
t0 = time.time();  mow(odp, odtworz=False);       t["3. TTS"] = time.time()-t0

print(f"\nUSLYSZANE:  {txt}")
print(f"ODPOWIEDZ:  {odp}\n")
razem = sum(t.values())
for k, v in t.items():
    print(f"  {k:20s} {v:6.2f} s   {100*v/razem:5.1f}%")
print(f"  {'RAZEM':20s} {razem:6.2f} s")
print("\nGdzie optymalizowac:")
print("  STT wolny  -> mniejszy model Whispera (small) albo krotsze wypowiedzi")
print("  LLM wolny  -> patrz czesc 8: dekodowanie spekulatywne, prompt cache")
print("  TTS wolny  -> Piper 'low' zamiast 'medium'")
PYEOF

cd $KURS && python3 pomiar-glos.py
```

⭐ **Prawie zawsze wyjdzie, że najdroższy jest model językowy.** To jest dokładnie ten
pomiar, który uzasadnia część 8 (optymalizacja) — i który pokaże, że **dekodowanie
spekulatywne z Twoim modelem `eagle3` jest najlepszą inwestycją**.

### 6.2 Trzy realne problemy pętli głosowej

| Problem | Przyczyna | Obejście |
| :-- | :-- | :-- |
| **agent słyszy sam siebie** | głośniki → mikrofon | ⭐ zestaw słuchawkowy (§2.1), albo wycisz mikrofon podczas TTS |
| **Whisper halucynuje przy ciszy** | model „słyszy" szum wentylatorów | próg głośności w `sox`, mikrofon kierunkowy |
| **odpowiedź za długa do słuchania** | model pisze jak do czytania | prompt: „maksymalnie trzy zdania, bez list" (jest w `SYSTEM`) |

⚠️ **Pułapka P36 (nowa): Whisper halucynuje na ciszy i szumie.**
Podany 3-sekundowy fragment samego szumu wentylatorów zwróci zdanie — często „Dziękuję za
uwagę" albo „Napisy stworzone przez...". To jest znany artefakt treningu. **Zawsze
odrzucaj transkrypcje z nagrań krótszych niż ~1 s lub o niskiej energii sygnału.**

---

## 7. Ćwiczenie — asystent, który czyta skany faktur

Złóż wszystko z części 3–5 w jedno narzędzie.

**Cel:** pokazujesz kamerze fakturę, mówisz „zaksięguj to", agent odczytuje dane,
zapisuje do bazy i **potwierdza głosem**.

```bash
cat > $KURS/asystent-faktur.py <<'PYEOF'
#!/usr/bin/env python3
"""Asystent faktur: obraz + glos -> dane -> baza -> potwierdzenie glosowe.

Wymaga:
  - llama-server z modelem VL na 8085   (czesc 5 §3.5)
  - Piper                               (czesc 5 §5.2)
  - whisper.cpp                         (czesc 5 §4)
"""
import base64, json, os, sqlite3, subprocess, sys, urllib.request

sys.path.insert(0, os.environ["KURS"])
from mow import mow

VL_URL = "http://127.0.0.1:8085/v1/chat/completions"
DB     = os.path.join(os.environ["KURS"], "faktury.db")

SCHEMA = {
  "type": "object",
  "properties": {
    "numer":        {"type": "string"},
    "data":         {"type": "string"},
    "sprzedawca":   {"type": "string"},
    "nip":          {"type": "string"},
    "netto":        {"type": "number"},
    "vat_stawka":   {"type": "integer", "enum": [0, 5, 8, 23]},
    "brutto":       {"type": "number"},
    "czytelnosc":   {"type": "string", "enum": ["dobra", "srednia", "zla"]},
  },
  "required": ["numer","data","sprzedawca","nip","netto","vat_stawka","brutto","czytelnosc"],
}

def zrob_zdjecie(plik: str) -> bool:
    """Robi zdjecie kamera. Wymaga fswebcam."""
    r = subprocess.run(["fswebcam", "-r", "1280x960", "--no-banner", "-q", plik],
                       capture_output=True)
    return r.returncode == 0 and os.path.exists(plik)

def odczytaj(plik_obrazu: str) -> dict:
    b64 = base64.b64encode(open(plik_obrazu, "rb").read()).decode()
    body = {
      "messages": [
        {"role": "system", "content":
           "Wyciągasz dane z polskich faktur ze zdjęć. Kwoty jako liczby. "
           "Daty RRRR-MM-DD. Jeśli czegoś nie widać — czytelnosc='zla', pole puste."},
        {"role": "user", "content": [
            {"type": "text", "text": "Odczytaj dane z tej faktury."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
        ]},
      ],
      "max_tokens": 500, "temperature": 0, "repeat_penalty": 1.0,
      "response_format": {"type": "json_schema", "json_schema": {"schema": SCHEMA}},
    }
    req = urllib.request.Request(VL_URL, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    txt = json.load(urllib.request.urlopen(req, timeout=300))["choices"][0]["message"]["content"]
    return json.loads(txt)

def sprawdz(d: dict) -> list[str]:
    """Kontrole, ktorych gramatyka NIE robi (czesc 3 §2.5)."""
    bledy = []
    oczek = round(d["netto"] * (1 + d["vat_stawka"]/100), 2)
    if abs(oczek - d["brutto"]) > 0.02:
        bledy.append(f"arytmetyka: netto {d['netto']} + {d['vat_stawka']}% = {oczek}, a brutto to {d['brutto']}")
    if d["nip"] and len(d["nip"].replace("-","").replace(" ","")) != 10:
        bledy.append(f"NIP ma zla dlugosc: {d['nip']!r}")
    if d["czytelnosc"] == "zla":
        bledy.append("model zglasza zla czytelnosc zdjecia")
    return bledy

def zapisz(d: dict):
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS faktury(
        id INTEGER PRIMARY KEY, numer TEXT UNIQUE, data TEXT, sprzedawca TEXT,
        nip TEXT, netto REAL, vat_stawka INTEGER, brutto REAL, dodano TEXT)""")
    con.execute("""INSERT OR REPLACE INTO faktury
        (numer,data,sprzedawca,nip,netto,vat_stawka,brutto,dodano)
        VALUES(?,?,?,?,?,?,?,datetime('now'))""",
        (d["numer"], d["data"], d["sprzedawca"], d["nip"],
         d["netto"], d["vat_stawka"], d["brutto"]))
    con.commit(); con.close()

def main():
    obraz = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ["KURS"], "obrazy/faktura.jpg")
    if not os.path.exists(obraz):
        print(f"Robie zdjecie -> {obraz}")
        if not zrob_zdjecie(obraz):
            sys.exit("brak kamery i brak pliku — podaj sciezke do zdjecia jako argument")

    print("Odczytuję fakturę...")
    d = odczytaj(obraz)
    print(json.dumps(d, indent=2, ensure_ascii=False))

    bledy = sprawdz(d)
    if bledy:
        print("\n⚠️  PROBLEMY:")
        for b in bledy: print(f"   - {b}")
        mow(f"Znalazłem {len(bledy)} problemów. Faktura wymaga sprawdzenia przez człowieka.")
        return

    zapisz(d)
    komunikat = (f"Zaksięgowano fakturę {d['numer']} od {d['sprzedawca']} "
                 f"na kwotę {d['brutto']:.2f} zł.")
    print(f"\n✅ {komunikat}")
    mow(komunikat)

if __name__ == "__main__":
    main()
PYEOF
chmod +x $KURS/asystent-faktur.py

# Uruchom (podaj zdjecie faktury albo podlacz kamere)
sudo apt install -y fswebcam
cd $KURS && python3 asystent-faktur.py $KURS/obrazy/faktura.jpg
```

### 7.1 Zadania rozszerzające

1. **Dodaj potwierdzenie głosowe przed zapisem** — agent czyta odczytane dane, Ty mówisz
   „tak" albo „popraw numer".
2. **Zmierz trafność OCR** — zrób 10 zdjęć faktur, zbuduj zestaw ewaluacyjny jak w części 3
   §6 i zmierz, ile pól odczytuje poprawnie. **Bez tej liczby nie wiesz, czy to działa.**
3. **Sprawdź wpływ rozdzielczości** — ten sam zestaw przy 640, 1024 i 1600 px.
   Znajdź punkt, w którym trafność przestaje rosnąć. To Twoja docelowa rozdzielczość.
4. **Dodaj wykrywanie duplikatów** — `numer` jest `UNIQUE`; obsłuż przypadek, gdy faktura
   już jest w bazie, i powiedz to głosem.

---

## Sprawdź się

- [ ] Dlaczego obraz „zjada kontekst" i ile go zjada?
- [ ] Co się stanie, jeśli podasz `mmproj` z innego modelu?
- [ ] Dlaczego nie wolno kwantyzować `mmproj` do Q4?
- [ ] Dlaczego `-l pl` trzeba podawać Whisperowi zawsze?
- [ ] Co robi `--prompt` w Whisperze i dlaczego jest kluczowy dla Twojej domeny?
- [ ] Dlaczego Piper jest lepszym wyborem niż `llama-tts` dla polskiego?
- [ ] Dlaczego TTS wymaga normalizacji tekstu?
- [ ] Dlaczego zestaw słuchawkowy jest lepszy niż mikrofon na biurku — dwa powody?
- [ ] Który etap pętli głosowej jest najdroższy czasowo?

## Nowe pułapki

| ID | Pułapka | § |
| :-- | :-- | :-- |
| **P32** | iGPU jako `GPU[2]` — małe modele trafiają na 2 GB i zwalniają 50× | §1 |
| **P33** | `mmproj` niezgodny z modelem — wizja nie działa albo bredzi | §3.1 |
| **P34** | OuteTTS słabo mówi po polsku — użyj Pipera | §5.1 |
| **P35** | TTS bez normalizacji liczb brzmi jak awaria | §5.3 |
| **P36** | Whisper halucynuje na ciszy i szumie wentylatorów | §6.2 |

---

**Następna część: `06-PETLA-AGENTA-OD-ZERA.md`** — serce kursu. Budujesz pętlę, która
czyta pliki, pisze kod i uruchamia polecenia. Twój własny OpenClaw.
