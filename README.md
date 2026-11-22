# Edgeweave brand assets

Official logos, wordmarks and brand identifiers of Edgeweave, the company and
its products, with the tooling that generates them.

## Layout

| Path        | Content                                                                                            |
| ----------- | -------------------------------------------------------------------------------------------------- |
| `logo/`     | Symbol, full logo, wordmark and ASCII rendering: SVG masters, exports, generation scripts          |
| `theme/`    | Colour theme for terminals, editors and other tools, generated from one palette                    |
| `LICENSES/` | Licence texts, in the [REUSE](https://reuse.software) layout                                       |

[`logo/README.md`](logo/README.md) explains how the files are organised and
named, which one to pick, and how they are generated from the three masters.
[`theme/README.md`](theme/README.md) does the same for the colour theme, and
says how to install it in each application.

Just the logo files, with the terms of use, are
[edgeweave-logo.zip](https://github.com/edgeweave-showroom/brand/releases/latest/download/edgeweave-logo.zip)
on the latest release.

## Using the assets

Short version; the full terms are in [LICENSE.md](LICENSE.md).

- Use the marks as provided to refer to Edgeweave: articles, talks,
  documentation, "works with Edgeweave" notices, banners in tools that
  integrate with it.
- Do not alter them, do not make them part of your own branding, do not imply
  endorsement.
- The colour themes are CC BY-ND 4.0: use them and share them unmodified,
  with credit; do not share adapted versions.
- Scripts and documentation are MIT; the marks they reproduce are not.

## Checks

Every file is mapped to an SPDX identifier in [`REUSE.toml`](REUSE.toml).
Scripts are linted and formatted by [ruff](https://docs.astral.sh/ruff/) and
type-checked by [mypy](https://mypy-lang.org/) in strict mode, with the
configuration in [`pyproject.toml`](pyproject.toml); each `.py` file carries
its own SPDX header, since scripts get copied into other tools. The colour
themes must match their sources: CI generates them again and fails on any
difference. The colours for Catppuccin's tmux plugin are checked against the
release that `theme/source/palette.toml` names: the same `@thm_*` colours, and
a tmux status line that takes them.

[uv](https://docs.astral.sh/uv/) brings the toolchain: its own version in
`pyproject.toml`, Python's in `.python-version`, the tools' in `uv.lock`. Once
per clone:

```sh
uv sync
uv run pre-commit install
```

Each commit then fixes and formats the staged scripts, and each push runs the
gate: every check above except Catppuccin's, which needs tmux and a download.
CI runs the same gate, then Catppuccin's check. To run the gate by hand:

```sh
uv run pre-commit run --all-files --hook-stage pre-push
```

CI also audits the locked tools with
[pip-audit](https://github.com/pypa/pip-audit), checks the workflows with
[zizmor](https://docs.zizmor.sh/), and scans the whole history for secrets
with [gitleaks](https://github.com/gitleaks/gitleaks). Actions are pinned by
commit SHA, their version in a comment. Dependabot moves them and the tools
weekly, a week after each release.
