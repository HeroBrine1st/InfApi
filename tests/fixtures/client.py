import os

import pytest
import urllib.parse

from httpx import AsyncClient
from inf import app

@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def client_authorized():
    async with AsyncClient(app=app, base_url="http://test") as client:
        client: AsyncClient
        body = "username=%s&password=%s" % (urllib.parse.quote(os.getenv("LOGIN")),
                                            urllib.parse.quote(os.getenv("PASSWORD")))
        response = await client.post("/login", content=body,
                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
        if response.status_code != 204:
            from pprint import pprint
            print(body)
            pprint(response.json())
            raise AssertionError("%s != 204" % response.status_code)
        yield client
