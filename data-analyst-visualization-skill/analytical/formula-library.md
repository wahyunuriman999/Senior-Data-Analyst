# Formula Library — Rumus yang Bisa Dieksekusi & Diverifikasi
**Phase B — Analytical Brain | Engine B0 (wajib dibaca sebelum SEMUA analisis)**
**Depth Contract: FULL — file ini adalah satu-satunya sumber kebenaran rumus skill ini.**

> Masalah yang file ini perbaiki: skill v2 menyuruh AI "cek distribusi",
> "urai varians", "jangan klaim kausal" — tapi tidak memberi rumus, ambang
> batas, dan cara verifikasi yang bisa dieksekusi. Akibatnya AI menebak rumus,
> salah logika (growth dari basis 0 = 0%, rata-rata dari rata-rata, CI pakai
> 1,96 untuk n=6), dan analisisnya dangkal. Mulai v3, **setiap angka yang
> tampil di dashboard WAJIB bisa dilacak ke satu rumus di file ini**, dan
> setiap rumus WAJIB lolos cek rekonsiliasi di §F-00.
>
> Implementasi kode dari rumus-rumus ini hidup di `tools/apex/analytics.py`
> (Python, stdlib saja) dan `tools/apex/dashboard.tpl.js` (JS, mirror yang
> sama). Bila rumus di dokumen dan di kode berbeda, **kode yang diuji
> (`proof/runners/test_engine_math.py`) yang menang** — perbaiki dokumennya.

---

## F-00 — Aturan Emas (berlaku untuk SEMUA angka)

1. **Satu angka, satu rumus.** Setiap KPI / fakta / label grafik menampilkan
   rumus atau aturannya persis seperti kartu formula dashboard referensi
   (contoh: `SUM(Durasi_Toko) / Total_Calls`). Angka tanpa rumus tidak tayang.
2. **Rekonsiliasi sebelum tayang.** Total = jumlah segmennya; rasio =
   komponennya dibagi ulang dari grain; dekomposisi = jumlah efeknya.
   Selisih > toleransi (§F-11) = BLOCKED, bukan dibulatkan diam-diam.
3. **Tidak ada default diam-diam.** Basis 0, denominator 0, periode belum
   selesai, data belum lengkap — semuanya DITAMPILKAN sebagai `n/a` /
   `periode berjalan` / `data belum lengkap`, tidak pernah diisi 0.
4. **Mean tidak pernah sendirian.** Setiap rata-rata yang dilaporkan WAJIB
   ditemani median (dan P90 bila n ≥ 20). Mean tanpa median = klaim yang
   belum diperiksa (§F-01).
5. **Tulis satuan & populasi.** `Rp`, `%`, `pp`, `menit`, `calls/hari` —
   dan populasi penyebutnya (`per employee-day aktif`, `excl. toko 1`).
   Angka tanpa satuan = angka yang tidak bisa dicek.

---

## F-01 — Mean, Median, P90, IQR (distribusi dulu, rata-rata kemudian)

```
n         = COUNT(x)                       # n = jumlah observasi, bukan jumlah baris mentah
mean      = Σx / n
median    = nilai tengah setelah x diurutkan
            (n ganjil: x[(n+1)/2]; n genap: (x[n/2] + x[n/2+1]) / 2)
Q1, Q3    = persentil 25 dan 75 (metode linear / nearest-rank — tulis metodenya)
IQR       = Q3 − Q1
P90       = persentil 90
```

**Kapan pakai apa:**

| Situasi | Laporkan | Alasan |
|---|---|---|
| Distribusi simetris, tanpa outlier | mean + SD | mean efisien |
| Skewed / ada outlier / ada nilai 0 | **median + IQR** (mean hanya pelengkap) | mean ditarik ekor |
| "Berapa yang dialami sebagian besar?" | median | mean menjawab "berapa totalnya dibagi n", bukan "berapa yang tipikal" |
| "Seberapa ekstrem ekor atas?" | P90 / P95 | ekor tidak terlihat dari mean |
| n < 30 | median + rentang (min–max), **tanpa** klaim CI | CI dari n kecil tidak stabil |

**Contoh kerja (dari dashboard referensi, terverifikasi):**

```
Durasi visit per toko: mean 88,8 m · median 84,3 m → distribusi agak right-skewed,
  ekor atas (kunjungan SPG yang menetap) menarik mean ke atas. Yang "tipikal"
  adalah 84,3 m, bukan 88,8 m.
Jam kerja harian: mean 7,97 J · median 8,16 J · P90 8,99 J → laporkan ketiganya.
```

**Larangan:** jangan pernah melaporkan mean dari kolom yang masih berisi
record belum selesai / in-progress (lihat §F-12).

---

## F-02 — Growth: % change vs percentage points (pp)

```
growth %  g = (M₁ − M₀) / |M₀| × 100%
Δ pp      = M₁% − M₀%                        # hanya bila M adalah persentase
```

| Kasus | Aturan |
|---|---|
| M₀ = 0 | **g = n/a — basis 0.** Jangan tampilkan 0%. 0% artinya "tidak berubah", padahal dari 0 ke berapa pun adalah tak terdefinisi. |
| M₀ < 0 (mis. laba negatif) | Tampilkan g dengan flag `⚠ basis negatif — arah terbalik`. Jangan bandingkan lintas tanda tanpa flag. |
| M dalam % (margin 20% → 25%) | Laporkan **+5 pp**, dan bila perlu tambahkan `(+25% relatif)`. Jangan tulis "+5%" saja — itu ambigu. |
| Perbandingan dua periode beda panjang | Normalisasi dulu (per hari / per minggu). Jangan bandingkan total 9 hari vs total 31 hari. |

**Bug yang file ini bunuh:** `div0(a, b) = b ? (a−b)/b : 0` — growth dari basis 0
dilaporkan 0%. Di engine v3, pembagi 0 mengembalikan `null` dan UI menampilkan `n/a`.

---

## F-03 — Rasio & rata-rata tertimbang: hitung ulang dari grain, jangan rata-ratakan rasio

```
margin        = Σ profit / Σ revenue            # BUKAN AVG(margin per baris)
AOV           = Σ revenue / Σ units             # BUKAN AVG(revenue/units per baris)
conversion    = COUNTD(pembilang) / COUNTD(penyebut)   # populasi harussama (§metric-definition-engine S5)
weighted mean = Σ(xᵢ · wᵢ) / Σ wᵢ
```

**Bukti kenapa AVG-of-AVG salah:** dua kota, A: revenue 100 dari 10 unit
(AOV 10), B: revenue 1.000 dari 10 unit (AOV 100). AVG(AOV) = 55 — salah.
AOV benar = 1.100 / 20 = 55? Di contoh ini kebetulan sama karena unit sama.
Ubah B jadi 100 unit: AVG(AOV) tetap 55, AOV benar = 1.100 / 110 = 10.
**Selisih 5,5x.** Itulah kenapa field `aov_list` per-baris dihapus dari
engine v3: ia mengundang AVG yang salah.

**Aturan agregasi (ringkas dari metric-definition-engine S7):**

| Metrik | Bisa di-SUM lintas dimensi? | Cara roll-up yang benar |
|---|---|---|
| Revenue, units, profit, cost | Ya | SUM |
| Margin %, conversion %, rate apa pun | **Tidak** | Hitung ulang dari Σ komponen |
| AOV, rata-rata apa pun | **Tidak** | Σ pembilang / Σ penyebut |
| COUNT DISTINCT (user, toko, karyawan) | **Tidak** | COUNT DISTINCT ulang dari grain (§F-04) |

---

## F-04 — COUNT DISTINCT tidak aditif (jebakan "jumlah segmen ≠ total")

```
COUNTD_total  = COUNT(DISTINCT id) atas SELURUH data
Σ COUNTD_segmen ≥ COUNTD_total   # SELALU ≥, karena satu id bisa muncul di >1 segmen
```

**Contoh kerja (dashboard referensi, angka teramati):**

```
Toko unik per region: 6.506 + 441 + 421 + 374 + 310 + 309 + 235 + 212 + 162 + 78
  = 9.048, SEMENTARA total toko unik = 9.032. Selisih 16.
Penjelasan: 16 toko tercatat di >1 region (pindah region / salah kode region).
  Ini BUKAN bug tampilan — ini sifat COUNT DISTINCT. Yang salah adalah
  menampilkan keduanya tanpa catatan overlap.
Aturan v3: bila Σ COUNTD segmen ≠ COUNTD total, tampilkan
  `termasuk N id yang muncul di >1 segmen` — jangan biarkan pembaca
  mengira tabelnya tidak menjumlah.
```

**Cek sebaliknya (yang HARUS menjumlah):** COUNT biasa (bukan distinct)
HARUS menjumlah persis. Contoh terverifikasi dari referensi:
`40.124 (MD) + 5.326 (SPG) + 610 (TL) = 46.060 calls` ✓ dan
`Σ calls per region = 46.060` ✓. Bila COUNT tidak menjumlah → ada baris
hilang / terfilter ganda → BLOCKED.

---

## F-05 — Dekomposisi varians harga / volume / mix (identitas harus nol residu)

Untuk dua periode (0 = awal, 1 = akhir), per kategori k:

```
p_k  = revenue_k / units_k        (harga rata-rata kategori k)
q_k  = units_k
Q    = Σ q_k                      (total units)
R    = Σ revenue_k                (total revenue)
p̄₀   = R₀ / Q₀                    (harga rata-rata tertimbang periode 0)

Efek Volume  = (Q₁ − Q₀) · p̄₀
Efek Harga   = Σ q₁ₖ · (p₁ₖ − p₀ₖ)
Efek Mix     = Σ (p₀ₖ − p̄₀) · (q₁ₖ − q₀ₖ · Q₁/Q₀)
ΔR           = R₁ − R₀
RESIDU       = ΔR − (Volume + Harga + Mix)   # HARUS = 0 (dalam toleransi pembulatan)
```

**Kenapa residu nol:** suku-suku di atas adalah pemecahan aljabar eksak dari
`Σ q₁p₁ − Σ q₀p₀` (bukti: uraikan `q₁−q₀` menjadi komponen skala
`q₀·(Q₁/Q₀−1)` dan komponen mix; suku `p̄₀·Σ(...)` lenyap karena jumlah
penyesuaian mix = 0). Bila implementasi menghasilkan residu ≠ 0, rumus
implementasinya salah — bukan "residu statistik". Tampilkan residu di panel
Fakta; residu ≠ 0 = BLOCKED.

**Contoh kerja (sudah ada di proof/real-examples.md Ex.1):**

```
ΔR = −Rp 7,85 M = Harga −8,80 + Volume +14,11 + Mix +2,54 · residu Rp 0,00 ✓
```

**Syarat:** harga p_k harus dihitung dari grain yang sama di kedua periode;
kategori yang muncul hanya di satu periode (q₀ₖ = 0 atau q₁ₖ = 0) ditangani
sebagai mix + harga penuh kategori itu, dan dicatat — jangan di-drop diam-diam.

---

## F-06 — Outlier & anomali: z-score klasik vs MAD (robust)

```
# Klasik — hanya bila n ≥ 30 dan distribusi kira-kira simetris:
SD sampel  s = √( Σ(x − x̄)² / (n − 1) )     # penyebut (n−1), BUKAN n
z          = (x − x̄) / s
flag       = |z| > 2                          # investigasi; |z| > 3 = ekstrem

# Robust — default bila n kecil, skewed, atau outlier dicurigai:
median     = med(x)
MAD        = med(|x − med(x)|)
z_mod      = 0,6745 · (x − med(x)) / MAD      # 0,6745 = Φ⁻¹(0,75)
flag       = |z_mod| > 3,5
```

**Kenapa dua versi:** z klasik memakai mean & SD yang ikut ditarik oleh
outlier itu sendiri (outlier menyembunyikan dirinya). Pada deret bulanan
n=12, satu bulan promo besar menaikkan mean & SD sehingga z-nya sendiri
mengecil. **Engine v3 memakai MAD sebagai default** dan menampilkan z
klasik hanya sebagai pembanding.

**Aturan tindak lanjut:** outlier TIDAK PERNAH dihapus diam-diam. Pilihan
yang sah: (a) tampilkan dengan anotasi, (b) tampilkan analisis dengan &
tanpa outlier berdampingan, (c) winsorize dengan catatan eksplisit.
Menghapus tanpa catatan = FATAL (Q-DATA-011).

---

## F-07 — Korelasi: hitung, laporkan n, jangan klaim kausal

```
Pearson r = Σ(x−x̄)(y−ȳ) / √( Σ(x−x̄)² · Σ(y−ȳ)² )     # r ∈ [−1, 1]
```

| |r|| Interpretasi bahasa (bukan klaim) | Syarat tayang |
|---|---|---|
| < 0,3 | lemah / tidak terlihat | sebutkan n |
| 0,3–0,7 | sedang | sebutkan n + scatter terlihat |
| > 0,7 | kuat | sebutkan n + cek outlier (satu titik bisa menciptakan r) |

**Wajib menyertai setiap r:** `n`, scatter/plot, dan kalimat
`"berkorelasi, belum tentu menyebabkan — confounder yang mungkin: …"`.
**Dilarang:** kata `menyebabkan`, `mendorong`, `akibat` untuk data observasional.

**Cek Simpson (wajib sebelum headline tren):**

```
1. Hitung tren agregat.
2. Hitung tren per segmen (region / kategori / kohort / channel).
3. Bila arah agregat ≠ arah mayoritas segmen → HEADLINE DILARANG memakai
   agregat saja. Tampilkan tabel segmen di samping agregat + kalimat
   "agregat naik karena mix bergeser ke segmen X (share a% → b%)".
```

Contoh kerja: lihat proof/real-examples.md Ex.3 (konversi agregat +0,3 pp
padahal 4/5 region turun — mix Jakarta 31% → 44%).

---

## F-08 — Forecast: regresi + interval prediksi t (bukan 1,96) + backtest

```
# OLS atas n titik terakhir (default n = 6; tulis n-nya):
b = (n·Σxy − Σx·Σy) / (n·Σx² − (Σx)²)
a = (Σy − b·Σx) / n
ŷ = a + b·x
σ = √( Σ(y − ŷ)² / (n − 2) )                 # residual SD, df = n−2

# Interval PREDIKSI 95% untuk horizon h (x₀ = titik forecast):
t*  = t(0,975; df = n − 2)                   # BUKAN 1,96 bila n kecil
      df=4 → 2,776 · df=5 → 2,571 · df=6 → 2,447 · df=10 → 2,228 · df≥30 → 1,96
SE_pred = σ · √( 1 + 1/n + (x₀ − x̄)² / Σ(x − x̄)² )
PI  = ŷ ± t* · SE_pred                        # melebar seiring horizon — WAJIB
```

**Bug yang file ini bunuh (engine v2):** `lo/hi = f ± 1,96·σ`.
Tiga kesalahan sekaligus: (1) 1,96 adalah z normal, padahal n=6 → t*=2,776
(interval jadi ~30% terlalu sempit); (2) tanpa suku leverage
`(x₀−x̄)²/…` sehingga interval tidak melebar per horizon; (3) tanpa `+1`
di dalam akar — itu interval untuk rata-rata, bukan untuk observasi
mendatang. Plus: label bulan forecast di-hardcode.

**Aturan forecast v3:**

1. Tampilkan SELALU: titik forecast + PI 80% & 95% + `n`, `σ`, dan
   **hasil backtest** (lihat bawah). Point forecast tanpa interval = FATAL.
2. **Backtest wajib:** latih di `n−3` titik pertama, prediksi 3 titik
   terakhir yang sudah diketahui, laporkan:
   `MAE = Σ|y−ŷ|/3` dan `sMAPE = (200%/3)·Σ|y−ŷ|/(|y|+|ŷ|)`
   (sMAPE, bukan MAPE — MAPE meledak bila aktual = 0).
   Bila sMAPE backtest > 20% → forecast ditandai `⚠ tidak andal — backtest sMAPE x%`.
3. **Clip:** metrik yang nilainya tidak bisa negatif (revenue, calls, units)
   → `lo = max(0, lo)`. Forecast negatif untuk revenue adalah bug, bukan hasil.
4. **Musiman & break:** bila data punya musiman yang terlihat (Desember
   melonjak tiap tahun) atau structural break, regresi linier mentah
   DILARANG sebagai satu-satunya model — tampilkan sebagai `baseline naif`
   dan catat keterbatasannya. Jangan pernah menyajikan baseline naif
   seolah-olah model musiman.
5. **Label dinamis:** label bulan forecast diturunkan dari daftar periode
   data (periode terakhir + 1, +2, +3 bulan kalender). Hardcode label
   bulan = FATAL.

---

## F-09 — Kohort & retensi: denominator tetap, periode belum lengkap = NA

```
retensi(kohort c, umur t) = aktif(c, t) / ukuran_kohort(c)
```

- `ukuran_kohort(c)` = jumlah anggota saat akuisisi — **tetap di semua kolom**.
  Jangan pernah memakai "anggota yang masih teramati di umur t" sebagai penyebut.
- Sel yang umur-nya melewati tanggal data terakhir = `NA (periode belum
  lengkap)`, BUKAN 0. 0 artinya "semua churn", NA artinya "belum bisa diamati".
- Bandingkan kohort hanya pada umur yang sama (B3 vs B3), jangan B3 satu
  kohort vs B6 kohort lain.

---

## F-10 — Funnel: strict vs loose, konversi per langkah

```
konversi langkah  = n(langkah k) / n(langkah k−1)     # penyebut = langkah sebelumnya
konversi total    = n(akhir) / n(awal) = Π konversi langkah
```

- **Strict funnel:** langkah k hanya dihitung bila timestamp-nya > langkah
  k−1 untuk user yang sama. **Loose funnel:** cukup pernah terjadi.
  Tulis jenisnya di samping angka — keduanya sah, mencampurnya tidak sah.
- Diagnosis drop-off: laporkan langkah dengan penurunan absolut TERBESAR
  dan penurunan relatif TERBESAR — keduanya, karena bisa berbeda.

---

## F-11 — Pembulatan & rekonsiliasi: jumlah harus cocok

| Cek | Toleransi | Bila gagal |
|---|---|---|
| Σ share % segmen | 100% ± 0,1 pp (sisa pembulatan) | Tampilkan `sisa pembulatan ±x pp`; bila > 0,1 pp → ada segmen hilang |
| Σ COUNT segmen vs total | persis (= 0 selisih) | BLOCKED — baris hilang / filter ganda |
| Σ COUNTD segmen vs total | ≥ total; selisih = overlap, dicatat (§F-04) | Bila selisih tidak dijelaskan → BLOCKED |
| Dekomposisi (§F-05) | residu = 0 (± pembulatan Rp) | BLOCKED — rumus implementasi salah |
| KPI vs tabel vs grafik (satu filter) | semua sama persis | BLOCKED — SSOT bocor (Q-VIS-ANALYTICAL) |

**Contoh cacat nyata (referensi):** share region berjumlah 100,1% tanpa
catatan sisa pembulatan; judul tren menjanjikan seri "Jam Kerja" yang tidak
ada di legenda; subjudul klaim "7 jabatan" padahal data hanya punya 3 role.
Ketiganya ditangkap oleh cek F-11 + cek konsistensi label-vs-data di validator.

---

## F-12 — Periode berjalan & record belum selesai

1. **Hari/bulan berjalan DITANDAI.** Rata-rata "hari ini" yang dihitung
   pukul 12:00 dari kunjungan yang masih berlangsung BUKAN angka yang sama
   dengan rata-rata hari lengkap. Tampilkan badge `periode berjalan` dan,
   bila mungkin, bandingkan dengan hari lengkap terakhir — jangan dengan
   rata-rata seluruh periode.
2. **Record in-progress dikeluarkan dari rata-rata durasi** (atau
   ditampilkan terpisah sebagai `n record masih berjalan`). Contoh cacat
   nyata: rata-rata durasi toko "hari ini" 27,0 m vs rata-rata keseluruhan
   88,8 m — sebagian besar selisihnya adalah 23 kunjungan berstatus
   "Sedang di Toko" yang durasinya belum final.
3. **Anomali operasional ditandai, bukan disembunyikan:** `Lupa Check-Out`,
   jam kerja > 10 jam/hari, travel 288 menit untuk 13 calls — tampilkan
   sebagai flag kualitas data di samping angka, bukan dihapus dari data.

---

## F-13 — Pola SQL analitik (ringkas; detail di sql-intelligence.md)

```sql
-- Growth MoM yang benar: LAG atas date spine, bukan self-join mentah
WITH spine AS (                       -- semua periode tampil, yang kosong = 0
  SELECT d AS bulan FROM calendar WHERE d BETWEEN :start AND :end
), agg AS (
  SELECT DATE_TRUNC('month', tgl) AS bulan, SUM(revenue) AS rev
  FROM orders WHERE status IN ('Completed','Shipped') GROUP BY 1
), joined AS (
  SELECT s.bulan, COALESCE(a.rev, 0) AS rev FROM spine s LEFT JOIN agg a USING (bulan)
)
SELECT bulan, rev,
  LAG(rev) OVER (ORDER BY bulan) AS rev_prev,
  CASE WHEN LAG(rev) OVER (ORDER BY bulan) = 0 THEN NULL        -- §F-02: basis 0 = NULL
       ELSE (rev - LAG(rev) OVER (ORDER BY bulan))
            / ABS(LAG(rev) OVER (ORDER BY bulan)) END AS growth
FROM joined ORDER BY bulan;

-- Agregasi SEBELUM join (hindari fan-out): hitung di CTE, baru join.
-- COUNT DISTINCT setelah join 1:N = salah. Dedup dulu (ROW_NUMBER() ... rn = 1).
```

---

## F-14 — Checklist verifikasi per angka (dijalankan SEBELUM tayang)

```
[ ] Rumus tertulis di samping angka (§F-00.1)?
[ ] Hitung ulang dari grain mentah — cocok? (§F-03)
[ ] Total = Σ segmen (COUNT) / overlap dijelaskan (COUNTD)? (§F-04, §F-11)
[ ] Growth: basis ≠ 0? satuan pp vs % benar? (§F-02)
[ ] Mean ditemani median (+P90 bila n ≥ 20)? (§F-01)
[ ] Dekomposisi residu = 0? (§F-05)
[ ] Outlier ditandai, bukan dihapus diam-diam? (§F-06)
[ ] Korelasi: n + scatter + tanpa kata kausal? (§F-07)
[ ] Forecast: PI t-based + backtest MAE/sMAPE + clip 0 + label dinamis? (§F-08)
[ ] Periode berjalan ditandai; record in-progress ditangani? (§F-12)
[ ] Label/judul cocok dengan seri yang benar-benar tampil? (§F-11)
```

---

## Peta ke file lain

| Butuh | Baca |
|---|---|
| Definisi metrik (numerator/denominator/grain) | `foundation/metric-definition-engine.md` |
| Distribusi & uji statistik mendalam | `analytical/statistical-engine.md` |
| Diagnosis "kenapa" (driver, counterfactual) | `analytical/diagnostic-reasoning.md` |
| Forecast musiman / break struktural | `analytical/forecasting.md`, `forecasting-intelligence.md` |
| Kohort & funnel SQL | `analytical/segmentation-cohort-funnel.md`, `sql-intelligence.md` |
| Cek kualitas sebelum tayang | `quality/qa-and-critique-engine.md` (Q-CALC, Q-STAT) |
| Bukti angka yang menjumlah | `proof/real-examples.md` |
