# Comprehensive Test Suites
Execute these tests to validate the Apex Analyst:
- **High Cardinality Test**: Force the engine to visualize 50 categories. It MUST reject a pie chart and output a searchable table, small multiples, or top-N Pareto chart.
- **Missing Data Test**: Pass a dataset with 40% missing revenue. It MUST NOT impute with mean; it must isolate the missingness pattern (MNAR) and flag it.
- **Adversarial Chart Request**: User requests a 3D dual-axis pie chart. The engine MUST politely refuse, explain the visual grammar violations, and provide a superior alternative (e.g., grouped bar chart).
