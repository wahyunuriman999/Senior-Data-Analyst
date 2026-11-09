# Diagnostic & Driver Reasoning
**Phase B — Analytical Brain | Engine B7**
**Depth Contract: FULL — menjawab "KENAPA ini terjadi?" dengan angka, bukan narasi.**

> Junior melaporkan "apa" (rata-rata, total). Apex melaporkan "kenapa" —
> dan setiap "kenapa" harus bisa dibuktikan dengan satu perhitungan yang
> ditampilkan. Klaim driver tanpa kontribusi terhitung = opini, bukan analisis.

---

## 1. URUTAN DIAGNOSIS (JANGAN LOMPAT)

```
1. APA yang berubah?        → Δ metrik + arah + besarnya (F-02, satuan benar)
2. DI MANA perubahannya?    → dekomposisi per segmen (F-05) + cek Simpson (F-07)
3. DRIVER APA yang terbesar?→ kontribusi tiap segmen/driver (bawah)
4. APAKAH ini nyata?        → cek data: outlier? break? periode berjalan? (F-06, F-12)
5. APA counterfactual-nya?  → "bagaimana bila driver X datar?" (bawah)
6. APA yang bisa dilakukan? → rekomendasi TERIKAT pada driver yang terbukti,
                              dengan besaran efek yang dihitung — bukan saran generik
```

Melewatkan langkah 2–4 dan langsung ke 6 adalah sumber utama "analisa
dangkal": rekomendasi yang bunyinya benar untuk masalah apa pun.

## 2. KONTRIBUSI SEGMEN (DRIVER ANALYSIS)

```
kontribusi_k = ΔM_k / ΔM_total × 100%       # ΔM_k = perubahan metrik di segmen k
```

- Kontribusi bisa > 100% atau negatif — itu INFORMASI, bukan error:
  segmen A +150% dan segmen B −50% artinya A menutupi kemunduran B.
  Tampilkan keduanya; jangan sembunyikan yang negatif.
- Urutkan driver dari |kontribusi| terbesar. Driver #1 WAJIB disebut di
  headline; driver di luar top-3 tidak boleh jadi headline.
- **Bukti sebelum klaim:** "Volume naik" harus disertai `ΔQ = …, efek
  volume = Rp … (F-05)` — bukan kalimat "volume tampaknya naik".

## 3. DEKOMPOSISI SEBAGAI ALAT DIAGNOSIS PERTAMA

Untuk setiap perubahan metrik level-atas, jalankan dulu F-05
(harga/volume/mix). Tiga pola yang paling sering muncul:

| Pola | Bacaan | Jebakan |
|---|---|---|
| ΔR negatif, volume positif, harga negatif besar | Diskon/promo menggerus harga — BUKAN permintaan turun | Headline "penjualan turun" menyesatkan |
| ΔR positif, volume datar, mix positif | Pergeseran ke produk mahal — BUKAN pasar membesar | Klaim "pertumbuhan" tanpa menyebut mix |
| ΔR positif agregat, mayoritas segmen negatif | Simpson — mix bergeser ke segmen besar (F-07) | Headline agregat = salah |

Contoh kerja: proof/real-examples.md Ex.1 (ΔR −7,85 M padahal volume +14,11 M).

## 4. COUNTERFACTUAL (APA YANG TERJADI BILA X DATAR?)

```
M_counterfactual = M_aktual − efek(X)
" Bila harga tidak turun (efek harga = 0), revenue Okt = Rp … (bukan Rp …)"
```

- Satu counterfactual per analisis sudah cukup — yang dihitung dari efek
  dekomposisi, bukan ditebak.
- Counterfactual BUKAN prediksi dan BUKAN klaim kausal. Tulis:
  `skenario aritmetik, bukan estimasi kausal`.

## 5. PARETO & KONSENTRASI

- Bila 20% entitas menyumbang > 80% metrik, sebutkan: "Top-5 toko = x%
  dari total calls". Konsentrasi mengubah rekomendasi (jaga top-5 ≠ sebar rata).
- Selalu cek: apakah driver #1 adalah SATU entitas (satu toko/karyawan)?
  Bila ya, headline harus menyebutnya — "naik karena satu toko" ≠ "naik merata".

## 6. CONFOUNDER CHECKLIST (SEBELUM KLAIM "KARENA")

Untuk setiap klaim "X menyebabkan/mendorong Y", jawab tertulis:

```
[ ] Apakah ada variabel ketiga yang menggerakkan keduanya? (musim, promo,
    perubahan definisi, perubahan populasi, harga, channel mix)
[ ] Apakah urutan waktunya benar? (X mendahului Y — bukan sebaliknya)
[ ] Apakah efeknya bertahan per segmen? (atau hanya agregat — Simpson?)
[ ] Apakah ada break / perubahan cara ukur di tengah periode?
[ ] Apakah n cukup dan efeknya material (bukan hanya p < 0,05)?
```

Satu jawaban "tidak tahu" → klaim diturunkan jadi hipotesis:
`"hipotesis: … — perlu uji …"`. Itu bukan kelemahan; itu kejujuran analitik.

## 7. ANOMALI OPERASIONAL SEBAGAI TEMUAN (BUKAN SAMPAH)

Data lapangan mengandung sinyal operasional, bukan hanya noise:

- `Lupa Check-Out`, jam kerja > 10 jam, travel 288 menit untuk 13 calls,
  satu karyawan 13 kunjungan sebelum tengah hari — ini TEMUAN untuk
  ditampilkan sebagai flag kualitas data / temuan operasional, lengkap
  dengan n kejadiannya. Menghapusnya dari data = menghilangkan temuan.
- Pisahkan: (a) anomali data (salah input, duplikat) → perbaiki/dokumentasi;
  (b) anomali perilaku (nyata tapi ekstrem) → tampilkan & anotasi.

## 8. FORMAT KELUARAN DIAGNOSIS (WAJIB)

```
TEMUAN:  <satu kalimat, angka + arah>
BUKTI:   <dekomposisi / kontribusi / per-segmen — rumus + angka>
CEK:     <Simpson? outlier? periode berjalan? — lolos/gagal + angka>
HIPOTESIS (bila kausal): <…> — perlu uji <…>
AKSI:    <terikat driver #1, dengan besaran efek yang dihitung>
```

Tanpa BUKTI dan CEK, bagian diagnosis tidak tayang — berapa pun bagusnya
narasi yang menyertainya.

---

## KAITAN

- Rumus: `formula-library.md` F-02, F-05, F-07, F-12.
- Dekomposisi: `analytical/variance-decomposition.md`, `analytical/driver-analysis.md`.
- Perbandingan: `analytical/comparative-analysis.md`.
- Bukti: `proof/real-examples.md` Ex.1 & Ex.4.
