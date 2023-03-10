import pandas as pd
import numpy as np
import random


class Recommendations:
    def __init__(self, movie_titles: list, model, vectors: pd.DataFrame, total_movie_list: list):
        self.model = model

        self.vectors = vectors
        self.total_movie_list = total_movie_list
        self.recommendations = list()

        self.liked_movie_vectors = [
            self.vectors['overview'].iloc[vectors.index[vectors['original_title'] == movie_title].tolist()[0]]
            for movie_title in movie_titles
        ][:5]

        self.total_movie_titles = {movie['original_title'] for movie in self.total_movie_list}

    def cosine_similarity(self, a, b) -> float:
        dot_prod = np.dot(a, b.T)

        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        return (dot_prod / (norm_a * norm_b))[0][0]

    def get_similarities(self, row):
        for movie_vector in self.liked_movie_vectors:
            self.recommendations.append(
                {
                    "original_title": row['original_title'],
                    "sim_score": self.cosine_similarity(movie_vector, row['overview'])
                }
            )

    def get_recommendations(self, n_films: int, k: float):
        len_recommended_movies = int(n_films*k)

        self.vectors.apply(self.get_similarities, axis=1)

        self.recommendations = sorted(
            self.recommendations,
            key=lambda x: x['sim_score'],
            reverse=True
        )[len(self.liked_movie_vectors) : len_recommended_movies]

        self.recommendations = list({
            movie['original_title'] for movie in self.recommendations
        })
        
        main_recommendations, other_recommendations = self.recommendations[:int(len_recommended_movies/5)], self.recommendations[int(len_recommended_movies/5):]

        self.total_movie_titles = self.total_movie_titles.symmetric_difference(set(self.recommendations))

        len_random_movies = n_films - len(self.recommendations)
        random_movies = random.sample(list(self.total_movie_titles), len_random_movies)

        main_recommendations = [*main_recommendations, *random_movies[:int(len_random_movies/2)]]
        other_recommendations = [*other_recommendations, *random_movies[int(len_random_movies/2):]]

        random.shuffle(main_recommendations)
        random.shuffle(other_recommendations)

        self.recommendations = [*main_recommendations, *other_recommendations]

        self.recommendations = [
            movie for movie in self.total_movie_list if movie['original_title'] in self.recommendations
        ]

        print(len(self.recommendations))
