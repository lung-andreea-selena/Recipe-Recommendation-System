from typing import List, Optional
from sqlalchemy.orm import Session
from models.cleaned_ingredients import CleanedIngredients
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

class CleanedIngredientsRepo:
    def __init__(self, db_session: Session):
        self._db_session = db_session
    
    def get_all(self) -> List[CleanedIngredients]:
        try:
            query = text("SELECT recipe_id, ingredients FROM cleaned_ingredients")
            result = self._db_session.execute(query).fetchall()
            return [CleanedIngredients(recipe_id=row[0], ingredients=row[1]) for row in result]
        except Exception as e:
            logger.exception("Failed to fetch all cleaned ingredients")
            return []  
      
    def get_by_recipe_id(self, recipe_id: int) -> Optional[CleanedIngredients]:
        if not isinstance(recipe_id, int):
            logger.warning(f"Invalid recipe_id type: {type(recipe_id)}")
            return None
        
        try:
            query = text("SELECT recipe_id, ingredients FROM cleaned_ingredients WHERE recipe_id = :recipe_id")
            result = self._db_session.execute(query, {"recipe_id": recipe_id}).fetchone()
            if result:
                return CleanedIngredients(recipe_id=result[0], ingredients=result[1])
            return None
        except Exception as e:
            logger.exception(f"Failed to fetch cleaned_ingredients for recipe_id={recipe_id}")
            return None