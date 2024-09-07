from typing import Dict
from src.dao.base_dao.neo4j_base_dao import Neo4JBaseDao
from src.models.neo4j.base_model import Neo4jNodeMetadata
from src.models.neo4j.email_model import Email, FindEmail, CreateEmail

class EmailDao(Neo4JBaseDao):
  def __init__(self):
    super().__init__(
      name='Email'
    )

  def findNode(self, queryParams: FindEmail):
    return [self.toDTO(record) for record in super().findNode(queryParams)]
  
  def findById(self, id: int):
    return self.toDTO(super().getNodeById(id))

  def createNode(self, email: CreateEmail):
    return self.toDTO(super().createNode(email)[0])
  
  def getNodeLabels(self, id: int):
    nodeList = self.findNode(FindEmail(id=id))

    if (len(nodeList) == 0):
      raise KeyError(f'Record with id ({id}) not found in database')
    
    node = nodeList[0]
    return Neo4jNodeMetadata(**super().getNodeLabels(node.id))
  
  def toDTO(self, record: Dict):
    return Email(**record);