# Polska i suwerenność danych — asystent, który nie wysyła danych do USA

**Stan na 11 października 2026.**

> ⚖️ **To nie jest porada prawna.** To materiał edukacyjny: streszczam przepisy, wytyczne samorządów zawodowych
> i komentarze, zawsze ze wskazaniem aktu i artykułu albo dokumentu. Przepisy i ich interpretacje zmieniają się
> szybko (AI Act po Omnibusie, nowa polska ustawa, odwołanie w sprawie DPF). Zanim oprzesz na tym produkt, umowę
> albo decyzję zawodową — zapytaj radcę prawnego lub adwokata. Ceny i liczby mają datę i źródło; sprzęt i modele
> nie były mierzone na mojej maszynie — to liczby z benchmarków społeczności i stron producentów.

Ta część odpowiada na pytanie, które stawiam sobie przy każdym asystencie dla adwokata, lekarza czy doradcy
podatkowego: **co musi się stać, żeby dane klienta nie wyszły z gabinetu — i czy ktoś za to zapłaci?** Najpierw
prawo (dlaczego „nie do USA" to nie fanaberia), potem tajemnice zawodowe, AI Act i polska ustawa, konkurencja,
rynek, modele, sprzęt i na końcu szanse oraz ryzyka. Profile produktów są w [01-PROFILE.md](01-PROFILE.md),
wzorce techniczne w [03-WZORCE-TECHNICZNE.md](03-WZORCE-TECHNICZNE.md).

---

## Spis treści

- [Najkrótsza odpowiedź](#najkrótsza-odpowiedź)
- [1. Dlaczego nie do USA](#1-dlaczego-nie-do-usa)
- [2. Tajemnice zawodowe](#2-tajemnice-zawodowe)
- [3. AI Act i polska ustawa](#3-ai-act-i-polska-ustawa)
- [4. Konkurencja w UE i w Polsce](#4-konkurencja-w-ue-i-w-polsce)
- [5. Adopcja w Polsce](#5-adopcja-w-polsce)
- [6. Polskie i otwarte modele do pracy lokalnej](#6-polskie-i-otwarte-modele-do-pracy-lokalnej)
- [7. Sprzęt na biurko](#7-sprzęt-na-biurko)
- [8. Szanse produktowe, ryzyka i wejście na rynek](#8-szanse-produktowe-ryzyka-i-wejście-na-rynek)
- [Źródła tej części](#źródła-tej-części)

---

## Najkrótsza odpowiedź

- **Region UE dostawcy z USA to nie suwerenność.** CLOUD Act (18 U.S.C. § 2713) sięga po dane, które firma z USA
  „kontroluje", niezależnie od lokalizacji serwera. Microsoft France pod przysięgą: „Non, je ne peux pas le garantir".
- **Pudełko na biurku usuwa trzy problemy naraz:** brak podmiotu przetwarzającego (art. 28 RODO) dla części AI,
  brak transferu poza EOG (art. 44–49 RODO) i brak zależności od losu DPF (odwołanie C-703/25 P w toku).
- **Każdy zawód zaufania publicznego ma ustawową tajemnicę bez limitu czasu** (adwokat, radca, lekarz, doradca
  podatkowy, notariusz, biegły rewident), a złamanie jej może być przestępstwem (art. 266 § 1 KK). Samorządy
  dopisały już reguły dla AI: NRA § 23e (VI 2026), KIDP (I 2026), KEL art. 12 (od 1.01.2025).
- **AI Act na dziś:** art. 4 (kompetencje), art. 5 (zakazy), art. 50 (przejrzystość, od 2.08.2026). Wysokie ryzyko
  z załącznika III dopiero od 2.12.2027 — i tylko gdy funkcje wejdą w triaż, scoring albo wymiar sprawiedliwości.
- **Polska ustawa (Dz.U. 2026 poz. 1003)** daje od 28.10.2026 wiążącą opinię indywidualną KRiBSI za 150 zł;
  brak odpowiedzi w terminie = opinia zgodna z wnioskiem (art. 12 ust. 3).
- **Rynek jest „EU cloud", nie „na biurku".** Beck-Noxtua (590 zł netto/mies.), Noa Notes (199 zł + VAT, AWS i Azure),
  LEX Expert AI — wszystko w chmurze. Najbliżej „on-prem" jest Gaius-Lex, ale dla firm 20–99 prawników.
- **Modele są gotowe:** Qwen3.5/3.6-27B i Gemma-4-31B do rozumowania, Bielik v3 do polszczyzny, Whisper do mowy.
  Sprzęt: od Maca mini M5 Pro (8 499 zł) po ASUS GX10 (24 499 zł) dla kancelarii.

---

## 1. Dlaczego nie do USA

### CLOUD Act: liczy się kontrola, nie adres serwera

**18 U.S.C. § 2713** (CLOUD Act, 23.03.2018) każe dostawcy ujawnić dane „within such provider's possession, custody,
or control, regardless of whether such communication, record, or other information is located within or outside of
the United States" ([Cornell LII](https://www.law.cornell.edu/uscode/text/18/2713)).

- **EDPB i EDPS (wspólna odpowiedź dla komisji LIBE, 12.07.2019):** bez umowy międzynarodowej (np. MLAT) dostawca
  podlegający prawu UE „cannot legally base the disclosure and transfer of personal data to the US on such requests"
  ([PDF EDPB](https://www.edpb.europa.eu/sites/default/files/files/file2/edpb_edps_joint_response_us_cloudact_annex.pdf)).
  W praktyce: dostawca z USA może stanąć między nakazem amerykańskim a RODO, a **klient-profesjonalista tego konfliktu
  nie rozwiąże**.
- **Art. 48 RODO** mówi to samo od strony UE: wyrok lub decyzja organu państwa trzeciego jest uznawana tylko na
  podstawie umowy międzynarodowej ([RODO](https://eur-lex.europa.eu/eli/reg/2016/679/oj)).
- **Senat Francji, czerwiec 2025:** dyrektor prawny Microsoft France Anton Carniaux zapytany pod przysięgą, czy dane
  Francuzów nigdy nie trafią do władz USA bez zgody Francji, odpowiedział: **„Non, je ne peux pas le garantir"**
  — dodając, że dotąd się to nie zdarzyło ([The Register, 25.07.2025](https://www.theregister.com/2025/07/25/microsoft_admits_it_cannot_guarantee/)).
- **„European digital commitments" Microsoftu (30.04.2025):** obietnica zaskarżania nakazów i odszkodowań — to
  **zabezpieczenie umowne, nie immunitet prawny** ([blog Microsoftu](https://blogs.microsoft.com/on-the-issues/2025/04/30/european-digital-commitments/), *dane firmy*).

**Co to znaczy dla asystenta na biurku:** dane leżące wyłącznie na urządzeniu, które profesjonalista fizycznie
kontroluje, są osiągalne tylko polską procedurą, z jej gwarancjami tajemnicy. Sprzęt z USA (Mac, pudełko NVIDIA)
to nie usługa z USA — pod warunkiem, że telemetria jest wyłączona i opisana w dokumentacji.

### DPF: trzecie unieważnienie to realny scenariusz na 2027

| Data | Zdarzenie | Źródło |
|---|---|---|
| 10.07.2023 | Komisja przyjmuje decyzję o adekwatności dla EU–US Data Privacy Framework (DPF) | [Komisja Europejska](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/eu-us-data-transfers_en) |
| 3.09.2025 | Sąd UE oddala skargę Latombe (T-553/23), DPF utrzymany | [WilmerHale (blog)](https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20251201-european-court-of-justice-to-review-challenge-to-eu-us-data-privacy-framework) |
| 31.10.2025 | Odwołanie do TSUE, sprawa **C-703/25 P** — w toku, bez terminu rozprawy (VII–VIII 2026) | [secureprivacy (blog)](https://secureprivacy.ai/blog/is-the-eu-us-data-privacy-framework-at-risk-the-ftc-ruling-explained-2026) |
| 29.06.2026 | Sąd Najwyższy USA, Trump v. Slaughter: ochrona komisarzy FTC przed odwołaniem niekonstytucyjna; decyzja z 2023 opiera się na niezależności FTC | [Skadden (blog)](https://www.skadden.com/insights/publications/2026/07/supreme-court-decision-raises-new-questions) |
| wczesny–środek 2027 | Spodziewany wyrok TSUE (szacunek Skadden, VII 2026) | jw. |

- Microsoft miał zostać dopuszczony jako interwenient po stronie Komisji (4.06.2026) — **niezweryfikowane** (tylko
  nagłówek DataGuidance). Wygaśnięcie FISA 702 12.06.2026 — **niezweryfikowane** w źródle pierwotnym (tylko Wikipedia).
- Po Safe Harbor (2015) i Privacy Shield (2020) **każdy amerykański asystent w chmurze żyje na DPF albo SCC
  z oceną transferu**. Pudełko na biurku nie zależy od wyroku — to trwały argument sprzedażowy, nie chwilowy.

### RODO w praktyce asystenta na biurku

| Przepis | Co mówi | Co znaczy dla asystenta |
|---|---|---|
| Art. 9 ust. 1, 2 lit. h, ust. 3 RODO | Zakaz przetwarzania danych szczególnych kategorii (zdrowie i in.); wyjątek dla opieki zdrowotnej, gdy przetwarza osoba objęta tajemnicą | Scribe lekarski przetwarza dane zdrowotne legalnie tylko „pod odpowiedzialnością" lekarza — dostawca nie powinien ich widzieć |
| Art. 10 RODO | Dane o wyrokach i czynach zabronionych | Dotyczy obrońców w sprawach karnych — te same reguły co dla danych szczególnych w projekcie |
| Art. 28 RODO | Podmiot przetwarzający potrzebuje umowy z art. 28 ust. 3; podprzetwarzający — zgody | Każde API chmurowe to procesor. **Dostawca pudełka ze zdalnym dostępem serwisowym też staje się procesorem** — stąd „wsparcie bez dostępu" albo gotowa umowa powierzenia |
| Art. 32 RODO | Bezpieczeństwo przetwarzania | Szyfrowanie dysku, konta per użytkownik, logi, kopie zapasowe — lokalnie to obowiązek klienta i produktu |
| Art. 33–34 RODO | Zgłaszanie naruszeń | Kradzież pudełka to naruszenie ochrony danych (art. 4 pkt 12); zgłoszenie do UODO w 72 h (art. 33), chyba że ryzyko jest mało prawdopodobne. Brak szyfrowania zwykle oznacza też obowiązek zawiadomienia osób (art. 34); szyfrowanie może go zwolnić (art. 34 ust. 3 lit. a) |
| Art. 35 ust. 3 lit. b + motyw 91 RODO | DPIA dla dużej skali danych szczególnych; motyw 91: pojedynczy lekarz lub prawnik to nie „duża skala" | Solo-praktyka zwykle bez obowiązkowej DPIA; przychodnia i większa kancelaria — już tak. **Gotowy wzór DPIA to tani atut sprzedażowy** |
| Art. 44–49 RODO | Transfery poza EOG: adekwatność (art. 45), SCC (art. 46), wyjątki (art. 49) | Model lokalny = brak transferu dla części AI; chmura USA = DPF albo SCC + ocena transferu |
| Art. 48 RODO | Nakaz sądu państwa trzeciego tylko przez umowę międzynarodową | Patrz CLOUD Act wyżej — konflikt praw leży po stronie dostawcy |
| Art. 24 ust. 2–6 ustawy o prawach pacjenta (Dz.U. 2024 poz. 581) | Informatycy i procesor dokumentacji medycznej działają na upoważnienie i są związani tajemnicą, także po śmierci pacjenta | Firma serwisująca pudełko w gabinecie wchodzi w reżim tajemnicy lekarskiej |

Źródła: [RODO, EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [motyw 91](https://gdpr-info.eu/recitals/no-91/),
[ustawa o prawach pacjenta](https://api.sejm.gov.pl/eli/acts/DU/2024/581/text.pdf). Dodatkowo EDPB, opinia 28/2024
(17.12.2024): anonimowość modelu ocenia się indywidualnie, a uzasadniony interes (art. 6 ust. 1 lit. f) nie jest
podstawą „domyślną" ([CMS, blog](https://cms.law/en/int/legal-updates/edpb-opinion-28-2024-key-takeaways-on-processing-personal-data-in-the-context-of-ai-models)).

**Uwaga praktyczna:** lokalne logi czatu i indeks RAG to nadal dane osobowe. Produkt potrzebuje ustawień retencji,
szyfrowania i narzędzi do eksportu oraz usunięcia danych per klient.

### Region UE dostawcy z USA to nie suwerenność

| Oferta | Kto kontroluje | Co daje | Czego nie daje |
|---|---|---|---|
| Microsoft EU Data Boundary (ukończona 26.02.2025), Azure Poland Central | Microsoft (USA) | Dane klienta i dane wsparcia w UE/EFTA, poza „limited security instances" | Ochrony przed § 2713; modele Anthropic w Copilocie są wyłączone z EU Data Boundary |
| Microsoft Sovereign Cloud (16.06.2025): Data Guardian, klucze w HSM klienta, Azure Local, M365 Local | Microsoft (USA) | Dostęp tylko personelu z Europy, wersje odcięte od sieci | Zmiany jurysdykcji spółki matki |
| AWS European Sovereign Cloud (GA 15.01.2026, Brandenburgia) | Niemiecka GmbH Amazona | Obsługa „exclusively by EU residents", 90+ usług | Ogłoszenie nie wspomina o CLOUD Act |
| S3NS (Thales + Google), Bleu (FR), Delos (DE) | Spółki z operatorem z UE | S3NS PREMI3NS ma SecNumCloud 3.2, które celuje w ochronę przed „lois extraterritoriales" | To nadal technologia hiperskalera, cena i dostępność dla małej firmy |
| OVHcloud AI Endpoints, STACKIT, IONOS AI Model Hub | Firmy z UE | Brak spółki matki w USA; tanie API modeli otwartych | Dane i tak wychodzą z gabinetu do chmury |
| Pudełko na biurku | Profesjonalista | Brak procesora i transferu dla części AI | Wygody chmury: aktualizacji, skalowania, wsparcia — musisz je zbudować |

Źródła: [Microsoft EU Data Boundary](https://blogs.microsoft.com/on-the-issues/2025/02/26/microsoft-completes-landmark-eu-data-boundary-offering-enhanced-data-residency-and-transparency/),
[Microsoft Sovereign Cloud](https://blogs.microsoft.com/blog/2025/06/16/announcing-comprehensive-sovereign-solutions-empowering-european-organizations/),
[Copilot a EU Data Boundary](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy),
[AWS European Sovereign Cloud](https://press.aboutamazon.com/aws/2026/1/aws-launches-aws-european-sovereign-cloud-and-announces-expansion-across-europe),
[S3NS](https://www.s3ns.io/en), [ANSSI SecNumCloud](https://cyber.gouv.fr/enjeux-technologiques/cloud/),
[OVHcloud](https://www.ovhcloud.com/en/public-cloud/ai-endpoints/), [STACKIT](https://stackit.com/en/),
[IONOS](https://cloud.ionos.com/managed/ai-model-hub), [Azure regiony](https://learn.microsoft.com/en-us/azure/reliability/regions-list)
— strony firm, *dane firm*.

**CADA nazywa to wprost.** Projekt Cloud and AI Development Act (pakiet suwerenności technologicznej, 3.06.2026;
w X 2026 **wciąż projekt**) definiuje 4 poziomy suwerenności dla zamówień publicznych
([Komisja Europejska](https://digital-strategy.ec.europa.eu/en/policies/cloud-and-ai-development-act)):

- **L1** — dane przetwarzane i przechowywane w UE;
- **L2** — niezależność od państw trzecich i przejrzystość łańcucha dostaw;
- **L3** — własność i kontrola UE, kryteria obywatelstwa personelu;
- **L4** — pełna kontrola łańcucha dostaw, „no interference from a third country".

„Region UE" to L1. Asystent na otwartych wagach, działający na sprzęcie klienta, może opisywać się w kategoriach
L3/L4 (moja ocena — sprawdź ostateczny tekst CADA, gdy zostanie przyjęty). Polski przykład, że etykieta sprzedaje:
Operator Chmury Krajowej reklamuje „100% polskie rozwiązanie chmurowe", a jednocześnie odsprzedaje Gemini i Azure
OpenAI ([OChK](https://ochk.cloud/pl/), *dane firmy*).

---

## 2. Tajemnice zawodowe

Wspólny mianownik: **tajemnica ustawowa, bez limitu czasu, często bez możliwości zwolnienia, a do tego weryfikacja
wyniku AI przez człowieka.** To pozwala zbudować jeden rdzeń produktu i różne „pakiety zgodności" dla zawodów.

| Zawód | Podstawa | Co oznacza dla AI | Praktyczna reguła dla asystenta |
|---|---|---|---|
| Adwokat | Art. 6 ust. 1–4 Prawa o adwokaturze (Dz.U. 2024 poz. 1564): wszystko, o czym dowiedział się „w związku z udzielaniem pomocy prawnej"; bez limitu czasu; bez zwolnienia. Zbiór Zasad Etyki § 23e (NRA, 12–13.06.2026) i § 19 ust. 6 | § 23e: AI tylko pomocniczo; zakaz ujawniania informacji poufnych narzędziom bez należytej ochrony; osobista weryfikacja; na prośbę klienta wskazanie narzędzi; § 19 ust. 6: szczególna staranność przy przesyłaniu elektronicznym | Dane lokalnie i szyfrowane; tylko szkice, nic nie wychodzi automatycznie; cytaty do akt i przepisów; eksportowalna „notatka o użytych narzędziach" per sprawa |
| Radca prawny | Art. 3 ust. 3–6 ustawy o radcach prawnych (Dz.U. 2024 poz. 499) — jak u adwokatów. KIRP, „Rekomendacje dotyczące korzystania z AI" (13.05.2025), 22 punkty | Rekomendacje (współtworzone z Microsoft Polska i SK&S) dopuszczają chmurę z zabezpieczeniami umownymi; sprawdzanie miejsca przetwarzania, trenowania na danych, praw do wyników; informowanie klienta w sprawach wrażliwych | Nie sprzedawaj „chmura jest zakazana" — sprzedawaj prostotę i pewność; dołącz jednostronicową odpowiedź na listę KIRP |
| Lekarz, lekarz dentysta | Art. 40 ustawy o zawodach lekarza (Dz.U. 2026 poz. 37); art. 13–14 i 24 ustawy o prawach pacjenta; Kodeks Etyki Lekarskiej art. 12 (od 1.01.2025) | KEL art. 12: AI w diagnostyce, leczeniu i profilaktyce tylko gdy pacjent poinformowany, wyraził świadomą zgodę, algorytm dopuszczony do użytku medycznego i certyfikowany, a decyzja należy do lekarza | Zakres „dokumentacja i administracja" (transkrypcja, notatka, skierowanie); żadnych sugestii diagnozy; jasno opisane przeznaczenie; nagrania tylko za zgodą |
| Doradca podatkowy | Art. 37 ustawy o doradztwie podatkowym (Dz.U. 2026 poz. 1274): bez limitu czasu, obejmuje pracowników (ust. 3); ograniczone prawa z RODO (ust. 5–6). Zmiany zasad etyki KIDP (I 2026) | Wg prezesa KIDP: obowiązek zapewnienia poufności przy narzędziach AI i weryfikacji wyników przed użyciem, z odpowiedzialnością dyscyplinarną (numery paragrafów niezweryfikowane) | Każda liczba w odpowiedzi z odnośnikiem do linii w KSeF XML, JPK lub umowie; anonimizacja zbędna, bo nikt trzeci nie widzi danych |
| Notariusz | Art. 18 Prawa o notariacie (Dz.U. 2026 poz. 614): tajemnica okoliczności sprawy, trwa po odwołaniu; zwolnienie przez Ministra Sprawiedliwości | Brak znalezionych wytycznych KRN dotyczących AI (strona KRN niedostępna) | Tylko lokalnie; traktuj jak adwokata, dopóki KRN się nie wypowie |
| Biegły rewident | Art. 78 ustawy o biegłych rewidentach (Dz.U. 2025 poz. 1891): wszystkie informacje i dokumenty z usług atestacyjnych, bez limitu czasu, także dla osób z dostępem | Brak wytycznych PIBR dotyczących AI (strona PIBR, 11.10.2026) | Dokumentacja badania nie opuszcza firmy; ślad audytowy każdego zapytania |
| Wszyscy powyżej | Art. 266 § 1 Kodeksu karnego: ujawnienie lub wykorzystanie informacji „wbrew przepisom ustawy lub przyjętemu na siebie zobowiązaniu" — grzywna, ograniczenie wolności albo do 2 lat pozbawienia wolności | Osobista odpowiedzialność karna profesjonalisty, nie tylko dyscyplinarna | Argument „nic nie wychodzi z pokoju" trafia w realne ryzyko klienta |

Źródła: [Prawo o adwokaturze](https://api.sejm.gov.pl/eli/acts/DU/2024/1564/text.pdf),
[NRA o § 23e](https://www.adwokatura.pl/z-zycia-nra/zmiany-w-zbiorze-zasad-etyki-adwokackiej-naczelna-rada-adwokacka-przyjela-nowe-regulacje-dotyczace-korzystania-ze-sztucznej-inteligencji-w-wykonywaniu-zawodu-adwokata/),
[Rzeczpospolita, 16.06.2026](https://www.rp.pl/zawody-prawnicze/art44636171-nra-zmienila-kodeks-etyki-adwokat-moze-korzystac-z-ai-ale-tylko-pomocniczo),
[ustawa o radcach prawnych](https://api.sejm.gov.pl/eli/acts/DU/2024/499/text.pdf),
[KIRP rekomendacje](https://kirp.pl/rekomendacje-dotyczace-korzystania-z-ai/),
[prawo.pl o KIRP](https://www.prawo.pl/prawnicy-sady/rekomendacje-korzystania-z-ai-dla-radcow-prawnych,532905.html),
[ustawa o zawodach lekarza](https://api.sejm.gov.pl/eli/acts/DU/2026/37/text.pdf),
[KEL (PDF NIL)](https://nil.org.pl/uploaded_images/1723037323_kel-2305.pdf),
[ustawa o doradztwie podatkowym](https://api.sejm.gov.pl/eli/acts/DU/2026/1274/text.pdf),
[Rzeczpospolita o KIDP, 12.01.2026](https://www.rp.pl/zawody-prawnicze/art43622191-michna-doradcy-podatkowi-beda-bardziej-widoczni-w-terenie),
[Prawo o notariacie](https://api.sejm.gov.pl/eli/acts/DU/2026/614/text.pdf),
[ustawa o biegłych rewidentach](https://api.sejm.gov.pl/eli/acts/DU/2025/1891/text.pdf),
[Kodeks karny (ISAP)](https://isap.sejm.gov.pl/isap.nsf/DocDetails.xsp?id=WDU19970880553).

Trzy uwagi, które łatwo przeoczyć:

- **Wyjątki od tajemnicy są wąskie i nie dotyczą AI.** U adwokatów, radców, doradców i notariuszy to głównie
  przepisy AML i raportowanie schematów podatkowych (MDR). „Wygoda" nie jest wyjątkiem.
- **KEL art. 12 krytykowano** jako niepraktyczny (zgoda pacjenta dodana tuż przed głosowaniem); Ligia Kornowska
  proponuje czytać go tylko dla AI istotnie wpływającej na leczenie ([blog OSOZ](https://blog.osoz.pl/nowy-kodeks-etyki-lekarskiej-z-niejasnym-zapisem-o-ai)).
  W źródłach z 11.10.2026 brak zmiany KEL i brak stanowiska NIL o scribe'ach. Bezpiecznie: zostań przy dokumentacji.
- **Data wejścia w życie zmian NRA nie padła w źródłach**, a praktyk z Instytutu Księgowości i Doradztwa Podatkowego
  ostrzega, że wklejanie opinii i umów do publicznych narzędzi AI może być ujawnieniem tajemnicy
  ([IKiDP, 9.08.2026](https://ikidp.pl/blog/ai-tajemnica-zawodowa-doradcy-podatkowego/)).

**Halucynacje to nie teoria.** Baza Damiena Charlotina liczy **2 184 sprawy sądowe z halucynacjami AI** (stan
10.10.2026), w tym **6 w Polsce**; 864 z udziałem prawników ([baza](https://www.damiencharlotin.com/hallucinations/)).
Dlatego § 23e i zasady KIDP mówią o osobistej weryfikacji — a produkt musi ją ułatwiać (cytat → źródło w ISAP lub SAOS).

---

## 3. AI Act i polska ustawa

### Kalendarz AI Act po Omnibusie

AI Act to rozporządzenie (UE) 2024/1689; terminy zmienił **AI Omnibus — rozporządzenie (UE) 2026/1744**, opublikowane
w Dz.Urz. UE 24.07.2026, w mocy od 27.07.2026 ([EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601744),
[FPF](https://fpf.org/blog/the-ai-act-implementation-timeline-what-changes-under-the-ai-omnibus/),
[Lewis Silkin, 27.07.2026](https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo)).

| Od kiedy | Co obowiązuje | Czy dotyczy asystenta dla profesjonalistów |
|---|---|---|
| 2.02.2025 | Zakazane praktyki (art. 5), kompetencje w zakresie AI (art. 4) | Tak — art. 4 po Omnibusie złagodzony: „support the development of" kompetencji |
| 2.08.2025 | Obowiązki dostawców modeli ogólnego przeznaczenia GPAI (art. 53–55), kary | Dla twórcy modelu (np. SpeakLeash, Mistral), nie dla integratora |
| 2.08.2026 | Ogólne stosowanie, w tym przejrzystość z art. 50 | **Tak** — art. 50 ust. 1 w czacie dla klienta lub pacjenta |
| 2.12.2026 | Nowy zakaz (generowanie CSAM i intymnych obrazów bez zgody); art. 50 ust. 2 dla systemów już na rynku | Art. 50 ust. 2 tylko przy generowaniu treści syntetycznych |
| 2.08.2027 | Modele GPAI sprzed 2.08.2025; piaskownica w każdym państwie | Pośrednio |
| 2.12.2027 | Wysokie ryzyko z **załącznika III** | Tylko jeśli funkcje w nie wejdą |
| 2.08.2028 | Wysokie ryzyko z **załącznika I** (np. wyroby medyczne) | Gdy oprogramowanie jest wyrobem medycznym (MDR) |

Inne zmiany Omnibusa: nowy **art. 4a** (dane szczególne kategorii tylko gdy „strictly necessary" do wykrywania
i korygowania stronniczości) i uproszczenia MŚP rozszerzone na „small mid-caps" (do 750 osób, do 150 mln EUR obrotu).

### Co faktycznie dotyczy asystenta

- **Role.** Ty jako twórca jesteś **dostawcą systemu AI** (art. 3 pkt 3), kancelaria lub przychodnia —
  **podmiotem stosującym** (art. 3 pkt 4). Użytek czysto osobisty jest poza rozporządzeniem (art. 2 ust. 10)
  ([AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)).
- **Art. 50.** Ust. 1: człowiek ma wiedzieć, że rozmawia z AI (czat dla klientów, recepcja). Ust. 4: oznaczanie
  tekstów publikowanych w sprawach publicznych **nie dotyczy** treści po ludzkiej redakcji z odpowiedzialnością
  redakcyjną — wewnętrzny szkic pisma, który prawnik sprawdza i podpisuje, jest w praktyce poza ust. 4
  ([art. 50](https://artificialintelligenceact.eu/article/50/)).
- **Załącznik III — wysokie ryzyko tylko gdy…**
  - pkt 8 lit. a: AI używana **przez organ sądowy lub w jego imieniu** albo w ADR — sądy i arbitrzy, nie kancelarie;
  - pkt 5: kwalifikacja do świadczeń, scoring kredytowy, wycena ubezpieczeń zdrowotnych i na życie,
    **triaż pacjentów w nagłych wypadkach**;
  - pkt 4: zatrudnienie i HR (selekcja CV)
  ([załącznik III](https://artificialintelligenceact.eu/annex/3/)).
- **Art. 6 ust. 3:** system z załącznika III nie jest wysokiego ryzyka, gdy wykonuje wąskie zadanie proceduralne,
  poprawia wynik zakończonej pracy człowieka, wykrywa wzorce bez zastępowania oceny albo wykonuje zadanie
  przygotowawcze. **Profilowanie osób zawsze jest wysokiego ryzyka** ([art. 6](https://artificialintelligenceact.eu/article/6/)).
- **Medycyna:** oprogramowanie dostarczające informacji do decyzji diagnostycznych lub terapeutycznych to co najmniej
  klasa IIa wg MDR (załącznik VIII, reguła 11), a więc wysokie ryzyko od 2.08.2028
  ([MDR](https://eur-lex.europa.eu/eli/reg/2017/745/oj)). Scribe bez celu diagnostycznego zwykle wyrobem nie jest —
  decyduje deklarowane przeznaczenie.
- **Fine-tuning modelu.** Integrator staje się dostawcą GPAI tylko przy „significant modifications"
  ([wytyczne Komisji](https://digital-strategy.ec.europa.eu/en/policies/guidelines-gpai-providers)). Lekki LoRA na Bieliku
  czy Qwenie prawie na pewno tego nie przekracza (próg obliczeniowy — niezweryfikowany).

**Reguła produktowa:** bez automatycznego triażu, bez „sugestii diagnozy", bez scoringu klientów, bez modułu
selekcji CV. Jeśli kiedyś — to jako osobny produkt z osobnym przeznaczeniem. Do tego notka z art. 50 ust. 1 w każdym
czacie dla klientów i krótki pakiet szkoleniowy z art. 4 dla personelu.

### Polska ustawa o systemach sztucznej inteligencji

**Ustawa z dnia 3 lipca 2026 r. o systemach sztucznej inteligencji, Dz.U. 2026 poz. 1003** (ogłoszona 27.07.2026)
([tekst, api.sejm.gov.pl](https://api.sejm.gov.pl/eli/acts/DU/2026/1003/text.pdf)):

| Przepis | Treść | Znaczenie dla dostawcy asystenta |
|---|---|---|
| Art. 5 | **KRiBSI** (Komisja Rozwoju i Bezpieczeństwa Sztucznej Inteligencji) — organ nadzoru rynku z art. 70 ust. 1 AI Act i pojedynczy punkt kontaktowy | Tu pytasz i tu ktoś cię kontroluje |
| Art. 9 | O opinię może wystąpić podmiot objęty AI Act **albo planujący nim zostać**; stan faktyczny lub zdarzenie przyszłe; ten sam podmiot ponownie najwcześniej po 30 dniach (ust. 5) | Możesz zapytać przed startem sprzedaży |
| Art. 11 | Opłata **150 zł**; zwrot m.in. gdy Komisja nie wyda opinii w terminie | Koszt pomijalny |
| Art. 12 | Opinia w 30 dni, w sprawach szczególnie skomplikowanych 60 dni (ust. 1); **brak opinii w terminie = opinia zgodna ze stanowiskiem wnioskodawcy** (ust. 3) | Milcząca zgoda działa na twoją korzyść |
| Art. 13 | Opinia wiąże KRiBSI oraz organy i jednostki, o których mowa w art. 12 ust. 2 (te, od których Komisja zasięgnęła opinii) — dla wskazanego stanu faktycznego (ust. 1); nie można jej zmienić, gdy wystąpiły nieodwracalne skutki (ust. 2). Ustawa nic nie mówi o związaniu sądów ani izb zawodowych | Dokument do pokazania izbie i klientowi |
| Art. 15 | Komisja może zmienić lub uchylić opinię m.in. po zmianie prawa lub wytycznych UE | Opinia nie jest wieczna — śledź zmiany |
| Art. 127 | Wejście w życie 14 dni po ogłoszeniu (**11.08.2026**); art. 8–18 i rozdz. 3–5, 8, 9 po 3 miesiącach (**28.10.2026**) | Opinie indywidualne od 28.10.2026 |

Daty potwierdzają też [gdpr.pl](https://gdpr.pl/ustawa-o-systemach-sztucznej-inteligencji-weszla-w-zycie) i
[infor.pl](https://www.infor.pl/prawo/nowosci-prawne/7668177,ustawa-o-systemach-sztucznej-inteligencji-od-28-pazdziernika-2026-obowiazki-firm-i-kary-co-to-jest-kribsi.html).
Ustawa przewiduje też piaskownicę regulacyjną (art. 91) i kary według rozdziału XII AI Act (art. 104).

**Pytanie, które warto zadać KRiBSI po 28.10.2026** (przykład, nie wzór wniosku): „Czy lokalny asystent do
redagowania, streszczania i transkrypcji dla kancelarii i gabinetów, bez triażu, scoringu i sugestii diagnoz, jest poza załącznikiem III?" (osobny wniosek: czy jest objęty art. 6 ust. 3 — jedno zagadnienie na wniosek, art. 9 ust. 3 pkt 1) Za 150 zł, z milczącą zgodą po 30–60 dniach, to najtańszy
dokument redukujący ryzyko, jaki można pokazać ostrożnej izbie.

### Jeśli sprzedajesz asystenta: PLD i CRA

| Akt | Od kiedy | Co znaczy dla sprzedawcy pudełka |
|---|---|---|
| Dyrektywa (UE) 2024/2853 o odpowiedzialności za produkty wadliwe (PLD) | Produkty wprowadzone od **9.12.2026** (też termin transpozycji) | Obejmuje „all types of software … including … AI-systems"; producent odpowiada za wady, także z aktualizacji i z zachowania uczenia maszynowego. Sprawdź polską transpozycję; nie sprawdzono, czy utrata danych zawodowych to szkoda objęta dyrektywą |
| Rozporządzenie (UE) 2024/2847, Cyber Resilience Act (CRA) | W mocy od 10.12.2024; **zgłaszanie od 11.09.2026**; główne obowiązki od **11.12.2027** | Produkt z elementami cyfrowymi: oznakowanie CE, aktualizacje bezpieczeństwa przez cały cykl życia, obsługa podatności, SBOM. Już dziś: proces zgłaszania aktywnie wykorzystywanych podatności |

Źródła: [Komisja — PLD](https://single-market-economy.ec.europa.eu/single-market/goods/free-movement-sectors/liability-defective-products_en),
[Komisja — CRA](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act).

**Wniosek:** sprzedając pudełko z modelem, sprzedajesz **produkt**, nie tylko usługę. Potrzebujesz: jasnego opisu
przeznaczenia („pomoc w redagowaniu i dokumentacji, wynik weryfikuje profesjonalista"), ograniczenia odpowiedzialności
w umowie B2B, ubezpieczenia OC, podpisanych aktualizacji offline i listy komponentów (SBOM). Bezpieczeństwo agenta
opisuje [kurs, część 16](../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md).

### UODO: listy kontrolne i lekcja MyDr

- **6.08.2026 UODO opublikował listy „pytań inicjalnych"**: „Zanim wdrożysz narzędzie AI, sprawdź czy jest ono
  zgodne z zasadami RODO" — cztery wersje: dla twórców AI, dla MŚP korzystających z gotowych narzędzi, dla sektora
  publicznego i rozszerzona (RODO + AI Act). UODO zaznacza, że nie zastępują analizy ryzyka ani DPIA; konsultacje
  trwały do 30.09.2026 ([UODO](https://uodo.gov.pl/pl/138/4533)). **Dołącz do produktu gotowe odpowiedzi na wersję
  dla MŚP** — klient oszczędza dzień pracy.
- **13.08.2026 UODO wszczął kontrolę MyDr** — chmurowego oprogramowania medycznego — po naruszeniu danych pacjentów;
  potencjalnie dotkniętych około **12 000 podmiotów leczniczych** ([UODO](https://uodo.gov.pl/pl/138/4540)).
  Lekcja: jedna chmura SaaS = jeden punkt awarii dla tysięcy gabinetów. Rozproszone dane na biurkach zmniejszają
  skalę jednego wycieku — ale **przenoszą odpowiedzialność za zabezpieczenia na gabinet i na ciebie**.
- UODO przypomina, że administratorzy mają „regularnie mierzyć i testować wdrożone środki bezpieczeństwa"
  (26.06.2026, [UODO](https://uodo.gov.pl/pl/138/4449)).

---

## 4. Konkurencja w UE i w Polsce

### Europejskie oferty „suwerenne" i prywatne

| Produkt | Dla kogo | Gdzie dane | Cena (z datą) | Lekcja |
|---|---|---|---|---|
| [Noxtua](01-PROFILE.md#14-noxtua) (DE, C.H.Beck) | Prawnicy, działy prawne, administracja w DACH i UE; 30 000+ użytkowników (IX 2026, *dane firmy*) | Niemcy (Deutsche Telekom, IONOS) i Szwajcaria; tier „Athena" na modelach otwartych, „Minerva" na modelach frontier w europejskim układzie; brak wersji na biurko | Abonament niepubliczny; seria B ok. 81 mln EUR (IV 2025), seria C 100+ mln EUR (23.09.2026) | Dwa tiery (suwerenny i frontier) do wyboru per sprawa; ustawa o tajemnicy na stronie bezpieczeństwa; treści wydawcy jako fosa |
| Mistral Vibe (dawniej Le Chat, zmiana 28–29.05.2026) | Firmy i osoby w UE | UE domyślnie; Enterprise self-hosted lub on-prem | Pro 14,99 EUR, Team 24,99 EUR/os./mies. (min. 50 EUR), bez VAT (X 2026) | Główny konkurent „UE, ale chmura"; jego małe modele Apache-2.0 (Ministral 3) to kandydaci na silnik pudełka |
| Proton Lumo (od 23.07.2025; 2.0 od 1.07.2026) | Konsumenci dbający o prywatność | Niemcy i Norwegia; historia z szyfrowaniem zero-access, ale serwer GPU widzi prompt w trakcie odpowiedzi | Lumo Plus 12,99 USD/mies. lub 9,99 USD rocznie | Wzorzec „privacy AI" dla konsumenta — nadal zaufanie do operatora; modele Qwen 3.5, GLM 5.3, Apertus 1.5 |
| Nextcloud Assistant (Nextcloud 36) | Firmy z własnym Nextcloudem | Serwer klienta: llm2, stt_whisper2, Context Chat (RAG), Context Agent z MCP | Cena wsparcia: nie sprawdzono | Najbliższy otwarty odpowiednik; domyślne modele 9B i mniejsze — miejsce na lepszy polski na mocniejszym sprzęcie |
| Cohere North 2 + Aleph Alpha | Banki, sektor publiczny, telekomy | On-prem, air-gapped, VPC, hybryda; Cohere ma działać na STACKIT | Licencje niepubliczne; ARR Cohere 240 mln USD (2025); łączna wycena ok. 20 mld USD, 600 mln USD od Schwarz Group (IV 2026) | Regulowani klienci płacą za air-gap — ale w dużych kontraktach; segment małych biur zostaje wolny |
| DeepL Pro i DeepL Agent | Tłumaczenia w firmach; 200 000+ klientów biznesowych (*dane firmy*) | Europejskie centra danych ISO 27001, teksty usuwane | Individual 7,49 EUR, Team 24,99 EUR, Business 49,99 EUR/os./mies. (rocznie, X 2026) | Tłumaczenie umów to częsty wyciek danych z biurka — lokalny tłumacz w asystencie go zamyka |
| Langdock | Firmy chcące wielu modeli w jednym miejscu | Hosting UE (wg recenzji Azure Frankfurt), opcja self-hosted; inferencja u dostawców z USA | Business 25 EUR/os./mies. (X 2026) | „Nakładka UE" na modele z USA — dane w UE, ale wnioskowanie nie |
| Heidi Health (AU, silna w UK/UE) | Lekarze, praktyki, NHS | Dane z UE w UE/EOG; „No audio recordings are ever saved" | Clinician ok. 150 USD/os./mies. (USA, 2026) | Rezydencja + brak nagrań to sufit prywatności rynku scribe'ów w 2026 |
| Nabla (FR) | Systemy szpitalne, głównie USA | Audio przetwarzane w przeglądarce, nie zapisywane na serwerach; transkrypty 14 dni domyślnie | Ceny niepubliczne; 120 mln USD łącznie (VI 2025) | Minimalizacja danych w architekturze to argument, który da się pokazać |
| Microsoft 365 Copilot (punkt odniesienia z USA) | Każda firma na M365; 30+ mln płatnych stanowisk (FY2026, *dane firmy*) | EU Data Boundary, poza modelami Anthropic | Business 18 USD/os./mies. rocznie (obniżka z 21 USD do XII 2026) | Na cenie za stanowisko nie wygrasz — wygrywasz tajemnicą, polskim prawem i pracą offline |

Źródła: [Noxtua](https://www.noxtua.com/), [Noxtua security](https://www.noxtua.com/security),
[Noxtua seria C](https://www.noxtua.com/news/press-releases/series-c),
[TechCrunch o Noxtua](https://techcrunch.com/2025/04/22/noxtua-raises-92m-for-its-sovereign-ai-tuned-for-the-german-legal-system/),
[Mistral cennik](https://mistral.ai/fr/pricing), [heise o Vibe](https://heise.de/-11311685),
[Proton Lumo cennik](https://proton.me/lumo/pricing), [Lumo prywatność](https://proton.me/support/lumo-privacy),
[Help Net Security o Lumo 2.0](https://www.helpnetsecurity.com/2026/07/01/proton-lumo-2-0-ai/),
[Nextcloud AI](https://docs.nextcloud.com/server/latest/admin_manual/ai/index.html),
[Nextcloud llm2](https://docs.nextcloud.com/server/latest/admin_manual/ai/app_llm2.html),
[Cohere North 2](https://cohere.com/blog/introducing-north-2),
[TechCrunch o Cohere](https://techcrunch.com/2026/02/13/coheres-240m-year-sets-stage-for-ipo/),
[TechCrunch o Aleph Alpha](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/),
[DeepL Pro](https://www.deepl.com/en/pro), [Langdock](https://www.langdock.com/pricing),
[Heidi safety](https://heidihealth.com/safety), [Heidi GDPR](https://www.heidihealth.com/au/compliance/gdpr),
[Heidi plany](https://support.heidihealth.com/en/articles/8885129-which-heidi-plan-is-right-for-you),
[Nabla (recenzja konkurenta)](https://www.commure.com/blog-scribe/nabla-ai-review),
[STAT o Nabla](https://www.statnews.com/2025/06/17/nabla-raises-70-million-ambient-market-heats-up/),
[Copilot cennik](https://www.microsoft.com/en-us/microsoft-365-copilot/pricing),
[Microsoft FY26 Q4](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast).
Różnica w kwocie serii B Noxtua: ok. 80,7 mln EUR (CMS) i 92,2 mln USD / 81,2 mln EUR (TechCrunch) — podaję zaokrąglenie.

Więcej o liderach z USA: [Harvey](01-PROFILE.md#4-harvey) (post-trening otwartego modelu, Tenet) i
[Abridge](01-PROFILE.md#3-abridge) (scribe medyczny).

### Rynek polski

| Produkt | Dla kogo | Gdzie dane | Cena (z datą) | Lekcja |
|---|---|---|---|---|
| Beck-Noxtua (C.H.Beck + Noxtua) | Prawnicy z Legalis | „Niezależna, europejska infrastruktura" — wg wydania czeskiego IONOS i Open Telekom Cloud, BSI C5 | **590 zł netto/mies./użytkownik**, bez limitu tokenów, wymaga Legalis Silver+ (11.10.2026) | Kotwica cenowa dla prawników; fosą są treści Legalis, nie lokalność |
| LEX Expert AI (Wolters Kluwer) | Abonenci LEX; od 14.07.2026 także finanse, podatki, HR, compliance | Serwery w UE, SOC 2, „nie do publicznych modeli"; model nieujawniony | Niepubliczna (start 19.11.2025) | Polscy prawnicy oczekują odnośnika do fragmentu źródła przy każdej odpowiedzi |
| LexisNexis Protégé (PL/CEE) | Kancelarie i doradcy podatkowi | „Prywatna przestrzeń robocza … zgodnie z europejskimi standardami" | Tylko demo, brak ceny (11.10.2026) | Trzeci międzynarodowy gracz w chmurze |
| Gaius-Lex („Gaius Vault") | Kancelarie 20–99 prawników (PL, CZ, AT, DE) | SaaS w EOG, hybryda albo „pełne wdrożenie on-premise" | Brak ceny; seed ok. 502 tys. USD (VIII 2025, agregator), 6 osób | **Najbliższy polski odpowiednik „dane nie wychodzą z biura"** — przestudiuj pozycjonowanie |
| LEX AI (LEX Secure AI, Navimor) | Konsumenci i małe firmy | Wg App Store serwery tylko w Polsce; „zamknięty model" z Politechniką Gdańską | Standard 49 zł, Premium 120 zł, PRO MAX 489 zł/mies.; podpisana opinia ok. 320–380 zł (v1.4.0, 21.09.2026) | Drabina cen w złotych dla klienta indywidualnego |
| Noa Notes (Docplanner / ZnanyLekarz) | Lekarze prywatni; „ponad 13 000 specjalistów" (*dane firmy*) | Chmura AWS i Microsoft Azure | **199 zł/mies. + VAT**, bez limitu notatek (X 2026) | Kotwica cenowa scribe'a; wtyczka Chrome jako integracja z dowolnym EDM; zależność od hiperskalerów z USA to luka |
| Medidesk | Placówki: asystent menedżera, chatbot, voicebot | EOG, bez trenowania | Nie sprawdzono | Rynek obsługi pacjenta też idzie w AI |
| Comarch ChatERP (Optima, beta) | Użytkownicy Comarch ERP | Na PLLuM, który „może być hostowany lokalnie"; dane trafiają do „podwykonawców technologicznych" | Nie podano | Polski model w komercyjnym produkcie — ale beta zabrania danych osobowych i tajemnic w pytaniach |
| Comarch AI | Firmy | SaaS, centrum danych Comarch w Krakowie | Nie podano | „Dane nie opuszczają infrastruktury" jako hasło |
| wFirma | Ok. 4 000 biur rachunkowych, 130k+ firm (*dane firmy*) | Chmura wFirma | Funkcje AI bez dopłaty | AI staje się dodatkiem do pakietu — trudno sprzedać to samo osobno |
| inFakt | Małe firmy | Podłączenie danych księgowych do Claude lub ChatGPT (USA) | Nie podano | Dostawcy wysyłają dane do modeli z USA — luka dla biur z tajemnicą |
| SentiOne | Banki, windykacja (Alior Bank, Kruk) | On-prem albo chmura | Nie podano | Polska tradycja on-prem istnieje w botach |

Źródła: [Beck-Noxtua](https://www.beck-noxtua.pl/), [Noxtua PL](https://www.noxtua.com/news/press-releases/beck-noxtua-poland),
[Noxtua CZ](https://www.noxtua.com/news/press-releases/beck-noxtua-for-the-czech-republic),
[prawo.pl o LEX Expert AI](https://www.prawo.pl/prawnicy-sady/lex-expert-ai-nowym-narzedziem-dla-prawnikow,535918.html),
[Wolters Kluwer, 14.07.2026](https://www.wolterskluwer.com/pl-pl/news/lex-expert-ai-wspiera-specjalistow-ktorzy-nie-sa-prawnikami),
[Protégé Polska](https://www.lexisnexis.com/de-at/cee/protege-polska), [Gaius-Lex](https://gaius-lex.pl/),
[Legal Technology Hub](https://www.legaltechnologyhub.com/vendors/gaius-lex/),
[Signalbase](https://www.trysignalbase.com/news/funding/gaius-lex-secures-5),
[LEX AI w App Store](https://apps.apple.com/pl/app/lex-ai/id6748342467?l=pl), [lexai.pl](https://lexai.pl/),
[Noa cennik](https://www.noa.ai/pl/cennik), [Noa Notes](https://noa.ai/pl/noa-notes),
[Medidesk](https://www.medidesk.com/), [Comarch ChatERP](https://www.comarch.pl/erp/asystent-ai/),
[Comarch AI](https://www.comarch.ai/), [wFirma](https://wfirma.pl/), [inFakt](https://www.infakt.pl/),
[SentiOne](https://sentione.com/) — strony firm, *dane firm*.

**Kontekst KSeF:** e-faktury są obowiązkowe od 1.02.2026 (sprzedaż za 2024 powyżej 200 mln zł) i od 1.04.2026 dla
pozostałych; do końca 2026 faktury do 10 000 zł miesięcznie mogą być poza KSeF (ustawa z 5.08.2025, Dz.U. 2025 poz. 1203)
([KSeF](https://ksef.podatki.gov.pl/informacje-ogolne-ksef-20/podstawy-prawne-oraz-kluczowe-terminy/)). Każda firma ma
więc ustrukturyzowane XML-e faktur — idealny materiał dla lokalnego modelu.

**Państwo też omija dane osobowe.** Asystent mObywatela na PLLuM (dla wszystkich od 31.12.2025) celowo nie ma
dostępu do PESEL, recept ani mandatów, a użytkownicy mają nie wpisywać danych wrażliwych
([iMagazine](https://imagazine.pl/2026/01/02/mobywatel-wchodzi-w-2026-rok-z-polskim-ai/)). To dokładnie luka, którą
wypełnia asystent na biurku.

**Wniosek z obu tabel:** w 11.10.2026 nikt z wymienionych nie sprzedaje **gotowego pudełka dla biura 1–10 osób**.
To wynik negatywnego wyszukiwania, nie dowód, że takiego produktu nie ma.

---

## 5. Adopcja w Polsce

| Wskaźnik | Polska | UE | Źródło |
|---|---|---|---|
| Firmy 10+ osób używające AI (2025) | 8,36% (Eurostat); 8,7% (GUS, wzrost z 5,9% w 2024) | 19,95% (wzrost z 13,5%); Dania 42,03% | [Eurostat](https://ec.europa.eu/eurostat/statistics-explained/index.php/Use_of_artificial_intelligence_in_enterprises), [GUS](https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultaktualnosci/5497/1/19/1/spoleczenstwo_informacyjne_w_polsce_2025.pdf) |
| Działalność profesjonalna, naukowa i techniczna (2025) | **23,2%** (wzrost z 14,4%) | **40,43%** | jw. |
| Firmy według wielkości (2025) | duże 42,0%, średnie 15,6%, małe 6,1% | duże 55,03%, średnie 30,36%, małe 17% | jw. |
| Generowanie tekstu (najczęstszy typ AI) | 5,3% firm (z 2,4%) | — | GUS |
| Skąd AI: gotowe / adaptacja open source / własne | 6,4% / 2,4% / 2,3% | — | GUS |
| Bariery wśród firm, które rozważały AI | — | brak wiedzy 70,89%, niejasne skutki prawne 52,52%, ochrona danych 48,83% | Eurostat |
| Niekorzystający, którzy nie wdrożą AI „dopóki nie muszą" | 77% (ok. co piąty wskazuje koszt) | — | [PIE, 24.09.2025](https://pie.net.pl/wp-content/uploads/2025/09/2025-09-22_Z-AI-korzysta-mniej-niz-co-szosta-firma-w-Polsce-a-pozostale-nie-planuja-jej-wdrazac-1.pdf) |
| Prawnicy używający co najmniej jednego narzędzia AI codziennie | ponad 92% (próba 810 osób z USA, Chin i 9 krajów Europy, w tym Polski; tylko 34% czuje się gotowych na regulacje) | — | [Future Ready Lawyer 2026 (prawo.pl)](https://www.prawo.pl/prawnicy-sady/prawnicy-na-co-dzien-korzystaja-z-ai-a-ai-zmienia-model-ich-zawodu,1540345.html) |

**Wielkość szansy:**

- **Lekarze:** rejestr NIL (30.06.2026) — **164 456 lekarzy i 42 903 lekarzy dentystów** wykonujących zawód, razem
  **207 821** ([NIL](https://nil.org.pl/uploaded_files/1783510889_30062026-zestawienie-nr-1.pdf)). NIL prowadzi szkolenia
  z AI dla lekarzy (29.09 i 20.10.2026); ankiety NIL o AI nie znaleziono.
- **Prawnicy i doradcy:** liczby adwokatów i radców prawnych nie zostały zweryfikowane w tym przeglądzie; polskich
  ankiet o AI w zawodach prawniczych, medycznych i podatkowych nie znaleziono (NRA, KRRP, NIL, KIDP, SKwP).
- **Czytanie liczb:** polskie firmy profesjonalne są około dwa lata za UE, ale w jeden rok przybyło 8,8 pkt proc.
  Dwie z trzech głównych barier w UE (skutki prawne, ochrona danych) to dokładnie to, co rozwiązuje asystent
  na biurku. Trzecia (brak wiedzy) mówi: **sprzedawaj wdrożenie i szkolenie, nie samo oprogramowanie.**
- **„Shadow AI":** PIE zauważa, że pracownicy sami korzystają z darmowych narzędzi, więc realne użycie jest wyższe
  niż raportowane. Dla kancelarii to ryzyko tajemnicy — zatwierdzony lokalny asystent je zastępuje.

---

## 6. Polskie i otwarte modele do pracy lokalnej

### Bielik v3 — polszczyzna na licencji Apache-2.0

| Model | Rozmiar | Licencja | Co wyróżnia |
|---|---|---|---|
| Bielik-11B-v3.0-Instruct (30.12.2025) | 11,2 mld, 50 warstw (z Mistral-7B-v0.2 przez dokładanie warstw) | Apache-2.0 | 32 języki z naciskiem na polski; kontekst 32 768 tokenów, 131 072 z YaRN |
| Bielik-Minitron-7B-v3.0 (III 2026) | 7,35 mld (−33,4% przez przycinanie i destylację) | Apache-2.0 | Ok. 90% jakości 11B, do ok. 50% szybciej; oficjalne GGUF i FP8 |
| Bielik-PL-11B-v3.0 i PL-Minitron-7B (IV 2026) | 11B / 7B | Apache-2.0 | Tokenizer **APT4** dla polszczyzny: mniej tokenów na słowo, więcej tekstu w kontekście |
| Bielik DFlash (24.06.2026) | ok. 1 mld | Apache-2.0 | Małe modele szkicujące do dekodowania spekulatywnego w vLLM i SGLang |
| Bielik-Guard „Sójka" v1.1 | 0,5 mld | Apache-2.0 | Polski klasyfikator bezpieczeństwa, 5 kategorii szkód, precyzja 75,28% przy 0,73% fałszywych alarmów |

Źródła: [Bielik-11B-v3.0](https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct),
[arXiv 2601.11579](https://arxiv.org/abs/2601.11579),
[Minitron-7B](https://huggingface.co/speakleash/Bielik-Minitron-7B-v3.0-Instruct),
[Bielik-PL-11B](https://huggingface.co/speakleash/Bielik-PL-11B-v3.0-Instruct), [arXiv 2604.10799](https://arxiv.org/abs/2604.10799),
[DFlash](https://huggingface.co/speakleash/Bielik-11B-v3.0-DFlash), [Bielik-Guard](https://huggingface.co/speakleash/Bielik-Guard-0.5B-v1.1).
Bielik v3.1 (50 języków) zapowiadano na czerwiec 2026 — w 11.10.2026 na Hugging Face są tylko modele v3.0.
Bielik deklaruje 4,7 mln+ pobrań (*dane projektu*), a w Ollamie wersja 11B ma 13,5 tys. pobrań (11.10.2026)
([bielik.ai](https://bielik.ai/), [Ollama](https://ollama.com/SpeakLeash)). **Brak umowy wsparcia i SLA** — wsparcie
musisz dać sam.

### PLLuM — uwaga na licencje

- **1. generacja (2412):** 12B na Mistral-Nemo i 8x7B na Mixtralu — Apache-2.0; warianty „-nc" — CC-BY-NC-4.0
  (niekomercyjne); Llama-PLLuM 8B i 70B — licencja Llama 3.1.
- **HIVE AI, VII 2025:** PLLuM-12B-nc-250715 na własnych licencjach pllum-1.x — **niekomercyjne**.
- **2. generacja (2512):** PLLuM-4B (na Gemma-3-4B) i PLLuM-12B — Apache-2.0 wg kart; ale 4B dziedziczy warunki Gemmy.
- **Paradoks:** komercyjny PLLuM-12B-chat-2512 ma PLCC 41,17, a niekomercyjny 250715 — 69,67. Najlepsza polszczyzna
  PLLuM jest na licencji, której nie użyjesz w płatnym produkcie.

Źródła: [PLLuM-12B-chat](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-chat),
[pllum-12b-nc-chat-250715](https://huggingface.co/CYFRAGOVPL/pllum-12b-nc-chat-250715),
[PLLuM-12B-instruct-2512](https://huggingface.co/CYFRAGOVPL/PLLuM-12B-instruct-2512),
[PLLuM-4B-instruct-2512](https://huggingface.co/CYFRAGOVPL/PLLuM-4B-instruct-2512).

### Kto wygrywa po polsku (benchmarki z datą)

| Model | CPTUB (1–5; rozumienie złożonego tekstu; dane 11.08.2026) | PLCC (kultura i język; dane 8.10.2026) | Licencja |
|---|---|---|---|
| Qwen3.6-27B (reasoning) | 4,41 | — | niezweryfikowana |
| Qwen3.5-122B-A10B | 4,36 | 68,33 | niezweryfikowana |
| Qwen3.5-27B (thinking) | 4,34 | 54,33 | Apache-2.0, 262k kontekstu |
| Gemma-4-31B | 4,32 | 69,33 z rozumowaniem / 59,17 bez | Apache-2.0, 256k kontekstu |
| DeepSeek-V3.2 | 4,14 | — | — |
| gpt-oss-120b | 3,82 | 54,33 | — |
| Bielik-11B-v3 | 3,73 | **70,67** | Apache-2.0 |
| PLLuM-12B-nc-250715 | 3,67 | 69,67 | niekomercyjna |
| Bielik-Minitron-7B | — | 53,00 | Apache-2.0 |
| gpt-oss-20b | — | 32,33 | Apache-2.0 |

Źródła: [CPTUB](https://huggingface.co/spaces/speakleash/cptu_bench), [PLCC](https://huggingface.co/spaces/sdadas/plcc),
[Qwen3.5-27B](https://huggingface.co/Qwen/Qwen3.5-27B), [Gemma 4 31B](https://huggingface.co/google/gemma-4-31B-it),
[gpt-oss-20b](https://huggingface.co/openai/gpt-oss-20b). Najlepszy otwarty model w PLCC to DeepSeek-V4-Pro-0813
(1,7 bln parametrów) z 89,83 — modele zamknięte mają 92–97.

**Zadania zawodowe po polsku — sufit jakości:**

- wyszukiwanie przepisów na pytaniach z egzaminów wstępnych na aplikację adwokacką i radcowską: **72,3% trafień
  top-1** wobec 61,7% dla BM25 (31.08.2026, [arXiv 2608.30929](https://arxiv.org/abs/2608.30929));
- egzamin kwalifikacyjny KIO: **żaden model nie zdał części praktycznej** (6.11.2025, [arXiv 2511.04205](https://arxiv.org/abs/2511.04205));
- polskie egzaminy lekarskie: najlepszy z 21 modeli to otwarty Qwen3.5-122B, ale przy ostrzejszej ocenie wyniki
  spadły o 31 pkt proc. (10.06.2026, [arXiv 2606.12250](https://arxiv.org/abs/2606.12250));
- Polish Medical Leaderboard: Bielik-11B-v3 50,21%, lider Llama-3.1-405B 69,2% (19.09.2026,
  [HF](https://huggingface.co/spaces/speakleash/polish_medical_leaderboard)).

**Wniosek:** w prawie jakość wyszukiwania po polskich przepisach znaczy więcej niż surowa siła modelu.

### Kwantyzacja: 2 bity psują agentów

- Bielik-11B-v2.3 w 2-bitowym QuIP# (3,26 GB) trzyma 71,92% wobec 72,07% na 22 polskich testach
  ([arXiv 2603.04162](https://arxiv.org/abs/2603.04162)) — ale to testy wyboru odpowiedzi.
- **PolAgentBench (25.09.2026)**, 67 polskich zadań agentowych z narzędziami: Bielik-11B-v3, Bielik-Minitron-7B
  i Llama-PLLuM-8B **„spadają z klifu" między 3 a 2 bitami GGUF** ([arXiv 2609.32042](https://arxiv.org/abs/2609.32042)).
- **Reguła:** Q4–Q8 dla czatu i narzędzi; nigdy Q2 dla agenta.

### Który model do czego (rekomendacja)

| Zadanie | Polecam | Dlaczego |
|---|---|---|
| Rozumowanie, analiza akt, pisma (pudełko 32–64 GB) | Qwen3.5-27B albo Gemma-4-31B (Q4–Q8); Qwen3.6-27B po sprawdzeniu licencji | Czołówka CPTUB, Apache-2.0, długi kontekst |
| To samo na pudełku 128 GB | Qwen3.5-122B-A10B lub gpt-oss-120b | MoE — szybki dekod przy dużej pamięci; Qwen3.5-122B najlepszy otwarty na egzaminach lekarskich |
| Polski styl, redakcja pism do klienta, tekst „po ludzku" | Bielik-11B-v3 lub Bielik-PL-11B (APT4); na małym sprzęcie Minitron-7B | Lider PLCC w swojej wielkości, Apache-2.0 |
| Filtr bezpieczeństwa wejścia i wyjścia | Bielik-Guard 0.5B | Polski, mały, Apache-2.0 |
| Tłumaczenie umów | EuroLLM-22B-Instruct (Apache-2.0, 35 języków) | Autorzy deklarują poziom Gemma-3-27B i Qwen-3-32B w tłumaczeniu ([HF](https://huggingface.co/utter-project/EuroLLM-22B-Instruct-2512)) |
| Mowa na tekst (wizyta, dyktowanie) | Whisper large-v3-turbo (whisper.cpp) | 30 s audio w ok. 618 ms na M1 Ultra ([whisper.cpp](https://github.com/ggml-org/whisper.cpp/issues/89)); polskiego słownictwa medycznego nie zweryfikowano — pilotaż z nagraniami za zgodą |
| Czego unikać w płatnym produkcie | PLLuM „-nc" i pllum-1.x; Q2 dla agentów | Licencja i jakość |

**Mój zestaw (4× R9700, DeepSeek-V4-Flash, 4 sloty po 131k, ok. 13,6 tok/s na agenta, tylko tekst):**
DeepSeek-V4-Flash nie występuje w danych PLCC ani CPTUB, które tu cytuję — w tabelach jest tylko V4-Pro (PLCC 89,83)
i V3.2 (CPTUB 4,14). Dlatego traktuję tę maszynę jako **laboratorium**: uruchamiam na niej PLCC, CPTUB i własne
zestawy prawne oraz medyczne dla każdego kandydata, zanim trafi do pudełka klienta. Licencji V4-Flash nie
weryfikowano w tym przeglądzie — sprawdź ją przed użyciem komercyjnym. Model jest tekstowy, więc mowę obsługuje
osobny Whisper. Hybryda z [Claude](01-PROFILE.md#2-claude) jako planistą ma sens tylko dla spraw, które klient
oznaczy jako niepoufne — patrz [kurs, hybryda lokalny + Claude](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md)
i [03-WZORCE-TECHNICZNE.md](03-WZORCE-TECHNICZNE.md). Ewaluację opisuje [kurs, część 14](../kurs_aplikacje_agentowe/14-EWALUACJA.md).

---

## 7. Sprzęt na biurko

Ceny z apple.com/pl i ceneo.pl, **sprawdzone 11.10.2026**; prędkości z benchmarków społeczności (llama.cpp, LMSYS)
i blogów — nie z własnego pomiaru. Ceny sprzętu z dużą pamięcią rosną: DGX Spark +17,5% (z 3 999 do 4 699 USD,
II 2026), RTX PRO 6000 ok. +87% od premiery — **wyceny dla klienta dawaj z terminem ważności**
([NVIDIA forum](https://forums.developer.nvidia.com/t/2-23-2026-price-change-announcement/361713),
[tech-insider](https://tech-insider.org/nvidia-rtx-pro-6000-blackwell-price-2026/)).

| Urządzenie | Pamięć / przepustowość | Cena w Polsce (11.10.2026) | Jakie modele | Prędkość dekodowania (przykłady) | Pobór / hałas | Dla kogo |
|---|---|---|---|---|---|---|
| Mac mini M5 Pro | 24–64 GB / 307 GB/s | od **8 499 zł** (24 GB); 18/20 rdzeni od 9 499 zł; cena 64 GB nieuchwycona | 8–14B gęste, 30B-A3B MoE (MoE 35B-A3B wymaga ponad 32 GB) | 7B Q4 ok. 67 tok/s; Qwen3.5-35B-A3B 112 tok/s na rodzinie M5 (MLX) | brak danych / bardzo cichy (niezmierzone) | Solo adwokat lub lekarz |
| Mac Studio M5 Max | 36–128 GB / do 614 GB/s | od **12 499 zł** (36 GB); 40-rdzeniowe GPU od 15 499 zł | do gpt-oss-120b (128 GB); 70B Q4 od 64 GB | 7B Q4 ok. 120 tok/s; 120B ok. 40–60 (szacunek bloga) | 7 W spoczynek / 200 W max; cichy | Solo z dużym modelem, mała przychodnia |
| Mac Studio M5 Ultra | 96–256 GB (512 GB od końca X) / 1,2 TB/s | od **27 999 zł** (96 GB); 80-rdzeniowe GPU od 34 499 zł | 235B-A22B MoE, 70B Q8 | 7B Q4 ok. 179 tok/s; 235B ok. 25–35 (szacunek) | 9 W / 385 W; cichy | Kancelaria na Macach, 1–5 osób |
| ASUS Ascent GX10 (GB10, jak DGX Spark) | 128 GB / 273 GB/s | od **24 499 zł** (1 TB); Dell ok. 27 992 zł; NVIDIA FE ok. 30 506 zł | gpt-oss-120b, 30B-A3B; 70B za wolny | 120B ok. 35–56 tok/s; prefill ok. 1,8–2 tys. tok/s; 70B FP8 2,7 tok/s | do 240 W; cichy, wentylator słyszalny pod obciążeniem | Kancelaria 1–5 osób, RAG po długich aktach; gwarancja biznesowa OEM |
| Strix Halo (Ryzen AI Max+ 395) 128 GB | 128 GB / 256 GB/s | **13 490 zł** (Minisforum MS-S1 Max) – 16 999 zł (GMKtec EVO-X2); Framework 16 529 zł (brak w magazynie) | Ta sama klasa co GB10 | 120B ok. 31–47 tok/s; 30B MoE 70–100 tok/s | ok. 100–120 W; 29–43 dBA | Solo na Windows lub Linux — najtańsze 128 GB; słabszy prefill |
| Wieża + RTX PRO 6000 Blackwell | 96 GB / 1 792 GB/s | sama karta: Max-Q od **65 999 zł**, Workstation 84 630–97 156 zł | 120B, 70B Q8, wielu użytkowników naraz | 120B ok. 196 tok/s; prefill ok. 5,5 tys. tok/s | karta 600 W; głośna wieża | Biuro 5–10 osób, szafa serwerowa |
| Wieża + 1–2× Radeon AI PRO R9700 | 32 GB na kartę / 640 GB/s | ok. **8 900** – 10 321 zł za kartę | 14–32B, 30B-A3B | 7B Q4 ok. 146 tok/s (Vulkan) | 300 W na kartę; turbina, głośno | Budżetowo dla kilku osób; dojrzałość ROCm i Vulkan niższa niż CUDA |

Źródła: [Mac mini](https://www.apple.com/pl/shop/buy-mac/mac-mini), [Mac Studio](https://www.apple.com/pl/shop/buy-mac/mac-studio),
[Apple newsroom](https://www.apple.com/newsroom/2026/08/apple-introduces-new-mac-studio-with-m5-max-and-m5-ultra/),
[Apple pobór mocy](https://support.apple.com/en-us/102027), [llama.cpp Apple](https://github.com/ggml-org/llama.cpp/discussions/4167),
[Ollama MLX](https://ollama.com/blog/mlx), [bestllmfor (szacunki)](https://bestllmfor.com/ai-hardware/mac-studio-m5/),
[ceneo GX10](https://www.ceneo.pl/;szukaj-ascent+gx10), [ceneo DGX Spark](https://www.ceneo.pl/;szukaj-dgx+spark),
[LMSYS DGX Spark](https://www.lmsys.org/blog/2025-10-13-nvidia-dgx-spark), [llama.cpp gpt-oss-120b](https://github.com/ggml-org/llama.cpp/discussions/16578),
[Framework forum](https://community.frame.work/t/dgx-spark-vs-strix-halo-initial-impressions/77055),
[ceneo Strix Halo](https://www.ceneo.pl/;szukaj-ryzen+ai+max%2B+395+128gb), [runaihome (blog)](https://runaihome.com/blog/framework-desktop-vs-gmktec-evo-x2-local-ai-2026/),
[ceneo RTX PRO 6000](https://www.ceneo.pl/;szukaj-rtx+pro+6000+blackwell), [llama.cpp RTX PRO 6000](https://github.com/ggml-org/llama.cpp/discussions/15396),
[ceneo R9700](https://www.ceneo.pl/;szukaj-radeon+ai+pro+r9700), [llama.cpp Vulkan](https://github.com/ggml-org/llama.cpp/discussions/10879).

**Jak wybrać:**

- **Solo profesjonalista** (jedna osoba, pisma i pytania do własnych plików): Mac mini M5 Pro 48–64 GB albo Mac Studio
  M5 Max 128 GB dla jakości klasy gpt-oss-120b. Pobór w spoczynku poniżej 10 W i cisza pasują do pokoju z klientem.
  Na Windows: Strix Halo 128 GB.
- **Kancelaria 1–5 osób, RAG po aktach:** liczy się prefill i współbieżność → GB10 (ASUS GX10, ok. 24,5 tys. zł):
  CUDA, vLLM, gwarancja OEM. Biuro na Macach → M5 Ultra. Ponad 5 osób naraz → wieża z RTX PRO 6000 (łącznie
  ok. 90–120 tys. zł wg cen z ceneo.pl).
- **Gabinet lekarski** (Whisper + notatka, zwykle jeden lekarz naraz): Mac mini M5 Pro 48–64 GB albo Mac Studio M5 Max;
  przy kilku gabinetach — jeden GB10 jako serwer.
- **Energia (orientacyjnie, bez ceny prądu):** Strix Halo pod obciążeniem ok. 110 W × 8 h × 21 dni ≈ 18,5 kWh
  miesięcznie; sama karta RTX PRO 6000 Workstation pobiera do 600 W, a Mac Studio M5 Max w spoczynku 7 W.

**Mój zestaw dla porównania:** 4× R9700 to 128 GB VRAM za ok. 35,6 tys. zł (same karty, 4 × ok. 8 900 zł, ceneo
11.10.2026), do 1 200 W TBP na kartach. Świetny do testów i wielu agentów naraz, **ale to nie jest produkt na biurko
klienta**: głośny, gorący i wymaga opieki nad ROCm. Szczegóły układu: [harnessy — koszty](../harnessy-agentowe/03-ARCHITEKTURA.md#5-koszty-czy-lokalnie-jest-taniej).

---

## 8. Szanse produktowe, ryzyka i wejście na rynek

### Szanse według zawodu

| Zawód | Co asystent robi lokalnie | Co go wyróżnia | Kotwica cenowa |
|---|---|---|---|
| Adwokat, radca prawny (1–10 osób) | Analiza akt, chronologia sprawy, szkice pism, porównanie wersji umów, tłumaczenie umów, odpowiedzi z cytatem do akt i ISAP/SAOS | Spełnia § 23e „z konstrukcji": dane lokalne, tylko szkice, weryfikowalne cytaty, notatka o narzędziach dla klienta | Beck-Noxtua 590 zł netto/mies./os. + Legalis; LEX AI 49–489 zł |
| Doradca podatkowy, biuro rachunkowe | Czytanie KSeF XML i JPK, klasyfikacja, odpowiedzi o konkretnej fakturze z odnośnikiem do linii, monitoring interpretacji KIS | Inkumbenci wysyłają dane do modeli z USA (inFakt) albo zakazują danych osobowych (Comarch beta) | wFirma — AI w pakiecie; M365 Copilot 18 USD/os./mies. |
| Lekarz, przychodnia | Transkrypcja wizyty (Whisper) i notatka, skierowania, listy; integracja przez wtyczkę przeglądarki jak w Noa | Audio i dane nie wychodzą z gabinetu; bez diagnoz (KEL art. 12, MDR) | Noa Notes 199 zł/mies. + VAT na lekarza |
| Notariusz | Szkice i porównania dokumentów, wyszukiwanie w archiwum kancelarii | Tajemnica z art. 18; brak wytycznych KRN — szansa i niepewność zarazem | Brak danych |
| Biegły rewident | Przegląd dokumentacji badania, wyszukiwanie w papierach roboczych, ślad audytowy | Art. 78 bez limitu czasu | Brak danych |

**Siedem obietnic, które da się udowodnić** (na podstawie źródeł z tego przeglądu):

1. **„Nic nie wychodzi z pokoju"** — brak procesora (art. 28) i transferu (art. 44–49) dla części AI, brak CLOUD Act,
   brak zależności od DPF.
2. **Praca na tym, czego inni zabraniają** — pełne akta, nieanonimizowana dokumentacja medyczna, księgi klientów.
3. **Zgodność wbudowana** — cytat przy każdej odpowiedzi, notatka o narzędziach per sprawa, zakres medyczny bez diagnoz.
4. **Polszczyzna** — Bielik do stylu, model 27–35B do rozumowania.
5. **Tryb bez internetu** — działa podczas awarii łącza; zgodne z zasadą offline z
   [kursu, część 07](../kurs_lokalne_modele/07-SANDBOX-BEZPIECZENSTWO-MONITORING.md).
6. **Dokumenty dla ostrożnych** — wzór DPIA, odpowiedzi na listę UODO, opinia KRiBSI.
7. **Rachunek kosztów** — poniżej.

### Rachunek: lokalnie czy chmura (2 lata, ceny katalogowe netto, bez rabatów)

| Scenariusz | Chmura przez 24 miesiące | Sprzęt lokalny (jednorazowo) | Wniosek |
|---|---|---|---|
| 1 adwokat, Beck-Noxtua | 590 × 24 = **14 160 zł** + Legalis | Mac mini M5 Pro od 8 499 zł lub Strix Halo 13 490 zł | Sprzęt tańszy, ale Beck-Noxtua daje treści Legalis, których pudełko nie ma — sprzedawaj jako uzupełnienie |
| 3 prawników, Beck-Noxtua | 590 × 3 × 24 = **42 480 zł** + Legalis | ASUS GX10 **24 499 zł** + abonament wsparcia | Margines na wsparcie, wdrożenie i aktualizacje |
| 1 lekarz, Noa Notes | 199 × 24 = **4 776 zł** | Mac mini M5 Pro od 8 499 zł | **Cena przegrywa** — tu sprzedaje tylko prywatność |
| Przychodnia, 5 lekarzy, Noa Notes | 199 × 5 × 24 = **23 880 zł** | Mac Studio M5 Max (40-rdzeniowe GPU) od 15 499 zł albo GX10 24 499 zł jako wspólny serwer | Wspólne pudełko się spina |
| Biuro 10 osób, M365 Copilot Business | 18 USD × 10 × 24 = **4 320 USD** | GX10 24 499 zł | Na cenie za stanowisko nie wygrasz z Copilotem — wygrywasz tajemnicą |

Do kosztu lokalnego dolicz: abonament wsparcia i aktualizacji, wdrożenie, prąd, VAT i ryzyko zmiany ceny sprzętu.
Dla porównania koszt chmury UE poza USA: IONOS bierze za Qwen3.5-9B 0,11/0,17 USD za mln tokenów wejścia/wyjścia
([IONOS](https://cloud.ionos.com/managed/ai-model-hub), *dane firmy*) — **chmura jest tania; pudełko musi wygrać
tajemnicą i kontrolą, nie ceną tokena.** Model wyceny, który wynika z tabeli: jednorazowo sprzęt + roczny abonament
(aktualizacje modeli, łatki, wymiana sprzętu), wyceniony względem 2–3 lat opłat za stanowiska w chmurze.

### Wejście na rynek: kanały

- **Kolejność przyczółków (hipoteza do sprawdzenia):** (1) małe kancelarie adwokackie i radcowskie — najostrzejsza
  tajemnica, jasna kotwica 590 zł, konkurencja tylko w chmurze; (2) biura podatkowe i rachunkowe — KSeF XML
  i obowiązek weryfikacji; (3) przychodnie z 3+ lekarzami — wspólne pudełko zamiast 199 zł na lekarza.
- **Przez samorządy zawodowe:** szkolenia z art. 4 AI Act i z § 23e dla izb adwokackich, OIRP, KIDP; NIL już robi
  szkolenia z AI (29.09 i 20.10.2026). **Nie twierdź, że NRA lub KIRP rekomenduje produkt** — mów „zaprojektowany
  pod § 23e".
- **Przez dostawców oprogramowania:** systemy do prowadzenia kancelarii, EDM w gabinetach (wtyczka przeglądarki jak
  Noa), ekosystem ERP. Wydawcy (LEX, Legalis) mają treści — **uzupełniaj ich**, działając na własnych plikach klienta.
- **Przez integratorów IT i producentów sprzętu:** Dell jest partnerem Bielika ([bielik.ai](https://bielik.ai/)),
  a wersje OEM GB10 (ASUS, Dell, HP) mają gwarancję biznesową i serwis na miejscu — to ważne dla klienta, który nie
  ma informatyka.
- **Dostrajanie poza biurkiem:** adaptery prawne i medyczne można trenować na publicznych danych w fabrykach AI
  EuroHPC (PIAST w Poznaniu, Gaia) albo na GPU Beyond.pl, a wnioskowanie u klienta zostaje lokalne
  ([EuroHPC](https://www.eurohpc-ju.europa.eu/ai-factories_en), [Beyond.pl](https://beyond.pl/en/)).
- **Ucz się od Noxtua:** dwa tiery (lokalny i opcjonalny frontier pod umową UE) wybierane per sprawa, a ustawa
  o tajemnicy na pierwszym planie strony bezpieczeństwa ([profil](01-PROFILE.md#14-noxtua)).

### Ryzyka i jak je ograniczyć

| Ryzyko | Skąd | Ograniczenie |
|---|---|---|
| Odpowiedzialność za produkt | PLD od 9.12.2026 obejmuje AI i aktualizacje; profesjonalista odpowiada osobiście (§ 23e, KIRP, KIDP) i przerzuci to w negocjacjach na dostawcę | Opis przeznaczenia, ograniczenie odpowiedzialności w umowie B2B, OC dostawcy, śledzenie polskiej transpozycji PLD |
| Halucynacje przed sądem | 2 184 sprawy w bazie Charlotina, 6 w Polsce (10.10.2026); 72,3% top-1 w wyszukiwaniu przepisów; KIO niezdany | Cytat przy każdej odpowiedzi, dozwolone „nie wiem", polskie testy akceptacyjne przed każdą zmianą modelu |
| Wsparcie i aktualizacje | Bielik bez SLA; czołowe modele zmieniały się w 2026 kilka razy (Qwen 3.5 → 3.6 → 3.8, Gemma 4) | Abonament z aktualizacjami, rejestr licencji, przypięte wersje, podpisane paczki offline |
| CRA | Zgłaszanie od 11.09.2026, pełne obowiązki od 11.12.2027 | SBOM, proces obsługi podatności, aktualizacje przez cały cykl życia |
| Bezpieczeństwo lokalne | MyDr pokazuje, że UODO kontroluje; kradzież pudełka bez szyfrowania = naruszenie (art. 33–34 RODO) | FileVault lub LUKS, konta i logi per użytkownik, szyfrowane kopie, linka zabezpieczająca, brak zdalnego dostępu domyślnie, wyłączona telemetria — por. [kurs, część 16](../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md) |
| Wejście w wysokie ryzyko | Triaż, scoring, HR, sugestie diagnoz (załącznik III od 2.12.2027, MDR i załącznik I od 2.08.2028) | Twarde granice funkcji; opinia KRiBSI |
| Licencje modeli | PLLuM „-nc", pllum-1.x, Gemma w PLLuM-4B, Llama w Llama-PLLuM | Tylko Apache-2.0 lub komercyjnie oczyszczone wagi; lista licencji dla klienta |
| Sprzęt | Ceny pamięci +17–87% w 2026; Framework niedostępny w Polsce; Mac Studio 512 GB jeszcze nie w sprzedaży | Wyceny z terminem ważności, dwa warianty sprzętu w ofercie |
| Popyt | 77% niekorzystających nie wdroży AI „dopóki nie musi" (PIE) | Sprzedawaj rozwiązanie ryzyka (tajemnica, shadow AI), nie „AI" |

---

## Źródła tej części

Wszystkie źródła z linkami są podane przy tabelach i akapitach powyżej oraz w zbiorczym [ZRODLA.md](ZRODLA.md).
Najważniejsze teksty prawne: [RODO](https://eur-lex.europa.eu/eli/reg/2016/679/oj),
[AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj), [AI Omnibus 2026/1744](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601744),
[ustawa o systemach SI, Dz.U. 2026 poz. 1003](https://api.sejm.gov.pl/eli/acts/DU/2026/1003/text.pdf),
[18 U.S.C. § 2713](https://www.law.cornell.edu/uscode/text/18/2713). Informacje oznaczone jako niezweryfikowane
(interwencja Microsoftu w C-703/25 P, wygaśnięcie FISA 702, numery paragrafów zasad KIDP, licencja Qwen3.6 i DeepSeek-V4-Flash,
liczba adwokatów i radców) wymagają sprawdzenia przed użyciem w materiałach sprzedażowych.
