from tortoise.fields import *
from tortoise.models import Model

class Variant(Model):
    name = CharField(64)
    tasks: ForeignKeyRelation["Task"]

class Task(Model):
    variant = ForeignKeyField("models.Variant", "tasks")
    number = IntField()
    content = TextField()
    subtheme = ForeignKeyField("models.Subtheme", "tasks")

class Theme(Model):
    name = TextField()
    subthemes: ReverseRelation["Subtheme"]

class Subtheme(Model):
    name = TextField()
    cheat = TextField()  # image_url
    theme = ForeignKeyField("models.Theme", "subthemes")
    tasks: ReverseRelation["Task"]