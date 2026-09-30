" Edgeweave Dark for Vim and Neovim
" Copy to ~/.vim/colors/ (Neovim: ~/.config/nvim/colors/), then:
"   set termguicolors
"   colorscheme edgeweave
"
" Generated from theme/source/palette.toml, https://github.com/edgeweave-showroom/brand
" SPDX-FileCopyrightText: 2026 Technologies Edgeweave
" SPDX-License-Identifier: CC-BY-ND-4.0

set background=dark
hi clear
let g:colors_name = 'edgeweave'

hi Normal guifg=#bdbfc1 guibg=#0d1829 guisp=NONE gui=NONE cterm=NONE
hi NormalFloat guifg=#bdbfc1 guibg=#0a1321 guisp=NONE gui=NONE cterm=NONE
hi FloatBorder guifg=#26395a guibg=#0a1321 guisp=NONE gui=NONE cterm=NONE
hi FloatShadow guifg=NONE guibg=#080f1a guisp=NONE gui=NONE cterm=NONE
hi FloatShadowThrough guifg=NONE guibg=#080f1a guisp=NONE gui=NONE cterm=NONE
hi Cursor guifg=#0d1829 guibg=#27a6c7 guisp=NONE gui=NONE cterm=NONE
hi lCursor guifg=#0d1829 guibg=#27a6c7 guisp=NONE gui=NONE cterm=NONE
hi CursorLine guifg=NONE guibg=#142137 guisp=NONE gui=NONE cterm=NONE
hi CursorColumn guifg=NONE guibg=#142137 guisp=NONE gui=NONE cterm=NONE
hi ColorColumn guifg=NONE guibg=#142137 guisp=NONE gui=NONE cterm=NONE
hi CursorLineNr guifg=#27a6c7 guibg=NONE guisp=NONE gui=bold cterm=bold
hi LineNr guifg=#4a5a75 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi SignColumn guifg=#4a5a75 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi FoldColumn guifg=#4a5a75 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Folded guifg=#7a879b guibg=#142137 guisp=NONE gui=NONE cterm=NONE
hi Conceal guifg=#4a5a75 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi NonText guifg=#26395a guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi SpecialKey guifg=#4a5a75 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Directory guifg=#27a6c7 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi VertSplit guifg=#26395a guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi StatusLine guifg=#bdbfc1 guibg=#1b2a45 guisp=NONE gui=NONE cterm=NONE
hi StatusLineNC guifg=#56657d guibg=#0a1321 guisp=NONE gui=NONE cterm=NONE
hi StatusLineTerm guifg=#bdbfc1 guibg=#1b2a45 guisp=NONE gui=NONE cterm=NONE
hi StatusLineTermNC guifg=#56657d guibg=#0a1321 guisp=NONE gui=NONE cterm=NONE
hi WinBar guifg=#bdbfc1 guibg=NONE guisp=NONE gui=bold cterm=bold
hi WinBarNC guifg=#56657d guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi TabLine guifg=#7a879b guibg=#0a1321 guisp=NONE gui=NONE cterm=NONE
hi TabLineFill guifg=NONE guibg=#080f1a guisp=NONE gui=NONE cterm=NONE
hi TabLineSel guifg=#ebebeb guibg=#0d1829 guisp=NONE gui=bold cterm=bold
hi ToolbarLine guifg=NONE guibg=#142137 guisp=NONE gui=NONE cterm=NONE
hi ToolbarButton guifg=#ebebeb guibg=#1b2a45 guisp=NONE gui=bold cterm=bold
hi Pmenu guifg=#bdbfc1 guibg=#142137 guisp=NONE gui=NONE cterm=NONE
hi PmenuSel guifg=#ebebeb guibg=#17516b guisp=NONE gui=NONE cterm=NONE
hi PmenuSbar guifg=NONE guibg=#1b2a45 guisp=NONE gui=NONE cterm=NONE
hi PmenuThumb guifg=NONE guibg=#4a5a75 guisp=NONE gui=NONE cterm=NONE
hi WildMenu guifg=#0d1829 guibg=#27a6c7 guisp=NONE gui=NONE cterm=NONE
hi Visual guifg=#ebebeb guibg=#17516b guisp=NONE gui=NONE cterm=NONE
hi VisualNOS guifg=#ebebeb guibg=#17516b guisp=NONE gui=NONE cterm=NONE
hi Search guifg=#0d1829 guibg=#d9a55b guisp=NONE gui=NONE cterm=NONE
hi CurSearch guifg=#0d1829 guibg=#27a6c7 guisp=NONE gui=NONE cterm=NONE
hi IncSearch guifg=#0d1829 guibg=#27a6c7 guisp=NONE gui=NONE cterm=NONE
hi MatchParen guifg=#d9a55b guibg=#26395a guisp=NONE gui=bold cterm=bold
hi QuickFixLine guifg=NONE guibg=#1b2a45 guisp=NONE gui=NONE cterm=NONE
hi ErrorMsg guifg=#f94f30 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi WarningMsg guifg=#d9a55b guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi ModeMsg guifg=#ebebeb guibg=NONE guisp=NONE gui=bold cterm=bold
hi MoreMsg guifg=#8cbf7a guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi OkMsg guifg=#8cbf7a guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Question guifg=#8cbf7a guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Todo guifg=#0d1829 guibg=#d9a55b guisp=NONE gui=bold cterm=bold
hi DiffAdd guifg=NONE guibg=#263939 guisp=NONE gui=NONE cterm=NONE
hi DiffChange guifg=NONE guibg=#112d41 guisp=NONE gui=NONE cterm=NONE
hi DiffDelete guifg=#26395a guibg=#3c232a guisp=NONE gui=NONE cterm=NONE
hi DiffText guifg=NONE guibg=#164a60 guisp=NONE gui=NONE cterm=NONE
hi SpellBad guifg=NONE guibg=NONE guisp=#f94f30 gui=undercurl cterm=undercurl
hi SpellCap guifg=NONE guibg=NONE guisp=#d9a55b gui=undercurl cterm=undercurl
hi SpellLocal guifg=NONE guibg=NONE guisp=#56c8d8 gui=undercurl cterm=undercurl
hi SpellRare guifg=NONE guibg=NONE guisp=#9a92de gui=undercurl cterm=undercurl
hi DiagnosticError guifg=#f94f30 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi DiagnosticWarn guifg=#d9a55b guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi DiagnosticInfo guifg=#27a6c7 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi DiagnosticHint guifg=#56c8d8 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi DiagnosticOk guifg=#8cbf7a guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi DiagnosticUnderlineError guifg=NONE guibg=NONE guisp=#f94f30 gui=undercurl cterm=undercurl
hi DiagnosticUnderlineWarn guifg=NONE guibg=NONE guisp=#d9a55b gui=undercurl cterm=undercurl
hi DiagnosticUnderlineInfo guifg=NONE guibg=NONE guisp=#27a6c7 gui=undercurl cterm=undercurl
hi DiagnosticUnderlineHint guifg=NONE guibg=NONE guisp=#56c8d8 gui=undercurl cterm=undercurl
hi DiagnosticUnderlineOk guifg=NONE guibg=NONE guisp=#8cbf7a gui=undercurl cterm=undercurl
hi DiagnosticDeprecated guifg=NONE guibg=NONE guisp=#f94f30 gui=strikethrough cterm=strikethrough
hi Comment guifg=#56657d guibg=NONE guisp=NONE gui=italic cterm=italic
hi Constant guifg=#d9a55b guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi String guifg=#8cbf7a guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Character guifg=#8cbf7a guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Identifier guifg=#bdbfc1 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Function guifg=#27a6c7 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Statement guifg=#9a92de guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Operator guifg=#7a879b guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi PreProc guifg=#9a92de guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Type guifg=#56c8d8 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Special guifg=#56c8d8 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Delimiter guifg=#7a879b guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Underlined guifg=#27a6c7 guibg=NONE guisp=NONE gui=underline cterm=underline
hi Error guifg=#f94f30 guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Title guifg=#27a6c7 guibg=NONE guisp=NONE gui=bold cterm=bold
hi Added guifg=#8cbf7a guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Changed guifg=#d9a55b guibg=NONE guisp=NONE gui=NONE cterm=NONE
hi Removed guifg=#f94f30 guibg=NONE guisp=NONE gui=NONE cterm=NONE

if has('nvim')
  hi! link @variable Identifier
endif

let g:terminal_ansi_colors = ['#1b2a45', '#f94f30', '#8cbf7a', '#d9a55b', '#27a6c7', '#9a92de', '#56c8d8', '#bdbfc1', '#4a5a75', '#ff7a5e', '#a8d69a', '#e8c080', '#5cc0db', '#b4aee8', '#85dce8', '#ffffff']
let g:terminal_color_0 = '#1b2a45'
let g:terminal_color_1 = '#f94f30'
let g:terminal_color_2 = '#8cbf7a'
let g:terminal_color_3 = '#d9a55b'
let g:terminal_color_4 = '#27a6c7'
let g:terminal_color_5 = '#9a92de'
let g:terminal_color_6 = '#56c8d8'
let g:terminal_color_7 = '#bdbfc1'
let g:terminal_color_8 = '#4a5a75'
let g:terminal_color_9 = '#ff7a5e'
let g:terminal_color_10 = '#a8d69a'
let g:terminal_color_11 = '#e8c080'
let g:terminal_color_12 = '#5cc0db'
let g:terminal_color_13 = '#b4aee8'
let g:terminal_color_14 = '#85dce8'
let g:terminal_color_15 = '#ffffff'
