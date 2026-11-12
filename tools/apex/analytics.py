#!/usr/bin/env python3
"""analytics.py — single source of truth for Apex v3 formulas (stdlib only).

Every formula here mirrors `data-analyst-visualization-skill/analytical/
formula-library.md` and its JS twin in `tools/apex/dashboard.tpl.js`.
If the doc, the Python, and the JS ever disagree, THIS module (as tested by
`proof/runners/test_engine_math.py`) wins — fix the other two.

Rules enforced here (see formula-library.md for the reasoning):
  F-01  mean never reported alone (median/P90 alongside)
  F-02  growth from a zero base is None ("n/a"), never 0%
  F-03  ratios recomputed from grain; never average ratios (no per-row AOV)
  F-05  variance decomposition is an exact identity: residual must be 0
  F-06  anomalies use median/MAD (modified z), not mean/SD
  F-08  forecast intervals use t-critical (df = n-2) + leverage, clip at 0,
        and always ship with a temporal backtest (MAE + sMAPE)
"""
import math

# ---------------------------------------------------------------- F-01
def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    if n == 0:
        return 0.0
    m = n // 2
    return xs[m] if n % 2 else (xs[m - 1] + xs[m]) / 2


def percentile(xs, p):
    """Nearest-rank percentile, p in [0, 1]."""
    xs = sorted(xs)
    if not xs:
        return 0.0
    return xs[min(len(xs) - 1, max(0, math.ceil(p * len(xs)) - 1))]


def sample_sd(xs):
    xs = list(xs)
    n = len(xs)
    if n < 2:
        return 0.0
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))  # n-1, not n (F-06)


# ---------------------------------------------------------------- F-02
def growth(cur, prev):
    """Period growth as a fraction. None when the base is 0 (undefined)."""
    if prev == 0:
        return None
    return (cur - prev) / abs(prev)


def growth_pp(cur_pct, prev_pct):
    """Percentage-point change between two percentages."""
    return cur_pct - prev_pct


# ---------------------------------------------------------------- F-03
def ratio(numerator_sum, denominator_sum):
    """A ratio recomputed from summed components. None on zero denominator."""
    if denominator_sum == 0:
        return None
    return numerator_sum / denominator_sum


def aov(total_revenue, total_units):
    """Average order value: SUM(revenue)/SUM(units). Never AVG(per-row AOV)."""
    return ratio(total_revenue, total_units)


def margin(total_profit, total_revenue):
    return ratio(total_profit, total_revenue)


def weighted_mean(pairs):
    """pairs: iterable of (value, weight)."""
    num = sum(x * w for x, w in pairs)
    den = sum(w for _, w in pairs)
    return ratio(num, den)


# ---------------------------------------------------------------- F-04
def distinct_overlap(segment_distinct_counts, total_distinct):
    """Overlap = ids counted in >1 segment. Must be >= 0; explain if > 0."""
    return sum(segment_distinct_counts) - total_distinct


# ---------------------------------------------------------------- F-05
def variance_decomp(cats):
    """Price/volume/mix decomposition between two periods.

    cats: iterable of (q0, p0, q1, p1) per category (q = units, p = avg price).
    Returns dict with volume/mix/price effects, dR, and residual.
    The identity dR == volume + mix + price is EXACT: residual must be 0
    (up to float rounding). A nonzero residual means the implementation
    is wrong — it is not "statistical residual".
    """
    q0 = sum(c[0] for c in cats)
    r0 = sum(c[0] * c[1] for c in cats)
    q1 = sum(c[2] for c in cats)
    r1 = sum(c[2] * c[3] for c in cats)
    p_bar0 = r0 / q0 if q0 else 0.0
    vol = (q1 - q0) * p_bar0
    price = sum(c[2] * (c[3] - c[1]) for c in cats)
    mix = sum((c[1] - p_bar0) * (c[2] - c[0] * (q1 / q0 if q0 else 0)) for c in cats)
    dr = r1 - r0
    return {"R0": r0, "R1": r1, "dR": dr, "volume": vol, "price": price,
            "mix": mix, "residual": dr - (vol + mix + price)}


# ---------------------------------------------------------------- F-06
def mad(xs):
    med = median(xs)
    return median([abs(x - med) for x in xs])


def modified_zscores(xs):
    """Robust z per point: 0.6745 * (x - median) / MAD. Flag |z| > 3.5."""
    med = median(xs)
    m = mad(xs)
    if m == 0:
        return [0.0 for _ in xs]
    return [0.6745 * (x - med) / m for x in xs]


def classic_zscores(xs):
    m = mean(xs)
    s = sample_sd(xs)
    if s == 0:
        return [0.0 for _ in xs]
    return [(x - m) / s for x in xs]


# ---------------------------------------------------------------- F-07
def pearson(xs, ys):
    xs, ys = list(xs), list(ys)
    n = len(xs)
    if n == 0 or n != len(ys):
        return 0.0
    mx, my = mean(xs), mean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0


# ---------------------------------------------------------------- F-08
_T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447,
        7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228, 12: 2.179, 15: 2.131,
        20: 2.086, 30: 2.042}


def t_crit_95(df):
    """Two-sided 95% t-critical. df >= 30 -> 1.96 (normal approx)."""
    if df in _T95:
        return _T95[df]
    if df > 30:
        return 1.96
    larger = [k for k in sorted(_T95) if k > df]
    return _T95[larger[0]] if larger else 1.96


def _ols(values):
    n = len(values)
    sx = sum(range(n))
    sy = sum(values)
    sxx = sum(i * i for i in range(n))
    sxy = sum(i * v for i, v in enumerate(values))
    denom = n * sxx - sx * sx
    b = (n * sxy - sx * sy) / denom if denom else 0.0
    a = (sy - b * sx) / n if n else 0.0
    return a, b


def forecast(values, horizon=3):
    """OLS on the last 6 points + 95% PREDICTION intervals (t-based).

    Returns {points: [{h, fc, lo, hi}], sigma, slope, t_star}.
    lo is clipped at 0: revenue/calls/units cannot be negative.
    """
    tail = list(values)[-6:]
    n = len(tail)
    a, b = _ols(tail)
    resid = [v - (a + b * i) for i, v in enumerate(tail)]
    sigma = math.sqrt(sum(r * r for r in resid) / max(n - 2, 1))
    xbar = sum(range(n)) / n if n else 0.0
    sxx_c = sum(i * i for i in range(n)) - sum(range(n)) ** 2 / n if n else 1.0
    t_star = t_crit_95(max(n - 2, 1))
    points = []
    for h in range(1, horizon + 1):
        x0 = n - 1 + h
        f = a + b * x0
        half = t_star * sigma * math.sqrt(1 + 1 / n + (x0 - xbar) ** 2 / (sxx_c or 1))
        points.append({"h": h, "fc": f, "lo": max(0.0, f - half), "hi": f + half})
    return {"points": points, "sigma": sigma, "slope": b, "t_star": t_star}


def backtest(values, holdout=3):
    """Temporal backtest: train on all but last `holdout`, predict them.

    Returns {mae, smape_pct}. sMAPE (not MAPE): MAPE explodes on actual = 0.
    """
    values = list(values)
    if len(values) < holdout + 3:
        return None
    train, test = values[:-holdout], values[-holdout:]
    a, b = _ols(train)
    preds = [a + b * (len(train) + i) for i in range(holdout)]
    errs = [abs(y - f) for y, f in zip(test, preds)]
    mae = sum(errs) / len(errs)
    smape = sum(abs(y - f) / ((abs(y) + abs(f)) / 2 or 1)
                for y, f in zip(test, preds)) / len(test) * 100
    return {"mae": mae, "smape_pct": smape}


def next_month_labels(last_period, count=3):
    """['2026-10'] + 3 -> ['Nov 26', 'Des 26', 'Jan 27']. Derived, never hardcoded."""
    mon = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
           "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    y, m = int(last_period[:4]), int(last_period[5:7])
    out = []
    for _ in range(count):
        m += 1
        if m > 12:
            m, y = 1, y + 1
        out.append(f"{mon[m - 1]} {str(y)[2:]}")
    return out
