# COMPARATIVE ANALYSIS ENGINE
**Phase B — Analytical Brain | Engine B1.2**
**Depth Contract: FULL (17/17 + Analytical Reasoning Contract 8/8)**

---

## PURPOSE
Determine whether meaningful differences exist between two or more groups, time periods, or conditions — and quantify the magnitude of those differences. Comparative analysis answers "Is A different from B, and by how much?" It is the foundation of A/B reasoning, period-over-period analysis, and segment performance evaluation. This engine enforces rigorous method selection, prevents false comparisons, and requires both statistical and practical significance assessment.

**Hard rule**: A difference is only meaningful when it is (a) statistically significant given sample size, AND (b) practically significant given business context. Statistical significance without practical significance is noise. Practical significance without statistical rigor is storytelling.

## SCOPE
- Two-group comparisons (A vs. B, pre vs. post, treatment vs. control).
- Multi-group comparisons (region A vs. B vs. C, cohort 1 vs. 2 vs. 3).
- Period-over-period comparisons (MoM, QoQ, YoY).
- Benchmark comparisons (actuals vs. target, actuals vs. industry benchmark).

---

## INPUTS
```
INPUT
├── group_a              : Dataset or aggregated metric for group A (with grain and metric contracts)
├── group_b              : Dataset or aggregated metric for group B
├── comparison_type      : (two_group | multi_group | period_over_period | vs_benchmark)
├── metric_contract      : From Foundation A1 — must be identical definition for both groups
├── sample_sizes         : n_A, n_B (required for significance testing)
├── significance_level   : alpha (default 0.05; adjust for multiple comparisons)
└── practical_threshold  : Minimum meaningful difference defined by business context
```

## OUTPUT CONTRACT
```
OUTPUT — COMPARISON REPORT
├── comparison_label     : "Group A vs Group B on [Metric], [Period]"
├── metric_a             : Value, n, std_dev for Group A
├── metric_b             : Value, n, std_dev for Group B
├── absolute_difference  : metric_a - metric_b (with direction)
├── relative_difference  : (metric_a - metric_b) / |metric_b| * 100%
├── method_used          : Statistical test applied
├── test_statistic       : t, z, chi², F, U, etc.
├── p_value              : With interpretation
├── confidence_interval  : 95% CI of the difference
├── effect_size          : Cohen's d / eta² / Cramér's V (as applicable)
├── practical_significance : Difference vs. practical_threshold
├── statistical_significance : p < alpha AND CI excludes 0
├── conclusion           : Combined assessment (both statistical and practical)
└── caution_flags        : Assumption violations, multiple comparison issues, etc.
```

---

## ANALYTICAL REASONING CONTRACT

### A. Question → Method Mapping
```
Q: "Is revenue higher in Region A than Region B?"
    → Two-group comparison of continuous metric

Q: "Did conversion rate improve after the feature launch?"
    → Period-over-period comparison (pre/post)
    → If randomized: two-proportion z-test
    → If observational: difference-in-differences or pre-post with caveats

Q: "Which of our 5 segments has the highest LTV?"
    → Multi-group comparison → ANOVA or Kruskal-Wallis

Q: "Are we hitting our revenue target?"
    → vs-benchmark comparison (point estimate vs fixed reference)

Q: "Do churned users differ from retained users in usage frequency?"
    → Two-group comparison of count/rate variable
```

### B. Method Selection Rationale
```
DECISION FRAMEWORK — select method based on:

    Data type of metric:
        Continuous (revenue, time, count) → t-test family or Mann-Whitney
        Proportion/rate (conversion %, churn %) → z-test for proportions
        Ordinal (NPS, satisfaction score) → Mann-Whitney U
        Categorical (distribution of plan types) → Chi-square

    Number of groups:
        2 groups → t-test / Mann-Whitney / z-test / Fisher's exact
        ≥ 3 groups → ANOVA (parametric) or Kruskal-Wallis (non-parametric)
        → follow with post-hoc tests if significant (Tukey, Bonferroni, Dunn)

    Distribution of the metric:
        Approximately normal AND n > 30 per group → parametric (t-test)
        Non-normal OR small n → non-parametric (Mann-Whitney U)
        → Shapiro-Wilk test for normality when n < 50
        → Anderson-Darling or D'Agostino-Pearson for larger samples

    Variance equality:
        Levene's test for equality of variances
        Equal variances → Student's t-test
        Unequal variances (p < 0.05 on Levene's) → Welch's t-test (default to Welch's)

    Sample type:
        Independent samples → independent t-test / Mann-Whitney
        Paired samples (same entity before/after) → paired t-test / Wilcoxon signed-rank
```

### C. Alternative Methods
```
PRIMARY METHOD COMPARISON:

Scenario: Compare mean revenue, two regions, n > 30, approximately normal:
    PRIMARY: Welch's t-test (does not assume equal variances)
    ALTERNATIVE: Permutation/bootstrap test (no distributional assumption)
    AVOID: Student's t-test (assumes equal variance — verify first)

Scenario: Compare conversion rates (proportions):
    PRIMARY: Two-proportion z-test
    ALTERNATIVE: Fisher's exact test (preferred when n < 30 per group)
    AVOID: t-test on 0/1 binary variable (technically works but two-proportion z-test is cleaner)

Scenario: Compare NPS scores (ordinal):
    PRIMARY: Mann-Whitney U test (does not assume normality)
    AVOID: t-test (NPS is ordinal; normality assumption invalid)
```

### D. When NOT to Use / Misuse Prevention
```
DO NOT compare metrics with different definitions:
    Region A: Revenue = gross bookings
    Region B: Revenue = net revenue (after returns)
    → Incomparable. Enforce identical Metric Contract (Foundation A1) before comparing.

DO NOT compare across different time periods without controlling for seasonality:
    "Q1 revenue > Q4 revenue → growing."
    → Q1 and Q4 have different seasonal baselines.
    → Use YoY comparison or seasonally adjusted figures.

DO NOT use t-test on proportion data when n is very small:
    n < 30 per group and proportion data → use Fisher's exact test.

DO NOT report p-value without effect size:
    With n = 1,000,000, a difference of $0.01 will be statistically significant.
    $0.01 difference in revenue is not practically meaningful.
    ALWAYS report effect size alongside p-value.

DO NOT claim causal direction from observational comparison:
    "Customers using Feature X have 30% higher LTV."
    → This is a descriptive comparison. Feature X may not CAUSE higher LTV.
    → Self-selection: high-value customers may be more likely to use Feature X.
```

### E. Interpretation Constraints
```
STATISTICAL SIGNIFICANCE (p < alpha):
    Means: if the null hypothesis (no difference) were true, we would observe a
           difference this extreme by chance with probability p.
    Does NOT mean: the difference is large, important, or real in a practical sense.
    Does NOT mean: the null hypothesis is false.

PRACTICAL SIGNIFICANCE (effect size):
    Cohen's d:
        d < 0.2: trivial effect
        0.2 ≤ d < 0.5: small effect
        0.5 ≤ d < 0.8: medium effect
        d ≥ 0.8: large effect

CONFIDENCE INTERVAL:
    The 95% CI does NOT mean "95% probability the true value is in this range."
    It means: if we repeated this analysis 100 times, ~95 of the CIs would contain
    the true population parameter.

MULTIPLE COMPARISONS:
    If 20 tests are run at α=0.05, we expect 1 false positive by chance alone.
    Apply Bonferroni correction: α_adjusted = α / number_of_tests
    Or use Benjamini-Hochberg FDR control for large test counts.
```

### F. Causal-vs-Associational Boundary
```
COMPARATIVE ANALYSIS IS OBSERVATIONAL unless:
    (a) Random assignment to groups (A/B test)
    (b) Natural experiment with credible exogenous variation
    (c) Quasi-experimental design (DID, RDD, IV) with proper controls

FOR OBSERVATIONAL COMPARISON:
    FORBIDDEN: "Feature X caused a 30% LTV increase."
    REQUIRED:  "Users of Feature X show 30% higher LTV compared to non-users.
                This association is subject to self-selection bias and confounding.
                Causal attribution requires controlled experimental evidence."

FOR RANDOMIZED A/B TEST:
    Causal language is permitted ONLY when:
        - Randomization was verified (balance check on pre-treatment covariates)
        - No interference between groups (SUTVA)
        - No differential attrition
        - No peeking / p-hacking
```

### G. Uncertainty Handling
```
Report ALL of these — not just p-value:
    1. Point estimate of difference
    2. 95% CI of difference (directional uncertainty)
    3. Effect size with interpretation
    4. p-value with alpha correction if applicable
    5. Power analysis: was the study adequately powered to detect the practical threshold?
       Power = P(reject H₀ | H₁ is true)
       Minimum acceptable power: 0.80
       If power < 0.80: interpret non-significant results with extreme caution —
       absence of evidence is not evidence of absence.
```

### H. Output Interpretation Contract
```
A complete comparison report answers:
    1. What is the difference in absolute and relative terms?
    2. Is the difference statistically significant? (p, CI)
    3. Is the difference practically meaningful? (effect size vs. business threshold)
    4. What method was used and why is it appropriate here?
    5. What assumptions were made and were they verified?
    6. If observational: what confounders could explain this difference?
    7. What is the recommended action based on both statistical and practical significance?
```

---

## PROCEDURE

### STEP 1 — Validate Metric Contract Alignment
```
Confirm that Group A and Group B use IDENTICAL metric definitions.
    □ Same numerator formula
    □ Same denominator formula
    □ Same population filter
    □ Same time window boundaries
    □ Same exclusions
If any definition differs → comparison is INVALID. Resolve before proceeding.
```

### STEP 2 — Compute Descriptive Statistics Per Group
```
For each group, complete Descriptive Analysis Engine (B1.1):
    n, mean, median, std_dev, IQR, distribution shape, outlier flags
These are required inputs to method selection in Step 3.
```

### STEP 3 — Select Comparison Method
```
Apply the decision framework from Section B (Method Selection Rationale).
Document:
    - Why this method was selected
    - What assumptions it makes
    - How those assumptions were verified
```

### STEP 4 — Run Significance Test
```
INDEPENDENT TWO-GROUP, CONTINUOUS, NORMAL (Welch's t-test):
    t = (x̄_A - x̄_B) / √(s²_A/n_A + s²_B/n_B)
    df = (s²_A/n_A + s²_B/n_B)² / [(s²_A/n_A)²/(n_A-1) + (s²_B/n_B)²/(n_B-1)]
    p = 2 * P(T > |t|) for two-tailed test

TWO PROPORTIONS (z-test):
    p̂_A = successes_A / n_A
    p̂_B = successes_B / n_B
    p̂_pool = (successes_A + successes_B) / (n_A + n_B)
    z = (p̂_A - p̂_B) / √(p̂_pool * (1 - p̂_pool) * (1/n_A + 1/n_B))

NON-PARAMETRIC (Mann-Whitney U):
    U = n_A * n_B + n_A*(n_A+1)/2 - R_A
    where R_A = sum of ranks in Group A
    Convert U to z for large samples: z = (U - n_A*n_B/2) / √(n_A*n_B*(n_A+n_B+1)/12)

MULTI-GROUP (one-way ANOVA):
    F = MS_between / MS_within
    MS_between = SS_between / (k-1)
    MS_within  = SS_within / (N-k)
    where k = number of groups, N = total sample
    If F significant → run post-hoc tests (Tukey HSD for equal n, Games-Howell for unequal)
```

### STEP 5 — Compute Effect Size
```
COHEN'S d (two continuous groups):
    d = (x̄_A - x̄_B) / s_pooled
    s_pooled = √[ ((n_A-1)*s²_A + (n_B-1)*s²_B) / (n_A + n_B - 2) ]

ETA-SQUARED (ANOVA):
    η² = SS_between / SS_total
    η² = 0.01: small; 0.06: medium; 0.14: large

CRAMÉR'S V (categorical comparison):
    V = √(χ² / (n * (min(r,c) - 1)))
    where r = rows, c = columns, n = sample size
```

### STEP 6 — Apply Multiple Comparison Correction (if applicable)
```
IF running k > 1 simultaneous comparisons:
    Bonferroni: α_i = α / k (conservative; controls family-wise error rate)
    Benjamini-Hochberg: controls false discovery rate (preferred for large test counts)
    Document: which correction was applied and why.
```

### STEP 7 — Assess Practical Significance
```
Compare effect size to the pre-defined practical threshold:
    Does the difference exceed the minimum meaningful difference for this business?
    Example: "A 0.1% conversion rate improvement = $2M/year → practically meaningful."
    Example: "A 0.01% CTR difference = $1,000/year → not worth acting on."
```

### STEP 8 — Produce Comparison Report (per Output Contract)

---

## DECISION TREE
```
Comparison requested
        │
        ▼
Are metric definitions IDENTICAL for both groups? (Step 1)
        │
       NO → HALT: Enforce metric contract alignment
        │
       YES
        ▼
Run descriptive profile on each group (Step 2)
        │
        ▼
Select method (Step 3):
    Continuous + normal + n>30? → Welch's t-test
    Continuous + non-normal OR small n? → Mann-Whitney U
    Proportion? → z-test (n>30) or Fisher's (n<30)
    Ordinal? → Mann-Whitney U
    Categorical distribution? → Chi-square
    3+ groups? → ANOVA or Kruskal-Wallis
        │
        ▼
Run test → compute t/z/U/F + p-value + CI (Step 4)
        │
        ▼
Compute effect size (Step 5)
        │
        ▼
Multiple comparisons? → Apply correction (Step 6)
        │
        ▼
p < α AND CI excludes 0?
    YES → Statistically significant
    NO  → Not statistically significant
            Check power: was study powered to detect practical threshold?
        │
        ▼
Effect size ≥ practical threshold?
    YES → Practically significant
    NO  → Practically trivial (even if statistically significant)
        │
        ▼
Both? → Report as meaningful difference
Stat only? → "Detectable but trivial"
Practical only? → "Meaningful if real, but insufficient power to confirm"
Neither? → "No meaningful difference detected"
        │
        ▼
Observational data? → Flag confounders, forbid causal language
        │
        ▼
Output Comparison Report (Step 8)
```

---

## MATHEMATICAL DEFINITIONS

**Welch's t-test statistic:**
$$t = \frac{\bar{x}_A - \bar{x}_B}{\sqrt{\frac{s^2_A}{n_A} + \frac{s^2_B}{n_B}}}$$

**Welch-Satterthwaite degrees of freedom:**
$$df = \frac{\left(\frac{s^2_A}{n_A} + \frac{s^2_B}{n_B}\right)^2}{\frac{(s^2_A/n_A)^2}{n_A-1} + \frac{(s^2_B/n_B)^2}{n_B-1}}$$

**Cohen's d (pooled):**
$$d = \frac{\bar{x}_A - \bar{x}_B}{s_{pooled}}, \quad s_{pooled} = \sqrt{\frac{(n_A-1)s^2_A + (n_B-1)s^2_B}{n_A + n_B - 2}}$$

**95% Confidence Interval for difference in means:**
$$CI = (\bar{x}_A - \bar{x}_B) \pm t_{df,\,0.025} \sqrt{\frac{s^2_A}{n_A} + \frac{s^2_B}{n_B}}$$

**Two-proportion z-test:**
$$z = \frac{\hat{p}_A - \hat{p}_B}{\sqrt{\hat{p}_{pool}(1-\hat{p}_{pool})\left(\frac{1}{n_A}+\frac{1}{n_B}\right)}}$$

---

## PRECONDITIONS
- [ ] Metric Contracts are identical for both groups (Foundation A1).
- [ ] Grain contracts confirmed for both datasets (Foundation A2).
- [ ] Descriptive profiles completed for both groups (Engine B1.1).
- [ ] Practical significance threshold defined before testing (not after seeing results).
- [ ] Sample sizes are known (n_A, n_B).

## ASSUMPTIONS
- For Welch's t-test: observations are independent within and between groups.
- For z-test on proportions: np ≥ 10 and n(1-p) ≥ 10 for both groups.
- For Mann-Whitney: observations are independent; the two distributions have the same shape (for location shift interpretation).
- For ANOVA: independence, normality within groups (or n > 30 by CLT), homoscedasticity (verify via Levene's test; if violated, use Welch's ANOVA).

---

## EDGE CASES

| Case | Problem | Resolution |
|------|---------|------------|
| Group sizes very unequal (n_A = 10, n_B = 10,000) | Power imbalance; CI driven by smaller group | Use Welch's t (handles unequal n); report CIs; power analysis |
| Metric definition differs between groups | Incomparable comparison | Halt; enforce identical metric contract |
| Period-over-period without seasonality control | False trend | Use YoY or seasonally-adjusted baseline |
| Same entity appears in both groups | Violates independence | Switch to paired test; investigate data design |
| Multiple comparisons not corrected | False positives | Apply Bonferroni or BH correction |
| Non-significant result, low power | "No difference" claimed incorrectly | Report power; "insufficient evidence" not "no difference" |
| Outliers driving the comparison result | Effect is driven by extreme values | Report comparison with and without outliers |

---

## FAILURE MODES

| Failure | Symptom | Detection | Severity |
|---------|---------|-----------|----------|
| t-test on non-normal small sample | False significant result | Normality not checked | HIGH |
| p-value reported without effect size | Trivial difference appears important | Effect size absent | HIGH |
| Causal claim from observational comparison | Misleading conclusion | No randomization noted | CRITICAL |
| Multiple comparisons not corrected | Inflated false positive rate | k > 1 tests without correction | HIGH |
| Metric definitions differ between groups | Invalid comparison | Contract alignment not checked | CRITICAL |
| Non-significant result reported as "no effect" | Power not assessed | Power analysis missing | HIGH |
| Period comparison without seasonal adjustment | False MoM/QoQ trend | No seasonality control | HIGH |

---

## COUNTEREXAMPLES

**Counterexample A — Statistical significance without practical significance:**
```
n_A = 500,000, n_B = 500,000
Conversion rate A = 4.00%, B = 4.01%
p-value = 0.001 (highly significant)
Absolute difference = 0.01 percentage points = $1,000/year revenue impact

WRONG: "Conversion rate significantly higher in Group A. Implement Group A's experience."
RIGHT: "Difference is statistically significant but practically trivial (0.01 pp = $1,000/year).
        Threshold for action is 0.5 pp ($50,000/year). No action warranted."
```

**Counterexample B — Observational comparison with causal framing:**
```
Users with Feature X: LTV = $1,200
Users without Feature X: LTV = $800
Difference: $400 (50%, p < 0.001, d = 0.8)

WRONG: "Feature X increases LTV by $400. Roll out to all users."
RIGHT: "Users with Feature X show $400 higher LTV. This is an observational finding.
        Feature X adoption is correlated with user type (enterprise vs. SMB).
        The difference may reflect segment composition, not Feature X's causal impact.
        Causal evidence requires a randomized rollout."
```

---

## WORKED EXAMPLE

**Question:** "Did conversion rate improve in North America after launching the new onboarding flow (Q3 vs Q2 2024)?"

```
STEP 1: Metric Contract — Conversion Rate is identically defined for both periods (Foundation A1 verified).

STEP 2: Descriptive Profile
    Q2: n=42,000, conversions=1,680, p̂_Q2 = 4.0%
    Q3: n=45,000, conversions=2,025, p̂_Q3 = 4.5%

STEP 3: Method — Two proportions, large n → two-proportion z-test

STEP 4: z-test
    p̂_pool = (1680+2025)/(42000+45000) = 3705/87000 = 0.04259
    z = (0.045 - 0.040) / √(0.04259*0.95741*(1/42000+1/45000))
    z = 0.005 / √(0.04259*0.95741*0.0000451)
    z = 0.005 / 0.000963 = 5.19
    p < 0.0001 (two-tailed)
    95% CI for difference: (0.005 ± 1.96 * 0.000963) = (0.003, 0.007)

STEP 5: Effect size
    h = 2*arcsin(√0.045) - 2*arcsin(√0.040) = 0.024
    Cohen's h = 0.024 → small effect

STEP 6: Single comparison — no correction needed.

STEP 7: Practical significance
    Business threshold: 0.5 pp improvement = $250,000 revenue impact
    Observed difference: 0.5 pp → meets practical threshold

STEP 8: Report
    "Conversion rate increased from 4.0% (Q2) to 4.5% (Q3) in North America.
    Difference = +0.5 pp (95% CI: 0.3pp to 0.7pp), p < 0.0001.
    Effect size (Cohen's h = 0.024) is small in absolute terms, but meets the
    practical significance threshold of 0.5 pp ($250,000 incremental revenue).

    CAUTION: This is a period-over-period observational comparison.
    The new onboarding flow launched at the same time as a seasonal marketing
    push in July. Both factors could explain the improvement. Causal attribution
    to the onboarding flow alone requires controlled A/B test evidence."
```

---

## ADVERSARIAL EXAMPLE

**Request:** "We ran 50 different comparisons between customer segments. Segment 12 has p=0.03. Can we report it's significantly different?"

**Engine Response:**
```
BLOCKED — Multiple comparison correction required.

ISSUE: 50 simultaneous tests at α=0.05 → expected ~2.5 false positives by chance alone.
       p=0.03 without correction may be a false positive.

CORRECTION REQUIRED:
    Bonferroni: α_adjusted = 0.05/50 = 0.001
    Segment 12 with p=0.03 → NOT significant after Bonferroni correction.

    Benjamini-Hochberg (FDR): Sort p-values, apply step-up procedure.
    If Segment 12 p-value is not among top BH-significant results → not reportable.

ACTION: Apply multiple comparison correction to all 50 tests.
        Report only those surviving correction. Document the correction method used.
```

---

## VALIDATION RULES
1. Metric Contracts must be verified as identical before any comparison.
2. Method selection must be justified — document why the chosen test is appropriate.
3. Effect size must be reported alongside p-value for every comparison.
4. Multiple comparison correction must be applied when k > 1 test is run.
5. Causal language is forbidden for observational comparisons.
6. Non-significant results must report statistical power before concluding "no difference."

## TEST CASES

| ID | Input | Expected | Pass Condition |
|----|-------|----------|----------------|
| CMP-001 | Groups with different metric definitions | HALT | Engine blocks before any test |
| CMP-002 | Large n, tiny difference, p<0.05 | Effect size flagged as trivial | Both p and d reported |
| CMP-003 | Non-normal distribution, small n | Mann-Whitney selected | Normality tested first |
| CMP-004 | 50 simultaneous tests, one p=0.03 | Bonferroni correction applied | Not reported as significant |
| CMP-005 | Observational comparison with causal framing | Causal language blocked | Observational caveat required |
| CMP-006 | Non-significant result, power = 0.4 | "Insufficient power" reported | Not reported as "no effect" |
| CMP-007 | Paired data treated as independent | Paired test recommended | Independence assumption flagged |

---

## AGENT EXECUTION INSTRUCTIONS
1. Verify identical metric contracts before any comparison — no exceptions.
2. Always complete a descriptive profile on each group first (Engine B1.1).
3. Document method selection rationale — do not default to t-test without checking assumptions.
4. Always report: absolute difference, relative difference, CI, p-value, effect size, practical significance.
5. When comparing periods: check for seasonality before attributing change to an intervention.
6. For every observational comparison: explicitly state that causal attribution requires experimental evidence.
7. Never report "no difference" from a non-significant result without first reporting statistical power.
