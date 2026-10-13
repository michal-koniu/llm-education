# Jak używać tanich i darmowych modeli online w aplikacjach agentowych (październik 2026)

Ten plik to praktyczna połowa przeglądu. [01-PROFILE.md](01-PROFILE.md) opisuje, co oferuje każda trasa, a
[02-MODELE.md](02-MODELE.md) mówi, które modele są wystarczająco mądre. Tutaj opisuję, jak wpinam je w moje agenty: która
praca trafia dokąd, konfiguracja routera, rachunek kosztów, pułapki, krótki test akceptacyjny, warunki korzystania i to, jak to
wszystko monitoruję.

**AA** w tym pliku oznacza **Artificial Analysis Intelligence Index v4.3.2, stan na 13.10.2026** (pomiar strony
trzeciej). Mój lokalny model, DeepSeek-V4-Flash-0731, uzyskuje **AA 34** i to jest poprzeczka. Ceny podaję w USD za 1M
tokenów (wejście / wyjście) według stanu z 13.10.2026. Ceny wejścia z cache podaję osobno.

## 1. Najkrótsza odpowiedź

- **Jeden router, cztery ścieżki.** Moje agenty rozmawiają z jednym endpointem zgodnym z OpenAI (proxy LiteLLM). Router
  to warstwa pośrednia, która decyduje, do którego modelu i hosta trafia każde żądanie. Za nim stoją: lokalny rig
  (moja domowa maszyna), darmowe plany (free tiers), tani hosting pay-as-you-go i Claude Opus jako planista. Agenty
  proszą o nazwę grupy, a nie o konkretnego dostawcę.
- **Dane klientów nigdy nie przechodzą przez router.** Prywatne zadania wołają llama-swap na rigu bezpośrednio. Fallback
  (automatyczne przełączenie na zapasową trasę, gdy główna zawiedzie) to dokładnie ta droga, którą prywatne dane
  wyciekłyby przez przypadek.
- **Darmowe plany służą do eksperymentów i małych partii, nie do pętli produkcyjnych.** Liczą żądania (Gemini około
  20 dziennie, Requesty 200 dziennie) albo tokeny (Groq 200K dziennie, czyli około 3 kroki agenta). Każdy z nich
  zmienił się w 2026 roku.
- **Tanim domyślnym wyborem jest GLM-5.3-Flash (AA 42) za USD 0,15 / 0,50** na zmierzonym hoście, z DeepSeek
  V4.1-Flash (AA 39) jako fallbackiem. 1000 dziesięciokrokowych zadań agentowych kosztuje około USD 20 do 40 z cache.
- **Cache i poziom wysiłku rozumowania (reasoning effort) liczą się bardziej niż cena z cennika.** Zepsuty prompt
  cache (pamięć podręczna wspólnego początku promptu po stronie dostawcy) sprawia, że ten sam przebieg kosztuje 3 do 7
  razy więcej. Maksymalny wysiłek kosztuje w moich przykładach 1,7 do 2,4 razy więcej niż niski.
- **Ten sam model u innego hosta to nie ten sam model.** Skuteczność tool calli (wywołań narzędzi przez model) dla
  GLM-5.3-Flash wahała się w jednym teście od 99,5% (Fireworks) do 84,8% (Nebius) *(pomiar strony trzeciej)*. Przypinaj
  hosty, które zmierzyłeś.
- **Zanim zaufasz trasie, zrób 15-minutowy test akceptacyjny,** i powtarzaj go co miesiąc. Modele, ceny, limity
  i warunki zmieniły się w ciągu ostatnich 90 dni.
- **Ryczałtowe abonamenty do kodowania nie są backendami dla agentów.** GLM Coding Plan, Kimi Code, Alibaba Coding Plan
  i MiMo Token Plan zabraniają używania ich z własnych skryptów czy backendów. Ollama Cloud tego nie ogranicza.

## 2. Cztery ścieżki, jeden router

Pomysł opiera się na [../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md](../kurs_aplikacje_agentowe/17-HYBRYDA-I-ROUTER.md)
oraz [../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md](../kurs_lokalne_modele/10-HYBRYDA-LOKALNY-PLUS-CLAUDE.md).
Ten przegląd dodaje dwie ścieżki online między rigiem a Claude.

| Ścieżka | Co to jest | Mocna strona | Słaba strona |
|---|---|---|---|
| Lokalna | DeepSeek-V4-Flash-0731 (AA 34) przez llama-swap, zgodny z OpenAI pod `http://localhost:8080/v1` | prywatność, brak kosztu za token, 131K kontekstu na slot | 4 sloty po około 13,6 tok/s każdy |
| Darmowa | NVIDIA build (GLM-5.3, AA 45), Kilo (Step 5 Preview, AA 44), Requesty (Ling 3.1 Flash, AA 41), Gemini API (Gemini 3.8 Flash, AA 41) | zerowy koszt, często mocniejsze niż lokalny model | malutkie lub nieopublikowane limity, kolejki, ciągłe zmiany, niektóre trenują na promptach |
| Tani PAYG | GLM-5.3-Flash, DeepSeek V4.1-Flash, V4-Flash-0731 na DeepInfra, MiMo-V2.6-Pro | szybkie, duża równoległość, USD 0,18 do 0,87 za wyjście | jakość zależy od hosta |
| Frontier | Claude Opus jako planista | najlepsze plany i osąd | cena, więc niewiele wywołań |

Przepustowość lokalna w liczbach: 4 sloty × 13,6 tok/s × 86 400 s daje w najlepszym razie około **4,7M tokenów wyjścia
na dobę**. Krok, który pisze 1500 tokenów, zajmuje na jednym slocie około 110 s. To w porządku na noc, ale za wolno do
czegokolwiek interaktywnego.

### Tabela decyzyjna według typu zadania

| Zadanie | Pierwszy wybór | Potem | Dlaczego |
|---|---|---|---|
| Wszystko z danymi klientów lub danymi zawodowymi | **tylko lokalnie** | nic: czekaj albo zakończ błędem | zasada dotycząca danych; dla tej klasy fallback nie istnieje |
| Masowa ekstrakcja i klasyfikacja (dane niewrażliwe) | GLM-5.3-Flash na niskim wysiłku w Z.ai lub Fireworks | V4-Flash-0731 na DeepInfra (te same wagi co lokalnie) | tanio, ExtractBench 80,75 *(deklaracja producenta)*; 0731 nie wymaga ponownego strojenia promptów |
| Mała jednorazowa partia (poniżej około 200 żądań) | Requesty za darmo (Ling 3.1 Flash) albo NVIDIA za darmo | tani GLM-5.3-Flash | mieści się w dziennym darmowym limicie |
| Subagent do kodowania | GLM-5.3-Flash (Vals TB4.0 37,4) | GLM-5.3 na wiernym hoście; darmowy GLM-5.3 w NVIDIA do eksperymentów | najlepszy wynik w trudnych zadaniach terminalowych na dolara |
| Pętla z dużą liczbą narzędzi (wiele krótkich kroków) | DeepSeek V4.1-Flash u producenta (190 tok/s, TTFT 0,96 s) | GLM-5.3-Flash | szybkość i trafienia w cache za USD 0,003 poza szczytem; darmowe plany padają na liczbie żądań |
| Czytanie długiego kontekstu (200K do 1M) | DeepSeek V4.1-Flash, kontekst 1M, stabilny prefiks | darmowy plan Gemini 3.8 Flash do czytania wymagającego dużej wiedzy | unikaj hostów z obciętym kontekstem (sekcja 6); lokalny model kończy się na 131K |
| Ewaluacja i ocenianie | model z innej rodziny niż oceniany, np. MiMo-V2.6-Pro (AA 46) | Claude Opus w spornych przypadkach | sędzia z tej samej rodziny sam sobie schlebia |
| Planowanie i dekompozycja | Claude Opus | MiMo-V2.6-Pro jako tania druga opinia | mało wywołań, wysoka stawka |
| Nadmiar, gdy lokalna kolejka jest pełna (tylko dane niewrażliwe) | V4-Flash-0731 na DeepInfra (USD 0,06 / 0,18) | V4.1-Flash | te same wagi, więc działają te same prompty i parsery |

**Moja zasada:** fallbacki idą od darmowych do tanich i od tanich do tanich. Nic nie przełącza się automatycznie na
ścieżkę lokalną, bo jej 4 sloty należą do prywatnej pracy. Nic też nigdy nie przełącza się ze ścieżki lokalnej na
zewnątrz.

## 3. Konkretna konfiguracja routera LiteLLM

LiteLLM działa jako proxy (domyślnie port 4000) przed wszystkim innym. Każde `model_name` to grupa, a wdrożenia
(deployments) o tej samej nazwie dzielą między siebie ruch (load balancing). Trzymam **jeden model na grupę**, więc
fallback nigdy po cichu nie podmieni GLM na DeepSeek w środku zadania. Robią to fallbacki między grupami, i robią to
jawnie.

**Wszystkie ID modeli i slugi dostawców OpenRouter poniżej są aktualne na 13.10.2026. Przed użyciem sprawdź bieżące
ID.** Wartości `rpm` to moje własne ograniczenia ustawione poniżej opublikowanych lub zmierzonych limitów.

```yaml
# litellm-config.yaml: cztery ścieżki, jeden router. Klucze wyłącznie ze zmiennych środowiskowych.
model_list:
  # ---- ścieżka 1: lokalny rig. Prywatne zadania wołają llama-swap bezpośrednio; ten wpis jest tylko dla danych niewrażliwych.
  - model_name: local
    litellm_params:
      model: openai/DeepSeek-V4-Flash-0731          # nazwa zdefiniowana w llama-swap
      api_base: http://localhost:8080/v1
      api_key: os.environ/LOCAL_API_KEY             # llama-swap go ignoruje; dowolny ciąg znaków
      max_parallel_requests: 4                      # 4 sloty
      timeout: 1800                                 # ~13,6 tok/s na slot: długie odpowiedzi trwają minuty
    model_info: {max_input_tokens: 131072}

  # ---- ścieżka 2: darmowe plany (tylko dane niewrażliwe)
  - model_name: free-glm                            # GLM-5.3, AA 45
    litellm_params:
      model: openai/z-ai/glm-5.3                    # sprawdź aktualne ID
      api_base: https://integrate.api.nvidia.com/v1
      api_key: os.environ/NVIDIA_API_KEY
      rpm: 30                                       # ~40 RPM na KONTO (pomiar społeczności), wspólne dla wszystkich modeli NVIDIA
      timeout: 900                                  # kolejkowanie przy popularnych modelach
      cooldown_time: 300
  - model_name: free-step                           # Step 5 Preview, AA 44; promocja; Kilo oznacza go jako „may train”
    litellm_params:
      model: openai/stepfun/step-5-preview-free
      api_base: https://api.kilo.ai/api/gateway
      api_key: os.environ/KILO_API_KEY              # darmowe modele odpowiadają bez klucza
      rpm: 3                                        # 200 żądań na godzinę na IP
      timeout: 300
  - model_name: free-ling                           # Ling 3.1 Flash, AA 41; endpoint w UE
    litellm_params:
      model: openai/novita/ling-3.1-flash
      api_base: https://router.eu.requesty.ai/v1
      api_key: os.environ/REQUESTY_API_KEY
      rpm: 5                                        # 200 żądań na DOBĘ łącznie dla wszystkich darmowych modeli Requesty
      timeout: 300
      cooldown_time: 3600
    model_info: {max_input_tokens: 262144, max_output_tokens: 32768}
  - model_name: free-gemini                         # Gemini 3.8 Flash, AA 41 (high)
    litellm_params:
      model: gemini/gemini-3.8-flash
      api_key: os.environ/GEMINI_API_KEY
      rpm: 5                                        # zmierzone ~5 RPM / ~20 RPD; reset o północy czasu pacyficznego
      timeout: 600                                  # zmierzone opóźnienie darmowego planu: 27-354 s
      cooldown_time: 3600                           # 429 z dziennego limitu nie zniknie po dwóch minutach
    model_info: {max_input_tokens: 1048576, max_output_tokens: 65536}

  # ---- ścieżka 3: tani pay-as-you-go
  - model_name: cheap-glm                           # GLM-5.3-Flash, AA 42: trzy hosty, ten sam model
    litellm_params:
      model: openrouter/z-ai/glm-5.3-flash
      api_key: os.environ/OPENROUTER_API_KEY
      rpm: 60
      timeout: 300
      extra_body:
        provider:
          order: ["fireworks", "together", "parasail"]  # najlepsza zmierzona skuteczność narzędzi; sprawdź slugi na /endpoints
          allow_fallbacks: false                    # nie odpływaj do niezmierzonego hosta
          require_parameters: true                  # nigdy nie trafiaj na host, który gubi tools lub response_format
          quantizations: ["fp8", "bf16"]
          data_collection: "deny"                   # pomijaj endpointy, które mogą przechowywać dane lub na nich trenować
  - model_name: cheap-glm
    litellm_params:
      model: openai/glm-5.3-flash
      api_base: https://api.z.ai/api/paas/v4        # endpoint PAYG, NIE endpoint Coding Plan
      api_key: os.environ/ZAI_API_KEY
      rpm: 60
      timeout: 300
  - model_name: cheap-glm
    litellm_params:
      model: fireworks_ai/accounts/fireworks/models/glm-5p3-flash   # sprawdź aktualne ID
      api_key: os.environ/FIREWORKS_API_KEY
      rpm: 60
      timeout: 300

  - model_name: cheap-ds                            # DeepSeek V4.1-Flash, AA 39
    litellm_params:
      model: deepseek/deepseek-flash                # ID u samego producenta, obecnie V4.1-Flash
      api_key: os.environ/DEEPSEEK_API_KEY
      max_parallel_requests: 100                    # DeepSeek pozwala na 2500 równoległych żądań
      timeout: 900                                  # serwer trzyma żądania w kolejce do 10 minut
  - model_name: cheap-ds
    litellm_params:
      model: openrouter/deepseek/deepseek-v4.1-flash
      api_key: os.environ/OPENROUTER_API_KEY
      rpm: 60
      timeout: 300
      extra_body:
        provider:
          order: ["deepinfra"]
          allow_fallbacks: false
          require_parameters: true
          quantizations: ["fp8"]
          data_collection: "deny"

  - model_name: cheap-0731                          # te same wagi co na rigu, na nadmiar niewrażliwej pracy
    litellm_params:
      model: openai/deepseek-ai/DeepSeek-V4-Flash-0731
      api_base: https://api.deepinfra.com/v1/openai
      api_key: os.environ/DEEPINFRA_TOKEN
      max_parallel_requests: 50                     # DeepInfra pozwala na 200 równoległych żądań na model
      timeout: 600

  # ---- ścieżka 4: planista z czołówki (frontier)
  - model_name: frontier
    litellm_params:
      model: anthropic/claude-opus-5-5              # sprawdź aktualne ID
      api_key: os.environ/ANTHROPIC_API_KEY
      timeout: 600

router_settings:
  routing_strategy: simple-shuffle
  enable_pre_call_checks: true                      # pomijaj wdrożenia ze zbyt małym oknem kontekstu
  num_retries: 2
  retry_policy:
    RateLimitErrorRetries: 1                        # jedna ponowna próba na innym wdrożeniu, potem fallback
    TimeoutErrorRetries: 1
    InternalServerErrorRetries: 2
    BadRequestErrorRetries: 0                       # 400 to błąd albo brak odesłanego z powrotem reasoningu; ponowienie nie pomoże
  allowed_fails_policy:
    RateLimitErrorAllowedFails: 1                   # jedno 429 wysyła wdrożenie na cooldown
    InternalServerErrorAllowedFails: 3
  cooldown_time: 120
  fallbacks:
    - {"free-glm": ["cheap-glm"]}
    - {"free-step": ["cheap-glm"]}
    - {"free-ling": ["cheap-glm"]}
    - {"free-gemini": ["cheap-glm"]}
    - {"cheap-glm": ["cheap-ds"]}
    - {"cheap-ds": ["cheap-0731"]}
    # celowo brak: cokolwiek -> local oraz local -> cokolwiek
  context_window_fallbacks:
    - {"free-ling": ["cheap-glm"]}                  # 262K na Requesty -> 1M

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
```

Uwagi do konfiguracji:

- **Blok `provider` OpenRoutera** jest przekazywany przez `extra_body`. `order` razem z `allow_fallbacks: false` przypina
  hosty. `require_parameters: true` odrzuca hosty, które nie obsługują każdego parametru z żądania, na przykład `tools`
  czy `response_format`. `quantizations` filtruje według precyzji. `data_collection: "deny"` pomija endpointy, które
  mogą przechowywać dane lub na nich trenować. Jeśli nie mam pomiaru dla danego modelu, pomijam `order` i pozwalam
  wybierać **Auto Exacto**: od 12.03.2026 dla każdego żądania z `tools` ustala ono na nowo ranking dostawców na
  podstawie telemetrii tool calli. Nigdy nie używaj `:floor` dla agentów, bo wybiera najtańszy host bez względu na
  jakość.
- **Filtr kwantyzacji może też usunąć endpointy, których kwantyzacja jest „unknown”** (tak na OpenRouterze pokazują ją
  sam DeepSeek, Fireworks i Together). Test akceptacyjny z sekcji 7 mówi mi, który host faktycznie odpowiedział.
- **Timeouty są celowo długie.** NVIDIA kolejkuje popularne modele, DeepSeek trzyma żądania w kolejce do 10 minut,
  a darmowe Gemini odpowiadało we wrześniowym pomiarze w 27 do 354 s. Krótki timeout po stronie klienta plus ponowienie
  po prostu podwajają obciążenie i rachunek.
- **Cooldowny po 429.** Cooldown to okres, przez który router omija wdrożenie po błędzie. Jedno 429 wysyła wdrożenie
  na cooldown i używane jest następne w grupie. Dla darmowych planów z limitem *dziennym* ustawiam długie
  `cooldown_time` na poziomie wdrożenia. O ile wiem, LiteLLM nie ma limitu żądań na dobę dla pojedynczego wdrożenia,
  więc po wyczerpaniu dziennego limitu router będzie próbował dalej raz na każdy cooldown. Na darmowych modelach
  OpenRoutera nawet nieudane żądania mogą się wliczać do dziennego limitu *(pomiar strony trzeciej)*.
- **Wysiłek rozumowania ustawiam dla każdego wywołania w aplikacji**, nie w routerze (sekcja 5). Kroki masowe idą na
  niskim wysiłku, a trudne kroki na wysokim.
- **Prompt cache żyje u jednego dostawcy.** Gdy router rozkłada jedno zadanie na kilka hostów, każda zmiana hosta
  oznacza ponowne zapłacenie pełnej ceny za prefiks. Przy długich zadaniach wolę grupę z jednym wdrożeniem i grupą
  zapasową niż grupę, która tasuje ruch między trzema hostami.

## 4. Uczciwe żonglowanie darmowymi planami

**Jedno konto na usługę, używane tak, jak usługa to przewiduje.** Nie łączę kont w pule. GLM Coding Plan zakazuje
współdzielenia kont (ponad 3 naruszenia oznaczają bana). Google zawieszał konta Antigravity, które zużywały limit
przez inne narzędzia. Repozytoria z pulami kont Puter łamią ducha warunków Puter. NVIDIA wymaga weryfikacji SMS dla
każdego konta. Ban zwykle trafia w tożsamość, a razem z nią w płatne konto, od którego zależę. Darmowe plany to
próbki; gdy któryś zaczyna dźwigać realne obciążenie, płacę za niego.

### Limity liczone w żądaniach a limity liczone w tokenach

Krok agenta wysyła ponownie całą historię, więc jednostka limitu decyduje o wszystkim. Mój standardowy krok ma
**60K tokenów kontekstu, z czego 54K trafia w cache, 6K jest nowych, a 1,5K to wyjście** (łącznie z rozumowaniem).

| Trasa | Limit liczy | Darmowy wolumen (13.10.2026) | Reset | Zakres | Kroki z kontekstem 60K na dobę |
|---|---|---|---|---|---|
| Gemini API, Gemini 3.8 Flash | żądania | ~5 RPM, ~20 RPD *(pomiar strony trzeciej)* | północ czasu pacyficznego | na projekt (dodatkowe klucze nic nie dają) | ~20 |
| NVIDIA build | żądania | ~40 RPM *(pomiar społeczności)*, dzienny limit nieznany | nieudokumentowany | na konto, wspólny dla wszystkich modeli | ogranicza kolejka, nie limit |
| Requesty za darmo | żądania | 200 RPD, bez karty | codziennie, godzina nieudokumentowana | na konto, wspólny dla wszystkich darmowych modeli | 200 |
| Kilo za darmo | żądania | 200 na godzinę na IP, bez konta | co godzinę | na IP (NAT go współdzieli) | do 200 na godzinę |
| OpenRouter za darmo | żądania | 20 RPM; 50 RPD albo 1000 RPD po łącznych zakupach za USD 10 | codziennie, godzina nieudokumentowana | na konto | 1000, ale tamtejsze darmowe modele są poniżej poprzeczki |
| Groq za darmo | tokeny i żądania | 30 RPM, 1K RPD, 8K TPM, 200K TPD | codziennie | na organizację, na model | ~3 (8K TPM blokuje nawet jeden krok) |
| Cerebras, darmowy okres próbny | tokeny | 5 RPM, 30K TPM bez cache, 1M TPD, kontekst 64K | codziennie | na model; wymagana karta | ~16, ale krok 60K ledwo mieści się w 64K |
| Cloudflare Workers AI | neurony | 10 000 neuronów dziennie (około 147K tokenów wyjścia gpt-oss-120b) | 00:00 UTC | na konto | tylko gpt-oss-120b (AA 12) |
| Alibaba Model Studio intl | tokeny | 1M na model, jednorazowo, na 90 dni | nigdy | na model | ~16 łącznie, na model |

Co to oznacza w praktyce:

- **Plany liczone w żądaniach faworyzują kroki z długim kontekstem.** Krok z 60K tokenów kosztuje w Requesty jedno
  żądanie z 200. Ten sam krok kosztuje w Groq 30% dziennych tokenów.
- **Zadanie z dziesięcioma krokami kosztuje 10 żądań plus ponowienia.** Requesty daje mi około 20 takich zadań
  dziennie, Gemini około dwóch.
- **Godziny resetu w czasie polskim:** północ czasu pacyficznego to przez większą część roku 09:00, ale między
  25.10.2026 a 1.11.2026 jest to 08:00, bo Europa przeszła już na czas zimowy, a USA jeszcze nie. Cloudflare
  dokumentuje 00:00 UTC. Większość pozostałych tego nie podaje, więc czytam nagłówki `x-ratelimit-*` i treść
  odpowiedzi 429 (Gemini podaje nazwę limitu, na przykład `GenerateRequestsPerDayPerProjectPerModel-FreeTier`).
- **Inne okna czasowe:** Ollama Free resetuje się co miesiąc, licząc od daty rejestracji. Okno poza szczytem w Z.ai
  zmniejsza o połowę zużycie kredytów Coding Plan. Okno szczytu w DeepSeek (01:00 do 04:00 i 06:00 do 10:00 UTC w dni
  robocze) podwaja cenę.
- **Pułapki przy przejściu na płatne:** w Vercel AI Gateway kupienie jakichkolwiek kredytów na zawsze kończy darmowy
  kredyt USD 5 na 30 dni. W OpenRouterze ujemne saldo zwraca 402 nawet na darmowych modelach.
## 5. Rachunek kosztów

Ceny użyte w tej sekcji (13.10.2026, wejście / wejście z cache / wyjście):

- **DeepSeek V4.1-Flash, bezpośrednio u producenta:** 0,15 / 0,003 / 0,60 poza godzinami szczytu. W szczycie ceny są dwa razy wyższe.
- **GLM-5.3-Flash na Z.ai:** 0,15 / 0,03 / 0,50.
- **MiMo-V2.6-Pro u Xiaomi:** 0,435 / 0,0036 / 0,87.
- **OpenRouter V4.1-Flash, host fp4 (Decart):** 0,09 / 0,018 / 0,18.
- **OpenRouter V4.1-Flash, host fp8 (DeepInfra):** 0,14 / 0,004 / 0,42. To cena promocyjna (−30%).

Wiersze OpenRouter uwzględniają jego 5,5% opłaty od zakupu kredytów. W Ollama Pro (USD 20 miesięcznie z kredytami za
USD 60) V4.1-Flash kosztuje 0,15 / 0,60 poza szczytem. Moje źródła nie podają ceny Ollamy za wejście z cache, więc
zakładam brak zniżki za cache. To najgorszy przypadek i warto go sprawdzić.

### Przykład 1: masowa ekstrakcja, 1000 zadań × 3 kroki

Każdy krok to 6K tokenów wejścia (3K prefiksu z cache plus 3K nowego tekstu) i 1K wyjścia. Łącznie daje to 9M tokenów
z cache, 9M bez cache i 3M tokenów wyjścia.

| Trasa | Model (AA) | Koszt 1000 zadań |
|---|---|---|
| DeepSeek poza szczytem | V4.1-Flash (39) | USD 3,18 (w szczycie 6,35) |
| Z.ai | GLM-5.3-Flash (42) | USD 3,12 |
| Xiaomi | MiMo-V2.6-Pro (46) | USD 6,56 |
| OpenRouter fp4 (Decart) | V4.1-Flash (39) | USD 1,60 |
| OpenRouter fp8 (DeepInfra) | V4.1-Flash (39) | USD 2,70 |
| Ollama Pro, poza szczytem | V4.1-Flash (39) | USD 4,50 z kredytów (7,5% miesiąca) |
| Lokalny rig | V4-Flash-0731 (34) | USD 0, około 15 godzin na 4 slotach |
| Requesty za darmo | Ling 3.1 Flash (41) | USD 0, 15 dni przy 200 RPD |

**Przy tej skali pieniądze niczego nie rozstrzygają. Rozstrzygają jakość, opóźnienie i warunki dotyczące danych.**
Oszczędność USD 1,10 dzięki przejściu na mikrohosta fp4 bez żadnych danych o dokładności nie jest tego warta.

### Przykład 2: pętla narzędziowa, 1000 zadań × 10 kroków, kontekst 60K

To mój standardowy krok: 54K z cache, 6K nowych tokenów i 1,5K wyjścia. 10 000 kroków daje 540M tokenów z cache, 60M
bez cache i 15M tokenów wyjścia. Druga kolumna to wariant z zepsutym cache (wszystkie 600M tokenów wejścia bez cache).
Trzecia to Przykład 3: ta sama pętla przy maksymalnym poziomie rozumowania (max effort), który modeluję jako 6K
wyjścia na krok zamiast 1,5K (łącznie 60M wyjścia).

| Trasa | Prz. 2, cache działa | Prz. 2, cache zepsuty | Prz. 3, max effort | Czas generowania na krok (1,5K / 6K wyjścia) |
|---|---|---|---|---|
| DeepSeek V4.1-Flash, poza szczytem | **USD 19,62** | USD 99,00 (5,0×) | USD 46,62 (2,4×) | 8 s / 32 s przy 190 tok/s |
| DeepSeek V4.1-Flash, szczyt | USD 39,24 | USD 198,00 | USD 93,24 | tak samo |
| GLM-5.3-Flash, Z.ai | **USD 32,70** | USD 97,50 (3,0×) | USD 55,20 (1,7×) | 23 s / 90 s przy 66,5 tok/s |
| MiMo-V2.6-Pro, Xiaomi | USD 41,09 | USD 274,05 (6,7×) | USD 80,24 (2,0×) | 32 s / 128 s przy 46,8 tok/s |
| OpenRouter V4.1-Flash fp4 (Decart) | USD 18,80 | USD 59,82 | USD 27,35 | zależy od hosta |
| OpenRouter V4.1-Flash fp8 (DeepInfra) | **USD 17,79** | USD 95,27 | USD 37,73 | zależy od hosta |
| Ollama Pro, V4.1-Flash poza szczytem (zakładam brak zniżki za cache) | USD 99 z kredytów | USD 99 z kredytów | USD 126 z kredytów | zależy od hosta |
| Lokalny rig, V4-Flash-0731 | USD 0 | USD 0 | USD 0 | 110 s / 441 s przy 13,6 tok/s |

Jak sumuje się główny wiersz, dla DeepSeek poza szczytem: 540M × 0,003 = 1,62, plus 60M × 0,15 = 9,00, plus
15M × 0,60 = 9,00.

Co pokazują liczby:

- **Tania cena wejścia z cache wygrywa z tanią ceną katalogową.** Gdy cache działa, endpoint fp8 w DeepInfra jest
  tańszy od fp4, bo jego cena za cache to 0,004 wobec 0,018. Trasa fp4 wygrywa tylko wtedy, gdy cache jest zepsuty.
- **GLM-5.3-Flash liczy cache po 20% swojej ceny wejścia**, wobec około 2% w DeepSeek i poniżej 1% w MiMo. Dlatego
  GLM jest najtańszy za token w Przykładzie 1, ale nie w Przykładzie 2.
- **MiMo-V2.6-Pro jest tani jako planista i drogi jako wykonawca.** Jego 0,435 za wejście bez cache boli przy każdym
  chybieniu cache.
- **Kredyty Ollama Pro za USD 60 wystarczają na około 600 takich zadań miesięcznie**, jeśli tokeny z cache są liczone
  w pełnej cenie. Plan błyszczy przy GLM-5.3 (AA 45) na krótkich kontekstach. Przy efektywnych około USD 0,47 / 1,47
  GLM-5.3 mieści się tam w paśmie.
- **Lokalny rig jest darmowy, ale 10 000 kroków po 110 s każdy na 4 slotach to około 76 godzin** generowania. To
  w porządku dla nocnej kolejki prywatnych zadań, a nie nadaje się do niczego innego.
- **Co psuje cache:** znacznik czasu lub ID żądania na początku system promptu, listy narzędzi w zmiennej kolejności,
  router przełączający hosty i przepisywanie historii (podsumowania, które zmieniają wcześniejsze wiadomości).
  Utrzymuję prefiks stabilny co do bajtu i tylko dopisuję na końcu.

### Pokrętła poziomu rozumowania (reasoning effort)

Maksymalny poziom często niewiele daje. DeepSeek podaje, że effort od 60 do 80 daje większość dokładności poziomu max
przy mniej niż połowie tokenów *(deklaracja producenta)*. AA uznaje DeepSeek V4.1-Flash za najbardziej rozwlekły model,
jaki zmierzyło: 250M tokenów wyjścia na indeksie wobec mediany 140M *(pomiar zewnętrzny)*. Niski effort może też
obniżyć wynik modelu do progu albo poniżej niego.

| Model | Pokrętło | Wartości | Domyślnie | Moje ustawienie |
|---|---|---|---|---|
| DeepSeek V4.1-Flash (u producenta) | `reasoning_effort` | low / high / max (NVIDIA build: od 1 do 100) | thinking włączone | low dla rutynowych kroków, high dla trudnych |
| GLM-5.3 (Z.ai) | `reasoning_effort` | low / high / max; thinking nie da się wyłączyć | **max** | low w pętlach; AA to 34 przy low i 45 przy max |
| GLM-5.3-Flash | `reasoning_effort` | od low w górę | rozumowanie włączone | low; tbench.ai TB4.0 to 35,8 nawet przy effort `none` *(pomiar zewnętrzny)* |
| Step 5 Preview | `reasoning_effort` | low / medium / high | brak w moich źródłach | medium |
| Gemini 3.8 Flash | thinking level | low / medium / high („minimal” zwraca błąd) | brak w moich źródłach | medium; AA 33 przy low (poniżej progu), 41 przy high |
| Kimi K3 | brak | thinking zawsze włączone | włączone | i tak poza pasmem; AA 30 przy low |
| Qwen3.8-27B (Groq, Cerebras) | `reasoning_effort` | none / low / medium / high | high na Cerebras | AA 34 dopiero przy xhigh |
| MiMo-V2.6-Pro | nie znalazłem w moich źródłach | rozumowanie włączone | włączone | zostawiam, używam do nielicznych wywołań |

## 6. Pułapki jakościowe

**Ten sam model, inny host.** Oto największe zmierzone różnice *(pomiary zewnętrzne)*:

| Model | Dobre hosty | Złe hosty | Źródło i data |
|---|---|---|---|
| GLM-5.3-Flash, 600 zadań z narzędziami | Fireworks 99,5%, Telnyx 99,5%, Modal 99,3%, Together 98,5%, Parasail 98,3%, Z.AI 97,5% | DeepInfra 95,5%, Novita 94,2%, **Nebius 84,8% (14,8% błędów)** | openbenchmarks, 3.09.2026 |
| GLM-5.2, AA Endpoint Accuracy | FriendliAI, Nebius, Fireworks 100 | **Scaleway 75, DeepInfra 73 (FP4)** | AA, 26.09.2026 |
| gpt-oss-120b, AA Endpoint Accuracy | Bedrock 104, Nebius 102, DeepInfra Turbo 98 | **DeepInfra domyślny 85, Together 81, Vertex 72** | AA, 26.09.2026 |
| GLM-5.3, AA Endpoint Accuracy | 15 hostów w przedziale od 95 do 99 | brak | AA, 26.09.2026 |
| DeepSeek V4 Pro, AA Endpoint Accuracy | od 97 do 107 wszędzie | brak | snapshot AA, sierpień 2026 |
| Kimi K2-0905, Moonshot K2VV | DeepInfra, Fireworks 100% zgodności ze schematem | Groq: 100% zgodności ze schematem, ale F1 tool calli 69,52% | K2VV, 15.11.2025 |

- **Szkody skupiają się w tool callingu.** W danych GLM-5.2 tool calling w BFCL spadł z 37% do 22% na najgorszym
  endpoincie, a GPQA przesunęło się tylko o około 8 punktów. Benchmark czatowy nie pokaże ci tego problemu.
- **Kwantyzacja nie jest automatycznie zła.** GLM-5.3 w FP4 na Nebius ma 99. GLM-5.2 w FP4 na DeepInfra ma 73. Mierz
  endpoint, nie etykietę.
- **Ponowne rankingowanie w OpenRouter pokazuje, jak częste są złe hosty.** Auto Exacto obniżyło odsetek błędów
  narzędzi GLM-5 z 8% do około 1%, a gpt-oss-120b z 5,6% do 3,5% *(deklaracja producenta)*. Wcześniej odsetek błędów
  narzędzi od 5 do 8% na dostawcę był normą dla popularnych modeli.
- **V4-Flash nie ma szablonu czatu Jinja**, więc każdy host pisze własny parser narzędzi. To jedno ze znanych źródeł
  różnic i dotyczy też dostępnych online kopii mojego lokalnego modelu.

**Ciche podmiany modeli i aliasy ID.**

- SiliconFlow 11.06.2026 skierował `GLM-5` na GLM-5.1, a `Kimi-K2.5` na K2.6. Together przekierował GLM-4.6 na 4.7.
- Starsze nazwy `deepseek-v4-flash` w DeepSeek prowadzą teraz do V4.1-Flash (inne wagi, 552B). GLM Coding Plan
  kieruje żądania o 5.2, 5.1 i 4.7 do nowszych modeli.
- Aliasy OpenRouter, takie jak `~deepseek/deepseek-flash-latest`, przechodzą na nowsze wersje. Przypinaj ID z datą.
- Nebius robi odwrotnie: stare ID po prostu przestają działać (wycofania 22.06.2026 i 31.08.2026).

**Limity wyjścia** ucinają długie rozumowanie lub długie patche, zwykle z `finish_reason: "length"`:

- 8K: SiliconFlow gpt-oss-120b.
- 16K: DeepInfra V4-Pro i Kimi K2.6; Groq Qwen3.8-27B.
- 32K: Vercel V4.1-Flash (32 768); Requesty Ling 3.1 Flash; darmowy tier Cerebras.
- 64K do 65K: Step 5 Preview, Gemini 3.8 Flash, DeepInfra V4-Flash.
- 384K: DeepSeek u producenta, dla porównania.

**Obcinanie kontekstu** poniżej natywnego okna:

- Darmowy tier Cerebras: 64K do 65K.
- SambaNova DeepSeek-V3.2: 32K.
- Groq Qwen3.8-27B: 131K (natywnie 256K).
- Scaleway: 256K dla modeli, które natywnie mają 1M.
- OpenRouter Ling 3.1 Flash: 262K.
- Mistral Large 4: zmierzone 524K wobec deklarowanego 1M.

**Echo rozumowania.** Kimi K3 na NVIDIA build wymaga odsyłania `reasoning_content` i `tool_calls` w każdej turze.
Endpoint Xiaomi zgodny z API Anthropic zwraca 400 w wieloturowych tool callach, jeśli treść rozumowania nie zostanie
odesłana. Gemini 3.x wymaga zwracania thought signatures (nie weryfikowałem tego ponownie). Moja pętla agenta trzyma
w historii pełną, niezmienioną wiadomość asystenta.

**Narzędzia i structured output, które są ignorowane lub odrzucane:**

- Inkling free na OpenRouter nie obsługuje `tool_choice`.
- Wątki na forum Groq opisują, jak gpt-oss-120b ignoruje narzędzia albo wymyśla ich nazwy.
- Cerebras gpt-oss-120b odrzuca `tools` i `response_format` w tym samym żądaniu.
- GPT-6 Luna w Chat Completions podobno wywołuje narzędzia tylko przy effort `none`.
- OpenRouter oznacza structured outputs jako nieobsługiwane na kilku endpointach Novita i SiliconFlow. Chutes Kimi K3
  w ogóle nie ma narzędzi.

`require_parameters: true` wyłapuje część z tego. Resztę wyłapuje test akceptacyjny.

**Modele preview i rotacja katalogu.**

- Groq usunął siedem modeli od marca 2026, a jego Qwen3.6-27B przetrwał około trzech miesięcy.
- Cerebras zszedł z około 12 publicznych modeli do 2.
- Na bieżącej liście modeli NVIDIA brakuje ID, które wciąż wymienia jej własna dokumentacja.
- Fireworks 26.09.2026 usunął V4-Flash-0731 i Kimi K2.6 z serverless, a Hyperbolic 24.09.2026 wycofał swoje
  serverless API.
- **Darmowe modele w OpenRouter utrzymują się na liście średnio (mediana) około 75 dni** *(pomiar zewnętrzny)*.
  Lista darmowych modeli skurczyła się z 24 do 16 między 21.09.2026 a 13.10.2026, a wśród usuniętych były
  `glm-5.2:free` i `deepseek-v4-flash-0731:free`.

## 7. 15-minutowy test akceptacyjny, zanim zaufam trasie

**Uruchamiam go bezpośrednio u dostawcy, nie przez router, bo inaczej fallbacki ukryją błędy.**

| Test | Co sprawdzam | Niepowodzenie oznacza |
|---|---|---|
| Tool call | wymuszone `tool_choice: "required"`, właściwa nazwa, argumenty parsują się jako JSON | host gubi lub psuje narzędzia |
| Druga tura narzędzia | pełna wiadomość asystenta odesłana, wynik narzędzia dołączony, sensowna odpowiedź | zasady echa rozumowania (Kimi K3, MiMo) albo zepsuty parser |
| JSON schema | ścisły `json_schema`, wynik się parsuje i pasuje do enum | brak structured output: waliduj i ponawiaj w kodzie albo porzuć trasę |
| Igła w długim kontekście | fakt na 70% głębokości w około 100K tokenów; `prompt_tokens` bliskie oczekiwanym | ciche obcięcie albo limit kontekstu |
| Burst | 20 równoległych żądań: liczba kodów 200 / 429 / 5xx, opóźnienie p50 i p95 | RPM lub współbieżność dużo niższe niż w dokumentacji |
| Tożsamość | zwrócone pole `model`, a na OpenRouter także pole `provider` | cicha podmiana albo host, którego nie przypiąłem |
| Moje własne zadania | od 10 do 20 zadań z mojego zestawu ewaluacyjnego, w porównaniu z lokalnym 0731 | trasa nie jest lepsza od tego, co już mam |

```python
#!/usr/bin/env python3
# accept.py: test akceptacyjny dla JEDNEJ trasy. Wywołuj dostawcę bezpośrednio, nie router.
# BASE_URL=https://api.z.ai/api/paas/v4 API_KEY=$ZAI_API_KEY MODEL=glm-5.3-flash python3 accept.py
# Przypinanie hosta w OpenRouter: EXTRA='{"provider":{"order":["fireworks"],"allow_fallbacks":false}}'
import asyncio, json, os, statistics, time
from collections import Counter
from openai import AsyncOpenAI, APIStatusError

c = AsyncOpenAI(base_url=os.environ["BASE_URL"], api_key=os.environ["API_KEY"], timeout=900, max_retries=0)
M, EXTRA = os.environ["MODEL"], json.loads(os.environ.get("EXTRA", "{}"))
TOOLS = [{"type": "function", "function": {"name": "get_weather", "parameters": {
    "type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}]

async def chat(**kw):
    return await c.chat.completions.create(model=M, extra_body=EXTRA, **kw)

async def tools():
    msgs = [{"role": "user", "content": "Jaka jest pogoda w Krakowie? Użyj narzędzia."}]
    r = await chat(messages=msgs, tools=TOOLS, tool_choice="required")
    m = r.choices[0].message
    tc = m.tool_calls[0]
    assert tc.function.name == "get_weather" and json.loads(tc.function.arguments)["city"]
    msgs += [m.model_dump(exclude_none=True),  # zachowuje reasoning_content, jeśli host go wysłał
             {"role": "tool", "tool_call_id": tc.id, "content": '{"temp_c": 11, "sky": "rain"}'}]
    r2 = await chat(messages=msgs, tools=TOOLS)
    assert "11" in (r2.choices[0].message.content or "")
    return f"model={r.model} provider={getattr(r, 'provider', '-')}"

async def schema():
    fmt = {"type": "json_schema", "json_schema": {"name": "triage", "strict": True, "schema": {
        "type": "object", "additionalProperties": False, "required": ["severity", "service"],
        "properties": {"severity": {"type": "string", "enum": ["low", "high"]},
                       "service": {"type": "string"}}}}}
    r = await chat(response_format=fmt, messages=[{"role": "user",
        "content": "Oceń zgłoszenie: dysk postgresa zapełniony w 100%, zapisy się nie udają."}])
    d = json.loads(r.choices[0].message.content)
    assert d["severity"] in ("low", "high")
    return str(d)

async def needle(tokens=int(os.environ.get("NEEDLE_TOKENS", "100000"))):
    lines = [f"Log line {i}: service healthy." for i in range(tokens // 9)]
    lines.insert(int(len(lines) * 0.7), "NOTE: the rollback password is plum-4417.")
    r = await chat(max_tokens=4096, messages=[{"role": "user",
        "content": "\n".join(lines) + "\n\nWhat is the rollback password? Answer with it only."}])
    assert "plum-4417" in (r.choices[0].message.content or "")
    return f"prompt_tokens={r.usage.prompt_tokens}"  # wynik dużo poniżej oczekiwanego rozmiaru = obcięcie

async def burst(n=20):
    async def one():
        t = time.monotonic()
        try:
            await chat(max_tokens=64, messages=[{"role": "user", "content": "Odpowiedz: OK."}])
            return "200", time.monotonic() - t
        except APIStatusError as e:
            return str(e.status_code), time.monotonic() - t
    res = await asyncio.gather(*[one() for _ in range(n)])
    lat = sorted(t for code, t in res if code == "200")
    p = f" p50={statistics.median(lat):.1f}s p95={lat[int(len(lat) * 0.95) - 1]:.1f}s" if lat else ""
    return f"codes={dict(Counter(code for code, _ in res))}{p}"

async def main():
    for name, test in [("tools", tools), ("schema", schema), ("needle", needle), ("burst", burst)]:
        try:
            print(f"PASS {name}: {await test()}")
        except Exception as e:
            print(f"FAIL {name}: {type(e).__name__}: {str(e)[:200]}")

asyncio.run(main())
```

Przed testem sprawdzam, co o hostach raportuje sam OpenRouter:

```bash
curl -s https://openrouter.ai/api/v1/models/z-ai/glm-5.3-flash/endpoints \
  | jq '.data.endpoints[]|{provider_name,quantization,pricing,uptime_last_1d}'
```

**Moja reguła akceptacji:** wszystkie cztery testy przechodzą, burst nie pokazuje żadnego 5xx, a na moich własnych
zadaniach trasa ma co najmniej taki odsetek zaliczonych zadań jak lokalny 0731. Część dotyczącą ewaluacji opisuję w
[../kurs_aplikacje_agentowe/14-EWALUACJA.md](../kurs_aplikacje_agentowe/14-EWALUACJA.md). W produkcji chcę, żeby
odsetek błędów parsowania tool calli był poniżej około 2%. Najlepsze hosty z tabeli wyżej zawiodły w 0,5 do 2,5% zadań
GLM-5.3-Flash, a Nebius w 14,8%.

## 8. Warunki i dane

### Plany ryczałtowe: własny agent dozwolony czy nie

| Plan | Cena (13.10.2026) | Własny agent lub backend? | Co mówią warunki |
|---|---|---|---|
| GLM Coding Plan | USD 18 / 80 / 168 miesięcznie (źródło zewnętrzne; oficjalnie „from USD 18” (od USD 18)) | **Nie** | „may only be used within officially supported tools and products” (może być używany wyłącznie w oficjalnie obsługiwanych narzędziach i produktach); ponad 3 naruszenia oznaczają bana; brak zwrotów |
| Kimi Code | USD 19 / 39 / 99 / 199 miesięcznie | **Nie** w produkcie, szara strefa we własnym agencie | zmiana User-Agent „is considered a violation” (jest uznawana za naruszenie); dla własnego produktu „visit the Kimi Platform” (odwiedź Kimi Platform) |
| Alibaba Coding Plan Pro | USD 50 miesięcznie | **Nie** | „Do not use the plan's API key for automated scripts, application backends, or other non-interactive scenarios” (nie używaj klucza API planu w zautomatyzowanych skryptach, backendach aplikacji ani innych nieinteraktywnych scenariuszach) |
| MiMo Token Plan | od USD 6 do 100 miesięcznie | **Nie** | „only available for use in programming tools” (dostępny wyłącznie w narzędziach programistycznych) i „prohibited” (zabroniony) dla „automated scripts and custom application backends” (zautomatyzowanych skryptów i własnych backendów aplikacji) |
| MiniMax M Plan | USD 22 / 55 / 132 miesięcznie | tylko interaktywnie | „designed for individual, interactive developer use” (przeznaczony do indywidualnej, interaktywnej pracy programisty); do produkcji zalecany PAYG |
| Fireworks Fire Pass | zamknięty dla nowych subskrybentów | **Nie** | tylko do użytku osobistego i w harnessach do kodowania |
| Ollama Cloud Pro | USD 20 miesięcznie, w tym kredyty za USD 60 | **Tak** | w dokumentacji brak ograniczenia do narzędzi programistycznych |
| StepFun Step Plan | od USD 6,99 do 99 miesięcznie (źródło zewnętrzne) | deklarowane tak | post premierowy: „works with Cursor, Windsurf, Cline, and your own stack” (działa z Cursor, Windsurf, Cline i twoim własnym stosem); sprawdź ToS, przelicznik kredytów nieznany |

Rachunek na planie z ograniczeniami może wyglądać świetnie. GLM Coding Plan Lite wychodzi na około 590 moich
standardowych kroków tygodniowo. To nie ma znaczenia, bo plan zabrania takiego użycia. **Do własnych agentów używam
kluczy PAYG albo Ollama Cloud.** Plany z ograniczeniami są w porządku w narzędziach, które same wymieniają, takich jak
Claude Code czy OpenCode na GLM.

### Flagi trenowania i hostingu (flaga, nie ocena)

| Trasa | Trenuje na promptach | Hosting |
|---|---|---|
| DeepSeek API | opt-out (domyślnie włączone, według zewnętrznej interpretacji polityki) | ChRL |
| Z.ai API (PAYG) | nie (tylko opt-in, zgodnie z DPA) | podmiot w Singapurze |
| Xiaomi MiMo PAYG | domyślnie nie (podsumowania zewnętrzne) | podmioty w Holandii i Singapurze |
| Platforma Kimi | tak, brak opt-outu na poziomie produktu | Singapur (interpretacja zewnętrzna) |
| Trial NVIDIA build | dane mogą służyć do ulepszania produktów NVIDIA | USA (założenie) |
| Darmowe modele Kilo | mogą trenować (Kilo oznacza tak każdy darmowy model) | nieznany |
| OpenCode Zen za darmo | Step 5: nie (zero retencji); Ling i MiMo-Flash: tak | USA i UE |
| Requesty, darmowy Ling 3.1 Flash | nie (metadane katalogu) | endpoint w UE, upstream Novita |
| OpenRouter | zależnie od endpointu; filtruje `data_collection: "deny"` | zależy od hosta |
| Darmowy tier Gemini API, z Polski | nie (EOG dostaje warunki usług płatnych) | Google |
| Mistral Free | tak, chyba że zrezygnujesz (opt-out) | UE |
| Ollama Cloud | nie („never logged or trained on” (nigdy nie są logowane ani używane do trenowania), deklaracja producenta) | głównie USA |
| DeepInfra | nie | USA |
| Together | domyślnie przechowywane, trenowanie opt-in | USA |
| Fireworks | dla modeli otwartych domyślnie nieprzechowywane | globalnie, chyba że używasz endpointu w USA |
| Meta Muse Spark Contributor, tokeny OpenAI za udostępnianie danych | **tak, na tym polega umowa** | USA |

**Uwagi dotyczące EOG.**

- **Gemini:** w EOG, Szwajcarii i Wielkiej Brytanii warunki dotyczące danych z usług płatnych obejmują też darmowy
  tier, więc moje darmowe prompty nie są używane do trenowania. Te same warunki mówią jednak: „You may use only Paid
  Services when making API Clients available to users in the European Economic Area” (udostępniając klientów API
  użytkownikom w Europejskim Obszarze Gospodarczym, możesz korzystać wyłącznie z usług płatnych). Darmowy tier służy
  więc do mojego własnego developmentu i testów, a aplikacja z użytkownikami z UE musi działać na płatnym tierze.
- **Mistral:** od 5.08.2026 (7.08.2026 w UE) API jest ograniczone do klientów biznesowych. Osoby prywatne nie mogą już
  używać go do projektów osobistych.
- **Nebius:** publiczny serverless działa w regionie „Global”, a lokalizacja przetwarzania może się zmienić bez
  uprzedzenia. Rezydencja danych w UE jest dostępna tylko z dedykowanymi endpointami.
- **OpenRouter:** routing w regionie UE jest dostępny tylko w planach Business i Enterprise.
- **Opcje hostowane w UE:** endpoint UE w Requesty, Scaleway (Paryż), OVHcloud (Gravelines) i GLM-5.3 hostowany przez
  Mistral na `api.eu.mistral.ai` (+10%).

**Dane klientów zostają lokalnie.** Nie ma znaczenia, że trasa deklaruje „no training” (brak trenowania). Dane klientów
i dane zawodowe nie opuszczają riga, a prywatny pipeline nawet nie wie, że router istnieje. Szersze zasady są w
[../asystenci-ai/README.md](../asystenci-ai/README.md). Prompt injection przez wynik narzędzia to osobne ryzyko na
każdym odcinku: zobacz
[../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md](../kurs_aplikacje_agentowe/16-BEZPIECZENSTWO-OWASP-ASI.md).

## 9. Monitoring i wyłączniki awaryjne

**Budżety, w trzech warstwach:**

1. **Salda prepaid to twardy limit.** Doładowuję DeepSeek, Z.ai, Xiaomi, DeepInfra i OpenRouter małymi kwotami i mam
   wyłączone automatyczne doładowanie. Together, Kimi i StepFun i tak działają na prepaid. Budżety Vercel zwracają 402
   `quota_for_entity_exceeded`. `curl -s https://openrouter.ai/api/v1/key -H "Authorization: Bearer $OPENROUTER_API_KEY"`
   pokazuje limity klucza.
2. **Budżety w routerze.** Każda aplikacja dostaje własny wirtualny klucz LiteLLM z `max_budget` i `budget_duration`,
   więc jeden agent, który wymknął się spod kontroli, nie przepali budżetu całego miesiąca.
3. **Limity na zadanie w aplikacji.** Ustawiam maksymalną liczbę kroków, `max_tokens` na wywołanie i limit czasu
   rzeczywistego na zadanie. Pętla, która nie zbiega, kosztuje pieniądze na każdym odcinku poza lokalnym.

**Co śledzę dla każdej trasy (dla każdego deploymentu, nie dla grupy):**

- Odsetek udanych odpowiedzi HTTP i rozkład kodów błędów.
- Odsetek błędów parsowania tool calli i odsetek wyników zgodnych ze schematem.
- Odsetek zaliczonych zadań z ewaluacji.
- Opóźnienie p50 i p95 oraz czas do pierwszego tokena.
- Tokeny wyjścia na zadanie, co wyłapuje dryf rozwlekłości po cichej aktualizacji modelu.
- Współczynnik trafień cache z `usage`. Jeśli spada, rachunek rośnie od 3 do 7 razy.
- Koszt na zadanie.
- Zwrócone pole `model` (i `provider` na OpenRouter) w porównaniu z tym, co przypiąłem.

**Moje progi alertów:**

| Sygnał | Alert, gdy | Typowa przyczyna |
|---|---|---|
| Odsetek 429 | powyżej 10% w ciągu 15 minut | wyczerpana kwota albo inny najemca we współdzielonej darmowej puli |
| 5xx lub timeouty | powyżej 2% | problemy hosta, kolejkowanie w NVIDIA, „maximum capacity” (maksymalne obciążenie) w Chutes |
| 400 | jakikolwiek wzrost po zmianie | brak echa rozumowania, nieobsługiwany parametr |
| 402 | każdy | osiągnięty budżet lub ujemne saldo (OpenRouter zwraca 402 nawet przy darmowych modelach) |
| 403 | każdy | kwota lub współbieżność w Kimi Code, weryfikacja karty w Vercel |
| Specyficzne dla dostawcy | każdy | Groq 498 `capacity_exceeded` (Flex); Z.ai 1113 „Insufficient balance” (niewystarczające saldo; zły endpoint) |
| Błędy parsowania narzędzi | powyżej 2% na 100 wywołań | zmiana hosta albo skwantyzowany endpoint |
| Tokeny wyjścia na zadanie | +50% tydzień do tygodnia | model podmieniony za aliasem |

**Wyłączniki awaryjne.** Każdą grupę można wyłączyć bez deployu. Usuwam deployment przez admin API LiteLLM albo
komentuję go i przeładowuję konfigurację. Fallback, któremu już nie ufam, usuwam, a nie tylko ignoruję. Każdy klucz
dostawcy da się unieważnić osobno, więc jeden wyciek nie kładzie reszty.

**Rytm ponownych kontroli:**

- **Co miesiąc**, dla każdej trasy, której używam: test akceptacyjny i mój zestaw ewaluacyjny, dane `/endpoints`
  z OpenRouter (kwantyzacja, uptime, cena), strony z wycofaniami modeli (Groq, Cerebras, Nebius, changelog Fireworks)
  i warunki dotyczące danych.
- **Co tydzień**, dla darmowych promocji: darmowy Step 5 Preview, lista darmowych modeli OpenRouter, OpenCode Zen.
- **Daty, które już mam w kalendarzu:**
  - Otwarte wagi Step 5 Preview: zapowiedziane na 15.10.2026.
  - Poolside Laguna S 2.1 za darmo w Vercel: wycofanie 31.10.2026.
  - GLM-5.2 w Mistral: wycofanie 31.10.2026.
  - Cena Gemini 3.8 Flash: od 1.01.2027 podwaja się do USD 1,50 / 7,50.
  - Mistral Large 4: zniżka premierowa (około dwóch tygodni od 6.10.2026) wkrótce się kończy.
- **Świeże przypomnienia, dlaczego to ważne:** Fireworks podniósł cenę V4.1-Flash 1.10.2026, a LLM7 obciął swoją
  darmową kwotę 7.10.2026. Hugging Face usunął darmowe kredyty 7.10.2026, a Mistral tego samego dnia wycofał
  deklarowany darmowy kredyt.

**Wszystko w tym pliku się zmienia. Zanim znów zaufam liczbom i testom, przeliczam je i uruchamiam ponownie.**

**Źródła:** [Limity OpenRouter](https://openrouter.ai/docs/api/reference/limits) · [Routing dostawców w OpenRouter](https://openrouter.ai/docs/guides/routing/provider-selection) ·
[Cennik OpenRouter](https://openrouter.ai/pricing) · [API modeli OpenRouter](https://openrouter.ai/api/v1/models) · [Zbieranie danych w OpenRouter](https://openrouter.ai/docs/guides/privacy/data-collection) ·
[OpenRouter Auto Exacto](https://openrouter.ai/blog/announcements/auto-exacto/) · [TrueFoundry o darmowych modelach OR](https://www.truefoundry.com/blog/openrouter-free-models-whats-actually-free-and-what-it-costs-you) ·
[Tracker darmowych modeli OR](https://github.com/cyclez2000/openrouter-free-models/issues/82) · [Cennik Vercel AI Gateway](https://vercel.com/docs/ai-gateway/pricing) ·
[Cennik Requesty](https://www.requesty.ai/pricing) · [Quickstart Requesty](https://docs.requesty.ai/quickstart) · [Dokumentacja Kilo Gateway](https://kilo.ai/docs/gateway) ·
[Modele Kilo Gateway](https://api.kilo.ai/api/gateway/models) · [Dokumentacja OpenCode Zen](https://opencode.ai/docs/zen/) · [Limity zapytań Puter](https://docs.puter.com/rate-limits-and-quotas/) ·
[Limity LLM7](https://docs.llm7.io/limits.md) · [Limity zapytań Gemini](https://ai.google.dev/gemini-api/docs/rate-limits) · [Cennik Gemini](https://ai.google.dev/gemini-api/docs/pricing) ·
[Warunki Gemini API](https://ai.google.dev/gemini-api/terms) · [Pomiar darmowego tieru Gemini](https://dev.to/romeroyang/geminis-free-tier-measured-20-requests-a-day-and-google-no-longer-publishes-the-number-4gf2) ·
[Blokady kont Antigravity](https://preuve.ai/blog/antigravity-review) · [Test darmowego API NVIDIA](https://dev.to/klukyanov/kimi-k3-deepseek-and-glm-free-from-nvidia-i-tested-the-claim-and-here-is-the-catch-2m9b) ·
[Timeouty na forum NVIDIA](https://forums.developer.nvidia.com/t/all-new-model-are-timeout/368931) · [Podsumowanie warunków trialu NVIDIA](https://standardcompute.com/providers/nvidia) ·
[Cennik Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/platform/pricing/) · [Darmowa kwota Alibaba](https://www.alibabacloud.com/help/en/model-studio/new-free-quota) ·
[Limity zapytań Groq](https://console.groq.com/docs/rate-limits) · [Wycofania modeli Groq](https://console.groq.com/docs/deprecations) · [Wątek Groq o narzędziach gpt-oss](https://community.groq.com/t/gpt-oss-120b-ignoring-tools/385) ·
[Limity zapytań Cerebras](https://inference-docs.cerebras.ai/support/rate-limits) · [Ograniczenia gpt-oss w Cerebras](https://inference-docs.cerebras.ai/models/openai-oss) ·
[Modele SambaNova](https://docs.sambanova.ai/cloud/docs/get-started/supported-models) · [Cennik DeepSeek](https://api-docs.deepseek.com/quick_start/pricing) ·
[Limit zapytań DeepSeek](https://api-docs.deepseek.com/quick_start/rate_limit) · [Interpretacja polityki danych DeepSeek](https://meetily.ai/llm-privacy/deepseek) · [Cennik Z.ai](https://docs.z.ai/guides/overview/pricing) ·
[Przegląd GLM Coding Plan](https://docs.z.ai/devpack/overview.md) · [Zasady użytkowania GLM Coding Plan](https://docs.z.ai/devpack/usage-policy) · [Podsumowanie DPA Z.ai](https://standardcompute.com/providers/z-ai) ·
[Dokumentacja Kimi Code](https://www.kimi.com/code/docs/en/) · [Błędy Kimi Code](https://www.kimi.com/code/docs/en/kimi-code/error-reference.html) · [Polityka danych Kimi](https://www.cometapi.com/is-kimi-safe-to-use/) ·
[Alibaba Coding Plan](https://www.alibabacloud.com/help/en/model-studio/coding-plan) · [MiMo Token Plan](https://mimo.mi.com/docs/en-US/tokenplan/Token%20Plan/subscription) ·
[Echo rozumowania MiMo](https://kingy.ai/blog/mimo-v2-6-pro-free-access-pricing-setup/) · [Cennik MiMo](https://www.eesel.ai/blog/xiaomi-mimo-v2-6-pricing) · [FAQ MiniMax M Plan](https://platform.minimax.io/docs/m-plan/faq.md) ·
[Cennik StepFun](https://platform.stepfun.ai/docs/en/guides/pricing/details) · [Post o StepFun Step Plan](https://x.com/StepFun_ai/status/2035815197584023835) · [Cennik Ollama](https://ollama.com/pricing) ·
[API Mistral tylko dla firm](https://agentdeals.dev/vendor/mistral-ai) · [Fireworks Fire Pass](https://docs.fireworks.ai/firepass) · [Changelog Fireworks](https://docs.fireworks.ai/updates/changelog) ·
[Limity zapytań DeepInfra](https://docs.deepinfra.com/account/rate-limits) · [Prywatność danych w DeepInfra](https://docs.deepinfra.com/account/data-privacy) · [Together ZDR](https://docs.together.ai/docs/zero-data-retention) ·
[Changelog Together](https://docs.together.ai/docs/changelog) · [Publiczny serverless Nebius](https://docs.tokenfactory.nebius.com/public-serverless.md) ·
[Obsługiwane modele Scaleway](https://raw.githubusercontent.com/scaleway/docs-content/main/pages/generative-apis/reference-content/supported-models.mdx) ·
[Recenzja SiliconFlow](https://dev.to/gretavolkov/siliconflow-api-review-2026-setup-models-and-real-pricing-1gdo) · [AA Endpoint Accuracy Index](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) ·
[Dostawcy GLM-5.2 w AA](https://artificialanalysis.ai/models/glm-5-2/providers) · [Dostawcy gpt-oss-120b w AA](https://artificialanalysis.ai/models/gpt-oss-120b/providers) ·
[openbenchmarks: dokładność tego samego modelu](https://openbenchmarks.com/inference/same-model-different-accuracy) · [K2 Vendor Verifier](https://github.com/MoonshotAI/K2-Vendor-Verifier) ·
[Ranking AA v4.3.2](https://artificialanalysis.ai/leaderboards/models) · [AA V4.1-Flash](https://artificialanalysis.ai/models/deepseek-v4-1-flash) · [AA GLM-5.3-Flash](https://artificialanalysis.ai/models/glm-5-3-flash) ·
[AA MiMo-V2.6-Pro](https://artificialanalysis.ai/models/mimo-v2-6-pro) · [Publikacja DeepSeek-V4.1-Flash](https://arxiv.org/pdf/2609.19969) · [Karta HF V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) ·
[HF GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash) · [Ranking tbench.ai](https://www.tbench.ai/leaderboard) · [computingforgeeks GPT-6 Luna](https://computingforgeeks.com/gpt-6-sol-luna-released-features-benchmarks/)
