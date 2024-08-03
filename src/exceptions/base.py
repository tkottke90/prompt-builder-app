
class BaseCustomException(Exception):

  def __init__(self, message: str) -> None:
    super().__init__(message)
    self.message = message
    self.name = self.__class__.__name__

  def getDetails(self) -> dict:
    """
    Helper function to return details about the specific message
    """
    return {}