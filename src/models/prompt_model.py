import datetime
from fastapi.encoders import jsonable_encoder
from src.models.base_model import Base_Table, Base_DTO
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer, Table
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import Mapped
from pydantic import BaseModel
from typing import List, Optional
from src.models import query_params
import inspect


association_table = Table(
    "prompt_versions",
    Base_Table.metadata,
    Column("promptId", ForeignKey("prompts.id"), primary_key=True),
    Column("versionId", ForeignKey("version.id"), primary_key=True),
)

class PromptTable(Base_Table):
  __tablename__ = "prompts"

  value = mapped_column(String, nullable=False)
  label = mapped_column(String, nullable=False, index=True)
  tags = mapped_column(String, default="")
  versions: Mapped[List["PromptVersionTable"]] = relationship(secondary=association_table)

  def toDTO(self):
    return {
      "id": self.id,
      "value": self.value,
      "label": self.label,
      "tags": self.tags.split(',') if self.tags is not None else [],
      "createdAt": self.createdAt,
      "updatedAt": self.updatedAt
    }


class PromptVersionTable(Base_Table):
  __tablename__ = "version"

  index = mapped_column(Integer, default=-1, nullable=False)
  
  prompt = mapped_column(String, nullable=False, index=True)
  comments = mapped_column(String, default="", nullable=False)

  def toDTO(self):
    return {
      "id": self.id,
      "index": self.index,
      "prompt": self.prompt,
      "comments": self.comments,
      "createdAt": self.createdAt,
      "updatedAt": self.updatedAt
    }

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
