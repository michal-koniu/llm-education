# Asymetrie zarobkowe z AI

Gdzie agentowa aplikacja AI w układzie hybrydowym może zarabiać pieniądze w sieci **bez zakładania firmy i bez sprzedawania produktu**?
Przyjrzałem się 22 kandydatom: bounty, konkursom, airdropom kryptowalut, rynkom predykcyjnym, arbitrażowi, płatnej pracy ręcznej,
ankietom, wynajmowi mocy obliczeniowej i roszczeniom. Przy każdym zadałem jedno pytanie: **czy płaci się tu jeszcze za ręczną
pracę, którą moje agenty mogą teraz wykonać szybciej, podczas gdy większość konkurencji nadal robi ją ręcznie?**

Mój układ: lokalny rig z DeepSeek-V4-Flash-0731 (4 równoległe sloty, 24/7), Claude Opus 5.5 jako planista i recenzent
oraz tanie modele online na nadmiarowe zadania ([../tanie-i-darmowe-modele/README.md](../tanie-i-darmowe-modele/README.md)). Mieszkam
w Polsce, więc legalność i podatki sprawdzam z perspektywy polskiego rezydenta. Stan faktów na 14.10.2026.

> **To nie jest porada finansowa, prawna ani podatkowa.** Platformy, regulaminy i ceny zmieniają się co miesiąc. Sprawdź wszystko ponownie, zanim zaczniesz działać, i
> zapytaj doradcę podatkowego o swoją sytuację.

## Krótka odpowiedź

- **Łatwych pieniędzy tu nie ma i research to pokazuje.** Żaden kandydat nie przekroczył 57 punktów na 100. Mediana
  realnego dochodu na okazję to od kilkudziesięciu do kilkuset USD miesięcznie, zwykle nierównomiernie.
- **Tam, gdzie AI jest już wszędzie, asymetria się odwróciła.** Bounty w open source są oblegane przez agenty kodujące
  (od 40 do 1447 komentarzy na bounty), a platformy bug bounty banują teraz masowe „AI slop”. Szybkość nie jest przewagą,
  kiedy wszyscy są szybcy.
- **Pozostała asymetria tkwi w nudnych, lokalnych niszach pełnych papierologii:** obwieszczeniach o licytacjach komorniczych
  i operatach szacunkowych, regulaminach konkursów, warunkach promocji bankowych, małych konkursach data science z 36 zespołami oraz
  red-teamingu AI, gdzie lokalny model bez cenzury generuje ataki bez kosztów tokenów.
- **Prawdziwa praca agenta to wyszukiwanie i selekcja, a nie ostatni krok.** Czyta tysiące ogłoszeń, regulaminów i
  obwieszczeń i podaje mi tych kilka, które są warte mojego czasu. Kliknięcie zatwierdzające, tożsamość i odpowiedzialność zostają przy mnie.
- **Skalowane wersje airdropów, ankiet i questów odrzucam.** Skalują się tylko przez wiele kont albo odpowiedzi
  botów, co łamie regulaminy, a w przypadku ankiet jest oszustwem. Wersje na jedną tożsamość są za małe.
- **Realistyczne portfolio** 4-5 okazji z pierwszej dziesiątki, prowadzonych równolegle na jednym pipelinie agentowym, to według moich szacunków
  **około 500-1300 USD miesięcznie po 3-6 miesiącach** (suma median z profili). To dochód poboczny, który przy okazji
  uczy mnie inżynierii agentów, a nie pensja.

## Pierwsza dziesiątka

Wynik na 100. Realny dochód to przypadek medianowy przy 10 godzinach mojego czasu tygodniowo i agentach działających 24/7.

| # | Okazja | Wynik | Realny dochód | Potrzebny kapitał |
|---|---|---|---|---|
| 1 | [Odzyskiwanie pieniędzy, które już mi się należą](01-OKAZJE.md#1-odzyskiwanie-pieniędzy-które-już-mi-się-należą) | 57 | 20-80 USD/miesiąc uśrednione w skali roku (jedno lub dwa odszkodowania lotnicze plus kilka zwrotów) | 0 USD |
| 2 | [Zlecenia freelance za zadanie (Upwork, Fiverr, Useme)](01-OKAZJE.md#2-zlecenia-freelance-za-zadanie-upwork-fiverr-useme) | 56 | 0-300 USD/mies. w miesiącach 1-2, mediana 200-800 USD/mies., gdy profil ma już opinie | ~0-50 USD (Connects na Upwork) |
| 3 | [Konkursy data science i AI](01-OKAZJE.md#3-konkursy-data-science-i-ai) | 56 | 0-200 USD/miesiąc średnio w skali roku (przypadek medianowy: 0, z rzadkimi jednorazowymi wygranymi 1000-10 000 USD) | 0 USD (lokalny rig pokrywa trening i inferencję offline) |
| 4 | [Bounty i areny red-teamingu AI](01-OKAZJE.md#4-bounty-i-areny-red-teamingu-ai) | 55 | mediana 0-300 USD/miesiąc (nierówno: w większości miesięcy 0, od czasu do czasu znalezisko za 500-2500 USD) | ~0-100 USD (tokeny API dla sędziego) |
| 5 | [Turnieje prognostyczne AI (legalna strona rynków predykcyjnych)](01-OKAZJE.md#5-turnieje-prognostyczne-ai-legalna-strona-rynków-predykcyjnych) | 55 | 0-150 USD/miesiąc w przypadku medianowym (nagrody są sezonowe i nieregularne) | 0 USD (sponsorowane kredyty LLM) |
| 6 | [Licytacje komornicze i przetargi publiczne](01-OKAZJE.md#6-licytacje-komornicze-i-przetargi-publiczne) | 52 | 0-400 USD/miesiąc (mediana ~150 USD po powolnym pierwszym kwartale) | 1000-2000 USD w obrocie (rękojmie plus cena zakupu) |
| 7 | [Konkursy audytowe smart kontraktów i bug bounty](01-OKAZJE.md#7-konkursy-audytowe-smart-kontraktów-i-bug-bounty) | 52 | 0-500 USD/miesiąc (przypadek medianowy dla nowicjusza przy 10 h/tydzień: ok. 0-200) | 0 USD (plus tokeny API; żadne środki nie są zagrożone) |
| 8 | [Konkursy z nagrodami za zadanie twórcze (polskie „konkursy”, konkursy projektowe)](01-OKAZJE.md#8-konkursy-z-nagrodami-za-zadanie-twórcze-polskie-konkursy-konkursy-projektowe) | 51 | mediana 0-200 USD/mies., głównie w rzeczach, bardzo nierówno | 0 (więcej, jeśli gonisz konkursy paragonowe) |
| 9 | [Śledzenie promocji bankowych](01-OKAZJE.md#9-śledzenie-promocji-bankowych) | 51 | 50-150 USD/miesiąc średnio w skali roku (około 2500-6000 PLN/rok, mediana ~3500 PLN) | 0 (przepuszczasz przez konta własną pensję i wydatki) |
| 10 | [Bug bounty dla aplikacji webowych i mobilnych z rekonesansem wspieranym przez AI](01-OKAZJE.md#10-bug-bounty-dla-aplikacji-webowych-i-mobilnych-z-rekonesansem-wspieranym-przez-ai) | 48 | 0-300 USD/miesiąc (przypadek medianowy: 0 w pierwszych 2-3 miesiącach, potem sporadyczne wypłaty za błędy o niskiej/średniej wadze) | ~0-50 USD (tokeny API, VPS do callbacków out-of-band) |

Tuż za progiem, ale z pełnymi profilami:

| # | Okazja | Wynik | Realny dochód | Potrzebny kapitał |
|---|---|---|---|---|
| 11 | [Ekspercka praca przy trenowaniu AI (Outlier, DataAnnotation, Alignerr, Mindrift)](01-OKAZJE.md#11-ekspercka-praca-przy-trenowaniu-ai-outlier-dataannotation-alignerr-mindrift) | 47 | 300-900 USD/mies. przy 10 h/tydz. własnego czasu, przypadek medianowy, z pustymi tygodniami | 0 |
| 12 | [Arbitraż na marketplace'ach (OLX, Allegro, Vinted)](01-OKAZJE.md#12-arbitraż-na-marketplaceach-olx-allegro-vinted) | 45 | 50-400 USD/miesiąc (mediana ~150 USD) | 500-1500 USD w towarze |
| 13 | [Bounty za zgłoszenia open source](01-OKAZJE.md#13-bounty-za-zgłoszenia-open-source) | 44 | 0-150 USD/miesiąc (przypadek medianowy: blisko 0) | 0 USD (plus kilka USD na tokeny API) |
| 14 | [Odsprzedaż wygasłych domen](01-OKAZJE.md#14-odsprzedaż-wygasłych-domen) | 37 | 0-100 USD/miesiąc (mediana bliska 0 w pierwszym roku, często ujemna po odnowieniach) | 300-1500 USD rocznie na rejestracje i odnowienia |
| 15 | [Wynajem bezczynnego rigu GPU](01-OKAZJE.md#15-wynajem-bezczynnego-rigu-gpu) | 36 | mediana 0-50 USD/miesiąc netto (karty AMD prawie nie znajdują najemców) | 0 USD (rig już posiadany) |

**Jak czytać ranking.** Wynik nagradza bezpieczeństwo i legalność tak samo jak pieniądze. Dlatego „odzyskiwanie pieniędzy, które
już mi się należą” jest na pierwszym miejscu: to czyste i pewne, ale małe. Jeśli posortuję według **zarobków plus asymetrii** (E + A),
kolejność się zmienia: licytacje komornicze i publiczne (21), konkursy z nagrodami (18), zlecenia freelance i red-teaming AI (17),
konkursy audytowe (16). Eksperckie trenowanie AI płaci najwięcej za godzinę (300-900 USD miesięcznie), ale prawie nie daje
dźwigni agentowi, bo płatną część musi wykonać człowiek.

## Jak punktowałem

| Litera | Co mierzy | Punkty |
|---|---|---|
| E | Realny zarobek netto miesięcznie, przypadek medianowy (poniżej 100 USD = 3, 100-500 = 8, 500-1500 = 14, 1500-4000 = 20, powyżej 4000 = 25) | 25 |
| A | Asymetria: o ile agent zwielokrotnia wydajność względem konkurentów pracujących ręcznie i jak niewielu już automatyzuje | 25 |
| F | Wykonalność: kapitał, umiejętności, czas uruchomienia, dostęp z Polski | 15 |
| L | Prawo i regulaminy: na ile czysta jest zautomatyzowana wersja w Polsce i UE (naruszenie oznacza odrzucenie) | 20 |
| R | Ryzyko: zmienność, utrata kapitału, ryzyko bana, jak szybko zamyka się okno (więcej = bezpieczniej) | 15 |

Remisy rozstrzyga E + A. Każdy profil pokazuje swoje wyniki cząstkowe, więc możesz samodzielnie zmienić wagi.

## Od czego bym zaczął

1. **Zbuduj pipeline raz** ([02-ARCHITEKTURA-HYBRYDOWA.md](02-ARCHITEKTURA-HYBRYDOWA.md)): obserwatory, lokalna selekcja,
   recenzja Opusa, bramka zatwierdzenia przez człowieka i rejestr SQLite każdej próby.
2. **Przeprowadź równolegle trzy tygodniowe testy**, każdy profil ma swój: jedną zagrywkę asymetryczną bez kapitału (red-teaming AI albo
   mały konkurs data science), jedno stałe źródło zarobku (zlecenia freelance na Useme lub Upwork) i jedną polską niszę
   papierologiczną (licytacje komornicze albo konkursy z nagrodami).
3. **Dodaj nawyki „darmowych pieniędzy”**, które prawie nie wymagają czasu agenta: roszczenia i promocje bankowe.
4. **Zastosuj kryteria przerwania** na koniec każdego testu. Zostaw to, co je przejdzie, odrzuć resztę i przenieś zwolniony
   slot na kolejnego kandydata z listy.

## Odrzuceni kandydaci

| Kandydat | Dlaczego odrzucony |
|---|---|
| Farmienie airdropów i punktów | Skalowana wersja to sybilowe farmienie na wielu portfelach: filtrowane i banowane (Linea, LayerZero). Jeden prawdziwy portfel z trackerem jest legalny, ale mały. |
| Płatne ankiety i mikrozadania | Odpowiedzi wypełniane przez agenta łamią zasady MTurk i Prolific, są wykrywane i oszukują badacza. Ankiety wypełniane ręcznie płacą stawki ankietowe. |
| Platformy questów krypto | Skalowanie wymaga wielu kont albo sztucznego zaangażowania, czego zabrania regulamin Galxe. |
| Boty DeFi (likwidacje, arbitraż, MEV) | Już w pełni zautomatyzowane przez profesjonalnych searcherów; wymagają kapitału i niskich opóźnień; agent nie daje przewagi. |
| Kopanie na subnetach Bittensor | Główne subnety wymagają kart NVIDIA i Intel TDX; wypłaty idą za ceną TAO. Niewykonalne na AMD za 2000 USD. |
| Zdecentralizowane sieci AI | Głównie punkty z testnetów, klienty tylko na NVIDIA, a farmienie węzłów to zachowanie sybilowe. |
| Odsprzedaż biletów i błędy cenowe | Odsprzedaż biletów powyżej ceny nominalnej to w Polsce wykroczenie (art. 133 Kodeksu wykroczeń); błędy cenowe nie są dochodem. |

Pełne notatki ze źródłami znajdziesz na końcu [01-OKAZJE.md](01-OKAZJE.md).

## Pliki

| Plik | Co zawiera |
|---|---|
| [01-OKAZJE.md](01-OKAZJE.md) | 15 profili: przepływ pieniędzy, asymetria, pipeline agentowy, podział hybrydowy, liczby, jak zacząć, zasady, test tygodniowy, kryteria przerwania; potem notatki o odrzuconych |
| [02-ARCHITEKTURA-HYBRYDOWA.md](02-ARCHITEKTURA-HYBRYDOWA.md) | Jeden pipeline agentowy dla wszystkich okazji, routing lokalny kontra płatny, rachunek kosztów, rejestr przewag, zabezpieczenia, harmonogram riga |
| [03-ZASADY-PODATKI-RYZYKA.md](03-ZASADY-PODATKI-RYZYKA.md) | Polskie podatki dla każdego rodzaju dochodu, raportowanie DAC7 i DAC8, prawo hazardowe, prawo dotyczące badań bezpieczeństwa, regulaminy platform, ryzyka operacyjne |
| [ZRODLA.md](ZRODLA.md) | Wszystkie źródła, dostęp 13-14.10.2026 |

**Ograniczenia researchu.** Niektóre liczby nie zostały nigdzie opublikowane w miejscach, do których dotarłem, np. prowizje Fiverr i Useme, pule nagród Gray Swan
i mediana zarobków w bug bounty. Profile oznaczają je jako „nie znaleziono”, zamiast zgadywać. Powiązane kursy:
[../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md](../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md),
[../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md](../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md),
[../harnessy-agentowe/README.md](../harnessy-agentowe/README.md).
