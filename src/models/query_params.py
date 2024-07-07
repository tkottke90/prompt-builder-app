from typing import Optional
from pydantic import BaseModel

class IntegerFieldQueryModel(BaseModel):
  eq: Optional[int] = None
  gt: Optional[int] = None
  lt: Optional[int] = None

class StringFieldQueryModel(BaseModel):
  eq: Optional[str] = None
  startsWith: Optional[str] = None
  endsWith: Optional[str] = None
  like: Optional[str] = None
  nlike: Optional[str] = None

class DateFieldQueryModel(BaseModel):
  eqDateTime: Optional[str] = None
  eqDate: Optional[str] = None
  before: str
  after: str
  daysUntil: int
  daysSince: int 