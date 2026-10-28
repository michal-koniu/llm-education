# 10 · Pieniądze i ludzie: kto za tym stoi i jak to się utrzymuje

**Po co ten rozdział.** To jedyny rozdział kursu, który nie uczy, jak działa silnik, tylko **kto go utrzymuje, z czego i po co**. Stos referencyjny — llama.cpp, llama-swap, kwanty GGUF z Unsloth, model DeepSeek, na Macu LM Studio albo MLX — jest zbudowany z kodu, za którym stoją konkretne firmy i konkretni ludzie, a ich interesy zmieniają się szybciej niż kod. Po przeczytaniu będziesz umieć: (1) rozpoznać, **w jaki sposób dany projekt zarabia** (albo dlaczego nie zarabia); (2) odczytać z publicznych źródeł, **kto płaci jego programistom**; (3) ocenić, **co się stanie z taką instalacją**, gdy projekt zostanie przejęty, przelicencjonowany albo porzucony; (4) wyciągnąć lekcje do własnych planów (asystent lokalny po polsku) — wyłącznie z opisanych tu przypadków.

> ⚠️ **Uwaga o charakterze rozdziału.** Niczego tu nie uruchamiałem ani nie testowałem. To **desk research**: strony firm i ich blogi, strony projektów, API GitHuba (liczby commitów, pola profilu, daty), pliki `LICENSE` w klonach repozytoriów oraz kilka źródeł wtórnych (Wikipedia, TechCrunch). Stan na **19 października 2026**. **Kwoty finansowania i wyceny są najsłabszymi faktami w całym przeglądzie** — większość pochodzi od samych firm albo z prasy, a nie z dokumentów rejestrowych. Każda liczba ma w tekście znacznik pochodzenia i datę. Wiersze „pracodawca" biorą się z **pola `company` w profilu GitHub (deklaracja własna)** albo z domeny e-mail w commitach; to nie jest wyciąg z kadr i bywa nieaktualne. Ten rozdział mówi o **motywacjach organizacji**, nie o motywach pojedynczych osób — o osobach podaję tylko publiczne fakty zawodowe (rola, projekt, dorobek).

**Znaczniki pochodzenia używane w całym rozdziale:**

| Zapis w tekście | Znaczenie |
|---|---|
| (bez znacznika) | sprawdzone w źródle pierwotnym: API GitHuba, plik w repozytorium, strona projektu/firmy podająca fakt jako fakt |
| *(dane firmy)* / *(dane projektu)* | twierdzenie samej firmy lub projektu (blog, strona, README); nie ma niezależnego potwierdzenia |
| *(prasa)* / *(źródło zewnętrzne)* | doniesienie prasowe lub Wikipedia; nie znalazłem komunikatu firmy |
| *(profil GitHub)* | deklaracja własna w profilu użytkownika, bywa nieaktualna |
| *(niezweryfikowane)* / *(moje wyliczenie)* | wniosek własny albo arytmetyka na danych z API |

**Spis treści**

1. [Pięć sposobów, w jakie open-source'owa infrastruktura AI zarabia (i dwa, w których nie zarabia)](#1-pięć-sposobów-w-jakie-open-sourceowa-infrastruktura-ai-zarabia-i-dwa-w-których-nie-zarabia)
2. [Kto płaci programistom — projekt po projekcie](#2-kto-płaci-programistom--projekt-po-projekcie)
3. [Konsolidacja 2026: kto kupuje opiekunów lokalnego AI](#3-konsolidacja-2026-kto-kupuje-opiekunów-lokalnego-ai)
4. [Hostowana inferencja na wierzchu (krótko)](#4-hostowana-inferencja-na-wierzchu-krótko)
5. [Kto jest kim — katalog osób](#5-kto-jest-kim--katalog-osób)
6. [Licencje: tabela i pułapki](#6-licencje-tabela-i-pułapki)
7. [Ryzyko zależności: co się stanie ze stosem referencyjnym](#7-ryzyko-zależności-co-się-stanie-ze-stosem-referencyjnym)
8. [Czego możesz się nauczyć do własnych planów](#8-czego-możesz-się-nauczyć-do-własnych-planów)

Rozdziały techniczne, do których odsyłam po „jak": silnik i jego kod — `04-LLAMA-CPP-I-RODZINA-GGML.md`; Ollama, LM Studio, Jan, llmman i spółka — `05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md`; vLLM, SGLang, TensorRT-LLM — `06-SILNIKI-SERWEROWE-VLLM-SGLANG.md`; MLX, oMLX, ds4 — `07-APPLE-MLX-OMLX-I-DS4.md`; KTransformers, mistral.rs, Unsloth — `08-SPECJALISCI-KTRANSFORMERS-I-INNE.md`; formaty i kwanty — `03-KWANTYZACJA-I-FORMATY.md`.

---

## 1. Pięć sposobów, w jakie open-source'owa infrastruktura AI zarabia (i dwa, w których nie zarabia)

Silnik wnioskowania jest zwykle **darmowy i na otwartej licencji**. Pieniądze pojawiają się obok niego. Z przejrzanych projektów da się wyodrębnić pięć powtarzalnych mechanizmów i dwa przypadki, w których pieniędzy nie ma w ogóle. Pełną tabelę dziesięciu wzorców z konsekwencjami dla ciebie znajdziesz w sekcji 7; tu jest wersja „skąd się biorą pensje".

### 1.1 Sprzęt ciągnie oprogramowanie

Oprogramowanie jest darmowe, bo sprzedaje krzem. Producent płaci inżynierom, żeby każdy nowy model działał najpierw na jego kartach.

- **NVIDIA:** TensorRT-LLM (Apache-2.0, repozytorium otwarte w całości od marca 2025 — wniosek o roku z kolejności wpisów w README), Dynamo, mikrousługi NIM. Software dopiero na drugim miejscu: **NVIDIA AI Enterprise** kosztuje według cennika firmy 4 500 USD za GPU rocznie (subskrypcja roczna), 22 500 USD za GPU w licencji wieczystej z 5-letnim wsparciem, w chmurze 1 USD za GPU-godzinę; zniżka 75% dla edukacji i startupów *(dane firmy: docs.nvidia.com, cennik)*. To wzór „darmowy silnik, płatny kontener ze wsparciem". Przychód całej NVIDIA za rok obrotowy 2026: 215,9 mld USD *(źródło zewnętrzne: Wikipedia)* — w notatkach ocena jest taka, że na pierwszym miejscu jest sprzęt, a subskrypcje oprogramowania na drugim *(wniosek z notatek, niezweryfikowane)*.
- **AMD:** Lemonade (Apache-2.0; README: „optymalizacje inżynierów AMD" dla Ryzen AI, Radeon, Strix Halo), inżynier AMD wśród najaktywniejszych committerów vLLM (AndreasKaratzas, 428 commitów *(profil GitHub)*).
- **Apple:** MLX (MIT, „Copyright © 2023 Apple Inc.", README: „brought to you by Apple machine learning research"). **Dlaczego Apple to finansuje — nie znalazłem żadnego oświadczenia Apple; to wniosek *(niezweryfikowane)*:** framework sprawia, że Apple Silicon z pamięcią zunifikowaną jest dobrym laptopem do modeli otwartych.
- **Qualcomm:** kupił Modular (Mojo, MAX) — ogłoszenie 2026-06-24, zamknięcie 2026-07-29, cena nieujawniona. Firmowa narracja: „silicon-agnostic compute layer" *(dane firmy)*.

### 1.2 Platforma kupuje opiekunów (platform complement)

Platforma, na której zarabia się czym innym (hub modeli, system kontenerów, subskrypcje korporacyjne), zatrudnia ludzi utrzymujących projekt, który zwiększa wartość platformy.

- **Hugging Face:** ggml.ai (llama.cpp) 2026-02-20; autor oMLX 2026-09-22; autor mistral.rs ma `@huggingface` w profilu *(profil GitHub; ogłoszenia nie znalazłem)*. Szczegóły w sekcji 3.
- **Red Hat:** Neural Magic (duży wkład w vLLM) — ogłoszenie 2024-11-12, zamknięcie 2025-01-13, warunki nieujawnione; Red Hat sprzedaje **Red Hat AI Inference** („oparty na vLLM i llm-d") jako subskrypcję **liczoną od akceleratora**.
- **Docker:** Docker Model Runner (Apache-2.0, beta ogłoszona 2025-04-09 w Docker Desktop 4.40, modele jako artefakty OCI na Docker Hub). Osobnego modelu przychodu nie ma; to funkcja trzymająca programistów w Docker Desktop/Hub *(niezweryfikowane — moja interpretacja; Docker nie podał takiego uzasadnienia w źródłach, które widziałem)*.

### 1.3 Darmowy klient lokalny, płatna chmura

Aplikacja lokalna jest „lejkiem". Przychód to hostowane użycie.

- **Ollama Inc.:** lokalnie za darmo; chmura według cennika ollama.com z 2026-10-19: Free 0 USD; **Pro 20 USD/mies.** (200 USD/rok) z kredytem 60 USD i 3 równoległymi żądaniami; **Max 100 USD/mies.** z kredytem 300 USD i 10 żądaniami; **Team 500 USD/mies.** (wczesny dostęp) z puli 1 000 USD; Enterprise wg wyceny; rozliczenie za token, 50% taniej poza szczytem *(dane firmy)*. Notatki odnotowują, że rozliczenie zmieniło się z czasu GPU na tokeny (blog z 2026-08-31) — cennik zmienia się w miesiącach, nie w latach.
- **LM Studio (Element Labs, Inc.):** aplikacja zamknięta; od 2025-07-08 „darmowa do użytku w pracy" (wpis na blogu); przychód ma iść z **LM Studio Bionic** (hostowane modele otwarte, deployment w chmurze z zerową retencją / na infrastrukturze prywatnej / na urządzeniach brzegowych) oraz z **planów Teams i Enterprise** *(dane firmy)*. Przejęcie **Locally AI** (zespół aplikacji iOS/iPadOS) — *(dane firmy; Wikipedia)*, kwiecień 2026.
- **AnythingLLM (Mintplex Labs):** MIT; darmowa aplikacja desktopowa, **płatny produkt hostowany** dla zespołów i wersja enterprise *(dane firmy)*; deklaruje wsparcie Y Combinator.

### 1.4 Darmowy silnik → startup → hosting i wsparcie

Najbardziej „klasyczny" scenariusz dla silników serwerowych: laboratorium akademickie tworzy silnik, oddaje go neutralnej fundacji, a założyciele (z największym blokiem committerów) zakładają firmę, która sprzedaje hosting i wsparcie.

- **vLLM → Inferact:** Berkeley Sky Computing Lab (repo od 2023-02-09, artykuł o PagedAttention na SOSP 2023); od 2025-05-06 projekt hostowany przez **PyTorch Foundation**; firma **Inferact** — *(dane firmy)* 150 mln USD „seed" przy wycenie 800 mln USD, styczeń 2026, prowadzący a16z i Lightspeed. Kwotę 150 mln potwierdza też prasa (Wikipedia za TechCrunch); wycenę i listę inwestorów znalazłem tylko w materiałach firmy.
- **SGLang → RadixArk:** SGLang hostowany przez LMSYS (organizacja non-profit 501(c)(3), zarejestrowana we wrześniu 2024); firma RadixArk — *(prasa: TechCrunch 2026-01-21)* wycena ok. 400 mln USD, rundę prowadził Accel, **wielkość rundy niepotwierdzona**.
- Obie firmy sprzedają rzeczy *obok* silnika: zarządzaną chmurę, platformę na twoich GPU, certyfikację dostawców modeli, stos do RL (Miles w RadixArk). Zobacz `06-SILNIKI-SERWEROWE-VLLM-SGLANG.md`.

### 1.5 Open-core i licencje z haczykiem

Rdzeń jest wolny, a element strategiczny (marka, interfejs, binarki) objęty ograniczeniem.

- **Open WebUI:** od wersji 0.6.6 (2025-04-19) „Open WebUI License": prawa jak w BSD-3 plus klauzula zakazująca usuwania/zastępowania marki „Open WebUI", chyba że masz ≤ 50 użytkowników końcowych w ciągu 30 dni, pisemną zgodę albo licencję enterprise.
- **Unsloth:** rdzeń Apache-2.0, ale interfejs **Unsloth Studio** na AGPL-3.0 (`studio/LICENSE.AGPL-3.0`) — README mówi, że taka struktura „wspiera dalszy rozwój".
- **Modular:** repozytorium Apache-2.0 z wyjątkami LLVM, ale **MAX** na „Modular Community License".
- **LiteLLM:** MIT poza katalogiem `enterprise/`, który wymaga subskrypcji BerriAI w produkcji.

### 1.6 (Bez zarobku) Jeden człowiek, dzień pracy gdzie indziej

Szczegóły liczbowe w tabelach sekcji 2; tu sam mechanizm. **ds4 (antirez):** MIT, bez firmy; autor wrócił do Redis w listopadzie 2024 jako deweloper-ewangelista na część etatu; GitHub Sponsors 10–12 osób (1/5/25 USD miesięcznie), a przychody ze sponsoringu, jak pisze, przekazuje innym projektom OSS — za czas przy ds4 nie płaci wprost nikt. **LocalAI:** sponsorzy „pokrywają koszty CI" (m.in. Spectro Cloud), 14 sponsorów, brak firmy. **llama-swap:** lista sponsorów istnieje, ma 0 sponsorów. **KoboldCpp, text-generation-webui:** jeden maintainer; u drugiego README wspomina o „hojnym grancie" a16z z sierpnia 2023 *(dane projektu)*.

### 1.7 (Bez zarobku) Pivot albo zombie

- **GPT4All (Nomic):** ostatni push **2025-05-27**; firma przeszła na agentów AI dla architektury, inżynierii i budownictwa *(dane firmy: nomic.ai/about)*. Aplikacja była lejkiem marketingowym; gdy firma zmieniła rynek, aplikacja zamarła.
- **Jan (Menlo Research):** firma prezentuje się dziś jako producent humanoidalnych robotów (Asimov 1, depozyt 499 USD) *(dane firmy: menlo.ai)*. Finansowania Menlo **nie znalazłem** — nie podaję żadnej kwoty.
- **TGI (Hugging Face):** repozytorium zarchiwizowane, ostatni commit 2026-03-21, README: „maintenance mode"; HF *sam porzucił własny silnik serwerowy* i poleca vLLM, SGLang oraz llama.cpp.

> **Sprawdź sam — czy projekt żyje (zombie check).** Zanim oprzesz coś ważnego na projekcie, sprawdź daty:
> ```bash
> gh api repos/huggingface/text-generation-inference --jq '{archived, pushed_at, license: .license.spdx_id}'
> gh api repos/ggml-org/llama.cpp --jq '{pushed_at, stargazers_count, forks_count}'
> ```
> (nie uruchamiałem dokładnie tych wywołań z `--jq`; pola `archived`, `pushed_at`, `stargazers_count` są tymi, z których korzystały notatki). Dla repozytorium TGI spodziewaj się `archived: true`.

---

## 2. Kto płaci programistom — projekt po projekcie

**Jak czytać tabele.** „Kto płaci" to ocena na podstawie profili GitHub i domen e-mail w commitach (deklaracje własne, mogą się rozjeżdżać z rzeczywistością). Udziały commitów to **moja arytmetyka** na danych z API z 2026-10-19 (łączna liczba commitów w historii repozytorium, z wyłączeniem botów tam, gdzie to zaznaczono) — liczba commitów mierzy aktywność, nie wartość wkładu. Kolumna „motywacja sponsora" to wniosek o organizacji, nie o osobach, i tam gdzie sponsor nie podał uzasadnienia, jest oznaczona jako niezweryfikowana.

### 2.1 Rodzina ggml i narzędzia lokalne

| Projekt (gwiazdki 2026-10-19) | Kto płaci twórcom | Model przychodu | Finansowanie | Zarządzanie | Koncentracja |
|---|---|---|---|---|---|
| **llama.cpp / ggml** (131,7 tys.; MIT) | od 2026-02-20 **Hugging Face** (zespół ggml.ai); wcześniej ggml.ai na pre-seedzie; do tego wkład inżynierów NVIDIA (Vulkan), akademii (KIT), niezależnych | brak własnego; HF zyskuje ekosystem (GGUF na Hubie, llama.cpp w HF Inference Endpoints *(dane firmy)*) | pre-seed Nat Friedman i Daniel Gross, 2023, **kwota nieujawniona** *(dane firmy: ggml.ai)*; cena przejęcia przez HF **nieujawniona** | `ggml-org` na GitHubie; CODEOWNERS per obszar; brak fundacji | 7 z 12 najaktywniejszych committerów deklaruje HF = 3 878 z 5 284 commitów (73%); sam Gerganov 2 035 (ok. 39% tej dwunastki, ok. 17% wszystkich ~11,7 tys.) *(moje wyliczenie)* |
| **ik_llama.cpp** (3,3 tys.; MIT) | nikt (projekt osobisty + społeczność) | brak | nie znalazłem | jeden maintainer (Kawrakow, w profilu „Gentleman at large") | wysoka |
| **llama-swap** (6,0 tys.; MIT) | maintainer pracuje gdzie indziej (*(profil GitHub)*: „Tailscale and Elethink") | brak | lista GitHub Sponsors: 0 sponsorów | jeden maintainer | 536 z ok. 653 commitów = 82% |
| **llamafile** (26,4 tys.; Apache-2.0) | **Mozilla.ai** (projekt zaczęty w Mozilla Builders) | brak (lejek do ofert Mozilla.ai *(niezweryfikowane)*) | *(dane firmy)* Mozilla ogłosiła 2023-03-22 „początkowe zobowiązanie" 30 mln USD na Mozilla.ai | Mozilla.ai; mała liczba aktywnych maintainerów | pierwotny autor (jart, 600 commitów) nie jest już widocznym committerem w 2026 |
| **KoboldCpp** (AGPL-3.0) | nikt | brak | brak listy sponsorów, brak FUNDING.yml | jeden maintainer (4 374 własnych commitów) | ok. 1 |
| **text-generation-webui** | grant a16z z 2023 *(dane projektu)* | brak | lista sponsorów istnieje | jeden maintainer | 82% commitów |
| **Ollama** (183,9 tys.; MIT) | **Ollama Inc.** (VC) | chmura: subskrypcje + opłaty za token | 88 mln USD *(dane firmy, blog 2026-07-09)* vs 65 mln USD *(prasa, Wikipedia za TechCrunch)* — **niepogodzone**, patrz niżej | firma, bez fundacji | czterech najaktywniejszych = ok. 3,6 tys. z ok. 5,9 tys. commitów (zapewne pracownicy) |
| **LM Studio** (aplikacja zamknięta; CLI `lms` MIT) | **Element Labs, Inc.** | Bionic, Teams, Enterprise | **nie znalazłem** (strona i blog milczą) | firma zamknięta | mały zespół (4–6 widocznych committerów) |
| **Jan** (45,0 tys.; Apache-2.0 z prośbą o atrybucję) | **Menlo Research** | brak widocznego dla Jana; firma sprzedaje roboty | **nie znalazłem** | firma | najaktywniejsi: urmauur 1 464, qnixsynapse 868 commitów |
| **LocalAI** (49,7 tys.; MIT) | sponsorzy CI + wkład własny autora | brak | brak firmy i rund | BDFL | mudler 3 507 commitów, dalej boty |
| **Open WebUI** (156,2 tys.; „Open WebUI License") | **Open WebUI Inc.** | edycja enterprise, brak marki, SSO/SCIM | **nie znalazłem** | firma, CLA dla kontrybutorów | tjbck 13 450 commitów |
| **AnythingLLM** (67,3 tys.; MIT) | **Mintplex Labs** | hostowany produkt zespołowy | YC *(dane firmy)*; kwoty brak | firma | timothycarambat 1 518 commitów |
| **GPT4All** (77,4 tys.; MIT) | **Nomic** (pivot) | agenci AEC | Series A 17 mln USD, Coatue, 2023 *(dane firmy)* | **zamarł 2025-05-27** | — |
| **Lemonade** (5,9 tys.; Apache-2.0) | **AMD** | brak (sprzęt) | — | inżynierowie AMD + społeczność | jeremyfowers (AMD) 569 commitów |
| **llmman** (563; Apache-2.0) | autor to inżynier Docker (adres `@docker.com` w commitach z października 2026) — **brak oświadczenia o sponsoringu** | brak | brak | osobista organizacja GitHub; strona nie podaje firmy | Curtin 402 z ok. 550–570 commitów (ok. 70%) |
| **RamaLama** (3,1 tys.; MIT) | pracownicy Red Hat (profile, e-mail) | pośredni (OpenShift, RHEL AI *(niezweryfikowane)*) | — | organizacja `containers` | rhatdan 1 462, ericcurtin 971 |
| **Docker Model Runner** (658; Apache-2.0) | Docker, Inc. | funkcja produktu | — | firma | doringeman 696, ilopezluna 387 |

**Niezgodność w notatkach, nierozstrzygnięta: Ollama 88 vs 65 mln USD.** Blog Ollama z 2026-07-09 mówi, że firma „zebrała 88 mln USD" od Benchmark (Peter Fenton), Theory Ventures (Tomasz Tunguz), 8VC (Alex Kolicich), Y Combinator oraz aniołów (m.in. Solomon Hykes, Aaron Katz, Spencer Kimball, Quinn Slack) i że obsługuje „8,9 mln programistów" *(dane firmy)*. Wikipedia za TechCrunch pisze o „65 milionach dolarów w lipcu 2026" *(prasa)*. Może to runda (65) kontra suma (88), ale **nie umiem tego uzgodnić** i niczego tu nie rozstrzygam. Wyceny firma nie ujawniła; wcześniejszych rund nie znalazłem. Zdanie z bloga o „85% firm z Fortune 500" to też twierdzenie firmy.

### 2.2 Silniki serwerowe

| Projekt | Kto płaci | Model przychodu | Finansowanie | Zarządzanie | Koncentracja |
|---|---|---|---|---|---|
| **vLLM** (94,2 tys.; Apache-2.0) | **Inferact** (założyciele i najwięksi committerzy), Red Hat/Neural Magic, AMD, Hugging Face, Mistral AI, Meta; sponsorzy mocy obliczeniowej na vllm.ai: Alibaba Cloud, AMD, Anyscale, AWS, Crusoe, Google Cloud, IBM, Intel, Lambda, Nebius, Novita AI, NVIDIA, Red Hat, Roblox, RunPod, UC Berkeley | Inferact Platform i Inferact Cloud *(dane firmy)*; Red Hat AI Inference (subskrypcja per akcelerator) | Inferact: 150 mln USD przy 800 mln USD, styczeń 2026 *(dane firmy; kwota też w prasie)* | **PyTorch Foundation** od 2025-05-06; dokument zarządzania: „nikt nie kupuje sobie miejsca w zarządzaniu; status committera należy do osób, nie do firm" | 8 committerów powiązanych z Inferact = 3 373 z 6 945 commitów top-15 = 49%; Red Hat (mgoin) 9% *(moje wyliczenie)* |
| **SGLang** (37,4 tys.; Apache-2.0) | **RadixArk**, Meta, niezależni; LMSYS finansowany przez NVIDIA, Google Cloud, a16z, AMD, Hugging Face, Together *(dane firmy: lmsys.org)* | hosting, Miles (RL) | RadixArk: ok. 400 mln USD wyceny, Accel, wielkość rundy nieznana *(prasa, 2026-01-21)* | LMSYS (501(c)(3)) + ekosystem PyTorch | 5 committerów RadixArk = 3 193 z 7 978 (top-12) = 40% *(moje wyliczenie)* |
| **TensorRT-LLM** (14,9 tys.; Apache-2.0 + noty) | pracownicy NVIDIA | sprzęt + AI Enterprise / NIM | spółka publiczna | NVIDIA sama | nie dotyczy |
| **Dynamo** (8,3 tys.; Apache-2.0) | NVIDIA | jw. | — | NVIDIA | — |
| **TGI** (10,9 tys.; Apache-2.0) | Hugging Face | brak osobnego | — | **zarchiwizowany** | — |
| **KTransformers** (19,6 tys.; Apache-2.0) | Tsinghua MADSys + Approaching.AI | publikacje + usługi Approaching.AI *(niezweryfikowane)* | Approaching.AI: **nie znalazłem** (strona niedostępna) | laboratorium | 11 osób w liście maintainerów (6 Tsinghua + 5 Approaching.AI) |
| **LMDeploy** | laboratorium (Shanghai AI Laboratory *(niezweryfikowane)*) | brak | nie znalazłem | laboratorium | — |
| **Modular (MAX/Mojo)** | od 2026-07-29 **Qualcomm** | w ramach Qualcomm | 250 mln USD, 2025-09-24, wycena 1,6 mld USD, łącznie 380 mln USD *(dane firmy)* | Qualcomm; Mojo, MAX i Modular Cloud „pozostaną odrębnymi produktami" *(dane firmy)* | — |

### 2.3 Mac i inne

| Projekt | Kto płaci | Model przychodu | Finansowanie | Zarządzanie | Koncentracja |
|---|---|---|---|---|---|
| **MLX** (28,8 tys.; MIT) | **Apple** (zcbenz, angeloskath, jagrit06 — *(profil GitHub)*: „Apple") | brak; sprzęt *(niezweryfikowane)* | — | Apple, bez fundacji | współtwórca Awni Hannun (718 commitów, #1) ma w profilu „Research at Anthropic. Prev: co-created MLX at Apple"; jego ostatni commit do MLX z adresu Apple widziałem 2026-02-24 |
| **mlx-lm** (7,4 tys.; MIT) | Apple + społeczność | brak | — | j.w. | awni 291, angeloskath 63, dalej społeczność |
| **oMLX** (22,9 tys.; Apache-2.0) | od 2026-09-22 **Hugging Face** zatrudnia autora; blog HF: projekt „utrzymuje licencję Apache 2.0 i pozostaje niezależny", staje się „w pełni utrzymywanym i finansowanym" | brak | — | autor | 2 110 z ok. 2 280 commitów w top-5 |
| **ds4 / DwarfStar** (24,0 tys.; MIT) | nikt (hobby autora) | brak | brak | BDFL | 523 commity autora; następny 33 |
| **mistral.rs** (7,8 tys.; MIT) | autor ma w profilu `@huggingface`; ogłoszenia nie znalazłem; **brak związku z firmą Mistral AI** (README zaprzecza afiliacji) | brak | brak | jeden maintainer | 3 073 vs następny 125 |
| **exo** (48,0 tys.; Apache-2.0) | exo labs | open source + wdrożenia dla zespołów *(dane firmy)* | **nie znalazłem** | firma | Alex Cheema 1 424 commity |
| **Unsloth** (78,3 tys.; Apache-2.0 + AGPL Studio) | **Unsloth AI Inc.** (YC lato 2024, zespół 12 osób wg strony YC — data wpisu nieznana) | open-core; ceny i plany **nie znalezione** | **nie znalazłem** (strony `about` i `pricing` zwracały 403) | firma | Daniel Han 6 391 z ok. 11,4 tys. commitów (ok. 56%) |

> **Sprawdź sam — kto naprawdę pisze kod (arytmetyka commitów).** Powtórzenie wyliczeń z tej sekcji dla dowolnego repozytorium:
> ```bash
> gh api 'repos/ggml-org/llama.cpp/contributors?per_page=15' --jq '.[] | [.login, .contributions] | @tsv'
> gh api users/ggerganov --jq '{login, name, company, location}'
> ```
> Dla każdego loginu z listy wywołaj drugie polecenie i odczytaj pole `company`. Policz sumę commitów osób z tym samym pracodawcą i podziel przez sumę całej listy. Pamiętaj: `company` to deklaracja własna; lista `contributors` zawiera boty, a przy forkach, które zachowują historię (jak ik_llama.cpp), na szczycie jest autor *upstreamu*. (Składnię `--jq` zapisałem z pamięci, nie uruchamiałem jej; endpointy `contributors?per_page=15` i `users/LOGIN` są tymi, których użyto w przeglądzie.)

---

## 3. Konsolidacja 2026: kto kupuje opiekunów lokalnego AI

W 2023 roku lokalne AI wyglądało jak zbiór projektów hobbystycznych i małych startupów. W 2026 widać coś odwrotnego: **opiekunowie najważniejszych projektów przechodzą na etaty u kilku dużych firm**. Poniżej historia w porządku chronologicznym, od najbliższej stosowi referencyjnemu.

### 3.1 Hugging Face i llama.cpp (2026-02-20)

**Fakty.** Hugging Face opublikował wpis „GGML and llama.cpp join Hugging Face" (2026-02-20; autorzy: Georgi Gerganov, Xuan-Son Nguyen, Aleksander Grygier, Lysandre, Victor Mustar, Julien Chaumond) oraz równoległą dyskusję w repozytorium llama.cpp (nr 19759, wątek założony przez `ggerganov`). Strona ggml.ai mówi: „firma została przejęta przez Hugging Face w 2026". **Warunków (cena, udziały) nie ujawniono** — wpis HF nie podaje kwoty. Obietnice HF: zespół „poświęca 100% czasu" na utrzymanie llama.cpp i ma „pełną autonomię" w kierunkach technicznych; projekt pozostaje „w 100% open-source i napędzany przez społeczność"; HF zapewnia „długoterminowe, zrównoważone zasoby"; celem jest „bezszwowa" integracja `transformers` z llama.cpp i lepsze pakowanie dla zwykłych użytkowników.

**Co z tego wynika dla struktury utrzymania.** Z 12 najaktywniejszych committerów llama.cpp 7 deklaruje HF jako pracodawcę, co daje 73% commitów tej dwunastki *(moje wyliczenie na podstawie API i profili)*. To dwa znaczenia naraz: **ryzyko porzucenia spadło** (ludzie mają pensje), a **koncentracja w jednym pracodawcy wzrosła**. W dyskusji pod ogłoszeniem pojawiły się według notatek uwagi o „własności kodu pod korporacyjnym zarządem" i o tym, że „nie było wcześniejszej publicznej dyskusji" *(źródło zewnętrzne: streszczenie dyskusji #19759, nie czytałem wątku w całości)*.

**Motywacja organizacji (nie osób).** HF chce, żeby to na jego Hubie żyły modele lokalne, i chce „jednego kliknięcia" od modelu w `transformers` do llama.cpp *(blog HF)*. To przyspiesza pokrycie nowych architektur i poprawia UX dla casualowych użytkowników — a nie obiecuje priorytetu dla wielogpu AMD, dopóki nie zażyczy go klient HF *(niezweryfikowane — wniosek, nie oświadczenie)*.

Nowa warstwa marki wokół llama.cpp: strona **llama.app**, repozytoria `Llama-macOS`, `Llama-Windows`, `llama-install.sh`, `llama.brand` (z licencją NOASSERTION, czyli kontrola marki, nie MIT). Czy llama.app będzie monetyzowane: **nie ustaliłem**. Techniczne szczegóły repozytorium: `04-LLAMA-CPP-I-RODZINA-GGML.md`.

### 3.2 NVIDIA i Hugging Face (doniesienia z sierpnia–września 2026)

> ⚠️ **Najsłabiej udokumentowany fakt tego rozdziału.** *Według doniesień prasowych* NVIDIA ma kupić Hugging Face za **12,93 mld USD**. Pierwsze doniesienia datowane są na **2026-08-26**, a artykuł TechCrunch „Nvidia confirms it will buy Hugging Face for $12.9 billion" na **2026-09-03**; zamknięcie transakcji miałoby nastąpić w **pierwszej połowie 2027**. Podstawą są **Wikipedia** (hasła „Hugging Face" i „Nvidia") i **ten jeden artykuł TechCrunch** *(prasa)*. **Nie znalazłem komunikatu prasowego żadnej ze stron** — ani na nvidianews.nvidia.com (zrzut, który dostałem, pokazywał tylko wpisy z października 2026), ani na huggingface.co/blog. Streszczenie TechCrunch cytuje Jensena Huanga: „Moc obliczeniowa Nvidii nie będzie wymagana, aby budować na Hugging Face lub z niego wdrażać" *(prasa)*. **Zweryfikuj to u źródła, zanim zacytujesz kwotę w jakimkolwiek dokumencie.**

Co by to oznaczało dla łańcucha własności, *jeśli doniesienia się potwierdzą*: opiekunowie llama.cpp byliby pracownikami spółki zależnej dominującego dostawcy GPU. Licencja MIT się nie zmienia (patrz sekcja 7), zmieniałby się **kierunek sterowania**: priorytety roadmapy, pierwszeństwo dla CUDA. Dla stosu referencyjnego to jednak mniej dramatyczne, niż brzmi, bo backend HIP w llama.cpp jest kompilowany **z tych samych źródeł `.cu` co CUDA** (przez warstwę `ggml/src/ggml-cuda/vendors/hip.h`; nie ma osobnego drzewa ROCm) — pierwszeństwo dla CUDA dotyczy więc w dużej mierze także twojej ścieżki, o ile gałęzie specyficzne dla RDNA4 (`gfx1201`) ktoś nadal utrzymuje. Zobacz `04-LLAMA-CPP-I-RODZINA-GGML.md`, sekcja o HIP.

### 3.3 HF zbiera opiekunów, nie tylko llama.cpp

| Co | Kiedy | Fakt | Źródło / znacznik |
|---|---|---|---|
| llama.cpp / ggml | 2026-02-20 | zespół ggml.ai dołącza do HF, warunki nieujawnione | blog HF, ggml.ai |
| **TGI** (własny silnik serwerowy HF) | ostatni commit 2026-03-21 | **archiwum**, „maintenance mode"; README poleca vLLM, SGLang i silniki lokalne jak llama.cpp | repozytorium |
| vLLM | obecnie | Harry Mellor (`hmellor`, HF) 601 commitów — wśród najaktywniejszych | API, profil |
| oMLX | 2026-09-22 | autor (Jun Kim) zatrudniony w HF; „pozostaje Apache-2.0", „w pełni utrzymywany i finansowany" | blog HF `/blog/omlx` |
| mistral.rs | brak daty | autor (Eric Buehler) ma `@huggingface` w profilu; ogłoszenia nie znalazłem | profil GitHub |
| Candle (biblioteka Rust ML) | — | utrzymywana przez HF; oryginalny autor w profilu: „Co-founder Kyutai & Gradium" | API, profil |

HF **porzucił własny silnik serwerowy** (TGI) i zamiast tego finansuje otwarte: ludzi w vLLM, w llama.cpp, w MLX (przez oMLX), w Rust (mistral.rs). Strategia, jaką deklaruje: `transformers` jako „źródło prawdy dla definicji modeli", a wokół niej hosting i oferta firmowa. Cennik publiczny HF *(dane firmy, huggingface.co/pricing)*: PRO 9 USD/mies.; Team 20 USD/użytkownika/mies.; Enterprise Hub 50 USD/użytkownika/mies.; magazyn 12–18 USD/TB/mies.; GPU w Spaces 0,40–23,50 USD/h; **Inference Endpoints** od 0,033 USD/h (CPU) do 4,50 USD/h (H100). Poprzednia runda: Series D 235 mln USD, sierpień 2023, wycena 4,5 mld USD *(prasa, Wikipedia)*.

### 3.4 Pozostali kupujący

- **Qualcomm kupuje Modular** (Mojo, MAX): ogłoszenie 2026-06-24, zamknięcie 2026-07-29, cena nieujawniona. Chris Lattner jest dziś według strony Modular „EVP, Advanced AI Software and Platforms" w Qualcomm, Tim Davis „SVP & GM of Modular, Qualcomm". Firma pisze, że Mojo, MAX i Modular Cloud „będą kontynuowane jako odrębne produkty i marki" *(dane firmy)*. W komunikacie Qualcomm, który czytałem, **nie ma zobowiązania**, że MAX/Mojo pozostaną otwarte ani że wsparcie dla NVIDIA/AMD będzie neutralne — to brak zapisu, nie zapowiedź zmiany. Traktuj MAX jako **produkt należący do dostawcy sprzętu**.
- **Red Hat kupuje Neural Magic** (wcześniejszy precedens): ogłoszenie 2024-11-12, zamknięcie 2025-01-13, warunki nieujawnione; Neural Magic (spin-out z MIT, 2018) opisany jest jako „czołowy współtwórca vLLM".
- **Docker** wchodzi przez Model Runner (2025-04-09) i przez ludzi: Eric Curtin — współtwórca RamaLama (adres `@redhat.com` w commitach z lipca–sierpnia 2025), dziś w profilu „Docker, Inc", commity do llmman i `docker/model-runner` z `@docker.com` (lipiec–październik 2026). Daty zatrudnienia: nie ustaliłem. Trzy narzędzia (llmman, RamaLama, Docker Model Runner) mają zbliżoną funkcję i wspólną osobę — *oczekuj konsolidacji (niezweryfikowane)*.
- **LM Studio kupuje Locally AI** (kwiecień 2026; zespół aplikacji iOS/iPadOS; aplikacja „Locally" w czerwcu 2026) *(dane firmy, Wikipedia)*.

### 3.5 Obserwacja przekrojowa (moja interpretacja)

Wszystkie te ruchy układają się w jeden wzorzec: **ten, kto sprzedaje sprzęt albo subskrypcje, kupuje warstwę oprogramowania, która decyduje, gdzie model będzie działał** *(niezweryfikowane — wniosek z zestawienia faktów, żadna z firm tak tego nie sformułowała)*. Do tego dochodzi drugi wątek: **ci sami ok. 30 ludzi przechodzą między tymi samymi ok. 10 pracodawcami** — Awni Hannun z Apple do Anthropic, Eric Curtin z Red Hat do Docker, Ying Sheng z Databricks/xAI do RadixArk, Zhuohan Li i Lianmin Zheng do Meta, Gerganov/Buehler/Kim do HF *(profile GitHub)*. To samo laboratorium w Berkeley wydał oba konkurencyjne silniki (vLLM i SGLang) i oba startupy.

### 3.6 Oś czasu 2022–2026

Tylko daty sprawdzone w notatkach: **(V)** = sprawdzone w API/źródle pierwotnym, **(F)** = data ogłoszenia podana przez firmę, **(P)** = data podana w prasie.

| Data | Zdarzenie | Znacznik |
|---|---|---|
| 2022-09-18 / 2022-09-25 | repozytoria ggml i whisper.cpp utworzone (Gerganov) | V (API) |
| 2023-02-09 | pierwsze commity vLLM (Berkeley) | V |
| 2023-03-10 | pierwsze commity llama.cpp (README; repo utworzone 18:58 UTC) | V |
| 2023-03-22 | Mozilla ogłasza Mozilla.ai i zobowiązanie 30 mln USD | F (blog Mozilla) |
| 2023 (miesiąc nieznany) | ggml.ai założone; pre-seed Friedman i Gross, kwota nieujawniona | F (ggml.ai) |
| 2023-06-26 / 2023-07-08 | repozytorium Ollama / wersja v0.0.1 | V |
| 2023-08-16 / 2023-08-17 | repozytoria TensorRT-LLM / Jan | V |
| 2023-09-12 | artykuł PagedAttention/vLLM (SOSP 2023) na arXiv | V |
| 2023-11-28 | MLX: pierwszy commit (Apple) | V |
| 2024-01-08 | repozytorium SGLang | V |
| 2024-03 | Redis przechodzi na SSPL | V (blog Redis) |
| 2024-07 | wpis o otwartym zarządzaniu vLLM; inkubacja LF AI & Data | V (tytuł wpisu); szczegóły: prasa |
| 2024-09 | LMSYS Corp. rejestruje się jako non-profit | V (lmsys.org) |
| 2024-11 | antirez wraca do Redis na część etatu | V |
| 2024-11-12 → 2025-01-13 | Red Hat ogłasza, potem zamyka przejęcie Neural Magic | V (komunikaty Red Hat) |
| 2025-03 | TensorRT-LLM: rozwój w całości na GitHubie (rok z kolejności wpisów README) | V (rok: wniosek) |
| 2025-04-09 | Docker Model Runner (beta, Docker Desktop 4.40) | V (blog Docker) |
| 2025-04-19 | Open WebUI: licencja z klauzulą o marce (v0.6.6) | V |
| 2025-05-01 | Redis 8: opcja AGPLv3 | V |
| 2025-05-06 | vLLM projektem hostowanym przez PyTorch Foundation | V |
| 2025-05-27 | ostatni push do GPT4All | V (API) |
| 2025-07-08 | LM Studio „darmowe do użytku w pracy" | V (blog) |
| 2025-09-24 | Modular: 250 mln USD, wycena 1,6 mld USD | F |
| 2025-12-19 | ostatnie wydanie TGI (v3.3.7) | V |
| 2026-01 (dzień nieustalony) | start Inferact, 150 mln USD seed | F; prasa potwierdza kwotę |
| 2026-01-21 | TechCrunch: SGLang → RadixArk, ok. 400 mln USD wyceny | P |
| **2026-02-20** | **ggml.ai (llama.cpp) dołącza do Hugging Face** | V |
| 2026-03-21 | ostatni commit TGI; repozytorium zarchiwizowane | V |
| 2026-03-30 | podgląd silnika MLX w Ollama (Apple silicon) | V (lista wpisów bloga) |
| 2026-05-06 | repozytorium ds4 utworzone | V |
| 2026-06-24 / 2026-07-29 | Qualcomm ogłasza / zamyka przejęcie Modular | V |
| 2026-07-01 | Together AI: seria C 800 mln USD | F |
| 2026-07-09 | Ollama: „88 mln USD", „8,9 mln programistów" | F |
| 2026-08-26 / 2026-09-03 | **doniesienia o przejęciu HF przez NVIDIA (12,93 mld USD)** / artykuł „confirms" | **P — brak komunikatu firm** |
| 2026-09-22 | autor oMLX dołącza do HF | V (blog HF) |
| 2026-10-14 | Modal: seria D 750 mln USD, wycena 15,75 mld USD, ARR 1 mld USD | F |
| 2026-10 (dzień nieustalony) | współpraca Inferact–AMD Instinct | F |

Pominąłem w tej osi wpisy z jednego źródła wtórnego (m.in. seria C i D Fireworks AI, początek LM Studio w maju 2023, rundy HF z 2023) — wracają niżej z odpowiednim znacznikiem.

---

## 4. Hostowana inferencja na wierzchu (krótko)

Nad otwartymi silnikami działa warstwa firm, które sprzedają **godziny GPU**. To tam są największe wyceny — i to ona tłumaczy, dlaczego silniki są dla wielu graczy „towarem dodatkowym".

| Firma | Co sprzedaje | Pieniądze | Znacznik |
|---|---|---|---|
| **Together AI** | API inferencji, klastry GPU, post-trening; własny stos (FlashAttention-4, „Together Megakernel", `together.compile`); wśród założycieli Tri Dao, Percy Liang, Chris Ré, Ce Zhang, Vipul Ved Prakash (strona firmy) | seria C **800 mln USD, 2026-07-01**; inwestorzy m.in. Aramco Ventures, NVIDIA, Vista Equity, General Catalyst, Salesforce Ventures; wyceny nie podano; zobowiązania mocy 500 MW | *(dane firmy)* |
| **Fireworks AI** | API do modeli otwartych, API treningowe, własny model „Ember-1" (wrzesień 2026) | seria B 52 mln USD (lipiec 2024, Sequoia); seria C 250 mln USD przy 4 mld USD (październik 2025); **seria D 1,51 mld USD przy 17,5 mld USD (lipiec 2026)**; CEO Lin Qiao (wcześniej Meta, PyTorch) | *(prasa — jedynie Wikipedia; nie znalazłem strony firmy)* |
| **Baseten** | dedykowana inferencja, API modeli (DeepSeek/GLM/Kimi), trening; klienci: Cursor, Notion, Zed, Canva, Vercel | finansowania **nie znalazłem**; konkretnych silników strona nie podaje | *(dane firmy)* |
| **Modal** | serverless GPU: inferencja, piaskownice dla agentów, trening | **seria D 750 mln USD przy 15,75 mld USD, 2026-10-14, Accel**; ARR 1 mld USD; użycie „potroiło się" w 5 miesięcy | *(dane firmy)* |

**Wniosek ostrożny.** Wyceny hostowanej inferencji (15–18 mld USD, o ile wierzyć firmom i Wikipedii) są o rząd wielkości większe niż startupów silnikowych (0,4–0,8 mld USD); notatki czytają to tak, że **silniki są wabikiem i lejkiem talentów, a gotówka jest w godzinach GPU** *(niezweryfikowane — interpretacja zestawienia, nie fakt)*. Wszystkie kwoty w tej tabeli to deklaracje firm lub prasa; żadnej nie sprawdzałem w rejestrach.

---

## 5. Kto jest kim — katalog osób

Zasady: **tylko role publiczne i zawodowe**; „rola" to to, co deklaruje profil GitHub lub strona firmy; „dorobek" to to, co dało się sprawdzić w API, artykule lub repozytorium. Pracodawca z profilu bywa nieaktualny. Liczby commitów — z API, 2026-10-19.

| Osoba | Rola / afiliacja | Projekt | Dorobek (sprawdzony) |
|---|---|---|---|
| **Georgi Gerganov** (`ggerganov`) | twórca; profil: `@huggingface` | ggml, llama.cpp, whisper.cpp | repozytoria ggml (2022-09-18) i whisper.cpp (2022-09-25); 2 035 commitów w llama.cpp (najwięcej; następny 630); właściciel katalogów `ggml/include`, CPU i Metal w CODEOWNERS |
| **Xuan-Son Nguyen** (`ngxson`) | HF, Francja | llama.cpp | 630 commitów; serwer i multimodalność (CODEOWNER `llama-server`, `llama-mtmd`) |
| **Aleksander Grygier** (`allozaur`) | HF | llama.cpp | 143 commity; webowy interfejs llama-server (`llama-ui`) |
| **Johannes Gäßler** (`JohannesGaessler`) | KIT (Karlsruhe); niezależny od HF | llama.cpp | 402 commity; CUDA, wielogpu, moduł GGUF; autor „meta backendu" (tensor parallel) |
| **Diego Devesa** (`slaren`) | brak pracodawcy w profilu | ggml | 362 commity; autor backendu/alokatora/schedulera ggml |
| **Jeff Bolz** (`jeffbolznv`) | NVIDIA *(profil)* | llama.cpp | 316 commitów; backend Vulkan |
| **Iwan Kawrakow** (`ikawrakow`) | niezależny („Gentleman at large") | ik_llama.cpp | autor k-quantów i i-quantów; 100 commitów w llama.cpp, opuścił projekt w marcu 2024 *(jego własne słowa w dyskusji #316)*; prowadzi fork ik_llama.cpp |
| **Benson Wong** (`mostlygeek`) | „Tailscale and Elethink" *(profil)* | llama-swap | 536 z ok. 653 commitów; wydania v262–v265 w październiku 2026 |
| **Jeffrey Morgan** (`jmorganca`) | współzałożyciel Ollama; wcześniej Docker, Twitter, Google *(profil)* | Ollama | 928 commitów; razem z Chiangiem Kitematic („przejęty przez Docker w 2015") *(dane firmy)* |
| **Michael Chiang** (`mchiang0610`) | współzałożyciel Ollama | Ollama | Kitematic → Docker Desktop *(dane firmy)* |
| **Woosuk Kwon** (`WoosukKwon`) | Inferact | vLLM | pierwszy autor artykułu o PagedAttention (arXiv 2309.06180); 873 commity; „lead maintainer" wg dokumentu zarządzania |
| **Simon Mo** | współzałożyciel Inferact, lead maintainer vLLM *(profil, strona Inferact)* | vLLM | wśród Core Maintainers (komitet techniczny projektu) |
| **Kaichao You** (`youkaichao`) | „Co-Founder & Chief Scientist" Inferact; doktorat Tsinghua *(profil)* | vLLM | 471 commitów |
| **Zhuohan Li** | profil: „vLLM / Meta" | vLLM | drugi autor artykułu o PagedAttention; lead maintainer vLLM wg dokumentu zarządzania |
| **Michael Goin** (`mgoin`) | Red Hat/Neural Magic *(profil)* | vLLM | 650 commitów (9% top-15) |
| **Ying Sheng** | CEO i współzałożycielka RadixArk; wcześniej xAI, Databricks *(prasa)* | SGLang | ostatnia autorka artykułu o SGLang; współautorka artykułu o vLLM |
| **Lianmin Zheng** (`merrymercy`) | profil: Meta | SGLang | pierwszy autor artykułu o SGLang; 1 267 commitów |
| **Liangsheng Yin** (`hnyls2002`) | RadixArk *(profil)* | SGLang | 1 205 commitów; drugi autor artykułu |
| **Chris Lattner** | EVP, Advanced AI Software and Platforms, Qualcomm (współzałożyciel Modular) | Modular, MAX/Mojo | rola potwierdzona na stronie Modular i w komunikacie o zamknięciu; wcześniejszego dorobku nie opisuję, bo w notatkach jest oznaczony jako niezweryfikowany |
| **Tim Davis** | współzałożyciel Modular → „SVP & GM of Modular, Qualcomm" | Modular | jw. |
| **Awni Hannun** (`awni`) | profil: „Research at Anthropic. Prev: co-created MLX at Apple" | MLX, mlx-lm | współautor artykułu o MLX (z Digani, Katharopoulos, Collobert); 718 commitów w MLX (#1), ostatni z adresu Apple 2026-02-24 |
| **Jun Kim** (`jundot`) | inżynier w Hugging Face od 2026-09-22 | oMLX | 2 110 z ok. 2 280 commitów top-5; blog HF z 2026-09-22 |
| **Salvatore Sanfilippo** (antirez) | Redis, deweloper-ewangelista na część etatu od listopada 2024 | ds4 | twórca Redis; w ds4 523 commity; argumentował za powrotem Redis z SSPL do AGPL (Redis 8, 2025-05-01) |
| **Eric Buehler** (`EricLBuehler`) | profil: `@huggingface` | mistral.rs | 3 073 commity (następny 125); 75 z 82 niebotowych commitów w ostatnich 90 dniach |
| **Eric Curtin** (`ericcurtin`) | profil: „Docker, Inc"; wcześniej `@redhat.com` | llmman, RamaLama, Docker Model Runner | 402 commity w llmman; 971 w RamaLama (#2); 318 w model-runner (#3) |
| **Dan Walsh** (`rhatdan`) | profil: „Retired" | RamaLama | 1 462 commity (#1) |
| **Ettore Di Giacinto** (`mudler`) | „ex-SUSE/Rancher, ex-gentoo" *(profil)* | LocalAI | 3 507 commitów |
| **Daniel Han** (`danielhanchen`) i **Michael Han** (`shimmyshimmer`) | współzałożyciele Unsloth AI Inc. (YC lato 2024) | Unsloth | 6 391 i 808 commitów; Daniel Han wg strony YC wcześniej w NVIDIA |
| **Justine Tunney** (`jart`) | autorka Cosmopolitan libc; Mozilla Builders | llamafile | 600 commitów; 42 sponsorów na GitHub Sponsors |
| **Timothy Baek** (`tjbck`) | założyciel Open WebUI Inc. | Open WebUI | 13 450 commitów; 42 sponsorów |
| **Alex Cheema** | exo labs (profil: „University of Oxford", prawdopodobnie nieaktualny) | exo | 1 424 commity |
| **Nat Friedman**, **Daniel Gross** | inwestorzy pre-seed ggml.ai (2023) | ggml.ai | *(dane firmy: ggml.ai)*, kwota nieujawniona |

**Czego tu nie ma.** Osób znanych w notatkach tylko z pseudonimu (m.in. `kyuz0`, `mitsuhiko` w ds4) i jakichkolwiek szczegółów prywatnych. Pełne imię Michaela Chianga pochodzi z Wikipedii *(źródło zewnętrzne)*; tytułu Yagila Burowskiego (LM Studio) nie ustaliłem.

> **Sprawdź sam — pracodawcy i adresy e-mail w commitach.** Profil to deklaracja, a adres w commicie to wskazówka niezależna od profilu:
> ```bash
> gh api 'repos/llmmanorg/llmman/commits?per_page=1' --jq '.[0].commit.author'
> gh api users/mostlygeek --jq '{name, company, location, bio}'
> gh api orgs/ggml-org --jq '{login, description, public_repos, created_at}'
> ```
> (nie uruchamiałem dokładnie w tej formie). W przeglądzie właśnie takie dane pokazały, że commity Erica Curtina do llmman w październiku 2026 mają domenę `@docker.com`, a do RamaLama w lipcu–sierpniu 2025 `@redhat.com`. Strona organizacji github.com/ggml-org mówi o „16 członkach zespołu rdzeniowego".

---

## 6. Licencje: tabela i pułapki

Licencje sprawdzałem w tekstach plików `LICENSE` (w drzewach na maszynie z kartami: `~/llama.cpp-0ce8cd1/LICENSE` i `~/runtimes-src/*/LICENSE` dla dziewięciu projektów; dla pozostałych — surowy plik z GitHuba, 2026-10-19). Kolumna „SPDX" to to, co zwraca API GitHuba; wartość `NOASSERTION` oznacza, że automat nie rozpoznał pojedynczej licencji, często dlatego, że plik ma nagłówek jednej licencji i dopiski.

| Projekt | SPDX (API) | Co wolno | Pułapki i uwagi |
|---|---|---|---|
| **llama.cpp, ggml, whisper.cpp** | MIT | prawie wszystko, z zachowaniem noty | „Copyright (c) 2023-2026 The ggml authors"; brak klauzuli patentowej; właścicielem organizacji jest dziś HF; marka (`llama.brand`) ma NOASSERTION, czyli *nie* jest objęta MIT |
| **ds4** | MIT | prawie wszystko | LICENSE zawiera trzy linie praw autorskich: autorzy ds4.c, autorzy ggml (2023–2026), DeepSeek (2023) — notatki wiążą to z zaadaptowanym kodem i formatem |
| **Ollama** | MIT | prawie wszystko | MIT dotyczy **kodu**; usługa chmurowa, rejestr modeli i warunki modeli hostowanych są osobne; **każdy model ma własną licencję**; notatki odnotowują otwarty od 2024-03-16 wątek #3185 o niedystrybuowaniu not licencyjnych w artefaktach wydań (stan na datę przeglądu: otwarty; czy naprawiono — nie ustaliłem) |
| **mistral.rs, LocalAI, MLX, mlx-lm, `lms` (CLI LM Studio), llama-swap, ik_llama.cpp, AnythingLLM, GPT4All, RamaLama** | MIT | prawie wszystko | MLX: „Copyright © 2023 Apple Inc."; produkt hostowany AnythingLLM jest osobno |
| **vLLM, SGLang, llmman, oMLX, Lemonade, Docker Model Runner, exo, KTransformers, llm-d, LMCache, mlc-llm, TGI** | Apache-2.0 | użycie komercyjne, zmiany, **udzielenie patentów** | klauzula odwetu patentowego; zachowaj plik NOTICE; vLLM jest własnością fundacji (PyTorch Foundation), SGLang — LMSYS |
| **TensorRT-LLM** | NOASSERTION (w istocie Apache-2.0 + noty) | jak Apache-2.0 | LICENSE = nagłówek Apache-2.0 + ok. 790 linii not stron trzecich (MIT, BSD-3, Apache); **telemetria** domyślnie włączona, opt-out opisany w README (kod w `tensorrt_llm/usage/`); działa tylko na GPU NVIDIA i zależy od zamkniętych bibliotek CUDA/TensorRT *(niezweryfikowane w plikach budowania)* |
| **Dynamo** | NOASSERTION (Apache-2.0 + nota o danych testowych) | jak Apache-2.0 | orkiestruje vLLM/SGLang/TRT-LLM |
| **Jan** | NOASSERTION (Apache-2.0 + zdanie o atrybucji) | jak Apache-2.0 | „Attribution is requested in user-facing documentation" — prośba, nie warunek licencji; prawa autorskie Menlo Research 2025 |
| **llamafile** | NOASSERTION w API; plik LICENSE = Apache-2.0, „Copyright 2023 Mozilla Foundation" | jak Apache-2.0 | zawiera llama.cpp (MIT), whisper.cpp (MIT), Cosmopolitan; wersja 0.10 ma nowy system budowania |
| **Open WebUI** | NOASSERTION („Open WebUI License") | prawa BSD-3 **plus** klauzula 4 | **nie wolno zmieniać, usuwać ani zastępować marki „Open WebUI"**, chyba że: ≤ 50 użytkowników końcowych w ciągu 30 dni, pisemna zgoda lub licencja enterprise; CLA dla kontrybutorów; kod do v0.6.5 pozostaje BSD-3, wcześniej MIT (LICENSE_HISTORY); **nie jest to licencja zatwierdzona przez OSI** |
| **Modular (repozytorium)** | NOASSERTION: Apache-2.0 **z wyjątkami LLVM** | jak Apache-2.0 + wyjątek LLVM | **MAX** jest na „Modular Community License": bezpłatna, bez limitu akceleratorów (dawny limit „ośmiu akceleratorów poza x86, ARM i NVIDIA" zniknął), ale **udostępnianie MAX jako hostowanej usługi innym podmiotom wymaga zgody pisemnej i zgodności ze znakiem**; nie wolno używać MAX jako danych treningowych do zbudowania zamiennika *(streszczenie strony licencji)* |
| **LiteLLM** | NOASSERTION (MIT + katalog `enterprise/`) | MIT poza `enterprise/` | zawartość `enterprise/` „tylko do produkcji" z subskrypcją BerriAI (per miejsce) |
| **Unsloth** | Apache-2.0 (korzeń) | rdzeń Apache-2.0 | `studio/` na **AGPL-3.0-only** (Unsloth AI Inc.) — copyleft sieciowy: wbudowanie Studio w zamknięty produkt hostowany odpada |
| **LM Studio (aplikacja)** | — (EULA zamknięta) | użytek osobisty i „wewnętrzny biznesowy" (bezpłatnie do pracy od 2025-07-08) | brak redystrybucji, brak inżynierii wstecznej, brak SaaS/biura usług; odpowiedzialność ograniczona do 50 USD; warunki mogą się zmienić; **wolność „do pracy" to wpis na blogu, nie umowa** |
| **KoboldCpp** | AGPL-3.0 | użycie i zmiany | copyleft sieciowy dla hostowanych forków |
| **Redis (kontekst)** | AGPLv3 jako opcja od Redis 8 (2025-05-01) | — | historia: SSPL (marzec 2024) → AGPL; relicencjonowanie bywa dwukierunkowe |

**Wagi modeli to osobna warstwa prawna.** Wszystkie powyższe licencje dotyczą **kodu**. Plik modelu (np. referencyjny DeepSeek-V4-Flash w kwancie `UD-IQ3_XXS`) ma własną licencję wag i — jeśli pochodzi z repozytorium Unsloth — jest *pochodną* oryginalnych wag, więc obowiązują warunki bazowego modelu. **Notatki nie zawierają treści licencji wag DeepSeek ani opisu warunków repozytoriów Unsloth z GGUF-ami. Nie ustaliłem ich** i nie będę zgadywać. Sprawdź je u źródła (box niżej).

> **Sprawdź sam — licencje.**
> ```bash
> # 1. co mówi GitHub o licencji kodu
> gh api repos/ggml-org/llama.cpp --jq '.license.spdx_id'
> gh api repos/open-webui/open-webui --jq '.license.spdx_id'      # spodziewaj się NOASSERTION
> # 2. pełny tekst — to on rozstrzyga, nie pole SPDX
> curl -s https://raw.githubusercontent.com/open-webui/open-webui/main/LICENSE | head -60
> # 3. historia zmian licencji Open WebUI (plik wymieniony w notatkach)
> curl -s https://raw.githubusercontent.com/open-webui/open-webui/main/LICENSE_HISTORY | head -60
> # 4. na maszynie z kartami
> head -5 ~/llama.cpp-0ce8cd1/LICENSE
> ```
> (nie uruchamiałem tych poleceń w tej formie; nazwy plików `LICENSE` i `LICENSE_HISTORY` oraz gałąź `main` są założeniem — jeśli `main` nie istnieje, sprawdź gałąź domyślną). Dla modelu: otwórz **kartę modelu i plik LICENSE** w repozytorium bazowego modelu DeepSeek-V4-Flash na Hugging Face oraz w repozytorium Unsloth z referencyjnym plikiem GGUF i porównaj. W tej sprawie nie mam danych z przeglądu.

---

## 7. Ryzyko zależności: co się stanie ze stosem referencyjnym

### 7.1 Dziesięć wzorców „idź za pieniędzmi" i ich konsekwencje

| # | Wzorzec | Mechanizm | Przykłady | Co to znaczy dla zależnego użytkownika |
|---|---|---|---|---|
| 1 | **Przejęcie opiekunów przez platformę** | hub lub chmura wchłania projekt prowadzony przez założyciela; kod zostaje otwarty, roadmapa zbliża się do platformy | ggml.ai→HF (2026-02-20); oMLX→HF (2026-09-22); mistral.rs→HF (profil); Neural Magic→Red Hat; Modular→Qualcomm | niskie ryzyko porzucenia, **średnie ryzyko sterowania**; zachowaj możliwość forka MIT/Apache; obserwuj łańcuch własności (HF→NVIDIA — doniesienia) |
| 2 | **Sprzęt ciągnie oprogramowanie** | software darmowy, bo sprzedaje krzem | NVIDIA (TRT-LLM, Dynamo, NIM→AI Enterprise); AMD (Lemonade, wkład w vLLM-ROCm); Apple (MLX); Qualcomm (Modular); Intel/AMD/Google jako sponsorzy vLLM | funkcje podążają za produktami dostawcy; ścieżki AMD są lubiane tam, gdzie AMD coś sprzedaje (Instinct, Strix Halo, Ryzen AI) — karty R9700 są pośrodku |
| 3 | **Neutralność fundacji** | projekt do neutralnego domu prawnego | vLLM→PyTorch Foundation (2025-05-06), LF AI & Data (2024); SGLang→LMSYS; (llama.cpp **nie** jest w fundacji, dom korporacyjny to HF) | najlepsza ochrona przed zmianą licencji; **nie** chroni przed koncentracją pracodawców |
| 4 | **VC + darmowy open source + chmura jako dosprzedaż** | darmowy runtime to lejek; przychód z użycia hostowanego | Ollama, LM Studio (Bionic/Teams), AnythingLLM (hostowany), Inferact Cloud, hosting RadixArk | lokalna aplikacja jest wabikiem; obserwuj domyślne okna logowania, telemetrię, ekrany „zaloguj się do chmury" |
| 5 | **Silnik → startup → platforma firmowa** | silnik oddany fundacji, założyciele robią firmę | Inferact, RadixArk, Together, Fireworks, Baseten, Modal | dla centrum danych w porządku; dla lokalnych maszyn istotne tylko przez wspólny kod silnika |
| 6 | **Open-core / source-available / zamek marką** | rdzeń wolny, element strategiczny z ograniczeniem | Open WebUI (v0.6.6, 2025-04-19), LiteLLM (`enterprise/`), Unsloth (Studio AGPL), Modular Community License | czytaj licencję przy każdym osadzaniu i redystrybucji; „open source w sensie OSI" przestało być bezpiecznym założeniem |
| 7 | **Subskrypcja dystrybucji otwartego silnika** | klienci płacą za wsparcie, odszkodowanie, certyfikację | Red Hat AI Inference (per akcelerator), NVIDIA AI Enterprise (4 500 USD/GPU/rok), Docker Desktop (Model Runner jako funkcja) | adoptujący w korporacjach pójdą tą drogą; hobbystyczne i devopsowe maszyny nie muszą |
| 8 | **Projekt korporacyjny z pracownikami** | jedna firma pisze większość commitów | Ollama, TRT-LLM, MLX (Apple), Lemonade (AMD), Docker Model Runner | szybki i spójny; podlega zmianom strategii sponsora i zwolnieniom (przykład: odejście Awniego Hannuna z Apple do Anthropic) |
| 9 | **BDFL na sponsoringu albo po godzinach** | jedna osoba, mało lub zero finansowania | antirez/ds4, mudler/LocalAI, llama-swap, llmman, ik_llama.cpp | wysokie tempo, współczynnik autobusu (*bus factor*) = 1; MIT/Apache pozwalają na fork, ale nie bezboleśnie |
| 10 | **Pivot albo zombie** | firma znajduje lepszy rynek, aktywo OSS „parkuje" | Nomic→AEC (GPT4All: ostatni push 2025-05-27); Menlo (Jan)→roboty humanoidalne; TGI zarchiwizowany; llamafile „odświeżony" przez Mozilla.ai | nie opieraj krytycznych procesów na projektach napędzanych marketingiem bez sprawdzenia daty ostatniego commitu |

### 7.2 Stos referencyjny, element po elemencie

Skala ryzyka poniżej jest **moją oceną** opartą na faktach z sekcji 2–6, nie pomiarem.

| Element | Kto za nim stoi | Jeśli zostanie przejęty | Jeśli zmieni licencję | Jeśli zostanie porzucony | Koszt wyjścia |
|---|---|---|---|---|---|
| **llama.cpp** (MIT; build `0ce8cd1` na maszynie referencyjnej — w przeglądzie to jest wersja produkcyjna) | zespół ggml.ai w HF; 24,5 tys. forków | HF→NVIDIA *(doniesienia)*: licencja bez zmian; ryzyko to **sterowanie roadmapą** | wydane wersje MIT nie przestają być MIT (zasada ogólna; przykład z notatek: Open WebUI — kod ≤ v0.6.5 został BSD-3 mimo późniejszej zmiany); realne zagrożenie dotyczy *przyszłych* wersji | niskie: 73% commitów top-12 od ludzi z pensją HF; ale **jeden pracodawca** | **niski**, jeśli przypinasz build i trzymasz kopię źródeł |
| **Backend HIP / gfx1201** | kod CUDA kompilowany jako HIP; gałęzie RDNA4 w `common.cuh`; CODEOWNERS dla CUDA: Gäßler, am17an, IMbackK, ORippler | CUDA-first w HF/NVIDIA dotyka też ciebie, ale ścieżka AMD „jedzie" na wspólnym kodzie | j.w. | najbardziej zależy od kilku osób; pracodawców części z nich notatki nie podają | średni: przejście na Vulkan (backend utrzymują m.in. 0cc4m i Jeff Bolz z NVIDIA) |
| **llama-swap** (MIT, 6,0 tys. gwiazdek) | **jeden** maintainer (82% commitów), pracuje gdzie indziej; 0 sponsorów | nie dotyczy (osoba, nie firma) | MIT, mały kod Go | **realne**: jeden punkt awarii; cykl wydań co kilka dni to dziś plus | **niski–średni**: wbudowany router llama.cpp (`--models-dir`, `--models-max` domyślnie 4, eksmisja LRU) pokrywa zwykłe przełączanie; tracisz grupy/macierz (`matrix`) do układania modeli na czterech GPU, upstreamy inne niż llama i UI |
| **GGUF-y Unsloth** (`UD-…`) | Unsloth AI Inc. (YC, 12 osób wg strony YC); Daniel Han ≈ 56% commitów repo | firma kupiona: *istniejące pliki nie zmieniają się*; ryzyko dotyczy przyszłych wydań i warunków | pliki już pobrane zostają; zmiana dotyczyłaby nowych | tracisz **szybkie kwanty nowych modeli i poprawki** (docs: pomogli naprawiać błędy llama.cpp — *(dane firmy)*) | **niski dla działania**, **średni dla odtwarzalności**: „UD-" i `_XL` to etykiety Unsloth (llama.cpp nie ma typu `Q4_K_XL`; nagłówek GGUF trzyma najbliższy standardowy typ, np. `file_type = 23` = `MOSTLY_IQ3_XXS`), więc plik czyta zwykły llama.cpp; **narzędzi receptury nie ma w publicznym repo**, więc nie odtworzysz identycznej mieszanki — możesz ją naśladować `llama-quantize --imatrix … --tensor-type <regex>=<typ>`; w repozytorium, które sprawdziłem (Qwen3-Coder-30B-A3B), plik imatrix (122 MB) jest opublikowany; **dla referencyjnego pliku DeepSeek tego nie sprawdzałem** |
| **Wagi DeepSeek (licencja)** | DeepSeek; pochodne: Unsloth | — | — | — | **nie ustaliłem** (brak w notatkach); zob. sekcja 6 |
| **Hugging Face jako Hub** | HF (wycena 4,5 mld USD w 2023 *(prasa)*; doniesienia o 12,93 mld od NVIDIA) | jeśli doniesienia się potwierdzą: zmiana właściciela dostawcy, z którego pobierasz modele; warunki Hubu i dostępność nie są w notatkach | — | — | trzymaj lokalne kopie plików (zob. lista niżej) |

**Strona Maców.**

| Element | Sponsor i ryzyko | Koszt wyjścia |
|---|---|---|
| **MLX / mlx-lm** (MIT) | Apple płaci rdzeniowy zespół (zcbenz, angeloskath, jagrit06 — *(profil)*); współtwórca odszedł; Apple może zmniejszyć inwestycję w każdej chwili. Łagodzi: ekosystem (HF/oMLX, LM Studio, podgląd MLX w Ollama 2026-03-30) od niego zależy, więc utrzymanie społecznościowe jest prawdopodobne *(niezweryfikowane)* | niski (MIT) |
| **oMLX** (Apache-2.0) | od 2026-09-22 finansowany przez HF; ryzyko przesunęło się od „hobbysta się wypali" do „roadmapa podąża za HF" | niski |
| **LM Studio** (zamknięty) | Element Labs, finansowanie nieznane; bezpłatność do pracy to wpis, nie umowa; zamrożenie binarek, jeśli usługa stanie | **niski**: modele leżą jako zwykłe pliki w `~/.lmstudio/models`; ale GUI i demona się nie sforkuje |
| **Ollama** (MIT kod) | VC, chmura; „fosą" jest biblioteka modeli, szablony, parsery, chmura; cennik już raz zmieniono (czas GPU → tokeny, 2026-08-31); okno logowania do chmury jest w domyślnym przepływie, jest zmienna `OLLAMA_NO_CLOUD` | **średni**: modele w układzie blobów wymagają re-eksportu; fork kodu możliwy |
| **ds4** (MIT) | hobby jednej osoby; ~24 tys. gwiazdek, ok. 2,3 tys. forków; kod mały i czytelny; **na AMD: wspierany jest `gfx1151` (Strix Halo), a nie `gfx1201` karty R9700** — zob. `07-APPLE-MLX-OMLX-I-DS4.md` | niski |

**Gdybyś kiedyś przeszedł na vLLM:** najlepiej chroniony z silników centrum danych (Apache-2.0 + fundacja + wielu korporacyjnych committerów); połowa pracy rdzeniowej jest dziś wykonywana przez pracowników jednej firmy (Inferact), a drugi krąg to Red Hat, AMD, HF i Meta. Inżynier AMD jest #9 wśród committerów, więc ROCm jest finansowane przez AMD — ale roadmapa Inferact to według komunikatów firmy TPU i Instinct, nie RDNA4 *(niezweryfikowane)*. **Domyślnie włączona telemetria**: vLLM wysyła statystyki użycia (wyłączenie: `VLLM_NO_USAGE_STATS=1` lub `DO_NOT_TRACK=1`), TensorRT-LLM także (`TRTLLM_NO_USAGE_STATS=1`, `DO_NOT_TRACK=1`, `--no-telemetry`); dla SGLang nie znalazłem telemetrii. To mały, widoczny w kodzie przykład motywacji organizacji. Zob. `06-SILNIKI-SERWEROWE-VLLM-SGLANG.md`.

### 7.3 Lista zabezpieczeń

1. **Przypinaj wersje.** Już to robisz dla llama.cpp (`0ce8cd1`). Zapisuj też wersje llama-swap (wydania mają kolejne numery całkowite, np. v265 z 2026-10-14) i hashe plików GGUF.
2. **Trzymaj lokalną kopię** źródeł przypiętego commitu, pliku `LICENSE` i plików GGUF, na których opierasz produkcję. Hub to usługa cudza.
3. **Zapisz, kto jest właścicielem każdego elementu stosu** (jedno zdanie, z datą) — tabela 7.2 to szablon. Powtarzaj co kwartał.
4. **Obserwuj sygnały wczesne**: zmianę pola `company` u głównych committerów, nowe pliki `LICENSE*`, archiwizację repozytoriów (jak TGI), „pivot" w opisie firmy.
5. **Przy każdym nowym narzędziu pięć pytań**: kto płaci twórcom? z czego firma zarabia? jaka licencja (przeczytaj tekst)? jaki jest *bus factor*? jakie jest wyjście (format modeli, API)?
6. **Preferuj formaty otwarte i API zgodne z OpenAI/Anthropic** — to obniża koszt wyjścia z każdego opakowania (zob. `05-OPAKOWANIA-OLLAMA-LM-STUDIO-I-INNE.md`).

> **Sprawdź sam — czy wątek o licencjach w Ollama jest nadal otwarty.** Notatki odnotowują, że zgłoszenie #3185 („ollama doesn't distribute notice licenses in its release artifacts", otwarte 2024-03-16, 59 komentarzy) było otwarte na dzień przeglądu:
> ```bash
> gh api repos/ollama/ollama/issues/3185 --jq '{state, comments, title}'
> ```
> (nie uruchamiałem tego wywołania). To przykład „sprawdzam stan wątku zamiast powtarzać opinię". Notatki odnotowują też argument drugiej strony: README Ollama zawiera dziś sekcję „Supported backends" z podziękowaniem dla projektu llama.cpp i Georgiego Gerganova.

> **Sprawdź sam — czy NVIDIA–HF jest potwierdzone u źródła.** Otwórz `nvidianews.nvidia.com` i `huggingface.co/blog` i poszukaj komunikatu z końca sierpnia / początku września 2026. W momencie przeglądu **nie znalazłem żadnego** — dlatego tekst mówi „według doniesień prasowych". Jeśli komunikat już jest, zaktualizuj sekcję 3.2.

### 7.4 Co z tego dla konfiguracji 4× R9700 + Mac (z aplikacjami agentowymi)

- **Największe pojedyncze ryzyko operacyjne nie jest w tym, co głośne** (HF/NVIDIA), tylko w tym, co ciche: **llama-swap = jedna osoba**. Dobra wiadomość: wyjście jest tanie, bo llama.cpp ma własny router; zły scenariusz to utrata układania modeli (`matrix`) na czterech GPU, nie utrata działania.
- **llama.cpp jest dziś najlepiej „sfinansowanym" elementem stosu referencyjnego** (pensje w HF), a jednocześnie najbardziej narażonym na zmianę właściciela. Dla produkcji liczy się przypięcie wersji i kopia źródeł, nie dyskusje o intencjach.
- **Karty R9700 prawdopodobnie nie są dla nikogo celem strategicznym** *(niezweryfikowane — wniosek z tego, gdzie AMD deklaruje inwestycje: Instinct, Strix Halo, Ryzen AI)*: ani NVIDIA, ani Apple tu nie zależy, a AMD sprzedaje przede wszystkim te trzy linie. Ścieżka HIP w llama.cpp działa, bo współdzieli kod CUDA. Nie licz na to, że ktoś będzie ją dopieszczał pod RDNA4 z powodów biznesowych.
- **Mac:** najmniej ryzykowne są formaty (pliki GGUF i wagi MLX leżą na dysku), najbardziej — aplikacje zamknięte i chmurowe dosprzedaże. Wybieraj narzędzia, z których da się wyjść plikiem.

---

## 8. Czego możesz się nauczyć do własnych planów

Ta sekcja jest dla osób, które budują aplikacje agentowe na lokalnych modelach i myślą o asystencie po polsku. Poniżej **wyłącznie lekcje z opisanych przypadków**. **Notatki nie zawierają żadnych danych o rynku polskim, o polskojęzycznych modelach, o polskich programach finansowania ani o gotowości klientów do płacenia** — nic z tego tu nie wyliczam i niczego nie oszacowuję. Gdzie coś wymagałoby takich danych, piszę „do sprawdzenia przez ciebie".

### 8.1 Siedem lekcji z przypadków

1. **Najpierw odpowiedz: kto płaci za twój czas za rok?** Projekty, które (moja synteza przypadków z sekcji 2) przetrwały z płatnymi opiekunami, miały jedno z trzech: producenta sprzętu (AMD, NVIDIA, Apple), platformę (HF, Red Hat, Docker) albo VC z chmurą (Ollama, Inferact). Projekty prowadzone po godzinach (ds4, llama-swap, LocalAI) mają świetne tempo i współczynnik autobusu równy 1. To nie ocena jakości, tylko opis ryzyka.
2. **Darmowa aplikacja lokalna jest lejkiem — musi mieć coś płatnego na końcu.** Ollama (chmura od 20 USD/mies.), LM Studio (Bionic, Teams), AnythingLLM (hostowany zespół) sprzedają **hostowane modele i funkcje zespołowe**, a nie samą aplikację. Cena uboczna: okna logowania i domyślne ścieżki do chmury (wymusiło to opcję `OLLAMA_NO_CLOUD`). Użytkownicy lokalnych narzędzi czytają takie sygnały.
3. **Odbierz tarcie jednostkom, pobieraj od organizacji za kontrolę.** LM Studio zniosło formularz dla użytku w pracy (2025-07-08), a płatne są plany Teams/Enterprise (SSO, bramkowanie modeli i MCP, zerowa retencja); Open WebUI sprzedaje SSO/SCIM, białą etykietę i izolowane terminale; Red Hat sprzedaje wsparcie liczone od akceleratora; NVIDIA — wspierany kontener. **To, za co organizacje płacą w tych przypadkach, to kontrola, zgodność i wsparcie — nie sama szybkość tokenów.**
4. **Licencja jest narzędziem biznesowym, wybierz ją wcześnie i świadomie.** Open WebUI przeszedł z MIT na BSD-3 i potem (v0.6.6, 2025-04-19) na licencję z klauzulą o marce, a CLA pozwala na dalsze zmiany; Unsloth rozdzielił rdzeń (Apache-2.0) od Studio (AGPL-3.0); Redis przeszedł SSPL → AGPL. Dla założyciela to elastyczność; dla adoptującego — ryzyko, o którym piszesz w sekcji 6. Jeśli zbudujesz własne narzędzie, zadaj sobie to samo pytanie z perspektywy *swojego* użytkownika.
5. **Pivot jest widoczny w dacie ostatniego commitu.** GPT4All (2025-05-27), Jan/Menlo (roboty), TGI (archiwum) pokazują, że aplikacja będąca lejkiem dla innego biznesu zamiera, gdy biznes się zmienia. Jeśli twój asystent ma być lejkiem do czegoś innego, powiedz to wprost użytkownikom.
6. **Neutralny dom chroni licencję, nie roadmapę.** vLLM (PyTorch Foundation) i SGLang (LMSYS) mają niskie ryzyko relicencjonowania, a mimo to największy blok committerów to pracownicy jednej firmy. Jeśli chcesz kontrybutorów z zewnątrz, neutralność ma znaczenie; jeśli chcesz kontrolować kierunek, trzeba to zrobić świadomie.
7. **Usługi wokół wdrożenia są realnym modelem — ale tylko tam, gdzie klient ma sprzęt albo wymogi zgodności.** Inferact oferuje „platformę na twoich zasobach" i chmurę na własnych GPU, Red Hat — wsparcie, NVIDIA — wspierane kontenery. Wszystkie trzy są zbudowane na **dużej skali wdrożeń**; czy to skaluje się w dół do pojedynczych firm lokalnych — **nie wynika z notatek**.

### 8.2 Hipotezy do przetestowania (nie rekomendacje)

Poniższa tabela zestawia modele przychodu z przypadkami, które je popierają i które przed nimi ostrzegają, oraz z tym, **czego musiałbyś się dowiedzieć sam**. Żadnych liczb rynkowych.

| Model przychodu dla asystenta lokalnego po polsku | Przypadek na „tak" | Przypadek na „uwaga" | Do sprawdzenia przez ciebie |
|---|---|---|---|
| darmowy asystent + płatna wersja zespołowa/firmowa (SSO, polityki, audyt) | LM Studio (free-for-work + Teams/Enterprise), Open WebUI Enterprise | warunki „free" mogą się zmienić (wpis, nie umowa); Open WebUI zaostrzył licencję po adopcji | czy twoi użytkownicy to organizacje wymagające kontroli; kto podejmuje decyzję zakupową |
| usługi wdrożeniowe i wsparcie dla firm uruchamiających lokalnie | Red Hat AI Inference, Inferact Platform, NVIDIA AI Enterprise | wszystkie opierają się na skali i sprzęcie dużych klientów | czy istnieje popyt na wsparcie dla małych instalacji; ile kosztuje twój czas |
| hostowana wersja tych samych modeli (chmura) obok lokalnej | Ollama Cloud, LM Studio Bionic, AnythingLLM hostowany | konkurujesz z wielkimi hostami (Together, Fireworks, Baseten, Modal), których wyceny są o rząd wielkości wyższe | kto jest twoim klientem, gdy lokalne wykonanie jest jego powodem zakupu |
| dwie licencje (rdzeń otwarty + interfejs na AGPL) | Unsloth (Apache-2.0 + AGPL Studio) | „open source" w sensie OSI staje się mniej oczywiste (Open WebUI) | czy twoi klienci akceptują AGPL; co z kontrybutorami (CLA?) |
| sponsoring / granty (finansowanie bez produktu) | LocalAI (Spectro Cloud), oobabooga (grant a16z 2023), Mozilla.ai (zobowiązanie 30 mln USD) | małe kwoty i niepewna ciągłość; w notatkach: 10–53 sponsorów na projekt | czy istnieją polskie/unijne programy — **notatki o tym milczą** |

---

**Gdzie dalej.** Porównanie technicznych właściwości silników i wybór dla maszyny referencyjnej: `09-POROWNANIE-I-WYBOR.md`. Lista źródeł i ich ocena: `ZRODLA.md`. Wróć do mapy warstw: `01-MAPA-I-WARSTWY.md`.
