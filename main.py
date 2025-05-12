# main.py
from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, Request
from app.exceptions.gemini_exception import GeminiException
from app.routes.analyze import router as analyze_router
from app.routes.generate import router as generate_router

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
