#!/usr/bin/env python3
"""pricing_model.py — kalkulator do kursu „Wycena prywatnego AI boxa".

Tylko biblioteka standardowa (Python >= 3.12). Sześć podkomend, po jednej na lekcję:

  floor   część 02  podłoga kosztowa: najniższa cena miesięczna, która utrzymuje docelową marżę brutto
  value   część 03  sufit wartości: wartość ekonomiczna pudełka dla jednej kancelarii
  cash    część 05  przepływy pieniężne czterech modeli sprzętowych przez N miesięcy
  vw      część 06  wrażliwość cenowa Van Westendorpa z pliku CSV z odpowiedziami z ankiety
  gg      część 06  Gabor-Granger: cena maksymalizująca przychód na podstawie odsetka akceptacji
  nrr     część 08  retencja przychodu netto: odpływ klientów vs dokupieni agenci vs indeksacja

Każda liczba ma wartość domyślną wziętą z lekcji. Wartości domyślne to założenia,
nie fakty: zastąp je własnymi pomiarami. Wszystkie kwoty to PLN netto (bez VAT).

Przykłady:
  python3 pricing_model.py floor
  python3 pricing_model.py floor --hardware 21950 --support-h 3 --offices 20
  python3 pricing_model.py value --people 5 --hours-saved 2 --rate 350
  python3 pricing_model.py cash --months 36 --new-per-month 2
  python3 pricing_model.py vw answers.csv
  python3 pricing_model.py gg 600:0.80 900:0.62 1200:0.41 1500:0.22
"""
from __future__ import annotations

import argparse
import csv
import sys


# ---------------------------------------------------------------- funkcje pomocnicze

def pln(x: float) -> str:
    """Formatuje kwotę jako PLN ze spacją jako separatorem tysięcy: 12 345 PLN."""
    return f"{x:,.0f}".replace(",", " ") + " PLN"


def table(rows: list[tuple], header: tuple) -> None:
    widths = [max(len(str(r[i])) for r in [header, *rows]) for i in range(len(header))]
    line = "  ".join(str(h).ljust(w) for h, w in zip(header, widths))
    print(line)
    print("-" * len(line))
    for r in rows:
        print("  ".join(str(c).ljust(w) for c, w in zip(r, widths)))


# ---------------------------------------------------------------- floor (część 02)

def cmd_floor(a: argparse.Namespace) -> None:
    """Miesięczny koszt obsługi JEDNEJ kancelarii, a potem cena dająca docelową marżę.

    Koszt obsługi (COGS) to tutaj wszystko, co musisz wydać, żeby jeden klient
    działał: amortyzacja sprzętu (jeśli jest Twój), wsparcie, aktualizacje modeli,
    monitoring, hosting kanału aktualizacji, ubezpieczenie. Sprzedaż i rozwój produktu
    to NIE jest COGS — to koszty operacyjne, opłacane z marży.
    """
    hw_month = a.hardware / a.amortise_months if a.you_own_hardware else 0.0
    install_month = a.install_h * a.hour_cost / a.contract_months
    support_month = a.support_h * a.hour_cost
    # Aktualizację modelu (nowa wersja Bielika / PLLuM + ponowne przejście zestawu ewaluacyjnego)
    # robisz raz i wdrażasz we wszystkich kancelariach, więc jej koszt jest dzielony.
    update_month = a.update_h_per_quarter * a.hour_cost / 3 / max(a.offices, 1)
    other_month = a.other

    lines = [
        ("hardware amortisation", hw_month),
        ("installation (spread over contract)", install_month),
        ("support and monitoring", support_month),
        ("model updates (shared)", update_month),
        ("other (licences, backup, insurance)", other_month),
    ]
    cogs = sum(v for _, v in lines)
    floor_price = cogs / (1 - a.margin)

    print(f"\nCost floor for one office ({a.offices} offices share the update cost)\n")
    table([(n, pln(v)) for n, v in lines] + [("= COGS per month", pln(cogs))],
          ("line", "per month"))
    print(f"\nTarget gross margin {a.margin:.0%}  ->  minimum price {pln(floor_price)} / month")
    print(f"Break-even price (0% margin)          {pln(cogs)} / month")
    if a.you_own_hardware:
        print("\nNote: you own the hardware, so its amortisation is in COGS.")
    else:
        print("\nNote: the customer owns the hardware (sold or leased), so it is not in COGS.")


# ---------------------------------------------------------------- value (część 03)

def cmd_value(a: argparse.Namespace) -> None:
    """Szacowanie wartości ekonomicznej (Nagle i Müller): wartość = najlepsza alternatywa + zróżnicowanie.

    Wartość zróżnicowania to tutaj zaoszczędzony czas, który kancelaria może zafakturować lub
    wykorzystać inaczej, plus wartość ryzyka. 'realisation' = odsetek zaoszczędzonych godzin, które
    zamieniają się w pieniądze (zafakturowane albo uwolnione na pracę fakturowaną). Bądź
    pesymistą: 0,3-0,5 to rozsądny start.
    """
    weeks = 4.33
    time_value = a.people * a.hours_saved * weeks * a.rate * a.realisation
    diff_value = time_value + a.risk_value
    eve = a.alternative + diff_value
    print("\nEconomic value of the box for one office, per month\n")
    table([
        ("next-best alternative (what they would pay instead)", pln(a.alternative)),
        (f"time value: {a.people} people x {a.hours_saved} h/week x {a.rate} PLN x {a.realisation:.0%}",
         pln(time_value)),
        ("risk value (secrecy, GDPR, lost files)", pln(a.risk_value)),
        ("= economic value (ceiling)", pln(eve)),
    ], ("component", "PLN / month"))
    print("\nA price the customer can say yes to sits well below the ceiling:")
    for share in (0.10, 0.20, 0.30):
        price = a.alternative + share * diff_value
        print(f"  capture {share:.0%} of the differentiation value -> {pln(price)} / month")


# ---------------------------------------------------------------- cash (część 05)

def cmd_cash(a: argparse.Namespace) -> None:
    """Twoja skumulowana gotówka w czterech modelach sprzętowych, z nowymi klientami co miesiąc.

    customer-buys : klient kupuje pudełko w sklepie; Ty pobierasz opłatę wdrożeniową + abonament.
    resell        : kupujesz i odsprzedajesz z marżą; finansujesz zakup, dopóki klient nie zapłaci.
    lease         : firma leasingowa płaci Ci za pudełko; klient płaci leasingodawcy.
    rent (HaaS)   : pudełko jest Twoje i pobierasz jedną opłatę miesięczną; finansujesz z góry każde pudełko.
    """
    hw_sale = a.hardware * (1 + a.hw_markup)
    # (wydatek na pudełko, przychód za pudełko, ile miesięcy do wpływu tego przychodu, opłata miesięczna)
    lag = a.payment_days // 30  # resell: klient płaci Twoją fakturę po terminie płatności
    models = {
        "customer-buys": (0.0, 0.0, 0, a.subscription),
        "resell": (a.hardware, hw_sale, lag, a.subscription),
        "lease": (a.hardware, hw_sale, 0, a.subscription),  # leasingodawca płaci Ci przy dostawie
        "rent (HaaS)": (a.hardware, 0.0, 0, a.subscription + hw_sale / a.rent_months),
    }
    print(f"\nCumulative cash, {a.new_per_month} new offices/month, churn {a.churn:.1%}/month, "
          f"support cost {pln(a.cost_per_office)}/office/month, payment term {a.payment_days} days, "
          f"fixed costs {pln(a.fixed_monthly)}/month\n")
    rows = []
    for name, (hw_cost, hw_income, hw_lag, fee) in models.items():
        cash, active, lowest, lowest_month = 0.0, 0.0, 0.0, 0
        for month in range(1, a.months + 1):
            active = active * (1 - a.churn) + a.new_per_month
            cash += a.new_per_month * (a.setup - hw_cost)          # płacisz sklepowi od razu
            if month > hw_lag:
                cash += a.new_per_month * hw_income                # za pudełko dostajesz pieniądze później
            cash += active * (fee - a.cost_per_office)
            cash -= a.fixed_monthly                                 # sprzedaż, rozwój, Twoja pensja
            if cash < lowest:
                lowest, lowest_month = cash, month
        rows.append((name, pln(lowest), f"month {lowest_month}" if lowest_month else "-", pln(cash)))
    table(rows, ("model", "lowest cash", "when", f"cash after {a.months} months"))
    print("\n'lowest cash' is the money you must have in the bank (or borrow) before you start.")


# ---------------------------------------------------------------- Van Westendorp (część 06)

def _share_at(values: list[float], price: float, below: bool) -> float:
    """Odsetek respondentów, których próg jest <= ceny (below=False) albo >= ceny (below=True)."""
    if below:
        return sum(1 for v in values if v >= price) / len(values)
    return sum(1 for v in values if v <= price) / len(values)


def _crossing(prices: list[float], f, g) -> float | None:
    """Pierwsza cena, przy której krzywa f - g zmienia znak (interpolacja liniowa)."""
    prev = None
    for p in prices:
        d = f(p) - g(p)
        if prev is not None and (prev[1] <= 0 <= d or prev[1] >= 0 >= d) and prev[1] != d:
            p0, d0 = prev
            return p0 + (p - p0) * (0 - d0) / (d - d0)
        prev = (p, d)
    return None


def cmd_vw(a: argparse.Namespace) -> None:
    """Kolumny CSV: too_cheap, cheap, expensive, too_expensive (jeden wiersz na respondenta).

    Cztery pytania (Van Westendorp, 1976):
      too_cheap      — przy jakiej cenie byłoby to tak tanie, że zwątpiłbyś w jakość?
      cheap          — przy jakiej cenie to okazja?
      expensive      — przy jakiej cenie robi się drogo, ale nadal brałbyś to pod uwagę?
      too_expensive  — przy jakiej cenie jest tak drogo, że nie brałbyś tego pod uwagę?
    """
    cols = {"too_cheap": [], "cheap": [], "expensive": [], "too_expensive": []}
    with open(a.csv, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            for k in cols:
                cols[k].append(float(row[k]))
    n = len(cols["cheap"])
    if n < 1:
        sys.exit("no rows")
    prices = sorted({v for vs in cols.values() for v in vs})
    lo, hi = prices[0], prices[-1]
    grid = [lo + (hi - lo) * i / 400 for i in range(401)]

    too_cheap = lambda p: _share_at(cols["too_cheap"], p, below=True)      # maleje, gdy p rośnie
    cheap = lambda p: _share_at(cols["cheap"], p, below=True)
    expensive = lambda p: _share_at(cols["expensive"], p, below=False)    # rośnie, gdy p rośnie
    too_exp = lambda p: _share_at(cols["too_expensive"], p, below=False)

    not_cheap = lambda p: 1 - cheap(p)
    not_exp = lambda p: 1 - expensive(p)

    pmc = _crossing(grid, too_cheap, not_cheap)   # punkt krańcowej taniości
    opp = _crossing(grid, too_cheap, too_exp)     # optymalny punkt cenowy
    ipp = _crossing(grid, cheap, expensive)       # punkt obojętności cenowej
    pme = _crossing(grid, too_exp, not_exp)       # punkt krańcowej drogości
    fmt = lambda v: pln(v) if v is not None else "no crossing"
    print(f"\nVan Westendorp, n = {n}" + ("   ⚠️ n < 30: read as a direction, not a number" if n < 30 else ""))
    table([
        ("PMC point of marginal cheapness", fmt(pmc)),
        ("OPP optimal price point", fmt(opp)),
        ("IPP indifference price point", fmt(ipp)),
        ("PME point of marginal expensiveness", fmt(pme)),
    ], ("point", "price"))
    print("\nAcceptable range = PMC .. PME. Price above IPP if you are clearly differentiated.")


# ---------------------------------------------------------------- Gabor-Granger (część 06)

def cmd_gg(a: argparse.Namespace) -> None:
    """Argumenty: pary cena:odsetek, np. 900:0.62 oznacza, że 62% odpowiedziało „tak, kupiłbym za 900"."""
    pts = []
    for item in a.points:
        p, s = item.split(":")
        pts.append((float(p), float(s)))
    pts.sort()
    rows, best = [], None
    for p, s in pts:
        rev = p * s
        margin_rev = (p - a.cost) * s
        rows.append((pln(p), f"{s:.0%}", pln(rev), pln(margin_rev)))
        if best is None or margin_rev > best[1]:
            best = (p, margin_rev)
    print("\nGabor-Granger: expected revenue and gross profit per 100% of prospects\n")
    table(rows, ("price", "would buy", "revenue index", "gross profit index"))
    print(f"\nGross-profit-maximising price among those tested: {pln(best[0])} (cost {pln(a.cost)})")
    print("Stated intent overstates real buying. Treat the shares as an upper bound.")


# ---------------------------------------------------------------- nrr (część 08)

def cmd_nrr(a: argparse.Namespace) -> None:
    """Retencja przychodu netto jednej kohorty kancelarii w ciągu 12 miesięcy.

    NRR = przychód, który ta kohorta płaci w miesiącu 12 / przychód, który płaciła w miesiącu 0.
    Odpływ usuwa kancelarie; ekspansja dodaje agentów w kancelariach, które zostają; indeksacja
    podnosi każdą cenę raz, przy rocznym odnowieniu.
    """
    offices = float(a.offices)
    agents_per_office = 0.0
    start = offices * a.platform
    for _ in range(12):
        offices *= 1 - a.churn
        agents_per_office += a.expansion  # odsetek kancelarii dokupujących w tym miesiącu jednego agenta
    end = offices * (a.platform + agents_per_office * a.agent_price) * (1 + a.indexation)
    grr = offices / a.offices
    print(f"\nOne cohort of {a.offices} offices at {pln(a.platform)}/month, 12 months\n")
    table([
        ("monthly churn", f"{a.churn:.1%}"),
        ("offices adding one agent per month", f"{a.expansion:.1%}"),
        ("agent price", pln(a.agent_price)),
        ("indexation at renewal", f"{a.indexation:.1%}"),
        ("offices left after 12 months", f"{offices:.1f}"),
        ("gross revenue retention (churn only)", f"{grr:.0%}"),
        ("NET revenue retention", f"{end / start:.0%}"),
    ], ("item", "value"))
    print("\nAbove 100%: the cohort pays you more each year even though some offices leave.")


# ---------------------------------------------------------------- CLI

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("floor", help="cost floor per office (part 02)")
    # 10 967 PLN netto = Minisforum MS-S1 MAX (Ryzen AI Max+ 395, 128 GB), 13 490 PLN brutto na Ceneo, 25 października 2026
    f.add_argument("--hardware", type=float, default=10967, help="box price, PLN net")
    f.add_argument("--amortise-months", type=int, default=36)
    f.add_argument("--you-own-hardware", action="store_true", help="rent model: hardware is your COGS")
    f.add_argument("--install-h", type=float, default=16, help="hours to install and configure")
    f.add_argument("--contract-months", type=int, default=24)
    f.add_argument("--support-h", type=float, default=2, help="support hours per office per month")
    f.add_argument("--hour-cost", type=float, default=200, help="cost of one hour of support work")
    f.add_argument("--update-h-per-quarter", type=float, default=40, help="model update + eval, hours")
    f.add_argument("--offices", type=int, default=10)
    f.add_argument("--other", type=float, default=100, help="other monthly cost per office")
    f.add_argument("--margin", type=float, default=0.75, help="target gross margin, 0-1")
    f.set_defaults(fn=cmd_floor)

    v = sub.add_parser("value", help="economic value per office (part 03)")
    v.add_argument("--people", type=int, default=5)
    v.add_argument("--hours-saved", type=float, default=2, help="hours per person per week")
    v.add_argument("--rate", type=float, default=300, help="PLN per hour the time is worth")
    v.add_argument("--realisation", type=float, default=0.4, help="share of saved time that becomes money")
    v.add_argument("--alternative", type=float, default=0, help="price of next-best alternative per month")
    v.add_argument("--risk-value", type=float, default=0)
    v.set_defaults(fn=cmd_value)

    c = sub.add_parser("cash", help="cash flow of hardware models (part 05)")
    c.add_argument("--months", type=int, default=36)
    c.add_argument("--new-per-month", type=float, default=2)
    c.add_argument("--churn", type=float, default=0.01)
    c.add_argument("--hardware", type=float, default=10967)
    c.add_argument("--hw-markup", type=float, default=0.10)
    c.add_argument("--setup", type=float, default=6000)
    c.add_argument("--subscription", type=float, default=1500)
    c.add_argument("--rent-months", type=int, default=36)
    c.add_argument("--cost-per-office", type=float, default=500)
    c.add_argument("--payment-days", type=int, default=14)
    c.add_argument("--fixed-monthly", type=float, default=15000,
                   help="fixed operating costs per month: sales, development, tools, your pay")
    c.set_defaults(fn=cmd_cash)

    w = sub.add_parser("vw", help="Van Westendorp from CSV (part 06)")
    w.add_argument("csv")
    w.set_defaults(fn=cmd_vw)

    g = sub.add_parser("gg", help="Gabor-Granger (part 06)")
    g.add_argument("points", nargs="+", help="price:share, e.g. 900:0.62")
    g.add_argument("--cost", type=float, default=0, help="monthly COGS per office")
    g.set_defaults(fn=cmd_gg)

    n = sub.add_parser("nrr", help="net revenue retention of a cohort (part 08)")
    n.add_argument("--offices", type=int, default=100)
    n.add_argument("--platform", type=float, default=1790, help="platform fee per office per month")
    n.add_argument("--churn", type=float, default=0.01, help="monthly share of offices leaving")
    n.add_argument("--expansion", type=float, default=0.03, help="monthly share of offices adding an agent")
    n.add_argument("--agent-price", type=float, default=390)
    n.add_argument("--indexation", type=float, default=0.036, help="price increase at renewal (CPI)")
    n.set_defaults(fn=cmd_nrr)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
