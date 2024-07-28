from fastapi import APIRouter, Cookie, Response
from typing import Annotated
from datetime import datetime

router = APIRouter(
  tags=["Application"]
)

@router.get('/healthcheck', name="Healthcheck Endpoint", description="Utility endpoint to check if the API is healthy")
def healthcheck_endpoint() -> str:
  
  return "OKAY"


@router.get('/teapot', status_code=418, name="Teapot Endpoint", description="Endpoint for returning the 418 - Teapot error status")
def healthcheck_endpoint(response: Response, teapotAchievementCookie: Annotated[str | None, Cookie(include_in_schema=False)] = None) -> str:
  if (isinstance(teapotAchievementCookie, str)):
    return "You found nothing looking for the teapot"


  response.set_cookie(key="teapotAchievementCookie", value='Achievement Unlocked on {:%Y-%m-%d %H:%M:%S}'.format(datetime.now()))
  return "Achievement Get: Find the Teapot"