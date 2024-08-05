from src.models import prompt_model, base_model
import datetime
import json
import pytest

def promptTableVersion(createdAt: datetime.datetime | None = None):
  if (createdAt is None):
    createdAt = datetime.datetime.now()

  return prompt_model.PromptVersionTable(
    id=1,
    createdAt=createdAt,
    updatedAt=createdAt,
    index="",
    previous="",
    next="",
    prompt="",
    comments=""
  )


def promptTable(createdAt: datetime.datetime | None = None):
  if (createdAt is None):
    createdAt = datetime.datetime.now()
  
  version = promptTableVersion(createdAt)
  version.prompt = 'This is a test prompt for testing'

  return prompt_model.PromptTable(
    id=1,
    createdAt=createdAt,
    updatedAt=createdAt,
    tags='',
    label='Test Prompt',
    value=version.prompt,
    versions=[version]
  )

class TestPromptTable():
  def test_table_dto(self):
    """
    Testing the #toDTO method to ensure it returns the expected structure.  This test will primarily ensure
    that the toDTO function is aligned to the DTO that it should be generating
    """
    # Arrange
    prompt = promptTable()
    
    # Act
    dto = prompt.toDTO()

    # Assert
    assert isinstance(dto, dict)
    assert dto == {
      "id": 1,
      "value": 'This is a test prompt for testing',
      "label": 'Test Prompt',
      "tags": [''],
      "createdAt": prompt.createdAt,
      "updatedAt": prompt.updatedAt,
      "versions": [
        {
          "id": 1,
          "index": '',
          "prompt": 'This is a test prompt for testing',
          "comments": '',
          "previous": '',
          "next": '',
          "createdAt": prompt.versions[0].createdAt,
          "updatedAt": prompt.versions[0].createdAt
        }
      ],
      "hasChanges": False
    }
    assert prompt_model.PromptDTO.model_validate_json(json.dumps(dto))