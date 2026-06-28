# 文献宽度扩展（引用图谱滚雪球 / Citation-Graph Snowballing）

> 母版规则 2 + 第 0 层的展开。借鉴 EmpiricalWiki `/discover` 的方法（不搬其基建，只用引用图谱 API）。
> **何时用**：基础研究/逻辑机制已立、但**锚点论文不到 10 篇**，写先行研究/文献综述时**宽度不够**。
> **覆盖范围**：以英文/国际文献为主（Semantic Scholar 对经济学含 NBER/AEA 覆盖好）；中文、日文文献稀疏，**暂不强求**，需要时另用 WebSearch 补。

---

## 目录

核心心智｜触发交互｜四向滚雪球｜API 调法｜排序信号｜按簇归位｜输出格式｜护栏｜衔接

## 核心心智

> **宽度不足 ≠ 锚点太少。** 你有足够锚点，缺的是**从锚点向外的系统性滚雪球**。
> 不要去"再找几篇核心论文"，而是**从已有锚点出发，用引用关系把周边文献长出来**。

---

## 触发交互（gated，先问后跑）

启动这一步时，先对用户说（等回答再往下）：

> 「请把你目前的**基础锚点论文**给我——就是逻辑机制上最核心的那不到 10 篇，**标题或 DOI 都行**。我从它们出发做引用图谱滚雪球，给你一份按簇排好序的候选宽度清单。」

拿到锚点后再执行下面的扩展。**没有锚点不要开跑。**

---

## 四个滚雪球方向

从每个锚点，往四个方向扩：

1. **向后（backward）**：锚点**引用了谁** → 机制的上游/源头，先行研究的根。
2. **向前（forward）**：**谁引用了锚点**，尤其近 3 年 → 最新进展，防"你怎么没引 XX 2024"。
3. **共被引 / 推荐（co-citation / recommendations）**：和锚点**常被一起引用**、或 S2 推荐的近邻 → 同一对话圈，补宽度最高效。
4. **横向（lateral）**：**同识别策略 / 同数据 / 同机制、不同主题** → 补方法与机制维度的厚度。

---

## 引用图谱 API 具体调法（Semantic Scholar Graph API，免费、无需 key，有速率限制）

用 **WebFetch（或 curl）GET 下列 URL，返回 JSON**。有 `SEMANTIC_SCHOLAR_API_KEY` 时配额更高（可选）。

**第 1 步 解析锚点 → 拿 paperId**
- 按 DOI：`https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=title,year,authors,venue,citationCount,externalIds`
- 按标题：`https://api.semanticscholar.org/graph/v1/paper/search?query={URL编码标题}&fields=title,year,authors,venue,citationCount,externalIds&limit=5`（在返回里挑标题/年份对得上的那条）

**第 2 步 三个方向各拉一批**（把 `{paperId}` 换成上一步拿到的 id）
- 向后（references）：`https://api.semanticscholar.org/graph/v1/paper/{paperId}/references?fields=title,year,authors,venue,citationCount,influentialCitationCount,externalIds&limit=100`
- 向前（citations）：`https://api.semanticscholar.org/graph/v1/paper/{paperId}/citations?fields=title,year,authors,venue,citationCount,influentialCitationCount,externalIds&limit=100`
- 推荐（recommendations，近邻/横向）：`https://api.semanticscholar.org/recommendations/v1/papers/forpaper/{paperId}?fields=title,year,authors,venue,citationCount,externalIds&limit=50`

**共被引**：S2 无直接端点 → 近似法：对**多个锚点**各拉 references/citations，**取交集**（被多个锚点共同引用、或共同引用多个锚点的论文）= 高价值近邻。

**批量解析**（锚点多时）：`POST https://api.semanticscholar.org/graph/v1/paper/batch`，body `{"ids":["DOI:...","..."]}`，同样带 `fields`。

> API 字段/端点若有变动，以实际返回为准，别硬套；拿不到就降级用 WebSearch 补。

---

## 排序信号

候选不是堆，按这个顺序筛排：

1. **相关度（主筛，0–3 由你判断）**：是否服务本篇主轴 / 落得进某一簇。**0 分直接丢**——宁缺毋滥。
2. **影响力**：`citationCount` / `influentialCitationCount` / venue 档次。
3. **新近度**：向前滚的结果，近 3 年加权（补"最新进展"）。

---

## 按簇归位（扩出来当场归类，别攒成一堆）

每篇候选**立即塞进它服务的那一簇**——簇用本篇第 0 层的主轴定义（通用默认）：
- 测量簇（构念/口径怎么测）
- 识别簇（内生性/识别策略）
- 机制簇（因果通道/理论）
- 方法簇（同模型/同数据）

归好类的候选**直接长成母版规则 2 的「文献地图」骨架**。

---

## 输出格式

给用户一张**按簇分组、簇内排序**的候选表：

| 簇 | 标题 | 作者 | 年 | venue | 被引 | 雪球方向 | 为何相关（1句） | DOI / S2链接 | 状态 |
|---|---|---|---|---|---|---|---|---|---|
| 识别 | … | … | 2024 | … | 312 | forward | 提出处理内生性的新工具变量 | 10.xxxx | 待读·待核 |

每篇默认状态 `待读·待核`，由用户决定读哪些。

---

## 护栏

1. **只列 API 真实返回的论文，绝不补造**作者/年份/标题。拿不准的标 `【待核】`。
2. **下游交 `reference-checker` 核实**：用户选定要用的，进 reference-checker 穷尽核验（与规则 5 衔接）。
3. **定向宽度、不注水**：每篇必须能一句话说清"它服务哪条主轴 / 哪一簇"，说不出就丢。先行研究是**定位不是罗列**（规则 2）。
4. **覆盖诚实**：英文/国际覆盖好；中文、日文稀疏，缺口明说、用户已确认暂不强求。

---

## 衔接

- **上游**：第 0 层的「结构母本 / 锚点」。
- **本步**：从锚点滚雪球 → 候选宽度清单（本文件）。
- **下游**：用户筛选 → `reference-checker` 核实 → 喂母版规则 2「文献地图」写先行研究。
