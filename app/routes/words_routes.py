from fastapi import APIRouter, Depends, Query
from models.random_words import RandomWords
from database import get_db_connection
from sqlite3 import Connection

router = APIRouter()

words_handler = RandomWords()

@router.post("/")
def post_random_word(word: str, lang: str, conn: Connection = Depends(get_db_connection)):
    if len(lang) != 2:
        raise HTTPException(status_code=400, detail="Language code must be 2 letters long.")
    words_handler.insert(conn, word, lang)
    return {"message": "Word saved successfully!", "word": word}

@router.get("/")
def get_random_word(lang: str = Query(None), conn: Connection = Depends(get_db_connection)):
    return {"random_word": words_handler.get_random(conn, lang)}

@router.get("/stats/")
def get_word_stats(conn: Connection = Depends(get_db_connection)):
    stats, top_items = words_handler.get_stats(conn)
    top_words_list = [{"value": row[0], "count": row[1]} for row in top_items]
    return {
        "total_words": stats[0],
        "top_words": top_words_list
    }

__all__ = ['router']
