from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import timedelta, datetime

from schemas.dashboard_user import DashboardUserCreate, Token
from schemas.token import TokenData
from models.dashboard_user import DashboardUser as DashboardUserModel
from models.user_role import UserRole as UserRoleModel
from core import security
from core.config import settings
from db.session import get_db
from utils.email import send_email
from crud.dashboard_user import get_user_by_email_and_role, create_user, get_user, update_user_password
from utils.token import create_access_token, decode_access_token

router = APIRouter()

# Ruta para login
@router.post("/login", response_model=Token)
def login_for_access_token(email: str, rawpassword: str, role_name: str, db: Session = Depends(get_db)):
    user = get_user_by_email_and_role(db, email=email, role_name=role_name)
    if not user or not security.verify_password(rawpassword, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email, password, or role",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(weeks=1)
    access_token = create_access_token(
        data={"user_id": user.id, "role_id": user.role_id, "created_at": str(datetime.utcnow())}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta para signup de profesores y padres
@router.post("/signup", response_model=Token)
def signup(name: str, last_name: str, rawpassword: str, email: str, token: str, db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        
        user = get_user(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        updated_user = update_user_password(db, user=user, name=name, last_name=last_name, rawpassword=rawpassword, email=email)
        
        access_token_expires = timedelta(weeks=1)
        access_token = create_access_token(
            data={"user_id": updated_user.id, "role_id": updated_user.role_id, "created_at": str(datetime.utcnow())}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
