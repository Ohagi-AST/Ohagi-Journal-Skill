# Ohagi-Journal-Skill

> 一套面向 **「研究已完成 → 开始把成果写成正式论文正文」** 这一步的可复用写作框架。核心场景是**实证经济学论文**（英文期刊稿、学位论文、图表叙事、日文稿整理），规则也可迁移到相近社会科学论文。三个组件都是 **Markdown-first skill**，并附带可选脚本工具链；可配合 [Claude Code](https://claude.com/claude-code)、Codex 等任何支持 skill 机制的 AI agent 使用（不支持 skill 文件夹的环境，也可直接让 agent 读对应的 `SKILL.md` 执行）。

把 agent harness 的设计思路 —— *Rules-as-spec（规则即规范）＋ Verification-loop（验证闭环）＋ Memory（记忆防漂移）* —— 落到论文成稿的全过程：从选择入口、锁定目标约束、搭骨架、做图表蓝图、逐节写、控制主张强度，到引用核验和投稿/答辩前预演。

**语言**：框架正文为中文；英文术语用于检索和论文写作场景。英文期刊、学位论文、日文投稿/修論各有入口。

---

## 这是什么

整套东西分两层：

1. **母版规则书 + 风格层**（`skills/journal-drafting/template-master-framework.md` 及其 `references/`）—— 原创。一份跨论文复用的规则书：每开一篇新论文先过「最小启动闸」，正式正文前补齐「完整 SPEC」，通用硬规则（1–9）永不改、所有论文共用。
2. **三个可调用的 skill**（`skills/`）—— 一个原创编排器（自带上面的母版）+ 两个第三方 MIT 工具，把流程串起来。

设计哲学：**最小启动可以轻，正式正文必须过完整 SPEC**；**结论的语气 ≤ 识别的强度**（最硬的一条铁律）；**绝不编造引用**。

---

## 我该走哪条路？

| 入口 | 适合你如果 | 第一件事 |
|---|---|---|
| 英文期刊成稿 | 研究已经完成，想写成英文期刊论文 | 过最小启动闸，再补完整 SPEC |
| 学位论文正文 | 要写修士/博士论文或毕业论文正文 | 先锁学校规程、答辩委员视角和章结构 |
| 已有日文稿整理 | 手里已有日文草稿，只想去中文味和统一学术文体 | 走日语优化快速入口，不进完整起草流程 |
| 图表蓝图/图表规范 | 结果很多，想先决定图表顺序、主附放置和叙事弧 | 只走 exhibit plan |

完整入口说明和可复制 prompt 见 [`docs/entrypoints.md`](docs/entrypoints.md) 与 [`docs/getting-started.md`](docs/getting-started.md)。

---

## 目录结构

```
Ohagi-Journal-Skill/
├── skills/
│   ├── journal-drafting/           ← 原创：起草编排器（自带母版规则书，开箱即用）
│   │   ├── SKILL.md                （编排器：串流程、管交互节奏）
│   │   ├── template-master-framework.md   （母版：最小启动闸 + 完整 SPEC + 通用硬规则 1–9 + 三道验证闸）
│   │   ├── references/             （展开层：en-* 英文写作风格/文献宽度/纯净度/领域约定 + ja/ 日语优化两层）
│   │   ├── scripts/                （图表渲染 exhibit_render.py/.do + zh_glyph_check.py 等工具链）
│   │   └── credits-and-sources.md  （所有借鉴/采用来源的单一真相）
│   └── vendor/                     ← 第三方 MIT 工具（随包附带，各带 VERSION 记录上游来源）
│       ├── reference-checker/      ← 第三方 MIT（Liuxiangjian-ai）：投稿前参考文献穷尽核验
│       └── journal-adapt/          ← 第三方 MIT（WantongC）：从目标刊语料萃取写作文化、生成动态写作 skill
├── tests/                          （Python 工具链单测 + 跨文件一致性元检查 + 冒烟测试）
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

每个 skill 都自包含、装在哪都能跑。以 **Claude Code** 为例，把三个 skill 文件夹（原创的 `journal-drafting` + `vendor/` 下两个第三方）复制到它的 skill 目录：

**macOS / Linux（bash）：**

```bash
# 在仓库根目录执行
mkdir -p ~/.claude/skills
cp -R skills/journal-drafting          ~/.claude/skills/
cp -R skills/vendor/reference-checker  ~/.claude/skills/
cp -R skills/vendor/journal-adapt      ~/.claude/skills/
```

**Windows（PowerShell）：**

```powershell
# 在仓库根目录执行
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force skills\journal-drafting          "$HOME\.claude\skills\"
Copy-Item -Recurse -Force skills\vendor\reference-checker  "$HOME\.claude\skills\"
Copy-Item -Recurse -Force skills\vendor\journal-adapt      "$HOME\.claude\skills\"
```

> **其他 agent（Codex 等）**：装进各自的 skill / 自定义指令目录即可；若环境不支持 skill 文件夹，直接让 agent 读取对应文件夹下的 `SKILL.md` 并按其执行，效果相同。
> `journal-drafting` 已**自带母版规则书**（`template-master-framework.md` + `references/`），无需任何额外放置或配置。
> `journal-adapt` 的部分功能（PDF→Markdown）依赖 MinerU；若你的语料已是 Markdown/文本则无需安装。详见 `skills/vendor/journal-adapt/docs/INSTALLATION.md`。

### 2. 选择入口

先看 [`docs/entrypoints.md`](docs/entrypoints.md)，选英文期刊成稿、学位论文正文、已有日文稿整理或图表蓝图。每条入口都给了「适合谁 / 准备什么 / 第一句 prompt / 会走哪些阶段 / 哪些可跳过」。

### 3. 低成本启动

材料不完整也可以先启动规划：只要给出入口、一句话研究问题、目标刊/学校规程/日语轨道、研究结果是否完成，agent 就能帮你判断下一步。正式逐节写正文前，仍必须补齐完整 SPEC（结构母本、contribution、识别红线、引用样式、数据出处等）。

---

## 文档

| 文档 | 内容 |
|---|---|
| [`docs/entrypoints.md`](docs/entrypoints.md) | 四条入口：英文期刊、学位论文、日语整理、图表蓝图 |
| [`docs/getting-started.md`](docs/getting-started.md) | 快速开始 + 可直接改用的示例 prompt |
| [`docs/overview.md`](docs/overview.md) | 体系结构鸟瞰（两层结构、组件分工、流程主轴） |
| [`docs/interaction-guide.md`](docs/interaction-guide.md) | 面向人类用户的交互说明（节奏、硬闸、加速/叫停） |
| [`docs/reference/rules-overview.md`](docs/reference/rules-overview.md) | 母版通用硬规则 1–9 一页速查 |
| [`docs/reference/field-templates/README.md`](docs/reference/field-templates/README.md) | 把自己的领域写作惯例加进来的模板 |

> `tests/` 下是 Python 工具链单测 + 跨文件一致性元检查 + 冒烟测试。先跑 `python -m pip install -r requirements-dev.txt` 安装测试依赖，再跑 `python -m unittest discover -s tests`。

---

## 第三方组件与致谢

`skills/` 下两个工具是**别人的 MIT 开源项目**，本仓库按其 MIT 许可证随包附带、保留原作者署名：

| 组件 | 来源 | 许可证 |
|---|---|---|
| `skills/vendor/reference-checker/` | [Liuxiangjian-ai/reference-checker-skill](https://github.com/Liuxiangjian-ai/reference-checker-skill) | MIT（见该子目录 `LICENSE`；上游来源记于 `VERSION`） |
| `skills/vendor/journal-adapt/` | [WantongC/journal-adapt-writing-skill](https://github.com/WantongC/journal-adapt-writing-skill) | MIT（见该子目录 `LICENSE`）·**本仓库已在其基础上修改**（方法族感知聚合 + 计量装置信号；改动详见该子目录 `LICENSE` 的 MODIFICATIONS 段；上游来源记于 `VERSION`） |

母版在搭建中还借鉴了若干开源仓库的**方法论、结构与清单**（未复制其内容）：
[affaan-m/ecc](https://github.com/affaan-m/ecc)、
[lishn6/awesome-ai-econ-research-writing](https://github.com/lishn6/awesome-ai-econ-research-writing)、
[Lambenthan/empiricalwiki](https://github.com/Lambenthan/empiricalwiki)、
[juliaError/econ-TopJournal-writing-Skill](https://github.com/juliaError/econ-TopJournal-writing-Skill)（CC BY-NC，仅再造思路、未复制文字）。

> 完整的来源、采用形式与许可证清单见 [`skills/journal-drafting/credits-and-sources.md`](skills/journal-drafting/credits-and-sources.md) —— 这是本框架的「来源单一真相」。

---

## 许可证

- 本仓库**原创部分**（`skills/journal-drafting/`，含其自带的母版与风格层）以 **MIT** 发布，见根目录 [`LICENSE`](LICENSE)。
- `skills/vendor/reference-checker/` 与 `skills/vendor/journal-adapt/` 各自遵循其原作者的 MIT 许可证。

使用时请保留相应署名。欢迎提 issue / PR。
