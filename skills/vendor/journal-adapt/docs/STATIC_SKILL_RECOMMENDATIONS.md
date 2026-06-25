# Static Skill Recommendations

This page lists optional static writing skills that can be used as the base layer for journal-adapt.

These are recommendations, not requirements. Users can skip the static layer, choose one of the original GitHub projects below, or bring any custom `SKILL.md` / writing guide.

Last checked: 2026-05-15.

---

## How to Choose

| User situation | Good default |
|----------------|--------------|
| Economics paper | `hanlulong/econ-writing-skill` |
| ML / CV / NLP paper | `Master-cai/Research-Paper-Writing-Skills` |
| CS systems / networking / ML-style paper | `SNL-UCSB/paper-writing-skill` |
| Philosophy or interdisciplinary paper | `lishix520/academic-paper-skills` |
| Generic AI-writing cleanup | `blader/humanizer` |
| Advisor or lab has strong preferences | Fork or write your own static skill |

When unsure, use a general cleanup skill, bring your own writing guide, or skip the static layer. The dynamic corpus layer will still learn target-journal signals from your primary corpus.

---

## External Skills

| Skill | Developer / maintainer | Field or purpose | Best fit | Notes |
|-------|------------------------|------------------|----------|-------|
| [econ-writing-skill](https://github.com/hanlulong/econ-writing-skill) | `hanlulong` | Economics writing | Economics papers needing section-level guidance, identification strategy language, theory/model exposition, or referee-style review | Public Agent Skill for Claude Code and Codex; includes installation paths for both. |
| [Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | `Master-cai`; curated from Prof. Peng Sida's open notes | ML / CV / NLP paper writing | Abstract, introduction, method, experiments, conclusion, and self-review for ML-style papers | Includes Codex, Claude Code, and Gemini installation notes. |
| [paper-writing-skill](https://github.com/SNL-UCSB/paper-writing-skill) | SNL-UCSB / Arpit Gupta | Research paper writing, especially CS systems/networking and ML-adjacent papers | Structured pipeline: brainstorm, draft, evaluate, write, compress | MIT licensed; designed to be customized for an advisor or group. |
| [academic-paper-skills](https://github.com/lishix520/academic-paper-skills) | Li Shixiong (`lishix520`) | Philosophy and interdisciplinary academic papers | Planning and composing papers with quality gates and reviewer simulation | Provides separate strategist and composer skills. |
| [humanizer](https://github.com/blader/humanizer) | `blader` | Generic AI-writing cleanup | Removing AI-generated writing patterns while preserving meaning and tone | High-visibility general writing skill; useful as a cleanup-oriented static layer, not a substitute for field logic. |

---

## Suggested Selection Menu

When journal-adapt asks for a static base skill, a user-facing menu can look like this:

```text
Choose a static base skill, or skip:

1. Economics writing — hanlulong/econ-writing-skill.
2. ML / CV / NLP writing — Master-cai/Research-Paper-Writing-Skills.
3. CS / research paper writing — SNL-UCSB/paper-writing-skill.
4. Philosophy / interdisciplinary writing — lishix520/academic-paper-skills.
5. General AI-writing cleanup — blader/humanizer.
6. Custom file — provide a path to your own SKILL.md or writing guide.
7. None — rely only on corpus-derived dynamic rules.
```

Keep this menu optional. The project should never require users to install an external skill before using journal-adapt.

---

## Recommendation Policy

- Check the license and repository status before recommending any external skill in a formal release.
- Prefer skills that expose their source as `SKILL.md` or clear Markdown instructions.
- Prefer skills with transparent attribution and installation instructions.
- Do not copy external skill contents into this repository unless the license allows it and attribution is preserved.
- Treat external skills as user-selected inputs, not dependencies.
