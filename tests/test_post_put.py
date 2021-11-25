import pytest

from httpx import AsyncClient
from fixtures import client_authorized, database_with_test_data, empty_database
from inf.datamodels import *

@pytest.mark.asyncio
@pytest.mark.usefixtures(client_authorized.__name__)
@pytest.mark.usefixtures(empty_database.__name__)
async def test_create(client_authorized: AsyncClient):
    # Variant 1
    response_post_variant1 = await client_authorized.post("/variants/",
                                                          content=VariantPostModel(name="TestVariant1").json())
    assert response_post_variant1.status_code == 201
    response_variants = await client_authorized.get("/variants/")
    assert response_variants.status_code == 200
    assert len(response_variants.json()) == 1
    assert response_variants.json()[0]["id"] == response_post_variant1.json()["id"]
    assert response_variants.json()[0]["name"] == "TestVariant1"
    variant_id1 = response_post_variant1.json()["id"]

    # Theme 1
    response_post_theme1 = await client_authorized.post("/themes/", content=ThemePostModel(name="TestTheme1").json())
    assert response_post_theme1.status_code == 201
    response_themes = await client_authorized.get("/themes/")
    assert response_themes.status_code == 200
    assert len(response_themes.json()) == 1
    assert response_themes.json()[0]["id"] == response_post_theme1.json()["id"]
    assert response_themes.json()[0]["name"] == "TestTheme1"
    theme_id1 = response_post_theme1.json()["id"]

    # Subtheme 1
    response_post_subtheme1 = await client_authorized.post("/themes/%s/subthemes/" % theme_id1,
                                                           content=SubthemePostModel(name="TestSubtheme1",
                                                                                     cheat="TestCheat").json())
    assert response_post_subtheme1.status_code == 201
    response_subthemes = await client_authorized.get("/themes/%s/subthemes/" % theme_id1)
    assert response_subthemes.status_code == 200
    assert len(response_subthemes.json()) == 1
    assert response_subthemes.json()[0]["id"] == response_post_subtheme1.json()["id"]
    assert response_subthemes.json()[0]["name"] == "TestSubtheme1"
    subtheme_id1 = response_post_subtheme1.json()["id"]

    # Task
    response_post_task = await client_authorized.post("/variants/%s/tasks/" % variant_id1,
                                                      content=TaskPostModel(number=0, content="Test content",
                                                                            solution="Test solution",
                                                                            subtheme_id=subtheme_id1).json())
    assert response_post_task.status_code == 201
    response_tasks = await client_authorized.get("/variants/%s/tasks/" % variant_id1)
    assert response_tasks.status_code == 200
    assert len(response_tasks.json()) == 1
    assert response_tasks.json()[0]["id"] == response_post_task.json()["id"]
    assert response_tasks.json()[0]["content"] == "Test content"
    assert response_tasks.json()[0]["solution"] == "Test solution"

@pytest.mark.asyncio
@pytest.mark.usefixtures(client_authorized.__name__)
@pytest.mark.usefixtures(database_with_test_data.__name__)
async def test_put(client_authorized: AsyncClient, database_with_test_data: list):
    theme_ids = database_with_test_data[:2]
    subtheme_ids = database_with_test_data[2:6]
    variant_ids = database_with_test_data[6:8]
    task_ids = database_with_test_data[8:]

    response = await client_authorized.put("/variants/%s/tasks/%s/" % (variant_ids[0], task_ids[0]),
                                           json=TaskPutModel(number=5, content="Test content", solution="Test solution",
                                                             subtheme_id=subtheme_ids[1],
                                                             variant_id=variant_ids[1]).dict())
    assert response.status_code == 200
    response_get_subtheme_tasks = await client_authorized.get(
        "/themes/%s/subthemes/%s/tasks/" % (theme_ids[0], subtheme_ids[0]))
    assert response_get_subtheme_tasks.status_code == 200
    assert len(response_get_subtheme_tasks.json()) == 3
    response_get_subtheme_tasks2 = await client_authorized.get(
        "/themes/%s/subthemes/%s/tasks/" % (theme_ids[0], subtheme_ids[1]))
    assert response_get_subtheme_tasks2.status_code == 200
    assert len(response_get_subtheme_tasks2.json()) == 5

    response_get_variant_tasks = await client_authorized.get("/variants/%s/tasks/" % variant_ids[0])
    assert response_get_variant_tasks.status_code == 200
    assert len(response_get_variant_tasks.json()) == 7
    response_get_variant_tasks2 = await client_authorized.get("/variants/%s/tasks/" % variant_ids[1])
    assert response_get_variant_tasks2.status_code == 200
    assert len(response_get_variant_tasks2.json()) == 9

    response_put_theme = await client_authorized.put("/themes/%s/" % theme_ids[0],
                                                     json=ThemePutModel(name="New name").dict())
    assert response_put_theme.status_code == 200
    assert response_put_theme.json()["id"] == theme_ids[0]
    response_get_theme = await client_authorized.get("/themes/%s/" % theme_ids[0])
    assert response_get_theme.status_code == 200
    assert response_get_theme.json()["id"] == theme_ids[0]
    assert response_get_theme.json()["name"] == "New name"

    response_put_subtheme = await client_authorized.put("/themes/%s/subthemes/%s/" % (theme_ids[0], subtheme_ids[0]),
                                                        json=SubthemePutModel(name="New name", cheat="New cheat",
                                                                              theme_id=theme_ids[1]).dict())
    assert response_put_subtheme.status_code == 200
    assert response_put_subtheme.json()["id"] == subtheme_ids[0]
    response_get_subtheme = await client_authorized.get("/themes/%s/subthemes/%s/" % (theme_ids[1], subtheme_ids[0]))
    assert response_get_subtheme.status_code == 200
    subtheme = response_get_subtheme.json()
    assert subtheme["id"] == subtheme_ids[0]
    assert subtheme["name"] == "New name"
    assert subtheme["cheat"] == "New cheat"

    response_get_theme_subthemes = await client_authorized.get("/themes/%s/subthemes/" % theme_ids[0])
    assert response_get_theme_subthemes.status_code == 200
    assert len(response_get_theme_subthemes.json()) == 1
    response_get_theme_subthemes2 = await client_authorized.get("/themes/%s/subthemes/" % theme_ids[1])
    assert response_get_theme_subthemes2.status_code == 200
    assert len(response_get_theme_subthemes2.json()) == 3

    response_put_variant = await client_authorized.put("/variants/%s/" % variant_ids[0], json=VariantPutModel(name="New name").dict())
    assert response_put_variant.status_code == 200
    response_get_variant = await client_authorized.get("/variants/%s/" % variant_ids[0])
    assert response_get_variant.status_code == 200
    assert response_get_variant.json()["name"] == "New name"


