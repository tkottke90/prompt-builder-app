from typing import Callable, List, Protocol, TypeVar
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import Runnable

CallableTemplateFactory = TypeVar('CallableTemplateFactory', bound=Callable)
class TemplateFactory(Protocol[CallableTemplateFactory]):

  def __call__(self, template: str, partial_variables: dict[str, str]): ...


def createFormatInstructions(schemas: list[ResponseSchema]):
  """
  Generates format instructions for an LLM Prompt using the Response Schema system
  """
  return StructuredOutputParser.from_response_schemas(schemas).get_format_instructions()

def createPromptWithFormat(
  *,
  prompt: str,
  schema: List[ResponseSchema],
  templateFactory: TemplateFactory | None = None,
  format_key: str = "format_instructions"
) -> Runnable:
  fnArguments = {
    'template': prompt,
    'partial_variables': {
      f'{format_key}': createFormatInstructions(schema)
    }
  }
  
  if isinstance(templateFactory, Callable):
    templateFactory(**fnArguments)
  else:
    return ChatPromptTemplate.from_template(**fnArguments )

