#!/usr/bin/env python3
"""Synthetic demo datasets for the 10 Apex reference domains.

Each domain returns (rows, cohorts, cfg) where rows use the canonical internal
schema: kota(=dim1), kategori(=dim2), bulan(=period), units, omzet, cogs,
diskon_pct, aov_list. Display labels come from cfg. All data is deterministic
(seeded) and declared synthetic.
"""
import numpy as np

PERIODS = ["2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
           "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]
SEASON = np.array([0.92, 0.90, 1.00, 0.98, 1.02, 1.00, 0.97, 1.00, 1.03, 1.10, 1.05, 1.28])


def synth(p):
    rng = np.random.default_rng(p["seed"])
    d1, d2 = p["dim1"], p["dim2"]
    w1 = np.array(p["w1"]); w1 = w1 / w1.sum()
    w2 = np.array(p["w2"]); w2 = w2 / w2.sum()
    aov = np.array(p["aov"], dtype=float)
    margin = np.array(p["margin"], dtype=float)
    drift = np.array(p.get("drift", [0.0] * len(d2)), dtype=float)
    rows = []
    for mi, per in enumerate(PERIODS):
        cal = int(per.split("-")[1]) - 1
        for i, v1 in enumerate(d1):
            for j, v2 in enumerate(d2):
                units = p["base_units"] * (1 + p.get("growth", 0.012)) ** mi
                units *= w1[i] * w2[j] * SEASON[cal]
                disc = 0.0
                for ev in p.get("events", []):
                    if ev["period"] == per and (not ev.get("d2") or v2 in ev["d2"]):
                        units *= ev["mult"]; disc = max(disc, ev["disc"])
                for sl in p.get("slumps", []):
                    if sl["period"] == per and sl["d1"] == v1 and sl["d2"] == v2:
                        units *= sl["mult"]
                units *= float(rng.lognormal(0, 0.06))
                units = int(round(units))
                aov_l = aov[j] * (1 + drift[j]) ** (mi / 12)
                rev = int(round(units * aov_l * (1 - disc)))
                m = float(np.clip(margin[j] + rng.normal(0, 0.015), 0.05, 0.6))
                rows.append({"kota": v1, "kategori": v2, "bulan": per, "units": units,
                             "omzet": rev, "cogs": int(round(rev * (1 - m))),
                             "diskon_pct": round(disc * 100, 1),
                             "aov_list": int(round(aov_l))})
    # cohorts
    crng = np.random.default_rng(p["seed"] + 999)
    sizes, mat = [], []
    for m in range(12):
        sizes.append(int(8000 * 1.02 ** m))
        mat.append([round(float(np.clip(0.62 / (1 + 0.5 * t) + crng.normal(0, 0.012), 0.015, 1.0)), 4)
                    for t in range(12)])
    cohorts = {"labels": PERIODS, "sizes": sizes, "retention": mat}
    cfg = {
        "title": p["title"], "currency": "Rp", "locale": "id-ID",
        "dim1": {"label": p["dim1_label"], "values": d1},
        "dim2": {"label": p["dim2_label"], "values": d2},
        "time": {"label": "Bulan", "periods": PERIODS,
                 "period_labels": {b: l for b, l in zip(
                     PERIODS, ["Nov 25", "Des 25", "Jan 26", "Feb 26", "Mar 26", "Apr 26",
                               "Mei 26", "Jun 26", "Jul 26", "Agu 26", "Sep 26", "Okt 26"])}},
        "metrics": {"revenue": p["m_rev"], "profit": p["m_prof"],
                    "margin": "Margin", "units": p["m_units"]},
        "provenance": ("Data SINTETIS deterministik (seed %d), digenerate oleh "
                       "tools/apex/demo_data.py untuk referensi standar Apex v2. "
                       "Bukan data operasional nyata." % p["seed"]),
        "freshness": "Nov 2025 – Okt 2026",
    }
    return rows, cohorts, cfg


DOMAINS = {
    "finance": dict(
        title="Corporate Finance — Variance Decomposition", seed=101,
        dim1_label="Region", dim1=["Jakarta", "Surabaya", "Bandung", "Medan", "Makassar"],
        w1=[.34, .20, .16, .15, .15],
        dim2_label="Divisi", dim2=["Ritel", "Korporat", "Treasury", "Syariah"],
        w2=[.30, .35, .20, .15], aov=[1_800_000, 4_500_000, 2_200_000, 900_000],
        margin=[.24, .31, .18, .27], drift=[.01, .02, -.01, .015],
        base_units=38000, m_rev="Pendapatan", m_prof="Laba", m_units="Transaksi",
        events=[{"period": "2025-12", "mult": 1.15, "disc": .10},
                {"period": "2026-10", "d2": ["Ritel"], "mult": 1.30, "disc": .15}]),
    "sales": dict(
        title="Executive Sales & Forecasting", seed=42,
        dim1_label="Kota", dim1=["Jakarta", "Surabaya", "Bandung", "Medan", "Makassar"],
        w1=[.34, .20, .16, .15, .15],
        dim2_label="Kategori", dim2=["Elektronik", "Fashion", "FMCG", "Home & Living"],
        w2=[.18, .34, .30, .18], aov=[2_400_000, 380_000, 95_000, 850_000],
        margin=[.22, .35, .18, .28], drift=[-.03, .01, .04, .015],
        base_units=46000, m_rev="Omzet", m_prof="Profit", m_units="Transaksi",
        events=[{"period": "2025-12", "mult": 1.15, "disc": .12},
                {"period": "2026-10", "d2": ["Fashion", "Elektronik"], "mult": 1.35, "disc": .18},
                {"period": "2026-10", "mult": 1.10, "disc": .08}],
        slumps=[{"period": "2026-07", "d1": "Bandung", "d2": "Fashion", "mult": .55},
                {"period": "2026-08", "d1": "Bandung", "d2": "Fashion", "mult": .55}]),
    "marketing": dict(
        title="Marketing — Cohort & Funnel Analytics", seed=103,
        dim1_label="Channel", dim1=["Organik", "Paid Ads", "Social", "Email", "Affiliate"],
        w1=[.28, .24, .22, .12, .14],
        dim2_label="Segmen", dim2=["Baru", "Kembali", "Reseller", "Korporat"],
        w2=[.40, .30, .18, .12], aov=[320_000, 450_000, 1_100_000, 2_800_000],
        margin=[.30, .25, .28, .35], drift=[.02, -.02, .01, .03],
        base_units=52000, m_rev="Revenue", m_prof="Kontribusi", m_units="Konversi",
        events=[{"period": "2026-10", "d2": ["Baru"], "mult": 1.50, "disc": .20},
                {"period": "2025-12", "mult": 1.20, "disc": .10}]),
    "logistics": dict(
        title="Logistics & Supply Chain", seed=104,
        dim1_label="Hub", dim1=["Jakarta", "Surabaya", "Medan", "Makassar", "Balikpapan"],
        w1=[.36, .22, .16, .14, .12],
        dim2_label="Moda", dim2=["Darat", "Laut", "Udara", "Kereta"],
        w2=[.45, .30, .10, .15], aov=[180_000, 420_000, 950_000, 260_000],
        margin=[.20, .26, .32, .22], drift=[.03, .02, .05, .02],
        base_units=61000, m_rev="Revenue", m_prof="Margin", m_units="Pengiriman",
        events=[{"period": "2026-04", "mult": 1.35, "disc": 0.0},
                {"period": "2025-12", "mult": 1.25, "disc": 0.0}],
        slumps=[{"period": "2026-02", "d1": "Medan", "d2": "Laut", "mult": .60}]),
    "product": dict(
        title="Product Engagement Analytics", seed=105,
        dim1_label="Platform", dim1=["Android", "iOS", "Web", "Desktop"],
        w1=[.44, .30, .18, .08],
        dim2_label="Fitur", dim2=["Search", "Checkout", "Feed", "Notifikasi"],
        w2=[.30, .22, .33, .15], aov=[12_000, 85_000, 4_000, 2_000],
        margin=[.40, .35, .45, .50], drift=[.01, .02, 0.0, -.01],
        base_units=880000, m_rev="Nilai Interaksi", m_prof="Kontribusi", m_units="Sesi",
        events=[{"period": "2026-10", "d2": ["Checkout"], "mult": 1.40, "disc": .12}]),
    "hr": dict(
        title="HR & People Analytics", seed=106,
        dim1_label="Departemen", dim1=["Engineering", "Sales", "Operasi", "Finance", "SDM"],
        w1=[.30, .26, .24, .12, .08],
        dim2_label="Level", dim2=["Junior", "Middle", "Senior", "Lead"],
        w2=[.38, .32, .22, .08], aov=[9_000_000, 16_000_000, 28_000_000, 45_000_000],
        margin=[.15, .18, .22, .25], drift=[.04, .045, .05, .06],
        base_units=2400, m_rev="Output Value", m_prof="Surplus", m_units="Karyawan",
        events=[{"period": "2026-01", "mult": 1.18, "disc": 0.0}]),
    "ecommerce": dict(
        title="E-Commerce — Market Basket", seed=107,
        dim1_label="Kota", dim1=["Jakarta", "Surabaya", "Bandung", "Medan", "Makassar"],
        w1=[.32, .21, .17, .16, .14],
        dim2_label="Kategori", dim2=["Elektronik", "Fashion", "Kecantikan", "Olahraga"],
        w2=[.22, .36, .24, .18], aov=[2_100_000, 350_000, 180_000, 420_000],
        margin=[.23, .36, .42, .30], drift=[-.02, .01, .03, .02],
        base_units=54000, m_rev="Omzet", m_prof="Profit", m_units="Pesanan",
        events=[{"period": "2026-10", "d2": ["Fashion", "Kecantikan"], "mult": 1.45, "disc": .20},
                {"period": "2025-12", "mult": 1.25, "disc": .12}]),
    "risk": dict(
        title="Risk Management — Statistical Confidence", seed=108,
        dim1_label="Portofolio", dim1=["Konsumer", "SME", "Korporat", "Mikro"],
        w1=[.40, .28, .20, .12],
        dim2_label="Kolektibilitas", dim2=["Lancar", "DPK", "Kurang Lancar", "Diragukan", "Macet"],
        w2=[.62, .18, .10, .06, .04], aov=[15_000_000, 45_000_000, 120_000_000, 8_000_000, 0],
        margin=[.12, .10, .06, .03, .01], drift=[.01, .01, 0.0, -.02, 0.0],
        base_units=12000, m_rev="Outstanding", m_prof="Net Spread", m_units="Akun",
        events=[{"period": "2026-06", "d2": ["Macet", "Diragukan"], "mult": 1.30, "disc": 0.0}]),
    "health": dict(
        title="Healthcare Patient Flow", seed=109,
        dim1_label="Rumah Sakit", dim1=["RS Harapan", "RS Sejahtera", "RS Medika", "RS Prima", "RS Sentosa"],
        w1=[.26, .22, .20, .17, .15],
        dim2_label="Layanan", dim2=["IGD", "Rawat Jalan", "Rawat Inap", "Bedah"],
        w2=[.28, .38, .22, .12], aov=[750_000, 450_000, 4_200_000, 12_500_000],
        margin=[.18, .24, .28, .32], drift=[.03, .03, .04, .05],
        base_units=18500, m_rev="Pendapatan", m_prof="Surplus", m_units="Pasien",
        events=[{"period": "2026-07", "d2": ["IGD"], "mult": 1.35, "disc": 0.0},
                {"period": "2026-08", "d2": ["IGD"], "mult": 1.28, "disc": 0.0}]),
    "operational": dict(
        title="Operational Network — Anomaly Detection", seed=110,
        dim1_label="Site", dim1=["Plant A", "Plant B", "Plant C", "Plant D", "Plant E"],
        w1=[.26, .24, .22, .16, .12],
        dim2_label="Shift", dim2=["Pagi", "Siang", "Malam"],
        w2=[.38, .36, .26], aov=[520_000, 540_000, 480_000],
        margin=[.20, .21, .16], drift=[.015, .015, .01],
        base_units=42000, m_rev="Output", m_prof="Margin", m_units="Batch",
        events=[{"period": "2026-03", "mult": 1.22, "disc": 0.0}],
        slumps=[{"period": "2026-09", "d1": "Plant C", "d2": "Malam", "mult": .55}]),
}


def get_domain(name):
    if name not in DOMAINS:
        raise KeyError(f"unknown domain '{name}'. choose from: {', '.join(sorted(DOMAINS))}")
    return synth(DOMAINS[name])


def list_domains():
    return sorted(DOMAINS)
