# 体系结构概览（Overview）

一套面向**「研究已完成 → 开始把成果写成正式期刊级论文（或学位论文正文）」**这一步的可复用写作框架。把 agent harness 的设计思路——*Rules-as-spec（规则即规范）＋ Verification-loop（验证闭环）＋ Memory（记忆防漂移）*——落到论文成稿全过程。

## 两层结构

1. **母版规则书 + 风格层**（`skills/journal-drafting/template-master-framework.md` 及其 `references/`）——原创。一份跨论文复用的规则书：每开一篇新论文只重填「第 0 层 SPEC 槽位」，通用硬规则 1–9 永不改、所有论文共用。
2. **三个可调用的 skill**——一个原创编排器（`journal-drafting`，自带上面的母版）+ 两个第三方 MIT 工具（`vendor/reference-checker`、`vendor/journal-adapt`），把流程串起来。

## 三条设计哲学（硬约束）

- **第 0 层没填满之前不许动笔写正文**（硬闸）。
- **结论的语气 ≤ 识别的强度**（最硬的一条铁律）。
- **绝不编造引用 / 数据 / 新规性证据**。

## 组件分工

| 组件 | 角色 | 关键产物 |
|---|---|---|
| `skills/journal-drafting/SKILL.md` | 编排器薄壳：路由 + 交互节奏 + 流程串联 | 进度面板、逐步推进 |
| `skills/journal-drafting/template-master-framework.md` | 母版：第 0 层 SPEC + 硬规则 1–9 + 三道验证闸 | 规则即规范 |
| `skills/journal-drafting/references/en-*` | 英文写作展开层：写作风格 / 文献宽度 / 纯净度 / 领域约定 / 图表叙事 | 逐节按需加载 |
| `skills/journal-drafting/references/ja/*` | 日语优化两层：净化层（中文残留）+ 文体层（投稿/修論） | 日语轨专用 |
| `skills/journal-drafting/scripts/` | 图表渲染（Stata `.do` / Python `exhibit_render.py`）+ 视觉读图 + 字形检测 | 渲染≠造数 |
| `skills/vendor/reference-checker` | 投稿前参考文献穷尽核验 | 清空【待核】、分级 |
| `skills/vendor/journal-adapt` | 从目标刊语料萃取写作文化、生成动态写作 skill | `dynamic_writing_skill.md` |

## 流程主轴（六步）

```
[0]   Phase 0 SPEC（三个 ⛔ 硬闸）
[0.5] 文献宽度扩展（可选）
[1]   动态写作层 journal-adapt（可选）
[2]   搭骨架
[2.5] 图表蓝图（结果型论文）
[3]   逐节写（一节一停，每节《单节自查》）
[3.5] 日语优化（仅日语轨）
[4]   总闸
[5]   引用穷尽核验 reference-checker
[6]   审稿人预演
```

学位论文档会**自动跳过/软化**期刊专属环节（动态写作层、层级现实性、新规性穷尽、投稿体例等），通用骨架照走。详见母版「适用档位」表。

## 完整流程细节

权威流程定义在编排器 [`SKILL.md`](../skills/journal-drafting/SKILL.md)（agent 每轮按它执行）；规则细节在 [`template-master-framework.md`](../skills/journal-drafting/template-master-framework.md)。本文件只做鸟瞰。
