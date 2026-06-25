#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
smoke_test.py — scripts/ 工具链 Python 侧的最小可用路径冒烟测试。

跑通即证明三件核心工具能 import 且跑出合理产物：
  - exhibit_map.split_sentences   句子分割（缩写保护）
  - zh_glyph_check.scan           中文残留字形检测
  - exhibit_render.render_table   三线表片段（+ 若装了 matplotlib，再出一张图）

用法： python tests/smoke_test.py      # 退出码 0 = 全绿
"""
import os
import sys
import tempfile

import _paths  # noqa: F401


def check(cond, msg):
    mark = "[OK]" if cond else "[FAIL]"
    print(f"  {mark} {msg}")
    return cond


def main():
    ok = True
    print("# smoke_test: scripts/ 工具链最小路径")

    import exhibit_map
    parts = exhibit_map.split_sentences("As Fig. 3 shows, it holds. Next point here.")
    ok &= check(len(parts) == 2 and "Fig. 3" in parts[0],
                f"exhibit_map.split_sentences → {len(parts)} 句，缩写未误断")

    import zh_glyph_check
    hits = list(zh_glyph_check.scan(["經濟發展"]))
    ok &= check(len(hits) == 3, f"zh_glyph_check.scan('經濟發展') → {len(hits)} 处残留（期望 3）")
    ok &= check(list(zh_glyph_check.scan(["経済発展"])) == [],
                "zh_glyph_check.scan 对正宗日文零误报")

    import exhibit_render
    tex = exhibit_render.render_table(
        [{"title": "(1)", "coefs": {"Treat": (0.083, 0.041, 0.043)}, "stats": {"N": 1240}}],
        stats=("N",))
    ok &= check(all(x in tex for x in (r"\toprule", r"\bottomrule", "0.083**", "1,240"))
                and "|" not in tex,
                "exhibit_render.render_table → booktabs 三线表、有星号、无竖线")

    # 可选：装了 matplotlib 才测图。
    try:
        import matplotlib  # noqa: F401
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "cp.pdf")
            exhibit_render.render_coefplot([("Treat", 0.075, 0.038)], using=out, ci="se")
            ok &= check(os.path.isfile(out) and os.path.getsize(out) > 0,
                        "exhibit_render.render_coefplot → 出 PDF")
    except ImportError:
        print("  [SKIP] matplotlib 未装，跳过图渲染（render_table 不受影响）")

    print("# 结果：", "全绿 ✅" if ok else "有失败 ❌")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
