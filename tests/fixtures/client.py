import pytest

from httpx import AsyncClient
from inf import app

@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
