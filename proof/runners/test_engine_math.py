#!/usr/bin/env python3
"""test_engine_math.py — proof tests for tools/apex/analytics.py (F-01..F-08).

Run:  python3 proof/runners/test_engine_math.py
Exit 0 = all identities hold. No third-party deps (stdlib unittest only).

Each test pins one formula rule from analytical/formula-library.md, so a
future "improvement" that silently reintroduces a wrong formula fails here
first — before any dashboard ships.
"""
import math
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "apex"))
import analytics as A  # noqa: E402


class TestGrowthZeroBase(unittest.TestCase):
    """F-02: growth from a zero base is undefined — never 0%."""

    def test_zero_base_is_none(self):
        self.assertIsNone(A.growth(100, 0))
        self.assertIsNone(A.growth(0, 0))

    def test_normal_growth(self):
        self.assertAlmostEqual(A.growth(110, 100), 0.10)
        self.assertAlmostEqual(A.growth(90, 100), -0.10)

    def test_negative_base_uses_abs(self):
        # (cur - prev) / |prev| keeps the direction honest on negative bases.
        self.assertAlmostEqual(A.growth(-50, -100), 0.50)

    def test_pp_vs_pct(self):
        self.assertAlmostEqual(A.growth_pp(25.0, 20.0), 5.0)  # 5 pp, not 5%


class TestRatiosFromGrain(unittest.TestCase):
    """F-03: ratios recomputed from summed components; AVG-of-AVG is wrong."""

    def test_aov_avg_of_avg_trap(self):
        # City A: rev 100 / 10 units (AOV 10). City B: rev 1000 / 100 units (AOV 10).
        # Naive AVG(per-row AOV) = 10 here by luck; change B to 10 units @ AOV 100:
        # AVG(AOV) = (10 + 100) / 2 = 55, true AOV = 1100 / 20 = 55 — same again
        # only because units match. Break the tie: B has 100 units.
        # A: 100/10 = 10, B: 1000/100 = 10 -> AVG = 10, true = 1100/110 = 10.
        # Now the real trap: A 100/10 (10), B 1000/10 (100), C 100/100 (1):
        # AVG = 37, true = 1200/120 = 10. The 3.7x gap is the bug v3 kills.
        self.assertAlmostEqual(A.aov(1200, 120), 10.0)
        naive_avg = (10 + 100 + 1) / 3
        self.assertNotAlmostEqual(naive_avg, 10.0, places=1)

    def test_zero_denominator_is_none(self):
        self.assertIsNone(A.aov(1000, 0))
        self.assertIsNone(A.margin(100, 0))

    def test_weighted_mean(self):
        self.assertAlmostEqual(A.weighted_mean([(10, 1), (20, 3)]), 17.5)


class TestDistribution(unittest.TestCase):
    """F-01: median/P90; F-06: MAD robustness."""

    def test_median_even_odd(self):
        self.assertEqual(A.median([3, 1, 2]), 2)
        self.assertEqual(A.median([4, 1, 3, 2]), 2.5)

    def test_p90(self):
        self.assertEqual(A.percentile(list(range(1, 11)), 0.9), 9)

    def test_median_robust_to_outlier(self):
        # One 300 in eleven ~100s: mean jumps to ~118, median stays 100.
        xs = [100, 101, 99, 100, 102, 98, 100, 101, 99, 100, 100, 300]
        self.assertEqual(A.median(xs), 100)
        self.assertGreater(A.mean(xs), 110)

    def test_modified_z_flags_outlier(self):
        xs = [100, 101, 99, 100, 102, 98, 100, 101, 99, 100, 100, 300]
        z = A.modified_zscores(xs)
        self.assertGreater(abs(z[-1]), 3.5)
        self.assertTrue(all(abs(v) < 3.5 for v in z[:-1]))

    def test_sample_sd_uses_n_minus_1(self):
        # [0, 2]: population SD = 1.0, sample SD = sqrt(2).
        self.assertAlmostEqual(A.sample_sd([0, 2]), math.sqrt(2))


class TestVarianceDecomposition(unittest.TestCase):
    """F-05: decomposition is an exact identity — residual must be 0."""

    def test_residual_zero_two_categories(self):
        cats = [(100, 10.0, 110, 9.0), (50, 20.0, 45, 22.0)]
        r = A.variance_decomp(cats)
        self.assertAlmostEqual(r["dR"], (110 * 9 + 45 * 22) - (100 * 10 + 50 * 20))
        self.assertAlmostEqual(r["residual"], 0.0, places=6)
        self.assertAlmostEqual(r["volume"] + r["mix"] + r["price"], r["dR"], places=6)

    def test_residual_zero_real_example_shape(self):
        # Shape of proof/real-examples.md Ex.1: price down, volume up, mix up.
        cats = [(1000, 38.8, 1090, 33.0), (500, 77.6, 520, 70.0)]
        r = A.variance_decomp(cats)
        self.assertAlmostEqual(r["residual"], 0.0, places=6)

    def test_single_category_is_pure_price_plus_volume(self):
        r = A.variance_decomp([(100, 10.0, 120, 12.0)])
        self.assertAlmostEqual(r["mix"], 0.0, places=9)


class TestDistinctOverlap(unittest.TestCase):
    """F-04: segment distinct-counts sum >= total; the gap is overlap."""

    def test_oatside_shape(self):
        segments = [6506, 441, 421, 374, 310, 309, 235, 212, 162, 78]
        self.assertEqual(A.distinct_overlap(segments, 9032), 16)


class TestForecast(unittest.TestCase):
    """F-08: t-intervals (not 1.96), widening with horizon, clip at 0."""

    def test_t_critical_small_df(self):
        self.assertAlmostEqual(A.t_crit_95(4), 2.776)  # n=6 -> df=4
        self.assertAlmostEqual(A.t_crit_95(40), 1.96)

    def test_interval_widens_with_horizon(self):
        vals = [100, 102, 101, 103, 102, 104, 103, 105, 104, 106, 105, 107]
        f = A.forecast(vals)
        widths = [p["hi"] - p["lo"] for p in f["points"]]
        self.assertTrue(widths[0] < widths[1] < widths[2])

    def test_interval_wider_than_z_interval(self):
        # t*=2.776 vs z=1.96 on n=6: t-interval must be ~42% wider.
        vals = [100, 102, 101, 103, 102, 104]
        f = A.forecast(vals)
        z_half = 1.96 * f["sigma"]
        t_half = (f["points"][0]["hi"] - f["points"][0]["lo"]) / 2
        self.assertGreater(t_half, z_half * 1.2)

    def test_negative_forecast_clipped(self):
        vals = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5, 2]
        f = A.forecast(vals)
        self.assertTrue(all(p["lo"] >= 0 for p in f["points"]))

    def test_backtest_perfect_series(self):
        vals = [10 * i for i in range(1, 13)]  # perfect linear
        bt = A.backtest(vals)
        self.assertAlmostEqual(bt["smape_pct"], 0.0, places=6)
        self.assertAlmostEqual(bt["mae"], 0.0, places=6)

    def test_backtest_returns_none_when_too_short(self):
        self.assertIsNone(A.backtest([1, 2, 3, 4, 5]))

    def test_next_month_labels_roll_over_year(self):
        self.assertEqual(A.next_month_labels("2026-10", 3), ["Nov 26", "Des 26", "Jan 27"])
        self.assertEqual(A.next_month_labels("2026-12", 2), ["Jan 27", "Feb 27"])


class TestPearson(unittest.TestCase):
    """F-07: correlation computed, bounded, and never causal by itself."""

    def test_perfect_correlation(self):
        self.assertAlmostEqual(A.pearson([1, 2, 3], [2, 4, 6]), 1.0)

    def test_no_correlation(self):
        r = A.pearson([1, 2, 3, 4], [4, 1, 3, 2])
        self.assertLess(abs(r), 0.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
