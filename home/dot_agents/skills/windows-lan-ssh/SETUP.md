# One-time setup for the personal laptop

Done on 14 Sep 2026 unless a section says otherwise: OpenSSH Server, the host key in this Mac's `known_hosts`, and the agent key that `IdentityFile` names in `~/.ssh/config`. Checked 7 Nov: the key login works, the account is an administrator and its SSH sessions run elevated, and `personal-laptop.local` resolves with the VPN up. Redo a section when the runbook's connect step points here, or after Windows is reinstalled.

## SSH server

SSH isn't available until this works, so the dev runs it on the laptop, in an elevated PowerShell window:

```powershell
Get-WindowsCapability -Online | Where-Object Name -Like 'OpenSSH.Server*'
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0  # only if absent
Start-Service sshd
Set-Service sshd -StartupType Automatic
Get-NetFirewallRule -Name OpenSSH-Server-In-TCP | Enable-NetFirewallRule
```

If the firewall rule doesn't exist, create it:

```powershell
New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH Server (sshd)' `
  -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

Done when `nc -G 5 -vz "$(ssh -G personal-laptop | awk '$1=="hostname" {print $2}')" 22` on this Mac succeeds.

## Host key

Compare the fingerprint `ssh` shows with this, run on the laptop:

```powershell
ssh-keygen -lf C:\ProgramData\ssh\ssh_host_ed25519_key.pub
```

Accept the key only when the two match exactly, and stop on a mismatch. After a planned reinstall, check the new fingerprint first, then remove the old line with `ssh-keygen -R <HostName from ~/.ssh/config>`.

## Agent key

The key pair is the `IdentityFile` in `~/.ssh/config` on this Mac, and the private half never leaves it. The dev's account is an administrator, so Windows OpenSSH reads `C:\ProgramData\ssh\administrators_authorized_keys`, not the account's own `authorized_keys`. The dev logs in with their password once, typing it in their own terminal, never in chat. Then, in an elevated session, with the `.pub` line in place of `PUBLIC_KEY_LINE`:

```powershell
$key = 'PUBLIC_KEY_LINE'
$file = "$env:ProgramData\ssh\administrators_authorized_keys"
if (-not (Test-Path $file)) { New-Item -Path $file -ItemType File -Force | Out-Null }
if (-not (Get-Content $file | Where-Object { $_ -eq $key })) { Add-Content -Path $file -Value $key -Encoding ascii }
icacls.exe $file /inheritance:r /grant:r "*S-1-5-32-544:F" "SYSTEM:F"
Restart-Service sshd
```

The group SID works on Windows installs whose Administrators group has a translated name. Done when the runbook's connect step prints the account and hostname.

## Default shell

Windows OpenSSH starts `cmd.exe` unless told otherwise. Point it at PowerShell 7, installed at `C:\Program Files\PowerShell\7\pwsh.exe`. If a reinstall lost it, use Windows PowerShell, `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`, until `winget.yaml` puts it back. This changes the registry, so ask the dev first.

While the shell is still `cmd.exe`, send PowerShell as an encoded script, which survives `cmd.exe`'s quoting:

```sh
printf '%s' 'New-ItemProperty -Path HKLM:\SOFTWARE\OpenSSH -Name DefaultShell -Value "C:\Program Files\PowerShell\7\pwsh.exe" -PropertyType String -Force' > /tmp/set-shell.ps1
ssh personal-laptop "powershell -NoProfile -EncodedCommand $(iconv -f UTF-8 -t UTF-16LE /tmp/set-shell.ps1 | base64)"
```

New sessions pick it up. Done when the connect step prints the account line instead of a `cmd.exe` error.

## Transfer folder

Created 7 Nov 2026. To recreate it:

```sh
ssh personal-laptop 'New-Item -ItemType Directory -Force $HOME\transfer'
```

## Revoke access

Remove the line ending in this key's comment, the last field of its `.pub` file, from `administrators_authorized_keys`, then `Restart-Service sshd`. Delete the key pair on this Mac only when the dev asks. Report which key went and whether the dev's password login still works.
