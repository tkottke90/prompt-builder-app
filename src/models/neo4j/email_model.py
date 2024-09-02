import dataclasses
from typing import Optional
from src.models.neo4j.base_model import Neo4JBaseDao, Neo4JSchema, BaseDataClass

@dataclasses.dataclass(kw_only=True)
class CreateEmail(BaseDataClass):
  sender: str;
  senderDisplayName: str;
  subject: str;
  message: str;
  summary: str;

@dataclasses.dataclass(kw_only=True)
class Email(CreateEmail, Neo4JSchema):
  id: str;

@dataclasses.dataclass(kw_only=True)
class UpdateEmail(BaseDataClass):
  sender: Optional[str] = None;
  senderDisplayName: Optional[str] = None;
  subject: Optional[str] = None;
  message: Optional[str] = None;
  summary: Optional[str] = None;

@dataclasses.dataclass(kw_only=True)
class FindEmail(UpdateEmail):
  id: Optional[str] = None;


