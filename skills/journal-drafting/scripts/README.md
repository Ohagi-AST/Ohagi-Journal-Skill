# scripts/ — 图表视觉闭环 + Stata 渲染工具（阶段一）

> 目标：让写作系统**真正"看见"图表**（去锁→渲染成 PNG→亲眼看），并以**统一 house-style**
> 把真实回归渲染成**三线表 + 灰度图**，杜绝"九宫格冒充三线表""图表不统一"。
> house-style 实证依据见 [`RECON_图表发现.md`](RECON_图表发现.md)（扫 EER 真实表/图归纳）。
>
> ✅ 已接线进 `[2.5] 图表蓝图`：编排器按环境三选一渲染（Stata `.do` / Python `exhibit_render.py` / 退化 Markdown 模板），见 `../SKILL.md` 图表蓝图第 5 步。

## 文件
| 文件 | 作用 |
|---|---|
| `pdf_to_png.py` | PDF（含加密）→ PNG。去 owner-password + 高清栅格化，供视觉读图。 |
| `exhibit_render.py` | **Python 等价渲染器**（不依赖 Stata/LaTeX；表格渲染无第三方依赖，画图用 `matplotlib`）：`render_table` 三线表片段 / `render_coefplot` / `render_event_study`。house-style 与下面两个 `.do` 对齐。`--demo` 看产物。 |
| `exhibit_style.do` | 三线表渲染封装 `exhibit_table`（锁定 esttab house-style：booktabs/星号/SE/列号/跨列头）。 |
| `exhibit_figs.do` | 图标准：黑白 `s1mono` 主题 + `graph_export_exhibit`（固定尺寸导出）+ `exhibit_coefplot`（系数图）。 |
| `exhibit_map.py` | 跨论文抽「图表叙事结构」：图表清单 / 章节位置 / 正文交叉引用句 / 主-附切分。 |
| `exhibit_preamble.tex` | 最小 LaTeX 前导（booktabs+threeparttable+caption）与"图表盒子"用法示例。 |
| `exhibit_build_template.do` | 规范流程范例（真实回归→表+图），照抄改路径。 |
| `zh_glyph_check.py` | 日语稿「中文汉字残留」字形检测器（净化层·第1关）。 |
| `_smoke_test.do` | 冒烟测试（`sysuse auto`），产出 `_smoke_out/`。 |
| `RECON_图表发现.md` | EER 图表视觉 house-style 侦察报告。 |

## 环境（本机已验证）
- Python + **PyMuPDF**（`pip install pymupdf`）；画图另需 `matplotlib`。开发/测试可直接 `python -m pip install -r ../../../requirements-dev.txt`
- **StataMP 18** + `ssc install estout coefplot`
- LaTeX：`latexmk` + `pdflatex`（TeX Live/MiKTeX）

> ⚠️ **Bash 在 auto 权限模式会被分类器卡死**（已知故障）。跑命令前把权限模式切到
> **default**（Claude Code 里 Shift+Tab 循环 / `/config`），Bash 改逐条 Y/N 确认即可。

## 用法

### A. 把论文 PDF 渲染成 PNG（看图 / 学 house-style）
```bash
python pdf_to_png.py paper.pdf --pages 10-15 --dpi 180     # 加密 EER 也能去锁渲染
# 产物：_exhibit_images/<paper>/<paper>_pNNN.png
```

### B. 把真实回归渲染成三线表 + 灰度系数图
```bash
# 从 scripts/ 目录（Git Bash）
"/c/Application/Stata18/StataMP-64.exe" -b do _smoke_test.do   # 看 _smoke_test.log 里 r(0)
```
Stata 侧产出 `_smoke_out/table_smoke.tex`（完整 booktabs tabular）+ `fig_smoke.pdf`。
LaTeX 侧把表 `\input` 进 `table`+`threeparttable`（题注在上、表注在下），见 `exhibit_preamble.tex`。

### C. 渲染产物视觉自检（硬闸，杜绝九宫格）
```bash
cd _smoke_out
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex   # main.tex 见 _smoke_test 流程
python ../pdf_to_png.py main.pdf --out pngs --dpi 170           # → pngs/main/main_p001.png
# 然后用 Read 工具看这张 PNG，核：三线表？无竖线/九宫格？星号/SE/对齐/表注达标？
```

### D. 日语稿中文残留字形检查
```bash
python zh_glyph_check.py draft.txt
python zh_glyph_check.py draft.txt --fix
```
Windows 下优先传 UTF-8 文本文件路径；不同终端的 `echo ... | python zh_glyph_check.py -` 管道编码可能不稳定。需要在自动化里拦截残留时，加 `--fail-on-hit`。

## 铁律
- **三线表**：booktabs 顶/中/底线，**禁竖线/全框线/九宫格**。
- **渲染≠造数**：只格式化**真实 `eststo` 存储估计**，绝不手写系数/SE/N/p。
- 题注：**表在上、图在下**；显著性约定 `* p<0.10, ** p<0.05, *** p<0.01`（EER 实证）。

## 工作产物（可随时删/可 gitignore）
`_exhibit_images/`、`_smoke_out/` 为渲染中间物，非源码。
