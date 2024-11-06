from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Genera una sesión de base de datos para cada solicitud y la cierra al finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()