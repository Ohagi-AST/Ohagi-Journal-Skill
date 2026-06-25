#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exhibit_render.py — 无 Stata / 无 LaTeX 也能渲染 house-style 图表的 Python 等价工具。

对标 Stata 侧的 exhibit_style.do（三线表）+ exhibit_figs.do（灰度系数图/事件研究图），
让没有 StataMP 的用户也能跑通「图表蓝图 [2.5]」的渲染环节。house-style 与 .do 对齐：
  - 表：booktabs 三线表（\\toprule/\\midrule/\\bottomrule），禁竖线/九宫格；
        系数 3 位小数、SE 在下方括号、星号三级 0.10 / 0.05 / 0.01。
  - 图：s1mono 风格的黑白极简（灰度、无 chartjunk）；点估计 + 置信区间；
        固定画布、字号克制；矢量 PDF 导出（投顶刊首选）。

⛔ 铁律（接母版规则 5/6）：本工具只是【真实估计】的格式化器，绝不编造/手写
   系数、标准误、N、p。所有数字必须来自用户真实回归的输出（由调用方传入）。

依赖：仅 pandas + matplotlib（不依赖 Stata、不依赖 LaTeX 引擎）。
  - render_table 产出的是【纯文本 LaTeX 片段】，本身不需要 LaTeX 即可生成；
    要编译成 PDF 时才需 booktabs 宏包（见 exhibit_preamble.tex）。
  - render_coefplot / render_event_study 用 matplotlib 直接出 PDF/PNG，全程不碰 LaTeX。

可作模块 import，也可命令行跑自带 demo：
    python3 exhibit_render.py --demo --out _exhibit_py_out
"""
from __future__ import annotations
import argparse
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

# 与 exhibit_style.do 完全一致的显著性约定（EER 实证）。
SIG_LEVELS = ((0.01, "***"), (0.05, "**"), (0.10, "*"))
SIGNOTE = (r"Standard errors in parentheses. "
           r"* \(p<0.10\), ** \(p<0.05\), *** \(p<0.01\).")


def stars(p):
    """p 值 → 星号串（0.10 / 0.05 / 0.01 三级），与 exhibit_style.do 对齐。"""
    if p is None:
        return ""
    for thr, mark in SIG_LEVELS:
        if p < thr:
            return mark
    return ""


def _fmt(x, nd=3):
    if x is None:
        return ""
    return f"{x:.{nd}f}"


def render_table(models, using=None, depvar=None, coef_order=None,
                 stats=("N",), nd=3):
    r"""把多列回归结果渲染成 booktabs 三线表 LaTeX 片段（fragment）。

    参数
    ----
    models : list[dict]
        每个 dict 是一列（一个模型），形如：
            {
              "title": "(1)",                # 列号/列标题；缺省按 1..k 自动编号
              "coefs": {                     # 变量名 -> (coef, se[, p])
                  "Treat": (0.123, 0.045, 0.006),
                  "logGDP": (-0.210, 0.090),  # 不给 p 则不打星
              },
              "stats": {"N": 1200, "R2": 0.34},  # 统计量行（可选）
            }
        ⛔ 这些数字必须来自真实回归（eststo / statsmodels / 手算无关），本函数不产生任何估计。
    using : str | None
        给定则把 .tex 片段写到该路径；否则只返回字符串。
    depvar : str | None
        给定则在列号上方加一行跨列「被解释变量」表头（\multicolumn + \cmidrule），对齐 .do 的 mgroups。
    coef_order : list[str] | None
        变量行顺序；缺省取各列并集、按首次出现排序。
    stats : tuple[str, ...]
        底部统计量行要打印哪些键（如 ("N", "R2")），缺失的列留空。
    nd : int
        系数/SE 小数位（默认 3，与 .do 的 b(%9.3f) se(%9.3f) 一致）。

    返回
    ----
    str —— 完整 \begin{tabular}…\end{tabular} 片段（含 toprule/midrule/bottomrule）。
            题注（表上）与表注（表下，含 SIGNOTE）交给 LaTeX 端 threeparttable，见 exhibit_preamble.tex。
    """
    k = len(models)
    if k == 0:
        raise ValueError("render_table: models 不能为空")

    titles = [m.get("title") or f"({i})" for i, m in enumerate(models, 1)]

    if coef_order is None:
        coef_order = []
        for m in models:
            for name in m.get("coefs", {}):
                if name not in coef_order:
                    coef_order.append(name)

    stat_labels = {"N": "Observations", "R2": r"\(R^{2}\)", "r2": r"\(R^{2}\)",
                   "r2_a": r"Adj. \(R^{2}\)", "F": r"\(F\)"}

    col_spec = "l" + "c" * k
    lines = [r"\begin{tabular}{" + col_spec + "}", r"\toprule"]

    # 可选跨列被解释变量表头
    if depvar:
        lines.append(f"& \\multicolumn{{{k}}}{{c}}{{{depvar}}} \\\\")
        lines.append(f"\\cmidrule(lr){{2-{k + 1}}}")

    # 列号行
    lines.append(" & " + " & ".join(titles) + r" \\")
    lines.append(r"\midrule")

    # 系数行（系数+星 在上，(SE) 在下）
    for name in coef_order:
        coef_cells, se_cells = [], []
        for m in models:
            entry = m.get("coefs", {}).get(name)
            if entry is None:
                coef_cells.append("")
                se_cells.append("")
                continue
            b = entry[0]
            se = entry[1] if len(entry) > 1 else None
            p = entry[2] if len(entry) > 2 else None
            coef_cells.append(f"{_fmt(b, nd)}{stars(p)}")
            se_cells.append(f"({_fmt(se, nd)})" if se is not None else "")
        lines.append(f"{name} & " + " & ".join(coef_cells) + r" \\")
        lines.append(" & " + " & ".join(se_cells) + r" \\")

    # 统计量行
    if stats:
        lines.append(r"\midrule")
        for key in stats:
            label = stat_labels.get(key, key)
            cells = []
            for m in models:
                v = m.get("stats", {}).get(key)
                if v is None:
                    cells.append("")
                elif key in ("N", "n"):
                    cells.append(f"{int(v):,}")  # 千分位，对齐 .do 的 %9.0fc
                else:
                    cells.append(_fmt(v, nd))
            lines.append(f"{label} & " + " & ".join(cells) + r" \\")

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    out = "\n".join(lines) + "\n"

    if using:
        os.makedirs(os.path.dirname(os.path.abspath(using)), exist_ok=True)
        with open(using, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"[OK] 三线表片段 → {os.path.abspath(using)}")
    return out


def _style_axes(ax):
    """s1mono 观感：去掉上/右边框、黑白、克制字号。"""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8, color="black")
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color("black")


def _new_fig(width=4.2, height=3.0):
    try:
        import matplotlib
    except ImportError:
        sys.exit("[!] 画图需要 matplotlib：pip install matplotlib"
                 "（只渲染表格 render_table 不需要它）。")
    matplotlib.use("Agg")  # 无显示环境也能出图
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(width, height))
    return plt, fig, ax


def _save(plt, fig, using, dpi=200):
    fig.tight_layout()
    os.makedirs(os.path.dirname(os.path.abspath(using)), exist_ok=True)
    fig.savefig(using, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] 图 → {os.path.abspath(using)}")


def render_coefplot(estimates, using, ci=None, level=95, title="",
                    xlabel="Estimate", sort=False, width=4.2, height=3.0):
    r"""灰度系数图/毛毛虫图（对标 exhibit_figs.do 的 exhibit_coefplot）。

    estimates : list[tuple]
        [(label, coef, lo, hi), ...] 或 [(label, coef, se), ...]（配合 ci="se"）。
    using : str
        输出路径（.pdf 矢量优先；.png 亦可）。
    ci : None | "se"
        None：estimates 已给 (label, coef, lo, hi)。
        "se"：estimates 给 (label, coef, se)，按正态近似 coef ± z*se 算区间。
    level : int
        置信水平（ci="se" 时用），默认 95。
    """
    import math
    rows = []
    z = {90: 1.645, 95: 1.96, 99: 2.576}.get(level, 1.96)
    for e in estimates:
        if ci == "se":
            label, coef, se = e
            lo, hi = coef - z * se, coef + z * se
        else:
            label, coef, lo, hi = e
        rows.append((label, coef, lo, hi))
    if sort:
        rows.sort(key=lambda r: r[1])

    plt, fig, ax = _new_fig(width, height)
    ys = list(range(len(rows)))
    for y, (label, coef, lo, hi) in zip(ys, rows):
        ax.plot([lo, hi], [y, y], color="black", linewidth=1.0)  # CI 横线
        ax.plot([coef], [y], marker="o", color="black", markersize=4)  # 点估计
    ax.axvline(0, linestyle="--", color="0.5", linewidth=0.8)  # 0 参考线（gs8 灰）
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows])
    ax.set_xlabel(f"{xlabel} ({level}% CI)", fontsize=9)
    if title:
        ax.set_title(title, fontsize=10)
    _style_axes(ax)
    _save(plt, fig, using)
    return using


def render_event_study(estimates, using, ci=None, level=95, title="",
                       xlabel="Event time", ylabel="Estimate", ref_period=None,
                       width=4.6, height=3.0):
    r"""灰度事件研究图：横轴=事件时点，纵轴=点估计 + 置信区间，0 处一条参考线。

    estimates : list[tuple]
        [(t, coef, lo, hi), ...] 或 [(t, coef, se), ...]（配合 ci="se"）；t 为相对事件时点（可负）。
    ref_period : int | None
        基期（通常 -1）：若该时点不在 estimates 里，自动补一个 (ref_period, 0, 0, 0) 归一化点。
    """
    rows = []
    z = {90: 1.645, 95: 1.96, 99: 2.576}.get(level, 1.96)
    for e in estimates:
        if ci == "se":
            t, coef, se = e
            lo, hi = coef - z * se, coef + z * se
        else:
            t, coef, lo, hi = e
        rows.append((t, coef, lo, hi))
    if ref_period is not None and all(r[0] != ref_period for r in rows):
        rows.append((ref_period, 0.0, 0.0, 0.0))
    rows.sort(key=lambda r: r[0])

    ts = [r[0] for r in rows]
    coefs = [r[1] for r in rows]
    los = [r[2] for r in rows]
    his = [r[3] for r in rows]

    plt, fig, ax = _new_fig(width, height)
    ax.errorbar(ts, coefs,
                yerr=[[c - lo for c, lo in zip(coefs, los)],
                      [hi - c for c, hi in zip(coefs, his)]],
                fmt="o", color="black", ecolor="black",
                elinewidth=1.0, capsize=2, markersize=4)
    ax.axhline(0, linestyle="--", color="0.5", linewidth=0.8)
    if ref_period is not None:
        ax.axvline(ref_period, linestyle=":", color="0.7", linewidth=0.8)
    ax.set_xlabel(f"{xlabel} ({level}% CI)", fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    if title:
        ax.set_title(title, fontsize=10)
    _style_axes(ax)
    _save(plt, fig, using)
    return using


def _demo(out_dir):
    """自带演示：用编造的占位数字仅为验证渲染管线（⚠️ 真实使用须换成真回归输出）。"""
    os.makedirs(out_dir, exist_ok=True)
    models = [
        {"title": "(1)", "coefs": {"Treat": (0.083, 0.041, 0.043)},
         "stats": {"N": 1240, "R2": 0.21}},
        {"title": "(2)", "coefs": {"Treat": (0.075, 0.038, 0.048),
                                   "logGDP": (-0.190, 0.071, 0.008)},
         "stats": {"N": 1240, "R2": 0.34}},
    ]
    tex = render_table(models, using=os.path.join(out_dir, "table_demo.tex"),
                       depvar="log exports", stats=("N", "R2"))
    print("\n--- table_demo.tex ---\n" + tex)
    print("表注（放进 LaTeX tablenotes）：" + SIGNOTE + "\n")

    render_coefplot(
        [("Treat", 0.075, 0.038), ("logGDP", -0.190, 0.071), ("Post", 0.012, 0.050)],
        using=os.path.join(out_dir, "coefplot_demo.pdf"), ci="se", title="Demo coefficients")

    render_event_study(
        [(-3, 0.01, 0.03), (-2, -0.02, 0.03), (0, 0.06, 0.03),
         (1, 0.09, 0.035), (2, 0.11, 0.04)],
        using=os.path.join(out_dir, "event_demo.pdf"), ci="se", ref_period=-1,
        title="Demo event study")
    print(f"\n演示产物在 {os.path.abspath(out_dir)}/ —— 用 Read 工具看 PDF/PNG 做视觉自检。")


def main():
    ap = argparse.ArgumentParser(description="house-style 图表渲染（Python 等价，无需 Stata/LaTeX）")
    ap.add_argument("--demo", action="store_true", help="跑自带演示，验证渲染管线可用")
    ap.add_argument("--out", default="_exhibit_py_out", help="演示产物输出目录")
    args = ap.parse_args()
    if args.demo:
        _demo(args.out)
    else:
        ap.print_help()
        print("\n提示：本工具主要作模块 import 用（render_table / render_coefplot / render_event_study）。"
              "\n      先跑 --demo 看产物长相。⛔ 真实使用时务必传入真实回归数字，不要用 demo 占位值。")


if __name__ == "__main__":
    main()
