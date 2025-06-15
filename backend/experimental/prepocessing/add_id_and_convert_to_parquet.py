import pandas as pd
import os

DATASET_PATH = os.path.join(os.path.dirname(__file__), "../dataset/full_dataset.csv")
OUTPUT_PARQUET_PATH = os.path.join(os.path.dirname(__file__), "../dataset/recipes.parquet")

def add_recipe_id():
    df = pd.read_csv(DATASET_PATH)

    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    if "recipe_id" not in df.columns:
        df = df.reset_index(drop=True)
        df.insert(0, "recipe_id", df.index)

    df.to_parquet(OUTPUT_PARQUET_PATH, engine="pyarrow", compression="snappy", index=False)
    print(f" Full dataset saved with correct recipe_id at: {OUTPUT_PARQUET_PATH}")

if __name__ == "__main__":
    add_recipe_id()
