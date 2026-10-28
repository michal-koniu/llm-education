# llm-education

English version: [README.md](README.md)

**Po polsku: dwa kursy o tym, jak naprawdę działają lokalne modele językowe i jak zbudować wokół nich agenta,
któremu można zaufać — oraz przegląd gotowych harnessów agentowych.**

> **Struktura:** treść po polsku jest w [`pl/`](pl/), wersja angielska w [`en/`](en/).

![Język: polski](https://img.shields.io/badge/język-polski-red)
![Kurs 1: 10 części, ~47 h](https://img.shields.io/badge/kurs%201-10%20części%20·%20~47%20h-blue)
![Kurs 2: 19 części, ~102 h](https://img.shields.io/badge/kurs%202-19%20części%20·%20~102%20h-blue)
![Przegląd: 20 harnessów agentowych](https://img.shields.io/badge/przegląd-20%20harnessów%20agentowych-orange)
![Przegląd: 15 asystentów AI](https://img.shields.io/badge/przegląd-15%20asystentów%20AI-orange)
![Licencja: CC BY 4.0 + MIT](https://img.shields.io/badge/licencja-CC%20BY%204.0%20%2B%20MIT-lightgrey)

Bez frameworków na start i bez magii. Każdy mechanizm budujesz sam, od zera, na modelach uruchomionych
**na własnym komputerze**: tokenizer, próbkowanie, gramatyki, bazę wektorową, pętlę agenta, piaskownicę,
harmonogram, ewaluację. Dopiero gdy rozumiesz, co robi biblioteka, świadomie wybierasz gotowe narzędzia.

Kursy powstały jako mój własny plan nauki na domowej maszynie z kartami AMD Radeon AI PRO R9700
(ROCm + [llama.cpp](https://github.com/ggml-org/llama.cpp)). Udostępniam je w nadziei, że przydadzą się
innym osobom uczącym się po polsku.

---

## Co jest w środku

### Kurs 1 — [od modelu do własnego agenta](pl/kurs_lokalne_modele/00-KURS-INDEKS.md) (`pl/kurs_lokalne_modele/`)

Po tym kursie potrafisz zbudować od zera własnego agenta, który czyta pliki, pisze kod, uruchamia polecenia,
widzi obrazy, słucha i mówi, pamięta kontekst i działa offline — i rozumiesz każdą warstwę pod nim.

| Część | Temat | Co budujesz |
|---|---|---|
| [01](pl/kurs_lokalne_modele/PODSTAWY-LOKALNYCH-MODELI.md) | Podstawy | tokeny, wagi, runtime, serwer; `llama-cli`, `llama-server`, `curl` |
| [02](pl/kurs_lokalne_modele/02-WNETRZE-MODELU.md) | Wnętrze modelu | tokenizer, logity, próbkowanie, KV-cache, embeddingi — policzone ręcznie |
| [03](pl/kurs_lokalne_modele/03-KONTROLA-I-NIEZAWODNOSC.md) | Kontrola | szablon czatu, gramatyki GBNF, determinizm, harness ewaluacyjny |
| [04](pl/kurs_lokalne_modele/04-PAMIEC-RAG-I-KONTEKST.md) | Pamięć (RAG) | baza wektorowa w sqlite od zera, chunking, BM25, reranking, cytowania |
| [05](pl/kurs_lokalne_modele/05-MULTIMODALNOSC.md) | Zmysły | wizja, Whisper (słuch), Piper (mowa) + lista sprzętu |
| [06](pl/kurs_lokalne_modele/06-PETLA-AGENTA-OD-ZERA.md) | **Pętla agenta** | narzędzia, edycja plików, powłoka, błędy, dziennik — serce kursu |
| [07](pl/kurs_lokalne_modele/07-SANDBOX-BEZPIECZENSTWO-MONITORING.md) | Piaskownica | bwrap, limity, sieć, prompt injection, audyt, monitoring |
| [08](pl/kurs_lokalne_modele/08-OPTYMALIZACJA-OFFLINE.md) | Szybkość | prompt cache, dekodowanie spekulatywne, kwantyzacja, wiele kart |
| [09](pl/kurs_lokalne_modele/09-KRAJOBRAZ-NARZEDZI.md) | Katalog narzędzi | vLLM, Docling, promptfoo i inne — ocenione pod kątem tego sprzętu |
| [10](pl/kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md) | Hybryda | granica prywatności, kiedy model w chmurze, offline-first |

### Kurs 2 — [aplikacje agentowe](pl/kurs_aplikacje_agentowe/00-INDEKS.md) (`pl/kurs_aplikacje_agentowe/`)

Kurs 1 uczy, **jak działa model**. Kurs 2 uczy, **jak zbudować wokół niego system, któremu można zaufać**.
Budujesz jeden rosnący system i stawiasz na nim trzech agentów osobistych, którzy działają tygodniami,
budzą się sami, pamiętają, są mierzeni i nie mogą zrobić Ci krzywdy:
**Archiwista** (dokumenty lokalne, bez sieci), **Badacz** (sieć, ścisła piaskownica) i **Gospodarz**
(kalendarz i przypomnienia).

| Blok | Części | Tematy |
|---|---|---|
| Fundament | 01–03 | architektury agentowe, brama i konfiguracja, **harness długich zadań** |
| Kontekst i pamięć | 04–06 | budżet uwagi, pamięć bi-temporalna, tożsamość w plikach |
| Działanie | 07–10 | ergonomia narzędzi, **code-mode**, MCP / CLI / A2A, piaskownica produkcyjna |
| Proaktywność | 11–13 | harmonogram, kanały, flota wielu agentów |
| Jakość i zaufanie | 14–16 | **ewaluacja**, obserwowalność (OTel), bezpieczeństwo (OWASP ASI) |
| Produkcja | 17–19 | router hybrydowy, wydania i utrzymanie, projekt końcowy |

⚠️ **Kurs 2 zaczynaj dopiero po części 6 kursu 1** — cały stoi na pętli agenta, którą tam budujesz.

### Przegląd — [harnessy agentowe dla lokalnych modeli](pl/harnessy-agentowe/README.md) (`pl/harnessy-agentowe/`)

Kursy uczą budować od zera. Przegląd odpowiada na pytanie, **co już istnieje**: ranking 20 najlepszych otwartych
harnessów (z 72 sprawdzonych), które zamieniają lokalny model w agenta — czym się różnią, jaki problem każdy rozwiązuje
lepiej od konkurencji, jak podłączyć go do llama-swap i jak złożyć z nich aplikacje hybrydowe: Claude Opus jako planista,
lokalni agenci jako wykonawcy. Stan na 11 października 2026.

| Plik | Co w nim jest |
|---|---|
| [README](pl/harnessy-agentowe/README.md) | ranking, porównanie techniczne, wybór do zastosowania, werdykt „budować czy brać gotowe" |
| [01-PROFILE](pl/harnessy-agentowe/01-PROFILE.md) | 20 profili z konfiguracją lokalnego modelu i siedem pułapek wspólnych dla wszystkich |
| [02-KLOCKI](pl/harnessy-agentowe/02-KLOCKI.md) | wyszukiwanie, monitoring cen, dane finansowe, powiadomienia, harmonogram, pamięć, głos, obraz |
| [03-ARCHITEKTURA](pl/harnessy-agentowe/03-ARCHITEKTURA.md) | wzorzec planista–wykonawcy na 4× R9700, tryb w pełni lokalny, pięć gotowych układów, koszty |
| [ZRODLA](pl/harnessy-agentowe/ZRODLA.md) | źródła z datą sprawdzenia i tym, co z nich wziąłem |

### Przegląd — [asystenci AI: 15 najlepszych](pl/asystenci-ai/README.md) (`pl/asystenci-ai/`)

Czego uczą najlepsze istniejące asystenty AI — codzienne, profesjonalne, autonomicznie wykonujące zadania i „żyjące"
w tle: otwarte i zamknięte, ich architektura, modele biznesowe, możliwość pracy offline i lekcje dla lokalnego asystenta
dla polskich profesjonalistów, którzy nie mogą wysyłać danych do USA. Stan na 11 października 2026.

| Plik | Co w nim jest |
|---|---|
| [README](pl/asystenci-ai/README.md) | mapa rynku, piętnastka w tabeli, 10 lekcji, metoda wyboru |
| [01-PROFILE](pl/asystenci-ai/01-PROFILE.md) | 15 profili po dziewięć obszarów i lista „warto znać" |
| [02-RYNEK](pl/asystenci-ai/02-RYNEK.md) | modele biznesowe, cenniki, liczby, przejęcia, porażki, trendy 2026 |
| [03-WZORCE-TECHNICZNE](pl/asystenci-ai/03-WZORCE-TECHNICZNE.md) | wzorce techniczne, macierz offline, architektura lokalnego asystenta na biurko |
| [04-POLSKA-I-SUWERENNOSC](pl/asystenci-ai/04-POLSKA-I-SUWERENNOSC.md) | RODO, AI Act, tajemnice zawodowe, konkurencja w Polsce i UE, polskie modele, sprzęt, szanse |
| [ZRODLA](pl/asystenci-ai/ZRODLA.md) | źródła z datą sprawdzenia |

### Praktyka — [przyspieszanie generowania tokenów](pl/przyspieszanie-generowania/README.md) (`pl/przyspieszanie-generowania/`)

Jak przyspieszyłem DeepSeek-V4-Flash z 23,5 do ok. 50 tok/s dla jednego agenta na 4× R9700, nie ruszając modelu: **speculative decoding** z własną głowicą draftu modelu
oraz **podział tensorowy** na czterech kartach — i procedura, jak zrobić to samo z każdym modelem, który pobiorę w przyszłości. Zmierzone, z porażkami włącznie.
Stan na 19 października 2026.

| Plik | Co w nim jest |
|---|---|
| [README](pl/przyspieszanie-generowania/README.md) | wynik w jednej tabeli, trzy dźwignie, co jest zmierzone, a co nie |
| [01-JAK-TO-DZIALA](pl/przyspieszanie-generowania/01-JAK-TO-DZIALA.md) | lekcja: dlaczego generowanie jest wolne, jak działa speculative decoding i podział tensorowy, odmiany |
| [02-WDROZENIE-DEEPSEEK](pl/przyspieszanie-generowania/02-WDROZENIE-DEEPSEEK.md) | studium przypadku: każdy krok, każdy pomiar, konfiguracja końcowa, pułapki |
| [03-PROCEDURA-NOWY-MODEL](pl/przyspieszanie-generowania/03-PROCEDURA-NOWY-MODEL.md) | instrukcja dla kolejnego modelu: drzewo decyzyjne, polecenia, bramki, kryteria |
| [04-UZYTKOWANIE-UI-CLI-OPENCLAW](pl/przyspieszanie-generowania/04-UZYTKOWANIE-UI-CLI-OPENCLAW.md) | rozmowa z szybkim modelem: przeglądarka, terminal, aplikacje agentowe |
| [05-ODNIESIENIE-LLAMA-CPP-SPECULATIVE](pl/przyspieszanie-generowania/05-ODNIESIENIE-LLAMA-CPP-SPECULATIVE.md) | dokumentacja llama.cpp po polsku — przekład wykonany lokalnym DeepSeekiem, ze zweryfikowanymi poprawkami |
| [narzedzia/](pl/przyspieszanie-generowania/narzedzia/README.md) | skrypty: inspekcja GGUF, szukanie draftów, benchmarki, czat w terminalu |

### Przegląd — [silniki lokalnych LLM: od mapy do kodu źródłowego](pl/silniki-lokalnych-llm/README.md) (`pl/silniki-lokalnych-llm/`)

Czym są llama.cpp, Ollama, LM Studio, vLLM, SGLang, MLX i oMLX, ds4, llmman i kilkanaście innych programów do uruchamiania modeli na własnym sprzęcie, co robią w środku,
do czego służą i czym się różnią — od mapy rynku po struktury danych w kodzie. Plus jeden rozdział nietechniczny: jak zarabiają i kto za nimi stoi.
Research biurkowy i lektura kodu, bez własnych pomiarów. Stan na 19 października 2026.

| Plik | Co w nim jest |
|---|---|
| [README](pl/silniki-lokalnych-llm/README.md) | mapa kursu, dziesięć niespodzianek, jak czytać |
| [01-MAPA-I-WARSTWY](pl/silniki-lokalnych-llm/01-MAPA-I-WARSTWY.md) | siedem warstw od pliku z wagami do okna czatu, tabele projektów, sieć zależności, oś czasu |
| [02-JAK-DZIALA-INFERENCJA](pl/silniki-lokalnych-llm/02-JAK-DZIALA-INFERENCJA.md) | prefill i dekodowanie, KV cache, MoE, batching, równoległość, spekulacja, próbkowanie, słowniczek |
| [03-KWANTYZACJA-I-FORMATY](pl/silniki-lokalnych-llm/03-KWANTYZACJA-I-FORMATY.md) | co jest w pliku GGUF, rodziny kwantyzacji, tabele jakości, analiza pliku DeepSeek |
| [04-LLAMA-CPP-I-RODZINA-GGML](pl/silniki-lokalnych-llm/04-LLAMA-CPP-I-RODZINA-GGML.md) | ggml, GGUF, `llama-server` od środka, tryby podziału na wiele GPU, HIP; ik_llama.cpp, llamafile, llama-swap |
| [05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE](pl/silniki-lokalnych-llm/05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md) | Ollama, LM Studio, llmman, Jan, LocalAI, Lemonade, Docker Model Runner, RamaLama |
| [06-SILNIKI-SERWEROWE-VLLM-SGLANG](pl/silniki-lokalnych-llm/06-SILNIKI-SERWEROWE-VLLM-SGLANG.md) | vLLM, SGLang, TensorRT-LLM, TGI; status na AMD gfx1201 |
| [07-APPLE-MLX-OMLX-I-DS4](pl/silniki-lokalnych-llm/07-APPLE-MLX-OMLX-I-DS4.md) | pamięć zunifikowana, MLX, mlx-lm, oMLX, ds4, exo |
| [08-SPECJALISCI-KTRANSFORMERS-I-INNE](pl/silniki-lokalnych-llm/08-SPECJALISCI-KTRANSFORMERS-I-INNE.md) | KTransformers, mistral.rs, MLC, stosy NPU |
| [09-POROWNANIE-I-WYBOR](pl/silniki-lokalnych-llm/09-POROWNANIE-I-WYBOR.md) | macierz, scenariusze, co działa na gfx1201, eksperymenty |
| [10-PIENIADZE-I-LUDZIE](pl/silniki-lokalnych-llm/10-PIENIADZE-I-LUDZIE.md) | **nietechniczny:** modele biznesowe, finansowanie, ludzie, licencje, ryzyka |
| [ZRODLA](pl/silniki-lokalnych-llm/ZRODLA.md) | źródła, przypięte commity, najsłabiej zweryfikowane punkty |

### Przegląd — [tanie i darmowe modele online dla agentów](pl/tanie-i-darmowe-modele/README.md) (`pl/tanie-i-darmowe-modele/`)

Trzecia noga obok czołowych API i modeli lokalnych: gdzie zdobyć inferencję online za niewielkie pieniądze albo za darmo
na modelach co najmniej tak mądrych jak lokalny DeepSeek-V4-Flash i na ile można jej ufać w pętli agenta. 20 najlepszych
tras, które modele naprawdę przekraczają poprzeczkę i jak podłączyć je do aplikacji agentowych. Stan na 13 października 2026.

| Plik | Co w nim jest |
|---|---|
| [README](pl/tanie-i-darmowe-modele/README.md) | krótka odpowiedź, ranking 20 tras, punktacja, która trasa do jakiego zadania |
| [01-PROFILE](pl/tanie-i-darmowe-modele/01-PROFILE.md) | 20 profili: ceny, limity, warunki, jak wywołać każdą trasę |
| [02-MODELE](pl/tanie-i-darmowe-modele/02-MODELE.md) | które modele są naprawdę co najmniej tak mądre jak DeepSeek-V4-Flash, na jednej wersji indeksu |
| [03-UZYCIE-W-AGENTACH](pl/tanie-i-darmowe-modele/03-UZYCIE-W-AGENTACH.md) | konfiguracja routera LiteLLM, limity darmowych planów, rachunek kosztów, pułapki jakości, 15-minutowy test akceptacyjny |
| [ZRODLA](pl/tanie-i-darmowe-modele/ZRODLA.md) | źródła z datą sprawdzenia |

### Przegląd — [asymetrie zarobkowe z AI](pl/asymetrie-zarobkowe-ai/README.md) (`pl/asymetrie-zarobkowe-ai/`)

Gdzie aplikacja agentowa na konfiguracji hybrydowej może zarabiać online bez zakładania firmy: 22 kandydatów (bounty,
konkursy, rynki predykcyjne, arbitraż, płatna praca ręczna, wynajem mocy obliczeniowej i inne), każdy sprawdzony pod
kątem tego, czy wciąż płaci się za ręczną pracę, którą agenty mogą dziś wykonać szybciej. Legalność i podatki sprawdzone
dla polskiego rezydenta. Stan na 14 października 2026.

| Plik | Co w nim jest |
|---|---|
| [README](pl/asymetrie-zarobkowe-ai/README.md) | krótka odpowiedź, 10 najlepszych, punktacja, od czego zacząć, odrzuceni kandydaci |
| [01-OKAZJE](pl/asymetrie-zarobkowe-ai/01-OKAZJE.md) | 10 najlepszych okazji, profil po profilu |
| [02-ARCHITEKTURA-HYBRYDOWA](pl/asymetrie-zarobkowe-ai/02-ARCHITEKTURA-HYBRYDOWA.md) | jeden wzorzec agenta hybrydowego: routing lokalnie czy płatnie, rachunek kosztów, zabezpieczenia |
| [03-ZASADY-PODATKI-RYZYKA](pl/asymetrie-zarobkowe-ai/03-ZASADY-PODATKI-RYZYKA.md) | polskie podatki, raportowanie, zasady hazardu i pracy security, regulaminy platform, ryzyka operacyjne |
| [ZRODLA](pl/asymetrie-zarobkowe-ai/ZRODLA.md) | źródła z datą sprawdzenia |

### Przegląd — [asymetrie biznesowe AI](pl/asymetrie-biznesowe-ai/README.md) (`pl/asymetrie-biznesowe-ai/`)

Gdzie adopcja AI jest wciąż na tyle niska, że mały zespół z aplikacjami agentowymi i lokalnymi otwartymi modelami może
zbudować biznes, zanim dogonią go obecni gracze: 26 kandydatów w Polsce, w UE i na rynkach globalnych, każdy przed
oceną zaatakowany z pięciu stron. Stan na 14 października 2026.

| Plik | Co w nim jest |
|---|---|
| [README](pl/asymetrie-biznesowe-ai/README.md) | krótka odpowiedź, 15 najlepszych, punktacja, kontrargumenty, od czego zacząć |
| [01-LUKI-ADOPCJI](pl/asymetrie-biznesowe-ai/01-LUKI-ADOPCJI.md) | gdzie adopcja AI jest wciąż niska: dane Eurostatu i GUS według kraju, wielkości i sektora |
| [02-OKAZJE](pl/asymetrie-biznesowe-ai/02-OKAZJE.md) | 15 najlepszych okazji, profil po profilu |
| [03-NAJPIERW-LOKALNIE](pl/asymetrie-biznesowe-ai/03-NAJPIERW-LOKALNIE.md) | dlaczego kupujący chcą lokalnie, wystarczające otwarte modele, klasy sprzętu, koszt lokalnie vs API |
| [ZRODLA](pl/asymetrie-biznesowe-ai/ZRODLA.md) | źródła z datą sprawdzenia |

### Ścieżka biznesowa — [wycena prywatnego AI boxa](pl/kurs_wycena_ai_box/00-INDEKS.md) (`pl/kurs_wycena_ai_box/`)

Cennik lokalnego AI boxa dla polskich kancelarii i biur, w którym każda liczba ma źródło: podłoga kosztowa, sufit
wartości dla kancelarii, katalog agentów eksperckich jako silnik wzrostu, cztery modele sprzętowe i Twoja gotówka,
rozmowy o gotowości do zapłaty po polsku i to, jak cennik wygląda w oczach inwestora. Z kalkulatorem w samej
bibliotece standardowej (`floor`, `value`, `cash`, `vw`, `gg`, `nrr`). Stan na 25 października 2026.

| Część | Temat | Co powstaje |
|---|---|---|
| [01](pl/kurs_wycena_ai_box/01-PODSTAWY-WYCENY.md) | Podstawy | cena „z brzucha” zapisana z góry, trzy kotwice |
| [02](pl/kurs_wycena_ai_box/02-PODLOGA-KOSZTOWA.md) | Podłoga kosztowa | COGS na jedno biuro, docelowa marża |
| [03](pl/kurs_wycena_ai_box/03-SUFIT-WARTOSCI.md) | Sufit wartości | wartość ekonomiczna dla trzech biur, pierwszy klient docelowy |
| [04](pl/kurs_wycena_ai_box/04-METRYKA-WARTOSCI-I-PAKIETY.md) | Metryka wartości | katalog agentów, pakiety dobry / lepszy / najlepszy |
| [05](pl/kurs_wycena_ai_box/05-SPRZET-I-GOTOWKA.md) | Sprzęt i gotówka | model sprzętowy i Twoje zapotrzebowanie na gotówkę |
| [06](pl/kurs_wycena_ai_box/06-GOTOWOSC-DO-ZAPLATY.md) | Gotowość do zapłaty | zestaw do wywiadów, Van Westendorp, płatny pilotaż |
| [07](pl/kurs_wycena_ai_box/07-CENNIK-I-WARUNKI.md) | Cennik | `price-book-v1.md` z rabatami i warunkami |
| [08](pl/kurs_wycena_ai_box/08-WYCENA-POD-SKALE-I-INWESTOROW.md) | Skala | ARR, NRR i decyzja: bootstrapping czy VC |

---

## Jak zacząć

```bash
git clone https://github.com/michal-koniu/llm-education.git
cd llm-education
source rig-env.sh        # ustawia ścieżki kursów, modeli i llama.cpp
```

Potem otwórz [część 1 kursu 1](pl/kurs_lokalne_modele/PODSTAWY-LOKALNYCH-MODELI.md). Każda lekcja zaczyna się od
`source rig-env.sh` w katalogu repozytorium — polecenia lekcji zakładają, że repozytorium leży w `~/llm-education`;
jeśli u Ciebie jest gdzie indziej, dostosuj ścieżkę.

**Dostosuj `rig-env.sh` do swojej maszyny:** ścieżki do modeli (`$M`, `$BIELIK`, …), do llama.cpp (`$LB`)
i widoczne karty (`HIP_VISIBLE_DEVICES`). To szablon: zmień wartości domyślne na górze pliku albo ustaw te zmienne
w powłoce przed `source rig-env.sh`.

## Gdzie powstają pliki

Wszystko, co tworzą kursy, powstaje **wewnątrz repozytorium**, w katalogach ignorowanych przez git:

| Zmienna | Katalog | Co tam trafia |
|---|---|---|
| `$KURS` | `pl/kurs_lokalne_modele/praca/` | skrypty, bazy, ewaluacje, gramatyki z kursu 1 |
| `$AGENT` | `pl/kurs_lokalne_modele/praca/agent/` | agent budowany od części 6 |
| `$OSA` | `pl/kurs_aplikacje_agentowe/praca/os-agenta/` | system z kursu 2 (z własnym repozytorium git) |
| `$VENVS` | `.venvs/` | środowiska Pythona używane w lekcjach |
| `$NARZEDZIA` | `narzedzia/` | whisper.cpp i piper z części 5 |

**Świadome wyjątki** — tych rzeczy nie trzyma się w katalogu projektu:

- **modele** (`~/models`) i **llama.cpp** (`~/llama.cpp`) — duże, wspólne z innymi narzędziami na maszynie;
- **jednostki systemd** (`~/.config/systemd/user/`) — systemd czyta je tylko stamtąd; `init.sh` generuje je
  z pełną ścieżką projektu;
- **sekrety** (`~/.config/osa/sekrety.json`, prawa 0600) — sekretów nie trzyma się w repozytorium,
  nawet ignorowanym;
- **gniazdo** (`~/.local/run/osa.sock`) — ścieżka gniazda ma limit 108 znaków;
- **Twoje dane**, na których pracują agenci (`~/dokumenty`, `~/skany`) — to Twoje pliki, nie wytwory kursu;
- **folder roboczy ścieżki biznesowej** (`~/founder/`) — notatki o cenach i dane prawdziwych klientów są prywatne
  i nie trafiają do publicznego repozytorium.

## Sprzęt i oprogramowanie

- Kursy pisane i sprawdzane na: Ubuntu 24.04, ROCm, llama.cpp (+ llama-swap), karty AMD Radeon AI PRO R9700.
- Większość ćwiczeń wymaga karty z **co najmniej 16 GB VRAM** (Bielik 11B w Q8, gpt-oss-20b). Części o wielu
  kartach i dużych modelach (np. 8) — odpowiednio więcej.
- Inne karty (NVIDIA, Apple Silicon) zadziałają tam, gdzie działa llama.cpp — zmienisz `rig-env.sh`
  i zignorujesz uwagi specyficzne dla ROCm.
- Python 3.12, `sqlite3`, `bwrap` (części o piaskownicy).

## Jak czytać lekcje

- **Pułapki** mają numery (`P4`, `P29`, …) — to błędy, które naprawdę wystąpiły na tej maszynie, z objawem
  i naprawą. Indeksy kursów zbierają je w jednym miejscu.
- **Eksperymenty** mają pustą tabelę na Twój pomiar i moją predykcję. Gdy się rozjadą, **Twój pomiar
  wygrywa** — popraw kurs.
- Liczby w lekcjach pochodzą z mojej maszyny; Twoje będą inne. Ważny jest kierunek i rząd wielkości.

## Powiązane repozytoria

| Repozytorium | Co to jest |
|---|---|
| [local-llm-perf-bench](https://github.com/michal-koniu/local-llm-perf-bench) | pomiar szybkości modeli w llama.cpp |
| [local-llm-quality-bench](https://github.com/michal-koniu/local-llm-quality-bench) | pomiar jakości modeli jako agentów, po polsku i angielsku |
| [local-llm-bench-results](https://github.com/michal-koniu/local-llm-bench-results) | wyniki obu benchmarków z tej maszyny |
| [radeon-r9700-rocm-notes](https://github.com/michal-koniu/radeon-r9700-rocm-notes) | notatki o sprzęcie: 4× R9700 + ROCm |

## Licencja

Licencja obejmuje całe repozytorium: cała treść (lekcje, przeglądy, poradniki - każdy plik `*.md`, w obu językach) na
**CC BY 4.0** — możesz kopiować, zmieniać i wykorzystywać, także komercyjnie, podając autora. Cały kod (skrypty,
`rig-env.sh`, `szkielet/`, `narzedzia/`, `tools/`, fragmenty w lekcjach): **MIT**. Szczegóły: [LICENSE.md](LICENSE.md).

Znalazłeś błąd albo Twój pomiar mówi co innego niż lekcja? Otwórz zgłoszenie (issue) — właśnie po to
lekcje mają tabele na pomiary.
