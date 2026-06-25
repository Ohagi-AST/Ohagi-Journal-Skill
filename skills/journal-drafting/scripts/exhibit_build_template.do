*! exhibit_build_template.do — 规范流程范例：真实回归 → house-style 三线表 + 系数图
*! 阶段一工具（范例/模板，照抄改路径即可，不直接跑）。
*!
*! ⛔ 核心纪律：表/图里的每个数字都来自【真实 eststo 存储估计】。
*!    本脚本不写死任何系数；换成你的数据与设定，数字自动来自你的回归。
*!    列的顺序 = 叙事顺序（约束设定 → 逐步加控制/FE → 最丰富设定）。

clear all
set more off

* 0) 加载 house-style 工具（按你的实际路径）
do "exhibit_style.do"
do "exhibit_figs.do"

* 1) 数据（换成你的）
*    use "mydata.dta", clear

* 2) 真实回归，按"叙事弧"从约束到丰富逐列存储
*    eststo clear
*    eststo c1: reghdfe y treat,                absorb(id)            vce(cluster id)
*    eststo c2: reghdfe y treat x1 x2,           absorb(id)            vce(cluster id)
*    eststo c3: reghdfe y treat x1 x2,           absorb(id year)       vce(cluster id)
*    eststo c4: reghdfe y treat x1 x2 x3,        absorb(id year sector) vce(cluster id)

* 3) 主结果三线表（fragment）：
*    - depvar() 给跨列被解释变量表头
*    - indicate() 把 FE 折成 Yes/No 指示行（EER 风）
*    - statsline() 自定义底部统计量行
*    exhibit_table c1 c2 c3 c4 using "tables/tab_main.tex", ///
*        depvar("Log exports") ///
*        indicate("Unit FE = *.id" "Year FE = *.year" "Sector FE = *.sector") ///
*        statsline(`"stats(N r2_within, fmt(%9.0fc %9.3f) labels("Observations" "Within \(R^{2}\)"))"')

* 4) 主结果系数图（coefplot）：核心处理效应 + 95%CI
*    exhibit_coefplot c1 c2 c3 c4, keep(treat) title("Effect of treatment across specifications")
*    graph_export_exhibit "figures/fig_main"

* 5) LaTeX 端（见 exhibit_preamble.tex 用法）：
*    \input{tables/tab_main} 放进 \begin{table}\caption{...}\begin{threeparttable}...\begin{tablenotes}
*    题注在表上方、图题注在图下方；表注里写 样本/聚类/方法 + 固定显著性脚注 $EXHIBIT_SIGNOTE。

display as text "这是模板：取消注释、替换数据与设定后运行。"
