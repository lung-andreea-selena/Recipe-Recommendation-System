import logging
from typing import Dict, List, Optional
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

    def get_by_ids(self, recipe_ids: List[int]) -> Dict[int, RawRecipe]:
        """
        Batch-fetch all the RawRecipe for the given list of IDs,
        and return a dict recipe_id → RawRecipe.
        """
        if not recipe_ids:
            return {}

        query = text("""
            SELECT recipe_id, title, ingredients, directions, link, source
              FROM raw_recipes
             WHERE recipe_id = ANY(:ids)
        """)
        rows = self._db_session.execute(query, {"ids": recipe_ids}).fetchall()
        return {row[0]: RawRecipe(*row) for row in rows}