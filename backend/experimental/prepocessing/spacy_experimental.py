import spacy
import time
import pandas as pd


nlp = spacy.load("en_core_web_sm")

with open("first_200_ingredients_not_cleaned.txt", "r", encoding="utf-8") as f:
    ingredients_list = [line.strip() for line in f if line.strip()]


def clean_with_spacy(text):
    doc = nlp(text.lower())
    return " ".join([
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and token.is_alpha
    ])

results = []
start = time.time()
for original in ingredients_list:
    cleaned = clean_with_spacy(original)
    results.append({
        "original": original,
        "spacy_cleaned": cleaned,
    })
elapsed = time.time() - start

df = pd.DataFrame(results)
df.to_csv("spacy_experiment_results.csv", index=False)

print(df.head(10))
print("\n spaCy cleaning complete. Results saved to 'spacy_experiment_results.csv'")
print(f"Elapsed time: {elapsed:.2f} seconds")
print(f"Number of ingredients processed: {len(ingredients_list)}")
