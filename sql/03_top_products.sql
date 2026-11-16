SELECT
    StockCode_norm AS StockCode,
    MAX(Description_norm) AS Description,

    ROUND(SUM(
        CASE WHEN Quantity > 0
        THEN TransactionValue ELSE 0 END
    ), 2) AS Gross_Sales,

    ROUND(SUM(
        CASE WHEN Quantity < 0
        THEN -TransactionValue ELSE 0 END
    ), 2) AS Returns_Value,

    ROUND(SUM(TransactionValue), 2) AS Net_Sales,

    COUNT(DISTINCT CASE
        WHEN Quantity > 0 THEN Invoice
    END) AS Sales_Invoices

FROM read_parquet('data/processed/online_retail_cleaned.parquet')

WHERE Transaction_Category = 'Product'

GROUP BY StockCode_norm

ORDER BY Net_Sales DESC

LIMIT 10;
