# Tanie i darmowe modele online dla agentów — 20 najlepszych tras (październik 2026)

Moje aplikacje agentowe stoją na trzech nogach: komercyjne API klasy frontier (Claude Opus jako planista), mój lokalny
zestaw (4× AMD Radeon AI PRO R9700 z DeepSeek-V4-Flash-0731) oraz **tanie lub darmowe modele online**. Ten przegląd
dotyczy trzeciej nogi: gdzie za niewielkie pieniądze albo za darmo dostać inferencję online na modelach **co najmniej
tak mądrych jak mój lokalny DeepSeek-V4-Flash** i na ile można jej zaufać w pętli agenta.

Wszystkie fakty, ceny i limity sprawdziłem **13.10.2026**. Ten rynek zmienia się co tydzień: sprawdź ponownie, zanim
oprzesz się na którejkolwiek liczbie z tego tekstu. Do tych tras trafiają wyłącznie dane niewrażliwe. Dane klientów i
dane służbowe zostają na modelach lokalnych (zob. [../asystenci-ai/README.md](../asystenci-ai/README.md)).

## Najkrótsza odpowiedź

- **Poprzeczka to AA 34.** Tyle ma DeepSeek-V4-Flash-0731 w Artificial Analysis Intelligence Index v4.3.2 („AA”).
  Oryginalny kwietniowy V4-Flash ma w tym samym indeksie 24, a V4.1-Flash 39. Zawsze porównuj liczby tylko z jednej
  wersji indeksu; szczegóły w [02-MODELE.md](02-MODELE.md).
- **„Darmowe” oznacza dziś przeważnie „poniżej poprzeczki”.** Darmowe modele, które zostały jeszcze na OpenRouter
  (Inkling, Nemotron 3 Ultra, gpt-oss-120b, Gemma 4), mają AA 12–26. GitHub Models wycofano 30.07.2026, Hugging Face
  zrezygnował z darmowych kredytów 7.10.2026, darmowy plan Qwen Code skończył się 15.04.2026.
- **„Tanie” to prawdziwa trzecia noga.** GLM-5.3-Flash (AA 42) kosztuje 0,15 / 0,50 USD za 1M tokenów, DeepSeek
  V4.1-Flash (AA 39) 0,15 / 0,60 USD poza godzinami szczytu, MiMo-V2.6-Pro (AA 46) 0,435 / 0,87 USD. Tysiąc długich
  zadań agentowych kosztuje od kilku do kilkudziesięciu dolarów.
- **Najmocniejsza darmowa trasa to NVIDIA build.nvidia.com** (GLM-5.3, Kimi K3, V4.1-Flash za darmo przy około 40 RPM),
  ale jej warunki pozwalają tylko na prototypowanie, a pod obciążeniem ustawia żądania w kolejce.
- **Host ma takie samo znaczenie jak model.** Ten sam model GLM uzyskał 73% u jednego hosta i 100% u innego w teście
  dokładności endpointów Artificial Analysis. Przypinaj dostawców i kwantyzację, najpierw uruchom test akceptacyjny
  ([03-UZYCIE-W-AGENTACH.md](03-UZYCIE-W-AGENTACH.md)).
- **Płaskie plany do kodowania przeważnie nie są dla własnych agentów.** GLM Coding Plan, Kimi Code, Alibaba Coding
  Plan i MiMo Token Plan ograniczają użycie do obsługiwanych narzędzi do kodowania. Ollama Cloud pozwala na użycie przez API.
- **Mój domyślny wybór:** OpenRouter jako router z przypiętymi dostawcami, GLM-5.3-Flash i DeepSeek V4.1-Flash jako
  tani wykonawcy, MiMo-V2.6-Pro albo GLM-5.3 do trudniejszych kroków, darmowe plany tylko jako przelew nadmiaru i do ewaluacji.

## Ranking: 20 najlepszych

Wynik na 100 punktów (metoda poniżej). Cena = USD za 1M tokenów, wejście / wyjście, dla najlepszego modelu w paśmie.
„Dane” to tylko flaga (czy trasa domyślnie trenuje na promptach), nie część wyniku.

| # | Trasa | Typ | Najlepsze modele w paśmie (AA) | Cena lub darmowy limit | Dane | Wynik |
|---|---|---|---|---|---|---|
| 1 | [OpenRouter](01-PROFILE.md#1-openrouter) | agregator, płatność za użycie | MiMo-V2.6-Pro (46), GLM-5.3 (45), GLM-5.3-Flash (42) | od 0,045 / 0,15; 1000 darmowych żądań/dzień po jednorazowych 10 USD | zależnie od dostawcy; przełączniki | 93 |
| 2 | [DeepInfra](01-PROFILE.md#2-deepinfra) | host, płatność za użycie | MiMo-V2.6-Pro (46), V4.1-Flash (39), V4-Flash-0731 (34) | od 0,06 / 0,18 (0731) do 0,435 / 0,87 | bez trenowania | 90 |
| 3 | [Fireworks AI](01-PROFILE.md#3-fireworks-ai) | host, płatność za użycie | GLM-5.3-Flash (42), V4.1-Flash (39) | 0,15 / 0,50 | nie przechowuje | 89 |
| 4 | [Z.ai (GLM) API](01-PROFILE.md#4-zai-glm-api) | dostawca własny | GLM-5.3-Flash (42) | 0,15 / 0,50 | bez trenowania (API) | 87 |
| 5 | [Parasail](01-PROFILE.md#5-parasail) | host, płatność za użycie | GLM-5.3-Flash (42), V4-Flash-0731 (34) | 0,14 / 0,28 (0731) | nieznane | 87 |
| 6 | [DeepSeek API](01-PROFILE.md#6-deepseek-api) | dostawca własny | V4.1-Flash (39) | 0,15 / 0,60 poza szczytem, 0,30 / 1,20 w szczycie | domyślnie trenuje, opt-out; ChRL | 85 |
| 7 | [Alibaba Cloud Model Studio](01-PROFILE.md#7-alibaba-cloud-model-studio-international) | dostawca własny + okres próbny | Qwen3.8-Max, GLM-5.3 (45) w okresie próbnym; Qwen3.8-Flash (40) | 1M darmowych tokenów na model przez 90 dni; 0,15 / 0,47 | bez trenowania; Singapur | 85 |
| 8 | [Xiaomi MiMo API](01-PROFILE.md#8-xiaomi-mimo-api) | dostawca własny | MiMo-V2.6-Pro (46) | 0,435 / 0,87 | bez trenowania (podsumowanie zewnętrzne) | 83 |
| 9 | [Together AI](01-PROFILE.md#9-together-ai) | host, płatność za użycie | GLM-5.3-Flash (42), V4-Flash-0731 (34) | 0,14 / 0,28 (0731) | domyślnie przechowuje, przełącznik ZDR | 82 |
| 10 | [NVIDIA build.nvidia.com](01-PROFILE.md#10-nvidia-buildnvidiacom-nim-trial-api) | darmowe próbne API | GLM-5.3 (45), Kimi K3 (44), V4.1-Flash (39) | za darmo, ~40 RPM, tylko prototypowanie | może służyć do ulepszania | 79 |
| 11 | [Vercel AI Gateway](01-PROFILE.md#11-vercel-ai-gateway) | agregator + darmowy kredyt | GLM-5.3-Flash (42) | 5 USD za darmo co 30 dni | zakładaj trenowanie, chyba że ZDR | 77 |
| 12 | [Kilo Gateway](01-PROFILE.md#12-kilo-gateway) | darmowa promocja | Step 5 Preview (44), Ling 3.1 Flash (41) | za darmo, 200 żądań/godzinę na IP, bez klucza | może trenować | 75 |
| 13 | [Ollama Cloud](01-PROFILE.md#13-ollama-cloud) | płaski plan z kredytami | GLM-5.3 (45), Kimi K3 (44) | Pro 20 USD/miesiąc = 60 USD kredytów | nigdy nie loguje | 74 |
| 14 | [Requesty](01-PROFILE.md#14-requesty) | agregator, darmowy plan | Ling 3.1 Flash (41) | 200 darmowych żądań/dzień, bez karty; endpoint w UE | bez retencji (metadane) | 72 |
| 15 | [Scaleway Generative APIs (EU)](01-PROFILE.md#15-scaleway-generative-apis-eu) | host w UE | V4.1-Flash (39) | 0,60 / 1,80 EUR; jednorazowo 1M darmowych tokenów | bez retencji; Paryż | 72 |
| 16 | [StepFun API and Step Plan](01-PROFILE.md#16-stepfun-api-and-step-plan) | dostawca własny + płaski plan | Step 5 Preview (44) | 1,00 / 2,70; plan od 6,99 USD | nieznane | 71 |
| 17 | [OpenCode Zen](01-PROFILE.md#17-opencode-zen) | darmowa promocja | Muse Spark 1.3 Contributor (45, trenuje), Step 5 Preview (44) | za darmo, limity nieopublikowane | zależnie od modelu | 70 |
| 18 | [Gemini API free tier](01-PROFILE.md#18-google-gemini-api-free-tier) | darmowy plan | Gemini 3.8 Flash (41) | za darmo, ~20 żądań/dzień | bez trenowania w EOG | 68 |
| 19 | [Groq (free tier)](01-PROFILE.md#19-groq-free-tier) | darmowy plan | Qwen3.8-27B (34) | za darmo, 1000 żądań/dzień, 200K tokenów/dzień | domyślnie bez retencji | 66 |
| 20 | [Cerebras Inference](01-PROFILE.md#20-cerebras-inference) | okres próbny + płatność za użycie | Qwen3.8-27B (34) przy ~1850 tok/s | 0,99 / 1,49; okres próbny 1M tokenów/dzień | bez retencji | 66 |

## Jak oceniałem

| Kryterium | Punkty | Co się liczy |
|---|---|---|
| Jakość modelu | 30 | AA najlepszego modelu, którego naprawdę można użyć na tej trasie w ramach budżetu: AA 34 = 18 punktów, +1 za każdy punkt AA, 30 przy AA 46 lub więcej |
| Efektywny koszt | 20 | cykliczne darmowe = 20; promocja lub jednorazowo za darmo 16–18; płatność za użycie wg ceny wyjścia (≤0,6 → 18–19, ≤1 → 16, ≤2 → 13, ≤3 → 10–11) |
| Limity | 15 | wolumen użyteczny dla pętli agentów: RPM, żądania i tokeny na dzień, współbieżność |
| Przydatność dla agentów | 20 | wywoływanie narzędzi, kontekst i maksymalne wyjście, endpointy zgodne z OpenAI/Anthropic, wyjście strukturalne, zmierzona dokładność wywołań narzędzi |
| Niezawodność | 15 | dane o dostępności, rotacja katalogu, status preview, jak często zmieniały się limity lub warunki |

„W paśmie” oznacza wyjście najwyżej około 3 USD za 1M tokenów albo trasę darmową lub płaską. Warunki dotyczące danych
pokazuję jako flagę, bo wysyłam tu tylko dane niewrażliwe.

## Która trasa do jakiego zadania

| Zadanie | Pierwszy wybór | Zapas |
|---|---|---|
| Masowa ekstrakcja, klasyfikacja, podsumowania | GLM-5.3-Flash w Fireworks lub Z.ai | V4-Flash-0731 w DeepInfra (0,06 / 0,18) |
| Podagent do kodowania, zadania w terminalu | GLM-5.3 przez hosty OpenRouter (najlepszy niezależny Terminal-Bench 4.0) | GLM-5.3-Flash, MiMo-V2.6-Pro |
| Pętle intensywnie używające narzędzi | GLM-5.3-Flash u hosta ze zmierzoną dokładnością narzędzi (Fireworks, Together, Parasail) | DeepSeek V4.1-Flash u dostawcy własnego |
| Czytanie długiego kontekstu (do 1M) | DeepSeek V4.1-Flash (kontekst 1M, wyjście 384K) | darmowy plan Gemini 3.8 Flash do okazjonalnych zadań |
| Ewaluacja i eksperymenty za darmo | NVIDIA build.nvidia.com, Kilo Gateway, Requesty | próbne tokeny Alibaba |
| Trudne kroki bez płacenia cen Opusa | MiMo-V2.6-Pro (AA 46) | GLM-5.3 przez kredyty Ollama Cloud |
| Wszystko z danymi klientów | tylko lokalny zestaw | — |

## Co się nie zmieściło

- **Poniżej poprzeczki, ale za darmo:** darmowe modele OpenRouter (Inkling, Nemotron 3 Ultra, Gemma 4, gpt-oss-120b),
  darmowy Cloudflare Workers AI (tylko gpt-oss-120b), darmowa SambaNova (20 żądań/dzień; MiniMax-M3 z AA 29 jest
  płatny), LLM7 (100K tokenów/dzień).
- **Zniknęły w 2026:** GitHub Models (wycofany 30.07), serverless Hyperbolic (24.09), darmowy OAuth Qwen Code (15.04),
  darmowe kredyty Hugging Face (7.10), godzinowe darmowe kredyty Pollinations (10.07), plany Cerebras Code (wyprzedane).
- **Powyżej poprzeczki, ale nie tanie:** Kimi K3 (AA 44, wyjście od 9,50 USD), Qwen3.8-Max, Grok 4.7, duże modele GPT.
- **Tanie modele zamknięte:** Claude Haiku 5.5 (AA 34 przy domyślnym wysiłku, 43 przy max), GPT-6 Luna (AA 38 przy max) i Muse Spark 1.3 Contributor (AA 45 przy najwyższym dozwolonym wysiłku,
  trenuje na promptach) opisuję w [02-MODELE.md](02-MODELE.md). Należą do komercyjnej nogi mojego stosu.
- **Dobre hosty tuż za pierwszą dwudziestką:** Novita, SiliconFlow, Nebius Token Factory (słaby wynik w zadaniach z
  narzędziami na GLM-5.3-Flash), Baseten, GMI Cloud, Chutes, router Hugging Face, Mistral (API tylko dla klientów
  biznesowych od sierpnia 2026).

## Pliki

| Plik | Zawartość |
|---|---|
| [01-PROFILE.md](01-PROFILE.md) | 20 tras: dostęp, limity, ceny, modele, przydatność dla agentów, niezawodność, haczyki, fragment do weryfikacji |
| [02-MODELE.md](02-MODELE.md) | które modele naprawdę osiągają poziom DeepSeek-V4-Flash, benchmarki, wybory według roli |
| [03-UZYCIE-W-AGENTACH.md](03-UZYCIE-W-AGENTACH.md) | jak łączyć modele lokalne, darmowe, tanie i komercyjne: konfiguracja routera, rachunek kosztów, pułapki, test akceptacyjny |
| [ZRODLA.md](ZRODLA.md) | wszystkie źródła wraz z tym, co z każdego wziąłem |

## Powiązane części tego repozytorium

- [../harnessy-agentowe/README.md](../harnessy-agentowe/README.md) — w jakim harnessie uruchamiać te modele.
- [../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md](../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md) — budowa routera.
- [../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md) — lokalnie plus chmura.

Wersja angielska: [../../en/cheap-free-models/README.md](../../en/cheap-free-models/README.md).
