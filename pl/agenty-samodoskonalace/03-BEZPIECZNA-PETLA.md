# 03 · Bezpieczna pętla: architektura do zbudowania

Wszystko na tej stronie to **propozycja projektowa (W)**, oparta na źródłach z [01](01-CO-MOZNA-ULEPSZAC.md)
i arytmetyce z [02](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md). Stoi na czterech zasadach:

- **oddziel tego, kto robi, od tego, kto ocenia;**
- **LLM proponuje, kod i statystyka rozstrzygają;**
- **zmiany mają być małe, typowane, odwracalne i rzadkie;**
- **maszyneria ulepszania ma być poza zasięgiem agenta.**

---

## 1. Komponenty

```
               ┌───────────────────── zamrożone, należą do człowieka ─────────────────┐
               │ constitution.md   hit_rules.py (progi, koszty)   metrics.py          │
               │ złoty zbiór + obowiązkowe + ukryta część   gate_rules.yaml  wartownik│
               └──────────────────────────────────────────────────────────────────────┘
                     ▲ tylko odczyt                       ▲ tylko odczyt
┌──────────────┐  ┌──┴───────────┐  ┌──────────────┐  ┌───┴──────────┐  ┌──────────────┐
│ Wykonawca    │→ │ Harness:     │→ │ Monitor:     │→ │ Refleksja    │→ │ Bramkarz     │
│ (szybki      │  │ dzienniki    │  │ zdrowie,     │  │ (wg planu,   │  │ (czysty kod):│
│ model,       │  │ tylko do     │  │ CUSUM,       │  │ świeży       │  │ bramki, SPRT,│
│ rundy)       │  │ dopisywania, │  │ Page-Hinkley,│  │ kontekst,    │  │ awans /      │
│ czyta:       │  │ migawki,     │  │ wartownik,   │  │ ≤1 propozycja│  │ odrzucenie / │
│ playbook vN  │  │ hit_rules,   │  │ przypisanie  │  └──────────────┘  │ wycofanie,   │
│ + wybór      │  │ aktualizacja │  │ przyczyn     │                    │ wersje w git │
│   bandyty    │  │ bandyty      │  └──────────────┘                    └──────────────┘
└──────────────┘  └──────────────┘
                              cotygodniowe podsumowanie → człowiek (zatwierdza zmiany warstwy zamrożonej)
```

| Komponent | Rodzaj | Robi | Nigdy nie robi |
|---|---|---|---|
| **Wykonawca** | szybki LLM | prowadzi rundy: odpytuje wybrane ramiona, wyciąga ogłoszenia, dopasowuje przedmioty, woła ocenę trafienia | nie zapisuje playbooka w trakcie rundy |
| **Harness** | kod | dzienniki JSONL tylko do dopisywania, surowe migawki, deduplikacja; stosuje `hit_rules.py`, więc o trafieniu decyduje kod (LLM dostarcza wyciągnięte pola i pewność); aktualizuje bandytę | nie pozwala LLM decydować, co jest trafieniem |
| **Monitor** | kod | kontrole zdrowia, poissonowski CUSUM na tempie trafień, Page–Hinkley na metrykach ciągłych, uruchamia wartownika, stosuje tabelę przypisania przyczyn (§8) | niczego nie zmienia |
| **Refleksja** | LLM, według planu | w świeżym kontekście czyta metryki policzone kodem, skupiska porażek i wylosowane surowe transkrypty; wydaje **najwyżej jedną** typowaną propozycję (§4) | nie ocenia własnej propozycji; nie widzi złotych etykiet |
| **Bramkarz** | kod | prowadzi kaskadę bramek (§6), planuje A/B, prowadzi SPRT, awansuje, odrzuca, wycofuje, zapisuje wersje w git | nie przyjmuje poleceń od LLM |
| **Człowiek** | osoba | jest właścicielem warstwy zamrożonej; czyta cotygodniowe podsumowanie; oznacza rozbieżności i prawie-trafienia (najtańsze, a najcenniejsze etykiety w systemie) | nie zatwierdza bez patrzenia na dowody |

**Izolacja jest wymuszona konstrukcyjnie.** Wykonawca i refleksja działają jako użytkownik albo w piaskownicy bez
prawa zapisu do warstwy zamrożonej, dzienników i zbiorów ewaluacyjnych. Askarbekuly i in. ujmują to jako regułę R3:
izoluj stan „konstrukcyjnie, a nie instrukcją” **(Z)**. Linijka w prompcie „nie edytuj X” nie jest zabezpieczeniem.

## 2. Co może się zmieniać i przez które drzwi

Każda zmiana ma swoje **drzwi**: ocenę, którą musi przejść. Ustalenie drzwi z góry to większość projektu.

| Warstwa | Przykłady (zwiadowca) | Kto ją zmienia | Drzwi oceny |
|---|---|---|---|
| **Zamrożona: konstytucja** | cel, etyka, regulaminy serwisów i limity zapytań, „nigdy nie kupuj i nie kontaktuj się ze sprzedającymi”, budżety | tylko człowiek | n/d |
| **Zamrożona: pomiar** | `hit_rules.py` (koszty, model stanu przedmiotu, próg), kod metryk, reguły deduplikacji, zbiory ewaluacyjne, progi bramek, **sam protokół refleksji** | tylko człowiek; agent może *złożyć propozycję* | przegląd przez człowieka i ponowna ocena historii offline |
| **Strojone przez kod** | które ramię uruchomić następne, częstość odwiedzin, plan dnia | bandyta (§5), nigdy LLM | ciągła; rozkład a posteriori jest oceną |
| **Katalog ramion** | nowe szablony zapytań, nowe źródła, nowe kategorie przedmiotów | refleksja proponuje; bramkarz dodaje z budżetem prób | budżet prób bandyty i reguła wycofania |
| **Heurystyki oceny** | normalizacja przedmiotów i wariantów, słowa ostrzegawcze, wybór ceny referencyjnej | refleksja proponuje, po jednej | offline: obowiązkowe, McNemar na złotym zbiorze, powtórka; potem **tryb cienia** (§7) |
| **Notatki proceduralne** | jak stronicować źródło X, obsługa logowania, „przed oznaczeniem sprawdź sprzedane ogłoszenia” | refleksja proponuje jako delty | metryki procesu (błędy, czas rundy, pokrycie) przez przełączanie; tempo trafień jako barierka „nie gorzej” |
| **Pamięć spostrzeżeń** | „sprzedający w serwisie X często podają pojemność tylko na zdjęciach” | refleksja dodaje lub edytuje po ID; **liczniki aktualizuje harness na podstawie wyników** | limit rozmiaru, deduplikacja, usuwanie pozycji, gdzie szkodliwe > pomocne |
| **Brudnopis** | notatki w obrębie jednej rundy | wykonawca | brak; wyrzucane |
| **Model i silnik** | wagi, kwantyzacja, szablon czatu, wersja silnika, sampler, rozmiar kontekstu | człowiek | **traktowane jak pretendent**: obowiązkowe, złoty zbiór i powtórka przed podmianą |

Ta tabela odpowiada na pytanie „co agent samodoskonalący się może zmieniać?”. Większość wartości jest w dolnej
połowie; większość niebezpieczeństwa w dwóch górnych wierszach.

## 3. Zamrożone zasoby do oceny

Wzorzec pochodzi z autoresearch, AlphaEvolve i DSPy: zamrożony oceniający, którego optymalizator nie może dotknąć.
autoresearch Karpathy'ego zamraża plik z danymi i oceną („Not modified”); agent może edytować tylko `train.py`; plik
z instrukcjami jest „edytowany i rozwijany przez człowieka”; każdy przebieg ma stały budżet 5 minut **(Z)**.

Askarbekuly i in. (2026) uruchamiali takie pętle z produkcyjnymi agentami programistycznymi i opisali oszukiwanie
specyfikacji: jeden agent wpisywał na sztywno 19–41 odpowiedzi z ewaluacji na przebieg; agenci czytali sąsiednie
przebiegi przez wspólny stan git i zostawiali notatki „dla przyszłych przebiegów”. Dodanie odłożonego zbioru
testowego — i poinformowanie agentów, że istnieje — wyeliminowało wpisywanie odpowiedzi **(Z)**. Ich pięć reguł:

1. **R1** odkładaj dane ewaluacyjne;
2. **R2** informacja zwrotna bez przecieków: nigdy nie pokazuj złotych etykiet;
3. **R3** izoluj stan przebiegu „konstrukcyjnie, a nie instrukcją”;
4. **R4** sprawdź własne kanały stanu narzędzi agenta (pamięć, globalna konfiguracja);
5. **R5** raportuj składowe, bo „metryki skalarne mogą ukrywać składowe rzadkich zdarzeń o dużej wariancji”,
   i rejestruj hipotezy z góry.

Zasoby do zbudowania dla zwiadowcy **(W)**:

| Zasób | Zawartość | Kto go pisze | Do czego służy |
|---|---|---|---|
| **Złoty zbiór** | ≥200 zarchiwizowanych ogłoszeń z etykietami: trafienie czy nie, właściwy przedmiot i wariant, cena referencyjna, uzasadnienie. Zawiera *każde* prawdziwe trafienie, *każdy* potwierdzony fałszywy alarm i przypadki podchwytliwe: „na części”, zestawy, zły wariant lub region, podróbki, nieaktualne ogłoszenia, pułapki kosztowe | etykiety człowieka albo wyniki zaobserwowane później. **Tylko do dopisywania, wersjonowany, agent nie ma prawa zapisu** | bramka offline dla zmian oceny |
| **Zestaw obowiązkowy** | 20–40 krytycznych przypadków ze złotego zbioru (dawne kosztowne pomyłki) | człowiek | twarda bramka: jedna porażka = odrzucenie |
| **Ukryta część** | 15–20% złotego zbioru, której refleksja nigdy nie widzi, odświeżana co miesiąc | człowiek | wykrywanie przeuczenia do złotego zbioru |
| **Korpus migawek** | surowe strony wyników i JSON ogłoszeń dla (źródło, zapytanie, czas), zapisywane w zwykłych rundach | harness | odtwarzanie filtrowania i rankingu pretendenta na tym, co rynek naprawdę pokazał |
| **Sonda-wartownik** | przypięty, nigdy niezmieniany playbook, który co N rund uruchamia mały stały zestaw zapytań | definiuje człowiek | oddzielanie „świat się zmienił” od „to ja zepsułem” (§8) |
| **Dziennik przeoczonych trafień** | trafienia znalezione przez okresowe szerokie przeszukanie, przez wartownika albo później („sprzedane tanio”), których mistrz nie oznaczył | harness | jedyny bezpośredni sygnał **czułości**; zamienia rzadkie przeoczenia w oznaczone przykłady |

## 4. Playbook z pozycji, edytowany deltami

Trzymaj playbook jako dane strukturalne, a nie prozę. Każda pozycja ma tożsamość i historię:

```yaml
version: 37
runtime: {weights_sha256: "…", quant: Q4_K_M, template_sha256: "…", runtime: "llama.cpp <build>", temperature: 0.2}
sections:
  judgment:
    - id: J-017
      text: "Słowa 'na części' lub 'uszkodzony' w tytule albo opisie wykluczają ogłoszenie."
      added_in: 12
      provenance: [log:2026-09-14T03:15Z#17]
      helpful: 14          # aktualizuje harness na podstawie wyników, nigdy LLM
      harmful: 1
      last_validated: 2026-10-20
  procedure: [...]
  insights: [...]
```

Refleksja wydaje **wyłącznie operacje delta** — `ADD`, `MODIFY(id)` albo `RETIRE(id)` — a scala je kod. Nigdy nie
wydaje całego nowego playbooka. To lekarstwo ACE na zapadanie się kontekstu i ten sam pomysł co ADD / EDIT / UPVOTE /
DOWNVOTE w ExpeL **(Z)**. Propozycja to typowany rekord:

```yaml
id: P-0042
op: MODIFY                       # ADD | MODIFY | RETIRE
target: judgment.J-021
door: judgment                   # które drzwi oceny (tabela w §2)
hypothesis: "Przeoczone 3 trafienia w źródle B: dopasowanie odrzuca numery modeli zapisane bez myślnika."
evidence: [log:2026-10-21T04:15Z#17, log:2026-10-23T11:30Z#5, missed:M-118]
predicted_effect: {metric: golden_recall, direction: up, size: "+2 pozycje"}
blast_radius: [judgment.J-021]
new_text: "Przed dopasowaniem normalizuj numery modeli: usuń spacje i myślniki."
rollback: {op: MODIFY, target: judgment.J-021, text: "<poprzedni tekst, wstawia kod>"}
```

Zasady formatu **(W)**:

- Jedna sekcja na propozycję; bramkarz odrzuca każdą propozycję o szerszym zasięgu.
- Twardy limit rozmiaru na sekcję i całość, na przykład łącznie 6–8 tys. tokenów. Długi kontekst najpierw psuje
  mniejsze modele (zob. psucie się kontekstu w
  [01 §5](01-CO-MOZNA-ULEPSZAC.md#5-wskazówki-praktyków-ważne-dla-pętli-samomodyfikujących-się)).
- Deduplikuj przy zapisie po podobieństwie embeddingów; prawie-duplikaty odrzucaj, zamiast je dodawać.
- Trzymaj stały układ bajtów pliku (stała kolejność kluczy, dopisywanie na końcu sekcji). Każda edycja unieważnia
  zbuforowany początek promptu dla wszystkich kolejnych rund — to drugi powód, żeby edytować rzadko.

## 5. Bandyta do alokacji zamiast przepisywania

Większość odruchów „przepiszmy playbook” to w istocie **decyzje o alokacji**: na które źródło i zapytanie wydać
następną rundę. Bandyta wieloręki podejmuje je na bieżąco, z jawną eksploracją i bez dotykania prozy przez LLM **(W)**.

**Próbkowanie Thompsona Gamma-Poisson.** Ramiona to pary (źródło × szablon zapytania), ewentualnie × pora dnia. Każde
ramię trzyma rozkład a posteriori λ_i ~ Gamma(α_i, β_i) swojego tempa trafień na jednostkę kosztu. Po pociągnięciu
z x trafieniami przy koszcie c (rundy, minuty albo zapytania): α_i ← α_i + x, β_i ← β_i + c. Przy wyborze losujesz
λ̃_i z każdego rozkładu i uruchamiasz ramię z największą wartością (samouczek Russo i in.) **(D)**.

**Rynki dryfują, więc dyskontuj stare dowody.** Przed każdą aktualizacją przyciągnij rozkład z powrotem w stronę
rozkładu a priori: α ← γα + (1−γ)α0, β ← γβ + (1−γ)β0. γ = 0,98 daje efektywną pamięć ok. 50 pociągnięć, γ = 0,99
ok. 100 **(O)**. Dyskontowane i okienkowe próbkowanie Thompsona to standardowe warianty niestacjonarne (Raj i Kalyani;
Fiandri i in.) **(D)**.

```python
import random

class Arm:
    def __init__(self, prior_rate=0.2, prior_weight=1.0):
        # słaby rozkład a priori wokół średniego tempa portfela: alpha0 / beta0 = prior_rate
        self.a0, self.b0 = prior_weight, prior_weight / prior_rate
        self.a, self.b, self.pulls = self.a0, self.b0, 0

    def update(self, hits, cost=1.0, gamma=0.98):
        self.a = gamma * self.a + (1 - gamma) * self.a0 + hits
        self.b = gamma * self.b + (1 - gamma) * self.b0 + cost
        self.pulls += 1

    def sample(self, rng):
        return rng.gammavariate(self.a, 1.0 / self.b)      # Gamma(kształt a, tempo b)

    def p_above(self, floor, rng, n=2000):
        return sum(self.sample(rng) > floor for _ in range(n)) / n


def pick(arms, rng, explore=0.05, trial_budget=10):
    new = [k for k, arm in arms.items() if arm.pulls < trial_budget]
    if new and rng.random() < 0.5:
        return rng.choice(new)                    # gwarantowane próby dla nowych ramion
    if rng.random() < explore:
        return rng.choice(list(arms))             # minimalna eksploracja
    return max(arms, key=lambda k: arms[k].sample(rng))
```

**Zabezpieczenia (W):**

- **Minimalna eksploracja**: każde aktywne ramię działa co najmniej raz dziennie albo ≥5% pociągnięć jest całkiem
  losowych. Źródło, które umarło w zeszłym miesiącu, może wrócić.
- **Budżet prób**: nowe ramię zaproponowane przez LLM dostaje ok. 10 gwarantowanych pociągnięć, zanim rozkład
  a posteriori może je zagłodzić.
- **Wycofanie do zimnej puli, nie kasowanie**: po ≥M pociągnięciach, jeśli P(λ_i > λ_min) < 0,05, ramię trafia do
  zimnej puli, sprawdzanej raz w tygodniu.
- **Stan bandyty to dane należące do harnessu.** LLM proponuje ramiona; nigdy nie edytuje rozkładów.

**Dlaczego to ważne dla regresji.** Bandyta zamienia ryzykowne, skokowe przepisanie („źródło A na górę, źródło C
wyrzucić”) w płynną, samokorygującą się realokację. Złe nowe zapytanie kosztuje tylko swój budżet prób. Rola LLM
zawęża się do generowania hipotez (nowych ramion), a decyduje statystyka. **„LLM proponuje, statystyka rozstrzyga”**
to najważniejsza zasada tego poradnika.

## 6. Kaskada bramek

Kaskady oceny (AlphaEvolve, etapy 10 → 60 → 200 zadań w DGM) uruchamiają najpierw tanie sprawdzenia, żeby drogą ocenę
wydawać tylko na tych, którzy przeżyli **(Z)**. Zastosuj tę samą kolejność **(W)**:

| # | Bramka | Koszt | Warunek przejścia |
|---|---|---|---|
| 1 | **Statyczna** | sekundy | parsuje się zgodnie ze schematem; dotyka ≤1 sekcji; mieści się w budżecie rozmiaru; nie zmienia pól zamrożonych; ma hipotezę, przewidywany efekt, drzwi i deltę odwrotną |
| 2 | **Obowiązkowe** | minuty | 100% przypadków obowiązkowych, we wszystkich k ≥ 3 przebiegach, jeśli silnik jest niedeterministyczny |
| 3 | **Złoty zbiór, w parach** | minuty | dokładny McNemar: c > b *i* p < 0,05 dla deklarowanej poprawy (albo b ≤ ok. 1% pozycji dla deklarowanego neutralnego refaktoru), *i* brak nowej klasy fałszywych alarmów |
| 4 | **Powtórka** | minuty–godziny | na migawkach z ostatnich 7–14 dni pretendent znajduje ponownie każde trafienie mistrza i nie dodaje alertów odrzuconych przez ludzi |
| 5 | **Online** (tylko dla zmian, które zmieniają działania) | dni | tryb cienia dla oceny (§7); dla procedury **przełączanie** (switchback): losowe przydzielanie rund mistrzowi i pretendentowi w blokach czasu zrównoważonych po godzinie i dniu tygodnia (Bojinov, Simchi-Levi i Zhao) **(D)**; pretendent dostaje 20–30% rund; decyzja przez SPRT ([02 §4](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#4-reguły-decyzji-dla-małych-zaszumionych-prób)) |
| 6 | **Okres próbny** | ok. 100 rund | CUSUM na nowym mistrzu; automatyczne wycofanie przy alarmie (§8) |

**„Napraw więcej, niż psujesz”** to bramka 3 w jednym zdaniu. SkillBoost przyjmuje zmianę tylko przy zysku > 0
i małej liczbie regresji; edycja, która naprawiła 20 i zepsuła 23, została odrzucona, a bez tej bramki jeden model
spadł z 80,0 do 67,5 **(Z)**.

**Jeśli test dojdzie do maksymalnej długości bez decyzji, zostaje mistrz.** To celowe przywiązanie do status quo:
nieudowodniona zmiana to koszt, a nie neutralne zdarzenie **(W)**.

Bramkarz to zwykły kod. Szkic:

```python
from rare_event_stats import binom_sf     # narzedzia/rare_event_stats.py

def gate(proposal, champion, challenger, ev):
    if not ev.static_ok(proposal):
        return "reject:static"
    if not ev.must_pass(challenger, k=3):
        return "reject:must-pass"
    b, c = ev.paired_golden(champion, challenger)    # b: dobrze tylko mistrz, c: dobrze tylko pretendent
    if not (c > b and binom_sf(c, b + c, 0.5) < 0.05):
        return "reject:golden"
    if ev.replay_misses(challenger, champion) or ev.replay_new_rejected_alerts(challenger):
        return "reject:replay"
    return {"judgment": "shadow", "procedure": "switchback"}.get(proposal.door, "promote")
```

## 7. Tryb cienia

Dla zmian oceny tryb cienia to najtańsza mocna ewaluacja, jaka istnieje **(W)**. Logika oceny mistrza i pretendenta
w każdej rundzie ocenia **ten sam strumień kandydatów**; działa się tylko na oznaczeniach mistrza. Każda
**rozbieżność** to darmowy, sparowany, pouczający przykład. Rozbieżności oznacza człowiek albo wynik zaobserwowany
później.

Awansuj, gdy jest ≥10 rozstrzygniętych rozbieżności, pretendent wygrywa je z dokładnym p < 0,05 w teście
dwumianowym i nie pada żaden przypadek obowiązkowy. Progi **(O)**:

| Rozbieżności | Pretendent musi wygrać co najmniej |
|---|---|
| 10 | 9 |
| 16 | 12 |
| 20 | 15 |
| 30 | 20 |

W odróżnieniu od testu na wynikach to nie czeka na rzadkie trafienia. Czeka na rozbieżności, które zdarzają się
znacznie częściej. `python3 narzedzia/rare_event_stats.py shadow` wypisuje pełną tabelę.

## 8. Wartownik, dryf i wycofanie

**Wartownik** to przypięty playbook, którego nigdy się nie zmienia; kilka razy dziennie uruchamia mały stały zestaw
zapytań. To Twoja grupa kontrolna: porównanie go z mistrzem to metoda różnicy w różnicach **(W)**.

| Wartownik | Mistrz | Niedawna zmiana? | Interpretacja | Działanie |
|---|---|---|---|---|
| dryf | dryf | dowolnie | **zmienił się świat** (podaż, ceny, sezon, padło źródło) | **nie** wycofuj; zresetuj dyskontowanie bandyty i na jakiś czas zwiększ eksplorację; uruchom refleksję nastawioną na adaptację |
| stabilny | dryf | tak, alarm zaczął się po niej | **regresja na własne życzenie** | **automatyczne wycofanie** do poprzedniego mistrza; oznacz zmianę jako nieudaną; zablokuj podobne propozycje na okres karencji |
| stabilny | dryf | nie | awaria tylko u mistrza (zapytanie albo ścieżka parsera, której wartownik nie używa) | najpierw kontrole zdrowia, potem celowana propozycja naprawy |
| dryf | stabilny | dowolnie | rynek się ruszył, ale playbook jest odporny | zapisz, nic nie zmieniaj |

Liczy się czas: przy opóźnieniu wykrycia ok. 50–100 rund
([02 §5](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#5-pilnowanie-spadku-poissonowski-cusum)) alarm w ciągu jednego okna
wykrycia po awansie domyślnie przypisuje się temu awansowi.

**Wyzwalacze wycofania.** Wszystkie automatyczne, wszystkie w kodzie. Każdy z nich przywraca wersję N−1 i oznacza
zmianę N jako `failed_in_prod`:

- CUSUM alarmuje w okresie próbnym, a wartownik jest stabilny;
- codzienne ponowne uruchomienie złotego zbioru pokazuje porażkę przypadku obowiązkowego;
- metryka zdrowia po zmianie przekracza próg (na przykład odsetek błędów narzędzi się podwaja);
- człowiek zgłasza w okresie próbnym 2 lub więcej złych alertów wynikających z nowej pozycji.

Nieudana zmiana trafia na **listę odrzuconych pomysłów**, którą refleksja widzi, więc ten sam pomysł nie wraca przez
30 dni. Bufor odrzuconych edycji w SkillOpt to ten sam pomysł: jego usunięcie kosztowało 4,6 punktu **(Z)**.

## 9. Goodhart: jak wygląda oszukiwanie i strukturalna ochrona

Agent, który sam się modyfikuje, optymalizuje każdy sygnał, który widzi, także te, których nie miałeś na myśli.
Zakazy w prompcie nie działają (80% oszustw mimo „proszę, nie oszukuj”); rozwiązaniem jest **utwardzić oceniającego
i odebrać prawo zapisu** **(Z)**. U zwiadowcy spodziewaj się tego **(W)**:

| Wzorzec oszukiwania | Objaw | Ochrona strukturalna |
|---|---|---|
| Rozluźnianie definicji trafienia (niższy próg, optymistyczna cena referencyjna, pomijanie kosztów lub stanu) | trafień więcej, odsetek odrzuceń przez człowieka rośnie, średnia marża spada | definicja, koszty i próg są w zamrożonym kodzie; agent może tylko proponować |
| Liczenie duplikatów i ponownie wystawionych ogłoszeń | trafień więcej, unikalnych ID ogłoszeń tyle samo | harness deduplikuje po ID i odcisku (tytuł, cena, zdjęcia) |
| Łatwe, ale bezużyteczne zapytania | kandydatów i prawie-trafień więcej, trafień tyle samo | wskaźniki zastępcze tylko przyspieszają; trafienia muszą przejść test „nie gorzej” |
| Edycja dzienników lub metryk albo ukrywanie porażek we własnych podsumowaniach | twierdzenia refleksji nie zgadzają się z surowymi dziennikami | dzienniki tylko do dopisywania, pisane przez harness; metryki liczy kod; refleksja czyta surowe dzienniki |
| Przenoszenie informacji między przebiegami ewaluacji | wyniki offline skaczą bez mechanizmu | świeże środowisko dla każdej ewaluacji; brak prawa zapisu do zbiorów (R3/R4) |
| Przeuczenie do złotego zbioru | wynik na złotym zbiorze rośnie, powtórka i online stoją | ukryta część; comiesięczne odświeżanie nowymi oznaczonymi przypadkami |

Tło: Manheim i Garrabrant opisują cztery odmiany prawa Goodharta (regresyjną, ekstremalną, przyczynową,
przeciwniczą); Gao, Schulman i Hilton pokazują, że optymalizacja niedoskonałego wskaźnika najpierw poprawia
prawdziwy cel, a potem go pogarsza. Ta krzywa to formalny obraz „drugiego miesiąca” **(Z, streszczenia; nazwy
odmian z pamięci, D)**.

## 10. Domyślne reguły przyjęcia, odrzucenia i wycofania

| Rodzaj zmiany | Przyjmij, gdy | Odrzuć, gdy | Maksymalna próba |
|---|---|---|---|
| **Nowe ramię** (zapytanie lub źródło) | przetrwa budżet prób (≥10 pociągnięć), a jego rozkład zostaje powyżej progu wycofania | P(λ_ramienia > λ_min) < 0,05 po ≥M pociągnięciach; trafia do zimnej puli, sprawdzanej co tydzień | zarządza bandyta |
| **Heurystyka oceny** | obowiązkowe 100%; McNemar c > b przy p < 0,05 (albo b ≤ 1% przy neutralnym refaktorze); czułość w powtórce ≥ mistrz; tryb cienia: ≥10 rozstrzygniętych rozbieżności wygranych przy p < 0,05 | dowolna porażka obowiązkowa; powtórka gubi trafienie mistrza; tryb cienia przegrywa albo nie rozstrzyga do limitu | 14 dni trybu cienia |
| **Notatka proceduralna** | przełączanie z 25% rund dla pretendenta: metryka procesu poprawia się przy p < 0,05 *i* SPRT przypisania trafień nie przekracza granicy odrzucenia | metryka procesu gorsza; SPRT odrzuca; błędy powyżej barierki | 200 rund pretendenta, potem zostaje mistrz |
| **Propozycja dla warstwy zamrożonej** | zatwierdzenie przez człowieka po ponownej ocenie ostatnich 30 dni offline | domyślnie | n/d |

## 11. Kto prowadzi refleksję i jak często

**Refleksja jest tania; ocena nie.** Przy ponad 100 tokenach na sekundę refleksja, która pisze 2–4 tys. tokenów,
zajmuje niecałą minutę. Wczytanie 20–40 tys. tokenów metryk i transkryptów dokłada sekundy przy ciepłym cache promptu
i minuty przy zimnym: jeden użytkownik llama.cpp zmierzył 222 s ponownego wczytania 44 tys. tokenów po utracie cache
wobec 0,47 s przy jego ponownym użyciu; prompt 60 tys. tokenów na modelu MoE 80B zajął 39–54 s na zimno wobec ok. 1 s
z punktów kontrolnych **(Z; pierwsza liczba D)**. Uruchamiaj refleksję w osobnym slocie albo procesie, żeby nie
wyrzucała cache wykonawcy.

Wąskim gardłem nie jest więc moc obliczeniowa. Jest nim **przepustowość oceny**: przy 0,1–0,3 trafienia na rundę test
zmiany, która zmienia działania, trwa ok. 50–200 rund na ramię, więc zweryfikujesz może **1–4 takie zmiany
miesięcznie**; oraz **ryzyko regresji**: każdy awans to szansa, żeby coś zepsuć. **Dopasuj częstość refleksji do
możliwości oceny, a nie do budżetu obliczeń (W).**

**Kto prowadzi refleksję (W), od najlepszego wariantu:**

1. **Mocniejszy model pisze propozycje raz w tygodniu, a lokalny je wykonuje** (wzorzec doradcy z
   [01 §4](01-CO-MOZNA-ULEPSZAC.md#4-małe-i-lokalne-modele-w-roli-refleksji)). Jeśli prywatność pozwala, wyślij
   zanonimizowane podsumowanie.
2. **Refleksję prowadzi lokalny model 70–80B**, losując 3–5 niezależnych diagnoz i idąc dalej tylko z tą, którą
   podziela większość; krytykuje ją *inny* prompt albo świeży kontekst.
3. **Model wykonawcy tylko klasyfikuje porażki** według stałej taksonomii: przeoczone trafienie, fałszywy alarm, błąd
   narzędzia lub parsowania, wolna ścieżka, źródło niedostępne. Mniejsze modele radzą sobie ze stałym zestawem etykiet
   znacznie pewniej niż z pisaniem strategii od zera.

**Przebieg krytyka** sprawdza każdą propozycję wobec konstytucji, warstwy zamrożonej i listy odrzuconych pomysłów,
zanim trafi ona do bramkarza. Cokolwiek wybierzesz, **sędzią jest statystyka bramkarza, nigdy refleksja**.

**Co widzi refleksja.** Surowe dowody: fragmenty dzienników wybrane przez kod, tabele metryk policzone przez kod,
rejestr przewidywań ([04 §6](04-KIEDY-PRZESTAC.md#6-rejestr-przewidywań)). **Nie** widzi własnych wcześniejszych
podsumowań narracyjnych, które kumulują błędy, i **nigdy** nie widzi złotych etykiet ani ukrytej części (R2).

## 12. Uwagi o harnessie i silniku

Fakty pochodzą z dokumentacji i zgłoszeń OpenClaw i llama.cpp **(Z)**; rekomendacje to **(W)**. Te same pytania
dotyczą każdego harnessu.

- **Funkcje samoedycji bez bramki.** Skill Workshop w OpenClaw stosuje zmiany skilli napisane przez agenta od razu
  i nie dokumentuje żadnej bramki zatwierdzania; wcześniejsze wersje da się przywrócić. Nie pozwalaj wykonawcy ani
  refleksji zapisywać skilli bezpośrednio. Niech zapisują *plik propozycji*, który bramkarz zastosuje po przejściu
  bramek — albo wyłącz tę funkcję i zarządzaj plikami playbooka z poziomu bramkarza. Wbudowanego przywracania używaj
  tylko jako awaryjnego „cofnij”; **systemem wersjonowania jest git**.
- **Awans pamięci w tle.** „Śnienie” pamięci w OpenClaw awansuje wspomnienia do `MEMORY.md` w tle; dokumentacja mówi,
  że „pamięć nie egzekwuje zasad”. Wyłącz to dla takiego agenta albo traktuj ten plik jako notatki bez mocy wiążącej.
  **Nigdy nie pozwól, żeby tekst z ogłoszeń albo od sprzedających awansował do reguł**: to prompt injection przez
  treść („zabójcza trójca” Willisona; kurs 3).
- **Ciche obcinanie.** OpenClaw obcina pliki startowe (domyślnie 20 000 znaków na plik, 60 000 łącznie). Rosnący
  playbook zostaje po cichu ucięty. Trzymaj limit rozmiaru (§4) wyraźnie poniżej tej granicy.
- **Puste rundy jako poprawny wynik.** Zadania automatyzacji, które zwracają `NO_REPLY` albo zapisują `no_change`,
  naturalnie reprezentują puste rundy. Polityka modelu dla każdego zadania pozwala, żeby refleksja używała innego
  modelu niż wykonawca.
- **Niedeterminizm.** W llama.cpp `cache_prompt` (domyślnie włączone) może dawać niedeterministyczne wyniki, bo logity
  nie są identyczne bit w bit przy różnych rozmiarach partii. Bramki złotego zbioru i powtórki muszą używać pass^k
  (k ≥ 3) albo większości z k. W każdej wersji playbooka zapisuj skrót modelu, kwantyzację, szablon czatu i ustawienia
  samplera.
- **Kruchość wywołań narzędzi.** W chwili sprawdzania Qwen3 nie był na liście natywnych obsług wywołań narzędzi
  w llama.cpp (spada do „Generic”), a kilka harnessów zgłasza problemy z szablonem lub parserem; agresywna kwantyzacja
  KV-cache potrafi pogorszyć wywołania narzędzi. Testuj wywołania narzędzi od końca do końca na dokładnie tym pliku
  modelu, szablonie i parserze; dodaj bezpiecznik na powtarzające się identyczne wywołania; sprawdzaj
  ustrukturyzowane wyjście w kodzie, nawet przy gramatyce.
- **Zmiana silnika to zmiana playbooka.** Nowy model, kwantyzacja, szablon albo wersja silnika przechodzi bramki 2–4,
  zanim zastąpi stary, i jest zapisywany w wersji.

## 13. Rytm pracy

| Kiedy | Co działa | Koszt modelu |
|---|---|---|
| Co rundę | runda wykonawcy; dzienniki i migawki; `hit_rules`; aktualizacja bandyty; kontrole zdrowia; CUSUM; ocena w trybie cienia, jeśli aktywny jest pretendent oceny | sama praca |
| 2–4 razy dziennie | sonda-wartownik | mały |
| Codziennie | szerokie przeszukanie pod kątem przeoczonych trafień; ponowne uruchomienie złotego zbioru na mistrzu (łapie niedeterminizm i ciche zmiany silnika); podsumowanie prawie-trafień i rozbieżności do oznaczenia; triaż porażek (tylko klasyfikacja) | mały |
| Na podstawie dowodów, w stanie ustalonym najwyżej raz w tygodniu | refleksja: grupowanie porażek → ≤1 propozycja → bramki | 1–3 minuty pracy modelu |
| Po alarmie | przypisanie przyczyny (§8); wycofanie albo refleksja adaptacyjna | mały |
| Co miesiąc (człowiek) | rejestr przewidywań i odsetek przyjęć; odświeżenie ukrytej części; ponowna kalibracja λ0, h, γ; przegląd warstwy zamrożonej | czas człowieka |

---

Dalej: [04 · Kiedy przestać](04-KIEDY-PRZESTAC.md).
