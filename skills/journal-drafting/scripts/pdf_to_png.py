#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf_to_png.py — 把 PDF（含加密/权限锁）渲染成 PNG，供「亲眼看图表」的视觉闭环。

为什么要它：本套写作框架原来的语料管线（journal-adapt 用 MinerU）只把 PDF 转成文字，
从没"看"过一张表的样子——三线表 vs 九宫格这种纯视觉差异，文字流根本察觉不到，
于是出过"九宫格冒充三线表"的低级错误。本工具把页面渲染成 PNG，让 agent 用 Read 工具
真正看见表/图，用于：① 扫 EER+顶刊学可见 house-style；② 渲染我们自己的表后视觉自检。

为什么用 PyMuPDF：很多期刊 PDF（Elsevier 等）带 owner-password 权限锁，原生读图工具直接拒收。
PyMuPDF 能打开这类锁（空用户口令）并直接渲染成高清 PNG，一个依赖搞定"去锁 + 栅格化"。

设计原则：
- 只读输入 PDF，只写输出 PNG，不改原文件。
- owner-password（仅限制复制/打印、无开档口令）自动 authenticate("") 放行；
  真正需要开档口令的（needs_pass）会明确报错，不静默失败。
- 1-indexed 页码（和人类/PDF 阅读器一致），内部转 0-indexed。

用法:
    python3 pdf_to_png.py paper.pdf                      # 全部页 → ./_exhibit_images/paper/
    python3 pdf_to_png.py paper.pdf --pages 10-15        # 仅第10–15页
    python3 pdf_to_png.py paper.pdf --pages 12,14,20-22  # 混合：单页+区间
    python3 pdf_to_png.py paper.pdf --dpi 200 --out outdir
    python3 pdf_to_png.py *.pdf --pages 1-8              # 多篇批量（各自子目录）
"""
import argparse, os, sys, glob

# Windows 控制台/管道默认 GBK：输出 ✅/⚠️ 及中文路径会 UnicodeEncodeError → 强制 UTF-8。
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

try:
    import pymupdf  # PyMuPDF >= 1.24 暴露 `pymupdf`
except ImportError:
    try:
        import fitz as pymupdf  # 旧名
    except ImportError:
        sys.exit("[!] 缺 PyMuPDF：先跑  pip install pymupdf")


def parse_pages(spec, n_pages):
    """'12,14,20-22' / '10-15' / 'all' → 排序去重的 1-indexed 页码列表（裁到 [1,n]）。"""
    if spec is None or spec.lower() == "all":
        return list(range(1, n_pages + 1))
    out = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            a, b = int(a), int(b)
            out.update(range(min(a, b), max(a, b) + 1))
        else:
            out.add(int(part))
    return [p for p in sorted(out) if 1 <= p <= n_pages]


def render_one(pdf_path, pages_spec, dpi, out_root):
    stem = os.path.splitext(os.path.basename(pdf_path))[0]
    out_dir = os.path.join(out_root, stem)
    os.makedirs(out_dir, exist_ok=True)

    doc = pymupdf.open(pdf_path)
    # owner-password 权限锁：needs_pass 通常为 False（可直接渲染）；若 True 先试空口令。
    if doc.needs_pass:
        if not doc.authenticate(""):
            # 真正的 user-password（开档口令）加密：空口令进不去，PyMuPDF 也无能为力。
            # 区别于 owner-password（仅限制复制/打印，空口令即可放行）——后者不会走到这里。
            print(f"[!] {stem}: 这是 user-password（开档口令）加密的 PDF，空口令无法打开，已跳过。")
            print( "    这不是 owner-password 权限锁（那种本工具能自动去锁），而是真正的开档加密。")
            print( "    出路（任选其一）：")
            print(f"      1) 拿到口令后手动解密：qpdf --password=<PW> --decrypt \"{pdf_path}\" out.pdf，再对 out.pdf 跑本工具；")
            print( "      2) 从期刊官网/机构库下载未加密的正式版（投稿/出版版通常不加开档口令）；")
            print( "      3) 若你有合法访问权，用阅读器另存/打印成无密码 PDF 后再处理。")
            doc.close()
            return None

    pages = parse_pages(pages_spec, doc.page_count)
    written = 0
    for p in pages:
        page = doc.load_page(p - 1)  # 0-indexed
        pix = page.get_pixmap(dpi=dpi)
        out_png = os.path.join(out_dir, f"{stem}_p{p:03d}.png")
        pix.save(out_png)
        written += 1
    doc.close()
    print(f"[OK] {stem}: 渲染 {written} 页 @ {dpi}dpi → {out_dir}")
    return written


def main():
    ap = argparse.ArgumentParser(description="PDF（含加密）→ PNG，供视觉读图")
    ap.add_argument("pdfs", nargs="+", help="PDF 路径（可多个 / 通配）")
    ap.add_argument("--pages", default="all", help="页码：'all' | '10-15' | '12,14,20-22'（1-indexed）")
    ap.add_argument("--dpi", type=int, default=180, help="渲染 dpi（默认 180；表格细节可 200–250）")
    ap.add_argument("--out", default="_exhibit_images", help="输出根目录（默认 ./_exhibit_images）")
    ap.add_argument("--allow-empty", action="store_true",
                    help="允许没有渲染出任何页面时仍返回 0；不会掩盖缺失文件或处理错误")
    args = ap.parse_args()

    # 展开通配（Windows shell 不一定展开）
    paths = []
    for pat in args.pdfs:
        hits = glob.glob(pat)
        if hits:
            paths.extend(hits)
        elif glob.has_magic(pat):
            print(f"[empty] 通配符未匹配任何 PDF：{pat}")
        else:
            paths.append(pat)

    total = 0
    failures = 0
    for pdf_path in paths:
        if not os.path.isfile(pdf_path):
            print(f"[skip] 找不到：{pdf_path}")
            failures += 1
            continue
        try:
            written = render_one(pdf_path, args.pages, args.dpi, args.out)
            if written is None:
                failures += 1
            else:
                total += written
        except Exception as e:
            print(f"[ERR] {pdf_path}: {e}")
            failures += 1
    print(f"\n共渲染 {total} 张 PNG → {os.path.abspath(args.out)}")
    if failures:
        return 1
    if total == 0 and not args.allow_empty:
        print("[ERR] 没有渲染出任何页面；若这是预期结果，请显式加 --allow-empty。")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
