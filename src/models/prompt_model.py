from src.models.base_model import Base_Table, Base_DTO
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import Mapped
from pydantic import BaseModel
from typing import List, Optional, Callable
from src.models import query_params
from src.utils import string_util

##### DTOs #####

class CreatePromptDTO(BaseModel):
  label: str
  value: str
  tags: Optional[list[str]] = None

class UpdatePromptDTO(CreatePromptDTO):
  label: Optional[str] = None
  value: Optional[str] = None
  tags: Optional[list[str]] = None



class PromptQuery(BaseModel):
  value: Optional[str | query_params.StringFieldQueryModel] = None
  label: Optional[str | query_params.StringFieldQueryModel] = None
  value: Optional[str | query_params.StringFieldQueryModel] = None
  createdAt: Optional[str | query_params.DateFieldQueryModel] = None
  updatedAt: Optional[str | query_params.DateFieldQueryModel] = None
  deletedAt: Optional[str | query_params.DateFieldQueryModel] = None

class PromptVersionDTO(Base_DTO):
  prompt: str
  previous: str
  next: str
  comments: str

class UpdatePromptVersionDTO(BaseModel):
  prompt: Optional[str] = None
  previous: Optional[str] = None
  next: Optional[str] = None
  comments: Optional[str] = None

class PromptDTO(Base_DTO, CreatePromptDTO):
  versions: list[PromptVersionDTO]
  deletedAt: str

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
    versions = self.versions
    current = string_util.checksum(self.value)
    last = string_util.checksum(versions[-1].prompt)

    versionDTOs = [ version.toDTO() for version in versions ]

    return {
      "id": self.id,
      "value": self.value,
      "label": self.label,
      "tags": self.tags.split(',') if self.tags is not None else [],
      "createdAt": self.createdAt,
      "updatedAt": self.updatedAt,
      "versions": versionDTOs[-5 if len(versions) > 5 else -1 * len(versions)::],
      "hasChanges": current != last
    }
  
  def toPersistance(self, dto: PromptDTO):
    if (dto.tags is not None):
      self.tags = ','.join(dto.tags)
      dto.tags = None

    super().toPersistance(dto)


class PromptVersionTable(Base_Table):
  __tablename__ = "version"

  index = mapped_column(String, nullable=False)
  previous = mapped_column(String, nullable=True)
  next = mapped_column(String, nullable=True)
  
  prompt = mapped_column(String, nullable=False, index=True)
  comments = mapped_column(String, default="", nullable=False)

  def toDTO(self):
    return {
      "id": self.id,
      "index": self.index,
      "prompt": self.prompt,
      "comments": self.comments,
      "previous": self.previous,
      "next": self.next,
      "createdAt": self.createdAt,
      "updatedAt": self.updatedAt
    }
