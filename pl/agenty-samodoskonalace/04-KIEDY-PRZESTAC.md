# 04 · Kiedy przestać

Agent samodoskonalący się potrzebuje sposobu, żeby stwierdzić, że działa dobrze i powinien zostawić siebie w spokoju.
Nie może to być osąd samego LLM: samoocena tym samym modelem jest „niezawodnie zawyżona” **(Z)**, a po kilku pechowych
rundach przechyla się w drugą stronę. **„Działa dobrze” musi być stanem, który kod wylicza z dowodów.** Ta strona
definiuje ten stan i sterownik wokół niego. Wszystko tutaj to propozycja projektowa **(W)**, chyba że oznaczono inaczej.

---

## Co mówią dowody o zatrzymywaniu się

- autoresearch zostawia zmianę tylko wtedy, gdy jest ściśle lepsza, a w przeciwnym razie cofa: to zapadka **(Z)**.
- U Askarbekuly i in. (2026) reguła plateau w protokole wynosiła ok. 15 eksperymentów bez poprawy. Agent nazwany przez
  autorów **generalizatorem** zatrzymał się sam po 12–13, odmówił dopisywania wyjątków dla pojedynczych wierszy
  i oznaczył pozostałe porażki jako „strukturalnie nie do wygrania”. **Maksymalizator metryki** szedł dalej i zamieniał
  porażki w przypadki szczególne **(Z)**.
- skill-creator Anthropic wycofuje skill, gdy model bazowy radzi sobie bez niego **(Z)**; Curator w Hermes Agent
  archiwizuje nieużywane pozycje i ma konsolidację przez LLM **domyślnie wyłączoną** **(Z)**.
- Gao, Schulman i Hilton: optymalizacja niedoskonałego wskaźnika najpierw pomaga prawdziwemu celowi, potem mu
  szkodzi **(Z, streszczenie)**.

**Lekcja (W): późne zyski to nieproporcjonalnie często przeuczenie.** Im dłużej pętla działa po dojściu do plateau,
tym większa część jej „ulepszeń” to zapamiętany szum.

## Kiedy agent „wie”, że działa dobrze?

Gdy spełnione są wszystkie poniższe warunki, a każdy z nich liczy kod:

| Sygnał | Jak liczony | Dlaczego oznacza „zostaw w spokoju” |
|---|---|---|
| Mistrz jest **w swoim paśmie** | przedział rozkładu a posteriori jego tempa trafień nakłada się na tempo z ostatnich 30 dni | nic mierzalnego się nie zmieniło |
| **Żaden alarm** nie jest aktywny | CUSUM, Page–Hinkley i kontrole zdrowia milczą | brak dowodów na problem do naprawienia |
| **Wartownik jest stabilny** | jego własne metryki w paśmie | świat się nie przesunął |
| **Ostatni pretendenci zostali odrzuceni** | ≥3 odrzucenia z rzędu | lokalne przeszukiwanie wokół mistrza jest wyczerpane |
| **Pozostałe pomysły są za małe, żeby je zmierzyć** | przewidywany efekt każdego pomysłu w kolejce < minimalny wykrywalny efekt w 2 tygodnie (§5) | test byłby rzutem monetą z dołączonym ryzykiem regresji |

Gdy to zachodzi, sterownik jest w **trybie utrzymania**, a refleksja w ogóle się nie uruchamia. „W tej rundzie nic nie
znalazłem” nie jest na tej liście i nigdy nie powinno być.

## 1. Wyzwalacze oparte na dowodach

Propozycja jest dozwolona tylko wtedy, gdy zachodzi co najmniej jedno z poniższych:

- odpalił alarm CUSUM albo kontroli zdrowia ([02 §5](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#5-pilnowanie-spadku-poissonowski-cusum));
- w dzienniku jest skupisko **≥3 porażek o tej samej przyczynie** (przeoczone trafienia, fałszywe alarmy, błędy
  narzędzi), sklasyfikowanych przez codzienny triaż;
- pojawiła się **nowa okazja** (nowe źródło, nowa kategoria przedmiotów);
- przypada **zaplanowany przegląd** (co tydzień w fazie ulepszania z bramkami, co miesiąc w utrzymaniu);
- poprosił **człowiek**.

**Same puste rundy nigdy nie są wyzwalaczem.** „Zero trafień w tej rundzie” ma być jawnie dozwolonym, niekaranym
wynikiem — zarówno w kodzie, jak i w prompcie wykonawcy. Anthropic stwierdził, że jawne dopuszczenie skrótu zatrzymało
uogólnianie się wyuczonego oszukiwania **(Z)**; odpowiednik w czasie inferencji to przestać traktować ciszę jak porażkę.

## 2. Jedna zmiana naraz

Nigdy nie nakładaj pretendentów na siebie. Gdy pretendent jest w teście, refleksja może pomysły tylko **odkładać
do kolejki**. Dwie edycje wprowadzone, zanim którąkolwiek oceniono, uniemożliwiają przypisanie efektu, a wycofanie
staje się zgadywaniem. Jeden edytowalny plik w autoresearch i budżet edycji w SkillOpt wymuszają tę samą dyscyplinę **(Z)**.

## 3. Okres próbny i karencja

Po awansie nowy mistrz jest na **okresie próbnym** co najmniej tak długim, jak czas wykrycia spadku o połowę przez
CUSUM: **ok. 50–100 rund przy λ ≈ 0,3** ([02 §5](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#5-pilnowanie-spadku-poissonowski-cusum))
**(O)**. W okresie próbnym nie ma propozycji. Alarm w tym czasie, przy stabilnym wartowniku, automatycznie wycofuje
zmianę ([03 §8](03-BEZPIECZNA-PETLA.md#8-wartownik-dryf-i-wycofanie)).

## 4. Wykładniczo rosnące przerwy po odrzuceniach

Po każdym odrzuconym pretendencie **podwój minimalny odstęp** między refleksjami: 1 → 2 → 4 → 8 dni, najwyżej 14.
Wróć do odstępu bazowego po przyjętej zmianie albo po alarmie dryfu. Seria odrzuceń to sygnał od systemu, że łatwe
ulepszenia się skończyły.

## 5. Tryb utrzymania

Wejdź w tryb utrzymania, gdy zachodzi jedno z dwóch:

- **≥3 kolejnych pretendentów zostało odrzuconych**; albo
- **największy wiarygodny efekt** pomysłów w kolejce jest **mniejszy niż minimalny efekt wykrywalny w 2 tygodnie**.

Przykład liczbowy do drugiej reguły **(O)**: przy rundzie co 15 minut 2 tygodnie to 1344 rundy, czyli 672 na ramię.
Z tabeli w [02 §2](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#2-ile-trafień-trzeba-żeby-pokazać-że-zmiana-pomogła) przy
λ = 0,1 zmiana o +50% wymaga 632 rund na ramię (ledwo wykrywalna), a o +25% — 2232 (niewykrywalna). Przy λ = 0,3 +50%
wymaga 211, a +25% — 744 (prawie, ale nie). Jeśli więc refleksja nie umie uzasadnić zysku rzędu +50% lub więcej, test
online nie ma sensu; pomysł idzie ścieżką tylko offline albo do zaległości. Sprawdź własne liczby:
`python3 narzedzia/rare_event_stats.py power --rates <Twoje λ>`.

**W trybie utrzymania:**

- **playbook jest zamrożony**;
- **bandyta dalej dostosowuje** alokację w bezpiecznych granicach, więc agent wciąż nadąża za rynkiem;
- monitory, wartownik i codzienne uruchomienie złotego zbioru działają dalej;
- playbook otwiera tylko alarm, awaria zdrowia, prośba człowieka albo comiesięczny przegląd — i to tylko dla **jednej
  celowanej zmiany przechodzącej przez bramki** (stan ADAPT poniżej).

To stan docelowy. Działający system powinien spędzać w nim większość życia.

## 6. Rejestr przewidywań

Każda propozycja zapisuje swój przewidywany efekt (metryka, kierunek, wielkość). Rejestr śledzi:

- **skuteczność** refleksji: odsetek propozycji, które przeszły wszystkie bramki;
- **kalibrację**: przewidywany wobec zmierzonego efektu dla tych, które przeszły.

Jeśli przez miesiąc przechodzi mniej niż ok. 20% propozycji, ogranicz częstość refleksji jeszcze bardziej albo przenieś
refleksję na mocniejszy model ([03 §11](03-BEZPIECZNA-PETLA.md#11-kto-prowadzi-refleksję-i-jak-często)). Rejestr jest
też tym, co refleksja czyta zamiast własnych dawnych narracji.

## 7. Cykl życia

```
BOOTSTRAP ──(≥20 trafień lub 2 tygodnie, złoty zbiór ≥200)──► ULEPSZANIE Z BRAMKAMI
    ▲                                                            │  ≥3 odrzucenia z rzędu albo
    │                                                            │  wiarygodny zysk < MDE z 2 tygodni
    │                                                            ▼
 duża zmiana świata ◄──(dryf wartownika i mistrza)──────── UTRZYMANIE (playbook zamrożony;
 (nowy serwis,                                                bandyta i monitory działają;
  podmiana modelu)                                            comiesięczny przegląd człowieka)
                                                                 │ alarm, awaria, prośba człowieka
                                                                 ▼
                                                          ADAPT (jedna celowana zmiana z bramkami)
                                                                 └──► z powrotem do UTRZYMANIA
```

| Stan | Co wolno | Cel |
|---|---|---|
| **Bootstrap** | większe edycje, oceniane głównie offline i przez przegląd oznaczeń przez człowieka; bez A/B online (nie ma jeszcze punktu odniesienia) | zbudować złoty zbiór, korpus migawek, wartownika i oszacowanie λ0 |
| **Ulepszanie z bramkami** | wszystko z [03](03-BEZPIECZNA-PETLA.md): jedna zmiana naraz, bramki, okres próbny, rosnące przerwy | wspinać się, póki wspinaczka jest mierzalna |
| **Utrzymanie** | bandyta, monitory, wartownik; bez edycji playbooka | pozostać dobrym; tu mieszka działający agent |
| **Adapt** | jedna zmiana, zawężona do dowodów, które ją wywołały, przez pełne bramki | zareagować na prawdziwy problem i wrócić do utrzymania |

Podmiana modelu lub silnika albo nowy serwis cofa system do bootstrapu dla tej części: to nowy punkt odniesienia.

## 8. Sterownik w kodzie

Szkic logiki zatrzymywania. Wyzwalacze to zbiór napisów liczony przez monitor; puste rundy nigdy go nie tworzą.

```python
from dataclasses import dataclass
from datetime import datetime, timedelta

BASE, CAP = timedelta(days=1), timedelta(days=14)
REOPEN = {"cusum_alarm", "health_alarm", "human_request", "monthly_review"}


@dataclass
class Controller:
    state: str = "BOOTSTRAP"            # BOOTSTRAP | GATED | MAINTENANCE | ADAPT
    in_flight: str | None = None        # id jedynego pretendenta w teście
    probation_until: int = 0            # numer rundy
    backoff: timedelta = BASE
    next_reflection: datetime = datetime.min
    rejections_in_row: int = 0

    def may_reflect(self, now: datetime, rnd: int, triggers: set[str]) -> bool:
        if self.in_flight or rnd < self.probation_until:
            return False                                  # jedna zmiana naraz; karencja
        if self.state == "MAINTENANCE":
            if triggers & REOPEN:
                self.state = "ADAPT"
                return True
            return False
        return now >= self.next_reflection and bool(triggers)

    def on_decision(self, now: datetime, rnd: int, accepted: bool, probation_rounds: int = 100):
        self.in_flight = None
        if accepted:
            self.rejections_in_row, self.backoff = 0, BASE
            self.probation_until = rnd + probation_rounds
        else:
            self.rejections_in_row += 1
            self.backoff = min(self.backoff * 2, CAP)
        self.next_reflection = now + self.backoff
        if self.state == "ADAPT" or (self.state == "GATED" and self.rejections_in_row >= 3):
            self.state = "MAINTENANCE"

    def on_alarm(self):
        self.backoff = BASE                               # alarm zeruje wydłużanie przerw
```

Przejście z BOOTSTRAP do GATED, i powrót do BOOTSTRAP po podmianie modelu, to decyzja człowieka: wymaga istnienia
zasobów do oceny, czego kod nie oceni. Reguła „wiarygodny zysk < MDE z 2 tygodni” należy do bramkarza: odrzuca
propozycję przed jakimkolwiek testem, gdy przewidywany efekt jest mniejszy, niż test potrafiłby wykryć, i takie
odrzucenie wlicza się do trzech.

## 9. Lista kontrolna

- [ ] Żadna ścieżka w kodzie nie zamienia „N pustych rund” w refleksję.
- [ ] O tym, czy refleksja się odbędzie, decyduje sterownik, nie LLM.
- [ ] W każdej chwili istnieje najwyżej jeden pretendent.
- [ ] Długość okresu próbnego wynika ze zmierzonego czasu wykrycia przez CUSUM, a nie ze zgadywania.
- [ ] Przerwa podwaja się po odrzuceniu i wraca do bazowej po przyjęciu albo alarmie.
- [ ] Tryb utrzymania istnieje, jest domyślnym celem i zamraża playbook, podczas gdy bandyta pracuje dalej.
- [ ] Każda propozycja ma przewidywany efekt w rejestrze, a comiesięczny przegląd go czyta.

---

Dalej: [05 · Pułapki](05-PULAPKI.md).
