import pytest

from httpx import AsyncClient
from fixtures import client_authorized, database_with_test_data

@pytest.mark.asyncio
@pytest.mark.usefixtures(client_authorized.__name__)
@pytest.mark.usefixtures(database_with_test_data.__name__)
async def test_delete_theme(client_authorized: AsyncClient, database_with_test_data: list):
    theme_ids = database_with_test_data[:2]
    subtheme_ids = database_with_test_data[2:6]
    variant_ids = database_with_test_data[6:8]
    task_ids = database_with_test_data[8:]

    response_delete_theme = await client_authorized.delete("/themes/%s/" % theme_ids[0])
    assert response_delete_theme.status_code == 204
    response_get_variant_1 = await client_authorized.get("/variants/%s/" % variant_ids[0])
    assert response_get_variant_1.status_code == 200
    assert len(response_get_variant_1.json()["tasks"]) == 4

    response_get_variant_2 = await client_authorized.get("/variants/%s/" % variant_ids[1])
    assert response_get_variant_2.status_code == 200
    assert len(response_get_variant_2.json()["tasks"]) == 4

@pytest.mark.asyncio
@pytest.mark.usefixtures(client_authorized.__name__)
@pytest.mark.usefixtures(database_with_test_data.__name__)
async def test_delete_subtheme(client_authorized: AsyncClient, database_with_test_data: list):
    theme_ids = database_with_test_data[:2]
    subtheme_ids = database_with_test_data[2:6]
    variant_ids = database_with_test_data[6:8]
    task_ids = database_with_test_data[8:]

    response_delete_subtheme = await client_authorized.delete("/themes/%s/subthemes/%s/" % (theme_ids[0], subtheme_ids[0]))
    assert response_delete_subtheme.status_code == 204

    response_get_variant_1 = await client_authorized.get("/variants/%s/" % variant_ids[0])
    assert response_get_variant_1.status_code == 200
    assert len(response_get_variant_1.json()["tasks"]) == 4

    response_get_variant_2 = await client_authorized.get("/variants/%s/" % variant_ids[1])
    assert response_get_variant_2.status_code == 200
    assert len(response_get_variant_2.json()["tasks"]) == 8

    response_get_theme_subthemes = await client_authorized.get("/themes/%s/subthemes/" % theme_ids[0])
    assert response_get_theme_subthemes.status_code == 200
    assert len(response_get_theme_subthemes.json()) == 1

@pytest.mark.asyncio
@pytest.mark.usefixtures(client_authorized.__name__)
@pytest.mark.usefixtures(database_with_test_data.__name__)
async def test_delete_variant(client_authorized: AsyncClient, database_with_test_data: list):
    theme_ids = database_with_test_data[:2]
    subtheme_ids = database_with_test_data[2:6]
    variant_ids = database_with_test_data[6:8]
    task_ids = database_with_test_data[8:]

    response_delete_variant = await client_authorized.delete("/variants/%s/" % variant_ids[0])
    assert response_delete_variant.status_code == 204

    response_get_subtheme1_tasks = await client_authorized.get("/themes/%s/subthemes/%s/tasks/" % (theme_ids[0], subtheme_ids[0]))
    assert response_get_subtheme1_tasks.status_code == 200
    assert len(response_get_subtheme1_tasks.json()) == 0

    response_get_subtheme2_tasks = await client_authorized.get("/themes/%s/subthemes/%s/tasks/" % (theme_ids[1], subtheme_ids[2]))
    assert response_get_subtheme2_tasks.status_code == 200
    assert len(response_get_subtheme2_tasks.json()) == 0

@pytest.mark.asyncio
@pytest.mark.usefixtures(client_authorized.__name__)
@pytest.mark.usefixtures(database_with_test_data.__name__)
async def test_delete_task(client_authorized: AsyncClient, database_with_test_data: list):
    theme_ids = database_with_test_data[:2]
    subtheme_ids = database_with_test_data[2:6]
    variant_ids = database_with_test_data[6:8]
    task_ids = database_with_test_data[8:]

    response_delete_task = await client_authorized.delete("/variants/%s/tasks/%s/" % (variant_ids[0], task_ids[0]))
    assert response_delete_task.status_code == 204

    response_get_variant_tasks = await client_authorized.get("/variants/%s/tasks/" % variant_ids[0])
    assert response_get_variant_tasks.status_code == 200
    assert len(response_get_variant_tasks.json()) == 7

    response_get_subtheme_tasks = await client_authorized.get("/themes/%s/subthemes/%s/tasks/" % (theme_ids[0], subtheme_ids[0]))
    assert response_get_subtheme_tasks.status_code == 200
    assert len(response_get_subtheme_tasks.json()) == 3

