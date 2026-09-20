# QA & SELF-CRITIQUE ENGINE
**Phase F — Quality Brain**

## DEEP OPERATIONAL QA CHECKS
All outputs must pass these checks. Failure triggers the Self-Critique loop.

### DATA QA
- **Q-DATA-001 Schema**: Input: Columns. Fail: Expected schema mismatch.
- **Q-DATA-002 Missingness**: Input: NULL counts. Fail: Silent imputation applied to MNAR data. Severity: CRITICAL. Fix: Require imputation strategy reasoning.
- **Q-DATA-003 Duplicate**: Input: Row keys. Fail: Primary key violated.
- **Q-DATA-004 Grain**: Input: Group By clauses. Fail: Aggregating mixed grains. Severity: CRITICAL.
- **Q-DATA-005 Join**: Input: Row counts. Fail: Cartesian explosion. Severity: CRITICAL.
- **Q-DATA-006 Referential Integrity**: Input: Foreign keys. Fail: Orphan records > 0.
- **Q-DATA-007 Currency**: Input: Currency symbols. Fail: Summing mixed currencies. Severity: MAJOR.
- **Q-DATA-008 Timezone**: Input: Timestamps. Fail: Grouping by date across mixed timezones.
- **Q-DATA-009 Unit Consistency**: Input: Unit measures. Fail: Summing Kg and Lbs.
- **Q-DATA-010 Freshness**: Input: Max date. Fail: Data is older than analysis context.
- **Q-DATA-011 Outlier**: Input: Z-scores. Fail: Blind deletion of outliers.

### CALCULATION QA
- **Q-CALC-001 Numerator**: Fail: Incorrect numerator definition.
- **Q-CALC-002 Denominator**: Fail: Denominator drops legitimate zeros. Severity: CRITICAL.
- **Q-CALC-003 Aggregation**: Fail: Aggregating a non-additive metric (e.g. ratios).
- **Q-CALC-004 Distinct Counting**: Fail: Using COUNT instead of COUNT DISTINCT on a joined table.
- **Q-CALC-005 Percentage**: Fail: Confusing % change with percentage points. Severity: MAJOR.
- **Q-CALC-006 Rate**: Fail: Averaging averages without weighting.
- **Q-CALC-007 Weighted Average**: Fail: Missing weights for grouped ratios.

### STATISTICAL QA
- **Q-STAT-001 Sample Size**: Fail: n < 30 without uncertainty bounds.
- **Q-STAT-002 Effect Size**: Fail: Reporting p-value without magnitude.
- **Q-STAT-003 Uncertainty**: Fail: Forecasting without prediction intervals.
- **Q-STAT-004 Multiple Testing**: Fail: k > 1 hypotheses tested without Bonferroni/FDR correction.
- **Q-STAT-005 Causality**: Fail: Using "causes" for observational data. Severity: CRITICAL.
- **Q-STAT-006 Leakage**: Fail: Future data included in temporal training set.

### VISUALIZATION QA
- **Q-VIS-001 Chart Fit**: Fail: Chart violates visual grammar engine.
- **Q-VIS-002 Axis**: Fail: Truncated zero baseline on bar chart. Severity: CRITICAL.
- **Q-VIS-003 Scale**: Fail: Linear scale for exponential data without justification.
- **Q-VIS-004 Unit**: Fail: Missing axis units.
- **Q-VIS-005 Cardinality**: Fail: > 7 categories on a pie chart.
- **Q-VIS-006 Overplotting**: Fail: Scatter plot is a solid block of ink. Fix: Use hexbin.
- **Q-VIS-007 Color**: Fail: Rainbow palette for continuous data.
- **Q-VIS-008 Accessibility**: Fail: Relying solely on red/green encoding.
- **Q-VIS-009 Annotation**: Fail: Missing contextual explanation for an anomaly.
- **Q-VIS-010 Density**: Fail: Overlapping text labels on x-axis.

### STORY QA
- **Q-STORY-001 Claim Support**: Fail: Headline exceeds evidence. Severity: CRITICAL.
- **Q-STORY-002 Denominator Visibility**: Fail: Absolute change highlighted without relative baseline context.
- **Q-STORY-003 Causal Language**: Fail: Treating correlation as proven intervention.
- **Q-STORY-004 Cherry Picking**: Fail: Starting timeline precisely at a trough to exaggerate growth.
- **Q-STORY-005 Context**: Fail: Missing macroeconomic or business context.

## UPGRADED SELF-CRITIQUE SCHEMA
Before outputting, execute:
```yaml
ISSUE:
  Category: [e.g., Visualization]
  Severity: [Critical | Major | Minor | Info]
  Evidence: [e.g., Axis starts at 50 instead of 0]
  Impact: [e.g., Exaggerates the difference between categories]
  Fix: [e.g., Set y-axis minimum to 0]
  Retest: [e.g., Verified axis limits in final chart object]
  RetestEvidence: [e.g., Code confirms ymin=0]
  Status: [PASS]
```
Critical/Major FAIL -> Artifact CANNOT be finalized. FIX WITHOUT RETEST = NOT VERIFIED.
