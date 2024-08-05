from src.utils import hateos_util
import pytest

class TestMetadataPopulator():
  """
  Tests the #caseInsensitiveMatch() function
  """

  def test_string_value(self):
    """
    An attribute should be added with a string value when passed a dict[str, str]
    """ 
    # Arrange
    existingObject = { "id": 1 }
    newItem = { "label": "test_one_value" }

    # Act
    hateos_util.metadataPopulator(
      existingObject,
      newItem
    )

    # Assert
    assert existingObject.get('id') == 1
    assert existingObject.get('label') == newItem.get('label')

  def test_callable_value(self):
    """
    An attribute should be added with a string value when passed a dict[str, Callable]
    """ 
    # Arrange
    existingObject = { "id": 1 }
    newItem = { "label": lambda data: f"user-{data.get('id')}" }

    # Act
    hateos_util.metadataPopulator(
      existingObject,
      newItem
    )

    # Assert
    assert existingObject.get('id') == 1
    assert existingObject.get('label') == 'user-1'

  def test_multiple_inputs(self):
    """
    An attribute should be added with a string value when passed
    """ 
    # Arrange
    existingObject = { "id": 1 }
    newItem = {
      "index": lambda data: f"user-{data.get('id')}",
      "status": "Under-Review"
    }

    # Act
    hateos_util.metadataPopulator(
      existingObject,
      newItem
    )

    # Assert
    assert existingObject.get('id') == 1
    assert existingObject.get('index') == 'user-1'
    assert existingObject.get('status') == 'Under-Review'

  def test_nested(self):
    """
    An attribute should be added with a string value when passed a nested string value
    """ 
    # Arrange
    existingObject = { "id": 1 }
    newItem = {
      "links": {
        "knowledge_base": "https://example.com/kb"
      }
    }

    # Act
    hateos_util.metadataPopulator(
      existingObject,
      newItem
    )

    # Assert
    assert existingObject.get('id') == 1 # Existing key is retained
    assert existingObject['links']['knowledge_base'] == newItem['links']['knowledge_base']

  def test_nested_callable(self):
    """
    An attribute should be added with a string value when passed a nested string value
    """ 
    # Arrange
    existingObject = { "id": 1 }
    newItem = {
      "links": {
        "knowledge_base": lambda record: f'https://example.com/kb/{record.get("id")}'
      }
    }

    # Act
    hateos_util.metadataPopulator(
      existingObject,
      newItem
    )

    # Assert
    assert existingObject.get('id') == 1 # Existing key is retained
    assert existingObject['links']['knowledge_base'] == 'https://example.com/kb/1'

class TestHateosSelfPopulator():
  """
  Tests the #hateosSelfPopulator() function
  """

  def test_add_self(self):
    """
    Should add a `self` property to the provided dict
    """ 
    # Arrange
    person = { "id": 1, "displayName": "John Smith" }

    # Act
    hateos_util.hateosSelfPopulator(person, '/person')

    # Assert
    assert person.get('self') == '/person/1'

  def test_missing_key(self):
    """
    Should throw a KeyError when the key doesn't exist in the provided object
    """
    # Arrange
    with pytest.raises(KeyError):
      person = { "id": 1, "displayName": "John Smith" }

      # Act
      hateos_util.hateosSelfPopulator(person, '/person', 'index')

class TestHateosParentPopulator():
  """
  Tests the #hateosParentPopulator() function
  """

  def test_parent_population(self):
    """
    Should add a `parent` property to the provided dict
    """ 
    # Arrange
    person = { "id": 1, "displayName": "John Smith" }

    # Act
    hateos_util.hateosParentPopulator(person, '/person')

    # Assert
    assert person.get('parent') == '/person'