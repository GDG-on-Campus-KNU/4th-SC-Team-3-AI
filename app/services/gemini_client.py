from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from typing import List
from app.schemas.prompt_schema import AnalysisResult, ImageGenerationPrompt
from google.genai.errors import APIError
from dotenv import load_dotenv

import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv('API_KEY'))

def format_scene_description(payload: List[ImageGenerationPrompt]) -> str:
    json_data = json.dumps([item.model_dump() for item in payload], ensure_ascii=False, indent=2)
    prompt = (
        "다음 JSON을 분석해서 사진을 생성해주세요.\n"
        "사진을 생성할 때, 프롬프트가 사진 내에 포함되지 않도록 주의해주세요.\n"
        "분석할 JSON:\n"
        f"{json_data}"
    )
    return prompt

def generate_image_from_gemini(data: List[ImageGenerationPrompt]) -> bytes:
    prompt = format_scene_description(data)

    print(prompt)

    # 🪄 이미지 생성 요청
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=["Text", "Image"])
        )
    except APIError as e:
        raise Exception("이미지 생성 실패: " + e.message)
    
    if not response.candidates:
        raise Exception("이미지 생성 실패: Gemini 응답에 후보가 없습니다.")

    # 첫 번째 후보에서 이미지 데이터 찾기
    candidate = response.candidates[0]
    if not candidate.content.parts:
        raise Exception("이미지 생성 실패: Gemini 응답에 이미지가 없습니다.")

    # 🎨 이미지 추출
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            return buffer.getvalue()

def analyze_prompt(text: str) -> str:
    prompt = (
        "다음 텍스트를 분석하여 JSON 형식으로 변환해주세요. 다음 카테고리에 맞게 분류해주세요:\n"
        "- Subject: 문장의 주어 (1개)\n"
        "- Action: 주어의 동작 (1개)\n"
        "- Visual elements: 시각적으로 보이는 요소 리스트 (여러 개 가능)\n"
        "- Auditory elements: 들리는 소리 요소 리스트 (여러 개 가능)\n"
        "- Environment: 주변 환경 묘사 리스트 (여러 개 가능)\n"
        f"분석할 텍스트: {text}"
    )
    return prompt

def analyze_with_gemini(text: str) -> dict:
    prompt = analyze_prompt(text)

    print(prompt)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=AnalysisResult,
            )
        )
    except APIError as e:
        raise Exception("카테고리 분석 실패: " + e.message)

    if not response.text:
        raise Exception("카테고리 분석 실패: Gemini 응답에 카테고리 분석 결과가 없습니다.")
    
    return json.loads(response.text)