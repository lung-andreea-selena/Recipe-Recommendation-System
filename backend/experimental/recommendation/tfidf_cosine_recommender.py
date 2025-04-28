import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import matplotlib.pyplot as plt

class TfidfRecommender:
    def __init__(self, data_path: str):
        """
        Loads recipe data, builds TF-IDF matrix (1-grams), and precomputes
        token sets for strict "cook-from-pantry" matching.
        """
        self.df = pd.read_csv(data_path)
        docs = self.df['cleaned_ingredients'].fillna('').tolist()
        # Precompute unigram token sets for each recipe
        self.rec_token_sets = [set(doc.split()) for doc in docs]

        # Initialize TF-IDF vectorizer (unigrams only)
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 1),  # unigrams
            min_df=2,
            max_df=0.8,
            max_features=None
        )
        # Fit-transform and measure time
        t0 = time.time()
        self.tfidf_matrix = self.vectorizer.fit_transform(docs)
        fit_time = time.time() - t0

        # Presence matrix & feature counts for overlap logic
        self.presence = (self.tfidf_matrix > 0).astype(int)
        self.feature_counts = self.presence.sum(axis=1).A1

        print(f"Loaded {len(self.df)} recipes")
        print(f"TF-IDF fit time: {fit_time:.3f} seconds; vocabulary size = {len(self.vectorizer.vocabulary_)}")

    def recommend(self, user_input: str, top_n: int = 10):
        """
        Recommends top_n recipes based on "strict subsets first" rule:
        1) fewest missing ingredients (strict subsets → extras)
        2) most matched ingredients
        3) highest TF-IDF cosine similarity

        Also prints timing breakdown for each step.
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
        matched = np.array([len(tokens & query_tokens) for tokens in self.rec_token_sets])
        missing = np.array([len(tokens - query_tokens) for tokens in self.rec_token_sets])
        t4 = time.time()

        # 4) Filter and sort candidates
        candidates = [i for i, m in enumerate(matched) if m > 1]
        candidates.sort(key=lambda i: (missing[i], -matched[i], -sims[i]))
        top_idxs = candidates[:top_n]
        t5 = time.time()

        # 5) Build recommendations
        recommendations = []
        for rank, i in enumerate(top_idxs, 1):
            recommendations.append({
                'rank': rank,
                'recipe_id': int(self.df.iloc[i]['recipe_id']),
                'matched_count': int(matched[i]),
                'missing_count': int(missing[i]),
                'score': float(sims[i])
            })
        t_end = time.time()

        # Print timing breakdown
        print(
            f"Timings (s): transform={t2-t1:.3f}, cosine={t3-t2:.3f}, \
            overlap={t4-t3:.3f}, sort={t5-t4:.3f}, build={t_end-t5:.3f}, total={t_end-t_start:.3f}"
        )

        return recommendations

    def plot_score(self, recommendations):
        recipe_ids = [str(r['recipe_id']) for r in recommendations]
        scores     = [r['score'] for r in recommendations]

        plt.figure(figsize=(8, 5))
        plt.bar(recipe_ids, scores, color='skyblue')
        plt.xlabel('Recipe ID')
        plt.ylabel('Similarity Score')
        plt.title('Top 10 Recipes (Cook-from-Pantry TF-IDF)')
        plt.tight_layout()
        plt.savefig('experimental/recommendation/tfidf_cookfrompantry_chart.png')
        plt.show()

# Example usage:
rec = TfidfRecommender('dataset/tfidf_sample.csv')
results = rec.recommend(
    'cream cheese, tomato, onion, garlic, basil, olive oil, salt, pepper', top_n=10
)
for r in results:
    print(
        f"{r['rank']}. Recipe {r['recipe_id']} "
        f"(matched={r['matched_count']}, missing={r['missing_count']}, score={r['score']:.3f})"
    )
rec.plot_score(results)
