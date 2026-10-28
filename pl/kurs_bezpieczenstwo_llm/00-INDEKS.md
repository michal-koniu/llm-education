# Kurs 3: bezpieczeństwo LLM, aplikacji agentowych i modeli lokalnych — indeks

**Utworzony 28 października 2026.**
Kontynuacja kursu 1 — [`../kurs_lokalne_modele/00-KURS-INDEKS.md`](../kurs_lokalne_modele/00-KURS-INDEKS.md) —
i kursu 2 — [`../kurs_aplikacje_agentowe/00-INDEKS.md`](../kurs_aplikacje_agentowe/00-INDEKS.md).

> **Cel całości.** Po tym kursie potrafisz **zaatakować własne modele, aplikacje i konfiguracje tak, jak zrobiłby
> to napastnik, zrozumieć, dlaczego każdy atak działa — aż do poziomu tokenów — i zamknąć go obroną, której efekt
> zmierzyłeś.** Zanim wpuścisz do swojego systemu innych ludzi, wiesz dokładnie, gdzie jest słaby.
>
> Kurs 1 uczył, **jak działa model**. Kurs 2 uczył, **jak zbudować wokół niego system**. Kurs 3 uczy,
> **jak ten system się psuje — i jak sprawić, żeby wytrzymał.**

---

## Teza, na której stoi cały kurs

> **Model językowy nie odróżnia instrukcji od danych. Wszystko, co czyta, może nim sterować.** Dla promptów nie
> istnieje odpowiednik sparametryzowanego zapytania SQL i nie pojawi się szybko.

Dlatego o bezpieczeństwie aplikacji LLM decyduje się **poza modelem**: w tym, co model może czytać, jakie
narzędzia trzyma, dokąd trafia jego wynik i co się dzieje, gdy się pomyli. Prompt systemowy mówiący „nigdy nie
rób X” to życzenie, nie zabezpieczenie. Trening bezpieczeństwa modelu o otwartych wagach, który uruchamiasz
sam, to nawyk, nie granica.

⭐ **Każda obrona w tym kursie jest mierzona.** Te same ataki uruchamiasz k razy na laboratorium, przed obroną
i po niej, i odczytujesz skuteczność ataku (ASR) z przedziałem ufności. Obrona, która nie rusza liczby, jest
dekoracją — kurs mówi to wprost, gdy tak się dzieje.

---

## Dla kogo i czym ten kurs nie jest

- **Dla:** osób, które budują agentów i uruchamiają modele lokalne (llama.cpp / llama-server, Ollama, vLLM,
  interfejsy czatu w stylu Open WebUI, narzędzia MCP, skille) i chcą udostępnić je innym, nie stając się
  bohaterem kolejnego raportu z incydentu.
- **Obronny z założenia.** Atakujesz **tylko laboratorium na 127.0.0.1 i własne maszyny**. Sukces pokazują
  kanarki, pliki-znaczniki i żądania do własnego serwera „napastnika” w laboratorium — nigdy prawdziwe
  złośliwe oprogramowanie, prawdziwe ofiary ani szkodliwe treści. Eksperymenty z jailbreakami celują
  w nieszkodliwą politykę tematyczną laboratorium.
- **Nie katalog gotowych ataków.** Techniki są wyjaśnione po to, żebyś je rozpoznawał i umiał na nie testować.
  Tam, gdzie technika jest tylko opisana (ataki optymalizacyjne, ataki adaptacyjne, usuwanie treningu
  bezpieczeństwa, wnioskowanie o danych innych użytkowników), kurs mówi dlaczego.

---

## Ścieżka

```
  BLOK I · PODSTAWY ──────────────────────────────── ~13 h
   01 krajobraz zagrożeń        trifecta, OWASP LLM / ASI, ATLAS, NIST, DFD + STRIDE
   02 laboratorium         ⭐⭐  Sieve: celowo dziurawy asystent + harness do ASR
   03 mechanika            ⭐   szablony, tokeny specjalne, role, czemu nie ma „prepared statement”
              │
  BLOK II · SAM MODEL ────────────────────────────── ~9 h
   04 jailbreaki                rodziny, ataki optymalizacyjne, alignment to nie granica
   05 bezpośredni injection     przejęcie celu, wycieki promptu, polityka w kodzie
              │
  BLOK III · APLIKACJA WOKÓŁ MODELU ──────────────── ~23 h
   06 pośredni injection   ⭐⭐  strony, dokumenty, ukryte nośniki, zatruwanie RAG
   07 agenci i eksfiltracja ⭐⭐ nadmierna sprawczość, kanały wycieku, taint, agent w stylu CaMeL
   08 MCP, skille, pamięć       zatruwanie narzędzi, rug pull, trwałość w pamięci, wiele agentów
   09 wyjście i zasoby          XSS / SQL / kod z wyniku modelu, pętle bez końca, limity
              │
  BLOK IV · MODELE, DANE, INFRASTRUKTURA ─────────── ~13 h
   10 łańcuch dostaw modeli ⭐  pickle, GGUF, szablony czatu, backdoory, przypinanie hashy
   11 prywatność                zapamiętywanie, embeddingi, najemcy, cache, logi
   12 infrastruktura lokalna    wystawione serwery, 0.0.0.0, DNS rebinding, proxy + auth
              │
  BLOK V · OBRONA JAKO INŻYNIERIA ────────────────── ~19 h
   13 guardrale i red teaming   strażnicy jako klasyfikatory, ataki adaptacyjne, bramka CI
   14 wykrywanie i reagowanie   log audytu, kanarki-pułapki, blokada, runbook, replay
   15 CAPSTONE ────────────────► utwardzony stos, końcowa tablica wyników, raport red teamu
```

⚠️ **Część 02 jest obowiązkowa przed wszystkim, co używa laboratorium.** Części 06 i 07 to rdzeń kursu:
większość prawdziwych incydentów z lat 2023–2026 to pośredni prompt injection plus kanał eksfiltracji. Nie
pomijaj ich.

---

## Pliki

| # | Plik | Poziom | Czego się nauczysz | Czas |
| :-- | :-- | :-- | :-- | :-- |
| 01 | [`01-KRAJOBRAZ-ZAGROZEN-I-MODELOWANIE.md`](01-KRAJOBRAZ-ZAGROZEN-I-MODELOWANIE.md) | ⭐⭐⭐ | czym różni się bezpieczeństwo LLM, model jako „zdezorientowany zastępca”, **zabójcza trójka (lethal trifecta)**, OWASP LLM 2025 / ASI / MITRE ATLAS / NIST AI 100-2, oś czasu incydentów, DFD + STRIDE, model zagrożeń laboratorium | ~4 h |
| 02 | [`02-LABORATORIUM.md`](02-LABORATORIUM.md) | ⭐⭐⭐ | ⭐⭐ **laboratorium:** Sieve, narzędzia, kanarki, serwer napastnika, harness, ASR z przedziałami Wilsona, pierwszy pomiar bazowy | ~4 h |
| 03 | [`03-DLACZEGO-MODELE-DA-SIE-ATAKOWAC.md`](03-DLACZEGO-MODELE-DA-SIE-ATAKOWAC.md) | ⭐⭐⭐⭐ | szablon czatu → tokeny, tokeny specjalne i podrabianie ról, hierarchia instrukcji i jej granice, trening bezpieczeństwa jako wyuczone zachowanie, **dlaczego prompty nie mają sparametryzowanych zapytań** | ~5 h |
| 04 | [`04-JAILBREAKI-I-ALIGNMENT.md`](04-JAILBREAKI-I-ALIGNMENT.md) | ⭐⭐⭐ | rodziny jailbreaków (odgrywanie ról, many-shot, Crescendo, kodowania, prefill, GCG/AutoDAN/PAIR/TAP), **dlaczego alignment otwartych wag nie jest granicą**, kontrola ról w bramce i filtr polityki na wyjściu | ~5 h |
| 05 | [`05-BEZPOSREDNI-PROMPT-INJECTION-I-WYCIEKI-PROMPTU.md`](05-BEZPOSREDNI-PROMPT-INJECTION-I-WYCIEKI-PROMPTU.md) | ⭐⭐⭐ | przejęcie celu i wyciąganie promptu systemowego, **dlaczego sekret w prompcie już wyciekł**, zmierzona drabina obron: kanarki, brak sekretów w prompcie, polityka w kodzie | ~4 h |
| 06 | [`06-POSREDNI-PROMPT-INJECTION-I-ZATRUWANIE-RAG.md`](06-POSREDNI-PROMPT-INJECTION-I-ZATRUWANIE-RAG.md) | ⭐⭐⭐⭐ | ⭐⭐ injection przez strony, dokumenty i wyniki narzędzi, ukryte nośniki, PoisonedRAG, sanityzacja, spotlighting, detektory, skaner przy ingeście — **ASR przed i po** | ~6 h |
| 07 | [`07-AGENCI-NARZEDZIA-I-EKSFILTRACJA.md`](07-AGENCI-NARZEDZIA-I-EKSFILTRACJA.md) | ⭐⭐⭐⭐⭐ | ⭐⭐ nadmierna sprawczość, kanały eksfiltracji (obrazki, linki, argumenty narzędzi, e-mail), prawdziwe przypadki m.in. EchoLeak, polityka renderowania, lista dozwolonych celów, **bramkowanie narzędzi po taincie, agent w stylu CaMeL** | ~7 h |
| 08 | [`08-MCP-SKILLE-PAMIEC-I-WIELE-AGENTOW.md`](08-MCP-SKILLE-PAMIEC-I-WIELE-AGENTOW.md) | ⭐⭐⭐⭐ | model zagrożeń MCP (zatruwanie narzędzi, rug pull, shadowing), skille jako łańcuch dostaw, **zatruwanie i trwałość pamięci**, zaufanie między agentami, przypinanie i kwarantanna pamięci | ~5 h |
| 09 | [`09-OBSLUGA-WYJSCIA-KOD-I-ZASOBY.md`](09-OBSLUGA-WYJSCIA-KOD-I-ZASOBY.md) | ⭐⭐⭐⭐ | wynik modelu jako niezaufane wejście: XSS, SQL, powłoka, wykonywanie kodu, halucynowane pakiety; **nieograniczone zużycie** na lokalnym serwerze GPU; limity i bezpieczniki | ~5 h |
| 10 | [`10-LANCUCH-DOSTAW-MODELI.md`](10-LANCUCH-DOSTAW-MODELI.md) | ⭐⭐⭐⭐ | ⭐ **pliki modeli to programy:** opkody pickle, `weights_only`, safetensors, CVE w GGUF i szablonach, `trust_remote_code`, backdoory; skaner opkodów, czytnik GGUF i przypinanie hashy od zera | ~5 h |
| 11 | [`11-PRYWATNOSC-I-WYCIEKI-DANYCH.md`](11-PRYWATNOSC-I-WYCIEKI-DANYCH.md) | ⭐⭐⭐⭐ | zapamiętywanie, membership inference, odwracanie embeddingów, **wycieki między najemcami**, współdzielony cache promptów, logi; kontrola własności w kodzie, przegląd sekretów, eksperyment z gościem | ~4 h |
| 12 | [`12-INFRASTRUKTURA-LOKALNA.md`](12-INFRASTRUKTURA-LOKALNA.md) | ⭐⭐⭐ | wystawione serwery inferencji i interfejsy czatu, `0.0.0.0`, CORS i **DNS rebinding na localhost**, reverse proxy + TLS + uwierzytelnianie, kontenery z GPU, sekrety — przeskanuj i zamknij **własną** konfigurację | ~4 h |
| 13 | [`13-GUARDRAILE-RED-TEAMING-I-OCENA-OBRON.md`](13-GUARDRAILE-RED-TEAMING-I-OCENA-OBRON.md) | ⭐⭐⭐⭐⭐ | strażnicy mierzeni jak klasyfikatory, **dlaczego testy statyczne zawyżają obrony** (ataki adaptacyjne), garak / PyRIT / promptfoo na laboratorium, bramka regresji w CI | ~6 h |
| 14 | [`14-WYKRYWANIE-MONITORING-I-REAGOWANIE.md`](14-WYKRYWANIE-MONITORING-I-REAGOWANIE.md) | ⭐⭐⭐⭐ | co logować, a czego nigdy, kanarki-pułapki na każdym wyjściu, blokada działająca bez modelu, **runbook incydentu** zakończony kontrfaktycznym replayem | ~5 h |
| 15 | [`15-CAPSTONE.md`](15-CAPSTONE.md) | ⭐⭐⭐⭐⭐ | wszystkie obrony w jednym stosie, cały zestaw na wersji bazowej i utwardzonej, **koszt dla zwykłych zapytań**, raport red teamu, przegląd przed wpuszczeniem innych ludzi | ~8 h |
| — | [`ZRODLA.md`](ZRODLA.md) | — | opisana bibliografia: **co skąd pochodzi i do której części trafiło** | — |
| — | [`lab/`](../../en/course_llm_security/lab/) | — | kod laboratorium (część 02, wspólny dla obu wersji językowych); kolejne części mówią, jakie pliki dodać | — |

**Razem: ~77 godzin przy klawiaturze**, plus czas modelu na eksperymenty.

---

## Anatomia każdej części

```
0. Problem — dlaczego to ważne, prostymi słowami
1-N. Teoria od wysokiego poziomu aż do mechanizmu
   „W prawdziwym świecie” — datowane incydenty i badania, z linkami
   Obrony — co działa, co nie i dlaczego
LAB — kod, który dodajesz do laboratorium (obrony, przypadki ataków, narzędzia)
⭐ EKSPERYMENT — hipoteza, procedura, przewidywanie, pusta tabela na TWÓJ wynik
ĆWICZENIA
Pułapki tej części — objaw → lekarstwo
Punkt kontrolny — co musi być prawdą przed następną częścią
```

⭐ **Tablica wyników to nić przewodnia kursu.** Każda część dodaje przypadki ataków (`lab/cases/partNN.jsonl`)
i konfiguracje obron (`pNN-…`). W części 15 masz jedną tabelę: każdy atak × każda obrona, na **Twoim** modelu,
z przedziałami ufności. Gdy Twoje liczby nie zgadzają się z przewidywaniami w tekście, **wygrywa Twój pomiar.**

---

## Zasady laboratorium

1. **Wszystko słucha na 127.0.0.1.** Interfejs czatu odrzuca obce nagłówki `Host`/`Origin`; `fetch_url` sięga
   tylko do własnej strony testowej laboratorium i serwera napastnika.
2. **Kanarki, nie sekrety.** Laboratorium generuje losowe ciągi `CANARY-…`; atak „się udaje”, gdy kanarek trafi
   tam, gdzie nie powinien. Nigdy nie wkładaj do laboratorium prawdziwych danych dostępowych.
3. **Tylko własne systemy.** Skrypty skanujące i sondujące z części 12 odmawiają pracy z adresami publicznymi.
   Skanuj wyłącznie maszyny, które należą do Ciebie.
4. **Obrony się mierzy, a nie w nie wierzy.** Uruchamiaj k ≥ 5 powtórzeń, czytaj przedział, zapisuj liczby.

---

## Jak ten kurs ma się do dwóch pozostałych

| Temat | Kurs 1 | Kurs 2 | Kurs 3 |
| :-- | :-- | :-- | :-- |
| Piaskownica, limity, sieć | część 07 (bwrap, systemd-run) | część 10 (drabina izolacji) | części 09, 12 z nich korzystają |
| Prompt injection | część 07 §6 (wstęp) | część 16 (ASI01) | części 03, 05, 06, 07 (dogłębnie) |
| OWASP dla agentów | — | część 16 (ASI01–ASI10) | część 01 (mapa), części 06–09, 14 |
| Ewaluacja | część 03 (harness) | część 14 (złoty zbiór) | części 02, 13 (ASR, bramka CI) |
| Obserwowalność | część 07 §7–8 | część 15 (OTel) | część 14 (wykrywanie, reagowanie) |
