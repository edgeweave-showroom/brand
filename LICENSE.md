# Licensing

This repository holds three kinds of content, under three different sets of
terms.

## Brand assets: all rights reserved, limited permission to use

The Edgeweave name, symbol, wordmark, logos, ASCII rendering and other brand
identifiers (the "Marks"), that is, every asset file in this repository but
the colour themes, are trademarks and copyrighted works of Technologies
Edgeweave. They are **not** open source.

You may use them, unmodified, to refer to Edgeweave under the terms in
[`LICENSES/LicenseRef-Edgeweave-Brand.txt`](LICENSES/LicenseRef-Edgeweave-Brand.txt).

## Colour themes: CC BY-ND 4.0

The colour themes for terminals, editors and other tools, that is, the files
under `theme/terminal/`, `theme/editor/` and `theme/tool/`, and the sources
they are generated from, `theme/source/palette.toml` and
`theme/source/starship.toml`, are licensed under
Creative Commons Attribution-NoDerivatives 4.0 International
([`LICENSES/CC-BY-ND-4.0.txt`](LICENSES/CC-BY-ND-4.0.txt)). You may use them,
and share them unmodified, crediting Edgeweave and keeping their licence
notices. You may adjust them for your own use, but not share an adapted
version.

The licence grants no trademark rights (its section 2(b)(2)). The Edgeweave
name the themes carry stays under the brand terms: a theme of your own may
not be called Edgeweave.

## Scripts, tooling and documentation: MIT

The scripts that generate or export the assets, the repository configuration
and the documentation are released under the MIT License
([`LICENSES/MIT.txt`](LICENSES/MIT.txt)).

The MIT License covers the code only. It grants no right to the Marks that the
code reproduces or produces: an MIT-licensed script that draws the Edgeweave
logo does not make the logo MIT, and the one that writes the colour themes
does not make them MIT.

## Which terms apply to a given file

The repository follows the [REUSE specification](https://reuse.software/spec/).
[`REUSE.toml`](REUSE.toml) maps every path to its SPDX identifier, and
`reuse lint` verifies that no file is left unlabelled.
