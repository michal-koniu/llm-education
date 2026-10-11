# Kurs: od modelu do własnego agenta — indeks

**Utworzony: 22 września 2026.** Dla Michała.

> **Cel całości.** Po przejściu tego kursu potrafisz **zbudować od zera własnego agenta
> klasy OpenClaw / Claude Code** — pętlę, która czyta pliki, pisze kod, uruchamia polecenia,
> widzi obrazy, słucha i mówi, pamięta kontekst i **działa offline na Twoim sprzęcie** —
> i rozumiesz każdą warstwę pod nią.
>
> Nie „umiesz użyć frameworka". Rozumiesz, dlaczego framework robi to, co robi, i umiesz to
> napisać sam. **Dopiero potem świadomie wybierasz gotowe narzędzia.**

---

## Droga

```
  CZĘŚĆ 1 ──► rozmawiasz z modelem, rozumiesz stos
     │        tokeny/wagi/runtime/serwer, llama-cli, llama-server, curl
     ▼
  CZĘŚĆ 2 ──► CZUJESZ model
     │        tokenizer, logity, próbkowanie, KV-cache, embeddingi
     ▼
  CZĘŚĆ 3 ──► ZMUSZASZ model do posłuszeństwa
     │        szablon czatu, gramatyki GBNF, determinizm, ewaluacja
     ▼
  CZĘŚĆ 4 ──► dajesz modelowi PAMIĘĆ
     │        embeddingi, baza wektorowa, chunking, cytowania, kompakcja
     ▼
  CZĘŚĆ 5 ──► dajesz mu ZMYSŁY
     │        wizja, Whisper (słuch), Piper (mowa) — plus lista sprzętu
     ▼
  CZĘŚĆ 6 ──► budujesz PĘTLĘ AGENTA          ◄── tu powstaje „Twój OpenClaw"
     │        narzędzia, edycja plików, shell, błędy, subagenci, dziennik
     ▼
  CZĘŚĆ 7 ──► zamykasz go w KLATCE
     │        bwrap, limity, sieć, prompt injection, audyt, monitoring
     ▼
  CZĘŚĆ 8 ──► robisz to SZYBKO
     │        prompt cache, dekodowanie spekulatywne, kwantyzacja, LoRA, 4 karty
     ▼
  CZĘŚĆ 9 ──► POZNAJESZ EKOSYSTEM
     │        alternatywne silniki, OCR, bazy, frameworki — z oceną pod RDNA4
     ▼
  CZĘŚĆ 10 ─► opcjonalnie: HYBRYDA z Claude API
              routing, granica prywatności, offline-first
```

⚠️ **Kolejność nie jest dekoracją.** Część 6 nie da się zrozumieć bez części 3 (bez
gramatyk lokalny model nie wywoła narzędzia niezawodnie). Część 8 nie da się zrozumieć bez
części 2 (bez KV-cache nie wiesz, co optymalizujesz). **Nie przeskakuj — poza częścią 9,
którą możesz czytać kiedykolwiek.**

---

## Pliki

| # | Plik | Poziom | Czego się nauczysz | Czas |
| :-- | :-- | :-- | :-- | :-- |
| 1 | `PODSTAWY-LOKALNYCH-MODELI.md` | ⭐ | ✅ **masz** — stos, pobieranie, `llama-cli`, `llama-server`, `llama-swap`, pierwsze narzędzia | — |
| 2 | `02-WNETRZE-MODELU.md` | ⭐⭐ | tokenizer, logity, **próbkowanie**, **KV-cache**, embeddingi, perplexity | ~4 h |
| 3 | `03-KONTROLA-I-NIEZAWODNOSC.md` | ⭐⭐⭐ | surowy szablon czatu, ⭐ **gramatyki GBNF**, JSON Schema, determinizm, **harness ewaluacyjny** | ~5 h |
| 4 | `04-PAMIEC-RAG-I-KONTEKST.md` | ⭐⭐⭐⭐ | embeddingi, **baza wektorowa od zera**, chunking, BM25, hybryda, cytowania, kompakcja | ~6 h |
| 5 | `05-MULTIMODALNOSC.md` | ⭐⭐⭐⭐ | **wizja** (`llama-mtmd`), **Whisper**, **Piper**, pętla głosowa + ⭐ **lista sprzętu do kupienia** | ~6 h |
| 6 | `06-PETLA-AGENTA-OD-ZERA.md` | ⭐⭐⭐⭐ | ⭐⭐ **pętla agenta**, protokół narzędzi, `read`/`edit`/`bash`, strażnik, subagenci, dziennik | ~8 h |
| 7 | `07-SANDBOX-BEZPIECZENSTWO-MONITORING.md` | ⭐⭐⭐⭐ | `bwrap`, `systemd-run`, kontrola sieci, ⭐ **prompt injection**, audyt, monitoring | ~5 h |
| 8 | `08-OPTYMALIZACJA-OFFLINE.md` | ⭐⭐⭐⭐⭐ | prompt cache, ⭐ **dekodowanie spekulatywne**, routing, własna kwantyzacja, LoRA, 4 karty | ~7 h |
| 9 | `09-KRAJOBRAZ-NARZEDZI.md` | ⭐⭐⭐ | ⭐ **katalog narzędzi** z oceną pod RDNA4: silniki, OCR, bazy, frameworki, ewaluacja | ~3 h |
| 10 | `10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md` | ⭐⭐⭐ | granica prywatności, router hybrydowy, koszty, **offline-first** | ~3 h |

**Łącznie: ~47 godzin pracy z klawiaturą.** To nie jest kurs do przeczytania.

---

## Konwencje we wszystkich plikach

**Binarki llama.cpp nie są w `PATH`.** Wykonaj to raz na sesję terminala:

```bash
cd ~/Desktop/github_repos/llm-education   # katalog repozytorium (u Ciebie może być inny)
source rig-env.sh
```

Utwórz ten plik raz:

```bash
cat > $LLMEDU/rig-env.sh <<'EOF'
# Binarki
export LB=~/llama.cpp/build/bin
export WB=$NARZEDZIA/whisper.cpp/build/bin          # po części 5

# Modele
export M=~/models
export BIELIK=$M/bielik-11b/Bielik-11B-v3.0-Instruct.Q8_0.gguf
export OSS20=$M/gpt-oss-20b/gpt-oss-20b-MXFP4.gguf
export QWEN32=$M/qwen3-32b/Qwen_Qwen3-32B-Q4_K_M.gguf
export QWEN80=$M/qwen3-next-80b/Q4_1/Qwen3-Next-80B-A3B-Instruct-Q4_1-00001-of-00002.gguf
export DRAFT=$M/gpt-oss-120b/eagle3-gpt-oss-120b-Q8_0.gguf
export EMB=$M/embed/bge-m3-f16.gguf        # po części 4
export VL=$M/vl/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf          # po części 5
export VLMM=$M/vl/mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf    # po części 5
export WMODEL=$NARZEDZIA/whisper.cpp/models/ggml-large-v3-turbo.bin  # po części 5

# P12/P32: iGPU jest GPU[2] — wyklucz ją
export HIP_VISIBLE_DEVICES=0,1

# P4: P2P zawiesza host przy 4 kartach
export NCCL_P2P_DISABLE=1
export NCCL_PROTO=Simple
EOF

source $LLMEDU/rig-env.sh
$LB/llama-cli --version    # → 0.4.1-dev (build 1, commit 987498f)
```

### Modele, których używam w przykładach

| Skrót | Rozmiar | Rola w kursie |
| :-- | --: | :-- |
| `$BIELIK` | 11,9 GB | polski, Q8 — ćwiczenia językowe |
| `$OSS20` | 12,1 GB | ⭐ **główny model agenta** — szybki |
| `$QWEN32` | 19,8 GB | mądrzejszy, gęsty — duży w routerze |
| `$QWEN80` | 49,7 GB | MoE — eksperymenty z `-cmoe` |
| `$DRAFT` | 849 MB | ⭐ **model szkicowy** — dekodowanie spekulatywne (część 8) |

---

## Zasady, których trzymam się w całym kursie

1. **Żadnych frameworków, dopóki nie napiszesz tego sam.** Framework poznasz w części 9
   i będziesz wiedział, co ukrywa.
2. **Czysty Python, bez `numpy` i bez `torch`.** Iloczyn skalarny napisany pętlą uczy
   więcej niż `np.dot()`. Gdzie potrzeba biblioteki — mówię wprost.
3. **Każde polecenie ma wytłumaczone, co robi i jakiego wyjścia oczekiwać.**
4. **Każdy rozdział kończy się ćwiczeniem, które coś realnie produkuje.**
5. **Nie optymalizuj bez pomiaru.** Każda dźwignia w części 8 ma liczbę przed i po.
6. **Pułapki (`P…`) numerowane wspólnie z `TECHNIKA.md`.** Sprzętowe: P1–P18.
   **Programowe z tego kursu: P20–P52.**

---

## Rejestr pułapek programowych

| ID | Pułapka | Część |
| :-- | :-- | :-- |
| P20 | Liczenie tokenów tokenizerem innego modelu | 2 |
| P21 | `repeat_penalty > 1.0` psuje generowanie JSON | 2 |
| P22 | Kontekst to VRAM: wagi + KV-cache razem | 2 |
| P23 | Przepełnienie kontekstu bywa **ciche** | 2 |
| P24 | Model generatywny jako embeddingowy — słaby | 2 |
| P25 | Nie każdy model ma rolę `system` | 3 |
| P26 | Gramatyka bez wyjścia zapętla generowanie | 3 |
| P27 | Gramatyka kosztuje 10–30 % tok/s | 3 |
| P28 | Jeden profil próbkowania dla całego agenta | 3 |
| P29 | Fragment bez metadanych — słabo znajdowany | 4 |
| P30 | Wektory bezużyteczne dla identyfikatorów | 4 |
| P31 | Kompakcja gubi dokładne liczby | 4 |
| P32 | iGPU jako `GPU[2]` — modele lądują na 2 GB | 5 |
| P33 | `mmproj` niezgodny z modelem | 5 |
| P34 | OuteTTS słabo mówi po polsku | 5 |
| P35 | TTS bez normalizacji liczb | 5 |
| P36 | Whisper halucynuje na ciszy i szumie | 5 |
| P37 | Model zapomina wywołać `odpowiedz` | 6 |
| P38 | Brak kontroli świeżości — agent zjada zmiany człowieka | 6 |
| P39 | Biała lista poleceń **nie jest** piaskownicą | 6 |
| P40 | Jedna obserwacja wypełnia całe okno kontekstu | 6 |
| P41 | Delegacja ma koszt stały | 6 |
| P42 | `--bind` zamiast `--ro-bind` na katalogu systemowym | 7 |
| P43 | Podłączenie katalogu domowego kończy piaskownicę | 7 |
| P44 | Brak `--new-session` — wstrzykiwanie do terminala | 7 |
| P45 | `HTTP_PROXY` to konwencja, nie wymuszenie | 7 |
| P46 | Zmienny prompt systemowy zabija prompt cache | 8 |
| P47 | Model szkicowy zjada VRAM i może zwolnić | 8 |
| P48 | Routing między serwerami unieważnia cache | 8 |
| P49 | PPL na tekście kalibracyjnym jest sztucznie dobre | 8 |
| P50 | `-np` dzieli kontekst, nie mnoży wydajności | 8 |
| P51 | Filtr regexowy przepuści nieprzewidziane | 10 |
| P52 | Ciche uzależnienie od chmury | 10 |

---

## Gdzie co leży

| Plik | Rola |
| :-- | :-- |
| `HANDOFF.md` | **stan projektu** — co zrobione, co następne |
| `TECHNIKA.md` | **procedury na tej maszynie** — inwentarz, pułapki sprzętowe P1–P18 |
| `KARTY-3-I-4-PLAN-PODLACZENIA.md` | rozbudowa do 4 kart |
| **kurs `00`–`10`** | **jak to działa i jak zbudować na tym agenta** |
| `BIZNES.md` | teza, rynek, produkt |

**Katalogi, które powstaną w trakcie kursu:**

```
$KURS/       narzędzia pomiarowe, RAG, zestawy ewaluacyjne
$AGENT/      ⭐ Twoja pętla agenta, piaskownica, audyt, dzienniki
$NARZEDZIA/whisper.cpp/  STT (część 5)
$NARZEDZIA/piper/      TTS (część 5)
~/models/     modele: embed/, vl/, tts/, wlasne/
```

---

## Zanim zaczniesz — sprawdź stanowisko

```bash
# 1. Karty widoczne? (oczekuj 2x R9700 + iGPU jako GPU[2])
rocm-smi --showid

# 2. Binarki dzialaja?
source $LLMEDU/rig-env.sh && $LB/llama-cli --version

# 3. Modele na miejscu? (oczekuj 7 plikow)
find ~/models -name '*.gguf' | wc -l

# 4. Miejsce na dysku? (oczekuj ~1,5 T)
df -h /home | tail -1
```

⚠️ **Pułapka P12/P32 — iGPU też jest urządzeniem ROCm.** `rocm-smi` pokazuje trzy
urządzenia: `GPU[0]`, `GPU[1]` to karty R9700 (34,2 GB każda), `GPU[2]` to **zintegrowana
grafika z 2 GB**. Małe modele potrafią tam wylądować i działać 50× wolniej.
**`HIP_VISIBLE_DEVICES=0,1` jest w `rig-env.sh` właśnie po to.**

⚠️ **Po dołożeniu kart 3 i 4 numeracja zmieni się znowu (P13).** Przemapuj przez
`amd-smi list` i zaktualizuj `rig-env.sh`.

---

**Start: `02-WNETRZE-MODELU.md`.**

---

## Po tym kursie: kurs 2

**`kurs2/00-INDEKS.md`** — ⭐ **aplikacje agentowe na modelach lokalnych.**
Dziewiętnaście części, ~102 h. Kurs 1 uczy, **jak działa model**. Kurs 2 uczy,
**jak zbudować wokół niego system, któremu można zaufać**:

```
harness na wiele okien kontekstu · pamięć bi-temporalna · code-mode
piaskownica produkcyjna · proaktywność · flota trzech agentów
ewaluacja i ślady · OWASP ASI01–ASI10 · wydania i runbook
```

Buduje **jeden rosnący system** `$OSA/` z trzema agentami osobistymi.
Każda część ma **eksperyment z pustą tabelą na Twój pomiar**. Pułapki **P60–P139**.

⚠️ **Nie zaczynaj kursu 2 przed częścią 6 kursu 1** — cały kurs 2 stoi na pętli
agenta, którą tam budujesz.
