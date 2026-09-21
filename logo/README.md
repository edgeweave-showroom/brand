# Edgeweave logo

The symbol, the full logo (symbol, wordmark and tagline) and an ASCII
rendering for terminals. Every file under `symbol/` and `full/` is generated
from the two masters in `source/`; edit a master, run the script, commit all
of it. The same two directories, with the terms of use, are the zip attached
to every [release](https://github.com/edgeweave-showroom/brand/releases).

## Picking a file

```
symbol/                          the symbol alone
├── rgb/                         screen: SVG and PNG (1000 px wide)
│   ├── light_bg/                  for light backgrounds
│   └── dark_bg/                   for dark backgrounds
├── cmyk/                        print: PDF with DeviceCMYK inks
│   ├── light_bg/
│   └── dark_bg/
└── monochrome/                  one ink, SVG, PNG and PDF
    ├── black/                     for light backgrounds
    └── white/                     for dark backgrounds
full/                            the same tree for the full logo
```

A file name is a list of tags, separated by hyphens, and spells everything
out: `edgeweave-symbol-light-on_white-framed.svg`.

| Tag                         | Meaning                                                        |
| --------------------------- | -------------------------------------------------------------- |
| `symbol`, `logo`            | the symbol alone, or the full logo                             |
| `light`, `dark`             | colour theme, for light or dark backgrounds                    |
| `black`, `white`            | monochrome, for light or dark backgrounds                      |
| `transparent`               | nothing behind the mark                                        |
| `on_white`, `on_navy`       | the theme's tile behind the mark, in that ink                  |
| `solid`                     | single tone, no tints (monochrome only)                        |
| `framed`                    | with the border (symbol only)                                  |

The marks are flattened: their tints are fixed colours, not transparency, so
they look the same on any background of the right kind. Sizes: the symbol is
500 × 500 units (500 × 500 pt in PDF), the full logo 4000 × 1000 units
(960 × 240 pt).

## Sources and generation

[`source/edgeweave-symbol.svg`](source/edgeweave-symbol.svg), the symbol,
framed, and [`source/edgeweave-logo.svg`](source/edgeweave-logo.svg), the
full logo, are the single source of every variant. Both are the light theme
on a transparent background, and both are flattened: every shape is opaque,
and where two translucent layers of the design overlap, the overlap is a
shape of its own. A shape's `class` is its recipe, top layer first;
`primary-35-over-primary-25` is the primary ink at 35 % over the primary ink
at 25 %, composited on the theme's background. The `<style>` block gives what
each recipe flattens to, and every shape has a stable `id`. The full logo
embeds the symbol's shapes under its own placement; the generator refuses to
run if they differ from the symbol master's. Each variant is a substitution
on its master:

| Variant     | Change                                                                 |
| ----------- | ---------------------------------------------------------------------- |
| Dark theme  | recompute every recipe with cyan, orange and white on navy             |
| Monochrome  | recompute every recipe with black on white, or white on black          |
| Solid       | every recipe becomes its ink at 100 %; the `glow` shapes are dropped   |
| On a tile   | insert the `background` layer                                          |
| No frame    | drop the `frame` layer (symbol only)                                   |

[`source/generate.py`](source/generate.py) applies them and writes every
variant. The inks, sRGB for screen and CMYK for print, are its `INKS` table:

| Ink    | Role                                      | sRGB      | CMYK              |
| ------ | ----------------------------------------- | --------- | ----------------- |
| teal   | primary, light theme                      | `#00b5b5` | 67 / 0 / 27 / 0   |
| cyan   | primary, dark theme                       | `#00dcff` | 50 / 0 / 4 / 0    |
| orange | accent, both themes                       | `#ff622d` | 0 / 72 / 82 / 0   |
| navy   | background, dark theme                    | `#0d1829` | 99 / 85 / 60 / 55 |
| white  | background, light theme; text, dark theme | `#ffffff` | 0 / 0 / 0 / 0     |
| black  | text, light theme; monochrome             | `#000000` | 0 / 0 / 0 / 100   |

The tagline is the text ink at 59 %. sRGB tints are computed by compositing,
and so are the CMYK tints of black and white, on the K plate alone. The
coloured CMYK values, inks and tints alike, are Affinity's conversions
through the U.S. Sheetfed Coated v2 profile; the tints are the `PRINT` table
of the script. The PDFs are written by the script itself, without a colour
profile, so those numbers reach the press as they are.

```sh
brew install librsvg        # or: apt install librsvg2-bin; for the PNGs
source/generate.py
```

## Release package

[`source/package.py`](source/package.py) bundles `symbol/`, `full/`, the
terms of use and the "Picking a file" section above into
`dist/edgeweave-logo.zip`, for people who will not clone the repository. CI
builds it on every pull request, and every push to `main` that changes any of
its content publishes a GitHub release with it, numbered after the previous
one: `v1.0`, `v1.1`, and so on. So the latest one is always at
`releases/latest/download/edgeweave-logo.zip`. For another number, a redesign
say, run the workflow by hand with the version as input.

```sh
source/package.py v1.0
```

## Typography

The wordmark is set in [Sora](https://fonts.google.com/specimen/Sora)
ExtraBold, the tagline in [IBM Plex Sans](https://github.com/IBM/plex)
Regular, tracked capitals. Both are outlines in the masters: nothing in this repository needs
the fonts, and the outlines are part of the marks. The fonts themselves are
free under the SIL Open Font License 1.1, which leaves artwork made with
them, such as these, outside its terms.

## ASCII rendering

[`ascii/ascii-logo.py`](ascii/ascii-logo.py) prints the logo in a terminal,
stacking coloured layers of ASCII art. It picks the colour mode from the
terminal, or takes one; it can print the symbol, the wordmark or both; and
`--sh` emits POSIX shell code that prints the logo without Python, to paste
into a tool's banner:

```sh
ascii/ascii-logo.py                  # symbol, wordmark and tagline
ascii/ascii-logo.py -p symbol -c 256
ascii/ascii-logo.py --sh -o logo.sh
```
