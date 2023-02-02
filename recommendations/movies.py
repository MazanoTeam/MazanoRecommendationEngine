import pandas as pd
import numpy as np

class Recommendations:
    def __init__(self, movie_titles: list, model, vectors: pd.DataFrame):
        self.model = model

        self.vectors = vectors
        self.recommendations = list()

        self.movie_vectors = [
            self.vectors['overview'].iloc[vectors.index[vectors['original_title'] == movie_title].tolist()[0]]
            for movie_title in movie_titles
        ][:5]

    def cosine_similarity(self, a, b) -> float:
        dot_prod = np.dot(a, b.T)

        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        return (dot_prod / (norm_a * norm_b))[0][0]

    def get_similarities(self, row):
        for movie_vector in self.movie_vectors:
            self.recommendations.append(
                {
                    "original_title": row['original_title'],
                    "sim_score": self.cosine_similarity(movie_vector, row['overview'])
                }
            )

    def get_recommendations(self, n_films: int):
        self.vectors.apply(self.get_similarities, axis=1)

        self.recommendations = sorted(
            self.recommendations,
            key=lambda x: x['sim_score'],
            reverse=True
        )[len(self.movie_vectors):n_films+len(self.movie_vectors)]
  