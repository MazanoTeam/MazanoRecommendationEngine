from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
from dotenv import load_dotenv
from mongo_connect.connect_to_db import LikesDB
from recomendations.movies import Recommendations
import pandas as pd
import os

class Request(BaseModel):
    uuid: str
    
app = FastAPI()

load_dotenv()
DB = LikesDB(os.environ["MONGO_URI"], "mazano", "users")
MOVIE_VECTORS = pd.read_pickle("recomendations\dataset\movie_vectors.pkl")

@app.get("/movies/get-recommendations")
async def movie_recommendations(request: Request):
    likes = DB.get_user_likes(request.uuid, "movie_likes")
    recs = Recommendations()
    
    return JSONResponse({
        "code": 200,
        "description": "Recommendations found",
        "likes": likes
    })
    
