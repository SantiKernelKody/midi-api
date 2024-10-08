import jwt
from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.session import SessionLocal, get_db
from models.dashboard_user import DashboardUser
from core.config import settings
from schemas.token import TokenData

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 1 week



def create_access_token(user_id: int, role_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"user_id": user_id, "role_id": role_id, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(user_id=payload["user_id"], role_id=payload["role_id"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(request: Request, db: Session = Depends(get_db)) -> DashboardUser:
    token_data = request.state.user  # Retrieve token data from request state
    print(f"Token data en JWT HELPER: {token_data}")
    user = db.query(DashboardUser).filter(DashboardUser.id == token_data.user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
