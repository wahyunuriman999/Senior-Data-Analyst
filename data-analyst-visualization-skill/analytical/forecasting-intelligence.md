# FORECASTING INTELLIGENCE
**Phase B — Analytical Brain Extension**

## 1. PRE-PROCESSING
- **Missing Periods**: Must be explicitly handled (Date Spine + Forward Fill or Interpolation). Never pass missing rows to a time-series model implicitly.
- **Structural Breaks**: Detect regime changes (e.g., Covid-19 drop). If detected, fit the model only on post-break data OR include an intervention dummy variable.

## 2. EVALUATION METRICS
Do not blindly output forecasts without validation metrics:
- **MAE**: Default for interpretability (absolute units).
- **RMSE**: Use when large errors are disproportionately bad.
- **MAPE**: Use for percentage errors. *Failure Mode*: Explodes to infinity if actuals contain 0. Switch to sMAPE or MAE if zeroes exist.
- **Data Leakage**: Ensure the train/test split strictly respects temporal order.

## 3. UNCERTAINTY
- **Rule**: Never present a point forecast without a prediction interval (e.g., 80% and 95% bands).
