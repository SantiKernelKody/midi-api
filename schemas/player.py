from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlayerBase(BaseModel):
    name: str
    last_name: str
    age: int
    ethnicity: Optional[str] = None
    special_need_description: Optional[str] = None
    special_need: Optional[int] = None
    user_name: str
    password: str

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    pass

class PlayerInDBBase(PlayerBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Player(PlayerInDBBase):
    pass

class PlayerInDB(PlayerInDBBase):
    pass
