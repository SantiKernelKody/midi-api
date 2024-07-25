from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.user_role import UserRole
from models.dashboard_user import DashboardUser
from core.security import get_password_hash

def seed():
    db: Session = SessionLocal()

    # Crear roles
    admin_role = UserRole(name="admin", display_name="Administrator", description="Admin role")
    teacher_role = UserRole(name="teacher", display_name="Teacher", description="Teacher role")
    parent_role = UserRole(name="parent", display_name="Parent", description="Parent role")

    db.add(admin_role)
    db.add(teacher_role)
    db.add(parent_role)
    db.commit()

    # Crear usuarios
    admin_user = DashboardUser(
        email="admin@example.com",
        password=get_password_hash("adminpassword"),
        name="Admin",
        last_name="User",
        role_id=admin_role.id
    )
    teacher_user = DashboardUser(
        email="teacher@example.com",
        password=get_password_hash("teacherpassword"),
        name="Teacher",
        last_name="User",
        role_id=teacher_role.id
    )
    parent_user = DashboardUser(
        email="parent@example.com",
        password=get_password_hash("parentpassword"),
        name="Parent",
        last_name="User",
        role_id=parent_role.id
    )

    db.add(admin_user)
    db.add(teacher_user)
    db.add(parent_user)
    db.commit()

    db.close()

if __name__ == "__main__":
    seed()
