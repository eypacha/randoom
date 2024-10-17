from fastapi import FastAPI
from database import init_db

from routes import numbers_routes
from routes import words_routes

app = FastAPI(
    title="Randoom",
    description="Human Random Generator as a service"
)

init_db()

app.include_router(numbers_routes, prefix="/random/number", tags=["numbers"])
app.include_router(words_routes, prefix="/random/word", tags=["words"])