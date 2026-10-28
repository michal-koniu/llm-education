# 04 · Jak rozmawiać z szybkim modelem — przeglądarka, terminal, aplikacje agentowe

Po wdrożeniu ([02](02-WDROZENIE-DEEPSEEK.md)) model dostępny jest pod tą samą nazwą co wcześniej (`deepseek`, `deepseek-v4`, `deepseek-v4-flash-0731`…),
więc **żaden klient nie wymaga zmian** — tylko działa szybciej. Wszystko przechodzi przez `llama-swap` (port 8080), który wystawia API zgodne z OpenAI.

> **Zweryfikowane vs. niezweryfikowane.** Sprawdziłem: dostępność interfejsów poniżej, strumieniowanie, wywołanie narzędzia przez `/v1/chat/completions`,
> działanie klienta `dschat.py`. **Nie uruchomiłem** OpenClaw ani innego agenta na tym modelu — sekcja o nim to wnioski z moich pomiarów i z przeglądu
> [asystentów](../asystenci-ai/01-PROFILE.md#1-openclaw), nie raport z użycia.

## 1. Przeglądarka

| Adres | Co to jest |
|---|---|
| `http://<adres-maszyny>:8080/ui/` | interfejs `llama-swap`: lista modeli, logi, zakładka **Playground** (czat z wybranym modelem) |
| `http://<adres-maszyny>:8080/upstream/deepseek-v4-flash-0731/` | wbudowany interfejs `llama-server` (czat, ustawienia próbkowania) |

W Playground wybierz model `deepseek-v4-flash-0731` (lub alias `deepseek`). Co warto wiedzieć:

- **Pierwsze żądanie po bezczynności trwa ~2 minuty** — `llama-swap` zwalnia model po 10 min (`ttl: 600`), a tryb tensorowy ładuje się ~108 s. Kolejne są natychmiastowe.
  Chcesz mieć go „zawsze na gorąco”? Podnieś `ttl` w `config.yaml` (np. 3600) — kosztem VRAM zajętego przez model, gdy z niego nie korzystasz.
- Model **najpierw „myśli”** — w czacie zobaczysz fazę rozumowania, potem odpowiedź. To normalne, a te tokeny też są liczone w tok/s.
- **Prędkość, którą zobaczysz, zależy od obciążenia**: 1 agent ≈ 50 tok/s, 2 równolegle ≈ 35 każdy. Są tylko **2 sloty** — trzecie żądanie czeka w kolejce.
  Jeśli równolegle leci długi test (np. benchmark jakości), interaktywna rozmowa będzie wolniejsza.
- Sprawdziłem strumieniowanie z klienta (jak w czacie): pierwszy token po ~1–6 s, potem płynnie; na wolnej maszynie, bez konkurencji, oczekuj ~50 tok/s.

## 2. Terminal — `dschat.py`

Bez zależności (sama biblioteka standardowa Pythona), w katalogu [narzedzia/](narzedzia/README.md):

```bash
export LLAMA_SWAP_URL=http://<adres-maszyny>:8080       # z innego komputera; lokalnie domyślnie localhost:8080
python3 dschat.py                                        # interaktywnie (/reset, /think, /exit)
python3 dschat.py "Wyjaśnij, czym jest MoE, w 3 zdaniach"
echo "Streść ten tekst: ..." | python3 dschat.py -       # prompt z potoku
python3 dschat.py --no-think "Przetłumacz: ..."          # bez „myślenia” (szybciej, krócej — do prostych zadań)
python3 dschat.py --show-thinking "..."                  # pokaż też rozumowanie modelu
```

Po każdej odpowiedzi widzisz liczniki serwera, np. `[91 tokenów, 29,2 tok/s, draft 59/96, 1,0 s do 1. tokenu]` — tok/s generowania, ile tokenów draftu przyjęto,
czas do pierwszego tokenu. (Wartość 29 pochodzi z chwili, gdy GPU obsługiwało jednocześnie jeszcze dwa inne zadania.)

Bez narzędzi, samym `curl` (strumieniowo):

```bash
curl -N http://<adres-maszyny>:8080/v1/chat/completions -H 'Content-Type: application/json' -d '{
  "model": "deepseek", "stream": true, "temperature": 0.3,
  "messages": [{"role": "user", "content": "Napisz haiku o pamięci GPU."}]}'
```

**Nie uruchamiaj `llama-cli` bezpośrednio na tych samych kartach**, gdy `llama-swap` trzyma model — VRAM jest pełny. Jeśli potrzebujesz `llama-cli`, najpierw zwolnij model
w `llama-swap` (ma endpoint do zwalniania modeli — sprawdź jego dokumentację; tego nie testowałem) albo użyj innego modelu przez `llama-swap`.

## 3. Aplikacje agentowe (np. OpenClaw)

Każdy klient zgodny z OpenAI konfigurujesz tak samo:

| Ustawienie | Wartość |
|---|---|
| base URL | `http://<adres-maszyny>:8080/v1` |
| model | `deepseek` (alias) |
| klucz API | dowolny niepusty ciąg (serwer go nie sprawdza) |
| temperatura | **0–0,3** dla wywołań narzędzi i JSON (wyższa akceptacja draftu i stabilniejsze wyniki; serwerowe 1,0 to tylko domyślna) |
| okno kontekstu | **≤ ~90 000 tokenów** (slot ma 98 304) |
| `max_tokens` | duży (≥ 2000) — model „myśli” i to zjada limit; przy małym dostaniesz pustą odpowiedź |

Co z tego wynika dla agenta (wnioski z moich pomiarów, nieprzetestowane na OpenClaw):

1. **Wywołania narzędzi są dokładnie tym, co ten układ robi najlepiej**: 54–62 tok/s przy akceptacji draftu 0,8–0,95. Sprawdziłem, że `llama-server` z `--jinja` zwraca
   poprawne `tool_calls` (np. `read_file` z argumentami JSON) — w moim przeglądzie asystentów OpenClaw ostrzega, że endpoint `/v1` *Ollamy* psuje wywołania narzędzi, ale to inny serwer.
   **Przetestuj swój harness na kilku wywołaniach**, zanim mu zaufasz — to ostrzeżenie dotyczy też „cichego gubienia wywołań narzędzi” z przeglądu harnessów.
2. **Stabilny początek promptu.** Przegląd harnessów opisuje pułapkę: zmienny początek promptu (np. znacznik czasu na górze) niszczy cache promptu. Przy prefillu ~700 tok/s pudło cache'u
   na 10-tysięcznym prompcie kosztuje ~14 s za każdym razem. System prompt i definicje narzędzi trzymaj na początku i niezmienne.
3. **Dwóch agentów równolegle to optimum.** 2 sloty × ~35 tok/s = 63 tok/s razem. Trzeci agent czeka. Dla kilku subagentów lepiej je kolejkować niż odpalać naraz.
4. **Długie konteksty kosztują prefill, nie generowanie**: ten układ jest szybki w pisaniu, a ~25 % wolniejszy w czytaniu niż bez draftu. Do zadań „przeczytaj tysiące tokenów i odpowiedz jednym zdaniem”
   użyj modelu `deepseek-v4-flash-0731-nospec` (ten sam model bez draftu).
5. **Zbyt małe `max_tokens`** przy „myślącym” modelu daje pustą odpowiedź — agent może to zinterpretować jako awarię.

## 4. Bezpieczeństwo — przeczytaj, zanim podepniesz agenta

Jeśli `llama-swap` słucha na **wszystkich interfejsach bez hasła**, a modele startują z `--agent`, każdy w sieci LAN może uruchamiać polecenia powłoki na hoście: `--agent`
włącza wbudowane narzędzia `llama-server` — w tym **wykonywanie poleceń powłoki** (`exec_shell_command`) z uprawnieniami użytkownika, który uruchomił serwer. **Nie sprawdzałem**,
czy da się to w praktyce nadużyć z sieci (narzędzia są przeznaczone dla wbudowanego interfejsu WWW), ale przyjmij najgorsze: każdy, kto dosięgnie portu (domyślnie 8080), może próbować.
Zanim podłączysz agenta, który czyta niezaufane treści (poczta, strony WWW), zdecyduj: zapora ograniczająca port do jednego adresu, odwrotny proxy z uwierzytelnianiem,
albo wyłączenie `--agent` we wpisach, które go nie potrzebują. Reguły sandboxa: [kurs 1, część 7](../kurs_lokalne_modele/07-SANDBOX-BEZPIECZENSTWO-MONITORING.md).
