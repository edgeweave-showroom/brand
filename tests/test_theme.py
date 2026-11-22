# SPDX-FileCopyrightText: 2026 Technologies Edgeweave
# SPDX-License-Identifier: MIT
"""theme/source/generate.py: colours resolved, and every theme file written."""

import json
import plistlib
import shutil
from typing import TYPE_CHECKING

import pytest

from tests.conftest import ROOT

if TYPE_CHECKING:
    from pathlib import Path
    from types import ModuleType


def test_a_palette_name_resolves_to_its_hex_value(theme: ModuleType) -> None:
    assert theme.colour("cerulean") == "#27a6c7"


def test_a_hex_colour_stays_as_it_is(theme: ModuleType) -> None:
    assert theme.colour("#123456") == "#123456"


def test_a_bright_ansi_name_resolves_through_the_ansi_table(theme: ModuleType) -> None:
    assert theme.colour("bright-red") == "#ff7a5e"
    # bright-black is overlay0, itself a palette name.
    assert theme.colour("bright-black") == "#4a5a75"


def test_an_opacity_is_flattened_over_the_terminal_background(
    theme: ModuleType,
) -> None:
    # green #8cbf7a at 20 % over base #0d1829.
    assert theme.colour("green 20%") == "#263939"


def test_an_opacity_becomes_an_alpha_channel_where_the_app_blends(
    theme: ModuleType,
) -> None:
    assert theme.colour("green 20%", blend=True) == "#8cbf7a33"


def test_a_style_takes_only_fg_bg_attr_and_sp(theme: ModuleType) -> None:
    assert theme.styles({"x": {"fg": "text", "attr": "bold"}}) == {
        "x": theme.Style(fg="text", attr="bold")
    }
    with pytest.raises(TypeError):
        theme.styles({"x": {"colour": "text"}})


def test_comments_carry_no_trailing_space_on_blank_lines(theme: ModuleType) -> None:
    assert theme.commented(["a", "", "b"], "#") == "# a\n#\n# b\n"


def test_a_tmux_style_lists_fg_bg_then_the_attribute(theme: ModuleType) -> None:
    style = theme.Style(fg="text", bg="petrol", attr="bold")
    assert theme.tmux_style(style) == "fg=#ebebeb,bg=#17516b,bold"
    assert theme.tmux_style(theme.Style(fg="text")) == "fg=#ebebeb"


def test_a_vim_highlight_sets_every_field(theme: ModuleType) -> None:
    assert theme.vim_highlight("Normal", theme.Style(fg="text")) == (
        "hi Normal guifg=#ebebeb guibg=NONE guisp=NONE gui=NONE cterm=NONE"
    )


def test_a_palette_colour_unlike_the_ansi_one_of_its_name_is_refused(
    theme: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setitem(theme.PALETTE, "red", "#000001")
    with pytest.raises(ValueError, match=r"\['red'\]"):
        theme.starship_colours()


def test_the_catppuccin_file_names_its_release_and_every_colour(
    theme: ModuleType,
) -> None:
    text = theme.tmux_catppuccin()
    assert f"for Catppuccin's tmux plugin {theme.CATPPUCCIN_RELEASE}." in text
    names = [line.split()[2] for line in text.splitlines() if line.startswith("set")]
    assert names == [f"@thm_{name}" for name in theme.CATPPUCCIN]


def test_the_iterm2_preset_is_a_property_list_of_the_terminal_colours(
    theme: ModuleType,
) -> None:
    preset = plistlib.loads(theme.iterm2().encode())
    background = preset["Background Color"]
    assert (background["Red Component"], background["Blue Component"]) == (
        13 / 255,
        41 / 255,
    )
    assert len([key for key in preset if key.startswith("Ansi ")]) == 16


def test_the_vscode_theme_blends_opacities(theme: ModuleType) -> None:
    text = theme.vscode_theme()
    body = "".join(line for line in text.splitlines(keepends=True) if line[:2] != "//")
    colours = json.loads(body)["colors"]
    assert colours["diffEditor.removedTextBackground"] == "#f94f3033"
    assert colours["terminal.ansiBrightWhite"] == "#ffffff"


def test_main_writes_the_committed_theme_files_and_nothing_else(
    theme: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    out = tmp_path / "theme"
    shutil.copytree(ROOT / "LICENSES", tmp_path / "LICENSES")
    (out / "vim").mkdir(parents=True)
    (out / "vim" / "stale.vim").write_text("old\n")
    (out / "source").mkdir()
    (out / "source" / "kept.toml").write_text("mine\n")
    monkeypatch.setattr(theme, "THEME", out)

    theme.main()

    written = {
        path.relative_to(out)
        for path in out.rglob("*")
        if path.is_file() and path.parts[len(out.parts)] != "source"
    }
    assert len(written) == 11
    for path in written:
        committed = (ROOT / "theme" / path).read_text(encoding="utf-8")
        assert (out / path).read_text(encoding="utf-8") == committed, path
    assert not (out / "vim" / "stale.vim").exists()
    assert (out / "source" / "kept.toml").read_text() == "mine\n"
    assert capsys.readouterr().out == f"11 files written under {out}\n"
