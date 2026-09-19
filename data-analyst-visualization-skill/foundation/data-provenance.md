# DATA PROVENANCE ENGINE
**Phase A — Foundation Brain | Engine A4**
**Depth Contract: FULL**

---

## PURPOSE
Record the complete audit trail of every analytical result — from raw source data to final metric or visualization. Provenance ensures that any number in an analysis can be traced back to its origin, every transformation is documented, and the analysis is reproducible. Without provenance, a dashboard number is a claim, not a fact.

The engine answers: **"Where did this 18.4% come from?"**

## SCOPE
- All metrics displayed in dashboards or reports.
- All intermediate transformations (joins, aggregations, filters, derived columns).
- All cleaning decisions made during data preparation.
- All analytical assumptions that affected the result.

---

## INPUTS
```
INPUT
├── analysis_id              : Unique identifier for this analytical run
├── business_question        : The question being answered
├── metric_contracts         : Output from Metric Definition Engine (A1)
├── grain_contracts          : Output from Data Grain Engine (A2)
├── join_audit_reports       : Output from Join Audit Engine (A3)
├── assumption_registry      : Output from Assumption Registry Engine (A5)
├── transformation_log       : All transformations applied (in order)
└── output_values            : Final metric values produced
```

## OUTPUT CONTRACT
```
OUTPUT — PROVENANCE RECORD
├── analysis_id              : Unique run ID
├── timestamp                : When this analysis was executed
├── business_question        : What question this answers
├── source_tables            : All raw data sources used, with row counts
├── transformation_chain     : Ordered list of all transformations applied
├── filter_chain             : All filter conditions applied, with row counts before and after
├── metric_contracts_used    : Reference to A1 contracts
├── grain_contracts_used     : Reference to A2 contracts
├── join_audit_results       : Reference to A3 reports
├── assumption_references    : Reference to A5 entries
├── final_values             : The metric values produced with their context
├── reproducibility_check    : Can this analysis be re-run to produce the same values?
└── version                  : Dataset version/snapshot date used
```

---

## THE LINEAGE CHAIN

Every analytical result must be traceable through this chain:
```
SOURCE
  │
  ├─ Table name, version/date, row count
  │
  ▼
TRANSFORMATION 1
  │
  ├─ Operation: [filter | join | aggregate | derive | clean | reshape]
  ├─ Parameters: [filter conditions, join keys, aggregation function]
  ├─ Row count before: N_before
  ├─ Row count after: N_after
  ├─ Measure sum before (if applicable): S_before
  └─ Measure sum after: S_after
  │
  ▼
TRANSFORMATION 2
  │ (same structure)
  ▼
...
  │
  ▼
FINAL METRIC VALUE
  │
  ├─ Value: [18.4%]
  ├─ Context: [Conversion Rate, October 2024, North America, Non-bot sessions]
  ├─ Metric Contract: [A1: Monthly Conversion Rate, v1.2]
  └─ Assumptions Applied: [A5: ASM-003, ASM-007]
```

---

## PROCEDURE

### STEP 1 — Register Data Sources
```
For each raw data source used:
    SOURCE_REGISTRY:
        name         : "orders" table
        location     : "data_warehouse.sales.orders"
        snapshot_date: "2024-10-01 00:00 UTC"
        row_count    : 250,000
        schema_hash  : [MD5 or checksum of schema if available]
        notes        : "Data as of end of October 2024 nightly batch"
```

### STEP 2 — Log Every Transformation
For each transformation applied to the data, log:
```
TRANSFORMATION LOG ENTRY:
    step_id      : T_001
    operation    : FILTER
    description  : "Remove internal test accounts"
    condition    : "WHERE account_type != 'internal'"
    rows_before  : 250,000
    rows_after   : 247,832
    rows_dropped : 2,168
    reason       : "Internal accounts distort conversion and revenue metrics"
    reference    : "Assumption A5: ASM-001"
    timestamp    : [execution time]
```

```
TRANSFORMATION LOG ENTRY:
    step_id      : T_002
    operation    : JOIN
    description  : "Join orders to dim_products for category enrichment"
    join_type    : "LEFT JOIN"
    join_key     : "product_id"
    rows_before  : 247,832
    rows_after   : 247,832
    fan_out      : 1.0 (PASS)
    measure_sum_before : $12,450,000
    measure_sum_after  : $12,450,000 (Δ% = 0%)
    join_audit_ref     : "A3: JAE-2024-10-001"
```

```
TRANSFORMATION LOG ENTRY:
    step_id      : T_003
    operation    : AGGREGATE
    description  : "Sum revenue by region and month"
    group_by     : ["region", "month"]
    measure      : "SUM(gross_revenue_usd)"
    rows_before  : 247,832
    rows_after   : 40 (10 regions × 4 months)
    total_sum_before : $12,450,000
    total_sum_after  : $12,450,000 (reconciliation: PASS)
```

### STEP 3 — Reconcile Critical Measures
After every aggregation, verify that the total of the measure is preserved:
```
RECONCILIATION CHECK:
    PRE-AGGREGATION SUM:  $12,450,000
    POST-AGGREGATION SUM: $12,450,000
    DIFFERENCE:           $0
    VERDICT: PASS

IF DIFFERENCE > $0:
    → Investigate: filter removed rows after measure was captured?
    → Check: NULL handling difference before and after transformation
    → Check: Join fan-out introduced after earlier safe point
```

### STEP 4 — Register Final Values
```
FINAL VALUE RECORD:
    metric_name     : "Monthly Conversion Rate"
    value           : 4.7%
    context         : "North America, October 2024, Calendar month"
    metric_contract : "A1: MDE-Monthly-Conversion-Rate-v1.2"
    grain           : "User × Month"
    filters_applied : ["region = 'North America'", "month = '2024-10'",
                       "account_type != 'internal'", "channel != 'bot'"]
    assumptions     : ["A5: ASM-003 (NULL sessions treated as 0 contribution)",
                       "A5: ASM-007 (Bot traffic defined as channel = 'bot')"]
    join_audits     : ["A3: JAE-2024-10-001"]
    reproducible    : YES
    run_id          : "ANALYSIS-2024-10-15-001"
```

### STEP 5 — Verify Reproducibility
A provenance record is only complete if the analysis can be reproduced.
```
REPRODUCIBILITY CHECK:
    □ Are all source datasets versioned or snapshotted?
    □ Are all transformation steps deterministic (no random sampling without seed)?
    □ Are all filter conditions fully specified (no "current date" without pinning)?
    □ Are all metric contracts versioned?
    □ Can a second execution produce the same final values?

IF ANY BOX IS UNCHECKED:
    → Document the non-reproducible element explicitly.
    → Flag the analysis as "As-Of Snapshot" — cannot be exactly reproduced.
```

---

## DECISION TREE
```
Metric/visualization to be produced
           │
           ▼
Step 1: Register all source datasets
           │
           ▼
For each transformation:
Step 2: Log operation, row counts, measure sums
           │
           ▼
After each aggregation:
Step 3: Reconcile measure totals
           │
      Δ = 0? ── NO ──► Investigate and fix before continuing
           │
          YES
           ▼
Step 4: Register final values with full context
           │
           ▼
Step 5: Verify reproducibility
           │
     Reproducible? ── NO ──► Flag as "As-Of Snapshot" and document why
           │
          YES
           ▼
     File provenance record → proceed to visualization
```

---

## MATHEMATICAL DEFINITIONS

**Measure Preservation Invariant:**
```
For any transformation T applied to dataset D:
    Σ(measure, D) = Σ(measure, T(D))

EXCEPTIONS (document explicitly):
    Filtering: Σ drops by exactly the sum of removed rows (verifiable)
    Aggregation: Σ must be preserved
    Join with fan-out: Σ will be inflated by φ (must be corrected)
```

**Provenance Completeness:**
```
A provenance record P is complete iff:
    ∀ m ∈ final_metrics : ∃ chain(source, T₁, T₂, ..., Tₙ) → m
    and each Tᵢ is fully specified with:
        {operation, parameters, row_count_before, row_count_after, measure_sum_before, measure_sum_after}
```

---

## PRECONDITIONS
- [ ] Metric contracts (A1) are completed for all metrics.
- [ ] Grain contracts (A2) are completed for all source tables.
- [ ] Join Audit reports (A3) are available for all joins.
- [ ] A unique analysis ID is assigned before execution begins.

## ASSUMPTIONS
- Source data is versioned or snapshotted — if not, the analysis is flagged as time-dependent.
- All transformations are applied in the logged order — order matters.
- Reconciliation tolerances: Δ% < 0.001% is acceptable for floating-point precision; Δ% > 0.01% requires investigation.

---

## EDGE CASES

| Case | Problem | Resolution |
|------|---------|------------|
| Live database (no snapshot) | Analysis not reproducible | Flag as "live query"; document execution timestamp |
| Random sampling without seed | Non-deterministic results | Always set a random seed; log the seed value |
| Data corrected retroactively | Historical analysis invalid | Use point-in-time snapshots; document correction |
| Multiple source systems | Conflicting values for same entity | Document which system is authoritative and why |
| Measure in different currencies | Aggregation mixes currencies | Normalize to one currency before aggregating; log conversion rate and date |
| Partial data load | Analysis covers only part of the period | Document data completeness explicitly |
| Derived column from another derived column | Deep transformation chains | Log every layer; validate at each step |

---

## FAILURE MODES

| Failure | Symptom | Detection | Severity |
|---------|---------|-----------|----------|
| No transformation log | Cannot explain how metric was derived | Missing log entries | CRITICAL |
| Measure sum not reconciled | Fan-out or filter error undetected | Δ% ≠ 0% | CRITICAL |
| Source not versioned | Analysis cannot be reproduced | Reproducibility check fails | HIGH |
| Assumption not documented | Cleaning decision invisible | Missing A5 reference | HIGH |
| Filter applied after aggregation | Wrong rows excluded | Row counts inconsistent | HIGH |
| Metric contract version mismatch | Metric definition changed mid-analysis | Contract version not logged | MEDIUM |

---

## WORKED EXAMPLE

**Analysis:** "What is the YoY revenue growth rate for North America, 2024 vs 2023?"

```
PROVENANCE RECORD: ANALYSIS-2024-10-15-002
═══════════════════════════════════════════
BUSINESS QUESTION: YoY revenue growth, North America, FY2024 vs FY2023

SOURCES:
  S1: data_warehouse.sales.orders | snapshot: 2024-10-01 | rows: 2,400,000
  S2: data_warehouse.dim.dim_accounts | snapshot: 2024-10-01 | rows: 15,000

TRANSFORMATIONS:
  T_001: FILTER orders | account_type != 'internal' AND order_status IN ('Completed','Shipped')
         Before: 2,400,000 | After: 2,318,744 | Dropped: 81,256 (test+cancelled orders)
         Ref: A5-ASM-001, A5-ASM-002

  T_002: JOIN orders (left) to dim_accounts (right) on account_id | LEFT JOIN
         Before: 2,318,744 | After: 2,318,744 | φ = 1.0 (PASS)
         Revenue PRE: $48,220,000 | Revenue POST: $48,220,000 | Δ% = 0% (PASS)
         Ref: A3-JAE-2024-10-002

  T_003: FILTER by region = 'North America'
         Before: 2,318,744 | After: 847,322

  T_004: AGGREGATE SUM(gross_revenue_usd) GROUP BY fiscal_year
         Before: 847,322 | After: 2 rows (2023, 2024)
         2023 Revenue: $18,450,000 | 2024 Revenue: $21,771,000
         Reconciliation: SUM = $40,221,000 | Pre-filter sum NA portion = $40,221,000 ✓

FINAL VALUES:
  2023 Revenue (NA, Fiscal): $18,450,000
  2024 Revenue (NA, Fiscal): $21,771,000
  YoY Growth = ($21,771,000 - $18,450,000) / $18,450,000 = +18.0%

METRIC CONTRACT: A1-MDE-Revenue-v1.1, A1-MDE-YoY-Growth-v1.0
ASSUMPTIONS: A5-ASM-001, A5-ASM-002
REPRODUCIBLE: YES (snapshot-based; re-run will produce identical result)
═══════════════════════════════════════════
```

---

## ADVERSARIAL EXAMPLE

**Challenge:** "You said revenue grew 18%, but our CFO's report says 15%. Who is right?"

**Engine Response (using provenance):**
```
INVESTIGATION USING PROVENANCE:

Our result: $18,450,000 → $21,771,000 = +18.0%
CFO report: unknown numerator/denominator

CHECKING:
    1. Metric Contract mismatch?
       → Our contract: gross_revenue_usd (includes shipping)
       → CFO contract: net_revenue (excludes shipping revenue)
       → Shipping revenue = $1,400,000
       → Our revenue adjusted: $21,771,000 - $1,400,000 = $20,371,000 prior year adjusted
       → With consistent net_revenue: +15.1% → MATCHES CFO REPORT

CONCLUSION:
    Both are correct; they measure different things.
    Our metric includes shipping revenue; CFO uses net revenue.
    Recommendation: Align on a single canonical revenue metric contract.
```

---


## COUNTEREXAMPLES

**Counterexample A � Reconstruction vs. Real Logging:**
`
WRONG: Logging the transformation steps AFTER execution from memory.
? Memory is imperfect; row counts and filters may be misremembered.
CORRECT: Log each transformation AS it is executed with actual row counts.
`

**Counterexample B � Claiming Reproducibility on a Live Database:**
`
WRONG: "This analysis is reproducible" for a query run against a live production table.
? Data changes daily; re-running tomorrow will produce different results.
CORRECT: Flag as "As-Of Snapshot" and record the exact execution timestamp.
         Reproducibility requires either a snapshot or a versioned extract.
`
## VALIDATION RULES
1. Every analytical result must have a provenance record before it is published.
2. Measure sums must be reconciled at every transformation step.
3. All assumption references must link to actual Assumption Registry entries (Engine A5).
4. Provenance records must be retained for at least as long as the dashboards using them.

## TEST CASES

| ID | Input | Expected | Pass Condition |
|----|-------|----------|----------------|
| DPE-001 | Analysis run without logging transformations | Missing provenance flagged | Engine blocks publication |
| DPE-002 | Measure sum changes unexpectedly after join | Δ% > 0.01% detected | Engine halts, triggers Join Audit |
| DPE-003 | CFO questions a metric value | Provenance trace produced | Engine returns full lineage chain |
| DPE-004 | Live database query (no snapshot) | Flagged as non-reproducible | Analysis marked "As-Of" with timestamp |
| DPE-005 | Two versions of same metric used in same analysis | Version mismatch flagged | Engine requires resolution |
| DPE-006 | Currency mix in revenue | Mix detected | Engine requires normalization before aggregation |

---

## AGENT EXECUTION INSTRUCTIONS
1. Assign a unique analysis_id at the start of every analytical task.
2. Log every transformation as it is executed — do not reconstruct the log after the fact.
3. Reconcile measure sums after every aggregation step.
4. Reference the exact Metric Contract (A1), Grain Contract (A2), and Join Audit (A3) used.
5. When a user questions a number, retrieve the provenance record and trace the lineage.
6. Never publish a metric that does not have a complete provenance record.
