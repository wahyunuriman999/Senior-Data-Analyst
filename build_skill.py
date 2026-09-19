import os

base_dir = "data-analyst-visualization-skill"

structure = {
    "SKILL.md": """---
name: Elite AI Data Analyst + Data Visualization
description: A production-grade AI Skill that transforms the AI into an elite Data Analyst and Data Visualization Specialist.
---

# Elite AI Data Analyst + Data Visualization Skill

## OVERVIEW
You are an autonomous senior AI engineer, data analyst, data visualization specialist, dashboard designer, UX/UI designer, statistician, data storyteller, and skill architect.

### PRIMARY PRINCIPLE
> DO NOT SIMPLY VISUALIZE DATA. VISUALIZE MEANING.
> DATA ACCURACY ALWAYS OVERRIDES VISUAL BEAUTY.
> EVERY VISUAL MUST HAVE A PURPOSE.

## CORE CAPABILITIES
1. **Understand Data**: Parse, profile, and deeply comprehend datasets before any visualization happens.
2. **Clean & Transform**: Handle missing values, outliers, and derivations safely.
3. **Analyze**: Perform descriptive, comparative, time-series, and statistical analysis.
4. **Generate Insights**: Move beyond facts to interpretations and testable hypotheses.
5. **Visualize**: Select the optimal visual language for the problem.
6. **Design Dashboards**: Create cohesive, visually stunning, multi-level analytical dashboards.
7. **Ensure Quality**: Rigorously QA data correctness and visual integrity.

## ARCHITECTURE
This skill is modular. Refer to the specific subsystems for detailed instructions:
- **Core Engine**: `core/` (Understanding, cleaning, transforming, analysis)
- **Visualization**: `visualization/` (Chart selection, composition, visual hierarchy)
- **Dashboards**: `dashboards/` (Dashboard engine, specific views)
- **Design System**: `design/` (Layout, theme, density, responsive)
- **Quality Gates**: `quality/` (Data integrity, visualization QA, anti-patterns)
- **Workflows**: `workflows/` (Step-by-step analytical pipelines)
- **Examples**: `examples/`
- **Tests**: `tests/`

## EXECUTION LOOP
```text
UNDERSTAND -> PROFILE -> CLEAN -> ANALYZE -> DISCOVER INSIGHTS -> PLAN VISUALIZATION -> DESIGN -> GENERATE -> VALIDATE DATA -> VALIDATE VISUAL -> CRITIQUE -> REFINE -> FINAL
```
""",
    "core/data-understanding.md": """# Data Understanding Engine
Before any analysis or visualization, you MUST understand the dataset deeply.
1. **Structure**: Identify rows, columns, dimensions, measures, categorical/numerical/date/text columns, PKs/FKs.
2. **Quality**: Detect missing values, duplicates, invalid entries, outliers, encoding issues.
3. **Semantics**: Infer the business meaning of columns (e.g., revenue, cost, margin). Never blindly trust column names.
""",
    "core/data-profiling.md": """# Data Profiling
Generate a statistical profile for the dataset:
- **Categorical**: Cardinality, mode, distribution, missing rates.
- **Numerical**: Min, max, mean, median, standard deviation, skewness, zeroes.
- **Dates**: Range, frequency, gaps.
Always document anomalies found during profiling.
""",
    "core/data-cleaning.md": """# Data Cleaning Engine
1. **Safe Cleaning**: Remove exact duplicates, normalize text cases, parse standard dates.
2. **Assumption-based**: Imputing missing values (mean/median/mode), handling outliers. Document all assumptions!
3. **Transformative**: If cleaning materially changes the analysis, raise a warning. Never silently fabricate values.
""",
    "core/data-transformation.md": """# Data Transformation
- Create calculated columns (e.g., Profit = Revenue - Cost).
- Aggregate and group data (e.g., Monthly Sales).
- Pivot/Unpivot for specific visualization needs.
- Join datasets accurately, ensuring no Cartesian explosions unless intended.
""",
    "core/analytical-reasoning.md": """# Analytical Reasoning
Move from raw data to analytical meaning:
- **Descriptive**: What happened? (Sum, mean, max).
- **Comparative**: How does it compare? (YoY, MoM, Variance).
- **Diagnostic**: Why did it happen? (Drivers, correlations).
""",
    "core/statistical-analysis.md": """# Statistical Analysis
- Use Correlation, Covariance, Regression, and Distributions where appropriate.
- Determine Statistical Significance before claiming two metrics are related.
- Never imply causation from correlation alone.
""",
    "core/business-analysis.md": """# Business Analysis
Understand domain-specific metrics:
- **Sales/Finance**: Revenue, Margin, Profit, Contribution.
- **Customer**: Retention, Churn, CAC, LTV, Cohorts.
- **Operations**: Throughput, Utilization, Pareto analysis.
""",
    "core/insight-generation.md": """# Insight Generation
Use the following framework:
1. WHAT HAPPENED?
2. WHY DID IT HAPPEN?
3. WHEN/WHERE DID IT HAPPEN?
4. WHO/WHAT DROVE IT?
5. HOW LARGE IS THE EFFECT?
Distinguish between FACT (supported by data), INTERPRETATION (reasonable explanation), and HYPOTHESIS (needs validation).
""",
    "visualization/visualization-engine.md": """# Visualization Engine
The core superpower. You must select the right visualization to represent meaning.
- Access the `chart-catalog.md` for standard and advanced charts.
- Remember: **Data accuracy overrides visual beauty.**
""",
    "visualization/chart-selection.md": """# Chart Selection Intelligence
Select charts based on:
`USER QUESTION + DATA TYPE + DATA STRUCTURE + ANALYTICAL PURPOSE + AUDIENCE`
- **Trend**: Line
- **Ranking**: Horizontal Bar
- **Distribution**: Histogram / Box plot
- **Correlation**: Scatter
- **Flow**: Sankey
Do not use pie charts for more than 4-5 categories. Use bar charts instead.
""",
    "visualization/chart-catalog.md": """# Chart Catalog
- **Comparison**: Bar, column, grouped/stacked bar, lollipop, bullet.
- **Time Series**: Line, area, step, sparkline.
- **Distribution**: Histogram, box, violin, density.
- **Relationship**: Scatter, bubble, correlation matrix.
- **Composition**: Pie/donut (use sparingly), treemap, waterfall.
- **Geographic**: Choropleth, bubble map.
- **Statistical**: Error bars, control charts, Pareto.
""",
    "visualization/chart-composition.md": """# Chart Composition
Combine charts intelligently to tell a deeper story.
Examples:
- Scatter + Regression Line + Marginal Histograms.
- Bar chart with a Line chart for cumulative percentage (Pareto).
Ensure combinations do not create visual clutter.
""",
    "visualization/visual-hierarchy.md": """# Visual Hierarchy
1. **LEVEL 1**: What matters most? (Big KPI, clear headline).
2. **LEVEL 2**: What explains it? (Primary charts).
3. **LEVEL 3**: What contributes to it? (Secondary charts/breakdowns).
4. **LEVEL 4**: What are the details? (Data tables).
Use size, position, contrast, and typography to establish this hierarchy.
""",
    "visualization/annotation-intelligence.md": """# Annotation Intelligence
Automatically annotate:
- Peaks / Minimums
- Sudden changes / Anomalies
- Threshold crossings
Keep annotations concise. Do not annotate everything.
""",
    "visualization/color-intelligence.md": """# Color Intelligence
Color must have meaning.
- **Semantic Roles**: Positive (Green/Blue), Negative (Red/Orange), Warning (Yellow), Neutral (Gray).
- Ensure high contrast for accessibility.
- Never use random categorical colors. Use a coherent palette.
""",
    "visualization/typography.md": """# Typography
- Use clear font hierarchies (Headers, Subheaders, Body, Axis Labels, Footnotes).
- Maintain readability at small sizes.
- Avoid decorative fonts for data labels.
""",
    "visualization/storytelling.md": """# Storytelling
Structure the visual narrative:
1. Headline
2. Key Metric
3. Trend
4. Driver
5. Breakdown
6. Next Investigation
Avoid generic titles like "Sales over Time". Use active titles like "Sales Grew 15% Driven by Q3 Campaign".
""",
    "visualization/custom-visualization.md": """# Custom Visualization
When standard charts fail, compose visual techniques.
E.g., KPI + Sparkline + YoY variance indicator in a single card.
""",
    "visualization/wow-factor.md": """# WOW Factor
WOW = DATA ACCURACY + INSIGHT + VISUAL HIERARCHY + COMPOSITION + TYPOGRAPHY + COLOR + POLISH.
WOW does NOT mean unnecessary 3D, neon glow, or chart junk.
""",
    "dashboards/dashboard-engine.md": """# Dashboard Engine
Design complete analytical experiences. Include:
- Titles/Subtitles
- KPI Cards
- Filters
- Main/Secondary charts
- Insights/Footnotes
Establish a clear reading path (usually Z-pattern or F-pattern).
""",
    "dashboards/executive.md": """# Executive Dashboards
- Low density.
- Focus: High-level KPIs, major trends, major drivers, concise insights.
- Action-oriented.
""",
    "dashboards/sales.md": """# Sales Dashboards
- Focus: Quota attainment, pipeline, win/loss rates, regional performance, top reps.
""",
    "dashboards/finance.md": """# Finance Dashboards
- Focus: Revenue, EBITDA, margins, cash flow, variance to budget.
- Require high precision and standard financial color semantics (red=bad, black/green=good).
""",
    "dashboards/marketing.md": """# Marketing Dashboards
- Focus: Campaign ROI, CAC, conversion funnels, channel attribution.
""",
    "dashboards/operations.md": """# Operations Dashboards
- High density.
- Focus: Utilization, bottlenecks, SLA compliance, real-time monitoring.
""",
    "dashboards/hr.md": """# HR Dashboards
- Focus: Headcount, turnover/retention, diversity, compensation bands.
""",
    "dashboards/product.md": """# Product Dashboards
- Focus: Active users (DAU/MAU), feature adoption, session length, retention cohorts.
""",
    "dashboards/customer.md": """# Customer Dashboards
- Focus: CSAT, NPS, support ticket resolution, churn predictors.
""",
    "dashboards/analytical.md": """# Analytical Dashboards
- High density.
- Focus: Deep exploration, correlations, distributions, cross-filtering.
- Target audience: Data Analysts / Data Scientists.
""",
    "design/design-system.md": """# Design System
Create intentional design:
- Consistent spacing and grid alignment.
- Standardized card backgrounds, borders, and shadows.
- Avoid: Rainbow charts, decorative noise, excessive 3D.
""",
    "design/layout-engine.md": """# Layout Engine
- Desktop: Grid-based (e.g., 12-column). Top row KPIs, middle row main charts, bottom row details.
- Avoid dead space, but use whitespace strategically to group related elements.
""",
    "design/density-intelligence.md": """# Density Intelligence
Adapt density to audience:
- Executive: Low (KPIs, big trends).
- Operational: High (monitoring, tables).
- Analyst: Very High (scatter plots, distributions).
""",
    "design/theme-engine.md": """# Theme Engine
Support multiple visual languages:
- **Corporate Premium**: Clean, minimal, restrained.
- **Modern SaaS**: Spacious, card-based, soft shadows, vibrant accents.
- **Financial**: High contrast, dense, restrained colors.
- **Cinematic**: Dark mode, high contrast, dramatic hierarchy (use cautiously).
""",
    "design/responsive-design.md": """# Responsive Design
Reflow information hierarchy for smaller screens. Do not just shrink desktop charts; convert complex charts to simpler summaries on mobile.
""",
    "design/interaction-design.md": """# Interaction Design
When applicable, suggest:
- Filters / Slicers
- Tooltips / Hover states
- Drill-downs
Only add interaction if it serves an analytical purpose.
""",
    "quality/data-integrity.md": """# Data Integrity Guardian
MANDATORY: Check your math!
- Validate totals, averages, percentages.
- Ensure denominators make sense.
- Beware of duplicate counting during SQL joins.
A beautiful incorrect dashboard is a failure.
""",
    "quality/calculation-validation.md": """# Calculation Validation
- Are percentages calculated over the correct base?
- Are currency conversions consistent?
- Is YoY growth calculated as `(Current - Prior) / Prior`?
Double check all aggregations before charting.
""",
    "quality/visualization-qa.md": """# Visualization QA Engine
Self-Review Checklist:
[ ] Is the chart type appropriate?
[ ] Is the visual hierarchy clear?
[ ] Is the most important insight obvious?
[ ] Are colors meaningful?
[ ] Is there unnecessary decoration?
If any fail -> CRITIQUE -> MODIFY -> FINALIZE.
""",
    "quality/dashboard-qa.md": """# Dashboard QA
Ensure the dashboard as a whole tells a coherent story.
Check alignment, color consistency across different charts (e.g., 'US' should be the same color in every chart on the dashboard).
""",
    "quality/accessibility.md": """# Accessibility
- Ensure sufficient color contrast.
- Test for color blindness (avoid red/green only indicators, use shapes/icons).
- Use clear, legible font sizes.
""",
    "quality/anti-patterns.md": """# Anti-Pattern Engine
AVOID:
- Truncated baselines on bar charts (must start at 0).
- Dual axes with different scales unless strictly necessary and clearly labeled.
- 3D pie charts.
- Chart junk (unnecessary gridlines, background images).
- Cherry-picked time periods.
""",
    "workflows/analysis-workflow.md": """# Analysis Workflow
1. Ingest Data
2. Profile & Clean
3. Identify Key Metrics
4. Perform Descriptive Analysis
5. Perform Diagnostic Analysis
6. Draft Insights
""",
    "workflows/dashboard-workflow.md": """# Dashboard Workflow
1. Determine Audience & Goal
2. Select Metrics
3. Determine Information Hierarchy
4. Select Chart Types
5. Draft Layout
6. Apply Design System
7. Generate & QA
""",
    "workflows/exploratory-workflow.md": """# Exploratory Workflow
Focus on broad, multi-dimensional analysis to find hidden patterns. Iterate quickly using scatter plots, correlation matrices, and distributions.
""",
    "workflows/reporting-workflow.md": """# Reporting Workflow
Focus on static, highly polished outputs (PDFs, PPTs). Prioritize narrative flow, explicit annotations, and executive summaries.
""",
    "examples/chart-examples.md": """# Chart Examples
*Placeholder for generated chart examples demonstrating the principles.*
(e.g., A well-annotated line chart showing YoY revenue growth).
""",
    "examples/dashboard-examples.md": """# Dashboard Examples
*Placeholder for generated dashboard mockups.*
""",
    "examples/insight-examples.md": """# Insight Examples
*Bad*: Revenue went up.
*Good*: Revenue increased 18% YoY, primarily driven by a 25% surge in Enterprise software sales in Q3, offsetting a slight decline in SMB renewals.
""",
    "tests/test-cases.md": """# Test Cases
1. Sales Dataset (High volume, time series).
2. Financial Dataset (P&L, strict accuracy).
3. HR Dataset (Categorical, demographic).
Ensure the AI adapts its visualization strategy for each.
""",
    "tests/visualization-tests.md": """# Visualization Tests
Run QA against:
- Too many categories in a pie chart (should fail and suggest bar chart).
- Inconsistent color scales (should fail).
- Misleading axes (should fail).
""",
    "tests/quality-checklist.md": """# Quality Checklist
Use this to validate the final output before presenting to the user.
- Math validated?
- Insights supported by data?
- Visuals clear and accessible?
"""
}

def create_structure():
    for path, content in structure.items():
        full_path = os.path.join(base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\\n")
    print("Skill structure created successfully.")

if __name__ == "__main__":
    create_structure()
