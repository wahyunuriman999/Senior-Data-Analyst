# DASHBOARD & DESIGN ENGINE
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
