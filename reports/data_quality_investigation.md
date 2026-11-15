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

### Return Rate Analysis

| KPI | Result |
|---|---:|
| Sales Value Return Rate | 3.72% |
| Unit Return Rate | 4.09% |

The unit return rate (4.09%) is slightly higher than the sales value return rate (3.72%). This suggests that returned units had a lower average transaction value than the overall units sold.

These metrics provide an initial view of merchandise returns and will be useful for further product performance analysis.

## Investigation of Extreme Product Returns

An investigation identified 40 product return records with
quantities of -1,000 units or lower.

Together, these records represent a transaction value of
-£285,136.11.

Three particularly large cancellation invoices were identified:

| Invoice | Products | Total Quantity | Return Value |
|---|---:|---:|---:|
| C541433 | 1 | -74,215 | -£77,183.60 |
| C550456 | 5 | -9,014 | -£22,998.40 |
| C581484 | 1 | -80,995 | -£168,469.60 |

The records contain valid product descriptions, prices and
customer identifiers. However, their unusually large quantities
require further investigation.

These records have been retained in the working dataset and
flagged for review. They have not been automatically removed.

### CRUK Commission

Sixteen CRUK Commission records were identified, with a combined
transaction value of -£7,933.43.

These represent financial/operational adjustments rather than
ordinary merchandise returns and are excluded from merchandise
sales calculations.

## Investigation of Extreme Product Returns

An investigation identified 40 product return records with
quantities of 1,000 units or more in absolute value.

These records were grouped into 13 invoices and represent a
combined transaction value of -£285,136.11.

This accounts for 39.36% of the total product return value
of -£724,473.06.

The impact is concentrated in a small number of invoices.
For example, invoice C581484 alone represents a return value
of -£168,469.60, while invoice C541433 represents
-£77,183.60.

Invoice C524235 contains multiple product lines, indicating
that some extreme returns may involve grouped product
cancellations or returns.

These records have been flagged for further investigation.
They have not been automatically removed because unusually
large quantities alone do not establish that a transaction
is invalid.

### Product and Customer Concentration

The 40 extreme product return records involve:

- 40 unique products
- 13 unique invoices
- 13 unique customers

Each extreme return record relates to a different product.
The exceptions are therefore not concentrated in a small
group of repeatedly returned products.

The largest two records involve PAPER CRAFT, LITTLE BIRDIE
and MEDIUM CERAMIC TOP STORAGE JAR. Together, they account
for approximately 86.2% of the total extreme-return value.

The findings suggest that a small number of unusually large
customer transactions have a substantial impact on reported
product returns.

The records remain flagged for further investigation and
have not been automatically excluded.

## Matching Extreme Returns to Earlier Sales

An investigation matched extreme product return records
against earlier sales using customer ID, product code and
transaction date.

All 13 extreme-return invoices had at least one earlier
sales candidate for the same customer and product.

Several returns had exact quantity matches with earlier
sales. For example:

- C541433: 74,215 units returned, matching an earlier sale
  of 74,215 units.
- C581484: 80,995 units returned, matching an earlier sale
  of 80,995 units.
- C524235: multiple returned product quantities matched
  quantities from an earlier bulk purchase.

Some returns had multiple candidate sales for the same
customer and product. Therefore, the matching results are
evidence of possible reversals, but do not independently
prove the original sale for every return.

All extreme-return records remain in the dataset pending
further reconciliation.

## Matching Extreme Returns to Earlier Sales

To investigate whether unusually large product returns could
represent reversals of earlier purchases, the 40 extreme-return
records were matched against earlier positive sales.

The matching criteria were:
- Same customer ID
- Same normalized product code
- Earlier sales transaction date
- Exact comparison of returned and previously sold quantities

### Findings

- 40 extreme-return records were investigated.
- 39 records (97.5%) had at least one earlier sales candidate.
- All 39 matched records had at least one candidate with an
  exact quantity match.
- One return record had no earlier sales candidate.

Some return records had multiple earlier sales candidates.
For example, certain customer-product combinations had more
than one previous purchase with a matching quantity.

These findings provide evidence that many extreme returns
may represent reversals of earlier purchases. However, an
exact quantity match alone does not establish a definitive
one-to-one relationship between the original sale and return.

The unmatched record and cases with multiple candidates
require further investigation. No extreme-return records
were automatically removed.

One return record could not be matched to an earlier positive
purchase in the customer's transaction history.

The unmatched record was invoice C550456 for TEA TIME PARTY
BUNTING (StockCode 47566B), involving 1,300 units with a
transaction value of -£3,315.00.

A further review of the customer's transaction history for
this product did not identify a corresponding positive
purchase.

This record has been flagged for further investigation.
It has been retained in the dataset because the absence
of a matching purchase does not, by itself, establish
that the return is invalid.
