" Edgeweave Dark for vim-airline
" Copy to ~/.vim/autoload/airline/themes/
" (Neovim: ~/.config/nvim/autoload/airline/themes/). vim-airline takes it
" with colorscheme edgeweave, unless the vimrc names another theme:
"   let g:airline_theme = 'edgeweave'
"
" Generated from theme/source/palette.toml, https://github.com/edgeweave-showroom/brand
" SPDX-FileCopyrightText: 2026 Technologies Edgeweave
" SPDX-License-Identifier: CC-BY-ND-4.0

let g:airline#themes#edgeweave#palette = {}

let g:airline#themes#edgeweave#palette.normal = {
      \ 'airline_a': ['#0d1829', '#27a6c7', '', '', ''],
      \ 'airline_b': ['#27a6c7', '#142137', '', '', ''],
      \ 'airline_c': ['#bdbfc1', '#0a1321', '', '', ''],
      \ 'airline_x': ['#bdbfc1', '#0a1321', '', '', ''],
      \ 'airline_y': ['#27a6c7', '#142137', '', '', ''],
      \ 'airline_z': ['#0d1829', '#27a6c7', '', '', ''],
      \ 'airline_warning': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_error': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_term': ['#bdbfc1', '#0a1321', '', '', ''],
      \ }
let g:airline#themes#edgeweave#palette.normal_modified = {
      \ 'airline_c': ['#d9a55b', '#0a1321', '', '', ''],
      \ 'airline_warning': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_error': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_term': ['#bdbfc1', '#0a1321', '', '', ''],
      \ }

let g:airline#themes#edgeweave#palette.insert = {
      \ 'airline_a': ['#0d1829', '#8cbf7a', '', '', ''],
      \ 'airline_b': ['#8cbf7a', '#142137', '', '', ''],
      \ 'airline_c': ['#bdbfc1', '#0a1321', '', '', ''],
      \ 'airline_x': ['#bdbfc1', '#0a1321', '', '', ''],
      \ 'airline_y': ['#8cbf7a', '#142137', '', '', ''],
      \ 'airline_z': ['#0d1829', '#8cbf7a', '', '', ''],
      \ 'airline_warning': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_error': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_term': ['#bdbfc1', '#0a1321', '', '', ''],
      \ }
let g:airline#themes#edgeweave#palette.insert_modified = {
      \ 'airline_c': ['#d9a55b', '#0a1321', '', '', ''],
      \ 'airline_warning': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_error': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_term': ['#bdbfc1', '#0a1321', '', '', ''],
      \ }

let g:airline#themes#edgeweave#palette.replace = {
      \ 'airline_a': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_b': ['#f94f30', '#142137', '', '', ''],
      \ 'airline_c': ['#bdbfc1', '#0a1321', '', '', ''],
      \ 'airline_x': ['#bdbfc1', '#0a1321', '', '', ''],
      \ 'airline_y': ['#f94f30', '#142137', '', '', ''],
      \ 'airline_z': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_warning': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_error': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_term': ['#bdbfc1', '#0a1321', '', '', ''],
      \ }
let g:airline#themes#edgeweave#palette.replace_modified = {
      \ 'airline_c': ['#d9a55b', '#0a1321', '', '', ''],
      \ 'airline_warning': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_error': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_term': ['#bdbfc1', '#0a1321', '', '', ''],
      \ }

let g:airline#themes#edgeweave#palette.visual = {
      \ 'airline_a': ['#0d1829', '#9a92de', '', '', ''],
      \ 'airline_b': ['#9a92de', '#142137', '', '', ''],
      \ 'airline_c': ['#bdbfc1', '#0a1321', '', '', ''],
      \ 'airline_x': ['#bdbfc1', '#0a1321', '', '', ''],
      \ 'airline_y': ['#9a92de', '#142137', '', '', ''],
      \ 'airline_z': ['#0d1829', '#9a92de', '', '', ''],
      \ 'airline_warning': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_error': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_term': ['#bdbfc1', '#0a1321', '', '', ''],
      \ }
let g:airline#themes#edgeweave#palette.visual_modified = {
      \ 'airline_c': ['#d9a55b', '#0a1321', '', '', ''],
      \ 'airline_warning': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_error': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_term': ['#bdbfc1', '#0a1321', '', '', ''],
      \ }

let g:airline#themes#edgeweave#palette.commandline = {
      \ 'airline_a': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_b': ['#d9a55b', '#142137', '', '', ''],
      \ 'airline_c': ['#bdbfc1', '#0a1321', '', '', ''],
      \ 'airline_x': ['#bdbfc1', '#0a1321', '', '', ''],
      \ 'airline_y': ['#d9a55b', '#142137', '', '', ''],
      \ 'airline_z': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_warning': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_error': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_term': ['#bdbfc1', '#0a1321', '', '', ''],
      \ }
let g:airline#themes#edgeweave#palette.commandline_modified = {
      \ 'airline_c': ['#d9a55b', '#0a1321', '', '', ''],
      \ 'airline_warning': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_error': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_term': ['#bdbfc1', '#0a1321', '', '', ''],
      \ }

let g:airline#themes#edgeweave#palette.terminal = {
      \ 'airline_a': ['#0d1829', '#8cbf7a', '', '', ''],
      \ 'airline_b': ['#8cbf7a', '#142137', '', '', ''],
      \ 'airline_c': ['#bdbfc1', '#0a1321', '', '', ''],
      \ 'airline_x': ['#bdbfc1', '#0a1321', '', '', ''],
      \ 'airline_y': ['#8cbf7a', '#142137', '', '', ''],
      \ 'airline_z': ['#0d1829', '#8cbf7a', '', '', ''],
      \ 'airline_warning': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_error': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_term': ['#bdbfc1', '#0a1321', '', '', ''],
      \ }
let g:airline#themes#edgeweave#palette.terminal_modified = {
      \ 'airline_c': ['#d9a55b', '#0a1321', '', '', ''],
      \ 'airline_warning': ['#0d1829', '#d9a55b', '', '', ''],
      \ 'airline_error': ['#0d1829', '#f94f30', '', '', ''],
      \ 'airline_term': ['#bdbfc1', '#0a1321', '', '', ''],
      \ }

let g:airline#themes#edgeweave#palette.inactive = {
      \ 'airline_a': ['#56657d', '#0a1321', '', '', ''],
      \ 'airline_b': ['#56657d', '#0a1321', '', '', ''],
      \ 'airline_c': ['#56657d', '#0a1321', '', '', ''],
      \ 'airline_x': ['#56657d', '#0a1321', '', '', ''],
      \ 'airline_y': ['#56657d', '#0a1321', '', '', ''],
      \ 'airline_z': ['#56657d', '#0a1321', '', '', ''],
      \ 'airline_warning': ['#56657d', '#0a1321', '', '', ''],
      \ 'airline_error': ['#56657d', '#0a1321', '', '', ''],
      \ 'airline_term': ['#56657d', '#0a1321', '', '', ''],
      \ }
let g:airline#themes#edgeweave#palette.inactive_modified = {
      \ 'airline_c': ['#d9a55b', '#0a1321', '', '', ''],
      \ 'airline_warning': ['#56657d', '#0a1321', '', '', ''],
      \ 'airline_error': ['#56657d', '#0a1321', '', '', ''],
      \ 'airline_term': ['#56657d', '#0a1321', '', '', ''],
      \ }

let g:airline#themes#edgeweave#palette.accents = {
      \ 'red': ['#f94f30', '', '', '', ''],
      \ 'green': ['#8cbf7a', '', '', '', ''],
      \ 'blue': ['#27a6c7', '', '', '', ''],
      \ 'yellow': ['#d9a55b', '', '', '', ''],
      \ 'orange': ['#d9a55b', '', '', '', ''],
      \ 'purple': ['#9a92de', '', '', '', ''],
      \ }
