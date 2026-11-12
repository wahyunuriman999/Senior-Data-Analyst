#!/usr/bin/env node
/* test_engine_js.cjs — proof tests for the JS mirror in tools/apex/dashboard.tpl.js.
 *
 * Run:  node proof/runners/test_engine_js.cjs
 * Exit 0 = all identities hold.
 *
 * It reads the REAL dashboard.tpl.js, extracts the pure-function region
 * (div0 ... pearson — function declarations only, no DOM touched) and
 * asserts the same F-rules as proof/runners/test_engine_math.py pins for
 * the Python mirror. If the two mirrors ever drift, one of these two
 * suites fails first.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const assert = require("assert");

const tplPath = path.join(__dirname, "..", "..", "tools", "apex", "dashboard.tpl.js");
const src = fs.readFileSync(tplPath, "utf8");

// Slice the pure-function region: from "function div0" to the end of
// "function pearson(...) {...}". Brace-match to find its end.
function extract(fromMarker, toMarker) {
  const start = src.indexOf(fromMarker);
  assert(start !== -1, `marker not found: ${fromMarker}`);
  const toStart = src.indexOf(toMarker, start);
  assert(toStart !== -1, `marker not found: ${toMarker}`);
  let i = src.indexOf("{", toStart);
  let depth = 0;
  for (; i < src.length; i++) {
    if (src[i] === "{") depth++;
    else if (src[i] === "}") { depth--; if (depth === 0) break; }
  }
  return src.slice(start, i + 1);
}

const code = extract("function div0(", "function pearson(");

// Globals the extracted functions read when CALLED (not at definition time).
const KATEGORI = ["Elektronik", "Fashion"];
const sandbox = { KATEGORI };
const factory = new Function("KATEGORI", code + "\nreturn { div0, median, percentile, tCrit95, nextMonthLabels, anomalies, forecast, varianceDecomp, pearson };");
const F = factory(KATEGORI);

// F-02: growth from a zero base is null, never 0%.
assert.strictEqual(F.div0(100, 0), null);
assert.strictEqual(F.div0(0, 0), null);
assert.ok(Math.abs(F.div0(110, 100) - 0.1) < 1e-12);

// F-01: median / P90.
assert.strictEqual(F.median([3, 1, 2]), 2);
assert.strictEqual(F.median([4, 1, 3, 2]), 2.5);
assert.strictEqual(F.percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.9), 9);

// F-06: MAD flags the planted outlier, median stays put.
const xs = [100, 101, 99, 100, 102, 98, 100, 101, 99, 100, 100, 300];
assert.strictEqual(F.median(xs), 100);
const anoms = F.anomalies(xs.map((omzet, i) => ({ omzet, label: "B" + i, bulan: "2026-" + String(i + 1).padStart(2, "0") })));
assert.strictEqual(anoms.length, 1, "exactly the planted outlier is flagged");
assert.ok(Math.abs(anoms[0].zmod) > 3.5);

// F-05: variance decomposition residual is 0 (exact identity).
const rows = [
  { bulan: "2026-09", kategori: "Elektronik", units: 100, omzet: 1000 },
  { bulan: "2026-09", kategori: "Fashion", units: 50, omzet: 1000 },
  { bulan: "2026-10", kategori: "Elektronik", units: 110, omzet: 990 },
  { bulan: "2026-10", kategori: "Fashion", units: 45, omzet: 990 },
];
const vd = F.varianceDecomp(rows, "2026-09", "2026-10");
assert.ok(Math.abs(vd.residual) < 1e-6, `residual should be 0, got ${vd.residual}`);
assert.ok(Math.abs(vd.volEff + vd.mixEff + vd.priceEff - vd.dR) < 1e-6);

// F-08: t-interval (not 1.96), widens with horizon, lo clipped at 0.
assert.strictEqual(F.tCrit95(4), 2.776);
const vals = [100, 102, 101, 103, 102, 104, 103, 105, 104, 106, 105, 107]
  .map((omzet, i) => ({ omzet, bulan: "2026-" + String(i + 1).padStart(2, "0") }));
const fc = F.forecast(vals);
const widths = fc.points.map((p) => p.hi - p.lo);
assert.ok(widths[0] < widths[1] && widths[1] < widths[2], "interval must widen with horizon");
assert.ok(fc.points.every((p) => p.lo >= 0), "lo must be clipped at 0");
assert.ok(fc.backtest && fc.backtest.smape >= 0, "backtest must be present");
assert.ok(Math.abs(fc.tStar - 2.776) < 1e-12, "n=6 -> t*=2.776");

// F-08.5: future labels derived from data, roll over the year.
assert.deepStrictEqual(F.nextMonthLabels("2026-10", 3), ["Nov 26", "Des 26", "Jan 27"]);
assert.deepStrictEqual(F.nextMonthLabels("2026-12", 2), ["Jan 27", "Feb 27"]);

// F-07: Pearson bounds.
assert.ok(Math.abs(F.pearson([1, 2, 3], [2, 4, 6]) - 1) < 1e-12);

console.log("test_engine_js: all assertions passed (F-02, F-01, F-06, F-05, F-08, F-07)");
