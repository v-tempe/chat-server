#!/bin/sh

export PYTHONPATH=/
export TORTOISE_ORM="app.infrastructure.database.TORTOISE_ORM"
tortoise init
tortoise makemigrations
tortoise migrate

uvicorn app.main:app --host 0.0.0.0 --port 8000
