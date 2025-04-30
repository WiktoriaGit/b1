from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Pobierz URL z ENV (Render -> Environment -> DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL")

# Tworzenie silnika do bazy danych
engine = create_engine(DATABASE_URL)

# Sesja do komunikacji z bazą
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bazowa klasa dla modeli SQLAlchemy
Base = declarative_base()

# Helper do pobierania sesji w FastAPI endpointach
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
