#!/usr/bin/env python3
"""Statystyka rzadkich zdarzeń dla pętli samodoskonalenia agenta.

Tylko biblioteka standardowa. Każda liczba oznaczona w poradniku (O) pochodzi z tego skryptu.
„Trafienie” to rzadki wynik, dla którego agent istnieje (potwierdzone znalezisko, prawdziwy błąd,
istotny biuletyn bezpieczeństwa). „Runda” to jedna jednostka pracy (jedno przeszukanie, jedna partia).

Polecenia (opcje: -h przy każdym):

  empty    Jak bardzo zaskakuje k pustych rund z rzędu przy danym tempie trafień?
  power    Ile trafień (i rund) trzeba, żeby pokazać, że pretendent jest lepszy od mistrza?
  sprt     Test sekwencyjny Walda na przypisaniu trafień (mistrz czy pretendent), symulacja.
  cusum    Poissonowski CUSUM na spadek tempa trafień: długość serii do fałszywego alarmu i do wykrycia.
  mcnemar  Dokładny test par dla złotego zbioru (b = dobrze tylko mistrz, c = dobrze tylko pretendent).
  shadow   Minimalna liczba wygranych z n rozstrzygniętych rozbieżności w trybie cienia, by p < alfa.
  zero     Reguła trzech: górna granica tempa po n rundach bez trafień.
  discount Efektywna pamięć dyskontowanego rozkładu a posteriori.
  all      Odtwarza wszystkie tabele z poradnika (kilka sekund).

Przykłady:

  python3 rare_event_stats.py empty --rates 0.1 0.3
  python3 rare_event_stats.py power --ratios 1.5 2 --rates 0.2 --proxy 5
  python3 rare_event_stats.py sprt --ratio 2 --share 0.25
  python3 rare_event_stats.py cusum --rate0 0.3 --rate1 0.15 --h 3 4 5
  python3 rare_event_stats.py mcnemar --b 3 --c 11

Licencja: MIT (zob. LICENSE.md w katalogu głównym repozytorium).
"""
import argparse
import math
import random


# ---------------------------------------------------------------- dokładny rozkład dwumianowy

def binom_sf(c, n, p):
    """P(X >= c) dla X ~ Binomial(n, p)."""
    if c <= 0:
        return 1.0
    if c > n:
        return 0.0
    return sum(math.comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(c, n + 1))


def critical_value(n, alpha, p0=0.5):
    """Najmniejsze c, dla którego P(X >= c | p0) <= alfa, albo None, jeśli takiego nie ma."""
    for c in range(n + 1):
        if binom_sf(c, n, p0) <= alpha:
            return c
    return None


def hits_needed(ratio, alpha, power, limit=5000):
    """Łączna liczba trafień potrzebna w dokładnym warunkowym teście dwumianowym (równa ekspozycja).

    Warunkujemy na łącznej liczbie trafień n. Przy H0 każde trafienie z równym
    prawdopodobieństwem pochodzi od mistrza i od pretendenta (p0 = 0,5). Przy prawdziwym
    stosunku tempa R: p1 = R / (1 + R). Zwraca (n, c): odrzucamy H0, gdy pretendent ma co
    najmniej c z n trafień.
    """
    p1 = ratio / (1 + ratio)
    c = 0
    for n in range(2, limit):
        # wartość krytyczna nie maleje razem z n, więc szukamy dalej od poprzedniej
        while c <= n and binom_sf(c, n, 0.5) > alpha:
            c += 1
        if c <= n and binom_sf(c, n, p1) >= power:
            return n, c
    return None, None


# ---------------------------------------------------------------- polecenia

def cmd_empty(args):
    print("P(k pustych rund z rzędu | tempo trafień lambda na rundę) = exp(-lambda * k)\n")
    ks = args.k
    print("lambda  " + "  ".join(f"k={k:<3}" for k in ks) + "  | seria dla p<0.05  p<0.01")
    for lam in args.rates:
        row = "  ".join(f"{math.exp(-lam * k):5.2f}" for k in ks)
        k05 = math.ceil(math.log(20) / lam)
        k01 = math.ceil(math.log(100) / lam)
        print(f"{lam:<6}  {row}  | {k05:>15}  {k01:>6}")
    print("\nSeria pustych rund jest dowodem dopiero wtedy, gdy jest dłuższa niż ln(1/p) / lambda.")


def cmd_power(args):
    print(f"Trafienia potrzebne do mocy {args.power:.0%}, jednostronny dokładny warunkowy test "
          f"dwumianowy, równa ekspozycja\n")
    for alpha in args.alpha:
        for R in args.ratios:
            n, c = hits_needed(R, alpha, args.power)
            if n is None:
                print(f"alfa={alpha} R={R}: potrzeba ponad 5000 trafień")
                continue
            per_arm = " / ".join(str(math.ceil(n / (lam * (1 + R)))) for lam in args.rates)
            print(f"alfa={alpha:<4} R={R:<5} trafień łącznie={n:<4} (przyjmij, gdy pretendent ma >= {c}); "
                  f"rund na ramię przy {' / '.join(map(str, args.rates))} trafień/rundę: {per_arm}")
            if args.proxy:
                rounds = math.ceil(n / (args.proxy * (1 + R)))
                print(f"{'':12}ze wskaźnikiem zastępczym {args.proxy}/rundę: ok. {rounds} rund na ramię")
    if args.share != 0.5:
        f = args.share
        print(f"\nGdy pretendent dostaje {f:.0%} rund zamiast 50%, łączna liczba rund rośnie "
              f"ok. x{1 / (4 * f * (1 - f)):.2f}.")


def run_sprt(R, alpha, beta, true_R, share, trials, cap, rng):
    p0 = share
    p1 = R * share / (1 - share + R * share)
    pt = true_R * share / (1 - share + true_R * share)
    up = math.log((1 - beta) / alpha)
    lo = math.log(beta / (1 - alpha))
    w_ch = math.log(p1 / p0)                # dodawane za każde trafienie pretendenta
    w_cp = math.log((1 - p1) / (1 - p0))    # dodawane za każde trafienie mistrza
    accepts, lengths = 0, []
    for _ in range(trials):
        s, n = 0.0, 0
        while lo < s < up and n < cap:
            n += 1
            s += w_ch if rng.random() < pt else w_cp
        lengths.append(n)
        accepts += s >= up
    lengths.sort()
    return accepts / trials, sum(lengths) / trials, lengths[int(0.9 * trials)], w_ch, w_cp, up, lo


def cmd_sprt(args, rng):
    print("SPRT Walda na tym, z którego ramienia pochodzi każde trafienie\n")
    for R in args.ratio:
        _, _, _, w_ch, w_cp, up, lo = run_sprt(R, args.alpha, args.beta, 1.0, args.share, 1, 1, rng)
        print(f"projekt R={R}, udział pretendenta {args.share:.0%}: +{w_ch:.3f} za trafienie pretendenta, "
              f"{w_cp:.3f} za trafienie mistrza; przyjęcie przy {up:.2f}, odrzucenie przy {lo:.2f}")
        for true_R in (1.0, R):
            acc, mean_n, p90, *_ = run_sprt(R, args.alpha, args.beta, true_R, args.share,
                                            args.trials, 2000, rng)
            print(f"   prawdziwe R={true_R}: P(przyjęcia)={acc:.3f}, średnio trafień do decyzji={mean_n:.1f}, "
                  f"90. percentyl={p90}")


def poisson_sample(lam, rng):
    L, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= L:
            return k
        k += 1


def run_length(lam_true, lam0, lam1, h, trials, rng, cap=20000):
    a = math.log(lam1 / lam0)
    b = lam1 - lam0
    runs = []
    for _ in range(trials):
        s, t = 0.0, 0
        while t < cap:
            t += 1
            s = max(0.0, s + poisson_sample(lam_true, rng) * a - b)
            if s > h:
                break
        runs.append(t)
    runs.sort()
    return sum(runs) / trials, runs[int(0.1 * trials)]


def cmd_cusum(args, rng):
    lam0, lam1 = args.rate0, args.rate1
    print(f"Poissonowski CUSUM pilnujący spadku {lam0} -> {lam1} trafień/rundę")
    print(f"S = max(0, S + x*ln({lam1}/{lam0}) - ({lam1} - {lam0})); alarm, gdy S > h")
    print(f"pusta runda dodaje +{lam0 - lam1:.2f}; każde trafienie dodaje "
          f"{math.log(lam1 / lam0) - (lam1 - lam0):.2f}\n")
    for h in args.h:
        arl0, arl0_p10 = run_length(lam0, lam0, lam1, h, args.trials, rng)
        arl1, _ = run_length(lam1, lam0, lam1, h, args.trials, rng)
        print(f"h={h}: średnio rund do fałszywego alarmu ~{arl0:.0f} (10. percentyl {arl0_p10}); "
              f"średnio rund do wykrycia spadku ~{arl1:.0f}")


def cmd_mcnemar(args):
    b, c = args.b, args.c
    n = b + c
    p = binom_sf(c, n, 0.5) if n else 1.0
    print(f"b={b} (mistrz dobrze, pretendent źle), c={c} (pretendent dobrze, mistrz źle)")
    print(f"dokładny jednostronny McNemar p = P(X >= {c} | n={n}, 0.5) = {p:.4f}")
    verdict = "PRZYJĄĆ" if c > b and p < args.alpha else "ODRZUCIĆ (zostaje mistrz)"
    print(f"bramka (c > b oraz p < {args.alpha}): {verdict}")


def cmd_shadow(args):
    print(f"Minimalna liczba wygranych pretendenta z n rozbieżności dla jednostronnego p < {args.alpha}\n")
    for n in range(args.min_n, args.max_n + 1):
        c = critical_value(n, args.alpha)
        if c is not None:
            print(f"n={n:<3} wygranych >= {c}  (p = {binom_sf(c, n, 0.5):.4f})")


def cmd_zero(args):
    for n in args.rounds:
        print(f"0 trafień w {n} rundach: 95% górna granica tempa ~ 3/{n} = {3 / n:.3f} na rundę")


def cmd_discount(args):
    for g in args.gamma:
        print(f"gamma={g}: efektywna pamięć ~{1 / (1 - g):.0f} pociągnięć")


def cmd_all(args, rng):
    sections = [
        ("1. Puste serie", lambda: cmd_empty(argparse.Namespace(rates=[0.1, 0.2, 0.3, 0.5, 1.0],
                                                              k=[2, 3, 5, 10]))),
        ("2. Potrzebne trafienia", lambda: cmd_power(argparse.Namespace(
            alpha=[0.05, 0.10], ratios=[1.25, 1.5, 2.0, 3.0], power=0.8, rates=[0.1, 0.3, 1.0],
            proxy=None, share=0.25))),
        ("2b. Przykład ze wskaźnikiem zastępczym", lambda: cmd_power(argparse.Namespace(
            alpha=[0.05], ratios=[1.25], power=0.8, rates=[0.3], proxy=5.0, share=0.5))),
        ("3. SPRT", lambda: cmd_sprt(argparse.Namespace(ratio=[1.5, 2.0], alpha=0.05, beta=0.2,
                                                        share=0.5, trials=args.trials), rng)),
        ("4. CUSUM 0.3 -> 0.15", lambda: cmd_cusum(argparse.Namespace(
            rate0=0.3, rate1=0.15, h=[3.0, 4.0, 5.0], trials=args.cusum_trials), rng)),
        ("4b. CUSUM 1.0 -> 0.5", lambda: cmd_cusum(argparse.Namespace(
            rate0=1.0, rate1=0.5, h=[3.0, 4.0], trials=args.cusum_trials), rng)),
        ("5. Tryb cienia", lambda: cmd_shadow(argparse.Namespace(alpha=0.05, min_n=10, max_n=30))),
        ("6. Zero zdarzeń", lambda: cmd_zero(argparse.Namespace(rounds=[10, 30, 100]))),
        ("7. Dyskontowanie", lambda: cmd_discount(argparse.Namespace(gamma=[0.95, 0.98, 0.99]))),
    ]
    for title, fn in sections:
        print(f"\n===== {title} =====")
        fn()


# ---------------------------------------------------------------- wiersz poleceń

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=7, help="ziarno losowania dla symulacji (domyślnie 7)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("empty", help="prawdopodobieństwo k pustych rund z rzędu")
    p.add_argument("--rates", type=float, nargs="+", default=[0.1, 0.2, 0.3, 0.5, 1.0])
    p.add_argument("--k", type=int, nargs="+", default=[2, 3, 5, 10])

    p = sub.add_parser("power", help="trafienia i rundy potrzebne do wykrycia stosunku tempa")
    p.add_argument("--ratios", type=float, nargs="+", default=[1.25, 1.5, 2.0, 3.0])
    p.add_argument("--alpha", type=float, nargs="+", default=[0.05])
    p.add_argument("--power", type=float, default=0.8)
    p.add_argument("--rates", type=float, nargs="+", default=[0.1, 0.3, 1.0],
                   help="tempo trafień mistrza na rundę, do kolumny rund na ramię")
    p.add_argument("--proxy", type=float, default=None,
                   help="zdarzenia gęstszego wskaźnika zastępczego na rundę, np. prawie-trafienia")
    p.add_argument("--share", type=float, default=0.5, help="udział rund pretendenta")

    p = sub.add_parser("sprt", help="test sekwencyjny na przypisaniu trafień")
    p.add_argument("--ratio", type=float, nargs="+", default=[1.5, 2.0])
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--beta", type=float, default=0.2)
    p.add_argument("--share", type=float, default=0.5, help="udział rund pretendenta")
    p.add_argument("--trials", type=int, default=20000)

    p = sub.add_parser("cusum", help="długości serii poissonowskiego CUSUM")
    p.add_argument("--rate0", type=float, default=0.3, help="normalne tempo trafień na rundę")
    p.add_argument("--rate1", type=float, default=0.15, help="obniżone tempo do wykrycia")
    p.add_argument("--h", type=float, nargs="+", default=[3.0, 4.0, 5.0])
    p.add_argument("--trials", type=int, default=4000)

    p = sub.add_parser("mcnemar", help="dokładny test par na złotym zbiorze")
    p.add_argument("--b", type=int, required=True, help="pozycje, które dobrze ocenia tylko mistrz")
    p.add_argument("--c", type=int, required=True, help="pozycje, które dobrze ocenia tylko pretendent")
    p.add_argument("--alpha", type=float, default=0.05)

    p = sub.add_parser("shadow", help="wygrane potrzebne w rozbieżnościach trybu cienia")
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--min-n", type=int, default=5)
    p.add_argument("--max-n", type=int, default=30)

    p = sub.add_parser("zero", help="reguła trzech")
    p.add_argument("--rounds", type=int, nargs="+", default=[10, 30, 100])

    p = sub.add_parser("discount", help="efektywna pamięć dyskontowanego rozkładu a posteriori")
    p.add_argument("--gamma", type=float, nargs="+", default=[0.95, 0.98, 0.99])

    p = sub.add_parser("all", help="odtwarza wszystkie tabele z poradnika")
    p.add_argument("--trials", type=int, default=20000, help="liczba prób symulacji SPRT")
    p.add_argument("--cusum-trials", type=int, default=4000, help="liczba prób symulacji CUSUM")

    args = ap.parse_args()
    rng = random.Random(args.seed)
    if args.cmd in ("sprt", "cusum", "all"):
        {"sprt": cmd_sprt, "cusum": cmd_cusum, "all": cmd_all}[args.cmd](args, rng)
    else:
        {"empty": cmd_empty, "power": cmd_power, "mcnemar": cmd_mcnemar, "shadow": cmd_shadow,
         "zero": cmd_zero, "discount": cmd_discount}[args.cmd](args)


if __name__ == "__main__":
    main()
