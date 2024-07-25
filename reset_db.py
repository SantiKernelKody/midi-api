from sqlalchemy.orm import Session
from sqlalchemy import text
from db.session import SessionLocal
from models.user_role import UserRole
from models.dashboard_user import DashboardUser

def reset_tables():
    db: Session = SessionLocal()

    # Reiniciar las tablas eliminando todos los registros
    db.query(DashboardUser).delete()
    db.query(UserRole).delete()

    # Reiniciar contadores de ID (opcional, solo para PostgreSQL)
    db.execute(text("ALTER SEQUENCE dashboard_user_id_seq RESTART WITH 1"))
    db.execute(text("ALTER SEQUENCE user_role_id_seq RESTART WITH 1"))

    db.commit()
    db.close()

if __name__ == "__main__":
    reset_tables()
