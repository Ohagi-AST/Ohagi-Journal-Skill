#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI 退出码测试：缺失输入严格失败，空通配需显式 --allow-empty。"""
import os
import subprocess
import sys
import tempfile
import unittest

import _paths


def run_script(name, *args, cwd):
    script = os.path.join(_paths.SCRIPTS, name)
    return subprocess.run(
        [sys.executable, script, *args],
        cwd=cwd,
        text=True,
        encoding="utf-8",
        capture_output=True,
    )


class TestCliFailureModes(unittest.TestCase):
    def test_pdf_to_png_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as d:
            proc = run_script("pdf_to_png.py", "missing.pdf", cwd=d)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("找不到", proc.stdout)

    def test_pdf_to_png_empty_glob_requires_allow_empty(self):
        with tempfile.TemporaryDirectory() as d:
            proc = run_script("pdf_to_png.py", "*.nope.pdf", cwd=d)
            ok = run_script("pdf_to_png.py", "*.nope.pdf", "--allow-empty", cwd=d)
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)

    def test_exhibit_map_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as d:
            proc = run_script("exhibit_map.py", "missing.pdf", cwd=d)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("[skip]", proc.stdout)

    def test_exhibit_map_empty_glob_requires_allow_empty(self):
        with tempfile.TemporaryDirectory() as d:
            proc = run_script("exhibit_map.py", "*.nope.pdf", cwd=d)
            ok = run_script("exhibit_map.py", "*.nope.pdf", "--allow-empty", cwd=d)
            self.assertTrue(os.path.isfile(os.path.join(d, "exhibit_map.json")))
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)


if __name__ == "__main__":
    unittest.main()
