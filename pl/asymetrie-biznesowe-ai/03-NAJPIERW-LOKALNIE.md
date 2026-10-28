# Najpierw lokalnie: kiedy otwarte modele na własnym sprzęcie wygrywają

Ten rozdział odpowiada na jedno pytanie dla każdej okazji z [02-OKAZJE.md](02-OKAZJE.md): czy agent powinien działać
na otwartych modelach u klienta, w prywatnej chmurze w Polsce lub UE, czy może po prostu wywoływać płatne API?
Krótka wersja, sprawdzona 14.10.2026: **lokalnie rzadko wygrywa się kosztem tokenów, a często wygrywa się sprzedażą.**
Kupujący objęci tajemnicą zawodową, regulacjami sektora publicznego albo z działem IT, który zakazał wysyłania danych
do chmur amerykańskich i chińskich, zapłacą za skrzynkę, na którą mogą wskazać palcem. Twoja marża bierze się z
wdrożenia, aktualizacji i wsparcia, a nie z tańszych tokenów.

Wszystkie ceny i wersje poniżej sprawdzono 14.10.2026, chyba że podano inną datę. Tam, gdzie nie dało się sprawdzić
jakiejś wartości w tym przebiegu, tekst mówi „nie znaleziono".

## 1. Dlaczego kupujący chcą lokalnie

### RODO: łańcuch podmiotów przetwarzających i transfery

- Dostawca AI przetwarzający dokumenty klienta jest **podmiotem przetwarzającym** w rozumieniu art. 28 RODO: kupujący
  potrzebuje umowy powierzenia przetwarzania danych i listy podprocesorów. Każda dodatkowa chmura (API modelu, jego
  dostawca hostingu) dodaje ogniwo, które musi przejrzeć inspektor ochrony danych kupującego. Skrzynka na miejscu
  usuwa większość z nich.
  ([RODO, EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj))
- **Szczególne kategorie danych z art. 9** (zdrowie, dane biometryczne, przynależność do związków zawodowych,
  przekonania) wymagają wyraźnej podstawy prawnej. Dokumenty medyczne, kadrowe i ubezpieczeniowe są ich pełne.
  „To nigdy nie opuszcza kliniki" to najłatwiejsza odpowiedź dla IOD.
- **Transfery poza EOG** (rozdział V) wymagają decyzji o odpowiednim stopniu ochrony albo standardowych klauzul
  umownych wraz z oceną skutków transferu. Unijno-amerykańskie Ramy Ochrony Danych (Data Privacy Framework, przyjęte
  10.07.2023) nadal są podstawą transferów do USA, ale są pod presją: Data Protection Review Court stracił w styczniu
  2025 członków z ramienia Demokratów, a po wyroku Sądu Najwyższego USA *Trump v. Slaughter* (czerwiec 2026), który
  odebrał ochronę komisarzom FTC, noyb zwrócił się do Komisji o uchylenie tych ram i zapowiedział postępowanie
  sądowe ([podsumowanie z Wikipedii, odczytane 14.10.2026](https://en.wikipedia.org/wiki/EU%E2%80%93US_Data_Privacy_Framework)).
  Dla kupującego oznacza to: „Twoje dane trafiają do amerykańskiego API" niesie dziś realne ryzyko, że podstawa
  prawna zniknie w trakcie umowy, tak jak już dwa razy wcześniej (Safe Harbor 2015, Privacy Shield 2020).
- **Chiny** nie mają decyzji o odpowiednim stopniu ochrony. Wywoływanie API DeepSeek z Polski z danymi osobowymi to
  transfer z rozdziału V bez łatwej podstawy. Uruchamianie tych samych otwartych wag lokalnie w ogóle nie jest
  transferem. To jest sedno argumentu „najpierw lokalnie".

### Polska tajemnica zawodowa

Każdy z tych obowiązków ma charakter osobisty i jest egzekwowany karnie lub dyscyplinarnie, co sprawia, że kupujący jest
znacznie ostrożniejszy, niż wynikałoby z samego RODO. Linki prowadzą do tekstów jednolitych w ISAP.

| Zawód | Reguła tajemnicy | Co to oznacza dla dostawcy AI |
| --- | --- | --- |
| Adwokat | tajemnica adwokacka, [Prawo o adwokaturze art. 6](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19820160124) | Każdy zewnętrzny podmiot przetwarzający wymaga uzasadnienia; rozwiązanie na miejscu zdejmuje to pytanie |
| Radca prawny | tajemnica radcowska, [ustawa o radcach prawnych art. 3](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19820190145) | Ta sama logika co u adwokatów; kancelarie pytają, gdzie działa model |
| Lekarz | tajemnica lekarska, [ustawa o zawodach lekarza art. 40](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19970280152) | Dane pacjentów to również art. 9 RODO; przychodnie wolą w ogóle bez chmury |
| Doradca podatkowy | tajemnica doradcy podatkowego, [ustawa o doradztwie podatkowym art. 37](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19961020475) | Księgi klientów i korespondencja zostają w biurze |
| Administracja podatkowa | tajemnica skarbowa, [Ordynacja podatkowa art. 293](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19971370926) | Dane urzędu skarbowego nie mogą trafiać do komercyjnych chmur bez podstawy prawnej |

Prawo nie zakazuje chmurowej AI tym zawodom. Sprawia jednak, że zawodowiec osobiście odpowiada za każdy wyciek, więc
najtańszym sposobem na zamknięcie transakcji jest usunięcie chmury z rozmowy.

### Sektor publiczny

Polskie podmioty publiczne kupują w trybie zamówień publicznych i muszą przejść przegląd bezpieczeństwa oraz lokalizacji
danych. Państwo sfinansowało własną polską rodzinę modeli (PLLuM, patrz niżej) wprost „dla zastosowań w polskim sektorze
publicznym", za około 18,5 M PLN
([karta modelu PLLuM](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512)). Dostawca, który wdraża państwowo
sfinansowany otwarty model na serwerze samego urzędu, jest zgodny z tą polityką, a nie z nią walczy.

### Harmonogram unijnego AI Act (stan na październik 2026)

Z harmonogramu wdrażania AI Act, strona zaktualizowana 31.08.2026
([artificialintelligenceact.eu](https://artificialintelligenceact.eu/implementation-timeline/)):

| Data | Co obowiązuje |
| --- | --- |
| 02.02.2025 | Praktyki zakazane, obowiązek kompetencji w zakresie AI |
| 02.08.2025 | Zasady dla modeli AI ogólnego przeznaczenia, zarządzanie, kary |
| 02.12.2026 | Nowe zakazy dotyczące nieskonsensualnych intymnych obrazów i generowania CSAM |
| 02.12.2027 | Zasady dla systemów wysokiego ryzyka (rozdział III) dla systemów z załącznika III |
| 02.08.2028 | Zasady dla systemów wysokiego ryzyka z załącznika I (bezpieczeństwo produktów) |
| 02.08.2030 | Systemy wysokiego ryzyka organów publicznych muszą być zgodne z przepisami |

Termin 02.12.2027 dla załącznika III jest późniejszy niż pierwotny 02.08.2026. To przesunięcie wynika z odroczenia w
ramach Digital Omnibus; strona podaje nowe daty, ale w tym przebiegu nie znalazłem ostatecznego tekstu przyjętego aktu.
Praktyczne znaczenie: większość agentowych narzędzi zaplecza biurowego (redagowanie dokumentów, ekstrakcja, triaż)
nie jest wysokiego ryzyka, ale wszystko, co ocenia ludzi pod kątem kredytu, zatrudnienia lub dostępu do świadczeń
publicznych, należy do załącznika III. Masz czas do grudnia 2027, nie w nieskończoność.

### Popyt na suwerenność danych

Nie znalazłem datowanego, opartego na źródle badania popytu polskich lub unijnych kupujących na suwerenną lub lokalną
AI w tym przebiegu, więc ten rozdział nie twierdzi nic o jego skali. Traktuj to jako hipotezę do sprawdzenia w rozmowach
discovery: zapytaj każdego potencjalnego klienta „czy zaakceptowałby Pan/Pani chmurowe API, jeśli umowa będzie dobra?"
i zapisz odpowiedź. Liczby dotyczące adopcji są w [01-LUKI-ADOPCJI.md](01-LUKI-ADOPCJI.md).

## 2. Otwarte modele wystarczająco dobre już dziś

### Modele nastawione na polski

| Model | Najnowsza znaleziona wersja | Rozmiar | Licencja | Uwaga |
| --- | --- | --- | --- | --- |
| Bielik (SpeakLeash) | Bielik-11B-v3.0-Instruct, Bielik-Minitron-7B-v3.0-Instruct (aktualizacja lipiec 2026) | 11B, 7B | Apache 2.0 | „32 języki europejskie, zoptymalizowany pod polski"; raport techniczny grudzień 2025 |
| PLLuM (państwowe konsorcjum) | rodzina 2512 (grudzień 2025): PLLuM-4B, Llama-PLLuM-8B, PLLuM-12B (baza Mistral-Nemo), Llama-PLLuM-70B | od 4B do 70B | Apache 2.0 dla PLLuM-12B; modele oparte na Llamie dziedziczą warunki Llamy (sprawdź każdą kartę) | Dostrojony do zadań administracji publicznej |

Źródła: [SpeakLeash na Hugging Face](https://huggingface.co/speakleash),
[karta Bielik-11B-v3.0-Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct),
[CYFRAGOVPL na Hugging Face](https://huggingface.co/CYFRAGOVPL),
[karta PLLuM-12B-instruct-2512](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512), wszystkie odczytane 14.10.2026.

Benchmarki: [Open PL LLM Leaderboard](https://huggingface.co/spaces/speakleash/open_pl_llm_leaderboard) jest punktem
odniesienia, ale jego tabela nie załadowała się przy pobraniu 14.10.2026, więc nie podaję żadnych wyników. Zanim
obiecasz klientowi jakość po polsku, uruchom własny zestaw testowy 50 dokumentów z jego dziedziny na Bieliku, PLLuM i
jednym dużym modelu wielojęzycznym. Małe polskie modele (7-12B) są mocne w polskim stylu i krótkiej ekstrakcji, słabsze
w długim, wieloetapowym rozumowaniu; typowy wzorzec to duży model wielojęzyczny do rozumowania i polski model do
tekstu końcowego.

### Wielojęzyczne modele otwarte

| Rodzina | Co warto wiedzieć | Pułapka licencyjna |
| --- | --- | --- |
| gpt-oss-120b (OpenAI, sierpień 2025) | 117B łącznie, 5,1B aktywnych, mieści się na jednym GPU 80 GB w MXFP4 ([karta](https://huggingface.co/openai/gpt-oss-120b)) | Apache 2.0, nie znaleziono |
| Rodzina DeepSeek V4 | Czytelnik już uruchamia DeepSeek-V4-Flash lokalnie; istnieje też API ([cennik](https://api-docs.deepseek.com/quick_start/pricing)) | Sprawdź licencję dla dokładnie tych wag, które dostarczasz |
| Qwen, Mistral | Mocne wielojęzyczne, wiele rozmiarów na Apache 2.0 | Niektóre rozmiary mają licencje własne: sprawdź każdą kartę |
| Gemma (Google) | Dobre małe modele wielojęzyczne i wizyjne | Własne warunki (ostatnia zmiana 01.04.2026): ograniczenia użycia trzeba przekazać dalej klientom, a Google może „ograniczyć (zdalnie lub w inny sposób)" użycie ([warunki](https://ai.google.dev/gemma/terms)) |
| Llama 4 (Meta) | Popularna baza do fine-tuningu | Prawa do multimodalnej Llamy 4 „nie są przyznawane, jeśli jesteś osobą fizyczną mającą miejsce zamieszkania lub firmą z głównym miejscem prowadzenia działalności w Unii Europejskiej" ([polityka użycia](https://dev.meta.ai/llama/llama4/use-policy/)); użytkownicy końcowi produktu są wyłączeni z tego zakazu, ale Ty, jako polski budujący, nie |

Klauzula Llamy dotyczy tego czytelnika bezpośrednio: polski jednoosobowy przedsiębiorca (JDG) nie może budować na
multimodalnej Llamie 4. Dla wszystkiego, co instalujesz u klienta, wybieraj wagi na Apache 2.0 lub MIT.

### Mowa, obraz, embeddingi

- **Mowa na tekst:** Whisper large-v3-turbo, licencja MIT, 809M parametrów, 99 języków wraz z polskim, średni WER
  7,83 na testach z karty skoncentrowanych na angielskim; karta ostrzega, że dokładność jest nierówna między językami
  ([karta](https://huggingface.co/openai/whisper-large-v3-turbo)). Nie znaleziono WER specyficznego dla polskiego w
  tym przebiegu: mierz na własnych nagraniach rozmów klienta.
- **Wizja i OCR:** Polskie skany dokumentów (faktury, pisma sądowe, archiwa) wymagają modelu wizyjno-językowego albo
  klasycznego kroku OCR przed LLM. W tym przebiegu nie robiłem benchmarku kandydatów; warianty wizyjne Gemmy i Qwen to
  zwykłe otwarte opcje, z uwagami licencyjnymi powyżej.
- **Embeddingi:** do wyszukiwania w polskich dokumentach użyj wielojęzycznego modelu embeddingów z otwartą licencją i
  przetestuj recall na własnych zapytaniach klienta. W tym przebiegu nie sprawdzono żadnego polskiego benchmarku
  embeddingów.

## 3. Poziomy sprzętu na miejscu u klienta

Generowanie tokenów na jednej skrzynce jest w większości ograniczone przepustowością pamięci. Zgrubne górne ograniczenie
to `tokeny/s ≈ przepustowość ÷ bajty odczytane na token`, gdzie bajty na token ≈ parametry aktywne × bajty na wagę.
Model typu mixture-of-experts z około 5B parametrów aktywnych w 4 bitach (około 3 GB na token) jest więc znacznie
szybszy niż gęsty model 70B (około 40 GB na token). Kolumna z przepustowością to to oszacowanie, a nie pomiar.

| Poziom | Przykład (cena sprawdzona 14.10.2026) | Pamięć | Przepustowość | Co uruchamia (szacunek) |
| --- | --- | --- | --- | --- |
| Mini PC | Framework Desktop, Ryzen AI Max+ 395, 128 GB: zł 16 529 ([Framework](https://frame.work/products/desktop-diy-amd-aimax300)) | 128 GB zunifikowanej | 256 GB/s (specyfikacja) | MoE klasy gpt-oss-120b z dziesiątkami tokenów/s dla 1-2 użytkowników; gęsty 70B jest wolny |
| Kompaktowy NVIDIA | DGX Spark, GB10: nie znaleziono ceny na stronie producenta ([NVIDIA](https://www.nvidia.com/en-us/products/workstations/dgx-spark/)) | 128 GB zunifikowanej | 273 GB/s | Producent: do 200B parametrów do inferencji *(deklaracja dostawcy)*; prędkość podobna do mini PC; plusem jest stos CUDA |
| Mac Studio | M5 Max do 128 GB, M5 Ultra do 512 GB; cen w PLN nie pokazało pobranie ([Apple PL](https://www.apple.com/pl/mac-studio/)) | do 512 GB | 614 GB/s (Max), 1,2 TB/s (Ultra) | Ultra mieści największe otwarte modele MoE; dobra szybkość dla jednego użytkownika, słaby przy wielu równoległych |
| Stacja wielo-GPU | Maszyna czytelnika: 4x Radeon AI PRO R9700, 128 GB VRAM; aktualnej ceny nie znaleziono w tym przebiegu | 128 GB VRAM | na kartę GDDR6 | DeepSeek-V4-Flash z 4 równoległymi slotami dziś; najlepsza dla biura z 10-30 użytkownikami |
| Wynajęty GPU w UE | Hetzner GEX131, RTX PRO 6000 Blackwell 96 GB, w Niemczech lub Finlandii; ceny miesięcznej nie pokazało pobranie ([Hetzner](https://www.hetzner.com/dedicated-rootserver/gex131/)) | 96 GB VRAM | n/d | Poziom prywatnej chmury: serwer dedykowany, centrum danych w UE, Twoja umowa z kupującym |

Polskich opcji GPU w centrach danych (żeby dane zostawały w Polsce, a nie tylko w UE) nie wyceniono w tym przebiegu;
poproś polskich dostawców hostingu o ofertę na dedykowany GPU, zanim sprzedasz obietnicę „dane zostają w Polsce".

Zasady kciuka przy wyborze poziomu:
1. Jeden specjalista lub małe biuro, praca wsadowa w nocy: klasa mini PC lub DGX Spark (128 GB).
2. 10-30 równoczesnych użytkowników, czat plus potoki dokumentów: stacja wielo-GPU jak maszyna czytelnika.
3. Klient nie ma serwerowni albo nie chce sprzętu: dedykowany serwer GPU w UE, pod Twoją umową powierzenia.

## 4. Koszt: lokalnie a API

Założenia (podaj je też klientowi):
- Obciążenie: 50 M tokenów miesięcznie, 3 tokeny wejściowe na 1 wyjściowy.
- API: cena katalogowa DeepSeek-Flash z 14.10.2026, wejście bez trafienia w cache $0,15 poza szczytem / $0,30 w
  szczycie, wyjście $0,60 / $1,20 za 1 M tokenów ([cennik DeepSeek](https://api-docs.deepseek.com/quick_start/pricing)).
- Lokalnie: Framework Desktop 128 GB za zł 16 529, amortyzowany przez 36 miesięcy (około zł 460 miesięcznie), plus około
  110 kWh miesięcznie energii (średnio 150 W, 24/7) przy założonych zł 1,0 za kWh, czyli około zł 570 miesięcznie przed
  doliczeniem Twojego czasu.

| Pozycja | Koszt miesięczny |
| --- | --- |
| API, uśrednione poza szczytem (około $0,26 za 1 M tokenów) | około $13 |
| API, uśrednione w szczycie (około $0,53 za 1 M tokenów) | około $26 |
| Lokalny mini PC (sprzęt + energia, bez robocizny) | około zł 570 |

Uczciwy wynik: **wobec tanich modeli API lokalny sprzęt nie zwraca się na samych tokenach przy wolumenach małego
biura.** Przy założonym kursie 3,8 PLN za USD zł 570 to około $150, więc jedna skrzynka dorównuje API dopiero przy
około 300-600 M tokenów miesięcznie (ceny w szczycie i poza szczytem). To 115-230 tokenów na sekundę przez całą
dobę, więcej, niż utrzymuje mini PC ze 128 GB, i znacznie więcej, niż produkuje małe biuro. Lokalnie wygrywa się tylko wtedy, gdy:
- tanie API jest prawnie nieużywalne (dane osobowe do chińskiego lub amerykańskiego API, tajemnica zawodowa), więc
  prawdziwe porównanie to lokalnie kontra niezrobienie tego w ogóle albo kontra premium API hostowane w UE;
- porównanie dotyczy drogich cen modeli czołowych, a nie DeepSeek-Flash;
- miejsce jest offline albo ma zawodny internet (fabryki, archiwa, niektóre przychodnie).

Wyceniaj więc skrzynkę jako zgodność i kontrolę, a nie oszczędność. Własny kompromis czytelnika między modelami
lokalnymi a płatnymi omówiono w [../tanie-i-darmowe-modele/README.md](../tanie-i-darmowe-modele/README.md).

## 5. Wzorce wdrożenia

1. **Urządzenie na miejscu (on-prem).** Wstępnie skonfigurowana skrzynka (mini PC lub stacja robocza) z serwerem modelu,
   agentem, interfejsem webowym i lokalnym magazynem dokumentów. Sprzedawana jako opłata wdrożeniowa plus miesięczna
   licencja i wsparcie. Najlepsza dla kancelarii, doradców podatkowych, przychodni.
2. **Prywatna chmura w PL lub UE.** Dedykowany serwer GPU wynajmowany przez Ciebie lub klienta, jednodzierżawny, w
   centrum danych w UE, pod Twoją umową powierzenia. Najlepsza dla klientów bez serwerowni lub z wieloma lokalizacjami.
3. **Hybryda z lokalną redakcją.** Lokalny model znajduje i zastępuje imiona i nazwiska, numery PESEL i NIP, adresy oraz
   sygnatury spraw znacznikami zastępczymi, następnie trudne rozumowanie trafia do płatnego API, a odpowiedź jest
   ponownie identyfikowana lokalnie. Dane spseudonimizowane to nadal dane osobowe w rozumieniu RODO, więc to obniża
   ryzyko, ale nie usuwa pytania o transfer; powiedz o tym klientowi. Szczegóły wzorca:
   [../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md)
   oraz [../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md](../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md).
4. **Reguły routingu.** Zapisz je w załączniku do umowy:
   - dokumenty objęte tajemnicą zawodową lub dane z art. 9: tylko lokalnie;
   - tekst po redakcji, prawo publiczne, szablony: mogą trafiać do płatnego API;
   - wszystko ze skutkiem prawnym lub finansowym: człowiek zatwierdza, zanim opuści system.

**Prawdziwy przychód cykliczny** to nie marża na sprzęcie. To:
- aktualizacje modeli (nowe wersje Bielika lub PLLuM, ponowne uruchomienie zestawu testowego klienta przed każdą zmianą);
- monitoring (dysk, kondycja GPU, długość kolejki, nieudane zadania) z alertem do Ciebie, a nie do klienta;
- kopie zapasowe, łatki bezpieczeństwa i linia wsparcia;
- rozszerzanie agenta o kolejny workflow w tym samym biurze.

Utwardzanie bezpieczeństwa dla agentów czytających niezaufane dokumenty jest w
[../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md](../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md);
wybory harnessów są w [../harnessy-agentowe/README.md](../harnessy-agentowe/README.md).

## 6. Które okazje są najpierw lokalne

| Kategoria | Domyślnie | Dlaczego | Czy polski model otwarty wystarcza? |
| --- | --- | --- | --- |
| Prawo (adwokaci, radcy prawni) | Najpierw lokalnie | Tajemnica zawodowa, zaufanie klienta jest sprzedażą | Redagowanie i ekstrakcja tak, po testach; złożone rozumowanie prawne wymaga dużego modelu, trzymaj go lokalnie albo redaguj |
| Medycyna (przychodnie, gabinety) | Najpierw lokalnie | Dane z art. 9 plus tajemnica lekarska | Notatki i streszczenia tak; wszystko kliniczne wymaga akceptacji lekarza |
| Podatki i księgowość | Najpierw lokalnie lub hybryda | Tajemnica doradcy podatkowego; przepisy publiczne i stawki mogą iść do API | Tak dla dokumentów; liczby musi sprawdzać kod, a nie model |
| Sektor publiczny | Najpierw lokalnie | Zamówienia publiczne, lokalizacja danych, państwowo sfinansowany PLLuM | PLLuM jest do tego dostrojony; zweryfikuj na prawdziwych przypadkach |
| Własność intelektualna w produkcji | Najpierw lokalnie | Tajemnice przedsiębiorstwa, czasem obiekty offline | Język mniej istotny; wielojęzyczne modele wystarczą |
| Archiwa i digitalizacja | Najpierw lokalnie | Wolumen plus dane osobowe w starych aktach | Zależy od jakości OCR na starych skanach: najpierw przetestuj |
| Głos w MŚP (rozmowy, recepcja) | Hybryda | Potrzeba niskich opóźnień; nagrania to dane osobowe | STT klasy Whisper dla polskiego trzeba zmierzyć na prawdziwych rozmowach |
| E-commerce | API wystarczy | Dane produktowe są publiczne; wolumen sprzyja tanim API | Nie jest to tu argument sprzedażowy |

## 7. Ryzyka

- **Luki w jakości polskiego.** Małe polskie modele piszą dobrze po polsku, ale mogą gubić wieloetapowe rozumowanie;
  duże modele wielojęzyczne rozumują lepiej, ale piszą sztywniejszą polszczyzną. Bez zestawu testowego klienta
  zgadujesz. W tym przebiegu nie uchwycono żadnych aktualnych wyników rankingów.
- **Odpowiedzialność za halucynacje.** Błędny cytat w piśmie procesowym lub zła stawka podatku to w pierwszej
  kolejności odpowiedzialność zawodowca, a w drugiej Twoja, przez umowę. Ogranicz swoją odpowiedzialność, zachowaj
  bramkę zatwierdzenia przez człowieka i loguj każde źródło użyte przez agenta.
- **Ciężar wsparcia sprzętu.** Skrzynka u klienta to aktualizacje sterowników, padające dyski i telefony „przestało
  działać". Przy 1-3 osobach ogranicz liczbę urządzeń na inżyniera i pobieraj opłatę za wsparcie od pierwszego dnia.
  Stosy AMD ROCm wymagają większej troski niż CUDA; czytelnik wie to z maszyny z R9700.
- **Pułapki licencyjne.** Multimodalna Llama 4 wyklucza firmy z siedzibą w UE; warunki Gemmy wymagają przekazywania
  ograniczeń dalej i dopuszczają zdalne ograniczenie; warianty PLLuM oparte na Llamie dziedziczą warunki Llamy. Prowadź
  rejestr licencji dla każdego wdrożenia i preferuj wagi na Apache 2.0 lub MIT.
- **Dryf regulacyjny.** DPF może upaść, terminy AI Act dla wysokiego ryzyka już raz się przesunęły. Buduj tak, by klient
  mógł zmienić dostawcę API albo przejść w pełni na lokalne bez przepisywania.
- **Złudzenie kosztowe.** Nie sprzedawaj lokalnego jako tańszego za token; według powyższych liczb tak nie jest.
  Sprzedawaj je jako powód, dla którego projekt w ogóle może powstać.
