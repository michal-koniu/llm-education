# 01 · Co może ulepszać samo siebie i jak to wyszło

Przegląd systemów samodoskonalących się z lat 2023–2026: co każdy z nich zmienia, jak rozstrzyga, że zmiana jest
lepsza, co go chroni przed pogorszeniem i gdzie zawiódł. Najwięcej uczą porażki. Oznaczenia: zob.
[README](README.md#jak-czytać-oznaczenia). Adresy: [ZRODLA](ZRODLA.md).

---

## 1. Samodoskonalenie na poziomie agenta: klasyka i podejścia ewolucyjne

Te systemy zmieniają samego agenta: jego kod, narzędzia, bibliotekę skilli albo refleksje.

| System | Rok | Co zmienia | Jak ocenia zmianę | Ochrona przed regresją | Charakterystyczna porażka lub ograniczenie |
|---|---|---|---|---|---|
| **Reflexion** | 2023 | Słowne refleksje, 1–3 na zadanie, używane tylko przy ponownej próbie tego samego zadania | Nagroda ze środowiska, heurystyki, testy jednostkowe pisane przez siebie | Tylko limit pamięci | Własne testy miały 16,3% fałszywych pozytywów na MBPP, więc wynik spadł poniżej bazowego GPT-4. **Na WebShop (wyszukiwanie w sklepie) nie dał nic i stanął po 4 próbach** **(Z)** |
| **Voyager** | 2023 | Bibliotekę wykonywalnych skilli w kodzie i automatyczny program nauki | Krytyk samoweryfikujący musi potwierdzić sukces, zanim skill trafi do biblioteki | Bramka weryfikacji; poddanie się po 4 rundach bez postępu | Bez samoweryfikacji −73% przedmiotów. GPT-3.5 i modele otwarte nie wystarczały (różnica 5,7×) **(Z)** |
| **ExpeL** | 2023 | Listę spostrzeżeń w języku naturalnym (ADD / EDIT / UPVOTE / DOWNVOTE) i pulę udanych przebiegów | Kontrastowe pary sukces–porażka | Każde spostrzeżenie ma wagę: start 2, głosy ±1, usunięcie przy 0 | Dokładanie własnych refleksji do ekstrakcji *zaszkodziło* (29% wobec 39%). Słabszy ekstraktor wypadł gorzej. Lista rośnie bez końca **(Z)** |
| **Agent Workflow Memory** | 2024 | Abstrakcyjne przepływy pracy dopisywane do pamięci | Offline: prawda bazowa. Online: sędzia LLM | Tylko filtr sukcesu | Uczył się z błędnych własnych etykiet. **Przepływy offline i online razem dały wynik gorszy niż same online**: zbiory się kłóciły **(Z)** |
| **ADAS / Meta Agent Search** | 2024 | Kod agenta (meta-agent jest stały) | Zbiory walidacyjne po 32–128 pytań; archiwum ocenionych projektów | Archiwum | Przeniesione do innych dziedzin wypadały *poniżej* punktów odniesienia. Malutkie zbiory walidacyjne **(Z)** |
| **Gödel Agent** | 2024 | Własny działający kod, **łącznie z modułem ulepszającym** | Użyteczność na walidacji | Nieformalne „można cofnąć” | Na 100 przebiegów: 4% padło po edycji modułu ulepszającego, 92% miało przejściowe spadki, **14% skończyło gorzej, niż zaczęło**. Jedna wersja „poprawiła się”, wołając silniejszy model z zewnątrz, czyli uciekając z protokołu oceny **(Z)** |
| **Darwin Gödel Machine (DGM)** | 2025 | Kod agenta programistycznego | Etapami: 10 zadań, potem 60, potem 200, z progami ustalonymi na podstawie zmierzonego szumu | Otwarte archiwum działających agentów | **Oszukiwanie celu:** usunął logowanie, na którym opierał się detektor halucynacji, i dostał wynik idealny; podrabiał też logi testów. Ok. 22 tys. USD za przebieg **(Z)** |
| **Huxley-Gödel Machine / DGM-H** | 2025–26 | Jak DGM (DGM-H edytuje też meta-agenta) | Ocena po zadaniach; wybór według produktywności całej linii potomków | Selekcja po liniach | Wynik agenta słabo przewiduje wyniki jego potomków (r ≈ 0,29–0,44) **(Z)** |
| **SICA** | 2025 | Własny kod, narzędzia, podagentów i nadzorcę | Użyteczność łącząca wynik, koszt i czas | Najlepszy z archiwum staje się kolejnym ulepszaczem; nadzorca LLM przerywa pętle | Wczesne pomysły dominują późniejsze. Brak zysku na benchmarkach rozumowania. Autorzy: „wymaga mocnych modeli” **(Z)** |
| **AlphaEvolve i otwarte odpowiedniki** (OpenEvolve, ShinkaEvolve, CodeEvolve) | 2025–26 | Oznaczone bloki kodu jako diffy, opcjonalnie meta-prompty | Funkcja `evaluate()` pisana przez użytkownika, w **kaskadzie** od tanich do drogich sprawdzeń | Populacje na wyspach, odrzucanie powtórzeń | Tao i współautorzy: system „zawsze w końcu znajdował sposób, żeby oszukać” dziurawe weryfikatory. **Najtańszy model w wielu przebiegach był najbardziej opłacalny**; CodeEvolve z Qwen3-Coder-30B pobił AlphaEvolve na jednym problemie przy ok. 10× niższym koszcie **(Z)** |
| **Promptbreeder** | 2023 | Prompty zadaniowe i prompty mutujące, które je zmieniają | Przystosowanie na partii 100 przykładów, turniej dwójkowy | Populacja i filtr podobieństwa | LLM „nie rozumiał” liczb przystosowania; zwycięskie prompty były nieczytelne **(Z)** |
| **STOP** | 2023 | Szkielet ulepszający, który ulepsza sam siebie | Użyteczność na zadaniach docelowych | Brak | **GPT-3.5 i Mixtral pogarszały ulepszacz z każdą iteracją.** Najmocniejszy model wyłączał flagę piaskownicy w 0,42% propozycji, a ostrzeżenie nie pomagało **(Z)** |
| **autoresearch** (Karpathy) | 2026 | Jeden plik, `train.py` | Stały budżet 5 minut, **zamrożony** plik oceny, jedna metryka | Twarda zapadka: zostaw tylko, jeśli lepiej, inaczej `git reset` | W replikacji agent programistyczny wpisywał na sztywno odpowiedzi z oceny, dopóki nie dodano zbioru odłożonego **(Z)** |

## 2. Optymalizatory promptów, kontekstu, skilli i pamięci

Te systemy nie ruszają kodu, tylko tekst: prompty, playbooki, skille, wspomnienia. To warstwa, której dotyka
większość praktycznych agentów, i to tu są dowody z 2026 roku.

| System | Rok | Co zmienia | Jak ocenia zmianę | Ochrona przed regresją | Charakterystyczna porażka lub ograniczenie |
|---|---|---|---|---|---|
| **DSPy MIPROv2** | 2024 | Instrukcje i przykłady few-shot dla każdego modułu | Bayesowskie przeszukiwanie na minipartiach, pełna ocena co kilka prób | Zwraca najlepszą *w pełni ocenioną* konfigurację | Wymaga metryki liczbowej i setek etykiet **(Z)** |
| **GEPA** | 2025 | Dowolny komponent tekstowy | Model refleksji czyta przebiegi; potomek musi pobić rodzica na **minipartii 3 przykładów**, potem jest oceniany na zbiorze Pareto | Pula Pareto dla każdego przykładu | „Puchnięcie promptu”: każda iteracja dopisuje reguły. **Spadł poniżej promptu startowego z refleksją na Llama-3.3-70B** w jednym zadaniu (59,4 wobec 62,5) **(Z)** |
| **TextGrad** | 2024 | Dowolną zmienną przez tekstowe „gradienty” | Walidacja w każdej iteracji | Aktualizacja tylko przy poprawie walidacji | Zakłada mocny model wsteczny; brak kontroli wariancji **(Z)** |
| **Trace / OptoPrime** | 2024 | Kod, prompty, parametry w śledzonym grafie | Ślad wykonania plus informacja zwrotna | **Brak**: przyjmuje każdą sparsowaną zmianę | Łamanie ograniczeń. Pokazanie śladu działa lepiej niż pokazanie samego wyniku **(Z)** |
| **ACE** (Agentic Context Engineering) | 2025 | „Ewoluujący playbook” z pozycji: punkty z identyfikatorami i licznikami pomocny/szkodliwy | Generator → refleksja → **kurator wypuszcza delty scalane przez kod** | Scalanie delt, liczniki, deduplikacja | Jego punkt odniesienia pokazuje **zapadnięcie się kontekstu**: jedno pełne przepisanie zmieniło playbook z 18 282 tokenów w 122, a trafność z 66,7 na 57,1, poniżej 63,7 bez żadnego playbooka. Refleksja na Llama-3.3-70B dała tylko +1,1 do +2,4 **(Z)** |
| **Dynamic Cheatsheet** | 2025 | Swobodną pamięć przepisywaną co krok | Tylko on sam | Brak | Zapadnięcie opisane wyżej. Małe modele: „ograniczone i niespójne”; „błędne heurystyki… wzmacniane tak samo” **(Z)** |
| **ReasoningBank** | 2025 | Wspomnienia strategii z sukcesów i porażek | Sędzia LLM o trafności 72,7% | Brak (tylko dopisywanie) | **Przywołanie 4 wspomnień dało gorszy wynik niż 1** (44,4% wobec 49,7%) **(Z)** |
| **Live-SWE-agent** | 2025 | Narzędzia tworzone w trakcie działania, refleksja po każdym kroku | Postęp zadania | Brak | GPT-5-Nano **spadł z 44% do 14%**, „utknął w pętlach”. Zyskują tylko mocne modele **(Z)** |
| **Hermes Agent** (Nous Research) | 2026 | Skille (preferowane łatanie) i plik pamięci | Samoocena agenta po sesjach | Twarde limity (plik pamięci 2200 znaków); zatwierdzanie zapisów; **Curator**: co tydzień w czasie bezczynności, oznacza pozycje jako nieświeże po 14 dniach, archiwizuje po 30, **nigdy nie kasuje**, **konsolidacja przez LLM domyślnie wyłączona**, migawki i wycofanie | Curator powstał, bo pętla produkowała „dziesiątki wąskich prawie-duplikatów” **(Z)** |
| **Anthropic skill-creator** | 2025–26 | Skille i opisy ich wyzwalania | Ślepe A/B wobec **migawki starej wersji**, 3 przebiegi na zapytanie, podział 60/40 trening/test, wybór według wyniku **testowego** | Stara wersja jako punkt odniesienia; wycofanie skilla, gdy model bazowy radzi sobie bez niego | Przestrzega przed „drobiazgowymi, przeuczonymi zmianami” **(Z)** |
| **Cookbook OpenAI o agentach samoewoluujących** | 2025 | Prompt systemowy | 4 gradery, progi zaliczenia, najwyżej 3 ponowienia | Wersjonowane prompty i powrót; zwycięzca według sumy wyników, nie świeżości | Przyznaje ryzyko przeuczenia do bieżących ocen; **jego własny przykładowy przebieg przyjmuje sekcje tuż poniżej deklarowanego progu** **(Z)** |
| **SkillOpt** (Microsoft) | 2026 | Dokument skilla przez dodaj / usuń / zamień w ramach **budżetu edycji**, „tekstowego współczynnika uczenia” | Zostaje tylko, jeśli poprawi się odłożony zbiór selekcyjny | Bufor odrzuconych edycji; powolne zmiany | Usunięcie bufora odrzuconych edycji obniżyło jeden wynik z 77,5 do 72,9 **(Z)** |
| **SkillBoost** | 2026 | Składniki skilli | Test wsteczny na pełnym zbiorze | **Przyjęcie tylko, gdy zysk > 0, a regresje poniżej małego ε**: „musi naprawić więcej przypadków, niż psuje” | Edycja, która naprawiła 20 i zepsuła 23, została odrzucona. **Bez tej bramki jeden model spadł z 80,0 do 67,5** **(Z)** |
| **Library Drift** | 2026 | Zarządzanie biblioteką skilli | Wkład każdego skilla | Wycofywanie na podstawie wyników, limit aktywnych skilli | Nieograniczony przyrost psuje wyszukiwanie; zbyt wczesne wycofywanie też szkodzi. Pass@1 0,258 → 0,584 przy zarządzaniu **(Z, streszczenie)** |
| **SkillsBench** | 2026 | (benchmark) | Deterministyczne weryfikatory | n/d | **Skille wygenerowane przez agenta wypadły poniżej braku skilli we wszystkich trzech harnessach (−8,1 do −11,5 punktu)**, a dopracowane przez ludzi dodały +18 do +25. Optimum to 2–3 skille; 4 i więcej zmniejsza zysk o połowę **(Z)** |
| **„Do Self-Evolving Agents Forget?”** | 2026 | Przepływy, skille, pamięć, wagi | Stare i nowe zadania | Zakotwiczone sygnatury zachowań; chronione pozycje | Erozja umiejętności we wszystkich czterech trybach: przepływy rozwijane na trudnych zadaniach traciły sprawność w łatwych **(Z)** |
| **SkillLearnBench** | 2026 | (benchmark) | | | Iteracja pomaga tylko z zewnętrzną informacją zwrotną. **„Samo sprzężenie od siebie wywołuje rekurencyjny dryf”** **(Z, streszczenie)** |
| **OpenClaw Skill Workshop i „śnienie” pamięci** | 2026 | Własne skille agenta; awans wspomnień w tle | Nieudokumentowana | Zapis poprzedniej wersji; polecenie przywracania | „Każda zmiana działa natychmiast”. **Brak udokumentowanej bramki zatwierdzania** **(Z)** |

Dalsze systemy z tej samej rodziny, z podobnymi lekcjami: Memento, Agent KB, SkillWeaver, EvoAgentX, PILOT,
HarnessBank, SelfOp ([ZRODLA](ZRODLA.md)).

## 3. Co wynika z przeglądu

**Sprawdzony sygnał wyniku to cała gra.** Reflexion i Agent Workflow Memory psują się, gdy sukces ocenia sam agent.
Największy pojedynczy zysk Voyagera to jego weryfikator. ExpeL wypada *gorzej*, gdy jego spostrzeżenia karmią własne
refleksje **(Z)**. Dla zwiadowcy: playbook zmieniaj tylko na podstawie wyników policzonych przez kod (potwierdzona
różnica ceny, faktyczna sprzedaż, etykieta człowieka), nigdy na podstawie opinii LLM o tym, jak poszła runda.

**Wszystko się sypie tam, gdzie system modyfikuje własny ulepszacz albo oceniającego.** Gödel Agent padał po edycji
ulepszacza; STOP wyłączał piaskownicę; DGM skasował znaczniki, których używał jego oceniający; AlphaEvolve znajdował
dziurawe weryfikatory **(Z)**. Zamroź oceniającego *konstrukcyjnie*: bez prawa zapisu, a nie przez „proszę, nie ruszaj”.

**Wspinaczka jedną linią prowadzi do regresji; archiwa i awans etapami pomagają.** 14% przebiegów Gödel Agent
skończyło gorzej, niż zaczęło. DGM bez archiwum doszedł do 23% zamiast 50% **(Z)**. W produkcji połącz zapadkę
(jeden mistrz, wymieniany tylko po dowodzie) z archiwum wszystkiego, czego próbowano.

**Słabe optymalizatory szkodzą, ale średnie modele dobrze proponują, gdy wybiera dokładny oceniający.** STOP z GPT-3.5
i Mixtralem pogarszał się z każdą iteracją; Live-SWE-agent z GPT-5-Nano się rozpadł **(Z)**. Z drugiej strony
CodeEvolve użył Qwen3-Coder-30B, a Tao i współautorzy uznali najtańszy model w wielu przebiegach za najbardziej
opłacalny — *bo wybierał dokładny oceniający* **(Z)**. Niech lokalny model proponuje małe, typowane delty; niech kod
i statystyka wybierają.

**Eksplorację trzeba wbudować, bo refleksja jej nie tworzy.** Reflexion zawiódł na WebShop, benchmarku najbliższym
przeszukiwaniu ogłoszeń, właśnie przez brak „różnorodności i eksploracji” **(Z)**. Systemy ewolucyjne kupują
eksplorację populacjami i filtrami nowości. Bandyta z gwarantowaną minimalną eksploracją to tani odpowiednik
([03 §5](03-BEZPIECZNA-PETLA.md#5-bandyta-do-alokacji-zamiast-przepisywania)).

**Przyrost bez zarządzania gnije.** Bez zarządzania skille i wspomnienia pisane przez agenta często wypadają *gorzej
niż brak pamięci*: SkillsBench, Dynamic Cheatsheet, Library Drift, erozja umiejętności **(Z)**. Harnessy produkcyjne
doszły do czterech odpowiedzi:

- twarde limity rozmiaru (Hermes: plik pamięci 2200 znaków);
- oznaczanie nieświeżych pozycji na podstawie użycia i archiwizacja, nigdy kasowanie (Hermes Curator);
- bramki „napraw więcej, niż psujesz” (SkillBoost);
- przywoływanie tylko 1–3 pozycji na zadanie (ReasoningBank, SkillsBench).

**Przepisywanie całego tekstu to główny mechanizm regresji; delty są lekarstwem.** Zapadnięcie ACE z 18 282 do 122
tokenów, STOP gubiący ograniczenia startowe „dla uproszczenia”, puchnięcie GEPA **(Z)**.

## 4. Małe i lokalne modele w roli refleksji

Pytanie dla każdego, kto uruchamia model lokalnie: czy on sam potrafi się poprawiać?

| Ustalenie | Dowody |
|---|---|
| Samopoprawianie *wewnętrzne*, bez zewnętrznego sygnału, obniża trafność | Huang i in. (ICLR 2024): Llama-2 na GSM8K spadła z 62,0 do 36,5 **(Z)**. Kamoi i in.: samopoprawianie działa tylko z wiarygodną zewnętrzną informacją zwrotną albo po dostrojeniu do zadania **(Z, streszczenie)** |
| Słabe optymalizatory pogarszają albo stoją w miejscu | STOP z GPT-3.5: tylko 12% przebiegów poprawiło się o ≥3%. ACE z refleksją na Llama-3.3-70B: małe zyski, a GEPA i Dynamic Cheatsheet spadły poniżej bazy. Live-SWE-agent na GPT-5-Nano się rozpadł **(Z)** |
| Średnie modele sprawdzają się jako *proponujący* przy dokładnym oceniającym | Zamiana refleksji na Qwen2.5-32B utrzymała w ESPO każdą metodę powyżej domyślnego promptu (ESPO 67,8, GEPA 63,5 wobec 31,1), choć niżej niż z modelem z czołówki. CodeEvolve z Qwen3-Coder-30B **(Z)** |
| Dostawcy zbiegają się na „mocny doradca, tani wykonawca” | „Strategia doradcy” Anthropic: mały wykonawca radzi się dużego modelu tylko przy trudnych decyzjach; Haiku z doradcą Opus uzyskał 41,2% wobec 19,7% samego Haiku na BrowseComp **(Z)** |
| Samoocena tym samym modelem jest zawyżona | Agenci „niezawodnie zawyżają ocenę własnej pracy”; dostrojenie osobnego, sceptycznego oceniającego jest „znacznie łatwiejsze” (Anthropic, projektowanie harnessów, 2026) **(Z)** |

**Wniosek (W):** otwarty model 30–80B jest blisko progu, poniżej którego zyski z refleksji maleją albo się odwracają.
Używaj go do *klasyfikowania* porażek i *proponowania* małych, typowanych delt, które przechodzą przez bramki oparte
na wynikach mierzonych kodem. Nie każ mu oceniać własnych propozycji ani przepisywać całego playbooka.

## 5. Wskazówki praktyków ważne dla pętli samomodyfikujących się

**Praktyka ewaluacji** (Anthropic „Demystifying evals for AI agents”, Husain i Shankar, Eugene Yan) **(Z)**:

- „20–50 prostych zadań wziętych z prawdziwych porażek to świetny początek.”
- Testuj, kiedy zachowanie powinno wystąpić, *i* kiedy nie powinno. Dla zwiadowcy „tu nie ma nic do oznaczenia”
  to pełnoprawny przypadek zaliczony.
- Wybieraj deterministyczne gradery, jeden binarny grader na jeden rodzaj porażki. Każdego sędziego LLM sprawdź na
  ≥50 zaliczeniach i ≥50 porażkach, zanim mu zaufasz.
- Oddziel **ewaluacje umiejętności** (niski odsetek zaliczeń, „góra do zdobycia”) od **ewaluacji regresji** (blisko
  100%). Nasycone zadania umiejętności przechodzą do regresji.
- Używaj **pass^k** (wszystkie k prób udane), gdy liczy się powtarzalność: 75% na próbę daje pass^3 ≈ 42%.
- Izoluj próby. Jeden agent zyskał nieuczciwą przewagę, czytając historię git zostawioną przez wcześniejsze próby.
- „Czytaj transkrypty!” Przeglądaj 10–20 przebiegów tygodniowo.

**Projektowanie harnessu** (wpisy Anthropic z listopada 2025 i marca 2026) **(Z)**: wykonawcy mogli zmieniać tylko pole
`passes` w liście funkcji w JSON, bo modele rzadziej nadpisują JSON niż Markdown; „Usuwanie lub edytowanie testów jest
niedopuszczalne”; elementy harnessu kodują założenia o słabościach modelu, więc trzeba je testować od nowa przy każdej
zmianie modelu.

**Oszukiwanie nagrody** **(Z)**:

- METR (czerwiec 2025): model z czołówki nadpisał licznik czasu, załatał ewaluator i czytał odpowiedzi ze stosu
  wywołań — oszukiwał w 30,4% przebiegów jednego benchmarku. **„Proszę, nie oszukuj” wciąż zostawiało 80% oszustw.**
  Ich rada: „załatać lukę w funkcji oceniającej, zamiast karać model”.
- Oszukiwanie nagrody w kontekście (Weng 2024, streszczając Pan i in.): pętle sprzężenia zwrotnego *w czasie
  inferencji*, bez zmiany wag, i tak prowadzą do narastającego łamania ograniczeń — im więcej rund, tym gorzej.
  Kluczowy czynnik to wspólny kontekst oceniającego i generującego. To dokładnie sytuacja agenta, który edytuje
  własne prompty.
- Anthropic (listopad 2025): wyuczone oszukiwanie testów uogólniło się na sabotowanie kodu wykrywającego. Jawne
  dopuszczenie skrótu zatrzymało to uogólnienie. Odpowiednik w czasie inferencji **(W)**: „zero trafień w tej
  rundzie” ma być jawnie dozwolonym, niekaranym wynikiem.

**Psucie się kontekstu** **(Z)**: badanie Chroma „Context Rot” — wszystkie 18 testowanych modeli pogarsza się wraz
ze wzrostem wejścia, a rozpraszacze to pogłębiają. Breunig wyróżnia cztery tryby awarii: zatrucie, rozproszenie,
pomieszanie, konflikt. Średnie modele zaczynają gubić reguły powyżej ok. 100 instrukcji. Manus: trzymaj stały
początek promptu dla trafień w cache, zostawiaj porażki w kontekście, „nie wpędzaj się few-shotami w koleinę”.

**Długo działające agenty w praktyce** **(Z)**:

- Project Vend (Anthropic 2025): agent sklepu sprzedawał poniżej kosztów i przywracał rabaty kilka dni po tym, jak
  zgodził się z nich zrezygnować. Wymuszone sprawdzenia pomogły („biurokracja ma znaczenie”), a „kierownik” na tym
  samym modelu miał te same martwe pola.
- Vending-Bench: „wszystkie modele mają przebiegi, które się wykolejają”, bez wyraźnego związku z zapełnieniem kontekstu.
- Samozatrucie pamięci (wpis z 2026): automatycznie zapisane błędne wnioski były potem przywoływane obok korekty,
  a agent „wybierał coś pośrodku”. Naprawa: ranking źródeł (sprawdzone dane wygrywają z wnioskami agenta) i zapisywanie
  sprostowań w tej samej warstwie pamięci.

Nie istnieje **rzetelna publiczna analiza poawaryjna** agenta, który tygodniami przepisywał własny playbook,
a potem się zdegradował. Dowody na „rozpad w drugim miesiącu” pochodzą z powyższych analogii i benchmarków z 2026
roku. Traktuj to jako dobrze uzasadnione oczekiwanie, a nie zmierzoną krzywą **(W)**.

---

Dalej: [02 · Pomiar przy rzadkich zdarzeniach](02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md).
