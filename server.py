from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
from dotenv import load_dotenv
from mongo_connect.connect_to_db import LikesDB
from recommendations.movies import Recommendations
import torch
import pandas as pd
import os

class Request(BaseModel):
    uuid: str
    
app = FastAPI()

load_dotenv()
DB = LikesDB(os.environ["MONGO_URI"], "mazano", "users")
MODEL = torch.load("recommendations\model\model.pt")
MOVIE_VECTORS = pd.read_pickle("recommendations\dataset\movie_vectors.pkl")

@app.get("/movies/get-recommendations")
async def movie_recommendations(request: Request):
    likes = DB.get_user_likes(request.uuid, "movie_likes")
    if not likes:
        return JSONResponse({
        "code": 402,
        "description": "Likes of this user is empty",
        "recommeandations": None
    })

    recs = Recommendations([movie['original_title'] for movie in likes], MODEL, MOVIE_VECTORS)
    
    recs.get_recommendations(10)

    recommendations = [movie['original_title'] for movie in recs.recommendations]
    return JSONResponse({
        "code": 200,
        "description": "Recommendations found",
        "recommeandations": recommendations
    })
    
