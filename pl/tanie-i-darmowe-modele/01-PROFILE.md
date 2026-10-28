# Profile: 20 najlepszych tanich i darmowych ścieżek online

Dwadzieścia ścieżek dostępu, uszeregowanych według wyniku (zob. [README.md](README.md#jak-oceniałem)). Każdy wpis ma te
same sekcje, więc można je porównywać obok siebie. Fakty i ceny według stanu na **13.10.2026**; „AA” to Artificial
Analysis Intelligence Index v4.3.2, w którym mój lokalny DeepSeek-V4-Flash-0731 ma **34** (poprzeczka). Tło modeli jest
w [02-MODELE.md](02-MODELE.md), a łączenie ścieżek w agencie w [03-UZYCIE-W-AGENTACH.md](03-UZYCIE-W-AGENTACH.md).

---

## 1. OpenRouter

**Typ:** pay-as-you-go (darmowy poziom istnieje, modele poniżej progu) · **Najlepsze modele:** `xiaomi/mimo-v2.6-pro` AA 46, `z-ai/glm-5.3` AA 45, `z-ai/glm-5.3-flash` AA 42, `deepseek/deepseek-v4.1-flash` AA 39 · **Wynik: 93** (Q30 C17 L14 A19 R13) · **Dane:** trenowanie na promptach: zależy od hosta, na który trafisz (darmowe endpointy: przeważnie „może trenować”); sam OpenRouter nie przechowuje promptów, chyba że wyrazisz zgodę; hosting tam, gdzie działa wybrany dostawca, routing w regionie UE tylko w planach Business/Enterprise

> Jeden klucz, jeden URL zgodny z OpenAI i ponad 30 hostów na każdy mocny otwarty model: najtańszy i najbardziej elastyczny sposób dotarcia do MiMo-V2.6-Pro, GLM-5.3(-Flash) i V4.1-Flash, z wbudowanymi fallbackami i routingiem świadomym wywołań narzędzi.

**Co dostajesz.**
- Kredyty pay-as-you-go. Ceny tokenów to ceny samych dostawców przekazane bez zmian; OpenRouter dolicza **5,5% opłaty od zakupu kredytów** (plan Standard, 13.10.2026).
- **Mocne modele nie są darmowe.** 13.10.2026 żaden z modeli DeepSeek, GLM, Kimi, Qwen, MiniMax ani MiMo nie ma wariantu `:free`. Najlepsze darmowe modele (Inkling Small AA 26, Inkling AA 25, Nemotron 3 Ultra AA 23) są poniżej mojego progu AA 34 (mój lokalny DeepSeek-V4-Flash-0731).
- Płatne trasy są niemal darmowe: GLM-5.3-Flash od 0,045 / 0,15 USD, V4.1-Flash od 0,09 / 0,18 USD, MiMo-V2.6-Pro za 0,43 / 0,87 USD za 1M tokenów (wejście / wyjście), 13.10.2026.
- **Jednorazowy zakup za 10 USD** na stałe podnosi limit darmowych modeli z 50 do 1000 żądań dziennie.

**Modele.** Najtańsze aktywne endpointy, 13.10.2026, ceny w USD za 1M (wejście / wyjście).

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `xiaomi/mimo-v2.6-pro` | 46 | 1M | 943k (DeepInfra) | sprawdź `/endpoints` | DeepInfra fp8 0,43 / 0,87, cache 0,004, dostępność 1-dniowa 100%; Xiaomi fp8 0,435 / 0,87, dostępność 95,9%; tylko 4 hosty, wolny (~42–47 t/s) |
| `z-ai/glm-5.3` | 45 | 1M | 128k (Z.ai) | tak | Baidu fp8 0,599 / 1,883; Inceptron fp4 0,60 / 1,883; SiliconFlow i Novita fp8 0,70 / 2,20; Z.ai 1,40 / 4,40 przekracza budżet; reasoning zawsze włączony |
| `z-ai/glm-5.3-flash` | 42 | 1M | 128k (StreamLake) | tak, wywołania równoległe | 32 dostawców; StreamLake fp8 0,045 / 0,15, dostępność 99,6%; DeepInfra fp4 0,075 / 0,25; Z.ai 0,15 / 0,50; `:batch` 0,06 / 0,20 |
| `deepseek/deepseek-v4.1-flash` | 39 | 1M | 131k (DeepInfra) | tak | 32 dostawców; Decart fp4 0,09 / 0,18; DeepInfra fp8 0,14 / 0,42; DeepSeek 0,15 / 0,60, dostępność 100%; `:batch` 0,112 / 0,336 |
| `deepseek/deepseek-v4-flash-0731` | 34 | 1M | 384k (DeepInfra) | tak | mój lokalny model w chmurze: DeepInfra fp8 0,06 / 0,18, dostępność 100%; przydatny do testów A/B względem mojego sprzętu |

Źródła są sprzeczne co do GLM-5.3: aktualny odczyt endpointów pokazuje 42 dostawców, a notatka badawcza z pierwszej ręki mówi, że OpenRouter wymienia tylko Z.ai. Sprawdź `/endpoints`, zanim zaczniesz polegać na tanim hoście GLM-5.3.

**Limity i ceny.**
- Darmowe modele: zawsze **20 RPM**; **50 żądań dziennie**, dopóki łączne zakupy kredytów są poniżej 10 USD; **1000 żądań dziennie** po przekroczeniu 10 USD (jednorazowy próg, nie subskrypcja). Ujemne saldo zwraca 402 nawet na darmowych modelach. Nieudane darmowe żądania mogą wliczać się do dziennego limitu *(pomiar zewnętrzny)*.
- Płatne modele: cena dostawcy + 5,5% opłaty od zakupu (plan Business 8%). BYOK: pierwsze 25 000 USD miesięcznie inferencji według cennika jest bez opłaty, potem 5%.
- Warianty `:batch` są tańsze (patrz tabela); `:floor` wybiera najtańszy endpoint, `:nitro` najszybszy.
- Zgoda na logowanie „use of inputs” daje 1% zniżki; ja bym tego nie robił.

**Jak uzyskać dostęp.**
1. Zarejestruj się na openrouter.ai przez e-mail lub OAuth. Nie odnotowano blokady regionalnej dla Polski/UE.
2. Karta jest potrzebna tylko do zakupu kredytów. Kup raz za 10 USD: to odblokowuje 1000 darmowych żądań dziennie i finansuje miesiące niemal darmowych płatnych wywołań.
3. W ustawieniach prywatności konta zdecyduj osobno o przełącznikach „may train” dla płatnych i darmowych endpointów. Wyłączenie darmowych endpointów, które mogą trenować, czyni około 9 darmowych modeli niedostępnymi (404 „No endpoints found matching your data policy”).
4. Utwórz klucz API i wyeksportuj go jako `OPENROUTER_API_KEY`. `GET /api/v1/key` pokazuje twoje limity i status darmowego poziomu.

**Przydatność dla agentów.**
- Bazowy URL zgodny z OpenAI: `https://openrouter.ai/api/v1`. Istnieje endpoint zgodny z Anthropic `/api/v1/messages` (sonda zwróciła 401 w formacie Anthropic), więc `ANTHROPIC_BASE_URL=https://openrouter.ai/api` działa z harnessami opartymi na Anthropic SDK.
- **Routing dostawców to kluczowa funkcja:** `provider.order`, `only`, `ignore`, `allow_fallbacks` (domyślnie true), `require_parameters`, `quantizations` (np. `["fp8","bf16"]`), `sort`, `max_price`, `preferred_min_throughput`, `preferred_max_latency`, `zdr`, `data_collection`; lista fallbacków `models: [...]` na najwyższym poziomie.
- **Auto Exacto** (od 12.03.2026, aktualizacja 24.06.2026) jest domyślnie włączone dla każdego żądania z `tools`: mniej więcej co 5 min ponownie szereguje dostawców według przepustowości, telemetrii wywołań narzędzi i wewnętrznych benchmarków. Zgłaszane spadki błędów narzędzi: GLM-5 −88% (z 8% do ~1%), gpt-oss-120b −36%, DeepSeek V3.2 −16% *(deklaracja dostawcy)*. `:exacto` (paź 2025) = wyselekcjonowani dostawcy do wywołań narzędzi, +10–20% na Tau2Bench/LiveMCPBench *(deklaracja dostawcy)*.
- Ustaw **`require_parameters: true`**, aby wywołanie narzędzia nigdy nie trafiło na hosta, który ignoruje `tools` lub `response_format` (endpointy V4-Flash w BaseTen nie mają structured outputs, Relace nie ma narzędzi).
- Przypnij kwantyzację: wiele najtańszych endpointów to mikrodostawcy fp4/int4 bez żadnych dowodów dokładności. Cena nie przewiduje dokładności *(pomiar zewnętrzny, AA Endpoint Accuracy Index)*.
- Błędy 429 na darmowych modelach pochodzą głównie od hosta upstream, najgorzej wieczorami czasu US i w weekendy (zgłoszenia społeczności 2026).

**Niezawodność.**
- Strona statusu: status.openrouter.ai (strona JS). Dostępność 1-dniowa per endpoint jest udostępniana w API `/endpoints`.
- Najtańsze hosty są często najbardziej zawodne: Baidu V4-Flash 94,0%, Chutes GLM-5.1 57,5%, GMICloud MiMo-Flash 42,9% (13.10.2026).
- **Rotacja darmowych modeli jest duża:** `z-ai/glm-5.2:free` usunięty 7.09.2026, `deepseek/deepseek-v4-flash-0731:free` usunięty 21.09.2026; liczba darmowych spadła z 24 (21.09) do 16 (13.10); mediana życia darmowego modelu na liście ~75 dni *(pomiar zewnętrzny)*.
- Aliasy takie jak `~deepseek/deepseek-flash-latest` i `~z-ai/glm-flash-latest` po cichu przechodzą na nowsze wersje; przypinaj ID z datą.

**Ograniczenia.**
- Nic na poziomie AA 34 lub wyżej nie jest darmowe; darmowy poziom to w najlepszym razie fallback dla modeli AA 23–26.
- 50 żądań dziennie bez doładowania za 10 USD jest bezużyteczne dla pętli agentowych.
- Przy domyślnym routingu możesz trafić na endpoint fp4, którego nigdy nie oceniałeś; musisz sam ustawić `quantizations` / `only`.
- Przetwarzanie w regionie UE wymaga planu Business/Enterprise.
- Opłata 5,5% sprawia, że jest nieco drożej niż bezpośrednio u tego samego hosta.

**Gdzie pasuje w moim stosie.**
- **Domyślna bramka dla taniej ścieżki:** jeden klucz do GLM-5.3-Flash (masowe pętle narzędzi), V4.1-Flash (ta sama rodzina co mój sprzęt, mocniejszy) i MiMo-V2.6-Pro (najtrudniejsze podzadania), z listą fallbacków `models`.
- Planner zostaje na Claude Opus; modele OpenRouter to sub-agenci i robotnicy do pracy masowej (zob. `../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md`).
- Runner ewaluacji: ten sam prompt na różnych hostach i kwantyzacjach w jednym skrypcie (`../kurs_aplikacje_agentowe/14-EWALUACJA.md`).
- Dane klientów zostają na moim sprzęcie; bezpośredniego hosta (DeepInfra, Fireworks) wybieram tylko wtedy, gdy chcę jeden stały endpoint bez opłaty.

**Sprawdź sam.**

```bash
# dzisiejsze darmowe modele (spodziewaj się tylko modeli poniżej progu)
curl -s https://openrouter.ai/api/v1/models | jq -r '.data[]|select(.id|endswith(":free")).id'
# cena, kwantyzacja i dostępność per host dla jednego modelu
curl -s https://openrouter.ai/api/v1/models/deepseek/deepseek-v4.1-flash/endpoints \
  | jq '.data.endpoints[]|{provider_name,quantization,pricing,uptime_last_1d}'
# wywołanie narzędzia na GLM-5.3-Flash, tylko fp8+, hosty respektujące każdy parametr
curl -s https://openrouter.ai/api/v1/chat/completions -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H 'Content-Type: application/json' -d '{
  "model":"z-ai/glm-5.3-flash",
  "messages":[{"role":"user","content":"Pogoda w Warszawie?"}],
  "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}],
  "provider":{"require_parameters":true,"quantizations":["fp8","bf16"]}}'
# twoje limity i status darmowego poziomu
curl -s https://openrouter.ai/api/v1/key -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

**Źródła:** [OpenRouter models API](https://openrouter.ai/api/v1/models) · [OpenRouter endpoints API](https://openrouter.ai/api/v1/models/deepseek/deepseek-v4.1-flash/endpoints) · [OpenRouter limits](https://openrouter.ai/docs/api/reference/limits) · [OpenRouter pricing](https://openrouter.ai/pricing) · [OpenRouter BYOK](https://openrouter.ai/docs/guides/overview/auth/byok) · [OpenRouter provider logging](https://openrouter.ai/docs/guides/privacy/provider-logging) · [OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection) · [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection) · [Auto Exacto](https://openrouter.ai/blog/announcements/auto-exacto/) · [Exacto](https://openrouter.ai/blog/announcements/provider-variance-introducing-exacto/) · [TrueFoundry o darmowych modelach OR](https://www.truefoundry.com/blog/openrouter-free-models-whats-actually-free-and-what-it-costs-you) · [Tracker darmowych modeli OR](https://github.com/cyclez2000/openrouter-free-models/issues/82) · [AA Endpoint Accuracy Index](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) · [Ranking AA](https://artificialanalysis.ai/leaderboards/models) · [Cennik Z.ai](https://docs.z.ai/guides/overview/pricing)

---

## 2. DeepInfra

**Typ:** pay-as-you-go · **Najlepsze modele:** `xiaomi/mimo-v2.6-pro` AA 46 (wg danych OpenRouter), `zai-org/GLM-5.3-Flash` AA 42, `deepseek-ai/DeepSeek-V4.1-Flash` AA 39, `deepseek-ai/DeepSeek-V4-Flash-0731` AA 34 · **Wynik: 90** (Q30 C19 L14 A15 R12) · **Dane:** trenuje na promptach: nie; wejście nie jest zapisywane na dysku, logowane są tylko metadane *(deklaracja dostawcy)*; hosting w USA (lokalizacja nie jest podana w dokumencie o prywatności)

> Dno cenowe amerykańskich hostów modeli open-weight: mój własny lokalny model V4-Flash-0731 za USD 0,06 / 0,18 i V4.1-Flash za USD 0,20 / 0,60, z endpointami zgodnymi z OpenAI i Anthropic i bez trenowania na promptach.

**Co dostajesz.**
- Zwykła bezserwerowa inferencja pay-as-you-go, rozliczana za token; do realnego użycia potrzebna karta lub przedpłata.
- **Najtańszy mocny DeepSeek, jaki znalazłem** (13.10.2026): V4-Flash-0731 USD 0,06 / 0,18 za 1M (wejście / wyjście), cache 0,015; V4.1-Flash USD 0,20 / 0,60, cache 0,006.
- GLM-5.3-Flash w cenie referencyjnej USD 0,15 / 0,50 (cache 0,03), ale **w FP4**.
- Darmowy kredyt: strony zewnętrzne podają „USD 5 za darmo, 90 dni”; brak tego w oficjalnej dokumentacji, traktuj jako niezweryfikowane.

**Modele.** Ceny bezpośredniego API, USD za 1M (wejście / wyjście), 13.10.2026.

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `xiaomi/mimo-v2.6-pro` | 46 | 1M | 943k | sprawdź endpoint | Widoczny jako DeepInfra fp8 na OpenRouter za 0,43 / 0,87, cache 0,004, uptime 100%; ceny bezpośredniej nie było na stronie cennika, którą czytałem; wolny model (~42–47 t/s) |
| `zai-org/GLM-5.3-Flash` | 42 | 1M | nieznane | tak + structured | 0,15 / 0,50, cache 0,03; FP4; 95,5% skuteczności w zadaniach z narzędziami *(pomiar zewnętrzny)*; promocja na OR 0,075 / 0,25 |
| `deepseek-ai/DeepSeek-V4.1-Flash` | 39 | 1M | 131k (OR) | tak + structured | 0,20 / 0,60, cache 0,006; FP8; OR pokazuje 0,14 / 0,42 z promocją −30% |
| `deepseek-ai/DeepSeek-V4-Flash-0731` | 34 | 1M | 384k | tak + structured | 0,06 / 0,18, cache 0,015; FP8; ten sam checkpoint co na moim sprzęcie |
| `zai-org/GLM-5.3` | 45 | 1M | nieznane | tak | 0,90 / 4,00 bezpośrednio (wyjście powyżej mojego limitu USD 3); promocja na OR 0,5625 / 2,50 fp4; dokładność endpointu 96 *(pomiar zewnętrzny)* |
| `deepseek-ai/DeepSeek-V4-Pro-0813` | 36 | 1M | **16k** | tak | 1,30 / 2,60, cache 0,10; FP8; 16k wyjścia zabija długie rozumowanie |

Poniżej progu, ale tanie tutaj: MiniMax-M3 (AA 29) 0,28 / 1,10 FP8, Kimi K2.6 (AA 27) 0,75 / 3,50 FP4 z maks. wyjściem 16k, gpt-oss-120b (AA 12) 0,037 / 0,17 BF16.

**Limity i ceny.**
- **200 równoległych żądań na model** (ok. 1200 RPM przy 10 s na żądanie); podniesienie przez panel. Brak opublikowanego limitu TPM.
- Brak darmowego planu; ceny cache promptów jak w tabeli.
- Przez Requesty poziom DeepInfra `:flex` pokazuje V4.1-Flash za USD 0,16 / 0,48 i V4-Flash-0731 za USD 0,072 / 0,144 (13.10.2026, przed 5% marżą Requesty).
- Przez Hugging Face Inference Providers te same modele są routowane bez marży (`deepseek-ai/DeepSeek-V4.1-Flash:deepinfra`), ale darmowego kredytu HF już nie ma.

**Jak uzyskać dostęp.**
1. Zarejestruj się na deepinfra.com przez e-mail lub GitHub. Dostępne w Polsce.
2. Dodaj kartę lub zrób przedpłatę; darmowy kredyt nie jest oficjalnie udokumentowany.
3. Utwórz token API w panelu i wyeksportuj go jako `DEEPINFRA_TOKEN`.
4. Lista modeli jest publiczna: `GET https://api.deepinfra.com/v1/openai/models` (bez klucza).

**Przydatność dla agentów.**
- Bazowy URL zgodny z OpenAI `https://api.deepinfra.com/v1/openai`; zgodny z Anthropic `ANTHROPIC_BASE_URL=https://api.deepinfra.com/anthropic` dla harnessów w stylu Claude Code.
- Narzędzia, `tool_choice` i structured outputs w modelach DeepSeek, GLM, Kimi, MiniMax i Qwen powyżej (wg metadanych endpointów OpenRouter); przełącznik rozumowania, cache promptów, streaming.
- **Dokładność zależy od modelu, więc sprawdzaj każdy osobno** *(pomiary zewnętrzne)*: V4-Pro 97 i GLM-5.3 96 w AA Endpoint Accuracy Index (wiernie); GLM-5.3-Flash 95,5% skuteczności zadań przy 4% błędów (openbenchmarks, vs Fireworks 99,5%); **GLM-5.2 FP4 tylko 73** (źle); gpt-oss-120b domyślnie 85 vs `-Turbo` 98. Kimi K2-0905 uzyskał 100% dokładności schematu w K2VV od Moonshot (listopad 2025).
- **Wolno:** AA zmierzyło V4-Flash-0731 na 42 t/s i Kimi K2.6 na 22 t/s (najwolniejszy poziom). Dobre do równoległej pracy masowej, bolesne w sekwencyjnej pętli agenta.
- Uważaj na niskie limity `max_tokens` (V4-Pro 16k, V4-Flash 0423 65k): model rozumujący może je wyczerpać, zanim odpowie.

**Niezawodność.**
- Strona statusu: status.deepinfra.com.
- 1-dniowy uptime na OpenRouter (13.10.2026): większość endpointów DeepInfra na poziomie 99,4% lub lepiej, ale Kimi K2.6 91,98%, a GLM-5.3-Flash w chwili pobrania pokazywał 0%.
- Katalog zmienia się z rynkiem: oryginalny V4-Flash 0423 nadal jest na liście (0,09 / 0,18, 65k wyjścia), choć hosty generalnie go wycofują; do przypięcia są ID 0731 i V4.1.

**Ograniczenia.**
- Najwolniejszy poziom wśród tanich hostów; zły dla jednowątkowych agentów wrażliwych na opóźnienia.
- **FP4 we wszystkich modelach GLM**; GLM-5.2 FP4 stracił jedną czwartą dokładności, GLM-5.3-Flash FP4 jest przyzwoity, ale nie najlepszy.
- Małe maks. wyjście w V4-Pro (16k) i Kimi K2.6 (16k).
- Tylko USA; brak opcji przetwarzania w UE.
- Darmowy kredyt niezweryfikowany; licz się z płaceniem od pierwszego wywołania.

**Gdzie pasuje w moim stosie.**
- **Masowy worker dla DeepSeek:** V4-Flash-0731 za USD 0,18 za wyjście to ten sam model co na moim sprzęcie, więc mogę tu przerzucać nadmiarowe zadania z identycznymi promptami, gdy moje 4 lokalne sloty są zajęte.
- V4.1-Flash za USD 0,60 za wyjście jako sub-agent „ta sama rodzina, mocniejszy” do zadań niewrażliwych.
- Równoległe przebiegi ewaluacji i ekstrakcja wsadowa, gdzie 200 równoległych żądań liczy się bardziej niż tokeny na sekundę.
- Do pętli GLM-5.3-Flash intensywnie używających narzędzi wolałbym Fireworks lub Parasail (lepiej zmierzona dokładność narzędzi); dla jednego klucza do wielu hostów — OpenRouter.

**Sprawdź sam.**

```bash
# publiczna lista modeli z cenami i kontekstem (bez klucza)
curl -s https://api.deepinfra.com/v1/openai/models
# wywołanie narzędzia na V4.1-Flash
curl -s https://api.deepinfra.com/v1/openai/chat/completions -H "Authorization: Bearer $DEEPINFRA_TOKEN" \
  -H 'Content-Type: application/json' -d '{"model":"deepseek-ai/DeepSeek-V4.1-Flash",
  "messages":[{"role":"user","content":"Pogoda w Krakowie?"}],
  "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
# endpointy DeepInfra na OpenRouter: kwantyzacja, maks. wyjście, uptime
curl -s https://openrouter.ai/api/v1/models/xiaomi/mimo-v2.6-pro/endpoints \
  | jq '.data.endpoints[]|select(.provider_name=="DeepInfra")'
```

**Źródła:** [DeepInfra pricing](https://deepinfra.com/pricing) · [DeepInfra models API](https://api.deepinfra.com/v1/openai/models) · [DeepInfra rate limits](https://docs.deepinfra.com/account/rate-limits) · [DeepInfra data privacy](https://docs.deepinfra.com/account/data-privacy) · [DeepInfra Anthropic integration](https://docs.deepinfra.com/integrations/anthropic) · [OpenRouter endpoints API](https://openrouter.ai/api/v1/models/xiaomi/mimo-v2.6-pro/endpoints) · [AA Endpoint Accuracy Index](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) · [AA GLM-5.2 providers](https://artificialanalysis.ai/models/glm-5-2/providers) · [AA GLM-5.3 providers](https://artificialanalysis.ai/models/glm-5-3/providers) · [AA gpt-oss-120b providers](https://artificialanalysis.ai/models/gpt-oss-120b/providers) · [openbenchmarks same-model accuracy](https://openbenchmarks.com/inference/same-model-different-accuracy) · [K2 Vendor Verifier](https://github.com/MoonshotAI/K2-Vendor-Verifier) · [Requesty models API](https://router.requesty.ai/v1/models) · [AA MiMo-V2.6-Pro](https://artificialanalysis.ai/models/mimo-v2-6-pro)

---

## 3. Fireworks AI

**Typ:** pay-as-you-go (jednorazowy kredyt USD 1) · **Najlepsze modele:** GLM 5.3 Flash AA 42, DeepSeek V4.1 Flash AA 39 · **Wynik: 89** (Q26 C17 L15 A19 R12) · **Dane:** trenuje na promptach: nie (domyślnie nic nie jest przechowywane); inferencja modeli otwartych nie jest trwale zapisywana (domyślnie ZDR) *(deklaracja dostawcy)*, wyjątki dla Responses API i batcha; routing „global”, przetwarzanie wyłącznie w USA na `us.api.fireworks.ai` za +50%

> Najdokładniejszy tani host do wywołań narzędzi, jaki znalazłem (99,5% na GLM-5.3-Flash), szybki, z ogromnymi limitami i z endpointami zgodnymi zarówno z OpenAI, jak i z Anthropic.

**Co dostajesz.**
- Serverless w modelu pay-as-you-go; około USD 1 darmowego kredytu przy rejestracji *(źródło wtórne)*.
- **GLM 5.3 Flash za USD 0,15 / 0,50 za 1M tokenów (wejście / wyjście), cache 0,03**, z najlepszą zmierzoną skutecznością zadań z narzędziami spośród wszystkich hostów.
- DeepSeek V4.1 Flash za USD 0,30 / 1,20, cache 0,006 (podniesione 1.10.2026 z 0,22 / 0,66).
- Batch API za 50% cen serverless.

**Modele.** Standardowe ceny serverless, USD za 1M (wejście / wyjście), październik 2026.

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| GLM 5.3 Flash | 42 | 1M (natywnie) | nieznane | tak | 0,15 / 0,50, cache 0,03; 99,5% skuteczności zadań z narzędziami, najlepszy z 10 hostów *(pomiar zewnętrzny)* |
| DeepSeek V4.1 Flash | 39 | 1M (natywnie) | nieznane | niezweryfikowane | 0,30 / 1,20, cache 0,006; cena podniesiona 1.10.2026 |
| GLM 5.3 | 45 | 1M (natywnie) | nieznane | niezweryfikowane | 1,40 / 4,40, cache 0,26: wyjście powyżej mojego limitu USD 3; wariant „Fast” 2,10 / 6,60 |
| Kimi K3 | 44 | 1M (natywnie) | nieznane | tak | 3 / 15, daleko ponad budżet; dokładność endpointu 97 *(pomiar zewnętrzny)* |

Poniżej poprzeczki tutaj: MiniMax M3 (AA 29) 0,30 / 1,20, GPT OSS 120B (AA 12) 0,15 / 0,60. Fireworks nie ujawnia kwantyzacji (OpenRouter pokazuje „unknown”).

**Limity i ceny.**
- Około **10 RPM, dopóki nie dodasz metody płatności** *(źródło wtórne)*.
- Od 1.09.2026 adaptacyjne TPM według klasy rozmiaru modelu. Klasa „Small” = modele poniżej 600B parametrów (GLM 5.3 Flash z 320B i V4.1 Flash z 552B się kwalifikują): **108M TPM promptu, 27M TPM bez cache, 1,08M TPM generowanych** (2.10.2026), **podwojone 7.10.2026**. To daleko ponad to, czego potrzebują moje agenty.
- Modyfikatory cen: warianty „(US)” +50%, Priority +25%, Batch −50%.
- **Fire Pass** (plan ryczałtowy, Kimi K3 Fast przez `kimi-fast-latest`, tylko do użytku osobistego/w harnessach do kodowania) jest „not currently open to new subscriptions” (dokumentacja, październik 2026).

**Jak uzyskać dostęp.**
1. Zarejestruj się na fireworks.ai. Dostępne w Polsce.
2. Wykorzystaj ~USD 1 kredytu na smoke test; dodaj kartę, aby znieść pułap ~10 RPM.
3. Utwórz klucz API w panelu i wyeksportuj go jako `FIREWORKS_API_KEY`.
4. Jeśli potrzebujesz przetwarzania wyłącznie w USA, użyj `us.api.fireworks.ai` i wariantów modeli „(US)” (+50%).

**Przydatność dla agentów.**
- Bazowy URL zgodny z OpenAI `https://api.fireworks.ai/inference/v1`; zgodny z Anthropic `https://api.fireworks.ai/inference` (`ANTHROPIC_BASE_URL`).
- **Najlepsza zmierzona wierność wywołań narzędzi** *(pomiary zewnętrzne)*: openbenchmarks GLM-5.3-Flash 99,5% na 600 ustrukturyzowanych zadaniach z narzędziami (3.09.2026; Nebius 84,8% w tym samym teście); AA Endpoint Accuracy GLM-5.2 100, Kimi K3 97; K2 Vendor Verifier od Moonshot 100% dokładności schematu na K2-Thinking i K2-0905. Moonshot wymienia Fireworks jako wiernego dostawcę.
- Słaby punkt w tych samych danych AA: gpt-oss-120b uzyskał 86 (sierpień 2026), ale ten model i tak jest poniżej mojej poprzeczki.
- Pułapy limitów sprawiają, że błędy 429 są mało prawdopodobne po podpięciu karty; bez karty ograniczeniem jest 10 RPM.
- Responses API domyślnie ma `store=true` (przechowywane 30 dni): przekaż `store=false`, jeśli używasz go do czegokolwiek, czego nie zapisałbyś w logach.

**Niezawodność.**
- Strona statusu: status.fireworks.ai. Dostępność 1-dniowa w OpenRouter 99,2–100% (13.10.2026).
- **Rotacja katalogu jest realna:** 26.09.2026 Fireworks usunął z publicznego serverless DeepSeek V4 Pro 0813, V4 Flash 0731, Kimi K2.6, K2.7 Code i GLM 5.2; 27.08 wycofał MiniMax M2.7, V4 Pro i K2.6 Turbo. Nie został tu żaden Kimi z wyjściem poniżej USD 3.
- Ceny też się zmieniają: wyjście V4.1 Flash wzrosło z 0,66 do 1,20 1.10.2026.
- Fire Pass od marca 2026 dwukrotnie zmienił cenę i model, a teraz jest zamknięty.

**Ograniczenia.**
- Tylko dwa modele w moim budżecie i powyżej poprzeczki (GLM 5.3 Flash, V4.1 Flash); brak MiMo, a V4-Flash-0731 (model z mojego rigu) został usunięty.
- V4.1 Flash kosztuje dwa razy więcej za wyjście niż w DeepInfra (1,20 vs 0,60).
- Kwantyzacja nieujawniona: ufasz pomiarom, nie specyfikacji.
- Brak przetwarzania w UE; domyślnie routing „global”.
- Kredyt USD 1 i wartość 10 RPM pochodzą ze źródeł wtórnych.

**Gdzie pasuje w moim stosie.**
- **Główny host dla pętli narzędziowych na GLM-5.3-Flash:** subagenty wywołujące wiele narzędzi, gdzie 4% błędów (DeepInfra, Novita) kosztowałoby więcej w ponowieniach niż różnica w cenie.
- Subagent do kodowania za harnessem opartym na Anthropic SDK, przez endpoint zgodny z Anthropic.
- Ewaluacje wsadowe i ekstrakcja za pół ceny przez Batch API.
- Do wolumenu DeepSeek użyłbym raczej DeepInfra lub Parasail; dla jednego klucza z fallbackami OpenRouter z Fireworks przypiętym w `provider.order`.

**Sprawdź sam.**

```bash
# lista modeli (znajdź dokładne ID GLM / DeepSeek)
curl -s https://api.fireworks.ai/inference/v1/models -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  | jq -r '.data[].id' | grep -iE 'glm|deepseek'
export FW_MODEL="<id z powyższej listy>"
# wywołanie narzędzia
curl -s https://api.fireworks.ai/inference/v1/chat/completions -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -H 'Content-Type: application/json' -d "{\"model\":\"$FW_MODEL\",
  \"messages\":[{\"role\":\"user\",\"content\":\"Pogoda w Gdańsku?\"}],
  \"tools\":[{\"type\":\"function\",\"function\":{\"name\":\"get_weather\",\"parameters\":{\"type\":\"object\",\"properties\":{\"city\":{\"type\":\"string\"}},\"required\":[\"city\"]}}}]}"
# endpointy Fireworks w OpenRouter: cena i dostępność
curl -s https://openrouter.ai/api/v1/models/z-ai/glm-5.3-flash/endpoints \
  | jq '.data.endpoints[]|select(.provider_name|test("Fireworks"))'
```

**Źródła:** [Cennik Fireworks](https://fireworks.ai/pricing) · [Cennik serverless Fireworks](https://docs.fireworks.ai/serverless/pricing) · [Changelog Fireworks](https://docs.fireworks.ai/updates/changelog) · [Dokumentacja Fire Pass](https://docs.fireworks.ai/firepass) · [Rezydencja danych Fireworks](https://docs.fireworks.ai/accounts/data-residency) · [Opis ZDR w Fireworks](https://abubakarsiddik.site/blog/fireworks-ai-zero-data-retention) · [Limity Fireworks bez karty](https://yangmao.ai/en/providers/fireworks/no-credit-card/) · [openbenchmarks: dokładność tego samego modelu](https://openbenchmarks.com/inference/same-model-different-accuracy) · [AA: dostawcy GLM-5.2](https://artificialanalysis.ai/models/glm-5-2/providers) · [AA: dostawcy Kimi K3](https://artificialanalysis.ai/models/kimi-k3/providers) · [K2 Vendor Verifier](https://github.com/MoonshotAI/K2-Vendor-Verifier) · [Kimi Vendor Verifier](https://github.com/MoonshotAI/Kimi-Vendor-Verifier) · [API endpointów OpenRouter](https://openrouter.ai/api/v1/models/z-ai/glm-5.3-flash/endpoints) · [AA GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash)

---

## 4. Z.ai (GLM) API

**Typ:** pay-as-you-go (plus darmowy poziom z małymi modelami i ryczałtowy plan do kodowania) · **Najlepsze modele:** `glm-5.3-flash` (AA 42), `glm-5.3` (AA 45, powyżej przedziału cenowego) ·
**Wynik: 87** (Q26 C18 L12 A18 R13) · **Dane:** trenowanie na promptach: nie dla API (tylko opt-in, zgodnie z DPA); podmiot w Singapurze, lokalizacja serwerów nie jest podana

> Własne API producenta modeli GLM: GLM-5.3-Flash za 0,50 USD za output to najlepszy model agentowy w przeliczeniu na dolara w tym przeglądzie, prosto od twórcy.

**Co dostajesz.** Zwykłe API pay-as-you-go z endpointami zgodnymi z OpenAI, Responses i Anthropic. Najważniejsze:
**GLM-5.3-Flash za 0,15 / 0,50 USD za 1M tokenów (input / output), input z cache 0,03** (13.10.2026). Duży GLM-5.3
kosztuje tu 1,40 / 4,40 USD, czyli powyżej mojego progu 3 USD za output. Darmowy poziom istnieje, ale tylko dla małych modeli,
które są poniżej poprzeczki.

**Modele.**

| Model | AA | Kontekst | Maks. output | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `glm-5.3-flash` | 42 | 1M | 128K na hostach OpenRoutera | tak | MoE 320B / 18B, MIT, vision, wydany 26.08.2026. Vals TB4.0 37,4 wobec poprzeczki 18,7 |
| `glm-5.3` | 45 (max) · 34 (low) | 1M | 128K | tak | 753B / 40B, wydany 18.08.2026. Tu 4,40 USD za output: korzystaj z hostów zewnętrznych |
| `glm-4.7-flash` (darmowy) | poniżej poprzeczki | 200K | nie podano | tak | 30B-A3B. Tylko do trywialnych podzadań |

**Limity i ceny.**
- PAYG (strona cennika Z.ai, bez daty strony, odczyt 13.10.2026), USD za 1M input / z cache / output:
  - `glm-5.3-flash` 0,15 / 0,03 / 0,50 · `glm-5.3-flashx` 0,37 / 0,075 / 1,25.
  - `glm-5.3` 1,40 / 0,26 / 4,40 (również GLM-5.2 i 5.1). Przechowywanie inputu w cache jest „limited-time free”.
  - `glm-4.7-flash` i `glm-4.5-flash`: darmowe.
- **GLM-5.3 w rozsądnej cenie jest gdzie indziej** (OpenRouter, 13.10.2026): Baidu fp8 0,599 / 1,883 USD, SiliconFlow i
  Novita fp8 0,70 / 2,20, DeepInfra fp4 0,5625 / 2,50 *(promocja)*. Samo Z.ai również podaje tam 1,40 / 4,40.
- Darmowy GLM-4.7-Flash: **1 równoczesne żądanie, około 1 RPS, około 1000 RPD**, bez karty *(pomiar zewnętrzny)*.
- Nie znalazłem opublikowanych wartości RPM/TPM dla płatnego API (13.10.2026).

**Jak uzyskać dostęp.**
1. Załóż konto na z.ai. Stroną umowy jest JINGSHENG HENGXING TECHNOLOGY PTE. LTD., Singapur; rejestracja działa
   z UE i z Polski.
2. Doładuj saldo w konsoli (szczegółów metod płatności nie było na stronach, które czytałem).
3. Utwórz klucz API i wyeksportuj go jako `ZAI_API_KEY`.
4. Używaj bazowego URL PAYG, **nie** URL planu do kodowania: wywołanie na złym endpoincie kończy się błędem 1113 „Insufficient balance”.

**Przydatność dla agentów.**
- Bazowe URL: zgodny z OpenAI `https://api.z.ai/api/paas/v4`, Responses API `https://api.z.ai/api/v1`,
  zgodny z Anthropic `https://api.z.ai/api/anthropic`.
- Obsługiwane są streaming, function calling, cache kontekstu i ustrukturyzowany output JSON. `parallel_tool_calls` działa
  na OpenRouterze. GLM-5.3-Flash uzyskuje ExtractBench 80,75 *(deklaracja producenta)*.
- **Rozumowanie jest zawsze włączone** w GLM-5.3 (`thinking.type` przyjmuje tylko `enabled`), a listing Z.ai traktuje Flash
  tak samo; tbench.ai uruchamiał jednak Flash z effort „none”, więc to przetestuj. `reasoning_effort` to low / high / max, a
  **max jest domyślne**, więc rachunki za output puchną, jeśli w pętlach narzędziowych nie ustawisz `"reasoning_effort":"low"`.
- Trafność narzędzi: na 600 ustrukturyzowanych zadaniach narzędziowych endpoint GLM-5.3-Flash od Z.ai osiągnął **97,5 %**, wobec 99,5 % dla
  Fireworks i 84,8 % dla Nebius *(pomiar zewnętrzny, 3.09.2026)*. W AA Endpoint Accuracy Index GLM-5.3 od Z.ai
  uzyskuje 98 % wyniku referencyjnego *(pomiar zewnętrzny, 26.09.2026)*.
- Oba modele GLM-5.3 są gadatliwe (Flash 180M, GLM-5.3 210M tokenów w przebiegu AA) i dość wolne: Flash 66,5 tok/s,
  TTFT 2,8 s; GLM-5.3 64 tok/s *(pomiar zewnętrzny)*.

**Niezawodność.**
- OpenRouter pokazuje dla endpointu GLM-5.3-Flash od Z.ai 100 % dostępności w ciągu 1 dnia (13.10.2026). W moich źródłach nie było historii strony statusu.
- Szybkie tempo wydań: GLM-5.1, 5.2 i 5.3 wyszły w 2026 r., 5.3 i 5.3-Flash w odstępie ośmiu dni w sierpniu.
  W planie do kodowania żądania do 5.2, 5.1 lub 4.7 są już automatycznie kierowane do modeli 5.3.
- Z.ai wycofało swój ostatni darmowy model na OpenRouterze (`z-ai/glm-5.2:free`) 7.09.2026.

**Ograniczenia.**
- **GLM-5.3 jest tu powyżej progu** (4,40 USD za output). Z.ai to droga do Flash; GLM-5.3 kupuj u hosta zewnętrznego.
- Darmowy GLM-4.7-Flash to klasa 30B-A3B, poniżej mojego lokalnego DeepSeek-V4-Flash-0731 (AA 34). To nie jest prawdziwy darmowy poziom.
- Domyślny maksymalny reasoning effort sprawia, że koszty są nieprzewidywalne, dopóki nie ustawisz effortu na sztywno.
- **GLM Coding Plan nie nadaje się do użycia z mojego własnego agenta.** Kosztuje od 18 / 80 / 168 USD miesięcznie (Lite / Pro / Max; jeden
  tracker podaje 18 / 72 / 160), ale regulamin mówi, że *„may only be used within officially supported tools and products”*
  (Claude Code, OpenCode, Codex i inne), z banem po 3 naruszeniach i bez zwrotów. Użytkownicy zgłaszają też silny
  throttling od zmiany kredytów 14.08.2026.
- Brak opublikowanych limitów dla płatnego API.

**Gdzie pasuje w moim stosie.**
- **Domyślny tani sub-agent i worker do pracy masowej** na GLM-5.3-Flash z niskim effortem: bije mój lokalny model w trudnych zadaniach
  terminalowych (Vals TB4.0 37,4 wobec 18,7) przy 0,50 USD za output.
- Endpoint zgodny z Anthropic: mogę podpiąć pod niego harness w stylu Claude do niewrażliwych podzadań programistycznych.
- Po sam GLM-5.3 poszedłbym do hosta zewnętrznego albo agregatora, nie do Z.ai.
- Dane klientów i dane zawodowe zostają na lokalnym sprzęcie, jak wszędzie w tym przeglądzie.

**Sprawdź sam.**
```bash
curl https://api.z.ai/api/paas/v4/chat/completions -H "Authorization: Bearer $ZAI_API_KEY" -H "Content-Type: application/json" \
 -d '{"model":"glm-5.3-flash","reasoning_effort":"low","messages":[{"role":"user","content":"hi"}],
      "tools":[{"type":"function","function":{"name":"ping","parameters":{"type":"object","properties":{}}}}]}'
# tańsze hosty GLM-5.3, z kwantyzacją i dostępnością
curl -s https://openrouter.ai/api/v1/models/z-ai/glm-5.3/endpoints | jq '.data.endpoints[]|{provider_name,quantization,pricing,uptime_last_1d}'
```

**Źródła:** [Cennik Z.ai](https://docs.z.ai/guides/overview/pricing) · [Przewodnik Z.ai GLM-5.3](https://docs.z.ai/guides/llm/glm-5.3.md) · [Informacje o wydaniach Z.ai](https://docs.z.ai/release-notes/new-released.md) · [Przegląd GLM Coding Plan](https://docs.z.ai/devpack/overview.md) · [Zasady korzystania z GLM Coding Plan](https://docs.z.ai/devpack/usage-policy) · [FAQ GLM Coding Plan](https://docs.z.ai/devpack/faq.md) · [Ceny GLM na codingplan.org](https://codingplan.org/en/plans/glm) · [Zmiana cen na usagepricing](https://usagepricing.com/blueprint/activity/zhipu-ai-2026-07-22-price-change) · [Limity planów na zentor.ai](https://zentor.ai/blog/glm-coding-plan-rate-limits) · [Standard Compute o danych w Z.ai](https://standardcompute.com/providers/z-ai) · [toolnavs o darmowym GLM-4.7-Flash](https://toolnavs.com/en/article/1100-zai-released-glm-47-flash-weights-and-api-free-tier-1-concurrency-and-launched-f) · [AA GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash) · [AA GLM-5.3](https://artificialanalysis.ai/models/glm-5-3) · [Dostawcy GLM-5.3 w AA](https://artificialanalysis.ai/models/glm-5-3/providers) · [openbenchmarks: trafność tego samego modelu](https://openbenchmarks.com/inference/same-model-different-accuracy) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [API modeli OpenRoutera](https://openrouter.ai/api/v1/models)

---

## 5. Parasail

**Typ:** pay-as-you-go · **Najlepsze modele:** GLM-5.3-Flash AA 42, DeepSeek-V4.1-Flash AA 39, DeepSeek-V4-Flash-0731 AA 34 · **Wynik: 87** (Q26 C18 L14 A17 R12) · **Dane:** trenowanie na promptach: nieznane (brak informacji w moich źródłach); hosting w USA

> Mały amerykański broker serverless, który w każdym teście dokładności należy do najbardziej konsekwentnie wiernych tanich hostów, z ujawnioną kwantyzacją i bez publikowanych limitów zapytań.

**Co dostajesz.**
- Serverless pay-as-you-go „bez minimów i limitów zapytań” *(deklaracja dostawcy)*.
- **V4-Flash-0731 za 0,14 / 0,28 USD za 1M tokenów (wejście / wyjście), cache 0,05**, FP8: mój lokalny model u wiernego hosta.
- GLM-5.3-Flash za 0,15 / 0,50 USD i V4.1-Flash za 0,30 / 1,20 USD (13.10.2026).
- Darmowe kredyty: nieznane (brak na stronie cennika).

**Modele.** Ceny bezpośrednie, USD za 1M (wejście / wyjście), 13.10.2026; kwantyzacja według informacji ujawnionych na OpenRouter.

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| GLM-5.3-Flash | 42 | 1M (natywnie) | nieznane | tak | 0,15 / 0,50; FP4; 98,3% skuteczności w zadaniach z narzędziami *(pomiar zewnętrzny)* |
| DeepSeek-V4.1-Flash | 39 | 1M (natywnie) | nieznane | niezweryfikowane | 0,30 / 1,20 (cena referencyjna, taka sama jak w Together/Fireworks) |
| DeepSeek-V4-Flash-0731 | 34 | 1M (natywnie) | nieznane | niezweryfikowane | 0,14 / 0,28, cache 0,05; FP8; dostępność OR w ciągu 1 dnia 100% |
| GLM-5.3 | 45 | 1M (natywnie) | nieznane | niezweryfikowane | 1,40 / 4,40, cache 0,26: wyjście ponad mój limit 3 USD; FP8; dokładność endpointu 99 *(pomiar zewnętrzny)* |
| DeepSeek-V4-Pro-0813 | 36 | 1M (natywnie) | nieznane | niezweryfikowane | 1,32 / 3,96: ponad limit |

Serwowane są też: starszy DeepSeek V4 Flash 0423 (AA 24) za 0,14 / 0,28, Kimi K2.6 i K2.7 Code (AA 27 / 26, INT4) za 0,75 / 3,50, MiniMax-M3 (AA 29) 0,30 / 1,20, Qwen3.5-397B 0,50 / 3,60, gpt-oss-120b 0,10 / 0,75, Kimi K3 3 / 15 (OpenRouter 2,60 / 13). Wszystkie poniżej mojej poprzeczki lub ponad budżet.

**Limity i ceny.**
- Brak publikowanych limitów zapytań („bez minimów i limitów zapytań” *(deklaracja dostawcy)*); w praktyce spodziewaj się, że ograniczeniem będzie pojemność hosta.
- Brak minimalnych wydatków. W moich źródłach brak rabatu za batch lub poza godzinami szczytu.
- Ceny odpowiadają amerykańskiemu „referencyjnemu” cennikowi (V4.1-Flash 0,30 / 1,20, GLM-5.3-Flash 0,15 / 0,50); dla 0731 Parasail remisuje z Together przy 0,14 / 0,28, DeepInfra jest tańszy: 0,06 / 0,18.

**Jak uzyskać dostęp.**
1. Zarejestruj się na parasail.io. W moich źródłach nie ma udokumentowanych ograniczeń regionalnych dla Polski.
2. Dodaj płatności; darmowy kredyt nie jest reklamowany.
3. Utwórz klucz API i wyeksportuj go jako `PARASAIL_API_KEY`.
4. Albo pomiń zakładanie konta: Parasail jest dostawcą na OpenRouter, można go przypiąć przez `provider.only: ["Parasail"]`.

**Przydatność dla agentów.**
- Bazowy URL zgodny z OpenAI: `https://api.parasail.io/v1`. Moje źródła nie wspominają o endpoincie zgodnym z Anthropic; używaj go z harnessów opartych na OpenAI SDK lub przez OpenRouter.
- **Dokładność jest konsekwentnie bliska referencyjnej** *(pomiary zewnętrzne)*: AA Endpoint Accuracy Index GLM-5.3 99, GLM-5.2 98, gpt-oss-120b 97, Kimi K3 102 (26.09.2026); openbenchmarks GLM-5.3-Flash 98,3% na 600 ustrukturyzowanych zadaniach z narzędziami (Fireworks 99,5%, Nebius 84,8%).
- Co istotne, GLM-5.3-Flash w Parasail to FP4, a mimo to osiąga 98,3%: ujawniona kwantyzacja plus zmierzona dokładność to dokładnie to, czego oczekuję od hosta.
- Wywoływanie narzędzi w GLM-5.3-Flash jest potwierdzone testem zadań z narzędziami; dla modeli DeepSeek sprawdź `supported_parameters` na endpoincie OpenRouter, zanim zaczniesz polegać na `tools` lub `response_format`.

**Niezawodność.**
- Strona statusu: status.parasail.io. Dostępność OpenRouter w ciągu 1 dnia 97,4–100% dla jego endpointów (13.10.2026).
- W moich źródłach brak odnotowanych zmian w katalogu czy wycofań modeli (w przeciwieństwie do Fireworks czy Together).
- Mała firma: mniej publicznej dokumentacji, nieznane warunki dotyczące danych, nieznany darmowy kredyt.

**Ograniczenia.**
- **Warunki dotyczące danych nieznane**: nie znalazłem nic o retencji ani trenowaniu; nadaje się tylko do pracy z niewrażliwymi danymi, co i tak jest moją zasadą dla tej części stosu.
- V4.1-Flash przy 1,20 za wyjście to dwukrotność bezpośredniej ceny DeepInfra.
- Brak MiMo-V2.6-Pro; jedyne modele powyżej poprzeczki mieszczące się w budżecie to GLM-5.3-Flash i V4.1-Flash.
- Limity kontekstu i maksymalnego wyjścia nie są udokumentowane w moich źródłach; przetestuj długie konteksty, zanim zaczniesz polegać na 1M.
- **Niemal równoważna alternatywa: [Together AI](#9-together-ai).** Te same ceny referencyjne (0731 0,14 / 0,28, GLM-5.3-Flash 0,15 / 0,50 FP8, V4.1-Flash 0,30 / 1,20 FP8), ujawniona kwantyzacja, GLM-5.3-Flash 98,5% skuteczności w zadaniach z narzędziami, ale minimalne doładowanie 5 USD, domyślne przechowywanie promptów (przełącznik ZDR), ciche przekierowania wycofanych ID i dokładność gpt-oss-120b na poziomie zaledwie 81.

**Gdzie pasuje w moim stosie.**
- **Zapasowy host dla pętli narzędziowych na GLM-5.3-Flash**, drugi w `provider.order` po Fireworks na OpenRouter.
- Nadmiarowy ruch dla V4-Flash-0731, gdy chcę wiernego hosta z opublikowaną kwantyzacją, a nie najtańszego.
- Endpoint kontrolny w ewaluacjach: jeśli model zachowuje się źle u taniego hosta, powtórz test na Parasail, aby oddzielić błędy hosta od ograniczeń modelu.
- Najniższa cena DeepSeek: DeepInfra; dane wrażliwe: mój sprzęt lokalny.

**Sprawdź sam.**

```bash
# endpointy Parasail na OpenRouter: cena, kwantyzacja, dostępność
curl -s https://openrouter.ai/api/v1/models/z-ai/glm-5.3-flash/endpoints \
  | jq '.data.endpoints[]|select(.provider_name|test("Parasail"))|{provider_name,quantization,pricing,uptime_last_1d}'
# bezpośrednio: wylistuj modele i wybierz ID
curl -s https://api.parasail.io/v1/models -H "Authorization: Bearer $PARASAIL_API_KEY" | jq -r '.data[].id'
export PS_MODEL="<ID GLM-5.3-Flash z listy>"
curl -s https://api.parasail.io/v1/chat/completions -H "Authorization: Bearer $PARASAIL_API_KEY" \
  -H 'Content-Type: application/json' -d "{\"model\":\"$PS_MODEL\",
  \"messages\":[{\"role\":\"user\",\"content\":\"Pogoda w Poznaniu?\"}],
  \"tools\":[{\"type\":\"function\",\"function\":{\"name\":\"get_weather\",\"parameters\":{\"type\":\"object\",\"properties\":{\"city\":{\"type\":\"string\"}},\"required\":[\"city\"]}}}]}"
```

**Źródła:** [Parasail pricing](https://www.parasail.io/pricing) · [OpenRouter endpoints API](https://openrouter.ai/api/v1/models/z-ai/glm-5.3-flash/endpoints) · [AA Endpoint Accuracy Index](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) · [AA GLM-5.3 providers](https://artificialanalysis.ai/models/glm-5-3/providers) · [AA GLM-5.2 providers](https://artificialanalysis.ai/models/glm-5-2/providers) · [AA gpt-oss-120b providers](https://artificialanalysis.ai/models/gpt-oss-120b/providers) · [AA Kimi K3 providers](https://artificialanalysis.ai/models/kimi-k3/providers) · [openbenchmarks same-model accuracy](https://openbenchmarks.com/inference/same-model-different-accuracy) · [Together pricing](https://www.together.ai/pricing) · [Together serverless models](https://docs.together.ai/docs/serverless-models) · [Together ZDR](https://docs.together.ai/docs/zero-data-retention) · [Together changelog](https://docs.together.ai/docs/changelog)

---

## 6. DeepSeek API

**Typ:** pay-as-you-go · **Najlepsze modele:** `deepseek-flash` = DeepSeek-V4.1-Flash (AA 39) ·
**Wynik: 85** (Q23 C16 L15 A18 R13) · **Dane:** trenuje na promptach: opt-out (domyślnie włączone); przechowywane w ChRL

> Twórca mojego lokalnego modelu: ta sama rodzina o krok wyżej (V4.1-Flash), bardzo tania poza szczytem i praktycznie bez limitów zapytań.

**Co dostajesz.** Tylko pay-as-you-go, brak darmowego planu. **`deepseek-flash` kosztuje USD 0,15 / 0,60 za 1M tokenów (wejście /
wyjście) poza szczytem i USD 0,30 / 1,20 w szczycie**; trafienie w cache to USD 0,003 poza szczytem (13.10.2026). Konto dostaje 2500
równoległych żądań na Flash i żadnych limitów RPM ani TPM. Haczykiem są warunki dotyczące danych, nie cena.

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `deepseek-flash` (V4.1-Flash) | 39 (max) · 25 (bez rozumowania) | 1M | 384K | tak | MoE 552B / 16B, MIT, wydany 10.09.2026. Wejście: tekst + obraz. Vals TB2.1 74,5 vs 67,0 dla 0731 |
| `deepseek-v4-pro` (0813) | 36 | 1M | 384K | tak | 1,6T / 49B. Poniżej Flash w AA i w Vals TB4.0 (14,1). Nie warto |

**Mojego lokalnego modelu nie ma w tym API.** Stare ID `deepseek-v4-flash` i `deepseek-v4-flash-vision-exp` zostały
wycofane 10.09.2026 i teraz kierują do V4.1-Flash. **Wagi 0731 serwują tylko hosty zewnętrzne**
(OpenRouter, 13.10.2026): DeepInfra fp8 USD 0,06 / 0,18, Parasail fp8 i Together 0,14 / 0,28, Alibaba 0,176 / 0,528.

**Limity i ceny.**

| Model | Trafienie w cache (poza szczytem / szczyt) | Chybienie cache (poza szczytem / szczyt) | Wyjście (poza szczytem / szczyt) |
|---|---|---|---|
| `deepseek-flash` | 0,003 / 0,006 | 0,15 / 0,30 | 0,60 / 1,20 |
| `deepseek-v4-pro` | 0,022 / 0,044 | 0,66 / 1,32 | 1,98 / 3,96 |

- **Szczyt = 01:00–04:00 i 06:00–10:00 UTC, od poniedziałku do piątku** (bez chińskich świąt), wprowadzony 16.08.2026.
- **W czasie polskim to 03:00–06:00 i 08:00–12:00 CEST w dni robocze.** Po zmianie na czas zimowy
  25.10.2026 będzie to 02:00–05:00 i 07:00–11:00 CET (moje wyliczenie). Popołudnia, wieczory, noce i weekendy są poza szczytem.
- Równoległość: **2500 na Flash, 500 na Pro** na konto; więcej za darmo na prośbę. Po przekroczeniu limitu dostajesz HTTP 429.
- Brak limitów RPM/TPM. Pod obciążeniem serwer trzyma żądanie otwarte (puste linie keep-alive lub komentarze SSE `: keep-alive`)
  i zamyka je, jeśli inferencja nie ruszy w ciągu 10 minut.

**Jak uzyskać dostęp.**
1. Zarejestruj się na DeepSeek Open Platform przez e-mail lub telefon. Polska i UE są obsługiwane.
2. Doładuj kartą lub przez PayPal (PayPal niezweryfikowany).
3. Utwórz klucz i wyeksportuj go jako `DEEPSEEK_API_KEY`.
4. Skorzystaj z opt-out z trenowania opisanego w polityce prywatności, jeśli chcesz je wyłączyć (domyślnie włączone, wg zewnętrznej interpretacji polityki).

**Przydatność dla agentów.**
- Zgodne z OpenAI `https://api.deepseek.com`, zgodne z Anthropic `https://api.deepseek.com/anthropic`, plus
  Responses API. Wyjście JSON, wywołania narzędzi i uzupełnianie z prefiksem czatu działają w obu modelach; FIM (tryb bez myślenia) i
  wizja tylko na Flash.
- Myślenie jest **domyślnie włączone**, effort low / high / max. Sam model obsługuje effort 1–100, a effort 60–80
  daje większość dokładności poziomu max przy mniej niż połowie tokenów *(deklaracja dostawcy)*. V4.1-Flash to **najbardziej rozwlekły model, jaki AA
  zmierzyło** (250M tokenów wyjścia, miejsce 40 z 40), więc do rutynowych kroków ustawiaj effort low lub high.
- Szybki: 190 tok/s, TTFT 0,96 s *(pomiar zewnętrzny)*.
- Opcjonalny `user_id` daje izolację KV-cache i szeregowanie per użytkownik. Trzymaj prefiksy promptów stabilne: trafienie w cache kosztuje
  ok. 1–2 % ceny chybienia.
- Wrażliwość na harness: DeepSWE 69,8 w Claude Code vs 74,2 w mini-SWE-agent *(deklaracja dostawcy)*.
- Dokładność: DeepSeek nie publikuje szablonu czatu Jinja, więc hosty zewnętrzne piszą własne parsowanie narzędzi.
  API producenta jest implementacją referencyjną; w AA Endpoint Accuracy Index (V4-Pro, sierpień 2026) DeepSeek
  uzyskał 107 %, a każdy host 97–107 %, więc rodzina jest serwowana wiernie *(pomiar zewnętrzny)*.

**Niezawodność.**
- 90-dniowy uptime na status.deepseek.com (lipiec–październik 2026): **API V4.1-Flash 99,69 %**, API V4-Pro 99,92 %, brak otwartych incydentów.
- **Duża rotacja za jednym ID:** V4-Flash 0731 (31.07), Vision Exp (21.08), aktualizacja V4-Pro (13.08), V4.1-Flash
  (10.09, z nowym ID modelu). Przypnij `deepseek-flash` i spodziewaj się cichych aktualizacji za nim.
- Hosty zewnętrzne starych wag też rotują: Fireworks usunął V4-Flash 0731 i V4-Pro 0813 z publicznego
  serverless 26.09.2026.

**Ograniczenia.**
- **Domyślnie trenuje na promptach (opt-out), dane przechowywane w ChRL**, a DeepSeek nie oferuje DPA ani SCC klientom
  API; włoski Garante zablokował usługę DeepSeek *(doniesienia zewnętrzne)*. Wyłącznie dane niewrażliwe.
- Brak darmowego planu, a godziny szczytu podwajają cenę w polskie robocze przedpołudnie.
- V4.1-Flash to nie mój lokalny 0731, więc wyniki z API nie dowodzą, co zrobi mój sprzęt.
- Rozwlekłość zjada przewagę cenową przy effort max.

**Gdzie pasuje w moim stosie.**
- **Dodatkowa moc dla tej samej rodziny:** gdy 4 lokalne sloty są zajęte, przerzucam tu nadmiarowe niewrażliwe zadania; prompty
  napisane pod 0731 przenoszą się z niewielkimi zmianami.
- **Worker wsadowy poza szczytem:** planuj masowe zadania na popołudnia, wieczory i weekendy czasu polskiego.
- Zapasowy sub-agent z dużym budżetem wyjścia (384K) do długiego generowania.
- Do dokładnego odpowiednika 0731 (ewaluacje względem mojego sprzętu) użyj hosta zewnętrznego, nie tego API.

**Sprawdź sam.**
```bash
curl https://api.deepseek.com/models -H "Authorization: Bearer $DEEPSEEK_API_KEY"
curl https://api.deepseek.com/chat/completions -H "Authorization: Bearer $DEEPSEEK_API_KEY" -H "Content-Type: application/json" \
 -d '{"model":"deepseek-flash","messages":[{"role":"user","content":"pogoda w Warszawie?"}],
      "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
# kto nadal serwuje wagi 0731
curl -s https://openrouter.ai/api/v1/models/deepseek/deepseek-v4-flash-0731/endpoints | jq '.data.endpoints[]|{provider_name,quantization,pricing,uptime_last_1d}'
```

**Źródła:** [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) · [DeepSeek rate limit](https://api-docs.deepseek.com/quick_start/rate_limit) · [DeepSeek changelog](https://api-docs.deepseek.com/updates) · [DeepSeek status](https://status.deepseek.com/) · [AA V4.1-Flash](https://artificialanalysis.ai/models/deepseek-v4-1-flash) · [AA V4-Pro](https://artificialanalysis.ai/models/deepseek-v4-pro) · [AA V4-Pro providers](https://artificialanalysis.ai/models/deepseek-v4-pro/providers) · [AA Endpoint Accuracy Index](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) · [DeepSeek-V4.1-Flash paper](https://arxiv.org/pdf/2609.19969) · [HF V4-Flash-0731 card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) · [Vals TB2.1](https://www.vals.ai/benchmarks/terminal-bench-2-1) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [OpenRouter models API](https://openrouter.ai/api/v1/models) · [Fireworks changelog](https://docs.fireworks.ai/updates/changelog) · [Meetily on DeepSeek data](https://meetily.ai/llm-privacy/deepseek) · [ComplianceHub on the Garante block](https://www.compliancehub.wiki/italys-privacy-watchdog-blocks-deepseek-ai-a-gdpr-battle-begins)

---

## 7. Alibaba Cloud Model Studio (international)

**Typ:** jednorazowe kredyty (1M darmowych tokenów na model), potem pay-as-you-go · **Najlepsze modele:** trial: `qwen3.8-max` (AA 45), `glm-5.3` (AA 45), `kimi-k3` (AA 44); PAYG w przedziale: `qwen3.8-flash` (AA 40), `deepseek-v4.1-flash` (AA 39) ·
**Wynik: 85** (Q29 C17 L11 A17 R11) · **Dane:** trenuje na promptach: nie („will never use your data for model training”); hosting w Singapurze

> Jedno konto daje darmową, 90-dniową próbkę niemal każdego mocnego modelu (Qwen3.8-Max, GLM-5.3, Kimi K3, DeepSeek V4.1), a potem tanie Qwen i DeepSeek w pay-as-you-go.

**Co dostajesz.** Nowi użytkownicy dostają **1M darmowych tokenów na model, ważnych 90 dni od aktywacji Model Studio**, jednorazowo,
dla każdego modelu z regionu Singapur o zakresie wdrożenia „International” (dokumentacja zaktualizowana 11.10.2026). Potem to
zwykłe pay-as-you-go: wybory w przedziale to **`qwen3.8-flash` za 0,15 / 0,47 USD za 1M tokenów (wejście / wyjście)** oraz
`deepseek-v4.1-flash` za 0,15 / 0,60 USD w godzinach niskiego obciążenia (13.10.2026).

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `qwen3.8-flash` | 40 (jako Qwen3.8-Flash-Next) | 1M na OpenRouter · 262K natywnie dla Flash-Next | nie podano | nie podano | Jedynym hostem jest Alibaba. Sprawdź, jakim modelem naprawdę jest to ID (patrz Ograniczenia) |
| `deepseek-v4.1-flash` | 39 | 1M | nie podano | tak | Niskie obciążenie 0,15 / 0,60 USD, szczyt 0,30 / 1,20 |
| `qwen3.8-max` | 45 | nie podano | nie podano | nie podano | 2 / 6 USD: dla mnie tylko w trialu |
| `ZHIPU/GLM-5.3` | 45 | 1M | nie podano | tak | 1,40 / 4,40 USD: tylko trial |
| `kimi-k3` | 44 | 1M | nie podano | tak | 3 / 15 USD: tylko trial |

**Limity i ceny.**
- PAYG, Singapur, USD za 1M wejścia / wyjścia (strona zaktualizowana 13.10.2026):
  - `qwen3.8-flash` 0,15 / 0,47 (cache 0,016 na OpenRouter) · `qwen3.7-plus` 0,40 / 1,60 do 256K (AA 25, poniżej progu).
  - `deepseek-v4.1-flash` niskie obciążenie 0,15 / 0,60, szczyt 0,30 / 1,20 · `deepseek-v4-pro-0813` niskie obciążenie 0,66 / 1,98, szczyt 1,32 / 3,96.
  - Poza przedziałem: `qwen3.8-max` 2 / 6, GLM-5.3 1,40 / 4,40, `kimi-k3` 3 / 15.
- **Batch to −50 %**; cache kontekstu jest przeceniony. Godziny niskiego obciążenia i szczytu dla DeepSeek nie zostały opublikowane w moich źródłach.
- OpenRouter wymienia też Alibabę jako hosta mojego lokalnego **DeepSeek-V4-Flash-0731 za 0,176 / 0,528 USD** (13.10.2026).
- Darmowa pula jest mała dla agentów: **1M tokenów to kilkadziesiąt długich zadań agentowych na model**. Przełącznik „Free Quota Only”
  zatrzymuje usługę przy zerze (błąd `AllocationQuota.FreeTierOnly`), więc nie ma niespodziewanego rachunku.
- Nie znalazłem opublikowanych wartości RPM/TPM dla PAYG (13.10.2026).

**Jak uzyskać dostęp.**
1. Załóż **międzynarodowe** konto Alibaba Cloud; jest otwarte dla użytkowników z UE. Zwykle wymagana jest karta do weryfikacji
   (nie sprawdzałem ponownie 13.10.2026).
2. Aktywuj Model Studio w regionie **Singapur**: tu startuje 90-dniowy zegar, więc aktywuj, gdy będziesz gotów do testów.
3. Włącz „Free Quota Only” na czas ewaluacji.
4. Utwórz klucz API i wyeksportuj go jako `DASHSCOPE_API_KEY`.

**Przydatność dla agentów.**
- Zgodny z OpenAI `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`.
- **Zgodny z Anthropic** `https://dashscope-intl.aliyuncs.com/apps/anthropic`, do użycia z Claude Code przez `ANTHROPIC_BASE_URL`.
- ID modeli rozróżniają wielkość liter i mają mieszany styl (`ZHIPU/GLM-5.3` obok `kimi-k3`): kopiuj je z `/models`.
- Qwen3.8-Flash-Next: TB2.1 86,1, DeepSWE 58,7, SWE-Pro 62,5 *(deklaracja producenta)*; brak jeszcze niezależnych wyników agentowych.
  Bardzo rozwlekły (240M tokenów w przebiegu AA).
- W moich źródłach nie było zewnętrznego pomiaru trafności wywołań narzędzi na endpointach Alibaby.

**Niezawodność.**
- Warunki się zmieniają: **darmowy tier OAuth Qwen Code został wyłączony 15.04.2026** (1000 RPD, potem 100, potem zero), a
  Coding Plan Lite zamknięto dla nowych kupujących 20.03.2026 i dla odnowień 13.04.2026.
- Brak danych o dostępności (uptime) ani statusie Model Studio w moich źródłach.

**Ograniczenia.**
- Darmowe tokeny są **jednorazowe**, a nie odnawialnym darmowym tierem.
- **`qwen3.8-flash` może nie być modelem, któremu AA daje 40**: zewnętrzny raport mówi, że „Qwen3.8-Flash” w Qwen Cloud to nie
  to samo ID co Qwen3.8-Flash-Next. Zweryfikuj przez `/models` i własną ewaluację.
- **Coding Plan** (tylko Pro za 50 USD miesięcznie; 6000 żądań na 5 godzin, 45 000 tygodniowo, 90 000 miesięcznie) ma starą listę
  modeli (bez Qwen3.8, bez GLM-5.3) i mówi *„Do not use the plan's API key for automated scripts, application backends,
  or other non-interactive scenarios”*; strony trzecie zgłaszają ryzyko bana.
- **Token Plan** (od Lite za 6 USD za 11,5k kredytów do Pro za 68 USD za 180k) jest sprzedawany dla wymienionych narzędzi (Claude Code,
  Cursor, Qwen Code, Codex i inne), a przelicznik kredytów na tokeny nie jest opublikowany. Nie uruchamiałbym na nim własnego agenta.
- Hosting w Singapurze; okres retencji nie jest podany.

**Gdzie pasuje w moim stosie.**
- **Darmowy runner ewaluacji przez 90 dni:** jednorazowo puszczam mój zestaw ewaluacyjny na Qwen3.8-Max, GLM-5.3, Kimi K3 i V4.1-Flash na jednym
  kluczu, zanim zainwestuję pieniądze u jakiegokolwiek dostawcy.
- **Tani worker PAYG** na `qwen3.8-flash`, gdy już potwierdzę, jaki to model, z batchem za −50 % dla zadań offline.
- Drugie źródło dla DeepSeek V4.1-Flash i być może do dokładnych porównań 0731 z moim sprzętem.
- Do produkcyjnych pętli agentowych wciąż wolałbym trasę z opublikowanymi limitami i dostępnością.

**Sprawdź sam.**
```bash
curl -s https://dashscope-intl.aliyuncs.com/compatible-mode/v1/models -H "Authorization: Bearer $DASHSCOPE_API_KEY"
curl -s https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" -d '{"model":"qwen3.8-flash","messages":[{"role":"user","content":"hi"}]}'
```

**Źródła:** [Model Studio – darmowa pula](https://www.alibabacloud.com/help/en/model-studio/new-free-quota) · [Model Studio – cennik](https://www.alibabacloud.com/help/en/model-studio/model-pricing) · [Model Studio – modele](https://www.alibabacloud.com/help/en/model-studio/models) · [Model Studio – informacja o prywatności](https://www.alibabacloud.com/help/en/model-studio/privacy-notice) · [Coding Plan](https://www.alibabacloud.com/help/en/model-studio/coding-plan) · [Token Plan](https://www.alibabacloud.com/help/en/model-studio/token-plan-overview) · [Token Plan – strona docelowa](https://www.alibabacloud.com/en/campaign/ai-landing-page-token) · [Kong – URL Anthropic dla DashScope](https://developer.konghq.com/ai-gateway/use-claude-code-with-ai-gateway-dashscope/) · [vibecoding.app – recenzja planu](https://vibecoding.app/blog/alibaba-coding-plan-review) · [Qwen Code – issue 1742](https://github.com/QwenLM/qwen-code/issues/1742) · [inventivehq o wyłączeniu Qwen Code](https://inventivehq.com/blog/qwen-code-still-free-2026-shutdown) · [AA Qwen3.8-Flash-Next](https://artificialanalysis.ai/models/qwen3-8-flash-next) · [llm-stats Qwen3.8-Flash-Next](https://llm-stats.com/blog/research/qwen3.8-flash-next-launch) · [OpenRouter – API modeli](https://openrouter.ai/api/v1/models)

---

## 8. Xiaomi MiMo API

**Typ:** pay-as-you-go (istnieje stały Token Plan, ale nie dla własnych agentów) · **Najlepsze modele:** `mimo-v2.6-pro` (AA 46), `mimo-v2.6-flash` (AA 38) ·
**Wynik: 83** (Q30 C16 L11 A15 R11) · **Dane:** trenuje na promptach: domyślnie nie *(podsumowanie strony trzeciej)*; podmioty umowne w Holandii i Singapurze, lokalizacja serwerów nie jest podana

> Najwyżej oceniany otwarty model w tym przeglądzie (MiMo-V2.6-Pro, AA 46) za mniej niż 1 USD za wyjście, sprzedawany bezpośrednio przez twórcę.

**Co dostajesz.** API pay-as-you-go zgodne z OpenAI. **MiMo-V2.6-Pro kosztuje 0,435 / 0,87 USD za 1M tokenów
(wejście / wyjście), odczyt z cache 0,0036 USD**, a zapisy do cache są przez ograniczony czas darmowe (13.10.2026). Xiaomi obniżyło ceny
na stałe nawet o 99 % 27.05.2026. Nie ma darmowego tieru; metoda płatności jest wymagana, zanim klucz zadziała.

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `mimo-v2.6-pro` | 46 (#1 wśród otwartych wag) | 1M | 128K | tak | MoE 1,02T / 42B, MIT, wydany 21.09.2026. Vals TB4.0 31,3, TB2.1 67,8 |
| `mimo-v2.6-flash` | 38 | 1M | nie podano | tak | MoE 309B / 15B, MIT. Vals TB2.1 76,4 (lepszy niż V4.1-Flash), TB4.0 24,2 |

Oba przyjmują na wejściu tekst, obraz, audio i wideo. Rozumowanie jest domyślnie włączone.

**Limity i ceny.**
- PAYG, USD za 1M wejścia / odczytu z cache / wyjścia (13.10.2026):
  - `mimo-v2.6-pro` 0,435 / 0,0036 / 0,87.
  - `mimo-v2.6-flash` 0,14 / 0,003 (OpenRouter) / 0,28.
  - `mimo-v2.6-pro-ultraspeed` 4,35 / 8,70 przy około 116 tok/s: poza przedziałem.
- Koszt AA na zadanie indeksu dla Pro: **0,13 USD** *(pomiar strony trzeciej)*.
- Brak wartości RPM/TPM dla PAYG na stronach, które przeczytałem (13.10.2026).
- **Token Plan:** Lite 6 USD, Standard 16, Pro 50, Max 100 miesięcznie za 4,1B / 11B / 38B / 82B kredytów (rocznie −12 %).
  Pro kosztuje 300 / 2,5 / 600 kredytów za token (wejście bez cache / trafienie w cache / wyjście); poza szczytem 0,8× w godz. 16:00–24:00 UTC
  (18:00–02:00 CEST). Według moich obliczeń Lite jest wart około 5,9 USD w PAYG za 6 USD, więc plan oszczędza tylko
  **0–20 %** (więcej poza szczytem).

**Jak uzyskać dostęp.**
1. Załóż konto Xiaomi i otwórz platformę deweloperską MiMo. Podmioty to Xiaomi Technology Netherlands B.V.
   i Xiaomi Singapore, więc rejestracja z Polski działa.
2. Dodaj metodę płatności: klucz nie działa, dopóki jakaś nie jest zapisana.
3. Utwórz klucz PAYG i wyeksportuj go jako `MIMO_API_KEY`. Nie używaj klucza Token Plan do własnego agenta.

**Przydatność dla agentów.**
- Bazowy URL PAYG: `https://api.xiaomimimo.com/v1` (zgodny z OpenAI). Endpointy Token Plan
  (`token-plan-{cn,sgp,ams}.xiaomimimo.com/v1`, ams = Amsterdam) mają też wariant `/anthropic`.
- Wywoływanie narzędzi, rozumowanie i wejście multimodalne są obsługiwane; wyjście JSON jest **„miękkie”** (brak trybu ścisłego schematu w moich
  źródłach), więc waliduj i ponawiaj.
- **Pułapka:** Xiaomi ostrzega, że endpoint zgodny z Anthropic zwraca **HTTP 400 przy wieloturowych wywołaniach narzędzi, jeśli
  treść rozumowania nie jest odsyłana z powrotem**. Odsyłaj `reasoning_content` w historii.
- **Wolny:** 46,8 tok/s, TTFT 4,0 s *(pomiar strony trzeciej)*. W porządku dla planera lub recenzenta, bolesny w ciasnych pętlach.
- Praktyczny test DevOps: Terraform i bash wyszły dobrze; manifesty Kubernetes przeszły lintery, ale wpadały w crash-loop (1 z 3 OK).
  Flash uzyskał 0 z 3 *(pomiar strony trzeciej)*.
- Niezależne wyniki agentowe są niejednoznaczne: Vals TB2.1 67,8 to mniej więcej tyle, co 67,0 mojego lokalnego modelu, ale **TB4.0 31,3 jest wyraźnie powyżej
  progu 18,7**. TB2.1 89,9 producenta *(deklaracja producenta)* jest daleko powyżej niezależnego wyniku.

**Niezawodność.**
- OpenRouter pokazuje endpoint Xiaomi Pro z **95,9 % dostępności w ciągu 1 dnia** wobec 100 % dla DeepInfra w tej samej cenie (13.10.2026).
- Niewielu hostów serwuje Pro (4 na OpenRouter, część ze statusem degraded), więc API producenta to główna trasa.
- Krótka historia: V2.6 wyszedł 21.09.2026, cztery miesiące po majowej obniżce cen.

**Ograniczenia.**
- **Token Plan nie jest dla własnych agentów:** *„only available for use in programming tools… prohibited… automated
  scripts and custom application backends”*. Używaj PAYG; plan i tak oszczędza tylko 0–20 %.
- Wolny pierwszy token i niska przepustowość dla Pro.
- Warunki dotyczące danych opierają się na podsumowaniach stron trzecich (domyślnie bez trenowania, ZDR dla Enterprise); nie przeczytałem całej
  polityki prywatności.
- Brak opublikowanych limitów PAYG, więc od początku zaplanuj obsługę 429.
- Wymagana karta: nie da się przetestować bez płacenia.

**Gdzie pasuje w moim stosie.**
- **Tani planer lub recenzent** do niewrażliwych zadań: AA 46 za 0,87 USD za wyjście to najlepsza jakość za dolara, jaką znalazłem.
- **MiMo-V2.6-Flash jako worker masowy** za 0,28 USD za wyjście tam, gdzie liczy się praca w terminalu w stylu TB2.1.
- Nie do wewnętrznych pętli ograniczonych opóźnieniem; tam lepszy jest lokalny sprzęt albo szybki host.
- Jako druga trasa do tych samych wag w tej samej cenie i z lepszą dostępnością: DeepInfra serwuje Pro za 0,43 / 0,87 USD.

**Sprawdź sam.**
```bash
curl https://api.xiaomimimo.com/v1/chat/completions -H "Authorization: Bearer $MIMO_API_KEY" -H "Content-Type: application/json" \
 -d '{"model":"mimo-v2.6-pro","messages":[{"role":"user","content":"hi"}],"tools":[{"type":"function","function":{"name":"ping","parameters":{"type":"object","properties":{}}}}]}'
# inni hości tych samych wag, z dostępnością
curl -s https://openrouter.ai/api/v1/models/xiaomi/mimo-v2.6-pro/endpoints | jq '.data.endpoints[]|{provider_name,quantization,pricing,uptime_last_1d}'
```

**Źródła:** [MiMo Token Plan](https://mimo.mi.com/docs/en-US/tokenplan/Token%20Plan/subscription) · [eesel – cennik MiMo](https://www.eesel.ai/blog/xiaomi-mimo-v2-6-pricing) · [TypingMind – przewodnik MiMo](https://www.typingmind.com/guide/xiaomi/mimo-v2.6-pro) · [kingy.ai – konfiguracja MiMo](https://kingy.ai/blog/mimo-v2-6-pro-free-access-pricing-setup/) · [36kr – obniżka cen](https://eu.36kr.com/en/p/3826964226691972) · [AA MiMo-V2.6-Pro](https://artificialanalysis.ai/models/mimo-v2-6-pro) · [AA MiMo-V2.6-Flash](https://artificialanalysis.ai/models/mimo-v2-6-flash) · [Vals TB2.1](https://www.vals.ai/benchmarks/terminal-bench-2-1) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [computingforgeeks – test MiMo](https://computingforgeeks.com/xiaomi-mimo-v2-6-pro-flash/) · [OpenRouter – API modeli](https://openrouter.ai/api/v1/models)

---

## 9. Together AI

**Typ:** pay-as-you-go · **Najlepsze modele:** GLM-5.3 (AA 45), GLM-5.3-Flash (AA 42), DeepSeek-V4.1-Flash (AA 39) ·
**Wynik: 82** (Q26 C17 L13 A15 R11) · **Dane:** trenowanie na promptach: nie (opt-in, domyślnie wyłączone); prompty i odpowiedzi
domyślnie przechowywane, dostępny przełącznik ZDR; hosting w USA

> Amerykański host serverless z dostępem po cenach katalogowych do każdej mocnej rodziny modeli open-weight i najlepszym ujawnianiem kwantyzacji
> w grupie, dlatego zajmuje wysokie miejsce mimo braku darmowego poziomu.

**Co dostajesz.** Kredyty prepaid, **minimalne doładowanie 5 USD, brak darmowego okresu próbnego od lipca 2025**. API zgodne z OpenAI,
kontekst 1M w modelach DeepSeek V4 i GLM-5.x, Batch API (wysokości rabatu nie ma na stronie). AA = Artificial Analysis
Intelligence Index v4.3.2 według stanu na 13.10.2026; mój lokalny DeepSeek-V4-Flash-0731 ma AA 34.

**Modele.**

| Model | AA | Kontekst | Maks. output | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `zai-org/GLM-5.3` | 45 | 1M | nie odczytano | tak | FP4 · trafność endpointu AA 97 |
| `zai-org/GLM-5.3-Flash` | 42 | 1M | nie odczytano | tak | FP8 · 98,5% skuteczności w zadaniach narzędziowych |
| `deepseek-ai/DeepSeek-V4.1-Flash` | 39 | 1M | nie odczytano | tak | FP8 · dodany 11.09.2026 |
| `deepseek-ai/DeepSeek-V4-Pro-0813` | 36 | 1M | nie odczytano | tak | NVFP4 · output powyżej 3 USD |
| `deepseek-ai/DeepSeek-V4-Flash-0731` | 34 | 1M | nie odczytano | tak | ten sam model co na moim lokalnym sprzęcie |

**Limity i ceny.** USD za 1M tokenów (input / z cache / output), 13.10.2026:
- GLM-5.3-Flash 0,15 / 0,03 / 0,50 · V4-Flash-0731 0,14 / 0,03 / 0,28 · V4.1-Flash 0,30 / 0,006 / 1,20.
- GLM-5.3 i GLM-5.2 1,40 / 0,26 / 4,40 · V4-Pro-0813 1,32 / 0,13 / 3,96 · MiniMax-M3 0,30 / 0,06 / 1,20 (524k).
- gpt-oss-120b 0,15 / 0,60 (MXFP4, 131k) · Kimi-K3 3 / 0,30 / 15.
- **„Dynamic rate limits for serverless retired” 2.10.2026**; nie są publikowane stałe RPM/TPM.
- Saldo może zejść na minus do -100 USD na poziomach 1–4.

**Jak uzyskać dostęp.**
1. Zarejestruj się na together.ai (dostępne w Polsce).
2. Kup kartą kredyty za co najmniej 5 USD.
3. Org Settings → Privacy → ustaw „Store prompts and model responses” na **No**, zanim cokolwiek wyślesz.
4. Utwórz klucz API w panelu i wyeksportuj go jako `TOGETHER_API_KEY`.

**Przydatność dla agentów.** Bazowy URL zgodny z OpenAI `https://api.together.xyz/v1`; w researchu nie znalazłem endpointu Anthropic. Trafność
dostawcy jest dobra na modelach, które się liczą *(pomiar zewnętrzny)*: AA Endpoint Accuracy Index GLM-5.2 97, GLM-5.3
97, Kimi K3 100; openbenchmarks GLM-5.3-Flash 98,5% na 600 zadaniach narzędziowych (3.09.2026); KVV Kimi K3 w granicach szumu względem
Moonshot. **Wyjątek: gpt-oss-120b uzyskuje tylko 81** w indeksie endpointów AA, więc nie używaj go tutaj.

**Niezawodność.** Status na status.together.ai. Dostępność w ciągu 1 dnia na OpenRouterze 94–100% (gpt-oss 94,4%, GLM-5.3 97,0%,
V4-Flash-0731 99,8%) 13.10.2026. Częste wycofywanie modeli serverless (gpt-oss-20b 14.09.2026) i **ciche
przekierowania** wycofanych ID (GLM-4.6 → GLM-4.7, DeepSeek-V3-0324 → V3.1).

**Ograniczenia.**
- Żadnego darmowego limitu; na start 5 USD.
- Prompty są domyślnie przechowywane, dopóki nie przełączysz ZDR.
- Stare ID modeli mogą być po cichu przekierowane na nowszy model, co psuje powtarzalność ewaluacji.
- Endpoint gpt-oss-120b jest zdegradowany (AA 81).
- Przetwarzanie tylko w USA.

**Gdzie pasuje w moim stosie.**
- **Worker do pracy masowej na GLM-5.3-Flash** (AA 42 przy 0,50 USD za output): mądrzejszy od mojego lokalnego modelu, wystarczająco tani na batch.
- Chmurowy przelew dla mojego lokalnego V4-Flash-0731 za 0,28 USD za output, te same wagi, więc prompty przenoszą się bez zmian.
- GLM-5.3 jako planer średniego poziomu, gdy Opus to przesada; dane klientów jak zawsze zostają lokalnie.

**Sprawdź sam.**
```bash
curl -s https://api.together.xyz/v1/models -H "Authorization: Bearer $TOGETHER_API_KEY" | jq '.[].id' | head
```

**Źródła:** [Cennik Together](https://www.together.ai/pricing) · [Modele serverless](https://docs.together.ai/docs/serverless-models) · [Changelog](https://docs.together.ai/docs/changelog) · [Zero data retention](https://docs.together.ai/docs/zero-data-retention) · [Zmiana darmowego poziomu, lipiec 2025](https://support.together.ai/articles/1862638756-changes-to-free-tier-and-billing-july-2025) · [AA DeepSeek V4 Flash](https://artificialanalysis.ai/models/deepseek-v4-flash)

---

## 10. NVIDIA build.nvidia.com (NIM trial API)

**Typ:** darmowy pakiet (wersja próbna dla deweloperów, tylko do prototypowania) · **Najlepsze modele:** `z-ai/glm-5.3` (AA 45), `moonshotai/kimi-k3` (AA 44), `z-ai/glm-5.3-flash` (AA 42), `deepseek-ai/deepseek-v4.1-flash` (AA 39) ·
**Wynik: 79** (Q29 C20 L10 A14 R6) · **Dane:** trenowanie na promptach: nieznane, NVIDIA „może wykorzystywać” treści do ulepszania swoich produktów i modeli; hosting w USA (założenie, nie podano wprost)

> Darmowe hostowane endpointy NIM od NVIDII to na 13.10.2026 jedyne miejsce, gdzie dostaję GLM-5.3 i Kimi K3 za USD 0 z
> API zgodnym z OpenAI, dlatego wypada wysoko pod względem jakości i kosztu, mimo że regulamin mówi „tylko do prototypowania”.

**Co dostajesz.** Darmowy klucz API dla członków NVIDIA Developer Program, bez karty. Aktualna lista `/v1/models` miała
**80 identyfikatorów modeli na 13.10.2026**. **Nie ma opublikowanego limitu tokenów ani dziennego**: jedyna spójna liczba to
**około 40 żądań na minutę na konto** *(pomiar zewnętrzny, konsensus społeczności i forum)*. Gwiazdą jest Kimi K3: wszędzie
indziej kosztuje od USD 9,50 do 15 za 1M tokenów wyjściowych, tutaj jest za darmo.

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `z-ai/glm-5.3` | 45 | 1M | nie podano | tak | ~40B aktywnych, rozumowanie; najlepsze niezależne wyniki agentowe wśród tanich otwartych modeli (Vals TB4.0 38,9) |
| `moonshotai/kimi-k3` | 44 | 1 048 576 | nie podano | tak | myślenie zawsze włączone; odsyłaj `reasoning_content` i `tool_calls` w każdej turze |
| `z-ai/glm-5.3-flash` | 42 | 1M | nie podano | nie podano | 18B aktywnych, multimodalny, ustrukturyzowane wyjście |
| `deepseek-ai/deepseek-v4.1-flash` | 39 | 1 048 576 | nie podano | tak | na build od 18.09.2026; wysiłek rozumowania od 1 do 100; cache KV w FP4 |

Poniżej mojej poprzeczki (AA 34) i przydatne tylko do trywialnych kroków: `moonshotai/kimi-k2.6` (AA 27), `nvidia/nemotron-3-ultra-550b-a55b`
(AA 23), `google/gemma-4-31b-it` (AA 15). Kwantyzacja **nie jest ujawniana** dla poszczególnych endpointów, poza wzmianką o FP4 KV przy V4.1-Flash.

**Limity i ceny.** Stan na 13.10.2026:
- Cena: USD 0. NVIDIA **nie** publikuje limitu żądań.
- **~40 RPM na konto, wspólne dla wszystkich modeli**, nie na model *(pomiar zewnętrzny)*. Moderator forum (lipiec 2026)
  napisał, że limit „zależy od modelu, przypadku użycia i ogólnego ruchu” i nie można go oficjalnie podnieść w darmowym pakiecie.
  Niektóre źródła zewnętrzne twierdzą, że nieformalnie przyznawane jest 200 RPM.
- Limit dzienny: **nieznany**. Źródła są sprzeczne: „bez limitu, ale RPM” (forum, maj 2026), „1000 kredytów” (starsze strony, powtórzone
  02.10.2026), „10 000 RPD na model” (jedna lista z października 2026).
- Błędy 429 pojawiają się po serii żądań nawet poniżej 40 RPM.
- Użycie produkcyjne wymaga NVIDIA AI Enterprise (od USD 4500 za GPU rocznie, około USD 1 za GPU-godzinę) lub jego 90-dniowej wersji próbnej.

**Jak uzyskać dostęp.**
1. Załóż konto NVIDIA i dołącz do NVIDIA Developer Program. Bez karty.
2. Przejdź **weryfikację telefonu przez SMS**; wcześniej klucz nie jest aktywowany (zgłoszone 01.10.2026).
3. Polska: brak doniesień o blokadzie. Lista obsługiwanych krajów jest niepełna (np. Rosja nie jest obsługiwana).
4. Wygeneruj klucz API na build.nvidia.com i wyeksportuj go jako `NVIDIA_API_KEY`.

**Przydatność dla agentów.**
- **Zgodny z OpenAI** bazowy URL `https://integrate.api.nvidia.com/v1` (`/chat/completions`, streaming, narzędzia).
  **Brak endpointu zgodnego z Anthropic**, więc harness w stylu Claude potrzebuje proxy tłumaczącego.
- Kimi K3 psuje naiwne pętle: w każdym wieloturowym żądaniu musisz odesłać pełną wiadomość asystenta, łącznie z `reasoning_content` i
  `tool_calls`.
- V4.1-Flash udostępnia wysiłek od 1 do 100; GLM-5.3 obsługuje rozumowanie i wywoływanie narzędzi; GLM-5.3-Flash obsługuje ustrukturyzowane wyjście.
- **Prawdziwym limitem jest współbieżność**: 40 RPM dotyczy całego konta, więc cztery równoległe sub-agenty dzielą się nim.
- Długie tury rozumowania plus kolejkowanie powodują timeouty po stronie klienta. Ustaw długie timeouty i ponawiaj 429 i 504 z backoffem.
- W moich źródłach brak danych o dokładności własnych endpointów NVIDII.

**Niezawodność.**
- **Brak SLA i brak publicznej strony statusu** dla API próbnego.
- Forum, maj 2026: nowe modele (GLM 5.1, Kimi K2.6) „ciągle mają timeout”, co przypisano użytkownikom agentów wysyłającym tysiące RPM;
  nie pojawiła się poprawka ze strony pracowników. Interfejs webowy w szczytach pokazuje „setki żądań w kolejce”.
- Hostowany przez NVIDIĘ endpoint `nemotron-3-ultra:free` na OpenRouter miał **77,4 % dostępności dobowej, stan degraded**,
  13.10.2026 *(pomiar zewnętrzny)*.
- **Rotacja katalogu jest realna**: dokumentacja wciąż wymienia `deepseek-v4-pro`, `deepseek-v4-flash(-0731)`, `minimax-m2.5`/`m2.7`,
  `gpt-oss-120b`, `qwen3-next-80b` i `glm-5.1`/`5.2`, ale żadnego z nich nie było na aktualnej liście 13.10.2026.

**Ograniczenia.**
- **Regulamin mówi: tylko prototypowanie, badania, rozwój i testy.** To nie jest backend produkcyjny.
- Dane: treści są używane do świadczenia usługi i domyślnie nie są przechowywane po sesji, **ale** NVIDIA może je monitorować,
  skanować i wykorzystywać do ulepszania produktów i modeli AI (zewnętrzne streszczenia regulaminu wersji próbnej). Tylko dane niewrażliwe.
- Brak opublikowanych limitów; limit dzienny jest nieznany i może się zmienić bez uprzedzenia.
- Modele znikają bez uprzedzenia; nie przypinaj niczego, czego nie da się zastąpić.
- Timeouty i kolejki na popularnych modelach dokładnie wtedy, gdy wszyscy inni też ich używają.

**Gdzie pasuje w moim stosie.**
- **Darmowa ewaluacja GLM-5.3 i Kimi K3**, zanim zapłacę za nie gdzie indziej: uruchamiam tu swój zestaw ewaluacyjny
  ([../kurs_aplikacje_agentowe/14-EWALUACJA.md](../kurs_aplikacje_agentowe/14-EWALUACJA.md)) przy ~40 RPM.
- Darmowy sub-agent „mądrzejszy niż lokalny” do prototypów: GLM-5.3 (AA 45) jako recenzent lub drugi planista obok mojego lokalnego
  V4-Flash-0731 (AA 34).
- **Nie do niczego, co musi skończyć się na czas**: przy zadaniach masowych lub harmonogramowanych moje 4 lokalne sloty są bardziej przewidywalne, a
  na produkcję zapłaciłbym hostowi z SLA.
- Tylko jako fallback za routerem z płatną trasą za nim, nigdy jako ostatni przeskok.

**Sprawdź sam.**
```bash
curl -s https://integrate.api.nvidia.com/v1/models | jq -r '.data[].id'   # klucz nie jest potrzebny
curl -s https://integrate.api.nvidia.com/v1/chat/completions -H "Authorization: Bearer $NVIDIA_API_KEY" \
  -H "Content-Type: application/json" -d '{"model":"deepseek-ai/deepseek-v4.1-flash","messages":[{"role":"user","content":"Pogoda w Warszawie?"}],
  "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}],"max_tokens":1024}'
```

**Źródła:** [NVIDIA aktualna lista modeli](https://integrate.api.nvidia.com/v1/models) · [build.nvidia.com DeepSeek V4.1-Flash](https://build.nvidia.com/deepseek-ai/deepseek-v4.1-flash) · [Dokumentacja produktu NIM](https://docs.api.nvidia.com/nim/docs/product) · [Dokumentacja API LLM NIM](https://docs.api.nvidia.com/nim/reference/llm-apis) · [dev.to: test darmowej oferty NVIDII](https://dev.to/klukyanov/kimi-k3-deepseek-and-glm-free-from-nvidia-i-tested-the-claim-and-here-is-the-catch-2m9b) · [klymentiev.com: wpis o kredytach](https://klymentiev.com/blog/nvidia-nim-free-credits) · [Forum NVIDIA: czy NIM jest darmowy](https://forums.developer.nvidia.com/t/is-nim-free/369368) · [Forum NVIDIA: nowe modele mają timeout](https://forums.developer.nvidia.com/t/all-new-model-are-timeout/368931) · [Standard Compute: streszczenie regulaminu NVIDII](https://standardcompute.com/providers/nvidia) · [OpenRouter endpoints API](https://openrouter.ai/api/v1/models) · [Ranking AA](https://artificialanalysis.ai/leaderboards/models) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4)

---

## 11. Vercel AI Gateway

**Typ:** darmowy pakiet (USD 5 kredytu co 30 dni) i pay-as-you-go · **Najlepsze modele:** `zai/glm-5.3-flash` (AA 42) w ramach darmowego kredytu; płatne `xiaomi/mimo-v2.6-pro` (AA 46), `deepseek/deepseek-v4.1-flash` (AA 39) ·
**Wynik: 77** (Q26 C18 L7 A17 R9) · **Dane:** trenowanie na promptach: nieznane dla poszczególnych dostawców, Vercel zakłada trenowanie, o ile nie ma umowy; flaga `no_training` dla każdego modelu w katalogu; regiony per model (DeepSeek `us`, Gemini `eu`/`us`)

> Router Vercela przekazuje ceny katalogowe dostawców bez marży i daje każdemu zespołowi USD 5 miesięcznie, co przy
> GLM-5.3-Flash daje około 10M tokenów wyjściowych: mała, ale odnawialna darmowa pula z API zarówno OpenAI, jak i Anthropic.

**Co dostajesz.** Jeden klucz do 463 modeli (aktualny katalog, 13.10.2026). Darmowy pakiet daje **USD 5 kredytu co 30 dni na
zespół Vercel**, liczone od pierwszego żądania, do wykorzystania tylko na podzbiorze modeli „free-tier-eligible” z niższymi,
nieopublikowanymi limitami żądań per model. **Zakup jakichkolwiek kredytów przenosi cię do płatnego pakietu i miesięczny darmowy kredyt znika na zawsze.** Płatny
pakiet: bez marży, bez opłaty platformowej od tokenów, bez limitów żądań na bramce.

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `zai/glm-5.3-flash` | 42 | 1M | 131k | tak (model) | w darmowym pakiecie; USD 0,15 / 0,50, cache 0,03 |
| `alibaba/qwen3.8-flash-next` | 40 | 262k (natywnie) | nie podano | nie podano | w darmowym pakiecie; może nie być tym samym modelem co `alibaba/qwen3.8-flash` (USD 0,15 / 0,47) |
| `xiaomi/mimo-v2.6-pro` | 46 | 1M (natywnie) | nie podano | nie podano | tylko płatny; USD 0,435 / 0,87 |
| `deepseek/deepseek-v4.1-flash` | 39 | 1M (natywnie) | **32 768** | tak (model) | tylko płatny; USD 0,30 / 1,20; wyjście ograniczone znacznie poniżej 384k modelu |
| `deepseek/deepseek-v4-flash-0731` | 34 | 1M (natywnie) | nie podano | tak (model) | tylko płatny; USD 0,076 / 0,153, cache 0,014; mój lokalny model, hostowany |

Pozostałe modele z darmowego pakietu (lista zweryfikowana przez stronę trzecią 02.09.2026) są poniżej mojej poprzeczki AA 34:
`minimax/minimax-m3` (29), `moonshotai/kimi-k2.7-code` (26), `google/gemma-4-31b-it` (15), `openai/gpt-oss-120b` (12),
plus `gpt-5.4-mini`, `gemini-2.5-flash`, `nemotron-3-super`, `llama-4-maverick`, `grok-4.6`, `deepseek-v3.2-thinking`.

**Limity i ceny.** Stan na 13.10.2026:
- Darmowo: **USD 5 na 30 dni**. Na GLM-5.3-Flash to **około 10M tokenów wyjściowych** (moje wyliczenie, bez wejścia).
- Limity żądań darmowego pakietu są **celowo nieopublikowane**: „Limity mogą się zmieniać, więc ta strona opisuje zachowanie, a nie
  stałe liczby” (dokumentacja, 08.09.2026).
- Trasy z zerową ceną, które nie zużywają USD 5: `poolside/laguna-s-2.1-free` (kontekst 256k, wyjście 32k,
  **wycofywany 31.10.2026**), `stealth/glyph-cluster` (Pro/Enterprise plus kupione kredyty) oraz
  `inclusionai/ling-3.1-flash-free` (AA 41, wymieniony przez stronę trzecią 13.10.2026, ale nieobecny w publicznym katalogu,
  który pokazuje tylko płatny `inclusionai/ling-3.1-flash` za USD 0,30 / 0,90).
- Ceny płatne to ceny katalogowe dostawców (za 1M, wejście / wyjście): `mimo-v2.6-flash` (AA 38) 0,14 / 0,28,
  `alibaba/qwen3.8-flash` 0,15 / 0,47, `mistral/mistral-large-4` (AA 38) 0,68 / 2,09, `zai/glm-5.3` (AA 45) 1,40 / 4,40
  (poza budżetem).
- Zero data retention: per żądanie za darmo tylko na Pro/Enterprise; ZDR dla całego zespołu USD 0,10 za 1 tys. żądań.

**Jak uzyskać dostęp.**
1. Załóż konto Vercel i zespół; darmowy kredyt należy do zespołu.
2. **Licz się z koniecznością podpięcia karty.** Wątek społeczności (09.07.2026) pokazuje `403 customer_verification_required`
   („AI Gateway requires a valid credit card on file”); niektóre katalogi (sierpień–wrzesień 2026) mówią, że karta nie jest potrzebna. Źródła są sprzeczne.
3. Utwórz klucz API AI Gateway i wyeksportuj go jako `AI_GATEWAY_API_KEY`.
4. **Nie kupuj kredytów w tym zespole**, jeśli chcesz zachować miesięczne USD 5. Nie znalazłem ograniczeń specyficznych dla Polski.

**Przydatność dla agentów.**
- **Zgodny z OpenAI**: `https://ai-gateway.vercel.sh/v1/chat/completions`. Także OpenResponses.
- **Anthropic Messages**: ustaw `ANTHROPIC_BASE_URL=https://ai-gateway.vercel.sh` i `ANTHROPIC_AUTH_TOKEN`, a
  harness w stylu Claude uruchomi GLM-5.3-Flash bez proxy.
- Katalog udostępnia `zdr`, `no_training` (`all`/`some`/`none`) i `regions` dla każdego modelu: filtruj po nich w kodzie.
- Treść 429: `{"error":{"message":"Rate limit exceeded","type":"rate_limit_exceeded"}}`; respektuj `retry-after`. Wyczerpanie
  budżetu zwraca **402** `quota_for_entity_exceeded`.
- BYOK nie ma opłaty, ale jest dostępny tylko w płatnym pakiecie, a **nieudane wywołanie BYOK przełącza się na poświadczenia Vercela i jest rozliczane**.
- Pilnuj limitów wyjścia per trasa: V4.1-Flash zatrzymuje się tu na 32 768 tokenach.

**Niezawodność.**
- W moich źródłach brak danych o dostępności czy statusie samej bramki.
- Katalog zawiera daty `deprecated_at` (darmowy Laguna S 2.1 kończy się 31.10.2026), więc rotację widać z wyprzedzeniem.
- Ryzyko regulaminowe: limity darmowego pakietu wprost „mogą się zmieniać”, a darmowy kredyt to drzwi jednokierunkowe, gdy tylko zapłacisz.

**Ograniczenia.**
- **USD 5 miesięcznie to mało**: jeden pracowity dzień równoległej pętli agentowej potrafi to spalić.
- Limity żądań darmowego pakietu są nieznane, więc planuj na 429 i drugą trasę.
- **Pierwszy zakup trwale kończy darmowy pakiet**; karta i tak jest prawdopodobnie wymagana.
- Domyślne stanowisko w sprawie danych to „zakładaj, że trenują”: sprawdzaj `no_training` per model.
- Mocne tanie modele, jak MiMo-V2.6-Pro, są tylko płatne; lista darmowych jest głównie poniżej mojej poprzeczki.

**Gdzie pasuje w moim stosie.**
- **Miesięczna darmowa pula dla sub-agentów GLM-5.3-Flash** (workery intensywnie używające narzędzi, ekstrakcja), gdy lokalne sloty są zajęte.
- **Środowisko testowe zgodne z Anthropic**: kieruję harness zorientowany na Claude ([../harnessy-agentowe/README.md](../harnessy-agentowe/README.md))
  na tanie modele bez pisania proxy.
- Jeśli kiedyś tu zapłacę, użyję go jako routera bez marży i bez limitów bramki, ale wtedy darmowa pula przepada; przy płatnym
  wolumenie najpierw porównałbym z OpenRouter lub DeepInfra.
- Dane klientów trzymam lokalnie; ta trasa domyślnie wysyła prompty do dostawców hostowanych w USA.

**Sprawdź sam.**
```bash
curl -s https://ai-gateway.vercel.sh/v1/models | jq -r '.data[]|select(.pricing.output=="0")|.id'
curl -s https://ai-gateway.vercel.sh/v1/chat/completions -H "Authorization: Bearer $AI_GATEWAY_API_KEY" -H 'Content-Type: application/json' \
 -d '{"model":"zai/glm-5.3-flash","messages":[{"role":"user","content":"cześć"}]}'
```

**Źródła:** [Vercel AI Gateway: cennik](https://vercel.com/docs/ai-gateway/pricing) · [Vercel AI Gateway: limity żądań](https://vercel.com/docs/ai-gateway/rate-limits) · [Vercel: aktualny katalog modeli](https://ai-gateway.vercel.sh/v1/models) · [Vercel Anthropic Messages API](https://vercel.com/docs/ai-gateway/sdks-and-apis/anthropic-messages-api) · [Społeczność Vercel: weryfikacja karty](https://community.vercel.com/t/ai-gateway-stuck-on-customer-verification-required-despite-valid-card-on-file/45438) · [itsfree.ai: Vercel AI Gateway](https://itsfree.ai/provider/vercel-ai-gateway/) · [awesome-free-ai-coding: Vercel](https://mvalentsev.github.io/awesome-free-ai-coding/providers/vercel-ai-gateway/) · [agentjournal.dev: darmowe kredyty Vercel](https://agentjournal.dev/blog/vercel-ai-gateway-free/) · [Ranking AA](https://artificialanalysis.ai/leaderboards/models)

---

## 12. Kilo Gateway

**Typ:** darmowa promocja (bez konta) oraz pay-as-you-go · **Najlepsze modele:** `stepfun/step-5-preview-free` (AA 44), `inclusionai/ling-3.1-flash` (AA 41) ·
**Wynik: 75** (Q28 C18 L9 A15 R5) · **Dane:** trenuje na promptach: **tak** (Kilo oznacza każdy darmowy model jako `mayTrainOnYourPrompts: true`); lokalizacja hostingu nie jest podana

> Gateway stojący za Kilo Code serwuje za darmo Step 5 Preview (AA 44, gdzie indziej USD 2,70 za wyjście), z narzędziami i
> kontekstem 1M, i odpowiada bez klucza i konta: na 13.10.2026 najszybszy sposób, by wypróbować model o dziesięć punktów powyżej mojej poprzeczki.

**Co dostajesz.** Gateway zgodny z OpenAI z katalogiem w stylu OpenRouter liczącym **393 modele** (na żywo, 13.10.2026) oraz
darmowymi promocjami dostępnymi tylko w Kilo. **Darmowe modele odpowiadają bez klucza i konta**, z limitem **200 żądań na godzinę na IP**
(dokumentacja Kilo). Płatne modele wymagają konta i kredytów; obsługiwany jest BYOK. Według dokumentacji Kilo firmę Kilo przejęła Anaconda.

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `stepfun/step-5-preview-free` | 44 | 1M | 64k | tak | reasoning low / medium / high; darmowy wyłącznie w Kilo, OpenRouter pobiera USD 1,00 / 2,70 |
| `inclusionai/ling-3.1-flash` | 41 | nie podano (262k w innych routerach) | nie podano (gdzie indziej 32k) | nie podano | tu darmowy; wydany 1–2.10.2026; brak jeszcze niezależnych benchmarków agentowych |

Step 5 Preview: 600B łącznie / 27B aktywnych, wejście obrazów, serwowany przez jednego hosta (StepFun, FP8). Vals Terminal-Bench 4.0
**31,8** *(pomiar zewnętrzny)* wobec mojej poprzeczki 18,7; Terminal-Bench 2.1 od dostawcy 85,0 *(deklaracja dostawcy)*. Otwarte
wagi obiecano na 15.10.2026.

Reszta darmowej listy jest poniżej mojej poprzeczki (AA 34) lub bez oceny: `nvidia/nemotron-3-ultra-550b-a55b:free` (AA 23),
`thinkingmachines/inkling-small:free` (AA 26), `nvidia/nemotron-3-super-120b-a12b:free` (AA 13), `cohere/north-mini-code:free`
(AA 10) oraz nieocenione `stealth/glyph-cluster`, `dots-studio/dots-3-note-preview:free`, `poolside/laguna-s-2.1:free`.

**Limity i ceny.** Stan na 13.10.2026:
- Darmowe modele: USD 0. Ruch anonimowy: **200 żądań na godzinę na IP**. Brak opublikowanego darmowego limitu na konto.
- To średnio około 3 żądań na minutę w skali godziny: wystarczy na jedną pętlę agenta, nie na cztery równoległe.
- Płatne modele: konto plus kredyty; katalog odzwierciedla OpenRouter. Dla Step 5 Preview po zakończeniu promocji cena
  referencyjna to USD 1,00 / 2,70 za 1M tokenów (wejście / wyjście), cache 0,05, w OpenRouter.
- Darmowa trasa Step 5 to **promocja ograniczona czasowo** bez opublikowanej daty końca.

**Jak uzyskać dostęp.**
1. Do darmowych modeli: nic. Wysyłaj żądania do gatewaya bez klucza.
2. Do płatnych modeli lub BYOK: załóż konto Kilo, dodaj kredyty i użyj klucza z konta.
3. Polska: nie znalazłem ograniczeń regionalnych. Współdzielony adres IP lub NAT (biuro, runner CI) dzieli te 200 na godzinę.

**Przydatność dla agentów.**
- Bazowy URL **zgodny z OpenAI** `https://api.kilo.ai/api/gateway` (czat pod `/chat/completions`). W moich źródłach brak endpointu
  zgodnego z Anthropic.
- Darmowy Step 5 Preview ma **narzędzia, kontekst 1M, 64k wyjścia i pokrętło effort**: to prawdziwy model agentowy, nie zabawka.
- **Nie używaj `kilo-auto/free`** (kontekst 256k, 32k wyjścia) w pętlach agentów: rotuje między dots-3-note, ling-3.1-flash,
  nemotron-3-ultra, laguna-s-2.1 i glyph-cluster, więc zachowanie wywołań narzędzi zmienia się z żądania na żądanie.
- Wiele identyfikatorów `:free` to **proxowane darmowe endpointy OpenRouter**, więc dziedziczą rotację OpenRouter i błędy 429 z upstreamu.
- Limit na IP oznacza, że wszystkie subagenty na jednej maszynie dzielą te same 200 żądań na godzinę.

**Niezawodność.**
- W moich źródłach brak strony statusu i danych o dostępności samego Kilo.
- Rotacja promocji: darmowe modele w OpenRouter, które Kilo proxuje, żyją **średnio (mediana) około 75 dni** *(pomiar zewnętrzny,
  TrueFoundry, październik 2026)*; darmowa lista OpenRouter skurczyła się z 24 do 16 modeli między 21.09 a 13.10.2026.
- Host NVIDIA w upstreamie za `nemotron-3-ultra:free` miał 13.10.2026 w OpenRouter 77,4% dostępności dobowej.
- Step 5 to preview na jednym hoście: spodziewaj się zmian, gdy pojawią się wagi.

**Ograniczenia.**
- **Wszystko, co darmowe, może być użyte do treningu**: „Auto Free may route your requests to providers that log prompts and outputs
  and use them to improve their services.” Endpointy NVIDIA dodają „Do not submit personal or confidential data”.
- Najlepsza trasa to promocja; może się skończyć w dowolnym tygodniu.
- 200 żądań na godzinę na IP to cały budżet, dzielony przez każdy proces za tym IP.
- Brak konta oznacza brak panelu zużycia i brak sposobu na podniesienie limitu poza płaceniem.
- Ling 3.1 Flash jest niesprawdzony: jeden host, brak niezależnych benchmarków agentowych, wagi niewydane.

**Gdzie pasuje w moim stosie.**
- **Próby bez tarcia**: kieruję harness na darmowy Step 5 Preview, żeby sprawdzić, czy model AA 44 pokonuje mój lokalny
  V4-Flash-0731 (AA 34) na moich własnych zadaniach agentowych, zanim za niego zapłacę.
- Darmowy **subagent planisty lub recenzenta** do pracy open source lub demo, gdzie trening na promptach nie ma znaczenia.
- Nie do produkcji ani zadań harmonogramowanych: gdy promocja się skończy, przełączam się na płatny Step 5 (USD 2,70 za wyjście) lub na GLM-5.3-Flash
  (AA 42, USD 0,50 za wyjście) u płatnego hosta, a lokalny rig zostawiam do wszystkiego z danymi klientów.
- Podłącz go jako pierwszy skok z płatnym fallbackiem, jak w [../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md](../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md).

**Sprawdź sam.**
```bash
curl -s https://api.kilo.ai/api/gateway/models | jq -r '.data[]|select(.isFree==true)|"\(.id) train=\(.mayTrainOnYourPrompts)"'
curl -s https://api.kilo.ai/api/gateway/chat/completions -H 'Content-Type: application/json' \
 -d '{"model":"stepfun/step-5-preview-free","messages":[{"role":"user","content":"hi"}]}'
```

**Źródła:** [Katalog modeli Kilo na żywo](https://api.kilo.ai/api/gateway/models) · [Dokumentacja Kilo Gateway](https://kilo.ai/docs/gateway) · [Kilo: modele i dostawcy](https://kilo.ai/docs/gateway/models-and-providers) · [Katalog OpenRouter na żywo](https://openrouter.ai/api/v1/models) · [TrueFoundry: darmowe modele OpenRouter](https://www.truefoundry.com/blog/openrouter-free-models-whats-actually-free-and-what-it-costs-you) · [Tracker openrouter-free-models](https://github.com/cyclez2000/openrouter-free-models/issues/82) · [Ranking AA](https://artificialanalysis.ai/leaderboards/models) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [OrcaRouter: otwarte wagi Step 5](https://www.orcarouter.ai/blog/step-5-preview-open-weights)

---

## 13. Ollama Cloud

**Typ:** plan ryczałtowy (Pro USD 20 miesięcznie zawiera USD 60 kredytów) · **Najlepsze modele:** `glm-5.3` (AA 45), `kimi-k3` (AA 44), `glm-5.3-flash` (AA 42), `deepseek-v4.1-flash` (AA 39) ·
**Wynik: 74** (Q29 C15 L8 A13 R9) · **Dane:** trenuje na promptach: **nie** *(deklaracja dostawcy: „never logged or trained on”)*; hosting głównie w USA u dostawców chmury NVIDIA z zerową retencją danych, możliwy routing do UE

> Plan chmurowy Ollamy daje trzy dolary kredytu na modele za każdego dolara subskrypcji, co wciąga GLM-5.3 (AA 45)
> i Kimi K3 (AA 44) do mojego przedziału cenowego, bez ograniczenia do narzędzi do kodowania.

**Co dostajesz.** Subskrypcję zamienianą na kredyty zużycia, rozliczane po stawkach za token odzwierciedlających cenniki
producentów. Model cenowy zmienił się z limitów zużycia na kredyty mniej więcej między 27.08 a 1.09.2026. **Pro: USD 20 miesięcznie (lub 200
rocznie) kupuje USD 60 kredytów miesięcznie.** W przeciwieństwie do GLM Coding Plan czy Kimi Code **użycie API nie jest ograniczone do narzędzi
do kodowania**, więc mogę go wywoływać z własnych agentów.

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `glm-5.3` | 45 | 1M (natywnie) | nie podano | tak (model) | cennik USD 1,40 / 4,40; efektywnie na Pro około 0,47 / 1,47 |
| `kimi-k3` | 44 | 1M (natywnie) | nie podano | tak (model) | cennik USD 3 / 15; efektywnie na Pro około 1 / 5; najmocniejszy otwarty model w użyciu narzędzi |
| `glm-5.3-flash` | 42 | 1M (natywnie) | nie podano | tak (model) | cennik USD 0,15 / 0,50 |
| `deepseek-v4.1-flash` | 39 | 1M (natywnie) | nie podano | tak (model) | cennik USD 0,30 / 1,20, poza szczytem 0,15 / 0,60 |
| `mistral-large-4` | 38 | 1M wg dostawcy, 524k zmierzone | nie podano | nie podano | cennik USD 0,68 / 2,09 |

Limity kontekstu i wyjścia po stronie Ollamy nie są opublikowane na stronach, które czytałem, a **kwantyzacja modeli chmurowych nie
jest ujawniona**. Poniżej mojej poprzeczki: `minimax-m3` (AA 29), `kimi-k2.6` (27), `kimi-k2.7-code` (26), `nemotron-3-ultra` (23),
`gpt-oss:120b` (12).

**Limity i ceny.** Stan na 13.10.2026:

| Plan | Cena | Kredyty w cenie | Współbieżność |
|---|---|---|---|
| Free | USD 0 | kredyty startowe, tylko modele startowe, odnawiane co miesiąc, bez przenoszenia | 1 (kolejkowane, potem odrzucane) |
| Pro | USD 20 miesięcznie lub 200 rocznie | USD 60 miesięcznie | 3 |
| Max | USD 100 miesięcznie | USD 300 miesięcznie | 10 |
| Team | USD 500 miesięcznie | USD 1000 współdzielone | 10 |

- Kupione kredyty wygasają po 1 roku.
- **Poza szczytem** to czas poza 12:00–18:00 UTC w dni robocze oraz cały weekend; poza szczytem jest taniej, dla DeepSeek za pół ceny.
  W Polsce to okno szczytu przypada na 14:00–20:00 w czasie letnim i 13:00–19:00 w czasie zimowym.
- Inne stawki (za 1M, wejście / wyjście): `deepseek-v4-pro` 1,32 / 3,96 (poza szczytem 0,66 / 1,98), `minimax-m3` 0,60 / 2,40,
  `kimi-k2.6` i `kimi-k2.7-code` 0,95 / 4, `gpt-oss:120b` 0,15 / 0,60, `nemotron-3-ultra` 0,10 / 3.
- Przybliżony miesięczny wolumen na Pro, tylko wyjście (moje wyliczenia): USD 60 to **około 13,6M tokenów wyjściowych GLM-5.3**, około 4M
  Kimi K3, około 100M V4.1-Flash poza szczytem lub około 120M GLM-5.3-Flash.

**Jak uzyskać dostęp.**
1. Załóż konto na ollama.com.
2. Wykup Pro (lub Max), aby dostać kredyty; plan darmowy obejmuje tylko modele startowe.
3. Utwórz klucz API na koncie ollama.com i wyeksportuj go jako `OLLAMA_API_KEY` (zob. docs.ollama.com/cloud).
4. W moich źródłach nie znalazłem ograniczeń specyficznych dla Polski.

**Przydatność dla agentów.**
- Natywne API pod `https://ollama.com/api`; `curl https://ollama.com/api/tags` wyświetla modele chmurowe.
- Dokumentacja mówi, że klienci OpenAI i Anthropic są obsługiwani **w ograniczonym zakresie (podzbiór)**. Bazowy URL w stylu OpenAI `https://ollama.com/v1` jest
  **założony, ale niezweryfikowany**: przetestuj na nim narzędzia i ustrukturyzowane wyjście, zanim zaczniesz na nim polegać.
- **Współbieżność 3 na Pro to wiążący limit**: mniej równoległych workerów niż moje 4 lokalne sloty. Max podnosi ją do 10.
- Kimi K3 wymaga odsyłania w każdej turze pełnej wiadomości asystenta, łącznie z `reasoning_content` i `tool_calls`.
- Brak opublikowanego zachowania przy 429; w planie darmowym nadmiarowe żądania trafiają do kolejki, a potem są odrzucane.
- W moich źródłach brak dowodów na dokładność endpointów Ollamy, a kwantyzacja jest nieznana.

**Niezawodność.**
- W moich źródłach brak danych o dostępności i statusie.
- **Warunki niedawno się zmieniły**: przejście z limitów zużycia na kredyty nastąpiło pod koniec sierpnia 2026, więc mnożnik kredytów
  jest młody i może się zmienić.
- Stawki modeli odzwierciedlają ceny producentów, więc zmiana cen u dostawcy (na przykład linii GLM) zmienia mój efektywny koszt.

**Ograniczenia.**
- **Płacisz USD 20 z góry**: wychodzi tanio tylko wtedy, gdy faktycznie co miesiąc przepalam większość z USD 60.
- Współbieżność 3 na Pro ogranicza agenty z rozgałęzieniem (fan-out).
- Zgodność z OpenAI to podzbiór, a ścieżka `/v1` jest niezweryfikowana; zarezerwuj czas na adapter.
- Kwantyzacja i limity kontekstu modeli chmurowych nie są ujawnione.
- W planie darmowym kredyty nie przechodzą na kolejny miesiąc; kupione kredyty wygasają po roku.

**Gdzie pasuje w moim stosie.**
- **Tani planista lub recenzent na GLM-5.3** (AA 45 przy efektywnie około USD 1,47 za wyjście) pomiędzy moim lokalnym V4-Flash-0731
  (AA 34) a Claude Opus do planowania.
- **Kimi K3 do subagentów intensywnie korzystających z narzędzi**, gdzie liczy się jego siła w użyciu narzędzi, za efektywnie około USD 5 za wyjście zamiast 15.
- Masowe zadania V4.1-Flash **planowane poza szczytem** (wieczory i weekendy w Polsce) za pół ceny.
- Deklaracja braku logowania to najlepsze podejście do danych w tej grupie, ale nadal to deklaracja dostawcy: dane klientów zostają na
  lokalnym rigu ([../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md)).

**Sprawdź sam.**
```bash
curl -s https://ollama.com/api/tags | jq -r '.models[].name'
# wywołanie czatu w natywnym API; sprawdź dokładny tag modelu w /api/tags i nagłówek autoryzacji w docs.ollama.com/cloud
curl -s https://ollama.com/api/chat -H "Authorization: Bearer $OLLAMA_API_KEY" -H 'Content-Type: application/json' \
 -d '{"model":"glm-5.3","messages":[{"role":"user","content":"hi"}],"stream":false}'
```

**Źródła:** [Cennik Ollama](https://ollama.com/pricing) · [Dokumentacja Ollama Cloud](https://docs.ollama.com/cloud) · [agentdeals.dev: Ollama Cloud](https://agentdeals.dev/vendor/ollama-cloud) · [Ranking AA](https://artificialanalysis.ai/leaderboards/models) · [AA Kimi K3](https://artificialanalysis.ai/models/kimi-k3) · [Karta modelu Kimi K3](https://huggingface.co/moonshotai/Kimi-K3) · [Specyfikacja Mistral Large 4](https://capitalandcompute.net/md/mistral-large-4-pricing-benchmarks.md)

---

## 14. Requesty

**Typ:** darmowy pakiet + pay-as-you-go · **Najlepsze modele:** `novita/ling-3.1-flash` (AA 41, darmowy); płatne GLM-5.3-Flash (AA 42),
DeepSeek V4.1 Flash (AA 39), MiMo-V2.6-Pro (AA 46) · **Wynik: 72** (Q25 C18 L6 A15 R8) · **Dane:** trenowanie na promptach: nie dla
darmowego Ling 3.1 Flash (metadane Requesty: brak retencji, brak trenowania, upstream Novita, geo global); tak dla darmowych
modeli z wersji próbnej NVIDII; router ma region UE (Frankfurt) w każdym planie

> Brytyjski router z prawdziwym darmowym pakietem bez karty, endpointem UE w darmowym planie i jedyną darmową trasą Ling 3.1 Flash
> oznaczoną jako bez trenowania, co daje model powyżej poprzeczki za adresem URL w UE za zero.

**Co dostajesz.** Stan na 13.10.2026: plan Free to „pełna platforma, na darmowych modelach”, **200 żądań dziennie, bez karty
kredytowej**. Pay-as-you-go dodaje wszystkie modele (784 trasy) z **marżą 5%** na zarządzanym użyciu, plus BYOK. Sam router działa
we Frankfurcie, jeśli używasz bazowego URL dla UE, nawet w planie Free.

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `novita/ling-3.1-flash` (darmowy) | 41 | 262k | 32k | tak, plus rozumowanie | brak flagi JSON-schema; jeden upstream (Novita) |
| GLM-5.3-Flash (zai / deepinfra / novita / fireworks / runware) | 42 | 1M natywnie | nie odczytano | zależnie od upstreamu | USD 0,15 / 0,50 |
| `melious/glm-5.3-flash` (geolokalizacja UE) | 42 | 1M natywnie | nie odczytano | zależnie od upstreamu | USD 0,12 / 0,46 |
| `deepinfra/deepseek-v4.1-flash` | 39 | 1M natywnie | nie odczytano | zależnie od upstreamu | USD 0,20 / 0,60, cache 0,006; `:flex` 0,16 / 0,48 |
| `melious/deepseek-v4-flash-0731` (geolokalizacja UE) | 34 | 1M natywnie | nie odczytano | zależnie od upstreamu | USD 0,12 / 0,29; ten sam model co na moim sprzęcie |
| MiMo-V2.6-Pro | 46 | 1M natywnie | nie odczytano | zależnie od upstreamu | USD 0,43–0,435 / 0,87 |

„1M natywnie” to własne okno modelu; nie odczytałem kontekstu per trasa w Requesty dla modeli płatnych. Ling 3.1 Flash ma
okno 1M według AA, ale na tej trasie tylko 262k / 32k.

**Limity i ceny.** Wszystko na 13.10.2026 (strona cennika Requesty i aktualny katalog):
- Darmowo: 200 żądań dziennie, **wspólne dla wszystkich darmowych modeli**; RPM nieopublikowany; bez karty.
- PAYG: cena katalogowa + 5%. Przykłady przed marżą: DeepSeek V4.1 Flash USD 0,20 / 0,60 (DeepInfra), 0,15 / 0,60 (Runware),
  0,30 / 1,20 (DeepSeek); V4 Flash 0731 USD 0,076 / 0,153 (Runware), 0,072 / 0,144 (DeepInfra `:flex`).
- Inne trasy z geolokalizacją UE: `lyceum/deepseek-v4-flash-0731` USD 0,25 / 0,30, `scaleway/deepseek-v4-flash-0731` 0,46 / 0,93
  (kontekst 256k), `sference/glm-5.3-flash` 0,20 / 0,60, `melious/deepseek-v4.1-flash` 0,23 / 1,14.
- Pozostałe darmowe modele są poniżej poprzeczki: Nemotron 3 Ultra (AA 23; warunki wersji próbnej NVIDII, 30-dniowa retencja, trenuje), Gemma 4 31B
  (AA 15; tutaj 8k wyjścia), Poolside Laguna (kontekst 32k i brak narzędzi w Requesty).

**Jak uzyskać dostęp.**
1. Zarejestruj się na requesty.ai; plan Free nie wymaga karty.
2. Utwórz klucz API w panelu i wyeksportuj go jako `REQUESTY_API_KEY`.
3. Z Polski używaj bazowego URL dla UE `https://router.eu.requesty.ai/v1`; nie obowiązuje blokada regionalna.
4. Doładuj środki tylko wtedy, gdy chcesz modeli płatnych; marża 5% dotyczy zarządzanego użycia, nie kluczy BYOK.

**Przydatność dla agentów.** Zgodny z OpenAI pod `https://router.requesty.ai/v1` (UE: `https://router.eu.requesty.ai/v1`) i
zgodny z Anthropic pod `https://router.requesty.ai/anthropic/v1/messages`. Sama nazwa modelu daje zarządzany failover;
`provider/model` przypina hosta; `policy/<name>` stosuje politykę routingu. Darmowy Ling 3.1 Flash obsługuje wywołania narzędzi i rozumowanie,
ale nie ma **flagi JSON-schema i ma limit wyjścia 32k**, więc używałbym zwykłych promptów JSON z walidatorem i trzymał wyjścia
krótkie. Ling nie ma jeszcze niezależnego benchmarku agentowego, jest bardzo rozwlekły (220M tokenów w przebiegu AA) i jest serwowany przez
jeden upstream. Nie znalazłem opublikowanego formatu 429 ani limitu współbieżności.

**Niezawodność.** Brak publicznych danych o dostępności, a katalog nie ma pól zdrowia: nieznane. Lista darmowych modeli „zmienia się, gdy
dostawcy je dodają i usuwają”. Rotację Ling 3.1 Flash widać gdzie indziej: OpenRouter wystawił go za zero 03.10.2026,
potem uczynił płatnym (USD 0,075 / 0,225), a jego darmowy wariant zniknął do 13.10.2026 *(pomiar zewnętrzny)*.

**Ograniczenia.**
- 200 żądań dziennie na wszystko, co darmowe: jeden długi przebieg agenta może zużyć połowę.
- URL dla UE sprawia, że w UE jest *router*; upstream Linga to Novita z geo „global”, więc inferencja nie odbywa się w UE.
- Maks. 32k wyjścia i brak obsługi JSON-schema na darmowej trasie Ling.
- Ling 3.1 Flash jest niesprawdzony: wydany 1–2.10.2026, wagi nieopublikowane, brak wyników Vals czy tbench.
- Brak danych o dostępności, brak opublikowanego RPM.

**Gdzie pasuje w moim stosie.**
- Darmowy sub-agent z endpointem w UE do krótkich wywołań klasyfikacji / ekstrakcji / streszczania na danych niewrażliwych, do ~200 dziennie.
- Model „drugiej opinii” w ewaluacjach (zob. `../kurs_aplikacje_agentowe/14-EWALUACJA.md`): Ling 41 vs mój lokalny 34.
- PAYG jako bramka z routingiem przez UE i failoverem na GLM-5.3-Flash lub V4 Flash 0731 po cenach Melious / Lyceum.
- Przy wolumenie zostaję lokalnie (4 sloty, bez limitu dziennego); przy ciężkich płatnych pętlach prostsze są OpenRouter lub DeepInfra.

**Sprawdź sam.**
```bash
curl -s https://router.requesty.ai/v1/models | jq -r '.data[]|select(.input_price==0 and .output_price==0)|.id'
curl -s https://router.eu.requesty.ai/v1/chat/completions -H "Authorization: Bearer $REQUESTY_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"novita/ling-3.1-flash","messages":[{"role":"user","content":"cześć"}],
       "tools":[{"type":"function","function":{"name":"f","parameters":{"type":"object","properties":{}}}}]}'
```

**Źródła:** [Requesty: cennik](https://www.requesty.ai/pricing) · [Requesty: darmowe modele](https://www.requesty.ai/models/free) ·
[Requesty: API modeli](https://router.requesty.ai/v1/models) · [Requesty: quickstart](https://docs.requesty.ai/quickstart) ·
[AA Ling 3.1 Flash](https://artificialanalysis.ai/models/ling-3-1-flash) · [OpenRouter: API modeli](https://openrouter.ai/api/v1/models) ·
[OpenRouter: tracker darmowych modeli](https://github.com/cyclez2000/openrouter-free-models/issues)

---

## 15. Scaleway Generative APIs (EU)

**Typ:** pay-as-you-go (plus jednorazowo 1M darmowych tokenów) · **Najlepsze modele:** `deepseek-v4.1-flash` (AA 39),
`deepseek-v4-flash-0731` (AA 34) · **Wynik: 72** (Q23 C12 L11 A14 R12) · **Dane:** Trenuje na promptach: nie (deklarowany brak
retencji danych, *deklaracja dostawcy*); hosting w Paryżu (fr-par), UE

> Bezserwerowe API zgodne z OpenAI od francuskiej chmury: najbardziej ugruntowana trasa z rezydencją w UE do modelu powyżej poprzeczki, z
> ujawnioną kwantyzacją i stroną statusu, za wyraźną dopłatą względem hostów z USA.

**Co dostajesz.** Stan na 13.10.2026: pierwszy **1M tokenów jest darmowy** (plus 60 minut audio), jednorazowo. Potem
pay-as-you-go w EUR. Poziom podstawowy wymaga ważnej metody płatności; poziom „Enhanced” po weryfikacji tożsamości podnosi
limity. Wszystko działa w Paryżu.

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `deepseek-v4.1-flash` | 39 | nie ustalono | nie ustalono | nie ustalono | EUR 0,60 / 1,80, cache 0,12 |
| `deepseek-v4-flash-0731` | 34 | 256k | 32k | nie ustalono | reasoning od none do max; w dokumentacji, cena nie ustalona |
| `glm-5.3` | 45 | nie ustalono | nie ustalono | nie ustalono | EUR 1,80 / 5,50: powyżej limitu 3 USD |
| `gpt-oss-120b` | 12 | 128k | 32k | nie ustalono | FP4; poniżej poprzeczki, ale 98% w AA endpoint accuracy |

Kontekst w Scaleway jest **przycięty poniżej natywnego** (256k wobec natywnego okna 1M).

**Limity i ceny.** Strona cennika, październik 2026 (EUR za 1M tokenów, wejście / wyjście): `deepseek-v4.1-flash` 0,60 / 1,80
(cache 0,12); `glm-5.3` 1,80 / 5,50; `qwen3.5-397b-a17b` 0,60 / 3,60; `mistral-medium-3.5-128b` 1,50 / 7,50;
`mistral-small-3.2-24b` 0,15 / 0,35. Batch jest 50% taniej. RPM i TPM nie są publikowane; widać je tylko w konsoli
w sekcji „Organization quotas”. Dla skali: własne API DeepSeek sprzedaje ten sam V4.1 Flash za USD 0,15 / 0,60 poza szczytem, więc rezydencja
w UE kosztuje około 3x więcej za wyjście.

**Jak uzyskać dostęp.**
1. Załóż konto Scaleway i dodaj metodę płatności: poziom podstawowy jej wymaga.
2. Opcjonalnie przejdź weryfikację tożsamości, by dostać poziom Enhanced i wyższe limity.
3. Utwórz w konsoli sekretny klucz API i wyeksportuj go jako `SCW_SECRET_KEY`.
4. Z Polski brak problemów regionalnych; usługa działa w fr-par.

**Przydatność dla agentów.** Zgodne z OpenAI pod `https://api.scaleway.ai/v1` (także `/{project_id}/v1`). Kwantyzacja jest ujawniona dla każdego
modelu w dokumentacji (fp8 / fp4 / bf16). Limit kontekstu 256k i 32k wyjścia na V4 Flash 0731 mają znaczenie dla długich pętli agentów: zaplanuj
kompakcję. Słabym punktem jest **dokładność endpointu**: AA zmierzyło GLM-5.2 w Scaleway na **75%** wzorca, przy czym
szkody skupiają się w wywołaniach narzędzi BFCL, podczas gdy gpt-oss-120b uzyskał tam 98% *(pomiar zewnętrzny, AA Endpoint Accuracy
Index, 26.09.2026)*. Brak pomiaru dla endpointów DeepSeek, więc najpierw zrób smoke test wywołań narzędzi. W moich źródłach nie znalazłem
endpointu zgodnego z Anthropic.

**Niezawodność.** Status na status.scaleway.com. Zmiany w katalogu: `devstral-2-123b` wycofano 1.07.2026, a dokumentacja modeli
na GitHubie nie nadąża za stroną cennika (dokumentacja nadal podaje GLM-5.2 z 256k / 16k wyjścia, a cennik pokazuje GLM-5.3).

**Inne trasy w UE w porównaniu.** Stan na 13.10.2026:

| Trasa | Najlepszy model w budżecie (AA) | Cena za 1M (wejście / wyjście) | Uwagi |
|---|---|---|---|
| Scaleway | V4.1 Flash (39) | EUR 0,60 / 1,80 | Paryż; deklarowany brak retencji; kwantyzacja ujawniona |
| Lyceum | GLM-5.3-Flash (42) | USD 0,20 / 0,50 | firma z Berlina, eu-north1 / Paryż; deklarowany tryb zerowej retencji; brak danych o dokładności |
| Endpoint UE Mistral | GLM-5.3 (45) | USD 1,54 / 4,84 | `api.eu.mistral.ai` za +10% do 1,40 / 4,40; NVFP4; trening wyłączony dla płatnego API, ZDR na życzenie |
| Mistral | Mistral Large 4 preview (38) | USD 0,68 / 2,09 promocja | przez około dwa tygodnie od 6.10.2026, potem 1,36 / 4,18; zmierzony kontekst 524k vs deklarowane 1M |
| OVHcloud | Qwen3.8-27B (34 przy xhigh) | EUR 0,40 / 2,70 | Gravelines; dane nie są przechowywane; gpt-oss-120b EUR 0,08 / 0,40; brak DeepSeek i GLM |
| Trasy UE w Requesty | GLM-5.3-Flash (42) | USD 0,12 / 0,46 + 5% | Melious; także `melious/deepseek-v4-flash-0731` 0,12 / 0,29, `lyceum/` 0,25 / 0,30 |

Haczyk Mistrala jest prawny, nie techniczny: **od 5.08.2026 (7.08 w UE) API jest tylko dla klientów biznesowych**;
osoby prywatne nie mogą go używać do projektów osobistych. Kredyt w planie Free jest nieokreślony od 7.10.2026, a plan
Free może trenować na danych wejściowych, chyba że zrezygnujesz (opt-out). Starsze zewnętrzne podsumowanie nadal opisuje darmowy poziom 1 mld tokenów/miesiąc
na model; nowsze źródła temu przeczą. OVHcloud pozwala też na 2 RPM na IP na model bez klucza i 400 RPM na
projekt na model z kluczem.

**Ograniczenia.**
- Około 3x cena hostów z USA za ten sam model DeepSeek; GLM-5.3 jest tu powyżej limitu.
- Kontekst przycięty do 256k; 32k wyjścia na V4 Flash 0731.
- Zmierzona degradacja wywołań narzędzi na jednym modelu (GLM-5.2, 75%); nic nie zmierzono dla DeepSeek.
- Limity widoczne tylko w konsoli.
- Darmowy 1M tokenów to próbka, nie poziom.

**Gdzie pasuje w moim stosie.**
- Płatna trasa z rezydencją w UE, gdy zadanie nie może opuścić UE, ale nie jest na tyle wrażliwe, by zostać na rigu.
- Failover dla mojego lokalnego V4 Flash 0731 (ten sam model, limit 256k), gdy rig jest zajęty lub nie działa.
- Pod kątem ceny i jakości w UE najpierw wypróbowałbym Lyceum GLM-5.3-Flash, a Scaleway zostawił jako ugruntowany fallback.
- Naprawdę wrażliwe dane klientów nadal zostają lokalnie (zob. `../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md`).

**Sprawdź sam.**
```bash
curl -s https://api.scaleway.ai/v1/models -H "Authorization: Bearer $SCW_SECRET_KEY" | jq -r '.data[].id'
curl -s https://api.scaleway.ai/v1/chat/completions -H "Authorization: Bearer $SCW_SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"deepseek-v4.1-flash","messages":[{"role":"user","content":"Pogoda w Warszawie?"}],
       "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
curl -s https://oai.endpoints.kepler.ai.cloud.ovh.net/v1/models | jq -r '.data[].id'
curl -s https://api.mistral.ai/v1/models -H "Authorization: Bearer $MISTRAL_API_KEY" | jq -r '.data[].id'
```

**Źródła:** [Cennik Scaleway](https://www.scaleway.com/en/pricing/model-as-a-service/) ·
[Obsługiwane modele Scaleway](https://raw.githubusercontent.com/scaleway/docs-content/main/pages/generative-apis/reference-content/supported-models.mdx) ·
[Limity Scaleway](https://raw.githubusercontent.com/scaleway/docs-content/main/pages/generative-apis/reference-content/rate-limits.mdx) ·
[Rejestracja Scaleway](https://www.scaleway.com/en/generative-apis-signup/) ·
[AA: dostawcy GLM-5.2](https://artificialanalysis.ai/models/glm-5-2/providers) ·
[AA: dostawcy gpt-oss-120b](https://artificialanalysis.ai/models/gpt-oss-120b/providers) ·
[Lista modeli Lyceum](https://lyceum.technology/magazine/eu-hosted-llm-api-lyceum-model-roster-prices/) ·
[Mistral GLM-5.3](https://docs.mistral.ai/models/zai-glm-5-3) ·
[Endpointy regionalne Mistral](https://www.digitalapplied.com/blog/mistral-hosts-rival-open-models-regional-endpoints-2026) ·
[Changelog Mistral](https://docs.mistral.ai/resources/changelogs) ·
[agentdeals Mistral](https://agentdeals.dev/mistral-api-pricing-2026) ·
[Specyfikacja Mistral Large 4](https://capitalandcompute.net/md/mistral-large-4-pricing-benchmarks.md) ·
[Katalog OVHcloud](https://www.ovhcloud.com/en/public-cloud/ai-endpoints/catalog/) ·
[Możliwości OVHcloud](https://docs.ovhcloud.com/en/guides/public-cloud/ai-machine-learning/ai-endpoints-capabilities) ·
[API modeli Requesty](https://router.requesty.ai/v1/models) ·
[Cennik DeepSeek](https://api-docs.deepseek.com/quick_start/pricing)

---

## 16. StepFun API and Step Plan

**Typ:** pay-as-you-go + plan ryczałtowy · **Najlepsze modele:** `step-5-preview` (AA 44, leaderboard) · **Wynik: 71**
(Q28 C11 L12 A13 R7) · **Dane:** trenuje na promptach: nieznane dla API producenta; region hostingu nieudokumentowany

> Rodzimy dom Step 5 Preview, jednego z najmocniejszych modeli poniżej limitu 3 USD za wyjście, sprzedawanego za token albo jako
> tani plan miesięczny, który deklaruje działanie z twoim własnym stosem.

**Co dostajesz.** Stan na 13.10.2026: międzynarodowe pay-as-you-go na platform.stepfun.ai, z progami limitów rosnącymi wraz z
łączną kwotą doładowań, oraz **Step Plan**, stała miesięczna subskrypcja rozliczana w kredytach. Step 5 Preview wydano
20.09.2026 jako model dostępny tylko przez API; **otwarte wagi zaplanowano na 15.10.2026** *(deklaracja producenta)*.

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `step-5-preview` (StepFun bezpośrednio) | 44 | 1M | 64k | nie ustalono | MoE 600B / 27B; `reasoning_effort` low / medium / high; wejście obrazu i wideo |
| `stepfun/step-5-preview` (OpenRouter) | 44 | 1M | 64k | nie ustalono | jeden host (StepFun, FP8); 1,00 / 2,70 USD, cache 0,05 |
| `stepfun/step-5-preview-free` (Kilo Gateway) | 44 | 1M | 64k | tak | darmowa promocja, bez konta; Kilo oznacza go jako „may train” |
| `step-5-preview-free` (OpenCode Zen) | 44 | nie ustalono | nie ustalono | nie ustalono | darmowa promocja; dostawca bez retencji, bez trenowania |

Liczby Step 5: Vals Terminal-Bench 4.0 **31,82** *(pomiar strony trzeciej)* wobec 18,69 dla mojego lokalnego V4 Flash 0731;
TB2.1 producenta 85,0, GPQA 93,5, BrowseComp 88,7 *(deklaracja producenta)*. `step-3.7-flash` i `step-3.5-flash` nie mają wyniku AA.

**Limity i ceny.** Pay-as-you-go u producenta, USD za 1M tokenów (wejście / cache / wyjście), 13.10.2026:
`step-5-preview` 1,00 / 0,10 / 2,70 (źródła zewnętrzne i OpenRouter pokazują cache po 0,05); `step-3.7-flash`
0,20 / 0,04 / 1,15; `step-3.5-flash` 0,10 / 0,02 / 0,30. **Wyjście obejmuje tokeny rozumowania.** Ceny CN dla Step 5:
7 / 0,70 / 20 CNY.

| Próg | Łączne doładowania | Współbieżność | RPM | TPM |
|---|---|---|---|---|
| V0 | poniżej 15 USD | 5 | 100 | 500K |
| V1 | 15–69 USD | 20 | 400 | 2M |
| V2 | 70–299 USD | 30 | 600 | 3M |
| V3 | 300–1499 USD | 40 | 800 | 4M |
| V4 | 1500+ USD | 130 | 2600 | 13M |

Step Plan (ceny ze źródeł zewnętrznych; oficjalna strona pokazuje tylko kredyty): Mini 6,99 USD (400M kredytów/miesiąc), Plus 9,99
(1600M), Pro 29 (8000M), Max 99 (40 000M). Modele: Step 5 Preview, 3.7 Flash, 3.5 Flash. **Nie znalazłem przelicznika kredytów
na tokeny ani informacji o ewentualnych oknach 5-godzinnych.**

**Jak uzyskać dostęp.**
1. Zarejestruj się na platform.stepfun.ai (platforma międzynarodowa; platform.stepfun.com to chińska).
2. Doładuj konto; 15 USD przenosi cię z V0 (5 współbieżnych) do V1 (20 współbieżnych).
3. Utwórz klucz API w konsoli i wyeksportuj go jako `STEPFUN_API_KEY`.
4. W przypadku planu wykup subskrypcję na stronie Step Plan i sprawdź, z którego salda pobierane są twoje wywołania.
W moich źródłach nie znalazłem uwag regionalnych dotyczących Polski.

**Przydatność dla agentów.** Katalog Kilo wymienia Step 5 z narzędziami i rozumowaniem low / medium / high; kontekst 1M i wyjście 64k
wystarczają do długich pętli, ale zanim zaczniesz na tym polegać, uruchom poniższy test wywołania narzędzia na płatnej trasie. Post premierowy mówi, że plan *„works with Cursor, Windsurf, Cline, and your own stack. Zero lock-in”*, więc
**wygląda na to, że dopuszcza własnych agentów** *(deklaracja producenta, sprawdź regulamin)*. Nie ustaliłem bezpośredniego bazowego URL; najprostsza
udokumentowana ścieżka to OpenRouter (`stepfun/step-5-preview`, zgodny z OpenAI, ten sam host StepFun i ta sama cena). Przy 5
współbieżnych żądaniach w V0 równoległość odpowiada 4 slotom mojego lokalnego sprzętu; V1 daje 20.

**Niezawodność.** Wszędzie model serwuje jeden host (StepFun, FP8), więc nie ma dostawcy zapasowego. To wersja preview:
ID, ceny i limity mogą się zmienić przy GA. Nie ma jeszcze danych o dostępności ani zewnętrznej weryfikacji trafności. Publikacja wag
15.10.2026 może dodać zewnętrznych hostów, ale nie jest to potwierdzone.

**Ograniczenia.**
- 2,70 USD za wyjście jest blisko limitu 3 USD; rozwlekłe rozumowanie jest rozliczane jako wyjście.
- Warunki dotyczące danych dla API producenta są nieznane.
- Kredyty planu i saldo pay-as-you-go są rozdzielne, więc wywołanie może zostać obciążone z niewłaściwego.
- Wartości Step Plan nie da się ocenić, dopóki przelicznik kredytów nie zostanie opublikowany.
- Model w wersji preview, jeden host.

**Gdzie pasuje w moim stosie.**
- Najpierw darmowe eksperymenty: wariant OpenCode Zen (bez retencji) albo Kilo (bez konta) nic nie kosztują.
- Płatny Step 5 jako sub-agent do trudnych zadań terminalowych, gdzie TB4.0 31,8 wyraźnie bije mój lokalny model.
- Cenowo GLM-5.3-Flash (TB4.0 37,4 za 0,50 USD za wyjście) jest lepszym workerem terminalowym; Step 5 to druga opinia.
- Step Plan staje się interesujący, jeśli 400M kredytów okaże się oznaczać dużo tokenów Step 5.

**Sprawdź sam.**
```bash
curl -s https://openrouter.ai/api/v1/models/stepfun/step-5-preview/endpoints \
  | jq '.data.endpoints[]|{provider_name,quantization,pricing,context_length}'
curl -s https://api.kilo.ai/api/gateway/chat/completions -H 'Content-Type: application/json' \
  -d '{"model":"stepfun/step-5-preview-free","messages":[{"role":"user","content":"hi"}]}'
curl -s https://openrouter.ai/api/v1/chat/completions -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"stepfun/step-5-preview","messages":[{"role":"user","content":"Jaka jest pogoda w Warszawie?"}],
       "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
```

**Źródła:** [Cennik StepFun (intl)](https://platform.stepfun.ai/docs/en/guides/pricing/details) ·
[Cennik StepFun (CN)](https://platform.stepfun.com/docs/zh/guides/pricing/details) ·
[Step Plan](https://platform.stepfun.ai/step-plan) · [Post premierowy StepFun](https://x.com/StepFun_ai/status/2035815197584023835) ·
[eesel Step 5](https://www.eesel.ai/blog/stepfun-step-5) · [Ceny Step Plan](https://omidsaffari.com/de/blog/step-5-preview-preise) ·
[Otwarte wagi Step 5](https://www.orcarouter.ai/blog/step-5-preview-open-weights) ·
[Leaderboard AA](https://artificialanalysis.ai/leaderboards/models) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) ·
[OpenRouter – API modeli](https://openrouter.ai/api/v1/models) · [Kilo – API modeli](https://api.kilo.ai/api/gateway/models) ·
[OpenCode Zen – modele](https://opencode.ai/zen/v1/models)

---

## 17. OpenCode Zen

**Typ:** darmowa promocja + pay-as-you-go · **Najlepsze modele:** `muse-spark-1.3-contributor-free` (AA 45 przy xhigh, trenuje),
`step-5-preview-free` (AA 44), `ling-3.1-flash-free` (AA 41), `mimo-v2.6-flash-free` (AA 38) · **Wynik: 70**
(Q30 C18 L6 A12 R4) · **Dane:** Trenowanie na promptach: zależnie od modelu, od nie (Step 5: zerowa retencja, bez trenowania) po tak
(Muse Spark Contributor trenuje modele Meta); hosting w USA i UE

> Kuratorowana bramka zespołu OpenCode z najmocniejszym darmowym zestawem modeli w tym przeglądzie, w tym Step 5 Preview z zerową
> retencją, ale to promocja zmieniająca się co tydzień, z nieopublikowanymi limitami, faworyzująca własnego klienta.

**Co dostajesz.** Stan na 13.10.2026: konto i klucz API z konsoli opencode.ai. Darmowe modele kosztują 0 USD „przez
ograniczony czas”, bez dat zakończenia. Płatne modele wymagają kredytu i są rozliczane za token. Modele są „hostowane w USA
i UE” *(deklaracja dostawcy)*; nie podano, który region obsługuje dane zapytanie.

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `muse-spark-1.3-contributor-free` | 45 (xhigh) | 1M | nie odnotowano | nie odnotowano | Meta trenuje na promptach i odpowiedziach; tylko Responses API |
| `step-5-preview-free` | 44 | 1M natywnie | nie odnotowano | nie odnotowano | zerowa retencja u dostawcy, bez trenowania |
| `ling-3.1-flash-free` | 41 | 1M w AA | nie odnotowano | nie odnotowano | dane używane do ulepszania modelu |
| `mimo-v2.6-flash-free` | 38 | 1M natywnie | nie odnotowano | nie odnotowano | dane wykorzystywane; TB4.0 24,2 (Vals) |
| GLM 5.3 Flash (płatny) | 42 | 1M natywnie | nie odnotowano | nie odnotowano | 0,15 / 0,50 USD, cache 0,03 |

**Zastrzeżenia dotyczące Muse Spark.** AA 48 to Muse Spark 1.3 przy maksymalnym wysiłku; dokumentacja Meta mówi, że **Contributor ID nie może działać na max**,
więc jego pułap to xhigh = AA 45 *(AA, 13.10.2026)*. Vals podaje „Muse Spark 1.3” z TB2.1 72,3 / TB4.0 **10,6** i „Muse Spark 1.3 Max” z 79,0 /
24,8 *(pomiar zewnętrzny)*. Mój lokalny V4 Flash 0731 uzyskuje 18,7 w TB4.0, więc standardowy 1.3 może być słabszy od mojego sprzętu lokalnego
w trudnych zadaniach terminalowych. Własny poziom Contributor od Meta kosztuje 0,10 / 0,20 USD, z limitem 150 RPM / 3M TPM na zespół na dzień 13.10.2026 (starsze blogi podają 60 RPM).

**Limity i ceny.** Darmowe limity **nie są publikowane**. Po osiągnięciu pułapu zwracany jest `429 FreeUsageLimitError` „Rate
limit exceeded” *(raport zewnętrzny, 18.08.2026)*; jeden katalog twierdzi, że to 100 zapytań/dzień, niezweryfikowane. Płatne ceny
katalogowe (dokumentacja Zen, 13.10.2026, USD za 1M wejście / wyjście / cache): DeepSeek V4 Flash 0,14 / 0,28 / 0,028 (checkpoint nie
podany), GLM 5.3 Flash 0,15 / 0,50 / 0,03, MiniMax M3 0,30 / 1,20 / 0,06, DeepSeek V4 Pro 1,74 / 3,48, Qwen3.8 Max 2 / 6,
Kimi K3 3 / 15. Ostatnie trzy przekraczają limit 3 USD.

**Jak uzyskać dostęp.**
1. Zaloguj się do konsoli opencode.ai i utwórz klucz API; wyeksportuj go jako `OPENCODE_API_KEY`.
2. Darmowe modele nie wymagają kredytu; płatności dodaj tylko dla płatnych modeli.
3. Przed każdym projektem pobierz aktualną listę z `https://opencode.ai/zen/v1/models`: ID zmieniają się co tydzień.
Nie znalazłem żadnej informacji regionalnej dotyczącej Polski.

**Przydatność dla agentów.** Zgodny z OpenAI. Dokumentacja używa teraz `https://opencode.ai/inference/v1/chat/completions`, a także `/messages`
dla modeli Anthropic i `/responses` dla GPT i Muse; starszy `https://opencode.ai/zen/v1/...` nadal obsługuje `/models`. Muse Spark
wymaga klienta Responses API, więc agent oparty na Chat Completions nie wywoła go bez zmian. Haczyk dla moich własnych agentów: **według raportów
bezpośrednie wywołania API dostają 429, podczas gdy OpenCode CLI działa z tym samym kluczem** *(raport zewnętrzny)*, więc darmowy poziom
wygląda na przeznaczony dla klienta OpenCode. Obsługi narzędzi, maksymalnego wyjścia i współbieżności dla poszczególnych modeli nie było w moich źródłach.

**Niezawodność.** Promocje zmieniają się co tydzień. `exo-free` dodano 6.10.2026 i już zniknął z aktualnej listy;
`nemotron-3-ultra-free`, `mimo-v2.5-free` i `ling-3.0-flash-fin-free` są w dokumentacji, ale nie na aktualnej liście (13.10.2026). Modele
„stealth” (`space-bunny-free`, `big-pickle`, `cat-jam-free`, `jev-1.13-free`) mają nieznaną tożsamość. Brak danych o dostępności.

**Ograniczenia.**
- Brak opublikowanych limitów; 429 może przyjść w każdej chwili, a bezpośrednie użycie API może być dławione mocniej niż CLI.
- Każdy darmowy model może zniknąć bez ostrzeżenia; nie podano dat zakończenia.
- Warunki dotyczące danych różnią się w zależności od modelu: Muse, Ling, MiMo i Big Pickle wykorzystują Twoje dane; Step 5, LongCat i Space Bunny nie.
- Muse Spark wymaga Responses API, a jego SKU Contributor może nie odpowiadać konfiguracji testowanej przez AA.
- Płatne ceny nie są lepsze niż bezpośrednio u hostów.

**Gdzie pasuje w moim stosie.**
- Darmowe próby plannera i ewaluacje ze Step 5 Preview (zerowa retencja) na niewrażliwych zadaniach.
- W OpenCode CLI jako darmowy agent do kodowania; tam darmowy poziom działa najlepiej (zobacz `../harnessy-agentowe/README.md`).
- Nie jako backend dla produkcyjnych pętli: brak SLA, brak limitów, cotygodniowe zmiany. Do tego zapłaciłbym hostowi lub użył sprzętu lokalnego.
- Muse Spark tylko na danych publicznych lub jednorazowych, bo Meta na nich trenuje.

**Sprawdź sam.**
```bash
curl -s https://opencode.ai/zen/v1/models | jq -r '.data[].id' | grep -E 'free|pickle'
curl -s https://opencode.ai/zen/v1/chat/completions -H "Authorization: Bearer $OPENCODE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"model":"step-5-preview-free","messages":[{"role":"user","content":"cześć"}]}'
```

**Źródła:** [OpenCode Zen models API](https://opencode.ai/zen/v1/models) · [OpenCode Zen docs](https://opencode.ai/docs/zen/) ·
[manifest.build 429 FreeUsageLimitError](https://manifest.build/errors/opencode-zen/429-freeusagelimiterror-60fcef/) ·
[Exo Free promo](https://www.aipromonow.com/en/promos/opencode-exo-free-oct2026) ·
[AA Muse Spark 1.3](https://artificialanalysis.ai/models/muse-spark-1-3) · [AA leaderboard](https://artificialanalysis.ai/leaderboards/models) ·
[Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) · [Vals TB2.1](https://www.vals.ai/benchmarks/terminal-bench-2-1) ·
[Muse Spark Contributor tier](https://cryptobriefing.com/meta-muse-spark-discounted-data-sharing/) ·
[Muse Spark pricing](https://www.eesel.ai/blog/meta-muse-spark-12-pricing)

---

## 18. Google Gemini API free tier

**Typ:** darmowy poziom (płatne Flex / Batch jako zapas) · **Najlepsze modele:** `gemini-3.8-flash` (AA 41 przy high) · **Wynik: 68**
(Q25 C20 L2 A15 R6) · **Dane:** Trenowanie na promptach: nie z Polski (użytkownicy z EOG dostają warunki danych usługi płatnej także na darmowym
poziomie); gdzie indziej tak, z przeglądem przez ludzi; region hostingu nie podany

> Darmowy poziom bez karty na mocnym, dobrze udokumentowanym modelu z prawdziwym wywoływaniem narzędzi i kontekstem 1M, ale dzienny wolumen jest
> znikomy, a warunki zabraniają udostępniania aplikacji na darmowym poziomie użytkownikom z EOG.

**Co dostajesz.** Stan na 13.10.2026: konto Google i klucz AI Studio dają darmowy dostęp do `gemini-3.8-flash`,
`gemini-3.6-flash`, modeli Flash-Lite, `gemini-3-flash-preview` i Gemma 4. **Modele Pro zniknęły z darmowego poziomu
1.04.2026** *(raport zewnętrzny)*, a `gemini-4-argon` jest tylko płatny. Wolumen dla 3.8 Flash to **około 20 zapytań
dziennie** *(pomiar zewnętrzny)*.

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `gemini-3.8-flash` | 41 (high), 40 (medium), 33 (low) | 1 048 576 | 65 536 | tak, plus ustrukturyzowane wyjścia | myślenie low / medium / high; „minimal” zwraca błąd; multimodalne wejście |
| `gemini-3.6-flash` | brak wyniku AA | nie odnotowano | nie odnotowano | nie odnotowano | darmowy; ta sama cena płatna co 3.8 |

Wyniki 3.8 Flash: Vals TB2.1 81,27, TB4.0 **19,70** (moja lokalna poprzeczka to 18,69), GPQA 94,44, MMLU-Pro 90,22, LCB 89,48
*(pomiar zewnętrzny)*. AA mierzy czas do pierwszego tokena na około 25 s przy wysiłku high. Flash-Lite (AA 22) i
Gemma 4 31B (AA 15) są poniżej poprzeczki.

**Limity i ceny.** Google **nie publikuje już darmowych limitów**; dokumentacja odsyła do strony limitów w AI Studio i mówi, że
„Specified rate limits are not guaranteed”. Zmierzone z treści odpowiedzi 429 w dniu 2.09.2026: 5 RPM / 20 RPD dla modeli Flash 3.7, 3.6, 3.5 i
3-preview, 15 RPM / 500 RPD dla Flash-Lite; około 20 RPD dla 3.8 Flash według raportu z forum z 09.2026 *(pomiary
zewnętrzne)*. Limity są **na projekt, nie na klucz**, i resetują się o północy czasu pacyficznego. Search grounding: 500 RPD za darmo.
Starsze strony podające 1500 RPD / 10 RPM wyglądają na nieaktualne.

Płatny zapas (USD za 1M wejście / wyjście, strona z 13.10.2026): `gemini-3.8-flash` 0,75 / 3,75, cache 0,075, **do
31.12.2026, potem 1,50 / 7,50**. Batch lub Flex: **0,375 / 1,875**, co mieści się w przedziale do 31.12.2026 dla zadań asynchronicznych.

**Jak uzyskać dostęp.**
1. Zaloguj się do AI Studio kontem Google (wiek 18+); karta nie jest potrzebna. Polska jest obsługiwanym regionem.
2. Utwórz klucz API i wyeksportuj go jako `GEMINI_API_KEY`.
3. Sprawdź rzeczywiste limity swojego projektu na aistudio.google.com/rate-limit.
4. Dodatkowe klucze w tym samym projekcie nie dodają limitu; włącz płatności w projekcie, aby korzystać z Flex / Batch.

**Przydatność dla agentów.** Natywne API pod `https://generativelanguage.googleapis.com/v1beta`, zgodne z OpenAI pod
`https://generativelanguage.googleapis.com/v1beta/openai/` (chat/completions, narzędzia, streaming); brak endpointu zgodnego
z Anthropic. Obsługiwane są wywoływanie funkcji, ustrukturyzowane wyjścia, cache, wykonywanie kodu i search grounding. Gemini 3.x
wymaga **odsyłania thought signatures** przy wieloturowym użyciu narzędzi (nie zweryfikowano ponownie). Treść odpowiedzi 429 podaje nazwę limitu
(`GenerateRequestsPerDayPerProjectPerModel-FreeTier`), więc router może wykryć dzienny pułap i od razu przełączyć się na zapas zamiast
ponawiać. Prawdziwym problemem jest opóźnienie na darmowym poziomie: **27–354 s na zapytanie** zmierzone na 3.7 Flash.

**Niezawodność.** Status na aistudio.google.com/status. Darmowe limity były wielokrotnie obcinane w latach 2025–2026 (usunięcie Pro, Flash obniżony
do około 20 RPD). Rotacja modeli jest szybka: 3.5, 3.6, 3.7 i 3.8 Flash wyszły w 2026; modele 2.0 są wyłączone; modele 2.5
zwracają 404 nowym użytkownikom, choć nadal figurują jako darmowe.

**Ograniczenia.**
- Około 20 RPD: jedno uruchomienie agenta z 20 turami narzędziowymi zużywa cały dzień.
- **Zasada EOG:** „You may use only Paid Services when making API Clients available to users in the European Economic Area,
  Switzerland, or the United Kingdom.” Osobisty development i testy na darmowym poziomie są w porządku; aplikacja z użytkownikami z UE musi być płatna.
- Minuty opóźnienia na darmowym poziomie.
- **Limit Antigravity i Gemini CLI to nie API.** Gemini CLI zostało zastąpione przez Antigravity CLI 18.06.2026; jego darmowy
  plan ma około 20 zapytań agenta dziennie z tygodniowym odnawianiem, a Google podobno zawiesza konta, które używają go przez
  inne narzędzia *(raporty zewnętrzne)*. Nie podpinaj go do moich agentów.
- Płatna cena katalogowa podwaja się 1.01.2027.

**Gdzie pasuje w moim stosie.**
- Darmowy runner ewaluacji: kilkadziesiąt sprawdzeń dziennie 3.8 Flash (AA 41) względem mojego lokalnego 34 (zobacz `../kurs_aplikacje_agentowe/14-EWALUACJA.md`).
- Czytnik długich dokumentów dla niewrażliwych danych wejściowych: kontekst 1M i mocne wyniki wiedzy, kilka wywołań dziennie.
- Płatny Flex (0,375 / 1,875 USD) jako tani asynchroniczny worker batch do 31.12.2026.
- Nie jako sub-agent w pętlach: RPD i opóźnienie to wykluczają. Wolumen zostaje na sprzęcie lokalnym.

**Sprawdź sam.**
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/openai/models" -H "Authorization: Bearer $GEMINI_API_KEY"
curl -s https://generativelanguage.googleapis.com/v1beta/openai/chat/completions \
  -H "Authorization: Bearer $GEMINI_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"gemini-3.8-flash","messages":[{"role":"user","content":"Pogoda w Warszawie?"}],
       "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
```

**Źródła:** [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) · [Gemini models](https://ai.google.dev/gemini-api/docs/models) ·
[Gemini 3.8 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) · [Gemini rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) ·
[Gemini API terms](https://ai.google.dev/gemini-api/terms) ·
[dev.to measured limits](https://dev.to/romeroyang/geminis-free-tier-measured-20-requests-a-day-and-google-no-longer-publishes-the-number-4gf2) ·
[Gemini forum 20 RPD](https://discuss.ai.google.dev/t/gemini-3-8-flash-free-tier-20-rpd-is-too-limited-for-practical-evaluation/180609) ·
[aifreeapi EEA note](https://www.aifreeapi.com/en/posts/google-gemini-api-free-tier) ·
[apiyi Pro removal](https://help.apiyi.com/en/google-gemini-api-free-tier-changes-april-2026-guide-en.html) ·
[Gemini CLI quota](https://geminicli.com/docs/resources/quota-and-pricing/) ·
[Antigravity credits](https://agentpedia.codes/blog/antigravity-credits-pricing-explained) · [Antigravity review](https://preuve.ai/blog/antigravity-review) ·
[AA Gemini 3.8 Flash](https://artificialanalysis.ai/models/gemini-3-8-flash) · [Vals TB4.0](https://www.vals.ai/benchmarks/terminal-bench-4) ·
[Vals TB2.1](https://www.vals.ai/benchmarks/terminal-bench-2-1)

---

## 19. Groq (free tier)

**Typ:** darmowy pakiet · **Najlepsze modele:** `qwen/qwen3.8-27b` (AA 34), `openai/gpt-oss-120b` (AA 12) ·
**Wynik: 66** (Q18 C20 L6 A13 R9) · **Dane:** trenowanie na promptach: nieznane (temat nieporuszony, nic na to nie wskazuje); domyślnie
brak retencji poza maksymalnie 30 dniami na monitoring nadużyć, ZDR dostępne; przechowywanie w USA (GCP)

> Inferencja na LPU ze stałym darmowym pakietem bez karty i bardzo wysoką prędkością; jest w top 20, bo Qwen3.8-27B
> dorównuje mojemu lokalnemu modelowi (AA 34) przy około 450 tok/s za darmo.

**Co dostajesz.** Darmowy pakiet bez karty, pakiet Developer pay-as-you-go i Enterprise. Darmowe limity są per
organizację i per model. AA = Artificial Analysis Intelligence Index v4.3.2 na 13.10.2026 (mój lokalny
V4-Flash-0731 = AA 34).

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `qwen/qwen3.8-27b` | 34 | 131 072 | 16 384 | tak | **preview** · vision · natywny kontekst 256K przycięty do 128K |
| `openai/gpt-oss-120b` | 12 | 131 072 | 65 536 | tak | produkcyjny · ~475 t/s, TTFT 0,63 s |

**Limity i ceny.** Darmowy pakiet, 13.10.2026:
- Oba modele: **30 RPM, 1K RPD, 8K TPM, 200K TPD**. Bez zmian co najmniej od września 2026.
- Ceny Developer (USD za 1M, wejście / wyjście): gpt-oss-120b 0,15 / 0,60 (cache 0,075); qwen3.8-27b 0,80 / **4,00**.
- Batch API −50%; pakiet Flex daje 10× wyższe limity w tej samej cenie, ale szybko odrzuca żądania z HTTP 498 `capacity_exceeded`.

**Jak uzyskać dostęp.**
1. Załóż konto na console.groq.com; karta nie jest potrzebna (doniesienia zewnętrzne z września–października 2026). Weryfikacja telefonu: nieznane.
2. Polska i UE są w porządku; zablokowane są tylko Chiny, Rosja, Syria, Iran, Korea Północna i Kuba.
3. Utwórz klucz w sekcji API Keys i wyeksportuj go jako `GROQ_API_KEY`.
4. Opcjonalnie: włącz ZDR w Data Controls (wyłącza Batch).

**Przydatność dla agentów.** Zgodny z OpenAI `https://api.groq.com/openai/v1` (Chat Completions i Responses). **Brak endpointu
Anthropic**; lukę wypełnia proxy społeczności (`wearedevx/groq-for-claude-code`). Tryby JSON object i JSON schema;
`reasoning_effort` i `reasoning_format` na Qwen. **Prawdziwym wąskim gardłem jest limit 8K TPM**: jeden prompt na 8K zjada
całą minutę. Wątki na forum zgłaszają, że gpt-oss-120b ignoruje `tool_choice` lub wymyśla narzędzia; dokładność endpointu AA dla Groq
gpt-oss-120b to 90 *(pomiar zewnętrzny)*. Po wyczerpaniu limitu 429 z nagłówkami `x-ratelimit-*`.

**Niezawodność.** groqstatus.com lipiec–październik 2026: produkcja 100%, preview 99,98%, brak incydentów w październiku. **Rotacja katalogu to
duże ryzyko**: siedem modeli usuniętych od marca 2026, w tym Kimi K2 (15.04), Llama 3.x (16.08, teraz
tylko enterprise) i `qwen3.6-27b` (14.09, około trzech miesięcy po premierze). Nvidia licencjonowała technologię Groq w grudniu 2025;
Groq twierdzi, że GroqCloud działa dalej.

**Ograniczenia.**
- 8K TPM i 200K TPD: żadnych pętli z długim kontekstem w darmowym pakiecie.
- Qwen3.8-27B to preview: wymiana w ciągu kilku miesięcy jest prawdopodobna, a wyjście jest ograniczone do 16K.
- Płatne wyjście Qwen (USD 4,00) przekracza mój budżet; zostań przy darmowym albo idź gdzie indziej po wolumen.
- gpt-oss-120b jest według AA daleko poniżej mojego lokalnego modelu.

**Gdzie pasuje w moim stosie.**
- **Szybki, darmowy sub-agent** do krótkich wywołań routingu narzędzi i klasyfikacji na Qwen3.8-27B.
- Fallback o niskich opóźnieniach, gdy wszystkie cztery lokalne sloty są zajęte, a prompt jest mały.
- Nie do pracy masowej i nie jako planista: do długiego kontekstu wolę lokalny, do planowania komercyjny.

**Sprawdź sam.**
```bash
curl -s https://api.groq.com/openai/v1/models -H "Authorization: Bearer $GROQ_API_KEY" | jq '.data[].id'
curl -s https://api.groq.com/openai/v1/chat/completions -H "Authorization: Bearer $GROQ_API_KEY" -H "Content-Type: application/json" -d '{
 "model":"qwen/qwen3.8-27b","messages":[{"role":"user","content":"Pogoda w Krakowie?"}],
 "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
```

**Źródła:** [Limity żądań](https://console.groq.com/docs/rate-limits) · [Modele](https://console.groq.com/docs/models) · [Qwen3.8 27B](https://console.groq.com/docs/model/qwen/qwen3.8-27b) · [Wycofania](https://console.groq.com/docs/deprecations) · [Flex](https://console.groq.com/docs/flex-processing) · [Twoje dane](https://console.groq.com/docs/your-data) · [Status](https://groqstatus.com/) · [Wątek o problemie z narzędziami](https://community.groq.com/t/gpt-oss-120b-ignoring-tools/385) · [AA: dostawcy gpt-oss](https://artificialanalysis.ai/models/gpt-oss-120b/providers) · [AA: Qwen vs V4 Flash](https://artificialanalysis.ai/models/comparisons/qwen3-8-27b-vs-deepseek-v4-flash)

---

## 20. Cerebras Inference

**Typ:** jednorazowe kredyty · **Najlepsze modele:** `qwen-3.8-27b` (AA 34), `gpt-oss-120b` (AA 12) ·
**Wynik: 66** (Q18 C14 L12 A14 R8) · **Dane:** trenowanie na promptach: nie; wejścia i wyjścia nie są przechowywane (polityka prywatności);
przetwarzanie w USA i innych krajach, brak rezydencji w UE

> Inferencja w skali całego wafla z najszybszą prędkością generowania na rynku; jest w top 20, bo Qwen3.8-27B (AA 34,
> tyle co mój lokalny model) działa z prędkością około 1500–1850 tok/s przy 1M darmowych tokenów dziennie.

**Co dostajesz.** Free Trial z **jednorazowym kredytem USD 5, który wygasa 30 dni po aktywacji**, pakiet Developer pay-as-you-go,
płaskie plany Cerebras Code (wyprzedane) i Enterprise. AA = Artificial Analysis Intelligence Index v4.3.2
na 13.10.2026 (mój lokalny V4-Flash-0731 = AA 34).

**Modele.**

| Model | AA | Kontekst | Maks. wyjście | Narzędzia | Uwagi |
|---|---|---|---|---|---|
| `qwen-3.8-27b` | 34 | 64K darmowo / 128K płatnie | 32K darmowo / 40K płatnie | tak | gęsty · domyślnie wysokie rozumowanie |
| `gpt-oss-120b` | 12 | 65K darmowo / 131K płatnie | 32K darmowo / 40K płatnie | tak | ~1686 t/s, TTFT 0,44 s (AA) |

**Limity i ceny.** 13.10.2026:
- Free Trial, per model: **5 RPM, 30K niecache'owanych / 90K łącznie TPM, 1M tokenów na godzinę, 1M tokenów dziennie**.
- Developer: gpt-oss-120b 1K RPM, 1M niecache'owanych / 3M łącznie TPM; qwen 300 RPM, 150K / 750K TPM; bez limitów dziennych.
- Ceny (USD za 1M, wejście / wyjście): qwen-3.8-27b **0,99 / 1,49**; gpt-oss-120b 0,35 / 0,75. Cena cache nieznana.
- Cerebras Code Pro USD 50/mies. (24M tokenów dziennie) i Max USD 200/mies. (120M dziennie): **„wyprzedane”**; strona wciąż wymienia
  wycofany GLM-4.7.

**Jak uzyskać dostęp.**
1. Zarejestruj się na cloud.cerebras.ai.
2. **Dodaj zweryfikowaną metodę płatności** (wymagane od 16.07.2026); do tego czasu API pozostaje nieaktywne. Wpisy mówiące „bez
   karty” są nieaktualne.
3. Nie znalazłem ograniczeń regionalnych dla Polski (nieznane).
4. Utwórz klucz i wyeksportuj go jako `CEREBRAS_API_KEY`.

**Przydatność dla agentów.** Zgodny z OpenAI `https://api.cerebras.ai/v1`; **brak endpointu Anthropic**. Równoległe wywołania narzędzi, wszystkie
tryby `tool_choice`, ścisłe ustrukturyzowane wyjścia (unikaj `pattern`, `minLength`, `maxLength`). Pułapki: gpt-oss
**odrzuca `tools` razem z `response_format` w jednym żądaniu**; `tool_stream` nieobsługiwane (użyj `stream: true`); brak `n > 1`.
**5 RPM to mało** dla wieloetapowych agentów, a darmowy kontekst 64K przycina długie historie. Ustaw
`reasoning_effort: "none"` na Qwen dla szybkich wywołań routingu. Dokładność endpointu AA dla gpt-oss-120b tutaj to 92
*(pomiar zewnętrzny)*.

**Niezawodność.** status.cerebras.ai nie pokazuje incydentów od 29.09 do 13.10.2026, ale widoczna historia jest krótka.
**Głównym ryzykiem jest zmienność katalogu**: publiczny katalog skurczył się z około 12 modeli do 2, GLM-4.7 usunięto 17.08,
a Gemma 4 03.09.2026; wpis na blogu z maja 2026 donosi o usunięciach bez uprzedzenia.

**Ograniczenia.**
- Karta wymagana, a kredyt USD 5 wystarcza tylko na 30 dni.
- 5 RPM i kontekst 64K w darmowej wersji próbnej.
- Tylko dwa publiczne modele; Kimi K2.6 i GLM-5.x są dostępne wyłącznie jako dedykowane endpointy enterprise.
- Płaskie plany Code są wyprzedane i nie wiadomo, jaki model serwują.

**Gdzie pasuje w moim stosie.**
- **Sub-agent krytyczny dla opóźnień**: szybkie serie rozumowania na Qwen3.8-27B tam, gdzie moje lokalne 13,6 tok/s jest za wolne.
- Runner ewaluacji dla zestawów z krótkimi promptami, wykorzystujący 1M TPD w ramach 5 RPM.
- Płatny Qwen za USD 1,49 za wyjście to rozsądna cena za szybkość; przy długim kontekście zostaję lokalnie (131k na slot).

**Sprawdź sam.**
```bash
curl -s https://api.cerebras.ai/v1/models -H "Authorization: Bearer $CEREBRAS_API_KEY" | jq '.data[].id'
curl -s https://api.cerebras.ai/v1/chat/completions -H "Authorization: Bearer $CEREBRAS_API_KEY" -H "Content-Type: application/json" -d '{
 "model":"qwen-3.8-27b","reasoning_effort":"none","messages":[{"role":"user","content":"Pogoda w Krakowie?"}],
 "tools":[{"type":"function","function":{"name":"get_weather","parameters":{"type":"object","properties":{"city":{"type":"string"}},"required":["city"]}}}]}'
```

**Źródła:** [Limity żądań](https://inference-docs.cerebras.ai/support/rate-limits) · [Przegląd modeli](https://inference-docs.cerebras.ai/models/overview) · [Qwen 3.8 27B](https://inference-docs.cerebras.ai/models/qwen-3.8-27b) · [gpt-oss](https://inference-docs.cerebras.ai/models/openai-oss) · [Użycie narzędzi](https://inference-docs.cerebras.ai/capabilities/tool-use) · [Zgodność z OpenAI](https://inference-docs.cerebras.ai/resources/openai) · [Wycofania](https://inference-docs.cerebras.ai/support/deprecation) · [Cennik](https://www.cerebras.ai/pricing) · [Plany Code](https://www.cerebras.ai/code) · [Prywatność](https://www.cerebras.ai/privacy-policy) · [Status](https://status.cerebras.ai/) · [Blog o zmienności katalogu](https://ianlpaterson.com/blog/free-llm-api-2026/)
