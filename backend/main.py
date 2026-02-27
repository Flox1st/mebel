import sys
import os
import json
from pathlib import Path

# Добавляем путь к папке backend
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI, Form, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Импорты без точек!
import models
import auth
import database

app = FastAPI()

# Пути к фронтенду
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Шаблонизатор
templates = Jinja2Templates(directory=str(FRONTEND_DIR))

# Создаём таблицы
models.Base.metadata.create_all(bind=database.engine)

# Зависимость для БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========== API ==========
class ReviewCreate(BaseModel):
    product_id: int
    rating: int
    text: str

# ========== API ДЛЯ ОТЗЫВОВ ==========

@app.post("/api/reviews")
async def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db)
):
    """Создать новый отзыв (без авторизации)"""
    try:
        # Проверяем, существует ли товар
        product = db.query(models.Product).filter(models.Product.id == review.product_id).first()
        if not product:
            return JSONResponse(
                content={"success": False, "message": "Товар не найден"},
                status_code=404
            )
        
        # Создаём отзыв с user_id = 1 (или можно сделать отдельную таблицу для гостей)
        # Для простоты используем user_id = 1 (первый пользователь)
        db_review = models.Review(
            user_id=1,  # Временно привязываем к первому пользователю
            product_id=review.product_id,
            rating=review.rating,
            text=review.text
        )
        
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
        return {
            "success": True,
            "message": "Отзыв добавлен",
            "review_id": db_review.id
        }
        
    except Exception as e:
        print(f"❌ Ошибка создания отзыва: {e}")
        return JSONResponse(
            content={"success": False, "message": f"Ошибка сервера: {str(e)}"},
            status_code=500
        )


@app.get("/api/products/{product_id}/reviews")
async def get_product_reviews(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Получить все отзывы для товара"""
    reviews = db.query(models.Review).filter(
        models.Review.product_id == product_id
    ).order_by(models.Review.created_at.desc()).all()
    
    result = []
    for r in reviews:
        result.append({
            "id": r.id,
            "user_name": r.user.full_name if r.user else "Пользователь",
            "rating": r.rating,
            "text": r.text,
            "created_at": r.created_at.strftime("%d.%m.%Y")
        })
    
    return {"reviews": result}

@app.post("/api/register")
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    phone: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Проверяем, что все поля заполнены
        if not username or not email or not password or not full_name or not phone:
            return JSONResponse(
                content={"success": False, "message": "Все поля обязательны"},
                status_code=400
            )
        
        # Проверяем, существует ли пользователь
        existing = db.query(models.User).filter(
            (models.User.username == username) | (models.User.email == email)
        ).first()
        
        if existing:
            return JSONResponse(
                content={"success": False, "message": "Пользователь уже существует"},
                status_code=400
            )
        
        # Создаём пользователя
        hashed = auth.get_password_hash(password)
        
        # Убедись, что в models.User есть все эти поля!
        user = models.User(
            username=username,
            email=email,
            hashed_password=hashed,
            full_name=full_name,
            phone=phone
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {
            "success": True,
            "message": "Регистрация успешна",
            "user_id": user.id
        }
        
    except Exception as e:
        print(f"❌ Ошибка регистрации: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return JSONResponse(
            content={"success": False, "message": f"Ошибка сервера: {str(e)}"},
            status_code=500
        )

@app.post("/api/login")
async def login(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        data = await request.form()
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            return JSONResponse(
                content={"success": False, "message": "Логин и пароль обязательны"},
                status_code=400
            )
        
        user = auth.authenticate_user(db, username, password)
        
        if not user:
            return JSONResponse(
                content={"success": False, "message": "Неверный логин или пароль"},
                status_code=401
            )
        
        token = auth.create_access_token(data={"sub": user.username})
        
        return {
            "success": True,
            "message": "Вход выполнен",
            "access_token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name
            }
        }
        
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": f"Ошибка: {str(e)}"},
            status_code=500
        )


# ========== ТОВАРЫ ==========

@app.get("/api/products")
async def get_products(
    category: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)
    if category and category != "all":
        query = query.filter(models.Product.category == category)
    
    products = query.all()
    
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "category": p.category,
            "image": p.image,
            "specs": json.loads(p.specs) if p.specs else {},
            "stock": p.stock
        })
    
    return {"products": result}


@app.get("/api/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        return JSONResponse(
            content={"success": False, "message": "Товар не найден"},
            status_code=404
        )
    
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "image": product.image,
        "specs": json.loads(product.specs) if product.specs else {},
        "stock": product.stock
    }


# ========== СТРАНИЦЫ ==========

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/products", response_class=HTMLResponse)
async def serve_products(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})


@app.get("/product/{product_id}", response_class=HTMLResponse)
async def serve_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        return templates.TemplateResponse("index.html", {"request": request})
    
    # Подготовка данных для шаблона
    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "image": product.image,
        "image_url": product.image_url if hasattr(product, 'image_url') else None,
        "specs": json.loads(product.specs) if product.specs else {},
        "stock": product.stock
    }
    
    return templates.TemplateResponse(
        "product_template.html", 
        {
            "request": request,
            "product": product_data
        }
    )


@app.get("/register", response_class=HTMLResponse)
async def serve_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/cart", response_class=HTMLResponse)
async def serve_cart(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def serve_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/contacts", response_class=HTMLResponse)
async def serve_contacts(request: Request):
    return templates.TemplateResponse("contacts.html", {"request": request})


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "API работает"}