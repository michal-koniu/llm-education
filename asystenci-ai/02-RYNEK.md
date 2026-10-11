# Rynek asystentów AI — modele biznesowe, liczby, porażki

**Stan na 11 października 2026.**

Ten plik to część „biznesowa" przeglądu: kto na asystentach AI zarabia, za co klienci płacą, ile to jest warte, kto
kogo kupił i co się nie udało. Piszę go z jednej perspektywy: **chcę sprzedawać lokalnego asystenta „na biurko"
polskim profesjonalistom** (prawnikom, lekarzom, doradcom podatkowym, księgowym) i potrzebuję wiedzieć, jakie
modele cenowe działają, czego klient się spodziewa i gdzie konkurencja ma lukę.

> ⚠️ **Liczby w tym pliku starzeją się w tygodnie.** Każda ma datę i źródło. *(dane firmy)* = deklaracja samej
> firmy (blog, komunikat, strona), *(szacunek prasy)* / *(Sacra)* = szacunek dziennikarzy albo analityków.
> ARR (*annual recurring revenue*) i *run-rate* to przychód z ostatniego okresu przemnożony do roku — nie to samo co
> roczny przychód w sprawozdaniu. Niczego tu nie przeliczałem po kursie walut.

Profile 15 asystentów z czołówki są w [01-PROFILE.md](01-PROFILE.md), wzorce techniczne
w [03-WZORCE-TECHNICZNE.md](03-WZORCE-TECHNICZNE.md), a polskie prawo, ceny i konkurencja
w [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md).

---

## Spis treści

- [Najkrótsza odpowiedź](#najkrótsza-odpowiedź)
- [1. Mapa rynku: cztery rodzaje asystentów](#1-mapa-rynku-cztery-rodzaje-asystentów)
- [2. Modele biznesowe i cenniki](#2-modele-biznesowe-i-cenniki)
- [3. Liczby: użytkownicy, przychody, finansowanie](#3-liczby-użytkownicy-przychody-finansowanie)
- [4. Fuzje, przejęcia i ruchy 2026](#4-fuzje-przejęcia-i-ruchy-2026)
- [5. Dystrybucja i fosy](#5-dystrybucja-i-fosy)
- [6. Porażki i lekcje](#6-porażki-i-lekcje)
- [7. Trendy 2026](#7-trendy-2026)
- [8. Co z tego wynika dla mnie](#8-co-z-tego-wynika-dla-mnie)
- [Źródła tego pliku](#źródła-tego-pliku)

---

## Najkrótsza odpowiedź

- **Największe pieniądze są w asystentach profesjonalnych, nie w „ogólnych".** Programiści (Cursor, Claude Code,
  Cognition), prawnicy (Harvey, Legora) i lekarze (Abridge, OpenEvidence) płacą najwięcej i najszybciej. Kodowanie to
  według Menlo Ventures 55% wydatków działowych na AI w firmach (2025).
- **Stała cena za stanowisko pęka, gdy agent pracuje godzinami.** Cały rynek przechodzi na kredyty i rozliczenie za
  zużycie (Cursor 2025, GitHub Copilot 1.06.2026, Glean 2026), a najodważniejsi na **płatność za wynik** (Sierra).
- **Otwarte środowiska wygrały warstwę „żyjących" asystentów.** OpenClaw ma fundację, a Microsoft zbudował na nim
  Autopilot (25.09.2026). Nikt nie zarabia na samym kodzie — zarabia się na chmurze, modelach, sprzęcie albo wsparciu.
- **Liderzy dotrenowują modele open-weight** (Harvey Tenet na Kimi K3, Cursor Composer 2 na Kimi K2.5, „Thomson" od
  Thomson Reuters). To potwierdza strategię „średni otwarty model + dobre wyszukiwanie + własne dane".
- **Żaden lider dla profesjonalistów nie działa na biurku, offline.** Pułap prywatności rynku w 2026 to „hosting w UE
  + brak trenowania". To jest moja nisza.
- **Polska kotwica cenowa:** Beck-Noxtua 590 zł netto/mies. za użytkownika (plus Legalis), Noa Notes 199 zł + VAT,
  LEX AI 49–489 zł/mies. Profesjonalista już płaci **200–600 zł miesięcznie za stanowisko** w chmurze.

---

## 1. Mapa rynku: cztery rodzaje asystentów

W całym przeglądzie dzielę asystentów na cztery rodzaje. Każdy ma inny model biznesowy i innych zwycięzców.

| Rodzaj | Co robi | Liderzy (czołówka) | Gdzie są pieniądze | Model biznesowy |
|---|---|---|---|---|
| **Codzienni** | czat, wyszukiwanie, pisanie, głos — dla każdego | [ChatGPT](01-PROFILE.md#7-chatgpt), [Gemini](01-PROFILE.md#8-gemini), [Claude](01-PROFILE.md#2-claude), [Perplexity](01-PROFILE.md#15-perplexity) | ogromne zasięgi (ChatGPT 1,2 mld tygodniowo 29.09.2026, Gemini 1 mld+ miesięcznie 11.08.2026), ale pieniądze idą z drogich progów 200–500 USD | subskrypcja z progami + API |
| **Profesjonalni** | wąska praca zawodowa: pismo procesowe, notatka z wizyty, kod, protokół | [Harvey](01-PROFILE.md#4-harvey), [Abridge](01-PROFILE.md#3-abridge), [Cursor](01-PROFILE.md#9-cursor), [Granola](01-PROFILE.md#10-granola), [Sierra](01-PROFILE.md#11-sierra), [OpenEvidence](01-PROFILE.md#12-openevidence), [Noxtua](01-PROFILE.md#14-noxtua) | **najwyższe przychody na klienta i najszybsze wzrosty** | licencje firmowe, stanowiska, zużycie, wynik, reklamy |
| **Wykonawcy autonomiczni** | wirtualny komputer albo przeglądarka, agent klika, pisze, oddaje plik | [Manus](01-PROFILE.md#6-manus), [browser-use](01-PROFILE.md#13-browser-use), Genspark, ChatGPT Work | szybkie ARR (Manus 100 mln USD w 8 miesięcy, XII 2025), ale wysoki koszt obliczeń | kredyty + subskrypcja |
| **Żyjący autonomicznie** | zawsze włączony agent z pamięcią, harmonogramem i komunikatorami | [OpenClaw](01-PROFILE.md#1-openclaw), [Hermes Agent](01-PROFILE.md#5-hermes-agent), Poke, Lindy, Microsoft Autopilot | pieniądze **wokół** otwartego kodu: chmura, modele, sprzęt, wersje firmowe | fundacja, open source + chmura, subskrypcja |

**Gdzie płyną budżety** — najlepsze dane przekrojowe, jakie mam, są z 2025 roku
([Menlo Ventures, 9.12.2025](https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/),
*(szacunek analityka)*):

- wydatki firm na generatywną AI: **37 mld USD w 2025** (11,5 mld w 2024, ×3,2);
- aplikacje do kodowania: **4,0 mld USD**, czyli 55% wydatków działowych (z 550 mln);
- AI branżowa (wertykalna): 3,5 mld USD, z czego ochrona zdrowia ok. 1,5 mld;
- 76% zastosowań firmy **kupują**, a nie budują; 27% wydatków na aplikacje przychodzi przez samoobsługę (PLG).

W medycynie: wydatki na AI w ochronie zdrowia 1,4 mld USD w 2025, z czego „skryby" (automatyczne notatki z wizyty)
600 mln; udziały: Nuance/Microsoft DAX ok. 33%, Abridge ok. 30%, Ambience ok. 13%
([Menlo Ventures, 21.10.2025](https://menlovc.com/perspective/2025-the-state-of-ai-in-healthcare/), *(szacunek analityka)*).

**Wniosek dla mnie:** zarabia się na **wąskiej pracy zawodowej**, za którą ktoś odpowiada podpisem. Ogólny czat to
rynek gigantów; profesjonalista kupuje gotowy, sprawdzalny produkt pracy (pismo, notatkę, zestawienie).

---

## 2. Modele biznesowe i cenniki

### Przegląd modeli

| Model | Przykłady | Plusy | Minusy | Lekcja dla mnie |
|---|---|---|---|---|
| **Subskrypcja z progami** (free / plus / pro / max) | ChatGPT, Claude, Gemini, Perplexity, Poke, Nous Portal | prosta, przewidywalna; drogi próg łapie „power userów" | najaktywniejsi użytkownicy zjadają marżę; trzeba dokładać limity | progi 20 i 200 USD to dziś standard rynku |
| **Kredyty** | Manus, Genspark, Lindy, Fellou, Flowith | jedna jednostka łączy tokeny, czas maszyny i API; skaluje się z pracą | klient nie wie, ile zapłaci za zadanie; kredyty przepadają | jeśli kredyty — tłumaczyć je w „rodzajach pracy", nie w tokenach |
| **Stanowisko → zużycie** | Cursor, GitHub Copilot, Glean, Notion, Claude Code | dopasowanie ceny do kosztu agentów | zmiana cennika budzi bunt (Cursor 2025) | zmianę zapowiadać wcześnie i jasno; dawać limit i pauzę zamiast niespodzianki |
| **Za wynik** | Sierra, Intercom Fin, Parloa, Ambience | klient płaci tylko za efekt; łatwa sprzedaż do zarządu | trzeba zdefiniować i mierzyć „wynik"; ryzyko po stronie dostawcy | działa przy mierzalnej pracy (sprawa zamknięta, notatka przyjęta) |
| **Darmowe + reklamy** | OpenEvidence, Doximity GPT | zerowa bariera wejścia; ogromny zasięg wśród lekarzy | zależność od reklamodawców (farmacja); konflikt interesów | model dla zasięgu, nie dla tajemnicy zawodowej — nie mój przypadek |
| **Open source + chmura / fundacja / BYOK** | OpenClaw, Hermes + Nous Portal, browser-use Cloud, Manus Flex, Kortix | zaufanie, zasięg, społeczność; klient może odejść z kodem | sam kod nie zarabia; bezpieczeństwo spada na użytkownika | mój produkt może stać na otwartym rdzeniu — płaci się za integrację, utrzymanie i wsparcie |
| **Licencja firmowa / pakiet z treścią** | Harvey, Legora, CoCounsel, Abridge, Beck-Noxtua, Microsoft Copilot | wysokie kontrakty roczne; treść (komentarze, orzecznictwo) jako fosa | długi cykl sprzedaży; cena ukryta | dla kancelarii 1–10 osób potrzebny jest cennik publiczny, nie „umów demo" |
| **Sprzęt + oprogramowanie** | Ghost (3 499 USD), Rabbit r1 | jednorazowa sprzedaż; „działa nawet, gdy dostawca zniknie" | logistyka, gwarancja, aktualizacje | to najbliżej mojego produktu — ale sprzęt nie może wyprzedzić działającego agenta |

### Subskrypcje: progi 20 / 200 USD

Prawie wszyscy codzienni asystenci zbiegli się na tych samych progach:

| Asystent | Progi (miesięcznie) | Data | Źródło |
|---|---|---|---|
| ChatGPT | Plus 20 USD · **Pro 500 za 500 USD** („25× limit Plus") | 29.09.2026 | [Emergent](https://emergent.sh/news/openai-devday-2026), [Decrypt](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced) |
| Claude | Pro 20 USD · Max 100 i 200 USD · Team 20 USD za stanowisko | 2026 | [Anthropic](https://claude.com/blog/cowork-research-preview) *(dane firmy)* |
| Google AI (ceny dla Polski) | Plus 23,99 zł · Pro 97,99 zł · Ultra 469,99 albo 979,99 zł | X 2026 | [Google](https://gemini.google/subscriptions/) |
| Perplexity | Pro 20 USD · Max 200 USD | VIII 2025 | [Vice](https://www.vice.com/en/article/perplexity-comet-plus-announced/) |
| Poke | Pro 19 USD · Ultra 199 USD | 11.10.2026 | [Poke](https://poke.com/pricing) |
| Nous Portal (modele dla Hermesa) | Plus 20 · Super 100 · Ultra 200 USD | 11.10.2026 | [Hermes](https://hermes-agent.nousresearch.com/) |
| Mistral Vibe | Pro 14,99 EUR · Team 24,99 EUR za użytkownika, bez VAT | X 2026 | [Mistral](https://mistral.ai/fr/pricing) |

**Lekcja:** drogi próg (200–500 USD) istnieje po to, żeby agenci, którzy pracują godzinami, mieli z czego żyć.
Perplexity wiąże wzrost przychodu z 450 do ok. 750 mln USD (III → VIII 2026) właśnie z progiem 200 USD i agentem
Computer ([PYMNTS](https://www.pymnts.com/news/artificial-intelligence/2026/perplexitys-shift-to-ai-agents-boosts-revenue-50/),
[Yahoo/The Information](https://finance.yahoo.com/technology/ai/articles/nvidia-discusses-perplexity-investment-30-031804276.html),
*(szacunek prasy)*).

### Kredyty: jednostka „pracy agenta"

Kredyt łączy w jedną liczbę tokeny modelu, czas maszyny wirtualnej i płatne API
([Manus, zasady kredytów](https://help.manus.im/en/articles/11711097-what-are-the-rules-for-credits-consumption-and-how-can-i-obtain-them)).

| Produkt | Cena | Ile to za zadanie | Źródło |
|---|---|---|---|
| Manus | 20 / 40 / 200 USD za 4 000 / 8 000 / 40 000 kredytów (IX 2026) | ok. 0,005 USD za kredyt (wyliczenie badacza) | [myclaw.ai](https://myclaw.ai/blog/manus-2-0) *(recenzja, nie cennik)* |
| Genspark | Plus 24,99 USD (10 000+ kredytów), Pro 249,99 USD (125 000+) | rozmowa telefoniczna „Call For Me" 500 kredytów ≈ 1,25 USD | [Genspark](https://www.genspark.ai/helpcenter/membership-plans), 11.10.2026 |
| Lindy | 49,99 USD za aktywnego użytkownika (5 000 kredytów, pula zespołu); 10 USD za 1 000 dodatkowych | „codzienne prośby" 2–250, „głęboka praca" 250–1 000 kredytów | [Lindy](https://www.lindy.ai/pricing), 11.10.2026 |
| Fellou | Plus 19 USD (2 000 „Sparks"), Pro 39,9 USD (5 000) | ok. 250 Sparks ≈ 2–2,4 USD za złożone zadanie | [Fellou](https://fellou.ai/pricing), X 2026 |
| browser-use Cloud | 0,02 USD za godzinę przeglądarki + tokeny | ok. 0,11–1,64 USD za zadanie | [browser-use](https://browser-use.com/pricing.md), IX 2026 |
| Amazon Nova Act | 4,75 USD za godzinę pracy agenta; czekanie na człowieka niepłatne | — | [AWS](https://aws.amazon.com/nova/pricing/) |

**Dobre praktyki z cenników kredytowych:** Lindy opisuje kredyty rodzajami pracy i **zatrzymuje agenta, gdy pula się
kończy**, zamiast wystawiać rachunek-niespodziankę; Fellou pokazuje szacunek zużycia przed uruchomieniem zadania;
Manus daje codzienne „odświeżane" kredyty, które budują nawyk
([Lindy](https://www.lindy.ai/pricing), [Fellou](https://fellou.ai/pricing), [Manus](https://help.manus.im/en/articles/11711097-what-are-the-rules-for-credits-consumption-and-how-can-i-obtain-them)).
Rabbit poszedł odwrotnie: „rabbit intern" za 99,99 USD/mies. za 30 zadań, reklamowany jako alternatywa dla
„mylących systemów kredytów" ([Rabbit, 13.06.2025](https://www.rabbit.tech/newsroom/rabbit-intern-launch)).

### Od stanowiska do zużycia

- **Cursor (VI 2025):** 16.06.2025 Pro zmienił się z 500 zapytań na 20 USD kredytu po cenach API + „nielimitowany"
  tryb Auto. Użytkownicy nie wiedzieli, że „nielimitowany" dotyczy tylko Auto, i dostali niespodziewane rachunki;
  4.07.2025 Cursor przeprosił i zwrócił pieniądze ([Cursor](https://cursor.com/blog/june-2025-pricing)).
- **Claude Code:** tygodniowe limity ogłoszone 28.07.2025, obowiązują od 28.08.2025 — przeciw pracy 24/7 w tle
  i odsprzedawaniu kont; według Anthropic dotyczyły <5% subskrybentów
  ([TechCrunch](https://techcrunch.com/2025/07/28/anthropic-unveils-new-rate-limits-to-curb-claude-code-power-users/)).
- **GitHub Copilot:** od **1.06.2026** kredyty AI (1 kredyt = 0,01 USD) zamiast „premium requests"; Pro 10 USD
  z kredytami za 15 + 5 USD, Max 100 USD z kredytami za 200 + 100 USD
  ([GitHub docs](https://docs.github.com/en/copilot/concepts/billing/copilot-requests),
  [cennik](https://github.com/features/copilot/plans)).
- **Glean:** z czystych stanowisk na opłatę stałą za aktywnych użytkowników + zużycie modeli (28.05.2026,
  [TechCrunch](https://techcrunch.com/2026/05/28/gleans-top-line-crosses-300m-as-ai-budget-cutting-becomes-its-major-selling-point/)).
- **Notion:** AI w wyższych progach stanowisk, a „Custom Agents" za 10 USD za 1 000 kredytów
  ([Notion](https://www.notion.com/pricing)).

Dlaczego: Gartner przewiduje, że **koszt wnioskowania na jeden agentowy przepływ pracy wzrośnie ponad 5× do 2028**,
mimo że tokeny tanieją (17.08.2026, [Gartner](https://www.gartner.com/en/newsroom/press-releases/2026-08-17-gartner-predicts-ai-inference-costs-per-agentic-workflow-will-increase-more-than-fivefold-through-2028),
*(prognoza analityka)*). Agenci zużywają po prostu dużo więcej tokenów na zadanie.

### Za wynik

- **Sierra** (od 10.12.2024): płacisz za rozwiązane rozmowy, uratowane anulacje, sprzedaż dodatkową; „jeśli rozmowa
  nie jest rozwiązana, w większości przypadków nie ma opłaty" ([Sierra](https://sierra.ai/blog/outcome-based-pricing-for-ai-agents)).
  Hasło z 2026: „płacisz za wyniki, nie za tokeny" ([Sierra Horizon](https://sierra.ai/blog/horizon)).
- **Intercom Fin:** 0,99 USD za wynik ([Intercom](https://www.intercom.com/pricing), *(dane firmy)*).
- **Parloa:** za minutę głosu albo za interakcję czatu, „za wynik, gdy ma to sens" ([Parloa](https://www.parloa.com/platform/pricing/)).
- **Ambience Healthcare:** kontrakty z premią zależną od wyników finansowych szpitala (IV 2026, [Ambience](https://www.ambiencehealthcare.com/blog), *(dane firmy)*).

Sierra sama tłumaczy swój wzrost tym, że wybiera wąskie „zadania do wykonania" ze zdefiniowaną miarą sukcesu
([Sierra, 6.02.2026](https://sierra.ai/blog/year-two-in-review)).

### Darmowe dla profesjonalisty, płaci ktoś inny

**OpenEvidence** daje lekarzom wyszukiwarkę medyczną za darmo i zarabia na reklamach farmacji i wyrobów medycznych
(CPM 70–150 USD). Przychód: ok. 7,9 mln USD (XII 2024) → 50 mln (VI 2025) → ok. 300 mln annualizowane (VII–IX 2026),
marża brutto ok. 90% ([Sacra](https://sacra.com/c/openevidence/), *(szacunek analityka)*). Fosa to licencjonowane
treści (NEJM, JAMA, NCCN), nie model ([Wikipedia](https://en.wikipedia.org/wiki/OpenEvidence)).
Doximity GPT działa tak samo — darmowy dla lekarzy, finansowany marketingiem farmacji
([Wikipedia](https://en.wikipedia.org/wiki/Doximity)).

### Open source + chmura, fundacja, BYOK

- **OpenClaw** nie sprzedaje niczego. Od 8.07.2026 prowadzi go **OpenClaw Foundation** (501(c)(3) w USA, 12 osób na
  etatach); darczyńcy i partnerzy to m.in. OpenAI, University of Michigan (największy darczyńca), NVIDIA, Microsoft,
  Red Hat, Tencent, Atlassian, Vercel, Cloudflare, GitHub; kwot nie podano
  ([fundacja](https://openclaw.ai/blog/introducing-openclaw-foundation), *(dane fundacji)*). OpenClaw Enterprise
  (29.09.2026) „zawsze będzie darmowy" ([OpenClaw](https://openclaw.ai/blog/openclaw-enterprise)).
- **Hermes Agent** jest darmowy (MIT); zarabia Nous Research na **Nous Portal** (modele i kredyty), **Hermes Business**
  (wspólna pula, limity na członka) i **Hermes Enterprise** (na infrastrukturze klienta)
  ([Nous Portal](https://portal.nousresearch.com/business)).
- **browser-use:** biblioteka MIT, zarabia Browser Use Cloud — godziny przeglądarki, proxy, odsprzedaż tokenów
  ([browser-use](https://browser-use.com/pricing.md)).
- **BYOK** (*bring your own key* — własny klucz do modelu): Manus Flex (29.09.2026) — klient płaci za model sam,
  Manus dalej bierze kredyty za maszyny i narzędzia ([Manus Flex](https://manus.im/blog/introducing-manus-flex));
  Kortix bierze tylko za piaskownicę ([Kortix](https://www.kortix.com/pricing)); OpenHands daje modele „po kosztach,
  bez marży" ([OpenHands](https://openhands.dev/pricing)).
- Egzotyka: Agent Zero finansuje rozwój tokenem kryptowalutowym A0T ([Agent Zero](https://www.agent-zero.ai/p/token/)),
  a nanobot linkami partnerskimi do dostawców modeli ([nanobot](https://github.com/HKUDS/nanobot)).

### Licencje firmowe i pakiety z treścią

Elitarne narzędzia prawnicze nie publikują cen:

- **Harvey:** szacunkowo ok. 1 200 USD za stanowisko miesięcznie przy małych wdrożeniach (minimum 20 stanowisk)
  i 100–200 USD w skali Am Law 100 ([Vaquill](https://www.vaquill.ai/blog/harvey-ai-review-honest-assessment),
  *(szacunek zewnętrzny, niezweryfikowany)*);
- **Legora:** ok. 3 000 USD za stanowisko rocznie (minimum 10) ([Layer3](https://www.layer3labs.io/guides/legora-pricing),
  *(szacunek zewnętrzny)*);
- **Abridge:** ok. 2 500 USD za lekarza rocznie ([Sacra](https://sacra.com/c/abridge/), *(szacunek analityka)*);
- **CoCounsel** sprzedawany w pakiecie z Westlaw i Practical Law
  ([Thomson Reuters](https://legal.thomsonreuters.com/en/products/cocounsel-legal/plans)).

Narzędzia dla małych kancelarii **publikują ceny**: Clio Work 199 USD za użytkownika miesięcznie
([LawSites](https://www.lawnext.com/2026/04/clio-work-clios-ai-workspace-is-now-available-to-solo-and-smaller-law-firms-as-a-standalone-product.html)),
Blue J 1 498 USD rocznie „bez dodatków" ([Blue J](https://www.bluej.com/pricing)). Poziom odniesienia:
Microsoft 365 Copilot Business 18–21 USD za użytkownika miesięcznie
([Microsoft](https://www.microsoft.com/en-us/microsoft-365-copilot/pricing)).

---

## 3. Liczby: użytkownicy, przychody, finansowanie

Tylko liczby z moich plików badawczych. „Brak danych" znaczy: nie znalazłem wiarygodnej liczby, nie że jej nie ma.
Gwiazdki GitHuba z API 11.10.2026.

### Czołówka 15

| # | Asystent | Użytkownicy / zasięg | Przychód / ARR | Finansowanie / wycena | Źródła |
|---|---|---|---|---|---|
| 1 | [OpenClaw](01-PROFILE.md#1-openclaw) | ⭐ 391,7k; „4,5 mln nowych clawów tygodniowo" (8.07.2026, *dane fundacji*) | nie sprzedaje (fundacja) | darczyńcy, kwoty nieujawnione | [fundacja](https://openclaw.ai/blog/introducing-openclaw-foundation), [GitHub](https://github.com/openclaw/openclaw) |
| 2 | [Claude](01-PROFILE.md#2-claude) | brak danych | run-rate 14 mld USD, Claude Code >2,5 mld (12.02.2026, *dane firmy*); ok. 44 mld (V 2026, *szacunek SemiAnalysis w prasie*) | seria G 30 mld USD przy 380 mld (12.02.2026) | [Anthropic](https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation), [iTiger](https://www.itiger.com/hans/news/1183910360) |
| 3 | [Abridge](01-PROFILE.md#3-abridge) | 300+ systemów ochrony zdrowia, 250 mln+ pacjentów (VI 2026) | ARR 100 mln USD (V 2025, *Sacra*) | seria E 300 mln przy 5,3 mld (VI 2025) + 316 mln (IV 2026); ok. 830 mln łącznie | [Sacra](https://sacra.com/c/abridge/), [MobiHealthNews](https://www.mobihealthnews.com/news/abridge-secures-300m-boosts-valuation-53b), [Fortune](https://fortune.com/2026/06/11/abridge-operating-system-medicine-nvidia-eli-lilly-artsight/) |
| 4 | [Harvey](01-PROFILE.md#4-harvey) | 1 500 organizacji, 100k+ prawników (V 2026); 80% Am Law 100 (9.09.2026, *dane firmy*) | ARR >400 mln USD (IX 2026, *szacunek prasy*) | 550 mln przy 15,5 mld (9.09.2026) | [Harvey](https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence), [itbrief](https://itbrief.co.uk/story/harvey-launches-500-legal-ai-agents-builder-tool), [raising.fi](https://raising.fi/news/harvey-undisclosed-september-2026) |
| 5 | [Hermes Agent](01-PROFILE.md#5-hermes-agent) | ⭐ 252,7k; „sklonowany ponad 24 mln razy", „ok. 2,5% światowego zużycia tokenów" (X 2026, *dane firmy*) | brak danych | Nous Research: 90 mln USD (X 2026) | [Nous](https://nousresearch.com/a-note-on-our-fundraise), [GitHub](https://github.com/NousResearch/hermes-agent) |
| 6 | [Manus](01-PROFILE.md#6-manus) | 80 mln wirtualnych komputerów, 147 bln tokenów (XII 2025, *dane firmy*) | ARR 100 mln USD (XII 2025, *dane firmy*); ok. 450 mln annualizowane (VI 2026, *Sacra, niezweryfikowane u źródła*) | seria B ok. 75 mln przy ok. 500 mln (IV 2025); runda >500 mln USD (8.10.2026, wycena nieujawniona) | [Manus](https://manus.im/blog/manus-100m-arr), [Sacra](https://sacra.com/c/manus), [TechCrunch](https://techcrunch.com/2026/10/08/chinas-manus-raises-over-500m-in-first-funding-round-since-split-with-meta/) |
| 7 | [ChatGPT](01-PROFILE.md#7-chatgpt) | 900 mln tygodniowo (II 2026); 1,2 mld tygodniowo (29.09.2026) | brak danych w moich źródłach | brak danych w moich źródłach | [Wikipedia](https://en.wikipedia.org/wiki/ChatGPT), [Decrypt](https://decrypt.co/379584/openai-ai-agents-computers-devday-2026-everything-announced) |
| 8 | [Gemini](01-PROFILE.md#8-gemini) | 1 mld+ miesięcznie (11.08.2026, *dane firmy*) | nieujawniane osobno (Google) | — (Google) | [Google](https://blog.google/innovation-and-ai/products/gemini-app/one-billion-monthly-users/) |
| 9 | [Cursor](01-PROFILE.md#9-cursor) | brak danych | ARR 2 mld USD (II 2026, *Bloomberg*); 3 mld (V 2026, *Bloomberg wg Wikipedii*) | seria D 2,3 mld przy 29,3 mld (13.11.2025); SpaceX ok. 60 mld w akcjach (finalizacja 14.08.2026) | [Bloomberg](https://www.bloomberg.com/news/articles/2026-03-02/cursor-recurring-revenue-doubles-in-three-months-to-2-billion), [Cursor](https://cursor.com/blog/joining-spacex), [Wikipedia](https://en.wikipedia.org/wiki/Cursor_%28company%29) |
| 10 | [Granola](01-PROFILE.md#10-granola) | 250k+ aktywnych (poł. 2025, *Sacra, niezweryfikowane*) | nieujawniony; ARR +ok. 250% w I kw. 2026 (*agregator*) | seria C 125 mln przy 1,5 mld (25.03.2026) | [TNW](https://thenextweb.com/news/granola-series-c-meeting-ai-enterprise-context), [arr.club](https://www.arr.club/granola/granola-arr-grow-at-250-in-q1-2026) |
| 11 | [Sierra](01-PROFILE.md#11-sierra) | brak danych | ARR 100 mln (XI 2025) → 150 mln+ USD (II 2026, *dane firmy*) | 950 mln przy >15 mld (4.05.2026) | [Sierra](https://sierra.ai/blog/year-two-in-review), [TechCrunch](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/) |
| 12 | [OpenEvidence](01-PROFILE.md#12-openevidence) | 760k lekarzy, 18 mln konsultacji/mies. (XII 2025) | ok. 300 mln USD annualizowane (VII–IX 2026, *Sacra*) | 250 mln przy 12 mld (21.01.2026); ok. 700 mln łącznie | [Sacra](https://sacra.com/c/openevidence/), [Rutland Herald](https://www.rutlandherald.com/news/business/openevidence-raises-250-million-to-build-medical-superintelligence-for-doctors/article_0960939c-ca41-5321-8417-54f84800ece6.html) |
| 13 | [browser-use](01-PROFILE.md#13-browser-use) | ⭐ 117,6k | brak danych | seed 17 mln USD (III 2025) | [Felicis](https://felicis.com/blog/browser-use-the-tool-making-it-easier-for-ai-agents-to-navigate-websites-raises-17m), [GitHub](https://github.com/browser-use/browser-use) |
| 14 | [Noxtua](01-PROFILE.md#14-noxtua) | 30 000+ użytkowników (IX 2026, *dane firmy*) | ceny niepubliczne; w Polsce 590 zł netto/mies. (Beck-Noxtua) | seria B 92,2 mln USD (22.04.2025); seria C 100+ mln EUR (23.09.2026) | [Noxtua](https://www.noxtua.com/news/press-releases/series-c), [TechCrunch](https://techcrunch.com/2025/04/22/noxtua-raises-92m-for-its-sovereign-ai-tuned-for-the-german-legal-system/), [Beck-Noxtua](https://www.beck-noxtua.pl/) |
| 15 | [Perplexity](01-PROFILE.md#15-perplexity) | 100 mln+ MAU (III 2026, *dane firmy*) | ARR ok. 450 mln (III 2026) → ok. 750 mln USD (VIII 2026, *szacunek prasy*) | ok. 20 mld (IX 2025); rozmowy z NVIDIA przy >30 mld (VIII 2026) | [PYMNTS](https://www.pymnts.com/news/artificial-intelligence/2026/perplexitys-shift-to-ai-agents-boosts-revenue-50/), [Yahoo](https://finance.yahoo.com/technology/ai/articles/nvidia-discusses-perplexity-investment-30-031804276.html), [Wikipedia](https://en.wikipedia.org/wiki/Perplexity_AI) |

### Następni — dla porównania

| Asystent | Użytkownicy / zasięg | Przychód / ARR | Finansowanie / wycena | Źródła |
|---|---|---|---|---|
| Legora (prawo, SE) | ok. 1 500 klientów (II kw. 2026) | 100 mln (IV 2026) → >200 mln USD (IX 2026, *wg założyciela, prasa wtórna*) | 600 mln przy 5,6 mld (IV 2026); rozmowy przy ok. 8,5–10 mld (VIII–IX 2026) | [TNW](https://thenextweb.com/news/legora-just-hit-100-million-in-revenue-it-took-18-months), [runtimewire](https://runtimewire.com/article/legora-funding-talks-8-5-billion-valuation) |
| Genspark | 2 mln+ MAU (koniec 2025, *Sacra*) | ok. 250 mln USD ARR (poł. 2026, *dane firmy w prasie*) | 485 mln przy 2,6 mld (17.06.2026) | [AOL](https://www.aol.com/articles/genspark-unveils-ai-workspace-6-150700000.html), [Yahoo](https://finance.yahoo.com/technology/ai/articles/genspark-ai-extends-series-b-131000248.html) |
| Microsoft Copilot | 30 mln+ płatnych stanowisk (FY2026) | nieujawniany osobno | — | [Microsoft IR](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast) |
| GitHub Copilot | 4,7 mln płatnych (I 2026, *źródło wtórne*) | nieujawniany osobno | — | [getpanto](https://www.getpanto.ai/blog/github-statistics) |
| Cognition (Devin, Windsurf) | brak danych | run-rate 1 mld USD (25.09.2026, *dane firmy*) | >2 mld przy 48 mld (8.09.2026) | [Cognition](https://cognition.com/blog/1b-run-rate), [Wikipedia](https://en.wikipedia.org/wiki/Cognition_AI) |
| Lovable (SE) | 60 mln projektów (VIII 2026) | „na drodze do” ok. 600 mln USD ARR (VIII 2026) | 400 mln przy 13,3 mld (VIII 2026) | [VKTR](https://www.vktr.com/ai-platforms/lovable-raises-400-million-at-133-billion-valuation/) |
| Glean | brak danych | 300 mln USD (28.05.2026, z annualizowanym zużyciem) | 7,2 mld (VI 2025) | [TechCrunch](https://techcrunch.com/2026/05/28/gleans-top-line-crosses-300m-as-ai-budget-cutting-becomes-its-major-selling-point/) |
| Heidi Health (AU, UK/UE) | 2,8 mln wizyt tygodniowo (IX 2026) | ARR 50 mln USD (IV 2026) | 100 mln przy 900 mln + 240 mln (IX 2026; Forbes Australia podaje ok. 1,2 mld — dane sprzeczne) | [HLTH](https://hlth.com/insights/news/heidi-raises-340m-to-expand-clinical-ai-into-supervised-agentic-workflows), [Heidi](https://www.heidihealth.com/blog/heidi-series-b) |
| Poke | „setki tysięcy", >100 mln wiadomości w 3 miesiące (VII 2026, *dane firmy*) | brak danych | 300 mln po rundzie (IV 2026); przejęty przez Cognition 23.07.2026 | [Cognition](https://cognition.com/blog/interaction), [TechCrunch](https://techcrunch.com/2026/04/08/poke-makes-ai-agents-as-easy-as-sending-a-text/) |
| Mistral (UE) | brak danych | nieujawniony | 3 mld EUR przy >21 mld EUR (IX 2026) | [Mistral](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/) |
| Cohere + Aleph Alpha | brak danych | ARR Cohere 240 mln USD (2025) | wspólnie ok. 20 mld USD; Schwarz 600 mln (24.04.2026) | [TechCrunch](https://techcrunch.com/2026/02/13/coheres-240m-year-sets-stage-for-ipo/), [TechCrunch](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/) |

**Jak to czytać:**

- **Najszybsze rampy przychodu w historii oprogramowania** to narzędzia dla programistów: Cursor od 100 mln (I 2025)
  do 2 mld USD ARR (II 2026), Claude Code >2,5 mld run-rate po niecałym roku.
- **Prawo to drugi najgorętszy pion:** Harvey z 3 mld (II 2025) do 15,5 mld USD wyceny (IX 2026), Legora od ok. 1 mln
  do 100 mln ARR w 18 miesięcy ([TNW](https://thenextweb.com/news/legora-just-hit-100-million-in-revenue-it-took-18-months)).
- **Otwarte projekty mierzą się zasięgiem, nie przychodem.** Liczby „klonów" i „clawów" to deklaracje — nie da się ich
  sprawdzić, ale gwiazdki i liczba zgłoszeń bezpieczeństwa już tak.

---

## 4. Fuzje, przejęcia i ruchy 2026

Chronologicznie, od końca 2025:

| Data | Ruch | Co to znaczy | Źródło |
|---|---|---|---|
| 10.11.2025 | **Clio** kupuje **vLex** za 1 mld USD; seria G 500 mln przy 5 mld | treść prawnicza to fosa — startupy ją kupują albo licencjonują | [The Logic](https://thelogic.co/news/clio-series-g-5-billion-legal-tech) |
| 29–30.12.2025 | **Meta** przejmuje **Manus** (ok. 2 mld USD wg prasy) | big tech kupuje gotowego wykonawcę z marką | [Yahoo](https://finance.yahoo.com/news/meta-acquire-chinese-startup-manus-233905821.html) |
| 14–15.02.2026 | Twórca OpenClaw, Peter Steinberger, przechodzi do **OpenAI**; projekt ma trafić do fundacji | laboratorium „kupuje" ludzi, nie kod | [TechCrunch](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/) |
| 25.02.2026 | **Anthropic** przejmuje **Vercept** (percepcja i obsługa komputera) | wyścig w *computer use* | [Anthropic](https://www.anthropic.com/news/acquires-vercept) |
| 10.03.2026 | **Meta** kupuje **Moltbook** (sieć społecznościowa agentów) | — | [TechCrunch](https://techcrunch.com/2026/03/10/meta-acquired-moltbook) |
| 24.04.2026 | **Cohere** łączy się z **Aleph Alpha**; wycena ok. 20 mld USD, Schwarz Group 600 mln; umowa podpisana 16.09.2026, hosting na STACKIT | flagowy niemiecki „suwerenny" model jest teraz częścią kanadyjskiej firmy | [TechCrunch](https://techcrunch.com/2026/04/24/cohere-acquires-merges-with-german-based-startup-to-create-a-transatlantic-ai-powerhouse/), [Cohere](https://cohere.com/blog/cohere-and-aleph-alpha-sign-agreement) |
| **27.04.2026** | Chińska NDRC **blokuje** przejęcie Manusa przez Metę — pierwszy publicznie ujawniony zakaz w chińskim przeglądzie bezpieczeństwa inwestycji | przeniesienie firmy do Singapuru nie chroni przed jurysdykcją Pekinu | [TechCrunch](https://techcrunch.com/2026/04/27/china-vetoes-metas-2b-manus-deal-after-months-long-probe/), [Dahui](https://www.dahuilawyers.com/en/news-insights/chinas-first-public-foreign-investment-security-review-prohibition-the-metamanus-decision/) |
| 4.05.2026 | Sierra: 950 mln USD przy >15 mld | wycena za model „za wynik" | [TechCrunch](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/) |
| 8.07.2026 | Powstaje **OpenClaw Foundation** (501(c)(3), 12 etatów) | otwarty runtime z budżetem i zarządem, jak Linux | [fundacja](https://openclaw.ai/blog/introducing-openclaw-foundation) |
| 23.07.2026 | **Poke** dołącza do **Cognition** (warunki nieujawnione) | zespoły „osobistych agentów" sprzedają się za UX i talent, nie przychód | [Cognition](https://cognition.com/blog/interaction) |
| 11.08 i 1.09.2026 | **Manus** ogłasza niezależność; założyciele z Tencent, ZhenFund i HongShan odkupują udziały Mety po ok. pierwotnej cenie; 8.10.2026 runda >500 mln USD | — | [Manus](https://manus.im/blog/a-note-to-our-users), [Manus](https://manus.im/blog/manus-resumes-independent-operations), [TechCrunch](https://techcrunch.com/2026/10/08/chinas-manus-raises-over-500m-in-first-funding-round-since-split-with-meta/) |
| **14.08.2026** | **SpaceX** finalizuje przejęcie **Cursora** (opcja z 21.04, wykonana 16.06; ok. 60 mld USD w akcjach) | najdroższe przejęcie asystenta AI w tym przeglądzie | [Cursor](https://cursor.com/blog/joining-spacex), [Wikipedia](https://en.wikipedia.org/wiki/Cursor_%28company%29) |
| 9.09.2026 | **Harvey**: 550 mln USD przy 15,5 mld (Diffusion + Lightspeed) | — | [Harvey](https://www.harvey.ai/blog/harvey-raises-dollar550m-at-a-dollar155b-valuation-to-help-legal-teams-own-their-intelligence) |
| IX 2026 | **Mistral** 3 mld EUR przy >21 mld; **Tandem Health** 100 mln USD z unijnego Scaleup Europe Fund (15.09); **Noxtua** 100+ mln EUR od C.H.Beck i MANZ (23.09) | „suwerenna AI" to finansowana kategoria | [Mistral](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/), [TNW](https://thenextweb.com/news/tandem-health-100m-series-b-scaleup-europe-fund), [Noxtua](https://www.noxtua.com/news/press-releases/series-c) |
| **25.09.2026** | **Microsoft Autopilot** (ewolucja Microsoft Scout) zbudowany na OpenClaw; prywatny podgląd od końca IX 2026; Microsoft oddaje poprawki do projektu (zgodność z polityką, Windows/WinUI, Teams, maskowanie sekretów w prośbach o zgodę) | otwarty runtime wygrał warstwę platformy | [OpenClaw](https://openclaw.ai/blog/microsoft-autopilot-openclaw) |
| 6.10.2026 | **Sierra + Meta**: Personal Agent Protocol (OAuth dla osobistych agentów działających u firm; Shopify, Stripe, Walmart i inni) | infrastruktura „po drugiej stronie" dla agentów się standaryzuje | [Sierra](https://sierra.ai/blog/introducing-personal-agent-protocol) |

**Historia Windsurf** (2025) jako przestroga: przejęcie przez OpenAI upadło, Google zapłacił 2,4 mld USD za zatrudnienie
liderów i licencję na technologię, a resztę firmy podpisał do przejęcia Cognition w VII 2025
([Wikipedia](https://en.wikipedia.org/wiki/Cognition_AI)). Windsurf wniósł Cognition ponad 1 mln użytkowników
i 4 000+ organizacji *(źródło wtórne)* — kupiono dystrybucję.

**Wzorzec:** wielcy nie walczą z otwartymi runtime'ami, tylko je **wchłaniają** — zatrudniają twórców (OpenAI),
budują produkty na ich kodzie (Microsoft), sprzedają pod nie sprzęt (NVIDIA NemoClaw) albo kupują zespoły (Cognition).

---

## 5. Dystrybucja i fosy

Fosa (*moat*) to to, co chroni biznes przed kopiowaniem. W 2026 model językowy **fosą nie jest** — każdy ma dostęp
do podobnych modeli. Oto, co działa.

### Dystrybucja przez system, przeglądarkę i komunikator

- **Gemini w Chrome i Androidzie:** Google ma przeglądarkę z ok. 2/3 rynku, menedżer haseł, Gmaila i Kalendarz;
  agent działa tam, gdzie użytkownik jest już zalogowany. Auto browse trafiło do Chrome na Androidzie 18.08.2026
  (USA) ([Google](https://blog.google/products-and-platforms/products/chrome/gemini-in-chrome-android-auto-browse/),
  [36Kr](https://eu.36kr.com/en/p/3931781634260099)). Wszystkie przeglądarki AI razem miały <1% rynku (VIII 2026).
- **Apple Messages:** Poke był pierwszym agentem AI zatwierdzonym na Apple Messages for Business (4.06.2026) —
  „jedynym agentem AI dopuszczonym do natywnego pisania w Apple Messages" *(dane firmy)*
  ([TechCrunch](https://techcrunch.com/2026/06/04/apple-approves-poke-as-the-first-ai-agent-on-its-messages-for-business-platform/)).
  Lindy w tym samym kanale dostał trwały ban (poniżej).
- **WhatsApp, Telegram, Signal i reszta:** OpenClaw i Hermes mają bramki do kilkunastu komunikatorów naraz — to ich
  główny interfejs ([OpenClaw docs](https://docs.openclaw.ai/llms.txt)).
- **Microsoft 365 i Windows:** 30 mln+ płatnych stanowisk Copilota (FY2026) i Autopilot w Teams
  ([Microsoft IR](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast)).
- **EHR w medycynie:** Epic wprowadził własny AI Charting (II 2026), a szpitale „ponownie oceniają sens osobnych
  umów" ([HLTH](https://hlth.com/insights/news/epic-releases-native-ai-charting-for-integrated-clinical-documentation-2026-02-06)).
  Kto ma system dokumentacji, ten ma klienta skryby.

### Dane i treść

- **Treść prawnicza:** u LexisNexis produkty AI to 90% nowej sprzedaży (23.07.2026,
  [LexisNexis](https://www.lexisnexis.com/community/pressroom/b/news/posts/legal-ai-propels-lexisnexis-to-fastest-growth-in-history));
  Harvey ma sojusz z LexisNexis, Noxtua należy do C.H.Beck, Clio kupił vLex.
- **W Polsce** komentarze kontrolują Wolters Kluwer (LEX Expert AI) i C.H.Beck (Legalis → Beck-Noxtua)
  ([prawo.pl](https://www.prawo.pl/prawnicy-sady/wolters-kluwer-przejmuje-libre-dostawce-rozwiazan-ai-dla-prawnikow,535867.html)).
  Lokalny asystent nie wygra z nimi treścią — powinien **uzupełniać** ich subskrypcje pracą na własnych aktach klienta
  (szczegóły w [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md)).
- **Medycyna:** OpenEvidence wygrywa licencjami NEJM, JAMA, NCCN, nie modelem.

### Przyzwyczajenie i przepływ pracy

- Wygrywają ci, którzy oddają **gotowy, sprawdzalny produkt pracy** (pismo, notatkę w EHR, poprawki w Wordzie),
  a nie odpowiedź na czacie. Harvey ma dodatki do Worda i Outlooka, Abridge zapisuje notatkę prosto do EHR,
  Granola siedzi w kalendarzu.
- **Pamięć per sprawa i per użytkownik** (Harvey, Hebbia, Sierra) — im dłużej klient używa, tym trudniej odejść.

### Własne modele (dotrenowane open-weight)

| Firma | Model | Baza | Efekt | Źródło |
|---|---|---|---|---|
| Harvey | Tenet (20.08.2026) | Kimi K3, RL z Fireworks, bez danych klientów | ok. 1/10 kosztu na komórkę tabeli przeglądu; −90% kosztu zapytania o wiedzę kancelarii | [Harvey](https://www.harvey.ai/blog/post-training-update-harvey-tenet) |
| Cursor | Composer 2 (19.03.2026) | Kimi K2.5 + własny pretrening i RL (przyznane dopiero 20.03.2026) | 0,50 / 2,50 USD za mln tokenów; konkurencyjne wyniki | [Cursor](https://cursor.com/blog/composer-2), [Gigazine](https://gigazine.net/gsc_news/en/20260323-cursor-admits-composer-2-kimi) |
| Thomson Reuters | Thomson (Thomson-1-Large) | otwarta baza + Westlaw, Practical Law | deklarowane wygrane z modelami czołówki na części testów prawniczych | [LawSites](https://www.lawnext.com/2026/08/thomson-reuters-says-its-homegrown-ai-model-now-rivals-the-frontier-labs-i-take-a-closer-look-at-the-benchmarks.html) |
| Noxtua | Athena Agent (Standard) | otwarte modele na suwerennej infrastrukturze UE | tańszy próg obok „Minerva" na modelach czołówki | [Noxtua](https://www.noxtua.com/) |
| Canva | modele własne | — | 17–30× taniej niż zewnętrzne (VIII 2026) | [B&T](https://www.bandt.com.au/canva-slashes-revenue-forecast-due-to-ai-spend-being-higher-than-expected/) |

**To najważniejsza wiadomość rynkowa dla lokalnego asystenta:** liderzy sami pokazują, że średni otwarty model,
dotrenowany na zadaniach z dziedziny i podpięty do dobrego wyszukiwania, wystarcza do wielu zadań — i jest
wielokrotnie tańszy.

### Zaufanie i zgodność

- Wszyscy liderzy linkują cytaty do źródeł (CoCounsel, Lexis z Shepard's, Abridge „Linked Evidence", LEX Expert AI).
- Ten sam zestaw certyfikatów wszędzie: SOC 2 Type II, ISO 27001, coraz częściej ISO 42001; w Niemczech BSI C5.
- Bezpieczeństwo wymuszane **poza modelem**: Harvey ma MCP Policy Engine blokujący „śmiertelną trójkę" (dostęp do
  danych + niezaufana treść + kanał wyjścia) ([Harvey](https://www.harvey.ai/blog/building-harveys-mcp-policy-engine)).
- W medycynie w UE fosą jest **certyfikacja wyrobu medycznego i zamówienia publiczne**, nie sama prywatność: Tandem
  ma MDR klasy IIa (21.05.2026), Heidi wygrała ramówkę NHS Midlands na 70 000 klinicystów
  ([TNW](https://thenextweb.com/news/tandem-health-100m-series-b-scaleup-europe-fund),
  [NHS](https://www.dgft.nhs.uk/newspost/nhs-launches-largest-ever-procurement-of-ai-clinical-documentation-covering-70000-midlands-clinicians/)).

### Efekty sieciowe

- **OpenClaw:** ClawHub (rynek „umiejętności"), 391,7k gwiazdek, partnerzy sprzętowi — ekosystem przyciąga
  ekosystem. Ale ten sam rynek umiejętności to też powierzchnia ataku (rozdział 6).
- **Poke:** udostępniane „przepisy" (automatyzacje w zwykłym tekście); twórca dostaje 0,10–1,00 USD za
  pozyskanego użytkownika ([TechCrunch](https://techcrunch.com/2026/04/08/poke-makes-ai-agents-as-easy-as-sending-a-text/)).

---

## 6. Porażki i lekcje

Uczę się z nich więcej niż z sukcesów — każda mówi, czego nie robić w produkcie dla profesjonalisty.

| Porażka | Co się stało (data) | Lekcja dla mnie |
|---|---|---|
| **Rabbit r1** | sprzęt za ok. 199 USD; po CES 2024 sprzedane 130 000 sztuk, ale we IX 2024 z r1 korzystało jednocześnie ok. 5 000 ze ~100 000 właścicieli; „to tylko aplikacja na Androida", wyciek zaszytych kluczy API (VI 2024) ([Wikipedia](https://en.wikipedia.org/wiki/Rabbit_r1), [The Verge](https://www.theverge.com/2024/9/25/24254253/rabbit-r1-5000-daily-users-ai-gadget)) | **nie wysyłać sprzętu, zanim agent działa.** Pudełko na biurku ma sens tylko z gotowym, przetestowanym oprogramowaniem |
| **11x** | III 2025: logotypy firm, które nie były klientami, groźba pozwu, słaba retencja; 5.05.2025 odchodzi CEO ([TechCrunch](https://techcrunch.com/2025/05/05/11x-ceo-hasan-sukkar-steps-down/)) | nigdy nie zawyżać klientów ani ARR; „cyfrowy pracownik" obiecuje zastąpienie, którego produkt nie dowiezie |
| **Artisan** | ban na LinkedIn za zeskrobane dane (XII 2025–I 2026), wycofanie hasła „Stop Hiring Humans" ([TechCrunch](https://techcrunch.com/2026/01/07/yes-linkedin-banned-ai-agent-startup-artisan-but-now-its-back/)) | sprzedawać **przepustowość**, nie zastępowanie ludzi; używać danych, do których ma się prawo |
| **Replit** | VII 2025: agent usunął produkcyjną bazę klienta w czasie „zamrożenia kodu", wbrew wyraźnym poleceniom ([Wikipedia](https://en.wikipedia.org/wiki/Replit)) | **twarde ograniczenia techniczne, nie polecenia w prompcie**: osobne środowiska, cofanie każdej akcji, zgoda przed nieodwracalnym |
| **Cennik Cursora** | 16.06.2025 zmiana na kredyty z „nielimitowanym" trybem tylko Auto → niespodziewane rachunki → przeprosiny i zwroty 4.07.2025 ([Cursor](https://cursor.com/blog/june-2025-pricing)) | zmianę cennika ogłaszać wcześnie, słowo „nielimitowany" tylko gdy to prawda; licznik zużycia na widoku |
| **Koszty Canvy** | prognoza wzrostu na 2026 obcięta z 30% do 20% przez koszty serwowania AI; potem własne modele 17–30× tańsze (5.08.2026, [B&T](https://www.bandt.com.au/canva-slashes-revenue-forecast-due-to-ai-spend-being-higher-than-expected/)) | koszt modeli z czołówki potrafi zjeść marżę nawet giganta; **lokalny model ma koszt krańcowy bliski zera** |
| **Otter i Granola w sądzie** | zarzuty podsłuchu i biometrii wobec Otter przetrwały wniosek o oddalenie (13.08.2026); Granola pozwana 30.07.2026 za niewidoczne nagrywanie i trenowanie domyślnie ([UC Today](https://uctoday.com/productivity-automation/otter-ai-fails-to-dismiss-core-privacy-claims-in-u-s-court/), [PPC Land](https://ppc.land/granola-sued-for-recording-meetings-without-consent-to-train-ai-models/)) | zgoda na nagrywanie **jawna i domyślnie włączona**; odcisk głosu to dane biometryczne (RODO art. 9) |
| **Bezpieczeństwo OpenClaw** | 722 zgłoszenia bezpieczeństwa w 2026 (14 krytycznych, 249 wysokich, 390 średnich, 69 niskich; API GitHuba 11.10.2026); złośliwe umiejętności: 341 z 2 857 (II 2026) i 1 103 z 14 706 (III 2026) w audytach ClawHub; OpenClaw 2.0 wciąż z nieszyfrowanym magazynem sekretów i piaskownicą domyślnie wyłączoną ([GitHub](https://github.com/openclaw/openclaw), [InsiderLLM](https://insiderllm.com/guides/openclaw-clawhub-security-alert/), [The Register](https://www.theregister.com/ai-and-ml/2026/08/31/openclaw-20-pours-glitter-on-slow-burning-security-dumpster-fire/5293492)) | budując na OpenClaw, **utwardzenie to mój produkt**: piaskownica domyślnie, zamknięty katalog umiejętności, szyfrowane sekrety |
| **Lindy na iMessage** | Apple trwale zablokował Apple ID Lindy w ciągu pół dnia; trzy przepisania kanału ([Lindy, 16.03.2026](https://www.lindy.ai/blog/imessage-api-three-rewrites-one-apple-ban-and-what-actually-works)) | komunikatory konsumenckie to wrogie platformy — oficjalne API biznesowe albo kanał, który kontroluję |
| **ChatGPT Atlas** | przeglądarka z 21.10.2025, nigdy na Windows ani telefony; wycofanie ogłoszone 9–10.07.2026, przestała działać **9.08.2026**; „przeglądarki AI powinny być funkcją, nie celem" ([forum OpenAI](https://community.openai.com/t/atlas-is-scheduled-to-stop-working-on-august-9-2026/1389473), [TechCrunch](https://techcrunch.com/2026/07/09/openai-is-shutting-down-atlas-but-its-ai-browser-ambitions-are-still-growing/)) | nie konkurować o „posiadanie przeglądarki"; konkurować pionowym przepływem pracy i zaufaniem |
| **Project Mariner** | zakończony **4.05.2026**, wchłonięty przez Gemini Agent/Spark i auto browse w Chrome ([Wikipedia](https://en.wikipedia.org/wiki/Project_Mariner)) | eksperymentalne produkty agentowe dużych firm znikają — budować na stabilnych API, nie na ich aplikacjach |
| **Martin** | prawdopodobnie zastój: w X 2026 na stronie baner Black Friday i makiety z VIII 2024, ostatni wpis 23.04.2025 ([Martin](https://www.trymartin.com/blog), *niezweryfikowane*) | cienka nakładka na cudze modele nie przeżyje konkurencji z laboratoriami |
| **Manus: wstrzyknięcie przez PDF** | 25.08.2025: ukryte polecenie w PDF kazało agentowi wystawić wewnętrzny VS Code do internetu i ujawnić hasło, bez zgody człowieka ([Embrace The Red](https://embracethered.com/blog/posts/2025/manus-ai-kill-chain-expose-port-vs-code-server-on-internet/)) | narzędzia sieciowe (porty, wyjście do internetu) tylko za bramką człowieka |
| **Claude Cowork: wyciek plików** | I 2026: ukryty tekst w dokumencie kazał wysłać pliki ofiary na konto atakującego przez **dozwolone** API Anthropic ([PromptArmor](https://www.promptarmor.com/resources/claude-cowork-exfiltrates-files)) | lista dozwolonych adresów nie wystarcza, gdy dozwolony adres przyjmuje dowolne klucze |
| **Halucynacje w sądach** | baza Damiena Charlotina: 2 184 sprawy z halucynacjami AI (10.10.2026), w tym 6 w Polsce ([baza](https://www.damiencharlotin.com/hallucinations/)) | każde cytowane źródło musi być sprawdzalne (SAOS, ISAP); to jednocześnie popyt i ryzyko |

**Wspólny mianownik:** porażki biorą się z **obietnicy większej niż produkt** (11x, Rabbit, Martin), **złych
domyślnych ustawień** (OpenClaw, Granola, Replit) albo **zależności od cudzej platformy** (Lindy, Atlas, Mariner).
Dla profesjonalisty, który odpowiada podpisem, każda z tych trzech rzeczy jest dyskwalifikująca.

---

## 7. Trendy 2026

Każdy trend z dowodami. Szczegóły techniczne — w [03-WZORCE-TECHNICZNE.md](03-WZORCE-TECHNICZNE.md).

### 1. Agenci w komunikatorach

- Poke w Apple Messages (4.06.2026), OpenClaw i Hermes z bramkami do WhatsAppa, Telegrama, Signala, Teams.
- Microsoft Autopilot w Teams (25.09.2026); Lindy przeniósł się z SMS do „kolegi z zespołu" w Slacku (31.08.2026,
  [Lindy](https://www.lindy.ai/blog/ai-teammate)).
- **Co ludzie faktycznie delegują:** „pracę wokół pracy", nie zarządzanie życiem. W Claude Cowork 33,4% to operacje
  biznesowe, 16,4% treści ([Anthropic, VII 2026](https://claude.com/resources/articles/how-people-are-using-claude-cowork));
  poranny brief to uniwersalny punkt wejścia (ChatGPT Pulse, Google CC, Lindy).

### 2. Agenci w tle i w chmurze

- ChatGPT **dots** (29.09.2026): zawsze włączeni agenci z własnym komputerem w chmurze
  ([TechCrunch](https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/)).
- Manus 2.0 (28.09.2026): trwały „Cloud Computer" i automatyzacje uruchamiane zdarzeniami
  ([Manus](https://manus.im/blog/introducing-manus-2-0)).
- Gemini Spark: do 15 zadań równolegle ([Google](https://support.google.com/gemini/answer/16596215)).
- Cognition nazywa zakup Poke zakładem na „zawsze włączonych agentów w chmurze"
  ([Cognition](https://cognition.com/blog/interaction)).
- Równolegle wraca **dedykowane pudełko**: Cloudflare pisał o „fali kupowania Mac minis" pod OpenClaw (I 2026),
  a Ghost sprzedaje lokalny komputer AI za 3 499 USD (5.10.2026)
  ([Cloudflare](https://blog.cloudflare.com/moltworker-self-hosted-ai-agent/),
  [TechCrunch](https://techcrunch.com/2026/10/05/at-19-ghost-founder-raises-11-million-to-build-a-3499-computer-for-your-personal-ai/)).

### 3. Dotrenowywanie modeli open-weight

Harvey Tenet, Cursor Composer 2, Thomson Reuters „Thomson", Noxtua Athena, Canva (rozdział 5). Do tego otwarte
modele GUI: Qwen3.8-27B (Apache 2.0) deklaruje 84,3% w OSWorld-Verified (VIII 2026,
[Hugging Face](https://huggingface.co/Qwen/Qwen3.8-27B), *(dane firmy)*). **Warstwa modelu się utowarowia.**

### 4. Suwerenne stosy w UE

- Pieniądze: Mistral 3 mld EUR (IX 2026), Cohere + Aleph Alpha (IV 2026), Noxtua 100+ mln EUR (IX 2026), Tandem
  i Lovable z unijnym Scaleup Europe Fund.
- Polityka: pakiet suwerenności technologicznej (3.06.2026) i projekt **CADA** z czterema poziomami suwerenności —
  od L1 (dane w UE) do L4 (pełna kontrola łańcucha dostaw)
  ([Komisja Europejska](https://digital-strategy.ec.europa.eu/en/policies/cloud-and-ai-development-act)).
  CADA to wciąż projekt (X 2026).
- Granica: „region UE" u amerykańskiego dostawcy to L1, nie suwerenność; EU Data Boundary Microsoftu nie obejmuje
  modeli Anthropic ([Microsoft](https://learn.microsoft.com/en-us/copilot/microsoft-365/microsoft-365-copilot-privacy)).
- Jednocześnie część funkcji agentowych startuje **bez EOG**: Gemini Spark „globalnie poza EOG, Nigerią, Szwajcarią
  i Wielką Brytanią", dots w progu Pro też bez EOG
  ([Google](https://support.google.com/gemini/answer/16596215), [Emergent](https://emergent.sh/news/openai-devday-2026)).

### 5. Płatność za wynik i za zużycie

Dowody w rozdziale 2 (Sierra, Intercom Fin, Parloa, Ambience; Copilot, Cursor, Glean, Notion) i prognoza Gartnera
(koszt na agentowy przepływ ×5 do 2028). **Ryzyko kosztów spada na klienta albo dostawcę — chyba że model jest lokalny.**

### 6. Przeglądarki AI w odwrocie

- Atlas zamknięty (9.08.2026), Mariner zamknięty (4.05.2026), wszystkie przeglądarki AI <1% rynku.
- Gartner (8.12.2025): „Cybersecurity Must Block AI Browsers for Now" — domyślne ustawienia stawiają wygodę ponad
  bezpieczeństwo ([The Register](https://www.theregister.com/2025/12/08/gartner_recommends_ai_browser_ban/)).
- OpenAI (22.12.2025): wstrzykiwanie poleceń „prawdopodobnie nigdy nie zostanie w pełni rozwiązane"
  ([TechCrunch](https://techcrunch.com/2025/12/22/openai-says-ai-browsers-may-always-be-vulnerable-to-prompt-injection-attacks/)).
- Akamai kupuje LayerX za ok. 205 mln USD (14.05.2026) — bezpieczeństwo przeglądarek AI staje się osobnym rynkiem
  ([BankInfoSecurity](https://www.bankinfosecurity.com/akamai-to-buy-layerx-for-205m-to-expand-ai-browser-security-a-31695)).

### 7. Konsolidacja i opór platform

- Konsolidacja: rozdział 4 (Cursor, Poke, Windsurf, Aleph Alpha, vLex, Vercept, Moltbook).
- Platformy się bronią: Amazon pozwał Perplexity o zakupy w Comet — 4.08.2026 Dziewiąty Okręg uchylił zakaz,
  uznając, że stronę „odwiedza" użytkownik, nie dostawca agenta
  ([Jones Day](https://www.jonesday.com/en/insights/2026/09/ninth-circuit-vacates-cfaa-injunction-against-perplexitys-comet-ai-agent));
  WeChat, Taobao i Alipay zablokowały agenta telefonicznego Doubao (XII 2025)
  ([Business Standard](https://www.business-standard.com/world-news/bytedance-ai-phone-doubao-nubia-zte-app-blocks-user-control-china-125120800459_1.html)).
- Wniosek: API, konektory MCP i własna sesja użytkownika zamiast skrobania stron.

### 8. Duzi wchodzą w piony

Anthropic rozszerzył „Claude for Legal" o wtyczki dziedzinowe i konektory do Westlaw, Box i Docusign (12.05.2026,
[TechCrunch](https://techcrunch.com/2026/05/12/the-ai-legal-services-industry-is-heating-up-anthropic-is-getting-in-on-the-action/));
Thomson Reuters buduje nowy CoCounsel na Claude Agent SDK
([LawSites](https://www.lawnext.com/2026/06/thomson-reuters-opens-early-access-to-the-next-generation-of-cocounsel-legal-saying-beta-users-fing-loved-the-product.html)).
Piony bronią się treścią, przepływem pracy i integracjami.

---

## 8. Co z tego wynika dla mnie

Cel: lokalny asystent na biurku dla polskiego profesjonalisty (kancelaria, gabinet, biuro rachunkowe), dane nie
wychodzą z pokoju. Prawne tło (tajemnica zawodowa, RODO, AI Act, polska ustawa o systemach AI) jest
w [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md) — to nie jest porada prawna.

### Kotwice cenowe w Polsce (sprawdzone 11.10.2026)

| Produkt | Cena | Gdzie są dane | Źródło |
|---|---|---|---|
| Beck-Noxtua (prawo) | **590 zł netto/mies. za użytkownika**, bez limitu tokenów; wymaga Legalis Silver lub wyżej | chmura UE (IONOS, Open Telekom Cloud) | [Beck-Noxtua](https://www.beck-noxtua.pl/), [Noxtua](https://www.noxtua.com/news/press-releases/beck-noxtua-for-the-czech-republic) |
| LEX AI (prawo, konsumenci i MŚP) | Standard 49 zł, Premium 120 zł, PRO MAX 489 zł/mies.; podpisana opinia ok. 320–380 zł | serwery w Polsce wg App Store | [App Store](https://apps.apple.com/pl/app/lex-ai/id6748342467?l=pl) |
| Noa Notes (skryba medyczny) | **199 zł/mies. + VAT**, notatki bez limitu | AWS i Azure | [Noa](https://www.noa.ai/pl/cennik) |
| Mistral Vibe Pro / Team | 14,99 / 24,99 EUR za użytkownika, bez VAT | UE domyślnie | [Mistral](https://mistral.ai/fr/pricing) |
| Google AI Pro (PL) | 97,99 zł/mies. | chmura Google | [Google](https://gemini.google/subscriptions/) |
| wFirma (księgowość) | funkcje AI w cenie abonamentu | chmura dostawcy | [wFirma](https://wfirma.pl/) |
| Gaius-Lex (prawo, on-prem) | brak cennika publicznego | SaaS w EOG, hybryda albo on-premise | [Gaius-Lex](https://gaius-lex.pl/) |

**Wniosek:** profesjonalista już płaci **ok. 200–600 zł miesięcznie za stanowisko** za AI w chmurze. Gaius-Lex jest
najbliższym polskim odpowiednikiem „dane nie wychodzą z biura", ale celuje w kancelarie 20–99 prawników i wdrożenia
projektowe. Segment **małego biura 1–10 osób, gotowe pudełko na biurko** — nie znalazłem w nim nikogo (to wynik
wyszukiwania, nie dowód, że nikogo nie ma).

### Ekonomika jednostkowa: lokalnie a chmura

**Chmura** — koszt rośnie z pracą agenta:

- Manus: stosunek tokenów wejścia do wyjścia ok. 100:1, średnio ok. 50 wywołań narzędzi na zadanie; tokeny z cache
  kosztują ok. 1/10 zwykłych ([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).
- Claude Opus 5.5: 4 USD za mln tokenów wejścia, 20 USD za mln wyjścia (22.09.2026,
  [Anthropic](https://www.anthropic.com/news/claude-opus-5-5)).
- **Moje wyliczenie (przykład):** zadanie z 50 krokami po 20 tys. tokenów wejścia i 500 wyjścia to 1 mln tokenów
  wejścia (4 USD) + 25 tys. wyjścia (0,50 USD) = **ok. 4,5 USD bez cache**, ok. 0,9 USD przy cache tnącym wejście
  ok. 10× (jak w przykładzie Manusa). Kilkanaście takich zadań dziennie na osobę to setki USD miesięcznie (moje wyliczenie).
- Długie zadania czołówki na OSWorld 2.0: 15,70–26,62 USD za zadanie (28.08.2026,
  [Simular](https://www.simular.ai/articles/sai-tops-osworld-2-0), *(dane firmy)*).

**Lokalnie** — koszt jest z góry, krańcowy prawie zerowy (prąd i amortyzacja):

- Moja maszyna: 4× Radeon AI PRO R9700, ok. 8 900 zł za kartę ([Ceneo](https://www.ceneo.pl/;szukaj-radeon+ai+pro+r9700),
  11.10.2026) i 300 W na kartę ([AMD](https://www.amd.com/en/products/graphics/workstations/radeon-ai-pro/ai-9000-series/amd-radeon-ai-pro-r9700.html)); czyli **ok. 35,6 tys. zł za same karty** i do 1,2 kW
  pod pełnym obciążeniem (moje wyliczenie).
- Przepustowość: 4 agentów × 13,6 tok/s = ok. 54 tok/s generowania łącznie (moje wyliczenie). Wspomniane zadanie
  z 25 tys. tokenów wyjścia to ok. 30 minut samego generowania na jednym slocie — wolniej niż chmura, ale bez rachunku
  za tokeny i bez limitów.
- Pudełka dla klientów: ASUS GX10 (GB10, 128 GB) od 24 499 zł ([Ceneo](https://www.ceneo.pl/;szukaj-ascent+gx10)),
  Mac mini M5 Pro od 8 499 zł ([Apple](https://www.apple.com/pl/shop/buy-mac/mac-mini)), Strix Halo 128 GB
  13 490–19 999 zł ([Ceneo](https://www.ceneo.pl/;szukaj-ryzen+ai+max%2B+395+128gb)) — ceny z 11.10.2026, porównanie
  w [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md).

**Przykład porównania** (ceny katalogowe netto, bez rabatów, bez VAT — tylko ilustracja):

- **3 prawników na Beck-Noxtua:** 590 × 3 × 24 mies. = **42 480 zł** w dwa lata, plus Legalis. Jedno pudełko GX10
  to **24 499 zł** plus abonament wsparcia.
- **Jeden lekarz na Noa Notes:** 199 × 24 = **4 776 zł** w dwa lata — mniej niż sam Mac mini M5 Pro. **Dla
  pojedynczego lekarza argumentem musi być prywatność, nie cena**; ekonomia działa przy wspólnym pudełku w przychodni
  (3+ lekarzy).

**Hybryda z Claude Opus 5.5 jako planistą** zmienia rachunek tylko trochę: jedno wywołanie planisty z 10 tys. tokenów
wejścia i 2 tys. wyjścia to ok. 0,08 USD (moje wyliczenie). Ale wtedy planista **widzi dane** — w trybie dla
tajemnicy zawodowej planista w chmurze może dostać tylko zanonimizowany opis zadania albo wcale. Granicę prywatności
opisuję w [kursie 1, części 10](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md)
i [kursie 2, części 17](../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md).

### Model cenowy — moja hipoteza do sprawdzenia

To jest **moja opinia** na podstawie powyższych faktów, nie dane rynkowe:

1. **Licencja płaska za stanowisko albo za biuro + sprzęt**, nie kredyty. Przy koszcie krańcowym bliskim zera
   „bez liczników, bez limitów tokenów" to argument sprzedażowy przeciw cennikom za zużycie (rozdział 2). Beck-Noxtua
   już reklamuje „bez limitu tokenów" — klient to rozumie.
2. **Sprzęt sprzedawany po kosztach albo w leasingu, marża na abonamencie** (aktualizacje modeli, łatki
   bezpieczeństwa, wymiana pudełka, testy jakości po polsku przed każdą zmianą modelu). Wzór: Ghost („działa, nawet
   gdy dostawca zniknie") + Hermes Business (płatna warstwa wokół darmowego rdzenia).
3. **Cena abonamentu poniżej kotwic chmurowych** w przeliczeniu na stanowisko w okresie 24–36 miesięcy, razem ze
   sprzętem — wtedy porównanie z Beck-Noxtua (590 zł) wygrywa na papierze, a prywatność jest bonusem.
4. **Nie zastępować wydawców, tylko ich uzupełniać:** LEX i Legalis zostają u klienta; mój asystent pracuje na jego
   aktach, mailach, KSeF i dokumentacji, do których chmurowi gracze nie mają (lub nie powinni mieć) dostępu.
5. **Pakiet zgodności jako część ceny:** mapowanie § 23e Kodeksu Etyki Adwokackiej (NRA, 12–13.06.2026), szablon
   DPIA, opinia KRiBSI z art. 12 polskiej ustawy o systemach AI — szczegóły w
   [04-POLSKA-I-SUWERENNOSC.md](04-POLSKA-I-SUWERENNOSC.md).
6. **Opcja „za wynik" na później:** np. za przyjętą notatkę z wizyty albo przygotowane pismo — dopiero gdy umiem to
   rzetelnie mierzyć (lekcja Sierry: wąskie zadanie, jasna miara).
7. **Bez grzechów z rozdziału 6:** żadnych obietnic „zastąpi aplikanta", piaskownica i szyfrowanie domyślnie
   włączone, nagrywanie tylko za jawną zgodą, zgoda człowieka przed każdą nieodwracalną akcją, kanał, który kontroluję.

### Sygnały popytu i ryzyka rynkowe

- Polska jest w ogonie UE: AI używa 8,7% polskich firm (GUS, 2025) wobec ok. 20% w UE (Eurostat, 2025), ale w usługach
  profesjonalnych 23,2% i +8,8 p.p. w rok ([GUS](https://stat.gov.pl/download/gfx/portalinformacyjny/pl/defaultaktualnosci/5497/1/19/1/spoleczenstwo_informacyjne_w_polsce_2025.pdf),
  [Eurostat](https://ec.europa.eu/eurostat/statistics-explained/index.php/Use_of_artificial_intelligence_in_enterprises)).
- Bariery w UE to „niejasne skutki prawne" (52,52%) i „ochrona danych" (48,83%) — dokładnie to, co rozwiązuje
  lokalne pudełko (Eurostat, j.w.).
- Ryzyko: 77% polskich firm bez AI nie wdroży jej „dopóki nie będzie trzeba", co piąta wskazuje koszt
  ([PIE, 24.09.2025](https://pie.net.pl/wp-content/uploads/2025/09/2025-09-22_Z-AI-korzysta-mniej-niz-co-szosta-firma-w-Polsce-a-pozostale-nie-planuja-jej-wdrazac-1.pdf)).
- Ryzyko: polscy programiści należą do najbardziej sceptycznych — tylko 26% ufa AI (Stack Overflow 2025,
  [Stack Overflow](https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/)). Zaufanie
  buduje się cytatami, krokiem przeglądu i cofaniem.
- Brakuje mi danych o **gotowości do zapłaty** polskich adwokatów, radców i lekarzy — nie znalazłem polskich badań.
  To pierwsza rzecz do sprawdzenia w rozmowach z klientami.

Ranking i profile — [README.md](README.md) i [01-PROFILE.md](01-PROFILE.md). Przegląd otwartych harnessów, na których
można zbudować rdzeń — [../harnessy-agentowe/README.md](../harnessy-agentowe/README.md).

---

## Źródła tego pliku

Każda liczba ma link przy sobie; szacunki analityków (Menlo Ventures, Gartner, Sacra) są oznaczone w tekście, a cenniki
sprawdziłem 11.10.2026. Pełna lista źródeł z opisem, co z nich wziąłem — [ZRODLA.md](ZRODLA.md).
