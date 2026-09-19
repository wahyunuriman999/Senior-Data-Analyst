# DATA GRAIN ENGINE
**Phase A — Foundation Brain | Engine A2**
**Depth Contract: FULL**

---

## PURPOSE
Determine and validate the analytical grain of every dataset before any aggregation, join, or visualization. Grain is the atomic unit of a fact table — it defines what one row represents. Incorrect grain assumptions produce aggregations that are mathematically wrong, even if they look plausible.

## SCOPE
- All datasets before any aggregation.
- All joins between tables (input to Join Audit Engine A3).
- All derived metrics that aggregate across dimensions.
- All dashboards where a metric rolls up from transactional data.

---

## INPUTS
```
INPUT
├── dataset_name             : Source table or file identifier
├── sample_rows              : At minimum 1,000 rows for profiling
├── schema                   : Column names and data types
├── domain_context           : Business domain (Sales, HR, Finance, Product)
└── candidate_key_columns    : Columns that might form a unique key
```

## OUTPUT CONTRACT
```
OUTPUT — GRAIN CONTRACT
├── declared_grain           : entity × time × event (explicit statement)
├── is_unique                : Boolean — does candidate key uniquely identify rows?
├── grain_violations         : List of duplicate key combinations found
├── grain_type               : (transactional | snapshot | aggregate | event_log | bridge)
├── safe_aggregations        : List of operations valid at this grain
├── unsafe_aggregations      : List of operations that will produce incorrect results
├── join_compatibility       : Which other tables are joinable without fan-out
└── remediation              : If grain violation found — corrective action
```

---

## GRAIN TYPE TAXONOMY

### TRANSACTIONAL GRAIN
One row = one discrete event (e.g., one order, one payment, one click).
```
CHARACTERISTICS:
├── Row count grows continuously over time
├── Timestamp column with high specificity (to-the-second)
├── Each row represents an atomic business event
└── Safe for SUM, COUNT; unsafe for direct snapshot-style aggregations

EXAMPLE: orders table
    order_id | customer_id | order_date | amount
    Each row = one order placed
    Grain = OrderID × OrderDate × Purchase
```

### SNAPSHOT GRAIN
One row = the state of an entity at a specific point in time.
```
CHARACTERISTICS:
├── Row count grows with entities × snapshot frequency
├── Date/period column (daily, weekly, monthly)
├── Represents the value at a moment, not an event
└── SUM across time is WRONG; use latest snapshot or period-specific snapshot

EXAMPLE: monthly_account_balances
    account_id | month | balance
    Each row = account balance at end of that month
    DANGER: SUM(balance) across all months ≠ "total balance" — it's nonsense
    CORRECT USE: Filter to specific month, then aggregate across accounts
```

### AGGREGATE GRAIN
One row = pre-aggregated result (e.g., daily sales by region).
```
CHARACTERISTICS:
├── Represents a roll-up of lower-grain data
├── Cannot be further rolled up without careful weighting
├── Non-additive metrics (averages, rates) may be embedded

EXAMPLE: daily_revenue_by_region
    region | date | total_revenue | avg_order_value
    DANGER: AVG(avg_order_value) across regions ≠ true average order value
    CORRECT: Re-aggregate from transactional grain
```

### EVENT LOG GRAIN
One row = one log entry (system events, user actions).
```
CHARACTERISTICS:
├── Very high row counts
├── Multiple event types in same table (event_type column)
├── Must filter to specific event type before aggregating

EXAMPLE: user_events
    user_id | event_type | event_timestamp | properties
    DANGER: COUNT(*) = all events, not unique users
    CORRECT: COUNT DISTINCT(user_id) WHERE event_type = 'purchase'
```

### BRIDGE GRAIN
One row = one relationship between two entities (many-to-many).
```
CHARACTERISTICS:
├── Joins between bridge and fact tables cause fan-out
├── Requires special handling to avoid measure inflation

EXAMPLE: order_products (one order can have many products)
    order_id | product_id | quantity
    DANGER: JOIN to orders → revenue will be multiplied per product line item
    CORRECT: Aggregate to order grain before joining, or use specific product-level metrics
```

---

## PROCEDURE

### STEP 1 — Declare Candidate Grain
Based on domain context and schema, hypothesize what one row represents:
```
HEURISTICS:
├── Does the table have a column named *_id with high uniqueness? → Likely entity key
├── Is there a timestamp column? → Likely event or snapshot grain
├── Are there multiple columns that together seem unique? → Compound grain
├── Are there repeated values in what looks like a key column? → Grain might be lower
└── Does the table name suggest aggregation (monthly_, daily_, summary_)? → Likely aggregate grain
```

### STEP 2 — Profile Row Uniqueness
```
OPERATION:
    SELECT candidate_key, COUNT(*) as row_count
    FROM dataset
    GROUP BY candidate_key
    HAVING COUNT(*) > 1

IF result_set IS EMPTY:
    → Candidate key is unique → grain hypothesis confirmed
IF result_set IS NOT EMPTY:
    → Grain violation found → proceed to Step 3

MATHEMATICAL CHECK:
    Let N = total row count
    Let U = distinct value count of candidate_key
    If N = U → grain is valid
    If N > U → duplicates exist; (N - U) excess rows present
    Fan-out factor = N / U
```

### STEP 3 — Investigate Grain Violations
When N > U, determine whether duplicates are:
```
TYPE A — LEGITIMATE MULTIPLE EVENTS:
    Example: One customer_id appears 5 times because they placed 5 orders.
    → The grain is customer × order, not just customer.
    → Add order_id to the grain key.

TYPE B — UNINTENDED DUPLICATES (DATA QUALITY ISSUE):
    Example: Same order_id appears twice due to ETL bug.
    → This is a data quality problem, not a grain problem.
    → Document in Assumption Registry (Engine A5) and deduplicate with business confirmation.

TYPE C — MULTI-VALUED DIMENSION (FAN-OUT FROM EARLIER JOIN):
    Example: order_id appears 3 times because it was joined to a product dimension with 3 matching rows.
    → Reverse-engineer the join source and correct upstream.
    → See Join Audit Engine A3.

DECISION RULE:
    IF duplicate rows are identical across all columns → Type B (dedup)
    IF duplicate rows differ in some columns → Type A or C (investigate dimension)
```

### STEP 4 — Classify Safe vs Unsafe Aggregations
```
FOR EACH AGGREGATION TYPE, CLASSIFY BASED ON GRAIN:

ALWAYS SAFE (for all grain types):
├── COUNT(*) → counts rows, interpretation depends on grain
├── MIN, MAX → safe as long as grain is correct
└── COUNT DISTINCT on a key column → safe if key is truly distinct

SAFE FOR TRANSACTIONAL GRAIN:
├── SUM(measure) → correct if grain is not duplicated
└── AVG(measure) → correct arithmetic mean at that grain

UNSAFE — REQUIRES SPECIAL HANDLING:
├── SUM across a snapshot grain (double-counts periods)
├── AVG of pre-aggregated averages (averages of averages)
├── COUNT(*) in a table with fan-out (overcounts entities)
├── COUNT DISTINCT across joined tables with fan-out
└── Percentage-of-total where total includes grain-level duplicates
```

### STEP 5 — Document Grain Contract
```
GRAIN CONTRACT: [Table/Dataset Name]
──────────────────────────────────────
Declared Grain:     [entity × time × event]
Grain Type:         [transactional | snapshot | aggregate | event_log | bridge]
Unique Key:         [column(s) that uniquely identify a row]
Is Unique:          [YES | NO — with duplicate count if NO]
Grain Violations:   [list with row counts]
Safe Aggregations:  [SUM(revenue), COUNT(order_id), ...]
Unsafe:             [SUM across time for snapshot, AVG of avg_order_value, ...]
Join Compatibility: [Which tables join safely at this grain]
Remediation:        [If violations exist — dedup strategy or grain correction]
──────────────────────────────────────
```

---

## DECISION TREE
```
Dataset received
      │
      ▼
Profile candidate key uniqueness
      │
   N == U?
  YES ▼    NO ▼
Grain      Investigate violations
valid           │
  │        All cols identical?
  │        YES ▼          NO ▼
  │     Type B: ETL    Cols differ in dimension?
  │     duplicate      YES ▼         NO ▼
  │     → dedup     Type A:      Type C:
  │                 Grain is     Fan-out from
  │                 compound     upstream join
  │                 → add col    → audit join
  │                    │              │
  └────────────────────┴──────────────┘
                        │
                        ▼
               Document Grain Contract
                        │
                        ▼
           Classify safe/unsafe aggregations
                        │
                        ▼
             Proceed to Join Audit (A3)
             if dataset will be joined
```

---

## MATHEMATICAL DEFINITIONS

**Grain Validity:**
```
Let G = {k₁, k₂, ..., kₙ} be the set of grain key columns.
Let F = fact table.

Grain is valid iff:
∀ r₁, r₂ ∈ F : G(r₁) = G(r₂) → r₁ = r₂

Equivalently:
|{G(r) : r ∈ F}| = |F|
(distinct key combinations = total row count)
```

**Fan-out Factor:**
```
φ = N_after_join / N_before_join

φ = 1 → no fan-out (safe join)
φ > 1 → fan-out (measures will be inflated by factor φ)
φ < 1 → data loss from join (check for unmatched rows)
```

---

## PRECONDITIONS
- [ ] Raw dataset is accessible for profiling.
- [ ] Business domain context is known (to disambiguate legitimate vs erroneous duplicates).
- [ ] Schema documentation or data dictionary is available (if possible).
- [ ] Sample size is adequate: minimum 1,000 rows; profile the full table if possible.

## ASSUMPTIONS
- The candidate key provided is a best hypothesis — it must be verified, not assumed.
- Duplicate rows with identical values across all columns are treated as ETL duplicates unless business logic confirms otherwise.
- Snapshot tables are assumed to have one row per entity per period unless contradicted.

---

## EDGE CASES

| Case | Problem | Resolution |
|------|---------|------------|
| Multi-grain table | Table mixes event and snapshot rows (flagged by event_type column) | Separate into subsets before aggregating |
| Slowly Changing Dimension (SCD) | Dimension rows are versioned — same entity_id, multiple validity periods | Use valid_from/valid_to filters before joining |
| Null in key column | NULL key creates invisible duplicates (NULLs are not equal in SQL) | Exclude or handle NULLs in key columns explicitly |
| Bridge table as fact | Joining a bridge to a fact inflates fact measures | Pre-aggregate fact to entity grain before joining bridge |
| Late-arriving data | Rows arrive after the period they belong to | Distinguish event_date from load_date; use event_date for analysis |
| Composite grain with partial nulls | Some key columns are NULL for certain row types | Document conditional grain rules per row type |

---

## FAILURE MODES

| Failure | Symptom | Detection | Severity |
|---------|---------|-----------|----------|
| Assumed grain without verification | Metrics inflated or deflated | Row count discrepancy post-join | CRITICAL |
| Fan-out from join not detected | Revenue or volume double-counted | Fan-out factor φ > 1 | CRITICAL |
| Snapshot grain summed across periods | "Total balance over all months" nonsense metric | Visual: impossible large numbers | HIGH |
| AVG of AVG computed | Wrong weighted metric | Aggregation level check | HIGH |
| Grain shift after transformation | Aggregated dataset treated as transactional | Schema comparison before/after transform | HIGH |
| Null key columns silently excluded | Undercounted metric | NULL count in key columns | MEDIUM |

---

## WORKED EXAMPLE

**Dataset:** `monthly_sales_by_region`
```
Schema:
    region_id | month | total_revenue | order_count | avg_order_value

Candidate key: region_id + month

STEP 1: Hypothesize grain = Region × Month (snapshot aggregate grain)

STEP 2: Profile uniqueness
    SELECT region_id, month, COUNT(*) FROM monthly_sales_by_region
    GROUP BY region_id, month HAVING COUNT(*) > 1
    Result: 0 rows → Grain is VALID

STEP 3: No violations.

STEP 4: Classify aggregations
    SAFE: SUM(total_revenue) across regions for a given month → Total monthly revenue
    SAFE: SUM(order_count) across regions → Total order count
    UNSAFE: SUM(avg_order_value) → Meaningless. Weighted average must be recomputed.
    UNSAFE: SUM(total_revenue) across all months → Only meaningful if explicitly intended

STEP 5: GRAIN CONTRACT
    Declared Grain:  Region × Month (Aggregate Snapshot)
    Grain Type:      Aggregate
    Unique Key:      region_id + month
    Is Unique:       YES
    Safe:            SUM(total_revenue) per month, SUM(order_count) per month
    Unsafe:          AVG(avg_order_value), SUM across all months without filter
    Remediation:     None required
```

---

## ADVERSARIAL EXAMPLE

**Request:** "Sum up all the avg_order_value across regions for Q3 to get our Q3 average."

**Engine Response:**
```
BLOCKED — Aggregation is mathematically invalid.

ISSUE: avg_order_value is a pre-computed average per region per month.
       Summing pre-aggregated averages does not produce a meaningful metric.

       If Region A has avg_order_value = $100 (from 10 orders)
       and Region B has avg_order_value = $200 (from 100 orders):
       Simple SUM: $300 (wrong)
       Simple AVG: $150 (wrong — ignores volume)
       Correct weighted average:
           (10 × $100 + 100 × $200) / (10 + 100) = $190.91

REQUIRED: Recompute from transactional grain using:
    SUM(total_revenue) / SUM(order_count) for Q3 across all regions.
```

---


## COUNTEREXAMPLES

**Counterexample A � Averaging Averages Across Regions:**
A dataset has `avg_order_value` pre-aggregated per region per month.
`
WRONG: AVG(avg_order_value) across all region-month rows
? Averages pre-computed averages without weighting by volume ? meaningless.
RIGHT: SUM(total_revenue) / SUM(order_count) ? volume-weighted correct average.
`

**Counterexample B � Summing Snapshot Balances Across Time:**
A `monthly_balances` table has one row per account per month.
`
WRONG: SUM(balance) across all 12 months � accounts = 12� the correct value.
RIGHT: Filter to end-of-period snapshot (December), then SUM(balance) across accounts.
`
## VALIDATION RULES
1. Grain contract must be documented before any aggregation is performed.
2. Fan-out factor must be calculated and verified for every join operation.
3. Unsafe aggregations must be explicitly flagged if a user requests them.
4. Grain contracts must be revisited if the source schema changes.

## TEST CASES

| ID | Input | Expected | Pass Condition |
|----|-------|----------|----------------|
| DGE-001 | orders table with duplicate order_ids | Grain violation detected | Engine reports N > U with duplicate count |
| DGE-002 | monthly_snapshot, user requests SUM across months | Unsafe aggregation flagged | Engine blocks and explains why |
| DGE-003 | Join of orders to order_products | Fan-out factor computed | φ = avg items per order reported |
| DGE-004 | NULL in customer_id column of fact table | NULL key flagged | Engine reports NULL count and requests policy |
| DGE-005 | SCD dimension joined to fact without date filter | Multiple version rows returned | Engine detects grain explosion |
| DGE-006 | AVG of AVG requested on aggregate table | Blocked | Engine redirects to weighted recomputation |

---

## AGENT EXECUTION INSTRUCTIONS
1. Execute this engine before any aggregation or join on a new dataset.
2. Always profile the candidate key — do not assume it is unique.
3. Classify every aggregation the analysis will require as SAFE or UNSAFE before proceeding.
4. If grain is violated (N > U), halt until the violation is understood and classified.
5. Document the Grain Contract and reference it in the Join Audit Engine (A3).
6. Include grain information in any provenance record (Engine A4).
