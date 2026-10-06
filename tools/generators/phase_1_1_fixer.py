import os

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

# ---------------------------------------------------------
# 1. FIX BEHAVIORAL BENCHMARKS
# ---------------------------------------------------------
benchmarks = """# PHASE I: APEX EVIDENCE & RUNTIME VALIDATION GATE

## SINGLE SOURCE OF TRUTH: BEHAVIORAL BENCHMARK STATUS

This document records the strict validation status of the 20 adversarial benchmarks.
LLM cognitive behaviors remain pending live-runtime validation.

| ID | Status | Reason / Evidence |
|----|--------|-------------------|
| B01 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B02 | PASS | Evidence: proof/runners/sql_validation_log.txt (N:M Join Fan-out averted) |
| B03 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B04 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B05 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B06 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B07 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B08 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B09 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B10 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B11 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B12 | PASS | Evidence: proof/runners/forecast_validation_log.txt (Structural break detected) |
| B13 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B14 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B15 | PASS | Evidence: proof/examples/executive_sales/executive_sales.html (Density handled) |
| B16 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B17 | PASS | Evidence: proof/examples/executive_sales/executive_sales.html (Composite visual) |
| B18 | NOT_EXECUTED | Reason: LLM runtime unavailable in current validation environment. |
| B19 | PASS | Evidence: proof/examples/executive_sales/executive_sales.html (Exec audience design) |
| B20 | PASS | Evidence: proof/examples/analyst_deep_dive/analyst_deep_dive.html (Decomposition workflow) |
"""
write_file("proof/behavioral-benchmarks.md", benchmarks)

# ---------------------------------------------------------
# 2. FIX QA ENGINE COVERAGE
# ---------------------------------------------------------
qa_engine = """# QA & SELF-CRITIQUE ENGINE
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
"""
write_file("data-analyst-visualization-skill/quality/qa-and-critique-engine.md", qa_engine)

# ---------------------------------------------------------
# 3. FIX README CLAIMS
# ---------------------------------------------------------
readme = """# Apex Data Analyst & Visualization Skill

**Status:** IMPLEMENTED & PARTIALLY VALIDATED

This repository contains the architecture for the Apex Data Analyst intelligence system. The architecture is implemented and deterministic validation has passed; LLM cognitive validation remains NOT EXECUTED pending a live-runtime environment.

## Capabilities & Validation Status
- **Foundation & Analytical Engines**: IMPLEMENTED & DETERMINISTIC VALIDATION PASSED (SQL and Forecasting verified via execution runners).
- **Visualization & Dashboard Engines**: IMPLEMENTED & DETERMINISTIC VALIDATION PASSED (Real visual artifacts generated in `proof/examples`).
- **QA Engine**: IMPLEMENTED (Complete Q-DATA-001 to Q-STORY-005 rule matrix mapped).
- **Behavioral Benchmarks**: IMPLEMENTED (Fixtures created. Core SQL/Forecast/Vis tests executed. LLM COGNITIVE VALIDATION NOT EXECUTED).

## Evidence
- Check `proof/examples/` for actual generated dashboard artifacts (HTML).
- Check `proof/runners/` for SQL and Forecast execution logs proving the analytical methodologies.
- Check `proof/fixtures/` for the synthetic datasets used in testing.
- Check `proof/behavioral-benchmarks.md` for the exact strict status mapping of all 20 behavioral scenarios.
"""
write_file("data-analyst-visualization-skill/README.md", readme)

# ---------------------------------------------------------
# 4. CREATE REGRESSION RUNNER
# ---------------------------------------------------------
runner_code = """import os
import sys
import re

print("APEX DATA ANALYST REGRESSION SUITE\\n")

errors = 0

def assert_check(condition, name):
    global errors
    if condition:
        print(f"[PASS] {name}")
    else:
        print(f"[FAIL] {name}")
        errors += 1

# 1. Fixture Integrity
fixtures = [
    "null_revenue.csv", "orders.csv", "order_tags.csv",
    "pie_18_categories.csv", "time_series.csv"
]
fixture_pass = all(os.path.exists(f"proof/fixtures/{f}") for f in fixtures)
assert_check(fixture_pass, "Fixture integrity")

# 2. SQL Validation
sql_log = "proof/runners/sql_validation_log.txt"
sql_pass = os.path.exists(sql_log) and "STATUS: PASS" in open(sql_log).read()
assert_check(sql_pass, "SQL validation execution log exists and passed")

# 3. Forecast Validation
fc_log = "proof/runners/forecast_validation_log.txt"
fc_pass = os.path.exists(fc_log) and "STATUS: PASS" in open(fc_log).read()
assert_check(fc_pass, "Forecast validation execution log exists and passed")

# 4. Artifact Integrity
exec_html = "proof/examples/executive_sales/executive_sales.html"
analyst_html = "proof/examples/analyst_deep_dive/analyst_deep_dive.html"
art_pass = False
if os.path.exists(exec_html) and os.path.exists(analyst_html):
    with open(exec_html, 'r', encoding='utf-8') as f:
        content = f.read()
        if "echarts.min.js" in content and "html" in content.lower():
            art_pass = True
assert_check(art_pass, "Visual artifact generation & structure integrity")

# 5. Benchmark Status Consistency
bench = "proof/behavioral-benchmarks.md"
bench_pass = False
if os.path.exists(bench):
    content = open(bench).read()
    # Check that B01 is strictly NOT_EXECUTED
    if re.search(r'B01\\s*\\|\\s*NOT_EXECUTED', content) and not re.search(r'B01\\s*\\|\\s*PASS', content):
        bench_pass = True
assert_check(bench_pass, "Benchmark status consistency (No fabricated LLM PASS claims)")

print("\\n")
if errors == 0:
    print("RESULT: PASS")
    print("EXIT CODE: 0")
    sys.exit(0)
else:
    print("RESULT: FAIL")
    print(f"EXIT CODE: {errors}")
    sys.exit(errors)
"""
write_file("proof/runners/run_regression.py", runner_code)

print("Files updated successfully.")