# This script uses TextBlob to clean a list of ingredients.
# It processes the ingredients in a loop, storing the results in a DataFrame and saving it to a CSV file.
# Elapsed time: 2.44 seconds
# This script uses TextBlob to clean a list of ingredients by lemmatizing and removing stop words and punctuation.

import time
import pandas as pd
from textblob import TextBlob


with open("first_200_ingredients_not_cleaned.txt", "r", encoding="utf-8") as file:
    lines = [line.strip() for line in file if line.strip()]

def clean_with_textblob(text):
    blob = TextBlob(text)
    cleaned = " ".join([word.lemmatize() for word in blob.words])
    return cleaned

results = []
start = time.time()
for line in lines:
    
    cleaned = clean_with_textblob(line)
    elapsed = time.time() - start
    results.append({
        "original": line,
        "textblob_cleaned": cleaned,
    })
elapsed = time.time() - start

df = pd.DataFrame(results)
df.to_csv("textblob_experiment_results.csv", index=False)

print("\n TextBlob cleaning complete. Results saved to 'textblob_experiment_results.csv'")
print(f"Elapsed time: {elapsed:.2f} seconds")
print(f"Number of ingredients processed: {len(lines)}")
print(f"Average time per ingredient: {elapsed / len(lines):.4f} seconds")