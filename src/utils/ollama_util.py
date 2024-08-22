from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel
from typing import TypedDict
import json

class OllamaChatResponse(TypedDict):
  response: dict

class JsonChatOptions(TypedDict):
  model: str
  temperature: float

def chat(template: Runnable, **options: JsonChatOptions) -> Runnable:
  llm = ChatOllama(
    model=options.get('model') or 'mistral:7b',
    temperature=options.get('temperature') or 0.0,
    format="json"
  )

def jsonChat(template: Runnable, **options: JsonChatOptions) -> Runnable:
  llm = ChatOllama(
    model=options.get('model') or 'mistral:7b',
    temperature=options.get('temperature') or 0.0,
    format="json"
  )

  return template | llm | RunnableParallel({
    'response': RunnableLambda(lambda x: json.loads(x.content)),
    'tokens': RunnableLambda(lambda x: llm.get_num_tokens_from_messages([x]))
  })
