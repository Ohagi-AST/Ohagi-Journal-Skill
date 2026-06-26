#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exhibit_map.py — 抽「图表叙事结构」：跨论文提取 图表清单 / 章节位置 / 正文交叉引用句 / 主-附切分。

为什么要它：图表的「长相」(house-style) 之外，更要紧的是图表在全局的【作用·分布·逻辑联系】——
一篇几张表几张图、落在哪节、正文怎么引出（引出句=声明的叙事角色）、主文 vs 附录怎么分。
这层主要靠文字即可全量抽取（不必逐页读图），用来给「图表蓝图」实证定标，而非拍脑袋。

抽取项（每篇）：
- exhibits：所有 Table N / Fig. N / Figure N 题注 + 页码 + 标题片段 + 主文/附录。
- sections：编号章节标题 + 起始页（给"图表落在哪节"定位）。
- xrefs：正文里"Table N…/Fig. N…"的句子（=该图表的叙事功能与上下文逻辑）。
- main/appendix：Appendix 边界页；字母前缀(Table A1)或在边界之后 = 附录。

用法:
    python3 exhibit_map.py *.pdf                 # 打印紧凑汇总 + 存 exhibit_map.json
    python3 exhibit_map.py a.pdf b.pdf --json out.json --maxxref 3
输出 JSON 含全量明细（含每张图表的全部 xref 句），stdout 为便于眼看的紧凑视图。
"""
import argparse, glob, json, os, re, sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        sys.exit("[!] 缺 PyMuPDF：pip install pymupdf")

# 题注：行首 Table/Fig./Figure + 编号（含 A1/B2 等附录前缀），兼容句点/冒号。
CAP_RE = re.compile(r'^(Tables?|Figs?\.?|Figures?)\s+([A-Z]?\.?\d+[A-Za-z]?)\.?\s*:?\s*(.*)$', re.I)
_NUM_RE = r'[A-Z]?\.?\d+[A-Za-z]?'
_NUM_SEP_RE = r'(?:\s*,\s*(?:and\s+|or\s+)?|\s+(?:and|or|to)\s+|\s*[-–]\s*)'
# 正文交叉引用：句中出现的 Table N / Fig. N，含复数列表与简单范围。
XREF_RE = re.compile(rf'\b(Tables?|Figs?\.?|Figures?)\s+({_NUM_RE}(?:{_NUM_SEP_RE}{_NUM_RE})*)', re.I)
# 章节标题：行首 "4 Results" / "4. Results" / "4.1 ..." （首词数字，后接大写词）
SEC_RE = re.compile(r'^(\d{1,2}(?:\.\d{1,2})?)\.?\s+([A-Z][A-Za-z][^\n]{1,48})$')
# 附录边界
APPX_RE = re.compile(r'^\s*(Online\s+)?Appendix\b', re.I)


def norm(lbl, num):
    lbl = "Fig." if lbl.lower().startswith("fig") else "Table"
    return f"{lbl} {num}"


def _nums_from_spec(spec):
    nums = re.findall(_NUM_RE, spec)
    simple_range = re.fullmatch(r'\s*(\d+)\s*[-–]\s*(\d+)\s*', spec)
    if simple_range:
        a, b = int(simple_range.group(1)), int(simple_range.group(2))
        step = 1 if a <= b else -1
        return [str(n) for n in range(a, b + step, step)]
    return nums


def extract_xref_labels(sentence):
    """Return normalized exhibit labels referenced in one sentence."""
    labels = []
    seen = set()
    for m in XREF_RE.finditer(sentence):
        for num in _nums_from_spec(m.group(2)):
            label = norm(m.group(1), num)
            if label not in seen:
                seen.add(label)
                labels.append(label)
    return labels


# 学术文本里带句点、但不该触发断句的缩写（句点是缩写的一部分，不是句末）。
# 关键：放过 "Fig." / "Figs." / "Eq." 等——否则 "see Fig. 3." 会在 "Fig." 后误断，
# 把交叉引用 "Fig. 3" 劈成两句，XREF_RE 再也匹配不到（这是本函数原来的 bug）。
_ABBREV = (
    "e.g.", "i.e.", "cf.", "vs.", "etc.", "et al.", "al.",
    "Fig.", "Figs.", "Eq.", "Eqs.", "No.", "Nos.", "pp.", "p.",
    "Sec.", "Tab.", "Col.", "Cols.", "Ch.", "Ref.", "Refs.", "approx.",
)
_DOT = "\x00"  # 占位符：临时顶替缩写里的句点，断句后再还原


def split_sentences(text):
    # 粗切句：按句末标点 + 空白。够用于挑含 xref 的句子。
    # 先把学术缩写里的句点藏成占位符，避免在 e.g./Fig./Table 等后面误断句。
    t = text.replace("\n", " ")
    for ab in _ABBREV:
        t = t.replace(ab, ab.replace(".", _DOT))
    parts = re.split(r'(?<=[.!?])\s+', t)
    return [p.replace(_DOT, ".") for p in parts]


def analyze(pdf_path, maxxref):
    doc = pymupdf.open(pdf_path)
    if doc.needs_pass:
        doc.authenticate("")
    pages_text = []
    for pg in doc:
        pages_text.append(pg.get_text("text"))
    npages = len(pages_text)
    doc.close()

    # 附录起始页
    appx_page = None
    for i, t in enumerate(pages_text, 1):
        for ln in t.splitlines():
            if APPX_RE.match(ln.strip()) and len(ln.strip()) < 40:
                appx_page = i
                break
        if appx_page:
            break

    # 章节
    sections = []
    for i, t in enumerate(pages_text, 1):
        for ln in t.splitlines():
            m = SEC_RE.match(ln.strip())
            if m and len(m.group(2).split()) <= 6:
                sections.append({"num": m.group(1), "title": m.group(2).strip(), "page": i})

    # 题注（去重：同一 label 取首次出现）
    seen, exhibits = set(), []
    for i, t in enumerate(pages_text, 1):
        for ln in t.splitlines():
            m = CAP_RE.match(ln.strip())
            if not m:
                continue
            label = norm(m.group(1), m.group(2))
            if label in seen:
                continue
            seen.add(label)
            is_appx = bool(re.match(r'^[A-Z]', m.group(2))) or (appx_page and i >= appx_page)
            kind = "figure" if label.lower().startswith("fig") else "table"
            exhibits.append({"label": label, "kind": kind, "page": i,
                             "title": m.group(3).strip()[:90], "appendix": bool(is_appx),
                             "xrefs": []})

    # 交叉引用句（归到对应 exhibit）
    bylabel = {e["label"]: e for e in exhibits}
    for t in pages_text:
        for sent in split_sentences(t):
            for label in extract_xref_labels(sent):
                e = bylabel.get(label)
                if e is None:
                    continue
                s = sent.strip()
                # 排除题注本身（句子以 label 开头且很短）
                if s.startswith(e["label"]) and len(s) < 120:
                    continue
                if 15 < len(s) < 320 and s not in e["xrefs"]:
                    e["xrefs"].append(s)

    exhibit_pages = sorted({e["page"] for e in exhibits})
    return {"file": os.path.basename(pdf_path), "pages": npages, "appendix_page": appx_page,
            "sections": sections, "exhibits": exhibits, "exhibit_pages": exhibit_pages}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdfs", nargs="+")
    ap.add_argument("--json", default="exhibit_map.json")
    ap.add_argument("--maxxref", type=int, default=2, help="stdout 每图表最多打印几句 xref")
    ap.add_argument("--allow-empty", action="store_true",
                    help="允许没有有效 PDF 结果时仍返回 0；不会掩盖缺失文件或处理错误")
    args = ap.parse_args()

    paths = []
    for pat in args.pdfs:
        hits = glob.glob(pat)
        if hits:
            paths.extend(hits)
        elif glob.has_magic(pat):
            print(f"[empty] 通配符未匹配任何 PDF：{pat}")
        else:
            paths.append(pat)

    results = []
    failures = 0
    for p in paths:
        if not os.path.isfile(p):
            print(f"[skip] {p}")
            failures += 1
            continue
        try:
            results.append(analyze(p, args.maxxref))
        except Exception as e:
            print(f"[ERR] {p}: {e}")
            failures += 1

    if not results and not args.allow_empty:
        print("[ERR] 没有生成任何有效 PDF 分析结果；若这是预期结果，请显式加 --allow-empty。")
        return 1

    # 紧凑 stdout
    tot_t = tot_f = tot_appx = 0
    for r in results:
        nt = sum(1 for e in r["exhibits"] if e["kind"] == "table")
        nf = sum(1 for e in r["exhibits"] if e["kind"] == "figure")
        na = sum(1 for e in r["exhibits"] if e["appendix"])
        tot_t += nt; tot_f += nf; tot_appx += na
        print(f"\n=== {r['file'][:30]} | {r['pages']}p | tables={nt} figs={nf} appx={na}"
              f" | appendix@p{r['appendix_page']} ===")
        print("  sections:", " · ".join(f"{s['num']} {s['title']}(p{s['page']})"
                                         for s in r["sections"][:12]))
        print("  exhibit-pages:", r["exhibit_pages"])
        for e in r["exhibits"]:
            tag = "APPX" if e["appendix"] else "main"
            print(f"  [{e['label']:>9}|p{e['page']:<3}|{tag}|{e['kind'][:3]}] {e['title']}")
            for s in e["xrefs"][:args.maxxref]:
                print(f"        ‣ {s}")
    print(f"\n# TOTneeds: papers={len(results)} tables={tot_t} figs={tot_f} appendix={tot_appx}")

    with open(args.json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print(f"# JSON 全量明细 → {os.path.abspath(args.json)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
