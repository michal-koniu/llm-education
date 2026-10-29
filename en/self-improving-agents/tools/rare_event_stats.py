#!/usr/bin/env python3
"""Rare-event statistics for a self-improving agent's improvement loop.

Standard library only. Every number marked (C) in the guide comes from this script.
A "hit" is the rare outcome your agent exists to produce (a confirmed find, a real bug,
a relevant advisory). A "round" is one unit of work (one scan, one batch, one run).

Subcommands (run with -h for options):

  empty    How surprising are k empty rounds in a row at a given hit rate?
  power    How many hits (and rounds) to show that a challenger beats the champion?
  sprt     Wald SPRT on hit attribution (champion vs challenger), simulated.
  cusum    Poisson CUSUM for a drop in the hit rate: false-alarm and detection run lengths.
  mcnemar  Exact paired test for a golden-set comparison (b = champion-only right, c = challenger-only right).
  shadow   Minimum wins out of n adjudicated shadow-mode disagreements for p < alpha.
  zero     Rule of three: upper bound on the rate after n rounds with zero hits.
  discount Effective memory of a discounted posterior.
  all      Reproduce every table in the guide (a few seconds).

Examples:

  python3 rare_event_stats.py empty --rates 0.1 0.3
  python3 rare_event_stats.py power --ratios 1.5 2 --rates 0.2 --proxy 5
  python3 rare_event_stats.py sprt --ratio 2 --share 0.25
  python3 rare_event_stats.py cusum --rate0 0.3 --rate1 0.15 --h 3 4 5
  python3 rare_event_stats.py mcnemar --b 3 --c 11

License: MIT (see LICENSE.md in the repository root).
"""
import argparse
import math
import random


# ---------------------------------------------------------------- exact binomial helpers

def binom_sf(c, n, p):
    """P(X >= c) for X ~ Binomial(n, p)."""
    if c <= 0:
        return 1.0
    if c > n:
        return 0.0
    return sum(math.comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(c, n + 1))


def critical_value(n, alpha, p0=0.5):
    """Smallest c with P(X >= c | p0) <= alpha, or None if no such c exists."""
    for c in range(n + 1):
        if binom_sf(c, n, p0) <= alpha:
            return c
    return None


def hits_needed(ratio, alpha, power, limit=5000):
    """Total hits needed by the exact conditional binomial test (equal exposure).

    Condition on the total number of hits n. Under H0 each hit is equally likely to come
    from champion or challenger (p0 = 0.5). Under a true rate ratio R, p1 = R / (1 + R).
    Returns (n, c): reject H0 when the challenger has at least c of the n hits.
    """
    p1 = ratio / (1 + ratio)
    c = 0
    for n in range(2, limit):
        # the critical value never decreases as n grows, so resume the search from the last one
        while c <= n and binom_sf(c, n, 0.5) > alpha:
            c += 1
        if c <= n and binom_sf(c, n, p1) >= power:
            return n, c
    return None, None


# ---------------------------------------------------------------- subcommands

def cmd_empty(args):
    print("P(k empty rounds in a row | hit rate lambda per round) = exp(-lambda * k)\n")
    ks = args.k
    print("lambda  " + "  ".join(f"k={k:<3}" for k in ks) + "  | run for p<0.05  p<0.01")
    for lam in args.rates:
        row = "  ".join(f"{math.exp(-lam * k):5.2f}" for k in ks)
        k05 = math.ceil(math.log(20) / lam)
        k01 = math.ceil(math.log(100) / lam)
        print(f"{lam:<6}  {row}  | {k05:>13}  {k01:>6}")
    print("\nA run of empty rounds is evidence only when it is longer than ln(1/p) / lambda.")


def cmd_power(args):
    print(f"Hits needed for {args.power:.0%} power, one-sided exact conditional binomial test, "
          f"equal exposure\n")
    for alpha in args.alpha:
        for R in args.ratios:
            n, c = hits_needed(R, alpha, args.power)
            if n is None:
                print(f"alpha={alpha} R={R}: more than 5000 hits needed")
                continue
            per_arm = " / ".join(str(math.ceil(n / (lam * (1 + R)))) for lam in args.rates)
            print(f"alpha={alpha:<4} R={R:<5} total hits={n:<4} (accept if challenger has >= {c}); "
                  f"rounds per arm at {' / '.join(map(str, args.rates))} hits/round: {per_arm}")
            if args.proxy:
                rounds = math.ceil(n / (args.proxy * (1 + R)))
                print(f"{'':12}with a proxy at {args.proxy}/round: about {rounds} rounds per arm")
    if args.share != 0.5:
        f = args.share
        print(f"\nGiving the challenger {f:.0%} of rounds instead of 50% inflates total rounds by "
              f"about x{1 / (4 * f * (1 - f)):.2f}.")


def run_sprt(R, alpha, beta, true_R, share, trials, cap, rng):
    p0 = share
    p1 = R * share / (1 - share + R * share)
    pt = true_R * share / (1 - share + true_R * share)
    up = math.log((1 - beta) / alpha)
    lo = math.log(beta / (1 - alpha))
    w_ch = math.log(p1 / p0)                # added for each challenger hit
    w_cp = math.log((1 - p1) / (1 - p0))    # added for each champion hit
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
    print("Wald SPRT on which arm each hit came from\n")
    for R in args.ratio:
        _, _, _, w_ch, w_cp, up, lo = run_sprt(R, args.alpha, args.beta, 1.0, args.share, 1, 1, rng)
        print(f"design R={R}, challenger share {args.share:.0%}: +{w_ch:.3f} per challenger hit, "
              f"{w_cp:.3f} per champion hit; accept at {up:.2f}, reject at {lo:.2f}")
        for true_R in (1.0, R):
            acc, mean_n, p90, *_ = run_sprt(R, args.alpha, args.beta, true_R, args.share,
                                            args.trials, 2000, rng)
            print(f"   true R={true_R}: P(accept)={acc:.3f}, mean hits to decide={mean_n:.1f}, "
                  f"90th percentile={p90}")


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
    print(f"Poisson CUSUM watching for a drop {lam0} -> {lam1} hits/round")
    print(f"S = max(0, S + x*ln({lam1}/{lam0}) - ({lam1} - {lam0})); alarm when S > h")
    print(f"an empty round adds +{lam0 - lam1:.2f}; each hit adds "
          f"{math.log(lam1 / lam0) - (lam1 - lam0):.2f}\n")
    for h in args.h:
        arl0, arl0_p10 = run_length(lam0, lam0, lam1, h, args.trials, rng)
        arl1, _ = run_length(lam1, lam0, lam1, h, args.trials, rng)
        print(f"h={h}: mean rounds to a false alarm ~{arl0:.0f} (10th percentile {arl0_p10}); "
              f"mean rounds to detect the drop ~{arl1:.0f}")


def cmd_mcnemar(args):
    b, c = args.b, args.c
    n = b + c
    p = binom_sf(c, n, 0.5) if n else 1.0
    print(f"b={b} (champion right, challenger wrong), c={c} (challenger right, champion wrong)")
    print(f"exact one-sided McNemar p = P(X >= {c} | n={n}, 0.5) = {p:.4f}")
    verdict = "ACCEPT" if c > b and p < args.alpha else "REJECT (keep the champion)"
    print(f"gate (c > b and p < {args.alpha}): {verdict}")


def cmd_shadow(args):
    print(f"Minimum challenger wins out of n disagreements for one-sided p < {args.alpha}\n")
    for n in range(args.min_n, args.max_n + 1):
        c = critical_value(n, args.alpha)
        if c is not None:
            print(f"n={n:<3} wins >= {c}  (p = {binom_sf(c, n, 0.5):.4f})")


def cmd_zero(args):
    for n in args.rounds:
        print(f"0 hits in {n} rounds: 95% upper bound on the rate ~ 3/{n} = {3 / n:.3f} per round")


def cmd_discount(args):
    for g in args.gamma:
        print(f"gamma={g}: effective memory ~{1 / (1 - g):.0f} pulls")


def cmd_all(args, rng):
    sections = [
        ("1. Empty runs", lambda: cmd_empty(argparse.Namespace(rates=[0.1, 0.2, 0.3, 0.5, 1.0],
                                                             k=[2, 3, 5, 10]))),
        ("2. Hits needed", lambda: cmd_power(argparse.Namespace(
            alpha=[0.05, 0.10], ratios=[1.25, 1.5, 2.0, 3.0], power=0.8, rates=[0.1, 0.3, 1.0],
            proxy=None, share=0.25))),
        ("2b. Proxy example", lambda: cmd_power(argparse.Namespace(
            alpha=[0.05], ratios=[1.25], power=0.8, rates=[0.3], proxy=5.0, share=0.5))),
        ("3. SPRT", lambda: cmd_sprt(argparse.Namespace(ratio=[1.5, 2.0], alpha=0.05, beta=0.2,
                                                        share=0.5, trials=args.trials), rng)),
        ("4. CUSUM 0.3 -> 0.15", lambda: cmd_cusum(argparse.Namespace(
            rate0=0.3, rate1=0.15, h=[3.0, 4.0, 5.0], trials=args.cusum_trials), rng)),
        ("4b. CUSUM 1.0 -> 0.5", lambda: cmd_cusum(argparse.Namespace(
            rate0=1.0, rate1=0.5, h=[3.0, 4.0], trials=args.cusum_trials), rng)),
        ("5. Shadow mode", lambda: cmd_shadow(argparse.Namespace(alpha=0.05, min_n=10, max_n=30))),
        ("6. Zero events", lambda: cmd_zero(argparse.Namespace(rounds=[10, 30, 100]))),
        ("7. Discounting", lambda: cmd_discount(argparse.Namespace(gamma=[0.95, 0.98, 0.99]))),
    ]
    for title, fn in sections:
        print(f"\n===== {title} =====")
        fn()


# ---------------------------------------------------------------- command line

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=7, help="random seed for the simulations (default 7)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("empty", help="probability of k empty rounds in a row")
    p.add_argument("--rates", type=float, nargs="+", default=[0.1, 0.2, 0.3, 0.5, 1.0])
    p.add_argument("--k", type=int, nargs="+", default=[2, 3, 5, 10])

    p = sub.add_parser("power", help="hits and rounds needed to detect a rate ratio")
    p.add_argument("--ratios", type=float, nargs="+", default=[1.25, 1.5, 2.0, 3.0])
    p.add_argument("--alpha", type=float, nargs="+", default=[0.05])
    p.add_argument("--power", type=float, default=0.8)
    p.add_argument("--rates", type=float, nargs="+", default=[0.1, 0.3, 1.0],
                   help="champion hit rates per round, for the rounds-per-arm column")
    p.add_argument("--proxy", type=float, default=None,
                   help="events per round of a denser proxy metric, e.g. near-misses")
    p.add_argument("--share", type=float, default=0.5, help="challenger share of rounds")

    p = sub.add_parser("sprt", help="sequential test on hit attribution")
    p.add_argument("--ratio", type=float, nargs="+", default=[1.5, 2.0])
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--beta", type=float, default=0.2)
    p.add_argument("--share", type=float, default=0.5, help="challenger share of rounds")
    p.add_argument("--trials", type=int, default=20000)

    p = sub.add_parser("cusum", help="Poisson CUSUM run lengths")
    p.add_argument("--rate0", type=float, default=0.3, help="normal hit rate per round")
    p.add_argument("--rate1", type=float, default=0.15, help="degraded rate to detect")
    p.add_argument("--h", type=float, nargs="+", default=[3.0, 4.0, 5.0])
    p.add_argument("--trials", type=int, default=4000)

    p = sub.add_parser("mcnemar", help="exact paired golden-set test")
    p.add_argument("--b", type=int, required=True, help="items only the champion gets right")
    p.add_argument("--c", type=int, required=True, help="items only the challenger gets right")
    p.add_argument("--alpha", type=float, default=0.05)

    p = sub.add_parser("shadow", help="wins needed in shadow-mode disagreements")
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--min-n", type=int, default=5)
    p.add_argument("--max-n", type=int, default=30)

    p = sub.add_parser("zero", help="rule of three")
    p.add_argument("--rounds", type=int, nargs="+", default=[10, 30, 100])

    p = sub.add_parser("discount", help="effective memory of a discounted posterior")
    p.add_argument("--gamma", type=float, nargs="+", default=[0.95, 0.98, 0.99])

    p = sub.add_parser("all", help="reproduce every table in the guide")
    p.add_argument("--trials", type=int, default=20000, help="SPRT simulation trials")
    p.add_argument("--cusum-trials", type=int, default=4000, help="CUSUM simulation trials")

    args = ap.parse_args()
    rng = random.Random(args.seed)
    if args.cmd in ("sprt", "cusum", "all"):
        {"sprt": cmd_sprt, "cusum": cmd_cusum, "all": cmd_all}[args.cmd](args, rng)
    else:
        {"empty": cmd_empty, "power": cmd_power, "mcnemar": cmd_mcnemar, "shadow": cmd_shadow,
         "zero": cmd_zero, "discount": cmd_discount}[args.cmd](args)


if __name__ == "__main__":
    main()
