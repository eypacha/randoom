from .random_data import RandomData
from fastapi import HTTPException
import random

class RandomNumbers(RandomData):
    def __init__(self):
        super().__init__('random_numbers')

    def insert(self, conn, value):
        conn.execute(f'INSERT INTO {self.table_name} (value) VALUES (?)', (value,))
        conn.commit()

    def get_random(self, conn, lang=None, min_length=None, max_length=None):
        query = f'SELECT value, lang FROM {self.table_name}'  # Selecciona ambos campos
        params = []

        if lang:
            query += ' WHERE lang = ?'
            params.append(lang)

        if min_length is not None:
            query += ' AND LENGTH(value) >= ?'
            params.append(min_length)

        if max_length is not None:
            query += ' AND LENGTH(value) <= ?'
            params.append(max_length)

        items = conn.execute(query, params).fetchall()

        if not items:
            raise HTTPException(status_code=404, detail=f"No items found in {self.table_name}")

        selected_item = random.choice(items)
        return selected_item  # Aquí selecciona un elemento con ambos campos

    def get_stats(self, conn):
        stats = conn.execute(f'''
            SELECT COUNT(value) as total_items,
                   MIN(value) as min_value,
                   MAX(value) as max_value,
                   AVG(value) as avg_value
            FROM {self.table_name}
        ''').fetchone()

        top_items = conn.execute(f'''
            SELECT value, COUNT(value) as count
            FROM {self.table_name}
            GROUP BY value
            ORDER BY count DESC
            LIMIT 10
        ''').fetchall()
        
        return {
            "total_items": stats["total_items"],
            "min_value": stats["min_value"],
            "max_value": stats["max_value"],
            "avg_value": stats["avg_value"],
            "top_items": top_items
        }
