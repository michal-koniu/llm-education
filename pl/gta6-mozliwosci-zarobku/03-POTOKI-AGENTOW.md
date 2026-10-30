# 03. Co agenty potrafią, a czego nie, oraz projekty potoków

Stan na 30 października 2026. Numery w nawiasach kwadratowych odsyłają do `ZRODLA.md`.

---

## 1. Gdzie „agenty robią wszystko" zawodzi

Pomysł jest kuszący: lokalny zestaw z LLM-ami, TTS, modelami obrazu i wideo, agentami przeglądarkowymi i publikującymi produkuje poradniki, filmy i tłumaczenia całą dobę. Na tym rynku zawodzi w sześciu konkretnych miejscach.

| # | Punkt awarii | Dlaczego | Dowody |
|---|---|---|---|
| 1 | **Agenty nie umieją grać** | GTA 6 jest tylko na konsole i jednoosobowe. Nie ma API ani wydobywania danych z plików na konsoli, a automatyzowanie gry lub dostępu do konta to problem z regulaminem. Każdy fakt o świecie gry musi pochodzić od grającego człowieka albo ze zgłoszeń społeczności | (oficjalne / relacje) [3, 26, 80] |
| 2 | **Platformy wyceniają masową produkcję** | Polityka YouTube'a o „treściach nieautentycznych" celuje w szablonowe, masowo produkowane filmy z małą ilością komentarza. System klastrów podobno zamknął około 130 000 kanałów w sześć miesięcy, oceniając po wspólnych szablonach i infrastrukturze (wdrożenie niepotwierdzone; zgłaszany odsetek cofnięć poniżej 1% jest niezweryfikowany). Jeden zestaw, jeden szablon, wiele kanałów to wzorzec, którego szuka | (oficjalne) [28]; (relacje) [32, 33] |
| 3 | **Wyszukiwarka wycenia masową produkcję** | „Scaled content abuse" w Google obowiązuje „niezależnie od tego, jak powstał" i wymienia automatyczne tłumaczenie scrapowanych treści | (oficjalne) [37] |
| 4 | **Egzekwowanie przez właściciela praw** | Take-Two uderza w „rozgrywkę" generowaną przez AI, fałszywe przecieki, porty i każdego, kto monetyzuje jego IP poza własnym kanałem. Agenty, które remiksują oficjalne zwiastuny lub wymyślają materiał, wpadają w to | (relacje) [22, 23, 25] |
| 5 | **Silniki odpowiedzi zjadają krótkie fakty** | AI Overviews mniej więcej o połowę zmniejszają kliknięcia w zapytaniach faktograficznych. Strony, które tylko podają fakt, są zastępowane przez ten sam rodzaj modelu, którego użyłbyś do ich napisania | (relacje) [38] |
| 6 | **Nasycenie jest symetryczne** | Każdy konkurent ma te same modele. Elden Ring miał 183 670 kanałów streamujących w 3,5 dnia; GTA 6 będzie miało więcej. Tańszy wynik nie zwiększa twojego prawdopodobieństwa, jeśli wynik każdego staje się tańszy. Darmowy auto-dubbing YouTube'a [35] już zlikwidował tłumaczenie jako fosę dla wideo | (relacje) [54]; (szacunek) |

**Co przetrwa te sześć punktów:** agenty wykonujące pracę wokół ludzkiego rdzenia: własnej gry, osądu redakcyjnego i zaufania społeczności. W zalecanej kombinacji agenty mogą przejąć mniej więcej 60-75% godzin (szacunek). Pozostałe 25-40% to to, za co płacą platformy.

### W czym agenty są tu dobre

| Zadanie | Dopasowanie agentów | Uwagi |
|---|---|---|
| Pobieranie i transkodowanie nagrań, wykrywanie scen, OCR tekstu na ekranie | Wysokie | Tylko własny materiał |
| Transkrypcja i streszczanie twoich notatek głosowych | Wysokie | Zamienia sesję gry w ustrukturyzowane notatki |
| Dane ustrukturyzowane: schemat, deduplikacja, walidacja, renderowanie stron z rekordów | Wysokie | Rdzeń W2 |
| Konwersja współrzędnych z pinezek stawianych przez człowieka na współrzędne mapy | Wysokie | Pinezkę stawia człowiek; agent ją normalizuje |
| Szkice scenariuszy i tekstu poradników **ze zweryfikowanych rekordów i twoich notatek** | Średnio-wysokie | Nigdy z pamięci modelu: gra jest nowa, więc pamięć modelu o niej jest domyślnie błędna |
| Tłumaczenie ze stałym glosariuszem, napisy, hreflang | Wysokie | Wymaga próbkowej weryfikacji przez native speakera |
| Miniatury i warianty tytułów z własnych klatek | Średnie | Bez oficjalnej grafiki reklamowej i logo |
| Wstępne montaże, rozdziały, kandydaci na Shorts | Średnio-wysokie | Człowiek wybiera i zatwierdza |
| Boty przyjmujące zgłoszenia społeczności, moderacja, wykrywanie duplikatów | Wysokie | W granicach regulaminu Discorda |
| Analityka, śledzenie pozycji, monitorowanie zmian zasad | Wysokie | Obserwuj strony z zasadami, nie tylko ruch |
| Skrypty Lua / JS do FiveM (P3) | Wysokie | Testuj na lokalnym serwerze |
| Granie, ocena spoilerów, głos, zaufanie, odpowiedzi prawne | **Brak lub niskie** | Człowiek |

### Do czego agentów nie wolno używać

- Tworzenia lub „rozgrzewania" wielu kont, kupowania lub fałszowania wyświetleń, głosów, recenzji lub komentarzy.
- Publikowania treści promocyjnych na Reddicie, serwerach Discorda lub forach w dużej ilości. Regulaminy społeczności i filtry spamu traktują to jako spam, a jeden ban może kosztować cię społeczność potrzebną do danych.
- Scrapowania poradników, map lub wiki konkurentów i przepisywania ich.
- Logowania się na konta Rockstara graczy ani jakiegokolwiek zautomatyzowanego dostępu do usług Rockstara.
- Automatycznego składania zamówień w sklepach.
- Generowania „materiału z GTA 6", renderów postaci podawanych za prawdziwe ani fałszywych przecieków.
- Klonowania głosów postaci GTA lub ich aktorów głosowych ani generowania wizerunku prawdziwych członków obsady. Wytyczne dla modów zakazują występów głosowych Rockstara i wizerunku prawdziwych osób bez zgody [10, 11]; mając pod ręką model TTS, to najbardziej kuszące naruszenie.
- Prowadzenia konkursów „darmowy kod GTA 6" lub „klucz do bety PC" w celu zdobywania obserwujących ani żadnego konkursu, którego nie możesz zrealizować.
- Nazywania serwisu, kanału, domeny lub aplikacji z „GTA" lub „Grand Theft Auto".

---

## 2. Zalecana kombinacja

**Rdzeń (okno premiery):**

1. **W2: mapa i tracker znajdziek** jako trwały zasób.
2. **V1: kanał z poradnikami na YouTube prowadzony przez człowieka** jako silnik publiczności i źródło nagrań, które zasilają też W2.
3. **W3: wersje lokalizowane** obu: strony w 3, potem 6-8 językach; auto-dubbing YouTube sprawdzany przez człowieka.
4. **W5: darmowy Discord** jako kanał przyjmowania danych od społeczności; płatny poziom później.
5. **V2: Shorts** wycinane z każdego długiego filmu, tylko jako lejek.
6. **C1: linki afiliacyjne do sprzętu**, oznaczone, na stronie i w opisach, tylko w oknie od Black Friday do stycznia.

**Silnik gotówkowy (wybierz jeden; to opcja nr 1 lub 2 według reguły wyboru z `02`):**

- Domyślnie: **S1, usługi dla twórców**: napisy, tłumaczenia, wycinki do Shorts i miniatury dla innych twórców GTA, sprzedawane z tego samego potoku (A1, A7, A9). Zacznij w tygodniu 3, gdy twoje własne nagrania premierowe zwolnią.
- Jeśli programujesz: **S3, freelancowe usługi dla FiveM** od razu, a **P3, własne skrypty do FiveM** od miesiąca 2 lub 3. Niezależne od premiery GTA 6; ustawia cię na platformę dla twórców z lat 2027-2028.
- Jeśli piszesz i wolisz pewność: **S2**, freelancowe poradniki lub wideo dla wydawcy. Najwyższe prawdopodobieństwo (Prob 4), ale najmniejsza dźwignia agentów. Sprawdź, czy umowa nie przejmuje twoich własnych danych.

**Dlaczego ta mieszanka (szacunek):**
- Kanał i tracker mają **wspólny wysiłek nagrywania**: każda sesja gry daje wideo, rekordy danych i zrzuty ekranu.
- Tracker to część, którą AI Overviews i nasycenie ranią najmniej, i część, w której agenty pomagają najbardziej.
- Lokalizacja mnoży oba, przy bliskim zeru koszcie krańcowym na lokalnym zestawie.
- Silnik gotówkowy płaci coś nawet wtedy, gdy kanał i serwis zostaną w wariancie niskim, który dla nich jest najbardziej prawdopodobny.

### Oczekiwany wynik kombinacji

Jeden operator, nowy uczestnik, średnia z miesięcy 4-12, netto. Wszystkie kwoty to szacunki zbudowane z zakresów i wag dla poszczególnych opcji z `02-OPCJE-Z-OCENA.md`, a nie zgłoszone wyniki.

**Wyprowadzenie.**
- Rdzeń (W2 + V1 + W3 + W5 + V2 + C1): W2 osiąga scenariusz bazowy w około 24% przypadków, V1 w około 22%. Gdyby były niezależne, P(co najmniej jedno) = 1 − 0,76 × 0,78 ≈ 41%. Są dodatnio skorelowane (rosnący kanał karmi serwis; oba zawodzą, gdy nisza jest źle dobrana), więc przyjmij **≈ 35%**. Wariant wysoki któregokolwiek z nich (5% i 4%) daje ≈ 7% szans, że rdzeń osiągnie 3500 $ i więcej.
- Silnik gotówkowy (S1): 38% samodzielnie; prowadzony na część etatu od tygodnia 3, przyjmij ≈ 30%, mniej więcej niezależnie od rdzenia. P(rdzeń lub S1 osiąga bazę) = 1 − 0,65 × 0,70 ≈ **55%**.

| Łączny netto / miesiąc (m4 do 12) | Netto w 12 miesięcy | Tylko rdzeń | Rdzeń + S1 |
|---|---|---|---|
| Poniżej $400 | -$1,500 do $3,000 | ~65% | ~45% |
| $400 do $3,500 | $3,000 do $30,000 | ~28% | ~45% |
| $3,500 do $10,000 | $25,000 do $80,000 | ~5% | ~7% |
| Powyżej $10,000 | $80,000 do $250,000 | ~2% | ~3% |

Przedziały obejmują każdy wynik, a każda kolumna sumuje się do 100%. Wagi zakładają zaangażowanie czasowe z `02` §1; przy mniejszej ilości czasu przesuń wagę do pierwszego wiersza.

---

## 3. Projekt potoku

### 3.1 Przegląd

```
 CZŁOWIEK: gra + nagrywanie + notatki głosowe
        |
        v
 [A1 Ingest] --> [A2 Bramka zasad/spoilerów] --(flagi)--> BRAMKA H2
        |                                                 |
        v                                                 v
 [A3 Budowa rekordów] <-- [A4 Bot zgłoszeń społeczności] <-- zgłoszenia z Discorda
        |
        +--> BRAMKA H3 (weryfikacja nowych typów; próbki pozostałych)
        |
        v
 Magazyn danych (rekordy, współrzędne, zrzuty, status)
        |                         |                          |
        v                         v                          v
 [A5 Budowa serwisu]      [A6 Szkic scenariusza]     [A9 Lokalizator]
        |                         |                          |
        v                         v                          v
 Tracker + strony          BRAMKA H4 (głos,           BRAMKA H5
 (auto-publikacja,          rekord, edycja,           (próbka native)
  jeśli zweryfikowane)      akceptacja)                      |
        |                         |                          |
        |                         v                          |
        |                  [A7 Pomoc w montażu] --> [A8 Publikacja] <---+
        |                         |
        v                         v
 [A10 Monitor: analityka, pozycje, strony z zasadami, skrzynka roszczeń, dostępność]
        |
        v
 [A11 Selekcja komentarzy i opinii] --> poprawki z powrotem do A3
                                    --> BRAMKA H6 (roszczenia, prawo, pieniądze)
```

### 3.2 Agenty

| Agent | Co robi | Wejścia | Wyjścia | Twarde limity |
|---|---|---|---|---|
| **A0 Orkiestrator** | Kolejkuje zadania, ponawia, pilnuje budżetów kosztów i czasu, dzienny raport | Stany wszystkich agentów | Graf zadań, dzienne podsumowanie dla człowieka | Brak własnych uprawnień do publikacji |
| **A1 Ingest** | Transkoduje nagrania, wykrywa sceny, OCR HUD-u i tekstu na ekranie, transkrybuje twoje notatki głosowe, znaczniki czasu | Surowe nagrania, notatki głosowe | Klipy, klatki, transkrypt, kandydackie zdarzenia („podniesienie znajdźki w 00:41:12") | Tylko własny materiał |
| **A2 Bramka zasad i spoilerów** | Klasyfikuje fragmenty: przerywnik fabularny, zakończenie, ujawnienie w misji, przemoc w pierwszych ~15 sekundach, surowe przebiegi przerywników | Klipy, transkrypt, lista kontrolna zasad | Przepuść / oflaguj / zablokuj, z uzasadnieniem | Nie może zatwierdzać własnych flag; wszystko oflagowane idzie do H2 |
| **A3 Budowa rekordów** | Zamienia zdarzenia i zgłoszenia w rekordy: typ, nazwa, współrzędne, zrzut, warunki, flaga „do przegapienia", pewność, źródło | Zdarzenia z A1, zgłoszenia z A4, pinezki człowieka | Szkice rekordów | Rekord bez zweryfikowanego przez człowieka źródła pozostaje „niezweryfikowany" i nie jest pokazywany jako fakt |
| **A4 Bot zgłoszeń społeczności** | Formularz na Discordzie na zgłoszenia, kontrola obrazów, wykrywanie duplikatów względem istniejących rekordów, uznanie dla zgłaszającego, ochrona przed spamem | Discord | Kolejka zgłoszeń | Przestrzega regulaminu Discorda i serwera; żadnych wiadomości prywatnych do nie-członków |
| **A5 Budowa serwisu** | Renderuje interfejs trackera i jedną stronę na rekord z szablonów, znaczniki schema, mapy witryny, linkowanie wewnętrzne, wdrożenie | Zweryfikowane rekordy | Statyczny serwis i tracker | Strony tylko dla rekordów z prawdziwymi danymi; bez stron-wypełniaczy; tempo publikacji ograniczone (zob. 3.4) |
| **A6 Szkic scenariusza** | Pisze szkice scenariuszy wideo i tekstów poradników **z rekordów i twojego transkryptu**, z identyfikatorami rekordów cytowanymi w tekście | Rekordy, transkrypt, zarys | Szkic scenariusza | Nigdy nie dodaje faktów, których nie ma w rekordzie lub transkrypcie |
| **A7 Pomoc w montażu** | Wstępny montaż według zatwierdzonego scenariusza, rozdziały, napisy, nakładki map z rekordów, warianty miniatur i tytułów z twoich klatek, kandydaci na Shorts | Zatwierdzony scenariusz, klipy | Plik projektu, warianty | Bez oficjalnej grafiki reklamowej, logo ani materiału ze zwiastunów |
| **A8 Publikacja** | Wysyła, planuje, ustawia metadane, włącza przegląd auto-dubbingu, publikuje Shorts | Pakiety zatwierdzone przez człowieka | Opublikowane filmy | Publikuje tylko pakiety z tokenem akceptacji H4 |
| **A9 Lokalizator** | Tłumaczy strony i napisy według stałego glosariusza nazw z gry; hreflang; oznacza fragmenty o niskiej pewności | Zatwierdzona wersja angielska | Zlokalizowane strony, pliki napisów | Próbka każdej partii trafia do H5, zanim język zostanie uruchomiony; potem kontrole wyrywkowe |
| **A10 Monitor** | Analityka, śledzenie pozycji, dostępność, postęp w Partner Program względem terminu 31 stycznia 2027, **różnice na stronach z zasadami** (polityka wideo i modów Rockstara, monetyzacja YouTube, polityka spamowa Google, warunki Tebex/Cfx), skrzynka roszczeń i ostrzeżeń | API, migawki stron | Cotygodniowy raport, natychmiastowe alerty o roszczeniach lub zmianach zasad | Tylko do odczytu |
| **A11 Selekcja opinii** | Klasyfikuje komentarze i wiadomości: poprawka, pytanie, spam, nadużycie | Komentarze, Discord, e-mail | Poprawki do A3, kandydaci do FAQ, działania moderacyjne | Eskaluje do H6 wszystko prawne, finansowe lub osobiste |
| **A12 Programista FiveM** (zabezpieczenie, P3) | Pisze i testuje skrypty Lua/JS na lokalnym serwerze FiveM, dokumentacja, changelogi, szkice odpowiedzi dla wsparcia | Specyfikacja produktu od człowieka | Buildy, dokumentacja | Nigdy nie buduje zakazanej monetyzacji (loot boxy, sprzedaż waluty); człowiek sprawdza przed wydaniem |

### 3.3 Bramki ludzkie

| Bramka | Kiedy | Czas dziennie (szacunek) | O czym decyduje człowiek |
|---|---|---|---|
| **H1 Gra i nagrywanie** | Każda sesja | 1,5-2 h przy premierze, 0,5-1 h później | Co nagrać; nagrywa notatki głosowe; stawia pinezki na mapie |
| **H2 Spoilery i zasady** | Każdy oflagowany fragment | 10-20 min | Zostawić, rozmyć, wyciąć lub opóźnić |
| **H3 Weryfikacja danych** | Każdy nowy typ pozycji; próbka pozostałych; każdy rekord społeczności, zanim zostanie oznaczony jako zweryfikowany | 15-30 min | Prawda czy fałsz; pewność |
| **H4 Głos i akceptacja** | Każdy długi film | 30-60 min | Narracja (własny głos albo ujawniony głos syntetyczny z własnymi poprawkami scenariusza), końcowy montaż, tytuł, miniatura |
| **H5 Weryfikacja native** | Pierwsza partia każdego języka, potem próbki około 10% | Płatni weryfikatorzy, kilka godzin tygodniowo | Zaliczone lub do poprawy |
| **H6 Roszczenia, prawo, pieniądze** | Gdy się pojawią | W miarę potrzeby | Odpowiedzi na usunięcia lub roszczenia; umowy ze sponsorami i ich ujawnienie; płatne poziomy; wszystko, co dotyczy płatności |
| **H7 Przegląd tygodniowy** | Raz w tygodniu | 30-60 min | Czytanie raportu A10; korekta planu; stosowanie kryteriów porzucenia (plik 04) |

**Razem:** około 2,5-4 h dziennie przy premierze na H1-H4, plus odpowiedzi dla społeczności, co daje 3-4,5 h dziennie założone w `02` §1. Silnik gotówkowy (S1, S3 lub S2) dodaje 0,5-1 h dziennie od tygodnia 3. Zob. budżet w pliku 04.

### 3.4 Zabezpieczenia wbudowane w potok

1. **Brak rekordu, brak strony.** A5 może renderować tylko stronę popartą zweryfikowanym rekordem albo oryginalnym poradnikiem napisanym przez człowieka. To trzyma serwis z dala od „scaled content abuse" [37].
2. **Limity tempa publikacji.** Stron dziennie tyle, ile rekordów zweryfikowano tego dnia. Żadnego masowego generowania stron.
3. **Jeden kanał, jeden głos.** Nie klonuj kanału na wiele kanałów językowych ani niszowych prowadzonych z tego samego szablonu. Zamiast tego używaj auto-dubbingu i napisów na kanale głównym [33, 35].
4. **Pamięć modelu nie jest źródłem.** Gra jest nowa. A6 i A9 pracują wyłącznie na rekordach i transkryptach. Wszystko inne to domyślnie halucynacja.
5. **Tylko własne zasoby.** Twoje nagrania, mapa narysowana z własnych obserwacji (nie odrysowana z mapy w grze ani z oficjalnej grafiki, co prawdopodobnie jest utworem zależnym i nadal ryzykiem zgłoszenia naruszenia), twoje ikony. Żadnych wyciągniętych tekstur, żadnej oficjalnej grafiki ani logo, linijka o braku powiązania na każdej stronie i żadnego „GTA" w nazwie marki, domeny ani aplikacji.
6. **Płatne poziomy sprzedają funkcje, nigdy materiał.** Tylko synchronizacja, brak reklam, wczesny dostęp do narzędzi i role w społeczności. Żadnych filmów, zrzutów ani galerii z GTA za paywallem [14].
7. **Ujawnienie.** Sponsoring i linki afiliacyjne są oznaczane jako reklama w filmie, opisie i na stronie.
8. **Polityka spoilerów jako kod.** A2 sprawdza przypadki, które Rockstar usuwa: wyizolowane przerywniki, zakończenia, surowe oficjalne wideo [14, 15]. Poradniki fabularne mają ostrzeżenia o spoilerach i rozdzielenie rozdziałów.
9. **Ujawnienie użycia AI.** Oznaczaj głos syntetyczny lub obrazy generowane przez AI tam, gdzie wymagają tego platformy. YouTube i tak nakłada własne etykiety [31].
10. **Zmiany zasad to alerty.** A10 co tydzień robi migawki stron z zasadami; każda zmiana powiadamia człowieka. Zasady zmieniały się kilkakrotnie w latach 2025-2026.

### 3.5 Stos technologiczny

Trzymaj prosto: konsola i karta przechwytująca; lokalne ASR, OCR, średni LLM do szkiców i klasyfikacji, model tłumaczeniowy oparty na glosariuszu, model obrazu do teł miniatur z własnych klatek; rekordy w bazie danych lub JSON/GeoJSON z polami statusu i źródła; statyczny serwis z trackerem po stronie klienta; jeden Discord z botem do zgłoszeń; kolejka zadań, która przed każdym krokiem publikacji sprawdza tokeny akceptacji. Niezawodność w tygodniu premiery ma większe znaczenie niż funkcje.

---

## 4. Warianty potoków

### 4.1 Usługi dla twórców (S1)

Te same agenty A1, A7, A9, skierowane na materiał klienta. Bramki ludzkie: zakres prac z klientem, polityka spoilerów per klient, akceptacja końcowej dostawy. Cena za film lub za miesiąc. Nie używaj materiału ani danych klienta we własnych zasobach bez pisemnej umowy.

### 4.2 Sklep ze skryptami do FiveM (P3)

A12 buduje i testuje na lokalnym serwerze; człowiek pisze specyfikację, wybiera lukę rynkową, sprawdza kod i UX oraz prowadzi wsparcie. A10 obserwuje warunki Creator Platform i strony z prowizjami Tebex. Używaj asset escrow platformy. Sklep zawiera wymaganą linijkę o braku poparcia [16].
