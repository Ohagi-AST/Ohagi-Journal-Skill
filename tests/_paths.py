#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/_paths.py — 共享路径与 sys.path 注入，供各测试 import scripts/ 下模块。"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
DRAFTING = os.path.join(REPO, "skills", "journal-drafting")
SCRIPTS = os.path.join(DRAFTING, "scripts")
REFERENCES = os.path.join(DRAFTING, "references")

if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)
