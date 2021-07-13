from fastapi import FastAPI
from tortoise import Tortoise
import settings

app = FastAPI()

@app.on_event("startup")
async def startup():
    await Tortoise.init(config=settings.TORTOISE_ORM)

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()
