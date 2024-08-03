from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable

class ApiInputError(Exception):
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
  _: Request,
  exception: ApiInputError
):
  return JSONResponse(
    status_code=exception.status_code,
    content={
       "message": exception.message,
       "details": exception.getDetails()
    }
  )
   
   