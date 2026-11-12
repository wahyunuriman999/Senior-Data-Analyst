# Forecasting Engine
**Phase B — Analytical Brain | Engine B6**
**Depth Contract: FULL — rumus OLS + interval prediksi + backtest ada di `formula-library.md` F-08. File ini mengatur MODEL dan KEPUTUSANNYA.**

---

## 1. DEKOMPOSISI DULU, MODEL KEMUDIAN

Setiap deret waktu diurai sebelum difit — jangan lempar angka mentah ke regresi:

```
y(t) = Tren(t) × Musiman(t) × Residu(t)     # atau aditif bila amplitudo musiman stabil
```

| Komponen | Yang dicari | Bila ditemukan |
|---|---|---|
| Tren | arah jangka panjang | laporkan slope + satuan per periode |
| Musiman | pola berulang (bulanan/tahunan) | model WAJIB menanganinya (bukan regresi linier mentah) |
| Break struktural | level/slope berubah mendadak (promo, krisis, perubahan harga) | fit hanya data pasca-break, ATAU dummy intervensi — dan ANOTASI di grafik |
| Residu | noise + outlier | cek: residual tidak berpola; outlier dianotasi, bukan dihapus (§F-06) |

**Aturan:** regresi linier atas data yang punya musiman kuat (mis. Desember
selalu melonjak) hanya boleh tampil sebagai `baseline naif` dengan label
keterbatasannya — bukan sebagai "forecast".

## 2. TANGGA MODEL (NAIK HANYA BILA BASELINE GAGAL)

```
1. Naif: ŷ(t+1) = y(t)                        # baseline paling jujur
2. Seasonal-naif: ŷ(t+1) = y(t+1−musim)       # bila musiman jelas
3. Rata-rata bergerak / ETS sederhana         # tren + musiman ringan
4. Regresi linier + dummy musiman             # tren + musiman eksplisit
5. Holt-Winters / ARIMA                       # bila 3–4 gagal di backtest
```

**Jangan lompat ke 5 sebelum 1–2 diukur.** Bila model canggih tidak
mengalahkan seasonal-naif di backtest, tampilkan seasonal-naif — dan katakan.

## 3. BACKTEST: SATU-SATUNYA BUKTI FORECAST PUNYA NILAI

```
Protokol (wajib):
  1. Potong temporal: latih [awal … T−3], uji [T−2 … T] — JANGAN acak (leakage).
  2. Laporkan MAE dan sMAPE di periode uji (rumus di F-08).
  3. Bandingkan dengan baseline naif & seasonal-naif.
  4. Bila sMAPE > 20% → forecast ditandai "⚠ tidak andal".
  5. Bila mungkin: expanding-window (latih makin panjang, uji bergeser) —
     satu backtest bisa beruntung; tiga lebih jujur.
```

**Metrik error — kapan pakai apa (dari forecasting-intelligence.md):**

| Metrik | Pakai bila | Jangan bila |
|---|---|---|
| MAE | default — satuannya sama dengan data, mudah dijelaskan | — |
| RMSE | error besar harus dihukum lebih berat | outlier akan mendominasi |
| sMAPE | bandingkan deret beda skala | — |
| MAPE | — | ada aktual = 0 (meledak ke ∞) |

## 4. HORIZON & INTERVAL

- Horizon default engine: **3 periode**. Lebih jauh = interval lebih lebar
  (leverage di F-08 membuatnya otomatis) + backtest lebih buruk — tulis keduanya.
- **Tidak ada point forecast tanpa PI 80% & 95%.** Tidak ada pengecualian.
- Metrik tak-negatif (revenue, calls, units): `lo = max(0, lo)` (§F-08.3).
- Tampilkan di samping forecast: `n latih`, `σ residual`, `sMAPE backtest`.
  Tanpa ketiganya, pembaca tidak bisa menilai forecast itu.

## 5. PERIODE BELUM LENGKAP & DATA HILANG

- Bulan berjalan (mis. Nov, 9 hari) **bukan** titik penuh: jangan masukkan
  ke training set tanpa normalisasi per-hari, dan jangan bandingkan
  totalnya dengan bulan penuh (§F-02, §F-12).
- Periode hilang: buat date spine (semua periode tampil; yang kosong = 0
  atau NA dengan alasan tertulis) — jangan biarkan model mengira jarak
  antar titik itu seragam padahal ada yang lompat.
- Data direvisi retroaktif: catat tanggal snapshot; bandingkan histori
  hanya dalam snapshot yang sama.

## 6. YANG DILARANG

- Forecast dari < 6 titik tanpa label `⚠ data latih sangat pendek`.
- Interval yang tidak melebar dengan horizon.
- Menyajikan baseline naif sebagai model musiman.
- Klaim "akurat" tanpa angka backtest.
- Forecast negatif untuk metrik tak-negatif.

---

## KAITAN

- Rumus: `formula-library.md` F-08 (OLS, t-interval, backtest, clip).
- Evaluasi metrik & leakage: `analytical/forecasting-intelligence.md`.
- Implementasi: `tools/apex/dashboard.tpl.js` `forecast()` + `tools/apex/analytics.py`.
