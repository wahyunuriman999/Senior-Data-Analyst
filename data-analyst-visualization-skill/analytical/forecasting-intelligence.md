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
- **Interval yang benar (F-08):** interval prediksi memakai **t-critical
  dengan df = n−2** (n=6 → t*=2,776 — BUKAN 1,96), memakai **leverage**
  `√(1 + 1/n + (x₀−x̄)²/Σ(x−x̄)²)` sehingga interval MELEBAR per horizon,
  dan di-clip di 0 untuk metrik tak-negatif. Interval `f ± 1,96·σ` adalah
  bug: ~30% terlalu sempit pada n=6, tidak melebar, dan itu interval
  rata-rata — bukan interval observasi mendatang.

## 4. BACKTEST (WAJIB — BUKAN OPSIONAL)
- Latih di [awal … T−3], uji di [T−2 … T] (temporal, jangan acak).
- Laporkan **MAE + sMAPE** backtest di samping forecast; sMAPE > 20% →
  forecast ditandai `⚠ tidak andal`.
- Bandingkan dengan baseline naif & seasonal-naif; bila model tidak
  mengalahkan baseline, tampilkan baseline.
- Detail protokol & tangga model: `analytical/forecasting.md` §2–3;
  rumus: `formula-library.md` F-08.

## 5. LABEL & PERIODE
- Label bulan forecast DITURUNKAN dari periode terakhir data (+1, +2, +3
  bulan kalender). Hardcode label bulan = FATAL.
- Bulan berjalan bukan titik penuh: jangan masuk training set tanpa
  normalisasi per-hari (§F-12).
