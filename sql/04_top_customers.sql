SELECT
    CAST("Customer ID" AS BIGINT) AS Customer_ID,

    COUNT(DISTINCT CASE
        WHEN Quantity > 0 THEN Invoice
    END) AS Purchase_Invoices,

    ROUND(SUM(
        CASE WHEN Quantity > 0
        THEN TransactionValue ELSE 0 END
    ), 2) AS Gross_Sales,

    ROUND(SUM(
        CASE WHEN Quantity < 0
        THEN -TransactionValue ELSE 0 END
    ), 2) AS Returns_Value,

    ROUND(SUM(TransactionValue), 2) AS Net_Sales

FROM read_parquet('data/processed/online_retail_cleaned.parquet')

WHERE Transaction_Category = 'Product'
  AND "Customer ID" IS NOT NULL

GROUP BY "Customer ID"

HAVING COUNT(DISTINCT CASE
    WHEN Quantity > 0 THEN Invoice
END) > 0

ORDER BY Net_Sales DESC

LIMIT 10;
