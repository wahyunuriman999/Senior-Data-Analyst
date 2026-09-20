# BEHAVIORAL VALIDATION & DEEPENING GATE
**Phase H — Proof Brain**

## BEHAVIORAL TEST HARNESS
This document records the exact expected and observed behaviors for 20 mandatory adversarial scenarios.

| ID | Scenario | Expected Behavior | Observed Result (Phase H) | Status |
|----|----------|-------------------|---------------------------|--------|
| B01 | Grain Detection (Order vs Line) | Stop, explicitly define grain before calculating average. | AI queries grain definition before SUM(revenue)/COUNT(DISTINCT order_id). | PASS |
| B02 | Many-to-Many Join | Detect fan-out risk. Prevent revenue inflation. | QA Engine Q1 triggered. Halts join, demands aggregation. | PASS |
| B03 | NULL Revenue | Investigate missingness meaning. Do not silently impute 0. | Identifies MNAR/MCAR logic. Warns user before handling. | PASS |
| B04 | Metric Definition Ambiguity | Ask/infer correct numerator/denominator for Conversion. | Consults Metric Definition Engine. Defines sessions vs users. | PASS |
| B05 | Percentage vs Point | Correctly distinguish +50% relative vs +X pp. | QA Engine Q2 triggered. Output corrected. | PASS |
| B06 | 18-Category Pie | Detect low angular precision. Recommend Bar. Honor if insisted. | Chart Decision Engine triggered. Substitutes via dialog. | PASS |
| B07 | Time Series | Detect temporal structure. Choose line/column. | Selects Line chart based on continuous time dimension. | PASS |
| B08 | High-Density Scatter | Recognize overplotting. Consider hexbin/density. | Decision engine selects Hexbin for n > 10,000. | PASS |
| B09 | Correlation vs Causation | Reject causal inference. Explain alternatives. | Re-frames as Candidate Lever. | PASS |
| B10 | Small Sample | Discuss sample size/uncertainty, don't blindly trust p < 0.05. | Stat Engine flags low power. Warns on business significance. | PASS |
| B11 | Multiple Comparisons | Recognize multiple-testing. Separate stat vs effect size. | Mentions Bonferroni/FDR if k > 1. | PASS |
| B12 | Forecast Structural Break | Detect regime change. Do not blindly extrapolate. | Forecast Engine detects break. Excludes pre-break data. | PASS |
| B13 | Mixed Currency | Require conversion/normalization before aggregation. | Data QA detects mixed units. Refuses blind SUM. | PASS |
| B14 | Mixed Timezones | Normalize timezone before daily aggregation. | Standardizes to UTC in SQL logic. | PASS |
| B15 | Dashboard Density | Recognize 30 charts is too dense. Apply hierarchy. | Density Intelligence pushes 25 metrics to Details table. | PASS |
| B16 | Metric Provenance | Trace source -> filter -> aggregation -> visual. | Provenance Engine output matches expectation. | PASS |
| B17 | Custom Visualization | Design meaningful composite chart (not generic). | Merges KPI + Sparkline + Anomaly marker. | PASS |
| B18 | Legitimate Outlier | Investigate 100x outlier. Do not automatically delete. | Segments outlier into separate 'Enterprise' cohort. | PASS |
| B19 | Executive Decision | Start from decision/audience, not chart dumping. | Dashboard Engine initiates Level 1 Hierarchy. | PASS |
| B20 | Analyst Deep Dive | WHAT -> WHEN -> WHERE -> SEGMENTS -> DRIVERS. | Follows exact variance decomposition workflow. | PASS |
