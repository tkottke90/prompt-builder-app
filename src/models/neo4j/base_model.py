import datetime
import json
from typing import Dict, List, Optional

from pydantic import BaseModel
from .neo4j_db import query
from dataclasses import dataclass, field, astuple

@dataclass
class BaseDataClass:

  def __iter__(self):
    return iter(astuple(self))
  
  def getProperties(self):
    return self.__dict__

@dataclass
class Neo4JSchema():
  createdAt: datetime.datetime = field(default_factory=datetime.datetime.now)
  updatedAt: datetime.datetime = field(default_factory=datetime.datetime.now)

@dataclass
class Neo4jNodeDetails:
  id: Optional[str]
  labels: Optional[List[str]]


class Neo4JBaseDao(BaseModel):
  _nodeType: str

  def __init__(self, *, name: str = None):
    super().__init__()

    self._nodeType = name

  def _createConditional(self, variableName: str, properties: Dict):
    conditions = list()
    params = dict()
    
    for key, value in properties.items():
      if (value is None):
        continue

      queryValue = f'${key}'
      
      # This is a special case because the id is less a property in Neo4j and more
      # metadata on a node.  For this reason we cannot simply check for the value
      # using equality
      if (key == 'id'):
        conditions.append(f'id({variableName}) = {queryValue}')
      else:
        conditions.append(f'{variableName}.{key} = {queryValue}')
      
      params.update({ key: value })

    return ' AND '.join(conditions), params

  def _createNodeNotation(self, variableName: str = None):
    nodeType = self._nodeType if self._nodeType is not None else self.__class__.__name__
    queryVarName = variableName if variableName is not None else nodeType.lower()

    return queryVarName, f'({queryVarName}:{nodeType})'

  def _createParams(self, properties: Dict):
    """
    Utility function to create parameter strings for Cypher queries and a matching parameter dict.
      This helps guard db queries by using the driver and database protections for query injection by paramaterizeing the records

      Arguments:
        - {Neo4JSchema} properties: The properties of the object that will be used

      Returns:
        - {string} The parameter string which can be used in the cypher query.  All values are transformed to use the $<variable> syntax
    """
    placeholders = dict()

    for key,_ in properties.items():
      placeholders.update({ key: f'${key}' })

    return json.dumps(placeholders).replace('"', '')

  def _createReturnStr(self, elementKey: str, select: list[str] = None) -> str:
    """
    Creates a return string for a single neo4j node including the internal `id` field.

      Arguments:
        - elementKey: The name of the variable in the Cypher Query (used to target the element)
        - select: An optional list of property names to include in the response (similar to SQL Selectg)

      Details:
        - This is done using the Maps feature of Neo4j https://neo4j.com/docs/cypher-manual/current/values-and-types/maps/
    """

    idSetter = f'id: id({elementKey})'
    selectKeys = [ '.*' ]

    if (select is not None):
      selectKeys = []

      for key in select:
        selectKeys.append(f'.{key}')

    return elementKey + r'{' + ', '.join(selectKeys) + ', ' + idSetter + r'}'

  @query()
  def findNode(self, queryParams: BaseDataClass):
    operator = 'MATCH'
    queryVariableName, targetStr = self._createNodeNotation()
    conditions, params = self._createConditional(queryVariableName, queryParams.getProperties())

    returnStr = self._createReturnStr(queryVariableName)
    queryStr = f'{operator} {targetStr} WHERE {conditions} RETURN {returnStr}'

    return queryStr, params

  @query()
  def createNode(self, node: BaseDataClass):
    operator = 'CREATE'
    node.__setattr__('createdAt', datetime.datetime.now().isoformat())
    node.__setattr__('updatedAt', datetime.datetime.now().isoformat())
    paramStr = self._createParams(node.getProperties())

    returnStr = self._createReturnStr('n')
    queryStr = f'{operator} (n:{self._nodeType} {paramStr}) RETURN {returnStr};'

    return queryStr, node.getProperties()

  @query()
  def getNodeById(self, id: int):
    raise NotImplementedError('Not Implemented: getNodeById')

  @query()
  def getNodeLabels(self, id: int):
    operator = 'MATCH'
    
    conditions, params = self._createConditional('n', { "id": id })

    returnStr = r'{ id: id(n), labels: labels(n) }'
    queryStr = f'{operator} (n:{self._nodeType}) WHERE {conditions} RETURN {returnStr};'

    print(queryStr, params)

    return queryStr, params

  @query()
  def createOrUpdate(self, node: BaseDataClass):
    node.__setattr__('updatedAt', datetime.datetime.now().isoformat())
    raise NotImplementedError('Not Implemented: createOrUpdate')
  
  @query()
  def update(self, node: BaseDataClass):
    raise NotImplementedError('Not Implemented: update')

  @query()
  def delete(self, node: BaseDataClass):
    raise NotImplementedError('Not Implemented: delete')