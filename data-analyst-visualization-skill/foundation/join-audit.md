# JOIN AUDIT ENGINE
**Phase A — Foundation Brain | Engine A3**
**Depth Contract: FULL**

---

## PURPOSE
Validate every dataset join operation before the resulting dataset is used for aggregation, analysis, or visualization. Incorrect joins are the most common source of analytically plausible but mathematically wrong dashboards. This engine enforces a pre-join audit and a post-join reconciliation for every merge operation.

## SCOPE
- All JOIN operations between two or more datasets.
- Merges in SQL (JOIN), pandas (merge), or any other tool.
- Re-applied whenever the schema or population of a joined table changes.

---

## INPUTS
```
INPUT
├── left_table               : Name, schema, row count, and grain contract
├── right_table              : Name, schema, row count, and grain contract
├── join_type                : INNER | LEFT | RIGHT | FULL OUTER | CROSS
├── join_keys                : Column(s) used to match rows
├── purpose                  : What the join is intended to accomplish
└── expected_relationship    : 1:1 | 1:N | N:1 | N:N (many-to-many)
```

## OUTPUT CONTRACT
```
OUTPUT — JOIN AUDIT REPORT
├── pre_join_left_rows       : Row count of left table before join
├── pre_join_right_rows      : Row count of right table before join
├── expected_rows            : Expected post-join row count given relationship type
├── actual_post_join_rows    : Actual row count after join
├── fan_out_factor           : actual / pre_join_left_rows
├── null_expansion           : Count of NULLs introduced in join keys
├── unmatched_left_rows      : Rows in left with no match in right (INNER vs LEFT behavior)
├── unmatched_right_rows     : Rows in right with no match in left
├── measure_reconciliation   : Pre- and post-join sum of a critical measure
├── measure_inflation_pct    : Percentage change in measure sum after join
├── verdict                  : PASS | FAIL | WARNING
└── remediation              : Action required if FAIL or WARNING
```

---

## JOIN RELATIONSHIP TAXONOMY

### 1:1 (One-to-One)
One row in left matches exactly one row in right.
```
EXAMPLE: orders joined to order_metadata by order_id.
EXPECTED: Post-join row count = Pre-join left row count
φ = 1.0 (perfect)
SAFE FOR: All aggregations
RISK: If right has duplicates on join key → silent fan-out
```

### 1:N (One-to-Many)
One row in left matches multiple rows in right.
```
EXAMPLE: customers joined to orders by customer_id.
EXPECTED: Post-join rows = number of orders (right side drives count)
φ = average orders per customer
SAFE FOR: Analysis at order grain (right grain)
DANGEROUS IF: Summing customer-level measures at result level (double counts customer attributes)
```

### N:1 (Many-to-One)
Multiple rows in left match one row in right (dimension lookup).
```
EXAMPLE: transactions joined to dim_products by product_id.
EXPECTED: Post-join rows = left row count
φ = 1.0 (dimension lookup should not inflate rows)
SAFE IF: right table has unique join key
DANGEROUS IF: dim_products has duplicate product_ids (SCD not filtered)
```

### N:N (Many-to-Many)
Multiple rows on both sides match.
```
THIS IS ALMOST ALWAYS A DESIGN ERROR.
EXPECTED: Post-join rows = left_rows × right_matching_rows_per_key
φ >> 1.0 (severe measure inflation)
IF INTENTIONAL: Must use aggregation bridge or intermediate deduplication
IF UNINTENTIONAL: STOP. Fix the data model. Do not proceed with N:N join results.
```

---

## PROCEDURE

### STEP 1 — Pre-Join Audit

**For the LEFT table:**
```
1a. Record row count: N_left = SELECT COUNT(*) FROM left_table
1b. Record distinct join key count: U_left = SELECT COUNT(DISTINCT join_key) FROM left_table
1c. Check for NULLs in join key: NULLS_left = SELECT COUNT(*) FROM left_table WHERE join_key IS NULL
1d. Retrieve grain contract from Engine A2
```

**For the RIGHT table:**
```
1e. Record row count: N_right = SELECT COUNT(*) FROM right_table
1f. Record distinct join key count: U_right = SELECT COUNT(DISTINCT join_key) FROM right_table
1g. Check for NULLs in join key: NULLS_right = SELECT COUNT(*) FROM right_table WHERE join_key IS NULL
1h. Retrieve grain contract from Engine A2
```

**Compute expected relationship via per-key multiplicity (not global count alone):**
```
STEP 1a — Profile LEFT key distribution:
    SELECT join_key, COUNT(*) AS m_L FROM left_table GROUP BY join_key
    → max_m_L = MAX(m_L)

STEP 1b — Profile RIGHT key distribution:
    SELECT join_key, COUNT(*) AS m_R FROM right_table GROUP BY join_key
    → max_m_R = MAX(m_R)

STEP 1c — Classify cardinality from per-key multiplicity:
    1:1  iff  max_m_L = 1  AND  max_m_R = 1
    1:N  iff  max_m_L = 1  AND  max_m_R > 1
    N:1  iff  max_m_L > 1  AND  max_m_R = 1
    N:N  iff  max_m_L > 1  AND  max_m_R > 1  -> HALT (see N:N policy)

NOTE: Global U_left vs N_left comparison is a PRELIMINARY SCREEN only.
      It confirms that duplicates exist but cannot identify which specific keys
      are duplicated or whether those keys overlap on the other side.
      Per-key multiplicity is required for precise cardinality classification.

EXAMPLE — WHERE GLOBAL COUNT MISLEADS:
    Left: 100 rows, U_left=99 (one key duplicated)
    Right: 50 rows, U_right=50 (all unique)
    Global: N:1 expected; per-key: only 1 key affected
    Actual fan-out: phi = 101/100 = 1.01, not uniformly 2.0
```

**Identify a critical measure for reconciliation:**
```
Select a SUM-able measure from the left table (e.g., revenue, quantity, cost).
Record: PRE_SUM = SELECT SUM(measure) FROM left_table
```

### STEP 2 — Execute Join
Execute the join with the declared join_type and join_keys.
Do not filter or aggregate yet — inspect the raw joined result first.

### STEP 3 — Post-Join Audit

```
3a. N_result = SELECT COUNT(*) FROM join_result
3b. Fan-out factor: φ = N_result / N_left
3c. POST_SUM = SELECT SUM(measure) FROM join_result
3d. Measure inflation: Δ% = (POST_SUM - PRE_SUM) / PRE_SUM × 100
3e. Unmatched left: SELECT COUNT(*) FROM left_table LEFT JOIN right_table WHERE right.key IS NULL
3f. Unmatched right: SELECT COUNT(*) FROM right_table LEFT JOIN left_table WHERE left.key IS NULL
```

### STEP 4 — Evaluate Results

```
PASS CONDITIONS:
├── φ = 1.0 for 1:1 and N:1 joins (no fan-out)
├── φ > 1.0 for known 1:N joins where N > 1 is expected
├── Δ% = 0% (measure sum unchanged — no inflation)
├── Unmatched left rows = 0 for INNER joins (or expected for LEFT joins)
└── Unmatched right rows documented and understood

FAIL CONDITIONS:
├── φ > 1.0 for an expected 1:1 or N:1 join → FAN-OUT
├── Δ% > 1% on a measure sum that should not change → MEASURE INFLATION
├── Δ% < -5% on a LEFT join (too many unmatched rows) → DATA LOSS
└── N:N join detected without explicit design justification → HALT

WARNING CONDITIONS:
├── Δ% between 0.1% and 1.0% → Investigate
├── Unmatched rows > 5% of left table → Investigate referential integrity
└── NULLs in join key > 0 → Document and decide treatment
```

### STEP 5 — Remediation (If Failed)
```
FAN-OUT DETECTED (φ > 1.0 unexpectedly):
    CAUSE A: Right table has duplicate join keys
        → Pre-aggregate right table to unique join key before joining
        → e.g., SELECT join_key, SUM(measure) FROM right GROUP BY join_key

    CAUSE B: SCD dimension not filtered to current version
        → Add filter: WHERE valid_to IS NULL or WHERE is_current = TRUE

    CAUSE C: Missing composite key
        → Add additional join condition to reduce cardinality

MEASURE INFLATION DETECTED (Δ% ≠ 0 for expected 1:1 or N:1):
    → Fan-out is the cause; apply CAUSE A/B/C remediation above

DATA LOSS DETECTED (too many unmatched rows):
    → Investigate referential integrity
    → Switch to LEFT JOIN if dropping unmatched rows is incorrect
    → Document which rows are dropped and why in Assumption Registry (A5)

N:N DETECTED:
    → Escalate to data model review
    → Create bridge table with explicit keys
    → Never proceed with raw N:N join results
```

### STEP 6 — Document Join Audit Report
Complete the Output Contract and file it in provenance (Engine A4).

---

## DECISION TREE
```
New join required
       │
       ▼
Step 1: Pre-join audit both tables
       │
       ▼
Determine expected relationship (1:1, 1:N, N:1, N:N)?
       │
    N:N? ─── YES → HALT. Design review required.
       │
       NO ▼
Execute join (Step 2)
       │
       ▼
Step 3: Post-join audit
       │
       ▼
φ = 1.0? (for 1:1 or N:1 expected)
       │
  YES ▼          NO ▼
Δ% = 0%?       FAN-OUT → Step 5 Remediation A/B/C
  YES ▼
Unmatched rows acceptable?
  YES ▼          NO ▼
PASS ✓         WARNING → Investigate referential integrity
```

---

## MATHEMATICAL DEFINITIONS

**Fan-out Factor:**
```
phi = N_result / N_left

Interpretation:
phi = 1.0  -> no row multiplication; expected for 1:1 and N:1 joins
phi = 2.0  -> average row multiplicity of 2 (each left row matched 2 right rows on average)
phi = 1.5  -> 50% row inflation; partial fan-out

IMPORTANT: phi measures ROW multiplication, not measure inflation directly.
Measure inflation depends on how the inflated rows are distributed across measure values.
A phi of 2.0 implies revenue is doubled ONLY if the duplicated rows have the same
distribution of revenue as the overall population. Verify independently via POST_SUM.
```
**Measure Inflation (must be measured independently from phi):**
```
Delta_pct = (POST_SUM - PRE_SUM) / |PRE_SUM| * 100

This is the DEFINITIVE measure of inflation. Compute it directly; do not derive from phi.

WHY phi != Delta_pct in general:
    If duplicated rows have above-average measure values:
        Delta_pct > (phi - 1) * 100
    If duplicated rows have below-average measure values:
        Delta_pct < (phi - 1) * 100
    If fan-out is uniform AND measure values are uniformly distributed:
        Delta_pct = (phi - 1) * 100  [this special case rarely holds in practice]

RULE: Always measure Delta_pct from POST_SUM vs PRE_SUM.
      Never assume Delta_pct = (phi - 1) * 100.
```
**Referential Integrity Score:**
```
RI = 1 - (N_unmatched_left / N_left)
RI = 1.0 → perfect integrity (all left rows have match)
RI < 0.95 → more than 5% data loss → investigate
```

---

## PRECONDITIONS
- [ ] Grain contracts for both tables are completed (Engine A2).
- [ ] Join keys are identified and their data types verified to match.
- [ ] At least one SUM-able measure exists for reconciliation.
- [ ] The purpose of the join is explicitly stated.

## ASSUMPTIONS
- NULL join keys do not match each other (SQL standard behavior).
- If NULLs in join key are valid entities, they must be handled separately.
- Measure reconciliation uses the left table's primary measure by default.

---

## EDGE CASES

| Case | Problem | Resolution |
|------|---------|------------|
| Joining on a fuzzy key (name strings) | False matches and missed matches | Use unique surrogate keys; never join on natural language fields |
| SCD Type 2 dimension | Multiple rows per entity (one per version) | Filter to current version before joining |
| NULL join keys on either side | NULLs excluded from INNER JOIN silently | Identify null counts, document exclusion |
| Composite join key with partial match | Partial fan-out from one key component | Profile each component separately |
| Self-join | Fan-out from matching entity to itself | Use explicit inequality conditions |
| Currency-inconsistent measures | Inflation/deflation appears as fan-out | Normalize currency before measure reconciliation |
| Joining aggregated to raw | Grain mismatch between tables | Pre-aggregate to matching grain |

---

## FAILURE MODES

| Failure | Symptom | Detection | Severity |
|---------|---------|-----------|----------|
| Silent fan-out | Revenue doubled | φ > 1.0 | CRITICAL |
| N:N join | Row count and aggregates explode (row multiplication is unbounded) | φ >> 1.0, N:N detected | CRITICAL |
| SCD not filtered | Historical attributes leak into current data | Multiple dim rows per entity | HIGH |
| Unmatched rows dropped silently | Underreported metrics | RI < 0.95 | HIGH |
| NULL key exclusion undocumented | Invisible population reduction | NULL count in key | MEDIUM |
| Wrong join type (INNER vs LEFT) | Data loss | Unmatched row count | HIGH |

---

## WORKED EXAMPLE

**Task:** Join `orders` (left) to `dim_products` (right) to get product category for each order.

```
PRE-JOIN AUDIT:
    N_left (orders): 50,000 rows
    U_left (order_id): 50,000 → grain: 1 row per order ✓
    NULLS in product_id (left): 0

    N_right (dim_products): 200 rows
    U_right (product_id): 198 ← NOT 200! 2 duplicates detected

EXPECTED: N:1 join (many orders to one product)
DUPLICATE IN RIGHT: 2 product_ids appear twice (SCD Type 2 — old and new version)

JOIN EXECUTED: INNER JOIN on product_id

POST-JOIN AUDIT:
    N_result: 50,100 rows (100 extra rows due to duplicate product_ids)
    φ = 50,100 / 50,000 = 1.002
    PRE_SUM(revenue) = $5,000,000
    POST_SUM(revenue) = $5,010,000
    Δ% = +0.2%

VERDICT: FAIL — measure inflation detected (φ = 1.002)

REMEDIATION:
    The dim_products table has 2 product_ids with two versions (SCD Type 2).
    Add filter: WHERE dim_products.is_current = TRUE
    → Re-execute join
    → Confirm N_result = 50,000 and Δ% = 0%
```

---

## ADVERSARIAL EXAMPLE

**Request:** "Just join orders to products and to customers simultaneously, then compute total revenue."

**Engine Response:**
```
BLOCKED — Multi-table join requires sequential audit.

ISSUE: If orders → products introduces any fan-out,
       and then that result is joined to customers,
       the compound fan-out effect will be:
       φ_total = φ_products × φ_customers

       Example: φ_products = 1.1, φ_customers = 1.05
       φ_total = 1.155 → Revenue inflated by 15.5%

REQUIRED: Execute Join Audit for each join separately in sequence:
    Step 1: Audit orders JOIN products → verify φ = 1.0
    Step 2: Audit result JOIN customers → verify φ = 1.0
    Only after both audits pass may revenue be computed.
```

---


## COUNTEREXAMPLES

**Counterexample A � Trusting a Named Column as Unique:**
A table has a column named `order_id` but the actual grain is order � product_line.
`
WRONG ASSUMPTION: order_id is unique ? join proceeds ? fan-out f = 3.2
CORRECT: Profile U_left. Discover order_id repeats 3.2� per order.
? Adjust grain; add product_line_id to key before joining.
`

**Counterexample B � Assuming LEFT JOIN Preserves Row Count:**
`
WRONG: LEFT JOIN always returns the same rows as left table.
CORRECT: LEFT JOIN returns AT LEAST left table rows, MORE if right has duplicates.
? A LEFT JOIN to a dimension with SCD duplicates will inflate rows EXACTLY like INNER JOIN.
`
## VALIDATION RULES
1. Join Audit must be completed before any aggregation on joined data.
2. Fan-out factor and measure reconciliation must both pass (φ = expected, Δ% < tolerance).
3. All N:N joins must have explicit design justification or be rejected.
4. Results of this audit must be filed in Data Provenance (Engine A4).

## TEST CASES

| ID | Input | Expected | Pass Condition |
|----|-------|----------|----------------|
| JAE-001 | 1:1 join, right has duplicate key | φ > 1.0 detected | Engine flags fan-out, blocks aggregation |
| JAE-002 | N:N join | Engine halts | Explicit halt with design review request |
| JAE-003 | SCD dim not filtered | 2 rows per entity | Engine detects U_right < N_right, recommends filter |
| JAE-004 | LEFT join drops 10% rows | RI = 0.90 | Engine issues WARNING, documents unmatched rows |
| JAE-005 | Valid 1:1 join, Δ% = 0% | PASS | Engine confirms and proceeds |
| JAE-006 | Multi-table join requested in one step | Blocked | Engine requires sequential audit |

---

## AGENT EXECUTION INSTRUCTIONS
1. Invoke this engine before every JOIN or merge operation.
2. Do not proceed with analysis if verdict is FAIL.
3. For WARNING verdicts, document the condition in the Assumption Registry (A5) and proceed only if the warning is understood and accepted.
4. File every Join Audit Report in Data Provenance (Engine A4) so analysis results can be traced back.
5. If a user claims "the join is fine" without evidence — run the audit anyway.
