# Narzędzia

Jeden skrypt, Python 3.10+, tylko biblioteka standardowa, bez instalacji. Tworzy każdą liczbę **(O)** z poradnika
i pozwala policzyć to samo dla tempa trafień Twojego agenta. Polecenia i flagi są po angielsku (jak w innych
`narzedzia/` w tym repozytorium), komentarze i komunikaty po polsku. Kopia angielska jest w
[`en/self-improving-agents/tools/`](../../../en/self-improving-agents/tools/README.md); liczby z obu wersji są identyczne.

```bash
cd pl/agenty-samodoskonalace/narzedzia
python3 rare_event_stats.py all          # odtwarza wszystkie tabele z poradnika (kilka sekund)
python3 rare_event_stats.py <polecenie> -h
```

| Polecenie | Odpowiada na pytanie | Przykład | W poradniku |
|---|---|---|---|
| `empty` | Jak prawdopodobne jest k pustych rund z rzędu przy tempie λ i jak długa musi być pusta seria, żeby coś znaczyła? | `empty --rates 0.15` | [02 §1](../02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#1-jak-bardzo-zaszumione-jest-nic-nie-znalazłem) |
| `power` | Ile trafień i rund na ramię trzeba, żeby wykazać stosunek tempa R? Z `--proxy`: ile pomaga gęstszy wskaźnik | `power --ratios 1.5 2 --rates 0.15 --proxy 4` | [02 §2–3](../02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#2-ile-trafień-trzeba-żeby-pokazać-że-zmiana-pomogła) |
| `sprt` | Granice, przyrosty za trafienie, błędy i oczekiwana długość SPRT Walda na przypisaniu trafień, dla dowolnego udziału pretendenta | `sprt --ratio 2 --share 0.25` | [02 §4](../02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#4-reguły-decyzji-dla-małych-zaszumionych-prób) |
| `cusum` | Średnia liczba rund do fałszywego alarmu i do wykrycia dla poissonowskiego CUSUM | `cusum --rate0 0.3 --rate1 0.15 --h 3 4 5` | [02 §5](../02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#5-pilnowanie-spadku-poissonowski-cusum) |
| `mcnemar` | Czy porównanie na złotym zbiorze przechodzi bramkę „napraw więcej, niż psujesz”? | `mcnemar --b 3 --c 11` | [03 §6](../03-BEZPIECZNA-PETLA.md#6-kaskada-bramek) |
| `shadow` | Minimalna liczba wygranych z n rozbieżności w trybie cienia | `shadow --max-n 30` | [03 §7](../03-BEZPIECZNA-PETLA.md#7-tryb-cienia) |
| `zero` | Górna granica tempa po n rundach bez trafień (reguła trzech) | `zero --rounds 30` | [02 §6](../02-POMIAR-PRZY-RZADKICH-ZDARZENIACH.md#6-zero-zdarzeń-i-nowe-źródła) |
| `discount` | Efektywna pamięć dyskontowanego rozkładu bandyty | `discount --gamma 0.98` | [03 §5](../03-BEZPIECZNA-PETLA.md#5-bandyta-do-alokacji-zamiast-przepisywania) |

**Uwagi.**

- Symulacje (`sprt`, `cusum`) używają stałego ziarna (`--seed 7`), więc wyniki są powtarzalne. Inne ziarno przesuwa
  liczby z symulacji o kilka procent; testy dokładne (`power`, `mcnemar`, `shadow`) się nie zmieniają.
- Model to proces Poissona ze stałym tempem. Prawdziwe tempo trafień zmienia się z godziną, dniem tygodnia i sezonem,
  więc wyniki traktuj jako **dolną granicę** potrzebnej ilości danych.
- Funkcję `binom_sf` może zaimportować Twój bramkarz: `from rare_event_stats import binom_sf`.

Licencja: MIT, jak cały kod w tym repozytorium ([LICENSE.md](../../../LICENSE.md)).
