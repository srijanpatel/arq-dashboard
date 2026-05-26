import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_stats(client: AsyncClient):
    res = await client.get("/api/stats/")
    assert res.status_code == 200
    assert isinstance(res.json(), dict)
