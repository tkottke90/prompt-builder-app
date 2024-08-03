import logging
from typing import Mapping
from fastapi import Request
from fastapi.responses import JSONResponse

ExceptionLogger = logging.getLogger('CustomExceptions')

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
  
def logException(exception: BaseCustomException, extra: Mapping[str, object] | None = None, **kwargs):
  if (extra is None):
    extra = exception.getDetails()
  else:
    extra = { **extra, **exception.getDetails() }

  extra['errorName'] = str(exception.__class__.__name__),
  
  ExceptionLogger.exception(exception, extra=extra, **kwargs)