# VARIANCE DECOMPOSITION ENGINE
**Phase B — Analytical Brain | Engine B1.3**
**Depth Contract: FULL (17/17 + Analytical Reasoning Contract 8/8)**

---

## PURPOSE
Quantify exactly *how* and *where* a metric changed between two states (e.g., Period 1 vs Period 2, or Actual vs Target) by breaking down the total variance into its structural, dimensional, or mathematical components. Variance decomposition is a mathematical identity, not a statistical inference. It provides the mechanical explanation for a change (the "what") which must be established before any diagnostic reasoning (the "why") can begin.

**Hard rule**: Never attempt to explain *why* a high-level metric changed without first decomposing exactly *where* the variance occurred mathematically.

## SCOPE
- Additive metrics (e.g., Total Revenue = Region A + Region B + Region C).
- Multiplicative metrics (e.g., Revenue = Traffic × Conversion Rate × AOV).
- Rate/Ratio metrics (e.g., Overall Margin = Sum(Profit) / Sum(Revenue)).
- Price-Volume-Mix (PVM) analysis.

---

## INPUTS
```
INPUT
├── metric                   : The target KPI being analyzed
├── metric_contract          : From Foundation A1 — defines the formula and dependencies
├── state_0                  : Baseline data (e.g., Previous Period, Target)
├── state_1                  : Current data (e.g., Current Period, Actual)
├── decomposition_type       : (dimensional | formulaic | price_volume_mix)
└── dimensions               : (Optional) Categorical splits for dimensional decomposition
```

## OUTPUT CONTRACT
```
OUTPUT — DECOMPOSITION REPORT
├── total_variance           : Absolute (Δ) and Relative (Δ%) change in target KPI
├── decomposition_method     : Method used (e.g., Taylor Series, PVM, Waterfall)
├── component_contributions  : List of components and their absolute/relative impact on total Δ
├── interaction_effect       : Joint/mix effect (if applicable)
├── reconciliation_check     : Boolean — do components sum EXACTLY to total_variance?
├── dominant_driver          : The component with the largest absolute contribution
├── structural_shift_flag    : Flag if a mix shift masked a rate change (Simpson's Paradox risk)
└── interpretation_notes     : Narrative explaining the mechanical breakdown of the change
```

---

## ANALYTICAL REASONING CONTRACT

### A. Question → Method Mapping
```
Q: "Why is overall conversion rate down when every region's conversion rate is up?"
    → Dimensional decomposition (Mix shift analysis / Simpson's Paradox).

Q: "Revenue missed target by $1M. Was it lower traffic or lower average order value?"
    → Formulaic decomposition (Revenue = Traffic × CR × AOV).

Q: "Sales are up 10%. Is that because we sold more units, or raised prices?"
    → Price-Volume-Mix (PVM) decomposition.

Q: "Which product category drove the Q3 revenue decline?"
    → Dimensional additive decomposition.
```

### B. Method Selection Rationale
```
DECISION FRAMEWORK:

    Is the metric a simple sum of segments? (e.g., Total = A + B + C)
    → Use DIMENSIONAL ADDITIVE DECOMPOSITION (Waterfall).

    Is the metric a product of other metrics? (e.g., KPI = A × B)
    → Use FORMULAIC DECOMPOSITION (Logarithmic mean Divisia index / Taylor expansion).

    Is the metric Revenue composed of Unit Price and Quantity across multiple products?
    → Use PRICE-VOLUME-MIX (PVM) DECOMPOSITION.

    Is the metric a Ratio/Rate across segments? (e.g., Overall CR = Total Conv / Total Visits)
    → Use RATE-MIX DECOMPOSITION to isolate true performance (rate) from structural changes (mix).
```

### C. Alternative Methods
```
For Formulaic Decomposition (A × B):
    PRIMARY: Logarithmic Mean Divisia Index (LMDI) — leaves no residual/interaction term.
    ALTERNATIVE: Step-by-step substitution (waterfall with explicit interaction/mix term).
    AVOID: Simple one-at-a-time isolation (leaves a massive unexplained interaction gap).
```

### D. When NOT to Use / Misuse Prevention
```
DO NOT confuse variance decomposition with causal driver analysis:
    Decomposition proves that "AOV dropping by $5 mathematically caused $1M of the revenue miss."
    It does NOT explain *why* AOV dropped. Do not claim causality beyond the mechanical formula.

DO NOT ignore the interaction/mix effect in multiplicative changes:
    If Price increases and Volume increases, total change is NOT just (ΔP × V) + (ΔV × P).
    There is a joint effect (ΔP × ΔV). Hiding this in "Volume" or "Price" is mathematically false.
    Always explicitly calculate and report the Interaction/Mix term, or use LMDI.

DO NOT decompose non-additive/non-multiplicative metrics without a defined formula:
    E.g., "Median Revenue" cannot be neatly decomposed into sub-segment medians.
    Decomposition requires algebraic links (sums, products, ratios).
```

### E. Interpretation Constraints
```
MIX EFFECT:
    A positive mix effect means a larger share of the total shifted toward higher-value components.
    It does not mean performance improved.
    (e.g., Selling more luxury cars instead of economy cars raises average revenue per car,
    even if the price of both car types dropped).

RECONCILIATION:
    The sum of decomposed impacts MUST equal the total variance exactly.
    If Sum(Impacts) ≠ Total Δ, the decomposition math is wrong or incomplete.
```

### F. Causal-vs-Associational Boundary
```
Variance decomposition is STRICTLY DETERMINISTIC and MECHANICAL.
It operates purely on algebraic identities.

FORBIDDEN: "The marketing campaign caused the volume increase, which drove the revenue variance."
    ← Decomposition does not know about the marketing campaign.

REQUIRED: "Volume variance mechanically accounts for 80% of the revenue increase.
           Diagnostic analysis (Engine B1.4/B4) is required to determine what drove the volume."
```

### G. Uncertainty Handling
```
Standard variance decomposition assumes NO UNCERTAINTY — it is an exact accounting framework applied to historical/actual data.
However, if the inputs themselves are estimates (e.g., sampled data):
    - Report the confidence interval of the total variance first (Comparative Analysis B1.2).
    - Propagate standard errors through the decomposition formula using the Delta Method.
    - If CI includes 0 for a component, flag its contribution as statistically indistinguishable from noise.
```

### H. Output Interpretation Contract
```
A complete decomposition report answers:
    1. What was the total absolute and relative change?
    2. Which component(s) mathematically drove this change?
    3. Did any components offset each other? (e.g., Volume up, Price down).
    4. Was there a structural shift (Mix effect)?
    5. Do all components reconcile perfectly to the total?
    6. What is the specific mechanical question this hands off to diagnostic reasoning?
```

---

## PROCEDURE

### STEP 1 — Validate Metric and Inputs
```
□ Retrieve Metric Contract (Foundation A1) to get the exact formula.
□ Ensure state_0 and state_1 data are at the same grain (Foundation A2).
□ Calculate Total KPI for state_0 (V0) and state_1 (V1).
□ Total Variance = V1 - V0.
```

### STEP 2 — Execute Additive Decomposition (if applicable)
```
If V = Σ X_i (e.g., Total Revenue = Region A + Region B):
    For each segment i:
        Impact_i = X_i1 - X_i0
    Verify: Σ Impact_i = Total Variance
```

### STEP 3 — Execute Rate-Mix Decomposition (if ratio metric)
```
If V = Σ(Numerator_i) / Σ(Denominator_i):
    Let R_i = Rate of segment i = Numerator_i / Denominator_i
    Let W_i = Weight (Mix) of segment i = Denominator_i / Σ(Denominator_i)
    V = Σ(R_i × W_i)

    Rate Effect (holding mix constant):
        Impact_Rate_i = (R_i1 - R_i0) × W_i0

    Mix Effect (holding rate constant):
        Impact_Mix_i = (W_i1 - W_i0) × R_i0

    Interaction Effect:
        Impact_Interaction_i = (R_i1 - R_i0) × (W_i1 - W_i0)

    Verify: Σ(Impact_Rate_i + Impact_Mix_i + Impact_Interaction_i) = Total Variance
```

### STEP 4 — Execute Price-Volume-Mix (PVM) (if Revenue/Margin)
```
Let P = Price per unit, Q = Quantity, V = P × Q (Revenue)
For multiple products i:
    Volume Effect:   Σ [ (Q_i1 - Q_i0) × P_i0 ]
    Price Effect:    Σ [ (P_i1 - P_i0) × Q_i0 ]
    Mix/Joint Effect: Σ [ (P_i1 - P_i0) × (Q_i1 - Q_i0) ]

    Verify: Volume Effect + Price Effect + Mix Effect = V1 - V0
```

### STEP 5 — Isolate the Dominant Driver
```
Sort components by Absolute(Impact) descending.
Identify which component accounts for the majority of the absolute variance.
Flag if a massive Mix Effect is present (indicates structural shift, not performance change).
```

### STEP 6 — Format for Waterfall Visualization
```
Prepare outputs specifically suited for a waterfall chart:
    Start: V0
    Steps: Sorted component impacts (Rate, Volume, Price, Mix, etc.)
    End: V1
```

---

## DECISION TREE
```
Decomposition requested for Metric M
        │
        ▼
What is the mathematical structure of M? (Check A1 Contract)
        │
M is a sum of parts (A + B) ───────────→ Use Additive Decomposition
        │                                  (Impact = ΔA + ΔB)
        │
M is a product (A × B) ────────────────→ Use Multiplicative Decomposition
        │                                  (ΔA·B0 + ΔB·A0 + ΔA·ΔB)
        │
M is a weighted ratio (Σ(r·w)) ────────→ Use Rate-Mix Decomposition
        │                                  (Isolate Rate vs Mix shift)
        │
M is Revenue = Σ(Price × Qty) ─────────→ Use PVM Decomposition
        │
        ▼
Calculate Component Impacts
        │
        ▼
Reconciliation Check: Do components sum EXACTLY to V1 - V0?
    NO  → HALT. Math error or unhandled interaction term.
    YES → Proceed.
        │
        ▼
Identify dominant component and output report.
```

---

## MATHEMATICAL DEFINITIONS

**Multiplicative Decomposition (2 factors: A × B):**
$$\Delta V = V_1 - V_0 = (A_1 B_1) - (A_0 B_0)$$
$$\Delta V = \underbrace{(A_1 - A_0) B_0}_{\text{Impact of A}} + \underbrace{(B_1 - B_0) A_0}_{\text{Impact of B}} + \underbrace{(A_1 - A_0)(B_1 - B_0)}_{\text{Interaction}}$$

**Logarithmic Mean Divisia Index (LMDI) (Alternative for no residual):**
If $V = A \times B \times C$, the impact of component $X \in \{A, B, C\}$ is:
$$\Delta V_X = \frac{V_1 - V_0}{\ln(V_1 / V_0)} \ln\left(\frac{X_1}{X_0}\right)$$
This ensures $\Delta V_A + \Delta V_B + \Delta V_C = \Delta V$ perfectly without an explicit interaction term. (Valid only when all values > 0).

**Rate-Mix Decomposition:**
$$\Delta V = \sum_{i} \left[ \Delta R_i W_{i0} + \Delta W_i R_{i0} + \Delta R_i \Delta W_i \right]$$

---

## PRECONDITIONS
- [ ] The metric is algebraically decomposable (sums, products, ratios).
- [ ] Metric Contract (A1) defines the exact formula.
- [ ] No missing values in the components for state_0 or state_1.
- [ ] Denominators for rates/ratios are strictly non-zero.

## ASSUMPTIONS
- Decomposition assumes the formula represents the complete universe of mechanical drivers.
- Assumes data grain is identical across state_0 and state_1.

---

## EDGE CASES

| Case | Problem | Resolution |
|------|---------|------------|
| Denominator = 0 in State 0 | Division by zero in growth/LMDI math | Use absolute additive decomposition; avoid LMDI |
| New product launched in State 1 | No State 0 baseline for PVM | Treat State 0 Price/Qty as 0; isolate as "New Volume" effect |
| Simpson's Paradox | Overall rate drops, but all sub-rates rise | Rate-Mix decomposition will show positive Rate Effect and massive negative Mix Effect |
| Non-additive metrics (Unique Users) | Total ≠ Sum of parts | Cannot use standard additive decomposition. Must decompose via set logic (New + Retained - Churned) |

---

## FAILURE MODES

| Failure | Symptom | Detection | Severity |
|---------|---------|-----------|----------|
| Ignoring interaction term | Components don't sum to total | Σ(Impacts) ≠ Total Δ | CRITICAL |
| Decomposing unique counts additively | Overstating segment contributions | Total < Σ(Parts) | HIGH |
| Treating Mix Effect as Performance | Wrong business conclusion | Mix effect not separated from Rate | HIGH |
| Causal language used for mechanical math | Confusing the "what" with the "why" | "Price caused..." in text | HIGH |

---

## COUNTEREXAMPLES

**Counterexample A — Simpson's Paradox (Ignoring Mix):**
```
Overall Conversion Rate: Q1 = 5.0%, Q2 = 4.8% (Drop of 0.2%)
Desktop CR: Q1 = 6.0%, Q2 = 6.5% (UP)
Mobile CR: Q1 = 2.0%, Q2 = 2.5% (UP)

WRONG: "Conversion rate dropped, so product performance worsened."
RIGHT (via Rate-Mix Decomposition):
    Rate Effect: +0.5% (Performance improved across all platforms)
    Mix Effect:  -0.7% (Massive shift in traffic from Desktop to Mobile)
    Interaction:  0.0%
    Total:       -0.2%
    Conclusion: Performance improved. The total metric dropped purely due to structural traffic shift.
```

**Counterexample B — Ignoring the Interaction Term:**
```
Revenue = Traffic × AOV
State 0: 100 visits × $10 = $1,000
State 1: 150 visits × $15 = $2,250 (Total Δ = +$1,250)

WRONG:
    Traffic Impact = 50 × $10 = $500
    AOV Impact     = $5 × 100 = $500
    Total explained = $1,000. (Leaves $250 unexplained).

RIGHT:
    Traffic Impact = $500
    AOV Impact     = $500
    Interaction    = 50 × $5 = $250
    Total explained = $1,250.
```

---

## WORKED EXAMPLE

**Question:** "Why did our overall profit margin drop from 20% to 18% YoY?"

```
STEP 1: Metric Contract
    Margin = Total Profit / Total Revenue
    Segments: Enterprise, SMB

STEP 2: Data (State 0 vs State 1)
    State 0:
      Enterprise: Rev $80k, Profit $24k (Rate 30%, Mix 80%)
      SMB: Rev $20k, Profit $2k (Rate 10%, Mix 20%)
      TOTAL: Rev $100k, Profit $26k -> Margin 26%

    State 1:
      Enterprise: Rev $50k, Profit $15k (Rate 30%, Mix 50%)
      SMB: Rev $50k, Profit $5k (Rate 10%, Mix 50%)
      TOTAL: Rev $100k, Profit $20k -> Margin 20%

    TOTAL VARIANCE = 20% - 26% = -6.0%

STEP 3: Rate-Mix Decomposition
    Enterprise Rate Effect: (30% - 30%) * 80% = 0.0%
    SMB Rate Effect:        (10% - 10%) * 20% = 0.0%
    Total Rate Effect = 0.0%

    Enterprise Mix Effect:  (50% - 80%) * 30% = -30% * 30% = -9.0%
    SMB Mix Effect:         (50% - 20%) * 10% = +30% * 10% = +3.0%
    Total Mix Effect = -6.0%

    Interaction Effect: 0.0%

STEP 4: Reconciliation
    0.0% (Rate) + -6.0% (Mix) + 0.0% (Interaction) = -6.0% (Total Variance) -> PASS.

STEP 8: Output Report
    "The 6.0 percentage point drop in total margin was driven entirely by a structural mix shift (Mix Effect = -6.0pp).
    Profitability (Rate) within the Enterprise and SMB segments did not change (Rate Effect = 0.0pp).
    The decline is mechanically caused by lower-margin SMB revenue growing from 20% to 50% of total revenue mix."
```

---

## ADVERSARIAL EXAMPLE

**Request:** "Revenue missed target by $5M. Calculate the volume vs price impact, and tell me if the marketing team failed."

**Engine Response:**
```
BLOCKED — Causal attribution violation.

ISSUE: Variance decomposition calculates mechanical mathematical impacts; it cannot attribute blame or establish causality to external teams/events.

MECHANICAL BREAKDOWN (PVM):
    Total Variance: -$5M
    Volume Effect: -$6M
    Price Effect: +$0.5M
    Mix/Joint Effect: +$0.5M
    Reconciliation: -6 + 0.5 + 0.5 = -5M (PASS)

REPORTING:
    WRONG: "Marketing failed to drive volume, causing a $6M drop."
    RIGHT: "The $5M revenue miss is mechanically driven by lower-than-target volume (-$6M impact), partially offset by higher realized prices (+$0.5M). Determining WHY volume missed target requires diagnostic driver analysis."
```

---

## VALIDATION RULES
1. The sum of all decomposed components MUST exactly equal the total variance.
2. Multiplicative decompositions MUST include an explicit interaction term or use LMDI.
3. Ratio/Rate metrics MUST be decomposed using Rate-Mix methodology to check for Simpson's Paradox.
4. Output must use mechanical language ("accounts for", "driven mathematically by") and never causal language ("caused by", "because of").

## TEST CASES

| ID | Input | Expected Output | Pass Condition |
|----|-------|----------------|----------------|
| VAR-001 | A×B decomposition lacking interaction term | HALT / FAIL | Engine detects Sum(Impacts) ≠ Total Δ |
| VAR-002 | Rate metric where sub-rates rise but total falls | Rate-Mix output showing negative Mix effect | Identifies Simpson's Paradox structurally |
| VAR-003 | Request to decompose "Median Session Time" by segment | HALT | Engine rejects non-decomposable non-additive metric |
| VAR-004 | PVM calculation with exact reconciliation | Outputs Vol, Price, and Mix contributions | Reconciliation passes exactly |

---

## AGENT EXECUTION INSTRUCTIONS
1. Always establish the algebraic formula from Foundation A1 before decomposing.
2. Run the reconciliation check (Σ Impacts = Total Δ) internally before outputting results. If it fails, recalculate.
3. If analyzing rates, conversions, or margins, DEFAULT to Rate-Mix decomposition. Do not just subtract the rates.
4. Strip all causal/blame language from the interpretation. Stick to "structural shift", "mechanical driver", and "rate vs mix".
