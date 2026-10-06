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
