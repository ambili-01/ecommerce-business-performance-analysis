from pathlib import Path

from src.data_cleaning import load_data, clean_data


def main():
    project_root = Path(__file__).resolve().parent
    input_path = project_root / "data" / "online_retail_II.xlsx"

    print("Loading Online Retail II dataset...")
    df = load_data(input_path)

    print("Original records:", len(df))

    print("Cleaning and classifying transactions...")
    cleaned_df = clean_data(df)

    print("Cleaned records:", len(cleaned_df))
    print("Duplicates removed:", len(df) - len(cleaned_df))

    print("\nTransaction categories:")
    print(cleaned_df["Transaction_Category"].value_counts())

    output_path = project_root / "data" / "processed" / "online_retail_cleaned.parquet"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Preserve invoice identifiers as strings for Parquet
    cleaned_df["Invoice"] = cleaned_df["Invoice"].astype("string")
    cleaned_df["StockCode"] = cleaned_df["StockCode"].astype("string")
    cleaned_df["Description"] = cleaned_df["Description"].astype("string")
    cleaned_df["Country"] = cleaned_df["Country"].astype("string")

    cleaned_df.to_parquet(
        output_path,
        engine="pyarrow",
        compression="snappy",
        index=False
    )

    print("\nCleaned dataset saved:", output_path)
    print("Exported records:", len(cleaned_df))

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
