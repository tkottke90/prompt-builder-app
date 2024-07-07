from src.models.base_model import Base_Table, Mapped, Column, mapped_column
from sqlalchemy import String, ARRAY
from pydantic import BaseModel
from typing import List, Optional
from src.models import query_params

class PromptTable(Base_Table):
  __tablename__ = "prompts"

  value = mapped_column(String, nullable=False)
  label = mapped_column(String, nullable=False, index=True)
  tags = mapped_column(String, default="")

class CreatePromptDTO(BaseModel):
  label: str
  value: str
  tags: Optional[list[str]] = None

class PromptDTO(BaseModel):
  id: int
  label: str
  value: str
  tags: list[str]
  createdAt: str
  updatedAt: str

class PromptQuery(BaseModel):
  value: Optional[str | query_params.StringFieldQueryModel] = None
  label: Optional[str | query_params.StringFieldQueryModel] = None
  value: Optional[str | query_params.StringFieldQueryModel] = None
  createdAt: Optional[str | query_params.DateFieldQueryModel] = None
  updatedAt: Optional[str | query_params.DateFieldQueryModel] = None