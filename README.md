# Edgeweave brand assets

Official logos, wordmarks and brand identifiers of Edgeweave, the company and
its products, with the tooling that generates them.

## Layout

| Path        | Content                                                                                            |
| ----------- | -------------------------------------------------------------------------------------------------- |
| `logo/`     | Symbol, full logo and ASCII rendering: SVG masters, exports in every variant, generation scripts   |
| `LICENSES/` | Licence texts, in the [REUSE](https://reuse.software) layout                                       |

[`logo/README.md`](logo/README.md) explains how the files are organised and
named, which one to pick, and how they are generated from the two masters.

## Using the assets

Short version; the full terms are in [LICENSE.md](LICENSE.md).

- Use the marks as provided to refer to Edgeweave: articles, talks,
  documentation, "works with Edgeweave" notices, banners in tools that
  integrate with it.
- Do not alter them, do not make them part of your own branding, do not imply
  endorsement.
- Scripts and documentation are MIT; the marks they reproduce are not.

## Checks

Every file is mapped to an SPDX identifier in [`REUSE.toml`](REUSE.toml).
Scripts are linted and formatted by [ruff](https://docs.astral.sh/ruff/) and
type-checked by [mypy](https://mypy-lang.org/) in strict mode, with the
configuration in [`pyproject.toml`](pyproject.toml); each `.py` file carries
its own SPDX header, since scripts get copied into other tools. CI runs all of
it on every push. Locally:

```sh
uvx reuse lint
uvx ruff check && uvx ruff format --check
uvx mypy
```
