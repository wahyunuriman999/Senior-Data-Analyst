# ASSUMPTION REGISTRY ENGINE
**Phase A — Foundation Brain | Engine A5**
**Depth Contract: FULL**

---

## PURPOSE
Every analytical decision that cannot be derived directly from the data must be recorded as an explicit assumption. This engine prevents invisible analytical choices from silently distorting results — choices like imputing missing values, excluding outliers, choosing a time boundary, or defining "active user." Every assumption has an ID, a justification, a severity, and a materiality assessment.

The core rule: **Never silently assume.**

## SCOPE
- All missing value treatments.
- All outlier decisions (treat as error vs. legitimate observation).
- All definition choices (e.g., what "active" means, what "revenue" includes).
- All exclusions applied to data.
- All imputation strategies.
- All data cleaning decisions that could affect the analytical result.
- All model choices (e.g., linear vs. log-log regression).

---

## INPUTS
```
INPUT
├── analytical_context       : What analysis is being performed
├── detected_data_issues     : Missing values, outliers, ambiguities found during profiling
├── business_domain          : Domain context to assess materiality
├── available_alternatives   : What other valid choices were available
└── stakeholder_information  : Who would be affected by the assumption choice
```

## OUTPUT CONTRACT
```
OUTPUT — ASSUMPTION ENTRY
├── assumption_id            : Unique ID (format: ASM-YYYY-NNN)
├── category                 : (missingness | outlier | definition | exclusion | imputation | model | boundary)
├── description              : Plain language statement of the assumption
├── rationale                : Why this assumption was made
├── alternative_considered   : What other valid approaches were available
├── materiality              : LOW | MEDIUM | HIGH | CRITICAL
├── direction_of_bias        : UPWARD | DOWNWARD | NEUTRAL | UNKNOWN
├── affected_metrics         : Which KPIs are affected by this assumption
├── validation_possible      : YES | NO | PARTIAL
├── validation_method        : How to check if assumption is reasonable
├── disclosure_required      : YES | NO (should this appear in the output/report?)
└── review_trigger           : Condition under which assumption should be revisited
```

---

## ASSUMPTION CATEGORY TAXONOMY

### MISSINGNESS ASSUMPTIONS
```
BEFORE choosing any missing value treatment, determine the missingness mechanism:

MCAR (Missing Completely At Random):
    Missingness is unrelated to the data itself.
    Example: Random sensor failures in IoT data.
    → Listwise deletion or simple imputation may be acceptable
    → Document that MCAR was assumed and how this was assessed

MAR (Missing At Random):
    Missingness depends on observed variables, not on the missing value itself.
    Example: Older customers less likely to report income (age is observed).
    → Conditional imputation may be appropriate
    → Document the conditioning variable

MNAR (Missing Not At Random):
    Missingness depends on the missing value itself.
    Example: High earners do not report income (the income is the reason for missing).
    → This is the most dangerous case
    → Simple imputation will bias results
    → Must model missingness explicitly or acknowledge the bias direction

RULE: If missingness mechanism cannot be determined, default to MNAR-safe treatment:
    → Flag as missing; do NOT impute
    → Report the missingness rate as an analytical caveat
    → NEVER silently substitute mean, median, or mode without checking the mechanism first

SPECIFIC CASE — NULL REVENUE:
    Revenue = NULL does NOT mean Revenue = 0 unless:
        (a) Business logic explicitly confirms this (e.g., trial user, $0 plan)
        (b) The source system uses NULL to represent zero transaction value
    If uncertain → classify as MNAR → flag; do NOT impute

SPECIFIC CASE — NULL IN DIMENSION:
    NULL product_id might mean:
        (a) The product was deleted (MNAR)
        (b) The order was placed before product tracking was implemented (MAR)
        (c) Random system error (MCAR)
    Each case has a different treatment.
```

### OUTLIER ASSUMPTIONS
```
BEFORE treating any value as an outlier:

STEP 1: Statistical detection
    Z-score > 3: unusual but not necessarily an error
    IQR method: outside 1.5 × IQR from Q1/Q3
    Domain method: business rule violation (e.g., transaction > $10M for a consumer product)

STEP 2: Determine nature
    LEGITIMATE OBSERVATION:
        Example: A single $2M enterprise deal in a $50 average-order-value business.
        → MUST NOT be removed; it represents real business activity
        → May require special visualization treatment (log scale, separate label)

    DATA ERROR:
        Example: A transaction for $9,999,999 when the product costs $99.
        → May be removed after confirmation
        → Document reason, value, and confirmation source

    AMBIGUOUS:
        Example: Cannot determine if $50,000 transaction is legitimate.
        → Present analysis both with and without the outlier
        → Never make a one-sided decision without flagging

RULE: NEVER remove an outlier without:
    (a) Documenting the value and its context
    (b) Assessing whether it is a legitimate business event
    (c) Evaluating the impact on the metric with and without it
    (d) Disclosing the decision to the analyst or consumer of the report
```

### DEFINITION ASSUMPTIONS
```
Many business terms have ambiguous definitions:

"ACTIVE USER":
    Could mean: logged in once in 30 days
    Or: made at least one meaningful action in 30 days
    Or: generated revenue in 30 days
    → Must pick one and document which was chosen

"REVENUE":
    Could mean: gross bookings
    Or: net revenue (after returns and discounts)
    Or: recognized revenue (by accounting period)
    → Affects period-over-period comparisons if definition changes

"CUSTOMER":
    Could mean: any account that ever paid
    Or: any account active in the period
    Or: only primary account holders (not sub-users)

RULE: For every domain term used in a metric, check whether an explicit canonical
      definition exists. If not, create one via Metric Definition Engine (A1) and
      register the choice here.
```

### EXCLUSION ASSUMPTIONS
```
Every exclusion removes data from the analysis population.
Exclusions must be:
    (a) Explicitly justified (not "we always exclude these")
    (b) Applied consistently across numerator and denominator
    (c) Assessed for materiality (what % of data is excluded?)

COMMON EXCLUSIONS:
    Internal/test accounts → usually safe if well-identified
    Cancelled orders → depends on metric (cancel before or after recognition?)
    Outlier transactions → see Outlier Assumptions above
    Incomplete periods → must define cutoff clearly
    Bot traffic → must define detection method

MATERIALITY THRESHOLD FOR DISCLOSURE:
    < 1% of data excluded → LOW (note in methodology)
    1–5% excluded → MEDIUM (disclose prominently)
    > 5% excluded → HIGH (must validate that exclusion doesn't bias the direction of results)
    > 20% excluded → CRITICAL (the population is materially different; may invalidate analysis)
```

---

## PROCEDURE

### STEP 1 — Detect Assumption Points
While profiling and cleaning data, flag every decision point:
```
PROFILING TRIGGERS:
    □ Any column with NULL count > 0
    □ Any column with values outside expected domain range
    □ Any metric term that has ambiguous business definition
    □ Any filter that removes > 0 rows
    □ Any imputation applied
    □ Any model choice made (linear vs. non-linear, etc.)
```

### STEP 2 — Classify Each Assumption
For each detected assumption point:
```
CLASSIFY:
    Category: [missingness | outlier | definition | exclusion | imputation | model | boundary]
    Materiality: LOW | MEDIUM | HIGH | CRITICAL
        LOW:      Affects < 0.1% of the metric value
        MEDIUM:   Affects 0.1% to 2% of the metric value
        HIGH:     Affects 2% to 10% of the metric value
        CRITICAL: Affects > 10% of the metric value or changes the directional conclusion
```

### STEP 3 — Assess Direction of Bias
```
For every assumption, determine if it causes upward or downward bias:

UPWARD BIAS: The assumption makes the metric look better than it truly is
    Example: Including partially completed orders in revenue
    → Revenue appears higher than if only shipped orders counted

DOWNWARD BIAS: The assumption makes the metric look worse
    Example: Excluding all orders above $1M as "outliers"
    → Revenue and growth rate are understated

NEUTRAL: Assumption has symmetric effects
    → e.g., replacing NULLs with median where MCAR is confirmed

UNKNOWN: Cannot determine direction without additional data
    → Flag explicitly; present sensitivity analysis if possible
```

### STEP 4 — Document in Assumption Registry
```
ASSUMPTION ENTRY:
    ID:          ASM-2024-001
    Category:    missingness
    Description: "Revenue NULL values in 'completed' orders treated as $0"
    Rationale:   "ETL team confirmed: NULLs in completed order revenue are caused by
                 a legacy system bug where $0 orders were not written to the revenue column.
                 They represent genuine $0 transactions."
    Alternative: "Could exclude these rows entirely. Would reduce order count by 1.2%."
    Materiality: MEDIUM (affects 1.2% of order count, 0% of revenue — $0 values)
    Bias:        NEUTRAL (adding $0 does not change revenue sum)
    Affected:    Order count, Conversion Rate denominator
    Validation:  Cross-check with billing system; $0 orders confirmed as trial conversions
    Disclosure:  YES — note in dashboard methodology
    Review:      If ETL bug is fixed, remove this assumption
```

### STEP 5 — Sensitivity Analysis for CRITICAL Assumptions
```
For any CRITICAL-materiality assumption:
    Run the analysis TWICE:
        (a) WITH the assumption applied
        (b) WITHOUT the assumption (or with the alternative)
    Report the delta:
        METRIC WITH ASSUMPTION: X
        METRIC WITHOUT ASSUMPTION: Y
        DELTA: (X - Y) / |Y| × 100%
        INTERPRETATION: "The assumption increases/decreases the metric by Z%"

IF delta changes the directional conclusion (from positive to negative growth, etc.):
    → This MUST be disclosed prominently in the report.
    → The consumer of the analysis must decide which assumption is correct.
    → Do NOT decide unilaterally for a CRITICAL materiality case.
```

---

## DECISION TREE FOR MISSING VALUE TREATMENT

```
Missing value detected
        │
        ▼
What type of column is this?
        │
  KEY COLUMN ▼          MEASURE ▼          DIMENSION ▼
Flag immediately.    What is business     What is business
Data quality issue.  meaning of missing?  meaning of missing?
Must not impute.          │                     │
                          ▼                     ▼
                     Determine               Was dimension
                     missingness             value applicable?
                     mechanism                   │
                     │         │            YES ▼     NO ▼
                    MCAR       MAR/MNAR    Impute    Flag as
                     │             │      mode /    "Not Applicable"
                     ▼             ▼      FK lookup
               Assess is:    Is zero the                │
               zero logical? right value?               ▼
               YES ▼  NO ▼   YES ▼  NO ▼          Document in
               Impute  Use    Impute  FLAG:          A5 Registry
               0       median 0       DO NOT
                              (doc in IMPUTE
                              A5)     → exclude
                                      and caveat
```

---

## MATHEMATICAL DEFINITIONS

**Materiality of an Assumption:**
```
Let M_with = metric value with assumption applied
Let M_without = metric value with assumption reversed or alternative applied

Materiality_pct = |M_with - M_without| / |M_without| × 100

< 0.1%  → LOW
0.1-2%  → MEDIUM
2-10%   → HIGH
> 10%   → CRITICAL
```

**Missingness Rate:**
```
Missing_pct = COUNT(NULL in column) / COUNT(all rows) × 100

> 0.1%  → Document in registry
> 5%    → Missingness pattern must be investigated
> 30%   → Column may be unusable; flag for stakeholder decision
```

---

## PRECONDITIONS
- [ ] Dataset profiling has been performed to detect NULLs and outliers.
- [ ] Domain expert or business logic is accessible to validate assumption choices.
- [ ] An analysis ID exists to associate assumption entries with a specific run.

## ASSUMPTIONS (Meta-Assumptions about this Engine)
- The analyst reviewing this registry has sufficient domain knowledge to assess materiality.
- "Stakeholder information" may require consultation outside the AI's context; flag and pause for input if critical assumptions cannot be assessed unilaterally.

---

## EDGE CASES

| Case | Problem | Resolution |
|------|---------|------------|
| Entire column is NULL | Column is unusable | Exclude from analysis; flag in methodology |
| Missing values in key join column | Cannot determine join behavior | Treat as separate population; do not join |
| Outlier is the most important data point | Removing it loses the critical insight | Never remove; annotate in visualization |
| Contradictory business rules | Different departments define "revenue" differently | Escalate; do not choose unilaterally |
| Historical assumption no longer valid | Old bug was fixed; assumption is stale | Review trigger fires; rerun analysis |
| MNAR detected but imputation is demanded | User insists on mean imputation | Produce result but prominently flag CRITICAL bias risk |

---

## FAILURE MODES

| Failure | Symptom | Detection | Severity |
|---------|---------|-----------|----------|
| Silent NULL → 0 substitution | Revenue understated or overstated | Compare raw vs. cleaned sums | CRITICAL |
| Outlier removed without documentation | Critical business event missing | Row count discrepancy | HIGH |
| MNAR treated as MCAR | Systematic bias in metric | Sensitivity analysis | CRITICAL |
| Inconsistent exclusions | Numerator/denominator use different populations | Population alignment check | HIGH |
| CRITICAL assumption undisclosed | Stakeholder misled | Disclosure field = NO for CRITICAL item | CRITICAL |
| Stale assumption still applied | Bug was fixed; assumption is now wrong | Review trigger not evaluated | HIGH |

---

## WORKED EXAMPLE

**Scenario:** E-commerce dataset. Revenue column has 8% NULL values.

```
STEP 1: Detected assumption point.
    Column: gross_revenue_usd
    NULL count: 8,240 of 103,000 rows (8%)

STEP 2: Classify.
    Category: missingness
    Initial materiality: UNKNOWN (depends on whether NULLs are $0 or unknown)

STEP 3: Investigate mechanism.
    Cross-reference with order_status:
        NULLs in revenue where order_status = 'pending': 6,000 rows
        NULLs in revenue where order_status = 'completed': 2,240 rows
        NULLs in revenue where order_status = 'cancelled': 0 rows

    COMPLETED orders with NULL revenue → MNAR (missing because of ETL failure)
    PENDING orders with NULL revenue → MAR (order exists but transaction not yet captured)

STEP 4: Document in registry.

    ASM-2024-007:
        Category: missingness
        Description: "2,240 completed orders have NULL revenue due to ETL gap (pre-2023 data migration)"
        Confirmed by: Data Engineering team
        Treatment: Exclude from revenue analysis; include in order count with note
        Materiality: HIGH — affects order count (2.2%) and revenue denominator
        Bias: DOWNWARD for order-volume metrics; NEUTRAL for revenue (these orders are not $0)
        Validation: ETL logs confirm missing revenue for these order_ids
        Disclosure: YES — note in dashboard footer

    ASM-2024-008:
        Category: missingness
        Description: "6,000 pending orders excluded from revenue; included in pipeline metrics"
        Treatment: Exclude from revenue; include in Pending Revenue metric
        Materiality: MEDIUM
        Bias: DOWNWARD for revenue; appropriately captured in pipeline
        Disclosure: YES — note in dashboard

STEP 5: Sensitivity analysis for HIGH-materiality ASM-2024-007.
    Revenue WITH exclusion: $8,200,000
    Revenue treating NULLs as $0: $8,200,000 (no change — these aren't $0, they're unknown)
    Revenue including estimated average ($85 per order): $8,390,400
    Delta: +2.3%
    CONCLUSION: Assumption is HIGH materiality and must be disclosed.
```

---

## ADVERSARIAL EXAMPLE

**Request:** "Just replace all the NULL revenues with the average so we can keep the sample size."

**Engine Response:**
```
BLOCKED — MNAR missingness detected. Mean imputation is inappropriate.

ISSUE: 2,240 completed orders have NULL revenue due to an ETL gap.
       These orders DO have non-zero revenue values — the values simply weren't captured.
       Substituting the mean would:
           (a) Assign incorrect revenue to orders whose actual values may differ significantly
           (b) Artificially inflate the sample's confidence (false precision)
           (c) Introduce a MEDIUM-HIGH bias upward or downward depending on whether
               the affected orders are larger or smaller than average

MCAR test: Revenue missingness is correlated with order creation date
           (pre-2023) → NOT MCAR.

CORRECT APPROACH:
    OPTION A: Exclude these orders from revenue analysis; note in methodology.
    OPTION B: Retrieve actual values from source billing system.
    OPTION C: If ETL gap affects less critical metrics, include with explicit "estimated" flag.

Proceeding with mean imputation is not authorized without stakeholder approval
and prominent bias disclosure.
```

---


## COUNTEREXAMPLES

**Counterexample A � Treating "Completed Orders with NULL Revenue" as MCAR:**
`
WRONG: NULL revenue is random ? impute with mean.
? Investigation reveals: ALL pre-2023 completed orders have NULL revenue (ETL gap).
? This is MNAR (correlated with order date) ? mean imputation biases results.
CORRECT: Exclude from revenue sum; flag in methodology; retrieve from billing system.
`

**Counterexample B � Not Disclosing a 25% Exclusion:**
`
WRONG: Exclude internal accounts (25% of dataset) silently, present analysis as complete.
? Results describe only 75% of the population. Conclusions may not generalize.
CORRECT: CRITICAL-materiality exclusion ? sensitivity analysis required ? disclosed
         prominently in report header: "Analysis excludes 25% internal accounts."
`
## VALIDATION RULES
1. Every data cleaning or imputation step must produce an Assumption Registry entry.
2. CRITICAL-materiality assumptions require sensitivity analysis before proceeding.
3. CRITICAL-materiality assumptions must be disclosed in any published report or dashboard.
4. Assumption entries must reference the specific metric(s) they affect.
5. Review triggers must be evaluated at the start of any re-run of the analysis.

## TEST CASES

| ID | Input | Expected | Pass Condition |
|----|-------|----------|----------------|
| ARE-001 | Revenue column has 8% NULLs | MNAR investigation triggered | Engine does not auto-impute |
| ARE-002 | User requests mean imputation for MNAR column | Blocked with explanation | Engine refuses and offers alternatives |
| ARE-003 | Transaction with value 100× average detected | Outlier classification required | Engine presents legitimate vs. error options |
| ARE-004 | Same metric defined differently in two places | Definition conflict flagged | Engine blocks; requires resolution |
| ARE-005 | Exclusion removes 25% of data | CRITICAL materiality | Engine requires sensitivity analysis |
| ARE-006 | CRITICAL assumption not disclosed in output | Publication blocked | Engine enforces disclosure flag |
| ARE-007 | Old stale assumption re-applied after data fix | Review trigger fires | Engine prompts re-assessment |

---

## AGENT EXECUTION INSTRUCTIONS
1. Scan for potential assumption points at the start of every data profiling step.
2. Never silently impute, exclude, or transform. Every such action requires a registry entry.
3. For MNAR-suspected missingness: STOP. Flag. Request business context before proceeding.
4. For CRITICAL-materiality assumptions: run sensitivity analysis. Do not proceed unilaterally.
5. Include the Assumption Registry ID in all provenance records (Engine A4).
6. Before publishing any dashboard or report, retrieve all CRITICAL and HIGH assumption entries and verify they are disclosed to the consumer.
