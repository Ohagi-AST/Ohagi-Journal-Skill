#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""journal-drafting 的语义接口与安全护栏守卫测试。"""
import os
import re
import unittest

import _paths


SKILL = os.path.join(_paths.DRAFTING, "SKILL.md")
MASTER = os.path.join(_paths.DRAFTING, "template-master-framework.md")
EVALS = os.path.join(_paths.REPO, "evals", "test-cases.md")
OPENAI_YAML = os.path.join(_paths.DRAFTING, "agents", "openai.yaml")


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


class TestSkillInterface(unittest.TestCase):
    def test_frontmatter_has_only_name_and_description(self):
        text = _read(SKILL)
        parts = text.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, "SKILL.md 缺 YAML frontmatter")
        keys = set(re.findall(r"^([A-Za-z0-9_-]+):", parts[1], re.MULTILINE))
        self.assertEqual(keys, {"name", "description"})

    def test_two_level_routing_six_shortcuts_and_upgrade_boundary(self):
        text = _read(SKILL)
        for letter in "ABCDEF":
            self.assertIn(f"**({letter})", text)
        self.assertIn("两层路由", text)
        self.assertIn("完整成稿主流程", text)
        self.assertIn("局部/专项任务", text)
        self.assertIn("局部/专项任务面板（C–F）", text)
        self.assertIn("不要为了层级再多问一次", text)
        self.assertIn("等用户确认", text)
        self.assertIn("转 A/B", text)

    def test_new_references_are_directly_routed(self):
        text = _read(SKILL)
        refs = (
            "en-section-playbooks.md",
            "en-identification-strategies.md",
            "en-empirical-standards.md",
            "en-submission-workflows.md",
        )
        for ref in refs:
            self.assertRegex(text, rf"\]\(references/{re.escape(ref)}\)")

    def test_openai_metadata(self):
        text = _read(OPENAI_YAML)
        self.assertIn('display_name: "Journal Drafting"', text)
        self.assertIn("$journal-drafting", text)
        self.assertIn("allow_implicit_invocation: true", text)


class TestSemanticGuardrails(unittest.TestCase):
    def test_full_spec_persists_method_and_reproducibility(self):
        text = _read(MASTER)
        required = (
            "paper_type", "method_family", "primary estimand",
            "主要识别策略 / 辅助识别策略", "关键推断风险",
            "外部有效性对象与边界", "PAP / 预注册状态",
            "数据访问与复现状态",
        )
        for token in required:
            self.assertIn(token, text)

    def test_core_safety_contract_remains(self):
        text = _read(SKILL) + "\n" + _read(MASTER)
        for token in (
            "主张强度 ≤ 识别强度", "绝不编", "【待核】",
            "【作者补", "不编造投稿政策", "官方要求",
        ):
            self.assertIn(token, text)

    def test_unsafe_upstream_rules_are_not_operational(self):
        paths = [SKILL, MASTER]
        paths.extend(
            os.path.join(_paths.REFERENCES, fn)
            for fn in os.listdir(_paths.REFERENCES)
            if fn.endswith(".md")
        )
        text = "\n".join(_read(path) for path in paths).lower()
        for phrase in (
            "supply a defensible illustrative value",
            "ready for top-5 submission",
            "contains at least one parenthetical aside",
        ):
            self.assertNotIn(phrase, text)

    def test_skill_and_long_reference_size_contract(self):
        self.assertLess(len(_read(SKILL).splitlines()), 500)
        for dp, _, fns in os.walk(_paths.REFERENCES):
            for fn in fns:
                if not fn.endswith(".md"):
                    continue
                path = os.path.join(dp, fn)
                text = _read(path)
                if len(text.splitlines()) > 100:
                    self.assertIn("## 目录", text, os.path.relpath(path, _paths.REPO))


class TestEvaluationCorpus(unittest.TestCase):
    def test_cases_have_prompt_expected_forbidden(self):
        text = _read(EVALS)
        cases = re.split(r"(?m)^## (E\d{2})[^\n]*\n", text)
        ids = cases[1::2]
        bodies = cases[2::2]
        self.assertEqual(ids, [f"E{i:02d}" for i in range(1, 16)])
        self.assertEqual(len(ids), len(bodies))
        for case_id, body in zip(ids, bodies):
            for heading in ("### Prompt", "### Expected", "### Forbidden"):
                self.assertIn(heading, body, f"{case_id} 缺 {heading}")


if __name__ == "__main__":
    unittest.main()
