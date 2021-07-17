from typing import List, Optional

from pydantic import BaseModel

from inf.models import Subtheme, Task, Theme, Variant

# region GET response models
class VariantReducedModel(BaseModel):
    id: int
    name: str

    @staticmethod
    async def of(variant: Variant):
        await variant.fetch_related()
        return VariantReducedModel(
            id=variant.id,
            name=variant.name
        )

class SubthemeReducedModel(BaseModel):
    id: int
    name: str
    theme_id: int
    task_count: int

    @staticmethod
    async def of(subtheme: Subtheme):
        return SubthemeReducedModel(
            id=subtheme.id,
            name=subtheme.name,
            theme_id=(await subtheme.theme).id,
            task_count=(await subtheme.tasks.all().count())
        )

class ThemeReducedModel(BaseModel):
    id: int
    name: str

    @staticmethod
    async def of(theme: Theme):
        return ThemeReducedModel(
            id=theme.id,
            name=theme.name,
        )

class TaskModel(BaseModel):
    id: int
    variant: VariantReducedModel
    number: int
    content: str
    subtheme: SubthemeReducedModel

    @staticmethod
    async def of(task: Task):
        return TaskModel(
            id=task.id,
            variant=await VariantReducedModel.of(await task.variant),
            number=task.number,
            content=task.content,
            subtheme=await SubthemeReducedModel.of(await task.subtheme)
        )

class VariantModel(VariantReducedModel):
    tasks: List[TaskModel]

    @staticmethod
    async def of(variant: Variant):
        return VariantModel(
            id=variant.id,
            name=variant.name,
            tasks=[await TaskModel.of(task) async for task in variant.tasks.all()]
        )

class SubthemeModel(SubthemeReducedModel):
    cheat: str  # image url
    tasks: List[TaskModel]

    @staticmethod
    async def of(subtheme: Subtheme):
        return SubthemeModel(
            id=subtheme.id,
            name=subtheme.name,
            theme_id=(await subtheme.theme).id,
            cheat=subtheme.cheat,
            tasks=[await TaskModel.of(task) async for task in subtheme.tasks.all()],
            task_count=(await subtheme.tasks.all().count())
        )

class ThemeModel(ThemeReducedModel):
    subthemes: List[SubthemeModel]

    @staticmethod
    async def of(theme: Theme):
        return ThemeModel(
            id=theme.id,
            name=theme.name,
            subthemes=[await SubthemeModel.of(subtheme) async for subtheme in theme.subthemes.all()]
        )

# endregion
# region POST request models
class TaskPostModel(BaseModel):
    # variant id included in URL
    number: int
    content: str
    subtheme_id: int

class VariantPostModel(BaseModel):
    name: str

class SubthemePostModel(BaseModel):
    name: str
    # theme id included in URL
    cheat: Optional[str] = ""  # image url

class ThemePostModel(BaseModel):
    name: str

# endregion
# region PUT request models
class TaskPutModel(TaskPostModel):
    variant_id: Optional[int] = None # Change variant
    subtheme_id: Optional[int] = None # Change subtheme

VariantPutModel = VariantPostModel

class SubthemePutModel(SubthemePostModel):
    theme_id: Optional[int] = None # Change theme

ThemePutModel = ThemePostModel
# endregion
