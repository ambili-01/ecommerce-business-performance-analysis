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

## Negative Quantity Investigation

### 1. Non-cancelled Negative Quantities

A total of 3,393 records contain negative quantities without a cancellation prefix.

Key findings:
- All 3,393 records have missing Customer IDs.
- All 3,393 records have zero prices.
- Frequent descriptions include "damages", "damaged", "missing", "smashed", "thrown away" and "check".
- 2,633 records have missing descriptions.

**Interpretation:** These records appear to represent inventory adjustments or operational stock corrections rather than ordinary customer sales.

**Proposed treatment:** Exclude these records from standard sales revenue calculations while retaining them in the original dataset.

### 2. Cancelled Negative Quantities

A total of 19,103 records contain negative quantities and invoice numbers beginning with "C".

Frequent descriptions include product names, postage, manual entries, discounts, samples and bank charges.

**Interpretation:** These records represent a mixture of cancellation-related transactions and other adjustments. They require further investigation before final classification.

**Proposed treatment:** Preserve these records and investigate their prices and transaction types before defining the sales analysis dataset.

**Python method:** `DataFrame.drop_duplicates()`

**Note:** The original combined dataset was preserved as `df_all`. Deduplication was performed on a separate working dataset called `df_dedup`.

### 3. Price Investigation of Cancelled Transactions

The 19,103 negative-quantity records associated with cancellation-prefixed invoices were examined.

| Metric | Result |
|---|---:|
| Total records | 19,103 |
| Zero-price records | 0 |
| Positive-price records | 19,103 |
| Negative-price records | 0 |
| Median unit price | 2.95 |
| Minimum unit price | 0.01 |
| Maximum unit price | 38,970.00 |

**Interpretation:**

All records have positive unit prices and negative quantities. Their calculated transaction values are therefore negative.

This is consistent with sales reversals, returns or cancellation-related adjustments. However, the unusually high maximum price requires further investigation.

**Proposed treatment:** Retain these records in the transaction dataset and investigate unusual values before finalising the sales analysis rules.

### 4. Investigation of High-Value Cancellation Records

The highest-priced cancellation-related transactions were examined.

Unusual transaction descriptions and stock codes included:

- Manual (`M`)
- Bank Charges (`BANK CHARGES`)
- Amazon Fees (`AMAZONFEE`)
- Postage (`POST`)

Several records had unusually high unit prices, including a manual transaction of 38,970.00.

**Interpretation:**

The cancellation-related dataset contains non-product financial adjustments in addition to possible product returns.

**Proposed treatment:**

Separate non-product adjustments from ordinary product transactions. Do not automatically classify all cancellation-related records as customer returns or remove them from the original dataset.

### 5. Transaction Type Investigation

The negative-quantity transactions were grouped by stock code and product description.

Several non-product transaction types were identified:

| Transaction type | Records |
|---|---:|
| Manual | 533 |
| Postage | 228 |
| Discount | 168 |
| Samples | 98 |
| Bank Charges | 62 |

Additional investigation identified Amazon fees among the high-value cancellation-related transactions.

Some of these entries have unusually high transaction values and should not automatically be included in merchandise revenue calculations.

**Important observation:** Non-numeric stock codes do not necessarily represent non-product transactions. Some legitimate product codes contain letters, such as `85123A` and `79323W`.

**Proposed treatment:** Classify special financial and operational entries separately from catalogue products. Preserve legitimate product returns and investigate their effect on net sales.

### 6. Special Transaction Classification

The cancellation-related transaction analysis identified several non-product transaction categories.

| Category | Records | Total transaction value |
|---|---:|---:|
| Manual | 533 | -422,926.14 |
| Postage | 228 | -15,252.01 |
| Discount | 168 | -13,277.52 |
| Samples | 98 | -6,127.96 |
| Bank Charges | 66 | -36,001.49 |
| Amazon Fees | 33 | -241,988.30 |

The analysis also identified numerous negative-quantity records associated with catalogue products.

**Cleaning decisions:**

- Separate financial and operational adjustments from merchandise transactions.
- Preserve catalogue product returns and cancellations.
- Retain the original dataset.
- Avoid excluding records solely because their stock codes contain letters.
- Investigate special transaction types across the complete dataset before finalising the classification rules.

## Initial Sales Performance

After investigating and classifying transaction records, an initial merchandise sales analysis was performed.

### Sales Performance Summary

| Metric | Value |
|---|---:|
| Gross Sales Value | £19,497,760 |
| Returns Value | £724,473.10 |
| Net Sales Value | £18,773,286.90 |
| Gross Units Sold | 11,431,970 |
| Returned Units | 467,761 |
| Net Units Sold | 10,964,209 |
| Sales Transactions | 1,005,971 |
| Return Transactions | 17,935 |

### Business Interpretation

- Gross sales represent the total value of positive-quantity merchandise transactions.
- Returns value represents the value reversed through negative-quantity merchandise transactions.
- Net sales value is calculated by subtracting returns value from gross sales value.
- Net units sold are calculated by subtracting returned units from gross units sold.

**Formula:**

Net Sales Value = Gross Sales Value − Returns Value

### Analysis Scope

This analysis includes merchandise transactions only. Delivery charges, samples, financial and operational adjustments, and inventory/damage adjustments are excluded from merchandise sales calculations.

These results provide the baseline for further analysis of monthly sales trends, product performance, and country-level sales.
