# Layered QA Matrices

Five layers, executed in order. A layer's CRITICAL failure blocks all later layers.
Check IDs cross-reference `qa-and-critique-engine.md`. The `Auto` column marks
checks enforceable by `validator/apex_validate.py` (static) — the rest are manual.

## Layer 1 — DATA (grain & integrity)

| Check | Verify | Fail condition | Severity | Auto |
|---|---|---|---|---|
| Q-DATA-001 | Schema matches declared grain | Unexpected/missing columns | CRITICAL | – |
| Q-DATA-002 | NULL count per column, missingness mechanism | Silent imputation of MNAR data | CRITICAL | – |
| Q-DATA-003 | Row-key uniqueness | Duplicate keys at declared grain | CRITICAL | – |
| Q-DATA-004 | Single grain per aggregation | Mixed grains summed together | CRITICAL | – |
| Q-DATA-005 | Join fan-out audit (row counts before/after) | Cartesian explosion | CRITICAL | – |
| Q-DATA-007 | Single currency / unit per measure | Summing mixed currencies or units | MAJOR | – |
| Q-DATA-008 | Single timezone before date grouping | Grouping across mixed timezones | MAJOR | – |
| Q-DATA-011 | Outlier treatment logged | Blind deletion of outliers | MAJOR | – |

## Layer 2 — CALCULATION (formulas)

| Check | Verify | Fail condition | Severity | Auto |
|---|---|---|---|---|
| Q-CALC-002 | Denominators keep legitimate zeros | Dropping zero-denominator rows | CRITICAL | – |
| Q-CALC-003 | Only additive measures are summed | Averaging ratios, summing percentages | CRITICAL | – |
| Q-CALC-005 | % change vs percentage points distinguished | "2% → 4% is a 2% increase" | MAJOR | – |
| Q-CALC-006/007 | Weighted averages with explicit weights | Averaging averages unweighted | MAJOR | – |
| INVARIANT | Reconciliation: components sum to total (e.g. waterfall Δ = Σ effects, residual ≈ 0) | Residual ≠ 0 unexplained | CRITICAL | – |

## Layer 3 — VISUAL (grammar & rendering)

| Check | Verify | Fail condition | Severity | Auto |
|---|---|---|---|---|
| Q-VIS-000 | Matches README baseline density/palette | Wrong colors, sparse layout, missing fact panel | FATAL | ✓ |
| Q-VIS-002 | Bar charts start y at 0 | Truncated baseline | CRITICAL | – |
| Q-VIS-005 | Pie/donut ≤ 7 categories | 18-slice pie | MAJOR | – |
| Q-VIS-007/008 | Token palette, no sole red/green encoding | Neon/rainbow, color-only encoding | MAJOR | ✓ |
| Q-VIS-FATAL | Zero external requests; no DOMContentLoaded wrapper; hardcoded px chart heights | Blank render in sandboxed viewers | FATAL | ✓ |

## Layer 4 — DESIGN (layout & interaction)

| Check | Verify | Fail condition | Severity | Auto |
|---|---|---|---|---|
| Q-VIS-HEADER-SLICER | Sticky header slicer, all dimensions, chips, Reset | Filters hidden in menus; missing chip/reset | MAJOR | ✓ |
| Q-VIS-CROSS-FILTER | Every dimension-based viz clickable; toggle-off works | Dead charts; one-way filter | MAJOR | ✓ |
| DENSITY | Bento 12-col grid, no giant stacked charts | Full-width chart stack | MINOR | – |

## Layer 5 — STORY (claims)

| Check | Verify | Fail condition | Severity | Auto |
|---|---|---|---|---|
| Q-STORY-001 | Every headline traceable to a computed number | Headline exceeds evidence | CRITICAL | ✓ |
| Q-STORY-003 | No causal language on observational data | "menyebabkan", "causes", "drives" | CRITICAL | ✓ |
| Q-STORY-004 | No cherry-picked time windows | Timeline starts at a trough | MAJOR | – |
| FACTS-PANEL | Every fact shows its formula/rule; no AI persona | Narrative "AI analysis" without formula | FATAL | ✓ |

## Execution rule

Run layers 1→5 in order. Any CRITICAL/FATAL failure stops the release —
fix, re-verify the failed layer fully, then continue. A fix without
re-verification is NOT VERIFIED.
