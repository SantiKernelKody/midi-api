from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from models.dashboard_user import DashboardUser
from schemas.user_settings import UpdatePasswordData, UpdateUserData
from utils.jwt_helper import get_current_user
from utils.auth import get_password_hash, verify_password


router = APIRouter()

@router.put("/update_user")
def update_user(
    update_data: UpdateUserData,
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user)
):
    # Buscar al usuario en la base de datos
    user = db.query(DashboardUser).filter(DashboardUser.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Actualizar los datos del usuario
    user.name = update_data.name
    user.last_name = update_data.last_name
    user.user_name = update_data.email  # Asumimos que user_name es el email

    db.commit()
    db.refresh(user)

    return {"message": "User data updated successfully"}


@router.put("/change_password")
def change_password(
    password_data: UpdatePasswordData,
    db: Session = Depends(get_db),
    current_user: DashboardUser = Depends(get_current_user)
):
    # Buscar al usuario en la base de datos
    user = db.query(DashboardUser).filter(DashboardUser.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verificar la contraseña actual
    if not verify_password(password_data.old_password, user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    # Actualizar la contraseña del usuario
    user.password = get_password_hash(password_data.new_password)
    db.commit()
    db.refresh(user)

    return {"message": "Password changed successfully"}
