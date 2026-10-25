# Część 02 · Podłoga kosztowa: ile naprawdę kosztuje Cię jedna kancelaria

> **Cel tej części.** Liczysz najniższą cenę miesięczną, przy której obsługa jednej kancelarii nadal ma
> sens biznesowy, i odkrywasz, która pozycja kosztowa o tym decyduje. Spoiler: to nie sprzęt.
>
> **Czas:** ~4 h · **Poziom:** ⭐⭐⭐ · **Wynik:** `pricing/02-cost-floor.md`, pierwsza wypełniona sekcja
> `pricing/01-anchors.md` · **Narzędzie:** `narzedzia/pricing_model.py floor`

---

## 0. Problem

Box *wygląda* na biznes sprzętowy: mini PC ze 128 GB na półce u prawnika. Pierwszy odruch to więc wycenić go
jak sprzęt: cena zakupu plus marża. Ale sprzęt to koszt jednorazowy, a klient widzi jego cenę na Ceneo. To,
co kosztuje Cię co miesiąc, niewidocznie, to **Twój czas**: odbieranie telefonu, wgrywanie aktualizacji
modeli, ponowne uruchamianie zestawu ewaluacyjnego, naprawianie zablokowanej kolejki OCR, dojazd do
kancelarii, gdy box nie chce się uruchomić.

Repo już nazywa to ryzyko: *„marża na sprzęcie jest cienka, a wsparcie pracochłonne; zysk musi pochodzić
z miesięcznej licencji i powtarzalnych procesów”* (`asymetrie-biznesowe-ai/02-OKAZJE.md`, profil 1),
z kryterium porzucenia *„miesięczne wsparcie przekracza 30% przychodu”*. Ta część zamienia te zdania
w liczbę.

---

## 1. Dwa rodzaje kosztów

| | **Koszt własny sprzedaży (COGS)** | **Koszty operacyjne (OpEx)** |
| :-- | :-- | :-- |
| Co | ile musisz wydać, żeby utrzymać działanie **jeszcze jednego** klienta | ile wydajesz na prowadzenie firmy, niezależnie od liczby klientów |
| Przykłady dla boxa | godziny wsparcia, udział w aktualizacjach modeli, monitoring, przestrzeń na kopie zapasowe, sprzęt, jeśli jest Twój, części zamienne | budowa nowych agentów, sprzedaż, marketing, biuro rachunkowe, Twoja własna pensja, narzędzia |
| Rośnie wraz z | liczbą kancelarii | decyzjami, które podejmujesz |
| Płacony z | ceny | **marży brutto** (cena − COGS) |

**Marża brutto** = (cena − COGS) ÷ cena. To część każdej złotówki, która zostaje na opłacenie wszystkiego
innego: rozwoju produktu, sprzedaży i Ciebie.

Dlaczego ta linia ma znaczenie: inwestorzy wyceniają złotówkę wysokomarżowego przychodu powtarzalnego
kilka razy wyżej niż złotówkę przychodu niskomarżowego (część 08). A dla Ciebie, jeszcze zanim pojawią się
inwestorzy, marża brutto decyduje o tym, czy dokładanie klientów czyni Cię bogatszym, czy tylko bardziej
zajętym.

### Marże dla porównania

| Rodzaj biznesu | Typowa marża brutto | Źródło |
| :-- | :-- | :-- |
| Publiczne spółki SaaS (mediana) | ~77% | PitchBook, Q4 2025 |
| Produkty AI (2025 → 2026 → plan na 2027) | 45% → 53% → 59% | ICONIQ *State of AI* 2026, *dane własne firmy* |
| Firmy AI, cel (mediana) | ~50% | Growth Unhinged 2026, *dane własne firmy* |
| Biznesy AI, szacunek strukturalny | 50–60% wobec 60–80%+ dla klasycznego SaaS | a16z, 2020 |
| Szybko skalujące się firmy AI („Supernovas”) | ~25% | Bessemer *State of AI* 2025 |
| Samsara (sprzęt sprzedawany w ramach abonamentu) | ~77–78% non-GAAP | wyniki spółki |
| Nutanix po przejściu z urządzeń na abonament | 83% non-GAAP (Q4 FY2020) | wyniki spółki |

Dla Ciebie najważniejsze są dwa ostatnie wiersze. Samsara i Nutanix dostarczają sprzęt i obie osiągnęły marże
jak w oprogramowaniu, **traktując sprzęt jako koszt abonamentu, a nie jako produkt z własną marżą**. Toast
poszedł dalej i sprzedawał sprzęt ze stratą (ok. −12% powtarzalnego zysku brutto, według konferencji
wynikowej), bo płacił za niego abonament.

---

## 2. Pozycje kosztowe jednej kancelarii

Wszystkie kwoty to **PLN netto, bez VAT**. ⚠️ Ceneo i Apple pokazują konsumentom ceny **brutto**. Zanim ich
użyjesz, podziel je przez 1,23 (pułapka B38).

### 2.1 Sprzęt (ceny sprawdzone 25 października 2026)

| Box | Brutto (Ceneo / Apple) | **Netto** | Mieści się w jednorazowym odpisie do 10 000 PLN? (część 05) |
| :-- | --: | --: | :-- |
| Minisforum MS-S1 MAX, Ryzen AI Max+ 395, 128 GB | 13 490–18 190 | **10 967–14 789** | nie (tuż powyżej) |
| HP Pro Max Edge, Ryzen AI Max+ 395, 128 GB | 19 999 | 16 259 | nie |
| Mac mini M5 Pro, 64 GB | ~13 094 | ~10 645 | nie (tuż powyżej) |
| Mac mini M5 Pro, 48 GB | 11 099 | 9 024 | **tak** |
| ASUS Ascent GX10 (GB10, 128 GB / 1 TB) | od 26 999 | 21 950 | nie |
| NVIDIA DGX Spark Founders Edition, 4 TB | 28 355 | 23 053 | nie |
| Mac Studio M5 Max, 128 GB | ~24 734 | ~20 109 | nie |

NVIDIA podniosła cenę referencyjną DGX Spark 128 GB z 3 999 USD do 4 699 USD w lutym 2026 z powodu niedoboru
pamięci (CHIP.pl). **Ceny sprzętu się zmieniają. Nigdy nie wpisuj ceny sprzętu do umowy bez daty ważności.**

To, jakiego poziomu sprzętu potrzebuje dana kancelaria, jest decyzją techniczną omówioną
w `asymetrie-biznesowe-ai/03-NAJPIERW-LOKALNIE.md`, sekcja 3. Dla wyceny liczą się dwa fakty:

- czy box należy do **Ciebie** (model wynajmu) — wtedy jego amortyzacja jest Twoim COGS;
- czy do **klienta** (kupuje go albo leasinguje) — wtedy w ogóle nie jest Twoim COGS.

### 2.2 Instalacja

Rozpakowanie, obraz systemu boxa, podłączenie folderu z dokumentami kancelarii, OCR istniejącego archiwum,
konta użytkowników, pierwszy proces dostrojony na ich dokumentach, godzina szkolenia. **Zmierz to**
(eksperyment terenowy 02). Dopóki nie masz pomiaru, zakładaj 16 godzin na każdą z pierwszych dziesięciu
instalacji.

Jeśli instalację pokrywa **opłata wdrożeniowa** (a powinna), instalacji nie ma w podłodze miesięcznej.
W takim przypadku uruchom kalkulator z `--install-h 0`.

### 2.3 Wsparcie i monitoring

Pytania przez telefon i e-mail, zablokowana kolejka, użytkownik, który zapomniał hasła, zapełniający się dysk,
sesja zdalna. To pozycja, która decyduje o Twojej podłodze. Inżynieria z tego repo — health check, rollback
w mniej niż 5 minut i runbook na 3 w nocy z `kurs_aplikacje_agentowe/18-WYDANIE-I-UTRZYMANIE.md` — to
**bezpośrednie obniżenie kosztu własnego sprzedaży**: każde sprawdzenie, które dzieje się automatycznie, to
godzina, której nie musisz sobie policzyć.

### 2.4 Aktualizacje modeli (współdzielone)

Wychodzi nowa wersja Bielika albo PLLuM. Pobierasz ją, uruchamiasz na swoim boxie referencyjnym, puszczasz
polski zestaw ewaluacyjny (`kurs_aplikacje_agentowe/14-EWALUACJA.md`), sprawdzasz każdego agenta pod kątem
regresji, przygotowujesz wdrożenie i wdrażasz zdalnie. Zakładaj 40 godzin na kwartał. **Tę pracę wykonujesz
raz i służy ona każdej kancelarii**, więc jej koszt na kancelarię spada wraz ze wzrostem. To pierwsza
ekonomia skali w tym biznesie.

### 2.5 Inne

Przestrzeń na kopie zapasowe, licencja na narzędzie do zdalnego zarządzania, okazjonalna część zamienna,
ubezpieczenie OC zawodowe (wycenione w kursie o umowach), dojazdy. Zakładaj 100 zł na kancelarię miesięcznie
i zastąp to prawdziwymi fakturami.

### 2.6 Cena godziny

Kalkulator potrzebuje `--hour-cost`: ile kosztuje jedna godzina pracy wsparcia. Dwie pułapki:

- **To nie jest Twoja stawka kontraktowa.** Fakturujesz bank na 1 700 zł dziennie. To cena *Twojego* czasu dla
  banku, a nie koszt pracy wsparcia. Jeśli wycenisz wsparcie według stawki bankowej, podłoga stanie się
  absurdalna i nigdy niczego nie sprzedasz.
- **To nie jest też zero.** „Robię to sam wieczorami” — tak założyciele kończą z biznesem, który potrzebuje
  ich na zawsze. Wyceń godzinę na tyle, **ile zapłaciłbyś komuś innemu** za pierwszą linię wsparcia i zdalną
  administrację. Rynkowa stawka nie została tu zbadana; domyślne 200 zł za godzinę to **założenie** —
  zastąp je wyceną od firmy usług IT, która jest zarazem Twoim przyszłym partnerem
  (`asymetrie-biznesowe-ai/02-OKAZJE.md`: *„współpracuj z nimi jako warstwa AI, z podziałem przychodu”*).

---

## 3. Uruchom to

```bash
cd narzedzia
python3 pricing_model.py floor                    # domyślnie: 10 kancelarii, 2 h wsparcia, marża 75%
```

Założenia domyślne: sprzęt należy do klienta, 16 h instalacji rozłożone na 24-miesięczną umowę, 2 h wsparcia
na kancelarię miesięcznie po 200 zł, 40 h aktualizacji modeli na kwartał dzielone przez wszystkie kancelarie,
100 zł innych kosztów, docelowa marża 75%.

Oto wyniki dla różnych liczb kancelarii i godzin wsparcia (wszystko po 200 zł za godzinę, sprzęt klienta,
instalacja nadal rozłożona w kwocie miesięcznej):

| Scenariusz | COGS / kancelaria / miesiąc | Podłoga przy marży 75% | Podłoga przy marży 60% |
| :-- | --: | --: | --: |
| 5 kancelarii, 2 h wsparcia | 1 167 | **4 667** | 2 917 |
| 20 kancelarii, 2 h wsparcia | 767 | **3 067** | 1 917 |
| 100 kancelarii, 2 h wsparcia | 660 | **2 640** | 1 650 |
| 20 kancelarii, **1 h** wsparcia | 567 | **2 267** | 1 417 |
| 20 kancelarii, **0,5 h** wsparcia | 467 | **1 867** | 1 167 |
| 20 kancelarii, 1 h, **box jest Twój** (wynajem) | 871 | **3 485** | 2 178 |

Czytaj tę tabelę powoli. Są w niej trzy lekcje:

1. **Godziny wsparcia decydują o podłodze.** Zejście z 2 h do 0,5 h na kancelarię miesięcznie obniża podłogę
   bardziej niż przejście z 20 do 100 klientów. Twój najsilniejszy ruch cenowy to ruch inżynierski: box,
   który Cię nie potrzebuje.
2. **Obsługa pierwszych kancelarii jest droga.** Przy pięciu kancelariach współdzielony koszt aktualizacji
   jest duży w przeliczeniu na kancelarię. Dlatego pierwsi klienci często dostają cenę „partnera
   startowego” (część 07): jeszcze na nich nie zarabiasz i to jest w porządku, *jeśli o tym wiesz*.
3. **Marża 75% jak w oprogramowaniu jest trudna przy cenach dla małych kancelarii.** Porównaj podłogi
   z cenami referencyjnymi z części 01: Beck-Noxtua po 590 zł za stanowisko to 2 950 zł dla kancelarii
   z 5 stanowiskami; LEX Kancelaria Prawna to 298–722 zł miesięcznie. Podłoga powyżej 3 000 zł za jedną
   kancelarię to więcej, niż Kancelaria K zwykle płaci za **całe** swoje oprogramowanie. Albo wsparcie
   spadnie do ok. 1 godziny, albo cel marżowy spadnie w stronę normy firm AI, czyli 50–60%, albo cena musi
   opierać się na argumencie wartości wystarczająco mocnym, żeby ją uzasadnić (część 03).

### 3.1 Cel marży brutto — zdecyduj teraz

Wpisz jeden z nich do `pricing/02-cost-floor.md` i napisz dlaczego:

| Cel | Kiedy to właściwy wybór |
| :-- | :-- |
| **75%+** | Planujesz pozyskać pieniądze od VC (część 08) i potrafisz zepchnąć wsparcie poniżej 1 h na kancelarię |
| **55–65%** | Norma firm AI w 2026. Realistyczny cel na lata 1–2 |
| **< 50%** | Jesteś firmą usługową. W porządku dla firmy „lifestyle'owej”, problem dla firmy, która ma się skalować |

Powiedziałeś mi, że chcesz firmy, która skaluje się przez kolejnych agentów eksperckich. To wskazuje na
55–65% teraz i plan dojścia do 70%+ w miarę dokładania agentów — bo nowy agent sprzedany istniejącej
kancelarii dodaje przychód **prawie bez nowego COGS** (box, relacja wsparcia i kanał aktualizacji już
istnieją). To druga ekonomia skali w tym biznesie i rdzeń części 04.

---

## 4. Jak podłoga spada z czasem

```
 COGS na kancelarię
   │█
   │█ █
   │█ █ ▆                       ← współdzielone aktualizacje rozłożone na więcej kancelarii
   │█ █ █ ▆ ▅
   │█ █ █ █ █ ▅ ▄ ▄ ▃ ▃ ▃       ← automatyzacja wsparcia, standardowy obraz boxa
   │█ █ █ █ █ █ █ █ █ █ █ ▂ ▂   ← jeszcze jeden agent na kancelarię: przychód w górę, COGS bez zmian
   └──────────────────────────► kancelarie / czas
```

Ceny dużo trudniej podnieść, niż obciąć koszty. Więc: **ustal cenę z wartości (część 03), a potem dopilnuj,
żeby podłoga kosztowa z czasem spadła poniżej niej.** Nigdy nie ustalaj ceny od podłogi z pierwszego
miesiąca.

---

## 5. ĆWICZENIE 02 — Twoja podłoga

1. Skopiuj wartości domyślne do `pricing/02-cost-floor.md` jako tabelę, jedna linia na założenie.
2. Zastąp każde założenie, które się da, prawdziwą liczbą: ofertą na sprzęt, stawką godzinową firmy IT,
   zmierzonym czasem instalacji (eksperyment terenowy 02).
3. Uruchom `pricing_model.py floor` dla 5, 20 i 100 kancelarii, przy wybranej przez siebie marży.
4. Wpisz do `pricing/01-anchors.md`, sekcja *Podłoga kosztowa*: **jedną liczbę** na rok 1 (przy 10
   kancelariach) i jedną na rok 3 (przy planowanej liczbie kancelarii).

---

## 6. ⭐ EKSPERYMENT TERENOWY 02 — ile trwa instalacja?

**Hipoteza.** Instalacja boxa od gołej maszyny do działającego pierwszego procesu za pierwszym razem trwa
dłużej niż dzień, a za trzecim razem krócej niż pół dnia — jeśli ją oskryptujesz.

**Procedura.** Na zapasowej maszynie (albo na maszynie wirtualnej, jeśli nie masz jeszcze zapasowego boxa)
zainstaluj od zera cały swój stos, trzy razy: system operacyjny, serwer modeli, runner agentów, wczytywanie
dokumentów, jeden proces, konto użytkownika, zadanie kopii zapasowej i health check. Zmierz każde podejście
stoperem. Po każdym podejściu oskryptuj jeden ręczny krok.

**Predykcja (moja).** Podejście 1: 10–16 h. Podejście 3: 3–5 h. Najdłuższy pojedynczy krok: OCR i indeksowanie
realistycznego archiwum dokumentów, a nie oprogramowanie.

| Podejście | Data | Łącznie godzin | Najdłuższy krok | Kroki oskryptowane po tym podejściu |
| :-- | :-- | --: | :-- | :-- |
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

Różnica między podejściem 1 a 3 to pieniądze: przy 20 kancelariach rocznie to mniej więcej 20 × (podejście 1
− podejście 3) godzin. Wynik z podejścia 3 wpisz do `--install-h`.

---

## 7. Pułapki

**B37 · Twój własny czas wyceniony na zero.**
*Objaw:* COGS zawiera sprzęt i prąd, ale nie zawiera godzin. *Lekarstwo:* każda godzina wsparcia jest wyceniona
według stawki, jaką zapłaciłbyś komuś innemu (sekcja 2.6).

**B38 · Pomieszane ceny brutto i netto.**
*Objaw:* cena z Ceneo użyta jako koszt. *Dlaczego boli:* 23% błędu na największej pozycji. *Lekarstwo:*
wszystkie wyliczenia biznesowe w PLN netto. Wpisuj „netto” w nagłówku każdej kolumny.

**B39 · Rozwój produktu liczony jako COGS.**
*Objaw:* „każdy nowy agent kosztuje mnie 80 godzin, więc cena musi to pokryć”. *Lekarstwo:* budowa nowego
agenta to OpEx (inwestycja, która służy wszystkim kancelariom). COGS to tylko praca potrzebna do utrzymania
działania **jednej** kancelarii.

**B40 · Wycena od podłogi z pierwszego miesiąca.**
*Objaw:* pierwszą cenę ustalono tak, żeby pokryła koszty obsługi pięciu kancelarii. *Lekarstwo:* cena wynika
z wartości (część 03); podłoga z pierwszego miesiąca mówi Ci, przez ile miesięcy będziesz tracić pieniądze,
a nie ile brać.

**B41 · Pełzające wsparcie.**
*Objaw:* „A mógłby Pan jeszcze zerknąć na naszą drukarkę?” — i zerkasz, za darmo. *Dlaczego boli:* wsparcie to
Twoja największa pozycja kosztowa i rośnie po cichu. *Lekarstwo:* spisany zakres wsparcia w cenniku — księdze cen (część 07)
i dziennik każdej godziny wsparcia od pierwszego pilotażu.

---

## 8. Checkpoint

- [ ] `pricing/02-cost-floor.md` zawiera tabelę założeń, każde oznaczone jako *zmierzone* albo *założone*.
- [ ] Uruchomiłeś kalkulator dla 5, 20 i 100 kancelarii.
- [ ] Wybrałeś cel marży brutto i zapisałeś jedno zdanie, dlaczego.
- [ ] `pricing/01-anchors.md`, *Podłoga kosztowa*: jedna liczba na rok 1 i jedna na rok 3.
- [ ] Eksperyment terenowy 02: przynajmniej podejście 1 jest zrobione.
- [ ] Potrafisz powiedzieć, która pojedyncza pozycja kosztowa najbardziej przesuwa Twoją podłogę i jaka
      inżynieria by ją obniżyła.

Źródła do tej części: [ZRODLA.md](ZRODLA.md), sekcja „Część 02”.
