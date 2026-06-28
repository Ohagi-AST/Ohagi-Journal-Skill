# 经济学写作风格层（通用，所有论文共用）

> 母版规则 7 的展开。**这是共享风格层**：写 intro、综述、结果、机制、审稿回复时都套这一份。
> 语言无关：英文刊、日文修論都适用（具体引用样式由该篇第 0 层的「引用样式」槽位决定，本文件不锁死某一种）。

## 目录

核心原则｜信息密度｜逻辑与段落｜自然措辞｜语气与主张｜结果与机制｜用词｜第一人称与共同作者｜脚注与符号｜图表｜数字与引用

## 核心原则

经济学写作不是把句子写得高级。**每一句话只该做四件事之一：帮读者认清问题、呈现证据、解释机制、限定结论。** 不做这四件事的句子，删。

目标是让目标读者顺畅理解，不是“看起来不像 AI”。不要为了规避检测而强塞破折号、括号、长短句配额或故意制造粗糙转折；节奏和措辞优先服从目标刊真实语料与清晰度。

## 信息密度

- 每句话都要推进论证 / 引入证据 / 指明机制 / 澄清解读。没有功能的句子删掉。
- ⛔ 禁止清嗓子式开头："It is important to note that…""值得注意的是…""It should be mentioned that…"
- ⛔ 禁止空洞结尾："This contributes to our understanding of…"——要具体说**加了什么**。

## 逻辑与段落

- 过渡靠**实质**，不靠通用连接词（别反复 Furthermore / Moreover / In addition / さらに）。
- **每段第一句要说清这段的逻辑角色**：主张 / 事实 / 机制 / caveat / 下一个检验 / 模型对象 / 反事实 / 福利解读。
- 强实证段落的典型推进：主张 → 证据 → 解读或机制 → caveat。
- 每句话要承接、限定或深化上一句，而不是罗列互不相关的事实。

## 自然措辞

- 朗读检查：若句子像直译、需要回读或堆叠多个名词修饰，改为清楚的主语—动词—宾语。
- 一次只用一个有效修饰语；删 redundant pairs、空洞强度词和混合隐喻。
- 给裸 `this` 穿衣：写 `This estimate/pattern/assumption…`，不要让读者猜 `This` 指什么。
- 表和图可以作主语：`Table 3 shows…`；但句子仍要说出它展示的实质对象。

## 语气与主张

- 语气克制、精确、低调。
- ⛔ 慎用 very / really / hugely / remarkably / strikingly / notably（除非事实真的强）。
- 改用：large / substantial / economically meaningful / quantitatively important / sizable / modest / limited / concentrated among。
- 新规性措辞**允许**用（novel / new / unique），但必须**指明在哪个维度新**：setting / data / measurement / identification / mechanism / model / counterfactual / policy。
- ⛔ 禁止无支撑的吹捧：groundbreaking / definitive / transformative。
- ⛔ 禁止主观措辞：I think / I feel / in my opinion / to be honest。
- ⛔ 禁止 "This proves that" / "demonstrates conclusively" / "X is the cause of Y"——**除非设计支撑**。

## 因果谨慎句库（设计不支持因果时改用这些）

> 这是母版规则 4「主张强度 ≤ 识别强度」的措辞落地。设计是关联/内生选择/描述性时，从下面挑：

- The evidence is consistent with…
- The estimates suggest…
- The results support the interpretation that…
- This pattern points to…
- These findings are consistent with…
- （日文）…と整合的である / …を示唆する / …と相関している

## 结果与机制

- Results 节只管：估计值、系数解读、量级、统计显著、经济显著、与预测是否一致。
- 表/图/检验没直接支撑的机制，**不要在 Results 节展开**。
- 机制证据默认按「渠道的提示性证据」写，不是完整因果链的证明——除非设计直接识别该渠道。

## 用词（avoid → prefer）

| 避免 | 改用 |
|---|---|
| utilise | use |
| commence | start / begin |
| regarding | about / on |
| demonstrate | show / suggest |
| facilitate | help |
| prior to | before |
| subsequent to | after |
| in order to | to |
| due to the fact that | because |

## 第一人称与共同作者

- 经济学写作里第一人称可以用，自然就好：I document / I estimate / I show that / We construct / This paper documents。
- 别为了避第一人称写成别扭被动（"It is shown by the analysis that…"）。
- 单作者用 `I`、多作者用 `we`，除非目标刊/作者已有一致约定；不要在同一稿件漂移。
- 多作者项目指定一名 voice editor，统一人称、时态、术语、hedging 与段落节奏；各节不能保留明显不同的作者声音。

## 脚注与符号

- 重要论证放正文；脚注只放典型读者可跳过、但部分读者确有用的资料、简单推导或延伸引用。
- 只编号后文会引用的公式；展示公式前先用文字说明其经济对象，展示后立即定义变量。
- 拉丁字母/希腊字母和下标层级保持一致；报告 2–3 个有意义的有效数字，不照抄软件全部小数。

## 图表

> 这是**句级 caption / 表注**标准。**全文级图表套件**（图表先行 / 图表蓝图 / 全文统一 house-style / 视觉自检 / 主附放置 / Stata 渲染）见 `en-exhibit-design-narrative.md`。

- 图表标题用 sentence case，一般句末不加句号。**题注缩写跟目标刊**（AEA 系 `Figure 1.`；Elsevier/EER 用 `Fig. 1.`）。
- 表注按需报告：样本、控制、固定效应、聚类、标准误、显著性约定。
- 来源行区分：作者计算 / 复制他人图 / 基于外部数据。
- 例：
  - `Figure 1. Earnings around childbirth`
  - `Table 2. Effects of sex ratio at birth on educational attainment`
  - `Source: Author's calculations using …`
  - `Source: Reproduced from Kleven et al. (2019).`

## 数字、单位、日期

- 文、表、图单位一致。
- 年份、统计量、样本量、参数估计用阿拉伯数字。
- 散文里 1–9 可拼写，结果节和表格里一般用数字。
- 散文用 percent，表格用 %。
- 等号两边留空格：`x = y`。
- 范围用 en dash：`1975–1990`，不是连字符。
- ⛔ 不编造页码、卷号、作者缩写、数据细节、模型假设、估计值、弹性、福利结果、样本筛选。

## 引用（样式跟随该篇第 0 层指定）

- 默认 author-year（Chicago author-date）；具体样式以目标刊/修論规程为准。
- 叙述引用 `Author (Year)`；括号引用 `(Author Year)`；两位 `Author and Author (Year)`；三位及以上 `Author et al. (Year)`。
- ⛔ 书目细节不确定 → 标 `【待核】`，绝不编。
