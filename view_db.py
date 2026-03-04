import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / 'data' / 'school.db'
print(f"🔍 Ищу базу по пути: {db_path}")

if not db_path.exists():
    print("❌ База не найдена!")
    exit()

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("✅ База найдена!\n")

# ===== ВСЕ ТАБЛИЦЫ =====
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("📊 ТАБЛИЦЫ В БАЗЕ ДАННЫХ:")
print("-" * 50)
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    print(f"  • {table[0]}: {count} записей")
print()

# ===== ПОЛЬЗОВАТЕЛИ =====
print("👥 ПОЛЬЗОВАТЕЛИ:")
print("-" * 50)
try:
    cursor.execute("SELECT id, username, email, full_name, phone, created_at FROM users")
    users = cursor.fetchall()
    
    if users:
        for user in users:
            print(f"  ID: {user[0]}")
            print(f"     Логин: {user[1]}")
            print(f"     Email: {user[2]}")
            print(f"     Имя: {user[3]}")
            print(f"     Телефон: {user[4]}")
            print(f"     Создан: {user[5]}")
            print()
        print(f"  Всего пользователей: {len(users)}")
    else:
        print("  Пользователей нет")
except sqlite3.OperationalError:
    print("  Таблица users не найдена")
print()

# ===== ТОВАРЫ =====
print("📦 ТОВАРЫ:")
print("-" * 50)
try:
    cursor.execute("SELECT id, name, price, category, stock FROM products ORDER BY id")
    products = cursor.fetchall()
    
    if products:
        for p in products:
            print(f"  ID: {p[0]}")
            print(f"     Название: {p[1]}")
            print(f"     Цена: {p[2]:,} ₽")
            print(f"     Категория: {p[3]}")
            print(f"     Наличие: {p[4]}")
            print()
        print(f"  Всего товаров: {len(products)}")
    else:
        print("  Товаров нет")
except sqlite3.OperationalError:
    print("  Таблица products не найдена")
print()

# ===== ОТЗЫВЫ (С ИНФОРМАЦИЕЙ О ТОВАРАХ И ПОЛЬЗОВАТЕЛЯХ) =====
print("💬 ОТЗЫВЫ:")
print("-" * 50)
try:
    # Получаем отзывы с JOIN, чтобы видеть названия товаров и имена пользователей
    cursor.execute('''
        SELECT 
            r.id,
            r.rating,
            r.text,
            r.created_at,
            p.name as product_name,
            u.username as user_name,
            u.full_name
        FROM reviews r
        LEFT JOIN products p ON r.product_id = p.id
        LEFT JOIN users u ON r.user_id = u.id
        ORDER BY r.created_at DESC
    ''')
    reviews = cursor.fetchall()
    
    if reviews:
        for r in reviews:
            print(f"  ID отзыва: {r[0]}")
            print(f"     Оценка: {'⭐' * r[1]}{'☆' * (5-r[1])} ({r[1]}/5)")
            print(f"     Текст: {r[2][:100]}{'...' if len(r[2]) > 100 else ''}")
            print(f"     Дата: {r[3]}")
            print(f"     Товар: {r[4]}")
            print(f"     Пользователь: {r[5] or 'Гость'} ({r[6] or 'Неизвестно'})")
            print()
        print(f"  Всего отзывов: {len(reviews)}")
    else:
        print("  Отзывов пока нет")
except sqlite3.OperationalError as e:
    print(f"  Таблица reviews не найдена или ошибка: {e}")
print()


print("\n" + "="*50)
conn.close()