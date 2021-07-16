from typing import List

from pydantic import BaseModel


#region GET response models
class VariantReducedModel(BaseModel):
    id: int
    name: str

class VariantModel(VariantReducedModel):
    tasks: List["TaskModel"]

class TaskModel(BaseModel):
    id: int
    variant: VariantReducedModel
    number: int
    content: str
    subtheme: "SubthemeReducedModel"

class SubthemeReducedModel(BaseModel):
    id: int
    name: str
    theme_id: int

class SubthemeModel(SubthemeReducedModel):
    cheat: str # image url
    tasks: List["TaskModel"]

class ThemeReducedModel(BaseModel):
    id: int
    name: str

class ThemeModel(ThemeReducedModel):
    subthemes: List[SubthemeModel]
#endregion