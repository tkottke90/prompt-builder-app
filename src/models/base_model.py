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

class Base_DTO(BaseModel):
  id: int
  createdAt: str
  updatedAt: str