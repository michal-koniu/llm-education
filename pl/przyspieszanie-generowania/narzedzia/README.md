# Narzędzia

Skrypty, których użyłem do wdrożenia opisanego w [02-WDROZENIE-DEEPSEEK.md](../02-WDROZENIE-DEEPSEEK.md). Wszystkie przeszły przez moją maszynę (4× Radeon AI PRO R9700,
llama.cpp + `llama-swap`); to **szablony**, nie gotowy produkt — zanim ich użyjesz, dostosuj ścieżki.

**Ustawienie ścieżek.** W skryptach katalog domowy jest zapisany jako `/home/USER`; zamień go na swój i ustaw, gdzie leży `llama-swap`/`config.yaml`:

```bash
cd narzedzia && sed -i "s#/home/USER#$HOME#g" *.py *.sh        # macOS: sed -i '' ...
```

Skrypty zakładają: `llama-swap` na `localhost:8080` (zmienna `LLAMA_SWAP_URL` dla `dschat.py`), `llama.cpp` w `~/llama.cpp`, modele w `~/models/`, środowisko Pythona
dla konwertera w `~/spec-dspark/venv` (patrz [02, sekcja 2](../02-WDROZENIE-DEEPSEEK.md)).

| Skrypt | Do czego | Przykład |
|---|---|---|
| `gguf-inspect.py` | czy GGUF ma głowicę MTP/NextN; czym jest plik (model czy draft); czyta tylko nagłówki, więc działa w sekundy | `~/spec-dspark/venv/bin/python gguf-inspect.py model-00001-of-0000N.gguf` |
| `find-drafts.sh` | szuka na Hugging Face gotowych draftów (MTP, EAGLE-3, DFlash, DSpark, „speculator”) dla danego modelu | `./find-drafts.sh Qwen3-30B-A3B` |
| `convert-draft-from-hf.sh` | szablon konwersji draftu z checkpointu HF do GGUF (tu: DSpark DeepSeeka, `--remote` pobiera tylko potrzebne pliki) | edytuj nazwę repo i flagę |
| `bench_spec.py` | **prędkość jednego strumienia**: 4 rodzaje zadań × temp. 0 i 1,0; tok/s i akceptacja z liczników serwera | `BENCH_REPS=2 python3 bench_spec.py NAZWA wynik.json` |
| `bench_conc.py` | 1, 2 i 4 agentów naraz: tok/s na strumień i łącznie | `python3 bench_conc.py NAZWA wynik.json` |
| `try-entries.py` | dopisuje **tymczasowe** wpisy do `config.yaml`, każdy ładuje, odpala `bench_spec.py`, mierzy wolny VRAM, na końcu przywraca konfigurację | edytuj słownik `E` albo zmienną `ENTRIES` |
| `vram-try.py` | j.w., ale tylko ładowanie i pomiar wolnego VRAM dla wielu wariantów pamięci (ubatch, kontekst, sloty) | edytuj słownik `V` |
| `gate-test.py` | **bramka przed wdrożeniem**: prefill, 1/2/4 agentów, wolny VRAM po użyciu, zgodność z modelem bez draftu | edytuj stałe na górze |
| `build-llama-cpp.sh` | budowa llama.cpp w **osobnym katalogu** z pinem pełnego SHA | edytuj SHA |
| `dschat.py` | czat w terminalu z licznikiem tok/s ([04](../04-UZYTKOWANIE-UI-CLI-OPENCLAW.md)) | `python3 dschat.py "pytanie"` |
| `translate_doc.py` | tłumaczy dokument Markdown lokalnym modelem, sekcja po sekcji | `python3 translate_doc.py zrodlo.md wynik.md deepseek` |
| `verify_translation.py` | mechaniczna weryfikacja przekładu: bloki kodu, URL-e, flagi, liczby, nagłówki, tabele, nieprzetłumaczone zdania | `python3 verify_translation.py en.md pl.md` |

**Uwagi.** `try-entries.py`, `vram-try.py` i `gate-test.py` **modyfikują `config.yaml`** (przywracają go w bloku `finally`) — a każdy zapis konfiguracji zwalnia załadowany model w `llama-swap`.
Nie uruchamiaj ich, gdy ktoś z modelu korzysta albo gdy trwa długi test. Skrypty `bench_*` tylko wysyłają zapytania.
