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
  previous: Optional[str]
  next: Optional[str]
  comments: str

class UpdatePromptVersionDTO(BaseModel):
  prompt: Optional[str] = None
  previous: Optional[str] = None
  next: Optional[str] = None
  comments: Optional[str] = None

class PromptDTO(Base_DTO, CreatePromptDTO):
  versions: list[PromptVersionDTO]

association_table = Table(
    "prompt_versions",
    Base_Table.metadata,
    Column("promptId", ForeignKey("prompts.id"), primary_key=True),
    Column("versionId", ForeignKey("version.id"), primary_key=True),
)

class PromptTable(Base_Table):
  __tablename__ = "prompts"

  value: Mapped[String] = mapped_column(String, nullable=False)
  label: Mapped[String] = mapped_column(String, nullable=False, index=True)
  tags: Mapped[String] = mapped_column(String, default="")
  versions: Mapped[List["PromptVersionTable"]] = relationship(secondary=association_table)

  def toDTO(self) -> PromptDTO:
    versions = self.versions
    current = string_util.checksum(self.value)
    last = string_util.checksum(versions[-1].prompt)

    versionDTOs = [ version.toDTO() for version in versions ]

    return {
      "id": self.id,
      "value": self.value,
      "label": self.label,
      "tags": self.tags.split(',') if self.tags is not None else [],
      "createdAt": self.createdAt.isoformat(),
      "updatedAt": self.updatedAt.isoformat(),
      "versions": versionDTOs[-5 if len(versions) > 5 else -1 * len(versions)::],
      "hasChanges": current != last
    }
  
  def toPersistance(self, dto: PromptDTO):
    # The DTO stores tags as a string array but we store it in
    # the database as a string.  So before passing it to the 
    # base model, we first do the transform
    tags = getattr(dto, 'tags', None);
    if (tags is not None):
      self.tags = ','.join(tags)
      setattr(dto, 'tags', None)

    # Base model handles the majority of primitive storage steps
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
      "createdAt": self.createdAt.isoformat(),
      "updatedAt": self.updatedAt.isoformat()
    }
