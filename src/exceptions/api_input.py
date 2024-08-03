from src.exceptions.base import BaseCustomException, JSONResponse, Request, logException

class ApiInputError(BaseCustomException):
  """
  Custom exception class for API input errors.  These will return a 400 to the caller
  """

  def __init__(
    self,
    message: str
  ):
      super().__init__(message)
      self.message = message
      self.status_code = 400

  def getDetails():
     return 'base api input error, no additional details'

class MissingInputError(ApiInputError):
  """
  Input exception when values are missing
  """

  def __init__(
    self,
    expected: list[str],
    missing: list[str]
  ):
    self.name = "MissingInputError"
    self.expected = expected
    self.missing = missing
    super().__init__(f"missing expected inputs")

  def getDetails(self):
     return {
        "expected": self.expected,
        "missing": self.missing
     }
    

def handleAPIInputException(
  req: Request,
  exception: ApiInputError
):
  logException(req, exception)

  return JSONResponse(
    status_code=exception.status_code,
    content={
       "error": exception.__class__.__name__,
       "message": exception.message,
       "details": exception.getDetails()
    }
  )
   
   