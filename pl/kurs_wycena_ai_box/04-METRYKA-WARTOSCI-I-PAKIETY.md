# Część 04 · Metryka wartości i pakiety: za co pobierasz opłatę

> **Cel tej części.** Decydujesz, do **jakiej jednostki** przypinasz cenę (kancelaria, użytkownik, agent,
> dokument, rezultat) i jak dzielisz ofertę na pakiety. Projektujesz katalog agentów eksperckich jako silnik,
> który zwiększa przychód z jednej kancelarii bez nowej sprzedaży.
>
> **Czas:** ~4 h · **Poziom:** ⭐⭐⭐⭐ · **Wynik:** `pricing/04-packages.md`

---

## 0. Problem

Część 03 dała Ci sufit wartości dla Kancelarii K. Ale Kancelaria K to jedna kancelaria. Następna ma ośmiu
prawników, kolejna to dwuosobowa kancelaria notarialna. Jeśli bierzesz jedną stałą kwotę, przepłacają mali
(odchodzą), a duzi płacą za mało (zostawiasz pieniądze na stole). Jeśli bierzesz za użytkownika, box — którego
koszt prawie nie zależy od liczby użytkowników — staje się drogi dokładnie tam, gdzie najtaniej go obsłużyć.

Rozwiązaniem jest **metryka wartości**: jednostka, która rośnie, gdy klient dostaje więcej wartości, i za
którą podąża cena.

---

## 1. Co robi dobra metryka wartości

Patrick Campbell (ProfitWell, obecnie Paddle) podaje, że firmy wyceniające według metryki wartości rosną
około 2× szybciej, mają mniej więcej o połowę mniejszy odpływ klientów (churn) i 2× większy przychód z
rozszerzeń (*dane własne firmy* dostawcy, ale spójne z poniższą logiką). Dobra metryka wartości:

1. **Rośnie razem z wartością dla klienta**, więc cena wydaje się uczciwa przy każdej wielkości.
2. **Jest łatwa do zrozumienia i przewidzenia** — klient może ją zabudżetować (część 01: nieprzewidywalne
   rachunki niszczą zaufanie szybciej niż wysokie ceny).
3. **Łatwo Ci ją policzyć** bez zaglądania w dane klienta. Przy boxie on-premise to nie szczegół: do
   wystawienia faktury nie możesz potrzebować dostępu do akt klientów.
4. **Rośnie bez nowej sprzedaży** — dzięki temu przychód z klienta z czasem rośnie (retencja przychodu netto,
   NRR, część 08).

---

## 2. Kandydaci dla boxa

| Metryka | Rośnie z wartością? | Przewidywalna? | Policzysz ją bez oglądania danych? | Rośnie bez sprzedaży? | Werdykt |
| :-- | :-- | :-- | :-- | :-- | :-- |
| **Za kancelarię** (stała) | słabo | ✅ | ✅ | ❌ | podstawa, nie cała cena |
| **Za użytkownika / stanowisko** | ✅ dla prawników | ✅ | ✅ | powoli (zatrudnianie) | wymiar wielkości; uwaga: AI może zmniejszać liczbę stanowisk |
| **Za agenta eksperckiego** (proces) | ✅ każdy agent to nazwana praca | ✅ | ✅ | ✅ **gdy wypuszczasz nowych agentów** | ⭐ silnik wzrostu |
| **Za przetworzony dokument / stronę** | ✅ | ❌ | wymaga liczników, ale da się | ✅ | licznik — straszy małych kupujących |
| **Za rezultat** (zaakceptowane streszczenie, złożone pismo) | ✅✅ | ❌ | wymaga liczników + definicji | ✅ | później, dla jednego wąskiego agenta |
| **Za token** | ❌ | ❌ | ✅ | — | ❌ nigdy (pułapka B32) |

Rekomendowana struktura — moja opinia, do przetestowania w części 06:

```
 cena miesięczna  =  opłata za platformę (za kancelarię; obejmuje usługę boxa i N użytkowników)
                  +  Σ wybranych agentów eksperckich (każdy wyceniany osobno)
                  +  dodatkowi użytkownicy ponad N (niewielka opłata)
```

Dlaczego taki kształt:

- **Opłata za platformę** pokrywa Twoją podłogę kosztową (część 02): wsparcie, aktualizacje, monitoring, box.
  Sprawia, że każda kancelaria jest rentowna od pierwszego miesiąca.
- **Agenci eksperccy** niosą wartość (część 03). Każdy to nazwana praca, którą kancelaria rozpoznaje —
  *„triaż przychodzących pism sądowych"*, *„porównanie umowy z naszym wzorem"*, *„sprawdzanie faktur w
  KSeF"* — z ceną, którą kancelaria może porównać z oszczędzonymi godzinami.
- **Wymiar użytkowników** obsługuje różnicę wielkości między kancelarią 2-osobową a 12-osobową, bez robienia
  z ceny bazowej ceny „od głowy".

To jest model „hybrydowy" w sensie badań z lat 2025–2026 (część 01), ale bez licznika: zmienną część wybiera
klient, a nie liczysz jej Ty.

---

## 3. Katalog agentów eksperckich: silnik skalowalnego biznesu

Powiedziałeś mi, że chcesz firmy, która skaluje się przez dodawanie eksperckich agentów AI. W języku wyceny
to bardzo precyzyjne stwierdzenie:

> **Każdego nowego agenta, którego zbudujesz, sprzedajesz każdej kancelarii, którą już masz, przy prawie
> zerowym dodatkowym koszcie własnym sprzedaży (COGS).**

Box, relacja wsparcia i kanał aktualizacji już istnieją. Nowy agent kosztuje Cię czas developmentu (koszty
operacyjne, OpEx, jednorazowo) i zestaw ewaluacyjny (jednorazowo), a potem jest zdalną aktualizacją na każdy
box. To najtańszy przychód, jaki kiedykolwiek zarobisz, i dlatego produktem jest katalog agentów — nie box.

### 3.1 Zasady projektowania katalogu

| Zasada | Dlaczego |
| :-- | :-- |
| **Jeden agent = jedna praca, którą profesjonalista nazywa własnymi słowami** | „Triaż pism sądowych" się sprzedaje; „RAG na Twoich dokumentach" — nie |
| **Każdy agent ma zmierzoną oszczędność czasu** (eksperyment terenowy 03) | cenę agenta uzasadnia jego własna liczba |
| **Agenci są specyficzni dla zawodu** | kancelaria prawna nie płaci za agenta KSeF; biuro rachunkowe tak. Osobne katalogi dla każdego zawodu |
| **Każdy agent ma własny zestaw ewaluacyjny przed wydaniem** | Twoja obietnica jakości; łączy się z `kurs_aplikacje_agentowe/14-EWALUACJA.md` |
| **Żaden agent nie jest darmowy na zawsze** | darmowy agent kotwiczy cenę wszystkich agentów na zerze (pułapka B49) |

### 3.2 Liderzy, wypełniacze, zabójcy (Ramanujam)

Zanim agent trafi do pakietu, sklasyfikuj go jako lider / wypełniacz / zabójca (leader / filler / killer),
korzystając z rozmów o gotowości do zapłaty z części 06:

| Typ | Definicja | Dla boxa (przykłady, hipotezy) | Gdzie trafia |
| :-- | :-- | :-- | :-- |
| **Lider** | powód, dla którego kupują; chce go większość kupujących i zapłaciliby za niego | triaż przychodzących pism z propozycją terminu; porównanie umów | w każdym pakiecie — to dla niego pakiet istnieje |
| **Wypełniacz** | miły dodatek, tanio podnosi postrzeganą wartość | agent tłumaczący; notatki ze spotkania z nagrania | w wyższych pakietach |
| **Zabójca** | chce go < 20%, a > 20% **aktywnie go nie lubi** | wszystko, co wysyła dane poza kancelarię, nawet „opcjonalnie"; agent, który rozmawia bezpośrednio z klientami | **nigdy w pakiecie**; co najwyżej osobny dodatek |

Kategoria „zabójca" nie jest dla Ciebie teoretyczna: funkcja hybrydowa, która wysyła zanonimizowany tekst do
modelu w chmurze, to świetny pomysł techniczny (kurs 1, część 10) i może być zabójcą dla połowy Twoich
kupujących. Oferuj ją jako jawny, osobno podpisywany dodatek, nigdy w pakiecie.

---

## 4. Good / better / best

Trzy pakiety — good / better / best (dobry / lepszy / najlepszy). Nie dwa (brak środka, który kotwiczy), rzadko
cztery (paraliż wyboru).

| | **Start** | **Office** ⭐ | **Office Pro** |
| :-- | :-- | :-- | :-- |
| Dla | 1–3 osoby, próbują | 4–10 osób, cel | 10+ osób lub kilka procesów |
| Użytkownicy w cenie | 3 | 10 | 25 |
| Agenci eksperccy w cenie | 1 lider | 2 liderów + 1 wypełniacz | 4 + wszystkie wypełniacze |
| Wsparcie | e-mail, następny dzień roboczy | telefon, ten sam dzień | telefon, 4 h, przegląd kwartalny |
| Aktualizacje i monitoring | ✅ | ✅ | ✅ |
| Log audytowy i pakiet zgodności (notatka o § 23e, umowa powierzenia, wzór DPIA) | podstawowy | ✅ | ✅ + przegląd roczny |
| Dodatkowi agenci | cena za agenta | cena za agenta | cena za agenta, z rabatem |

Nazwy i zawartość pakietów powyżej to **ilustracja**. Ceny pojawią się w części 07, po zmierzeniu gotowości
do zapłaty.

### 4.1 Cele do sprawdzenia po pierwszych 20 klientach

Cele Ramanujama dla zdrowego podziału good/better/best:

| Udział kupujących w… | Zdrowo | Co mówi Ci chybienie |
| :-- | :-- | :-- |
| Good (Start) | **< 30%** | > 50% na poziomie wejściowym: Start jest za dobry albo pozostałe za drogie |
| Better + Best (Office + Pro) | **> 70%** | środkowy pakiet nie jest oczywistym wyborem |
| Best (Pro) | **> 10%** | 0%: Pro nie ma niczego, czego chciałby prawdziwy klient |

### 4.2 Pakiet zgodności — Twój ukryty klejnot

Część 01 nazwała ryzyko **ukrytego klejnotu**: wartościowej rzeczy, którą oddajesz za darmo, nie zauważając
tego. Dla Twoich kupujących kandydatem jest pakiet zgodności:

- pisemna notatka mapująca Twój box na § 23e Kodeksu Etyki Adwokackiej (albo na rekomendacje KIRP dla radców
  prawnych);
- wzór umowy powierzenia przetwarzania danych i wzór DPIA dla kancelarii;
- log audytowy, który kancelaria może wyeksportować, gdy klient zapyta *„jakich narzędzi użyliście?"* —
  dokładnie to pytanie, na które według § 23e adwokat musi odpowiedzieć.

Nie oddawaj go po cichu. Umieść go **widocznie** w tabeli pakietów, bo to część powodu, dla którego Kancelaria
K płaci więcej niż za ChatGPT. Czy jest wart osobnej pozycji na fakturze — to pytanie do części 06.

---

## 5. Opłaty jednorazowe: wdrożenie i onboarding

**Opłata wdrożeniowa** pokrywa instalację, pierwsze indeksowanie archiwum i pierwszego agenta dostrojonego na
własnych dokumentach kancelarii. Zasady:

1. **Zawsze ją pobieraj**, nawet jeśli dajesz rabat. Darmowe wdrożenie mówi klientowi, że instalacja jest
   banalna, i uczy go oczekiwać darmowej pracy.
2. **Wyceniaj ją na podstawie zmierzonego czasu instalacji** (eksperyment terenowy 02) × koszt godziny, plus
   marża. To jedyna cena, przy której metoda koszt-plus jest do przyjęcia, bo płaci za pracę.
3. **Trzymaj ją poniżej progu „to wymaga spotkania"** w kancelarii. W części 06 zapytaj, jaką kwotę starszy
   partner może zatwierdzić sam.

Wcześniejszy szacunek z repo — 25 000–60 000 zł za wdrożenie *łącznie ze sprzętem* (`asymetrie-biznesowe-ai`)
— powstał, zanim istniała podłoga kosztowa. Gdy sprzęt jest rozliczany osobno (część 05), a instalacja
zmierzona w godzinach, sama opłata wdrożeniowa będzie prawdopodobnie dużo mniejsza. Rozstrzygnie to Twój
eksperyment terenowy.

---

## 6. Długość umowy i okres rozliczeniowy

| Wybór | Skutek dla Ciebie | Skutek dla klienta |
| :-- | :-- | :-- |
| Miesięcznie, wypowiedzenie w każdej chwili | łatwo sprzedać, wysokie ryzyko odpływu, brak gotówki z góry | niskie ryzyko |
| **12 miesięcy, rozliczane miesięcznie** | przewidywalny przychód, umiarkowane zobowiązanie | znajome (tak sprzedają LEX i Legalis) |
| 12 miesięcy, **płatne rocznie z góry** | gotówka z góry — finansuje kolejne boxy (część 05) | chce za to rabatu |
| 24–36 miesięcy powiązane ze sprzętem | pasuje do okresu leasingu lub wynajmu | duża decyzja dla małej kancelarii |

**Rekomendacja (moja opinia):** domyślnie 12 miesięcy, rozliczane miesięcznie; umiarkowany rabat za zapłatę
roku z góry; 24–36 miesięcy tylko wtedy, gdy dostarczasz sprzęt (model wynajmu, część 05). O rabatach: dane
ProfitWell Campbella pokazały, że wielkość rabatu jest **prawie idealnie skorelowana z odpływem klientów**, a
jego zasada to nigdy nie dawać rabatu większego niż około 20% (*dane własne firmy* dostawcy). Politykę
rabatową buduje część 07.

---

## 7. ĆWICZENIE 04 — Twoje pakiety

W `pricing/04-packages.md`:

1. Zapisz swoją **metrykę wartości** w jednym zdaniu i sprawdź ją czterema testami z sekcji 1.
2. Wypisz agentów eksperckich, których mógłbyś zbudować w ciągu najbliższych 12 miesięcy dla **jednego**
   zawodu. Co najmniej sześciu. Oznacz każdego jako *lidera*, *wypełniacza* albo *zabójcę* — jako hipotezę do
   potwierdzenia w części 06.
3. Naszkicuj trzy pakiety w tabeli jak w sekcji 4, bez cen.
4. Zdecyduj, co jest w opłacie za platformę, a co nigdy nie jest darmowe.
5. Naszkicuj opłatę wdrożeniową jako: zmierzone godziny × koszt godziny × (1 + marża).

---

## 8. ⭐ EKSPERYMENT TERENOWY 04 — którzy agenci są liderami?

**Hipoteza.** Spośród sześciu agentów z Twojej listy co najwyżej dwóch to liderzy. Kupujący typu Kancelarii K
wskażą tych samych dwóch.

**Procedura.** Pięciu profesjonalistom z Twojego segmentu docelowego (w miarę możliwości tym samym osobom co
w części 06) pokaż nazwy sześciu agentów, każdą z jednozdaniowym opisem. Poproś ich, żeby:

1. posortowali je od *„muszę mieć"* do *„nie użyłbym"*;
2. zaznaczyli te, których w ogóle **nie chcieliby** w kancelarii;
3. dla pierwszego na liście: *„Gdyby box robił tylko to, czy warto byłoby za to płacić?"*

**Predykcja (moja).** Triaż przychodzących pism i porównanie umów to liderzy dla kancelarii prawnych. Każdy
agent, który pisze pisma *do klientów*, zostanie oznaczony jako niechciany przez co najmniej jedną osobę na
pięć (kandydat na zabójcę).

| Agent | Głosy „muszę mieć" (na 5) | Głosy „niechciany" (na 5) | „Wart płacenia sam w sobie"? | Typ |
| :-- | --: | --: | :-- | :-- |
| | | | | |

---

## 9. Pułapki

**B47 · Cena za stanowisko dla boxa, którego koszt nie zależy od stanowisk.**
*Objaw:* 12-osobowa kancelaria płaci 4× więcej niż 3-osobowa za ten sam box i wsparcie. *Lekarstwo:* opłata
za platformę od kancelarii; użytkownicy tylko jako wymiar wielkości, z hojnym limitem w cenie.

**B48 · Licznik u małego kupującego.**
*Objaw:* „0,50 zł za przetworzoną stronę". *Dlaczego boli:* kancelaria nie może tego zabudżetować i zaczyna
racjonować użycie — co zabija wartość, którą musisz udowodnić. *Lekarstwo:* stałe pakiety; liczniki tylko
powyżej hojnego wolumenu w cenie, jeśli w ogóle.

**B49 · Darmowy agent.**
*Objaw:* „pierwszy agent w cenie za darmo". *Dlaczego boli:* kotwiczy cenę każdego agenta na zerze.
*Lekarstwo:* agenci są zawarci w **płatnym** pakiecie, nigdy „za darmo".

**B50 · Zabójcy w pakiecie.**
*Objaw:* funkcja eskalacji do chmury jest częścią pakietu Pro. *Lekarstwo:* osobny, jawnie podpisywany
dodatek.

**B51 · Pakiety projektowane według funkcji, a nie kupujących.**
*Objaw:* Start/Office/Pro różnią się limitami technicznymi (RAM, modele). *Lekarstwo:* pakiety różnią się
tym, **kim jest kupujący** (wielkość, procesy, poziom obsługi).

---

## 10. Checkpoint

- [ ] Jednozdaniowa metryka wartości, która przechodzi cztery testy.
- [ ] Katalog ≥ 6 agentów dla jednego zawodu, każdy z hipotezą: lider / wypełniacz / zabójca.
- [ ] Trzy pakiety bez cen, różniące się typem kupującego.
- [ ] Spisana lista: *nigdy za darmo*.
- [ ] Eksperyment terenowy 04 ma co najmniej trzy wypełnione wiersze.

Źródła do tej części: [ZRODLA.md](ZRODLA.md), sekcja „Część 04".
