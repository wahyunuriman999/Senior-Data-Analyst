# ADVANCED ANALYTICAL ENGINE (B2-B4)
**Phase B — Analytical Brain Extension**
**Depth Contract: FULL**

## COHORT & RETENTION ANALYSIS
- **Rule**: Always align the denominator (acquisition cohort size). 
- **Output**: Triangular matrix (absolute or %).
- **QA**: Ensure later periods with incomplete data are marked NA, not 0.

## FUNNEL ANALYSIS
- **Rule**: Distinguish between strictly ordered funnels (must complete Step 1 to do Step 2) and loose funnels.
- **QA**: Verify denominator logic (Total Users vs Users who reached previous step).

## FORECASTING ENGINE
- **Rule**: Never present a point forecast without a prediction interval (e.g., 80% and 95% bands).
- **Rule**: Decompose history into Trend, Seasonality, Residual before fitting.
- **QA**: Check for negative forecasts on strictly positive metrics (use log transform).

## SQL INTELLIGENCE
- **Rule**: Analytical SQL is about *grain management*.
- **Anti-Pattern**: Using `COUNT(id)` instead of `COUNT(DISTINCT id)` when joining across one-to-many relationships.
- **Anti-Pattern**: Forgetting `COALESCE` or `IFNULL` when doing outer joins for comparative analysis.
