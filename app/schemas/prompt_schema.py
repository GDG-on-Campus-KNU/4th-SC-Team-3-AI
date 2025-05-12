from typing import List, Literal, Union
from pydantic import BaseModel

class BaseImageGenerationPrompt(BaseModel):
    type: str
    model_config = {
        "discriminator": "type"
    }

class TextImageGenerationPrompt(BaseImageGenerationPrompt):
    type: Literal["text"]
    content: str

class CategoryImageGenerationPrompt(BaseImageGenerationPrompt):
    type: Literal["category"]
    key: str
    value: List[str]

class GroupImageGenerationPrompt(BaseImageGenerationPrompt):
    type: Literal["group"]
    contents: List["ImageGenerationPrompt"]

ImageGenerationPrompt = Union[
    TextImageGenerationPrompt,
    CategoryImageGenerationPrompt,
    GroupImageGenerationPrompt,
]

class AnalysisResult(BaseModel):
    subject: str
    action: str
    visual_elements: List[str]
    auditory_elements: List[str]
    environment: List[str]