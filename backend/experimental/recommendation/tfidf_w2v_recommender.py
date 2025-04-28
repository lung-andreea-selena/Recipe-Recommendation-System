import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import time
import matplotlib.pyplot as plt

class TfidfW2VRecommender:
    def __init__(
        self,
        data_path: str,
        vector_size: int = 100,
        window: int = 5,
        min_count: int = 2,
        sg: int = 1,
        epochs: int = 10,
        tfidf_ngram_range=(1, 1),
        tfidf_min_df: int = 2,
        tfidf_max_df: float = 0.8
    ):
        # Load data
        self.df = pd.read_csv(data_path)
        docs = self.df["cleaned_ingredients"].fillna("").tolist()
        # Precompute unigram token sets for overlap logic
        self.rec_token_sets = [set(doc.split()) for doc in docs]

        # 1) Fit TF-IDF vectorizer
        t0 = time.time()
        self.tfidf = TfidfVectorizer(
            ngram_range=tfidf_ngram_range,
            min_df=tfidf_min_df,
            max_df=tfidf_max_df
        )
        self.tfidf_matrix = self.tfidf.fit_transform(docs)
        t1 = time.time()

        # 2) Train Word2Vec model
        self.corpus_tokens = [doc.split() for doc in docs]
        t2 = time.time()
        self.w2v = Word2Vec(
            sentences=self.corpus_tokens,
            vector_size=vector_size,
            window=window,
            min_count=min_count,
            sg=sg,
            epochs=epochs
        )
        t3 = time.time()

        # 3) Precompute TF-IDF–weighted document embeddings
        self.doc_embeddings = np.vstack([
            self._weighted_vector(tokens, tfidf_row)
            for tokens, tfidf_row in zip(
                self.corpus_tokens,
                self.tfidf_matrix.toarray()
            )
        ])
        t4 = time.time()

        print(
            f"Loaded {len(self.df)} recipes; "
            f"TF-IDF fit={t1-t0:.3f}s; "
            f"W2V train={t3-t2:.3f}s; "
            f"embed_calc={t4-t3:.3f}s; "
            f"TF-IDF vocab={len(self.tfidf.vocabulary_)}, "
            f"W2V vocab={len(self.w2v.wv)}"
        )

    def _weighted_vector(self, tokens: list[str], tfidf_row: np.ndarray) -> np.ndarray:
        vecs = []
        weights = []
        for token in tokens:
            if token in self.w2v.wv and token in self.tfidf.vocabulary_:
                idx = self.tfidf.vocabulary_[token]
                w = tfidf_row[idx]
                vecs.append(self.w2v.wv[token] * w)
                weights.append(w)
        if not vecs or sum(weights) == 0:
            return np.zeros(self.w2v.vector_size)
        return np.sum(vecs, axis=0) / sum(weights)

    def recommend(self, user_input: str, top_n: int = 10):
        """
        Recommends top_n recipes using strict "cook-from-pantry" rule:
          1) fewest missing unigrams
          2) most matched unigrams
          3) highest TF-IDF–W2V cosine score
        Prints timing breakdown for each step.
        """
        t_start = time.time()

        # 1) TF-IDF transform
        t1 = time.time()
        user_tfidf = self.tfidf.transform([user_input]).toarray()[0]
        t2 = time.time()

        # 2) Build user embedding (TF-IDF–weighted W2V)
        t3 = time.time()
        user_tokens = user_input.lower().replace(',', ' ').split()
        user_vec = self._weighted_vector(user_tokens, user_tfidf).reshape(1, -1)
        t4 = time.time()

        # 3) Cosine similarity
        sims = cosine_similarity(user_vec, self.doc_embeddings).flatten()
        t5 = time.time()

        # 4) Overlap counts on unigrams-only
        query_tokens = set(user_tokens)
        matched = np.array([len(rec & query_tokens) for rec in self.rec_token_sets])
        missing = np.array([len(rec - query_tokens) for rec in self.rec_token_sets])
        t6 = time.time()

        # 5) Filter candidates with ≥1 match
        candidates = [i for i, m in enumerate(matched) if m > 0]
        t7 = time.time()

        # 6) Sort by (missing asc, matched desc, score desc)
        candidates.sort(key=lambda i: (missing[i], -matched[i], -sims[i]))
        top_idxs = candidates[:top_n]
        t8 = time.time()

        # 7) Build result list
        recs = []
        for rank, i in enumerate(top_idxs, start=1):
            recs.append({
                'rank': rank,
                'recipe_id': int(self.df.iloc[i]['recipe_id']),
                'matched_count': int(matched[i]),
                'missing_count': int(missing[i]),
                'score': float(sims[i])
            })
        t9 = time.time()

        print(
            f"Timings (s): transform={t2-t1:.3f}, embed={t4-t3:.3f}, \
            cosine={t5-t4:.3f}, overlap={t6-t5:.3f}, \
            filter={t7-t6:.3f}, sort={t8-t7:.3f}, build={t9-t8:.3f}, total={t9-t_start:.3f}"
        )

        return recs

    def plot_score(self, recommendations: list[dict]):
        ids = [str(r['recipe_id']) for r in recommendations]
        scores = [r['score'] for r in recommendations]
        plt.figure(figsize=(8, 5))
        plt.bar(ids, scores, color='skyblue')
        plt.xlabel('Recipe ID')
        plt.ylabel('Similarity Score')
        plt.title('Top 10 Recipes (TF-IDF–W2V Cook-from-Pantry)')
        plt.tight_layout()
        plt.savefig('experimental/recommendation/tfidf_w2v_cookfrompantry_chart.png')
        plt.show()

# Example usage:
rec = TfidfW2VRecommender(
    'dataset/tfidf_sample.csv',
    vector_size=100, window=5, min_count=2, sg=1, epochs=10,
    tfidf_ngram_range=(1,2), tfidf_min_df=2, tfidf_max_df=0.8
)
results = rec.recommend(
    'cream cheese tomato onion garlic basil olive oil salt pepper', top_n=10
)
for r in results:
    print(f"{r['rank']}. Recipe {r['recipe_id']} (matched={r['matched_count']}, missing={r['missing_count']}, score={r['score']:.3f})")
rec.plot_score(results)

