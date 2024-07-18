from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class DashboardUserBase(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    role_id: int

class DashboardUserCreate(DashboardUserBase):
    email: EmailStr
    name: str
    last_name: str
    role_id: int
    

class DashboardUserUpdate(DashboardUserBase):
    password: Optional[str] = None

class DashboardUserInDBBase(DashboardUserBase):
    id: int
    role_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class DashboardUser(DashboardUserInDBBase):
    pass

class DashboardUserInDB(DashboardUserInDBBase):
    hashed_password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str