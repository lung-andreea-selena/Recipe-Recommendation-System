import pandas as pd

clean_parquet_path = 'dataset/recipes_cleaned_spacy.parquet'
df_clean = pd.read_parquet(clean_parquet_path)
clean_csv_path = 'dataset/cleaned_recipes.csv'
df_clean.to_csv(clean_csv_path, index=False)
print("Conversion completed: Parquet files have been converted to CSV files.")
