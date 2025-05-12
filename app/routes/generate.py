from fastapi import APIRouter, Response
from typing import List
from app.services.gemini_client import generate_image_from_gemini
from app.schemas.prompt_schema import ImageGenerationPrompt

router = APIRouter()

@router.post("/generate/image")
async def generate_image(payload: List[ImageGenerationPrompt]):
    image_bytes = generate_image_from_gemini(payload)
    return Response(content=image_bytes, media_type="image/png")