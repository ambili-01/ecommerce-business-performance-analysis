# Data Quality Investigation

## Initial Findings

The combined dataset contains 1,067,371 transaction records across eight columns.

### Identified Data Quality Issues

| Issue | Records |
|---|---:|
| Missing Customer IDs | 243,007 |
| Missing Descriptions | 4,382 |
| Duplicate occurrences | 34,335 |
| Negative quantities | 22,950 |
| Negative prices | 5 |
| Cancelled invoice records | 19,494 |
| Negative quantities without cancellation prefix | 3,457 |

### Initial Observations

1. Missing Customer IDs may limit customer-level analysis but do not necessarily invalidate sales records.
2. Negative quantities without a cancellation prefix include descriptions suggesting damaged, lost or adjusted inventory.
3. Five negative-price records are labelled as bad-debt adjustments.
4. Duplicate transaction records require further investigation before removal.
5. Negative quantities and cancellation invoice prefixes need to be examined together to understand transaction types.

### Cleaning Approach

No records have been removed at this stage.

Further investigation will determine appropriate treatment for missing values, duplicate records, cancellations and unusual transactions.
