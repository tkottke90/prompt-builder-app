from typing import Callable, Dict, TypeVar

T = TypeVar('T')

MappingAction = str | Callable[[T], str]
Mapping = Dict[str, MappingAction]

def metadataPopulator(data: T, mapping: Mapping):
  def executeAction(data: T, action: MappingAction):
    if (isinstance(action, str)):
      return action
    else:
      return action(data)

  data.update({
    key: executeAction(data, action)
    for key,action in mapping.items()
  })

  return data


def hateosSelfPopulator(data: T, rootPath: str, key: str = 'id'):
  return metadataPopulator(
    data,
    {
      "self": lambda record: f"{rootPath}/{record.get(key)}"
    }
  )

def hateosParentPopulator(data: T, rootPath: str):
  return metadataPopulator(
    data,
    {
      "parent": lambda _: f"{rootPath}"
    }
  )