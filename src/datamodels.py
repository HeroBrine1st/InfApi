from typing import List

from pydantic import BaseModel


#region GET response models
class VariantReduced(BaseModel):
    id: int
    name: str

class Variant(VariantReduced):
    tasks: List["Task"]

class Task(BaseModel):
    id: int
    variant: VariantReduced
    number: int
    content: str
    subtheme: "SubthemeReduced"

class SubthemeReduced(BaseModel):
    id: int
    name: str
    theme_id: int

class Subtheme(SubthemeReduced):
    cheat: str # image url
    tasks: List["Task"]

class ThemeReduced(BaseModel):
    id: int
    name: str
    subthemes: List[Subtheme]
#endregion