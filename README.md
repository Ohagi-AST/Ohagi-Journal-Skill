# Ohagi-Journal-Skill

> 一套面向 **「研究已完成 → 开始把成果写成正式英文期刊级论文（或学位论文正文）」** 这一步的可复用写作框架，配合 [Claude Code](https://claude.com/claude-code) 的 skill 机制使用。

把 agent harness 的设计思路 —— *Rules-as-spec（规则即规范）＋ Verification-loop（验证闭环）＋ Memory（记忆防漂移）* —— 落到论文成稿的全过程：从锁定目标期刊、搭骨架、逐节写、控制主张强度，到引用穷尽核验和审稿人预演。

**语言**：框架正文为中文，适配中/英文论文写作，并对学位论文档位做了软化处理。

---

## 这是什么

整套东西分两层：

1. **母版规则书 + 风格层**（`journal-framework/`）—— 原创。一份跨论文复用的规则书：每开一篇新论文只重填「第 0 层 SPEC 槽位」，通用硬规则（1–9）永不改、所有论文共用。
2. **三个可调用的 skill**（`skills/`）—— 一个原创薄壳 + 两个第三方 MIT 工具，把流程串起来。

设计哲学：**第 0 层没填满之前不许动笔写正文**（硬闸）；**结论的语气 ≤ 识别的强度**（最硬的一条铁律）；**绝不编造引用**。

---

## 目录结构

```
Ohagi-Journal-Skill/
├── journal-framework/              ← 原创：母版 + 风格层 + 致谢
│   ├── 英文期刊规则.md              （母版：第 0 层 SPEC + 通用硬规则 1–9 + 三道验证闸）
│   ├── references/
│   │   ├── 经济学写作风格.md         （共享写作风格层）
│   │   ├── 文献宽度扩展.md           （引用图谱滚雪球，补先行研究宽度）
│   │   ├── 稿件语气与正文纯净度.md    （三通道分离 + 段级 linter）
│   │   └── 领域写作约定.md           （分子领域的呈现约定）
│   └── 致谢与来源.md                （所有借鉴/采用来源的单一真相）
├── skills/
│   ├── journal-drafting/           ← 原创：编排器薄壳（串流程、管交互节奏）
│   ├── reference-checker/          ← 第三方 MIT（Liuxiangjian-ai）：投稿前参考文献穷尽核验
│   └── journal-adapt/              ← 第三方 MIT（WantongC）：从目标刊语料萃取写作文化、生成动态写作 skill
├── LICENSE                         （原创部分 MIT）
└── README.md
```

---

## 怎么用（配合 Claude Code）

### 1. 安装三个 skill

把 `skills/` 下三个文件夹复制到 Claude Code 的 skill 目录：

```bash
# 在仓库根目录执行
mkdir -p ~/.claude/skills
cp -R skills/journal-drafting   ~/.claude/skills/
cp -R skills/reference-checker  ~/.claude/skills/
cp -R skills/journal-adapt      ~/.claude/skills/
```

> `journal-adapt` 的部分功能（PDF→Markdown）依赖 MinerU；若你的语料已是 Markdown/文本则无需安装。详见 `skills/journal-adapt/docs/INSTALLATION.md`。

### 2. 放置母版

`journal-drafting` 启动时会用 `find ~ -path "*journal-framework/英文期刊规则.md"` 向上搜索母版，**所以把整个 `journal-framework/` 文件夹放在你用户目录（`~`）下任意位置即可**（比如直接把本仓库 clone 在那里）。

### 3. 开始起草

在 Claude Code 里描述你的需求（触发词例：「开始起草」「写成期刊论文」「按期刊标准整理」），`journal-drafting` 会：

1. 判断档位（期刊投稿 / 学位论文）；
2. 带你逐项填「第 0 层 SPEC」（目标刊、层级现实性、结构母本 3–5 篇 —— 三个硬闸）；
3. 可选：调 `journal-adapt` 从目标刊真论文萃取写作文化、调文献宽度扩展补先行研究；
4. 搭骨架 → 一节一停地逐节写，每节跑《单节自查》；
5. 齐稿后跑三道终检：总闸 → `reference-checker` 引用穷尽核验 → 审稿人预演。

---

## 第三方组件与致谢

`skills/` 下两个工具是**别人的 MIT 开源项目**，本仓库按其 MIT 许可证随包附带、保留原作者署名：

| 组件 | 来源 | 许可证 |
|---|---|---|
| `skills/reference-checker/` | [Liuxiangjian-ai/reference-checker-skill](https://github.com/Liuxiangjian-ai/reference-checker-skill) | MIT（见该子目录 `LICENSE`） |
| `skills/journal-adapt/` | [WantongC/journal-adapt-writing-skill](https://github.com/WantongC/journal-adapt-writing-skill) | MIT（见该子目录 `LICENSE`） |

母版在搭建中还借鉴了若干开源仓库的**方法论、结构与清单**（未复制其内容）：
[affaan-m/ecc](https://github.com/affaan-m/ecc)、
[lishn6/awesome-ai-econ-research-writing](https://github.com/lishn6/awesome-ai-econ-research-writing)、
[Lambenthan/empiricalwiki](https://github.com/Lambenthan/empiricalwiki)、
[juliaError/econ-TopJournal-writing-Skill](https://github.com/juliaError/econ-TopJournal-writing-Skill)（CC BY-NC，仅再造思路、未复制文字）。

> 完整的来源、采用形式与许可证清单见 [`journal-framework/致谢与来源.md`](journal-framework/致谢与来源.md) —— 这是本框架的「来源单一真相」。

---

## 许可证

- 本仓库**原创部分**（`journal-framework/` 与 `skills/journal-drafting/`）以 **MIT** 发布，见根目录 [`LICENSE`](LICENSE)。
- `skills/reference-checker/` 与 `skills/journal-adapt/` 各自遵循其原作者的 MIT 许可证。

使用时请保留相应署名。欢迎提 issue / PR。
