import joblib
import numpy as np
from scipy.sparse import load_npz
from flask import Flask, g
from flask_cors import CORS
from utils.db_connection import SessionLocal
from repositories.cleaned_ingredients_repo import CleanedIngredientsRepo
from repositories.raw_recipes_repo import RawRecipesRepo
from service.pantry_recommender import PantryRecommender
from routes.recommend import recommend_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    db1 = SessionLocal()
    cleaned_objs    = CleanedIngredientsRepo(db1).get_all()
    cleaned_records = [c.to_dict() for c in cleaned_objs]
    db1.close()

    vectorizer        = joblib.load("models/tfidf_vectorizer.joblib")
    tfidf_matrix      = load_npz("models/tfidf_matrix.npz")
    recipe_ids        = np.load("models/recipe_ids.npy")

    app.config["PANTRY_RECOMMENDER"] = PantryRecommender(
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
        recipe_ids=recipe_ids,
        cleaned_records=cleaned_records
    )

    raw_db = SessionLocal()
    app.config["RAW_RECIPES_REPO"] = RawRecipesRepo(raw_db)

    app.register_blueprint(recommend_bp, url_prefix="/api")

    @app.before_request
    def open_db_session():
        g.db = SessionLocal()

    @app.teardown_request
    def close_db_session(exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    return app

if __name__ == "__main__":
    create_app().run(debug=True)