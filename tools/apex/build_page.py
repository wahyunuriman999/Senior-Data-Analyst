#!/usr/bin/env python3
"""Assemble a self-contained Apex v2 dashboard HTML.

Inputs: rows (canonical schema), cohorts-or-None, cfg, echarts JS, app JS.
Output: single HTML file, zero external requests (Q-VIS-FATAL).
"""
import json

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0A0F1E;--card:#111A30;--card2:#182238;--bd:#26314D;--tx:#ECEFF6;--mut:#8E97AD;
--blue:#5B8DEF;--pos:#34B98A;--neg:#E0605F;--amber:#E8A54B}
html{background:var(--bg)}
body{background:var(--bg);color:var(--tx);font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:13px}
#app{display:flex;min-height:100vh}
.sidebar{width:216px;flex:none;background:#0C1327;border-right:1px solid var(--bd);padding:18px 12px;position:sticky;top:0;height:100vh}
.brand{font-weight:800;font-size:15px;letter-spacing:.4px;margin:2px 8px 4px}
.brand small{display:block;font-weight:400;color:var(--mut);font-size:10.5px;letter-spacing:.2px;margin-top:2px}
.nav{margin-top:14px;display:flex;flex-direction:column;gap:2px}
.nav a{color:var(--mut);text-decoration:none;padding:9px 10px;border-radius:8px;font-size:12.5px;display:block}
.nav a:hover{background:var(--card2);color:var(--tx)}
.nav a.on{background:var(--card2);color:var(--tx);border-left:3px solid var(--blue)}
.side-foot{margin-top:18px;padding:10px;font-size:10.5px;color:var(--mut);border:1px dashed var(--bd);border-radius:8px;line-height:1.5}
.main{flex:1;min-width:0;padding:18px 20px 30px}
.topbar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px}
.topbar h1{font-size:19px;font-weight:800}
.badge{font-size:10.5px;padding:4px 10px;border-radius:20px;border:1px solid var(--bd);color:var(--mut)}
.badge.syn{border-color:var(--amber);color:var(--amber)}
.scope{margin-left:auto;color:var(--mut);font-size:11.5px}
.slicer{position:sticky;top:0;z-index:50;background:rgba(10,15,30,.92);backdrop-filter:blur(12px);
border:1px solid var(--bd);border-radius:12px;padding:10px 14px;display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:14px}
.slicer label{font-size:11px;color:var(--mut)}
.slicer select{background:var(--card2);color:var(--tx);border:1px solid var(--bd);border-radius:8px;padding:7px 10px;font-size:12.5px}
#chips{display:flex;gap:8px;flex-wrap:wrap}
.chip{background:rgba(91,141,239,.14);border:1px solid var(--blue);color:var(--tx);border-radius:20px;
padding:5px 12px;font-size:11.5px;cursor:pointer}
.chip span{color:var(--neg);font-weight:700;margin-left:4px}
#btn-reset{background:transparent;border:1px solid var(--neg);color:var(--neg);border-radius:8px;
padding:7px 14px;font-size:12px;cursor:pointer;font-weight:600}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px}
.kpi{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:14px 16px 8px}
.kpi .k-label{font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:.6px}
.kpi .k-val{font-family:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
font-size:23px;font-weight:700;margin:6px 0 2px}
.kpi .k-delta{font-size:11.5px;margin-bottom:2px}
.kpi .spark{height:46px;width:100%}
.content{display:grid;grid-template-columns:minmax(0,1fr) 336px;gap:14px;align-items:start}
.bento{display:grid;grid-template-columns:repeat(12,1fr);gap:12px}
.card{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:14px 16px;min-width:0}
.card h3{font-size:13px;font-weight:700;margin-bottom:2px}
.card .sub{font-size:11px;color:var(--mut);margin-bottom:8px}
.s4{grid-column:span 4}.s6{grid-column:span 6}.s8{grid-column:span 8}.s12{grid-column:span 12}
#ch-trend{height:340px}#ch-waterfall{height:340px}#ch-heat{height:330px}
#ch-sankey{height:330px}#ch-citybar{height:300px}#ch-donut{height:300px}
.story{position:sticky;top:76px;background:rgba(24,34,56,.55);backdrop-filter:blur(12px);
border:1px solid var(--bd);border-radius:12px;padding:16px;max-height:calc(100vh - 100px);overflow:auto}
.story h2{font-size:13px;margin-bottom:4px}
.story .s-sub{font-size:11px;color:var(--mut);margin-bottom:12px}
.fact{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:10px 12px;margin-bottom:10px}
.fact-label{font-size:10.5px;color:var(--mut);text-transform:uppercase;letter-spacing:.5px;margin-bottom:3px}
.fact-value{font-family:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;font-size:14px;font-weight:700;margin-bottom:3px}
.fact-formula{font-size:10.5px;color:var(--mut);line-height:1.5}
table{width:100%;border-collapse:collapse;font-size:12px}
th{text-align:left;color:var(--mut);font-weight:600;font-size:11px;padding:8px 10px;border-bottom:1px solid var(--bd)}
td{padding:9px 10px;border-bottom:1px solid #1c2540}
td.num{font-family:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;text-align:right}
tbody tr{cursor:pointer}
tbody tr:hover{background:var(--card2)}
tbody tr.sel{background:rgba(91,141,239,.12)}
.chip-mini{font-size:9.5px;background:var(--blue);border-radius:10px;padding:2px 8px;color:#fff}
.hint{font-size:10.5px;color:var(--mut);margin-top:8px}
footer{margin-top:16px;color:var(--mut);font-size:11px;line-height:1.7;border-top:1px solid var(--bd);padding-top:12px}
@media(max-width:1100px){.content{grid-template-columns:1fr}.story{position:static;max-height:none}
.s4,.s6,.s8{grid-column:span 12}.kpis{grid-template-columns:repeat(2,1fr)}.sidebar{display:none}}
"""


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def build(rows, cohorts, cfg, echarts_js, app_js):
    d1l = esc(cfg["dim1"]["label"])
    d2l = esc(cfg["dim2"]["label"])
    tl = esc(cfg["time"]["label"])
    mrev = esc(cfg["metrics"]["revenue"])
    mprof = esc(cfg["metrics"]["profit"])
    mmarg = esc(cfg["metrics"]["margin"])
    munit = esc(cfg["metrics"]["units"])
    title = esc(cfg["title"])
    prov = esc(cfg["provenance"])
    fresh = esc(cfg.get("freshness", ""))
    has_cohort = bool(cohorts)

    cohort_card = ""
    if has_cohort:
        cohort_card = f"""
        <div class="card s6"><h3>Retensi Kohort Akuisisi</h3><div class="sub">% aktif per {tl.lower()} sejak akuisisi · kohort nasional · sel bukan dimensi filter</div><div id="ch-heat"></div></div>"""
    cohort_nav = '<a href="#sec-kohort">🗺️ Kohort &amp; Alur</a>' if has_cohort else ""

    body = f"""
<div id="app">
  <aside class="sidebar">
    <div class="brand">🦅 APEX ANALYST<small>Apex Standard v2</small></div>
    <nav class="nav">
      <a href="#sec-tren" class="on">📈 Tren &amp; Forecast</a>
      <a href="#sec-var">🧮 Dekomposisi Varians</a>
      {cohort_nav}
      <a href="#sec-wilayah">📍 {d1l} &amp; {d2l}</a>
      <a href="#sec-tabel">🗂️ Tabel {d1l}</a>
      <a href="#sec-insight">✓ Fakta Terverifikasi</a>
    </nav>
    <div class="side-foot">Standar: Apex v2<br>File: 100% mandiri (tanpa CDN)<br>Engine: tools/apex</div>
  </aside>
  <div class="main">
    <div class="topbar">
      <h1>{title}</h1>
      <span class="badge syn">DATA SINTETIS</span>
      <span class="badge">{fresh}</span>
      <span class="scope" id="scope-label"></span>
    </div>
    <div class="slicer">
      <label>{d1l} <select id="sel-kota"><option value="ALL">Semua {d1l}</option></select></label>
      <label>{d2l} <select id="sel-kategori"><option value="ALL">Semua {d2l}</option></select></label>
      <label>{tl} <select id="sel-bulan"><option value="ALL">Semua {tl}</option></select></label>
      <label>Periode <select id="sel-periode"><option value="12">12 {tl.lower()}</option><option value="6">6 {tl.lower()}</option></select></label>
      <div id="chips"></div>
      <button id="btn-reset">⟲ Reset / Clear All</button>
    </div>
    <div class="kpis">
      <div class="kpi"><div class="k-label">{mrev}</div><div class="k-val" id="kpi-omzet-v">–</div><div class="k-delta" id="kpi-omzet-d"></div><div class="spark" id="kpi-omzet-s"></div></div>
      <div class="kpi"><div class="k-label">{mprof}</div><div class="k-val" id="kpi-profit-v">–</div><div class="k-delta" id="kpi-profit-d"></div><div class="spark" id="kpi-profit-s"></div></div>
      <div class="kpi"><div class="k-label">{mmarg}</div><div class="k-val" id="kpi-margin-v">–</div><div class="k-delta" id="kpi-margin-d"></div><div class="spark" id="kpi-margin-s"></div></div>
      <div class="kpi"><div class="k-label">{munit}</div><div class="k-val" id="kpi-trx-v">–</div><div class="k-delta" id="kpi-trx-d"></div><div class="spark" id="kpi-trx-s"></div></div>
    </div>
    <div class="content">
      <div class="bento">
        <div class="card s8" id="sec-tren"><h3>Tren {mrev} + Forecast 3 {tl.lower()}</h3><div class="sub">Zona target +8% · forecast putus-putus + CI 95% · <b>klik titik untuk filter {tl.lower()}</b></div><div id="ch-trend"></div></div>
        <div class="card s4" id="sec-var"><h3>Dekomposisi Varians</h3><div class="sub">Δ{mrev} = Harga + Volume + Mix (2 {tl.lower()} terakhir) · komponen bukan dimensi filter</div><div id="ch-waterfall"></div></div>
        <div id="sec-kohort" style="display:contents">{cohort_card}</div>
        <div class="card s6"><h3>Alur {mrev}: {d1l} → {d2l}</h3><div class="sub">Sankey · <b>klik node untuk cross-filter</b></div><div id="ch-sankey"></div></div>
        <div class="card s6" id="sec-wilayah"><h3>{mrev} per {d1l}</h3><div class="sub">Klik bar untuk cross-filter seluruh dashboard</div><div id="ch-citybar"></div></div>
        <div class="card s6"><h3>Mix {d2l}</h3><div class="sub">Klik potongan untuk cross-filter</div><div id="ch-donut"></div></div>
        <div class="card s12" id="sec-tabel"><h3>Ringkasan per {d1l}</h3><div class="sub">Klik baris untuk cross-filter</div><div id="city-table"></div><div class="hint">{mmarg} = {mprof} / {mrev} · dihitung dari SSOT, bukan hardcode.</div></div>
      </div>
      <aside class="story" id="sec-insight">
        <h2>✓ Fakta Terverifikasi</h2>
        <div class="s-sub">Angka hasil hitungan dari data terfilter · tanpa narasi · tiap fakta mencantumkan rumus/aturannya</div>
        <div id="insights"></div>
      </aside>
    </div>
    <footer>
      <b>Provenance:</b> {prov}<br>
      Grain: {d1l.lower()} × {d2l.lower()} × {tl.lower()} ({len(rows)} baris) ·
      Standar: Apex v2 (Fakta Terverifikasi · click-to-filter dua arah · zero-CDN).
    </footer>
  </div>
</div>"""

    data_payload = {
        "meta": {"grain": f"{d1l} x {d2l} x {tl}", "currency": cfg.get("currency", "Rp"),
                 "provenance": cfg["provenance"]},
        "rows": rows,
    }
    if cohorts:
        data_payload["cohorts"] = cohorts

    assert "</script" not in echarts_js.lower()
    assert "</script" not in app_js.lower()
    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>APEX v2 — {title}</title>
<style>{CSS}</style>
</head>
<body>
{body}
<script>
/* ECharts 5.5.1 — Apache-2.0, di-inline per mandat Q-VIS-FATAL (tanpa CDN eksternal) */
{echarts_js}
</script>
<script>
window.APEX_DATA = {json.dumps(data_payload, separators=(",", ":"))};
</script>
<script>
window.APEX_CFG = {json.dumps(cfg, separators=(",", ":"), ensure_ascii=False)};
</script>
<script>
{app_js}
</script>
</body>
</html>"""
    return html
