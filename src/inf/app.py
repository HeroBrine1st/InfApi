import os
from typing import List
from fastapi import FastAPI, HTTPException
from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist

from inf.datamodels import VariantModel, VariantReducedModel
from inf.models import Variant

app = FastAPI(title="Inf API", root_path=os.environ.get("ROOT_PATH") or "")

@app.on_event("startup")
async def startup():
    import settings
    await Tortoise.init(config=settings.TORTOISE_ORM)

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()

@app.get("/variants", response_model=List[VariantReducedModel])
async def get_variants():
    return [await VariantModel.of(variant) async for variant in Variant.all()]

@app.get("/variants/{variant_id}", response_model=VariantModel)
async def get_variants(variant_id: int):
    try:
        variant = await Variant.get(id=variant_id)
    except DoesNotExist:
        raise HTTPException(status_code=404)
    return await VariantModel.of(variant)