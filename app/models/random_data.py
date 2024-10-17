from fastapi import HTTPException
import random

class RandomData:
    def __init__(self, table_name):
        self.table_name = table_name

    def insert(self, conn, value):
        conn.execute(f'INSERT INTO {self.table_name} (value) VALUES (?)', (value,))
        conn.commit()

    def get_random(self, conn):
        items = conn.execute(f'SELECT value FROM {self.table_name}').fetchall()
        if not items:
            raise HTTPException(status_code=404, detail=f"No items found in {self.table_name}")
        return random.choice(items)["value"]

    def get_stats(self, conn):
        stats = conn.execute(f'''
            SELECT COUNT(value) as total_items
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