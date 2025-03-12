import re
import pandas as pd
import os
from remove_measurements import remove_measurements

# # Load dataset
# DATASET_PATH = os.path.join(os.path.dirname(__file__), "../dataset/full_dataset.csv")
# df = pd.read_csv(DATASET_PATH)

# Function to clean text using regex
def clean_ingredients_regex(ingredient):
    ingredient = re.sub(r"\d+(\.\d+)?", "", ingredient)  # Remove numbers
    ingredient = re.sub(r"[^\w\s]", "", ingredient)  # Remove punctuation
    ingredient = remove_measurements(ingredient)  # Remove measurement words
    ingredient = ingredient.lower().strip()
    return ingredient

# df["cleaned_ingredients"] = df["ingredients"].apply(clean_ingredients_regex)
# df.to_csv("regex_cleaned.csv", index=False)
# print("Regex-based cleaning done. Results saved to regex_cleaned.csv")
