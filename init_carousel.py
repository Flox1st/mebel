import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / 'data' / 'school.db'
print(f"📁 Добавляю слайды в: {db_path}")

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Создаём таблицу carousel
cursor.execute('''
    CREATE TABLE IF NOT EXISTS carousel (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        subtitle TEXT,
        image_url TEXT NOT NULL,
        link TEXT,
        "order" INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
print("✅ Таблица carousel создана")

# Очищаем таблицу (чтоб не было дублей)
cursor.execute("DELETE FROM carousel")

# Добавляем слайды
slides = [
    {
        "title": "Мягкая мебель",
        "subtitle": "Диваны и кресла для уютного отдыха",
        "image_url": "/static/images/products/divan1.jpg",
        "link": "/products?category=sofas",
        "order": 1
    },
    {
        "title": "Гармоничный стиль",
        "subtitle": "Кровати, шкафы и комоды для вашей спальни",
        "image_url": "/static/images/products/krovat4.jpg",
        "link": "/products?category=beds",
        "order": 2
    },
    {
        "title": "Столы для всего дома",
        "subtitle": "Столы, стулья и кухонные гарнитуры",
        "image_url": "/static/images/products/stol2.jpg",
        "link": "/products?category=tables",
        "order": 3
    },
    {
        "title": "Прихожие",
        "subtitle": "Шкафы, вешалки и тумбы для прихожей",
        "image_url": "/static/images/products/divan3.jpg",
        "link": "/products",
        "order": 4
    }
]

for slide in slides:
    cursor.execute('''
        INSERT INTO carousel (title, subtitle, image_url, link, "order")
        VALUES (?, ?, ?, ?, ?)
    ''', (slide["title"], slide["subtitle"], slide["image_url"], slide["link"], slide["order"]))

conn.commit()

# Проверяем, сколько добавилось
cursor.execute("SELECT COUNT(*) FROM carousel")
count = cursor.fetchone()[0]
print(f"✅ Добавлено {count} слайдов в карусель")

conn.close()