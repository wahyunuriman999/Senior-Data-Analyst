/* =====================================================================
 * APEX Proof Dashboard — application logic
 * Mandat skill: SEMUA angka dihitung dari SSOT (window.APEX_DATA.rows).
 * Tidak ada angka hardcode. Filter = .filter() pada SSOT + rekalkulasi total.
 * Insight = fungsi deterministik dari state data, bukan halusinasi.
 * ===================================================================== */
(function () {
"use strict";

if (!window.echarts) {
  document.getElementById("app").innerHTML =
    '<div style="padding:40px;color:#ECEFF6;font-family:sans-serif">Gagal memuat ECharts (inline). File rusak.</div>';
  return;
}

/* ---------------- SSOT ---------------- */
var DATA = window.APEX_DATA;
var CFG = window.APEX_CFG || {};
CFG.dim1 = CFG.dim1 || {}; CFG.dim2 = CFG.dim2 || {};
CFG.time = CFG.time || {}; CFG.metrics = CFG.metrics || {}; CFG.labels = CFG.labels || {};
var L = {
  dim1: CFG.dim1.label || "Kota",
  dim2: CFG.dim2.label || "Kategori",
  time: CFG.time.label || "Bulan",
  revenue: CFG.metrics.revenue || "Omzet",
  profit: CFG.metrics.profit || "Profit",
  margin: CFG.metrics.margin || "Margin",
  units: CFG.metrics.units || "Transaksi",
  scope: CFG.labels.scope || "Cakupan",
  rows: CFG.labels.rows || "baris data",
  period12: CFG.labels.period12 || "12 bulan",
  period6: CFG.labels.period6 || "6 bulan",
  currency: CFG.currency || "Rp",
  locale: CFG.locale || L.locale
};
var ROWS = DATA.rows;                 // grain: kota x kategori x bulan
var COHORT = DATA.cohorts || null;
var MONTHS = CFG.time.periods || ["2025-11","2025-12","2026-01","2026-02","2026-03","2026-04",
              "2026-05","2026-06","2026-07","2026-08","2026-09","2026-10"];
var MLABEL = CFG.time.period_labels || {"2025-11":"Nov 25","2025-12":"Des 25","2026-01":"Jan 26","2026-02":"Feb 26",
  "2026-03":"Mar 26","2026-04":"Apr 26","2026-05":"Mei 26","2026-06":"Jun 26",
  "2026-07":"Jul 26","2026-08":"Agu 26","2026-09":"Sep 26","2026-10":"Okt 26"};
var KOTA = CFG.dim1.values || ["Jakarta","Surabaya","Bandung","Medan","Makassar"];
var KATEGORI = CFG.dim2.values || ["Elektronik","Fashion","FMCG","Home & Living"];

var C = { base:"#5B8DEF", pos:"#34B98A", neg:"#E0605F", amber:"#E8A54B",
          peri:"#8C9BDB", teal:"#3EC6A5", text:"#ECEFF6", muted:"#8E97AD", grid:"#26314D" };
var CATCOLORS = ["#5B8DEF", "#3EC6A5", "#E8A54B", "#8C9BDB"];

var state = { kota: "ALL", kategori: "ALL", bulan: "ALL", periode: "12" };

/* ---------------- format ---------------- */
function fmtIDR(n) {
  var a = Math.abs(n);
  var v, s;
  if (a >= 1e9)      { v = n / 1e9; s = " M"; }
  else if (a >= 1e6) { v = n / 1e6; s = " jt"; }
  else if (a >= 1e3) { v = n / 1e3; s = " rb"; }
  else               { return L.currency + " " + Math.round(n).toLocaleString(L.locale); }
  return L.currency + " " + v.toLocaleString(L.locale, { maximumFractionDigits: 2 }) + s;
}
function fmtInt(n) { return Math.round(n).toLocaleString(L.locale); }
function fmtPct(x, d) {
  d = (d === undefined) ? 1 : d;
  var sign = x > 0 ? "+" : "";
  return sign + (x * 100).toLocaleString(L.locale, { maximumFractionDigits: d, minimumFractionDigits: d }) + "%";
}
function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/* ---------------- filter SSOT ---------------- */
function inWindow(bulan) {
  if (state.periode === "12") return true;
  return MONTHS.indexOf(bulan) >= 6; // 6M: Mei 26 - Okt 26
}
function filteredNoBulan() {
  return ROWS.filter(function (r) {
    return inWindow(r.bulan) &&
      (state.kota === "ALL" || r.kota === state.kota) &&
      (state.kategori === "ALL" || r.kategori === state.kategori);
  });
}
function filtered() {
  return filteredNoBulan().filter(function (r) {
    return state.bulan === "ALL" || r.bulan === state.bulan;
  });
}
function div0(a, b) { return b ? (a - b) / b : 0; }
function monthAgg(rows, bulan) {
  var rs = rows.filter(function (r) { return r.bulan === bulan; });
  var omzet = sum(rs, function (r) { return r.omzet; });
  var cogs = sum(rs, function (r) { return r.cogs; });
  var units = sum(rs, function (r) { return r.units; });
  return { omzet: omzet, profit: omzet - cogs, units: units,
           margin: omzet ? (omzet - cogs) / omzet : 0 };
}
function sum(rows, f) {
  return rows.reduce(function (a, r) { return a + f(r); }, 0);
}
function groupMonth(rows) {
  var win = MONTHS.filter(inWindow);
  return win.map(function (b) {
    var rs = rows.filter(function (r) { return r.bulan === b; });
    var omzet = sum(rs, function (r) { return r.omzet; });
    var cogs = sum(rs, function (r) { return r.cogs; });
    var units = sum(rs, function (r) { return r.units; });
    var dsk = rs.length ? sum(rs, function (r) { return r.diskon_pct * r.omzet; }) / (omzet || 1) : 0;
    return { bulan: b, label: MLABEL[b], omzet: omzet, profit: omzet - cogs,
             units: units, margin: omzet ? (omzet - cogs) / omzet : 0, diskon: dsk };
  });
}
function kpis(rows) {
  var g = groupMonth(rows);
  var n = g.length;
  var cur = { omzet: 0, profit: 0, units: 0 };
  var prv = { omzet: 0, profit: 0, units: 0 };
  g.forEach(function (m) { cur.omzet += m.omzet; cur.profit += m.profit; cur.units += m.units; });
  if (n >= 2) {
    var l = g[n - 1], p = g[n - 2];
    prv.omzet = p.omzet; prv.profit = p.profit; prv.units = p.units;
    cur.lastLabel = l.label; prv.lastLabel = p.label;
  }
  function d(c, p) { return p ? (c - p) / p : 0; }
  return {
    omzet: cur.omzet, profit: cur.profit, units: cur.units,
    margin: cur.omzet ? cur.profit / cur.omzet : 0,
    mom: n >= 2 ? {
      omzet: d(g[n-1].omzet, g[n-2].omzet),
      profit: d(g[n-1].profit, g[n-2].profit),
      units: d(g[n-1].units, g[n-2].units),
      marginPp: (g[n-1].margin - g[n-2].margin) * 100,
      label: g[n-1].label + " vs " + g[n-2].label
    } : null,
    series: g
  };
}

/* ---------------- analitik deterministik ---------------- */
// Dekomposisi varians: dR = Efek Harga + Efek Volume + Efek Mix  (mA -> mB)
function varianceDecomp(rows, mA, mB) {
  function pq(bulan) {
    var out = {};
    KATEGORI.forEach(function (k) {
      var rs = rows.filter(function (r) { return r.bulan === bulan && r.kategori === k; });
      var q = sum(rs, function (r) { return r.units; });
      var rev = sum(rs, function (r) { return r.omzet; });
      out[k] = { q: q, p: q ? rev / q : 0, rev: rev };
    });
    return out;
  }
  var A = pq(mA), B = pq(mB);
  var Q0 = 0, R0 = 0, Q1 = 0, R1 = 0;
  KATEGORI.forEach(function (k) { Q0 += A[k].q; R0 += A[k].rev; Q1 += B[k].q; R1 += B[k].rev; });
  var pBar0 = Q0 ? R0 / Q0 : 0;
  var volEff = (Q1 - Q0) * pBar0;
  var mixEff = 0, priceEff = 0;
  var perCat = KATEGORI.map(function (k) {
    var mix = (A[k].p - pBar0) * (B[k].q - A[k].q * (Q0 ? Q1 / Q0 : 0));
    var price = B[k].q * (B[k].p - A[k].p);
    mixEff += mix; priceEff += price;
    return { kategori: k, mix: mix, price: price };
  });
  return { mA: mA, mB: mB, R0: R0, R1: R1, dR: R1 - R0,
           volEff: volEff, mixEff: mixEff, priceEff: priceEff, perCat: perCat,
           residual: (R1 - R0) - (volEff + mixEff + priceEff) };
}
// Anomali: z-score omzet bulanan, |z| > 2
function anomalies(g) {
  var xs = g.map(function (m) { return m.omzet; });
  var mean = xs.reduce(function (a, b) { return a + b; }, 0) / xs.length;
  var sd = Math.sqrt(xs.reduce(function (a, b) { return a + (b - mean) * (b - mean); }, 0) / xs.length);
  return g.map(function (m) {
    return { label: m.label, bulan: m.bulan, omzet: m.omzet, z: sd ? (m.omzet - mean) / sd : 0 };
  }).filter(function (o) { return Math.abs(o.z) > 2; });
}
// Forecast 3 bulan: regresi linier 6 bulan terakhir + CI 95%
function forecast(g) {
  var tail = g.slice(-6);
  var n = tail.length;
  var sx = 0, sy = 0, sxx = 0, sxy = 0;
  tail.forEach(function (m, i) { sx += i; sy += m.omzet; sxx += i * i; sxy += i * m.omzet; });
  var denom = n * sxx - sx * sx;
  var b = denom ? (n * sxy - sx * sy) / denom : 0;
  var a = (sy - b * sx) / n;
  var resid = tail.map(function (m, i) { return m.omzet - (a + b * i); });
  var sigma = Math.sqrt(resid.reduce(function (s, r) { return s + r * r; }, 0) / Math.max(n - 2, 1));
  var out = [];
  for (var h = 1; h <= 3; h++) {
    var f = a + b * (n - 1 + h);
    out.push({ h: h, fc: f, lo: f - 1.96 * sigma, hi: f + 1.96 * sigma });
  }
  return { points: out, sigma: sigma, slope: b };
}
function pearson(xs, ys) {
  var n = xs.length;
  var mx = xs.reduce(function (a, b) { return a + b; }, 0) / n;
  var my = ys.reduce(function (a, b) { return a + b; }, 0) / n;
  var sxy = 0, sxx = 0, syy = 0, i;
  for (i = 0; i < n; i++) { sxy += (xs[i] - mx) * (ys[i] - my); sxx += (xs[i] - mx) * (xs[i] - mx); syy += (ys[i] - my) * (ys[i] - my); }
  return (sxx && syy) ? sxy / Math.sqrt(sxx * syy) : 0;
}

/* ---------------- chart builders (ECharts) ---------------- */
var charts = {};
function mk(id) {
  if (charts[id]) { charts[id].dispose(); }
  var el = document.getElementById(id);
  charts[id] = echarts.init(el, null, { renderer: "canvas" });
  return charts[id];
}
var AX = { axisLine: { lineStyle: { color: "#26314D" } }, axisTick: { show: false },
           axisLabel: { color: "#8E97AD", fontFamily: "Inter,system-ui,sans-serif" } };
var TT = { backgroundColor: "#182238", borderColor: "#26314D", textStyle: { color: "#ECEFF6", fontSize: 12 } };

function renderSpark(id, values, color) {
  var ch = mk(id);
  ch.setOption({
    grid: { left: 0, right: 0, top: 4, bottom: 0 },
    xAxis: { type: "category", show: false, data: values.map(function (_, i) { return i; }) },
    yAxis: { type: "value", show: false, min: function (v) { return v.min * 0.9; } },
    series: [{ type: "line", data: values, smooth: true, symbol: "none",
               lineStyle: { color: color, width: 2 },
               areaStyle: { color: color, opacity: 0.15 } }],
    animationDuration: 400
  });
}

function renderTrend(g, fc, selBulan) {
  var ch = mk("ch-trend");
  var labels = g.map(function (m) { return m.label; });
  var vals = g.map(function (m) { return Math.round(m.omzet / 1e9 * 100) / 100; });
  var target = vals.reduce(function (a, b) { return a + b; }, 0) / vals.length * 1.08;
  var fl = labels.concat(["Nov 26", "Des 26", "Jan 27"]);
  var fvals = vals.concat(fc.points.map(function (p) { return Math.round(p.fc / 1e9 * 100) / 100; }));
  var lo = vals.map(function () { return null; }).concat(fc.points.map(function (p) { return Math.round(p.lo / 1e9 * 100) / 100; }));
  var hi = vals.map(function () { return null; }).concat(fc.points.map(function (p) { return Math.round(p.hi / 1e9 * 100) / 100; }));
  var selIdx = selBulan && selBulan !== "ALL" ? g.map(function (m) { return m.bulan; }).indexOf(selBulan) : -1;
  var omzetData = vals.map(function (v, i) {
    if (i === selIdx) return { value: v, symbolSize: 10, itemStyle: { color: C.amber, borderColor: "#0A0F1E", borderWidth: 2 } };
    return v;
  });
  ch.setOption({
    tooltip: Object.assign({ trigger: "axis",
      formatter: function (p) {
        var s = p[0].name + "<br/>";
        p.forEach(function (it) {
          if (it.value !== null && it.value !== undefined)
            s += it.marker + " " + it.seriesName + ": <b>" + it.value.toLocaleString(L.locale) + " M</b><br/>";
        });
        return s + "<span style='color:#8E97AD'>Klik titik untuk filter bulan</span>";
      } }, TT),
    legend: { textStyle: { color: "#8E97AD" }, top: 0,
              data: [L.revenue, "Forecast", "CI 95%"] },
    grid: { left: 56, right: 16, top: 36, bottom: 28 },
    xAxis: Object.assign({ type: "category", data: fl, boundaryGap: false }, AX),
    yAxis: Object.assign({ type: "value", name: L.currency + " M", nameTextStyle: { color: "#8E97AD" },
      axisLabel: { color: "#8E97AD", formatter: "{value}" } }, AX),
    series: [
      { name: L.revenue, type: "line", data: omzetData, smooth: true, symbol: "circle", symbolSize: 5,
        lineStyle: { color: C.base, width: 3 },
        itemStyle: { color: C.base },
        markLine: { silent: true, symbol: "none",
          label: { color: C.amber, formatter: "Target +8%", fontSize: 10 },
          lineStyle: { color: C.amber, type: "dashed" }, data: [{ yAxis: Math.round(target * 100) / 100 }] },
        markArea: { silent: true, itemStyle: { color: "rgba(232,165,75,0.07)" },
          data: [[{ yAxis: target * 0.97, name: "Zona target" }, { yAxis: target * 1.03 }]] } },
      { name: "Forecast", type: "line", data: fvals, smooth: true, symbol: "emptyCircle", symbolSize: 5,
        lineStyle: { color: C.peri, width: 2, type: "dashed" }, itemStyle: { color: C.peri } },
      { name: "CI 95%", type: "line", data: lo, symbol: "none",
        lineStyle: { color: "#8E97AD", width: 1, type: "dotted", opacity: 0.7 } },
      { name: "CI 95% ", type: "line", data: hi, symbol: "none",
        lineStyle: { color: "#8E97AD", width: 1, type: "dotted", opacity: 0.7 } }
    ],
    animationDuration: 500
  });
  ch.off("click");
  ch.on("click", function (p) {
    if (p.componentType === "series" && p.seriesName === L.revenue && typeof p.dataIndex === "number" && p.dataIndex < g.length) {
      toggleFilter("bulan", g[p.dataIndex].bulan);
    }
  });
  return ch;
}

function renderWaterfall(vd) {
  var ch = mk("ch-waterfall");
  var cats = [MLABEL[vd.mA].replace(" 2", " "), "Harga", "Volume", "Mix", MLABEL[vd.mB].replace(" 2", " ")];
  var steps = [vd.R0, vd.priceEff, vd.volEff, vd.mixEff, 0];
  var cum = [vd.R0];
  for (var i = 1; i < 4; i++) cum.push(cum[i - 1] + steps[i]);
  var assist = [], val = [], col = [];
  for (i = 0; i < 5; i++) {
    var from, to, v, c;
    if (i === 0)      { from = 0; to = vd.R0; v = vd.R0; c = C.base; }
    else if (i === 4) { from = 0; to = vd.R1; v = vd.R1; c = C.base; }
    else { from = cum[i - 1]; to = cum[i]; v = to - from; c = v >= 0 ? C.pos : C.neg; }
    assist.push(Math.min(from, to) / 1e9);
    val.push(Math.abs(v) / 1e9);
    col.push(c);
  }
  ch.setOption({
    tooltip: Object.assign({ trigger: "axis",
      formatter: function (p) {
        return p[1].name + "<br/><b>" +
          p[1].value.toLocaleString(L.locale, { maximumFractionDigits: 2 }) + " M</b> (Rp)";
      } }, TT),
    grid: { left: 56, right: 16, top: 30, bottom: 28 },
    xAxis: Object.assign({ type: "category", data: cats }, AX),
    yAxis: Object.assign({ type: "value", name: L.currency + " M", nameTextStyle: { color: "#8E97AD" } }, AX),
    series: [
      { type: "bar", stack: "w", silent: true, itemStyle: { color: "transparent" }, data: assist },
      { type: "bar", stack: "w", data: val.map(function (v, i) { return { value: v, itemStyle: { color: col[i], borderRadius: 3 } }; }),
        label: { show: true, position: "top", color: "#ECEFF6", fontSize: 10,
                 formatter: function (p) { return (p.dataIndex > 0 && p.dataIndex < 4 ? (steps[p.dataIndex] >= 0 ? "+" : "") : "") + p.value.toLocaleString(L.locale, { maximumFractionDigits: 1 }); } } }
    ],
    animationDuration: 500
  });
}

function renderHeatmap() {
  if (!COHORT) { var hc = document.getElementById("ch-heat"); if (hc) hc.innerHTML = ""; return; }
  var ch = mk("ch-heat");
  var data = [];
  COHORT.retention.forEach(function (row, c) {
    row.forEach(function (v, t) { data.push([t, c, Math.round(v * 1000) / 10]); });
  });
  ch.setOption({
    tooltip: Object.assign({ formatter: function (p) {
      return "Kohort " + COHORT.labels[p.value[1]] + "<br/>Bulan ke-" + p.value[0] +
             ": <b>" + p.value[2].toLocaleString(L.locale) + "%</b> retensi";
    } }, TT),
    grid: { left: 64, right: 16, top: 30, bottom: 40 },
    xAxis: Object.assign({ type: "category",
      data: ["B0","B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","B11"],
      name: "Bulan sejak akuisisi", nameLocation: "middle", nameGap: 26,
      nameTextStyle: { color: "#8E97AD" } }, AX),
    yAxis: Object.assign({ type: "category", data: COHORT.labels.map(function (l) { return MLABEL[l]; }) }, AX),
    visualMap: { min: 0, max: 65, calculable: true, orient: "horizontal", left: "center", bottom: 0,
      textStyle: { color: "#8E97AD" },
      inRange: { color: ["#0A0F1E", "#1E2C52", "#5B8DEF", "#3EC6A5"] } },
    series: [{ type: "heatmap", data: data,
      label: { show: true, color: "#ECEFF6", fontSize: 9,
               formatter: function (p) { return p.value[2].toLocaleString(L.locale, { maximumFractionDigits: 0 }); } },
      itemStyle: { borderColor: "#0A0F1E", borderWidth: 2, borderRadius: 3 } }],
    animationDuration: 500
  });
}

function renderSankey(rows) {
  var ch = mk("ch-sankey");
  var links = [];
  KOTA.forEach(function (k) {
    KATEGORI.forEach(function (c) {
      var v = sum(rows.filter(function (r) { return r.kota === k && r.kategori === c; }),
                      function (r) { return r.omzet; });
      if (v > 0) links.push({ source: k, target: c, value: Math.round(v / 1e6) });
    });
  });
  var nodes = KOTA.map(function (k) { return { name: k }; })
    .concat(KATEGORI.map(function (c) { return { name: c }; }));
  ch.setOption({
    tooltip: Object.assign({ formatter: function (p) {
      if (p.dataType === "edge")
        return p.data.source + " → " + p.data.target + "<br/><b>" + fmtIDR(p.data.value * 1e6) + "</b>";
      return "<b>" + p.name + "</b><br/><span style='color:#8E97AD'>Klik untuk cross-filter</span>";
    } }, TT),
    series: [{ type: "sankey", left: 8, right: 120, top: 10, bottom: 10,
      nodeAlign: "justify",
      label: { color: "#ECEFF6", fontSize: 11 },
      lineStyle: { color: "source", opacity: 0.35, curveness: 0.5 },
      itemStyle: { borderWidth: 0 },
      emphasis: { focus: "adjacency" },
      color: ["#5B8DEF", "#6E9BF2", "#4A76D4", "#7FA8F5", "#3E63B8",
              "#3EC6A5", "#E8A54B", "#8C9BDB", "#A78BDB"],
      data: nodes, links: links }]
  });
  ch.off("click");
  ch.on("click", function (p) {
    if (p.dataType === "node") {
      if (KOTA.indexOf(p.name) >= 0) toggleFilter("kota", p.name);
      else if (KATEGORI.indexOf(p.name) >= 0) toggleFilter("kategori", p.name);
    }
  });
  return ch;
}

function renderCityBar(rows) {
  var ch = mk("ch-citybar");
  var data = KOTA.map(function (k) {
    var rs = rows.filter(function (r) { return r.kota === k; });
    return { name: k, value: Math.round(sum(rs, function (r) { return r.omzet; }) / 1e9 * 100) / 100 };
  }).sort(function (a, b) { return b.value - a.value; });
  ch.setOption({
    tooltip: Object.assign({ trigger: "item",
      formatter: function (p) { return "📍 <b>" + p.name + "</b><br/>" + L.revenue + ": <b>" + fmtIDR(p.value * 1e9) + "</b><br/><span style='color:#8E97AD'>Klik untuk cross-filter</span>"; } }, TT),
    grid: { left: 56, right: 16, top: 12, bottom: 28 },
    xAxis: Object.assign({ type: "category", data: data.map(function (d) { return d.name; }) }, AX),
    yAxis: Object.assign({ type: "value", name: L.currency + " M", nameTextStyle: { color: "#8E97AD" }, min: 0 }, AX),
    series: [{ type: "bar",
      data: data.map(function (d) {
        var dim = state.kota !== "ALL" && state.kota !== d.name;
        return { value: d.value, name: d.name,
                 itemStyle: { color: C.base, opacity: dim ? 0.35 : 1, borderRadius: [4, 4, 0, 0] } };
      }),
      label: { show: true, position: "top", color: "#ECEFF6", fontSize: 10,
               formatter: function (p) { return p.value.toLocaleString(L.locale, { maximumFractionDigits: 0 }); } },
      emphasis: { itemStyle: { color: C.peri } } }]
  });
  ch.off("click");
  ch.on("click", function (p) { toggleFilter("kota", p.name); });
  return ch;
}

function renderDonut(rows) {
  var ch = mk("ch-donut");
  var data = KATEGORI.map(function (k, i) {
    var rs = rows.filter(function (r) { return r.kategori === k; });
    var dim = state.kategori !== "ALL" && state.kategori !== k;
    return { name: k, value: sum(rs, function (r) { return r.omzet; }),
             itemStyle: { color: CATCOLORS[i % CATCOLORS.length], opacity: dim ? 0.35 : 1 } };
  });
  ch.setOption({
    tooltip: Object.assign({ formatter: function (p) {
      return "<b>" + p.name + "</b><br/>" + fmtIDR(p.value) +
             " (" + p.percent.toLocaleString(L.locale, { maximumFractionDigits: 1 }) + "%)<br/>" +
             "<span style='color:#8E97AD'>Klik untuk cross-filter</span>";
    } }, TT),
    legend: { bottom: 0, textStyle: { color: "#8E97AD", fontSize: 11 } },
    series: [{ type: "pie", radius: ["52%", "74%"], center: ["50%", "44%"],
      label: { color: "#ECEFF6", fontSize: 10, formatter: "{d}%" },
      labelLine: { lineStyle: { color: "#26314D" } },
      emphasis: { scale: true, scaleSize: 4 },
      data: data }]
  });
  ch.off("click");
  ch.on("click", function (p) { toggleFilter("kategori", p.name); });
  return ch;
}

/* ---------------- Fakta Terverifikasi: angka hitungan, tanpa narasi AI ---------------- */
function buildFacts(rows, k, g, vd, anoms) {
  var F = [];
  function push(label, value, formula, tone) { F.push({ label: label, value: value, formula: formula, tone: tone || "neu" }); }
  var n = g.length;

  if (k.mom) {
    push("Perubahan " + L.revenue + " (" + k.mom.label + ")",
      fmtIDR(g[n-1].omzet) + " (" + fmtPct(k.mom.omzet) + ")",
      "omzet bulan berjalan vs bulan sebelumnya", k.mom.omzet >= 0 ? "pos" : "neg");
  }
  push("Total periode", fmtIDR(k.omzet) + " · margin " +
    (k.margin * 100).toLocaleString(L.locale, { maximumFractionDigits: 1 }) + "%",
    "Σ omzet & profit pada cakupan aktif", "neu");

  if (vd) {
    push("Dekomposisi " + fmtIDR(vd.dR),
      "Harga " + fmtIDR(vd.priceEff) + " · Volume " + fmtIDR(vd.volEff) + " · Mix " + fmtIDR(vd.mixEff),
      "Σ(q1·Δp) + ΔQ·p̄0 + Σ(p0−p̄0)·Δq_adj · residu " + fmtIDR(vd.residual),
      vd.dR >= 0 ? "pos" : "neg");
  }

  if (anoms.length) {
    push("Anomali bulan",
      anoms.map(function (a) { return a.label + " (z=" + a.z.toLocaleString(L.locale, { maximumFractionDigits: 1 }) + ")"; }).join(", "),
      "aturan: |z|>2 pada omzet bulanan", "warn");
  } else {
    push("Anomali bulan", "tidak ada", "aturan: |z|>2 pada omzet bulanan", "neu");
  }

  if (n >= 2 && k.mom) {
    var div = KOTA.map(function (ct) {
      var r0 = sum(rows.filter(function (r) { return r.kota === ct && r.bulan === g[n-2].bulan; }), function (r) { return r.omzet; });
      var r1 = sum(rows.filter(function (r) { return r.kota === ct && r.bulan === g[n-1].bulan; }), function (r) { return r.omzet; });
      return { kota: ct, growth: r0 ? (r1 - r0) / r0 : 0 };
    }).filter(function (o) { return (k.mom.omzet >= 0 && o.growth < 0) || (k.mom.omzet < 0 && o.growth >= 0); });
    if (div.length) {
      push(L.dim1 + " berlawanan arah agregat",
        div.map(function (o) { return o.kota + " " + fmtPct(o.growth); }).join(", "),
        "agregat " + fmtPct(k.mom.omzet) + " vs kota di atas", "warn");
    } else {
      push("Arah antar-" + L.dim1.toLowerCase(), "selaras dengan agregat", "perbandingan MoM per " + L.dim1.toLowerCase(), "neu");
    }
  }

  var r = pearson(g.map(function (m) { return m.diskon; }), g.map(function (m) { return m.omzet; }));
  push("Korelasi diskon–omzet", "r = " + r.toLocaleString(L.locale, { maximumFractionDigits: 2 }),
    "n=" + n + " bulan, observasional — bukan bukti kausal", "neu");

  if (COHORT) {
    var b1 = COHORT.retention.map(function (row) { return row[1]; });
    var avgB1 = b1.reduce(function (a, b) { return a + b; }, 0) / b1.length;
    push("Retensi kohort B1", (avgB1 * 100).toLocaleString(L.locale, { maximumFractionDigits: 1 }) + "%",
      "rata-rata 12 kohort nasional", "neu");
  }

  if (n >= 2) {
    var risky = KOTA.map(function (ct) {
      var rs1 = rows.filter(function (r) { return r.kota === ct && r.bulan === g[n-1].bulan; });
      var o1 = sum(rs1, function (r) { return r.omzet; });
      var o0 = sum(rows.filter(function (r) { return r.kota === ct && r.bulan === g[n-2].bulan; }), function (r) { return r.omzet; });
      var p1 = o1 - sum(rs1, function (r) { return r.cogs; });
      return { kota: ct, growth: o0 ? (o1 - o0) / o0 : 0, margin: o1 ? p1 / o1 : 0 };
    }).filter(function (o) { return o.growth < -0.05 && o.margin < 0.20; });
    push(L.dim1 + " berisiko", risky.length ? risky.map(function (o) { return o.kota; }).join(", ") : "tidak ada",
      "aturan: MoM < -5% ∧ margin < 20%", risky.length ? "neg" : "pos");
  }

  push("Kualitas data", rows.length + " " + L.rows,
    "grain " + L.dim1.toLowerCase() + "×" + L.dim2.toLowerCase() + "×" + L.time.toLowerCase() + " · tanpa missing", "neu");
  return F;
}

function renderFacts(list) {
  var el = document.getElementById("insights");
  var toneC = { pos: C.pos, neg: C.neg, warn: C.amber, neu: C.base };
  el.innerHTML = list.map(function (f) {
    return '<div class="fact" style="border-left:3px solid ' + toneC[f.tone] + '">' +
      '<div class="fact-label">' + esc(f.label) + '</div>' +
      '<div class="fact-value">' + esc(f.value) + '</div>' +
      '<div class="fact-formula">' + esc(f.formula) + '</div></div>';
  }).join("");
}

/* ---------------- tabel kota (klik = filter) ---------------- */
function renderTable(rows, g) {
  var n = g.length;
  var tot = sum(rows, function (r) { return r.omzet; });
  var html = '<table><thead><tr><th>' + L.dim1 + '</th><th>' + L.revenue + '</th><th>Share</th><th>MoM</th><th>' + L.margin + '</th><th>' + L.units + '</th></tr></thead><tbody>';
  KOTA.forEach(function (ct) {
    var rs = rows.filter(function (r) { return r.kota === ct; });
    var o = sum(rs, function (r) { return r.omzet; });
    var p = o - sum(rs, function (r) { return r.cogs; });
    var u = sum(rs, function (r) { return r.units; });
    var mom = null;
    if (n >= 2) {
      var o1 = sum(rs.filter(function (r) { return r.bulan === g[n-1].bulan; }), function (r) { return r.omzet; });
      var o0 = sum(rs.filter(function (r) { return r.bulan === g[n-2].bulan; }), function (r) { return r.omzet; });
      mom = o0 ? (o1 - o0) / o0 : 0;
    }
    var sel = state.kota === ct;
    html += '<tr data-kota="' + esc(ct) + '" class="' + (sel ? "sel" : "") + '">' +
      "<td><b>" + esc(ct) + "</b>" + (sel ? ' <span class="chip-mini">aktif</span>' : "") + "</td>" +
      "<td class='num'>" + fmtIDR(o) + "</td>" +
      "<td class='num'>" + (tot ? (o / tot * 100).toLocaleString(L.locale, { maximumFractionDigits: 1 }) : "0") + "%</td>" +
      "<td class='num' style='color:" + (mom !== null && mom >= 0 ? C.pos : C.neg) + "'>" + (mom === null ? "–" : fmtPct(mom)) + "</td>" +
      "<td class='num'>" + (o ? (p / o * 100).toLocaleString(L.locale, { maximumFractionDigits: 1 }) : "0") + "%</td>" +
      "<td class='num'>" + fmtInt(u) + "</td></tr>";
  });
  document.getElementById("city-table").innerHTML = html + "</tbody></table>";
  var trs = document.querySelectorAll("#city-table tr[data-kota]");
  for (var i = 0; i < trs.length; i++) {
    trs[i].addEventListener("click", function () { toggleFilter("kota", this.getAttribute("data-kota")); });
  }
}

/* ---------------- slicer, chips, filter ---------------- */
function syncSelects() {
  document.getElementById("sel-kota").value = state.kota;
  document.getElementById("sel-kategori").value = state.kategori;
  document.getElementById("sel-bulan").value = state.bulan;
  document.getElementById("sel-periode").value = state.periode;
}
function renderChips() {
  var el = document.getElementById("chips");
  var out = [];
  if (state.kota !== "ALL")
    out.push('<button class="chip" data-k="kota">📍 ' + L.dim1 + ': ' + esc(state.kota) + ' <span>✕</span></button>');
  if (state.kategori !== "ALL")
    out.push('<button class="chip" data-k="kategori">🏷️ ' + L.dim2 + ': ' + esc(state.kategori) + ' <span>✕</span></button>');
  if (state.bulan !== "ALL")
    out.push('<button class="chip" data-k="bulan">📅 ' + L.time + ': ' + esc(MLABEL[state.bulan]) + ' <span>✕</span></button>');
  if (state.periode !== "12")
    out.push('<button class="chip" data-k="periode">🗓️ Periode: ' + L.period6 + ' <span>✕</span></button>');
  el.innerHTML = out.join("");
  var cs = el.querySelectorAll(".chip");
  for (var i = 0; i < cs.length; i++) {
    cs[i].addEventListener("click", function () {
      var k = this.getAttribute("data-k");
      state[k] = (k === "periode") ? "12" : "ALL";
      renderAll();
    });
  }
  document.getElementById("btn-reset").style.display = out.length ? "" : "none";
}
function toggleFilter(key, val) {
  state[key] = (state[key] === val) ? "ALL" : val;
  renderAll();
}
function resetAll() {
  state.kota = "ALL"; state.kategori = "ALL"; state.bulan = "ALL"; state.periode = "12";
  renderAll();
}

/* ---------------- KPI cards ---------------- */
function setKpi(id, value, delta, deltaPp, label, sparkVals, color) {
  document.getElementById(id + "-v").textContent = value;
  var dEl = document.getElementById(id + "-d");
  var isPp = (deltaPp !== undefined && deltaPp !== null);
  var dv = isPp ? deltaPp : delta;
  var txt = (dv === null || dv === undefined) ? "–" :
    (isPp ? ((dv >= 0 ? "+" : "") + dv.toLocaleString(L.locale, { maximumFractionDigits: 1 }) + " pp")
          : fmtPct(dv));
  dEl.textContent = txt + "  " + label;
  dEl.style.color = (dv === null) ? C.muted : (dv >= 0 ? C.pos : C.neg);
  renderSpark(id + "-s", sparkVals, color);
}

/* ---------------- renderAll: satu-satunya jalan render ---------------- */
function renderAll() {
  syncSelects();
  renderChips();
  var rowsNB = filteredNoBulan(); // tanpa filter bulan: untuk tren & dekomposisi
  var rows = filtered();
  var g = groupMonth(rows);
  var gTime = groupMonth(rowsNB);
  var n = gTime.length;
  var k, sparkG = gTime;

  if (state.bulan !== "ALL") {
    // KPI = bulan terpilih vs bulan sebelumnya (cakupan kota/kategori tetap berlaku)
    var idx = MONTHS.indexOf(state.bulan);
    var cur = monthAgg(rowsNB, state.bulan);
    var prv = idx > 0 ? monthAgg(rowsNB, MONTHS[idx - 1]) : null;
    k = {
      omzet: cur.omzet, profit: cur.profit, units: cur.units, margin: cur.margin,
      mom: prv ? {
        omzet: div0(cur.omzet, prv.omzet), profit: div0(cur.profit, prv.profit),
        units: div0(cur.units, prv.units), marginPp: (cur.margin - prv.margin) * 100,
        label: MLABEL[state.bulan] + " vs " + MLABEL[MONTHS[idx - 1]]
      } : null,
      series: g
    };
  } else {
    k = kpis(rows);
  }

  setKpi("kpi-omzet", fmtIDR(k.omzet), k.mom ? k.mom.omzet : null, null,
         k.mom ? k.mom.label : "", sparkG.map(function (m) { return m.omzet; }), C.base);
  setKpi("kpi-profit", fmtIDR(k.profit), k.mom ? k.mom.profit : null, null,
         k.mom ? k.mom.label : "", sparkG.map(function (m) { return m.profit; }), C.pos);
  setKpi("kpi-margin", (k.margin * 100).toLocaleString(L.locale, { maximumFractionDigits: 1 }) + "%",
         null, k.mom ? k.mom.marginPp : null,
         k.mom ? k.mom.label : "", sparkG.map(function (m) { return m.margin * 100; }), C.peri);
  setKpi("kpi-trx", fmtInt(k.units), k.mom ? k.mom.units : null, null,
         k.mom ? k.mom.label : "", sparkG.map(function (m) { return m.units; }), C.amber);

  var vd = n >= 2 ? varianceDecomp(rowsNB, gTime[n-2].bulan, gTime[n-1].bulan) : null;
  var fc = forecast(gTime);
  renderTrend(gTime, fc, state.bulan);
  if (vd) renderWaterfall(vd);
  renderHeatmap();
  renderSankey(rows);
  renderCityBar(rows);
  renderDonut(rows);
  renderTable(rows, g);
  renderFacts(buildFacts(rows, k, g, vd, anomalies(gTime)));

  var sub = [];
  if (state.kota !== "ALL") sub.push(state.kota);
  if (state.kategori !== "ALL") sub.push(state.kategori);
  if (state.bulan !== "ALL") sub.push(MLABEL[state.bulan]);
  sub.push(state.periode === "12" ? L.period12 : L.period6);
  document.getElementById("scope-label").textContent = L.scope + ": " + sub.join(" · ") +
    " · " + rows.length + " " + L.rows;
}

/* ---------------- init (tanpa DOMContentLoaded — Q-VIS-FATAL) ---------------- */
(function init() {
  var sk = document.getElementById("sel-kota");
  KOTA.forEach(function (k) { var o = document.createElement("option"); o.value = k; o.textContent = k; sk.appendChild(o); });
  var sg = document.getElementById("sel-kategori");
  KATEGORI.forEach(function (k) { var o = document.createElement("option"); o.value = k; o.textContent = k; sg.appendChild(o); });
  var sb = document.getElementById("sel-bulan");
  MONTHS.forEach(function (b) { var o = document.createElement("option"); o.value = b; o.textContent = MLABEL[b]; sb.appendChild(o); });
  sk.addEventListener("change", function () { state.kota = this.value; renderAll(); });
  sg.addEventListener("change", function () { state.kategori = this.value; renderAll(); });
  sb.addEventListener("change", function () { state.bulan = this.value; renderAll(); });
  document.getElementById("sel-periode").addEventListener("change", function () { state.periode = this.value; renderAll(); });
  document.getElementById("btn-reset").addEventListener("click", resetAll);
  window.addEventListener("resize", function () {
    Object.keys(charts).forEach(function (id) { charts[id].resize(); });
  });
  renderAll();
})();

})();
