from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class DashboardUserBase(BaseModel):
    name: str
    last_name: str
    email: EmailStr

class DashboardUserCreate(DashboardUserBase):
    password: str
    role_id: int

class DashboardUserUpdate(DashboardUserBase):
    password: Optional[str] = None
    role_id: Optional[int] = None

class DashboardUserInDBBase(DashboardUserBase):
    id: int
    role_id: int
    created_at: datetime

    class Config:
         from_attributes = True

class DashboardUser(DashboardUserInDBBase):
    pass

class DashboardUserInDB(DashboardUserInDBBase):
    hashed_password: str
