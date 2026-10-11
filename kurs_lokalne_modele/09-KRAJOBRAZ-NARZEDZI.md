# Część 9 — Krajobraz narzędzi open source

**Poziom: ⭐⭐⭐** (do czytania w dowolnym momencie) · Czas: ~3 h czytania + eksperymenty

> **Po co ten rozdział.** Części 1–8 nauczyły Cię budować wszystko od zera — celowo,
> żebyś rozumiał mechanizmy. **Teraz możesz świadomie wybierać gotowe narzędzia**, bo wiesz,
> co one robią pod spodem i co ukrywają.
>
> Ten rozdział to **katalog z oceną**, nie lista linków. Przy każdym narzędziu: co robi,
> kiedy je wziąć, kiedy nie — i **czy zadziała na Twoim RDNA4**, bo to jest realne sito,
> które odsiewa połowę ekosystemu.

---

## ⚠️ Zanim zaczniesz: Twoje żelazo to sito

Masz **Radeon AI PRO R9700, `gfx1201`, RDNA4, ROCm 7.2.4.** To jest architektura **nowa
i niszowa**. Znaczna część ekosystemu AI zakłada NVIDIA/CUDA.

**Trzy poziomy wsparcia, którymi oceniam każde narzędzie:**

| Oznaczenie | Znaczenie |
| :-- | :-- |
| ✅ **działa** | zbudujesz i uruchomisz bez heroizmu |
| ⚠️ **z zachodem** | działa po łatkach / nieoficjalnym obrazie / kompilacji ze źródeł |
| ❌ **nie na RDNA4** | wymaga CUDA albo nie ma wsparcia gfx1201 |

⚠️ **To nie jest wada Twojego wyboru sprzętu.** Masz 65 GB VRAM za ułamek ceny
odpowiednika NVIDII. Płacisz za to czasem na integrację. **Wiedz o tym, wybierając
narzędzie.**

---

## Spis treści

| § | Kategoria |
| :-- | :-- |
| [1](#1-silniki-inferencji) | ⭐ **Silniki inferencji** — alternatywy dla llama.cpp |
| [2](#2-bramki-i-orkiestracja) | Bramki i orkiestracja modeli |
| [3](#3-interfejsy-użytkownika) | Interfejsy użytkownika |
| [4](#4-wymuszanie-struktury) | Wymuszanie struktury wyjścia |
| [5](#5-bazy-wektorowe) | Bazy wektorowe |
| [6](#6-embeddingi-i-reranking) | Embeddingi i reranking |
| [7](#7-przetwarzanie-dokumentów-i-ocr) | ⭐ Przetwarzanie dokumentów i OCR |
| [8](#8-mowa-stt-i-tts) | Mowa — STT i TTS |
| [9](#9-frameworki-agentowe) | Frameworki agentowe |
| [10](#10-gotowi-agenci-kodujący) | Gotowi agenci kodujący |
| [11](#11-obserwowalność) | Obserwowalność |
| [12](#12-ewaluacja) | ⭐ Ewaluacja |
| [13](#13-dostrajanie-fine-tuning) | Dostrajanie |
| [14](#14-kwantyzacja) | Kwantyzacja |
| [15](#15-co-wziąć-na-start) | ⭐ Rekomendacje |

---

## 1. Silniki inferencji

To jest kategoria, o którą pytałeś wprost. `llama.cpp` to Twój start — oto reszta.

### 1.1 Porównanie

| Silnik | Format | RDNA4 | Mocna strona | Słaba strona |
| :-- | :-- | :-- | :-- | :-- |
| **llama.cpp** | GGUF | ✅ | ⭐ działa wszędzie, wszystkie kwantyzacje, gramatyki, spekulacja | niższa przepustowość przy wielu użytkownikach |
| **vLLM** | safetensors, AWQ, GPTQ | ⚠️ | ⭐ **~2× przepustowość**, PagedAttention, ciągły batching | ciężki, trudny na gfx1201 |
| **SGLang** | safetensors | ⚠️ | RadixAttention (świetny cache prefiksów), złożone przepływy | młodszy, mniej dokumentacji |
| **ExLlamaV2 / V3** | EXL2, EXL3 | ❌ | najszybszy na pojedynczym GPU, świetne kwantyzacje | **tylko CUDA** |
| **TGI** (HuggingFace) | safetensors | ⚠️ | produkcyjny, dobry ekosystem | ciężki, Rust + Python |
| **MLC-LLM** | własny | ⚠️ | kompiluje pod konkretny sprzęt, działa też na telefonach | egzotyczny łańcuch budowania |
| **Ollama** | GGUF | ✅ | ⭐ najłatwiejszy start, biblioteka modeli | **własny llama.cpp** — patrz ostrzeżenie |
| **KoboldCpp** | GGUF | ✅ | jeden plik, dużo próbkowań, UI w zestawie | nastawiony na kreatywne pisanie |
| **TabbyAPI** | EXL2 | ❌ | lekki serwer OpenAI dla ExLlamy | tylko CUDA |
| **Aphrodite** | wiele | ⚠️ | fork vLLM z mnóstwem próbkowań | j.w. co vLLM |

### 1.2 ⭐ vLLM — kiedy naprawdę warto

**Co robi lepiej od llama.cpp:**

| Mechanizm | Zysk |
| :-- | :-- |
| **PagedAttention** | KV-cache stronicowany jak pamięć wirtualna → mniej fragmentacji |
| **ciągły batching** | nowe żądania dołączają do wsadu w locie, nie czekają |
| **prefix caching** | współdzielony prefiks między żądaniami (jak `--cache-reuse`, ale lepiej) |

⭐ **Kiedy vLLM wygrywa: WIELU RÓWNOLEGŁYCH UŻYTKOWNIKÓW.** Dla jednego agenta
llama.cpp jest w zupełności wystarczający i **dużo prostszy**.

⚠️ **Realia na gfx1201** — to jest wiedza, którą masz już zapisaną w projekcie:

| Problem | Obejście |
| :-- | :-- |
| brak oficjalnego wsparcia gfx1201 | obraz `kyuz0/vllm-therock-gfx1201` z gotowymi łatkami |
| **TP ≥ 2 zakleszcza się** | **`NCCL_PROTO=Simple` obowiązkowo** (RCCL LL nie ma poprawek RDNA4) |
| **FP8 cicho spada do FP32** | tabela architektur AITER pomijała gfx1201 — sprawdź `arch_info.py` **w kontenerze** |
| **P2P zawiesza host przy 4 kartach** | `NCCL_P2P_DISABLE=1` (pułapka **P4**) |
| pipeline-parallel niestabilny | **używaj TP, nie PP** — odwrotnie niż zwykła rada |

```bash
# Szkic uruchomienia (wymaga Dockera - ktorego NIE masz, patrz czesc 7 §2)
# sudo apt install -y docker.io
# docker run --rm -it --device=/dev/kfd --device=/dev/dri \
#   --group-add video --ipc=host --shm-size 16G \
#   -e NCCL_P2P_DISABLE=1 -e NCCL_PROTO=Simple \
#   -p 8000:8000 kyuz0/vllm-therock-gfx1201 \
#   --model /models/... --tensor-parallel-size 2
```

💡 **Rekomendacja: vLLM zostaw na później.** Wracaj do niego, gdy (a) będziesz serwował
wielu klientów naraz, albo (b) llama.cpp okaże się wąskim gardłem **zmierzonym**, a nie
przeczuwanym.

### 1.3 ⛔ Ollama i LM Studio — dlaczego nie u Ciebie

Oba są wygodne. Oba **niosą własny, wbudowany silnik**.

⚠️ **To rozwala Twoją metodykę pomiarową.** Cała Twoja dyscyplina zapisuje **dokładny
commit llama.cpp i flagi budowy** (`GGML_HIP=ON`, `GPU_TARGETS=gfx1201`). Drugi silnik
o nieznanej konfiguracji oznacza, że **pomiar przestaje opisywać to, co realnie serwujesz.**
Na świeżym gfx1201 to nie jest ryzyko teoretyczne.

💡 **To nie znaczy, że są złe.** Dla kogoś, kto chce pogadać z modelem — Ollama jest
świetna. Dla kogoś, kto **sprzedaje liczby wydajnościowe klientowi** — nie.

---

## 2. Bramki i orkiestracja

| Narzędzie | Co robi | RDNA4 | Werdykt |
| :-- | :-- | :-- | :-- |
| **llama-swap** | przełącza modele za jednym adresem | ✅ | ⭐ **masz i używaj** |
| **LiteLLM** | jedno API do 100+ dostawców (lokalnych i chmurowych) | ✅ | ⭐ **weź przy hybrydzie** (część 10) |
| **OpenRouter** | bramka chmurowa | n/d | nie dla offline |
| **RouteLLM** | uczy się routować tanie/drogie | ✅ | ciekawe po części 8 §4 |

### 2.1 LiteLLM — wart uwagi

```bash
python3 -m venv $VENVS/litellm
$VENVS/litellm/bin/pip install 'litellm[proxy]'

cat > $KURS/litellm.yaml <<'EOF'
model_list:
  - model_name: lokalny-maly
    litellm_params:
      model: openai/gpt-oss-20b
      api_base: http://127.0.0.1:8081/v1
      api_key: nieuzywany
  - model_name: lokalny-duzy
    litellm_params:
      model: openai/qwen3-32b
      api_base: http://127.0.0.1:8082/v1
      api_key: nieuzywany
EOF

$VENVS/litellm/bin/litellm --config $KURS/litellm.yaml --port 4000
```

⭐ **Dlaczego to ma sens:** jedno API dla modeli lokalnych **i** Claude (część 10).
Zmiana modelu = zmiana jednego stringa. Ma też wbudowane liczenie kosztów i limity.

---

## 3. Interfejsy użytkownika

| Narzędzie | Opis | RDNA4 | Werdykt |
| :-- | :-- | :-- | :-- |
| **Open WebUI** | ⭐ najpopularniejszy; czat, RAG, wielu użytkowników, wtyczki | ✅ | ⭐ **weź, gdy chcesz UI** |
| **LibreChat** | podobny, mocniejszy w zarządzaniu użytkownikami | ✅ | dobra alternatywa |
| **AnythingLLM** | nastawiony na RAG z dokumentów, desktop + serwer | ✅ | ⭐ dobry do **demo dla klienta** |
| **Text Generation WebUI** | „oobabooga", wiele backendów, dużo suwaków | ⚠️ | do eksperymentów z próbkowaniem |
| **SillyTavern** | zarządzanie postaciami, bardzo rozbudowane prompty | ✅ | nie Twój przypadek |
| **Chatbox / Jan** | lekkie klienty desktopowe | ✅ | gdy chcesz tylko okno |

```bash
# Open WebUI - najprosciej (wymaga Dockera albo pip)
python3 -m venv $VENVS/webui
$VENVS/webui/bin/pip install open-webui
OPENAI_API_BASE_URL=http://127.0.0.1:8080/v1 \
  $VENVS/webui/bin/open-webui serve --port 3000
```

💡 **Dla produktu księgowego AnythingLLM jest wart obejrzenia** — ma gotowe wgrywanie
dokumentów, izolację „workspace'ów" per klient i cytowania. **Zanim go weźmiesz, zrozum,
że robi to samo, co Twoja część 4 — tylko bez Twojej kontroli nad chunkingiem.**

---

## 4. Wymuszanie struktury

Część 3 robiła to gramatykami GBNF. Alternatywy:

| Narzędzie | Podejście | RDNA4 | Kiedy |
| :-- | :-- | :-- | :-- |
| **GBNF w llama.cpp** | gramatyka w silniku | ✅ | ⭐ **masz, wystarcza** |
| **XGrammar** | szybkie gramatyki, używane przez vLLM/SGLang | ⚠️ | gdy przejdziesz na vLLM |
| **Outlines** | biblioteka Pythona, regex/JSON/Pydantic | ⚠️ | gdy potrzebujesz Pydantic |
| **Guidance** | język szablonów z przeplotem generowania | ⚠️ | złożone przepływy |
| **lm-format-enforcer** | filtr tokenów, integruje się z wieloma backendami | ⚠️ | alternatywa dla Outlines |
| **Instructor** | walidacja Pydantic + retry (nie wymusza!) | ✅ | ⚠️ **retry ≠ gwarancja** |

⚠️ **Rozróżnienie, które ma znaczenie:** Outlines/XGrammar/GBNF **wymuszają na poziomie
próbkowania** — wynik jest gwarantowany. Instructor **próbuje i powtarza** — gwarancji nie ma.
Dla lokalnego modelu 20B ta różnica jest krytyczna (część 3 §2.1).

---

## 5. Bazy wektorowe

| Narzędzie | Typ | RDNA4 | Kiedy |
| :-- | :-- | :-- | :-- |
| **sqlite + Python** (część 4) | plik | ✅ | ⭐ **do 100k fragmentów — masz** |
| **sqlite-vec** | rozszerzenie sqlite | ✅ | ⭐ gdy liniowe skanowanie zwolni |
| **LanceDB** | plikowa, kolumnowa | ✅ | ⭐ **dobry następny krok** — bez serwera, szybka |
| **Qdrant** | serwer (Rust) | ✅ | gdy potrzebujesz filtrów i skali |
| **Chroma** | serwer/plik (Python) | ✅ | popularna, prosta, wolniejsza |
| **Milvus** | serwer rozproszony | ✅ | przesada poniżej milionów wektorów |
| **pgvector** | rozszerzenie PostgreSQL | ✅ | ⭐ gdy **już masz Postgresa** |
| **FAISS** | biblioteka | ✅ (CPU) | gdy chcesz sam sterować indeksem |

### 5.1 Ścieżka rozwoju

```
część 4 (sqlite + Python)  →  sqlite-vec  →  LanceDB  →  Qdrant
      < 100k fragmentów       < 1 mln       < 10 mln    powyżej
```

```bash
# sqlite-vec - najmniejszy skok z czesci 4
python3 -m venv $VENVS/kurs
$VENVS/kurs/bin/pip install sqlite-vec
```

💡 **Nie przeskakuj od razu na Qdranta.** Twoja baza z części 4 wystarcza do dziesiątek
tysięcy fragmentów i **rozumiesz ją w całości**. Migruj, gdy zmierzysz, że wyszukiwanie
trwa za długo — nie wcześniej.

---

## 6. Embeddingi i reranking

### 6.1 Modele embeddingowe

| Model | Wymiar | Polski | Uwagi |
| :-- | --: | :-- | :-- |
| **bge-m3** | 1024 | ⭐ bardzo dobry | ⭐ **polecany w części 4**; do 8192 tok |
| multilingual-e5-large | 1024 | dobry | wymaga prefiksów `query:`/`passage:` |
| jina-embeddings-v3 | 1024 | dobry | świetny na długich tekstach |
| Qwen3-Embedding | 1024–4096 | dobry | nowy, mocny, kilka rozmiarów |
| nomic-embed-text | 768 | przeciętny | otwarte dane treningowe |
| **mmlw-roberta** (PL) | 1024 | ⭐ **dedykowany polski** | ⭐ **warto przetestować** |

⭐ **`mmlw` to polski model embeddingowy** z Politechniki Wrocławskiej. **Zmierz go
przeciwko `bge-m3`** metodą „marginesu" z części 4 §2.4 — na polskim tekście księgowym
może wygrać.

### 6.2 Reranking

| Model / narzędzie | Opis |
| :-- | :-- |
| **bge-reranker-v2-m3** | ⭐ dedykowany reranker cross-encoder, wielojęzyczny |
| **jina-reranker-v2** | szybki, wielojęzyczny |
| LLM jako sędzia (część 4 §6.2) | działa, ale **wolniejsze** niż dedykowany reranker |

💡 **Dedykowany reranker jest 10–50× szybszy niż LLM w tej roli** i zwykle trafniejszy.
Jeśli reranking z części 4 jest u Ciebie wąskim gardłem — to jest właściwa wymiana.

### 6.3 Serwery embeddingów

| Narzędzie | Uwagi |
| :-- | :-- |
| **llama-server `--embedding`** | ✅ **masz** — wystarcza |
| **Infinity** | szybki serwer embeddingów i rerankerów, OpenAI API |
| **TEI** (HuggingFace) | produkcyjny, ⚠️ wsparcie ROCm ograniczone |

---

## 7. Przetwarzanie dokumentów i OCR

⭐ **To jest kategoria, która dla Ciebie znaczy najwięcej** — pracujesz z fakturami,
umowami i skanami.

| Narzędzie | Co robi | RDNA4 | Werdykt |
| :-- | :-- | :-- | :-- |
| **Docling** (IBM) | ⭐ PDF/DOCX/PPTX → strukturalny Markdown; **rozumie tabele i układ** | ✅ | ⭐⭐ **zacznij od tego** |
| **Marker** | PDF → Markdown, bardzo dobra jakość | ⚠️ (torch) | świetny do długich dokumentów |
| **Surya** | detekcja układu, OCR, tabele; **wspiera polski** | ⚠️ (torch) | mocny OCR |
| **olmOCR** | OCR oparty na modelu VL | ⚠️ | nowy, dobre wyniki |
| **PaddleOCR** | klasyczny OCR, wiele języków | ⚠️ | dojrzały, szybki |
| **Tesseract** | klasyczny OCR | ✅ | ⭐ **łatwy start**, `apt install tesseract-ocr-pol` |
| **unstructured** | uniwersalny parser wielu formatów | ✅ | dobry do mieszanych źródeł |
| **PyMuPDF** (`fitz`) | szybkie wyciąganie tekstu z PDF | ✅ | ⭐ gdy PDF **ma** warstwę tekstową |
| **pdfplumber** | wyciąganie tabel z PDF | ✅ | ⭐ dobry do tabel |
| **model VL** (część 5) | czyta obraz bezpośrednio | ✅ | gdy układ jest nietypowy |

### 7.1 ⭐ Strategia dla faktur — hierarchia kosztu

```
1. PDF ma warstwę tekstową?         → PyMuPDF          (milisekundy, darmowe)
2. PDF to skan, układ typowy?       → Docling/Tesseract (sekundy)
3. Układ nietypowy, zdjęcie z ręki? → model VL (część 5) (dziesiątki sekund)
```

⚠️ **Nie wysyłaj każdej faktury do modelu VL.** To jest najdroższa opcja. **Sprawdź
najpierw, czy PDF nie ma już tekstu** — połowa faktur, które dostajesz mailem, go ma.

```bash
# Szybki test: czy PDF ma warstwe tekstowa?
python3 -m venv $VENVS/dok
$VENVS/dok/bin/pip install pymupdf docling pdfplumber

$VENVS/dok/bin/python - <<'PYEOF'
import sys, fitz   # PyMuPDF
p = "/sciezka/do/faktura.pdf"
try:
    d = fitz.open(p)
    tekst = "".join(page.get_text() for page in d)
    if len(tekst.strip()) > 100:
        print(f"✅ PDF MA tekst ({len(tekst)} znaków) — użyj PyMuPDF, nie modelu VL")
        print(tekst[:400])
    else:
        print("⚠️ PDF to SKAN — potrzebny OCR albo model VL")
except Exception as e:
    print("błąd:", e)
PYEOF
```

```bash
# Docling: PDF -> Markdown ze struktura
sudo apt install -y tesseract-ocr tesseract-ocr-pol
$VENVS/dok/bin/python -c "
from docling.document_converter import DocumentConverter
r = DocumentConverter().convert('/sciezka/faktura.pdf')
print(r.document.export_to_markdown()[:1500])
"
```

⭐ **Docling zachowuje tabele jako tabele Markdown.** Dla faktur z pozycjami to jest
ogromna różnica w porównaniu z płaskim OCR — model dostaje strukturę, nie sieczkę.

---

## 8. Mowa — STT i TTS

### 8.1 Rozpoznawanie mowy (STT)

| Narzędzie | Opis | RDNA4 | Werdykt |
| :-- | :-- | :-- | :-- |
| **whisper.cpp** | ⭐ C++, GGUF, HIP | ✅ | ⭐ **część 5, masz** |
| **faster-whisper** | CTranslate2, szybszy | ⚠️ (CUDA-centryczny) | świetny na NVIDII |
| **WhisperX** | Whisper + wyrównanie + **diaryzacja** | ⚠️ (torch) | ⭐ gdy potrzebujesz „kto mówił" |
| **Whisper.cpp streaming** | transkrypcja na żywo | ✅ | do dyktowania ciągłego |
| **Vosk** | lekki, offline, działa na słabym sprzęcie | ✅ | gdy chcesz minimalizmu |

### 8.2 Synteza mowy (TTS)

| Narzędzie | Polski | RDNA4 | Werdykt |
| :-- | :-- | :-- | :-- |
| **Piper** | ⭐ **kilka głosów PL** | ✅ (CPU) | ⭐⭐ **część 5, polecany** |
| **Kokoro** | ⚠️ ograniczony | ✅ | bardzo dobra jakość EN, mały |
| **XTTS v2** (Coqui) | ✅ + **klonowanie głosu** | ⚠️ (torch) | gdy chcesz własny głos |
| **F5-TTS** | ⚠️ | ⚠️ | świetna jakość, klonowanie |
| **espeak-ng** | ✅ | ✅ | ⛔ brzmi robotycznie — tylko awaryjnie |
| **`llama-tts`** | ⚠️ obcy akcent | ✅ | masz, ale P34 |

⭐ **Dla polskiego: Piper.** Działa na CPU, nie konkuruje o VRAM, ma naturalne głosy.
**XTTS v2 wtedy, gdy potrzebujesz konkretnego głosu** (np. klonowanie własnego).

---

## 9. Frameworki agentowe

⚠️ **Przeczytaj to po częściach 6–7, nie przed.** Wtedy zobaczysz, że każdy z nich robi
to, co Twój `agent.py` — i ocenisz, czy jego abstrakcje Ci pomagają, czy przeszkadzają.

| Framework | Filozofia | Werdykt |
| :-- | :-- | :-- |
| **LangChain / LangGraph** | wszystko dla wszystkich; LangGraph = graf stanów | ⚠️ **ciężki**; LangGraph sam w sobie sensowny |
| **LlamaIndex** | nastawiony na RAG i indeksowanie | ⭐ dobry, jeśli RAG to rdzeń |
| **smolagents** (HF) | ⭐ **minimalistyczny**, agent pisze kod | ⭐ **najbliższy Twojej filozofii** |
| **Pydantic AI** | typowanie i walidacja jako fundament | ⭐ dobry dla ustrukturyzowanych wyjść |
| **CrewAI** | zespoły agentów z rolami | fajne demo, trudne w debugowaniu |
| **AutoGen** (MS) | konwersacje wieloagentowe | badawczy, ciężki |
| **Haystack** | potoki produkcyjne | solidny, mniej modny |
| **DSPy** | ⭐ **optymalizuje prompty automatycznie** | ⭐ ciekawy, inna kategoria |

### 9.1 Co realnie warto wziąć z tych frameworków

| Element | Skąd | Dlaczego |
| :-- | :-- | :-- |
| **maszyna stanów agenta** | LangGraph | Twoja pętla `while` jest prosta; przy rozgałęzieniach graf jest czytelniejszy |
| **automatyczna optymalizacja promptów** | DSPy | ⭐ **realnie nowa wartość** — dobiera prompt pod Twoje metryki |
| parsery dokumentów | LlamaIndex | gotowe wczytywanie dziesiątków formatów |
| **nic więcej** | — | resztę masz w częściach 3–8 |

⭐ **DSPy jest jedyną pozycją na tej liście, która robi coś, czego nie napisałeś sam.**
Zamiast ręcznie poprawiać prompt, definiujesz metrykę (masz ją — część 3 §6) i DSPy
szuka lepszego promptu. **To jest naturalna kontynuacja Twojego zestawu ewaluacyjnego.**

---

## 10. Gotowi agenci kodujący

| Narzędzie | Opis | Model lokalny? |
| :-- | :-- | :-- |
| **Aider** | ⭐ agent kodujący w terminalu, mocna integracja z git | ✅ **tak** |
| **OpenHands** (dawniej OpenDevin) | agent w kontenerze, przeglądarka + terminal | ✅ tak |
| **Continue** | wtyczka do VS Code / JetBrains | ✅ tak |
| **Cline** | wtyczka VS Code, agentowa | ✅ tak |
| **goose** (Block) | agent CLI z rozszerzeniami | ✅ tak |

```bash
# Aider z Twoim lokalnym modelem
python3 -m venv $VENVS/aider
$VENVS/aider/bin/pip install aider-install && $VENVS/aider/bin/aider-install

cd ~/projekt
OPENAI_API_BASE=http://127.0.0.1:8081/v1 OPENAI_API_KEY=x \
  $VENVS/aider/bin/aider --model openai/gpt-oss-20b
```

⭐ **Uruchom Aidera i porównaj z własnym `agent.py`.** Zobacz, jak rozwiązał te same
problemy: edycję plików, kontekst, zatwierdzanie. **To jest najlepsza lekcja projektowa
w tym rozdziale** — i będzie zrozumiała tylko dlatego, że najpierw napisałeś swojego.

---

## 11. Obserwowalność

| Narzędzie | Co daje | Werdykt |
| :-- | :-- | :-- |
| **Langfuse** | ⭐ ślady, koszty, ewaluacja; **self-hosted** | ⭐ **weź, gdy dziennik z części 6 przestanie wystarczać** |
| **Phoenix** (Arize) | ślady + ewaluacja, lokalnie | dobra alternatywa |
| **OpenLLMetry** | OpenTelemetry dla LLM | gdy masz już stos OTel |
| **netdata** | metryki systemowe i GPU | ⭐ **masz** |
| własny dziennik (część 6) | pełna kontrola | ⭐ **na start wystarcza** |

💡 **Langfuse ma sens, gdy masz wielu użytkowników albo chcesz porównywać wersje
promptów na wykresach.** Dla jednego agenta Twój JSONL jest wygodniejszy — `grep` działa
od razu.

---

## 12. Ewaluacja

⭐ **Najbardziej niedoceniana kategoria w całym ekosystemie.**

| Narzędzie | Opis | Werdykt |
| :-- | :-- | :-- |
| **promptfoo** | ⭐ deklaratywne testy promptów w YAML, porównania side-by-side | ⭐⭐ **weź to** |
| **Ragas** | metryki specyficzne dla RAG (wierność, trafność) | ⭐ pasuje do części 4 |
| **DeepEval** | testy LLM w stylu pytest | dobry, jeśli lubisz pytest |
| **lm-evaluation-harness** | standardowe benchmarki akademickie | do porównań modeli |
| **własny harness** (część 3 §6) | pełna kontrola, Twoja domena | ⭐ **fundament** |

```bash
# promptfoo - porownaj trzy modele na tym samym zestawie
npm install -g promptfoo

cat > $KURS/promptfooconfig.yaml <<'EOF'
providers:
  - id: openai:chat:gpt-oss-20b
    config: { apiBaseUrl: http://127.0.0.1:8081/v1, apiKey: x }
  - id: openai:chat:qwen3-32b
    config: { apiBaseUrl: http://127.0.0.1:8082/v1, apiKey: x }

prompts:
  - "Wyciągnij z faktury numer, datę i kwotę brutto jako JSON:\n{{tekst}}"

tests:
  - vars:
      tekst: "FV/2025/01/0001 z 2025-01-10. Netto 1000 zł, VAT 23%, brutto 1230 zł."
    assert:
      - type: is-json
      - type: javascript
        value: JSON.parse(output).brutto === 1230
  - vars:
      tekst: "Rachunek A/12/2025 z 2025-06-30, zwolniony z VAT, 500,00 zł."
    assert:
      - type: is-json
      - type: contains
        value: "A/12/2025"
EOF

cd $KURS && promptfoo eval && promptfoo view
```

⭐ **`promptfoo view` daje tabelę porównawczą w przeglądarce.** To jest to samo, co Twój
harness z części 3, ale z UI i wygodnym porównywaniem wielu modeli naraz. **Warto —
zwłaszcza gdy będziesz pokazywał wyniki klientowi.**

---

## 13. Dostrajanie (fine-tuning)

| Narzędzie | Opis | RDNA4 | Werdykt |
| :-- | :-- | :-- | :-- |
| **llama-finetune** | ⭐ masz, LoRA w llama.cpp | ✅ | do nauki mechanizmu (część 8 §6) |
| **Unsloth** | 2× szybszy, 70 % mniej pamięci | ⚠️ (CUDA-first, ROCm eksperymentalne) | najlepszy na NVIDII |
| **Axolotl** | konfiguracja YAML, dużo metod | ⚠️ ROCm możliwe | dojrzały |
| **torchtune** (PyTorch) | oficjalny, czysty | ⚠️ ROCm przez PyTorch-ROCm | ⭐ **najpewniejsza droga na ROCm** |
| **LLaMA-Factory** | UI + CLI, wiele metod | ⚠️ | wygodny |
| **PEFT** (HF) | biblioteka bazowa LoRA/QLoRA | ⚠️ | fundament innych |

⚠️ **Realia dostrajania na RDNA4:** PyTorch-ROCm wspiera gfx1201, ale ekosystem
(bitsandbytes, flash-attention, xformers) **jest nierówny**. Spodziewaj się zachodu.

💡 **Zanim zaczniesz dostrajać, przeczytaj część 8 §6.1 jeszcze raz.** W 80 % przypadków
odpowiedzią jest RAG (część 4) albo gramatyka (część 3), nie LoRA.

---

## 14. Kwantyzacja

| Narzędzie | Formaty | RDNA4 | Werdykt |
| :-- | :-- | :-- | :-- |
| **llama-quantize** | GGUF: Q2–Q8, K, IQ | ✅ | ⭐ **masz** (część 8 §5) |
| **llama-imatrix** | macierz istotności | ✅ | ⭐ **masz** |
| **AutoAWQ** | AWQ (4-bit, dla vLLM) | ⚠️ | gdy przejdziesz na vLLM |
| **GPTQModel** | GPTQ | ⚠️ | j.w. |
| **ExLlamaV3 (EXL3)** | najlepsze kwantyzacje | ❌ CUDA | niedostępne |
| **llm-compressor** | kwantyzacja dla vLLM | ⚠️ | ekosystem vLLM |

💡 **Zostań przy GGUF.** Jest najlepiej wspierany na ROCm, masz do niego wszystkie
narzędzia i cała Twoja metodyka pomiarowa jest na nim zbudowana.

---

## 15. Co wziąć na start

### 15.1 Trzy rzeczy do wzięcia od razu

| # | Narzędzie | Dlaczego teraz |
| --: | :-- | :-- |
| **1** | **Docling** | faktury i umowy → strukturalny Markdown; **największy zysk dla Twojej domeny** |
| **2** | **promptfoo** | porównywanie modeli i promptów z UI; rozszerza część 3 §6 |
| **3** | **Piper** | polski TTS (część 5 §5.2) — jeśli jeszcze nie masz |

### 15.2 Do przetestowania w drugiej kolejności

| Narzędzie | Po co |
| :-- | :-- |
| **Aider** | zobacz, jak inni rozwiązali Twoją część 6 |
| **mmlw** (embeddingi PL) | może pobić `bge-m3` na polskim |
| **bge-reranker-v2-m3** | szybszy reranking niż LLM-jako-sędzia |
| **LanceDB** | następny krok po sqlite z części 4 |
| **DSPy** | automatyczna optymalizacja promptów pod Twoje metryki |

### 15.3 Świadomie odkładam na później

| Narzędzie | Dlaczego nie teraz |
| :-- | :-- |
| **vLLM** | duży zachód na gfx1201; wróć, gdy zmierzysz, że llama.cpp jest wąskim gardłem |
| **LangChain** | ciężkie abstrakcje nad tym, co już umiesz napisać |
| **Ollama / LM Studio** | rozwalają metodykę pomiarową |
| **Qdrant / Milvus** | przesada poniżej miliona wektorów |
| **Unsloth** | CUDA-first |

### 15.4 ⭐ Zasada, którą warto zapamiętać

> **Bierz narzędzie wtedy, gdy potrafisz opisać, czego dokładnie ono za Ciebie nie zrobi.**

Po częściach 1–8 potrafisz to dla każdej pozycji w tym katalogu. **To jest prawdziwy
efekt tego kursu** — nie to, że napisałeś własną bazę wektorową, tylko że **wiesz, co
kupujesz**, biorąc cudzą.

---

## Ćwiczenia

1. **Docling na prawdziwej fakturze.** Weź PDF faktury, przepuść przez Docling i porównaj
   z tym, co dał model VL z części 5. Zmierz czas i trafność. **Który wygrał i w jakim typie
   dokumentu?**
2. **promptfoo na zestawie z części 3.** Przenieś `faktury.jsonl` do konfiguracji promptfoo
   i porównaj trzy modele w UI.
3. **mmlw vs bge-m3.** Zmierz „margines" metodą z części 4 §2.4 na polskim tekście
   księgowym. Który lepiej rozdziela?
4. **Aider vs Twój agent.** To samo zadanie kodujące na tym samym modelu. Porównaj liczbę
   tur, jakość i **to, co Aider robi inaczej**. Zapisz trzy rzeczy, które od niego
   zapożyczysz.
5. **Ustal swój stos.** Napisz w `HANDOFF.md` jedną tabelę: warstwa → wybrane narzędzie →
   dlaczego → co odrzuciłeś. **To jest dokument architektury Twojego produktu.**

---

**Następna część: `10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md`** — krótki rozdział: kiedy i jak
dołożyć Claude API do lokalnego stosu, nie tracąc kontroli nad prywatnością.
