import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import matplotlib.pyplot as plt

class TfidfRecommender:
    def __init__(self, data_path: str):
        # Load data and build TF-IDF matrix with unigrams + bigrams
        self.df = pd.read_csv(data_path)
        docs = self.df['cleaned_ingredients'].fillna('').tolist()

        # Measure fit time for TF-IDF
        t0 = time.time()
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),  # capture multi-word ingredients
            min_df=2,
            max_df=0.8
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(docs)
        fit_time = time.time() - t0

        print(f"Loaded {len(self.df)} recipes; TF-IDF vocab={len(self.vectorizer.vocabulary_)}; fit_time={fit_time:.3f}s")

        # Binary presence matrix for feature overlap
        self.presence = (self.tfidf_matrix > 0).astype(int)
        # Precompute number of features per recipe
        self.feature_counts = self.presence.sum(axis=1).A1

    def recommend(self, user_input: str, top_n: int = 10):
        """
        1) Transform query with TF-IDF
        2) Compute cosine similarities
        3) Compute matched & missing counts on unigrams-only
        4) Filter out zero-match recipes
        5) Sort by (fewest extras, most matches, highest TF-IDF score)
        6) Return top_n recommendations and timings
        """
        t_start = time.time()

        # 1) TF-IDF transform
        t1 = time.time()
        q_tfidf = self.vectorizer.transform([user_input])
        t2 = time.time()

        # 2) Cosine similarity
        sims = cosine_similarity(q_tfidf, self.tfidf_matrix).flatten()
        t3 = time.time()

        # 3) Compute overlap on unigrams
        query_tokens = set(user_input.lower().replace(',', ' ').split())
        rec_token_sets = [set(doc.split()) for doc in self.df['cleaned_ingredients'].fillna('')]
        matched = np.array([len(tokens & query_tokens) for tokens in rec_token_sets])
        missing = np.array([len(tokens - query_tokens) for tokens in rec_token_sets])
        t4 = time.time()

        # 4) Filter candidates with at least one match
        candidates = [i for i, m in enumerate(matched) if m > 1]
        t5 = time.time()

        # 5) Sort candidates
        candidates.sort(key=lambda i: (missing[i], -matched[i], -sims[i]))
        top_idxs = candidates[:top_n]
        t6 = time.time()

        # 6) Build recommendation list
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

        # Print timing breakdown
        print(
            f"Timings (s): transform={t2-t1:.3f}, cosine={t3-t2:.3f}, \
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
        plt.title('Top 10 Recipes (Cook-from-Pantry TF-IDF handling biagrams)')
        plt.tight_layout()
        plt.savefig('experimental/recommendation/tfidf_biagrams_cookfrompantry_chart.png')
        plt.show()

# Example usage:
rec = TfidfRecommender('dataset/tfidf_sample.csv')
results = rec.recommend('cream cheese, tomato, onion, garlic, basil, olive oil, salt, pepper', top_n=10)
for r in results:
    print(f"{r['rank']}. Recipe {r['recipe_id']} (matched={r['matched_count']}, missing={r['missing_count']}, score={r['score']:.3f})")
rec.plot_score(results)