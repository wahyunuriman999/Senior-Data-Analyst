# Chart Decision Engine
Do NOT rely on static rules. Use the reasoning chain:
1. Determine analytical task (Compare, Distribute, Correlate, Flow).
2. Determine data grain and cardinality.
3. Determine temporal structure.
4. Determine precision requirement (e.g., length vs. area).
5. Generate candidate visuals.
6. Score internally and reject unsuitable ones.
