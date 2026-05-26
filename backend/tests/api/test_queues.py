import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_queues(client: AsyncClient):
    res = await client.get("/api/queues/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
