import pandas as pd
import os

DATASET_PATH = os.path.join(os.path.dirname(__file__), "../dataset/full_dataset.csv")

# Cache the dataset in memory
df = pd.read_csv(DATASET_PATH)

def get_cached_dataset():
    return df  # Return the cached dataset
