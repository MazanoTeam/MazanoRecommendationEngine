from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
from dotenv import load_dotenv
from mongo_connect.connect_to_db import LikesDB, ItemsAPI
from recommendations.movies import Recommendations
import torch
import pandas as pd
import os
import timeit


class Request(BaseModel):
    uuid: str
    n_films: int = 20
    
app = FastAPI()

load_dotenv()

s = timeit.default_timer()
MODEL = torch.load("./recommendations/model/model.pt")
e = timeit.default_timer()
print(f"Model loaded ({(e-s):.2f} s)")

s = timeit.default_timer()
USERS_DB = LikesDB(os.environ["MONGO_URI_USERS"], "mazano", "users")
e = timeit.default_timer()
print(f"User DB connected ({(e-s):.2f} s)")

s = timeit.default_timer()
MOVIES = ItemsAPI(os.environ['MONGO_URI_API'], "Mazano-API", "Films-API")
e = timeit.default_timer()
print(f"Items(Movies) loaded({(e-s):.2f} s)")

MOVIE_VECTORS = pd.read_pickle("./recommendations/dataset/movie_vectors.pkl")

@app.get("/movies/get-recommendations")
async def movie_recommendations(request: Request):
    likes = USERS_DB.get_user_likes(request.uuid, "movie_likes")
    
    if not likes:
        return JSONResponse({
        "code": 402,
        "description": "Likes of this user is empty",
        "recommeandations": None
    })
    
    recs = Recommendations([movie['original_title'] for movie in likes], MODEL, MOVIE_VECTORS, MOVIES.items)
    
    recs.get_recommendations(request.n_films, k=0.8)

    return JSONResponse({
        "code": 200,
        "description": "Recommendations found",
        "recommendations": recs.recommendations
    })
    
