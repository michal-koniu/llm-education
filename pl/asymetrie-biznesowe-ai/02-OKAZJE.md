# 15 najlepszych okazji, profil po profilu

Każdy profil ma ten sam układ: asymetria, kto płaci i ile, aplikacja agentowa, podział pracy między lokalne modele otwarte
a płatne API, tabela konkurencji, kontra z pięciu stron (klient, obecny gracz, czołowe laboratoria i big tech, regulator,
ekonomia jednostkowa), liczby, jak zacząć, ryzyka i kryteria przerwania. Fakty według stanu na 14.10.2026. Punktacja
(M rynek 20, G luka adopcji 20, C miejsce na konkurencję 15, L dopasowanie modeli lokalnych 15, F wykonalność 15, R
trwałość i ryzyko 15) jest opisana w [README](README.md#jak-punktowałem). Pomysły, które nie przetrwały kontry, są na
końcu.

**Przeczytaj kontrę przed pitchem.** Każdy pomysł tutaj wygląda dobrze w pierwszym akapicie. Wynik jest ustalany po
kontrze, nie przed nią.

---

## 1. Prywatne pudełko AI dla polskich biur profesjonalnych

**Region:** PL, potem UE · **Kupujący:** kancelarie prawne, notarialne, biura doradztwa podatkowego, biura rachunkowe i gabinety medyczne zatrudniające 5-50 osób · **Model przychodu:** wdrożenie + marża na sprzęcie + miesięczna licencja serwisowa · **Konkurencja:** średnia · **Dopasowanie modeli lokalnych:** wysokie · **Wynik: 72** (M14 G16 C9 L14 F11 R8)

> Najmocniejszy pomysł typu local-first w tym zestawie: sprzedawać skonfigurowane pudełko plus 2-3 wąskie przepływy agentowe, a nie „serwer z chatbotem".

**Asymetria.** Polska jest blisko dołu UE pod względem wykorzystania AI w biznesie: w 2025 roku AI stosowało 8,36% przedsiębiorstw wobec średniej unijnej 19,95%; niżej była tylko Rumunia (Eurostat, dane za 2025). Małe firmy odstają wszędzie (17% małych wobec 55,03% dużych przedsiębiorstw w UE, 2025). Bariery wskazywane przez firmy, które AI nie stosują, idealnie pasują do oferty na miejscu: brak wiedzy 70,89%, niepewność prawna 52,52%, prywatność i ochrona danych 48,83% (Eurostat, 2025). Biura profesjonalne związane tajemnicą (adwokacką, notarialną, doradcy podatkowego, lekarską) nie mogą po prostu wklejać akt klientów do amerykańskiego czatu w chmurze, więc ich praca na dokumentach (streszczenia, pisma, porównania, rejestry) pozostaje ręczna. Luka pozostaje otwarta, dopóki dostawcy chmury nie potrafią zaoferować „dane nigdy nie opuszczają pomieszczenia", a lokalny sprzęt wciąż tanieje.

**Kto płaci i ile.** Liczba polskich biur profesjonalnych: nie znaleziono w tym przebiegu badania (do sprawdzenia rejestry GUS i izb). Dziś płacą za godziny pracy pracowników przy redagowaniu i weryfikacji; dokładne wydatki: nie znaleziono. Ceny do przetestowania: 25 000-60 000 PLN wdrożenia wraz ze sprzętem, 800-2500 PLN miesięcznie za aktualizacje, monitoring i nowe przepływy (moje założenie do sprawdzenia, nie dane rynkowe). Kanał: izby adwokackie i doradców podatkowych, stowarzyszenia biur rachunkowych, lokalne firmy IT, które już obsługują te biura.

**Aplikacja agentowa.**
1. Wczytanie: obserwowanie wspólnego folderu lub systemu dokumentów; lokalne OCR skanów.
2. Ekstrakcja: strony, daty, kwoty, sygnatury spraw do lokalnego indeksu (RAG po własnych plikach biura).
3. Rozumowanie: agent dla konkretnego przepływu (na przykład „streść nowe pismo sądowe i zaproponuj termin", „porównaj projekt umowy ze wzorem").
4. Redakcja: pismo, streszczenie lub lista kontrolna po polsku.
5. Weryfikacja: drugi przebieg sprawdza odwołania do stron źródłowych; oznacza niską pewność.
6. Działanie: **bramka zatwierdzenia przez człowieka** zanim cokolwiek opuści biuro lub trafi do kalendarza; pełny lokalny dziennik audytu.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| OCR i ekstrakcja | Tak (klasa Qwen-VL lub Bielik 11B v3) | Nie | Dane klientów objęte tajemnicą zawodową |
| Redagowanie po polsku | Tak (Bielik-11B-v3.0-Instruct, Apache 2.0) | Nie | Jakość polszczyzny, brak transferu danych |
| Trudne rozumowanie na zanonimizowanym tekście | Opcjonalnie | Tak, tylko za zgodą | Lepsza jakość w rzadkich, złożonych przypadkach |
| Budowa przepływów przez integratora | Nie | Tak | Produktywność programisty, brak danych klientów |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
|---|---|---|---|---|---|
| NVIDIA DGX Spark i pudełka OEM GB10 (Dell, HP, Lenovo, ASUS) | platforma globalna | globalnie | Biurkowe pudełko AI 128 GB, „do 200 mld parametrów" *(deklaracja dostawcy)* | Tylko sprzęt | nie znaleziono na stronie dostawcy (10.2026) |
| Microsoft 365 Copilot | platforma globalna | globalnie | Asystent w chmurze w pakiecie Office | Wysoka, tylko chmura | nie sprawdzono |
| Polskie firmy usługowe IT i integratorzy | firma doradcza | PL | Serwery, sieci, niektóre projekty „prywatnego AI" | Niska do średniej | nie znaleziono |
| Asseco i inni więksi polscy integratorzy | obecny gracz | PL | Projekty AI i voicebotów dla przedsiębiorstw | Średnia | nie znaleziono |
| Legal-tech SaaS (chmura) | startup | PL/UE | Asystenci prawni w chmurze | Średnia | nie znaleziono |

Luka: dostawcy sprzętu sprzedają pudełka bez polskich przepływów pracy; narzędzia w chmurze nie przechodzą testu tajemnicy; więksi integratorzy nie sprzedają projektów za 30 tys. PLN. Wygrywa się hasłem „zainstalowane, po polsku, audytowane, utrzymywane", najpierw dla jednego zawodu.

**Kontra z pięciu stron.**
- **Klient:** małe biura boją się projektów IT i mogą powiedzieć „mamy już Copilota". Odpowiedź: zacząć od jednego płatnego przepływu i dema na ich własnych zanonimizowanych plikach.
- **Obecny gracz:** lokalne firmy usługowe IT mają relację z klientem i mogą odsprzedawać DGX Spark. Odpowiedź: współpracować z nimi jako warstwa AI, z podziałem przychodu.
- **Czołowe laboratoria i big tech:** chmury z granicą danych w UE i oferty chmur suwerennych osłabiają argument „dane nigdy nie wychodzą" w perspektywie 2-3 lat.
- **Regulator:** RODO i przepisy o tajemnicy pomagają; odpowiedzialność za błędne pisma pozostaje przy profesjonaliście, dlatego trzeba zachować bramkę człowieka i logi.
- **Ekonomia jednostkowa:** marża na sprzęcie jest cienka, a wsparcie pracochłonne; zysk musi pochodzić z miesięcznej licencji i powtarzalnych przepływów.

**Po kontrze.** Przetrwa jako wertykał (jeden zawód, 2-3 przepływy) z dystrybucją przez partnerów IT. Ogólne „pudełko AI dla każdego" nie przetrwa. Wynik pozostaje blisko 70.

**Liczby.**
- 8,36% polskich przedsiębiorstw używało AI w 2025 roku wobec 19,95% w UE (Eurostat, dane za 2025, *statystyki oficjalne*).
- Małe przedsiębiorstwa w UE 17% wobec dużych 55,03% w użyciu AI (Eurostat, 2025).
- Bariery: wiedza 70,89%, prawo 52,52%, prywatność 48,83% (Eurostat, 2025).
- Bielik-11B-v3.0-Instruct na licencji Apache 2.0, model bazowy z 30.07.2025 (karta modelu w Hugging Face, odczytano 14.10.2026).
- Rodzina PLLuM 2512 (4B, 8B, 12B, 70B) w Hugging Face, aktualizacja w połowie 2026; licencji nie potwierdzono w tym przebiegu.
- DGX Spark 128 GB, „do 200 mld parametrów", 4 sztuki „do 700 mld" (*deklaracja dostawcy*, odczytano 14.10.2026).

**Jak zacząć.**
1. Tygodnie 1-4: jeden przepływ (segregowanie przychodzących pism dla kancelarii lub biur podatkowych) na sprzęcie czytelnika, Bielik + Qwen, lokalne OCR.
2. Tygodnie 5-8: spakować na jednym małym pudełku; napisać notatkę o ochronie danych i dziennik audytu.
3. Pierwszych 10 klientów: dwa piloty przez osobiste kontakty, potem wydarzenia izb i dwóch partnerów usługowych IT.
4. Test ceny: płatny pilot 3000-5000 PLN, potem wdrożenie + miesięczna opłata; zrezygnować z marży na sprzęcie, jeśli blokuje sprzedaż.

**Ryzyka i ograniczenia.**
- Obciążenie wsparciem na miejscu rośnie z każdym pudełkiem.
- Jakość modeli otwartych na długich polskich tekstach prawniczych trzeba zmierzyć, a nie zakładać.
- Ceny i dostępność sprzętu szybko się zmieniają.
- Odpowiedzialność zawodowa, jeśli pracownicy pominą bramkę zatwierdzenia.

**Kiedy przerwać.** Przerwać, jeśli po 4 miesiącach aktywnej sprzedaży będzie mniej niż 3 płatne piloty lub jeśli miesięczne wsparcie przekroczy 30% przychodu.

**Źródła:** [Eurostat: wykorzystanie AI w przedsiębiorstwach](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Bielik-11B-v3.0-Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [SpeakLeash w Hugging Face](https://huggingface.co/speakleash) · [PLLuM (CYFRAGOVPL)](https://huggingface.co/CYFRAGOVPL) · [NVIDIA DGX Spark](https://www.nvidia.com/en-us/products/workstations/dgx-spark/)

---

## 2. Lokalny agent dokumentowy dla polskich urzędów gmin

**Region:** PL · **Kupujący:** gminy, powiaty i ich integratorzy IT · **Model przychodu:** wdrożenie + roczna licencja na urząd (urządzenie u klienta), sprzedaż przez zamówienie publiczne lub integratora · **Konkurencja:** niska · **Dopasowanie modeli lokalnych:** wysokie · **Wynik: 71** (M13 G16 C11 L15 F7 R9)

> Najmocniejszy przypadek modeli lokalnych na tej liście: dane osobowe i akta administracyjne muszą zostać w urzędzie, rząd sam udostępnia polski model na licencji Apache, a dostawcy systemów obiegu dokumentów nie pokazują żadnej AI, ale publiczny cykl sprzedaży jest powolny.

**Asymetria.** W Polsce jest 2477 gmin (liczba GUS TERYT, nie zweryfikowana ponownie w tej sesji) oraz powiaty i inne urzędy, a każdy z nich obsługuje ręcznie wnioski o informację publiczną, pisma obywateli, decyzje administracyjne i rejestrację dokumentów. Wykorzystanie AI w polskich przedsiębiorstwach wyniosło w 2025 roku 8,4% (Eurostat, 11.12.2025); wskaźnika dla sektora publicznego nie znaleziono. Dwóch sprawdzonych przez nas dostawców systemów obiegu dokumentów nie pokazuje AI: darmowa strona EZD RP (NASK) wymienia cyfrową kancelarię, e-podpisy i wyszukiwanie bez żadnej AI (gov.pl, 10.2026), a Madkom (SIDAS EZD, BIP) deklaruje 1200 wdrożeń i 120000 użytkowników, bez AI na stronie głównej *(deklaracja dostawcy, 10.2026)*. Luka pozostaje otwarta, bo urzędy nie mogą wysyłać akt obywateli do chmury w USA bez analizy RODO i lokalizacji danych, a EZD stanie się obowiązkowe najwcześniej od 1.01.2029 (Ministerstwo Cyfryzacji, według wyników wyszukiwania, 10.2026), więc modernizacja obiegu dokumentów dopiero przed nami.

**Kto płaci i ile.** Około 2500 urzędów gmin plus około 380 powiatów (liczba nie zweryfikowana ponownie). Dziś koszt to czas urzędników; danych o wynagrodzeniach urzędników gminnych nie znaleziono w tej sesji. Ceny do przetestowania: 15000-30000 PLN za wdrożenie (urządzenie z GPU + instalacja) plus 6000-12000 PLN rocznie. Poniżej progu 130000 PLN z Pzp urząd może kupować bez pełnego przetargu, co utrzymuje sprzedaż małą i szybką. Kanał: istniejący lokalni integratorzy IT i dostawcy oprogramowania dla gmin jako resellerzy, wojewódzkie spotkania sekretarzy gmin.

**Aplikacja agentowa.**
1. Pobranie: przychodzące e-maile, pisma z ePUAP/e-Doręczeń i skany papierowej korespondencji z kancelarii.
2. Ekstrakcja: nadawca, rodzaj sprawy, termin (14 dni dla wniosków o informację publiczną), obecność danych osobowych.
3. Wnioskowanie: klasyfikacja do wykazu akt JRWA, przekazanie do wydziału, wyszukanie podobnych dawnych spraw i decyzji.
4. Szkic: odpowiedź na wniosek o informację publiczną, wzór decyzji, zanonimizowana wersja do publikacji w BIP.
5. Weryfikacja: podstawy prawne sprawdzone względem lokalnego korpusu aktów prawnych; kontrola zanonimizowania danych osobowych.
6. Działanie: **bramka akceptacji przez człowieka**: urzędnik podpisuje każde wychodzące pismo i decyzję; agent tylko rejestruje i przygotowuje szkice.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| OCR i ekstrakcja | lokalnie | nie | Dane osobowe obywateli, muszą zostać w urzędzie |
| Klasyfikacja i kierowanie | PLLuM 12B lub Bielik 11B | nie | Polski język administracyjny, rządowy model jest argumentem sprzedażowym |
| Szkice odpowiedzi i decyzji | PLLuM lub większy model lokalny | nie | Skutek prawny i dane osobowe |
| Anonimizacja do BIP | lokalnie | nie | RODO, dane nie mogą opuścić budynku |
| Aktualizacje korpusu prawnego | lokalnie | płatne API tylko dla tekstów prawa publicznego | Teksty publiczne może przetwarzać płatny model, offline od danych obywateli |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Poziom AI | Cena |
|---|---|---|---|---|---|
| EZD RP (NASK) | obecny gracz | PL | Darmowy rządowy system zarządzania dokumentami | brak na stronie produktu | za darmo |
| Madkom SIDAS | obecny gracz | PL | EZD, BIP, oprogramowanie dla gmin, 1200 wdrożeń | brak na stronie głównej | niepublicznie |
| PLLuM (Ministerstwo Cyfryzacji) | obecny gracz | PL | Otwarte polskie modele dla administracji publicznej, v2.2 z 12.2025 | tylko model, nie aplikacja | Apache 2.0, za darmo |
| Sputnik Software, Asseco, Rekord | obecny gracz | PL | Oprogramowanie finansowe i ERP dla gmin | niezweryfikowane, strony nie sprawdzone lub niedostępne | niepublicznie |
| Microsoft 365 Copilot | platforma globalna | globalnie | Asystent w Office dla urzędów korzystających z M365 | wysoki, chmura | licencja na stanowisko |
| Lokalni integratorzy IT | firma doradcza | PL | Sprzęt, sieci, wdrożenia EZD | niski | wg projektu |

Szukałem 14.10.2026 (Bing, polskie zapytania o asystentów AI dla gmin) i nie znalazłem polskiego dostawcy sprzedającego lokalnego agenta do przygotowywania szkiców dla gmin; to nie jest wyszukiwanie wyczerpujące. Nie walczyłbym z dostawcami EZD: wpiąłbym się obok nich jako dodatek albo sprzedawał przez nich.

**Kontra z pięciu stron.**
- **Klient:** Małe gminy mają niewielkie budżety IT i boją się być pierwsze; sekretarz musi ufać szkicom o skutku prawnym.
- **Obecny gracz:** NASK może dodać PLLuM do EZD RP za darmo, co zabiłoby płatny dodatek w urzędach korzystających z EZD RP. Madkom mógłby zrobić to samo dla swoich 1200 wdrożeń.
- **Czołowe laboratoria i big tech:** Microsoft Copilot dociera do urzędów już korzystających z M365, ale przetwarzanie akt obywateli w chmurze to zarzut, który utrzymuje sens lokalnego urządzenia.
- **Regulator:** Obowiązki z AI Act i RODO (DPIA, rejestry, nadzór człowieka) dla organu publicznego; decyzje o skutku prawnym muszą pozostać po stronie człowieka. To koszt, ale też powód wyboru rozwiązania lokalnego.
- **Ekonomia jednostkowa:** Urządzenie z GPU na urząd plus instalacja i wsparcie na miejscu są drogie przy 2500 małych klientach; jedna osoba obsłuży może 30-50 lokalizacji.

**Po kontrze.** Przetrwa jako wąski produkt: wnioski o informację publiczną, anonimizacja do BIP i rejestracja, sprzedawany przez integratorów, w cenie poniżej progu zamówień publicznych. Wynik zostaje na poziomie około 71, ale F jest niskie; zaplanowałbym 9-12-miesięczne cykle sprzedaży.

**Liczby.**
- 2477 gmin (GUS TERYT, nie zweryfikowano ponownie).
- Modele PLLuM 4B, 12B, 8B i 70B, v2.2 z 12.2025; PLLuM-12B-instruct-2512 jest na licencji Apache 2.0 na bazie Mistral-Nemo (Hugging Face, 10.2026).
- Bielik 11B v3.0 Instruct, Apache 2.0, wersja bazowa wydana 30.07.2025 (Hugging Face).
- Madkom: 1200 wdrożeń, 120000 użytkowników *(deklaracja dostawcy)*.
- Obowiązek EZD najwcześniej od 1.01.2029 *(szacunek zewnętrzny, fragment wyników wyszukiwania powołujący się na ministerstwo)*.
- Polska 8,4% wykorzystania AI w przedsiębiorstwach w 2025 (Eurostat).

**Jak zacząć.**
1. Tygodnie 1-4: na lokalnym sprzęcie pipeline dla wniosków o informację publiczną: klasyfikacja, szkic odpowiedzi, anonimizacja, z PLLuM 12B i małym korpusem prawa.
2. Tygodnie 5-6: pilotaż w jednej przyjaznej gminie na zanonimizowanych pismach z archiwum; pomiar zaoszczędzonych minut pracy urzędnika.
3. Tygodnie 7-8: spakowanie w małe urządzenie (jedno GPU) z interfejsem webowym i dziennikiem audytu; gotowy wzór DPIA.
4. Pierwszych 10 klientów: 2-3 integratorzy, którzy obsługują już po 20+ gmin; darmowy pilotaż, płatne od 3. miesiąca.
5. Test cen: wdrożenie + roczna licencja kontra stała opłata miesięczna, obie poniżej 130000 PLN łącznie.

**Ryzyka i ograniczenia.**
- NASK lub Madkom wprowadzą funkcje PLLuM bez opłat.
- Powolne zakupy publiczne; budżety ustalane z rocznym wyprzedzeniem.
- Wsparcie sprzętowe na miejscu dla firmy 1-3 osobowej.
- Odpowiedzialność i obowiązki z AI Act za szkice o skutku prawnym.

**Kiedy przerwać.** Przerwać, jeśli żadna gmina ani integrator nie podpisze płatnego pilotażu w ciągu 6 miesięcy lub jeśli EZD RP ogłosi wbudowane przygotowywanie szkiców z PLLuM.

**Źródła:** [EZD RP](https://www.gov.pl/web/ezd-rp) · [Madkom](https://www.madkom.pl) · [Kolekcja PLLuM](https://huggingface.co/CYFRAGOVPL) · [PLLuM 12B instruct 2512](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512) · [Bielik 11B v3](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [Eurostat – wykorzystanie AI 2025](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2) · [Sprawozdania UZP](https://www.gov.pl/web/uzp/sprawozdania-o-funkcjonowaniu-systemu-zamowien-publicznych)

---

## 3. Agent dokumentacji zgodności z NIS2 / KSC dla nowo objętych podmiotów w Polsce

**Region:** PL (potem CEE) · **Kupujący:** średnie i duże firmy nowo zaklasyfikowane jako „podmiot kluczowy” lub „podmiot ważny” na podstawie znowelizowanej ustawy o KSC oraz obsługujące je firmy IT/MSP · **Model przychodu:** opłata wdrożeniowa za podmiot + roczna subskrypcja za aktualizację dokumentów, przygotowywanie zgłoszeń incydentów i przygotowanie do audytu · **Konkurencja:** średnia · **Dopasowanie modeli lokalnych:** wysokie · **Wynik: 71** (M15 G13 C9 L13 F12 R9)

> Twardy, określony datą termin (3.04.2027) oraz dokumenty, których nikt nie chce wysyłać do amerykańskiej chmury, czynią z tego najbardziej „bankowalną” falę compliance w Polsce w tej chwili, ale okno na sprzedaż „pierwszego SZBI” to około 6 miesięcy.

**Asymetria.** Polska transponowała NIS2 z opóźnieniem: Komisja wysłała Polsce uzasadnioną opinię 7.05.2025 za brak transpozycji (strona KE o transpozycji NIS, aktualizacja 1.07.2025). Ustawa nowelizująca nosi datę 23.01.2026 (Dz.U. 2026 poz. 252) i weszła w życie 3.04.2026 (API ELI Sejmu). Podmioty, które spełniały kryteria w tym dniu, muszą wdrożyć obowiązki z rozdziału 3 (analiza ryzyka, SZBI, polityki, obsługa incydentów) w ciągu 12 miesięcy, czyli do 3.04.2027, a podmioty kluczowe muszą przejść pierwszy audyt w ciągu 24 miesięcy (art. 33 ustawy nowelizującej). Tysiące średnich firm w 18 sektorach (próg zaczyna się od średniego przedsiębiorstwa, 50+ pracowników, według nis2.org.pl, stan prawny z 10.07.2026) nigdy nie prowadziło SZBI. Tylko 8,36% polskich przedsiębiorstw używało jakiejkolwiek AI w 2025 roku wobec 19,95% w UE (Eurostat, 12.2025). Dziś pracę wykonują konsultanci piszący zestawy polityk w Wordzie i rejestry ryzyka w Excelu. Luka pozostaje otwarta do pierwszych audytów w latach 2027-2028, które rozstrzygną, co znaczy „wystarczająco dobrze”.

**Kto płaci i ile.** Liczba podmiotów objętych ustawą w Polsce: nie znaleziono oficjalnej liczby (przeszukano gov.pl, biznes.gov.pl, nis2.org.pl). Kary wyznaczają punkt odniesienia budżetu: podmioty kluczowe do 10 mln EUR lub 2% przychodu, podmioty ważne do 7 mln EUR lub 1,4% przychodu, a do 100 mln PLN przy poważnych zagrożeniach; kierownik podmiotu ponosi odpowiedzialność osobistą (art. 8c, art. 73 w brzmieniu po nowelizacji). Ceny usług doradczych: nis2.org.pl publikuje stronę z ofertą, ale nie znaleziono kwot; gdzie indziej wycena indywidualna. Cena, którą zaakceptuje firma z 50-250 osobami: zakładam 15 000-40 000 PLN za pierwszy pakiet dokumentów i 1000-3000 PLN miesięcznie za utrzymanie (moja hipoteza do przetestowania). Kanał: MSP, integratorzy IT i audytorzy ISO 27001, którzy już mają tych klientów i brakuje im ludzi.

**Aplikacja agentowa.**
1. Pobranie: kwestionariusz, lista zasobów, schemat sieci, istniejące dokumenty ISO 9001/27001, lista dostawców.
2. Ekstrakcja: zbudowanie rejestru zasobów i dostawców, zmapowanie usług na załącznik sektorowy KSC i test wielkości (memo kwalifikacyjne podmiotu).
3. Wnioskowanie: analiza ryzyka dla każdego zasobu (katalog zagrożeń zmapowany na środki z art. 8), lista luk względem ustawy i aktów wykonawczych.
4. Szkic: zestaw polityk (SZBI, obsługa incydentów, BCP, łańcuch dostaw, kontrola dostępu), plan postępowania z ryzykiem, dane do wpisu do rejestru.
5. Weryfikacja: agent kontrolny wskazuje artykuł dla każdego wymogu; konsultant-człowiek zatwierdza. **Bramka ludzka:** zatwierdzenie polityk i akceptacji ryzyka przez kierownictwo (odpowiedzialność prawna kierownika podmiotu).
6. Działanie: tryb incydentu przygotowuje teksty wczesnego ostrzeżenia w 24 h i zgłoszenia w 72 h do CSIRT; zgłasza człowiek.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| Pobranie zasobów, sieci i dostawców | tak | nie | mapy sieci i podatności to najbardziej wrażliwe dane, jakie firma ma |
| Memo kwalifikacyjne | tak | opcjonalna weryfikacja | rozumowanie prawne po polsku, niski wolumen |
| Analiza ryzyka i redakcja polityk | tak | nie | zawiera słabości; kupujący zapytają, gdzie to jest przetwarzane |
| Tworzenie szablonów (ogólnych, bez danych klienta) | nie | tak | najlepsza jakość dla szablonów wzorcowych, bez tajemnic w środku |
| Redakcja zgłoszeń incydentów | tak | nie | czas krytyczny, działanie offline, zawiera dane z trwającego incydentu |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
|---|---|---|---|---|---|
| Vanta | platforma globalna | globalnie | dedykowany produkt NIS 2: gotowe kontrole, 400+ integracji, ryzyko dostawców, szablony polityk | mapowanie kontroli przez AI, redakcja polityk, chatbot do polityk *(deklaracja dostawcy)* | demo, niepubliczna |
| Drata, Sprinto i podobne SaaS GRC | platforma globalna | globalnie | automatyzacja compliance dla ISO 27001 i SOC 2 | niezweryfikowane w tym przebiegu | niezweryfikowane w tym przebiegu |
| nis2.org.pl | firma doradcza | PL | poradniki KSC, FAQ, oferta wdrożenia | nie znaleziono | strona „ceny orientacyjne”, nie znaleziono kwot |
| Wielka Czwórka i audytorzy ISO 27001 w PL | firma doradcza | PL | analiza luk, pakiety polityk, audyty | ręcznie | stawki dzienne, niepubliczne |
| Polskie MSP i integratorzy | obecny gracz | PL | usługi bezpieczeństwa w pakiecie z NIS2 | nie znaleziono | nie znaleziono |

Vanta już oferuje NIS 2, więc „brak konkurenta z AI” to nieprawda. Globalne platformy GRC są zbudowane wokół integracji chmurowych i dyrektywy UE, a nie polskiego rejestru KSC, polskich formularzy CSIRT i polskojęzycznych polityk. Pokonać je można polskim mapowaniem prawnym i przetwarzaniem on-prem; sprzedawać przez MSP, a nie przeciwko nim.

**Kontra z pięciu stron.**
- **Klient:** wiele firm kupi najtańszy pakiet szablonów albo zignoruje temat, aż spadnie kara; kierownik chce podpisu konsultanta, a nie oprogramowania.
- **Obecny gracz:** MSP i audytorzy mogą kupić te same modele otwarte i zbudować to samo; Vanta lub Drata mogą dodać mapowanie ram KSC.
- **Czołowe laboratoria i big tech:** asystent ogólny potrafi dziś napisać przyzwoity szkic polityki; fosa to polskie mapowanie, dane rejestrowe i dowody audytowe, a nie samo redagowanie.
- **Regulator:** rozporządzenia wykonawcze mogą zmienić wymogi; narzędzie nie może twierdzić, że daje „zgodność”, tylko dowody i szkice sprawdzone przez wykwalifikowaną osobę.
- **Ekonomia jednostkowa:** sprzedaż pierwszego pakietu osiąga szczyt przed kwietniem 2027; potem przychód powtarzalny zależy od audytów, obsługi incydentów i ocen dostawców.

**Po kontrze.** Przetrwa jako narzędzie white-label dla MSP i audytorów ISO, uruchamiane na urządzeniu u MSP lub klienta, wyceniane za podmiot rocznie. Porzucić pitch „zastąp konsultanta”. R zostaje 9 z powodu klifu po terminie.

**Liczby.**
- Ustawa z 23.01.2026 nowelizująca KSC, Dz.U. 2026 poz. 252, w mocy od 3.04.2026 (API ELI Sejmu, odczyt 14.10.2026).
- Obowiązki w ciągu 12 miesięcy, pierwszy audyt podmiotów kluczowych w ciągu 24 miesięcy (art. 33 ustawy).
- Wniosek o wpis w ciągu 6 miesięcy od spełnienia kryteriów (art. 7c), wczesne ostrzeżenie 24 h, zgłoszenie 72 h.
- Kary: kluczowe do 10 mln EUR / 2%, ważne do 7 mln EUR / 1,4%, do 100 mln PLN w poważnych przypadkach (art. 73 po nowelizacji).
- Polska 8,36% przedsiębiorstw używających AI wobec 19,95% w UE w 2025 (Eurostat, 12.2025).
- Liczba podmiotów objętych ustawą w Polsce: nie znaleziono.

**Jak zacząć.**
1. Tygodnie 1-3: mapa wymogów KSC (artykuł do kontroli do dokumentu), polski zestaw szablonów, test kwalifikacji.
2. Tygodnie 3-6: lokalny potok na stanowisku z Bielikiem lub Qwenem do redakcji i weryfikator cytowań; jeden prawdziwy pilotaż przez audytora ISO.
3. Tygodnie 6-8: redaktor zgłoszeń incydentów i moduł kwestionariusza dostawców.
4. Pierwszych 10 klientów: 3-5 MSP lub audytorów w Polsce, każdy przynosi 2-5 podmiotów.
5. Test cenowy: 990 vs 2490 PLN za podmiot miesięcznie dla MSP; stały pierwszy pakiet za 9900 PLN.

**Ryzyka i ograniczenia.**
- Odpowiedzialność, jeśli sporządzona polityka pomija jakiś wymóg; umowy muszą zostawiać wykwalifikowanego człowieka jako autora.
- Skok popytu przed 3.04.2027, potem spowolnienie.
- Rozporządzenia wykonawcze i wytyczne krajowego organu cyberbezpieczeństwa mogą zmienić szablony.
- Kanał MSP zabiera marżę i może skopiować produkt.

**Kiedy przerwać.** Przerwać, jeśli do końca stycznia 2027 mniej niż 3 MSP lub audytorów zapłaci za pilotaż.

**Źródła:** [Dz.U. 2026 poz. 252 via Sejm ELI API](https://api.sejm.gov.pl/eli/acts/DU/2026/252/text.pdf) · [EC NIS2 transposition](https://digital-strategy.ec.europa.eu/en/policies/nis-transposition) · [nis2.org.pl FAQ](https://nis2.org.pl/faq-nis2) · [Vanta NIS 2](https://www.vanta.com/products/nis2) · [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

---

## 4. Dokumentowanie i modernizacja kodu legacy on-prem dla MŚP i firm regulowanych

**Region:** PL / UE · **Kupujący:** dyrektorzy techniczni (CTO) i szefowie IT w MŚP, bankach spółdzielczych, regionalnych ubezpieczycielach i miejskich spółkach komunalnych, które utrzymują systemy w Delphi, Clarion, Visual FoxPro, starym PHP lub COBOL-u · **Model przychodu:** ocena za stałą cenę + pakiet dokumentacji za każdą bazę kodu + opcjonalna licencja na urządzenie on-prem · **Konkurencja:** średnia · **Dopasowanie modeli lokalnych:** wysokie · **Wynik: 70** (M12 G15 C11 L14 F11 R7)

> Mocne dopasowanie do podejścia „najpierw lokalnie”: kod nie może opuścić budynku, duże platformy modernizacyjne celują w mainframe’y i firmy z Fortune 500, a długi ogon średniego rynku z Delphi/FoxPro pozostaje bez obsługi, ale darmowe AWS Transform ustawia punkt odniesienia cenowego dla segmentu COBOL.

**Asymetria.** Tylko 8,36% polskich przedsiębiorstw używało AI w 2025 roku wobec 19,95% w UE, a wśród małych firm w całej UE 17% (Eurostat, 2025). Systemy objęte zakresem (magazyn, fakturowanie, dodatki do ERP napisane w Delphi, Clarion, FoxPro, PHP 5) powstały z rąk ludzi, którzy odchodzą na emeryturę; dokumentacją jest zwykle sam kod. Kupujący skali mainframe’ów mają już narzędzia AI (AWS Transform, IBM watsonx Code Assistant for Z, Mechanical Orchard), ale te celują w COBOL/PL/I na mainframe’ach i w bardzo duże firmy. Poniżej tego poziomu pracę nadal wykonują ręcznie software house’y za stawki dzienne. Luka pozostaje otwarta, dopóki narzędzia hiperskalerów ignorują stosy 4GL/desktopowe, a banki i ubezpieczyciele zabraniają wysyłania kodu źródłowego do publicznego API.

**Kto płaci i ile.** Liczba MŚP i banków spółdzielczych, które w PL/UE nadal używają Delphi/FoxPro/Clarion: nie znaleziono (nie istnieje spis starych stosów technologicznych). Zastępczy kupujący: banki spółdzielcze, regionalni ubezpieczyciele, firmy komunalne, producenci z własnym ERP. Ile płacą dziś: stawki dzienne software house’ów za inżynierię wsteczną (stawki nie znaleziono w publicznym źródle w tej sesji). Ceny do przetestowania: 3000-8000 EUR za stałą cenę „codebase X-ray” (mapa architektury, słownik danych, katalog reguł biznesowych, inwentarz testów), potem 1000-3000 EUR miesięcznie w trakcie migracji. Kanał: bezpośrednie docieranie przez LinkedIn do szefów IT, partnerstwa z polskimi software house’ami, które sprzedają przepisanie systemu, a brakuje im zdolności analitycznych.

**Aplikacja agentowa.**
1. Pobranie: migawka repozytorium lub zasobu plikowego skopiowana na urządzenie u klienta (bez ruchu wychodzącego do sieci); parsowanie za pomocą tree-sitter lub parserów właściwych dla danego języka tam, gdzie istnieją, a dla Clarion/FoxPro awaryjnie dzielenie surowego tekstu na fragmenty.
2. Ekstrakcja: graf wywołań, schemat bazy danych, formularze, SQL osadzony w kodzie, konfiguracja i zadania wsadowe.
3. Wnioskowanie: agent per moduł opisuje cel, wejścia/wyjścia, reguły biznesowe i oznacza martwy kod; drugi agent weryfikuje twierdzenia względem grafu wywołań.
4. Szkic: dokument architektury, słownik danych, katalog reguł biznesowych po polsku lub angielsku, propozycje testów charakteryzujących.
5. Weryfikacja: wygenerowane testy uruchamiane na systemie legacy tam, gdzie da się go uruchomić; twierdzenia niemożliwe do sprawdzenia oznaczane jako „niezweryfikowane”.
6. Działanie: bramka zatwierdzenia przez człowieka, zanim jakikolwiek dokument zostanie dostarczony jako „stan faktyczny as-is” albo jakikolwiek przepisany moduł zastąpi kod produkcyjny.

**Podział lokalny i płatny.**
| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
| --- | --- | --- | --- |
| Parsowanie i dzielenie na fragmenty | Niepotrzebny (narzędzia deterministyczne) | Niepotrzebne | Parsery kodu są tańsze i dokładne |
| Streszczenia per moduł | Tak, na urządzeniu klienta | Nie | Kod źródłowy to poufny zasób |
| Wnioskowanie o architekturze między modułami | Tak, domyślnie | Tylko na zanonimizowanych streszczeniach, jeśli klient się zgodzi | Wnioskowanie w długim kontekście jest silniejsze w modelach czołowych |
| Pisanie dokumentacji po polsku | Tak (Bielik 11B v3 lub model wielojęzyczny) | Opcjonalnie | Jakość językowa wystarcza dla prozy technicznej |
| Propozycje przepisania | Tak | Opcjonalnie, na zanonimizowanym kodzie | Jakość przepisania ma znaczenie, ale kod może nie opuszczać firmy |

**Konkurencja.**
| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
| --- | --- | --- | --- | --- | --- |
| AWS Transform | platforma globalna | globalnie | Agenci do modernizacji mainframe’ów, Windows/.NET i VMware | Głęboka, agentowa | Agent mainframe za darmo, agent własnej transformacji 0,035 USD za minutę pracy agenta (strona z cennikiem, 10.2026) |
| IBM watsonx Code Assistant for Z | platforma globalna | globalnie | Rozumienie COBOL-a i PL/I oraz transformacja COBOL-a do Javy | Głęboka | Niepubliczna |
| Mechanical Orchard (Imogen) | startup | USA / globalnie | Przepisuje systemy mainframe na kod chmurowy z automatyczną weryfikacją, celuje w firmy z Fortune 20-500 | Głęboka | Niepubliczna, bezpłatny proof of concept |
| GitHub Copilot i asystenci w stylu Claude Code | platforma globalna | globalnie | Ogólne asystenty kodu użyteczne w każdym języku | Średnia dla stosów 4GL | Za stanowisko, w chmurze |
| Polskie software house’y wykonujące przepisywanie | firma doradcza | PL | Ręczna analiza plus projekty przepisywania | Niska do średniej | Stawki dzienne, niepubliczne |
| Duże firmy doradcze (Accenture, Capgemini, Deloitte) | firma doradcza | UE | Programy modernizacji z własnymi akceleratorami AI | Średnia | Ceny programowe, niepubliczne |

Luka: średni rynek, stosy 4GL spoza mainframe’ów, tylko on-prem, wynik po polsku, stała cena. Unikać segmentu COBOL-owych mainframe’ów, gdzie AWS jest za darmo, a IBM jest właścicielem platformy.

**Kontra z pięciu stron.**
- **Klient:** „Przepiszemy to kiedyś” to plan sprzed dekady; samą dokumentację łatwo odłożyć. Impulsem jest zwykle odchodzący na emeryturę programista albo ustalenie audytu, więc sprzedaż musi wyłapywać te momenty.
- **Obecny gracz:** Pierwotny dostawca lub lokalny software house może dodać LLM do własnej analizy. Partnerstwo z nimi (my sprzedajemy X-ray, oni sprzedają przepisanie) zamienia zagrożenie w kanał.
- **Czołowe laboratoria i big tech:** Agenci kodujący poprawiają się co kwartał i działają w każdym języku, więc klient z zatwierdzoną polityką chmurową może zrobić dużą część tego sam. Obronny jest tylko segment „nie może opuścić budynku”.
- **Regulator:** Banki i ubezpieczyciele podlegają DORA i przepisom o outsourcingu; urządzenie u klienta bez ruchu wychodzącego omija większość papierkowej roboty związanej z ryzykiem stron trzecich, co jest atutem sprzedażowym, a nie przeszkodą.
- **Ekonomia jednostkowa:** Każda baza kodu jest unikalna; praca nad parserem dla Clarion lub FoxPro to jednorazowy wysiłek per język. Pakiety za stałą cenę trzeba wyceniać według liczby linii kodu, aby nie tracić na systemach-spaghetti.

**Po kontrze.** Przetrwa jako nisza: on-premowy „codebase X-ray” dla starych stosów spoza mainframe’ów w firmach regulowanych lub dbających o tajemnicę, sprzedawany przez polskie software house’y. Wynik spada w trwałości (R7), ponieważ agenci kodujący utowarowią ogólne rozumienie kodu.

**Liczby.**
- Przedsiębiorstwa UE używające AI: 19,95% w 2025; małe 17%, średnie 30,36%, duże 55,03% (Eurostat, dane za 2025).
- Polska: 8,36% przedsiębiorstw używało AI w 2025 (Eurostat, dane za 2025).
- AWS Transform: agenci do mainframe’ów, Windows i VMware bezpłatnie; agent własnej transformacji 0,035 USD za minutę pracy agenta (strona z cennikiem AWS, odczytana 14.10.2026) *(deklaracja dostawcy)*.
- Mechanical Orchard: skrócenie modernizacji z około 18 miesięcy do około 5 miesięcy *(deklaracja dostawcy, strona internetowa odczytana 14.10.2026)*.
- Liczba systemów Delphi/FoxPro/Clarion w PL/UE: nie znaleziono.

**Jak zacząć.**
1. Tygodnie 1-4: zbudować potok X-ray dla starego PHP i Delphi (najlepsze wsparcie parserów) na lokalnym sprzęcie; testować na publicznych open-source’owych repozytoriach legacy.
2. Tygodnie 5-8: spakować jako urządzenie odcięte od sieci (air-gapped) (jedna stacja robocza z GPU lub serwer klienta) z pisemnym oświadczeniem o postępowaniu z danymi.
3. Pierwszych 10 klientów: 3 polskie software house’y jako resellerzy, 7 bezpośrednio (banki spółdzielcze, regionalni producenci) przez LinkedIn i lokalne spotkania branży IT.
4. Test cenowy: zaoferować ten sam pakiet za 3000 i 6000 EUR porównywalnym potencjalnym klientom; śledzić wskaźnik zamknięcia i nakład godzin.

**Ryzyka i ograniczenia.**
- Zhalucynowane reguły biznesowe w dokumencie opisanym jako „as-is” mogą wprowadzić migrację w błąd; każde twierdzenie wymaga odwołania do kodu.
- Parsery 4GL są słabe lub ich brak; jakość dla Clarion/FoxPro może odstawać od PHP i Delphi.
- Koszt sprzętu i wsparcie urządzenia u klienta zjadają marżę przy małych transakcjach.
- Długie cykle sprzedaży w bankach (przeglądy bezpieczeństwa), nawet gdy nic nie opuszcza budynku.

**Kiedy przerwać.** Przerwać, jeśli po 6 miesiącach sprzedano mniej niż 3 płatne X-ray’e albo realizacja zajmuje średnio więcej niż 2 razy tyle godzin, ile wyceniono.

**Źródła:** [Eurostat: Use of AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [AWS Transform pricing](https://aws.amazon.com/transform/pricing/) · [IBM watsonx Code Assistant for Z](https://www.ibm.com/products/watsonx-code-assistant-z/pricing) · [Mechanical Orchard](https://www.mechanical-orchard.com/) · [SpeakLeash Bielik models](https://huggingface.co/speakleash)

---

## 5. Asystent przetargowy dla polskich MŚP startujących w przetargach

**Region:** najpierw PL, potem UE (TED) · **Kupujący:** MŚP-wykonawcy startujący w zamówieniach publicznych (roboty budowlane, dostawy, usługi) i małe biura doradztwa przetargowego · **Model przychodu:** abonament na firmę + opłata za „pakiet SWZ" przy każdym przetargu · **Konkurencja:** średnia · **Dopasowanie modeli lokalnych:** średnie · **Wynik: 70** (M17 G14 C9 L9 F12 R9)

> Prawdziwy, duży rynek pełen papierologii, na którym polskie portale przetargowe wciąż sprzedają wyszukiwarkę i powiadomienia e-mail, więc agent, który czyta SWZ i buduje listę kontrolną zgodności, ma 1-2 lata okna.

**Asymetria.** Polskie zamówienia publiczne na podstawie ustawy Pzp były w 2024 roku warte około 330,4 mld PLN (9,07% PKB), w około 153000 udzielonych zamówień, przy 130002 ogłoszeniach w biuletynie BZP i 31940 polskich ogłoszeń w TED (sprawozdanie UZP za 2024, opublikowane w 2025). MŚP złożyły 95% ofert w przetargach na roboty budowlane poniżej progów unijnych oraz 84-85% w dostawach i usługach. Każda z tych ofert oznacza ręczne czytanie SWZ (specyfikacji warunków zamówienia), formularzy (JEDZ/ESPD, oświadczenia), warunków umowy i zmian wynikających z pytań i odpowiedzi. Wykorzystanie AI w polskich przedsiębiorstwach wyniosło w 2025 roku 8,4%, jedno z najniższych w UE (Eurostat, 11.12.2025). Największa sprawdzona przez nas polska baza przetargów, Oferent, sprzedaje wyszukiwanie i powiadomienia, bez funkcji AI na stronie z cennikiem (14.10.2026). Luka istnieje, bo obecni gracze to wydawcy i agregatory, a nie firmy programistyczne, a praca dotyczy prawniczego tekstu po polsku.

**Kto płaci i ile.** Około 52000 wykonawców wygrało w 2024 roku zamówienia poniżej progów unijnych (UZP), co jest dolną granicą liczby aktywnych oferentów. Już płacą za bazy przetargów: Oferent 900 PLN za kwartał lub 2000 PLN za rok (strona z cennikiem dostawcy, 10.2026). Koszt ręczny to dni pracy specjalisty ds. ofert przy każdej ofercie; wynagrodzeń na tym stanowisku nie znaleziono w tej sesji. Ceny do przetestowania: 249-499 PLN miesięcznie na firmę lub 99-199 PLN za przeanalizowany przetarg. Kanał: bezpośredni kontakt z powtarzającymi się oferentami znalezionymi w ogłoszeniach o udzieleniu zamówienia w BZP (dane publiczne), regionalne stowarzyszenia budowlane, doradcy przetargowi jako resellerzy.

**Aplikacja agentowa.**
1. Pobranie: odpytywanie e-Zamówień/BZP i ogłoszeń TED, pobieranie pakietów SWZ i późniejszych zmian.
2. Ekstrakcja: warunki udziału, terminy, wadium, wymagane dokumenty, kryteria oceny ofert, kary umowne.
3. Wnioskowanie: ocena start/nie start względem profilu firmy (obrót, referencje, certyfikaty); oznaczanie ryzykownych klauzul.
4. Szkic: lista kontrolna zgodności, lista dokumentów, pytania do zamawiającego, pierwszy szkic oświadczeń i formularza ofertowego.
5. Weryfikacja: drugie przejście porównuje każdą pozycję listy kontrolnej z cytowanym paragrafem SWZ; porównanie zmian w SWZ.
6. Działanie: **bramka akceptacji przez człowieka** przed podpisaniem lub złożeniem czegokolwiek; agent nigdy nie podpisuje ani nie składa oferty.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| Wstępna selekcja i klasyfikacja ogłoszeń | Bielik 11B v3 lub PLLuM 12B | nie | Duży wolumen, krótkie teksty po polsku, koszt na ogłoszenie bliski zeru |
| Ekstrakcja SWZ do pól | DeepSeek-V4-Flash na lokalnym sprzęcie | zapas dla długich skanowanych PDF-ów | Praca masowa; dokumenty przetargowe są publiczne, więc tajemnica nie jest motorem |
| Wnioskowanie o ryzykownych klauzulach | najpierw lokalnie | Claude dla trudnych umów | Jakość ma znaczenie tam, gdzie pominięta klauzula kosztuje wadium |
| Szkic oferty z danymi firmy | lokalnie | opcjonalnie | Dane finansowe i ceny firmy zostają u oferenta |
| Przejście weryfikacyjne | lokalnie | wyrywkowe kontrole | Tania druga opinia, wymagane cytaty |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Poziom AI | Cena |
|---|---|---|---|---|---|
| Oferent | obecny gracz | PL | Baza przetargów od 2007, powiadomienia, wyniki | brak na stronie z cennikiem | 2000 PLN rocznie |
| Portal ZP (Pressinfo) | obecny gracz | PL | Wyszukiwarka przetargów, portal premium, webinary o AI dla SWZ | treści o AI, nie widziano agenta SWZ | na zapytanie, 14-dniowy okres próbny |
| Biznes-Polska | obecny gracz | PL | Codzienne aktualizacje przetargów, oferty B2B | niezweryfikowane | nie sprawdzono |
| Tendium | startup | Szwecja, Norwegia, Finlandia | Streszczenia przetargów z AI, BidFlow, asystent pisania | wysoki | od 125 EUR miesięcznie |
| Stotles | startup | Wielka Brytania | Streszczenia ogłoszeń z AI, raporty start/nie start, współpilot do szkiców | wysoki | Bid Studio od 990 GBP miesięcznie |
| Brainial | startup | UE (NL, DE, SV) | Analiza dokumentów, oznaczanie ryzyk, pisanie ofert | wysoki | niepublicznie |
| ChatGPT lub Copilot | platforma globalna | globalnie | Ogólny czat nad wgranym SWZ | ogólny | plany konsumenckie i biznesowe |

Szukałem 14.10.2026 polskiego produktu analizującego SWZ z użyciem AI (Bing, polskie zapytania): wyniki pokazały tylko portale; tendersguru.pl się nie otworzył. To nie jest wyszukiwanie wyczerpujące. Luka: nordyckie, brytyjskie i holenderskie narzędzia przetargowe z AI nie zostały zlokalizowane pod Pzp i polskie formularze; polskie portale nie wypuściły agentów. Wygrywa się listami kontrolnymi specyficznymi dla Pzp i ceną poniżej 500 PLN miesięcznie.

**Kontra z pięciu stron.**
- **Klient:** Mali budowlańcy kupują za cenę i na zaufaniu; wielu wklei SWZ do ChatGPT za darmo. Trzeba pokazać pominiętą klauzulę lub utracone wadium, które agent by wychwycił.
- **Obecny gracz:** Oferent i Pressinfo mają ruch i powiadomienia; dołożenie streszczenia z LLM do ich listingu to dla nich kwartał pracy. Ich dotychczasowa powolność to jedyna fosa.
- **Czołowe laboratoria i big tech:** Modele ogólne już dobrze streszczają PDF-y; wartość musi leżeć w zestawie reguł Pzp, profilu firmy i przepływie pracy wokół terminów, a nie w streszczeniu.
- **Regulator:** Niskie ryzyko, bo dokumenty przetargowe są publiczne. Ryzyko odpowiedzialności, jeśli lista kontrolna pominie wymagany dokument i oferta zostanie odrzucona: warunki muszą czynić podpisującym człowieka.
- **Ekonomia jednostkowa:** Długie pakiety SWZ (setki stron) sprawiają, że koszty płatnego API dają się we znaki przy niskich cenach; lokalny sprzęt obniża koszt na przetarg niemal do zera, i to jest prawdziwy powód, by działać lokalnie.

**Po kontrze.** Przetrwa jako nisza: lista kontrolna zgodności z Pzp plus ocena start/nie start dla MŚP z branży budowlanej i dostawczej, najpierw lokalnie ze względu na koszt, sprzedawana przez doradców przetargowych. Wynik zostaje około 70, słabym punktem jest C.

**Liczby.**
- 330,4 mld PLN zamówień Pzp w 2024, 9,07% PKB; około 153000 zamówień (sprawozdanie UZP 2024).
- 130002 ogłoszeń BZP i 31940 polskich ogłoszeń TED w 2024 (sprawozdanie UZP 2024).
- Średnio 2,89 oferty na przetarg poniżej progów unijnych w 2024; MŚP złożyły 95% ofert w robotach poniżej progów unijnych (sprawozdanie UZP 2024).
- Około 52000 wykonawców wygrało zamówienia poniżej progów unijnych w 2024 (sprawozdanie UZP 2024).
- Polska: 8,4% przedsiębiorstw (10+ pracowników) używało AI w 2025 (Eurostat, 11.12.2025).
- Oferent 2000 PLN rocznie, bez AI w ofercie *(deklaracja dostawcy, 10.2026)*; Tendium od 125 EUR miesięcznie *(deklaracja dostawcy)*; Stotles Bid Studio od 990 GBP miesięcznie *(deklaracja dostawcy)*.

**Jak zacząć.**
1. Tygodnie 1-4: pipeline dla jednej rodziny CPV (roboty drogowe i budowlane), pobieranie z BZP, SWZ do JSON z listą kontrolną, cytaty przy każdej pozycji.
2. Tygodnie 5-6: test na 30 dawnych przetargach o znanych wynikach; pomiar pominiętych wymagań.
3. Tygodnie 7-8: aplikacja webowa z profilem firmy i kalendarzem terminów; ekran akceptacji przez człowieka.
4. Pierwszych 10 klientów: wykonawcy, którzy przegrali ofertę z powodów formalnych (widocznych w ogłoszeniach o udzieleniu zamówienia), plus 2-3 doradców przetargowych jako resellerzy.
5. Test cen: 149 PLN za przetarg kontra 399 PLN miesięcznie, test A/B na pierwszych 20 leadach.

**Ryzyka i ograniczenia.**
- Obecne portale dodadzą streszczenia z AI i dołączą je do istniejącego abonamentu za 2000 PLN.
- Odpowiedzialność za pominięte wymaganie; potrzebne jasne warunki i widoczne cytaty.
- Skanowane i źle ustrukturyzowane pliki SWZ wymagają OCR; jakość bywa różna.
- Skłonność MŚP do płacenia jest niska, a rezygnacje sezonowe.

**Kiedy przerwać.** Przerwać, jeśli mniej niż 5 z pierwszych 30 firm pokazowych zapłaci po 4-tygodniowym okresie próbnym lub jeśli Oferent albo Pressinfo wprowadzą listy kontrolne SWZ bez dodatkowej opłaty.

**Źródła:** [Sprawozdanie UZP 2024](https://www.gov.pl/attachment/b61cce3a-f71c-4271-be11-d7eaa1a03f76) · [Indeks sprawozdań UZP](https://www.gov.pl/web/uzp/sprawozdania-o-funkcjonowaniu-systemu-zamowien-publicznych) · [Eurostat – wykorzystanie AI 2025](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2) · [Cennik Oferenta](https://www.oferent.com.pl/cennik) · [Portal ZP](https://portalzp.pl) · [Cennik Tendium](https://www.tendium.com/pricing) · [Cennik Stotles](https://www.stotles.com/pricing) · [Brainial](https://www.brainial.com) · [Bielik 11B v3](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [PLLuM 12B instruct](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512)

---

## 6. Lokalny asystent prawny dla małych polskich kancelarii

**Region:** PL · **Kupujący:** małe kancelarie adwokatów i radców prawnych (1-15 prawników) · **Model przychodu:** wdrożenie + box na miejscu + miesięczna licencja · **Konkurencja:** średnia · **Dopasowanie modeli lokalnych:** wysokie · **Wynik: 67** (M14 G13 C8 L13 F11 R8)

> Luka prawdziwa, ale się zawęża: sprzedać małym kancelariom box oparty na tajemnicy zawodowej wraz z polskimi workflow orzeczniczymi, zanim dotrą do nich AI wydawców i Gaius-Lex, i liczyć się z tym, że konkuruje się usługą, a nie modelem.

**Asymetria.** Polska jest blisko dna unijnego rankingu wykorzystania AI: 8,36% polskich przedsiębiorstw używało AI w 2025 roku wobec 19,95% w UE, a wśród małych przedsiębiorstw w całej UE tylko 17% (Eurostat, opublikowano 12.2025). Małe kancelarie nadal płacą asocjatom i aplikantom za ręczne czytanie wyroków, porównywanie wersji umów i pisanie rutynowych pism procesowych. Luka istnieje z powodu tajemnicy zawodowej (tajemnica adwokacka i tajemnica radcowska to obowiązki ustawowe), nieufności wobec amerykańskich narzędzi w chmurze oraz polskojęzycznego orzecznictwa, które globalne narzędzia obsługują słabo. Samorząd zaczął już aktywnie dyskutować o AI: strona KIRP zawiera „Rekomendacje dotyczące korzystania z AI” oraz konferencję z czerwca 2026 o AI, etyce i europejskiej suwerenności technologicznej (strona KIRP, pobrano 10.2026). Spodziewam się, że okno dla małych kancelarii zostanie otwarte przez 1-2 lata: wydawcy sprzedają AI kancelariom, które już płacą za LEX lub Legalis, a duże kancelarie najpierw kupują Harvey lub Legora.

**Kto płaci i ile.** Kupujący: tysiące małych polskich kancelarii prowadzonych przez adwokatów i radców prawnych (dokładnej liczby nie znaleziono w tym przebiegu; publikują ją rejestry samorządów). Już teraz płacą abonament za LEX (Wolters Kluwer) lub Legalis (C.H.Beck); ceny są ustalane indywidualnie i nie znaleziono ich publicznie. Realistyczna oferta: wdrożenie 6000-12 000 PLN plus 600-1500 PLN miesięcznie dla kancelarii z 3-10 prawnikami (moja hipoteza cenowa do przetestowania). Kanał: regionalne izby (izby adwokackie i okręgowe izby radców prawnych), spotkania legal-techu, firmy IT już obsługujące kancelarie oraz darmowy webinar „AI i tajemnica” oparty na rekomendacjach KIRP.

**Aplikacja agentowa.**
1. Pobranie: akta spraw, umowy i korespondencja z udziału sieciowego kancelarii lub folderu DMS; wyroki z publicznego REST API SAOS (JSON) i z portali sądowych.
2. Ekstrakcja: strony, daty, terminy, roszczenia, klauzule, przywołane artykuły, do lokalnego indeksu.
3. Rozumowanie: wyszukanie podobnych wyroków i przeciwnych linii orzeczniczych; oznaczenie ryzykownych lub brakujących klauzul na tle własnych wzorców kancelarii.
4. Szkic: memo, poprawki do klauzul (redline), pierwszy szkic pisma procesowego lub listu, z każdym cytatem powiązanym ze źródłem.
5. Weryfikacja: drugi przebieg sprawdza, czy każdy cytowany wyrok i artykuł istnieje i mówi to, co twierdzi szkic.
6. Działanie: **bramka akceptacji przez człowieka**: nic nie opuszcza kancelarii, dopóki prawnik tego nie zatwierdzi; żadnego składania pism ani e-maili do klientów bez przeglądu.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| Pobranie i OCR akt klientów | tak | nie | dane klientów objęte tajemnicą zawodową |
| Ekstrakcja i indeksowanie | tak (Bielik-11B v3, Qwen) | nie | wolumen, tajemnica |
| Wyszukiwanie orzecznictwa w publicznych wyrokach | tak | opcjonalnie | wyroki są publiczne, więc model z czołówki jest tu dozwolony |
| Pisanie szkiców na podstawie faktów klienta | tak | tylko z zanonimizowanymi danymi | tajemnica i RODO |
| Sprawdzanie cytatów | tak | nie | deterministyczne wyszukiwanie plus mały model |
| Budowa wzorców i projektowanie promptów | nie | tak (model z czołówki na etapie budowy) | brak danych klientów |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
|---|---|---|---|---|---|
| Gaius-Lex (Gaius Vault) | startup | PL | prywatne AI dla zespołów prawnych: przegląd umów, wyszukiwanie precedensów, korespondencja, z wdrożeniem on-prem i hybrydowym | wysoka | plany Lite, Standard, Pro, Edu; 7-dniowy okres próbny; kwoty niewidoczne |
| LEX (Wolters Kluwer Polska) | obecny gracz | PL | system informacji prawnej z LEX Navigator; funkcji AI nie potwierdzono w tym przebiegu | średnia (niezweryfikowane) | wycena indywidualna, nie znaleziono |
| Legalis (C.H.Beck) | obecny gracz | PL | komentarze, orzecznictwo, wzory; asystenta AI nie potwierdzono w tym przebiegu | średnia (niezweryfikowane) | wycena indywidualna, nie znaleziono |
| Harvey | platforma globalna | globalnie | platforma AI dla prawników, ponad 3500 organizacji w ponad 85 krajach *(deklaracja dostawcy)* | wysoka | tylko demo, niepubliczna |
| Legora | platforma globalna | UE (Szwecja) | agentowy system operacyjny dla prawników, dodatki do Worda i Outlooka | wysoka | tylko demo, niepubliczna |
| SAOS | baza publiczna | PL | darmowa baza orzeczeń sądowych z publicznym API | brak (źródło danych) | za darmo |

Luka: Harvey i Legora celują w duże kancelarie i są chmurowym SaaS; wydawcy zamykają AI w obrębie własnych treści; Gaius-Lex jest bezpośrednim rywalem, który ma już wersję on-prem. Pokonać ich fizycznym boxem w biurze, stałą ceną, lokalnym polskim serwisem i integracją z własnymi plikami kancelarii albo zawrzeć partnerstwo z wydawcą w zakresie treści.

**Kontra z pięciu stron.**
- **Klient:** małe kancelarie są wrażliwe na cenę i konserwatywne; wiele powie „ChatGPT wystarczy” albo „LEX to doda”. Wspólnicy muszą zaufać jednoosobowemu dostawcy w sprawie akt klientów.
- **Obecny gracz:** Wolters Kluwer i C.H.Beck mają komentarze i relację z klientem; gdy ich AI będzie dobre, samotny dostawca nie dorówna treści.
- **Czołowe laboratoria i big tech:** Copilot w Wordzie i ogólne modele czatu poprawiają się w polskim z kwartału na kwartał; tajemnica zawodowa to jedyna fosa, której nie pokrywają dla małych kancelarii.
- **Regulator:** rekomendacje samorządu w sprawie AI mogą zaostrzyć (lub złagodzić) zasady; odpowiedzialność za błędny cytat pozostaje przy prawniku, ale błąd dostawcy to ryzyko reputacyjne.
- **Ekonomia jednostkowa:** sprzęt na klienta plus serwis na miejscu pochłaniają czas; przy 1000 PLN miesięcznie potrzeba ponad 40 kancelarii, by zastąpić pensję.

**Po kontrze.** Przetrwa jako nisza: „box oparty na tajemnicy zawodowej plus workflow orzecznicze SAOS” dla kancelarii z 3-15 prawnikami, sprzedawany przez izby i integratorów IT. Nie konkurować treścią komentarzy; zintegrować się z wydawcą, któremu kancelaria już płaci. Wynik pozostaje 67, z realnym ryzykiem, że Gaius-Lex lub wydawca zniwelują lukę.

**Liczby.**
- Przedsiębiorstwa w UE korzystające z AI: 19,95% w 2025, Polska 8,36% (Eurostat, 12.2025).
- Małe przedsiębiorstwa w UE korzystające z AI: 17%; duże: 55,03% (Eurostat, 2025).
- Harvey: ponad 3500 organizacji prawniczych, ponad 200 000 profesjonalistów, ponad 85 krajów, wycena 15,5 mld USD *(deklaracja dostawcy, 10.2026)*.
- Gaius-Lex oferuje wdrożenie on-prem i hybrydowe oraz cztery plany *(deklaracja dostawcy, 10.2026)*.
- Bielik-11B-v3.0-Instruct: licencja Apache 2.0, trenowany na 32 językach europejskich z naciskiem na polski (karta modelu Hugging Face, 10.2026).
- Liczba adwokatów i radców prawnych: nie znaleziono w tym przebiegu.

**Jak zacząć.**
1. Tygodnie 1-3: pipeline na wyrokach SAOS plus jeden workflow przeglądu umów, działający na lokalnym rigu z Bielikiem i Qwenem.
2. Tygodnie 4-6: spakować to w biurowy box z jednym GPU, szyfrowanym dyskiem i dziennikiem audytu; napisać jednostronicowe memo „tajemnica i RODO” zmapowane na rekomendacje KIRP.
3. Tygodnie 6-8: pilotaż w 3 kancelariach za darmo w zamian za opinię i wycenę.
4. Pierwszych 10 klientów: webinary w izbach, spotkania legal-techu, dwaj integratorzy IT obsługujący kancelarie.
5. Test cenowy: porównać wdrożenie + 900 PLN miesięcznie z wyższym pakietem z alertami o orzecznictwie.

**Ryzyka i ograniczenia.**
- Gaius-Lex już sprzedaje to samo pozycjonowanie.
- Zhalucynowane cytaty: jeden fałszywy wyrok w pismie kończy relację.
- Serwis sprzętu na miejscu nie skaluje się dla firmy 1-3 osobowej.
- Polskie rozumowanie prawnicze lokalnych modeli 11B-30B może być zbyt słabe do pisania szkiców; zostawić je przy ekstrakcji i wyszukiwaniu.
- Długi cykl sprzedaży ze wspólnikami, którzy rzadko kupują oprogramowanie.

**Kiedy przerwać.** Przerwać, jeśli mniej niż 3 z 10 kancelarii pilotażowych przejdzie na płatne w ciągu 4 miesięcy albo jeśli wydawca wypuści AI on-prem w ramach swojej subskrypcji.

**Źródła:** [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Gaius-Lex](https://gaius-lex.pl/) · [Gaius-Lex pricing](https://gaius-lex.pl/cennik) · [KIRP AI search](https://kirp.pl/?s=sztuczna+inteligencja) · [Harvey](https://www.harvey.ai/) · [Legora](https://legora.com/) · [SAOS API](https://www.saos.org.pl/help/index.php/dokumentacja-api) · [Bielik-11B-v3.0-Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct)

---

## 7. Agent back-office'u spedycyjnego dla polskich małych spedytorów

**Region:** PL (potem UE) · **Kupujący:** mali i średni polscy spedytorzy, przewoźnicy z działem spedycji, agencje celne · **Model przychodu:** subskrypcja za stanowisko + opłata za przetworzone zlecenie lub zgłoszenie · **Konkurencja:** średnia · **Dopasowanie modeli lokalnych:** średnie · **Wynik: 67** (M16 G14 C8 L10 F10 R9)

> Polska to największy przewoźnik drogowy w UE, a jej działy spedycji wciąż przepisują maile do TMS i formularzy celnych; pieniądze są realne, ale Digicust, Raft i Trans.eu już wchodzą na ten rynek, więc wygrywać trzeba na małych polskich stanowiskach i polskojęzycznej poczcie.

**Asymetria.** Polska przewiozła 20,2% całego unijnego drogowego transportu towarowego w tonokilometrach w 2025 roku, przed Niemcami (14,7%) i Hiszpanią (14,5%) (Eurostat, 07.2026). Polskie firmy należą do najwolniej wdrażających AI: 8,36% przedsiębiorstw używało AI w 2025 wobec 19,95% w UE, a w całej UE tylko 17% małych firm (Eurostat, 12.2025). Spedytorzy dostają zlecenia jako maile w wolnym tekście i PDF-y po polsku, niemiecku, angielsku i ukraińsku, przepisują je do TMS, budują dokumenty CMR, sprawdzają przewoźników na giełdach, a dla odcinków spoza UE przygotowują zgłoszenia celne. Sama Trans.eu reklamuje ograniczenie ręcznej obsługi zleceń „nawet o 75%” *(deklaracja dostawcy)*, co potwierdza ręczny punkt wyjścia. Luka pozostaje otwarta w długim ogonie spedytorów z 1-20 osobami, których nie stać na narzędzia klasy enterprise.

**Kto płaci i ile.** Liczba polskich spedytorów i agencji celnych: nie znaleziono w tym przebiegu (nie pobrano liczb z rejestru GUS). Dzisiejsze wydatki: pensje dyspozytorów i pracowników celnych; klient Digicust, ZLS, podaje spadek czasu zgłoszenia z 3-4 godzin do 10-15 minut *(deklaracja dostawcy)*, co pokazuje skalę kosztu ręcznej pracy. Cena, którą zaakceptuje spedytor z 5 stanowiskami: zakładam 300-800 PLN za stanowisko miesięcznie lub 2-5 PLN za przetworzone zlecenie (moja hipoteza). Kanał: dostawcy TMS, ekosystem Trans.eu (API), stowarzyszenia spedycyjne, grupy dyspozytorów na LinkedIn.

**Aplikacja agentowa.**
1. Pobranie: wspólna skrzynka ze zleceniami, PDF-y, eksporty z WhatsAppa, potwierdzenia stawek.
2. Ekstrakcja: miejsca załadunku i rozładunku, daty, towar, waga, ADR, cena, numery referencyjne; normalizacja adresów.
3. Wnioskowanie: dopasowanie do klienta, sprawdzenie przewoźnika (status VAT, licencja, ubezpieczenie, ocena na giełdzie), oznaczanie sygnałów oszustwa (nowa domena, zmieniony rachunek bankowy).
4. Szkic: zlecenie w TMS, zlecenie dla przewoźnika, dane do CMR, dane zgłoszenia celnego z propozycją kodu HS.
5. Weryfikacja: kontrole regułowe plus drugi przebieg modelu na liczbach; **bramka ludzka** dla ceny, wyboru przewoźnika, danych bankowych i każdego zgłoszenia celnego (skutek prawny).
6. Działanie: wysłanie do TMS i na giełdę przez API; zgłaszający składa w PUESC.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| Ekstrakcja z maili i PDF-ów | tak | zapas dla trudnych skanów | wolumen jest wysoki, liczy się koszt za zlecenie |
| Normalizacja wielojęzyczna (PL, DE, EN, UA) | tak | nie | modele otwarte radzą sobie z tymi językami wystarczająco dobrze |
| Wnioskowanie o oszustwach przewoźników | tak | opcjonalnie | wymaga historii klienta, zostaje lokalnie |
| Propozycja kodu HS | częściowo | tak | trudne wnioskowanie, niski wolumen, nie trzeba danych osobowych |
| Dane zgłoszenia celnego | tak | nie | dane klienta i ceny, RODO i tajemnice handlowe |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
|---|---|---|---|---|---|
| Trans.eu | obecny gracz | PL / UE | giełda frachtów i TMS; przydział frachtów „Powered by AI”; 25 000 aktywnych przewoźników spot | AI w przydziale i sprawdzaniu przewoźników *(deklaracja dostawcy)* | tylko demo, niepubliczna |
| TIMOCOM | obecny gracz | DE / UE | giełda frachtów, śledzenie, komunikator, API | na stronie głównej nie opisano funkcji AI (10.2026) | niepubliczna |
| Digicust | startup | AT / UE | zgłoszenia celne z AI, klasyfikacja taryfowa, triaż maili; podaje obsługę Polski; 100+ firm produkcyjnie | wysoka *(deklaracja dostawcy)* | niepubliczna |
| Raft | startup | UK / globalnie | agentowa AI dla spedytorów i agentów celnych, przyjmowanie maili, AP; „do 93% dokumentacji celnej” | wysoka *(deklaracja dostawcy)* | niepubliczna |
| Polskie agencje celne | obecny gracz | PL | ręczne zgłoszenia jako usługa | niska | za zgłoszenie, nie znaleziono |

Luką jest małe polskie stanowisko: Digicust i Raft sprzedają większym agentom z integracjami ERP; Trans.eu automatyzuje wewnątrz własnej giełdy. Na początku unikać konkurowania na odprawie celnej; zacząć od „mail do zlecenia” i weryfikacji przewoźników oraz zintegrować się z Trans.eu zamiast z nim walczyć.

**Kontra z pięciu stron.**
- **Klient:** mali spedytorzy są wrażliwi na cenę i lojalni wobec swojego TMS; kupią tylko to, co oszczędza czas dyspozytora już w pierwszym tygodniu.
- **Obecny gracz:** Trans.eu już oferuje przydział z AI i może dodać przyjmowanie maili; ma klientów i dane o przewoźnikach.
- **Czołowe laboratoria i big tech:** ogólny asystent pocztowy dobrze wyciąga zlecenia; wartość leży w integracji z TMS i giełdą, a nie w ekstrakcji.
- **Regulator:** zgłoszenia celne mają skutek prawny i grożą za nie kary; zgłaszającym musi pozostać człowiek; AI Act nie klasyfikuje tego jako wysokiego ryzyka.
- **Ekonomia jednostkowa:** niska cena za stanowisko; praca integracyjna przy każdym TMS może zjeść marżę.

**Po kontrze.** Przetrwa jako wąskie narzędzie „mail ze zleceniem do TMS + kontrola oszustw przewoźnika” dla polskich spedytorów z 1-20 osobami, zintegrowane z dwoma-trzema najczęściej używanymi TMS. Odprawa celna później lub przez partnerstwo. C zostaje 8.

**Liczby.**
- Polska 20,2% unijnych tkm drogowych w 2025, miejsce 1 (Eurostat, 07.2026).
- Użycie AI: PL 8,36%, UE 19,95% przedsiębiorstw w 2025 (Eurostat, 12.2025).
- Trans.eu: 25 000 aktywnych przewoźników spot, „do 75%” mniej ręcznej obsługi zleceń *(deklaracja dostawcy, odczyt 10.2026)*.
- Digicust: 100+ firm produkcyjnie, 70-90% automatyzacji zgłoszeń, ZLS z 3-4 h do 10-15 min *(deklaracja dostawcy, odczyt 10.2026)*.
- Raft: 5 mln+ przesyłek rocznie, do 93% dokumentacji celnej zautomatyzowane *(deklaracja dostawcy, odczyt 10.2026)*.
- Liczba polskich firm spedycyjnych: nie znaleziono.

**Jak zacząć.**
1. Tygodnie 1-3: zebrać 300 zanonimizowanych maili ze zleceniami od 2 przyjaznych spedytorów; zbudować ekstraktor na lokalnym stanowisku.
2. Tygodnie 3-6: wysyłanie do TMS dla jednego popularnego polskiego TMS plus sprawdzenie przewoźnika (biała lista VAT, ocena na giełdzie).
3. Tygodnie 6-8: sygnały oszustw i codzienny dashboard; mierzyć minuty zaoszczędzone na zleceniu.
4. Pierwszych 10 klientów: społeczności dyspozytorów, targi spedycyjne, jeden partner TMS.
5. Test cenowy: 399 PLN za stanowisko miesięcznie vs 3 PLN za zlecenie.

**Ryzyka i ograniczenia.**
- Trans.eu lub dostawca TMS włączy tę samą funkcję za darmo.
- Nakład integracyjny na każdy TMS; mali dostawcy mają słabe API.
- Błędna ekstrakcja daty lub ceny powoduje realny koszt; bramka ludzka jest obowiązkowa.
- Spowolnienia na rynku frachtów tną budżety na oprogramowanie jako pierwsze.

**Kiedy przerwać.** Przerwać, jeśli pilotaże oszczędzają poniżej 3 minut na zleceniu lub żaden TMS nie udostępnia API do 4. miesiąca.

**Źródła:** [Eurostat road freight](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Road_freight_transport_statistics) · [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Trans.eu enterprise](https://enterprise.trans.eu/en/) · [TIMOCOM](https://www.timocom.co.uk/) · [Digicust](https://www.digicust.com/en) · [Raft](https://www.raft.ai/)

---

## 8. Agent wiedzy o utrzymaniu ruchu i serwisie terenowym on-prem dla przemysłowych MŚP w Europie Środkowo-Wschodniej

**Region:** PL / UE (CEE) · **Kupujący:** kierownicy utrzymania ruchu i dyrektorzy serwisu w średnich zakładach produkcyjnych, u producentów maszyn, w wodociągach i ciepłowniach · **Model przychodu:** opłata wdrożeniowa + roczna licencja na urządzenie on-prem, wyceniana za lokalizację · **Konkurencja:** średnia · **Dopasowanie modeli lokalnych:** wysokie · **Wynik: 66** (M13 G16 C10 L13 F9 R5)

> Realna luka w przemysłowych MŚP z Europy Środkowo-Wschodniej, które nie wyślą rysunków i dzienników serwisowych do chmury, ale duże platformy (Microsoft, Siemens, Aquant) schodzą w dół rynku, a przygotowanie danych jest najtrudniejsze.

**Asymetria.** Polskie przedsiębiorstwa używały AI w 8,36% w 2025 roku wobec 19,95% w UE, a małe firmy w całej UE w 17% (Eurostat, 2025). Wiedza o utrzymaniu ruchu leży w instrukcjach PDF (często po niemiecku lub angielsku), papierowych albo excelowych dziennikach serwisowych i w głowach starszych techników. Siemens pokazuje kierunek za pomocą czatbota Industrial Copilot do zadań utrzymaniowych we własnej fabryce w Erlangen, a Aquant sprzedaje dużym producentom OEM (Makino, Terex, JLG, Stryker), ale żaden z nich nie celuje w 200-osobowy polski zakład z maszynami mieszanych marek. Luka istnieje z powodu rozdziału IT/OT na hali, lokalizacji offline, mieszanych języków i konserwatywnych kupujących; w segmencie MŚP może pozostać otwarta 2-3 lata.

**Kto płaci i ile.** Liczba MŚP produkcyjnych w PL i UE z zespołem utrzymania ruchu: nie znaleziono w źródle odczytanym w tej sesji. Ile płacą dziś: czas techników spędzony na szukaniu w instrukcjach i dzwonieniu do OEM oraz koszt przestojów; żadnej z tych liczb nie znaleziono dla PL. Punkt odniesienia: Microsoft Dynamics 365 Field Service kosztuje 105 USD za użytkownika miesięcznie przed kredytami Copilota (10.2026), czego mały zakład często w ogóle nie kupuje. Ceny do przetestowania: 5000-10 000 EUR opłaty wdrożeniowej plus 500-1500 EUR miesięcznie za lokalizację. Kanał: targi utrzymania ruchu, resellerzy systemów CMMS, dystrybutorzy obrabiarek.

**Aplikacja agentowa.**
1. Pobranie: instrukcje, schematy elektryczne, eksporty z CMMS, dzienniki serwisowe, listy części zamiennych z zasobu plikowego na urządzenie w sieci zakładu.
2. Ekstrakcja: OCR, wyciąganie tabel i numerów części, powiązanie kodów usterek z maszynami i częściami.
3. Wnioskowanie: technik pyta po polsku („prasa 3, alarm E-214, co dalej”); agent wyszukuje strony instrukcji, wcześniejsze naprawy tej samej maszyny, dostępność części.
4. Szkic: procedura krok po kroku z odwołaniami do strony instrukcji i wcześniejszego zlecenia pracy.
5. Weryfikacja: kroki istotne dla bezpieczeństwa (blokowanie i oznakowanie – lockout/tagout, prace elektryczne) są oznaczane i nigdy skracane; odpowiedzi bez przytoczonego źródła są odrzucane.
6. Działanie: szkic zlecenia pracy lub zapotrzebowania na część zamienną tworzony w CMMS dopiero po zatwierdzeniu przez kierownika utrzymania ruchu.

**Podział lokalny i płatny.**
| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
| --- | --- | --- | --- |
| OCR i ekstrakcja | Tak | Nie | Rysunki i instrukcje są poufne, a wolumen duży |
| Pytania i odpowiedzi techników po polsku | Tak (Bielik 11B v3 lub model wielojęzyczny) | Nie | Sieć zakładowa często nie ma internetu, potrzebne małe opóźnienie |
| Tłumaczenie niemieckich lub angielskich instrukcji | Tak | Opcjonalnie dla trudnych dokumentów | Koszt wolumenu i tajemnica |
| Analiza wzorców usterek w dziennikach | Tak | Opcjonalnie na zanonimizowanych agregatach | Dzienniki ujawniają wolumeny produkcji |
| Konfiguracja produktu i inżynieria promptów | Nie | Tak | Praca po stronie dewelopera, bez danych klienta |

**Konkurencja.**
| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
| --- | --- | --- | --- | --- | --- |
| Siemens Industrial Copilot | obecny gracz | globalnie | Czatbot wspierający zadania utrzymaniowe, zbudowany z Microsoftem | Głęboka w ekosystemie Siemensa | Niepubliczna |
| Aquant | startup | USA / globalnie | Konwersacyjne AI serwisowe ze studiem agentów dla producentów sprzętu | Głęboka | Niepubliczna, bezpłatny okres próbny |
| Microsoft Dynamics 365 Field Service | platforma globalna | globalnie | Zarządzanie serwisem terenowym z Copilotem, przewodnikami i zdalną pomocą | Średnia | 105 USD za użytkownika miesięcznie plus kredyty Copilota |
| Dostawcy CMMS (lokalni polscy i unijni) | obecny gracz | PL / UE | Zlecenia pracy i rejestry aktywów, dodatki AI bardzo różne | Niska | Nie znaleziono |

Luka: neutralność wobec dostawców, zakłady z maszynami mieszanych marek, on-prem i offline, interfejs technika po polsku. Pokonać platformy wdrożeniem (jedno urządzenie, bez chmury) i przygotowaniem danych wykonanym za klienta.

**Kontra z pięciu stron.**
- **Klient:** Kierownicy zakładów finansują to, co skraca przestoje, a nie to, co „porządkuje wiedzę”; dowód wymaga zmierzonego przed/po na jednej linii, co trwa miesiące.
- **Obecny gracz:** Dostawcy CMMS i OEM dodadzą czat z wyszukiwaniem na własnych danych; agent wygrywa tylko w obrębie marek i dokumentów, których oni nie posiadają.
- **Czołowe laboratoria i big tech:** Microsoft Copilot nad SharePointem już odpowiada na pytania o instrukcje w firmach na Microsoft 365; zostaje segment on-prem i offline.
- **Regulator:** Unijne rozporządzenie maszynowe i przepisy bezpieczeństwa sprawiają, że błędna rada serwisowa to odpowiedzialność; agent musi cytować i nie może wymyślać kroków bezpieczeństwa.
- **Ekonomia jednostkowa:** Każdy zakład ma bałaganiarskie, skanowane, wielojęzyczne dokumenty; nakład na wdrożenie może przekroczyć licencję pierwszego roku.

**Po kontrze.** Przetrwa jako wąski produkt: „dziennik serwisowy plus wyszukiwanie w instrukcjach” dla jednej klasy maszyn (na przykład wtryskarki lub CNC), gdzie dokumenty są do siebie podobne, sprzedawany ze stałym wdrożeniem. Trwałość to najsłabszy wynik.

**Liczby.**
- Użycie AI w Polsce 8,36% przedsiębiorstw wobec 19,95% w UE (Eurostat, dane za 2025).
- Małe przedsiębiorstwa UE 17%, średnie 30,36% używających AI (Eurostat, dane za 2025).
- Dynamics 365 Field Service 105 USD za użytkownika miesięcznie, plan dla kontraktorów 50 USD (strona z cennikiem Microsoftu, odczytana 14.10.2026) *(cena dostawcy)*.
- Klienci Aquant to m.in. Makino, Terex, JLG, Stryker, Siemens *(deklaracja dostawcy, strona internetowa odczytana 14.10.2026)*.
- Liczba polskich MŚP produkcyjnych z zespołami utrzymania ruchu: nie znaleziono.

**Jak zacząć.**
1. Tygodnie 1-4: RAG z cytowaniami nad publicznym zestawem instrukcji maszyn plus syntetycznymi dziennikami serwisowymi; polski interfejs czatu.
2. Tygodnie 5-8: pilotaż w jednym zakładzie z jedną klasą maszyn, z mierzonym czasem do uzyskania odpowiedzi przez techników.
3. Pierwszych 10 klientów: przez dystrybutorów maszyn i stowarzyszenia utrzymania ruchu; zaoferować 3 pilotaże z rabatem w zamian za studia przypadków.
4. Test cenowy: samo wdrożenie vs wdrożenie plus miesięczna licencja; obserwować, które się zamyka.

**Ryzyka i ograniczenia.**
- Przygotowanie dokumentów jest ręczne i powolne; może przerodzić się w konsulting.
- Odpowiedzialność za bezpieczeństwo przy błędnych instrukcjach serwisowych.
- Cykl sprzedaży w produkcji jest długi i sezonowy.
- Silne lokalne relacje mają znaczenie; nowemu graczowi brakuje wiarygodności w przemyśle.

**Kiedy przerwać.** Przerwać, jeśli dwa pilotaże nie wykażą mierzalnej oszczędności czasu potwierdzonej przez techników albo wdrożenie w jednym zakładzie przekracza 30 dni.

**Źródła:** [Eurostat: Use of AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Siemens Industrial Copilot](https://www.siemens.com/global/en/products/automation/topic-areas/industrial-ai/industrial-copilot.html) · [Aquant](https://www.aquant.ai/) · [Dynamics 365 Field Service pricing](https://www.microsoft.com/en-us/dynamics-365/products/field-service/pricing) · [SpeakLeash Bielik models](https://huggingface.co/speakleash)

---

## 9. Agent back-office KSeF dla polskich biur rachunkowych

**Region:** PL · **Kupujący:** biura rachunkowe, 2-30 osób · **Model przychodu:** opłata wdrożeniowa + miesięczna licencja za każdy obsługiwany podmiot klienta · **Konkurencja:** wysoka · **Dopasowanie modeli lokalnych:** wysokie · **Wynik: 65** (M16 G12 C6 L12 F11 R8)

> Okazja prawdziwa, ale zatłoczona: wygrać można tylko jako dodatkowa warstwa agentowa na istniejącym oprogramowaniu księgowym biura, sprzedawana najpierw lokalnie, nigdy jako nowy system księgowy.

**Asymetria.** KSeF 2.0 stał się jedynym kanałem e-faktur 1.02.2026 dla dużych firm i wszystkich odbiorców faktur, od 1.04.2026 jest obowiązkowy dla większości wystawców, a dla najmniejszych firm (do 10 000 PLN sprzedaży miesięcznie) od 1.01.2027 (ksef.podatki.gov.pl, pobrano 10.2026). Strukturalne faktury XML eliminują krok OCR, ale praca, która zostaje w biurze, nadal jest ręczna: przypisywanie kategorii kosztów, traktowanie VAT, dopasowanie do pozycji bankowych, ściganie brakujących dokumentów, które nie są fakturami KSeF (faktury zagraniczne, paragony paliwowe, umowy), oraz odpowiadanie na pytania klientów telefonicznie i mailowo. Polska jest późnym adopterem AI: 8,36% polskich przedsiębiorstw używało AI w 2025 roku wobec 19,95% w UE (Eurostat, dane za 2025). Luka pozostaje otwarta, dopóki obecni gracze dodają funkcje do własnych pakietów po jednym module; szacuję, że mają 1-2 lata do wprowadzenia księgowania na poziomie agenta (moje oszacowanie, nie pomiar).

**Kto płaci i ile.** Liczby biur rachunkowych w Polsce nie znaleziono w tym przebiegu (tabel GUS PKD 69.20 nie pobrano). Biura zwykle pobierają od klienta miesięczny ryczałt; cen nie zweryfikowano w tym przebiegu. Za oprogramowanie biura już płacą (cenniki dostawców, pobrano 14.10.2026): wFirma 24 PLN netto za klienta miesięcznie za pełny system biurowy, z promocją 2026 na rok za darmo dla biura i 10 klientów; pakiety biurowe SaldeoSMART 289, 409 i 789 PLN netto miesięcznie. Kupujący zaakceptuje narzędzie kosztujące ułamek miesięcznej pensji jednego młodszego księgowego, jeśli zwolni moce na obsługę większej liczby klientów. Cena testowa: 300-1000 PLN za biuro miesięcznie plus 5-15 PLN za podmiot klienta (hipoteza do przetestowania, nie dane rynkowe). Kanały: regionalne stowarzyszenia księgowych, grupy biur rachunkowych na Facebooku, programy partnerskie dostawców oprogramowania księgowego.

**Aplikacja agentowa.**
1. Pobranie: faktury KSeF (XML) każdego klienta przez token API KSeF, wyciągi bankowe (MT940/CSV) i dokumenty spoza KSeF przesyłane e-mailem.
2. Ekstrakcja: XML z KSeF parsowany bezpośrednio; OCR plus ekstrakcja modelem tylko dla dokumentów spoza KSeF.
3. Rozumowanie: propozycja konta, kategorii kosztów, kodu VAT i kolumny KPiR/księgi na podstawie historii klienta i reguł planu kont biura.
4. Szkic: propozycja księgowania plus lista brakujących dokumentów i wiadomość do klienta po polsku.
5. Weryfikacja: kontrole regułowe (stawki VAT, sprawdzenie rachunku bankowego na białej liście, wykrywanie duplikatów), wskaźnik pewności dla każdej pozycji.
6. Działanie: bramka akceptacji przez człowieka, księgowy akceptuje lub poprawia; dopiero potem eksport do formatu importu Comarch Optima, Symfonia, enova365 lub Rachmistrz. Bez automatycznego składania JPK ani deklaracji.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| Parsowanie XML z KSeF | brak modelu, kod | brak | dane ustrukturyzowane, deterministyczne |
| Ekstrakcja z dokumentów spoza KSeF | klasa Qwen-VL lub Bielik 11B v3 (Apache 2.0) | tylko awaryjnie | dane finansowe klienta, koszt wolumenu |
| Propozycja księgowania | model lokalny z regułami biura w kontekście | tylko trudne przypadki, zanonimizowane | tajemnica zawodowa, RODO, stały wolumen |
| Szkice wiadomości do klientów po polsku | Bielik 11B v3 | brak | płynność w polskim wystarcza przy 11B |
| Projektowanie reguł i zbiory ewaluacyjne | brak | model z czołówki offline | praca jednorazowa, bez danych klientów |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
|---|---|---|---|---|---|
| SaldeoSMART (BrainShare) | obecny gracz | PL | obieg dokumentów, OCR, wyciągi bankowe, darmowe pobieranie i wysyłka KSeF, ponad 300 000 użytkowników *(deklaracja dostawcy)* | AI ustawia parametry, wymiary i typ dokumentu faktur KSeF *(deklaracja dostawcy)* | pakiety biurowe 289 / 409 / 789 PLN netto miesięcznie (10.2026) |
| Comarch ERP Optima / Betterfly | obecny gracz | PL | księga, KPiR, VAT, moduł biurowy, KSeF | nie zweryfikowano w tym przebiegu | nie znaleziono |
| Symfonia | obecny gracz | PL | księga i kadry dla MŚP i biur | nie zweryfikowano w tym przebiegu | nie znaleziono |
| enova365 (Soneta) | obecny gracz | PL | ERP, moduł biurowy | nie zweryfikowano w tym przebiegu | nie znaleziono |
| wFirma | obecny gracz | PL | internetowy system biurowy, księga, płace, nielimitowany KSeF i OCR, portal klienta | Magic Box do przetwarzania dokumentów, SMART Lista, cyfrowy asystent księgowy *(deklaracja dostawcy)* | 24 PLN netto za klienta miesięcznie (10.2026) |
| inFakt / Fakturownia | obecny gracz | PL | fakturowanie, księgowość online, darmowy KSeF, sprawdzanie białej listy VAT, dopasowanie płatności, OCR | inFakt: brak deklaracji AI na stronie KSeF; Fakturownia: integracja asystenta AI (MCP) we wszystkich planach *(deklaracja dostawcy)* | Fakturownia plan darmowy 3 faktury miesięcznie; księgowość online inFakt od 200 PLN miesięcznie (10.2026) |
| Rachmistrz / Rewizor (InsERT) | obecny gracz | PL | oprogramowanie desktopowe KPiR i księgi | nie zweryfikowano w tym przebiegu | nie znaleziono |

Luka: obecni gracze posiadają księgę i połączenie z KSeF, więc miejsce jest w warstwie osądu (klasyfikacja, brakujące dokumenty, odpowiedzi na pytania klientów), która obejmuje kilka ksiąg w jednym biurze; SaldeoSMART już typuje faktury KSeF z użyciem AI we własnym obiegu, więc klasyfikacja w obrębie jednego produktu nie jest już luką. Unikać czołowego starcia: integrować przez pliki importu, sprzedawać biurom korzystającym z dwóch lub więcej produktów księgowych.

**Kontra z pięciu stron.**
- **Klient:** biura są konserwatywne i odpowiadają za błędy; nie zaufają automatycznemu księgowaniu, dopóki nie wykaże dokładności na historii ich własnych klientów.
- **Obecny gracz:** Comarch, Saldeo i wFirma kontrolują ścieżkę danych i mogą dodać klasyfikację do swojego produktu przy zerowym krańcowym koszcie sprzedaży.
- **Czołowe laboratoria i big tech:** niskie bezpośrednie zagrożenie; nie budują polskich eksportów do ksiąg, ale ogólne copiloty obniżają postrzeganą wartość „AI”.
- **Regulator:** propozycje księgowań nie zmieniają odpowiedzialności prawnej (biuro podpisuje); potrzebne umowy powierzenia przetwarzania danych (RODO) i zapisy o tajemnicy zawodowej; tokeny KSeF to wrażliwe dane uwierzytelniające.
- **Ekonomia jednostkowa:** lokalna inferencja na urządzeniu w biurze jest tania przy dużym wolumenie; kosztem jest wsparcie integracji dla każdego produktu księgowego.

**Po kontrze.** Przetrwa jako wąski, lokalny asystent księgowania i brakujących dokumentów dla biur z wieloma księgami; cena za podmiot klienta, która musi być wyraźnie poniżej 24 PLN wFirmy za klienta za cały system biurowy; wynik spada do 65 (C6), bo SaldeoSMART już oferuje klasyfikację faktur KSeF z użyciem AI.

**Liczby.**
- KSeF 2.0: 1.02.2026 duże firmy i odbiorcy, 1.04.2026 większość wystawców, 1.01.2027 mali wystawcy do 10 tys. PLN miesięcznie (ksef.podatki.gov.pl, pobrano 14.10.2026).
- Wykorzystanie AI: 8,36% polskich przedsiębiorstw wobec 19,95% w UE, małe przedsiębiorstwa 17% w całej UE (Eurostat, dane za 2025).
- Działalność profesjonalna, naukowa i techniczna: 40,43% wykorzystania AI w całej UE (Eurostat, dane za 2025), więc polskie biura są w tyle za unijnymi odpowiednikami *(szacunek zewnętrzny trendu, podziału sektorowego dla PL nie znaleziono)*.
- Liczba polskich biur rachunkowych i niedobór księgowych: nie znaleziono w tym przebiegu (sprawdzono GUS, KIDP i strony wyników wyszukiwania, 14.10.2026).
- Plan biurowy wFirma: 24 PLN netto za klienta miesięcznie, nielimitowany KSeF i OCR (wfirma.pl, pobrano 14.10.2026, cennik dostawcy).
- SaldeoSMART: pakiety biurowe 289 / 409 / 789 PLN netto miesięcznie, KSeF za 0 PLN, typowanie faktur KSeF z użyciem AI, ponad 300 000 użytkowników i 6300-7000 firm i biur (dwie liczby na tej samej stronie) (saldeosmart.pl, pobrano 14.10.2026, *(deklaracja dostawcy)*).

**Jak zacząć.**
1. Tygodnie 1-4: czytnik API KSeF plus propozycja księgowania dla jednej księgi (import Comarch Optima), testowane na zanonimizowanej historii jednego życzliwego biura.
2. Tygodnie 5-8: ściągacz brakujących dokumentów i szkice wiadomości do klientów po polsku; raport dokładności dla każdego klienta.
3. Pierwszych 10 klientów: biura w jednym mieście przez lokalne stowarzyszenie księgowych; darmowy 60-dniowy pilotaż na 20 klientach każde.
4. Test cen: ryczałt za biuro vs opłata za podmiot, oferowane na przemian kolejnym potencjalnym klientom.

**Ryzyka i ograniczenia.**
- Obecny gracz wprowadza tę samą funkcję do księgi.
- Dokładność poniżej poziomu, jakiego biura potrzebują do księgowania bez nadzoru; wartość sprowadza się wtedy do sugestii.
- Obciążenie wsparciem integracji w różnych wersjach ksiąg.
- Roszczenia odszkodowawcze, jeśli błędny kod VAT przejdzie przez bramkę człowieka.

**Kiedy przerwać.** Przerwać, jeśli po 3 miesiącach płaci mniej niż 3 biura lub akceptacja księgowań pozostaje poniżej 80% pozycji.

**Źródła:** [Etapy KSeF](https://ksef.podatki.gov.pl/etapy-wdrozenia-ksef/) · [Eurostat wykorzystanie AI w przedsiębiorstwach](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [SaldeoSMART](https://www.saldeosmart.pl) · [Bielik 11B v3 Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [wFirma](https://wfirma.pl) · [Ceny wFirma dla biur](https://wfirma.pl/cennik-dla-biur-rachunkowych) · [Ceny SaldeoSMART dla biur](https://www.saldeosmart.pl/cennik/biuro) · [inFakt KSeF](https://www.infakt.pl/ksef) · [Ceny Fakturowni](https://fakturownia.pl/cennik)

---

## 10. Agent do należności i dokumentów EPU dla polskich MŚP

**Region:** PL · **Kupujący:** MŚP z fakturami B2B (hurt, podwykonawcy budowlani, usługi) oraz obsługujące je biura rachunkowe · **Model przychodu:** miesięczna subskrypcja za firmę + opłata za sprawę przy pozwach sądowych · **Konkurencja:** średnia · **Dopasowanie modeli lokalnych:** średnie · **Wynik: 64** (M13 G13 C8 L9 F12 R9)

> Warto przetestować jako agenta „przed windykatorem”, który czyta dane z KSeF i banku, wysyła stopniowane przypomnienia i przygotowuje pozew EPU do złożenia przez człowieka, wyceniony poniżej 8% prowizji od sukcesu internetowych windykatorów.

**Asymetria.** Ściganie zaległych faktur w małych firmach to nadal ręczna mieszanka telefonów, szablonów e-maili i papierowych wezwań do zapłaty, a polskie firmy są późnymi adopterami AI: 8,36% polskich przedsiębiorstw używało AI w 2025 roku wobec 19,95% w UE, a w całej UE tylko 17% małych firm wobec 55% dużych (Eurostat, dane za 2025). Kanał państwowy jest już cyfrowy: elektroniczne postępowanie upominawcze (EPU, e-sad.gov.pl) obsłużyło od 2010 roku 33 407 345 spraw i ma około 373 160 użytkowników, z czego 341 882 to konta indywidualne, a 16 916 to profesjonalni pełnomocnicy, z API dla masowych powodów (gov.pl, strona EPU 3.0, pobrano 10.2026). Większość MŚP więc sama składa pozwy albo płaci windykatorowi. KSeF (obowiązkowy dla większości wystawców od 1.04.2026) nadaje każdej fakturze ustrukturyzowany, czytelny maszynowo zapis, co czyni wykrywanie przeterminowań trywialnym dla każdego narzędzia z dostępem do odczytu. Luka: istniejące usługi automatyzują szablony i stały workflow, a nie osąd (do którego dłużnika zadzwonić, co powiedzieć, kiedy eskalować).

**Kto płaci i ile.** Liczby MŚP z chronicznie przeterminowanymi fakturami B2B nie znaleziono w tym przebiegu. BIG InfoMonitor posiada 113,5 mln informacji o zadłużeniu (BIG, 02.2026, *(deklaracja dostawcy)*). Cena referencyjna: Vindicat pobiera 8% odzyskanej kwoty albo subskrypcję od 169 PLN miesięcznie za automatyczne przypomnienia SMS i e-mail, wezwania do zapłaty z odsetkami i automatyczny wpis do BIG InfoMonitor (strony dostawcy, pobrano 14.10.2026). Cena testowa: 99-299 PLN miesięcznie za firmę za przypomnienia i szkice pozwów, plus stała opłata za każdy przygotowany pozew EPU (hipoteza). Kanał: biura rachunkowe jako resellerzy, bo już widzą należności swoich klientów.

**Aplikacja agentowa.**
1. Pobranie: faktury sprzedaży z KSeF, wyciągi bankowe, historia płatności każdego dłużnika.
2. Ekstrakcja: lista przeterminowań, wpłaty częściowe, spory znalezione w wątkach e-mail.
3. Rozumowanie: scoring ryzyka dłużnika z historii płatności plus sprawdzenia KRD i BIG (przez ich płatne API lub ręczne sprawdzenie), wybór tonu i kolejnego kroku.
4. Szkic: sekwencja przypomnień po polsku, formalne wezwanie do zapłaty, obliczenie odsetek oraz szkic pozwu EPU z listą dowodów.
5. Weryfikacja: kwoty, daty i odsetki sprawdzane kodem; kontrola terminu przedawnienia.
6. Działanie: bramka akceptacji przez człowieka przed każdym formalnym wezwaniem, każdym wpisem do rejestru (KRD/BIG) i każdym złożeniem EPU; składa właściciel lub prawnik.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| Wykrywanie przeterminowań i odsetki | brak modelu, kod | brak | deterministyczne |
| Czytanie sporów w e-mailach | Bielik 11B v3 lub klasa Qwen | brak | dane osobowe dłużnika objęte RODO |
| Szkice przypomnień i wezwań po polsku | Bielik 11B v3 | brak | szablony plus ton, jakość polskiego wystarcza |
| Uzasadnienie pozwu EPU | najpierw model lokalny | model z czołówki dla trudnych sporów, zanonimizowane | jakość sformułowań prawnych |
| Sprawdzenia w rejestrach dłużników | brak | płatna usługa KRD lub BIG | dane, które mają tylko oni |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
|---|---|---|---|---|---|
| KRD (Krajowy Rejestr Długów) | obecny gracz | PL | sprawdzanie kontrahentów, wpis dłużnika, windykacja przez Grupę Kaczmarski, RiskRadar, faktoring NFG | nie pokazano na stronie głównej | nie znaleziono |
| BIG InfoMonitor | obecny gracz | PL | sprawdzanie firm i konsumentów, wpis dłużnika, powiadomienia o płatnościach, monitoring | nie pokazano na stronie głównej | nie znaleziono na stronie głównej |
| Vindicat.pl | startup | PL | automatyczne przypomnienia SMS i e-mail, wezwania z odsetkami, pozwy, negocjacje online, giełda długów, automatyczny wpis do BIG, ponad 20 000 firm *(deklaracja dostawcy)* | „inteligentny robot windykacyjny” *(deklaracja dostawcy)*, workflow regułowy, nie pokazano LLM | 8% odzyskanej kwoty albo subskrypcja od 169 PLN miesięcznie (10.2026) |
| Kaczmarski Inkasso | obecny gracz | PL | agencja windykacji B2B, grupa KRD | nie zweryfikowano w tym przebiegu | nie znaleziono |
| Narzędzia do fakturowania (inFakt, Fakturownia, wFirma) | obecny gracz | PL | fakturowanie z KSeF; Fakturownia wysyła automatyczne przypomnienia o płatności w planach płatnych; inFakt dopasowuje transakcje bankowe do faktur | Fakturownia: integracja asystenta AI (MCP) *(deklaracja dostawcy)*; pozostałych nie zweryfikowano | Fakturownia plan darmowy 3 faktury miesięcznie, ceny płatnych niewidoczne (10.2026) |

Luka: windykatorzy i rejestry zarabiają na późnym, formalnym etapie; nikt znaleziony w tym przebiegu nie sprzedaje agenta, który pracuje na wczesnym etapie z osądem i przekazuje właścicielowi gotowy plik EPU. Unikać konkurowania z rejestrami; integrować je.

**Kontra z pięciu stron.**
- **Klient:** właściciele obawiają się zepsucia relacji z klientami; kontrola tonu i akceptacja muszą być widoczne.
- **Obecny gracz:** Vindicat lub aplikacje do fakturowania mogą szybko dodać szkicowanie przez LLM; KRD kontroluje aktywo rejestru.
- **Czołowe laboratoria i big tech:** ogólny asystent potrafi napisać wezwanie do zapłaty; fosą jest dostęp do danych (KSeF, bank) i polska procedura.
- **Regulator:** windykacja musi respektować ochronę konsumentów i RODO; pozostanie przy samym B2B i niezłożenie niczego bez akceptacji ogranicza ekspozycję; zasady i opłaty składania EPU zmieniają się wraz z EPU 3.0.
- **Ekonomia jednostkowa:** tani w uruchomieniu lokalnym; ryzyko odejścia klientów po wyczyszczeniu zaległości.

**Po kontrze.** Przetrwa jako agent wczesnego etapu tylko dla B2B, sprzedawany przez biura rachunkowe; ryczałt wygrywa z prowizją od sukcesu u klientów z regularnym wolumenem, ale subskrypcja Vindicat za 169 PLN i darmowe przypomnienia w narzędziach do fakturowania ograniczają cenę; wynik spada do 64 (C8).

**Liczby.**
- EPU: 33 407 345 spraw od 2010 roku, około 373 160 użytkowników (strona EPU gov.pl, pobrano 14.10.2026).
- BIG InfoMonitor: 113,5 mln rekordów o długach, 381,0 mln pobranych raportów od 2014 roku (big.pl, 02.2026, *(deklaracja dostawcy)*).
- Vindicat: 8% prowizji od sukcesu, 93% ugód polubownych, ponad 20 000 firm (vindicat.pl, pobrano 10.2026, *(deklaracja dostawcy)*); subskrypcja od 169 PLN miesięcznie (vindicat.pl/cennik, pobrano 14.10.2026, cennik dostawcy).
- Fakturownia: automatyczne przypomnienia o płatności w planach płatnych (fakturownia.pl/cennik, pobrano 14.10.2026).
- Inne polskie usługi windykacyjne widoczne w wynikach wyszukiwania (KRUK, INDOS, CollectIn): oferty i ceny nie zweryfikowane, 14.10.2026.
- Wykorzystanie AI: PL 8,36% wobec 19,95% przedsiębiorstw w UE (Eurostat, dane za 2025).

**Jak zacząć.**
1. Tygodnie 1-4: detektor przeterminowań z KSeF i banku plus polska sekwencja przypomnień dla jednej firmy pilotażowej.
2. Tygodnie 5-8: generator wezwania do zapłaty i szkicu pozwu EPU z kalkulatorem odsetek; przegląd szablonów przez prawnika.
3. Pierwszych 10 klientów: przez dwa biura rachunkowe odsprzedające usługę swoim klientom.
4. Test cen: stała opłata miesięczna vs 3% odzyskanej kwoty.

**Ryzyka i ograniczenia.**
- Szablony prawne wymagają akceptacji prawnika; błędy kosztują opłaty sądowe.
- API rejestrów są płatne i uwarunkowane umową.
- Wartość jest skoncentrowana na początku; retencja wymaga funkcji ciągłego monitoringu.
- Długi konsumenckie oznaczają surowsze zasady; pozostać przy B2B.

**Kiedy przerwać.** Przerwać, jeśli klienci pilotażowi nie odzyskają w ciągu 3 miesięcy co najmniej 2-krotności subskrypcji w zaległej gotówce.

**Źródła:** [EPU gov.pl](https://www.gov.pl/web/sprawiedliwosc/epu) · [Vindicat](https://vindicat.pl/) · [Ceny Vindicat](https://vindicat.pl/cennik) · [Ceny Fakturowni](https://fakturownia.pl/cennik) · [BIG InfoMonitor](https://www.big.pl/) · [KRD](https://krd.pl/) · [Etapy KSeF](https://ksef.podatki.gov.pl/etapy-wdrozenia-ksef/) · [Eurostat wykorzystanie AI](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

---

## 11. Agent dokumentacji technicznej CE dla małych producentów maszyn i wyrobów

**Region:** PL (potem UE) · **Kupujący:** polscy mali i średni producenci maszyn, urządzeń i wyrobów konsumenckich oraz ich zewnętrzni konsultanci CE · **Model przychodu:** za dokumentację techniczną + roczna subskrypcja za aktualizacje · **Konkurencja:** średnia · **Dopasowanie modeli lokalnych:** wysokie · **Wynik: 63** (M13 G13 C9 L12 F8 R8)

> Termin z rozporządzenia maszynowego (20.01.2027) zmusza każdego producenta maszyn do przebudowy dokumentacji technicznej, a projekty to tajemnice handlowe, które pasują do modelu on-prem; ryzykiem są odpowiedzialność oraz długie, wymagające ekspertów MVP.

**Asymetria.** Rozporządzenie (UE) 2023/1230 obowiązuje obligatoryjnie od 20 stycznia 2027; do tego czasu stosuje się dyrektywę maszynową 2006/42/WE (strona Komisji Europejskiej o maszynach, odczyt 10.2026). Dopuszcza ono cyfrowe instrukcje i deklaracje zgodności, więc dokumentację i tak trzeba przebudować. Rozporządzenie o ogólnym bezpieczeństwie produktów (GPSR) obowiązuje od 13 grudnia 2024, a rozporządzenie bateryjne (UE) 2023/1542 dodaje paszport baterii od lutego 2027 (daty z rozporządzeń na EUR-Lex; nie sprawdzano ponownie pod kątem zmian z 2026 roku w tym przebiegu). Polska: 8,36% przedsiębiorstw używało AI w 2025 wobec 19,95% w UE (Eurostat, 12.2025). Dokumentacje techniczne piszą inżynierowie i freelancerzy-konsultanci CE w Wordzie: ocena ryzyka wg EN ISO 12100, lista norm zharmonizowanych, instrukcje, deklaracja zgodności.

**Kto płaci i ile.** Liczba polskich małych producentów maszyn: nie znaleziono w tym przebiegu. Dzisiejsze wydatki: zewnętrzni konsultanci CE i czas inżynierów; nie znaleziono publicznego cennika. Cena, którą zaakceptuje producent z 20-200 osobami: zakładam 3000-10 000 PLN za dokumentację maszyny i subskrypcję aktualizacji (moja hipoteza). Kanał: konsultanci CE (white label), klastry branżowe, targi, szkolenia jednostek notyfikowanych.

**Aplikacja agentowa.**
1. Pobranie: BOM, metadane rysunków, zdjęcia, stara dokumentacja techniczna, deklaracje dostawców.
2. Ekstrakcja: zagrożenia, komponenty, źródła energii, funkcje bezpieczeństwa.
3. Wnioskowanie: mapowanie na zasadnicze wymagania z załącznika III do 2023/1230 i normy zharmonizowane; oznaczanie kategorii z załącznika I, które wymagają jednostki notyfikowanej.
4. Szkic: tabela oceny ryzyka, sekcje instrukcji obsługi, deklaracja zgodności UE, dane o bezpieczeństwie produktu wg GPSR.
5. Weryfikacja: każdy wymóg cytuje artykuł rozporządzenia lub punkt normy; **bramka ludzka**: odpowiedzialny inżynier producenta podpisuje deklarację (skutek prawny).
6. Działanie: eksport dokumentacji i dziennika zmian; śledzenie aktualizacji norm.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| Pobranie rysunków i BOM | tak | nie | projekty to tajemnice handlowe |
| Ekstrakcja zagrożeń | tak | nie | wolumen i poufność |
| Mapowanie wymagań | tak | opcjonalna druga opinia | tekst rozporządzenia jest publiczny, dane klienta nie |
| Redakcja instrukcji i deklaracji po PL, EN, DE | tak | nie | modele otwarte piszą w tych językach wystarczająco dobrze |
| Tworzenie szablonów ogólnych | nie | tak | bez danych klienta |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
|---|---|---|---|---|---|
| Safexpert (IBF Solutions) | obecny gracz | AT / UE | oprogramowanie do CE i oceny ryzyka dla producentów maszyn | niezweryfikowane (strona nie załadowała się w tym przebiegu) | nie znaleziono |
| TÜV SÜD / TÜV Rheinland | firma doradcza | globalnie | ocena zgodności, usługi jednostki notyfikowanej | ręcznie | wycena indywidualna |
| Intertek | firma doradcza | globalnie | badania i certyfikacja produktów | ręcznie | wycena indywidualna |
| Polskie Centrum Badań i Certyfikacji | firma doradcza | PL | certyfikacja i badania | ręcznie | wycena indywidualna |
| Freelancerzy-konsultanci CE | firma doradcza | PL | dokumentacje techniczne ręcznie | niska | nie znaleziono |

Nie znaleziono natywnego AI narzędzia do dokumentacji CE dla polskich małych firm, ale wyszukiwanie było płytkie (jedna strona dostawcy się nie załadowała); C traktować jako wstępne. Sprzedawać najpierw freelancerom-konsultantom: to oni są wąskim gardłem przed styczniem 2027.

**Kontra z pięciu stron.**
- **Klient:** wiele małych firm kopiuje zeszłoroczną dokumentację i liczy na szczęście; płacą dopiero, gdy zażąda tego klient lub inspektor.
- **Obecny gracz:** Safexpert i jednostki notyfikowane mogą dodać redakcję z AI; jednostki notyfikowane mają zaufanie.
- **Czołowe laboratoria i big tech:** modele ogólne dobrze redagują instrukcje; fosa to mapowanie norm i dowody, a teksty norm są płatne (licencje ograniczają to, co można osadzić).
- **Regulator:** odpowiedzialność zostaje przy producencie; błędna ocena ryzyka po wypadku to poważna sprawa; produkt nigdy nie może niczego podpisywać.
- **Ekonomia jednostkowa:** każdy typ maszyny wymaga przeglądu eksperta; sprzedaż konsultantom zostawia eksperta w pętli, ale ogranicza cenę.

**Po kontrze.** Przetrwa jako współpilot konsultanta działający on-prem, dla jednej niszy (np. maszyny do przetwórstwa spożywczego lub obróbki drewna). F i R zostają niskie z powodu głębi dziedziny i odpowiedzialności.

**Liczby.**
- Rozporządzenie maszynowe 2023/1230 obowiązkowo od 20.01.2027 (Komisja Europejska, odczyt 10.2026).
- PL 8,36% vs UE 19,95% przedsiębiorstw używających AI w 2025 (Eurostat, 12.2025).
- Liczba polskich małych producentów maszyn i ceny doradztwa CE: nie znaleziono.

**Jak zacząć.**
1. Tygodnie 1-4: partnerstwo z 2 konsultantami CE; przebudować 5 prawdziwych dokumentacji na lokalnym stanowisku.
2. Tygodnie 4-8: mapa wymagań dla jednej niszy maszyn, weryfikator cytowań, szkice instrukcji po PL/EN/DE.
3. Pierwszych 10 klientów: klienci konsultantów przed styczniem 2027.
4. Test cenowy: 2500 vs 6000 PLN za dokumentację.

**Ryzyka i ograniczenia.**
- Odpowiedzialność za produkt po wypadku; umowy muszą zostawiać inżyniera jako autora.
- Normy zharmonizowane są objęte prawem autorskim; koszt licencji.
- Długi przegląd eksperta przy każdej dokumentacji ogranicza skalę.
- Szczyt popytu wokół stycznia 2027.

**Kiedy przerwać.** Przerwać, jeśli konsultanci nie skrócą czasu pracy nad dokumentacją o połowę przy pierwszych 5 dokumentacjach.

**Źródła:** [EC machinery](https://single-market-economy.ec.europa.eu/sectors/mechanical-engineering/machinery_en) · [Regulation 2023/1230](https://eur-lex.europa.eu/eli/reg/2023/1230/oj) · [GPSR 2023/988](https://eur-lex.europa.eu/eli/reg/2023/988/oj) · [Battery Regulation 2023/1542](https://eur-lex.europa.eu/eli/reg/2023/1542/oj) · [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

---

## 12. Asystent kosztorysowy i przetargowy dla polskich wykonawców budowlanych

**Region:** PL · **Kupujący:** małe i średnie firmy generalnego wykonawstwa, instalatorzy, niezależni kosztorysanci · **Model przychodu:** subskrypcja za kosztorysanta + pakiety na przetarg · **Konkurencja:** średnia · **Dopasowanie modeli lokalnych:** średnie · **Wynik: 63** (M12 G15 C10 L8 F8 R10)

> Prawdziwa luka: globalne narzędzia AI do przedmiarów nie znają KNR ani polskich zasad przetargowych, a polscy dostawcy oprogramowania kosztorysowego nie pokazują widocznego AI.

**Asymetria.** Budownictwo to sektor o niskim wykorzystaniu AI: w 2025 roku AI stosowało 10,79% unijnych przedsiębiorstw budowlanych, czyli około połowy unijnej stawki dla wszystkich sektorów, 19,95% (Eurostat, 2025). Polska ogółem ma 8,36% (Eurostat, 2025). Kosztorysowanie w Polsce opiera się na katalogach norm KNR/KNNR i przepisach o zamówieniach publicznych, więc kosztorysanci nadal czytają rysunki, ręcznie budują przedmiar i wpisują pozycje do programów desktopowych. Globalne narzędzia AI do obmiarów (Togal, Kreo) mierzą rysunki, ale nie generują kosztorysów z kodami KNR. Luka trwa, dopóki obecni gracze utrzymują produkty desktopowe, a globalne narzędzia ignorują polskie normy.

**Kto płaci i ile.** Liczba polskich firm budowlanych i kosztorysantów: nie znaleziono w tym przebiegu (do sprawdzenia liczby z GUS REGON). Globalne punkty odniesienia cen: Togal 299 USD za użytkownika miesięcznie, Kreo Pro 175 USD za użytkownika miesięcznie (*ceny dostawców*, odczytano 14.10.2026). Ceny polskich licencji programów kosztorysowych desktopowych: nie znaleziono w tym przebiegu. Przetestować 300-900 PLN za kosztorysanta miesięcznie lub cenę za przetarg dla okazjonalnych oferentów. Kanał: fora kosztorysantów, firmy szkoleniowe, hurtownie budowlane.

**Aplikacja agentowa.**
1. Wczytanie: dokumentacja przetargowa (SIWZ/SWZ, opis robót, rysunki w PDF).
2. Ekstrakcja: pozycje zakresu, ilości z tekstu, obmiary z rysunków (model wizyjny).
3. Rozumowanie: przypisanie każdej pozycji do pozycji KNR z oceną pewności i alternatywami.
4. Redakcja: przedmiar i kosztorys eksportowane do formatu, który importuje program obecnego gracza.
5. Weryfikacja: porównanie z opisem robót; lista brakujących pozycji i ryzykownych założeń.
6. Działanie: **zatwierdzenie przez kosztorysanta** zanim cena trafi do oferty.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| Parsowanie dokumentów i OCR | Tak | Nie | Liczba stron, koszt |
| Obmiar z rysunków | Częściowo | Tak dla trudnych rysunków | Jakość wizji bywa różna |
| Mapowanie KNR | Tak, z wyszukiwaniem po katalogu | Opcjonalnie | Powtarzalne, duży wolumen |
| Przegląd ryzyk warunków przetargu | Nie | Tak | Lepsze rozumowanie, dane nie są tajne |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
|---|---|---|---|---|---|
| Norma PRO / EXPERT (Athenasoft) | obecny gracz | PL | Kosztorysowanie desktopowe na KNR | Nie znaleziono AI w tym przebiegu | nie znaleziono |
| Zuzia | obecny gracz | PL | Kosztorysowanie desktopowe | Nie znaleziono AI w tym przebiegu | nie znaleziono |
| Rodos | obecny gracz | PL | Kosztorysowanie desktopowe | Nie znaleziono AI w tym przebiegu | nie znaleziono |
| Togal.AI | startup | globalnie | Obmiar AI z rysunków, polecenia czatu | Wysoka dla obmiarów | 299 USD za użytkownika miesięcznie |
| Kreo | startup | globalnie | Obmiar, Auto Measure, Ask AI dla rysunków | Wysoka dla obmiarów | 35-175 USD za użytkownika miesięcznie |

Luka: nie znaleziono nikogo, kto łączyłby obmiar AI z kodowaniem KNR i polskim tekstem przetargowym. Nie walczyć z obecnymi graczami: eksportować do ich formatów.

**Kontra z pięciu stron.**
- **Klient:** kosztorysanci nie ufają automatycznym ilościom; jedna błędna pozycja kosztuje przetarg. Odpowiedź: pozycjonować jako kontrolera i pierwszy szkic, pokazywać każde źródło.
- **Obecny gracz:** Athenasoft i inni posiadają dane KNR i mogliby dodać AI; ich tempo jest nieznane.
- **Czołowe laboratoria i big tech:** ogólni asystenci potrafią czytać PDF-y przetargowe, ale nie wyceniają według KNR; niskie zagrożenie w ciągu 2 lat.
- **Regulator:** niskie; odpowiedzialność za ofertę pozostaje przy wykonawcy.
- **Ekonomia jednostkowa:** mały rynek, cykle budowlane wpływają na gotowość do płacenia; licencjonowanie katalogów KNR może kosztować.

**Po kontrze.** Przetrwa jako „czytnik przetargów + kontroler przedmiaru", który zasila programy obecnych graczy, a nie ich zastępuje. Potrzebuje kosztorysanta jako współzałożyciela lub doradcy. Wynik około 60.

**Liczby.**
- Wykorzystanie AI w budownictwie 10,79% wobec 19,95% dla wszystkich sektorów, UE 2025 (Eurostat, *statystyki oficjalne*).
- Polska: 8,36% przedsiębiorstw używa AI, 2025 (Eurostat).
- Togal Growth 299 USD za użytkownika miesięcznie (*cena dostawcy*, 14.10.2026).
- Kreo Lite 35 USD, Plus 70 USD, Pro 175 USD za użytkownika miesięcznie (*ceny dostawcy*, 14.10.2026).
- Liczba polskich kosztorysantów i ceny licencji: nie znaleziono.

**Jak zacząć.**
1. Tygodnie 1-3: przeprowadzić wywiady z 10 kosztorysantami; zebrać 5 dawnych przetargów z końcowymi kosztorysami.
2. Tygodnie 4-8: MVP, które czyta opis robót i wypluwa szkic przedmiaru z podpowiedziami KNR; zmierzyć trafność względem prawdziwych kosztorysów.
3. Pierwszych 10 klientów: niezależni kosztorysanci przez fora i LinkedIn, pierwszy przetarg za darmo.
4. Test ceny: za przetarg (100-300 PLN) vs miesięcznie.

**Ryzyka i ograniczenia.**
- Prawa do katalogów KNR i dostęp do danych.
- Jakość rysunków bywa różna; dokładność wizji dla polskich rysunków niesprawdzona.
- Czytelnikowi brakuje wiedzy dziedzinowej.
- Cykliczność nabywców.

**Kiedy przerwać.** Przerwać, jeśli po 8 tygodniach mapowanie KNR jest poprawne w mniej niż 70% na prawdziwych przetargach lub żaden kosztorysant nie zapłaci po darmowym okresie próbnym.

**Źródła:** [Eurostat: wykorzystanie AI w przedsiębiorstwach](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Togal: cennik](https://www.togal.ai/pricing) · [Kreo: cennik](https://www.kreo.net/pricing)

---

## 13. Lokalny polski skryba medyczny dla prywatnych klinik

**Region:** PL · **Kupujący:** prywatne kliniki, praktyki specjalistyczne, dentyści, ośrodki fizjoterapii i medycyny pracy · **Model przychodu:** opłata za lekarza miesięcznie + wdrożenie boxa na miejscu · **Konkurencja:** średnia · **Dopasowanie modeli lokalnych:** wysokie · **Wynik: 61** (M15 G13 C7 L12 F7 R7)

> Duży ból i wyraźny argument tajemnicy, ale Noa od Docplanner już sprzedaje polskim lekarzom notatki AI przez ZnanyLekarz, więc jedyny wolny pas to skrybowanie on-premise zintegrowane z EDM dla klinik, które odrzucają chmurę.

**Asymetria.** Polscy lekarze wpisują notatki z wizyt do EDM (elektronicznej dokumentacji medycznej, obowiązkowej w Polsce od 2021 roku) ręcznie, w trakcie lub po wizycie. Polskie firmy wdrażają AI w tempie 8,36% wobec 19,95% w UE (Eurostat, 2025). Duzi globalni skrybowie omijają Polskę: Microsoft Dragon Copilot dla lekarzy wymienia USA, Kanadę, Wielką Brytanię, Irlandię, Francję, Niemcy, Austrię, Belgię, Holandię i Szwajcarię, a nie Polskę (Microsoft, 10.2026); Abridge pokazuje tylko amerykańskie systemy opieki zdrowotnej (10.2026). Luka istnieje z powodu języka (polska mowa, łacina i nazwy leków), tajemnicy lekarskiej i danych zdrowotnych z art. 9 RODO oraz małych, rozdrobnionych dostawców EDM. Luka się zamyka: Noa Notes od Docplanner działa już w Polsce, a Tandem Health deklaruje ponad 10 000 organizacji opieki w Europie. Okno: 12-24 miesięcy dla niszy on-prem.

**Kto płaci i ile.** Kupujący: polski prywatny sektor ambulatoryjny, tysiące klinik i indywidualnych praktyk; Centralny Rejestr Lekarzy (NIL) publikuje liczby z dnia 30.06.2026 (dokładnej liczby nie wyciągnięto w tym przebiegu). Za co płacą teraz: czas lekarza spędzony na pisaniu, według powszechnych anegdot często 20-30% wizyty (niemierzone; nie znaleziono polskiego badania). Cena, którą klinika może zaakceptować: 150-400 PLN za lekarza miesięcznie plus jednorazowy box (moja hipoteza do przetestowania względem ceny Noa, która nie była widoczna na jej stronie). Kanał: dostawcy EDM jako resellerzy, regionalne izby lekarskie, sieci prywatnych klinik, stowarzyszenia dentystyczne.

**Aplikacja agentowa.**
1. Pobranie: nagranie audio wizyty (ze zgodą pacjenta zapisaną w aplikacji), rejestrowane na tablecie; audio nigdy nie opuszcza sieci LAN kliniki.
2. Ekstrakcja: lokalne rozpoznawanie polskiej mowy, potem diaryzacja (lekarz i pacjent), potem ustrukturyzowane fakty: dolegliwości, wywiad, badanie, leki, dawki, kandydaci ICD-10.
3. Rozumowanie: zmapowanie faktów na szablon notatki kliniki; zaproponowanie kodów ICD-10 i oznaczenie brakujących elementów (alergie, przeciwwskazania).
4. Szkic: notatka z wizyty, zalecenia dla pacjenta, tekst skierowania, szkic pól formularza zwolnienia lekarskiego (e-zwolnienie).
5. Weryfikacja: nazwy leków i dawki sprawdzane względem lokalnej listy leków; wszystko niepewne podświetlone, nigdy po cichu uzupełniane.
6. Działanie: **bramka akceptacji przez człowieka**: lekarz czyta, edytuje i podpisuje; dopiero wtedy notatka trafia do EDM; e-zwolnienia i recepty zawsze wystawia lekarz w oficjalnym systemie.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| Rozpoznawanie mowy po polsku | tak | nie | audio pacjenta to dane zdrowotne z art. 9 |
| Ekstrakcja faktów i szkic notatki | tak (Bielik-11B v3 lub Qwen) | nie | tajemnica lekarska, koszt wolumenu |
| Kontrole ICD-10 i leków | tak, plus tabele referencyjne | nie | kontrola deterministyczna jest bezpieczniejsza |
| Projekt szablonu dla specjalizacji | nie | tak (model z czołówki na przykładach syntetycznych) | brak danych pacjentów |
| Ewaluacja na zanonimizowanych transkrypcjach | częściowo | tak, tylko po anonimizacji | kontrola jakości |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
|---|---|---|---|---|---|
| Noa Notes (Docplanner, ZnanyLekarz) | startup | PL i 13 krajów | notatki AI do dokumentacji medycznej; dane w chmurze AWS i Azure | wysoka | niepokazana publicznie |
| Tandem Health | startup | UE | skryba otoczenia (ambient scribe), CE MDR klasa IIa, centra danych w UE, ponad 10 000 organizacji opieki *(deklaracja dostawcy)* | wysoka | niepokazana na stronie głównej |
| Microsoft Dragon Copilot | platforma globalna | 10 krajów, bez PL | ambientowa dokumentacja kliniczna dla lekarzy | wysoka | tylko wycena |
| Abridge | platforma globalna | USA | skryba otoczenia, ponad 300 systemów opieki zdrowotnej *(deklaracja dostawcy)* | wysoka | niepubliczna |
| Medfile i inni polscy dostawcy EDM | obecny gracz | PL | EDM, grafiki, dokumentacja pacjentów; notatek AI nie potwierdzono w tym przebiegu | niska (niezweryfikowane) | nie znaleziono |

Szukano polskich startupów typu ambient scribe zapytaniami po polsku i angielsku (asystent AI lekarza, transkrypcja wizyty, ambient AI scribe Poland): żadnego innego nie znaleziono w tym przebiegu. Luka: każdy znaleziony skryba działa w chmurze; żaden nie reklamuje boxa na miejscu. Lepiej partnerować z dostawcami EDM, niż walczyć z Noa o dystrybucję.

**Kontra z pięciu stron.**
- **Klient:** lekarze chcą tego za darmo lub w pakiecie; kliniki już w ZnanyLekarz dostają Noa od dostawcy, z którego korzystają do rezerwacji.
- **Obecny gracz:** Docplanner ma dystrybucję i markę; dostawcy EDM mogą dołączyć chmurowego skrybę w jednym wydaniu.
- **Czołowe laboratoria i big tech:** Microsoft może w każdej chwili dodać Polskę do Dragon Copilot; ogólne modele mowy stale poprawiają się w polskim.
- **Regulator:** skryba, który sugeruje kody lub treść kliniczną, może wejść na teren wyrobów medycznych (Tandem ma MDR klasy IIa); unijny AI Act dodaje obowiązki dla AI w wyrobach medycznych; odpowiedzialność za błędną dawkę jest poważna.
- **Ekonomia jednostkowa:** sprzęt na miejscu, serwis dla każdej kliniki i integracje z EDM są drogie dla firmy 1-3 osobowej; klinika z 5 lekarzami po 250 PLN za lekarza daje 1250 PLN miesięcznie.

**Po kontrze.** Przetrwa tylko jako produkt on-prem dla klinik ze ścisłą polityką tajemnicy (medycyna pracy, psychiatria i psychologia, sieci dentystyczne, prywatne skrzydła szpitali), sprzedawany przez jednego partnera EDM, ze ścisłym zakresem „tylko dokumentacja, żadnych porad klinicznych”, by pozostać poza MDR. Wynik 61; wykonalność i trwałość to słabe punkty.

**Liczby.**
- Wykorzystanie AI w Polsce 8,36% przedsiębiorstw wobec 19,95% w UE (Eurostat, 2025).
- Tandem Health: ponad 10 000 organizacji opieki w Europie, MDR klasa IIa, ISO 13485 i 27001 *(deklaracja dostawcy, 10.2026)*.
- Abridge: ponad 300 systemów opieki zdrowotnej, ponad 100 mln rozmów rocznie *(deklaracja dostawcy, 10.2026)*.
- Dragon Copilot dla lekarzy: wymienionych 10 krajów, Polski wśród nich nie ma (Microsoft, 10.2026).
- Noa: dane przechowywane w AWS i Azure, działa w 13 krajach *(deklaracja dostawcy, 10.2026)*.
- Udział czasu wizyty poświęcanego na dokumentację w Polsce: nie znaleziono.

**Jak zacząć.**
1. Tygodnie 1-3: polskie rozpoznawanie mowy plus szkicowanie notatek na lokalnym rigu, testowane na odegranych wizytach (bez prawdziwych pacjentów).
2. Tygodnie 4-6: szablony dla 2 specjalizacji (na przykład medycyny pracy i stomatologii), eksport jako tekst do jednego EDM.
3. Tygodnie 6-8: przegląd prawny zakresu „to nie wyrób medyczny” i szablon DPIA dla klinik.
4. Pierwszych 10 klientów: jedno partnerstwo z dostawcą EDM, potem prywatne kliniki w jednym mieście; oferować 1-miesięczny płatny pilotaż.
5. Test cenowy: za lekarza miesięcznie vs ryczałt za klinikę z boxem w cenie.

**Ryzyka i ograniczenia.**
- Noa i Tandem mogą już być wystarczająco dobre i tańsze niż box na miejscu.
- Klasyfikacja MDR lub AI Act, jeśli zakres rozszerzy się na kodowanie lub sugestie kliniczne.
- Błędy rozpoznawania mowy w nazwach leków i dawkach są niebezpieczne.
- Integracja z EDM to praca osobno dla każdego dostawcy.
- Czytelnik nie ma wykształcenia medycznego; potrzebny jest współzałożyciel lub doradca kliniczny.

**Kiedy przerwać.** Przerwać, jeśli żaden dostawca EDM nie zgodzi się na pilotaż w ciągu 3 miesięcy albo jeśli lekarze pilotażowi nadal edytują ponad połowę każdej notatki.

**Źródła:** [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Noa](https://noa.ai/pl) · [Tandem Health](https://www.tandemhealth.ai/) · [Dragon Copilot](https://www.microsoft.com/en-us/health-solutions/clinical-workflow/dragon-copilot) · [Abridge](https://www.abridge.com/) · [NIL doctor register statistics](https://nil.org.pl/rejestry/centralny-rejestr-lekarzy/informacje-statystyczne) · [Medfile search](https://www.bing.com/search?q=Medfile+AI+asystent+notatki+wizyta) · [Bielik-11B-v3.0-Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct)

---

## 14. Digitalizacja i wyszukiwanie w papierowych archiwach na miejscu

**Region:** PL / UE · **Kupujący:** archiwa firmowe i składnice akt, notariusze, parafie i diecezje, lokalne muzea, serwisy genealogiczne, urzędy gmin · **Model przychodu:** za stronę lub za projekt partii + opcjonalna licencja na urządzenie na miejscu · **Konkurencja:** średnia · **Dopasowanie modeli lokalnych:** wysokie · **Wynik: 60** (M9 G12 C8 L11 F11 R9)

> Wykonalne i obronne dla dokumentów, które nie mogą opuścić budynku (notarialne, kadrowe, księgi parafialne z danymi osobowymi), ale budżety są małe, a Transkribus jest tani, więc sprzedawać przeszukiwalne archiwa jako projekt, a nie OCR jako towar.

**Asymetria.** Papierowe archiwa w Polsce (akta osobowe firm przechowywane przez dekady, repertoria notarialne, księgi parafialne, akta urzędów gmin) nadal przeszukuje człowiek czytający teczki. Polskie firmy używają AI w 8,36% wobec 19,95% w UE (Eurostat, 2025). Rozpoznawanie tekstu odręcznego (HTR) istnieje, ale wiodąca platforma działa w chmurze: Transkribus przetwarza dane na swoich serwerach w Austrii i nie wspomina o opcji on-premise (10.2026). Wielu posiadaczy nie może lub nie chce wgrywać akt osobowych, aktów notarialnych ani ksiąg kościelnych z danymi wrażliwymi (religia to dane z art. 9 RODO). Klasyczny OCR, taki jak ABBYY FineReader, jest nastawiony na tekst drukowany i nie reklamuje obsługi pisma ręcznego. Modele wizyjno-językowe czytają dziś dokumenty dobrze (Qwen2.5-VL-7B osiąga 95,7% na DocVQA, karta modelu), co otwiera lokalną drogę; jakość na starym polskim piśmie odręcznym nie jest publicznie mierzona (nie znaleziono). Okno: 2-3 lata, bo praca jest projektowa i niechlujna, czego duże platformy unikają.

**Kto płaci i ile.** Kupujący: firmy ze starymi archiwami (przemysł, zakłady użyteczności publicznej, dawne firmy państwowe), notariusze, diecezje i parafie, firmy genealogiczne, muzea i samorządy (przetargi publiczne). Liczby i obecnych wydatków na ręczne indeksowanie: nie znaleziono w tym przebiegu. Ceny referencyjne: Transkribus Scholar 99 EUR rocznie za 900 kredytów, Team 449 EUR rocznie za 1500 kredytów i 5 miejsc, pakiety kredytów 250 za 59,50 EUR, 1 kredyt za stronę odręczną (Transkribus, 10.2026), więc chmurowy HTR kosztuje mniej więcej 0,24-0,50 EUR za stronę przy małym wolumenie. Projekt lokalny musi więc liczyć za cały wynik (koordynacja skanowania, indeksowanie, wyszukiwanie, prywatność), a nie za stronę: na przykład 15 000-60 000 PLN za projekt archiwalny (moja hipoteza do przetestowania). Kanał: stowarzyszenia archiwistów, integratorzy systemów zarządzania dokumentami, społeczności genealogiczne, izby notarialne.

**Aplikacja agentowa.**
1. Pobranie: skany lub zdjęcia teczek z telefonu; zapisana kolejność stron i metadane teczki.
2. Ekstrakcja: wykrywanie układu, potem HTR lub OCR lokalnym modelem wizyjno-językowym (rodzina Qwen VL, Apache 2.0) albo modelami Kraken wytrenowanymi na piśmie klienta.
3. Rozumowanie: normalizacja imion, dat i miejsc; łączenie rekordów (ta sama osoba w różnych księgach); klasyfikacja typów dokumentów.
4. Szkic: karty indeksowe, streszczenia teczek, ustrukturyzowane tabele (urodzenia, akty, akta zatrudnienia).
5. Weryfikacja: wskaźniki pewności dla każdej linii; linie o niskiej pewności trafiają do kolejki ręcznych poprawek; poprawki douczają model.
6. Działanie: **bramka akceptacji przez człowieka** przed opublikowaniem lub udostępnieniem jakiegokolwiek rekordu wnioskodawcy, ponieważ chodzi o dane osobowe i dokumenty prawne; portal wyszukiwania pozostaje w sieci klienta.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| Układ i HTR dokumentów wrażliwych | tak (Qwen VL, Kraken) | nie | dane osobowe i z art. 9, koszt wolumenu |
| HTR publicznych materiałów historycznych | tak | opcjonalnie (Transkribus lub wizja z czołówki) | brak tajemnicy, porównać jakość |
| Łączenie encji i indeksowanie | tak (Bielik, Qwen) | nie | wolumen |
| Trudne strony (uszkodzone, łacina, cyrylica, niemieckie Kurrent) | tak, najpierw | tak, na stronach niewrażliwych | wizja z czołówki jest lepsza przy rzadkich pismach |
| Interfejs wyszukiwania i streszczenia | tak | nie | zostaje w sieci klienta |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
|---|---|---|---|---|---|
| Transkribus (READ-COOP) | startup | UE (Austria) | chmurowy HTR, ponad 300 modeli społeczności, ponad 100 języków, ponad 500 000 użytkowników *(deklaracja dostawcy)* | wysoka | darmowe 50 kredytów miesięcznie; 99 do 449 EUR rocznie; wycena dla organizacji |
| eScriptorium z Kraken | open source | UE (Francja) | pipeline HTR do samodzielnego hostowania, silnik Kraken 7.1 | wysoka | darmowe oprogramowanie |
| ABBYY FineReader PDF | obecny gracz | globalnie | OCR i edycja PDF; pismo odręczne nie jest reklamowane | średnia | 99 do 165 EUR rocznie |
| Modele wizyjne z czołówki (ogólne aplikacje czatu) | platforma globalna | globalnie | czytają zdjęcia dokumentów w czacie | wysoka | subskrypcja lub za token |
| Lokalne biura usług digitalizacji | firma doradcza | PL | skanowanie i ręczne indeksowanie | niska (niezweryfikowane) | wycena indywidualna, nie znaleziono |

Luka: Transkribus jest wzorcem jakości i ceny, ale działa tylko w chmurze; eScriptorium jest darmowe, ale wymaga operatora. Pokonać ich, dostarczając gotowy box na miejscu plus warstwę indeksowania i wyszukiwania, używając pod spodem otwartych narzędzi.

**Kontra z pięciu stron.**
- **Klient:** wielu posiadaczy nie ma budżetu; parafie i genealodzy oczekują darmowych narzędzi; firmy rzadko widzą wyszukiwanie w archiwum jako pilne.
- **Obecny gracz:** Transkribus jest tani, dojrzały i mógłby dodać pakiet on-prem lub suwerenny dla UE; biura usług mają umowy na skanowanie.
- **Czołowe laboratoria i big tech:** ogólne modele wizyjne już czytają pismo odręczne w czacie; dla materiałów niewrażliwych są wystarczająco dobre.
- **Regulator:** księgi kościelne i notarialne mają zasady dostępu; archiwa publiczne kupują w przetargach o długich cyklach.
- **Ekonomia jednostkowa:** ceny za stronę są niskie; zysk daje tylko opłata projektowa i cykliczne licencje na wyszukiwanie; logistyka skanowania to praca ludzka.

**Po kontrze.** Przetrwa jako nisza dla wrażliwych archiwów, które nie mogą korzystać z chmury (akta osobowe, akta notarialne, księgi diecezjalne), sprzedawana jako projekt z licencją na wyszukiwanie. Nie konkurować ceną HTR za stronę. Wynik 60, ograniczony wielkością rynku i budżetem.

**Liczby.**
- Wykorzystanie AI w Polsce 8,36% wobec 19,95% w UE (Eurostat, 2025).
- Transkribus: ponad 500 000 użytkowników, ponad 200 mln stron, ponad 300 modeli, serwery w Austrii *(deklaracja dostawcy, 10.2026)*.
- Cena Transkribus: Scholar 99 EUR rocznie 900 kredytów, Team 449 EUR rocznie 1500 kredytów, 1 kredyt za stronę odręczną *(cennik dostawcy, 10.2026)*.
- ABBYY FineReader PDF Standard 99 EUR rocznie, Corporate 165 EUR rocznie *(cennik dostawcy, 10.2026)*.
- Qwen2.5-VL-7B: Apache 2.0, DocVQA 95,7% *(deklaracja dostawcy, karta modelu)*.
- Dokładność HTR na polskim piśmie parafialnym z XIX wieku przy lokalnych modelach: nie znaleziono.

**Jak zacząć.**
1. Tygodnie 1-3: porównać Qwen VL, Kraken i Transkribus na 200 stronach próbnych każdego typu (formularze drukowane, maszynopis, pismo odręczne).
2. Tygodnie 4-6: pipeline z kolejką poprawek i lokalnym wyszukiwaniem pełnotekstowym; spakować na box z jednym GPU.
3. Tygodnie 6-8: jeden płatny pilotaż z archiwum firmowym lub notariuszem, jeden darmowy z parafią lub towarzystwem genealogicznym jako studium przypadku.
4. Pierwszych 10 klientów: stowarzyszenia archiwistów, integratorzy systemów zarządzania dokumentami, izby notarialne.
5. Test cenowy: stała cena projektu vs cena za teczkę plus roczna licencja na wyszukiwanie.

**Ryzyka i ograniczenia.**
- Modele lokalne mogą być wyraźnie gorsze niż Transkribus na starym piśmie odręcznym.
- Małe budżety i wolne przetargi publiczne.
- Logistyka skanowania i fizyczne obchodzenie się z dokumentami to praca, a nie oprogramowanie.
- Obowiązki ochrony danych jako podmiot przetwarzający dane osobowe.

**Kiedy przerwać.** Przerwać, jeśli lokalna dokładność po treningu pozostaje dalece poniżej Transkribus na docelowych dokumentach albo jeśli w ciągu 4 miesięcy nie zamknie się żaden płatny pilotaż.

**Źródła:** [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Transkribus](https://www.transkribus.org/) · [Transkribus plans](https://www.transkribus.org/plans) · [eScriptorium](https://escriptorium.inria.fr/) · [ABBYY FineReader pricing](https://pdf.abbyy.com/pricing/) · [Qwen2.5-VL-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct)

---

## 15. Agent dokumentacji regulacyjnej dla małych firm medtech i farmaceutycznych (dokumentacje techniczne MDR/IVDR, PSUR-y, selekcja literatury)

**Region:** UE · **Kupujący:** szefowie ds. regulacyjnych (RA) i jakości w małych firmach medtech, małych firmach farmaceutycznych i generycznych oraz obsługujące je firmy doradztwa regulacyjnego · **Model przychodu:** za pakiet dokumentów (PSUR, przegląd literatury, kontrola luk w dokumentacji technicznej) + subskrypcja dla firm doradczych · **Konkurencja:** średnio-wysoka · **Dopasowanie modeli lokalnych:** średnie · **Wynik: 60** (M14 G12 C8 L9 F8 R9)

> Płatna nisza napędzana terminami (okres przejściowy MDR do 2027/2028), w której małe firmy nadal kupują godziny konsultantów, ale istniejące narzędzia AI już obejmują selekcję literatury, a czytelnikowi brakuje wiarygodności w dziedzinie regulacji.

**Asymetria.** Ponowna certyfikacja wyrobów dotychczasowych (legacy) w ramach MDR została przedłużona do 2027 roku dla większości klas i do 2028 dla klasy III oraz implantów klasy IIb (nowelizacja z 2023), więc tysiące dokumentacji technicznych, raportów z oceny klinicznej i PSUR-ów trzeba napisać lub zaktualizować w krótkim oknie czasowym. Komisja wciąż zmienia przepisy: rozporządzenie wykonawcze (UE) 2026/977 w sprawie jednolitych wymogów oceny zgodności weszło w maju 2026. Duzi producenci kupują platformy (Veeva, IQVIA); małe firmy kupują dni konsultantów, a resztę robią w Wordzie. Zmierzone przyjęcie AI w małych zespołach RA w medtechu: nie znaleziono. Luka istnieje z powodu odpowiedzialności (jednostka notyfikowana odrzuca słabą dokumentację), rozdrobnionych małych kupujących i pracy mocno opartej na angielskim, ale szablonowej. Zamyka się, gdy firmy doradcze same przyjmują narzędzia AI, prawdopodobnie w ciągu 2-3 lat.

**Kto płaci i ile.** Europejski medtech zatrudnia ponad 950 000 osób, a rynek wart jest około 173 mld EUR w 2025 roku (MedTech Europe, *szacunek zewnętrzny*); liczby małych producentów nie znaleziono w odczytanych źródłach. Jednostki notyfikowane: Team-NB wymienia 57 organizacji członkowskich (08.2026). Ile firmy płacą teraz: stawki dzienne konsultantów za pisanie CER i PSUR (nie znaleziono w publicznym źródle w tej sesji). Ceny do przetestowania: 1500-4000 EUR za pakiet PSUR lub przeglądu literatury; 500-2000 EUR miesięcznie za stanowisko w firmie doradczej. Kanał: firmy doradztwa regulacyjnego jako resellerzy (mają klientów i ponoszą odpowiedzialność), wydarzenia RAPS i klastrów medtech.

**Aplikacja agentowa.**
1. Pobranie: opis wyrobu, plik zarządzania ryzykiem, poprzedni CER/PSUR, dane o reklamacjach i vigilance, eksporty wyszukiwań literatury (PubMed, Embase).
2. Ekstrakcja: charakterystyka wyrobu, deklaracje (claims), liczba reklamacji w okresach, zdarzenia niepożądane.
3. Wnioskowanie: selekcja literatury według pisemnego protokołu (kryteria włączenia/wyłączenia z uzasadnieniem), mapowanie dowodów na wymogi z załącznika I do MDR, wyszukiwanie luk.
4. Szkic: sekcje PSUR, tabele przeglądu literatury, lista luk względem załączników II/III.
5. Weryfikacja: każde zdanie powiązane z wierszem źródła; liczby przeliczane z danych; drugi model sprawdza spójność twierdzeń z dowodami.
6. Działanie: wykwalifikowana osoba z RA zatwierdza, zanim cokolwiek trafi do jednostki notyfikowanej lub organu; agent nigdy niczego nie składa.

**Podział lokalny i płatny.**
| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
| --- | --- | --- | --- |
| Ekstrakcja danych o reklamacjach i vigilance | Tak | Nie | Mogą zawierać dane pacjentów, szczególna kategoria danych w RODO |
| Selekcja literatury po tytułach i abstraktach | Tak | Opcjonalnie | Duży wolumen, dane publiczne, liczy się koszt |
| Synteza dowodów i redakcja | Możliwe | Tak, preferowane | Długie, precyzyjne wnioskowanie po angielsku; dane w większości nieosobowe |
| Krzyżowa kontrola twierdzenie-dowód | Tak | Tak (druga opinia) | Dwa różne modele zmniejszają wspólne błędy |
| Formatowanie do szablonów | Niepotrzebne (deterministyczne) | Niepotrzebne | Szablony są stałe |

**Konkurencja.**
| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
| --- | --- | --- | --- | --- | --- |
| DistillerSR | platforma globalna | globalnie | Przegląd literatury do CER/PER w ramach MDR/IVDR, selekcja AI, ponowne rankingowanie, ekstrakcja dowodów, Part 11 i Annex 11 | Głęboka | Niepubliczna |
| Veeva Vault Safety | obecny gracz | globalnie | Zarządzanie przypadkami bezpieczeństwa z agentami Falcon Safety i narracjami Vault AI, od początkujących firm biotech wzwyż | Głęboka | Niepubliczna |
| IQVIA Vigilance Platform | obecny gracz | globalnie | Farmakowigilancja w modelu SaaS z przetwarzaniem przypadków i tłumaczeniem opartym na AI i ML | Głęboka | Niepubliczna |
| Firmy doradztwa regulacyjnego (w całej UE) | firma doradcza | UE | CER-y, PSUR-y, dokumentacje techniczne pisane przez ludzi | Niska do średniej | Stawki dzienne, niepubliczne |

Luka: małe firmy medtech potrzebujące redakcji PSUR i dokumentacji technicznej za stałą cenę; unikać samej selekcji literatury (DistillerSR) i przetwarzania przypadków bezpieczeństwa leków (Veeva, IQVIA).

**Kontra z pięciu stron.**
- **Klient:** Szefowie RA odpowiadają przed jednostkami notyfikowanymi; nie zaufają nowemu graczowi bez uprawnień regulacyjnych. Wymagany jest partner – konsultant RA.
- **Obecny gracz:** DistillerSR już oferuje selekcję AI ze ścieżką audytu; Veeva i IQVIA schodzą w dół do początkujących firm biotech.
- **Czołowe laboratoria i big tech:** Modele ogólne piszą dobrą prozę regulacyjną; firmy doradcze mogą ich używać bezpośrednio z szablonami, kurcząc warstwę narzędziową.
- **Regulator:** Oczekiwania walidacyjne (Part 11, Annex 11, GAMP) wobec narzędzi dotykających rekordów jakościowych dodają koszt; AI Act może też dotyczyć narzędzi używanych w procesach bezpieczeństwa.
- **Ekonomia jednostkowa:** Każda rodzina wyrobów jest inna; przegląd przez wykwalifikowaną osobę pozostaje, więc marża zależy od partnera-konsultanta.

**Po kontrze.** Przetrwa tylko jako narzędzie sprzedawane firmom doradztwa RA i razem z nimi (to one ponoszą odpowiedzialność i mają klientów), skoncentrowane na redakcji PSUR i kontroli luk. Modele lokalne mają tu mniejsze znaczenie, bo większość danych wejściowych jest nieosobowa; wynik pozostaje blisko 60.

**Liczby.**
- Okres przejściowy MDR przedłużony do 2027 i 2028 zależnie od klasy (nowelizacja z 2023, podsumowanie z Wikipedii rozporządzenia 2017/745).
- Rozporządzenie wykonawcze (UE) 2026/977 w sprawie oceny zgodności i jednostek notyfikowanych, maj 2026 (Komisja Europejska).
- Team-NB: 57 jednostek notyfikowanych będących członkami, 08.2026.
- Europejski medtech: ponad 950 000 miejsc pracy, rynek około 173 mld EUR w 2025 *(szacunek zewnętrzny, MedTech Europe)*.
- DistillerSR: ponowne rankingowanie AI „potencjalnie skracające czas selekcji nawet o 70%” *(deklaracja dostawcy)*.

**Jak zacząć.**
1. Tygodnie 1-4: potok redakcji PSUR dla jednej klasy wyrobów na danych publicznych (FDA MAUDE, opublikowane szablony PSUR).
2. Tygodnie 5-8: partnerstwo z 1-2 konsultantami RA; wspólne przygotowywanie prawdziwych PSUR-ów z ich akceptacją.
3. Pierwszych 10 klientów: najpierw firmy doradcze (każda przynosi kilku producentów).
4. Test cenowy: cena za PSUR vs subskrypcja stanowiska w firmie doradczej.

**Ryzyka i ograniczenia.**
- Luka w wiarygodności dziedzinowej; brak doświadczenia RA w zespole.
- Odpowiedzialność, jeśli złożony dokument zawiera błąd.
- Walidacja i dokumentacja QMS dla samego narzędzia.
- Przepisy się zmieniają (akty wykonawcze z 2026, możliwa reforma MDR).

**Kiedy przerwać.** Przerwać, jeśli żadna firma doradztwa RA nie zgodzi się na płatny pilotaż w ciągu 3 miesięcy.

**Źródła:** [Regulation (EU) 2017/745 on Wikipedia](https://en.wikipedia.org/wiki/Regulation_(EU)_2017/745) · [European Commission: medical devices new regulations](https://health.ec.europa.eu/medical-devices-sector/new-regulations_en) · [Team-NB documents](https://www.team-nb.org/team-nb-documents/) · [MedTech Europe: about the industry](https://www.medtecheurope.org/about-the-industry/) · [DistillerSR](https://www.distillersr.com/products/distillersr-systematic-review-software) · [Veeva Vault Safety](https://www.veeva.com/products/vault-safety/) · [IQVIA safety and pharmacovigilance](https://www.iqvia.com/solutions/safety-regulatory-compliance/safety-and-pharmacovigilance)

---

## 16. Polski agent telefoniczny i czatowy dla lokalnych firm usługowych

**Region:** PL · **Kupujący:** prywatne gabinety i kliniki, warsztaty samochodowe, salony, małe hotele · **Model przychodu:** miesięczna subskrypcja + opłata za minuty · **Konkurencja:** wysoka · **Dopasowanie modeli lokalnych:** niskie · **Wynik: 59** (M15 G13 C6 L7 F11 R7)

> Popyt jest realny, ale rynek jest zatłoczony, a marże cienkie; przetrwa tylko wąski wertykał z głęboką integracją z kalendarzem.

**Asymetria.** Polskie MŚP wdrażają AI powoli (8,36% przedsiębiorstw w 2025 roku wobec 19,95% w UE; małe firmy 17% w całej UE, Eurostat 2025). Małe firmy usługowe nadal odbierają telefony ręcznie, tracą połączenia podczas pracy i przepisują rezerwacje. Platformy rezerwacyjne już zdigitalizowały kalendarz (Booksy Biz od 145 PLN netto miesięcznie, 2026), ale linia telefoniczna i wiadomości pozostają u wielu ręczne. Luka szybko się zawęża, bo platformy agentów głosowych sprawiają, że zbudowanie bota jest tanie dla każdego.

**Kto płaci i ile.** Liczba polskich gabinetów, warsztatów i salonów: nie znaleziono w tym przebiegu. Punkty odniesienia kosztów: Booksy Biz 145 PLN netto miesięcznie + 35 PLN za każdego dodatkowego pracownika (*cena dostawcy*, 14.10.2026). Koszt infrastruktury głosowej: Retell podaje 0,07-0,31 USD za minutę łącznie (*cena dostawcy*, 14.10.2026). Cena dla kupującego do przetestowania: 300-900 PLN miesięcznie z pulą minut. Kanał: partnerzy z oprogramowania rezerwacyjnego, lokalne agencje marketingowe, stowarzyszenia warsztatów i gabinetów.

**Aplikacja agentowa.**
1. Wczytanie: przychodzące połączenie lub czat, rozpoznawanie mowy po polsku.
2. Ekstrakcja: intencja, usługa, preferowane terminy, tożsamość klienta.
3. Rozumowanie: sprawdzenie wolnych terminów w kalendarzu na żywo, FAQ firmy, cennik.
4. Redakcja: odpowiedź głosowa i proponowany termin.
5. Weryfikacja: potwierdzenie szczegółów rozmówcy; przekazanie człowiekowi w razie wątpliwości.
6. Działanie: rezerwacja w kalendarzu; **zatwierdzenie przez człowieka** dla triażu medycznego, zwrotów lub czegokolwiek poza cennikiem. Przetwarzanie danych pacjentów zgodnie z RODO.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| Rozpoznawanie mowy | Możliwe | Zwykle | Opóźnienie i dokładność dla polskiego |
| Rozumowanie dialogowe | Możliwe (Bielik 11B v3) | Zwykle | Opóźnienie poniżej sekundy w godzinach szczytu |
| Synteza mowy | Rzadko | Tak | Naturalne polskie głosy |
| Streszczenia rozmów i analityka | Tak | Nie | Przetwarzanie wsadowe, tanie lokalnie |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
|---|---|---|---|---|---|
| Booksy | obecny gracz | PL/globalnie | Platforma rezerwacyjna dla salonów | Nie znaleziono agenta telefonicznego AI w tym przebiegu | od 145 PLN netto miesięcznie |
| Docplanner (ZnanyLekarz) | obecny gracz | PL/globalnie | Rezerwacje dla gabinetów, narzędzia telefoniczne | Funkcje AI: szczegółów nie znaleziono w tym przebiegu | nie znaleziono |
| Retell AI | platforma globalna | globalnie | Infrastruktura agentów głosowych | Wysoka | 0,07-0,31 USD za minutę |
| Voicebot.pl | startup | PL | Voiceboty dla procesów biznesowych | Średnia do wysokiej | nie znaleziono |
| EasyCall | startup | PL | Voicebot do obsługi klienta | Średnia | nie znaleziono |
| Asseco voicebot | obecny gracz | PL | Chatbot i voicebot | Średnia | nie znaleziono |

Luka: dostawców horyzontalnych jest wielu; wertykał (na przykład warsztaty samochodowe z ich oprogramowaniem warsztatowym) może być jeszcze wolny. Platformy rezerwacyjne są największym zagrożeniem, bo to one posiadają kalendarz.

**Kontra z pięciu stron.**
- **Klient:** właściciele nie lubią płacić miesięcznie; zła jakość głosu traci klientów.
- **Obecny gracz:** Booksy i Docplanner mogą dodać agenta głosowego do milionów kalendarzy naraz.
- **Czołowe laboratoria i big tech:** modele głosowe czasu rzeczywistego tanieją i poprawiają się po polsku; przewaga się kurczy.
- **Regulator:** przejrzystość według AI Act (rozmówca musi wiedzieć, że to AI), RODO dla danych zdrowotnych, zgoda na nagrywanie rozmów.
- **Ekonomia jednostkowa:** koszty za minutę plus wsparcie przy bilecie 300-900 PLN; wysoki odpływ klientów.

**Po kontrze.** Przetrwa tylko jako dodatek wertykalny (jedna branża, jedna integracja oprogramowania) lub jako white-label dla agencji. Modele lokalne mają tu małe znaczenie. Wynik poniżej 60.

**Liczby.**
- PL 8,36% vs UE 19,95% wykorzystania AI w przedsiębiorstwach, 2025 (Eurostat).
- Booksy Biz 145 PLN netto miesięcznie (*cena dostawcy*, 14.10.2026).
- Retell 0,055 USD za minutę infrastruktury, 0,07-0,31 USD za minutę łącznie (*cena dostawcy*, 14.10.2026).
- Liczba docelowych MŚP: nie znaleziono.

**Jak zacząć.**
1. Tygodnie 1-4: wybrać warsztaty samochodowe; zbudować na platformie głosowej; zintegrować jeden kalendarz warsztatowy.
2. Tygodnie 5-8: 3 darmowe piloty; zmierzyć odzyskiwanie nieodebranych połączeń.
3. Pierwszych 10 klientów: akwizycja od drzwi do drzwi w jednym mieście plus partner z oprogramowania warsztatowego.
4. Test ceny: 399 vs 699 PLN miesięcznie z limitami minut.

**Ryzyka i ograniczenia.**
- Ryzyko platformy ze strony obecnych graczy z rezerwacjami.
- Jakość polskiego głosu i opóźnienia.
- Cienkie marże i odpływ klientów.
- Obowiązki informacyjne wynikające z regulacji.

**Kiedy przerwać.** Przerwać, jeśli w ciągu 6 tygodni piloty nie pokażą więcej zarezerwowanych zleceń niż kosztów lub jeśli obecny gracz z rezerwacjami wypuści tańszego wbudowanego agenta.

**Źródła:** [Eurostat: wykorzystanie AI w przedsiębiorstwach](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Booksy Biz: cennik](https://biz.booksy.com/pl-pl/cennik) · [Retell: cennik](https://www.retellai.com/pricing) · [Bielik-11B-v3.0-Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct)

---

## 17. Współpilot do wniosków o dotacje dla polskich firm doradczych

**Region:** PL · **Kupujący:** małe firmy doradcze od dotacji i MŚP aplikujące do FENG, KPO, FEnIKS i programów regionalnych · **Model przychodu:** abonament na stanowisko konsultanta + opłata za wniosek · **Konkurencja:** średnia · **Dopasowanie modeli lokalnych:** średnie · **Wynik: 58** (M12 G13 C8 L7 F11 R7)

> Prawdziwa papierologia i prawdziwe pieniądze, ale kupującym jest firma doradcza, która sprzedaje pracę ręczną, nabory są nierówne, a ogólne modele czatu już wykonują część pisarską, więc działa to tylko jako narzędzie dla konsultantów, a nie przeciwko nim.

**Asymetria.** Polskie MŚP aplikują o środki unijne przez długie formularze, biznesplany i listy kryteriów, które w większości piszą firmy doradcze. Sam FENG ma około 7,9 mld EUR na lata 2021-2027 (portal programu, według wyników wyszukiwania, 10.2026), z naborami zaplanowanymi do 2026 roku. Wykorzystanie AI w polskich przedsiębiorstwach wyniosło w 2025 roku 8,4% (Eurostat, 11.12.2025). Nie znaleziono polskiego produktu, który z użyciem AI przygotowuje wnioski FENG lub KPO (wyszukiwania w Bing po polsku, 14.10.2026; wyniki pokazały tylko ogólne narzędzia czatu). Luka istnieje, bo każdy nabór ma własne kryteria, formularze i polski język prawniczy, a firmy doradcze są małe i konserwatywne. Zamknie się szybko, gdy firmy doradcze ustandaryzują się na ogólnych narzędziach czatu.

**Kto płaci i ile.** Kupujący: polskie firmy doradcze od dotacji (liczby nie znaleziono) oraz MŚP aplikujące bezpośrednio. Wysokości wynagrodzenia firm doradczych (opłata stała plus premia za sukces) nie znaleziono w tej sesji; nie podawałbym procentu bez źródła. Ceny do przetestowania: 300-600 PLN za stanowisko miesięcznie dla firm doradczych lub 500-1500 PLN za wniosek dla MŚP. Kanał: najpierw firmy doradcze (mają pipeline), potem stowarzyszenia MŚP.

**Aplikacja agentowa.**
1. Pobranie: dokumentacja naboru (regulamin, kryteria, wzory formularzy) i dokumenty klienta (dane finansowe, pomysł na projekt).
2. Ekstrakcja: zasady kwalifikowalności, kryteria punktowe, wymagane załączniki, limity budżetu i zasady pomocy publicznej.
3. Wnioskowanie: sprawdzenie kwalifikowalności i szacunek punktacji kryterium po kryterium z lukami.
4. Szkic: opis projektu, analiza rynku, tabela wskaźników i uzasadnienie budżetu dla każdej sekcji.
5. Weryfikacja: każde twierdzenie powiązane z dokumentem źródłowym; macierz pokrycia kryteriów; limity znaków.
6. Działanie: **bramka akceptacji przez człowieka**: konsultant lub firma podpisuje i składa; agent nigdy nie składa wniosku.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| Parsowanie dokumentów naboru | lokalnie | nie | Teksty publiczne, duży wolumen przy każdym naborze |
| Dane finansowe i know-how klienta | lokalnie | nie | Tajemnice handlowe wnioskodawcy, niepublikowane pomysły B&R |
| Pisanie narracji | najpierw lokalnie | Claude dla kluczowych sekcji | Jakość polskiej prozy decyduje o punktacji |
| Sprawdzenie pokrycia kryteriów | lokalnie | nie | Oparte na regułach, tanie |
| Przegląd końcowy | nie | płatny model opcjonalnie | Druga opinia przy wnioskach o wysokiej wartości |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Poziom AI | Cena |
|---|---|---|---|---|---|
| Grantable | startup | USA | Wyszukiwanie naborów, biurko do pisania, pipeline, biblioteka | wysoki | 50 do 150 USD miesięcznie, centrum dla agencji 300 USD |
| Polskie firmy doradcze od dotacji | firma doradcza | PL | Pełne pisanie wniosków za opłatę i premię za sukces | niski lub nieznany | nie znaleziono |
| ChatGPT, Claude, Copilot | platforma globalna | globalnie | Ogólne pisanie na podstawie wgranych dokumentów naboru | ogólny | plany biznesowe |
| PARP i punkty informacyjne funduszy UE | obecny gracz | PL | Bezpłatne doradztwo w sprawie naborów i kwalifikowalności | brak | za darmo |
| Granter i inne polskie narzędzia AI do dotacji | startup | PL | nie znaleziono w wyszukiwaniu 14.10.2026 | nie znaleziono | nie znaleziono |

Grantable jest zbudowany dla amerykańskich fundacji, a nie dla formularzy unijnych funduszy strukturalnych. Polskie firmy doradcze to rynek, a nie wróg: sprzedaje się im szybkość.

**Kontra z pięciu stron.**
- **Klient:** Firmy doradcze mogą widzieć narzędzie jako zagrożenie dla swojego wynagrodzenia; MŚP kupujące je bezpośrednio nie mają wiedzy, by ocenić szkice.
- **Obecny gracz:** Duże firmy doradcze mogą w kilka tygodni zbudować własne biblioteki promptów na ogólnych narzędziach czatu.
- **Czołowe laboratoria i big tech:** Modele ogólne już piszą dobrą polską prozę; pozostała wartość to kryteria specyficzne dla naboru i kontrola załączników.
- **Regulator:** Instytucje finansujące mogą dodać oświadczenia o użyciu AI lub karać za szablonowy tekst; fałszywe oświadczenia we wniosku mają skutki prawne, więc weryfikacja jest krytyczna.
- **Ekonomia jednostkowa:** Popyt szczytuje wokół terminów naborów i spada między nimi; rezygnacje między naborami to główne zagrożenie.

**Po kontrze.** Przetrwa tylko jako narzędzie do sprawdzania kryteriów i pisania, sprzedawane 10-30 firmom doradczym, z lokalnym przetwarzaniem jako argumentem poufności dla pomysłów B&R klientów. Wynik 58, poniżej poprzeczki top-15, chyba że dołączy partner z firmy doradczej.

**Liczby.**
- FENG około 7,9 mld EUR na lata 2021-2027 *(portal programu przez fragment wyników wyszukiwania, 10.2026)*.
- Polska 8,4% wykorzystania AI w przedsiębiorstwach w 2025 (Eurostat, 11.12.2025).
- Grantable: plany miesięczne 50, 150 i 300 USD *(deklaracja dostawcy, 10.2026)*.
- Wysokość wynagrodzeń firm doradczych: nie znaleziono.

**Jak zacząć.**
1. Tygodnie 1-3: sparsować jeden nabór FENG i jeden regionalny do macierzy kryteriów.
2. Tygodnie 4-6: pisanie i sprawdzanie pokrycia dla 5 dawnych udanych wniosków przekazanych przez firmę doradczą.
3. Tygodnie 7-8: aplikacja webowa oparta na stanowiskach z opcją lokalnego przetwarzania.
4. Pierwszych 10 klientów: małe firmy doradcze o wielkości 2-10 osób, 1 miesiąc darmowego użytkowania przed terminem naboru.
5. Test cen: za stanowisko kontra za wniosek.

**Ryzyka i ograniczenia.**
- Sezonowy popyt związany z kalendarzami naborów.
- Okres finansowania 2021-2027 się kończy; kolejna perspektywa może zmienić formularze.
- Firmy doradcze budują własne narzędzia na ogólnych modelach czatu.
- Odpowiedzialność za fałszywe oświadczenia we wnioskach.

**Kiedy przerwać.** Przerwać, jeśli mniej niż 5 firm doradczych zapłaci po pierwszym dużym cyklu naborów.

**Źródła:** [Portal FENG](https://www.nowoczesnagospodarka.gov.pl) · [Eurostat – wykorzystanie AI 2025](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2) · [Cennik Grantable](https://www.grantable.co/pricing) · [Bielik 11B v3](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [PLLuM 12B instruct](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512)

---

## 18. Agent badawczy do polskich interpretacji podatkowych i orzecznictwa

**Region:** PL · **Kupujący:** firmy doradztwa podatkowego (doradcy podatkowi), wewnętrzne zespoły podatkowe średnich i dużych firm, biura rachunkowe z działami doradczymi · **Model przychodu:** miesięczna subskrypcja za stanowisko, licencja on-prem dla firm trzymających akta u siebie · **Konkurencja:** wysoka · **Dopasowanie modeli lokalnych:** wysokie · **Wynik: 52** (M10 G10 C5 L11 F9 R7)

> Technicznie łatwy i dobrze pasujący do modeli lokalnych, ale konkuruje z dwoma wydawcami prawniczymi, którzy posiadają komentarze i relację z klientem; opłacalny tylko jako warstwa badawcza on-prem nad darmowymi źródłami publicznymi plus własne opinie firmy.

**Asymetria.** Surowiec jest publiczny i darmowy: indywidualne interpretacje podatkowe (KIS) w bazie Eureka Ministerstwa Finansów oraz orzeczenia sądów administracyjnych (NSA i WSA) w bazie CBOSA pod adresem orzeczenia.nsa.gov.pl. Przeszukiwanie ich nadal opiera się na słowach kluczowych, a doradca czyta dziesiątki interpretacji, żeby znaleźć linię argumentacji dla jednego pytania klienta. Polska jest ogólnie późnym adopterem AI (8,36% przedsiębiorstw w 2025 roku wobec 19,95% w UE, Eurostat), podczas gdy sektor profesjonalny, naukowy i techniczny jest drugim najwyższym użytkownikiem AI w całej UE (40,43%), więc doradcy podatkowi prawdopodobnie przyjmą AI szybciej niż inne polskie MŚP, a luka może się szybko zamknąć (moja inferencja). Dlaczego luka istnieje: tajemnica zawodowa doradców sprawia, że niechętnie wklejają fakty klienta do zagranicznych narzędzi w chmurze.

**Kto płaci i ile.** Liczby licencjonowanych doradców podatkowych w Polsce nie znaleziono w tym przebiegu. Doradcy już płacą za subskrypcje LEX (Wolters Kluwer) lub Legalis (C.H.Beck); LEX Księgowość „z czatem AI” jest wymieniony od 159,60 PLN netto miesięcznie (promocja, regularnie 168,00 PLN; lex.pl, pobrano 14.10.2026), cen Legalis nie znaleziono (strona niedostępna w tym przebiegu). Agent badawczy musi kosztować mniej niż dodatkowy moduł wydawcy albo dowodzić zaoszczędzonych godzin. Cena testowa: 200-500 PLN za stanowisko miesięcznie, box on-prem dla 10+ stanowisk (hipoteza). Kanał: regionalne wydarzenia Krajowej Izby Doradców Podatkowych, konferencje podatkowe, LinkedIn.

**Aplikacja agentowa.**
1. Pobranie: crawl interpretacji z Eureki i orzeczeń z CBOSA (z poszanowaniem regulaminów i limitów zapytań), plus własne dotychczasowe opinie firmy.
2. Ekstrakcja: stan faktyczny, pytanie, stanowisko podatnika, stanowisko organu, podstawa prawna, wynik, data.
3. Rozumowanie: wyszukanie interpretacji i orzeczeń o podobnym stanie faktycznym; grupowanie według linii argumentacji; oznaczanie zmian linii w czasie.
4. Szkic: memo badawcze po polsku z cytatami (sygnatura, data, sąd) i fragmentami.
5. Weryfikacja: każdy cytat jest sprawdzany względem zapisanego tekstu źródłowego; twierdzenia bez cytatu są usuwane.
6. Działanie: bramka akceptacji przez człowieka, doradca podpisuje każdą opinię; agent nigdy nie wysyła porad klientowi.

**Podział lokalny i płatny.**

| Krok | Lokalny model otwarty | Płatne API | Dlaczego |
|---|---|---|---|
| Crawl i indeksowanie źródeł publicznych | model embeddingów uruchomiony lokalnie | brak | dane publiczne, wolumen |
| Ekstrakcja stanu faktycznego i wyniku | Bielik 11B v3 lub klasa Qwen | brak | duży wolumen, polski tekst prawniczy |
| Wyszukiwanie po faktach klienta | tylko lokalnie | brak | tajemnica zawodowa doradcy |
| Pisanie memo | model lokalny | model z czołówki tylko z zanonimizowanymi faktami, za zgodą | jakość w trudnym rozumowaniu |
| Weryfikacja cytatów | brak modelu, dopasowanie ciągów | brak | deterministyczne |

**Konkurencja.**

| Konkurent | Typ | Region | Co oferuje | Głębokość AI | Cena |
|---|---|---|---|---|---|
| LEX (Wolters Kluwer Polska) | obecny gracz | PL | system informacji prawnej z treściami podatkowymi, interpretacjami, orzeczeniami; LEX Księgowość, LEX Kadry i LEX Biuro Rachunkowe „z czatem AI”, LEX Flex „z Expert AI” | wyspecjalizowany czat AI w ramach subskrypcji *(deklaracja dostawcy)*, głębokość nietestowana | LEX Księgowość od 159,60 PLN netto miesięcznie (10.2026, promocja) |
| Legalis (C.H.Beck) | obecny gracz | PL | komentarze, czasopisma, duża baza orzecznictwa, wzory | funkcji AI nie zweryfikowano w tym przebiegu | nie znaleziono |
| Eureka (Ministerstwo Finansów) | publiczny | PL | darmowa baza interpretacji podatkowych | wyszukiwanie po słowach kluczowych | za darmo |
| CBOSA (orzeczenia.nsa.gov.pl) | publiczny | PL | darmowa baza orzeczeń sądów administracyjnych | wyszukiwanie po słowach kluczowych | za darmo |
| Harvey | platforma globalna | globalnie | asystent AI dla kancelarii prawnych i podatkowych | wysoka *(deklaracja dostawcy)* | niepubliczna |

Luka: wydawcy sprzedają treść plus wyszukiwanie; agenta po stronie firmy, który łączy źródła publiczne z prywatnym archiwum opinii firmy, na sprzęcie samej firmy, nie znaleziono w tym przebiegu. Pokonać ich prywatnością i prywatnym archiwum, nie treścią.

**Kontra z pięciu stron.**
- **Klient:** doradcy już płacą za LEX lub Legalis i nie dodadzą drugiego narzędzia bez wyraźnej oszczędności czasu; zaufanie do cytatów to cały produkt.
- **Obecny gracz:** obaj wydawcy posiadają komentarze, markę i umowy; dodanie RAG nad własnym korpusem jest dla nich tanie.
- **Czołowe laboratoria i big tech:** ogólni asystenci z wyszukiwaniem w sieci potrafią znaleźć interpretacje; obronną częścią jest prywatne archiwum i wdrożenie on-prem.
- **Regulator:** doradca pozostaje odpowiedzialny; tajemnica zawodowa przemawia za wdrożeniem lokalnym; crawl baz publicznych musi respektować ich regulaminy.
- **Ekonomia jednostkowa:** mała liczba stanowisk w firmie; boxy on-prem dodają koszt wsparcia sprzętu.

**Po kontrze.** Przetrwa tylko jako niszowe narzędzie on-prem dla średnich firm doradczych z dużym prywatnym archiwum opinii; LEX już dołącza czat AI do subskrypcji księgowych i kadrowych za około 160 PLN miesięcznie, poniżej mojej ceny testowej 200-500 PLN, więc wynik spada do 52 (C5) i zostaje poza górną grupą.

**Liczby.**
- Wykorzystanie AI: PL 8,36% wobec 19,95% przedsiębiorstw w UE; unijny sektor profesjonalny, naukowy i techniczny 40,43% (Eurostat, dane za 2025).
- Liczba doradców podatkowych i wewnętrznych zespołów podatkowych w Polsce: nie znaleziono w tym przebiegu (sprawdzono 14.10.2026 stronę główną kidp.pl, strony „poznaj KIDP” i „30 lat KIDP”, pl.wikipedia i strony wyników wyszukiwania; żadna nie podaje liczby).
- LEX: czat AI w LEX Księgowość, LEX Kadry, LEX Biuro Rachunkowe; LEX Księgowość od 159,60 PLN netto miesięcznie, regularnie 168,00 PLN (lex.pl, pobrano 14.10.2026, *(deklaracja dostawcy)*); daty uruchomienia czatu AI nie znaleziono.
- Funkcje AI i ceny Legalis: nie znaleziono (legalis.pl i beck.pl niedostępne w tym przebiegu, 14.10.2026).
- Bielik 11B v3 Instruct, Apache 2.0, model bazowy z 30.07.2025 (karta modelu Hugging Face).

**Jak zacząć.**
1. Tygodnie 1-4: zaindeksować jeden temat podatkowy (VAT od usług budowlanych) z Eureki i CBOSA; generator memo ze sprawdzaniem cytatów.
2. Tygodnie 5-8: dodać import prywatnego archiwum i skrypt wdrożenia lokalnego.
3. Pierwszych 10 klientów: butikowe firmy doradcze poznane na wydarzeniach KIDP; darmowy pilotaż na jednym żywym temacie każda.
4. Test cen: cena za stanowisko vs licencja on-prem dla całej firmy.

**Ryzyka i ograniczenia.**
- Wydawcy dodają tę samą funkcję do istniejących subskrypcji.
- Zhalucynowane cytaty natychmiast niszczą zaufanie.
- Dostęp do baz publicznych może się zmienić lub zostać ograniczony limitami.
- Mały rynek kupujących z budżetem.

**Kiedy przerwać.** Przerwać, jeśli pilotaże pokażą mniej niż 30% oszczędności czasu na pytanie badawcze albo żadna firma nie przejdzie na płatny plan w ciągu 2 miesięcy.

**Źródła:** [Eureka](https://eureka.mf.gov.pl/) · [CBOSA](https://orzeczenia.nsa.gov.pl/) · [Legalis](https://legalis.pl) · [LEX](https://www.lex.pl) · [KIDP](https://kidp.pl/) · [Eurostat wykorzystanie AI](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Bielik 11B v3 Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) · [Harvey](https://www.harvey.ai)

---

## Pomysły, które nie przetrwały kontry

Ci kandydaci byli badani według tego samego szablonu. Odpadli przez konkurencję, budżet, jakość modeli lub regulacje albo
wchłonął ich silniejszy pomysł z tej samej przestrzeni. Każda notatka podaje powód i dowody.

### Zaplecze administracyjne wspólnot mieszkaniowych i zarządców nieruchomości

Pomysł: agent dla zarządców wspólnot mieszkaniowych i spółdzielni, który czyta pisma mieszkańców, przygotowuje projekty uchwał i odpowiedzi, uzgadnia wpłaty opłat i przygotowuje roczne sprawozdania. Wynik: **56** (M10 G14 C9 L9 F7 R7). Nieruchomości nie są na papierze maruderem: w 2025 roku AI stosowało 24,82% unijnych przedsiębiorstw z branży nieruchomości, powyżej stawki 19,95% dla wszystkich sektorów (Eurostat, 2025), choć Polska ogółem ma 8,36%. Liczba polskich wspólnot mieszkaniowych i zarządców oraz to, ile płacą dziś: nie znaleziono w tym przebiegu (wyszukiwania nie zwróciły użytecznych wyników). Odpada w kontrze głównie z powodu dostępu: kupujący to wiele malutkich firm na utrwalonych programach księgowych i administracyjnych, czytelnik nie ma wiedzy dziedzinowej, a budżet na wspólnotę jest mały. Modele lokalne trochę pomagają (dane osobowe mieszkańców), ale nie na tyle, by uzasadnić pudełko. Warto wrócić do tematu z partnerem, który zarządza budynkami.

**Źródła:** [Eurostat: wykorzystanie AI w przedsiębiorstwach](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

### Due diligence nieruchomości na podstawie ksiąg wieczystych i planów zagospodarowania

Pomysł: agent, który czyta księgę wieczystą, miejscowy plan zagospodarowania przestrzennego (MPZP) lub decyzję o warunkach zabudowy (WZ) oraz akty notarialne i przygotowuje szkic raportu ryzyka dla kupujących, pośredników, banków i małych deweloperów. **Wynik: 55** (M11 G12 C10 L5 F9 R8). Dane z ksiąg wieczystych są już tanio sprzedawane online: EKW+ przeszukuje ponad 24,8 mln ksiąg i ponad 40 mln działek i sprzedaje raporty z ksiąg od 35 PLN za jeden do 12 PLN za sztukę w pakiecie 100, plus nowy „Raport o działce” *(cennik dostawcy, 10.2026)*. Wyszukiwanie w Bing narzędzi AI do analizy ksiąg i due diligence („sztuczna inteligencja analiza ksiąg wieczystych”, „due diligence nieruchomości koszt raportu”) nie wykazało w tym przebiegu dedykowanego produktu AI, więc jakieś miejsce jest. Ale nie przechodzi testu modeli lokalnych: księgi i plany zagospodarowania to dane publiczne, więc chmurowy model z czołówki jest dozwolony i lepszy. Poufne są tylko akty i akta kupującego. Odpowiedzialność za przeoczoną hipotekę lub służebność ponosi ten, kto podpisuje raport, więc prawdziwymi kupującymi są notariusze i prawnicy, których obejmuje profil prawniczy. Interfejsy API danych (dostęp do ksiąg, geometria planów zagospodarowania) różnią się też między gminami. Lepiej sprzedawać to jako moduł asystenta prawnego niż jako samodzielny biznes.

**Źródła:** [EKW+](https://ekw.plus/) · [Bing search: AI land register analysis](https://www.bing.com/search?q=sztuczna+inteligencja+analiza+ksiąg+wieczystych+aplikacja) · [Eurostat AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

### Agent do dokumentacji dopłat rolniczych

Pomysł: agent przygotowujący wnioski do ARiMR (płatności obszarowe, ekoschematy, pomoc doraźna, taka jak nabór pomocy do nawozów i oleju napędowego, który ruszył 1.10.2026 z terminem 23.10, według wyników wyszukiwania) oraz ewidencję gospodarstwa dla rolników i doradców ODR. **Wynik: 54** (M11 G16 C10 L8 F5 R4).
Dlaczego nie przechodzi kontry: ARiMR już wstępnie wypełnia wniosek w eWniosekPlus danymi działek i map, a państwowe ośrodki doradztwa rolniczego pomagają w tym bezpłatnie lub za niewielką opłatę, więc płatna luka jest cienka. Skłonność rolników do płacenia za oprogramowanie jest niska, a sprzedaż odbywa się offline i sezonowo. Wyszukiwania narzędzi AI do polskich wniosków o dopłaty rolnicze (Bing, 14.10.2026) zwróciły tylko ogólne narzędzia czatu, więc konkurencja jest niska. Ale agencja kontroluje formularz, może go zmieniać co roku i może dodać własnego asystenta. Modele lokalne pomagają w prywatności danych gospodarstw, ale nie jest to tu mocny powód zakupu. Liczba gospodarstw (około 1,3 mln, z briefu) i liczba wniosków nie zostały zweryfikowane w tej sesji.
**Źródła:** [eWniosekPlus](https://ewniosek.arimr.gov.pl) · [Eurostat – wykorzystanie AI 2025](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/ddn-20251211-2)

### Agenci AI do biura rachunkowego dla niemieckich kancelarii doradztwa podatkowego (Steuerberater)

Pomysł: agenci, którzy wstępnie księgują dokumenty, redagują pisma do klientów i przygotowują zeznania dla niemieckich kancelarii Steuerberater borykających się z brakiem pracowników, działający on-prem ze względu na tajemnicę zawodową. **Wynik: 52** (M15 G12 C6 L10 F4 R5).
Dlaczego nie przechodzi kontry: ekosystem jest zamknięty przez DATEV, spółdzielnię z ponad 40 000 członków i 9000 pracowników (strona firmowa DATEV, odczytana 14.10.2026). Każdy agent musi się integrować z DATEV, a DATEV decyduje, jak wdraża własne funkcje AI.
Startupy AI są już w tej niszy: Taxy.io oferuje przestrzeń roboczą AI do pytań podatkowych i prawnych oraz konektor MCP (strona internetowa, 10.2026), a narzędzia do dokumentów, takie jak Candis, integrują się z DATEV (strona z cennikiem niedostępna w tej sesji).
Dla tego czytelnika kluczowa jest wykonalność: sprzedaż, wsparcie i prawo podatkowe są po niemiecku, a czytelnik sprzedaje po polsku i angielsku. Zaufanie zależy też od lokalnej obecności i sieci izbowych.
Danych z badania o użyciu AI w Kanzleien oraz liczby Steuerberater szukano (strony BStBK, DATEV), ale nie pobrano ich w tej sesji: nie znaleziono.
Lepiej zrobi to niemiecki założyciel; wersja polska (biura rachunkowe) lepiej pasuje do tego czytelnika.

**Źródła:** [DATEV company](https://www.datev.de/web/de/m/ueber-datev/das-unternehmen/) · [Taxy.io](https://www.taxy.io/) · [Eurostat: Use of AI in enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

### Dokumentacja cen transferowych i agent TP-R dla polskich grup średniej wielkości

Pomysł: agent, który przygotowuje szkic lokalnej dokumentacji, opis benchmarkingu i wypełnia raport TP-R na podstawie ksiąg dla polskich spółek w grupach kapitałowych. Wynik: 51 (M7 G10 C8 L12 F6 R8).
Dlaczego nie przechodzi kontry: kupujących jest niewielu (tylko firmy powyżej ustawowych progów transakcji; liczby podmiotów składających nie znaleziono w tym przebiegu), a pracę już kupują od Wielkiej Czwórki i butikowych doradców TP, którzy zachowują odpowiedzialność. Benchmarking wymaga płatnych baz danych spółek, których firma bez zewnętrznego finansowania nie może tanio licencjonować. Wiedza dziedzinowa (wytyczne OECD, polskie progi, schemat TP-R) jest głęboka, a autor jej nie ma, więc czas do MVP jest długi, a cykl sprzedaży biegnie przez dyrektorów finansowych raz w roku. Modele lokalne pasują dobrze (dane finansowe grupy są poufne), ale to nie wystarcza, żeby zrównoważyć mały rynek. Lepiej jako funkcja sprzedawana butikom doradztwa TP niż jako produkt. Szczegółów progów i terminów nie pobrano w tym przebiegu (przekierowanie podatki.gov.pl nie zostało na czas obsłużone).
Źródła: [podatki.gov.pl ceny transferowe](https://www.podatki.gov.pl/ceny-transferowe) · [Eurostat wykorzystanie AI](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

### Raportowanie CBAM i EUDR dla małych importerów

Pomysł: agent zbierający dane o emisjach dostawców (CBAM) oraz geolokalizację i oświadczenia należytej staranności (EUDR) dla małych importerów. Wynik: **51** (M8 G12 C8 L6 F10 R7). Dlaczego nie przechodzi kontry: uproszczenie CBAM z 2025 roku (rozporządzenie (UE) 2025/2083) dodało roczny próg importu 50 ton; materiały Komisji do pakietu Omnibus I oceniały skutek na około 90% importerów zwolnionych przy około 99% emisji nadal objętych (liczby z propozycji z 02.2025, nie pobrano ich ponownie w tym przebiegu, więc traktować jako niezweryfikowane), więc rynek małych firm w większości zniknął; pozostali importerzy są więksi i korzystają z brokerów i platform ESG. Ostateczny reżim CBAM obowiązuje od 1.01.2026 (Komisja Europejska). EUDR ponownie przesunięto: więksi i średni operatorzy od 30.12.2026, mikro i mali od 30.06.2027, z poprawkami upraszczającymi przyjętymi w 12.2024 i 12.2025 (strona KE o EUDR, odczyt 10.2026). Powtarzane opóźnienia sprawiają, że kupujący czekają. Dane to dane dostawców, a nie tajemnice, więc modele lokalne niewiele dodają. Przegląd konkurentów był w tym przebiegu płytki (wyszukiwarki nie zwróciły nic użytecznego); to nie jest wiarygodne twierdzenie „brak konkurenta”.

**Źródła:** [EC CBAM](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en) · [EC CBAM legislation](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-legislation-and-guidance_en) · [EC EUDR](https://environment.ec.europa.eu/topics/forests/deforestation/regulation-deforestation-free-products_en)

### Audyty i naprawy zgodności z Europejskim Aktem o Dostępności

Pomysł: agent audytujący sklepy internetowe i serwisy usługowe pod kątem wymogów EAA (opartych na WCAG), a następnie przygotowujący poprawki i deklarację dostępności. Wynik: **48** (M11 G10 C5 L3 F12 R7). Dlaczego nie przechodzi kontry: w Polsce EAA to ustawa z 26.04.2024 (Dz.U. 2024 poz. 731), w mocy od 28.06.2025; egzekwowanie leży po stronie Prezesa PFRON i organów nadzoru rynku, kary sięgają dziesięciokrotności przeciętnego miesięcznego wynagrodzenia, a usługi oferowane przez mikroprzedsiębiorstwa są wyłączone (tekst ustawy, ELI Sejmu). Zatem punkt odniesienia kar jest niski, a najmniejsze sklepy są poza zakresem. Testowanie dostępności to zatłoczony, dojrzały rynek (skanery automatyczne, dostawcy nakładek, agencje dostępności); konkurentów nie sprawdzano ponownie w tym przebiegu, ale powszechnie wiadomo, że kategoria jest nasycona. Publiczne strony internetowe nie zawierają tajemnic, więc modele lokalne nie dają przewagi (L3).

**Źródła:** [Dz.U. 2024 poz. 731 via Sejm ELI API](https://api.sejm.gov.pl/eli/acts/DU/2024/731/text.pdf)

### Obsługa ofert na marketplace'ach w sprzedaży transgranicznej

Pomysł: agent, który lokalizuje katalogi i prowadzi oferty polskich MŚP sprzedających na Allegro CZ/SK/HU, Amazon EU, Kaufland i eMAG. Wynik: **45** (M12 G6 C4 L5 F11 R7). Odpada w kontrze z powodu nasycenia rynku i luki adopcyjnej: handel internetowy to jedna z bardziej gotowych na AI części gospodarki, same marketplace'y podsuwają sprzedawcom narzędzia do tłumaczeń i ofert, a integratorzy ofert oraz duża liczba generatorów ofert AI już istnieją. Nie udało mi się potwierdzić szczegółów własnych narzędzi tłumaczeniowych Allegro w tym przebiegu (wyszukiwanie zwróciło tylko strony startowe), więc werdykt o nasyceniu opiera się na widocznej liczbie dostawców i motywacjach marketplace'ów, a nie na zmierzonej liczbie. Opisy produktów nie są tajne, więc modele lokalne dają tylko oszczędność kosztów przy dużym wolumenie; API czołowych modeli robią wielojęzyczne teksty lepiej i tanio. Wąska nisza może pozostać w kategoriach obciążonych zgodnością z przepisami (etykiety, karty charakterystyki), ale to nie jest gra na luce adopcyjnej.

**Źródła:** [Eurostat: wykorzystanie AI w przedsiębiorstwach](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises) · [Allegro](https://allegro.pl)
