import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

class PantryRecommender:
    def __init__(self,
                 cleaned_records: List[Dict[str, str]],
                 tfidf_params: Dict = None):
        """
        cleaned_records: list of {"recipe_id": int, "ingredients": str}
        """
        self.records = cleaned_records
        docs = [r["ingredients"] or "" for r in cleaned_records]

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=(tfidf_params or {}).get("min_df", 2),
            max_df=(tfidf_params or {}).get("max_df", 0.8),
            max_features=(tfidf_params or {}).get("max_features", None)
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(docs)
        print(f"[INIT] Built TF–IDF on {len(docs)} recipes; vocab={len(self.vectorizer.vocabulary_)}")

    def recommend(self, pantry_list: List[str], page: int = 0, per_page: int = 40, min_match: int = 2) -> List[int]:
        """
        Returns a page of recipe_ids (ints), **not** dicts, so that
        your blueprint can do `get_by_id(rid)` without error.
        """
        t0 = time.time()

        pantry = {tok.strip().lower() for tok in pantry_list if tok.strip()}
        print(f"[LOG] Pantry tokens = {sorted(pantry)}")
        if not pantry:
            return []

        stats = []
        for idx, rec in enumerate(self.records):
            ingr = rec.get('ingredients') or ""
            toks = set(ingr.split())
            m = len(toks & pantry)
            x = len(toks - pantry)
            if m >= min_match:
                stats.append((idx, m, x))

        needed = (page + 1) * per_page
        picked = []
        miss   = 0
        max_missing = max((x for _,_,x in stats), default=0)
        while len(picked) < needed and miss <= max_missing:
            for idx, m, x in stats:
                if x == miss:
                    picked.append((idx, m, x))
                    if len(picked) >= needed:
                        break
            miss += 1

        start = page * per_page
        page_stats = picked[start:start + per_page]
        if not page_stats:
            print("[LOG] no recipes for this page")
            return []

        query_str = " ".join(pantry)
        q_vec = self.vectorizer.transform([query_str])
        row_idxs = [idx for idx, _, _ in page_stats]
        sim_vals = cosine_similarity(q_vec, self.tfidf_matrix[row_idxs]).flatten()

        out = []
        for (idx, m, x), sim in zip(page_stats, sim_vals):
            out.append({
                "recipe_id":self.records[idx]["recipe_id"],
                "matched":m,
                "missing":x,
                "score":float(sim)
            })
        out.sort(key=lambda r: (-r["matched"], -r["score"]))
        recipe_ids = [r["recipe_id"] for r in out]

        elapsed = time.time() - t0
        print(f"[LOG] recommendation took {elapsed:.3f}s → returned {len(recipe_ids)} recipes")
        for i, rid in enumerate(recipe_ids, 1):
            stats_dict = next(item for item in out if item["recipe_id"] == rid)
            print(f"  {i:2}. #{rid}  matched={stats_dict['matched']}  "
                  f"missing={stats_dict['missing']}  score={stats_dict['score']:.3f}")
        print()

        return recipe_ids
