from src.models import prompt_model
import datetime

def createMockPromptTableVersion(createdAt: datetime.datetime | None = None):
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


def createMockPromptTable(createdAt: datetime.datetime | None = None):
  if (createdAt is None):
    createdAt = datetime.datetime.now()
  
  version = createMockPromptTableVersion(createdAt)
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
    prompt = createMockPromptTable()
    newPromptLabel = "Old Prompt"
    newPromptTags = [ 'DEPRECATED' ]

    changes: prompt_model.UpdatePromptDTO = { "label": newPromptLabel, "tags": newPromptTags }

    # Act
    prompt.toPersistance(changes)

    # Assert
    assert prompt.label == newPromptLabel
    assert prompt.tags == ','.join(newPromptTags)

  def test_table_toPersistance(self):
    # Arrange
    prompt = createMockPromptTable()
    
    # Act


    # Assert
    assert True == True

class TestPromptVersionTable():
  def test_table_dto(self):
    """
    Testing the #toDTO method to ensure it returns the expected structure.  This test will primarily ensure
    that the toDTO function is aligned to the DTO that it should be generating
    """
    # Arrange
    version = createMockPromptTableVersion()
    version.prompt = 'This is a test prompt for testing'
    
    # Act
    dto = version.toDTO()

    # Assert
    assert isinstance(dto, dict)
    assert dto == {
      "id": 1,
      "index": '',
      "prompt": 'This is a test prompt for testing',
      "comments": '',
      "previous": '',
      "next": '',
      "createdAt": version.createdAt.isoformat(),
      "updatedAt": version.createdAt.isoformat()
    }