from models.base_model import BaseModel

class RawRecipe(BaseModel):
    def __init__(self, recipe_id, title, ingredients, directions, link, source):
        self._recipe_id = recipe_id
        self._title = title
        self._ingredients = ingredients
        self._directions = directions
        self._link = link 
        self._source = source

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