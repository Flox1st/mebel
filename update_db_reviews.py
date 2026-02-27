import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / 'data' / 'school.db'
print(f"📁 Обновляю базу: {db_path}")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Создаём таблицу reviews
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
''')

print("✅ Таблица reviews создана или уже существует")

conn.commit()
conn.close()
print("✅ База данных обновлена!")