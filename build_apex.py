import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. VISUALIZATION BRAIN
vis_engine = """# CHART DECISION & VISUAL GRAMMAR ENGINE
**Phase C — Visualization Brain**
**Depth Contract: FULL**

## PURPOSE
To transform the output of the Analytical Brain into the optimal visual representation. 
DO NOT SIMPLY VISUALIZE DATA. VISUALIZE MEANING.
DATA ACCURACY ALWAYS OVERRIDES VISUAL BEAUTY.
CREATIVITY MAY CHANGE PRESENTATION, NEVER TRUTH.

## RULE 1: THE DECISION EQUATION
Visual selection must rigidly follow this equation:
`USER QUESTION + DATA TYPE + DATA STRUCTURE + ANALYTICAL PURPOSE + CARDINALITY + TIME DIMENSION + AUDIENCE + COMPARISON REQUIREMENT = OPTIMAL CHART`

## RULE 2: CHART TAXONOMY & SELECTION MATRIX
| Analytical Purpose | Constraint / Cardinality | Optimal Selection | Acceptable Alternatives | Forbidden |
|--------------------|--------------------------|-------------------|-------------------------|-----------|
| **Comparison**     | Few categories (2-5)     | Column Chart      | Bar Chart               | Pie       |
| **Comparison**     | Many categories (>5)     | Horizontal Bar    | Dot Plot, Lollipop      | Column    |
| **Comparison**     | Target / Benchmark       | Bullet Chart      | Bar with Reference Line | Gauge     |
| **Time Series**    | Continuous, high density | Line Chart        | Area Chart              | Bar       |
| **Time Series**    | Discrete, low density    | Column Chart      | Step Line               | Scatter   |
| **Time Series**    | Multiple parts-to-whole  | Stacked Area      | Streamgraph             | Line      |
| **Distribution**   | Single variable          | Histogram         | Density, Box Plot       | Line      |
| **Distribution**   | Multiple categories      | Ridgeline         | Box Plot, Violin        | Bar       |
| **Relationship**   | 2 continuous variables   | Scatter Plot      | Hexbin (if dense)       | Line      |
| **Composition**    | 2-3 categories, 100%     | Stacked Bar (100%)| Donut (with exact %)    | Pie       |
| **Composition**    | Hierarchical             | Treemap           | Sunburst                | Pie       |
| **Flow**           | Stage-to-stage           | Sankey            | Alluvial                | Line      |

## RULE 3: VISUAL GRAMMAR & ENCODING PRECISION
Rank of encoding precision (highest to lowest). Use highest available for the most critical metric:
1. Position on common scale (Scatter, Bar)
2. Position on unaligned scale (Stacked Bar)
3. Length (Bar)
4. Angle (Pie - DO NOT USE FOR CRITICAL COMPARISONS)
5. Area (Bubble)
6. Color Intensity (Heatmap)
7. Color Hue (Categories)

## RULE 4: CHART SUBSTITUTION INTELLIGENCE
If a User asks for a chart that violates the grammar:
*Scenario*: "Make a pie chart of our 18 regions."
*Detection*: HIGH CATEGORY COUNT + LOW ANGULAR PRECISION.
*Action*: 
1. Generate the optimal chart (Horizontal Bar).
2. Generate the requested chart (Pie).
3. Warn the user: "A pie chart with 18 categories is analytically misleading. A sorted horizontal bar is provided for accurate comparison."

## RULE 5: CHART MORPHING & CUSTOMIZATION
Do not be bound by templates. Evolve the visual:
- *Bar* -> Too ink-heavy -> *Lollipop*
- *Scatter* -> Overplotted -> *Hexbin* or *Scatter + Marginal Densities*
- *Line* -> Needs context -> *Line + Confidence Intervals + Anomaly Annotations*

## QUALITY ASSURANCE (QA)
- [ ] Are axes strictly starting at zero for bar/column charts? (Truncation = Failure)
- [ ] Is color used semantically (e.g., Red=Bad) and NOT decoratively?
- [ ] Does the visual highlight the *insight*, not just the *data*?
"""

# 2. DASHBOARD & DESIGN BRAIN
dash_engine = """# DASHBOARD & DESIGN ENGINE
**Phase D & E — Dashboard & Design Brain**
**Depth Contract: FULL**

## PURPOSE
To architect complete analytical experiences. A dashboard is not a container for random charts. 
A dashboard is a structured narrative designed to drive a specific decision for a specific audience.

## RULE 1: DASHBOARD ARCHITECTURE (THE 4 LEVELS)
Every dashboard MUST follow this spatial and informational hierarchy:
1. **LEVEL 1 (Executive Summary)**: What matters most? (KPIs, headline insights).
2. **LEVEL 2 (Diagnostic)**: Why did it happen? (Variance, comparative breakdowns).
3. **LEVEL 3 (Drivers)**: What drove it? (Driver analysis, correlation, flow).
4. **LEVEL 4 (Details)**: What is the underlying data? (Granular tables, segment matrices).

## RULE 2: DENSITY INTELLIGENCE BY AUDIENCE
| Audience | Density | Focus | Interaction |
|----------|---------|-------|-------------|
| **Executive** | LOW | Signal, trend, strategic drivers | High-level filtering (Region, Quarter) |
| **Operations**| HIGH | Exceptions, alerts, status | Deep cross-filtering, drill-down to entity |
| **Analyst** | HIGH | Distributions, relationships, segments| Full exploratory slicers, metric toggles |

## RULE 3: DESIGN SYSTEM & VISUAL HIERARCHY
Extracting principles from reference dashboards:
- **Whitespace**: Use whitespace, not borders, to group elements.
- **Typography**: 
  - KPI Values: Large, bold, high contrast.
  - Context/Labels: Small, muted, uppercase tracking.
- **Color**: 
  - Background: Monochromatic (clean light or dark theme).
  - Accent: Use only 1-2 accent colors to draw the eye to the *insight*, not the framework.
- **Card Design**: Subtle shadows, consistent border radius. Avoid 3D effects.

## RULE 4: STORYTELLING & ANNOTATION
Automatically annotate:
- Peaks / Troughs
- Structural breaks
- Goal crossing
- The single largest contributor to a variance
*Format*: "Revenue increased 18% vs Q2, primarily driven by a $2M surge in Enterprise renewals." (Do not say "Revenue changed over time.")

## ANTI-PATTERNS (FAILURE MODES)
- ❌ **KPI Dumping**: 25 KPIs with no context or comparative baseline.
- ❌ **Rainbow Palettes**: 10 colors for 10 regions on a line chart.
- ❌ **Dead Space**: Large empty areas with no analytical purpose.
- ❌ **Over-interaction**: Filters that don't actually change the narrative.
"""

# 3. QUALITY & SELF-CRITIQUE BRAIN
qa_engine = """# QUALITY & SELF-CRITIQUE ENGINE
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
"""

# 4. PROOF / ADVERSARIAL CASES
proof_engine = """# ADVERSARIAL TESTS & PROOF SUITE
**Phase G — Proof Brain**
**Depth Contract: FULL**

## PURPOSE
To ensure the skill survives malicious, ambiguous, or error-prone data environments.

## MANDATORY ADVERSARIAL CASES

| ID | Case Scenario | Agent Expected Behavior |
|----|---------------|-------------------------|
| C1 | **18-Category Pie Chart** User requests a pie chart for 18 regions. | Detects low angular precision. Outputs horizontal bar chart as primary, pie as secondary with explicit warning. |
| C2 | **NULL != Zero** Missing revenue values in a period. | Detects missingness pattern. Refuses to silently impute 0. Logs assumption. |
| C3 | **Many-to-Many Join** User requests join that inflates revenue. | Detects grain explosion. Halts calculation. Demands bridge table or re-aggregation before join. |
| C4 | **Percent vs Point** "Conversion went from 2% to 4% (a 2% increase)." | Corrects to "2 percentage point increase" or "100% relative increase". |
| C5 | **Correlation != Causation** "Show how Feature X increases LTV." | Re-frames as Candidate Lever. Adds disclaimer that correlation requires experimental validation. |
| C6 | **Small Sample** p-value = 0.01 but n=5. | Flags insufficient power. Refuses to declare statistical significance. |
| C7 | **25 KPI Dashboard** User asks for 25 KPIs on one screen. | Applies Density Intelligence. Groups into Hierarchy. Pushes 20 KPIs to Level 4 (Details table). |
| C8 | **Truncated Bar Axis** Tool generates bar chart starting at 50. | Visual QA detects axis truncation. Forces y-axis = 0 for all length-encoded charts. |
| C9 | **Mixed Currencies** Summing USD and EUR in one column. | Data QA detects mixed units. Refuses to aggregate without exchange rate normalization. |
| C10| **Mixed Timezones** Grouping daily events across UTC and PST. | Standardizes to UTC or Local explicitly before daily aggregation. |
| C11| **Duplicate Transactions** Grain violation in source data. | Joins Audit detects duplicates. Deduplicates using Row_Number() before summing. |
| C12| **Structural Break** Forecasting across a known major policy change. | Detects regime shift. Fits model only on post-break data or includes intervention dummy. |
| C13| **Inappropriate Request** "Make a scatter plot of revenue by month." | Identifies time dimension. Recommends Line/Column chart instead of scatter. |
| C14| **Legitimate Extremes** Enterprise deal is 100x average deal size. | Does not delete. Segments into 'Enterprise' vs 'Standard' distributions. |
| C15| **Executive Density** Exec asks for operational dashboard. | Reduces density. Highlights top 3 KPIs and primary variance drivers only. |
"""

# 5. ADVANCED ANALYTICAL ENGINE
advanced_analytics = """# ADVANCED ANALYTICAL ENGINE (B2-B4)
**Phase B — Analytical Brain Extension**
**Depth Contract: FULL**

## COHORT & RETENTION ANALYSIS
- **Rule**: Always align the denominator (acquisition cohort size). 
- **Output**: Triangular matrix (absolute or %).
- **QA**: Ensure later periods with incomplete data are marked NA, not 0.

## FUNNEL ANALYSIS
- **Rule**: Distinguish between strictly ordered funnels (must complete Step 1 to do Step 2) and loose funnels.
- **QA**: Verify denominator logic (Total Users vs Users who reached previous step).

## FORECASTING ENGINE
- **Rule**: Never present a point forecast without a prediction interval (e.g., 80% and 95% bands).
- **Rule**: Decompose history into Trend, Seasonality, Residual before fitting.
- **QA**: Check for negative forecasts on strictly positive metrics (use log transform).

## SQL INTELLIGENCE
- **Rule**: Analytical SQL is about *grain management*.
- **Anti-Pattern**: Using `COUNT(id)` instead of `COUNT(DISTINCT id)` when joining across one-to-many relationships.
- **Anti-Pattern**: Forgetting `COALESCE` or `IFNULL` when doing outer joins for comparative analysis.
"""

# Write files
base_dir = "data-analyst-visualization-skill"
write_file(f"{base_dir}/visualization/chart-decision-engine.md", vis_engine)
write_file(f"{base_dir}/dashboards/dashboard-engine.md", dash_engine)
write_file(f"{base_dir}/quality/qa-and-critique-engine.md", qa_engine)
write_file(f"{base_dir}/proof/adversarial-cases.md", proof_engine)
write_file(f"{base_dir}/analytical/advanced-analytics-engine.md", advanced_analytics)
print("Deep implementation files created.")