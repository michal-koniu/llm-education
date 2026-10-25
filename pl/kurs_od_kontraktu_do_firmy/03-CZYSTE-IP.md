# Część 03 · Czyste IP: buduj tak, żeby nikt nie mógł rościć sobie praw do Twojego produktu

> **Cel tej części.** Ustawiasz rozdzielenie pracy dla banku i startupu, które przekonałoby sceptycznego
> prawnika: osobne urządzenia, konta, czas, dane i narzędzia AI, plus ślad dowodowy, który pokazuje, kiedy i jak
> zbudowałeś każdy element. Decydujesz, co zostaje publicznie w `llm-education`, a co nie, i przygotowujesz się
> na chwilę, w której inwestor zapyta: *„Kto jest właścicielem kodu?"*
>
> **Czas:** ~4 h na ustawienie, potem nawyk · **Poziom:** ⭐⭐⭐ · **Efekt:** `founder/03-separation.md`,
> `founder/03-ip-register.md`

> **To nie jest porada prawna.** Zasady rozdzielenia opisane tutaj to higiena inżynierska oparta na prawie
> streszczonym w części 02. Czy wystarczą przy Twojej umowie, potwierdzi prawnik.

---

## 0. Problem

Każdy inwestor, nabywca i poważny klient w końcu zapyta, kto jest właścicielem produktu. Odpowiedź, której
potrzebuje, to **łańcuch praw (chain of title)**: czysta, udokumentowana linia od każdego autora każdego
fragmentu kodu do spółki. Typowe luki, według źródeł o due diligence IP zebranych w researchu do tego kursu
(MaRS, Mondaq), są dokładnie dwie: **kod, który założyciel napisał, zanim spółka powstała**, i **kod napisany
przez kontraktorów**.

Ty masz obie, plus trzecią lukę, której większość założycieli nie ma: klienta — bank — którego umowa może
zawierać szeroką klauzulę IP (część 02). Przestroga, którą opowiada każdy prawnik startupów, to *Mattel v. MGA*
(lalki Bratz): własność produktu wartego miliardy dolarów zależała od brzmienia klauzuli o przeniesieniu praw
i od tego, **kiedy** projektant zrobił pierwsze szkice (streszczenie Harvard JOLT). Obroną są dowody tworzone na
bieżąco, a nie wspomnienia odtwarzane później.

---

## 1. Pięć rozdzieleń

| Rozdzielenie | Zasada | Dlaczego |
| :-- | :-- | :-- |
| **Urządzenia** | startup budujesz wyłącznie na własnych maszynach (Twój rig, Twój własny laptop). Nigdy na laptopie banku, VDI ani koncie chmurowym banku | sprzęt banku i klauzula audytu DORA (część 02, §4) |
| **Konta** | osobny e-mail, organizacja na GitHubie, konta chmurowe, sejf w menedżerze haseł, subskrypcje AI — opłacane przez Ciebie | logi i własność kont są dowodem; narzędzia AI banku mogą mieć własne warunki co do tego, co z nimi wytworzysz |
| **Czas** | praca nad startupem poza godzinami, które fakturujesz bankowi lub w których jesteś dla niego dostępny (część 01, §2) | „w czasie pracy w ramach umowy" to częsty haczyk w klauzulach IP i wskaźnik przy uznaniu za stosunek pracy |
| **Dane** | żadnych danych, dokumentów, kodu, konfiguracji, promptów, zgłoszeń ani wiadomości z banku — w żadnej formie, nigdy | tajemnica przedsiębiorstwa (art. 11 UZNK), tajemnica bankowa, NDA (część 02, §3) |
| **Wiedza** | ogólne umiejętności są Twoje; konkretne rozwiązania banku nie. W razie wątpliwości odbuduj z publicznych źródeł i zapisz, z których | niezależne opracowanie jest zgodne z prawem (art. 11 ust. 7 UZNK); kopiowanie nie |

Piąte rozdzielenie jest najsubtelniejsze. Umiesz budować agentów, bo ich studiowałeś i budowałeś — kursy
`llm-education` są tego publicznym dowodem, datowanym przez gita. Ta wiedza jest Twoja. Konkretny wewnętrzny
projekt, który widziałeś w banku, nie jest, nawet jeśli potrafiłbyś go odtworzyć z pamięci.

---

## 2. Ślad dowodowy

Twórz dowody **w trakcie pracy**, nie po fakcie:

| Dowód | Jak | Siła |
| :-- | :-- | :-- |
| **Historia gita** we własnej organizacji, z podpisanymi commitami | `git config commit.gpgsign true` z własnym kluczem; commity na własnych maszynach | mocny dowód tego, *kiedy* i *kto*, o ile repozytorium nigdy nie miało przepisywanej historii |
| **Notatki projektowe z datami** | ADR (architecture decision record) dla każdej istotnej decyzji, jak w kursach technicznych — w repozytorium produktu | pokazują niezależne rozumowanie i jego źródła |
| **Lista źródeł dla każdego komponentu** | dla każdego agenta: na jakich publicznych artykułach, dokumentacjach, projektach open source się opiera | dowodzi niezależnego opracowania (art. 11 ust. 7 UZNK) |
| **Rejestr czasu** | CSV z części 01, prowadzony dalej jako nawyk | pokazuje, że praca nad startupem odbywała się poza godzinami kontraktu |
| **Data pewna** dla kluczowych dokumentów | polskie prawo zna „datę pewną" (art. 81 KC) — np. notarialne poświadczenie daty; częstym cyfrowym odpowiednikiem jest **kwalifikowany elektroniczny znacznik czasu** zgodny z eIDAS | bardzo mocny dla pierwszego dokumentu projektowego i rejestru IP. *Wiedza ogólna, nie z researchu do tego kursu — potwierdź metodę ze swoim prawnikiem* |

Datę pewną zrób raz, na początku, dla jednego dokumentu: opisu produktu i listy wszystkiego, co do tej pory
zbudowałeś (rejestr IP, sekcja 4). Kosztuje niewiele i kończy każdy spór o to, co istniało **przed** daną datą.

---

## 3. Co zostaje publiczne

`llm-education` jest publiczne na licencji **CC BY 4.0** (lekcje) i **MIT** (kod). Te licencje pozwalają
każdemu — także konkurentowi — kopiować, zmieniać i wykorzystywać materiał **komercyjnie**, z podaniem autora.
To w porządku i ma wartość: publiczne repozytorium jest dowodem Twoich kompetencji i tego, *kiedy* co wiedziałeś.

Ale od teraz decyduj świadomie, co gdzie trafia:

| Publiczne (`llm-education`) | Prywatne (repozytorium produktu) |
| :-- | :-- |
| ogólne kursy, przeglądy, techniki, benchmarki | agenci dla konkretnych zawodów, ich prompty i przepływy pracy |
| ogólne narzędzia (np. kalkulator wyceny z tego kursu) | **zbiory ewaluacyjne** zbudowane z dokumentów zawodowych — Twoja fosa jakościowa |
| to, co pomaga Twojej reputacji i rekrutacji | integracje, instalatory, obraz boxa, kanał aktualizacji |
| | wszystko, co zawiera informacje o prawdziwych klientach |

Przydatny test: *czy byłbym niezadowolony, widząc to w produkcie konkurenta w przyszłym miesiącu?* Jeśli tak —
prywatne.

I pamiętaj o licencjach, które **otrzymujesz**: Bielik jest na Apache 2.0 (`asymetrie-biznesowe-ai/02-OKAZJE.md`);
samo repozytorium ostrzega, żeby *„uważać na licencje"* PLLuM (`asystenci-ai/04-POLSKA-I-SUWERENNOSC.md`).
Każdy model i każda biblioteka w boxie trafia do rejestru IP razem ze swoją licencją.

---

## 4. Rejestr IP

`founder/03-ip-register.md` — jeden wiersz na komponent produktu:

| Komponent | Autor(zy) | Powstał (od–do) | Gdzie (urządzenie, konto) | Oparty na (źródła publiczne) | Licencja zależności | Przeniesiony na | Dokument |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| agent do triażu pism | ja | 2026-11 → | własny rig, własna organizacja na GitHubie | kurs_aplikacje_agentowe 03, 14; dokumentacja Bielika | Apache 2.0 (Bielik) | — (nadal moje) | — |
| instalator boxa | ja | | | | | | |
| polski zbiór ewaluacyjny, pisma sądowe | ja + prawnik L01 (zanonimizowane dokumenty) | | | | | | **pisemna umowa z L01?** |

Dwa wiersze wymagają uwagi od samego początku:

- **Każdy, kto coś wnosi** — freelancer, znajomy, który pisze skrypt, prawnik, który projektuje zbiór
  ewaluacyjny. Bez pisemnego przeniesienia praw z wymienionymi polami eksploatacji (art. 41 ust. 2, art. 53)
  **to on jest właścicielem swojej części**. Podpisz przeniesienie przy odbiorze pracy, a nie wtedy, gdy zapyta
  inwestor.
- **Dokumenty od przyszłych klientów** używane do zbiorów ewaluacyjnych: są objęte tajemnicą zawodową i RODO.
  Używaj dokumentów zanonimizowanych albo publicznych, z pisemną zgodą. To temat kursu o umowach; na razie
  zapisuj w rejestrze, skąd pochodzi każdy dokument.

---

## 5. Gdy powstaje spółka

Dziś IP należy do Ciebie jako osoby (albo do Twojej JDG). Gdy założysz spółkę — a musisz to zrobić przed
przyjęciem inwestycji (część 06) — IP musi do niej przejść **na piśmie**, z wymienionymi polami eksploatacji,
jako przeniesienie praw, a nie licencja: inwestorzy oczekują, że spółka będzie **właścicielem** IP w całości
(źródła z researchu: Mondaq, KS&K). Rejestr IP jest załącznikiem do tego przeniesienia.

Jak dokładnie to przenieść (sprzedaż, aport, wkład do prostej spółki akcyjnej (PSA), w której akcje można
wydać za pracę lub usługi), ma konsekwencje podatkowe. To temat planowanego kursu o formie prawnej. Teraz liczy
się jedno: **jeśli rejestr jest kompletny, a dowody istnieją, przeniesienie jest formalnością. Jeśli nie — jest
negocjacją.**

---

## 6. ĆWICZENIE 03 — ustaw rozdzielenie

W `founder/03-separation.md` zapisz, a potem zrób:

1. Listę urządzeń, których używasz do startupu (i potwierdzenie, że żadne nie należy do banku).
2. Listę kont: e-mail, organizacja na GitHubie, chmura, subskrypcje AI, domena — wszystkie na Twoje nazwisko,
   opłacane przez Ciebie.
3. Twój klucz do podpisywania commitów i potwierdzenie, że podpisywanie jest włączone w repozytorium produktu.
4. Zasadę dotyczącą czasu, przepisaną z części 01, z godzinami, których będziesz używać.
5. Podział na publiczne i prywatne z sekcji 3, zastosowany do wszystkiego, co planujesz zbudować w ciągu
   najbliższych trzech miesięcy.
6. Pierwszą wersję `founder/03-ip-register.md` — wszystko, co istnieje dziś.
7. Decyzję o dacie pewnej dla rejestru i opisu produktu oraz metodę, którą poleca Twój prawnik.

---

## 7. ⭐ EKSPERYMENT TERENOWY 03 — wrogi recenzent

**Hipoteza.** Recenzent, który czyta wyłącznie Twój ślad dowodowy (historię gita, rejestr IP, rejestr czasu,
ADR-y), nie znajdzie komponentu produktu o niejasnym pochodzeniu.

**Procedura.** Po miesiącu budowania poproś kogoś zaufanego — najlepiej prawnika, a jeśli nie, doświadczonego
inżyniera, który nie zna projektu — żeby zagrał prawnika inwestora. Daj mu dostęp do odczytu dowodów (oczywiście
nie do materiałów banku). Poproś, żeby wypisał każdy komponent, dla którego nie potrafi odpowiedzieć: *kto go
napisał, kiedy, na czym, z jakich źródeł i kto jest teraz jego właścicielem?*

**Predykcja (moja).** Dwie albo trzy luki: skrypt pomocniczy bez notatki o źródłach, dokument testowy
o niezapisanym pochodzeniu i pierwsze dwa tygodnie commitów sprzed włączenia podpisywania.

| Znaleziona luka | Komponent | Dlaczego jest niejasny | Poprawka | Poprawione (data) |
| :-- | :-- | :-- | :-- | :-- |
| | | | | |

---

## 8. Pułapki

**B11 · „Tylko przetestuję" na laptopie banku.**
*Objaw:* pierwszy prototyp działał na służbowej maszynie, „bo ma GPU / VPN / licencję Copilota".
*Lekarstwo:* nic ze startupu, nawet test, na sprzęcie ani kontach banku.

**B12 · Narzędzie AI banku pisze Twój produkt.**
*Objaw:* firmowa licencja Copilota albo czatu używana do kodu startupu. *Dlaczego boli:* własność konta, logi
i warunki narzędzia są pod kontrolą banku. *Lekarstwo:* własne subskrypcje, opłacane przez Ciebie.

**B13 · Współtwórca bez przeniesienia praw.**
*Objaw:* znajomy napisał pipeline OCR „po znajomości". *Lekarstwo:* pisemne przeniesienie praw z polami
eksploatacji przy odbiorze (art. 53).

**B14 · Wszystko publiczne z przyzwyczajenia.**
*Objaw:* zbiory ewaluacyjne i prompty agentów wypchnięte do publicznego repozytorium razem z kursami.
*Lekarstwo:* test publiczne/prywatne z sekcji 3.

**B15 · Przepisywanie historii.**
*Objaw:* `git rebase` i force-push na miesiącach commitów startupu, „żeby posprzątać". *Dlaczego boli:* niszczy
daty, które są Twoim dowodem. *Lekarstwo:* nigdy nie przepisuj opublikowanej historii repozytorium produktu;
squashuj tylko gałęzie funkcjonalne przed scaleniem.

---

## 9. Checkpoint

- [ ] Wszystkie pięć rozdzieleń działa i jest zapisanych w `founder/03-separation.md`.
- [ ] Podpisane commity są włączone w repozytorium produktu.
- [ ] `founder/03-ip-register.md` wymienia każdy istniejący komponent, jego źródła i licencje.
- [ ] Zdecydowałeś, co z Twoich planów idzie publicznie, a co zostaje prywatne.
- [ ] EKSPERYMENT TERENOWY 03 jest zaplanowany za miesiąc.

Źródła do tej części: [ZRODLA.md](ZRODLA.md), sekcja „Część 03".
