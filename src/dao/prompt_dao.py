import src.database as database
from src.models.prompt_model import CreatePromptDTO, PromptTable, PromptDTO, PromptQuery
from datetime import datetime, UTC
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.utils import sqlalchemy_query
from src.models.base_model import Base_Table
from fastapi.encoders import jsonable_encoder

def toDTO(table: PromptTable) -> PromptDTO:
  return {
    "id": table.id,
    "value": table.value,
    "label": table.label,
    "tags": table.tags.split(',') if table.tags is not None else [],
    "createdAt": table.createdAt,
    "updatedAt": table.updatedAt
  }

def getRowByPrimaryId(session: Session, table: Base_Table, recordId: int):
  row = session.get(table, recordId)

  if (row is None):
    raise ValueError('Item not found')

  return row

def getPromptByID(session: Session, id: int):
  prompt = session.get(PromptTable, id);

  if (prompt is None):
    raise IndexError(f'Prompt with ID [id={id}] not found in database')
  
  return prompt

@database.transaction()
def createPrompt(createInput: CreatePromptDTO, *, session: Session):
  newRecord = PromptTable(**jsonable_encoder(createInput), createdAt=datetime.now(UTC), updatedAt=datetime.now(UTC))

  session.add(newRecord)
  session.flush()

  return toDTO(newRecord)

@database.transaction()
def deletePrompt(id: int, *, session: Session):
  prompt = getPromptByID(session, id)

  session.delete(prompt)

@database.transaction()
def findPrompt(filterParameters: PromptQuery, *, skip: int, limit: int, session: Session):
  query = select(PromptTable) 

  if ('value' in filterParameters):
    query = sqlalchemy_query.stringQueryBuilder(query, PromptTable.value, filterParameters.get('value')) 

  return {
    "prompts": [ toDTO(prompt) for prompt in session.scalars(query.limit(limit).offset(skip)).fetchmany() ],
    "paging": sqlalchemy_query.calculatePagination(session, query, skip, limit)
  }

@database.transaction()
def updatePrompt(id: int, createInput: CreatePromptDTO, *, session: Session):
  prompt = getPromptByID(session, id)

  lockedKeys = [ "id", "createdAt", "updatedAt" ]
  for key,value in createInput.__dict__.items():
    if key not in lockedKeys and value is not None:
      setattr(prompt, key, value)

  session.flush()

  return toDTO(prompt)

@database.transaction()
def addVersion(promptId: int, version, *, session: Session):
  pass

@database.transaction()
def deleteVersion(versionId: int, *, session: Session):
  pass

@database.transaction()
def updateVersion(versionId: int, *, session: Session):
  pass