from sqlalchemy.orm import Session
from schemas.dashboard_user import DashboardUserCreate
from models.dashboard_user import DashboardUser
from models.user_role import UserRole

def get_user_by_email(db: Session, email: str):
    return db.query(DashboardUser).filter(DashboardUser.email == email).first()

def get_user_by_email_and_role(db: Session, email: str, role_name: str):
    role = db.query(UserRole).filter(UserRole.name == role_name).first()
    if not role:
        return None
    return db.query(DashboardUser).filter(DashboardUser.email == email, DashboardUser.role_id == role.id).first()

def create_user(db: Session, user: DashboardUserCreate):
    db_user = DashboardUser(
        email=user.email,
        password=user.password,
        name=user.name,
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(DashboardUser).filter(DashboardUser.id == user_id).first()

def get_role(db: Session, role_id: int):
    return db.query(UserRole).filter(UserRole.id == role_id).first()

def get_role_by_name(db: Session, role_name: str):
    return db.query(UserRole).filter(UserRole.name == role_name).first()
