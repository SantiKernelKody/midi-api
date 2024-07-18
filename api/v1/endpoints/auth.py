from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import timedelta

import schemas, models, crud
from core import security
from db.session import get_db
from core.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not security.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "uid": user.id, "urole": user.role_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = security.get_password_hash(user.password)
    return crud.create_user(db=db, user=user)

@router.get("/verify_hash/{hash}")
def verify_hash(hash: str, db: Session = Depends(get_db)):
    try:
        payload = security.decode_access_token(hash)
        if payload is None:
            raise HTTPException(status_code=400, detail="Invalid hash")
        user_id = payload.get("user_id")
        role_id = payload.get("role_id")
        user = crud.get_user(db, user_id=user_id)
        role = crud.get_role(db, role_id=role_id)
        if not user or not role:
            raise HTTPException(status_code=400, detail="Invalid user or role")
        return {"user": user, "role": role}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid hash")
