# QA & SELF-CRITIQUE ENGINE
**Phase F — Quality Brain**

## OPERATIONAL QA CHECKS
Instead of a simple checklist, use explicit operational definitions for every check:

### Q1: Join Grain Integrity
- **CHECK**: Does the join multiply rows unexpectedly?
- **INPUT**: Left row count, Right row count, Join keys.
- **FAIL CONDITION**: Output rows > Left rows (in a Many-to-One intent).
- **SEVERITY**: CRITICAL.
- **FIX**: Pre-aggregate the Many side, or use a bridge table.
- **RETEST**: Reconcile a core measure (e.g., SUM(revenue)) pre and post join.

### Q2: Percentage vs Percentage-Point
- **CHECK**: Correct terminology for rate changes.
- **FAIL CONDITION**: Saying "increased by 2%" when moving from 10% to 12%.
- **SEVERITY**: MAJOR.
- **FIX**: Rewrite to "increased by 2 percentage points" or "increased by 20% relative".

## SELF-CRITIQUE SCHEMA
Before presenting the final analytical artifact, the AI must internally generate a critique using this strict schema:
```yaml
ISSUE:
  Category: [Data | Calculation | Statistical | Visual | Design | Story]
  Severity: [Critical | Major | Minor | Info]
  Evidence: [What specifically triggered this?]
  Impact: [How does this mislead the user?]
  Fix: [What action was taken to correct it?]
  Status: [PASS | FAIL]
```
If ANY Critical or Major issue remains FAIL, the AI must NOT output the artifact to the user. Fix it first.
