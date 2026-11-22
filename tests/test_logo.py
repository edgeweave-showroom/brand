# SPDX-FileCopyrightText: 2026 Technologies Edgeweave
# SPDX-License-Identifier: MIT
"""logo/source/generate.py: recipes, variants, PDF drawing, and every export."""

import os
import re
import shutil
import xml.etree.ElementTree as ET
from functools import partial
from typing import TYPE_CHECKING

import pytest

from tests.conftest import ROOT

if TYPE_CHECKING:
    from pathlib import Path
    from types import ModuleType

SVG = "http://www.w3.org/2000/svg"

# A master in miniature: a style block, a frame, a glow and two shapes.
MASTER = f"""<svg xmlns="{SVG}" viewBox="0 0 100 50">
  <style>
  </style>
  <path id="frame" class="primary-25" d="M0 0H100V50H0Z"/>
  <path id="glow" class="accent-25-over-primary-25" d="M0 0H1V1Z"/>
  <circle id="core" class="accent" cx="50" cy="25" r="10"/>
  <rect id="bar" class="primary-35-over-primary-25" x="1" y="2" width="3" height="4"/>
</svg>"""

# A stand-in for rsvg-convert: writes a PNG signature where -o says, as the
# real one writes the image.
FAKE_RSVG = """#!/bin/sh
while [ $# -gt 0 ]; do
  if [ "$1" = -o ]; then out=$2; fi
  shift
done
printf '\\211PNG\\r\\n\\032\\n' > "$out"
"""


def master() -> ET.Element:
    return ET.fromstring(MASTER)  # noqa: S314  # a literal of this file


def classes(root: ET.Element) -> list[str]:
    return [e.attrib["class"] for e in root.iter() if "class" in e.attrib]


def test_a_recipe_lists_its_layers_top_first(logo: ModuleType) -> None:
    assert logo.recipe("primary-35-over-primary-25") == [
        ("primary", 0.35),
        ("primary", 0.25),
    ]
    assert logo.recipe("accent") == [("accent", 1.0)]


def test_a_recipe_is_composited_on_the_theme_background(logo: ModuleType) -> None:
    # The value the symbol's master carries for its light primary-25.
    assert logo.composite("light", "primary-25") == "#bfecec"
    assert logo.composite("black", "primary-50") == "#808080"
    assert logo.composite("black", "primary-50-over-primary-50") == "#404040"
    assert logo.composite("dark", "text") == "#ffffff"


def test_black_and_white_recipes_go_on_the_k_plate(logo: ModuleType) -> None:
    assert logo.cmyk("black", "primary-50") == (0, 0, 0, 50)
    assert logo.cmyk("white", "primary-25") == (0, 0, 0, 75)


def test_a_full_ink_keeps_its_own_cmyk(logo: ModuleType) -> None:
    assert logo.cmyk("light", "accent") == (0, 72, 82, 0)


def test_a_coloured_tint_takes_the_print_table(logo: ModuleType) -> None:
    assert logo.cmyk("dark", "primary-35") == (93, 49, 34, 11)


def test_every_variant_of_each_mark_is_named(logo: ModuleType) -> None:
    symbol, full, wordmark = logo.MARKS
    assert len(logo.variants(symbol)) == 16
    assert ["dark", "on_navy", "framed"] in logo.variants(symbol)
    assert ["white", "transparent", "solid", "framed"] in logo.variants(symbol)
    assert len(logo.variants(full)) == 8
    assert logo.variants(wordmark) == [
        ["black", "transparent"],
        ["white", "transparent"],
    ]


def test_a_variant_file_goes_under_its_format_and_theme(logo: ModuleType) -> None:
    symbol = logo.MARKS[0]
    assert logo.outdir(symbol, ["dark", "transparent"], "pdf") == (
        logo.LOGO / "symbol" / "cmyk" / "dark_bg"
    )
    assert logo.outdir(symbol, ["light", "on_white"], "png") == (
        logo.LOGO / "symbol" / "rgb" / "light_bg"
    )
    assert logo.outdir(symbol, ["black", "transparent"], "svg") == (
        logo.LOGO / "symbol" / "monochrome" / "black"
    )


def test_a_variant_on_a_background_gets_a_tile_and_drops_the_frame(
    logo: ModuleType,
) -> None:
    variant = logo.derive(master(), ["dark", "on_navy"])
    ids = [e.get("id") for e in variant]
    assert ids == [None, "background", "glow", "core", "bar"]
    tile = variant[1]
    assert (tile.get("width"), tile.get("height")) == ("100", "50")
    style = variant.find(f"{{{SVG}}}style")
    assert style is not None
    assert ".background { fill: #0d1829; }" in (style.text or "")


def test_a_framed_variant_keeps_the_frame(logo: ModuleType) -> None:
    variant = logo.derive(master(), ["light", "transparent", "framed"])
    assert [e.get("id") for e in variant][1] == "frame"


def test_a_solid_variant_loses_the_glow_and_keeps_one_ink(logo: ModuleType) -> None:
    variant = logo.derive(master(), ["black", "transparent", "solid"])
    assert "glow" not in [e.get("id") for e in variant]
    assert classes(variant) == ["accent", "primary"]


def test_the_style_block_holds_only_the_classes_in_use(logo: ModuleType) -> None:
    variant = logo.derive(master(), ["light", "transparent"])
    style = variant.find(f"{{{SVG}}}style")
    assert style is not None
    rules = re.findall(r"\.([\w-]+) \{", style.text or "")
    assert rules == [
        "accent-25-over-primary-25",
        "accent",
        "primary-35-over-primary-25",
    ]


def test_a_master_without_a_style_block_is_refused(logo: ModuleType) -> None:
    root = ET.fromstring(f'<svg xmlns="{SVG}" viewBox="0 0 1 1"/>')  # noqa: S314  # a literal
    with pytest.raises(ValueError, match="no <style> block"):
        logo.derive(root, ["light", "transparent"])


def test_shapes_lists_a_group_or_a_single_shape(logo: ModuleType) -> None:
    root = ET.fromstring(  # noqa: S314  # a literal
        f'<svg xmlns="{SVG}"><g id="pair"><rect id="a"/><rect id="b"/></g>'
        '<circle id="one" r="1"/></svg>'
    )
    assert [attrs["id"] for _, attrs in logo.shapes(root, "pair")] == ["a", "b"]
    assert logo.shapes(root, "one") == [(f"{{{SVG}}}circle", {"id": "one", "r": "1"})]
    with pytest.raises(ValueError, match="no missing in the master"):
        logo.shapes(root, "missing")


def test_numbers_are_written_short(logo: ModuleType) -> None:
    assert [logo.num(v) for v in (1.0, 0.12345, 0.0, 12.5)] == [
        "1",
        "0.123",
        "0",
        "12.5",
    ]


def test_a_point_is_framed_then_flipped_onto_the_page(logo: ModuleType) -> None:
    assert logo.to_page(10, 20, (2.0, 5.0, 3.0), 100) == "25 57"


def test_a_group_transform_is_a_translation_then_an_optional_scale(
    logo: ModuleType,
) -> None:
    def group(transform: str | None) -> ET.Element:
        return ET.Element("g", {} if transform is None else {"transform": transform})

    assert logo.transform(group(None)) == (1.0, 0.0, 0.0)
    assert logo.transform(group("translate(10 20)")) == (1.0, 10.0, 20.0)
    assert logo.transform(group("translate(1.5 -2) scale(0.5)")) == (0.5, 1.5, -2.0)
    with pytest.raises(ValueError, match="unsupported transform"):
        logo.transform(group("rotate(45)"))


def test_path_data_becomes_pdf_operators(logo: ModuleType) -> None:
    pt = partial(logo.to_page, frame=(1.0, 0.0, 0.0), height=10)
    assert logo.path_ops("M0 0H10V5C1 2 3 4 5 6Z", pt) == [
        "0 10 m",
        "10 10 l",
        "10 5 l",
        "1 8 3 6 5 4 c",
        "h",
    ]


def test_a_circle_is_four_bezier_arcs(logo: ModuleType) -> None:
    pt = partial(logo.to_page, frame=(1.0, 0.0, 0.0), height=0)
    ops = logo.circle_ops(0, 0, 1, pt)
    assert ops[0] == "1 0 m"
    assert [op[-1] for op in ops[1:5]] == ["c"] * 4
    assert ops[4].endswith(" 1 0 c")
    assert ops[-1] == "h"


def test_a_shape_is_filled_with_its_ink_and_its_fill_rule(logo: ModuleType) -> None:
    inks = {"x": (100, 50, 0, 0)}
    frame = (1.0, 0.0, 0.0)
    rect = ET.Element(f"{{{SVG}}}rect", {"class": "x", "width": "2", "height": "1"})
    assert logo.paint(rect, frame, 1, inks) == [
        "1 0.5 0 0 k",
        "0 1 m",
        "2 1 l",
        "2 0 l",
        "0 0 l",
        "h",
        "f",
    ]
    path = ET.Element(
        f"{{{SVG}}}path", {"class": "x", "d": "M0 0Z", "fill-rule": "evenodd"}
    )
    assert logo.paint(path, frame, 1, inks)[-1] == "f*"
    assert logo.paint(ET.Element(f"{{{SVG}}}style"), frame, 1, inks) == []


def test_a_pdf_points_at_each_of_its_objects(logo: ModuleType) -> None:
    variant = logo.derive(master(), ["light", "transparent"])
    inks = {cls: logo.cmyk("light", cls) for cls in classes(variant)}
    out = logo.pdf(variant, (200, 100), inks)
    assert out.startswith(b"%PDF-1.4\n")
    assert out.endswith(b"%%EOF\n")
    xref = int(out.rsplit(b"startxref\n", 1)[1].split(b"\n")[0])
    assert out[xref:].startswith(b"xref\n0 5\n")
    offsets = re.findall(rb"(\d{10}) 00000 n ", out)
    for number, offset in enumerate(offsets, 1):
        assert out[int(offset) :].startswith(f"{number} 0 obj\n".encode())
    assert b"/MediaBox [0 0 200 100]" in out


@pytest.fixture
def rsvg(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Put a fake rsvg-convert first on PATH."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake = bin_dir / "rsvg-convert"
    fake.write_text(FAKE_RSVG)
    fake.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    return fake


def test_main_writes_the_committed_svg_and_pdf_exports(
    logo: ModuleType,
    rsvg: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert rsvg.exists()
    out = tmp_path / "logo"
    monkeypatch.setattr(logo, "LOGO", out)

    logo.main()

    files = [p.relative_to(out) for p in out.rglob("*") if p.is_file()]
    assert len(files) == 78
    for path in files:
        written = (out / path).read_bytes()
        if path.suffix == ".png":
            assert written.startswith(b"\x89PNG")
        else:
            assert written == (ROOT / "logo" / path).read_bytes(), path
    assert capsys.readouterr().out == f"78 files written under {out}\n"


def test_main_stops_without_rsvg_convert(
    logo: ModuleType, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("PATH", str(tmp_path))
    with pytest.raises(SystemExit, match="rsvg-convert not found"):
        logo.main()


def copy_masters(logo: ModuleType, tmp_path: Path) -> Path:
    masters = tmp_path / "source"
    masters.mkdir()
    for mark in logo.MARKS:
        shutil.copy(mark.master, masters)
    return masters


def test_main_stops_on_a_master_that_is_not_its_own_variant(
    logo: ModuleType, rsvg: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert rsvg.exists()
    masters = copy_masters(logo, tmp_path)
    symbol = masters / "edgeweave-symbol.svg"
    symbol.write_text(symbol.read_text().replace("#bfecec", "#000000"))
    monkeypatch.setattr(logo, "HERE", masters)
    with pytest.raises(SystemExit, match="is not its own light-transparent-framed"):
        logo.main()


def test_main_stops_when_the_full_logo_and_the_symbol_differ(
    logo: ModuleType, rsvg: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert rsvg.exists()
    masters = copy_masters(logo, tmp_path)
    full = masters / "edgeweave-logo.svg"
    full.write_text(full.read_text().replace('id="node-top"', 'id="node-up"', 1))
    monkeypatch.setattr(logo, "HERE", masters)
    with pytest.raises(SystemExit, match=r"its symbol is not edgeweave-symbol\.svg's"):
        logo.main()
