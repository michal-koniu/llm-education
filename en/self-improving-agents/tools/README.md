# Tools

One script, Python 3.10+ standard library only, no installation. It produces every **(C)** number in the guide and
lets you redo the arithmetic with your own agent's rates. The Polish copy, with Polish comments and output, is in
[`pl/agenty-samodoskonalace/narzedzia/`](../../../pl/agenty-samodoskonalace/narzedzia/README.md).

```bash
cd en/self-improving-agents/tools
python3 rare_event_stats.py all          # reproduce every table in the guide (a few seconds)
python3 rare_event_stats.py <command> -h # options for one command
```

| Command | Answers | Example | Guide |
|---|---|---|---|
| `empty` | How likely are k empty rounds in a row at rate λ, and how long must an empty run be to mean something? | `empty --rates 0.15` | [02 §1](../02-MEASURING-WITH-RARE-EVENTS.md#1-how-noisy-is-nothing-found) |
| `power` | How many hits, and rounds per arm, to show a rate ratio R? With `--proxy`, how much a denser metric helps | `power --ratios 1.5 2 --rates 0.15 --proxy 4` | [02 §2–3](../02-MEASURING-WITH-RARE-EVENTS.md#2-how-many-hits-to-show-a-change-helped) |
| `sprt` | Bounds, per-hit increments, error rates and expected length of Wald's SPRT on hit attribution, for any challenger share | `sprt --ratio 2 --share 0.25` | [02 §4](../02-MEASURING-WITH-RARE-EVENTS.md#4-decision-rules-for-small-noisy-samples) |
| `cusum` | Mean rounds to a false alarm and to detection for a Poisson CUSUM | `cusum --rate0 0.3 --rate1 0.15 --h 3 4 5` | [02 §5](../02-MEASURING-WITH-RARE-EVENTS.md#5-watching-for-a-drop-poisson-cusum) |
| `mcnemar` | Does a golden-set comparison pass the "fix more than you break" gate? | `mcnemar --b 3 --c 11` | [03 §6](../03-THE-SAFE-LOOP.md#6-the-gate-cascade) |
| `shadow` | Minimum wins out of n shadow-mode disagreements | `shadow --max-n 30` | [03 §7](../03-THE-SAFE-LOOP.md#7-shadow-mode) |
| `zero` | Upper bound on the rate after n rounds with zero hits (rule of three) | `zero --rounds 30` | [02 §6](../02-MEASURING-WITH-RARE-EVENTS.md#6-zero-events-and-new-sources) |
| `discount` | Effective memory of a discounted bandit posterior | `discount --gamma 0.98` | [03 §5](../03-THE-SAFE-LOOP.md#5-a-bandit-for-allocation-instead-of-rewrites) |

**Notes.**

- The simulations (`sprt`, `cusum`) use a fixed seed (`--seed 7`), so results are reproducible. A different seed
  moves the simulated numbers by a few percent; the exact tests (`power`, `mcnemar`, `shadow`) do not move.
- The model is a Poisson process with a constant rate. Real hit rates vary by hour, weekday and season, so treat the
  outputs as a **lower bound** on how much data you need.
- `binom_sf` can be imported by your gatekeeper: `from rare_event_stats import binom_sf`.

License: MIT, like all code in this repository ([LICENSE.md](../../../LICENSE.md)).
