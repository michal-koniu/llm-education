"""The LLM security lab: a deliberately vulnerable assistant ("Sieve") plus the tools
to attack it, measure attack success rate (ASR) and test defences.

Everything binds to 127.0.0.1. Nothing leaves your machine: e-mail goes to a file,
the "internet" is a local fixture server, the "attacker" is a local logging server.

Run every command from the directory that CONTAINS this package, e.g.:

    LLM_BASE_URL=mock python3 -m unittest discover lab/tests
    python3 -m lab.harness --cases lab/cases/part02.jsonl --defenses none --k 5
"""

__version__ = "1.0"
