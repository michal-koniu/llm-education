# Kurs: wycena prywatnego AI boxa — indeks

**Utworzono 25 października 2026. Dla Michała.**
Część ścieżki biznesowej: pierwszy kurs to
[Od kontraktu B2B do własnej firmy](../kurs_od_kontraktu_do_firmy/00-INDEKS.md). Ten kurs zakłada, że przeczytałeś
`asymetrie-biznesowe-ai/` (okazja 1, *Prywatny AI box dla polskich kancelarii i biur*) oraz
`asystenci-ai/02-RYNEK.md`.

> **Cel całości.** Po tym kursie masz **cennik — księgę cen** — prywatnego AI boxa: pakiety, ceny agentów
> eksperckich, opłaty wdrożeniowe, warianty sprzętowe, rabaty i warunki. Każda liczba ma w nim źródło:
> wyliczenie, pomiar albo rozmowę z kupującym. I wiesz, jak z tego cennika robi się firma, która rośnie
> przez dokładanie agentów, a nie przez dokładanie boxów.

> **To nie jest porada podatkowa, prawna ani inwestycyjna.** Ceny, przepisy i dane rynkowe zmieniają się co
> miesiąc. Fakty według stanu na 25 października 2026; sprawdź je jeszcze raz, zanim zaczniesz działać.

---

## Teza, na której stoi cały kurs

> **Box nie sprzedaje tokenów. Sprzedaje pozwolenie, odzyskane godziny i spokój — więc jego cena musi
> wynikać z wartości, a nie ze sprzętu.**

Analiza kosztów w tym repo już pokazała, że lokalny box nie wygrywa z tanim API na koszcie tokenów
(`asymetrie-biznesowe-ai/03-NAJPIERW-LOKALNIE.md`). To nie jest słabość biznesu — to informacja, za co brać
pieniądze. Jeśli wycenisz box jak sprzęt, konkurujesz z Ceneo. Jeśli wycenisz go jako rozwiązanie dla
tajemnicy zawodowej i oszczędności czasu, konkurujesz z alternatywami, jakie ma kancelaria — a produktem staje
się katalog agentów.

⭐ **W części 03 sprawdzisz tę tezę na liczbach.** Wynik jest mniej wygodny niż teza: działa ona dla jednych
kancelarii, a dla innych nie — i to właśnie mówi Ci, komu sprzedawać najpierw.

---

## Ścieżka

```
  BLOK I · TRZY LICZBY ────────────────────────────── ~11 h
   01 podstawy              podłoga, wartość referencyjna, wartość ekonomiczna; jak wycenia się AI w 2026
   02 podłoga kosztowa ⭐   ile kosztuje Cię jedna kancelaria — decydują godziny wsparcia, nie sprzęt
   03 sufit wartości  ⭐⭐  ile box jest wart dla Kancelarii K — i wynik targetowania
              │
  BLOK II · OFERTA ────────────────────────────────── ~8 h
   04 metryka wartości ⭐⭐ za kancelarię + agenci eksperccy; good/better/best; katalog jako silnik
   05 sprzęt                klient kupuje / odsprzedaż / leasing / wynajem — i Twoja gotówka
              │
  BLOK III · DOWODY I PAPIERY ─────────────────────── ~10 h + tygodnie rozmów
   06 gotowość        ⭐⭐  drabina dowodów, Van Westendorp i Gabor-Granger po polsku, płatne pilotaże
   07 cennik                ceny, rabaty, indeksacja, zakres wsparcia, partnerzy
              │
   08 SKALA ───────────────► ARR, marża brutto, NRR; bootstrapping vs VC; ocena kursu
```

⚠️ **Nie przeskakuj do części 07.** Cennik napisany przed częściami 02, 03 i 06 to cena „na oko” z części 01,
tylko ładnie sformatowana.

---

## Pliki

| # | Plik | Poziom | Czego się nauczysz | Czas |
| :-- | :-- | :-- | :-- | :-- |
| 01 | `01-PODSTAWY-WYCENY.md` | ⭐⭐ | trzy liczby; tryby porażki według Ramanujama; wycena za stanowisko vs za zużycie vs za efekt w latach 2025–2026 | ~3 h |
| 02 | `02-PODLOGA-KOSZTOWA.md` | ⭐⭐⭐ | COGS vs OpEx, marża brutto, **dlaczego to godziny wsparcia wyznaczają Twoją podłogę** | ~4 h |
| 03 | `03-SUFIT-WARTOSCI.md` | ⭐⭐⭐ | szacowanie wartości ekonomicznej (Economic Value Estimation) dla kancelarii; § 23e; **wszystko rozstrzyga alternatywa** | ~4 h |
| 04 | `04-METRYKA-WARTOSCI-I-PAKIETY.md` | ⭐⭐⭐⭐ | metryka wartości, **katalog agentów eksperckich**, lider / wypełniacz / zabójca (leader / filler / killer), good / better / best (dobry / lepszy / najlepszy) | ~4 h |
| 05 | `05-SPRZET-I-GOTOWKA.md` | ⭐⭐⭐⭐ | cztery modele sprzętowe, **Twoje zapotrzebowanie na gotówkę**, leasing, perspektywa podatkowa i VAT klienta | ~4 h |
| 06 | `06-GOTOWOSC-DO-ZAPLATY.md` | ⭐⭐⭐⭐ | drabina dowodów, **pytania o cenę po polsku**, płatne pilotaże, uczciwość przy małej próbie | ~6 h + tygodnie |
| 07 | `07-CENNIK-I-WARUNKI.md` | ⭐⭐⭐ | spisany cennik, polityka rabatowa, indeksacja o CPI, zakres wsparcia, marże partnerów | ~4 h |
| 08 | `08-WYCENA-POD-SKALE-I-INWESTOROW.md` | ⭐⭐⭐⭐ | roczny przychód powtarzalny (ARR), marża brutto, **retencja przychodu netto (NRR) z katalogu agentów**, mnożniki wycen, bootstrapping vs VC | ~4 h |
| — | `narzedzia/pricing_model.py` | — | kalkulator: `floor`, `value`, `cash`, `vw`, `gg`, `nrr` (tylko biblioteka standardowa Pythona) | — |
| — | `ZRODLA.md` | — | każda liczba ze źródłem, datą i etykietą; **najsłabsze punkty wypisane na początku** | — |

**Razem: ~33 godziny przy biurku plus 2–4 tygodnie rozmów z kancelariami.** Tak jak kursy techniczne, ten kurs
nie jest do czytania. Większość wartości jest w eksperymentach terenowych.

---

## Anatomia każdej części

Ten sam szkielet co w kursach technicznych, przełożony na biznes:

```
0. Problem — dlaczego to pytanie ma znaczenie dla boxa
1-N. Teoria — ze źródłem każdej liczby
   ⭐ „Jak robią to inni” — prawdziwe firmy i ich ceny
TWOJE LICZBY — kalkulator uruchomiony z Twoimi założeniami
ĆWICZENIE — tworzy plik w Twoim folderze pricing/
⭐ EKSPERYMENT TERENOWY — hipoteza, procedura, tabela DO WYPEŁNIENIA, moja predykcja
Pułapki — numerowane B31–B70, z objawem i lekarstwem
Checkpoint — co MUSI istnieć przed następną częścią
```

⭐ **Eksperyment terenowy jest sednem każdej części.** Każdy ma **predykcję** — co spodziewam się, że
znajdziesz — i pustą tabelę. **Gdy się rozjadą, Twój pomiar wygrywa i popraw kurs.** Rozmowa z jedną
prawdziwą kancelarią jest warta więcej niż każda liczba w tym kursie.

---

## Zasady, których trzymam się przez cały kurs

1. **Zawsze ceny netto.** Wszystkie kwoty to PLN netto, bez VAT, chyba że kolumna mówi *brutto* (B38).
2. **Każda liczba ma etykietę:** *zmierzona*, *zbadana (źródło)* albo *założona*. Liczba bez etykiety to
   zgadywanie udające fakt.
3. **Jedna cena, nie przedział.** Przedziału nie da się obalić (B35).
4. **Pytaj o przeszłość, nie o przyszłość.** Ludzie uczciwie opisują to, co zrobili, a optymistycznie to, co by
   zrobili (B57).
5. **Jedynym dowodem są pieniądze.** Słowa < zobowiązanie < pieniądze < odnowienie (część 06).
6. **Twój folder roboczy `pricing/` leży poza każdym publicznym repo.** Znajdą się w nim informacje
   o prawdziwych kancelariach (B36).
7. **Pułapki są numerowane w całej ścieżce biznesowej:** B1–B30 w kursie dla założyciela, **B31–B70 tutaj**.

---

## Przykład przewodni: Kancelaria K

Fikcyjna kancelaria w średniej wielkości polskim mieście: **dwóch adwokatów, jeden aplikant, dwóch
asystentów**. Płaci za prawniczą bazę danych, część jej prawników już wkleja różne rzeczy do ChatGPT,
a starszy partner martwi się § 23e. Każde wyliczenie w kursie robisz najpierw dla Kancelarii K. Zastąp ją
prawdziwą kancelarią, gdy tylko z jakąś przeprowadzisz rozmowę.

---

## Rejestr pułapek — B31–B70

| ID | Pułapka | Część |
| :-- | :-- | --: |
| B31 | Wycena koszt-plus dla produktu, który sprzedaje wartość | 01 |
| B32 | Wycena technologii zamiast wykonanej pracy | 01 |
| B33 | Kopiowanie ceny z USA przez kurs walut | 01 |
| B34 | Ustalanie ceny po zbudowaniu produktu | 01 |
| B35 | Przedział zamiast ceny | 01 |
| B36 | Dane klientów w publicznym repozytorium | 01 |
| B37 | Twój własny czas wyceniony na zero | 02 |
| B38 | Pomieszane ceny brutto i netto | 02 |
| B39 | Rozwój produktu liczony jako COGS | 02 |
| B40 | Wycena od podłogi z pierwszego miesiąca | 02 |
| B41 | Pełzające wsparcie | 02 |
| B42 | Wartość policzona względem złej alternatywy | 03 |
| B43 | Założona realizacja 100% | 03 |
| B44 | Hasła „jedyna legalna opcja” | 03 |
| B45 | Wartość ryzyka w cenie | 03 |
| B46 | Jedna cena dla wszystkich zawodów | 03 |
| B47 | Wycena za stanowisko dla boxa, którego koszt nie zależy od liczby stanowisk | 04 |
| B48 | Licznik zużycia dla małego kupującego | 04 |
| B49 | Darmowy agent | 04 |
| B50 | Zabójcy wewnątrz pakietu | 04 |
| B51 | Pakiety projektowane według funkcji, a nie według kupujących | 04 |
| B52 | Wzrost szybszy niż Twoja gotówka | 05 |
| B53 | Przychód ze sprzętu pokazywany jako wzrost | 05 |
| B54 | Cena sprzętu bez daty ważności | 05 |
| B55 | Ignorowanie sytuacji VAT klienta | 05 |
| B56 | Podnajem leasingowanych boxów bez zgody leasingodawcy | 05 |
| B57 | „Kupiłby Pan to?” | 06 |
| B58 | Prezentacja, zanim wysłuchasz | 06 |
| B59 | Przyjaciele i rodzina jako próba | 06 |
| B60 | Wynik ankiety odczytany jako fakt | 06 |
| B61 | Darmowy pilotaż | 06 |
| B62 | Improwizowany rabat | 07 |
| B63 | Brak klauzuli indeksacyjnej | 07 |
| B64 | Zakres wsparcia tylko w Twojej głowie | 07 |
| B65 | Ceny bez numeru wersji | 07 |
| B66 | Marża partnera z kieszeni klienta | 07 |
| B67 | Całkowity przychód zamiast ARR | 08 |
| B68 | Wzrost dzięki rabatom | 08 |
| B69 | Katalog, który staje w miejscu | 08 |
| B70 | Wycena za efekt wprowadzona za wcześnie | 08 |

---

## Czego ten kurs nie zawiera — i dlaczego

| Czego brakuje | Dlaczego |
| :-- | :-- |
| **Pogłębionego odkrywania klientów (customer discovery)** | Część 06 obejmuje rozmowę o cenie. Pełny kurs o znajdowaniu kupujących i rozmowach z nimi jest planowany osobno (kurs 2 w propozycji) |
| **Prawa umów** | Część 07 mówi, co klauzule mają osiągnąć; ich brzmienie należy do prawnika i do planowanego kursu o umowach |
| **Twoich własnych podatków** | To, jak *Twoja* firma księguje przychód, jest w kursie dla założyciela, część 04, i w planowanym kursie o formie prawnej |
| **Modelu finansowego całej firmy** | Kalkulator obejmuje ekonomikę jednej kancelarii i gotówkę na sprzęt; pełny model na 36 miesięcy to planowany kurs finansowy |

---

## Zanim zaczniesz

```bash
cd narzedzia
python3 --version                       # oczekuj >= 3.12
python3 pricing_model.py --help         # sześć podkomend
python3 pricing_model.py floor          # wartości domyślne z części 02
mkdir -p ~/founder/pricing              # Twój prywatny folder roboczy — NIE w publicznym repo
```
