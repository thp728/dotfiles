---
name: windows-lan-ssh
description: Work on the dev's personal Windows laptop from this Mac over SSH. Use only when the dev asks to run commands, copy files or set something up on that laptop.
---

# Personal laptop over SSH

`personal-laptop` is the dev's personal Windows laptop, an alias in `~/.ssh/config`, which holds its address, Windows account and key, and shares one connection across commands, so every step here starts with `ssh personal-laptop`. Both machines have to be on the same Wi-Fi network. One-time setup lives in [SETUP.md](SETUP.md): read it only when a step here sends you there.

In replies, write the laptop's paths, Windows or Ubuntu, as plain text. T3 turns a path in code formatting into a link to a file on this Mac.

## Connect

```sh
ssh personal-laptop '$p = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent(); "$env:USERNAME on $env:COMPUTERNAME, admin: $($p.IsInRole(544))"'
```

Connected when it prints the Windows account from `~/.ssh/config`'s `User` line and the laptop's machine name. `admin: True` means every command runs with administrator rights and no UAC prompt, which is why the ask-first list below matters. When it fails:

- `Could not resolve hostname`, or a timeout: the laptop is asleep, off or on another network. Ask the dev to wake it and join this Mac's Wi-Fi, then connect again.
- No output after 10 seconds: the shared connection is stale. Run `ssh -O exit personal-laptop`, then connect again.
- `Connection refused`: the SSH server isn't running. Follow SETUP.md, "SSH server".
- `Permission denied (publickey)`: the agent key isn't installed. Follow SETUP.md, "Agent key".
- A host key warning: stop and tell the dev. SETUP.md, "Host key", covers checking it.
- Output that looks like `cmd.exe`, such as `'$p' is not recognized`: the default shell isn't set. Follow SETUP.md, "Default shell".

## Run commands

Run each command as its own `ssh` call and check its exit code. Commands land in PowerShell 7.

```sh
ssh personal-laptop 'Get-ChildItem $HOME'
ssh personal-laptop 'wsl -d Ubuntu --shell-type login -- gh --version'
```

Linux commands run as the default user `thp728`. `--shell-type login` runs them in zsh as a login shell, so `.zprofile` puts Homebrew's and mise's tools on PATH. `bash -lc` skips `.zprofile` and finds none of them. That puts three shells in one line: this Mac's, PowerShell, then zsh. PowerShell fills in `$VAR` inside double quotes before zsh sees it, and `wsl.exe` joins its arguments into one line, which can drop nested quotes. Once a command needs quotes, pipes or `$` inside Linux, pass it as base64, which no shell along the way can mangle:

```sh
b64=$(printf '%s' 'echo "$HOME"; gh auth status' | base64 | tr -d '\n')
ssh personal-laptop "wsl -d Ubuntu -- zsh -l -c 'echo $b64 | base64 -d | zsh -l'"
```

PowerShell commands have the same problem: nested quotes and regexes fail with `ParserError`. Write those to a file and pass it as UTF-16 base64:

```sh
ssh personal-laptop "pwsh -NoProfile -EncodedCommand $(iconv -f UTF-8 -t UTF-16LE /tmp/cmd.ps1 | base64)"
```

Interactive prompts, such as a sign-in, can fail through these layers. Have the dev run those in an Ubuntu window on the laptop.

`sudo` needs the dev's password, so root work, such as `apt`, runs with `wsl -d Ubuntu -u root` instead. `wsl.exe` prints its own messages, such as `wsl --list`, in UTF-16, so prefix those with `$env:WSL_UTF8=1;` to get readable text.

Before changing a repo on the laptop, read its `AGENTS.md` and `git status`.

## Copy files

Every copy from this Mac waits for the dev's yes. Files go through `%USERPROFILE%\transfer`, which Ubuntu sees as /mnt/c/Users/<account>/transfer, with `<account>` the `User` in `~/.ssh/config`, which SETUP.md, "Transfer folder", creates:

```sh
scp FILE personal-laptop:transfer/
ssh personal-laptop "wsl -d Ubuntu -- cp '/mnt/c/Users/<account>/transfer/FILE' ~/"
ssh personal-laptop 'Remove-Item $HOME\transfer\FILE'
```

Done when the file is where the task needs it and `transfer` is empty again.

## Ask the dev first

Read-only commands and changes to what the task names go ahead. These wait for the dev's yes:

- a reboot or shutdown
- installing or uninstalling software, including `winget`, `wsl --install` and `apt`
- deleting files outside the task
- changing Windows settings, the registry or services
- copying anything from this Mac to the laptop

## After a reboot

Close the shared connection with `ssh -O exit personal-laptop`, then connect again every 30 seconds for up to five minutes. Still unreachable after that: ask the dev to check the laptop.
