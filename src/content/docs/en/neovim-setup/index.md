---
title: A Guide to LaTeX Writing with Neovim
date: 2026-06-14
description: A complete LaTeX writing environment built on Neovim, covering LSP completion, compilation preview, and code snippets.
---
LaTeX writing often presents a dilemma: typing everything by hand is tedious, yet full IDEs feel bloated. This post documents the complete process of setting up a LaTeX writing environment in Neovim, covering compilation preview, code snippets, syntax completion, and more — all with the goal of making the writing experience as smooth as possible. The guide uses [lazy.nvim](https://lazy.folke.io/) as the plugin manager and is aimed at readers who already know how to use Neovim but haven't yet set up a LaTeX workflow.

> [!TIP]
> This guide uses lazy.nvim as the plugin manager. If you use a different plugin manager, you'll need to adjust the configuration code accordingly.

## Prerequisites
- [texlive](https://www.tug.org/texlive/): provides the TeX environment; `latexmk` is required later
- [neovim](https://neovim.io/): version 0.10 or later
- [zathura](https://pwmt.org/projects/zathura/): used as the PDF viewer
## Steps
### Configuring LSP + Completion Engine
I use the mainstream trio of `mason` + `mason-lspconfig` + `nvim-lspconfig` to manage LSP installation, configuration, and integration, with `blink.cmp` as the completion engine. Since this isn't the main focus of the article, I'll just share my configuration:

``` lua

return {
	{
		"mason-org/mason-lspconfig.nvim",
		opts = {
			ensure_installed = { "clangd", "lua_ls", "rust_analyzer", "pyright", "ruff", "texlab", "marksman", "gopls" },
		},
		dependencies = {
			{ "mason-org/mason.nvim", opts = {} },
			"neovim/nvim-lspconfig",
		},
	},
	{
		"saghen/blink.cmp",
		-- optional: provides snippets for the snippet source
		-- dependencies = { "rafamadriz/friendly-snippets" },

		-- use a release tag to download pre-built binaries
		version = "1.*",
		-- AND/OR build from source, requires nightly: https://rust-lang.github.io/rustup/concepts/channels.html#working-with-nightly-rust
		-- build = 'cargo build --release',
		-- If you use nix, you can build from source using latest nightly rust with:
		-- build = 'nix run .#build-plugin',

		---@module 'blink.cmp'
		---@type blink.cmp.Config
		opts = {
			-- 'default' (recommended) for mappings similar to built-in completions (C-y to accept)
			-- 'super-tab' for mappings similar to vscode (tab to accept)
			-- 'enter' for enter to accept
			-- 'none' for no mappings
			--
			-- All presets have the following mappings:
			-- C-space: Open menu or open docs if already open
			-- C-n/C-p or Up/Down: Select next/previous item
			-- C-e: Hide menu
			-- C-k: Toggle signature help (if signature.enabled = true)
			--
			-- See :h blink-cmp-config-keymap for defining your own keymap
			keymap = {
				preset = "default",
				["<Tab>"] = {
					function(cmp)
						local ls = require("luasnip")
						if ls.expandable() then
							cmp.cancel()
							vim.schedule(function()
								ls.expand()
							end)
							return true
						end
					end,
					"snippet_forward",
					"fallback",
				},
				["<CR>"] = { "accept", "fallback" },
				["<C-j>"] = { "show", "show_documentation", "hide_documentation" },
			},
			appearance = {
				-- 'mono' (default) for 'Nerd Font Mono' or 'normal' for 'Nerd Font'
				-- Adjusts spacing to ensure icons are aligned
				nerd_font_variant = "mono",
			},

			-- (Default) Only show the documentation popup when manually triggered
			completion = { documentation = { auto_show = true } },

			-- Default list of enabled providers defined so that you can extend it
			-- elsewhere in your config, without redefining it, due to `opts_extend`
			snippets = { preset = "luasnip" },
			sources = {
				default = { "lsp", "path", "snippets", "buffer" },
			},

			-- (Default) Rust fuzzy matcher for typo resistance and significantly better performance
			-- You may use a lua implementation instead by using `implementation = "lua"` or fallback to the lua implementation,
			-- when the Rust fuzzy matcher is not available, by using `implementation = "prefer_rust"`
			--
			-- See the fuzzy documentation for more information
			fuzzy = { implementation = "prefer_rust_with_warning" },
			signature = { enabled = true },
		},
		opts_extend = { "sources.default" },
	},
}
```
### VimTeX
[VimTeX](https://github.com/lervag/vimtex) provides rich text objects, syntax highlighting, environment detection, and compilation integration. Configuration:

``` lua

return {
    {
        "lervag/vimtex",
        lazy = false, 
        init = function()
            vim.g.vimtex_syntax_enabled = 1 -- Enable VimTeX syntax highlighting
            vim.g.vimtex_view_method = "zathura" -- Use Zathura as the PDF viewer
        end
    }
}
```

For specific features and usage, readers are encouraged to explore on their own. Here are a few features I use regularly:

1. **Auto-compilation**: Automatically compiles after saving. The default mapping is `<LocalLeader>ll` (LocalLeader defaults to `\`). After compilation, use `<LocalLeader>lv` for forward search to locate the corresponding PDF segment in Zathura. In Zathura, `Ctrl+Click` performs reverse search, jumping back to the corresponding line in the TeX source.
2. **Table of Contents**: `<LocalLeader>lt` opens a floating ToC window for quick navigation between sections, labels, references, and TODO items.
3. **Text Objects**: VimTeX provides rich text objects, such as `ie` to select environment content, `ae` to select an environment with its `\begin`/`\end` lines, `id` to select inline math (`$...$` or `\(...\)`), and `am` to select block-level math with its `\[...\]` delimiters.

![](edit-latex.gif)
### LuaSnip
[LuaSnip](https://github.com/L3MON4D3/LuaSnip) provides snippet completion, allowing common structures to be preset as snippets — significantly improving editing speed and experience. Configuration:

``` lua

return {
	{
		"L3MON4D3/LuaSnip",
		version = "v2.*", 
		build = "make install_jsregexp",
		config = function()
			local ls = require("luasnip")
			require("luasnip.loaders.from_vscode").lazy_load()
			require("luasnip.loaders.from_lua").load({ paths = "./LuaSnip" })
			require("luasnip").config.set_config({
				enable_autosnippets = true,
				store_selection_keys = "<Tab>",
			})
			vim.keymap.set({ "i", "s" }, "<C-f>", function()
				if ls.choice_active() then
					ls.change_choice(1)
				end
			end, { silent = true })
			vim.keymap.set({ "i", "s" }, "<C-b>", function()
				if ls.choice_active() then
					ls.change_choice(-1)
				end
			end, { silent = true })
			vim.keymap.set({ "i", "s" }, "<C-k>", function()
				if ls.expandable() then
					ls.expand()
				end
			end, { silent = true })
		end,
	},
}
```

When writing snippet files, the following convention is commonly used:

``` lua
local ls = require("luasnip")
local s = ls.snippet
local sn = ls.snippet_node
local t = ls.text_node
local i = ls.insert_node
local f = ls.function_node
local d = ls.dynamic_node
local fmt = require("luasnip.extras.fmt").fmt
local fmta = require("luasnip.extras.fmt").fmta
local rep = require("luasnip.extras").rep
```

I'll cover only a few examples of this plugin's configuration and usage. This barely scratches the surface, but should serve as a good starting point.

Let's begin with the simplest example — a snippet that expands `alpha` into `\alpha`:

```lua
s({ trig = "alpha" }, {
  t("\\alpha"),
})
```

In insert mode, typing `alpha` followed by the expand key (mapped to `<C-k>` earlier) inserts `\alpha`. The first argument to `s()` specifies the trigger conditions (here just `trig`), and the second is a list of nodes — just a single `text_node` (plain text) in this case.

1. Auto-expanding Snippets
![](luasnip-1.gif)

Once you've grasped the basics, let's look at how to make snippets smarter using VimTeX's API. The core requirement is: Greek letter completion should only trigger inside math environments, not in body text. Simply add:

``` lua
local tex_utils = {}
tex_utils.in_mathzone = function() -- math context detection
	return vim.fn["vimtex#syntax#in_mathzone"]() == 1
end
```

This allows us to use context-aware auto-expansion in subsequent configurations — so `;a` in body text won't misfire, but will auto-expand to `\alpha` only inside math environments:

```lua
	s({ trig = ";a", snippetType = "autosnippet", condition = tex_utils.in_mathzone }, {
		t("\\alpha"),
	}),
	s({ trig = ";b", snippetType = "autosnippet", condition = tex_utils.in_mathzone }, {
		t("\\beta"),
	}),
```

2. Dynamically Generated Snippets
![](luasnip-2.gif)

Using Lua, we can create dynamically generated snippets for even greater efficiency.

``` lua
local function make_table(_, parent)
	local rows = tonumber(parent.captures[1])
	local cols = tonumber(parent.captures[2])
	local nodes = {}
	local k = 1

	for r = 1, rows do
		for c = 1, cols do
			table.insert(nodes, i(k))
			k = k + 1
			if c ~= cols then
				table.insert(nodes, t(" & "))
			end
		end
		if r ~= rows then
			table.insert(nodes, t({ " \\\\", "\t\t" }))
		end
	end
	return sn(nil, nodes)
end

local function make_colspec(_, parent)
	local cols = tonumber(parent.captures[2])
	local nodes = {}
	for c = 1, cols do
		table.insert(nodes, t({ "X" }))
	end
	return sn(nil, nodes)
end
return {
	s(
		{ trig = "t(%d+)x(%d+)", hidden = true, regTrig = true, wordTrig = true, dscr = "Quick make a table" },
		fmta(
			[[
        \begin{table}[htbp]
            \centering
            \caption{<>}
            \begin{tblr}{
                colspec={<>},
                width=<>\linewidth,
                hlines,
            }
                <>
            \end{tblr}
        \end{table}
        ]],
			{
				i(1),
				d(2, make_colspec),
				i(3),
				d(4, make_table),
			}
		)
	),
}
```

3. Inline Calculator
![](luasnip-3.gif)

This leverages Lua's math library to implement a calculator. Due to `blink.cmp`'s completion mechanism, we need to prevent premature evaluation. The relevant code:

``` lua
local function eval_math(_, parent)
	-- Return placeholder during static/docstring resolution (blink.cmp resolve)
	-- without blocking. parent or parent.snippet may be nil.
	local in_buffer = pcall(function()
		return parent.snippet:extmarks_valid()
	end)
	if not in_buffer then
		return sn(nil, t(""))
	end

	-- Real expansion: prompt for input.
	local expr = vim.fn.input("expr: ")
	if expr == "" then
		return sn(nil, t(""))
	end
	local env = { math = math }
	for k, v in pairs(math) do env[k] = v end
	env.sqrt = function(n, x)
		if x then return x ^ (1 / n) end
		return math.sqrt(n)
	end
	local fn, err = load("return " .. expr, "eval_ctx", "t", env)
	if not fn then
		return sn(nil, t(err or "invalid"))
	end
	local ok, result = pcall(fn)
	if not ok then
		return sn(nil, t("error"))
	end
	return sn(nil, t(tostring(result)))
end

return {
	s(
		{ trig = "calc", desc = "calculate the expression" },
		fmta("<>", { d(1, eval_math) })
	),
}
```

## Summary
The above covers the core components of my LaTeX writing environment: texlab + blink.cmp for completion, VimTeX for compilation and preview, and LuaSnip for reducing repetitive work with snippets. Together, these three tools make daily writing essentially mouse-free. For more detailed tutorials, check the [reference](https://ejmastnak.com/tutorials/vim-latex/intro/) and thanks to the original [inspiration](https://castel.dev/post/lecture-notes-1/) for this article, as well as the contributors of the open-source projects mentioned above.
