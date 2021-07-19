import os
import dotenv
dotenv.load_dotenv()

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": os.getenv("MYSQL_HOST"),
                "port": int(os.getenv("MYSQL_PORT")),
                "user": os.getenv("MYSQL_USER"),
                "password": os.getenv("MYSQL_PASSWORD"),
                "database": os.getenv("MYSQL_DATABASE")
            }
        }
    },
    "apps": {
        "inf": {
            "models": ["aerich.models", "inf.models"],
            "default_connection": "default",
        }
    }
}
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
COOKIE_BASE = os.getenv("COOKIE_BASE")
ENABLE_POST_METHODS = os.getenv("ENABLE_POST_METHODS")
ROOT_URL=os.getenv("ROOT_URL")
