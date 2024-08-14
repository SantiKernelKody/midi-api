from pydantic import BaseModel
from typing import Optional

class AvatarBase(BaseModel):
    name: str
    description: Optional[str]

class AvatarCreate(AvatarBase):
    pass

class AvatarUpdate(AvatarBase):
    pass

class AvatarInDBBase(AvatarBase):
    id: int

    class Config:
        orm_mode = True

class Avatar(AvatarInDBBase):
    pass

class AvatarInDB(AvatarInDBBase):
    pass
