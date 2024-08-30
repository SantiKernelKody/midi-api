from sqlalchemy.orm import Session
from models.dashboard_user import DashboardUser
from models.user_role import UserRole

def is_admin(user: DashboardUser, db: Session) -> bool:
    role = db.query(UserRole).filter(UserRole.id == user.role_id).first()
    return role and role.name.lower() == "admin"

def is_teacher(user: DashboardUser, db: Session) -> bool:
    role = db.query(UserRole).filter(UserRole.id == user.role_id).first()
    return role and role.name.lower() == "teacher"

# crea una funcion que reciba el name del UserRole y retorne el id de ese role
def get_role_id_by_name(role_name: str, db: Session) -> int:
    role = db.query(UserRole).filter(UserRole.name == role_name).first()
    return role.id if role else None

def get_parent_role_id(db: Session) -> int:
    return get_role_id_by_name("parent", db)