import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / 'data' / 'school.db'
print(f"📁 Обновляю базу: {db_path}")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Проверяем структуру таблицы users
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()
column_names = [col[1] for col in columns]
print("Существующие колонки:", column_names)

# Добавляем недостающие колонки
if 'full_name' not in column_names:
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
        print("✅ Добавлена колонка full_name")
    except:
        print("⏩ full_name уже существует")

if 'phone' not in column_names:
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
        print("✅ Добавлена колонка phone")
    except:
        print("⏩ phone уже существует")

conn.commit()
conn.close()
print("✅ База обновлена!")