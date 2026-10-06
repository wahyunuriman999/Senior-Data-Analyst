# Apex Engine — `tools/apex/`

Turns a tidy dataset (or a synthetic demo domain) into a **self-contained,
Apex v2–compliant dashboard HTML**: ECharts inlined, zero external requests,
universal click-to-filter, Fakta Terverifikasi panel, v2 palette.

This is the executable counterpart of the skill prose in
`data-analyst-visualization-skill/SKILL.md`. Where the skill tells an AI *how*
to build a dashboard, this engine *is* a dashboard builder following that
standard.

## Quick start

```bash
# 1. ECharts must be vendored once (Q-VIS-FATAL mandates inlining, no CDN):
mkdir -p tools/apex/vendor
curl -sSL -o tools/apex/vendor/echarts.min.js \
  https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js

# 2a. Synthetic demo (10 domains):
python3 tools/apex/apex_generate.py --demo sales --out sales.html
python3 tools/apex/apex_generate.py --list-domains   # finance sales marketing
                                                     # logistics product hr
                                                     # ecommerce risk health
                                                     # operational
# 2b. Your own CSV:
python3 tools/apex/apex_generate.py --csv data.csv --config cfg.json --out out.html

# 3. Validate:
python3 validator/apex_validate.py out.html   # expect 12/12
```

## CSV schema

`period,dim1,dim2,units,revenue,cost[,discount]`

- `period`: sortable period key, e.g. `2026-01`
- `dim1`, `dim2`: two filter dimensions (e.g. city, category)
- `units`, `revenue`, `cost`: numbers; `discount`: percent (optional)

## Config JSON (APEX_CFG)

```json
{
  "title": "Executive Sales — Indonesia",
  "currency": "Rp", "locale": "id-ID",
  "dim1": {"label": "Kota", "values": ["Jakarta", "Surabaya"]},
  "dim2": {"label": "Kategori", "values": ["Fashion", "FMCG"]},
  "time": {"label": "Bulan", "periods": ["2026-01", "2026-02"],
           "period_labels": {"2026-01": "Jan 26", "2026-02": "Feb 26"}},
  "metrics": {"revenue": "Omzet", "profit": "Profit",
              "margin": "Margin", "units": "Transaksi"},
  "provenance": "Sumber: ...",
  "freshness": "Jan–Feb 2026"
}
```

Omit `--config` and a generic one is inferred from the CSV
(`Dimensi 1/2`, `Revenue/Profit/Margin/Units`).

Without cohort data the cohort heatmap is skipped automatically
(demo domains always include synthetic cohorts).

## Files

| File | Role |
|---|---|
| `apex_generate.py` | CLI entry point |
| `demo_data.py` | 10 deterministic synthetic domains (seeded, declared synthetic) |
| `dashboard.tpl.js` | Generalized dashboard app (SSOT + filters + facts), labels via `APEX_CFG` |
| `build_page.py` | HTML assembler (v2 shell, palette, layout) |
| `vendor/` | `echarts.min.js` lives here (not committed; download once) |

## Design notes

- The app JS keeps a **canonical internal schema**
  (`kota/kategori/bulan/units/omzet/cogs/diskon_pct`); the CLI normalizes any
  input into it, and all display strings come from `APEX_CFG`. Ugly field
  names, zero user-visible leakage (verified by test).
- Every number on screen is computed from the filtered row set — no hardcode.
- The variance decomposition invariant `R0 + Σefek = R1` is asserted by the
  proof tests, not assumed.
