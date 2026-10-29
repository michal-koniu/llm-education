# Agenty samodoskonalące się — bez regresji

**Stan na 29 października 2026.** Jak zbudować agenta, który przez tygodnie pracy poprawia własne instrukcje, pamięć
albo skille, a przy tym nie psuje po cichu wersji, która już działała — i jak sprawić, żeby sam rozpoznał, że jest
wystarczająco dobry i powinien przestać się zmieniać. Ten katalog to **poradnik**: przegląd tego, co istnieje,
statystyka, której nie da się ominąć, architektura do zbudowania i pułapki w kolejności, w jakiej na nie trafisz.

> ⚠️ **Czym ten poradnik jest, a czym nie.** To research biurkowy: ponad 100 artykułów, dokumentacji i wpisów
> inżynierskich przeczytanych 29 października 2026, plus statystyka policzona małym skryptem
> ([narzedzia/](narzedzia/README.md)). Architektura z [03](03-BEZPIECZNA-PETLA.md) to **propozycja projektowa**
> oparta na tych źródłach, a **nie** zmierzony wynik. Każde ważne twierdzenie ma oznaczenie (niżej), żeby dało się
> odróżnić liczbę z artykułu od mojego wniosku.

---

## Problem w jednym akapicie

Pętla samodoskonalenia ma trzy części: agent pracuje, coś analizuje, jak mu poszło, a ta refleksja zmienia to, co
agent zrobi następnym razem (prompt, playbook, plik skilla, pamięć, własny kod). Artykuły pokazują, że to działa.
Pokazują też ciągle tę samą porażkę: pętla **uczy się z szumu albo z własnej opinii o sobie**, poprawia przez
**przepisywanie całych dokumentów** i gubi to, co wiedziała, **sięga do tego, czym jest mierzona**, i to oszukuje,
a do tego **nigdy się nie zatrzymuje**. Gdy wynik, na którym Ci zależy, jest rzadki, wszystkie cztery problemy się
nasilają, bo kilka rund prawie nic nie mówi o tym, czy zmiana pomogła. Większość poradnika dotyczy właśnie tego.

## Przykład przewodni: zwiadowca z rzadkimi trafieniami

Żeby nie mówić ogólnikami, przez cały poradnik towarzyszy nam jeden agent — celowo generyczny.

**Zwiadowca** pracuje w *rundach*, powiedzmy co 15 minut, przez całą dobę. W każdej rundzie przeszukuje kilka
publicznych serwisów ogłoszeniowych, wyciąga ogłoszenia, porównuje każde z ceną referencyjną i oznacza te, które są
wyraźnie poniżej niej. Oznaczenie, które okaże się trafne, to **trafienie**. Trafienia są rzadkie: poradnik
zakłada, dla ilustracji, **od 0,1 do 0,3 trafienia na rundę**. Zwiadowca ma **playbook** (zbiór reguł i notatek:
które źródła i zapytania uruchamiać, jak dopasowywać przedmioty, sygnały ostrzegawcze, notatki proceduralne),
a krok **refleksji** ten playbook edytuje.

Ten sam kształt ma wielu agentów. Jeśli Twój ma rzadki, cenny wynik i tanią, częstą rundę — wszystko tutaj Cię dotyczy:

| Agent | Runda | Rzadkie trafienie | Gęstszy sygnał, którego można użyć zamiast |
|---|---|---|---|
| Zwiadowca ogłoszeń | jedno przeszukanie | potwierdzone ogłoszenie poniżej ceny | prawie-trafienia, kandydaci po wstępnym sicie, ocena na oznaczonym archiwum |
| Strażnik biuletynów bezpieczeństwa | jeden przegląd kanałów | biuletyn, który naprawdę dotyczy Twojego kodu | poprawnie odrzucone biuletyny na oznaczonym zbiorze |
| Zwiadowca literatury | jedna partia zapytań | artykuł, którego naprawdę potrzebowałeś | oceny trafności na stałym zbiorze dawnych wyników |
| Agent szukający błędów | jedno przejście po module | potwierdzony prawdziwy błąd | błędy podrzucone celowo, odsetek odtworzeń znanych błędów |
| Triaż zgłoszeń | jedna partia zgłoszeń | trafna eskalacja rzadkiego pilnego przypadku | zgodność z człowiekiem na zamrożonym zbiorze dawnych zgłoszeń |

## Najważniejsze zasady

To jest cały poradnik w skrócie. Każda zasada prowadzi do miejsca, gdzie jest uzasadniona.

| # | Zasada | Dlaczego | Gdzie |
|---|---|---|---|
| 1 | **Nigdy nie traktuj „nic nie znalazłem” jako dowodu samego w sobie.** | Przy 0,1–0,3 trafienia na rundę trzy puste rundy zdarzają się w 41–74% przypadków bez żadnej zmiany **(O)**. „Refleksja po 2–3 pustych rundach” reaguje na szum. | [02 §1](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#1-jak-bardzo-zaszumione-jest-nic-nie-znalazłem) |
| 2 | **Pogódź się z arytmetyką rzadkich zdarzeń.** | Wykazanie, że zmiana *podwaja* tempo trafień, wymaga ok. 58 trafień łącznie, czyli 65–194 rund na ramię przy 0,1–0,3 trafienia na rundę. +25% jest praktycznie niemierzalne na samych trafieniach **(O)**. | [02 §2](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#2-ile-trafień-trzeba-żeby-pokazać-że-zmiana-pomogła) |
| 3 | **LLM proponuje, kod i statystyka rozstrzygają.** | Alokację (które źródło, które zapytanie) przejmuje bandyta wieloręki. LLM dokłada hipotezy. Przyjęcie, odrzucenie i wycofanie to deterministyczny kod **(W)**. | [03 §5](03-BEZPIECZNA-PETLA.md#5-bandyta-do-alokacji-zamiast-przepisywania) |
| 4 | **Zamroź warstwę pomiaru konstrukcyjnie, a nie instrukcją.** | Systemy, które mogły sięgnąć do swojego oceniającego, oszukiwały: kasowały znaczniki, wyłączały piaskownicę, wpisywały odpowiedzi na sztywno, łatały gradery. „Proszę, nie oszukuj” wciąż dawało 80% oszustw **(Z)**. | [03 §2](03-BEZPIECZNA-PETLA.md#2-co-może-się-zmieniać-i-przez-które-drzwi) |
| 5 | **Edytuj deltami, nigdy przepisaniem.** | Jedno pełne przepisanie skurczyło playbook z 18 282 tokenów do 122, poniżej wyniku bez playbooka **(Z)**. | [03 §4](03-BEZPIECZNA-PETLA.md#4-playbook-z-pozycji-edytowany-deltami) |
| 6 | **Jedna zmiana naraz**, z typem, hipotezą, dowodami, przewidywanym efektem i deltą odwrotną. | Nałożone zmiany uniemożliwiają przypisanie efektu i wycofanie **(W)**. | [04 §2](04-KIEDY-PRZESTAC.md#2-jedna-zmiana-naraz) |
| 7 | **Najpierw najtańsze bramki, i „napraw więcej, niż psujesz”.** | Schemat → zestaw obowiązkowy → sparowany złoty zbiór → powtórka → tryb cienia albo przełączanie → okres próbny. Usunięcie bramki „regresje < naprawy” kosztowało do 12,5 punktu **(Z)**. | [03 §6](03-BEZPIECZNA-PETLA.md#6-kaskada-bramek) |
| 8 | **Ucz się tylko ze sprawdzonych wyników.** | Sukces oceniany przez samego siebie zatruwa pamięć; samo sprzężenie od siebie „wywołuje rekurencyjny dryf”; samopoprawianie bez zewnętrznego sygnału obniża trafność **(Z)**. | [01 §3](01-CO-MOZNA-ULEPSZAC.md#3-co-wynika-z-przeglądu) |
| 9 | **Zmiany oceny testuj w trybie cienia.** | Mistrz i pretendent oceniają ten sam strumień; działa tylko mistrz. Rozbieżności są częste, sparowane i tanie w oznaczaniu **(W)**. | [03 §7](03-BEZPIECZNA-PETLA.md#7-tryb-cienia) |
| 10 | **Odróżniaj „świat się zmienił” od „moja zmiana coś zepsuła”.** | Wartownik, którego nigdy się nie zmienia, CUSUM na tempie trafień i zwykłe kontrole zdrowia. Wykrycie spadku o połowę przy 0,3 trafienia na rundę zajmuje ok. 50–100 rund **(O)**. | [03 §8](03-BEZPIECZNA-PETLA.md#8-wartownik-dryf-i-wycofanie) |
| 11 | **Używaj porządnej statystyki małych prób.** | Testy dokładne, testy sekwencyjne, które pozwalają zaglądać, reguła trzech, żadnych przedziałów z CTG poniżej kilkuset punktów, poprawka na klątwę zwycięzcy, pass^k przy niedeterministycznych powtórkach **(Z/D/O)**. | [02 §4](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#4-reguły-decyzji-dla-małych-zaszumionych-prób) |
| 12 | **System, który działa, powinien przestać się zmieniać.** | Okres próbny, wykładniczo rosnące przerwy, tryb utrzymania. Późne „zyski” to nieproporcjonalnie często przeuczenie **(Z/W)**. | [04](04-KIEDY-PRZESTAC.md) |
| 13 | **Dopasuj częstość refleksji do możliwości oceny, nie do mocy obliczeniowej.** | Refleksja jest tania; zweryfikowane zmiany są rzadkie (kilka w miesiącu). Średnie modele są blisko progu, poniżej którego zyski z refleksji znikają **(Z/W)**. | [03 §11](03-BEZPIECZNA-PETLA.md#11-kto-prowadzi-refleksję-i-jak-często) |
| 14 | **Zarządzaj przyrostem.** | Skille napisane przez agenta wypadły *gorzej niż brak skilli* (−8 do −11,5 punktu); 4 przywołane wspomnienia dały gorszy wynik niż 1 **(Z)**. Limity, archiwizacja, żadnej automatycznej konsolidacji. | [01 §3](01-CO-MOZNA-ULEPSZAC.md#3-co-wynika-z-przeglądu) |
| 15 | **Zmianę środowiska uruchomieniowego traktuj jak pretendenta.** | Nowy model, kwantyzacja, szablon czatu czy wersja silnika to największa zmiana playbooka, jaką kiedykolwiek zrobisz **(W)**. | [03 §12](03-BEZPIECZNA-PETLA.md#12-uwagi-o-harnessie-i-silniku) |

## Co budujesz

Na końcu masz te elementy. Żaden nie wymaga frameworka; każdy to mały plik albo kilkadziesiąt linii kodu.

| Element | Co to jest | Plik |
|---|---|---|
| Zamrożony moduł pomiaru | definicja trafienia, progi, metryki, deduplikacja; agent nie może do niego pisać | [03 §2](03-BEZPIECZNA-PETLA.md#2-co-może-się-zmieniać-i-przez-które-drzwi) |
| Zasoby do oceny | złoty zbiór, zestaw obowiązkowy, ukryta część, korpus migawek, dziennik przeoczonych trafień | [03 §3](03-BEZPIECZNA-PETLA.md#3-zamrożone-zasoby-do-oceny) |
| Playbook z pozycji + schemat propozycji | pozycje YAML z identyfikatorami i licznikami; jedna typowana delta na propozycję | [03 §4](03-BEZPIECZNA-PETLA.md#4-playbook-z-pozycji-edytowany-deltami) |
| Bramkarz | czysty kod: kaskada bramek, McNemar, SPRT, awans / odrzucenie / wycofanie, wersje w git | [03 §6](03-BEZPIECZNA-PETLA.md#6-kaskada-bramek) |
| Bandyta | dyskontowane próbkowanie Thompsona Gamma-Poisson po ramionach (źródło × zapytanie) | [03 §5](03-BEZPIECZNA-PETLA.md#5-bandyta-do-alokacji-zamiast-przepisywania) |
| Monitor | kontrole zdrowia, poissonowski CUSUM, sonda-wartownik, tabela przypisania przyczyn | [03 §8](03-BEZPIECZNA-PETLA.md#8-wartownik-dryf-i-wycofanie) |
| Logika zatrzymania | wyzwalacze oparte na dowodach, karencja, wydłużanie przerw, tryb utrzymania, rejestr przewidywań | [04](04-KIEDY-PRZESTAC.md) |
| Kalkulator | statystyka stojąca za każdą liczbą (O), dla Twoich własnych wartości | [narzedzia/](narzedzia/README.md) |

## Co jest w tym katalogu

| Plik | Co w nim jest |
|---|---|
| [01-CO-MOZNA-ULEPSZAC](01-CO-MOZNA-ULEPSZAC.md) | **Przegląd.** Ponad 30 systemów samodoskonalących się: co zmieniają, jak oceniają zmianę, co je chroni, jak zawiodły |
| [02-POMIAR-PRZY-RZADKICH-ZDARZENIACH](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md) | **Lekcja.** Dlaczego rzadkie wyniki psują naiwną ocenę, arytmetyka, testy dokładne, SPRT, CUSUM, klątwa zwycięzcy |
| [03-BEZPIECZNA-PETLA](03-BEZPIECZNA-PETLA.md) | **Budowa.** Komponenty, co może się zmieniać i przez które drzwi, zamrożony oceniający, delty, bramki, tryb cienia, bandyta, wartownik, wycofanie, rytm pracy |
| [04-KIEDY-PRZESTAC](04-KIEDY-PRZESTAC.md) | **Budowa.** Wyzwalacze, jedna zmiana naraz, okres próbny, wydłużanie przerw, tryb utrzymania, maszyna stanów cyklu życia |
| [05-PULAPKI](05-PULAPKI.md) | 25 porażek w kolejności, w jakiej je spotkasz, każda z objawem i naprawą |
| [ZRODLA](ZRODLA.md) | wszystkie źródła z adresami i tym, jak dokładnie je sprawdzono |
| [narzedzia/](narzedzia/README.md) | `rare_event_stats.py`: kalkulator w samej bibliotece standardowej, do Twoich własnych wartości |

Proponowana kolejność: ta strona, potem [02](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md) (zmienia sposób czytania całej
reszty), potem [03](03-BEZPIECZNA-PETLA.md) i [04](04-KIEDY-PRZESTAC.md). Do [01](01-CO-MOZNA-ULEPSZAC.md) sięgaj,
gdy chcesz zobaczyć dowody stojące za konkretną zasadą.

## Jak czytać oznaczenia

| Oznaczenie | Znaczenie |
|---|---|
| **(Z)** | Zweryfikowane: przeczytane w źródle pierwotnym (artykuł, repozytorium, oficjalna dokumentacja lub wpis) 29 października 2026 |
| **(D)** | Z drugiej ręki: z wyniku wyszukiwania, streszczenia albo standardowego podręcznika, bez sprawdzenia oryginału |
| **(O)** | Obliczone na potrzeby poradnika skryptem [`narzedzia/rare_event_stats.py`](narzedzia/README.md): dokładne testy dwumianowe i symulacja |
| **(W)** | Wniosek: moje rozumowanie albo rekomendacja projektowa, oparta na źródłach, ale niezmierzona |

Zasada oznaczona (W) to przemyślane ustawienie domyślne, a nie prawo. Jeśli Twój pomiar mówi co innego, wygrywa Twój pomiar.

## Powiązane części repozytorium

- Kurs 2, [część 14: ewaluacja](../kurs_aplikacje_agentowe/00-INDEKS.md) i część 18 (wydania i utrzymanie): harness
  ewaluacyjny i dyscyplina wydań, które ten poradnik zakłada.
- Kurs 3, [pośredni prompt injection i zatruwanie pamięci](../kurs_bezpieczenstwo_llm/00-INDEKS.md): dlaczego tekstu
  z ogłoszeń nigdy nie wolno awansować do reguł ([05, pułapka 22](05-PULAPKI.md)).
- [Przegląd harnessów agentowych](../harnessy-agentowe/README.md): Hermes Agent, OpenClaw i inne, których funkcje
  pamięci i skilli omawiam w [01](01-CO-MOZNA-ULEPSZAC.md) i [03 §12](03-BEZPIECZNA-PETLA.md#12-uwagi-o-harnessie-i-silniku).
