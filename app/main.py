from fastapi import FastAPI
from database import init_db

from routes import numbers_routes
from routes import words_routes

app = FastAPI(
    title="Randoom",
    summary="Human Random Generator as a service",
    openapi_tags=[
        { "name": "numbers", "description": "Operations with numbers"},
        { "name": "words", "description": "Operations with words"},
    ]
)

init_db()

app.include_router(numbers_routes)
app.include_router(words_routes)