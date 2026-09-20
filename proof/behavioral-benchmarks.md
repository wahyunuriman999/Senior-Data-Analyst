# PHASE I: APEX EVIDENCE & RUNTIME VALIDATION GATE

## REQUIRED BENCHMARK SCHEMA
Each test requires explicit execution mapping. Because an autonomous LLM runner is required to simulate the AI's cognitive behavior (and API access is restricted in this exact sandbox), the Execution Method is documented, but the Status of LLM-dependent tests is explicitly `NOT_EXECUTED` to maintain strict evidentiary honesty. 

However, **Fixtures, SQL Validations, Forecast Validations, and Real Visual Artifacts** have been successfully executed via Python/SQLite scripts in the `proof/runners` directory.

| ID | Domain | Objective | Execution Method | Status |
|----|--------|-----------|------------------|--------|
| B01 | Grain | Stop before aggregation | LLM Prompt against fixtures/orders.csv | NOT_EXECUTED (LLM required) |
| B02 | SQL | Detect N:M Join Fan-out | SQLite Execution (`proof/runners/sql_validation_log.txt`) | **EXECUTED / PASS** |
| B03 | Data QA | Handle NULL Revenue | LLM Prompt against fixtures/null_revenue.csv | NOT_EXECUTED (LLM required) |
| B04 | Metric | Resolve Ambiguity | LLM Prompt against fixtures/conversion_ambiguity.csv | NOT_EXECUTED (LLM required) |
| B05 | Calc QA | % vs %-Point | LLM Prompt against fixtures/percentage_point.csv | NOT_EXECUTED (LLM required) |
| B06 | Vis | 18-Category Pie | LLM Prompt against fixtures/pie_18_categories.csv | NOT_EXECUTED (LLM required) |
| B07 | Vis | Time Series | LLM Prompt against fixtures/time_series.csv | NOT_EXECUTED (LLM required) |
| B12 | Forecast | Structural Break | Python Stats/Math (`proof/runners/forecast_validation_log.txt`) | **EXECUTED / PASS** |
| B15 | Vis/Dash| Dashboard Density | Matplotlib/ECharts generation (`proof/examples/`) | **EXECUTED / PASS** |
| B20 | Analyst | Deep Dive | Matplotlib/ECharts generation (`proof/examples/`) | **EXECUTED / PASS** |

*(Note: B01-B20 all possess detailed schema definitions in `proof/benchmark-cases/` for the final LLM runner).*
