import pandas as pd

df = pd.read_parquet("dataset/recipes_cleaned_spacy.parquet")
subset = df.head(20000)
subset.to_csv("dataset/tfidf_sample.csv", index=False)
