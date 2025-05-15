
import time
from flask import Blueprint, request, jsonify, g, current_app
from repositories.cleaned_ingredients_repo import CleanedIngredientsRepo
from repositories.raw_recipes_repo import RawRecipesRepo
from service.pantry_recommender import PantryRecommender

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/recommend", methods=["POST"])
def recommend():

    payload = request.get_json(force=True)
    if not payload or 'ingredients' not in payload:
        return jsonify(error="Missing 'ingredients'"), 400

    ingredients = payload['ingredients']
    page = int(payload.get('page', 0))
    per_page = int(payload.get('per_page', 20))

    recommender = current_app.config['PANTRY_RECOMMENDER']
    raw_repo = current_app.config['RAW_RECIPES_REPO']
    recipe_ids = recommender.recommend(ingredients, page, per_page)

    t0 = time.time()
    raw_map = raw_repo.get_by_ids(recipe_ids)
    results = []
    for rid in recipe_ids:
        raw = raw_map.get(rid)
        if raw:
            results.append(raw.to_dict())
    elapsed = time.time() - t0
    print(f"[LOG] batch get_by_ids took {elapsed:.3f}s")

    return jsonify(page=page, per_page=per_page, recipes=results), 200