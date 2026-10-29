# 02 · Pomiar przy rzadkich zdarzeniach

**Najważniejszy fakt:** gdy wynik, na którym Ci zależy, jest rzadki, kilka rund prawie nic nie mówi o tym, czy zmiana
pomogła. Każda zasada z [03](03-BEZPIECZNA-PETLA.md) i [04](04-KIEDY-PRZESTAC.md) wynika z tej strony. Wszystkie
liczby (O) pochodzą z [`narzedzia/rare_event_stats.py`](narzedzia/README.md); uruchom go z własnymi wartościami.

Model przez całą lekcję: trafienia przychodzą jak **proces Poissona** z tempem λ na rundę. To uproszczenie (rynki mają
godziny szczytu, dni tygodnia i sezony), ale to właściwe pierwsze przybliżenie — a rzeczywistość jest bardziej
zaszumiona, nie mniej.

---

## 1. Jak bardzo zaszumione jest „nic nie znalazłem”?

Jeśli obecny playbook znajduje trafienia w tempie λ na rundę, prawdopodobieństwo k pustych rund z rzędu wynosi
e^(−λk) **(O)**:

| λ (trafień/rundę) | P(2 puste) | P(3 puste) | P(5 pustych) | P(10 pustych) | seria potrzebna do p < 0,05 | do p < 0,01 |
|---|---|---|---|---|---|---|
| 0,1 | 0,82 | 0,74 | 0,61 | 0,37 | 30 | 47 |
| 0,2 | 0,67 | 0,55 | 0,37 | 0,14 | 15 | 24 |
| 0,3 | 0,55 | 0,41 | 0,22 | 0,05 | 10 | 16 |
| 0,5 | 0,37 | 0,22 | 0,08 | 0,01 | 6 | 10 |
| 1,0 | 0,14 | 0,05 | 0,01 | ~0 | 3 | 5 |

**Co z tego wynika (W).** Wyzwalacz w stylu „po 2–3 pustych rundach zrób refleksję i przepisz playbook” odpala się na
czystym przypadku, chyba że agent już znajduje mniej więcej jedno trafienie na rundę. Każde przepisanie to nowa
szansa, żeby coś zepsuć, a następna szczęśliwa runda „potwierdza” przepisanie. To przepis na agenta, który dryfuje,
wierząc, że się poprawia: błądzenie losowe z dorobioną historią.

Zastąp ten wyzwalacz jednym z:

- reguły długości serii skalibrowanej do zmierzonego tempa: k ≥ ln(1/p) / λ̂, przy p = 0,01;
- lepiej: poissonowskiego CUSUM z [§5](#5-pilnowanie-spadku-poissonowski-cusum), który wykorzystuje też trafienia,
  które się zdarzają;
- w pozostałych sprawach: wyzwalaczy opartych na dowodach z [04 §1](04-KIEDY-PRZESTAC.md#1-wyzwalacze-oparte-na-dowodach).

## 2. Ile trafień trzeba, żeby pokazać, że zmiana pomogła?

Uruchom **mistrza** (obecny playbook, A) i **pretendenta** (B) z równą ekspozycją, na przykład na zmianę albo
losując rundy. Teraz warunkuj na łącznej liczbie trafień n. Jeśli B nie jest lepszy, każde trafienie z równym
prawdopodobieństwem pochodzi od A i od B, więc porównanie sprowadza się do dokładnego testu dwumianowego z p0 = 0,5.
Jeśli tempo B jest R razy większe niż A, trafienie pochodzi od B z prawdopodobieństwem p1 = R/(1+R). To test
warunkowy, który implementuje `poisson.test` w R **(D)**.

Łączna liczba trafień potrzebna do mocy 80%, test jednostronny **(O)**:

| Efekt do wykrycia | α = 0,05: trafień łącznie | rund na ramię przy λ = 0,1 / 0,3 / 1,0 | α = 0,10: trafień łącznie | rund na ramię przy λ = 0,1 / 0,3 / 1,0 |
|---|---|---|---|---|
| +25% (R = 1,25) | 502 | 2232 / 744 / 224 | 370 | 1645 / 549 / 165 |
| +50% (R = 1,5) | 158 | 632 / 211 / 64 | 115 | 460 / 154 / 46 |
| ×2 | 58 | 194 / 65 / 20 | 39 | 130 / 44 / 13 |
| ×3 | 23 | 58 / 20 / 6 | 19 | 48 / 16 / 5 |

**Przeczytaj tę tabelę, zanim cokolwiek zaprojektujesz (W):**

- Przy 0,1–0,3 trafienia na rundę nawet *podwojenie* wymaga 44–194 rund na ramię. Przy rundzie co 15 minut to od
  pół dnia do dwóch dni na ramię — *o ile świat stoi w miejscu*.
- Zysk +25% jest na samych trafieniach praktycznie niemierzalny.
- Agent, który przepisuje playbook co kilka rund, nie ma więc jak się dowiedzieć, czy którekolwiek przepisanie pomogło.
- Nierówny podział kosztuje. Gdy pretendent dostaje ułamek f rund zamiast połowy, łączna liczba rund rośnie
  ok. 1/(4f(1−f)) razy: ×1,33 przy f = 0,25 **(O)**. I tak warto, bo ogranicza szkody ze złego pretendenta.

## 3. Wyjścia z sytuacji, od najcenniejszego

**1. Oceniaj offline, na zamrożonych danych, wszystko, co się da.** Logikę oceny (dopasowanie przedmiotu, cenę
referencyjną, sygnały ostrzegawcze, próg trafienia) można odtworzyć na zarchiwizowanych ogłoszeniach. Każdy kandydat,
któremu agent kiedykolwiek się przyjrzał, staje się oznaczonym przykładem: setki tygodniowo zamiast kilku trafień.
Zob. złoty zbiór i korpus migawek w [03 §3](03-BEZPIECZNA-PETLA.md#3-zamrożone-zasoby-do-oceny).

**2. Online używaj gęstszych wskaźników wyprzedzających.** Na przykład prawie-trafień (ogłoszeń w pewnej odległości
procentowej od progu), kandydatów po wstępnym sicie na rundę, pokrycia katalogu. Przy 5 prawie-trafieniach na rundę
zmiana o +25% wymaga ok. 502 / (5 × 2,25) ≈ 45 rund na ramię zamiast 744 **(O)**. Wskaźniki zastępcze łatwo oszukać
([03 §9](03-BEZPIECZNA-PETLA.md#9-goodhart-jak-wygląda-oszukiwanie-i-strukturalna-ochrona)), więc używaj ich tylko do
*przyspieszenia* decyzji; główna metryka i tak musi przejść test „nie gorzej”.

**3. Małych zmian w ogóle nie testuj online.** Zbierz je w wydanie zweryfikowane offline albo pozwól, żeby bandyta
([03 §5](03-BEZPIECZNA-PETLA.md#5-bandyta-do-alokacji-zamiast-przepisywania)) wchłonął je jako zmianę alokacji.

**Powtórka ma twardą granicę (D, Li i in. 2011).** Odtworzenie zapisanych danych offline jest nieobciążone tylko tam,
gdzie nowa polityka podjęłaby to samo działanie co zapisana. Powtórka oceni nowy *filtr* na starych wynikach
wyszukiwania. Nie oceni *zapytania, którego nikt nie uruchomił*. Zatem **zmiany oceny da się testować offline;
zmiany zapytań i źródeł trzeba testować online**, przez bandytę albo przełączanie **(W)**.

## 4. Reguły decyzji dla małych, zaszumionych prób

**Przy małym n używaj metod dokładnych albo bayesowskich, a nie przedziałów z centralnego twierdzenia granicznego.**
Bowyer, Aitchison i Ivanova (ICML 2025) pokazują, że zwykłe przedziały średnia ± 1,96·SE „dramatycznie zaniżają
niepewność” poniżej „kilkuset punktów danych” **(Z, streszczenie)**.

**Paruj, co się da.** Oceniaj mistrza i pretendenta na *tych samych* pozycjach. Miller („Adding Error Bars to Evals”)
podaje błędy standardowe dla par i dla klastrów; te drugie bywają ponad 3× większe od naiwnych **(D)**. U agenta
klastruj po dniu albo po źródle, bo rundy z jednego dnia dzielą warunki rynkowe **(W)**.

**Na złotym zbiorze używaj dokładnego testu McNemara.** Policz b = pozycje, które mistrz ocenia dobrze, a pretendent
źle, oraz c = odwrotnie. Pozycje, które obaj oceniają dobrze albo obaj źle, nie niosą informacji. Przy braku różnicy
c ma rozkład Binomial(b + c; 0,5). Deklarowaną poprawę przyjmij tylko, gdy c > b i jednostronne p < 0,05:

```bash
python3 narzedzia/rare_event_stats.py mcnemar --b 3 --c 11      # p = 0,029 → przyjąć
python3 narzedzia/rare_event_stats.py mcnemar --b 20 --c 23     # naprawia 23, psuje 20 → p = 0,38 → odrzucić
```

**Będziesz zaglądać, więc używaj testu sekwencyjnego.** Wyniki będziesz oglądać po każdej rundzie, a p-wartość dla
ustalonego horyzontu traci sens przy ciągłym podglądaniu. Mieszany SPRT Johariego, Pekelisa i Walsha daje p-wartości
„zawsze ważne” **(D)**. Najprostsza poprawna opcja przy przypisywaniu trafień to **SPRT Walda na tym, z którego
ramienia pochodzi każde trafienie (O)**:

- Zaprojektuj test na stosunek R. Przy udziale pretendenta f w rundach: p0 = f oraz p1 = Rf / (1 − f + Rf). Przy
  równej ekspozycji to p0 = 0,5 i p1 = R/(1+R).
- Każde trafienie pretendenta dodaje ln(p1/p0). Każde trafienie mistrza dodaje ln((1−p1)/(1−p0)). Puste rundy nie
  dodają nic.
- Przyjmij pretendenta, gdy suma dojdzie do ln((1−β)/α); odrzuć go, gdy spadnie do ln(β/(1−α)). Przy α = 0,05
  i β = 0,2 granice wynoszą **+2,77 i −1,56**.

Zachowanie w symulacji, równa ekspozycja **(O)**:

| Projekt | Za trafienie pretendenta | Za trafienie mistrza | Gdy pretendent nie jest lepszy | Gdy pretendent jest tak dobry, jak zakładano |
|---|---|---|---|---|
| R = 2 | +0,288 | −0,405 | błędnie przyjęty w 4,6%; decyzja po ~26 trafieniach (90. percentyl 54) | przyjęty w 83%; po ~37 trafieniach (90. percentyl 70) |
| R = 1,5 | +0,182 | −0,223 | błędnie przyjęty w 4,6%; ~71 trafień | przyjęty w 82%; ~101 trafień |

To mniej więcej połowa z 58 trafień testu o stałym horyzoncie z §2 — *i* wolno zaglądać po każdym trafieniu.

**Alternatywa bayesowska.** Trzymaj rozkład a posteriori Gamma dla każdego ramienia, licz P(λ_B > λ_A | dane)
i zatrzymaj się, gdy oczekiwana strata z wyboru prowadzącego spadnie poniżej „progu, od którego Ci zależy”
(Stucchio). Łatwo to wytłumaczyć, ale przy dowolnym momencie zatrzymania *nie* kontroluje fałszywych alarmów **(D)**.
Połącz z minimalną liczbą prób i maksymalnym czasem trwania **(W)**.

**Bootstrap tylko dla metryk wartości o ciężkich ogonach**, np. wartości na rundę, i tylko jako **bootstrap blokowy
po dniach**. Przy mniej niż ~20 trafieniach na ramię jest zawodny, więc wartość traktuj jako barierkę, nie jako
metrykę decyzyjną **(W)**.

**Uwzględnij klątwę zwycięzcy.** Jeśli refleksja wygeneruje k kandydatów, a Ty zostawisz najlepiej wyglądającego, jego
zmierzony zysk jest zawyżony (Lee i Shen, KDD 2018) **(D)**. Testuj jednego pretendenta naraz; jeśli kilku odsiano
offline, wymagaj potwierdzenia w świeżym oknie; w prognozach dziel zmierzony zysk przez dwa **(W)**.

**Prawo Twymana.** Każda liczba, która wygląda ciekawie albo nietypowo, zwykle jest błędna (Kohavi i in.).
Pretendent, który „potraja trafienia”, ma najpierw uruchomić audyt pod kątem oszustwa, błędu w logowaniu albo zmiany
definicji, a dopiero potem awans.

**pass^k przy niedeterministycznych przebiegach.** Jeśli Twój silnik nie jest powtarzalny bit w bit (llama.cpp
z cache promptu nie jest, zob. [03 §12](03-BEZPIECZNA-PETLA.md#12-uwagi-o-harnessie-i-silniku)), jeden przebieg
złotego zbioru to jedna próbka, a nie wynik. Na pozycjach obowiązkowych wymagaj zaliczenia we wszystkich k ≥ 3
przebiegach, gdzie indziej — większości z k.

## 5. Pilnowanie spadku: poissonowski CUSUM

Żeby zauważyć, że tempo trafień spadło z λ0 do λ1, trzymaj jedną liczbę S, zaczynając od 0, i po każdej rundzie
z x trafieniami aktualizuj ją (Page 1954; Lucas 1985, „Counted Data CUSUMs”) **(D)**:

```
S = max(0, S + x·ln(λ1/λ0) − (λ1 − λ0))        alarm, gdy S > h
```

Każda pusta runda dodaje λ0 − λ1; każde trafienie odejmuje. W kodzie to trzy linie:

```python
import math
def cusum_step(S, hits, lam0=0.3, lam1=0.15):
    return max(0.0, S + hits * math.log(lam1 / lam0) - (lam1 - lam0))
```

Długości serii z symulacji **(O)**:

| Pilnujemy spadku | h | Średnio rund do fałszywego alarmu | 10. percentyl fałszywego alarmu | Średnio rund do wykrycia spadku |
|---|---|---|---|---|
| 0,3 → 0,15 | 3 | ~430 | 71 | ~51 |
| 0,3 → 0,15 | 4 | ~1270 | 178 | ~72 |
| 0,3 → 0,15 | 5 | ~3590 | 448 | ~95 |
| 1,0 → 0,5 | 3 | ~180 | 27 | ~17 |
| 1,0 → 0,5 | 4 | ~530 | 73 | ~23 |

Nawet dobrze dostrojony detektor potrzebuje **ok. 50–100 rund**, żeby potwierdzić, że tempo 0,3 spadło o połowę. To
uczciwe opóźnienie monitorowania rzadkich zdarzeń i żaden spryt go nie usunie. Rozsądne ustawienie przy λ0 = 0,3 to
h ≈ 4: fałszywy alarm mniej więcej co 1300 rund. Przeliczaj λ0 przy każdej zmianie mistrza **(O/W)**.

**Dla metryk ciągłych** (mediana różnicy ceny, liczba ogłoszeń na zapytanie, sekundy na rundę) używaj
**Page–Hinkleya**: m_T = Σ(x_t − x̄_T − δ), M_T = min m_t, alarm, gdy m_T − M_T > λ. δ toleruje drobne wahania;
λ wymienia fałszywe alarmy na opóźnienie (przegląd Gamy i in. 2014; domyślne w scikit-multiflow δ = 0,005,
λ = 50) **(D)**.

**Kontrole zdrowia przed statystyką.** Większość „dryfu” w agencie, który przegląda strony, to awarie: zmieniony
układ strony, blokada albo limit zapytań, wygasłe logowanie. Pilnuj zapytań z zerem wyników, odsetka błędów
parsowania i błędów HTTP zwykłymi progami. Te zdarzenia są częste i binarne; nie potrzebują CUSUM **(W)**.

## 6. Zero zdarzeń i nowe źródła

Przy 0 trafień w n rundach 95-procentowa górna granica tempa wynosi ok. **3/n** („reguła trzech”) **(O)**. 30 pustych
rund na nowym źródle wciąż dopuszcza tempo do 0,1 na rundę, czyli być może tyle, ile daje Twoje najlepsze źródło.
Nigdy nie wycofuj nowego źródła po krótkiej pustej serii; daj mu gwarantowany budżet prób
([03 §5](03-BEZPIECZNA-PETLA.md#5-bandyta-do-alokacji-zamiast-przepisywania)).

## 7. Ćwiczenia

Uruchom je z liczbami *Twojego* agenta. Zapisz odpowiedzi, zanim zaprojektujesz pętlę.

```bash
cd pl/agenty-samodoskonalace/narzedzia
python3 rare_event_stats.py empty --rates 0.15                  # jak długa pusta seria jest prawdziwym dowodem?
python3 rare_event_stats.py power --ratios 1.25 1.5 2 --rates 0.15 --proxy 4
python3 rare_event_stats.py sprt --ratio 1.5 --share 0.25       # pretendent z 25% rund
python3 rare_event_stats.py cusum --rate0 0.15 --rate1 0.075 --h 3 4
python3 rare_event_stats.py shadow --max-n 30                   # zob. 03 §7
```

1. Ile rund na ramię potrzebowałaby zmiana o +50% przy Twoim zmierzonym λ? Ile to dni kalendarzowych?
2. Ile zmian tej wielkości zdołasz zweryfikować w miesiącu? Ta liczba to Twój **budżet oceny**, a częstość refleksji
   powinna się do niego dopasować ([03 §11](03-BEZPIECZNA-PETLA.md#11-kto-prowadzi-refleksję-i-jak-często)).
3. Jaki gęstszy wskaźnik zastępczy możesz zacząć logować od jutra i co zrobi z odpowiedzią na pytanie 1?

---

Dalej: [03 · Bezpieczna pętla](03-BEZPIECZNA-PETLA.md).
