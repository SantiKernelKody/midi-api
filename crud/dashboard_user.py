from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from schemas.dashboard_user import DashboardUserCreate
from models.dashboard_user import DashboardUser
from models.user_role import UserRole
from core.security import get_password_hash

def get_user_by_email_and_role(db: Session, email: str, role_name: str):
    return db.query(DashboardUser).join(UserRole).filter(DashboardUser.email == email, UserRole.name == role_name).first()

def create_user(db: Session, user: DashboardUserCreate):
    db_user = DashboardUser(
        email=user.email,
        password=get_password_hash(user.password),
        name=user.name,
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(DashboardUser).filter(DashboardUser.id == user_id).first()

def update_user_password(db: Session, user: DashboardUser, name: str, last_name: str, rawpassword: str, email: str):
    user.name = name
    user.last_name = last_name
    user.password = get_password_hash(rawpassword)
    user.email = email
    db.commit()
    db.refresh(user)
    return user

# construye funcion de update_user_password que solo reciba la contraseña y el id del usuario
def update_only_user_password(db: Session, user_id: int, rawpassword: str):
    user = db.query(DashboardUser).filter(DashboardUser.id == user_id).first()
    user.password = get_password_hash(rawpassword)
    db.commit()
    db.refresh(user)
    return user
