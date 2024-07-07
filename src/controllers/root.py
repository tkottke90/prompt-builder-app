from fastapi import APIRouter

router = APIRouter()

@router.get('/healthcheck')
def healthcheck_endpoint() -> str:
  return "OKAY"