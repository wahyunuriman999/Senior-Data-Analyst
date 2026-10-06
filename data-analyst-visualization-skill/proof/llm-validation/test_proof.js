#!/usr/bin/env node
/* Proof test: jalankan dashboard.js dengan DOM/ECharts stub, lalu verifikasi
 * klaim skill: SSOT, rekonsiliasi invarian waterfall, dan cross-filter reality.
 * Exit 0 = semua PASS, exit 1 = ada FAIL. */
"use strict";
const fs = require("fs");
const BASE = "/home/hatch/workspace/apex-proof";
const DATA = JSON.parse(fs.readFileSync(BASE + "/data.json", "utf8"));
const APP = fs.readFileSync(BASE + "/dashboard.js", "utf8");

// ---------- fake DOM ----------
const els = {};
function mkEl(id) {
  return { id: id, children: [], _html: "", _text: "", style: {}, value: "ALL",
    dataset: {},
    set innerHTML(v) { this._html = String(v); }, get innerHTML() { return this._html; },
    set textContent(v) { this._text = String(v); }, get textContent() { return this._text; },
    appendChild(c) { this.children.push(c); return c; },
    addEventListener() {}, getAttribute() { return null; },
    querySelectorAll() { return []; } };
}
function el(id) { if (!els[id]) els[id] = mkEl(id); return els[id]; }
global.document = {
  getElementById: el,
  createElement: (t) => mkEl("dyn-" + Math.random().toString(36).slice(2)),
  querySelectorAll: () => [],
};
// window === global (seperti browser), supaya window.echarts & window.APEX_DATA terlihat
global.window = global;
global.APEX_DATA = DATA;
global.addEventListener = () => {};

// ---------- fake echarts: tangkap setOption + click handler ----------
const chartOpts = {}, clickHandlers = {};
global.echarts = {
  init: (elm) => {
    const id = elm.id;
    return {
      setOption(o) { chartOpts[id] = o; },
      on(ev, fn) { if (ev === "click") clickHandlers[id] = fn; },
      off() {}, dispose() {}, resize() {},
    };
  },
};

// ---------- run app ----------
eval(APP);

// ---------- helpers ----------
let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; console.log("PASS  " + name); }
  else { fail++; console.log("FAIL  " + name + (detail ? " :: " + detail : "")); }
}
const sum = (rs, f) => rs.reduce((a, r) => a + f(r), 0);
function parseIDR(s) { // "Rp 448,64 M" | "Rp 842 jt" | "Rp 12,4 rb"
  const m = String(s).match(/Rp\s+([\d.,]+)\s*(M|jt|rb)?/);
  if (!m) return NaN;
  const v = parseFloat(m[1].replace(/\./g, "").replace(",", "."));
  const u = m[2] === "M" ? 1e9 : m[2] === "jt" ? 1e6 : m[2] === "rb" ? 1e3 : 1;
  return v * u;
}

// 1. SSOT: KPI omzet 12M = total rows
const totalAll = sum(DATA.rows, r => r.omzet);
const kpiShown = parseIDR(els["kpi-omzet-v"].textContent);
check("KPI omzet = SUM(SSOT)", Math.abs(kpiShown - totalAll) / totalAll < 0.01,
  `shown=${els["kpi-omzet-v"].textContent} expected≈${totalAll}`);

// 2. Waterfall invariant: R0 + price + vol + mix = R1 (dari opsi chart, bukan klaim teks)
const wf = chartOpts["ch-waterfall"];
const assist = wf.series[0].data, val = wf.series[1].data.map(d => d.value);
const R0 = assist[0] + val[0];
const R1 = assist[4] + val[4];
const dR = (val[1] + val[2] + val[3]); // harga+volume+mix (positif); tanda dari assist
// rekonstruksi bertanda: cum dari assist/val
let cum = R0; const eff = [];
for (let i = 1; i <= 3; i++) {
  const lo = assist[i], hi = assist[i] + val[i];
  eff.push(hi - lo >= 0 && assist[i] === Math.min(assist[i], hi) ? (val[i] * (assist[i] + val[i] <= R0 + 1e-9 && false ? -1 : 1)) : 0);
}
// cara langsung: efek bertanda dari selisih kumulatif
let c = R0; const signed = [];
for (let i = 1; i <= 3; i++) { const nxt = assist[i] + val[i]; signed.push(nxt - c); c = nxt; }
const recon = R0 + signed[0] + signed[1] + signed[2];
check("Waterfall invariant R0+Σefek=R1", Math.abs(recon - R1) / R1 < 1e-9,
  `R0=${R0} efek=${signed} R1=${R1} recon=${recon}`);

// 3. Cross-filter reality: klik Bandung di bar -> KPI = SUM Bandung saja
const totalBDG = sum(DATA.rows.filter(r => r.kota === "Bandung"), r => r.omzet);
clickHandlers["ch-citybar"]({ name: "Bandung" }); // toggle filter kota
const kpiBDG = parseIDR(els["kpi-omzet-v"].textContent);
check("Click-to-filter Bandung -> KPI terfilter", Math.abs(kpiBDG - totalBDG) / totalBDG < 0.01,
  `shown=${els["kpi-omzet-v"].textContent} expected≈${totalBDG}`);
// toggle lagi -> kembali ke ALL
clickHandlers["ch-citybar"]({ name: "Bandung" });
const kpiBack = parseIDR(els["kpi-omzet-v"].textContent);
check("Klik kedua = reset ke ALL", Math.abs(kpiBack - totalAll) / totalAll < 0.01,
  `shown=${els["kpi-omzet-v"].textContent}`);

// 4. Donut click -> filter kategori
const totalFashion = sum(DATA.rows.filter(r => r.kategori === "Fashion"), r => r.omzet);
clickHandlers["ch-donut"]({ name: "Fashion" });
const kpiF = parseIDR(els["kpi-omzet-v"].textContent);
check("Click-to-filter Fashion -> KPI terfilter", Math.abs(kpiF - totalFashion) / totalFashion < 0.01,
  `shown=${els["kpi-omzet-v"].textContent} expected≈${totalFashion}`);

// 5. Fakta Terverifikasi: angka hitungan + rumus/aturan, tanpa narasi AI
const html = els["insights"].innerHTML;
check("Panel fakta terisi (>=8 fakta)", (html.match(/fact-label/g) || []).length >= 8);
check("Aturan anomali eksplisit", html.includes("aturan: |z|&gt;2") || html.includes("aturan: |z|>2"));
check("Aturan risiko eksplisit", html.includes("aturan: MoM"));
check("Rumus dekomposisi tercantum", html.includes("residu"));
check("Tanpa persona AI", !/AI Data Storyteller|sebagai AI|menurut saya/i.test(html));
check("Tanpa kata 'menyebabkan'", !/menyebabkan/i.test(html));

// 5b. Klik titik tren -> filter bulan (Okt 26)
clickHandlers["ch-donut"]({ name: "Fashion" }); // reset filter Fashion dari test 4
const totalOkt = sum(DATA.rows.filter(r => r.bulan === "2026-10"), r => r.omzet);
clickHandlers["ch-trend"]({ componentType: "series", seriesName: "Omzet", dataIndex: 11, name: "Okt 26" });
const kpiOkt = parseIDR(els["kpi-omzet-v"].textContent);
check("Klik tren Okt 26 -> KPI = bulan itu", Math.abs(kpiOkt - totalOkt) / totalOkt < 0.01,
  `shown=${els["kpi-omzet-v"].textContent} expected≈${totalOkt}`);
clickHandlers["ch-trend"]({ componentType: "series", seriesName: "Omzet", dataIndex: 11, name: "Okt 26" }); // toggle off

// 5c. Klik node Sankey -> filter kota
const totalSBY = sum(DATA.rows.filter(r => r.kota === "Surabaya"), r => r.omzet);
clickHandlers["ch-sankey"]({ dataType: "node", name: "Surabaya" });
const kpiSBY = parseIDR(els["kpi-omzet-v"].textContent);
check("Klik node Sankey Surabaya -> KPI terfilter", Math.abs(kpiSBY - totalSBY) / totalSBY < 0.01,
  `shown=${els["kpi-omzet-v"].textContent} expected≈${totalSBY}`);
clickHandlers["ch-sankey"]({ dataType: "node", name: "Surabaya" }); // reset

// 6. Semua chart ter-render (10 instance incl. 4 sparkline)
const need = ["kpi-omzet-s","kpi-profit-s","kpi-margin-s","kpi-trx-s","ch-trend","ch-waterfall","ch-heat","ch-sankey","ch-citybar","ch-donut"];
check("10 chart instance ter-render", need.every(id => chartOpts[id]),
  "missing=" + need.filter(id => !chartOpts[id]).join(","));

// 7. Zero network request di HTML final (URL di komentar lisensi/SVG namespace dikecualikan)
const finalHTML = fs.readFileSync("/home/hatch/workspace/your_files/apex_skill_proof_dashboard.html", "utf8");
const netLoad = (finalHTML.match(/(src|href)="https?:[^"]*"|fetch\(\s*["']https?:|@import[^;]*|url\(\s*["']?https?:|<script[^>]+src=|<link[^>]+href="http/g) || []).length;
check("Zero network request di HTML final", netLoad === 0, netLoad + " pola pemuatan jaringan");

console.log(`\n${pass} PASS, ${fail} FAIL`);
process.exit(fail ? 1 : 0);
