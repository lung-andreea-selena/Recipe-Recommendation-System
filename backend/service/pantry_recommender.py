import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Sequence, Set
import joblib
from scipy import sparse

class PantryRecommender:
    def __init__(
        self,
        vectorizer,
        tfidf_matrix,
        recipe_ids,
        cleaned_records:   List[Dict[str, str]]
    ):
        """
        Loads precomputed TF–IDF artifacts plus cleaned ingredient data.
        """
        self.vectorizer   = vectorizer
        self.tfidf_matrix = tfidf_matrix
        self.recipe_ids   = recipe_ids
        self.records      = cleaned_records

        self.token_sets = [set((r.get("ingredients") or "").split()) for r in cleaned_records]

        print(
            f"[INIT] Loaded TF–IDF (vocab={len(self.vectorizer.vocabulary_)}, "
            f"docs={self.tfidf_matrix.shape[0]})"
        )


    def recommend(
        self,
        pantry_list: List[str],
        page: int     = 0,
        per_page: int = 20,
        min_match: int= 2
    ) -> List[int]:
        t0 = time.time()

        pantry = {
            w
            for entry in pantry_list
            for w in entry.lower().replace(",", " ").split()
            if w
        }
        print(f"[LOG] Pantry tokens = {sorted(pantry)}")
        if not pantry:
            return []

        stats = []
        for idx, toks in enumerate(self.token_sets):
            m = len(toks & pantry)
            x = len(toks - pantry)
            if m >= min_match:
                stats.append((idx, m, x))

        needed      = (page + 1) * per_page
        picked      = []
        miss        = 0
        max_missing = max((x for _,_,x in stats), default=0)
        while len(picked) < needed and miss <= max_missing:
            for idx, m, x in stats:
                if x == miss:
                    picked.append((idx, m, x))
                    if len(picked) >= needed:
                        break
            miss += 1

        start      = page * per_page
        page_stats = picked[start : start + per_page]
        if not page_stats:
            print("[LOG] no recipes for this page")
            return []

        query_str = " ".join(pantry)
        q_vec     = self.vectorizer.transform([query_str])
        row_idxs  = [idx for idx,_,_ in page_stats]
        sim_vals  = cosine_similarity(q_vec, self.tfidf_matrix[row_idxs]).flatten()

        out = []
        for (idx, m, x), sim in zip(page_stats, sim_vals):
            out.append({
                "recipe_id": int(self.recipe_ids[idx]),
                "matched":    m,
                "missing":    x,
                "score":      float(sim)
            })
        out.sort(key=lambda r: (-r["matched"], -r["score"]))

        recipe_ids = [r["recipe_id"] for r in out]

        elapsed = time.time() - t0
        print(f"[LOG] recommendation took {elapsed:.3f}s → returned {len(recipe_ids)} recipes")
        for i, r in enumerate(out, 1):
            print(f"  {i:2}. #{r['recipe_id']}  matched={r['matched']}  "
                  f"missing={r['missing']}  score={r['score']:.3f}")
        print()

        return recipe_ids