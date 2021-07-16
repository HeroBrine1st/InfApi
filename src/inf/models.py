from tortoise.fields import *
from tortoise.models import Model

class Variant(Model):
    id = IntField(pk=True)
    name = CharField(64)
    tasks: ForeignKeyRelation["Task"]

class Task(Model):
    id = IntField(pk=True)
    variant = ForeignKeyField("inf.Variant", "tasks")
    number = IntField()
    content = TextField()
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