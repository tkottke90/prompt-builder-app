from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_community.chat_models.ollama import ChatOllama
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from pydantic import BaseModel, Field
from src.models.prompt_model import PromptDTO
from src.exceptions import api_input
from src.utils import ollama_util
from typing import Any
import json
import logging
import re

from src.utils import prompt_util

def formatInstructions(schemas: list[ResponseSchema]):
  return StructuredOutputParser.from_response_schemas(schemas).get_format_instructions()

PROMPT_INPUT_REGEX = re.compile('(\{([^!:}]*)(?:[:!]?([^}]*))?\})', re.DOTALL)

EvaluatorLogger = logging.getLogger('Evaluator')

testllm = ChatOllama(
  model="mistral:7b",
  temperature=0.1
)

scoreLLM = ChatOllama(
  model="mistral:7b",
  temperature=0.0,
  format="json"
)

class PromptArgument(BaseModel):
  label: str = Field()
  formatting: str = Field()

def validatePromptInput(prompt: ChatPromptTemplate, input: dict):
  "Validates that a input dict contains all of the required string formatting keys"
  missing = [ inputVar for inputVar in prompt.input_variables if inputVar not in input ]

  if (len(missing) > 0):
    raise api_input.MissingInputError(
      expected=prompt.input_variables,
      missing=missing
    ) 

def scoreGeneration(prompt: str, generation: str):
  template = prompt_util.createPromptWithFormat(
    schema=[
      ResponseSchema(name="score", description="a grading between 0 and 10 of how well the llm responds to the humans request", type="float"),
      ResponseSchema(name="score_explanation", description="a description of why the response received that score"),
    ],
    prompt="""# Instructions
You are an AI Assistant specializing in Generative AI using Natural Language.
You task is to evaluate the following LLM Prompt Template and LLM Response and provide feedback to the template author to assist them in generating an effective prompt for LLM driven applications.
Use the step by step program provided below to evaluate Prompt Template and Generated Response.
"Prompt Template" was the template provided to the LLM by the user
"Generated Response" was a response generated by an LLM when provided with the template
You should respond using the following format:

{format_instructions}

## Human Request
{template}

## LLM Response
{generation}

# Program
1. generate a score between 0 and 10 of how well the Generated Response responded to the Prompt Template
2. explain why this score was given based on your analysis 
"""
  )

  EvaluatorLogger.info(msg=f'Starting test for prompt', extra={ "prompt": template.format(template="", generation="") })

  result = ollama_util.jsonChat(template, options={ 'temperature': 0.1 }).invoke(input={ "template": prompt, "generation": generation })
  response = result.get('response')
  tokens = result.get('tokens')

  return {
    "score": response.get('score', -1),
    "score_explanation": response.get('score_explanation', 'Missing Explanation'),
    "token_usage": tokens
  }

def testPrompt(prompt: PromptDTO, args: list[Any], kwargs: dict[str, Any]):
  """
  Call LLM using a provided prompt and return the results of that prompt
  """
  fnLogger = EvaluatorLogger.getChild('testPrompt')
  fnLogger.info(msg=f'Starting test for prompt: {prompt.get("id")}', extra={ "inputs": kwargs })

  template = ChatPromptTemplate.from_template(template=prompt.get('value'))
  fnLogger.debug('Validating Input', extra={ "keys": template.input_variables })

  validatePromptInput(template, kwargs)

  chain = template | testllm

  result = chain.invoke(input=kwargs)

  EvaluatorLogger.info(msg=f'Test complete', extra={ "run_id": result.id, "response": result })

  return (result.content, template.format(**kwargs))

def getPromptInputs(prompt: PromptDTO):
  """
    Extracts the placeholders in a prompt.  Returning labeled placeholders as keyword args and unlabeled as positional args
  """
  positionalArgs: list[PromptArgument] = []
  keywordArgs: dict[str, PromptArgument] = {}

  for (match, key, formatting) in re.findall(PROMPT_INPUT_REGEX, prompt.get('value')):
    arg = PromptArgument(label=match, formatting=formatting)

    if (len(key) == 0):
      positionalArgs.append(arg)
    else:
      keywordArgs.update({ key: arg })


  return {
    "positional": positionalArgs,
    "keyword": keywordArgs
  }