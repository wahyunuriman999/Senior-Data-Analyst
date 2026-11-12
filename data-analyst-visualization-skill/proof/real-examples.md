# Real Examples (No Placeholders)

Worked examples with numbers that reconcile. Each shows: context → analysis →
visual → the fact-panel entry (number + formula, no narrative).

## Example 1: Variance Decomposition

**Context**: Revenue fell from Rp 38,80 M (Sep) to Rp 30,95 M (Okt): Δ = −Rp 7,85 M.

**Analysis** (price/volume/mix, per category):
- Price effect Σ(q₁·Δp) = −Rp 8,80 M — broad discounting (avg discount 4% → 11%).
- Volume effect ΔQ·p̄₀ = +Rp 14,11 M — units actually grew 9%.
- Mix effect = +Rp 2,54 M — shift toward higher-priced Electronics.
- Residual: −7,85 − (−8,80 + 14,11 + 2,54) = Rp 0,00 M ✓

**Visual**: Waterfall Sep → Harga → Volume → Mix → Okt, bars signed and colored.

**Fact panel**: `Dekomposisi −Rp 7,85 M | Harga −8,8 · Volume +14,11 · Mix +2,54 (Rp M) | rumus: Σ(q1·Δp) + ΔQ·p̄0 + Σ(p0−p̄0)·Δq_adj · residu Rp 0`

**Lesson**: the headline "revenue dropped" hides that volume grew — discounting,
not demand, drove the decline.

## Example 2: Cohort Retention

**Context**: SaaS, 12 monthly cohorts, 40.000 customers.

**Analysis**: Month-3 retention: Q1 cohorts 41%, Q2 cohorts 33% (−8 pp).
Structural break aligns with the March pricing change (annotated, not claimed causal).

**Visual**: Cohort heatmap, Q2 rows annotated at month-3 column.

**Fact panel**: `Retensi B3 kohort Q2 | 33% vs 41% (Q1): −8 pp | n=6 kohort/kuartal · break ditandai Mar`

## Example 3: Simpson's Paradox

**Context**: National conversion rose 2,1% → 2,4% (+0,3 pp).

**Analysis**: Per-region: 4 of 5 regions DECLINED (−0,1 to −0,4 pp). The aggregate
rose only because traffic mix shifted toward the highest-converting region
(Jakarta share 31% → 44%).

**Visual**: Grouped bars per region (declines visible) + aggregate line; annotation
on the mix shift.

**Fact panel**: `Konversi agregat +0,3 pp | 4/5 region turun | penyebab: mix Jakarta 31%→44% · agregat tidak diklaim sebagai tren`

**Lesson**: never headline the aggregate without the segment table beside it.

## Example 4: OATSIDE Field-Visit Dashboard — the minimum bar, audited live

**Context**: Operational field-force dashboard (OATSIDE oat-milk distribution,
Indonesia), observed 2026-11-09 via the public Apps Script link. Data
2026-01-02 s.d. 2026-11-09: **46.060 calls, 9.032 toko unik, 83 karyawan,
10 region, 3 role**. One long scrollable page: sticky filters (tanggal /
bulan / region / role / karyawan + reset + scope status), today summary
(123 calls, 27 petugas aktif), live visit feed (searchable, click row to
filter), 5 formula cards, Indonesia map + region ranking, role composition,
monthly trend, daily work-pattern area chart, top-5 travel ranking,
83-row employee leaderboard, top-100 store table.

**What it does right — this is the MINIMUM the skill must match:**

- Every formula card shows **mean + median (+P90) + exact formula**,
  e.g. `Jam kerja harian 7,97 J · median 8,16 J · P90 8,99 J ·
  MAX(Jam_Keluar) − MIN(Jam_Masuk) per tanggal aktif`;
  `Revisit 5,10x · formula: COUNT(Calls) & COUNT(DISTINCT Store_ID)`.
- Reconciliation that HOLDS: calls per region sum to exactly 46.060;
  calls per role 40.124 + 5.326 + 610 = 46.060 ✓;
  46.060 / 9.032 = 5,099 → **5,10x** ✓.
- Click-to-filter everywhere (map, bars, table rows, leaderboard names)
  with a visible scope status — the same interaction contract as Apex v2.

**Six flaws the skill's rules must catch (each was live on the page):**

1. **Distinct-count overlap, unexplained (F-04).** Toko unik per region
   sum to 6.506+441+421+374+310+309+235+212+162+78 = **9.048**, but total
   toko unik = **9.032** — selisih 16 toko yang tercatat di >1 region.
   Bukan bug hitung; bug PENJELASAN. Aturan v3: tampilkan
   `termasuk 16 toko di >1 region`.
2. **Shares don't sum (F-11).** Share region berjumlah **100,1%** tanpa
   catatan sisa pembulatan. Aturan v3: tampilkan `sisa pembulatan ±x pp`.
3. **Label contradicts data (F-11).** Subjudul role mengklaim "7 jabatan"
   padahal filter maupun grafik hanya punya 3 role. Aturan v3: label
   dihitung dari data, bukan ditulis tangan.
4. **Title promises a series that isn't there (F-11).** Judul tren
   menyebut "& Jam Kerja" tetapi legenda hanya punya Total Calls &
   Toko Unik. Aturan v3: judul = seri yang benar-benar tampil.
5. **In-progress records in the denominator (F-12).** Rata-rata durasi
   toko "hari ini" **27,0 m** vs rata-rata keseluruhan **88,8 m** —
   sebagian besar selisihnya adalah 23 kunjungan berstatus
   "Sedang di Toko" yang durasinya belum final. Aturan v3: record
   in-progress dikeluarkan dari rata-rata durasi (atau ditandai),
   dan hari berjalan memakai badge `periode berjalan`.
6. **Population contamination (metric-definition S5/S6).** Tabel Database
   Toko berisi entri non-toko: "UPLOAD PO (JADI / ESTIMASI) & PRINT OUT
   SELLING" (146 calls), "UPLOAD TANDA TERIMA MATERIAL EVENT" (45),
   "OFFICE INDOSAKTI" (41). Aturan v3: populasi & eksklusi tertulis di
   kontrak metrik; entri non-toko difilter atau dilabeli kategorinya.

**Bonus lesson — segmentation trap:** MD MOBILE 6,7 calls/hari vs SPG
MOBILE ±1,0 call/hari dengan avg visit ±500 menit BUKAN "SPG malas" —
SPG menetap di satu toko (model kerja beda). Satu tolok ukur untuk dua
model kerja = perbandingan yang salah (segmentation-cohort-funnel §1).

**Fact panel**: `Revisit 5,10x | 46.060 / 9.032 = 5,099 → 5,10x ✓ |
overlap toko antar-region 16 (F-04) · share region Σ 100,1% (sisa
pembulatan, F-11) · avg visit hari ini 27,0 m vs 88,8 m — 23 kunjungan
masih berjalan (F-12)`

**Lesson**: dashboard ini adalah patokan MINIMUM — bukan karena sempurna,
melainkan karena ia menunjukkan standar yang harus dilewati: rumus
ditampilkan, median menemani mean, angka menjumlah — DAN enam cacat di
atas adalah tepat jenis kesalahan yang skill v3 dibangun untuk menangkap.
