# 体系结构概览（Overview）

这是一套面向**「研究已完成 → 正式成稿、局部改写与投稿准备」**的写作框架。核心场景是经济学论文：英文期刊稿、学位论文、英文局部任务、投稿/R&R、图表叙事和日文投稿/修論整理。默认假设是研究事实已由作者提供；skill 不替作者生成证据。

设计思路来自 agent harness：*Rules-as-spec（规则即规范）＋ Verification-loop（验证闭环）＋ Memory（记忆防漂移）*。在本项目里，它们分别落成「最小启动闸 + 完整 SPEC」/ 单节与总闸 / 成稿决策日志。

## 两层路由

| 任务层级 | 快捷路径 | 运行方式 |
|---|---|---|
| **完整成稿主流程** | A 英文期刊成稿；B 学位论文正文 | 最小启动闸 → 完整 SPEC → 骨架/图表 → 逐节写 → 终检 |
| **局部/专项任务** | C 日文稿整理；D 图表蓝图；E 英文局部；F 投稿/R&R | 轻量任务卡 → 对应模块 → 校验；需要整篇重构时确认后升级 A/B |

图表蓝图是结果型完整论文的标准阶段，同时保留“只做 exhibit plan”的直接快捷路由；它是模块，不是与期刊/学位平级的交付目标。

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
| `references/en-section-playbooks.md` | 标题、摘要、引言、模型、数据、结果、结论、附录 | 分节默认结构 |
| `references/en-identification-strategies.md` | RCT/DiD/IV/RDD/SCM/结构/描述等方法卡 | estimand 与主张上限路由 |
| `references/en-empirical-standards.md` | 推断、多重检验、PAP、复现与披露 | 现代实证审计 |
| `references/en-submission-workflows.md` | 快审/深审、缩稿、R&R | 投稿任务卡与输出格式 |
| `skills/journal-drafting/references/ja/*` | 日语优化两层：净化层 + 投稿/修論文体层 | 日语轨专用 |
| `skills/journal-drafting/scripts/` | 图表渲染、视觉读图、字形检测 | 渲染≠造数 |
| `skills/vendor/reference-checker` | 投稿前参考文献穷尽核验 | 清空【待核】、分级 |
| `skills/vendor/journal-adapt` | 从目标刊语料萃取写作文化、生成动态写作 skill | `dynamic_writing_skill.md` |

## 一页式流程卡片

| 阶段 | 目的 | 成本 | 产出 |
|---|---|---|---|
| 最小启动闸 | 判断 A/B 主流程和材料状态 | 低 | 可启动/需补材料判断 |
| 完整 SPEC | 锁定正式写作边界 | 中 | 本篇规则卡 |
| 文献宽度扩展 | 补先行研究宽度 | 高，可选 | 按簇候选文献清单 |
| 动态写作层 | 学目标刊写作文化 | 高，可选 | 动态写作 skill |
| 骨架 | 定章节顺序 | 中 | 每节做什么、得什么 |
| 图表蓝图 | 让图表承载论点 | 中 | exhibit 清单、叙事弧、主附放置 |
| 逐节写 | 生成正文并自查 | 中 | 正文草稿 + warnings |
| 英文局部任务 | 小范围改写/审查 | 低 | 正文或审查 + 改动说明 |
| 投稿任务 | 深审、缩稿或 R&R | 中 | 严重度清单或逐点回应 |
| 总闸/核验/预演 | 定稿前查错 | 中 | 修改优先级清单 |

## 档位原则

期刊投稿档全配置跑；学位论文档不是“降级期刊稿”，而是独立路径：学校规程优先、章结构完整性优先、材料充分性优先、答辩委员视角优先。通用硬规则仍保留：主张强度、引用诚信、防漂移、图表先行。

## 完整流程细节

权威流程定义在编排器 [`SKILL.md`](../skills/journal-drafting/SKILL.md)；规则细节在 [`template-master-framework.md`](../skills/journal-drafting/template-master-framework.md)。本文件只做鸟瞰。
