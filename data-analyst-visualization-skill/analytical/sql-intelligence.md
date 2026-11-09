# SQL INTELLIGENCE ENGINE
**Phase B — Analytical Brain Extension**

## PURPOSE
Analytical SQL is about reasoning, not syntax. The AI must manage grain, join paths, and denominator integrity.

## SQL REASONING PATTERNS
### 1. Common Table Expressions (CTEs)
- **Why**: Modularity, avoiding nested subquery hell, controlling execution context.
- **Rule**: Use CTEs to isolate aggregations *before* joining to fact tables to prevent Cartesian fan-out.

### 2. Date Spine / Calendar Tables
- **Why**: Handling missing periods in time series.
- **Rule**: If querying daily active users, do NOT just group by `event_date`. Left join a Date Spine to the grouped data to ensure days with 0 events show as `0`, not missing rows.

### 3. Window Functions
- **LAG / LEAD**: Mandatory for WoW, MoM, YoY calculations.
  - *Failure Mode*: Sorting incorrectly in the `OVER` clause.
- **ROW_NUMBER()**: Mandatory for deduplication.
  - *Grain Rule*: Partition by unique entity ID, order by timestamp desc, filter `WHERE rn = 1`.

### 4. Cohort & Retention SQL
- **Pattern**: `user_id`, `cohort_month` (min date), `activity_month`.
- **Validation**: The denominator (users in cohort) must remain constant across the row, derived from the `cohort_month` total, not the `activity_month` subset.

### 5. Funnel SQL
- **Pattern**: Self-joins or conditional aggregation (`COUNT(CASE WHEN step=1 THEN id END)`).
- **Rule**: Differentiate strict funnels (must have timestamp of step 2 > step 1) vs loose funnels (any occurrence).

### 6. Growth MoM/YoY yang benar (LAG + basis 0 = NULL)
```sql
WITH spine AS (
  SELECT d AS bulan FROM calendar WHERE d BETWEEN :start AND :end
), agg AS (
  SELECT DATE_TRUNC('month', tgl) AS bulan, SUM(revenue) AS rev
  FROM orders WHERE status IN ('Completed','Shipped') GROUP BY 1
), joined AS (
  SELECT s.bulan, COALESCE(a.rev, 0) AS rev
  FROM spine s LEFT JOIN agg a USING (bulan)
)
SELECT bulan, rev,
  LAG(rev) OVER (ORDER BY bulan) AS rev_prev,
  CASE WHEN LAG(rev) OVER (ORDER BY bulan) = 0 THEN NULL
       ELSE (rev - LAG(rev) OVER (ORDER BY bulan))
            / ABS(LAG(rev) OVER (ORDER BY bulan)) END AS growth
FROM joined ORDER BY bulan;
```
- **Kenapa date spine:** tanpa spine, bulan kosong hilang — LAG lalu
  membandingkan bulan yang salah (mis. Mar vs Jan, dikira MoM).
- **Kenapa `= 0 → NULL`:** growth dari basis 0 tidak terdefinisi (§F-02).
  Menampilkan 0% adalah klaim "tidak berubah" yang salah.
- **Kenapa `ABS()`:** basis negatif membalik arah growth; flag bila terjadi.

### 7. Larangan agregasi setelah join (fan-out & distinct)
- **Jangan** `COUNT(DISTINCT id)` SETELAH join 1:N — duplikasi baris
  tidak mengubah COUNT DISTINCT, tapi `SUM()` dan `COUNT()` MELEDAK.
  Agregasi dulu di CTE, baru join (§1).
- **Jangan** `AVG(rasio)` / `AVG(margin per baris)` — hitung ulang rasio
  dari Σ komponen (§F-03). Contoh: `AVG(revenue/units)` per baris bisa
  meleset 5,5x dari `Σrevenue/Σunits` yang benar.
- **Jangan** `SUM(DISTINCT …)` sebagai jalan pintas — itu menyembunyikan
  fan-out, bukan memperbaikinya. Perbaiki grain-nya (join-audit.md).
