import pandas as pd
from regex_preprocessing import clean_ingredients_regex
from nltk_preprocessing import clean_ingredients_nltk
import nltk
# nltk.download('punkt_tab')

# mock_ingredients = [
#     "2 cups all-purpose flour, sifted",
#     "1 (8 oz.) package cream cheese, softened",
#     "3 tablespoons olive oil",
#     "1 cup whole milk",
#     "4 teaspoons baking powder",
#     "2 lbs boneless chicken breast, diced",
#     "1/2 teaspoon salt",
#     "3 cloves garlic, minced",
#     "1 can (15 oz.) black beans, drained and rinsed",
#     "1/4 cup chopped fresh parsley",
#     "2 tablespoons unsalted butter, melted",
#     "1 pint cherry tomatoes, halved",
#     "1 teaspoon ground cumin",
#     "1 tablespoon soy sauce",
#     "1/2 cup grated Parmesan cheese",
#     "1 cup frozen peas",
#     "1 (12 oz.) package spaghetti noodles",
#     "1/4 teaspoon ground black pepper",
#     "1 medium onion, finely chopped",
#     "3 tablespoons lemon juice",
#     "firmly packed brown sugar evaporated milk vanilla broken nut pecan butter margarine bite size shredded rice biscuit",
#     "small jar chipped beef cut boned chicken breast cream mushroom soup carton sour cream",
#     "pkg frozen corn pkg cream cheese cubed butter cubed garlic powder salt pepper",
#     "large whole chicken can chicken gravy cream mushroom soup box stove top stuffing shredded cheese"
#     "peanut butter graham cracker crumb melted butter powdered sugar large pkg chocolate chip"
# ]
file_path = "first_200_ingredients_not_cleaned.txt"

with open(file_path, "r", encoding="utf-8") as file:
    mock_ingredients = [line.strip() for line in file.readlines()]

results = []
for ingredient in mock_ingredients:
    results.append({
        "NLTK": clean_ingredients_nltk(ingredient),
    })


df_results = pd.DataFrame(results)


df_results.to_csv("preprocessing_test.csv", index=False)


print(df_results)
print("\n🚀 Test completed! Results saved in preprocessing_test.csv")
