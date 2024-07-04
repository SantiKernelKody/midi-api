from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Crear el motor de la base de datos
engine = create_engine(settings.DATABASE_URL)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
