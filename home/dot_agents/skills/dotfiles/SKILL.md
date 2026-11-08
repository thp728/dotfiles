---
name: dotfiles
description: Sync this machine's portable config with the chezmoi repo at ~/repos/dotfiles. Use after editing a file it manages (shell, git, starship, Ghostty, fzf, mise, uv, atuin, ~/.agents/AGENTS.md), before applying it, or when adding config that isn't work-only.
---

# Portable dotfiles

`~/repos/dotfiles` is a chezmoi source, rooted at `home/`, published on GitHub as `thp728/dotfiles`. A machine without GitHub access pushes it through `relay`, and the personal laptop's copies pull from its relay mirror. It holds config for every machine: this Mac, and Ubuntu under WSL plus a small Windows layer on the personal machine. `chezmoi managed` lists every file it tracks. On a work machine, the `dotfiles-work` skill covers the second source that sits on top.

## Sync

Agents and apps edit the live files in `$HOME`, so the repo drifts behind them. Sync with:

```sh
~/repos/dotfiles/.tools/sync.sh               # re-add, then apply
~/repos/dotfiles/.tools/sync.sh --re-add-only # after editing a managed file
```

Templates are the exception: `chezmoi re-add` skips them, and `sync.sh` names them when they drift. `chezmoi managed --include templates` lists them. Make the edit in the source under `home/` instead, then `chezmoi apply`. `~/.agents/AGENTS.md` is one, and so are `.zprofile` and `.gitconfig`.

Colors live in `home/.chezmoidata/t3.toml`. Change them there, run `chezmoi apply`, then `python3 themes/editor-colors.py` for the editors. Cursor and VS Code share the keys in `home/.chezmoidata/editor.jsonc`. Change a shared key there, since a change made in an editor's settings reverts on the next apply.

Commit source edits before `chezmoi add`, since its auto-commit takes every pending change. After `npx skills add`, run `chezmoi add` on the new skill folder and the lock file.

Done when the script prints `in sync`. `cz apply`, `cz diff`, `cz status` and `cz verify` run the same command against this repo and then the work repo, where one exists.

## Which repo a file belongs in

Anything that names the employer, its hosts, projects, accounts, work identity or work-only tools goes in the work repo. Everything else goes here. When a file mixes both, keep the portable part here and move the work lines into a local file that the work repo owns and the portable file reads: `~/.config/zsh/local/*.zsh`, `~/.config/git/local.gitconfig`, `~/.config/mise/conf.d/work.toml`, `~/.agents/AGENTS.work.md`.

A gitleaks pre-commit hook blocks secrets with `.gitleaks.toml`, or with `~/.config/gitleaks/work.toml` on a machine that has one, which adds that machine's own strings. When it blocks a commit, move the line to the work repo and commit again. Hooks don't travel in bundles, so run `.tools/install-hooks.sh` after every clone. `.tools/check.sh` runs the scans plus chezmoi's health checks.

## Machine data

Each machine answers `home/.chezmoi.toml.tmpl` once, at `chezmoi init`: `work`, the git name and email, and the notes vault, profile and index paths. The answers live in `~/.config/chezmoi/chezmoi.toml`, outside the repo, so a machine-specific value stays out of history. Templates branch on `.work` and `.chezmoi.os`.

## Leaving this machine

Ask the dev before pushing the repo anywhere or copying it, or a bundle of it, off this machine. Backups run on demand only: `.tools/backup.sh`, with `DOTFILES_BACKUP_DIR` set.
