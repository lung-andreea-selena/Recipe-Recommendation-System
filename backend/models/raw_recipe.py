from models.base_model import BaseModel

class RawRecipe(BaseModel):
    def __init__(self, recipe_id, title, ingredients, directions, link, source, ner):
        self.recipe_id = recipe_id
        self.title = title
        self.ingredients = ingredients
        self.directions = directions
        self.link = link
        self.source = source

    @property
    def recipe_id(self):
        return self._recipe_id
    
    @property
    def title(self):
        return self._title
    
    @property
    def ingredients(self):
        return self._ingredients    
    
    @property
    def directions(self):
        return self._directions
    
    @property
    def link(self):
        return self._link
    
    @property
    def source(self):
        return self._source
    
    def to_dict(self):
        return {
            "recipe_id": self.recipe_id,
            "title": self.title,
            "ingredients": self.ingredients,
            "directions": self.directions,
            "link": self.link,
            "source": self.source,
        }