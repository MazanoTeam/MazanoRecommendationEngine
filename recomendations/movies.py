import pandas as pd
import numpy as np

class Recommendations:
    def __init__(self, movie_title: list, model, vectors: pd.DataFrame):
        self.model = model

        self.vectors = vectors
        self.recommendations = list()

        self.idx = vectors.index[vectors['original_title'] == movie_title].tolist()[0]

    def cosine_similarity(self, a, b):
        dot_prod = np.dot(a, b.T)

        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        return (dot_prod / (norm_a * norm_b))[0][0]

    def get_similarities(self, row):
        self.recommendations.append(
            {
                "original_title": row['original_title'],
                "sim_score": self.cosine_similarity(self.vectors['overview'].iloc[self.idx], row['overview'])
            }
        )

    def get_recommendations(self, n_films: int):
        self.vectors.apply(self.get_similarities, axis=1)

        self.recommendations = sorted(
            self.recommendations,
            key=lambda x: x['sim_score'],
            reverse=True
        )[1:n_films]
  