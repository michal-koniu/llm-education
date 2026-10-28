# Przyspieszanie generowania tokenów — speculative decoding i podział tensorowy na 4 kartach

**Stan na 19 października 2026.** Jak przyspieszyłem DeepSeek-V4-Flash z **23,5 do ~50 tok/s** (jeden agent) bez zmiany
modelu i jego wag — i jak zrobić to samo z każdym innym modelem, który pobiorę w przyszłości. Ten katalog jest
jednocześnie **lekcją** (jak to działa w środku) i **studium przypadku** (co dokładnie zrobiłem na rigu referencyjnym, co strojić).

> ⚠️ **Co tu jest zmierzone, a co nie.** Wszystko poniżej zmierzyłem na jednej maszynie (4× Radeon AI PRO R9700,
> ROCm, llama.cpp). **Szybkość** mierzyłem dokładnie. **Jakości po zmianie — czy model nie zgłupiał — NIE zmierzyłem**
> (sekcja [Jakość](#jakość-czy-model-nie-zgłupiał)). Tryb tensorowy jest w llama.cpp oznaczony jako eksperymentalny.

---

## Wynik w jednej tabeli

DeepSeek-V4-Flash-0731 (284 mld parametrów, MoE, 13 mld aktywnych), kwantyzacja UD-IQ3_XXS, 4 karty. Jeden agent, średnia z 4 rodzajów
zadań (tłumaczenie, wywołanie narzędzia, kod, proza) × 2 temperatury:

| Konfiguracja | tok/s (średnia) | wywołanie narzędzia (JSON) |
|---|---|---|
| początek dnia: stary llama.cpp, podział warstwami, bez draftu | **23,5** | 23,4 |
| + speculative decoding (DSpark, 3 tokeny) | 35,2 | 43 |
| nowy llama.cpp, podział warstwami, z draftem | 37,9 | 48–50 |
| nowy llama.cpp, **podział tensorowy**, z draftem — **wdrożone** | **49,2** | **54–62** |

A gdy działa kilku agentów naraz (wdrożona konfiguracja, 2 sloty):

| Agentów naraz | każdy | razem |
|---|---|---|
| 1 | 49,7 tok/s | 46 |
| 2 | 34,5 | **63** |
| 4 (2 sloty, reszta czeka w kolejce) | 33 | 60 |

Cena: **czytanie promptu (prefill) jest wolniejsze** — ~700 zamiast ~960 tok/s — i zostają **2 sloty po 98 304 tokeny**
kontekstu zamiast 4 po 131 072. Szczegóły i uzasadnienia: [02-WDROZENIE-DEEPSEEK.md](02-WDROZENIE-DEEPSEEK.md).

## Trzy dźwignie, które to dały

1. **Speculative decoding** (+50 %): mały „zgadywacz” proponuje 3 tokeny, duży model sprawdza je jednym przebiegiem.
   Zgadywacz to oficjalna głowica **DSpark** od DeepSeeka, ukryta w checkpoincie 0731; trzeba było ją skonwertować do GGUF.
2. **Podział tensorowy** (`--split-mode tensor`, +30 % na wierzchu): wszystkie 4 karty liczą każdy token równolegle, zamiast
   po kolei jak w potoku. Zrobiłem go na **zaktualizowanym llama.cpp** (o 499 commitów): nowy kod ma jawną obsługę stanów kompresowanej uwagi DeepSeek V4 w tym trybie. Na starej wersji trybu tensorowego nie próbowałem.
3. **Dopasowanie pamięci**: draft kosztuje ~4 GB na kartę, więc zmniejszyłem mikro-wsad (`--ubatch-size` 512) i liczbę slotów.

## Co jest w tym katalogu

| Plik | Po co |
|---|---|
| [01-JAK-TO-DZIALA.md](01-JAK-TO-DZIALA.md) | **Lekcja.** Dlaczego generowanie jest wolne, jak działa speculative decoding, czym różnią się jego odmiany, czym jest podział tensorowy |
| [02-WDROZENIE-DEEPSEEK.md](02-WDROZENIE-DEEPSEEK.md) | **Dziennik wdrożenia (studium przypadku).** Co zrobiłem krok po kroku, wszystkie pomiary, konfiguracja końcowa, co strojić, pułapki |
| [03-PROCEDURA-NOWY-MODEL.md](03-PROCEDURA-NOWY-MODEL.md) | **Instrukcja** dla kolejnych modeli: drzewo decyzyjne, polecenia, bramki, kryteria |
| [04-UZYTKOWANIE-UI-CLI-OPENCLAW.md](04-UZYTKOWANIE-UI-CLI-OPENCLAW.md) | Jak rozmawiać z szybkim modelem: przeglądarka, terminal, aplikacje agentowe (OpenClaw) |
| [05-ODNIESIENIE-LLAMA-CPP-SPECULATIVE.md](05-ODNIESIENIE-LLAMA-CPP-SPECULATIVE.md) | Dokumentacja llama.cpp o speculative decodingu **przetłumaczona na polski przez lokalny DeepSeek** (z opisem, jak ją zweryfikowałem) |
| [narzedzia/](narzedzia/README.md) | Skrypty: inspekcja GGUF, szukanie draftów, benchmarki, czat w terminalu, pętla pomiaru VRAM |

## Jakość: czy model nie zgłupiał?

**Nie zmierzyłem tego.** Co wiem, a czego nie:

- **Speculative decoding z założenia nie zmienia wyników** — duży model zatwierdza każdy token, więc rozkład odpowiedzi jest ten sam.
- **Podział tensorowy zmienia kolejność sumowania zmiennoprzecinkowego**, więc przy temperaturze 0 odpowiedzi nie są identyczne znak w znak z dawnymi
  (0 z 4 identycznych; z podziałem warstwami i draftem: 2 z 4). Odpowiedzi, które czytałem, były poprawne: tłumaczenie, kod, wywołanie narzędzia z poprawnym JSON.
- **Praktyczny test, nie benchmark:** wdrożona konfiguracja przetłumaczyła 24 KB dokumentacji EN→PL i 60 KB moich własnych dokumentów PL→EN. Struktura, kod, liczby i adresy
  wyszły poprawnie; zdarzyły się błędy rzeczowe (np. źle przełożony nagłówek) i tłumaczenie fragmentów kodu, którego miał nie ruszać — opisane w [05](05-ODNIESIENIE-LLAMA-CPP-SPECULATIVE.md).
  Model się nie rozpada, ale to nie jest pomiar jakości.
- **Benchmark jakości** (zestaw „hard”, 20 zadań po polsku i angielsku, k=3, 120 próbek; ten model miał 10 października wynik PL 92 / EN 93) uruchomiłem, ale **przerwałem po 11 próbkach**:
  pełny przebieg trwa kilka godzin, a 11 próbek nie pozwala wyciągnąć żadnego wniosku, więc ich nie publikuję.

**Zanim zbudujesz na tym agentów**, powtórz ten pomiar i porównaj z raportem z 10 października:
`python3 -m qbench run --model deepseek-v4-flash-0731 --suite hard --k 3` (kilka godzin; nie zmieniaj konfiguracji `llama-swap` w trakcie — zwolni model).
Jeśli wynik się pogorszy, przełącz klientów na bliźniaczy wpis `-nospec` albo wróć do podziału warstwami (zob. [03-PROCEDURA-NOWY-MODEL.md](03-PROCEDURA-NOWY-MODEL.md)).

## Powiązane części repozytorium

- Kurs 1, część 8 „Szybkość” — [prompt cache, speculative decoding, kwantyzacja, wiele kart](../kurs_lokalne_modele/08-OPTYMALIZACJA-OFFLINE.md): teoria; tutaj jest praktyka na konkretnym modelu.
- [Przegląd harnessów](../harnessy-agentowe/README.md) i [przegląd asystentów](../asystenci-ai/README.md) — OpenClaw i spółka, które będą korzystać z tego modelu.
