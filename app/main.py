from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.presentation.routers.auth import router as auth_router
from app.presentation.routers.chat import router as chat_router
from app.infrastructure.database import TORTOISE_ORM

app = FastAPI(
    title="Chat Server",
    description="Серверная часть веб-приложения «Чат» на основе Clean Architecture",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(chat_router)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "Chat API is running"}
