from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import hashlib
import os
from pathlib import Path

app = FastAPI()

# Пути к фронтенду
BASE_DIR = Path(__file__).resolve().parent.parent  # Папка Lab1
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR

# Подключаем статические файлы (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Шаблонизатор для HTML
templates = Jinja2Templates(directory=str(FRONTEND_DIR))


# ----------------- Простая база данных -----------------

def get_db_connection():
    """Создает соединение с SQLite базой"""
    db_path = BASE_DIR / "data" / "school.db"
    # Создаем папку data если её нет
    db_path.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Инициализирует базу данных"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")


# Инициализируем БД при старте
init_db()


# ----------------- API эндпоинты -----------------

@app.post("/api/register")
async def register(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)
):
    """Простая регистрация пользователя"""

    # Хэшируем пароль
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        user_id = cursor.lastrowid
        conn.commit()

        return {
            "success": True,
            "message": "Регистрация успешна",
            "user_id": user_id
        }

    except sqlite3.IntegrityError:
        return JSONResponse(
            content={"success": False, "message": "Пользователь уже существует"},
            status_code=400
        )
    finally:
        conn.close()


@app.post("/api/login")
async def login(request: Request):
    """Простой вход пользователя"""
    try:
        print(f"=== DEBUG LOGIN REQUEST ===")
        print(f"Headers: {dict(request.headers)}")
        
        content_type = request.headers.get('content-type', '')
        print(f"Content-Type: {content_type}")
        
        username = None
        password = None
        
        if 'multipart/form-data' in content_type:
            print("Parsing multipart/form-data...")
            form_data = await request.form()
            print(f"Form data keys: {list(form_data.keys())}")
            username = form_data.get("username")
            password = form_data.get("password")
            
        elif 'application/x-www-form-urlencoded' in content_type:
            print("Parsing x-www-form-urlencoded...")
            form_data = await request.form()
            username = form_data.get("username")
            password = form_data.get("password")
            
        else:
            print("Trying JSON...")
            try:
                json_data = await request.json()
                username = json_data.get("username")
                password = json_data.get("password")
            except:
                print("Failed to parse JSON")
        
        print(f"Extracted - username: '{username}', password: '{password}'")
        print(f"Username type: {type(username)}, Password type: {type(password)}")
        
        if not username or not password:
            print("ERROR: Empty fields!")
            return JSONResponse(
                content={"success": False, "message": "Логин и пароль обязательны"},
                status_code=400
            )
        
        # Преобразуем в строку если это не строка
        if not isinstance(username, str):
            username = str(username)
        if not isinstance(password, str):
            password = str(password)
        
        # Хэшируем пароль
        import hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(f"Hashed password: {hashed_password[:20]}...")
        
        # Ищем пользователя в БД
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user:
            print(f"User found: {user['username']}")
            print(f"DB hash: {user['password'][:20]}...")
            print(f"Input hash: {hashed_password[:20]}...")
            print(f"Match: {user['password'] == hashed_password}")
        
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, hashed_password)
        )
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            print("✅ Login successful!")
            return {
                "success": True,
                "message": "Вход выполнен",
                "user": {
                    "id": user['id'],
                    "username": user['username'],
                    "email": user['email'],
                    "created_at": user['created_at']
                }
            }
        else:
            print("❌ Login failed")
            return JSONResponse(
                content={"success": False, "message": "Неверный логин или пароль"},
                status_code=401
            )
            
    except Exception as e:
        print(f"Login error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            content={"success": False, "message": f"Ошибка сервера: {str(e)}"},
            status_code=500
        )

# ----------------- Обработка HTML страниц -----------------

# Список существующих HTML файлов
HTML_FILES = [
    "index.html", "about.html", "contacts.html", "cart.html"
]


@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    """Главная страница"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/auth", response_class=HTMLResponse)
async def serve_auth(request: Request):
    """Страница авторизации"""
    return templates.TemplateResponse("auth.html", {"request": request})

@app.get("/register")
async def serve_register():
    """Страница регистрации"""
    register_path = FRONTEND_DIR / "register.html"
    if register_path.exists():
        return FileResponse(str(register_path))
    return FileResponse(str(FRONTEND_DIR / "index.html"))


# Динамические маршруты для всех остальных страниц
@app.get("/{page_name}", response_class=HTMLResponse)
async def serve_page(request: Request, page_name: str):
    """Обработка всех остальных страниц"""
    # Проверяем существование файла
    file_path = FRONTEND_DIR / f"{page_name}.html"

    if file_path.exists():
        return templates.TemplateResponse(f"{page_name}.html", {"request": request})

    # Если файл не найден, пробуем без расширения .html
    file_path_no_ext = FRONTEND_DIR / page_name
    if file_path_no_ext.exists() and file_path_no_ext.suffix == '.html':
        return templates.TemplateResponse(page_name, {"request": request})

    # Если страница не найдена - возвращаем 404 или главную
    return templates.TemplateResponse("index.html", {"request": request})


# ----------------- Дополнительные маршруты -----------------

@app.get("/api/health")
async def health_check():
    """Проверка работы API"""
    return {"status": "ok", "message": "API работает"}


@app.get("/api/users")
async def get_all_users():
    """Получить всех пользователей (для отладки)"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, email, created_at FROM users")
    users = cursor.fetchall()
    conn.close()

    return {"users": [dict(user) for user in users]}


# Обработчик для favicon.ico (чтобы не было ошибок 404)
@app.get("/favicon.ico")
async def favicon():
    return FileResponse(FRONTEND_DIR / "favicon.ico" if (FRONTEND_DIR / "favicon.ico").exists() else None)