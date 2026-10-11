#!/usr/bin/env bash
# Odtwarza środowisko od zera. Wymagany przez harness (część 3).
set -euo pipefail
cd "$(dirname "$0")"

echo "1/6 · katalogi"
mkdir -p decyzje pomiary dziennik agenci narzedzia kod piaskownica \
         harmonogram kanaly flota pamiec ewaluacja obserwacja \
         bezpieczenstwo router wydania wydanie testy/ucieczka testy/ataki
mkdir -p ~/.local/run ~/.config/osa

echo "2/6 · zależności systemowe"
for p in bwrap systemd-run sqlite3 git python3; do
  command -v "$p" >/dev/null || { echo "✗ brak: $p"; exit 1; }
done
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,12) else 1)' \
  || { echo "✗ wymagany Python ≥ 3.12"; exit 1; }

echo "3/6 · środowisko wirtualne"
[ -d .venv ] || python3 -m venv .venv
./.venv/bin/pip -q install --upgrade pip

echo "4/6 · git"
[ -d .git ] || { git init -q && git add -A && git commit -qm "szkielet"; }

echo "5/6 · sekrety (poza repozytorium, w ~/.config/osa - sekrety nie leżą w katalogu projektu)"
if [ ! -f ~/.config/osa/sekrety.json ]; then
  echo '{}' > ~/.config/osa/sekrety.json
  chmod 600 ~/.config/osa/sekrety.json
fi
[ "$(stat -c %a ~/.config/osa/sekrety.json)" = "600" ] \
  || { echo "✗ sekrety.json musi mieć 0600"; exit 1; }

echo "6/6 · jednostki systemd z pełną ścieżką projektu"
mkdir -p systemd/wygenerowane
for u in systemd/*.service; do
  sed "s#@OSA@#$PWD#g" "$u" > "systemd/wygenerowane/$(basename "$u")"
done

echo
echo "✓ gotowe. Dalej: kurs2/01-ARCHITEKTURY-AGENTOWE.md"
echo "  systemd:  cp systemd/wygenerowane/*.service ~/.config/systemd/user/ && systemctl --user daemon-reload"
