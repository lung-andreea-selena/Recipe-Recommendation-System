# This script uses spaCy to clean ingredient lines by removing measurement nouns and retaining meaningful nouns. 
# It processes a list of ingredient lines and saves the cleaned data to a CSV file.
import spacy
import time
import pandas as pd

nlp = spacy.load("en_core_web_sm")

MEASUREMENT_NOUNS = set([
    "can", "pkg", "package", "oz", "ounce", "bag", "container", "cup", "quart", "pint", "jar",
    "bottle", "box", "envelope", "stick", "slice", "serving", "packet", "lb", "pound", "gallon",
    "tablespoon", "tbsp", "teaspoon", "tsp", "dash", "pinch", "clove", "head", "bunch", "sprig",
    "size", "small", "medium", "large", "extra", "bite", "bite-size", "chopped", "shredded",
    "diced", "minced", "frozen", "fresh", "lean", "fat", "boneless", "skinless", "prepared",
    "uncooked", "raw", "melted", "cooked", "grated", "sliced", "divided", "softened", "refrigerated",
    "optional", "thawed", "warm", "cold", "room", "temperature", "cut", "inch", "thick"
])


def clean_with_spacy_pos(text):
    doc = nlp(text)
    cleaned = []

    for token in doc:
        lemma = token.lemma_.lower()

        if (
            token.pos_ in ["NOUN", "PROPN"] and  # keep meaningful nouns
            lemma not in MEASUREMENT_NOUNS and  # remove measurements
            token.is_alpha                       # skip numbers or punctuation
        ):
            cleaned.append(lemma)

    return " ".join(cleaned)

with open("first_200_ingredients_not_cleaned.txt", "r", encoding="utf-8") as file:
    lines = file.read().splitlines()

results = []
start_time = time.time()

for line in lines:
    cleaned = clean_with_spacy_pos(line)
    results.append({
        "original": line,
        "spacy_pos_cleaned": cleaned
    })

elapsed_time = time.time() - start_time

df = pd.DataFrame(results)
df.to_csv("spacy_pos_final_cleaned.csv", index=False)


print("\nSpaCy POS-based cleaning complete. Saved to 'spacy_pos_final_cleaned.csv'")
print(f"Elapsed time: {elapsed_time:.2f} seconds")
print(f"Ingredients processed: {len(results)}")
print(f"Avg. time per ingredient: {elapsed_time / len(results):.5f} seconds")
