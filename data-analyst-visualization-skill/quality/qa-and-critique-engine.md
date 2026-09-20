# QUALITY & SELF-CRITIQUE ENGINE
**Phase F — Quality Brain**
**Depth Contract: FULL**

## PURPOSE
To act as the final hostile reviewer before presenting artifacts to the user. 
A BEAUTIFUL WRONG DASHBOARD IS A FAILED DASHBOARD.

## THE 5-LAYER QA GATE

### 1. DATA QA
- [ ] Grain match? (No duplicate multiplication in joins).
- [ ] Missingness handled? (No blind mean imputation).
- [ ] Outliers acknowledged? 

### 2. CALCULATION QA
- [ ] Denominators intact? (Did filtering remove the baseline?)
- [ ] Percentage change vs Percentage-point change used correctly?
- [ ] Aggregation logic matches metric definition?

### 3. STATISTICAL QA
- [ ] Correlation != Causation explicit?
- [ ] Sample size sufficient for claims?
- [ ] Uncertainty / Confidence Intervals visualized?

### 4. VISUALIZATION QA
- [ ] Chart type passes Decision Engine rules?
- [ ] Axes not misleadingly truncated?
- [ ] Units and currency consistent?
- [ ] No chart junk (3D, unnecessary gridlines, heavy borders)?

### 5. STORY QA
- [ ] Does the headline exceed the evidence?
- [ ] Is the most important insight visually dominant?
- [ ] Are next steps or diagnostic hypotheses clear?

## THE SELF-CRITIQUE LOOP
`GENERATE -> INSPECT -> CRITIQUE -> CLASSIFY -> FIX -> RE-INSPECT -> PASS/FAIL`
If an output fails any of the 5 QA layers, the Agent MUST fix it before finalizing the turn. Do not present a broken chart with an apology; present a fixed chart.
