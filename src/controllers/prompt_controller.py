from fastapi import APIRouter, Request, HTTPException
from src.dao import prompt_dao
from src.models.prompt_model import CreatePromptDTO, PromptDTO, UpdatePromptDTO
from src.models.query_params import DateFieldQueryModel, StringFieldQueryModel
from src.utils import sqlalchemy_query, string_util
from src.utils.hateos_util import hateosParentPopulator, hateosSelfPopulator

PROMPTS_PATH = "/prompts"

router = APIRouter(
  prefix=PROMPTS_PATH
)

def promptsPopulator(data: PromptDTO):
  return hateosParentPopulator(hateosSelfPopulator(data, PROMPTS_PATH), PROMPTS_PATH)

@router.post('/', status_code=201)
def create(prompt: CreatePromptDTO):
  return promptsPopulator(prompt_dao.createPrompt(prompt))
  

@router.get('/')
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
    return hateosParentPopulator({
      "prompts": result.get('prompts'),
      "query": string_util.urlQueryDecode(request.url.query),
      "paging": result.get('paging')
    }, PROMPTS_PATH)
  except sqlalchemy_query.IndexOutOfBoundsError as boundsErr:
    raise HTTPException(400, 'BadRequest: Query Exceeded the number of items')

@router.patch('/{prompt_id}')
def update(prompt_id: int, prompt: UpdatePromptDTO):
  return promptsPopulator(prompt_dao.updatePrompt(prompt_id, prompt))

@router.delete('/{prompt_id}', status_code=203)
def remove(prompt_id: int):
  prompt_dao.deletePrompt(prompt_id)