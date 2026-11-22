# SPDX-FileCopyrightText: 2026 Technologies Edgeweave
# SPDX-License-Identifier: MIT
"""logo/source/package.py: the release zip."""

import sys
import zipfile
from typing import TYPE_CHECKING

import pytest

from tests.conftest import ROOT

if TYPE_CHECKING:
    from pathlib import Path
    from types import ModuleType


def test_the_guide_is_the_picking_a_file_section_alone(package: ModuleType) -> None:
    guide = package.guide()
    assert guide.startswith("## Picking a file\n")
    assert "\n## " not in guide


def test_a_readme_without_the_section_stops_the_package(
    package: ModuleType, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    (tmp_path / "README.md").write_text("# Logo\n\n## Something else\n")
    monkeypatch.setattr(package, "LOGO", tmp_path)
    with pytest.raises(SystemExit, match="no '## Picking a file' section"):
        package.guide()


def test_the_zip_holds_the_marks_the_terms_and_a_readme_for_the_release(
    package: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(package, "ROOT", tmp_path)
    monkeypatch.setattr(sys, "argv", ["package.py", "v9.9"])

    package.main()

    out = tmp_path / "dist" / "edgeweave-logo.zip"
    marks = sorted(
        f"edgeweave-logo/{p.relative_to(ROOT / 'logo').as_posix()}"
        for d in ("symbol", "full", "wordmark")
        for p in (ROOT / "logo" / d).rglob("*")
        if p.is_file()
    )
    with zipfile.ZipFile(out) as bundle:
        names = bundle.namelist()
        readme = bundle.read("edgeweave-logo/README.md").decode()
        terms = bundle.read("edgeweave-logo/LICENSE.txt")
    assert names == ["edgeweave-logo/README.md", "edgeweave-logo/LICENSE.txt", *marks]
    assert "Release v9.9:" in readme
    assert readme.endswith(package.guide())
    assert terms == package.TERMS.read_bytes()
    assert capsys.readouterr().out == f"{len(names)} files in {out}\n"
