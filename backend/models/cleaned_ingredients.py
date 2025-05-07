from models.base_model import BaseModel

class CleanedIngredients(BaseModel):
    def __init__(self, recipe_id, ingredients):
        self._recipe_id   = recipe_id
        self._ingredients = ingredients

    @property
    def recipe_id(self) -> int:
        return self._recipe_id
    
    @property
    def ingredients(self) -> str:
        return self._ingredients
    
    def to_dict(self):
        return {
            "recipe_id": self.recipe_id,
            "ingredients": self.ingredients
        }