#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Technologies Edgeweave
# SPDX-License-Identifier: MIT
"""Generate the colour theme of every application from palette.toml.

    ./generate.py            rewrite ../terminal/, ../editor/ and ../tool/

palette.toml, next to this script, holds every colour decision: the palette,
tested in Ghostty, and how each application maps it. Starship's prompt is the
exception: starship.toml, next to it too, names the palette's colours itself,
since the palette travels with it.

- Terminals take the 16 ANSI colours and a few roles of their own, so that
  every program in them follows the palette.
- Editors colour code by role, which Vim maps onto its highlight groups and
  VS Code onto TextMate scopes, and paint their interface, vim-airline's
  status line with Vim's.
- tmux and Starship use the palette's hex values, so they look the same in
  any terminal.

This script knows the file formats only. Every file it writes opens with a
comment naming it, saying how to install it, and giving its origin and
licence, wherever the format takes comments: the attribution travels with
the file. The themes and their two sources are CC BY-ND 4.0, this script
is MIT.
"""

import json
import plistlib
import shutil
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEME = HERE.parent
DIRS = ("terminal", "editor", "tool")
REPO = "https://github.com/edgeweave-showroom/brand"
# REUSE-IgnoreStart
LICENCE = [
    "SPDX-FileCopyrightText: 2026 Technologies Edgeweave",
    "SPDX-License-Identifier: CC-BY-ND-4.0",
]
STARSHIP_LICENCE = [
    "SPDX-FileCopyrightText: 2026 Technologies Edgeweave",
    "SPDX-FileCopyrightText: 2019-2022 Starship Contributors",
    "SPDX-License-Identifier: CC-BY-ND-4.0 AND ISC",
]
# REUSE-IgnoreEnd

ANSI_NAMES = ("Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White")
STARSHIP_NAMES = ("black", "red", "green", "yellow", "blue", "purple", "cyan", "white")


@dataclass(frozen=True)
class Style:
    """How to paint text: colours, and an attribute, as palette.toml gives them."""

    fg: str = ""
    bg: str = ""
    attr: str = ""
    sp: str = ""


def styles(table: dict[str, dict[str, str]]) -> dict[str, Style]:
    """Read a table of styles; a key other than fg, bg, attr or sp is an error."""
    return {name: Style(**fields) for name, fields in table.items()}


SPEC = tomllib.loads((HERE / "palette.toml").read_text(encoding="utf-8"))
PALETTE: dict[str, str] = SPEC["palette"]
ANSI: list[str] = SPEC["ansi"]["normal"] + SPEC["ansi"]["bright"]
BRIGHT = {f"bright-{n.lower()}": c for n, c in zip(ANSI_NAMES, ANSI[8:], strict=True)}
TERMINAL: dict[str, str] = SPEC["terminal"]
SYNTAX = styles(SPEC["syntax"])
VIM_SYNTAX: dict[str, str] = SPEC["vim"]["syntax"]
VIM = styles(SPEC["vim"]["interface"])
AIRLINE_A = styles(SPEC["airline"]["a"])
AIRLINE_B = styles(SPEC["airline"]["b"])
AIRLINE = styles(SPEC["airline"]["sections"])
AIRLINE_ACCENTS: dict[str, str] = SPEC["airline"]["accents"]
SCOPES: dict[str, list[str]] = SPEC["vscode"]["syntax"]
VSCODE: dict[str, str] = SPEC["vscode"]["interface"]
TMUX = styles(SPEC["tmux"]["styles"])
TMUX_COLOURS: dict[str, str] = SPEC["tmux"]["colours"]
CATPPUCCIN: dict[str, str] = SPEC["tmux"]["catppuccin"]


def rgb(hex_colour: str) -> tuple[int, int, int]:
    """Channels of a #rrggbb colour."""
    r, g, b = (int(hex_colour[i : i + 2], 16) for i in (1, 3, 5))
    return (r, g, b)


def colour(value: str, *, blend: bool = False) -> str:
    """Resolve a palette name, bright-red or #rrggbb, at an opacity: "green 20%".

    The opacity is flattened over the background, or kept as an alpha channel,
    #rrggbbaa, for an application that blends.
    """
    name, _, percent = value.partition(" ")
    if name in BRIGHT:
        name = colour(BRIGHT[name])
    hex_colour = name if name.startswith("#") else PALETTE[name]
    if not percent:
        return hex_colour
    opacity = int(percent.removesuffix("%")) / 100
    if blend:
        return f"{hex_colour}{round(opacity * 255):02x}"
    background = rgb(colour(TERMINAL["background"]))
    channels = (
        opacity * c + (1 - opacity) * b
        for c, b in zip(rgb(hex_colour), background, strict=True)
    )
    return "#" + "".join(f"{round(c):02x}" for c in channels)


def header(
    title: str,
    usage: list[str],
    source: str = "palette.toml",
    licence: list[str] = LICENCE,
) -> list[str]:
    """Lines opening a file: its name, how to install it, its origin and licence."""
    return [
        title,
        *usage,
        "",
        f"Generated from theme/source/{source}, {REPO}",
        *licence,
    ]


def commented(lines: list[str], mark: str) -> str:
    """Lines as comments, each opened by mark."""
    return "".join(f"{mark} {line}".rstrip() + "\n" for line in lines)


def ghostty() -> str:
    """Ghostty theme: the terminal roles, then the ANSI palette."""
    keys = {
        "background": "background",
        "foreground": "foreground",
        "cursor-color": "cursor",
        "cursor-text": "cursor_text",
        "selection-background": "selection",
        "selection-foreground": "selection_text",
    }
    usage = [
        "Copy to ~/.config/ghostty/themes/, then in the Ghostty config:",
        "  theme = edgeweave-dark",
    ]
    lines = [f"{key} = {colour(TERMINAL[role])}" for key, role in keys.items()]
    lines += [f"palette = {i}={colour(c)}" for i, c in enumerate(ANSI)]
    heading = commented(header("Edgeweave Dark for Ghostty", usage), "#")
    return heading + "\n" + "\n".join(lines) + "\n"


def iterm2() -> str:
    """iTerm2 colour preset: a property list, the header as an XML comment."""
    keys = {f"Ansi {i} Color": c for i, c in enumerate(ANSI)}
    keys |= {
        "Background Color": TERMINAL["background"],
        "Foreground Color": TERMINAL["foreground"],
        "Bold Color": TERMINAL["bold"],
        "Cursor Color": TERMINAL["cursor"],
        "Cursor Text Color": TERMINAL["cursor_text"],
        "Selection Color": TERMINAL["selection"],
        "Selected Text Color": TERMINAL["selection_text"],
        "Link Color": TERMINAL["link"],
    }
    preset = {}
    for key, value in keys.items():
        r, g, b = rgb(colour(value))
        preset[key] = {
            "Color Space": "sRGB",
            "Red Component": r / 255,
            "Green Component": g / 255,
            "Blue Component": b / 255,
            "Alpha Component": 1.0,
        }
    usage = ["In iTerm2: Settings > Profiles > Colors > Color Presets > Import."]
    note = "<!--\n" + "\n".join(header("Edgeweave Dark for iTerm2", usage)) + "\n-->\n"
    prolog, plist = plistlib.dumps(preset).decode().split("<plist", 1)
    return f"{prolog}{note}<plist{plist}"


def vim_highlight(group: str, style: Style) -> str:
    """Write a :highlight command giving every field, so no default shows through."""
    fg, bg, sp = (colour(v) if v else "NONE" for v in (style.fg, style.bg, style.sp))
    attr = style.attr or "NONE"
    return f"hi {group} guifg={fg} guibg={bg} guisp={sp} gui={attr} cterm={attr}"


def vim() -> str:
    """Vim and Neovim colour scheme; Vim reads attributes from cterm in a terminal."""
    groups = VIM | {group: SYNTAX[role] for group, role in VIM_SYNTAX.items()}
    ansi = ", ".join(f"'{colour(c)}'" for c in ANSI)
    lines = [
        "set background=dark",
        "hi clear",
        "let g:colors_name = 'edgeweave'",
        "",
        *(vim_highlight(group, style) for group, style in groups.items()),
        "",
        "if has('nvim')",
        "  hi! link @variable Identifier",
        "endif",
        "",
        f"let g:terminal_ansi_colors = [{ansi}]",
        *(f"let g:terminal_color_{i} = '{colour(c)}'" for i, c in enumerate(ANSI)),
    ]
    usage = [
        "Copy to ~/.vim/colors/ (Neovim: ~/.config/nvim/colors/), then:",
        "  set termguicolors",
        "  colorscheme edgeweave",
    ]
    heading = commented(header("Edgeweave Dark for Vim and Neovim", usage), '"')
    return heading + "\n" + "\n".join(lines) + "\n"


def airline_colours(style: Style) -> str:
    """Write a style the vim-airline way; no terminal colours, as in the scheme."""
    fg, bg = (colour(v) if v else "" for v in (style.fg, style.bg))
    return f"['{fg}', '{bg}', '', '', '{style.attr}']"


def airline_dict(variable: str, entries: dict[str, Style]) -> list[str]:
    """Write a :let of an airline dictionary, one entry a line."""
    return [
        f"let {variable} = {{",
        *(f"      \\ '{key}': {airline_colours(s)}," for key, s in entries.items()),
        "      \\ }",
    ]


def airline() -> str:
    """vim-airline theme: every mode, and its modified override, then the accents."""
    inactive, modified = AIRLINE["inactive"], AIRLINE["modified"]
    modes = {
        mode: (a, AIRLINE_B[mode], AIRLINE["c"], AIRLINE["warning"], AIRLINE["error"])
        for mode, a in AIRLINE_A.items()
    } | {"inactive": (inactive,) * 5}
    palette = "g:airline#themes#edgeweave#palette"
    lines = [f"let {palette} = {{}}"]
    for mode, (a, b, c, warning, error) in modes.items():
        # airline gives its own colours to these in any dictionary without them,
        # overrides included.
        checks = {"airline_warning": warning, "airline_error": error, "airline_term": c}
        sections = {
            "airline_a": a,
            "airline_b": b,
            "airline_c": c,
            "airline_x": c,
            "airline_y": b,
            "airline_z": a,
        }
        lines += ["", *airline_dict(f"{palette}.{mode}", sections | checks)]
        overrides = {"airline_c": modified} | checks
        lines += airline_dict(f"{palette}.{mode}_modified", overrides)
    accents = {name: Style(fg=value) for name, value in AIRLINE_ACCENTS.items()}
    lines += ["", *airline_dict(f"{palette}.accents", accents)]
    usage = [
        "Copy to ~/.vim/autoload/airline/themes/",
        "(Neovim: ~/.config/nvim/autoload/airline/themes/). vim-airline takes it",
        "with colorscheme edgeweave, unless the vimrc names another theme:",
        "  let g:airline_theme = 'edgeweave'",
    ]
    heading = commented(header("Edgeweave Dark for vim-airline", usage), '"')
    return heading + "\n" + "\n".join(lines) + "\n"


def vscode_manifest() -> str:
    """package.json of the VS Code extension, which contributes the theme."""
    manifest = {
        "name": "edgeweave-theme",
        "displayName": "Edgeweave Theme",
        "description": "The Edgeweave colour theme",
        "version": "1.0.0",
        "publisher": "edgeweave",
        "license": "CC-BY-ND-4.0",
        "repository": {"type": "git", "url": REPO},
        "engines": {"vscode": "^1.70.0"},
        "categories": ["Themes"],
        "contributes": {
            "themes": [
                {
                    "label": "Edgeweave Dark",
                    "uiTheme": "vs-dark",
                    "path": "./themes/edgeweave-dark-color-theme.json",
                }
            ]
        },
    }
    return json.dumps(manifest, indent=2) + "\n"


def vscode_theme() -> str:
    """VS Code colour theme: the interface, the integrated terminal, then code."""
    colours = {key: colour(value, blend=True) for key, value in VSCODE.items()}
    colours |= {
        "terminal.background": colour(TERMINAL["background"]),
        "terminal.foreground": colour(TERMINAL["foreground"]),
        "terminalCursor.foreground": colour(TERMINAL["cursor"]),
        "terminal.selectionBackground": colour(TERMINAL["selection"]),
    }
    for prefix, half in (("ansi", ANSI[:8]), ("ansiBright", ANSI[8:])):
        for name, value in zip(ANSI_NAMES, half, strict=True):
            colours[f"terminal.{prefix}{name}"] = colour(value)
    tokens = []
    for role, scopes in SCOPES.items():
        style = SYNTAX[role]
        settings = {"foreground": colour(style.fg)} if style.fg else {}
        if style.attr:
            settings["fontStyle"] = style.attr
        tokens.append({"name": role, "scope": scopes, "settings": settings})
    theme = {
        "$schema": "vscode://schemas/color-theme",
        "name": "Edgeweave Dark",
        "type": "dark",
        "semanticHighlighting": True,
        "colors": colours,
        "tokenColors": tokens,
    }
    usage = ["Part of the Edgeweave Theme extension for VS Code."]
    heading = commented(header("Edgeweave Dark for VS Code", usage), "//")
    return heading + json.dumps(theme, indent=2) + "\n"


def tmux_style(style: Style) -> str:
    """Write a style the tmux way: fg, bg and attribute, comma-separated."""
    parts = [f"fg={colour(style.fg)}"] if style.fg else []
    parts += [f"bg={colour(style.bg)}"] if style.bg else []
    parts += [style.attr] if style.attr else []
    return ",".join(parts)


def tmux() -> str:
    """Write tmux settings to source: styles, then plain colours."""
    lines = [f'set -g {key} "{tmux_style(style)}"' for key, style in TMUX.items()]
    lines += [f'set -g {key} "{colour(c)}"' for key, c in TMUX_COLOURS.items()]
    usage = [
        "Source it from tmux.conf:",
        "  source-file ~/.config/tmux/edgeweave-dark.conf",
    ]
    heading = commented(header("Edgeweave Dark for tmux", usage), "#")
    return heading + "\n" + "\n".join(lines) + "\n"


def tmux_catppuccin() -> str:
    """Write Catppuccin's colours for its tmux plugin, to source before it loads."""
    lines = [f'set -g @thm_{name} "{colour(c)}"' for name, c in CATPPUCCIN.items()]
    usage = [
        "Catppuccin's status line in the Edgeweave colours, in place of",
        "edgeweave-dark.conf. Source it from tmux.conf before the plugin loads,",
        "which keeps colours set before it:",
        "  source-file ~/.config/tmux/edgeweave-dark-catppuccin.conf",
    ]
    title = "Edgeweave Dark for Catppuccin's tmux plugin"
    heading = commented(header(title, usage), "#")
    return heading + "\n" + "\n".join(lines) + "\n"


def starship_colours() -> list[str]:
    """List the palette table: its own names, then Starship's for the ANSI colours.

    Starship looks a colour name up in the palette first, so a style written
    with red or bright-blue takes the theme too. A name in both, green or
    cyan, is written once, and must be the same colour in both.
    """
    names = [*STARSHIP_NAMES, *(f"bright-{name}" for name in STARSHIP_NAMES)]
    ansi = {name: colour(c) for name, c in zip(names, ANSI, strict=True)}
    clashes = sorted(n for n in ansi.keys() & PALETTE.keys() if ansi[n] != PALETTE[n])
    if clashes:
        message = f"palette colours unlike the ANSI ones of their name: {clashes}"
        raise ValueError(message)
    return [
        "[palettes.edgeweave-dark]",
        *(f'{name} = "{value}"' for name, value in PALETTE.items()),
        "# Starship's own names for the ANSI colours, those the palette lacks:",
        "# a style written with them takes the theme too.",
        *(f'{name} = "{value}"' for name, value in ansi.items() if name not in PALETTE),
    ]


def starship_palette() -> str:
    """Write the Starship palette, to merge into a configuration of one's own."""
    lines = ['palette = "edgeweave-dark"', "", *starship_colours()]
    usage = [
        "Merge into ~/.config/starship.toml, the palette line before any table.",
        "Styles can then name its colours, bg:surface1, fg:amber, and Starship's",
        "own names, red or bright-blue, take the ANSI colours of the theme.",
    ]
    heading = commented(header("Edgeweave Dark palette for Starship", usage), "#")
    return heading + "\n" + "\n".join(lines) + "\n"


def starship() -> str:
    """Write a whole Starship configuration: starship.toml, then the palette.

    starship.toml opens with a comment, up to the first blank line, that stays
    out. The palette table comes last, so that the prompt may start with keys
    of its own: in TOML, they come before any table.
    """
    source = (HERE / "starship.toml").read_text(encoding="utf-8")
    _, prompt = source.split("\n\n", 1)
    lines = ['palette = "edgeweave-dark"', "", prompt.strip(), "", *starship_colours()]
    usage = [
        "A whole configuration, for Starship 1.25 or later: copy to",
        "~/.config/starship.toml, or point STARSHIP_CONFIG at it. Its symbols,",
        "Starship's Nerd Font Symbols preset under the ISC licence, need a Nerd",
        "Font. To keep a prompt of your own, merge edgeweave-dark-palette-only.toml",
        "into it instead.",
    ]
    title = "Edgeweave Dark for Starship"
    sources = "starship.toml and palette.toml"
    heading = commented(header(title, usage, sources, STARSHIP_LICENCE), "#")
    return heading + "\n" + "\n".join(lines) + "\n"


def main() -> None:
    """Rewrite every theme file."""
    files = {
        "terminal/ghostty/edgeweave-dark": ghostty(),
        "terminal/iterm2/edgeweave-dark.itermcolors": iterm2(),
        "editor/vim/colors/edgeweave.vim": vim(),
        "editor/vim/autoload/airline/themes/edgeweave.vim": airline(),
        "editor/vscode/package.json": vscode_manifest(),
        "editor/vscode/themes/edgeweave-dark-color-theme.json": vscode_theme(),
        "tool/tmux/edgeweave-dark.conf": tmux(),
        "tool/tmux/edgeweave-dark-catppuccin.conf": tmux_catppuccin(),
        "tool/starship/edgeweave-dark-palette-only.toml": starship_palette(),
        "tool/starship/edgeweave-dark.toml": starship(),
    }
    for name in DIRS:
        shutil.rmtree(THEME / name, ignore_errors=True)
    for path, text in files.items():
        out = THEME / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    sys.stdout.write(f"{len(files)} files written under {THEME}\n")


if __name__ == "__main__":
    main()
