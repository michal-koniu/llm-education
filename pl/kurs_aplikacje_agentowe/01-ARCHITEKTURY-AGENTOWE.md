# Część 1 · Architektury agentowe — mapa terenu

**Poziom:** ⭐⭐ · **Czas:** ~5 h · **Wymaga:** kursu 1, część 6 (pętla agenta)
**Produkuje:** diagnozę Twojej pętli z kursu 1, decyzję architektoniczną na piśmie, katalog `$OSA/`

---

## 0. Co się zmienia między kursem 1 a kursem 2

W kursie 1 zbudowałeś **pętlę**. Czyta plik, pisze plik, uruchamia polecenie, pamięta
kilkanaście tur, działa w `bwrap`. To jest prawdziwy agent i nie jest zabawką.

Ale spróbuj zrobić z niej to, co zapowiedziałeś: **kilku agentów, którzy działają
tygodniami, budzą się sami i współpracują**. Pęknie w pięciu miejscach, i to nie
dlatego, że jest źle napisana:

| Co pęka | Dlaczego | Część, która to naprawia |
| :-- | :-- | :-- |
| Kontekst kończy się po ~40 minutach pracy | Pętla nie ma kompakcji ani pamięci zewnętrznej | 3, 4, 5 |
| Po restarcie nie wie, co robiła | Historia żyje w pamięci procesu | 2, 3 |
| Nie da się jej zapytać „dlaczego to zrobiłeś" | Nie ma śladów, tylko wynik | 15 |
| Dołożenie 20. narzędzia psuje wybór pierwszych 19 | Deskryptory narzędzi zjadają kontekst i mieszają model | 7, 8 |
| Dwa agenty naraz to dwa niezależne światy | Nie ma bramy, sesji ani wspólnego stanu | 2, 12, 13 |

**Kurs 2 nie uczy lepszej pętli. Uczy systemu, w którym pętla jest jednym z ośmiu
elementów** — i to nie najtrudniejszym.

> ⭐ **Jedno zdanie, które streszcza cały kurs.**
> Pętla to 10 % pracy. Sesje, pamięć, harmonogram, piaskownica, obserwowalność
> i ewaluacja to pozostałe 90 % — i to one decydują, czy agent jest narzędziem,
> czy ciekawostką.

---

## 1. Zanim zbudujesz agenta — cztery pytania, które oszczędzają miesiąc

Anthropic w [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents)
podaje cztery kryteria. Przepisuję je, bo **trzy z czterech odpowiedzi u Ciebie brzmią
inaczej niż w firmie z chmurą**.

**1 · Złożoność.** Czy zadanie jest wielokrokowe i trudne do pełnego opisania z góry?

- „Wyciągnij tytuł z tego PDF-a" → **to nie jest zadanie dla agenta.** To jedno wywołanie
  z gramatyką. Agent doda 30× koszt i wprowadzi niepewność tam, gdzie jej nie było.
- „Przejrzyj moje dokumenty z ostatniego kwartału i powiedz, o czym zapomniałem" →
  **to jest zadanie dla agenta.** Nie wiesz z góry, ile plików trzeba przeczytać ani czego
  szukać.

**2 · Wartość.** Czy wynik uzasadnia koszt i opóźnienie?

U Ciebie „koszt" znaczy co innego niż u innych. **Nie płacisz za token.** Płacisz
**czasem karty i prądem** — i to jest realny, ale zupełnie inaczej ukształtowany budżet.
Agent, który mieli 40 minut w nocy, kosztuje Cię grosze. Ten sam agent w chmurze
kosztowałby kilkanaście dolarów. **To przesuwa granicę opłacalności bardzo mocno w Twoją
stronę** i jest głównym powodem, dla którego warto budować lokalnie.

**3 · Wykonalność.** Czy model to w ogóle potrafi?

Tu masz twardsze ograniczenie niż ktoś na modelu frontier. `gpt-oss-20b` wywoła
narzędzie poprawnie w ponad 90 % prostych przypadków, ale **end-to-end na zadaniu
wielokrokowym publikowane liczby spadają do 80–90 %**
([LLM Configurator](https://llmconfigurator.com/en/guides/coding-agents/tool-calling-local-models)),
bo błędy wyboru narzędzia i błędy argumentów **mnożą się przez liczbę kroków**.

Policz to sobie na serwetce. Przy 92 % skuteczności na krok:

```
 3 kroki  →  0.92³  =  78 %
 8 kroków →  0.92⁸  =  51 %
15 kroków →  0.92¹⁵ =  29 %
```

⭐ **To jest najważniejsza arytmetyka w całym kursie.** Nie poprawisz tego lepszym
promptem. Poprawiasz to **skracaniem łańcucha** (część 8, code-mode), **weryfikacją po
drodze** (część 14) i **odzyskiwaniem po błędzie** (część 3). Wszystkie trzy to praca
nad systemem, nie nad modelem.

**4 · Koszt błędu.** Czy da się błąd wykryć i cofnąć?

To pytanie rozstrzyga, **co agentowi wolno**, i wraca w częściach 10, 12 i 16. Zapamiętaj
regułę: *jeśli nie umiesz wykryć, że agent się pomylił, nie dawaj mu tego narzędzia.*

---

## 2. Widmo: od workflow do agenta

Rynek nazywa „agentem" wszystko. Rozróżnienie, które ma znaczenie inżynierskie, jest
jedno: **kto decyduje o następnym kroku — Twój kod czy model?**

```
  TWÓJ KOD DECYDUJE                              MODEL DECYDUJE
  ├───────────────┼──────────────┼──────────────┼───────────────┤
  1 wywołanie     łańcuch        router         pętla           flota
                  (chain)        (routing)      (agent)         (multi-agent)

  przewidywalne   przewidywalne  półprzewid.    nieprzewid.     nieprzewid.²
  1 wywołanie     N wywołań      1-2 wywołania  ? wywołań       ?? wywołań
  koszt znany     koszt znany    koszt znany    koszt nieznany  koszt nieznany
  łatwe testy     łatwe testy    łatwe testy    trudne testy    bardzo trudne
```

**Reguła, której trzymam się przez cały kurs:** *schodź w prawo tylko wtedy, gdy lewa
strona udowodniła, że nie wystarcza.* Każdy krok w prawo kupuje elastyczność za
przewidywalność — a przewidywalność jest tym, co pozwala spać.

> 💡 **Praktycznie.** W systemie, który zbudujesz, **większość pracy wykona workflow, nie
> agent.** Gospodarz sprawdzający kalendarz to workflow. Gospodarz, który zauważył
> konflikt i szuka, jak go rozwiązać, to agent. **Ta sama „aplikacja agentowa" zawiera
> obie warstwy** i to jest zdrowe — nie niedoróbka.

---

## 3. Cztery sposoby zbudowania agenta

Warto znać wszystkie cztery, bo **mylą się nawzajem nawet ludziom, którzy je budują**.
Rozdziela je jedno pytanie: **kto dostarcza harness, a kto dostarcza wdrożenie?**

| # | Sposób | Ty piszesz | Harness | Wdrożenie | Kiedy |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | **Ręczna pętla** | wszystko | Twój | Twoje | Gdy chcesz rozumieć. **To jest kurs 1 i baza kursu 2** |
| 2 | **Tool runner z SDK** | tylko narzędzia | SDK | Twoje | Gdy chcesz szybko, ale z kontrolą nad hakami |
| 3 | **Agent zarządzany** | konfigurację | dostawcy | dostawcy | Gdy stan i sesje mają być cudzym problemem |
| 4 | **Gotowy harness kodujący** (Claude Agent SDK, OpenHands) | prompt | biblioteki | Twoje | Gdy chcesz agenta do kodu, nie budować agenta |

**Dla Ciebie odpadają 3 i 4**, i to nie z powodów ideologicznych:

- **3 odpada** z definicji — zarządzany agent oznacza cudzy proces, cudzy stan i cudzą
  dostępność. Cała teza Twojego projektu jest przeciwna.
- **4 odpada jako cel**, ale **nie jako punkt odniesienia**. Claude Agent SDK jest
  świetnie zaprojektowany i w częściach 3, 7 i 13 porównuję z nim Twoje rozwiązania.

Zostaje **1 z elementami 2**: piszesz pętlę sam, ale nie odrzucasz bibliotek tam, gdzie
niczego nie ukrywają. Dokładnie to ustaliliśmy jako zasadę kursu.

---

## 4. Topologie — jak agenci układają się względem siebie

Cztery układy. Każdy ma miejsce, w którym umiera.

### 4.1 · Hub-and-spoke (gwiazda) — jedna brama, wiele kanałów i narzędzi

```
        kanały                  BRAMA                narzędzia
    CLI  ─────┐            ┌──────────────┐        ┌──── pliki
    HTTP ─────┼───────────►│   sesje      │◄───────┼──── shell
    Signal ───┤            │   routing    │        ├──── sieć
    cron ─────┘            │   polityki   │        └──── pamięć
                           └──────┬───────┘
                                  │
                           ┌──────▼───────┐
                           │  RUNTIME     │  ← pętla agenta
                           └──────────────┘
```

**Tak jest zbudowany OpenClaw** i tak zbudujesz swój system. Zalety: jedno miejsce na
politykę bezpieczeństwa, jedno na stan sesji, jedno do obserwowania. Wada: brama jest
pojedynczym punktem awarii — dlatego w części 18 uczysz się ją restartować bez utraty stanu.

### 4.2 · Graf ze stanem typowanym

Węzły to funkcje lub agenci, krawędzie to przejścia, stan jest jawny i typowany. Tak
działa LangGraph. Świetne, gdy przepływ jest **znany z góry i musi być audytowalny**.
Słabe, gdy nie znasz kształtu zadania — a w agencie osobistym zwykle nie znasz.

### 4.3 · Hierarchia (nadzorca i wykonawcy)

Nadzorca rozbija zadanie, wykonawcy realizują w **czystym kontekście** i zwracają
streszczenie na 1–2 tys. tokenów. To jest wzorzec subagenta z
[Anthropica](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
Działa świetnie przy równoległym przeszukiwaniu. **Kosztuje stałą opłatę za delegację**
(pułapka P41 z kursu 1) i dlatego przegrywa na zadaniach krótkich.

### 4.4 · Rój / tablica ogłoszeń

Agenci piszą i czytają ze wspólnej tablicy, bez centralnego nadzorcy. Elegancki
i **prawie zawsze zły wybór na start**: nieprzewidywalny, trudny do debugowania i
maksymalnie podatny na awarię kaskadową.

> ⚠️ **Liczba, która powinna Cię onieśmielić.** Wedle OWASP jeden skompromitowany serwer
> **w 72,4 % przypadków pociągał za sobą działanie kolejnych**
> ([Teleport](https://goteleport.com/blog/owasp-top-10-agentic-applications/)).
> Topologia, w której wszyscy gadają ze wszystkimi, to topologia, w której jedna
> pomyłka staje się wszystkimi pomyłkami. Wracamy do tego w częściach 13 i 16.

---

## 5. OpenClaw rozłożony na części

Prosiłeś, żebym to sprawdził — i słusznie, bo to najlepiej udokumentowany działający
system tej klasy. Nie kopiujemy go. **Rozbieramy, żeby zobaczyć, jakie decyzje trzeba
podjąć**, i część z nich podejmiemy inaczej.

### 5.1 · Cztery bloki

| Blok | Co robi | Gdzie o tym w kursie |
| :-- | :-- | :-- |
| **Gateway** (brama) | Jedyne źródło prawdy o sesjach, routingu i kanałach. Nasłuchuje na `127.0.0.1:18789`, **tylko na pętli zwrotnej** | część 2, 12 |
| **Brain** (runtime) | Składa prompt systemowy z plików roboczych, woła model z przełączaniem awaryjnym, przechwytuje wywołania narzędzi | część 3, 6 |
| **Hands** (narzędzia) | Wykonuje — na hoście albo w piaskownicy, zależnie od poziomu zaufania sesji | część 7, 10 |
| **Memory** | SQLite z wyszukiwaniem hybrydowym: wektory + BM25 | część 5 |

### 5.2 · Sześć faz obsługi wiadomości

To jest szkielet, który zaimplementujesz w części 2. Warto znać czasy, bo pokazują,
**gdzie naprawdę schodzi czas** (liczby z opisu OpenClaw, do zweryfikowania u siebie):

```
1. Przyjęcie              adapter kanału odbiera wiadomość
2. Kontrola dostępu       lista dozwolonych, parowanie, typ sesji     < 10 ms
3. Złożenie kontekstu     pliki robocze + historia + pamięć           < 100 ms
4. Wywołanie modelu       strumieniowo do dostawcy               200–500 ms do 1. tokena
5. Wykonanie narzędzi     shell, pliki, przeglądarka            100 ms – 3 s
6. Dostarczenie           formatowanie, dzielenie, zapis stanu
```

⭐ **Zwróć uwagę na proporcje.** Bezpieczeństwo kosztuje **poniżej 10 ms**. Składanie
kontekstu **poniżej 100 ms**. Cała reszta to model i narzędzia. To znaczy, że **nie masz
żadnej wymówki, żeby oszczędzać na kontroli dostępu** — jest darmowa w porównaniu do
tego, co i tak robisz.

### 5.3 · Rozwiązywanie sesji — pomysł, który kradnę w całości

OpenClaw mapuje wiadomość na sesję o **jawnie nazwanym poziomie zaufania**:

```
wiadomość z konsoli            →  main                          (host, pełne uprawnienia)
prywatna z kanału              →  agent:main:<kanał>:dm:<id>     (piaskownica)
z grupy                        →  agent:main:<kanał>:group:<id>  (piaskownica, węziej)
```

**To jest najlepsza pojedyncza decyzja w tej architekturze.** Poziom zaufania nie jest
flagą doklejaną do narzędzia — jest **właściwością sesji, wynikającą z tego, skąd
przyszła wiadomość**. Nie da się o nim zapomnieć, bo bez sesji nie ma wywołania.
Implementujesz to w części 2, egzekwujesz w części 10.

### 5.4 · Pliki robocze jako program

```
AGENTS.md     instrukcje rdzenia        ← co agent ma robić
SOUL.md       osobowość i ton           ← jak ma to robić, rośnie w czasie
MEMORY.md     co wie o Tobie            ← audytowalne, otwierasz i czytasz
HEARTBEAT.md  lista spraw do pilnowania ← cron wyrażony po polsku
SKILL.md      pojedyncza zdolność       ← doładowywana, gdy potrzebna
```

⭐ **Dlaczego to jest genialne, a nie prymitywne.** Zachowanie agenta jest **plikiem
tekstowym, który otwierasz, czytasz, wersjonujesz w git i cofasz**. Alternatywa —
dostrajanie modelu — daje to samo zachowanie w formie, której **nie da się przeczytać,
pokazać komuś ani cofnąć**. Przy agencie dotykającym Twoich spraw to nie jest wybór
estetyczny.

### 5.5 · Czego OpenClaw uczy przez kontrprzykład

Nie idealizuję go. Trzy udokumentowane problemy, z których każdy jest materiałem do
części 16:

| Problem | Czego uczy |
| :-- | :-- |
| Secret Store **nieszyfrowany spoczynkowo** w 2.0 | Sekrety to osobna warstwa, nie pole w konfiguracji (część 10) |
| Piaskownica **niewłączona domyślnie** | Domyślna wartość jest polityką bezpieczeństwa. U Ciebie domyślnie **włączona** (część 10) |
| Cisco: umiejętności zewnętrzne z **realną eksfiltracją** | Łańcuch dostaw umiejętności to ASI04. Zamknięty, podpisany zestaw (część 16) |
| Incydent MoltMatch — agent działał poza intencją | Proaktywność wymaga granic, nie tylko zdolności (część 11) |

---

## 6. Loop engineering — kontrapunkt, który musisz znać

Peter Steinberger, autor OpenClaw, napisał w czerwcu 2026:

> „Here's your monthly reminder that you shouldn't be prompting coding agents anymore.
> You should be designing loops that prompt your agents."

**To jest najważniejsze zdanie o agentach, jakie znalazłem w całym researchu**, i warto
je rozpakować, bo brzmi jak slogan, a nie jest.

**Promptowanie** = optymalizujesz jedno wejście do modelu. Poprawiasz sformułowanie,
dokładasz przykłady, prosisz „take your time".
**Loop engineering** = optymalizujesz **maszynę, która generuje wejścia**. Co agent
dostaje na starcie każdej tury. Kiedy się zatrzymuje. Co widzi po błędzie. Jak
przekazuje pracę następnej sesji. Kto sprawdza wynik.

Różnica jest taka jak między pisaniem jednego dobrego zapytania SQL a zaprojektowaniem
schematu bazy. **Pierwsze skaluje się liniowo z Twoim czasem. Drugie skaluje się samo.**

### 6.1 · Reszta tez Steinbergera — i gdzie się z nim nie zgadzam

| Jego teza | Uzasadnienie | Mój komentarz dla Ciebie |
| :-- | :-- | :-- |
| **MCP i RAG to trucizna kontekstu** | GitHub MCP ≈ 23 tys. tokenów. CLI kosztuje **zero**, bo model już go zna i przeczyta `--help` | ⭐ Mocna teza, testowalna — **mierzymy ją w części 9**. U Ciebie kontekst jest droższy niż u niego (mniejsze modele), więc argument jest jeszcze silniejszy |
| **Prompty 1–2 zdania + obrazek** | Dobry model sam przeczyta kod | ⚠️ **To zależy od modelu.** On używa frontier. `gpt-oss-20b` potrzebuje więcej prowadzenia. Nie kopiuj tego bez pomiaru |
| **Bez trybu planowania** | Dobre modele nie potrzebują teatru | ⚠️ Dla Twoich modeli **jawny plan realnie pomaga** — wróci w części 3 jako lista funkcji |
| **Bez subagentów** | „Obchodzenie zepsutego systemu" | ⚠️ Nie zgadzam się przy małych modelach: czysty kontekst subagenta to **jedyny sposób na odzyskanie budżetu uwagi**. Rozstrzygasz pomiarem w części 13 |
| **Promień rażenia** jako jednostka planowania | Ile plików ruszy ta zmiana | ⭐ **Bezdyskusyjnie dobre.** Wchodzi do części 7 i 16 jako kryterium projektowe narzędzia |
| **3–8 agentów równolegle, atomowe commity** | Bez gałęzi, szybciej | ⭐ Dobre i u Ciebie wykonalne — część 13 |

> 🎯 **Jak z tego korzystać.** Steinberger ma rację **w swoim kontekście**: doświadczony
> inżynier, model frontier, zadania programistyczne, pełne zaufanie do maszyny.
> **Trzy z tych czterech warunków u Ciebie nie zachodzą.** Dlatego przez cały kurs
> stawiam jego tezy obok pomiaru i każę Ci rozstrzygać samemu. **Umiejętność
> rozstrzygnięcia jest cenniejsza niż wybór strony.**

---

## 7. Odkrycie, które zmienia priorytety

Z badań nad benchmarkami agentowymi
([Prefactor](https://prefactor.tech/learn/agent-benchmarks)):

> **Wynik agenta zmienia się bardziej wraz z harnessem niż z modelem.** Ten sam model pod
> dwoma różnymi szkieletami daje istotnie różne liczby. Harness decyduje, jak
> udostępnione są narzędzia, jak pokazywane są błędy i ile prób dostaje agent.

Przeczytaj to jeszcze raz, bo ma konsekwencję finansową. **Zmienną, nad którą masz
pełną kontrolę — harness — jest ważniejsza niż zmienna, nad którą masz zerową kontrolę —
wagi modelu.** Czas spędzony na dobieraniu modelu jest w dużej mierze zmarnowany, dopóki
harness jest słaby.

⭐ **To jest uzasadnienie dla istnienia tego kursu** i powód, dla którego nie ma w nim
części o dostrajaniu modeli.

---

## 8. OD ZERA — decyzja architektoniczna na piśmie

Zanim napiszesz linijkę kodu, napisz **ADR** (Architecture Decision Record). To jedna
strona, która za pół roku odpowie Ci na pytanie „dlaczego to jest tak zrobione".

```bash
mkdir -p $OSA/decyzje
cd $OSA
```

```bash
cat > $OSA/decyzje/0001-topologia.md <<'EOF'
# ADR 0001 · Topologia systemu

- **Data:** <dzisiaj>
- **Status:** przyjęta
- **Kontekst:** buduję system dla 3+ agentów osobistych działających tygodniami
  na własnym sprzęcie, z których część wychodzi do sieci.

## Decyzja

Hub-and-spoke z jedną bramą na pętli zwrotnej.

## Dlaczego nie inaczej

- **Graf ze stanem typowanym** — odpada, bo nie znam kształtu zadań z góry.
- **Rój / tablica** — odpada, bo awaria kaskadowa (72,4 % wg OWASP) i brak
  jednego miejsca na politykę.
- **Hierarchia** — nie jako topologia systemu, tylko jako wzorzec wewnątrz
  pojedynczego zadania (subagenci, część 13).

## Konsekwencje

- (+) jedno miejsce na politykę bezpieczeństwa, sesje i obserwowalność
- (+) da się odtworzyć każdą rozmowę z jednego dziennika
- (−) brama jest pojedynczym punktem awarii → wymaga restartu bez utraty stanu (część 18)
- (−) wszystko przechodzi przez jeden proces → limit przepustowości (mierzę w części 13)

## Jak poznam, że to była zła decyzja

Gdy brama stanie się wąskim gardłem przy >3 równoległych sesjach — wtedy
runtime wychodzi do osobnego procesu, brama zostaje.
EOF
```

> 💡 **Ostatnia sekcja jest najważniejsza i prawie nikt jej nie pisze.** „Jak poznam, że
> to była zła decyzja" zamienia opinię w **hipotezę z warunkiem falsyfikacji**. Bez niej
> ADR jest tylko ładnie sformatowanym uprzedzeniem.

---

## 9. PRODUKCYJNIE — co robią frameworki, czego Ty nie robisz

Żeby wiedzieć, co odrzucasz, trzeba wiedzieć, co dostajesz.

| Warstwa | LangGraph | CrewAI | Claude Agent SDK | **Ty** |
| :-- | :-- | :-- | :-- | :-- |
| Pętla | graf, stan typowany | role i zadania | pełna, wbudowana | piszesz (kurs 1) |
| Trwałość | checkpointer | ograniczona | sesje | dziennik zdarzeń (cz. 2) |
| Narzędzia | dekorator | dekorator | wbudowane + MCP | rejestr (cz. 7) |
| Piaskownica | brak | brak | uprawnienia | drabina izolacji (cz. 10) |
| Pamięć | LangMem | podstawowa | pliki + kompakcja | bi-temporalna (cz. 5) |
| Harmonogram | brak | brak | brak | ⭐ heartbeat (cz. 11) |
| Ślady | LangSmith | OTel | wbudowane | OTel (cz. 15) |
| **Model lokalny** | przez adapter | przez LiteLLM | ⚠️ zaprojektowany pod Claude | ⭐ **pierwszej klasy** |

**Dwie kolumny z gwiazdką to powód, dla którego budujesz sam.** Żaden framework nie
traktuje harmonogramu jako warstwy pierwszej klasy, a wszystkie traktują model lokalny
jako adapter doklejony z boku. U Ciebie to jest **rdzeń, a nie wtyczka**.

> ⚠️ **Uczciwie: kiedy framework wygrywa z Tobą.** Gdy potrzebujesz przepływu, który ma
> być audytowalny i zatwierdzony przez kogoś z zewnątrz — graf z typowanym stanem jest
> lepszy niż Twoja pętla, bo **da się go narysować i pokazać**. Zapamiętaj to na moment,
> w którym Twój produkt spotka się z wymogiem zgodności.

---

## 10. EKSPERYMENT 1 — gdzie pęka Twoja pętla z kursu 1

**Hipoteza:** pętla z `$AGENT/agent.py` radzi sobie z zadaniami do ~5 kroków, a powyżej
~10 kroków zawodzi **nie z powodu jakości modelu, tylko z powodu braku warstw systemowych**.

**Procedura.** Przygotuj pięć zadań o rosnącej długości łańcucha i uruchom każde **trzy
razy** (bo interesuje Cię powtarzalność, nie jednorazowy sukces):

```bash
cd ~/llm-education   # katalog repozytorium (u Ciebie może być inny)
source rig-env.sh
mkdir -p $OSA/pomiary
```

| # | Zadanie | Kroków ~ | Co sprawdza |
| :-- | :-- | --: | :-- |
| Z1 | „Przeczytaj `plik.txt` i powiedz, ile ma linii" | 2 | punkt odniesienia |
| Z2 | „Znajdź w `~/dokumenty` wszystkie PDF-y z 2026 i wypisz nazwy" | 4 | wybór narzędzia |
| Z3 | „Dla każdego z tych PDF-ów podaj pierwszą linię" | 8 | pętla po wynikach |
| Z4 | „Zrób to samo, ale wynik zapisz do CSV i sprawdź, czy się zapisał" | 12 | zapis + weryfikacja |
| Z5 | „Powtórz Z4, ale jeśli plik już istnieje, dopisz tylko nowe" | 18 | stan + warunek |

Dla każdego przebiegu notuj:

```
zadanie | próba | sukces | kroków | tokenów | czas | tryb awarii
--------|-------|--------|--------|---------|------|-------------
Z1      | 1     | tak    | 2      |   1 840 | 4 s  | —
...
```

**Tryby awarii nazywaj z tej listy** — to będzie Twoja mapa na resztę kursu:

| Kod | Tryb awarii | Naprawia część |
| :-- | :-- | :-- |
| `KONTEKST` | okno się zapełniło, agent zapomniał celu | 3, 4 |
| `NARZĘDZIE` | wybrał złe narzędzie albo złe argumenty | 7, 8 |
| `PĘTLA` | zapętlił się, powtarza ten sam krok | 3 |
| `CICHY` | powiedział „gotowe", a nie zrobił | 3, 14 |
| `BŁĄD` | dostał błąd i się poddał zamiast poprawić | 3 |
| `STAN` | zgubił, co już zrobił | 2, 5 |

**Czego oczekuję** (⚠️ do sprawdzenia u Ciebie, to jest predykcja, nie pomiar):

```
Z1  ███████████████████████  100 %
Z2  ████████████████████     ~90 %
Z3  ██████████████           ~65 %     ← tu zaczyna się NARZĘDZIE
Z4  ███████                  ~35 %     ← tu wchodzi CICHY i BŁĄD
Z5  ██                       ~10 %     ← tu dominuje KONTEKST i STAN
```

**Zachowaj ten plik.** W części 19 powtórzysz dokładnie ten sam eksperyment na gotowym
systemie i **to porównanie jest oceną całego kursu**.

---

## 11. ĆWICZENIE — założenie systemu

```bash
mkdir -p $OSA/{decyzje,pomiary,dziennik,konfiguracja,agenci,narzedzia,pamiec,testy}
cd $OSA && git init && git add -A && git commit -m "część 1: szkielet katalogów"
```

```
$OSA/
├── decyzje/        ADR — dlaczego jest tak, a nie inaczej
├── pomiary/        wyniki eksperymentów, plik na część
├── dziennik/       dzienniki sesji (część 2)
├── konfiguracja/   konfiguracja jako dane (część 2)
├── agenci/         Archiwista, Badacz, Gospodarz — pliki robocze (część 6)
├── narzedzia/      rejestr narzędzi (część 7)
├── pamiec/         magazyn bi-temporalny (część 5)
└── testy/          zbiór złoty i harness ewaluacyjny (część 14)
```

⭐ **`git init` nie jest ozdobą.** W części 3 git staje się **mechanizmem pamięci
agenta** — sposobem, w jaki nowa sesja dowiaduje się, co zrobiła poprzednia. Zacznij
commitować od dziś.

**Zadanie domowe:** napisz `decyzje/0002-modele.md`. Który model będzie domyślny dla
pętli, który dla zadań trudnych, i **po czym poznasz, że wybrałeś źle**. Bez tego
w części 17 nie zbudujesz routera, bo nie będziesz miał kryterium.

---

## 12. Pułapki tej części

| ID | Pułapka | Objaw | Jak uniknąć |
| :-- | :-- | :-- | :-- |
| **P60** | **Budowanie agenta tam, gdzie wystarczy workflow** | Zadanie działa, ale 30× drożej i czasem losowo zawodzi | Cztery kryteria z §1. Jeśli potrafisz narysować przepływ, nie potrzebujesz agenta |
| **P61** | **Mierzenie jednym przebiegiem** | „Działa!" — a przy trzecim uruchomieniu nie działa | Zawsze ≥3 przebiegi. Agenci są niedeterministyczni **z definicji**, jedno uruchomienie to anegdota |
| **P62** | **Przyjęcie tez autorytetu bez sprawdzenia kontekstu** | Kopiujesz „bez MCP, bez subagentów" i tracisz miesiąc | Sprawdź, czy warunki autora zachodzą u Ciebie. Zwykle nie zachodzą — model, skala i ryzyko są inne |

---

## 13. Checkpoint — co masz po tej części

```bash
# Powinno przejść w całości:
test -d $OSA/decyzje            && echo "✓ katalogi"
test -f $OSA/decyzje/0001-topologia.md && echo "✓ ADR 0001"
test -f $OSA/decyzje/0002-modele.md    && echo "✓ ADR 0002"
test -f $OSA/pomiary/01-gdzie-peka.md  && echo "✓ pomiar bazowy"
git -C $OSA log --oneline | head -3
```

- [ ] Wiesz, kiedy **nie** budować agenta
- [ ] Umiesz policzyć, dlaczego 15-krokowy łańcuch przy 92 %/krok daje 29 %
- [ ] Znasz cztery topologie i wiesz, która umiera i jak
- [ ] Rozłożyłeś OpenClaw na Bramę / Runtime / Narzędzia / Pamięć
- [ ] Rozumiesz różnicę między promptowaniem a projektowaniem pętli
- [ ] **Masz zmierzone, gdzie pęka Twoja obecna pętla** — to jest mapa na resztę kursu

---

**Dalej: `02-SZKIELET-SESJE-KONFIGURACJA.md`** — budujesz bramę, konfigurację jako dane
i dziennik zdarzeń, z którego odtworzysz każdą rozmowę co do bitu.
