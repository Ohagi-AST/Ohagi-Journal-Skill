#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""zh_glyph_check.py 测试：检出中文残留字形、不误报中日同形字。"""
import os
import subprocess
import sys
import tempfile
import unittest
import _paths  # noqa: F401
import zh_glyph_check as z


class TestZh2Jp(unittest.TestCase):
    def test_no_same_glyph_entries(self):
        # 同形条目（键==值）必须已被剔除，否则会把中日同字误报为残留。
        for k, v in z.ZH2JP.items():
            self.assertNotEqual(k, v, f"残留同形条目 {k}")

    def test_known_mappings(self):
        self.assertEqual(z.ZH2JP.get("经"), "経")
        self.assertEqual(z.ZH2JP.get("發"), "発")
        self.assertEqual(z.ZH2JP.get("濟"), "済")


class TestScan(unittest.TestCase):
    def _hits(self, text):
        return list(z.scan(text.splitlines(keepends=True)))

    def test_detects_simplified_residue(self):
        # '经济' 是中文简体残留（日本应作 '経済'）。
        hits = self._hits("经济发展")
        chars = {h[2] for h in hits}
        self.assertIn("经", chars)
        self.assertIn("济", chars)
        self.assertIn("发", chars)

    def test_detects_traditional_residue(self):
        hits = self._hits("經濟發展")
        chars = {h[2] for h in hits}
        self.assertEqual(chars, {"經", "濟", "發"})  # '展' 中日同形，不报

    def test_clean_japanese_no_hits(self):
        # 正宗日本新字体写法，应零检出。
        self.assertEqual(self._hits("経済発展と政策"), [])

    def test_suggestion_payload(self):
        hits = self._hits("経済発展は重要だ。経済成長も。")
        self.assertEqual(hits, [])

    def test_hit_shape(self):
        # 每条命中应是 (line, col, ch, jp, ctx)。
        hits = self._hits("発")
        self.assertEqual(len(hits), 0)  # 発 已是日本写法
        hits = self._hits("发")
        self.assertEqual(len(hits), 1)
        line, col, ch, jp, ctx = hits[0]
        self.assertEqual((ch, jp), ("发", "発"))


class TestCli(unittest.TestCase):
    SCRIPT = os.path.join(_paths.SCRIPTS, "zh_glyph_check.py")

    def run_cli(self, *args, input_text=None):
        return subprocess.run(
            [sys.executable, self.SCRIPT, *args],
            input=input_text,
            text=True,
            encoding="utf-8",
            capture_output=True,
        )

    def test_fix_file_writes_fixed_copy(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "draft.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write("經濟發展")
            proc = self.run_cli(path, "--fix")
            fixed = os.path.join(d, "draft.fixed.txt")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(os.path.isfile(fixed))
            with open(fixed, encoding="utf-8") as f:
                self.assertEqual(f.read(), "経済発展")

    def test_fix_stdin_stdout_is_clean(self):
        proc = self.run_cli("-", "--fix", input_text="經濟發展\n")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, "経済発展\n")
        self.assertIn("检测到", proc.stderr)

    def test_fail_on_hit_returns_nonzero(self):
        proc = self.run_cli("-", "--fail-on-hit", input_text="經濟發展\n")
        self.assertEqual(proc.returncode, 1)


if __name__ == "__main__":
    unittest.main()
