# Szkielet `$OSA/`

**To jest rusztowanie, nie rozwiązanie.** Zawiera wyłącznie rzeczy, których
przepisywanie ręcznie jest nudne i niczego nie uczy: strukturę katalogów, szablon
konfiguracji, jednostki systemd i skrypt startowy.

**Nie ma tu ani jednej linii logiki agenta.** Bramę, harness, pamięć, narzędzia
i resztę piszesz sam — o to chodzi w kursie.

## Instalacja

    cp -r szkielet $OSA && cd $OSA && bash init.sh

## Co dostajesz

    konfiguracja/system.json     szablon z sekcją `zaufanie` (część 2)
    systemd/                     jednostki użytkownika dla bramy i planisty
    init.sh                      katalogi, git, venv, kontrola wstępna
    .gitignore                   sekrety, dzienniki, pamięć poza repozytorium

## Czego NIE dostajesz — i w której części to napiszesz

    brama.py konfig.py sesje.py    cz. 2      harness.py            cz. 3
    kontekst.py                    cz. 4      pamiec/magazyn.py     cz. 5
    agenci/*/AGENTS.md itd.        cz. 6      narzedzia/rejestr.py  cz. 7
    kod/ (code-mode)               cz. 8      piaskownica/          cz. 10
    harmonogram/planista.py        cz. 11     kanaly/               cz. 12
    flota/                         cz. 13     ewaluacja/            cz. 14
    obserwacja/                    cz. 15     bezpieczenstwo/       cz. 16
    router/                        cz. 17     wydanie/ RUNBOOK STOP cz. 18
