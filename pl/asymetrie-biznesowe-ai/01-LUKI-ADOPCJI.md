# Gdzie adopcja AI jest wciąż niska

Ten rozdział to baza dowodowa całego kursu. „Asymetria" istnieje tam, gdzie kupujący wciąż płacą ludziom za
powolną ręczną pracę, mimo że AI, które mogłoby ją wykonać, jest już tanie. Poniższe dane pokazują, gdzie tak jest:
według krajów, wielkości firm, sektorów oraz powodów, dla których firmy nie wdrażają AI.

Wszystkie dane o przedsiębiorstwach pochodzą z unijnego badania wykorzystania ICT (zbiory Eurostatu `isoc_eb_ai`
i `isoc_eb_ain2`), obejmującego przedsiębiorstwa zatrudniające 10 lub więcej osób, ze wszystkich sektorów poza
rolnictwem, górnictwem i finansami, o ile nie zaznaczono inaczej. Pobrałem je z API Eurostatu 14.10.2026; zbiór był
ostatnio aktualizowany 15.06.2026. **Najnowsze jest badanie z 2025 roku; wartości za 2026 nie były opublikowane w
momencie pisania.** Mikrofirm (poniżej 10 osób) nie ma w głównych liczbach dla UE.

## 1. Europa: trzykrotna różnica między północą a wschodem

Odsetek przedsiębiorstw używających co najmniej jednej technologii AI (wskaźnik `E_AI_TANY`), lata 2023-2025
([Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table)):

| Kraj | 2023 | 2024 | 2025 | Uwaga |
|---|---|---|---|---|
| Dania | 15,2% | 27,6% | 42,0% | najwyżej w UE |
| Finlandia | 15,1% | 24,4% | 37,8% | |
| Szwecja | 10,4% | 25,1% | 35,0% | |
| Holandia | 14,1% | 23,1% | 33,2% | |
| Niemcy | 11,6% | 19,8% | 26,0% | |
| **Średnia UE-27** | 8,1% | 13,5% | **20,0%** | |
| Francja | 5,9% | 9,9% | 18,2% | |
| Czechy | 5,9% | 11,3% | 17,6% | |
| Włochy | 5,1% | 8,2% | 16,4% | |
| Węgry | 3,7% | 7,4% | 10,4% | |
| Grecja | 4,0% | 9,8% | 8,9% | |
| Bułgaria | 3,6% | 6,5% | 8,6% | |
| **Polska** | 3,7% | 5,9% | **8,4%** | drugie najniższe w UE |
| Rumunia | 1,5% | 3,1% | 5,2% | najniższe w UE |

Co to znaczy:
- Adopcja w Polsce wzrosła z 3,7% do 8,4% w dwa lata, ale UE rosła szybciej, więc **różnica powiększyła się z 4,4 do
  11,6 punktu procentowego** (2023-2025). Średnia UE jest 2,4 raza wyższa niż w Polsce.
- Polska jest poniżej każdego sąsiada z Europy Środkowej: Czechy 17,6%, Słowacja 18,0%, Litwa 21,3% (2025).
- Około **91,6% polskich firm zatrudniających 10+ osób nie używało w 2025 roku żadnego AI**; tylko 4,3% firm, które
  go nie używały, w ogóle rozważało jego użycie (UE: 14,2%)
  ([Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table)).

### Według wielkości firmy (2025)

| Klasa wielkości | UE-27 | Polska | UE / PL |
|---|---|---|---|
| Małe (10-49 osób) | 17,0% | 5,8% | 2,9x |
| Średnie (50-249) | 30,4% | 14,8% | 2,1x |
| Duże (250+) | 55,0% | 45,8% | 1,2x |
| Wszystkie 10+ | 20,0% | 8,4% | 2,4x |

Źródło: [Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table), 2025.

Asymetria to **problem małych i średnich firm**. Duże polskie firmy są blisko poziomu UE (45,8% wobec 55,0%). Małe
polskie firmy mają 5,8%, mniej więcej tyle, ile wynosiła średnia UE w 2023 roku. To segment, na który celuje ten
kurs.

## 2. Polska w szczegółach

**GUS (Główny Urząd Statystyczny).** Coroczny raport „Społeczeństwo informacyjne w Polsce w 2025 r." (Warszawa
i Szczecin, 2025) podaje ([GUS PDF](https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultaktualnosci/5497/1/19/1/spoleczenstwo_informacyjne_w_polsce_2025.pdf)):
- 8,7% przedsiębiorstw używało AI w 2025 roku (GUS liczy nieco szerszy zestaw sektorów niż główna liczba Eurostatu,
  stąd 8,7% wobec 8,4%).
- Najwyżej: duże firmy 42,0% oraz sekcja „Informacja i komunikacja" 37,8%.
- Najniżej: małe firmy 6,1% i **budownictwo 2,6%**.
- Według regionów: mazowieckie 12,5% (najwyżej), warmińsko-mazurskie 5,1% (najniżej).
- 91,3% firm nie używało AI; tylko 3,9% nie używało go, ale rozważało użycie.
- W administracji publicznej AI używało w 2024 roku 6,8% jednostek (administracja rządowa 24,1%, samorządowa 6,1%).

**Inne polskie badania różnią się co do poziomu, nie co do kierunku.** Przegląd Polskiego Instytutu Ekonomicznego
(PIE) „AI w polskich przedsiębiorstwach" (komunikat prasowy z 24.09.2025) szacuje wykorzystanie AI na „od prawie 6 do
16 procent firm w zależności od metody"; dane PIE i Ministerstwa Rozwoju i Technologii (MRiT) pokazują, że 16% mikro-
i 15% małych firm używa narzędzi AI, a **77% firm niestosujących AI nie planuje jej wdrażać „dopóki nie stanie się to
konieczne"**. Prawie 90% firm, które nie planują wdrożenia, jest w całości polskich. PIE zauważa też, że użycie AI
często zaczyna się oddolnie, od pracowników, więc rzeczywiste użycie (pracownicy na darmowych czatbotach) jest
prawdopodobnie wyższe niż oficjalne liczby
([PIE, 24.09.2025](https://pie.net.pl/wp-content/uploads/2025/09/2025-09-22_Z-AI-korzysta-mniej-niz-co-szosta-firma-w-Polsce-a-pozostale-nie-planuja-jej-wdrazac-1.pdf)).
*(szacunek zewnętrzny)* dla liczb PIE/MRiT; metoda różni się od GUS.

Moja interpretacja: pojedynczy pracownicy polskich MŚP już wklejają tekst do ChatGPT, ale **firmy nie kupiły ani nie
wbudowały AI w swoje procesy**. Luka dotyczy automatyzacji na poziomie procesów, nie świadomości.

**Do czego używają jej nieliczni polscy adopterzy (2025, odsetek firm używających AI).** Administracja i zarządzanie
firmą 42,9% (UE 31,0%), księgowość i finanse 30,7% (UE 23,1%)
([Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table)). Polscy adopterzy
zaczynają od zastosowań w back office, co wspiera agentów back-office jako punkt wejścia.

**Analiza tekstu to największa luka.** Tylko 2,1% polskich firm używa AI do eksploracji tekstu (text mining), wobec
11,8% w UE (2025), czyli luka 5,6-krotna
([Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table)). Czytanie
dokumentów, czyli to, co agenci robią dziś dobrze, jest w Polsce najmniej adoptowaną technologią AI w porównaniu z UE.

**Polska polityka AI w skrócie.**
- **PLLuM**: finansowana przez rząd polska rodzina modeli LLM, opublikowana na Hugging Face przez organizację
  Ministerstwa Cyfryzacji `CYFRAGOVPL` (np. [PLLuM-12B-instruct-2512](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512));
  licencje różnią się w zależności od modelu (część jest niekomercyjna), więc sprawdzaj każdą kartę modelu. Model
  napędza asystenta w aplikacji mObywatel
  ([iMagazine, 02.01.2026](https://imagazine.pl/2026/01/02/mobywatel-wchodzi-w-2026-rok-z-polskim-ai/)).
- **Bielik**: model stworzony przez społeczność SpeakLeash, rodzina v3, w tym
  [Bielik-11B-v3.0-Instruct](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct) (Apache-2.0 według jego
  karty modelu) ([bielik.ai](https://bielik.ai/)).
- **Fabryki AI**: EuroHPC wymienia dwie polskie fabryki AI (AI Factories), **PIAST** i **Gaia**; projekt Gaia „ma na
  celu przyspieszenie rozwoju i zwiększenie adopcji najnowocześniejszych technologii AI w Polsce"
  ([EuroHPC AI Factories](https://www.eurohpc-ju.europa.eu/ai-factories_en), odczytano 14.10.2026). Budżety,
  lokalizacje i warunki dostępu dla MŚP: nie zweryfikowano w tej sesji.

Dla dostawcy polityka ma znaczenie w jednym aspekcie: istnieją już polskojęzyczne modele otwarte z użytecznymi
licencjami, więc „po polsku, on-prem, żadne dane nie wychodzą z biura" to produkt możliwy do zbudowania, nie hasło.
Rozdział `03-NAJPIERW-LOKALNIE.md` omawia to szerzej.

## 3. Według sektorów: kto używa AI najmniej

Odsetek przedsiębiorstw używających AI, 2025, wybrane sekcje NACE
([Eurostat isoc_eb_ain2](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ain2/default/table)):

| Sektor (NACE) | UE-27 | Polska | Komentarz |
|---|---|---|---|
| Budownictwo (F) | 10,8% | 2,4% | najniżej w obu; ogromny ciężar papierologii |
| Transport i gospodarka magazynowa (H) | 11,2% | 3,0% | dokumenty frachtowe, dyspozytura, odprawy celne |
| Obsługa rynku nieruchomości (L) | 24,8% | 4,1% | 6-krotna luka wobec UE |
| Produkcja żywności (C10-C12) | 12,5% | 5,0% | |
| Zakwaterowanie i gastronomia (I) | 12,0% | 5,6% | |
| Handel pojazdami i ich naprawa (G45) | 14,4% | 5,9% | |
| Gospodarka odpadami i wodna (E) | 13,1% | 6,0% | |
| Handel detaliczny (G47) | 15,5% | 7,1% | |
| Przetwórstwo przemysłowe, ogółem (C) | 17,3% | 7,7% | |
| Handel hurtowy (G46) | 23,4% | 11,2% | |
| Prawo, księgowość, doradztwo (M69-M71) | 37,9% | 20,5% | wysoko, ale wciąż połowa poziomu UE |
| Działalność profesjonalna, naukowa, techniczna (M) | 40,4% | 22,2% | |
| Informacja i komunikacja (J) | 62,5% | 38,1% | |
| Programowanie i usługi IT (J62-J63) | 65,7% | 42,0% | najwyżej |

Wzorce:
- **Nisko wszędzie**: budownictwo, transport, zakwaterowanie i gastronomia, tradycyjny przemysł. Te sektory są niskie
  w całej UE, nie tylko w Polsce, więc produkt zbudowany dla nich może sprzedawać się na obu rynkach.
- **Nisko tylko w Polsce**: nieruchomości (4,1% wobec 24,8%) oraz prawo i księgowość (20,5% wobec 37,9%). To branże
  dokumentowe, w których UE już pokazuje popyt, więc polska luka prawdopodobnie się zamknie; pytanie brzmi, kto ją
  zamknie.
- **ICT jest nasycone**: firmy IT używają już AI na poziomie od 42% do 66%. Sprzedawanie AI firmom IT oznacza
  konkurowanie z własnymi inżynierami kupującego.

## 4. Porównanie globalne

- **Stany Zjednoczone (Census Bureau BTOS).** Badanie Census Business Trends and Outlook Survey pyta firmy co dwa
  tygodnie, czy używały AI do wytwarzania towarów lub usług ([Census BTOS](https://www.census.gov/hfp/btos/data)).
  Nie udało mi się w tej sesji pobrać aktualnego wskaźnika, więc nie podaję tu liczby; aktualną wartość odczytaj na
  tej stronie. Zauważ, że BTOS obejmuje firmy wszystkich wielkości, w tym mikrofirmy, i używa innego pytania, więc
  nie jest bezpośrednio porównywalny z Eurostatem.
- **Badania dużych firm** (McKinsey „The State of AI",
  [mckinsey.com](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai); raporty
  Microsoftu o dyfuzji AI) w większości badają próbę dużych firm lub indywidualnych użytkowników i podają znacznie
  wyższe wykorzystanie. Nie udało mi się w tej sesji załadować ich aktualnych edycji: nie zweryfikowano, więc nie
  cytuję żadnych liczb.
- **Spójny wzorzec** w danych, które mogłem zweryfikować: duże firmy adoptują 2 do 3 razy więcej niż małe (UE 55,0%
  wobec 17,0%, Polska 45,8% wobec 5,8%, Eurostat 2025). Nagłówkowe liczby „większość firm używa AI" opisują duże
  firmy i indywidualnych pracowników, nie procesy małych firm. Nie używaj ich do szacowania rynku MŚP.

## 5. Dlaczego firmy nie wdrażają AI i co każda bariera oznacza dla dostawcy

Eurostat pyta firmy, które **rozważały AI, ale jej nie użyły**, dlaczego. Odsetki tych firm, 2025
([Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table), jednostka „% of
enterprises which ever considered AI"):

| Bariera | UE-27 | Polska | Co może zaoferować dostawca aplikacji agentowej |
|---|---|---|---|
| Brak odpowiedniej wiedzy | 70,3% | 62,6% | Usługa „pod klucz": dostawca konfiguruje, uruchamia i utrzymuje; kupujący nigdy nie „uczy się AI" |
| Brak jasności co do skutków prawnych | 53,6% | 52,3% | Papierologia AI Act i RODO w pakiecie: szablon DPIA, log audytowy, krok zatwierdzenia przez człowieka |
| Obawy o ochronę danych i prywatność | 52,7% | 49,4% | Modele lokalne na urządzeniu u klienta lub w polskim/unijnym centrum danych; żadnych danych do chmur amerykańskich |
| Dostępność lub jakość danych | 43,5% | 33,4% | Start od dokumentów, które już mają (PDF, skany, e-mail), a nie od projektu danych |
| Niezgodność z istniejącymi systemami | 41,6% | 40,9% | Integracja z polskimi narzędziami (KSeF, Subiekt, Optima, Symfonia) albo praca przez e-mail i pliki |
| Koszty wydają się zbyt wysokie | 38,4% | **55,5%** | Stała cena miesięczna, wycena za dokument, tania inferencja lokalna przy dużym wolumenie |
| Względy etyczne | 24,6% | 26,6% | Człowiek w pętli, wyjaśnialne projekty, brak autonomicznych decyzji dotyczących ludzi |
| AI nie jest przydatna dla biznesu | 17,8% | **34,6%** | Sprzedawaj zmierzony rezultat (zaoszczędzone godziny, przetworzone faktury), a nie „AI" |

Dwie polskie różnice mają znaczenie dla wyceny i sprzedaży:
- **Koszt jest drugą barierą w Polsce (55,5%), ale szóstą w UE (38,4%).** Polskie MŚP są wrażliwe na cenę;
  inferencja lokalna, która utrzymuje koszt krańcowy blisko zera, to argument sprzedażowy, nie tylko dotyczący
  prywatności.
- **Co trzeci polski respondent, który rozważał AI, uważa ją za „nieprzydatną"** (34,6% wobec 17,8% w UE).
  Sprzedawaj zadanie, nie technologię. W połączeniu z wynikiem PIE „77% nie wdroży, dopóki nie będzie to konieczne"
  polskie cykle sprzedaży będą wymagały dowodu na własnych dokumentach kupującego.

Zastrzeżenie: tylko 4,3% polskich firm niestosujących AI kiedykolwiek ją rozważało, więc te odsetki opisują małą
grupę. Pozostałe około 87% firm w ogóle o niej nie myślało, co jest zarazem szansą i problemem sprzedażowym.

## 6. Gdzie AI jest już nasycona: unikaj

Te kategorie są zapchane globalnymi platformami oraz tanimi lub darmowymi narzędziami. Mały polski dostawca nie ma
tam przewagi (moja ocena, poparta Eurostatem: generowanie języka lub kodu stosuje 8,8% firm w UE, a generowanie
obrazów, wideo lub dźwięku 9,6% w 2025 roku, oba wskaźniki powyżej większości innych technologii AI, a marketing
i sprzedaż to najczęstszy cel użycia AI na poziomie 6,9%
([Eurostat isoc_eb_ai](https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table))):

| Kategoria | Dlaczego unikać |
|---|---|
| Czatboty obsługi klienta na stronach | Wbudowane w każdy helpdesk i CRM; wiele lokalnych agencji czatbotów |
| Teksty marketingowe, posty w mediach społecznościowych, obrazy | Wbudowane w narzędzia Canva, Google, Meta i Microsoft; darmowe plany |
| Asystenci kodowania | Zdominowani przez czołowe laboratoria i dostawców IDE; firmy ICT już na poziomie 42% do 66% użycia AI |
| Notatki ze spotkań i transkrypcja | Wbudowane w Teams, Zoom, Google Meet |
| Generyczne „czat z twoimi dokumentami" | Plany korporacyjne Copilota, ChatGPT i Gemini mają to w standardzie |
| Generyczne tłumaczenia | DeepL i duże platformy; cena towarowa |

Test dla nowego pomysłu: jeśli Microsoft 365 lub Google Workspace już to robi z poziomu menu, to nie jest
asymetria.

## 7. Mapa asymetrii

| Segment | Sygnał adopcji | Główna bariera | Co może zaoferować dostawca agentów |
|---|---|---|---|
| Polskie małe firmy (10-49) ogółem | 5,8% wobec UE 17,0% (2025) | Koszt (55,5% polskich respondentów rozważających AI) | Stała niska cena, inferencja lokalna, brak projektu wdrożeniowego |
| Budownictwo (PL i UE) | 2,4% PL, 10,8% UE (2025) | Wiedza; praca w terenie, dużo papieru | Agenci do przetargów, przedmiarów i dokumentacji budowy, pracujący na e-mailach i skanach |
| Transport i logistyka | 3,0% PL, 11,2% UE (2025) | Niezgodność z TMS i obiegiem papierowym | Ekstrakcja dokumentów frachtowych i celnych do istniejących systemów |
| Nieruchomości (PL) | 4,1% PL wobec 24,8% UE (2025) | Wiedza | Agenci po polsku do ofert, umów najmu i dokumentów zarządzania nieruchomościami |
| Zakwaterowanie i gastronomia | 5,6% PL, 12,0% UE (2025) | Wiedza i koszt | Back office (faktury, zamówienia u dostawców, dokumenty kadrowe), a nie czatboty dla gości |
| Produkcja żywności i tradycyjny przemysł (MŚP) | 5,0% do 7,7% PL (2025) | Ochrona danych, niezgodność systemów | Agenci on-prem do dokumentów jakościowych, zamówień i certyfikatów |
| Prawo i księgowość (PL) | 20,5% PL wobec 37,9% UE (2025) | Jasność prawna, tajemnica zawodowa | Redagowanie i przegląd dokumentów modelem lokalnym ze ścieżką audytu |
| Back office z dużą ilością tekstu (PL) | text mining 2,1% PL wobec 11,8% UE (2025) | Ochrona danych (49,4%) | Agenci czytający dokumenty na lokalnym urządzeniu; zatwierdzenie przez człowieka przed jakąkolwiek akcją |
| Lokalna administracja publiczna (PL) | 6,1% jednostek samorządowych (2024) | Jasność prawna, zamówienia publiczne | Nie pierwszy cel: wolne zamówienia; wróć do tego z klientem referencyjnym |

Jak to czytać: najlepsze komórki łączą **niską zmierzoną adopcję**, **ręczną pracę na dokumentach** i barierę, którą
mały dostawca może usunąć (wiedza, prywatność, koszt). Rozdział `02-OKAZJE.md` zamienia te komórki w punktowane
profile biznesowe; rozdział `03-NAJPIERW-LOKALNIE.md` omawia argument za modelami lokalnymi; architekturę hybrydową
znajdziesz w
[../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md).

## Ograniczenia tych danych

- Eurostat wyklucza firmy poniżej 10 pracowników oraz sektor finansowy; większość polskich firm to mikrofirmy, więc
  prawdziwy obraz dla firm jednoosobowych nie jest tu zmierzony (PIE/MRiT sugerują, że 16% mikrofirm używa jakiegoś
  narzędzia AI).
- „Używa AI" obejmuje firmę, która raz użyła jednego narzędzia. Nie mierzy głębokości; prawdziwa automatyzacja
  procesów jest niższa.
- Dane za 2025 rok zebrano na początku 2025 roku. Adopcja mniej więcej podwajała się co roku w latach 2023-2025,
  więc pod koniec 2026 poziomy są prawdopodobnie wyższe; stabilnym sygnałem są względne luki (PL wobec UE, małe
  wobec dużych, budownictwo wobec ICT).
- Porównań dla USA i dużych firm (sekcja 4) nie dało się zweryfikować w tej sesji.
