#!/usr/bin/env python3
"""apex_generate.py — CSV/demo -> dashboard HTML berstandar Apex v2.

Usage:
  python3 apex_generate.py --demo sales --out sales.html
  python3 apex_generate.py --demo sales --out sales.html --echarts /path/echarts.min.js
  python3 apex_generate.py --csv data.csv --config cfg.json --out out.html
  python3 apex_generate.py --list-domains

CSV columns: period,dim1,dim2,units,revenue,cost[,discount]
Config JSON: the APEX_CFG object (see tools/apex/README.md for schema).

Output: single self-contained HTML (ECharts inlined, zero external requests).
Validate with: python3 validator/apex_validate.py <out.html>
"""
import argparse
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_page import build  # noqa: E402
import demo_data  # noqa: E402

with open(os.path.join(HERE, "dashboard.tpl.js"), encoding="utf-8") as f:
    APP_JS = f.read()

ECHARTS_CDN = "https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js"


def resolve_echarts(path):
    if path:
        cand = [path]
    else:
        cand = [os.path.join(HERE, "vendor", "echarts.min.js")]
    for c in cand:
        if os.path.isfile(c):
            with open(c, encoding="utf-8") as f:
                js = f.read()
            if "echarts" not in js[:2000].lower():
                continue
            return js
    sys.stderr.write(
        "ECharts not found. Download it once (Q-VIS-FATAL mandates inlining, no CDN):\n"
        f"  mkdir -p {os.path.join(HERE, 'vendor')} && \\\n"
        f"    curl -sSL -o {os.path.join(HERE, 'vendor', 'echarts.min.js')} {ECHARTS_CDN}\n"
        "then re-run, or pass --echarts /path/to/echarts.min.js\n")
    sys.exit(2)


def rows_from_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        rdr = csv.DictReader(f)
        need = {"period", "dim1", "dim2", "units", "revenue", "cost"}
        missing = need - set(rdr.fieldnames or [])
        if missing:
            sys.stderr.write(f"CSV missing columns: {sorted(missing)}\n")
            sys.exit(2)
        for i, r in enumerate(rdr, 1):
            try:
                rows.append({
                    "kota": r["dim1"].strip(), "kategori": r["dim2"].strip(),
                    "bulan": r["period"].strip(),
                    "units": int(float(r["units"])), "omzet": int(float(r["revenue"])),
                    "cogs": int(float(r["cost"])),
                    "diskon_pct": round(float(r.get("discount") or 0), 1),
                    "aov_list": int(float(r["revenue"]) / max(int(float(r["units"])), 1)),
                })
            except (ValueError, KeyError) as e:
                sys.stderr.write(f"CSV row {i}: bad value ({e}) — skipped\n")
    if not rows:
        sys.stderr.write("CSV produced no valid rows\n")
        sys.exit(2)
    return rows


def default_cfg_from_rows(rows):
    d1 = sorted({r["kota"] for r in rows})
    d2 = sorted({r["kategori"] for r in rows})
    pers = sorted({r["bulan"] for r in rows})
    return {
        "title": "Apex Dashboard", "currency": "Rp", "locale": "id-ID",
        "dim1": {"label": "Dimensi 1", "values": d1},
        "dim2": {"label": "Dimensi 2", "values": d2},
        "time": {"label": "Periode", "periods": pers,
                 "period_labels": {p: p for p in pers}},
        "metrics": {"revenue": "Revenue", "profit": "Profit",
                    "margin": "Margin", "units": "Units"},
        "provenance": "Data dari CSV pengguna. Validasi mandiri sebelum dipakai.",
        "freshness": f"{pers[0]} – {pers[-1]}",
    }


def main():
    ap = argparse.ArgumentParser(description="Generate an Apex v2 dashboard")
    ap.add_argument("--demo", help="synthetic demo domain")
    ap.add_argument("--list-domains", action="store_true")
    ap.add_argument("--csv", help="input CSV (period,dim1,dim2,units,revenue,cost[,discount])")
    ap.add_argument("--config", help="JSON config (APEX_CFG) for --csv mode")
    ap.add_argument("--out", required=False, help="output HTML path")
    ap.add_argument("--echarts", help="path to echarts.min.js")
    a = ap.parse_args()

    if a.list_domains:
        print("\n".join(demo_data.list_domains()))
        return 0
    if not a.out:
        sys.stderr.write("--out is required (try --list-domains)\n")
        return 2

    echarts_js = resolve_echarts(a.echarts)

    if a.demo:
        rows, cohorts, cfg = demo_data.get_domain(a.demo)
    elif a.csv:
        rows = rows_from_csv(a.csv)
        cohorts = None
        if a.config:
            with open(a.config, encoding="utf-8") as f:
                cfg = json.load(f)
        else:
            cfg = default_cfg_from_rows(rows)
    else:
        sys.stderr.write("specify --demo <domain> or --csv <file>\n")
        return 2

    html = build(rows, cohorts, cfg, echarts_js, APP_JS)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK -> {a.out} ({len(html) / 1024:.0f} KB, {len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
