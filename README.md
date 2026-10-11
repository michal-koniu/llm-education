# llm-education

**Po polsku: dwa kursy o tym, jak naprawdę działają lokalne modele językowe i jak zbudować wokół nich agenta,
któremu można zaufać — oraz przegląd gotowych harnessów agentowych.**

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

### Kurs 1 — [od modelu do własnego agenta](kurs_lokalne_modele/00-KURS-INDEKS.md) (`kurs_lokalne_modele/`)

Po tym kursie potrafisz zbudować od zera własnego agenta, który czyta pliki, pisze kod, uruchamia polecenia,
widzi obrazy, słucha i mówi, pamięta kontekst i działa offline — i rozumiesz każdą warstwę pod nim.

| Część | Temat | Co budujesz |
|---|---|---|
| [01](kurs_lokalne_modele/PODSTAWY-LOKALNYCH-MODELI.md) | Podstawy | tokeny, wagi, runtime, serwer; `llama-cli`, `llama-server`, `curl` |
| [02](kurs_lokalne_modele/02-WNETRZE-MODELU.md) | Wnętrze modelu | tokenizer, logity, próbkowanie, KV-cache, embeddingi — policzone ręcznie |
| [03](kurs_lokalne_modele/03-KONTROLA-I-NIEZAWODNOSC.md) | Kontrola | szablon czatu, gramatyki GBNF, determinizm, harness ewaluacyjny |
| [04](kurs_lokalne_modele/04-PAMIEC-RAG-I-KONTEKST.md) | Pamięć (RAG) | baza wektorowa w sqlite od zera, chunking, BM25, reranking, cytowania |
| [05](kurs_lokalne_modele/05-MULTIMODALNOSC.md) | Zmysły | wizja, Whisper (słuch), Piper (mowa) + lista sprzętu |
| [06](kurs_lokalne_modele/06-PETLA-AGENTA-OD-ZERA.md) | **Pętla agenta** | narzędzia, edycja plików, powłoka, błędy, dziennik — serce kursu |
| [07](kurs_lokalne_modele/07-SANDBOX-BEZPIECZENSTWO-MONITORING.md) | Piaskownica | bwrap, limity, sieć, prompt injection, audyt, monitoring |
| [08](kurs_lokalne_modele/08-OPTYMALIZACJA-OFFLINE.md) | Szybkość | prompt cache, dekodowanie spekulatywne, kwantyzacja, wiele kart |
| [09](kurs_lokalne_modele/09-KRAJOBRAZ-NARZEDZI.md) | Katalog narzędzi | vLLM, Docling, promptfoo i inne — ocenione pod kątem tego sprzętu |
| [10](kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md) | Hybryda | granica prywatności, kiedy model w chmurze, offline-first |

### Kurs 2 — [aplikacje agentowe](kurs_aplikacje_agentowe/00-INDEKS.md) (`kurs_aplikacje_agentowe/`)

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

### Przegląd — [harnessy agentowe dla lokalnych modeli](harnessy-agentowe/README.md) (`harnessy-agentowe/`)

Kursy uczą budować od zera. Przegląd odpowiada na pytanie, **co już istnieje**: ranking 20 najlepszych otwartych
harnessów (z 72 sprawdzonych), które zamieniają lokalny model w agenta — czym się różnią, jaki problem każdy rozwiązuje
lepiej od konkurencji, jak podłączyć go do llama-swap i jak złożyć z nich aplikacje hybrydowe: Claude Opus jako planista,
lokalni agenci jako wykonawcy. Stan na 11 października 2026.

| Plik | Co w nim jest |
|---|---|
| [README](harnessy-agentowe/README.md) | ranking, porównanie techniczne, wybór do zastosowania, werdykt „budować czy brać gotowe" |
| [01-PROFILE](harnessy-agentowe/01-PROFILE.md) | 20 profili z konfiguracją lokalnego modelu i siedem pułapek wspólnych dla wszystkich |
| [02-KLOCKI](harnessy-agentowe/02-KLOCKI.md) | wyszukiwanie, monitoring cen, dane finansowe, powiadomienia, harmonogram, pamięć, głos, obraz |
| [03-ARCHITEKTURA](harnessy-agentowe/03-ARCHITEKTURA.md) | wzorzec planista–wykonawcy na 4× R9700, tryb w pełni lokalny, pięć gotowych układów, koszty |
| [ZRODLA](harnessy-agentowe/ZRODLA.md) | źródła z datą sprawdzenia i tym, co z nich wziąłem |

### Przegląd — [asystenci AI: 15 najlepszych](asystenci-ai/README.md) (`asystenci-ai/`)

Czego uczą najlepsze istniejące asystenty AI — codzienne, profesjonalne, autonomicznie wykonujące zadania i „żyjące"
w tle: otwarte i zamknięte, ich architektura, modele biznesowe, możliwość pracy offline i lekcje dla lokalnego asystenta
dla polskich profesjonalistów, którzy nie mogą wysyłać danych do USA. Stan na 11 października 2026.

| Plik | Co w nim jest |
|---|---|
| [README](asystenci-ai/README.md) | mapa rynku, piętnastka w tabeli, 10 lekcji, metoda wyboru |
| [01-PROFILE](asystenci-ai/01-PROFILE.md) | 15 profili po dziewięć obszarów i lista „warto znać" |
| [02-RYNEK](asystenci-ai/02-RYNEK.md) | modele biznesowe, cenniki, liczby, przejęcia, porażki, trendy 2026 |
| [03-WZORCE-TECHNICZNE](asystenci-ai/03-WZORCE-TECHNICZNE.md) | wzorce techniczne, macierz offline, architektura lokalnego asystenta na biurko |
| [04-POLSKA-I-SUWERENNOSC](asystenci-ai/04-POLSKA-I-SUWERENNOSC.md) | RODO, AI Act, tajemnice zawodowe, konkurencja w Polsce i UE, polskie modele, sprzęt, szanse |
| [ZRODLA](asystenci-ai/ZRODLA.md) | źródła z datą sprawdzenia |

---

## Jak zacząć

```bash
git clone https://github.com/michal-koniu/llm-education.git
cd llm-education
source rig-env.sh        # ustawia ścieżki kursów, modeli i llama.cpp
```

Potem otwórz [część 1 kursu 1](kurs_lokalne_modele/PODSTAWY-LOKALNYCH-MODELI.md). Każda lekcja zaczyna się od
`source rig-env.sh` w katalogu repozytorium — w poleceniach lekcji stoi moja ścieżka
(`~/Desktop/github_repos/llm-education`), u Ciebie może być inna.

**Dostosuj `rig-env.sh` do swojej maszyny:** ścieżki do modeli (`$M`, `$BIELIK`, …), do llama.cpp (`$LB`)
i widoczne karty (`HIP_VISIBLE_DEVICES`).

## Gdzie powstają pliki

Wszystko, co tworzą kursy, powstaje **wewnątrz repozytorium**, w katalogach ignorowanych przez git:

| Zmienna | Katalog | Co tam trafia |
|---|---|---|
| `$KURS` | `kurs_lokalne_modele/praca/` | skrypty, bazy, ewaluacje, gramatyki z kursu 1 |
| `$AGENT` | `kurs_lokalne_modele/praca/agent/` | agent budowany od części 6 |
| `$OSA` | `kurs_aplikacje_agentowe/praca/os-agenta/` | system z kursu 2 (z własnym repozytorium git) |
| `$VENVS` | `.venvs/` | środowiska Pythona używane w lekcjach |
| `$NARZEDZIA` | `narzedzia/` | whisper.cpp i piper z części 5 |

**Świadome wyjątki** — tych rzeczy nie trzyma się w katalogu projektu:

- **modele** (`~/models`) i **llama.cpp** (`~/llama.cpp`) — duże, wspólne z innymi narzędziami na maszynie;
- **jednostki systemd** (`~/.config/systemd/user/`) — systemd czyta je tylko stamtąd; `init.sh` generuje je
  z pełną ścieżką projektu;
- **sekrety** (`~/.config/osa/sekrety.json`, prawa 0600) — sekretów nie trzyma się w repozytorium,
  nawet ignorowanym;
- **gniazdo** (`~/.local/run/osa.sock`) — ścieżka gniazda ma limit 108 znaków;
- **Twoje dane**, na których pracują agenci (`~/dokumenty`, `~/skany`) — to Twoje pliki, nie wytwory kursu.

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

Treść lekcji: **CC BY 4.0** — możesz kopiować, zmieniać i wykorzystywać, także komercyjnie, podając autora.
Kod (fragmenty w lekcjach, `rig-env.sh`, `szkielet/`): **MIT**. Szczegóły: [LICENSE.md](LICENSE.md).

Znalazłeś błąd albo Twój pomiar mówi co innego niż lekcja? Otwórz zgłoszenie (issue) — właśnie po to
lekcje mają tabele na pomiary.
