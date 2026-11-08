#!/usr/bin/env python3
"""Write T3 Code's window colors and a softened Ayu Dark into Cursor's and VS Code's settings.json,
and into Obsidian for the notes vault.

Owns three keys in each settings file: workbench.colorCustomizations,
editor.tokenColorCustomizations and editor.semanticTokenColorCustomizations. In the vault named
by chezmoi's notesVault it owns .obsidian/snippets/t3.css, plus the accentColor, theme and
enabledCssSnippets keys in .obsidian/appearance.json. Edit this script, not those, then run it.
T3's colors come from home/.chezmoidata/t3.toml. The gray text shades, extra border alphas and
button hover below are local choices.

    python3 themes/editor-colors.py            # write both settings files and the vault snippet
    python3 themes/editor-colors.py --print    # print the three keys instead
"""

import colorsys
import glob
import json
import math
import os
import sys
import tomllib
from pathlib import Path

THEME = "[Ayu Dark]"
SATURATION = 0.8  # chroma kept from Ayu's colors, 1.0 is the original theme
SETTINGS = [
    "~/Library/Application Support/Cursor/User/settings.json",
    "~/Library/Application Support/Code/User/settings.json",
]

with open(Path(__file__).resolve().parent.parent / "home/.chezmoidata/t3.toml", "rb") as f:
    T3 = tomllib.load(f)["t3"]
TERMINAL = T3["terminal"]

BACKGROUND = T3["background"]
CARD = T3["card"]
RAISED = T3["message_surface"]
ACCENT = T3["accent"]
BORDER = T3["border"]
INPUT = T3["input"]
MUTED_TEXT = T3["muted_foreground"]
BLUE = T3["primary"]
LINK = T3["info_text"]
CURSOR = TERMINAL["cursor"]
ACTIVE_TEXT = "#d4d4d4"
FAINT_BORDER = "#ffffff0f"
NONE = "#00000000"

ANSI_NAMES = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]

# T3 Code's dark theme, written over whatever Ayu sets.
WINDOW = {
    "editor.background": BACKGROUND,
    "editorGutter.background": BACKGROUND,
    "editor.lineHighlightBackground": ACCENT,
    "editor.lineHighlightBorder": NONE,
    "editorLineNumber.foreground": "#4d4d4d",
    "editorLineNumber.activeForeground": MUTED_TEXT,
    "editorCursor.foreground": CURSOR,
    "editorWidget.background": CARD,
    "editorHoverWidget.background": CARD,
    "editorSuggestWidget.background": CARD,
    "editorSuggestWidget.selectedBackground": BORDER,
    "editorGroupHeader.tabsBackground": BACKGROUND,
    "editorGroupHeader.noTabsBackground": BACKGROUND,
    "editorGroupHeader.connectedTabsBackground": BACKGROUND,
    "tab.activeBackground": CARD,
    "tab.inactiveBackground": BACKGROUND,
    "tab.activeBorderTop": BLUE,
    "tab.activeBorder": NONE,
    "breadcrumb.background": BACKGROUND,
    "sideBar.background": BACKGROUND,
    "sideBarSectionHeader.background": BACKGROUND,
    "activityBar.background": BACKGROUND,
    "activityBar.foreground": ACTIVE_TEXT,
    "activityBar.activeBorder": BLUE,
    "activityBarBadge.background": BLUE,
    "activityBarBadge.foreground": "#ffffff",
    "titleBar.activeBackground": BACKGROUND,
    "titleBar.inactiveBackground": BACKGROUND,
    "statusBar.background": BACKGROUND,
    "statusBar.noFolderBackground": BACKGROUND,
    "statusBar.debuggingBackground": BLUE,
    "panel.background": BACKGROUND,
    "panelTitle.activeBorder": BLUE,
    "input.background": CARD,
    "input.border": INPUT,
    "dropdown.background": CARD,
    "dropdown.border": INPUT,
    "quickInput.background": CARD,
    "menu.background": CARD,
    "notifications.background": CARD,
    "list.activeSelectionBackground": BORDER,
    "list.inactiveSelectionBackground": ACCENT,
    "list.hoverBackground": ACCENT,
    "list.focusOutline": BLUE,
    "focusBorder": BLUE,
    "button.background": BLUE,
    "button.hoverBackground": "#4a7cf3",
    "button.foreground": "#ffffff",
    "badge.background": BLUE,
    "badge.foreground": "#ffffff",
    "progressBar.background": BLUE,
    "textLink.foreground": LINK,
    "textLink.activeForeground": LINK,
    "scrollbarSlider.background": BORDER,
    "scrollbarSlider.hoverBackground": "#ffffff1f",
    "scrollbarSlider.activeBackground": "#ffffff29",
    "minimap.background": BACKGROUND,
    "terminal.background": TERMINAL["background"],
    "terminal.foreground": TERMINAL["foreground"],
    "terminalCursor.foreground": CURSOR,
    "terminal.selectionBackground": TERMINAL["selection"],
    **{f"terminal.ansi{name}": TERMINAL["ansi"][i] for i, name in enumerate(ANSI_NAMES)},
    **{f"terminal.ansiBright{name}": TERMINAL["ansi"][i + 8] for i, name in enumerate(ANSI_NAMES)},
    # VS Code 1.144's modern layout reads its own keys.
    "modernUI.shellBackground": BACKGROUND,
    "modernUI.inactiveShellBackground": BACKGROUND,
    "modernActivityBar.background": BACKGROUND,
    "modernActivityBar.inactiveBackground": BACKGROUND,
    "modernActivityBarItem.activeBackground": BORDER,
    "modernActivityBarItem.activeForeground": ACTIVE_TEXT,
    "modernActivityBarItem.hoverBackground": ACCENT,
    "modernActivityBarItem.hoverForeground": ACTIVE_TEXT,
    "modernEditorTab.activeBackground": BORDER,
    "modernEditorTab.activeForeground": ACTIVE_TEXT,
    "modernEditorTab.activeHoverBackground": BORDER,
    "modernEditorTab.hoverBackground": ACCENT,
    "modernEditorTab.hoverForeground": ACTIVE_TEXT,
    "modernEditorTab.inactiveBackground": NONE,
    "modernEditorTab.activeActionBackground": RAISED,
    "modernEditorTab.activeHoverActionBackground": RAISED,
    "modernEditorTab.hoverActionBackground": CARD,
    "modernEditorTab.selectedActionBackground": RAISED,
    "modernTab.activeBackground": BORDER,
    "modernTab.activeForeground": ACTIVE_TEXT,
    "modernTab.hoverBackground": ACCENT,
    "modernTab.hoverForeground": ACTIVE_TEXT,
    "modernSash.gripForeground": "#ffffff2b",
    "surface.background": BACKGROUND,
    "surface.foreground": MUTED_TEXT,
    "chat.requestBackground": RAISED,
    "multiDiffEditor.background": BACKGROUND,
    "welcomePage.tileBackground": CARD,
}

# The only borders left: between split editors, around the bottom panel, and around floating widgets.
KEPT_BORDERS = {
    "editorGroup.border", "panel.border", "modernPanel.border", "widget.border",
    "editorWidget.border", "editorHoverWidget.border", "editorSuggestWidget.border",
    "menu.border", "notifications.border", "inlineChat.border", "inlineChatInput.border",
    "debugExceptionWidget.border", "pickerGroup.border",
}

# Ayu's code-colored UI keys, which follow the softened code text instead of the window text.
CODE_TEXT_KEYS = {"editor.foreground", "textPreformat.foreground",
                  "symbolIcon.textForeground", "symbolIcon.variableForeground"}

# Ayu's dark navy backgrounds, mapped to T3's black and card grays.
NAVY = {"0d1017": BACKGROUND, "10141c": CARD, "141821": CARD,
        "161a24": RAISED, "1b1f29": RAISED}
AYU_BORDERS = {"1b1f29", "171a23", "141821"}
AYU_GOLD = {"e6b450", "deae4d", "e2b14f"}


def parse(h):
    h = h.lstrip("#")
    rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    alpha = h[6:8] if len(h) == 8 else ""
    return rgb, alpha


def to_oklch(rgb):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = map(lin, rgb)
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(A, B), math.atan2(B, A)


def from_oklch(L, C, H):
    A, B = C * math.cos(H), C * math.sin(H)
    l = (L + 0.3963377774 * A + 0.2158037573 * B) ** 3
    m = (L - 0.1055613458 * A - 0.0638541728 * B) ** 3
    s = (L - 0.0894841775 * A - 1.2914855480 * B) ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)

    def enc(c):
        c = max(0.0, min(1.0, c))
        c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
        return round(c * 255)
    return "#%02x%02x%02x" % tuple(map(enc, rgb))


def soften(hex_color, text=False):
    """Scale chroma by SATURATION and dim lightness a little with it, keeping the hue and alpha."""
    rgb, alpha = parse(hex_color)
    if text and alpha:
        rgb = tuple(round(c * int(alpha, 16) / 255) for c in rgb)
        alpha = ""
    L, C, H = to_oklch(rgb)
    lightness = 1 - (1 - SATURATION) * (0.175 if text else 0.125)
    return from_oklch(L * lightness, C * SATURATION, H) + alpha


def is_text(hex_color):
    return hex_color.lower().startswith("#fcf8ec")


def code_color(hex_color):
    if hex_color.lower() == "#5a6673":
        return hex_color  # comments stay as they are
    if is_text(hex_color):
        return soften(hex_color, text=True)
    return soften(hex_color)


def window_color(key, value):
    rgb_hex = value.lower()[1:7]
    alpha = value.lower()[7:9]
    is_border = "border" in key.lower()
    if is_border and rgb_hex in AYU_BORDERS:
        return FAINT_BORDER if key in KEPT_BORDERS else NONE
    if rgb_hex == "475266":
        return NONE if alpha == "00" else "#ffffff" + ("0f" if alpha == "33" else "14")
    if rgb_hex in NAVY and not is_border:
        return NAVY[rgb_hex]
    if key in CODE_TEXT_KEYS:
        return code_color(value)
    if rgb_hex in ("c4d6fe", "fcf8ec"):
        if alpha == "bd":
            return ACTIVE_TEXT
        if "foreground" in key.lower() and int(alpha or "ff", 16) >= 0x6b:
            return MUTED_TEXT
        return "#ffffff" + alpha
    if rgb_hex == "765b24":
        return "#ffffff" + alpha
    if rgb_hex in AYU_GOLD and "warning" not in key.lower():
        if "foreground" in key.lower():
            return LINK
        return BLUE + alpha
    rgb, _ = parse(value)
    if to_oklch(rgb)[1] > 0.03:
        return soften(value)
    return value


def build(ayu):
    colors = {k: window_color(k, v) for k, v in ayu["colors"].items()}
    colors.update(WINDOW)
    for key in KEPT_BORDERS:
        colors[key] = FAINT_BORDER
    bracket_sources = ["#ffb454", "#d2a6ff", "#59c2ff"]
    for i, source in enumerate(bracket_sources, 1):
        colors[f"editorBracketHighlight.foreground{i}"] = soften(source)
    colors["editorBracketHighlight.unexpectedBracket.foreground"] = soften("#d95757")

    rules = []
    for rule in ayu["tokenColors"]:
        settings = dict(rule.get("settings", {}))
        if "foreground" in settings:
            settings["foreground"] = code_color(settings["foreground"])
        rules.append({k: v for k, v in {**rule, "settings": settings}.items() if k != "name"})

    semantic = {}
    for selector, style in ayu.get("semanticTokenColors", {}).items():
        if isinstance(style, str):
            semantic[selector] = code_color(style)
        else:
            semantic[selector] = {**style, "foreground": code_color(style["foreground"])}

    return {
        "workbench.colorCustomizations": {THEME: dict(sorted(colors.items()))},
        "editor.tokenColorCustomizations": {THEME: {"textMateRules": rules}},
        "editor.semanticTokenColorCustomizations": {THEME: {"rules": semantic}},
    }


def value_span(text, start):
    """Return the end index of the JSON value starting at text[start], skipping strings and comments."""
    depth, i = 0, start
    while i < len(text):
        ch = text[i]
        if ch == '"':
            i += 1
            while text[i] != '"':
                i += 2 if text[i] == "\\" else 1
        elif text.startswith("//", i):
            i = text.index("\n", i)
            continue
        elif ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1
            if depth == 0:
                return i + 1
        elif depth == 0 and ch in ",\n":
            return i
        i += 1
    raise ValueError("unterminated value")


def write_key(text, key, value):
    rendered = json.dumps(value, indent=2).replace("\n", "\n  ")
    marker = f'\n  "{key}":'
    at = text.find(marker)
    if at >= 0:
        start = at + len(marker)
        while text[start] in " \t":
            start += 1
        end = value_span(text, start)
        return text[:start] + rendered + text[end:]
    close = text.rstrip().rfind("}")
    head = text[:close].rstrip()
    comma = "" if head.endswith((",", "{")) else ","
    return f'{head}{comma}\n  "{key}": {rendered},\n' + text[close:]


def ayu_scope(ayu, scope):
    for rule in ayu["tokenColors"]:
        scopes = rule.get("scope", [])
        if isinstance(scopes, str):
            scopes = scopes.split(",")
        if scope in (s.strip() for s in scopes) and "foreground" in rule.get("settings", {}):
            return rule["settings"]["foreground"]
    raise KeyError(scope)


def rgb_triplet(hex_color):
    return ",".join(map(str, parse(hex_color)[0]))


def obsidian_css(ayu):
    """Obsidian's and the Minimal theme's color variables, set after Minimal loads."""
    h, l, s = colorsys.rgb_to_hls(*(c / 255 for c in parse(BLUE)[0]))
    code = lambda scope: code_color(ayu_scope(ayu, scope))
    status = {"red": T3["error"], "green": T3["success"], "orange": T3["warning"],
              "yellow": T3["warning_text"], "blue": T3["info"]}
    variables = {
        "--accent-h": f"{round(h * 360)}", "--accent-s": f"{round(s * 100)}%", "--accent-l": f"{round(l * 100)}%",
        # Minimal derives most of its colors from these.
        "--bg1": BACKGROUND, "--bg2": CARD, "--bg3": BORDER,
        "--ui1": BORDER, "--ui2": INPUT, "--ui3": "#ffffff29",
        "--tx1": T3["foreground"], "--tx2": MUTED_TEXT, "--tx3": "#737373",
        "--hl1": TERMINAL["selection"], "--hl2": T3["warning"] + "40",
        "--background-primary": BACKGROUND, "--background-primary-alt": BACKGROUND,
        "--background-secondary": CARD, "--background-secondary-alt": CARD,
        "--background-modifier-border": BORDER, "--background-modifier-hover": ACCENT,
        "--background-modifier-active-hover": BORDER,
        "--text-normal": T3["foreground"], "--text-muted": MUTED_TEXT, "--text-faint": "#737373",
        "--text-selection": TERMINAL["selection"], "--text-highlight-bg": T3["warning"] + "40",
        "--interactive-accent": BLUE, "--interactive-accent-hover": "#4a7cf3", "--text-on-accent": "#ffffff",
        "--link-color": LINK, "--link-color-hover": LINK, "--link-external-color": LINK,
        "--link-external-color-hover": LINK, "--link-unresolved-color": MUTED_TEXT,
        **{f"--color-{name}": value for name, value in status.items()},
        **{f"--color-{name}-rgb": rgb_triplet(value) for name, value in status.items()},
        "--code-background": CARD,
        "--code-normal": code_color(ayu["colors"]["editor.foreground"]),
        "--code-comment": code("comment"),
        "--code-function": code("entity.name.function"),
        "--code-important": code("string.regexp"),
        "--code-keyword": code("keyword"),
        "--code-operator": code("keyword.operator"),
        "--code-property": code("variable.member"),
        "--code-punctuation": MUTED_TEXT,
        "--code-string": code("string"),
        "--code-tag": code("entity.name.tag"),
        "--code-value": code("constant.numeric"),
    }
    body = "\n".join(f"  {k}: {v};" for k, v in variables.items())
    return ("/* Written by ~/repos/dotfiles/themes/editor-colors.py from home/.chezmoidata/t3.toml.\n"
            "   Edit that script, not this file. */\n"
            f".theme-dark,\n.theme-dark.minimal-default-dark {{\n{body}\n}}\n")


def write_obsidian(ayu):
    with open(os.path.expanduser("~/.config/chezmoi/chezmoi.toml"), "rb") as f:
        vault = tomllib.load(f).get("data", {}).get("notesVault", "")
    config = Path(vault) / ".obsidian" if vault else None
    if not config or not config.is_dir():
        return
    (config / "snippets").mkdir(exist_ok=True)
    (config / "snippets/t3.css").write_text(obsidian_css(ayu))
    appearance = config / "appearance.json"
    data = json.loads(appearance.read_text()) if appearance.exists() else {}
    snippets = data.get("enabledCssSnippets", [])
    data.update({"accentColor": BLUE, "theme": "obsidian",
                 "enabledCssSnippets": snippets + ["t3"] if "t3" not in snippets else snippets})
    appearance.write_text(json.dumps(data, indent=2))
    print("wrote", config / "snippets/t3.css")


def main():
    path = sorted(glob.glob(os.path.expanduser("~/.vscode/extensions/teabyii.ayu-*/ayu-dark.json")))[-1]
    with open(path) as f:
        ayu = json.load(f)
    keys = build(ayu)
    if "--print" in sys.argv:
        print(json.dumps(keys, indent=2))
        return
    for settings in SETTINGS:
        settings = os.path.expanduser(settings)
        with open(settings) as f:
            text = f.read()
        for key, value in keys.items():
            text = write_key(text, key, value)
        with open(settings, "w") as f:
            f.write(text)
        print("wrote", settings)
    write_obsidian(ayu)


if __name__ == "__main__":
    main()
