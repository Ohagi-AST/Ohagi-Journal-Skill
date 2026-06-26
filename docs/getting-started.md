# 快速开始（Getting Started）

最短路径：装好 skill → 把下面的示例 prompt 改成你自己的情况 → 发给 agent。

## 1. 安装

见根 [`README.md`](../README.md) 的「怎么用 → 安装三个 skill」。装完 `journal-drafting`（原创编排器）即可起草；`vendor/` 下的 `reference-checker` 与 `journal-adapt` 在流程中按需被调用。

## 2. 一个可直接改用的示例 prompt

把方括号里的内容换成你自己的，复制给 agent：

```
我有一篇论文想写。研究已经做完了，有 [Stata do 文件和数据 / 已整理好的回归结果]。
目标期刊是 [Journal of Environmental Economics and Management]。
请按 journal-drafting 流程走，帮我起草。先从 Phase 0 开始。
```

agent 会：

1. 先判断**档位**（期刊投稿 / 学位论文），不确定会问你一句；
2. 带你逐项填**第 0 层 SPEC**（目标刊、层级现实性、结构母本 3–5 篇——三个硬闸 ⛔）；
3. 可选：调 `journal-adapt` 从目标刊真论文萃取写作文化、调文献宽度扩展补先行研究；
4. 搭骨架 → 进**图表蓝图**（结果型论文）→ 一节一停地逐节写，每节跑《单节自查》；
5. 齐稿后跑三道终检：总闸 → `reference-checker` 引用穷尽核验 → 审稿人预演。

> 全程节奏是「问 → 等 → 执行」，**一次只推进一步**。你不喊「连跑」，它做完一步就停下报进度。

## 3. 只想整理已有日文稿？

不需要从头起草、手里已有日文草稿时，直接说：

```
帮我整理这段日语 / 修改日语 / 把这段日文改地道：
[贴入日文段落]
```

会走**日语优化快速入口**，跳过起草全流程，直奔净化层（清中文打底残留）+ 文体层（投稿轨 / 修論轨）。

Windows 下做字形检查时，优先把文本保存成 UTF-8 文件后运行 `python skills/journal-drafting/scripts/zh_glyph_check.py draft.txt`；不同终端的 `echo ... | python ...` 管道编码不一定稳定。

## 4. 想渲染图表但没装 Stata？

图表蓝图的渲染环节**按环境三选一**（见 [`SKILL.md`](../skills/journal-drafting/SKILL.md) 图表蓝图第 5 步）：

- 有 **Stata** → `scripts/exhibit_style.do` + `scripts/exhibit_figs.do`；
- 无 Stata、有 **Python** → `scripts/exhibit_render.py`（表格渲染不需要第三方库；画图需 `matplotlib`，`python exhibit_render.py --demo` 先看产物）；
- 两者都没有 → 退化为三线表 Markdown 模板手填 + 视觉自检清单。

## 下一步

- 想了解整体设计 → [`overview.md`](overview.md)
- 想知道每一步怎么和 agent 配合 → [`interaction-guide.md`](interaction-guide.md)
- 想看通用硬规则在管什么 → [`reference/rules-overview.md`](reference/rules-overview.md)
- 想把自己的领域写作惯例加进来 → [`reference/field-templates/README.md`](reference/field-templates/README.md)
