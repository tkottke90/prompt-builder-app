from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
import re

PROMPT_INPUT_REGEX = re.compile('(\{([^!:}]*)(?:[:!]?([^}]*))?\})', re.DOTALL)

class PromptArgument(BaseModel):
  label: str = Field()
  formatting: str = Field()

def getPromptInputs(prompt: str):
  positionalArgs: list[PromptArgument] = []
  keywordArgs: dict[str, PromptArgument] = {}

  for (match, key, formatting) in re.findall(PROMPT_INPUT_REGEX, prompt):
    arg = PromptArgument(label=match, formatting=formatting)

    if (len(key) == 0):
      positionalArgs.append(arg)
    else:
      keywordArgs.update({ key: arg })


  return {
    "positional": positionalArgs,
    "keyword": keywordArgs
  }