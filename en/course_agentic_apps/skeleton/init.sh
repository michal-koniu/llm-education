#!/usr/bin/env bash
# Recreates the environment from scratch. Required by the harness (part 3).
set -euo pipefail
cd "$(dirname "$0")"

echo "1/6 · directories"
mkdir -p decyzje pomiary dziennik agenci narzedzia kod piaskownica \
         harmonogram kanaly flota pamiec ewaluacja obserwacja \
         bezpieczenstwo router wydania wydanie testy/ucieczka testy/ataki
mkdir -p ~/.local/run ~/.config/osa

echo "2/6 · system dependencies"
for p in bwrap systemd-run sqlite3 git python3; do
  command -v "$p" >/dev/null || { echo "✗ missing: $p"; exit 1; }
done
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,12) else 1)' \
  || { echo "✗ Python ≥ 3.12 required"; exit 1; }

echo "3/6 · virtual environment"
[ -d .venv ] || python3 -m venv .venv
./.venv/bin/pip -q install --upgrade pip

echo "4/6 · git"
[ -d .git ] || { git init -q && git add -A && git commit -qm "skeleton"; }

echo "5/6 · secrets (outside the repository, in ~/.config/osa - secrets do not live in the project directory)"
if [ ! -f ~/.config/osa/sekrety.json ]; then
  echo '{}' > ~/.config/osa/sekrety.json
  chmod 600 ~/.config/osa/sekrety.json
fi
[ "$(stat -c %a ~/.config/osa/sekrety.json)" = "600" ] \
  || { echo "✗ sekrety.json must be 0600"; exit 1; }

echo "6/6 · systemd units with the full project path"
mkdir -p systemd/wygenerowane
for u in systemd/*.service; do
  sed "s#@OSA@#$PWD#g" "$u" > "systemd/wygenerowane/$(basename "$u")"
done

echo
echo "✓ done. Next: kurs2/01-AGENT-ARCHITECTURES.md"
echo "  systemd:  cp systemd/wygenerowane/*.service ~/.config/systemd/user/ && systemctl --user daemon-reload"
