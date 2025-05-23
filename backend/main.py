from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from analysis.core import sentToAnalysis

app = FastAPI()

origins = [
    "http://localhost:4200",
    "https://visus-obscura.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,
    allow_methods=["*"],              
    allow_headers=["*"],             
)

#better payload deconstruction

@app.post("/")
async def analyse(url: str = Body(... , embed=True)):
    try:
        report = await sentToAnalysis(url)
        return {"status": "success", "report": report}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")