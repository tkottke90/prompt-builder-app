from typing import List
from src.models.neo4j.base_model import Neo4JBaseDao
from src.models.neo4j.email_model import Email, FindEmail, CreateEmail

class EmailDao(Neo4JBaseDao):
  def __init__(self):
    super().__init__(
      name='Email'
    )

  def findNode(self, queryParams: FindEmail) -> List[Email]:
    return [Email(**record) for record in super().findNode(queryParams)]
  
  def findById(self, id: int):
    return super().findById

  def createNode(self, email: CreateEmail) -> Email:
    return Email(**super().createNode(email)[0])
  
  def getNodeLabels(self, id: int) -> Email:
    nodeList = self.findNode(FindEmail(id=id))

    if (len(nodeList) == 0):
      raise KeyError(f'Record with id ({id}) not found in database')
    
    node = nodeList[0]

    response = super().getNodeLabels(node.id)

    return response[0]