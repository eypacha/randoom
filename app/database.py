import sqlite3

def get_db_connection():
    conn = sqlite3.connect('random_data.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS random_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value INTEGER NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS random_words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT NOT NULL,
            lang TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
