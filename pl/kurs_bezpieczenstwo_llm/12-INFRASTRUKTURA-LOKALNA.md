# Część 12 · Infrastruktura lokalna

**Poziom:** ⭐⭐⭐ · **Czas:** ~4 h · **Wymaga:** części 01, 02 (+ kurs 1 część 07, kurs 2 część 10) · **Daje:** inwentarz każdego nasłuchującego portu na Twoim komputerze i w Twojej sieci LAN, układ loopback + reverse proxy + uwierzytelnianie, skrypty skanujące, zweryfikowany skan przed/po

---

## 0. Problem

Części 03–11 atakowały to, co model czyta i robi. Ta część atakuje to, **na czym model działa**: serwer
inferencji, interfejs czatu, bazę wektorową, serwery MCP, GPU, komputer i sieć wokół nich.

Prawie każde narzędzie w lokalnym stosie LLM powstało po to, żeby działać na laptopie w pięć minut. To znaczy:
**bez logowania, zwykły HTTP, jeden proces, któremu wolno wszystko, i numer portu.** Nic z tego nie jest błędem
na `127.0.0.1`. Wszystko staje się błędem w chwili, gdy do portu może dotrzeć ktoś, kogo nie chciałeś wpuścić:
reszta Twojej sieci LAN, gość w Twoim Wi-Fi, kontener w tej samej sieci Dockera albo **strona WWW otwarta
w Twojej własnej przeglądarce**.

Dwa fakty wyznaczają ramy tej części:

1. Serwer inferencji bez uwierzytelniania daje obcemu **Twoje GPU, Twój model i Twój rachunek za prąd**, a często
   także wgląd w to, o co pytają inni ludzie. Żadne sztuczki z prompt injection nie są do tego potrzebne.
2. Najczęściej wykorzystywane błędy w tym ekosystemie to nie sprytne ataki na model. To **brak uwierzytelniania,
   usługa przypięta do wszystkich interfejsów i parser, który ufa temu, co pobrał** — te same trzy błędy, które
   miał internet w 2005 roku.

⭐ **Teza tej części: osiągalność to pierwsza kontrola bezpieczeństwa.** Najpierw zdecyduj, kto może wysłać
pakiet do każdego portu, potem dodaj uwierzytelnianie, potem pilnuj aktualizacji. Napiszesz trzy małe skrypty,
zrobisz inwentarz **własnego** komputera, zamkniesz to, co nie powinno być otwarte, i udowodnisz to skanem przed/po.

**Zakres i bezpieczeństwo.** Każde polecenie w tej części dotyka tylko `127.0.0.1` i maszyn, **które posiadasz
w swojej sieci LAN**. Skrypty odmawiają publicznych adresów (sprawdzają to i kończą działanie). Nie kieruj
skanera na nic, czego nie posiadasz: w najlepszym razie to nieuprzejme, w najgorszym nielegalne, a nic tutaj tego
nie wymaga. Przykłady używają zakresu dokumentacyjnego `192.0.2.0/24`; podstaw własny.

---

## 1. Pojęcia i mapy

**Listener (nasłuchujący).** Proces, który wywołał `listen()` na adresie i porcie. To *adres* decyduje, kto może
się połączyć:

| Przypięty do | Kto może się połączyć | Typowe znaczenie |
| :-- | :-- | :-- |
| `127.0.0.1` / `::1` (loopback) | tylko procesy na tym komputerze (i **strony WWW w przeglądarce tego komputera**, zob. §4) | bezpieczna wartość domyślna |
| adres LAN (np. `192.0.2.10`) | każdy, kto ma trasę do tego adresu | „chcę, żeby telefon z tego korzystał” |
| `0.0.0.0` / `::` (wszystkie interfejsy) | wszystkie interfejsy naraz: LAN, Wi-Fi, VPN, mosty Dockera i internet, jeśli router lub zapora chmurowa na to pozwala | „po prostu działa” — i zwykła przyczyna wystawienia na świat |

**Stos jako powierzchnia ataku.** Każdy wiersz to coś, co możesz uruchamiać. Kolumna „domyślna postawa” opisuje to,
co projekt dostarcza; sprawdź swoją wersję, domyślne wartości się zmieniają.

| Składnik | Typowy port | Domyślna postawa (sprawdź!) | Co dostaje nieuwierzytelniony rozmówca |
| :-- | :-- | :-- | :-- |
| llama-server (llama.cpp) | 8080 | przypięty do `127.0.0.1`; uwierzytelnianie tylko jeśli podasz `--api-key` / `--api-key-file` | darmową inferencję, informacje o modelu, w niektórych wersjach/flagach także `/props`, `/slots`, `/metrics` |
| Ollama | 11434 | przypięta do `127.0.0.1`; **w ogóle nie ma funkcji uwierzytelniania** | inferencję, listowanie/pobieranie/usuwanie modeli, informacje o działających modelach |
| vLLM, TGI i inne serwery zgodne z OpenAI | 8000, … | różnie; zwykle klucz opcjonalny | to samo co llama-server |
| Open WebUI i podobne interfejsy czatu | 3000 / 8080 | ma konta użytkowników; pierwsze zarejestrowane konto zostaje administratorem | interfejs, zapisane czaty, połączenia z Twoimi serwerami modeli |
| Bazy wektorowe (Qdrant, Chroma, …) | 6333, 8000 | w domyślnej instalacji często bez uwierzytelniania | **Twój korpus RAG** (część 11): odczyt, zatrucie (część 06), usunięcie |
| Serwery i inspektory MCP | różnie | lokalne stdio albo lokalny port HTTP | wszystkie narzędzia, które wystawiają (część 08) |
| Ray / klastry obliczeniowe | 8265, 6379 | dashboard i API zadań bez uwierzytelniania z założenia | dowolny kod na każdym workerze (§3, ShadowRay) |
| `rpc-server` z llama.cpp | 50052 | bez uwierzytelniania, ufa wywołującemu bez reszty | użycie GPU i pamięci hosta |
| Jupyter, Gradio, doraźne dashboardy | 8888, 7860 | token albo brak | wykonanie kodu (Jupyter) lub aplikacja demo |

Mapą tej części jest więc **tabela, którą wypełniasz dla własnego komputera** (§6.1). OWASP LLM Top 10 tego nie
obejmuje, bo to klasyczne bezpieczeństwo infrastruktury; najbliższe są pozycje łańcucha dostaw (LLM03, część 10)
oraz całe myślenie o „środowisku wykonania” z NIST i MITRE ATLAS. Liczy się tu coś starszego i prostszego:
**minimalna ekspozycja, uwierzytelnianie wszystkiego, co osiągalne, aktualizacje.**

```
                        internet
                           │   (router / zapora w chmurze: kto może wejść?)
        ┌──────────────────┴───────────────────────────────────────┐
        │  LAN / Wi-Fi  ── cudze urządzenia, goście, IoT            │
        │        │                                                  │
        │  ┌─────┴───────── Twój komputer ────────────────────┐    │
        │  │  reverse proxy :443  (TLS + auth + limity + log)  │◄───┼── JEDYNA rzecz na adresie innym niż loopback
        │  │        │                                          │    │
        │  │  ┌─────┴─ loopback 127.0.0.1 ───────────────┐     │    │
        │  │  │ llama-server  UI czatu  baza wekt.  MCP …│◄────┼────┼── Twoja przeglądarka: strona WWW też tu dotrze (§4)
        │  │  └──────────────────────────────────────────┘     │    │
        │  └───────────────────────────────────────────────────┘    │
        └───────────────────────────────────────────────────────────┘
```

---

## 2. Wystawione serwery inferencji

### 2.1 · Ile kosztuje „wystawiony”

Serwer inferencji bez uwierzytelniania to otwarte GPU. Co może z nim zrobić obcy, w kolejności prawdopodobieństwa:
uruchomić własne obliczenia na Twoim sprzęcie (darmowa moc i Twój prąd); odczytać Twój prompt systemowy
i konfigurację przez wszelkie endpointy stanu, jakie serwer ma; zalać go tak, że Twoje własne użycie ustanie
(część 09, nieograniczona konsumpcja); a na serwerach z API zarządzania — załadować lub usunąć modele. Jeśli Twoja
aplikacja obsługuje też innych ludzi (część 11), obcy może także **zobaczyć, o co pytają inni**, bo większość
tych serwerów nie zna pojęcia „użytkownik”.

### 2.2 · W prawdziwym świecie

- **Cisco**, skanując internet we **wrześniu 2025**, znalazło **1139 wystawionych serwerów Ollama** (pomiar Cisco).
- **SentinelOne i Censys**, **styczeń 2026**, podały około **175 000 hostów** wystawiających Ollamę (ich pomiar).

Te dwie liczby różnią się o ponad dwa rzędy wielkości. Nie sprawdzałem, jak każdy zespół zdefiniował „wystawiony”
ani jak sondował, więc **nie porównuj ich jako trendu**; weź to, co oba mówią: to nie jest rzadkie, a skanery
obejmujące cały internet znajdują takie usługi w ciągu godzin. (Źródła w [`ZRODLA.md`](ZRODLA.md).)

Dwie wartości domyślne pogarszają sprawę:

- **Ollama nie ma funkcji uwierzytelniania.** Domyślnie przypina się do `127.0.0.1`, a udokumentowany sposób
  dostępu z zewnątrz to ustawienie `OLLAMA_HOST=0.0.0.0`, które publikuje API niezdolne poprosić o hasło. Jeśli
  potrzebujesz zdalnego dostępu, *jedynym* projektem jest reverse proxy (§5.2) przed serwerem przypiętym do loopbacka.
- **llama-server domyślnie przypina się do `127.0.0.1` i obsługuje `--api-key` / `--api-key-file`.** To dobra
  wartość domyślna i użyteczny zamek. Zostają dwie pułapki: ktoś dodaje `--host 0.0.0.0` „tylko do jednego testu”
  i zapomina, a `--api-key KEY` wkłada klucz na listę procesów, gdzie czyta go każdy lokalny użytkownik (użyj
  `--api-key-file` i `chmod 600`, §5.5).

### 2.3 · Docker publikuje porty na każdym interfejsie

⚠️ `docker run -p 8080:8080 …` przypina się do **`0.0.0.0:8080`** na hoście. Docker zapisuje też własne reguły
filtrowania pakietów *przed* tymi, którymi zarządza nakładka zapory hosta (`ufw`, `firewalld`), więc port
„zamknięty” w `ufw` może nadal być osiągalny. Poprawka to jedno słowo we fladze publikacji:

```bash
docker run -p 127.0.0.1:8080:8080 …       # tylko loopback; proxy na hoście to drzwi frontowe
```

W Compose: `ports: ["127.0.0.1:8080:8080"]`. Sprawdź wynik skryptem inwentarza z §6.1, a nie czytając plik.
To samo dotyczy kontenera z interfejsem czatu, bazy wektorowej i wszystkiego z linią `ports:`.

---

## 3. Błędy w stosie (publiczne, załatane)

Tylko publiczne, **załatane** problemy, z wersją naprawioną i lekcją; żadnych kroków eksploatacji. Każdy to
przykład *klasy* błędu, którą spotkasz ponownie. Zaktualizuj przynajmniej do pokazanej wersji i przeczytaj
poradnik producenta.

| CVE | Produkt | Rodzaj błędu | Naprawiony w | Lekcja |
| :-- | :-- | :-- | :-- | :-- |
| **CVE-2024-37032** („Probllama”, Wiz, 2024) | Ollama | path traversal w ścieżce pobierania modelu (dane z rejestru użyte do zbudowania ścieżek plików), możliwy do wywołania przez nieuwierzytelnione API | 0.1.34 | pobranie modelu to **parsowanie niezaufanego wejścia**, a API zarządzania bez uwierzytelniania pozwala każdemu je zacząć |
| **CVE-2024-28224** (NCC Group, kwiecień 2024) | Ollama | DNS rebinding: strona WWW mogła sprawić, by przeglądarka rozmawiała z lokalnym API jak z tym samym originem | 0.1.29 | „nasłuchuje na localhost” nie znaczy „nieosiągalne z internetu” (§4) |
| **CVE-2026-7482** („Bleeding Llama”, Cyera, maj 2026) | Ollama | ujawnienie pamięci (pamięć serwera wycieka do zdalnego wywołującego) | 0.17.1 | serwer trzymający w pamięci prompty innych użytkowników zamienia każdy błąd pamięci w incydent prywatności (część 11) |
| **CVE-2025-64496** (Open WebUI „Direct Connections”) | Open WebUI | interfejs ufał serwerowi modelu, z którym go połączysz, więc wrogi *endpoint modelu* mógł zaatakować interfejs | 0.6.35 | endpoint modelu to **wejście**, a nie zaufany back-end: łącz tylko z serwerami, które kontrolujesz |
| **CVE-2025-49596** (Oligo, 2025) | MCP Inspector | narzędzie deweloperskie z lokalnym proxy i bez uwierzytelniania; strona WWW w przeglądarce mogła je sterować | 0.14.1 | lokalne narzędzia deweloperskie to też usługi; przeglądarka + localhost + brak uwierzytelniania to kompletna ścieżka ataku (§4) |
| **CVE-2024-0132** | NVIDIA Container Toolkit | ucieczka z kontenera typu time-of-check/time-of-use | 1.16.2 | narzędzia GPU działają z uprawnieniami hosta: **kontener z dostępem do GPU nie jest piaskownicą, dopóki toolkit nie jest załatany** |
| **CVE-2025-23266** („NVIDIAScape”, Wiz, lipiec 2025) | NVIDIA Container Toolkit | kolejny błąd ucieczki z kontenera w tej samej warstwie | 1.17.8 | to samo: ucieczka jest w warstwie klejącej, nie w Twoim kodzie |
| **CVE-2023-48022** (Ray; „ShadowRay”, 2024) | Ray | API zadań uruchamia kod dla każdego wywołującego; producent kwestionuje to jako podatność (z założenia, bez łatki) | brak (sporne) | funkcja „z założenia” nadal jest Twoją ekspozycją: klaster w sieci prywatnej i za uwierzytelnianiem |
| **CVE-2023-4969** („LeftoverLocals”, Trail of Bits, styczeń 2024) | sterowniki GPU (zgłoszone: Apple, AMD, Qualcomm, Imagination) | pamięć lokalna GPU niczyszczona między kernelami | aktualizacje sterowników producentów | **GPU współdzielone między użytkownikami może przeciekać dane między nimi**; na maszynie wieloużytkownikowej izolacja procesów nie obejmuje GPU |

Po ShadowRay przyszedł **ShadowRay 2.0** (Oligo, listopad 2025): ta sama klasa, znów wystawione klastry, znów
nadużyte. Jedno zdanie obejmuje całą tabelę: *niebezpieczne błędy mieszkają w warstwach wokół modelu i znajdują je
ludzie skanujący internet, a nie ludzie badający prompty.*

⚠️ Nie podaję wersji dla LeftoverLocals, bo poprawka jest w sterowniku każdego producenta; sprawdź poradnik
producenta własnego GPU.

---

## 4. Przeglądarka jest mostem do Twojego loopbacka

„Przypięty do `127.0.0.1`” chroni przed innymi maszynami. **Nie** chroni przed stroną otwartą w Twojej własnej
przeglądarce, bo przeglądarka działa na Twoim komputerze i może wysyłać żądania do `127.0.0.1`.

### 4.1 · Co CORS robi, a czego nie

Polityka same-origin przeglądarki decyduje, co strona może **przeczytać**. CORS to sposób, w jaki serwer ją
rozluźnia. Reguły, które mają znaczenie:

- Strona z `https://evil.example` może **wysłać** „proste” żądanie (np. `POST` z `Content-Type: text/plain`) do
  `http://127.0.0.1:8080/...` **bez preflightu**. Serwer je przetwarza. Strona tylko nie może przeczytać odpowiedzi.
- Dla `POST` z JSON przeglądarka najpierw wysyła preflight (`OPTIONS`). Serwer, który odpowie na niego
  liberalnymi nagłówkami CORS, oddaje stronie także odpowiedź.

Zatem „odpowiedź zablokował CORS” znaczy: *serwer i tak wykonał pracę.* Dla nieuwierzytelnionego API zmieniającego
stan (załaduj model, wyślij prompt wywołujący narzędzie) atakiem jest **efekt uboczny**, którego CORS nigdy nie widzi.

### 4.2 · DNS rebinding

Strona atakującego ładuje się z `rebind.example`. Po jej załadowaniu serwer DNS atakującego zmienia odpowiedź dla
`rebind.example` na `127.0.0.1`. Następne żądanie przeglądarki do `rebind.example` trafia do **Twojego** lokalnego
serwera, a ponieważ origin nadal brzmi `rebind.example`, polityka same-origin **pozwala teraz stronie czytać
odpowiedzi.** Serwer widzi żądanie z `Host: rebind.example`.

⭐ **Obrona jest po stronie serwera: sprawdzaj nagłówek `Host` względem listy dozwolonych** (`127.0.0.1:PORT`,
`localhost:PORT`, Twoja prawdziwa nazwa hosta) i resztę odrzucaj kodem `421`. Klucz w nagłówku `Authorization`
też to zatrzymuje, bo obca strona go nie ma. Zrób jedno i drugie. Dokładnie o tym był CVE-2024-28224 (Ollama).

### 4.3 · Przeglądarka zaczyna pomagać

**Local Network Access** w Chrome (ogłoszone w czerwcu 2025; opt-in od Chrome 138) sprawia, że przeglądarka pyta
użytkownika, zanim publiczna strona może sięgnąć do adresów prywatnych. Dobrze, ale to **pas bezpieczeństwa, nie
zamek**: zależy od przeglądarki i wersji, od tego, czy użytkownik kliknie właściwy przycisk, i nie chroni przed
Twoimi innymi procesami ani innymi przeglądarkami. Traktuj to jako obronę w głąb, nigdy jako kontrolę.

### 4.4 · Dlaczego strona może znaleźć Twój port

Skanowanie `127.0.0.1:1…65535` ze strony WWW jest wolne, ale możliwe; strony próbują najpierw znanych portów
(11434, 8080, 3000, 6333, 8000, 8265). **Domyślne porty są publiczną wiedzą**, więc przeniesienie na „tajny”
port nie jest kontrolą; skraca tylko listę linii w logu.

---

## 5. Układ, do którego dążysz

```
 klient ──TLS──▶ reverse proxy ──zwykły HTTP──▶ llama-server (127.0.0.1)
                 · TLS            · klucz bearer           · osiągalny tylko z proxy
                 · klucz per klient · limit rozmiaru treści · klucz niepotrzebny (albo taki, który dodaje proxy)
                 · limit żądań    · log żądań
```

### 5.1 · Zawsze przypinaj do loopbacka

Każdy back-end dostaje adres loopback (`--host 127.0.0.1`, `OLLAMA_HOST=127.0.0.1`, `-p 127.0.0.1:…`). Dokładnie
jedna rzecz może nasłuchiwać na adresie innym niż loopback: reverse proxy. Jeśli back-end musi być na innej
maszynie niż jego proxy, użyj sieci prywatnej albo tunelu SSH/WireGuard i nadal przypnij go **tylko** do adresu tunelu.

### 5.2 · Reverse proxy z przodu

Proxy dodaje w jednym miejscu to, czego brakuje back-endom: TLS, uwierzytelnianie, limity rozmiaru żądań, limity
częstości i log dostępu. W Caddy to kilkanaście linii (`deploy/Caddyfile`):

```
# Caddy 2: TLS + klucz bearer + limit treści przed llama-server na 127.0.0.1:8080.
# Start:  LLM_PROXY_KEY=$(cat ~/llm.key) caddy run --config deploy/Caddyfile
llm.example.test {
	tls internal                      # lokalne CA Caddy; w produkcji użyj prawdziwego certyfikatu
	@denied not header Authorization "Bearer {$LLM_PROXY_KEY}"
	respond @denied 401
	request_body {
		max_size 1MB
	}
	reverse_proxy 127.0.0.1:8080
}
```

`tls internal` używa lokalnego urzędu certyfikacji samego Caddy (dobre dla sieci domowej lub laboratoryjnej:
instalujesz ten certyfikat główny na swoich urządzeniach raz). Matcher `@denied` odrzuca kodem `401` każde żądanie
bez właściwego klucza bearer, `request_body` ogranicza treść, a `reverse_proxy` przekazuje resztę. Za nim
llama-server nie potrzebuje własnego klucza, ale dodanie `--api-key-file` to darmowa obrona w głąb. nginx i Traefik
robią tę samą robotę; wybór nie ma znaczenia, znaczenie ma **topologia**.

⚠️ Jeden wspólny klucz dla wszystkich jest lepszy niż żaden i gorszy niż klucz na klienta: nie odwołasz jednej
osoby, a log nie powie, kto co zrobił. §5.6 omawia klucze per użytkownik. Ten Caddyfile sprawdziłem poleceniem
`caddy validate` i uruchomiłem w jednorazowym kontenerze przed atrapą upstreamu: brak klucza dawał `401`, zły klucz
`401`, dobry klucz `200`, treść 1,2 MB `413`. Zrób to samo u siebie, zaczynając od `caddy validate`.

### 5.3 · Segmentacja i ruch wychodzący

- **Umieść host inferencji w segmencie sieci** (VLAN albo przynajmniej zestaw reguł zapory), do którego nie
  sięgają Twoje telefony, telewizory i goście i który może wychodzić tylko tam, gdzie musi.
- **Kontroluj ruch wychodzący (egress).** Host modelu, który sięga całego internetu, to ścieżka eksfiltracji
  (część 07) i ścieżka dowodzenia i kontroli, jeśli cokolwiek na nim zostanie kiedyś skompromitowane. Jeśli host
  musi tylko pobierać modele z jednego miejsca, zezwól na to i na nic więcej, a pobieranie modeli rób świadomie
  (część 10), nie z procesu serwującego.
- Nazwij jawnie trzy przepływy: *kto może wołać proxy*, *co może wołać proxy*, *co mogą wołać back-endy*. Wszystko
  spoza listy jest zabronione. Ostatnią pozycję ludzie zapominają.

### 5.4 · Kontenery i dostęp do GPU

Kontener to wygodna granica, nie piaskownica, chyba że skonfigurujesz go jak piaskownicę. Dla kontenera serwującego:

```bash
MODELS=~/models                    # folder z Twoimi plikami .gguf
IMAGE=your-llama-server-image      # wybrany obraz serwera llama.cpp; przypnij go po digeście
# Poniżej urządzenia AMD ROCm; dla NVIDIA usuń oba --device i dodaj --gpus device=0
docker run --rm \
  -p 127.0.0.1:8080:8080 \
  --cap-drop ALL --security-opt no-new-privileges \
  --read-only --tmpfs /tmp \
  -v "$MODELS":/models:ro \
  --device /dev/kfd --device /dev/dri \
  "$IMAGE" -m /models/your-model.gguf --host 0.0.0.0 --port 8080
```

(`--host 0.0.0.0` to adres **wewnątrz** kontenera, jedyny, na który Docker potrafi przekierować; przed Twoją siecią
LAN serwer chroni `127.0.0.1:` we fladze publikacji.)

Co daje każdy wybór: `127.0.0.1` we fladze publikacji (§2.3); brak uprawnień (capabilities) i brak eskalacji
uprawnień; system plików tylko do odczytu i wolumen modeli tylko do odczytu (przejęty serwer nie przepisze modelu,
część 10); oraz **tylko te węzły urządzeń GPU, których potrzebuje.** Nigdy `--privileged`, nigdy nie montuj gniazda
Dockera (`/var/run/docker.sock`) do kontenera i nigdy nie montuj swojego katalogu domowego. Pamiętaj o §3: sama
ścieżka GPU to powierzchnia ataku (CVE toolkitu NVIDIA, LeftoverLocals), więc aktualizuj sterowniki i toolkit
i nie dziel jednego GPU między użytkowników, którzy sobie wzajemnie nie ufają. Piaskownica dla kodu, który pisze
model, jest w kursie 1 części 07 i kursie 2 części 10: to inny, surowszy kontener.

### 5.5 · Sekrety

- Klucze w **pliku** z trybem `600` (`--api-key-file`, sekret Dockera/Compose, poświadczenie systemd), nie
  w wierszach poleceń (widoczne dla każdego lokalnego użytkownika na liście procesów) i nie w zmiennych
  środowiskowych długo żyjącej powłoki.
- Nigdy w obrazie, nigdy w gicie, nigdy w historii czatu, którą widzi model (część 05: cokolwiek jest w prompcie,
  użytkownik może przeczytać).
- Jeden klucz na klienta i na cel; rotuj według harmonogramu i natychmiast po każdej wątpliwości. Część 14 ma
  kroki rotacji na wypadek incydentu.
- Klucz modelu u dostawcy, który trzyma proxy, **nie** jest przekazywany klientom: zob. komentarz w
  `infra/auth_proxy.py`.

### 5.6 · Więcej niż jeden użytkownik

Gdy Twojej aplikacji używają inni: uwierzytelniaj **każdego użytkownika** (klucz albo login na osobę), loguj, kto
co wołał (część 14, z redakcją), ograniczaj częstość per klucz (część 09) i przeczytaj ponownie część 11 o
współdzieleniu cache i pamięci. Własne konta interfejsu czatu to nie konta proxy: zdecyduj, które jest prawdziwą
granicą, a drugie uczyń redundantnym, nie sprzecznym. Interfejsy w stylu Open WebUI często czynią *pierwsze
zarejestrowane konto administratorem*: zarejestruj swoje, zanim zrobi to ktokolwiek inny, i wyłącz otwartą
rejestrację.

### 5.7 · Aktualizacje

Lokalny stos nie ma producenta wypychającego łatki. Każdy wiersz z §3 został naprawiony wydaniem, które ktoś musiał
zainstalować.

- **Przypinaj** wersje (tagi kontenerów po digeście, pliki lock `pip`/`npm`), żeby wiedzieć, co uruchamiasz.
- **Subskrybuj** poradniki bezpieczeństwa każdego składnika z tabeli w §1 (wystarczy „Watch → Security advisories”
  na GitHubie).
- **Zaplanuj** comiesięczny slot „zaktualizuj i powtórz skan”; dodaj aktualizację poza cyklem, gdy CVE dotyczy
  czegoś, co uruchamiasz.
- Nie aktualizuj też ślepo ścieżki serwującej: zła wersja to także zdarzenie łańcucha dostaw (część 10).
  Aktualizuj w kopii, uruchom bramkę z części 13, potem przełącz.

---

## 6. LABORATORIUM · inwentarz, sonda, skan, zamknięcie, weryfikacja

Wszystko uruchamiasz z `$SEC` (folder zawierający `lab/`). Skrypty leżą w `$SEC/infra/` i są samodzielnym Pythonem
ze standardowej biblioteki. Są tylko do odczytu, poza `auth_proxy.py` i `cors_lab.py`, które uruchamiają serwery
na loopbacku.

```bash
mkdir -p "$SEC/infra" && cd "$SEC"
```

### 6.1 · Inwentarz: każdy nasłuchujący port na tym komputerze

```bash
cat > infra/inventory.py <<'EOF'
"""Wypisuje każdy nasłuchujący port TCP na TYM komputerze i mówi, jak bardzo jest wystawiony.

Linux: używa `ss`; macOS: używa `lsof`. Tylko odczyt, niczego nie zmienia.
Usage: python3 infra/inventory.py [--json out.jsonl]
"""
import json, platform, re, subprocess, sys

KNOWN = {  # domyślne porty typowych składników stosu LLM (wskazówka, nie dowód)
    8080: "llama-server / Open WebUI (container)", 11434: "Ollama",
    8000: "vLLM / Chroma", 3000: "Open WebUI (published)", 8265: "Ray dashboard",
    6333: "Qdrant", 50052: "llama.cpp rpc-server", 7860: "Gradio",
    8888: "Jupyter", 8760: "lab UI", 8765: "lab web", 8766: "lab attacker",
}

def listeners():
    if platform.system() == "Linux":
        out = subprocess.run(["ss", "-ltnpH"], capture_output=True, text=True).stdout
        for line in out.splitlines():
            cols = line.split()
            if len(cols) < 4:
                continue
            local = cols[3]
            proc = re.search(r'users:\(\("([^"]+)"', line)
            yield local, proc.group(1) if proc else "?"
    else:  # macOS / BSD
        out = subprocess.run(["lsof", "-nP", "-iTCP", "-sTCP:LISTEN"],
                             capture_output=True, text=True).stdout
        for line in out.splitlines()[1:]:
            cols = line.split()
            if len(cols) >= 9:
                yield cols[8], cols[0]

def classify(addr: str) -> str:
    host = addr.rsplit(":", 1)[0].strip("[]")
    if host in ("127.0.0.1", "::1", "localhost") or host.startswith("127."):
        return "loopback"
    if host in ("*", "0.0.0.0", "::", ""):
        return "ALL-INTERFACES"
    return f"interface {host}"

def main():
    rows = []
    for local, proc in listeners():
        port = int(local.rsplit(":", 1)[1])
        rows.append({"addr": local, "port": port, "process": proc,
                     "exposure": classify(local), "hint": KNOWN.get(port, "")})
    rows.sort(key=lambda r: (r["exposure"] == "loopback", r["port"]))
    for r in rows:
        flag = "⚠️ " if r["exposure"] != "loopback" else "   "
        print(f"{flag}{r['addr']:<28} {r['process']:<18} {r['exposure']:<20} {r['hint']}")
    if "--json" in sys.argv:
        path = sys.argv[sys.argv.index("--json") + 1]
        with open(path, "w") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        print(f"\nsaved {len(rows)} rows to {path}")

if __name__ == "__main__":
    main()
EOF
python3 infra/inventory.py --json before.jsonl
```

Pierwsza kolumna to adres, do którego proces jest przypięty: wszystko oznaczone `ALL-INTERFACES` albo
`interface …` jest osiągalne z innych maszyn (z zastrzeżeniem Twojej zapory). Kolumna „hint” to zgadywanka po
numerze portu, nic więcej. `process` to nazwa programu; na Linuksie możesz potrzebować `sudo`, by zobaczyć procesy
innych użytkowników (`ss -p`). Na macOS skrypt używa `lsof`.

### 6.2 · Sonda: co dostałby obcy?

```bash
cat > infra/probe_llm.py <<'EOF'
"""Pyta TWOJE WŁASNE hosty, co dostałby nieuwierzytelniony obcy.

Odmawia wszystkiego, co nie jest adresem loopback ani prywatnym / dokumentacyjnym.
Usage: python3 infra/probe_llm.py 127.0.0.1 8080 11434 [--key KEY]
"""
import ipaddress, json, sys, urllib.error, urllib.request

PATHS = [  # odciski tylko do odczytu; nic tu nie zmienia stanu serwera
    "/v1/models", "/health", "/props", "/slots", "/metrics",   # llama-server
    "/api/version", "/api/tags", "/api/ps",                     # Ollama
    "/api/jobs/",                                              # Ray job API
]

def own_address(host: str) -> bool:
    ip = ipaddress.ip_address(host)
    return ip.is_loopback or ip.is_private

def get(url, headers):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=3) as r:
            return r.status, dict(r.headers), r.read(300)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), b""
    except Exception as e:  # zamknięty port, przekroczenie czasu, TLS
        return None, {}, str(e).encode()

def probe(host, port, key=None):
    base = f"http://{host}:{port}"
    auth = {"Authorization": f"Bearer {key}"} if key else {}
    found = []
    for p in PATHS:
        status, hdrs, body = get(base + p, auth)
        if status is None:
            return [("port", "closed or not HTTP")]
        if status == 200:
            found.append((p, body[:80].decode(errors="replace").replace("\n", " ")))
    # CORS: czy serwer oddaje odpowiedzi dowolnej stronie WWW?
    _, hdrs, _ = get(base + "/v1/models", {"Origin": "http://evil.example", **auth})
    acao = {k.lower(): v for k, v in hdrs.items()}.get("access-control-allow-origin")
    if acao:
        found.append(("CORS", f"Access-Control-Allow-Origin: {acao}"))
    # DNS rebinding: czy obcy nagłówek Host jest akceptowany?
    status, _, _ = get(base + "/v1/models", {"Host": "rebind.example", **auth})
    found.append(("Host check", "foreign Host ACCEPTED" if status == 200
                  else f"foreign Host refused ({status})"))
    return found

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    key = sys.argv[sys.argv.index("--key") + 1] if "--key" in sys.argv else None
    if key in args:
        args.remove(key)
    host, ports = args[0], [int(p) for p in args[1:]]
    if not own_address(host):
        sys.exit(f"refusing {host}: only loopback / private addresses (your own LAN)")
    for port in ports:
        print(f"== {host}:{port}")
        for what, detail in probe(host, port, key):
            print(f"   {what:<14} {detail}")

if __name__ == "__main__":
    main()
EOF
python3 infra/probe_llm.py 127.0.0.1 8080 11434          # z samej maszyny
python3 infra/probe_llm.py 192.0.2.10 8080 11434         # podaj adres LAN SWOJEJ maszyny
```

Druga forma to ładna sztuczka: łączenie się ze **swoim własnym adresem LAN** z tej samej maszyny testuje
*przypięcie*. Usługa przypięta tylko do `127.0.0.1` odmówi takiego połączenia; przypięta do `0.0.0.0` odpowie.
Skrypt pokazuje, które ścieżki tylko do odczytu odpowiadają bez klucza, czy serwer zwraca nagłówek
`Access-Control-Allow-Origin` dla obcego `Origin` i czy akceptuje obcy nagłówek `Host` (warunek wstępny DNS
rebindingu, §4.2). Dodaj `--key KEY`, by zobaczyć różnicę, jaką robi klucz.

### 6.3 · Przeskanuj własną sieć LAN (z drugiej własnej maszyny)

```bash
cat > infra/lan_scan.py <<'EOF'
"""Skan TCP connect TWOJEJ WŁASNEJ sieci LAN pod kątem portów stosu LLM. Stdlib, wolny, grzeczny.

Odmawia sieci nieprywatnych i czegokolwiek większego niż /24.
Usage: python3 infra/lan_scan.py 192.0.2.0/24 [--out scan.jsonl]
"""
import concurrent.futures as cf, ipaddress, json, socket, sys

PORTS = [22, 3000, 6333, 7860, 8000, 8080, 8265, 8888, 11434, 50052]

def is_open(host, port):
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0

def main():
    net = ipaddress.ip_network(sys.argv[1], strict=False)
    if not net.is_private or net.num_addresses > 256:
        sys.exit("refusing: only your own private network, at most a /24")
    jobs = [(str(h), p) for h in net.hosts() for p in PORTS]
    with cf.ThreadPoolExecutor(max_workers=32) as ex:
        hits = [j for j, ok in zip(jobs, ex.map(lambda j: is_open(*j), jobs)) if ok]
    for host, port in hits:
        print(f"{host:<16} {port}")
    if "--out" in sys.argv:
        with open(sys.argv[sys.argv.index("--out") + 1], "w") as f:
            for host, port in hits:
                f.write(json.dumps({"host": host, "port": port}) + "\n")

if __name__ == "__main__":
    main()
EOF
python3 infra/lan_scan.py 192.0.2.0/24 --out lan-before.jsonl      # TWOJA sieć, nie moja
```

To zwykłe połączenie TCP na dziesięciu dobrze znanych portach. Odmawia zakresów nieprywatnych i czegokolwiek
większego niż /24 i jest celowo wolny. Uruchom go **z innej maszyny niż ta, którą sprawdzasz** (laptop przeciw
serwerowi), bo maszyna skanująca samą siebie mówi Ci o własnej zaporze, a nie o tym, co widzi sieć. Jeśli nie masz
drugiej maszyny, pomiń ten krok i polegaj na sztuczce z własnym adresem LAN z §6.2. **Nie skanuj sieci, której
nie prowadzisz.**

### 6.4 · Ścieżka przez przeglądarkę: CORS i kontrola Host

```bash
cat > infra/cors_lab.py <<'EOF'
"""Dwa serwery na loopbacku, żeby zobaczyć, co *obca strona WWW* może zrobić lokalnemu API.

  127.0.0.1:8798  „obca” strona (inny origin = inny port)
  127.0.0.1:8799  docelowe API: loguje każde żądanie (metoda, Origin, Host, treść)
Usage: python3 infra/cors_lab.py [--strict]   potem otwórz http://127.0.0.1:8798/
(porty zajęte? CORS_PAGE_PORT=... CORS_API_PORT=... python3 infra/cors_lab.py)
--strict włącza dwie obrony: listę dozwolonych Host + token bearer.
"""
import http.server, json, os, sys, threading

STRICT = "--strict" in sys.argv
PAGE_PORT = int(os.environ.get("CORS_PAGE_PORT", "8798"))
API_PORT = int(os.environ.get("CORS_API_PORT", "8799"))
TOKEN = "lab-token-not-a-secret"
ALLOWED_HOSTS = {f"127.0.0.1:{API_PORT}", f"localhost:{API_PORT}"}

PAGE = """<!doctype html><meta charset=utf-8><title>foreign page</title>
<pre id=log></pre><script>
const T = new URLSearchParams(location.search).get("target") || "http://127.0.0.1:__API__";
const log = m => document.getElementById("log").textContent += m + "\\n";
async function tryIt(name, opts) {
  try { const r = await fetch(T + "/v1/chat/completions", opts);
        log(name + ": response READABLE, status " + r.status); }
  catch (e) { log(name + ": response blocked by the browser (" + e + ")"); }
}
tryIt("A simple POST text/plain", {method: "POST", body: '{"messages":[{"role":"user","content":"say MARKER-A"}]}'});
tryIt("B JSON POST (preflight)", {method: "POST", headers: {"Content-Type": "application/json"},
      body: '{"messages":[{"role":"user","content":"say MARKER-B"}]}'});
new Image().src = T + "/v1/models?marker=C";  log("C image GET sent");
</script>"""

class Page(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(PAGE.replace("__API__", str(API_PORT)).encode())
    def log_message(self, *a):
        pass

class Target(http.server.BaseHTTPRequestHandler):
    def _guard(self) -> bool:
        if not STRICT:
            return True
        if self.headers.get("Host") not in ALLOWED_HOSTS:
            self._reply(421, {"error": "unknown Host (DNS rebinding?)"}); return False
        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            self._reply(401, {"error": "missing token"}); return False
        return True
    def _reply(self, code, obj):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode())
    def _record(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n).decode(errors="replace") if n else ""
        print(f"[target] {self.command:<7} {self.path:<28} Origin={self.headers.get('Origin')} "
              f"Host={self.headers.get('Host')} body={body[:60]!r}", flush=True)
    def do_OPTIONS(self):          # preflight: NIE zezwalamy na obce originy
        self._record(); self.send_response(204); self.end_headers()
    def do_GET(self):
        self._record()
        if self._guard(): self._reply(200, {"data": [{"id": "local"}]})
    def do_POST(self):
        self._record()
        if self._guard(): self._reply(200, {"choices": [{"message": {"content": "ok"}}]})
    def log_message(self, *a):
        pass

def serve(port, handler):
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()

if __name__ == "__main__":
    threading.Thread(target=serve, args=(PAGE_PORT, Page), daemon=True).start()
    print(f"strict={STRICT}. Open http://127.0.0.1:{PAGE_PORT}/ in your browser. Ctrl-C to stop.")
    serve(API_PORT, Target)
EOF
python3 infra/cors_lab.py            # terminal A: otwórz http://127.0.0.1:8798/ w przeglądarce
```

Strona na porcie 8798 to *obcy origin* względem API na 8799. Wysyła trzy żądania: proste `POST` z `text/plain`,
`POST` z JSON (wymaga preflightu) i `GET` obrazka `<img>`. Porównaj to, co pokazuje **terminal** (serwer zalogował
wszystkie, z `Origin` i `Host`), z tym, co pokazuje **strona** (których odpowiedzi mogła przeczytać). Przewidywanie,
moje i niezmierzone: proste POST i GET obrazka docierają do serwera, a strona nie może przeczytać żadnej
odpowiedzi; POST z JSON wysyła tylko `OPTIONS`, na które serwer odpowiada bez nagłówków CORS, więc przeglądarka
nigdy nie wysyła właściwego żądania. Potem zatrzymaj serwer i uruchom `python3 infra/cors_lab.py --strict`: lista
dozwolonych Host i klucz bearer są włączone: te same trzy żądania nadal docierają (terminal je loguje), ale serwer
odmawia im teraz z `401` zamiast wykonywać pracę, a strona nadal nic nie czyta. Obronę przed rebindingiem udowodnisz
bez sztuczek z DNS, zmieniając nagłówek ręcznie:

```bash
curl -s -i -H "Host: rebind.example:8799" http://127.0.0.1:8799/v1/models           # 421 w trybie --strict
curl -s -i -H "Authorization: Bearer lab-token-not-a-secret" http://127.0.0.1:8799/v1/models   # 200
```

(Porty zajęte? Ustaw `CORS_PAGE_PORT` i `CORS_API_PORT`.)

### 6.5 · Malutkie proxy z uwierzytelnianiem do ćwiczeń (nie do produkcji)

```bash
cat > infra/auth_proxy.py <<'EOF'
"""Minimalny reverse proxy z uwierzytelnianiem i kontrolą Host. Narzędzie DYDAKTYCZNE: bez streamingu (buforuje
całą odpowiedź), bez HTTP/2. Na serio używaj Caddy lub nginx (sekcja 5.2).

    python3 infra/auth_proxy.py --listen 8081 --upstream http://127.0.0.1:8080
        --key-file proxy.key --host llm.example.test [--bind 127.0.0.1] [--cert c.pem --key k.pem]

Co egzekwuje: nagłówek Host z listy dozwolonych (zatrzymuje DNS rebinding), klucz bearer porównywany
w stałym czasie, ograniczony rozmiar treści, każde żądanie logowane z krótkim odciskiem klucza.
"""
import argparse
import hashlib
import hmac
import http.server
import pathlib
import ssl
import sys
import urllib.error
import urllib.request

MAX_BODY = 1_000_000


def make_handler(upstream, key, hosts):
    class H(http.server.BaseHTTPRequestHandler):
        def _reply(self, code, body=b"", ctype="application/json"):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _handle(self):
            fp = "-"
            if self.headers.get("Host", "") not in hosts:
                code = 421                                   # błędnie skierowane żądanie: zły Host
            else:
                got = self.headers.get("Authorization", "")
                if not hmac.compare_digest(got.encode(), f"Bearer {key}".encode()):
                    code = 401
                else:
                    fp = hashlib.sha256(key.encode()).hexdigest()[:6]
                    n = int(self.headers.get("Content-Length") or 0)
                    code = 413 if n > MAX_BODY else 0
            if code:
                print(f"{self.command} {self.path} -> {code} key={fp}", file=sys.stderr, flush=True)
                return self._reply(code, b'{"error": "refused by proxy"}')
            body = self.rfile.read(n) if n else None
            req = urllib.request.Request(upstream + self.path, data=body, method=self.command)
            req.add_header("Content-Type", self.headers.get("Content-Type", "application/json"))
            try:                                             # klucza upstreamu, jeśli jest, nie przekazujemy dalej
                with urllib.request.urlopen(req, timeout=300) as r:
                    code, data, ctype = r.status, r.read(), r.headers.get("Content-Type", "application/json")
            except urllib.error.HTTPError as e:
                code, data, ctype = e.code, e.read(), "application/json"
            except OSError:
                code, data, ctype = 502, b'{"error": "upstream unreachable"}', "application/json"
            print(f"{self.command} {self.path} -> {code} key={fp}", file=sys.stderr, flush=True)
            self._reply(code, data, ctype)

        do_GET = do_POST = _handle

        def log_message(self, *a):
            pass
    return H


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--listen", type=int, required=True)
    ap.add_argument("--bind", default="127.0.0.1")
    ap.add_argument("--upstream", required=True)
    ap.add_argument("--key-file", required=True)
    ap.add_argument("--host", action="append", default=[], help="allowed Host name (repeatable)")
    ap.add_argument("--cert")
    ap.add_argument("--key")
    a = ap.parse_args()
    key = pathlib.Path(a.key_file).read_text().strip()
    hosts = set()
    for h in a.host + ["127.0.0.1", "localhost"]:
        hosts.update({h, f"{h}:{a.listen}"})
    srv = http.server.ThreadingHTTPServer((a.bind, a.listen),
                                          make_handler(a.upstream.rstrip("/"), key, hosts))
    if a.cert:
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(a.cert, a.key)
        srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    print(f"proxy {a.bind}:{a.listen} -> {a.upstream}  hosts={sorted(hosts)}", file=sys.stderr)
    srv.serve_forever()


if __name__ == "__main__":
    main()
EOF
python3 -c "import secrets; print(secrets.token_urlsafe(32))" > proxy.key && chmod 600 proxy.key
python3 infra/auth_proxy.py --listen 8081 --upstream http://127.0.0.1:8080 --key-file proxy.key --host llm.example.test
```

W drugim terminalu:

```bash
python3 infra/probe_llm.py 127.0.0.1 8081                              # bez klucza: nic nie odpowiada
python3 infra/probe_llm.py 127.0.0.1 8081 --key "$(cat proxy.key)"     # z kluczem: odpowiada upstream
```

Buforuje całą odpowiedź, więc czat w streamingu nie będzie przez nie płynął; taka jest cena 90 linii stdlib.
Prawdziwe wdrożenia używają Caddyfile z §5.2. Proxy uczy trzech decyzji: lista dozwolonych Host, porównanie klucza
w stałym czasie (`hmac.compare_digest`) i limit treści. Zauważ też, czego w nim *nie ma*: TLS (daj mu
`--cert`/`--key`, jeśli kiedykolwiek wyjdzie poza loopback: klucz bearer przez zwykły HTTP w sieci LAN może
przeczytać każdy w tej sieci), kluczy per użytkownik i limitów częstości.

---

## 7. ⭐ EKSPERYMENT 12 — przed i po na Twoim komputerze

**Hipoteza.** Na Twoim komputerze jest co najmniej jeden listener bardziej wystawiony, niż musi być (kontener
publikujący na wszystkich interfejsach, serwer deweloperski przypięty do `0.0.0.0`, interfejs uruchomiony „tylko
żeby przetestować”), a po przeniesieniu każdego back-endu na loopback i postawieniu jednego uwierzytelnianego
proxy sonda od strony LAN nie znajduje nic otwartego poza proxy i nic nie odpowiada bez klucza.

**Procedura.**

1. `python3 infra/inventory.py --json before.jsonl`. Oznacz każdy wiersz jako **potrzebny / niepotrzebny** i **kto
   musi do niego sięgać** (nikt, ten komputer, urządzenie w mojej sieci LAN).
2. Dla każdego wiersza, który nie jest loopbackiem, zapisz powód. Jeśli nie umiesz, to ustalenie.
3. `python3 infra/probe_llm.py <twój-adres-LAN> <port>…` dla każdego takiego portu; zapisz wynik.
4. Z drugiej własnej maszyny: `python3 infra/lan_scan.py <twoja-podsieć> --out lan-before.jsonl`.
5. Napraw: przypnij back-endy do loopbacka; zmień flagi `-p` na `127.0.0.1:`; ustaw `--api-key-file` tam, gdzie
   jest; to, co musi być osiągalne, ukryj za proxy; wyłącz otwartą rejestrację w interfejsie.
6. Powtórz kroki 1, 3 i 4 jako `after`.
7. `diff before.jsonl after.jsonl` i `diff lan-before.jsonl lan-after.jsonl`.

**Przewidywanie** (moje, niezmierzone, dla typowego domowego labu z kontenerem UI i jednym–dwoma serwerami
inferencji): krok 1 pokaże od jednego do czterech listenerów poza loopbackiem; co najmniej jeden to port
opublikowany przez Dockera, którego nie pamiętasz; krok 3 pokaże, że co najmniej jeden odpowiada na `/v1/models`
bez klucza i akceptuje obcy `Host`; po poprawkach skan LAN pokaże tylko port proxy.

| Co | Przed | Po |
| :-- | :-- | :-- |
| Listenery poza loopbackiem (liczba) | | |
| Które i dlaczego | | |
| Porty odpowiadające bez klucza (adres LAN) | | |
| Obcy `Host` zaakceptowany (liczba) | | |
| Porty widziane przez skan LAN | | |
| Czego nie dało się zamknąć i kontrola kompensująca | | |

---

## 8. ĆWICZENIA

1. **Inwentarz innych maszyn.** Powtórz §6.1 na każdej maszynie z jakąkolwiek częścią Twojego stosu (serwer,
   laptop, komputer z GPU). Na której był listener, o którym nie wiedziałeś?
2. **Rebinding w laboratorium.** Uruchom interfejs czatu z laboratorium (`python3 -m lab.servers`, port 8760).
   Który z trzech serwerów sprawdza nagłówek `Host`? Dodaj kontrolę 421 do tego, który uważasz za najważniejszy,
   i udowodnij ją `curl -H`.
3. **Proxy dla endpointu Sieve.** Część 13 §6.4 buduje endpoint Sieve zgodny z OpenAI. Postaw przed nim
   `auth_proxy.py` i skonfiguruj narzędzia red team tak, by rozmawiały z proxy z kluczem. Co zmienia się w
   konfiguracjach narzędzi?
4. **Model zagrożeń sieci.** Narysuj swoją prawdziwą sieć jak diagram z §1 (nazwy, nie adresy) i zaznacz każdą
   granicę zaufania, którą żądanie przekracza od „Wi-Fi dla gości” do „modelu”. Które przejście nie ma żadnej kontroli?
5. **Ćwiczenie aktualizacji.** Wypisz każdy składnik stosu, wersję, którą uruchamiasz, i najnowszą. Które są więcej
   niż dwie wersje minor z tyłu i czy dotyczy ich jakiś poradnik?
6. **Egress.** Z wnętrza kontenera serwującego uruchom `curl -sI https://example.com`. Jeśli działa, zapisz, do
   czego kontener naprawdę musi sięgać, i regułę, która pozwoliłaby tylko na to.

---

## 9. Pułapki tej części

| ID | Pułapka | Objaw | Remedium |
| :-- | :-- | :-- | :-- |
| **T12.1** | `0.0.0.0` „żeby sprawdzić z telefonu”, nigdy nie cofnięte | Inwentarz pokazuje `ALL-INTERFACES` po tygodniach | Proxy plus loopback; nigdy nie testuj wystawionym back-endem |
| **T12.2** | `-p 8080:8080` i zapora hosta, która „blokuje 8080” | Port nadal odpowiada z LAN | `-p 127.0.0.1:8080:8080`; sprawdź inwentarzem, nie konfiguracją zapory |
| **T12.3** | Bezpieczeństwo przez niejasny port | „Nikt nie wie, że to jest na 18434” | Skanery i strony WWW próbują najpierw domyślnych, potem wszystkiego; uwierzytelniaj |
| **T12.4** | „To tylko na localhost” | Strona w Twojej własnej przeglądarce do tego sięga | Lista dozwolonych Host plus klucz (§4) |
| **T12.5** | `--api-key KEY` w wierszu poleceń | Klucz widoczny w `ps` dla każdego lokalnego użytkownika | `--api-key-file`, tryb 600 |
| **T12.6** | Jeden wspólny klucz | Nie odwołasz jednej osoby; log nie mówi, kto | Klucz na klienta w proxy |
| **T12.7** | Klucz bearer przez zwykły HTTP w LAN | Każdy w LAN go czyta | TLS na proxy, zawsze, gdy wychodzi poza loopback |
| **T12.8** | Skanowanie siebie z siebie | „Nic nie jest otwarte”, a laptop się łączy | Skanuj z drugiej maszyny; użyj własnego adresu LAN (§6.2) |
| **T12.9** | `--privileged`, gniazdo Dockera albo `$HOME` zamontowane w kontenerze serwującym | Przejęty serwer posiada hosta | Zrzuć uprawnienia, montuj tylko do odczytu, przekaż tylko węzły GPU (§5.4) |
| **T12.10** | Jednorazowe łatanie | CVE z tej tabeli trafia w starą wersję | Przypinaj, subskrybuj, comiesięczny slot aktualizacji (§5.7) |
| **T12.11** | Ufanie endpointowi modelu, z którym łączy się UI | Wrogi endpoint (klasa CVE-2025-64496) atakuje UI | Łącz tylko z serwerami, które kontrolujesz; aktualizuj UI |
| **T12.12** | Jedno GPU dla nieufających sobie użytkowników | Wyciek w stylu LeftoverLocals między procesami | Nie dziel jednego GPU między użytkowników, którzy sobie nie ufają |

---

## 10. Punkt kontrolny

```bash
cd "$SEC"
python3 infra/inventory.py | grep -v "loopback"        # idealnie tylko proxy
python3 infra/probe_llm.py <twój-adres-LAN> 8080 11434   # odmowa połączenia dla back-endów
python3 infra/probe_llm.py <host-lub-adres-proxy> <port-proxy>   # nic bez klucza
```

- [ ] Umiesz wyjaśnić różnicę między loopbackiem, adresem LAN i `0.0.0.0` oraz dlaczego strona w Twojej własnej
      przeglądarce może dotrzeć do loopbacka
- [ ] Każdy back-end, który uruchamiasz, jest przypięty do loopbacka; dokładnie jedna rzecz (proxy) nie jest
- [ ] Proxy ma TLS i klucz; Twój klucz leży w pliku z trybem 600, nie w wierszu poleceń
- [ ] `inventory.py` i skan z drugiej maszyny zgadzają się z Twoją własną listą w tabeli z §7
- [ ] Tabela przed/po jest wypełniona, razem z tym, czego nie dało się zamknąć, i kontrolą kompensującą
- [ ] Masz zapisaną rutynę aktualizacji i poradniki, które śledzisz
- [ ] Dla każdej klasy błędów z §3 umiesz wskazać tę jedną kontrolę z §5, która by go zatrzymała

---

**Dalej: [`13-GUARDRAILE-RED-TEAMING-I-OCENA-OBRON.md`](13-GUARDRAILE-RED-TEAMING-I-OCENA-OBRON.md)** —
modele guardrail, jak je uczciwie mierzyć, narzędzia red team skierowane na laboratorium i bramka regresji dla CI.

Powiązane: kurs 1, [część 07 — piaskownica, bezpieczeństwo, monitoring](../kurs_lokalne_modele/07-SANDBOX-BEZPIECZENSTWO-MONITORING.md);
kurs 2, [część 10 — piaskownica produkcyjna](../kurs_aplikacje_agentowe/10-PIASKOWNICA-PRODUKCYJNA.md). Źródła:
[`ZRODLA.md`](ZRODLA.md).
