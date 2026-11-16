import pandas as pd


def load_data(file_path):
    """Load and combine both Online Retail II worksheets."""

    sheets = [
        "Year 2009-2010",
        "Year 2010-2011"
    ]

    dataframes = [
        pd.read_excel(file_path, sheet_name=sheet)
        for sheet in sheets
    ]

    return pd.concat(dataframes, ignore_index=True)


def clean_data(df):
    """Remove exact duplicates and classify transactions."""

    df = df.drop_duplicates().copy()

    df["StockCode_norm"] = (
        df["StockCode"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["Description_norm"] = (
        df["Description"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["TransactionValue"] = df["Quantity"] * df["Price"]

    df["Transaction_Category"] = "Product"

    financial_codes = [
        "M", "D", "BANK CHARGES", "AMAZONFEE", "ADJUST"
    ]

    df.loc[
        df["StockCode_norm"].isin(financial_codes),
        "Transaction_Category"
    ] = "Financial / Operational Adjustment"

    delivery_codes = ["POST", "DOT", "C2"]

    df.loc[
        df["StockCode_norm"].isin(delivery_codes),
        "Transaction_Category"
    ] = "Delivery"

    df.loc[
        df["Description_norm"] == "NEXT DAY CARRIAGE",
        "Transaction_Category"
    ] = "Delivery"

    df.loc[
        (df["StockCode_norm"] == "S") |
        (df["Description_norm"] == "SHOW SAMPLES"),
        "Transaction_Category"
    ] = "Samples"

    inventory_adjustment_mask = (
        (df["Transaction_Category"] == "Product") &
        (df["Quantity"] < 0) &
        (~df["Invoice"].astype(str).str.startswith("C")) &
        (df["Price"] == 0) &
        (df["Customer ID"].isna())
    )

    df.loc[
        inventory_adjustment_mask,
        "Transaction_Category"
    ] = "Inventory / Damage Adjustment"

    return df
