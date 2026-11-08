#!/bin/sh
# Hooks don't travel in git bundles, so rerun this after every clone.
set -eu

repo="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
hook="$repo/.git/hooks/pre-commit"

cat > "$hook" <<'HOOK'
#!/bin/sh
# A machine's ~/.config/gitleaks/work.toml layers its own rules on the repo's, so prefer it.
repo="$(git rev-parse --show-toplevel)"
rules="$HOME/.config/gitleaks/work.toml"
[ -f "$rules" ] || rules="$repo/.gitleaks.toml"
exec gitleaks git --pre-commit --staged --redact --no-banner --config "$rules"
HOOK
chmod +x "$hook"
echo "installed $hook"
