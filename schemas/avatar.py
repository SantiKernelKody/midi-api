from pydantic import BaseModel

class AvatarBase(BaseModel):
    name: str
    description: str

class AvatarCreate(AvatarBase):
    pass

class AvatarUpdate(AvatarBase):
    pass

class AvatarInDBBase(AvatarBase):
    id: int

    class Config:
         from_attributes = True

class Avatar(AvatarInDBBase):
    pass

class AvatarInDB(AvatarInDBBase):
    pass
