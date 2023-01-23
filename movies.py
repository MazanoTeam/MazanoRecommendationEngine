import pandas as pd
import random

from timeit import default_timer as timer

class Movies:
    def __init__(self, path_to_csv: str) -> None:
        self.path_to_csv = path_to_csv

        self.movies_overview, self.movies_tags = self.load_movies()

    def load_movies(self):
        return pd.read_pickle("datasets/movies/movies_overview.pkl"), pd.read_pickle("datasets/movies/movies_with_tags.pkl")
        

class MoviesRecommendation:
    def __init__(self, Movies: Movies) -> None:
        self.Movies = Movies
        
        self.cosine_similarity_overview, self.cosine_similarity_tags = self.get_cosine_similarity()
    
    def get_cosine_similarity(self):
        return pd.read_pickle("datasets/movies/cosine_similarity_overview.pkl"), pd.read_pickle("datasets/movies/cosine_similarity_tags.pkl")

    def get_last_liked_movie_recommendations(self, movie, n_films: int, k: float = 0.5) -> list:
        n_recommended_films = int((n_films * k)/2)
        
        indeces_overview = pd.Series(
            data=self.Movies.movies_overview.index, 
            index=self.Movies.movies_overview['original_title']
        ).drop_duplicates()
        
        indeces_tags = pd.Series(
            data=self.Movies.movies_tags.index, 
            index=self.Movies.movies_tags['title']
        ).drop_duplicates()

        sim_scores_overview = enumerate(self.cosine_similarity_overview[indeces_overview[movie]])
        sim_scores_tags = enumerate(self.cosine_similarity_tags[indeces_tags[movie]])

        sim_scores_overview = sorted(sim_scores_overview, key=lambda x: x[1], reverse=True)[1:n_recommended_films]
        sim_scores_tags = sorted(sim_scores_tags, key=lambda x: x[1], reverse=True)[1:n_recommended_films]
        
        sim_index_overview = [i[0] for i in sim_scores_overview]
        sim_index_tags = [i[0] for i in sim_scores_tags]

        movies_rec_by_overview = self.Movies.movies_overview['original_title'].iloc[sim_index_overview]
        movies_rec_by_tags = self.Movies.movies_tags['title'].iloc[sim_index_tags]
        
        recommendations = [*movies_rec_by_overview, *movies_rec_by_tags]
        
        random_films = random.choices(self.Movies.movies_overview['original_title'], k=(n_films - len(recommendations)))
        
        recommendations = [*recommendations, *random_films]
        
        random.shuffle(recommendations)
        
        return recommendations


if __name__ == "__main__":
    start = timer()
    
    movies = Movies("datasets/movies/movies.csv")

    recommendations = MoviesRecommendation(movies)

    recs = recommendations.get_last_liked_movie_recommendations("Avatar", 80, k=0.8)
    
    end = timer()
    print(recs)
    print(end-start)