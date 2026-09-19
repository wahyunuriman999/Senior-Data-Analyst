# METRIC DEFINITION ENGINE
**Phase A — Foundation Brain | Engine A1**
**Depth Contract: FULL**

---

## PURPOSE
Enforce rigorous, unambiguous metric definitions before any analysis or visualization begins.
A metric without a precise contract is a liability: it produces numbers that look correct but mean different things to different stakeholders.
This engine must be executed for **every KPI or measure** before it is used in analysis, dashboard, or visualization.

## SCOPE
- All numerical measures derived from a dataset.
- All ratios, rates, percentages, growth metrics, and derived aggregations.
- All "obvious" metrics (e.g., Revenue, Users, Orders) — especially these, because they carry the most hidden assumptions.

---

## INPUTS
```
INPUT
├── business_question        : The analytical question being answered
├── dataset                  : The raw or transformed dataset available
├── available_dimensions     : List of categorical/date columns
├── available_measures       : List of numerical columns
├── reporting_context        : Audience, domain, and granularity required
└── existing_definitions     : Any prior agreed metric contracts (if available)
```

## OUTPUT CONTRACT
```
OUTPUT — METRIC CONTRACT
├── metric_name              : Official name used consistently
├── metric_type              : (count | distinct_count | sum | average | ratio | rate | percentage | index | weighted | derived)
├── numerator                : Formula + filters + population
├── denominator              : Formula + filters + population + stability notes
├── grain                    : entity × time × event
├── time_window              : Inclusive/exclusive bounds, timezone, fiscal vs calendar
├── inclusions               : What qualifies for numerator and denominator
├── exclusions               : What is explicitly removed and why
├── unit                     : Currency, percentage, count, duration, etc.
├── aggregation_level        : How the metric rolls up (sum-able, average-able, weighted)
├── null_handling            : How NULLs are treated in numerator and denominator
├── caveats                  : Known data lags, approximations, or measurement issues
└── validation_check         : A specific test query or calculation to verify the metric is correct
```

---

## PROCEDURE

### STEP 1 — Identify Analytical Object
Determine what the metric is fundamentally measuring:
```
IF counting distinct entities (users, orders, products)
    → metric_type = distinct_count
    → WARNING: Distinct count is NOT sum-able across dimensions

IF summing a continuous measure (revenue, cost, quantity)
    → metric_type = sum
    → CHECK: Is the column grain correct? Avoid double-counting.

IF measuring a ratio (conversion rate, margin %)
    → metric_type = ratio
    → REQUIRES: Both numerator and denominator fully defined
    → REQUIRES: Denominator stability check (Step 8)

IF measuring change over time (growth rate, MoM delta)
    → metric_type = rate
    → REQUIRES: Prior period definition (Step 9)

IF measuring a weighted average (average order value per region weighted by volume)
    → metric_type = weighted
    -> Use weighted mean: Weighted_Mean = [Sum_i(x_i * w_i)] / [Sum_i(w_i)]
              where i = {1,...,n}; this is NOT equivalent to AVG of pre-aggregated averages
    → DO NOT use simple average of averages

IF combining multiple metrics (EBITDA = Revenue − COGS − OpEx)
    → metric_type = derived
    → Define all component metrics first using this engine
    → Derived metric cannot be more precise than its least precise component
```

### STEP 2 — Determine Grain
The grain defines the most atomic row in the fact table.
Express grain as: **entity × time × event**

```
EXAMPLES:
    "One row = one order" → grain = Order × OrderDate × Purchase
    "One row = one daily user session" → grain = UserID × SessionDate × Session
    "One row = one monthly snapshot" → grain = AccountID × Month × Snapshot

FAILURE MODES:
    If grain is ambiguous → aggregations can double-count.
    If join adds rows → grain has silently changed. (→ See Join Audit Engine A3)
    If dataset mixes grains → split before aggregating.

RULE: Never aggregate across mixed grains.
RULE: If grain is unknown, STOP. Profile the dataset first.
```

**Mathematical expression:**
```
Let F be the fact table.
Grain G = {e₁, e₂, ..., t, ev} where eᵢ are entity keys, t is time, ev is event type.
Each row r ∈ F must be uniquely identified by G.
∃ rows rᵢ ≠ rⱼ where G(rᵢ) = G(rⱼ) → GRAIN VIOLATION → must investigate duplicates.
```

### STEP 3 — Define Numerator
```
SPECIFY:
├── Source column(s): exact table.column name
├── Aggregation function: SUM / COUNT / COUNT DISTINCT / MAX / MIN
├── Population filter: e.g., "where status = 'Completed'"
├── Time filter: e.g., "where order_date BETWEEN '2024-01-01' AND '2024-03-31'"
├── Dimension filter: e.g., "where region != 'Test'"
└── Null treatment: e.g., "NULL revenue treated as 0 for completed orders; excluded for pending"

COUNTEREXAMPLE — DO NOT:
"Revenue = SUM(revenue_column)"
← Missing: status filter, null handling, currency normalization

CORRECT FORM:
"Revenue = SUM(orders.gross_revenue_usd)
    WHERE order_status IN ('Completed', 'Shipped')
    AND order_date >= [period_start]
    AND order_date <  [period_end]
    AND is_test_account = FALSE
    NULLS treated as 0 (only for Completed status)"
```

### STEP 4 — Define Denominator
```
SPECIFY (same detail as numerator):
├── Source column(s)
├── Aggregation function
├── Population filter
├── Time filter
├── Dimension filter
└── Null treatment

ADDITIONAL DENOMINATOR CHECKS:
├── Can the denominator be zero? → define zero-denominator handling
├── Is the denominator the same population as numerator? → verify alignment
└── Is the denominator stable across time periods? → verify (Step 8)

COUNTEREXAMPLE — CONVERSION RATE:
BAD:  Conversion Rate = Orders / Visitors  ← Visitors from which session? Unique or total?
GOOD: Conversion Rate = COUNT DISTINCT(orders.user_id WHERE order_completed)
                      / COUNT DISTINCT(sessions.user_id WHERE session_date IN period
                                       AND channel != 'Internal')
```

### STEP 5 — Determine Population
```
DEFINE EXPLICITLY:
├── What entities are in scope?
├── What time range is in scope?
├── What dimension values are in scope?
├── Are there exclusions (test accounts, internal, canceled)?

POPULATION MISMATCH is the #1 cause of metric errors.
Example: If numerator = active paying users
        and denominator = all registered users
        → Metric is NOT "activation rate."
        → It is something else; name it correctly.
```

### STEP 6 — Determine Exclusions
```
Explicitly document every exclusion and the rationale:
├── Test/internal accounts → excluded because they distort behavioral metrics
├── Refunded orders → excluded from Revenue, included in Gross Bookings
├── Outlier transactions above $1M → flag and document, do NOT silently remove
├── NULL values in key dimensions → document treatment

RULE: Exclusions must be documented in the metric contract.
RULE: Exclusions must not be applied inconsistently (e.g., exclude from numerator
      but not from denominator — unless that is the intended behavior).
```

### STEP 7 — Validate Aggregation Level
```
CHECK: Is the metric sum-able across dimensions?

sum-able: Revenue (sum across regions = total revenue)
NOT sum-able: Conversion Rate (rate across regions ≠ sum of rates)
NOT sum-able: Average Order Value (avg across regions ≠ sum of averages)
NOT sum-able: Count Distinct Users (distinct across regions ≠ sum per region if users appear in multiple regions)

FOR NON-SUM-ABLE METRICS:
    → Use weighted average or re-aggregate from grain level
    → DO NOT average percentages; re-compute from components

Mathematical:
    WRONG: AVG(conversion_rate_by_region) where n regions exist
    RIGHT: SUM(converted_users_all_regions) / SUM(eligible_users_all_regions)
```

### STEP 8 — Check Denominator Stability
```
A denominator that changes in size due to external factors can make a metric misleading.

EXAMPLE:
    Churn Rate = Churned Users / Total Users (start of month)
    If Total Users grew 30% during the month → denominator at end of month is wrong.
    → Use denominator = users at START of period.

CHECK:
├── Does denominator change within the measurement period?
├── Is denominator affected by the same events driving the numerator?
├── Is denominator subject to retroactive correction (data lags)?
└── Is denominator consistent with how the metric has been defined historically?
```

### STEP 9 — Check Time Semantics
```
DEFINE PRECISELY:
├── Period start: inclusive or exclusive? (>= vs >)
├── Period end: inclusive or exclusive? (< vs <=)
├── Fiscal year vs calendar year
├── Timezone: UTC or local? If multi-region, which timezone?
├── Event date vs processing date vs report date
├── Cutoff for incomplete periods: use as-of date or exclude incomplete month?

COUNTEREXAMPLE:
    BAD:  "Revenue last quarter"
    ← Which quarter? Fiscal Q3 or calendar Q3? UTC or PST close? Through yesterday or through last midnight?

    GOOD: "Revenue for fiscal Q3 2024 (July 1 – September 30, 2024, inclusive),
          measured by order_date in UTC, as of 2024-10-01 00:00 UTC"
```

### STEP 10 — Produce Metric Contract
Assemble all of the above into a formal metric contract:
```
METRIC CONTRACT: [Metric Name]
──────────────────────────────────────────────
Metric Type:    [ratio | sum | count | ...]
Numerator:      [exact formula with filters]
Denominator:    [exact formula with filters]
Grain:          [entity × time × event]
Time Window:    [start (inclusive) → end (exclusive), timezone, fiscal/calendar]
Population:     [in-scope entities]
Exclusions:     [explicit list with reasons]
Unit:           [USD | % | count | ...]
Aggregation:    [sum-able | not sum-able; roll-up method]
Null Handling:  [numerator null = 0 | excluded | error flag]
Caveats:        [known issues, lags, approximations]
Validation:     [specific SQL/formula to cross-check result]
──────────────────────────────────────────────
```

---

## DECISION TREE
```
START: New metric requested
         │
         ▼
Is metric explicitly defined in existing contracts?
         │
     YES ▼                 NO ▼
Use existing contract     Execute Steps 1–10
    │                          │
    ▼                          ▼
Verify contract still      Does metric involve a ratio?
matches current dataset         │
schema and population       YES ▼           NO ▼
         │              Check denominator   Check grain
         │              stability (S8)      (Step 2)
         ▼                   │                  │
Cross-validate with         ▼                  ▼
validation check        Time semantics     Aggregation
(Step 10)               defined (S9)?      level valid (S7)?
         │                   │                  │
         ▼                   ▼                  ▼
     PASS/FAIL         Produce Contract    Produce Contract
```

---

## MATHEMATICAL DEFINITIONS

**Ratio Metric:**
$$M_{ratio} = \frac{\sum_{i \in N} v_i}{\sum_{j \in D} w_j}$$
where N = numerator population, D = denominator population, v and w are values.

**Weighted Average:**
$$\bar{x}_w = \frac{\sum_{i=1}^{n} x_i \cdot w_i}{\sum_{i=1}^{n} w_i}$$
where x_i is the measure value for entity i, w_i is the weight for entity i, and summation bounds are i = 1 to n on BOTH numerator and denominator.

**Period-over-Period Growth Rate:**
$$g = \frac{M_{current} - M_{prior}}{|M_{prior}|} \times 100\%$$
⚠️ If M_prior = 0, growth rate is undefined. Report as "N/A — zero base."
⚠️ If M_prior < 0 (e.g., negative operating income), growth rate is directionally inverted. Flag explicitly.

**Contribution to Change:**
$$\Delta M_{total} = \sum_{k} \Delta M_k$$
where ΔMₖ is the contribution from segment k.

---

## PRECONDITIONS
- [ ] Dataset schema is known and grain is verified.
- [ ] Business question is explicit (not "analyze everything").
- [ ] Column names have been verified against the actual dataset (not assumed from memory).
- [ ] Time range boundaries are confirmed.

## ASSUMPTIONS
- All currency values are in the same denomination unless explicitly converted.
- NULL in a measure does NOT equal 0 unless business logic explicitly confirms this.
- Count distinct is bounded by the dataset period — cross-period distinct counts require special handling.

---

## EDGE CASES

| Case | Problem | Resolution |
|------|---------|------------|
| Denominator = 0 | Division by zero | Return NULL, flag in output, do not divide |
| All numerator values are NULL | SUM = 0 or NULL depending on engine | Distinguish "zero revenue" from "no data" |
| Metric defined differently in two source systems | Conflicting definitions | Escalate to metric owner; use one canonical definition |
| Metric aggregated at wrong grain | Fan-out inflation | Re-aggregate from lowest grain |
| Fiscal and calendar periods misaligned | Incorrect period-over-period | Lock fiscal calendar mapping |
| Users appear in multiple regions | Distinct count inflated | Assign primary region or count by transaction |
| Test account contamination | Metric inflated | Exclude via explicit filter, document exclusion |
| Retroactive data corrections | Historical metrics change | Use snapshot date for historical comparisons |

---

## FAILURE MODES

| Failure | Symptom | Detection | Severity |
|---------|---------|-----------|----------|
| Missing denominator definition | Rate metric cannot be verified | Metric contract incomplete | CRITICAL |
| Grain mismatch | Row count increases after join | Join Audit (Engine A3) | CRITICAL |
| NULL = 0 assumed silently | Revenue understated or overstated | NULL count profile | HIGH |
| Non-sum-able metric averaged | Incorrect roll-up | Aggregation level check (S7) | HIGH |
| Wrong time boundary | Wrong period included/excluded | Time semantics check (S9) | HIGH |
| Test accounts included | Inflated engagement metrics | Exclusion filter missing | MEDIUM |
| Inconsistent exclusions | Numerator/denominator mismatch | Population check (S5) | HIGH |

---

## WORKED EXAMPLE

**Business Question:** "What is our monthly conversion rate for paying customers?"

```
STEP 1: metric_type = ratio

STEP 2: grain = UserID × Month × Session
    (One row per user per month; a user can have multiple sessions in a month)

STEP 3: Numerator
    = COUNT DISTINCT(users.user_id)
      WHERE first_payment_date >= period_start
        AND first_payment_date <  period_end
        AND user_type != 'internal'

STEP 4: Denominator
    = COUNT DISTINCT(sessions.user_id)
      WHERE session_date >= period_start
        AND session_date <  period_end
        AND channel != 'bot'
        AND user_type != 'internal'

STEP 5: Population
    Numerator: new paying users in period
    Denominator: all non-bot sessions in period (distinct users)

STEP 6: Exclusions
    Internal team accounts (user_type = 'internal')
    Bot traffic (channel = 'bot')
    Reason: They distort both numerator (internal purchases) and denominator (artificial sessions)

STEP 7: NOT sum-able across months. Must re-compute from components per period.

STEP 8: Denominator = sessions in same period. Stable — not retroactively corrected.

STEP 9: period_start = YYYY-MM-01 00:00 UTC (inclusive)
        period_end   = YYYY-MM+1-01 00:00 UTC (exclusive)

STEP 10: METRIC CONTRACT
    Metric: Monthly Conversion Rate
    Type: ratio
    Numerator: COUNTD(paying users, non-internal, first_payment in period)
    Denominator: COUNTD(sessioning users, non-bot, non-internal, session in period)
    Grain: UserID × Month
    Time Window: Calendar month, UTC boundaries
    Unit: %
    Aggregation: NOT sum-able — recompute from grain
    Null Handling: Users with NULL user_type excluded
    Caveats: 48-hour payment processing delay may cause end-of-month undercounting
    Validation: Cross-check vs billing system monthly new subscriptions
```

---

## ADVERSARIAL EXAMPLE

**Request:** "Just calculate Conversion Rate = orders / sessions."

**Engine Response:**
```
BLOCKED — Metric contract is incomplete.

ISSUES DETECTED:
1. "orders" is undefined. Does it mean:
    (a) all orders including refunded?
    (b) only completed orders?
    (c) unique ordering users or total order count?

2. "sessions" is undefined. Does it mean:
    (a) unique users who had a session?
    (b) total session count (one user can have 100 sessions)?
    Using total sessions would deflate conversion rate by up to 20x.

3. No population filter. Internal and bot traffic would contaminate result.

4. No time boundary specified.

REQUIRED: Complete Steps 1–10 of Metric Definition Engine before proceeding.
```

---

## VALIDATION RULES
1. Every metric used in a dashboard must have a completed Metric Contract.
2. Validation cross-check must be run before metric is displayed.
3. If validation fails (result differs from cross-check by >1%), investigate before publishing.
4. Metrics must be reviewed if underlying schema changes.

## TEST CASES

| ID | Input | Expected Output | Pass Condition |
|----|-------|----------------|----------------|
| MDE-001 | "Revenue" with no definition | Engine requests metric contract | Engine does not return a number |
| MDE-002 | Conversion Rate with denominator = all visitors | Engine flags population mismatch | Warning raised about denominator population |
| MDE-003 | AVG(region_conversion_rate) requested | Engine rejects simple average | Engine returns weighted re-aggregation |
| MDE-004 | Denominator = 0 scenario | Engine returns NULL | No division by zero error |
| MDE-005 | Metric with NULL revenue, no null handling specified | Engine halts and requests null policy | No silent 0-substitution |
| MDE-006 | Same metric defined differently in two tables | Engine flags conflict | Conflict escalation logged |

---

## AGENT EXECUTION INSTRUCTIONS
When activated for metric definition:
1. Do NOT compute a metric before completing this engine.
2. Ask clarifying questions if Steps 1–9 cannot be completed from available information.
3. Output the completed Metric Contract before any analysis begins.
4. If a user provides a pre-defined metric, verify it against Steps 1–9. If any step is incomplete, flag it.
5. Never assume a metric definition based on column names alone.
6. When presenting analysis results, always reference the Metric Contract used.
