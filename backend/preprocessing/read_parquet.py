import pandas as pd

# df_light = pd.read_parquet("dataset/recipes_cleaned_spacy.parquet")
# print(df_light.head(10))

# df_light = pd.read_parquet("dataset/recipes.parquet")
# ingredients_column = df_light["ingredients"].head(200)
# pd.set_option("display.max_colwidth", None)
# output_file = "first_200_ingredients_not_cleaned.txt"

# Save the data to a plain text file (one ingredient list per line)
# with open(output_file, "w", encoding="utf-8") as file:
#     file.write("\n".join(ingredients_column.astype(str)))

# print(f"File '{output_file}' has been created successfully! 🎉")
#print(ingredients_column.head(200))

# df = pd.read_parquet("dataset/recipes.parquet", engine="pyarrow")
# print(df.columns)


# # Specify the path to your Parquet file
# parquet_file_path = 'dataset/recipes.parquet'

# # Read the Parquet file into a DataFrame
# df = pd.read_parquet(parquet_file_path)

# # Print the column names
# print("Column names:", df.columns.tolist())
# print(df.head(10))


# Define the path to your Parquet file
parquet_file_path = 'dataset/recipes.parquet'

# Read the Parquet file into a DataFrame
df = pd.read_parquet(parquet_file_path)

# Get the first 10 rows of the DataFrame
first_10_rows = df.head(10)

# Define the output text file path
output_txt_path = 'output.txt'

# Write the first 10 rows to a text file using the DataFrame's string representation
with open(output_txt_path, 'w') as file:
    file.write(first_10_rows.to_string(index=False))

print(f"First 10 rows have been written to {output_txt_path}")