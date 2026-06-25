*! exhibit_style.do — EER house-style 三线表渲染封装（基于 esttab/estout）
*! 阶段一工具。house-style 规格来自 RECON_图表发现.md 的 EER 实证归纳。
*!
*! 为什么要它：全文所有回归表走同一个 exhibit_table 命令 → 天然统一，
*!   杜绝"每张表各写各的"导致的不统一；booktabs 保证三线表、禁九宫格。
*!
*! ⛔ 铁律（接母版规则5/6）：本工具只是【真实 eststo 存储估计】的格式化器，
*!   绝不手写/编造系数、标准误、N、p。数字一律来自用户真实回归的 eststo。
*!
*! 依赖：ssc install estout
*! 用法：见 exhibit_build_template.do / _smoke_test.do
*!   exhibit_table m1 m2 m3 using "tabX.tex", depvar("log exports") ///
*!       statsline(`"stats(N r2, fmt(%9.0fc %9.3f) labels("Observations" "\(R^{2}\)"))"') ///
*!       [ indicate("Year FE = *.year") nonotes 等 esttab 透传选项 ]
*!   产出：booktabs 三线表【fragment】(.tex)，由 LaTeX 端 \input（题注+表注见 exhibit_preamble.tex 用法）。

cap program drop exhibit_table
program define exhibit_table
    // anything = 一串已 eststo 存储的模型名；using = 输出 .tex 片段
    syntax anything using/ , [ DEPvar(string) STATSline(string) * ]

    // —— 锁定的 house-style（实证自 EER）——
    //  booktabs 三线 / 系数3位小数 / SE在下方括号 / 星号三级 0.10·0.05·0.01
    //  label 用变量标签 / nomtitles(靠 mgroups 给跨列被解释变量头) / 默认(1)(2)列号
    //  不用 fragment：让 esttab 自带 \begin{tabular}+\toprule/\midrule/\bottomrule，
    //  LaTeX 端只 \input 这张完整 tabular（放进 table+threeparttable 加题注/表注）。
    //  nonotes：表注交给 LaTeX threeparttable 端（避免在表内拼脚注）。
    local k : word count `anything'

    // 可选：跨列"被解释变量"表头（EER 常见），自动按列数张成 \multicolumn + \cmidrule
    local mg ""
    if `"`depvar'"' != "" {
        local pat 1
        forvalues j = 2/`k' {
            local pat `pat' 0
        }
        local mg mgroups("`depvar'", pattern(`pat') ///
            prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}))
    }

    // 默认统计量行：仅 Observations（千分位）。需要更多由调用方用 statsline() 覆盖。
    if `"`statsline'"' == "" {
        local statsline stats(N, fmt(%9.0fc) labels("Observations"))
    }

    esttab `anything' using "`using'", replace ///
        booktabs ///
        b(%9.3f) se(%9.3f) ///
        star(* 0.10 ** 0.05 *** 0.01) ///
        label nomtitles nonotes collabels(none) ///
        `mg' `statsline' `options'
end

// house-style 的固定显著性脚注（常量文本、非数字，放进 LaTeX tablenotes 用）
global EXHIBIT_SIGNOTE "Standard errors in parentheses. * \(p<0.10\), ** \(p<0.05\), *** \(p<0.01\)."

display as text "exhibit_style.do loaded: 用 exhibit_table 渲染三线表（fragment）。"
