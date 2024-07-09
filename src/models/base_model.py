from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import DateTime
from datetime import datetime, UTC
from pydantic import BaseModel

class Base(DeclarativeBase):
  pass

class Base_Table(Base):
  __abstract__ = True

  id = mapped_column(Integer, primary_key=True, autoincrement="auto", unique=True)
  createdAt = mapped_column(DateTime(), default=lambda _: datetime.now(UTC)) 
  updatedAt = mapped_column(DateTime(), default=datetime.now(UTC), onupdate=lambda _: datetime.now(UTC))

  def toPersistance(self, dto: BaseModel):
    def filterFn(member: str):
      lockedKeys = [ "id", "createdAt", "updatedAt", "metadata", "registry" ]

      return not (member.startswith("__") or member in lockedKeys)

    for key in filter(filterFn, dto.__dict__.keys()):
      if (key in self and getattr(dto, key) is not None):
        setattr(self, key, getattr(dto, key))

class Base_DTO(BaseModel):
  id: int
  createdAt: str
  updatedAt: str