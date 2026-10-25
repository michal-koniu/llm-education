# Część 01 · Podstawy wyceny: trzy liczby, nie jedna

> **Cel tej części.** Przestajesz myśleć o „cenie” jak o jednej liczbie, którą się zgaduje. Poznajesz
> trzy liczby, między którymi leży każda cena — **podłogę kosztową, wartość referencyjną i wartość
> ekonomiczną** — oraz kolejność, w jakiej ten kurs zmierzy je dla prywatnego AI boxa.
>
> **Czas:** ~3 h · **Poziom:** ⭐⭐ · **Wynik:** `pricing/00-gut-price.md`, `pricing/01-anchors.md`

---

## 0. Problem

Repo zawiera już cenę boxa. W `asymetrie-biznesowe-ai/02-OKAZJE.md` stoi:
*„25 000–60 000 zł za wdrożenie wraz ze sprzętem, 800–2 500 zł miesięcznie … (moje założenie, do
sprawdzenia, nie dane rynkowe).”* To uczciwe zdanie, a zarazem typowa cena inżyniera: przedział na tyle
szeroki, żeby był bezpieczny (rozrzut 2,4× na wdrożeniu, 3,1× na abonamencie), i wyprowadzony z tego, ile
kosztuje sprzęt, plus „coś za mój czas”.

Tak ustalona cena ma trzy problemy:

1. **Zaczyna się od Twojego kosztu.** Klient nie wie i nie obchodzi go, ile kosztował Cię box. Porównuje
   Twoją cenę z tym, co zrobiłby zamiast tego, i z tym, ile box jest dla niego wart.
2. **To jedna liczba dla wszystkich.** Dwuosobowa kancelaria notarialna i dziesięcioosobowa kancelaria
   prawna dostają z tego samego boxa zupełnie inną wartość.
3. **Nie da się jej obalić.** „800–2 500” przetrwa każdą rozmowę. Cena, której błędności nie da się
   wykazać, niczego Cię nie uczy.

Ten kurs zastępuje zgadywanie trzema zmierzonymi liczbami i jedną przetestowaną decyzją.

---

## 1. Dlaczego cena zasługuje na cały kurs

Cena to najsilniejsza dźwignia zysku, jaką kontrolujesz — i ta, której inżynierowie poświęcają najmniej czasu.

| Badanie | Zmiana o 1% w… | Wpływ na zysk | Źródło |
| :-- | :-- | :-- | :-- |
| Marn & Rosiello, HBR 1992 (duże firmy) | cenie | **+11,1%** zysku operacyjnego | pierwotne (HBR) |
| | wolumenie sprzedaży | +3,3% | |
| ProfitWell / Paddle, 512 firm SaaS | monetyzacji (wycenie) | **+12,7%** wyniku netto | *dane własne dostawcy* |
| | retencji | +6,7% | |
| | pozyskiwaniu klientów | +3,3% | |

Mechanizm to prosta arytmetyka. Jeśli Twoja marża jest cienka, mała zmiana ceny to duża część zysku. Jeśli
sprzedajesz box z marżą brutto 20%, podniesienie ceny o 5% podnosi Twój zysk brutto o 25%.

**Dla Ciebie oznacza to:** godzina spędzona na wycenie przed pierwszą sprzedażą jest warta więcej niż
godzina spędzona na czwartym agencie. To nie jest opinia o biznesie; to proporcja z tabeli.

---

## 2. Trzy liczby

Każda cena leży między podłogą a sufitem.

```
 PLN / miesiąc za kancelarię
   │
   │   ┌──────────────────────────────┐  ← WARTOŚĆ EKONOMICZNA (sufit)
   │   │  wartość zróżnicowania        │     ile box jest wart dla TEJ kancelarii:
   │   │  (zaoszczędzony czas, usunięte│     alternatywa + to, co lepsze w Twoim
   │   │   ryzyko, rzeczy, których     │
   │   │   alternatywa nie potrafi)    │
   │   ├──────────────────────────────┤  ← WARTOŚĆ REFERENCYJNA
   │   │  najlepsza alternatywa        │     ile zapłaciliby zamiast tego
   │   │  (stanowiska Beck-Noxtua,     │     (albo koszt robienia tego ręcznie)
   │   │   Copilot, godziny aplikanta) │
   │   └──────────────────────────────┘
   │          ↕ Twoja cena mieszka gdzieś tutaj
   │   ════════════════════════════════  ← PODŁOGA KOSZTOWA
   │                                        Twój koszt obsługi jednej kancelarii ÷ (1 − docelowa marża)
   └────────────────────────────────────
```

### 2.1 Podłoga kosztowa — część 02

Twój koszt obsługi jednej kancelarii przez jeden miesiąc: godziny wsparcia, aktualizacje modeli, monitoring,
sprzęt, jeśli jest Twój. Podziel go przez `(1 − docelowa marża brutto)` i dostajesz najniższą cenę, przy
której biznes działa. **Poniżej podłogi tracisz pieniądze na każdym kliencie. Powyżej niej wybierasz już
tylko, jaką część wartości bierzesz dla siebie.**

Podłogę inżynierowie liczą dobrze. Pułapka polega na tym, żeby na niej poprzestać i dodać narzut.

### 2.2 Wartość referencyjna — część 03

Ile kancelaria zapłaciłaby za **najlepszą alternatywę**. Nagle i Müller (*The Strategy and Tactics of
Pricing*, 6. wyd., 2018) nazywają to wartością referencyjną. Dla Twojego kupującego może to być:

- chmurowe AI prawnicze płatne za stanowisko (kotwice z repo: Beck-Noxtua 590 zł netto za użytkownika
  miesięcznie, progi LEX AI 49–489 zł miesięcznie, sprawdzone 11 października 2026 w `asystenci-ai/02-RYNEK.md`);
- asystent ogólny: Microsoft 365 Copilot 30 USD za użytkownika miesięcznie; Copilot Business dla maksymalnie 300
  użytkowników 21 USD cennikowo od 1 grudnia 2025 (Computerworld), 18 USD w promocji do 31 grudnia 2026
  (źródła wtórne); ChatGPT Business 20–25 USD i Claude Team 20–25 USD za standardowe stanowisko;
- **robienie tego ręcznie** — godziny aplikanta albo asystenta. Dla wielu małych kancelarii to jest prawdziwa
  alternatywa, bo narzędzia chmurowe nie przechodzą testu tajemnicy zawodowej.

### 2.3 Wartość ekonomiczna — część 03

Wartość referencyjna **plus wartość zróżnicowania**: to, co jest lepsze (albo gorsze — może być ujemna)
w Twoim boxie w porównaniu z tą alternatywą. Dla boxa dodatnie zróżnicowanie jest konkretne:

- dane nigdy nie opuszczają pokoju (tajemnica zawodowa, RODO, brak ekspozycji na CLOUD Act — argument
  z `asystenci-ai/04-POLSKA-I-SUWERENNOSC.md`);
- brak licznika za stanowisko, brak limitu tokenów;
- polskie procesy pracy na własnych plikach kancelarii;
- dziennik audytowy, który kancelaria może pokazać swojej izbie adwokackiej albo klientowi.

Ujemne zróżnicowanie też istnieje i musisz je odjąć: sprzęt w biurze, mniejszy model niż chmurowa czołówka,
jednoosobowy dostawca (Ty), wysiłek instalacji.

**Wartość ekonomiczna to sufit.** Żaden racjonalny kupujący nie zapłaci więcej niż alternatywa plus
przewaga netto. Cena, na którą klient mówi „tak” bez długiego wahania, zwykle zgarnia **ułamek** wartości
zróżnicowania — resztę zostawiasz mu jako powód do zmiany. Część 03 liczy ten ułamek za pomocą
`narzedzia/pricing_model.py value`.

---

## 3. Cena to decyzja produktowa, a nie sprzedażowa

Madhavan Ramanujam i Georg Tacke (*Monetizing Innovation*, Wiley, 2016; obaj z Simon-Kucher) twierdzą, że
większość nowych produktów upada na monetyzacji, a rozwiązaniem jest **zaprojektować produkt wokół ceny** —
przeprowadzić rozmowę o gotowości do zapłaty *zanim* zaczniesz budować. Ich cztery tryby porażki przekładają
się wprost na box:

| Tryb porażki | Co oznacza | Jak wygląda w przypadku AI boxa |
| :-- | :-- | :-- |
| **Feature shock** (szok funkcji) | za dużo funkcji, nikt nie rozumie wartości, cena wydaje się za wysoka | box z 15 agentami, chatbotem, OCR, kalendarzem i RAG-iem po wszystkim — prawnik widzi „projekt IT” |
| **Minivation** (mini-innowacja) | właściwy produkt wyceniony za nisko; pieniądze zostawione na stole | box sprzedany po cenie sprzętu plus trochę, bo „to małe kancelarie” |
| **Hidden gem** (ukryty klejnot) | cenna funkcja, której nikt nie sprzedaje, bo nie dostrzegłeś jej wartości | **pakiet dziennika audytowego i zgodności z tajemnicą zawodową** — dla kancelarii podlegającej samorządowi zawodowemu być może wart więcej niż same agenty |
| **Undead** (nieumarły) | produkt, którego nikt nie chce za żadną cenę | „serwer z chatbotem” — generyczny box, który samo repo już odrzuciło |

Dwa kolejne ich narzędzia pojawią się dalej w kursie:

- **Podział funkcji na lider / wypełniacz / zabójca (leader / filler / killer)** (część 04): *liderzy*
  napędzają zakup, *wypełniacze* to miłe dodatki, *zabójców* chce mniej niż 20% kupujących, a ponad 20%
  aktywnie ich nie lubi — nigdy nie wolno ich wciskać do pakietu.
- **Cele pakietowania good / better / best (dobry / lepszy / najlepszy)** (część 04): poniżej 30% kupujących
  na Good, ponad 70% na Better lub Best, ponad 10% na Best. Ponad połowa kupujących na najniższym progu to
  sygnał ostrzegawczy, że próg wejściowy jest za dobry albo wyższe progi za słabe.

---

## 4. Co naprawdę sprzedaje AI box

Zanim wycenisz, nazwij **pracę**, za którą płaci kancelaria. Analiza kosztów w repo
(`asymetrie-biznesowe-ai/03-NAJPIERW-LOKALNIE.md`, sekcja 4) daje uczciwą odpowiedź: *„w porównaniu z tanimi
modelami przez API lokalny sprzęt nie zwraca się na tokenach przy wolumenach małej kancelarii … wyceniaj box
jako zgodność i kontrolę, nie jako oszczędność.”*

Box **nie** sprzedaje więc tokenów, mocy obliczeniowej ani „AI”. Sprzedaje trzy rzeczy:

1. **Pozwolenie** — kancelaria w ogóle może używać AI na aktach klientów, nie naruszając tajemnicy. Bez boxa
   alternatywą dla tej pracy jest często „bez AI”.
2. **Odzyskane godziny** — konkretne procesy (segregacja przychodzącej korespondencji, porównywanie umów,
   propozycje terminów) zrobione w minuty zamiast w godzinę.
3. **Spokój** — ktoś inny dba o aktualizacje, pomiary i łatki, a wszystko jest w dzienniku.

Każda z nich podsuwa inny sposób pobierania opłat (część 04): pozwolenie sugeruje stałą opłatę za kancelarię,
odzyskane godziny — wycenę za proces albo za agenta eksperckiego, spokój — abonament utrzymaniowy. Twój pakiet
połączy je wszystkie.

---

## 5. Jak produkty AI pobierają opłaty w latach 2025–2026

Rynek ruszył szybko. Nie potrzebujesz z niego mody do skopiowania, tylko wyczucia, do czego kupujący są już
przyzwyczajeni i co poszło nie tak.

| Model | Przykład (ze źródłem) | Czego Cię uczy |
| :-- | :-- | :-- |
| **Za stanowisko** | Microsoft 365 Copilot 30 USD/użytkownik/mies.; Copilot Business 21 USD cennikowo (od 1 grudnia 2025, Computerworld), 18 USD w promocji do końca 2026. Clio publikuje EasyStart za 49 USD/użytkownik/mies. i dokłada AI do wyższych progów | Kupujący to rozumieją. Model karze Cię, gdy AI zastępuje stanowiska, a 3-osobowa kancelaria to mała sprzedaż |
| **Za zużycie / kredyty** | Salesforce Agentforce: 2 USD za rozmowę → Flex Credits 500 USD za 100 tys. kredytów (ok. 0,10 USD za akcję) → dodatki per użytkownik 125 USD/mies. (strona cennika Salesforce) | Nawet Salesforce trzy razy zmieniał licznik. Mały kupujący nie umie zabudżetować licznika |
| **Bunt przeciw opłatom za zużycie** | Cursor, 16 czerwca 2025: plan Pro przeszedł na pulę zużycia; firma przeprosiła i zwróciła opłaty za okres 16 czerwca–4 lipca (blog Cursora). Wycena Replita oparta na nakładzie pracy (effort-based): użytkownicy zgłaszali ~1 000 USD w tydzień wobec ~200 USD miesięcznie wcześniej (The Register, 18 września 2025) | **Nieprzewidywalne rachunki niszczą zaufanie szybciej niż wysokie ceny** |
| **Za efekt** | Intercom Fin 0,99 USD za rozwiązaną sprawę, minimum 50 miesięcznie (strona cennika Intercom). Sierra pobiera opłaty za zrealizowane efekty i podała 100 mln USD rocznego przychodu powtarzalnego (ARR) w listopadzie 2025 (*dane własne firmy*) | Działa, gdy efekt jest wąski i mierzalny |
| **Kontrprzykład** | Decagon twierdzi, że „zdecydowana większość” jego klientów wybrała opłatę za rozmowę zamiast za rozwiązanie, dla przewidywalności (*dane własne firmy*) | Nawet gdy wycena za efekt jest w ofercie, kupujący często wolą to, co potrafią przewidzieć |
| **Sprzęt + abonament** | Lemony AI: 499 USD/mies. za box, aktualizacje i wsparcie, do 5 użytkowników; runda seed 2 mln USD (TechCrunch, czerwiec 2025) | **Najbliższy odpowiednik Twojego produktu.** Około 1 900 PLN miesięcznie przy założonym kursie 3,8 PLN/USD |

**Ankiety** (wszystkie to dane własne firm, które odpowiedziały):

- Growth Unhinged 2025 (ponad 240 firm): wycena hybrydowa (opłata bazowa plus zużycie) jako główny model
  wzrosła z 27% do 41%; za stanowisko spadła z 21% do 15%; za efekt jest głównym modelem dla 5%, a 25%
  spodziewa się, że będzie nim do 2028.
- Growth Unhinged 2026 (ponad 230 firm, 13 maja 2026): hybryda 37% jako główny model (inna próba, nie da się
  porównać wprost); 29% używa kredytów AI; inwestorzy deklarują, że wolą hybrydę (35%) od wyceny za efekt
  (26%), za zużycie (24%), stałej (10%) i za stanowisko (5%).
- ICONIQ *State of AI* 2026 (~300 menedżerów): wycena za zużycie 35% → 42%, wycena za efekt 18% → 23%.

**Co to oznacza dla boxa (moja opinia, do sprawdzenia w części 06):** Twoi kupujący to małe kancelarie,
które budżetują miesięcznie i boją się niespodzianek. Zacznij od **stałej, przewidywalnej opłaty za
kancelarię plus płatnych dodatków** (agentów eksperckich). Wycenę za efekt zostaw na później, dla jednego
wąskiego procesu, który potrafisz rzetelnie zmierzyć. To „hybryda” w rozumieniu ankiet, tyle że część
zmienną wybiera klient (których agentów dokłada), a nie licznik.

---

## 6. Kolejność tego kursu

```
 02 podłoga kosztowa ─► najniższa cena, przy której biznes przeżyje
 03 sufit wartości ───► ile to jest warte dla Kancelarii K, i wartość referencyjna
 04 metryka wartości ─► ZA CO pobierasz opłatę: kancelaria, agent, stanowisko, efekt; good/better/best
 05 sprzęt ───────────► do kogo należy box i ile gotówki potrzebujesz
 06 gotowość ─────────► mierz, nie zgaduj: rozmowy, Van Westendorp, płatne pilotaże
 07 cennik ───────────► spisany cennik, rabaty, warunki umowy
 08 skala ────────────► jak ta wycena wygląda dla inwestora i w miarę dokładania agentów
```

**Przykład przewodni.** Przez cały kurs wyceniasz box dla **Kancelarii K**: fikcyjnej kancelarii prawnej
w polskim mieście regionalnym, pięć osób — dwóch adwokatów, jeden aplikant i dwóch asystentów. Zastąp
Kancelarię K prawdziwą kancelarią, gdy tylko z jakąś przeprowadzisz rozmowę.

---

## 7. ĆWICZENIE 01 — zarejestruj z góry swoją cenę na oko

Zanim nauczysz się czegokolwiek innego, zapisz, ile wziąłbyś dzisiaj. Na końcu kursu porównasz to ze
zmierzoną ceną. To biznesowa wersja zasady z kursów: *„predykcja przed każdym eksperymentem”*.

Utwórz `pricing/00-gut-price.md`, **poza publicznym repo** (później znajdą się tam informacje o klientach):

```markdown
# Cena na oko — zapisana <data>, przed częścią 02

Opłata wdrożeniowa (jednorazowa):  ____ PLN netto
Sprzęt (kto płaci, jak):           ____
Opłata miesięczna za kancelarię:   ____ PLN netto
Co jest w cenie:                   ____
Dlaczego ta liczba (jedna linia):  ____
Pewność (0–100%):                  ____
```

Potem utwórz `pricing/01-anchors.md` z trzema pustymi sekcjami — *Podłoga kosztowa*, *Wartość referencyjna*,
*Wartość ekonomiczna* — które wypełnią części 02 i 03.

---

## 8. ⭐ EKSPERYMENT TERENOWY 01 — ile płacą dziś za oprogramowanie?

**Hipoteza.** Mała polska kancelaria prawna już wydaje co najmniej 500 zł netto miesięcznie na oprogramowanie
(prawnicza baza danych, system do prowadzenia spraw, pakiet biurowy) i myśli o oprogramowaniu jak o koszcie
miesięcznym, a nie jak o zakupie.

**Procedura.** Zapytaj trzy osoby, które pracują w małych biurach zawodowych albo je prowadzą (wystarczy Twoja
sieć kontaktów — to nie jest rozmowa sprzedażowa). Pytaj wyłącznie o przeszłość, nigdy o Twój produkt:

1. *„Za jakie programy Pani/Pana kancelaria płaci co miesiąc albo co rok?”*
2. *„Ile to mniej więcej wychodzi miesięcznie, wszystko razem?”*
3. *„Kto zdecydował o zakupie ostatniego z nich i ile to trwało?”*

**Predykcja (moja).** Dwie z trzech wydają łącznie 500–1 500 zł miesięcznie; największą pozycją jest prawnicza
baza danych (LEX albo Legalis); decyzję podjął sam starszy partner, w ciągu kilku tygodni.

| Kancelaria | Osoby | Opłacane programy | PLN / miesiąc łącznie | Największa pozycja | Kto zdecydował | Ile trwało |
| :-- | --: | :-- | --: | :-- | :-- | :-- |
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

**Gdy wynik różni się od mojej predykcji, Twój pomiar wygrywa** — popraw `01-anchors.md`, nie dane.

---

## 9. Pułapki

**B31 · Wycena koszt-plus dla produktu, który sprzedaje wartość.**
*Objaw:* cena to „sprzęt + 20% + moje godziny”. *Dlaczego boli:* ignoruje wartość referencyjną i ogranicza Cię
do marży firmy usługowej. *Lekarstwo:* policz podłogę, a potem zapomnij o niej, dopóki nie masz sufitu.

**B32 · Wycena technologii zamiast wykonanej pracy.**
*Objaw:* cennik wspomina tokeny, rozmiary modeli albo pamięć GPU. *Lekarstwo:* wyceniaj pozwolenie, odzyskane
godziny i spokój (sekcja 4). Specyfikacja techniczna idzie do załącznika.

**B33 · Kopiowanie ceny z USA przez kurs walut.**
*Objaw:* „Lemony bierze 499 USD, więc 1 900 zł”. *Dlaczego boli:* inny kupujący, inna alternatywa, inny poziom
płac. *Lekarstwo:* używaj cen zagranicznych tylko jako jednego punktu odniesienia obok polskich.

**B34 · Ustalanie ceny po zbudowaniu produktu.**
*Objaw:* box ma dziesięć funkcji, a Ty dopiero teraz zastanawiasz się, ile za niego wziąć. *Lekarstwo:* rozmowa
o gotowości do zapłaty (część 06) odbywa się, zanim zbudujesz drugi proces.

**B35 · Przedział zamiast ceny.**
*Objaw:* „800–2 500 miesięcznie”. *Dlaczego boli:* przedziału nie da się obalić, więc niczego Cię nie uczy.
*Lekarstwo:* jedna cena na pakiet, ze spisanym warunkiem, pod jakim ją zmienisz.

**B36 · Dane klientów w publicznym repozytorium.**
*Objaw:* notatki z rozmów zacommitowane obok plików kursu. *Lekarstwo:* `pricing/` leży poza każdym publicznym
repo i nigdy nie wpisujesz nazwy klienta do pliku, który trafia na GitHuba.

---

## 10. Checkpoint

Nie zaczynaj części 02, dopóki wszystkie te punkty nie są prawdziwe:

- [ ] `pricing/00-gut-price.md` istnieje, z jedną liczbą w każdej linii i poziomem pewności.
- [ ] `pricing/01-anchors.md` istnieje z trzema pustymi sekcjami.
- [ ] Potrafisz bez notatek wyjaśnić różnicę między wartością referencyjną a wartością ekonomiczną.
- [ ] Eksperyment terenowy 01 ma co najmniej jeden wypełniony wiersz (celem są trzy).
- [ ] Potrafisz nazwać trzy rzeczy, które sprzedaje box (sekcja 4), każdą jednym zdaniem.

Źródła do tej części: [ZRODLA.md](ZRODLA.md), sekcja „Część 01”.
