from typing import List

from fastapi import FastAPI
from tortoise import Tortoise
import settings
from datamodels import SubthemeReducedModel, TaskModel, VariantModel, VariantReducedModel
import models

app = FastAPI()

@app.on_event("startup")
async def startup():
    await Tortoise.init(config=settings.TORTOISE_ORM)

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()

@app.get("variants", response_model=List[VariantModel])
async def get_variants():
    return [
        VariantModel(id=variant.id, name=variant.name, tasks=[
            TaskModel(id=task.id,
                      variant=VariantReducedModel(id=task.variant.id, name=task.variant.name),
                      content=task.content,
                      subtheme=SubthemeReducedModel(id=task.subtheme.id, name=task.subtheme.name,
                                                    theme_id=task.subtheme.theme.id),
                      number=task.number)
            async for task in variant.tasks
        ]) async for variant in models.Variant.all()]
