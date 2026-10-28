# Część 03 · Sufit wartości: ile box jest wart dla Kancelarii K

> **Cel tej części.** Szacujesz, w złotych miesięcznie, ile box jest wart dla jednej konkretnej kancelarii:
> cenę jej najlepszej alternatywy plus wartość tego, co box robi lepiej. Odkrywasz, że odpowiedź zależy
> bardziej od tego, **której kancelarii** sprzedajesz, niż od tego, co box robi — i że to rozstrzyga o Twoim
> kliencie docelowym.
>
> **Czas:** ~4 h · **Poziom:** ⭐⭐⭐ · **Wynik:** `pricing/03-value.md`, sekcje *Wartość referencyjna* i
> *Wartość ekonomiczna* w `pricing/01-anchors.md` · **Narzędzie:** `narzedzia/pricing_model.py value`

---

## 0. Problem

W części 02 podłoga kosztowa wyszła na mniej więcej 1 400–3 000 zł za kancelarię miesięcznie, zależnie od
godzin wsparcia i docelowej marży. Czy to dużo? Od strony kosztów tego nie wiesz. Jedyny sposób, żeby się
dowiedzieć, to oszacować, ile box jest wart dla osoby, która płaci — i co zrobiłaby zamiast niego.

Inżynierowie zwykle pomijają ten krok z dobrego powodu: „wartość" brzmi jak coś niemierzalnego. Nie jest. To
suma kilku liczb, z których każdą możesz sprawdzić albo o nią zapytać. Są niepewne, więc liczysz przedział i
zapisujesz założenia. To i tak dużo lepsze niż brak liczby.

---

## 1. Metoda: szacowanie wartości ekonomicznej (Economic Value Estimation)

Za Nagle & Müller, *The Strategy and Tactics of Pricing* (wyd. 6, 2018):

```
 wartość ekonomiczna  =  wartość referencyjna  +  wartość zróżnicowania
                         (cena najlepszej         (to, w czym Twoje jest lepsze, w zł,
                          alternatywy)             minus to, w czym jest gorsze)
```

Cztery kroki:

1. **Nazwij najlepszą alternatywę**, której klient naprawdę by użył. Nie tę, z którą Ty byś się porównał;
   tę, którą wybraliby *oni*.
2. **Wyceń ją** dla tego klienta, miesięcznie.
3. **Wypisz różnice** między Twoim boxem a tą alternatywą, dodatnie i ujemne.
4. **Przypisz każdej różnicy wartość w złotych**, z założeniem zapisanym obok.

Wynik to sufit. Twoja cena musi być **poniżej** niego, tak żeby klient miał powód do zmiany. Jak daleko
poniżej — to kwestia negocjacji i pozycjonowania (sekcja 5).

---

## 2. Kim jest Kancelaria K i kim mogłaby być

Rynek, według researchu do tego kursu (25 paź 2026; szczegóły i zastrzeżenia w [ZRODLA.md](ZRODLA.md)):

| Zawód | Ilu w Polsce | Uwagi do wyceny |
| :-- | --: | :-- |
| Adwokaci | 29 506 ma tytuł; ~23 600 wykonuje zawód (2025) | rp.pl, powołując się na raport Watchdog Polska, 2 wrz 2026; nie znaleziono oficjalnej liczby praktykujących adwokatów od NRA |
| Radcowie prawni | 56 415 na listach (2025) | to samo źródło; udziału praktykujących nie znaleziono |
| Notariusze | 4 297 notariuszy, 3 507 kancelarii (31 gru 2025) | KRN. W I połowie 2025 r. 23% notariuszy nie miało pracowników, a 35% miało dokładnie jednego (rp.pl). **Taksy notarialne zamrożone od 2004 r.** |
| Doradcy podatkowi | 9 220 (18 gru 2025) | KIDP |
| Biura rachunkowe | ~70 000 (**szacunek**) | KIBR, 2022, powtórzone przez Infor w 2026; KIBR twierdzi, że prawdziwa liczba jest nieznana |
| Wielkość firm | ~99% firm prawniczych, rachunkowych i podatkowych zatrudnia ≤ 9 osób | GUS, **2014** — nie znaleziono nowszego podziału |

Dwa wnioski przed jakimkolwiek liczeniem:

- **Rynek jest duży pod względem liczby i mały w przeliczeniu na kupującego**. Dziesiątki tysięcy kancelarii
  i biur, prawie wszystkie poniżej dziesięciu osób. Cena, która wymaga firmy na 20 osób, opisuje niewielką
  mniejszość.
- **Notariusze wyglądają słabo pod kątem wyceny**: większość kancelarii to jedna–dwie osoby, a ich własne
  ceny są zamrożone. Ich gotowość do zapłaty jest prawdopodobnie niższa, niż sugerowałaby ich potrzeba
  tajemnicy. (To hipoteza — sprawdź ją w części 06, zanim z nich zrezygnujesz.)

**Kancelaria K** (nasz przykład przewodni) to pięcioosobowa kancelaria w średnim mieście: dwóch adwokatów,
jeden aplikant, dwie asystentki.

---

## 3. Kroki 1–2: wartość referencyjna

Czego Kancelaria K użyłaby zamiast Twojego boxa? Jest trzech uczciwych kandydatów.

### 3.1 Alternatywa A: profesjonalne chmurowe AI prawnicze

| Produkt | Cena (netto) | Uwaga |
| :-- | :-- | :-- |
| Beck-Noxtua | 590 zł za użytkownika miesięcznie, bez limitu użycia; **wymaga Legalis Silver lub wyższego** | beck-noxtua.pl; jeden serwis branżowy (TAX.PL, ~sie 2026) wciąż opisywał go jako „wkrótce" |
| LEX Kancelaria Prawna | Standard 298,30 zł; Optimum 525 zł; Premium 722 zł miesięcznie | lex.pl; cena dodatku *LEX Expert AI* nie jest publikowana |
| Gaius-Lex „Gaius Vault" | on-premise / air-gapped; **brak publicznej ceny** | najbliższy polski konkurent dla Twojego pozycjonowania |

Dla Kancelarii K: dwóch adwokatów na Beck-Noxtua = **1 180 zł miesięcznie**, ponad bazę prawną, za którą już
płacą.

### 3.2 Alternatywa B: ogólny asystent chmurowy

ChatGPT Business 20–25 USD za stanowisko, Claude Team 20–25 USD za standardowe stanowisko, Microsoft 365
Copilot 30 USD (Business: 21 USD cennikowo, 18 USD promocyjnie do końca 2026). Dla pięciu osób: mniej więcej
**400–550 zł miesięcznie**.

To tanie i wielu prawników już tego używa: w badaniu Fundacji SET / Logit wśród polskich adwokatów i radców
prawnych (luty 2026) **53,6% korzysta z darmowych lub otwartych narzędzi, często bez umowy powierzenia
przetwarzania danych i poza bezpiecznymi środowiskami**. Jednocześnie **81% wskazuje bezpieczeństwo i
poufność danych klientów jako obawę**.

Reguła, która teraz obowiązuje adwokatów: **§ 23e Kodeksu Etyki Adwokackiej** (przyjęty przez NRA 12–13
czerwca 2026, opublikowany 15 czerwca 2026). W streszczeniu z researchu: AI można używać wyłącznie w roli
pomocniczej; informacji objętych tajemnicą zawodową nie wolno wprowadzać do narzędzi, które nie chronią ich
odpowiednio; wyniki trzeba weryfikować; a na żądanie klienta adwokat musi powiedzieć, jakich narzędzi użył.
Rekomendacje KIRP dla radców prawnych (2025) każą sprawdzić, czy przetwarzanie pozostaje w EOG, czy dane są
używane do trenowania i czy potrzebna jest umowa powierzenia — i zauważają, że AI on-premise jest możliwe,
ale w praktyce **„niezwykle rzadkie"**.

⚠️ § 23e **nie** zakazuje AI w chmurze. Narzędzie chmurowe z lokalizacją danych w EOG i porządną umową
powierzenia może być „odpowiednie". Nie sprzedawaj boxa jako „jedynej legalnej opcji" — to nieprawda i
prawnik będzie o tym wiedział (pułapka B44). Sprzedawaj go jako **opcję, przy której to pytanie w ogóle się
nie pojawia**.

### 3.3 Alternatywa C: robienie tego ręcznie

Cena: 0 zł w gotówce, płatne godzinami. Dla kancelarii, która uznała, że AI w chmurze nie wchodzi w grę dla
akt klientów, to jest prawdziwa alternatywa, a jej wartość referencyjna wynosi **zero**.

### 3.4 Która z nich dotyczy Kancelarii K?

Nie wiesz, dopóki nie zapytasz (część 06 i eksperyment terenowy 01 z części 01). Ten wybór ma ogromne
znaczenie, co pokazuje sekcja 6. Wpisz wszystkie trzy do `pricing/03-value.md` i zaznacz, która Twoim zdaniem
ma zastosowanie.

---

## 4. Kroki 3–4: wartość zróżnicowania

### 4.1 Czas

Największa pozycja dodatnia. Potrzebujesz trzech liczb na każdą rolę:

| Liczba | Skąd ją wziąć |
| :-- | :-- |
| **Godziny zaoszczędzone na osobę tygodniowo** | Zmierz w pilotażu. Do tego czasu: Wolters Kluwer *Future Ready Lawyer 2026* (810 prawników, 11 krajów, w tym Polska): ponad 60% respondentów mówi, że AI oszczędza im **6–20% tygodniowego czasu pracy** (*dane własne firmy*, deklaracje respondentów). 3 godziny z 40-godzinnego tygodnia to 7,5% — w tym przedziale, po ostrożnej stronie |
| **Ile warta jest godzina** | Dla prawników — stawka godzinowa. Nie ma wiarygodnego polskiego badania stawek godzinowych za 2025–2026; orientacyjne przedziały ze źródeł blogowych i marketingowych: **150–250 zł** netto w miejscowościach poniżej 100 000 mieszkańców, **250–400 zł** w średnich miastach, **350–600 zł** w Warszawie, Krakowie i Wrocławiu. Dla asystentek — ich koszt godziny dla kancelarii; zapytaj, nie zgaduj |
| **Realizacja** | Udział zaoszczędzonych godzin, które zamieniają się w pieniądze: zafakturowane klientowi albo wykorzystane na pracę, za którą można wystawić fakturę. **To liczba, którą większość wyliczeń wartości ma źle.** Zaoszczędzona godzina, która staje się dłuższym lunchem, jest warta 0 zł dla konta bankowego kancelarii. Zacznij od 0,3–0,5 |

Policz to dla dwóch adwokatów Kancelarii K (po 3 h/tydzień, 300 zł/h — średnie miasto, realizacja 40%):

```bash
python3 pricing_model.py value --people 2 --hours-saved 3 --rate 300 --realisation 0.4 --alternative 1180
```

Wartość czasu: **3 118 zł miesięcznie** dla dwóch adwokatów.

To samo dla aplikanta i dwóch asystentek, przy **założonym** koszcie 60 zł za ich godzinę i realizacji 30%,
dokłada około **700 zł**. Ich zaoszczędzony czas jest prawdziwy, ale rzadko zamienia się w pieniądze, chyba
że pozwala kancelarii uniknąć zatrudnienia kolejnej osoby.

### 4.2 Pozwolenie i ryzyko

Box umożliwia coś, co inaczej nie jest możliwe: AI na aktach klientów bez żadnego pytania o transfer danych.
Ile to jest warte?

- Jeśli Kancelaria K zdecydowała, że **nigdy nie wrzuci akt klientów do narzędzia chmurowego**, to *cała*
  powyższa wartość czasu zależy od boxa. Bez niego wartość to nie „mniej AI", tylko „brak AI".
- Jeśli Kancelaria K **już używa ChatGPT na aktach klientów**, jak ponad połowa ankietowanych prawników
  korzystających z darmowych narzędzi, box usuwa ryzyko, którego mogli nie wycenić: sprawę dyscyplinarną na
  gruncie § 23e, incydent RODO, klienta pytającego „jakich narzędzi użyliście?".

**Nie wkładaj liczby za ryzyko do ceny.** Wyliczenia oczekiwanej straty (prawdopodobieństwo × kara) wyglądają
rygorystycznie, a takie nie są: nie znasz prawdopodobieństwa. Używaj ryzyka w *opowieści sprzedażowej*
(część 07), a w kalkulatorze zostaw `--risk-value 0`. Dzięki temu Twoja cena da się obronić.

### 4.3 Pozycje ujemne

Odejmij je uczciwie, przynajmniej słownie w `03-value.md`:

| Różnica ujemna względem chmury | Jak duża |
| :-- | :-- |
| Mniejszy model niż czołowe modele chmurowe | zależy od procesu; zmierz na ich dokumentach |
| Sprzęt w kancelarii: miejsce, hałas, prąd, rzecz, która może się zepsuć | mała, ale odczuwalna |
| Jednoosobowy dostawca: „a co, jeśli znikniesz?" | **duża** dla ostrożnego kupującego — odpowiedz na to w umowie (depozyt obrazu boxa, partner, który może przejąć obsługę) |
| Instalacja i krzywa uczenia się | jednorazowa, ale opóźnia wartość o tygodnie |

---

## 5. Od sufitu do ceny

Kalkulator wypisuje trzy kandydackie ceny: wartość referencyjna plus 10%, 20% lub 30% wartości
zróżnicowania. Dlaczego tylko ułamek?

- Klient musi **widzieć zysk** po zapłaceniu Tobie, inaczej nie ma powodu, żeby cokolwiek zmieniać.
- Twój szacunek wartości jest **niepewny**, a własny szacunek klienta jest niższy niż Twój.
- Zmiana ma koszt (czas, ryzyko), którego nie widać w wyliczeniu.

Przechwycenie 10–30% wartości zróżnicowania to typowy przedział startowy dla nowego dostawcy bez referencji.
Rośnie, w miarę jak zbierasz dowody (referencje, zmierzone godziny z pilotaży).

---

## 6. Wynik: alternatywa rozstrzyga wszystko

Ten sam box, ten sam zaoszczędzony czas, ta sama kancelaria — zmienia się tylko alternatywa (dwóch
adwokatów, po 3 h/tydzień, 300 zł/h, realizacja 40%; z `pricing_model.py value`):

| Alternatywa Kancelarii K | Wartość referencyjna | Wartość ekonomiczna (sufit) | Cena przy przechwyceniu 10% / 20% / 30% |
| :-- | --: | --: | :-- |
| A — Beck-Noxtua dla obu adwokatów | 1 180 | **4 298** | 1 492 / **1 804** / 2 115 |
| C — ręcznie (AI w chmurze nie wchodzi w grę) | 0 | **3 118** | 312 / **624** / 935 |

Teraz postaw obok część 02. Podłoga kosztowa przy 20 kancelariach, 1 godzinie wsparcia i marży 60% wyniosła
**1 417 zł**.

- Wobec kancelarii, która **w przeciwnym razie kupiłaby chmurowe AI prawnicze**, cena 1 500–2 100 zł leży
  nad Twoją podłogą i pod ich sufitem. **Biznes działa.**
- Wobec kancelarii, która **w przeciwnym razie robiłaby to ręcznie**, wygodna cena (300–900 zł) jest
  **poniżej Twojej podłogi**. Biznes nie działa na samym czasie adwokatów — chyba że kancelaria jest większa,
  ich stawka wyższa, realizacja wyższa albo wsparcie mniejsze.

To najważniejszy wynik kursu jak dotąd, i jest to wynik o **wyborze klienta docelowego**, a nie o wycenie:

> **Sprzedawaj najpierw kancelariom, które już płacą albo są gotowe płacić za AI — i nie są spokojne o to,
> gdzie trafiają ich dane.** Mają wartość referencyjną powyżej zera i powód do zmiany. Kancelarię, która nigdy
> nie płaciła za AI, trzeba przekonać dwa razy: że AI jest warte pieniędzy i że Twój box to właściwe AI.

W praktyce to wskazuje na: kancelarie **5–15-osobowe** w miastach z wyższymi stawkami, już na LEX-ie lub
Legalisie, już eksperymentujące z ChatGPT albo Copilotem. To zgadza się z przedziałem kupujących z profilu w
repo (5–50 pracowników), zawężonym od dołu.

---

## 7. ĆWICZENIE 03 — wartość dla trzech kancelarii

W `pricing/03-value.md` policz wartość ekonomiczną dla trzech kancelarii:

1. **Kancelaria K** jak opisana.
2. **Dwuosobowa kancelaria notarialna** (jeden notariusz, jedna asystentka), alternatywa C, wartość godziny,
   którą sam wybierzesz i uzasadnisz.
3. **Dziesięcioosobowa kancelaria doradztwa podatkowego lub biuro rachunkowe**, z alternatywą, którą uważasz
   za najbardziej prawdopodobną.

Dla każdej: alternatywa, wartość referencyjna, pozycje zróżnicowania (dodatnie i ujemne), wynik kalkulatora i
cena przy przechwyceniu 20%. Potem porównaj każdą cenę przy przechwyceniu 20% ze swoją podłogą z części 02.
Napisz jedno zdanie na kancelarię: *działa / nie działa / działa tylko, jeśli …*.

Uzupełnij `pricing/01-anchors.md`: *Wartość referencyjna* i *Wartość ekonomiczna* dla Kancelarii K.

---

## 8. ⭐ EKSPERYMENT TERENOWY 03 — mierz godziny, nie opinie

**Hipoteza.** Na jednym prawdziwym procesie (na przykład triaż przychodzących pism sądowych: streszczenie,
termin, proponowany następny krok) box oszczędza prawnikowi co najmniej 10 minut na dokument w porównaniu z
pracą ręczną.

**Procedura.** Z jednym życzliwym prawnikiem weź 20 zanonimizowanych lub publicznych dokumentów takiego
rodzaju, jaki naprawdę dostaje. Przerabia 10 ręcznie i 10 z Twoim procesem, na przemian. Zmierz czas każdego.
Zapisz, ile wyników AI wymagało poprawki i ile ta poprawka trwała. Zrób to na własnym sprzęcie — to pomiar,
nie pilotaż.

**Predykcja (moja).** Ręcznie: 15–25 minut na dokument. Z procesem: 5–10 minut łącznie ze sprawdzeniem. Dwa
lub trzy wyniki na dziesięć wymagają prawdziwej poprawki.

| Dokument | Metoda | Minuty | Potrzebna poprawka? | Minuty poprawki |
| :-- | :-- | --: | :-- | --: |
| 1 | ręcznie | | — | — |
| 2 | proces | | | |
| … | | | | |

Zamień wynik na `--hours-saved`: zaoszczędzone minuty na dokument × dokumenty tygodniowo ÷ 60. **Twój pomiar
zastępuje liczbę z ankiety z sekcji 4.1.** Jeden zmierzony proces to najmocniejszy argument, jaki kiedykolwiek
przyniesiesz na spotkanie sprzedażowe.

---

## 9. Pułapki

**B42 · Wartość liczona względem złej alternatywy.**
*Objaw:* porównujesz box z Harveyem (szacowanym przez strony trzecie na 1 000–2 000 USD za użytkownika
miesięcznie) i wnioskujesz, że jest tani. *Lekarstwo:* alternatywa to to, czego użyłby **ten** klient,
zwykle „ręcznie" albo asystent za 100 zł miesięcznie.

**B43 · Założona realizacja 100%.**
*Objaw:* „3 zaoszczędzone godziny × 300 zł = 900 zł wartości tygodniowo". *Lekarstwo:* liczą się tylko
godziny, które zamieniają się w pieniądze. Zacznij od 30–50% i zapytaj klienta, co zrobiłby z tym czasem.

**B44 · Twierdzenia o „jedynej legalnej opcji".**
*Objaw:* prezentacja sprzedażowa mówi, że AI w chmurze jest zakazane dla prawników. *Dlaczego boli:* § 23e
tego nie mówi, prawnik o tym wie, a Ty właśnie straciłeś wiarygodność. *Lekarstwo:* „z boxem to pytanie się
nie pojawia".

**B45 · Wartość ryzyka w cenie.**
*Objaw:* „kara RODO może wynieść 1 mln zł, więc 1% z tego jest wart 10 000 zł". *Lekarstwo:* ryzyko należy do
opowieści, nie do liczby. `--risk-value 0`.

**B46 · Jedna cena dla wszystkich zawodów.**
*Objaw:* ten sam cennik dla notariusza i 10-osobowej kancelarii prawnej. *Lekarstwo:* wartość ekonomiczna
różni się 5–10-krotnie. Różne pakiety albo różni klienci docelowi (część 04).

---

## 10. Checkpoint

- [ ] `pricing/03-value.md` zawiera trzy kancelarie z rozpisanymi wszystkimi czterema krokami EVE.
- [ ] Każda liczba jest oznaczona jako *zmierzona*, *z researchu (źródło)* albo *założenie*.
- [ ] Potrafisz z pamięci podać sufit Kancelarii K i swoją cenę przy przechwyceniu 20%.
- [ ] Masz zapisane, jakiemu rodzajowi kancelarii będziesz sprzedawać **najpierw** i dlaczego (sekcja 6).
- [ ] Eksperyment terenowy 03 jest zaplanowany z konkretnym prawnikiem i datą.

Źródła do tej części: [ZRODLA.md](ZRODLA.md), sekcja „Część 03".
