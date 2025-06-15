# word2vec_cosine_recommender.py
import pandas as pd
import numpy as np
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import time
import matplotlib.pyplot as plt

class Word2VecRecommender:
    def __init__(self, data_path: str,
                 vector_size: int = 100, window: int = 5,
                 min_count: int = 1, sg: int = 1, epochs: int = 10):
        self.df = pd.read_csv(data_path)
        docs = self.df['cleaned_ingredients'].fillna('').tolist()
        self.rec_token_sets = [set(doc.split()) for doc in docs]
        self.corpus = [doc.split() for doc in docs]

        t0 = time.time()
        self.model = Word2Vec(
            sentences=self.corpus,
            vector_size=vector_size,
            window=window,
            min_count=min_count,
            sg=sg,
            epochs=epochs
        )
        t1 = time.time()

        self.recipe_vectors = np.vstack([
            self._vectorize(tokens) for tokens in self.corpus
        ])
        t2 = time.time()

        print(
            f"Loaded {len(self.df)} recipes; "
            f"Word2Vec vocab={len(self.model.wv)}; "
            f"train_time={t1-t0:.3f}s; embed_time={t2-t1:.3f}s"
        )

    def _vectorize(self, tokens: list[str]) -> np.ndarray:
        vecs = [self.model.wv[t] for t in tokens if t in self.model.wv]
        if not vecs:
            return np.zeros(self.model.vector_size)
        return np.mean(vecs, axis=0)

    def recommend(self, user_input: str, top_n: int = 10):
        t_start = time.time()

        t1 = time.time()
        tokens = user_input.lower().replace(',', ' ').split()
        user_vec = self._vectorize(tokens).reshape(1, -1)
        t2 = time.time()

        sims = cosine_similarity(user_vec, self.recipe_vectors).flatten()
        t3 = time.time()

        query_tokens = set(tokens)
        matched = np.array([len(rec & query_tokens) for rec in self.rec_token_sets])
        missing = np.array([len(rec - query_tokens) for rec in self.rec_token_sets])
        t4 = time.time()

        candidates = [i for i, m in enumerate(matched) if m > 0]
        t5 = time.time()

        candidates.sort(key=lambda i: (missing[i], -matched[i], -sims[i]))
        top_idxs = candidates[:top_n]
        t6 = time.time()

        recs = []
        for rank, i in enumerate(top_idxs, start=1):
            recs.append({
                'rank': rank,
                'recipe_id': int(self.df.iloc[i]['recipe_id']),
                'matched_count': int(matched[i]),
                'missing_count': int(missing[i]),
                'score': float(sims[i])
            })
        t7 = time.time()

        print(
            f"Timings (s): build_vec={t2-t1:.3f}, cosine={t3-t2:.3f}, \
            overlap={t4-t3:.3f}, filter={t5-t4:.3f}, sort={t6-t5:.3f}, build={t7-t6:.3f}, total={t7-t_start:.3f}"
        )

        return recs

    def plot_score(self, recommendations):
        ids = [str(r['recipe_id']) for r in recommendations]
        scores = [r['score'] for r in recommendations]
        plt.figure(figsize=(8, 5))
        plt.bar(ids, scores, color='skyblue')
        plt.xlabel('Recipe ID')
        plt.ylabel('Similarity Score')
        plt.title('Top 10 Recipes (Word2Vec Cook-from-Pantry)')
        plt.tight_layout()
        plt.savefig('experimental/recommendation/w2v_cookfrompantry_chart.png')
        plt.show()


rec = Word2VecRecommender('dataset/tfidf_sample.csv')
res = rec.recommend(
    'cream cheese tomato onion garlic basil olive oil salt pepper', top_n=10
)
for r in res:
    print(
        f"{r['rank']}. Recipe {r['recipe_id']} "
        f"(matched={r['matched_count']}, missing={r['missing_count']}, score={r['score']:.3f})"
    )
rec.plot_score(res)
