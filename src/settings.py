import os

TORTOISE_ORM = {
    "connections": {
        "default": os.environ.get("DATABASE_URL")
    },
    "apps": {
        "main": {
            "models": ["aerich.models", "models"],
            "default_connection": "default",
        }
    }
}