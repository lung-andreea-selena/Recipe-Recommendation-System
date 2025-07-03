from typing import List, Dict, Any, Sequence, Set
import time, logging
from sklearn.metrics.pairwise import cosine_similarity
from utils.phrase_tokenizer import tokenizer

logger = logging.getLogger(__name__)

class PantryRecommender:
    def __init__(
        self,
        vectorizer,
        tfidf_matrix,
        recipe_ids: Sequence[int],
        cleaned_records: List[Dict[str, Any]],
    ) -> None:
        self.vectorizer = vectorizer
        self.tfidf_matrix = tfidf_matrix
        self.recipe_ids = recipe_ids
        self.records = cleaned_records
        self.token_sets: List[Set[str]] = [
            set(tokenizer(r.get("ingredients") or "")) for r in cleaned_records
        ]

    def _select_candidates(
        self,
        pantry_tokens: Set[str],
        min_match: int,
        needed: int,
    ) -> List[tuple[int, int, int]]:
        stats = []
        for idx, toks in enumerate(self.token_sets):
            matched = len(toks & pantry_tokens)
            if matched >= min_match:
                missing = len(toks - pantry_tokens)
                stats.append((idx, matched, missing))

        picked: List[tuple[int, int, int]] = []
        miss = 0
        max_missing = max((x for _, _, x in stats), default=0)
        while len(picked) < needed and miss <= max_missing:
            for idx, m, x in stats:
                if x == miss:
                    picked.append((idx, m, x))
                    if len(picked) >= needed:
                        break
            miss += 1
        return picked

    def recommend(
        self,
        pantry_list: List[str],
        page: int = 0,
        per_page: int = 20,
        min_match: int = 2,
    ) -> List[Dict[str, Any]]:
        start_time = time.time()

        pantry_tokens = set(tokenizer(" ".join(pantry_list)))
        logger.info("Pantry tokens: %s", sorted(pantry_tokens))
        if not pantry_tokens:
            return []

        needed = (page + 1) * per_page
        page_stats = self._select_candidates(pantry_tokens, min_match, needed)[
            page * per_page : (page + 1) * per_page
        ]
        if not page_stats:
            return []

        query_str = " ".join(pantry_tokens)
        query_vec = self.vectorizer.transform([query_str])
        row_idxs = [idx for idx, _, _ in page_stats]
        similarities = cosine_similarity(query_vec, self.tfidf_matrix[row_idxs]).flatten()

        results = []
        for (idx, matched, missing), score in zip(page_stats, similarities):
            results.append(
                {
                    "recipe_id": int(self.recipe_ids[idx]),
                    "matched": matched,
                    "missing": missing,
                    "score": float(score),
                }
            )

        results.sort(key=lambda r: (r["missing"], -r["matched"], -r["score"]))

        elapsed = time.time() - start_time
        logger.info(
            "Recommendation took %.3fs -> returned %d recipes", elapsed, len(results)
        )
        for i, r in enumerate(results, 1):
            logger.info("  %2d. %d  matched=%d  missing=%d  score=%.3f",
                        i, r['recipe_id'], r['matched'], r['missing'], r['score'])
        logger.info("")

        return results