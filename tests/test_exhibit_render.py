#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""exhibit_render.py 测试：星号约定 + booktabs 三线表片段（无竖线/九宫格）。"""
import unittest
import _paths  # noqa: F401
import exhibit_render as r


class TestStars(unittest.TestCase):
    def test_levels(self):
        self.assertEqual(r.stars(0.005), "***")  # <0.01
        self.assertEqual(r.stars(0.03), "**")    # <0.05
        self.assertEqual(r.stars(0.08), "*")     # <0.10
        self.assertEqual(r.stars(0.20), "")      # 不显著
        self.assertEqual(r.stars(None), "")

    def test_boundaries(self):
        # 阈值是严格小于。
        self.assertEqual(r.stars(0.01), "**")    # 0.01 不 < 0.01，落到 <0.05
        self.assertEqual(r.stars(0.05), "*")
        self.assertEqual(r.stars(0.10), "")


class TestRenderTable(unittest.TestCase):
    def setUp(self):
        self.models = [
            {"title": "(1)", "coefs": {"Treat": (0.083, 0.041, 0.043)},
             "stats": {"N": 1240, "R2": 0.21}},
            {"title": "(2)", "coefs": {"Treat": (0.075, 0.038, 0.048),
                                       "logGDP": (-0.190, 0.071, 0.008)},
             "stats": {"N": 1240, "R2": 0.34}},
        ]
        self.tex = r.render_table(self.models, depvar="log exports", stats=("N", "R2"))

    def test_booktabs_three_lines(self):
        for rule in (r"\toprule", r"\midrule", r"\bottomrule"):
            self.assertIn(rule, self.tex)

    def test_no_vertical_rules(self):
        # 三线表铁律：禁竖线/九宫格。列格式只能是 l + c*k，正文无 \hline。
        self.assertNotIn(r"\hline", self.tex)
        self.assertIn(r"\begin{tabular}{lcc}", self.tex)
        self.assertNotIn("|", self.tex)

    def test_stars_applied(self):
        # Treat 列1 p=0.043 → **；列2 p=0.048 → **；logGDP p=0.008 → ***。
        self.assertIn("0.083**", self.tex)
        self.assertIn("-0.190***", self.tex)

    def test_se_in_parentheses(self):
        self.assertIn("(0.041)", self.tex)

    def test_thousands_separator(self):
        self.assertIn("1,240", self.tex)

    def test_depvar_header(self):
        self.assertIn(r"\multicolumn{2}{c}{log exports}", self.tex)
        self.assertIn(r"\cmidrule(lr){2-3}", self.tex)

    def test_empty_models_raises(self):
        with self.assertRaises(ValueError):
            r.render_table([])

    def test_signote_constant(self):
        self.assertIn("p<0.10", r.SIGNOTE)
        self.assertIn("p<0.05", r.SIGNOTE)
        self.assertIn("p<0.01", r.SIGNOTE)


if __name__ == "__main__":
    unittest.main()
