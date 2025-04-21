import logging
from typing import List, Optional
from models.raw_recipe import RawRecipe
from sqlalchemy.orm import Session
from sqlalchemy import text

logger = logging.getLogger(__name__)

class RawRecipesRepo:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    def get_all(self) -> List[RawRecipe]:
        try:
            query = text("SELECT recipe_id, title, ingredients, directions, link, source FROM raw_recipes")
            result = self._db_session.execute(query).fetchall()
            return [dict(row) for row in result]
        except Exception as e:
            logger.exception("Failed to fetch all raw recipes")
            return []

    def get_by_id(self, recipe_id)-> Optional[RawRecipe]:
        if not isinstance(recipe_id, int):
            logger.warning(f"Invalid recipe_id type: {type(recipe_id)}")
            return None

        try:
            query =text("SELECT recipe_id, title, ingredients, directions, link, source FROM raw_recipes WHERE recipe_id = :recipe_id")
            result = self._db_session.execute(query, {"recipe_id": recipe_id}).fetchone()
            if result:
                return RawRecipe(*result)
            return None
        except Exception as e:
            logger.exception(f"Failed to fetch raw recipe for recipe_id={recipe_id}")
            return None