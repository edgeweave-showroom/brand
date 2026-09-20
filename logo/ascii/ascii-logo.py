#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Technologies Edgeweave
# SPDX-License-Identifier: MIT
"""Edgeweave ASCII logo, built by stacking coloured layers.

    ./ascii-logo.py                  symbol + wordmark + tagline, colour auto-detected
    ./ascii-logo.py -p symbol | -p wordmark | -p logo
    ./ascii-logo.py -c true|256|none
    ./ascii-logo.py --sh             emit POSIX shell code on stdout
    ./ascii-logo.py --sh -o logo.sh

How it works
------------
The logo is not plotted character by character. It is a stack of complete
ASCII pictures, painted in order, each one carrying a single colour. A cell
takes the colour of the last layer that wrote a non-blank character there, so
where two layers touch, the upper one wins.

Editing the artwork therefore means editing the pictures below, in place.
Leading blank lines are significant - they position a layer vertically.

Layout: MARGIN blank columns, the logo, GAP blank columns, the wordmark.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Literal, get_args

Cell = tuple[str, str | None]  # character, layer that painted it (None: blank)
Grid = list[list[Cell]]
Rgb = tuple[int, int, int]
Weight = Literal["bold", "dim", ""]
ColorMode = Literal["true", "256", "none"]
ColorArg = Literal["auto", "true", "256", "none"]
Part = Literal["symbol", "wordmark", "logo", "tagline"]

# --------------------------------------------------------------------------
# the layers, painted bottom to top
# --------------------------------------------------------------------------
# fmt: off
LAYERS = [

    ("outer", r"""
      _.-'0'-._
 _.-''    |    ''-._
0._       |       _.0
|  ''-._  |  _.-''  |
|                   |
|                   |
|     _-' | '-_     |
0_.-''    |    ''-._0
 ''-._    |    _.-''
      ''-.0.-''
     """),

    ("nodes", r"""
          0

0                   0




0                   0

          0
     """),

    ("inner", r"""

        _. ._
    .-''     ''-.
   '             '
   |             |
   |             |
   |             |
    ''._     _.''
        '' ''
     """),

    ("halo", r"""




        /   \
        \   /
     """),

    ("core", r"""




         / \
         \ /
     """),
]
# fmt: on

# --------------------------------------------------------------------------
# palette - single source of truth for both output paths
# --------------------------------------------------------------------------
# Weight is an SGR intensity attribute: 'bold' (1), 'dim' (2) or '' (22, normal).
# Bold thickens the glyph in terminals whose font has a bold cut; elsewhere it
# usually just brightens the colour.
#
# fmt: off
#    layer       24-bit rgb      256   weight  role
PALETTE: list[tuple[str, Rgb, int, Weight, str]] = [
    ("outer",    (23, 81, 107),    24, "",     "layer 1, outer hexagon"),
    ("nodes",    (39, 166, 199),   38, "bold", "layer 2, outer nodes"),
    ("inner",    (39, 166, 199),   38, "bold", "layer 3, inner hexagon"),
    ("halo",     (78, 44, 46),     52, "",     "layer 4, core halo"),
    ("core",     (249, 79, 48),   202, "bold", "layer 5, core"),
    ("wordmark", (255, 255, 255), 231, "bold", "EDGEWEAVE wordmark"),
    ("tagline",  (138, 138, 138), 245, "",     "INDUSTRIAL AI PLATFORM tagline"),
]
# fmt: on
ATTR: dict[Weight, int] = {"bold": 1, "dim": 2, "": 22}

RGB = {n: c for n, c, _, _, _ in PALETTE}
X256 = {n: i for n, _, i, _, _ in PALETTE}
WGT = {n: w for n, _, _, w, _ in PALETTE}
ROLE = {n: r for n, _, _, _, r in PALETTE}
VAR = {n: "C_" + n.upper() for n, _, _, _, _ in PALETTE}
RESET = "\033[0m"


def sgr(layer: str, mode: ColorMode) -> str:
    """Intensity + colour SGR parameters for a layer, without the escape framing."""
    a = ATTR[WGT[layer]]
    if mode == "true":
        r, g, b = RGB[layer]
        return f"{a};38;2;{r};{g};{b}"
    if mode == "256":
        return f"{a};38;5;{X256[layer]}"
    return ""


def seq(layer: str, mode: ColorMode) -> str:
    """Intensity + colour escape sequence for a layer, in a given colour mode."""
    params = sgr(layer, mode)
    return f"\033[{params}m" if params else ""


def hex_rgb(layer: str) -> str:
    """Colour of a layer in web notation, for the comments of the sh header."""
    r, g, b = RGB[layer]
    return f"#{r:02X}{g:02X}{b:02X}"


# --------------------------------------------------------------------------
# stacking
# --------------------------------------------------------------------------
def rows(art: str) -> list[str]:
    """Artwork lines.

    One leading newline - the one after the opening quotes - is dropped; any
    further leading blank line is part of the picture and sets where the layer
    starts. The closing quotes sit right after the last line, so no trailing
    blank creeps in; the loop below is a safety net.
    """
    lines = art.removeprefix("\n").split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def stack(layers: list[tuple[str, str]] = LAYERS) -> Grid:
    """Paint the layers in order into a grid of (character, layer) cells."""
    parsed = [(name, rows(art)) for name, art in layers]
    h = max(len(ls) for _, ls in parsed)
    w = max((len(line) for _, ls in parsed for line in ls), default=0)
    g: Grid = [[(" ", None) for _ in range(w)] for _ in range(h)]
    for name, ls in parsed:
        for r, line in enumerate(ls):
            for c, ch in enumerate(line):
                if ch != " ":
                    g[r][c] = (ch, name)
    return g


def trim_left(g: Grid) -> Grid:
    """Drop the blank columns on the left, so MARGIN is the only margin."""
    first = min(
        (c for row in g for c, (ch, _) in enumerate(row) if ch != " "), default=0
    )
    return [row[first:] for row in g] if first else g


def blit(g: Grid, top: int, left: int, cells: Grid) -> None:
    """Copy the non-blank cells into `g`, offset by `top` rows and `left` columns."""
    for r, row in enumerate(cells):
        for c, cell in enumerate(row):
            if cell[0] != " ":
                g[top + r][left + c] = cell


# --------------------------------------------------------------------------
# wordmark and composition
# --------------------------------------------------------------------------
# Small Mono 12. SHIFT nudges the art up or down relative to the centre line;
# the descender of the g counts as height, so the font otherwise sits low.
WORDMARK_SHIFT = 0
WORDMARK = """▗▄▄▄▖   ▗▖
▐▛▀▀▘   ▐▌
▐▌    ▟█▟▌ ▟█▟▌ ▟█▙ █   █ ▟█▙  ▟██▖▐▙ ▟▌ ▟█▙
▐███ ▐▛ ▜▌▐▛ ▜▌▐▙▄▟▌▜ █ ▛▐▙▄▟▌ ▘▄▟▌ █ █ ▐▙▄▟▌
▐▌   ▐▌ ▐▌▐▌ ▐▌▐▛▀▀▘▐▙█▟▌▐▛▀▀▘▗█▀▜▌ ▜▄▛ ▐▛▀▀▘
▐▙▄▄▖▝█▄█▌▝█▄█▌▝█▄▄▌▝█ █▘▝█▄▄▌▐▙▄█▌ ▐█▌ ▝█▄▄▌
▝▀▀▀▘ ▝▀▝▘ ▝▀▐▌ ▝▀▀  ▀ ▀  ▝▀▀  ▀▀▝▘  ▀   ▝▀▀
           ██▛▘"""

# Right-aligned on the wordmark, one row below its last line.
TAGLINE = "INDUSTRIAL AI PLATFORM"

WIDTH = 80  # target line width, only used for the warning
MARGIN = 4  # blank columns to the left of the logo
GAP = 6  # blank columns between the logo and the wordmark


def compose(logo: Grid, part: Part, margin: int = MARGIN, gap: int = GAP) -> Grid:
    """Assemble the requested parts.

        symbol     the hexagon alone
        wordmark   EDGEWEAVE alone
        logo       hexagon + wordmark
        tagline    hexagon + wordmark + INDUSTRIAL AI PLATFORM

    The symbol is indented by `margin`, the wordmark sits `gap` columns to its
    right and is centred against it, and the tagline is right-aligned on the
    wordmark, one row below its last line.
    """
    sym = part in ("symbol", "logo", "tagline")
    word = part in ("wordmark", "logo", "tagline")
    tag = part == "tagline"

    lines = [line.rstrip() for line in WORDMARK.split("\n")]
    nw, nh = max(len(line) for line in lines), len(lines)
    # visible width, not grid width: trailing blanks are stripped on output
    lw = max((len("".join(ch for ch, _ in row).rstrip()) for row in logo), default=0)
    lh = len(logo)

    start = margin + lw + gap if sym else margin
    top = max(0, (lh - nh) // 2 + WORDMARK_SHIFT) if sym else 0
    tag_row, tag_col = top + nh, max(0, start + nw - len(TAGLINE))

    w = max(
        (margin + len(logo[0])) if sym else 0,
        (start + nw) if word else 0,
        (tag_col + len(TAGLINE)) if tag else 0,
    )
    h = max(lh if sym else 0, (top + nh) if word else 0, (tag_row + 1) if tag else 0)
    g: Grid = [[(" ", None) for _ in range(w)] for _ in range(h)]

    if sym:
        blit(g, 0, margin, logo)
    if word:
        blit(g, top, start, [[(ch, "wordmark") for ch in line] for line in lines])
    if tag:
        blit(g, tag_row, tag_col, [[(ch, "tagline") for ch in TAGLINE]])
    return g


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
def render(g: Grid, mode: ColorMode) -> str:
    """Render the grid for a terminal.

    Emits a colour code only when the layer changes, so runs of one layer stay
    in a single escape sequence.
    """
    lines = []
    for row in g:
        text = "".join(ch for ch, _ in row).rstrip()
        buf, used = "", False
        cur: str | None = None
        for ch, ly in row[: len(text)]:
            if ly is not None and ly != cur and mode != "none":
                buf += seq(ly, mode)
                cur = ly
                used = True
            buf += ch
        lines.append(buf + (RESET if used else ""))
    return "\n".join(lines)


def autodetect() -> ColorMode:
    """Colour mode for stdout, from NO_COLOR, TERM, a tty check and COLORTERM."""
    if os.environ.get("NO_COLOR") or os.environ.get("TERM") == "dumb":
        return "none"
    if not sys.stdout.isatty():
        return "none"
    if os.environ.get("COLORTERM") in ("truecolor", "24bit"):
        return "true"
    return "256"


# --------------------------------------------------------------------------
# sh emitter
# --------------------------------------------------------------------------
# How each line is printed, {} standing for the line. The colour variables
# already hold a real escape byte, so %s is enough - and must stay %s: dash's
# echo would re-interpret the backslashes of the drawing.
SH_LINE = """printf '%s\\n' "{}\""""

# Escaping for a double-quoted shell string. Only one pass this time, since
# nothing re-reads the line afterwards: a literal backslash needs two, not four.
SH_ESCAPE = {"\\": "\\\\", "`": "\\`", "$": "\\$", '"': '\\"'}


def sh_lines(g: Grid, *, coloured: bool = True) -> list[str]:
    """One printf per row.

    With `coloured`, every run of a layer is prefixed by its ${C_...} variable;
    without, the drawing goes out bare.
    """
    out = []
    for row in g:
        text = "".join(ch for ch, _ in row).rstrip()
        buf, used = "", False
        cur: str | None = None
        for ch, ly in row[: len(text)]:
            if coloured and ly is not None and ly != cur:
                buf += "${" + VAR[ly] + "}"
                cur = ly
                used = True
            buf += SH_ESCAPE.get(ch, ch)
        out.append(SH_LINE.replace("{}", buf + ("${R}" if used else "")))
    return out


SH_MODE_LABEL = {"true": "24-bit colour", "256": "256 colours"}


def emit_sh(g: Grid, mode: ColorArg = "auto") -> str:
    """Shell code that prints the logo.

    One variable per layer the drawing uses, set once by the header, then one
    printf per line - the drawing is written once and carries no colour of its
    own. The code is meant to be linted and run as any other file: shellcheck
    clean (a `shell=sh` directive, braces around every `${ESC}`, no unused
    variable) and safe to source under `set -u` (the environment is read with
    `${VAR:-}`).

    mode 'auto' emits the three-way detection header, so the terminal that runs
    the code decides. Any other mode hard-codes that palette: shorter, but
    NO_COLOR and COLORTERM no longer have any say. 'none' drops the variables
    and the subshell altogether, since there is nothing left to set or hide.
    """
    gen = "# Edgeweave ASCII logo - generated by ascii-logo.py --sh"
    lint = "# shellcheck shell=sh"
    if mode == "none":
        plain = sh_lines(g, coloured=False)
        return "\n".join(
            [gen, lint, "# Plain text, no escape sequences.", "", *plain, ""]
        )
    used = {ly for row in g for _, ly in row}
    names = [n for n, _, _, _, _ in PALETTE if n in used]
    decl = {n: f'{VAR[n]}="${{ESC}}[{sgr(n, "true")}m"' for n in names}
    pad = max(len(d) for d in decl.values())
    true_block = [f"  {decl[n]:<{pad}} # {hex_rgb(n)}  {ROLE[n]}" for n in names]
    x256_block = [f'  {VAR[n]}="${{ESC}}[{sgr(n, "256")}m"' for n in names]
    head = [gen, lint]
    if mode == "auto":
        head += [
            "# POSIX sh. The subshell keeps the C_* variables out of the caller,",
            "# and takes a single redirection for the whole block if you need one.",
            "(",
            "ESC=$(printf '\\033')",
            'R="${ESC}[0m"',
            "",
            'if [ -n "${NO_COLOR:-}" ] || [ "${TERM:-}" = "dumb" ]; then',
            "  " + " ; ".join(f"{VAR[n]}=" for n in names) + " ; R=",
            (
                'elif [ "${COLORTERM:-}" = "truecolor" ]'
                ' || [ "${COLORTERM:-}" = "24bit" ]; then'
            ),
            "  # --- 24-bit colour: exact brand values",
            "\n".join(true_block),
            "else",
            "  # --- 256-colour fallback, and anything below that maps to the nearest",
            "\n".join(x256_block),
            "fi",
            "",
        ]
    else:
        label = SH_MODE_LABEL[mode]
        head += [
            f"# POSIX sh, {label} only. No detection: NO_COLOR and COLORTERM are",
            "# ignored. The subshell keeps the C_* variables out of the caller.",
            "(",
            "ESC=$(printf '\\033')",
            'R="${ESC}[0m"',
            "",
            # no if/elif to sit inside, so drop the two-space indent
            "\n".join(
                line[2:] for line in (true_block if mode == "true" else x256_block)
            ),
            "",
        ]
    return "\n".join([*head, *sh_lines(g), ")", ""])


# --------------------------------------------------------------------------
def main() -> None:
    """Parse the command line, render or emit, warn when the result is too wide."""
    p = argparse.ArgumentParser(description="Edgeweave ASCII logo, layered")
    p.add_argument(
        "-p",
        "--part",
        default="tagline",
        choices=get_args(Part),
        help="symbol, wordmark, logo (both) or tagline (all three); "
        "default: %(default)s",
    )
    p.add_argument(
        "-c",
        "--color",
        default="auto",
        choices=get_args(ColorArg),
        help="colour mode; with --sh, auto emits the detection header",
    )
    p.add_argument(
        "-m",
        "--margin",
        type=int,
        default=MARGIN,
        help="blank columns left of the drawing, 0 for none (default: %(default)s)",
    )
    p.add_argument(
        "-g",
        "--gap",
        type=int,
        default=GAP,
        help="blank columns between symbol and wordmark (default: %(default)s)",
    )
    p.add_argument(
        "-w",
        "--width",
        type=int,
        default=WIDTH,
        help="warn above this many columns (default: 80)",
    )
    p.add_argument(
        "--sh", action="store_true", help="emit POSIX shell code instead of rendering"
    )
    p.add_argument("-o", "--output", help="write to a file instead of stdout")
    a = p.parse_args()

    g = compose(trim_left(stack()), a.part, margin=a.margin, gap=a.gap)
    got = max((len("".join(ch for ch, _ in r).rstrip()) for r in g), default=0)
    if got > a.width:
        over = got - a.width
        sys.stderr.write(
            f"warning: {got} columns, {over} over the {a.width}-column target\n"
        )
    if a.sh:
        out = emit_sh(g, a.color)
    else:
        out = render(g, autodetect() if a.color == "auto" else a.color) + "\n"
    if a.output:
        Path(a.output).write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
