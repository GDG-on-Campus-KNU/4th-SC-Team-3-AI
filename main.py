# main.py
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Request
from app.exceptions.gemini_exception import GeminiException
from app.routes.analyze import router as analyze_router
from app.routes.generate import router as generate_router
from dotenv import load_dotenv
from fastapi import status

import uvicorn
import os

load_dotenv()

PIPY_API_KEY = os.getenv("PIPY_API_KEY")

app = FastAPI()

app.include_router(analyze_router)
app.include_router(generate_router)

@app.exception_handler(HTTPException)
async def general_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "message": exc.detail,
        },
    )

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    api_key = request.headers.get("X-Api-Key")
    if api_key != PIPY_API_KEY:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "Invalid API key",
            },
        )
    response = await call_next(request)
    return response

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
