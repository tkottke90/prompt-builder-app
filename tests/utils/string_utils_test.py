from src.utils import string_util

class TestCaseInsensitiveMatch():
  """
  Tests the #caseInsensitiveMatch() function
  """

  def test_should_return_true_when_match(self):
    """
    Tests that the function returns 'true' when the strings (transformed to lower case) are the same
    """
    
    # Arrange
    firstStr = "test"
    secondStr = "Test" # Match should be insensitive so we can assert that by intentionally making the case different

    # Act
    result = string_util.caseInsensitiveMatch(firstStr, secondStr)

    # Assert
    assert result == True

  def test_should_return_false_with_mismatch(self):
    """
    Tests that the function returns 'false' when the strings (transformed to lower case) are the same
    """
    
    # Arrange
    firstStr = "test"
    secondStr = "bar" # Match should be insensitive so we can assert that by intentionally making the case different

    # Act
    result = string_util.caseInsensitiveMatch(firstStr, secondStr)

    # Assert
    assert result == False

class TestUrlQueryDecode():
  """
  Tests the #urlQueryDecode() function
  """

  pass # Intentionally skipped because this method abstracts a method call but does no owned units of work

class TestChecksum():
  """
  Tests the #urlQueryDecode() function
  """

  pass # Intentionally skipped because this method abstracts a method call but does no owned units of work