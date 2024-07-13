import src.database as database
from src.models import prompt_model
from src.models.prompt_model import CreatePromptDTO, PromptTable, PromptQuery
from datetime import datetime, UTC
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.utils import sqlalchemy_query, string_util
from fastapi.encoders import jsonable_encoder
from datetime import datetime

class ValueHasNoChangeError(Exception):
  def __init__(self, message, *args: object) -> None:
    self.message = f'ValueHasNoChangeError: {message}'

    self.detail = {
      "name": "PromptHasNoChangeError",
      "description": "Prompt matches current version.  Make changes to the prompt before adding a version"
    }
    super().__init__(self.detail, self.message, *args)

def getRowByPrimaryId(session: Session, recordId: int):
  return sqlalchemy_query.getRowByPrimaryId(session, prompt_model, recordId)

def getPromptByID(session: Session, id: int):
  prompt = session.get(PromptTable, id);

  if (prompt is None):
    raise IndexError(f'Prompt with ID [id={id}] not found in database')
  
  return prompt

@database.transaction()
def createPrompt(createInput: CreatePromptDTO, *, session: Session):
  createInput.tags = ','.join(createInput.tags) if 'tags' in createInput else ''
  newRecord = PromptTable(
    **jsonable_encoder(createInput),
    createdAt=datetime.now(UTC),
    updatedAt=datetime.now(UTC),
    versions=[
      prompt_model.PromptVersionTable(
        index=string_util.checksum(createInput.value),
        prompt=createInput.value,
        comments="",
        createdAt=datetime.now(UTC),
        updatedAt=datetime.now(UTC),
      )
    ]
  )

  session.add(newRecord)
  session.flush()

  return newRecord.toDTO()

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
    "prompts": [ prompt.toDTO() for prompt in session.scalars(query.limit(limit).offset(skip)).fetchmany() ],
    "paging": sqlalchemy_query.calculatePagination(session, query, skip, limit)
  }

@database.transaction()
def updatePrompt(id: int, dto: prompt_model.UpdatePromptDTO, *, session: Session):
  prompt = getPromptByID(session, id)
  prompt.toPersistance(dto)

  session.flush()

  return prompt.toDTO()

@database.transaction()
def addVersionCommit(promptId: int, *, session: Session):
  prompt = getPromptByID(session, promptId)
  currentVersion = prompt.versions[-1]
  
  promptValueChecksum = string_util.checksum(prompt.value)
  currentVersionChecksum = string_util.checksum(currentVersion.prompt)

  if (promptValueChecksum == currentVersionChecksum):
    raise ValueHasNoChangeError('Prompt has not been changed from previous versions')

  newVersion = prompt_model.PromptVersionTable(
    index = string_util.checksum(prompt.value),
    previous = currentVersion.index,
    prompt = prompt.value
  )

  currentUpdates = prompt_model.UpdatePromptVersionDTO(
    next=newVersion.index,
  )
  
  currentVersion.toPersistance(currentUpdates)
  prompt.versions.append(newVersion)
  session.flush()
  
  return prompt.toDTO()
