from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from analysis.core import sentToAnalysis

app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,
    allow_methods=["*"],              
    allow_headers=["*"],             
)

@app.post("/")
async def analyse(url: str = Body(... , embed=True)):
    report = await sentToAnalysis(url)
    return report