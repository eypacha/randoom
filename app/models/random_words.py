from .random_data import RandomData
from fastapi import HTTPException
import random

class RandomWords(RandomData):
    def __init__(self):
        super().__init__('random_words')

    def insert(self, conn, value, lang):
        conn.execute(f'INSERT INTO {self.table_name} (value, lang) VALUES (?, ?)', (value, lang))
        conn.commit()

    def get_random(self, conn, lang=None, min_length=None, max_length=None):
        query = f'SELECT value, lang FROM {self.table_name}'
        conditions = []
        params = []
        if lang:
            conditions.append('lang = ?')
            params.append(lang)
        if min_length is not None:
            conditions.append('LENGTH(value) >= ?')
            params.append(min_length)
        if max_length is not None:
            conditions.append('LENGTH(value) <= ?')
            params.append(max_length)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY RANDOM() LIMIT 1'
        
        result = conn.execute(query, params).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail=f"No items found in {self.table_name}")
        
        return {"value": result['value'], "lang": result['lang']}

    def get_stats(self, conn):
        stats = conn.execute(f'''
            SELECT COUNT(value) as total_items,
                   MIN(LENGTH(value)) as min_letters_value,
                   MAX(LENGTH(value)) as max_letters_value,
                   AVG(LENGTH(value)) as avg_length
            FROM {self.table_name}
        ''').fetchone()
        
        top_items = conn.execute(f'''
            SELECT value, COUNT(value) as count
            FROM {self.table_name}
            GROUP BY value
            ORDER BY count DESC
            LIMIT 10
        ''').fetchall()
        
        return stats, top_items