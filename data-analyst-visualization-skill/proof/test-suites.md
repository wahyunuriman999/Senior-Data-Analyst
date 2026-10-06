# Comprehensive Test Suites

Each suite defines: **Input** → **Expected behavior** → **Pass criteria**.
Suites T1–T3 are the original core; T4–T8 extend coverage to the v2 mandates
(Fakta Terverifikasi, universal click-to-filter, zero-CDN rendering).

## T1 — High Cardinality
- **Input**: Dataset with 50 categories, request "show the mix".
- **Expected**: MUST reject pie/donut; output top-N Pareto bar + searchable table.
- **Pass**: Pie slices = 0; bar chart ≤ 12 bars + "Other" row; table has search input.

## T2 — Missing Data (MNAR)
- **Input**: Revenue column 40% NULL, missingness correlated with region.
- **Expected**: MUST NOT mean-impute; MUST surface the missingness pattern per segment.
- **Pass**: Output states mechanism + affected segments; no silent fill.

## T3 — Adversarial Chart Request
- **Input**: User requests "3D dual-axis pie chart".
- **Expected**: Refuse politely, name the violated rules (Q-VIS-001, Q-VIS-007),
  provide a superior alternative (grouped bar).
- **Pass**: No 3D/pie/dual-axis in output; alternative rendered with rationale.

## T4 — Fakta Terverifikasi Panel
- **Input**: Any dashboard generation task.
- **Expected**: Side panel where EVERY fact shows its formula/rule; no AI persona,
  no narrative sentences, no causal verbs.
- **Pass**: `validator/apex_validate.py` checks V-FACTS and V-NO-AI-PERSONA → PASS.

## T5 — Universal Click-to-Filter
- **Input**: Dashboard with bar, donut, trend, sankey, table.
- **Expected**: Clicking a bar/donut-slice/table-row/trend-point/sankey-node filters
  the whole dashboard; clicking again (or chip ✕ / Reset) restores.
- **Pass**: `validator` check V-CLICK counts ≥ 4 wired handlers; manual toggle test green.

## T6 — Zero-CDN Render
- **Input**: Generated HTML opened in a sandboxed viewer (no network).
- **Expected**: Fully rendered, no blank charts.
- **Pass**: `validator` checks V-NOCDN, V-NODCL, V-HEIGHTS → PASS; no `http` src/href.

## T7 — Simpson's Paradox Trap
- **Input**: Dataset where the aggregate trend reverses in 3 of 5 segments.
- **Expected**: MUST NOT headline the aggregate trend without the segment caveat.
- **Pass**: Output contains per-segment comparison before any aggregate claim.

## T8 — Invariant Reconciliation
- **Input**: Any dashboard with a waterfall/decomposition visual.
- **Expected**: Components sum to the total; residual ≈ 0 and SHOWN.
- **Pass**: Residual displayed; |residual| / |total| < 1e-6.

## Running the suites

Static suites (T4, T5, T6) run via `validator/apex_validate.py <file.html>`.
Behavioral suites (T1, T2, T3, T7, T8) require an LLM runtime — see
`proof/llm-validation/` for the execution protocol and recorded evidence.
