import os

from starlette.requests import Request

import settings

from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import Response
from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist
from inf.auth import CookieAuth
from inf.datamodels import *
from inf.models import *
from typing import List

COOKIE_NAME = "SESSION"

app = FastAPI(title="Inf API", root_path=settings.ROOT_URL)
cookie = CookieAuth(name=COOKIE_NAME)

# region Initialization and shutdown
@app.on_event("startup")
async def startup():  # pragma: nocoverage
    await Tortoise.init(config=settings.TORTOISE_ORM)

@app.on_event("shutdown")
async def shutdown():  # pragma: nocoverage
    await Tortoise.close_connections()

# endregion
# region GET Methods
@app.get("/variants/", response_model=List[VariantReducedModel])
async def get_variants():
    return [await VariantReducedModel.of(variant) async for variant in Variant.all()]

@app.get("/variants/{variant_id}/", response_model=VariantModel)
async def get_variant(variant_id: int):
    try:
        variant = await Variant.get(id=variant_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404)
    return await VariantModel.of(variant)

@app.get("/variants/{variant_id}/tasks/", response_model=List[TaskModel])
async def get_tasks(variant_id: int):
    try:
        variant = await Variant.get(id=variant_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404)
    return [await TaskModel.of(task) async for task in variant.tasks.all()]

@app.get("/variants/{variant_id}/tasks/{task_id}/", response_model=TaskModel)
async def get_task(variant_id: int, task_id: int):
    try:
        variant = await Variant.get(id=variant_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404)
    return await TaskModel.of(await variant.tasks.all().get(id=task_id))

@app.get("/themes/", response_model=List[ThemeReducedModel])
async def get_themes():
    return [await ThemeReducedModel.of(theme) async for theme in Theme.all()]

@app.get("/themes/{theme_id}/", response_model=ThemeReducedModel)
async def get_theme(theme_id: int):
    try:
        theme = await Theme.get(id=theme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404)
    return await ThemeModel.of(theme)

@app.get("/themes/{theme_id}/subthemes/", response_model=List[SubthemeReducedModel])
async def get_subthemes(theme_id: int):
    try:
        theme = await Theme.get(id=theme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404)
    return [await SubthemeReducedModel.of(subtheme) async for subtheme in theme.subthemes.all()]

@app.get("/themes/{theme_id}/subthemes/{subtheme_id}/", response_model=SubthemeModel)
async def get_subtheme(theme_id: int, subtheme_id: int):
    try:
        theme = await Theme.get(id=theme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404)
    try:
        subtheme = await theme.subthemes.all().get(id=subtheme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404)
    return await SubthemeModel.of(subtheme)

@app.get("/themes/{theme_id}/subthemes/{subtheme_id}/tasks/", response_model=List[TaskModel])
async def get_subtheme_tasks(theme_id: int, subtheme_id: int):
    try:
        theme = await Theme.get(id=theme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404)
    try:
        subtheme = await theme.subthemes.all().get(id=subtheme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404)
    return [await TaskModel.of(task) async for task in subtheme.tasks.all()]

# endregion
# region Authentication
@app.post("/login", status_code=204)
async def login(response: Response, credentials: OAuth2PasswordRequestForm = Depends()):
    if not settings.ENABLE_POST_METHODS: # pragma: nocoverage
        return HTTPException(503, "Disabled")
    cookie.validate(credentials)
    response.set_cookie(COOKIE_NAME, cookie.get_cookie(),
                        expires=(datetime.combine(
                            (datetime.now() + timedelta(days=1)).date(),
                            datetime.min.time()
                        ) - datetime.now()).seconds)
    response.status_code = 204
    return response

@app.get("/checkauth", status_code=204, response_class=Response)
async def check_auth(_=Depends(cookie)):
    if not settings.ENABLE_POST_METHODS: # pragma: nocoverage
        return HTTPException(503, "Disabled")
# endregion
# region POST Methods
@app.post("/themes/", status_code=201, response_model=ThemeModel)
async def create_theme(theme: ThemePostModel, _=Depends(cookie)):
    return await ThemeModel.of(await Theme.create(name=theme.name))

@app.post("/themes/{theme_id}/subthemes/", status_code=201, response_model=SubthemeModel)
async def create_subtheme(theme_id: int, subtheme: SubthemePostModel, _=Depends(cookie)):
    try:
        theme = await Theme.get(id=theme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Theme with provided theme_id not found")
    return await SubthemeModel.of(await Subtheme.create(name=subtheme.name, cheat=subtheme.cheat, theme=theme))

@app.post("/variants/", status_code=201, response_model=VariantModel)
async def create_variant(variant: VariantPostModel, _=Depends(cookie)):
    return await VariantModel.of(await Variant.create(name=variant.name))

@app.post("/variants/{variant_id}/tasks/", status_code=201, response_model=TaskModel)
async def create_task(variant_id: int, task: TaskPostModel, _=Depends(cookie)):
    try:
        variant = await Variant.get(id=variant_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Variant with provided variant_id not found")
    try:
        subtheme = await Subtheme.get(id=task.subtheme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Subtheme with provided subtheme_id not found")
    return await TaskModel.of(
        await Task.create(number=task.number, content=task.content, variant=variant, subtheme=subtheme,
                          solution=task.solution))

# endregion
#region PUT Methods
@app.put("/themes/{theme_id}/", status_code=200, response_model=ThemeModel)
async def put_theme(theme_id: int, theme: ThemePutModel, _=Depends(cookie)):
    try:
        theme_db = await Theme.get(id=theme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Theme with provided theme_id not found")
    theme_db.name = theme.name
    await theme_db.save()
    return await ThemeModel.of(theme_db)

@app.put("/themes/{theme_id}/subthemes/{subtheme_id}/", status_code=200, response_model=SubthemeModel)
async def put_subtheme(theme_id, subtheme_id: int, subtheme: SubthemePutModel, _=Depends(cookie)):
    try:
        theme_db = await Theme.get(id=theme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Theme with provided theme_id not found")
    try:
        subtheme_db = await theme_db.subthemes.all().get(id=subtheme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Subtheme with provided subtheme_id not found")
    subtheme_db.name = subtheme.name
    subtheme_db.cheat = subtheme.cheat
    if subtheme.theme_id:
        try:
            new_theme = await Theme.get(id=subtheme.theme_id)
        except DoesNotExist: # pragma: nocoverage
            raise HTTPException(status_code=404, detail="Theme with provided theme_id in body not found")
        subtheme_db.theme = new_theme
    await subtheme_db.save()
    return await SubthemeModel.of(subtheme_db)

@app.put("/variants/{variant_id}/", status_code=200, response_model=VariantModel)
async def put_variant(variant_id: int, variant: VariantPutModel, _=Depends(cookie)):
    try:
        variant_db = await Variant.get(id=variant_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Variant with provided variant_id not found")
    variant_db.name = variant.name
    await variant_db.save()
    return await VariantModel.of(variant_db)

@app.put("/variants/{variant_id}/tasks/{task_id}/", status_code=200, response_model=TaskModel)
async def put_task(variant_id: int, task_id: int, task: TaskPutModel, _=Depends(cookie)):
    try:
        variant_db = await Variant.get(id=variant_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Variant with provided variant_id not found")
    try:
        task_db = await variant_db.tasks.all().get(id=task_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Task with provided task_id not found")
    task_db.content = task.content
    task_db.number = task.number
    task_db.solution = task.solution
    if task.subtheme_id:
        try:
            new_subtheme = await Subtheme.get(id=task.subtheme_id)
        except DoesNotExist: # pragma: nocoverage
            raise HTTPException(status_code=404, detail="Subtheme with provided subtheme_id in body not found")
        task_db.subtheme = new_subtheme
    if task.variant_id:
        try:
            new_variant = await Variant.get(id=task.variant_id)
        except DoesNotExist: # pragma: nocoverage
            raise HTTPException(status_code=404, detail="Variant with provided variant_id in body not found")
        task_db.variant = new_variant
    await task_db.save()
    return await TaskModel.of(task_db)

# endregion
#region DELETE Methods
@app.delete("/themes/{theme_id}/", status_code=204)
async def delete_theme(theme_id: int, _=Depends(cookie)):
    try:
        theme_db = await Theme.get(id=theme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Theme with provided theme_id not found")
    await theme_db.delete()
    return

@app.delete("/themes/{theme_id}/subthemes/{subtheme_id}/", status_code=204)
async def delete_subtheme(theme_id, subtheme_id: int, _=Depends(cookie)):
    try:
        theme_db = await Theme.get(id=theme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Theme with provided theme_id not found")
    try:
        subtheme_db = await theme_db.subthemes.all().get(id=subtheme_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Subtheme with provided subtheme_id not found")
    await subtheme_db.delete()
    return

@app.delete("/variants/{variant_id}/", status_code=204)
async def delete_variant(variant_id: int, _=Depends(cookie)):
    try:
        variant_db = await Variant.get(id=variant_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Variant with provided variant_id not found")
    await variant_db.delete()
    return

@app.delete("/variants/{variant_id}/tasks/{task_id}/", status_code=204)
async def delete_task(variant_id: int, task_id: int, _=Depends(cookie)):
    try:
        variant_db = await Variant.get(id=variant_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Variant with provided variant_id not found")
    try:
        task_db = await variant_db.tasks.all().get(id=task_id)
    except DoesNotExist: # pragma: nocoverage
        raise HTTPException(status_code=404, detail="Task with provided task_id not found")
    await task_db.delete()
    return
#endregion
