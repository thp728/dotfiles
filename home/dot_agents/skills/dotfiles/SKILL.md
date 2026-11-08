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

T3's recurring scheduled tasks live only in T3's database, and `~/.config/t3-schedules/` is their source, one file per task. The portable ones are templates that render only on a machine with the vault paths their prompt needs, and work-only ones come from the work repo. After creating or changing a task, run `t3-schedules check`. For a new task, `t3-schedules export '<title>'` prints its file. For a changed one, edit its source, apply, and call `schedule_task` with the arguments the check prints.

Colors live in `home/.chezmoidata/t3.toml`. Change them there, run `chezmoi apply`, then `python3 themes/editor-colors.py` for the editors. Cursor and VS Code share the keys in `home/.chezmoidata/editor.jsonc`. Change a shared key there, since a change made in an editor's settings reverts on the next apply.

Commit source edits before `chezmoi add`, since its auto-commit takes every pending change. After `npx skills add`, run `chezmoi add` on the new skill folder and the lock file.

Without a terminal, as over SSH, `chezmoi apply` waits forever on its overwrite prompt for a file changed outside chezmoi. Run `chezmoi status` first, deal with each `MM` file, then apply with `--force`.

Done when the script prints `in sync`. `cz apply`, `cz diff`, `cz status` and `cz verify` run the same command against this repo and then the work repo, where one exists.

## Which repo a file belongs in

Anything that names the employer, its hosts, projects, accounts, work identity or work-only tools goes in the work repo. Everything else goes here. When a file mixes both, keep the portable part here and move the work lines into a local file that the work repo owns and the portable file reads: `~/.config/zsh/local/*.zsh`, `~/.config/git/local.gitconfig`, `~/.config/mise/conf.d/work.toml`, `~/.agents/AGENTS.work.md`.

A tool that writes to `~/.gitconfig`, such as `gh auth setup-git`, puts machine settings in a generated file. Move its lines into `~/.config/git/local.gitconfig`, which `~/.gitconfig` includes last.

A gitleaks pre-commit hook blocks secrets with `.gitleaks.toml`, or with `~/.config/gitleaks/work.toml` on a machine that has one, which adds that machine's own strings. When it blocks a commit, move the line to the work repo and commit again. Hooks don't travel in bundles, so run `.tools/install-hooks.sh` after every clone. `.tools/check.sh` runs the scans plus chezmoi's health checks.

If chezmoi doctor's hardlink test fails with `invalid cross-device link`, rerun the check with TMPDIR set to an existing directory on the source repo's filesystem, such as `$HOME/.cache` in Ubuntu.

## Machine data

Each machine answers `home/.chezmoi.toml.tmpl` once, at `chezmoi init`: `work`, the git name and email, and the notes vault, profile and index paths. The answers live in `~/.config/chezmoi/chezmoi.toml`, outside the repo, so a machine-specific value stays out of history. Templates branch on `.work` and `.chezmoi.os`.

## Leaving this machine

Ask the dev before pushing the repo anywhere or copying it, or a bundle of it, off this machine. Backups run on demand only: `.tools/backup.sh`, with `DOTFILES_BACKUP_DIR` set.
