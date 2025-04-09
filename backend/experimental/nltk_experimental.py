# This script cleans a list of ingredients using NLTK for tokenization, lemmatization, and stopword removal.
# It processes the ingredients in a loop, storing the results in a DataFrame and saving it to a CSV file.
# Elapsed time: 2.23 seconds


import time
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Make sure you have the necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Setup
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Load ingredients
with open("first_200_ingredients_not_cleaned.txt", "r", encoding="utf-8") as file:
    lines = [line.strip() for line in file if line.strip()]

# Cleaning function using NLTK
def clean_with_nltk(text):
    tokens = word_tokenize(text)
    filtered = [lemmatizer.lemmatize(word.lower()) for word in tokens if word.lower() not in stop_words and word.isalpha()]
    return " ".join(filtered)

# Run experiments
results = []
start = time.time()
for line in lines:
    cleaned = clean_with_nltk(line)
    results.append({
        "original": line,
        "nltk_cleaned": cleaned,
    })
elapsed = time.time() - start

# Save results
df = pd.DataFrame(results)
df.to_csv("nltk_experiment_results.csv", index=False)

print("\n NLTK cleaning complete. Results saved to 'nltk_experiment_results.csv'")
print(f"Elapsed time: {elapsed:.2f} seconds")
print(f"Number of ingredients processed: {len(lines)}")
print(f"Average time per ingredient: {elapsed / len(lines):.4f} seconds")
