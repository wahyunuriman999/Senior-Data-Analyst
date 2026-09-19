# Join Audit Protocol
MANDATORY before merging datasets:
1. **Before**: Check row count, unique keys, and grain of both tables.
2. **After**: Check row count. If it increased, did you expect a 1-to-many relationship? 
3. **Check**: Duplicate keys, null expansion, measure inflation (fan-out).
4. **Reconciliation**: Sum a critical measure before and after the join to ensure it hasn't artificially inflated.
