# Skeleton `$OSA/`

**This is scaffolding, not a solution.** It contains only the things that are
boring to retype by hand and teach nothing: the directory structure, the
configuration template, the systemd units and the startup script.

**There is not a single line of agent logic here.** You write the gateway, the
harness, memory, tools and the rest yourself — that is the point of the course.

## Installation

    cp -r skeleton $OSA && cd $OSA && bash init.sh

## What you get

    konfiguracja/system.json     template with the `zaufanie` (trust) section (part 2)
    systemd/                     user units for the gateway and the scheduler
    init.sh                      directories, git, venv, preflight check
    .gitignore                   secrets, logs, memory kept out of the repository

## What you do NOT get — and in which part you will write it

    brama.py konfig.py sesje.py    pt. 2      harness.py            pt. 3
    kontekst.py                    pt. 4      pamiec/magazyn.py     pt. 5
    agenci/*/AGENTS.md etc.        pt. 6      narzedzia/rejestr.py  pt. 7
    kod/ (code-mode)               pt. 8      piaskownica/          pt. 10
    harmonogram/planista.py        pt. 11     kanaly/               pt. 12
    flota/                         pt. 13     ewaluacja/            pt. 14
    obserwacja/                    pt. 15     bezpieczenstwo/       pt. 16
    router/                        pt. 17     wydanie/ RUNBOOK STOP pt. 18
