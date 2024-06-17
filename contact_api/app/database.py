from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL підключення до бази даних PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@db:5432/contacts"

# Створення об'єкта двигуна бази даних
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Налаштування сесії бази даних
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для моделей SQLAlchemy
Base = declarative_base()







