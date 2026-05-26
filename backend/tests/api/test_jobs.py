import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_jobs(client: AsyncClient):
    res = await client.get("/api/jobs/")
    assert res.status_code == 200
    assert isinstance(res.json(), dict)
