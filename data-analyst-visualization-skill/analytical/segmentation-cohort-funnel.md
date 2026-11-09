# Segmentation, Cohort & Funnel Analysis
**Phase B — Analytical Brain | Engine B8**
**Depth Contract: FULL — rumus kohort & funnel ada di `formula-library.md` F-09, F-10.**

---

## 1. SEGMENTASI: SEGEMEN YANG TIDAK BISA DIUJI = SEGEMEN YANG TIDAK ADA

**Syarat segmen yang sah:**

| Syarat | Aturan |
|---|---|
| Ukuran minimum | n ≥ 30 per segmen untuk perbandingan; n < 30 → badge `n kecil`, tanpa klaim |
| Definisi stabil | definisi segmen sama di semua periode (bila definisi berubah, pisahkan periodenya) |
| Saling lepas (untuk share) | satu entitas = satu segmen dalam satu analisis; bila entitas bisa di >1 segmen, share TIDAK dijumlahkan tanpa catatan overlap (§F-04) |
| Perbedaan teruji | beda antar segmen dilaporkan dengan CI / uji (§statistical-engine) — bukan selisih mata |

**Segmentasi yang berguna vs yang palsu:**

- Berguna: segmen yang mengubah KEPUTUSAN (region dengan biaya travel
  beda 10x, role dengan pola kerja beda — MD mobile vs SPG menetap).
- Palsu: segmen yang hanya memecah angka tanpa mengubah keputusan apa pun,
  atau segmen hasil p-hacking (dari 20 potongan, satu "signifikan").
- **Cek Simpson tiap segmentasi** (§F-07): agregat vs per-segmen harus
  ditampilkan berdampingan.

**Contoh kerja (dashboard referensi):** MD MOBILE 6,7 calls/hari vs SPG
MOBILE ±1,0 call/hari dengan avg visit ±500 menit — BUKAN "SPG malas".
SPG menetap di satu toko (model kerja beda). Membandingkan keduanya dengan
satu tolok ukur calls/hari adalah kesalahan segmentasi: tolok ukurnya
harus dibedakan per model kerja, atau perbandingan itu diberi konteks.

## 2. KOHORT: DENOMINATOR TETAP, UMUR DISEJAJARKAN

```
retensi(kohort c, umur t) = aktif(c, t) / ukuran_kohort(c)     # F-09
```

- **Matriks segitiga:** baris = kohort (bulan akuisisi), kolom = umur
  (B0, B1, B2, …). Sel di kanan atas yang melewati tanggal data = `NA`,
  bukan 0.
- **Bandingkan pada umur yang sama:** retensi B3 kohort Q1 vs B3 kohort Q2.
  Jangan bandingkan B3 vs B6.
- **Ukuran kohort dicantumkan** di tiap baris (n=…): retensi 50% dari n=8
  tidak sama bobotnya dengan 50% dari n=8.000.
- **Break dianotasi, bukan diklaim kausal:** "B3 turun 8 pp bersamaan
  dengan perubahan harga Maret" — kata "bersamaan", bukan "akibat".
- **Survivorship bias:** kohort lama yang masih teramati adalah yang
  bertahan — jangan bandingkan retensi kohort lama vs baru tanpa menyebut ini.

Contoh kerja: proof/real-examples.md Ex.2.

## 3. FUNNEL: STRICT VS LOOSE, DAN DIAGNOSIS DROP-OFF

```
konversi langkah = n(langkah k) / n(langkah k−1)   # F-10
```

- **Strict:** langkah k dihitung hanya bila timestamp k > timestamp k−1
  untuk user yang sama. **Loose:** cukup pernah terjadi. **Tulis jenisnya.**
- Laporkan DUA angka drop-off: penurunan absolut terbesar DAN penurunan
  relatif terbesar — keduanya, karena bisa menunjuk langkah yang berbeda.
- **Denominator funnel ≠ denominator populasi umum.** Funnel dari 1.000
  pengunjung yang 100 sampai checkout: konversi checkout = 100/1.000,
  BUKAN 100/jumlah user terdaftar.
- **Waktu antar langkah:** bila median waktu langkah 1→2 adalah 3 hari,
  funnel "hari ini" akan selalu terlihat bocor — ukur funnel pada kohort
  yang sudah cukup umur, bukan pada data hari ini.

## 4. PERILAKU vs DEMOGRAFI

- Segmentasi perilaku (frekuensi, recency, durasi, pola) hampir selalu
  lebih menjelaskan daripada demografi (region, role) — tapi keduanya
  harus diuji, bukan diasumsikan.
- **RFM ringkas** (bila relevan): Recency–Frequency–Monetary, masing-masing
  di-kuartil-kan; laporkan definisi kuartilnya (kuartil dari populasi apa,
  periode apa).
- Jangan membuat segmen dari variabel yang JUGA dipakai sebagai outcome
  (mis. segmen "pelanggan bernilai tinggi" dari revenue, lalu "menemukan"
  bahwa segmen itu revenue-nya tinggi — itu tautologi).

## 5. FORMAT KELUARAN

```
SEGMENTASI: <definisi tiap segmen + n tiap segmen>
PERBANDINGAN: <metrik per segmen + CI/uji + badge n kecil bila ada>
CEK SIMPSON: <agregat vs segmen — searah / berlawanan + penjelasan mix>
KOHORT/FUNNEL: <matriks segitiga atau langkah + penyebut tiap langkah + jenis strict/loose>
```

---

## KAITAN

- Rumus: `formula-library.md` F-04 (overlap), F-09 (kohort), F-10 (funnel).
- SQL: `analytical/sql-intelligence.md` §4–5.
- Statistik: `analytical/statistical-engine.md` §3–6.
- Bukti: `proof/real-examples.md` Ex.2 & Ex.3.
