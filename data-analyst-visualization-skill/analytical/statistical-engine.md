# Advanced Statistical Engine
**Phase B — Analytical Brain | Engine B5**
**Depth Contract: FULL — semua rumus hitung ada di `formula-library.md` (F-01, F-06, F-07). File ini mengatur KAPAN dan BAGAIMANA rumus itu dipakai.**

---

## 1. DESKRIPTIF: KENALI DISTRIBUSI SEBELUM SATU ANGKA PUN DILAPORKAN

Jangan pernah melaporkan mean tanpa menjawab dulu: bentuk distribusinya apa?

| Bentuk | Ciri | Yang dilaporkan |
|---|---|---|
| Normal / simetris | mean ≈ median, skew ∈ [−0,5, 0,5] | mean ± SD |
| Right-skewed (revenue, durasi, kunjungan) | mean > median, ekor kanan panjang | **median + IQR + P90** (mean pelengkap) |
| Bimodal | dua puncak (mis. dua segmen tercampur) | **PISAHKAN segmennya** — satu mean untuk dua puncak adalah fiksi |
| Heavy zero (banyak 0) | median bisa 0 | laporkan % nol + median dari yang > 0, terpisah |

```
skew (Pearson) ≈ 3 · (mean − median) / SD     # |skew| > 1 = sangat skewed
```

**Aturan:** bila mean dan median berbeda > 10%, distribusi dinyatakan skewed
dan headline memakai median. Contoh nyata: durasi visit mean 88,8 m vs
median 84,3 m — selisih 5% masih wajar, tapi ekor SPG (±500 m) wajib disebut.

## 2. KETIDAKPASTIAN: SELALU DENGAN INTERVAL

```
# CI 95% untuk mean (n ≥ 30 → z; n < 30 → t, df = n−1):
mean ± t* · s / √n

# CI 95% untuk proporsi (pakai Wilson, BUKAN Wald — Wald ambruk di p dekat 0/1):
Wilson: (p̂ + z²/2n ± z·√(p̂(1−p̂)/n + z²/4n²)) / (1 + z²/n),  z = 1,96
```

**Aturan:** estimasi tanpa interval = estimasi yang belum selesai.
n < 30 → laporkan intervalnya yang LEBAR itu apa adanya; jangan sembunyikan
dengan membulatkan.

## 3. UJI HIPOTESIS: ASUMSI DULU, p-VALUE KEMUDIAN

```
Langkah:  (1) tulis H0/H1 SEBELUM melihat data  (2) cek asumsi  (3) pilih uji
          (4) laporkan effect size + CI  (5) baru p-value
```

| Pertanyaan | Uji default | Bila asumsi gagal |
|---|---|---|
| Dua mean berbeda? | t-test (Welch bila varians beda) | Mann-Whitney U |
| > 2 mean berbeda? | ANOVA | Kruskal-Wallis |
| Dua proporsi berbeda? | chi-square / z 2-proporsi | Fisher exact (n kecil) |
| Hubungan dua numerik? | Pearson r | Spearman ρ (monotonik, non-linier) |
| Sebelum vs sesudah (berpasangan)? | paired t-test | Wilcoxon signed-rank |

**Asumsi yang dicek (dan ditulis):** normalitas (n kecil), homogenitas
varians, independensi observasi. Uji tanpa cek asumsi = angka tanpa fondasi.

**Effect size (WAJIB menyertai p-value — Q-STAT-002):**

```
Cohen's d = (mean₁ − mean₂) / SD_pooled
  |d| ≈ 0,2 kecil · 0,5 sedang · 0,8 besar
```

p < 0,05 dengan d = 0,05 pada n = 100.000 artinya "beda yang nyata tapi
tidak penting". Tulis keduanya.

## 4. MULTIPLE TESTING: SEMAKIN BANYAK YANG DIUJI, SEMAKIN KETAT AMBANGNYA

Menguji 20 segmen dengan α = 0,05 → harapan ~1 false positive. Aturan:

```
Bonferroni:  α_adj = 0,05 / k        # k = jumlah uji; ketat, untuk klaim konfirmatori
Benjamini–Hochberg (FDR): urutkan p, tolak p(i) ≤ (i/k) · 0,05
```

Bila dashboard menampilkan "segmen X signifikan" dari 20 segmen tanpa
koreksi → klaim ditandai `⚠ belum dikoreksi multiple-testing`.

## 5. REGRESI: DIAGNOSTIK, BUKAN SEKADAR R²

- **R² vs adjusted R²:** laporkan adjusted R² bila > 1 prediktor.
  R² naik sendiri tiap tambah variabel — adjusted R² menghukumnya.
- **Residual:** plot residual vs fitted — pola corong = heteroskedastisitas
  (CI jadi tidak valid); pola lengkung = hubungan non-linier.
- **Multikolinearitas:** VIF > 5 = prediktor saling menjelaskan; koefisien
  tidak bisa diinterpretasi satu-per-satu.
- **Outlier berpengaruh:** satu titik dengan leverage tinggi bisa membalik
  tanda koefisien. Cek Cook's distance; laporkan analisis dengan & tanpa titik itu.
- **Jangan ekstrapolasi:** prediksi di luar rentang x yang diamati ditandai
  `⚠ ekstrapolasi`.

## 6. UKURAN SAMPEL & KEKUATAN

- n < 30 per grup: jangan klaim perbedaan "signifikan" tanpa CI yang lebar
  itu ditulis; lebih jujur katakan "data belum cukup — butuh n ≈ …".
- Aturan praktis (bukan pengganti power analysis): untuk mendeteksi efek
  sedang (d = 0,5) dengan power 80% butuh ±64 observasi per grup.
- Segmen dengan n < 30 di dashboard: tampilkan dengan badge `n kecil`
  dan tanpa klaim perbandingan.

## 7. BAHASA YANG DILARANG & YANG DITUNTUT

| Dilarang (klaim tanpa dasar) | Gantinya |
|---|---|
| "Terbukti X menyebabkan Y" (observasional) | "X berkorelasi dengan Y (r=…, n=…); confounder mungkin: …" |
| "Signifikan" tanpa angka | "p=0,03, d=0,4 (sedang), 95% CI [0,1, 0,7]" |
| "Rata-rata naik" (tanpa median) | "Mean naik x, median naik y — kenaikan didorong ekor atas/bawah" |
| "Tidak ada perbedaan" (p > 0,05) | "Tidak terdeteksi perbedaan pada n ini (CI mencakup 0)" |

---

## KAITAN

- Rumus hitung: `formula-library.md` F-01 (distribusi), F-06 (outlier), F-07 (korelasi).
- Kualitas: `quality/qa-and-critique-engine.md` Q-STAT-001 s.d. Q-STAT-006.
- Uji sebelum tayang: `proof/runners/test_engine_math.py`.
