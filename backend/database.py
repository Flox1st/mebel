from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base 
import os

# Создаем папку data если её нет
os.makedirs("../data", exist_ok=True)

# SQLite база данных (путь относительно backend/)
SQLALCHEMY_DATABASE_URL = "sqlite:///../data/school.db"

# Создаем движок
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Генератор сессий для зависимостей"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Создает все таблицы в базе данных"""
    Base.metadata.create_all(bind=engine)