from src.utils import hateos_util

class TestMetadataPopulator():
  """
  Tests the #caseInsensitiveMatch() function
  """

  def test_string_value(self):
    """
    An attribute should be added with a string value when passed
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
    An attribute should be added with a string value when passed
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

class TestHateosSelfPopulator():
  """
  Tests the #caseInsensitiveMatch() function
  """

  def test_one(self):
    """
    
    """ 
    # Arrange

    # Act

    # Assert
    assert True == True

class TestHateosParentPopulator():
  """
  Tests the #caseInsensitiveMatch() function
  """

  def test_one(self):
    """
    
    """ 
    # Arrange

    # Act

    # Assert
    assert True == True