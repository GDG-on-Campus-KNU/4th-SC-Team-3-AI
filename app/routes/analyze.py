from fastapi import APIRouter
from app.schemas.prompt_schema import TextImageGenerationPrompt
from app.services.gemini_client import analyze_with_gemini

router = APIRouter()

@router.post("/analyze")
async def analyze(request: TextImageGenerationPrompt):
    return analyze_with_gemini(request.content)
