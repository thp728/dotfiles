#!/bin/sh
# Pull edits made in $HOME back into the repo, then apply the repo to $HOME.
# Usage: sync.sh [--re-add-only]
set -eu

chezmoi re-add

drifted="$(chezmoi status | awk 'substr($0, 1, 1) == "M" { print $2 }')"
if [ -n "$drifted" ]; then
  echo "still drifted after re-add, probably templates. Fix these by hand:" >&2
  echo "$drifted" >&2
  exit 1
fi

if [ "${1:-}" != "--re-add-only" ]; then
  chezmoi apply
fi

echo "in sync"
