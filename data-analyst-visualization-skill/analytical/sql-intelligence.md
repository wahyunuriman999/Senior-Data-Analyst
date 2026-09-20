# SQL INTELLIGENCE ENGINE
**Phase B — Analytical Brain Extension**

## PURPOSE
Analytical SQL is about reasoning, not syntax. The AI must manage grain, join paths, and denominator integrity.

## SQL REASONING PATTERNS
### 1. Common Table Expressions (CTEs)
- **Why**: Modularity, avoiding nested subquery hell, controlling execution context.
- **Rule**: Use CTEs to isolate aggregations *before* joining to fact tables to prevent Cartesian fan-out.

### 2. Date Spine / Calendar Tables
- **Why**: Handling missing periods in time series.
- **Rule**: If querying daily active users, do NOT just group by `event_date`. Left join a Date Spine to the grouped data to ensure days with 0 events show as `0`, not missing rows.

### 3. Window Functions
- **LAG / LEAD**: Mandatory for WoW, MoM, YoY calculations.
  - *Failure Mode*: Sorting incorrectly in the `OVER` clause.
- **ROW_NUMBER()**: Mandatory for deduplication.
  - *Grain Rule*: Partition by unique entity ID, order by timestamp desc, filter `WHERE rn = 1`.

### 4. Cohort & Retention SQL
- **Pattern**: `user_id`, `cohort_month` (min date), `activity_month`.
- **Validation**: The denominator (users in cohort) must remain constant across the row, derived from the `cohort_month` total, not the `activity_month` subset.

### 5. Funnel SQL
- **Pattern**: Self-joins or conditional aggregation (`COUNT(CASE WHEN step=1 THEN id END)`).
- **Rule**: Differentiate strict funnels (must have timestamp of step 2 > step 1) vs loose funnels (any occurrence).
