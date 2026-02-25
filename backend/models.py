from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # храним хэш пароля!
    created_at = Column(DateTime, default=func.now())

    # Для отладки
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"