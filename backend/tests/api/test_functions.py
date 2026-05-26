import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_functions(client: AsyncClient):
    res = await client.get("/api/functions/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
