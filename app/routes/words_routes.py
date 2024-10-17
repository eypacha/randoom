from fastapi import APIRouter, Depends, Query, HTTPException
from models.random_words import RandomWords
from database import get_db_connection
from sqlite3 import Connection
from pydantic import BaseModel

router = APIRouter()

class PostResponse(BaseModel):
    message: str
    word: str
    
class GetResponse(BaseModel):
    word: str
    lang: str

class StatsResponse(BaseModel):
    total_words: int
    min_letters_value: int
    max_letters_value: int
    avg_length: float
    top_words: list[dict]


VALID_LANGUAGES = [
    "aa", "ab", "ae", "af", "ak", "am", "an", "ar", "as", "av", "ay", "az",
    "ba", "be", "bg", "bh", "bi", "bm", "bn", "bo", "br", "bs", "ca", "ce",
    "ch", "co", "cr", "cs", "cu", "cv", "cy", "da", "de", "dv", "dz", "ee",
    "el", "en", "eo", "es", "et", "eu", "fa", "ff", "fi", "fj", "fo", "fr",
    "fy", "ga", "gd", "gl", "gn", "gu", "gv", "ha", "he", "hi", "ho", "hr",
    "ht", "hu", "hy", "hz", "ia", "id", "ie", "ig", "ii", "ik", "io", "is",
    "it", "iu", "ja", "jv", "ka", "kg", "ki", "kj", "kk", "kl", "km", "kn",
    "ko", "kr", "ks", "ku", "kv", "kw", "ky", "la", "lb", "lg", "li", "ln",
    "lo", "lt", "lu", "lv", "mg", "mh", "mi", "mk", "ml", "mn", "mr", "ms",
    "mt", "my", "na", "nb", "nd", "ne", "ng", "nl", "nn", "no", "nr", "nv",
    "ny", "oc", "oj", "om", "or", "os", "pa", "pi", "pl", "ps", "pt", "qc",
    "rm", "rn", "ro", "ru", "rw", "sa", "sc", "sd", "se", "sg", "si", "sk",
    "sl", "sm", "sn", "so", "sq", "sr", "ss", "st", "su", "sv", "sw", "ta",
    "te", "tg", "th", "ti", "tk", "tl", "tn", "to", "tr", "ts", "tt", "tw",
    "ty", "ug", "uk", "ur", "uz", "ve", "vi", "vo", "wa", "wo", "xh", "yi",
    "yo", "za", "zh", "zu"
]

def validate_language(lang: str):
    if lang not in VALID_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"The language '{lang}' is not supported.")
    
words_handler = RandomWords()

@router.post("/", response_model=PostResponse, summary="Save a random word", description="Insert a random word into the database.")
def post_random_word(
    word: str = Query(..., description="The word to be saved"),
    lang: str = Query(..., description="The language of the word Filter by language (ISO 639, 2-letter code)"),
    conn: Connection = Depends(get_db_connection)):
    
    if lang:
        validate_language(lang)
        
    words_handler.insert(conn, word, lang)
    return {"message": "Word saved successfully!", "word": word}

@router.get("/", response_model=GetResponse, summary="Get a random word", description="Retrieve a random word from the database with optional language and length filters.")
def get_random_word(
    lang: str = Query(None, description="Filter by language (ISO 639, 2-letter code)"),
    min_length: int = Query(None, description="Minimum word length"),
    max_length: int = Query(None, description="Maximum word length"),
    conn: Connection = Depends(get_db_connection)):
    
    if lang:
        validate_language(lang)
        
    result = words_handler.get_random(conn, lang, min_length, max_length)
    return {"word": result["value"], "lang": result["lang"]}

@router.get("/stats/", response_model=StatsResponse, summary="Get statistics of words", description="Retrieve statistics including total count, min, max, avg length, and top items.")
def get_word_stats(conn: Connection = Depends(get_db_connection)):
    stats, top_items = words_handler.get_stats(conn)
    top_words_list = [{"value": row[0], "count": row[1]} for row in top_items]
    return {
        "total_words": stats[0],
        "min_letters_value": stats[1],
        "max_letters_value": stats[2],
        "avg_length": stats[3],
        "top_words": top_words_list
    }

__all__ = ['router']