from typing import Optional
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import Mapped, DeclarativeBase
from sqlalchemy.orm import mapped_column, declarative_base
from sqlalchemy.sql import func, text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.types import TIMESTAMP, DateTime
from datetime import datetime, UTC
from pydantic import BaseModel

class Base(DeclarativeBase):
  pass

class Base_Table(Base):
  __abstract__ = True

  id = mapped_column(Integer, primary_key=True, autoincrement="auto", unique=True)
  createdAt = mapped_column(DateTime(), default=lambda _: datetime.now(UTC)) 
  updatedAt = mapped_column(DateTime(), default=datetime.now(UTC), onupdate=lambda _: datetime.now(UTC))
