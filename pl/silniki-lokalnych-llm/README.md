# Silniki lokalnych LLM — od wielkiego obrazu do szczegółów kodu

**Stan na 19 października 2026.** Kurs o programach, które uruchamiają modele językowe na własnym sprzęcie: llama.cpp, Ollama, LM Studio, vLLM, SGLang, MLX i oMLX, ds4, llmman
i kilkunastu innych. Cel: zrozumieć **czym są, co robią, jak działają w środku, do czego służą i czym się różnią** — od mapy rynku po struktury danych w kodzie źródłowym —
oraz (w jednym osobnym rozdziale, nietechnicznym) **jak zarabiają i kto za nimi stoi**.

Większość kursu jest techniczna. Punkt odniesienia to twój sprzęt: 4× Radeon AI PRO R9700 (ROCm, gfx1201) z llama.cpp i llama-swap oraz Maki.

> ⚠️ **Jak powstał ten kurs i czego nie obiecuje.** To **research biurkowy i lektura kodu**: dokumentacja, API GitHuba, artykuły naukowe, strony projektów i repozytoria sklonowane
> na rigu (tylko do odczytu; commity w [`ZRODLA.md`](ZRODLA.md)). **Niczego tu nie uruchomiłem ani nie zmierzyłem** — karty pracują produkcyjnie, więc nie ma żadnych nowych pomiarów wydajności.
> Przeszukiwarka internetowa była w tej sesji niedostępna (wyczerpany limit zapytań), więc źródłami są strony i API pobierane bezpośrednio. Funduszowe liczby (rundy, wyceny) są najsłabszym ogniwem:
> każda ma tag źródła. Ten przegląd **starzeje się w tygodniach**; część materiału (np. przejęcia) jest świeża z ostatnich miesięcy.
> Oznaczenia: brak = sprawdzone w kodzie lub źródle pierwotnym · *(dane projektu/firmy)* = deklaracja zainteresowanej strony · *(prasa)* = doniesienie niepotwierdzone u źródła ·
> *(moje wyliczenie)* = arytmetyka na liczbach ze źródeł · *(niezweryfikowane)* = przypuszczenie.

## Dla kogo i jak czytać

Każdy rozdział zaczyna się od celu i kończy sekcją **„Co z tego dla mnie”** (praktyka na twoim sprzęcie) oraz ramkami **„Sprawdź sam”** — małymi ćwiczeniami do wykonania w prawdziwym kodzie
(komendy z notatek; nieuruchomione przeze mnie oznaczam).

| Chcesz… | Czytaj |
|---|---|
| zobaczyć całość w jednej tabeli i wybrać silnik | [09 · Porównanie i wybór](09-POROWNANIE-I-WYBOR.md) |
| zrozumieć strukturę świata lokalnych LLM | [01 · Mapa i warstwy](01-MAPA-I-WARSTWY.md) |
| zrozumieć, dlaczego generowanie jest takie, jakie jest | [02 · Jak działa inferencja](02-JAK-DZIALA-INFERENCJA.md) → [03 · Kwantyzacja i formaty](03-KWANTYZACJA-I-FORMATY.md) |
| wejść w silnik, na którym stoi twoja produkcja | [04 · llama.cpp i rodzina ggml](04-LLAMA-CPP-I-RODZINA-GGML.md) |
| rozumieć „gotowce” z oknem czatu | [05 · Opakowania: Ollama, LM Studio i inne](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) |
| zrozumieć silniki serwerowe i status AMD gfx1201 | [06 · Silniki serwerowe: vLLM, SGLang](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) |
| mieć plan dla Maców | [07 · Apple: MLX, oMLX, ds4, exo](07-APPLE-MLX-OMLX-I-DS4.md) |
| poznać nisze: ogromne MoE w RAM-ie, Rust, przeglądarka, NPU | [08 · Specjaliści](08-SPECJALISCI-KTRANSFORMERS-I-INNE.md) |
| zrozumieć pieniądze i ludzi (rozdział nietechniczny) | [10 · Pieniądze i ludzie](10-PIENIADZE-I-LUDZIE.md) |
| sprawdzić, skąd co wiem | [ZRODLA.md](ZRODLA.md) |

## Spis rozdziałów

| # | Rozdział | O czym | Typ |
|---|---|---|---|
| 01 | [Mapa i warstwy](01-MAPA-I-WARSTWY.md) | siedem warstw od pliku z wagami do okna czatu; ok. 35 projektów w tabelach; sieć zależności; pięć filozofii; oś czasu | wprowadzenie |
| 02 | [Jak działa inferencja](02-JAK-DZIALA-INFERENCJA.md) | prefill i dekodowanie, roofline na twoim rigu, uwaga i KV cache, MoE, batching, równoległość, spekulacja, próbkowanie, gramatyki, szablony, metodologia pomiarów, słowniczek | techniczny |
| 03 | [Kwantyzacja i formaty](03-KWANTYZACJA-I-FORMATY.md) | co jest w pliku GGUF bajt po bajcie; K-/i-kwanty, MXFP4, AWQ, GPTQ, FP8, oQ, Unsloth Dynamic; tabele jakości; analiza twojego pliku | techniczny |
| 04 | [llama.cpp i rodzina ggml](04-LLAMA-CPP-I-RODZINA-GGML.md) | ggml, GGUF, libllama, KV, `llama-server` od środka, spekulacja, tryby podziału na wiele GPU, HIP; ik_llama.cpp, llamafile, KoboldCpp, llama-swap | techniczny (najgłębszy) |
| 05 | [Opakowania](05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) | Ollama, LM Studio, llmman, Jan, GPT4All, LocalAI, Lemonade, Docker Model Runner, RamaLama; co się psuje, gdy sponsor zmieni zdanie | techniczny + rynkowy |
| 06 | [Silniki serwerowe](06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) | vLLM (PagedAttention, v1), SGLang (RadixAttention), TensorRT-LLM, TGI, Dynamo, llm-d; vLLM na twoim R9700 | techniczny |
| 07 | [Apple i ds4](07-APPLE-MLX-OMLX-I-DS4.md) | pamięć zunifikowana, MLX, mlx-lm, oMLX, ds4/DwarfStar, exo | techniczny |
| 08 | [Specjaliści](08-SPECJALISCI-KTRANSFORMERS-I-INNE.md) | KTransformers, mistral.rs, MLC/WebLLM, stosy NPU; hybrydowe MoE w porównaniu | techniczny |
| 09 | [Porównanie i wybór](09-POROWNANIE-I-WYBOR.md) | macierz, gfx1201, API/offline/telemetria, scenariusze, pomysły do pożyczenia, plan eksperymentów | praktyczny |
| 10 | [Pieniądze i ludzie](10-PIENIADZE-I-LUDZIE.md) | modele biznesowe, finansowanie, konsolidacja 2026, katalog osób, licencje, ryzyka zależności | **nietechniczny** |

## Dziesięć rzeczy, które mnie zaskoczyły (i dlaczego warto je znać)

1. **Prawie wszystkie „różne” programy do lokalnych modeli uruchamiają llama.cpp.** Ollama usunęła własny silnik GGUF w maju 2026 i uruchamia upstreamowy `llama-server` (rozdz. 05).
2. **llama.cpp urósł z silnika w platformę**: tryb routera z wymianą modeli (LRU), endpointy Anthropic i Responses, wbudowane narzędzia i klient MCP, a nawet aplikacje desktopowe (rozdz. 04).
3. **Tryb tensorowy w llama.cpp jest oficjalnie „eksperymentalny, bez gwarancji dla AMD”** — a na twoich 4×R9700 zadziałał i dał ~50 tok/s (rozdz. 04, 02 i [przewodnik o przyspieszaniu](../przyspieszanie-generowania/README.md)).
4. **Na twojej karcie (gfx1201) działa naprawdę jeden silnik: llama.cpp.** vLLM ma deklarowane wsparcie bez pomiarów, SGLang go nie ma, ds4 ma niezmergowane łatki, MLX i exo to tylko Mac (rozdz. 09).
5. **Dla MoE batchowanie nie jest „za darmo”**: przy 32 równoległych sekwencjach dotykasz ok. połowy ekspertów, więc spekulacja daje mniej niż na modelach gęstych (rozdz. 02; *moje wyliczenie*).
6. **Większość ruchu pamięci na token w twoim modelu to część gęsta, nie eksperci** — bity ekspertów kosztują pojemność, nie przepustowość (rozdz. 03).
7. **ds4 pokazuje drugą drogę: silnik jednego modelu z dyskiem jako warstwą pamięci** — 24 tys. gwiazdek w pięć miesięcy; na twoim sprzęcie jednak tylko z łatkami (rozdz. 07).
8. **Konsolidacja 2026**: ggml.ai w Hugging Face (2026-02-20), Qualcomm kupuje Modular, doniesienia o przejęciu HF przez NVIDIA *(prasa)*, TGI zarchiwizowane (rozdz. 10, 06).
9. **Dwa światy formatów**: GGUF (jeden plik, wiele kwantyzacji) kontra safetensors z kalibrowanymi kwantami; przejście między nimi nie jest darmowe (rozdz. 03).
10. **Największe ryzyko twojego stosu to nie szybkość, tylko ekspozycja**: `llama-swap` na wszystkich interfejsach bez hasła + modele z `--agent` (wbudowane wykonywanie poleceń) (rozdz. 09 i 04).

## Powiązane części repozytorium

- [Przyspieszanie generowania](../przyspieszanie-generowania/README.md) — moje własne pomiary i wdrożenie spekulacji + podziału tensorowego na rigu (23,5 → ~50 tok/s).
- [Asystenci AI](../asystenci-ai/README.md) i [Harnessy agentowe](../harnessy-agentowe/README.md) — warstwa *nad* silnikami: gdzie te silniki są używane.
- [Kurs lokalnych modeli](../kurs_lokalne_modele/) — podstawy, od których ten kurs zakłada, że zaczynasz.
