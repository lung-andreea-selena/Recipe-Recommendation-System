import pandas as pd

df_light = pd.read_parquet("dataset/nltk_cleaned_light.parquet")
print(df_light.head())

# df = pd.read_parquet("dataset/recipes.parquet", engine="pyarrow")
# print(df.columns)
