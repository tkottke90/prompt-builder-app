import datetime
import json

from enum import StrEnum
from pydantic import BaseModel
from src.models.neo4j.neo4j_db import getGraphDB
from dataclasses import astuple, dataclass
from typing import Dict, List, Optional, TypeVar, Generic

EdgeModel = TypeVar('EdgeModel');

class Neo4jOperator(StrEnum):
  CREATE = 'CREATE'
  MATCH = 'MATCH'

@dataclass
class Neo4jBaseModel:

  def __iter__(self):
    return iter(astuple(self))
  
  def getProperties(self):
    return self.__dict__

@dataclass
class Neo4jNodeMetadata:
  id: int
  labels: Optional[List[str]]


class Neo4JBaseDao(BaseModel, Generic[EdgeModel]):
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

  def _createIdConditional(self, variableKey: str, id: int):
    return self._createConditional(variableKey, { "id": id })

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
  
  def _parseResults(self, variableKey: str, result: Dict):
    """
    Parses the output of the Neo4j Query which uses this structure:
      Query: MATCH (n:User)-[r]-() RETURN n,r;
      Response: [{ "n": { "name": "John" }, "r": { "type": "FRIEND_OF" } }]

      The response create an array of objects, where each item has a key for each variable used in the query.  In the above example
      that is the "n" variable used to collect nodes/edges with the "User" label and the "r" variable is for vertex/relationships
      with that node. This function helps grab an value of an individual variable from the output

      Arguments:
        - result: An individual element from a Neo4j Cypher response

      Returns:
        A Dictionary with the nested value for the element.
    """
    if (variableKey in result):
      return result[variableKey]
    else:
      raise KeyError(f'The Neo4J Output did not contain a value for {variableKey}')

  def _queryDatabase(self, queryStr: str, params: Dict):
    db = getGraphDB()

    return db.query(queryStr, params)

  def findNode(self, queryParams: Neo4jBaseModel) -> List[Dict]:
    operator = Neo4jOperator.MATCH
    queryVariableName, targetStr = self._createNodeNotation()
    conditions, params = self._createConditional(queryVariableName, queryParams.getProperties())

    returnStr = self._createReturnStr(queryVariableName)
    queryStr = f'{operator} {targetStr} WHERE {conditions} RETURN {returnStr}'

    resultList = self._queryDatabase(queryStr, params)

    return [self._parseResults(queryVariableName, result) for result in resultList]

  def createNode(self, node: Neo4jBaseModel):
    operator = Neo4jOperator.CREATE
    node.__setattr__('createdAt', datetime.datetime.now().isoformat())
    node.__setattr__('updatedAt', datetime.datetime.now().isoformat())
    paramStr = self._createParams(node.getProperties())

    returnStr = self._createReturnStr('n')
    queryStr = f'{operator} (n:{self._nodeType} {paramStr}) RETURN {returnStr};'

    resultList = self._queryDatabase(queryStr, node.getProperties())

    return self._parseResults('n', resultList[0])

  def getNodeById(self, id: int):
    operator = Neo4jOperator.MATCH

    conditions, params = self._createConditional('n', { "id": id })
    queryStr = f'{operator} (n:{self._nodeType}) WHERE {conditions} RETURN n'

    return self._queryDatabase(queryStr, params)

  def getNodeLabels(self, id: int):
    operator = Neo4jOperator.MATCH
    
    conditions, params = self._createConditional('n', { "id": id })

    returnStr = r'n{ id: id(n), labels: labels(n) }'
    queryStr = f'{operator} (n:{self._nodeType}) WHERE {conditions} RETURN {returnStr};'

    result = self._queryDatabase(queryStr, params)

    return self._parseResults('n', result[0])
  
  def delete(self, node: Neo4jBaseModel):
    raise NotImplementedError('Not Implemented: delete')

  def update(self, node: Neo4jBaseModel):
    raise NotImplementedError('Not Implemented: update')
  
  def toDTO(self, record: Dict) -> EdgeModel:
    raise NotImplementedError(f'{self.__class__.__name__} does not implement a `toDTO` function')

  def toPersistance(self, record: EdgeModel) -> Dict:
    raise NotImplementedError(f'{self.__class__.__name__} does not implement a `toPersistance` function')
