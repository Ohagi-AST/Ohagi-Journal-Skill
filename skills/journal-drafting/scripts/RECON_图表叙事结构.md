# RECON｜图表叙事结构发现报告（全 10 篇 EER，作用·分布·逻辑联系）

> 配套 [`RECON_图表发现.md`](RECON_图表发现.md)（图表"长相"house-style）。本报告管**全局**：
> 图表在论文里**干什么活、怎么分布、怎么串成叙事**——这才是"段落服务图表、图表服务叙事"的骨架。
> 数据来自 `exhibit_map.py` 对**全 10 篇 EER**的文本抽取（题注 + 章节位置 + 正文交叉引用句 + 主/附切分），
> 全量明细见 `_exhibit_images/exhibit_map.json`。

---

## 0. 总量（全 10 篇）
- **77 张表 + 59 张图 = 136 个 exhibit**；其中 **32 个在附录（≈24%）**，**104 个在正文（≈76%）**。
- 每篇 exhibit 数：**7–26，中位 ~13–14**。不是"提到就放"，是**成套设计**。

## 1. 最强信号：方法族决定"谁领头"（实证印证 journal-adapt）
图/表的主次**不是偏好，是方法族的硬约束**——10 篇清楚分两类：

| 领头 | 方法族 | 例（本语料） | 图:表 |
|---|---|---|---|
| **表领头** | gravity/PPML、缩减式、结构分解、IV | Zylkin(FTA gravity) 8表1图；Sandkamp(AD反倾销) 12表14图但**正文表领头**；GVC劳动份额 10表；企业逃税 7表 | 表为主 |
| **图领头** | 合成控制(SCM)、事件研究、SDID、placebo | Mäkelä(葡萄牙移民) 12表**14图**；NAIM(墨西哥SCM) **13图**1表；挪威非欧盟 4图3表 | 图为主 |

> 推论给阶段二：图表蓝图的"头牌"必须按 `manuscript_method_family` 定——缩减式/gravity 篇头牌=基准系数表（走列）；SCM/事件研究篇头牌=主事件研究图。**不能一刀切。**

## 2. 典型叙事弧（canonical arc，跨 10 篇高度一致）
1. **动机图 Fig.1**（Intro，常 p1–p2）：一张"刺激读者"的趋势/事实图。
   - 证据："Fig.1 illustrates that while declines in labor shares started in the 1980s…"（GVC）；"China's and top-10 prefectures' export share…"；"The Effects of Globalization,1983–2002"。
2. **描述统计 Table 1**（Data 节）：几乎固定是 `Table 1 Descriptive statistics`（企业逃税、出口动态、GVC 均如此）。
3. **基准主结果表/图**（Results 开头，Table 2/3 或主 SCM 图）：**走列**从约束到丰富。
   - "Baseline aggregate-level gravity results **Table 2 presents** several estimates…"；"**Column (1) of Table 2** replicates…"。
4. **扩展/分解/机制**（连续多张，逐个递进）："Decomposition: extensive versus intensive margin"（Table 4）、"Duty interacted with firm size"（Table 6）。
5. **稳健性**（靠后，常直接命名）："**Table 10 Robustness checks**"；"Table 2 summarises the results from these various tests used as **robustness checks**"。
6. **异质性/机制图**（后段）：事件研究/分地区分部门森林图、机制指标图。
7. **附录（~24%）**：placebo/falsification 图、全样本估计、数据来源表、额外稳健。
   - "Fig. B.7 shows **placebo** SCM results…"；"Table A.1 Data descriptions and sources"；"estimates for all 78 countries… in Table C.1 of the Appendix"。

## 3. 图表之间的逻辑联系（不是孤立的）
- **互相引用、构成链条**："repeat the baseline WLS results **from Table 3, column 7**"（Table 5↔Table 3）；"Market potential is less important in **Table 7**… than in **Table 11**"；"present results in **Table 7** along with corresponding results **from Table 3**"。
- **列/面板级走读是常态**（与 house-style 的"每句绑定单元格"咬合）："The second column of Table 3 presents price effects"；"columns 1 and 3 of Table 6 show…"；"at the bottom of columns 3 and 4 of Table 4"；"Panel (I) of Table 9 while Panel (II) shows…"。

## 4. 正文"引出句式库"（写 write-to-exhibit 直接复用）
抽自 10 篇正文，按功能归类：

- **呈现/落位**：`We present results in Table N.` ／ `Our main results are presented in Table N.` ／ `Table N presents/reports/displays several estimates…` ／ `We report the results in Table N.`（GVC 篇每张表都这么引）
- **走列**：`Column (1) of Table N replicates…` ／ `The second column of Table N presents…` ／ `columns 1 and 3 of Table N show…`
- **解读/推断**：`Table N shows that…` ／ `The results in Table N indicate/imply that…` ／ `An overarching implication of Table N is that…`
- **跨图表衔接**：`…in line with those reported in Table M` ／ `repeat the baseline results from Table M, column k`
- **图**：`Fig. N illustrates/presents/plots/shows…` ／ `Fig. N (event study / placebo / by region and sector)`

## 5. 分布要点（给"放置计划"）
- **正文 ~76% / 附录 ~24%**：附录承接 placebo·全样本·数据来源·额外稳健；**主结果与基准识别一律留正文**（与 journal-adapt 的"系数表不得流放附录"硬规则一致）。
- 附录边界靠后（多在末 2–4 页或 Online Appendix）；附录 exhibit 用**字母前缀**（Table A.1 / Fig. B.7 / Table C.1）。
- 每节挂图表数随节而变：Results/Robustness 密集，Intro 仅 1 张动机图，Conclusion 一般 0。

---

## 6. 给阶段二的直接落点
1. **图表蓝图**字段已被实证支撑：`编号|类型|承载论点|锚定节|主/附|领头对象(按方法族)`；外加**叙事弧模板**（动机图→描述表→基准表/图→扩展→稳健→机制→附录）。
2. **头牌按方法族**：缩减式/gravity→基准系数表（走列）；SCM/事件研究→主事件研究图。
3. **引出句式库**（§4）并入 write-to-exhibit，反"文字提到就放表"。
4. **主/附放置规则**（§5）写进标准文档 checklist。

> 待补：顶刊（AER/QJE/ReStud）到位后同法抽取，看顶刊是否更"图领头/更少附录/更强叙事"，再校准 EER 基线。
