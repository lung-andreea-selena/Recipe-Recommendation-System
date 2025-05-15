# build_tfidf.py
import joblib
import numpy as np
from scipy import sparse
from repositories.cleaned_ingredients_repo import CleanedIngredientsRepo
from utils.db_connection import SessionLocal
from sklearn.feature_extraction.text import TfidfVectorizer

def main():
    db = SessionLocal()
    rows = CleanedIngredientsRepo(db).get_all()
    docs = [r.ingredients or "" for r in rows]

    vec = TfidfVectorizer(ngram_range=(1,2), min_df=2, max_df=0.8)
    X = vec.fit_transform(docs)

    joblib.dump(vec, "models/tfidf_vectorizer.joblib")
    sparse.save_npz("models/tfidf_matrix.npz", X)
    with open("models/recipe_ids.npy", "wb") as f:
        np.save(f, np.array([r.recipe_id for r in rows]))

    print(f"Persisted TF–IDF (vocab={len(vec.vocabulary_)}, docs={len(docs)})")

if __name__ == "__main__":
    main()
