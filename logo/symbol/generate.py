#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Technologies Edgeweave
# SPDX-License-Identifier: MIT
"""Generate every symbol variant from the master, edgeweave-symbol.svg.

    ./generate.py            rewrite rgb/, cmyk/ and monochrome/ next to the master

Each variant is a substitution on the master: a theme overrides colours in
its <style> block, and layers are dropped by id (the background tile, the
frame, and for the solid variants the glow together with every opacity).
Its name spells all of it out: theme, then the background (transparent, or
the tile's ink), then the options. Screen files go under rgb/: the derived
SVG, and a PNG rendered from it by rsvg-convert (librsvg). Print files go
under cmyk/: a PDF written here from the same geometry with DeviceCMYK
fills, so the ink values below reach the press untouched. Monochrome
variants are a single ink either way and get all three formats under
monochrome/.
"""

import copy
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from functools import partial
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASTER = HERE / "edgeweave-symbol.svg"
PREFIX = "edgeweave-symbol"
PNG_SIZE = 1000
PAGE = 500  # points, the master's viewBox: one SVG unit is one point
SVG_NS = "http://www.w3.org/2000/svg"
KAPPA = 0.5522847498  # Bézier control distance of a quarter circle, in radii

Cmyk = tuple[int, int, int, int]
Frame = tuple[float, float, float]  # scale, then x and y offsets

# Named inks: sRGB for screen, CMYK percentages for print. The CMYK values are
# Affinity's conversion of the sRGB ones through the U.S. Sheetfed Coated v2
# profile; black is the K plate alone and white is bare paper.
INKS: dict[str, tuple[str, Cmyk]] = {
    "white": ("#ffffff", (0, 0, 0, 0)),
    "black": ("#000000", (0, 0, 0, 100)),
    "teal": ("#00b5b5", (67, 0, 27, 0)),
    "cyan": ("#00dcff", (50, 0, 4, 0)),
    "orange": ("#ff622d", (0, 72, 82, 0)),
    "navy": ("#0d1829", (99, 85, 60, 55)),
}

# Ink of each class of the master's <style> block, per theme.
THEMES: dict[str, dict[str, str]] = {
    "light": {"background": "white", "primary": "teal", "accent": "orange"},
    "dark": {"background": "navy", "primary": "cyan", "accent": "orange"},
    "black": {"primary": "black", "accent": "black"},
    "white": {"primary": "white", "accent": "white"},
}
MONOCHROME = ("black", "white")


def variants() -> list[list[str]]:
    """List the name parts of every variant: theme, background, then options."""
    colour = [
        [theme, background, *framed]
        for theme in ("light", "dark")
        for background in ("transparent", f"on-{THEMES[theme]['background']}")
        for framed in ([], ["framed"])
    ]
    mono = [
        [theme, "transparent", *solid, *framed]
        for theme in MONOCHROME
        for solid in ([], ["solid"])
        for framed in ([], ["framed"])
    ]
    return colour + mono


def outdir(parts: list[str], fmt: str) -> Path:
    """Directory of a variant's file in the given format."""
    theme = parts[0]
    if theme in MONOCHROME:
        return HERE / "monochrome" / theme
    return HERE / ("cmyk" if fmt == "pdf" else "rgb") / f"{theme}-bg"


def drop(root: ET.Element, ids: set[str]) -> None:
    """Remove the layers whose id is in ids, wherever they sit in the tree."""
    for parent in root.iter():
        for child in list(parent):
            if child.get("id") in ids:
                parent.remove(child)


def derive(master: ET.Element, parts: list[str]) -> ET.Element:
    """Return the variant named by parts as a new tree."""
    theme, background, *options = parts
    root = copy.deepcopy(master)
    style = root.find(f"{{{SVG_NS}}}style")
    if style is None:
        msg = f"{MASTER}: no <style> block"
        raise ValueError(msg)

    ids: set[str] = set()
    if background == "transparent":
        ids.add("background")
    if "framed" not in options:
        ids.add("frame")
    if "solid" in options:
        ids.add("glow")
        for element in root.iter():
            element.attrib.pop("fill-opacity", None)
    drop(root, ids)

    used = {element.get("class") for element in root.iter()}
    rules = [
        f".{role} {{ fill: {INKS[ink][0]}; }}"
        for role, ink in THEMES[theme].items()
        if role in used
    ]
    style.text = "".join(f"\n    {rule}" for rule in rules) + "\n  "
    return root


def svg_text(root: ET.Element) -> str:
    """Serialise an SVG tree the way the master is written."""
    return ET.tostring(root, encoding="unicode") + "\n"


def render_png(svg: Path, out: Path, rsvg: str) -> None:
    """Rasterise svg into out with rsvg-convert."""
    size = ["-w", str(PNG_SIZE), "-h", str(PNG_SIZE)]
    cmd = [rsvg, "-f", "png", *size, "-o", str(out), str(svg)]
    subprocess.run(cmd, check=True)  # noqa: S603  # our own command on our own files


def num(value: float) -> str:
    """Write a number the short way PDF operands are written."""
    return f"{value:.3f}".rstrip("0").rstrip(".") or "0"


def to_page(x: float, y: float, frame: Frame) -> str:
    """Map SVG coordinates through frame onto the page, whose origin is bottom left."""
    scale, dx, dy = frame
    return f"{num(dx + scale * x)} {num(PAGE - dy - scale * y)}"


def transform(group: ET.Element) -> Frame:
    """Read a group's transform attribute; the master only translates then scales."""
    value = group.get("transform")
    if value is None:
        return (1.0, 0.0, 0.0)
    match = re.fullmatch(r"translate\(([-\d.]+) ([-\d.]+)\) scale\(([\d.]+)\)", value)
    if match is None:
        msg = f"unsupported transform: {value}"
        raise ValueError(msg)
    return (float(match[3]), float(match[1]), float(match[2]))


def path_ops(d: str, pt: partial[str]) -> list[str]:
    """PDF path operators for absolute M, L, H, V and Z path data."""
    ops: list[str] = []
    x = y = 0.0
    for command, args in re.findall(r"([MLHVZ])([^MLHVZ]*)", d):
        values = [float(v) for v in args.split()]
        if command == "Z":
            ops.append("h")
            continue
        if command == "H":
            x = values[0]
        elif command == "V":
            y = values[0]
        else:
            x, y = values
        ops.append(f"{pt(x, y)} {'m' if command == 'M' else 'l'}")
    return ops


def circle_ops(cx: float, cy: float, r: float, pt: partial[str]) -> list[str]:
    """PDF path operators for a circle, as four Bézier arcs."""
    k = KAPPA * r
    arcs = (
        ((cx + r, cy + k), (cx + k, cy + r), (cx, cy + r)),
        ((cx - k, cy + r), (cx - r, cy + k), (cx - r, cy)),
        ((cx - r, cy - k), (cx - k, cy - r), (cx, cy - r)),
        ((cx + k, cy - r), (cx + r, cy - k), (cx + r, cy)),
    )
    ops = [f"{pt(cx + r, cy)} m"]
    ops += [f"{pt(*a)} {pt(*b)} {pt(*end)} c" for a, b, end in arcs]
    ops.append("h")
    return ops


def paint(
    element: ET.Element, frame: Frame, inks: dict[str, Cmyk], alphas: dict[str, str]
) -> list[str]:
    """PDF operators filling one shape; alphas collects the opacity states it needs."""
    tag = element.tag.removeprefix(f"{{{SVG_NS}}}")
    at = element.attrib
    pt = partial(to_page, frame=frame)
    if tag == "rect":
        x, y = float(at.get("x", 0)), float(at.get("y", 0))
        w, h = float(at["width"]), float(at["height"])
        shape = path_ops(f"M{x} {y}H{x + w}V{y + h}H{x}Z", pt)
    elif tag == "circle":
        shape = circle_ops(float(at["cx"]), float(at["cy"]), float(at["r"]), pt)
    elif tag == "path":
        shape = path_ops(at["d"], pt)
    else:
        return []

    ops = ["q"]
    if "fill-opacity" in at:
        alpha = num(float(at["fill-opacity"]))
        ops.append(f"/{alphas.setdefault(alpha, f'GS{len(alphas)}')} gs")
    ops.append(" ".join(num(v / 100) for v in inks[at["class"]]) + " k")
    ops += shape
    ops.append("f*" if at.get("fill-rule") == "evenodd" else "f")
    ops.append("Q")
    return ops


def draw(
    element: ET.Element, frame: Frame, inks: dict[str, Cmyk], alphas: dict[str, str]
) -> list[str]:
    """PDF operators painting element's children in document order."""
    ops: list[str] = []
    for child in element:
        if child.tag == f"{{{SVG_NS}}}g":
            scale, dx, dy = frame
            s, tx, ty = transform(child)
            inner = (scale * s, dx + scale * tx, dy + scale * ty)
            ops += draw(child, inner, inks, alphas)
        else:
            ops += paint(child, frame, inks, alphas)
    return ops


def pdf(ops: list[str], alphas: dict[str, str]) -> bytes:
    """Wrap the content stream ops and its opacity states into a one-page PDF."""
    content = "\n".join(ops)
    states = " ".join(f"/{name} << /ca {alpha} >>" for alpha, name in alphas.items())
    page = f"/MediaBox [0 0 {PAGE} {PAGE}] /Resources << /ExtGState << {states} >> >>"
    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        f"<< /Type /Page /Parent 2 0 R {page} /Contents 4 0 R >>",
        f"<< /Length {len(content)} >>\nstream\n{content}\nendstream",
    ]
    out = "%PDF-1.4\n"
    offsets = []
    for number, body in enumerate(objects, 1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n{body}\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n"
    out += "".join(f"{offset:010} 00000 n \n" for offset in offsets)
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
    out += f"startxref\n{xref}\n%%EOF\n"
    return out.encode("ascii")


def main() -> None:
    """Regenerate the three output directories."""
    rsvg = shutil.which("rsvg-convert")
    if rsvg is None:
        sys.exit("rsvg-convert not found: install librsvg (librsvg2-bin on Debian)")

    ET.register_namespace("", SVG_NS)
    master = ET.parse(MASTER).getroot()  # noqa: S314  # our own file
    if svg_text(derive(master, ["light", "on-white", "framed"])) != MASTER.read_text():
        sys.exit(f"{MASTER.name} is not its own light-on-white-framed variant")
    for name in ("rgb", "cmyk", "monochrome"):
        shutil.rmtree(HERE / name, ignore_errors=True)

    for parts in variants():
        stem = "-".join([PREFIX, *parts])
        variant = derive(master, parts)
        paths = {
            fmt: outdir(parts, fmt) / f"{stem}.{fmt}" for fmt in ("svg", "png", "pdf")
        }
        for path in paths.values():
            path.parent.mkdir(parents=True, exist_ok=True)
        paths["svg"].write_text(svg_text(variant), encoding="utf-8")
        render_png(paths["svg"], paths["png"], rsvg)
        inks = {role: INKS[ink][1] for role, ink in THEMES[parts[0]].items()}
        alphas: dict[str, str] = {}
        ops = draw(variant, (1.0, 0.0, 0.0), inks, alphas)
        paths["pdf"].write_bytes(pdf(ops, alphas))
    sys.stdout.write(f"{3 * len(variants())} files written under {HERE}\n")


if __name__ == "__main__":
    main()
