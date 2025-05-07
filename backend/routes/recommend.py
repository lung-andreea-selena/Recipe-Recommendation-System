
from flask import Blueprint, request, jsonify, g, current_app
from repositories.cleaned_ingredients_repo import CleanedIngredientsRepo
from repositories.raw_recipes_repo import RawRecipesRepo
from service.pantry_recommender import PantryRecommender

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    if 'PANTRY_RECOMMENDER' not in current_app.config:
        cleaned_records = CleanedIngredientsRepo(g.db).get_all()
        rows = [c.to_dict() for c in cleaned_records]
        current_app.config['PANTRY_RECOMMENDER'] = PantryRecommender(rows)
        current_app.config['RAW_RECIPES_REPO']    = RawRecipesRepo(g.db)

    payload = request.get_json(force=True)
    if not payload or 'ingredients' not in payload:
        return jsonify(error="Missing 'ingredients'"), 400

    ingredients = payload['ingredients']
    page = int(payload.get('page', 0))
    per_page = int(payload.get('per_page', 40))

    recommender = current_app.config['PANTRY_RECOMMENDER']
    raw_repo = current_app.config['RAW_RECIPES_REPO']
    recipe_ids = recommender.recommend(ingredients, page, per_page)

    results = []
    for rid in recipe_ids:
        raw = raw_repo.get_by_id(rid)
        if raw:
            results.append(raw.to_dict())

    return jsonify(page=page, per_page=per_page, recipes=results), 200
