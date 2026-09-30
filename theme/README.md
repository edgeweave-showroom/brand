# Edgeweave colour theme

The Edgeweave colours for terminals, editors and the tools that run in them,
a directory per application. Every file in them is generated from
[`source/palette.toml`](source/palette.toml) by
[`source/generate.py`](source/generate.py); edit the palette, run the script,
commit all of it. The theme is dark only for now, named
`edgeweave-dark` so that a light one can join it.

## Picking a file

```
ghostty/     edgeweave-dark
iterm2/      edgeweave-dark.itermcolors
vim/         colors/edgeweave.vim, for Vim and Neovim, and
             autoload/airline/themes/edgeweave.vim, for vim-airline
vscode/      an extension: package.json, themes/, LICENSE
tmux/        edgeweave-dark.conf, and edgeweave-dark-catppuccin.conf
             for Catppuccin's plugin
starship/    edgeweave-dark-palette-only.toml, to merge, and
             edgeweave-dark.toml, a whole configuration
```

Terminals take the 16 ANSI colours, which every program in them follows.
Editors colour code by role, and paint their interface. tmux and Starship
use hex values, the same in any terminal. Each file opens with its name, how
to install it and its licence notice.

## Installing

**Ghostty.** Copy `ghostty/edgeweave-dark` into
`~/.config/ghostty/themes/`, and in the Ghostty config:

```
theme = edgeweave-dark
```

**iTerm2.** Settings > Profiles > Colors > Color Presets > Import, pick
`iterm2/edgeweave-dark.itermcolors`, then choose it in the same menu.

**Vim and Neovim.** Copy `vim/colors/edgeweave.vim` into `~/.vim/colors/` or
`~/.config/nvim/colors/`, or load `vim/` as a plugin; with vim-plug,
`Plug 'edgeweave-showroom/brand', { 'rtp': 'theme/vim' }`. Then:

```vim
set termguicolors
colorscheme edgeweave
```

The scheme is in 24-bit colour only: without `termguicolors`, Vim keeps its
own colours. Neovim turns it on by itself in terminals that support it.

**vim-airline.** Loaded as a plugin, `vim/` brings the airline theme along;
otherwise copy `vim/autoload/airline/themes/edgeweave.vim` into
`~/.vim/autoload/airline/themes/` or `~/.config/nvim/autoload/airline/themes/`.
vim-airline takes it with `colorscheme edgeweave`, unless the vimrc names
another theme; then name this one instead:

```vim
let g:airline_theme = 'edgeweave'
```

The mode shows in cerulean, green in insert and terminal modes, violet in
visual mode, vermilion in replace mode and amber on the command line; the
file name turns amber while it has unsaved changes. Like the scheme, the
theme is in 24-bit colour only: without `termguicolors`, the status line is
plain.

**VS Code.** Package `vscode/` as an extension, install it, then pick
Edgeweave Dark in Preferences: Color Theme.

```sh
cd vscode && npx @vscode/vsce package
code --install-extension edgeweave-theme-1.0.0.vsix
```

**tmux.** In `tmux.conf`; the second line lets tmux send 24-bit colours to
the terminal, instead of rounding them to the nearest of 256:

```tmux
source-file ~/.config/tmux/edgeweave-dark.conf
set -as terminal-features ",xterm*:RGB"
```

With [Catppuccin's tmux plugin](https://github.com/catppuccin/tmux), source
`tmux/edgeweave-dark-catppuccin.conf` instead, before the plugin loads:
Catppuccin keeps colours set before it, and takes these in place of its
flavour. Its layers match the palette's; its fourteen accents go to the
nearest of the palette's, several to one. Written for Catppuccin v2.3.1.
Without the plugin, the file does nothing.

**Starship.** To keep your own prompt, merge
`starship/edgeweave-dark-palette-only.toml` into `~/.config/starship.toml`,
its `palette` line before any table. Your styles can then name every colour
below, `bg:surface1`, `fg:amber`, and those written with Starship's own
names, `red` or `bright-blue`, take the ANSI colours of the theme: an
existing configuration follows it unchanged.

For the Edgeweave prompt as well, `starship/edgeweave-dark.toml` is a whole
configuration, palette included, for Starship 1.25 or later: copy it to
`~/.config/starship.toml`, or point `STARSHIP_CONFIG` at it; an older one
warns of a module it lacks, `maven` before 1.25, and ignores it. The
prompt symbol turns cerulean, vermilion after a failed command; the words
between modules, _on_, _via_, _took_, fade to slate. Every module takes its
symbol from Starship's
[Nerd Font Symbols](https://starship.rs/presets/nerd-font) preset, so the
terminal needs a [Nerd Font](https://www.nerdfonts.com).

## Palette

Tested in Ghostty: neutral layers tinted towards the navy of the logo,
darkest first, then the brand colours, then accents softened for text on the
navy. Contrast is against the background, for the colours that write text.

| Name        | sRGB      | Contrast | Use                                                      |
| ----------- | --------- | -------- | -------------------------------------------------------- |
| `crust`     | `#080f1a` |          | VS Code's title, activity and status bars                |
| `mantle`    | `#0a1321` |          | side panels, floating windows, tmux status line          |
| `base`      | `#0d1829` |          | Midnight Navy, the background                            |
| `surface0`  | `#142137` |          | current line, menus, folds                               |
| `surface1`  | `#1b2a45` |          | Deep Slate Blue: ANSI black, status lines                |
| `surface2`  | `#26395a` |          | borders, whitespace characters                           |
| `overlay0`  | `#4a5a75` | 2.6:1    | ANSI bright black (autosuggestions), line numbers        |
| `dim`       | `#56657d` | 3.0:1    | comments                                                 |
| `slate`     | `#7a879b` | 4.9:1    | secondary information, operators and punctuation         |
| `subtext0`  | `#8a8a8a` | 5.2:1    | Mid Grey, reserved                                       |
| `subtext1`  | `#bdbfc1` | 9.7:1    | text, ANSI white                                         |
| `text`      | `#ebebeb` | 14.9:1   | Smoke White: emphasis, selected text                     |
| `petrol`    | `#17516b` |          | Deep Petrol: selection                                   |
| `cerulean`  | `#27a6c7` | 6.2:1    | ANSI blue: cursor, prompt symbol, functions              |
| `vermilion` | `#f94f30` | 5.2:1    | ANSI red: errors                                         |
| `cyan`      | `#56c8d8` | 9.0:1    | ANSI cyan: types, escapes                                |
| `violet`    | `#9a92de` | 6.4:1    | ANSI magenta: keywords                                   |
| `amber`     | `#d9a55b` | 8.0:1    | ANSI yellow: constants, search matches, warnings         |
| `green`     | `#8cbf7a` | 8.3:1    | ANSI green: strings                                      |

The bright ANSI colours are lighter accents of their own, `#ff7a5e`,
`#a8d69a`, `#e8c080`, `#5cc0db`, `#b4aee8` and `#85dce8`, and bright white is
the wordmark's `#ffffff`.

## Generation

[`source/palette.toml`](source/palette.toml) holds every colour decision: the
palette and, after it, how each application maps it. The ANSI colours and the
terminal roles; code by role, then Vim's syntax groups and VS Code's scopes
for each role; the interfaces of Vim, with vim-airline's status line, VS Code
and tmux, and Catppuccin's colours for its tmux plugin. A colour there is a
palette name, a bright ANSI colour by name, `bright-red`, or `#rrggbb`, at an
opacity if one follows, `"green 20%"`: VS Code blends it, the others get it flattened over the
background.

Starship's prompt is the exception: [`source/starship.toml`](source/starship.toml)
is a Starship configuration without its palette, and names the colours
itself, since the palette travels with it. Its module formats are Starship
1.26's, the linking word dimmed; a new Starship may bring modules or formats
to carry over.

[`source/generate.py`](source/generate.py) knows the file formats only. It
needs nothing but Python 3.14.

```sh
source/generate.py
```

## Licence

The theme files, `palette.toml` and `starship.toml` are licensed under
CC BY-ND 4.0: use them and share them unmodified, with their notice; adjust
them for yourself, but do not share an adapted version. The Edgeweave name on
them stays under the brand terms. The symbols in the Starship prompt are
Starship's, under the ISC licence. The script and this README are MIT.
[LICENSE.md](../LICENSE.md) has the details.
