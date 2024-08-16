from sqlalchemy.orm import Session
from models.dashboard_user import DashboardUser
from models.user_role import UserRole

def is_admin(user: DashboardUser, db: Session) -> bool:
    role = db.query(UserRole).filter(UserRole.id == user.role_id).first()
    return role and role.name.lower() == "admin"

def is_teacher(user: DashboardUser, db: Session) -> bool:
    role = db.query(UserRole).filter(UserRole.id == user.role_id).first()
    return role and role.name.lower() == "teacher"
