import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Usar DATABASE_URL do Railway, ou fallback para SQLite local
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./escola.db")

# Se usar PostgreSQL, remove "postgresql://" e usa "postgresql+psycopg2://"
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")

# Create Database Engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    except ValueError as e:
        # Sanitizar URL para não mostrar password nos logs
        sanitized_url = (
            DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else "INVALID_URL_FORMAT"
        )
        print(
            f"❌ CRITICAL ERROR: Invalid DATABASE_URL format. It seems to contain strict text instead of numbers (e.g. 'port')."
        )
        print(f"❌ Connection attempt to: ...@{sanitized_url}")
        print(
            "❌ Please check your Railway Variables. Do NOT manually add DATABASE_URL if you added a PostgreSQL service."
        )
        raise e

# Session Local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
