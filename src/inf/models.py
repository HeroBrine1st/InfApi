from tortoise.fields import *
from tortoise.models import Model

class Variant(Model):
    id = IntField(pk=True)
    name = CharField(64)
    tasks: ReverseRelation["Task"]

class Task(Model):
    id = IntField(pk=True)
    number = IntField()
    content = TextField()
    variant: ForeignKeyRelation["Variant"] = ForeignKeyField("inf.Variant", "tasks")
    subtheme: ForeignKeyRelation["Subtheme"] = ForeignKeyField("inf.Subtheme", "tasks")

class Theme(Model):
    id = IntField(pk=True)
    name = TextField()
    subthemes: ReverseRelation["Subtheme"]

class Subtheme(Model):
    id = IntField(pk=True)
    name = TextField()
    cheat = TextField()  # image_url
    theme: ForeignKeyRelation["Theme"] = ForeignKeyField("inf.Theme", "subthemes")
    tasks: ReverseRelation["Task"]