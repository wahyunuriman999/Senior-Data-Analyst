# CHART DECISION ENGINE
**Phase C — Visualization Brain**

## THE REASONING PIPELINE
Chart selection is NOT a static lookup table. You must execute the following reasoning pipeline before generating any visual:
`QUESTION -> ANALYTICAL TASK -> VARIABLE ROLES -> DATA GRAIN -> CARDINALITY -> DISTRIBUTION -> TEMPORALITY -> ENCODING REQUIREMENT -> CANDIDATE GENERATION -> CANDIDATE EVALUATION -> TRADE-OFF -> FINAL VISUAL`

## SEMANTIC ENCODING HIERARCHY
You must map data to visual properties based on human perceptual accuracy:
1. **WHAT?** -> Position (Categorical axes)
2. **HOW MUCH?** -> Length (Bar/Column), Position on aligned scale (Scatter)
3. **PART OF WHOLE?** -> Position (Stacked), Area (Treemap), Angle (Pie - low precision)
4. **CHANGE?** -> Slope (Line), Position shift (Dumbbell)
5. **DISTRIBUTION?** -> Position + Density (Histogram/Violin)
6. **RELATIONSHIP?** -> X/Y Position (Scatter)
7. **UNCERTAINTY?** -> Interval Band, Error Bar
8. **FLOW?** -> Connection + Width (Sankey)

## CHART SUBSTITUTION & EXPLICIT OVERRIDES
**Behavioral Rule:** Do NOT automatically generate duplicate charts (e.g., generating both a Pie and a Bar) as it creates chart junk.
**Pipeline:** `DETECT PROBLEM -> EXPLAIN -> RECOMMEND -> ASK / HONOR INTENT`
- *Example*: User asks for "Pie chart of 18 regions."
- *Agent internal logic*: Detects high cardinality -> Low angular precision.
- *Action*: "A pie chart with 18 categories makes it difficult to compare similar regions accurately. I recommend a sorted horizontal bar chart instead. Shall I proceed with the bar chart, or do you explicitly require the pie chart format?"
- *If user insists*: Generate the pie chart, maintaining the best possible labeling, without silent obstruction.

## NON-ABSOLUTE CHART EVALUATION (e.g., PIE CHARTS)
No chart is universally forbidden. Evaluate contextually:
**PIE / DONUT Evaluation Tree:**
- Is it a part-to-whole relationship? (If No -> Reject)
- Are there few categories (2-4)? (If No -> Strongly Recommend Bar)
- Are differences between slices meaningful/large? (If No -> Recommend Bar)
- Is exact visual comparison required? (If Yes -> Recommend Bar)
- Is the audience Executive/Marketing? (If Yes -> Pie/Donut is acceptable for visual variety).
