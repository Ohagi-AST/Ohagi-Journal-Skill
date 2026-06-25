#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_rules_consistency.py — 跨文件元检查（不导入脚本，纯读文本）：

  1. 链接完整性：所有 .md 文件里提到的「内部 .md 引用」（references/XXX.md、
     母版/致谢相对链接、backtick 包住的 *.md）都必须在磁盘上真实存在。
     —— 这是文件改名（阶段一）的安全网：漏改一个交叉引用，这里立刻红。
  2. 术语一致性：显著性星号约定（p<0.10 / 0.05 / 0.01）全仓不许出现偏离阈值。
"""
import os
import re
import unittest
import _paths


# 运行时生成、或属于第三方子目录的产物——不是仓库里的源文件，跳过链接检查。
_GENERATED = {
    "dynamic_writing_skill.md", "style_profile.md", "paper_style_card.md",
    "journal_style_card.md", "revision_log.md", "skill.md",
}
# 只扫这些根（原创部分）；第三方 vendor/journal-adapt 等不在改名范围内。
_SCAN_ROOTS = [
    _paths.DRAFTING,
    os.path.join(_paths.REPO, "README.md"),
    os.path.join(_paths.REPO, "docs"),
]

_LINK_RE = re.compile(r"\]\(([^)]+\.md)(?:#[^)]*)?\)")        # [text](path.md)
_REF_RE = re.compile(r"references/[^\s`)\"'，。、]+?\.md")      # references/XXX.md
_BACKTICK_MD_RE = re.compile(r"`([^`\s]+\.md)`")               # `XXX.md`


def _iter_md_files():
    seen = set()
    for root in _SCAN_ROOTS:
        if os.path.isfile(root) and root.endswith(".md"):
            seen.add(os.path.abspath(root))
        elif os.path.isdir(root):
            for dp, _, fns in os.walk(root):
                for fn in fns:
                    if fn.endswith(".md"):
                        seen.add(os.path.abspath(os.path.join(dp, fn)))
    return sorted(seen)


def _candidate_refs(text):
    cands = set()
    for m in _LINK_RE.finditer(text):
        cands.add(m.group(1))
    for m in _REF_RE.finditer(text):
        cands.add(m.group(0))
    for m in _BACKTICK_MD_RE.finditer(text):
        cands.add(m.group(1))
    return cands


def _resolve(ref, from_dir):
    """ref 能否在磁盘上找到？相对 from_dir / journal-drafting / 仓库根 任一命中即可；
    纯文件名则在 journal-drafting 树下按 basename 搜。"""
    if ref.startswith(("http://", "https://")):
        return True
    base = os.path.basename(ref).lower()
    if base in _GENERATED:
        return True
    bases = [from_dir, _paths.DRAFTING, _paths.REPO]
    if "/" in ref or "\\" in ref:
        for b in bases:
            if os.path.isfile(os.path.normpath(os.path.join(b, ref))):
                return True
        return False
    # 裸文件名：先看同目录，再在 journal-drafting / docs 树里找同名文件
    if os.path.isfile(os.path.join(from_dir, ref)):
        return True
    for tree in (_paths.DRAFTING, os.path.join(_paths.REPO, "docs")):
        for dp, _, fns in os.walk(tree):
            if any(fn == ref for fn in fns):
                return True
    return False


class TestLinkIntegrity(unittest.TestCase):
    def test_all_internal_md_links_exist(self):
        broken = []
        for path in _iter_md_files():
            with open(path, encoding="utf-8") as f:
                text = f.read()
            from_dir = os.path.dirname(path)
            for ref in _candidate_refs(text):
                if not _resolve(ref, from_dir):
                    broken.append(f"{os.path.relpath(path, _paths.REPO)} → {ref}")
        self.assertFalse(
            broken,
            "发现指向不存在文件的内部引用（改名漏改？）：\n  " + "\n  ".join(sorted(broken)))


class TestTerminologyConsistency(unittest.TestCase):
    def test_significance_thresholds(self):
        # 全仓显著性星号阈值必须是 0.10 / 0.05 / 0.01；不许出现 0.1/0.5/0.001 等偏离写法。
        bad = []
        triple_re = re.compile(r"p\s*<\s*0\.\d+")
        allowed = {"0.10", "0.05", "0.01"}
        for dp, _, fns in os.walk(_paths.REPO):
            if ".git" in dp:
                continue
            for fn in fns:
                if not fn.endswith((".md", ".do", ".py")):
                    continue
                p = os.path.join(dp, fn)
                try:
                    with open(p, encoding="utf-8") as fh:
                        text = fh.read()
                except (OSError, UnicodeDecodeError):
                    continue
                for m in triple_re.finditer(text):
                    val = m.group(0).split("<")[-1].strip()
                    if val not in allowed:
                        bad.append(f"{os.path.relpath(p, _paths.REPO)}: {m.group(0)}")
        self.assertFalse(bad, "显著性阈值不一致：\n  " + "\n  ".join(bad))


if __name__ == "__main__":
    unittest.main()
