# Edgeweave brand assets

Official logos, wordmarks and brand identifiers of Edgeweave, the company and
its products, with the tooling that generates them.

## Layout

| Path        | Content                                                                                            |
| ----------- | -------------------------------------------------------------------------------------------------- |
| `logo/`     | Symbol, full logo and ASCII rendering: SVG masters, exports in every variant, generation scripts   |
| `LICENSES/` | Licence texts, in the [REUSE](https://reuse.software) layout                                       |

## Symbol and full logo

Two masters are the single source of every variant:
[`logo/symbol/source/edgeweave-symbol.svg`](logo/symbol/source/edgeweave-symbol.svg),
the symbol, framed, and
[`logo/full/source/edgeweave-logo.svg`](logo/full/source/edgeweave-logo.svg),
the symbol with the wordmark and the tagline. Both are the light theme on a
transparent background, and both are flattened, so that their tints do not
change with whatever they are placed on: every shape is opaque, and where two
translucent layers of the design overlap, the overlap is a shape of its own.
A shape's `class` is its recipe, top layer first; `primary-35-over-primary-25`
is the primary ink at 35 % over the primary ink at 25 %, composited on the
theme's background. The `<style>` block gives what each recipe flattens to,
and every shape has a stable `id`. The full logo embeds the symbol's shapes
under its own placement; the generator refuses to run if they differ from
the symbol master's. Each variant is a substitution on its master:

| Variant     | Change                                                                 |
| ----------- | ---------------------------------------------------------------------- |
| Dark theme  | recompute every recipe with cyan, orange and white on navy             |
| Monochrome  | recompute every recipe with black on white, or white on black          |
| Solid       | every recipe becomes its ink at 100 %; the `glow` shapes are dropped   |
| On a tile   | insert the `background` layer                                          |
| No frame    | drop the `frame` layer (symbol only)                                   |

[`logo/generate.py`](logo/generate.py) applies them and writes every variant
next to each `source/`, split by what it is for:

```
logo/
├── generate.py
├── symbol/
│   ├── source/        edgeweave-symbol.svg
│   ├── rgb/           screen: SVG and PNG (1000 px wide)
│   │   ├── light-bg/    edgeweave-symbol-light-{transparent,on-white}[-framed]
│   │   └── dark-bg/     edgeweave-symbol-dark-{transparent,on-navy}[-framed]
│   ├── cmyk/          print: PDF with DeviceCMYK inks, 500 × 500 pt
│   │   ├── light-bg/    same names, .pdf
│   │   └── dark-bg/
│   └── monochrome/    one ink, all three formats
│       ├── black/       edgeweave-symbol-black-transparent[-solid][-framed]
│       └── white/       edgeweave-symbol-white-transparent[-solid][-framed]
└── full/              the same tree, 960 × 240 pt, no frame
    ├── source/        edgeweave-logo.svg
    ├── rgb/           edgeweave-logo-{light,dark}-…
    ├── cmyk/
    └── monochrome/    edgeweave-logo-{black,white}-transparent[-solid]
```

A name reads theme, background, options: `-transparent` has nothing behind
the mark, `-on-white` and `-on-navy` the tile in that ink; `-solid` is the
single-tone version (monochrome only); `-framed` adds the border. The inks,
sRGB for screen and CMYK for print, are the `INKS` table of the script:

| Ink    | Role                             | sRGB      | CMYK              |
| ------ | -------------------------------- | --------- | ----------------- |
| teal   | primary, light theme             | `#00b5b5` | 67 / 0 / 27 / 0   |
| cyan   | primary, dark theme              | `#00dcff` | 50 / 0 / 4 / 0    |
| orange | accent, both themes              | `#ff622d` | 0 / 72 / 82 / 0   |
| navy   | background, dark theme           | `#0d1829` | 99 / 85 / 60 / 55 |
| white  | background, light theme; text, dark theme | `#ffffff` | 0 / 0 / 0 / 0 |
| black  | text, light theme; monochrome    | `#000000` | 0 / 0 / 0 / 100   |

The tagline is the text ink at 59 %. sRGB tints are computed by compositing,
and so are the CMYK tints of black and white, on the K plate alone. The
coloured CMYK values, inks and tints alike, are Affinity's conversions
through the U.S. Sheetfed Coated v2 profile; the tints are the `PRINT` table
of the script. The PDFs are written by the script itself, without a colour
profile, so those numbers reach the press as they are. PNG rendering needs
`rsvg-convert` from librsvg (`brew install librsvg`, `apt install
librsvg2-bin`). Edit a master, run the script, commit all of it.

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
