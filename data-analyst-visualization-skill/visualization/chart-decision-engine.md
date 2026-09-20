# VISUAL DECISION ENGINE

## REASONING PIPELINE
`QUESTION -> TASK -> ROLES -> GRAIN -> CARDINALITY -> TEMPORALITY -> CANDIDATES -> EVALUATION -> FINAL`

## CANDIDATE EVALUATION SCHEMA
Do not use a simple numeric score as the sole decision mechanism. Evaluate candidates explicitly:

```yaml
candidate:
  chart: [e.g., Pie Chart]
  semantic_fit: [High/Med/Low]
  precision: [Low - angles are hard to compare]
  cardinality_fit: [Fail - 18 categories]
  temporal_fit: [N/A]
  audience_fit: [High - Executive]
  density: [Poor - labels will overlap]
  accessibility: [Poor - relies on 18 colors]
  strengths: [Familiar to executives]
  weaknesses: [Analytically misleading for this N]
  score: [Reject]
```
Final reasoning must explicitly explain the trade-offs that led to the selection.
