from src.models.base_model import Base_DTO
from pydantic import BaseModel, Field
from typing import List, Optional

class CreatePromptVersionDTO(BaseModel):
  parentId: int = Field(gt=0)
  index: int = Field(gt=0)

  prompt: str
  comments: list[str] = Field(default_factory=list)

class UpdatePromptVersionDTO(BaseModel):
  parentId: Optional[int]
  index: Optional[int]

  prompt: Optional[str]
  comments: Optional[list[str]]

class PromptVersionDTO(Base_DTO, CreatePromptVersionDTO):
  ...