from typing import List
from fastapi import FastAPI
from tortoise import Tortoise
from inf.datamodels import VariantModel
from inf.models import Variant

app = FastAPI()

@app.on_event("startup")
async def startup():
    import settings
    await Tortoise.init(config=settings.TORTOISE_ORM)

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()

@app.get("/variants", response_model=List[VariantModel])
async def get_variants():
    return [await VariantModel.of(variant) async for variant in Variant.all()]
