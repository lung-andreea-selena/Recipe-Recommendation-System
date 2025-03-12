import pandas as pd

# Paths
csv_path = "../dataset/full_dataset.csv"
parquet_path = "../dataset/recipes.parquet"

print("Reading CSV (this may take a while)...")
df = pd.read_csv(csv_path)

print("Converting to Parquet (compressed)...")
df.to_parquet(parquet_path, engine="pyarrow", compression="snappy")

print(f"Successfully converted CSV to Parquet! File saved at: {parquet_path}")
#not used in the final code