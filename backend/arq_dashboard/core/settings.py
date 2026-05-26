import sys
from typing import Any
from urllib.parse import urlparse

from arq.connections import RedisSettings
from arq.constants import default_queue_name
from arq.jobs import Deserializer
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ARQ_DASHBOARD_",
        arbitrary_types_allowed=True,
    )

    project_name: str = "arq-dashboard"
    debug: bool = False
    testing: bool = False

    log_file: Any = sys.stderr
    log_level: str = "DEBUG"
    log_backtrace: bool = True

    redis_url: str = "redis://localhost:6379"
    arq_deserializer: Deserializer | None = None

    max_at_once: int | None = 10
    max_per_seconds: int | None = None

    cache_ttl: int = 60
    cache_max_size: int = 32

    @property
    def redis_settings(self) -> RedisSettings:
        parsed = urlparse(self.redis_url)
        return RedisSettings(
            host=parsed.hostname or "localhost",
            port=parsed.port or 6379,
            password=parsed.password,
            database=int(parsed.path.lstrip("/") or 0),
        )

    @property
    def arq_queues(self) -> dict[str, RedisSettings]:
        return {default_queue_name: self.redis_settings}


settings = Settings()
