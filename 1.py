import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / 'data' / 'school.db'
print(f"📁 Проверяю базу: {db_path}")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Проверяем структуру таблицы users
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()

print("📊 Структура таблицы users:")
if columns:
    for col in columns:
        print(f"  {col[1]} - {col[2]} {'NOT NULL' if col[3] else 'NULL'}")
else:
    print("  Таблица users не существует!")
    
    # Создаём таблицу, если её нет
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
    print("✅ Таблица users создана!")

conn.close()