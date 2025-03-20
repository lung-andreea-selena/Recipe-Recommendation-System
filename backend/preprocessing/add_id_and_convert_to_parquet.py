#no need to use this function anymore, as the dataset is already saved with the correct recipe_id

import pandas as pd
import os

# Paths
DATASET_PATH = os.path.join(os.path.dirname(__file__), "../dataset/full_dataset.csv")
OUTPUT_PARQUET_PATH = os.path.join(os.path.dirname(__file__), "../dataset/recipes.parquet")

def add_recipe_id():
    """Adds a unique recipe_id to the full dataset and removes unwanted columns."""
    df = pd.read_csv(DATASET_PATH)  # Load the full dataset

    # Remove any unnamed columns if they exist
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # If 'recipe_id' does not exist, create one using the DataFrame index
    if "recipe_id" not in df.columns:
        df = df.reset_index(drop=True)  # Drop the existing index
        df.insert(0, "recipe_id", df.index)  # Add recipe_id as the first column

    df.to_parquet(OUTPUT_PARQUET_PATH, engine="pyarrow", compression="snappy", index=False)
    print(f" Full dataset saved with correct recipe_id at: {OUTPUT_PARQUET_PATH}")

# Run the function
if __name__ == "__main__":
    add_recipe_id()
