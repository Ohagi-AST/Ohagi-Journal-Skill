#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""exhibit_map.split_sentences 的句子分割测试：重点验证学术缩写不再误断句。"""
import unittest
import _paths  # noqa: F401  (注入 sys.path)
import exhibit_map as m


class TestSplitSentences(unittest.TestCase):
    def test_basic_split(self):
        s = "We find an effect. It is large. Robust too."
        self.assertEqual(m.split_sentences(s),
                         ["We find an effect.", "It is large.", "Robust too."])

    def test_fig_abbrev_not_split(self):
        # 原 bug：'Fig. 3' 会在 'Fig.' 后断开，导致交叉引用跨句、匹配不到。
        s = "As Fig. 3 shows, the trend is clear. The next point follows."
        parts = m.split_sentences(s)
        self.assertEqual(len(parts), 2)
        self.assertIn("Fig. 3", parts[0])

    def test_eg_ie_not_split(self):
        s = "Many drivers, e.g. price and income, matter. We test each."
        parts = m.split_sentences(s)
        self.assertEqual(len(parts), 2)
        self.assertIn("e.g. price", parts[0])

    def test_et_al_not_split(self):
        s = "Following Smith et al. 2020, we cluster. Results hold."
        parts = m.split_sentences(s)
        self.assertEqual(len(parts), 2)

    def test_table_xref_recoverable(self):
        # 关键回归测试：'Table 2.' 句末 + 正文里的 'Table 2' 交叉引用应能在一句内被 XREF_RE 命中。
        s = "Results appear in Table 2. Table 2 reports the baseline estimates clearly."
        parts = m.split_sentences(s)
        # 第二句完整含 'Table 2' → XREF_RE 能匹配
        hit = [p for p in parts if m.extract_xref_labels(p) and "reports" in p]
        self.assertTrue(hit, "交叉引用句应可被 XREF_RE 命中")

    def test_abbrev_period_restored(self):
        # 占位符必须被还原成真正的句点，不能泄漏 \x00。
        s = "See e.g. the appendix."
        for p in m.split_sentences(s):
            self.assertNotIn("\x00", p)
            self.assertIn("e.g.", " ".join(m.split_sentences(s)))


class TestXrefExtraction(unittest.TestCase):
    def test_plural_table_list(self):
        self.assertEqual(
            m.extract_xref_labels("Tables 1 and 2 report the baseline estimates."),
            ["Table 1", "Table 2"],
        )

    def test_lowercase_and_figure_list(self):
        self.assertEqual(
            m.extract_xref_labels("figures 1, 2, and 3 show the event-study path."),
            ["Fig. 1", "Fig. 2", "Fig. 3"],
        )

    def test_simple_range(self):
        self.assertEqual(
            m.extract_xref_labels("Tables 1-3 summarize the robustness checks."),
            ["Table 1", "Table 2", "Table 3"],
        )

    def test_caption_colon(self):
        cap = m.CAP_RE.match("Figure 2: Event-study estimates")
        self.assertIsNotNone(cap)
        self.assertEqual(m.norm(cap.group(1), cap.group(2)), "Fig. 2")
        self.assertEqual(cap.group(3), "Event-study estimates")


if __name__ == "__main__":
    unittest.main()
