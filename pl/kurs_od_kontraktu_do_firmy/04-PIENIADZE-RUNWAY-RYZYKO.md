# Część 04 · Pieniądze, runway i budżet ryzyka

> **Cel tej części.** Decydujesz, jaka część dochodu z kontraktu idzie na startup, ile zostaje jako bufor
> bezpieczeństwa i ile jesteś gotów stracić, zanim się zatrzymasz. Dowiadujesz się, co Twoja forma
> opodatkowania robi z wydatkami na startup, gdzie startup powinien na razie „mieszkać" podatkowo i które
> terminy administracyjne już biegną.
>
> **Czas:** ~4 h + jedno spotkanie z księgowym · **Poziom:** ⭐⭐⭐ · **Wynik:** `founder/04-budget.md`,
> `founder/04-accountant-questions.md`

> **To nie jest porada podatkowa.** Liczby to uproszczony model oparty na przepisach sprawdzonych 25 paź 2026.
> Twoje rzeczywiste liczby policzy Twój księgowy. Kilka pytań o stawki poniżej jest wprost **nierozstrzygniętych**
> — zadaj je.

---

## 0. Problem

Kontrakt dobrze płaci, więc pieniądze wydają się jedyną rzeczą, której nie trzeba planować. Dokładnie tak
założyciele w Twojej sytuacji powoli tracą roczne oszczędności: bez budżetu, bez limitu, z zakupami „na startup",
których forma opodatkowania nie pozwala odliczyć, i bez momentu, w którym przyznaliby, że pomysł nie działa.

Naprawia to **budżet ryzyka**. To kwota w złotych i liczba godzin, które jesteś gotów stracić, ustalone
**zanim** je wydasz, z warunkiem przypisanym do każdego kolejnego kroku.

---

## 1. Trzy pule

```
 dochód netto z kontraktu (część 01: ≈ 28 300 PLN/mies. na ryczałcie — zastąp to liczbą od księgowego)
   │
   ├── 1. ŻYCIE                 Twoje realne miesięczne koszty (część 01, spisana liczba)
   ├── 2. BUFOR BEZPIECZEŃSTWA  miesiące kosztów życia w gotówce, nietykalne dla startupu
   └── 3. STARTUP               budżet ryzyka, uwalniany etapami
```

### 1.1 Bufor bezpieczeństwa

Ile miesięcy kosztów życia trzymać nietkniętych? Na potrzeby tego kursu nie znaleziono sprawdzonej reguły; moim
zdaniem **6–12 miesięcy**, więcej, jeśli masz kogoś na utrzymaniu albo kredyt hipoteczny, bo kontrakt może się
skończyć z okresem wypowiedzenia — a bank może go zakończyć z powodów, które nie mają z Tobą nic wspólnego
(część 02, §4: DORA daje bankom wyraźne prawo do wypowiedzenia).

Napełnij bufor, zanim budżet startupu urośnie ponad etap walidacji.

### 1.2 Budżet ryzyka według etapów

Uwalniaj pieniądze etapami. Każdy etap ma limit i **bramkę** (warunek przejścia) — warunek, który musi być
spełniony, zanim wydasz pieniądze kolejnego etapu:

| Etap | Co kupujesz | Limit (przykład — ustal własny) | Bramka do kolejnego etapu |
| :-- | :-- | --: | :-- |
| **0 · Walidacja** (teraz → 3 miesiące) | godzina prawnika (część 02), godzina księgowego, dojazdy na rozmowy, domena, Twoje własne subskrypcje AI. Sprzęt, który już masz | 10 000 PLN | ≥ 10 rozmów, ≥ 2 kancelarie na poziomie „zobowiązanie" (kurs wyceny, część 06) |
| **1 · Pilotaże** (3 → 9 miesięcy) | jeden lub dwa boxy pilotażowe (9 000–23 000 PLN netto każdy — kurs wyceny, część 02), ubezpieczenie, prosta strona internetowa, prawnik do umowy pilotażowej | 50 000 PLN | ≥ 3 płatne pilotaże (kryterium zakończenia z samego repozytorium: *„mniej niż 3 płatne pilotaże po 4 miesiącach aktywnej sprzedaży"*), wsparcie poniżej 30% przychodu |
| **2 · Pierwsza kohorta** (9 → 18 miesięcy) | boxy dla płacących klientów (albo leasing — kurs wyceny, część 05), pomocnik na część etatu, spółka (część 06) | 150 000 PLN | ≥ 10 płacących kancelarii, miesięczny odpływ klientów (churn) < 1%, wiarygodny plan retencji przychodu netto (NRR) |

Zapisz limity **teraz**, póki jesteś spokojny. Wydanie ponad limit wymaga spełnionej bramki — nie dobrego
nastroju.

---

## 2. Co Twoja forma opodatkowania robi z wydatkami na startup

### 2.1 Na ryczałcie koszty startupu nie są odliczane

Ryczałt opodatkowuje **przychód**, nie dochód: kosztów w ogóle się nie odlicza (art. 12 ust. 2 ustawy
o zryczałtowanym podatku dochodowym). Jeśli startup działa w Twojej kontraktowej JDG, a Ty jesteś na ryczałcie,
box pilotażowy za 13 000 zł w całości pochodzi z opodatkowanych pieniędzy.

Na podatku liniowym 19% ten sam box obniżyłby podatek dochodowy i składkę zdrowotną 4,9% — wraca mniej więcej
ćwierć jego ceny.

### 2.2 To może zmienić formę? Próg opłacalności

Model z części 01 rozszerzono: ten sam przychód z kontraktu (428 400 zł rocznie), koszty startupu `S` ponoszone
przez JDG, pozostałe koszty firmowe 2% przychodu w obu wariantach:

| Wydatki na startup rocznie, `S` | Netto po wszystkim — ryczałt 12% | Netto — podatek liniowy 19% | Ryczałt korzystniejszy o |
| --: | --: | --: | --: |
| 0 | 331 213 | 304 576 | **26 637** |
| 50 000 | 281 213 | 266 526 | **14 687** |
| 100 000 | 231 213 | 228 476 | **2 737** |
| 150 000 | 181 213 | 190 044 | −8 830 |
| 200 000 | 131 213 | 151 528 | −20 315 |

**Wynik:** przy tym kontrakcie ryczałt pozostaje tańszy, dopóki koszty startupu, które dałoby się odliczyć,
nie przekroczą mniej więcej **110 000 zł rocznie**. Na etapach 0 i 1 z sekcji 1.2 jesteś daleko poniżej. Zatem:
**nie zmieniaj formy opodatkowania ze względu na startup** w pierwszym roku. Wróć do tematu, gdy etap 2 będzie
w zasięgu.

Dwa kolejne fakty zmienią to później:

- **IP Box (5% od kwalifikowanego dochodu z IP)** jest dostępny tylko na skali podatkowej albo na podatku
  liniowym, **nie na ryczałcie** (interpretacja indywidualna 0114-KDIP3-3.4011.427.2019.1.MT). Ma znaczenie,
  gdy produkt zacznie przynosić dochód z licencji — zwykle będzie to już wtedy w spółce.
- **Formę opodatkowania wybiera się na cały rok**: do 20. dnia miesiąca następującego po miesiącu, w którym
  osiągnięto pierwszy przychód w roku, bez możliwości dobrowolnej zmiany w trakcie roku (art. 9). Na 2027 rok
  będzie to najpewniej **do 20 lutego 2027**. Wpisz to teraz do kalendarza.

### 2.3 Jeśli startup zarabia w tej samej JDG

Możesz sprzedawać pilotaże przez obecną JDG, zanim powstanie spółka. Wtedy **stawka ryczałtu zależy od tego,
co sprzedajesz** — a część tej kwestii jest naprawdę nierozstrzygnięta:

| Co sprzedajesz | Stawka ryczałtu (stan na 25 paź 2026) | Pewność |
| :-- | :-- | :-- |
| instalacja, konfiguracja, doradztwo IT, zarządzanie systemami | 12% | jasne |
| czysto techniczne wsparcie IT | 8,5% dopuszczone w jednej interpretacji indywidualnej (1 wrz 2026, *źródło wtórne*) | jedna interpretacja |
| **licencje na oprogramowanie** (PKWiU 58.29.50.0) | **15%** — nie 12% | jasne |
| hosting, przetwarzanie danych | 15% | jasne |
| **oprogramowanie online / SaaS** (58.29.40.0) | wprost wyłączone z 12%; przez eliminację **8,5%**, co podobno potwierdziły dwie interpretacje z 2023 r. (niezweryfikowane) | **nierozstrzygnięte** |
| odsprzedaż boxa bez zmian | 3% (handel towarami) | jasne dla towarów nieprzetworzonych |
| box, który **konfigurujesz w nowy produkt** | być może 5,5% (produkcja) | **nierozstrzygnięte — nie znaleziono interpretacji** |

I zasada, która czyni to niebezpiecznym: różne stawki dla różnych rodzajów działalności są dozwolone **tylko
wtedy, gdy ewidencja przychodów rozdziela te strumienie**; w przeciwnym razie do całości stosuje się
**najwyższą** stawkę (art. 12 ust. 3). Próg składki zdrowotnej zależy od łącznego przychodu — i tak jesteś już
w najwyższym progu (powyżej 300 000 zł).

**Praktyczna zasada:** przed pierwszą fakturą startupu z JDG poproś księgowego o założenie osobnej kategorii
przychodu dla każdego strumienia i o opinię w sprawie stawki dla „box + instalacja + miesięczny abonament".

---

## 3. VAT i administracja, które już Cię dotyczą

| Kwestia | Fakt (stan na 25 paź 2026) | Co zrobić |
| :-- | :-- | :-- |
| **Jesteś czynnym podatnikiem VAT** | limit zwolnienia podmiotowego wynosi od 2026 r. 240 000 PLN; Twój przychód z kontraktu jest dużo wyższy | VAT naliczony od zakupów na startup, wykorzystywanych do Twojej sprzedaży opodatkowanej, podlega odliczeniu (art. 86 ustawy o VAT) — kolejny powód, by kupować sprzęt na startup przez JDG, **po tym**, jak kody PKD obejmą tę działalność |
| **PKD 2025** | każda JDG musi zaktualizować kody działalności do PKD 2025 **do 31 gru 2026**; od 1 sty 2027 CEIDG przeklasyfikuje je automatycznie, być może błędnie (gov.pl, 20 paź 2026) | zaktualizuj teraz i w tym samym kroku dodaj kody startupu |
| **KSeF** | obowiązkowe e-fakturowanie dla wszystkich od **1 kwi 2026**; kary od 1 sty 2027 | już fakturujesz bank w KSeF; faktury startupu idą tą samą drogą |

Mapowanie kodów do aktualizacji (klucz powiązań GUS, według researchu):

| Działalność | PKD 2007 | PKD 2025 |
| :-- | :-- | :-- |
| tworzenie oprogramowania (Twoja praca dla banku, agenci) | 62.01.Z | 62.10.B |
| doradztwo IT | 62.02.Z | 62.20.A lub 62.20.B |
| zarządzanie sprzętem IT | 62.03.Z | 62.20.Z |
| pozostałe usługi IT | 62.09.Z | 62.90.Z |
| przetwarzanie danych, hosting | 63.11.Z | 63.10.A–D |
| sprzedaż hurtowa sprzętu ICT | 46.51.Z | 46.50.Z |
| sprzedaż detaliczna sprzętu ICT | 47.41.Z | 47.40.Z |

Które z nich są Ci potrzebne, potwierdzi księgowy; termin nie podlega dyskusji.

---

## 4. Składki społeczne ZUS: co Cię nie dotyczy

Dla porządku, żebyś nie gonił ulg, których nie dostaniesz:

- **Pełny ZUS** w 2026 r.: 1 926,76 zł miesięcznie (podstawa 5 652 zł; 1 788,29 zł bez ubezpieczenia
  chorobowego).
- **Ulga na start** (6 miesięcy) i **preferencyjny ZUS** (456,18 zł): tylko dla nowej albo od dawna
  zawieszonej JDG — nie Twojej.
- **Mały ZUS Plus**: wymaga przychodu za poprzedni rok najwyżej 120 000 zł — nie Twój przypadek.

Te ulgi będą miały znaczenie dla wspólnika, który zakłada świeżą JDG, i wpłyną później na decyzję o formie
prawnej.

---

## 5. ĆWICZENIE 04 — budżet

`founder/04-budget.md`:

```markdown
# Budżet — <data>

Dochód netto miesięcznie (od księgowego):     ____ PLN
Życie miesięcznie:                            ____ PLN
Nadwyżka miesięcznie:                         ____ PLN

Cel bufora bezpieczeństwa: __ mies. × życie = ____ PLN   | dziś: ____ PLN
Miesięczny przelew na bufor do jego wypełnienia: ____ PLN
Miesięczny przelew na startup:                ____ PLN

Budżet ryzyka
| Etap | Limit PLN | Godziny/tydz. | Bramka | Termin |
| 0 | | | | |
| 1 | | | | |
| 2 | | | | |

Warunek stopu (spisany teraz): zatrzymuję się, jeśli ____________ do ________.
```

Oraz `founder/04-accountant-questions.md` — co najmniej te pytania:

1. Mój rzeczywisty dochód netto w 2026 r. i prognoza na 2027 r. na ryczałcie vs na podatku liniowym, przy
   kosztach startupu 20 tys., 50 tys. i 100 tys. zł.
2. Czy mogę kupować sprzęt na startup przez moją JDG i odliczać VAT? Jakie kody PKD muszę dodać?
3. Jaka stawka ryczałtu dotyczy skonfigurowanego boxa, jego instalacji, miesięcznego abonamentu, licencji?
   Jak prowadzimy osobną ewidencję przychodów?
4. W którym momencie warto przenieść startup do spółki i w jakiej formie?
5. Termin wyboru formy opodatkowania na 2027 r.

---

## 6. ⭐ EKSPERYMENT TERENOWY 04 — rzeczywiste wydatki

**Hipoteza.** Przez trzy miesiące etapu 0 rzeczywiste wydatki na startup zostaną poniżej 10 000 zł, ale godziny
przekroczą Twój plan o co najmniej 30%.

**Procedura.** Zapisuj każdą złotówkę i każdą godzinę poświęconą startupowi w `founder/04-spend.csv`
(`date,category,amount_pln_net,hours,note`). Kategorie: `legal`, `accounting`, `hardware`, `software`, `travel`,
`marketing`, `other`. Na koniec każdego miesiąca porównaj z planem.

**Predykcja (moja).** Miesiąc 1: dominują wydatki prawne i księgowe. Godziny: plan 10 tygodniowo, rzeczywistość
13–15, głównie na budowanie, a nie na rozmowy z klientami — czyli odwrotnie, niż powinno być na etapie 0.

| Miesiąc | Plan PLN | Rzeczywiście PLN | Plan h | Rzeczywiście h | Udział godzin z klientami |
| --: | --: | --: | --: | --: | --: |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

Obserwuj ostatnią kolumnę. Na etapie 0 co najmniej jedna trzecia godzin startupu powinna przypadać na ludzi
z Twoich docelowych zawodów.

---

## 7. Pułapki

**B16 · Brak warunku stopu.**
*Objaw:* „Będę wiedział, kiedy to nie działa". *Dlaczego boli:* nie będziesz — koszty utopione sprawiają, że
każdy miesiąc wydaje się tym tuż przed sukcesem. *Lekarstwo:* spisany warunek stopu z datą, ustalony przed
rozpoczęciem etapu 0.

**B17 · Zbyt wczesna zmiana formy opodatkowania dla startupu.**
*Objaw:* przejście na podatek liniowy, żeby odliczyć box za 13 000 zł. *Dlaczego boli:* przy Twoim przychodzie
z kontraktu ryczałt jest korzystniejszy, dopóki koszty startupu nie przekroczą około 110 000 zł rocznie.
*Lekarstwo:* tabela z §2.2, przeliczona przez Twojego księgowego.

**B18 · Wymieszana ewidencja przychodów.**
*Objaw:* faktury za pilotaże i faktury dla banku w jednej kolumnie przychodów. *Dlaczego boli:* do całości może
zostać zastosowana najwyższa stawka ryczałtu (art. 12 ust. 3). *Lekarstwo:* osobne kategorie przed pierwszą
fakturą startupu.

**B19 · Przegapiony termin PKD 2025.**
*Objaw:* nic nie zrobione do 31 gru 2026. *Lekarstwo:* zaktualizuj kody teraz i w tym samym kroku dodaj
działalność startupu.

**B20 · Bufor wydany na startup.**
*Objaw:* „tylko ten jeden raz" — box kupiony z bufora bezpieczeństwa. *Lekarstwo:* osobne konta dla trzech pul;
konto bufora nie ma karty.

---

## 8. Checkpoint

- [ ] `founder/04-budget.md` z trzema pulami, trzema etapami, limitami, bramkami i warunkiem stopu z datą.
- [ ] Osobne konta bankowe (albo subkonta) na bufor i na startup.
- [ ] Spotkanie z księgowym jest umówione; lista pytań jest spisana.
- [ ] Aktualizacja PKD 2025 jest zrobiona albo zaplanowana przed 31 gru 2026.
- [ ] Termin wyboru formy opodatkowania na 2027 r. jest w Twoim kalendarzu.

Źródła do tej części: [ZRODLA.md](ZRODLA.md), sekcja „Część 04".
