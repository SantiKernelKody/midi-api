from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session
from datetime import timedelta, datetime

from schemas.dashboard_user import DashboardUserCreate, Token
from schemas.token import TokenData
from schemas.auth import LoginRequest, SignupRequest
from models.dashboard_user import DashboardUser as DashboardUserModel
from models.user_role import UserRole as UserRoleModel
from core import security
from core.config import settings
from db.session import get_db
from utils.email import send_email
from crud.dashboard_user import get_user_by_email_and_role, create_user, get_user, update_user_password
from utils.jwt_helper import create_access_token, decode_access_token, get_current_user

router = APIRouter()

# Ruta para login
@router.post("/login", response_model=Token)
def login_for_access_token(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email_and_role(db, email=login_request.email, role_name=login_request.role_name)
    if not user or not security.verify_password(login_request.rawpassword, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email, password, or role",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(weeks=1)
    access_token = create_access_token(
        user_id=user.id,
        role_id=user.role_id
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify_signup_token")
def verify_signup_token(
    token: str,
    db: Session = Depends(get_db)
):
    try:
        # Decodificar el token para obtener el user_id
        payload = decode_access_token(token)
        user_id = payload.user_id
        if not user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido")
        
        # Buscar al usuario en la base de datos
        user = get_user(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        
        # Retornar la información básica del usuario
        return {
            "name": user.name,
            "last_name": user.last_name,
            "email": user.email  # Suponiendo que user_name es el email
        }
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido")


@router.post("/signup", response_model=Token)
def signup(
    signup_data: SignupRequest,
    db: Session = Depends(get_db)
):
    try:
        # Decodificar el token para obtener el user_id
        payload = decode_access_token(signup_data.token)
        print(f"Payload en signup: {payload}")
        user_id = payload.user_id
        if not user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido")
        
        # Buscar al usuario en la base de datos
        user = get_user(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        
        # Actualizar la información del usuario con los datos proporcionados
        updated_user = update_user_password(
            db=db,
            user=user,
            name=signup_data.name,
            last_name=signup_data.last_name,
            rawpassword=signup_data.rawpassword,
            email=signup_data.email
        )
        
        # Generar un nuevo token de acceso con una expiración de una semana
        access_token = create_access_token(
            user_id=updated_user.id,
            role_id=updated_user.role_id,
        )
        
        # Retornar el nuevo token de acceso
        return {"access_token": access_token, "token_type": "bearer"}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido")