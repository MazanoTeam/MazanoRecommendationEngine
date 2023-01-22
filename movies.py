import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class Movies:
    def __init__(self, path_to_csv: str) -> None:
        self.path_to_csv = path_to_csv

        self.dataframe = self.load_csv()

    def load_csv(self):
        return pd.read_csv(self.path_to_csv)
        

class MoviesRecommendation:
    def __init__(self, Movies: Movies) -> None:
        self.Movies = Movies

        self.tfidf_matrix = self.create_tfidf_matrix()
        self.cosine_similarity = self.get_cosine_similarity()

    def create_tfidf_matrix(self):
        tfidf = TfidfVectorizer(stop_words="english")
        self.Movies.dataframe['overview'] = self.Movies.dataframe['overview'].fillna('')

        return tfidf.fit_transform(self.Movies.dataframe['overview'])
    
    def get_cosine_similarity(self):
        return linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

    def get_last_liked_movie_recommendations(self, movie, n_films: int):
        indeces = pd.Series(
            data=self.Movies.dataframe.index, 
            index=self.Movies.dataframe['original_title']
        ).drop_duplicates()

        sim_scores = enumerate(self.cosine_similarity[indeces[movie]])

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n_films]
        sim_index = [i[0] for i in sim_scores]

        print(self.Movies.dataframe['original_title'].iloc[sim_index])


if __name__ == "__main__":
    movies = Movies("datasets/movies.csv")

    recommendations = MoviesRecommendation(movies)

    recommendations.get_last_liked_movie_recommendations("The Matrix", 20)