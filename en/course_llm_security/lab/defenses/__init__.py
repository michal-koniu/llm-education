"""Named defence configurations.

CONFIGS maps a name to a list of Defense instances:

    CONFIGS = {"none": []}

Later parts add defences in two equivalent ways:

  1. edit this file: import your class and add e.g.
         CONFIGS["p05-canary"] = [OutputCanaryCheck()]
  2. or put a module in this folder that registers itself:
         # lab/defenses/canary.py
         from lab.defenses import CONFIGS
         from lab.defenses.base import Defense, Verdict
         class OutputCanaryCheck(Defense): ...
         CONFIGS["p05-canary"] = [OutputCanaryCheck()]
     Every module in this folder is imported automatically (base.py first).

On the command line, "a+b" combines configs: --defenses p05-canary+p07-taint
"""
from __future__ import annotations

import importlib
import pkgutil

from .base import ALLOW, Context, Defense, Verdict  # noqa: F401  (re-exported)

CONFIGS: dict[str, list] = {"none": []}


def _discover() -> None:
    for mod in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
        if mod.name != "base" and not mod.name.startswith("_"):
            importlib.import_module(f"{__name__}.{mod.name}")


_discover()


def get_config(spec) -> list:
    """'none' -> [], 'a+b' -> CONFIGS['a'] + CONFIGS['b']; a list of Defense passes through."""
    if not isinstance(spec, str):
        return list(spec)
    out = []
    for part in spec.split("+"):
        part = part.strip()
        if part not in CONFIGS:
            raise KeyError(f"unknown defence config {part!r}; known: {', '.join(sorted(CONFIGS))}")
        out.extend(CONFIGS[part])
    return out
