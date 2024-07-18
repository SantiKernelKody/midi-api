from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import timedelta

from schemas.dashboard_user import DashboardUserCreate, DashboardUser, Token
from schemas.player import PlayerCreate
from models.dashboard_user import DashboardUser as DashboardUserModel
from models.user_role import UserRole as UserRoleModel
from models.player import Player as PlayerModel
from core import security
from core.config import settings
from db.session import get_db
from utils.email import send_email
from crud.dashboard_user import get_user_by_email, get_user_by_email_and_role, create_user, get_user, get_role, get_role_by_name
from crud.player import create_player

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Ruta para login
@router.post("/token", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email_and_role(db, email=form_data.username, role_name=form_data.client_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email, password or role",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not security.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email, password or role",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "role": user.role_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta para signup de profesores (teachers)
@router.post("/signup_teacher", response_model=DashboardUser)
def signup_teacher(email: str, name: str, last_name: str, db: Session = Depends(get_db)):
    role = get_role_by_name(db, role_name="teacher")
    if not role:
        raise HTTPException(status_code=400, detail="Role 'teacher' not found")
    
    user_data = DashboardUserCreate(email=email, name=f"{name} {last_name}", password="default_password", role_id=role.id)
    new_user = create_user(db=db, user=user_data)

    # Generar hash para el usuario
    hash_data = {"user_id": new_user.id, "role_id": new_user.role_id}
    hash = security.create_access_token(data=hash_data, expires_delta=timedelta(days=7))

    # Enviar correo electrónico con el link de signup
    signup_link = f"{settings.FRONTEND_URL}/signup?hash={hash}"
    email_context = {
        "name": new_user.name,
        "signup_link": signup_link
    }
    send_email(to_email=new_user.email, subject="Complete your registration", template_name="invitation_email.html", context=email_context)

    return new_user

# Ruta para signup de estudiantes (players) y sus padres (parents)
@router.post("/signup_player", response_model=DashboardUser)
def signup_player(full_name: str, school_id: int, course_id: int, age: int, parent_email: str, db: Session = Depends(get_db)):
    # Crear registro del estudiante
    player_data = PlayerCreate(full_name=full_name, school_id=school_id, course_id=course_id, age=age)
    new_player = create_player(db=db, player=player_data)

    # Crear cuenta para el padre de familia
    role = get_role_by_name(db, role_name="parent")
    if not role:
        raise HTTPException(status_code=400, detail="Role 'parent' not found")
    
    user_data = DashboardUserCreate(email=parent_email, name=full_name, password="default_password", role_id=role.id)
    new_parent = create_user(db=db, user=user_data)

    # Generar hash para el padre
    hash_data = {"user_id": new_parent.id, "role_id": new_parent.role_id}
    hash = security.create_access_token(data=hash_data, expires_delta=timedelta(days=7))

    # Enviar correo electrónico con el link de signup
    signup_link = f"{settings.FRONTEND_URL}/signup?hash={hash}"
    email_context = {
        "name": new_parent.name,
        "signup_link": signup_link
    }
    send_email(to_email=new_parent.email, subject="Complete your registration", template_name="invitation_email.html", context=email_context)

    return new_parent

# Ruta para verificar el hash de signup
@router.get("/verify_hash/{hash}")
def verify_hash(hash: str, db: Session = Depends(get_db)):
    try:
        payload = security.decode_access_token(hash)
        if payload is None:
            raise HTTPException(status_code=400, detail="Invalid hash")
        user_id = payload.get("user_id")
        role_id = payload.get("role_id")
        user = get_user(db, user_id=user_id)
        role = get_role(db, role_id=role_id)
        if not user or not role:
            raise HTTPException(status_code=400, detail="Invalid user or role")
        return {"user": user, "role": {"id": role.id, "name": role.name}}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid hash")
