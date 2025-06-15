from __future__ import annotations

import joblib
import numpy as np
from pathlib import Path
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from repositories.cleaned_ingredients_repo import CleanedIngredientsRepo
from utils.db_connection import SessionLocal
from utils.phrase_tokenizer import tokenizer  

MODELS_DIR = Path(__file__).resolve().parent / "models"
MODELS_DIR.mkdir(exist_ok=True)


def main() -> None: 

    db = SessionLocal()
    rows = CleanedIngredientsRepo(db).get_all()
    docs = [row.ingredients or "" for row in rows]
    print(f"Loaded {len(docs):,} ingredient documents")

    vectorizer = TfidfVectorizer(
        tokenizer=tokenizer,          
        token_pattern=None,           
        ngram_range=(1, 1),           
        min_df=5,                     
        max_df=0.85,                  
        sublinear_tf=True,
        norm="l2",
        lowercase=False,              
    )

    X = vectorizer.fit_transform(docs)

    joblib.dump(vectorizer, MODELS_DIR / "tfidf_vectorizer.joblib")
    sparse.save_npz(MODELS_DIR / "tfidf_matrix.npz", X)
    np.save(MODELS_DIR / "recipe_ids.npy", np.array([row.recipe_id for row in rows]))

    print(
        "Saved vectoriser (vocab="
        f"{len(vectorizer.vocabulary_):,}), matrix shape={X.shape}, ids={len(rows):,}"
    )


if __name__ == "__main__":
    main()