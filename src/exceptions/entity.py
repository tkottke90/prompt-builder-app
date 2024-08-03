from src.exceptions.base import BaseCustomException, JSONResponse, Request, logException

class EntityException(BaseCustomException):
  """
  Custom exception class for API input errors.
  """
  def __init__(self, message: str, status_code: int = 500):
    super().__init__(message)
    self.status_code = status_code

class EntityNotFoundError(EntityException):
  def __init__(self, id: str | int):
    super().__init__(f"entity not found with id: {id}", 404)
    self.entityId = id

  def getDetails(self) -> dict:
    return { "entityId": self.entityId }

class EntityAlreadyExistsError(EntityException):
  def __init__(self, id: str | int):
    super().__init__(f"entity already exists [id: {id}]", 400)

class EntityHasNoChangesError(EntityException):
  def __init__(
      self,
      *, 
      entityName: str,
      entityId: str | int,
      message: str = "no changes detected for entity"
  ):
    super().__init__(message, 400)
    self.entity = entityName
    self.entityId = entityId

def handleEntityException(
  req: Request,
  exception: EntityException
):
  logException(exception, { "request_id": req.headers.get('request_id', 'missing') })

  return JSONResponse(
    status_code=exception.status_code,
    content={
      "error": exception.__class__.__name__,
      "message": exception.message
    }
  )