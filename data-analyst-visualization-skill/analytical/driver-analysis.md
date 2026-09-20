# DRIVER ANALYSIS ENGINE
**Phase B — Analytical Brain | Engine B1.4**
**Depth Contract: FULL (17/17 + Analytical Reasoning Contract 8/8)**

---

## PURPOSE
Identify, quantify, and rank the underlying variables (features, behaviors, metrics) that have the strongest association with a target KPI. Driver analysis bridges the gap between *what* happened (Descriptive B1.1, Comparative B1.2, Decomposition B1.3) and *where* to focus diagnostic attention. It separates the signal (highly predictive/associated features) from the noise (weak or spurious correlates).

**Hard rule**: Driver analysis discovers *predictors* and *correlates*. It does NOT discover *causes* unless operated within a strict causal inference framework. A high importance score means "knowing X helps predict Y," not "changing X will change Y."

## SCOPE
- Continuous targets (e.g., LTV, Revenue, Time-on-site).
- Binary targets (e.g., Churned vs. Retained, Converted vs. Dropped).
- Feature importance ranking.
- Bivariate and multivariate association.

---

## INPUTS
```
INPUT
├── target_variable          : The KPI to be explained (with Foundation A1 contract)
├── candidate_drivers        : List of potential explanatory variables
├── dataset                  : Analytical dataset at the correct grain (Foundation A2)
├── method_preference        : (linear | tree_based | relative_importance | bivariate)
└── missingness_handling     : Defined via Assumption Registry (Foundation A5)
```

## OUTPUT CONTRACT
```
OUTPUT — DRIVER REPORT
├── target_metric            : Name of the target being analyzed
├── driver_ranking           : Ranked list of features by importance score
├── importance_metric        : Pearson r, standardized beta, SHAP, or relative variance explained
├── direction_of_effect      : Positive, Negative, or Non-linear (per driver)
├── variance_explained       : R² or pseudo-R² (how much of the target is explained by the model)
├── multicollinearity_flag   : VIF scores > 5 flagged (if multivariate linear)
├── causal_disclaimer        : Explicit warning against interpreting drivers as levers
└── interpretation_notes     : Narrative prioritizing top 3 drivers for further investigation
```

---

## ANALYTICAL REASONING CONTRACT

### A. Question → Method Mapping
```
Q: "What behaviors are most common among users who churn?"
    → Bivariate driver analysis (Correlation / Information Value).

Q: "Which product feature usage is the strongest predictor of high LTV, holding others constant?"
    → Multivariate analysis (Standardized Regression / Relative Importance).

Q: "Are there complex, non-linear patterns driving conversion?"
    → Tree-based Feature Importance (Random Forest / SHAP).
```

### B. Method Selection Rationale
```
DECISION FRAMEWORK:

    Are drivers highly correlated with EACH OTHER (Multicollinearity)?
    YES → Standard regression coefficients (beta) will be unstable/wrong.
          Use Relative Importance Analysis (Shapley value regression / LMG) or Ridge Regression.

    Are relationships linear and additive?
    YES → Standardized Linear/Logistic Regression.
    NO / UNKNOWN → Tree-based models (Random Forest, Gradient Boosting) + SHAP values.

    Is interpretability more important than maximum predictive power?
    YES → Linear/Logistic with standardized coefficients.
    NO → Black-box + SHAP.

    Quick exploratory pass?
    → Bivariate correlation matrix (Pearson/Spearman) or Information Value (IV) for binary targets.
```

### C. Alternative Methods
```
PRIMARY: Shapley Value Regression (LMG / relaimpo) for linear, SHAP for non-linear.
    Why? Fairly distributes variance explained among correlated predictors.
ALTERNATIVE: Standardized Regression Coefficients (Beta).
    Why? Fast to compute, but highly sensitive to multicollinearity.
AVOID: Stepwise Regression.
    Why? Statistically flawed, inflates false positives, unstable with collinearity.
```

### D. When NOT to Use / Misuse Prevention
```
DO NOT interpret Driver Importance as a Causal Lever:
    Finding: "Number of support tickets" is the #1 driver of Churn.
    Misuse: "We should stop users from opening support tickets to reduce churn."
    Correction: Support tickets are a SYMPTOM of a broken product experience, not the cause.

DO NOT ignore Multicollinearity:
    If "Page Views" and "Time on Site" have r=0.95, putting both in a standard regression
    will cause their importance scores to be erratic, artificially deflated, or flip signs.
    Always check Variance Inflation Factor (VIF).

DO NOT analyze drivers at the wrong grain:
    Target: Account-level Churn. Drivers: User-level clicks.
    Must aggregate drivers to the Account grain (Foundation A2) before modeling.
```

### E. Interpretation Constraints
```
BIVARIATE CORRELATION (Pearson r):
    Only measures linear association. r=0 does not mean no relationship (could be U-shaped).
    Suffers from omitted variable bias.

STANDARDIZED BETA (β):
    "A 1 standard deviation increase in X is associated with a β standard deviation change in Y,
    holding all other modeled variables constant."

SHAP VALUES:
    "Feature X contributed +Y to the prediction for this specific instance, compared to the base value."
    Global importance is the mean absolute SHAP value across all instances.
```

### F. Causal-vs-Associational Boundary
```
Driver analysis is STRICTLY ASSOCIATIONAL.

FORBIDDEN: "Feature X drives a 10% increase in LTV."
FORBIDDEN: "To improve conversion, we need to increase Metric Y."

REQUIRED: "Feature X is the strongest predictor of high LTV in the historical data."
REQUIRED: "Metric Y is highly associated with conversion. It is a strong candidate lever. 
           We recommend an A/B test to validate if intervening on Metric Y causally improves conversion."

Observational associations may generate "Candidate Drivers," "Hypotheses," or "Candidate Levers."
However, explicitly label them as associational hypotheses. Do NOT present them as proven causal interventions unless the data comes from a randomized experiment.
```

### G. Uncertainty Handling
```
Models fit to historical data contain sampling error and structural error.
- Report R²: If R² = 0.15, the top "drivers" only explain 15% of the variance; 85% is unknown.
- Cross-validation: Report importance scores calculated on hold-out folds to avoid overfitting,
  especially for tree-based models.
- If CI for a regression coefficient crosses zero, flag the driver as statistically insignificant.
```

### H. Output Interpretation Contract
```
A complete driver analysis report answers:
    1. Which variables have the strongest predictive association with the target?
    2. Are these associations positive, negative, or non-linear?
    3. How much of the total variance in the target do these drivers explain?
    4. Are the drivers correlated with each other (confounding)?
    5. What is the explicit warning regarding causality?
    6. What hypotheses does this generate for future causal testing (A/B tests)?
```

---

## PROCEDURE

### STEP 1 — Validate Preconditions
```
□ Target metric definition verified (Foundation A1).
□ Grain consistency verified between target and all drivers (Foundation A2).
□ Missing values imputed or handled per Assumption Registry (Foundation A5).
□ Outliers treated (Descriptive B1.1).
```

### STEP 2 — Bivariate Screening
```
Compute bivariate association for all candidate drivers with the target:
    Continuous Target: Pearson r (linear), Spearman ρ (monotonic/non-linear).
    Binary Target: Point-biserial correlation, or Information Value (IV).
Filter out variables with near-zero association to simplify the multivariate model.
```

### STEP 3 — Multicollinearity Check
```
Compute correlation matrix of all candidate predictors.
Compute Variance Inflation Factor (VIF) for each predictor:
    VIF_i = 1 / (1 - R²_i) (where R²_i is the R² of predicting X_i using all other X's).
IF any VIF > 5:
    Flag multicollinearity.
    Standard regression coefficients will be invalid.
    Must use Relative Importance (Shapley) or remove redundant variables.
```

### STEP 4 — Fit Multivariate Model
```
LINEAR (if relationships are linear and VIFs < 5):
    Standardize all continuous variables (mean=0, std=1).
    Fit OLS regression (or Logistic for binary target).
    Extract Standardized Coefficients (Betas).

TREE-BASED (if non-linear, high VIF, or complex interactions):
    Fit Random Forest or Gradient Boosting Machine (e.g., XGBoost).
    Tune depth to avoid extreme overfitting.
```

### STEP 5 — Calculate Importance Scores
```
If LINEAR:
    Use Relative Importance (LMG / Shapley Value Regression) to decompose R² among predictors.
    Fallback: absolute value of standardized Beta.

If TREE-BASED:
    Use TreeSHAP.
    Global Importance = mean(|SHAP_i|) across all observations.
    Check direction via SHAP dependence plots (does higher feature value yield positive SHAP?).
```

### STEP 6 — Format Output
```
Rank drivers by Importance Score descending.
Calculate cumulative variance explained.
Append Causal Disclaimer to the top of the report.
```

---

## DECISION TREE
```
Driver Analysis requested for Target Y
        │
        ▼
Run Bivariate Screen & VIF Check (Steps 2-3)
        │
Are relationships highly non-linear OR VIF > 5?
   YES ──────────────────────────────────────┐
   NO                                        │
    ▼                                        ▼
Fit Standardized OLS / Logistic         Fit Random Forest / XGBoost
    │                                        │
Calculate Relative Importance           Calculate SHAP values
(Shapley decomposition of R²)           (mean absolute SHAP)
    │                                        │
    ▼                                        ▼
Rank Drivers & Extract Directionality
        │
        ▼
Is Total R² < 0.10?
    YES → Flag: "Model has very low explanatory power. Top drivers are weak signals."
    NO  → Proceed.
        │
        ▼
Attach Causal Disclaimer (Associational only)
        │
        ▼
Output Driver Report
```

---

## MATHEMATICAL DEFINITIONS

**Standardization (Z-score):**
$$z_{ij} = \frac{x_{ij} - \bar{x}_j}{s_j}$$
Required before OLS so coefficients are comparable.

**Variance Inflation Factor (VIF):**
$$VIF_j = \frac{1}{1 - R^2_j}$$
where $R^2_j$ is the $R^2$ of regression of predictor $X_j$ on all other predictors.

**Relative Importance (LMG / Shapley for Linear Models):**
The marginal contribution of feature $j$ to a model containing a subset of features $S$ is:
$$\Delta R^2(j | S) = R^2(S \cup \{j\}) - R^2(S)$$
The Shapley value (LMG importance) averages this marginal contribution over all possible subsets $S$.

**Global SHAP Feature Importance:**
$$I_j = \frac{1}{N} \sum_{i=1}^N |\phi_j^{(i)}|$$
where $\phi_j^{(i)}$ is the SHAP value for feature $j$ on observation $i$.

---

## PRECONDITIONS
- [ ] Variables have sufficient variance (std_dev > 0, checked in B1.1).
- [ ] Grain is mathematically aligned (e.g., do not mix session-level drivers with user-level targets without aggregation).
- [ ] Sufficient sample size (n > 10 * number_of_predictors).

## ASSUMPTIONS
- OLS Beta assumes linear, additive relationships and homoscedasticity.
- SHAP assumes the model has sufficiently learned the true data generation process without extreme overfitting.

---

## EDGE CASES

| Case | Problem | Resolution |
|------|---------|------------|
| Two perfectly correlated drivers | VIF = ∞, model fails | Drop one, or use PCA to combine |
| Target is heavily imbalanced (e.g., 1% churn) | Model predicts majority class only | Use balanced class weights, SMOTE, or evaluate via PR-AUC |
| Time-series data | Autocorrelation violates independence | Use time-series specific methods (e.g., Granger Causality, VAR); do not use standard OLS |
| Categorical driver with 1000 levels | Explodes model dimensionality | Group rare levels into "Other" or use Target Encoding |

---

## FAILURE MODES

| Failure | Symptom | Detection | Severity |
|---------|---------|-----------|----------|
| Ignoring Multicollinearity | Betas have wrong signs or massive standard errors | VIF > 5 not checked | CRITICAL |
| Causal interpretation | Recommending changing X to fix Y without experiment | Manual review against Rule F | CRITICAL |
| Overfitting | R² on training = 0.99, test = 0.10 | No cross-validation / holdout used | HIGH |
| Reverse causality included | Target actually causes the Driver | Logical check of timeline (e.g., receipt printed driving purchase) | HIGH |

---

## COUNTEREXAMPLES

**Counterexample A — The Multicollinearity Trap:**
```
Target: LTV. Drivers: "Total Sessions", "Total Pageviews", "Total Clicks".
These three drivers have Pearson r > 0.90 with each other (VIF > 20).

WRONG: Run OLS. "Total Sessions" beta is negative, "Total Clicks" beta is positive.
       Conclusion: "Sessions are bad for LTV, clicks are good."
RIGHT: Check VIF. VIF > 5 detected. Switch to Shapley relative importance, which fairly distributes
       the shared R² among the three, showing they are all strong, positive predictors of LTV.
```

**Counterexample B — The Causal Trap (Reverse Causality / Symptom as Cause):**
```
Target: Churn. Driver analysis finds "Number of password resets" is the #1 predictor.

WRONG: "We should remove the password reset button so users don't churn."
RIGHT: "Password resets are a strong leading indicator of churn intent.
        This is an associational finding. Users likely reset passwords because they want
        to log in one last time to cancel their account. The reset is a symptom, not a lever."
```

---

## WORKED EXAMPLE

**Question:** "What user actions in the first 7 days best predict Day 30 Retention?"

```
STEP 1: Preconditions
    Target: Day 30 Retained (Binary 1/0)
    Drivers: D7_logins, D7_messages_sent, D7_profile_views, D7_errors_hit
    Grain: User-level

STEP 2 & 3: VIF Check
    VIF for all variables < 2.5 (No severe multicollinearity).

STEP 4: Model Fit
    Binary target, VIF < 5 → Fit Logistic Regression with standardized predictors.

STEP 5: Importance Scores (Standardized absolute Betas)
    D7_messages_sent: |Beta| = 1.45 (Positive)
    D7_errors_hit:    |Beta| = 0.85 (Negative)
    D7_profile_views: |Beta| = 0.22 (Positive)
    D7_logins:        |Beta| = 0.15 (Positive)

    Pseudo R² = 0.28 (Moderate explanatory power)

STEP 8: Output Report
    "The strongest predictor of Day 30 Retention is 'D7_messages_sent' (Positive association).
    Users who send more messages in their first week are significantly more likely to retain,
    holding other factors constant. The second strongest predictor is 'D7_errors_hit' (Negative association).
    The model explains ~28% of the variance in retention behavior.

    CAUSAL DISCLAIMER: These are associational predictors, not confirmed causal levers.
    Forging 'message sent' events or forcing users to send messages will not necessarily increase retention.
    RECOMMENDATION: Run an A/B test on onboarding flows that naturally encourage messaging."
```

---

## ADVERSARIAL EXAMPLE

**Request:** "Tell me exactly what features to change to increase conversion rate based on the driver analysis."

**Engine Response:**
```
CAUSAL CLAIM BLOCKED — Re-framing as Candidate Levers.

ISSUE: Driver analysis identifies what correlates with conversion (associational), not what causes it.
       You asked what to "change" (intervention). I cannot guarantee a causal outcome from observational data.

ACTION:
    I will identify the top PREDICTORS of conversion and present them as CANDIDATE LEVERS (Hypotheses).
    Changing a highly ranked feature (e.g., 'Viewed Pricing Page') by forcing users to view it
    may decrease conversion despite the correlation. Causal validation requires an experiment.

OUTPUT PROCEEDING WITH CANDIDATE LEVERS (HYPOTHESES) REPORT...
```

---

## VALIDATION RULES
1. VIF must be calculated before any linear/logistic regression; if VIF > 5, standard betas are invalid.
2. Standardized coefficients (z-score inputs) must be used if comparing Betas.
3. Every driver analysis report must include the explicit Causal Disclaimer.
4. R² (or pseudo-R²) must be reported to contextualize how much variance remains unexplained.

## TEST CASES

| ID | Input | Expected Output | Pass Condition |
|----|-------|----------------|----------------|
| DRV-001 | 3 highly correlated drivers (r=0.95) | VIF flag triggered | Engine refuses standard OLS betas |
| DRV-002 | Request causal levers from observational data | "Candidate lever" allowed with hypothesis label; proven causal claim blocked | Engine reframes request but does not fail |
| DRV-003 | Continuous target, linear relationships | Relative Importance or Std Beta used | Standardization applied before fit |
| DRV-004 | Target with no strong drivers (R² = 0.02) | "Weak signal" warning reported | Engine does not over-hype the #1 weak driver |

---

## AGENT EXECUTION INSTRUCTIONS
1. Never fit an OLS regression for driver importance without checking VIF first.
2. If interpretability of non-linear patterns is needed, default to Random Forest + SHAP.
3. Paste the Causal Disclaimer verbatim at the bottom of every driver analysis.
4. Ensure the target and drivers are at the exact same data grain (refer to Foundation A2) before building the design matrix.
