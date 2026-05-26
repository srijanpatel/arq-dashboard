from fastapi import APIRouter

from arq_dashboard import schemas
from arq_dashboard.core.settings import settings

router = APIRouter()


@router.get("/", response_model=list[schemas.Queue])
async def get_queues() -> list[schemas.Queue]:
    return [schemas.Queue(name=name) for name in settings.arq_queues]
