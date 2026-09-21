#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Technologies Edgeweave
# SPDX-License-Identifier: MIT
"""Generate every variant of the symbol and of the full logo from their masters.

    ./generate.py            rewrite ../symbol/ and ../full/ but for their sources

A master (edgeweave-symbol.svg, edgeweave-logo.svg, next to this script)
is flattened: every shape is opaque, and where two translucent layers of the
design overlap, the overlap is a shape of its own. A shape's class is its
recipe, top layer first: "primary-35-over-primary-25" is the primary ink at
35 % over the primary ink at 25 %, composited on the theme's background. The
full logo embeds the symbol's shapes under its own placement; they must stay
the symbol master's, which is checked.

Each variant is a substitution on its master: a theme composites every recipe
with its own inks and rewrites the <style> block, a tile is inserted or the
frame dropped, and the solid variants keep one ink at 100 % and lose the
glow. Its name spells all of it out: theme, background, options.

Screen files go under rgb/: the derived SVG, and a PNG rendered from it by
rsvg-convert (librsvg). Print files go under cmyk/: a PDF written here from
the same geometry with DeviceCMYK fills. Recipes of black and white alone are
composited on the K plate; the coloured ones cannot be, a colour profile made
them, so they are the PRINT table below. Monochrome variants are a single ink
either way and get all three formats under monochrome/.
"""

import copy
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from functools import partial
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOGO = HERE.parent
PNG_SIZE = 1000
SVG_NS = "http://www.w3.org/2000/svg"
KAPPA = 0.5522847498  # Bézier control distance of a quarter circle, in radii

Rgb = tuple[float, float, float]
Cmyk = tuple[int, int, int, int]
Frame = tuple[float, float, float]  # scale, then x and y offsets


@dataclass(frozen=True)
class Mark:
    """A mark: its directory under logo/, its file prefix, its PDF page in points."""

    name: str
    prefix: str
    page: tuple[int, int]
    framed: bool  # the master carries a frame, and every variant comes with or without

    @property
    def master(self) -> Path:
        """The master SVG of the mark."""
        return HERE / f"{self.prefix}.svg"


MARKS = (
    Mark("symbol", "edgeweave-symbol", (500, 500), framed=True),
    Mark("full", "edgeweave-logo", (960, 240), framed=False),
)

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

# Ink of each role, per theme. The background is what the recipes are
# composited on; the colour themes also offer it as a tile.
THEMES: dict[str, dict[str, str]] = {
    "light": {
        "background": "white",
        "primary": "teal",
        "accent": "orange",
        "text": "black",
    },
    "dark": {
        "background": "navy",
        "primary": "cyan",
        "accent": "orange",
        "text": "white",
    },
    "black": {
        "background": "white",
        "primary": "black",
        "accent": "black",
        "text": "black",
    },
    "white": {
        "background": "black",
        "primary": "white",
        "accent": "white",
        "text": "white",
    },
}
MONOCHROME = ("black", "white")

# CMYK of the flattened coloured recipes, per colour theme: Affinity's
# flattened exports through the same profile.
PRINT: dict[str, dict[str, Cmyk]] = {
    "light": {
        "primary-25": (18, 0, 7, 0),
        "primary-35": (25, 0, 10, 0),
        "primary-52": (38, 0, 15, 0),
        "primary-70": (52, 0, 20, 0),
        "primary-50": (37, 0, 15, 0),
        "primary-43": (32, 0, 13, 0),
        "primary-61": (45, 0, 18, 0),
        "primary-35-over-primary-25": (38, 0, 15, 0),
        "primary-52-over-primary-25": (48, 0, 18, 0),
        "primary-70-over-primary-25": (57, 0, 22, 0),
        "primary-50-over-primary-25": (47, 0, 18, 0),
        "primary-43-over-primary-25": (43, 0, 17, 0),
        "primary-61-over-primary-25": (52, 0, 20, 0),
        "primary-80": (58, 0, 22, 0),
        "primary-80-over-primary-25": (61, 0, 24, 0),
        "accent-25": (0, 13, 12, 0),
        "accent-25-over-primary-25": (15, 12, 18, 0),
    },
    "dark": {
        "primary-25": (97, 60, 41, 18),
        "primary-35": (93, 49, 34, 11),
        "primary-52": (84, 30, 24, 2),
        "primary-70": (72, 10, 15, 0),
        "primary-50": (85, 32, 25, 3),
        "primary-43": (88, 39, 29, 5),
        "primary-61": (78, 20, 20, 0),
        "primary-35-over-primary-25": (84, 30, 25, 2),
        "primary-52-over-primary-25": (76, 16, 18, 0),
        "primary-70-over-primary-25": (67, 3, 11, 0),
        "primary-50-over-primary-25": (77, 18, 19, 0),
        "primary-43-over-primary-25": (80, 24, 21, 1),
        "primary-61-over-primary-25": (72, 9, 15, 0),
        "primary-80": (66, 0, 11, 0),
        "primary-80-over-primary-25": (62, 0, 9, 0),
        "accent-25": (56, 77, 71, 47),
        "accent-25-over-primary-25": (72, 55, 53, 23),
    },
}


def variants(mark: Mark) -> list[list[str]]:
    """List the name parts of every variant: theme, background, then options."""
    frames: list[list[str]] = [[], ["framed"]] if mark.framed else [[]]
    colour = [
        [theme, background, *framed]
        for theme in ("light", "dark")
        for background in ("transparent", f"on-{THEMES[theme]['background']}")
        for framed in frames
    ]
    mono = [
        [theme, "transparent", *solid, *framed]
        for theme in MONOCHROME
        for solid in ([], ["solid"])
        for framed in frames
    ]
    return colour + mono


def outdir(mark: Mark, parts: list[str], fmt: str) -> Path:
    """Directory of a variant's file in the given format."""
    theme = parts[0]
    if theme in MONOCHROME:
        return LOGO / mark.name / "monochrome" / theme
    return LOGO / mark.name / ("cmyk" if fmt == "pdf" else "rgb") / f"{theme}-bg"


def recipe(cls: str) -> list[tuple[str, float]]:
    """Layers of a recipe class, top first, as (role, opacity)."""
    layers = []
    for layer in cls.split("-over-"):
        role, _, percent = layer.partition("-")
        layers.append((role, int(percent or 100) / 100))
    return layers


def rgb(hex_colour: str) -> Rgb:
    """Channels of a #rrggbb colour."""
    r, g, b = (int(hex_colour[i : i + 2], 16) for i in (1, 3, 5))
    return (r, g, b)


def composite(theme: str, cls: str) -> str:
    """Flatten a recipe in a theme, as #rrggbb."""
    inks = {role: rgb(INKS[ink][0]) for role, ink in THEMES[theme].items()}
    colour = inks["background"]
    for role, opacity in reversed(recipe(cls)):
        r, g, b = (
            opacity * i + (1 - opacity) * c
            for i, c in zip(inks[role], colour, strict=True)
        )
        colour = (r, g, b)
    return "#" + "".join(f"{round(channel):02x}" for channel in colour)


def cmyk(theme: str, cls: str) -> Cmyk:
    """Flatten a recipe in a theme, as CMYK percentages."""
    layers = recipe(cls)
    inks = {role: INKS[ink][1] for role, ink in THEMES[theme].items()}
    if all(THEMES[theme][role] in ("black", "white") for role, _ in layers):
        colour = [float(v) for v in inks["background"]]
        for role, opacity in reversed(layers):
            colour = [
                opacity * i + (1 - opacity) * c
                for i, c in zip(inks[role], colour, strict=True)
            ]
        c, m, y, k = (round(v) for v in colour)
        return (c, m, y, k)
    (role, opacity), *below = layers
    if opacity == 1 and not below:
        return inks[role]
    return PRINT[theme][cls]


def drop(root: ET.Element, ids: set[str]) -> None:
    """Remove the layers whose id is in ids, wherever they sit in the tree."""
    for parent in root.iter():
        for child in list(parent):
            if child.get("id") in ids:
                parent.remove(child)


def box(root: ET.Element) -> tuple[float, float]:
    """Width and height of a master, from its viewBox."""
    _, _, width, height = root.attrib["viewBox"].split()
    return (float(width), float(height))


def derive(master: ET.Element, parts: list[str]) -> ET.Element:
    """Return the variant named by parts as a new tree."""
    theme, background, *options = parts
    root = copy.deepcopy(master)
    style = root.find(f"{{{SVG_NS}}}style")
    if style is None:
        msg = "no <style> block in the master"
        raise ValueError(msg)

    if background != "transparent":
        width, height = box(root)
        attributes = {
            "id": "background",
            "class": "background",
            "width": num(width),
            "height": num(height),
        }
        tile = ET.Element(f"{{{SVG_NS}}}rect", attributes)
        tile.tail = style.tail
        root.insert(1, tile)
    if "framed" not in options:
        drop(root, {"frame"})
    if "solid" in options:
        drop(root, {"glow", "glow-outer-hexagon"})
        for element in root.iter():
            if "class" in element.attrib:
                element.set("class", recipe(element.attrib["class"])[0][0])

    used = dict.fromkeys(e.attrib["class"] for e in root.iter() if "class" in e.attrib)
    rules = [f".{cls} {{ fill: {composite(theme, cls)}; }}" for cls in used]
    style.text = "".join(f"\n    {rule}" for rule in rules) + "\n  "
    return root


def svg_text(root: ET.Element) -> str:
    """Serialise an SVG tree the way the masters are written."""
    return ET.tostring(root, encoding="unicode") + "\n"


def symbol_shapes(root: ET.Element) -> list[tuple[str, dict[str, str]]]:
    """List the shapes of a master's symbol group, as tags and attributes."""
    group = root.find(f"{{{SVG_NS}}}g[@id='symbol']")
    if group is None:
        msg = "no symbol group in the master"
        raise ValueError(msg)
    return [(shape.tag, dict(shape.attrib)) for shape in group]


def render_png(svg: Path, out: Path, rsvg: str) -> None:
    """Rasterise svg into out with rsvg-convert, PNG_SIZE wide."""
    cmd = [rsvg, "-f", "png", "-w", str(PNG_SIZE), "-o", str(out), str(svg)]
    subprocess.run(cmd, check=True)  # noqa: S603  # our own command on our own files


def num(value: float) -> str:
    """Write a number the short way PDF operands are written."""
    return f"{value:.3f}".rstrip("0").rstrip(".") or "0"


def to_page(x: float, y: float, frame: Frame, height: float) -> str:
    """Map SVG coordinates through frame onto a page of that height, y going up."""
    scale, dx, dy = frame
    return f"{num(dx + scale * x)} {num(height - dy - scale * y)}"


def transform(group: ET.Element) -> Frame:
    """Read a group's transform attribute; the masters only translate then scale."""
    value = group.get("transform")
    if value is None:
        return (1.0, 0.0, 0.0)
    match = re.fullmatch(r"translate\(([-\d.]+) ([-\d.]+)\) scale\(([\d.]+)\)", value)
    if match is None:
        msg = f"unsupported transform: {value}"
        raise ValueError(msg)
    return (float(match[3]), float(match[1]), float(match[2]))


def path_ops(d: str, pt: partial[str]) -> list[str]:
    """PDF path operators for absolute M, L, H, V, C and Z path data."""
    ops: list[str] = []
    x = y = 0.0
    for command, args in re.findall(r"([MLHVCZ])([^MLHVCZ]*)", d):
        values = [float(v) for v in args.split()]
        if command == "Z":
            ops.append("h")
            continue
        controls: list[float] = []
        if command == "H":
            x = values[0]
        elif command == "V":
            y = values[0]
        else:
            *controls, x, y = values
        points = [pt(*controls[i : i + 2]) for i in range(0, len(controls), 2)]
        points.append(pt(x, y))
        ops.append(" ".join(points) + " " + {"M": "m", "C": "c"}.get(command, "l"))
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
    element: ET.Element, frame: Frame, height: float, inks: dict[str, Cmyk]
) -> list[str]:
    """PDF operators filling one shape."""
    tag = element.tag.removeprefix(f"{{{SVG_NS}}}")
    at = element.attrib
    pt = partial(to_page, frame=frame, height=height)
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
    colour = " ".join(num(v / 100) for v in inks[at["class"]]) + " k"
    return [colour, *shape, "f*" if at.get("fill-rule") == "evenodd" else "f"]


def draw(
    element: ET.Element, frame: Frame, height: float, inks: dict[str, Cmyk]
) -> list[str]:
    """PDF operators painting element's children in document order."""
    ops: list[str] = []
    for child in element:
        if child.tag == f"{{{SVG_NS}}}g":
            scale, dx, dy = frame
            s, tx, ty = transform(child)
            inner = (scale * s, dx + scale * tx, dy + scale * ty)
            ops += draw(child, inner, height, inks)
        else:
            ops += paint(child, frame, height, inks)
    return ops


def pdf(root: ET.Element, page: tuple[int, int], inks: dict[str, Cmyk]) -> bytes:
    """Write a variant as a one-page PDF."""
    width, height = page
    ops = draw(root, (width / box(root)[0], 0.0, 0.0), height, inks)
    content = "\n".join(ops)
    media = f"/MediaBox [0 0 {width} {height}] /Contents 4 0 R"
    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        f"<< /Type /Page /Parent 2 0 R {media} >>",
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


def generate(mark: Mark, master: ET.Element, rsvg: str) -> int:
    """Write every variant of a mark; return how many files that is."""
    for name in ("rgb", "cmyk", "monochrome"):
        shutil.rmtree(LOGO / mark.name / name, ignore_errors=True)
    count = 0
    for parts in variants(mark):
        stem = "-".join([mark.prefix, *parts])
        variant = derive(master, parts)
        paths = {
            fmt: outdir(mark, parts, fmt) / f"{stem}.{fmt}"
            for fmt in ("svg", "png", "pdf")
        }
        for path in paths.values():
            path.parent.mkdir(parents=True, exist_ok=True)
        paths["svg"].write_text(svg_text(variant), encoding="utf-8")
        render_png(paths["svg"], paths["png"], rsvg)
        used = {e.attrib["class"] for e in variant.iter() if "class" in e.attrib}
        inks = {cls: cmyk(parts[0], cls) for cls in used}
        paths["pdf"].write_bytes(pdf(variant, mark.page, inks))
        count += len(paths)
    return count


def main() -> None:
    """Check the masters against themselves and each other, then regenerate."""
    rsvg = shutil.which("rsvg-convert")
    if rsvg is None:
        sys.exit("rsvg-convert not found: install librsvg (librsvg2-bin on Debian)")

    ET.register_namespace("", SVG_NS)
    masters = {
        mark: ET.parse(mark.master).getroot()  # noqa: S314  # our own files
        for mark in MARKS
    }
    for mark, master in masters.items():
        parts = ["light", "transparent", *(["framed"] if mark.framed else [])]
        if svg_text(derive(master, parts)) != mark.master.read_text():
            sys.exit(f"{mark.master.name} is not its own {'-'.join(parts)} variant")
    symbol, full = MARKS
    if symbol_shapes(masters[full]) != symbol_shapes(masters[symbol]):
        sys.exit(
            f"{full.master.name}: its symbol shapes are not {symbol.master.name}'s"
        )

    count = sum(generate(mark, master, rsvg) for mark, master in masters.items())
    sys.stdout.write(f"{count} files written under {LOGO}\n")


if __name__ == "__main__":
    main()
