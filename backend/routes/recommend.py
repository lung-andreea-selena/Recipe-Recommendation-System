import time
from flask import Blueprint, json, request, jsonify, current_app
from dtos.recipe_dto import RecipeDTO
from repositories.raw_recipes_repo import RawRecipesRepo

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    payload = request.get_json(force=True)
    if not payload or "ingredients" not in payload:
        return jsonify(error="Missing 'ingredients'"), 400

    ingredients = payload["ingredients"]
    page = int(payload.get("page", 0))
    per_page = int(payload.get("per_page", 20))

    recommender = current_app.config["PANTRY_RECOMMENDER"]
    raw_repo = current_app.config["RAW_RECIPES_REPO"]
    recs = recommender.recommend(ingredients, page, per_page)
    has_more = bool(recommender.recommend(ingredients, page + 1, 1))


    t0 = time.time()
    ids = [r["recipe_id"] for r in recs]
    raw_map = raw_repo.get_by_ids(ids)
    results = []
    for r in recs:
        raw = raw_map.get(r["recipe_id"])
        if not raw:
            continue

        try:
            maybe = json.loads(raw.ingredients)
            if isinstance(maybe, list):
                ingr_list = [str(i).strip() for i in maybe if str(i).strip()]
            else:
                raise ValueError
        except Exception:
            ingr_list = [i.strip() for i in raw.ingredients.split(",") if i.strip()]

        dto = RecipeDTO(
            recipe_id=raw.recipe_id,
            title=raw.title,
            ingredients=ingr_list,
            has_missing_ingredients=(r["missing"] > 0)
        )
        results.append(dto.to_dict())

    elapsed = time.time() - t0
    print(f"[LOG] batch get_by_ids took {elapsed:.3f}s")

    return jsonify(page=page, per_page=per_page, has_more=has_more, recipes=results), 200

@recommend_bp.route("/recipe/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id: int):
    raw_repo = current_app.config['RAW_RECIPES_REPO']

    raw_map = raw_repo.get_by_ids([recipe_id])
    raw = raw_map.get(recipe_id)
    if raw is None:
        return jsonify(error=f"Recipe {recipe_id} not found"), 404

    return jsonify(raw.to_dict()), 200