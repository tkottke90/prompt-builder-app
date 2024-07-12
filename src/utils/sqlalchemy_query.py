import json
import re
from math import ceil
from sqlalchemy import Select, Tuple, select, func
from sqlalchemy.orm import Query, InstrumentedAttribute, Session, FromStatement
from src.models.base_model import Base_Table
from src.models.query_params import StringFieldQueryModel
from src.utils.string_util import caseInsensitiveMatch

class IndexOutOfBoundsError(Exception):
  def __init__(self, index: int, upperBound: int):
    super().__init__(f"Index [{index}] is outside the upper bounds [{upperBound}]")

NESTED_QUERY_REGEX = re.compile(r'(^(\w+)(?:\[(\w+)\]))', re.DOTALL)

def calculatePagination(session: Session, subQuery, skip: int, limit: int):
  count = session.execute(getCountQuery(subQuery)).scalar_one()

  if (skip > count):
    raise IndexOutOfBoundsError(skip, count)

  return {
    "total": ceil(count / limit),
    "current": ceil(skip / limit) if (skip > 0) else 1,
    "next": {
      "skip": skip + limit if (skip + limit) <= count else -1,
      "limit": limit
    },
    "previous": {
      "skip": skip - limit if (skip - limit) >= 0 else -1,
      "limit": limit
    }
  }

def getCountQuery(index: InstrumentedAttribute):
  return select(func.count()).select_from(select(index).subquery())

def getCountQuery(subQuery):
  return select(func.count()).select_from(subQuery)

def getRowByPrimaryId(session: Session, table: Base_Table, recordId: int):
  row = session.get(table, recordId)

  if (row is None):
    raise ValueError('Item not found')

  return row

def parseQueryKey(key: str, value, target: dict):
  _key = str(key)

  result = re.search(NESTED_QUERY_REGEX, _key)

  if result is None:
    target[_key] = value
  else:
    matchedPattern = result.group(1)
    currentKey = result.group(2)
    childKey = result.group(3)

    nextKey = _key.replace(matchedPattern, childKey)

    if (currentKey in target):
      target[currentKey] =  parseQueryKey(nextKey, value, target.get(currentKey))
    else:
      target[currentKey] = parseQueryKey(nextKey, value, {})

    
  return target

def parseQueryParamsToDict(query_params: dict):
  queryDict = {}

  for key,value in query_params.items():
    keyDetails = parseQueryKey(key, value, queryDict)

    queryDict.update(keyDetails)

  return queryDict

def stringQueryBuilder(query: Query, key: InstrumentedAttribute, filter: StringFieldQueryModel):
  if isinstance(filter, str) or 'eq' in filter:
    return query.where(key == filter)
  else:
    for filterKey,value in dict(filter).items():
      if (caseInsensitiveMatch(filterKey, 'startsWith')):
        return query.where(key.startswith(value))
      elif (caseInsensitiveMatch(filterKey, 'endsWith')):
        return query.where(key.endswith(value))
      elif (caseInsensitiveMatch(filterKey, 'like')):
        return query.where(key.like(value))
      elif (caseInsensitiveMatch(filterKey, 'nlike')):
        return query.where(key.not_like(value))
