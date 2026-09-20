# Edgeweave brand assets

Official logos, wordmarks and brand identifiers of Edgeweave, the company and
its products, with the tooling that generates them.

## Layout

| Path        | Content                                                                                            |
| ----------- | -------------------------------------------------------------------------------------------------- |
| `logo/`     | Symbol, full logo and ASCII rendering: SVG masters, exports in every variant, generation scripts   |
| `LICENSES/` | Licence texts, in the [REUSE](https://reuse.software) layout                                       |

## Symbol master

[`logo/symbol/edgeweave-symbol.svg`](logo/symbol/edgeweave-symbol.svg) is the
single source of every symbol variant. It is the framed, light-theme symbol on
its background; colours are the three classes in its `<style>` block, per-layer
opacities are `fill-opacity` attributes, and every layer has a stable `id`.
Each variant is a substitution on it:

| Variant       | Change                                                                  |
| ------------- | ----------------------------------------------------------------------- |
| Dark theme    | `.background` → `#0d1829`, `.primary` → `#00dcff`; `.accent` unchanged  |
| Monochrome    | `.primary` and `.accent` → black or white                               |
| Flat          | drop every `fill-opacity` and the `glow` layer                          |
| No frame      | drop the `frame` layer                                                  |
| No background | drop the `background` layer                                             |

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
