# 体系结构概览（Overview）

这是一套面向**「研究已完成 → 开始把成果写成正式论文正文」**的写作框架。核心场景是**实证经济学**：英文期刊稿、学位论文正文、图表叙事、日文投稿/修論整理。规则也可迁移到相近社会科学论文，但默认假设是“结果和识别已经基本完成，下一步是成稿”。

设计思路来自 agent harness：*Rules-as-spec（规则即规范）＋ Verification-loop（验证闭环）＋ Memory（记忆防漂移）*。在本项目里，它们分别落成「最小启动闸 + 完整 SPEC」/ 单节与总闸 / 成稿决策日志。

## 四个入口

| 入口 | 目标 | 主轴 |
|---|---|---|
| 英文期刊成稿 | 把已完成实证研究写成英文期刊论文 | 最小启动闸 → 完整 SPEC → 骨架 → 图表蓝图 → 逐节写 → 投稿前终检 |
| 学位论文正文 | 把研究写成修士/博士论文或毕业论文正文 | 学校规程 → 章结构完整性 → 材料充分性 → 答辩委员视角预演 |
| 已有日文稿整理 | 对已有日文草稿去中文味、修学术文体 | 日语轨确认 → 字形/词汇/表达净化 → 投稿轨/修論轨文体 |
| 图表蓝图/图表规范 | 先整理结果图表、主附放置和叙事弧 | exhibit 清单 → 头牌图表 → house-style → write-to-exhibit |

入口细节见 [`entrypoints.md`](entrypoints.md)；可复制 prompt 见 [`getting-started.md`](getting-started.md)。

## 两层结构

1. **母版规则书 + 风格层**（`skills/journal-drafting/template-master-framework.md` 及其 `references/`）——原创。一份跨论文复用的规则书：每开一篇新论文先过最小启动闸，正式正文前补齐完整 SPEC；通用硬规则 1–9 稳定复用。
2. **三个可调用的 skill**——一个原创编排器（`journal-drafting`，自带上面的母版）+ 两个第三方 MIT 工具（`vendor/reference-checker`、`vendor/journal-adapt`），把流程串起来。

## 三条设计哲学（硬约束）

- **最小启动可以轻，正式正文必须过完整 SPEC**。不准备好边界，不动笔写正文。
- **结论的语气 ≤ 识别的强度**。关联/描述性设计不能偷写成因果。
- **绝不编造引用 / 数据 / 新规性证据**。拿不准就标【待核】或问用户。

## 组件分工

| 组件 | 角色 | 关键产物 |
|---|---|---|
| `skills/journal-drafting/SKILL.md` | 编排器薄壳：入口路由 + 交互节奏 + 流程串联 | 进度面板、逐步推进 |
| `skills/journal-drafting/template-master-framework.md` | 母版：最小启动闸 + 完整 SPEC + 硬规则 1–9 + 三道验证闸 | 本篇规则卡、验证清单 |
| `skills/journal-drafting/references/en-*` | 英文/实证写作展开层：风格、文献宽度、纯净度、领域约定、图表叙事 | 逐节按需加载 |
| `skills/journal-drafting/references/ja/*` | 日语优化两层：净化层 + 投稿/修論文体层 | 日语轨专用 |
| `skills/journal-drafting/scripts/` | 图表渲染、视觉读图、字形检测 | 渲染≠造数 |
| `skills/vendor/reference-checker` | 投稿前参考文献穷尽核验 | 清空【待核】、分级 |
| `skills/vendor/journal-adapt` | 从目标刊语料萃取写作文化、生成动态写作 skill | `dynamic_writing_skill.md` |

## 一页式流程卡片

| 阶段 | 目的 | 成本 | 产出 |
|---|---|---|---|
| 最小启动闸 | 判断入口和材料状态 | 低 | 可启动/需补材料判断 |
| 完整 SPEC | 锁定正式写作边界 | 中 | 本篇规则卡 |
| 文献宽度扩展 | 补先行研究宽度 | 高，可选 | 按簇候选文献清单 |
| 动态写作层 | 学目标刊写作文化 | 高，可选 | 动态写作 skill |
| 骨架 | 定章节顺序 | 中 | 每节做什么、得什么 |
| 图表蓝图 | 让图表承载论点 | 中 | exhibit 清单、叙事弧、主附放置 |
| 逐节写 | 生成正文并自查 | 中 | 正文草稿 + warnings |
| 总闸/核验/预演 | 定稿前查错 | 中 | 修改优先级清单 |

## 档位原则

期刊投稿档全配置跑；学位论文档不是“降级期刊稿”，而是独立路径：学校规程优先、章结构完整性优先、材料充分性优先、答辩委员视角优先。通用硬规则仍保留：主张强度、引用诚信、防漂移、图表先行。

## 完整流程细节

权威流程定义在编排器 [`SKILL.md`](../skills/journal-drafting/SKILL.md)；规则细节在 [`template-master-framework.md`](../skills/journal-drafting/template-master-framework.md)。本文件只做鸟瞰。
