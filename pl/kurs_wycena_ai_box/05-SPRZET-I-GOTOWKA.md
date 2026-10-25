# Część 05 · Sprzęt i gotówka: kto jest właścicielem boxa?

> **Cel tej części.** Wybierasz, jak sprzęt trafia do kancelarii — klient go kupuje, Ty go odsprzedajesz,
> finansuje go firma leasingowa albo Ty go wynajmujesz — i liczysz, co każdy wybór robi z **Twoją gotówką**, z
> **podatkami klienta** i z tym, **jak inwestor czyta Twój przychód**.
>
> **Czas:** ~4 h · **Poziom:** ⭐⭐⭐⭐ · **Wynik:** `pricing/05-hardware.md` · **Narzędzie:**
> `narzedzia/pricing_model.py cash`

> **To nie jest porada podatkowa ani prawna.** Poniższe zasady podatkowe streszczono z publicznych źródeł
> według stanu na 25 paź 2026. O tym, jak klient zaksięguje box, decyduje jego księgowy; o tym, jak Ty — Twój.

---

## 0. Problem

Box kosztuje 9 000–23 000 zł netto (część 02). Ktoś musi za niego zapłacić pierwszego dnia. Jeśli Ty, to każdy
nowy klient kosztuje Cię boxa, zanim zapłaci Ci cokolwiek, i **im szybciej rośniesz, tym więcej gotówki
potrzebujesz** — klasyczny sposób, w jaki małe firmy sprzętowe umierają, choć ich sprzedaż wygląda świetnie.
Jeśli klient, to zakup za 15 000 zł może wymagać spotkania wspólników i sprzedaż zwalnia.

Nie ma darmowej opcji. Są cztery opcje o różnych kosztach, a wybór jest decyzją cenową, bo zmienia to, co
klient widzi na fakturze.

---

## 1. Cztery modele

| | **A. Klient kupuje** | **B. Ty odsprzedajesz** | **C. Leasing** | **D. Wynajem (sprzęt jako usługa, HaaS)** |
| :-- | :-- | :-- | :-- | :-- |
| Kto jest właścicielem boxa | klient | klient | firma leasingowa → klient po wykupie | **Ty** |
| Kto płaci pierwszego dnia | klient, sklepowi | Ty płacisz sklepowi; klient płaci Twoją fakturę | firma leasingowa płaci Tobie | **Ty** |
| Klient widzi | fakturę ze sklepu + Twoje wdrożenie + abonament | Twoją fakturę za box + abonament | ratę leasingową + Twój abonament | **jedną miesięczną opłatę** |
| Twoja potrzeba gotówki | żadna | box, dopóki klient nie zapłaci | żadna (płatność przy dostawie) | **box, odzyskiwany przez 24–36 miesięcy** |
| Gwarancja i wymiany | sklep | **Ty** | sklep / Ty | **Ty** |
| Twój przychód | wdrożenie + abonament | + niskomarżowy przychód ze sprzętu | wdrożenie + abonament (+ sprzedaż sprzętu leasingodawcy) | w całości powtarzalny |
| Najlepszy dla | wrażliwych na cenę kancelarii, które znają się na podatkach | zwykle dla nikogo | większości małych kancelarii | szybkiej sprzedaży, historii dla inwestorów — jeśli masz kapitał |

### 1.1 A — klient kupuje

Publikujesz krótką listę zatwierdzonych boxów (część 02, tabela sprzętu), a klient kupuje jeden z nich w
sklepie. Ty go instalujesz. Dla Ciebie najczystsza opcja: bez kapitału, bez gwarancji, bez przychodu ze
sprzętu, który rozwadnia Twoją marżę. Tarciem jest sam zakup i ryzyko, że kupią zły model. Ogranicz je,
podając dwa dokładne modele i sprawdzając zamówienie, zanim je złożą.

### 1.2 B — Ty odsprzedajesz

Kupujesz box i wystawiasz go na swojej fakturze. To **wygląda** na dodatkowy przychód i zwykle jest pułapką:

- płacisz sklepowi od razu, a klient płaci Tobie po terminie płatności (do 60 dni między firmami —
  sekcja 4);
- gwarancja, kurier i zepsuta sztuka stają się Twoim problemem;
- przychód ze sprzętu ma cienką marżę i sprawia, że Twoja marża brutto wygląda gorzej (część 08).

Odsprzedawaj tylko wtedy, gdy klient upiera się przy jednej fakturze, i wyceniaj box jako cenę sklepową plus
marżę, która pokryje obsługę gwarancji.

### 1.3 C — leasing przez partnera

Firma leasingowa kupuje box (od Ciebie albo ze sklepu), a klient spłaca go co miesiąc. Ty dostajesz
pieniądze przy dostawie. Co znalazł research (25 paź 2026; szczegóły w [ZRODLA.md](ZRODLA.md)):

| Fakt | Źródło |
| :-- | :-- |
| EFL: leasing od 1 000 zł netto, do 36 miesięcy, wpłata własna 0–45%, **tylko nowy sprzęt** | strona produktu EFL |
| Leasing online od 500 zł; leasing tradycyjny zwykle od 4 500 zł | Leason (przegląd brokera), luty 2026 |
| Sprzęt IT leasinguje się zwykle na **16–36 miesięcy**, wykup od 1% | Leason |
| Leasing online (Leaselink) może sfinansować używany sprzęt do 250 000 zł netto bez wyceny | Leason |
| Wynajem laptopów: Netland365, 99 zł netto za urządzenie miesięcznie, umowy na 24 miesiące | Netland365 |
| Oferta device-as-a-service dla **serwerów AI** w Polsce | **nie znaleziono** — luka albo sygnał, że rynek jeszcze nie istnieje |

Dla klienta rata **leasingu operacyjnego** jest kosztem uzyskania przychodu, gdy (streszczenie researchu,
sprawdź z księgowym):

- leasing trwa co najmniej **40% normatywnego okresu amortyzacji** — dla komputerów (KŚT grupa 4,
  pozycja 487, 30% rocznie) to około **16 miesięcy**; oraz
- suma rat jest co najmniej równa wartości początkowej środka trwałego.

**Praktyczny krok:** przed pierwszą sprzedażą zapytaj dwie firmy leasingowe, czy sfinansują *Twój*
skonfigurowany box (PC plus zainstalowane przez Ciebie oprogramowanie) jako jeden środek trwały, i od jakiej
minimalnej wartości. Niektóre wyleasingują sprzęt, ale nie oprogramowanie ani usługi, więc Twoja opłata
wdrożeniowa i abonament pozostaną osobnymi fakturami.

### 1.4 D — wynajem (sprzęt jako usługa, HaaS)

Jesteś właścicielem boxa i pobierasz jedną miesięczną opłatę, która go obejmuje. Dla klienta to najłatwiejszy
zakup: bez wydatku inwestycyjnego, jedna liczba, „jak się zepsuje, to Twój problem". To także model Lemony AI:
499 USD miesięcznie za box, aktualizacje i wsparcie, do 5 użytkowników (TechCrunch, czerwiec 2025).

Dla inwestorów jest atrakcyjny: raport *State of HaaS* 2024 Silicon Valley Bank (obecnie First Citizens)
wykazał **medianę mnożnika przychodów wyższą o 59%** dla firm typu sprzęt jako usługa niż dla innych modeli
frontier-tech, przy typowym zwrocie systemu po około **15 miesiącach** (*dane z raportu*).

Dla Ciebie to zdecydowanie najbardziej kapitałochłonny model (sekcja 2). Wybierz go tylko wtedy, gdy wiesz,
skąd przyjdą pieniądze na boxy (sekcja 3).

---

## 2. Uruchom model gotówkowy

```bash
python3 pricing_model.py cash                          # 2 nowe kancelarie miesięcznie, 36 miesięcy
python3 pricing_model.py cash --payment-days 60        # klienci płacą późno
python3 pricing_model.py cash --hardware 21950         # box klasy GX10 / DGX Spark
```

Wartości domyślne (wszystkie to założenia — zastąp je): sprzęt 10 967 zł netto, 10% narzutu na sprzęt,
wdrożenie 6 000 zł, abonament 1 500 zł miesięcznie, koszt wsparcia 500 zł za kancelarię miesięcznie, 1%
miesięcznego odpływu klientów (churn), **koszty stałe 15 000 zł miesięcznie** (development, sprzedaż, narzędzia, Twoja
wypłata), wynajem odzyskuje koszt boxa przez 36 miesięcy.

Wyniki:

| Scenariusz | A. klient kupuje | B. odsprzedaż | C. leasing | D. wynajem |
| :-- | --: | --: | --: | --: |
| Najniższa gotówka, 2 kancelarie/miesiąc, termin płatności 14 dni | −1 000 | 0 | 0 | **−107 396** (miesiąc 9) |
| Najniższa gotówka, 2 kancelarie/miesiąc, termin płatności **60 dni** | −1 000 | **−43 888** (miesiąc 2) | 0 | −107 396 |
| Najniższa gotówka, **5** kancelarii/miesiąc | 0 | 0 | 0 | −101 137 (miesiąc 6) |
| Najniższa gotówka, **box klasy GX10** (21 950 zł) | −1 000 | 0 | 0 | **−320 651** (miesiąc 15) |
| Gotówka po 36 miesiącach, scenariusz bazowy | 1 080 982 | 1 159 944 | 1 159 944 | 689 789 |

Jak to czytać:

- **„Najniższa gotówka" to pieniądze, które musisz już mieć** albo pożyczyć, żeby przetrwać dany model. Wynajem
  wymaga około 100 000 zł przy małym boxie i ponad 300 000 zł przy boxie klasy GX10, przy dwóch kancelariach
  miesięcznie.
- **Model wynajmu kończy z mniejszą gotówką po 36 miesiącach**, ale jesteś właścicielem boxów (wartość
  rezydualna, której model nie liczy) i masz najbardziej przewidywalny przychód. To wymiana gotówki teraz na
  jakość przychodu później.
- **Odsprzedaż z długimi terminami płatności** po cichu robi z Ciebie bank dla Twoich klientów.
- W modelach A–C to **opłata wdrożeniowa utrzymuje Cię przy życiu na początku**: przy dwóch nowych
  kancelariach miesięcznie opłaty wdrożeniowe pokrywają większość kosztów stałych, zanim baza abonamentów
  urośnie. Nie oddawaj wdrożenia za darmo.

---

## 3. Skąd wziąć pieniądze na boxy do wynajmu

Jeśli wybierzesz wynajem, potrzebujesz kapitału, zanim potrzebujesz klientów. Opcje, od najtańszej:

1. **Twój dochód z kontraktu.** Fakturujesz 1 700 zł netto dziennie. Miesiąc dochodu z kontraktu kupuje
   mniej więcej dwa–trzy małe boxy. Kurs *Od kontraktu B2B do własnej firmy*, część 04, wylicza, ile z tego
   możesz zaryzykować bez naruszania poduszki bezpieczeństwa.
2. **Leasing boxów na siebie** i wynajmowanie ich dalej. Sprawdź umowę leasingu: wiele zakazuje
   podnajmu bez zgody leasingodawcy. Poproś o tę zgodę na piśmie.
3. **Przedpłata klienta.** Rok abonamentu zapłacony z góry (część 04, sekcja 6) pokrywa koszt boxa. Oferuj
   rabat za przedpłatę roczną tylko razem z modelem wynajmu.
4. **Inwestorzy.** Sprzęt to klasyczny powód, dla którego firma programistyczna o niskich potrzebach
   kapitałowych potrzebuje pieniędzy. Część 08 i kurs dla założycieli omawiają, kiedy to ma sens.

**Moja rekomendacja:** zacznij od **C (leasing) i A (klient kupuje)** równolegle; **D (wynajem)** oferuj tylko
klientom, którzy płacą rok z góry, dopóki nie masz kapitału albo inwestorów. **B** zostaw dla rzadkiego
klienta, który upiera się przy jednej fakturze.

---

## 4. Terminy płatności i opóźnienia

Według ustawy o przeciwdziałaniu nadmiernym opóźnieniom w transakcjach handlowych (Dz.U. 2023 poz. 1790), w
streszczeniu z researchu:

| Zasada | Wartość |
| :-- | :-- |
| Maksymalny termin płatności między firmami | **60 dni**, chyba że wyraźnie uzgodniono inaczej i nie jest to rażąco nieuczciwe wobec wierzyciela (art. 7 ust. 2) |
| Duże przedsiębiorstwo płacące MŚP | twarde maksimum 60 dni (art. 7 ust. 2a) |
| Podmioty publiczne | 30 dni |
| Ustawowe odsetki za opóźnienie w transakcjach handlowych | stopa referencyjna NBP + 10 punktów procentowych: **13,75%** rocznie od 1 lip do 31 gru 2026 (M.P. 2026 poz. 642) |
| Stała rekompensata za koszty odzyskania należności | 40 EUR (należności do 5 000 zł), 70 EUR (5 000–50 000 zł), 100 EUR (od 50 000 zł) |

**Wpisz 14-dniowy termin płatności do swojego cennika — księgi cen** (część 07). Małe kancelarie płacą za
oprogramowanie co miesiąc; 14 dni to dla nich norma i trzyma Cię z dala od wiersza „bank dla klientów" w
tabeli powyżej.

---

## 5. Podatkowe spojrzenie klienta — dlaczego model zmienia cenę, którą odczuwa

Ten sam box za 13 000 zł odczuwa się różnie, zależnie od tego, jak klient może go zaksięgować. Z researchu
(sprawdź z księgowym):

| Sytuacja klienta | Co może zrobić |
| :-- | :-- |
| Środek trwały do **10 000 zł netto** | wrzucić od razu w koszty |
| Komputer powyżej 10 000 zł | amortyzować **30% rocznie** (KŚT 487) — albo skorzystać z jednorazowego odpisu poniżej |
| **Nowe** środki trwałe w grupach KŚT 3–6 i 8 | jednorazowy odpis do **100 000 zł rocznie** |
| Mali podatnicy i firmy rozpoczynające działalność | jednorazowa amortyzacja de minimis do **50 000 EUR** (213 000 zł w 2026) |
| Leasing operacyjny, ≥ 16 miesięcy dla komputerów | raty są kosztem w miarę ich płacenia |

I VAT:

- Kancelaria, która jest czynnym podatnikiem VAT, odlicza 23% VAT od boxa i od Twojego abonamentu. Dla niej
  Twoja cena netto jest prawdziwą ceną.
- Kancelaria, która **nie może** odliczyć VAT, płaci 23% więcej za wszystko, co sprzedajesz. Usługi medyczne
  są co do zasady zwolnione z VAT, więc prywatna klinika zwykle nie może odliczyć VAT od boxa; mała firma
  korzystająca ze zwolnienia podmiotowego z VAT — też nie. Usługi doradztwa prawnego, jak rozumiem ustawę o
  VAT, nie mogą korzystać z tego zwolnienia podmiotowego (art. 113 ust. 13), więc większość kancelarii
  prawnych to czynni podatnicy VAT — **sprawdź to z księgowym, zanim oprzesz się na tym w rozmowie
  sprzedażowej.**

**Dla wyceny oznacza to:** kancelariom prawnym i doradcom podatkowym podawaj ceny netto; klinikom i małym
firmom zwolnionym z VAT pokazuj też cenę brutto, bo to tę liczbę odczują.

---

## 6. ĆWICZENIE 05 — wybierz i uzasadnij

W `pricing/05-hardware.md`:

1. Uruchom model gotówkowy z **Twoimi** liczbami z części 02–04.
2. Wypełnij tabelę z sekcji 2 dla swojego scenariusza.
3. Wybierz model(e), które zaoferujesz najpierw, i zapisz warunek, przy którym dodasz wynajem.
4. Zapisz dokładnie dwa modele boxa, które będziesz wspierać na start, z cenami netto i datą „cena ważna
   do".
5. Zapisz pytania do firm leasingowych (sekcja 1.3, „praktyczny krok").

---

## 7. ⭐ EKSPERYMENT TERENOWY 05 — czy firma leasingowa sfinansuje box?

**Hipoteza.** Co najmniej jedna z dwóch firm leasingowych sfinansuje skonfigurowany box za 11 000–22 000 zł
netto dla małej kancelarii prawnej, na 24–36 miesięcy, bez żądania, żeby oprogramowanie było leasingowane
razem z nim.

**Procedura.** Skontaktuj się z dwiema firmami leasingowymi (jedną tradycyjną, jedną online). Opisz transakcję
tak, jak będzie naprawdę wyglądać: mini PC kupiony w konkretnym sklepie albo od Ciebie, zainstalowany przez
Ciebie, dla kancelarii prawnej z dwuletnią historią. Zapytaj o: minimalną wartość, okres, wpłatę własną,
miesięczną ratę, czy możliwe są egzemplarze używane lub odnowione, czy istnieje program dla dostawców
(płacą Ci przy dostawie) i jakich dokumentów potrzebuje kancelaria.

**Predykcja (moja).** Obie sfinansują sprzęt. Żadna nie sfinansuje oprogramowania ani wdrożenia. Miesięczna
rata za box za 11 000 zł netto na 36 miesięcy wyniesie mniej więcej 350–400 zł netto.

| Firma | Min. wartość | Okres | Wpłata własna | Rata (netto) | Finansuje oprogramowanie? | Program dla dostawców? |
| :-- | --: | :-- | --: | --: | :-- | :-- |
| | | | | | | |
| | | | | | | |

---

## 8. Pułapki

**B52 · Wzrost szybszy niż Twoja gotówka.**
*Objaw:* model wynajmu, więcej klientów niż w planie i puste konto w 9. miesiącu. *Lekarstwo:* uruchom `cash`,
zanim wybierzesz wynajem, i ustal maksymalną liczbę boxów do wynajmu miesięcznie, na jaką pozwala Twój
kapitał.

**B53 · Przychód ze sprzętu przedstawiany jako wzrost.**
*Objaw:* „Przychód 400 000 zł", z czego 300 000 zł to odsprzedane boxy. *Dlaczego boli:* inwestorzy i Twoje
własne decyzje patrzą na przychód powtarzalny i marżę brutto (część 08). *Lekarstwo:* zawsze raportuj
przychód ze sprzętu osobno.

**B54 · Cena sprzętu bez daty ważności.**
*Objaw:* oferta z marca honorowana w październiku po 17-procentowej podwyżce ceny (przykład DGX Spark z
części 02). *Lekarstwo:* każda cena sprzętu ma „ważna do".

**B55 · Ignorowanie sytuacji VAT klienta.**
*Objaw:* klinika jest zaskoczona ceną wyższą o 23%. *Lekarstwo:* na pierwszym spotkaniu zapytaj „czy
odliczacie VAT?"; tam, gdzie nie, pokazuj ceny brutto.

**B56 · Podnajem leasingowanych boxów bez zgody leasingodawcy.**
*Objaw:* model wynajmu finansowany leasingiem, bez klauzuli, która na to pozwala. *Lekarstwo:* najpierw zgoda
na piśmie.

---

## 9. Checkpoint

- [ ] `pricing/05-hardware.md` zawiera tabelę gotówkową dla Twoich liczb.
- [ ] Wybrałeś model(e) sprzętowe na pierwszy rok, ze spisanym warunkiem dodania wynajmu.
- [ ] Dwa wspierane modele boxa z cenami netto i datami ważności.
- [ ] Eksperyment terenowy 05: odpowiedziała co najmniej jedna firma leasingowa.
- [ ] Potrafisz w dwóch zdaniach wyjaśnić Kancelarii K, jak może zaksięgować box podatkowo.

Źródła do tej części: [ZRODLA.md](ZRODLA.md), sekcja „Część 05".
