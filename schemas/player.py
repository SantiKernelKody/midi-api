from pydantic import BaseModel
from datetime import datetime

class PlayerBase(BaseModel):
    school_id: int
    special_need_id: int
    full_name: str
    edad: int = None
    ethnicity: str = None
    special_need_description: str = None
    special_need: bool = None
    user_name: str = None
    password: str = None

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    pass

class PlayerInDBBase(PlayerBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class Player(PlayerInDBBase):
    pass
