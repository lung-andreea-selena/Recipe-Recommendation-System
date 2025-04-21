import pandas as pd

clean_parquet_path = 'dataset/recipes_cleaned_spacy.parquet'

# Read the Parquet files into DataFrames

df_clean = pd.read_parquet(clean_parquet_path)

# Define output CSV file paths

clean_csv_path = 'dataset/cleaned_recipes.csv'

# Convert DataFrames to CSV files (without the index)

df_clean.to_csv(clean_csv_path, index=False)

print("Conversion completed: Parquet files have been converted to CSV files.")
