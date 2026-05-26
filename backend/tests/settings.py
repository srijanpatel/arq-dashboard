import os

from arq.connections import RedisSettings

REDIS_HOST: str = os.getenv("TESTING_REDIS_HOST", "localhost")
REDIS_PORT: int = int(os.getenv("TESTING_REDIS_PORT", "6379"))
REDIS_PASSWORD: str | None = os.getenv("TESTING_REDIS_PASSWORD")

REDIS_SETTINGS = RedisSettings(
    host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD
)
