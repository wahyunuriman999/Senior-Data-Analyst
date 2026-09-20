# DESCRIPTIVE ANALYSIS ENGINE
**Phase B — Analytical Brain | Engine B1.1**
**Depth Contract: FULL (17/17 + Analytical Reasoning Contract 8/8)**

---

## PURPOSE
Provide a rigorous, structured characterization of a dataset before any inferential or predictive analysis. Descriptive analysis is NOT a preliminary step to be rushed — it is the primary mechanism for discovering data behavior, surfacing anomalies, validating assumptions, and forming precise hypotheses. Every analytical conclusion is only as valid as the descriptive understanding that precedes it.

**Default Prerequisite**: A descriptive pass is the default requirement before comparative, variance, or causal analysis. 
**Exceptions**: This step may be skipped IF (a) the dataset already has documented profiling, (b) prior analysis validated grain, quality, and assumptions, (c) the user explicitly requests analysis on a well-understood dataset, or (d) the descriptive step would not materially change method selection. If prerequisite evidence is missing, perform or request minimal profiling—do not automatically fail.

## SCOPE
- All numerical variables used in analysis.
- All categorical variables used as dimensions.
- All time-series variables used in trend analysis.
- All derived metrics after their Metric Contract (Foundation A1) has been completed.

---

## INPUTS
```
INPUT
├── dataset              : Profiled dataset with confirmed grain (Foundation A2)
├── metric_contracts     : One per measure (Foundation A1)
├── variable_list        : Specific variables to describe
├── analytical_question  : The business question this description supports
└── audience_context     : Executive, technical, or operational (affects depth and output format)
```

## OUTPUT CONTRACT
```
OUTPUT — DESCRIPTIVE PROFILE
├── variable_name        : Exact column name
├── data_type            : continuous | ordinal | nominal | boolean | datetime
├── n_total              : Total row count
├── n_valid              : Count of non-null values
├── n_missing            : Count of null values and % of total
├── distribution_shape   : symmetric | right-skewed | left-skewed | bimodal | uniform | unknown
├── central_tendency     : mean, median, mode (with applicability flag per measure type)
├── dispersion           : std_dev, variance, IQR, range, CV
├── tail_behavior        : min, max, p1, p5, p25, p50, p75, p95, p99
├── outlier_flags        : IQR-based and Z-score-based counts
├── temporal_pattern     : if datetime — trend direction, seasonality, cycle (if applicable)
├── cardinality          : for categoricals — distinct count, top-5 values with frequency
├── anomalies            : Specific values, patterns, or behaviors that require attention
└── interpretation_notes : Plain-language summary of the most important findings
```

---

## ANALYTICAL REASONING CONTRACT

### A. Question → Method Mapping
```
WHEN TO USE DESCRIPTIVE ANALYSIS:
    Q: "What does the data look like?"
    Q: "What is the typical value of X?"
    Q: "How much does X vary?"
    Q: "Are there outliers in X?"
    Q: "What is the distribution of X?"
    Q: "Is the data complete?"
    Q: "What patterns exist before we model?"

USE DESCRIPTIVE ANALYSIS FIRST for ANY of the above.
Do NOT skip to comparative or causal analysis without completing a descriptive pass.
```

### B. Method Selection Rationale
```
Descriptive statistics is selected because:
    - It makes NO distributional assumptions (non-parametric descriptives are always valid)
    - It surfaces data quality issues before they corrupt downstream analysis
    - It bounds the plausible range of results for all subsequent analyses
    - It identifies the appropriate follow-on analytical method (normal → parametric;
      skewed → non-parametric or transformation; bimodal → investigate subgroups)
```

### C. Alternative Methods
```
Descriptive analysis has no true alternative — it is a prerequisite.
However, the DEPTH of descriptive analysis can be adjusted:

    MINIMAL: n, mean, std_dev (acceptable only for well-understood, clean data)
    STANDARD: full profile including distribution shape and outlier flags
    DEEP: includes temporal patterns, cross-variable correlations, and subgroup profiles

If data is very large (> 1M rows), use SAMPLE-BASED profiling with documented sampling method.
```

### D. When NOT to Use / Misuse Prevention
```
DO NOT treat descriptive statistics as the END of analysis:
    Mean revenue = $120 is a DESCRIPTION, not an INSIGHT.
    Insight requires context: "Mean revenue = $120, down 15% vs Q3 2023, driven by [X segment]."

DO NOT report mean alone for skewed distributions:
    Income, transaction value, and time-to-event distributions are typically right-skewed.
    For right-skewed data: median is a more robust central tendency measure than mean.
    Report BOTH and explain the difference.

DO NOT assume completeness:
    NULL count = 0 does not mean data is complete.
    Check for: impossible values (age = -5), implausible values (revenue = $999,999,999),
    and structural NULLs (rows exist but all measures are 0 due to system errors).
```

### E. Interpretation Constraints
```
MEAN: Only valid central tendency for approximately symmetric distributions.
      Sensitive to extreme values; a single large outlier can shift mean dramatically.

STANDARD DEVIATION: Only meaningful for approximately normal distributions.
                    For skewed data, use IQR instead.

MODE: Only useful for categorical or discrete variables with meaningful repetition.
      For continuous data, mode is rarely informative without binning.

RANGE: Extremely sensitive to outliers; min and max are not robust.
       Prefer p5–p95 or p1–p99 range for practical spread.

COEFFICIENT OF VARIATION (CV = std_dev / mean):
    Only valid when mean > 0. Useful for comparing dispersion across variables with different scales.
    CV > 1.0 indicates high relative variability.
```

### F. Causal-vs-Associational Boundary
```
Descriptive analysis is PURELY OBSERVATIONAL.
It describes what IS in the data. It does NOT explain why.

FORBIDDEN INFERENCES:
    "Revenue is higher on weekends → weekend promotions cause higher revenue."
    ← Descriptive finding only. Causation requires experimental or quasi-experimental evidence.

    "Customers who use Feature X have higher retention → Feature X improves retention."
    ← Self-selection bias: Feature X users may be fundamentally different from non-users.

CORRECT INFERENCE:
    "Revenue tends to be higher on weekends (median: $X vs $Y on weekdays).
     This pattern warrants further investigation into causation."
```

### G. Uncertainty Handling
```
All descriptive statistics are point estimates from a sample (unless full population is analyzed).
For sample-based descriptive analysis, report:
    - Sample size
    - Sampling method
    - Confidence intervals for mean (if parametric assumptions hold): CI = x̄ ± t_{α/2} * (s/√n)
    - Bootstrap confidence intervals for median (preferred for non-normal distributions)

Acknowledge that descriptive statistics may be affected by:
    - Data collection period (shorter period → less stable estimates)
    - Missing data mechanism (MCAR/MAR/MNAR — see Foundation A5)
    - Outlier treatment decisions (see Foundation A5: Assumption Registry)
```

### H. Output Interpretation Contract
```
Every descriptive output must answer these questions explicitly:
    1. What is the central tendency of X, and is it a reliable estimate given the distribution shape?
    2. How spread out is X, and does this spread indicate natural variation or data quality issues?
    3. Are there values in X that are unusual and require investigation?
    4. Is the data complete enough for downstream analysis?
    5. What does the distribution shape imply about the appropriate analytical methods to use next?

The output is NOT a list of numbers.
It is a structured narrative that positions the data for the next analytical step.
```

---

## PROCEDURE

### STEP 1 — Validate Prerequisites
```
□ Metric Contract (A1) is complete for all measures being described.
□ Grain Contract (A2) is confirmed — know what each row represents.
□ Join Audit (A3) completed if data was joined.
□ Assumption Registry (A5) has flagged any known data quality issues.
```

### STEP 2 — Profile Data Completeness
```
For each variable:
    n_total   = SELECT COUNT(*) FROM dataset
    n_valid   = SELECT COUNT(variable) FROM dataset  [excludes NULLs]
    n_missing = n_total - n_valid
    pct_miss  = n_missing / n_total * 100

THRESHOLDS:
    pct_miss = 0%      → complete; proceed
    pct_miss < 5%      → investigate mechanism; proceed with flag
    pct_miss 5-20%     → investigate mechanism; consider impact on results
    pct_miss > 20%     → serious completeness issue; consult stakeholder before proceeding
    pct_miss = 100%    → column is empty; exclude from analysis
```

### STEP 3 — Compute Central Tendency
```
MEAN:
    x̄ = (1/n) * Σ xᵢ  for i = 1 to n
    Apply ONLY for continuous variables with approximately symmetric distribution.
    Check symmetry first (Step 4) before deciding if mean is appropriate.

MEDIAN:
    x_med = middle value when data is sorted.
    Robust to outliers. Preferred for right-skewed continuous variables.
    Always report for: revenue, income, transaction value, time duration.

MODE:
    Most frequent value (categorical) or most frequent bin (continuous with binning).
    Report ONLY when meaningful (e.g., categorical dimensions, discrete counts).
```

### STEP 4 — Assess Distribution Shape
```
VISUAL ASSESSMENT (fastest):
    Histogram: reveals shape, modality, and range
    Box plot: reveals quartiles, median, and outlier flags
    Density plot (KDE): smooth approximation of shape

QUANTITATIVE ASSESSMENT:
    Skewness: g₁ = [n / ((n-1)(n-2))] * Σ((xᵢ - x̄)/s)³
        g₁ ≈ 0:   symmetric
        g₁ > 1:   right-skewed (long right tail)
        g₁ < -1:  left-skewed (long left tail)

    Kurtosis: g₂ = [n(n+1) / ((n-1)(n-2)(n-3))] * Σ((xᵢ - x̄)/s)⁴ - 3(n-1)² / ((n-2)(n-3))
        g₂ ≈ 0:   mesokurtic (normal-like tails)
        g₂ > 0:   leptokurtic (heavier tails, more outliers than normal)
        g₂ < 0:   platykurtic (lighter tails)

DISTRIBUTION FLAGS:
    bimodal   → investigate subgroups; likely two distinct populations in one dataset
    uniform   → check for data artifact (common for ID columns, not measures)
    spike     → check for data truncation or rounding artifact
```

### STEP 5 — Compute Dispersion
```
STANDARD DEVIATION (parametric):
    s = √[ (1/(n-1)) * Σ(xᵢ - x̄)² ]
    Use for symmetric, approximately normal distributions.
    Divide by n-1 (Bessel's correction) for sample standard deviation.

IQR (non-parametric):
    IQR = Q3 - Q1  where Q1 = 25th percentile, Q3 = 75th percentile
    Use for skewed distributions or when outlier-robustness is needed.

COEFFICIENT OF VARIATION:
    CV = s / |x̄| * 100%
    Valid only when x̄ ≠ 0 and all values are positive or all negative.
    CV > 100%: very high relative dispersion; investigate.
```

### STEP 6 — Flag Outliers
```
IQR METHOD (non-parametric, robust):
    Lower fence = Q1 - 1.5 * IQR
    Upper fence = Q3 + 1.5 * IQR
    Flag: xᵢ < Lower fence OR xᵢ > Upper fence

Z-SCORE METHOD (parametric):
    z = (xᵢ - x̄) / s
    Flag: |z| > 3 (standard) or |z| > 2.5 (more sensitive)
    Limitation: not robust when the outlier itself inflates mean and std_dev.
    Use Modified Z-Score for robustness: M = 0.6745 * (xᵢ - median) / MAD
    where MAD = Median(|xᵢ - Median(x)|)

DOMAIN METHOD:
    Apply business rules: transaction amount > $1M for consumer product = flag
    Any value outside the physically or operationally possible range = flag

DECISION:
    Outliers are flagged, NOT automatically removed.
    Each flagged outlier must go through Foundation A5 (Assumption Registry).
```

### STEP 7 — Characterize Temporal Pattern (if datetime variable)
```
For time-series variables:
    Plot value over time (raw and moving average)
    Identify:
        Trend:      long-term upward/downward direction
        Seasonality: regular periodic pattern (weekly, monthly, quarterly)
        Cycle:      irregular multi-year fluctuation
        Irregularity: one-off events (spikes, drops)

    Decompose: Value = Trend + Seasonality + Cycle + Residual
    (or multiplicative: Value = Trend × Seasonality × Cycle × Residual)

    Flag: Step changes (regime shifts), missing periods, data gaps.
```

### STEP 8 — Profile Categorical Variables
```
For each categorical variable:
    distinct_count  = COUNT(DISTINCT value)
    top_values      = Top 5 values by frequency with count and percentage
    null_count      = Count of NULLs
    high_cardinality flag: distinct_count > 50 → may need grouping for visualization
```

### STEP 9 — Synthesize and Interpret
```
Produce a structured summary:
    1. State what the central tendency is and whether it is a reliable estimate.
    2. Characterize spread relative to the business context (is CV of 30% normal for this metric?).
    3. List any anomalies that require investigation before downstream analysis.
    4. State what distribution shape implies about appropriate methods.
    5. Confirm data completeness or flag incompleteness with severity.
```

---

## DECISION TREE
```
Variable received
        │
        ▼
What is the data type?
        │
CONTINUOUS ──────────────────────────────────────────────────┐
        │                                                      │
Compute n, n_valid, pct_missing                               │
        │                                                      │
pct_missing > 20%? → Flag HIGH; consult A5                    │
        │                                                      │
Compute mean, median, mode, std, IQR, percentiles             │
        │                                                      │
Assess skewness:                                              │
g₁ ≈ 0 → symmetric → mean is reliable                        │
g₁ > 1 → right-skewed → prefer median; log-transform?        │
g₁ < -1→ left-skewed → prefer median; investigate floor?     │
        │                                                      │
bimodal? → investigate subgroups before aggregating           │
        │                                                      │
Flag outliers (IQR + domain method) → log in A5              │
        │                                                      │
Temporal? → Run Step 7 (trend, seasonality, cycle)           │
        │                                                      │
Synthesize (Step 9) ─────────────────────────────────────────┤
                                                              │
CATEGORICAL ─────────────────────────────────────────────────┤
        │                                                      │
Compute n, n_valid, distinct_count, top-5 values             │
        │                                                      │
distinct_count > 50? → Flag high cardinality                 │
        │                                                      │
Synthesize (Step 9) ─────────────────────────────────────────┘
                                    │
                                    ▼
              DESCRIPTIVE PROFILE COMPLETE
                    → Proceed to:
                    [Comparative] [Variance] [Correlation]
                    as indicated by analytical question
```

---

## MATHEMATICAL DEFINITIONS

**Sample Mean:**
$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

**Sample Variance (Bessel-corrected):**
$$s^2 = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2$$

**Sample Skewness (adjusted Fisher-Pearson):**
$$g_1 = \frac{n}{(n-1)(n-2)} \sum_{i=1}^{n} \left(\frac{x_i - \bar{x}}{s}\right)^3$$

**Coefficient of Variation:**
$$CV = \frac{s}{|\bar{x}|} \times 100\%$$
Valid only when $\bar{x} \neq 0$.

**Modified Z-Score (outlier detection robust to own outliers):**
$$M_i = \frac{0.6745 \times (x_i - \tilde{x})}{\text{MAD}}$$
where $\tilde{x}$ = median and $\text{MAD} = \text{Median}(|x_i - \tilde{x}|)$.

---

## PRECONDITIONS
- [ ] Metric Contracts (A1) complete for all variables being described.
- [ ] Grain Contract (A2) confirmed — interpretation of n depends on what one row means.
- [ ] Data has been loaded into a profilable environment.
- [ ] Analytical question is defined (descriptive analysis serves a purpose; it is not data exploration for its own sake).

## ASSUMPTIONS
- Sample is representative of the population being described (document if not).
- Temporal variables use consistent timezone and event date (not processing date) unless documented otherwise.
- Missing values are not selectively distributed in a way that biases the profile (verify with Foundation A5).

---

## EDGE CASES

| Case | Problem | Resolution |
|------|---------|------------|
| All values identical | std_dev = 0; CV undefined | Flag as zero-variance; note in profile; do not use for correlation or regression |
| Single unique value in categorical | 100% concentration | Flag; dimension may be useless for segmentation |
| Bimodal distribution | Single mean is misleading | Profile each mode separately; investigate subgroups |
| Negative values in ratio metric | May indicate returns, adjustments | Do not apply log transformation; investigate business meaning |
| Infinite values (Inf) | Mean/std computation fails | Detect and treat as outliers; document in A5 |
| All values are NULL | Column unusable | Exclude; document in A5 |
| Duplicate rows inflating counts | Grain violation | Halt; fix grain first (Foundation A2) |
| Datetime with timezone mix | Incorrect temporal grouping | Normalize to UTC before any temporal profiling |

---

## FAILURE MODES

| Failure | Symptom | Detection | Severity |
|---------|---------|-----------|----------|
| Mean reported for skewed distribution | Misleading central tendency | g₁ > 1 not flagged | HIGH |
| Outliers removed without documentation | Distorted distribution profile | A5 entry missing | HIGH |
| NULL count not reported | Completeness unknown | pct_missing not computed | HIGH |
| Bimodal distribution treated as unimodal | Subpopulations invisible | No modality test | HIGH |
| CV computed with x̄ near 0 | Infinite or meaningless CV | No x̄ ≠ 0 check | MEDIUM |
| Descriptive analysis treated as inferential | Causal claims made | Interpretation violation (F boundary) | CRITICAL |
| Distribution shape assumed without verification | Wrong follow-on method chosen | No skewness/kurtosis computed | HIGH |

---

## COUNTEREXAMPLES

**Counterexample A — Mean as summary for revenue:**
```
Revenue distribution: right-skewed (many small transactions, few large ones).
    Mean revenue = $850 (inflated by 5 large enterprise deals).
    Median revenue = $120 (representative of typical transaction).

WRONG: "Average customer spends $850."
RIGHT: "Typical customer (median) spends $120; mean is $850 due to right-skew
        driven by enterprise transactions. The two populations should be analyzed separately."
```

**Counterexample B — Ignoring bimodality:**
```
User session duration: bimodal at 1-2 minutes and 15-20 minutes.
    Mean = 9 minutes (no one actually spends this amount of time).

WRONG: Report mean = 9 minutes.
RIGHT: Detect bimodality. Segment into two groups:
       quick-exit users (< 5 min) and engaged users (> 5 min).
       Describe each group separately.
```

---

## WORKED EXAMPLE

**Dataset:** `monthly_orders` — 50,000 rows, one row per order.
**Question:** "Describe the distribution of order value."

```
STEP 2: Completeness
    n_total = 50,000
    n_valid (order_value) = 49,750
    pct_missing = 0.5% → flag MEDIUM; log in A5

STEP 3: Central Tendency
    mean = $312.50
    median = $185.00
    mode = $19.99 (most common price point — likely a base plan)

    Mean >> Median → right-skewed distribution

STEP 4: Distribution Shape
    g₁ = 2.34 → strongly right-skewed
    g₂ = 8.7  → leptokurtic (heavy right tail)
    → Mean is not a reliable central tendency; use median for reporting.

STEP 5: Dispersion
    std_dev = $520.10 (large relative to mean)
    IQR = Q3 - Q1 = $380 - $75 = $305
    CV = 520.10 / 312.50 = 166% → very high relative variability

STEP 6: Outliers
    IQR fence upper = $380 + 1.5*305 = $837.50
    Flagged above fence: 1,243 orders (2.5%)
    Max value: $28,500 → investigate (enterprise deal? data error?)
    Log flagged values in A5.

STEP 9: Interpretation
    "Order value is strongly right-skewed. The typical order (median = $185)
    is far below the mean ($312.50), which is inflated by a long right tail of
    large-value orders. 2.5% of orders exceed $837.50; the largest single order
    is $28,500 — requires classification as enterprise or investigation as error.
    Median is the recommended central tendency for business reporting.
    Downstream analysis (segmentation, regression) should consider log-transformation
    or separate treatment of enterprise orders."
```

---

## ADVERSARIAL EXAMPLE

**Request:** "Quick summary: revenue average is $312.50. Can we say our customers typically spend $312?"

**Engine Response:**
```
BLOCKED — Mean is not appropriate central tendency for this distribution.

ISSUE: g₁ = 2.34 → strongly right-skewed distribution.
       Mean ($312.50) is inflated by a long right tail of high-value orders.
       Median ($185.00) is the correct representation of typical spend.

REPORTING:
    WRONG: "Customers typically spend $312."
    RIGHT: "Typical customer spends $185 (median).
            Mean is $312 due to right-skew from large enterprise orders.
            Reporting mean alone would misrepresent typical customer behavior."

ACTION: Use median for customer behavior reporting.
        Flag mean vs. median discrepancy in the dashboard methodology note.
```

---

## VALIDATION RULES
1. Descriptive profile must be completed before any comparative or inferential analysis.
2. For skewed distributions (|g₁| > 1): median must be reported alongside mean.
3. All flagged outliers must have a corresponding A5 entry.
4. pct_missing must be computed and reported for every variable.
5. Bimodal distributions must be investigated before reporting any aggregate statistics.
6. Causal language is forbidden in descriptive output (use "associated with," "tends to," "patterns suggest").

## TEST CASES

| ID | Input | Expected Output | Pass Condition |
|----|-------|----------------|----------------|
| DES-001 | Revenue with g₁=2.3 | Mean AND median both reported; mean flagged as unreliable central tendency | Engine does not report mean alone |
| DES-002 | 25% NULL revenue | HIGH completeness flag; A5 entry required | Engine does not proceed without flag |
| DES-003 | Bimodal session duration | Two modes identified; single mean blocked as summary | Engine reports both modes, recommends segmentation |
| DES-004 | User requests "customers spend $312 on average" | Engine flags mean-for-skewed-data error | Correction provided before any downstream use |
| DES-005 | All values identical | Zero variance flagged; CV undefined | Engine reports and excludes from correlation/regression |
| DES-006 | Causal claim from descriptive output | Blocked | Engine replaces with observational language |
| DES-007 | Outlier 100× above p99 | Flagged via both IQR and domain method; A5 entry required | Engine does not auto-remove |

---

## AGENT EXECUTION INSTRUCTIONS
1. Execute this engine for EVERY variable before any downstream analytical method.
2. Never report mean as the sole central tendency for skewed distributions.
3. Never make causal claims from descriptive output — flag any causal language in draft output.
4. Document every outlier flag in Foundation A5 before proceeding.
5. State explicitly what the distribution shape implies for the next analytical method:
   - Symmetric → parametric methods may be appropriate (verify assumptions)
   - Right-skewed → consider log transformation or non-parametric methods
   - Bimodal → segment before aggregating; investigate subpopulations
6. Include n, n_valid, pct_missing in every output — never omit completeness information.
