# Część 02 · Audyt kontraktu: na co pozwala Twój kontrakt B2B

> **Cel tej części.** Czytasz swoją umowę z bankiem klauzula po klauzuli i wypełniasz macierz: co mówi o IP,
> konkurencji, poufności, dostępności, narzędziach i rozwiązaniu umowy — i co o każdej z tych klauzul mówi
> polskie prawo. Poznajesz nowe przepisy z 2026 roku o uznawaniu kontraktów B2B za stosunek pracy. Decydujesz,
> czy prosić klienta o pisemne potwierdzenie, i masz gotowy list.
>
> **Czas:** ~5 h + godzina z prawnikiem · **Poziom:** ⭐⭐⭐⭐ · **Efekt:** `founder/02-clause-matrix.md`,
> opcjonalnie `founder/02-letter-draft.md`

> **To nie jest porada prawna.** Ta część uczy Cię **czytać** umowę i zadawać właściwe pytania. Jedna płatna
> godzina z prawnikiem, który przeczyta Twoją prawdziwą umowę, jest warta więcej niż cała ta część. Odbądź ją,
> zanim podpiszesz cokolwiek z klientem.

---

## 0. Problem

Twój startup będzie wytwarzał oprogramowanie, prompty, zbiory ewaluacyjne i dokumentację i będzie sprzedawał
na rynek sąsiadujący z bankowością (kancelarie i biura, może kiedyś doradcy finansowi). Twoją umowę z bankiem
napisali prawnicy banku, żeby chronić bank. Prawdopodobnie zawiera:

- klauzulę przenoszącą na bank autorskie prawa majątkowe do „utworów";
- klauzulę poufności, być może z tajemnicą bankową;
- może zakaz konkurencji;
- kary umowne za naruszenie tych klauzul;
- klauzule DORA (prawo audytu, bezpieczeństwo, podwykonawstwo), bo dostawcy IT banków są dziś regulowani.

Żadna z nich nie jest problemem, **jeśli wiesz, co mówi**. Każda jest poważnym problemem, jeśli dowiesz się
o niej dopiero wtedy, gdy zapyta o nią prawnik inwestora (część 03) albo gdy napisze do Ciebie prawnik banku.

---

## 1. Prawo autorskie: kto jest właścicielem tego, co piszesz

### 1.1 Zasady

Z ustawy o prawie autorskim i prawach pokrewnych (Dz.U. 2025 poz. 24), według researchu do tego kursu:

| Zasada | Przepis | Co to znaczy dla Ciebie |
| :-- | :-- | :-- |
| Przeniesienie praw lub licencja obejmuje **tylko pola eksploatacji wyraźnie w niej wymienione** | art. 41 ust. 2 | „wszelkie prawa" bez listy to słaby zapis; bank ma tylko to, co wymieniono |
| Umowa jest **nieważna w zakresie, w jakim dotyczy wszystkich utworów przyszłych** twórcy albo wszystkich jego utworów przyszłych określonego rodzaju | art. 41 ust. 3 | „wszystko, co stworzysz w okresie obowiązywania umowy" jest co najmniej częściowo nieważne |
| Umowa może obejmować tylko pola eksploatacji **znane w chwili jej zawarcia** | art. 41 ust. 4 | |
| Przeniesienie praw **wymaga formy pisemnej** pod rygorem nieważności | art. 53 | żadnych przeniesień w stylu „bierzcie" w e-mailu |
| Pracodawca nabywa prawa do utworów (art. 12) i programów (art. 74 ust. 3) stworzonych przez **pracownika** w ramach obowiązków ze stosunku pracy | art. 12, art. 74 ust. 3 | **nie dotyczy Ciebie** jako kontraktora B2B — bank dostaje tylko to, co przenosi umowa |

Konkretne, dobrze oznaczone utwory przyszłe *można* przenieść (PARP); nieważne jest ogólnikowe „wszystko".

### 1.2 Czego szukać w swojej umowie

Typowa, zbyt szeroka klauzula IT wygląda tak (przykład z researchu, nie Twoja umowa):

> *„Wykonawca przenosi na Zamawiającego autorskie prawa majątkowe do wszelkich utworów, w tym programów
> komputerowych, stworzonych w okresie obowiązywania Umowy…"*

Jej problemy: obejmuje **wszystkie** utwory, więc koliduje z art. 41 ust. 3; nie oddziela pracy wykonanej
**dla klienta** od pracy wykonanej w Twoim czasie i na Twoich narzędziach; a lista pól eksploatacji jest często
ogólnikowa.

To, że klauzula jest prawdopodobnie częściowo nieważna, **nie** jest planem. Klauzulę nieważną „w części" i tak
trzeba wykazać przed sądem. Chcesz umowy, w której przeniesienie jest wyraźnie powiązane z **rezultatami
wytworzonymi w ramach wykonywania umowy lub konkretnych zleceń**, z wyraźnym wyłączeniem IP istniejącego
wcześniej i niezależnej pracy wykonanej poza umową, bez zasobów klienta i bez jego informacji poufnych. Temu
służy list z sekcji 8.

---

## 2. Zakaz konkurencji: czego nie wolno Ci robić

### 2.1 Zasady

- Między przedsiębiorcami zakaz konkurencji jest dopuszczalny w ramach **swobody umów** (art. 353¹ KC),
  ograniczonej art. 58 KC (nieważność czynności sprzecznej z ustawą lub z zasadami współżycia społecznego).
- **Żaden przepis nie wymaga odszkodowania** za zakaz konkurencji w kontrakcie B2B. Przepisy Kodeksu pracy —
  odrębna umowa na piśmie i odszkodowanie co najmniej **25%** wynagrodzenia po ustaniu zatrudnienia
  (art. 101¹–101³ KP) — dotyczą wyłącznie pracowników.
- Orzecznictwo:
  - **SN, wyrok z 11 września 2003 r., III CKN 579/01:** zakaz konkurencji **w trakcie** trwania umowy jest
    ważny. **Trzyletni zakaz po rozwiązaniu umowy** **bez odszkodowania** był **nieważny** jako sprzeczny
    z zasadami współżycia społecznego, w drodze analogii do Kodeksu pracy.
  - **SN, wyrok z 19 listopada 2015 r., IV CSK 804/14** (za: Rzeczpospolita): między przedsiębiorcami **sam**
    brak odszkodowania nie czyni klauzuli nieważną — staje się nieważna, jeśli narzucono ją, wykorzystując
    silniejszą pozycję negocjacyjną.

### 2.2 Czego szukać

1. **Czy w ogóle jest?** Wiele kontraktów B2B w IT nie ma go wcale albo ma tylko klauzulę o zakazie
   podkupywania pracowników (non-solicitation) — nie wolno Ci podbierać bankowi ludzi ani klientów.
2. **Zakres:** jak zdefiniowano „działalność konkurencyjną"? Bankowość? Oprogramowanie finansowe? „Wszelkie
   usługi IT"? AI box dla kancelarii nie konkuruje z bankiem — **chyba że** klauzula brzmi „wszelka działalność
   w obszarze IT" albo „na rzecz jakiejkolwiek instytucji finansowej". Wpisz do macierzy dokładne brzmienie.
3. **Czas trwania:** tylko w trakcie umowy czy także po niej? Jak długo?
4. **Odszkodowanie:** brak czy płatne?

---

## 3. Poufność, tajemnica przedsiębiorstwa i tajemnica bankowa

| Źródło | Co mówi | Skutek dla startupu |
| :-- | :-- | :-- |
| **Ustawa o zwalczaniu nieuczciwej konkurencji, art. 11** (Dz.U. 2026 poz. 85) | wykorzystanie lub ujawnienie cudzej tajemnicy przedsiębiorstwa jest czynem nieuczciwej konkurencji; wiąże Cię **z mocy ustawy**, nie tylko umowy. **Niezależne opracowanie i inżynieria wsteczna legalnie uzyskanego, publicznie dostępnego produktu są zgodne z prawem** (art. 11 ust. 7) | architektura, kod, prompty, warunki dostawców, dane i dokumenty wewnętrzne banku nigdy nie mogą trafić do Twojego produktu. Twoja własna, niezależnie zbudowana praca jest Twoja |
| **Prawo bankowe, art. 104** (Dz.U. 2026 poz. 38) | tajemnica bankowa wiąże bank, jego pracowników i osoby, za pośrednictwem których bank wykonuje czynności; dostawcy w ramach outsourcingu bankowego, którzy otrzymują dane objęte tajemnicą, mogą ich używać **wyłącznie** do wykonania umowy (art. 104 ust. 5) | kara za naruszenie: grzywna do 1 000 000 PLN i pozbawienie wolności do lat 3 (art. 171 ust. 5). Czy wiąże pojedynczego kontraktora IT, który nigdy nie widzi danych klientów, **nie jest przesądzone** — banki i tak nakładają ją umownie |
| **NDA w Twojej umowie** | zwykle szersze niż oba powyższe | przeczytaj definicję „informacji poufnych" — często obejmuje „know-how" |

Praktyczna zasada jest prosta i surowa: **nic z banku nie wchodzi do startupu.** Ani kod, ani dokumenty, ani
dane, ani wiadomość ze Slacka, ani „wzorzec, który tam widziałem". Część 03 zamienia tę zasadę w procedurę.

---

## 4. DORA: dlaczego prawników banku obchodzisz Ty

Rozporządzenie DORA o operacyjnej odporności cyfrowej (rozporządzenie (UE) 2022/2554) stosuje się do banków od
**17 stycznia 2025 r.** Reguluje **bank**, nie Ciebie — ale wymaga od banku wpisania określonych postanowień do
każdej umowy na usługi ICT, a te postanowienia dosięgają Ciebie:

| Wymóg DORA (art. 28, 30) | Jak może się pojawić w Twojej umowie |
| :-- | :-- |
| Rejestr wszystkich umów ICT; ocena ryzyka przed zawarciem umowy | bank klasyfikuje Twoją usługę — zapytaj, jak |
| Prawo rozwiązania umowy za naruszenia, słabości w zarządzaniu ryzykiem ICT, przeszkody w nadzorze (art. 28 ust. 7) | podstawy, na których bank może zakończyć Twoją umowę |
| Prawa i obowiązki w **jednym dokumencie pisemnym** (art. 30 ust. 1) | aneks — „Aneks DORA" |
| Czy podwykonawstwo jest dozwolone i na jakich warunkach (art. 30 ust. 2 lit. a) | nie możesz zlecić pracy nikomu innemu |
| Lokalizacje danych, poufność, pomoc przy incydentach, współpraca z organami, szkolenia z bezpieczeństwa (art. 30 ust. 2) | obowiązek zgłaszania incydentów, udziału w szkoleniach |
| Dla funkcji krytycznych lub istotnych: prawo audytu i dostępu dla banku i KNF, strategia wyjścia i okres przejściowy (art. 30 ust. 3) | bank może audytować „Twoje systemy" — sprawdź, jak je zdefiniowano |

Polskie rynkowe wzory aneksów DORA traktują JDG pracującą osobiście jako **personel**, a nie podwykonawcę
(wzór MessageFlow, 2025). Nie ma wytycznych europejskich organów nadzoru ani KNF dotyczących jednoosobowych
kontraktorów.

**Dlaczego to ważne dla startupu:** klauzula audytu zdefiniowana jako „systemy ICT wykonawcy wykorzystywane do
świadczenia usług" jest w porządku. Zdefiniowana jako „wszystkie systemy wykonawcy" sięgałaby teoretycznie
maszyn, na których budujesz startup. Kolejny powód rozdzielenia z części 03.

---

## 5. Kary umowne

Z Kodeksu cywilnego:

- Karę umowną można zastrzec za niewykonanie lub nienależyte wykonanie zobowiązania **niepieniężnego** —
  poufności, zakazu konkurencji, IP (art. 483 KC).
- Należy się **bez względu na wysokość szkody** (art. 484 § 1 KC); Sąd Najwyższy potwierdził, że należy się
  nawet wtedy, gdy **szkody nie ma wcale** (uchwała składu siedmiu sędziów z 6 listopada 2003 r., III CZP 61/03).
- Sąd może obniżyć karę **rażąco wygórowaną** albo gdy zobowiązanie zostało w znacznej części wykonane —
  miarkowanie kary (art. 484 § 2 KC).

Wpisz do macierzy każdą kwotę kary. Kara umowna 100 000 zł za naruszenie poufności, należna bez szkody, to
liczba, która powinna kształtować Twoje zachowanie — a nie prawdopodobieństwo procesu.

---

## 6. Uznanie za stosunek pracy: przepisy z 2026 roku

### 6.1 Co się zmieniło

Nowelizacja ustawy o Państwowej Inspekcji Pracy z 11 marca 2026 r. (**Dz.U. 2026 poz. 473**) **obowiązuje od
8 lipca 2026 r.** Najważniejsze punkty, według researchu:

| Zasada | Szczegóły |
| :-- | :-- |
| **Okręgowy inspektor pracy może w drodze decyzji administracyjnej stwierdzić istnienie stosunku pracy** | gdy praca jest wykonywana w warunkach z art. 22 § 1 KP: pod kierownictwem klienta, w miejscu i czasie przez niego wyznaczonym, za wynagrodzeniem |
| Najpierw **polecenie** | inspektor najpierw wydaje polecenie usunięcia naruszenia; decyzja zapada dopiero wtedy, gdy polecenie nie zostanie wykonane |
| **Wola stron się liczy** | trzeba ją uwzględnić, chyba że jest sprzeczna z prawem albo ma na celu jego obejście (art. 33a ust. 4) |
| Skutki **od dnia wydania decyzji** | dla prawa pracy, podatków, ubezpieczeń społecznych i zdrowotnego; sięgnięcie dalej wstecz wymaga sprawy sądowej |
| Domniemania przy braku dowodów | czas nieokreślony, pełny etat, **minimalne wynagrodzenie** |
| Odwołanie | do sądu pracy w ciągu miesiąca |
| **Dotyczy istniejących umów** | umów zawartych przed 8 lipca 2026 r., które nadal trwają |
| „Amnestia" dla klienta | brak kary, jeśli klient dobrowolnie przekształci pozorny kontrakt B2B w umowę o pracę **do 8 lipca 2027 r.** |
| Wymiana danych | PIP, ZUS i Krajowa Administracja Skarbowa (KAS) wymieniają dane do analizy ryzyka |
| Interpretacje indywidualne | Główny Inspektor Pracy wydaje interpretację indywidualną GIP dotyczącą opisanego stosunku, opłata **40 PLN** |

Sam art. 22 KP **nie** się zmienił: stosunek pracy jest tym, czym był zawsze; inspektor ma teraz szybsze
narzędzie, żeby to stwierdzić.

Pierwsza praktyka: do 25 sierpnia 2026 r. Główny Inspektor Pracy wydał 9 interpretacji — 4 potwierdziły
stosunek cywilnoprawny, 5 stwierdziło stosunek pracy. Jedna dotyczyła **pracy IT w modelu B2B i nie stwierdziła
stosunku pracy**, bo praca była wykonywana na podstawie odrębnych zleceń, które można było odrzucić, klient
określał rezultaty i terminy, ale nie metodę, a wykonawca ponosił ryzyko gospodarcze i dostawał wynagrodzenie
za usługę (PIP, 30 września 2026 r.).

### 6.2 Dlaczego to ważne dla założyciela

Gdyby Twój kontrakt kiedykolwiek uznano za stosunek pracy, od dnia decyzji:

- **IP:** zastosowanie miałyby art. 12 i art. 74 ust. 3 ustawy o prawie autorskim — utwory i programy, które
  tworzysz **w ramach obowiązków**, należałyby do banku. Startup poza Twoimi obowiązkami zostaje Twój, ale
  „oprogramowanie AI" i „oprogramowanie dla banku" są na tyle blisko, że można się o to spierać.
- **Zakaz konkurencji:** zastosowanie miałyby przepisy Kodeksu pracy; w trakcie zatrudnienia pracodawca może
  zakazać działalności konkurencyjnej bez odszkodowania (art. 101¹ KP).
- **Podatki:** podatnik traci ryczałt na dany rok, jeśli wystawia faktury obecnemu lub byłemu pracodawcy za
  pracę, którą wykonywał dla niego jako pracownik (art. 8 ust. 2 ustawy o zryczałtowanym podatku dochodowym).

### 6.3 Twoje wskaźniki ryzyka — szczerze

Z Twojego opisu: kontrakt płaci **za dzień**, a praca zajmuje **około godziny dziennie**. Czytaj tabelę
z tym w głowie:

| Wskazuje na stosunek pracy | Wskazuje przeciw stosunkowi pracy |
| :-- | :-- |
| wynagrodzenie za dzień dostępności, a nie za rezultat | niewiele godzin faktycznej pracy; brak stałego miejsca |
| stałe godziny albo okna dostępności wyznaczone przez bank | sam wybierasz, jak wykonać pracę |
| codzienne raportowanie, przełożony, który wydaje polecenia co do metody | ponosisz ryzyko gospodarcze (nieopłacone dni wolne, własny sprzęt) |
| jeden klient od lat, włączenie w zespół banku | inni klienci — **w tym Twój własny startup** |

Ostatni wiersz to pożyteczna ironia: prawdziwa, odrębna własna działalność jest jednym z sygnałów, że jesteś
przedsiębiorcą, a nie pracownikiem. Zbuduj ją czysto (część 03), a będzie wspierać Twój status B2B, zamiast mu
zagrażać.

---

## 7. ĆWICZENIE 02 — macierz klauzul

Utwórz `founder/02-clause-matrix.md`. Jeden wiersz na klauzulę; cytuj klauzulę **dosłownie**:

| # | Temat | Klauzula (dokładny tekst, nr §) | Co obejmuje | Co mówi prawo (sekcja tej części) | Ryzyko dla startupu (N/Ś/W) | Działanie |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| 1 | Przeniesienie praw autorskich (IP) | | | §1 | | |
| 2 | IP istniejące wcześniej / wyłączenie | | | §1 | | |
| 3 | Zakaz konkurencji w trakcie umowy | | | §2 | | |
| 4 | Zakaz konkurencji po umowie | | | §2 | | |
| 5 | Klauzula o zakazie podkupywania pracowników (non-solicitation) | | | §2 | | |
| 6 | Poufność / definicja informacji poufnych | | | §3 | | |
| 7 | Tajemnica bankowa | | | §3 | | |
| 8 | Aneks DORA: zakres audytu, podwykonawstwo, incydenty | | | §4 | | |
| 9 | Dostępność, godziny pracy, raportowanie | | | §6 | | |
| 10 | Korzystanie ze sprzętu, kont i narzędzi AI banku | | | §3 | | |
| 11 | Wyłączność / zgoda na inną działalność | | | §2 | | |
| 12 | Kary umowne (kwota przy każdej klauzuli) | | | §5 | | |
| 13 | Rozwiązanie umowy i okres wypowiedzenia | | | — | | |

Ryzyko: N — niskie, Ś — średnie, W — wysokie.

Potem umów się na **godzinę z prawnikiem** (prawo pracy i umowy IT), wyślij mu umowę i swoją macierz i zadaj
trzy pytania: *Czy klauzula IP sięga pracy, którą wykonuję w swoim czasie na własnym sprzęcie? Czy jest
klauzula, którą naruszyłaby moja działalność z AI boxem? Co należałoby zmienić?*

---

## 8. Pytać czy nie pytać: list

Możesz poprosić bank o pisemne potwierdzenie, że Twoja odrębna działalność jest poza zakresem umowy. Zważ
argumenty:

| Zapytać | Nie pytać (jeszcze) |
| :-- | :-- |
| pisemne wyłączenie raz na zawsze zamyka kwestię IP — inwestorzy o nie zapytają (część 03) | zwraca uwagę na działalność poboczną; niektórzy przełożeni reagują źle |
| jeśli bank odmówi, dowiadujesz się tego teraz, a nie po zbudowaniu produktu | jeśli umowa już jest czysta (opinia prawnika), nie ma czego naprawiać |
| to uczciwe i profesjonalne | |

**Moja rekomendacja:** najpierw niech prawnik przeczyta umowę. Jeśli klauzule IP albo zakazu konkurencji są
szerokie, zapytaj — zanim napiszesz kod produktu, a nie po. Jeśli są czyste, zachowaj pisemną opinię prawnika
w dokumentach i zapytaj dopiero wtedy, gdy będziesz blisko podpisania umowy z inwestorem.

Szkic do dopracowania przez Twojego prawnika:

> **Szanowni Państwo,**
>
> w związku z umową nr … z dnia … informuję, że poza jej wykonywaniem prowadzę odrębną działalność
> polegającą na tworzeniu i sprzedaży oprogramowania do lokalnej analizy dokumentów dla kancelarii i biur
> rachunkowych. Działalność ta nie obejmuje usług dla instytucji finansowych, jest prowadzona poza czasem
> świadczenia usług na rzecz Państwa, na moim własnym sprzęcie i bez wykorzystania jakichkolwiek informacji,
> zasobów ani dokumentów Banku.
>
> Proszę o potwierdzenie, że (1) postanowienia § … umowy dotyczące przeniesienia autorskich praw majątkowych
> obejmują wyłącznie utwory stworzone w ramach wykonywania umowy i zleceń na jej podstawie, a nie utwory
> powstałe w ramach opisanej działalności, oraz (2) działalność ta nie stanowi działalności konkurencyjnej
> w rozumieniu § … umowy.
>
> Z poważaniem, …

W skrócie: list informuje bank o odrębnej działalności i prosi o potwierdzenie, że klauzula o przeniesieniu
autorskich praw majątkowych obejmuje tylko utwory z wykonania umowy i zleceń, a ta działalność nie jest
konkurencyjna w rozumieniu klauzuli o zakazie konkurencji.

---

## 9. ⭐ EKSPERYMENT TERENOWY 02 — co naprawdę mówi umowa?

**Hipoteza.** Twoja umowa zawiera klauzulę IP szerszą niż „rezultaty w ramach zleceń", nie ma zakazu konkurencji
po rozwiązaniu umowy, ma klauzulę poufności z karą umowną i aneks DORA dodany w 2025 roku.

**Procedura.** Wypełnij macierz (ćwiczenie 02) na podstawie podpisanej umowy i każdego aneksu, w tym aneksu DORA
i każdej późniejszej zmiany. Potem porównaj z odczytaniem prawnika.

**Predykcja (moja).** Klauzula IP: szeroka („wszystkie utwory stworzone w okresie obowiązywania umowy"). Zakaz
konkurencji: tylko w trakcie umowy, w zakresie bankowości albo „usług dla konkurentów banku". Kara: stała kwota
za każde naruszenie poufności. Aneks DORA: jest, z prawem audytu i zakazem podwykonawstwa.

| Klauzula | Moja predykcja | Co mówi umowa | Zdanie prawnika | Działanie |
| :-- | :-- | :-- | :-- | :-- |
| IP | szeroka | | | |
| Zakaz konkurencji | w trakcie umowy, zakres: bankowość | | | |
| Kary umowne | stała kwota za naruszenie | | | |
| Aneks DORA | jest | | | |
| Dostępność | godziny pracy banku | | | |

---

## 10. Pułapki

**B6 · Poleganie na „ta klauzula jest pewnie nieważna".**
*Objaw:* budujesz mimo wszystko, bo art. 41 ust. 3 czyni klauzulę częściowo nieważną. *Dlaczego boli:* musiałbyś
to wykazać przed sądem, przeciwko bankowi. *Lekarstwo:* pisemne wyłączenie albo pisemna opinia prawnika.

**B7 · Przeczytana umowa, nieprzeczytane aneksy.**
*Objaw:* macierz wypełniona na podstawie umowy z 2023 roku; aneks DORA z 2025 roku nieprzeczytany. *Lekarstwo:*
każdy aneks, każda zmiana, każda polityka, którą umowa włącza „przez odesłanie".

**B8 · Materiały banku w startupie.**
*Objaw:* „to tylko wzorzec, który widziałem w pracy", szablon dokumentu, prompt. *Dlaczego boli:* tajemnica
przedsiębiorstwa, być może tajemnica bankowa i kary umowne należne bez szkody. *Lekarstwo:* zasada z sekcji 3 —
nic z banku, nigdy.

**B9 · Ignorowanie tego, jak zorganizowane są dni.**
*Objaw:* stałe godziny, codzienne raporty i polecenia co do metody, wynagrodzenie za dzień — i zero refleksji.
*Lekarstwo:* znaj swoje wskaźniki (sekcja 6.3); prawdziwa odrębna działalność pomaga.

**B10 · List wysłany, zanim prawnik przeczytał umowę.**
*Objaw:* prosisz bank o potwierdzenie, którego umowa nie potrzebuje, albo źle je formułujesz.
*Lekarstwo:* najpierw prawnik, potem list (sekcja 8).

---

## 11. Checkpoint

- [ ] `founder/02-clause-matrix.md` jest wypełniona dosłownymi cytatami z umowy **i** wszystkich aneksów.
- [ ] Każda kwota kary umownej jest zapisana.
- [ ] Prawnik przeczytał umowę (albo spotkanie jest umówione, z datą).
- [ ] Zdecydowałeś: list teraz, list później albo list niepotrzebny — z uzasadnieniem.
- [ ] Potrafisz wskazać trzy najsilniejsze i trzy najsłabsze wskaźniki w tabeli uznania za stosunek pracy.

Źródła do tej części: [ZRODLA.md](ZRODLA.md), sekcja „Część 02".
