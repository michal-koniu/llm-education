# Asymetrie biznesowe AI

Gdzie adopcja AI jest wciąż na tyle niska, że mały zespół z aplikacjami agentowymi i **lokalnymi otwartymi modelami** może zbudować biznes, zanim dogonią go obecni gracze? Przyjrzałem się 26 kandydatom w Polsce, w UE i na rynkach globalnych: back-office'om, zawodom regulowanym, sektorowi publicznemu, terminom compliance, przemysłowi i operacjom MŚP. Przy każdym zadałem trzy pytania: **czy tę pracę wciąż robi się ręcznie, kto już sprzedaje tam AI i czy uruchamianie modelu lokalnie pomaga w sprzedaży?** Potem każdy pomysł atakowałem kontrą z pięciu stron, zanim dałem mu punkty.

Moja konfiguracja: lokalny zestaw z DeepSeek-V4-Flash-0731 (4 równoległe sloty), Claude Opus 5.5 jako planista i recenzent, tanie modele online na nadmiar zadań ([../tanie-i-darmowe-modele/README.md](../tanie-i-darmowe-modele/README.md)). Mieszkam w Polsce, mogę sprzedawać po polsku i po angielsku, zakładam małą firmę bez zewnętrznego finansowania (1-3 osoby, około 20 000 EUR). Fakty według stanu na 14.10.2026. Poprzedni kurs dotyczył zarobków bez zakładania firmy ([../asymetrie-zarobkowe-ai/README.md](../asymetrie-zarobkowe-ai/README.md)); ten jest o budowaniu firmy.

> **To nie jest porada inwestycyjna, prawna ani podatkowa.** Rynki, przepisy i funkcje dostawców zmieniają się co miesiąc. Sprawdź jeszcze raz, zanim zaczniesz działać.

## Krótka odpowiedź

- **Luka jest realna i mierzalna.** W 2025 roku AI stosowało 8,4% polskich przedsiębiorstw wobec 20,0% w UE, co daje przedostatnie miejsce po Rumunii (Eurostat). Polskie małe firmy: 5,8% (UE 17,0%); polskie budownictwo: 2,4% (UE 10,8%). Koszt zablokował 55,5% polskich firm, które rozważały AI ([01-LUKI-ADOPCJI.md](01-LUKI-ADOPCJI.md) zawiera pełne dane). Firmy, które wciąż robią tę pracę ręcznie, to klienci.
- **Najlepsze otwarcia są tam, gdzie dane nie mogą opuścić budynku.** Dziewięć z 15 najlepszych ma wysokie dopasowanie modeli lokalnych: kancelarie prawne, urzędy gmin, kliniki, dokumenty bezpieczeństwa NIS2, kod źródłowy legacy, rysunki maszyn, archiwa. Tu argumentem sprzedażowym, a nie szczegółem technicznym, jest „działa na urządzeniu w twoim biurze, na polskim modelu na licencji Apache".
- **Lokalnie nie wygrywa się kosztem tokenów, tylko sprzedażą.** Przy cenach z października 2026 tanie API jest tańsze za token niż lokalne urządzenie przy większości wolumenów MŚP ([03-NAJPIERW-LOKALNIE.md](03-NAJPIERW-LOKALNIE.md)). Pieniądze są we wdrożeniu, przepływach pracy, aktualizacjach i wsparciu, wycenianych za biuro lub za podmiot.
- **Terminy w kalendarzu tworzą budżety.** NIS2 w Polsce (nowelizacja KSC w mocy od 3.04.2026, obowiązki do 3.04.2027), rozporządzenie maszynowe (20.01.2027), e-fakturowanie KSeF (2026) i przejście MDR zmuszają firmy do kupowania pomocy już teraz.
- **Polskie prawo i język to fosa, ale cienka.** Zasady przetargowe (Pzp), normy kosztorysowe KNR, pisma sądowe EPU i polska poczta e-mail to miejsca, do których globalne narzędzia AI jeszcze nie dotarły. Polscy obecni gracze ruszają: SaldeoSMART klasyfikuje faktury KSeF z użyciem AI, Noa od Docplanner pisze notatki lekarskie, Gaius-Lex sprzedaje prywatne AI prawnicze, LEX dołącza czat AI. Okno to 12-24 miesiące, nie wieczność.
- **Żaden pomysł nie dostał więcej niż 72 punkty na 100.** Każdy przetrwał kontrę tylko w węższej formie: jeden zawód, dwa lub trzy przepływy pracy, sprzedaż przez partnera, który już ma klientów.

## 15 najlepszych

Wynik w skali do 100. Konkurencja oznacza, jak zatłoczona jest dziś strona AI na danym rynku; dopasowanie modeli lokalnych oznacza, jak bardzo uruchamianie otwartych modeli na miejscu pomaga w sprzedaży.

| # | Okazja | Wynik | Region | Konkurencja | Dopasowanie modeli lokalnych |
|---|---|---|---|---|---|
| 1 | [Prywatne pudełko AI dla polskich biur profesjonalnych](02-OKAZJE.md#1-prywatne-pudełko-ai-dla-polskich-biur-profesjonalnych) | 72 | PL, potem UE | średnia | wysokie |
| 2 | [Lokalny agent dokumentowy dla polskich urzędów gmin](02-OKAZJE.md#2-lokalny-agent-dokumentowy-dla-polskich-urzędów-gmin) | 71 | PL | niska | wysokie |
| 3 | [Agent dokumentacji zgodności z NIS2 / KSC dla nowo objętych podmiotów w Polsce](02-OKAZJE.md#3-agent-dokumentacji-zgodności-z-nis2--ksc-dla-nowo-objętych-podmiotów-w-polsce) | 71 | PL (potem Europa Środkowo-Wschodnia) | średnia | wysokie |
| 4 | [Dokumentowanie i modernizacja kodu legacy on-prem dla MŚP i firm regulowanych](02-OKAZJE.md#4-dokumentowanie-i-modernizacja-kodu-legacy-on-prem-dla-mśp-i-firm-regulowanych) | 70 | PL / UE | średnia | wysokie |
| 5 | [Asystent przetargowy dla polskich MŚP startujących w przetargach](02-OKAZJE.md#5-asystent-przetargowy-dla-polskich-mśp-startujących-w-przetargach) | 70 | najpierw PL, potem UE (TED) | średnia | średnie |
| 6 | [Lokalny asystent prawny dla małych polskich kancelarii](02-OKAZJE.md#6-lokalny-asystent-prawny-dla-małych-polskich-kancelarii) | 67 | PL | średnia | wysokie |
| 7 | [Agent back-office'u spedycyjnego dla polskich małych spedytorów](02-OKAZJE.md#7-agent-back-officeu-spedycyjnego-dla-polskich-małych-spedytorów) | 67 | PL (potem UE) | średnia | średnie |
| 8 | [Agent wiedzy o utrzymaniu ruchu i serwisie terenowym on-prem dla przemysłowych MŚP w Europie Środkowo-Wschodniej](02-OKAZJE.md#8-agent-wiedzy-o-utrzymaniu-ruchu-i-serwisie-terenowym-on-prem-dla-przemysłowych-mśp-w-europie-środkowo-wschodniej) | 66 | PL / UE (Europa Środkowo-Wschodnia) | średnia | wysokie |
| 9 | [Agent back-office KSeF dla polskich biur rachunkowych](02-OKAZJE.md#9-agent-back-office-ksef-dla-polskich-biur-rachunkowych) | 65 | PL | wysoka | wysokie |
| 10 | [Agent do należności i dokumentów EPU dla polskich MŚP](02-OKAZJE.md#10-agent-do-należności-i-dokumentów-epu-dla-polskich-mśp) | 64 | PL | średnia | średnie |
| 11 | [Agent dokumentacji technicznej CE dla małych producentów maszyn i wyrobów](02-OKAZJE.md#11-agent-dokumentacji-technicznej-ce-dla-małych-producentów-maszyn-i-wyrobów) | 63 | PL (potem UE) | średnia | wysokie |
| 12 | [Asystent kosztorysowy i przetargowy dla polskich wykonawców budowlanych](02-OKAZJE.md#12-asystent-kosztorysowy-i-przetargowy-dla-polskich-wykonawców-budowlanych) | 63 | PL | średnia | średnie |
| 13 | [Lokalny polski skryba medyczny dla prywatnych klinik](02-OKAZJE.md#13-lokalny-polski-skryba-medyczny-dla-prywatnych-klinik) | 61 | PL | średnia | wysokie |
| 14 | [Digitalizacja i wyszukiwanie w papierowych archiwach na miejscu](02-OKAZJE.md#14-digitalizacja-i-wyszukiwanie-w-papierowych-archiwach-na-miejscu) | 60 | PL / UE | średnia | wysokie |
| 15 | [Agent dokumentacji regulacyjnej dla małych firm medtech i farmaceutycznych (dokumentacje techniczne MDR/IVDR, PSUR-y, selekcja literatury)](02-OKAZJE.md#15-agent-dokumentacji-regulacyjnej-dla-małych-firm-medtech-i-farmaceutycznych-dokumentacje-techniczne-mdrivdr-psur-y-selekcja-literatury) | 60 | UE | średnia-wysoka | średnie |

Następne w kolejce, poniżej progu, ale w pełni opisane:

| # | Okazja | Wynik | Region | Konkurencja | Dopasowanie modeli lokalnych |
|---|---|---|---|---|---|
| 16 | [Polski agent telefoniczny i czatowy dla lokalnych firm usługowych](02-OKAZJE.md#16-polski-agent-telefoniczny-i-czatowy-dla-lokalnych-firm-usługowych) | 59 | PL | wysoka | niskie |
| 17 | [Współpilot do wniosków o dotacje dla polskich firm doradczych](02-OKAZJE.md#17-współpilot-do-wniosków-o-dotacje-dla-polskich-firm-doradczych) | 58 | PL | średnia | średnie |
| 18 | [Agent badawczy do polskich interpretacji podatkowych i orzecznictwa](02-OKAZJE.md#18-agent-badawczy-do-polskich-interpretacji-podatkowych-i-orzecznictwa) | 52 | PL | wysoka | wysokie |

**Jak czytać ranking.** Wyniki są blisko siebie: od 60 do 72 w pierwszej piętnastce. Traktuj listę jako trzy grupy, a nie ścisłą kolejność.

| Grupa | Okazje | Dlaczego tworzą klaster |
|---|---|---|
| Najpierw lokalnie z mocy prawa lub tajemnicy | 1, 2, 4, 6, 8, 13, 14 | Dane nie mogą trafić do chmury w USA ani w Chinach; argumentem są otwarte modele na miejscu |
| Compliance napędzane terminem | 3, 9, 11, 15 | Datowany obowiązek prawny tworzy budżet teraz; okno zamyka się po terminie |
| Fosy polskiego prawa i języka | 5, 7, 10, 12 | Globalne narzędzia AI nie znają Pzp, KNR, EPU ani polskiej poczty spedycyjnej; lokalni gracze sprzedają wyszukiwanie, a nie agentów |

## Jak punktowałem

| Litera | Co mierzy | Punkty |
|---|---|---|
| M | Rynek: liczba kupujących w PL/UE, ile dziś płacą za pracę ręczną, gotowość do zapłaty | 20 |
| G | Luka adopcji: zmierzone niskie użycie AI w sektorze, klasie wielkości lub kraju oraz udział pracy ręcznej | 20 |
| C | Miejsce wśród konkurentów: wyższy wynik oznacza mniej wiarygodnych konkurentów AI i wolnych obecnych graczy | 15 |
| L | Dopasowanie modeli lokalnych: tajemnica prawna, RODO, koszt wolumenu lub obiekty offline sprawiają, że lokalne otwarte modele są atutem sprzedażowym, a modele są wystarczająco dobre w wymaganym języku | 15 |
| F | Wykonalność dla mnie: czas do MVP, dostęp do wiedzy dziedzinowej, cykl sprzedaży, kapitał | 15 |
| R | Trwałość i ryzyko: wyższy wynik oznacza, że przewaga utrzyma się ponad 2 lata, a odpowiedzialność jest do opanowania | 15 |

Remisy rozstrzygam według L (dopasowanie lokalne), potem G. Każdy profil pokazuje swoje oceny literowe, więc możesz zmienić wagi.

## Kontra dla całej piętnastki

Każdy profil argumentuje przeciwko sobie z pięciu stron. Te same zarzuty wracały raz po raz:

| Strona | Powtarzający się zarzut | Co przetrwa |
|---|---|---|
| Klient | „Już płacimy za LEX / Saldeo / naszego dostawcę EZD; po co kolejne narzędzie?" | Sprzedawaj dodatek zasilający system, którego już używają, a nie zamiennik |
| Obecny gracz | Polscy obecni gracze wdrażają AI w 2026 roku (SaldeoSMART, Noa, Gaius-Lex, czat AI w LEX) | Idź tam, gdzie nie mają jeszcze AI (dostawcy EZD, kosztorysowanie KNR, portale przetargowe) albo poniżej ich ceny |
| Czołowe laboratoria i big tech | Ogólny model czatowy już pisze tekst | Wartość tkwi we wczytywaniu danych, polskich regułach, listach kontrolnych, integracji i bramce z udziałem człowieka, a nie w szkicu |
| Regulator | Praca prawnicza, medyczna, CE i regulacyjna wiąże się z odpowiedzialnością; narzędzia medyczne mogą podpadać pod MDR | Niech wszystko podpisuje wskazany człowiek; zakres określaj jako „wsparcie dokumentacji", nigdy jako poradę |
| Ekonomia jednostkowa | Lokalne urządzenia kosztują więcej za token niż tanie API; wsparcie zjada marżę | Wyceniaj za biuro lub podmiot rocznie, standaryzuj jeden obraz urządzenia, sprzedawaj przez partnerów (MSP, integratorów, izby adwokackie, biura rachunkowe) |

**Dopasowanie założyciela to ukryty filtr.** Jako inżynier DevOps sam potrafię zbudować urządzenie, wdrożenie i warstwę bezpieczeństwa. Okazje 1, 3 i 4 pasują bezpośrednio do mojego doświadczenia; większość pozostałych wymaga partnera dziedzinowego (kosztorysanta, doradcy podatkowego, konsultanta regulacyjnego, spedytora) od pierwszego dnia.

## Od czego bym zaczął

1. **Zbudowałbym jeden lokalny stos** ([03-NAJPIERW-LOKALNIE.md](03-NAJPIERW-LOKALNIE.md)): instalowalny obraz urządzenia z otwartym modelem znającym polski, wczytywaniem dokumentów, uruchamiaczem agentów i dziennikiem audytu, a do tego hybrydową trasę, która lokalnie redaguje dane przed każdym wywołaniem płatnego API ([../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md)).
2. **Skierowałbym go na dwie branże z terminem lub regułą tajemnicy:** dokumentację NIS2 sprzedawaną w białej etykiecie przez MSP (termin 3.04.2027) oraz „rentgen" kodu legacy sprzedawany przez polskie software house'y. Obie pasują do moich umiejętności.
3. **Porozmawiałbym z 10 kupującymi, zanim napiszę przepływy pracy.** Każdy profil ma część „Jak zacząć" i kryterium przerwania; skorzystaj z nich.
4. **Trzymałbym w gotowości trzecią opcję:** przetargi publiczne lub urzędy gmin, przez integratora, który już im sprzedaje.

## Pomysły, które nie przetrwały

| Kandydat | Dlaczego odpadł |
|---|---|
| Back-office wspólnot mieszkaniowych i zarządców nieruchomości | Wielu drobnych kupujących na zakorzenionym oprogramowaniu; wymaga partnera dziedzinowego |
| Badanie prawne nieruchomości z ksiąg wieczystych | Dane publiczne, więc modele lokalne dodają niewiele; raporty z ksiąg już sprzedają się po 12-35 PLN |
| Papierkowa robota przy dopłatach rolniczych | Agencja wstępnie wypełnia formularze, a doradcy ODR pomagają za darmo; niska gotowość do zapłaty |
| Back-office niemieckiego doradcy podatkowego | DATEV dominuje, a sprzedaż tam wymaga sprzedaży po niemiecku |
| Dokumentacja cen transferowych | Niewielu kupujących, odpowiedzialność trzymają Wielka Czwórka, dane benchmarkowe są płatne |
| Raportowanie CBAM i EUDR | Uproszczenie z 2025 roku (próg 50 t) wyeliminowało większość importerów z sektora MŚP; EUDR znów opóźnione |
| Audyty European Accessibility Act | Nasycony rynek audytów, mikroprzedsiębiorstwa wyłączone, brak przewagi modeli lokalnych |
| Oferty na rynkach międzynarodowych | Nasycone, to nie luka adopcji; API czołowych modeli wygrywają w wielojęzycznych tekstach |

Pełne notatki ze źródłami są na końcu [02-OKAZJE.md](02-OKAZJE.md).

## Pliki

| Plik | Co zawiera |
|---|---|
| [01-LUKI-ADOPCJI.md](01-LUKI-ADOPCJI.md) | Dane: adopcja AI według kraju UE, wielkości firmy i sektora, Polska szczegółowo, porównanie globalne, bariery, gdzie AI jest już nasycone |
| [02-OKAZJE.md](02-OKAZJE.md) | 18 profili: asymetria, kupujący, aplikacja agentowa, podział lokalny i płatny, tabela konkurencji, kontra z pięciu stron, liczby, jak zacząć, kiedy przerwać; potem odrzucone pomysły |
| [03-NAJPIERW-LOKALNIE.md](03-NAJPIERW-LOKALNIE.md) | Dlaczego kupujący chcą lokalnie, otwarte modele wystarczająco dobre dziś, poziomy sprzętu, koszt a API, wzorce wdrożenia, które okazje są „najpierw lokalnie" |
| [ZRODLA.md](ZRODLA.md) | Wszystkie źródła, sprawdzone 14.10.2026 |

**Ograniczenia badania.** Budżet na wyszukiwanie w sieci w tej sesji skończył się wcześnie, więc badanie opiera się na stronach pobranych bezpośrednio: Eurostat, polskie akty prawne (ISAP i API ELI Sejmu), strony UE i witryny dostawców. Kilka liczb oznaczono „nie znaleziono" zamiast zgadywać, na przykład liczbę polskich biur rachunkowych i kancelarii oraz ceny kilku polskich obecnych graczy. Tabele konkurencji wymieniają prawdziwe firmy, ale głębokość AI i ceny podano tylko tam, gdzie potwierdza je źródło. Powiązane kursy: [../harnessy-agentowe/README.md](../harnessy-agentowe/README.md), [../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md](../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md).
