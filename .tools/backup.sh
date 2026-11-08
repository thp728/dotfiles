#!/bin/sh
# On-demand backup: writes one verified bundle file to DOTFILES_BACKUP_DIR.
# The repo itself must never live in a synced folder, only bundles.
set -eu

: "${DOTFILES_BACKUP_DIR:?set DOTFILES_BACKUP_DIR to the folder that keeps the bundles}"
repo="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
name="$(basename "$repo")"
dest="$DOTFILES_BACKUP_DIR"
keep="${DOTFILES_BACKUP_KEEP:-5}"

mkdir -p "$dest"
file="$dest/$name-$(date +%Y%m%d-%H%M%S).bundle"

git -C "$repo" bundle create "$file" --all
git -C "$repo" bundle verify "$file" >/dev/null
echo "wrote $file"

find "$dest" -maxdepth 1 -name "$name-*.bundle" | sort -r | tail -n +"$((keep + 1))" | while read -r old; do
  rm -f "$old"
  echo "removed $old"
done
