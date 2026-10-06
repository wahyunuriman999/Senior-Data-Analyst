# Apex Validator

Machine-checkable compliance for the Apex dashboard standard.
Enforces the static (`Auto=✓`) checks from
`data-analyst-visualization-skill/quality/qa-matrices.md`.

## Usage

```bash
python3 validator/apex_validate.py <dashboard.html>          # human-readable
python3 validator/apex_validate.py <dashboard.html> --json   # machine-readable
```

Exit codes: `0` = all checks pass, `1` = any check fails, `2` = usage error.
Stdlib only — no dependencies.

## Checks

| ID | Reference | What it verifies |
|---|---|---|
| V-DARK | Q-VIS-000 | Dark background token `#0A0F1E` present |
| V-PALETTE | Q-VIS-007 | v2 semantic tokens used; v1 neon tokens absent |
| V-NOCDN | Q-VIS-FATAL | Zero external network-loading patterns |
| V-NODCL | Q-VIS-FATAL | No `DOMContentLoaded` wrapper |
| V-HEIGHTS | Q-VIS-FATAL | ≥ 4 hardcoded pixel chart heights |
| V-FACTS | FACTS-PANEL | Fact panel present, ≥ 3 formula/rule markers |
| V-NO-AI-PERSONA | FACTS-PANEL | No narrative AI persona |
| V-NOCAUSAL | Q-STORY-003 | No causal language on observational data |
| V-CLICK | Q-VIS-CROSS-FILTER | ≥ 4 wired click handlers |
| V-SLICER | Q-VIS-HEADER-SLICER | ≥ 3 selects, chips, reset, sticky bar |
| V-MONO | tokens.json | Monospace numeral stack |
| V-SSOT | Q-VIS-ANALYTICAL | SSOT marker + `.filter()` usage |

## Design note

The validator is intentionally static: it checks the artifact, not the author.
Behavioral suites (does the AI *choose* the right chart?) still need an LLM
runtime — see `data-analyst-visualization-skill/proof/llm-validation/`.
