*! exhibit_figs.do — EER house-style 图标准（黑白极简 + coefplot 系数图模板）
*! 阶段一工具。规格来自 RECON_图表发现.md：EER 图为灰度/黑白、极简、无 chartjunk，
*!   主力图型=系数/毛毛虫图（点估计+置信区间，常按估计值排序或分面）、核密度、choropleth。
*!
*! ⛔ 同样铁律：图里画的是【真实估计/真实数据】，不编造点位与区间。
*! 依赖：ssc install coefplot（系数图）。

// —— 全文统一图风格 ——
// s1mono 为 Stata 内置黑白主题（无需外部 scheme 包），契合 EER 黑白印刷观感。
set scheme s1mono

// 统一导出：矢量 PDF（投顶刊首选）。固定画布宽高，字号克制。
//   用法：先画图，再 graph_export_exhibit "fig3"
cap program drop graph_export_exhibit
program define graph_export_exhibit
    syntax anything(name=stub) [, Width(real 4.2) Height(real 3.0)]
    // 去掉调用时可能带进来的引号（anything 不剥引号，否则文件名非法 r(198)）
    local stub = subinstr(`"`stub'"', `"""', "", .)
    graph display, xsize(`width') ysize(`height')
    graph export "`stub'.pdf", replace
    // 需要位图预览/或期刊要 EPS 时再加：
    // graph export "`stub'.eps", replace
end

// —— 系数图/毛毛虫图模板（coefplot）——
// 例：把多个 eststo 估计画成"按系数排序 + 95%CI"的横向毛毛虫图。
//   先 eststo m1 ...；再 exhibit_coefplot m1, keep(treat) sortby
cap program drop exhibit_coefplot
program define exhibit_coefplot
    syntax anything(name=models) [, Keep(string) Level(integer 95) TITLE(string) ]
    cap which coefplot
    if _rc {
        di as error "需要 coefplot：ssc install coefplot"
        exit 198
    }
    local keepopt
    if "`keep'"!="" local keepopt keep(`keep')
    coefplot `models', `keepopt' ///
        vertical levels(`level') ///
        yline(0, lpattern(dash) lcolor(gs8)) ///
        msymbol(O) mcolor(black) ciopts(lcolor(black)) ///
        title("`title'", size(medium)) ///
        ytitle("Estimate (95% CI)", size(small)) ///
        legend(off)
end

display as text "exhibit_figs.do loaded: s1mono 黑白主题 + graph_export_exhibit + exhibit_coefplot。"
