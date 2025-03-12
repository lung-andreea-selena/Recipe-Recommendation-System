import re

MEASUREMENTS = [
    'teaspoon', 'tsp', 'tablespoon', 'tbsp', 'fluid ounce', 'fl oz', 'cup', 'c',
    'pint', 'pt', 'quart', 'qt', 'gallon', 'gal', 'ml', 'milliliter', 'mL',
    'l', 'liter', 'kg', 'kilogram', 'g', 'gram', 'oz', 'ounce', 'lb', 'pound',
    'mg', 'milligram'
]

# Regex pattern with optional plural forms
MEASUREMENTS_PATTERN = r"\b(?:\d*\s*(?:" + "|".join([m + "s?" for m in MEASUREMENTS]) + r")\b\.?)"

def remove_measurements(text):
    # Remove fractions (e.g., '1/2', '3/4')
    text = re.sub(r'\d+\s*/\s*\d+', '', text)
    # Remove measurements with associated numbers (e.g., '2 cups', '1 tbsp')
    text = re.sub(MEASUREMENTS_PATTERN, "", text, flags=re.IGNORECASE)
    # Remove any remaining standalone numbers
    text = re.sub(r'\d+\s*', '', text)
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()
