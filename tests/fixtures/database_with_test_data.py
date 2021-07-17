import pytest
import settings

from tortoise import Tortoise
from inf.models import *

@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def database_with_test_data():
    # Connect
    await Tortoise.init(config=settings.TORTOISE_ORM)
    # Clear database
    async for theme in Theme.all():
        await theme.delete()
    async for variant in Variant.all():
        await variant.delete()
    async for task in Task.all():
        await task.delete()
    async for subtheme in Subtheme.all():
        await subtheme.delete()
    # Create test entries
    theme1 = await Theme.create(name="Тема 1")
    theme2 = await Theme.create(name="Тема 2")
    subtheme1 = await Subtheme.create(name="Подтема 1", theme=theme1, cheat="Image URL")
    subtheme2 = await Subtheme.create(name="Подтема 2", theme=theme1, cheat="Image URL")
    subtheme3 = await Subtheme.create(name="Подтема 3", theme=theme2, cheat="Image URL")
    subtheme4 = await Subtheme.create(name="Подтема 4", theme=theme2, cheat="Image URL")

    variant1 = await Variant.create(name="Вариант 1")
    variant2 = await Variant.create(name="Вариант 2")

    for i in range(16):
        variant = variant1
        if i % 2 == 1:
            variant = variant2
        subtheme = subtheme1
        if i % 4 == 1:
            subtheme = subtheme2
        if i % 4 == 2:
            subtheme = subtheme3
        if i % 4 == 3:
            subtheme = subtheme4
        await Task.create(number=i // 2 + 1, content="Задание %s" % i, solution="Решение %s" % i, subtheme=subtheme, variant=variant)

    # Close connection
    yield [theme1.id, theme2.id, subtheme1.id, subtheme2.id, subtheme3.id, subtheme4.id, variant1.id, variant2.id] + [task.id async for task in Task.all()]
    await Tortoise.close_connections()