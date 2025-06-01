from dataclasses import dataclass
from typing import List, Any

@dataclass
class RecipeDTO:
    recipe_id: int
    title: str
    ingredients: List[str]
    has_missing_ingredients: bool

    def to_dict(self) -> dict:
        return {
            "recipe_id": self.recipe_id,
            "title": self.title,
            "ingredients": self.ingredients,
            "has_missing_ingredients": self.has_missing_ingredients,
        }