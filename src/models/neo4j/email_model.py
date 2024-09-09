import dataclasses
from typing import Optional, List
from src.models.neo4j.base_model import Neo4JTimestampModel
from src.dao.base_dao.neo4j_base_dao import Neo4jBaseModel


@dataclasses.dataclass(kw_only=True)
class CreateEmail(Neo4jBaseModel):
  sender: str
  senderDisplayName: str
  subject: str
  message: str
  summary: str

@dataclasses.dataclass(kw_only=True)
class Email(CreateEmail, Neo4JTimestampModel):
  id: int

@dataclasses.dataclass(kw_only=True)
class UpdateEmail(Neo4jBaseModel):
  sender: Optional[str] = None
  senderDisplayName: Optional[str] = None
  subject: Optional[str] = None
  message: Optional[str] = None
  summary: Optional[str] = None

@dataclasses.dataclass(kw_only=True)
class FindEmail(UpdateEmail):
  id: Optional[str] = None


