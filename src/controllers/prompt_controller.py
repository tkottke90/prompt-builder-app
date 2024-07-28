from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from src.dao import prompt_dao
from src.models.prompt_model import CreatePromptDTO, PromptDTO, UpdatePromptDTO, UpdatePromptVersionDTO, PromptVersionDTO
from src.models.query_params import DateFieldQueryModel, StringFieldQueryModel
from src.utils import sqlalchemy_query, string_util, hateos_util
from src.services import evaluator
from typing import List
import logging
import traceback

controllerLogger = logging.getLogger('Controllers.PromptController')

PROMPTS_PATH = "/prompts"
PROMPT_VERSION_PATH = "/prompts/{promptId}/versions"

router = APIRouter(
  prefix=PROMPTS_PATH,
  tags=["Prompts"]
)

def promptsPopulator(data: PromptDTO):
  return hateos_util.hateosParentPopulator(hateos_util.hateosSelfPopulator(data, PROMPTS_PATH), PROMPTS_PATH)

def promptVersionHateos(data: PromptVersionDTO):
  return hateos_util.hateosParentPopulator(hateos_util.hateosSelfPopulator(data, PROMPT_VERSION_PATH, PROMPTS_PATH))

def addHatos(data: List[PromptDTO]):
  for index,prompt in enumerate(data):
    data[index] = hateos_util.hateosParentPopulator(prompt, PROMPTS_PATH)
    data[index] = hateos_util.hateosSelfPopulator(prompt, PROMPTS_PATH)
    promptVersionPath = PROMPT_VERSION_PATH.format(promptId=prompt.get('id'))

    [
      hateos_util.hateosSelfPopulator(hateos_util.metadataPopulator(version, { "parent": data[index].get('self') }), promptVersionPath)
      for version in prompt.get('versions')
    ]
  
  return data

@router.post('/', status_code=201, description="Create a new prompt in the database", name="Create New Prompt")
def create(prompt: CreatePromptDTO):
  controllerLogger.debug('Creating New Prompt', extra={ "value": prompt.value, "label": prompt.label })
  return addHatos([prompt_dao.createPrompt(prompt)]).pop()
  
@router.get('/', description="Find a prompt", name="Prompt Search")
def find(
  request: Request,
  skip: int = 0,
  limit: int = 10
):
  try:
    result = prompt_dao.findPrompt(
      filterParameters=sqlalchemy_query.parseQueryParamsToDict(request.query_params),
      skip=skip,
      limit=limit
    )

    return {
      "prompts": addHatos(result.get('prompts', [])),
      "query": string_util.urlQueryDecode(request.url.query),
      "paging": result.get('paging')
    }
  except sqlalchemy_query.IndexOutOfBoundsError as boundsErr:
    raise HTTPException(400, 'BadRequest: Query Exceeded the number of items')

@router.patch('/{prompt_id}', description="Update prompt details", name="Update Prompt")
def update(prompt_id: int, prompt: UpdatePromptDTO):
  return addHatos([
    prompt_dao.updatePrompt(prompt_id, prompt)
  ]).pop()

@router.delete('/{prompt_id}', status_code=203, description="Delete a Prompt")
def remove(prompt_id: int):
  prompt_dao.deletePrompt(prompt_id)

@router.post('/{promptId}/version/commit', description="Save the current prompt changes as a version")
def createRouterCommit(promptId: int):
  try:
    return addHatos([prompt_dao.addVersionCommit(promptId)]).pop()
  except prompt_dao.ValueHasNoChangeError as valueError:
    controllerLogger.error('Prompt commit rejected - no changes detected', extra={ "promptId": promptId, "source": "createRouterCommit" })
    raise HTTPException(status_code=400, detail=valueError.message)
  except IndexError as indexError:
    controllerLogger.error('Prompt commit rejected - no changes detected', extra={ "promptId": promptId, "rootError": indexError.__repr__(), "source": "createRouterCommit" })
    raise HTTPException(status_code=404, detail="Not Found")
  except Exception as e:
    controllerLogger.error(f'Prompt commit rejected - {type(e)}', extra={ "promptId": promptId, "rootError": indexError.__repr__(), "source": "createRouterCommit" })
    raise HTTPException(status_code=404, detail="Not Found")
 
@router.get('/{promptId}/evaluator/inputs', description="Get a prompt's template inputs")
def getPromptInputs(promptId: int):
  try:
    prompt = prompt_dao.getPrompt(promptId)

    return evaluator.getPromptInputs(prompt)

  except IndexError as indexError:
    print(indexError)
    controllerLogger.error('Prompt commit rejected - no changes detected', extra={ "promptId": promptId, "rootError": indexError.__repr__(), "source": "getPromptInputs" })
    raise HTTPException(status_code=404, detail="Not Found")
  except Exception as e:
    controllerLogger.error(f'Prompt commit rejected - {type(e)}', extra={ "promptId": promptId, "rootError": e.__repr__(), "source": "getPromptInputs" })
    raise HTTPException(status_code=404, detail="Not Found")
  
@router.post('/{promptId}/evaluator/test', name="Generate LLM Response from Prompt", description="Execute a prompt with the given input values")
def getPromptInputs(promptId: int, body: dict):
  try:
    prompt = prompt_dao.getPrompt(promptId)

    return evaluator.testPrompt(prompt, [], body)

  except HTTPException as httpException:
    raise httpException
  except Exception as e:
    controllerLogger.error(f'Prompt commit rejected - {type(e)}', extra={ "promptId": promptId, "rootError": e.__repr__(), "source": "getPromptInputs", "trace": traceback.format_exception(e) })
    raise HTTPException(status_code=500, detail="Server Error")
  
@router.post('/{promptId}/evaluator/score', name="Score LLM Response", description="Execute an LLM Generation with the given prompt. Then ask the LLM to score the response and provide feedback")
def getPromptInputs(promptId: int, body: dict):
  try:
    prompt = prompt_dao.getPrompt(promptId)

    (result, template) = evaluator.testPrompt(prompt, [], body)

    return {
      "result": result,
      "template": template,
      "score": evaluator.scoreGeneration(template, result)
    }

  except HTTPException as httpException:
    raise httpException
  except Exception as e:
    controllerLogger.error(f'Prompt commit rejected - {type(e)}', extra={ "promptId": promptId, "rootError": e.__repr__(), "source": "getPromptInputs", "trace": traceback.format_exception(e) })
    raise HTTPException(status_code=500, detail="Server Error")