from sqlalchemy.orm import Session
from models.dashboard_user import DashboardUser
from models.player import Player
from utils.auth import verify_password


def authenticate_user(db: Session, email: str, password: str) -> DashboardUser | bool:
    user = db.query(DashboardUser).filter(DashboardUser.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


