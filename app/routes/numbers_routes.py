from fastapi import APIRouter, Depends, Query
from models.random_numbers import RandomNumbers
from database import get_db_connection
from sqlite3 import Connection
from pydantic import BaseModel

router = APIRouter(
    prefix="/random/number",
    tags=["numbers"],
)

class PostResponse(BaseModel):
    message: str
    number: int
    
class GetResponse(BaseModel):
    number: int

class StatsResponse(BaseModel):
    total_numbers: int
    min_value: int
    max_value: int
    avg_value: float
    top_numbers: list[dict]
    
numbers_handler = RandomNumbers()

@router.post("/", response_model=PostResponse, summary="Save a random number", description="Insert a random number into the database.")
def post_random_number(
    number: int = Query(..., description="The random number to be saved"),
    conn: Connection = Depends(get_db_connection)):
    numbers_handler.insert(conn, number)
    return {
        "message": "Number saved successfully!",
        "number": number
    }

@router.get("/", response_model=GetResponse, summary="Get a random number", description="Retrieve a random number from the database, with optional min and max range.")
def get_random_number(
    min_value: int = Query(None, description="Minimum value of the random number range"),
    max_value: int = Query(None, description="Maximum value of the random number range"),
    conn: Connection = Depends(get_db_connection)):
    random_number = numbers_handler.get_random(conn, min_value=min_value, max_value=max_value)
    return {
        "random_number": random_number
    }

@router.get("/stats/", response_model=StatsResponse, summary="Get statistics of numbers", description="Retrieve statistics including total count, min, max, avg, and top items.")
def get_number_stats(conn: Connection = Depends(get_db_connection)):
    stats, top_items = numbers_handler.get_stats(conn)
    top_numbers_list = [{"value": row[0], "count": row[1]} for row in top_items]
    return {
        "total_numbers": stats[0],
        "min_value": stats[1],
        "max_value": stats[2],
        "avg_value": stats[3],
        "top_numbers": top_numbers_list
    }

__all__ = ['router']