import re
import os
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from remove_measurements import clean_ingredient


# nltk.download("punkt")
# nltk.download("wordnet")
# nltk.download("stopwords")

# Initialize lemmatizer and stopwords only once
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Paths
DATASET_PATH = os.path.join(os.path.dirname(__file__), "../dataset/recipes.parquet")
OUTPUT_PATH_LIGHT = os.path.join(os.path.dirname(__file__), "../dataset/nltk_cleaned_light.parquet")

def clean_ingredients_nltk(ingredient):
    """Cleans ingredient text using NLTK (tokenization, stopword removal, lemmatization)."""
    if not isinstance(ingredient, str):  # Ensure ingredient is a string
        return ""
    ingredient = clean_ingredient(ingredient)  # Remove measurement and other words
    words = word_tokenize(ingredient.lower())  # Tokenization
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]  # Lemmatization & Stopword removal
    return " ".join(words)

def process_dataset_in_chunks(chunk_size=5000):
    """Processes dataset in chunks and writes the cleaned data into a single Parquet file."""
    print(f"Processing dataset in chunks of {chunk_size}...")

    # Load the entire dataset (ensure it contains the 'recipe_id' and 'ingredients' columns)
    df = pd.read_parquet(DATASET_PATH, engine="pyarrow", columns=["recipe_id", "ingredients"])
    
    if "ingredients" not in df.columns:
        raise ValueError("ERROR: 'ingredients' column not found in dataset!")

    # Ensure the 'ingredients' column is treated as string
    df["ingredients"] = df["ingredients"].astype(str)
    
    cleaned_chunks = []
    # Split the dataframe into chunks
    for start in range(0, len(df), chunk_size):
        end = start + chunk_size
        chunk = df.iloc[start:end].copy()
        chunk["cleaned_ingredients"] = chunk["ingredients"].apply(clean_ingredients_nltk)
        cleaned_chunks.append(chunk[["recipe_id", "cleaned_ingredients"]])
        print(f"Processed chunk from index {start} to {end}.")

    # Concatenate all processed chunks and save to a single parquet file
    cleaned_df = pd.concat(cleaned_chunks, ignore_index=True)
    cleaned_df.to_parquet(OUTPUT_PATH_LIGHT, engine="pyarrow", compression="snappy", index=False)
    print(f"Cleaning complete! Dataset saved at: {OUTPUT_PATH_LIGHT}")

# Run the processing function when the script is executed
if __name__ == "__main__":
    process_dataset_in_chunks()