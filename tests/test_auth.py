import pytest
from httpx import AsyncClient

from fixtures import client

@pytest.mark.asyncio
@pytest.mark.usefixtures(client.__name__)
async def test_auth(client: AsyncClient):

    response = await client.post("/variants/", content="") # Похер какой там контент, тест должен сфейлить
    assert response.status_code == 403
    response = await client.get("/checkauth")
    assert response.status_code == 403
    client.cookies.set("SESSION", "invalid", "test.local")
    response = await client.post("/variants/", content="")  # Похер какой там контент, тест должен сфейлить
    assert response.status_code == 401
    response = await client.get("/checkauth")
    assert response.status_code == 401
    response = await client.post("/login", content="username=invalid&password=invalid",
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401