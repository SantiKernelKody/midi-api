from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlayerBase(BaseModel):
    name: str
    last_name: str
    edad: int
    ethnicity: str
    special_need_description: Optional[str] = None
    special_need: bool
    user_name: str
    password: str

class PlayerCreate(PlayerBase):
    school_id: int
    avatar_id: Optional[int] = None
    special_need_id: Optional[int] = None

class PlayerUpdate(PlayerBase):
    school_id: Optional[int] = None
    avatar_id: Optional[int] = None
    special_need_id: Optional[int] = None

class PlayerInDBBase(PlayerBase):
    id: int
    school_id: int
    avatar_id: Optional[int] = None
    special_need_id: Optional[int] = None
    created_at: datetime

    class Config:
         from_attributes = True

class Player(PlayerInDBBase):
    pass

class PlayerInDB(PlayerInDBBase):
    hashed_password: str
