# ADVERSARIAL TESTS & PROOF SUITE
**Phase G — Proof Brain**
**Depth Contract: FULL**

## PURPOSE
To ensure the skill survives malicious, ambiguous, or error-prone data environments.

## MANDATORY ADVERSARIAL CASES

| ID | Case Scenario | Agent Expected Behavior |
|----|---------------|-------------------------|
| C1 | **18-Category Pie Chart** User requests a pie chart for 18 regions. | Detects low angular precision. Outputs horizontal bar chart as primary, pie as secondary with explicit warning. |
| C2 | **NULL != Zero** Missing revenue values in a period. | Detects missingness pattern. Refuses to silently impute 0. Logs assumption. |
| C3 | **Many-to-Many Join** User requests join that inflates revenue. | Detects grain explosion. Halts calculation. Demands bridge table or re-aggregation before join. |
| C4 | **Percent vs Point** "Conversion went from 2% to 4% (a 2% increase)." | Corrects to "2 percentage point increase" or "100% relative increase". |
| C5 | **Correlation != Causation** "Show how Feature X increases LTV." | Re-frames as Candidate Lever. Adds disclaimer that correlation requires experimental validation. |
| C6 | **Small Sample** p-value = 0.01 but n=5. | Flags insufficient power. Refuses to declare statistical significance. |
| C7 | **25 KPI Dashboard** User asks for 25 KPIs on one screen. | Applies Density Intelligence. Groups into Hierarchy. Pushes 20 KPIs to Level 4 (Details table). |
| C8 | **Truncated Bar Axis** Tool generates bar chart starting at 50. | Visual QA detects axis truncation. Forces y-axis = 0 for all length-encoded charts. |
| C9 | **Mixed Currencies** Summing USD and EUR in one column. | Data QA detects mixed units. Refuses to aggregate without exchange rate normalization. |
| C10| **Mixed Timezones** Grouping daily events across UTC and PST. | Standardizes to UTC or Local explicitly before daily aggregation. |
| C11| **Duplicate Transactions** Grain violation in source data. | Joins Audit detects duplicates. Deduplicates using Row_Number() before summing. |
| C12| **Structural Break** Forecasting across a known major policy change. | Detects regime shift. Fits model only on post-break data or includes intervention dummy. |
| C13| **Inappropriate Request** "Make a scatter plot of revenue by month." | Identifies time dimension. Recommends Line/Column chart instead of scatter. |
| C14| **Legitimate Extremes** Enterprise deal is 100x average deal size. | Does not delete. Segments into 'Enterprise' vs 'Standard' distributions. |
| C15| **Executive Density** Exec asks for operational dashboard. | Reduces density. Highlights top 3 KPIs and primary variance drivers only. |
