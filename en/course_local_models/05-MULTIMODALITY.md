# Part 5 — Multimodality: an agent that sees, hears and speaks

**Level: ⭐⭐⭐⭐** · Requires: parts 2–4 · Time: ~6 h

> **Why this chapter.** An agent that only reads text is a calendar. An agent that
> **sees an invoice scan**, **listens as you dictate**, and **answers by voice** — that is
> a working tool. Everything in this chapter works **completely offline** on your hardware.
>
> We start low: every modality is a separate model, a separate file, a separate command. First
> you will understand each piece, then you will join them into a single loop.

```bash
cd ~/llm-education   # repository directory (yours may differ)
source rig-env.sh
```

---

## Table of contents

| § | Topic | Tool |
| :-- | :-- | :-- |
| [1](#1-what-you-have-and-what-is-missing) | **Inventory** | what is on the machine, what to buy |
| [2](#2-hardware--what-to-buy-and-why) | **Hardware** | ⭐ shopping list: microphone, camera, speaker |
| [3](#3-vision--a-model-that-reads-images) | **Vision** | `llama-mtmd-cli` + a VL model |
| [4](#4-listening--whispercpp-from-scratch) | **Listening** | `whisper.cpp` built on ROCm |
| [5](#5-speaking--two-routes) | **Speaking** | `llama-tts` vs Piper |
| [6](#6-the-full-voice-loop) | **Voice loop** | speak → agent → you hear the answer |
| [7](#7-exercise--an-assistant-that-reads-invoice-scans) | **Exercise** | scan → data → voice |

---

## 1. What you have and what is missing

Checked on your machine on 22 September 2026:

| Item | Status | Note |
| :-- | :-- | :-- |
| **`llama-mtmd-cli`** | ✅ **present** | vision + audio input, built |
| **`llama-tts`** | ✅ **present** | speech synthesis, built |
| `libmtmd.so` | ✅ present | multimodal library |
| `arecord` / `aplay` | ✅ present | ALSA — recording and playback |
| `pw-cat` | ✅ present | PipeWire — an alternative to ALSA |
| **audio input** | ✅ **present** | `card 3: ALC1220 Analog` (the board's line/microphone input) |
| **`whisper.cpp`** | ❌ **missing** | §4 — you need to clone and build it |
| **VL models (`mmproj`)** | ❌ **missing** | §3 — you need to download them |
| camera | ❌ no `/dev/video*` | §2 — you need to buy one |
| `ffmpeg`, `sox` | ❌ missing | §4.1 — `apt install` |
| Piper (TTS) | ❌ missing | §5.2 — optional, but recommended for Polish |

⚠️ **Trap P32 (new): the iGPU is now `GPU[2]`.**
`rocm-smi` shows three devices: `GPU[0]` and `GPU[1]` are the R9700 cards (34.2 GB each),
`GPU[2]` is the **integrated graphics with 2 GB**. Multimodal models are small and **may land
on the iGPU by mistake** — then they work, but 50× slower. This is trap **P12** in new
clothes. **Always set `HIP_VISIBLE_DEVICES=0,1`** for tasks that are meant to run on the cards:

```bash
export HIP_VISIBLE_DEVICES=0,1
echo 'export HIP_VISIBLE_DEVICES=0,1' >> $LLMEDU/rig-env.sh
```

⚠️ **Check this after adding cards 3 and 4** — the numbering will change again (trap **P13**).

---

## 2. Hardware — what to buy and why

You have an audio input on the board (`ALC1220`), but **you have no microphone or camera**.

### 2.1 Microphone — the most important purchase

| Option | Price | Why |
| :-- | --: | :-- |
| ⭐ **USB condenser microphone** (Fifine K669B, Trust GXT 232) | PLN 120–200 | **recommended to start.** USB = its own sound card, bypasses the board's noise. Sufficient for dictation |
| **USB headset** (Logitech H390, Jabra Evolve) | PLN 150–350 | ⭐ **better for the voice loop** — microphone at your mouth, no echo from speakers |
| XLR microphone + interface (Rode PodMic + Focusrite) | PLN 900–1500 | studio quality; **overkill** for STT |
| **Microphone array** (ReSpeaker 4-Mic Array, Anker PowerConf) | PLN 350–700 | for voice control **from the other end of the room**; buy once the voice loop already works |

💡 **The key technical tip:** Whisper works on **16 kHz mono**. You do not need
a studio microphone — you need a **clean signal without background noise**. A USB
headset for PLN 200 will give better STT results than a condenser microphone for PLN 800 standing a metre from
the fans of four graphics cards. **And a multi-GPU machine is loud.**

⚠️ **This is a real problem, not theory.** Four R9700 cards under load make serious
noise. An omnidirectional microphone on the desk will record the fans and Whisper will hallucinate.
**Get a headset or a directional microphone.**

### 2.2 Camera

| Option | Price | What for |
| :-- | --: | :-- |
| ⭐ **Logitech C920 / C922** | PLN 250–400 | **recommended.** 1080p, great Linux support (UVC, zero drivers) |
| Logitech Brio 4K | PLN 700–900 | 4K — useful if the camera is to **read documents** |
| **Document camera / visualizer** (IPEVO, Aver) | PLN 600–1200 | ⭐ if the goal is **scanning invoices on the desk** — an arm above the desk, focus on paper |
| USB camera with autofocus and macro | PLN 200–300 | budget option for documents |

💡 **For reading invoices a document camera beats a webcam.** A webcam is optimized for
a face at 50 cm; a document on the desk comes out crooked and with glare. If
multimodality is to serve **accounting**, a camera on an arm is the right tool.

⚠️ **Check UVC support before buying.** A "UVC-compatible" camera works in Linux without
drivers. Everything else is a lottery.

### 2.3 Audio output

You have an output on the board. It is enough. If you want a dedicated one:

| Option | Price |
| :-- | --: |
| USB speakers / active speakers on a jack | PLN 100–300 |
| USB DAC + headphones | PLN 200–500 |

### 2.4 Minimal starter kit

```
USB headset (Logitech H390)              ~PLN 170   ← microphone + speaker in one
Logitech C920 camera                     ~PLN 300
─────────────────────────────────────────────────
TOTAL                                    ~PLN 470
```

That is enough to get through **this whole chapter**. You will buy the document camera and the microphone array
once you know you need them.

### 2.5 Check the hardware after connecting it

```bash
# Is the microphone visible?
arecord -l

# Record 5 seconds as a test (substitute the right card number)
arecord -D plughw:3,0 -f S16_LE -r 16000 -c 1 -d 5 $KURS/test-mic.wav
aplay $KURS/test-mic.wav

# Is the camera visible?
ls -l /dev/video*
v4l2-ctl --list-devices 2>/dev/null || sudo apt install -y v4l-utils
```

🔧 **`-f S16_LE -r 16000 -c 1`** = 16-bit, 16 kHz, mono. **This is exactly the format
Whisper wants** — record like this from the start and you will not have to convert.

---

## 3. Vision — a model that reads images

### 3.1 How it works underneath

A language model does not understand pixels. It needs a **translator**:

```
   JPEG image
       │
       ▼
  ┌──────────────────────────┐
  │  VISION ENCODER (ViT)    │  mmproj.gguf file
  │  image → feature grid    │
  └──────────────────────────┘
       │
       ▼
  ┌──────────────────────────┐
  │  PROJECTOR               │  also in mmproj.gguf
  │  vectors → "image tokens"│  ← in the model's embedding space!
  └──────────────────────────┘
       │
       ▼
  inserted into the token sequence next to your text
       │
       ▼
  ┌──────────────────────────┐
  │  LANGUAGE MODEL          │  the model .gguf file
  └──────────────────────────┘
```

⭐ **The key intuition:** the image is **turned into tokens** and thrown into the same
context as the text. Therefore:

| Fact | Consequence |
| :-- | :-- |
| an image takes **hundreds to thousands of tokens** | one photo can eat ¼ of the context |
| higher resolution = more tokens | an A4 scan at 300 dpi is a very expensive image |
| **you need TWO files** | model + `mmproj` — the model alone cannot see |

⚠️ **Trap P33 (new): `mmproj` must match the model.**
An `mmproj` from Qwen2.5-VL will not work with Gemma. It is not a generic "vision add-on" —
it is part of a specific model. **Download both files from the same repository.**

### 3.2 Download a vision model

For Polish + reading documents I recommend **Qwen2.5-VL-7B**:

```bash
mkdir -p ~/models/vl && cd ~/models/vl

# Model + vision projector - BOTH files from the same repo
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

**Alternatives worth noting:**

| Model | Size | Strength |
| :-- | --: | :-- |
| **Qwen2.5-VL-7B** | ~5 GB | ⭐ best for **text in images** (invoice OCR), good Polish |
| Gemma 3 12B (vision) | ~8 GB | strong reasoning about the image, weaker OCR |
| MiniCPM-V 2.6 | ~5 GB | a very good quality/size ratio |
| InternVL2.5 | 4–26 GB | strongest on charts and tables |

⚠️ **Do not quantize `mmproj` below `f16`.** The projector is a numerical layer; `Q4` on it
wrecks image understanding drastically more than `Q4` on the language model.

### 3.3 The first image

```bash
# Prepare a test image: a screenshot or a photo
mkdir -p $KURS/obrazy
# If you have a camera:
#   sudo apt install -y fswebcam && fswebcam -r 1280x720 $KURS/obrazy/test.jpg
# Or use a file you already have (e.g. a photo of the F43SG board):
ls $KURS/obrazy/ 2>/dev/null || echo "put some .jpg into $KURS/obrazy/"

export HIP_VISIBLE_DEVICES=0,1

# The prompt is Polish: "Describe exactly what you see in this image. Answer in Polish."
$LB/llama-mtmd-cli \
  -m $VL --mmproj $VLMM \
  -ngl 999 -c 8192 \
  --image $KURS/obrazy/test.jpg \
  -p "Opisz dokładnie, co widzisz na tym obrazie. Odpowiedz po polsku."
```

🔧 **Flags:** `--mmproj` is the vision projector, `--image` is the image file (it can be given
several times for several images), `-c 8192` because **an image eats a lot of context**.

### 3.4 Measure how many tokens an image eats

```bash
for ROZM in 320 640 1280; do
  python3 - "$ROZM" <<'PYEOF'
import subprocess, sys, os
r = sys.argv[1]
src = os.path.join(os.environ["KURS"], "obrazy/test.jpg")
dst = os.path.expandvars(f"$KURS/obrazy/skala-{r}.jpg")
# Scaling through Python (no ffmpeg) - requires Pillow
try:
    from PIL import Image
    im = Image.open(src); im.thumbnail((int(r), int(r))); im.save(dst, quality=88)
    print(f"{r}px -> {dst} ({os.path.getsize(dst)//1024} KB)")
except ImportError:
    print("no Pillow: python3 -m venv $VENVS/kurs && $VENVS/kurs/bin/pip install pillow")
PYEOF
done

# Now compare the prompt token count for each scale
for ROZM in 320 640 1280; do
  IMG=$KURS/obrazy/skala-$ROZM.jpg
  [ -f "$IMG" ] || continue
  echo -n "$ROZM px: "
  $LB/llama-mtmd-cli -m $VL --mmproj $VLMM -ngl 999 -c 8192 \
    --image "$IMG" -p "Co to?" -n 1 2>&1 | grep -oE 'prompt eval.*tokens' | head -1
done
```

⭐ **See how the token count grows with resolution.** This is a direct cost —
of context, of time and (in part 10, with Claude) of money.

💡 **A practical rule for invoices:** scale the long edge to **1024–1280 px**. Below that
Whisper... sorry, the VL model stops reading fine print; above it you pay in tokens with no
gain in accuracy. **Measure it on your own scans** — it takes three minutes and saves half
of the context.

### 3.5 The vision model as a server

```bash
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1

$LB/llama-server -m $VL --mmproj $VLMM \
  -ngl 999 -c 16384 \
  --host 127.0.0.1 --port 8085 --no-warmup &
sleep 30

# Send an image through the API (base64, OpenAI protocol)
python3 - <<'PYEOF'
import base64, json, os, urllib.request

img = os.path.join(os.environ["KURS"], "obrazy/test.jpg")
b64 = base64.b64encode(open(img, "rb").read()).decode()

body = {
    "messages": [{
        "role": "user",
        "content": [
            # "Describe this image in Polish in two sentences."
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
print("\nprompt tokens:", r.get("usage", {}).get("prompt_tokens"))
PYEOF
```

⭐ **This is the same protocol the Claude API uses** (part 10). By learning it here,
you learn an interface that will work both ways.

### 3.6 Extracting data from a scan — combine it with part 3

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
# (document type: invoice / receipt / contract / other; legibility: good / medium / bad)

img = os.path.join(os.environ["KURS"], "obrazy/test.jpg")
b64 = base64.b64encode(open(img, "rb").read()).decode()

body = {
  "messages": [
    # System prompt (Polish): "You extract data from Polish accounting documents in photos. If something
    # is not clearly visible - set czytelnosc to 'zla' and enter an empty string."
    {"role": "system", "content":
       "Wyciągasz dane z polskich dokumentów księgowych ze zdjęć. "
       "Jeśli czegoś nie widać wyraźnie — ustaw czytelnosc na 'zla' i wpisz pusty string."},
    {"role": "user", "content": [
        # "Extract the data from this document."
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
    print("\n⚠️  The model reports bad legibility -> needs verification by a human")
PYEOF
```

⭐ **This is the grammar from part 3 laid over the vision from part 5.** A scan goes in, guaranteed
JSON comes out, and the `czytelnosc` ("legibility") field is your escalation mechanism. **This is a real
piece of an accounting product.**

---

## 4. Listening — `whisper.cpp` from scratch

`whisper.cpp` is by the same author as llama.cpp, with the same philosophy: one model file,
one binary, zero Python dependencies.

### 4.1 Install the audio tools

```bash
sudo apt update
sudo apt install -y ffmpeg sox libsox-fmt-all v4l-utils
```

🔧 `ffmpeg` for format conversion, `sox` for processing (normalization, silence detection),
`v4l-utils` for the camera.

### 4.2 Clone and build on ROCm

⚠️ **These are the same HIP build flags you used for llama.cpp** (part 1).
**Do not change them**, or you will end up with a CPU build.

```bash
cd ~
git clone https://github.com/ggml-org/whisper.cpp
cd whisper.cpp
git log -1 --format='%h %ad %s' --date=short   # write down the commit!

# Build with HIP for gfx1201 (RDNA4)
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

⚠️ **If the build fails on HIP** — check that `ROCM_PATH` is set:
```bash
export ROCM_PATH=/opt/rocm
export HIP_PATH=/opt/rocm
```
and repeat `cmake`. Write down what worked in your own machine notes — just as with llama.cpp.

### 4.3 Download a Whisper model

```bash
cd $NARZEDZIA/whisper.cpp
# large-v3-turbo: the best quality/speed ratio, good Polish
bash ./models/download-ggml-model.sh large-v3-turbo

ls -la models/*.bin
export WMODEL=$NARZEDZIA/whisper.cpp/models/ggml-large-v3-turbo.bin
echo 'export WMODEL=$NARZEDZIA/whisper.cpp/models/ggml-large-v3-turbo.bin' >> $LLMEDU/rig-env.sh
```

| Model | Size | Polish | Speed |
| :-- | --: | :-- | :-- |
| `tiny` | 75 MB | ❌ weak | very fast |
| `base` | 142 MB | ⚠️ average | fast |
| `small` | 466 MB | ✅ good | good |
| **`large-v3-turbo`** | ~1.6 GB | ⭐ **very good** | **fast** — recommended |
| `large-v3` | ~3.1 GB | ⭐ best | slower |

💡 **`large-v3-turbo` is the right choice.** It has nearly the quality of `large-v3` at ~4× the
speed. With your cards it will fit without any problem anyway.

### 4.4 The first transcription

```bash
export HIP_VISIBLE_DEVICES=0,1

# Record 8 seconds (substitute the right card from arecord -l)
arecord -D plughw:3,0 -f S16_LE -r 16000 -c 1 -d 8 $KURS/nagranie.wav
echo "Recorded. Transcribing..."

$WB/whisper-cli -m $WMODEL -f $KURS/nagranie.wav -l pl --output-txt
cat $KURS/nagranie.wav.txt
```

🔧 **`-l pl`** forces Polish. **Always pass it** — autodetection on short recordings
confuses Polish with Czech and Slovak.

### 4.5 Important Whisper flags

```bash
$WB/whisper-cli -m $WMODEL -f $KURS/nagranie.wav \
  -l pl \
  --output-json \
  --max-len 0 \
  --threads $(nproc) \
  --print-progress
```

| Flag | What for |
| :-- | :-- |
| `-l pl` | language (always pass it) |
| `--output-json` | output with timestamps — for synchronization |
| `--output-srt` | subtitles |
| `--max-len N` | max segment length in characters |
| `-t N` | CPU threads |
| `--no-timestamps` | plain text without times |
| `--prompt "..."` | ⭐ **context hint** — see below |

### 4.6 ⭐ `--prompt` — the most underrated flag

Whisper accepts a hint that **improves recognition of industry terms**:

```bash
# Hint: "Accounting terminology: VAT invoice, KPiR (tax revenue and expense ledger), depreciation, NIP (tax ID), lump-sum tax, JPK_V7M, PKPiR, fixed asset."
$WB/whisper-cli -m $WMODEL -f $KURS/nagranie.wav -l pl \
  --prompt "Terminologia księgowa: faktura VAT, KPiR, amortyzacja, NIP, ryczałt, JPK_V7M, PKPiR, środek trwały."
```

💡 **For your product this is key.** Without the hint Whisper will write "kapir",
"jotpekawusiedem". With the hint — correctly. **Build a vocabulary for your domain and always
pass it.**

### 4.7 Recording with silence detection — practical dictation

```bash
cat > $KURS/sluchaj.sh <<'EOF'
#!/usr/bin/env bash
# Records while you speak. Stops after 2 s of silence. Transcribes.
set -euo pipefail

KARTA="${KARTA:-plughw:3,0}"
WAV=$(mktemp /tmp/sluchaj-XXXXXX.wav)
SLOWNIK="Terminologia księgowa: faktura VAT, KPiR, amortyzacja, NIP, ryczałt, JPK, środek trwały, przychód, koszt."

echo "🎤 Speak... (I stop after 2 s of silence)" >&2

# sox: record, trim the silence at the end
rec -q -c 1 -r 16000 -b 16 "$WAV" \
    silence 1 0.1 2% 1 2.0 2% 2>/dev/null \
  || arecord -D "$KARTA" -f S16_LE -r 16000 -c 1 -d 10 "$WAV" 2>/dev/null

echo "⏳ Transcribing..." >&2
"$WB/whisper-cli" -m "$WMODEL" -f "$WAV" -l pl \
  --no-timestamps --output-txt --prompt "$SLOWNIK" >/dev/null 2>&1

cat "${WAV}.txt"
rm -f "$WAV" "${WAV}.txt"
EOF
chmod +x $KURS/sluchaj.sh

# Use it
$KURS/sluchaj.sh
```

🔧 **`silence 1 0.1 2% 1 2.0 2%`** — `sox` starts recording from the moment the level exceeds 2%,
and ends after 2 seconds of silence. **This is what turns "record 10 seconds" into natural
dictation.**

---

## 5. Speaking — two routes

### 5.1 Route A: `llama-tts` (you already have it)

```bash
$LB/llama-tts --help 2>&1 | head -30
```

It needs **two files**, just like vision: a base model (*backbone*) + a vocoder (passed as
`-mm`).

```bash
mkdir -p ~/models/tts && cd ~/models/tts

# OuteTTS - a TTS model that works in llama.cpp
hf download OuteAI/OuteTTS-0.3-500M-GGUF OuteTTS-0.3-500M-Q8_0.gguf --local-dir . 2>/dev/null
hf download ggml-org/WavTokenizer WavTokenizer-Large-75-F16.gguf --local-dir . 2>/dev/null

ls -la ~/models/tts/
```

```bash
# The text to speak (Polish): "The invoice was booked correctly."
$LB/llama-tts \
  -m ~/models/tts/OuteTTS-0.3-500M-Q8_0.gguf \
  -mm ~/models/tts/WavTokenizer-Large-75-F16.gguf \
  -p "Faktura została zaksięgowana poprawnie." \
  -o $KURS/mowa.wav

aplay $KURS/mowa.wav
```

⚠️ **Trap P34 (new): OuteTTS speaks Polish poorly.**
The TTS models in llama.cpp are trained mainly on English. The Polish comes out intelligible, but
with a foreign accent and wrong word stress. **For a Polish-language product that is not enough.**

### 5.2 Route B: Piper — ⭐ recommended for Polish

**Piper** is a dedicated TTS engine (ONNX, CPU, very fast) with **real Polish
voices**.

```bash
mkdir -p $NARZEDZIA/piper && cd $NARZEDZIA/piper

# Binary (check the latest version at github.com/rhasspy/piper/releases)
curl -L -o piper_amd64.tar.gz \
  https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz
tar -xzf piper_amd64.tar.gz
ls -la $NARZEDZIA/piper/piper/

# Polish voice
mkdir -p $NARZEDZIA/piper/glosy && cd $NARZEDZIA/piper/glosy
curl -L -O https://huggingface.co/rhasspy/piper-voices/resolve/main/pl/pl_PL/darkman/medium/pl_PL-darkman-medium.onnx
curl -L -O https://huggingface.co/rhasspy/piper-voices/resolve/main/pl/pl_PL/darkman/medium/pl_PL-darkman-medium.onnx.json
ls -la
```

```bash
# "Invoice number FV two thousand twenty-five was booked correctly." (numbers spelled out in words)
echo "Faktura numer FV dwa tysiące dwadzieścia pięć została zaksięgowana poprawnie." | \
  $NARZEDZIA/piper/piper/piper \
    --model $NARZEDZIA/piper/glosy/pl_PL-darkman-medium.onnx \
    --output_file $KURS/mowa-piper.wav

aplay $KURS/mowa-piper.wav
```

**Compare both routes on the same sentence.** You will hear the difference immediately.

| | `llama-tts` (OuteTTS) | **Piper** |
| :-- | :-- | :-- |
| Polish | ⚠️ foreign accent | ✅ **natural** |
| where it runs | GPU | CPU (~50 MB RAM) |
| speed | slower | ⭐ **faster than real time** |
| dependencies | you already have it | a separate binary |
| PL voices | — | several to choose from |

⭐ **Recommendation: Piper.** It runs on the CPU, so it **does not compete with the language model
for VRAM** — and in your system that is worth more than the elegance of a single stack.

💡 **Other Polish Piper voices to try:** `pl_PL-gosia-medium` (female),
`pl_PL-mc_speech-medium`. You download them the same way — you only change the path in the URL.

### 5.3 Text normalization before TTS — mandatory

```bash
cat > $KURS/mow.py <<'PYEOF'
#!/usr/bin/env python3
"""TTS through Piper with normalization of Polish text.

TTS reads "1476,50 zl" as "one four seven six" - it has to be spelled out.
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
    """Polish numeral inflection: 1 zloty / 2-4 zlote / 5+ (and 12-14) zlotych.
    The standard pluralization rule of the Polish language (the same one used by
    gettext/ICU for pl_PL) - it is NOT enough to check just the last digit,
    the "-teens" (11-14) must be excluded from the "few" form."""
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
    """Spells out amounts, numbers and abbreviations as words."""
    # amounts: 1476,50 zl  /  1 476,50 zł
    def kwota(m):
        cal = int(m.group(1).replace(" ", "").replace(" ", ""))
        gr  = int(m.group(2))
        s = liczba_slownie(cal) + " " + forma(cal, "złoty", "złote", "złotych")
        if gr:
            s += " " + liczba_slownie(gr) + " " + forma(gr, "grosz", "grosze", "groszy")
        return s
    t = re.sub(r"([\d  ]+),(\d{2})\s*(?:zł|zl|PLN)", kwota, t)

    # percentages
    t = re.sub(r"(\d+)\s*%", lambda m: liczba_slownie(int(m.group(1))) + " procent", t)

    # industry abbreviations
    for a, b in (("VAT", "wat"), ("NIP", "en i pe"), ("KPiR", "ka pe i er"),
                 ("JPK", "jot pe ka"), ("ZUS", "zus"), ("PIT", "pit"),
                 ("FV", "ef fau"), ("nr", "numer")):
        t = re.sub(rf"\b{a}\b", b, t)

    # remaining bare numbers
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
    print(f"ORIGINAL:   {t}")
    print(f"NORMALIZED: {norm}")
PYEOF
chmod +x $KURS/mow.py

python3 $KURS/mow.py
```

⚠️ **Trap P35 (new): TTS without normalization sounds like a malfunction.**
"1476,50 zł" read literally comes out as "jeden cztery siedem sześć przecinek pięć zero
zet ł" ("one four seven six comma five zero zet l"). **Normalizing numbers and abbreviations is mandatory**, not cosmetic — especially
in a domain where amounts are the content.

---

## 6. The full voice loop

Now we join it all up: **microphone → Whisper → model → Piper → speaker.** All offline.

```bash
cat > $KURS/glos.py <<'PYEOF'
#!/usr/bin/env python3
"""Offline voice loop: you speak -> the agent answers by voice.

Requires a running llama-server on 8081.
Usage:   python3 glos.py            # continuous loop
         python3 glos.py --raz      # a single exchange
"""
import json, os, subprocess, sys, tempfile, urllib.request

WB      = os.path.join(os.environ["NARZEDZIA"], "whisper.cpp/build/bin")
WMODEL  = os.path.join(os.environ["NARZEDZIA"], "whisper.cpp/models/ggml-large-v3-turbo.bin")
KARTA   = os.environ.get("KARTA", "plughw:3,0")
LLM     = "http://127.0.0.1:8081"

sys.path.insert(0, os.environ["KURS"])
from mow import mow          # our TTS with normalization

SLOWNIK = ("Terminologia księgowa: faktura VAT, KPiR, amortyzacja, NIP, "
           "ryczałt, JPK, środek trwały, przychód, koszt, bilans.")

# System prompt (Polish): "You are an accounting assistant. You answer BRIEFLY - at most three sentences,
# because your answer will be read aloud. No lists, no bullet points, no markdown formatting.
# If you do not know - say so plainly."
SYSTEM = ("Jesteś asystentem księgowym. Odpowiadasz KRÓTKO — maksymalnie trzy zdania, "
          "bo Twoja odpowiedź będzie przeczytana na głos. Bez list, bez punktorów, "
          "bez formatowania markdown. Jeśli nie wiesz — powiedz to wprost.")

# ---------- 1. LISTENING --------------------------------------------------
def sluchaj(max_sek: int = 15) -> str:
    wav = tempfile.mktemp(suffix=".wav")
    print("🎤 Speak... (I stop after 2 s of silence)", flush=True)
    # sox with silence detection; arecord for a fixed time as a fallback
    r = subprocess.run(["rec", "-q", "-c", "1", "-r", "16000", "-b", "16", wav,
                        "silence", "1", "0.1", "2%", "1", "2.0", "2%"],
                       capture_output=True)
    if r.returncode != 0 or not os.path.exists(wav) or os.path.getsize(wav) < 2000:
        subprocess.run(["arecord", "-q", "-D", KARTA, "-f", "S16_LE",
                        "-r", "16000", "-c", "1", "-d", str(max_sek), wav], check=False)
    if not os.path.exists(wav) or os.path.getsize(wav) < 2000:
        return ""
    print("⏳ Recognizing...", flush=True)
    subprocess.run([f"{WB}/whisper-cli", "-m", WMODEL, "-f", wav, "-l", "pl",
                    "--no-timestamps", "--output-txt", "--prompt", SLOWNIK],
                   capture_output=True, check=False)
    txt = ""
    if os.path.exists(wav + ".txt"):
        txt = open(wav + ".txt", encoding="utf-8").read().strip()
        os.unlink(wav + ".txt")
    os.unlink(wav)
    return txt

# ---------- 2. THINKING --------------------------------------------------
def mysl(historia: list[dict]) -> str:
    req = urllib.request.Request(LLM + "/v1/chat/completions",
        data=json.dumps({"messages": historia, "max_tokens": 200,
                         "temperature": 0.4, "min_p": 0.05}).encode(),
        headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=300))
    return r["choices"][0]["message"]["content"].strip()

# ---------- 3. LOOP ------------------------------------------------------
def main():
    raz = "--raz" in sys.argv
    hist = [{"role": "system", "content": SYSTEM}]
    # The Polish exit words are "koniec" (end), "zakończ" (finish), "do widzenia" (goodbye);
    # the spoken farewell "Do usłyszenia." means "Until next time."
    print("=== Voice assistant (offline). Say 'koniec' to exit. ===\n")
    while True:
        uzytkownik = sluchaj()
        if not uzytkownik:
            print("(I heard nothing)\n"); 
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

        if len(hist) > 13:                    # simple compaction (part 4 §8.2)
            hist = [hist[0]] + hist[-8:]
        if raz:
            break

if __name__ == "__main__":
    main()
PYEOF
chmod +x $KURS/glos.py
```

Run it:

```bash
pkill -f llama-server; sleep 2
export HIP_VISIBLE_DEVICES=0,1
$LB/llama-server -m $BIELIK -ngl 999 -c 8192 --port 8081 --host 127.0.0.1 --no-warmup &
sleep 25

cd $KURS && python3 glos.py --raz    # first a single exchange
python3 glos.py                        # then the loop
```

### 6.1 Measure the latencies — where the time really goes

```bash
cat > $KURS/pomiar-glos.py <<'PYEOF'
#!/usr/bin/env python3
"""Measures how much time each stage of the voice loop eats."""
import os, sys, time
sys.path.insert(0, os.environ["KURS"])
import glos
from mow import mow

t = {}
t0 = time.time();  txt = glos.sluchaj();          t["1. recording+STT"] = time.time()-t0
if not txt:
    sys.exit("nothing recorded")
t0 = time.time()
odp = glos.mysl([{"role":"system","content":glos.SYSTEM},{"role":"user","content":txt}])
t["2. model (LLM)"] = time.time()-t0
t0 = time.time();  mow(odp, odtworz=False);       t["3. TTS"] = time.time()-t0

print(f"\nHEARD:   {txt}")
print(f"ANSWER:  {odp}\n")
razem = sum(t.values())
for k, v in t.items():
    print(f"  {k:20s} {v:6.2f} s   {100*v/razem:5.1f}%")
print(f"  {'TOTAL':20s} {razem:6.2f} s")
print("\nWhere to optimize:")
print("  STT slow  -> a smaller Whisper model (small) or shorter utterances")
print("  LLM slow  -> see part 8: speculative decoding, prompt cache")
print("  TTS slow  -> Piper 'low' instead of 'medium'")
PYEOF

cd $KURS && python3 pomiar-glos.py
```

⭐ **Almost always the language model will turn out to be the most expensive.** This is exactly the
measurement that justifies part 8 (optimization) — and that will show that **speculative
decoding with your `eagle3` model is the best investment**.

### 6.2 Three real problems of the voice loop

| Problem | Cause | Workaround |
| :-- | :-- | :-- |
| **the agent hears itself** | speakers → microphone | ⭐ a headset (§2.1), or mute the microphone during TTS |
| **Whisper hallucinates on silence** | the model "hears" the fan noise | a volume threshold in `sox`, a directional microphone |
| **the answer is too long to listen to** | the model writes as if for reading | prompt: "at most three sentences, no lists" (it is in `SYSTEM`) |

⚠️ **Trap P36 (new): Whisper hallucinates on silence and noise.**
Given a 3-second fragment of nothing but fan noise it will return a sentence — often "Dziękuję za
uwagę" ("Thank you for your attention") or "Napisy stworzone przez..." ("Subtitles created by..."). This is a known training artifact. **Always
discard transcriptions of recordings shorter than ~1 s or with low signal energy.**

---

## 7. Exercise — an assistant that reads invoice scans

Put everything from parts 3–5 together into one tool.

**Purpose:** you show the camera an invoice, say "book this" ("zaksięguj to"), the agent reads the data,
saves it to the database and **confirms by voice**.

```bash
cat > $KURS/asystent-faktur.py <<'PYEOF'
#!/usr/bin/env python3
"""Invoice assistant: image + voice -> data -> database -> voice confirmation.

Requires:
  - llama-server with a VL model on 8085   (part 5 §3.5)
  - Piper                                  (part 5 §5.2)
  - whisper.cpp                            (part 5 §4)
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
    """Takes a photo with the camera. Requires fswebcam."""
    r = subprocess.run(["fswebcam", "-r", "1280x960", "--no-banner", "-q", plik],
                       capture_output=True)
    return r.returncode == 0 and os.path.exists(plik)

def odczytaj(plik_obrazu: str) -> dict:
    b64 = base64.b64encode(open(plik_obrazu, "rb").read()).decode()
    body = {
      "messages": [
        # System prompt (Polish): "You extract data from Polish invoices in photos. Amounts as numbers.
        # Dates YYYY-MM-DD. If something is not visible - czytelnosc='zla', leave the field empty."
        {"role": "system", "content":
           "Wyciągasz dane z polskich faktur ze zdjęć. Kwoty jako liczby. "
           "Daty RRRR-MM-DD. Jeśli czegoś nie widać — czytelnosc='zla', pole puste."},
        {"role": "user", "content": [
            # "Read the data from this invoice."
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
    """Checks that the grammar does NOT do (part 3 §2.5)."""
    bledy = []
    oczek = round(d["netto"] * (1 + d["vat_stawka"]/100), 2)
    if abs(oczek - d["brutto"]) > 0.02:
        bledy.append(f"arithmetic: net {d['netto']} + {d['vat_stawka']}% = {oczek}, but gross is {d['brutto']}")
    if d["nip"] and len(d["nip"].replace("-","").replace(" ","")) != 10:
        bledy.append(f"NIP has the wrong length: {d['nip']!r}")
    if d["czytelnosc"] == "zla":
        bledy.append("the model reports bad legibility of the photo")
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
        print(f"Taking a photo -> {obraz}")
        if not zrob_zdjecie(obraz):
            sys.exit("no camera and no file — pass the path to a photo as an argument")

    print("Reading the invoice...")
    d = odczytaj(obraz)
    print(json.dumps(d, indent=2, ensure_ascii=False))

    bledy = sprawdz(d)
    if bledy:
        print("\n⚠️  PROBLEMS:")
        for b in bledy: print(f"   - {b}")
        # Spoken (Polish): "I found N problems. The invoice needs to be checked by a human."
        mow(f"Znalazłem {len(bledy)} problemów. Faktura wymaga sprawdzenia przez człowieka.")
        return

    zapisz(d)
    # Spoken (Polish): "Booked invoice <number> from <seller> for the amount of <gross> zł."
    komunikat = (f"Zaksięgowano fakturę {d['numer']} od {d['sprzedawca']} "
                 f"na kwotę {d['brutto']:.2f} zł.")
    print(f"\n✅ {komunikat}")
    mow(komunikat)

if __name__ == "__main__":
    main()
PYEOF
chmod +x $KURS/asystent-faktur.py

# Run it (give it a photo of an invoice or connect the camera)
sudo apt install -y fswebcam
cd $KURS && python3 asystent-faktur.py $KURS/obrazy/faktura.jpg
```

### 7.1 Extension tasks

1. **Add a voice confirmation before saving** — the agent reads out the extracted data, you say
   "tak" (yes) or "popraw numer" (correct the number).
2. **Measure the OCR accuracy** — take 10 photos of invoices, build an evaluation set as in part 3
   §6 and measure how many fields it reads correctly. **Without this number you do not know whether it works.**
3. **Check the effect of resolution** — the same set at 640, 1024 and 1600 px.
   Find the point at which accuracy stops growing. That is your target resolution.
4. **Add duplicate detection** — `numer` is `UNIQUE`; handle the case when the invoice
   is already in the database, and say so by voice.

---

## Check yourself

- [ ] Why does an image "eat context", and how much does it eat?
- [ ] What will happen if you give an `mmproj` from a different model?
- [ ] Why must you not quantize `mmproj` to Q4?
- [ ] Why must you always pass `-l pl` to Whisper?
- [ ] What does `--prompt` do in Whisper, and why is it key for your domain?
- [ ] Why is Piper a better choice than `llama-tts` for Polish?
- [ ] Why does TTS require text normalization?
- [ ] Why is a headset better than a microphone on the desk — two reasons?
- [ ] Which stage of the voice loop is the most expensive in time?

## New traps

| ID | Trap | § |
| :-- | :-- | :-- |
| **P32** | the iGPU as `GPU[2]` — small models land on 2 GB and slow down 50× | §1 |
| **P33** | `mmproj` mismatched with the model — vision does not work or raves | §3.1 |
| **P34** | OuteTTS speaks Polish poorly — use Piper | §5.1 |
| **P35** | TTS without number normalization sounds like a malfunction | §5.3 |
| **P36** | Whisper hallucinates on silence and fan noise | §6.2 |

---

**Next part: `06-AGENT-LOOP-FROM-SCRATCH.md`** — the heart of the course. You build a loop that
reads files, writes code and runs commands. Your own OpenClaw.
