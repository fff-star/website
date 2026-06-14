---
title: 基于Neovim的LaTeX配置指北
date: 2026-06-14
description: 基于 Neovim 搭建的 LaTeX 写作环境，从 LSP 补全、编译预览到代码片段全覆盖。
---
LaTeX 写作常常陷入两难：纯手打效率太低，IDE 又太过臃肿。本文记录笔者在 Neovim 中搭建 LaTeX 写作环境的完整过程，涵盖编译预览、代码片段、语法补全等环节，目标是让写作体验足够顺手。全文以 [lazy.nvim](https://lazy.folke.io/) 为插件管理器，适合已经会用 Neovim 但还没搭好 LaTeX 工作流的读者。

> [!TIP]
> 使用lazy.nvim作为插件管理器，如使用其他插件管理器，需要适当修改配置代码

## 准备工作
- [texlive](https://www.tug.org/texlive/)：完成环境配置，后续依赖`latexmk`
- [neovim](https://neovim.io/)：要求版本大于0.10
- [zathura](https://pwmt.org/projects/zathura/)：作为 PDF 查看器
## 步骤
### 配置 LSP + 补全引擎
笔者使用的是最主流的`mason+mason-lspconfig+nvim-lspconfig`三个插件来管理 LSP 的下载、配置、接入；补全引擎为`blink.cmp`。由于这个部分不是本文重点，仅仅放出笔者的配置：
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
[VimTeX](https://github.com/lervag/vimtex) 提供了丰富的文本对象、高亮、环境检测和编译集成等功能。配置代码如下：
``` lua

return {
    {
        "lervag/vimtex",
        lazy = false, 
        init = function()
            vim.g.vimtex_syntax_enabled = 1 -- 使用vimtex提供的高亮
            vim.g.vimtex_view_method = "zathura" -- 使用zathura打开pdf
        end
    }
}
```

具体的功能和用法，读者可以自行研究，下面介绍几例笔者常用的功能：

1. **开启自动编译**：保存文件后自动编译，默认映射为 `<LocalLeader>ll`（LocalLeader 默认为 `\`）；编译完成后用 `<LocalLeader>lv` 正向搜索，在 Zathura 中定位到光标所在位置对应的 PDF 片段；在 Zathura 中按 `Ctrl+Click` 可以反向搜索，跳回 tex 源码对应行。
2. **显示目录**：`<LocalLeader>lt` 打开浮动目录窗口，可以快速跳转到各个 section、label、引用和 TODO 项。
3. **文本对象**：VimTeX 提供了丰富的 text object，比如 `ie` 选中环境内容、`ae` 选中环境及其 `\begin`/`\end` 行、`id` 选中 `$...$` 或 `\(...\)` 内联公式内容、`am` 选中块级公式及其 `\[...\]` 边界。
![](edit-latex.gif)
### LuaSnip
[LuaSnip](https://github.com/L3MON4D3/LuaSnip) 提供代码片段补全功能，将常见结构预设为片段，能显著提高编辑速度和体验。配置代码如下：
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
在编写 snippet 文件时，通常会做如下的约定：
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
关于这个插件的具体配置和使用，笔者只介绍几例，挂一漏万，权当是抛砖引玉。
1. 重复的代码片段 
![](luasnip-1.gif)
这个部分是这类插件的基本功能，唯一值得介绍的点是 VimTeX 提供的 API 可以方便地在这里使用，只需要：
``` lua
local tex_utils = {}
tex_utils.in_mathzone = function() -- math context detection
	return vim.fn["vimtex#syntax#in_mathzone"]() == 1
end
```
就可以在后续的配置中使用这个环境来让一些代码片段自动展开——这样 `;a` 在正文中不会误触发，只在公式环境内自动展开为 `\alpha`：
```lua
	s({ trig = ";a", snippetType = "autosnippet", condition = tex_utils.in_mathzone }, {
		t("\\alpha"),
	}),
	s({ trig = ";b", snippetType = "autosnippet", condition = tex_utils.in_mathzone }, {
		t("\\beta"),
	}),
```
2. 动态生成片段
![](luasnip-2.gif)
利用 Lua 我们可以实现动态生成的代码片段，提升效率。
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
3. 实现计算器
![](luasnip-3.gif)
同样是利用 Lua 的数学库实现的计算功能，需要注意的是由于`blink.cmp`的补全机制，需要阻止提前运行，涉及的代码如下：
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

## 总结
以上是笔者 LaTeX 写作环境的核心组件：texlab + blink.cmp 提供补全，VimTeX 负责编译预览，LuaSnip 用片段削减重复劳动。三者配合，日常写作基本脱离鼠标。具体教程推荐 [参考](https://ejmastnak.com/tutorials/vim-latex/intro/)，感谢最初启发本文的 [分享](https://castel.dev/post/lecture-notes-1/)，以及上述开源项目的贡献者。
