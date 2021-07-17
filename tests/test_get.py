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

@pytest.mark.asyncio
@pytest.mark.usefixtures(client.__name__)
@pytest.mark.usefixtures(database_with_test_data.__name__)
async def test_get_themes(client: AsyncClient):
    response_themes = await client.get("/themes/")
    assert response_themes.status_code == 200
    themes = response_themes.json()
    assert len(themes) == 2
    for theme in themes:
        response_theme = await client.get("/themes/%s/" % theme["id"])
        assert response_theme.status_code == 200
        response_subthemes = await client.get("/themes/%s/subthemes/" % theme["id"])
        assert response_subthemes.status_code == 200
        subthemes = response_subthemes.json()
        assert len(subthemes) == 2
        for subtheme in subthemes:
            response_subtheme = await client.get("/themes/%s/subthemes/%s/" % (theme["id"], subtheme["id"]))
            assert response_subtheme.status_code == 200
            assert response_subtheme.json()["id"] == subtheme["id"]
            response_tasks = await client.get("/themes/%s/subthemes/%s/tasks" % (theme["id"], subtheme["id"]))
            assert response_tasks.status_code == 200
            assert len(response_tasks.json()) == 4

@pytest.mark.asyncio
@pytest.mark.usefixtures(client.__name__)
@pytest.mark.usefixtures(database_with_test_data.__name__)
async def test_get_task(client: AsyncClient, database_with_test_data: list):
    task_id = database_with_test_data[8]
    variant_id = database_with_test_data[6]
    response = await client.get("/variants/%s/tasks/%s/" % (variant_id, task_id))
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["variant"]["id"] == variant_id