from dataclasses import dataclass

from arq.constants import default_queue_name

from arq_dashboard.cache import async_ttl_cache
from arq_dashboard.core.settings import settings
from arq_dashboard.queue import Queue


@dataclass
class Metadata:
    functions: set[str]


@async_ttl_cache(ttl=settings.cache_ttl, maxsize=settings.cache_max_size)
async def get_metadata(queue_name: str = default_queue_name) -> Metadata:
    queue = Queue.from_name(queue_name)
    jobs = await queue.get_jobs()
    functions: set[str] = {job.function for job in jobs}
    return Metadata(functions=functions)
