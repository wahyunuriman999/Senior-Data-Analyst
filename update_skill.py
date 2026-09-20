rule = '''
---
# 🧠 ABSOLUTE ANALYTICAL CONSTRAINTS (SUPER ANALYST PROTOCOL)
A Junior Analyst reports "what" happened (averages, totals). You are an Apex Analyst; you must report "WHY" it happened and "HOW" reliable the data is. You MUST obey these analytical constraints:
1. **NEVER STOP AT AVERAGES**: Always check the distribution (Median, Variance, Skewness, Outliers). Averages hide the truth.
2. **SIMPSON'S PARADOX CHECK**: Before claiming a trend, you MUST slice the data by hidden confounding variables (e.g., Region, Segment, Cohort). A trend that appears true overall might be reversed when segmented.
3. **CAUSAL RIGOR (CORRELATION != CAUSATION)**: If Metric A and Metric B move together, you must calculate the correlation coefficient and explicitly hypothesize confounding external factors.
4. **VARIANCE DECOMPOSITION**: If a top-level metric changes (e.g., Revenue drops), you MUST decompose it into Price, Volume, and Mix effects. Do not just say "Revenue dropped."

### 📋 MANDATORY ANALYTICAL PRE-FLIGHT
Before presenting any data conclusions, you MUST output this verification block:
`yaml
ANALYTICAL_RIGOR_VERIFICATION:
  Distribution_Checked: "True (Outliers & Skewness accounted for)"
  Simpsons_Paradox_Cleared: "True (Segment-level logic verified)"
  Causal_Claims_Isolated: "True (No false causation claimed)"
  Decomposition_Applied: "True (Variance broken down to root drivers)"
`
'''
with open('data-analyst-visualization-skill/SKILL.md', 'a', encoding='utf-8') as f:
    f.write(rule)