# Real Self-Critique Loop

Execute this explicit protocol on EVERY output before shipping. It is not
optional, and it is not a vibe — each step produces a written record in the
YAML schema from `qa-and-critique-engine.md` (UPGRADED SELF-CRITIQUE SCHEMA).

## The 6 steps

1. **CRITIQUE** — State what is wrong, concretely. Name the element, not the feeling.
   Bad: "The dashboard feels off." Good: "The trend line has 15 series — spaghetti."
2. **WHY** — Name the violated rule (check ID from `qa-matrices.md`).
   Good: "Violates Q-VIS-001 chart fit and readability limits."
3. **SEVERITY** — Critical / Major / Minor / Info. Critical or Major blocks shipping.
4. **FIX** — The smallest change that resolves the root cause, not the symptom.
   Good: "Faceted small-multiples, one panel per top-5 category, rest in 'Other'."
5. **RENDER & COMPARE** — Re-render and compare side by side. The fix must
   measurably improve comprehension (fewer overlapping labels, faster insight).
   A fix without re-render is NOT VERIFIED.
6. **PASS** — Ship only when zero Critical/Major issues remain. Record the
   schema block as evidence.

## Worked example

```yaml
ISSUE:
  Category: Visualization
  Severity: Major
  Evidence: Donut chart renders 14 slices; smallest 4 slices < 2% each, labels collide
  Impact: Reader cannot distinguish or compare the small categories (Q-VIS-005)
  Fix: Top-6 categories as slices, remainder grouped as "Lainnya" with exact value in tooltip
  Retest: Re-rendered; 7 slices, no label collision, percentages sum to 100%
  RetestEvidence: validator V-DONUT-SLICES=7 <= 7 → PASS
  Status: PASS
```

## Stop conditions

- STOP and escalate to the user when: the data cannot support the requested
  visual (e.g. asked for a forecast with n < 6 periods), or two QA rules
  conflict and the trade-off needs a human decision.
- NEVER "fix" by deleting the inconvenient data. Fix the encoding, not the evidence.
