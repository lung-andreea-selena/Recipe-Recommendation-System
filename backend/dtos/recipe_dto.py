from dataclasses import dataclass
from typing import List, Any

@dataclass
class RecipeDTO:
    title: str
    ingredients: List[str]
    has_missing_ingredients: bool

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "ingredients": self.ingredients,
            "has_missing_ingredients": self.has_missing_ingredients,
        }