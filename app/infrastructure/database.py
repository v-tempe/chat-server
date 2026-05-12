import os
from tortoise import Tortoise


TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": os.getenv("DB_HOST", "localhost"),
                "port": int(os.getenv("DB_PORT", 5432)),
                "user": os.getenv("POSTGRES_USER", "chat_user"),
                "password": os.getenv("POSTGRES_PASSWORD", "chat_secure_password_123"),
                "database": os.getenv("POSTGRES_DB", "chat_db"),
            }
        }
    },
    "apps": {
        "models": {
            "models": ["app.infrastructure.models"],
            "default_connection": "default",
            "migrations": "app.infrastructure.migrations",
        }
    },
    "use_tz": False,
    "timezone": "UTC"
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)


async def close_db():
    await Tortoise.close_connections()


def get_tortoise_config():
    return TORTOISE_ORM
