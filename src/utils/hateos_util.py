from typing import Callable, Dict, TypeVar, Any

T = TypeVar('T')

MappingAction = str | Callable[[T], str] | Dict[str, Any]
Mapping = Dict[str, MappingAction]

def metadataPopulator(data: T, mapping: Mapping):
  def executeAction(record: T, action: MappingAction):
    if (isinstance(action, Callable)):
      return action(record)
    elif (isinstance(action, dict)):
      return {
        key: executeAction(record, childAction)
        for key,childAction in action.items()
      }
    else:
      return action

  data.update({
    key: executeAction(data, action)
    for key,action in mapping.items()
  })

  return data


def hateosSelfPopulator(data: T, rootPath: str, key: str = 'id'):
  return metadataPopulator(
    data,
    {
      "self": lambda record: f"{rootPath}/{record[key]}"
    }
  )

def hateosParentPopulator(data: T, rootPath: str):
  return metadataPopulator(
    data,
    {
      "parent": lambda _: f"{rootPath}"
    }
  )