
import pytest
from httpx import AsyncClient

from inf.datamodels import *
from fixtures import client, database_with_test_data

@pytest.mark.asyncio
@pytest.mark.usefixtures(client.__name__)
@pytest.mark.usefixtures(database_with_test_data.__name__)
async def test_get_variants(client: AsyncClient):
    response_variants = await client.get("/variants/")
    assert response_variants.status_code == 200
    assert len(response_variants.json()) == 2
    for variant in response_variants.json():
        response_variant = await client.get("/variants/%s" % variant["id"])
        assert response_variant.status_code == 200
        model = VariantModel.parse_obj(response_variant.json())
        assert len(model.tasks) == 8
