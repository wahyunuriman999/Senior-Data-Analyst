# QA & SELF-CRITIQUE ENGINE

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
- **Q-DATA-009 Unit**: Input: Unit measures. Fail: Summing Kg and Lbs.
- **Q-DATA-010 Freshness**: Input: Max date. Fail: Data is older than analysis context.
- **Q-DATA-011 Outlier**: Input: Z-scores. Fail: Blind deletion of outliers.

### CALCULATION QA
- **Q-CALC-001 Numerator**: Fail: Incorrect numerator definition.
- **Q-CALC-002 Denominator**: Fail: Denominator drops legitimate zeros. Severity: CRITICAL.
- **Q-CALC-005 Percentage**: Fail: Confusing % change with percentage points. Severity: MAJOR.

### STATISTICAL QA
- **Q-STAT-001 Sample Size**: Fail: n < 30 without uncertainty bounds.
- **Q-STAT-004 Multiple Testing**: Fail: k > 1 hypotheses tested without Bonferroni/FDR correction.
- **Q-STAT-005 Causality**: Fail: Using "causes" for observational data. Severity: CRITICAL.

### VISUALIZATION QA
- **Q-VIS-001 Chart Fit**: Fail: Chart violates visual grammar engine.
- **Q-VIS-002 Axis**: Fail: Truncated zero baseline on bar chart. Severity: CRITICAL.
- **Q-VIS-006 Overplotting**: Fail: Scatter plot is a solid block of ink. Fix: Use hexbin.

### STORY QA
- **Q-STORY-001 Claim Support**: Fail: Headline exceeds evidence. Severity: CRITICAL.

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
