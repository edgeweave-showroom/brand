# SPDX-FileCopyrightText: 2026 Technologies Edgeweave
# SPDX-License-Identifier: MIT
"""logo/ascii/ascii-logo.py: stacking, composition, and its two outputs."""

import shutil
import subprocess
import sys
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path
    from types import ModuleType

Grid = list[list[tuple[str, str | None]]]


def text(grid: Grid) -> list[str]:
    return ["".join(ch for ch, _ in row).rstrip() for row in grid]


@pytest.fixture
def full(ascii_logo: ModuleType) -> Grid:
    """Compose the whole logo, as the command line draws it by default."""
    grid: Grid = ascii_logo.compose(ascii_logo.trim_left(ascii_logo.stack()), "tagline")
    return grid


def run_sh(code: str, env: dict[str, str]) -> str:
    """Run shell code with sh in a bare environment, return what it prints."""
    sh = shutil.which("sh")
    assert sh is not None
    done = subprocess.run(  # noqa: S603  # sh on code this test generated
        [sh], input=code, env=env, capture_output=True, text=True, check=True
    )
    assert done.stderr == ""
    return done.stdout


def test_a_layer_keeps_its_leading_blank_lines_but_not_its_trailing_ones(
    ascii_logo: ModuleType,
) -> None:
    assert ascii_logo.rows("\n\nab\n  \n") == ["", "ab"]


def test_the_upper_layer_wins_where_two_layers_draw(ascii_logo: ModuleType) -> None:
    assert ascii_logo.stack([("low", "xx\nxx"), ("high", " y")]) == [
        [("x", "low"), ("y", "high")],
        [("x", "low"), ("x", "low")],
    ]


def test_blank_columns_on_the_left_are_trimmed(ascii_logo: ModuleType) -> None:
    grid = [[(" ", None), ("a", "l")], [(" ", None), (" ", None)]]
    assert ascii_logo.trim_left(grid) == [[("a", "l")], [(" ", None)]]
    assert ascii_logo.trim_left([[("a", "l")]]) == [[("a", "l")]]


def test_the_wordmark_alone_starts_at_the_margin(ascii_logo: ModuleType) -> None:
    grid = ascii_logo.compose([], "wordmark", margin=2)
    assert text(grid)[0].startswith("  ▗▄▄▄▖")


def test_the_tagline_sits_right_aligned_under_the_wordmark(
    ascii_logo: ModuleType, full: Grid
) -> None:
    lines = text(full)
    wordmark = [line.rstrip() for line in ascii_logo.WORDMARK.split("\n")]
    end = max(len(line) for line in lines[:-1] if line)
    assert lines[-1].endswith(ascii_logo.TAGLINE)
    assert len(lines[-1]) == end
    assert any(line.endswith(wordmark[2]) for line in lines)


def test_the_symbol_alone_is_only_the_hexagon(ascii_logo: ModuleType) -> None:
    lines = text(ascii_logo.compose(ascii_logo.trim_left(ascii_logo.stack()), "symbol"))
    assert lines[0] == "          _.-'0'-._"
    assert not any("▗" in line for line in lines)


def test_without_colour_the_render_is_the_bare_drawing(
    ascii_logo: ModuleType, full: Grid
) -> None:
    assert ascii_logo.render(full, "none").split("\n") == text(full)


def test_a_colour_code_is_written_only_when_the_layer_changes(
    ascii_logo: ModuleType,
) -> None:
    grid = [[("a", "core"), ("b", "core"), (" ", None), ("c", "tagline")]]
    core, tagline = ascii_logo.seq("core", "256"), ascii_logo.seq("tagline", "256")
    assert core == "\033[1;38;5;202m"
    assert ascii_logo.render(grid, "256") == f"{core}ab {tagline}c\033[0m"


def test_true_colour_writes_the_exact_brand_values(ascii_logo: ModuleType) -> None:
    assert ascii_logo.seq("core", "true") == "\033[1;38;2;249;79;48m"
    assert ascii_logo.seq("core", "none") == ""
    assert ascii_logo.hex_rgb("core") == "#F94F30"


@pytest.mark.parametrize(
    ("env", "tty", "mode"),
    [
        ({"NO_COLOR": "1", "COLORTERM": "truecolor"}, True, "none"),
        ({"TERM": "dumb"}, True, "none"),
        ({"COLORTERM": "truecolor"}, False, "none"),
        ({"COLORTERM": "truecolor"}, True, "true"),
        ({"COLORTERM": "24bit"}, True, "true"),
        ({}, True, "256"),
    ],
)
def test_the_colour_mode_follows_the_environment_and_the_terminal(
    ascii_logo: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    env: dict[str, str],
    *,
    tty: bool,
    mode: str,
) -> None:
    for name in ("NO_COLOR", "TERM", "COLORTERM"):
        monkeypatch.delenv(name, raising=False)
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: tty)
    assert ascii_logo.autodetect() == mode


@pytest.mark.parametrize(
    ("env", "mode"),
    [
        ({"NO_COLOR": "1", "COLORTERM": "truecolor"}, "none"),
        ({"TERM": "dumb"}, "none"),
        ({"COLORTERM": "truecolor"}, "true"),
        ({"COLORTERM": "24bit"}, "true"),
        ({}, "256"),
    ],
)
def test_the_shell_code_prints_what_the_script_renders(
    ascii_logo: ModuleType, full: Grid, env: dict[str, str], mode: str
) -> None:
    printed = run_sh(ascii_logo.emit_sh(full), env)
    assert printed == ascii_logo.render(full, mode) + "\n"


@pytest.mark.parametrize("mode", ["true", "256", "none"])
def test_shell_code_for_one_mode_ignores_the_environment(
    ascii_logo: ModuleType, full: Grid, mode: str
) -> None:
    printed = run_sh(ascii_logo.emit_sh(full, mode), {"NO_COLOR": "1"})
    assert printed == ascii_logo.render(full, mode) + "\n"


@pytest.mark.skipif(shutil.which("shellcheck") is None, reason="needs shellcheck")
@pytest.mark.parametrize("mode", ["auto", "true", "256", "none"])
def test_the_shell_code_is_shellcheck_clean(
    ascii_logo: ModuleType, full: Grid, mode: str
) -> None:
    shellcheck = shutil.which("shellcheck")
    assert shellcheck is not None
    subprocess.run(  # noqa: S603  # shellcheck on code this test generated
        [shellcheck, "-"], input=ascii_logo.emit_sh(full, mode), text=True, check=True
    )


def test_the_command_prints_the_bare_logo_when_stdout_is_not_a_terminal(
    ascii_logo: ModuleType,
    full: Grid,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(sys, "argv", ["ascii-logo.py"])
    ascii_logo.main()
    captured = capsys.readouterr()
    assert captured.out == ascii_logo.render(full, "none") + "\n"
    assert captured.err == ""


def test_the_command_warns_when_the_logo_is_wider_than_asked(
    ascii_logo: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(sys, "argv", ["ascii-logo.py", "-p", "symbol", "-w", "10"])
    ascii_logo.main()
    assert (
        capsys.readouterr().err == "warning: 25 columns, 15 over the 10-column target\n"
    )


def test_the_command_writes_shell_code_to_a_file(
    ascii_logo: ModuleType,
    full: Grid,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    out = tmp_path / "logo.sh"
    argv = ["ascii-logo.py", "--sh", "-c", "256", "-o", str(out)]
    monkeypatch.setattr(sys, "argv", argv)
    ascii_logo.main()
    assert out.read_text(encoding="utf-8") == ascii_logo.emit_sh(full, "256")
