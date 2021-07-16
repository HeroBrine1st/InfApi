
import pytest
from httpx import AsyncClient

from inf.datamodels import *
from test_initialization import client, database

@pytest.mark.asyncio
@pytest.mark.usefixtures(client.__name__)
@pytest.mark.usefixtures(database.__name__)
async def test_get_variants(client: AsyncClient):
    response = await client.get("/variants/")
    assert response.status_code == 200
    models = [VariantModel.parse_obj(entry) for entry in response.json()]

    assert len(models) == 2
