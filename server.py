from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
from dotenv import load_dotenv
from mongo_connect.connect_to_db import LikesDB, ItemsAPI
from recommendations.movies import Recommendations
import torch
import pandas as pd
import os

class Request(BaseModel):
    uuid: str
    n_films: int = 20
    
app = FastAPI()

load_dotenv()
USERS_DB = LikesDB(os.environ["MONGO_URI_USERS"], "mazano", "users")
MODEL = torch.load("recommendations\model\model.pt")

MOVIES = ItemsAPI(os.environ['MONGO_URI_API'], "Mazano-API", "Films-API")
MOVIE_VECTORS = pd.read_pickle("recommendations\dataset\movie_vectors.pkl")

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
        "recommeandations": recs.recommendations
    })
    
