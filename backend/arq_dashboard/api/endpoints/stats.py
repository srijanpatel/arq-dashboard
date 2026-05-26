from fastapi import APIRouter, Depends

from arq_dashboard import schemas
from arq_dashboard.cache import async_ttl_cache
from arq_dashboard.core.settings import settings
from arq_dashboard.dependencies import get_queue_name
from arq_dashboard.queue import Queue

router = APIRouter()


@async_ttl_cache(ttl=settings.cache_ttl, maxsize=1)
async def _get_stats(queue_name: str) -> schemas.QueueStats:
    queue = Queue.from_name(queue_name)
    return await queue.get_stats()


@router.get("/", response_model=schemas.QueueStats)
async def get_stats(
    queue_name: str = Depends(get_queue_name),
) -> schemas.QueueStats:
    return await _get_stats(queue_name)
