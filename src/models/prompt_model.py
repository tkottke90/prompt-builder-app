import datetime
from src.models.base_model import Base_Table, Base_DTO
from sqlalchemy import DateTime, ForeignKey, String, Integer
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import Mapped
from pydantic import BaseModel
from typing import List, Optional
from src.models import query_params

PVT = "PromptTableVersion"

class PromptTable(Base_Table):
  __tablename__ = "prompts"

  value = mapped_column(String, nullable=False)
  label = mapped_column(String, nullable=False, index=True)
  tags = mapped_column(String, default="")
  versions: Mapped[List["PromptVersionTable"]] = relationship(back_populates="parent", cascade="all, delete-orphan")


class PromptVersionTable(Base_Table):
  __tablename__ = "prompt_version"

  parent = relationship("PromptTable", back_populates="versions")
  index = mapped_column(Integer, default=-1, nullable=False)
  
  parentId: Mapped[int] = mapped_column(ForeignKey("prompts.id"))
  prompt = mapped_column(String, nullable=False, index=True)
  comments = mapped_column(String, default="", nullable=False)

##### DTOs #####

class CreatePromptDTO(BaseModel):
  label: str
  value: str
  tags: Optional[list[str]] = None

class UpdatePromptDTO(CreatePromptDTO):
  label: Optional[str] = None
  value: Optional[str] = None
  tags: Optional[list[str]] = None

class PromptDTO(Base_DTO, CreatePromptDTO):
  deletedAt: str

class PromptQuery(BaseModel):
  value: Optional[str | query_params.StringFieldQueryModel] = None
  label: Optional[str | query_params.StringFieldQueryModel] = None
  value: Optional[str | query_params.StringFieldQueryModel] = None
  createdAt: Optional[str | query_params.DateFieldQueryModel] = None
  updatedAt: Optional[str | query_params.DateFieldQueryModel] = None
  deletedAt: Optional[str | query_params.DateFieldQueryModel] = None
