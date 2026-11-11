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
4. Exact duplicate records were investigated across all eight columns. The investigation identified 32,907 duplicate groups containing 34,335 extra occurrences.
5. Negative quantities and cancellation invoice prefixes need to be examined together to understand transaction types.

### Cleaning Approach

Exact duplicate rows have been removed from a separate working dataset.
All other cleaning decisions are pending further investigation.

Further investigation will determine appropriate treatment for missing values, duplicate records, cancellations and unusual transactions.

## Duplicate Investigation and Cleaning

### Investigation Results

Exact duplicate records were identified by comparing all eight columns.

| Metric | Result |
|---|---:|
| Original records | 1,067,371 |
| Rows belonging to duplicate groups | 67,242 |
| Exact duplicate groups | 32,907 |
| Extra duplicate occurrences | 34,335 |

A detailed inspection of invoice `555524` confirmed that some product records appeared multiple times with identical values across all eight columns.

### Cleaning Decision

Exact duplicate rows were removed using Pandas `drop_duplicates()`.

One occurrence of each unique record was retained. Records with the same invoice and product but different transaction details were preserved.

### Cleaning Results

| Metric | Result |
|---|---:|
| Records before deduplication | 1,067,371 |
| Records removed | 34,335 |
| Records after deduplication | 1,033,036 |
| Remaining exact duplicates | 0 |

**Python method:** `DataFrame.drop_duplicates()`

**Note:** The original combined dataset was preserved as `df_all`. Deduplication was performed on a separate working dataset called `df_dedup`.

