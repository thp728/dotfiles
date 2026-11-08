# T3 Code's default dark theme

Where the T3 colors in [`home/.chezmoidata/t3.toml`](../home/.chezmoidata/t3.toml) come from. That
file is the one copy the tools use: chezmoi renders Ghostty's `t3-dark` theme, starship's `t3`
palette and `fzfrc` from it, and [`themes/editor-colors.py`](../themes/editor-colors.py) reads it
for Cursor, VS Code, and Obsidian in the notes vault. Change a color there, not here. Read on 5 Nov 2026 from T3 Code 0.1.7's own
files: the stylesheet `apps/server/dist/client/assets/main-C6Cjx1mu.css` and the terminal drawer
script `ThreadTerminalDrawer-9EIdX1Sz.js`, inside
`/Applications/T3 Code (Beta).app/Contents/Resources/app.asar`. The dev runs the default theme: no
theme id is stored, and `~/.t3/userdata/themes` is empty. T3 also ships `ember`, `grove`, `iris`,
`ocean` and `t3-chat`. oklch values are converted to sRGB hex.

## App colors (`:root:is(.dark)`)

| Token | Value | Use |
| --- | --- | --- |
| `--background` | `#000000` | window background |
| `--card`, `--popover`, `--surface-raised` | `#111111` | panels, menus, raised surfaces |
| `--message-surface` | `#1e1e1e` | your messages |
| `--foreground` | `#f5f5f5` (neutral-100) | text |
| `--muted-foreground` | `#a1a1a1` (neutral-400) | secondary text |
| `--border` | `#ffffff14` (white 8%, about `#141414` on black) | borders |
| `--input` | `#ffffff1c` (white 11%) | input borders |
| `--accent` | `#ffffff0a` (white 4%) | hover and selection fills |
| `--secondary`, `--muted` | `#ffffff08` (white 3%) | subtle fills |
| `--primary`, `--ring` | `#346bf1`, oklch(57.1% .21 264) | accent blue, buttons, focus |
| `--error` | `#fb414a`, text `#ff6467` | errors |
| `--success` | `#00bc7d`, text `#00d492` | success, diff additions |
| `--warning` | `#fe9a00`, text `#ffb900` | warnings |
| `--info` | `#2b7fff`, text `#51a2ff` | info, modified files |

The sidebar (`[data-app-sidebar]` dark) uses `#000000` with text `#f1f3f7`, hover `#191a1d`, muted
fill `#0a0a0a` and muted text `#a3a3a3`.

## Terminal

Background `--terminal-background`, which is `--background` (`#000000`). Foreground `#f5f5f5`.
Cursor `#b4cbff`. Selection `#b4cbff40` (the cursor blue at 25%). The 16 ANSI colors, from `Rn.dark`,
are VS Code's default dark terminal palette:

| | black | red | green | yellow | blue | magenta | cyan | white |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| normal | `#000000` | `#cd3131` | `#0dbc79` | `#e5e510` | `#2472c8` | `#bc3fbc` | `#11a8cd` | `#e5e5e5` |
| bright | `#666666` | `#f14c4c` | `#23d18b` | `#f5f543` | `#3b8eea` | `#d670d6` | `#29b8db` | `#e5e5e5` |

## Code highlighting

T3 highlights code and diffs with the Pierre themes (`pierre-dark` and its soft, vibrant and
color-vision variants). The same theme is on Open VSX as `pierrecomputer.pierre-theme` (1.0.3),
installable in Cursor and VS Code.

## Fonts

The dev's T3 settings set the code font to `JetBrainsMono Nerd Font`, at 13 px for code and 12 px
for the terminal.
