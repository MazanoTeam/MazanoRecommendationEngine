from fastapi import FastAPI
from starlette.responses import JSONResponse

app = FastAPI()

@app.get("/recommendations/get-recommendations")
async def home(uuid: str):
    return JSONResponse({
        "code": 200,
        "description": "Recommendations found"
    })
    
