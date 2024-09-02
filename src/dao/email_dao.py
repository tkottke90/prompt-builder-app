from src.models.neo4j.base_model import Neo4JBaseDao
from src.models.neo4j.email_model import Email, FindEmail, CreateEmail

class EmailDao(Neo4JBaseDao):
  def __init__(self):
    super().__init__(
      name='Email'
    )

  def findNode(self, queryParams: FindEmail):
    return super().findNode(queryParams)

  def createNode(self, email: CreateEmail):
    return super().createNode(email)