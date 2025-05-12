# main.py
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from app.exceptions.gemini_exception import GeminiException
from app.routes.analyze import router as analyze_router
from app.routes.generate import router as generate_router
from dotenv import load_dotenv

import uvicorn
import os

app = FastAPI()

app.include_router(analyze_router)
app.include_router(generate_router)

@app.exception_handler(GeminiException)
async def general_exception_handler(request: Request, exc: GeminiException):
    return JSONResponse(
        status=exc.status,
        content={
            "status": exc.status,
            "message": exc.message,
        },
    )

if __name__ == "__main__":
    load_dotenv()
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
