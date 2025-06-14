import numpy as np
from scipy import sparse
from service.pantry_recommender import PantryRecommender


class StubVectoriser:
    def __init__(self, vocab: list[str]):
        self.vocabulary_ = {t: i for i, t in enumerate(vocab)}

    def transform(self, docs):
        rows, cols = [], []
        for r, doc in enumerate(docs):
            tok = doc.split()[0]
            if tok in self.vocabulary_:
                rows.append(r)
                cols.append(self.vocabulary_[tok])
        data = np.ones(len(rows))
        return sparse.csr_matrix(
            (data, (rows, cols)),
            shape=(len(docs), len(self.vocabulary_)),
            dtype=float,
        )


def make_tiny():
    """
    3 recipes:
      100 -> soy sauce
      101 -> soy sauce + garlic
      102 -> garlic
    """
    vec = StubVectoriser(["soy_sauce", "garlic"])
    mat = sparse.csr_matrix(
        [
            [1, 0],   # 100
            [1, 1],   # 101
            [0, 1],   # 102
        ],
        dtype=float,
    )
    ids  = np.array([100, 101, 102])
    docs = [
        {"ingredients": "soy sauce"},
        {"ingredients": "soy sauce garlic"},
        {"ingredients": "garlic"},
    ]
    return PantryRecommender(vec, mat, ids, docs)

def test_two_token_match_selected():
    rec = make_tiny()
    res = rec.recommend(["soy sauce", "garlic"], min_match=2)
    assert len(res) == 1
    rec0 = res[0]
    assert rec0["recipe_id"] == 101
    assert rec0["matched"] == 2 and rec0["missing"] == 0

def test_single_match_filtered_out():
    rec = make_tiny()
    res = rec.recommend(["soy sauce"], min_match=2)
    assert res == []  # nothing meets the 2-match bar

def test_no_candidates_returns_empty():
    rec = make_tiny()
    res = rec.recommend(["rice", "oil"], min_match=2)
    assert res == []

def test_matched_missing_counts():
    rec = make_tiny()
    res = rec.recommend(["soy sauce", "garlic"], min_match=2)
    r = res[0]
    assert (r["matched"], r["missing"]) == (2, 0)
