# Część 07 · Cennik: ceny, rabaty i warunki na papierze

> **Cel tej części.** Zamieniasz części 02–06 w jeden spisany dokument, **cennik — księgę cen**. Może się na
> niego powołać każda rozmowa, oferta i umowa. Zawiera ceny, to, co obejmuje każda z nich, zasady rabatów,
> warunki płatności i indeksacji oraz marże dla partnerów. Gdy już istnieje, przestajesz wymyślać ceny na
> spotkaniach.
>
> **Czas:** ~4 h · **Poziom:** ⭐⭐⭐ · **Efekt:** `pricing/price-book-v1.md`

> **To nie jest porada prawna.** Przykładowe klauzule poniżej pokazują, *co* klauzula musi osiągnąć.
> Ostateczny tekst umowy niech napisze prawnik — zajmuje się tym kurs o umowach.

---

## 0. Problem

Bez cennika każda cena jest negocjowana od zera, każdy rabat zależy od nastroju, a po dziesięciu klientach masz
dziesięć różnych umów, których nie potrafisz zapamiętać, obronić ani podnieść. Cennik jest dla wyceny tym, czym
manifest wydania dla wdrożenia w `kurs_aplikacje_agentowe/18-WYDANIE-I-UTRZYMANIE.md`: wersjonowanym zapisem
aktualnej prawdy, dzięki któremu decyzje są świadome, a zmiany da się prześledzić.

---

## 1. Co trafia do cennika

```
 price-book-v1.md
 ├─ 1. Pakiety              ceny, co obejmują, dla kogo są
 ├─ 2. Agenci eksperccy     katalog z ceną każdego agenta
 ├─ 3. Opłaty jednorazowe   wdrożenie, pilotaż, dodatkowe szkolenie, wizyta na miejscu
 ├─ 4. Sprzęt               obsługiwane boxy, cztery modele (część 05), „ważne do"
 ├─ 5. Zakres wsparcia      co jest w cenie, czego nie ma, czasy reakcji
 ├─ 6. Warunki handlowe     długość umowy, fakturowanie, termin płatności, indeksacja, wypowiedzenie
 ├─ 7. Polityka rabatowa    kto może dostać co, w zamian za co, i maksimum
 ├─ 8. Warunki partnerskie  marże za polecenie i za odsprzedaż
 └─ 9. Rejestr zmian        wersja, data, co się zmieniło, dlaczego
```

---

## 2. Przykładowy cennik dla segmentu kancelarii prawnych

Liczby poniżej to **ilustracja** spójna z przykładowymi obliczeniami z kursu. Nie są rekomendacją. Zastąp
każdą liczbę wynikami własnych części 02–06 i przy każdej zostaw informację, skąd pochodzi.

Dlaczego te liczby (łańcuch rozumowania, żebyś mógł go powtórzyć na swoich):

- Podłoga kosztowa przy instalacji opłaconej z opłaty wdrożeniowej, 20 kancelarii, marża 60% (`pricing_model.py floor
  --install-h 0`): **833 zł** miesięcznie przy 0,5 h wsparcia, **1 083 zł** przy 1 h.
- Cena Kancelarii K przy przechwyceniu 20% wartości względem chmurowego AI prawniczego (część 03): **1 804 zł**.
- Ilustracyjny przedział Van Westendorpa z próbki z części 06: mniej więcej 600–1 600 zł, IPP w okolicach 1 000 zł.
  (Twój prawdziwy przedział zastępuje te liczby.)

### 2.1 Pakiety (PLN netto miesięcznie, umowa na 12 miesięcy)

| | **Start** | **Office** ⭐ | **Office Pro** |
| :-- | --: | --: | --: |
| Opłata miesięczna | **1 190** | **1 790** | **3 290** |
| Użytkownicy w cenie | 3 | 10 | 25 |
| Agenci eksperccy w cenie | 1 | 3 | 6 |
| Wsparcie | e-mail, następny dzień roboczy | telefon, ten sam dzień roboczy | telefon, 4 godziny robocze, przegląd kwartalny |
| Pakiet zgodności (notatka do § 23e, umowa powierzenia przetwarzania, szablon DPIA, eksport logu audytowego) | podstawowy | pełny | pełny + przegląd roczny |
| Dodatkowy użytkownik | 59 | 49 | 39 |
| Dodatkowy agent | 490 | 390 | 290 |
| Opłata wdrożeniowa (jednorazowa) | 3 900 | 6 900 | 11 900 |

Kontrola względem wcześniejszych części:

- **Start** leży tuż nad podłogą przy 0,5 h wsparcia. Istnieje po to, żeby małe kancelarie mogły powiedzieć
  „tak", i po to, żeby **Office** wyglądał na rozsądny wybór. Nie na nim zarabiasz.
- **Office** leży na cenie przechwycenia 20% wartości dla Kancelarii K. To pakiet, na którym chcesz mieć 50%+
  klientów.
- **Pro** mniej więcej podwaja Office przy 2,5× większej liczbie użytkowników i dwa razy większej liczbie
  agentów — kotwica „best", przy której Office wygląda rozsądnie, i dom dla 10%+ klientów, którzy potrzebują więcej.

### 2.2 Agenci eksperccy (kancelarie prawne)

| Agent | Typ (część 04) | Cena jako dodatek |
| :-- | :-- | :-- |
| Triaż przychodzących pism sądowych (streszczenie, propozycja terminu, następny krok) | lider | cena z pakietu powyżej |
| Porównanie umowy ze wzorem kancelarii | lider | cena z pakietu powyżej |
| Chronologia akt sprawy ze skanów dokumentów | wypełniacz | cena z pakietu powyżej |
| Tłumaczenie dokumentów (PL ↔ EN/DE) | wypełniacz | cena z pakietu powyżej |
| Eskalacja zanonimizowanego tekstu do chmury przy trudnych pytaniach | **kandydat na zabójcę** | **nieoferowana w pakietach**; osobny, podpisany dodatek |

### 2.3 Opłaty jednorazowe

| Pozycja | Cena (PLN netto) | Uwaga |
| :-- | --: | :-- |
| Płatny pilotaż, 6–8 tygodni, jeden agent-lider | 4 000 | **zaliczany na poczet opłaty wdrożeniowej**, jeśli umowa zostanie podpisana w ciągu 30 dni od końca |
| Dodatkowa sesja szkoleniowa (zdalnie, 1 h) | 400 | |
| Wizyta na miejscu poza wdrożeniem | 900 + dojazd | po pierwszym roku |
| Indeksowanie archiwum powyżej 50 000 stron | wycena indywidualna | mierzone w pilotażu |

### 2.4 Sprzęt (ceny ważne do 31 grudnia 2026)

| Box | Model A: kupujesz je w sklepie | Model C: leasing | Model D: wynajem (tylko z przedpłatą roczną) |
| :-- | :-- | :-- | :-- |
| Minisforum MS-S1 MAX 128 GB | ~10 967 PLN netto (Ceneo, 25 października 2026) | przez partnera | + 390 PLN miesięcznie |
| ASUS Ascent GX10 128 GB | ~21 950 PLN netto | przez partnera | + 750 PLN miesięcznie |

---

## 3. Zakres wsparcia — cena mówienia „nie"

Wsparcie to Twoja największa pozycja kosztowa (część 02). Zakres ją chroni:

| W cenie | Poza ceną (rozliczane stawką godzinową albo odrzucane) |
| :-- | :-- |
| box, jego oprogramowanie, modele i agenci | drukarki, sieć, komputery, poczta e-mail kancelarii |
| aktualizacje modeli i bezpieczeństwa, monitoring, kopie zapasowe boxa | odzyskiwanie danych z własnych urządzeń kancelarii |
| pytania o korzystanie z agentów | pisanie nowych agentów dla jednej kancelarii (to zgłoszenie do katalogu) |
| jedna sesja zdalna na incydent | wizyty na miejscu po wdrożeniu (cena w 2.3) |

Zapisz czasy reakcji **w godzinach roboczych** i kanał wsparcia. Potem prowadź log każdej godziny wsparcia od
pierwszego pilotażu (pułapka B41). Po sześciu miesiącach log powie Ci, czy Twoja podłoga kosztowa była dobra.

---

## 4. Warunki handlowe

### 4.1 Długość umowy, fakturowanie, płatność

- **12 miesięcy**, z odnowieniem na kolejne 12, chyba że umowa zostanie wypowiedziana z **3-miesięcznym
  okresem wypowiedzenia**.
- Fakturowanie **miesięcznie z góry**, termin płatności **14 dni** (ustawowe maksimum między przedsiębiorcami
  to 60 dni — część 05, sekcja 4; nie chcesz być nawet blisko).
- **Przedpłata roczna: dwa miesiące gratis** (≈ 16,7% rabatu — mieści się w regule 20% z sekcji 5).

### 4.2 Indeksacja

Ceny, które nie mogą rosnąć, realnie spadają. Inflacja w Polsce (GUS): średnio **3,6%** w 2025 roku; w 2026
rok do roku między 2,1% (styczeń) a 4,1% (wrzesień); ceny usług wzrosły o 5,7% rok do roku w maju 2026.
Umowa dwuletnia bez indeksacji traci 6–8% swojej realnej wartości.

Co klauzula musi osiągnąć (sformułowanie dla Twojego prawnika):

> Raz w roku, przy odnowieniu umowy, opłaty miesięczne zmieniają się o średnioroczny wskaźnik cen
> towarów i usług konsumpcyjnych za poprzedni rok kalendarzowy ogłoszony przez Prezesa GUS. Opłaty nie ulegają
> obniżeniu. O nowych opłatach informujemy klienta co najmniej 30 dni przed ich zastosowaniem.

### 4.3 Zmiany cen poza indeksacją

- Nowe ceny obowiązują **nowych** klientów od razu.
- Obecni klienci zachowują swoją cenę do najbliższego odnowienia i dostają **co najmniej 60 dni
  wyprzedzenia**.
- Ceny dla partnerów startowych (sekcja 5) są od pierwszego dnia zapisane z datą końcową.

---

## 5. Polityka rabatowa

Dane ProfitWell Patricka Campbella: wysokość rabatu jest **„niemal idealnie skorelowana" z odpływem klientów
(churn)**; jego zasada to nigdy nie dawać rabatu większego niż około 20% (*dane własne firmy*). Klient z rabatem
powiedział Ci, że produkt jest wart mniej niż Twoja cena — i zachowuje się zgodnie z tym.

Zasada dla Twojego cennika: **każdy rabat kupuje coś konkretnego, ma maksimum i ma koniec.**

| Rabat | Co dostajesz w zamian | Maksimum | Koniec |
| :-- | :-- | :-- | :-- |
| Przedpłata roczna | gotówka na boxy (część 05) | 2 miesiące (~17%) | — |
| **Partner startowy** (pierwsze 5 kancelarii) | spisane studium przypadku, rozmowa referencyjna raz na kwartał, ich zmierzone godziny (część 03) | 20% opłaty miesięcznej | po 12 miesiącach, zapisane w umowie |
| Zaliczenie opłaty za pilotaż | podpisują umowę w ciągu 30 dni od końca pilotażu | opłata za pilotaż | 30 dni po pilotażu |
| Wiele lokalizacji (ten sam właściciel, 3+ lokalizacje) | jedna decyzja, kilka boxów | 15% | — |
| **Niedozwolone** | „są mali", „poprosili", „koniec miesiąca" | 0% | — |

Wszystko spoza tej tabeli to zmiana cennika, z numerem wersji i uzasadnieniem — a nie przysługa na spotkaniu.

---

## 6. Warunki partnerskie

Krytyczna analiza pomysłu z boxem w repo kończy się wnioskiem: *„partnerstwo z [firmami usług IT] jako
warstwa AI, podział przychodu"*. Partnerzy muszą wiedzieć, ile zarobią, zanim Cię komuś przedstawią. Dwie
popularne struktury — w researchu **nie** udało się znaleźć polskich danych rynkowych o marżach dla tego rodzaju produktu, więc
procenty to **założenia do przetestowania** z pierwszymi dwoma partnerami:

| Struktura | Co robi partner | Ile zarabia (założenie) |
| :-- | :-- | :-- |
| **Polecenie** | przedstawia kancelarię; Ty sprzedajesz i obsługujesz | 10–15% abonamentu z pierwszego roku |
| **Odsprzedaż** | sprzedaje, fakturuje, prowadzi wsparcie pierwszej linii; Ty robisz aktualizacje i drugą linię | 20–30% rabatu od Twojej ceny katalogowej, na stałe |

Cokolwiek płacisz partnerowi, wychodzi z Twojej marży brutto, a nie z ceny dla klienta. Zanim podpiszesz,
przelicz jeszcze raz podłogę kosztową (część 02) z marżą partnera jako dodatkową pozycją kosztową.

---

## 7. Jak przedstawić cenę prawnikowi

- **Netto, miesięcznie, za kancelarię.** Prawnicy porównują z LEX (298–722 zł miesięcznie) i ze stanowiskami
  w chmurze (590 zł za użytkownika miesięcznie w Beck-Noxtua). Pokaż swoją cenę w tej samej jednostce.
- **Zaczynaj od pakietu, nie od sprzętu.** Box to załącznik.
- **Umieść porównanie w ofercie**: ile kancelaria płaci dziś, ile kosztuje alternatywa, ile warte są zmierzone
  godziny (część 03). Wartość ekonomiczna jest Twoim argumentem; cena jest wnioskiem.
- **Nazwij ryzyko raz, spokojnie**: pytanie z § 23e *„z jakich narzędzi Pan korzystał?"* i log audytowy, który
  na nie odpowiada. Potem przestań (pułapka B44 w części 03).
- **Opublikuj Start i Office** na swojej stronie; Pro „na zapytanie". Małe kancelarie ufają dostawcy, który
  pokazuje ceny, a Ty oszczędzasz sobie spotkania z tymi, których na to nie stać.

---

## 8. ĆWICZENIE 07 — napisz `price-book-v1.md`

Użyj dziewięciu sekcji z sekcji 1. Przy każdej liczbie dodaj kolumnę *źródło*: *obliczenie z części 02*,
*wartość z części 03*, *wywiady z części 06 (n = …)*, *pilotaż* albo *założenie*. Oznacz wersję jako `v1`,
z dzisiejszą datą i rejestrem zmian. Od teraz każda oferta mówi *„zgodnie z cennikiem v1"*.

---

## 9. ⭐ EKSPERYMENT TERENOWY 07 — czy cennik przetrwa prawdziwą ofertę?

**Hipoteza.** Oferta oparta ściśle na cenniku (bez improwizowanych rabatów), wysłana do trzech kancelarii, które
w części 06 doszły do poziomu 3, dostaje co najmniej jedno „tak" albo prośbę o konkretną zmianę, którą możesz
przypisać do wiersza tabeli rabatów.

**Procedura.** Napisz trzy oferty, korzystając wyłącznie z cennika. Wyślij je. Zapisz każdą odpowiedź
dosłownie (w swoich prywatnych notatkach). Przy każdym zastrzeżeniu zanotuj, czy cennik miał na nie odpowiedź.

**Predykcja (moja).** Żadnego zastrzeżenia do samej ceny Office; jedno zastrzeżenie do opłaty wdrożeniowej;
jedna prośba, żeby zacząć od Start i przejść wyżej później.

| Kancelaria (kod) | Oferowany pakiet | Odpowiedź | Zastrzeżenie | Cennik miał odpowiedź? | Zmiana w v2? |
| :-- | :-- | :-- | :-- | :-- | :-- |
| | | | | | |

---

## 10. Pułapki

**B62 · Improwizowany rabat.**
*Objaw:* „Dobra, 25% mniej, bo jesteście pierwsi". *Lekarstwo:* wiersz „partner startowy": 20%, studium
przypadku w zamian, data końcowa.

**B63 · Brak klauzuli indeksacyjnej.**
*Objaw:* cena z 2026 roku nadal obowiązuje w 2029. *Lekarstwo:* klauzula z CPI GUS, od pierwszej umowy.

**B64 · Zakres wsparcia tylko w Twojej głowie.**
*Objaw:* kancelaria dzwoni w sprawie drukarki. *Lekarstwo:* sekcja 3 cennika, dołączona do umowy.

**B65 · Ceny bez wersji.**
*Objaw:* nie wiesz, który klient ma jaką cenę i dlaczego. *Lekarstwo:* rejestr zmian i wersja cennika wpisana
do każdej umowy.

**B66 · Marża partnera z kieszeni klienta.**
*Objaw:* partner dolicza 25% do Twojej ceny katalogowej, a kancelaria znajduje cenę na Twojej stronie.
*Lekarstwo:* jedna publiczna cena katalogowa; marża partnera pochodzi z Twojej strony.

---

## 11. Checkpoint

- [ ] `price-book-v1.md` istnieje, ma wszystkie dziewięć sekcji i źródło przy każdej liczbie.
- [ ] Tabela rabatów ma maksimum i wiersz „niedozwolone".
- [ ] Klauzule indeksacyjna i o wypowiedzeniu są gotowe dla Twojego prawnika.
- [ ] EKSPERYMENT TERENOWY 07: co najmniej jedna oferta wysłana ściśle według cennika.

Źródła do tej części: [ZRODLA.md](ZRODLA.md), sekcja „Część 07".
