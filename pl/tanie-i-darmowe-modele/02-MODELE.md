# Które modele są naprawdę co najmniej tak mądre jak DeepSeek-V4-Flash (październik 2026)

Ten plik dotyczy **modeli, nie dostawców**. Pytanie jest proste: mój lokalny sprzęt uruchamia DeepSeek-V4-Flash-0731. Które
modele dostępne tanio lub za darmo online są co najmniej tak samo mądre, a które „darmowe” oferty tylko wyglądają na
ulepszenie? Szczegóły dostawców (rejestracja, limity, warunki danych) są w [01-PROFILE.md](01-PROFILE.md). Jak podłączyć modele
do agenta, opisuje [03-UZYCIE-W-AGENTACH.md](03-UZYCIE-W-AGENTACH.md).

**AA** w tym pliku oznacza **Artificial Analysis Intelligence Index v4.3.2, stan na 13.10.2026** (pomiar
niezależny). **Vals** to niezależny harness Vals.ai, który puszcza każdy model przez tę samą konfigurację. Liczby
od twórców modeli są oznaczone *(deklaracja producenta)*. Ceny są w USD za 1M tokenów (wejście / wyjście), według stanu z 13.10.2026.

## 1. Najkrótsza odpowiedź

- **Poprzeczka to AA 34**, wynik DeepSeek-V4-Flash-0731 przy maksymalnym wysiłku. Poprzeczka dla trudnych agentów terminalowych to
  **Vals Terminal-Bench 4.0 = 18,7**.
- **Wyraźnie powyżej poprzeczki i tanio (otwarte wagi):** MiMo-V2.6-Pro (AA 46, USD 0,87 za wyjście), GLM-5.3 u zewnętrznych
  hostów (AA 45, od USD 1,88), Step 5 Preview (AA 44, USD 2,70, darmowe promocje), GLM-5.3-Flash (AA 42, od USD 0,15),
  DeepSeek V4.1-Flash (AA 39, od USD 0,18) i MiMo-V2.6-Flash (AA 38, USD 0,28).
- **Powyżej poprzeczki, ale zamknięte:** Claude Haiku 5.5 (AA 43 przy max), GPT-6 Luna (AA 38 przy max) i Muse Spark 1.3
  Contributor (AA 45 przy najwyższym dozwolonym wysiłku, ale **Meta trenuje na twoich promptach**). To własnościowe API, więc nie ma lokalnego planu awaryjnego.
- **Najlepszy model agentowy w przeliczeniu na dolara to GLM-5.3-Flash.** Ma Vals TB4.0 37,4, dwa razy więcej niż poprzeczka, przy USD 0,50 za wyjście
  na Z.ai.
- **Samo AA wprowadza w błąd w przypadku agentów.** GPT-6 Luna (AA 38) i DeepSeek V4-Pro-0813 (AA 36) spadają **poniżej** poprzeczki na
  Vals TB4.0 (13,6 i 14,1).
- **Znane darmowe modele są poniżej poprzeczki.** Inkling, Inkling Small, Nemotron 3 Ultra, gpt-oss-120b,
  MiniMax-M3 i Kimi K2.6 mają AA od 12 do 29.
- **Kimi K3 (AA 44) to najmocniejszy otwarty model do używania narzędzi, ale nie jest tani.** Wyjście kosztuje od USD 9,50 do 15
  wszędzie, więc ma sens tylko w planie ryczałtowym.
- **Nie porównuj liczb AA między wersjami indeksu.** Ten sam model 0731 miał 50 w lipcu, a dziś ma 34.

## 2. Poprzeczka: trzy checkpointy „V4-Flash”

„DeepSeek-V4-Flash” to trzy różne rzeczy, a poprzeczka mocno się przesuwa w zależności od tego, o którą chodzi:

| Checkpoint | Wydany | Rozmiar | AA v4.3.2 (max) | Status |
|---|---|---|---|---|
| V4-Flash 0420 (preview) | 24.04.2026 | 284B łącznie / 13B aktywnych | 24 | wycofany na AA |
| **V4-Flash 0731 (GA), mój lokalny model** | 31.07.2026 | 284B / 13B | **34** | wycofany na AA na rzecz V4.1 |
| V4.1-Flash (nowe wagi) | 10.09.2026 | 552B / 16B | 39 (25 bez rozumowania) | aktualny |

Wszystkie trzy mają licencję MIT i natywny kontekst 1M. Wynikają z tego dwie pułapki:

- **Identyfikator online `deepseek-v4-flash` to już nie jest V4-Flash.** Od 10.09.2026 własne API DeepSeeka kieruje stare
  nazwy na `deepseek-flash`, czyli V4.1-Flash. Jeśli chcę dokładnie tych wag, które działają na moim sprzęcie, muszę użyć zewnętrznego
  hosta. OpenRouter wymienia `deepseek/deepseek-v4-flash-0731` z 27 endpointami.
- **Starsze wpisy na blogach używają liczb z preview 0420.** Słynne „SWE-bench Verified 79,0” i „SWE-bench Pro 52,6”
  należą do preview *(deklaracja producenta)*. Dla 0731 Vals zmierzył SWE-bench Verified 88,8 *(pomiar niezależny)*.

**Dlaczego wersja indeksu AA ma znaczenie.** AA kilka razy przeskalowało indeks, więc ten sam model dostaje bardzo różne
liczby w zależności od wersji:

| Model | AA v4.0 (kwi 2026) | AA v4.1 (lip 2026) | AA v4.3.2 (od 19.09.2026) |
|---|---|---|---|
| V4-Flash 0420 | 47 | 40 | 24 |
| V4-Flash 0731 | – | 50 | 34 |

Przeskalowanie v4.3 (7.09.2026) dodało Terminal-Bench 4.0 i zastąpiło tau3-Banking przez AutomationBench. Obecne
wagi to Agents 30 %, Coding 20 %, Science 20 % i General 30 %. Każdy wpis na blogu, który mówi „Inkling 41 vs V4 Flash 40”,
używa starszej wersji. **W tym pliku porównuję tylko liczby z v4.3.2.** Gdyby mój sprzęt uruchamiał preview 0420, poprzeczka wynosiłaby
24, a MiniMax-M3, Kimi K2.6, GLM-5.1 i oba Inklingi by ją przeskoczyły. Uruchamia 0731, więc nie przeskakują (sekcja 7).

Inne liczby bazowe dla 0731: Vals TB2.1 **67,0**, Vals TB4.0 **18,7**, Vals SWE-bench Verified 88,8, Vals
LiveCodeBench 87,3, Vals GPQA 89,9 *(pomiary niezależne)*. Własna karta DeepSeeka deklaruje TB2.1 82,7, DeepSWE 54,4
i Toolathlon-Verified 70,3 *(deklaracja producenta)*. Tryb bez myślenia jest dużo słabszy: w preview HLE spadło z 35 do
8, a LiveCodeBench z 92 do 55 *(deklaracja producenta)*. Uruchamiaj go z włączonym rozumowaniem.

## 3. Benchmarki: co jeszcze żyje w II połowie 2026

Większość benchmarków cytowanych w poradnikach o agentach jest **zamrożona**: od miesięcy nie dodano nowych modeli.

| Benchmark | Stan na 13.10.2026 | Używać? |
|---|---|---|
| AA Intelligence Index v4.3.2 | żywy, obejmuje prawie każdy model | tak, jako główny ranking |
| Vals Terminal-Bench 4.0 | żywy, 48 modeli | **tak, dla trudnych agentów** |
| Vals Terminal-Bench 2.1 | zarchiwizowany 28.09.2026, 76 modeli | tak, dla modeli wydanych przed tą datą |
| Tablica tbench.ai TB4.0 | żywa, mniej modeli | do kontroli krzyżowej |
| SWE-bench Verified (oficjalny) | ostatnie wpisy w lutym 2026. Vals zarchiwizował go 1.09.2026 jako nasycony | tylko dla modeli, które już na nim są |
| BFCL V4 | ostatnia aktualizacja 12.04.2026 | nie, za stary |
| tau2-bench | ok. marca 2026 | nie |
| SWE-Bench Pro public (Scale) | nieaktualny | nie |
| LiveCodeBench, GPQA, MMLU-Pro (Vals) | zarchiwizowane 1.09.2026 | tylko jako tło |
| Terminal-Bench 2.0 (Vals) | zarchiwizowany 4.06.2026 | nie, nie jest porównywalny z 2.1 |

W II połowie 2026 producenci raportują Terminal-Bench 2.1/3.0/4.0, DeepSWE v1.1, Toolathlon-Verified, AutomationBench, MCP-Atlas
i Agents' Last Exam. Te liczby producentów rzadko pochodzą z tego samego harnessu.

**Różnica między liczbami producentów a niezależnymi jest duża.** Na Terminal-Bench 2.1 producenci raportują o około 10 do 20
punktów więcej, niż mierzy Vals:

| Model | TB2.1 *(deklaracja producenta)* | TB2.1 Vals *(pomiar niezależny)* | Różnica |
|---|---|---|---|
| DeepSeek V4-Flash 0731 | 82,7 | 67,0 | 15,7 |
| DeepSeek V4.1-Flash | 90,6 | 74,5 | 16,1 |
| GLM-5.3 | 88,2 | 71,5 | 16,7 |
| MiMo-V2.6-Pro | 89,9 | 67,8 | 22,1 |

Różnica działa też w drugą stronę: DeepSeek raportuje TB4.0 7,0 dla 0731, a Vals mierzy 18,7. **Zasada jest taka, że modele rankinguję
wyłącznie według AA oraz kolumn Vals.** Liczb producentów używam do opisania charakteru modelu, nie do ustalania jego miejsca w rankingu.

## 4. Główna tabela: na poziomie poprzeczki lub powyżej, i tanio

„Tanio” oznacza co najmniej jedną publiczną ścieżkę na poziomie około USD 3 za 1M tokenów wyjścia lub niżej, albo za darmo. Cena to
najtańsza cena wyjścia, jaką widziałem 13.10.2026. „OR” oznacza endpoint OpenRouter, a „–” oznacza brak opublikowanego wyniku.
Model-poprzeczka jest w pierwszym wierszu.

| Model | AA | Vals TB4.0 | Vals TB2.1 | Natywny kontekst | Licencja / otwartość | Wydany | Najtańsze wyjście (ścieżka) |
|---|---|---|---|---|---|---|---|
| DeepSeek V4-Flash 0731 (poprzeczka) | 34 | 18,7 | 67,0 | 1M | MIT, otwarty | 31.07.2026 | 0,18 (DeepInfra FP8, OR) |
| Muse Spark 1.3 Contributor | 45 (xhigh; max niedostępny) | 10,6 std / 24,8 Max | 72,3 std / 79,0 Max | 1M | własnościowy, trenuje na promptach | 2.09.2026 | 0,20 (Meta Contributor); za darmo w OpenCode Zen |
| MiMo-V2.6-Pro | 46 | 31,3 | 67,8 | 1M | MIT, otwarty | 21.09.2026 | 0,87 (Xiaomi, DeepInfra FP8) |
| GLM-5.3 (max) | 45 | 38,9 | 71,5 | 1M | licencja GLM-5.3 (ograniczenia), otwarty | 18.08.2026 | 1,88 (Baidu FP8 / Inceptron FP4, OR); Z.ai 4,40 |
| Step 5 Preview | 44 | 31,8 | – | 1M | tylko API, wagi obiecane na 15.10.2026 | 20.09.2026 | 2,70 (StepFun); za darmo w Kilo i OpenCode Zen |
| Claude Haiku 5.5 (max) | 43 | 36,4 | – | 1M | własnościowy | 7.10.2026 | 0,50 (prompt do 100K; 2,50 powyżej) |
| GLM-5.3-Flash | 42 | 37,4 | 62,9 | 1M | MIT, otwarty | 26.08.2026 | 0,15 (StreamLake FP8, OR); Z.ai 0,50 |
| Ling 3.1 Flash | 41 | – | – | 1M na AA, 262K na OR | na razie własnościowy, „wagi wkrótce” | 1.10.2026 | 0,225 (Novita, OR); za darmo w Requesty, Kilo, OpenCode Zen |
| Gemini 3.8 Flash (high) | 41 | 19,7 | 81,3 | 1M | własnościowy | 2.09.2026 | 1,875 batch; 3,75 standard; darmowy pakiet ok. 20 RPD |
| Qwen3.8-Flash-Next | 40 | – | – | 262K | Qwen Community Licence 1.0, otwarty | 26.08.2026 | 0,47 (Alibaba, jedyny host) |
| DeepSeek V4.1-Flash | 39 | 19,7 | 74,5 | 1M | MIT, otwarty | 10.09.2026 | 0,18 (Decart FP4, OR); DeepSeek 0,60 poza szczytem |
| MiMo-V2.6-Flash | 38 | 24,2 | 76,4 | 1M | MIT, otwarty | 21.09.2026 | 0,28 (Xiaomi); za darmo w OpenCode Zen |
| GPT-6 Luna (max) | 38 | 13,6 | 73,0 | 1,05M | własnościowy | 22.09.2026 | 0,50 (prompt od 272K: 0,75) |
| Mistral Large 4 Preview | 38 | 23,2 | – | deklarowane 1M, zmierzone 524K | „otwarty”, licencja i wagi pod koniec października 2026 | 6.10.2026 | 2,09 promocja startowa (cennik 4,18) |
| DeepSeek V4-Pro 0813 | 36 | 14,1 | 54,7 | 1M | MIT, otwarty | sie 2026 | 0,75 (Baidu FP8, OR, promocja); DeepSeek 1,98 poza szczytem |
| Qwen3.8 27B (xhigh) | 34 | – | 58,4 | 256K | Apache 2.0, otwarty, gęsty | 14.08.2026 | 1,25 (Chutes); Cerebras 1,49 |

Jak to czytać:

- **AA i TB4.0 często się nie zgadzają.** Muse Spark, GPT-6 Luna i V4-Pro wyglądają mocno na AA i słabo na TB4.0. Haiku 5.5 i
  GLM-5.3-Flash to przypadek odwrotny. Omawia to sekcja 8.
- **Poziom wysiłku jest częścią wyniku.** GLM-5.3 przy niskim wysiłku to AA 34, Haiku 5.5 przy średnim to 34, GPT-6 Luna przy high
  to 33, a Gemini 3.8 Flash przy low to 33. Tanie wywołanie przy niskim wysiłku może wylądować na poziomie poprzeczki lub poniżej.
- **Najtańsza ścieżka to często FP4 albo promocja.** FP4 nie jest automatycznie złe (Nebius FP4 GLM-5.3 osiągnął 99 % w
  Endpoint Accuracy Index AA), ale konkretne endpointy traciły od 15 do 27 % *(pomiar niezależny)*. Przypnij kwantyzację
  albo dostawcę. Porównanie hostów jest w [01-PROFILE.md](01-PROFILE.md).

## 5. Notatki o poszczególnych modelach pod kątem agentów

**MiMo-V2.6-Pro (Xiaomi, AA 46).** To najwyżej oceniany otwarty model na AA: 1,02T łącznie / 42B aktywnych, kontekst 1M,
wejście tekstowe, obrazowe, audio i wideo. Xiaomi sprzedaje go po USD 0,435 / 0,87 z odczytem cache za 0,0036.
- Mocne strony: Vals TB4.0 31,3 to wynik wyraźnie powyżej poprzeczki. Producent deklaruje DeepSWE 71,9 i AutomationBench 53,1 *(deklaracja
  producenta, harness nieujawniony)*.
- Słabe strony: jest wolny (ok. 42 do 47 tok/s, TTFT ok. 4 s) i ma niewielu hostów (4 na OR, część zdegradowana). Vals TB2.1
  67,8 to tylko poziom poprzeczki. W praktycznym teście DevOps Terraform i bash były w porządku, ale zadziałał tylko 1 z 3 manifestów Kubernetes;
  pozostałe wpadały w crash-loop *(pomiar niezależny)*.
- Pułapki: rozumowanie jest domyślnie włączone. Na endpoincie zgodnym z Anthropic **wieloturowe wywołania narzędzi zwracają 400, jeśli
  `reasoning_content` nie jest odsyłane z powrotem**, więc powtarzaj je w historii. Maksymalne wyjście u producenta to 128K.

**MiMo-V2.6-Flash (Xiaomi, AA 38).** Ma 309B / 15B parametrów, licencję MIT i kontekst 1M, za USD 0,14 / 0,28.
- Mocne strony: **Vals TB2.1 76,4 bije V4.1-Flash**, a TB4.0 24,2 jest powyżej poprzeczki. Razem z V4.1-Flash ma
  najlepszą cenę za punkt inteligencji w zestawieniu.
- Słabe strony: bardzo rozwlekły (240M tokenów wyjścia w przebiegu AA, przy medianie 140M). Wypadł gorzej niż Pro w tym samym
  teście DevOps (zadziałało 0 z 3 manifestów Kubernetes).
- Pułapki: obowiązuje zasada odsyłania rozumowania z Pro. Darmowy wariant w OpenCode Zen wykorzystuje twoje dane.

**GLM-5.3 (Z.ai, AA 45 przy max).** Ma 753B / 40B parametrów i kontekst 1M, z wysiłkiem low/high/max i flagą
`clear_thinking`.
- Mocne strony: **najmocniejsze niezależne wyniki agentowe spośród wszystkich tanio dostępnych otwartych modeli.** Ma Vals TB4.0 38,9,
  tbench.ai TB4.0 41,8 (harness Claude Code) i Vals SWE-bench Verified 95,4.
- Słabe strony: rozwlekły (210M) i wolny (64 tok/s). Licencja ma ograniczenia, więc ją przeczytaj.
- Pułapki: cena u samego Z.ai (USD 1,40 / 4,40) przekracza limit. Zewnętrzni hości sprzedają go za USD 1,88 do 2,90,
  a endpointy trzymają się blisko siebie pod względem dokładności (95 do 99 % w Endpoint Accuracy Index AA). **Myślenie jest zawsze włączone, a
  domyślny wysiłek to max**, więc w pętlach narzędziowych ustaw `reasoning_effort` na low. Przy niskim wysiłku to AA 34, dokładnie poprzeczka.

**GLM-5.3-Flash (Z.ai, AA 42).** Ma 320B / 18B parametrów, licencję MIT, kontekst 1M i hybrydową atencję rzadką plus liniową,
za USD 0,15 / 0,50 na Z.ai.
- Mocne strony: **najlepszy wynik w trudnych zadaniach terminalowych w przeliczeniu na dolara.** Ma Vals TB4.0 37,4 i tbench.ai TB4.0 35,8 nawet
  przy wysiłku `none`. Ma też ExtractBench 80,75 dla wyjścia strukturalnego *(deklaracja producenta)* i Vals SWE-bench
  Verified 92,0. Obsługuje `parallel_tool_calls` na OR i ma 32 endpointy na OR.
- Słabe strony: bardzo rozwlekły (180M) i poniżej przeciętnej szybkości. Jego wynik LiveCodeBench (80,5) jest słabszy niż DeepSeeka.
- Pułapki: jakość hostów się różni. W teście narzędzi na 600 zadaniach Fireworks uzyskał 99,5 %, a Nebius 84,8 % *(pomiar
  niezależny)*.

**DeepSeek V4.1-Flash (AA 39, 25 bez rozumowania).** To naturalne ulepszenie online w ramach tej samej rodziny. Ma
552B / 16B parametrów, cache KV w FP4, kontekst 1M, do 384K wyjścia i ciągłe ustawienie wysiłku od 1 do 100.
- Mocne strony: Vals TB2.1 74,5 wobec 67,0 dla 0731. U producenta działa z prędkością 190 tok/s przy TTFT 0,96 s i obsługuje do
  2500 równoległych żądań. Przyjmuje wyjście JSON i wywołania narzędzi oraz obsługuje u producenta Responses API i
  API zgodne z Anthropic.
- Słabe strony: **w trudnych zadaniach TB4.0 rośnie tylko z 18,7 do 19,7.** To najbardziej rozwlekły model zmierzony przez AA (250M).
- Pułapki: nie ma szablonu czatu Jinja, więc każdy host implementuje własne parsowanie narzędzi, a wywołania narzędzi mogą się różnić
  między hostami. Wiele z jego 32 endpointów na OR to FP4. Vercel ogranicza wyjście do 32K. Producent mówi, że wysiłek 60 do 80 daje większość
  maksymalnej dokładności przy mniej niż połowie tokenów *(deklaracja producenta)*. DeepSeek domyślnie trenuje na danych wejściowych API (opt-out).

**DeepSeek V4-Flash-0731 (AA 34, poprzeczka).** To dokładnie te wagi, które działają na moim sprzęcie. Online kosztuje USD 0,06 / 0,18
w DeepInfra (FP8).
- Mocne strony: to idealny cel dla nadmiarowego ruchu. Moje prompty zachowują się online tak samo jak lokalnie, mniej więcej w cenie
  prądu.
- Słabe strony: jest słaby w wiedzy, a AA zmierzyło bardzo wysoki odsetek halucynacji, gdy model nie jest pewny (96 % dla
  preview). Jest rozwlekły (ok. 206M w przebiegu v4.1).
- Pułapki: nie ma szablonu Jinja (to samo zastrzeżenie co przy V4.1). Wariant `:free` na OR został usunięty 21.09.2026.
  Hości wycofują starszy identyfikator 0420.

**DeepSeek V4-Pro-0813 (AA 36).** Ma 1,6T / 49B parametrów i licencję MIT.
- Mocne strony: **Vals SWE-bench Verified 96,4, najlepszy wynik w pisaniu poprawek w tanim zestawie.** Ma też GPQA 92,4.
- Słabe strony: w agentach terminalowych jest słabszy niż poprzeczka: Vals TB2.1 54,7 i TB4.0 14,1.
- Pułapki: tania ścieżka Baidu (USD 0,75) to promocja z 81 % rabatu. DeepInfra ogranicza wyjście do 16K. Cena u samego DeepSeeka
  w szczycie (USD 3,96) przekracza limit, a poza szczytem wynosi USD 1,98.

**Step 5 Preview (StepFun, AA 44).** Ma 600B / 27B parametrów, kontekst 1M oraz wejście obrazowe i wideo.
- Mocne strony: Vals TB4.0 31,8. Producent deklaruje TB2.1 85,0, GPQA 93,5 i BrowseComp 88,7 *(deklaracja producenta)*. Jest darmowy
  w Kilo (bez konta, 200 żądań/h na IP, może trenować) i w OpenCode Zen (zero retencji, bez trenowania).
- Słabe strony: jeden płatny host (StepFun FP8), a jego warunki dotyczące danych są nieznane.
- Pułapki: **to preview**, więc spodziewaj się zmian. Wagi obiecano na 15.10.2026. Maksymalne wyjście to 64K. Darmowe
  ścieżki to promocje ograniczone czasowo.

**Ling 3.1 Flash (InclusionAI, AA 41).** To hybrydowy MoE z rozumowaniem 560B / 25B wydany 1.10.2026.
- Mocne strony: bardzo tani (Novita USD 0,075 / 0,225) i darmowy w Requesty (bez retencji i bez trenowania według
  metadanych Requesty, endpoint w UE, 200 RPD).
- Słabe strony: nie ma jeszcze niezależnych benchmarków agentowych ani wag. Jest bardzo rozwlekły (220M).
- Pułapki: **OR i Requesty serwują tylko kontekst 262K i maksymalnie 32K wyjścia**, a Requesty oznacza brak obsługi JSON-schema.
  Jego darmowe oferty zmieniają się z dnia na dzień; darmowy wariant na OR zniknął między 12 a 13.10.2026. Jest obiecujący, ale
  niesprawdzony.

**Qwen3.8-Flash-Next (Alibaba, AA 40).** Ma 180B / 6B parametrów, jest zapowiedzią architektury Qwen4 i
ma kontekst 262K.
- Mocne strony: producent deklaruje TB2.1 86,1, DeepSWE 58,7 i SWE-Pro 62,5 *(deklaracja producenta)*. Cena jest niska: USD
  0,15 / 0,47.
- Słabe strony: nie ma liczb z Vals, a Alibaba jest jedynym hostem. Jest bardzo rozwlekły (240M).
- Pułapki: **identyfikator modelu jest niejednoznaczny.** Według doniesień identyfikator Qwen Cloud „Qwen3.8-Flash” to nie ten sam model, a
  `qwen/qwen3.8-flash` na OR (kontekst 1M) może być modelem chmurowym. Sprawdź, który dostajesz.

**Qwen3.8 27B (AA 34 przy xhigh, 28 przy medium).** To gęsty model 27B z licencją Apache 2.0, kontekstem 256K i
wejściem multimodalnym.
- Mocne strony: to jedyny model na poziomie poprzeczki, który jest na tyle mały, by działać na skromnym lokalnym sprzęcie. Cerebras serwuje go
  szybko.
- Słabe strony: osiąga poprzeczkę tylko przy wysiłku xhigh (200M tokenów, 45 tok/s). Vals TB2.1 58,4 jest poniżej poprzeczki.
- Pułapki: Cerebras ogranicza kontekst do 65K. Darmowy wariant na OR został usunięty 6.10.2026.

**Gemini 3.8 Flash (Google, AA 41 przy high).** Jest własnościowy, z kontekstem 1M.
- Mocne strony: najlepsze wyniki wiedzy w zestawieniu: Vals GPQA 94,4, MMLU-Pro 90,2, LiveCodeBench 89,5 i TB2.1 81,3.
  Istnieje darmowy pakiet z warunkami bez trenowania w EOG.
- Słabe strony: **Vals TB4.0 19,7 to tylko poziom poprzeczki** dla trudnych agentów. TTFT według AA przy wysokim wysiłku to ok. 25 s.
- Pułapki: maksymalne wyjście to 65K. Cena wprowadzająca (USD 0,75 / 3,75) rośnie do **USD 1,50 / 7,50 od 1.01.2027**, a pod limitem
  utrzymuje ją wtedy tylko przetwarzanie wsadowe (za pół ceny). Darmowy pakiet daje ok. 20 żądań dziennie według doniesień
  z forów.

**Mistral Large 4 Preview (AA 38).** Ma 1,05T / 52B parametrów, wejście obrazowe i jest trenowany oraz hostowany w UE.
- Mocne strony: Vals TB4.0 23,2 jest powyżej poprzeczki. Producent deklaruje AutomationBench 59,9 i DeepSWE 61,7 *(deklaracja producenta)*.
  Ma znaczenie, jeśli potrzebuję rezydencji danych w UE.
- Słabe strony: zmierzony kontekst to 524K, wobec deklarowanych 1M.
- Pułapki: **to preview i jest tani tylko podczas promocji startowej** (USD 0,68 / 2,09; cennikowe wyjście 4,18).
  Wagi i licencja mają się pojawić pod koniec października 2026.

**Tanie modele zamknięte.** To własnościowe API. Nie ma wag ani lokalnego planu awaryjnego, a dostawca może
zmienić zachowanie pod tym samym identyfikatorem.

- **Claude Haiku 5.5 (AA 43 max, 38 high, 34 medium).** Kosztuje USD 0,10 / 0,50 do promptu 100K, a potem **0,50 /
  2,50 powyżej 100K**, więc pętle agentowe z długim kontekstem szybko trafiają na próg 5x. Jego wyniki agentowe są mocne: Vals TB4.0
  36,4, trzeci najlepszy w tym pliku, i OSWorld 2.1 72,4 *(deklaracja producenta)*. Przy maksymalnym wysiłku jest skrajnie rozwlekły (440M
  tokenów), a AA zmierzyło **TTFT ok. 303 s**. Średni wysiłek to tylko poziom poprzeczki. API jest natywne dla Anthropic, a
  dostęp zgodny z OpenAI idzie przez bramy.
- **GPT-6 Luna (AA 38 max, 35 xhigh, 33 high).** Kosztuje USD 0,10 / 0,50 (0,75 za wyjście od promptu 272K), z kontekstem 1,05M
  i wyjściem 128K. Ma Vals TB2.1 73,0, ale **TB4.0 13,6, poniżej poprzeczki**. Jedno źródło podaje, że **wywoływanie narzędzi
  działa tylko przy wysiłku rozumowania `none` w Chat Completions**, więc do rozumowania z narzędziami potrzebne jest Responses API
  (sprawdź to sam). To samo źródło podaje 93 % halucynacji przy maksymalnym wysiłku. TTFT według AA przy max to ok.
  89 s.
- **Muse Spark 1.3 Contributor (Meta, AA 45 przy xhigh).** Kosztuje USD 0,10 / 0,20, bo **Meta trenuje na twoich
  promptach i odpowiedziach**. Według dokumentacji Mety identyfikator Contributor nie działa na poziomie „max”, więc jego
  sufit to xhigh = AA 45 (Muse Spark 1.3 standard przy max = 48). Oficjalny limit 13.10.2026 to 150 RPM / 3M TPM na zespół
  (starsze blogi podają 60 lub 100 RPM). Dostęp z UE jest niepotwierdzony: działa tylko tam, „gdzie Meta włączyła dostęp”,
  bez umowy powierzenia (DPA). Vals wymienia „Muse Spark 1.3” (TB4.0 10,6) i „Muse Spark 1.3 Max” (TB4.0 24,8)
  osobno. Wysyłałbym do niego tylko niewrażliwy tekst masowy, nigdy nic z kontekstem klienta.

## 6. Powyżej poprzeczki, ale nie tanio

| Model | AA | Niezależne liczby agentowe | Najtańsze wyjście | Dlaczego tu jest |
|---|---|---|---|---|
| Kimi K3 (max) | 44 (30 przy low) | Vals TB2.1 80,9, TB4.0 17,2, SWE-V 93,4 | 9,50 (Chutes, bez narzędzi); Moonshot 15,00 | najlepszy otwarty model do narzędzi, drogi w przeliczeniu na token |
| Grok 4.7 | 46 | Vals TB4.0 28,8 | 6,00 | kontekst 500K, TTFT ok. 101 s |
| Qwen3.8 Max | 45 | Vals TB4.0 34,3 | 6,00 | własnościowy |
| GPT-6.1 Sol (low) | 42 | – | 10,00 | zwięzły: koszt zadania według AA USD 0,13 |
| GPT-5.6 Terra | 42 | Vals TB2.1 77,5, SWE-V 95,4 | 12,00 | |
| Muse Spark 1.3 standard | 48 | patrz sekcja 5 | 4,25 | tania ścieżka to pakiet Contributor |
| Gemini 3.8 Flash od 2027 | 41 | patrz sekcja 5 | 7,50 cennik | pozostaje tani tylko przez batch lub darmowy pakiet |

**Kimi K3** jest tu najciekawszy. Ma najlepsze liczby do używania narzędzi spośród otwartych modeli: MCP-Atlas 84,2, MCPMark-V 94,5,
Toolathlon-Verified 76,5 i BrowseComp 91,2 *(deklaracja producenta)*. Zauważ jednak, że jego Vals TB4.0 (17,2) jest tuż poniżej
poprzeczki. Myślenie jest zawsze włączone i **każda tura musi powtarzać pełną wiadomość asystenta, łącznie z `reasoning_content`
i `tool_calls`**. Polityka prywatności Moonshot pozwala trenować na treściach użytkowników.

**Plany ryczałtowe zmieniają cenę, ale mają zasady dotyczące zakresu użycia:**

- **Kimi Code** (Plus USD 19, Pro 39, Max 99, Ultra 199 miesięcznie) obejmuje K3. `k3-256k` jest w Plus, a `k3` z kontekstem 1M
  jest w Pro i wyżej. Ograniczony do obsługiwanych klientów do kodowania, takich jak Claude Code, OpenCode i Codex.
  Manipulowanie User-Agentem może skończyć się zawieszeniem konta. **Mój własny agent to tu szara strefa, a backend produktu
  jest niedozwolony.**
- **GLM Coding Plan** (Lite USD 18 miesięcznie, cena zewnętrzna) daje GLM-5.3 o wartości mniej więcej USD 65 do 175 miesięcznie
  w trybie PAYG, według moich obliczeń na podstawie opublikowanych mnożników kredytów. Można go używać **tylko w oficjalnie
  obsługiwanych narzędziach**, więc surowe wywołania API z mojego własnego agenta odpadają. Dla GLM-5.3-Flash plan jest mało opłacalny; PAYG jest
  lepszy.
- **Ollama Cloud Pro** (USD 20 miesięcznie z kredytami za USD 60) serwuje `kimi-k3` i `glm-5.3` po cenach cennikowych, bez
  ograniczeń w używaniu API. To obniża efektywną cenę wyjścia K3 do ok. USD 5, co wciąż przekracza limit.
- **Step Plan** (od Mini USD 6,99 do Max USD 99, ceny zewnętrzne) obejmuje Step 5 Preview i wydaje się pozwalać na własny
  stos. Sprawdź to w warunkach korzystania z usługi.
- Fireworks Fire Pass (Kimi K3 Fast) został zamknięty dla nowych subskrybentów w październiku 2026.

## 7. Poniżej poprzeczki, w tym darmowe modele

„Darmowy” zwykle oznacza model słabszy niż ten, który mój sprzęt już uruchamia. Oto te, które są wciąż oferowane, z
wynikami AA v4.3.2 wobec poprzeczki 34:

| Model | AA | Niezależne liczby agentowe | Gdzie jest darmowy lub tani | Werdykt |
|---|---|---|---|---|
| MiniMax-M3 | 29 | Vals TB2.1 53,6, **TB4.0 1,0**, SWE-V 75,0 | USD 0,96 do 1,20 za wyjście; kwalifikuje się do darmowego pakietu Vercel | poniżej, tani i otwarty, kontekst 1M |
| Kimi K2.6 | 27 | Vals TB2.1 53,6, SWE-V 76,2 | USD 1,82 do 1,95 (Baidu, Chutes) | poniżej, wycofany na AA |
| Kimi K2.7 Code | 26 | Vals TB2.1 67,0, SWE-V 78,2 | kwalifikuje się do darmowego pakietu Vercel; USD 4,00 cennik | dostrojony do kodu, poniżej na AA |
| Inkling Small | 26 | Vals TB2.1 55,1 | `:free` na OR, Kilo | poniżej |
| Inkling | 25 | Vals TB2.1 47,6 | `:free` na OR (kontekst 1M, 262K wyjścia) | poniżej, ignoruje `tool_choice` |
| Nemotron 3 Ultra 550B | 23 | Vals TB2.1 50,9, SWE-V 69,0; AutomationBench 3 % (AA) | za darmo na OR, Kilo, Requesty | poniżej, warunki próbne NVIDIA mówią, by nie wysyłać danych osobowych |
| gpt-oss-120b (high) | 12 | Vals TB2.0 19,1, SWE-V 33,6 | od USD 0,15 za wyjście; OVH anonimowo 2 RPM | daleko poniżej dla agentów |

Inne modele poniżej poprzeczki to m.in. Gemini 3.1 Pro Preview (30, TB4.0 2,5), GLM-5.1 (26), Gemini 3 Flash (26), Qwen3.7 Plus
(25), preview V4-Flash 0420 (24), Kimi K2.5 i MiniMax-M2.7 (23), GLM-4.7 (22), Gemini 3.5 Flash-Lite (22),
Qwen3.5 i Qwen3.6 (18), Mistral Medium 3.5 (14) oraz Llama 4 Maverick i Scout (10 i 8). **Wszystko z typowych list
„darmowych i tanich” z początku 2026 jest dziś poniżej V4-Flash-0731:** GLM-4.6/4.7, Kimi K2.x, Qwen3.5/3.6, MiniMax
M2.x, gpt-oss-120b, Gemini 2.5/3 Flash, Mistral Medium 3.x, Grok fast, GPT-5.x mini i Llama 4.

**Naprawdę darmowe modele powyżej poprzeczki to wyłącznie promocje ograniczone czasowo:** Step 5 Preview (Kilo, OpenCode Zen),
Ling 3.1 Flash (Requesty, Kilo, OpenCode Zen), MiMo-V2.6-Flash (OpenCode Zen) i Muse Spark 1.3 Contributor (OpenCode
Zen, trenuje). Mediana czasu obecności darmowego modelu na OR to ok. 75 dni, a lista darmowych modeli na OR skurczyła się z 24 do 16 pozycji
między 21.09 a 13.10.2026. GLM-5.3-Flash nie jest darmowy, ale miesięczny kredyt Vercel o wartości USD 5 kupuje ok. 10M jego
tokenów wyjścia.

## 8. Ranking trudnych agentów: Vals Terminal-Bench 4.0

TB4.0 to najtrudniejszy żywy benchmark agentowy z niezależnym harnessem. Poprzeczka (0731) to **18,7**. Tabela obejmuje
każdy model z tego pliku, który Vals uruchomił.

| Miejsce | Model | Vals TB4.0 | AA | Tanio? |
|---|---|---|---|---|
| 1 | GLM-5.3 | 38,9 | 45 | tak (zewnętrzni hości) |
| 2 | GLM-5.3-Flash | 37,4 | 42 | **tak, USD 0,15 do 0,50** |
| 3 | Claude Haiku 5.5 | 36,4 | 43 | tak, zamknięty |
| 4 | Qwen3.8 Max | 34,3 | 45 | nie |
| 5 | Step 5 Preview | 31,8 | 44 | tak, preview |
| 6 | MiMo-V2.6-Pro | 31,3 | 46 | tak |
| 7 | Grok 4.7 | 28,8 | 46 | nie |
| 8 | Muse Spark 1.3 Max | 24,8 | 48 | tylko cena standardowa |
| 9 | MiMo-V2.6-Flash | 24,2 | 38 | tak |
| 10 | Mistral Large 4 Preview | 23,2 | 38 | tylko w promocji |
| 11 | DeepSeek V4.1-Flash | 19,7 | 39 | tak |
| 11 | Gemini 3.8 Flash | 19,7 | 41 | batch lub darmowy pakiet |
| – | **DeepSeek V4-Flash 0731 (poprzeczka)** | **18,7** | **34** | lokalnie |
| 13 | Kimi K3 | 17,2 | 44 | nie |
| 14 | DeepSeek V4-Pro 0813 | 14,1 | 36 | tak |
| 15 | GPT-6 Luna | 13,6 | 38 | tak, zamknięty |
| 16 | Muse Spark 1.3 (standard) | 10,6 | 48 | pakiet Contributor |
| 17 | MiniMax-M3 | 1,0 | 29 | tak |

Co to pokazuje:

- **Samo AA wprowadza w błąd w przypadku agentów.** GPT-6 Luna i V4-Pro-0813 przeskakują poprzeczkę AA, ale w trudnych zadaniach terminalowych
  spadają poniżej 0731. Muse Spark 1.3 ma najwyższe AA w pliku (48), a mimo to jego standardowe SKU uzyskuje 10,6.
- **Zdarza się też odwrotnie.** GLM-5.3-Flash i Haiku 5.5 zajmują na TB4.0 wyższe miejsca, niż sugerowałaby ich pozycja na AA.
- **V4.1-Flash nie jest dużym krokiem naprzód dla trudnych agentów.** Ledwo bije poprzeczkę (19,7 wobec 18,7), więc powodem, by go używać,
  są szybkość i cena, a nie możliwości.
- Oficjalna tablica tbench.ai potwierdza kolejność: GLM-5.3 41,8, GLM-5.3-Flash 35,8, Gemini 3.8 Flash 19,1, GPT-6 Luna
  16,4.
- Ling 3.1 Flash, Qwen3.8-Flash-Next i Qwen3.8 27B nie mają jeszcze przebiegu TB4.0, więc traktuję je jako niesprawdzone dla trudnych agentów.

Aby sprawdzić model na własnych zadaniach zamiast na rankingu, zobacz
[../kurs_aplikacje_agentowe/14-EWALUACJA.md](../kurs_aplikacje_agentowe/14-EWALUACJA.md).

## 9. Moje wybory według roli

Te wybory dotyczą wyłącznie danych niewrażliwych. Dane klientów i dane zawodowe zostają na lokalnym sprzęcie.

- **Pracownik masowy** (streszczenia, ekstrakcja, klasyfikacja na dużą skalę): **GLM-5.3-Flash** za USD 0,15 / 0,50 na Z.ai,
  Fireworks, Together lub Parasail, z `reasoning_effort` ustawionym nisko. Z.ai nie trenuje na danych z API. Mój drugi wybór
  to **V4-Flash-0731 w DeepInfra** (USD 0,06 / 0,18). To mój lokalny model, więc te same prompty działają przy nadmiarowym ruchu
  bez żadnego ponownego strojenia. **MiMo-V2.6-Flash** (USD 0,28) to alternatywa, gdy potrzebuję pracy w powłoce w stylu TB2.1.
- **Podagent do kodowania:** **GLM-5.3** przez wiernego zewnętrznego hosta (USD 1,88 do 2,20 za wyjście) albo przez GLM
  Coding Plan, gdy działa w Claude Code lub OpenCode. GLM-5.3-Flash jest prawie tak samo mocny na TB4.0 za ćwierć
  ceny. Do zadań polegających tylko na poprawkach (napraw ten nieprzechodzący test) **V4-Pro-0813** ma najlepszy wynik SWE-bench Verified (96,4),
  ale nie pozwoliłbym mu sterować terminalem. Jeśli zamknięty model jest w porządku: **Haiku 5.5** przy wysokim wysiłku, z promptem poniżej
  100K.
- **Router narzędzi** (wybiera narzędzie lub emituje JSON, liczy się opóźnienie): **GLM-5.3-Flash** przy wysiłku `none` lub low. Wciąż
  uzyskuje 35,8 na tbench.ai TB4.0 przy `none`, obsługuje `parallel_tool_calls` i ma 80,75 na ExtractBench *(deklaracja
  producenta)*. W przeciwnym razie **V4.1-Flash u producenta** przy niskim wysiłku (190 tok/s, TTFT poniżej 1 s). Unikałbym GPT-6 Luna w
  Chat Completions (narzędzia tylko przy wysiłku `none`), darmowego Inklinga (brak `tool_choice`) oraz losowych routerów `openrouter/free` czy
  `kilo-auto/free`.
- **Czytnik długiego kontekstu** (całe repozytoria, długie logi, od 200K do 1M tokenów): **V4.1-Flash na DeepSeek** ma kontekst 1M i
  trafienia cache za USD 0,003 poza szczytem, więc utrzymuję stabilny prefiks. **Gemini 3.8 Flash** (darmowy pakiet lub batch) dobrze się sprawdza
  przy czytaniu wymagającym wiedzy, ale wyjście jest ograniczone do 65K. Unikałbym Ling na OR (262K), Mistral Large 4 (524K
  zmierzone) i ograniczonych endpointów 256K w Scaleway. Haiku 5.5 i GPT-6 Luna mają kontekst 1M, ale ich cena
  skacze powyżej 100K i 272K.
- **Lekki planista** (tania druga opinia poniżej Claude Opus): **MiMo-V2.6-Pro** (AA 46, USD 0,87 za wyjście). Jest wolny,
  ale planista nie potrzebuje wielu wywołań. Do darmowych eksperymentów **Step 5 Preview w OpenCode Zen** (zero retencji).
  **Muse Spark 1.3 Contributor** tylko do jednorazowych promptów, bo Meta na nich trenuje. Do prawdziwego planowania Opus pozostaje
  planistą (zobacz [../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md](../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md)).

**Źródła:** [AA leaderboard v4.3.2](https://artificialanalysis.ai/leaderboards/models) · [Metodologia AA](https://artificialanalysis.ai/methodology/intelligence-benchmarking) ·
[Changelog AA](https://artificialanalysis.ai/changelog) · [AA V4-Flash 0731](https://artificialanalysis.ai/models/deepseek-v4-flash) · [AA V4-Flash 0420](https://artificialanalysis.ai/models/deepseek-v4-flash-0420) ·
[AA 0731 w v4.1](https://artificialanalysis.ai/articles/deepseek-v4-flash-0731-scores-50-on-the-artificial-analysis-intelligence-index-10-points-above-previous-deepseek-v4-flash) ·
[Premiera V4 w AA v4.0](https://artificialanalysis.ai/articles/deepseek-is-back-among-the-leading-open-weights-models-with-v4-pro-and-v4-flash) · [AA V4.1-Flash](https://artificialanalysis.ai/models/deepseek-v4-1-flash) ·
[AA MiMo-V2.6-Pro](https://artificialanalysis.ai/models/mimo-v2-6-pro) · [AA GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash) · [AA Kimi K3](https://artificialanalysis.ai/models/kimi-k3) ·
[AA Claude Haiku 5.5](https://artificialanalysis.ai/models/claude-haiku-5-5) · [AA Endpoint Accuracy Index](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) ·
[Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [Vals TB2.1](https://www.vals.ai/benchmarks/terminal-bench-2-1) · [Vals SWE-bench](https://www.vals.ai/benchmarks/swebench) ·
[Ranking tbench.ai](https://www.tbench.ai/leaderboard) · [BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) · [Publikacja DeepSeek-V4](https://arxiv.org/pdf/2606.19348) ·
[Publikacja DeepSeek-V4.1-Flash](https://arxiv.org/pdf/2609.19969) · [Karta HF V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) · [HF GLM-5.3](https://huggingface.co/zai-org/GLM-5.3) ·
[HF Kimi K3](https://huggingface.co/moonshotai/Kimi-K3) · [Cennik DeepSeek](https://api-docs.deepseek.com/quick_start/pricing) · [Cennik Z.ai](https://docs.z.ai/guides/overview/pricing) ·
[Zasady użycia GLM Coding Plan](https://docs.z.ai/devpack/usage-policy) · [Dokumentacja Kimi Code](https://www.kimi.com/code/docs/en/) · [Cennik platformy Kimi](https://platform.kimi.ai/docs/pricing/chat) ·
[MiMo Token Plan](https://mimo.mi.com/docs/en-US/tokenplan/Token%20Plan/subscription) · [Cennik StepFun](https://platform.stepfun.ai/docs/en/guides/pricing/details) · [API modeli OpenRouter](https://openrouter.ai/api/v1/models) ·
[TrueFoundry o darmowych modelach OR](https://www.truefoundry.com/blog/openrouter-free-models-whats-actually-free-and-what-it-costs-you) · [Modele Kilo Gateway](https://api.kilo.ai/api/gateway/models) ·
[Dokumentacja OpenCode Zen](https://opencode.ai/docs/zen/) · [Darmowe modele Requesty](https://www.requesty.ai/models/free) · [Cennik Vercel AI Gateway](https://vercel.com/docs/ai-gateway/pricing) ·
[openbenchmarks: dokładność tego samego modelu](https://openbenchmarks.com/inference/same-model-different-accuracy) · [Test MiMo na computingforgeeks](https://computingforgeeks.com/xiaomi-mimo-v2-6-pro-flash/) ·
[computingforgeeks o GPT-6 Luna](https://computingforgeeks.com/gpt-6-sol-luna-released-features-benchmarks/) · [Cennik Claude](https://claude.com/pricing) · [Warunki Gemini API](https://ai.google.dev/gemini-api/terms) ·
[Vellum o Gemini 3.8 Flash](https://www.vellum.ai/md/blog/gemini-3-8-flash-benchmarks-explained) · [Cennik Mistral Large 4](https://capitalandcompute.net/md/mistral-large-4-pricing-benchmarks.md) ·
[Step 5 Preview](https://www.orcarouter.ai/blog/step-5-preview-open-weights) · [Qwen3.8-Flash-Next](https://llm-stats.com/blog/research/qwen3.8-flash-next-launch) ·
[Pakiet Muse Spark Contributor](https://cryptobriefing.com/meta-muse-spark-discounted-data-sharing/) · [Cennik Ollama Cloud](https://ollama.com/pricing)
