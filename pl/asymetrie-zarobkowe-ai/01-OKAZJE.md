# 10 najlepszych okazji, profil po profilu

Każdy profil ma ten sam układ: skąd płyną pieniądze, gdzie jest asymetria, co robi agent, jak praca dzieli się między
mój serwer a płatne API, prawdziwe liczby, jak zacząć, zasady i podatki, ograniczenia oraz tygodniowy test z
kryteriami przerwania. Stan na 14.10.2026. Punktacja (E zarobki 25, A asymetria 25, F wykonalność 15, L prawo i
regulaminy 20, R ryzyko 15) jest opisana w [README](README.md#jak-punktowałem). Profile 11-15 to kandydaci tuż pod kreską; odrzuceni kandydaci są na końcu.

**Traktuj liczby jak medianę, nie obietnicę.** Każda platforma tutaj ma długi ogon: nieliczni zarabiają dużo,
większość mało. Moje agenty przesuwają mnie w górę tego ogona tylko wtedy, gdy uczciwie mierzę wyniki
([02-ARCHITEKTURA-HYBRYDOWA.md](02-ARCHITEKTURA-HYBRYDOWA.md) pokazuje rejestr, którego używam).

---

## 1. Odzyskiwanie pieniędzy, które już mi się należą

**Kategoria:** roszczenia · **Realny dochód:** 20-80 USD/miesiąc uśrednione w skali roku (jedno lub dwa odszkodowania lotnicze plus kilka zwrotów) · **Potrzebny kapitał:** 0 USD · **Wynik: 57** (E3 A6 F14 L20 R14) · **Zasady:** roszczenia składasz sam, więc żadna zasada platformy dotycząca automatyzacji nie ma zastosowania; legalne w Polsce: tak (wyłącznie dla własnych roszczeń)

> Agent, który śledzi moje własne rezerwacje, paragony i formularze podatkowe oraz składa roszczenia, do których mam prawo, jest w pełni legalny i prawie bez ryzyka, ale roczna wartość jest niewielka, więc to raczej pożyteczny nawyk niż źródło dochodu.

**Skąd płyną pieniądze.** Linie lotnicze wypłacają pasażerowi odszkodowanie z EU261 przelewem bankowym po pisemnym wniosku; sklepy i producenci zwracają pieniądze lub wymieniają towar w ramach gwarancji lub gwarancji ceny; urząd skarbowy zwraca nadpłacony PIT po złożeniu korekty zeznania. Robiąc to samodzielnie, unikasz prowizji, którą zatrzymują firmy odszkodowawcze. Składanie roszczeń w imieniu innych osób to działalność regulowana i wykracza poza zakres tego opracowania.

**Asymetria.** Większość ludzi nigdy nie składa roszczeń: nie znają przepisów, gubią paragony albo poddają się po pierwszej odmowie linii lotniczej. Formalności to czysta praca z tekstem (znaleźć rezerwację, sprawdzić opóźnienie, powołać się na artykuł, napisać pismo, ponowić po 2 miesiącach), którą agent wykonuje w kilka minut. Okno się nie zamyka: prawa wynikają z prawa UE. Przewaga polega na tym, że zatrzymujesz 100% zamiast płacić firmie odszkodowawczej.

**Co robi agent.**
1. Obserwacja: czyta dedykowany folder skrzynki pocztowej lub wyeksportowane potwierdzenia rezerwacji i paragony (tylko lokalnie).
2. Filtrowanie: dla każdego lotu sprawdza opóźnienie przylotu o 3+ godziny lub odwołanie zgłoszone z wyprzedzeniem krótszym niż 14 dni; dla zakupów oznacza okresy gwarancji i spadki cen.
3. Praca: przygotowuje projekt pisma z roszczeniem, powołując się na art. 7 rozporządzenia 261/2004 i właściwą kwotę zależną od odległości.
4. Weryfikacja: płatny model ocenia ryzyko „nadzwyczajnych okoliczności” i sprawdza pismo.
5. Złożenie: BRAMKA CZŁOWIEKA. Każde roszczenie czytam i wysyłam sam; agent pilnuje terminów i po 2 miesiącach przygotowuje projekt eskalacji do krajowego organu.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na rigu) | Płatne API | Dlaczego |
|---|---|---|---|
| Parsowanie rezerwacji, paragonów, danych PIT | wszystko | nic | dane osobowe zostają na rigu |
| Sprawdzenie uprawnień | reguły plus model | Opus 5.5 w przypadkach granicznych | ocena nadzwyczajnych okoliczności wymaga osądu |
| Pisanie pism | projekt | końcowe szlify | jasne pisma szybciej kończą się wypłatą |
| Pilnowanie terminów | harmonogram | nic | deterministyczne |

**Liczby.**
- Odszkodowanie z EU261: 250 EUR do 1500 km, 400 EUR dla 1500-3500 km, 600 EUR powyżej 3500 km, przy przylocie spóźnionym o 3+ godziny lub odwołaniu z wyprzedzeniem krótszym niż 14 dni; nie przysługuje w nadzwyczajnych okolicznościach; problemy techniczne i strajki własnego personelu linii zwykle nie są uznawane za nadzwyczajne, więc odszkodowanie nadal się należy *(Your Europe, UE, 10.2026)*.
- Procedura: pisemne roszczenie do linii lotniczej, odczekanie 2 miesięcy, potem krajowy organ egzekwujący albo ADR/postępowanie w sprawach drobnych roszczeń *(Your Europe, 10.2026)*.
- Przy kursie 4,38 PLN/EUR *(NBP, 13.10.2026)* jedno roszczenie za lot krótkodystansowy to około 1095 PLN.
- Stawki prowizji firm odszkodowawczych: nie znaleziono w chwili pisania (strony firm zablokowane).
- Nieodebrane środki i ugody z pozwów zbiorowych dostępne dla rezydentów Polski: nie znaleziono wiarygodnego zestawienia; traktuj je jako okazjonalne niespodziewane wpływy.

**Jak zacząć.**
1. Wyeksportuj rezerwacje lotów i potwierdzenia zamówień z ostatnich 3 lat do lokalnego folderu.
2. Zbuduj parser i moduł sprawdzania uprawnień; najpierw uruchom go na przeszłych lotach (terminy przedawnienia roszczeń zależą od prawa krajowego sądu; przed złożeniem sprawdź polskie terminy).
3. Dodaj coroczny krok z listą kontrolną PIT: wypisz ulgi, które mogłem pominąć, i sprawdź każdą na podatki.gov.pl przed złożeniem korekty.
4. Pierwszy cel: najstarszy kwalifikujący się opóźniony lot, który wciąż mieści się w terminie.

**Zasady, podatki i ryzyka.**
- Składanie własnych roszczeń nie wymaga żadnej licencji; działanie za wynagrodzeniem w imieniu innych to działalność regulowana.
- Podatek: odszkodowanie z EU261 jest zasadniczo traktowane jako odszkodowanie, a nie dochód, a zwroty nie są dochodem; potwierdź w rozdziale o zasadach.
- Ryzyka: prawie żadne; linie lotnicze mogą odmówić, powołując się na nadzwyczajne okoliczności, co może wymagać eskalacji.
- Prywatność: dane z rezerwacji i dane podatkowe muszą zostać lokalnie.

**Ograniczenia.**
- Wartość zależy od tego, ile latasz i kupujesz; ktoś, kto nie podróżuje, dostaje blisko zera.
- Linie lotnicze często najpierw odmawiają; eskalacja trwa miesiącami.
- Ulgi podatkowe odlicza się raz w roku i tylko wtedy, gdy naprawdę ci przysługują.
- Brak efektu skali: nie da się wyjść poza własne życie.

**Test pierwszego tygodnia.** Uruchom moduł sprawdzający na 3 latach rezerwacji i paragonów. Test zaliczony, jeśli znajdzie co najmniej jedno roszczenie warte 250 EUR lub więcej, które wciąż mieści się w terminie; wyślij je.

**Kiedy przerwać.** W zaległościach nie znaleziono nic kwalifikującego się; wtedy zostaw tylko coroczne sprawdzenie PIT.

**Źródła:** [Your Europe: prawa pasażerów linii lotniczych](https://europa.eu/youreurope/citizens/travel/passenger-rights/air/index_en.htm) · [Rozporządzenie 261/2004](https://eur-lex.europa.eu/eli/reg/2004/261/oj/eng) · [Wyszukiwarka polskich ulg PIT](https://www.podatki.gov.pl/pit/ulgi-odliczenia-i-zwolnienia/) · [Kurs EUR w NBP](https://api.nbp.pl/api/exchangerates/rates/a/eur/?format=json)

---

## 2. Zlecenia freelance za zadanie (Upwork, Fiverr, Useme)

**Kategoria:** praca płatna · **Realny dochód:** 0-300 USD/mies. w miesiącach 1-2, mediana 200-800 USD/mies., gdy profil ma już opinie · **Potrzebny kapitał:** ~0-50 USD (Connects na Upwork) · **Wynik: 56** (E8 A9 F12 L16 R11) · **Zasady:** praca wspierana przez AI dozwolona (klient kupuje wynik; trzeba respektować poufność i każde polecenie klienta „bez AI”); legalne w Polsce: tak (Useme wystawia fakturę za ciebie bez firmy)

> Sprzedaż małych zadań za stałą cenę (konwersja dokumentów, czyszczenie danych, automatyzacja Excela/Arkuszy, scraping do celów badawczych, skrypty DevOps), w których agent robi 80% pracy, a ty ją sprawdzasz; to realny, ale kurczący się i konkurencyjny rynek, więc jest to kandydat ze środka tabeli, a nie żyła złota.

**Skąd płyną pieniądze.** Klient publikuje zadanie albo kupuje usługę (gig), wpłaca pieniądze na escrow, ty dostarczasz,
a platforma zwalnia pieniądze pomniejszone o swoją prowizję. Upwork: zmienna opłata serwisowa 0-15% od kontraktu, ustalana w momencie składania oferty; Connects
kosztują 0,15 USD za sztukę, 10 darmowych miesięcznie, standardowe zlecenia to 2-6 Connects za ofertę (2026). Fiverr pobiera od sprzedawcy prowizję
od każdego zamówienia (klasycznie 20%; nie zweryfikowano ponownie, zob. Liczby). Useme (Polska) wystawia fakturę klientowi i płaci
tobie na podstawie umowy (umowa o dzieło / zlecenie), więc firma nie jest potrzebna. Wypłata: z Upwork na PayPal (bezpłatnie po stronie Upwork)
lub przelewem (30 USD); z Useme na polskie konto bankowe.

**Asymetria.** Klienci wciąż płacą za zadanie za pracę, która dla agenta jest mechaniczna: PDF/skan do ustrukturyzowanego
Excela, deduplikacja eksportu z CRM, napisanie skryptu Google Apps Script, poprawka w bash/Terraform, jednorazowy scraper publicznych
stron. Haczyk: klienci też mają już ChatGPT, więc najprostsze zadania znikają. Upwork podał 763 000 aktywnych
klientów w czerwcu 2026, mniej niż we wcześniejszych okresach, oraz spadki przychodów i wolumenu usług brutto w II kw. 2026; w maju 2026 zwolnił
25% pracowników *(podsumowanie raportów spółki w Wikipedii)*. Przewagą nie jest „używanie AI” (wielu sprzedawców już to robi),
lecz dostarczanie zweryfikowanego, przetestowanego wyniku w kilka godzin przy zadaniach z chaotycznymi, prawdziwymi danymi, przy których własna próba klienta z chatbotem się nie powiodła.
Okno zawęża się dla zadań tekstowych; jest szersze dla zadań typu „chaotyczne dane plus kod plus weryfikacja”.

**Co robi agent.**
1. Obserwacja: odpytuje kanały ze zleceniami (zapisane wyszukiwania/RSS na Upwork, gdzie są dostępne, listy zleceń na Useme) w docelowych kategoriach co 30 min.
2. Filtrowanie: lokalny model ocenia każde ogłoszenie (jasny rezultat? budżet na godzinę pracy agenta + przeglądu? dane, które wolno ci przetwarzać?
   sygnały ostrzegawcze, takie jak „darmowe zadanie testowe” albo płatność poza platformą). Zostawia 3-5 najlepszych dziennie.
3. Szkic: płatny model pisze krótką, konkretną ofertę plus 3-wierszowy plan; **bramka akceptacji przez człowieka**: wysyłasz ją sam
   (Connects to pieniądze; nigdy nie aplikuj automatycznie).
4. Praca: agent konwertuje/czyści/pisze skrypty na maszynie; dane klienta zostają lokalnie, chyba że klient zgodził się na przetwarzanie w chmurze.
5. Weryfikacja: automatyczne kontrole (liczba wierszy, schemat, porównanie próbki, testy jednostkowe skryptów), potem przegląd płatnym modelem.
6. Dostarczenie: **bramka człowieka**: czytasz diff/raport, dostarczasz i sam odpowiadasz na wiadomości.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na maszynie) | Płatne API | Dlaczego |
|---|---|---|---|
| Obserwacja kanałów i ocena | tak, klasyfikacja każdego ogłoszenia 24/7 | nie | duży wolumen, niska trudność |
| Szkic oferty | pierwsza wersja | końcowa redakcja tonu i poprawności | oferty decydują o skuteczności |
| Czyszczenie danych, konwersja | tak, wszystkie masowe przekształcenia | nie | dane klienta zostają prywatne, długie pliki |
| Generowanie skryptów lub kodu | pierwsza wersja i przebiegi testowe | przegląd trudnej logiki | jakość tam, gdzie błędy kosztują opinie |
| Końcowa kontrola jakości | sprawdzenie listy kontrolnej | przegląd rezultatu przez Opus | jedna zła opinia szkodzi nowemu profilowi |

**Liczby.**
- Opłata serwisowa Upwork zmienna 0-15%, Connect 0,15 USD, 10 darmowych/mies., 2-6 Connects na standardową ofertę (2026, golance.com i strona zasobów Upwork, zweryfikowano 27.05.2026).
- Freelancer Plus 19,99 USD/mies. z 100 Connects w cenie (2026, podsumowanie cennika Upwork).
- Wypłata z Upwork: przelew 30 USD, PayPal bezpłatnie po stronie Upwork (27.05.2026, golance.com).
- Upwork: 763 000 aktywnych klientów w czerwcu 2026; zwolnienie 25% pracowników w maju 2026; spadki w II kw. 2026 (Wikipedia, odczyt 14.10.2026).
- Opłata kupującego na Fiverr ok. 5,5% + 2,50 USD za zamówienie (2026, golance.com). Prowizja sprzedawcy na Fiverr: nie zweryfikowano ponownie (oficjalna strona regulaminu zwróciła 403 w dniu 14.10.2026).
- Poziom prowizji Useme: nie znaleziono (strona cennika zwróciła 403 w dniu 14.10.2026).
- Skuteczność ofert dla nowych profili: nie znaleziono w dostępnym źródle.

**Jak zacząć.**
1. Wybierz 2 wąskie oferty, które da się zweryfikować automatycznie: „chaotyczny Excel/CSV/PDF w czysty zbiór danych w 24 h” oraz „mały skrypt DevOps/automatyzacji z testami”.
2. Załóż konto na Useme (polscy klienci, bez firmy) i profil na Upwork; przejdź weryfikację tożsamości.
3. Najpierw zbuduj agenta oceniającego zlecenia (tylko odczyt, bez automatycznego aplikowania); loguj każde ogłoszenie i jego ocenę.
4. Przygotuj 2 próbki do portfolio na danych publicznych/syntetycznych, pokazujące stan przed/po i raport z testów.
5. Przez 2 tygodnie wysyłaj 3-5 ręcznie zatwierdzonych ofert dziennie; pierwsze zlecenia bierz po niskiej stałej cenie, żeby zdobyć opinie.

**Zasady, podatki i ryzyka.**
- Zasady platform: automatyczne wysyłanie ofert i scraping samej platformy są zwykle sprzeczne z regulaminami marketplace'ów; trzymaj agenta przy pracy, nie przy koncie na platformie. Respektuj wyraźne polecenie klienta „bez AI” lub dotyczące poufności (oraz NDA) i nie wklejaj danych klienta do zewnętrznych API bez zgody; lokalny model eliminuje większość tego problemu.
- Polskie prawo: przez Useme dostajesz zapłatę na podstawie umowy cywilnoprawnej (oni zajmują się fakturowaniem). Bezpośrednio z Upwork/Fiverr bez firmy sam wykazujesz dochód jako przychód z innych źródeł albo w ramach działalności nierejestrowanej, jeśli mieścisz się w limicie; sprawdź 03-ZASADY-PODATKI-RYZYKA.
- Podatek w jednym zdaniu: progresywny PIT (12%/32%) od dochodu z Useme/zagranicznych platform, rozliczany w zeznaniu rocznym; szczegóły w rozdziale o zasadach.
- Ryzyka: nieopłacony czas na oferty, zła opinia na początku, rozrastający się zakres prac, klienci oczekujący darmowych poprawek.

**Ograniczenia.**
- Twój czas (wiadomości, poprawki) ogranicza wolumen do może 3-6 małych zleceń tygodniowo przy 10 h.
- Popyt na najłatwiejsze zadania wykonalne przez AI spada, bo klienci obsługują się sami chatbotami.
- Wielu konkurencyjnych sprzedawców już używa ChatGPT; asymetria leży w weryfikacji i szybkości, a nie w dostępie do AI.
- Nowe profile mają problem zimnego startu; pierwsze zlecenia często są słabo płatne.
- Connects i prowizje zjadają 10-20% małych zleceń.

**Test pierwszego tygodnia.** Uruchom agenta oceniającego na 7 dni i wyślij 15 ręcznie zatwierdzonych ofert dla obu usług; test zaliczony, jeśli zdobędziesz i dostarczysz co najmniej 1 płatne zlecenie, poświęcając mniej niż 2 godziny własnego czasu.

**Kiedy przerwać.** Przerwij, jeśli po 6 tygodniach i 60 ofertach zysk netto jest poniżej 100 USD/mies. albo twój czas na zlecenie przekracza 3 godziny.

**Źródła:** [Upwork: Is Upwork free (2026)](https://www.upwork.com/resources/is-upwork-free) · [goLance: Upwork fees explained 2026](https://golance.com/blogs/upwork-fees-explained-2026) · [Wikipedia: Upwork](https://en.wikipedia.org/wiki/Upwork)

---

## 3. Konkursy data science i AI

**Kategoria:** konkursy · **Realny dochód:** 0-200 USD/miesiąc średnio w skali roku (przypadek medianowy: 0, z rzadkimi jednorazowymi wygranymi 1000-10 000 USD) · **Potrzebny kapitał:** 0 USD (lokalny rig pokrywa trening i inferencję offline) · **Wynik: 56** (E4 A10 F12 L18 R12) · **Zasady:** kodowanie z pomocą AI dozwolone; zewnętrzne API LLM często zakazane podczas ewaluacji; legalne w Polsce: tak

> Udział w konkursach z nagrodami (Kaggle, DrivenData, Zindi, AIcrowd, ARC Prize) z agentami kodującymi, które równolegle prowadzą wiele eksperymentów na lokalnym rigu; w pełni legalne i naprawdę pasujące do 128 GB VRAM, ale nagrody trafiają do kilku najlepszych spośród setek lub tysięcy zespołów, więc medianowy miesiąc to zero.

**Skąd płyną pieniądze.** Organizator (firma, agencja, fundacja) finansuje pulę nagród dzieloną między 3-5 najwyższych miejsc w rankingu, czasem z dodatkowymi nagrodami za publikację lub nagrodami specjalnymi. Zwycięzcy zwykle muszą przekazać lub udostępnić jako open source kod i opis rozwiązania przed wypłatą. ARC Prize 2026 wymaga, by zwycięzcy „open source their solutions before receiving official private evaluation scores” na liberalnych licencjach (arcprize.org, odczyt 14.10.2026). Wypłata przelewem bankowym po weryfikacji tożsamości i formularzach podatkowych, zwykle po tygodniach lub miesiącach od finalnego rankingu. Niektóre nagrody finansowane przez rządy są ograniczone do określonych krajów (sprawdzaj kwalifikowalność dla każdego konkursu; w przypadku wyzwania DOE GEMS nie podano tego na stronie z ogłoszeniem).

**Asymetria.** Umiarkowana i leży w małych konkursach. Raport ML Contests wykazał, że medianowy konkurs w 2025 roku miał tylko 36 zespołów, wobec ponad 3700 zespołów w najpopularniejszym (Jane Street); ponad połowa zwycięskich zespołów w 2025 roku to pojedyncze osoby, a ponad 50% wygrało po raz pierwszy (relacja zewnętrzna). Przewaga polega więc na tym, że agent obserwuje 30+ platform, znajduje konkursy z małą liczbą uczestników i przez noc prowadzi dziesiątki eksperymentów na lokalnych GPU, podczas gdy większość uczestników iteruje ręcznie. W flagowych konkursach Kaggle najlepsze zespoły już używają agentów kodujących, więc nie spodziewałbym się tam przewagi. Okno: dopóki mali organizatorzy publikują niszowe zadania; powoli się zamyka wraz z upowszechnianiem się agentowych narzędzi ML (szacunek).

**Co robi agent.**
1. Obserwacja: codziennie agreguje nowe konkursy (Kaggle, DrivenData, Zindi, AIcrowd oraz listy agregatorów); zapisuje nagrodę, liczbę zespołów, termin, kwalifikowalność, zasady dotyczące zewnętrznych danych/modeli/API.
2. Filtr: zostawia konkursy z wysoką nagrodą na zespół (np. powyżej 500 USD na zespół), dostępne dla rezydentów Polski, bez potrzeby użycia API podczas ewaluacji, z zadaniem pasującym do lokalnego sprzętu.
3. Praca: agent buduje baseline, potem przez całą dobę prowadzi kolejkę eksperymentów (cechy, modele, ensemble) na 4 slotach GPU; loguje każde uruchomienie z wynikiem CV.
4. Weryfikacja: ufa tylko walidacji krzyżowej, która pokrywa się z publicznym rankingiem; Opus 5.5 co tydzień przegląda ryzyko wycieku danych i przeuczenia.
5. **Bramka ludzka:** czytasz zasady dla każdego źródła danych i licencji modelu, wybierasz 2 finalne zgłoszenia oraz zajmujesz się kodem zwycięzcy i formalnościami.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na rigu) | Płatne API | Dlaczego |
|---|---|---|---|
| Obserwacja konkursów i parsowanie zasad | Tak, 24/7 | Nie | Masowy tekst, niska stawka |
| Kod eksperymentów i nocne uruchomienia | Tak | Nie | Czas GPU lokalnie jest darmowy |
| Strategia, przegląd wycieków i CV | Nie | Opus 5.5 co tydzień | Mało wywołań, duża dźwignia |
| Inferencja wewnątrz zgłoszenia | Tylko lokalne modele open-weight | Niedozwolone w wielu regulaminach | ARC Prize 2026 zakazuje systemów opartych na API podczas ewaluacji |

**Liczby.**
- 2025 na 30+ platformach: ponad 16 mln USD w nagrodach, 390+ konkursów, średnio ~41 000 USD na konkurs, mediana 36 zespołów na konkurs; 23 konkursy z pulą 100 tys. USD+ (ML Contests, State of ML Competitions 2025, relacja zewnętrzna).
- Kaggle w 2025: 68 konkursów, 3,668 mln USD nagród, 29 mln+ użytkowników (ten sam raport).
- ARC Prize 2025: 1455 zespołów, 15 154 zgłoszenia; nagrody za najlepszy wynik 25 000 USD, 10 000 USD, potem 5000 USD za miejsca 3-5; dwa z pięciu najlepszych zespołów to pojedyncze osoby; nagrody za publikacje 50 000 / 20 000 / 5000 USD (wyniki arcprize.org, odczyt 14.10.2026).
- ARC Prize 2026: 2 mln USD w 3 ścieżkach, zgłoszenia do 2.11.2026, wyniki 4.12.2026; „Internet access is not available during Kaggle evaluation (no API-based systems like GPT/Claude/etc.)” (arcprize.org, odczyt 14.10.2026).
- DrivenData GEMS Prize Challenge (US DOE): 300 000 USD, 593 uczestników, zostało ok. 7 tygodni (drivendata.org, 14.10.2026).
- Hackathony: najbliższy hackathon ETHGlobal (Mumbaj, 5-7.11.2026) odbywa się stacjonarnie, a pula nagród nie jest podana (ethglobal.com, 14.10.2026); listy Devpost nie udało się odczytać (HTTP 403). Nie uwzględniam ich tutaj.
- Wybór modelu tekstowego przez zwycięzców w 2025: niemal wszyscy zwycięzcy konkursów tekstowych używali modeli Qwen (ML Contests 2025), czyli modeli open-weight, które działają na lokalnym rigu takim jak ten.

**Jak zacząć.**
1. Załóż konta na Kaggle, DrivenData, Zindi i AIcrowd; zweryfikuj telefon/tożsamość tam, gdzie jest to wymagane.
2. Zbuduj obserwatora i checklistę zasad (kwalifikowalność, zewnętrzne dane, licencje modeli, użycie API, limity zespołów).
3. Wybierz jeden trwający konkurs z mniej niż 100 zespołami i terminem co najmniej 4 tygodnie naprzód.
4. Skonfiguruj na rigu runner eksperymentów ze stałym CV i logowaniem eksperymentów.
5. Wykorzystaj jeden „treningowy” konkurs do skalibrowania CV względem rankingu, zanim zaczniesz gonić za pieniędzmi.

**Zasady, podatki i ryzyka.**
- Zasady różnią się między konkursami: niektóre zakazują zewnętrznych API lub promptowania wytrenowanych LLM (przykład: PARADOX ML Challenge, ogłoszenie zewnętrzne); ARC Prize zakazuje API podczas ewaluacji. Sprawdzaj na stronie regulaminu każdego konkursu limity kont, zespołów i prywatnego udostępniania kodu.
- Legalne w Polsce: tak. Podatek: nagroda od zagranicznego organizatora to dochód osobisty polskiego rezydenta podatkowego (PIT-36); szczegóły w rozdziale o zasadach.
- Ryzyka: miesiące pracy bez nagrody; przetasowania w rankingu między wynikami publicznymi i prywatnymi; obowiązki zwycięzcy (udostępnienie open source, przeniesienie licencji).

**Ograniczenia.**
- Nagrody skupione na szczycie: trafiają do 3-5 zespołów na konkurs.
- Duże konkursy Kaggle są już pełne zespołów wspieranych przez agentów.
- Niektóre nagrody rządowe wykluczają osoby spoza USA.
- 10 h/tydzień czasu człowieka ogranicza liczbę konkursów, które da się śledzić.
- Zakazy API podczas ewaluacji oznaczają, że płatny model pomaga tylko offline.

**Test pierwszego tygodnia.** Zgłoś się do jednego trwającego konkursu z mniej niż 100 zespołami; uruchom agenta na 7 dni. Zaliczone, jeśli najlepsze zgłoszenie jest w górnych 25% publicznego rankingu. **Kiedy przerwać.** Przerwij po 3 konkursach bez miejsca w górnych 10%.

**Źródła:** [ML Contests: State of ML Competitions 2025](https://mlcontests.com/state-of-machine-learning-competitions-2025/) · [ARC Prize 2026](https://arcprize.org/competitions/2026) · [Wyniki ARC Prize 2025](https://arcprize.org/blog/arc-prize-2025-results-analysis) · [Konkursy DrivenData](https://www.drivendata.org/competitions/) · [Wydarzenia ETHGlobal](https://ethglobal.com/events) · [PARADOX ML Challenge](https://gdg.community.dev/events/details/google-gdg-on-campus-jamia-millia-islamia-delhi-india-presents-paradox-ml-challenge)

---

## 4. Bounty i areny red-teamingu AI

**Kategoria:** bounty / konkursy · **Realny dochód:** mediana 0-300 USD/miesiąc (nierówno: w większości miesięcy 0, od czasu do czasu znalezisko za 500-2500 USD) · **Potrzebny kapitał:** ~0-100 USD (tokeny API dla sędziego) · **Wynik: 55** (E5 A12 F13 L16 R9) · **Zasady:** automatyzacja nie jest zakazana w polityce 0DIN, ale każdy raport musi być powtarzalnym opisem napisanym przez człowieka; zasady aren i konkursów różnią się w zależności od wydarzenia i trzeba je czytać za każdym razem; legalne w Polsce: tak (testowanie w ramach autoryzowanego programu)

> Płatne badania nad jailbreakami i prompt injection dla laboratoriów AI i aren; agent z lokalnym modelem bez cenzury może dziennie wypróbować tysiące wariantów ataku, ale wypłaty są rzadkie, nierówne i zdominowane przez niewielką grupę ekspertów, więc to poboczny zakład rozwijający umiejętności, a nie stały dochód.

**Skąd płyną pieniądze.** Są trzy rodzaje płatników. (1) Otwarte programy bug bounty: 0DIN od Mozilli płaci 500-15 000 USD za zweryfikowaną lukę w GenAI, z wypłatą w ciągu 30 dni od zawarcia porozumienia; wymagany jest dokument tożsamości i formularz podatkowy W-8BEN. (2) Programy laboratoriów: Anthropic (przez HackerOne) i OpenAI prowadzą bounty za jailbreaki, w większości tylko na zaproszenie. (3) Konkursy czasowe z pulami nagród: Gray Swan Arena, HackAPrompt 2.0, wyzwania red-teamingowe na Kaggle. Nagrody trafiają do miejsc w rankingu lub do tego, kto „pierwszy złamie” cel.

**Asymetria.** Większość graczy na arenach wciąż wpisuje ataki ręcznie w okienku czatu. Agent może przez całą dobę generować, mutować i oceniać warianty ataków na lokalnym modelu, który nie ma kosztu za token ani własnego filtra bezpieczeństwa, podczas gdy płatny model pełni rolę dokładnego sędziego („czy cel naprawdę ujawnił zakazaną treść?”). Haczyk w tym, że czołówka każdego rankingu już używa skryptów. Gray Swan podaje ponad trzy miliony prób ataku w swojej sieci *(deklaracja platformy, 2026)*. Asymetria istnieje więc wobec przypadkowej większości, a nie wobec zwycięzców. Okno: otwarte, dopóki laboratoria płacą za jailbreaki znalezione przez ludzi; zwęża się, w miarę jak laboratoria automatyzują własny red-teaming.

**Co robi agent.**
1. Obserwacja: odpytuje strony zakresu 0DIN, strony wydarzeń Gray Swan / HackAPrompt i Kaggle w poszukiwaniu nowych celów; streszcza zasady (czy automatyzacja jest dozwolona? limity zapytań? ujawnianie?) do przeczytania przez człowieka.
2. Filtrowanie: odrzuca wydarzenia, których zasady zabraniają zgłoszeń ze skryptów lub dostępu przez API; zostawia tylko modele i kategorie szkód objęte zakresem.
3. Praca: lokalny model generuje kandydatów na ataki na podstawie biblioteki publicznych rodzin technik; uruchamia je przeciwko celowi wyłącznie przez oficjalny interfejs i w granicach limitów zapytań.
4. Weryfikacja: płatny model ocenia każdą odpowiedź według kryteriów sukcesu programu; usuwa duplikaty względem znanych publicznych jailbreaków (0DIN dzieli bounty przy duplikatach zgłoszonych w ciągu 7 dni).
5. Zgłoszenie: BRAMKA CZŁOWIEKA. Czytam każdego kandydata, odtwarzam go ręcznie, piszę raport (0DIN prosi najpierw o krótkie streszczenie) i sam go zgłaszam.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na rigu) | Płatne API | Dlaczego |
|---|---|---|---|
| Streszczenie zasad i zakresu | pierwsze streszczenie | Opus 5.5 sprawdza klauzule o automatyzacji | źle odczytana zasada może zdyskwalifikować wszystko |
| Generowanie ataków | wszystkie warianty, 24/7 | nic | wolumen, brak odmów, brak kosztu tokenów |
| Ocena sukcesu | zgrubny filtr | ostateczny sędzia dla krótkiej listy | dokładność sędziego decyduje o tym, co zgłaszasz |
| Deduplikacja względem publicznych jailbreaków | wyszukiwanie po embeddingach | nic | prywatne i tanie |
| Napisanie raportu | projekt | przegląd przez Opus 5.5 | jakość raportu wpływa na wysokość wypłaty |

**Liczby.**
- Progi nagród 0DIN: Low do 500, Medium do 2500, High do 5000, Severe do 15 000 USD; wypłata w ciągu 30 dni od zawarcia porozumienia; 2 tygodnie walidacji; duplikaty w ciągu 7 dni dzielą bounty *(polityka, aktualizacja 2.10.2026, 0din.ai)*.
- Anthropic: do 15 000 USD za uniwersalne jailbreaki, tylko na zaproszenie, HackerOne *(08.2024)*; do 25 000 USD za klasyfikatory Claude 3.7 Sonnet, tylko na zaproszenie *(05.2025)*.
- OpenAI: od lipca 2024 nagrodzono tylko 6 znalezisk dotyczących bezpieczeństwa, średnia wypłata w ostatnich 3 miesiącach 250 USD *(relacja zewnętrzna, EA Forum, 2.06.2025)*.
- HackAPrompt: rozdano „ponad 100 000 USD”, 30 tys.+ uczestników w 150+ krajach; jeden czołowy gracz wygrał 28 tys.+ USD w różnych wydarzeniach *(deklaracja platformy, 10.2026)*. Przy 30 tys. uczestników mediana uczestnika nie wygrywa nic.
- Gray Swan Arena: aktualnych pul nagród nie udało się pobrać w chwili pisania (strona z limitem zapytań, 10.2026): sprawdź bieżącą stronę wyzwania.

**Jak zacząć.**
1. Załóż konta na 0DIN, Gray Swan Arena, HackAPrompt i Kaggle; przeczytaj zasady każdego wydarzenia i zapisz je do pliku.
2. Przygotuj się do KYC przy wypłacie: dokument tożsamości ze zdjęciem (paszport) i formularz W-8BEN (osoba spoza USA) dla 0DIN.
3. Zbuduj harness: adapter celu (oficjalne API albo interfejs webowy tylko tam, gdzie to dozwolone), lokalny generator, płatny sędzia, log SQLite każdej próby.
4. Pierwszy cel: trwające wyzwanie dla początkujących w Gray Swan lub HackAPrompt, które dopuszcza użycie API, aby skalibrować sędziego przed polowaniem na bounty 0DIN.

**Zasady, podatki i ryzyka.**
- 0DIN: nie znaleziono klauzuli zakazującej zautomatyzowanych narzędzi, ale wypłata wymaga „porozumienia umownego” i dokumentu tożsamości ze zdjęciem; badacze z regionów objętych sankcjami są wykluczeni *(polityka, 10.2026)*.
- Programy laboratoriów: tylko na zaproszenie, objęte NDA; testowanie produkcyjnego modelu poza programem nie jest objęte safe harbour i może naruszać zasady korzystania dostawcy.
- Prawo polskie: testowanie w ramach autoryzowanego programu nie jest nieuprawnionym dostępem; trzymaj się ściśle zakresu (patrz `../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md`).
- Podatek: nagrody z konkursów są opodatkowane według zasad PIT dla nagród lub jako inne źródła, zależnie od formy; nagrody za zgłoszenia to zwykle „inne źródła” (szczegóły w rozdziale o zasadach).
- Ryzyka: blokady kont za przekroczenie limitów zapytań, zduplikowane znaleziska, miesiące na zero.

**Ograniczenia.**
- Zwycięzca bierze prawie wszystko: kilku ekspertów zgarnia większość puli nagród.
- Wygenerowane szkodliwe treści muszą pozostać prywatne: przechowuj je zaszyfrowane, nigdy nie publikuj.
- Laboratoria szybko łatają; działający jailbreak może przestać działać przed walidacją.
- Wydarzenia na arenach są nieregularne; nie ma stałego strumienia pracy.

**Test pierwszego tygodnia.** Uruchom harness na jednym otwartym wyzwaniu przez 7 dni. Test zaliczony, jeśli potwierdzony przez sędziego odsetek sukcesów przekracza 1 na 1000 prób ORAZ co najmniej jedno złamanie zostanie zaakceptowane przez tablicę wyników areny.

**Kiedy przerwać.** Brak zaakceptowanego złamania lub płatnego znaleziska po 8 tygodniach pracy agenta.

**Źródła:** [Polityka 0DIN](https://0din.ai/policy) · [Ogłoszenie 0DIN, Mozilla Hacks](https://hacks.mozilla.org/2024/08/0din-a-genai-bug-bounty-program-securing-tomorrows-ai-together/) · [Anthropic: bounty za bezpieczeństwo modeli](https://www.anthropic.com/news/model-safety-bug-bounty) · [Anthropic: bounty 2025](https://www.anthropic.com/news/testing-our-safety-defenses-with-a-new-bug-bounty-program) · [Krytyka programów bounty bezpieczeństwa AI na EA Forum](https://forum.effectivealtruism.org/posts/xAWKpgiTFF9ruEpsz/critique-of-current-ai-safety-bug-bounty-programs) · [HackAPrompt](https://hackaprompt.com/) · [Gray Swan](https://www.grayswan.ai/)

---

## 5. Turnieje prognostyczne AI (legalna strona rynków predykcyjnych)

**Kategoria:** konkursy · **Realny dochód:** 0-150 USD/miesiąc w przypadku medianowym (nagrody są sezonowe i nieregularne) · **Potrzebny kapitał:** 0 USD (sponsorowane kredyty LLM) · **Wynik: 55** (E3 A8 F13 L18 R13) · **Zasady:** automatyzacja dozwolona (turniej FutureEval jest wyłącznie dla botów); legalne w Polsce: tak w przypadku turniejów z nagrodami, NIE w przypadku handlu za prawdziwe pieniądze na Polymarket/Kalshi

> Rynki predykcyjne na prawdziwe pieniądze są zamknięte dla rezydenta Polski, więc zostaje turniej botów Metaculus FutureEval: legalny, z darmowym udziałem i zbudowany dla agentów, ale stawka liczy już ponad 100 botów, więc to konkurs budujący umiejętności z małą oczekiwaną kwotą nagród, a nie źródło dochodu.

**Skąd płyną pieniądze.** Metaculus wypłaca pulę nagród 50 000 USD na sezon FutureEval twórcom botów spoza Metaculus, czyli około 175 tys. USD rocznie we wszystkich turniejach (wpis z wynikami Spring 2026, wrzesień 2026). Nagrody trafiają do czołówki rankingu po rozstrzygnięciu pytań. Sezon Spring 2026 rozstrzygnął się w maju, a wypłaty planowano na czerwiec/lipiec 2026, więc pieniądze przychodzą miesiące po wykonanej pracy. Zwycięzcy muszą wypełnić ankietę o swojej strategii, żeby dostać wypłatę. Jak pula dzieli się według miejsc: nie znaleziono.

**Asymetria.** W zwykłym sensie nie ma żadnej. To konkurs, w którym każdy uczestnik jest botem: w Spring 2026 było 173 boty, z czego 111 zewnętrznych, na 297 ocenianych pytaniach (EA Forum, 9.09.2026). Przewagą jest tu rusztowanie agenta (pipeline'y researchu, ensembling, kalibracja), a nie „używanie AI w ogóle”. Metaculus podaje, że przewaga ludzkich profesjonalistów „prawie zniknęła”, a zwykły, nieagentowy bot na GPT-5.1 zajął dopiero 18. miejsce, więc lepsze rusztowanie wygrywa z surowym modelem. Strona na prawdziwe pieniądze (Polymarket) to miejsce, gdzie nadal dominują ręczni traderzy, ale czytelnik nie ma do niej legalnego dostępu (patrz zasady).

**Co robi agent.**
1. Obserwacja: odpytuje API turnieju o nowo otwarte pytania.
2. Research: uruchamia kilka wyszukiwań newsów na pytanie, pobiera częstości bazowe i wcześniejsze rozstrzygnięcia.
3. Prognoza: 3-5 niezależnych prognoz na pytanie, potem agregacja (mediana, lekko ekstremizowana).
4. Weryfikacja: kontrola sensowności (prawdopodobieństwa sumują się do 1 przy wielokrotnym wyborze, brak skrajności 0/1, poprawnie sparsowane daty).
5. Wysłanie przez API. Nie przepływają żadne pieniądze, więc nie ma ludzkiej bramki przy każdej prognozie; człowiek przegląda cotygodniowy raport kalibracji.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na maszynie) | Płatne API | Dlaczego |
|---|---|---|---|
| Triaż pytań i streszczanie newsów | tak, 24/7 na 4 slotach | nie | masowy tekst, prywatnie, za darmo |
| Wyszukanie częstości bazowej i szkic uzasadnienia | tak | nie | długi kontekst, wiele wywołań |
| Ostateczne prawdopodobieństwo | nie | sponsorowane modele frontier (kredyty od organizatora) | cała pierwsza dziesiątka Spring 2026 używała GPT-5.x; model lokalny z Indeksem 34 się nie załapie |
| Cotygodniowy przegląd kalibracji | nie | Opus 5.5 | trudne rozumowanie, mały wolumen |

**Liczby.**
- Pula nagród: 50 000 USD na sezon; ~175 tys. USD/rok w całym FutureEval (wpis z wynikami na EA Forum, 9.09.2026; Substack Metaculus).
- Stawka: 173 boty, 111 zewnętrznych, 297 ocenianych pytań w Spring 2026 (EA Forum, 9.09.2026).
- Sezon Summer 2026: start 18.05.2026, 300-500 pytań; darmowe kredyty od Anthropic, Google i OpenAI, z prośbą o zużywanie mniejszej liczby kredytów OpenAI (ogłoszenie na LessWrong, 2026).
- Zwycięski stack: GreeneiBot2 używał równoległego researchu (AskNews, Perplexity, wyszukiwanie GPT-5); każdy z respondentów ankiety z pierwszej dziesiątki używał GPT-5.2 lub nowszego (EA Forum, 9.09.2026).
- Nagroda według miejsca i medianowa nagroda na bota: nie znaleziono. Przy 111 zewnętrznych botach większość uczestników nie wygrywa nic.

**Jak zacząć.**
1. Załóż konto na Metaculus i zarejestruj bota w bieżącym sezonie FutureEval; złóż wniosek o sponsorowane kredyty.
2. Zrób fork szablonowego bota Metaculus, uruchom go bez zmian przez tydzień, żeby mieć punkt odniesienia.
3. Dodaj lokalny etap researchu (pobieranie + streszczanie newsów na maszynie), ostateczną prognozę zostaw na sponsorowanym modelu frontier.
4. Loguj każdą prognozę; oceniaj ją względem rozstrzygniętych pytań; iteruj co tydzień.

**Zasady, podatki i ryzyka.**
- Polymarket oznacza Polskę jako „Close-Only”: użytkownicy „nie mogą otwierać nowych pozycji” (dokumentacja geoblokady Polymarket, odczyt 14.10.2026). Francja zablokowała go przez dostawców internetu 16.07.2026; Holandia również go zablokowała (prasa, 2026).
- Polska ustawa o grach hazardowych (art. 2 ust. 2) traktuje zakłady na „zaistnienie różnych zdarzeń” jako zakłady wzajemne wymagające polskiej licencji; art. 107 Kodeksu karnego skarbowego (kks) przewiduje grzywnę dla gracza, który uczestniczy w nielicencjonowanych lub zagranicznych grach hazardowych. Użycie VPN, żeby dostać się do Polymarket, łamałoby zarówno jego regulamin, jak i polskie prawo. Kalshi: Polski nie ma na jego stronach pomocy (nie znaleziono); traktuj jako niedostępny.
- Manifold działa wyłącznie na wirtualne pieniądze; Metaculus Cup i FutureEval płacą prawdziwe nagrody za umiejętność prognozowania, a nie za zakłady.
- Podatek: nagroda z konkursu jest opodatkowana w Polsce (szczegóły w 03-ZASADY-PODATKI-RYZYKA.md).
- Ryzyka: zero nagród przez miesiące, zasady nagród zmieniają się co sezon, sponsoring kredytów może się skończyć.

**Ograniczenia.**
- Turniej już teraz składa się w 100% z botów; konkurujesz rusztowaniem z zespołami badawczymi.
- Podziału nagród według miejsc nie ma w materiałach, które znalazłem; medianowy uczestnik prawdopodobnie dostaje 0.
- Opóźnienie wypłaty o 1-3 miesiące po zakończeniu sezonu.
- Model lokalny jest za słaby na ostateczną decyzję; przewaga zależy od sponsorowanych kredytów na modele frontier.
- Wartość to głównie portfolio i umiejętności (agenci prognostyczni), a nie gotówka.

**Test pierwszego tygodnia.** Uruchom szablonowego bota z lokalnym etapem researchu na każdym otwartym pytaniu przez 7 dni. Zaliczone, jeśli bot wysyła prognozy na ≥90% otwartych pytań, a jego wynik Brier/log na już rozstrzygniętych pytaniach treningowych jest lepszy od bazowego szablonu.

**Kiedy przerwać.** Przerwij, jeśli po jednym pełnym sezonie bot jest poza pierwszą dwudziestką botów zewnętrznych.

**Źródła:** [Geoblokada Polymarket](https://docs.polymarket.com/developers/CLOB/geoblock) · [Wyniki FutureEval Spring 2026 (EA Forum)](https://forum.effectivealtruism.org/posts/iJ3qBDwpWCfNy9ZGd/pros-beat-bots-but-the-gap-is-nearly-gone) · [Ogłoszenie FutureEval Summer 2026](https://www.lesswrong.com/posts/E7wxQnBvYxgB3rTTk/announcing-metaculus-summer-2026-futureeval-bot-tournament) · [Metaculus FutureEval](https://metaculus.substack.com/p/metaculus-futureeval-ai-forecasting-benchmark) · [Francja blokuje Polymarket](https://xyz.pl/dzieje-sie/francja-blokuje-dostep-do-polymarket-1050) · [Holandia blokuje Polymarket](https://yellow.com/pl/news/niderlandy-blokują-polymarket-i-grożą-karami-do-840-tys-euro-–-rynki-predykcyjne-tracą-bezpieczne-przystanie) · [Ustawa o grach hazardowych (ISAP)](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU20092011540) · [Kodeks karny skarbowy (ISAP)](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19990830930)

---

## 6. Licytacje komornicze i przetargi publiczne

**Kategoria:** arbitraż · **Realny dochód:** 0-400 USD/miesiąc (mediana ~150 USD po powolnym pierwszym kwartale) · **Potrzebny kapitał:** 1000-2000 USD w obrocie (rękojmie plus cena zakupu) · **Wynik: 52** (E7 A14 F8 L16 R7) · **Zasady:** automatyzacja w regulaminie: niezweryfikowana dla portalu licytacji komorniczych, czytaj publiczne obwieszczenia z niską częstotliwością; legalne w Polsce: tak, licytacja wymaga numeru PESEL i prawdziwej tożsamości

> Czytanie setek obwieszczeń o licytacjach komorniczych i przetargach agencji państwowych oraz operatów szacunkowych to powolna, nudna papierkowa robota, czyli dokładnie to, w czym agent jest dobry; limit kapitału i cienkie, nieregularne marże trzymają tę okazję w środku tabeli.

**Skąd płyną pieniądze.** Kupujesz zajętą lub zbędną rzecz (samochód, narzędzia, elektronikę, maszyny) na licytacji komorniczej lub w przetargu agencji państwowej, a potem odsprzedajesz ją na Allegro/OLX. Na licytacji komorniczej ruchomości cena wywołania jest ustalona ustawowo: „Cena wywołania w pierwszym terminie licytacji publicznej wynosi trzy czwarte wartości szacunkowej”, a w drugim terminie „połowę wartości szacunkowej” (art. 867 § 2 KPC, t.j. Dz.U. 2026, odczyt 14.10.2026). Twoja marża to różnica między tą ceną plus kosztami a realną ceną odsprzedaży. Pieniądze wpływają dopiero przy odsprzedaży, często po kilku tygodniach.

**Asymetria.** Obwieszczenia są na portalu licytacji komorniczych (licytacje.komornik.pl), na stronie Agencji Mienia Wojskowego (AMW) i na jej platformie przetargowej oraz w plikach PDF z operatami szacunkowymi. Większość licytujących to lokalni handlarze, którzy ręcznie czytają kilka obwieszczeń ze swojej okolicy. Agent może codziennie przeczytać każde nowe obwieszczenie w całym kraju, wyciągnąć wycenę, uwagi o stanie i zdjęcia, a potem porównać je z cenami odsprzedaży. Nie znalazłem źródła mówiącego, ilu licytujących już to automatyzuje (nie znaleziono); format pełen papierów sugeruje, że niewielu. Okno pozostaje otwarte, dopóki obwieszczenia są w PDF-ach i wolnym tekście.

**Co robi agent.**
1. Obserwacja: raz dziennie czyta nowe obwieszczenia z portalu komorniczego i ogłoszenia AMW w kulturalnym tempie (najpierw sprawdź regulamin każdej strony).
2. Filtrowanie: zostawia kategorie, które możesz odsprzedać i przewieźć; odrzuca rzeczy powyżej twojego kapitału lub poza zasięgiem dojazdu.
3. Praca: wyciąga wartość szacunkową, cenę wywołania (3/4 lub 1/2), rękojmię, termin oględzin, wady; szacuje cenę odsprzedaży na podstawie porównywalnych ogłoszeń, które sprawdzasz ręcznie.
4. Weryfikacja: płatny model ponownie czyta operat w poszukiwaniu pułapek prawnych (współwłasność, brak dokumentów, problemy z VIN w samochodach).
5. Działanie: bramka zatwierdzenia przez człowieka. To ty decydujesz, wpłacasz rękojmię i licytujesz; agent nigdy nie licytuje.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na rigu) | Płatne API | Dlaczego |
|---|---|---|---|
| Codzienne czytanie obwieszczeń | Parsowanie obwieszczeń, PDF-ów po OCR, wyciąganie pól | Brak | Duża skala, tanio, 24/7 |
| Sprawdzenie zdjęć i stanu | Pierwszy przegląd zdjęć | Analiza wizyjna rzeczy z krótkiej listy | Jakość liczy się tylko dla krótkiej listy |
| Przegląd pułapek prawnych | Brak | Opus 5.5 czyta cały operat | Trudne rozumowanie, kilka pozycji tygodniowo |
| Szacunek ceny odsprzedaży | Szkic na podstawie wklejonych porównań | Przegląd 3 najlepszych okazji | Ostateczna liczba decyduje o prawdziwych pieniądzach |

**Liczby.**
- Rękojmia przy licytacji komorniczej ruchomości: „w wysokości jednej dziesiątej sumy oszacowania”; bez rękojmi, „jeżeli suma oszacowania jest niższa niż pięć tysięcy złotych” (art. 867¹ § 1 KPC, t.j. Dz.U. 2026, odczyt 14.10.2026).
- Licytacja elektroniczna: rękojmia musi wpłynąć na rachunek bankowy komornika „najpóźniej na 2 dni robocze przed rozpoczęciem przetargu”, a licytant musi podać PESEL, numer dowodu osobistego i stan cywilny (art. 879⁵ KPC).
- Licytacje nieruchomości wymagają rękojmi w wysokości jednej dziesiątej sumy oszacowania (art. 962 § 1 KPC), co znacznie przekracza budżet 2000 USD.
- AMW sprzedaje zbędne mienie i sprzęt w przetargach oraz przez sklep internetowy (amw.com.pl, odczyt 14.10.2026; zasady wadium są określone w każdym ogłoszeniu).
- Typowe marże przy odsprzedaży: nie znaleziono. Zmierz je w pierwszym tygodniu na podstawie własnych porównań.

**Jak zacząć.**
1. Przeczytaj regulamin portalu licytacji komorniczych i zasady przetargów AMW; zanotuj każdy zapis o automatycznym dostępie.
2. Zbuduj mały czytnik najnowszych obwieszczeń w jednej kategorii (na przykład samochody albo elektronarzędzia) w swoim województwie.
3. Ustal twardą regułę budżetową: na początek tylko rzeczy z wyceną poniżej 5000 PLN (bez rękojmi, niska strata).
4. Zanim cokolwiek wylicytujesz, pojedź osobiście na jedne oględziny.

**Zasady, podatki i ryzyka.**
- Licytujesz we własnym imieniu, z numerem PESEL (art. 879⁵ § 2 KPC); nie ma anonimowego ani zautomatyzowanego licytowania.
- Kupowanie w celu odsprzedaży to działalność o charakterze handlowym: w 2026 roku działalność nierejestrowana jest dozwolona do 10 813,50 PLN przychodu na kwartał, potem musisz zarejestrować się w CEIDG w ciągu 7 dni (money.pl, 19.08.2026). Dochód wykazujesz w PIT-36 według skali podatkowej.
- Ryzyka: rzeczy sprzedawane w stanie, w jakim są, ukryte wady, koszty transportu, powolna odsprzedaż, zaskarżenie licytacji przez dłużnika.

**Ograniczenia.**
- Nieruchomości są poza zasięgiem przy tym kapitale.
- Rzeczy trzeba odebrać fizycznie; czas dojazdu zjada 10 godzin tygodniowo.
- Operaty są często trafne, więc realna różnica pojawia się głównie w drugim terminie (50%).
- Brak danych ze źródeł o medianie marż.

**Test pierwszego tygodnia.** Pozwól agentowi przez 7 dni czytać każde nowe obwieszczenie w jednej kategorii i regionie i tworzyć ranking z szacowaną marżą; sprawdź ręcznie 10 pozycji. Test zaliczony, jeśli ≥2 pozycje mają szacowaną marżę netto ≥25% po opłatach i transporcie. **Kiedy przerwać.** Przerwij, jeśli po 2 miesiącach i 3 zakupach marża netto jest poniżej 10% albo kapitał utknął w niesprzedanych rzeczach.

**Źródła:** [Tekst jednolity KPC (ISAP)](https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19640430296/U/D19640296Lj.pdf) · [Portal licytacji komorniczych](https://licytacje.komornik.pl/) · [Agencja Mienia Wojskowego](https://amw.com.pl/) · [money.pl: działalność nierejestrowana 2026](https://direct.money.pl/artykuly/porady/dzialalnosc-nierejestrowana-2026-limit-10-813,50-zl,-po-przekroczeniu-7-dni-na-ceidg)

---

## 7. Konkursy audytowe smart kontraktów i bug bounty

**Kategoria:** konkursy · **Realny dochód:** 0-500 USD/miesiąc (przypadek medianowy dla nowicjusza przy 10 h/tydzień: ok. 0-200) · **Potrzebny kapitał:** 0 USD (plus tokeny API; żadne środki nie są zagrożone) · **Wynik: 52** (E6 A10 F10 L16 R10) · **Zasady:** praca z pomocą AI dozwolona, ale raporty z AI/skanerów bez udowodnionego wpływu są zakazane (Immunefi); legalne w Polsce: tak, z KYC

> Przegląd kodu Solidity w konkursach o ograniczonym czasie (Cantina, Sherlock, CodeHawks) i w stałych programach bug bounty (Immunefi) z agentem, który robi pierwsze przejście, i człowiekiem, który udowadnia wpływ; prawdziwe pule nagród i mnożnik agenta przy czytaniu kodu, ale stroma krzywa umiejętności, dzielenie nagród za duplikaty i kurczący się rynek konkursów utrzymują niską medianę.

**Skąd płyną pieniądze.** Protokół finansuje pulę nagród (konkursy) lub stałą tabelę nagród (Immunefi). W konkursach ważne znaleziska High/Medium dzielą pulę; im więcej osób zgłosi ten sam błąd, tym mniejszy udział każdej z nich, który może spaść „at times less than $1” przy powszechnych błędach o niskiej wadze (Runtime Verification, 08.2024). W bounty pierwsze ważne zgłoszenie krytycznego błędu bierze całą podaną nagrodę. Wypłaty są zwykle w stablecoinach (USDC) po KYC; Immunefi pisze, że brak KYC „may result in forfeiture of payment” (regulamin, odczyt 14.10.2026). Terminy: konkursy płacą po ocenie i odwołaniach, zwykle kilka tygodni po zakończeniu.

**Asymetria.** Częściowa i się zawęża. Agenci są dobrzy w żmudnym pierwszym przejściu (czytanie 5000-20 000 linii, mapowanie niezmienników, wypisywanie podejrzanych ścieżek), czyli tam, gdzie początkujący pracujący ręcznie tracą najwięcej czasu. Ale audytorzy AI to już produkt: Krait od Zealynx deklaruje 100% precyzji w 50 konkursach na ślepo, a Pashov Auditor jest publicznym punktem odniesienia (Zealynx, 31.05.2026, deklaracja dostawcy), podczas gdy generyczne skanery LLM mają średnio ok. 8% precyzji, „5 real findings out of 60 reported” (to samo źródło). Pole się więc podzieliło: generyczny output AI to szum, który platformy odrzucają; dostrojony agent plus człowiek, który pisze działający PoC, wciąż wyprzedza medianowego uczestnika pracującego ręcznie. Okno: 6-18 miesięcy, zanim dostrojeni audytorzy AI spłaszczą pulę duplikatów (szacunek).

**Co robi agent.**
1. Obserwacja: codziennie listuje nadchodzące konkursy i nowe programy bounty (Cantina, Sherlock, CodeHawks, Immunefi); na starcie pobiera repozytoria i zakres.
2. Filtr: wybiera konkursy według wielkości puli na linię kodu i według znanych ci typów protokołów (lending, AMM, vaulty).
3. Praca: agent mapuje kontrakty, wywołania zewnętrzne, kontrolę dostępu i niezmienniki; uruchamia Slither/fuzzing Foundry; szkicuje hipotezy uszeregowane według wpływu.
4. Weryfikacja: dla każdej czołowej hipotezy agent pisze test PoC w Foundry na lokalnym forku; bez PoC nie ma raportu.
5. **Bramka ludzka:** sam czytasz ścieżkę w kodzie, potwierdzasz wagę zgodnie z zasadami oceny platformy i zgłaszasz tylko znaleziska poparte PoC. Nigdy nie testuj na mainnecie ani publicznych testnetach (Immunefi banuje za to na stałe).

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na rigu) | Płatne API | Dlaczego |
|---|---|---|---|
| Obserwacja konkursów i mapowanie kodu | Tak, 24/7 | Nie | Długi kod, wiele plików, tanio |
| Generowanie hipotez | Masowe przejście po plikach | Opus 5.5 dla logiki między kontraktami | Trudne błędy wymagają głębokiego rozumowania |
| Pisanie i uruchamianie PoC | Szkice testów | Opus 5.5 do naprawy nieudanych PoC | Poprawność ważniejsza niż szybkość |
| Raport i argumentacja wagi | Szkic | Opus 5.5 finalnie | Sędziowie nagradzają jasno pokazany wpływ |

**Liczby.**
- Code4rena zamknęła się 13.05.2026 po 512 audytach, 26 898 zgłoszonych podatnościach i ponad 16 600 zarejestrowanych badaczach (shattered.io, 1.10.2026, relacja zewnętrzna). Mniej miejsc z konkursami.
- Cantina: 55,5 mln USD łącznych wypłat, 23 886 badaczy, 51 aktywnych bounty i 1 aktywny konkurs (pula 50 000 USDC), 144 zakończone konkursy (cantina.xyz, 14.10.2026, deklaracja platformy).
- Immunefi: 140,6 mln USD skumulowanych wypłat, 92 000+ badaczy, 650+ protokołów (stan na 06.2026, za shattered.io, relacja zewnętrzna).
- Rozkład zarobków: medianowy uczestnik poniżej 50 tys. USD/rok, top-25 200-500 tys. USD, początkujący 5-20 tys. USD w 3-6 miesięcy intensywnej praktyki (Zealynx academy, relacja zewnętrzna; „intensywnej” oznacza znacznie więcej niż 10 h/tydzień).
- Rekordowa pojedyncza wypłata: jeden audytor wziął ponad 500 000 USD z puli konkursu zkSync (Runtime Verification, 08.2024).
- Typowa wielkość konkursu: ok. 5342 linie Solidity, 2-3 tygodnie (Runtime Verification, 08.2024).

**Jak zacząć.**
1. Naucz się Foundry i 10 najczęstszych klas błędów DeFi; odtwórz 5 przeszłych konkursów z opublikowanymi znaleziskami i zmierz recall swojego agenta.
2. Załóż konta na Cantina i Sherlock; skonfiguruj portfel do wypłat w USDC; przejdź KYC, gdy pierwsze znalezisko zostanie uznane.
3. Zgłoś się do jednego małego konkursu ze skromną pulą, w którym rywalizuje mniej czołowych audytorów.
4. Śledź dla każdego konkursu: godziny, zgłoszone znaleziska, ważne, duplikaty, USD.

**Zasady, podatki i ryzyka.**
- Immunefi zakazuje „Submitting AI-generated/automated scanner bug reports that lack the required information regarding the vulnerability's impact” oraz „Automated testing of services that generates significant amounts of traffic”; „Testing on mainnet or public testnet is grounds for an immediate and permanent ban” (regulamin, odczyt 14.10.2026).
- Wytyczne oceny Sherlocka: nie znalazłem wyraźnej klauzuli o AI (odczyt 14.10.2026); duplikaty dostają najwyższą wagę spośród nich.
- Legalność w Polsce: przegląd opublikowanego kodu źródłowego nie jest dostępem do czyjegoś systemu; trzymaj się lokalnych forków. Wypłaty przychodzą w kryptowalutach, więc traktowanie podatkowe (dochód osobisty w momencie otrzymania vs PIT-38 przy zbyciu) wymaga rozdziału o zasadach i być może doradcy.
- Ryzyka: tygodnie pracy bez żadnego ważnego znaleziska; silne rozmycie przez duplikaty; KYC wymagane do wypłaty; koszty wymiany stablecoinów na walutę fiat.

**Ograniczenia.**
- Realna bariera umiejętności: Solidity i ekonomia DeFi, a nie tylko programowanie.
- 10 h/tydzień to mało na 2-3-tygodniowy konkurs z ponad 5000 linii.
- Produkty audytorów AI już konkurują o te same łatwe błędy.
- Rynek konkursów skurczył się po zamknięciu Code4rena.
- Wypłaty w kryptowalutach komplikują podatki i wymianę na fiat.

**Test pierwszego tygodnia.** Odtwórz jeden przeszły konkurs z publicznymi znaleziskami: uruchom pipeline na 7 dni i porównaj. Zaliczone, jeśli agent razem z tobą ponownie odkryje co najmniej 2 opublikowane znaleziska High/Medium z działającymi PoC. **Kiedy przerwać.** Przerwij po 3 konkursach na żywo bez żadnego ważnego znaleziska.

**Źródła:** [Regulamin Immunefi](https://immunefi.com/rules/) · [Konkursy Cantina](https://cantina.xyz/competitions) · [shattered.io: porównanie platform](https://shattered.io/fr/?p=1682) · [Zealynx: benchmark audytorów AI](https://academy.zealynx.io/blog/ai-auditor-118-finding-benchmark) · [Zealynx: Code4rena vs samodzielny trening bezpieczeństwa](https://academy.zealynx.io/blog/code4rena-vs-self-directed-security-training) · [Runtime Verification: ograniczenia konkursów audytowych](https://runtimeverification.com/blog/on-the-limitations-of-audit-competitions) · [Wytyczne oceny Sherlock](https://docs.sherlock.xyz/audits/judging/guidelines)

---

## 8. Konkursy z nagrodami za zadanie twórcze (polskie „konkursy”, konkursy projektowe)

**Kategoria:** konkursy · **Realny dochód:** mediana 0-200 USD/mies., głównie w rzeczach, bardzo nierówno · **Potrzebny kapitał:** 0 (więcej, jeśli gonisz konkursy paragonowe) · **Wynik: 51** (E5 A13 F13 L11 R9) · **Zasady:** sprawdź każdy regulamin: wiele wymaga zgłoszenia wykonanego „samodzielnie” i przeniesienia praw autorskich; szkic wspierany przez AI z ludzkim dopracowaniem to tryb, którego da się bronić; legalne w Polsce: tak, z warunkami (bez zakupu jako warunku udziału, jeśli to w istocie gra losowa)

> Agent może czytać setki regulaminów konkursów tygodniowo i wstępnie szkicować zgłoszenia, czego robi niewielu hobbystów, ale nagrody są małe, głównie rzeczowe i oceniane za oryginalność, więc to przyjemne zajęcie poboczne o niskim pułapie, a nie główne źródło zarobku.

**Skąd płyną pieniądze.** Marka (lub instytucja) organizuje konkurs na podstawie regulaminu; jury wybiera najlepsze
„zadanie konkursowe” (hasło, krótkie opowiadanie, zdjęcie, film, odpowiedź na pytanie). Nagrody to zwykle rzeczy
(AGD, bilety, vouchery), czasem gotówka. Organizator pobiera 10% zryczałtowanego podatku od nagrody, gdy jest należny, i często dodaje
niewielką kwotę pieniężną na jego pokrycie. Marketplace'y projektowe (99designs) płacą zwycięskiemu projektantowi konkursu zorganizowanego przez klienta.

**Asymetria.** Większość uczestników znajduje konkursy na agregatorach i zgłasza się ręcznie; czytanie 4-8 stron regulaminu każdego
konkursu to nudna część, która odsiewa ludzi. Agent może obserwować agregatory i strony marek, zamieniać każdy
regulamin w listę kontrolną (wymagany zakup? paragon do zachowania? wiek/miejsce zamieszkania? termin? klauzula o AI lub „samodzielnie”?
przeniesienie praw autorskich? jury czy losowanie?) i szkicować 3 warianty dla tych, które pasują. Szanse na wygraną są niskie, bo jury wybiera jedno lub
kilka zgłoszeń spośród wielu; agent zwiększa liczbę dobrze dobranych zgłoszeń, a nie szanse na jedno zgłoszenie. Popularność takich
pipeline'ów wśród hobbystów: niezmierzona (nie znaleziono).

**Co robi agent.**
1. Obserwacja: codziennie przeszukuje publiczne strony z listami (np. agregatory konkursów) i strony marek; zapisuje URL konkursu i PDF regulaminu.
2. Filtrowanie: lokalny model wyciąga listę kontrolną zasad; odrzuca konkursy wymagające zakupu, którego i tak byś nie zrobił, te, które są
   losowaniami (loteria, wymaga zezwolenia i to inna gra), albo te, które zakazują AI lub wymagają w pełni własnej pracy, której nie możesz uczciwie zapewnić.
3. Szkic: płatny model przygotowuje 3 krótkie propozycje zgłoszenia na konkurs na podstawie twojego briefu (twoja historia, pomysł na zdjęcie, ton).
4. Weryfikacja: przepisujesz wybrane zgłoszenie własnymi słowami, dodajesz własne doświadczenie lub zdjęcie i sprawdzasz je z listą kontrolną.
5. Zgłoszenie: **bramka człowieka**: zgłaszasz ręcznie, z jednego własnego konta, i zachowujesz paragony, jeśli są wymagane.
6. Śledzenie: loguje zgłoszenia, wyniki i wartość nagród, żeby wyliczyć wartość na godzinę.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na maszynie) | Płatne API | Dlaczego |
|---|---|---|---|
| Przeszukiwanie i parsowanie regulaminów | tak, wszystkie PDF-y | nie | masowy polski tekst prawny, 24/7 |
| Wyciąganie listy kontrolnej zasad | tak | wyrywkowa kontrola przypadków granicznych | błędy tutaj unieważniają zgłoszenia |
| Pomysły i szkice zgłoszeń | pierwsze pomysły | 3 najlepsze szkice | liczą się kreatywność i polski styl |
| Ostateczne zgłoszenie | nie | nie | dopracowujesz je sam (oryginalność, prawa autorskie) |
| Śledzenie wyników | tak | nie | prosta ewidencja |

**Liczby.**
- e-konkursy.info pokazywał ok. 25-30 aktywnie promowanych konkursów w dniu 14.10.2026; przykłady: pralka za odpowiedź na pytanie (bez zakupu, koniec 31.10.2026), AGD za film o produkcie (wymagany zakup, koniec 31.12.2026), skarpetki za komentarz (bez zakupu) (e-konkursy.info, 14.10.2026).
- Przykład konkursu B2B: „Weź udział i wygraj konsultacje strategiczne!” firmy Enigma (6-13.03.2026): nagrodami były sesje konsultingowe, „nie podlegają wymianie na ekwiwalent pieniężny”, zgłoszenie „powinno być przygotowane samodzielnie”, decyzja jury ostateczna (regulamin, 03.2026).
- Konkursy na logo w 99designs: Bronze 289 EUR z ok. 30 koncepcjami, Silver 479 EUR ok. 60, Gold 859 EUR ok. 90 (cennik 99designs, 14.10.2026), więc pojedynczy projekt konkuruje z mniej więcej 30-90 koncepcjami na konkurs *(deklaracja platformy)*. Warunki 99designs (wersja z 30.06.2025) umieszczają zasady oryginalności w osobnej Originality Policy; wyraźnej klauzuli o AI w ogólnych warunkach nie znaleziono.
- Realne szanse na wygraną na zgłoszenie w polskich konkursach marek: nie znaleziono w publicznym źródle.

**Jak zacząć.**
1. Najpierw zbuduj parser regulaminów i uruchom go na 50 aktualnych konkursach; sprawdź ręcznie jego listę kontrolną na 10.
2. Wybierz typy konkursów, w których twoje prawdziwe życie daje przewagę (technologia, DIY, podróże, zdjęcia, które faktycznie robisz).
3. W pierwszym tygodniu weź udział w 10 konkursach z ręcznie dopracowanymi zgłoszeniami; loguj poświęcony czas i daty wyników.
4. Konkursy projektowe rozważ dopiero później; są zatłoczone i wymagają umiejętności projektowych wykraczających poza szkice.

**Zasady, podatki i ryzyka.**
- Zasady: wiele regulaminów wymaga utworu wykonanego „samodzielnie” i przeniesienia autorskich praw majątkowych; według polskiego prawa autorskiego ochrona obejmuje ludzką twórczość, więc surowy wynik modelu słabo pasuje do takiej klauzuli. Używaj modelu do pomysłów i redakcji, twórczy rdzeń zachowaj własny; pomijaj konkursy zakazujące AI.
- Jedna osoba, jedno konto, jedno zgłoszenie, chyba że regulamin pozwala na więcej; nigdy wiele kont.
- Polskie prawo: konkurs z jury i zadaniem twórczym nie jest grą losową; „loterie promocyjne” oparte na losowaniu to gry wymagające zezwolenia na podstawie ustawy o grach hazardowych i inna kategoria.
- Podatek w jednym zdaniu: nagrody z konkursów są opodatkowane 10% ryczałtem pobieranym przez organizatora, ze zwolnieniem dla małych nagród w ramach sprzedaży premiowej (art. 21 ust. 1 pkt 68 i art. 30 ust. 1 pkt 2 ustawy o PIT: zwolnione, jeśli jednorazowa nagroda „nie przekracza kwoty 2000 zł”; szczegóły w [03-ZASADY-PODATKI-RYZYKA.md](03-ZASADY-PODATKI-RYZYKA.md)).
- Ryzyka: pożeracz czasu, nagrody, których nie potrzebujesz (wartość przy odsprzedaży jest niższa), konkursy z wymaganym zakupem zamieniają się w wydatki.

**Ograniczenia.**
- Pułap jest niski, a wypłaty to głównie rzeczy, nie gotówka.
- Konkursy z jury nagradzają oryginalność; generyczne szkice AI przegrywają.
- Wiele konkursów to konkursy na komentarz w mediach społecznościowych z drobnymi nagrodami.
- Konkursy paragonowe wymagają zakupów i zachowania paragonów.
- Szanse na zgłoszenie pozostają niskie; wyniki przychodzą po tygodniach, więc informacja zwrotna jest powolna.

**Test pierwszego tygodnia.** Sparsuj 50 regulaminów i wyślij 10 ręcznie dopracowanych zgłoszeń; test zaliczony, jeśli lista kontrolna parsera jest poprawna dla co najmniej 9 z 10 wyrywkowo sprawdzonych regulaminów, a twój czas na zgłoszenie wynosi poniżej 20 minut. Wygrane oceń po 6 tygodniach.

**Kiedy przerwać.** Przerwij, jeśli po 8 tygodniach i 40 zgłoszeniach wartość otrzymanych nagród jest poniżej 200 PLN.

**Źródła:** [e-konkursy.info](https://www.e-konkursy.info/) · [Regulamin konkursu Enigma (03.2026)](https://www.enigma.com.pl/wp-content/uploads/2026/03/regulamin-konkursu.pdf) · [Cennik 99designs](https://en.99designs.de/pricing) · [Warunki korzystania z 99designs](https://en.99designs.de/legal/terms-of-use) · [Ustawa o PIT, rekord ELI (tekst jednolity Dz.U. 2026 poz. 592)](https://api.sejm.gov.pl/eli/acts/DU/1991/350)

---

## 9. Śledzenie promocji bankowych

**Kategoria:** roszczenia · **Realny dochód:** 50-150 USD/miesiąc średnio w skali roku (około 2500-6000 PLN/rok, mediana ~3500 PLN) · **Potrzebny kapitał:** 0 (przepuszczasz przez konta własną pensję i wydatki) · **Wynik: 51** (E4 A6 F14 L17 R10) · **Zasady:** automatyzacja w regulaminie: agent tylko czyta publiczne regulaminy, działasz ty; legalne w Polsce: tak, jedna prawdziwa tożsamość, jedno konto w banku zgodnie z ofertą

> Polskie banki płacą prawdziwą gotówkę za założenie i używanie kont oraz kart; agent, który czyta każdy regulamin i pilnuje każdego terminu, sprawia, że jest to mało pracochłonne i niezawodne, ale łączna kwota jest mała i ograniczona zasadami dla „nowych klientów”.

**Skąd płyną pieniądze.** Bank wypłaca premię za założenie konta lub karty i spełnienie warunków: miesięczne wpływy, określona liczba płatności kartą, logowania do aplikacji mobilnej, czasem lokata. Premia trafia na konto, zwykle w transzach przez kilka miesięcy. Z każdej oferty możesz skorzystać tylko raz w danym banku, w jego oknie dla „nowego klienta”.

**Asymetria.** Porównywarki już listują oferty (kontomaniak.pl pokazywał w październiku 2026 roku 11 promocji dla klientów indywidualnych), więc samo znajdowanie ofert nie daje przewagi. Przewaga leży w wykonaniu: przeczytaniu 10-20 stron regulaminu na ofertę, zapisaniu dokładnych warunków i niepominięciu ani jednej miesięcznej liczby płatności kartą czy wpływu. Ludzie tracą premie przez drobne potknięcia. Agent z kalendarzem i listą kontrolną to naprawia. Wykorzystanie AI w tym obszarze: niezmierzone (nie znaleziono); okno jest otwarte, dopóki banki prowadzą kampanie akwizycyjne.

**Co robi agent.**
1. Obserwacja: co tydzień czyta listę ofert w porównywarkach oraz strony promocji i regulaminy w PDF na stronach samych banków.
2. Filtrowanie: odrzuca oferty, w których nie jesteś „nowym klientem”, oferty tylko dla firm i oferty wymagające produktu kredytowego, którego nie chcesz.
3. Praca: zamienia każdy regulamin w listę kontrolną z datami (kwota wpływu, liczba płatności kartą, terminy, klauzule wyłączające, opłaty za zamknięcie konta).
4. Weryfikacja: płatny model ponownie czyta regulamin w poszukiwaniu pułapek (zwrot premii przy wcześniejszym zamknięciu, minimalny okres utrzymania, opłaty po promocji).
5. Działanie: bramka zatwierdzenia przez człowieka. Konto zakładasz sam; agent tylko przypomina, śledzi postępy i sprawdza, czy premia wpłynęła.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na rigu) | Płatne API | Dlaczego |
|---|---|---|---|
| Czytanie regulaminów w PDF | Wyciąganie warunków i dat | Brak | Długie dokumenty, prywatny kontekst |
| Przegląd pułapek | Brak | Opus 5.5 dla każdej przyjętej oferty | Przeoczona klauzula kosztuje całą premię |
| Miesięczne śledzenie | Porównanie wyeksportowanych wyciągów z listą kontrolną | Brak | Wyciągi bankowe zostają na rigu |
| Przypomnienia | Wpisy w kalendarzu i alerty | Brak | 24/7, trywialne |

**Liczby.**
- Oferty dla klientów indywidualnych na kontomaniak.pl (odczyt 14.10.2026, *(relacja zewnętrzna)*): Erste Bank do 1050 PLN, BNP Paribas 1100 PLN, mBank 1010 PLN, Credit Agricole 1000 PLN cashbacku, ING 800 PLN, karta kredytowa BNP Paribas 400 PLN, oszczędności w Pekao do 2700 PLN; kilka kończy się w połowie października lub w listopadzie 2026.
- „Nowy klient” oznacza brak konta w danym banku przez okres od 6 do 36 miesięcy, zależnie od banku (kontomaniak.pl, październik 2026).
- Podatek: nagrody ze „sprzedaży premiowej” są zwolnione z podatku, jeśli jednorazowa wartość „nie przekracza kwoty 2000 zł” (art. 21 ust. 1 pkt 68 ustawy o PIT); powyżej obowiązuje zryczałtowany podatek 10% („w wysokości 10 % wygranej lub nagrody”, art. 30 ust. 1 pkt 2). Kontomaniak podaje, że premie są wypłacane „w pełnej wysokości netto” *(relacja zewnętrzna)*: sprawdź w każdym regulaminie, kto płaci podatek.
- Realna suma roczna: żadne znalezione źródło jej nie mierzy; powyższy szacunek zakłada 3-5 ofert rocznie po 700-1100 PLN każda.

**Jak zacząć.**
1. Wypisz banki, w których już masz lub niedawno miałeś konto; one odpadają.
2. Niech agent zbuduje tabelę otwartych ofert z zasadami dla „nowego klienta” i terminami.
3. Wybieraj maksymalnie dwie oferty naraz, tak by warunki pasowały do twoich normalnych wydatków i wpływów z pensji.
4. Co miesiąc eksportuj wyciągi i pozwól lokalnemu modelowi sprawdzić postępy.

**Zasady, podatki i ryzyka.**
- Używaj wyłącznie własnej tożsamości i tylu kont, ile dopuszcza oferta; zakładanie wielu kont lub fałszywe polecenia łamią regulamin i mogą być oszustwem.
- Zwolnienie do 2000 PLN na nagrodę na podstawie art. 21 ust. 1 pkt 68 ustawy o PIT; powyżej zryczałtowany podatek 10% (zob. Liczby). Nagrody za polecenia mogą być opodatkowane inaczej; sprawdź każdy regulamin.
- Karty kredytowe oznaczają sprawdzenie w BIK (praktyka banków, nieweryfikowana ponownie w tym przebiegu); wiele nowych kart w krótkim czasie może obniżyć twoją ocenę przed kredytem hipotecznym.
- Ryzyka: niespełniony warunek, odmowa wypłaty premii przez bank na podstawie klauzul o „nadużyciach”, opłaty po okresie promocji.

**Ograniczenia.**
- Twardy limit: każdy bank raz na 6-36 miesięcy.
- Kwoty są małe w porównaniu z pensją DevOpsa.
- Co miesiąc trzeba przesunąć wiele przepływów; to praca administracyjna.
- Znajdowaniem ofert zajmują się już porównywarki.

**Test pierwszego tygodnia.** Niech agent zbuduje tabelę ofert i listę kontrolną dla jednej wybranej oferty, a potem porównaj ją z własną lekturą regulaminu. Test zaliczony, jeśli lista agenta wyłapuje każdy warunek, który znalazłeś, i co najmniej jeden, który przeoczyłeś. **Kiedy przerwać.** Przerwij, jeśli dwie premie z rzędu przepadną lub zostaną odmówione albo jeśli otwarte oferty dostępne dla ciebie spadną poniżej 1500 PLN rocznie.

**Źródła:** [kontomaniak.pl: promocje bankowe](https://kontomaniak.pl/promocje-bankowe) · [Tekst jednolity ustawy o PIT (ISAP)](https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19910800350/U/D19910350Lj.pdf)

---

## 10. Bug bounty dla aplikacji webowych i mobilnych z rekonesansem wspieranym przez AI

**Kategoria:** bounty · **Realny dochód:** 0-300 USD/miesiąc (przypadek medianowy: 0 w pierwszych 2-3 miesiącach, potem sporadyczne wypłaty za błędy o niskiej/średniej wadze) · **Potrzebny kapitał:** ~0-50 USD (tokeny API, VPS do callbacków out-of-band) · **Wynik: 48** (E6 A8 F12 L14 R8) · **Zasady:** praca z pomocą AI dozwolona, wymagana walidacja przez człowieka (HackerOne, Bugcrowd); legalne w Polsce: warunkowo (tylko w opublikowanym zakresie programu)

> Polowanie na błędy bezpieczeństwa w programach na HackerOne, Bugcrowd, Intigriti lub YesWeHack z agentami, którzy robią rekonesans i wstępną selekcję; legalne i dozwolone, ale przewagę AI ma już tysiące łowców, a reakcja na „AI slop” karze dokładnie tę grę na wolumen, do której zachęca agent, więc to pozycja ze środka tabeli.

**Skąd płyną pieniądze.** Firmy prowadzą publiczne lub prywatne programy na platformie i płacą za każde ważne, mieszczące się w zakresie, niezduplikowane znalezisko, wycenione według wagi w tabeli programu. Platforma wypłaca (przelew bankowy, PayPal lub podobnie, po formularzach podatkowych/tożsamości), gdy program zweryfikuje i nagrodzi raport. Duplikaty i raporty spoza zakresu nie dostają nic. Terminy: od dni do miesięcy, zależnie od weryfikacji. HackerOne wypłacił 89,1 mln USD w nagrodach w okresie 07.2025-06.2026 (deklaracja platformy).

**Asymetria.** Jest słabsza, niż wygląda. Polowanie z pomocą AI to już główny nurt: kodeks postępowania HackerOne „permits and encourages the responsible use of AI tools” przy rekonesansie, wykrywaniu i pracy nad proof-of-concept (odczyt 14.10.2026), więc same narzędzia nie dają przewagi. Pozostała asymetria jest wąska: (1) agenci czytają duże paczki JS, specyfikacje API i changelogi nowo dodanych lub nowo poszerzonych zakresów szybciej niż ludzie; (2) klasy błędów specyficzne dla AI (prompt injection, wyciek system promptu, niewłaściwa obsługa outputu), gdzie liczba ważnych raportów wzrosła o 222% w dwa lata (raport HackerOne 2026, deklaracja platformy). Okno na „wolumen” zamknęło się w latach 2025-2026: curl zakończył płatny program 31.01.2026, bo odsetek potwierdzonych podatności spadł z ~15% do poniżej 5% pod zalewem raportów generowanych przez AI, a Internet Bug Bounty HackerOne wstrzymał przyjmowanie nowych zgłoszeń 27.03.2026 (relacja zewnętrzna).

**Co robi agent.**
1. Obserwacja: codziennie odpytuje strony programów i zmiany zakresu (nowe programy, nowe zasoby, podniesione tabele nagród); zapisuje zasady zakresu jako ustrukturyzowane dane.
2. Filtr: zostawia tylko zasoby wprost objęte zakresem; odrzuca wszystko, co ma zapis „no automated scanning” dla typu zasobu, którego miałbyś dotknąć.
3. Praca (najpierw pasywnie): czyta publiczny JS, dokumentację OpenAPI, release notes i porównuje je dzień do dnia; proponuje hipotezy (IDOR, obejście uwierzytelniania, prompt injection w funkcjach LLM) z planem testów.
4. **Bramka ludzka:** czytasz plan testów i sprawdzasz go względem zasad programu i limitów zapytań, zanim jakiekolwiek zapytanie trafi do celu.
5. Weryfikacja: odtwarzasz ręcznie; agent szkicuje raport z dokładnymi krokami, wpływem i minimalnym PoC.
6. **Bramka ludzka:** zgłaszasz tylko odtworzone znaleziska mieszczące się w zakresie. Jeden dobry raport jest lepszy niż dziesięć spekulatywnych.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na rigu) | Płatne API | Dlaczego |
|---|---|---|---|
| Obserwacja zakresu i porównywanie zmian | Tak, 24/7 | Nie | Tanio, stale, dane prywatne |
| Czytanie JS/API i lista hipotez | Tak, pierwsze przejście | Opus 5.5 dla 5 najlepszych tropów | Wolumen lokalnie, osąd płatnie |
| Plan testów vs zasady programu | Szkic | Przegląd Opus 5.5 | Ryzyko prawne wymaga najlepszego rozumowania |
| Pisanie raportu | Szkic | Finalna redakcja Opus 5.5 | Jakość raportu decyduje o weryfikacji |

**Liczby.**
- 89,1 mln USD wypłat nagród na HackerOne, 07.2025-06.2026; przeanalizowano 92 194 ważne raporty (HackerOne Security Research Report 2026, deklaracja platformy). Prosta średnia ok. 970 USD na ważny raport; mediana na raport nieopublikowana (nie znaleziono).
- Liczba otwartych ważnych raportów wzrosła o 131% z 2024 do 2026, a walidacja krytycznego znaleziska trwa 30 godzin (ten sam raport): weryfikacja jest wąskim gardłem, więc opóźnienia wypłat rosną.
- curl: ~7 lat, 87 potwierdzonych podatności, ponad 100 000 USD wypłacone; zakończony 31.01.2026 (BleepingComputer 22.01.2026; blog Pinggy, relacja zewnętrzna).
- Medianowy dochód łowcy: nie znaleziono w źródle pierwotnym. Większość kont na każdej platformie nigdy nie zarabia żadnej nagrody (szeroko raportowane, nie znaleziono aktualnej twardej liczby).
- Koszt: lokalna inferencja ~za darmo; przegląd 5 tropów tygodniowo przez Opus, kilka USD/tydzień (szacunek).

**Jak zacząć.**
1. Załóż konta na HackerOne i Intigriti (z siedzibą w UE, wypłaty w euro); wypełnij formularze podatkowe/tożsamości przed pierwszą wypłatą.
2. Przeczytaj kodeks postępowania każdej platformy; zapisz klauzule dotyczące AI.
3. Wybierz 2-3 programy z szerokim zakresem, wyraźną deklaracją safe harbor i opublikowaną tabelą wypłat; preferuj programy z funkcjami AI/LLM w zakresie.
4. Najpierw zbuduj obserwatora zakresu i pasywny czytnik JS/API; żadnych narzędzi do aktywnego testowania, dopóki nie pojawi się trop.
5. Zrób jeden ręczny raport od początku do końca dla znaleziska o niskiej wadze, żeby poznać proces weryfikacji.

**Zasady, podatki i ryzyka.**
- HackerOne zakazuje „Generating large volumes of low-signal or non-actionable reports” oraz „Submitting unverified or fabricated vulnerability claims”; sankcje: ostatnie ostrzeżenie, 12-miesięczny ban, ban na stałe (Code of Conduct, odczyt 14.10.2026).
- Bugcrowd: „Manually review and validate any vulnerability report you've created with the help of GenAI tools before submitting it” (Code of Conduct, odczyt 14.10.2026). Warunki Bugcrowd wymagają też zatrzymania automatycznych narzędzi przy pierwszych oznakach spadku wydajności.
- Prawo polskie (tekst jednolity Kodeksu karnego, tekst w ISAP z datą 28.08.2026): zastosowanie mają art. 267 (nieuprawniony dostęp), 269a (zakłócanie systemów) i 269b (narzędzia/hasła do tych przestępstw). Art. 269c wyłącza karalność tylko z art. 267 § 2 i 269a przy działaniu „wyłącznie w celu zabezpieczenia systemu” z niezwłocznym powiadomieniem i bez szkody; art. 269b § 1a wyłącza karalność narzędzi stworzonych w celu zabezpieczenia. NIE obejmuje to art. 267 § 1 (przełamanie zabezpieczenia) ani działania bez zgody właściciela. Praktyczna zasada: testuj tylko to, na co program zezwala na piśmie. W tym tekście nie znalazłem nowszej nowelizacji dotyczącej badaczy bezpieczeństwa.
- Podatek: wypłaty z zagranicznych platform to dochód osobisty polskiego rezydenta podatkowego (PIT-36, skala lub przez jednoosobową działalność gospodarczą); szczegóły w rozdziale o zasadach.
- Ryzyka: duplikaty (większość raportów), oceny N/A obniżające twój signal score, bany za niskiej jakości wolumen, odpowiedzialność prawna, jeśli agent dotknie hostów spoza zakresu.

**Ograniczenia.**
- Wszyscy mają te same narzędzia AI; asymetria to szybkość na nowym zakresie, a nie możliwości.
- Zaległości w weryfikacji oznaczają, że pieniądze przychodzą po tygodniach lub miesiącach.
- Prawdziwe znaleziska wymagają ręcznego odtworzenia, które zjada większość z 10 h/tydzień.
- Prywatne zaproszenia (gdzie konkurencja jest mniejsza) wymagają historii osiągnięć, której jeszcze nie masz.
- Wiele programów wprost zakazuje automatycznego skanowania.

**Test pierwszego tygodnia.** Obserwuj zakres 3 programów przez 7 dni, generuj tropy lokalnie, ręcznie sprawdź 10 najlepszych; zaliczone, jeśli co najmniej 1 znalezisko zostanie odtworzone i zgłoszone z PoC (akceptacja w 1. tygodniu nie jest wymagana). **Kiedy przerwać.** Przerwij, jeśli po 8 tygodniach nie masz żadnego zaakceptowanego (zweryfikowanego jako ważny) raportu albo jeśli którykolwiek raport dwa razy zostanie zamknięty jako N/A z powodu niskiej jakości.

**Źródła:** [HackerOne Code of Conduct](https://www.hackerone.com/policies/code-of-conduct) · [HackerOne Security Research Report 2026](https://www.hackerone.com/report/hacker-powered-security) · [Bugcrowd Code of Conduct](https://www.bugcrowd.com/resources/essentials/code-of-conduct/) · [Bugcrowd Standard Disclosure Terms](https://www.bugcrowd.com/resources/standard-disclosure-terms/) · [BleepingComputer: curl kończy bug bounty](https://www.bleepingcomputer.com/news/security/curl-ending-bug-bounty-program-after-flood-of-ai-slop-reports/) · [Pinggy: curl summer of bliss](https://pinggy.io/blog/curl_ai_slop_summer_of_bliss/) · [Kodeks karny, tekst jednolity (ISAP)](https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19970880553/U/D19970553Lj.pdf)

---

## 11. Ekspercka praca przy trenowaniu AI (Outlier, DataAnnotation, Alignerr, Mindrift)

**Kategoria:** praca płatna · **Realny dochód:** 300-900 USD/mies. przy 10 h/tydz. własnego czasu, przypadek medianowy, z pustymi tygodniami · **Potrzebny kapitał:** 0 · **Wynik: 47** (E12 A2 F10 L15 R8) · **Zasady:** wyłącznie praca ludzka; agent dozwolony tylko wokół pracy (szukanie projektów, planowanie, własna nauka), nigdy do tworzenia odpowiedzi; legalne w Polsce: tak

> Dobrze płatna ekspercka praca ludzka (przegląd kodu, pisanie po polsku, ocenianie RLHF), którą laboratoria AI kupują właśnie dlatego, że jest ludzka, więc agent nie może wykonać płatnej części, a asymetria jest bliska zeru; opisuję ją dla uczciwości, nie jako najlepszy wybór.

**Skąd płyną pieniądze.** Laboratoria AI płacą platformom za ludzkie oceny; platformy płacą wykonawcom za godzinę lub za
zadanie. Outlier płaci co tydzień we wtorki przez PayPal, Airtm lub ACH (FAQ Outlier, odczyt 14.10.2026). DataAnnotation płaci
przez PayPal, a środki docierają w ciągu kilku dni od zlecenia wypłaty (FAQ DataAnnotation, 2026). Większość platform wymaga nieopłacanych
testów kwalifikacyjnych przed jakąkolwiek płatną pracą.

**Asymetria.** Odwrócona. Klientowi chodzi właśnie o ludzkie dane do trenowania i ewaluacji modeli; użycie modelu
do pisania odpowiedzi zatruwa te dane. Jedyna uczciwa dźwignia leży poza zadaniem: agent, który monitoruje,
które projekty są otwarte, śledzi twoją efektywną stawkę godzinową na projekt i pomaga ci uczyć się do testów kwalifikacyjnych
w twojej najmocniejszej dziedzinie (DevOps/kodowanie, polski). Oszczędza to może 1-2 godziny tygodniowo na szukaniu, nie więcej.

**Co robi agent.**
1. Obserwacja: wklejasz lub eksportujesz listę projektów, którą już widzisz, do lokalnego trackera (bez automatycznego dostępu do konta wykonawcy).
2. Filtrowanie: lokalny model układa projekty według deklarowanej stawki, dopasowania do twoich umiejętności i zalogowanej efektywnej stawki.
3. Przygotowanie: płatny model tworzy notatki do nauki i pytania ćwiczeniowe z dziedziny testu kwalifikacyjnego (nie sam test).
4. Praca: **ty** wykonujesz każde zadanie ręcznie. Żaden model nie dotyka treści zadań.
5. Weryfikacja: tracker loguje godziny, liczbę zadań i wypłaty; oznacza projekty, których efektywna stawka spada poniżej twojego minimum.
6. Działanie: **bramka człowieka**: sam decydujesz, który projekt przyjąć i kiedy z niego zrezygnować.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na maszynie) | Płatne API | Dlaczego |
|---|---|---|---|
| Śledzenie i ranking projektów | tak | nie | prywatny rejestr twoich zarobków |
| Analityka efektywnej stawki | tak | nie | prosta arytmetyka i podsumowania |
| Materiały do nauki z dziedziny | szkice | sprawdzenie poprawności | błędne notatki kosztują oblany test |
| Wykonywanie zadań | nigdy | nigdy | klient płaci za ludzki osąd |

**Liczby.**
- Outlier: nowi wykonawcy 15-22 USD/h; minimum 15-20, maksimum 35-50 USD/h (Breaking Even, analiza oparta na Reddicie, dane 29.05-17.08.2026) *(relacja zewnętrzna)*.
- Outlier wg typu zadania: ogólne RLHF 18-28 USD/h, przegląd kodu 28-45 USD/h, poziom ekspercki 35-60 USD/h (Breaking Even, 05.2026, aktual. 09.2026) *(relacja zewnętrzna)*.
- Outlier, eksperci od pisania po polsku: średnio ok. 15 USD/h za podstawową pracę projektową (ogłoszenie Outlier widoczne w wynikach wyszukiwania, 10.2026; strona ogłoszenia zwraca teraz 404) *(deklaracja platformy)*.
- DataAnnotation: ogólne 25-50+ USD/h, wielojęzyczne 20+ USD/h, kodowanie 40-150+ USD/h (FAQ DataAnnotation, 2026) *(deklaracja platformy)*; lista krajów nie jest publikowana.
- Alignerr: minimum 25 USD/h, maksimum 80-125 USD/h, ale wiele nieopłacanych ocen kwalifikacyjnych (Breaking Even, 04-09.2026) *(relacja zewnętrzna)*.
- „Pusta kolejka” wspomniana w 231 z 1532 dyskusji na Reddicie; pilnowanie kolejki obniża efektywną płacę o 20-30% (Breaking Even, 05.2026) *(relacja zewnętrzna)*.
- Efektywne stawki są o 20-40% niższe niż z wyliczeń za zadanie po doliczeniu szukania zadań (CareerSeeker, 07.07.2026) *(relacja zewnętrzna)*.

**Jak zacząć.**
1. Zgłoś się do Outlier (najszerszy zasięg językowy/geograficzny, są polskie projekty) i Mindrift (opisywany jako przyjaźniejszy dla wykonawców spoza USA); spróbuj DataAnnotation, ale spodziewaj się odrzucenia ze względu na kraj.
2. Wybierz ścieżkę programistyczną lub polskojęzyczną; testy kwalifikacyjne rozwiązuj sam.
3. Przygotuj lokalny arkusz lub log w SQLite z godzinami, zadaniami i zarobkami na projekt.
4. Zbuduj małego lokalnego agenta rankingującego listę projektów, którą eksportujesz ręcznie.

**Zasady, podatki i ryzyka.**
- Użycie AI: wyraźnych publicznych klauzul nie znaleziono w FAQ Outlier ani DataAnnotation (sprawdzono 14.10.2026), ale używanie LLM do tworzenia odpowiedzi w ramach danych ludzkich niweczy cel umowy, a platformy badawcze, takie jak Prolific, mówią uczestnikom, by nie używali LLM, chyba że jest to dozwolone. Traktuj odpowiedzi pisane przez model jako zakazane.
- Polskie prawo: legalne; jesteś niezależnym wykonawcą zagranicznej firmy.
- Podatek w jednym zdaniu: dochód z zagranicznej platformy jest opodatkowany PIT w zeznaniu rocznym (skala 12%/32% albo przez działalność); szczegóły w rozdziale o zasadach.
- Ryzyka: zgłaszane są usunięcia z projektów bez wyjaśnienia i niezapłacone faktury przez 30+ dni (Breaking Even, 02-09.2026) *(relacja zewnętrzna)*; Scale AI (właściciel Outlier) mierzyło się z pozwami o kradzież wynagrodzeń i błędną klasyfikację zatrudnienia w 12.2024-01.2025 (Wikipedia).

**Ograniczenia.**
- Brak dźwigni agenta w płatnej pracy: dochód to ściśle godziny × stawka.
- Zużywa twoje cenne 10 godzin, które mogłyby napędzać pomysły z dźwignią agenta.
- Kolejki są zmienne; projekt może zniknąć z dnia na dzień.
- Na niektórych platformach listy krajów wykluczają Polskę.
- Nieopłacany onboarding i oceny kwalifikacyjne obniżają realną stawkę.

**Test pierwszego tygodnia.** Zalicz co najmniej jedną płatną kwalifikację i zaloguj 5 płatnych godzin; test zaliczony, jeśli efektywna stawka wynosi co najmniej 20 USD/h, wliczając czas szukania.

**Kiedy przerwać.** Przerwij, jeśli efektywna stawka utrzymuje się poniżej 15 USD/h przez 3 tygodnie albo nie dostajesz pracy przez 2 tygodnie.

**Źródła:** [Breaking Even: Outlier vs DataAnnotation vs Alignerr pay](https://breakingeven.online/blog/outlier-vs-dataannotation-vs-alignerr-pay-comparison) · [Breaking Even: Outlier pay per hour 2026](https://breakingeven.online/blog/outlier-ai-pay-per-hour-2026) · [Breaking Even: AI training jobs tier list 2026](https://breakingeven.online/blog/ai-training-jobs-2026-platform-tier-list) · [DataAnnotation FAQ](https://www.dataannotation.tech/faq) · [Outlier FAQ](https://outlier.ai/faq) · [AI Trainer: DataAnnotation vs Outlier](https://aitrainer.work/compare/dataannotation-vs-outlier) · [CareerSeeker: data annotation jobs 2026](https://careerseeker.ai/data-annotation-jobs/) · [Wikipedia: Scale AI](https://en.wikipedia.org/wiki/Scale_AI) · [WU Vienna: Detect and prevent AI in online surveys](https://www.wu.ac.at/fileadmin/wu/d/cc/exp/PDFs/Detect_and_Prevent_AI_in_Online_Surveys_Guide.pdf)

---

## 12. Arbitraż na marketplace'ach (OLX, Allegro, Vinted)

**Kategoria:** arbitraż · **Realny dochód:** 50-400 USD/miesiąc (mediana ~150 USD) · **Potrzebny kapitał:** 500-1500 USD w towarze · **Wynik: 45** (E7 A9 F11 L10 R8) · **Zasady:** automatyzacja w regulaminie: scraping niedozwolony na Allegro, oficjalne API tylko dla własnych ofert; legalne w Polsce: warunkowo (limity handlu, DAC7)

> Kupowanie niedoszacowanych rzeczy z drugiej ręki i ich odsprzedaż działa, ale w legalnej wersji nie da się skanować marketplace'ów botami, więc agent pomaga ci oceniać i wystawiać, a nie polować na dużą skalę.

**Skąd płyną pieniądze.** Kupujesz rzecz wystawioną za tanio (słabe zdjęcia, zła kategoria, sprzedawcy się spieszy) i odsprzedajesz ją z lepszym ogłoszeniem, na tym samym lub innym marketplace. Kupujący płacą przez platformę; Allegro i Vinted wypłacają środki na twoje konto bankowe po dostawie. Zysk to cena odsprzedaży minus cena zakupu, opłaty platformy i wysyłka.

**Asymetria.** Większość prywatnych odsprzedawców nadal ocenia rzeczy na oko i pisze ogłoszenia ręcznie. Model wizyjny potrafi odczytać rozmazane zdjęcia, wyłapać numery modeli i w kilka sekund napisać pełne ogłoszenie. Ale strona polowania jest już chroniona: Allegro używa DataDome, „jednego z najpopularniejszych komercyjnych systemów antybotowych”, który sprawdza „twoją sygnaturę TLS, nagłówki HTTP i wzorce zachowań” (Scrapfly, 06.10.2026, *(relacja zewnętrzna)*). Przewaga dotyczy więc tylko oceniania i wystawiania, nie znajdowania.

**Co robi agent.**
1. Obserwacja: tylko przez dozwolone kanały: alerty zapisanych wyszukiwań, które ustawiasz w każdej aplikacji, i ogłoszenia, które sam otwierasz.
2. Filtrowanie: wklejasz lub przekazujesz ogłoszenie; lokalny model czyta zdjęcia i tekst, rozpoznaje dokładny model i stan.
3. Praca: szacuje cenę odsprzedaży na podstawie sprzedanych lub porównywalnych ogłoszeń, które wyszukujesz; liczy marżę netto po opłatach i wysyłce.
4. Weryfikacja: bramka zatwierdzenia przez człowieka przed każdym zakupem.
5. Działanie: po zakupie agent szkicuje nowe ogłoszenie (tytuł, opis, kolejność zdjęć); na Allegro możesz publikować własne oferty przez REST API.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na rigu) | Płatne API | Dlaczego |
|---|---|---|---|
| Czytanie ogłoszenia | Wyciąganie tekstu i pierwsza wycena | Brak | Prywatnie, tanio, wiele dziennie |
| Analiza zdjęć | Brak (model na rigu jest tekstowy) | Tani model wizyjny | Wymaga wizji |
| Decyzja o marży | Szkic obliczeń | Sprawdzenie przez Opus 5.5 dla rzeczy powyżej 300 PLN | Prawdziwe pieniądze |
| Tekst ogłoszenia | Szkic po polsku i angielsku | Brak | Tekst masowy |

**Liczby.**
- API Buy eBaya (Browse API) mają status „Limited Release” i są „intended for eBay partners only”; produkcja wymaga zatwierdzenia w eBay Partner Network, „There is no guarantee that your application for production use of the APIs will be approved” (dokumentacja deweloperska eBay, odczyt 14.10.2026).
- Dokumentacja Allegro REST API wymienia endpointy sprzedawcy, takie jak `GET /sale/offers` dla własnych ofert; w dokumentacji nie znalazłem publicznego wyszukiwania ofert innych sprzedawców (odczyt 14.10.2026).
- DAC7: platforma zgłasza sprzedawcę do urzędu skarbowego, chyba że ma on mniej niż 30 transakcji sprzedaży i poniżej 2000 EUR w roku; dwa polskie artykuły opisują ten próg różnie (antyweb.pl mówi o obu warunkach, fashionbiznes.pl o dowolnym z nich), więc zakładaj wariant „dowolny”. W kwietniu 2025 roku polski urząd skarbowy miał dane DAC7 o ponad 487 000 osób z platform zarejestrowanych za granicą, takich jak Vinted (fashionbiznes.pl, 23.04.2025).
- Mediana marży na jednej transakcji: nie znaleziono. Zmierz ją sam.

**Jak zacząć.**
1. Wybierz jedną wąską niszę, którą znasz (na przykład używane karty graficzne albo obiektywy).
2. Ustaw alerty zapisanych wyszukiwań w OLX, Allegro i Vinted dla tej niszy.
3. Zbuduj agenta jako narzędzie „drugiej opinii”: wklejasz link lub zrzut ekranu, a on zwraca model, ryzyka związane ze stanem, przedział cen i marżę netto.
4. Złóż wniosek o dostęp do Allegro REST API, żeby wystawiać własne rzeczy.

**Zasady, podatki i ryzyka.**
- Allegro zabrania scrapingu i pobierania swoich treści bez zgody; automatyczny dostęp jest możliwy tylko przez REST API (streszczenie regulaminu Allegro, źródło zewnętrzne; pełny regulamin zwrócił naszemu pobieraniu HTTP 403, przeczytaj go sam).
- Sprzedaż własnych rzeczy osobistych po upływie sześciu miesięcy od końca miesiąca, w którym je kupiłeś, nie jest dochodem podlegającym opodatkowaniu (art. 10 ust. 1 pkt 8 ustawy o PIT); kupowanie w celu odsprzedaży to handel.
- Handel bez firmy jest dozwolony w 2026 roku do 10 813,50 PLN przychodu na kwartał; powyżej tej kwoty rejestrujesz się w CEIDG w ciągu 7 dni (money.pl, 19.08.2026). Podatek w PIT-36.
- Ryzyka: podróbki, rzeczy uszkodzone w transporcie, zwroty, powolna sprzedaż, limity konta za zachowanie „profesjonalne” na platformach konsumenckich.

**Ograniczenia.**
- Na Allegro nie ma legalnego polowania botem; agent nie wyprzedzi ludzkich snajperów przy świeżych ogłoszeniach.
- Kwartalny limit przychodu jest mały: około 3600 PLN sprzedaży miesięcznie, zanim musisz zarejestrować działalność.
- Twój czas idzie na spotkania, pakowanie i wysyłkę, nie na pracę z AI.
- Wielu doświadczonych handlarzy zna ceny w swojej niszy na pamięć.

**Test pierwszego tygodnia.** Uruchamiaj agenta przez 7 dni na każdym ogłoszeniu, które przysyłają ci zapisane wyszukiwania. Test zaliczony, jeśli znajdzie ≥3 rzeczy z szacowaną marżą netto ≥20%, z którymi zgadzasz się po ręcznym sprawdzeniu. Kup najwyżej jedną. **Kiedy przerwać.** Przerwij, jeśli po miesiącu zysk netto na godzinę twojego czasu jest niższy niż polska minimalna stawka godzinowa.

**Źródła:** [Wymagania eBay Buy API](https://developer.ebay.com/api-docs/buy/static/buy-requirements.html) · [Dokumentacja Allegro REST API](https://developer.allegro.pl/documentation) · [Scrapfly: scraping Allegro](https://scrapfly.io/blog/posts/how-to-scrape-allegro) · [antyweb: DAC7 Allegro OLX Vinted](https://antyweb.pl/allegro-olx-vinted-dac7) · [fashionbiznes: dane DAC7](https://fashionbiznes.pl/urzad-skarbowy-ma-juz-dane-z-vinted-i-innych-platform-liczby-robia-wrazenie/) · [money.pl: działalność nierejestrowana 2026](https://direct.money.pl/artykuly/porady/dzialalnosc-nierejestrowana-2026-limit-10-813,50-zl,-po-przekroczeniu-7-dni-na-ceidg) · [Tekst jednolity ustawy o PIT (ISAP)](https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19910800350/U/D19910350Lj.pdf)

---

## 13. Bounty za zgłoszenia open source

**Kategoria:** bounty · **Realny dochód:** 0-150 USD/miesiąc (przypadek medianowy: blisko 0) · **Potrzebny kapitał:** 0 USD (plus kilka USD na tokeny API) · **Wynik: 44** (E3 A5 F13 L14 R9) · **Zasady:** praca z pomocą AI dozwolona w większości repozytoriów, często wymagane ujawnienie, niektóre projekty zakazują PR-ów od AI; legalne w Polsce: tak

> Naprawianie zgłoszeń na GitHubie z przypisaną nagrodą pieniężną (Algora, Opire, IssueHunt, Gitcoin, zgłoszenia finansowane przez Polar) za pomocą agenta kodującego; legalne i proste, ale w październiku 2026 każde widoczne bounty jest oblegane przez agentów innych ludzi, więc asymetria w większości zniknęła i pozycja jest nisko.

**Skąd płyną pieniądze.** Maintainer lub sponsor przypisuje pieniądze do zgłoszenia na GitHubie (etykieta Algory to „💎 Bounty”; bounty w Opire zaczynają się od 20 USD). Wielu programistów „podejmuje próbę”; maintainer merguje jeden PR, a nagroda trafia przez platformę do jego autora (Algora oznacza ją jako „💰 Rewarded”). Opire zaznacza, że płatność nie jest automatyczna: „the creator arranges payment only if the pull request meets the issue requirements” (odczyt 14.10.2026). Zwycięzca bierze wszystko; drugie najlepsze PR-y nie zarabiają nic. Kanałów wypłat i opłat nie zweryfikowałem ponownie w tym researchu (sprawdź dokumentację każdej platformy przed pierwszym zgłoszeniem roszczenia).

**Asymetria.** Odwrócona. W 2024 roku agent kodujący dawał przewagę; w 2026 roku to domyślny uczestnik. Wyszukiwanie na GitHubie 14.10.2026: otwarte bounty tscircuit miały po 40, 40 i 73 komentarze, a jedno otwarte zgłoszenie z bounty w innym repozytorium miało 1447 komentarzy, w większości automatycznych roszczeń. Tekst z czerwca 2026 opisuje fałszywe repozytorium z „bounty” zbudowane jako pułapka, w którą wpadli agenci AI, ujawniając swoje prompty (s-anand.net, relacja zewnętrzna). Maintainerzy stawiają opór: GitHub 27.08.2026 udostępnił opcje wyłączenia PR-ów, ograniczenia ich do współpracowników lub limitowania równoczesnych zewnętrznych PR-ów; Ghostty w 01.2026 przeszło na politykę zerowej tolerancji ze stałymi banami; Gentoo zakazuje wkładu generowanego maszynowo; NetBSD traktuje kod z AI jako „skażony” (relacje zewnętrzne). Jedyna pozostała przewaga to niszowe, trudne bounty (Scala/ZIO, Rust, embedded), gdzie tani agent zawodzi, a ekspert z agentem odnosi sukces.

**Co robi agent.**
1. Obserwacja: co godzinę przeszukuje GitHub pod kątem etykiet bounty; zapisuje kwotę, repozytorium, wiek, liczbę komentarzy, otwarte PR-y.
2. Filtr: odrzuca zgłoszenia z więcej niż 5 komentarzami o próbach lub z jakimkolwiek otwartym PR; odrzuca repozytoria, których CONTRIBUTING.md zakazuje PR-ów od AI lub roszczeń „/attempt”; zostawia repozytoria, które możesz zbudować i przetestować lokalnie.
3. Praca: agent w sandboksie odtwarza błąd, pisze nieprzechodzący test, a potem poprawkę.
4. Weryfikacja: pełny zestaw testów plus przegląd diffa przez Opus 5.5 pod kątem stylu maintainera i kryteriów akceptacji zgłoszenia.
5. **Bramka ludzka:** czytasz diff, ujawniasz pomoc AI tam, gdzie repozytorium tego wymaga, i otwierasz jeden PR na bounty. Nigdy nie zgłaszaj roszczeń masowo.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na rigu) | Płatne API | Dlaczego |
|---|---|---|---|
| Obserwacja i filtrowanie bounty | Tak, 24/7 | Nie | Czysty wolumen, bez potrzeby rozumowania |
| Czytanie repozytorium i odtworzenie błędu | Tak | Nie | Długi kontekst, prywatny sandbox |
| Poprawka trudnych zgłoszeń | Pierwsza próba | Opus 5.5 lub tanie API do kodowania | Tylko trudne zgłoszenia da się wygrać |
| Przegląd diffa przed PR | Nie | Opus 5.5 | O wypłacie decyduje zaufanie maintainera |

**Liczby.**
- Otwarte zgłoszenia na GitHubie z etykietą Algory „💎 Bounty”: 549; zgłoszenia oznaczone „💰 Rewarded” i zamknięte w ostatnich 12 miesiącach: 249 (GitHub search API, 14.10.2026). Te 249 nagrodzonych zgłoszeń to cały światowy tort na rok dla tej etykiety.
- Spośród pierwszych 100 nagrodzonych zgłoszeń większość pochodziła z kilku organizacji: archestra-ai 36, zio 22, projectdiscovery 18, Cap-go 9 (to samo zapytanie, 14.10.2026).
- Nowe zgłoszenia „💎 Bounty”: 1446 utworzonych w 2025, 496 dotąd w 2026, ale tylko 1 utworzone i 3 nagrodzone w ciągu 3 miesięcy do 14.10.2026 (to samo zapytanie). Albo sponsorzy w połowie 2026 roku wycofali się z publicznych bounty z etykietą, albo platforma zmieniła sposób etykietowania zgłoszeń; przyczyny nie znalazłem, więc zweryfikuj to na samej platformie, zanim zainwestujesz czas.
- Minimalne bounty w Opire 20 USD (opire.dev, 14.10.2026).
- Spośród 1000 największych repozytoriów na GitHubie 118 ma spisane zasady dotyczące AI, a 51% z nich wymaga ujawnienia (relacja zewnętrzna, 07.2026).
- Medianowe zarobki na uczestnika: nie znaleziono.

**Jak zacząć.**
1. Użyj istniejącego konta GitHub; połącz je z Algorą i Opire; dokończ konfigurację wypłat i dane podatkowe.
2. Zbuduj obserwatora z powyższymi filtrami; loguj każde zauważone bounty, liczbę komentarzy i to, kto wygrał.
3. Wybierz stack, który znasz (Python, Go, narzędzia Terraform/DevOps), i tylko takie repozytoria.
4. Zrób jedno bounty w całości ręcznie z pomocą agenta, żeby poznać pętlę przeglądu u maintainera.

**Zasady, podatki i ryzyka.**
- Decydują zasady repozytorium: niektóre wprost zakazują PR-ów od AI (Gentoo) albo zakazują nieujawnionego użycia AI (Ghostty, 01.2026, relacja zewnętrzna). Najpierw przeczytaj CONTRIBUTING.md.
- GitHub zawieszał konta za masowe zgłaszanie PR-ów (jeden inżynier otworzył ponad 130 PR-ów w 72 godziny; relacja zewnętrzna, 09.2026). Masowe zgłaszanie roszczeń naraża twoją główną tożsamość na GitHubie, która jest też twoim CV.
- Legalność w Polsce: zwykła płatna praca programistyczna. Podatek: dochód osobisty wykazywany w PIT-36 (lub przez jednoosobową działalność gospodarczą); szczegóły w rozdziale o zasadach.
- Ryzyka: nieopłacona praca, gdy wcześniej zostanie zmergowany inny PR; maintainer może zamknąć bounty bez wypłaty.

**Ograniczenia.**
- Pula jest mała: ok. 249 nagrodzonych bounty z etykietą rocznie na całym świecie.
- Zwycięzca bierze wszystko w starciu z wieloma agentami.
- Łatwe zgłoszenia są zajmowane w ciągu godzin; trudne wymagają prawdziwej wiedzy dziedzinowej.
- Szkoda dla reputacji z odrzuconego PR-a od AI trwa dłużej niż samo bounty.

**Test pierwszego tygodnia.** Uruchom obserwatora na 7 dni i zgłoś PR-y do 3 bounty, które przechodzą filtry; zaliczone, jeśli 1 zostanie zmergowany albo maintainer powie, że jest głównym kandydatem. **Kiedy przerwać.** Przerwij, jeśli 8 tygodni przyniesie łącznie poniżej 100 USD albo jeśli którykolwiek maintainer oznaczy twój PR jako spam od AI.

**Źródła:** [Wyszukiwanie GitHub: otwarte bounty Algora](https://github.com/search?q=label%3A%22%F0%9F%92%8E+Bounty%22+state%3Aopen&type=issues) · [Opire](https://opire.dev/) · [Crypto Briefing: kontrola PR-ów na GitHubie](https://cryptobriefing.com/github-restricts-pull-requests-ai-slop/) · [Tianpan: agenci są tani, uwaga maintainera nie](https://tianpan.co/blog/2026/07/02/your-agents-are-cheap-maintainer-attention-isnt) · [s-anand: ekosystem agentów polujących na bounty](https://www.s-anand.net/blog/bounty-hunting-agent-ecosystem-2/)

---

## 14. Odsprzedaż wygasłych domen

**Kategoria:** arbitraż · **Realny dochód:** 0-100 USD/miesiąc (mediana bliska 0 w pierwszym roku, często ujemna po odnowieniach) · **Potrzebny kapitał:** 300-1500 USD rocznie na rejestracje i odnowienia · **Wynik: 37** (E3 A5 F12 L12 R5) · **Zasady:** automatyzacja w regulaminie: API rejestru i rejestratorów dozwolone w ramach ich regulaminów; legalne w Polsce: tak, ale nazwy oparte na znakach towarowych można stracić w sporze

> Agent może codziennie przesiać tysiące wygasających nazw pod kątem znaczenia i potencjału marki, ale sprzedaże są rzadkie, rynek jest stary i pełen narzędzi, więc ta okazja ląduje na dole listy.

**Skąd płyną pieniądze.** Rejestrujesz (lub zamawiasz w backorderze) nazwę, gdy wygaśnie, wystawiasz ją na sprzedaż na marketplace'ach takich jak Sedo, Afternic czy Dan i czekasz, aż kupi ją użytkownik końcowy. Marketplace pobiera prowizję (aktualne stawki: niezweryfikowane w tym przebiegu, strona pomocy Afternic zwróciła HTTP 403). Co roku płacisz za odnowienie, dopóki nazwa się nie sprzeda.

**Asymetria.** Wycena nazw to głównie ocena: czy to prawdziwe słowo, marka, rodzaj działalności, miasto plus usługa? Model językowy potrafi dokonywać takiej oceny na dużą skalę, po polsku i w innych językach, w których inwestorzy znający tylko angielski są słabi. Ale narzędzia do przechwytywania domen i wyceny istnieją od lat, a duzi inwestorzy już prowadzą duże zautomatyzowane portfele. Wykorzystanie AI przez konkurencję: niezmierzone (nie znaleziono); zakładaj wysokie w .com, niższe w .pl.

**Co robi agent.**
1. Obserwacja: codzienne listy wygasających i zwolnionych nazw (listy backorderów rejestratorów; dla .pl rejestr publikuje statystyki nazw zwolnionych z powodu braku odnowienia).
2. Filtrowanie: odrzuca znaki towarowe, imiona i nazwiska oraz literówki marek; zostawia ogólne polskie słowa, lokalne usługi, krótkie nazwy.
3. Praca: ocenia każdą nazwę (znaczenie, długość, popularność w wyszukiwarkach, porównywalne sprzedaże, które wyszukujesz).
4. Weryfikacja: płatny model przegląda 20 najlepszych pod kątem znaków towarowych i jakości.
5. Działanie: bramka zatwierdzenia przez człowieka. Rejestrujesz niewielką liczbę nazw i ustalasz ceny; nigdy nie rejestruj nazwy pokrywającej się z czyimś znakiem towarowym.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na rigu) | Płatne API | Dlaczego |
|---|---|---|---|
| Przesiewanie codziennych list wygasających domen | Ocena tysięcy nazw | Brak | Duża skala, 24/7, koszt bliski zera |
| Sprawdzenie znaków towarowych | Oznaczanie oczywistych zbieżności z markami | Przegląd krótkiej listy przez Opus 5.5 | Ryzyko prawne |
| Wycena | Szkic ceny na podstawie porównań | Brak | Niska stawka na jedną nazwę |
| Kontakt z kupującymi | Brak | Brak | Zimny kontakt z kupującymi łatwo uznać za spam; unikaj |

**Liczby.**
- Rejestr .pl obejmował 2 736 154 domeny, z około 1514 nowymi dziennie (dns.pl, odczyt 14.10.2026).
- Wejście do rankingu 100 największych sprzedaży DNJournal od początku 2026 roku (do 04.10.2026) wymaga co najmniej 95 000 USD; największa sprzedaż to AI.com za 70 000 000 USD. To wartości odstające, które nic nie mówią o typowej nazwie.
- Roczny odsetek sprzedaży portfela inwestora: w tym przebiegu nie znalazłem datowanego źródła. Często przytaczana liczba około 1% rocznie to folklor, dopóki nie znajdziesz źródła; przy takim tempie portfel 100 nazw sprzedaje około jednej nazwy rocznie.
- Koszt odnowienia jednej nazwy rocznie: zależy od rejestratora, niezweryfikowany w tym przebiegu.

**Jak zacząć.**
1. Wybierz jedną niszę, którą rozumiesz (polskie lokalne usługi albo słowa techniczne).
2. Przez miesiąc uruchamiaj agenta na codziennej liście wygasających domen, niczego nie kupując; zapisuj, które nazwy przechwytują inni.
3. Zarejestruj najwyżej 10 nazw i wystaw je na jednym marketplace.
4. Śledź koszt na nazwę na rok w zestawieniu ze sprzedażą.

**Zasady, podatki i ryzyka.**
- Nazwy kopiujące znak towarowy można stracić w sporze (UDRP lub Sąd Polubowny ds. Domen Internetowych dla .pl) i mogą one naruszać prawo znaków towarowych; odfiltruj je.
- Sprzedaż to przychód; powtarzalny handel to działalność gospodarcza, opodatkowana w PIT-36 (limit działalności nierejestrowanej 10 813,50 PLN na kwartał w 2026 roku, money.pl 19.08.2026).
- Ryzyka: odnowienia zjadają kapitał, większość nazw nigdy się nie sprzedaje, długie oczekiwanie.

**Ograniczenia.**
- Sprzedaże są rzadkie i losowe; rok może przynieść zero.
- Dobre nazwy przechwytują zawodowi drop-catcherzy, zanim je zobaczysz.
- Kapitał jest co roku zamrożony w odnowieniach.
- Przewaga oceny przez AI jest mała, bo narzędzia do wyceny już istnieją.

**Test pierwszego tygodnia.** Pozwól agentowi ocenić listy wygasających domen z 7 dni i wybrać 20 najlepszych nazw bez kupowania; sprawdź, które przechwycili inni. Test zaliczony, jeśli ≥5 z 20 przechwycił ktoś inny (agent widzi wartość, którą widzi rynek). **Kiedy przerwać.** Przerwij, jeśli po 12 miesiącach odnowienia przewyższają sprzedaż.

**Źródła:** [Rejestr dns.pl](https://www.dns.pl/) · [Ranking sprzedaży DNJournal od początku roku](https://www.dnjournal.com/ytd-sales-charts.htm) · [money.pl: działalność nierejestrowana 2026](https://direct.money.pl/artykuly/porady/dzialalnosc-nierejestrowana-2026-limit-10-813,50-zl,-po-przekroczeniu-7-dni-na-ceidg)

---

## 15. Wynajem bezczynnego rigu GPU

**Kategoria:** moc obliczeniowa · **Realny dochód:** mediana 0-50 USD/miesiąc netto (karty AMD prawie nie znajdują najemców) · **Potrzebny kapitał:** 0 USD (rig już posiadany) · **Wynik: 36** (E3 A3 F6 L18 R6) · **Zasady:** automatyzacja dozwolona (marketplace'y udostępniają API/CLI dla hostów); legalne w Polsce: tak (dochód trzeba zgłosić)

> Wystawienie rigu 4x R9700 na marketplace'ach GPU jest legalne i łatwe do zautomatyzowania, ale prawie każdy marketplace obsługuje tylko NVIDIA albo nie ma popytu na AMD, a polskie ceny prądu zjadają większość stawki za wynajem konsumenckiego GPU, więc ta okazja nie trafia do pierwszej dziesiątki.

**Skąd płyną pieniądze.** Najemcy płacą marketplace'owi za GPU-godzinę; marketplace pobiera opłatę i wypłaca hostowi (Vast.ai w USD; Clore.ai i Nosana we własnych tokenach). Minimalne kwoty i harmonogramy wypłat różnią się między platformami. Dochód istnieje tylko wtedy, gdy najemca zajmuje maszynę, a podczas wynajmu rig nie może uruchamiać moich własnych agentów.

**Asymetria.** Nie ma żadnej, która byłaby warta zachodu. Wynajem GPU to dojrzały rynek z konkurencją cenową, na którym hosty już stosują automatyczne zmiany cen. Jedyna przewaga, jaką dodaje agent, to przełączanie rigu między własnym użyciem a wynajmem, co nie tworzy popytu na karty AMD.

**Co robi agent.**
1. Obserwacja: co godzinę odpytuje API ofert marketplace'ów o ceny porównywalnych GPU i o wszelkie oferty AMD.
2. Filtrowanie: wylicza cenę progu rentowności = koszt prądu + opłata platformy + zużycie sprzętu; wystawia rig tylko wtedy, gdy cena rynkowa jest wyższa.
3. Działanie: BRAMKA CZŁOWIEKA przy pierwszym wystawieniu i ustaleniu ceny minimalnej; później agent wystawia i wycofuje ofertę w zatwierdzonym przedziale.
4. Przełączanie: wycofuje ofertę i wznawia serwowanie własnego modelu, gdy lokalne agenty mają pracę w kolejce.
5. Raport: co tydzień zarobki wobec zużytych kWh.

**Podział hybrydowy.**

| Krok | Lokalnie (DeepSeek-V4-Flash na rigu) | Płatne API | Dlaczego |
|---|---|---|---|
| Odpytywanie cen i wyliczenie progu rentowności | wszystko, zwykły Python | nic | deterministyczne, model niepotrzebny |
| Decyzje o wystawieniu | oparte na regułach | cotygodniowy przegląd przez Opus 5.5 | tanio; przeglądana jest tylko polityka |
| Przełączanie między własnym użyciem a wynajmem | harmonogram | nic | musi reagować w ciągu minut |

**Liczby.**
- Wsparcie AMD: Vast.ai ogłosił obsługę AMD Radeon/Instinct, ale w wersji beta, z szablonami ROCm *(Vast.ai, 2.04.2024)*. Zapytanie do publicznego API ofert Vast z 14.10.2026 nie zwróciło żadnych dostępnych do wynajęcia ofert pod nazwami MI100, MI210, MI300X, Radeon Pro W7900, RX 7900 XTX ani Radeon AI PRO R9700 *(własne zapytanie, 14.10.2026)*.
- Clore.ai: „Any farm/server with an NVIDIA GPU” *(FAQ platformy, 10.2026)*; opłata marketplace'u 1,8-2,5% spot, 5-10% on-demand.
- Nosana: tylko NVIDIA (RTX 30/40/50, A100, H100), tylko Linux, wypłaty w tokenie NOS *(dokumentacja, 10.2026)*.
- Salad, io.net, Akash, Runpod community, TensorDock: hostowanie konsumenckich kart AMD niepotwierdzone w ich dokumentacji w chwili pisania (nie znaleziono).
- Porównywalne stawki NVIDIA na Vast (za GPU-godzinę, mediana ofert on-demand): RTX 3090 0,175 USD, RTX 4090 0,535 USD, RTX 5090 0,635 USD *(własne zapytanie do API, po 64 oferty, 14.10.2026)*.
- Prąd: cena dla gospodarstw domowych w taryfie G11 w 2026 około 0,95 PLN/kWh brutto *(relacja zewnętrzna, voltflow.net, 04.2026)*; składnik sprzedaży energii 495,16 PLN/MWh netto *(URE, 10.02.2026)*. USD/PLN 3,9177 *(NBP, 13.10.2026)*.
- Szkic progu rentowności: pobór mocy karty R9700 około 300 W *(deklaracja dostawcy, nie pobrano ponownie)*; 4 karty plus host przy około 1,4 kW kosztują około 1,33 PLN/h = 0,34 USD/h. Nawet gdyby karty wynajmowały się po stawce RTX 3090 (0,70 USD/h za 4), 50% wykorzystania daje około 250 USD/miesiąc brutto minus około 120 USD za prąd minus opłata platformy: poniżej 100 USD/miesiąc, i to przy założeniu popytu na AMD, którego rynek nie wykazuje.

**Jak zacząć.**
1. Niczego nie kupuj. Sprawdź aktualną dokumentację dla hostów każdego marketplace'u pod kątem obsługi AMD/ROCm.
2. Jeśli któryś ją obsługuje: skonfiguruj dual-boot lub wydziel partycję z obrazem hosta Ubuntu zgodnie z wymaganiami; nigdy nie udostępniaj danych głównej stacji roboczej.
3. Wystaw jedno GPU po cenie progu rentowności plus 20% na 2 tygodnie, aby zmierzyć rzeczywisty popyt.

**Zasady, podatki i ryzyka.**
- Umowy z hostami wymagają dedykowanego, czystego środowiska; najemcy uruchamiają dowolne kontenery na twoim sprzęcie, więc odizoluj sieć.
- Prawo polskie: dochód z wynajmu uzyskany przez osobę prywatną jest opodatkowany jako najem prywatny lub inne źródła; wypłaty w tokenach to kryptowaluty (szczegóły w rozdziale o zasadach).
- Ryzyka: zużycie kart, ruch nadużyć od najemców na domowym IP, wahania cen tokenów w sieciach płacących tokenami.

**Ograniczenia.**
- Konsumenckie i stacyjne karty AMD są w 2026 praktycznie niemożliwe do wynajęcia na głównych marketplace'ach.
- Wynajem zabija główny atut tego kursu: darmowy lokalny model działający 24/7.
- Domowa przepustowość wysyłania i IP mieszkaniowe obniżają ocenę niezawodności maszyny.
- Polskie ceny prądu dla gospodarstw domowych są wysokie jak na standardy UE.

**Test pierwszego tygodnia.** Odpytaj API ofert każdego wymienionego marketplace'u o karty AMD. Test zaliczony, jeśli co najmniej jeden marketplace pokazuje 10+ wynajętych GPU AMD z 24+ GB VRAM po stawce powyżej 0,35 USD/h.

**Kiedy przerwać.** Test niezaliczony albo wykorzystanie poniżej 30% po 2 tygodniach wystawienia.

**Źródła:** [Ogłoszenie obsługi AMD przez Vast.ai](https://vast.ai/article/announcing-amd-support) · [Aktualizacja Vast.ai z kwietnia 2024](https://vast.ai/article/vast-april-product-update) · [Dokumentacja hostingu Vast.ai](https://docs.vast.ai/documentation/host/hosting-overview) · [Clore.ai](https://clore.ai/) · [Dokumentacja dla hostów Nosana](https://learn.nosana.com/hosts/grid.html) · [Taryfy URE na 2026](https://www.ure.gov.pl/en/communication/news/501,The-President-of-the-Energy-Regulatory-Office-URE-has-approved-the-tariffs-for-t.html) · [Voltflow: cena G11 w 2026](https://www.voltflow.net/blog/obliczanie-zuzycia-energii-elektrycznej-dom-2026) · [Kurs USD w NBP](https://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json)

---

## Odrzuceni kandydaci

Te pomysły pojawiły się w badaniu. Ich zautomatyzowana wersja albo łamie regulamin platformy lub prawo, albo
pieniądze są zbyt małe, żeby opłacał się agent. Tam, gdzie istnieje legalny, mniejszy wariant, podaję go.

### Farmienie airdropów i punktów

Co to jest: wczesne korzystanie z protokołów krypto, żeby późniejszy airdrop ich tokena cię nagrodził. Wersja skalowana przez AI to farmienie na wielu portfelach („sybil”): agent prowadzący wiele portfeli, żeby wyglądały jak wielu użytkowników.
Dlaczego odrzucone: wersja skalowana to dokładnie to, co projekty odfiltrowują i czego zabraniają. Linea razem z Nansen oznaczyła 516 960 z 1 297 203 uprawnionych adresów jako Sybile za „zautomatyzowane i skoordynowane działania na powiązanych portfelach” (The Block, 21.01.2025). LayerZero podało, że około 1 miliona z jego 6 milionów portfeli to farmerzy sybil, i wykluczyło ich, oferując tym, którzy sami się zgłosili, tylko 15% przydziału (The Defiant, 2024). Regulamin Galxe pozwala mu „ograniczyć liczbę Kont Użytkownika lub Portfeli Cyfrowych” i zawieszać konta z utratą nagród (Galxe Terms, aktualizacja 10.09.2025). Farmienie na wielu portfelach = naruszenie regulaminu = L0.
Legalny mały wariant: jedna prawdziwa tożsamość, jeden lub dwa portfele, rzeczywiste korzystanie z protokołów, których i tak byś używał. Agent tylko śledzi kampanie, kryteria uprawnienia, terminy, koszty gasu i okna odbioru oraz sprawdza adresy URL do odbioru względem oficjalnych źródeł (nigdy nie podpisuje automatycznie). Wartość na prawdziwego użytkownika to loteria: często 0, czasem kilkaset USD; medianowe kwoty na użytkownika w dropach z lat 2025-2026: nie znaleziono. Opłaty za gas i bridging zjadają małe przydziały.
Główne dodatkowe ryzyko: phishing na fałszywe airdropy. Drainery portfeli zabrały 494 mln USD w 2024 roku, a straty z phishingu wyniosły 84 mln USD w 2025 roku (raporty roczne Scam Sniffer). Nigdy nie pozwalaj agentowi trzymać kluczy do podpisywania.
Podatek: zbycie kryptowalut jest opodatkowane w Polsce (patrz 03-ZASADY-PODATKI-RYZYKA.md).

**Źródła:** [Filtr sybil Linea (The Block)](https://www.theblock.co/post/335979/linea-filters-over-half-a-million-sybil-addresses-from-upcoming-token-airdrop) · [Samozgłoszenia sybil w LayerZero (The Defiant)](https://thedefiant.io/news/defi/layerzero-tells-sybil-farmers-to-out-themselves-or-face-airdrop-exclusion) · [Regulamin Galxe](https://docs.galxe.com/about/legal) · [Raport Scam Sniffer 2025](https://drops.scamsniffer.io/scam-sniffer-2025-crypto-phishing-losses-fall-83-to-84-million/) · [Raport Scam Sniffer 2024](https://drops.scamsniffer.io/scam-sniffer-2024-web3-phishing-attacks-wallet-drainers-drain-494-million/)

### Płatne ankiety i mikrozadania (Prolific, MTurk, Swagbucks, polskie panele)

**Co to jest.** Zarabianie kilku dolarów za ankietę lub mikrozadanie na Prolific, Swagbucks, YouGov, Clickworker, Toloka albo w polskich panelach (Ankieter.pl, Opinie.pl, Panel Ariadna). Wersja „agentowa” polegałaby na tym, że agent odpowiada za ciebie.

**Dlaczego odrzucone.** Płatnym produktem jest odpowiedź prawdziwego człowieka, więc odpowiedzi wypełnione przez agenta to oszustwo wobec badacza i naruszenie regulaminu. Umowa uczestnictwa MTurk: „you will not use robots, scripts, or other automated methods as a substitute for your human intelligence or independent judgment to perform Tasks” (ostatnia aktualizacja 25.03.2020). Prolific „reminds participants not to use LLMs unless explicitly permitted” (przewodnik laboratorium WU Vienna). Wykrywanie jest skuteczne: test autentyczności botów Prolific odróżnił 125 ludzi od 5 agentów AI ze 100% trafnością (Prolific, 04.02.2026); badanie z 2026 r. wykazało poniżej 1% odpowiedzi chatbotów u 12 dostawców, ale 16% u trzynastego (relacja z 30.04.2026). Sam MTurk został zamknięty 30.09.2026 (Wikipedia). Wynik 0.

**Legalny mniejszy wariant.** Odpowiadasz na ankiety sam; agent może jedynie czytać listy badań, które i tak widzisz, i układać je według stawki za minutę oraz twojej kwalifikowalności (bez odpowiadania, bez automatycznego akceptowania). Zarobki zostają na poziomie stawek ankietowych (badaczom zaleca się płacić równowartość co najmniej ok. 12 USD/godz.; przewodnik WU), więc nie jest to warte miejsca w kursie.

**Źródła:** [Prolific: authenticity checks test (Feb 2026)](https://www.prolific.com/resources/authenticity-checks-how-we-tested-the-most-accurate-method-for-identifying-agentic-ai) · [MTurk participation agreement](https://www.mturk.com/participation-agreement) · [WU Vienna: Detect and prevent AI in online surveys](https://www.wu.ac.at/fileadmin/wu/d/cc/exp/PDFs/Detect_and_Prevent_AI_in_Online_Surveys_Guide.pdf) · [Let's Data Science: limited AI chatbot presence in surveys (Apr 2026)](https://letsdatascience.com/news/study-finds-limited-ai-chatbot-presence-in-online-surveys-c14178ff) · [Research Live: safeguards against AI in polls (Apr 2026)](https://www.research-live.com/article/opinion/the-right-safeguards-can-protect-public-opinion-polls-from-ai-pollution/id/5148723) · [Wikipedia: Amazon Mechanical Turk](https://en.wikipedia.org/wiki/Amazon_Mechanical_Turk)

### Platformy questów krypto (Galxe, Layer3, Zealy, Intract)

Co to jest: wykonywanie zadań on-chain i społecznościowych („questów”) za punkty, NFT lub nagrody w tokenach.
Dlaczego odrzucone: jedyny sposób, w jaki agent może to skalować, to wiele kont albo skryptowe, fałszywe zaangażowanie, czego platformy zabraniają. Regulamin Galxe zastrzega prawo do „ograniczenia liczby Kont Użytkownika lub Portfeli Cyfrowych”, zakazuje „działań służących oszukaniu Galxe, dowolnego użytkownika Galxe lub dowolnej innej osoby” i pozwala mu „zawiesić lub ograniczyć twoje Konto Użytkownika” z utratą nagród (Galxe Terms of Use, aktualizacja 10.09.2025). Questy są też główną przynętą w phishingu na fałszywe airdropy (drainery zabrały 494 mln USD w 2024 roku, Scam Sniffer). Klauzule Layer3, Zealy i Intract: niezweryfikowane w tym przebiegu.
Legalny mały wariant: rób questy ręcznie na jednym koncie dla protokołów, z których naprawdę korzystasz; agent może jedynie wypisywać kampanie i terminy. Typowa realna wypłata za quest: nie znaleziono; zwykle punkty o niepewnej wartości.

**Źródła:** [Regulamin Galxe](https://docs.galxe.com/about/legal) · [Raport Scam Sniffer 2024](https://drops.scamsniffer.io/scam-sniffer-2024-web3-phishing-attacks-wallet-drainers-drain-494-million/)

### Boty DeFi (likwidacje, arbitraż, MEV)

Co to jest: boty, które likwidują niedozabezpieczone pożyczki, arbitrażują ceny między DEX-ami lub między CEX a DEX albo przechwytują inne MEV.
Dlaczego odrzucone (wykonalność i ryzyko, nie prawo): to przeciwieństwo asymetrii. To już jest w pełni zautomatyzowane i wygrywane przez profesjonalnych searcherów z prywatnym orderflow, kolokowaną infrastrukturą i dużymi zapasami kapitału; agent LLM nic nie wnosi do wyścigu na opóźnienia. Mając 2000 USD, czytelnik nie utrzyma zapasu po obu stronach transakcji CEX-DEX, a nieudane lub przelicytowane transakcje i tak kosztują gas. Konkretne dane z lat 2025-2026 o rentowności samodzielnych searcherów: nie znaleziono w tym przebiegu badania (brak budżetu wyszukiwań na weryfikację), więc nie podaję tu żadnych liczb.
Legalny mały wariant: żaden nie jest polecany. Zbudowanie bota likwidacyjnego na testnecie to dobry projekt do nauki, a nie dochód.
Podatek: zyski z kryptowalut są opodatkowane w Polsce (patrz 03-ZASADY-PODATKI-RYZYKA.md).

**Źródła:** nie znaleziono (w tym przebiegu nie zweryfikowano żadnego datowanego źródła; werdykt opiera się na powyższych ograniczeniach kapitałowych i opóźnieniowych)

### Kopanie w subnetach Bittensor

Co to jest: wykonywanie pracy AI (inferencja, modele, dane) dla subnetu Bittensor i otrzymywanie zapłaty w tokenie alpha tego subnetu, wymienialnym na TAO.
Dlaczego odrzucone (wykonalność i ryzyko, nie prawo): najbardziej znany subnet obliczeniowy, Chutes (SN64), wymaga GPU klasy NVIDIA (przykłady z README: A10, A6000, L40S, H100) na sprzęcie z poufnymi maszynami wirtualnymi Intel TDX, z pamięcią RAM systemu co najmniej równą łącznej VRAM; AMD Radeon/ROCm nie jest wymieniony (README chutes-miner, odczyt 14.10.2026). Wypłaty sieci to głównie inflacja, a nie klienci: 3600 TAO/dzień po halvingu z grudnia 2025, 41% dla minerów, wobec szacowanych 3-15 mln USD/rok zewnętrznych przychodów we wszystkich 128 subnetach; sam Chutes wypłaca około 52 mln USD/rok emisji przy 1,3-2,4 mln USD zewnętrznych przychodów (Pine Analytics, 23.03.2026). Zarobki podążają więc za ceną TAO, a nowy miner płaci opłatę rejestracyjną w TAO oprócz kosztu sprzętu: jeden operator opisał „mniej więcej siedem godzin dziennie przez pierwsze miesiące, płacąc zarówno za GPU, jak i za rejestrację” (edgeX, 24.08.2026; *(relacja zewnętrzna)*). Dokładny obecny koszt rejestracji: nie znaleziono. Przy kapitale 2000 USD i kartach AMD to spekulacyjny zakład na token, a nie dochód.
Legalny mały wariant: żaden nie jest wart profilu; zaciekawiony czytelnik może zestakować niewielkie kwoty zamiast kopać, akceptując ryzyko cenowe.
Podatek: tokeny otrzymane, a później sprzedane, są opodatkowane w Polsce jak kryptowaluty (patrz 03-ZASADY-PODATKI-RYZYKA.md).

**Źródła:** [Pesymistyczny scenariusz dla Bittensor (Pine Analytics)](https://pineanalytics.substack.com/p/the-bear-case-for-bittensor-tao) · [README chutes-miner](https://github.com/chutesai/chutes-miner) · [Subnety Bittensor i dTAO (edgeX)](https://pro.edgex.exchange/en-US/news/article/bittensor-subnets-miners-validators-dtao)

### Zdecentralizowane sieci AI (Gensyn, Psyche, Prime Intellect, Nosana i inne)

**Co to jest.** Sieci, które obiecują płacić ludziom za udostępnianie czasu GPU do rozproszonego treningu lub inferencji: Gensyn RL Swarm, Nous Psyche, Prime Intellect, Nosana, Hyperbolic, Ritual, Akash.

**Dlaczego odrzucone (niewykonalne dla tego czytelnika, nie kwestia regulaminu).** (1) Większość płaci punktami, a nie pieniędzmi: Gensyn RL Swarm działa na „Gensyn Testnet”, a uczestnicy zdobywają punkty aktywności w rankingu, a nie tokeny *(README na GitHubie, 10.2026)*; testnet Delphi od Gensyn używa „valueless tokens” *(dokumentacja, 10.2026)*. (2) Sprzęt: RL Swarm oficjalnie obsługuje tylko NVIDIA RTX 3090/4090/5090, A100 i H100 *(README, 10.2026)*; Nosana obsługuje tylko NVIDIA *(dokumentacja, 10.2026)*. Żadna ze sprawdzonych sieci nie dokumentuje hostowania na AMD Radeon/ROCm. (3) Prime Intellect to obecnie firma finansowana przez fundusze venture (runda Series A 130 mln USD, lipiec 2026, relacja zewnętrzna), sprzedająca moc obliczeniową w chmurze; jej dokumentacja nie pokazuje płatnego publicznego programu dla kontrybutorów (nie znaleziono). (4) Uruchamianie wielu węzłów w celu farmienia punktów pod przyszły airdrop to sybil farming i wykracza poza zakres tego kursu.

**Legalny mały wariant.** Uruchom jeden uczciwy węzeł testnetu na CPU (RL Swarm dopuszcza węzeł CPU z 32 GB RAM) wyłącznie po to, by poznać stos technologiczny; każdy przyszły token traktuj jako niespodziewany wpływ, a nie dochód.

**Źródła:** [Gensyn RL Swarm](https://github.com/gensyn-ai/rl-swarm) · [Dokumentacja Gensyn](https://docs.gensyn.ai/testnet) · [Dokumentacja dla hostów Nosana](https://learn.nosana.com/hosts/grid.html) · [Series A Prime Intellect, KuCoin News](https://www.kucoin.com/news/flash/prime-intellect-completes-130m-a-round-at-1b-valuation-backed-by-nvidia-intel-and-dell) · [Dokumentacja Prime Intellect](https://docs.primeintellect.ai/)

### Odsprzedaż biletów i polowanie na błędy cenowe

**Na czym polega.** Agent obserwuje premiery sprzedaży biletów i sklepy pod kątem błędów cenowych, kupuje bilety lub źle wycenione towary i odsprzedaje je drożej, niż zapłacił.

**Dlaczego odrzucone.** Odsprzedaż biletów z zyskiem jest w Polsce wykroczeniem. Art. 133 § 1 Kodeksu wykroczeń (tekst jednolity Dz.U. 2025 poz. 734, odczyt 14.10.2026): „Kto nabywa w celu odprzedaży z zyskiem bilety wstępu na imprezy artystyczne, rozrywkowe lub sportowe albo kto bilety takie sprzedaje z zyskiem, podlega karze aresztu, ograniczenia wolności albo grzywny.” § 2 dodaje, że karalne są także usiłowanie i pomocnictwo. Wersja zautomatyzowana łamie więc polskie prawo: L=0.

**Błędy cenowe.** Próba zakupu po oczywiście błędnej cenie jest legalna, ale sprzedawca może odmówić lub anulować zamówienie (polskie przepisy prawa cywilnego o błędzie; w tym przebiegu nie zweryfikowano ponownie konkretnego źródła), więc wartość jest niska i nieprzewidywalna. Osobiste alerty o okazjach nie wymagają łamania regulaminu ani prawa, ale nie są źródłem dochodu.

**Legalny mały wariant.** Osobiste alerty o okazjach: agent śledzi ceny rzeczy, które i tak planujesz kupić, i informuje cię, gdy spadną. To oszczędność, nie dochód. Sprzedaż biletu, z którego nie możesz skorzystać, po cenie nominalnej lub niższej przez oficjalną odsprzedaż organizatora jest w porządku.

**Źródła:** [Tekst jednolity Kodeksu wykroczeń (ISAP)](https://isap.sejm.gov.pl/isap.nsf/download.xsp/WDU19710120114/U/D19710114Lj.pdf)
