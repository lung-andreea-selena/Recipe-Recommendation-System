import re

MEASUREMENTS = [
    'teaspoon', 'tsp', 'tablespoon', 'tbsp', 'fluid ounce', 'fl oz', 'cup', 'c',
    'pint', 'pt', 'quart', 'qt', 'gallon', 'gal', 'ml', 'milliliter', 'mL',
    'l', 'liter', 'kg', 'kilogram', 'g', 'gram', 'oz', 'ounce', 'lb', 'pound',
    'mg', 'milligram','pkg', 'package', 'can', 'jar', 'bottle', 'bunch', 'pinch',
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

WORDS_TO_REMOVE = [
    "more", "choice", "dinner", "lunch", "breakfast", "snack", "appetizer", "dessert", "side", "main", "course",
    "firmly", "packed", "broken", "bite", "size", "shredded", "small", "cut", "up", "boned", "cubed", "melted",
    "divided", "optional", "baking", "extra", "lean", "chopped","chipped","evaporated", "diced", "minced", "beaten", "crushed", "crumbled",
    "softened", "sifted", "whole", "cooked", "frozen", "reserved", "save", "fresh", "dry", "dried", "boiled",
    "thawed", "grated", "light", "instant", "prepared", "reduced", "stirred", "finely", "coarsely", "sliced",
    "halved", "peeled", "pitted", "seeded", "trimmed", "ripe", "baked", "uncooked", "cored", "shelled", "taste",
    "chunks", "piece", "pieces", "thick", "thinly", "many", "each","chipped", "round", "square", "long", "short",
    "room", "warmed", "boneless", "skinless", "deveined", "drained", "canned", "jarred", "packet","slice","box",
    "container", "bottle", "bag", "package", "bunch", "can", "jar", "carton", "tube", "bowl",
    "sautéed", "roasted", "charred", "grilled", "seared", "stewed", "simmered", "fried", "blanched", "toasted",
    "crispy", "zesty", "unsweetened", "sweetened", "garnish", "serve", "approximate", "approximately", "needed",
    "in", "on", "at", "with","all-purpose","allpurpose", "self-rising", "lowfat", "nonfat", "fat-free", "skim", "organic", "natural", "flavored", "plain",
    "lite", "virgin","small", "medium", "large", "extra-large", "jumbo", "baby", "mini", "whole", "half", "low-sodium",
]

# Regex pattern for words to remove; each word is allowed an optional trailing 's'
WORDS_PATTERN = r"\b(?:" + "|".join([re.escape(w) + "s?" for w in WORDS_TO_REMOVE]) + r")\b"

def remove_words(text):
    # Remove all defined words (and their plural forms)
    text = re.sub(WORDS_PATTERN, "", text, flags=re.IGNORECASE)
    # Remove extra whitespace that might result from removals
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_ingredient(text):
    text = remove_measurements(text)
    text = remove_words(text)
    return text
