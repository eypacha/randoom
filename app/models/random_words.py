from .random_data import RandomData
from fastapi import HTTPException
import random

class RandomWords(RandomData):
    def __init__(self):
        super().__init__('random_words')

    def insert(self, conn, value, lang):
        conn.execute(f'INSERT INTO {self.table_name} (value, lang) VALUES (?, ?)', (value, lang))
        conn.commit()

    def get_random(self, conn, lang=None):
        if lang:
            items = conn.execute(f'SELECT value FROM {self.table_name} WHERE lang = ?', (lang,)).fetchall()
        else:
            items = conn.execute(f'SELECT value FROM {self.table_name}').fetchall()

        if not items:
            raise HTTPException(status_code=404, detail=f"No items found in {self.table_name}")
        
        return random.choice(items)["value"]
