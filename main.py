# main.py
import uvicorn
from fastapi import FastAPI
from app.routes.analyze import router as analyze_router
from app.routes.generate import router as generate_router

app = FastAPI()

app.include_router(analyze_router)
app.include_router(generate_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
