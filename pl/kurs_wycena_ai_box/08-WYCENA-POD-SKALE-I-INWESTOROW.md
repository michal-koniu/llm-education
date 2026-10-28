# Część 08 · Wycena pod skalę: jak cena wygląda w oczach inwestora

> **Cel tej części.** Patrzysz na swoją wycenę tak, jak patrzy na nią inwestor — albo kupiec firmy: nie jak na
> cenę za kancelarię, ale jak na **jakość przychodu**, który ona generuje. Poznajesz cztery liczby, które o tej
> jakości decydują, i planujesz, jak cena będzie się zmieniać, gdy katalog agentów będzie rósł. Decydujesz, co
> optymalizować — zależnie od tego, czy finansujesz się z własnych środków (bootstrapping), czy pozyskujesz
> kapitał.
>
> **Czas:** ~4 h · **Poziom:** ⭐⭐⭐⭐ · **Efekt:** `pricing/08-scale.md` · **Narzędzie:**
> `narzedzia/pricing_model.py nrr`

---

## 0. Problem

Dwie firmy mają po 2 miliony zł przychodu. Jedna sprzedała 150 boxów z niską marżą i opłatami za instalację.
Druga ma 90 kancelarii płacących abonament, który rośnie co roku, bo dokupują agentów. Inwestor wyceni drugą
na kilkukrotność pierwszej — choć przychód jest taki sam. Jeśli chcesz firmy, która się skaluje, cennik to nie
tylko sposób, w jaki zarabiasz w tym roku: decyduje o tym, ile firma jest warta.

---

## 1. Nie każdy przychód jest równy

| Rodzaj przychodu | Powtarza się? | Marża | Jak traktują go inwestorzy |
| :-- | :-- | :-- | :-- |
| **Abonament** (opłata za platformę + agenci) | ✅ co miesiąc | wysoka, rosnąca ze skalą (część 02) | rdzeń: roczny przychód powtarzalny (**ARR**) = miesięczny przychód powtarzalny × 12 |
| **Opłaty wdrożeniowe i za pilotaż** | ❌ raz | średnia (praca) | przydatna gotówka, niska wartość |
| **Odsprzedany sprzęt** | ❌ raz | cienka | wartość bliska zeru; może szkodzić, bo obniża łączną marżę |
| **Wynajmowany sprzęt** (w ramach abonamentu) | ✅ | średnia | powtarzalny, ale kapitałochłonny; zobacz dane o HaaS poniżej |

Dane o wycenach (wszystko to dane własne firm lub dane doradców; sprawdzaj daty):

| Dana | Wartość | Źródło |
| :-- | :-- | :-- |
| Prywatne firmy SaaS, mnożnik wyceny | **4,8× ARR** finansowane z własnych środków, **5,3× ARR** finansowane kapitałem inwestorów | SaaS Capital, styczeń 2025 (brak znalezionej aktualizacji z 2026) |
| Mediana EV/przychód w fuzjach i przejęciach SaaS | 3,8× (2025), 3,1× (I kw. 2026) | Aventis Advisors |
| Fuzje i przejęcia, od 2015 do połowy 2025, EV/przychód | oprogramowanie **3,0×**, sprzęt **1,4×**, usługi IT **1,3×** | Aventis Advisors |
| Firmy typu sprzęt jako usługa (HaaS) a inne technologie przełomowe | mediana mnożnika przychodu **o 59% wyższa**; typowy okres zwrotu ~15 miesięcy | SVB / First Citizens, *State of HaaS* 2024 |

Przeczytaj trzeci wiersz z myślą o swoim produkcie: ta sama złotówka przychodu jest warta mniej więcej
**dwa razy więcej**, jeśli kupujący widzi ją jako oprogramowanie, niż jeśli widzi ją jako sprzęt albo usługi IT.
To Twój cennik decyduje, na co wygląda.

---

## 2. Cztery liczby

### 2.1 Roczny przychód powtarzalny (ARR)

Liczy się tylko abonament. Wdrożenia i sprzęt raportuj osobno (pułapka B53 w części 05).

### 2.2 Marża brutto

Z części 02. Punkty odniesienia: mediana publicznych firm SaaS ~77% (PitchBook); produkty AI 45% w 2025,
53% oczekiwane w 2026 (ICONIQ, *dane własne firmy*); mediana docelowej marży firm AI ~50% (Growth Unhinged
2026). Esej SaaStr przekonuje, że większość metryk SaaS „działa" dopiero przy marży brutto 75%+ i retencji
przychodu netto 100%+. Dla Twojego boxa planem z części 02 jest **55–65% w latach 1–2, 70%+ w miarę
dodawania agentów**.

### 2.3 Retencja przychodu brutto (GRR)

Odsetek zeszłorocznego przychodu powtarzalnego, który zachowujesz, licząc tylko straty (odchodzące kancelarie,
przejścia na niższy pakiet). Benchmarki: mediana GRR około **91%** dla prywatnych firm B2B SaaS z roczną
wartością kontraktu poniżej 250 tys. USD (SaaS Capital 2025); Benchmarkit podaje spadek z 88% do 84% w 2026
(*źródło wtórne*). Dla bardzo małych firm często przytacza się miesięczny odpływ klientów (churn) na poziomie
**3–7%** (*źródła wtórne*), a SaaStr zauważa, że firmy z bardzo małymi klientami często tracą 3%+ miesięcznie.

Ta ostatnia liczba jest dla Ciebie zagrożeniem: 3% miesięcznie to jedna trzecia klientów utracona w ciągu roku.
Kancelarie na umowach 12-miesięcznych, z Twoim boxem przechowującym ich zaindeksowane archiwum, powinny
odchodzić znacznie rzadziej — ale to hipoteza. Zmierz to na pierwszej kohorcie.

### 2.4 Retencja przychodu netto (NRR)

Odsetek zeszłorocznego przychodu powtarzalnego, który **ci sami** klienci płacą Ci w tym roku, łącznie z tym,
co **dokupili**. Powyżej 100% oznacza, że firma rośnie, nawet jeśli nie podpiszesz żadnego nowego klienta.

Benchmarki: mediana NRR **101%** (Benchmarkit 2025); **102%** dla kontraktów o wartości 25–50 tys. USD rocznie,
rosnąca wraz z wielkością kontraktu (SaaS Capital 2025); około 98% dla najmniejszych kontraktów (odczytane
z wykresu — niepewne). SaaS dla małych firm często jest poniżej 100%.

**To tu mieszka Twoja strategia.** Katalog agentów (część 04) to maszyna do NRR: każdy agent dodany
w istniejącej kancelarii to przychód bez nowej sprzedaży.

---

## 3. Uruchom: od czego zależy NRR?

```bash
python3 pricing_model.py nrr                                  # przypadek bazowy
python3 pricing_model.py nrr --churn 0.03 --expansion 0.03    # odpływ jak w małych firmach
python3 pricing_model.py nrr --churn 0.005 --expansion 0.06   # lojalne kancelarie, mocny katalog
```

Jedna kohorta 100 kancelarii na pakiecie *Office* (1 790 zł), 12 miesięcy, agenci po 390 zł, indeksacja 3,6%
przy odnowieniu (CPI GUS za 2025):

| Miesięczny odpływ | Kancelarie dodające jednego agenta miesięcznie | GRR | **NRR** |
| --: | --: | --: | --: |
| 1,0% | 0% (brak katalogu), bez indeksacji | 89% | **89%** |
| 3,0% | 3% | 69% | **78%** |
| 1,0% | 3% | 89% | **99%** |
| 1,0% | 6% | 89% | **106%** |
| 0,5% | 6% | 94% | **113%** |

Trzy lekcje:

1. **Bez nowych agentów się kurczysz.** Nawet przy niskim odpływie box ze stałym zestawem funkcji traci
   11% przychodu rocznie. Sama indeksacja go nie uratuje.
2. **Odpływ wygrywa z ekspansją.** Przy odpływie typowym dla małych firm (3% miesięcznie) nawet dobry katalog nie
   utrzyma NRR na poziomie 100%. Twoje pierwsze zadanie to sprawić, żeby trudno było od boxa odejść:
   zaindeksowane archiwum, log audytowy, zmierzone godziny, relacja.
3. **Katalog, który co miesiąc lub dwa dostarcza agenta wartego dokupienia, zamienia biznes w taki, który
   rośnie jak procent składany.** 6% kancelarii dodających agenta co miesiąc to około 70% kancelarii
   dodających jednego w ciągu roku — wiarygodne tylko wtedy, gdy nowi agenci są naprawdę przydatni. To
   zobowiązanie produktowe, a nie sztuczka cenowa.

---

## 4. Jak cena powinna się zmieniać, gdy rośniesz

| Etap | Co robi cena | Dlaczego |
| :-- | :-- | :-- |
| **Pilotaże (0–5 kancelarii)** | płatny pilotaż; cena dla partnera startowego (−20%, kończy się po 12 miesiącach) | kupuje dowody: studia przypadków, zmierzone godziny |
| **Pierwsza kohorta (5–30)** | cennik v1; żadnych improwizowanych rabatów | mierzy prawdziwy odpływ i prawdziwą ekspansję |
| **Katalog (30–100)** | nowi agenci wyceniani według własnej zmierzonej wartości; pakiety przecięte na nowo tak, by Office zawierał najczęściej kupowanych agentów | utrzymuje Office jako oczywisty wybór, gdy katalog rośnie |
| **Dowód wartości (100+)** | podnieś ceny katalogowe dla nowych klientów; rozważ **wycenę za wynik dla jednego wąskiego agenta**, którego rezultat da się policzyć (zaakceptowane streszczenie pisma, złożony dokument) | wycena za wynik działa przy wąskich, mierzalnych zadaniach (Intercom Fin, 0,99 USD za rozwiązaną sprawę) — a wielu kupujących i tak woli przewidywalność (Decagon) |

O podnoszeniu cen: wynik Marna i Rosiello „1% → 11,1% zysku" (część 01) najbardziej dotyczy firmy,
która przestała sprzedawać ceną. Twoja pierwsza podwyżka to oznaka siły, a nie chciwości — o ile Twoje NRR
i studia przypadków ją uzasadniają.

---

## 5. Bootstrapping czy VC: co optymalizować

Mówiłeś, że możesz wystartować z finansowaniem VC albo bez niego. Priorytety cenowe są różne:

| | **Finansowany z własnych środków (bootstrapping)** | **Finansowany przez VC** |
| :-- | :-- | :-- |
| Zasób deficytowy | gotówka | czas (tempo wzrostu) |
| Optymalizuj | opłaty wdrożeniowe, przedpłatę roczną, modele A/C dla sprzętu (część 05) | wzrost ARR, NRR, marżę brutto; wynajem (model D) staje się możliwy dzięki kapitałowi inwestorów |
| Zaakceptuj | wolniejszy wzrost | przepalanie gotówki, większe rozwodnienie, jeśli wzrost jest powolny |
| Cennik powinien pokazywać | rentowność od pierwszej kancelarii | model przychodu, który rośnie jak procent składany (katalog, NRR > 100%) |
| Pytanie inwestora | — | *„Dlaczego to stanie się firmą software'ową, a nie firmą usług IT?"* — odpowiedz marżą brutto i NRR |

Co inwestorzy deklarują, że wolą: w ankiecie Growth Unhinged z 2026 roku inwestorzy wybrali wycenę
**hybrydową** (35%), potem za wynik (26%), za użycie (24%), stałą (10%) i za stanowisko (5%) (*dane własne
firmy*). Twoja opłata za platformę plus katalog agentów to hybryda w tym sensie, w jakim rozumieją ją
inwestorzy: opłata bazowa plus część zmienna, która rośnie wraz z użyciem.

W polskim kontekście finansowania VC sprawdź, czego oczekują fundusze pre-seed, program PFR Starter i czy
Twoje obecne umowy lub zatrudnienie pozwalają pozyskiwać kapitał bez ich utraty.

---

## 6. ĆWICZENIE 08 — plan skali

W `pricing/08-scale.md`:

1. Zapisz swój **cel ARR** na miesiąc 12 i miesiąc 36 oraz ile kancelarii × który pakiet to oznacza.
2. Uruchom `nrr` ze swoimi założeniami. Zapisz wskaźniki odpływu i ekspansji, których potrzebujesz do NRR ≥ 100%.
3. Wypisz agentów, których musiałbyś dostarczyć, żeby osiągnąć taki wskaźnik ekspansji — z miesiącem przy każdym.
4. Wybierz: *bootstrapping* albo *VC* na najbliższe 12 miesięcy. Zapisz jedną decyzję cenową, która z tego
   wynika (np. „wynajem tylko z przedpłatą roczną").
5. Zapisz warunki swojej pierwszej podwyżki ceny katalogowej.

---

## 7. ⭐ EKSPERYMENT TERENOWY 08 — pierwsza kohorta, zmierzona

**Hipoteza.** W ciągu pierwszych 6 miesięcy pierwsza kohorta płacących kancelarii (≥ 5) ma miesięczny odpływ
poniżej 1%, a co najmniej jedna kancelaria na pięć dokupuje agenta bez proszenia jej dwa razy.

**Procedura.** Od pierwszej płacącej kancelarii prowadź `pricing/cohort.csv`: miesiąc, kod kancelarii, pakiet,
agenci, opłata miesięczna, wypowiedziana (tak/nie). Co miesiąc licz przychód kohorty względem miesiąca 0.
W miesiącu 6 uruchom `nrr` ze zmierzonym miesięcznym odpływem i ekspansją i porównaj z planem.

**Predykcja (moja).** Odpływ 0 w pierwszych sześciu miesiącach (umowy 12-miesięczne) i jedna lub dwie
kancelarie dokupujące agenta — **tylko** jeśli w tych miesiącach rzeczywiście został wydany nowy agent.

| Miesiąc | Kancelarie | MRR (PLN) | Dodani agenci | Wypowiedzenia | Przychód kohorty względem miesiąca 0 |
| --: | --: | --: | --: | --: | --: |
| 0 | | | — | — | 100% |
| 3 | | | | | |
| 6 | | | | | |

---

## 8. Pułapki

**B67 · Całkowity przychód zamiast ARR.**
*Objaw:* „zrobiliśmy w tym roku 1,2 mln zł", w większości sprzęt i wdrożenia. *Lekarstwo:* raportuj ARR, marżę
brutto i sprzęt osobno, zawsze.

**B68 · Wzrost przez rabat.**
*Objaw:* nowe kancelarie podpisane z rabatem −30%, żeby dobić do liczby. *Dlaczego boli:* rabaty korelują
z odpływem (część 07), więc spada NRR, którego potrzebujesz. *Lekarstwo:* tabela rabatów i nic poza nią.

**B69 · Katalog, który stanął.**
*Objaw:* ostatni agent wyszedł osiem miesięcy temu. *Lekarstwo:* zależy od tego NRR (sekcja 3). Planuj agentów
jak wydania, z datami.

**B70 · Wycena za wynik zbyt wcześnie.**
*Objaw:* „5 zł za przetworzone pismo", zanim potrafisz wiarygodnie policzyć, czym jest przetworzone pismo.
*Lekarstwo:* wycena za wynik tylko dla jednego wąskiego agenta, po miesiącach zmierzonych wyników — i tylko
wtedy, gdy klienci o to proszą.

---

## 9. Checkpoint — i koniec kursu

- [ ] `pricing/08-scale.md` z celami ARR, obliczeniem NRR i planem agentów.
- [ ] Decyzja na najbliższe 12 miesięcy: bootstrapping albo VC, i reguła cenowa, która z niej wynika.
- [ ] `pricing/cohort.csv` istnieje, nawet jeśli jest pusty.
- [ ] **Otwórz `pricing/00-gut-price.md` z części 01.** Porównaj swoją cenę „na czuja" z `price-book-v1.md`.
      Napisz jeden akapit: co się zmieniło i która część zmieniła to najbardziej.

To ostatnie porównanie jest oceną tego kursu — ta sama idea co powtórzony pomiar na końcu
`kurs_aplikacje_agentowe/19-CAPSTONE.md`. Jeśli Twój cennik jest identyczny z ceną „na czuja", albo Twoje
przeczucie było bardzo dobre, albo kurs niczego Cię nie nauczył. Twoje pomiary rozstrzygną, które z dwojga.

Źródła do tej części: [ZRODLA.md](ZRODLA.md), sekcja „Część 08".
