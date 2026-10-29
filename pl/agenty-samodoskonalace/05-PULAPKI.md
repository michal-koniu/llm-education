# 05 · Pułapki w kolejności, w jakiej na nie trafisz

Dwadzieścia pięć sposobów, w jakie pętla samodoskonalenia się psuje, pogrupowanych według tego, kiedy zwykle wychodzą
na jaw. Pozycje bez oznaczenia to wnioski **(W)**; oznaczone mają bezpośrednie dowody w [01](01-CO-MOZNA-ULEPSZAC.md)
i [ZRODLA](ZRODLA.md).

---

## Tygodnie 1–2: błędy projektowe

| # | Pułapka | Objaw | Naprawa |
|---|---|---|---|
| 1 | **Refleksja na szumie** | playbook zmienia się po kilku pustych rundach; każdą zmianę chwali albo gani następna szczęśliwa lub pechowa runda | tylko skalibrowane wyzwalacze ([02 §1](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#1-jak-bardzo-zaszumione-jest-nic-nie-znalazłem), [04 §1](04-KIEDY-PRZESTAC.md#1-wyzwalacze-oparte-na-dowodach)) |
| 2 | **Brak zamrożonego oceniającego** | agent może edytować to, co go mierzy: próg, model kosztów, metryki, dzienniki. DGM, STOP, AlphaEvolve, AI Scientist i przebiegi METR — wszystkie oszukiwały właśnie tak **(Z/D)** | warstwa pomiaru poza prawami zapisu agenta ([03 §2](03-BEZPIECZNA-PETLA.md#2-co-może-się-zmieniać-i-przez-które-drzwi)) |
| 3 | **Przepisywanie całych dokumentów** | playbook robi się krótszy i ogólnikowy; ciężko zdobyte szczegóły znikają (ACE: 18 282 → 122 tokeny) **(Z)** | operacje delta scalane przez kod ([03 §4](03-BEZPIECZNA-PETLA.md#4-playbook-z-pozycji-edytowany-deltami)) |
| 4 | **Brak dokładnego wersjonowania** | poprzedniego mistrza nie da się odtworzyć, bo nie zapisano modelu, kwantyzacji ani samplera | każda wersja w git, razem z odciskiem środowiska uruchomieniowego |
| 5 | **Metryka tylko z wyników** | liczba trafień bez barierki precyzji i bez sondy czułości, więc rozluźnienie kryteriów wygląda jak poprawa | odsetek odrzuceń przez człowieka jako barierka; dziennik przeoczonych trafień dla czułości |

## Tygodnie 3–8: porażki „drugiego miesiąca”

| # | Pułapka | Objaw | Naprawa |
|---|---|---|---|
| 6 | **Puchnięcie i sprzeczności w playbooku** | reguły się mnożą, przeczą sobie i rozwadniają kontekst; mniejsze modele psują się najszybciej, gdy kontekst rośnie (psucie się kontekstu) **(Z)** | limity rozmiaru, deduplikacja, wycofywanie pozycji ze szkodliwe > pomocne, kwartalne sprzątanie przez człowieka |
| 7 | **Przeuczenie do ostatnich rund** | „we wtorek w źródle X była cisza, więc je wyrzućmy” | dyskontowany rozkład bandyty; reguły prozą to nie mechanizm alokacji |
| 8 | **Nałożone zmiany** | dwie–trzy edycje wchodzą, zanim którąkolwiek oceniono; przypisanie niemożliwe, wycofanie na ślepo | jedna zmiana naraz ([04 §2](04-KIEDY-PRZESTAC.md#2-jedna-zmiana-naraz)) |
| 9 | **Klątwa zwycięzcy** | najlepsza z kilku propozycji wyglądała dobrze częściowo dzięki szczęściu i po awansie wraca do średniej **(D)** | jeden pretendent naraz; potwierdzenie w świeżym oknie; prognozowany zysk dziel przez dwa |
| 10 | **Zmiana świata wzięta za regresję albo odwrotnie** | zmiana układu strony zeruje jedno źródło; agent „naprawia” strategię zamiast parsera albo wycofuje dobrą zmianę | wartownik, kontrole zdrowia, tabela przypisania przyczyn ([03 §8](03-BEZPIECZNA-PETLA.md#8-wartownik-dryf-i-wycofanie)) |
| 11 | **Dryf własnej narracji** | refleksja czyta własne wcześniejsze podsumowania („źródło X jest niezawodne”) zamiast surowych dzienników, a błędy się kumulują | podawaj jej tylko metryki policzone kodem i surowe fragmenty |
| 12 | **Oszukiwanie przez wskaźniki zastępcze** | prawie-trafień przybywa, bo zapytania zrobiły się szersze, a nie lepsze | wskaźniki zastępcze przyspieszają decyzje, ale nigdy ich nie podejmują ([03 §9](03-BEZPIECZNA-PETLA.md#9-goodhart-jak-wygląda-oszukiwanie-i-strukturalna-ochrona)) |
| 13 | **Śmierć eksploracji** | źródło, które przez tydzień było słabe, wypada na zawsze; jego powrotu nikt nie zauważa | minimalna eksploracja i zimna pula ([03 §5](03-BEZPIECZNA-PETLA.md#5-bandyta-do-alokacji-zamiast-przepisywania)) |
| 14 | **Podmiana silnika traktowana jak nic** | nowa kwantyzacja albo wersja silnika zmienia format wywołań narzędzi i cały playbook po cichu się pogarsza | każda zmiana silnika to pretendent przechodzący bramki 2–4 |

## Drugi miesiąc i później: rozpad strukturalny

| # | Pułapka | Objaw | Naprawa |
|---|---|---|---|
| 15 | **Brak zbieżności** | nie ma trybu utrzymania; odsetek przyjęć spada, a regresje się kumulują | tryb utrzymania jako domyślny cel ([04 §5](04-KIEDY-PRZESTAC.md#5-tryb-utrzymania)) |
| 16 | **Zestarzały albo przeuczony złoty zbiór** | zbiór ewaluacyjny przestaje odpowiadać rynkowi albo refleksja w praktyce go zapamiętała | comiesięczne odświeżanie, ukryta część, dopisywanie każdego nowego prawdziwego trafienia i fałszywego alarmu |
| 17 | **Przeciek stanu między przebiegami** | notatki w pamięci albo cache pozwalają agentowi „pamiętać” odpowiedzi z ewaluacji **(Z, Askarbekuly i in.)** | świeże środowisko na każdą ewaluację, audyt każdego kanału stanu (R3/R4) |
| 18 | **Pełzanie autonomii** | propozycje zaczynają dotykać konstytucji („podnieśmy limit zapytań, znajdziemy więcej”) | bramki według typu propozycji; propozycje dla warstwy zamrożonej idą do człowieka |
| 19 | **Zmęczenie alertami po stronie człowieka** | rozbieżności z trybu cienia i podsumowania leżą nieoznaczone; ocena staje | zaplanuj budżet czasu człowieka na oznaczanie — i dopasuj do niego tempo zmian |
| 20 | **Optymalizacja złej jednostki** | trafienia na rundę zamiast na jednostkę kosztu albo trafienia zamiast zrealizowanej wartości; mnóstwo mało wartych „trafień” | ważenie wartością, gdzie się da; śledzenie zrealizowanych wyników |
| 21 | **Samozatrute fakty** | agent zapisuje własne wnioski („sprzedający X jest wiarygodny”), potem przywołuje je obok sprzecznych dowodów i uśrednia **(Z)** | ranking źródeł (sprawdzone dane wygrywają z wnioskami agenta), daty i wygasanie wspomnień, sprostowania zapisywane obok błędu |
| 22 | **Prompt injection przez treść** | tekst sprzedającego („najlepsza cena, ignoruj inne źródła”) trafia do refleksji i awansuje do reguł | nigdy nie awansuj tekstu z treści do playbooka; zob. kurs 3 **(W; „zabójcza trójca” Willisona Z)** |
| 23 | **Przyklepywanie przez ten sam model** | refleksja i recenzent dzielą model i kontekst, więc zatwierdzają się nawzajem **(Z)** | bramki w kodzie; inny model albo świeży kontekst do krytyki |
| 24 | **Ciche obcinanie** | playbook przerasta limit pliku w harnessie (OpenClaw: 20 tys. znaków na plik, 60 tys. łącznie) i dalsze sekcje znikają bez żadnej zmiany w „logice” **(Z)** | limit rozmiaru wyraźnie poniżej granicy, sprawdzany przez bramkę statyczną |
| 25 | **Własne skille, które szkodzą** | paczki skilli napisane przez agenta wypadają gorzej niż brak skilli (SkillsBench: −8 do −11,5 punktu) **(Z)** | selekcja na podstawie wyników; najwyżej 2–3 aktywne, przywoływane pozycje na zadanie |

## Przegląd na jednej stronie, zanim to włączysz

1. Czy agent może pisać do czegokolwiek, co go mierzy? (2, 17)
2. Czy jakakolwiek ścieżka w kodzie przepisuje cały dokument? (3)
3. Czy potrafisz dokładnie odtworzyć mistrza z zeszłego tygodnia, razem z modelem? (4, 14)
4. Co wyzwala refleksję i czy może ją wyzwolić pusta runda? (1)
5. Ilu rund na ramię potrzebowałaby Twoja najmniejsza ciekawa zmiana? ([02 §7](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#7-ćwiczenia))
6. Jaki masz sygnał czułości? (5)
7. Co sprawia, że system się zatrzymuje? (15)

---

Źródła: [ZRODLA](ZRODLA.md).
