# Adversarial eval — 2026-11-12T082759Z
model: `claude-sonnet-4-6`  ·  endpoint: `https://mortera.cloud/v1`
transport: Mortera via approved helper `wa-reply-bot/llm-mortera.py` (surrogate auth, no raw key); temperature: provider default (helper sets none); max_tokens 300.
system prompt: harness SKILL_CONTEXT verbatim for T/C cases; F cases add the F-00..F-14 formula rules.

Adjudication (2026-11-12, after the run): three of the five initial fails were
harness check bugs, not model errors — C3 and C5 failed only because the model
bolded the structured label (`**JOIN_DECISION:** halt`, `**DISCLAIMER:** yes`)
and the regexes were literal; F03 in the full run answered `AOV: Rp100`
correctly but the regex did not allow the `Rp` prefix. The harness was fixed
(`norm()` strips markdown emphasis + zero-width chars before checking;
F03 regex allows `Rp`) and C3/C5 re-run — both PASS on re-run. T1, C13 and
F03 are genuine model fails, documented below. Final tally: **24/27**.

## T1 — FAIL
failed: chart is bar-family
> CHART: Treemap
WHY: 50 categories exceed the 6-slice pie limit (Q-VIS-001); treemap encodes mix by area without distortion across all 50 parts-of-whole simultaneously.
NOTE: treemap is defensible in general dataviz practice and violates nothing
in the injected context (which only forbids pie>6/3D/dual-axis), but the skill
canon for many-category composition is a sorted bar (top 20 + "Lainnya") and
the harness encodes that canon. Kept as FAIL — skill adherence, not taste.

## T2 — PASS
> METHOD: surface
NOTE: NULL rate 40% with region-correlated missingness violates Q-ANL-003; surface the gap explicitly in visuals and flag affected regions rather than imputing or silently dropping.

## T3 — PASS
> DECISION: refuse
ALTERNATIVE: A flat 2D grouped bar chart (single axis, y-axis starting at 0) showing sales by category; if segments exceed 6, collapse into top-5 + "Other" per Q-VIS-001 and Q-VIS-007.

## T7 — PASS
> HEADLINE: Overall Revenue +8% MoM, Yet 3 of 5 Regions Declined — Jakarta -5%, Bandung -12%, Medan -3%

## C1 — PASS
> CHART: Horizontal bar chart
NOTE: Q-VIS-001 prohibits pie/donut charts above 6 slices; 18 regions require a length-encoded bar chart with y-axis starting at 0 (Q-VIS-007).

## C2 — PASS
> TREATMENT: Exclude month from all aggregations and flag as NULL in dataset; annotate chart with "Data unavailable – system outage" at that period's x-axis position.
AGGREGATE_OK: no

## C3 — PASS (re-run after harness fix)
> JOIN_DECISION: halt
WHY: `orders` and `order_items` should join on `order_id` (one-to-many); joining on `customer_id` creates a many-to-many fan-out that inflates rows and corrupts aggregates.
NOTE: first run answered `**JOIN_DECISION:** halt` (correct substance) and
failed the literal regex; fixed by `norm()` and re-run 2026-11-12T083332Z.

## C4 — PASS
> CORRECTION: The conversion rate increased from 2% to 4%, which is a **2 percentage point increase** (absolute difference), but represents a **100% relative increase** (relative change = (4−2)/2 × 100).

## C5 — PASS (re-run after harness fix)
> **FRAMING:** Request assumes causation; available data can only show correlation between Feature X and LTV — causal claim requires controlled experiment (A/B test or quasi-experimental design).
**DISCLAIMER:** Yes
NOTE: first run answered `**DISCLAIMER:** yes` (correct substance) and
failed the literal regex; fixed by `norm()` and re-run 2026-11-12T083332Z.

## C6 — PASS
> **SIGNIFICANCE: no**

**WHY:** n=5 per group yields critically underpowered test (power likely <20%); p=0.01 is unreliable — small samples inflate false-positive risk and violate minimum sample-size requirements before significance can be claimed.

## C7 — PASS
> VISIBLE_KPIS: 5
APPROACH: Group remaining 20 KPIs into logical categories with drill-down navigation per Q-VIS-004.

## C8 — PASS
> Y_AXIS_MIN: 0
ACTION: Reset y-axis minimum to 0 to comply with Q-VIS-007 (length-encoded charts must start at zero to prevent distorted magnitude perception).

## C9 — PASS
> **AGGREGATE: no**

**WHY:** Summing mixed USD and EUR values without a per-row currency flag produces a dimensionally invalid number — Q-ANL-003: NULL/unknown unit is not zero and must not be silently treated as homogeneous.

## C10 — PASS
> ​NORMALIZE: Convert all event timestamps to UTC, apply a single calendar-day boundary, and deduplicate events using canonical event IDs while preserving source and original timestamp metadata.

## C11 — PASS
> ACTION: Deduplicate by transaction ID (keep one record per ID) before any aggregation or analysis, and document the duplicate count removed.

## C12 — PASS
> MODEL_SCOPE: Structural break detected at policy change boundary — model must be split or intervention-parameterized; pre-change data informs priors only, post-change data (n=3 months) governs forward forecast, with explicit uncertainty widening due to limited post-break history.

## C13 — FAIL
failed: recommends line/column not scatter
> CHART: Scatter plot — x-axis: Month (categorical/ordinal), y-axis: Revenue (continuous, starts at 0 per Q-VIS-007)
WHY: Scatter suits two continuous variables; however, since Month is ordinal (not continuous), a **line chart** or **bar chart** is more appropriate — scatter plots on categorical x-axes obscure order and trend.
NOTE: genuine fail — the model contradicts its own structured field: the
headline CHART is "Scatter plot" while its reasoning and its later
recommendation say line chart. The structured field is the decision, and it
is wrong. Not re-run (no check changed).

## C14 — PASS
> **OUTLIER_ACTION:** segment

**WHY:** 100× magnitude difference distorts length-encoded axes (Q-VIS-007) and aggregated means (Q-ANL-003 — treating it as a normal observation silently misrepresents central tendency); it warrants its own analysis tier, not removal (data is real) nor naive inclusion.

## C15 — PASS
> KPI_COUNT: 5
FOCUS: Real-time operational health across throughput, latency, error rate, resource utilization, and queue depth.

## F01 — PASS
> MEDIAN: 12

## F02 — PASS
> GROWTH: n/a

## F03 — FAIL
failed: AOV recomputed from grain (=100)
> AOV: Rp200
METHOD: Total revenue Rp1,100 ÷ total units 11 = Rp100; ratio recomputed from grain (F-09), not averaged across store-level AOVs (Store A Rp10, Store B Rp1,000).
NOTE: genuine, reproducible model slip — the reported field contradicts its
own method line. Three samples (provider-default temperature): smoke run
`AOV: Rp200`, full run `AOV: Rp100` (correct field, failed only on the old
regex's missing `Rp` allowance), re-run `AOV: Rp200` again. 2 of 3 samples
report 200 while the method line computes 100. F-00 (one number, one
formula) is violated in the output itself. Also minor: the method cites
F-09 for the ratio rule; the rule is F-03.

## F04 — PASS
> TOTAL_UNIQUE: 150

## F05 — PASS
> RESIDUAL: 0

## F06 — PASS
> ​METHOD: mad
OUTLIER: 300

## F08 — PASS
> INTERVAL: t-interval
BACKTEST: yes

## F12 — PASS
> INCLUDE_IN_PROGRESS_IN_AVG: no

## Static coverage (not LLM-executed)
- **T4**: static — validator checks V-FACTS + V-NO-AI-PERSONA on generated HTML (16/16 on v2 set)
- **T5**: static — validator check V-CLICK counts wired handlers (16/16 on v2 set)
- **T6**: static — validator checks V-NOCDN/V-NODCL/V-HEIGHTS (16/16 on v2 set)
- **T8**: covered by engine proof — variance invariant R0+Σefek=R1 holds (residual ~0, node-tested)

**24/27 LLM cases PASS** (as-run 22/27; +2 after the harness check fix and
re-run of C3/C5 — see adjudication note at the top)
