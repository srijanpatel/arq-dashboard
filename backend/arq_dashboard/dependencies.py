from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from arq import ArqRedis, create_pool
from arq.connections import RedisSettings
from arq.constants import default_queue_name
from fastapi import Header


@asynccontextmanager
async def get_redis(redis_settings: RedisSettings) -> AsyncGenerator[ArqRedis, None]:
    redis: ArqRedis | None = None
    try:
        redis = await create_pool(settings_=redis_settings)
        yield redis
    finally:
        if redis is not None:
            await redis.close()


def get_queue_name(
    arq_queue_name: str | None = Header(
        default=None, description="ARQ queue name"
    ),
) -> str:
    return arq_queue_name or default_queue_name
