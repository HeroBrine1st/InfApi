import pytest
import settings

from tortoise import Tortoise
from inf.models import *

@pytest.fixture(scope="function")
@pytest.mark.asyncio
async def empty_database():
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
    yield
    await Tortoise.close_connections()