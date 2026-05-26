import time
from collections import OrderedDict
from functools import wraps
from typing import Any


def async_ttl_cache(ttl: int = 60, maxsize: int = 32):
    """Simple async TTL cache decorator."""

    def decorator(func):
        cache: OrderedDict[Any, tuple[Any, float]] = OrderedDict()

        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()

            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl:
                    cache.move_to_end(key)
                    return result
                del cache[key]

            if len(cache) >= maxsize:
                cache.popitem(last=False)

            result = await func(*args, **kwargs)
            cache[key] = (result, now)
            return result

        wrapper.cache = cache  # type: ignore[attr-defined]
        return wrapper

    return decorator
