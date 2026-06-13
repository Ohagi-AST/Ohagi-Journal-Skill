# Ohagi-Journal-Skill

> 一套面向 **「研究已完成 → 开始把成果写成正式英文期刊级论文（或学位论文正文）」** 这一步的可复用写作框架。三个组件都是**纯 Markdown skill**，可配合 [Claude Code](https://claude.com/claude-code)、Codex 等任何支持 skill 机制的 AI agent 使用（不支持 skill 文件夹的环境，也可直接让 agent 读对应的 `SKILL.md` 执行）。

把 agent harness 的设计思路 —— *Rules-as-spec（规则即规范）＋ Verification-loop（验证闭环）＋ Memory（记忆防漂移）* —— 落到论文成稿的全过程：从锁定目标期刊、搭骨架、逐节写、控制主张强度，到引用穷尽核验和审稿人预演。

**语言**：框架正文为中文，适配中/英文论文写作，并对学位论文档位做了软化处理。

---

## 这是什么

整套东西分两层：

1. **母版规则书 + 风格层**（`skills/journal-drafting/起草框架母版.md` 及其 `references/`）—— 原创。一份跨论文复用的规则书：每开一篇新论文只重填「第 0 层 SPEC 槽位」，通用硬规则（1–9）永不改、所有论文共用。
2. **三个可调用的 skill**（`skills/`）—— 一个原创编排器（自带上面的母版）+ 两个第三方 MIT 工具，把流程串起来。

设计哲学：**第 0 层没填满之前不许动笔写正文**（硬闸）；**结论的语气 ≤ 识别的强度**（最硬的一条铁律）；**绝不编造引用**。

---

## 目录结构

```
Ohagi-Journal-Skill/
├── skills/
│   ├── journal-drafting/           ← 原创：起草编排器（自带母版规则书，开箱即用）
│   │   ├── SKILL.md                （编排器：串流程、管交互节奏）
│   │   ├── 起草框架母版.md          （母版：第 0 层 SPEC + 通用硬规则 1–9 + 三道验证闸）
│   │   ├── references/             （展开层：写作风格 / 文献宽度 / 稿件纯净度 / 领域约定）
│   │   └── 致谢与来源.md            （所有借鉴/采用来源的单一真相）
│   ├── reference-checker/          ← 第三方 MIT（Liuxiangjian-ai）：投稿前参考文献穷尽核验
│   └── journal-adapt/              ← 第三方 MIT（WantongC）：从目标刊语料萃取写作文化、生成动态写作 skill
├── LICENSE                         （原创部分 MIT）
└── README.md
```

---

## 怎么用

### 1. 安装三个 skill

先把仓库克隆下来：

```bash
git clone https://github.com/Ohagi-AST/Ohagi-Journal-Skill.git
cd Ohagi-Journal-Skill
```

每个 skill 都自包含、装在哪都能跑。以 **Claude Code** 为例，把 `skills/` 下三个文件夹复制到它的 skill 目录：

**macOS / Linux（bash）：**

```bash
# 在仓库根目录执行
mkdir -p ~/.claude/skills
cp -R skills/journal-drafting   ~/.claude/skills/
cp -R skills/reference-checker  ~/.claude/skills/
cp -R skills/journal-adapt      ~/.claude/skills/
```

**Windows（PowerShell）：**

```powershell
# 在仓库根目录执行
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force skills\journal-drafting   "$HOME\.claude\skills\"
Copy-Item -Recurse -Force skills\reference-checker  "$HOME\.claude\skills\"
Copy-Item -Recurse -Force skills\journal-adapt      "$HOME\.claude\skills\"
```

> **其他 agent（Codex 等）**：装进各自的 skill / 自定义指令目录即可；若环境不支持 skill 文件夹，直接让 agent 读取对应文件夹下的 `SKILL.md` 并按其执行，效果相同。
> `journal-drafting` 已**自带母版规则书**（`起草框架母版.md` + `references/`），无需任何额外放置或配置。
> `journal-adapt` 的部分功能（PDF→Markdown）依赖 MinerU；若你的语料已是 Markdown/文本则无需安装。详见 `skills/journal-adapt/docs/INSTALLATION.md`。

### 2. 开始起草

向你的 agent 描述需求（触发词例：「开始起草」「写成期刊论文」「按期刊标准整理」），`journal-drafting` 会：

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

> 完整的来源、采用形式与许可证清单见 [`skills/journal-drafting/致谢与来源.md`](skills/journal-drafting/致谢与来源.md) —— 这是本框架的「来源单一真相」。

---

## 许可证

- 本仓库**原创部分**（`skills/journal-drafting/`，含其自带的母版与风格层）以 **MIT** 发布，见根目录 [`LICENSE`](LICENSE)。
- `skills/reference-checker/` 与 `skills/journal-adapt/` 各自遵循其原作者的 MIT 许可证。

使用时请保留相应署名。欢迎提 issue / PR。
