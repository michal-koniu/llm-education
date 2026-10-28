# Część 06 · Gotowość do zapłaty: zmierz ją, nie zgaduj

> **Cel tej części.** Mierzysz, ile zapłacą kancelarie, do których celujesz — najpierw w słowach, potem
> zobowiązaniem, a na końcu pieniędzmi. Prowadzisz ustrukturyzowaną rozmowę o cenie z pytaniami Van Westendorpa
> i Gabora-Grangera po polsku i projektujesz płatny pilotaż, który powie Ci więcej niż jakakolwiek ankieta.
>
> **Czas:** ~6 h plus 2–4 tygodnie rozmów · **Poziom:** ⭐⭐⭐⭐ · **Efekt:**
> `pricing/06-interviews/`, `pricing/06-wtp.md` · **Narzędzia:** `pricing_model.py vw`, `pricing_model.py gg`

---

## 0. Problem

Części 02–05 dały Ci podłogę, sufit i strukturę. Wszystko pomiędzy to wciąż Twoja opinia. Jedyni ludzie, którzy
wiedzą, ile zapłaci Kancelaria K, to ludzie, którzy prowadzą kancelarie takie jak Kancelaria K. Zapytaj ich —
ale tak, żeby nie dostać grzecznych kłamstw.

---

## 1. Drabina dowodów

Nie wszystkie odpowiedzi są równe. Od najsłabszej do najmocniejszej:

```
  5  ODNOWIENIE          zapłacili, używali i zapłacili znowu        ← jedyny dowód
  4  PIENIĄDZE           płatny pilotaż, zaliczka, podpisane zamówienie
  3  ZOBOWIĄZANIE        list intencyjny, spotkanie ze wspólnikiem, ich dokumenty do testu
  2  DEKLAROWANA CENA    odpowiedzi na pytania o cenę (ankiety z tej części)
  1  OPINIA              „ciekawe", „na pewno byśmy używali"         ← bezwartościowe dla wyceny
```

Każdy szczebel w górę kosztuje klienta coś — czas, reputację, pieniądze — i właśnie ten koszt sprawia, że
odpowiedź jest prawdziwa. **Projektuj każdą rozmowę tak, żeby wejść co najmniej o jeden szczebel wyżej.**
Rozmowa, która kończy się na poziomie 1, była miłą pogawędką, a nie badaniem.

---

## 2. Rozmowa, zanim padną pytania

Madhavan Ramanujam (*Monetizing Innovation*) nalega, żeby rozmawiać o gotowości do zapłaty **zanim** zaczniesz
budować — i żeby robić to jako rozmowę o wartości, a nie jako „ile by Pan zapłacił?". Kolejność, która działa:

1. **Ich praca, w czasie przeszłym.** *„Proszę opowiedzieć o ostatnim piśmie z sądu, które do Państwa
   przyszło. Co Pan/Pani z nim zrobił(a)? Ile to zajęło?"* (Jeszcze bez produktu.)
2. **Ich obecne wydatki.** *„Ile płacą Państwo dziś za oprogramowanie? Kto o tym zdecydował?"* (EKSPERYMENT
   TERENOWY 01.)
3. **Waga problemu.** *„Gdyby to zajmowało pięć minut zamiast dwudziestu, co zrobił(a)by Pan/Pani z tym
   czasem?"* — to Twój współczynnik *realizacji* z części 03.
4. **Koncepcja, krótko.** Jeden akapit i — jeśli masz — dwuminutowe demo na publicznych dokumentach.
5. **Pytania o cenę** (sekcje 3–4).
6. **Prośba** — szczebel w górę drabiny: *„Czy da mi Pan/Pani dziesięć zanonimizowanych pism do testu?"*,
   *„Czy możemy pokazać to Pana/Pani wspólnikowi w przyszłym tygodniu?"*, *„Czy zaczęlibyśmy płatny pilotaż
   w styczniu?"*

Nigdy nie prezentuj produktu przed krokiem 4. Gdy zaczniesz go zachwalać, przestają opowiadać o swojej pracy
i zaczynają być grzeczni wobec Twojego produktu.

---

## 3. Van Westendorp: cztery pytania

Price Sensitivity Meter (Peter van Westendorp, ESOMAR Congress, 1976). Zadaj cztery pytania o **jeden
konkretny pakiet** opisany w jednym akapicie — na przykład pakiet *Office* z części 04, z ceną miesięczną
i osobną opłatą wdrożeniową. Pytaj o cenę miesięczną.

| Kod | Sens pytania | Polski (do rozmowy) |
| :-- | :-- | :-- |
| `too_cheap` | Przy jakiej cenie miesięcznej byłoby to tak tanie, że zwątpiłbyś w jakość? | Przy jakiej miesięcznej cenie byłoby to tak tanie, że zaczął(-ęła)by Pan/Pani wątpić w jakość? |
| `cheap` | Przy jakiej cenie miesięcznej byłaby to okazja — dobry zakup za te pieniądze? | Przy jakiej cenie uznał(a)by Pan/Pani, że to okazja — dobry zakup za te pieniądze? |
| `expensive` | Przy jakiej cenie miesięcznej zaczęłoby to być drogie, ale nadal brałbyś to pod uwagę? | Przy jakiej cenie zaczęłoby to być drogie, ale nadal brał(a)by to Pan/Pani pod uwagę? |
| `too_expensive` | Przy jakiej cenie miesięcznej byłoby to tak drogie, że w ogóle nie brałbyś tego pod uwagę? | Przy jakiej cenie byłoby to tak drogie, że w ogóle nie brał(a)by Pan/Pani tego pod uwagę? |

Zapisz odpowiedzi w CSV, jeden wiersz na osobę, PLN netto miesięcznie:

```csv
too_cheap,cheap,expensive,too_expensive
300,600,1200,2000
500,800,1500,2500
```

Potem:

```bash
python3 pricing_model.py vw pricing/06-interviews/vw.csv
```

### 3.1 Jak narzędzie czyta krzywe

Z czterech odpowiedzi buduje cztery krzywe skumulowane i znajduje cztery punkty przecięcia:

| Punkt | Przecięcie (konwencja przyjęta w tym narzędziu) | Znaczenie |
| :-- | :-- | :-- |
| **PMC** — punkt krańcowej taniości (point of marginal cheapness) | „za tanio" × „nie tanio" (1 − tanio) | poniżej niego zbyt wielu ludzi wątpi w jakość |
| **OPP** — optymalny punkt cenowy (optimal price point) | „za tanio" × „za drogo" | tyle samo osób odrzuca produkt jako zbyt tani, co jako zbyt drogi |
| **IPP** — punkt obojętności cenowej (indifference price point) | „tanio" × „drogo" | tyle samo osób nazywa to okazją, co nazywa to drogim — często czytany jako cena „normalna" |
| **PME** — punkt krańcowej drogości (point of marginal expensiveness) | „za drogo" × „nie drogo" (1 − drogo) | powyżej niego zbyt wielu odrzuca produkt |

⚠️ Praktycy i narzędzia dostawców stosują **nieco różne konwencje**, zwłaszcza dla PMC, PME i OPP (niektórzy
krzyżują „za tanio" z „drogo" zamiast z „nie tanio"). Tylko IPP jest prawie wszędzie zdefiniowany tak samo.
Zawsze podawaj, której konwencji użyłeś, i porównuj wyniki tylko w obrębie jednej konwencji.

**Akceptowalny przedział: od PMC do PME.** Jeśli Twoje zróżnicowanie jest wyraźne (część 03), ustaw cenę
w górnej połowie przedziału, powyżej IPP.

### 3.2 Wielkość próby — Twoje uczciwe ograniczenie

Wytyczne dostawców dla Van Westendorpa: **co najmniej 30** respondentów, żeby wykres cokolwiek znaczył,
zalecane **100–200** (co najmniej 100 na segment); Qualtrics używa 300. Ty będziesz mieć **10–20** rozmów.
Dlatego:

- używaj czterech pytań jako **ustrukturyzowanej rozmowy**, nie jako ankiety;
- czytaj wynik jako **kierunek** („nasz przedział to mniej więcej 900–1 600, a nie 300–600"), nigdy jako liczbę;
- właśnie z tego powodu narzędzie wypisuje ostrzeżenie poniżej n = 30.

Podstawowa metoda **nie** szacuje też, ilu klientów kupi przy danej cenie. Do tego potrzebujesz następnej
sekcji — a jeszcze lepiej pieniędzy (sekcja 5).

---

## 4. Gabor-Granger: tak albo nie przy danej cenie

Metoda Gabora-Grangera (André Gabor i Clive Granger, lata 60.) zadaje pytanie o zakup przy kolejnych cenach
i buduje krzywą popytu. W rozmowie:

> *„Gdyby pakiet Office kosztował 1 200 zł netto miesięcznie, zdecydował(a)by się Pan/Pani?"* — tak → zapytaj
> o wyższą cenę; nie → zapytaj o niższą. Zatrzymaj się przy pierwszej zmianie odpowiedzi.

Użyj czterech cen rozłożonych w Twoim przedziale Van Westendorpa. **Zaczynaj od losowej** dla każdej osoby
(albo od wysokiej), żeby pierwsza cena nie zakotwiczyła wszystkich.

Zbierz odsetek odpowiedzi „tak" przy każdej cenie ze wszystkich rozmów i uruchom:

```bash
python3 pricing_model.py gg 900:0.70 1200:0.55 1500:0.35 1800:0.20 --cost 570
```

Narzędzie pokazuje przychód i **zysk brutto** na potencjalnego klienta przy każdej cenie, korzystając z Twojego
kosztu obsługi (COGS) z części 02, i wybiera spośród testowanych cen tę, która maksymalizuje zysk brutto.
Deklarowany zamiar **zawyża** rzeczywiste zakupy — traktuj odsetki jako górną granicę i porównuj ceny ze sobą,
a nie z rzeczywistością.

---

## 5. Pieniądze: płatny pilotaż

Najmocniejszy dowód, jaki możesz zdobyć przed startem. Profil okazji w repo już to sugeruje: *„płatny
pilotaż 3 000–5 000 PLN, potem wdrożenie + abonament"*. Zaprojektuj go tak, żeby testował **cenę**, a nie
tylko produkt.

| Element | Rekomendacja |
| :-- | :-- |
| **Czas trwania** | 6–8 tygodni — wystarczająco długo, żeby kancelaria przestała być grzeczna i zaczęła używać |
| **Cena** | płatny, nigdy darmowy. 3 000–5 000 zł netto to wyjściowa hipoteza z repo |
| **Zakres** | jeden agent-lider (część 04), na własnych dokumentach kancelarii, na Twoim boxie albo ich |
| **Kryteria sukcesu — spisane przed startem** | np. „≥ 8 minut oszczędności na piśmie przy ≥ 30 pismach, ≤ 1 na 5 wyników wymagający realnej poprawki" |
| **Klauzula konwersji** | opłata za pilotaż jest **zaliczana na poczet opłaty wdrożeniowej**, jeśli podpiszą umowę w ciągu 30 dni od końca |
| **Cena po pilotażu** | **zapisana w umowie pilotażowej**. Pilotaż bez ceny „po" testuje produkt, nie cenę |
| **Wyjście** | jeśli kryteria nie zostaną spełnione, nie są Ci winni nic więcej, a Ty zabierasz box |

Dlaczego cena po pilotażu musi być w umowie pilotażowej: jeśli ogłosisz cenę dopiero po udanym pilotażu,
kancelaria już ustaliła w głowie, ile to jest „warte" — zwykle cenę pilotażu w przeliczeniu na miesiąc.
Tracisz kotwicę.

**List intencyjny** (poziom 3) to wyjście awaryjne, gdy na pilotaż jest za wcześnie: jednostronicowe,
niewiążące pismo, w którym kancelaria deklaruje zamiar kupna pakietu *Office* za X zł miesięcznie, jeśli
kryteria pilotażu zostaną spełnione. Niewiążące, ale ludzie rzadko podpisują cenę, którą uważają za absurdalną.

---

## 6. Czytanie dowodów przy małych liczbach

Przy dziesięciu rozmowach jedna osoba zmienia wynik o 10 punktów procentowych. Zasady:

1. **Szukaj zgodności, nie średnich.** „Siedem z dziesięciu osób umieszcza *za drogo* powyżej 1 800 zł" to
   wniosek; „średnia wynosi 1 537 zł" to szum z miejscami po przecinku.
2. **Segmentuj, zanim uśrednisz.** Notariusz i 10-osobowa kancelaria w jednej średniej nie opisują nikogo
   (pułapka B46).
3. **Waż według drabiny.** Jeden płatny pilotaż za 1 500 zł miesięcznie waży więcej niż dziesięć deklarowanych
   cen po 800 zł.
4. **Zapisz, co zmieniłoby Twoje zdanie**, zanim spojrzysz na dane — dokładnie tak jak predykcje
   w eksperymentach kursu.

---

## 7. ĆWICZENIE 06 — zestaw do wywiadów

Utwórz `pricing/06-interviews/`:

- `script.md` — sześciokrokowa rozmowa z sekcji 2 po polsku, z opisem Twojego pakietu w jednym akapicie;
- `vw.csv` — pusty, z wierszem nagłówka;
- `gg.md` — Twoje cztery ceny testowe i tabela tak/nie;
- `log.md` — jedna linia na rozmowę: data, zawód, wielkość, miasto, osiągnięty szczebel drabiny, następny krok.

Niczyje nazwisko nie trafia do tych plików. Używaj kodu (`L01`, `N02` dla prawnika lub notariusza).

---

## 8. ⭐ EKSPERYMENT TERENOWY 06 — dziesięć kancelarii, dwa pilotaże

**Hipoteza.** Wśród dziesięciu kancelarii prawnych lub podatkowych liczących 4–15 osób, które już płacą za
oprogramowanie, akceptowalny przedział Van Westendorpa dla pakietu *Office* leży mniej więcej między 900 a 2 000 zł
netto miesięcznie, a co najmniej dwie kancelarie zgadzają się na płatny pilotaż za 3 000–5 000 zł.

**Procedura.** Dziesięć rozmów według `script.md`. Cztery pytania Van Westendorpa, potem Gabor-Granger przy
czterech cenach, potem sortowanie lider/zabójca z części 04, potem prośba. Zapisuj wszystko w plikach
z ćwiczenia 06. Zaproponuj płatny pilotaż każdej kancelarii, która dojdzie do poziomu 3.

**Predykcja (moja).** IPP w okolicach 1 200–1 500 zł. Mniej niż połowa kancelarii dochodzi do poziomu 3.
Dwa pilotaże — ale tylko od kancelarii, które już płacą za chmurowe AI prawnicze albo za premium bazę prawniczą
(wynik targetowania z części 03).

| Wynik | Wartość |
| :-- | :-- |
| Przeprowadzone rozmowy | |
| PMC / OPP / IPP / PME (konwencja: to narzędzie) | |
| Gabor-Granger: cena maksymalizująca zysk brutto | |
| Kancelarie na poziomie 3 (zobowiązanie) | |
| Uzgodnione płatne pilotaże i za jaką cenę | |
| Co mnie zaskoczyło | |

---

## 9. Pułapki

**B57 · „Kupiłby Pan to?"**
*Objaw:* kluczowe pytanie jest hipotetyczne i dotyczy przyszłości. *Dlaczego boli:* ludzie są uprzejmi
i optymistyczni. *Lekarstwo:* pytaj o przeszłość i proś o szczebel wyżej na drabinie.

**B58 · Prezentacja przed słuchaniem.**
*Objaw:* demo startuje w drugiej minucie. *Lekarstwo:* najpierw kroki 1–3 z sekcji 2, zawsze.

**B59 · Przyjaciele i rodzina jako próba.**
*Objaw:* kancelaria Twojego kuzyna to trzy z Twoich dziesięciu odpowiedzi. *Lekarstwo:* najwyżej jeden ciepły
kontakt na dziesięć, oznaczony w logu.

**B60 · Liczba z ankiety czytana jako fakt.**
*Objaw:* „optymalna cena to 1 347 zł". *Lekarstwo:* przy n < 30 tylko przedział i kierunek.

**B61 · Darmowy pilotaż.**
*Objaw:* „Niech sprawdzą za darmo przez miesiąc, potem porozmawiamy o pieniądzach". *Dlaczego boli:* nie mierzy
niczego w sprawie ceny i kotwiczy wartość na zerze. *Lekarstwo:* płatny pilotaż z ceną „po" zapisaną w umowie.

---

## 10. Checkpoint

- [ ] Zestaw do wywiadów istnieje po polsku i raz przećwiczyłeś go z życzliwym prawnikiem jako próbę generalną.
- [ ] Co najmniej pięć prawdziwych rozmów jest zapisanych w logu, z osiągniętym szczeblem drabiny przy każdej.
- [ ] `vw.csv` ma co najmniej pięć wierszy i uruchomiłeś na nim `pricing_model.py vw`.
- [ ] Istnieje jeden projekt umowy pilotażowej, z kryteriami sukcesu i ceną po pilotażu.
- [ ] `pricing/06-wtp.md` podaje Twój przedział cenowy i to, co mogłoby go zmienić.

Źródła do tej części: [ZRODLA.md](ZRODLA.md), sekcja „Część 06".
