import sqlite3
import os

# Путь к базе данных (относительно этого файла)
db_path = os.path.join('data', 'school.db')

print(f"🔍 Ищу базу по пути: {os.path.abspath(db_path)}")

# Проверяем, существует ли файл
if not os.path.exists(db_path):
    print("❌ База не найдена!")
    print("Проверь:")
    print("  - Есть ли папка 'data' в текущей папке?")
    print("  - Есть ли в ней файл 'school.db'?")
    exit()

# Подключаемся
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("✅ База найдена!\n")

# Получаем все таблицы
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("📊 Таблицы в базе данных:")
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    print(f"  - {table[0]} ({count} записей)")

print("\n👥 Пользователи:")
cursor.execute("SELECT id, username, email, created_at FROM users")
users = cursor.fetchall()

if users:
    for user in users:
        print(f"  ID: {user[0]}, Логин: {user[1]}, Email: {user[2]}, Создан: {user[3]}")
    print(f"\nВсего пользователей: {len(users)}")
else:
    print("  Пользователей пока нет")

conn.close()