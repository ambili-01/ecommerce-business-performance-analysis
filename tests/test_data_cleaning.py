import pandas as pd

from src.data_cleaning import clean_data


def test_duplicate_removal():
    df = pd.DataFrame({
        "Invoice": ["100", "100"],
        "StockCode": ["22423", "22423"],
        "Description": ["Test Product", "Test Product"],
        "Quantity": [2, 2],
        "Price": [5.0, 5.0],
        "Customer ID": [12345, 12345]
    })

    result = clean_data(df)

    assert len(result) == 1
    assert result.duplicated().sum() == 0


def test_transaction_classification():
    df = pd.DataFrame({
        "Invoice": ["100", "101", "102", "103", "104"],
        "StockCode": ["22423", "POST", "M", "S", "22424"],
        "Description": [
            "Product", "Postage", "Manual",
            "Show Samples", "Damaged Product"
        ],
        "Quantity": [2, 1, 1, 1, -3],
        "Price": [5.0, 2.0, 1.0, 0.0, 0.0],
        "Customer ID": [12345, 12345, 12345, 12345, None]
    })

    result = clean_data(df)

    assert result["Transaction_Category"].tolist() == [
        "Product",
        "Delivery",
        "Financial / Operational Adjustment",
        "Samples",
        "Inventory / Damage Adjustment"
    ]


def test_transaction_value():
    df = pd.DataFrame({
        "Invoice": ["100"],
        "StockCode": ["22423"],
        "Description": ["Test Product"],
        "Quantity": [3],
        "Price": [4.5],
        "Customer ID": [12345]
    })

    result = clean_data(df)

    assert result["TransactionValue"].iloc[0] == 13.5
