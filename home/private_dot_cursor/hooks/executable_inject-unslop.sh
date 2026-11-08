#!/bin/bash
set -euo pipefail

payload=$(cat)

# Cursor can't read user-level instructions from a file, so this hook is how the global
# AGENTS.md (which Codex reads directly) and the writing rules reach every Cursor session.
agents="$HOME/.agents/AGENTS.md"
skill="$HOME/.agents/skills/unslop/SKILL.md"

# AGENTS.override.md is a local, untracked supplement to a project's AGENTS.md. Codex reads it
# natively; Cursor only gets it from here. A git worktree without its own copy uses the one at the
# same path in the main checkout, since untracked files don't follow new worktrees.
override_for() {
  local root top common main
  root=$(cd "$1" 2>/dev/null && pwd -P) || return 0
  if [[ -r "$root/AGENTS.override.md" ]]; then
    printf '%s\n' "$root/AGENTS.override.md"
    return 0
  fi
  top=$(git -C "$root" rev-parse --show-toplevel 2>/dev/null) || return 0
  common=$(git -C "$root" rev-parse --path-format=absolute --git-common-dir 2>/dev/null) || return 0
  main=${common%/.git}
  [[ "$main" != "$common" && "$main" != "$top" ]] || return 0
  if [[ -r "$main${root#"$top"}/AGENTS.override.md" ]]; then
    printf '%s\n' "$main${root#"$top"}/AGENTS.override.md"
  fi
}

parts=()
[[ -r "$agents" ]] && parts+=("Global instructions, from ~/.agents/AGENTS.md:"$'\n\n'"$(cat "$agents")")

while IFS= read -r root; do
  [[ -n "$root" ]] || continue
  override=$(override_for "$root")
  [[ -n "$override" ]] || continue
  parts+=("Local instructions for $root, from $override. They're untracked and take precedence over the project's AGENTS.md:"$'\n\n'"$(cat "$override")")
done < <(printf '%s' "$payload" | jq -r '.workspace_roots[]? // empty' 2>/dev/null || true)

[[ -r "$skill" ]] && parts+=("Apply these writing instructions to every response:"$'\n\n'"$(cat "$skill")")

if (( ${#parts[@]} == 0 )); then
  printf '{}\n'
  exit 0
fi

printf '%s\n\n' "${parts[@]}" | jq -Rs '{additional_context: .}'
