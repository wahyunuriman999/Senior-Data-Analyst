#!/usr/bin/env python3
"""test_sidebar.py — proof tests for Sidebar v2 (design/sidebar.md).

Run:  python3 data-analyst-visualization-skill/proof/runners/test_sidebar.py
Exit 0 = all pass. Stdlib only, no browser: builds a dashboard through the
real tools/apex/build_page.py and asserts the anatomy in the HTML string.

Covers: grouped nav (3 groups), exactly one active item, collapse button,
hamburger + drawer (and NO display:none sidebar rule), honest badges
(period count / dim1 count), brand/footer overrides, cohort item present
only with cohort data, and no dead nav links (every href resolves to a
section id in the same file).
"""
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, "tools", "apex"))
from build_page import build  # noqa: E402


def make_cfg(**over):
    cfg = {
        "title": "Sidebar Test", "currency": "Rp", "locale": "id-ID",
        "dim1": {"label": "Kota", "values": ["Jakarta", "Bandung", "Surabaya"]},
        "dim2": {"label": "Kategori", "values": ["Fashion", "Elektronik"]},
        "time": {"label": "Bulan", "periods": ["2026-01", "2026-02", "2026-03"],
                 "period_labels": {"2026-01": "Jan 26", "2026-02": "Feb 26",
                                   "2026-03": "Mar 26"}},
        "metrics": {"revenue": "Omzet", "profit": "Profit",
                    "margin": "Margin", "units": "Transaksi"},
        "provenance": "Test fixture.", "freshness": "Jan–Mar 2026",
    }
    cfg.update(over)
    return cfg


ROWS = [{"kota": "Jakarta", "kategori": "Fashion", "bulan": "2026-01",
         "units": 10, "omzet": 1000, "cogs": 600, "diskon_pct": 0.0}]
COHORTS = {"labels": ["2026-01"], "sizes": [100], "retention": [[1.0]]}


class TestSidebar(unittest.TestCase):
    def setUp(self):
        self.html = build(ROWS, COHORTS, make_cfg(), "/* echarts */", "/* app */")
        self.plain = build(ROWS, None, make_cfg(), "/* echarts */", "/* app */")

    def test_aside_and_groups(self):
        self.assertIn('<aside class="sidebar" id="sidebar"', self.html)
        labels = re.findall(r'class="nav-group-label">([^<]+)<', self.html)
        self.assertEqual(labels, ["Analisis", "Data", "Verifikasi"])

    def test_items_and_single_active(self):
        items = re.findall(r'class="nav-item[^"]*"', self.html)
        self.assertEqual(len(items), 6)  # Tren, Var, Kohort, Wilayah, Tabel, Fakta
        self.assertEqual(len(re.findall(r'class="nav-item on"', self.html)), 1)
        self.assertIn('href="#sec-tren" class="nav-item on"', self.html)

    def test_collapse_hamburger_drawer_no_display_none(self):
        self.assertIn('id="btn-sidebar-collapse"', self.html)
        self.assertIn('id="btn-sidebar-menu"', self.html)
        self.assertIn('id="sidebar-backdrop"', self.html)
        self.assertIn("drawer-open", self.html)
        self.assertNotRegex(self.html, r'\.sidebar\s*\{[^}]*display\s*:\s*none')
        self.assertIn("#app.rail .sidebar{width:68px", self.html)

    def test_honest_badges(self):
        # Tren badge = period count (3), Tabel badge = dim1 value count (3).
        badges = re.findall(r'class="nav-badge">(\d+)<', self.html)
        self.assertEqual(badges, ["3", "3"])

    def test_brand_and_footer_override(self):
        cfg = make_cfg(sidebar={
            "brand": {"mark": "ZZ", "name": "Toko Uji", "tag": "Uji v9"},
            "footer": {"user": "Budi Santoso", "role": "Owner"},
        })
        html = build(ROWS, None, cfg, "/* echarts */", "/* app */")
        self.assertIn('<span class="brand-mark">ZZ</span>', html)
        self.assertIn("Toko Uji", html)
        self.assertIn("<b>Budi Santoso</b>", html)
        self.assertIn('<span class="side-avatar">BS</span>', html)

    def test_cohort_item_conditional(self):
        self.assertIn('href="#sec-kohort"', self.html)
        self.assertNotIn('href="#sec-kohort"', self.plain)
        self.assertEqual(len(re.findall(r'class="nav-item[^"]*"', self.plain)), 5)

    def test_no_dead_nav_links(self):
        hrefs = re.findall(r'<a href="#(sec-[a-z]+)" class="nav-item', self.html)
        self.assertTrue(hrefs)
        for h in hrefs:
            self.assertIn(f'id="{h}"', self.html, f"nav link #{h} has no section")

    def test_every_item_has_title_tooltip(self):
        items = re.findall(r'<a href="#sec-[a-z]+" class="nav-item[^>]*>', self.html)
        self.assertTrue(all('title="' in i for i in items))


if __name__ == "__main__":
    unittest.main(verbosity=2)
