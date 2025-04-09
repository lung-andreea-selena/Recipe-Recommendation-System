import pandas as pd
import spacy
import os
import time

nlp = spacy.load("en_core_web_sm")

DATASET_PATH = os.path.join(os.path.dirname(__file__), "../dataset/recipes.parquet")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../dataset/recipes_cleaned_spacy.parquet")

total_start = time.time()

UNWANTED_NOUNS = set([
    "can", "pkg", "package", "oz", "ounce", "bag", "container", "cup", "quart", "pint", "jar",
    "bottle", "box", "envelope", "stick", "slice", "serving", "packet", "lb", "pound", "gallon",
    "tablespoon", "tbsp", "teaspoon", "tsp", "dash", "pinch", "clove", "head", "bunch", "sprig",
    "size", "small", "medium", "large", "extra", "bite", "bite-size", "chopped", "shredded",
    "diced", "minced", "frozen", "fresh", "lean", "fat", "boneless", "skinless", "prepared",
    "uncooked", "raw", "melted", "cooked", "grated", "sliced", "divided", "softened", "refrigerated",
    "optional", "thawed", "warm", "cold", "room", "temperature", "cut", "inch", "thick"
])

def clean_ingredients_spacy_pos(text):
    doc = nlp(text)
    return " ".join([
        token.lemma_.lower()
        for token in doc
        if token.pos_ in ["NOUN", "PROPN"]
        and token.lemma_.lower() not in UNWANTED_NOUNS
        and token.is_alpha
    ])

df_full = pd.read_parquet(DATASET_PATH, engine="pyarrow", columns=["recipe_id", "ingredients"])

chunk_size = 5000
num_chunks = (len(df_full) + chunk_size - 1) // chunk_size
all_chunks = []

for i in range(num_chunks):
    print(f"Processing chunk {i+1}/{num_chunks}...")
    start_idx = i * chunk_size
    end_idx = min((i + 1) * chunk_size, len(df_full))
    chunk = df_full.iloc[start_idx:end_idx].copy()
    chunk["cleaned_ingredients"] = chunk["ingredients"].astype(str).apply(clean_ingredients_spacy_pos)
    out_chunk = chunk[["recipe_id", "cleaned_ingredients"]]
    all_chunks.append(out_chunk)

final_df = pd.concat(all_chunks, ignore_index=True)
final_df.to_parquet(OUTPUT_PATH, index=False, engine="pyarrow", compression="snappy")

total_end = time.time()
print(f"\n Total processing time: {total_end - total_start:.2f} seconds")
print("\n Chunked cleaning complete and saved to:", OUTPUT_PATH)