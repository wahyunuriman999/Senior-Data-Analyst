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
.sidebar{width:248px;flex:none;background:#0C1327;border-right:1px solid var(--bd);padding:16px 12px 12px;position:sticky;top:0;height:100vh;display:flex;flex-direction:column;z-index:60}
.brand{display:flex;align-items:center;gap:10px;padding:2px 8px 14px;border-bottom:1px solid var(--bd)}
.brand-mark{flex:none;width:36px;height:36px;border-radius:10px;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;letter-spacing:.5px}
.brand-name{font-weight:800;font-size:13px;letter-spacing:.4px;line-height:1.25;min-width:0}
.brand-name small{display:block;font-weight:400;color:var(--mut);font-size:10.5px;letter-spacing:.2px}
.brand-collapse{margin-left:auto;flex:none;width:26px;height:26px;border-radius:7px;border:1px solid var(--bd);background:transparent;color:var(--mut);cursor:pointer;font-size:13px;line-height:1}
.brand-collapse:hover{background:var(--card2);color:var(--tx)}
.nav{margin-top:10px;display:flex;flex-direction:column;gap:2px;overflow-y:auto;flex:1;min-height:0}
.nav-group-label{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:var(--mut);padding:14px 10px 6px;white-space:nowrap}
.nav-item{display:flex;align-items:center;gap:10px;color:var(--mut);text-decoration:none;padding:7px 10px;border-radius:8px;font-size:12.5px;border-left:3px solid transparent;white-space:nowrap}
.nav-item:hover{background:var(--card2);color:var(--tx)}
.nav-item.on{background:rgba(91,141,239,.14);color:var(--tx);border-left-color:var(--blue);font-weight:600}
.nav-ico{flex:none;width:28px;height:28px;border-radius:8px;background:var(--card2);display:flex;align-items:center;justify-content:center;font-size:14px}
.nav-item.on .nav-ico{background:var(--blue)}
.nav-label{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis}
.nav-badge{flex:none;font-size:10px;font-weight:700;font-family:"JetBrains Mono",ui-monospace,Menlo,Consolas,monospace;background:var(--card2);border:1px solid var(--bd);color:var(--mut);border-radius:10px;padding:2px 7px}
.nav-item.on .nav-badge{background:rgba(91,141,239,.25);border-color:var(--blue);color:var(--tx)}
.side-user{display:flex;align-items:center;gap:10px;margin-top:12px;padding:10px;border-top:1px solid var(--bd)}
.side-avatar{flex:none;width:32px;height:32px;border-radius:50%;background:var(--card2);border:1px solid var(--bd);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:var(--tx)}
.side-user-meta{flex:1;min-width:0;line-height:1.35}
.side-user-meta b{display:block;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.side-user-meta span{font-size:10.5px;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:block}
.side-ver{flex:none;font-size:10px;font-weight:700;color:var(--mut);border:1px solid var(--bd);border-radius:10px;padding:2px 7px}
#app.rail .sidebar{width:68px;padding:16px 8px 12px}
#app.rail .brand-name,#app.rail .nav-group-label,#app.rail .nav-label,#app.rail .nav-badge,#app.rail .side-user-meta,#app.rail .side-ver{display:none}
#app.rail .brand{justify-content:center;padding:2px 0 14px}
#app.rail .brand-collapse{margin-left:0}
#app.rail .nav-item{justify-content:center;padding:7px 0;border-left-width:0}
#app.rail .side-user{justify-content:center;padding:10px 0}
.nav-item:focus-visible,.brand-collapse:focus-visible,#btn-sidebar-menu:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
#btn-sidebar-menu{display:none}
#sidebar-backdrop{display:none}
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
.s4,.s6,.s8{grid-column:span 12}.kpis{grid-template-columns:repeat(2,1fr)}
#btn-sidebar-menu{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:8px;border:1px solid var(--bd);background:var(--card);color:var(--tx);cursor:pointer;font-size:16px}
.sidebar{position:fixed;left:0;top:0;bottom:0;transform:translateX(-105%);transition:transform .18s ease;box-shadow:0 0 40px rgba(0,0,0,.5)}
#app.drawer-open .sidebar{transform:none}
#app.drawer-open #sidebar-backdrop{display:block;position:fixed;inset:0;background:rgba(4,7,16,.6);z-index:55}}
@media(prefers-reduced-motion:reduce){.sidebar{transition:none}}
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
    cohort_nav = ('<a href="#sec-kohort" class="nav-item" title="Kohort &amp; Alur"><span class="nav-ico">🗺️</span>'
                  '<span class="nav-label">Kohort &amp; Alur</span></a>') if has_cohort else ""

    # Sidebar v2 (design/sidebar.md): nav diturunkan dari section nyata di
    # halaman ini — tanpa link inventaris. Badge berisi hitungan build-time
    # yang jujur: jumlah periode (Tren) dan jumlah nilai dim1 (Tabel).
    sb_cfg = cfg.get("sidebar") or {}
    brand_cfg = sb_cfg.get("brand") or {}
    sb_mark = esc(brand_cfg.get("mark", "AX"))
    sb_name = esc(brand_cfg.get("name", "APEX ANALYST"))
    sb_tag = esc(brand_cfg.get("tag", "Apex Standard v2"))
    foot_cfg = sb_cfg.get("footer") or {}
    sb_user = esc(foot_cfg.get("user", "Analyst"))
    sb_role = esc(foot_cfg.get("role", "Apex Standard v2"))
    sb_initials = esc("".join(w[0] for w in sb_user.split()[:2]).upper() or "A")
    n_periods = len(cfg["time"].get("periods") or [])
    n_d1 = len(cfg["dim1"].get("values") or [])

    body = f"""
<div id="app">
  <aside class="sidebar" id="sidebar" aria-label="Navigasi dashboard">
    <div class="brand">
      <span class="brand-mark">{sb_mark}</span>
      <span class="brand-name">{sb_name}<small>{sb_tag}</small></span>
      <button id="btn-sidebar-collapse" class="brand-collapse" type="button" aria-label="Ciutkan sidebar" aria-expanded="true" title="Ciutkan sidebar">«</button>
    </div>
    <nav class="nav" aria-label="Bagian dashboard">
      <div class="nav-group-label">Analisis</div>
      <a href="#sec-tren" class="nav-item on" title="Tren &amp; Forecast"><span class="nav-ico">📈</span><span class="nav-label">Tren &amp; Forecast</span><span class="nav-badge">{n_periods}</span></a>
      <a href="#sec-var" class="nav-item" title="Dekomposisi Varians"><span class="nav-ico">🧮</span><span class="nav-label">Dekomposisi Varians</span></a>
      {cohort_nav}
      <div class="nav-group-label">Data</div>
      <a href="#sec-wilayah" class="nav-item" title="{d1l} &amp; {d2l}"><span class="nav-ico">📍</span><span class="nav-label">{d1l} &amp; {d2l}</span></a>
      <a href="#sec-tabel" class="nav-item" title="Tabel {d1l}"><span class="nav-ico">🗂️</span><span class="nav-label">Tabel {d1l}</span><span class="nav-badge">{n_d1}</span></a>
      <div class="nav-group-label">Verifikasi</div>
      <a href="#sec-insight" class="nav-item" title="Fakta Terverifikasi"><span class="nav-ico">✓</span><span class="nav-label">Fakta Terverifikasi</span></a>
    </nav>
    <div class="side-user">
      <span class="side-avatar">{sb_initials}</span>
      <span class="side-user-meta"><b>{sb_user}</b><span>{sb_role}</span></span>
      <span class="side-ver">v2</span>
    </div>
  </aside>
  <div id="sidebar-backdrop"></div>
  <div class="main">
    <div class="topbar">
      <button id="btn-sidebar-menu" type="button" aria-label="Buka menu navigasi" aria-expanded="false" aria-controls="sidebar">☰</button>
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
<title>APEX v2: {title}</title>
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
