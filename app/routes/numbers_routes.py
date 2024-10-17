from fastapi import APIRouter, Depends
from models.random_numbers import RandomNumbers
from database import get_db_connection
from sqlite3 import Connection

router = APIRouter()

numbers_handler = RandomNumbers()

@router.post("/")
def post_random_number(number: int, conn: Connection = Depends(get_db_connection)):
    numbers_handler.insert(conn, number)
    return {"message": "Number saved successfully!", "number": number}

@router.get("/")
def get_random_number(conn: Connection = Depends(get_db_connection)):
    return {"random_number": numbers_handler.get_random(conn)}

@router.get("/stats/")
def get_number_stats(conn: Connection = Depends(get_db_connection)):
    stats, top_items = numbers_handler.get_stats(conn)
    top_numbers_list = [{"value": row[0], "count": row[1]} for row in top_items]
    return {
        "total_numbers": stats[0],
        "top_numbers": top_numbers_list
    }

__all__ = ['router']