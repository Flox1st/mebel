from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Связь с отзывами
    reviews = relationship("Review", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    image = Column(String, nullable=False)
    specs = Column(Text, nullable=False)
    stock = Column(String, default="В наличии")
    created_at = Column(DateTime, default=func.now())
    
    # Связь с отзывами
    reviews = relationship("Review", back_populates="product")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Связи
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")