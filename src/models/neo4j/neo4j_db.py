import os
import functools
from langchain_core.embeddings import Embeddings
from langchain_community.chat_message_histories import Neo4jChatMessageHistory
from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector
from typing import Dict, List, Protocol, Optional
from logging import Logger, getLogger



neo4jLogger = getLogger('Neo4J_DB');
neo4jLogger.setLevel('DEBUG')

NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_URL = os.getenv('NEO4J_URL')
NEO4J_DB = os.getenv('NEO4J_DB')

class VectorDBOptions(Protocol):
  keyword_index_name: Optional[str]
  index_name: Optional[str]
  node_label: Optional[str]
  embedding_node_property: Optional[str]
  text_node_property: Optional[str]
  logger: Optional[Logger]

class ChatHistoryOptions(Protocol):
  node_label: Optional[str]

@functools.cache
def getGraphDB():
  return Neo4jGraph(
    url=NEO4J_URL,
    database=NEO4J_DB,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD
  )

def getVectorDB(embedding: Embeddings, **kwargs: VectorDBOptions):
  return Neo4jVector(
    url=NEO4J_URL,
    database=NEO4J_DB,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    embedding=embedding,
    **kwargs
  )

def getChatHistory(userSessionId: str, **kwargs: ChatHistoryOptions):
  return Neo4jChatMessageHistory(
    url=NEO4J_URL,
    database=NEO4J_DB,
    session_id=userSessionId,
    node_label='ChatSession',
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    **kwargs
  )

def parseResponse(response: List[Dict]):
  records = [];

  for result in response:
      record = dict()
      for value in result.values():
        record.update(value)

      records.append(record)

  return records

def query():
  def functionWrapper(fn):
    def executionWrapper(*args, **kwargs):
      db = getGraphDB()

      queryStr, paramsDict = fn(*args, **kwargs)

      neo4jLogger.debug('Querying Neo4jDB', extra={ "query": queryStr, "params": paramsDict })


      return parseResponse(db.query(queryStr, paramsDict))

    return executionWrapper
  return functionWrapper