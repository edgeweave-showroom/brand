#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Technologies Edgeweave
# SPDX-License-Identifier: MIT
"""Generate every symbol variant from the master, edgeweave-symbol.svg.

    ./generate.py            rewrite svg/, png/ and pdf/ next to the master

Each variant is a substitution on the master: a theme overrides colours in
its <style> block, and layers are dropped by id (the background tile, the
frame, and for the flat variants the glow together with every opacity).
PNG and PDF are rendered from the derived SVG by rsvg-convert (librsvg).
"""

import copy
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "edgeweave-symbol.svg"
PREFIX = "edgeweave-symbol"
PNG_SIZE = 1000
SVG_NS = "http://www.w3.org/2000/svg"

# Colour overrides per theme, by the class names of the master's <style>
# block; "light" is the master itself.
THEMES: dict[str, dict[str, str]] = {
    "light": {},
    "dark": {"background": "#0d1829", "primary": "#00dcff"},
    "black": {"primary": "#000000", "accent": "#000000"},
    "white": {"primary": "#ffffff", "accent": "#ffffff"},
}

RULE = re.compile(r"\.(\w+) \{ fill: (#[0-9a-f]{6}); \}")


def variants() -> list[list[str]]:
    """List the name parts of every variant: theme first, then its options."""
    colour = [
        [theme, *background, *framed]
        for theme in ("light", "dark")
        for background in ([], ["background"])
        for framed in ([], ["framed"])
    ]
    mono = [
        [theme, *flat, *framed]
        for theme in ("black", "white")
        for flat in ([], ["flat"])
        for framed in ([], ["framed"])
    ]
    return colour + mono


def drop(root: ET.Element, ids: set[str]) -> None:
    """Remove the layers whose id is in ids, wherever they sit in the tree."""
    for parent in root.iter():
        for child in list(parent):
            if child.get("id") in ids:
                parent.remove(child)


def derive(master: ET.Element, parts: list[str]) -> ET.Element:
    """Return the variant named by parts as a new tree."""
    theme, options = parts[0], set(parts[1:])
    root = copy.deepcopy(master)
    style = root.find(f"{{{SVG_NS}}}style")
    if style is None:
        msg = f"{MASTER}: no <style> block"
        raise ValueError(msg)

    ids: set[str] = set()
    if "background" not in options:
        ids.add("background")
    if "framed" not in options:
        ids.add("frame")
    if "flat" in options:
        ids.add("glow")
        for element in root.iter():
            element.attrib.pop("fill-opacity", None)
    drop(root, ids)

    palette = dict(RULE.findall(style.text or "")) | THEMES[theme]
    used = {element.get("class") for element in root.iter()}
    rules = [
        f".{role} {{ fill: {fill}; }}" for role, fill in palette.items() if role in used
    ]
    style.text = "".join(f"\n    {rule}" for rule in rules) + "\n  "
    return root


def render(svg: Path, out: Path, rsvg: str) -> None:
    """Rasterise or convert svg into out, the format following out's suffix."""
    size = ["-w", str(PNG_SIZE), "-h", str(PNG_SIZE)] if out.suffix == ".png" else []
    cmd = [rsvg, "-f", out.suffix[1:], *size, "-o", str(out), str(svg)]
    subprocess.run(cmd, check=True)  # noqa: S603  # our own command on our own files


def main() -> None:
    """Regenerate the three output directories."""
    rsvg = shutil.which("rsvg-convert")
    if rsvg is None:
        sys.exit("rsvg-convert not found: install librsvg (librsvg2-bin on Debian)")

    ET.register_namespace("", SVG_NS)
    master = ET.parse(MASTER).getroot()  # noqa: S314  # our own file
    for fmt in ("svg", "png", "pdf"):
        shutil.rmtree(HERE / fmt, ignore_errors=True)
        (HERE / fmt).mkdir()

    for parts in variants():
        stem = "-".join([PREFIX, *parts])
        svg = HERE / "svg" / f"{stem}.svg"
        svg.write_text(
            ET.tostring(derive(master, parts), encoding="unicode") + "\n",
            encoding="utf-8",
        )
        render(svg, HERE / "png" / f"{stem}.png", rsvg)
        render(svg, HERE / "pdf" / f"{stem}.pdf", rsvg)
    sys.stdout.write(f"{3 * len(variants())} files written under {HERE}\n")


if __name__ == "__main__":
    main()
