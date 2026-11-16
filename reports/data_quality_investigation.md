# Data Quality Investigation

## 1. Dataset Overview

The Online Retail II dataset contains transaction records from December 2009 to December 2011, covering two Excel worksheets.

- Original records: 1,067,371
- Exact duplicate records removed: 34,335
- Records after deduplication: 1,033,036

## 2. Data Quality Findings

| Issue | Records | Investigation |
|---|---:|---|
| Missing Customer ID | 243,007 | Limits customer-level analysis |
| Missing Description | 4,382 | Requires careful product identification |
| Exact duplicates | 34,335 | Removed to avoid double-counting |
| Negative quantities | 22,950 | Investigated as returns, cancellations or adjustments |
| Cancelled invoices | 19,494 | Identified using invoice prefixes |
| Negative quantity without cancellation prefix | 3,457 | Investigated separately |
| Negative prices | 5 | Identified as financial adjustments |

These issue counts describe the original investigation and may overlap. They should not be added together.

## 3. Transaction Classification

After deduplication, transactions were classified into five categories.

| Category | Records |
|---|---:|
| Product | 1,023,906 |
| Delivery | 3,868 |
| Inventory / Damage Adjustment | 3,392 |
| Financial / Operational | 1,768 |
| Samples | 102 |
| **Total** | **1,033,036** |

This classification separates merchandise sales from delivery charges, stock adjustments and other operational transactions.

## 4. Initial Sales Performance

The following results are based on product transactions.

| Metric | Value |
|---|---:|
| Gross merchandise sales | £19,497,760 |
| Product returns | £724,473 |
| Net merchandise sales | £18,773,290 |
| Sales value return rate | 3.72% |
| Unit return rate | 4.09% |

Net merchandise sales were calculated by deducting product return and cancellation values from gross merchandise sales.

## 5. Business Implications

Removing exact duplicates reduces the risk of overstating transaction volumes and revenue.

Separating merchandise transactions from operational adjustments makes product sales and return metrics more meaningful.

Missing customer identifiers limit customer-level analysis, so customer segmentation and retention results must be interpreted as representing identifiable customers rather than the entire customer population.

Negative quantities and cancellation records require careful classification to avoid treating all negative transactions as ordinary product returns.

## 6. Conclusion

The investigation established a consistent transaction classification and a validated foundation for product performance, customer behaviour and retention analysis.

The cleaning decisions improve the interpretability of business metrics while preserving important distinctions between sales, returns and operational adjustments.
