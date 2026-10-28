# 05 · Opakowania: Ollama, LM Studio i reszta

**Po co ten rozdział.** W rozdziałach 02–04 poznałeś silnik: jak z tokenów robi się kolejne tokeny, czym jest GGUF i co robi `llama-server`. Ten rozdział jest o warstwie **nad silnikiem**: o programach, które sprawiają, że "uruchomienie modelu" to jedno polecenie albo jedno kliknięcie. Po przeczytaniu będziesz w stanie powiedzieć, co dokładnie wrapper dodaje do llama.cpp, za co za to płacisz (kontrola, opóźnienie względem upstreamu, domyślne wartości, zależność od firmy), czym różnią się Ollama, LM Studio, llmman, Jan, GPT4All, LocalAI, Lemonade, Docker Model Runner i RamaLama, które z nich w ogóle nie są runtime'ami (Open WebUI, AnythingLLM) oraz co ta wiedza zmienia w konfiguracji referencyjnej: 4× Radeon AI PRO R9700 (gfx1201, ROCm), llama.cpp + llama-swap, do tego Mac.

> ⚠️ **Niczego tu nie uruchamiałem.** Cały przegląd to *desk research* i czytanie kodu: README, dokumentacja, API GitHuba, płytkie klony repozytoriów (stan z 19 października 2026). Żadnego z opisanych programów nie instalowałem, żadnego benchmarku nie wykonałem. Dla Ollamy i llmmana czytałem kod w klonie; dla Jana, LocalAI, Lemonade, Docker Model Runnera, RamaLamy, GPT4All, Open WebUI i AnythingLLM — README, pliki z drzewa repozytorium i wybrane pliki źródłowe pobrane przez API, bez pełnego checkoutu. Tam, gdzie nie ma weryfikacji, piszę to wprost.

**Jak czytać znaczniki wiarygodności.** Fakt bez znacznika = sprawdzony w źródle pierwotnym (kod, API GitHuba, dokument projektu — podaję ścieżkę lub adres). *(dane projektu)* / *(dane firmy)* = tak twierdzi sam autor, bez niezależnej weryfikacji. *(prasa)* / *(źródło zewnętrzne)* = np. Wikipedia. *(niezweryfikowane)* / *(moje wyliczenie)* = wniosek albo coś, czego nie umiem potwierdzić.

## Spis treści

1. [Idea opakowania: co dodaje, ile kosztuje](#1-idea-opakowania)
2. [Ollama w głąb](#2-ollama-w-głąb)
3. [LM Studio w głąb](#3-lm-studio-w-głąb)
4. [llmman: modele jako obrazy OCI](#4-llmman-modele-jako-obrazy-oci)
5. [Jan, GPT4All, LocalAI, Lemonade, Docker Model Runner, RamaLama](#5-pozostałe-opakowania)
6. [Frontendy, które nie są runtime'ami: Open WebUI i AnythingLLM](#6-frontendy-które-nie-są-runtimeami)
7. [Co się psuje, gdy sponsor zmieni zdanie](#7-co-się-psuje-gdy-sponsor-zmieni-zdanie)
8. [Co z tego dla konfiguracji referencyjnej](#8-co-z-tego-dla-konfiguracji-referencyjnej)
9. [Czego nie ustaliłem](#9-czego-nie-ustaliłem)

Powiązane rozdziały: silnik, który wszystkie te programy opakowują — [`04-LLAMA-CPP-I-RODZINA-GGML.md`](04-LLAMA-CPP-I-RODZINA-GGML.md); format plików — [`03-KWANTYZACJA-I-FORMATY.md`](03-KWANTYZACJA-I-FORMATY.md); ścieżka MLX na Macu — [`07-APPLE-MLX-OMLX-I-DS4.md`](07-APPLE-MLX-OMLX-I-DS4.md); silniki serwerowe, które część opakowań potrafi uruchamiać — [`06-SILNIKI-SERWEROWE-VLLM-SGLANG.md`](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md); pieniądze i ludzie — [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md); wybór na koniec — [`09-POROWNANIE-I-WYBOR.md`](09-POROWNANIE-I-WYBOR.md).

---

## 1. Idea opakowania

### 1.1 Gdzie to jest w stosie

Pomyśl o różnicy między silnikiem samochodu a samochodem. `llama-server` to silnik: dostaje ścieżkę do pliku `.gguf`, port i garść flag, a w zamian udostępnia HTTP API do generowania tokenów. Nie wie, skąd wziąć model, nie pamięta, który model ostatnio ładowałeś, nie zwolni VRAM-u po godzinie bezczynności (co prawda `llama-server` ma już własny tryb routera, o nim w sekcji 8). **Opakowanie (*wrapper*) to wszystko dookoła tego silnika.**

Precyzyjnie: wrapper to program, który sam nie liczy macierzy, tylko uruchamia i nadzoruje inny program, który to robi.

```
 aplikacja / agent / IDE / Open WebUI
            │  HTTP: OpenAI / Anthropic / Ollama API
            ▼
 ┌────────────────────────────────────────────┐
 │  OPAKOWANIE (Ollama, LM Studio, Jan, …)    │
 │  · rejestr modeli (pull / push / katalog)  │
 │  · cykl życia (ładuj, trzymaj, zwolnij)    │
 │  · wartości domyślne (kontekst, równoleg.) │
 │  · tłumaczenie API, szablony czatu         │
 │  · GUI / CLI / aktualizacje / pakiet       │
 └───────────────┬────────────────────────────┘
                 │  proces potomny, HTTP na 127.0.0.1:<losowy port>
                 ▼
 ┌────────────────────────────────────────────┐
 │  SILNIK: llama-server (llama.cpp), MLX, …  │  ← tu liczą się tokeny
 └───────────────┬────────────────────────────┘
                 ▼
          ggml / MLX → CUDA, ROCm, Vulkan, Metal, CPU
```

Wniosek, na którym stoi cały rozdział: **niemal wszystkie opakowania uruchamiają ten sam silnik**. W stanie z października 2026 Ollama (część GGUF), LM Studio (część GGUF), Jan, LocalAI (jeden z 60+ backendów), Lemonade, Docker Model Runner, RamaLama i llmman uruchamiają GGUF przez llama.cpp; GPT4All przez własny fork llama.cpp. Różnią się **pakowaniem, dystrybucją modeli, harmonogramem ładowania, nakładkami API i pieniędzmi — nie mnożeniem macierzy**.

### 1.2 Co wrapper dodaje

| Dodatek | Co to znaczy w praktyce | Przykład z tego rozdziału |
|---|---|---|
| **Rejestr modeli** | `ollama pull qwen3` zamiast szukania pliku na Hugging Face, wybierania kwantyzacji i pobierania ręcznie; metadane (szablon, parametry, licencja) jadą razem z wagami | manifest + bloby w Ollamie; obrazy OCI w llmmanie, Docker Model Runnerze, RamaLamie |
| **Cykl życia** | Model ładuje się przy pierwszym żądaniu, siedzi w pamięci przez *keep-alive*, potem jest zwalniany; kilka modeli może współistnieć | `OLLAMA_KEEP_ALIVE` = 5 min; JIT + TTL w LM Studio |
| **Wartości domyślne** | Za ciebie wybiera okno kontekstu, liczbę slotów, liczbę warstw na GPU, *flash attention* | kontekst zależny od ilości VRAM-u w Ollamie |
| **Tłumaczenie API** | Jeden serwer mówi po OpenAI, Anthropic i Ollamie jednocześnie; wiadomości czatu zamieniane na prompt właściwym szablonem, wywołania narzędzi (*tool calls*) parsowane z odpowiedzi | `model/renderers`, `model/parsers` w Ollamie |
| **GUI i pakowanie** | Instalator, aktualizacje, ikona w pasku, wyszukiwarka modeli, czat | LM Studio, Jan, aplikacja Ollamy |
| **Wykrywanie sprzętu** | Sam sprawdza, jakie masz GPU, i dobiera odpowiedni build silnika | `discover/` w Ollamie; wybór obrazu po zmiennej środowiskowej w RamaLamie |

### 1.3 Ile to kosztuje

1. **Kontrola.** Flagi, których potrzebujesz (`--n-cpu-moe`, własny podział tensorów między karty, konkretne ustawienia dekodowania spekulatywnego), są dostępne tylko wtedy, gdy opakowanie je wystawia. Zmiennych `OLLAMA_*` jest mniej niż flag `llama-server`.
2. **Opóźnienie względem upstreamu.** Wrapper przypina wersję silnika: Ollama `LLAMA_CPP_VERSION` b11669 (w sprawdzanym klonie), llmman b11429, Docker Model Runner `LLAMA_SERVER_VERSION=b9879`. Im niższy numer buildu, tym starszy silnik; b9879 vs b11669 to ok. 1800 buildów różnicy *(moje wyliczenie, dat tagów nie sprawdzałem)*. Produkcyjny build z rigu referencyjnego, `0ce8cd1`, jest identyfikowany hashem, więc z numerami `bNNNNN` nie porównam go bez historii git (klony są płytkie).
3. **Wartości domyślne, które psują wyniki po cichu.** Najgłośniejsza: mały kontekst. Ollama dziś dobiera kontekst według VRAM-u (sekcja 2.6), ale użytkownik z małą kartą wciąż dostaje 4k, a skrócenie historii bywa niezgłaszane (issue #14259).
4. **Format na dysku.** Jeśli opakowanie trzyma modele jako własne bloby, inne programy nie przeczytają ich bez eksportu.
5. **Zależność od sponsora.** Wrapper to produkt czyjejś firmy, i to firma decyduje o roadmapie, cloud-upsellu, licencji i telemetrii. Sekcja 7 zbiera to w tabeli.

### 1.4 Tabela porównawcza (silnik, licencja, kto steruje)

Gwiazdki z API GitHuba, 2026-10-19.

| Produkt | Silnik pod spodem | Licencja | Gwiazdki | Kto steruje roadmapą |
|---|---|---|---|---|
| **Ollama** | upstream `llama-server` (GGUF) + własny runner **MLX** (Apple Silicon, safetensors) | MIT | 183 857 | Ollama, Inc. (firma z VC) |
| **LM Studio** | zamknięte "LM Runtimes": buildy llama.cpp + silnik MLX (`mlx-engine`, MIT) | aplikacja zamknięta (freeware); `lms`, SDK, `mlx-engine` MIT | `lms` 5 360; `mlx-engine` 1 189 | Element Labs, Inc. |
| **llmman** | nietknięte upstreamowe llama.cpp / vLLM / SGLang / mlx-lm / ds4-server | Apache-2.0 | 563 | Eric Curtin (pracownik Dockera), jedna osoba |
| **Jan** | llama.cpp zlinkowane statycznie w procesie roboczym (od v0.8.5) + własny `mlx-server` w Swifcie | Apache-2.0 + prośba o atrybucję (GitHub: NOASSERTION) | 45 017 | Menlo Research |
| **GPT4All** | własny fork llama.cpp (`llama.cpp-mainline`), Vulkan | MIT | 77 350 | Nomic AI (projekt de facto uśpiony) |
| **LocalAI** | 60+ backendów jako obrazy OCI za gRPC (llama.cpp, vLLM, SGLang, MLX, whisper.cpp, diffusers…) | MIT | 49 695 | Ettore Di Giacinto (`mudler`) + sponsorzy |
| **Lemonade** | llama.cpp (Vulkan/ROCm/CUDA/Metal/CPU), FastFlowLM i Ryzen AI OGA (NPU), vLLM-ROCm, whisper.cpp… | Apache-2.0 | 5 936 | społeczność + inżynierowie AMD |
| **Docker Model Runner** | llama.cpp (domyślnie), vLLM, SGLang, MLX, Diffusers | Apache-2.0 | 658 | Docker, Inc. |
| **RamaLama** | llama.cpp / vLLM / stable-diffusion / OpenVINO w obrazach per GPU | MIT | 3 086 | org `containers`, opiekunowie z Red Hata |
| **Open WebUI** | brak (frontend) | własna: BSD-3 + klauzula o brandingu (od v0.6.6) | 156 189 | Open WebUI Inc. |
| **AnythingLLM** | domyślnie brak; opcjonalnie wbudowany silnik (llama.cpp/Lemonade) | MIT | 67 323 | Mintplex Labs |

### 1.5 Tabela porównawcza (API, interfejs, tryb offline)

| Produkt | API | Interfejs | Offline |
|---|---|---|---|
| **Ollama** | własne `/api/*`, OpenAI (w tym `/v1/responses`), Anthropic `/v1/messages` | CLI + aplikacja (macOS/Windows); Linux: CLI/systemd | Inferencja offline (`--offline`); do sieci sięga po aktualizacje (aplikacja), modele z rejestru, opcjonalnie chmurę (`OLLAMA_NO_CLOUD=1` wyłącza) |
| **LM Studio** | natywne REST, OpenAI, Anthropic `/v1/messages`; port 1234 | GUI (Electron) + `lms` + demon `llmster` | Działa offline po pobraniu modeli; sieć: aktualizacje, wyszukiwanie/pobieranie modeli, funkcje chmurowe; deklaracja prywatności *(dane firmy)* |
| **llmman** | Ollama, OpenAI, Anthropic, Gemini | CLI + web UI pod `/` | Offline po zbuforowaniu silników (`serve --pull-only`); telemetrii nie przeszukiwałem *(niezweryfikowane)* |
| **Jan** | OpenAI na `localhost:1337` | GUI (Tauri) | Offline; analityka opt-in (PostHog EU) *(dane projektu)* |
| **GPT4All** | w notatkach brak opisu serwera API | GUI (Qt) + Python | Lokalne modele offline; telemetrii nie ustaliłem |
| **LocalAI** | OpenAI, Anthropic, Ollama, ElevenLabs, Realtime | serwer + CLI `local-ai` | Offline po pobraniu backendu i modelu (pierwsze użycie wymaga sieci) |
| **Lemonade** | OpenAI, Anthropic, Ollama | CLI, zasobnik, aplikacja web/Electron | Offline; backendy i modele pobierane przy pierwszym użyciu; "zero telemetrii" *(dane projektu)* |
| **Docker Model Runner** | OpenAI (`:12434`), Ollama, Anthropic, Responses | `docker model …`, Docker Desktop | brak opisu w notatkach; modele z Docker Hub, rejestrów OCI lub HF |
| **RamaLama** | `ramalama serve` (szczegóły nie opisane) | CLI | Kontener domyślnie bez sieci; obrazy z quay.io |
| **Open WebUI** | konsument cudzych API | web (FastAPI + Svelte) | zależy od backendu |
| **AnythingLLM** | konsument cudzych API (Ollama, LM Studio, LocalAI…) | desktop + Docker | zależy od backendu |

---

## 2. Ollama w głąb

**W jednym zdaniu:** demon w Go (`ollama serve`, port 11434) + CLI + aplikacja desktopowa + rejestr modeli podobny do OCI (ollama.com), który dla każdego modelu uruchamia osobny proces silnika; od 2026 roku tym silnikiem jest upstreamowy `llama-server` (modele GGUF) albo własny runner MLX (Apple Silicon), do tego płatna chmura "Ollama Cloud".

### 2.1 Kto za tym stoi

Ollama, Inc.; współzałożyciele Jeffrey Morgan (`jmorganca`, wcześniej Docker, Twitter, Google) i Michael Chiang (`mchiang0610`); obaj współtworzyli Kitematic, kupiony przez Dockera w 2015 roku. Firma zebrała — według własnego wpisu z 2026-07-09 — **88 mln USD** (Benchmark, Theory Ventures, 8VC i inni) *(dane firmy)*; Wikipedia podaje 65 mln *(źródło zewnętrzne)*. Nie rozstrzygnąłem tej rozbieżności: nie wiem, czy 88 mln to jedna runda, czy suma. Kod jest na licencji MIT, ale rejestr modeli, szablony, parsery i chmura to osobna sprawa. Przychód to subskrypcje chmury (Free / Pro 20 USD / Max 100 USD / Team 500 USD miesięcznie, rozliczane za tokeny). Szczegóły w [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

### 2.2 Po co to jest

Żeby `ollama run <model>` działało na laptopie bez konfiguracji: ściąga wagi skwantyzowane, ustawia rozsądne wartości domyślne i wystawia zawsze włączone lokalne REST API, z którym rozmawia każdy agent i każde IDE. Od 2026 roku to także rampa do chmury: `ollama launch claude|codex|opencode` uruchamia agenta kodującego wobec modelu lokalnego **lub** chmurowego (`docs/cloud.mdx`).

Czym Ollama celowo **nie** jest: serwerem o wysokiej przepustowości (`NUM_PARALLEL` domyślnie 1), narzędziem do trenowania ani wielodostępną bramką.

Stan na 2026-10-19: MIT, Go (UI aplikacji TS/React, części natywne C/C++ przez CMake), repozytorium z 2023-06-26, **183 857 gwiazdek**, ~5 917 commitów. Najnowsza stabilna: **v0.40.6 (2026-10-16)**; numeracja skakała (0.24 → 0.30 w dniach 13–14 maja 2026 → 0.35 → 0.40 w dniu 2026-09-25), tag co 2–4 dni. Rozmiary kodu Go (z testami): `cmd/` 63 tys. linii, `server/` 40 tys., `model/` (parsery i renderery) 39 tys., `mlxrunner/` 32,6 tys., `app/` 26 tys., `llm/` 9,7 tys., `discover/` 5,4 tys.; C++: `llama/compat/llama-ollama-compat.cpp` 3 507 linii.

### 2.3 Co się zmieniło w 2026: Ollama nie ma już własnego silnika GGUF

To najważniejsza zmiana w tym rozdziale i miejsce, w którym starsze źródła są nieaktualne, więc zapisuję dokładnie, **co jest zweryfikowane, a co nie**.

**Zweryfikowane (API GitHuba i kod w klonie):**

- PR **#16031** "runner: Remove CGO engines, use llama-server exclusively for GGML models" został wpięty **2026-05-29**: +28 tys. / −430 tys. linii, ~1100 plików. Usunął wendorowane ggml, runner CGO i Go-natywne implementacje modeli ("silnik Ollamy").
- Uzasadnienie w opisie PR: szybsze przejmowanie funkcji z llama.cpp.
- Dziś GGUF uruchamia **upstreamowy `llama-server` jako proces potomny**. Wersję przypina plik `LLAMA_CPP_VERSION` (**b11669** w klonie). `llama/README.md` opisuje: pobranie przypiętych źródeł, nałożenie łatek z `llama/compat/`, zbudowanie `llama-server`. Główny `CMakeLists.txt` mówi to samo komentarzem ("GGML backend for inference is provided by llama-server (built separately … using FetchContent from the pinned llama.cpp source)").
- W klonie **nie ma** katalogu `ml/backend` (stary silnik w procesie). Jedyna pozostałość nazwy to komentarz w `mlxrunner/embed.go` ("old ollamarunner"). Tag `ggml` w manifestach to dziś tylko starszy znacznik; takie manifesty też idą do `llama-server`.
- Modele safetensors na Apple Silicon biegną na **własnym runnerze MLX** (`mlxrunner/`, 32,6 tys. linii): to nadal własny kod Ollamy, tyle że o MLX, nie o ggml.

**Co to znaczy precyzyjnie.** Ollama nie dołącza *niezmodyfikowanego* binarium `llama-server`. Bierze upstreamowe źródła w przypiętej wersji, nakłada **małą warstwę łatek** (`001-llama-cpp-hooks.patch`) plus kod `llama-ollama-compat.cpp` i buduje. To różni się od llmmana, który uruchamia silniki bez żadnych modyfikacji.

**Rozbieżność ze starszym opisem.** README llmmana zawiera tabelę porównawczą, w której Ollama jest opisana jako "Bundled llama.cpp/ggml fork plus Ollama's own engine". Po 2026-05-29 to nieprawda, więc README llmmana jest nieaktualne w tym punkcie *(sprawdzone przez zestawienie z kodem Ollamy)*. To samo dotyczy każdego tekstu z 2025 roku o "nowym silniku Ollamy kontra llama.cpp". Do 29 maja 2026 Ollama faktycznie prowadziła własny silnik w Go na wendorowanym ggml, więc takie teksty były w swoim czasie poprawne.

**Czego dowody NIE rozstrzygają:**

- **Chronologii przejścia.** Tag v0.30.0 pochodzi z 2026-05-13/14, PR #16031 został wpięty 2026-05-29, a wpis na blogu o szybszej pracy po przejściu na GGUF/llama.cpp — z 2026-06-05. Kolejność tagów sugeruje, że ścieżka przez `llama-server` mogła istnieć wcześniej obok starego silnika (za flagą lub w linii 0.30) *(niezweryfikowane)*. Ustalone jest tylko, że od 2026-05-29 stary silnik został usunięty.
- **Wydajności.** Blog Ollamy (2026-06-05) twierdzi, że po przejściu na llama.cpp jest "do 20% szybciej na NVIDIA" (Gemma 4 26B, RTX 5090, Q4_K_M) *(dane firmy)*. Niezależnego pomiaru nie sprawdzałem; przeczytałem tylko ten jeden zakres.
- **Czy łatki są "małe".** Samo `llama/compat/` to ~4,5 tys. linii (łatka + `llama-ollama-compat.cpp` 3 507 linii). Nazywam to "małą warstwą" za notatkami; policz sam przy lekturze.

> **Sprawdź sam #1 — czy Ollama naprawdę nie ma własnego silnika GGUF.**
> W klonie `~/runtimes-src/ollama/` *(nie uruchamiałem tych poleceń, ścieżki z notatek)*:
> ```
> cat LLAMA_CPP_VERSION
> sed -n '1,60p' llama/README.md
> grep -rn "ollamarunner" --include=*.go . | head
> ls ml 2>/dev/null || echo "brak ml/"
> ```
> Przez API GitHuba (wymaga zalogowanego `gh`): `gh api repos/ollama/ollama/pulls/16031` — tytuł, data wpięcia, liczba zmienionych plików. Dla drugiej strony sporu otwórz tabelę porównawczą w README llmmana (`grep -n -i ollama ~/runtimes-src/llmman/README.md`) i zestaw ją z powyższym.

### 2.4 Przepływ żądania i procesy runnerów

```
HTTP (gin, server/routes.go, 3 653 linii)
   │  GenerateHandler / ChatHandler: rozwiąż model (manifest → bloby)
   ▼
Scheduler.getRunner   (server/sched.go, 1 851 linii)
   │  runnerRef  ──►  llm.LlamaServer
   ▼
HTTP do procesu potomnego na 127.0.0.1:<losowy port>
   │  llama-server  (GGUF)      albo      mlxrunner (safetensors, Apple Silicon)
   ▼
strumień tokenów → przepisany na JSON Ollamy / OpenAI / Anthropic
```

**Proces potomny — izolacja jako decyzja projektowa.** `llm/llama_server.go` uruchamia `llama-server` z flagami: `--model <blob> --port N --host 127.0.0.1 --no-webui --offline`, `-c NumCtx×numParallel`, `-np numParallel`, opcjonalnie `--cache-type-k/v` (z `OLLAMA_KV_CACHE_TYPE`), `--flash-attn on|off|auto`, `--split-mode none --main-gpu N` dla umieszczenia na jednej karcie, `--mmproj` (wizja), `--lora`, `--context-shift`, flagi dekodowania spekulatywnego (`--spec-type`, `--spec-draft-model`) i `--load-mode dio|none`. Liczbę warstw na GPU, wątki i dopasowanie do pamięci (`LLAMA_ARG_FIT`, `LLAMA_ARG_FIT_TARGET`) ustala sam `llama-server`.

Dlaczego proces osobny? Bo `GGML_ASSERT` wywołuje `abort()`: błąd w silniku nie może zabić demona, który trzyma stan wszystkich modeli. (Ta sama decyzja stoi za procesem roboczym w Janie, sekcja 5.1.)

**Runner MLX.** Modele safetensors idą do innego dziecka (`mlxrunner.Execute`, flagi `--model --port`). To reimplementacja architektur modeli w Go na wiązaniach C do MLX (`mlx/`, `mlxrunner/`): drzewo trie do pamięci podręcznej prefiksów (`cache_trie.go`), maski gramatyki (`grammar.go`, xgrammar), dekodowanie spekulatywne (`speculate.go`, `dflash.go`, `mtp.go`), tokenizer, sampler. Więcej o MLX w [`07-APPLE-MLX-OMLX-I-DS4.md`](07-APPLE-MLX-OMLX-I-DS4.md).

### 2.5 Który silnik dla którego modelu

Manifest niesie znacznik "runner": `mlx`, `llamacpp` albo `ggml` (stary). Kolejność preferencji zależy od platformy:

| Platforma | Preferencja | Skutek |
|---|---|---|
| Apple Silicon (darwin/arm64) | **mlx > llamacpp > ggml** | od **v0.40.0 (2026-09-25)** architektury obsługiwane przez MLX "automatycznie biegną na MLX" |
| Linux, Windows, Intel Mac, a na Apple Silicon modele bez implementacji MLX | **llamacpp > ggml > mlx** | GGUF przez `llama-server` |

Architektury zarejestrowane w `mlxrunner/model/architectures/architectures.go`: llama, qwen3, qwen3_5, qwen3_5_moe, qwen4_exp, gemma4 (+embedding), glm4_moe_lite, laguna, nemotron_h, cohere2_moe, a do tego modele "decyzyjne" (clef, kev, laya, strands, pplxdecider, glimmer, dflash). Wniosek praktyczny: jeśli na Macu masz model spoza tej listy, dostaniesz GGUF przez llama.cpp, nie MLX.

### 2.6 Scheduler i wartości domyślne

Ten fragment to serce "opakowania": Ollama sama zarządza tym, co llama-swap robisz ręcznie. Wszystko z `server/sched.go` i `envconfig/config.go`.

- **Kolejka.** Jedna pętla (goroutine) `processPending` konsumuje kanał `pendingReqCh` o buforze `OLLAMA_MAX_QUEUE` (domyślnie **512**); przepełnienie daje `ErrMaxQueue`.
- **Ładowanie.** Mapa `loaded map[string]*runnerRef`. Jeśli model jest załadowany, a `needsReload` jest fałszem (kontekst, opcje, adaptery i projektory bez zmian), żądanie dołącza do istniejącego runnera (licznik odwołań). W przeciwnym razie następuje załadowanie, przy czym **naraz ładuje się tylko jeden model** (`activeLoading`), choć żądania do już załadowanych modeli idą równolegle.
- **Limit załadowanych modeli.** `OLLAMA_MAX_LOADED_MODELS`; gdy nieustawione (0), wynosi `defaultModelsPerGPU (=3) × max(liczba GPU, 1)`. Gdy limit jest osiągnięty, `findRunnerToUnload` wyrzuca model według `ByDurationAndName` (najkrótsza pozostała sesja / najdłużej bezczynny). Przy braku pamięci przy ładowaniu: `evictAllAndWait` + jedna próba ponowna (`oomRetryAttempted`).
- **Keep-alive.** `OLLAMA_KEEP_ALIVE` domyślnie **5 minut**; wartość ujemna = na zawsze, 0 = zwolnij od razu; `keep_alive` w żądaniu ma pierwszeństwo. Technicznie: licznik `expireTimer` na runnerze.
- **Równoległość.** `OLLAMA_NUM_PARALLEL` domyślnie **1** (`envconfig.NumParallel`); wymuszone 1 dla modeli embeddingowych i architektur oznaczonych jako niebezpieczne (mllama, qwen3vl, qwen35, qwen3next, lfm2, nemotron_h…). Sloty to `-np` w `llama-server`, a alokowany kontekst to `NumCtx × numParallel`. Czyli domyślnie masz jeden slot na model: obsługa wielu równoległych żądań do tego samego modelu wymaga podniesienia tego parametru (i zapłacenia za to pamięcią podręczną KV, *KV cache*) *(moje wyliczenie z opisu parametrów)*.
- **Rozmieszczenie na wielu GPU** (`selectLlamaServerPlacement`). Przy kilku kartach: grupuje GPU według biblioteki (`ml.ByLibrary`), potem (o ile nie ustawiono `OLLAMA_SCHED_SPREAD`) **najpierw próbuje zmieścić cały model na jednej, najlepszej karcie** (`bestSingleGPUFit` → `--split-mode none --main-gpu N`); jeśli się nie mieści, używa grupy z największą wolną pamięcią, a `llama-server` dzieli warstwy. Zapotrzebowanie na VRAM jest przewidywane z metadanych GGUF (`llm.PredictServerVRAM`), przy obecności innych modeli próg to 80% wolnej pamięci. `mmap` bywa wyłączany heurystycznie (`disableMmapDefaultReason`); przy braku pamięci Ollama automatycznie zmniejsza rozmiar batcha i kontekst (`reduceAutoNumCtxForLoadOOM`).
- **Domyślne okno kontekstu** zależy od VRAM-u (`docs/context-length.mdx`): **< 24 GiB → 4k, 24–48 GiB → 32k, ≥ 48 GiB → 256k**; modele chmurowe działają na maksimum. Ta sama dokumentacja pisze, że agenci, kodowanie i wyszukiwanie "powinny mieć ustawione co najmniej 64000". Nadpisanie: `OLLAMA_CONTEXT_LENGTH`, `num_ctx`, suwak w aplikacji. Dla rigu referencyjnego 4×32 GB *(moje wyliczenie)* automatyczny próg wypadłby w najwyższym przedziale — ale nie ustaliłem, czy próg liczy się od VRAM-u jednej karty, czy od sumy kart, więc nie bierz tego za pewnik.

Zwróć uwagę na zbieżność z ideami llama-swap: TTL = keep-alive, grupy = limit modeli na GPU, ale w tym, co przeczytałem, brak odpowiednika *macierzy* kosztów wyrzucania (por. [`04-LLAMA-CPP-I-RODZINA-GGML.md`](04-LLAMA-CPP-I-RODZINA-GGML.md), sekcja o llama-swap).

> **Sprawdź sam #2 — domyślne wartości.**
> W klonie Ollamy *(nie uruchamiałem)*: `grep -n "KeepAlive\|NumParallel\|MaxQueue" envconfig/config.go` pokaże 5 minut, 1 i 512; `grep -rn "defaultModelsPerGPU" server/` — mnożnik 3; `sed -n '1,80p' docs/context-length.mdx` — progi 4k/32k/256k i zdanie o 64000 dla agentów.

### 2.7 Modelfile

Plik w stylu Dockerfile (`docs/modelfile.mdx`), instrukcje: `FROM`, `PARAMETER`, `TEMPLATE`, `SYSTEM`, `LICENSE`, `MESSAGE`, `REQUIRES`, `CAPABILITY`. Import z GGUF albo safetensors. Za pomocą `ollama create` budujesz z niego nowy model: wagi zostają bez zmian, a do manifestu dochodzą warstwy (szablon, parametry, prompt systemowy). To ważny punkt: **szablon czatu i parametry są częścią modelu**, nie osobną konfiguracją serwera. W llama.cpp odpowiednikiem są `--jinja`, `--chat-template` i flagi w `cmd` w konfiguracji llama-swap.

### 2.8 Rejestr: manifest i bloby

Modele leżą pod `~/.ollama/models`:

```
~/.ollama/models/
  blobs/sha256-<digest>                       ← wagi GGUF, szablon, parametry… jako pliki po skrócie
  manifests/<host>/<namespace>/<nazwa>/<tag>  ← manifest JSON
```

Manifest to schemat dystrybucji Dockera (`application/vnd.docker.distribution.manifest.v2+json`): `config` (JSON z formatem modelu, rodziną i kwantyzacją, typ `application/vnd.docker.container.image.v1+json`) oraz lista `layers[]` z własnymi typami mediów:

| Typ warstwy | Zawartość |
|---|---|
| `application/vnd.ollama.image.model` | wagi GGUF |
| `.projector` | projektor multimodalny |
| `.adapter` | LoRA |
| `.embed`, `.tensor`, `.draft` | embeddingi, safetensors, model szkicujący do dekodowania spekulatywnego |
| `.template`, `.system`, `.params`, `.messages`, `.license` | szablon, prompt systemowy, parametry, przykładowe wiadomości, licencja |

Nowość: **listy manifestów** (`application/vnd.ollama.manifest.list.v2+json`), których dzieci niosą pola `runner` i `format`, dzięki czemu jeden tag może oferować zarówno build MLX, jak i GGUF. Pobieranie i wysyłanie idzie przez HTTP API rejestru ollama.com (podobne do OCI, z własną autoryzacją; pakiet `transfer/`, `OLLAMA_MAX_TRANSFER_STREAMS=4`).

Konsekwencja: **plik modelu nie leży na dysku jako `nazwa.gguf`**, tylko jako blob `sha256-…`. Inne programy go nie rozpoznają bez eksportu (ten argument podnosi README llmmana *(dane projektu)*). Plus tej decyzji: deduplikacja warstw i weryfikacja skrótu.

### 2.9 API

Zarejestrowane w `server/routes.go` (okolice linii 2362–2425): **natywne** `/api/generate`, `/api/chat`, `/api/embed`, `/api/pull|push|create|copy|delete|show|tags|ps`, `/api/blobs/:digest`, konto (`/api/me`, `/api/usage`…), eksperymentalne `web_search` i `web_fetch`; **OpenAI** `/v1/chat/completions`, `/v1/completions`, `/v1/embeddings`, `/v1/models`, `/v1/responses`, `/v1/audio/transcriptions`; **Anthropic** `/v1/messages` (`anthropic/anthropic.go`); `/v1/systemone` ("modele decyzyjne", v0.35.0, 2026-09-28).

Narzędzia, "myślenie" (*thinking*), wizja, embeddingi i wyjście ustrukturyzowane (schemat JSON w polu `format`, przekazywany do `llama-server` jako `json_schema` albo gramatyka GBNF) opisuje `docs/capabilities/`. Wiadomości na prompt zamieniają **renderery i parsery w Go** (`model/renderers`, `model/parsers`, `harmony/`); modele bez nich używają `chat_template` z `llama-server`. Integracje (`docs/integrations/`): Claude Code, Codex, OpenCode, Cline, Roo, Zed, JetBrains, VS Code, Xcode, n8n, goose i inne.

To jest główna siła Ollamy: **każde narzędzie agentowe ma "dostawcę Ollama"**. Jeśli piszesz własne aplikacje agentowe, i tak najpewniej potrzebujesz tylko OpenAI-zgodnego endpointu, który ma też `llama-server`.

### 2.10 Warstwa compat: tłumaczenie GGUF w pamięci

Modele opublikowane w rejestrze Ollamy przed 2026 rokiem mogą nie pasować do upstreamowych loaderów. Dlatego `llama/compat/` (≈4,5 tys. linii) tłumaczy metadane i układ tensorów **w pamięci, przy ładowaniu**, dla ~20 architektur (m.in. gemma3/3n/4, gpt-oss, qwen3.5/3-vl/3-next, mistral3, llama4, lfm2, olmo3, deepseek-ocr, glm-ocr, nemotron-h). `llama/compat/README.md` sam nazywa tę warstwę "tymczasową … mającą żyć krótko". Pomysł wart zapamiętania: tłumaczyć przy ładowaniu, a nie wymuszać ponownego pobrania wszystkich modeli.

### 2.11 Chmura, telemetria i tryb offline

- **Inferencja jest offline**: `llama-server` startuje z `--offline`, silnik nigdy nie dotyka sieci.
- **Aplikacja desktopowa pyta o aktualizacje:** `app/updater/updater.go` robi GET na `https://ollama.com/api/update?os&arch&version&ts&nonce`, podpisane lokalnym kluczem; na macOS dochodzi identyfikator urządzenia (`id`).
- **Pobieranie modeli** idzie z ollama.com; opcjonalne logowanie, chmura i wyszukiwanie internetowe używają dalszych punktów końcowych.
- **Telemetria:** w katalogu `app/` nie znalazłem żadnego SDK analitycznego (grep po posthog/segment/mixpanel). To tylko grep po kodzie klienta; telemetrii po stronie ollama.com nie da się zaudytować.
- **Wyłączenie chmury:** `OLLAMA_NO_CLOUD=1` albo `disable_ollama_cloud` w `~/.ollama/server.json` (`docs/faq.mdx`). Środowisko odcięte od sieci: skopiuj `~/.ollama/models`.
- **Wystawienie na sieć:** serwer domyślnie nasłuchuje na `127.0.0.1:11434` (`OLLAMA_HOST` zmienia to). Wikipedia opisuje wystawione do internetu serwery Ollamy znajdowane przez SentinelOne i Censys *(źródło zewnętrzne)*. Wniosek: nie ustawiaj `OLLAMA_HOST=0.0.0.0` bez zapory ani uwierzytelniania przed nim.

### 2.12 Krytyka: obie strony

Każdy zarzut sprawdzony na źródłach pierwotnych tam, gdzie to możliwe.

| Zarzut | Co mówi źródło | Druga strona | Mój wniosek |
|---|---|---|---|
| **1. Brak atrybucji llama.cpp / notek licencyjnych** | Issue **#3185** "ollama doesn't distribute notice licenses in its release artifacts" (otwarte 2024-03-16, nadal **otwarte**, 59 komentarzy): MIT wymaga zachowania notek praw autorskich w dystrybucji binarnej; autor zgłoszenia nie znalazł "Georgi Gerganov" w instalacjach Linux/Windows | README ma dziś sekcję "Supported backends" z podziękowaniem dla projektu llama.cpp Georgiego Gerganova; blog do wersji 0.30 dziękuje twórcom llama.cpp i NVIDIA, AMD, Qualcomm, Intelowi *(dane firmy)*. Po PR #16031 Ollama jest cienkim konsumentem upstreamu, więc zarzut "fork zasłaniający źródło" zmienia charakter | Czy braki notek zostały naprawione, **nie ustaliłem** (w klonie nie ma plików NOTICE/THIRD_PARTY w korzeniu). Zarzut z 2024 jest formalny, a nie dotyczący jakości kodu |
| **2. Nazewnictwo modeli** | Issue **#8557** "Please separate deepseek-r1 from deepseek-r1-Distill!" (2025-01-24, otwarte): destylaty na Qwen/Llama były wystawiane jako `deepseek-r1:7b` itd. | — | Samo istnienie zgłoszenia sprawdzone; aktualny stan biblioteki nie jest sprawdzony *(niezweryfikowane)*. Zasada na przyszłość: czytaj kartę modelu, nie tag |
| **3. Mały domyślny kontekst** | Dziś próg zależny od VRAM-u (4k / 32k / 256k). Przed 2026 domyślne 2048/4096 *(niezweryfikowane, z pamięci autora notatek)*. Issue **#14259** "Chat history and embedding truncation happens silently" (otwarte 2026-02-14) | Dokumentacja otwarcie mówi, że agentom trzeba 64 000+ | Dla ciebie nieistotne przy dużym VRAM-ie, ale ważne dla ludzi z małymi kartami, którzy czytają "Ollama jest głupia" |
| **4. Wolniej niż llama.cpp** | Do maja 2026 własny silnik w Go na wendorowanym ggml mógł dawać różnice | Własna deklaracja "do 20% szybciej na NVIDIA" po przejściu na llama.cpp pośrednio potwierdza, że różnice były *(dane firmy)* | Dziś silnik jest ten sam, więc różnica to głównie wartości domyślne (parallel=1, progi kontekstu) i hop przez proxy. Niezależnych pomiarów nie sprawdzałem (m.in. benchmarki gpt-oss z 2025 pominąłem) |
| **5. Sprzężenie z chmurą** | Logowanie, `ollama launch`, wyszukiwanie i modele chmurowe są pierwszoplanowe w CLI i aplikacji | Jest przełącznik `OLLAMA_NO_CLOUD` | Rozsądne: lokalny użytkownik może to wyłączyć, ale domyślny przepływ prowadzi do konta |
| **6. Ekspozycja i bezpieczeństwo** | Serwery wystawione do internetu *(źródło zewnętrzne)* | Domyślnie loopback | Odpowiedzialność użytkownika, ale prosty do popełnienia błąd |
| **7. Tempo wydań** | Tag co kilka dni; otwarty issue **#17878** (2026-08-19): embeddingi zwracające po cichu zerowe wektory pod obciążeniem | — | Nie wdrażaj `latest` na produkcję; przypinaj wersję |

### 2.13 Wydajność

Opóźnienie jednego strumienia jest z grubsza takie jak w samym llama.cpp (ten sam silnik) plus hop przez proxy w Go. Przepustowość ogranicza konfiguracja domyślna: `NUM_PARALLEL=1`, 3 modele na GPU, jedno ładowanie naraz, 5 minut keep-alive. Wpisów o silniku MLX (2026-03-30, 06-11, 06-29) nie czytałem w całości *(dane firmy)*. Własnej liczby tok/s dla Ollamy nie podaję.

### 2.14 Ollama a rig referencyjny z kartami AMD

- `docs/gpu.mdx` wymienia **Radeon AI PRO R9700 / R9600D** w sekcji ROCm. **Wymagany jest ROCm v7** (Linux i Windows). Vulkan jest włączony domyślnie ("no vendor library needed"). Zmienne: `HIP_VISIBLE_DEVICES`, `ROCR_VISIBLE_DEVICES`, `HSA_OVERRIDE_GFX_VERSION`, `GGML_VK_VISIBLE_DEVICES`, `OLLAMA_VULKAN=0`.
- Czyli Ollama **powinna** działać na R9700 (gfx1201). Notatki nie mówią, czy ktoś to u siebie sprawdził; ja też nie.
- Rozmieszczenie na wielu GPU: najpierw cały model na jednej karcie, a jeśli się nie mieści, `llama-server` dzieli warstwy. Notatki **nie mówią**, czy Ollama wystawia tryby podziału znane z przewodnika [`../przyspieszanie-generowania/README.md`](../przyspieszanie-generowania/README.md) (tensor parallel, ratio per karta). Przy modelu 284B w IQ3_XXS na czterech kartach to właśnie te ustawienia decydują o 50 tok/s, więc sprawdź przed przesiadką.

### 2.15 Kiedy wybrać Ollamę

Kiedy chcesz najkrótszej drogi od zera do działającego modelu na Macu lub laptopie; kiedy narzędzie, z którego korzystasz, ma tylko "dostawcę Ollama"; kiedy chcesz biblioteki modeli z gotowymi szablonami i parserami wywołań narzędzi; kiedy na Macu chcesz MLX bez własnej konfiguracji. **Nie wybieraj**, gdy potrzebujesz pełnej kontroli nad flagami silnika, plików GGUF w zwykłym katalogu albo ścisłego przypięcia buildu llama.cpp.

---

## 3. LM Studio w głąb

**W jednym zdaniu:** zamknięta aplikacja desktopowa (Electron) do znajdowania, pobierania i uruchamiania modeli lokalnie, z warstwą silników w postaci zamkniętych "LM Runtimes" (buildy llama.cpp + MLX) oraz otwartym CLI, SDK i wrapperem MLX; od wersji 0.4.0 także demon bez interfejsu (`llmster`); od lipca 2026 obok istnieje drugi, osobny produkt **Bionic**.

### 3.1 Kto za tym stoi

Firma **Element Labs, Inc.** (regulamin z 2026-08-23). Pierwsze wydanie w maju 2023 *(źródło zewnętrzne: Wikipedia)*; organizacja GitHub `lmstudio-ai` założona 2023-05-16. Tekst o darmowym użyciu w pracy podpisuje Yagil Burowski; jego formalnego tytułu nie zweryfikowałem. **Finansowania i założycieli nie znalazłem** na stronach firmy i w Wikipedii: zostawiam to puste zamiast zgadywać. W kwietniu 2026 do LM Studio dołączył zespół **Locally AI** (aplikacja iOS/Mac, Adrien Grondin), warunki nieujawnione. Pieniądze i ludzie: [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

### 3.2 Co jest otwarte, a co zamknięte

To najczęstsze nieporozumienie, więc w tabeli:

| Element | Status | Uwagi |
|---|---|---|
| Aplikacja desktopowa (Electron) | **zamknięta**, darmowa (freeware) | kodu źródłowego nie ma w żadnym repozytorium; `lmstudio-bug-tracker` to tylko tracker zgłoszeń |
| Demon `llmster`, buildy llama.cpp ("LM Runtimes") | **zamknięte** | w organizacji nie ma forka llama.cpp |
| Backend huba modeli, LM Link, Bionic | **zamknięte** | SaaS / usługi |
| CLI `lms` | MIT, 5 360 gwiazdek, TypeScript | część monorepo `lmstudio-js`; "nie da się zbudować samodzielnie" |
| SDK `lmstudio-js` (1 798), `lmstudio-python` (884; ostatni push 2025-10-27) | MIT | |
| `mlx-engine` (1 189, Python) | MIT | zbudowany na mlx-lm, Outlines i mlx-vlm |
| `model-catalog` (803) | Apache-2.0 | opisy modeli w JSON |
| `docs`, `configs`, `venvstacks`, `nq`, `localization` | otwarte | `office-document-processor-sources` (MPL-2.0) pojawiło się 2026-10-06 |

Wniosek: **otwarte są klienci i wtyczki, zamknięty jest środek**. Nie możesz zaaudytować ani załatać runtime'u, ani wskazać dowolnego commita llama.cpp. `lms` i SDK nadal potrzebują działającej zamkniętej aplikacji lub demona.

### 3.3 Trzy sposoby użycia: aplikacja, `lms`, `llmster`

Według dokumentacji (`lmstudio-vs-llmster-vs-lms.md`):

- **Aplikacja LM Studio:** wyszukiwanie i pobieranie z Hugging Face, czat, RAG po dokumentach, presety, lokalny serwer, MCP.
- **`llmster`:** demon bez ekranu: "serwer Linuksa, GPU rig bez monitora, CI/CD, usługa startująca z systemem". Instalacja: `curl -fsSL https://lmstudio.ai/install.sh | bash` (Windows: `irm …/install.ps1 | iex`), potem `lms daemon up` i `lms server start`. Instalator pochodzi z notatek i go nie uruchamiałem; nie wykonuj `curl | bash` na rigu bez przeczytania skryptu.
- **`lms`:** CLI: `get`, `load`, `ls`, `ps`, `server start`, `chat`, `log stream`, `runtime ls|get|select|remove|update`.

### 3.4 Serwer, API, MCP, równoległość

- **Port domyślny 1234.** Natywne REST (`/api/v1/…`) ze stanowym `/v1/chat` (pola `response_id`, `previous_response_id`, od 0.4.0): serwer pamięta rozmowę i klient odsyła tylko identyfikator poprzedniej odpowiedzi.
- **Zgodność z OpenAI** (czat, completions, embeddings, wyjście ustrukturyzowane) i **z Anthropic**: dokumentacja wymienia tylko `POST /v1/messages`; strumieniowania i narzędzi na tej stronie nie opisano.
- **JIT i TTL:** model ładuje się przy pierwszym żądaniu i po bezczynności jest zwalniany automatycznie (dokumentacja trybu headless). Ten sam wzorzec jest w Ollamie i w llama-swap.
- **MCP:** `mcp.json` w notacji Cursora, serwery lokalne i zdalne, z ostrzeżeniem o dowolnym kodzie; 0.4.0 dodało w REST "lokalnie skonfigurowane MCP z kontrolą kluczy uprawnień".
- **Równoległe żądania i ciągłe batchowanie** (*continuous batching*) przyszły z "llama.cpp engine 2.0.0" w wersji 0.4.0 (ustawienia "max concurrent predictions" i zunifikowany KV); równoległość MLX była w styczniu 2026 opisana jako "nadchodząca".
- **LM Link** (blog 2026-06-04): szyfrowany end-to-end zdalny dostęp do lokalnych modeli z innych urządzeń, np. z iPhone'a; sposób transportu niejawny.

Wersja: **0.4.0 wydana 2026-01-28** *(blog)*; późniejszej "0.5" nie znalazłem.

### 3.5 Silniki i sprzęt

- macOS: wyłącznie Apple Silicon, macOS 14+; Intel Maki niewspierane. Windows: x64 (AVX2) i ARM64 (Snapdragon X). Linux: x64 i ARM64, dystrybucja AppImage, Ubuntu 20.04+.
- Silniki: **llama.cpp (GGUF)** na wszystkich platformach i **MLX** na Apple Silicon. Runtime'y to osobno aktualizowane paczki ("LM Runtimes", skrót Ctrl/Cmd+Shift+R, `lms runtime …`).
- ⚠️ **ROCm i gfx1201:** nie umiem tego potwierdzić. Strona dokumentacji "LM Runtimes" zwróciła 404, a repozytorium z jej źródłem to szablon z tekstem zastępczym. Lista backendów (CUDA, Vulkan, ROCm, Metal, CPU) to "zwykły zestaw", ale konkretnie ROCm dla R9700 jest *(niezweryfikowane)*. Jeśli rozważasz LM Studio na rigu, najpierw przetestuj na jednej karcie.
- Blog z 2026-09-18 promuje "Splash Engine", **otwarty silnik firmy Inco AI** (74 tok/s dla krótkich promptów i 54 przy 32K na Qwen3.8-27B, 170 tok/s przy 4 równoległych żądaniach, na 48 GB M5 Pro) *(dane firmy)*; jak jest podłączony do LM Studio — niejasne *(niezweryfikowane)*.

### 3.6 Architektura (tyle, ile widać)

Zamknięty rdzeń uniemożliwia czytanie kodu, więc to wniosek z otwartych elementów: powłoka Electron z "rdzeniem" w Node, który rozmawia z osobnymi procesami silników przez protokół SDK `lmstudio-js` (oparty na WebSocket, ten sam co w SDK i `lms`). Silniki to runtime pochodzący z llama.cpp i pythonowy `mlx-engine`. Aplikacja, `llmster` i Bionic mają osobne katalogi stanu, ale "współdzielą magazyn modeli i runtime'ów". Katalog modeli to otwarty JSON, Hub to zamknięty SaaS.

### 3.7 Regulamin, offline, Bionic

- **Regulamin (Element Labs, 2026-08-23):** oprogramowanie na użytek "osobisty i/lub wewnętrzny firmy"; zakaz użycia jako usługi (*service bureau*, ASP, SaaS), zakaz inżynierii wstecznej i redystrybucji; limit odpowiedzialności **50 USD**. **Od 2025-07-08 jest darmowe do pracy** ("bez formularza i kontaktu"); wcześniej do użycia służbowego wymagano formularza/licencji.
- **Offline:** "LM Studio może działać w całości na twoim urządzeniu… żadne wiadomości, historie czatów ani dokumenty nie są nigdzie przesyłane" *(dane firmy: lmstudio.ai/app-privacy)*. Łączy się z siecią w celu: aktualizacji (wersja aplikacji, OS, IP), zanonimizowanych zapytań wyszukiwarki modeli i pobrań, opcjonalnych funkcji chmurowych, poczty do wsparcia. Po pobraniu modeli działa offline.
- **Bionic (2026-07-16):** "agent AI dla otwartych modeli", "nowa, osobna aplikacja". Działa lokalnie, przez LM Link albo w "LM Studio Secure Cloud" (wymaga konta do rozliczeń; zero retencji danych i brak trenowania na nich *(dane firmy)*); tworzy dokumenty, slajdy, PDF-y i oprogramowanie; umiejętności (*skills*, 2026-08-17), Auto Review (2026-08-27). Do pobrania wersja na Windows x64 według strony głównej. Klasyczna aplikacja, `llmster` i `lms` nadal istnieją; `lms` rozpoznaje Bionic (woli działającą aplikację LM Studio lub llmster).
- **Model biznesowy** *(dane firmy)*: organizacje w Hubie (publiczna darmowa, zespołowa samoobsługowa **Teams**, **Enterprise** z SSO i bramkowaniem modeli/MCP, bez cennika); Bionic + Secure Cloud (hostowane otwarte modele z rozliczeniem); przejęcia zespołów (Locally AI).

### 3.8 Mocne i słabe strony

| + | − |
|---|---|
| najlepsze GUI i najłatwiejsze odkrywanie modeli | zamknięty rdzeń: nie załatasz runtime'u, nie wskażesz commita silnika, nie zaudytujesz |
| MLX i GGUF obok siebie | regulamin zakazuje inżynierii wstecznej i redystrybucji |
| `llmster` + `lms` = skryptowalne na maszynie bez ekranu | mniej pokręteł próbkowania i harmonogramu niż w `llama-server` |
| endpointy OpenAI i Anthropic | ROCm/gfx1201 niezweryfikowane |
| pliki modeli leżą w zwykłym katalogu (`~/.lmstudio/models`), niski koszt wyjścia | firma może wprowadzić płatne warstwy (do 2025-07 do pracy była potrzebna licencja) |

### 3.9 Kiedy wybrać LM Studio

Gdy chcesz **tego samego API na Macu i na Ubuntu** i nie przeszkadza ci zamknięty kod; gdy ktoś nietechniczny ma korzystać z modeli lokalnie; gdy chcesz MLX i GGUF w jednym GUI. Nie wybieraj, gdy potrzebujesz przypiętego, audytowalnego silnika lub gdy sprzęt to karty AMD, o których dokumentacja milczy.

> **Sprawdź sam #3 — co jest otwarte w LM Studio.**
> `gh api orgs/lmstudio-ai/repos --paginate --jq '.[] | [.name,.license.spdx_id,.stargazers_count] | @tsv'` *(nie uruchamiałem; filtr jq mój, polecenie `gh api orgs/lmstudio-ai` było użyte w badaniu)*. Znajdziesz `lms`, `mlx-engine`, SDK i tracker, ale **żadnego repozytorium aplikacji ani forka llama.cpp**. Dla porównania otwórz `lmstudio.ai/terms` i znajdź zapis o zakazie inżynierii wstecznej.

---

## 4. llmman: modele jako obrazy OCI

**W jednym zdaniu:** jednoplikowy program w Rust, który traktuje modele jak artefakty OCI i potrafi wykonać `llmman launch claude --model qwen3.8`: uruchamia lokalnego demona `serve`, odpala **niezmodyfikowany** silnik upstreamowy, wystawia API Ollamy, OpenAI, Anthropic i Gemini, a następnie uruchamia agenta kodującego skierowanego na ten serwer.

### 4.1 Kto za tym stoi, i co jest prawdziwe, a co aspiracyjne

Repozytorium `llmmanorg/llmman`, Apache-2.0, utworzone **2026-03-22**; pierwszy commit w historii **2026-05-02**; 567 commitów; wydanie **v0.1.567 z 2026-10-19** (CI ustawia numer łatki na liczbę commitów: "każdy commit na main wychodzi jako wydanie"). 563 gwiazdki, 67 forków. Organizacja `llmmanorg` założona 2026-08-14, bez opisu i linków; blog zaczyna się 2026-08-31 wpisem "Introducing llmman".

Główny autor: **Eric Curtin** (`ericcurtin`, 402 commity z ~567; kolejni: ricky-chaoju 57, HassanBahati 40, doringeman 14, maxgio92 12). Adres commitów llmmana to `@docker.com`; wcześniejsze commity do RamaLamy mają adres `@redhat.com` (ostatni 2025-08-11), a pierwszy commit do `docker/model-runner` pochodzi z 2025-08-18. Czyli Red Hat → Docker, z dokładnymi datami zatrudnienia *(niezweryfikowane)*. Curtin współtworzył RamaLamę i jest jednym z głównych opiekunów Docker Model Runnera.

**Czy to produkt Dockera?** Za: pracodawca autora, obraz `docker.io/ai/llmman` (przestrzeń `ai/` to przestrzeń Dockera), typy mediów Dockera, współautor z Dockera (doringeman), Docker Agent i Sandboxes jako pierwszoklasowe cele. Przeciw: osobna organizacja GitHub bez brandingu Dockera, brak not Dockera, strona nie mówi, kto za tym stoi. **Wniosek: projekt osobisty inżyniera Dockera z narzędziami z ekosystemu Dockera; żadnego oficjalnego sponsoringu nie stwierdzono** *(niezweryfikowane)*. Nie ma firmy, przychodu ani finansowania. *Bus factor* około 1 (402 z ~567 commitów).

Co jest **prawdziwe** (kod przeczytany): ~98,9 tys. linii Rust; `src/cmd/serve/` 30,7 tys. (nakładki API Ollamy, OpenAI, Anthropic, Responses, Gemini, planista `sched.rs`, `aggregation.rs`, `hybrid.rs`), `src/mediagen/` 10,3 tys. (własna dyfuzja w ggml), `src/cmd/launch/` 9,2 tys. (integracje agentów i piaskownice), `src/storage/` 2,8 tys. (magazyn OCI + GC), `src/modelpack.rs`; shim w Go (7,5 tys. linii, `go-shim/`) kompilowany przez CGO do obsługi rejestrów i transferu OCI.

Co jest **aspiracyjne lub nieudowodnione:** README i dokumenty twierdzą, że zmiany mają "przewyższać wszystkie porównywalne rozwiązania" (`AGENTS.md`), ale **żadnych danych** na to nie ma *(dane projektu)*; własnych pomiarów brak; wersja 0.1.x; dominujący autor. Kod powstaje z pomocą agentów kodujących (jest `AGENTS.md`); 98 tys. linii w pięć miesięcy przy ~4 commitach dziennie jest z tym spójne, ale to moje wnioskowanie *(niezweryfikowane)*. Telemetrii w kodzie nie przeszukiwałem.

### 4.2 Po co to jest

Dla deweloperów, którzy chcą dowolnego agenta (Claude Code, Codex, OpenCode, Cline, Aider, Gemini CLI, goose, Docker Agent i kilkanaście innych) na dowolnym modelu, lokalnym lub hostowanym, z łańcuchem dostaw modeli wyglądającym jak łańcuch dostaw kontenerów: lustra rejestrów, podpisy cosign, transfer do środowisk odciętych. **Nie dostarcza silnika**: "llmman does not ship an inference engine" (`docs/backends.md`).

### 4.3 Funkcje

Polecenia: `pull|push|transfer|run|serve|launch|list|ps|stop|show|rm|search|build|verify|config|usage|log`. `serve` nasłuchuje na `127.0.0.1:17434` i mówi po **Ollamie** (`/api/*`; prawdziwe `ollama` CLI działa po ustawieniu `OLLAMA_HOST`), **OpenAI** (czat, completions, embeddings, models, responses, transkrypcja, obrazy/wideo/mowa dla dyfuzji) i **Anthropic** (`/v1/messages`), plus Gemini i `/v1/systemone`. Narzędzia, wizja, wyjście ustrukturyzowane, embeddingi (GGUF), UI na `/`, metryki Prometheusa `/metrics`.

Dodatki: **agregacja** (demony łączą się w pulę; żądanie trafia do węzła z załadowanym modelem lub największą ilością miejsca), pary **hybrydowe** (`--overflow-provider`: zbyt duże żądania idą do modelu hostowanego), **piaskownice** (`--sandbox sbx|seatbelt|docker|podman|apple-container|microsandbox|openshell`), dostawcy z models.dev.

### 4.4 Silniki i sprzęt

Z `docs/backends.md`:

| Format | Silnik |
|---|---|
| GGUF | upstreamowy `llama-server`: obraz `ghcr.io/ggml-org/llama.cpp:server-{cuda,cuda13,rocm,vulkan}-<wydanie>` na Linuksie przez docker/podman; albo pobrany gotowy zasób wydania (`--runtime bin`); albo z `PATH` (`--runtime path`) |
| safetensors | `vllm` (na AMD x86_64 obraz `rocm/vllm:latest`), `sglang`, `mlx_lm.server` na macOS (instaluje własne `uv` + mlx-lm) |
| opcjonalnie | `ds4-server` |
| dyfuzja | w procesie na ggml; Diffusers przez vLLM-Omni |

Przypięte wersje: `LLAMA_CPP_RELEASE` = b11429, `MLX_LM_RELEASE` = 0.31.3. Kolejność sondowania GPU: CUDA, ROCm, OpenCL (Adreno), Vulkan, Metal; `LLMMAN_LLM_LIBRARY` nadpisuje. Llama.cpp nie dostarcza gotowego buildu CUDA dla Linuksa, więc na NVIDIA+Linux tryb `auto` woli kontener.

**AMD:** istnieje ścieżka ROCm (obraz `server-rocm`), ale notatki **nie wymieniają gfx1201** i nie sprawdzano jej na R9700 *(niezweryfikowane)*.

### 4.5 Architektura

**Obrazy modeli OCI.** Lokalny magazyn to *OCI Image Layout* (`<root>/oci-layout`, `manifests/<ścieżka ref>/<tag>` jako mały deskryptor JSON na referencję "odzwierciedlający układ manifestów Ollamy", `blobs/sha256/<hex>`): `src/storage/oci.rs`. Typy mediów manifestu: **CNCF ModelPack** (`application/vnd.cncf.model.config.v1+json`, pliki kluczowane przez `org.cncf.model.filepath`) oraz Docker Model Runnera `application/vnd.docker.ai.gguf.v3` dla warstw GGUF (`src/modelpack.rs`, `HF_GGUF_MEDIA_TYPE`). `modelpack::resolve_model` zwraca `ModelPath::{Gguf(+mmproj), SafeTensors, Diffusion, Omni}` i na tej podstawie wybiera backend. Operacje na rejestrze przechodzą przez shim w Go (pomocnicy poświadczeń docker/podman, lustra, weryfikacja cosign). `llmman transfer hf.co/... docker.io/...` przesyła strumieniowo bez lądowania w magazynie lokalnym.

**Przepływ żądania.** HTTP (obsługa w stylu axum, `src/cmd/serve/*`) → `ensure_model` (`backend.rs`) uruchamia proces backendu per model na losowym porcie (flagi `llama-server`: `--model --port --host --ctx-size --flash-attn --cache-type-k/v --parallel --threads --split-mode --mmproj --embeddings`) → proxy i tłumaczenie. Reaper bezczynności (`sched.rs`) odwzorowuje keep-alive Ollamy (domyślnie 5 minut, `LLMMAN_KEEP_ALIVE`); nazwy zmiennych środowiskowych celowo odbijają Ollamę (`LLMMAN_MAX_LOADED_MODELS`, `LLMMAN_NUM_PARALLEL`, `LLMMAN_SCHED_SPREAD`, `LLMMAN_KV_CACHE_TYPE`, `LLMMAN_FLASH_ATTENTION`). Klucz API jest wymagany, gdy nasłuch jest poza loopbackiem; TLS opcjonalny.

### 4.6 Mocne i słabe strony

+ Czyste silniki (bez opóźnienia forka): przypięcie b11429 przy b11669 u Ollamy oznacza, że oba są w odległości dni od upstreamu; jedno polecenie do startu agenta; podpisany łańcuch dostaw OCI; agregacja między Makiem a rigiem.
− Bardzo młody (pierwszy commit w maju 2026), v0.1.x, jeden dominujący autor, deklaracje "przewyższa konkurencję" bez danych. README opisuje Ollamę jako "Bundled llama.cpp/ggml fork plus Ollama's own engine", **co jest nieaktualne od 2026-05-29** (sekcja 2.3). Wybór typów mediów wiąże projekt z przestrzenią `ai/` Dockera.

### 4.7 Kiedy wybrać llmmana

Gdy interesuje cię **dystrybucja modeli przez rejestr kontenerów** (Harbor, Artifactory, ghcr), podpisy i transfer do środowisk odciętych, i gdy akceptujesz ryzyko wersji 0.1.x. Dla rigu referencyjnego to raczej **źródło pomysłów** (sekcja 8) niż zamiennik llama-swap, choć autor notatek zauważa, że można by nim zastąpić llama-swap, jeśli chcesz modeli jako OCI i API Anthropic/Ollama.

---

## 5. Pozostałe opakowania

Zwięźle: tożsamość, architektura w kilku zdaniach, akapit "Kto za tym stoi", uwaga o AMD (tylko to, co mówią notatki) i **"Kiedy wybrać"**. Dla Jana, LocalAI, Lemonade, Docker Model Runnera, RamaLamy i GPT4All opieram się na README, drzewach plików i wybranych plikach z API GitHuba, nie na pełnym checkoucie.

### 5.1 Jan

**Co to:** otwartoźródłowa aplikacja desktopowa w stylu ChatGPT (Tauri: Rust + React/TS), uruchamiająca GGUF przez wbudowany proces roboczy llama.cpp, MLX na Macach, z możliwością łączenia z dostawcami chmurowymi. `janhq/jan`, utworzone 2023-08-17, **45 017 gwiazdek**, **v0.8.6 (2026-10-09)**.

**Licencja.** `LICENSE` to Apache-2.0 plus jedno dopisane zdanie: "Attribution is requested in user-facing documentation and materials, where appropriate." Przez tę modyfikację GitHub pokazuje NOASSERTION; w praktyce to Apache-2.0 z niewiążącą prośbą o atrybucję.

**Architektura.** `src-tauri/` (Rust + wtyczki `llamacpp`, `mlx`, `hardware`, `rag`, `websearch`, `agent-tools`), `extensions/` (TS), `mlx-server/` (pakiet Swift: serwer w kształcie OpenAI i Anthropic na MLX-Swift, wymaga Xcode 26.2), `web-app/`. Od **v0.8.5 (2026-10-08)** llama.cpp jest **linkowane statycznie** do `jan-llama-worker` (`engine/mod.rs`: "no llama-server child, no downloaded binary"; dostęp do `server_routes` przez shim C++), ale nadal w osobnym nadzorowanym procesie, bo `GGML_ASSERT` wywołuje `abort()` — ten sam powód co w Ollamie. Wersję przypina `JAN_LLAMA_CPP_TAG`. GUI wystawia `--n-cpu-moe`, podział tensorów, `fit` i `models_max` (`extensions/llamacpp-extension/settings.json`).

**Funkcje.** Serwer zgodny z OpenAI na `localhost:1337`, MCP, łączniki chmurowe (OpenAI, Anthropic, Mistral, Groq…), własne dostrojone modele Menlo na Hugging Face. **Offline:** tak; analityka opt-in (PostHog EU) *(dane projektu)*; plugin aktualizacji obecny.

**AMD.** Backend **ROCm/HIP na Linuksie od v0.8.2 (2026-06-01)** (changelog); gfx1201 niewymieniony.

**Kto za tym stoi.** Menlo Research, dziś przedstawiająca się jako producent **humanoidalnych robotów** (Asimov 1). Finansowania, założycieli i inwestorów **nie znalazłem** — nie wpisuję liczb. Jan nie ma widocznego przychodu *(dane projektu)*. Ryzyko: komunikacja firmy-matki dotyczy robotów. Zob. [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

**Kiedy wybrać:** gdy chcesz **otwartego** odpowiednika LM Studio z GUI i przełączaniem model lokalny / chmurowy. Wzorzec do skopiowania: nadzorowany proces roboczy z routerem i presetami.

### 5.2 GPT4All

**Co to:** aplikacja desktopowa Nomic AI (Qt/C++/QML) z lokalnym czatem i *LocalDocs* (RAG na `usearch`). MIT, **77 350 gwiazdek**, utworzona 2023-03-27; silnik to **fork** llama.cpp (`llama.cpp-mainline`), GPU przez Vulkan (README: Q4_0/Q4_1 na NVIDIA i AMD).

**Werdykt:** ostatnie wydanie **v3.10.0 z 2025-02-25**, ostatni commit **2025-05-27** (~17 miesięcy ciszy), 775 otwartych zgłoszeń, README bez słowa o trybie podtrzymania. **De facto niepielęgnowany; oficjalnego oświadczenia nie znalazłem.** Fork silnika stanął w połowie 2025, więc nowe architektury modeli odpadają.

**Kto za tym stoi.** Nomic (CEO Andriy Mulyar; seria A 2023 na 17 mln USD pod przewodnictwem Coatue *(dane firmy)*) robi dziś "AI dla AEC" (architektura, inżynieria, budownictwo); GPT4All nie występuje na nomic.ai. Produkt był lejkiem marketingowym, a po pivocie projekt zamarł. MIT pozwala na fork, ale prawdziwym kosztem jest gnijący fork silnika.

**Kiedy wybrać:** **nie do nowych zastosowań.**

### 5.3 LocalAI

**Co to:** serwer w Go (API zgodne z OpenAI, Anthropic, Ollamą, ElevenLabs): **mały rdzeń + backendy na żądanie**, każdy jako obraz OCI z kontraktem gRPC; tekst, wizja, mowa, obraz, wideo, tryb rozproszony. `mudler/LocalAI`, MIT, **49 695 gwiazdek**, utworzone 2023-03-18, **v4.11.0 (2026-10-02)**.

**Architektura** (`backend/backend.proto`, `pkg/model/process.go`): `core/http` → ModelLoader → **proces backendu per model** rozmawiający po gRPC (usługa `Backend`, ok. 55 wywołań: `Predict`, `Embedding`, `GenerateImage`, `TTS`, `Rerank`…). Backendy (60+) w `backend/{cpp,go,python,rust}`: llama-cpp, vllm, sglang, mlx, whisper, diffusers… **Publikowane jako obrazy OCI z Galerii Backendów**, podpisane cosign od v4.3.0; od v3.2.0 (2025-07) wszystkie poza głównym plikiem binarnym. Wykrywanie GPU wybiera obraz (CUDA 12/13, ROCm, SYCL, Metal, Vulkan, Jetson). Tryb rozproszony z routingiem świadomym VRAM-u (v4.1.0, 2026-04), OIDC/klucze/limity, MCP, Realtime API.

**AMD:** ROCm na liście sprzętu; **dostępność obrazu per backend dla gfx1201 niesprawdzona** *(niezweryfikowane)*. **Offline:** po pobraniu backendu i modelu; oba pobierane na żądanie.

**Mocne/słabe:** + najszersze pokrycie modalności, izolacja silników, vLLM/SGLang per model; − cienki szlif per backend, dużo YAML-a, jeden dominujący opiekun, szybki dryf.

**Kto za tym stoi.** Ettore Di Giacinto (`mudler`, ex-SUSE/Rancher); 3 507 commitów jego, reszta głównie boty. README wymienia sponsorów pokrywających CI (Spectro Cloud, solstone.app); firmy ani finansowania nie ujawniono. Zob. [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md).

**Kiedy wybrać:** gdy potrzebujesz **jednego API na wiele modalności i wiele silników** (llama.cpp-ROCm obok vLLM-ROCm) i akceptujesz złożoną konfigurację. Szablon "backend jako obraz OCI + gRPC" jest najczystszy w tej grupie.

### 5.4 Lemonade (AMD): dla ciebie najważniejsze z tej grupy

**Co to:** serwer/runtime w C++ z API OpenAI, Anthropic i Ollamy, który wybiera spośród backendów: llama.cpp (Vulkan/ROCm/CUDA/Metal/CPU), FastFlowLM i Ryzen AI OGA (**NPU XDNA2**), vLLM-ROCm, whisper.cpp, stable-diffusion.cpp, Kokoro. Najprościej: **odpowiedź w stylu AMD na Ollamę**. `lemonade-sdk/lemonade`, **Apache-2.0**, **5 936 gwiazdek**, utworzone 2025-05-15, wydania co tydzień (`v2026.42.1` z 2026-10-14). Najwięcej commitów: `jeremyfowers` 569, `superm1` (Mario Limonciello) 150, `fl0rianr` 121, `ramkrishna2910` 111, `danielholanda` 81.

**Związek z AMD (zweryfikowany).** README: "built by the community for every PC, with optimizations by AMD engineers to get the most from Ryzen AI, Radeon, and Strix Halo PCs". Jeremy Fowers, Daniel Holanda i Ramakrishnan Sivakumar wpisują na GitHubie firmę **AMD**; Limonciello commituje z `@amd.com`; 14 z ostatnich 100 commitów ma adresy `amd.com` (59 to noreply, więc prawdziwy udział jest wyższy). **FastFlowLM** (runtime NPU) mieszka w `github.com/ROCm/FastFlowLM`, a jego jądra to "Copyright (c) 2026 Advanced Micro Devices, Inc.", "not open source", swobodnie redystrybuowalne bez zmian. Nie ma zdania "Lemonade to projekt AMD" (osobna organizacja `lemonade-sdk`), ale rdzeń to pracownicy AMD; finansowanie = płace AMD *(warunki niezweryfikowane)*.

**Tabela backendów** (`docs/dev/backends-reference.md`, generowana z deskryptorów C++; skrót):

| Backend | Cele | Uwagi |
|---|---|---|
| `llamacpp` | cpu, cuda (sm_75…sm_121), metal, **rocm** (gfx103X, gfx110X, gfx1150–1152, **gfx120X**, gfx908/90a/942/950), vulkan, system | `system` = twój własny `llama-server` |
| `llamacpp-hrx` | eksperymentalny: gfx1100/gfx1151 | |
| `flm` (FastFlowLM) | NPU XDNA2, Windows i Linux | jądra zamknięte |
| `ryzenai-llm` (OGA) | NPU, tylko Windows | |
| `vllm` rocm | eksperymentalny: gfx110X/1150/1151/**120X** | |
| `ds4` (gość) | gfx1151 | zob. [`07-APPLE-MLX-OMLX-I-DS4.md`](07-APPLE-MLX-OMLX-I-DS4.md) |
| `whispercpp`, `sd-cpp`, `kokoro`, `onnxruntime`… | różne | |

**gfx1201 a ta tabela.** R9700 to gfx1201, tabela mówi o rodzinie **`gfx120X`**; notatki wnioskują, że gfx1201 się w niej mieści, czyli llama.cpp-ROCm (Linux i Windows), vLLM-ROCm (eksperymentalnie), sd.cpp i whisper. To wniosek z nazwy rodziny, nie wpis wprost, i nie sprawdzony na sprzęcie *(niezweryfikowane)*.

**Czym różni się od "llama.cpp-ROCm zbudowanego samemu":** (1) **dystrybuuje gotowe buildy** llama.cpp z ROCm 7 (`lemonade-sdk/llamacpp-rocm`, 786 gwiazdek; kanały "Stable" i "Nightly"; także `vllm-rocm`, `whisper.cpp-rocm`, `ds4-rocm`); (2) wykrywa rodzinę urządzenia i pobiera właściwy backend (`lemonade backends`); (3) dodaje ścieżki NPU, których llama.cpp nie ma; (4) menedżer modeli (`lemonade pull`, aliasy z failoverem active-standby, telemetria OTLP); (5) *osadzalny* plik binarny dla aplikacji. Dokumentacja poleca Vulkan "dla większości użytkowników GPU", a ROCm "może przewyższać Vulkan". Na wielokartowym rigu pod spodem nadal jest llama.cpp (`llamacpp.backend=system` pozwala użyć własnego `llama-server`).

**Słabości:** NPU głównie na Windows; część backendów eksperymentalna; priorytety AMD (najpierw Strix Halo); wielokartowy podział to to, co daje llama.cpp/vLLM. **Offline:** lokalnie tak; backendy i modele pobierane przy pierwszym użyciu; FLM sprawdza wersję przy starcie, chyba że `FLM_DISABLE_UPDATE_CHECK=1`; strona deklaruje "zero telemetrii" *(dane projektu)*.

**Kiedy wybrać:** gdy sprzęt to **Ryzen AI / Strix Halo / Radeon** i chcesz gotowych buildów ROCm lub ścieżki NPU. Na rigu referencyjnym to przede wszystkim **ściągawka**: tabela wsparcia `gfx120X` i gotowe buildy jako punkt odniesienia dla własnego buildu.

> **Sprawdź sam #4 — co Lemonade mówi o gfx120X.**
> `gh api repos/lemonade-sdk/lemonade/contents/docs/dev/backends-reference.md --jq .content | base64 -d | grep -n -i "gfx120"` *(nie uruchamiałem tego polecenia; plik czytałem przez API)*. Szukaj wierszy `llamacpp` (rocm) i `vllm` (rocm). Związek z AMD: `gh api users/jeremyfowers --jq .company`.

### 5.5 Docker Model Runner (DMR)

**Co to:** runner "model jako artefakt OCI": `docker model pull|run|ls|ps …`, za nim demon w Go zarządzający silnikami llama.cpp / vLLM / SGLang / MLX / Diffusers; w Docker Desktop, Docker Engine (Linux) i jako samodzielny `dmr`. `docker/model-runner`, Apache-2.0, **658 gwiazdek**, utworzone 2025-03-28, **v1.2.8 (2026-08-12)**. Najwięcej commitów: `doringeman` 696, `ilopezluna` 387, **`ericcurtin` 318**.

**Silniki przypięte w `.versions`:** `LLAMA_SERVER_VERSION=b9879`, vLLM 0.19.1, SGLang 0.5.6. Llama.cpp to submoduł budowany przez Dockera; obrazy: `cpu` (upstream `server-vulkan`), `rocm` (`server-rocm`), CUDA. **Architektura:** `pkg/inference/scheduling/` — loader z **8 slotami runnerów** i **5-minutowym limitem bezczynności**, klucz runnera = (backend, skrót modelu, skrót draftu, tryb); `pkg/distribution` (126 plików) — klient i magazyn modeli OCI (Docker Hub `ai/`, dowolny rejestr, Hugging Face); nakładki API `pkg/anthropic`, `pkg/ollama`, `pkg/responses`; domyślnie OpenAI na `:12434`. Na macOS/Windows silniki biegną jako izolowane procesy hosta, na Linuksie w kontenerach *(dane firmy)*.

**Pieniądze:** w pakiecie z Docker Desktop/Engine; to funkcja zatrzymująca deweloperów na Docker Hub, nie linia produktowa *(niezweryfikowane)*. **AMD:** ROCm tylko na Linuksie, gfx1201 niewymieniony; strojenie wielu GPU ograniczone względem samego `llama-server`.

**Kiedy wybrać:** gdy **już żyjesz w Dockerze** i chcesz modeli jako artefaktów w tych samych rejestrach co obrazy. Zauważ przypięty `b9879` — starszy silnik niż b11669 w Ollamie *(moje wyliczenie z numerów buildów)*.

### 5.6 RamaLama

**Co to:** CLI w Pythonie (`ramalama run|serve|pull|push|bench`), które wykrywa GPU, ściąga **pasujący obraz kontenera** z silnikiem w środku i uruchamia model w bezrootowym kontenerze podman/docker **domyślnie bez sieci**. Org `containers` (rodzina Podmana), opiekunowie z Red Hata. MIT, **3 086 gwiazdek**, utworzone 2024-07-24, **v0.25.0 (2026-09-25)**.

**Wybór obrazu po zmiennej środowiskowej** (README): Vulkan/CPU → `quay.io/ramalama/ramalama`; **`HIP_VISIBLE_DEVICES` → `quay.io/ramalama/rocm`**; `CUDA_VISIBLE_DEVICES` → `…/cuda`; Asahi, Intel, CANN, MUSA — własne obrazy. Znacznik = mniejsza wersja RamaLamy, nadpisanie przez `--image`. Źródła modeli: `ollama://`, `huggingface://`, ModelScope, `oci://`. Na macOS llama.cpp lub MLX na hoście.

**Kto za tym stoi.** Red Hat (IBM) płaci opiekunom (Dan Walsh, Mike Bonnet, Oliver Walsh) *(strategia RHEL AI / Podman AI Lab: niezweryfikowane)*; przychodu własnego brak. Dan Walsh (`rhatdan`, 1 462 commity) ma na GitHubie status "Retired". Eric Curtin współtworzył projekt (971 commitów) i przeszedł do Dockera (sekcja 4.1).

**AMD:** `quay.io/ramalama/rocm` to gotowy czysty userland ROCm; gfx1201 niewymieniony. **Vs Ollama:** kontenery + silniki upstream + rootless, bez własnej biblioteki modeli i chmury.

**Kiedy wybrać:** gdy **izolacja** jest ważniejsza od wygody (agent w piaskownicy `--network none`), na Fedorze/RHEL, i gdy chcesz obrazów per GPU bez budowania.

---

## 6. Frontendy, które nie są runtime'ami

Nie liczą tokenów: są **klientami** wszystkiego, co opisałem wyżej.

### 6.1 Open WebUI

Webowy czat/RAG (FastAPI + Svelte) rozmawiający z Ollamą i backendami zgodnymi z OpenAI. **156 189 gwiazdek**, v0.12.3 (2026-10-16), główny autor `tjbck` (13 450 commitów).

**Licencja (uwaga praktyczna).** MIT, potem BSD-3-Clause; **od v0.6.6 (2025-04-19)** własna "Open WebUI License": BSD-3 plus klauzula 4 — nie wolno zmieniać, usuwać ani zasłaniać nazwy "Open WebUI", **chyba że** (i) masz co najwyżej 50 użytkowników końcowych w ruchomym oknie 30 dni, (ii) masz pisemną zgodę albo (iii) licencję enterprise. Współtwórcy podpisują CLA; kod sprzed zmiany zostaje na BSD/MIT (`LICENSE_HISTORY`). GitHub pokazuje NOASSERTION; licencja **nie jest zatwierdzona przez OSI**. Uzasadnienie: powstrzymać zmianę marki i komercyjne przepakowanie bez wkładu *(dane projektu)*. **Pieniądze:** licencje enterprise/white-label, wsparcie (ceny niepubliczne) *(dane projektu)*; finansowania nie zweryfikowałem.

**Kiedy wybrać:** przeglądarkowy czat dla zespołu do twojego serwera zgodnego z OpenAI (np. llama-swap). Do własnego zespołu z oryginalnym brandingiem — bez problemu; white-label wymaga umowy.

### 6.2 AnythingLLM

All-in-one RAG/agenci (desktop + Docker, Node/React) z bazą wektorową, MCP i budowniczym agentów; używa zewnętrznego runtime'u albo opcjonalnego wbudowanego silnika "napędzanego przez Lemonade i llama.cpp" (README). Mintplex Labs, MIT, **67 323 gwiazdki**, v1.18.0 (2026-10-13), autor `timothycarambat`.

**Pieniądze** *(dane firmy: anythingllm.com/pricing)*: desktop darmowy; chmura **50 USD/mies. (Basic)** i **99 USD/mies. (Pro, SLA wsparcia 72 h)**; Enterprise na zapytanie. Finansowania nie zweryfikowałem. To *klient* Ollamy, LM Studio, LocalAI — nie konkurent.

**Kiedy wybrać:** RAG po dokumentach i agenci w jednej aplikacji, gdy silnik masz gdzie indziej.

---

## 7. Co się psuje, gdy sponsor zmieni zdanie

Opakowanie jest produktem czyjejś firmy albo czyjegoś wolnego czasu. Ta tabela odpowiada na pytanie: *co konkretnie przestaje działać lub przestaje się rozwijać, jeśli ten, kto płaci (albo pisze), zmieni plany — i ile kosztuje ucieczka?* Opis modeli finansowania i ludzi jest w [`10-PIENIADZE-I-LUDZIE.md`](10-PIENIADZE-I-LUDZIE.md); tu tylko skutki techniczne.

| Produkt | Kto steruje | Silnik | Co się psuje | Co zostaje | Koszt wyjścia |
|---|---|---|---|---|---|
| **Ollama** | Ollama, Inc. (VC; 88 mln USD wg firmy) | upstream `llama-server` + własny MLX | biblioteka i rejestr modeli, szablony i parsery, chmura; ceny chmury już raz zmieniono (z czasu GPU na tokeny, 2026-08-31). Jeśli rejestr lub konta przestaną działać, nowe pobrania modeli z biblioteki stają | pobrane modele nadal działają; kod MIT można rozwidlić | **średni**: modele są blobami (trzeba wyeksportować do GGUF), a moat to biblioteka, nie kod |
| **LM Studio** | Element Labs (zamknięty; finansowanie nieznane) | zamknięte runtime'y llama.cpp + MLX | "free for work" może się skończyć (wcześniej wymagano licencji), runtime'y zamarzną jako binaria, kierunek Bionic/chmura | pliki modeli w zwykłym katalogu | **niski** dla modeli, ale GUI i demona nie rozwidlisz |
| **llmman** | jedna osoba (pracownik Dockera) | upstream bez zmian | porzucenie projektu | silniki są upstreamowe, modele to standardowe OCI/HF | **bardzo niski** |
| **Jan** | Menlo Research (komunikacja o robotyce) | wbudowane llama.cpp + własny MLX | opiekunowie mogą się przesunąć; aktualizator i telemetria są pod kontrolą Menlo | kod Apache-2.0, zwykłe GGUF | **niski do średniego** (fork ciężki: Rust+TS+Swift) |
| **GPT4All** | Nomic (pivot na AEC) | przestarzały fork llama.cpp | **już się stało**: zamrożone od 2025-05 | licencja MIT, ale fork silnika gnije | nie dotyczy: porzucone |
| **LocalAI** | mudler + sponsorzy | 60+ silników w obrazach OCI | przepustowość opiekuna | MIT, modułowość | niski |
| **Lemonade** | inżynierowie AMD + społeczność | llama.cpp (+ NPU FLM/OGA) | przestałyby się poprawiać zamknięte jądra NPU (binaria FLM) i budowane przez AMD obrazy ROCm | generyczne backendy llama.cpp dalej działają; rdzeń C++ Apache-2.0 do rozwidlenia | niski dla ścieżek GPU |
| **Docker Model Runner** | Docker, Inc. | llama.cpp / vLLM / SGLang / MLX / Diffusers | priorytety (pokrycie AMD i Metal) | Apache-2.0, artefakty OCI zgodne z ModelPack | niski |
| **RamaLama** | Red Hat (opiekunowie) | llama.cpp / vLLM w obrazach per GPU | przestałyby się odświeżać obrazy na quay.io | MIT; obrazy można budować samemu z `container-images/` | niski |
| **Open WebUI** | Open WebUI Inc. | brak | zaostrzenie licencji (**już zrobione w 2025**) | wersje do v0.6.5 na BSD | można przypiąć stary fork |
| **AnythingLLM** | Mintplex Labs | brak / opcjonalny | ceny chmury | MIT | niski |

Dwa przypadki warte zapamiętania. **GPT4All**: firma znalazła lepszy rynek, a otwarty projekt zamarł. **Open WebUI**: licencja zmieniana dwukrotnie (MIT → BSD-3 → BSD-3 + klauzula brandingowa); "otwarte" nie znaczy "niezmienne".

---

## 8. Co z tego dla konfiguracji referencyjnej

### 8.1 Dlaczego uruchamiasz llama.cpp + llama-swap bezpośrednio

Rig referencyjny to 4× R9700 (gfx1201, ROCm), model 284B MoE (DeepSeek-V4-Flash, UD-IQ3_XXS) przy ~50 tok/s, a o tym wyniku decydują ustawienia, które opakowania często chowają. Powody, dla których to ma sens, w kolejności ważności:

1. **Pokrętła.** Ustawienia z przewodnika [`../przyspieszanie-generowania/README.md`](../przyspieszanie-generowania/README.md) (podział tensorowy, dekodowanie spekulatywne) oraz takie flagi jak `--n-cpu-moe` to flagi `llama-server`. W Ollamie dostępne są tylko te, które Ollama przepuszcza przez własne zmienne `OLLAMA_*` i pole `options`; w LM Studio — te, które pokazuje GUI. Przy modelu tej wielkości różnica między domyślnym a dostrojonym rozmieszczeniem na czterech kartach to różnica między "działa" a "działa szybko" *(moja ocena, bez pomiaru)*.
2. **Przypięty build.** Produkcja stoi na buildzie `0ce8cd1`, który wybierasz ty. Ollama buduje przypiętą wersję upstreamu **z własną warstwą łatek** (b11669 w sprawdzanym klonie), LM Studio dostarcza zamknięte runtime'y, które aktualizuje według własnego rytmu.
3. **Rozmieszczenie GPU.** llama-swap ma **grupy i macierz** (z kosztami wyrzucania): jedna pozycja "70B gęsty na czterech kartach" (`HIP_VISIBLE_DEVICES=0,1,2,3`), druga "dwa modele 30B na kartach 0–1 i 2–3", trzecia "zawsze włączony embedding/rerank na osobnym kawałku". Ollama ma heurystykę "najpierw jedna karta, potem podział" i `OLLAMA_SCHED_SPREAD`, ale **nie ma odpowiednika macierzy** *(moje wnioskowanie z lektury `sched.go`, nie z dokumentu)*.
4. **Zwykłe pliki GGUF.** Modele leżą jako pliki, które widzą wszystkie twoje narzędzia (llama-bench, quantize, imatrix); w Ollamie są blobami `sha256-…`.
5. **Minimalizm zależności.** llama-swap to jeden statyczny plik w Go, ale uczciwie: to też projekt z *bus factorem* 1 (Benson Wong, około 82% commitów, licencja MIT), więc ryzyko "jedna osoba" masz tak samo jak przy llmmanie. Różnica: jest mały i łatwy do rozwidlenia lub zastąpienia.

**Uwaga o nowszym llama.cpp:** sam `llama-server` ma już **tryb routera** (`--models-dir`, `--models-preset`, `--models-max`, domyślnie 4 modele jednocześnie): uruchamia proces potomny `llama-server` na model, wyrzuca najdawniej używany bezczynny model (LRU) i obsługuje `--sleep-idle-seconds`. To "wbudowany mini llama-swap" bez grup i macierzy. W świetle tego wartość "pełnego" opakowania dla lifecycle'u modeli maleje; przestrzeń, której llama.cpp nie pokrywa, to rejestr modeli, GUI i tłumaczenie API. Szczegóły routera: [`04-LLAMA-CPP-I-RODZINA-GGML.md`](04-LLAMA-CPP-I-RODZINA-GGML.md).

### 8.2 Co zyskałbyś, a co stracił

**Gdybyś przeszedł na Ollamę:**

| Zyskujesz | Tracisz |
|---|---|
| bibliotekę modeli z gotowymi szablonami i parserami narzędzi | pełny zestaw flag `llama-server` i swój build |
| `ollama launch` dla agentów, "dostawcę Ollama" w każdym narzędziu | macierz GPU z llama-swap (sekcja 8.1, punkt 3) |
| na Macach: **własny runner MLX** i wybór silnika per tag (listy manifestów) | zwykłe pliki `.gguf` |
| zarządzanie cyklem życia bez konfiguracji | przewidywalne domyślne wartości (limit 1 równoległego żądania, 3 modele/GPU, kontekst zależny od VRAM-u, 5 min keep-alive) |
| (R9700 wymienione w `docs/gpu.mdx`, ROCm v7) | pewność, że to zadziała dla modelu referencyjnego 284B: tego nie sprawdzałem |

**Gdybyś przeszedł na LM Studio (`llmster` + `lms` na Ubuntu, GUI na Macu):**

| Zyskujesz | Tracisz |
|---|---|
| to samo API (OpenAI + Anthropic) i ten sam program na Macu i na Ubuntu | audytowalność i swobodę wyboru buildu silnika |
| JIT + TTL, `lms runtime` do przypinania wersji silnika per maszyna | ROCm/gfx1201: nie ma potwierdzenia (strona runtime'ów zwróciła 404) |
| stanowe `/v1/chat` z `response_id` — wygodne dla agentów | część pokręteł; regulamin zabrania inżynierii wstecznej |

### 8.3 Co pożyczyć, nie przesiadając się

1. **Dystrybucja modeli jako OCI** (llmman, Docker Model Runner, RamaLama, Ollama): typy mediów CNCF ModelPack lub `application/vnd.docker.ai.gguf.v3`, lokalny *OCI Image Layout*. Zysk: Harbor/Artifactory/ghcr jako magazyn modeli w twojej infrastrukturze, podpisy cosign, transfer do środowisk odciętych (`llmman transfer`).
2. **Lista manifestów z polami `runner` i `format`** (Ollama): jeden tag, dwa buildy: GGUF dla rigu AMD i MLX dla Maka.
3. **Cykl życia modelu:** keep-alive + liczniki odwołań + "jedno ładowanie naraz" (Ollama) to minimalny rozsądny harmonogram dla wielomodelowego serwera; JIT + TTL (LM Studio); idle reaper (llmman).
4. **Heurystyka rozmieszczenia:** najpierw spróbuj zmieścić model na jednej karcie (`--split-mode none --main-gpu N`), dopiero potem dziel. Llama-swap może to wyrazić per model.
5. **Wzorzec compat:** tłumaczyć GGUF przy ładowaniu, a nie przy pobieraniu (`llama/compat/` w Ollamie), jeśli kiedyś potrzebujesz wspólnie konsumować pliki GGUF różnych źródeł.
6. **Macierz backendów Lemonade** (`docs/dev/backends-reference.md`) jako krzyżowa kontrola własnego buildu gfx1201 (wiersze `gfx120X`), oraz jego gotowe buildy llama.cpp-ROCm (`lemonade-sdk/llamacpp-rocm`) jako punkt odniesienia do porównania z referencyjnym `0ce8cd1`. Aliasy z failoverem active-standby jako pomysł do konfiguracji llama-swap.
7. **Backend jako obraz OCI + kontrakt gRPC** (LocalAI): najczystszy szablon "wiele silników, jedno API" (np. llama.cpp-ROCm i vLLM-ROCm wybierane per model).
8. **Izolacja agentów:** RamaLama z `--network none` w rootless kontenerze jako baza bezpieczeństwa dla piaskownic agentów; llmman z flagą `--sandbox`.
9. **UX "uruchom agenta na lokalnym modelu"** (`ollama launch`, `llmman launch`, `lemonade launch claude`): dla własnych aplikacji agentowych wystarczy skrypt, który ustawia zmienne środowiskowe i adres endpointu.
10. **Stanowe API rozmowy** (`response_id` w LM Studio): serwer pamięta stan, klient odsyła identyfikator. Pasuje do agentów z długimi sesjami.

### 8.4 Które opakowania mogą użyć kart gfx1201

Tylko to, co mówią notatki. ⚠️ **Żadnego z tych potwierdzeń nie sprawdzałem na sprzęcie.**

| Produkt | Co mówią notatki o AMD / R9700 |
|---|---|
| **Ollama** | `docs/gpu.mdx` wymienia **Radeon AI PRO R9700 / R9600D** w sekcji ROCm (wymagany ROCm v7); Vulkan domyślnie włączony. R9700 jest w dokumentacji, ale gfx1201 wprost nie pada; **nie testowane tu** |
| **LM Studio** | **niezweryfikowane** (dokumentacja runtime'ów niedostępna) |
| **llmman** | ścieżka ROCm istnieje (obraz `server-rocm`, `rocm/vllm:latest`), gfx1201 niewymieniony |
| **Jan** | backend ROCm/HIP na Linuksie od v0.8.2, gfx1201 niewymieniony |
| **GPT4All** | Vulkan na AMD w README; projekt uśpiony |
| **LocalAI** | ROCm na liście sprzętu; dostępność obrazu per backend niesprawdzona |
| **Lemonade** | tabela backendów wymienia rodzinę **`gfx120X`**; llama.cpp-ROCm (Linux i Windows), vLLM-ROCm eksperymentalnie, sd.cpp, whisper. Najbliższe wprost potwierdzenia dla R9700 w tej grupie, choć jako rodzina, nie jako gfx1201 |
| **Docker Model Runner** | ROCm na Linuksie (obraz `rocm`); gfx1201 niewymieniony; strojenie wielu GPU ograniczone |
| **RamaLama** | obraz `quay.io/ramalama/rocm` wybierany przez `HIP_VISIBLE_DEVICES`; gfx1201 niewymieniony |

Nie sprawdzałem, czy któreś z tych opakowań uruchomi model referencyjny DeepSeek-V4-Flash w UD-IQ3_XXS ani z jaką szybkością.

Całościowe porównanie i wybór: [`09-POROWNANIE-I-WYBOR.md`](09-POROWNANIE-I-WYBOR.md).

---

## 9. Czego nie ustaliłem

1. **Ollama:** czy brakujące noty licencyjne (issue #3185) są dziś w artefaktach; chronologia przejścia na `llama-server` (tag v0.30.0 z 13–14 maja vs PR #16031 z 29 maja vs blog z 5 czerwca); czy 88 mln USD to jedna runda czy suma (Wikipedia: 65 mln); wcześniejsze rundy; domyślny kontekst sprzed 2026; niezależne pomiary wydajności; czy próg kontekstu dla ≥ 48 GiB liczy się od jednej karty czy od sumy; czy Ollama wystawia tryby podziału znane z przewodnika o przyspieszaniu.
2. **LM Studio:** finansowanie i tytuły założycieli; lista backendów i ROCm/gfx1201; relacja z "Splash Engine" Inco AI; ceny Bionic i Teams; wersja po 0.4.0.
3. **llmman:** czy Docker go oficjalnie sponsoruje; telemetria w kodzie; benchmarki.
4. **Jan:** finansowanie Menlo; historia licencji (wcześniej AGPL? — niezweryfikowane); zachowanie aktualizatora.
5. **LocalAI:** pracodawca mudlera; ROCm dla gfx1201 per backend. **Lemonade:** formalna własność AMD; dojrzałość NPU na Linuksie. **Docker Model Runner:** szczegóły macOS i wielu GPU AMD. **RamaLama:** obsada po odejściu Dana Walsha, data odejścia Erica Curtina z Red Hata. **Open WebUI, AnythingLLM:** finansowanie i przychody.
6. **Ograniczenie metody:** dla Jana, GPT4All, LocalAI, Lemonade, Docker Model Runnera, RamaLamy, Open WebUI i AnythingLLM nie miałem pełnych checkoutów.

Źródła rozdziału: [`ZRODLA.md`](ZRODLA.md) oraz plik `05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md.sources.txt` obok.
