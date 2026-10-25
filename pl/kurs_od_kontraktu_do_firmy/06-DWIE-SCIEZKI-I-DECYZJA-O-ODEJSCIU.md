# Część 06 · Dwie ścieżki i decyzja o odejściu

> **Cel tej części.** Rozumiesz dwa sposoby budowania skalowalnej firmy — **finansowanie z własnych środków
> (bootstrapping)**, czyli z kontraktu i od klientów, oraz **finansowanie przez VC** — i wiesz, czego każdy
> z nich wymaga od Ciebie krok po kroku. Dowiadujesz się, jak działa polski rynek pre-seed w latach 2025–2026,
> co sprawdzą inwestorzy i co w praktyce oznacza „robienie startupu", jeśli na to się zdecydujesz. Potem
> spisujesz warunki, na jakich ograniczysz albo zakończysz kontrakt — zanim spiszą je za Ciebie emocje.
>
> **Czas:** ~5 h + trzy rozmowy z inwestorami · **Poziom:** ⭐⭐⭐⭐ · **Wynik:** `founder/06-path.md`,
> `founder/06-quit-triggers.md`

> **To nie jest porada inwestycyjna ani prawna.** Dane rynkowe według stanu na 25 paź 2026. Pozyskiwanie
> finansowania w szczegółach — pitch deck, term sheety, negocjacje — to osobny kurs w tej ścieżce; ta część
> daje Ci mapę i decyzję.

---

## 0. Problem

Powiedziałeś, że chcesz firmy, która skaluje się przez dodawanie agentów eksperckich, i że możesz zacząć
z finansowaniem VC albo bez niego — ale jeśli wybierzesz VC, chcesz wiedzieć, jak to zrobić. Te dwie ścieżki
to nie dwa sposoby robienia tego samego. Prowadzą do różnych firm, z różnymi zobowiązaniami, a wybór wpływa
na kontrakt, który teraz chronisz. Podjęcie tej decyzji domyślnie („wszyscy zbierają pre-seed") albo pod
wpływem nastroju („mam dość banku") to błąd, przed którym chroni ta część.

---

## 1. Czy AI box ma skalę venture?

Fundusze VC potrzebują w każdym funduszu kilku spółek, które zwrócą cały fundusz. Dlatego pierwsze pytanie
inwestora nie brzmi „czy to dobry biznes?", tylko „**czy to może stać się bardzo duże?**". Zrób tę arytmetykę,
zanim zrobi ją on.

Liczebności z kursu wyceny (część 03), wszystkie dane z 2025 r., z zastrzeżeniami opisanymi tam:

| Nabywcy w Polsce | Liczba |
| :-- | --: |
| Adwokaci wykonujący zawód | ~23 600 |
| Radcowie prawni (wpisani na listy) | 56 415 |
| Doradcy podatkowi | 9 220 |
| Notariusze (kancelarie) | 3 507 |
| Biura rachunkowe (szacunek) | ~70 000 |

To ludzie i biura, a nie nabywcy boxa: wielu prawników dzieli jedną kancelarię, wiele biur nigdy nic nie kupi.
Przyjmij mniej więcej **100 000 biur** jako górną granicę polskiego rynku kancelarii i biur profesjonalnych
i przetestuj jego udziały przy poglądowej cenie pakietu *Office* 1 790 zł miesięcznie (kurs wyceny, część 07):

| Płacące biura | Udział w ~100 tys. | ARR (PLN) | ARR (≈ EUR, kurs 4,25) |
| --: | --: | --: | --: |
| 100 | 0,1% | 2,1 mln | 0,5 mln |
| 1 000 | 1% | 21,5 mln | 5,1 mln |
| 5 000 | 5% | 107 mln | 25 mln |

**Uczciwa interpretacja:**

- **100–1 000 biur** to bardzo dobra firma finansowana z własnych środków — od kilku do kilkudziesięciu milionów
  złotych rocznego przychodu powtarzalnego (ARR), i należy do Ciebie.
- **Skala venture wymaga więcej niż Polski**: tego samego boxa dla kancelarii i biur w innych krajach UE (własny
  profil repozytorium mówi *„PL, potem UE"*), większej liczby zawodów albo platformy, na której inni budują
  agentów. Inwestor zapyta o tę historię pierwszego dnia. Jeśli w nią nie wierzysz, nie zbieraj pieniędzy od VC.
- **Katalog agentów** pomaga na obu ścieżkach (kurs wyceny, część 08): przychód na biuro rośnie bez nowej
  sprzedaży.

---

## 2. Ścieżka A: finansowanie z własnych środków (bootstrapping)

| | |
| :-- | :-- |
| **Pieniądze z** | nadwyżki z kontraktu (część 04), potem od klientów: opłaty wdrożeniowe, przedpłaty roczne, abonamenty |
| **Zatrzymujesz** | 100% firmy i swobodę rośnięcia we własnym tempie |
| **Rezygnujesz z** | tempa; możliwości finansowania sprzętu w modelu wynajmu na dużą skalę (kurs wyceny, część 05); wczesnego zespołu |
| **Kontrakt** | zostaje, dopóki jest użyteczny — to Twój inwestor |
| **Pasuje, gdy** | rynek to najpierw Polska, cenisz kontrolę, liczby działają przy 100–1 000 biurach |

Bootstrapping nie zamyka drzwi przed inwestorami. Firma z płacącymi klientami, zmierzonym odpływem klientów
(churn) i rosnącym katalogiem pozyska pieniądze później na lepszych warunkach, jeśli zechce — albo nigdy nie
będzie musiała. Prywatne firmy SaaS wyceniane przez SaaS Capital: 4,8× ARR przy bootstrappingu vs 5,3× przy
finansowaniu kapitałowym (sty 2025, *dane własne firmy*). Różnica w wartości jest mniejsza niż różnica we
własności.

---

## 3. Ścieżka B: finansowanie przez VC — jak to naprawdę działa

Prosiłeś, żeby nauczyć Cię, jak to zrobić. Oto kolejność, wraz z tym, co research wykazał o Polsce. Kroki bez
źródła traktuj jako ogólną praktykę.

### 3.1 Polski rynek pre-seed w liczbach

| Fakt | Wartość | Źródło |
| :-- | :-- | :-- |
| Transakcje seed w Polsce w 2025 r. (seed obejmuje pre-seed) | **134**, wzrost ze 113 w 2024 r.; średni ticket seed ~**1,5 mln EUR** | PFR Ventures × Inovo, *Polish VC Market Outlook 2025* *(fragment z wyszukiwarki)* |
| Rundy z udziałem funduszy wspieranych przez PFR | prawie **trzy czwarte** rund seed; PFR dostarczył **47%** całego kapitału dla startupów w 2025 r. | xyz.pl, 1 lut 2026 |
| II kw. 2026 | seed + pre-seed = **33 transakcje, 77%** wszystkich rund | PFR Ventures, II kw. 2026 *(fragment z wyszukiwarki)* |
| PFR Starter (FENG) | tickety **do 5 mln PLN** na spółkę; budżet 807 mln PLN; co najmniej 20% kapitału prywatnego; cel: **70% pierwszych inwestycji w spółki przed przychodami** | PFR Ventures *(fragment z wyszukiwarki)* |
| Nowe fundusze Starter / FENG, gru 2025 – mar 2026 | betacluster, Cofounder VC, Stelo, VO2, Epic, Invento II, YouNick Mint, Pomerangels | PFR Ventures *(fragment z wyszukiwarki)* |
| Typowe wyceny pre-seed w Polsce | **nie znaleziono** | — |

Uderzający jest cel PFR Starter: **większość pierwszych inwestycji trafia do spółek przed ich pierwszą
sprzedażą.** Polski rynek, nietypowo, ma pieniądze publiczne przeznaczone na finansowanie dokładnie Twojego
etapu.

### 3.2 Fundusze inwestujące na Twoim etapie (aktywność zweryfikowana 25 paź 2026)

| Fundusz | Etap i ticket (według znalezionych danych) |
| :-- | :-- |
| **SMOK Ventures** | pre-seed, 100–500 tys. EUR na start (łącznie do 1 mln EUR) |
| **AIP Seed** | pre-seed, ~200 tys. EUR; ponad 120 inwestycji (*według własnego opisu* największy fundusz pre-seed w CEE) |
| **Tar Heel Capital Pathfinder** | Pathfinder VC II (pieniądze z PFR Starter), do 1 mln EUR, inwestuje przed przychodami |
| **Movens Capital** | Fund II 60 mln EUR (cze 2025), od pre-seed do Series A, 250 tys.–3 mln EUR |
| **Inovo** | głównie seed, 0,5–4 mln EUR |
| **Simpact Ventures** | nacisk na impact, 0,5–2 mln EUR |
| *Nie pasują* | bValue (teraz etap growth, 5–15 mln EUR); Market One (nie potwierdzono aktywności w 2025 r.) |

Istnieją też pieniądze nierozwadniające (bez oddawania udziałów): rodzina programów PARP *Startup Booster
Poland* (Smart UP do 400 tys. zł trwał do 10 mar 2026; nabór do 100 tys. zł planowano na II połowę 2026 r.).
Poland Prize jest skierowany do założycieli **z zagranicy**.

### 3.3 Czego inwestorzy będą wymagać, zanim zainwestują

| Wymóg | Szczegóły | Gdzie w tej ścieżce |
| :-- | :-- | :-- |
| **Spółka** | zwykle **sp. z o.o.**; możliwa jest **PSA** (prosta spółka akcyjna): 1 zł kapitału, akcje można wydawać **za pracę lub usługi** — ale akcji PSA nie można notować na GPW ani na NewConnect | planowany kurs o formie prawnej |
| **IP należące do spółki** | pisemne przeniesienie wszystkiego, co zbudowałeś (część 03) — ciągłość praw (*chain of title*) | część 03 |
| **Założyciele na pełen etat** | YC: założyciele *"commit to working full-time"* (zobowiązują się do pracy na pełen etat); Antler: *"a full-time commitment"* (zobowiązanie na pełen etat); inwestorzy cytowani przez LaunchVic nazywają pracę na część etatu *"red flag"* (czerwoną flagą). **Nie znaleziono wyraźnej polskiej deklaracji** — pyta o to eksperyment terenowy 06 | §5 poniżej |
| **Vesting założycieli** | europejska norma: **4 lata z rocznym okresem cliff**, jako vesting *odwrócony* (reverse vesting) z warunkami good/bad leaver; nie znaleziono źródła specyficznego dla prawa polskiego (w praktyce często opcje call w umowie wspólników — *wiedza ogólna, niezweryfikowana*) | planowany kurs o pozyskiwaniu finansowania |
| **Zespół** | YC przyjmuje samodzielnych założycieli, ale mówi *"one-person startups are tough"* (startupy jednoosobowe mają trudno). U Ciebie lukę stanowi **wspólnik dziedzinowy** (prawnik albo doradca podatkowy), jak repozytorium już ustaliło | planowany kurs o zespole |

### 3.4 Instrument i cena

W USA **93% rund pre-seed w II kw. 2026 stanowiły SAFE-y** (Simple Agreements for Future Equity), z czego 91%
w wariancie post-money; mediana limitów wyceny (cap) post-money w 2025 r. wynosiła około **10 mln USD** dla
rund 250 tys.–1 mln USD (Carta, dane z USA). Standardowa oferta YC: 125 tys. USD za 7% na SAFE post-money plus
375 tys. USD na SAFE bez limitu wyceny (uncapped).

SAFE to instrument prawa amerykańskiego. Polskie transakcje używają odpowiedników na gruncie prawa polskiego
(pożyczki zamienne i podobne umowy) — **research do tego kursu ich nie obejmował**; zajmie się nimi kurs
o pozyskiwaniu finansowania.

Arytmetyka, której potrzebujesz już teraz, to rozwodnienie (dilution):

```
 wycena post-money  = wycena pre-money + inwestycja
 udział inwestora   = inwestycja / wycena post-money

 przykład: 2 mln PLN zainwestowane przy wycenie pre-money 8 mln PLN → post-money 10 mln PLN → inwestor ma 20%, Ty zachowujesz 80%
           dwie kolejne rundy po 20% każda → zachowujesz 80% × 80% × 80% ≈ 51%
```

Liczby w przykładzie są ilustracją, a nie danymi z polskiego rynku.

### 3.5 Proces (ogólna praktyka)

```
 1. dowody          płatne pilotaże, zmierzone godziny, pierwsza kohorta     (kurs wyceny, części 06–08)
 2. spółka          sp. z o.o. / PSA, przeniesione IP, umowa wspólników
 3. lista           20–40 funduszy inwestujących na Twoim etapie i w Twoim sektorze (§3.2 to początek)
 4. intro           ciepłe rekomendacje wygrywają z zimnymi e-mailami — założyciele, których finansowali, anioły biznesu, akceleratory
 5. deck + model    problem, box, zmierzone liczby, historia UE, zespół, kwota, o którą prosisz
 6. spotkania       spotkanie z partnerem → drugie spotkanie → komitet inwestycyjny
 7. term sheet      wycena, kwota, instrument, rada nadzorcza (board), vesting, prawa inwestora
 8. due diligence   ciągłość praw do IP, umowy, podatki, inne zobowiązania założycieli (Twój kontrakt z bankiem!)
 9. zamknięcie      podpisanie, notariusz (dla sp. z o.o.), rejestracja, pieniądze
```

W kroku 8 procentują części 02–04 tego kursu: prawnik inwestora przeczyta Twój kontrakt z bankiem, Twój rejestr
IP i Twoją dokumentację podatkową. **Samo pozyskiwanie finansowania to przez 3–6 miesięcy niemal praca na pełen
etat** — kolejny powód, dla którego nie da się go pogodzić z kontraktem.

---

## 4. Która ścieżka i kiedy zdecydować

Nie musisz decydować teraz i nie powinieneś. Zdecyduj przy **bramce 2** z części 04 (≥ 10 płacących biur,
zmierzony churn), gdy będziesz mieć liczby, o które inwestor i tak by zapytał. Do tego czasu trzymaj obie
ścieżki otwarte, robiąc to, czego wymagają obie: czyste IP (część 03), płatny pilotaż, zmierzona wartość.

| Jeśli przy bramce 2… | To skłaniaj się ku |
| :-- | :-- |
| popyt przekracza to, co możesz obsłużyć; historia UE jest wiarygodna; wspólnik dziedzinowy jest gotów dołączyć na pełen etat | **VC** |
| wzrost jest stabilny, marże dobre, możesz obsłużyć popyt z jednym albo dwoma pomocnikami | **bootstrapping** |
| wzrost jest powolny, churn wysoki | żadnej — produkt musi się zmienić albo zastosowanie ma warunek stopu z części 04 |

---

## 5. Decyzja o odejściu

### 5.1 Wyzwalacze

Spisz je teraz. **Każdy z nich z osobna** jest wyzwalaczem do ograniczenia albo zakończenia kontraktu:

| Wyzwalacz | Jak go mierzyć |
| :-- | :-- |
| **T1 · Finansowanie, które tego wymaga** | podpisany term sheet z warunkiem pracy na pełen etat |
| **T2 · Startup utrzymuje Twoje życie** | miesięczny zysk brutto startupu ≥ Twoje koszty życia (część 01). Przykład: życie 12 000 PLN miesięcznie; przy marży brutto 60% potrzebujesz 20 000 PLN miesięcznego przychodu z abonamentów — około 11 biur na pakiecie *Office* po 1 790 PLN |
| **T3 · Czas jest wąskim gardłem** | przez dwa kolejne miesiące transakcje przepadały albo się opóźniały, bo nie miałeś godzin w ciągu dnia (przeglądy tygodnia z części 05) |
| **T4 · Kontrakt i tak się kończy** | wypowiedzenie od banku albo zmiana, której nie akceptujesz |

Oraz **warunki**, które muszą być też spełnione, zanim zadziałasz na podstawie T2 lub T3 (nie T1 ani T4 —
te wymuszają decyzję):

- bufor bezpieczeństwa z części 04 jest pełny;
- co najmniej jeden płacący klient odnowił umowę (szczyt drabiny dowodów z kursu wyceny);
- Twoi bliscy się zgadzają.

### 5.2 Nie wszystko albo nic

Kontrakt B2B często można ograniczyć, zanim się go zakończy. Opcje do negocjacji, w tej kolejności:

1. **Mniej dni w tygodniu** — np. trzy dni dla banku, dwa dla startupu.
2. **Stały projekt zamiast stawki dziennej** — rezultaty i terminy, bez okna dostępności; to także oddala
   kontrakt od przesłanek stosunku pracy (część 02, §6.3).
3. **Zakończenie z zachowaniem pełnego okresu wypowiedzenia**, z propozycją przekazania obowiązków. Banki
   pamiętają profesjonalne odejścia; Twoja reputacja w IT jest częścią Twojej przyszłej sieci rekrutacyjnej
   i partnerskiej.

### 5.3 Notatka decyzyjna

Gdy wyzwalacz zadziała, zanim cokolwiek zrobisz, napisz jedną stronę: wyzwalacz, dowody, warunki, opcję wybraną
z §5.2 i to, co skłoniłoby Cię do jej odwrócenia. Ta sama dyscyplina co ADR z warunkiem falsyfikacji w kursach
technicznych.

---

## 6. ĆWICZENIE 06 — ścieżka i wyzwalacze

1. `founder/06-path.md`: Twoja obecna skłonność (bootstrapping / VC / niezdecydowany) z trzema powodami,
   arytmetyka rynku z §1 dla wybranego zawodu i bramka, przy której podejmiesz decyzję.
2. `founder/06-quit-triggers.md`: T1–T4 z Twoimi liczbami (koszty życia, marża, liczba biur dla T2), warunki
   i opcja z §5.2, którą wypróbowałbyś jako pierwszą.
3. Lista 10 funduszy lub aniołów biznesu z §3.2 i z Twojej sieci kontaktów, z opisem, jak mógłbyś zdobyć ciepłe
   intro do każdego z nich.

---

## 7. ⭐ EKSPERYMENT TERENOWY 06 — zapytaj inwestorów

**Hipoteza.** Polscy inwestorzy pre-seed zainwestują w założyciela, który wciąż ma kontrakt **przed** rundą, ale
od rundy będą wymagać pracy na pełen etat, a samodzielnego technicznego założyciela bez wspólnika dziedzinowego
uznają za główną słabość AI boxa.

**Procedura.** Poproś o 20-minutowe rozmowy trzech inwestorów działających na Twoim etapie (§3.2 — co najmniej
jeden fundusz wspierany przez PFR Starter). Powiedz otwarcie, że **teraz nie zbierasz pieniędzy** i prosisz
o radę. Zapytaj:

1. *„Czy zainwestowalibyście w założyciela, który utrzymuje kontrakt B2B aż do rundy? A po niej?"*
2. *„Co musielibyście zobaczyć w przypadku AI boxa on-premise dla kancelarii i biur, zanim zainwestujecie
   w pre-seed?"*
3. *„Jak patrzycie na sprzęt w biznesie abonamentowym?"*
4. *„Jaka jest największa słabość tego pomysłu w takiej formie, w jakiej go opisałem?"*

**Predykcja (moja).** Wszyscy trzej: kontrakt przed rundą w porządku, po rundzie wymagany pełen etat. Dwóch z
trzech wskaże brak wspólnika dziedzinowego; co najmniej jeden poprosi o historię ekspansji w UE; co najmniej
jeden będzie sceptyczny wobec sprzętu i zapyta o leasing.

| Inwestor (kod) | P1: kontrakt przed / po | P2: potrzebne dowody | P3: zdanie o sprzęcie | P4: największa słabość |
| :-- | :-- | :-- | :-- | :-- |
| | | | | |
| | | | | |
| | | | | |

Te trzy rozmowy zaczynają też relacje, których będziesz potrzebować przy bramce 2 — inwestorzy wolą założycieli,
których rozwój obserwowali przez dłuższy czas.

---

## 8. Pułapki

**B26 · Zbieranie pieniędzy przed dowodami.**
*Objaw:* pitch deck przed pierwszym płatnym pilotażem. *Dlaczego boli:* niska wycena albo „nie", które trudno
odwrócić. *Lekarstwo:* najpierw dowody (kurs wyceny, części 06–08); rozmowy bez prośby o pieniądze (eksperyment
terenowy 06).

**B27 · Odejście po dobrym tygodniu.**
*Objaw:* dwa świetne spotkania i składasz wypowiedzenie. *Lekarstwo:* wyzwalacze i warunki z §5, mierzone
miesiącami.

**B28 · Pieniądze VC bez historii na skalę VC.**
*Objaw:* zbieranie pieniędzy na biznes tylko na Polskę, którego sufit to kilkaset biur. *Lekarstwo:* arytmetyka
z §1; bootstrapping, jeśli nie wierzysz w większą historię.

**B29 · Samodzielny techniczny założyciel.**
*Objaw:* żaden prawnik ani doradca podatkowy nie jest głęboko zaangażowany w produkt. *Lekarstwo:* szukaj
partnera dziedzinowego już teraz, zaczynając od ludzi z Twoich wywiadów cenowych.

**B30 · Zapominanie, że due diligence czyta Twoją przeszłość.**
*Objaw:* jest term sheet, a potem prawnik inwestora znajduje szeroką klauzulę IP w kontrakcie z bankiem.
*Lekarstwo:* części 02–03 zrobione na długo przed pozyskiwaniem finansowania.

---

## 9. Checkpoint — i koniec kursu

- [ ] `founder/06-path.md` z Twoją skłonnością, arytmetyką rynku i bramką decyzyjną.
- [ ] `founder/06-quit-triggers.md` z liczbami.
- [ ] Lista 10 inwestorów ze ścieżkami dotarcia do nich.
- [ ] Eksperyment terenowy 06: odbyła się co najmniej jedna rozmowa z inwestorem.
- [ ] **Przeczytaj ponownie `founder/01-position.md`.** Napisz jeden akapit: co wiesz teraz o swojej pozycji,
      czego nie wiedziałeś, kiedy go pisałeś.

Ten akapit jest oceną za ten kurs. Kolejne kursy w tej ścieżce — odkrywanie klientów (customer discovery),
finanse, forma prawna, umowy, sprzedaż — zaczynają się od plików, które tu utworzyłeś.

Źródła do tej części: [ZRODLA.md](ZRODLA.md), sekcja „Część 06".
