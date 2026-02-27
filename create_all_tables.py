import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / 'data' / 'school.db'
print(f"📁 Создаю таблицы в: {db_path}")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Создаём таблицу users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print("✅ Таблица users создана")

# Создаём таблицу products
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price INTEGER NOT NULL,
        category TEXT NOT NULL,
        image TEXT NOT NULL,
        specs TEXT NOT NULL,
        stock TEXT DEFAULT 'В наличии',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print("✅ Таблица products создана")

# Создаём таблицу reviews
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        author_name TEXT,
        product_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
''')
print("✅ Таблица reviews создана")

conn.commit()
conn.close()
print("✅ Все таблицы созданы!")