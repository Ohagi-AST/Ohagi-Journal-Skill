# Module Specifications

This file describes the public, implementation-neutral workflow. It avoids private directory names and manuscript-specific assumptions.

---

## Module 0 — Input Preparation

**Purpose:** make corpus and manuscript files readable by the agent.

### Inputs

- primary corpus: target-journal papers;
- optional secondary corpus: field-top or topic-similar papers;
- optional user/lab exemplars;
- manuscript file;
- optional static base writing skill.

### Accepted formats

- Markdown or plain text: preferred;
- PDF: allowed, but requires conversion;
- Word or LaTeX: convert relevant sections to Markdown before revision.

### Output

Readable Markdown/text files for corpus analysis and manuscript revision.

### Conversion gate

Every converted file must pass a readability check before style-card extraction:

- major sections are readable;
- section order is intact;
- equations, tables, citations, and technical terms are not badly corrupted.

If conversion is partial or failed, retry conversion, use another converter, ask the user for Markdown/text, or replace the paper. Partial and failed conversions do not enter Phase 1.

### Notes

MinerU is optional and only needed for PDF conversion. If PDF conversion fails, provide Markdown/text by another route.

---

## Module A — Corpus Setup

**Purpose:** record what each corpus file is for and decide whether to use an optional static base skill.

### Suggested metadata

```yaml
writing_destination: "Target journal or writing context"
primary_corpus:
  - id: target_001
    venue: "Target Journal"
    year: 2024
    relevance: "topic+method"
secondary_corpus:
  - id: field_001
    venue: "Field Top Journal"
    year: 2023
    relevance: "method"
user_exemplars:
  - id: exemplar_001
    source: "Advisor or lab writing sample"
    relevance: "style"
static_base_skill: "base_rules/economics.md"
```

If the user does not know which static base skill to choose, point them to `docs/STATIC_SKILL_RECOMMENDATIONS.md`. The static base skill is optional; users may skip it and rely on corpus-derived rules.

### Relevance tags

| Tag | Meaning |
|-----|---------|
| `topic+method` | Closest match to the manuscript's topic and method. |
| `topic` | Similar topic, different method. |
| `method` | Similar method, different topic. |
| `supplement` | Useful but lower weight. |

---

## Module B — Paper Style Card Extraction

**Purpose:** extract structural and rhetorical patterns from each corpus paper.

### Output

One Paper Style Card per corpus paper.

### Required boundary

Style cards must describe how the paper is written, not what the paper finds.

Allowed:

- "The introduction opens with an applied problem before narrowing to a modeling gap."
- "The contribution paragraph is explicit and appears before the roadmap."

Not allowed:

- direct quotes;
- paraphrased sentences;
- named results;
- copied statistics;
- paper-specific claims that reveal source content.

---

## Module C — Style Profile Aggregation

**Purpose:** aggregate paper-level cards into a writing profile.

### Pattern review

### Output

- target-journal profile;
- optional secondary-corpus profile;
- optional user/lab exemplar profile;
- conflict table;
- red flags;
- language register summary.

The profile should emphasize reviewed writing patterns rather than pseudo-statistical STRONG/WEAK labels. Users who want more confidence should add more high-quality corpus papers and review the patterns manually.

---

## Module D — Dynamic Writing Skill Generation

**Purpose:** turn the style profile and optional static base skill into an actionable temporary skill.

### Output

`dynamic_writing_skill.md`

### Required sections

1. priority rules;
2. target-journal patterns;
3. secondary-corpus signals, if any;
4. user/lab exemplar signals, if any;
5. static base skill defaults, if any;
6. section-specific guidance;
7. conflict resolutions;
8. cautions and conflicts;
9. language register calibration;
10. do-not-do list.

### Human gate

The user reviews the dynamic skill before manuscript revision begins.

---

## Module E — Manuscript Revision

**Purpose:** revise one manuscript section at a time.

### Inputs

- `dynamic_writing_skill.md`;
- current manuscript section;
- optional previous revision logs.

### Rounds

1. Diagnosis: identify style, logic, journal-fit, and AI-taste problems.
2. Revision: rewrite while preserving all P1 elements.
3. Revision log: explain what changed, which rules applied, and what was preserved.

### Output

```text
[manuscript_name]_revised/
├── dynamic_writing_skill.md
├── style_profile.md
├── [section]_revised.md
├── [section]_revision_log.md
└── revision_summary.md
```

---

## Module F — Rule Reuse

**Purpose:** identify rules that may be useful beyond the current manuscript.

### Output

`revision_summary.md` with rule candidates:

| Section | Paragraph | Rule candidate | Target |
|---------|-----------|----------------|--------|
| introduction | 3 | State contribution through the decision object rather than a generic literature claim. | dynamic-general |

The user decides whether candidates should become part of a future static base skill.
