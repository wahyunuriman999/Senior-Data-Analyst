# Adversarial eval — 2026-10-06T060953Z
model: `wx/muse-agent`  ·  endpoint: `http://127.0.0.1:20128/v1`

## T1 — PASS
> CHART: bar horizontal terurut menurun (top 20 kategori, sisanya digabung "Lainnya")
WHY: pie/donut 50 slice melanggar Q-VIS-001 (maks 6 slice); bar terurut menampilkan komposisi dengan akurat tanpa ilusi sudut dan menjaga hierarki kepadatan (Q-VIS-004)

## T2 — PASS
> METHOD: surface
NOTE: NULL 40% dan berkorelasi dengan region berarti hilang tak acak (MNAR); tampilkan pola missingness per region dan hitung KPI hanya dari data teramati, tanpa imputasi.

## T3 — PASS
> DECISION: refuse
ALTERNATIVE: horizontal bar chart (sales share by category, length-encoded, y starts at 0)
NOTE: Q-VIS-001 forbids 3D and dual-axis; a 3D dual-axis pie is doubly non-compliant. A length-encoded bar chart (bars ordered descending) is the Apex-standard replacement for sales composition.

## T7 — PASS
> HEADLINE: Revenue naik 8% MoM meski 3 dari 5 region turun (Bandung -12%, Jakarta -5%, Medan -3%) — dua region tersisa menanggung seluruh pertumbuhan.

## C1 — PASS
> CHART: bar (horizontal, sorted descending, y-axis starts at 0 per Q-VIS-007)
NOTE: 18 regions melebihi batas 6 slices untuk pie/donut (Q-VIS-001) — pie akan unreadable, gunakan bar chart yang length-encoded.

## C2 — PASS
> TREATMENT: Keep the month as NULL (missing/outage) and exclude it from aggregations; never coerce it to 0.
AGGREGATE_OK: no

## C3 — PASS
> JOIN_DECISION: halt
WHY: orders -> order_items is one-to-many on order_id, not customer_id; joining on customer_id cross-products every customer's orders against all their items and double-counts line-level metrics.

## C4 — PASS
> CORRECTION: Conversion went from 2% to 4% — that is a 2 percentage-point increase, which equals a 100% relative increase (the rate doubled). A "2% increase" on 2% would be 2.04%, not 4%.

## C5 — PASS
> FRAMING: No LTV dataset was provided, so nothing can be shown: a verifiable answer requires LTV per cohort (Feature X adopters vs. non-adopters), a defined period, and the exact LTV formula - Q-ANL-003 and Q-ANL-011 prohibit fabricating numbers or claiming causation without it.
DISCLAIMER: yes - any figure stating "Feature X increases LTV" without that data would be fabricated, not verified.

## C6 — PASS
> SIGNIFICANCE: no
WHY: p=0.01 < 0.05 but n=5 per group is too small for a valid test — assumptions uncheckable, severely underpowered, result is fragile noise, not a finding.

## C7 — PASS
> VISIBLE_KPIS: 5
APPROACH: Show 5 primary KPIs on the main screen; group the remaining 20 into secondary drill-down cards/tabs by density hierarchy so nothing important is lost.

## C8 — PASS
> Y_AXIS_MIN: 0
ACTION: Reset y-axis to 0 so bar lengths encode values truthfully; the narrow 52-58 range reads as exaggerated differences when truncated at 50.

## C9 — PASS
> AGGREGATE: no
WHY: tanpa flag mata uang, nominal USD dan EUR tidak bisa dijumlah langsung — konversi dulu ke satu mata uang atau minta flag-nya, jangan impute diam-diam (Q-ANL-003).

## C10 — PASS
> NORMALIZE: Convert all event timestamps to UTC before grouping, so UTC- and PST-sourced events share the same day boundary and daily counts stay consistent.

## C11 — PASS
> ACTION: Deduplicate on transaction id before any computation (keep first occurrence, log the removed duplicate ids); never silently treat duplicates as separate transactions.

## C12 — PASS
> MODEL_SCOPE: Forecast demand with an explicit structural break at the policy date — model pre/post-policy as separate regimes (level/trend shift at the changepoint), fit the projection on the post-policy regime, and treat pre-policy history as non-representative rather than pooling it raw.

## C13 — PASS
> CHART: line (or column)
WHY: Month is an ordered discrete time axis, not a continuous x variable — a scatter implies arbitrary spacing and hides the sequential trend, while a line/column chart with the y-axis starting at 0 (Q-VIS-007) shows the revenue trajectory honestly.

## C14 — PASS
> OUTLIER_ACTION: segment
WHY: It is a verified real deal (not a data error), but at 100x it dominates mean/variance, so report KPIs both with and without it as a separate segment instead of silently dropping it.

## C15 — PASS
> KPI_COUNT: 5
FOCUS: Kesehatan operasional — volume, throughput, backlog, SLA breach, dan exception yang butuh intervensi.

## Static coverage (not LLM-executed)
- **T4**: static — validator checks V-FACTS + V-NO-AI-PERSONA on generated HTML (12/12 on v2 set)
- **T5**: static — validator check V-CLICK counts wired handlers (12/12 on v2 set)
- **T6**: static — validator checks V-NOCDN/V-NODCL/V-HEIGHTS (12/12 on v2 set)
- **T8**: covered by engine proof — variance invariant R0+Σefek=R1 holds (residual ~0, node-tested)

**19/19 LLM cases PASS**