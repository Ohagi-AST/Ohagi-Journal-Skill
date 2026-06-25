*! _smoke_test.do — 渲染工具链冒烟测试：真实回归 → 三线表 fragment + 系数图 PDF
*! 跑法（Git Bash，从 scripts/ 目录）：
*!   "/c/Application/Stata18/StataMP-64.exe" -b do _smoke_test.do
*!   然后读 _smoke_test.log 看 r(0)；产物在 _smoke_out/
*! 用 sysuse auto（Stata 自带真实数据）演示，不编造任何数字。

clear all
set more off
cap mkdir _smoke_out

* 依赖（缺则装）
cap which esttab
if _rc ssc install estout, replace
cap which coefplot
if _rc ssc install coefplot, replace

* house-style 工具
do exhibit_style.do
do exhibit_figs.do

* —— 真实回归：1978 汽车数据，价格的决定因素，逐列加控制（叙事弧）——
sysuse auto, clear
eststo clear
eststo m1: regress price mpg
eststo m2: regress price mpg weight
eststo m3: regress price mpg weight i.foreign

* 三线表 fragment（booktabs）
exhibit_table m1 m2 m3 using "_smoke_out/table_smoke.tex", ///
    depvar("Price (USD)") ///
    statsline(`"stats(N r2, fmt(%9.0fc %9.3f) labels("Observations" "\(R^{2}\)"))"')

* 系数图：三设定下 mpg 的系数 + 95%CI
exhibit_coefplot m1 m2 m3, keep(mpg) title("Coefficient on mpg across specs")
graph_export_exhibit "_smoke_out/fig_smoke"

di as result "SMOKE DONE -> _smoke_out/table_smoke.tex + _smoke_out/fig_smoke.pdf"
