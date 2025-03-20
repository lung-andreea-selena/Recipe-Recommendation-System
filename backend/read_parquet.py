import pandas as pd

# df_light = pd.read_parquet("dataset/nltk_cleaned_light.parquet")
# print(df_light.head())

df_light = pd.read_parquet("dataset/recipes.parquet")
ingredients_column = df_light["ingredients"].head(200)
pd.set_option("display.max_colwidth", None)
output_file = "first_200_ingredients_not_cleaned.txt"

# Save the data to a plain text file (one ingredient list per line)
with open(output_file, "w", encoding="utf-8") as file:
    file.write("\n".join(ingredients_column.astype(str)))

print(f"File '{output_file}' has been created successfully! 🎉")
#print(ingredients_column.head(200))

# df = pd.read_parquet("dataset/recipes.parquet", engine="pyarrow")
# print(df.columns)
