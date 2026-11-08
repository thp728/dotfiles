#!/bin/sh
# Secret scan, with a machine's extra rules where it has them, plus chezmoi health.
# Fails when $HOME has drifted from the repo; .tools/sync.sh fixes that.
set -eu

repo="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
cd "$repo"

for f in .tools/*.sh; do sh -n "$f"; done

# A machine's ~/.config/gitleaks/work.toml layers its own rules on the repo's, so prefer it.
rules="$HOME/.config/gitleaks/work.toml"
[ -f "$rules" ] || rules=.gitleaks.toml
gitleaks git --redact --no-banner --config "$rules" .
gitleaks dir --redact --no-banner --config "$rules" .

if ! out="$(chezmoi doctor)"; then printf '%s\n' "$out"; exit 1; fi
printf '%s\n' "$out" | awk '$1 == "warning"'

if ! chezmoi verify --exclude scripts; then
  echo "drift between \$HOME and the repo: run .tools/sync.sh" >&2
  exit 1
fi
echo "check passed"
