from fastapi import FastAPI


app = FastAPI(
    title="Chat Server",
    description="Серверная часть веб-приложения «Чат» на основе Clean Architecture",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Chat API is running"}
