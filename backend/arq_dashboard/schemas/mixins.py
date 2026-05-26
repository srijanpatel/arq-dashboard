from datetime import UTC, datetime

from pydantic import Field

from .api_model import APIModel


def get_cached_at() -> datetime:
    return datetime.now(UTC)


class CachedAtMixin(APIModel):
    cached_at: datetime = Field(default_factory=get_cached_at)


class PaginationMixin(APIModel):
    total: int
    page_size: int
    current_page: int
