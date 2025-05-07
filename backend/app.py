# app.py
from flask import Flask, g
from flask_cors import CORS
from repositories.cleaned_ingredients_repo import CleanedIngredientsRepo
from repositories.raw_recipes_repo import RawRecipesRepo
from service.pantry_recommender import PantryRecommender
from utils.db_connection import SessionLocal
from routes.recommend import recommend_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
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
